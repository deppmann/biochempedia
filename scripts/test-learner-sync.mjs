// End-to-end checks of learner sync through the worker (worker/learner.js), in Node with no network:
//   node scripts/test-learner-sync.mjs
// D1 is an in-memory SQLite shim loaded with the real migrations; sign-in uses the worker's own
// test-only route (LEARNER_TEST=1 on localhost). Two "devices" are two session cookies.
import { register } from 'node:module';
import { DatabaseSync } from 'node:sqlite';
import { readFileSync, readdirSync } from 'node:fs';
import assert from 'node:assert/strict';

// worker/ai.js imports a .json file without an import attribute, which wrangler's bundler allows and Node does not.
register('data:text/javascript,' + encodeURIComponent(`export async function load(u,c,n){return u.endsWith('.json')?n(u,{...c,importAttributes:{type:'json'}}):n(u,c)}`));
const { handleApi } = await import('../worker/api.js');
const { allowN } = await import('../worker/util.js');
const { mergeProgress } = await import('../src/lib/learner-merge.mjs');

function makeDb() {
  const sql = new DatabaseSync(':memory:');
  const dir = new URL('../migrations/', import.meta.url);
  for (const f of readdirSync(dir).sort()) sql.exec(readFileSync(new URL(f, dir), 'utf8'));
  const stmt = (q, args = []) => ({
    bind: (...a) => stmt(q, a),
    run: async () => ({ meta: { changes: Number(sql.prepare(q).run(...args).changes) } }),
    first: async () => sql.prepare(q).get(...args) ?? null,
    all: async () => ({ results: sql.prepare(q).all(...args) }),
    _run: () => sql.prepare(q).run(...args),
  });
  return { prepare: (q) => stmt(q), batch: async (ss) => ss.map((s) => ({ meta: { changes: Number(s._run().changes) } })), sql };
}

const ORIGIN = 'http://localhost:8787';
const db = makeDb();
const env = { CLASSES: db, LEARNER_TEST: '1' };
async function call(method, path, body, cookie) {
  const res = await handleApi(new Request(ORIGIN + path, {
    method, headers: { 'Content-Type': 'application/json', Origin: ORIGIN, ...(cookie ? { Cookie: cookie } : {}) },
    ...(body !== undefined ? { body: JSON.stringify(body) } : {}),
  }), env);
  const set = res.headers.getSetCookie?.() ?? [];
  return { status: res.status, data: await res.json().catch(() => null), cookie: set.map((c) => c.split(';')[0]).filter((c) => !c.endsWith('=')).join('; ') };
}
const P = (x = {}) => ({ v: 1, lessons: {}, items: {}, ...x });
// What src/lib/learner.ts does on a device: send local state, then merge the reply into it.
async function sync(cookie, local) {
  const r = await call('PUT', '/api/learner/sync', { notebook: { items: {} }, progress: local }, cookie);
  assert.equal(r.status, 200, JSON.stringify(r.data));
  return mergeProgress(r.data.progress, local);
}

let n = 0;
const check = async (name, fn) => { await fn(); n++; console.log('  ok  ' + name); };

const made = await call('POST', '/api/learner/test/create', { name: 'Ada' });
assert.equal(made.status, 200, JSON.stringify(made.data));
const phone = made.cookie;
const laptop = (await call('POST', '/api/learner/test/session', { id: made.data.id })).cookie;
assert.ok(phone && laptop);

let onPhone = P({ path: 'mcat', pathAt: 1000, last: 'glycolysis', lessons: { glycolysis: { v: 900, d: 1100 }, 'amino-acids': { v: 950, d: 1200 } }, items: { 'glycolysis:q1': { l: 'glycolysis', n: 1, c: 0, s: 0, due: 5000, t: 1150 } } });
let onLaptop = P();

await check('two devices end up with the same progress', async () => {
  onPhone = await sync(phone, onPhone);
  onLaptop = await sync(laptop, onLaptop);
  assert.deepEqual(onLaptop.lessons, onPhone.lessons);
  assert.equal(onLaptop.path, 'mcat');
});
await check('unticking "done" on the laptop sticks there and reaches the phone', async () => {
  delete onLaptop.lessons.glycolysis.d; onLaptop.lessons.glycolysis.u = 2000;     // what setDone(slug, false) writes
  onLaptop = await sync(laptop, onLaptop);
  assert.equal(onLaptop.lessons.glycolysis.d, undefined);
  onPhone = await sync(phone, onPhone);
  assert.equal(onPhone.lessons.glycolysis.d, undefined);
  assert.equal(onPhone.lessons['amino-acids'].d, 1200);
});
await check('clearing the path on the phone sticks and reaches the laptop', async () => {
  delete onPhone.path; onPhone.pathAt = 3000;                                    // what setPath(null) writes
  onPhone = await sync(phone, onPhone);
  assert.equal(onPhone.path, undefined);
  onLaptop = await sync(laptop, onLaptop);
  assert.equal(onLaptop.path, undefined);
});
await check('reset on the laptop clears the server and the phone', async () => {
  onLaptop = P({ reset: 4000 });                                                 // what clearAll() writes
  onLaptop = await sync(laptop, onLaptop);
  assert.deepEqual(onLaptop, P({ reset: 4000 }));
  onPhone = await sync(phone, onPhone);
  assert.deepEqual(onPhone, P({ reset: 4000 }));
  const stored = JSON.parse(db.sql.prepare('SELECT progress_json FROM learner_data').get().progress_json);
  assert.deepEqual(stored, P({ reset: 4000 }));
});
await check('work after the reset syncs as usual', async () => {
  onPhone.lessons.glycolysis = { v: 4500, d: 4600 }; onPhone.last = 'glycolysis';
  onPhone = await sync(phone, onPhone);
  onLaptop = await sync(laptop, onLaptop);
  assert.equal(onLaptop.lessons.glycolysis.d, 4600);
  assert.equal(onLaptop.last, 'glycolysis');
});
await check('stored data over the byte cap is refused with 413, not a database error', async () => {
  // Multibyte text: under 1 MB of characters per request, far more in bytes once two devices' notes merge.
  const note = (id) => ({ id, kind: 'note', slug: 'glycolysis', updated: Date.now(), text: '酵'.repeat(60_000) });
  const batch = (k) => Object.fromEntries(Array.from({ length: 5 }, (_, i) => [`n${k}-${i}`, note(`n${k}-${i}`)]));
  const a = await call('PUT', '/api/learner/sync', { notebook: { items: batch(1) }, progress: P() }, phone);
  assert.equal(a.status, 200);                                                   // 5 x 180 kB = 0.9 MB stored
  const b = await call('PUT', '/api/learner/sync', { notebook: { items: batch(2) }, progress: P() }, phone);
  assert.equal(b.status, 413);                                                   // would be 1.8 MB+ stored
  const row = db.sql.prepare('SELECT length(CAST(notebook_json AS BLOB)) AS bytes FROM learner_data').get();
  assert.ok(row.bytes < 1_800_000, `stored ${row.bytes} bytes`);
});
await check('the invitation email budget is spent by the email, not by the call', async () => {
  const key = 'gmail:test';
  assert.equal(await allowN(db, key, 30, 60, 86_400_000), true);
  assert.equal(await allowN(db, key, 30, 60, 86_400_000), true);
  assert.equal(await allowN(db, key, 1, 60, 86_400_000), false);
  assert.equal(db.sql.prepare('SELECT count FROM rate_limits WHERE key=?').get(key).count, 60);
});
console.log(`${n} passed`);
