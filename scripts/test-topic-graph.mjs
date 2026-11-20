#!/usr/bin/env node
/**
 * Hop graph tests: the rules (validateGraph), the merge (ingest) and the build-time API
 * (src/lib/topic-graph-core.mjs: conceptsOf, ladder, hops, filmsFor, searchIndex, the browser forms).
 * Every rule has a good case (the committed graph passes) and a bad case (one change breaks exactly
 * that rule). Runs against the real lessons from source; needs no build and calls no model.
 *
 * Run: node scripts/test-topic-graph.mjs   (also in npm test and CI)
 */
import assert from 'node:assert/strict';
import { loadGraphSite, coreSite, readGraph, validateGraph, normalizeGraph, serializeGraph, contentHash, registryOf, LIMITS, addsProblem, blurbProblem, whyProblem, aliasProblem, copyProblems, idProblem } from './topic-graph/lib.mjs';
import { ingest, decomposeGraph, ticketOf } from './topic-graph/ingest.mjs';
import { makeTopicGraph, headingIds, fold, searchConcepts, expandClientGraph } from '../src/lib/topic-graph-core.mjs';
import { buildDigests, digestText } from './topic-graph/digest.mjs';
import { proposePrompt, proposeBatchPrompt, canonicalizePrompt, nearPrompt, assignPrompt, verifyPrompt } from './topic-graph/prompts.mjs';

let passed = 0;
const check = (name, fn) => { try { fn(); passed++; console.log(`  ok  ${name}`); } catch (e) { console.log(`  FAIL ${name}\n${e.stack ?? e}`); process.exitCode = 1; } };
const clone = (x) => JSON.parse(JSON.stringify(x));

const site = await loadGraphSite();
const good = readGraph();
assert.ok(good, 'src/data/topic-graph.json is missing');
const errs = (g) => validateGraph(g, site).errors;
const warns = (g) => validateGraph(g, site).warnings;
/** One change to a copy of the committed graph must produce an error (or warning) matching `re`. */
const breaks = (name, re, edit, list = errs) => check(name, () => {
  const g = clone(good); edit(g);
  const out = list(g);
  assert.ok(out.some((e) => re.test(e)), `expected ${re}, got:\n    ${out.slice(0, 5).join('\n    ') || '(nothing)'}`);
});
// handles used by the bad cases: a concept with several core rungs, a film and a sideways hop
const ID = 'osmosis';
const C = (g) => g.concepts[ID];
assert.ok(good.concepts[ID] && good.concepts.diffusion, 'the tests lean on the osmosis and diffusion concepts');

console.log('the committed graph');
check('passes every rule', () => assert.deepEqual(errs(good), []));
check('is in the one fixed order the tools write', () => assert.equal(serializeGraph(normalizeGraph(good, site)), serializeGraph(good)));
check('every hash is the hash of a lesson\'s teaching text', () => { for (const [s, r] of Object.entries(good.lessons)) assert.match(r.hash, /^[0-9a-f]{16}$/, s); });

console.log('header and areas');
breaks('wrong version', /version/, (g) => { g.version = 2; });
breaks('no date', /updated/, (g) => { g.updated = 'today'; });
breaks('no about', /about/, (g) => { g.about = ''; });
breaks('too few areas', /areas/, (g) => { g.areas = g.areas.slice(0, 5); });
breaks('area id not kebab-case', /area id/, (g) => { g.areas[0].id = 'Cells'; });
breaks('area listed twice', /listed twice/, (g) => { g.areas[1].id = g.areas[0].id; });

console.log('concepts');
breaks('id not kebab-case', /kebab-case/, (g) => { g.concepts.Bad_Id = C(g); });
breaks('missing field', /missing blurb/, (g) => { delete C(g).blurb; });
breaks('unknown subject', /subject/, (g) => { C(g).subject = 'alchemy'; });
breaks('unknown area', /unknown area/, (g) => { C(g).area = 'nowhere'; });
breaks('two concepts with one name', /same name/, (g) => { g.concepts.diffusion.name = C(g).name; });
breaks('blurb too long', /blurb is \d+ words/, (g) => { C(g).blurb = Array(30).fill('water').join(' ') + '.'; });
breaks('blurb of two sentences', /not one sentence/, (g) => { C(g).blurb = 'Water moves. It moves again.'; });
breaks('dash in copy', /dash/, (g) => { C(g).blurb = 'Water moves across a membrane — toward the salt.'; });
breaks('emoji in copy', /emoji/, (g) => { C(g).name = 'Osmosis \u{1F4A7}'; });
breaks('product name in copy', /product, company or test/, (g) => { C(g).blurb = 'Water moves the way Gatorade says it does.'; });
breaks('exam name in copy', /product, company or test/, (g) => { C(g).rungs[0].adds = 'What the MCAT asks about water.'; });
breaks('medical-advice phrasing', /medical-advice/, (g) => { C(g).aliases[0] = 'is it safe to drink salt water'; });

console.log('aliases');
breaks('too many aliases', /aliases \(limit/, (g) => { C(g).aliases = ['a one', 'b two', 'c three', 'd four', 'e five', 'f six']; });
breaks('too few aliases (warning)', /only 1 alias/, (g) => { C(g).aliases = C(g).aliases.slice(0, 1); }, warns);
breaks('alias is another concept\'s name', /is the name of diffusion/, (g) => { C(g).aliases[0] = g.concepts.diffusion.name.toLowerCase(); });
breaks('alias repeats its own name', /own name/, (g) => { C(g).aliases[0] = C(g).name; });
breaks('one phrase on two concepts', /also an alias of/, (g) => { g.concepts.diffusion.aliases[0] = C(g).aliases[0]; });
breaks('alias listed twice', /listed twice/, (g) => { C(g).aliases[1] = C(g).aliases[0]; });

console.log('rungs');
breaks('lesson does not exist', /not a live lesson/, (g) => { C(g).rungs[0].lesson = 'no-such-lesson'; });
breaks('lesson listed twice', /listed twice/, (g) => { C(g).rungs.push(clone(C(g).rungs[0])); });
breaks('unknown role', /role "teaches"/, (g) => { C(g).rungs[0].role = 'teaches'; });
breaks('core rung without a note', /without a note/, (g) => { delete C(g).rungs[0].adds; });
breaks('note too long', /note is \d+ words/, (g) => { C(g).rungs[0].adds = Array(20).fill('salt').join(' ') + '.'; });
breaks('vague note', /vague note/, (g) => { C(g).rungs[0].adds = 'Covers osmosis in more detail.'; });
breaks('analogy formula in a note', /analogy/, (g) => { C(g).rungs[0].adds = 'Osmosis mirrors what a sponge does.'; });
breaks('uses rung with a note', /uses rung carries/, (g) => { const r = C(g).rungs.find((x) => x.role === 'uses'); r.adds = 'A note.'; });
breaks('no core rung', /no core rung/, (g) => { C(g).rungs = C(g).rungs.filter((r) => r.role === 'uses'); C(g).films = []; });
breaks('anchor that is not a section (warning, never a failure)', /falls back to the top/, (g) => { C(g).rungs[0].anchor = 'no-such-section'; }, warns);
check('a broken anchor is not an error', () => { const g = clone(good); C(g).rungs[0].anchor = 'no-such-section'; assert.deepEqual(errs(g), []); });
breaks('more than three core concepts on one lesson (warning)', /is core for 4 concepts/, (g) => {
  const slug = C(g).rungs[0].lesson;
  let n = Object.values(g.concepts).filter((c) => c.rungs.some((r) => r.lesson === slug && r.role === 'core')).length;
  for (const [id, c] of Object.entries(g.concepts)) { if (n >= 4) break; if (!c.rungs.some((r) => r.lesson === slug)) { c.rungs.push({ lesson: slug, role: 'core', adds: 'A stand-in note with one case.' }); g.lessons[slug].concepts.push(id); n++; } }
}, warns);

console.log('films');
breaks('film that does not exist', /not a film of any live lesson/, (g) => { C(g).films.push('osmoregulation/no-such-film'); });
breaks('film listed twice', /listed twice/, (g) => { C(g).films.push(C(g).films[0]); });
breaks('film from a lesson that is not a rung', /not a rung of this concept/, (g) => { C(g).films.push('action-potential/explainer'); });

console.log('sideways hops');
breaks('too many hops', /sideways hops \(limit/, (g) => { C(g).near = Object.keys(g.concepts).filter((x) => x !== ID).slice(0, 5).map((id) => ({ id, why: 'A reason in one sentence.' })); });
breaks('no hop yet (warning)', /no sideways hop/, (g) => { C(g).near = []; }, warns);
breaks('hop to a missing concept', /not a concept/, (g) => { C(g).near[0].id = 'no-such-concept'; });
breaks('hop to itself', /to itself/, (g) => { C(g).near[0].id = ID; });
breaks('hop listed twice', /listed twice/, (g) => { C(g).near.push(clone(C(g).near[0])); });
breaks('reason of two sentences', /not one sentence/, (g) => { C(g).near[0].why = 'One thing. Another thing.'; });
breaks('reason too long', /reason is \d+ words/, (g) => { C(g).near[0].why = Array(30).fill('water').join(' ') + '.'; });
breaks('analogy formula in a reason', /analogy or contrast/, (g) => { C(g).near[0].why = 'Diffusion parallels osmosis in every way.'; });

console.log('lesson records');
breaks('index out of step with the rungs', /does not match the rungs/, (g) => { g.lessons[C(g).rungs[0].lesson].concepts = []; });
breaks('record for a lesson that is gone', /not a live lesson/, (g) => { g.lessons['no-such-lesson'] = { hash: '0123456789abcdef', concepts: [] }; });
breaks('record lists a concept no rung names', /no rung names it/, (g) => { const free = [...site.lessons.keys()].find((s) => !g.lessons[s]); g.lessons[free] = { hash: site.lessons.get(free).contentHash, concepts: [ID] }; });
breaks('record without a hash', /no hash/, (g) => { Object.values(g.lessons)[0].hash = 'sample'; });
breaks('stale record (warning, listed by slug)', /written before their lesson's teaching text/, (g) => { Object.values(g.lessons)[0].hash = '0000000000000000'; }, warns);
check('a stale record is not an error, and names the lesson', () => {
  const g = clone(good); const slug = Object.keys(g.lessons)[0]; g.lessons[slug].hash = '0000000000000000';
  const v = validateGraph(g, site); assert.deepEqual(v.errors, []); assert.deepEqual(v.stale, [slug]);
});
check('live lessons with no record are a warning, each listed by slug', () => {
  const v = validateGraph(good, site);
  assert.equal(v.uncovered.length, site.lessons.size - Object.keys(good.lessons).length);
  if (v.uncovered.length) assert.ok(v.warnings.some((w) => w.includes(v.uncovered[0]) && /no record yet/.test(w)));
});
check('an empty record ("read, nothing to file") is allowed', () => {
  const g = clone(good); const free = [...site.lessons.keys()].find((s) => !g.lessons[s]);
  if (!free) return;
  g.lessons[free] = { hash: site.lessons.get(free).contentHash, concepts: [] };
  assert.deepEqual(errs(normalizeGraph(g, site)), []);
});

console.log('the content hash');
check('ignores frontmatter that is not teaching text (credits, quiz questions)', () => {
  const l = site.lessons.get('diffusion-and-osmosis');
  const fm = clone(l.fm); fm.practiceQuestions = []; fm.simulations = []; fm.estMinutes = 999;
  assert.equal(contentHash({ ...l, fm }), l.contentHash);
});
check('changes when the prose or a heading changes', () => {
  const l = site.lessons.get('diffusion-and-osmosis');
  assert.notEqual(contentHash({ ...l, body: l.body.replace('## Explain:', '## Explained:') }), l.contentHash);
  assert.notEqual(contentHash({ ...l, body: l.body + '\nOne more sentence of teaching.' }), l.contentHash);
  assert.notEqual(contentHash({ ...l, summary: l.summary + ' More.' }), l.contentHash);
});

console.log('wording rules');
check('good copy passes', () => {
  assert.equal(addsProblem('Water drifts to the saltier side: weigh cucumber slices and see.'), '');
  assert.equal(blurbProblem('Water moves across a membrane toward the side with more dissolved stuff.'), '');
  assert.equal(whyProblem('The same random motion, without the membrane\'s rule about who may cross.'), '');
  assert.equal(aliasProblem('why does salt make cucumbers wet'), '');
  assert.equal(idProblem('nitrogen-cycle'), '');
  assert.deepEqual(copyProblems('Microbes unlock matter others cannot use.'), []);
});
check('bad copy is named', () => {
  assert.match(addsProblem('An introduction to diffusion.'), /vague/);
  assert.match(addsProblem('Explores the action potential.'), /vague/);
  assert.match(whyProblem('This is related to that.'), /vague|filler/);
  assert.match(aliasProblem('how do you spell mitosis'), /spelled/);
  assert.match(idProblem('Nitrogen Cycle'), /kebab/);
  assert.ok(copyProblems('An amazing idea').includes('hype word'));
});

console.log('heading ids');
check('follow the page: repeats, punctuation, typographic dashes, keyboard subscripts', () => {
  const ids = headingIds('## Explain: water crosses\n\ntext\n\n## Explain: water crosses\n\n### Inside\n\n```\n## not a heading\n```\n\n## "Highly Conserved-- target"\n\n## How far E_K moves\n\n## The **bold** `code` [link](/x) one').map((h) => h.id);
  assert.deepEqual(ids, ['explain-water-crosses', 'explain-water-crosses-1', 'inside', 'highly-conserved-target', 'how-far-ek-moves', 'the-bold-code-link-one']);
});
check('every anchor in the committed graph is a section of its lesson', () => {
  for (const [id, c] of Object.entries(good.concepts)) for (const r of c.rungs) if (r.anchor) assert.ok(site.lessons.get(r.lesson).h2.has(r.anchor), `${id}/${r.lesson}#${r.anchor}`);
});

console.log('the build-time API');
const api = makeTopicGraph(good, coreSite(site));
check('conceptsOf: roles, core first; [] for a lesson with no record', () => {
  const cs = api.conceptsOf('diffusion-and-osmosis');
  assert.deepEqual(cs.map((c) => c.id).sort(), ['diffusion', 'osmosis']);
  assert.ok(cs.every((c) => c.role === 'core' && c.adds && c.anchor));
  const mixed = api.conceptsOf('synaptic-transmission');
  assert.equal(mixed[0].role, 'core'); assert.equal(mixed[mixed.length - 1].role, 'uses');
  assert.deepEqual(api.conceptsOf('no-such-lesson'), []);
  const free = [...site.lessons.keys()].find((s) => !good.lessons[s]);
  if (free) assert.deepEqual(api.conceptsOf(free), []);
});
check('concept and concepts', () => {
  assert.equal(api.concept('osmosis').name, 'Osmosis');
  assert.equal(api.concept('nope'), undefined);
  assert.equal(api.concepts.length, Object.keys(good.concepts).length);
});
check('ladder: core rungs only, lowest level first, joined, with step sizes', () => {
  const rungs = api.ladder('osmosis');
  assert.ok(rungs.length >= 4 && rungs.every((r) => r.role === 'core' && r.title && r.courseTitle && r.stageTitle && r.href.startsWith(`/lessons/${r.slug}/`)));
  for (let i = 1; i < rungs.length; i++) assert.ok(rungs[i].rank >= rungs[i - 1].rank);
  assert.equal(rungs[0].stepFromBelow, null);
  assert.equal(rungs[rungs.length - 1].stepToAbove, null);
  assert.equal(rungs[0].href, `/lessons/diffusion-and-osmosis/#${rungs[0].anchor}`);
  assert.deepEqual(rungs[0].films.map((f) => f.key), ['diffusion-and-osmosis/chapter-2']);
  // smell: an ages 5 to 10 activity, then nothing until college-further: a big step, stated
  const smell = api.ladder('smell');
  const up = smell.find((r) => r.rank > 0);
  assert.equal(smell[0].rank, 0); assert.equal(up.stepFromBelow, up.rank); assert.ok(up.stepFromBelow >= 4);
  assert.deepEqual(api.ladder('nope'), []);
});
check('ladderByLevel and span: gaps are data', () => {
  const rows = api.ladderByLevel('smell', true);
  assert.equal(rows.length, site.STAGES.length);
  assert.ok(rows.filter((g) => g.gap).length >= 3);
  assert.ok(api.ladderByLevel('smell').every((g) => g.rungs.length));
  const s = api.span('smell');
  assert.equal(s.lowest, 'ages-5-10'); assert.ok(s.gaps.includes('grade-7'));
  assert.equal(api.span('nerve-growth-factor').levels.length, 1);
});
check('usedBy: the uses rungs, never on the ladder', () => {
  const used = api.usedBy('action-potential').map((r) => r.slug);
  assert.ok(used.includes('synaptic-transmission'));
  assert.ok(!api.ladder('action-potential').some((r) => used.includes(r.slug)));
});
check('hops: down, up and sideways for each idea a lesson teaches', () => {
  const h = api.hops('crossing-the-membrane');
  const o = h.find((x) => x.id === 'osmosis');
  assert.ok(o, 'osmosis is core for crossing-the-membrane');
  assert.equal(o.down.slug, 'diffusion-and-osmosis'); assert.equal(o.down.jump, 1);
  assert.ok(o.up && o.up.rank > 2 && o.up.jump === o.up.rank - 2);
  assert.ok(o.upAll.every((r) => r.rank === o.up.rank));
  assert.ok(o.sideways.length && o.sideways.every((s) => s.name && s.why && s.id !== 'osmosis'));
  const side = o.sideways.find((s) => s.to);
  assert.ok(side && side.to.slug !== 'crossing-the-membrane');
  // the bottom of a ladder: no simpler version, said plainly
  const bottom = api.hops('diffusion-and-osmosis').find((x) => x.id === 'osmosis');
  assert.equal(bottom.down, undefined); assert.deepEqual(bottom.downAll, []); assert.ok(bottom.up);
  // an idea at one level only: neighbours beside it, nothing above or below
  const ngf = api.hops('neurotrophic-hypothesis').find((x) => x.id === 'nerve-growth-factor');
  assert.equal(ngf.down, undefined); assert.equal(ngf.up, undefined); assert.ok(ngf.beside.length >= 2);
  // uses rungs give no hops; a lesson with no record gives none
  assert.ok(!api.hops('synaptic-transmission').some((x) => x.id === 'action-potential'));
  assert.deepEqual(api.hops('no-such-lesson'), []);
});
check('filmsFor: joined with the films, lowest level first', () => {
  const fs = api.filmsFor('action-potential');
  assert.ok(fs.length >= 4 && fs.every((f) => f.title && f.href.startsWith('/watch/') && f.poster && f.durationSec > 0 && f.lessonTitle));
  for (let i = 1; i < fs.length; i++) assert.ok(fs[i].rank >= fs[i - 1].rank);
  assert.ok(fs.some((f) => f.key === 'action-potential/three-gates' && f.href === '/watch/action-potential/three-gates/'));
  assert.deepEqual(api.filmsFor('nope'), []);
});
check('searchIndex and searchConcepts: names, everyday phrases, both spellings', () => {
  const index = api.searchIndex();
  assert.equal(index.length, api.concepts.length);
  assert.ok(index.every((r) => r.terms.length === r.aliases.length + 1 && r.levels.length));
  assert.equal(searchConcepts(index, 'osmosis')[0], 'osmosis');
  assert.equal(searchConcepts(index, 'Why does salt make cucumbers wet?')[0], 'osmosis');
  assert.equal(searchConcepts(index, 'how do nerves send signals')[0], 'action-potential');
  assert.equal(searchConcepts(index, 'why does celery soak up coloured water')[0], 'plant-water-transport');
  assert.deepEqual(searchConcepts(index, ''), []);
  assert.equal(fold('Colour of the Tumour, fertilised'), fold('color of the tumor fertilized'));
});
check('the browser forms: index, one area, everything; tables point at real rows', () => {
  const all = api.clientGraph();
  assert.equal(all.concepts.length, api.concepts.length);
  for (const c of all.concepts) {
    for (const r of c.r) { assert.ok(all.lessons[r[0]], `${c.id} rung`); if (r[1] === 0) assert.ok(typeof r[2] === 'string' && r[2]); }
    for (const f of c.f) assert.ok(all.films[f]);
    for (const x of c.x) assert.ok(all.concepts[x[0]]);
  }
  for (const l of all.lessons) assert.ok(all.courses[l[2]] && all.stages[all.courses[l[2]][2]]);
  const back = expandClientGraph(all).find((c) => c.id === 'osmosis');
  assert.deepEqual(back.rungs.filter((r) => r.role === 'core').map((r) => r.slug).sort(), good.concepts.osmosis.rungs.filter((r) => r.role === 'core').map((r) => r.lesson).sort());
  assert.deepEqual(back.near, good.concepts.osmosis.near);
  assert.deepEqual(back.films.map((f) => f.key).sort(), [...good.concepts.osmosis.films].sort());
  const cells = api.clientGraph(api.concepts.filter((c) => c.area === 'cells').map((c) => c.id));
  assert.ok(cells.concepts.length && cells.concepts.every((c) => good.concepts[c.id].area === 'cells'));
  assert.ok(cells.concepts.every((c) => c.x.every((x) => typeof x[0] === 'string' && good.concepts[x[0]])));
  assert.ok(cells.lessons.length < all.lessons.length);
  const index = api.clientIndex();
  assert.equal(index.covered, Object.keys(good.lessons).length); assert.equal(index.live, site.lessons.size);
  assert.equal(index.areas.reduce((n, a) => n + a[2], 0), index.concepts.length);
  const o = index.concepts.findIndex((c) => c.id === 'osmosis');
  assert.ok(index.lessons['diffusion-and-osmosis'].includes(o));
  assert.equal(index.concepts[o].l & 1, 0); assert.ok(index.concepts[o].l & 2);
  assert.ok(!JSON.stringify(index).includes('undefined'));
});
check('a lesson that is gone or an anchor that was reworded degrades, never throws', () => {
  const g = clone(good);
  g.concepts.osmosis.rungs[0].anchor = 'reworded-away';
  g.concepts.osmosis.rungs.push({ lesson: 'unpublished-lesson', role: 'core', adds: 'x' });
  const a = makeTopicGraph(g, coreSite(site));
  const rungs = a.ladder('osmosis');
  assert.ok(!rungs.some((r) => r.slug === 'unpublished-lesson'));
  assert.equal(rungs[0].href, '/lessons/diffusion-and-osmosis/'); assert.equal(rungs[0].anchor, undefined);
  assert.doesNotThrow(() => { a.clientGraph(); a.clientIndex(); a.hops('diffusion-and-osmosis'); });
});

console.log('ingest');
const stagingOf = (parts) => ({ proposals: [], canonical: [], near: [], verify: [], problems: [], ...parts });
const file = (kind, name, data) => ({ file: `${kind}/${name}.json`, name, data });
const FREE = [...site.lessons.values()].filter((l) => !good.lessons[l.slug] && l.h2.size && l.filmList.length);
const [L1, L2, L3] = FREE;
const prop = (l, concepts, extra = {}) => file('proposals', l.slug, { lesson: l.slug, hash: l.contentHash, opened_lesson: true, concepts, relations: [], notes: '', ...extra });
const newDef = (n) => ({ name: `Test idea ${n}`, blurb: `A test idea number ${n} for the merge.`, area: 'methods', aliases: [`test question ${n}`, `test term ${n}`] });
const core = (id, l, extra = {}) => ({ id, role: 'core', anchor: [...l.h2][0], adds: 'A test note that names one case.', films: [l.filmList[0].key], ...extra });
const run = (parts, opts = {}) => ingest({ base: good, site, staging: stagingOf(parts), date: '2026-01-01', ...opts });
const rejected = (r, re) => r.log.rejected.some((x) => re.test(`${x.item}: ${x.reason}`));

check('the seed goes through the pipeline unchanged (decompose, then ingest onto an empty graph)', () => {
  const r = ingest({ base: { version: 1, updated: good.updated, about: '', areas: good.areas, concepts: {}, lessons: {} }, site, staging: decomposeGraph(good, site), maxUses: LIMITS.usesPerLesson, date: good.updated });
  assert.deepEqual(r.log.rejected, []); assert.deepEqual(r.validation.errors, []);
  assert.equal(serializeGraph(r.graph), serializeGraph(good));
});
check('no staging files: the graph comes back byte for byte', () => {
  const r = ingest({ base: good, site, staging: stagingOf({}) });
  assert.equal(serializeGraph(r.graph), serializeGraph(good));
});
check('a good proposal: reuse of a registry id and a new concept', () => {
  const r = run({ proposals: [prop(L1, [core('test-idea-one', L1, { new: newDef('one') }), { id: 'diffusion', role: 'uses' }])] });
  assert.deepEqual(r.log.rejected, []); assert.deepEqual(r.validation.errors, []);
  assert.deepEqual(r.graph.lessons[L1.slug], { hash: L1.contentHash, concepts: ['test-idea-one', 'diffusion'] });
  assert.deepEqual(r.graph.concepts['test-idea-one'].films, [L1.filmList[0].key]);
  assert.ok(r.graph.concepts.diffusion.rungs.some((x) => x.lesson === L1.slug && x.role === 'uses'));
});
check('a proposal replaces that lesson\'s rungs and nothing else, and the change is logged', () => {
  const slug = 'diffusion-and-osmosis'; const l = site.lessons.get(slug);
  const r = run({ proposals: [prop(l, [{ id: 'diffusion', role: 'core', anchor: 'explain-particles-spread-from-more-to-less', adds: 'Random moves add up to a one-way drift from crowded to empty.', films: ['diffusion-and-osmosis/explainer'] }])] });
  assert.ok(!r.graph.concepts.osmosis.rungs.some((x) => x.lesson === slug));
  assert.ok(!r.graph.concepts.osmosis.films.some((k) => k.startsWith(`${slug}/`)));
  assert.equal(r.graph.concepts.osmosis.rungs.length, good.concepts.osmosis.rungs.length - 1);
  assert.deepEqual(r.graph.concepts.diffusion, good.concepts.diffusion);
  assert.ok(r.log.changed.some((c) => c.stage === 'propose' && c.what.includes(slug) && c.what.includes('removed')));
});
const badProposal = (name, re, concepts, extra) => check(`rejected: ${name}`, () => { const r = run({ proposals: [prop(L1, concepts, extra)] }); assert.ok(rejected(r, re), JSON.stringify(r.log.rejected)); assert.deepEqual(r.validation.errors, []); });
badProposal('unknown concept id with no definition', /no valid definition/, [core('never-defined', L1)]);
badProposal('bad id', /kebab-case/, [core('Bad Id', L1, { new: newDef('x') })]);
badProposal('bad role', /role must be/, [{ ...core('diffusion', L1), role: 'teaches' }]);
badProposal('core without a note', /without a note/, [{ ...core('diffusion', L1), adds: '' }]);
badProposal('vague note', /vague note/, [core('diffusion', L1, { adds: 'Covers diffusion in more detail.' })]);
badProposal('note over 14 words', /note is \d+ words/, [core('diffusion', L1, { adds: Array(16).fill('word').join(' ') + '.' })]);
badProposal('film of another lesson', /not a film of this lesson/, [core('diffusion', L1, { films: ['action-potential/explainer'] })]);
badProposal('concept listed twice', /listed twice/, [core('diffusion', L1), { id: 'diffusion', role: 'uses' }]);
badProposal('new concept with a two-sentence blurb', /not one sentence/, [core('test-idea-two', L1, { new: { ...newDef('two'), blurb: 'One. Two.' } })]);
badProposal('new concept with one alias', /valid aliases/, [core('test-idea-two', L1, { new: { ...newDef('two'), aliases: ['only one'] } })]);
badProposal('new concept in an unknown area', /unknown area/, [core('test-idea-two', L1, { new: { ...newDef('two'), area: 'nowhere' } })]);
badProposal('more than three core concepts', /over the limit of 3 core/, ['a', 'b', 'c', 'd'].map((x) => core(`test-idea-${x}`, L1, { new: newDef(x), films: [] })));
badProposal('more than two uses', /over the limit of 2 "uses"/, [core('diffusion', L1), { id: 'osmosis', role: 'uses' }, { id: 'enzymes', role: 'uses' }, { id: 'synapse', role: 'uses' }]);
check('rejected: an anchor that is not a section, but the rung is kept without it', () => {
  const r = run({ proposals: [prop(L1, [core('diffusion', L1, { anchor: 'no-such-section' })])] });
  assert.ok(rejected(r, /kept without an anchor/));
  const rung = r.graph.concepts.diffusion.rungs.find((x) => x.lesson === L1.slug);
  assert.ok(rung && rung.role === 'core' && !rung.anchor);
});
check('rejected whole: wrong lesson name, missing hash, a lesson that is not live; the lesson keeps what it had', () => {
  const r = run({ proposals: [
    file('proposals', L1.slug, { lesson: 'something-else', hash: L1.contentHash, concepts: [] }),
    file('proposals', L2.slug, { lesson: L2.slug, concepts: [core('diffusion', L2)] }),
    file('proposals', 'no-such-lesson', { lesson: 'no-such-lesson', hash: '0123456789abcdef', concepts: [] }),
    prop(site.lessons.get('diffusion-and-osmosis'), [core('never-defined', L1)]),
  ] });
  assert.equal(r.log.rejected.filter((x) => x.item === '(whole file)').length, 4);
  assert.equal(serializeGraph({ ...r.graph, updated: good.updated }), serializeGraph(good));
});
check('a proposal read from an older version of the lesson is stored with its hash and shows as stale', () => {
  const r = run({ proposals: [prop(L1, [core('diffusion', L1)], { hash: '0123456789abcdef' })] });
  assert.equal(r.graph.lessons[L1.slug].hash, '0123456789abcdef');
  assert.deepEqual(r.validation.stale, [L1.slug]);
});
check('an empty proposal files the lesson as read', () => {
  const r = run({ proposals: [prop(L1, [], { notes: 'A course welcome page.' })] });
  assert.deepEqual(r.graph.lessons[L1.slug], { hash: L1.contentHash, concepts: [] });
  assert.deepEqual(r.validation.errors, []);
});
const three = () => [prop(L1, [core('test-idea-a', L1, { new: newDef('a') })]), prop(L2, [core('test-idea-b', L2, { new: newDef('b') })]), prop(L3, [core('test-idea-c', L3, { new: newDef('c') })])];
check('canonicalize: merge two ids into one, keep one, drop one; rungs, films and aliases follow', () => {
  const r = run({ proposals: three(), canonical: [file('canonical', 'methods', { area: 'methods', concepts: [{ id: 'test-idea-a', merge: ['test-idea-a', 'test-idea-b'] }], drop: [{ id: 'test-idea-c', why: 'A topic, not an idea.' }], rungs: [] })] });
  assert.deepEqual(r.log.rejected, []); assert.deepEqual(r.validation.errors, []);
  const c = r.graph.concepts['test-idea-a'];
  assert.deepEqual(c.rungs.map((x) => x.lesson).sort(), [L1.slug, L2.slug].sort());
  assert.equal(c.films.length, 2); assert.ok(c.aliases.includes('test term b'));
  assert.ok(!r.graph.concepts['test-idea-b'] && !r.graph.concepts['test-idea-c']);
  assert.deepEqual(r.graph.lessons[L3.slug].concepts, []);
  assert.ok(r.log.changed.some((x) => /test-idea-c dropped, so .* loses its core rung/.test(x.what)));
});
check('canonicalize: merge into a new id needs a full definition; merge into a registry id keeps its fields', () => {
  const bad = run({ proposals: three(), canonical: [file('canonical', 'methods', { area: 'methods', concepts: [{ id: 'test-merged', merge: ['test-idea-a', 'test-idea-b'] }, { id: 'test-idea-c', merge: ['test-idea-c'] }], drop: [] })] });
  assert.ok(rejected(bad, /a new id needs/)); assert.ok(bad.graph.concepts['test-idea-a'] && bad.graph.concepts['test-idea-b']);
  const ok = run({ proposals: three(), canonical: [file('canonical', 'methods', { area: 'methods', concepts: [{ id: 'test-merged', merge: ['test-idea-a', 'test-idea-b'], name: 'Merged test idea', blurb: 'Two test ideas that turned out to be one.', area: 'cells', aliases: ['merged question', 'merged term'] }, { id: 'diffusion', merge: ['test-idea-c'] }], drop: [] })] });
  assert.deepEqual(ok.log.rejected, []);
  assert.equal(ok.graph.concepts['test-merged'].area, 'cells'); assert.equal(ok.graph.concepts['test-merged'].rungs.length, 2);
  assert.equal(ok.graph.concepts.diffusion.name, good.concepts.diffusion.name);
  assert.ok(ok.graph.concepts.diffusion.rungs.some((x) => x.lesson === L3.slug && x.role === 'core'));
});
check('canonicalize: an id left out is reported and kept; a registry concept cannot be dropped; rung fixes apply', () => {
  const r = run({ proposals: three(), canonical: [file('canonical', 'methods', { area: 'methods', concepts: [{ id: 'test-idea-a', merge: ['test-idea-a'] }], drop: [{ id: 'osmosis', why: 'no' }], rungs: [{ id: 'test-idea-a', lesson: L1.slug, adds: 'A sharper test note with one number, 42.', why: 'blurred' }, { id: 'diffusion', lesson: 'gas-exchange', role: 'uses', why: 'leans on it' }, { id: 'diffusion', lesson: 'no-such', role: 'drop' }] })] });
  assert.ok(rejected(r, /not mentioned in/)); assert.ok(rejected(r, /cannot be dropped/)); assert.ok(rejected(r, /no such rung/));
  assert.ok(r.graph.concepts['test-idea-b'] && r.graph.concepts.osmosis);
  assert.equal(r.graph.concepts['test-idea-a'].rungs[0].adds, 'A sharper test note with one number, 42.');
  const g = r.graph.concepts.diffusion.rungs.find((x) => x.lesson === 'gas-exchange');
  assert.equal(g.role, 'uses'); assert.ok(!r.graph.concepts.diffusion.films.includes('gas-exchange/explainer'));
});
check('canonicalize across areas: sideways hops that pointed at a merged id follow it', () => {
  const r = run({ proposals: three(), near: [file('near', 'methods', { area: 'methods', near: { 'test-idea-a': [{ id: 'test-idea-b', why: 'They share one test mechanism.' }], 'test-idea-c': [{ id: 'test-idea-b', why: 'A real case joins the two.' }] } })], canonical: [file('canonical', '_cross', { area: '_cross', concepts: [{ id: 'test-idea-a', merge: ['test-idea-a', 'test-idea-b'] }] })] });
  assert.deepEqual(r.validation.errors, []);
  assert.deepEqual(r.graph.concepts['test-idea-c'].near.map((n) => n.id), ['test-idea-a']);
  assert.deepEqual(r.graph.concepts['test-idea-a'].near, []);      // a hop to itself is not kept
});
check('near: good hops replace the list; a hop to itself, an analogy, a missing target and a fifth hop are rejected', () => {
  const others = Object.keys(good.concepts).filter((x) => x !== 'osmosis').slice(0, 5);
  const r = run({ near: [file('near', 'cells', { area: 'cells', near: { osmosis: [
    { id: others[0], why: 'A real case joins the two ideas.' }, { id: 'osmosis', why: 'Itself.' }, { id: others[1], why: 'This mirrors that.' }, { id: 'no-such', why: 'Nothing here.' },
    { id: others[2], why: 'A second real case.' }, { id: others[3], why: 'A third real case.' }, { id: others[4], why: 'A fourth real case.' }, { id: others[1], why: 'A fifth real case.' },
  ], 'no-such-concept': [] } })] });
  assert.deepEqual(r.graph.concepts.osmosis.near.map((n) => n.id), [others[0], others[2], others[3], others[4]]);
  for (const re of [/a hop to itself/, /analogy or contrast/, /target is not a concept/, /over the limit of 4/, /not a concept/]) assert.ok(rejected(r, re), String(re));
});
const verdict = (id, rungs, extra = {}, base = good) => file('verify', id, { concept: id, ticket: ticketOf(id, base.concepts[id]), same_idea: true, rungs, bad_anchors: [], bad_films: [], bad_aliases: [], notes: '', ...extra });
const okAll = (id) => good.concepts[id].rungs.filter((r) => r.role === 'core').map((r) => ({ lesson: r.lesson, verdict: 'ok' }));
check('verify: a rung judged wrong is removed and logged; not-core becomes uses; a note is replaced', () => {
  const rungs = okAll('osmosis');
  rungs[0] = { ...rungs[0], verdict: 'wrong', why: 'About something else.' };
  rungs[1] = { ...rungs[1], verdict: 'not-core', why: 'Leans on it.' };
  rungs[2] = { ...rungs[2], verdict: 'note', adds: 'A truer note that names the sea fish.', why: 'The number was not in the lesson.' };
  const r = run({ verify: [verdict('osmosis', rungs)] });
  assert.deepEqual(r.validation.errors, []);
  const c = r.graph.concepts.osmosis;
  assert.ok(!c.rungs.some((x) => x.lesson === rungs[0].lesson));
  const demoted = c.rungs.find((x) => x.lesson === rungs[1].lesson);
  assert.deepEqual(demoted, { lesson: rungs[1].lesson, role: 'uses' });
  assert.ok(!c.films.some((k) => k.startsWith(`${rungs[0].lesson}/`) || k.startsWith(`${rungs[1].lesson}/`)));
  assert.equal(c.rungs.find((x) => x.lesson === rungs[2].lesson).adds, 'A truer note that names the sea fish.');
  assert.equal(r.log.changed.filter((x) => x.stage === 'verify').length, 3);
  assert.ok(!r.graph.lessons[rungs[0].lesson].concepts.includes('osmosis'));
});
check('verify: bad aliases, films and anchors are removed; a missing verdict and an unusable note are reported', () => {
  const rungs = okAll('osmosis').slice(1);
  rungs[0] = { ...rungs[0], verdict: 'note', adds: 'Covers it in more detail.' };
  const c0 = good.concepts.osmosis;
  const r = run({ verify: [verdict('osmosis', rungs, { bad_aliases: [{ alias: c0.aliases[0], why: 'A nerve response.' }], bad_films: [{ film: c0.films[0], why: 'Shows diffusion.' }], bad_anchors: [c0.rungs[1].lesson] })] });
  const c = r.graph.concepts.osmosis;
  assert.ok(!c.aliases.includes(c0.aliases[0]) && !c.films.includes(c0.films[0]) && !c.rungs[1].anchor);
  assert.ok(rejected(r, /gave no verdict/)); assert.ok(rejected(r, /replacement was not usable/));
  assert.equal(c.rungs[1].adds, c0.rungs[1].adds);
});
check('verify: a verdict on a concept that changed since it was judged is not applied', () => {
  const rungs = okAll('osmosis'); rungs[0] = { ...rungs[0], verdict: 'wrong', why: 'x' };
  const r = run({ verify: [file('verify', 'osmosis', { concept: 'osmosis', ticket: 'aaaaaaaaaa', same_idea: true, rungs })] });
  assert.ok(rejected(r, /ticket .* does not match/));
  assert.deepEqual(r.graph.concepts.osmosis, good.concepts.osmosis);
});
check('verify: a concept left with no core rung is removed, with the hops that pointed at it', () => {
  const id = 'nerve-growth-factor';
  const r = run({ verify: [verdict(id, okAll(id).map((x) => ({ ...x, verdict: 'wrong', why: 'x' })), { same_idea: false })] });
  assert.ok(!r.graph.concepts[id]); assert.deepEqual(r.validation.errors, []);
  assert.ok(!Object.values(r.graph.concepts).some((c) => c.near.some((n) => n.id === id)));
  assert.ok(r.log.changed.some((x) => x.what.includes(`${id} removed: no lesson teaches it`)));
});
check('an alias cannot end up on two concepts or be a concept\'s name', () => {
  const taken = good.concepts.osmosis.aliases[0];
  const r = run({ proposals: [prop(L1, [core('test-idea-a', L1, { new: { ...newDef('a'), aliases: [taken, 'diffusion', 'test term a', 'test question a'] } })])] });
  assert.deepEqual(r.validation.errors, []);
  assert.deepEqual(r.graph.concepts['test-idea-a'].aliases, ['test term a', 'test question a']);
  assert.ok(rejected(r, /already an alias of osmosis/)); assert.ok(rejected(r, /it is the name of diffusion/));
});
check('the same input gives the same bytes, whatever order the files arrive in', () => {
  const parts = { proposals: three(), near: [file('near', 'methods', { area: 'methods', near: { 'test-idea-a': [{ id: 'osmosis', why: 'A real case joins the two.' }] } })] };
  const a = run(parts), b = run({ proposals: [...parts.proposals].reverse(), near: parts.near });
  assert.equal(serializeGraph(a.graph), serializeGraph(b.graph));
});
check('unreadable files are reported, not skipped silently', () => {
  const r = run({ problems: [{ stage: 'proposals', file: 'proposals/x.json', item: '(whole file)', reason: 'not valid JSON' }] });
  assert.equal(r.log.rejected.length, 1);
});

console.log('digests and prompts');
const digests = buildDigests(site, ['diffusion-and-osmosis', 'thirsty-celery', 'action-potential']);
const registry = registryOf(good, site);
check('a digest carries the hash, every section with its id, the level texts, films with keys, and the links on the page', () => {
  const d = digests.get('diffusion-and-osmosis');
  assert.equal(d.hash, site.lessons.get(d.slug).contentHash);
  assert.deepEqual(d.sections.map((s) => s.id), [...site.lessons.get(d.slug).h2]);
  assert.ok(d.sections.some((s) => s.lead)); assert.equal(d.levels.length, 4);
  assert.deepEqual(d.films.map((f) => f.key), ['diffusion-and-osmosis/explainer', 'diffusion-and-osmosis/chapter-2']);
  assert.ok(d.films.every((f) => f.takeaways?.length)); assert.ok(d.ladder.highSchool.length && d.links.before.length);
  const t = digestText(d);
  for (const s of ['[explain-water-crosses-a-choosy-membrane]', 'diffusion-and-osmosis/chapter-2', d.hash, 'src/content/lessons/diffusion-and-osmosis/lesson.mdx']) assert.ok(t.includes(s), s);
  const a = digests.get('thirsty-celery');
  assert.match(a.reader, /grown-up/); assert.ok(a.films[0].opens, 'a film with no take-homes shows how it opens'); assert.ok(a.openTheLessonIf.length);
  assert.ok(!JSON.stringify([...digests.values()]).includes('"adds"'), 'a digest holds nothing from the graph');
});
check('every prompt is self-contained: the rules, the registry, the answer shape', () => {
  const d = digests.get('diffusion-and-osmosis');
  const p = proposePrompt(d, registry, { existing: [{ id: 'osmosis', role: 'core' }] });
  for (const s of ['The anchor is the test', 'PREREQUISITES', 'THREE WORKED EXAMPLES', 'neurotrophic-hypothesis', 'fingers wrinkle', 'the grown-up', 'osmosis | Osmosis', 'ALREADY HAS A RECORD', '"hash"', 'explain-water-crosses-a-choosy-membrane', 'No dashes', 'medical advice']) assert.ok(p.includes(s), s);
  const b = proposeBatchPrompt([...digests.values()], registry, { answerDir: '/x/proposals', courseMap: 'MAP' });
  assert.ok(b.includes('/x/proposals/<slug>.json') && b.includes('LESSON thirsty-celery') && b.includes('MAP'));
  const c = canonicalizePrompt({ area: 'cells', proposed: [{ id: 'water-movement', defs: [{ name: 'Water movement', blurb: 'x', area: 'cells', aliases: ['a', 'b'], by: 'osmoregulation' }], rungs: [{ lesson: 'osmoregulation', title: 'T', stage: 'starting-college', rank: 3, role: 'core', adds: 'n', anchor: 'a' }] }], existing: [] }, registry);
  for (const s of ['water-movement', 'EVERY new id', '"merge"', 'KEEP APART', 'a wrong rung is worse than a missing one']) assert.ok(c.includes(s), s);
  assert.ok(canonicalizePrompt({ area: '_cross', proposed: [] }, registry).includes('ACROSS all areas'));
  const n = nearPrompt('cells', registry.filter((x) => x.area === 'cells').map((x) => ({ ...x, near: [] })), registry, { hints: [{ a: 'osmosis', b: 'diffusion', note: 'h', by: 'x' }] });
  for (const s of ["from the reader's", 'antibiotic', 'CONCEPTS TO WRITE FOR', 'osmosis <-> diffusion']) assert.ok(n.includes(s), s);
  const a = assignPrompt(d, registry, { ladders: [{ id: 'osmosis', rungs: [{ lesson: 'x', stage: 'grade-7', adds: 'n' }] }] });
  for (const s of ['no later merging step', 'LADDERS THIS LESSON MAY JOIN', 'also asked as', '"near"']) assert.ok(a.includes(s), s);
  const g = good.concepts.osmosis;
  const v = verifyPrompt({ id: 'osmosis', ...g, ticket: ticketOf('osmosis', g), rungs: g.rungs.map((r) => ({ ...r, stage: site.lessons.get(r.lesson).stage })), films: g.films.map((k) => ({ key: k, title: 't' })) }, digests);
  for (const s of ['You did not write it', ticketOf('osmosis', g), '"not-core"', 'Do not be generous', 'LESSON diffusion-and-osmosis', 'no digest available']) assert.ok(v.includes(s), s);
  for (const text of [p, b, c, n, a, v]) assert.ok(!/undefined|\[object Object\]/.test(text), 'a prompt has a hole in it');
});

console.log(`\n${passed} checks passed.${process.exitCode ? ' SOME FAILED.' : ''}`);
