// Assignment order (worker/api.js), in Node with no network:
//   node scripts/test-assign-order.mjs
// The class page's "Also assign" boxes put a lesson's review-first lessons just before it in the
// list it saves. These checks prove the order a teacher saves is the order the brief and students
// get back among lessons due the same day, that due dates still come first, and that re-saving
// keeps it. D1 is an in-memory SQLite shim loaded with the real migrations.
import { register } from 'node:module';
import { DatabaseSync } from 'node:sqlite';
import { readFileSync, readdirSync } from 'node:fs';
import assert from 'node:assert/strict';

register('data:text/javascript,' + encodeURIComponent(`export async function load(u,c,n){return u.endsWith('.json')?n(u,{...c,importAttributes:{type:'json'}}):n(u,c)}`));
const { handleApi } = await import('../worker/api.js');

function makeDb() {
  const sql = new DatabaseSync(':memory:');
  const dir = new URL('../migrations/', import.meta.url);
  for (const f of readdirSync(dir).sort()) sql.exec(readFileSync(new URL(f, dir), 'utf8'));
  const stmt = (q, args = []) => ({
    bind: (...a) => stmt(q, a),
    run: async () => { const r = sql.prepare(q).run(...args); return { meta: { changes: Number(r.changes), last_row_id: Number(r.lastInsertRowid) } }; },
    first: async () => sql.prepare(q).get(...args) ?? null,
    all: async () => ({ results: sql.prepare(q).all(...args) }),
    _run: () => sql.prepare(q).run(...args),
  });
  return { prepare: (q) => stmt(q), batch: async (ss) => ss.map((s) => ({ meta: { changes: Number(s._run().changes) } })), sql };
}

const ORIGIN = 'http://localhost:8787';
let ipN = 0;
async function call(env, method, path, body, cookie) {
  const res = await handleApi(new Request(ORIGIN + path, {
    method, headers: { 'Content-Type': 'application/json', Origin: ORIGIN, 'CF-Connecting-IP': `198.51.100.${++ipN % 250}`, ...(cookie ? { Cookie: cookie } : {}) },
    ...(body !== undefined ? { body: JSON.stringify(body) } : {}),
  }), env);
  const set = res.headers.getSetCookie?.() ?? [];
  return { status: res.status, data: await res.json().catch(() => null), cookie: set.map((c) => c.split(';')[0]).filter((c) => !c.endsWith('=')).join('; ') };
}

async function setup() {
  const env = { CLASSES: makeDb() };
  const t = await call(env, 'POST', '/api/teacher/signup', { email: `t${ipN}@example.com`, name: 'Ms. R', password: 'a-long-password', agree: true });
  assert.equal(t.status, 201, JSON.stringify(t.data));
  const c = await call(env, 'POST', '/api/classes', { name: 'Genetics', course: 'genetics' }, t.cookie);
  assert.equal(c.status, 201, JSON.stringify(c.data));
  const code = (await call(env, 'GET', `/api/classes/${c.data.id}/brief`, undefined, t.cookie)).data.class.code;
  const s = await call(env, 'POST', '/api/join', { code, nickname: 'Ava' });
  assert.equal(s.status, 200, JSON.stringify(s.data));
  const put = async (list) => {
    const r = await call(env, 'PUT', `/api/classes/${c.data.id}/assignments`, { assignments: list }, t.cookie);
    assert.equal(r.status, 200, JSON.stringify(r.data));
  };
  const brief = async () => (await call(env, 'GET', `/api/classes/${c.data.id}/brief`, undefined, t.cookie)).data.assignments.map((a) => a.slug);
  const student = async () => (await call(env, 'GET', '/api/student/me', undefined, s.cookie)).data.assignments.map((a) => a.slug);
  return { put, brief, student };
}

let passed = 0;
const test = async (name, fn) => { try { await fn(); passed++; console.log('ok   ' + name); } catch (e) { console.log('FAIL ' + name + '\n' + (e.stack || e)); process.exitCode = 1; } };

const DUE = '2026-11-20';

await test('review lessons saved before a lesson, due the same day, come back before it', async () => {
  const k = await setup();
  await k.put([{ slug: 'pedigrees', due: DUE }, { slug: 'mutation', due: DUE }, { slug: 'cancer-genetics', due: DUE }]);
  assert.deepEqual(await k.brief(), ['pedigrees', 'mutation', 'cancer-genetics']);
  assert.deepEqual(await k.student(), ['pedigrees', 'mutation', 'cancer-genetics']);
});

await test('review lessons added later go before a lesson that was assigned earlier', async () => {
  const k = await setup();
  await k.put([{ slug: 'cancer-genetics', due: DUE }]);
  // A later visit: the page puts the newly ticked review lessons ahead of the saved lesson.
  await k.put([{ slug: 'mutation', due: DUE }, { slug: 'dna-repair-and-recombination', due: DUE }, { slug: 'cancer-genetics', due: DUE }]);
  assert.deepEqual(await k.student(), ['mutation', 'dna-repair-and-recombination', 'cancer-genetics']);
  // Re-saving the list as the page reads it back keeps the order.
  await k.put((await k.brief()).map((slug) => ({ slug, due: DUE })));
  assert.deepEqual(await k.student(), ['mutation', 'dna-repair-and-recombination', 'cancer-genetics']);
});

await test('due dates still order first; no due date goes last', async () => {
  const k = await setup();
  await k.put([{ slug: 'linkage' }, { slug: 'pedigrees', due: DUE }, { slug: 'cancer-genetics', due: DUE }, { slug: 'mendel', due: '2026-11-18' }]);
  assert.deepEqual(await k.brief(), ['mendel', 'pedigrees', 'cancer-genetics', 'linkage']);
  assert.deepEqual(await k.student(), ['mendel', 'pedigrees', 'cancer-genetics', 'linkage']);
});

await test('among lessons due the same day, the order of the saved list holds (not the alphabet)', async () => {
  const k = await setup();
  await k.put([{ slug: 'mendel', due: DUE }, { slug: 'linkage', due: DUE }]);
  await k.put([...(await k.brief()).map((slug) => ({ slug, due: DUE })), { slug: 'pedigrees', due: DUE }]);
  assert.deepEqual(await k.student(), ['mendel', 'linkage', 'pedigrees']);
});

console.log(`\n${passed} passed${process.exitCode ? ', some FAILED' : ''}`);
