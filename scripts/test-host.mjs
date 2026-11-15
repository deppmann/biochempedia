// The site's address and the move to a new one (src/lib/site-host.mjs, worker/host.js,
// worker/handoff.js, src/lib/handoff-merge.mjs), in Node with no network:
//   node scripts/test-host.mjs
// Both phases are checked by passing the host settings in, so the test does not depend on which
// phase the repository is in. The worker itself is also run once with a stand-in for the static
// assets, on whatever PRIMARY_HOST is set to now.
import { register } from 'node:module';
import { DatabaseSync } from 'node:sqlite';
import { readFileSync, readdirSync, statSync } from 'node:fs';
import { join } from 'node:path';
import assert from 'node:assert/strict';

register('data:text/javascript,' + encodeURIComponent(`export async function load(u,c,n){return u.endsWith('.json')?n(u,{...c,importAttributes:{type:'json'}}):n(u,c)}`));
const H = await import('../worker/host.js');
const HO = await import('../worker/handoff.js');
const M = await import('../src/lib/handoff-merge.mjs');
const S = await import('../src/lib/site-host.mjs');
const L = await import('../worker/learner.js');
const worker = (await import('../worker/index.js')).default;

const KNOWN = ['biochemistrypedia.com', 'www.biochemistrypedia.com', 'stemhop.com', 'www.stemhop.com'];
const A = { primary: 'biochemistrypedia.com', legacy: 'biochemistrypedia.com', rpId: 'biochemistrypedia.com', known: KNOWN };
const B = { ...A, primary: 'stemhop.com' };

let n = 0;
const check = async (name, fn) => { await fn(); n++; console.log('  ok  ' + name); };
const NAV = { 'Sec-Fetch-Mode': 'navigate', 'Sec-Fetch-Dest': 'document', 'User-Agent': 'Mozilla/5.0 (Macintosh) AppleWebKit/605.1.15 Safari/605.1.15' };
const req = (url, { method = 'GET', headers = {}, body } = {}) => new Request(url, { method, headers, ...(body !== undefined ? { body } : {}) });
const go = (url, cfg, opts) => H.route(req(url, opts), cfg);

console.log('host settings');
await check('the settings file is self-consistent', () => {
  assert.ok(S.KNOWN_HOSTS.includes(S.PRIMARY_HOST), 'PRIMARY_HOST must be one of KNOWN_HOSTS');
  assert.ok(S.KNOWN_HOSTS.includes(S.LEGACY_HOST));
  assert.equal(S.PASSKEY_RP_ID, 'biochemistrypedia.com', 'the passkey RP ID must never change');
  assert.equal(S.SITE_ORIGIN, `https://${S.PRIMARY_HOST}`);
  for (const h of S.KNOWN_HOSTS) assert.match(h, /^[a-z0-9.-]+$/);
});
await check('wrangler.jsonc does not set a second, conflicting address', () => {
  const w = readFileSync(new URL('../wrangler.jsonc', import.meta.url), 'utf8');
  assert.ok(!/"PRIMARY_HOST"\s*:/.test(w));
  assert.match(w, /"run_worker_first": \["\/\*"/, 'pages must reach the worker, or other hosts would be served');
});

console.log('phase A (primary biochemistrypedia.com)');
await check('the primary host, its www and plain http are served as before', () => {
  for (const u of ['https://biochemistrypedia.com/lessons/action-potential/', 'http://biochemistrypedia.com/lessons/action-potential/?x=1',
    'https://www.biochemistrypedia.com/', 'https://biochemistrypedia.com/api/learner/me', 'https://biochemistrypedia.com/explainers/a/explainer.mp4']) {
    assert.deepEqual(go(u, A, { headers: NAV }), { kind: 'pass' }, u);
  }
  assert.deepEqual(go('https://biochemistrypedia.com/api/learner/sync', A, { method: 'PUT' }), { kind: 'pass' });
});
await check('stemhop.com and www.stemhop.com: 302 to the same path and query, for everything', () => {
  for (const host of ['stemhop.com', 'www.stemhop.com', 'STEMHOP.com']) {
    for (const p of ['/', '/lessons/action-potential/', '/lessons/action-potential/?utm_source=x&a=1', '/lessons/action-potential.md',
      '/api/learner/me', '/explainers/a/explainer.mp4', '/g/some-school/', '/handoff/', '/.well-known/webauthn']) {
      for (const scheme of ['https', 'http']) {
        const r = go(`${scheme}://${host}${p}`, A, { headers: NAV });
        assert.deepEqual(r, { kind: 'redirect', status: 302, location: `https://biochemistrypedia.com${p}` }, `${scheme}://${host}${p}`);
      }
    }
  }
});
await check('phase A: a POST to stemhop.com keeps its method (307), so nothing is saved there', () => {
  assert.deepEqual(go('https://stemhop.com/api/learner/sync', A, { method: 'PUT' }), { kind: 'redirect', status: 307, location: 'https://biochemistrypedia.com/api/learner/sync' });
  assert.deepEqual(go('https://stemhop.com/handoff/receive', A, { method: 'POST' }).status, 307);
});
await check('phase A: no hand-off anywhere', () => {
  assert.deepEqual(go('https://biochemistrypedia.com/handoff/', A, { headers: NAV }), { kind: 'pass' });
});
await check('hosts that are not ours (local, the workers.dev preview) are served as they are', () => {
  for (const cfg of [A, B]) {
    assert.deepEqual(go('http://localhost:8787/lessons/x/', cfg, { headers: NAV }), { kind: 'pass' });
    assert.deepEqual(go('https://biochempedia.deppmann.workers.dev/x/', cfg), { kind: 'pass' });
  }
});

console.log('phase B (primary stemhop.com)');
await check('stemhop.com is served; www.stemhop.com sends 301 there', () => {
  assert.deepEqual(go('https://stemhop.com/lessons/action-potential/', B, { headers: NAV }), { kind: 'pass' });
  assert.deepEqual(go('https://www.stemhop.com/lessons/a/?q=1', B, { headers: NAV }), { kind: 'redirect', status: 301, location: 'https://stemhop.com/lessons/a/?q=1' });
});
await check('old social links (apex, www, http, query) land on the same lesson with a 301', () => {
  for (const host of ['biochemistrypedia.com', 'www.biochemistrypedia.com']) {
    for (const scheme of ['https', 'http']) {
      for (const p of ['/lessons/action-potential/', '/lessons/action-potential/?utm_source=instagram&utm_medium=social', '/lessons/action-potential', '/lessons/action-potential/skim/']) {
        const r = go(`${scheme}://${host}${p}`, B);   // a crawler or link preview: no navigation headers
        assert.deepEqual(r, { kind: 'redirect', status: 301, location: `https://stemhop.com${p}` }, `${scheme}://${host}${p}`);
      }
    }
  }
});
await check('a person following an old link gets the hand-off page first, with the path and query kept', () => {
  const r = go('https://biochemistrypedia.com/lessons/action-potential/?utm_source=x', B, { headers: NAV });
  assert.deepEqual(r, { kind: 'handoff', to: '/lessons/action-potential/?utm_source=x' });
  assert.deepEqual(go('http://www.biochemistrypedia.com/', B, { headers: NAV }), { kind: 'handoff', to: '/' });
});
await check('repeat visitors (bp_moved), crawlers, previews, files, feeds, HEAD and API get the plain 301/308', () => {
  const loc = 'https://stemhop.com/lessons/a/';
  assert.deepEqual(go('https://biochemistrypedia.com/lessons/a/', B, { headers: { ...NAV, Cookie: 'x=1; bp_moved=1' } }), { kind: 'redirect', status: 301, location: loc });
  assert.deepEqual(go('https://biochemistrypedia.com/lessons/a/', B, { headers: { ...NAV, 'User-Agent': 'Mozilla/5.0 (compatible; Googlebot/2.1)' } }).status, 301);
  assert.deepEqual(go('https://biochemistrypedia.com/lessons/a/', B, { headers: { ...NAV, 'User-Agent': 'Slackbot-LinkExpanding 1.0' } }).status, 301);
  assert.deepEqual(go('https://biochemistrypedia.com/lessons/a/', B, { method: 'HEAD', headers: NAV }).status, 301);
  for (const p of ['/lessons/a.md', '/sitemap.xml', '/updates.xml', '/llms.txt', '/og.png', '/explainers/a/explainer.mp4', '/api/learner/me', '/g/x/']) {
    const r = go(`https://biochemistrypedia.com${p}`, B, { headers: p === '/g/x/' ? {} : NAV });
    assert.deepEqual(r, { kind: 'redirect', status: 301, location: `https://stemhop.com${p}` }, p);
  }
  assert.deepEqual(go('https://biochemistrypedia.com/api/learner/sync', B, { method: 'PUT' }), { kind: 'redirect', status: 308, location: 'https://stemhop.com/api/learner/sync' });
});
await check('the hand-off exemptions stay on the old host', () => {
  assert.deepEqual(go('https://biochemistrypedia.com/handoff/?to=/lessons/a/', B), { kind: 'handoff', to: '/lessons/a/' });
  assert.deepEqual(go('https://biochemistrypedia.com/handoff/', B, { headers: { ...NAV, Cookie: 'bp_moved=1' } }), { kind: 'handoff', to: '/' });
  assert.deepEqual(go('https://www.biochemistrypedia.com/handoff/signin/?to=/account/', B), { kind: 'signin' });
  for (const p of ['/api/learner/passkey/login/options', '/api/learner/passkey/login/verify', '/api/learner/bridge/issue']) {
    assert.deepEqual(go(`https://biochemistrypedia.com${p}`, B, { method: 'POST' }), { kind: 'pass' }, p);
  }
  assert.deepEqual(go('https://biochemistrypedia.com/.well-known/webauthn', B), { kind: 'webauthn' });
  // Everything else under /api/learner moves.
  assert.equal(go('https://biochemistrypedia.com/api/learner/passkey/register/options', B, { method: 'POST' }).status, 308);
});
await check('the new host receives and merges; nothing else does', () => {
  assert.deepEqual(go('https://stemhop.com/handoff/receive', B, { method: 'POST' }), { kind: 'receive' });
  assert.deepEqual(go('https://stemhop.com/handoff/merge', B, { method: 'POST' }), { kind: 'merge' });
  assert.deepEqual(go('https://stemhop.com/handoff/receive', B), { kind: 'pass' });   // a GET is just a 404 page
});

console.log('passkeys and links');
await check('/.well-known/webauthn lists the stemhop origins, only on the RP ID host', () => {
  assert.deepEqual(H.webauthnOrigins(A), ['https://stemhop.com', 'https://www.stemhop.com']);
  assert.deepEqual(H.webauthnOrigins(B), ['https://stemhop.com', 'https://www.stemhop.com']);
  assert.deepEqual(go('https://biochemistrypedia.com/.well-known/webauthn', A), { kind: 'webauthn' });
  assert.equal(go('https://www.biochemistrypedia.com/.well-known/webauthn', A).kind, 'pass');
});
await check('links we write (emails, Google) use the primary host', () => {
  assert.equal(H.siteOrigin('https://www.biochemistrypedia.com/api/x', A), 'https://biochemistrypedia.com');
  assert.equal(H.siteOrigin('https://biochemistrypedia.com/api/x', B), 'https://stemhop.com');
  assert.equal(H.siteOrigin('http://localhost:8787/api/x', B), 'http://localhost:8787');
  assert.deepEqual(H.legacyOrigins(B), ['https://biochemistrypedia.com', 'http://biochemistrypedia.com', 'https://www.biochemistrypedia.com', 'http://www.biochemistrypedia.com']);
});

console.log('hand-off pages');
await check('the old host page posts only to the primary host and only ever forwards to a path', async () => {
  const html = await HO.handoffPage('/lessons/a/?x=1', B).text();
  assert.match(html, /action="https:\/\/stemhop\.com\/handoff\/receive"/);
  assert.match(html, /"to":"\/lessons\/a\/\?x=1"/);
  for (const evil of ['//evil.com/x', 'https://evil.com', '/\\evil.com', 'javascript:alert(1)', '/a b']) assert.equal(HO.safePath(evil), '/', evil);
  const x = await HO.handoffPage('/</script><script>alert(1)</script>', B).text();
  assert.ok(!x.includes('</script><script>alert(1)'), 'a path cannot break out of the script');
  const res = HO.handoffPage('/', B);
  assert.equal(res.headers.get('Cache-Control'), 'no-store');
  assert.equal(res.headers.get('X-Robots-Tag'), 'noindex');
  assert.notEqual(res.headers.get('Referrer-Policy'), 'no-referrer', 'no-referrer would make the form post carry Origin: null');
});

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
const form = (o) => new URLSearchParams(o).toString();
const post = (origin, fields) => req('https://stemhop.com/handoff/receive', { method: 'POST', headers: { Origin: origin, 'Content-Type': 'application/x-www-form-urlencoded' }, body: form(fields) });

await check('/handoff/receive refuses a post that did not come from the old host', async () => {
  for (const o of ['https://evil.example', 'null', '', 'https://stemhop.com']) {
    const r = await HO.receive(post(o, { data: '{"v":1,"items":{}}', to: '/' }), {}, B);
    assert.equal(r.status, 403, o);
  }
});
await check('/handoff/receive keeps only site keys, embeds them safely, and carries a sign-in', async () => {
  const db = makeDb();
  const now = Date.now();
  db.sql.prepare("INSERT INTO learners (id, display_name, email, google_sub, created_at, last_active_at) VALUES ('L1','Ada',NULL,NULL,?,?)").run(now, now);
  const code = await L.issueBridge(db, 'L1');
  const items = { 'biochempedia:progress:v1': '{"v":1,"lessons":{},"items":{}}', 'bp-cer:/lessons/a/:x': '{"t":"</script><b>"}', 'someone-else': 'x' };
  const r = await HO.receive(post('http://www.biochemistrypedia.com', { data: JSON.stringify({ v: 1, items }), to: '/lessons/a/#sec', signin: code }), {}, B,
    (c) => L.redeemBridge(db, new Request('https://stemhop.com/handoff/receive'), c));
  assert.equal(r.status, 200);
  const html = await r.text();
  assert.ok(html.includes('biochempedia:progress:v1') && html.includes('bp-cer:'));
  assert.ok(!html.includes('someone-else'), 'keys that are not ours are dropped');
  assert.ok(!html.includes('</script><b>'), 'saved text cannot close the script');
  assert.match(html, /"to":"\/lessons\/a\/#sec"/);
  const cookies = r.headers.getSetCookie();
  assert.ok(cookies.some((c) => /^bp_learner=[0-9a-f]{64};.*HttpOnly.*Secure/.test(c)), 'a session on the new host');
  assert.ok(cookies.some((c) => c.startsWith('bp_signed_in=1')));
  // Single use.
  assert.deepEqual(await L.redeemBridge(db, new Request('https://stemhop.com/'), code), []);
  // A normal login flow row (no "bridge:" challenge) is never accepted as a sign-in code.
  const raw = 'a'.repeat(64);
  const { sha256Hex } = await import('../worker/auth.js');
  db.sql.prepare("INSERT INTO learner_challenges (id, purpose, challenge, learner_id, display_name, extra, created_at, expires_at) VALUES (?,?,?,?,?,?,?,?)")
    .run(await sha256Hex(raw), 'login', 'ordinary-challenge', 'L1', null, null, now, now + 60_000);
  assert.deepEqual(await L.redeemBridge(db, new Request('https://stemhop.com/'), raw), []);
  // An expired code does nothing.
  const old = await L.issueBridge(db, 'L1');
  db.sql.prepare('UPDATE learner_challenges SET expires_at=0').run();
  assert.deepEqual(await L.redeemBridge(db, new Request('https://stemhop.com/'), old), []);
});
await check('/handoff/merge is same-origin JSON only', async () => {
  const bad = await HO.mergeEndpoint(req('https://stemhop.com/handoff/merge', { method: 'POST', headers: { Origin: 'https://evil.example', 'Content-Type': 'application/json' }, body: '{}' }));
  assert.equal(bad.status, 403);
  const ok = await HO.mergeEndpoint(req('https://stemhop.com/handoff/merge', { method: 'POST', headers: { Origin: 'https://stemhop.com', 'Content-Type': 'application/json' }, body: JSON.stringify({ current: {}, incoming: { 'bp-supports': '1' } }) }));
  assert.deepEqual(await ok.json(), { write: { 'bp-supports': '1' } });
});

console.log('merging what came across');
const J = (x) => JSON.stringify(x);
await check('nothing to move, nothing written', () => {
  assert.deepEqual(M.mergeStorage({}, {}), { write: {} });
  assert.deepEqual(M.mergeStorage({ 'bp-supports': '2' }, undefined), { write: {} });
});
await check('a key the new host lacks is copied; one it has is kept (it is newer)', () => {
  const w = M.mergeStorage({ 'bp-supports': '2', 'biochempedia:listen:rate': '1.25' }, { 'bp-supports': '0', 'biochempedia:class:v1': '{"code":"ABC"}', 'biochempedia:listen:rate': '1.25' }).write;
  assert.deepEqual(w, { 'biochempedia:class:v1': '{"code":"ABC"}' });
});
await check('probes, the account cache and other sites\' keys are not carried', () => {
  const w = M.mergeStorage({}, { 'biochempedia:probe': '1', 'biochempedia:learner:v1': '{}', 'biochempedia:progress:v1:test': '1', 'other:key': 'x', 'biochempedia:notebook:v1:probe': '1' }).write;
  assert.deepEqual(w, {});
});
await check('progress merges lesson by lesson; newer marks on the new host survive', () => {
  const cur = { v: 1, lessons: { a: { v: 500, d: 900 } }, items: { q1: { t: 900, s: 2 } }, last: 'a' };
  const inc = { v: 1, lessons: { a: { v: 100, d: 200 }, b: { v: 300 } }, items: { q1: { t: 100, s: 0 }, q2: { t: 50 } }, last: 'b' };
  const out = JSON.parse(M.mergeStorage({ 'biochempedia:progress:v1': J(cur) }, { 'biochempedia:progress:v1': J(inc) }).write['biochempedia:progress:v1']);
  assert.deepEqual(out.lessons, { a: { v: 100, d: 900 }, b: { v: 300 } });
  assert.deepEqual(out.items.q1, { t: 900, s: 2 });
  assert.ok(out.items.q2);
  assert.equal(out.last, 'a');
});
await check('notebook: per item the later edit wins, deletions included', () => {
  const it = (id, updated, extra = {}) => ({ id, kind: 'note', slug: 's', updated, ...extra });
  const cur = { v: 1, items: { x: it('x', 900, { note: 'new' }), y: it('y', 800, { deleted: true }) } };
  const inc = { v: 1, items: { x: it('x', 100, { note: 'old' }), y: it('y', 100), z: it('z', 300) } };
  const out = JSON.parse(M.mergeStorage({ 'biochempedia:notebook:v1': J(cur) }, { 'biochempedia:notebook:v1': J(inc) }, 1000).write['biochempedia:notebook:v1']);
  assert.equal(out.items.x.note, 'new');
  assert.equal(out.items.y.deleted, true);
  assert.ok(out.items.z);
});
await check('flashcard schedule, films and personal cards merge without losing either side', () => {
  const cards = M.mergeStorage({ 'biochempedia:cards:v1': J({ v: 1, cards: { 'a:1': { t: 900, due: 5 }, 'a:2': { t: 1, due: 1 } } }) },
    { 'biochempedia:cards:v1': J({ v: 1, cards: { 'a:1': { t: 100, due: 9 }, 'a:2': { t: 50, due: 2 }, 'b:1': { t: 10, due: 3 } } }) }).write;
  assert.deepEqual(JSON.parse(cards['biochempedia:cards:v1']).cards, { 'a:1': { t: 900, due: 5 }, 'a:2': { t: 50, due: 2 }, 'b:1': { t: 10, due: 3 } });
  const films = JSON.parse(M.mergeStorage(
    { 'biochempedia:films:v1': J({ v: 1, w: { f1: 500 }, p: [{ f: 'f2', at: 900, t: 30 }], q: { c: { f: 'f2', t: 30, at: 900 } } }) },
    { 'biochempedia:films:v1': J({ v: 1, w: { f1: 100, f3: 50 }, p: [{ f: 'f2', at: 100, t: 5 }, { f: 'f4', at: 80, t: 9 }], q: { c: { f: 'f9', t: 1, at: 10 }, d: { f: 'f4', t: 9, at: 80 } }, b: { 'course:c': { at: 5 } } }) },
  ).write['biochempedia:films:v1']);
  assert.deepEqual(films.w, { f1: 100, f3: 50 });
  assert.deepEqual(films.p.map((x) => [x.f, x.at]), [['f2', 900], ['f4', 80]]);
  assert.equal(films.q.c.f, 'f2');
  assert.ok(films.q.d && films.b['course:c']);
  const my = JSON.parse(M.mergeStorage({ 'biochempedia:mycards:v1': J({ v: 1, decks: { s: [{ id: 'my-card1', front: 'new' }] } }) },
    { 'biochempedia:mycards:v1': J({ v: 1, decks: { s: [{ id: 'my-card1', front: 'old' }, { id: 'my-card2', front: 'b' }], t: [{ id: 'my-card3' }] } }) }).write['biochempedia:mycards:v1']);
  assert.deepEqual(my.decks.s.map((c) => c.front), ['new', 'b']);
  assert.equal(my.decks.t.length, 1);
});
await check('damaged data never replaces good data', () => {
  assert.deepEqual(M.mergeStorage({ 'biochempedia:cards:v1': J({ v: 1, cards: {} }) }, { 'biochempedia:cards:v1': '{broken' }).write, {});
  assert.deepEqual(M.mergeStorage({ 'biochempedia:cards:v1': '{broken' }, { 'biochempedia:cards:v1': J({ v: 1, cards: {} }) }).write, { 'biochempedia:cards:v1': J({ v: 1, cards: {} }) });
});
await check('running the hand-off twice changes nothing the second time', () => {
  const cur = { 'biochempedia:progress:v1': J({ v: 1, lessons: { a: { v: 5 } }, items: {} }), 'bp-supports': '1' };
  const inc = { 'biochempedia:progress:v1': J({ v: 1, lessons: { b: { v: 9, d: 10 } }, items: {} }), 'bcp-arcade:muted': '1', 'bp-supports': '2' };
  const after = { ...cur, ...M.mergeStorage(cur, inc).write };
  assert.deepEqual(M.mergeStorage(after, inc), { write: {} });
});
await check('every localStorage key the site writes is one the hand-off carries', () => {
  const found = new Set();
  const walk = (d) => {
    for (const f of readdirSync(d)) {
      const p = join(d, f);
      if (statSync(p).isDirectory()) walk(p);
      else if (/\.(astro|ts|mjs|js)$/.test(f)) {
        const t = readFileSync(p, 'utf8');
        if (!/localStorage/.test(t)) continue;
        for (const m of t.matchAll(/['"`]((?:biochempedia|bcp|bp)[-:][A-Za-z0-9:_\-]*)/g)) found.add(m[1]);
      }
    }
  };
  walk(new URL('../src/', import.meta.url).pathname);
  // Literals that are event names, CSS classes or sessionStorage only, not localStorage keys.
  const notKeys = /^bp-(cards-open|class|films|learner|mycards|notebook|progress|reading|section|hl|lp|listen)\b|^biochempedia:(cards-prompt|films:budget)|^biochempedia-/;
  const keys = [...found].filter((k) => !notKeys.test(k));
  assert.ok(keys.length >= 15, 'found the keys: ' + keys.join(' '));
  for (const k of keys) {
    const sample = k.endsWith(':') ? k + 'x' : k;
    assert.ok(M.HANDOFF_KEY.test(sample), `${k} is not carried by the hand-off: add its prefix to HANDOFF_KEY`);
  }
});

console.log('the worker, end to end, on the current setting (' + S.PRIMARY_HOST + ')');
await check('primary host pages are the static asset response, untouched; others redirect', async () => {
  const seen = [];
  const sentinel = new Response('PAGE', { headers: { 'X-From': 'assets' } });
  const env = { ASSETS: { fetch: async (r) => { seen.push(new URL(r.url).pathname); return sentinel; } } };
  const res = await worker.fetch(req(`https://${S.PRIMARY_HOST}/lessons/action-potential/`, { headers: NAV }), env);
  assert.equal(res, sentinel, 'the very same response object');
  assert.deepEqual(seen, ['/lessons/action-potential/']);
  const other = S.KNOWN_HOSTS.find((h) => !H.inFamily(h, S.PRIMARY_HOST) && !H.inFamily(S.PRIMARY_HOST, h) && !(H.switched() === false && H.inFamily(h, S.LEGACY_HOST)));
  const r2 = await worker.fetch(req(`https://${other}/lessons/action-potential/?a=1`), env);
  assert.ok([301, 302].includes(r2.status));
  assert.equal(r2.headers.get('Location'), `https://${S.PRIMARY_HOST}/lessons/action-potential/?a=1`);
  const wk = await worker.fetch(req(`https://${S.PASSKEY_RP_ID}/.well-known/webauthn`), env);
  assert.equal(wk.headers.get('Content-Type'), 'application/json');
  assert.ok((await wk.json()).origins.includes('https://stemhop.com'));
});

console.log(`\n${n} checks passed.`);
