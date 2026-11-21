#!/usr/bin/env node
/**
 * Hopping tests: the words (src/lib/hop-words.mjs) and the idea search (src/lib/hop-search.mjs),
 * against every idea and every lesson in the committed hop graph. Runs from source; needs no build
 * and calls no model.
 *
 *   node scripts/test-hop.mjs            the tests (also in CI)
 *   node scripts/test-hop.mjs --print    every generated hop sentence, for reading
 *   node scripts/test-hop.mjs --print osmosis touch   only lessons on those ideas
 */
import assert from 'node:assert/strict';
import { loadGraphSite, coreSite, readGraph, makeTopicGraph } from './topic-graph/lib.mjs';
import { inSentence, lessonSentence, authoredLinks, plain, stepNote, levelNote, gapLine, taughtAt, levelCount, edgeLines, compactLine, maskOf, ranksOf, SENTENCE_MAX, LEVEL_SHORT, LEVEL_LABEL, QUICK_NAME, andList } from '../src/lib/hop-words.mjs';
import { ladderHtml, ladderGlyph, ladderRows } from '../src/lib/hop-ladder.mjs';
import { buildIndex, search, stem, oneSlip, solCode } from '../src/lib/hop-search.mjs';

let passed = 0;
const check = (name, fn) => { try { fn(); passed++; console.log(`  ok  ${name}`); } catch (e) { console.log(`  FAIL ${name}\n${e.message ?? e}`); process.exitCode = 1; } };

const site = await loadGraphSite();
const graph = readGraph();
const api = makeTopicGraph(graph, coreSite(site));
const lessons = [...site.lessons.values()];

/** What is wrong with a sentence a reader will see. [] when it reads cleanly. */
function faults(text) {
  const out = [];
  if (!text.trim()) out.push('empty');
  if (/\b(\w+) \1\b/i.test(text.replace(/\b(that that|had had)\b/g, ''))) out.push(`doubled word: ${/\b(\w+) \1\b/i.exec(text)[0]}`);
  if (/undefined|null|NaN|\[object/.test(text)) out.push('a value leaked');
  if (/ {2}|\( | \)|\(\)| ,| \.|,,|\.\.|, \)|;\)/.test(text)) out.push('spacing or punctuation');
  if (!/[.:]$/.test(text.trim())) out.push('no full stop');
  if (/\b(easier|harder|level up|beginner|advanced|lower level|higher level|dumbed)\b/i.test(text)) out.push('ranks the reader');
  if (/—/.test(text)) out.push('em-dash');
  return out;
}
/** A level named twice in one line ("grade 7 … grade 7") is allowed only where the second names the short version. */
function levelTwice(line) {
  const t = line.replace(/read a short [a-z0-9 ]+ version here/, '');
  return LEVEL_SHORT.filter((l) => t.split(l).length > 2);
}

const sentences = lessons.map((l) => {
  const authored = authoredLinks(l.slug, site.lessons);
  const s = lessonSentence(api.hops(l.slug), { slug: l.slug, title: l.title, rank: l.rank, courseTitle: l.courseTitle, explainLevels: l.fm.explainLevels, authored });
  const lines = ['teaches', 'simpler', 'deeper', 'next'].filter((k) => s.lines[k]).map((k) => [k, s.lines[k], plain(s.lines[k])]);
  return { l, s, authored, lines, ideas: api.hops(l.slug).map((h) => h.id) };
});

if (process.argv.includes('--print')) {
  const only = process.argv.slice(process.argv.indexOf('--print') + 1);
  for (const x of sentences) {
    if (only.length && !x.ideas.some((i) => only.includes(i)) && !only.includes(x.l.slug)) continue;
    console.log(`\n${x.l.slug}  [${x.l.stage}]`);
    for (const [, , text] of x.lines) console.log(`  ${text}`);
    console.log(`  > ${x.s.more}  (${x.s.length} characters)`);
  }
  process.exit(0);
}

console.log('names inside a sentence');
check('every idea has a name that reads inside a sentence', () => {
  const bad = [];
  for (const c of api.concepts) {
    const s = inSentence(c.id, c.short ?? c.name);
    if (!s || /[()]/.test(s) || /[:,]$/.test(s) || s.length > 60) bad.push(`${c.id}: "${s}"`);
    if (/^(A|An|The|How|Why|What|Which|Where|When) /.test(s)) bad.push(`${c.id}: starts with a capital: "${s}"`);
  }
  assert.deepEqual(bad, []);
});
check('abbreviations and names keep their capitals; plain words lose them', () => {
  assert.equal(inSentence('atp', 'ATP, the cell’s energy carrier'), 'ATP');
  assert.equal(inSentence('dna-structure', 'DNA, the molecule of heredity'), 'DNA');
  assert.equal(inSentence('mtor-growth-control', 'mTOR: the cell’s decision to grow'), 'mTOR');
  assert.equal(inSentence('ph-and-buffers', 'pH and buffers'), 'pH and buffers');
  assert.equal(inSentence('hardy-weinberg', 'Hardy-Weinberg and allele frequencies'), 'Hardy-Weinberg and allele frequencies');
  assert.equal(inSentence('action-potential', 'Nerve signals (the action potential)'), 'nerve signals');
  assert.equal(inSentence('cell-theory', 'Cells, the unit of life'), 'cells');
  assert.equal(inSentence('rho-gtpases', 'Rho, Rac and Cdc42'), 'Rho, Rac and Cdc42');
  assert.equal(inSentence('cell-migration', 'How cells crawl (cell migration)'), 'how cells crawl');
});

console.log('the size of a step, in words');
check('the next level needs no note; one skipped level is named; more is a big step', () => {
  assert.equal(stepNote(2, 1), '');
  assert.equal(stepNote(2, 3), '');
  assert.equal(stepNote(2, 5), '', 'college is one place: its three bands are named, not counted as gaps');
  assert.equal(stepNote(3, 5), '');
  assert.equal(stepNote(1, 4), 'nothing at high school yet');
  assert.equal(stepNote(2, 6), 'nothing at college level yet');
  assert.equal(stepNote(0, 2), 'nothing at grade 7 yet');
  assert.equal(stepNote(0, 5), 'a big step: nothing in between yet');
  assert.equal(levelNote(2, 1), '(grade 7)');
  assert.equal(levelNote(1, 4), '(college core; nothing at high school yet)');
  assert.equal(levelNote(0, 5), '(upper-level college, a big step: nothing in between yet)');
});
check('a step is the same size in both directions', () => {
  for (let a = 0; a < 7; a++) for (let b = 0; b < 7; b++) if (a !== b) assert.equal(stepNote(a, b), stepNote(b, a));
});
check('gaps and edges are said plainly', () => {
  assert.equal(gapLine('touch', [2]), 'No lesson on touch at high school yet.');
  assert.equal(gapLine('touch', [1, 2]), 'No lesson on touch at grade 7 or at high school yet.');
  assert.equal(gapLine('touch', [1, 2, 3, 4]), 'No lesson on touch at these four levels yet.');
  assert.equal(taughtAt(maskOf([1, 2])), 'Taught at two levels: grade 7 and high school.');
  assert.equal(taughtAt(maskOf([6])), 'Taught at one level so far: graduate level.');
  assert.equal(edgeLines(maskOf([1, 2])).below, 'Nothing simpler on the site yet. The first place it is taught is grade 7.');
  assert.equal(edgeLines(maskOf([0, 6])).below + edgeLines(maskOf([0, 6])).above, '');
  assert.equal(compactLine({ name: 'Osmosis', mask: maskOf([1, 2, 3]), here: 2 }), 'Osmosis, high school. Also at: grade 7 and a first college course.');
  assert.equal(compactLine({ name: 'Reelin', mask: maskOf([6]), here: 6 }), 'Reelin, graduate level: the only level so far.');
});

console.log(`the hop sentence, over all ${lessons.length} lessons`);
check('every live lesson gets a sentence that names an idea', () => {
  const none = sentences.filter((x) => !x.ideas.length).map((x) => x.l.slug);
  assert.deepEqual(none, [], 'lessons with no idea in the graph get no sentence; the page falls back to its old ladder card');
});
check('no line is empty, doubled, leaking or ranking, and each ends with a full stop', () => {
  const bad = [];
  for (const x of sentences) for (const [k, , text] of x.lines) for (const f of faults(text)) bad.push(`${x.l.slug} ${k}: ${f}: ${text}`);
  assert.deepEqual(bad.slice(0, 12), []);
});
check('no line names a level twice', () => {
  const bad = [];
  for (const x of sentences) for (const [k, , text] of x.lines) { const t = levelTwice(text); if (t.length) bad.push(`${x.l.slug} ${k}: ${t}: ${text}`); }
  assert.deepEqual(bad.slice(0, 12), []);
});
check('at most one lesson link on the Simpler line and one on the Deeper line', () => {
  for (const x of sentences) for (const [k, segs] of x.lines) assert.ok(segs.filter((s) => s.href).length <= 1, `${x.l.slug} ${k}`);
});
check('a hop link never points at the lesson itself, and carries where the reader came from', () => {
  for (const x of sentences) for (const [, segs] of x.lines) for (const s of segs.filter((y) => y.href)) {
    assert.ok(!s.href.startsWith(`/lessons/${x.l.slug}/`), x.l.slug);
    assert.ok(s.href.endsWith(`?from=${x.l.slug}`), x.l.slug);
  }
});
const target = (segs) => { const link = segs.find((y) => y.href); return link ? site.lessons.get(link.href.split('/')[2]) : undefined; };
check('Simpler points to a lower level and Deeper to a higher one', () => {
  for (const x of sentences) for (const [k, segs] of x.lines) {
    const t = target(segs);
    if (t && k === 'simpler') assert.ok(t.rank < x.l.rank, `${x.l.slug} simpler`);
    if (t && (k === 'deeper' || k === 'next')) assert.ok(t.rank > x.l.rank, `${x.l.slug} ${k}`);
  }
});
check('a link chosen by hand wins: the school ladders, the step up from a guide, the way back from college', () => {
  let n = 0;
  for (const x of sentences) for (const [dir, key] of [['down', 'simpler'], ['up', x.l.rank === 0 ? 'next' : 'deeper']]) {
    const mine = x.authored[dir];
    if (!mine.length || (x.l.rank === 0 && mine.every((m) => m.rank > 2))) continue;
    const line = x.lines.find(([k]) => k === key);
    assert.ok(line, `${x.l.slug}: a hand-picked ${dir} link exists but the ${key} line is missing`);
    assert.ok(mine.some((m) => m.slug === target(line[1])?.slug), `${x.l.slug} ${key}: ${line[2]} is not one of the hand-picked ${mine.map((m) => m.slug)}`);
    n++;
  }
  assert.ok(n > 150, `only ${n} hand-picked sides were checked`);
});
check('the sentence and the ladder agree: every lesson the sentence names is on the named idea\u2019s ladder, or drawn on it as picked by hand', () => {
  for (const x of sentences) {
    const main = x.s.ideas[0];
    const rungs = new Set(api.ladder(main.id).map((r) => r.slug));
    for (const [k, segs, text] of x.lines) {
      const t = target(segs);
      if (!t) continue;
      assert.ok(rungs.has(t.slug) || x.s.also.some((a) => a.slug === t.slug), `${x.l.slug} ${k}: ${text} is not on the ladder of ${main.id}`);
      assert.ok(!/^(Simpler|Deeper), for /.test(text), `${x.l.slug} ${k}: no link to another idea's lesson: ${text}`);
      const dir = k === 'simpler' ? 'down' : 'up';
      if (!x.authored[dir].length) assert.equal(t.slug, main[dir].slug, `${x.l.slug} ${k}: the nearest rung of ${main.id}`);
    }
  }
});
check('among hand-picked links at the nearest level, one on the named idea\u2019s ladder is preferred', () => {
  for (const x of sentences) for (const [dir, key] of [['down', 'simpler'], ['up', 'deeper']]) {
    const line = x.lines.find(([k]) => k === key); const t = line && target(line[1]);
    if (!t || !x.authored[dir].length) continue;
    const rungs = new Set(api.ladder(x.s.ideas[0].id).map((r) => r.slug));
    const sameLevel = x.authored[dir].filter((a) => a.rank === t.rank);
    if (sameLevel.some((a) => rungs.has(a.slug))) assert.ok(rungs.has(t.slug), `${x.l.slug} ${key}: ${line[2]}`);
  }
});
check('the level is always said: the lesson\u2019s own, and each linked lesson\u2019s in brackets', () => {
  const lvl = new RegExp(`\\((${LEVEL_SHORT.join('|')}|a hands-on activity)[;,)]`);
  for (const x of sentences) {
    if (x.l.rank > 0) assert.match(x.lines[0][2], /grade 7|high school|college|graduate/, x.l.slug);
    for (const [k, segs, text] of x.lines) if (target(segs)) assert.match(text, lvl, `${x.l.slug} ${k}`);
  }
});
check('the sentence never says "nothing at a level" when the page links a lesson there', () => {
  for (const x of sentences) for (const [, , text] of x.lines) {
    const m = /nothing (at grade 7|at high school|at college level) yet/.exec(text);
    if (!m) continue;
    const band = { 'at grade 7': [1], 'at high school': [2], 'at college level': [3, 4, 5] }[m[1]];
    const there = [...api.hops(x.l.slug).flatMap((i) => [...i.downAll, ...i.upAll]), ...x.authored.down, ...x.authored.up].filter((r) => band.includes(r.rank));
    assert.deepEqual(there.map((r) => r.slug), [], `${x.l.slug}: ${text}`);
  }
});
check('ages 5 to 10: an activity, one next lesson, taken from the guide\u2019s own step up when it has one', () => {
  for (const x of sentences.filter((y) => y.l.rank === 0)) {
    assert.match(x.lines[0][2], /^An activity for ages 5 to 10 about .+\.$/);
    assert.ok(!x.s.lines.simpler && !x.s.lines.deeper, x.l.slug);
    if (x.s.lines.next) assert.match(plain(x.s.lines.next), /^Next, for an older child: .+ \((grade 7|high school)\)\.$/);
    const step = (x.l.activity?.stepUp ?? []).filter((s) => site.lessons.has(s));
    if (step.length) assert.ok(step.includes(target(x.s.lines.next)?.slug), `${x.l.slug}: the next lesson is not in its step up`);
  }
});
check('a side with no lesson is left out, never printed as "none"', () => {
  for (const x of sentences) for (const [, , text] of x.lines) assert.ok(!/no lesson yet|none yet/i.test(text), `${x.l.slug}: ${text}`);
});
check('the short version offered in place exists in that lesson', () => {
  for (const x of sentences) {
    const q = x.lines.flatMap(([, segs]) => segs).find((s) => s.quick);
    if (q) { assert.ok(x.l.fm.explainLevels.some((e) => e.level === q.quick), x.l.slug); assert.ok(QUICK_NAME[q.quick], q.quick); }
    if (x.l.rank >= 2) assert.ok(q, `${x.l.slug}: a lesson from high school up offers its short simpler version in place`);
  }
});
check('one idea is named: the lesson\u2019s main idea, the first in the graph\u2019s record, by its short name', () => {
  for (const x of sentences) {
    assert.equal(x.s.ideas[0].id, graph.lessons[x.l.slug].concepts.find((id) => graph.concepts[id].rungs.some((r) => r.lesson === x.l.slug && r.role === 'core')), x.l.slug);
    const c = graph.concepts[x.s.ideas[0].id];
    assert.ok(x.lines[0][2].toLowerCase().includes(inSentence(x.s.ideas[0].id, c.short ?? c.name).toLowerCase()), `${x.l.slug}: ${x.lines[0][2]}`);
    assert.ok(!/ and also |more idea/.test(x.lines[0][2]), x.l.slug);
  }
});
check('school lessons name their level; college lessons name their course', () => {
  for (const x of sentences) {
    if (x.l.rank >= 3 && x.s.tight < 3) assert.ok(x.lines[0][2].includes(` in ${x.l.courseTitle}`), x.l.slug);
    else if (x.l.rank > 0 && x.l.rank <= 2) assert.ok(x.lines[0][2].endsWith(`${LEVEL_SHORT[x.l.rank]} level.`), x.l.slug);
  }
});
check(`the closed sentence fits four phone lines: at most ${SENTENCE_MAX} characters in all`, () => {
  const long = sentences.filter((x) => x.s.length > SENTENCE_MAX).map((x) => `${x.l.slug} (${x.s.length}): ${x.lines.map((l) => l[2]).join(' ')}`);
  assert.deepEqual(long, []);
});

console.log(`ideas: ${api.concepts.length}`);
const joined = (id) => { const c = api.concept(id); return { id, name: c.name, short: inSentence(id, c.short ?? c.name), rungs: api.ladder(id) }; };
check('every idea draws a ladder: a rung per level, every lesson on it, nothing locked or counted', () => {
  for (const c of api.concepts) {
    const idea = joined(c.id);
    if (!idea.rungs.length) continue;
    const ranks = [...new Set(idea.rungs.map((r) => r.rank))];
    const mask = maskOf(ranks);
    assert.deepEqual(faults(taughtAt(mask)), [], c.id);
    assert.ok(levelCount(mask), c.id);
    const html = ladderHtml(idea);
    assert.equal((html.match(/class="hl-rung"/g) ?? []).length, ranks.length, `${c.id}: one rung per level`);
    assert.equal((html.match(/class="hl-lesson/g) ?? []).length, idea.rungs.length, `${c.id}: every lesson is on its rung`);
    assert.ok(!/class="hl-hex"|hl-windowed|hl-far|disabled|aria-disabled/.test(html), `${c.id}: no Hex without a reader, no rung folded or switched off`);
    for (const row of ladderRows(idea).filter((r) => r.kind === 'gap')) assert.deepEqual(faults(row.text), [], c.id);
    const glyph = ladderGlyph(mask, { here: ranks[0], size: 'tiny' });
    assert.equal((glyph.match(/hl-rung/g) ?? []).length, ranks.length, c.id);
    assert.ok(glyph.includes('aria-hidden="true"') && !glyph.includes('role="img"'), 'the mark is a picture only');
  }
});
check('Hex stands on the reader’s rung, once, and that lesson is not a link to itself', () => {
  const html = ladderHtml(joined('osmosis'), { here: 'crossing-the-membrane' });
  assert.equal((html.match(/class="hl-hex"/g) ?? []).length, 1);
  assert.match(html, /hl-here[^>]*data-hop-level="high-school"/);
  assert.ok(html.includes('<strong>Crossing the Membrane</strong>') && !html.includes('href="/lessons/crossing-the-membrane/'));
  assert.ok(html.includes('/lessons/diffusion-and-osmosis/?from=crossing-the-membrane'), 'other rungs carry where the reader came from');
  assert.ok(!ladderHtml(joined('osmosis'), { here: 'crossing-the-membrane', hex: false }).includes('class="hl-hex"'), 'a second ladder in view draws no second Hex');
});
check('on a lesson the ladder opens on the reader’s rung and the nearest rung each way', () => {
  const idea = joined('osmosis');
  const html = ladderHtml(idea, { here: 'diffusion-and-osmosis' });
  const levels = [...new Set(idea.rungs.map((r) => r.rank))].length;
  assert.ok(levels >= 4, 'osmosis has four levels');
  assert.ok(html.includes('hl-windowed') && html.includes('data-hl-all'));
  assert.equal((html.match(/hl-level hl-far/g) ?? []).length, levels - 2, 'the lowest rung shows itself and the one above');
  const mid = ladderHtml(idea, { here: 'crossing-the-membrane' });
  assert.ok(/hl-here"[^>]*data-hop-level="high-school"/.test(mid) && /hl-level" data-hop-level="grade-7"/.test(mid), 'from high school: this rung and the simpler one below it');
  assert.ok(mid.indexOf('data-hop-level="high-school"') < mid.indexOf('data-hop-level="grade-7"'), 'written as drawn: deeper rungs first');
  assert.ok(mid.includes('aria-expanded="false"') && mid.includes('data-fewer="Show fewer levels"'), 'the button stays and says what it will do');
  assert.ok(!ladderHtml(joined('nerve-growth-factor'), { here: api.ladder('nerve-growth-factor')[0].slug }).includes('hl-windowed'), 'a one-rung ladder has nothing to fold');
});
check('a gap is one short row; college counts as one place', () => {
  const rows = ladderRows({ short: 'touch', name: 'Touch', rungs: [{ rank: 0 }, { rank: 5 }, { rank: 6 }] });
  assert.deepEqual(rows.map((r) => r.kind), ['level', 'gap', 'level', 'level']);
  assert.equal(rows[1].text, 'No lesson on touch at grade 7 or at high school yet.');
  const covered = ladderRows({ short: 'touch', name: 'Touch', rungs: [{ rank: 0 }, { rank: 5 }] }, [1]);
  assert.equal(covered[1].text, 'No lesson on touch at high school yet.', 'a level the page links by hand is not called empty');
  assert.deepEqual(ladderRows({ name: 'x', rungs: [{ rank: 0 }, { rank: 2 }] }, [1]).map((r) => r.kind), ['level', 'level']);
  assert.deepEqual(ladderRows({ name: 'x', rungs: [{ rank: 3 }, { rank: 5 }] }).map((r) => r.kind), ['level', 'level']);
});
check('"Play the ladder" states its size and its end', () => {
  const html = ladderHtml(joined('osmosis'), { play: { href: '/watch/x/?idea=osmosis', n: 4, minutes: 13, from: 1, to: 5 } });
  assert.ok(html.includes('Play the ladder</a><span> · 4 films, about 13 min, from grade 7 to upper-level college.'));
});
check('level labels: seven, none ranks a reader', () => {
  assert.equal(LEVEL_SHORT.length, 7); assert.equal(LEVEL_LABEL.length, 7);
  assert.equal(andList(['a']), 'a'); assert.equal(andList(['a', 'b', 'c']), 'a, b and c');
});

console.log('search');
const index = buildIndex(api.clientIndex(), { lessons: lessons.map((l) => [l.slug, l.title, l.rank, l.ladder?.sol ?? l.activity?.sol ?? [], l.unit ?? '']) });
const top = (q, n = 1) => search(index, q).results.slice(0, n).map((r) => r.id);
const FIXTURES = [
  // [query, an id that must be first, or a list of which one must be first]
  ['osmosis', 'osmosis'], ['Osmosis', 'osmosis'], ['osmosis grade 7', 'osmosis'], ['what is osmosis', 'osmosis'],
  ['why does salt make cucumbers wet', 'osmosis'], ['osmossis', 'osmosis'], ['omsosis', 'osmosis'],
  ['photosynthesis', 'photosynthesis'], ['photosynthsis', 'photosynthesis'], ['why are leaves green', ['leaf-pigments', 'photosynthesis']],
  ['how do vaccines work', 'immunity'], ['action potential', 'action-potential'], ['action potentials', 'action-potential'],
  ['synapses', 'synapse'], ['viruses', 'viruses'], ['virus', 'viruses'], ['enzyme', 'enzymes'], ['mitochondria', ['cellular-respiration', 'endosymbiosis', 'organelles', 'chemiosmosis']],
  ['cell membrane', 'cell-membrane'], ['osmo', 'osmosis'], ['dna', 'dna-structure'], ['natural selection', 'natural-selection'], ['colour vision', 'colour-vision'], ['color vision', 'colour-vision'],
  ['hemoglobin', 'oxygen-transport'], ['haemoglobin', 'oxygen-transport'], ['mitosis', 'cell-division'], ['PCR', 'pcr'], ['crispr', 'genetic-engineering'],
  ['heart', 'circulation'], ['food web', 'food-webs'], ['pain', 'pain'], ['atp', 'atp'], ['evolution', ['natural-selection', 'evidence-for-evolution', 'regulatory-evolution', 'coevolution']],
];
check(`ranking on ${FIXTURES.length} fixtures`, () => {
  const bad = [];
  for (const [q, want] of FIXTURES) {
    const got = top(q)[0];
    if (!(Array.isArray(want) ? want : [want]).includes(got)) bad.push(`"${q}" -> ${top(q, 3).join(', ') || '(nothing)'}; wanted ${want}`);
  }
  assert.deepEqual(bad, []);
});
check('every idea is found first by its own name', () => {
  const bad = api.concepts.filter((c) => api.ladder(c.id).length && top(c.name)[0] !== c.id).map((c) => `${c.name} -> ${top(c.name)[0]}`);
  assert.deepEqual(bad, []);
});
check('nine in ten everyday phrases find their idea in the first three results', () => {
  let n = 0, hit = 0; const miss = [];
  for (const c of api.concepts) for (const a of c.aliases) { n++; if (top(a, 3).includes(c.id)) hit++; else miss.push(`${a} -> ${top(a, 3).join(', ')} (wanted ${c.id})`); }
  assert.ok(hit / n >= 0.9, `${hit} of ${n}\n${miss.slice(0, 15).join('\n')}`);
});
check('a lesson title finds the ideas that lesson teaches, and says which lesson', () => {
  let n = 0, hit = 0;
  for (const l of lessons) {
    const mine = Object.entries(graph.concepts).filter(([, c]) => c.rungs.some((r) => r.lesson === l.slug && r.role === 'core')).map(([id]) => id);
    if (!mine.length) continue;
    n++; if (search(index, l.title).results.slice(0, 4).some((r) => mine.includes(r.id))) hit++;
  }
  assert.ok(hit / n >= 0.95, `${hit} of ${n}`);
});
check('a standards code finds the lessons that carry it', () => {
  assert.equal(solCode('BIO.3d'), 'bio3d'); assert.equal(solCode('ls 2 e'), 'ls2e'); assert.equal(solCode('LS.2'), 'ls2'); assert.equal(solCode('osmosis'), ''); assert.equal(solCode('3 5'), '');
  const withCode = lessons.find((l) => l.ladder?.sol?.length);
  const res = search(index, withCode.ladder.sol[0]);
  assert.ok(res.code && res.results.length > 0);
  assert.ok(res.results.every((r) => r.why.kind === 'code'));
  assert.ok(res.results.some((r) => r.why.slug === withCode.slug), `${withCode.ladder.sol[0]} should find ${withCode.slug}`);
});
check('nonsense finds nothing; a loose match is marked closest, not passed off as an answer', () => {
  assert.deepEqual(search(index, 'zxqv blorp').results, []);
  assert.deepEqual(search(index, '   ').results, []);
  assert.deepEqual(search(index, 'quantum chromodynamics').results.filter((r) => !r.closest), []);
  assert.ok(search(index, 'osmosis').results[0].exact && !search(index, 'osmosis').results[0].closest);
  assert.ok(!search(index, 'osmo').results[0].closest, 'the start of a name is a match, not a near miss');
});
check('plurals and slips', () => {
  assert.equal(stem('cells'), 'cell'); assert.equal(stem('viruses'), 'virus'); assert.equal(stem('bodies'), 'body'); assert.equal(stem('synapses'), 'synapse'); assert.equal(stem('mitosis'), 'mitosis'); assert.equal(stem('glass'), 'glass');
  assert.ok(oneSlip('osmosis', 'osmossis') && oneSlip('omsosis', 'osmosis') && oneSlip('enzyme', 'enzime') && !oneSlip('mitosis', 'meiosis1') && !oneSlip('cell', 'wall'));
});
check('a search is quick: under 15 ms on average over 200 queries', () => {
  const qs = FIXTURES.map((f) => f[0]);
  const t = performance.now();
  for (let i = 0; i < 200; i++) search(index, qs[i % qs.length]);
  const each = (performance.now() - t) / 200;
  assert.ok(each < 15, `${each.toFixed(2)} ms`);
});

console.log(process.exitCode ? '\nhop tests FAILED' : `\nhop tests passed (${passed})`);
