// The site's address and the move to a new one (src/lib/site-host.mjs, worker/host.js,
// worker/handoff.js, worker/index.js, src/lib/handoff-merge.mjs), in Node with no network:
//   node scripts/test-host.mjs
// Both phases are checked by passing the host settings in (createWorker(cfg) in worker/index.js), so
// the test does not depend on which phase the repository is in. Which paths reach the worker at all
// is read from run_worker_first in wrangler.jsonc, and both configurations are modelled.
import { register } from 'node:module';
import { DatabaseSync } from 'node:sqlite';
import { readFileSync, readdirSync, statSync } from 'node:fs';
import { join } from 'node:path';
import { createHash } from 'node:crypto';
import vm from 'node:vm';
import assert from 'node:assert/strict';

register('data:text/javascript,' + encodeURIComponent(`export async function load(u,c,n){return u.endsWith('.json')?n(u,{...c,importAttributes:{type:'json'}}):n(u,c)}`));
const H = await import('../worker/host.js');
const HO = await import('../worker/handoff.js');
const M = await import('../src/lib/handoff-merge.mjs');
const S = await import('../src/lib/site-host.mjs');
const L = await import('../worker/learner.js');
const { sha256Hex } = await import('../worker/auth.js');
const { createWorker, default: worker } = await import('../worker/index.js');

const KNOWN = ['biochemistrypedia.com', 'www.biochemistrypedia.com', 'stemhop.com', 'www.stemhop.com'];
const A = { primary: 'biochemistrypedia.com', legacy: 'biochemistrypedia.com', rpId: 'biochemistrypedia.com', known: KNOWN };
const B = { ...A, primary: 'stemhop.com' };

let n = 0;
const check = async (name, fn) => { await fn(); n++; console.log('  ok  ' + name); };
const NAV = { 'Sec-Fetch-Mode': 'navigate', 'Sec-Fetch-Dest': 'document', 'User-Agent': 'Mozilla/5.0 (Macintosh) AppleWebKit/605.1.15 Safari/605.1.15' };
const CHROME_UA = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/157.0.0.0 Safari/537.36';
// What Chrome sent on a plain-http navigation in the 2026-11-15 browser test: no Sec-Fetch-* at all.
const HTTP_NAV = { 'Upgrade-Insecure-Requests': '1', Accept: 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8', 'User-Agent': CHROME_UA };
const req = (url, { method = 'GET', headers = {}, body } = {}) => new Request(url, { method, headers, ...(body !== undefined ? { body } : {}) });
const go = (url, cfg, opts) => H.route(req(url, opts), cfg);

// ---- run_worker_first, as Cloudflare applies it: "*" matches across "/", "!" patterns win ----
const glob = (p) => new RegExp('^' + p.replace(/[.+?^${}()|[\]\\]/g, '\\$&').replace(/\*/g, '.*') + '$');
const workerFirst = (patterns, path) => patterns.some((p) => !p.startsWith('!') && glob(p).test(path)) && !patterns.some((p) => p.startsWith('!') && glob(p.slice(1)).test(path));
const wranglerText = readFileSync(new URL('../wrangler.jsonc', import.meta.url), 'utf8');
const CURRENT = JSON.parse(/"run_worker_first":\s*(\[[^\]]*\])/.exec(wranglerText)[1]);
const FOUR = ['/explainers/*', '/api/*', '/g/*', '/listen/*'];
const ALL = ['/*', '!/_astro/*', '!/pagefind/*', '!/vendor/*', '!/figures/*', '!/scientists/*', '!/quiz/*', '!/flashcards/*', '!/helper-data/*', '!/graph.json', '!/graph/*'];
/** What a request gets with a given run_worker_first: the static file as it is, or the worker's answer. */
const outcome = (url, cfg, patterns, opts) => (workerFirst(patterns, new URL(url).pathname) ? go(url, cfg, opts) : { kind: 'static' });

// ---- an in-memory D1 with the real migrations ----
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

// ---- a stand-in for the static assets, and for HTMLRewriter (body append only) ----
const ASSETS = { fetch: async (r) => new Response(`<html><body><main>PAGE ${new URL(r.url).pathname}</main></body></html>`, { headers: { 'Content-Type': 'text/html; charset=utf-8', 'X-From': 'assets' } }) };
// HTMLRewriter.transform returns a Response at once; here the rewrite is done first, so callers settle() it.
globalThis.HTMLRewriter = class {
  on(sel, h) { this.h = h; return this; }
  transform(res) {
    return { __pending: (async () => {
      const t = await res.text(); let add = '';
      this.h.element({ append: (s) => { add += s; } });
      return new Response(t.replace('</body>', add + '</body>'), { status: res.status, headers: res.headers });
    })() };
  }
};
const settle = async (r) => (r && r.__pending ? r.__pending : r);

/** The one inline script of a page and the CSP hash it must match. */
function scriptOf(html) {
  const all = [...html.matchAll(/<script>([\s\S]*?)<\/script>/g)];
  return all.length ? all[all.length - 1][1] : '';
}
const b64sha = (t) => createHash('sha256').update(t, 'utf8').digest('base64');

/**
 * Run a page's inline script with a small fake browser: localStorage, cookies, a form, fetch and
 * location. Returns what the page did.
 */
async function runPage(html, { origin, store = {}, cookie = '', fetchImpl = null } = {}) {
  const els = {};
  const el = (id) => els[id] || (els[id] = { id, hidden: true, textContent: '', onclick: null, elements: { data: {}, to: {}, signin: {} }, submitted: false, submit() { this.submitted = true; }, addEventListener() {}, appendChild() {}, click() {} });
  const dataBlock = /<script type="application\/json" id="d">([\s\S]*?)<\/script>/.exec(html);
  if (dataBlock) el('d').textContent = dataBlock[1].replace(/\\u003c/g, '<');
  const ls = new Map(Object.entries(store));
  const out = { replaced: null, cookie, fetched: [] };
  const ctx = {
    location: { protocol: new URL(origin).protocol, hash: '', replace: (u) => { out.replaced = u; } },
    document: {
      getElementById: el, querySelector: () => null, createElement: () => el('x' + Math.random()), body: { appendChild() {} },
      get cookie() { return out.cookie; }, set cookie(v) { out.cookie += (out.cookie ? '; ' : '') + v.split(';')[0]; },
    },
    localStorage: {
      get length() { return ls.size; }, key: (i) => [...ls.keys()][i] ?? null,
      getItem: (k) => (ls.has(k) ? ls.get(k) : null), setItem: (k, v) => { ls.set(k, String(v)); }, removeItem: (k) => { ls.delete(k); },
    },
    fetch: async (u, o) => { out.fetched.push(u); return fetchImpl ? fetchImpl(u, o) : new Response('{}', { status: 500 }); },
    JSON, Object, String, Number, encodeURIComponent, Blob, URL, Promise, Error, console,
  };
  vm.createContext(ctx);
  vm.runInContext(scriptOf(html), ctx);
  for (let i = 0; i < 20; i++) await new Promise((r) => setImmediate(r));
  return { ...out, els, store: Object.fromEntries(ls) };
}

console.log('host settings');
await check('the settings file is self-consistent', () => {
  assert.ok(S.KNOWN_HOSTS.includes(S.PRIMARY_HOST), 'PRIMARY_HOST must be one of KNOWN_HOSTS');
  assert.ok(S.KNOWN_HOSTS.includes(S.LEGACY_HOST));
  assert.equal(S.PASSKEY_RP_ID, 'biochemistrypedia.com', 'the passkey RP ID must never change');
  assert.equal(S.SITE_ORIGIN, `https://${S.PRIMARY_HOST}`);
  for (const h of S.KNOWN_HOSTS) assert.match(h, /^[a-z0-9.-]+$/);
});
await check('wrangler.jsonc: no second address, and run_worker_first is one of the two known shapes', () => {
  assert.ok(!/"PRIMARY_HOST"\s*:/.test(wranglerText));
  assert.ok(JSON.stringify(CURRENT) === JSON.stringify(FOUR) || JSON.stringify(CURRENT) === JSON.stringify(ALL), 'run_worker_first: ' + JSON.stringify(CURRENT));
});
await check('a phase B setting is refused unless the worker runs first for every page', () => {
  if (H.switched()) assert.ok(workerFirst(CURRENT, '/lessons/action-potential/') && workerFirst(CURRENT, '/'), 'PRIMARY_HOST moved but pages skip the worker: the old host would serve pages instead of redirecting');
  // Why: with only the four prefixes, an old-host page would be served as it is, never redirected.
  assert.deepEqual(outcome('https://biochemistrypedia.com/lessons/a/', B, FOUR, { headers: NAV }), { kind: 'static' });
  assert.equal(outcome('https://biochemistrypedia.com/lessons/a/', B, ALL).status, 301);
});

console.log('phase A (primary biochemistrypedia.com)');
await check('the primary host, its www and plain http are served as before', () => {
  for (const u of ['https://biochemistrypedia.com/lessons/action-potential/', 'http://biochemistrypedia.com/lessons/action-potential/?x=1',
    'https://www.biochemistrypedia.com/', 'https://biochemistrypedia.com/api/learner/me', 'https://biochemistrypedia.com/explainers/a/explainer.mp4']) {
    assert.deepEqual(go(u, A, { headers: NAV }), { kind: 'pass' }, u);
  }
  assert.deepEqual(go('https://biochemistrypedia.com/api/learner/sync', A, { method: 'PUT' }), { kind: 'pass' });
});
await check('stemhop.com, whatever reaches the worker: 302 to the same path and query', () => {
  for (const host of ['stemhop.com', 'www.stemhop.com', 'STEMHOP.com']) {
    for (const p of ['/', '/lessons/action-potential/', '/lessons/action-potential/?utm_source=x&a=1', '/lessons/action-potential.md',
      '/api/learner/me', '/explainers/a/explainer.mp4', '/g/some-school/', '/handoff/', '/.well-known/webauthn']) {
      for (const scheme of ['https', 'http']) {
        assert.deepEqual(go(`${scheme}://${host}${p}`, A, { headers: NAV }), { kind: 'redirect', status: 302, location: `https://biochemistrypedia.com${p}` }, `${scheme}://${host}${p}`);
      }
    }
  }
  assert.deepEqual(go('https://stemhop.com/api/learner/sync', A, { method: 'PUT' }), { kind: 'redirect', status: 307, location: 'https://biochemistrypedia.com/api/learner/sync' });
});
await check('stemhop.com attached by mistake with the four prefixes: pages served as they are, API and media sent home', () => {
  const lesson = 'https://stemhop.com/lessons/action-potential/';
  assert.deepEqual(outcome(lesson, A, FOUR, { headers: NAV }), { kind: 'static' });          // the page loads on stemhop.com
  assert.equal(outcome('https://stemhop.com/api/learner/sync', A, FOUR, { method: 'PUT' }).status, 307);   // no sign-in or sync there
  assert.equal(outcome('https://stemhop.com/explainers/a/explainer.mp4', A, FOUR).status, 302);
  assert.equal(outcome('https://stemhop.com/g/school/', A, FOUR).status, 302);
  assert.deepEqual(outcome('https://stemhop.com/_astro/x.css', A, FOUR), { kind: 'static' });
  // With every page worker-first, the page itself is sent home too.
  assert.equal(outcome(lesson, A, ALL, { headers: NAV }).status, 302);
  assert.deepEqual(outcome('https://stemhop.com/_astro/x.css', A, ALL), { kind: 'static' });
});
await check('phase A: no hand-off anywhere', () => {
  assert.deepEqual(go('https://biochemistrypedia.com/handoff/', A, { headers: NAV }), { kind: 'pass' });
  assert.deepEqual(go('https://biochemistrypedia.com/handoff/done', A), { kind: 'pass' });
});
await check('hosts that are not ours (local, the workers.dev preview) are served as they are', () => {
  for (const cfg of [A, B]) {
    assert.deepEqual(go('http://localhost:8787/lessons/x/', cfg, { headers: NAV }), { kind: 'pass' });
    assert.deepEqual(go('https://biochempedia.deppmann.workers.dev/x/', cfg), { kind: 'pass' });
  }
});

console.log('phase B (primary stemhop.com), the routing rules');
await check('stemhop.com is served; www.stemhop.com sends 301 there', () => {
  assert.deepEqual(go('https://stemhop.com/lessons/action-potential/', B, { headers: NAV }), { kind: 'pass' });
  assert.deepEqual(go('https://www.stemhop.com/lessons/a/?q=1', B, { headers: NAV }), { kind: 'redirect', status: 301, location: 'https://stemhop.com/lessons/a/?q=1' });
});
await check('old social links (apex, www, http, query) land on the same lesson with a 301', () => {
  for (const host of ['biochemistrypedia.com', 'www.biochemistrypedia.com']) {
    for (const scheme of ['https', 'http']) {
      for (const p of ['/lessons/action-potential/', '/lessons/action-potential/?utm_source=instagram&utm_medium=social', '/lessons/action-potential', '/lessons/action-potential/skim/']) {
        assert.deepEqual(go(`${scheme}://${host}${p}`, B), { kind: 'redirect', status: 301, location: `https://stemhop.com${p}` }, `${scheme}://${host}${p}`);
      }
    }
  }
});
await check('a person following an old link gets the hand-off page first; the moved cookie and bots get the 301', () => {
  assert.deepEqual(go('https://biochemistrypedia.com/lessons/action-potential/?utm_source=x', B, { headers: NAV }), { kind: 'handoff', to: '/lessons/action-potential/?utm_source=x' });
  assert.deepEqual(go('http://www.biochemistrypedia.com/', B, { headers: NAV }), { kind: 'handoff', to: '/' });
  const loc = 'https://stemhop.com/lessons/a/';
  assert.deepEqual(go('https://biochemistrypedia.com/lessons/a/', B, { headers: { ...NAV, Cookie: 'x=1; bp_moved=1' } }), { kind: 'redirect', status: 301, location: loc });
  assert.equal(go('https://biochemistrypedia.com/lessons/a/', B, { headers: { ...NAV, 'User-Agent': 'Mozilla/5.0 (compatible; Googlebot/2.1)' } }).status, 301);
  assert.equal(go('https://biochemistrypedia.com/lessons/a/', B, { headers: { ...NAV, 'User-Agent': 'Slackbot-LinkExpanding 1.0' } }).status, 301);
  assert.equal(go('https://biochemistrypedia.com/lessons/a/', B, { method: 'HEAD', headers: NAV }).status, 301);
  for (const p of ['/lessons/a.md', '/sitemap.xml', '/updates.xml', '/llms.txt', '/og.png', '/explainers/a/explainer.mp4', '/api/learner/me', '/g/x/']) {
    assert.deepEqual(go(`https://biochemistrypedia.com${p}`, B, { headers: p === '/g/x/' ? {} : NAV }), { kind: 'redirect', status: 301, location: `https://stemhop.com${p}` }, p);
  }
});
await check('plain-http old links: a browser navigation (no Sec-Fetch on http) gets the hand-off; crawlers and scripts do not', () => {
  for (const host of ['biochemistrypedia.com', 'www.biochemistrypedia.com']) {
    assert.deepEqual(go(`http://${host}/lessons/a/?u=1`, B, { headers: HTTP_NAV }), { kind: 'handoff', to: '/lessons/a/?u=1' }, host);
  }
  const no = (headers, url = 'http://biochemistrypedia.com/lessons/a/') => assert.equal(go(url, B, { headers }).status, 301, JSON.stringify(headers));
  no({ ...HTTP_NAV, 'User-Agent': 'Mozilla/5.0 (compatible; Googlebot/2.1; +http://www.google.com/bot.html)' });
  no({ ...HTTP_NAV, 'User-Agent': 'facebookexternalhit/1.1' });
  no({ ...HTTP_NAV, 'User-Agent': 'curl/8.7.1' });
  no({ ...HTTP_NAV, 'User-Agent': '' });
  no({ Accept: '*/*', 'User-Agent': 'curl/8.7.1' });
  no({ 'User-Agent': CHROME_UA, Accept: HTTP_NAV.Accept });                                  // no Upgrade-Insecure-Requests
  no({ ...HTTP_NAV, Accept: 'image/avif,image/webp,*/*' });                                    // an image, not a page
  no({ ...HTTP_NAV, 'Sec-Fetch-Mode': 'no-cors', 'Sec-Fetch-Dest': 'image' });                // Fetch Metadata wins when present
  no(HTTP_NAV, 'https://biochemistrypedia.com/lessons/a/');                                    // on https, browsers always send Sec-Fetch
  assert.equal(H.isBrowserNavigation(req('http://biochemistrypedia.com/', { headers: HTTP_NAV })), true);
  assert.equal(H.isBrowserNavigation(req('https://biochemistrypedia.com/', { headers: NAV })), true);
});
await check('the old-host exemptions', () => {
  assert.deepEqual(go('https://biochemistrypedia.com/handoff/?to=/lessons/a/', B), { kind: 'handoff', to: '/lessons/a/' });
  assert.deepEqual(go('https://biochemistrypedia.com/handoff/', B, { headers: { ...NAV, Cookie: 'bp_moved=1' } }), { kind: 'handoff', to: '/' });
  assert.deepEqual(go('https://biochemistrypedia.com/handoff/done?to=/x/', B), { kind: 'done', to: '/x/' });
  assert.deepEqual(go('https://www.biochemistrypedia.com/handoff/signin/?to=/account/', B), { kind: 'signin' });
  for (const p of ['/api/learner/passkey/login/options', '/api/learner/passkey/login/verify', '/api/learner/bridge/issue', '/api/learner/passkey/register/options', '/api/learner/passkey/register/verify']) {
    assert.deepEqual(go(`https://biochemistrypedia.com${p}`, B, { method: 'POST' }), { kind: 'pass' }, p);
  }
  assert.deepEqual(go('https://biochemistrypedia.com/.well-known/webauthn', B), { kind: 'webauthn' });
  assert.equal(go('https://biochemistrypedia.com/api/learner/sync', B, { method: 'POST' }).status, 308);
});
await check('links we write (emails, Google) use the primary host', () => {
  assert.equal(H.siteOrigin('https://www.biochemistrypedia.com/api/x', A), 'https://biochemistrypedia.com');
  assert.equal(H.siteOrigin('https://biochemistrypedia.com/api/x', B), 'https://stemhop.com');
  assert.equal(H.siteOrigin('http://localhost:8787/api/x', B), 'http://localhost:8787');
  assert.deepEqual(H.webauthnOrigins(B), ['https://stemhop.com', 'https://www.stemhop.com']);
});

console.log('phase B end to end, through the real fetch handler (worker/index.js)');
const db = makeDb();
const now = Date.now();
db.sql.prepare("INSERT INTO learners (id, display_name, email, google_sub, created_at, last_active_at) VALUES ('L1','Ada',NULL,NULL,?,?)").run(now, now);
const token = 'b'.repeat(64);
db.sql.prepare('INSERT INTO learner_sessions (token_hash, learner_id, created_at, expires_at) VALUES (?,?,?,?)').run(await sha256Hex(token), 'L1', now, now + 86_400_000);
const envB = { ASSETS, CLASSES: db };
const WB = createWorker(B);
const WA = createWorker(A);
const fetchB = async (url, opts) => settle(await WB.fetch(req(url, opts), envB));
const multipart = (fields) => { const f = new FormData(); for (const [k, v] of Object.entries(fields)) f.set(k, v); return f; };

await check('301 / 308 rules and the stemhop page, through fetch', async () => {
  let r = await fetchB('https://biochemistrypedia.com/lessons/a/?u=1');
  assert.equal(r.status, 301); assert.equal(r.headers.get('Location'), 'https://stemhop.com/lessons/a/?u=1'); assert.equal(r.headers.get('Cache-Control'), 'no-store');
  r = await fetchB('https://www.biochemistrypedia.com/api/learner/sync', { method: 'PUT', headers: { 'Content-Type': 'application/json' }, body: '{}' });
  assert.equal(r.status, 308);
  r = await fetchB('https://stemhop.com/lessons/a/', { headers: NAV });
  assert.equal(r.headers.get('X-From'), 'assets');
});
await check('the hand-off page: strict CSP with the script hash, multipart post to the new host only, no moved cookie yet', async () => {
  const r = await fetchB('https://biochemistrypedia.com/lessons/a/?u=1', { headers: NAV });
  assert.equal(r.status, 200);
  assert.equal(r.headers.get('Set-Cookie'), null, 'not marked as moved before the new host has the data');
  const html = await r.text();
  const csp = r.headers.get('Content-Security-Policy');
  assert.ok(csp.includes(`'sha256-${b64sha(scriptOf(html))}'`), 'script hash');
  assert.match(csp, /default-src 'none'/); assert.match(csp, /form-action https:\/\/stemhop\.com(;|$)/); assert.match(csp, /frame-ancestors 'none'/);
  assert.match(html, /enctype="multipart\/form-data" action="https:\/\/stemhop\.com\/handoff\/receive"/);
  assert.notEqual(r.headers.get('Referrer-Policy'), 'no-referrer', 'no-referrer would make the post carry Origin: null');
  for (const evil of ['//evil.com/x', 'https://evil.com', '/\\evil.com', 'javascript:alert(1)', '/a b']) assert.equal(HO.safePath(evil), '/', evil);
  const x = await (await fetchB('https://biochemistrypedia.com/handoff/?to=' + encodeURIComponent('/</script><script>alert(1)</script>'))).text();
  assert.ok(!x.includes('</script><script>alert(1)'));
});
await check('the hand-off page script: nothing saved marks moved at once; saved data is posted, unmarked; a failed try asks first', async () => {
  const html = await (await fetchB('https://biochemistrypedia.com/lessons/a/', { headers: NAV })).text();
  let p = await runPage(html, { origin: 'https://biochemistrypedia.com' });
  assert.match(p.cookie, /bp_moved=1/); assert.equal(p.replaced, 'https://stemhop.com/lessons/a/');
  p = await runPage(html, { origin: 'https://biochemistrypedia.com', store: { 'biochempedia:progress:v1': '{"v":1}', 'other': 'x' } });
  assert.ok(p.els.f.submitted, 'posted'); assert.ok(!/bp_moved/.test(p.cookie), 'not marked moved');
  assert.deepEqual(JSON.parse(p.els.f.elements.data.value).items, { 'biochempedia:progress:v1': '{"v":1}' });
  assert.equal(p.store['biochempedia:handoff:tries'], '1');
  p = await runPage(html, { origin: 'https://biochemistrypedia.com', store: { 'bp-supports': '1', 'biochempedia:handoff:tries': '1' } });
  assert.ok(!p.els.f?.submitted, 'after a failed try it asks instead of posting again'); assert.equal(p.els.ask.hidden, false); assert.equal(p.replaced, null);
  const big = 'x'.repeat(M.MAX_STORE_CHARS + 10);
  p = await runPage(html, { origin: 'https://biochemistrypedia.com', store: { 'bp-design:a:b': big } });
  assert.ok(!p.els.f?.submitted); assert.equal(p.els.save.hidden, false, 'too large: offers a download');
  // A signed-in learner on http is not offered a sign-in code (and nothing is fetched).
  p = await runPage(html, { origin: 'http://biochemistrypedia.com', cookie: 'bp_signed_in=1', store: { 'bp-supports': '1' } });
  assert.deepEqual(p.fetched, []);
});
await check('a plain-http old link through fetch: the hand-off page; with bp_moved or as a crawler, the 301', async () => {
  const r = await fetchB('http://biochemistrypedia.com/lessons/a/?u=1', { headers: HTTP_NAV });
  assert.equal(r.status, 200);
  assert.match(await r.text(), /"to":"\/lessons\/a\/\?u=1"/);
  assert.equal((await fetchB('http://biochemistrypedia.com/lessons/a/', { headers: { ...HTTP_NAV, Cookie: 'bp_moved=1' } })).status, 301);
  assert.equal((await fetchB('http://biochemistrypedia.com/lessons/a/', { headers: { ...HTTP_NAV, 'User-Agent': 'Googlebot/2.1' } })).status, 301);
});
await check('every hand-off page: a data: favicon in the head and img-src allowing it (no /favicon.ico request to block)', async () => {
  const pages = [
    await fetchB('https://biochemistrypedia.com/handoff/?to=/x/'),
    await fetchB('https://biochemistrypedia.com/handoff/signin/'),
    await fetchB('https://biochemistrypedia.com/handoff/done?to=/x/'),
    await fetchB('https://stemhop.com/handoff/receive', { method: 'POST', headers: { Origin: 'https://evil.example' }, body: multipart({ data: '{}', to: '/' }) }),
  ];
  for (const r of pages) {
    const html = await r.text();
    assert.match(html, /<head>[\s\S]*<link rel="icon" href="data:,">[\s\S]*<\/head>/);
    assert.match(r.headers.get('Content-Security-Policy'), /img-src 'self' data:(;|$)/);
    assert.ok(r.headers.get('Content-Security-Policy').includes(`'sha256-${b64sha(scriptOf(html))}'`), 'hash still matches');
  }
});
let code;
await check('bridge/issue on the old host gives a code to a signed-in learner, through fetch', async () => {
  const r = await fetchB('https://biochemistrypedia.com/api/learner/bridge/issue', { method: 'POST', headers: { Origin: 'https://biochemistrypedia.com', 'Content-Type': 'application/json', Cookie: `bp_learner=${token}` }, body: '{}' });
  assert.equal(r.status, 200);
  code = (await r.json()).code;
  assert.match(code, /^[0-9a-f]{64}$/);
  const anon = await fetchB('https://biochemistrypedia.com/api/learner/bridge/issue', { method: 'POST', headers: { Origin: 'https://biochemistrypedia.com', 'Content-Type': 'application/json' }, body: '{}' });
  assert.equal(anon.status, 401);
  // In phase A there is no bridge.
  const a = await settle(await WA.fetch(req('https://biochemistrypedia.com/api/learner/bridge/issue', { method: 'POST', headers: { Origin: 'https://biochemistrypedia.com', 'Content-Type': 'application/json', Cookie: `bp_learner=${token}` }, body: '{}' }), { ASSETS, CLASSES: db }));
  assert.equal(a.status, 404);
});
const store = { 'biochempedia:progress:v1': JSON.stringify({ v: 1, lessons: { a: { v: 100, d: 200 } }, items: {} }), 'bp-cer:/lessons/a/:x': '{"t":"</script><b>"}', 'bp-supports': '2', 'someone-else': 'x' };
const post = (origin, fields) => fetchB('https://stemhop.com/handoff/receive', { method: 'POST', headers: { Origin: origin }, body: multipart(fields) });
let receivedHtml;
await check('receive (multipart) from the https old host: session carried, data embedded safely, CSP hash matches', async () => {
  const r = await post('https://biochemistrypedia.com', { data: JSON.stringify({ v: 1, items: store }), to: '/lessons/a/#sec', signin: code });
  assert.equal(r.status, 200);
  const cookies = r.headers.getSetCookie();
  assert.ok(cookies.some((c) => /^bp_learner=[0-9a-f]{64};.*HttpOnly.*Secure/.test(c)), 'a session on the new host');
  receivedHtml = await r.text();
  assert.ok(!receivedHtml.includes('</script><b>'), 'saved text cannot close the script');
  assert.ok(r.headers.get('Content-Security-Policy').includes(`'sha256-${b64sha(scriptOf(receivedHtml))}'`));
  assert.match(receivedHtml, /"done":"https:\/\/biochemistrypedia\.com\/handoff\/done\?to=%2Flessons%2Fa%2F%23sec"/);
});
await check('receive from the plain-http old origin: data taken, sign-in code ignored', async () => {
  const r2 = await fetchB('https://biochemistrypedia.com/api/learner/bridge/issue', { method: 'POST', headers: { Origin: 'https://biochemistrypedia.com', 'Content-Type': 'application/json', Cookie: `bp_learner=${token}` }, body: '{}' });
  const c2 = (await r2.json()).code;
  const r = await post('http://biochemistrypedia.com', { data: JSON.stringify({ v: 1, items: { 'bp-supports': '1' } }), to: '/', signin: c2 });
  assert.equal(r.status, 200);
  assert.deepEqual(r.headers.getSetCookie(), [], 'no session from an http page');
  assert.match(await r.text(), /bp-supports/);
  // The code was not used up either: it simply expires.
  assert.ok(db.sql.prepare('SELECT 1 FROM learner_challenges WHERE id=?').get(await sha256Hex(c2)));
});
await check('receive refuses posts not from the old host, and oversized ones, without marking anything', async () => {
  for (const o of ['https://evil.example', 'null', '', 'https://stemhop.com']) assert.equal((await post(o, { data: '{"v":1,"items":{}}', to: '/' })).status, 403, o);
  const big = await HO.receive(req('https://stemhop.com/handoff/receive', { method: 'POST', headers: { Origin: 'https://biochemistrypedia.com', 'Content-Length': String(M.MAX_BYTES + 1) }, body: 'x' }), {}, B);
  assert.equal(big.status, 413);
  assert.deepEqual(big.headers.getSetCookie(), []);
  assert.match(await big.text(), /https:\/\/biochemistrypedia\.com\/handoff\/\?to=/, 'offers to try again');
});
await check('the receive page writes, then marks moved only through /handoff/done; a failed merge leaves it unmarked', async () => {
  const mergeVia = async (u, o) => fetchB('https://stemhop.com' + u, { method: 'POST', headers: { Origin: 'https://stemhop.com', 'Content-Type': 'application/json' }, body: o.body });
  // Nothing on the new host yet: everything copied, then off to /handoff/done.
  let p = await runPage(receivedHtml, { origin: 'https://stemhop.com', fetchImpl: mergeVia });
  assert.equal(p.replaced, 'https://biochemistrypedia.com/handoff/done?to=%2Flessons%2Fa%2F%23sec');
  assert.equal(p.store['bp-supports'], '2'); assert.ok(!('someone-else' in p.store));
  // Keys on both sides go through /handoff/merge; the new host's newer progress survives.
  const newer = JSON.stringify({ v: 1, lessons: { a: { v: 50, d: 900 } }, items: {} });
  p = await runPage(receivedHtml, { origin: 'https://stemhop.com', store: { 'biochempedia:progress:v1': newer, 'bp-supports': '1' }, fetchImpl: mergeVia });
  assert.deepEqual(p.fetched, ['/handoff/merge']);
  assert.deepEqual(JSON.parse(p.store['biochempedia:progress:v1']).lessons.a, { v: 50, d: 900 });
  assert.equal(p.store['bp-supports'], '1', 'a plain key the new host has is kept');
  assert.match(p.replaced, /\/handoff\/done\?/);
  // The merge fails (a 5xx, a CPU limit): no /handoff/done, so the next old link offers it again.
  p = await runPage(receivedHtml, { origin: 'https://stemhop.com', store: { 'biochempedia:progress:v1': newer }, fetchImpl: async () => new Response('', { status: 503 }) });
  assert.equal(p.replaced, '/lessons/a/#sec');
  assert.ok(!go('https://biochemistrypedia.com/lessons/a/', B, { headers: NAV }).status, 'still the hand-off next time');
});
await check('if /handoff/receive itself fails: a page with the way on, the work still on the old address, nothing marked', async () => {
  const brokenDb = { prepare() { throw new Error('D1 down'); } };
  const W = createWorker(B);
  const errors = []; const orig = console.error; console.error = (...a) => errors.push(a.join(' '));
  let r;
  try {
    r = await W.fetch(req('https://stemhop.com/handoff/receive?to=' + encodeURIComponent('/lessons/a/#s2'), { method: 'POST', headers: { Origin: 'https://biochemistrypedia.com' }, body: multipart({ data: '{"v":1,"items":{}}', to: '/lessons/a/#s2', signin: 'c'.repeat(64) }) }), { ASSETS, CLASSES: brokenDb });
  } finally { console.error = orig; }
  assert.equal(r.status, 500);
  assert.deepEqual(r.headers.getSetCookie(), []);
  const html = await r.text();
  assert.match(html, /href="\/lessons\/a\/#s2">Continue to the page you asked for/);
  assert.match(html, /still saved in this browser at the old address, and it will be offered again/);
  assert.match(html, /href="https:\/\/biochemistrypedia\.com\/handoff\/\?to=%2Flessons%2Fa%2F%23s2"/);
  assert.ok(errors.some((e) => e.includes('handoff receive error')), 'logged');
  // An unreadable form: the page asked for still comes from the query string.
  const bad = await fetchB('https://stemhop.com/handoff/receive?to=%2Fnotebook%2F', { method: 'POST', headers: { Origin: 'https://biochemistrypedia.com', 'Content-Type': 'multipart/form-data; boundary=x' }, body: 'not multipart' });
  assert.equal(bad.status, 400);
  assert.match(await bad.text(), /href="\/notebook\/">Continue to the page you asked for/);
});
await check('the hand-off page posts with the page asked for in the query too; the retry line after a failed try is accurate', async () => {
  const html = await (await fetchB('https://biochemistrypedia.com/lessons/a/?u=1', { headers: NAV })).text();
  let p = await runPage(html, { origin: 'https://biochemistrypedia.com', store: { 'bp-supports': '1' } });
  assert.equal(p.els.f.action, 'https://stemhop.com/handoff/receive?to=%2Flessons%2Fa%2F%3Fu%3D1');
  p = await runPage(html, { origin: 'https://biochemistrypedia.com', store: { 'bp-supports': '1', 'biochempedia:handoff:tries': '1' } });
  assert.match(p.els.msg.textContent, /may not all have come across/);
  assert.match(p.els.msg.textContent, /Trying again is safe/);
});
await check('/handoff/done on the old host sets the moved cookie and forwards', async () => {
  const r = await fetchB('https://biochemistrypedia.com/handoff/done?to=%2Flessons%2Fa%2F');
  assert.match(r.headers.get('Set-Cookie'), /^bp_moved=1; Path=\/; Max-Age=31536000; SameSite=Lax; Secure$/);
  const p = await runPage(await r.text(), { origin: 'https://biochemistrypedia.com', store: { 'biochempedia:handoff:tries': '2' } });
  assert.equal(p.replaced, 'https://stemhop.com/lessons/a/');
  assert.ok(!('biochempedia:handoff:tries' in p.store));
  assert.equal((await fetchB('https://biochemistrypedia.com/lessons/a/', { headers: { ...NAV, Cookie: 'bp_moved=1' } })).status, 301);
});
await check('/handoff/merge through fetch: same-origin JSON only', async () => {
  const bad = await fetchB('https://stemhop.com/handoff/merge', { method: 'POST', headers: { Origin: 'https://evil.example', 'Content-Type': 'application/json' }, body: '{}' });
  assert.equal(bad.status, 403);
  const ok = await fetchB('https://stemhop.com/handoff/merge', { method: 'POST', headers: { Origin: 'https://stemhop.com', 'Content-Type': 'application/json' }, body: JSON.stringify({ current: {}, incoming: { 'bp-supports': '1' } }) });
  assert.deepEqual(await ok.json(), { write: { 'bp-supports': '1' } });
});
await check('a large store (the whole 5 MiB browser quota) is received in one pass', async () => {
  const items = {}; for (let i = 0; i < 50; i++) items['bp-cer:/lessons/x/:' + i] = 'y'.repeat(100_000) + '"<';
  const data = JSON.stringify({ v: 1, items });
  assert.ok(data.length > 5_000_000 && data.length < M.MAX_STORE_CHARS);
  const t0 = performance.now();
  const r = await post('https://biochemistrypedia.com', { data, to: '/' });
  const ms = performance.now() - t0;
  assert.equal(r.status, 200);
  const html = await r.text();
  assert.ok(html.length > data.length && !/"<"/.test(html));
  console.log(`      (${(data.length / 1e6).toFixed(1)} M characters received in ${ms.toFixed(0)} ms of Node time)`);
});
await check('the passkey sign-in and sign-up page on the old host: CSP, and both ceremonies on the old origin', async () => {
  const r = await fetchB('https://biochemistrypedia.com/handoff/signin/?to=/account/&name=Sam');
  const html = await r.text();
  assert.ok(r.headers.get('Content-Security-Policy').includes(`'sha256-${b64sha(scriptOf(html))}'`));
  assert.match(html, /value="Sam"/);
  assert.match(scriptOf(html), /navigator\.credentials\.get/); assert.match(scriptOf(html), /navigator\.credentials\.create/);
  assert.match(scriptOf(html), /\/handoff\/\?to=/);
});
await check('/account/ on the new host gets the passkey note in phase B only', async () => {
  const b = await (await fetchB('https://stemhop.com/account/')).text();
  assert.ok(b.includes('relatedOrigins') && b.includes('https://biochemistrypedia.com/handoff/signin/'));
  assert.ok(b.includes('[data-pk-new]') && b.includes('[data-add-pk]'), 'registration and add-passkey are intercepted');
  const a = await (await settle(await WA.fetch(req('https://biochemistrypedia.com/account/'), { ASSETS, CLASSES: db }))).text();
  assert.ok(!a.includes('relatedOrigins'));
  const other = await (await fetchB('https://stemhop.com/lessons/a/')).text();
  assert.ok(!other.includes('relatedOrigins'));
});
await check('/.well-known/webauthn through fetch', async () => {
  const r = await fetchB('https://biochemistrypedia.com/.well-known/webauthn');
  assert.equal(r.headers.get('Content-Type'), 'application/json');
  assert.deepEqual(await r.json(), { origins: ['https://stemhop.com', 'https://www.stemhop.com'] });
});

console.log('the sign-in code');
await check('single use, also under concurrency; ordinary login rows and expired codes refused', async () => {
  const c = await L.issueBridge(db, 'L1');
  const rq = new Request('https://stemhop.com/');
  const both = await Promise.all([L.redeemBridge(db, rq, c), L.redeemBridge(db, rq, c), L.redeemBridge(db, rq, c)]);
  assert.equal(both.filter((x) => x.length).length, 1, 'exactly one redeem wins');
  assert.deepEqual(await L.redeemBridge(db, rq, c), []);
  const raw = 'a'.repeat(64);
  db.sql.prepare('INSERT INTO learner_challenges (id, purpose, challenge, learner_id, display_name, extra, created_at, expires_at) VALUES (?,?,?,?,?,?,?,?)')
    .run(await sha256Hex(raw), 'login', 'ordinary-challenge', 'L1', null, null, now, now + 60_000);
  assert.deepEqual(await L.redeemBridge(db, rq, raw), []);
  assert.ok(db.sql.prepare('SELECT 1 FROM learner_challenges WHERE id=?').get(await sha256Hex(raw)), 'an ordinary login row is left alone');
  const old = await L.issueBridge(db, 'L1');
  db.sql.prepare("UPDATE learner_challenges SET expires_at=0 WHERE challenge LIKE 'bridge:%'").run();
  assert.deepEqual(await L.redeemBridge(db, rq, old), []);
  assert.deepEqual(await L.redeemBridge(db, rq, 'not-a-code'), []);
});

console.log('fail open');
await check('an exception: GET/HEAD outside the API falls back to the static assets; the API and POSTs do not', async () => {
  const broken = { get known() { throw new Error('boom'); }, primary: 'x', legacy: 'x', rpId: 'x' };
  const W = createWorker(broken);
  const errors = []; const orig = console.error; console.error = (...a) => errors.push(a.join(' '));
  try {
    const r = await W.fetch(req('https://biochemistrypedia.com/lessons/a/'), { ASSETS });
    assert.equal(r.headers.get('X-From'), 'assets');
    assert.equal((await W.fetch(req('https://biochemistrypedia.com/explainers/a/x.mp4', { method: 'HEAD' }), { ASSETS })).headers.get('X-From'), 'assets');
    await assert.rejects(W.fetch(req('https://biochemistrypedia.com/api/learner/me'), { ASSETS }));
    await assert.rejects(W.fetch(req('https://biochemistrypedia.com/x/', { method: 'POST', body: 'a' }), { ASSETS }));
    assert.ok(errors.length >= 1 && errors[0].includes('worker error'), 'logged');
  } finally { console.error = orig; }
});
await check('the production worker: primary pages are the static asset response, untouched; others redirect', async () => {
  const seen = [];
  const sentinel = new Response('PAGE', { headers: { 'X-From': 'assets' } });
  const env = { ASSETS: { fetch: async (r) => { seen.push(new URL(r.url).pathname); return sentinel; } } };
  assert.equal(await worker.fetch(req(`https://${S.PRIMARY_HOST}/lessons/action-potential/`, { headers: NAV }), env), sentinel);
  assert.equal(await worker.fetch(req(`https://${S.PRIMARY_HOST}/explainers/a/x.vtt`, { method: 'POST' }), env), sentinel);
  const other = S.KNOWN_HOSTS.find((h) => !H.inFamily(h, H.switched() ? S.PRIMARY_HOST : S.LEGACY_HOST));
  const r2 = await worker.fetch(req(`https://${other}/api/learner/me?a=1`), env);
  assert.ok([301, 302].includes(r2.status));
  assert.equal(r2.headers.get('Location'), `https://${S.PRIMARY_HOST}/api/learner/me?a=1`);
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
await check('probes, the account cache, the hand-off counter and other sites\' keys are not carried', () => {
  const w = M.mergeStorage({}, { 'biochempedia:probe': '1', 'biochempedia:learner:v1': '{}', 'biochempedia:progress:v1:test': '1', 'other:key': 'x', 'biochempedia:notebook:v1:probe': '1', 'biochempedia:handoff:tries': '1' }).write;
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
        for (const m of t.matchAll(/['"`]((?:(?:biochempedia|bcp|bp)[-:]|stemhop:)[A-Za-z0-9:_\-]*)/g)) found.add(m[1]);
      }
    }
  };
  walk(new URL('../src/', import.meta.url).pathname);
  // Literals that are event names, CSS classes or sessionStorage only, not localStorage keys.
  const notKeys = /^bp-(cards-open|class|films|learner|mycards|notebook|progress|reading|section|hl|lp|listen)\b|^biochempedia:(cards-prompt|films:budget|handoff)|^biochempedia-/;
  // Keys under the new "stemhop:" prefix were first written on stemhop.com itself, so there is nothing
  // on the old domain to carry: the site-wide preferences (role, level, how long a lesson to open) and
  // the old per-lesson Side Hops view, now read only as a fallback. Listing them here keeps the scan
  // honest: a new "stemhop:" key fails this check until someone decides whether the hand-off carries it.
  const stemhopOnly = /^stemhop:(prefs:v1|side-hops:view:|prefs)$/;
  const keys = [...found].filter((k) => !notKeys.test(k) && !stemhopOnly.test(k));
  assert.ok([...found].some((k) => k === 'stemhop:prefs:v1'), 'the scan sees stemhop: keys');
  assert.ok(keys.length >= 15, 'found the keys: ' + keys.join(' '));
  for (const k of keys) {
    const sample = k.endsWith(':') ? k + 'x' : k;
    assert.ok(M.HANDOFF_KEY.test(sample), `${k} is not carried by the hand-off: add its prefix to HANDOFF_KEY`);
  }
});

console.log(`\n${n} checks passed.`);
