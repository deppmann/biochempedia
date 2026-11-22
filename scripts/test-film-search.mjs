#!/usr/bin/env node
/* Tests for film search (src/lib/film-search.mjs), 2026-11-22.

   Two parts:
   1. Rules, on a small made-up list: kind and level words are filters, plurals and small typos are
      forgiven, every word must be found, films with all but one word come after and are counted apart.
   2. The real library, read from the BUILT site (dist/films/list.json and dist/films/search.json, so
      run `npm run build` first): the queries Chris and a sweep of likely searches tried on 2026-11-22,
      when "neuroscience methods" on /films/ found nothing. Each must keep finding what it found then.

   Run: node scripts/test-film-search.mjs [--verbose]   (in `npm test` and in CI) */
import { existsSync, readFileSync } from 'node:fs';
import { parseQuery, prepare, searchFilms, stem, quality } from '../src/lib/film-search.mjs';
import { matchFilms, runQueue } from '../src/lib/film-logic.mjs';

const verbose = process.argv.includes('--verbose');
let failed = 0;
let passed = 0;
const ok = (cond, name, detail = '') => { if (cond) passed++; else { failed++; console.error(`✗ ${name}${detail ? `: ${detail}` : ''}`); } };
const eq = (a, b, name) => ok(JSON.stringify(a) === JSON.stringify(b), name, `got ${JSON.stringify(a)}, wanted ${JSON.stringify(b)}`);

/* ---- 1. rules */
eq(parseQuery('neuroscience methods'), { words: ['neuroscience'], kind: 'method', levels: [], dropped: ['methods'] }, '"methods" is a kind filter, not a word');
eq(parseQuery('physiology films').words, ['physiology'], '"films" asks for films: dropped');
eq(parseQuery('krebs cycle video').words, ['krebs', 'cycle'], '"video" is dropped');
eq(parseQuery('second chapter photosynthesis'), { words: ['photosynthesis'], kind: 'second', levels: [], dropped: ['second', 'chapter'] }, '"second chapter" is a kind');
eq(parseQuery('osmosis high school').levels, ['high-school'], '"high school" is a level');
eq(parseQuery('how do cells divide').words, ['cells', 'divide'], 'little words are dropped');
eq(stem('synapses'), 'synapse', 'plural: synapses');
eq(stem('activities'), 'activity', 'plural: activities');
eq(stem('glucose'), 'glucose', 'not a plural: glucose');
ok(quality('mitochondira', 'mitochondria') > 0, 'a swapped pair of letters is forgiven');
ok(quality('glycolysis', 'glycolsis') > 0, 'a dropped letter is forgiven');
eq(quality('atp', 'adaptation'), 0, '"atp" is not found in "adaptation"');
eq(quality('cell', 'cello'), 0.75, 'a word can start a longer word');
{
  const F = (i, t, l, s, c, k, extra = {}) => ({ i, t, l, s, c, k, b: k, d: 180, h: k === 'method' ? `/methods/m${i}/` : `/watch/x${i}/`, f: `x${i}/explainer`, ...extra });
  const list = {
    courses: { neuro: 'Neuroscience', cell: 'Cell Biology', bio: 'High School Biology' },
    levels: { 'high-school': 'High school', 'college-core': 'College: the core' },
    films: [
      F(0, 'Downhill for Free', 'Crossing the Membrane', 'high-school', 'bio', 'first'),
      F(1, 'The Spike and Its Puzzles', 'Action Potential', 'college-core', 'neuro', 'first'),
      F(2, 'Holding the Voltage Still', 'Action Potential', 'college-core', 'neuro', 'second'),
      F(3, 'One Neuron in Separate Chambers', undefined, '', '', 'method'),
      F(4, 'One Protein Out of Thousands', undefined, '', '', 'method'),
      F(5, 'Water Drifts to the Saltier Side', 'Diffusion and Osmosis', 'high-school', 'bio', 'second'),
    ],
  };
  const data = {
    v: 1,
    fields: { neuroscience: 'neuroscience neuro', 'cell-biology': 'cell biology', biology: 'biology' },
    lessons: [{ fd: 'biology:1', i: 'osmosis' }, { fd: 'neuroscience:1', i: 'spike' }, { fd: 'biology:1', i: 'osmosis water' }],
    films: {
      'x0/explainer': { L: 0 }, 'x1/explainer': { L: 1 }, 'x2/explainer': { L: 1, tr: 'clamp hodgkin' }, 'x5/explainer': { L: 2 },
      'x3/explainer': { m: 'Compartmented (Campenot) culture Campenot chamber', fd: 'neuroscience:0.9 cell-biology:0.6' },
      'x4/explainer': { m: 'Western blot immunoblot', fd: 'cell-biology:0.8' },
    },
  };
  const idx = prepare(list, data);
  const ids = (q, o) => searchFilms(idx, q, o).films.map((f) => f.i);
  eq(ids('neuroscience methods'), [3], 'field + kind: the neuroscience method film only');
  eq(ids('cell biology methods'), [4, 3], 'two-word field + kind: best field first');
  eq(ids('campenot'), [3], 'a method film by its method name');
  eq(ids('western blots'), [4], 'a plural finds the method');
  eq(ids('acton potential'), [1, 2], 'a typo in a lesson word');
  eq(ids('osmosis high school'), [5, 0], 'level words filter; the title match first');
  eq(ids('second chapter action potential'), [2], 'a kind phrase filters');
  eq(ids('hodgkin'), [2], 'a transcript word finds its film');
  const r = searchFilms(idx, 'spike chambers');
  eq([r.full, r.films.map((f) => f.i)], [0, [1, 3, 2]], 'no film has both words: the partial matches, counted as partial');
  const sm = searchFilms(idx, 'scientific methods');
  eq([sm.full, sm.kind], [0, ''], 'a kind word that leaves nothing is read as a plain word again: no film has both words');
  const view = (o = {}) => ({ q: '', sort: 'course', level: '', course: '', kind: '', ...o });
  eq(matchFilms(list.films, view({ q: 'neuroscience methods' }), data, list).map((f) => f.i), [3], 'the library\'s matcher uses the same search');
  eq(runQueue(list.films, view({ q: 'neuroscience methods' }), data, list).map((f) => f.i), [3], 'and a run of it plays method films');
  eq(matchFilms(list.films, view({ q: 'action potential', sort: 'long' }), data, list).full, 2, 'the full count is carried with the list');
}

/* ---- 2. the real library (needs a build) */
const LIST = 'dist/films/list.json';
const DATA = 'dist/films/search.json';
if (!existsSync(LIST) || !existsSync(DATA)) {
  console.error(`✗ test-film-search: ${LIST} or ${DATA} is missing. Run \`npm run build\` first.`);
  process.exit(1);
}
const list = JSON.parse(readFileSync(LIST, 'utf8'));
const data = JSON.parse(readFileSync(DATA, 'utf8'));
const index = prepare(list, data);
const byPage = (h) => list.films.find((f) => f.h === h);
const find = (q) => searchFilms(index, q);
const pages = (r, n = r.films.length) => r.films.slice(0, n).map((f) => f.h);

/** Each query: what must be in its first `top` results (by film page or title), and at least how many full matches. */
const CASES = [
  // Chris, 2026-11-22: "I searched neuroscience methods in the film page and it didn't pull anything up."
  { q: 'neuroscience methods', min: 15, top: 40, has: ['/methods/compartmented-culture/', '/methods/nerve-injury-and-axotomy/', '/methods/patch-clamp/', '/methods/optogenetics/', '/methods/calcium-imaging/', '/methods/brain-slice-electrophysiology/'], allMethods: true },
  { q: 'action potential', min: 5, top: 5, has: ['/watch/action-potential/'] },
  { q: 'western blot', min: 1, top: 1, has: ['/methods/western-blot/'] },
  { q: 'patch clamp', min: 1, top: 3, has: ['/methods/patch-clamp/'] },
  { q: 'axon guidance', min: 3, top: 10, has: ['/methods/axon-guidance-assays/'] },
  { q: 'glycolysis', min: 3, top: 10, hasTitle: /glycoly/i },
  { q: 'physiology films', min: 30 },
  { q: 'cell biology methods', min: 10, allMethods: true },
  { q: 'compartmented culture', min: 1, top: 1, has: ['/methods/compartmented-culture/'] },
  { q: 'campenot', min: 1, top: 3, has: ['/methods/compartmented-culture/'] },
  { q: 'optogenetics', min: 1, top: 1, has: ['/methods/optogenetics/'] },
  { q: 'mitochondira', min: 3 },
  { q: 'synapses', min: 10 },
  { q: 'calcium imaging', min: 1, top: 1, has: ['/methods/calcium-imaging/'] },
  { q: 'nerve injury', min: 1, top: 3, has: ['/methods/nerve-injury-and-axotomy/'] },
  { q: 'krebs cycle video', min: 1 },
  { q: 'osmosis high school', min: 1, level: 'high-school' },
  { q: 'second chapter photosynthesis', min: 1, kinds: ['second', 'series'] },
  { q: 'hodgkin', min: 2 },
  { q: 'crispr', min: 2 },
  { q: 'meiosis', min: 3 },
  { q: 'gel electrophoresis', min: 1 },
  { q: 'retrograde signaling', min: 3 },
  { q: 'methods', min: 90, allMethods: true },
];
for (const c of CASES) {
  const r = find(c.q);
  const name = `"${c.q}"`;
  ok(r.full >= c.min, `${name} finds at least ${c.min} films with every word`, `found ${r.full}`);
  const top = pages(r, c.top ?? r.full);
  for (const h of c.has ?? []) ok(top.includes(h), `${name} has ${h} in its first ${c.top}`, `first: ${top.slice(0, 8).join(' ')}`);
  if (c.hasTitle) ok(r.films.slice(0, c.top).some((f) => c.hasTitle.test(f.t)), `${name} has a title matching ${c.hasTitle}`);
  if (c.allMethods) ok(r.films.slice(0, r.full).every((f) => f.k === 'method' || data.films[f.f]?.m), `${name} lists method films only`);
  if (c.level) ok(r.films.every((f) => f.s === c.level), `${name} stays at ${c.level}`);
  if (c.kinds) ok(r.films.every((f) => c.kinds.includes(f.k)), `${name} lists ${c.kinds.join(' or ')} films only`);
  if (verbose) console.log(`${String(r.full).padStart(4)} (+${r.films.length - r.full}) ${c.q.padEnd(30)} ${r.films.slice(0, 4).map((f) => f.t).join(' | ')}`);
}
{
  // The methods neuroscience lessons lean on, including the ones the long-distance and reverse signaling lessons cite.
  const r = find('neuroscience methods');
  const methodFor = (f) => data.films[f.f]?.m ?? '';
  ok(r.films.some((f) => /compartment/i.test(methodFor(f))), '"neuroscience methods" includes compartmented culture');
  ok(r.films.some((f) => /axotomy|nerve injury/i.test(methodFor(f))), '"neuroscience methods" includes nerve injury and axotomy');
  ok(!r.films.some((f) => /^\/methods\/(gwas|phylogenetic-inference|mark-recapture-and-abundance)\//.test(f.h)), '"neuroscience methods" leaves out field ecology and genome-scan methods');
  const run = runQueue(list.films, { q: 'neuroscience methods', sort: 'course', level: '', course: '', kind: '' }, data, list);
  ok(run.length === r.full, '"Play these results" for "neuroscience methods" plays every film found', `${run.length} of ${r.full}`);
}
ok(!!byPage('/methods/compartmented-culture/'), 'the compartmented culture film is in the list');

if (failed) { console.error(`✗ test-film-search: ${failed} failed, ${passed} passed`); process.exit(1); }
console.log(`✓ test-film-search: ${passed} checks passed.`);
