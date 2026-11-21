// The owner's totals, the optional role question and the anonymous film counter, in Node with no network:
//   node scripts/test-admin.mjs
// (worker/admin.js, worker/film-count.js, the role parts of worker/learner.js and worker/handoff.js,
// src/lib/prefs.ts.) D1 is an in-memory SQLite shim loaded with the real migrations, once WITH
// migration 0009 and once WITHOUT it, because the code ships before the migration is applied.
// Passkey sign-up is driven for real: the test plays the authenticator (a P-256 key and a "none"
// attestation), so the role is followed from the sign-up request to the stored row. Google is a
// stub (global fetch) that signs its own ID token; nothing here can reach a real service.
import { register } from 'node:module';
import { DatabaseSync } from 'node:sqlite';
import { readFileSync, readdirSync } from 'node:fs';
import crypto, { createHash } from 'node:crypto';
import assert from 'node:assert/strict';

// worker/ai.js imports a .json file without an import attribute, which wrangler's bundler allows and Node does not.
register('data:text/javascript,' + encodeURIComponent(`export async function load(u,c,n){return u.endsWith('.json')?n(u,{...c,importAttributes:{type:'json'}}):n(u,c)}`));
const { handleApi } = await import('../worker/api.js');
const { createWorker } = await import('../worker/index.js');
const ADMIN = await import('../worker/admin.js');
const HO = await import('../worker/handoff.js');
const { sha256Hex } = await import('../worker/auth.js');
const { clientKey } = await import('../worker/util.js');
const FILM = await import('../worker/film-count.js');
const LEARNER = await import('../worker/learner.js');

let n = 0;
const check = async (name, fn) => { await fn(); n++; console.log('  ok  ' + name); };
const src = (p) => readFileSync(new URL('../' + p, import.meta.url), 'utf8');

// ---- an in-memory D1 with the real migrations; `before` stops short of 0009 -------------------
function makeDb({ before0009 = false, before0011 = false } = {}) {
  const sql = new DatabaseSync(':memory:');
  const dir = new URL('../migrations/', import.meta.url);
  for (const f of readdirSync(dir).sort()) {
    if ((before0009 && f >= '0009') || (before0011 && f >= '0011')) continue;
    sql.exec(readFileSync(new URL(f, dir), 'utf8'));
  }
  const seen = [];   // every SQL statement run, for the "aggregates only" check
  const stmt = (q, args = []) => ({
    bind: (...a) => stmt(q, a),
    run: async () => { seen.push(q); return { meta: { changes: Number(sql.prepare(q).run(...args).changes) } }; },
    first: async () => { seen.push(q); return sql.prepare(q).get(...args) ?? null; },
    all: async () => { seen.push(q); return { results: sql.prepare(q).all(...args) }; },
    _run: () => { seen.push(q); return sql.prepare(q).run(...args); },
  });
  return { prepare: (q) => stmt(q), batch: async (ss) => ss.map((s) => ({ meta: { changes: Number(s._run().changes) } })), sql, seen };
}

// ---- the site's catalog, as the Worker reads it (src/pages/usage-catalog.json.ts) -------------
const CATALOG = {
  levels: [['grade-7', 'Grade 7'], ['college-core', 'College: the core'], ['college-further', 'College: going further']],
  courses: { 'life-science': ['Life Science', 'grade-7'], genetics: ['Genetics', 'college-core'], 'cell-biology': ['Cell Biology', 'college-core'], biochemistry: ['Biochemistry', 'college-further'] },
  lessons: { glycolysis: ['Glycolysis', 'biochemistry'], osmosis: ['Osmosis', 'life-science'], mitosis: ['Mitosis', 'cell-biology'], 'mendel-peas': ['Mendel and his peas', 'genetics'] },
  films: { 'glycolysis/explainer': ['Glycolysis', 'biochemistry'], 'osmosis/explainer': ['Osmosis', 'life-science'], 'method-pcr/explainer': ['PCR', ''] },
};
const ASSETS = { fetch: async (req) => (new URL(req.url).pathname === '/usage-catalog.json' ? new Response(JSON.stringify(CATALOG)) : new Response('no', { status: 404 })) };

const ORIGIN = 'http://localhost:8787';
const SECRET = 'test-secret-0123456789-abcdefghij';   // 33 characters; not a real secret
async function call(env, method, path, { body, cookie, headers = {}, origin = ORIGIN, json = true } = {}) {
  const res = await handleApi(new Request(origin + path, {
    method, redirect: 'manual',
    headers: { ...(json && method !== 'GET' ? { 'Content-Type': 'application/json', Origin: origin } : {}), ...(cookie ? { Cookie: cookie } : {}), ...headers },
    ...(body !== undefined ? { body: typeof body === 'string' ? body : JSON.stringify(body) } : {}),
  }), env);
  const set = res.headers.getSetCookie?.() ?? [];
  const text = await res.text();
  let data = null; try { data = JSON.parse(text); } catch { /* not JSON */ }
  return { status: res.status, text, data, headers: res.headers, cookie: set.map((c) => c.split(';')[0]).filter((c) => !c.endsWith('=')).join('; ') };
}
const admin = (env, { token = SECRET, path = '/api/admin/stats', headers = {}, ip = '198.51.100.1' } = {}) =>
  call(env, 'GET', path, { headers: { ...(token ? { Authorization: `Bearer ${token}` } : {}), 'CF-Connecting-IP': ip, ...headers } });

// ---- a passkey authenticator, just enough of one -----------------------------------------------
const cat = (...parts) => Buffer.concat(parts.map((p) => Buffer.from(p)));
const head = (major, len) => (len < 24 ? Buffer.from([(major << 5) | len]) : len < 256 ? Buffer.from([(major << 5) | 24, len]) : Buffer.from([(major << 5) | 25, len >> 8, len & 255]));
function cbor(x) {
  if (typeof x === 'number') return x >= 0 ? head(0, x) : head(1, -1 - x);
  if (typeof x === 'string') { const b = Buffer.from(x, 'utf8'); return cat(head(3, b.length), b); }
  if (x instanceof Uint8Array) return cat(head(2, x.length), x);
  if (x instanceof Map) return cat(head(5, x.size), ...[...x].flatMap(([k, v]) => [cbor(k), cbor(v)]));
  throw new Error('cbor: unsupported');
}
function attest(origin, rpId, challenge) {
  const jwk = crypto.generateKeyPairSync('ec', { namedCurve: 'P-256' }).publicKey.export({ format: 'jwk' });
  const cose = cbor(new Map([[1, 2], [3, -7], [-1, 1], [-2, Buffer.from(jwk.x, 'base64url')], [-3, Buffer.from(jwk.y, 'base64url')]]));
  const credId = crypto.randomBytes(16);
  const authData = cat(createHash('sha256').update(rpId).digest(), [0x45], [0, 0, 0, 0], Buffer.alloc(16), [0, credId.length], credId, cose);
  const att = cbor(new Map([['fmt', 'none'], ['attStmt', new Map()], ['authData', authData]]));
  const id = credId.toString('base64url');
  return {
    id, rawId: id, type: 'public-key', clientExtensionResults: {},
    response: { clientDataJSON: Buffer.from(JSON.stringify({ type: 'webauthn.create', challenge, origin, crossOrigin: false })).toString('base64url'), attestationObject: att.toString('base64url'), transports: ['internal'] },
  };
}
/** Sign up with a passkey through `send(method, path, opts)`; returns the new session cookie. */
async function passkeySignUp(send, origin, rpId, fields) {
  const o = await send('POST', '/api/learner/passkey/register/options', { body: fields, origin });
  assert.equal(o.status, 200, o.text);
  const v = await send('POST', '/api/learner/passkey/register/verify', { body: { response: attest(origin, rpId, o.data.options.challenge) }, cookie: o.cookie, origin });
  assert.equal(v.status, 200, v.text);
  return v.cookie;
}

// ---- Google, stubbed: a token endpoint and a key set that sign for this test only ---------------
const rsa = crypto.generateKeyPairSync('rsa', { modulusLength: 2048 });
const googleJwk = { ...rsa.publicKey.export({ format: 'jwk' }), kid: 'test-kid', alg: 'RS256', use: 'sig' };
let nextClaims = null;
const b64 = (o) => Buffer.from(JSON.stringify(o)).toString('base64url');
globalThis.fetch = async (url) => {
  if (String(url) === 'https://www.googleapis.com/oauth2/v3/certs') return new Response(JSON.stringify({ keys: [googleJwk] }));
  if (String(url) === 'https://oauth2.googleapis.com/token') {
    const body = `${b64({ alg: 'RS256', kid: 'test-kid', typ: 'JWT' })}.${b64(nextClaims)}`;
    return new Response(JSON.stringify({ id_token: `${body}.${crypto.sign('RSA-SHA256', Buffer.from(body), rsa.privateKey).toString('base64url')}` }));
  }
  throw new Error('unexpected network call: ' + url);
};

const roleOf = (db, cookieOrId) => db.sql.prepare('SELECT role FROM learners WHERE id=?').get(cookieOrId)?.role;
const newestLearner = (db) => db.sql.prepare('SELECT id, role, display_name FROM learners ORDER BY rowid DESC LIMIT 1').get();
const filmRows = (db) => db.sql.prepare('SELECT * FROM film_counts ORDER BY film_key, day').all().map((r) => ({ ...r }));

// =================================================================================================
console.log('before migration 0009 (the code ships first)');
{
  const db = makeDb({ before0009: true });
  const env = { CLASSES: db, ASSETS, LEARNER_TEST: '1', ADMIN_TOKEN: SECRET };
  const made = await call(env, 'POST', '/api/learner/test/create', { body: { name: 'Ada' } });
  const ada = made.cookie;

  await check('/me says nothing about roles, signed out or signed in', async () => {
    const out = await call(env, 'GET', '/api/learner/me');
    assert.deepEqual(Object.keys(out.data).sort(), ['googleAvailable', 'signedIn']);
    const me = await call(env, 'GET', '/api/learner/me', { cookie: ada });
    assert.deepEqual(Object.keys(me.data).sort(), ['created', 'googleAvailable', 'lastSynced', 'methods', 'name', 'passkeys', 'signedIn']);
  });
  await check('PUT /api/learner/role is the same 404 as any unknown learner path', async () => {
    const a = await call(env, 'PUT', '/api/learner/role', { body: { role: 'student' }, cookie: ada });
    const b = await call(env, 'PUT', '/api/learner/nothing-here', { body: { role: 'student' }, cookie: ada });
    assert.equal(a.status, 404); assert.equal(a.text, b.text);
  });
  await check('a passkey sign-up that sends a role still works, and the role is dropped', async () => {
    const cookie = await passkeySignUp((m, p, o) => call(env, m, p, o), ORIGIN, 'localhost', { displayName: 'Bea', age13: true, role: 'parent' });
    const me = await call(env, 'GET', '/api/learner/me', { cookie });
    assert.equal(me.data.name, 'Bea'); assert.ok(!('role' in me.data));
    assert.ok(!db.seen.some((q) => /INSERT INTO learners[^;]*role/.test(q)), 'the role column is never named');
  });
  await check('the export has no role field', async () => {
    const x = await call(env, 'GET', '/api/learner/export', { cookie: ada });
    assert.equal(x.status, 200); assert.ok(!('role' in x.data.account));
  });
  await check('the film counter answers 204 and writes nothing at all', async () => {
    const before = db.sql.prepare('SELECT COUNT(*) AS n FROM rate_limits').get().n;
    const r = await call(env, 'POST', '/api/film-count', { body: { k: 'glycolysis/explainer', e: 's' } });
    assert.equal(r.status, 204); assert.equal(r.text, '');
    assert.equal(db.sql.prepare('SELECT COUNT(*) AS n FROM rate_limits').get().n, before);
    assert.equal(db.sql.prepare("SELECT COUNT(*) AS n FROM sqlite_master WHERE name='film_counts'").get().n, 0);
  });
  await check('the totals stay shut (the unknown-path 404) until the migration is applied, even with the right secret', async () => {
    const r = await admin(env);
    const unknown = await call(env, 'GET', '/api/nothing-here');
    assert.equal(r.status, 404); assert.equal(r.text, unknown.text);
    assert.ok(!db.seen.some((q) => /FROM learners WHERE created_at/.test(q)), 'and nothing was counted');
  });
}

// =================================================================================================
console.log('the gate');
const db = makeDb();
const env = { CLASSES: db, ASSETS, LEARNER_TEST: '1', ADMIN_TOKEN: SECRET };
{
  const unknown = await call(env, 'GET', '/api/nothing-here');
  const same = (r, why) => {
    assert.equal(r.status, 404, why); assert.equal(r.text, unknown.text, why);
    assert.deepEqual([...r.headers].sort(), [...unknown.headers].sort(), why);
  };
  await check('secret not set: the same 404 as any unknown API path, and nothing is written', async () => {
    const off = makeDb();
    const unusable = ['', 'short-secret', 'a passphrase with spaces that is long enough', 'sécret-with-a-non-ascii-letter-0123456789', 'x'.repeat(513)];
    for (const e of [{ CLASSES: off, ASSETS }, ...unusable.map((t) => ({ CLASSES: off, ASSETS, ADMIN_TOKEN: t }))]) {
      same(await admin(e), 'unset or too short');
      if (/^[\x21-\x7e]+$/.test(e.ADMIN_TOKEN || '')) same(await admin(e, { token: e.ADMIN_TOKEN }), 'even when the caller knows the unusable value');
    }
    assert.equal(off.sql.prepare('SELECT COUNT(*) AS n FROM rate_limits').get().n, 0, 'not even a rate-limit row');
  });
  await check('wrong, missing or misplaced secret: the same 404', async () => {
    const rowsBefore = db.sql.prepare('SELECT COUNT(*) AS n FROM rate_limits').get().n;
    same(await admin(env, { token: '' }), 'no header');
    same(await admin(env, { token: '', headers: { Authorization: SECRET } }), 'no Bearer');
    assert.equal(db.sql.prepare('SELECT COUNT(*) AS n FROM rate_limits').get().n, rowsBefore, 'a request with no Bearer header does no database work');
    same(await admin(env, { token: SECRET.slice(0, -1) + 'X' }), 'wrong secret');
    same(await admin(env, { token: SECRET + 'x' }), 'longer');
    same(await admin(env, { token: '', headers: { Authorization: SECRET } }), 'no Bearer');
    same(await admin(env, { token: '', headers: { Authorization: `Basic ${SECRET}` } }), 'Basic');
    same(await admin(env, { token: '', headers: { 'X-Admin-Token': SECRET, Cookie: `admin=${SECRET}` } }), 'other headers');
    same(await admin(env, { path: '/api/admin' }), 'parent path');
    same(await admin(env, { path: '/api/admin/stats/x' }), 'child path');
    const post = await call(env, 'POST', '/api/admin/stats', { body: {}, headers: { Authorization: `Bearer ${SECRET}` } });
    assert.equal(post.status, 404); assert.equal(post.text, unknown.text);
  });
  await check('a secret in the web address is refused, even with the right header, and a warning says to replace it', async () => {
    const warned = [];
    const realWarn = console.warn; console.warn = (...a) => warned.push(a.join(' '));
    try {
      same(await admin(env, { token: '', path: `/api/admin/stats?token=${SECRET}` }), 'query only');
      same(await admin(env, { path: `/api/admin/stats?token=${SECRET}` }), 'query and header');
      same(await admin(env, { path: '/api/admin/stats?x=1' }), 'any query string at all');
      same(await admin(env, { token: '', path: `/api/admin/stats?${SECRET}` }), 'the secret as a bare key');
      same(await admin(env, { token: '', path: `/api/admin/stats?auth=Bearer%20${SECRET}` }), 'the secret inside a value');
    } finally { console.warn = realWarn; }
    assert.equal(warned.length, 4); assert.ok(warned.every((w) => /ADMIN_TOKEN/.test(w) && !w.includes(SECRET)), 'the warning never repeats the value');
  });
  await check('the right secret in the Authorization header: 200, numbers, never cached, no CORS', async () => {
    const r = await admin(env);
    assert.equal(r.status, 200, r.text);
    assert.equal(r.headers.get('Cache-Control'), 'no-store');
    assert.equal(r.headers.get('Access-Control-Allow-Origin'), null);
    assert.equal(r.headers.get('Set-Cookie'), null);
    assert.equal(r.data.learners.total, 0); assert.equal(r.data.smallCell, 5);
    db.sql.exec('DELETE FROM admin_snapshots');
  });
  await check('twenty a minute per connection, then the same 404 even with the right secret', async () => {
    for (let i = 0; i < 20; i++) assert.equal((await admin(env, { ip: '198.51.100.77' })).status, 200);
    same(await admin(env, { ip: '198.51.100.77' }), 'over the limit');
    assert.equal((await admin(env, { ip: '198.51.100.78' })).status, 200, 'another connection is not affected');
  });
  await check('the page: noindex, in no sitemap or robots file, holds no secret and stores nothing', async () => {
    const page = src('src/pages/admin/index.astro');
    assert.match(page, /<BaseLayout[^>]*\bnoindex\b/);
    assert.ok(!/localStorage|sessionStorage|indexedDB|document\.cookie/.test(page.replace(/\/\*[\s\S]*?\*\//g, '')), 'no browser storage on the admin page');
    assert.match(page, /<BaseLayout[^>]*\bnoAnalytics\b/, 'no third-party script on the owner\'s page');
    assert.match(src('src/layouts/BaseLayout.astro'), /import\.meta\.env\.PROD && !noAnalytics/);
    assert.ok(!/stats\?/.test(page) && !/type="password"|Bearer/.test(page), 'the page asks with the session cookie only: no secret box, nothing in the address');
    assert.match(page, /credentials: 'same-origin'/);
    assert.match(page, /signedInHint\(\)/, 'a signed-out visitor makes no request');
    assert.ok(!/ADMIN_EMAILS|gmail/i.test(page.replace(/---[\s\S]*?---/, '')), 'the page does not say who the owner is');
    assert.ok(!/admin/i.test(src('src/pages/sitemap.xml.ts')) && !/admin/i.test(src('src/pages/robots.txt.ts')));
    assert.ok(!/ADMIN_TOKEN"\s*:/.test(src('wrangler.jsonc')), 'the secret is not a var in wrangler.jsonc');
  });
}

// =================================================================================================
console.log("the owner's own account (ADMIN_EMAILS)");
{
  const OWNER = 'deppmann@gmail.com';
  const odb = makeDb();
  const oenv = { CLASSES: odb, ASSETS, LEARNER_TEST: '1', ADMIN_EMAILS: OWNER, GOOGLE_CLIENT_ID: 'client-id.test', GOOGLE_CLIENT_SECRET: 'not-a-real-secret' };
  const unknown = await call(oenv, 'GET', '/api/nothing-here');
  const stats = (cookie, { env: e = oenv, headers = {}, path = '/api/admin/stats' } = {}) => call(e, 'GET', path, { cookie, headers: Object.fromEntries(Object.entries({ 'Sec-Fetch-Site': 'same-origin', 'CF-Connecting-IP': '198.51.100.40', ...headers }).filter(([, v]) => v !== undefined)) });
  const shut = (r, why) => { assert.equal(r.status, 404, why); assert.equal(r.text, unknown.text, why); assert.deepEqual([...r.headers].sort(), [...unknown.headers].sort(), why); };
  /** Sign in through the real Google flow (stubbed token endpoint). Returns the session cookie, or the error the callback redirected with. */
  const googleSignIn = async (claims, cookie = '', { link = false, env: e = oenv, headers = {} } = {}) => {
    const call_ = (m, p, o) => call(e, m, p, o);
    const start = await call_('GET', `/api/learner/google/start?return=%2Fadmin%2F&age=1${link ? '&link=1' : ''}`, { cookie, headers });
    if (!/accounts\.google\.com/.test(start.headers.get('Location') || '')) return { cookie: '', location: start.headers.get('Location') };
    const to = new URL(start.headers.get('Location'));
    nextClaims = { iss: 'https://accounts.google.com', aud: 'client-id.test', nonce: to.searchParams.get('nonce'), exp: Math.floor(Date.now() / 1000) + 600, iat: Math.floor(Date.now() / 1000), ...claims };
    const back = await call_('GET', `/api/learner/google/callback?state=${to.searchParams.get('state')}&code=abc`, { cookie: [cookie, start.cookie].filter(Boolean).join('; ') });
    return { cookie: back.cookie, location: back.headers.get('Location') };
  };
  /** A learner row written straight into the table, with a session: for accounts Google would never produce. */
  let made = 0;
  const rawLearner = async (fields) => {
    const id = 'RAW' + (++made), token = crypto.randomBytes(32).toString('hex'), now = Date.now();
    odb.sql.prepare('INSERT INTO learners (id, display_name, email, google_sub, created_at, last_active_at) VALUES (?,?,?,?,?,?)').run(id, fields.name ?? 'x', fields.email ?? null, fields.sub ?? null, now, now);
    // As if a Google sign-in had made the session (unless told otherwise), so only the address itself is under test.
    const via = fields.via === undefined ? { method: 'google', sub: fields.sub ?? null, email: fields.email ?? null } : fields.via;
    odb.sql.prepare('INSERT INTO learner_sessions (token_hash, learner_id, created_at, expires_at, method, google_sub, google_email) VALUES (?,?,?,?,?,?,?)').run(await sha256Hex(token), id, now, now + 86_400_000, via?.method ?? null, via?.sub ?? null, via?.email ?? null);
    return `bp_learner=${token}; bp_signed_in=1`;
  };

  const owner = await googleSignIn({ sub: 'G-OWNER', email: 'Deppmann@Gmail.com', email_verified: true, given_name: 'Chris' });
  await check('signed in with Google as the owner\'s address: the totals open, never cached', async () => {
    assert.equal(owner.location, '/admin/');
    const r = await stats(owner.cookie);
    assert.equal(r.status, 200, r.text);
    assert.equal(r.headers.get('Cache-Control'), 'no-store'); assert.equal(r.headers.get('Access-Control-Allow-Origin'), null);
    assert.equal(r.data.smallCell, 5);
    assert.equal((await stats(owner.cookie, { headers: { 'Sec-Fetch-Site': undefined } })).status, 200, 'a client that sends no fetch metadata but has the cookie');
  });
  await check('the same address on a claim Google did not verify gets no account at all', async () => {
    const before = odb.sql.prepare('SELECT COUNT(*) AS n FROM learners').get().n;
    for (const email_verified of [false, 'false', undefined, 0]) {
      const r = await googleSignIn({ sub: 'G-FAKE', email: OWNER, email_verified });
      assert.equal(r.location, '/account/?error=google-failed'); assert.equal(r.cookie, '');
    }
    assert.equal(odb.sql.prepare('SELECT COUNT(*) AS n FROM learners').get().n, before);
  });
  await check('another Google account, and lookalike addresses, stay out', async () => {
    const other = await googleSignIn({ sub: 'G-OTHER', email: 'someone.else@gmail.com', email_verified: true, given_name: 'Sam' });
    shut(await stats(other.cookie), 'another Google account');
    for (const email of ['d.eppmann@gmail.com', 'deppmann+admin@gmail.com', 'deppmann@googlemail.com', 'deppmann@gmail.com.evil.example', 'deppmann@gmail.co', 'xdeppmann@gmail.com', 'deppmann@gmail.comx', 'deppmann@gmail.com,other@x.org', ' deppmann@gmail.com.', 'deppmann@gmai1.com', 'deppmann']) {
      shut(await stats(await rawLearner({ email, sub: 'G-' + email })), email);
    }
  });
  await check('a passkey-only account named like the address, a typed email with no Google link, a teacher and a class seat stay out', async () => {
    const pk = await passkeySignUp((m, p, o) => call(oenv, m, p, o), ORIGIN, 'localhost', { displayName: OWNER, age13: true });
    assert.equal(odb.sql.prepare('SELECT display_name, email, google_sub FROM learners ORDER BY rowid DESC LIMIT 1').get().email, null);
    shut(await stats(pk), 'passkey-only, display name is the address');
    shut(await stats(await rawLearner({ email: OWNER, sub: null })), 'the address in the email column but no Google link (no route writes this; refused anyway)');
    shut(await stats(await rawLearner({ name: OWNER, email: null, sub: 'G-NAMEONLY' })), 'Google-linked, address only in the name');
    odb.sql.prepare("INSERT INTO teachers (email, name, password_hash, email_verified_at, created_at) VALUES (?, 'Chris', 'x', ?, ?)").run(OWNER, Date.now(), Date.now());
    const tt = 'e'.repeat(64);
    odb.sql.prepare('INSERT INTO teacher_sessions (teacher_id, token_hash, created_at, expires_at) VALUES (1, ?, ?, ?)').run(await sha256Hex(tt), Date.now(), Date.now() + 86_400_000);
    assert.equal((await call(oenv, 'GET', '/api/teacher/me', { cookie: `bp_teacher=${tt}` })).data.email, OWNER, 'a real teacher session with the very same address');
    shut(await stats(`bp_teacher=${tt}`), 'teacher account');
    shut(await stats(`bp_student=${'f'.repeat(64)}; bp_teacher=${tt}`), 'class seat');
    shut(await stats(''), 'nobody signed in');
  });
  await check('another site cannot ask through the owner\'s browser; any query string is refused', async () => {
    for (const site of ['cross-site', 'same-site', 'none']) shut(await stats(owner.cookie, { headers: { 'Sec-Fetch-Site': site } }), 'Sec-Fetch-Site: ' + site);
    shut(await stats(owner.cookie, { headers: { 'Sec-Fetch-Site': undefined, Origin: 'https://evil.example' } }), 'foreign Origin');
    shut(await stats(owner.cookie, { headers: { Origin: 'https://evil.example' } }), 'foreign Origin with forged metadata');
    shut(await stats(owner.cookie, { path: '/api/admin/stats?x=1' }), 'query string');
    assert.equal((await call(oenv, 'POST', '/api/admin/stats', { cookie: owner.cookie, body: {} })).status, 404);
  });
  await check('ADMIN_EMAILS: empty or junk means nobody; case and spaces do not matter; several addresses work', async () => {
    for (const v of [undefined, '', ' ', ',', '*', '@gmail.com', 'gmail.com', 'deppmann', '%', 'deppmann@gmail', 'true']) shut(await stats(owner.cookie, { env: { ...oenv, ADMIN_EMAILS: v } }), `ADMIN_EMAILS=${JSON.stringify(v)}`);
    for (const v of ['  DEPPMANN@GMAIL.COM  ', 'other@x.org, Deppmann@gmail.com ,third@y.org']) assert.equal((await stats(owner.cookie, { env: { ...oenv, ADMIN_EMAILS: v } })).status, 200, v);
    assert.deepEqual(ADMIN.adminEmails({ ADMIN_EMAILS: ' A@b.co ,, bad, c@d.org ' }), ['a@b.co', 'c@d.org']);
    assert.match(src('wrangler.jsonc'), /"ADMIN_EMAILS": "deppmann@gmail\.com"/);
  });
  await check('nobody else\'s visit costs anything: no cookie means no database work, and only the owner is counted', async () => {
    const mark = odb.seen.length;
    shut(await stats(''), 'no cookie'); shut(await stats('bp_learner=not-a-token'), 'malformed cookie');
    assert.equal(odb.seen.length, mark, 'no statement ran');
    const other = await rawLearner({ email: 'x@y.org', sub: 'G-X' });
    const m2 = odb.seen.length;
    shut(await stats(other), 'another learner');
    assert.ok(odb.seen.slice(m2).every((q) => /^\s*SELECT/.test(q)), 'a non-owner session is looked up and nothing is written');
  });
  await check('the secret still works as a second way in, and both together are fine', async () => {
    const e2 = { ...oenv, ADMIN_TOKEN: SECRET };
    assert.equal((await admin(e2, { ip: '198.51.100.41' })).status, 200);
    assert.equal((await stats(owner.cookie, { env: e2, headers: { Authorization: 'Bearer wrong-wrong-wrong-wrong-wrong' } })).status, 200, 'a wrong secret does not shut out the owner\'s own session');
    shut(await admin({ ...oenv, ADMIN_EMAILS: '' }, { ip: '198.51.100.42' }), 'no secret set and no owner address: nobody');
  });
  await check('it is the session that counts: on the owner\'s own account, a passkey session, an old session and a carried-over one stay out', async () => {
    const ownerId = odb.sql.prepare("SELECT id FROM learners WHERE google_sub='G-OWNER'").get().id;
    const sess = async (method, sub, email) => { const t = crypto.randomBytes(32).toString('hex'); odb.sql.prepare('INSERT INTO learner_sessions (token_hash, learner_id, created_at, expires_at, method, google_sub, google_email) VALUES (?,?,?,?,?,?,?)').run(await sha256Hex(t), ownerId, Date.now(), Date.now() + 86_400_000, method, sub, email); return `bp_learner=${t}`; };
    shut(await stats(await sess('passkey', null, null)), 'a passkey session on the owner\'s account');
    shut(await stats(await sess(null, null, null)), 'a session from before the migration, or carried from the old address');
    shut(await stats(await sess('google', 'G-SOMEONE-ELSE', OWNER)), 'a Google sign-in as a different Google account than the row holds');
    shut(await stats(await sess('google', 'G-OWNER', 'other@x.org')), 'a Google sign-in whose own verified address is not the owner\'s');
    shut(await stats(await sess('passkey', 'G-OWNER', OWNER)), 'method passkey, whatever else is recorded');
    assert.equal((await stats(await sess('google', 'G-OWNER', OWNER))).status, 200);
    assert.equal((await stats(owner.cookie)).status, 200);
  });
  await check('the review\'s attack: the owner presses "Sign in with Google" on a computer where a student is still signed in', async () => {
    const a = makeDb(); const aenv = { ...oenv, CLASSES: a };
    const sendA = (m, p, o) => call(aenv, m, p, o);
    const statsA = (cookie) => stats(cookie, { env: aenv });
    const shared = await passkeySignUp(sendA, ORIGIN, 'localhost', { displayName: 'Student', age13: true });
    const student = a.sql.prepare('SELECT id FROM learners').get().id;
    const phoneTok = crypto.randomBytes(32).toString('hex');
    a.sql.prepare("INSERT INTO learner_sessions (token_hash, learner_id, created_at, expires_at, method) VALUES (?,?,?,?,'passkey')").run(await sha256Hex(phoneTok), student, Date.now(), Date.now() + 86_400_000);
    const phone = `bp_learner=${phoneTok}`;
    shut(await statsA(phone), 'the student\'s phone, before'); shut(await statsA(shared), 'the shared computer, before');
    const chris = await googleSignIn({ sub: 'G-OWNER', email: OWNER, email_verified: true, given_name: 'Chris' }, shared, { env: aenv });
    const row = { ...a.sql.prepare('SELECT google_sub, email FROM learners WHERE id=?').get(student) };
    assert.deepEqual(row, { google_sub: null, email: null }, 'nothing was attached to the student\'s account');
    assert.equal(a.sql.prepare('SELECT COUNT(*) AS n FROM learners').get().n, 2, 'the owner got an account of his own');
    assert.equal((await statsA(chris.cookie)).status, 200, 'and his own session opens the page');
    shut(await statsA(phone), 'the student\'s phone, after');
    assert.equal((await call(aenv, 'GET', '/api/learner/me', { cookie: shared })).data.signedIn, false, 'the student\'s session on that computer was ended, not left behind the new one');
    assert.equal((await call(aenv, 'GET', '/api/learner/me', { cookie: phone })).data.name, 'Student', 'her phone is still signed in to her own account');
    // And if the damage had already been done (the identity sitting on her row), her sessions still stay out.
    a.sql.prepare("DELETE FROM learners WHERE google_sub='G-OWNER'").run();
    a.sql.prepare("UPDATE learners SET google_sub='G-OWNER', email=? WHERE id=?").run(OWNER, student);
    shut(await statsA(phone), 'a passkey session on a row that holds the owner\'s Google identity');
  });
  await check('"Link Google" is its own request: it attaches the identity only when asked from the signed-in account page, and signs the other devices out', async () => {
    const mk = async (name) => { odb.sql.exec('DELETE FROM rate_limits');   /* the sign-in limit is not what is under test here */ const c = await passkeySignUp((m, p, o) => call(oenv, m, p, o), ORIGIN, 'localhost', { displayName: name, age13: true }); return { c, id: odb.sql.prepare('SELECT id FROM learners ORDER BY rowid DESC LIMIT 1').get().id }; };
    const mallory = await mk('Mallory');
    // The owner's identity is already on his account: it cannot be linked to a second one.
    assert.equal((await googleSignIn({ sub: 'G-OWNER', email: OWNER, email_verified: true }, mallory.c, { link: true })).location, '/account/?error=google-in-use');
    shut(await stats(mallory.c), 'the second account');
    // A link asked for by another site's page is not a link: it is treated as a plain sign-in.
    const lee = await mk('Lee');
    const forged = await googleSignIn({ sub: 'G-LEE', email: 'lee@x.org', email_verified: true }, lee.c, { link: true, headers: { 'Sec-Fetch-Site': 'cross-site' } });
    assert.equal(odb.sql.prepare('SELECT google_sub FROM learners WHERE id=?').get(lee.id).google_sub, null);
    assert.ok(forged.cookie && forged.cookie !== lee.c);
    // A link with nobody signed in is refused before Google is involved.
    assert.equal((await googleSignIn({ sub: 'G-X' }, '', { link: true })).location, '/account/?error=google-state');
    // The real thing: signed in, pressed "Link Google". Linked, this device kept, the other device signed out.
    const kim = await mk('Kim');
    const otherTok = crypto.randomBytes(32).toString('hex');
    odb.sql.prepare("INSERT INTO learner_sessions (token_hash, learner_id, created_at, expires_at, method) VALUES (?,?,?,?,'passkey')").run(await sha256Hex(otherTok), kim.id, Date.now(), Date.now() + 86_400_000);
    const linked = await googleSignIn({ sub: 'G-KIM', email: 'kim@x.org', email_verified: true }, kim.c, { link: true });
    assert.equal(linked.location, '/admin/'); assert.equal(linked.cookie, '', 'no new session: the same one carries on');
    assert.deepEqual({ ...odb.sql.prepare('SELECT google_sub, email FROM learners WHERE id=?').get(kim.id) }, { google_sub: 'G-KIM', email: 'kim@x.org' });
    assert.equal((await call(oenv, 'GET', '/api/learner/me', { cookie: kim.c })).data.signedIn, true);
    assert.equal((await call(oenv, 'GET', '/api/learner/me', { cookie: `bp_learner=${otherTok}` })).data.signedIn, false, 'the other device must sign in again');
    // A second, different Google account cannot replace the linked one.
    assert.equal((await googleSignIn({ sub: 'G-KIM-2', email: 'kim2@x.org', email_verified: true }, kim.c, { link: true })).location, '/account/?error=google-in-use');
    // Linking the owner's address to a passkey account does not make that passkey session the owner.
    const pat = await mk('Pat');
    odb.sql.prepare("DELETE FROM learners WHERE google_sub='G-OWNER-2'").run();
    // The owner's Google identity is never added to an account made another way (it has a passkey, perhaps someone else's).
    const tried = await googleSignIn({ sub: 'G-OWNER-2', email: OWNER, email_verified: true }, pat.c, { link: true });
    assert.equal(tried.location, '/account/?error=google-link-owner');
    assert.deepEqual({ ...odb.sql.prepare('SELECT google_sub, email FROM learners WHERE id=?').get(pat.id) }, { google_sub: null, email: null });
    assert.equal((await call(oenv, 'GET', '/api/learner/me', { cookie: pat.c })).data.signedIn, true, 'and nobody was signed out by the refusal');
    shut(await stats(pat.c), 'the passkey account');
    assert.match(src('src/pages/account/index.astro'), /'google-link-owner': '[^']*Sign out, then choose Sign in with Google/);
    // The owner can still add a passkey to the owner's own (Google-made) account, and relinking the same identity is a no-op.
    assert.equal((await call(oenv, 'POST', '/api/learner/passkey/register/options', { cookie: owner.cookie, body: {} })).status, 200);
    odb.sql.exec('DELETE FROM rate_limits');
    assert.equal((await googleSignIn({ sub: 'G-OWNER', email: OWNER, email_verified: true }, owner.cookie, { link: true })).location, '/admin/');
    assert.equal((await stats(owner.cookie)).status, 200);
    for (const [m, p] of [['PUT', '/api/learner/email'], ['POST', '/api/learner/email'], ['PUT', '/api/learner/me'], ['POST', '/api/learner/google/unlink']]) assert.equal((await call(oenv, m, p, { cookie: mallory.c, body: { email: OWNER } })).status, 404, p);
    const src_ = src('worker/learner.js');
    const writes = [...src_.matchAll(/(INSERT INTO learners[^']*|UPDATE learners SET[^']*)/g)].map((x) => x[1]).filter((q) => /email/.test(q));
    assert.equal(writes.length, 4, 'the email column is written by four statements only (two forms of the insert, the link, the refresh at sign-in): ' + writes.join(' | '));
    const creators = [...src_.matchAll(/createLearner\(db, \{[^}]*\}/g)].map((x) => x[0]);
    assert.deepEqual(creators.filter((c) => /email/.test(c) && !/email = null/.test(c)), ['createLearner(db, { name, email, googleSub: sub_ }'], 'and only the Google callback ever passes an email when an account is made');
    assert.match(src_, /if \(claims\.email_verified !== true && claims\.email_verified !== 'true'\) throw/);
    assert.match(src('src/pages/account/index.astro'), /googleStartUrl\('\/account\/', false, true\)/, 'only the signed-in "Link Google" button asks for a link');
  });
  await check('a different account signed in on the same browser: the outgoing person\'s unsynced work is not merged into it', async () => {
    odb.sql.exec('DELETE FROM rate_limits');
    const sync = (cookie, body) => call(oenv, 'PUT', '/api/learner/sync', { cookie, body });
    const P = (lessons) => ({ v: 1, lessons, items: {} });
    const mkA = await passkeySignUp((m, p, o) => call(oenv, m, p, o), ORIGIN, 'localhost', { displayName: 'Ana', age13: true });
    const mkB = await passkeySignUp((m, p, o) => call(oenv, m, p, o), ORIGIN, 'localhost', { displayName: 'Ben', age13: true });
    // Ana was signed out when she did her first work: it merges into her new account, as it always has.
    const a1 = await sync(mkA, { notebook: { items: {} }, progress: P({ glycolysis: { v: 1, d: 2 } }) });
    assert.equal(a1.status, 200); assert.match(a1.data.acct, /^[0-9a-f]{16}$/); assert.ok(a1.data.progress.lessons.glycolysis);
    // Ben signs in on the same browser. The device still holds Ana's work, tagged with her account.
    const b1 = await sync(mkB, { notebook: { items: { n1: { id: 'n1', kind: 'note', slug: 'osmosis', text: 'ZZ Ana private note', updated: Date.now() } } }, progress: P({ glycolysis: { v: 1, d: 2 }, osmosis: { v: 5 } }), acct: a1.data.acct });
    assert.equal(b1.status, 409); assert.equal(b1.data.accountChanged, true); assert.notEqual(b1.data.acct, a1.data.acct);
    const benRow = odb.sql.prepare("SELECT d.notebook_json, d.progress_json FROM learner_data d JOIN learners l ON l.id=d.learner_id WHERE l.display_name='Ben'").get();
    assert.equal(benRow.notebook_json, '{}'); assert.equal(benRow.progress_json, '{}', 'nothing of Ana\'s reached Ben\'s account');
    // What the page does next: with the device cleared, it syncs under Ben's tag and gets Ben's own (empty) data.
    const b2 = await sync(mkB, { notebook: { items: {} }, progress: P({}), acct: b1.data.acct });
    assert.equal(b2.status, 200); assert.deepEqual(b2.data.progress.lessons, {}); assert.equal(b2.data.acct, b1.data.acct);
    // Ana's own account is untouched, and her own device keeps syncing.
    assert.equal((await sync(mkA, { notebook: { items: {} }, progress: P({}), acct: a1.data.acct })).data.progress.lessons.glycolysis.d, 2);
    assert.equal((await call(oenv, 'GET', '/api/learner/sync', { cookie: mkA })).data.acct, a1.data.acct);
    const lib = src('src/lib/learner.ts');
    assert.match(lib, /r\.status === 409 && r\.data\?\.accountChanged[\s\S]{0,600}clearDevice\(\)/, 'the page clears the outgoing account\'s copy before syncing again');
    assert.match(lib, /\.\.\.\(known \? \{ acct: known \} : \{\}\)/, 'a device with no tag (a signed-out reader\'s own work) sends none, and is merged');
  });
  await check('before migration 0011 sign-in works as it did and the owner\'s page stays shut for accounts; the export says how each device signed in after it', async () => {
    const early = makeDb({ before0011: true }); const eenv = { ...oenv, CLASSES: early };
    const o = await googleSignIn({ sub: 'G-OWNER', email: OWNER, email_verified: true, given_name: 'Chris' }, '', { env: eenv });
    assert.equal(o.location, '/admin/'); assert.equal((await call(eenv, 'GET', '/api/learner/me', { cookie: o.cookie })).data.name, 'Chris');
    shut(await stats(o.cookie, { env: eenv }), 'no record of how the session was made yet');
    assert.ok(!('signedInWith' in (await call(eenv, 'GET', '/api/learner/export', { cookie: o.cookie })).data.sessions[0]));
    assert.equal((await admin({ ...eenv, ADMIN_TOKEN: SECRET }, { ip: '198.51.100.43' })).status, 200, 'the secret still works');
    assert.equal((await call(oenv, 'GET', '/api/learner/export', { cookie: owner.cookie })).data.sessions[0].signedInWith, 'google');
    assert.equal((await stats(owner.cookie)).headers.get('X-Content-Type-Options'), 'nosniff');
  });
  await check('before migration 0009 the route stays shut for the owner too', async () => {
    const early = makeDb({ before0009: true });
    const now = Date.now(), token = 'a'.repeat(64);
    early.sql.prepare("INSERT INTO learners (id, display_name, email, google_sub, created_at, last_active_at) VALUES ('O','Chris',?, 'G-OWNER', ?, ?)").run(OWNER, now, now);
    early.sql.prepare("INSERT INTO learner_sessions (token_hash, learner_id, created_at, expires_at) VALUES (?, 'O', ?, ?)").run(await sha256Hex(token), now, now + 86_400_000);
    shut(await stats(`bp_learner=${token}`, { env: { ...oenv, CLASSES: early } }), 'no snapshot table yet');
  });
}

// =================================================================================================
console.log('the role question');
const jar = {};   // name -> { id, cookie }
{
  await check('/me offers the question only now that the column exists', async () => {
    assert.equal((await call(env, 'GET', '/api/learner/me')).data.roleSupported, true);
  });
  await check('passkey sign-up carries the role; skipping it stores nothing', async () => {
    jar.pat = { cookie: await passkeySignUp((m, p, o) => call(env, m, p, o), ORIGIN, 'localhost', { displayName: 'Pat', age13: true, role: 'parent' }) };
    jar.pat.id = newestLearner(db).id;
    assert.equal(newestLearner(db).role, 'parent');
    const me = await call(env, 'GET', '/api/learner/me', { cookie: jar.pat.cookie });
    assert.equal(me.data.role, 'parent'); assert.equal(me.data.roleSupported, true);
    await passkeySignUp((m, p, o) => call(env, m, p, o), ORIGIN, 'localhost', { displayName: 'Sky', age13: true });
    assert.equal(newestLearner(db).role, null);
    for (const bad of ['admin', 'Student', 'child', 7, { a: 1 }, 'student; DROP']) {
      await passkeySignUp((m, p, o) => call(env, m, p, o), ORIGIN, 'localhost', { displayName: 'Odd', age13: true, role: bad });
      assert.equal(newestLearner(db).role, null, `"${JSON.stringify(bad)}" is not a role`);
    }
  });
  await check('the age gate still comes first: no tick, no account, whatever role is sent', async () => {
    const before = db.sql.prepare('SELECT COUNT(*) AS n FROM learners').get().n;
    const o = await call(env, 'POST', '/api/learner/passkey/register/options', { body: { displayName: 'Kid', role: 'student' } });
    assert.equal(o.status, 400); assert.match(o.data.error, /13 and older/);
    assert.equal(db.sql.prepare('SELECT COUNT(*) AS n FROM learners').get().n, before);
  });
  await check('Google sign-up: the role is never in a web address; the page sets it once signed in', async () => {
    const genv = { ...env, GOOGLE_CLIENT_ID: 'client-id.test', GOOGLE_CLIENT_SECRET: 'not-a-real-secret' };
    const start = await call(genv, 'GET', '/api/learner/google/start?return=%2Faccount%2F&age=1');
    assert.equal(start.status, 302);
    const to = new URL(start.headers.get('Location'));
    assert.equal(to.origin, 'https://accounts.google.com');
    assert.ok(!/role|student|parent|teacher/i.test(to.href), 'nothing about a role goes to Google');
    nextClaims = { iss: 'https://accounts.google.com', aud: 'client-id.test', sub: 'ZZSUB-1001', email: 'zzmail-gia@marker.example', email_verified: true, given_name: 'Gia', nonce: to.searchParams.get('nonce'), exp: Math.floor(Date.now() / 1000) + 600, iat: Math.floor(Date.now() / 1000) };
    const back = await call(genv, 'GET', `/api/learner/google/callback?state=${to.searchParams.get('state')}&code=abc`, { cookie: start.cookie });
    assert.equal(back.status, 302); assert.equal(back.headers.get('Location'), '/account/');
    jar.gia = { cookie: back.cookie, id: newestLearner(db).id };
    let me = await call(genv, 'GET', '/api/learner/me', { cookie: jar.gia.cookie });
    assert.equal(me.data.name, 'Gia'); assert.equal(me.data.role, null);
    // What src/pages/account/index.astro does on return, with the role it held in sessionStorage:
    assert.equal((await call(genv, 'PUT', '/api/learner/role', { body: { role: 'teacher' }, cookie: jar.gia.cookie })).status, 200);
    me = await call(genv, 'GET', '/api/learner/me', { cookie: jar.gia.cookie });
    assert.equal(me.data.role, 'teacher');
    const page = src('src/pages/account/index.astro'), lib = src('src/lib/learner.ts');
    assert.match(page, /holdRole\(back === '\/account\/' \? pickedRole\(\) : null\)/, 'held only when Google returns to /account/'); assert.match(page, /takeHeldRole\(\)/);
    assert.ok(!/seedRole|writePrefs/.test(page + lib), "the account's role is never copied into the device preferences");
    assert.ok(!/role/.test(/export const googleStartUrl[\s\S]*?;\n/.exec(lib)[0]), 'googleStartUrl takes no role');
    assert.match(lib, /sessionStorage/);
  });
  await check('changed, cleared, refused when it is not a role, and only for the signed-in learner', async () => {
    const put = (body, cookie = jar.pat.cookie) => call(env, 'PUT', '/api/learner/role', { body, cookie });
    assert.equal((await put({ role: 'student' })).status, 200); assert.equal(roleOf(db, jar.pat.id), 'student');
    assert.equal((await put({ role: null })).status, 200); assert.equal(roleOf(db, jar.pat.id), null);
    assert.equal((await put({ role: 'teacher' })).status, 200);
    for (const bad of [{ role: 'admin' }, { role: '' }, { role: 5 }, {}, { role: ['teacher'] }, 'not json']) assert.equal((await put(bad)).status, 400, JSON.stringify(bad));
    assert.equal(roleOf(db, jar.pat.id), 'teacher', 'a refused change leaves it alone');
    assert.equal((await put({ role: 'student' }, '')).status, 401);
    assert.equal((await call(env, 'PUT', '/api/learner/role', { body: { role: 'student' }, cookie: jar.pat.cookie, origin: ORIGIN, headers: { Origin: 'https://evil.example' } })).status, 403);
    assert.equal(roleOf(db, jar.gia.id), 'teacher', "another learner's role was never touched");
  });
  await check('"Download my data" includes it', async () => {
    const x = await call(env, 'GET', '/api/learner/export', { cookie: jar.pat.cookie });
    assert.equal(x.data.account.role, 'teacher');
    await call(env, 'PUT', '/api/learner/role', { body: { role: null }, cookie: jar.pat.cookie });
    assert.equal((await call(env, 'GET', '/api/learner/export', { cookie: jar.pat.cookie })).data.account.role, null);
  });
  await check('deleting the account deletes the role with it', async () => {
    await call(env, 'PUT', '/api/learner/role', { body: { role: 'parent' }, cookie: jar.pat.cookie });
    assert.equal((await call(env, 'POST', '/api/learner/delete', { body: { confirm: 'DELETE' }, cookie: jar.pat.cookie })).status, 200);
    assert.equal(db.sql.prepare('SELECT COUNT(*) AS n FROM learners WHERE id=?').get(jar.pat.id).n, 0);
    for (const t of ['learner_sessions', 'learner_passkeys', 'learner_data', 'learner_challenges']) {
      assert.equal(db.sql.prepare(`SELECT COUNT(*) AS n FROM ${t} WHERE learner_id=?`).get(jar.pat.id).n, 0, t);
    }
    assert.equal(db.sql.prepare("SELECT COUNT(*) AS n FROM learners WHERE role='parent'").get().n, 0, 'no orphan role anywhere');
  });
  await check('a sign-up that was started and dropped does not keep its name and role past ten minutes', async () => {
    const o = await call(env, 'POST', '/api/learner/passkey/register/options', { body: { displayName: 'ZZDROPPED', age13: true, role: 'parent' } });
    assert.equal(o.status, 200);
    const held = () => db.sql.prepare("SELECT COUNT(*) AS n FROM learner_challenges WHERE display_name='ZZDROPPED'").get().n;
    assert.equal(held(), 1);
    db.sql.exec("UPDATE learner_challenges SET expires_at = 1 WHERE display_name='ZZDROPPED'");
    LEARNER._resetSweep();
    await call(env, 'GET', '/api/learner/me');   // a visit to the account page sweeps
    assert.equal(held(), 0);
    const mark = db.seen.length;
    await call(env, 'GET', '/api/learner/me');   // but at most once a minute: the next page view writes nothing
    assert.ok(!db.seen.slice(mark).some((q) => /^\s*(DELETE|INSERT|UPDATE)/.test(q)));
  });
  await check('nobody else is shown a role: teacher, class and group answers never carry one', async () => {
    for (const f of ['worker/api.js', 'worker/groups.js', 'worker/feedback.js', 'worker/planner.js', 'worker/helper.js']) {
      assert.ok(!/\blearners\b[^;]*\brole\b|\bl\.role\b/.test(src(f)), `${f} does not read learners.role`);
    }
  });
}

console.log('the old-domain sign-up page (browsers that cannot use the passkey on the new host)');
{
  const B = { primary: 'stemhop.com', legacy: 'biochemistrypedia.com', rpId: 'biochemistrypedia.com', known: ['biochemistrypedia.com', 'www.biochemistrypedia.com', 'stemhop.com', 'www.stemhop.com'] };
  const W = createWorker(B);
  const OLD = 'https://biochemistrypedia.com';
  const send = async (method, path, { body, cookie, origin }) => {
    const res = await W.fetch(new Request(origin + path, { method, headers: { 'Content-Type': 'application/json', Origin: origin, ...(cookie ? { Cookie: cookie } : {}) }, body: JSON.stringify(body) }), env);
    const text = await res.text();
    return { status: res.status, text, data: JSON.parse(text), cookie: (res.headers.getSetCookie?.() ?? []).map((c) => c.split(';')[0]).filter((c) => !c.endsWith('=')).join('; ') };
  };
  await check('a sign-up made on the old host stores the role it was sent', async () => {
    await passkeySignUp(send, OLD, 'biochemistrypedia.com', { displayName: 'Tam', age13: true, role: 'teacher' });
    assert.deepEqual({ ...newestLearner(db) }, { id: newestLearner(db).id, role: 'teacher', display_name: 'Tam' });
  });
  await check('its page asks the question, hidden until asked for and until the age box is ticked, and sends the answer in the request body', async () => {
    const res = await HO.signinPage(`${OLD}/handoff/signin/?to=%2Faccount%2F&name=Tam`, B);
    const html = await res.text();
    assert.match(html, /<fieldset id="rl" hidden>/);
    for (const v of ['student', 'parent', 'teacher']) assert.ok(html.includes(`name="role" value="${v}"`));
    assert.match(html, /name="role" value="" checked/, 'nothing is chosen for the reader');
    const script = /<script>([\s\S]*)<\/script>/.exec(html)[1];
    new Function(script);   // it parses
    assert.match(script, /age13:true,role:role\(\)/);
    assert.match(script, /\^#role=\(student\|parent\|teacher\|\)\$/, 'read from the fragment, which is never sent to a server');
    assert.match(script, /rl\.hidden=!age\.checked/);
    const csp = res.headers.get('Content-Security-Policy');
    assert.ok(csp.includes(`'sha256-${createHash('sha256').update(script).digest('base64')}'`), 'the strict CSP still matches the script');
  });
  await check('the account page forwards the choice in the fragment, never in the query string', async () => {
    const js = HO.accountScript(B);
    new Function(js);
    assert.match(js, /'#role='\+encodeURIComponent/);
    assert.ok(!/[?&]role=/.test(js), 'no ?role= or &role=');
    assert.match(js, /\[data-role-new\]\[data-role-on\]/);
    assert.match(src('src/pages/account/index.astro'), /data-role-new/);
  });
}

// =================================================================================================
console.log('the film counter');
{
  const post = (body, { ip = '203.0.113.5', headers = {}, cookie } = {}) => call(env, 'POST', '/api/film-count', { body, cookie, headers: { 'CF-Connecting-IP': ip, ...headers } });
  const today = FILM.siteDay();
  await check('the table has four columns and nothing else', async () => {
    assert.deepEqual(db.sql.prepare('PRAGMA table_info(film_counts)').all().map((c) => c.name), ['film_key', 'day', 'started', 'watched']);
  });
  await check('started, watched and both are counted per film per day', async () => {
    for (const e of ['s', 's', 'w', 'sw']) assert.equal((await post({ k: 'glycolysis/explainer', e })).status, 204);
    await post({ k: 'method-pcr/explainer', e: 's' });
    assert.deepEqual(filmRows(db), [
      { film_key: 'glycolysis/explainer', day: today, started: 3, watched: 2 },
      { film_key: 'method-pcr/explainer', day: today, started: 1, watched: 0 },
    ]);
  });
  await check('unknown films and junk are answered 204 and never stored', async () => {
    const before = JSON.stringify(filmRows(db));
    const junk = [
      { k: 'not-a-film/explainer', e: 's' }, { k: 'zzname maria lopez', e: 's' }, { k: 'glycolysis/explainer', e: 'x' }, { k: 'glycolysis/explainer' },
      { k: ['glycolysis/explainer'], e: 's' }, { k: 'g'.repeat(300), e: 's' }, { e: 's' }, {}, 'not json', { k: 'glycolysis/explainer', e: 's', pad: 'x'.repeat(500) },
      { k: "glycolysis/explainer'; DROP TABLE film_counts;--", e: 's' }, { k: 'home/sizzle', e: 'w' },
    ];
    for (const b of junk) { const r = await post(b); assert.equal(r.status, 204, JSON.stringify(b).slice(0, 60)); assert.equal(r.text, ''); }
    assert.equal(JSON.stringify(filmRows(db)), before);
  });
  await check('it reads no cookie, looks nobody up and stores nothing about the sender', async () => {
    const tables = db.sql.prepare("SELECT name FROM sqlite_master WHERE type='table' AND name NOT IN ('film_counts','rate_limits') AND name NOT LIKE 'sqlite_%'").all().map((t) => t.name);
    const snap = () => JSON.stringify(tables.map((t) => db.sql.prepare(`SELECT * FROM ${t}`).all()));
    const before = snap();
    const mark = db.seen.length;
    const r = await post({ k: 'osmosis/explainer', e: 'sw', name: 'ZZNAME', id: jar.gia.id }, { cookie: `${jar.gia.cookie}; bp_student=${'c'.repeat(64)}; bp_teacher=${'d'.repeat(64)}`, ip: '203.0.113.99' });
    assert.equal(r.status, 204); assert.equal(r.headers.get('Set-Cookie'), null);
    assert.equal(snap(), before, 'no other table changed (not even "last active")');
    const ran = db.seen.slice(mark);
    assert.ok(ran.every((q) => /\b(film_counts|rate_limits)\b/.test(q)), 'only the counter and the rate limit were touched: ' + ran.join(' | '));
    const row = db.sql.prepare("SELECT * FROM film_counts WHERE film_key='osmosis/explainer'").get();
    assert.deepEqual({ ...row }, { film_key: 'osmosis/explainer', day: today, started: 1, watched: 1 });
    // The rate limit holds a salted one-way hash and a count: not the address, and not the hash other tables use.
    const keys = db.sql.prepare("SELECT key FROM rate_limits WHERE key LIKE 'film:%'").all().map((x) => x.key);
    assert.ok(keys.length >= 3 && keys.every((k) => /^film:(m|d):[0-9a-f]{64}$|^film:g:min$/.test(k)));
    assert.ok(!keys.some((k) => k.includes('203.0.113')));
    const plain = await clientKey(new Request(ORIGIN, { headers: { 'CF-Connecting-IP': '203.0.113.99' } }));
    assert.ok(!keys.some((k) => k.endsWith(plain)), 'salted: cannot be matched to the sign-in counters');
    assert.ok(keys.includes('film:m:' + await sha256Hex(`film|${SECRET}|203.0.113.99`)), 'keyed with a Worker secret');
    assert.ok(!keys.includes('film:m:' + await sha256Hex('film||203.0.113.99')) && !keys.includes('film:m:' + await sha256Hex('film|203.0.113.99')), 'not findable by hashing every address');
    const r1 = new Request(ORIGIN, { headers: { 'CF-Connecting-IP': '203.0.113.99' } });
    assert.equal(await FILM.filmClientKey(r1, { RATE_SALT: 'a', ADMIN_TOKEN: 'b' }), await sha256Hex('film|a|203.0.113.99'));
    assert.equal(await FILM.filmClientKey(r1, {}), await sha256Hex('film||203.0.113.99'), 'with no secret it falls back to the fixed prefix');
    const text = JSON.stringify(db.sql.prepare('SELECT * FROM film_counts').all()) + JSON.stringify(db.sql.prepare("SELECT * FROM rate_limits WHERE key LIKE 'film:%'").all());
    assert.ok(!/ZZNAME|bp_/.test(text) && !text.includes('203.0.113') && !text.includes(jar.gia.id));
  });
  await check('only this site may post, only as JSON, and a GET is the ordinary 404', async () => {
    const before = JSON.stringify(filmRows(db));
    assert.equal((await post({ k: 'glycolysis/explainer', e: 's' }, { headers: { Origin: 'https://evil.example' } })).status, 403);
    assert.equal((await call(env, 'POST', '/api/film-count', { body: 'k=glycolysis/explainer&e=s', json: false, headers: { 'Content-Type': 'application/x-www-form-urlencoded' } })).status, 403);
    const g = await call(env, 'GET', '/api/film-count');
    assert.equal(g.status, 404); assert.equal(g.text, (await call(env, 'GET', '/api/nothing-here')).text);
    assert.equal(JSON.stringify(filmRows(db)), before);
  });
  await check('rate limit: 120 a minute per connection; the rest are dropped quietly', async () => {
    const start = db.sql.prepare("SELECT started FROM film_counts WHERE film_key='glycolysis/explainer'").get().started;
    for (let i = 0; i < 130; i++) assert.equal((await post({ k: 'glycolysis/explainer', e: 's' }, { ip: '203.0.113.200' })).status, 204);
    assert.equal(db.sql.prepare("SELECT started FROM film_counts WHERE film_key='glycolysis/explainer'").get().started, start + 120);
    await post({ k: 'glycolysis/explainer', e: 's' }, { ip: '203.0.113.201' });
    assert.equal(db.sql.prepare("SELECT started FROM film_counts WHERE film_key='glycolysis/explainer'").get().started, start + 121, 'another connection still counts');
  });
  await check('a long body with no stated length is cut off at the limit, not read whole', async () => {
    let pulled = 0;
    const stream = new ReadableStream({ pull(c) { pulled++; if (pulled > 50) c.close(); else c.enqueue(new TextEncoder().encode('{"k":"glycolysis/explainer","e":"s","pad":"' + 'x'.repeat(300))); } });
    const before = JSON.stringify(filmRows(db));
    const res = await handleApi(new Request(ORIGIN + '/api/film-count', { method: 'POST', headers: { 'Content-Type': 'application/json' }, body: stream, duplex: 'half' }), env);
    assert.equal(res.status, 204);
    assert.ok(pulled < 10, `stopped reading early (read ${pulled} chunks)`);
    assert.equal(JSON.stringify(filmRows(db)), before);
  });
  await check('once the site-wide allowance is used up, a flood from new addresses writes no new rows', async () => {
    db.sql.prepare("INSERT OR REPLACE INTO rate_limits (key, count, window_start) VALUES ('film:g:min', 1500, ?)").run(Date.now());
    const rows = db.sql.prepare('SELECT COUNT(*) AS n FROM rate_limits').get().n;
    const before = JSON.stringify(filmRows(db));
    for (let i = 0; i < 20; i++) await post({ k: 'glycolysis/explainer', e: 's' }, { ip: `2001:db8::${i}` });
    assert.equal(db.sql.prepare('SELECT COUNT(*) AS n FROM rate_limits').get().n, rows);
    assert.equal(JSON.stringify(filmRows(db)), before);
    db.sql.exec("DELETE FROM rate_limits WHERE key='film:g:min'");
  });
  await check('one connection over its own limit cannot use up the allowance everyone shares', async () => {
    db.sql.exec("DELETE FROM rate_limits WHERE key LIKE 'film:%'");
    for (let i = 0; i < 200; i++) await post({ k: 'glycolysis/explainer', e: 's' }, { ip: '203.0.113.210' });
    assert.equal(db.sql.prepare("SELECT count FROM rate_limits WHERE key='film:g:min'").get().count, 120);
  });
  await check('the page sends the film and the event, without cookies, and fails silently', async () => {
    const lib = src('src/lib/film-progress.ts');
    const send = /fetch\('\/api\/film-count',[\s\S]*?\}\)\.catch/.exec(lib)[0];
    assert.match(send, /credentials: 'omit'/);
    assert.match(send, /referrerPolicy: 'no-referrer'/);
    assert.match(send, /body: JSON\.stringify\(\{ k: key, e \}\)/);
    assert.ok(!/learner|student|nickname|classroom/.test(/\/\/ ---- the anonymous film count[\s\S]*?\n}\n/.exec(lib)[0]), 'the count code knows nothing about accounts or classes');
  });
}

// =================================================================================================
console.log('the totals: aggregates only, small cells hidden, one answer a day');
{
  const s = db.sql;
  const now = Date.now();
  const DAYMS = 86_400_000;
  const T = now - 2 * DAYMS;                      // everything is counted "as of the end of yesterday"
  const yesterday = new Date(FILM.siteDay(now) + 'T12:00:00Z').getTime() - DAYMS;
  const dayStr = (ms) => new Date(ms).toISOString().slice(0, 10);
  s.exec('DELETE FROM learner_passkeys; DELETE FROM learner_sessions; DELETE FROM learner_data; DELETE FROM learner_challenges; DELETE FROM learners; DELETE FROM rate_limits; DELETE FROM admin_snapshots;');
  // 22 learners: 12 students, 1 parent, 0 teachers, 9 who did not say. Every identifying field carries a marker.
  const roles = [...Array(12).fill('student'), 'parent', ...Array(9).fill(null)];
  roles.forEach((role, i) => {
    const id = `ZZID-learner-${i}`;
    s.prepare('INSERT INTO learners (id, display_name, email, google_sub, created_at, last_active_at, role) VALUES (?,?,?,?,?,?,?)')
      .run(id, `ZZNAME Maria ${i}`, i < 14 ? `zzmail${i}@marker.example` : null, i < 14 ? `ZZSUB-${i}` : null, T - (i % 3) * 7 * DAYMS, T - i * 2 * DAYMS, role);
    if (i >= 8) s.prepare('INSERT INTO learner_passkeys (credential_id, learner_id, public_key, counter, transports, created_at) VALUES (?,?,?,?,?,?)').run(`ZZCRED-${i}`, id, 'ZZKEY', 0, '[]', T);
    const lessons = {};
    if (i < 10) lessons.glycolysis = { v: 1, d: 2 };                      // 10 opened, 10 finished
    if (i < 11) lessons.mitosis = { v: 1, ...(i < 10 ? { d: 2 } : {}) };  // 11 opened, 10 finished: the one who did not is a cell of 1
    if (i < 3) lessons.osmosis = { v: 1 };                                // 3: hidden
    if (i < 20) lessons['mendel-peas'] = { v: 1, d: 2 };                  // 20 of 22: the 2 who did not are a small group, so it is not listed
    if (i < 15) lessons['zz-typed-by-a-learner'] = { v: 1, d: 2 };        // not a lesson the site has
    const notebook = i < 7 ? { [`ZZNOTEID-${i}`]: { id: `ZZNOTEID-${i}`, kind: 'note', slug: 'glycolysis', text: 'ZZNOTE my secret diary', updated: now } } : {};
    s.prepare('INSERT INTO learner_data (learner_id, notebook_json, progress_json, updated_at) VALUES (?,?,?,?)')
      .run(id, JSON.stringify(notebook), i === 21 ? 'not json at all' : JSON.stringify({ v: 1, lessons, items: {} }), T);
  });
  // An account made today: it must not show until tomorrow.
  s.prepare("INSERT INTO learners (id, display_name, created_at, last_active_at, role) VALUES ('ZZID-today','ZZNAME Today',?,?,'teacher')").run(now, now);
  // 12 teachers (10 confirmed). Teachers 1 to 6 have classes; teacher 7 has five periods of one course alone.
  for (let i = 0; i < 12; i++) s.prepare('INSERT INTO teachers (email, name, password_hash, email_verified_at, created_at, last_active_at) VALUES (?,?,?,?,?,?)').run(`zzteacher${i}@marker.example`, `ZZTEACHER Ms Rivera ${i}`, 'ZZHASH', i < 10 ? T : null, T - i * DAYMS, T);
  s.prepare("INSERT INTO groups (id, slug, name, about, created_by, created_at) VALUES ('ZZGROUPID','zzgroup-lincoln-high','ZZGROUP Lincoln High','ZZABOUT',1,?)").run(T);
  s.prepare("INSERT INTO group_members (group_id, teacher_id, role, status, joined_at) VALUES ('ZZGROUPID',1,'admin','active',?)").run(T);
  const courses = [...Array(12).fill('genetics'), ...Array(2).fill('cell-biology'), ...Array(6).fill('life-science'), 'zz-made-up-course', ...Array(5).fill('biochemistry')];
  courses.forEach((course, i) => {
    const id = `ZZCLASSID${i}`;
    const teacher = course === 'biochemistry' ? 7 : (i % 6) + 1;          // one person's five biochemistry periods
    s.prepare('INSERT INTO classes (id, teacher_id, name, course, code, join_mode, created_at, last_activity_at, group_id) VALUES (?,?,?,?,?,?,?,?,?)')
      .run(id, teacher, `ZZCLASS Period ${i}`, course, `ZZCODE${i}`, course === 'biochemistry' ? 'roster' : 'open', T - (i % 4) * 7 * DAYMS, T - i * 2 * DAYMS, i === 0 ? 'ZZGROUPID' : null);
    if (i < 12) s.prepare('INSERT INTO assignments (class_id, lesson_slug, assigned_at) VALUES (?,?,?)').run(id, 'glycolysis', T);   // 6 teachers
    if (course === 'biochemistry') s.prepare('INSERT INTO assignments (class_id, lesson_slug, assigned_at) VALUES (?,?,?)').run(id, 'osmosis', T);   // 5 classes, 1 teacher
    if (i < 6) s.prepare('INSERT INTO assignments (class_id, lesson_slug, assigned_at) VALUES (?,?,?)').run(id, 'zz-assigned-free-text', T);
    for (let k = 0; k < (i < 20 ? 3 : 0); k++) {
      const r = s.prepare('INSERT INTO students (class_id, nickname, code_hash, status, created_at, last_seen_at) VALUES (?,?,?,?,?,?)').run(id, `ZZNICK kid ${k}`, 'ZZCODEHASH', i === 0 && k < 2 ? 'pending' : 'active', T - 20 * DAYMS, T - k * 10 * DAYMS);
      if (i < 6) s.prepare("INSERT INTO answers (student_id, lesson_slug, kind, item, value, correct, created_at, updated_at) VALUES (?,?,'stuck','',?,NULL,?,?)").run(Number(r.lastInsertRowid), 'glycolysis', 'ZZANSWER I do not get it', T, T);
      if (i === 0) for (let q = 0; q < 4; q++) s.prepare("INSERT INTO answers (student_id, lesson_slug, kind, item, value, correct, created_at, updated_at) VALUES (?,?,'quiz',?,'1',1,?,?)").run(Number(r.lastInsertRowid), 'glycolysis', `q${q}`, T, T);   // 12 quiz rows, 3 children, 1 class
    }
  });
  s.prepare('INSERT INTO router_budget (period, spent_micro, calls, errors, blocked) VALUES (?, 123456, 9, 1, 2)').run('d' + dayStr(yesterday));
  s.prepare('INSERT INTO router_budget (period, spent_micro, calls) VALUES (?, 99, 77)').run('d' + FILM.siteDay(now));
  s.prepare("INSERT INTO router_budget (period, spent_micro, calls) VALUES ('m2026-11', 654321, 40)").run();
  s.prepare("INSERT INTO router_queries (created_at, query, picks) VALUES (?, 'ZZQUERY why is my kid sick', 'glycolysis')").run(now);
  s.exec('DELETE FROM film_counts');
  const film = s.prepare('INSERT INTO film_counts (film_key, day, started, watched) VALUES (?,?,?,?)');
  film.run('glycolysis/explainer', dayStr(yesterday), 20, 9); film.run('glycolysis/explainer', dayStr(yesterday - 40 * DAYMS), 5, 5);
  film.run('osmosis/explainer', dayStr(yesterday), 1, 1); film.run('zz-junk-key', dayStr(yesterday), 50, 50);
  film.run('glycolysis/explainer', FILM.siteDay(now), 1000, 1000);        // today: left out

  const mark = db.seen.length;
  const r = await admin(env, { ip: '198.51.100.9' });
  assert.equal(r.status, 200, r.text);
  const d = r.data;
  const ran = db.seen.slice(mark);

  await check('plain whole-site totals are shown as they are, as of the end of yesterday, and stay separate lines', async () => {
    assert.equal(d.learners.total, 22, "today's new account is not counted yet"); assert.equal(d.teachers.total, 12);
    assert.equal(d.classes.total, 26); assert.equal(d.seats.total, 60);   // shown because 7 different teachers have classes
    assert.equal(d.asOf, dayStr(yesterday));
    assert.ok(!JSON.stringify(Object.keys(d)).match(/people|users|everyone|allAccounts/i), 'no summed "users" figure');
    assert.deepEqual(d.groups, { total: null }, 'one school group is a small count');
  });
  await check('the count is made about once a day, not when the reader asks: the kept reply is served for 20 hours whatever happens', async () => {
    s.prepare("INSERT INTO learners (id, display_name, created_at, last_active_at, role) VALUES ('ZZID-late','ZZNAME Late',?,?,'parent')").run(T, T);
    s.prepare("UPDATE film_counts SET started = started + 1 WHERE film_key='osmosis/explainer'").run();
    const again = await admin(env, { ip: '198.51.100.10' });
    assert.equal(again.text, r.text);
    for (const h of [0.1, 5, 19.9]) assert.equal(await ADMIN.dailyReply(db, env, new Request(ORIGIN), now + h * 3_600_000), r.text, `${h} hours later`);
    assert.deepEqual(s.prepare('SELECT day FROM admin_snapshots ORDER BY day').all().map((x) => x.day), ['hold:v1', 'reply:v3'], 'two rows, replaced in place');
    const later = JSON.parse(await ADMIN.dailyReply(db, env, new Request(ORIGIN), now + 20.5 * 3_600_000));
    assert.ok(later.learners.total === 23 || later.learners.total === 24, 'after 20 hours a new count is made (24 if the site day has turned and today\'s account now counts)');
    assert.deepEqual(s.prepare('SELECT day FROM admin_snapshots ORDER BY day').all().map((x) => x.day), ['hold:v1', 'reply:v3']);
    assert.ok(!/base|held/.test(JSON.stringify(later)), 'the totals the holds are measured against are never sent');
    s.exec("DELETE FROM learners WHERE id='ZZID-late'; UPDATE film_counts SET started = started - 1 WHERE film_key='osmosis/explainer'; DELETE FROM admin_snapshots;");
  });
  await check('role split: with 1 parent to hide, every group with anyone in it is hidden; the empty one stays 0', async () => {
    assert.deepEqual(d.learners.role, { student: null, parent: null, teacher: 0, unset: null });
  });
  await check('sign-in method and notes follow the same rule; "active lately" and weekly counts are cells too', async () => {
    assert.deepEqual(d.learners.signIn, { google: 8, passkey: 8, both: 6, neither: 0 });
    assert.deepEqual(d.learners.withNotes, { yes: 7, no: 15 });
    assert.deepEqual(d.learners.active, { last7: null, days8to30: null, older: null }, '4 active in 7 days is a small group, so the three-way split is hidden');
    assert.ok(!('active7' in d.learners) && !('active30' in d.learners), 'no nested recency figures to subtract');
    assert.equal(d.learners.splitsAsOf, d.asOf);
    assert.equal(d.learners.newByWeek.length, 26);
    assert.ok(d.learners.newByWeek.every((w) => w.n === null || w.n === 0 || w.n >= 5));
    assert.ok(!('withProgress' in d.learners));
  });
  await check('teachers are one three-way split, with no exact count beside a hidden one', async () => {
    assert.deepEqual(d.teachers.classes, { active30: null, idle: null, none: null }, '6 active, 1 idle, 5 with none: the 1 must be hidden, so all three are');
    assert.deepEqual(d.teachers.verified, { yes: null, no: null });
    assert.ok(!('withActiveClass30' in d.teachers) && !('withClass' in d.teachers));
  });
  await check('lessons: no grand totals; a lesson is listed only if neither those who opened it nor those who did not are a small group', async () => {
    assert.deepEqual(d.lessons, { opened: [{ slug: 'mitosis', opened: 11, finished: null }, { slug: 'glycolysis', opened: 10, finished: 10 }], hidden: null });
  });
  await check('class cells count teachers, not classes: one teacher with five periods is never shown as 5', async () => {
    assert.deepEqual(d.classes.byLevel, { 'college-core': null, 'grade-7': null, other: null, 'college-further': null });
    assert.deepEqual(d.classes.byCourse, { genetics: null, 'cell-biology': null, 'life-science': null, other: null, biochemistry: null });
    assert.deepEqual(d.classes.joinMode, { open: null, approve: 0, roster: null, locked: 0 }, 'roster = 5 classes, but one teacher');
    assert.deepEqual(d.classes.inGroup, { yes: null, no: null });
    assert.deepEqual(d.classWork.assigned, [{ slug: 'glycolysis', classes: 12, teachers: 6 }], 'osmosis is on 5 class lists, all one teacher');
    assert.equal(d.classWork.hidden, null, 'a count of 1 lesson not listed is itself a small count');
    assert.ok(!('assignments' in d.classWork));
  });
  await check('answers count students and classes, not rows: 12 quiz answers from one class are hidden', async () => {
    assert.deepEqual(d.classWork.answers30, { quiz: null, idea: 0, cer: 0, done: 0, stuck: null });
    assert.deepEqual(d.seats.status, { active: null, pending: null });
    assert.deepEqual(d.seats.seen, { last7: 20, days8to30: 40, older: 0 });
    assert.deepEqual(d.classes.active, { last7: null, days8to30: null, older: null }, 'the 4 classes used in 7 days belong to 4 teachers');
  });
  await check('films: whole days only (today left out), for films the site has, with nothing about who', async () => {
    assert.equal(d.on.films, true);
    assert.deepEqual(d.films.byFilm, [
      { film: 'glycolysis/explainer', started: 25, watched: 14, started30: 20, watched30: 9 },
      { film: 'osmosis/explainer', started: 1, watched: 1, started30: 1, watched30: 1 },
    ]);
    assert.equal(d.films.byDay.length, 30); assert.equal(d.films.byDay.at(-1).day, dayStr(yesterday)); assert.equal(d.films.byDay.at(-1).started, 71);
    assert.deepEqual(d.films.last7, { started: 71, watched: 60 }); assert.deepEqual(d.films.all, { started: 76, watched: 65 });
    assert.match(src('src/pages/admin/index.astro'), /A rough guide, not an exact count/);
    assert.ok(!/numbers are exact/.test(src('src/pages/admin/index.astro')));
  });
  await check('lesson suggester: calls per whole day and nothing about cost or questions', async () => {
    assert.deepEqual(d.router.byDay.at(-1), { day: dayStr(yesterday), calls: 9, errors: 1, blocked: 2 });
    assert.ok(!/micro|spent|usd|cost|token|77/i.test(JSON.stringify(d.router)));
  });

  // ---- the scan: nothing that looks like a person, a class or an id, anywhere in the reply ------
  const ALLOWED_KEYS = new Set([
    'generated', 'asOf', 'smallCell', 'splitsAsOf', 'last7', 'days8to30', 'older', 'seen', 'on', 'role', 'films', 'catalog', 'learners', 'lessons', 'teachers', 'classes', 'seats', 'classWork', 'groups', 'router', 'planner',
    'total', 'active7', 'active30', 'newByWeek', 'week', 'n', 'signIn', 'google', 'passkey', 'both', 'neither', 'withNotes', 'yes', 'no',
    'student', 'parent', 'teacher', 'unset', 'opened', 'finished', 'slug', 'hidden', 'verified', 'idle', 'none',
    'byLevel', 'byCourse', 'joinMode', 'open', 'approve', 'roster', 'locked', 'size', 's1to9', 's10to29', 's30up', 'withAssignments', 'inGroup', 'aiFeedbackOn',
    'seen7', 'seen30', 'status', 'active', 'pending', 'assigned', 'answers30', 'quiz', 'idea', 'cer', 'done', 'stuck',
    'since', 'last7', 'last30', 'all', 'started', 'watched', 'started30', 'watched30', 'byDay', 'day', 'byFilm', 'film', 'calls', 'errors', 'blocked',
    'savedPlans', 'classLists', 'other',
  ]);
  const siteKeys = new Set([...CATALOG.levels.map((l) => l[0]), ...Object.keys(CATALOG.courses), ...Object.keys(CATALOG.lessons), ...Object.keys(CATALOG.films)]);
  const strings = [], keys = [], numbers = [];
  (function walk(x) {
    if (typeof x === 'string') strings.push(x);
    else if (typeof x === 'number') numbers.push(x);
    else if (Array.isArray(x)) x.forEach(walk);
    else if (x && typeof x === 'object') for (const [k, v] of Object.entries(x)) { keys.push(k); walk(v); }
  })(d);
  await check('every string in the reply is a date or one of the site\'s own keys; every field name is on a fixed list', async () => {
    for (const k of keys) assert.ok(ALLOWED_KEYS.has(k) || siteKeys.has(k), `unexpected field "${k}"`);
    for (const v of strings) assert.ok(/^\d{4}-\d{2}-\d{2}(T[\d:.]+Z)?$/.test(v) || siteKeys.has(v), `unexpected text "${v}"`);
    for (const v of numbers) assert.ok(Number.isInteger(v) && v >= 0, `not a count: ${v}`);
    assert.ok(strings.length > 80 && numbers.length > 150, 'the scan saw the whole reply');
  });
  await check('no name, email, nickname, class, group, answer, note, code, id, question or cost from the database is in it', async () => {
    assert.ok(!/zz/i.test(r.text), 'a marker leaked: ' + (/.{0,40}zz.{0,40}/i.exec(r.text) || [''])[0]);
    assert.ok(!r.text.includes('@') && !/marker|example|Rivera|Maria|Lincoln|Period|diary|sick/i.test(r.text));
    assert.ok(!/[0-9a-f]{32,}/i.test(r.text), 'nothing that looks like a token or a hash');
    assert.ok(!/123456|654321/.test(r.text), 'no spend figure');
    for (const row of s.prepare('SELECT id FROM learners').all()) assert.ok(!r.text.includes(row.id));
  });
  await check('every statement it ran was a count or a sum, or read a table that holds no person; typed lesson keys never leave the database', async () => {
    const own = ran.filter((q) => !/\brate_limits\b|\badmin_snapshots\b/.test(q));
    assert.ok(own.length > 30);
    for (const q of own) {
      assert.match(q, /^\s*SELECT\b/i, q);
      const anonymous = /\bFROM (router_budget|film_counts)\b/.test(q) || /LIMIT 0\s*$/.test(q);
      assert.ok(anonymous || /\b(COUNT|SUM)\(/.test(q), 'not an aggregate: ' + q);
      assert.ok(!/\b(display_name|nickname|email|name|code|code_hash|about|note|query|draft|final|answer|password_hash|token_hash|credential_id|public_key|notebook_json AS|progress_json AS)\b(?!_)/.test(q.replace(/email_verified_at/g, '')), 'names a private column: ' + q);
      // What the statement hands back (its own select list, with the counts taken out) names no id.
      const handsBack = q.slice(0, q.search(/\bFROM\b/)).replace(/COUNT\((DISTINCT )?[^)]*\)/g, 'COUNT').replace(/[\w.]+ IS (NOT )?NULL/g, 'TEST');
      assert.ok(!/\b(id|learner_id|student_id|teacher_id|class_id|group_id)\b/.test(handsBack), 'selects an id: ' + q);
      if (/json_each\(CASE/.test(q) || /lesson_slug AS slug/.test(q)) assert.match(q, /JOIN json_each\(\?1\)/, 'joined to the site\'s lesson list inside SQL: ' + q);
    }
  });

  await check('the split rules themselves, with the cases the review found', async () => {
    assert.deepEqual(ADMIN.split({ a: 10, b: 7, c: 0 }), { a: 10, b: 7, c: 0 });
    assert.deepEqual(ADMIN.split({ a: 10, b: 7, c: 2 }), { a: null, b: null, c: null });
    assert.deepEqual(ADMIN.split({ a: 10, b: 7, c: 2, d: 0 }), { a: null, b: null, c: null, d: 0 });
    assert.deepEqual(ADMIN.split({ a: 3, b: 0, c: 0 }), { a: null, b: null, c: null }, 'one cell holds everyone: the zeros would give it away');
    assert.deepEqual(ADMIN.split({ a: 1, b: 1, c: 0 }), { a: null, b: null, c: null }, 'every filled cell holds one: the zeros would give them away');
    assert.deepEqual(ADMIN.split({ a: 0, b: 0 }), { a: 0, b: 0 });
    assert.deepEqual(ADMIN.split({ student: 10, parent: 1, teacher: 1, unset: 0 }), { student: null, parent: null, teacher: null, unset: 0 }, 'review: two hidden cells adding up to 2 were recoverable');
    assert.deepEqual(ADMIN.split({ student: 10, parent: 1, teacher: 0, unset: 0 }), { student: null, parent: null, teacher: 0, unset: 0 }, 'review: the complement must not be a zero cell');
    assert.deepEqual(ADMIN.split({ a: 10, b: 1, c: 1, d: 1 }), { a: null, b: null, c: null, d: null });
    assert.deepEqual(ADMIN.split({ a: 5, b: 4, c: 4 }), { a: null, b: null, c: null }, 'the case a rule-aware reader could solve under "hide the next smallest"');
    assert.deepEqual(ADMIN.split({ a: 9, b: 3 }), { a: null, b: null });
    assert.deepEqual(ADMIN.split({ a: 9, b: 6, c: 8 }, ['b']), { a: null, b: null, c: null }, 'a forced cell (too few people behind it) is protected like a small one');
    assert.equal(ADMIN.part(6, 7), null); assert.equal(ADMIN.part(7, 7), 7); assert.equal(ADMIN.part(6, 12), 6); assert.equal(ADMIN.part(11, 12), null); assert.equal(ADMIN.part(0, 12), 0);
    const nest = ADMIN.nestedSplit({ x1: 6, x2: 2, y1: 9, z1: 3, z2: 4 }, (k) => k[0]);
    assert.deepEqual(nest.byParent, { x: 8, y: 9, z: 7 });
    assert.deepEqual(nest.byChild, { x1: null, x2: null, y1: 9, z1: null, z2: null });
    const hid = ADMIN.nestedSplit({ x1: 2, y1: 6, y2: 5, z1: 30 }, (k) => k[0]);
    assert.deepEqual(hid.byParent, { x: null, y: null, z: null });
    assert.deepEqual(hid.byChild, { x1: null, y1: null, y2: null, z1: null }, 'a hidden level hides its courses');
  });
  await check('property: for every split of up to 4 cells with values 0 to 9, no hidden cell can be worked out from the shown cells and the total, even by a reader who knows the rule', async () => {
    for (const width of [2, 3, 4]) {
      const groups = new Map();
      const cellsOf = (i) => Array.from({ length: width }, (_, k) => Math.floor(i / 10 ** k) % 10);
      for (let i = 0; i < 10 ** width; i++) {
        const v = cellsOf(i);
        const out = ADMIN.split(Object.fromEntries(v.map((x, k) => ['c' + k, x])));
        const key = v.reduce((a, b) => a + b, 0) + '|' + JSON.stringify(out);     // what a reader sees: the shown cells and the total
        if (!groups.has(key)) groups.set(key, []);
        groups.get(key).push(v);
      }
      for (const [key, inputs] of groups) {
        const out = Object.values(JSON.parse(key.slice(key.indexOf('|') + 1)));
        out.forEach((shown, k) => {
          if (shown !== null) { assert.ok(shown === 0 || shown >= 5, key); return; }
          const possible = new Set(inputs.map((v) => v[k]));
          assert.ok(possible.size >= 2, `cell ${k} of ${key} can only be ${[...possible]}`);
        });
      }
    }
  });
  await check('property: across every way 9 or 13 accounts can answer the role question, the whole reply never pins down a hidden role count', async () => {
    const quiet = { fetch: ASSETS.fetch };
    for (const N of [9, 13]) {
      const groups = new Map();
      for (let a = 0; a <= N; a++) for (let b = 0; a + b <= N; b++) for (let c = 0; a + b + c <= N; c++) {
        const t = makeDb();
        const mix = [...Array(a).fill('student'), ...Array(b).fill('parent'), ...Array(c).fill('teacher'), ...Array(N - a - b - c).fill(null)];
        const ins = t.sql.prepare('INSERT INTO learners (id, display_name, created_at, last_active_at, role) VALUES (?,?,?,?,?)');
        mix.forEach((role, i) => ins.run('L' + i, 'x', T, T, role));
        const reply = (await ADMIN.buildStats(t, { ASSETS: quiet }, new Request(ORIGIN), now)).stats;
        delete reply.generated;
        const key = JSON.stringify(reply);
        if (!groups.has(key)) groups.set(key, []);
        groups.get(key).push([a, b, c, N - a - b - c]);
      }
      for (const [key, mixes] of groups) {
        const role = Object.values(JSON.parse(key).learners.role);
        role.forEach((shown, k) => { if (shown === null) assert.ok(new Set(mixes.map((m) => m[k])).size >= 2, `N=${N}: role cell ${k} can only be ${mixes[0][k]} given ${JSON.stringify(JSON.parse(key).learners.role)}`); });
      }
    }
  });

  // ---- two days running, and the one-teacher site ---------------------------------------------
  const world = async (setup) => { const t = makeDb(); await setup(t.sql); return t; };
  const E = { ASSETS: { fetch: ASSETS.fetch } };
  const addLearners = (sql, mix, at = T, tag = 'L') => { const ins = sql.prepare('INSERT INTO learners (id, display_name, created_at, last_active_at, role) VALUES (?,?,?,?,?)'); mix.forEach((role, i) => { ins.run(tag + i, 'x', at, at, role); sql.prepare("INSERT INTO learner_data (learner_id, notebook_json, progress_json, updated_at) VALUES (?, '{}', ?, 0)").run(tag + i, JSON.stringify({ v: 1, lessons: i < 20 ? { glycolysis: { v: 1, ...(i < 10 ? { d: 1 } : {}) } } : {}, items: {} })); }); };
  const BIG = [...Array(10).fill('student'), ...Array(5).fill('parent'), ...Array(5).fill('teacher'), ...Array(10).fill(null)];   // every cell is 5 or more: the split is shown
  const day2 = now + 26 * 3_600_000;
  const strip = (text) => { const o = JSON.parse(text); delete o.generated; return JSON.stringify(o); };
  await check('property, two days running: whatever one newcomer answers, the next day\'s reply is the same', async () => {
    const replies = new Set(); let first = null;
    for (const answer of ['student', 'parent', 'teacher', null]) {
      const t = await world((sql) => addLearners(sql, BIG));
      const one = JSON.parse(await ADMIN.dailyReply(t, E, new Request(ORIGIN), now));
      assert.deepEqual(one.learners.role, { student: 10, parent: 5, teacher: 5, unset: 10 });
      t.sql.prepare('INSERT INTO learners (id, display_name, created_at, last_active_at, role) VALUES (?,?,?,?,?)').run('NEW', 'x', now, now, answer);
      const two = await ADMIN.dailyReply(t, E, new Request(ORIGIN), day2);
      assert.equal(JSON.parse(two).learners.total, 31); assert.deepEqual(JSON.parse(two).learners.role, one.learners.role, 'the split is carried forward');
      assert.equal(JSON.parse(two).learners.splitsAsOf, one.asOf);
      replies.add(strip(two)); first = one;
    }
    assert.equal(replies.size, 1, 'the newcomer\'s answer changes nothing a reader can see');
    assert.ok(first);
  });
  await check('property, two days running: a deleted account\'s role, and a lesson one learner finished, do not show the next day', async () => {
    const replies = new Set();
    for (const change of ['none', 'delete-student', 'delete-parent', 'delete-unset', 'finish-lesson', 'open-lesson']) {
      const t = await world((sql) => addLearners(sql, BIG));
      await ADMIN.dailyReply(t, E, new Request(ORIGIN), now);
      const id = { 'delete-student': 'L0', 'delete-parent': 'L10', 'delete-unset': 'L25' }[change];
      if (id) t.sql.exec(`DELETE FROM learner_data WHERE learner_id='${id}'; DELETE FROM learners WHERE id='${id}'`);
      if (change === 'finish-lesson') t.sql.prepare("UPDATE learner_data SET progress_json=? WHERE learner_id='L15'").run(JSON.stringify({ v: 1, lessons: { glycolysis: { v: 1, d: 2 } }, items: {} }));
      if (change === 'open-lesson') t.sql.prepare("UPDATE learner_data SET progress_json=? WHERE learner_id='L25'").run(JSON.stringify({ v: 1, lessons: { glycolysis: { v: 1 } }, items: {} }));
      const two = JSON.parse(await ADMIN.dailyReply(t, E, new Request(ORIGIN), day2));
      const total = two.learners.total; delete two.learners.total; delete two.generated; delete two.learners.newByWeek; delete two.learners.active;
      assert.deepEqual(two.learners.withNotes, { yes: 0, no: 30 }, 'the notes pair is held with the rest');
      assert.equal(total, id ? 29 : 30);
      replies.add(JSON.stringify(two));
    }
    assert.equal(replies.size, 1, 'apart from the plain total, nothing a reader sees depends on which account went or what one learner did');
  });
  await check('the held split is republished once five more accounts exist, and then the change is five people\'s, not one\'s', async () => {
    const t = await world((sql) => addLearners(sql, BIG));
    const one = JSON.parse(await ADMIN.dailyReply(t, E, new Request(ORIGIN), now));
    addLearners(t.sql, ['teacher', 'teacher', 'student', null], now, 'M');
    const two = JSON.parse(await ADMIN.dailyReply(t, E, new Request(ORIGIN), day2));
    assert.deepEqual(two.learners.role, one.learners.role, '4 more: still held');
    addLearners(t.sql, ['parent'], day2, 'N');
    const three = JSON.parse(await ADMIN.dailyReply(t, E, new Request(ORIGIN), day2 + 26 * 3_600_000));
    assert.deepEqual(three.learners.role, { student: 11, parent: 6, teacher: 7, unset: 11 });
    assert.equal(three.learners.splitsAsOf, three.asOf);
  });
  await check('a query that fails on the day a block is republished does not force it out again the next day', async () => {
    for (const failing of [/json_each\(CASE/, /COALESCE\(role/]) {
      const replies = new Set();
      for (const answer of ['student', 'parent', null]) {
        const t = await world((sql) => addLearners(sql, BIG));
        const real = t.prepare; let fail = true;
        t.prepare = (q) => { if (fail && failing.test(q)) throw new Error('a passing database error'); return real(q); };
        const one = JSON.parse(await ADMIN.dailyReply(t, E, new Request(ORIGIN), now));
        fail = false;
        t.sql.prepare('INSERT INTO learners (id, display_name, created_at, last_active_at, role) VALUES (?,?,?,?,?)').run('NEW', 'x', now, now, answer);
        t.sql.prepare("UPDATE learner_data SET progress_json=? WHERE learner_id='L15'").run(JSON.stringify({ v: 1, lessons: { glycolysis: { v: 1, d: 2 } }, items: {} }));
        const two = JSON.parse(await ADMIN.dailyReply(t, E, new Request(ORIGIN), day2));
        assert.deepEqual(two.learners.role, one.learners.role, 'the role split did not move');
        assert.deepEqual(two.lessons, one.lessons, 'nor did the lesson list');
        replies.add(strip(JSON.stringify(two)));
      }
      assert.equal(replies.size, 1);
    }
  });
  await check('saved plans and class lists need five different people behind them', async () => {
    const t = await world((sql) => {
      addLearners(sql, BIG); sql.prepare("INSERT INTO teachers (email, name, password_hash, created_at) VALUES ('t@x.test','x','x',?)").run(T);
      sql.prepare("INSERT INTO classes (id, teacher_id, name, course, code, created_at, last_activity_at) VALUES ('C1',1,'x','genetics','K1',?,?)").run(T, T);
      for (let i = 0; i < 5; i++) {
        sql.prepare("INSERT INTO learner_plans (id, learner_id, title, goal_json, plan_json, start_at, created_at, updated_at) VALUES (?, 'L0', 'x', '{}', '{}', ?, ?, ?)").run('P' + i, T, T, T);
        sql.prepare("INSERT INTO class_resource_lists (id, class_id, teacher_id, title, items_json, created_at, updated_at) VALUES (?, 'C1', 1, 'x', '[]', ?, ?)").run('R' + i, T, T);
      }
    });
    const o = JSON.parse(await ADMIN.dailyReply(t, E, new Request(ORIGIN), now));
    assert.deepEqual(o.planner, { savedPlans: null, classLists: null }, 'five plans from one learner, five lists from one teacher');
  });
  const oneTeacher = (sql, course = 'genetics', extra = 0) => {
    for (let i = 0; i < 8; i++) sql.prepare('INSERT INTO teachers (email, name, password_hash, created_at) VALUES (?,?,?,?)').run(`t${i}@x.test`, 'x', 'x', T);
    for (let i = 0; i < 5 + extra; i++) {
      sql.prepare('INSERT INTO classes (id, teacher_id, name, course, code, join_mode, created_at, last_activity_at) VALUES (?,?,?,?,?,?,?,?)').run('C' + i, 1, 'x', i < 5 ? 'genetics' : course, 'K' + i, 'roster', T, T);
      for (let k = 0; k < 6; k++) sql.prepare('INSERT INTO students (class_id, nickname, code_hash, status, created_at, last_seen_at) VALUES (?,?,?,?,?,?)').run('C' + i, 'n' + k, 'h', k ? 'active' : 'pending', T, T);
    }
  };
  await check('one teacher with five periods: nothing about classes or seats is shown at all, not even the totals', async () => {
    const t = await world((sql) => oneTeacher(sql));
    const o = JSON.parse(await ADMIN.dailyReply(t, E, new Request(ORIGIN), now));
    assert.equal(o.teachers.total, 8);
    assert.equal(o.classes.total, null); assert.equal(o.seats.total, null);
    const nums = [];
    (function walk(x) { if (typeof x === 'number') nums.push(x); else if (x && typeof x === 'object') Object.values(x).forEach(walk); })({ c: o.classes, s: o.seats, w: o.classWork, t: o.teachers.classes });
    assert.ok(nums.every((v) => v === 0), 'every class and seat figure is hidden or zero: ' + nums.filter(Boolean));
    assert.ok(o.classes.newByWeek.every((w) => !w.n) && o.seats.newByWeek.every((w) => !w.n));
    assert.deepEqual(o.seats.status, { active: null, pending: null }); assert.deepEqual(o.seats.seen, { last7: null, days8to30: null, older: null });
  });
  await check('property, two days running: which course a teacher\'s new class is for does not show the next day', async () => {
    const replies = new Set();
    for (const course of ['genetics', 'life-science', 'biochemistry']) {
      const t = await world((sql) => { oneTeacher(sql); for (let i = 2; i <= 7; i++) for (let k = 0; k < 2; k++) sql.prepare('INSERT INTO classes (id, teacher_id, name, course, code, join_mode, created_at, last_activity_at) VALUES (?,?,?,?,?,?,?,?)').run(`D${i}${k}`, i, 'x', 'genetics', `Q${i}${k}`, 'open', T, T); });
      const one = JSON.parse(await ADMIN.dailyReply(t, E, new Request(ORIGIN), now));
      assert.equal(one.classes.total, 17); assert.deepEqual(one.classes.byCourse, { genetics: 17 });
      t.sql.prepare('INSERT INTO classes (id, teacher_id, name, course, code, join_mode, created_at, last_activity_at) VALUES (?,?,?,?,?,?,?,?)').run('NEWC', 2, 'x', course, 'NEWK', 'open', now, now);
      replies.add(strip(await ADMIN.dailyReply(t, E, new Request(ORIGIN), day2)));
    }
    assert.equal(replies.size, 1);
  });
}

console.log('the shared preferences helper (src/lib/prefs.ts)');
{
  const store = new Map();
  let blocked = false;
  const ls = {
    getItem: (k) => { if (blocked) throw new Error('blocked'); return store.has(k) ? store.get(k) : null; },
    setItem: (k, v) => { if (blocked) throw new Error('blocked'); store.set(k, String(v)); },
    removeItem: (k) => { if (blocked) throw new Error('blocked'); store.delete(k); },
  };
  const target = new EventTarget();
  globalThis.window = { localStorage: ls, addEventListener: (...a) => target.addEventListener(...a), removeEventListener: (...a) => target.removeEventListener(...a), dispatchEvent: (e) => target.dispatchEvent(e) };
  const P = await import('../src/lib/prefs.ts');
  await check('reads, writes, clears a field, keeps fields it does not know, and tells listeners', async () => {
    assert.equal(P.PREFS_KEY, 'stemhop:prefs:v1');
    assert.deepEqual(P.readPrefs(), {});
    const heard = [];
    const stop = P.onPrefsChange((p) => heard.push(p));
    assert.deepEqual(P.writePrefs({ role: 'parent', level: 'grade-7' }), { role: 'parent', level: 'grade-7' });
    store.set(P.PREFS_KEY, JSON.stringify({ ...JSON.parse(store.get(P.PREFS_KEY)), later: { x: 1 } }));
    assert.deepEqual(P.writePrefs({ level: null, time: 'short' }), { role: 'parent', time: 'short' });
    assert.deepEqual(JSON.parse(store.get(P.PREFS_KEY)), { role: 'parent', later: { x: 1 }, time: 'short' });
    assert.deepEqual(heard, [{}, { role: 'parent', level: 'grade-7' }, { role: 'parent', time: 'short' }]);
    stop(); P.clearPrefs();
    assert.equal(store.has(P.PREFS_KEY), false); assert.equal(heard.length, 3);
  });
  await check('damaged or hostile values are ignored, and blocked storage never throws', async () => {
    for (const bad of ['not json', '[]', '"x"', '{"role":"admin","level":"<script>","time":5}', 'null']) { store.set(P.PREFS_KEY, bad); assert.deepEqual(P.readPrefs(), {}, bad); }
    blocked = true;
    assert.deepEqual(P.readPrefs(), {});
    assert.deepEqual(P.writePrefs({ role: 'teacher' }), {});
    P.clearPrefs(); P.onPrefsChange(() => {})();
    blocked = false;
  });
}

console.log(`\n${n} checks passed.`);
