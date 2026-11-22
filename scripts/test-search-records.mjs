#!/usr/bin/env node
/**
 * Checks the typed search records and the index builder without a site build:
 *  - runsFromVtt cuts captions into short timed runs and keeps a phrase split across two cues together
 *  - recordHtml writes the type filter, the meta and the time anchors, and refuses a bad record
 *  - readPagefindYml reads the real pagefind.yml (the settings the CLI used to read itself)
 *  - a tiny real Pagefind index built the way scripts/build-search-index.mjs builds it answers:
 *    a word only in a film's narration finds the film and the run that says it (anchor t-<second>),
 *    the type filter keeps lessons and films apart, a quoted phrase works, and a word in the title
 *    outranks the same word in another record's narration.
 *   node scripts/test-search-records.mjs
 */
import { readFile, rm, mkdtemp } from 'node:fs/promises';
import { tmpdir } from 'node:os';
import { join, resolve } from 'node:path';
import { fileURLToPath, pathToFileURL } from 'node:url';
import * as pagefind from 'pagefind';
import { runsFromVtt, recordHtml, clozeText, filmAt, secondsOfId, RUN_MAX } from '../src/lib/search-records.mjs';
import { readPagefindYml } from './build-search-index.mjs';

let failed = 0;
const ok = (cond, msg) => { if (cond) console.log(`  ok    ${msg}`); else { failed++; console.log(`  FAIL  ${msg}`); } };

console.log('\nCaptions to timed runs');
const vtt = `WEBVTT

1
00:00:01.000 --> 00:00:04.000
The squid giant axon is as wide

2
00:00:04.000 --> 00:00:07.500
as a pencil lead. That is why Hodgkin and Huxley could thread a wire inside it.

3
00:01:15.200 --> 00:01:19.000
Tetrodotoxin &amp; saxitoxin <i>block</i> the sodium channel.
`;
const runs = runsFromVtt(vtt);
ok(runs.length === 2, `two runs (got ${runs.length})`);
ok(runs[0].start === 1 && runs[0].text.includes('as wide as a pencil lead'), 'a phrase split across two cues stays in one run');
ok(Math.floor(runs[1].start) === 75 && runs[1].text === 'Tetrodotoxin & saxitoxin block the sodium channel.', 'tags and entities are removed, the start second kept');
const long = `WEBVTT\n\n${Array.from({ length: 30 }, (_, i) => `00:00:${String(i).padStart(2, '0')}.000 --> 00:00:${String(i).padStart(2, '0')}.900\nword after word after word without any stop`).join('\n\n')}\n`;
ok(runsFromVtt(long).every((r) => r.text.length <= RUN_MAX + 60), 'a run without a full stop is still cut near RUN_MAX');

console.log('\nRecords as HTML');
const film = {
  type: 'film', url: '/watch/action-potential/', title: 'Three gates make one spike', lead: 'The Action Potential',
  kicker: 'First film', courses: ['neuro-core'], courseTitle: 'Neuroscience', level: 'college-core', levelTitle: 'College: the core',
  lesson: 'The Action Potential', poster: '/explainers/action-potential/poster.jpg', dur: 215, filmKey: 'action-potential/explainer',
  parts: [{ id: 't-1', h: '0:01', text: runs[0].text }, { id: 't-75', h: '1:15', text: runs[1].text }],
};
const html = recordHtml(film);
ok(html.includes('data-pagefind-filter="type">film<'), 'type filter');
ok(html.includes('data-pagefind-filter="course">neuro-core<'), 'course filter');
ok(html.includes('<h3 id="t-75">1:15</h3>'), 'time anchor heading');
ok(html.includes('data-pagefind-meta="filmKey">action-potential/explainer<'), 'film key meta');
const lad = recordHtml({ type: 'ladder', url: '/films/?ladder=osmosis', title: 'Osmosis', films: 4, parts: [{ id: 'films', h: 'Films on this ladder', text: 'Why cells swell · Water follows salt' }] });
ok(lad.includes('data-pagefind-filter="type">ladder<') && lad.includes('data-pagefind-meta="films">4<'), 'a ladder record carries its type and how many films it plays');
let threw = false;
try { recordHtml({ ...film, type: 'lesson' }); } catch { threw = true; }
ok(threw, 'a record may not claim to be a lesson (lessons are pages)');
threw = false;
try { recordHtml({ ...film, url: 'watch/x' }); } catch { threw = true; }
ok(threw, 'a record needs a site-relative url');
ok(clozeText('peak of about {{c1::+40 mV}} and {{c2::zero::a number}}') === 'peak of about +40 mV and zero', 'cloze cards read as plain text');
ok(filmAt('/watch/a/?pagefind-highlight=x', 'a/explainer', 75) === '/watch/a/?pagefind-highlight=x&film=a%2Fexplainer&at=75', 'time link on a URL with a query');
ok(filmAt('/watch/a/', 'a/explainer', 75) === '/watch/a/?film=a%2Fexplainer&at=75', 'time link on a plain URL');
ok(secondsOfId('t-75') === 75 && secondsOfId('take-homes') === null, 'anchor ids back to seconds');

console.log('\npagefind.yml');
const cfg = readPagefindYml(await readFile(resolve('pagefind.yml'), 'utf8'));
ok(cfg.excludeSelectors.includes('.design-answer') && cfg.excludeSelectors.some((s) => s.startsWith('details:not')), `exclude_selectors read (${cfg.excludeSelectors.length})`);

console.log('\nA real index, built as the build script builds it');
const dir = await mkdtemp(join(tmpdir(), 'search-records-'));
const out = join(dir, 'pagefind');
const { index } = await pagefind.createIndex(cfg);
await index.addHTMLFile({ url: '/lessons/action-potential/', content: '<html lang="en"><body><div data-pagefind-body><span hidden data-pagefind-filter="type:lesson"></span><h1>The Action Potential</h1><p>Sodium rushes in at threshold.</p></div></body></html>' });
await index.addHTMLFile({ url: film.url, content: recordHtml(film) });
await index.addHTMLFile({ url: '/watch/tetrodotoxin/', content: recordHtml({ type: 'film', url: '/watch/tetrodotoxin/', title: 'Tetrodotoxin and the pufferfish', parts: [{ text: 'A fish that carries a poison.' }] }) });
await index.addHTMLFile({ url: '/lessons/action-potential/#sh-1', content: recordHtml({ type: 'sidehop', url: '/lessons/action-potential/#sh-1', title: 'Why Sichuan peppercorns buzz', parts: [{ text: 'Hydroxy-alpha-sanshool blocks potassium channels.' }] }) });
await index.writeFiles({ outputPath: out });
await pagefind.close();

globalThis.fetch = async (u) => {
  const s = String(u);
  return new Response(await readFile(s.startsWith('file:') ? fileURLToPath(s) : s), { status: 200, headers: s.endsWith('.wasm') ? { 'content-type': 'application/wasm' } : {} });
};
const pf = await import(pathToFileURL(join(out, 'pagefind.js')).href);
await pf.options({ basePath: pathToFileURL(out + '/').href, baseUrl: '/' });
const find = async (q, filters = {}) => Promise.all((await pf.search(q, { filters })).results.map((r) => r.data()));

const pencil = await find('pencil', { type: 'film' });
ok(pencil.length === 1 && pencil[0].meta.title === 'Three gates make one spike', 'a word only in the narration finds the film');
const sub = pencil[0]?.sub_results.find((s) => /<mark>/.test(s.excerpt));
ok(sub?.anchor?.id === 't-1' && /pencil/.test(sub.excerpt), 'and the run that says it, with its time anchor');
ok((await find('pencil', { type: 'lesson' })).length === 0, 'the lesson filter leaves films out');
ok((await find('sodium', { type: 'lesson' })).length === 1, 'the lesson filter keeps lessons');
ok((await find('sanshool', { type: { any: ['sidehop', 'film'] } })).length === 1, 'several types at once');
ok((await find('"sodium channel"', { type: 'film' })).length === 1 && (await find('"channel sodium"', { type: 'film' })).length === 0, 'a quoted phrase must be in that order');
const ttx = await find('tetrodotoxin', { type: 'film' });
ok(ttx[0]?.meta.title === 'Tetrodotoxin and the pufferfish', 'a word in a title outranks the same word in another film\'s narration');

await rm(dir, { recursive: true, force: true });
console.log(failed ? `\n${failed} check(s) failed` : '\nAll checks passed');
process.exit(failed ? 1 : 0);
