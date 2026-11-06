// Learner accounts: /api/learner/*
//
// Optional accounts for learners 13 and older. An account only syncs what the browser
// already keeps on its own (the notebook of highlights and notes, and progress) between
// a learner's devices. Sign-in is Google (OAuth 2.0 code flow with PKCE, no client
// library) or a passkey (WebAuthn via @simplewebauthn/server). There are no passwords.
//
// Security, as in the rest of the API (worker/api.js): the session cookie bp_learner is
// HttpOnly, SameSite=Lax, Secure on https, and only its SHA-256 is stored; every request
// that changes state is same-origin JSON (checked in handleApi before we get here); the
// Google callback is bound to the browser that started it by a one-time state cookie.
// A second, readable cookie bp_signed_in=1 holds no secret: it only tells the page
// header to show the learner's name and to sync, so signed-out visitors make no calls.
//
// Nothing here calls a paid service. Google sign-in is free; D1 and Workers are free tier.

import { generateRegistrationOptions, verifyRegistrationResponse, generateAuthenticationOptions, verifyAuthenticationResponse } from '@simplewebauthn/server';
import { sha256Hex, randomToken, readCookie, cookie } from './auth.js';
import { json, fail, clean, clientKey, allow } from './util.js';
import { mergeNotebookItems, mergeProgress, validProgress, validNoteItem } from '../src/lib/learner-merge.mjs';

export const LEARNER_COOKIE = 'bp_learner';
const HINT_COOKIE = 'bp_signed_in';
const FLOW_COOKIE = 'bp_learner_flow';
const SESSION_DAYS = 365;
const FLOW_MS = 10 * 60 * 1000;
const MAX_SYNC_BYTES = 1024 * 1024;
const MAX_ITEMS = 10_000;
const NAME_MAX = 40;
const DELETE_WORD = 'DELETE';
const RP_NAME = 'Biochemistrypedia';

// ---- small helpers --------------------------------------------------------------------
const b64url = (bytes) => btoa(String.fromCharCode(...new Uint8Array(bytes))).replace(/\+/g, '-').replace(/\//g, '_').replace(/=+$/, '');
const unb64url = (s) => {
  const t = String(s).replace(/-/g, '+').replace(/_/g, '/');
  return Uint8Array.from(atob(t + '='.repeat((4 - (t.length % 4)) % 4)), (c) => c.charCodeAt(0));
};
const enc = new TextEncoder();

function hintCookie(request, on) {
  const secure = new URL(request.url).protocol === 'https:' ? '; Secure' : '';
  return `${HINT_COOKIE}=${on ? '1' : ''}; Path=/; SameSite=Lax; Max-Age=${on ? SESSION_DAYS * 86400 : 0}${secure}`;
}
const flowCookie = (request, value) => cookie(FLOW_COOKIE, value, request, value ? FLOW_MS / 1000 : 0);

/** Several Set-Cookie headers on one response. */
function withCookies(res, cookies) {
  for (const c of cookies) res.headers.append('Set-Cookie', c);
  return res;
}
const redirect = (location, cookies = []) => withCookies(new Response(null, { status: 302, headers: { Location: location, 'Cache-Control': 'no-store' } }), cookies);

/** Only a path on this site: "/x/y?z", never "//evil.com" or "https://…". */
function safeReturn(r) {
  const s = String(r || '');
  return /^\/(?![\/\\])[^\s]*$/.test(s) && s.length < 300 ? s : '/account/';
}

const googleOn = (env) => !!(env.GOOGLE_CLIENT_ID && env.GOOGLE_CLIENT_SECRET);

/** The test-only path exists only under `wrangler dev` with LEARNER_TEST=1, on a local host. */
function testMode(env, request) {
  const host = new URL(request.url).hostname;
  return env.LEARNER_TEST === '1' && (host === 'localhost' || host === '127.0.0.1' || host === '[::1]' || host.endsWith('.localhost'));
}

async function readJson(request, max = 64 * 1024) {
  const len = Number(request.headers.get('Content-Length') || 0);
  if (len > max) return { tooBig: true };
  let text;
  try { text = await request.text(); } catch { return null; }
  if (text.length > max) return { tooBig: true };
  try { return JSON.parse(text); } catch { return null; }
}

// ---- sessions --------------------------------------------------------------------------
export async function getLearner(db, request) {
  const token = readCookie(request, LEARNER_COOKIE);
  if (!token || !/^[0-9a-f]{64}$/.test(token)) return null;
  const row = await db.prepare(
    `SELECT l.id, l.display_name, l.email, l.google_sub, l.created_at, l.last_active_at, s.expires_at
       FROM learner_sessions s JOIN learners l ON l.id = s.learner_id WHERE s.token_hash = ?`).bind(await sha256Hex(token)).first();
  if (!row || row.expires_at < Date.now()) return null;
  return { ...row, token };
}

async function startSession(db, request, learnerId) {
  const token = randomToken();
  const now = Date.now();
  if (Math.random() < 0.05) {
    await db.prepare('DELETE FROM learner_sessions WHERE expires_at < ?').bind(now).run().catch(() => {});
  }
  await db.batch([
    db.prepare('INSERT INTO learner_sessions (token_hash, learner_id, created_at, expires_at) VALUES (?,?,?,?)')
      .bind(await sha256Hex(token), learnerId, now, now + SESSION_DAYS * 86_400_000),
    db.prepare('UPDATE learners SET last_active_at=? WHERE id=?').bind(now, learnerId),
  ]);
  return [cookie(LEARNER_COOKIE, token, request, SESSION_DAYS * 86400), hintCookie(request, true)];
}

async function createLearner(db, { id = randomToken(16), name, email = null, googleSub = null }) {
  const now = Date.now();
  await db.batch([
    db.prepare('INSERT INTO learners (id, display_name, email, google_sub, created_at, last_active_at) VALUES (?,?,?,?,?,?)')
      .bind(id, name, email, googleSub, now, now),
    db.prepare("INSERT INTO learner_data (learner_id, notebook_json, progress_json, updated_at) VALUES (?, '{}', '{}', 0)").bind(id),
  ]);
  return id;
}

// ---- sign-in flows in progress (WebAuthn challenges, Google state) --------------------
async function startFlow(db, purpose, challenge, { learnerId = null, displayName = null, extra = null } = {}) {
  const raw = randomToken();
  const now = Date.now();
  if (Math.random() < 0.1) await db.prepare('DELETE FROM learner_challenges WHERE expires_at < ?').bind(now).run().catch(() => {});
  await db.prepare('INSERT INTO learner_challenges (id, purpose, challenge, learner_id, display_name, extra, created_at, expires_at) VALUES (?,?,?,?,?,?,?,?)')
    .bind(await sha256Hex(raw), purpose, challenge, learnerId, displayName, extra, now, now + FLOW_MS).run();
  return raw;
}

/** Take (and delete) the flow this browser started. One use only. */
async function takeFlow(db, raw, purpose) {
  if (!raw || !/^[0-9a-f]{64}$/.test(raw)) return null;
  const id = await sha256Hex(raw);
  const row = await db.prepare('SELECT * FROM learner_challenges WHERE id=? AND purpose=?').bind(id, purpose).first();
  if (!row) return null;
  await db.prepare('DELETE FROM learner_challenges WHERE id=?').bind(id).run();
  return row.expires_at >= Date.now() ? row : null;
}

// ---- Google ID token check (RS256 against Google's published keys) ---------------------
let jwksCache = { keys: null, until: 0 };
async function googleKeys(force = false) {
  if (!force && jwksCache.keys && jwksCache.until > Date.now()) return jwksCache.keys;
  const r = await fetch('https://www.googleapis.com/oauth2/v3/certs');
  if (!r.ok) throw new Error('jwks ' + r.status);
  const { keys } = await r.json();
  const maxAge = Number(/max-age=(\d+)/.exec(r.headers.get('Cache-Control') || '')?.[1] || 3600);
  jwksCache = { keys, until: Date.now() + Math.min(maxAge, 86400) * 1000 };
  return keys;
}

export async function verifyGoogleIdToken(idToken, clientId, nonce, keysFn = googleKeys) {
  const parts = String(idToken || '').split('.');
  if (parts.length !== 3) throw new Error('bad token');
  const header = JSON.parse(new TextDecoder().decode(unb64url(parts[0])));
  const claims = JSON.parse(new TextDecoder().decode(unb64url(parts[1])));
  if (header.alg !== 'RS256') throw new Error('bad alg');
  let jwk = (await keysFn()).find((k) => k.kid === header.kid);
  if (!jwk) jwk = (await keysFn(true)).find((k) => k.kid === header.kid);   // keys rotate
  if (!jwk) throw new Error('unknown key');
  const key = await crypto.subtle.importKey('jwk', { kty: jwk.kty, n: jwk.n, e: jwk.e, alg: 'RS256', ext: true },
    { name: 'RSASSA-PKCS1-v1_5', hash: 'SHA-256' }, false, ['verify']);
  const ok = await crypto.subtle.verify('RSASSA-PKCS1-v1_5', key, unb64url(parts[2]), enc.encode(`${parts[0]}.${parts[1]}`));
  if (!ok) throw new Error('bad signature');
  const now = Math.floor(Date.now() / 1000);
  if (claims.iss !== 'https://accounts.google.com' && claims.iss !== 'accounts.google.com') throw new Error('bad iss');
  const aud = Array.isArray(claims.aud) ? claims.aud : [claims.aud];
  if (!aud.includes(clientId)) throw new Error('bad aud');
  if (!(claims.exp > now - 60)) throw new Error('expired');
  if (claims.iat && claims.iat > now + 300) throw new Error('issued in the future');
  if (nonce && claims.nonce !== nonce) throw new Error('bad nonce');
  if (claims.email_verified !== true && claims.email_verified !== 'true') throw new Error('email not verified');
  if (!claims.sub) throw new Error('no sub');
  return claims;
}

async function pkceChallenge(verifier) {
  return b64url(await crypto.subtle.digest('SHA-256', enc.encode(verifier)));
}

// ---- the learner's view ---------------------------------------------------------------
async function meView(db, env, l) {
  const pk = await db.prepare('SELECT COUNT(*) AS n FROM learner_passkeys WHERE learner_id=?').bind(l.id).first();
  const data = await db.prepare('SELECT updated_at FROM learner_data WHERE learner_id=?').bind(l.id).first();
  const methods = [];
  if (l.google_sub) methods.push('google');
  if (pk?.n) methods.push('passkey');
  return {
    signedIn: true, name: l.display_name, ...(l.email ? { email: l.email } : {}), methods,
    passkeys: pk?.n || 0, created: l.created_at, lastSynced: data?.updated_at || null,
    googleAvailable: googleOn(env),
  };
}

// ---- sync ------------------------------------------------------------------------------
async function readData(db, learnerId) {
  const row = await db.prepare('SELECT notebook_json, progress_json, updated_at FROM learner_data WHERE learner_id=?').bind(learnerId).first();
  let items = {}, progress = { v: 1, lessons: {}, items: {} };
  try { const n = JSON.parse(row?.notebook_json || '{}'); if (n && typeof n === 'object') items = n; } catch { /* keep empty */ }
  try { const p = JSON.parse(row?.progress_json || '{}'); if (validProgress(p)) progress = p; } catch { /* keep empty */ }
  return { items, progress, updatedAt: row?.updated_at ?? null, exists: !!row };
}

/** Merge what a device sent into what the server holds. Retries if another device wrote meanwhile. */
async function mergeAndStore(db, learnerId, incoming) {
  for (let attempt = 0; attempt < 4; attempt++) {
    const cur = await readData(db, learnerId);
    const items = mergeNotebookItems(cur.items, incoming.items);
    const progress = mergeProgress(cur.progress, incoming.progress);
    const nb = JSON.stringify(items);
    const pr = JSON.stringify(progress);
    if (nb.length + pr.length > MAX_SYNC_BYTES * 2) return { error: 'too big' };
    const now = Date.now();
    let res;
    if (!cur.exists) {
      res = await db.prepare('INSERT OR IGNORE INTO learner_data (learner_id, notebook_json, progress_json, updated_at) VALUES (?,?,?,?)')
        .bind(learnerId, nb, pr, now).run();
    } else {
      // Optimistic: only write if nobody else wrote since we read.
      res = await db.prepare('UPDATE learner_data SET notebook_json=?, progress_json=?, updated_at=? WHERE learner_id=? AND updated_at=?')
        .bind(nb, pr, Math.max(now, cur.updatedAt + 1), learnerId, cur.updatedAt).run();
    }
    if (res.meta?.changes) {
      await db.prepare('UPDATE learners SET last_active_at=? WHERE id=?').bind(now, learnerId).run();
      return { items, progress, serverTime: Math.max(now, (cur.updatedAt ?? 0) + 1) };
    }
  }
  return { error: 'busy' };
}

function cleanIncoming(b) {
  const rawItems = b?.notebook?.items;
  const items = {};
  if (rawItems && typeof rawItems === 'object' && !Array.isArray(rawItems)) {
    let n = 0;
    for (const [id, it] of Object.entries(rawItems)) {
      if (!validNoteItem(it, id)) continue;
      if (++n > MAX_ITEMS) break;
      items[id] = it;
    }
  }
  const progress = validProgress(b?.progress) ? b.progress : null;
  return { items, progress };
}

// ---- delete: every learner table is here ---------------------------------------------
async function deleteLearner(db, id) {
  await db.batch([
    db.prepare('DELETE FROM learner_challenges WHERE learner_id=?').bind(id),
    db.prepare('DELETE FROM learner_sessions WHERE learner_id=?').bind(id),
    db.prepare('DELETE FROM learner_passkeys WHERE learner_id=?').bind(id),
    db.prepare('DELETE FROM learner_data WHERE learner_id=?').bind(id),
    db.prepare('DELETE FROM learners WHERE id=?').bind(id),
  ]);
}

// ---- router ----------------------------------------------------------------------------
/** Returns a Response for /api/learner/* paths, or null for anything else. */
export async function handleLearner(request, env, db, path, method, url) {
  if (!path.startsWith('/api/learner/')) return null;
  const sub = path.slice('/api/learner'.length);
  const ip = await clientKey(request);
  const signinLimit = () => allow(db, 'lsign:' + ip, 30, 60_000);
  const origin = url.origin;
  // www.biochemistrypedia.com serves the site too (no redirect), so passkeys are tied to the parent
  // domain: one passkey then works on both hostnames. Google sign-in always returns to the bare
  // domain, so only one redirect URI needs registering.
  const SITE = 'biochemistrypedia.com';
  const onSite = url.hostname === SITE || url.hostname.endsWith('.' + SITE);
  const rpID = onSite ? SITE : url.hostname;
  const googleOrigin = onSite ? `https://${SITE}` : origin;

  if (sub === '/me' && method === 'GET') {
    const l = await getLearner(db, request);
    if (!l) {
      const res = json({ signedIn: false, googleAvailable: googleOn(env) });
      // A stale hint (session expired or deleted elsewhere) is cleared so the header stops asking.
      return readCookie(request, HINT_COOKIE) ? withCookies(res, [hintCookie(request, false)]) : res;
    }
    return json(await meView(db, env, l));
  }

  // ---------- Google ----------
  if (sub === '/google/start' && method === 'GET') {
    const ret = safeReturn(url.searchParams.get('return'));
    // Start on the bare domain, so the state cookie and the callback share one hostname.
    if (onSite && url.hostname !== SITE) return redirect(`https://${SITE}${url.pathname}${url.search}`);
    if (!googleOn(env)) return redirect('/account/?error=google-off');
    if (!(await signinLimit())) return redirect('/account/?error=busy');
    const current = await getLearner(db, request);
    const verifier = randomToken(32);
    const nonce = randomToken(16);
    const age = url.searchParams.get('age') === '1';
    const raw = await startFlow(db, 'google', verifier, { learnerId: current?.id ?? null, extra: JSON.stringify({ nonce, ret, age }) });
    const q = new URLSearchParams({
      client_id: env.GOOGLE_CLIENT_ID,
      redirect_uri: `${googleOrigin}/api/learner/google/callback`,
      response_type: 'code',
      scope: 'openid email profile',
      state: raw,
      nonce,
      code_challenge: await pkceChallenge(verifier),
      code_challenge_method: 'S256',
      prompt: 'select_account',
    });
    return redirect(`https://accounts.google.com/o/oauth2/v2/auth?${q}`, [flowCookie(request, raw)]);
  }

  if (sub === '/google/callback' && method === 'GET') {
    const clear = [flowCookie(request, '')];
    const state = url.searchParams.get('state') || '';
    const code = url.searchParams.get('code') || '';
    if (!googleOn(env)) return redirect('/account/?error=google-off', clear);
    if (!(await signinLimit())) return redirect('/account/?error=busy', clear);
    // The state must match the cookie this browser got at /google/start.
    if (!state || state !== readCookie(request, FLOW_COOKIE)) return redirect('/account/?error=google-state', clear);
    const flow = await takeFlow(db, state, 'google');
    if (!flow) return redirect('/account/?error=google-state', clear);
    if (url.searchParams.get('error') || !code) return redirect('/account/?error=google-cancel', clear);
    let extra = {};
    try { extra = JSON.parse(flow.extra || '{}'); } catch { /* none */ }

    let claims;
    try {
      const tr = await fetch('https://oauth2.googleapis.com/token', {
        method: 'POST',
        headers: { 'Content-Type': 'application/x-www-form-urlencoded' },
        body: new URLSearchParams({
          code, client_id: env.GOOGLE_CLIENT_ID, client_secret: env.GOOGLE_CLIENT_SECRET,
          redirect_uri: `${googleOrigin}/api/learner/google/callback`, grant_type: 'authorization_code', code_verifier: flow.challenge,
        }),
      });
      const tok = await tr.json().catch(() => ({}));
      if (!tr.ok || !tok.id_token) throw new Error('token exchange ' + tr.status);
      claims = await verifyGoogleIdToken(tok.id_token, env.GOOGLE_CLIENT_ID, extra.nonce);
    } catch (e) {
      console.error('google sign-in failed', e && e.message);
      return redirect('/account/?error=google-failed', clear);
    }
    const sub_ = String(claims.sub);
    const email = typeof claims.email === 'string' ? claims.email.toLowerCase().slice(0, 200) : null;
    const name = clean(claims.given_name || claims.name || (email ? email.split('@')[0] : 'Learner'), NAME_MAX) || 'Learner';
    const owner = await db.prepare('SELECT id FROM learners WHERE google_sub=?').bind(sub_).first();

    if (flow.learner_id) {
      // Signed in already: link this Google account to the current learner.
      if (owner && owner.id !== flow.learner_id) return redirect('/account/?error=google-in-use', clear);
      await db.prepare('UPDATE learners SET google_sub=?, email=? WHERE id=?').bind(sub_, email, flow.learner_id).run();
      return redirect(safeReturn(extra.ret), clear);
    }
    let id = owner?.id;
    if (!id) {
      if (!extra.age) return redirect('/account/?error=age', clear);
      id = await createLearner(db, { name, email, googleSub: sub_ });
    } else if (email) {
      await db.prepare('UPDATE learners SET email=? WHERE id=?').bind(email, id).run();
    }
    return redirect(safeReturn(extra.ret), [...clear, ...(await startSession(db, request, id))]);
  }

  // ---------- passkeys ----------
  if (sub === '/passkey/register/options' && method === 'POST') {
    if (!(await signinLimit())) return fail(429, 'Too many tries from here. Wait a minute and try again.');
    const b = await readJson(request);
    const current = await getLearner(db, request);
    let userId, name, displayName = null, learnerId = null;
    let exclude = [];
    if (current) {
      learnerId = current.id;
      userId = current.id;
      name = current.display_name;
      exclude = ((await db.prepare('SELECT credential_id, transports FROM learner_passkeys WHERE learner_id=?').bind(current.id).all()).results || [])
        .map((r) => ({ id: r.credential_id, transports: safeArr(r.transports) }));
    } else {
      displayName = clean(b?.displayName, NAME_MAX);
      if (!displayName) return fail(400, 'Please choose a name to show on your account.');
      if (b?.age13 !== true) return fail(400, 'Accounts are for people 13 and older.');
      userId = randomToken(16);
      name = displayName;
    }
    const options = await generateRegistrationOptions({
      rpName: RP_NAME, rpID, userName: name, userDisplayName: name, userID: enc.encode(userId),
      attestationType: 'none', excludeCredentials: exclude,
      authenticatorSelection: { residentKey: 'required', userVerification: 'preferred' },
    });
    const raw = await startFlow(db, 'register', options.challenge, { learnerId, displayName, extra: userId });
    return json({ options }, 200, { 'Set-Cookie': flowCookie(request, raw) });
  }

  if (sub === '/passkey/register/verify' && method === 'POST') {
    if (!(await signinLimit())) return fail(429, 'Too many tries from here. Wait a minute and try again.');
    const b = await readJson(request);
    const flow = await takeFlow(db, readCookie(request, FLOW_COOKIE), 'register');
    const clear = flowCookie(request, '');
    if (!flow) return withCookies(fail(400, 'That took too long. Please try again.'), [clear]);
    let v;
    try {
      v = await verifyRegistrationResponse({ response: b?.response, expectedChallenge: flow.challenge, expectedOrigin: origin, expectedRPID: rpID, requireUserVerification: false });
    } catch (e) {
      return withCookies(fail(400, 'The passkey could not be checked. Please try again.', { detail: String(e?.message || e).slice(0, 200) }), [clear]);
    }
    if (!v.verified) return withCookies(fail(400, 'The passkey could not be checked. Please try again.'), [clear]);
    const cred = v.registrationInfo.credential;
    if (await db.prepare('SELECT 1 FROM learner_passkeys WHERE credential_id=?').bind(cred.id).first()) {
      return withCookies(fail(409, 'That passkey is already on an account.'), [clear]);
    }
    let learnerId = flow.learner_id;
    const cookies = [clear];
    if (learnerId) {
      // Adding a passkey: the same learner must still be signed in.
      const current = await getLearner(db, request);
      if (!current || current.id !== learnerId) return withCookies(fail(401, 'Please sign in again.'), [clear]);
    } else {
      learnerId = await createLearner(db, { id: flow.extra, name: flow.display_name || 'Learner' });
    }
    await db.prepare('INSERT INTO learner_passkeys (credential_id, learner_id, public_key, counter, transports, created_at) VALUES (?,?,?,?,?,?)')
      .bind(cred.id, learnerId, b64url(cred.publicKey), cred.counter || 0, JSON.stringify(cred.transports || b?.response?.response?.transports || []), Date.now()).run();
    if (!flow.learner_id) cookies.push(...(await startSession(db, request, learnerId)));
    const l = await db.prepare('SELECT display_name FROM learners WHERE id=?').bind(learnerId).first();
    return withCookies(json({ ok: true, name: l?.display_name }), cookies);
  }

  if (sub === '/passkey/login/options' && method === 'POST') {
    if (!(await signinLimit())) return fail(429, 'Too many tries from here. Wait a minute and try again.');
    const options = await generateAuthenticationOptions({ rpID, userVerification: 'preferred', allowCredentials: [] });
    const raw = await startFlow(db, 'login', options.challenge);
    return json({ options }, 200, { 'Set-Cookie': flowCookie(request, raw) });
  }

  if (sub === '/passkey/login/verify' && method === 'POST') {
    if (!(await signinLimit())) return fail(429, 'Too many tries from here. Wait a minute and try again.');
    const b = await readJson(request);
    const flow = await takeFlow(db, readCookie(request, FLOW_COOKIE), 'login');
    const clear = flowCookie(request, '');
    if (!flow) return withCookies(fail(400, 'That took too long. Please try again.'), [clear]);
    const credId = typeof b?.response?.id === 'string' ? b.response.id : '';
    const pk = credId && await db.prepare('SELECT * FROM learner_passkeys WHERE credential_id=?').bind(credId).first();
    if (!pk) return withCookies(fail(404, 'This passkey is not on any account here. It may have been deleted.'), [clear]);
    let v;
    try {
      v = await verifyAuthenticationResponse({
        response: b.response, expectedChallenge: flow.challenge, expectedOrigin: origin, expectedRPID: rpID, requireUserVerification: false,
        credential: { id: pk.credential_id, publicKey: unb64url(pk.public_key), counter: pk.counter || 0, transports: safeArr(pk.transports) },
      });
    } catch (e) {
      return withCookies(fail(400, 'The passkey could not be checked. Please try again.', { detail: String(e?.message || e).slice(0, 200) }), [clear]);
    }
    if (!v.verified) return withCookies(fail(400, 'The passkey could not be checked. Please try again.'), [clear]);
    await db.prepare('UPDATE learner_passkeys SET counter=? WHERE credential_id=?').bind(v.authenticationInfo.newCounter || 0, pk.credential_id).run();
    const l = await db.prepare('SELECT display_name FROM learners WHERE id=?').bind(pk.learner_id).first();
    return withCookies(json({ ok: true, name: l?.display_name }), [clear, ...(await startSession(db, request, pk.learner_id))]);
  }

  // ---------- session ----------
  if (sub === '/logout' && method === 'POST') {
    const token = readCookie(request, LEARNER_COOKIE);
    if (token && /^[0-9a-f]{64}$/.test(token)) await db.prepare('DELETE FROM learner_sessions WHERE token_hash=?').bind(await sha256Hex(token)).run();
    return withCookies(json({ ok: true }), [cookie(LEARNER_COOKIE, '', request, 0), hintCookie(request, false)]);
  }

  // ---------- test-only: make a learner without Google or a passkey ----------
  if (sub === '/test/create' && method === 'POST') {
    if (!testMode(env, request)) return fail(404, 'Not found.');
    const b = await readJson(request);
    const id = await createLearner(db, { name: clean(b?.name, NAME_MAX) || 'Test learner' });
    return withCookies(json({ ok: true, id }), await startSession(db, request, id));
  }
  if (sub === '/test/session' && method === 'POST') {
    // A second "device" for an existing test learner.
    if (!testMode(env, request)) return fail(404, 'Not found.');
    const b = await readJson(request);
    const l = await db.prepare('SELECT id FROM learners WHERE id=?').bind(String(b?.id || '')).first();
    if (!l) return fail(404, 'No such learner.');
    return withCookies(json({ ok: true }), await startSession(db, request, l.id));
  }

  // Everything below needs a signed-in learner.
  const l = await getLearner(db, request);
  if (!l) return withCookies(fail(401, 'Not signed in.'), readCookie(request, HINT_COOKIE) ? [hintCookie(request, false)] : []);

  if (sub === '/sync' && method === 'GET') {
    if (!(await allow(db, 'lsync:' + ip, 60, 60_000))) return fail(429, 'Syncing too often. It will try again shortly.');
    const d = await readData(db, l.id);
    return json({ notebook: { items: d.items }, progress: d.progress, serverTime: d.updatedAt || Date.now() });
  }

  if (sub === '/sync' && method === 'PUT') {
    if (!(await allow(db, 'lsync:' + ip, 60, 60_000))) return fail(429, 'Syncing too often. It will try again shortly.');
    const b = await readJson(request, MAX_SYNC_BYTES);
    if (b?.tooBig) return fail(413, 'Your notebook is too big to sync (over 1 MB).');
    if (!b) return fail(400, 'Bad sync data.');
    const r = await mergeAndStore(db, l.id, cleanIncoming(b));
    if (r.error === 'too big') return fail(413, 'Your notebook is too big to sync (over 1 MB).');
    if (r.error) return fail(503, 'Another device is syncing. Try again in a moment.');
    return json({ notebook: { items: r.items }, progress: r.progress, serverTime: r.serverTime });
  }

  if (sub === '/export' && method === 'GET') {
    if (!(await allow(db, 'lexport:' + ip, 10, 60_000))) return fail(429, 'Too many downloads. Wait a minute.');
    const d = await readData(db, l.id);
    const passkeys = ((await db.prepare('SELECT credential_id, public_key, counter, transports, created_at FROM learner_passkeys WHERE learner_id=?').bind(l.id).all()).results || [])
      .map((p) => ({ credentialId: p.credential_id, publicKey: p.public_key, counter: p.counter, transports: safeArr(p.transports), created: iso(p.created_at) }));
    const sessions = ((await db.prepare('SELECT created_at, expires_at FROM learner_sessions WHERE learner_id=? ORDER BY created_at').bind(l.id).all()).results || [])
      .map((s) => ({ created: iso(s.created_at), expires: iso(s.expires_at) }));
    const out = {
      site: 'biochemistrypedia.com',
      exported: new Date().toISOString(),
      note: 'Everything Biochemistrypedia holds about your account. Signed-in devices are listed by date only; their keys are stored as one-way hashes and are not included.',
      account: {
        name: l.display_name, email: l.email, googleLinked: !!l.google_sub, googleAccountId: l.google_sub,
        created: iso(l.created_at), lastActive: iso(l.last_active_at),
      },
      passkeys, sessions,
      lastSynced: d.updatedAt ? iso(d.updatedAt) : null,
      notebook: { v: 1, items: d.items },
      progress: d.progress,
    };
    return new Response(JSON.stringify(out, null, 1), {
      headers: {
        'Content-Type': 'application/json; charset=utf-8', 'Cache-Control': 'no-store',
        'Content-Disposition': `attachment; filename="biochemistrypedia-account-${new Date().toISOString().slice(0, 10)}.json"`,
      },
    });
  }

  if (sub === '/delete' && method === 'POST') {
    const b = await readJson(request);
    if (String(b?.confirm || '').trim().toUpperCase() !== DELETE_WORD) return fail(400, `Type ${DELETE_WORD} to confirm.`);
    await deleteLearner(db, l.id);
    return withCookies(json({ ok: true, deleted: true }), [cookie(LEARNER_COOKIE, '', request, 0), hintCookie(request, false), flowCookie(request, '')]);
  }

  return fail(404, 'Not found.');
}

function safeArr(s) {
  try { const a = JSON.parse(s || '[]'); return Array.isArray(a) ? a.filter((x) => typeof x === 'string') : []; } catch { return []; }
}
const iso = (ms) => (ms ? new Date(ms).toISOString() : null);
