#!/usr/bin/env node
/**
 * Checks lesson search against the BUILT site: the real Pagefind index in dist/pagefind and the real
 * ranking code in src/lib/lesson-search.ts, run in Node. Needs `npm run build` first.
 *
 *   node scripts/test-search.mjs            run the checks (exit 1 on any failure)
 *   node scripts/test-search.mjs --verbose  also print the top 3 for every query
 *
 * What it covers:
 *  - the owner's example: "health department" puts the lesson with that exact phrase first
 *  - text that exists in only ONE place on a lesson page is found, and is labelled for where it is:
 *    an anecdote, an "Explain at my level" text, a self-test question, a "How we measure it" blurb,
 *    and a film transcript (each probe word was checked to occur in that one place on that one lesson)
 *  - title queries still put the lesson of that name first
 *  - the worked answers folded under "Design problem" are NOT searchable
 *  - odd input (one common word, a stop word, a quoted phrase, a word nobody wrote) does not throw
 *
 * If a probe starts failing after lesson text is edited, the probe word was probably rewritten:
 * pick another word that appears in just one place (see how each is described below).
 */
import { nodeEngine, lib } from './lesson-search-node.mjs';

const verbose = process.argv.includes('--verbose');
const engine = nodeEngine();
let failed = 0;
const fail = (msg) => { failed++; console.log(`  FAIL  ${msg}`); };
const pass = (msg) => console.log(`  ok    ${msg}`);

const run = (q, o = {}) => lib.searchLessons(q, { engine, limit: 8, ...o });
const top = (hits, n = 3) => hits.slice(0, n).map((h) => h.slug).join(', ') || '(none)';

/** @param {string} q @param {(hits: any[]) => string | null} check returns an error text or null */
async function expect(q, check, o) {
  let hits;
  try { hits = await run(q, o); } catch (e) { fail(`"${q}" threw: ${e?.message ?? e}`); return; }
  const err = check(hits);
  if (err) fail(`"${q}" -> ${top(hits)}   (${err})`);
  else pass(`"${q}" -> ${top(hits)}`);
  if (verbose) for (const h of hits.slice(0, 3)) console.log(`          ${h.score.toFixed(2)} ${h.slug}  ${h.spots.map((s) => `[${s.kind}] ${s.label}`).join(' | ')}`);
}

const first = (slug) => (hits) => (hits[0]?.slug === slug ? null : `expected ${slug} first`);
const inTop = (slug, n) => (hits) => (hits.slice(0, n).some((h) => h.slug === slug) ? null : `expected ${slug} in the top ${n}`);

console.log('\nThe owner\'s example');
await expect('health department', first('sleep-or-travel'));
await expect('health department', (h) => (h.length >= 2 && h[0].parts.X > h[1].parts.X ? null : 'the phrase lesson should have the closer words'));

console.log('\nText in one place only: found, and labelled for where it is');
// word, lesson, kind of spot, what the word is in (so a failure can be traced)
const PROBES = [
  ['agnathan', 'adaptive-immunity', 'story', 'a story: "An immune system with no antibodies"'],
  ['lipolytic', 'absorption-and-liver', 'level', 'an "Explain at my level" text'],
  ['insemination', 'animal-development', 'quiz', 'a self-test question'],
  ['synteny', 'animal-body-plans', 'method', 'a "How we measure it" technique blurb'],
  ['burette', 'amino-acids', 'film', 'a film transcript: "pH Sets an Amino Acid\'s Charge"'],
];
for (const [word, slug, kind, where] of PROBES) {
  await expect(word, (hits) => {
    if (hits[0]?.slug !== slug) return `expected ${slug} first (word is in ${where})`;
    const kinds = [...new Set(hits[0].spots.map((s) => s.kind))];
    if (!kinds.includes(kind)) return `expected a ${kind} spot, got ${kinds.join('/') || 'none'}`;
    if (kinds.some((k) => k !== kind)) return `the word is only in ${where}, but spots say ${kinds.join('/')}`;
    const s = hits[0].spots.find((x) => x.kind === kind);
    if (!s.url.includes('#sx-') || !s.url.includes('pagefind-highlight=')) return `spot link should open the region with highlights: ${s.url}`;
    if (!/<mark>/.test(s.excerptHtml) || /<mark>/.test(s.excerptText)) return 'excerpt marks are wrong';
    return null;
  });
}

console.log('\nTitle queries put that lesson first');
await expect('GTPase', first('gtpase-switches'));
await expect('GTPase', inTop('integrins-and-rho-gtpases', 2));
await expect('action potential', inTop('action-potential', 2));
await expect('cell death', first('cell-death'));
await expect('allostery', first('protein-binding-allostery'));
await expect('krebs cycle', first('citric-acid-cycle'));
await expect('Ras', first('ras-to-mapk'));
await expect('insulin signaling', first('pi3k-akt-insulin'));
await expect('ATP synthase', inTop('proton-motive-force', 2));
await expect('western blot', inTop('detecting-a-signal', 3));

console.log('\nCourse scope');
await expect('action potential', (hits) => (hits.length && hits.every((h) => h.course === 'neuroscience') ? null : `all hits should be in neuroscience, got ${[...new Set(hits.map((h) => h.course))].join(',')}`), { scope: 'neuroscience' });

console.log('\nWorked answers stay out of the index');
// Take a six-word run from inside each folded answer ("One way to do it", "What scientists think",
// "Compare with a model answer", "Check your labels") that appears nowhere else on that lesson's page,
// and search for it as an exact phrase: no spot of that lesson may contain it.
{
  const { readdirSync, readFileSync, existsSync } = await import('node:fs');
  const { fileURLToPath } = await import('node:url');
  const dir = fileURLToPath(new URL('../dist/lessons/', import.meta.url));
  const text = (h) => h.replace(/<script[\s\S]*?<\/script>|<style[\s\S]*?<\/style>/g, ' ').replace(/<[^>]+>/g, ' ').replace(/&[a-z#0-9]+;/g, ' ').toLowerCase().split(/[^a-z0-9]+/).filter(Boolean).join(' ');
  const fold = /<details[^>]*>\s*<summary[^>]*>\s*(?:One way to do it|What scientists think|Compare with a model answer|Check your labels)([\s\S]*?)<\/details>/g;
  let tested = 0;
  let leaked = 0;
  for (const slug of readdirSync(dir)) {
    if (tested >= 60) break;
    const f = `${dir}${slug}/index.html`;
    if (!existsSync(f)) continue;
    const html = readFileSync(f, 'utf8');
    const outside = text(html.replace(fold, ' '));
    for (const m of html.matchAll(fold)) {
      const w = text(m[1]).split(' ');
      if (w.length < 30) continue;
      const phrase = w.slice(10, 16).join(' ');
      if (outside.includes(phrase)) continue;
      tested++;
      const hits = await run(`"${phrase}"`, { limit: 5 });
      if (hits.some((h) => h.slug === slug && h.spots.some((sp) => text(sp.excerptText).includes(phrase)))) { leaked++; fail(`a folded answer in ${slug} is searchable: "${phrase}"`); }
      break;
    }
  }
  if (tested < 20) fail(`only ${tested} folded answers could be tested`);
  else if (!leaked) pass(`${tested} folded answers, none searchable`);
}

console.log('\nOdd input');
await expect('the', () => null);
await expect('cell', (h) => (h.length >= 5 ? null : 'a common word should return ranked lessons'));
await expect('the cell of a', () => null);
await expect('"membrane potential"', (h) => (h.length ? null : 'a quoted phrase should match'));
await expect('qzxjvk', (h) => (h.length === 0 ? null : 'a made-up word should match nothing'));
await expect('health departmnt', (h) => (h.length ? null : 'one misspelled word should still offer lessons with the other'));
await expect('a', () => null);
await expect('   ', (h) => (h.length === 0 ? null : 'blank query'));
await expect('C++ (!) [x]', () => null);

console.log(failed ? `\n${failed} check(s) failed.` : '\nAll search checks passed.');
process.exit(failed ? 1 : 0);
