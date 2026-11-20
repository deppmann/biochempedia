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

let n = 0;
const check = async (name, fn) => { await fn(); n++; console.log('  ok  ' + name); };
const src = (p) => readFileSync(new URL('../' + p, import.meta.url), 'utf8');

// ---- an in-memory D1 with the real migrations; `before` stops short of 0009 -------------------
function makeDb({ before0009 = false } = {}) {
  const sql = new DatabaseSync(':memory:');
  const dir = new URL('../migrations/', import.meta.url);
  for (const f of readdirSync(dir).sort()) {
    if (before0009 && f >= '0009') continue;
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
  await check('the totals still answer, with role and films marked as not there yet', async () => {
    const r = await admin(env);
    assert.equal(r.status, 200, r.text);
    assert.deepEqual(r.data.on, { role: false, films: false, catalog: true });
    assert.equal(r.data.learners.total, 2); assert.equal(r.data.learners.role, null); assert.equal(r.data.films, null);
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
    for (const e of [{ CLASSES: off, ASSETS }, { CLASSES: off, ASSETS, ADMIN_TOKEN: '' }, { CLASSES: off, ASSETS, ADMIN_TOKEN: 'short-secret' }]) {
      same(await admin(e), 'unset or too short');
      same(await admin(e, { token: e.ADMIN_TOKEN || 'x' }), 'even when the caller knows a too-short value');
    }
    assert.equal(off.sql.prepare('SELECT COUNT(*) AS n FROM rate_limits').get().n, 0, 'not even a rate-limit row');
  });
  await check('wrong, missing or misplaced secret: the same 404', async () => {
    same(await admin(env, { token: '' }), 'no header');
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
    } finally { console.warn = realWarn; }
    assert.equal(warned.length, 2); assert.ok(warned.every((w) => /ADMIN_TOKEN/.test(w) && !w.includes(SECRET)), 'the warning never repeats the value');
  });
  await check('the right secret in the Authorization header: 200, numbers, never cached, no CORS', async () => {
    const r = await admin(env);
    assert.equal(r.status, 200, r.text);
    assert.equal(r.headers.get('Cache-Control'), 'no-store');
    assert.equal(r.headers.get('Access-Control-Allow-Origin'), null);
    assert.equal(r.headers.get('Set-Cookie'), null);
    assert.equal(r.data.learners.total, 0); assert.equal(r.data.smallCell, 5);
  });
  await check('twenty a minute per connection, then the same 404 even with the right secret', async () => {
    for (let i = 0; i < 20; i++) assert.equal((await admin(env, { ip: '198.51.100.77' })).status, 200);
    same(await admin(env, { ip: '198.51.100.77' }), 'over the limit');
    assert.equal((await admin(env, { ip: '198.51.100.78' })).status, 200, 'another connection is not affected');
  });
  await check('the page: noindex, in no sitemap or robots file, and the secret never goes to localStorage or a URL', async () => {
    const page = src('src/pages/admin/index.astro');
    assert.match(page, /<BaseLayout[^>]*\bnoindex\b/);
    assert.ok(!/localStorage/.test(page), 'no localStorage on the admin page');
    assert.ok(!/stats\?/.test(page) && /Authorization/.test(page), 'the secret is sent in a header');
    assert.ok(!/admin/i.test(src('src/pages/sitemap.xml.ts')) && !/admin/i.test(src('src/pages/robots.txt.ts')));
    assert.ok(!/ADMIN_TOKEN"\s*:/.test(src('wrangler.jsonc')), 'the secret is not a var in wrangler.jsonc');
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
    assert.match(page, /holdRole\(pickedRole\(\)\)/); assert.match(page, /takeHeldRole\(\)/);
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
  const today = new Date().toISOString().slice(0, 10);
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
    assert.ok(keys.includes('film:m:' + await sha256Hex('film|203.0.113.99')));
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
  await check('the page sends the film and the event, without cookies, and fails silently', async () => {
    const lib = src('src/lib/film-progress.ts');
    const send = /fetch\('\/api\/film-count',[\s\S]*?\}\)\.catch/.exec(lib)[0];
    assert.match(send, /credentials: 'omit'/);
    assert.match(send, /body: JSON\.stringify\(\{ k: key, e \}\)/);
    assert.ok(!/learner|student|nickname|classroom/.test(/\/\/ ---- the anonymous film count[\s\S]*?\n}\n/.exec(lib)[0]), 'the count code knows nothing about accounts or classes');
  });
}

// =================================================================================================
console.log('the totals: aggregates only, small cells hidden');
{
  const s = db.sql;
  const now = Date.now();
  const DAYMS = 86_400_000;
  s.exec('DELETE FROM learner_passkeys; DELETE FROM learner_sessions; DELETE FROM learner_data; DELETE FROM learner_challenges; DELETE FROM learners; DELETE FROM rate_limits;');
  // 12 learners: 6 students, 1 parent, 0 teachers, 5 who did not say. Every identifying field carries a marker.
  const roles = ['student', 'student', 'student', 'student', 'student', 'student', 'parent', null, null, null, null, null];
  roles.forEach((role, i) => {
    const id = `ZZID-learner-${i}`;
    s.prepare('INSERT INTO learners (id, display_name, email, google_sub, created_at, last_active_at, role) VALUES (?,?,?,?,?,?,?)')
      .run(id, `ZZNAME Maria ${i}`, i < 8 ? `zzmail${i}@marker.example` : null, i < 8 ? `ZZSUB-${i}` : null, now - (i % 4) * 7 * DAYMS, now - i * 3 * DAYMS, role);
    if (i >= 6) s.prepare('INSERT INTO learner_passkeys (credential_id, learner_id, public_key, counter, transports, created_at) VALUES (?,?,?,?,?,?)').run(`ZZCRED-${i}`, id, 'ZZKEY', 0, '[]', now);
    const lessons = {};
    if (i < 6) lessons.glycolysis = { v: 1, d: 2 };          // 6 opened, 6 finished
    if (i < 7) lessons.mitosis = { v: 1, ...(i < 6 ? { d: 2 } : {}) };   // 7 opened, 6 finished: the one who did not is a cell of 1
    if (i < 3) lessons.osmosis = { v: 1 };                   // 3: hidden
    if (i < 9) lessons['zz-typed-by-a-learner'] = { v: 1, d: 2 };   // 9, but not a lesson the site has
    const notebook = i < 5 ? { [`ZZNOTEID-${i}`]: { id: `ZZNOTEID-${i}`, kind: 'note', slug: 'glycolysis', text: 'ZZNOTE my secret diary', updated: now } } : {};
    s.prepare('INSERT INTO learner_data (learner_id, notebook_json, progress_json, updated_at) VALUES (?,?,?,?)')
      .run(id, JSON.stringify(notebook), i === 11 ? 'not json at all' : JSON.stringify({ v: 1, lessons, items: {} }), now);
  });
  // 7 teachers (6 confirmed), 16 classes, 42 seats.
  for (let i = 0; i < 7; i++) s.prepare('INSERT INTO teachers (email, name, password_hash, email_verified_at, created_at, last_active_at) VALUES (?,?,?,?,?,?)').run(`zzteacher${i}@marker.example`, `ZZTEACHER Ms Rivera ${i}`, 'ZZHASH', i < 6 ? now : null, now - i * DAYMS, now);
  s.prepare("INSERT INTO groups (id, slug, name, about, created_by, created_at) VALUES ('ZZGROUPID','zzgroup-lincoln-high','ZZGROUP Lincoln High','ZZABOUT',1,?)").run(now);
  s.prepare("INSERT INTO group_members (group_id, teacher_id, role, status, joined_at) VALUES ('ZZGROUPID',1,'admin','active',?)").run(now);
  const courses = [...Array(6).fill('genetics'), ...Array(2).fill('cell-biology'), ...Array(2).fill('biochemistry'), ...Array(5).fill('life-science'), 'zz-made-up-course'];
  courses.forEach((course, i) => {
    const id = `ZZCLASSID${i}`;
    s.prepare('INSERT INTO classes (id, teacher_id, name, course, code, join_mode, created_at, last_activity_at, group_id) VALUES (?,?,?,?,?,?,?,?,?)')
      .run(id, (i % 6) + 1, `ZZCLASS Period ${i}`, course, `ZZCODE${i}`, i < 9 ? 'open' : 'roster', now - i * DAYMS, now - i * 4 * DAYMS, i === 0 ? 'ZZGROUPID' : null);
    if (i < 5) s.prepare('INSERT INTO assignments (class_id, lesson_slug, assigned_at) VALUES (?,?,?)').run(id, 'glycolysis', now);
    if (i < 2) s.prepare('INSERT INTO assignments (class_id, lesson_slug, assigned_at) VALUES (?,?,?)').run(id, 'osmosis', now);
    if (i < 6) s.prepare('INSERT INTO assignments (class_id, lesson_slug, assigned_at) VALUES (?,?,?)').run(id, 'zz-assigned-free-text', now);
    for (let k = 0; k < (i < 14 ? 3 : 0); k++) {
      const r = s.prepare('INSERT INTO students (class_id, nickname, code_hash, status, created_at, last_seen_at) VALUES (?,?,?,?,?,?)').run(id, `ZZNICK kid ${k}`, 'ZZCODEHASH', i === 0 && k < 2 ? 'pending' : 'active', now, now - k * 10 * DAYMS);
      if (i < 4) s.prepare("INSERT INTO answers (student_id, lesson_slug, kind, item, value, correct, created_at, updated_at) VALUES (?,?,'stuck','',?,NULL,?,?)").run(Number(r.lastInsertRowid), 'glycolysis', 'ZZANSWER I do not get it', now, now);
    }
  });
  s.prepare("INSERT INTO router_budget (period, spent_micro, calls, errors, blocked) VALUES (?, 123456, 9, 1, 2)").run('d' + new Date(now).toLocaleDateString('en-CA', { timeZone: 'America/New_York' }));
  s.prepare("INSERT INTO router_budget (period, spent_micro, calls) VALUES ('m2026-11', 654321, 40)").run();
  s.prepare("INSERT INTO router_queries (created_at, query, picks) VALUES (?, 'ZZQUERY why is my kid sick', 'glycolysis')").run(now);
  s.prepare("INSERT INTO film_counts (film_key, day, started, watched) VALUES ('zz-junk-key', ?, 50, 50)").run(new Date(now).toISOString().slice(0, 10));

  const mark = db.seen.length;
  const r = await admin(env, { ip: '198.51.100.9' });
  assert.equal(r.status, 200, r.text);
  const d = r.data;
  const ran = db.seen.slice(mark);

  await check('whole-site totals are shown as they are, and the three kinds of account stay separate lines', async () => {
    assert.equal(d.learners.total, 12); assert.equal(d.teachers.total, 7); assert.equal(d.classes.total, 16); assert.equal(d.seats.total, 42);
    assert.equal(d.learners.active7, 3); assert.equal(d.learners.active30, 10);
    assert.equal(d.learners.newByWeek.length, 26);
    assert.equal(d.learners.newByWeek.reduce((a, w) => a + w.n, 0), 12);
    assert.ok(!JSON.stringify(Object.keys(d)).match(/people|users|everyone|allAccounts/i), 'no summed "users" figure');
    assert.deepEqual(d.groups, { total: 1, members: 1 });
  });
  await check('role split: a cell of 1 is hidden, and the next smallest with it so it cannot be found by subtraction', async () => {
    assert.deepEqual(d.learners.role, { student: 6, parent: null, teacher: null, unset: 5 });
  });
  await check('sign-in method, notes and progress follow the same rule', async () => {
    assert.deepEqual(d.learners.signIn, { google: 6, passkey: null, both: null, neither: 0 });   // 6 / 4 / 2 / 0
    assert.deepEqual(d.learners.withNotes, { yes: 5, no: 7 });
    assert.deepEqual(d.learners.withProgress, { yes: null, no: null });                           // 9 / 3: with one side of a pair hidden, the other would give it away
  });
  await check('a two-way split with one small side hides both sides', async () => {
    assert.deepEqual(ADMIN.split({ yes: 9, no: 3 }), { yes: null, no: null });
    assert.deepEqual(d.teachers.verified, { yes: null, no: null });                               // 6 confirmed, 1 not
  });
  await check('per-lesson lists need five learners, never name a lesson the site does not have, and say only how many were left out', async () => {
    assert.deepEqual(d.lessons.opened, [{ slug: 'mitosis', opened: 7, finished: null }, { slug: 'glycolysis', opened: 6, finished: 6 }]);
    assert.equal(d.lessons.hidden, 1);
    assert.equal(d.lessons.opens, 16); assert.equal(d.lessons.finishes, 12);
    assert.deepEqual(d.classWork.assigned, [{ slug: 'glycolysis', classes: 5 }]);
    assert.equal(d.classWork.hidden, 1);
  });
  await check('classes by level and by course: small cells hidden, and a hidden course takes its neighbour with it', async () => {
    assert.deepEqual(d.classes.byLevel, { 'college-core': 8, 'college-further': null, 'grade-7': 5, other: null });
    assert.deepEqual(d.classes.byCourse, { genetics: null, 'cell-biology': null, biochemistry: null, 'life-science': 5, other: null });
    assert.deepEqual(d.classes.joinMode, { open: 9, approve: 0, roster: 7, locked: 0 });
    assert.deepEqual(d.classes.inGroup, { yes: null, no: null });
    assert.deepEqual(d.seats.status, { active: null, pending: null });
    assert.deepEqual(d.classWork.answers30, { quiz: 0, idea: 0, cer: 0, done: 0, stuck: 12 });
  });
  await check('films: counted as they are, for films the site has, with nothing about who', async () => {
    assert.equal(d.on.films, true);
    assert.deepEqual(d.films.byFilm.map((f) => f.film), ['glycolysis/explainer', 'osmosis/explainer', 'method-pcr/explainer']);
    assert.deepEqual(d.films.byFilm[0], { film: 'glycolysis/explainer', started: 124, watched: 2, started30: 124, watched30: 2 });
    assert.equal(d.films.byDay.length, 30); assert.equal(d.films.byDay.at(-1).started, 176);   // every row for the day, a whole-site total (a film later removed from the site still counted)
    assert.deepEqual(Object.keys(d.films.byFilm[0]).sort(), ['film', 'started', 'started30', 'watched', 'watched30']);
  });
  await check('curiosity router: calls per day and nothing about cost or questions', async () => {
    assert.deepEqual(d.router.byDay.at(-1), { day: d.router.byDay.at(-1).day, calls: 9, errors: 1, blocked: 2 });
    assert.equal(d.router.callsAll, 40);
    assert.ok(!/micro|spent|usd|cost|token/i.test(JSON.stringify(d.router)));
  });

  // ---- the scan: nothing that looks like a person, a class or an id, anywhere in the reply ------
  const ALLOWED_KEYS = new Set([
    'generated', 'smallCell', 'on', 'role', 'films', 'catalog', 'learners', 'lessons', 'teachers', 'classes', 'seats', 'classWork', 'groups', 'router', 'planner', 'helpers',
    'total', 'active7', 'active30', 'newByWeek', 'week', 'n', 'signIn', 'google', 'passkey', 'both', 'neither', 'withNotes', 'withProgress', 'yes', 'no',
    'student', 'parent', 'teacher', 'unset', 'opens', 'finishes', 'opened', 'finished', 'slug', 'hidden', 'verified', 'withClass', 'withActiveClass30',
    'byLevel', 'byCourse', 'joinMode', 'open', 'approve', 'roster', 'locked', 'size', 'none', 's1to9', 's10to29', 's30up', 'withAssignments', 'inGroup', 'aiFeedbackOn',
    'seen7', 'seen30', 'status', 'active', 'pending', 'assignments', 'assigned', 'answers30', 'quiz', 'idea', 'cer', 'done', 'stuck', 'members',
    'since', 'last7', 'last30', 'all', 'started', 'watched', 'started30', 'watched30', 'byDay', 'day', 'byFilm', 'film', 'callsAll', 'calls', 'errors', 'blocked',
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
  await check('every statement it ran was a count or a sum, or read a table that holds no person', async () => {
    const own = ran.filter((q) => !/\brate_limits\b/.test(q));
    assert.ok(own.length > 30);
    for (const q of own) {
      assert.match(q, /^\s*SELECT\b/i, q);
      const anonymous = /\bFROM (router_budget|planner_budget|helper_budget|film_counts)\b/.test(q) || /LIMIT 0\s*$/.test(q);
      assert.ok(anonymous || /\b(COUNT|SUM)\(/.test(q), 'not an aggregate: ' + q);
      assert.ok(!/\b(display_name|nickname|email|name|code|code_hash|about|note|query|draft|final|answer|password_hash|token_hash|credential_id|public_key|notebook_json AS|progress_json AS)\b(?!_)/.test(q.replace(/email_verified_at/g, '')), 'names a private column: ' + q);
      assert.ok(!/SELECT[^(]*\b(id|learner_id|student_id|teacher_id|class_id|group_id)\b\s*(,|FROM)/.test(q), 'selects an id: ' + q);
    }
  });
  await check('the split rules themselves', async () => {
    assert.equal(ADMIN.cell(0), 0); assert.equal(ADMIN.cell(4), null); assert.equal(ADMIN.cell(1), null); assert.equal(ADMIN.cell(5), 5);
    assert.deepEqual(ADMIN.split({ a: 10, b: 7, c: 0 }), { a: 10, b: 7, c: 0 });
    assert.deepEqual(ADMIN.split({ a: 10, b: 7, c: 2 }), { a: 10, b: null, c: null });
    assert.deepEqual(ADMIN.split({ a: 10, b: 3, c: 2 }), { a: 10, b: null, c: null });
    assert.deepEqual(ADMIN.split({ a: 3, b: 0, c: 0 }), { a: null, b: null, c: null }, 'a split that adds up to under 5 is hidden whole');
    assert.deepEqual(ADMIN.split({ a: 0, b: 0 }), { a: 0, b: 0 });
    assert.deepEqual(ADMIN.split({ a: 4 }), { a: null });
    const nest = ADMIN.nestedSplit({ x1: 6, x2: 2, y1: 9, z1: 3, z2: 4 }, (k) => k[0]);
    assert.deepEqual(nest.byParent, { x: 8, y: 9, z: 7 });
    assert.deepEqual(nest.byChild, { x1: null, x2: null, y1: 9, z1: null, z2: null });
    const hid = ADMIN.nestedSplit({ x1: 2, y1: 6, y2: 5, z1: 30 }, (k) => k[0]);
    assert.deepEqual(hid.byParent, { x: null, y: null, z: 30 });
    assert.deepEqual(hid.byChild, { x1: null, y1: null, y2: null, z1: 30 }, 'a hidden level hides its courses');
  });
}

// =================================================================================================
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
