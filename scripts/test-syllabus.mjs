#!/usr/bin/env node
/**
 * The mini syllabus (/start/) and the teacher's syllabus matcher (/teach/match/): the shared
 * matcher (src/lib/syllabus-match.mjs), the path builder, the Word reader and the assignment
 * merge, against the committed hop graph and lessons. Runs from source; needs no build, no
 * network and no model.
 *
 *   node scripts/test-syllabus.mjs            the tests (also in CI)
 *   node scripts/test-syllabus.mjs --print    every miss and wrong match in the fixtures, for reading
 *
 * The bars below are floors, set a little under what the matcher scores today. Two of the four
 * sets (HELD_OUT, SYLLABI_HELD_OUT) were written after tuning and are never tuned against: they
 * say how words nobody has seen will fare. A wrong match costs more than a missing one, so the
 * precision floors are the strict ones.
 */
import assert from 'node:assert/strict';
import { readFileSync } from 'node:fs';
import { deflateRawSync } from 'node:zlib';
import { loadGraphSite, coreSite, readGraph, makeTopicGraph } from './topic-graph/lib.mjs';
import { buildMatcher, matchQuestion, matchTopic, matchSyllabus, parseSyllabus, cleanTopic, splitTopics, pickRungs, defaultLevel, rootOf, needsHelp, SURE, LEVEL_AT, LEVEL_CLASS } from '../src/lib/syllabus-match.mjs';
import { SYNONYMS } from '../src/lib/syllabus-synonyms.mjs';
import { ideaFromArea, buildPath, levelFor, timeFrom, MAX_STEPS } from '../src/lib/start-path.mjs';
import { docxText, documentXmlToText } from '../src/lib/docx-text.mjs';
import { mergeAssignments, MAX_ASSIGNMENTS } from '../src/lib/syllabus-assign.mjs';
import { QUESTIONS, HELD_OUT, SYLLABI, SYLLABI_HELD_OUT, PANEL_QUESTIONS, PANEL_SENSITIVE, PANEL_SYLLABI, R2_HELP, R2_BIOLOGY, R2_QUESTIONS, R2_SYLLABI } from './test-syllabus-fixtures.mjs';
import { HELP, withNumbers } from '../src/lib/start-help.mjs';

const PRINT = process.argv.includes('--print');
let passed = 0;
const pending = [];
const check = (name, fn) => pending.push(async () => { try { await fn(); passed++; console.log(`  ok  ${name}`); } catch (e) { console.log(`  FAIL ${name}\n${e.message ?? e}`); process.exitCode = 1; } });

const site = await loadGraphSite();
const graph = readGraph();
const api = makeTopicGraph(graph, coreSite(site));
const lessons = [...site.lessons.values()];
const links = JSON.parse(readFileSync('src/data/lesson-links.json', 'utf8')).lessons;
// The three files the browser fetches, built here from the same sources.
const graphIndex = api.clientIndex();
const lessonFile = { lessons: lessons.map((l) => [l.slug, l.title, l.rank, l.ladder?.sol ?? l.activity?.sol ?? [], l.unit ?? '']) };
const extra = { lessons: Object.fromEntries(lessons.map((l) => [l.slug, [30, l.rank === 0 ? 0 : 3, links[l.slug]?.search ?? []]])) };
const m = buildMatcher(graphIndex, lessonFile, extra);

// ------------------------------------------------------------------ a learner's question
function scoreQuestions(set) {
  let n = 0, top1 = 0, top3 = 0, none = 0, noneOk = 0;
  const miss = [], wrong = [];
  for (const [q, want] of set) {
    const r = matchQuestion(m, q);
    const ids = r.kind === 'match' ? r.ideas.map((x) => x.id) : [];
    if (!want.length) { none++; if (r.kind !== 'match') noneOk++; else wrong.push(`"${q}" -> ${ids[0]} (the honest answer is nothing)`); continue; }
    n++;
    if (want.includes(ids[0])) top1++;
    if (ids.slice(0, 3).some((i) => want.includes(i))) top3++; else miss.push(`"${q}" -> ${ids.slice(0, 3).join(', ') || `(${r.kind})`}; wanted ${want.join(' | ')}`);
  }
  return { n, top1, top3, none, noneOk, miss, wrong };
}
const pct = (a, b) => `${a}/${b} = ${(a / b * 100).toFixed(1)}%`;

console.log('a learner\'s question');
check(`${QUESTIONS.length} questions: top-1 at least 93%, top-3 at least 96%, and never a confident answer where the site has none`, () => {
  const s = scoreQuestions(QUESTIONS);
  console.log(`      top-1 ${pct(s.top1, s.n)}, top-3 ${pct(s.top3, s.n)}, honest "nothing" ${pct(s.noneOk, s.none)}`);
  if (PRINT) [...s.miss, ...s.wrong].forEach((x) => console.log(`      ${x}`));
  assert.ok(QUESTIONS.length >= 60);
  assert.ok(s.top1 / s.n >= 0.93, `top-1 ${pct(s.top1, s.n)}\n${s.miss.join('\n')}`);
  assert.ok(s.top3 / s.n >= 0.96, `top-3 ${pct(s.top3, s.n)}\n${s.miss.join('\n')}`);
  assert.deepEqual(s.wrong, []);
});
check(`${HELD_OUT.length} held-out questions: top-1 at least 80%, top-3 at least 85%, at most one confident wrong answer`, () => {
  const s = scoreQuestions(HELD_OUT);
  console.log(`      top-1 ${pct(s.top1, s.n)}, top-3 ${pct(s.top3, s.n)}, honest "nothing" ${pct(s.noneOk, s.none)}`);
  if (PRINT) [...s.miss, ...s.wrong].forEach((x) => console.log(`      ${x}`));
  assert.ok(s.top1 / s.n >= 0.8, `top-1 ${pct(s.top1, s.n)}`);
  assert.ok(s.top3 / s.n >= 0.85, `top-3 ${pct(s.top3, s.n)}`);
  assert.ok(s.wrong.length <= 1, s.wrong.join('\n'));
});
check(`the review panel's ${PANEL_QUESTIONS.length} questions (PANEL), and its ${PANEL_SENSITIVE.length} questions about health, feelings and the body`, () => {
  const s = scoreQuestions(PANEL_QUESTIONS);
  // A confident answer that is not a right one: the costly kind.
  const confident = PANEL_QUESTIONS.filter(([q, want]) => { const r = matchQuestion(m, q); return r.kind === 'match' && !want.includes(r.ideas[0].id); }).map(([q]) => `"${q}" -> ${matchQuestion(m, q).ideas[0].id}`);
  // Questions about the asker's own health, feelings or body are matched like any other: a lesson only
  // when the words really name a biology idea, and never one that merely shares a word.
  const OK = { 'why do I have a period': ['menstrual-cycle'], 'do vaccines cause autism': ['immunity', 'germ-theory'], 'are GMOs safe': ['genetic-engineering'], 'how do I hurt myself': [] };
  const body = PANEL_SENSITIVE.map((q) => [q, matchQuestion(m, q)]);
  const odd = body.filter(([q, r]) => (r.kind === 'match' || r.kind === 'closest') && !r.ideas.every((x) => (OK[q] ?? []).includes(x.id))).map(([q, r]) => `"${q}" -> ${r.kind} ${r.ideas.map((x) => x.id).join(', ')}`);
  console.log(`      top-1 ${pct(s.top1, s.n)}, top-3 ${pct(s.top3, s.n)}, honest "nothing" ${pct(s.noneOk, s.none)}, confident wrong ${confident.length} of ${PANEL_QUESTIONS.length}; body and feelings questions given an unrelated lesson or suggestion: ${odd.length} of ${PANEL_SENSITIVE.length}`);
  if (PRINT) [...confident.map((x) => `confident wrong ${x}`), ...s.miss.map((x) => `missed ${x}`), ...odd].forEach((x) => console.log(`      ${x}`));
  assert.deepEqual(odd, []);
  assert.equal(matchQuestion(m, 'how do I hurt myself').kind, 'help');
  assert.ok(confident.length <= 1, confident.join('\n'));
  assert.ok(s.noneOk / s.none >= 0.95, `honest nothing ${pct(s.noneOk, s.none)}`);
  assert.ok(s.top3 / s.n >= 0.6, `top-3 ${pct(s.top3, s.n)}`);
});
check(`round 2 of the review: ${R2_HELP.length} sentences that ask for help, ${R2_BIOLOGY.length} biology questions that must not be refused, ${R2_QUESTIONS.length} questions (R2)`, () => {
  // Wording that is plainly about self-harm, abuse or danger: the help message, never a lesson. The
  // detector was widened on these very sentences, so its rate here says little about new wording; what
  // the page relies on for wording it misses is the permanent help line, checked further down.
  const res = R2_HELP.map((q) => [q, matchQuestion(m, q)]);
  const caught = res.filter(([, r]) => r.kind === 'help').length;
  const lesson = res.filter(([, r]) => r.kind === 'match' || r.kind === 'closest').map(([q, r]) => `"${q}" -> ${r.kind} ${r.ideas[0]?.id}`);
  // Biology that mentions the body, health, sex, drugs or death is biology.
  const refused = R2_BIOLOGY.filter((q) => needsHelp(q) || matchQuestion(m, q).kind === 'help');
  const s = scoreQuestions(R2_QUESTIONS);
  // An answer found through a lesson's own search phrase is that lesson, which the page shows as such.
  const confident = R2_QUESTIONS.filter(([q, want]) => { const r = matchQuestion(m, q); return r.kind === 'match' && !want.includes(r.ideas[0].id) && !r.ideas[0].viaLesson; }).map(([q]) => `"${q}" -> ${matchQuestion(m, q).ideas[0].id}`);
  const byLesson = R2_QUESTIONS.filter(([q, want]) => { const r = matchQuestion(m, q); return r.kind === 'match' && !want.includes(r.ideas[0].id) && r.ideas[0].viaLesson; }).length;
  console.log(`      help wording caught ${pct(caught, R2_HELP.length)}, given a lesson instead ${lesson.length}; biology refused ${refused.length} of ${R2_BIOLOGY.length}; questions top-1 ${pct(s.top1, s.n)}, confident wrong ${confident.length} of ${R2_QUESTIONS.length} (${byLesson} more answered with the one lesson that carries those words), honest "nothing" ${pct(s.noneOk, s.none)}`);
  if (PRINT) [...lesson, ...refused.map((q) => `refused: ${q}`), ...confident.map((x) => `confident wrong ${x}`), ...s.miss.map((x) => `missed ${x}`)].forEach((x) => console.log(`      ${x}`));
  assert.deepEqual(lesson, [], 'a sentence that asks for help was answered with a lesson');
  assert.ok(caught / R2_HELP.length >= 0.9, pct(caught, R2_HELP.length));
  assert.deepEqual(refused, []);
  assert.ok(confident.length <= 1, confident.join('\n'));
});
check('nothing typed, or nonsense, is no match; a loose match is "closest", never an answer', () => {
  assert.equal(matchQuestion(m, '').kind, 'none');
  assert.equal(matchQuestion(m, '   ').kind, 'none');
  assert.equal(matchQuestion(m, 'zxqv blorp').kind, 'none');
  assert.equal(matchQuestion(m, 'the of and').kind, 'none');
  for (const [q] of QUESTIONS) { const r = matchQuestion(m, q); if (r.kind === 'closest') assert.ok(r.ideas.every((x) => !x.sure), q); if (r.kind === 'match') assert.ok(r.ideas[0].score >= SURE, q); }
});
check('every idea is found first by its own name, and nine in ten everyday phrases find their idea in the first three', () => {
  const bad = api.concepts.filter((c) => api.ladder(c.id).length && matchQuestion(m, c.name).ideas[0]?.id !== c.id).map((c) => `${c.name} -> ${matchQuestion(m, c.name).ideas[0]?.id}`);
  assert.ok(bad.length <= 4, bad.join('\n'));
  let n = 0, hit = 0;
  for (const c of api.concepts) { if (!api.ladder(c.id).length) continue; for (const a of c.aliases) { n++; if (matchQuestion(m, a).ideas.slice(0, 3).some((r) => r.id === c.id)) hit++; } }
  console.log(`      everyday phrases: ${pct(hit, n)}`);
  assert.ok(hit / n >= 0.9, pct(hit, n));
});
check('the help detector is narrow: plain self-harm, abuse or danger wording only', () => {
  for (const q of ['how do I hurt myself', 'i want to die', 'my dad hits me', 'kms', 'someone touched my private parts']) assert.equal(needsHelp(q), true, q);
  for (const q of ['programmed cell death', 'why do cells kill themselves', 'long-term depression at synapses', 'how does a virus kill a cell', 'what kills bacteria', 'why do leaves die in the fall', 'how do antibiotics hurt bacteria', 'how do vaccines work', 'am i fat', 'is vaping safe', 'what is sex', 'why am i so anxious', 'does it hurt when a tooth falls out', 'how do pills dissolve', 'do plants feel pain when you cut them', 'what happens when we stop breathing', 'predators and prey', 'antibiotic resistance']) assert.equal(needsHelp(q), false, q);
  for (const [q] of [...QUESTIONS, ...HELD_OUT, ...PANEL_QUESTIONS, ...R2_QUESTIONS]) assert.equal(needsHelp(q), false, `"${q}" is an ordinary question`);
  const r = matchQuestion(m, 'i want to kill myself');
  assert.deepEqual([r.kind, r.ideas.length], ['help', 0]);
  // In a syllabus the health-class units are set aside, and nothing is suggested for them.
  for (const t of ['reproductive system & puberty', 'drugs and alcohol', 'sex education unit']) assert.deepEqual(matchTopic(m, t), { ideas: [], maybe: [] }, t);
  assert.ok(matchTopic(m, 'Reward, dopamine and addiction').ideas.length, 'a neuroscience line is not a health unit');
});
check('one common word, or half of a compound name, never decides', () => {
  for (const q of ['genes and environment', 'muscle force and speed']) assert.equal(matchQuestion(m, q).kind, 'match', q);
  for (const q of ['power', 'speed', 'resistance', 'environment', 'size', 'learning', 'repair']) assert.notEqual(matchQuestion(m, q).kind, 'match', q);
  assert.notEqual(matchQuestion(m, 'plants and animals').ideas[0]?.id, 'animal-body-plans', '"plants" is not a slip of "plans"');
  for (const [q, not] of [['why are my eyes blue', 'vision'], ['lung cancer', 'breathing'], ['fossil fuels', 'evidence-for-evolution'], ['carrier of sickle cell', 'active-transport']]) {
    const r = matchQuestion(m, q);
    assert.ok(!(r.kind === 'match' && r.ideas[0].id === not), `"${q}" is answered as ${not}`);
  }
  // In a syllabus: one known word among words the site does not know is not a match; "secretion" is not the secretory pathway.
  assert.deepEqual(matchTopic(m, "Earth's changing surface: weathering, erosion, plate tectonics").ideas, []);
  for (const t of ['GI motility and secretion; absorption', 'Kidney: secretion and reabsorption', 'Water, pH and buffers']) assert.ok(!matchTopic(m, t).ideas.some((x) => x.id === 'secretory-pathway' || x.id === 'body-water-compartments'), t);
});
check('two ideas asked for at once are both in the answer', () => {
  const r = matchQuestion(m, 'photosynthesis and cellular respiration');
  assert.equal(r.together, 2);
  assert.deepEqual(r.ideas.slice(0, 2).map((x) => x.id).sort(), ['cellular-respiration', 'photosynthesis']);
});
check('words: roots meet, slips are forgiven, the textbook names point at real ideas', () => {
  assert.equal(rootOf('immunity'), rootOf('immune'));
  assert.equal(rootOf('vaccines'), rootOf('vaccination'));
  assert.notEqual(rootOf('flower'), rootOf('flow'));
  assert.equal(matchQuestion(m, 'photosynthsis').ideas[0].id, 'photosynthesis');
  const unknown = Object.keys(SYNONYMS).filter((id) => !graph.concepts[id]);
  assert.deepEqual(unknown, [], 'syllabus-synonyms.mjs names ideas that are not in the graph');
  for (const [id, list] of Object.entries(SYNONYMS)) for (const s of list) assert.ok(s.trim().length > 1 && s.length <= 60, `${id}: "${s}"`);
});

// ------------------------------------------------------------------ a syllabus
function scoreSyllabi(set) {
  let right = 0, wrong = 0, want = 0, hit = 0;
  const bad = [], missed = [], lost = [];
  for (const s of set) {
    const res = matchSyllabus(m, s.text, s.level);
    const used = new Set();
    for (const row of res.rows) {
      const lab = s.lines.filter(([k]) => row.raw.includes(k)).sort((a, b) => b[0].length - a[0].length)[0];
      if (lab) used.add(lab[0]);
      const ok = lab ? lab[1] : [];
      // A lesson found by its own title is right when that lesson teaches one of the listed ideas.
      const teaches = (x) => x.why.kind === 'lesson' && (m.coreOf[x.why.slug] ?? []).some((ci) => ok.includes(m.ideas[ci].id));
      const off = row.ideas.filter((x) => !ok.includes(x.id) && !teaches(x));
      right += row.ideas.length - off.length; wrong += off.length;
      for (const x of off) bad.push(`${s.name}: "${row.topic}" -> ${x.id} (on ${x.why.kind} "${x.why.text}")`);
      if (ok.length) { want++; if (row.ideas.length > off.length) hit++; else missed.push(`${s.name}: "${row.topic}"`); }
    }
    for (const [k] of s.lines) if (!used.has(k)) lost.push(`${s.name}: the line "${k}" did not become a row`);
  }
  return { right, wrong, want, hit, bad, missed, lost };
}
console.log('a syllabus');
check(`${SYLLABI.length} syllabi: at least 97% of matches right, and at least 93% of topics the site covers get a right match`, () => {
  const s = scoreSyllabi(SYLLABI);
  console.log(`      precision ${pct(s.right, s.right + s.wrong)}, topics matched ${pct(s.hit, s.want)}`);
  if (PRINT) [...s.bad.map((x) => `wrong  ${x}`), ...s.missed.map((x) => `missed ${x}`)].forEach((x) => console.log(`      ${x}`));
  assert.ok(SYLLABI.length >= 8);
  assert.deepEqual(s.lost, []);
  assert.ok(s.right / (s.right + s.wrong) >= 0.97, `precision ${pct(s.right, s.right + s.wrong)}\n${s.bad.join('\n')}`);
  assert.ok(s.hit / s.want >= 0.93, `matched ${pct(s.hit, s.want)}\n${s.missed.join('\n')}`);
});
check(`${SYLLABI_HELD_OUT.length} held-out syllabi: at least 92% of matches right, at least 80% of covered topics matched`, () => {
  const s = scoreSyllabi(SYLLABI_HELD_OUT);
  console.log(`      precision ${pct(s.right, s.right + s.wrong)}, topics matched ${pct(s.hit, s.want)}`);
  if (PRINT) [...s.bad.map((x) => `wrong  ${x}`), ...s.missed.map((x) => `missed ${x}`)].forEach((x) => console.log(`      ${x}`));
  assert.deepEqual(s.lost, []);
  assert.ok(s.right / (s.right + s.wrong) >= 0.92, `precision ${pct(s.right, s.right + s.wrong)}\n${s.bad.join('\n')}`);
  assert.ok(s.hit / s.want >= 0.8, `matched ${pct(s.hit, s.want)}\n${s.missed.join('\n')}`);
});
check(`the review panel's ${PANEL_SYLLABI.length} syllabi (PANEL): no wrong match`, () => {
  const s = scoreSyllabi(PANEL_SYLLABI);
  console.log(`      precision ${pct(s.right, s.right + s.wrong)}, topics matched ${pct(s.hit, s.want)}`);
  if (PRINT) [...s.bad.map((x) => `wrong  ${x}`), ...s.missed.map((x) => `missed ${x}`), ...s.lost].forEach((x) => console.log(`      ${x}`));
  if (process.env.PANEL_BASELINE) return;
  assert.deepEqual(s.lost, []);
  assert.equal(s.wrong, 0, s.bad.join('\n'));
  assert.ok(s.hit / s.want >= 0.85, `matched ${pct(s.hit, s.want)}\n${s.missed.join('\n')}`);
});
check(`round 2 of the review: ${R2_SYLLABI.length} syllabi (R2): no wrong match, and science that looks like housekeeping is kept`, () => {
  const s = scoreSyllabi(R2_SYLLABI);
  console.log(`      precision ${pct(s.right, s.right + s.wrong)}, topics matched ${pct(s.hit, s.want)}`);
  if (PRINT) [...s.bad.map((x) => `wrong  ${x}`), ...s.missed.map((x) => `missed ${x}`), ...s.lost].forEach((x) => console.log(`      ${x}`));
  assert.deepEqual(s.lost, []);
  assert.equal(s.wrong, 0, s.bad.join('\n'));
  assert.ok(s.hit / s.want >= 0.85, `matched ${pct(s.hit, s.want)}\n${s.missed.join('\n')}`);
  const kindOf = (line) => matchSyllabus(m, `Week 1: Osmosis\nWeek 2: Enzymes\nWeek 3: Meiosis\nWeek 4: ${line}`, 2).rows[3];
  for (const line of ['Review of mitosis', 'Test crosses and dihybrid crosses', 'Buffer systems and pH', 'Final stages of meiosis', 'Welcome to the nervous system']) assert.equal(kindOf(line).kind, 'topic', line);
  for (const line of ['Unit test', 'TEST: Cells and energy', 'EXAM 1 (lectures 1-8)', 'Winter break', 'Review for final', 'Quiz on mitosis', 'Final exam, cumulative']) assert.deepEqual([kindOf(line).kind, kindOf(line).ideas.length], ['admin', 0], line);
  assert.ok(!matchTopic(m, 'Special senses: vision, hearing & balance').ideas.some((x) => x.id === 'speciation'));
  assert.ok(!matchTopic(m, 'Symbiosis (mutualism etc.)').ideas.some((x) => x.id === 'chemiosmosis'));
  assert.equal(rootOf('pollinate'), rootOf('pollination')); assert.equal(rootOf('circulated'), rootOf('circulation')); assert.notEqual(rootOf('special'), rootOf('speciation'));
});
check('the word matcher\'s failure does not come back: "Properties of water" is water, not ecosystems', () => {
  const r = matchTopic(m, 'Properties of water');
  assert.deepEqual(r.ideas.map((x) => x.id), ['properties-of-water']);
  for (const t of ['Properties of water', 'Water', 'The properties of water (2 days)']) {
    assert.ok(!matchTopic(m, t).ideas.some((x) => /ecosystem|water-cycle|nutrient-pollution|stream/.test(x.id)), t);
  }
});
check('housekeeping is never matched: exams, holidays, policies and contact lines', () => {
  const text = 'Mr. Okafor  okafor@example.org  Room 12\nGrading: tests 40%, labs 30%\nLate work loses 10% per day.\n\nWeek 1: Welcome, lab safety\nWeek 2: Osmosis\nWeek 3: Exam 1\nWeek 4: Thanksgiving break - no school\nWeek 5: Exam 2; meiosis\nWeek 6: Review for final';
  const res = matchSyllabus(m, text, 2);
  assert.deepEqual(res.rows.map((r) => [r.kind, r.ideas.map((x) => x.id).join(',')]), [['admin', ''], ['topic', 'osmosis'], ['admin', ''], ['admin', ''], ['topic', 'meiosis'], ['admin', '']]);
  assert.equal(res.skipped.length, 3);
  assert.equal(res.topics, 2);
  assert.equal(res.matched, 2);
});
check('rows keep the syllabus\'s own order and wording', () => {
  for (const s of [...SYLLABI, ...SYLLABI_HELD_OUT]) {
    const res = matchSyllabus(m, s.text, s.level);
    const at = res.rows.map((r) => s.text.replace(/\t+/g, ' | ').replace(/[  ]+/g, ' ').indexOf(r.raw.replace(/\s+/g, ' ')));
    assert.ok(at.every((x) => x >= 0), `${s.name}: a row is not a line of the syllabus`);
    assert.deepEqual(at, [...at].sort((a, b) => a - b), `${s.name}: rows are out of order`);
    assert.deepEqual(res.rows.map((r) => r.n), res.rows.map((_, i) => i));
  }
});
check('reading a line: week numbers, dates, chapters and standards codes come off; the topic stays', () => {
  assert.equal(cleanTopic('Week 3 (Sep 8-12): Cell membrane (Ch. 7) BIO.3'), 'Cell membrane');
  assert.equal(cleanTopic('Tue Sep 2 - Resting membrane potential'), 'Resting membrane potential');
  assert.equal(cleanTopic('10/8 | Cellular respiration'), 'Cellular respiration');
  assert.equal(cleanTopic('12. Feb 13  Microtubules, dynamic instability'), 'Microtubules, dynamic instability');
  assert.equal(cleanTopic('Unit 7  Meiosis and sexual reproduction'), 'Meiosis and sexual reproduction');
  assert.deepEqual(splitTopics('Mitosis and meiosis').map((f) => f[f.length - 1]), ['Mitosis', 'meiosis']);
  assert.ok(splitTopics('DNA replication and repair').some((f) => f.includes('dna repair')));
  assert.deepEqual(parseSyllabus('').rows, []);
  assert.deepEqual(parseSyllabus('just some words\n\n').rows.map((r) => r.topic), ['just some words']);
});
check('lessons at the class\'s level, one level down and one level up; a gap is said, not hidden', () => {
  const rungs = [{ slug: 'a', rank: 1 }, { slug: 'b', rank: 2 }, { slug: 'c', rank: 4 }, { slug: 'd', rank: 5 }];
  assert.deepEqual(pickRungs(rungs, 2).at.map((r) => r.slug), ['b']);
  assert.deepEqual(pickRungs(rungs, 2).down.map((r) => r.slug), ['a']);
  assert.deepEqual(pickRungs(rungs, 2).up.map((r) => r.slug), ['c']);
  assert.deepEqual(pickRungs(rungs, 3), { at: [], down: [rungs[1]], up: [rungs[2]] });
  assert.equal(defaultLevel([{ rank: 0 }, { rank: 2 }]), 2);
  assert.equal(defaultLevel([{ rank: 0 }]), 0);
  // In a real syllabus: every lesson offered is live, sits where the row says, and is offered once.
  for (const s of SYLLABI) {
    for (const row of matchSyllabus(m, s.text, s.level).rows) {
      if (!row.lessons) continue;
      const all = [...row.lessons.at, ...row.lessons.down, ...row.lessons.up];
      assert.equal(new Set(all.map((l) => l.slug)).size, all.length, `${s.name}: "${row.topic}" lists a lesson twice`);
      for (const l of all) assert.ok(site.lessons.has(l.slug), l.slug);
      assert.ok(row.lessons.at.every((l) => l.rank === s.level) && row.lessons.down.every((l) => l.rank < s.level) && row.lessons.up.every((l) => l.rank > s.level), `${s.name}: "${row.topic}"`);
      for (const id of row.lessons.missing) assert.ok(!m.byId.get(id).lessons.some((l) => l.rank === s.level), `${s.name}: says no lesson on ${id}, but there is one`);
    }
  }
});
check('matching a long syllabus is quick enough for a phone', () => {
  const t0 = Date.now();
  for (const s of SYLLABI) matchSyllabus(m, s.text, s.level);
  const ms = Date.now() - t0;
  assert.ok(ms < 4000, `${ms} ms for ${SYLLABI.length} syllabi`);
});

// ------------------------------------------------------------------ the path
console.log('the path');
const areaOf = (id) => api.clientGraph(api.concepts.filter((c) => c.area === graph.concepts[id].area).map((c) => c.id));
const ideaOf = (id) => ideaFromArea(areaOf(id), id, extra.lessons);
check('a path is one to five steps, its minutes are the sum of its steps, and every link is a real lesson or film', () => {
  for (const c of api.concepts) {
    if (!api.ladder(c.id).length) continue;
    const it = ideaOf(c.id);
    assert.ok(it && it.rungs.length, c.id);
    for (const level of [null, 0, 1, 2, 3, 4, 5, 6]) for (const time of ['skim', 'films', 'lesson']) {
      const p = buildPath([it], { level, time });
      assert.ok(p.steps.length >= 1 && p.steps.length <= MAX_STEPS, `${c.id} ${level} ${time}: ${p.steps.length} steps`);
      assert.equal(p.minutes, Math.max(1, Math.round(p.steps.reduce((n, s) => n + s.sec, 0) / 60)));
      assert.equal(p.stops[time], p.minutes);
      for (const s of p.steps) {
        const slug = /^\/(?:lessons|watch)\/([^/?#]+)\//.exec(s.href)?.[1];
        assert.ok(site.lessons.has(slug), `${c.id}: ${s.href}`);
        assert.ok(s.rank === p.rank, `${c.id}: a step at another level`);
      }
      if (level !== null && it.rungs.some((r) => r.rank === level)) assert.ok(p.rank === level && !p.moved);
      if (p.down) assert.ok(p.down.rank < p.rank);
      if (p.up) assert.ok(p.up.rank > p.rank);
    }
  }
});
check('with no level said, the path starts at the simplest lesson that is not an activity for young children', () => {
  const it = ideaOf('osmosis');
  const p = buildPath([it], { time: 'films' });
  assert.equal(p.rank, 1);
  assert.equal(p.steps[p.steps.length - 1].kind, 'skim');
  assert.ok(p.steps[0].kind === 'film' && /^\d+:\d\d$/.test(p.steps[0].length));
  assert.deepEqual(buildPath([it], { time: 'skim' }).steps.map((s) => s.kind), ['skim'], '"a few minutes" is the skim alone');
  assert.ok(buildPath([it], { time: 'skim' }).minutes <= p.minutes);
  assert.equal(buildPath([it], { time: 'lesson' }).steps[0].kind, 'lesson');
  assert.deepEqual(levelFor([{ rank: 0 }, { rank: 4 }], 2), { rank: 4, moved: true });
  assert.deepEqual(levelFor([{ rank: 1 }, { rank: 4 }], 2), { rank: 1, moved: true });
  assert.equal(timeFrom('stories'), 'films'); assert.equal(timeFrom(undefined), 'films'); assert.equal(timeFrom('skim'), 'skim');
});
check('an activity for ages 5 to 10 is always its guide, never its film alone', () => {
  let n = 0;
  for (const c of api.concepts) {
    const it = api.ladder(c.id).some((r) => r.rank === 0) ? ideaOf(c.id) : null;
    if (!it) continue;
    for (const time of ['skim', 'films', 'lesson']) {
      const p = buildPath([it], { level: 0, time });
      n++;
      assert.deepEqual(p.steps.map((s) => s.kind), ['activity'], `${c.id} ${time}`);
      assert.ok(/^\/lessons\/[^/]+\/$/.test(p.steps[0].href), `${c.id}: ${p.steps[0].href} is not the guide`);
    }
  }
  assert.ok(n > 30);
});
check('a level reads as a sentence at every level', () => {
  assert.equal(LEVEL_AT.length, 7); assert.equal(LEVEL_CLASS.length, 7);
  for (const s of [...LEVEL_AT.map((a) => `A short path ${a}, about 5 minutes.`), ...LEVEL_CLASS.map((c) => `I read 9 topics for ${c}.`)]) {
    assert.ok(!/level level|at a first|at an? upper|for a college,|  /.test(s), s);
  }
  const it = ideaOf('osmosis');
  for (let level = 0; level < 7; level++) assert.ok(buildPath([it], { level, time: 'films' }).levelAt.length > 5);
  for (const f of ['src/lib/start-page.ts', 'src/lib/teach-match.ts']) assert.ok(!/\$\{[^}]*(LEVEL_SHORT|path\.level)\b[^}]*\} level/.test(readFileSync(f, 'utf8')), `${f} glues a level name to the word "level"`);
});
check('two ideas share one path of at most five steps', () => {
  const p = buildPath([ideaOf('photosynthesis'), ideaOf('cellular-respiration')], { level: 2, time: 'films' });
  assert.ok(p.steps.length <= MAX_STEPS);
  assert.deepEqual([...new Set(p.steps.map((s) => s.idea))], ['photosynthesis', 'cellular-respiration']);
});

// ------------------------------------------------------------------ files and classes
console.log('files and classes');
function zip(name, data, method) {
  const body = method === 8 ? deflateRawSync(data) : data;
  const n = Buffer.from(name);
  const local = Buffer.alloc(30); local.writeUInt32LE(0x04034b50, 0); local.writeUInt16LE(method, 8); local.writeUInt32LE(body.length, 18); local.writeUInt32LE(data.length, 22); local.writeUInt16LE(n.length, 26);
  const central = Buffer.alloc(46); central.writeUInt32LE(0x02014b50, 0); central.writeUInt16LE(method, 10); central.writeUInt32LE(body.length, 20); central.writeUInt32LE(data.length, 24); central.writeUInt16LE(n.length, 28); central.writeUInt32LE(0, 42);
  const end = Buffer.alloc(22); end.writeUInt32LE(0x06054b50, 0); end.writeUInt16LE(1, 8); end.writeUInt16LE(1, 10); end.writeUInt32LE(46 + n.length, 12); end.writeUInt32LE(30 + n.length + body.length, 16);
  return new Uint8Array(Buffer.concat([local, n, body, central, n, end]));
}
check('a Word file is read on the device: paragraphs to lines, table rows to one line', async () => {
  const xml = '<?xml version="1.0"?><w:document><w:body><w:p><w:r><w:t>Week 1: Cells &amp; membranes</w:t></w:r></w:p><w:p><w:r><w:t xml:space="preserve">Week 2: </w:t></w:r><w:r><w:t>Osmosis</w:t></w:r></w:p>'
    + '<w:tbl><w:tr><w:tc><w:p><w:r><w:t>9/8</w:t></w:r></w:p></w:tc><w:tc><w:p><w:r><w:t>Meiosis</w:t></w:r></w:p></w:tc></w:tr></w:tbl></w:body></w:document>';
  assert.equal(documentXmlToText(xml), 'Week 1: Cells & membranes\nWeek 2: Osmosis\n9/8 | Meiosis');
  for (const method of [8, 0]) assert.equal(await docxText(zip('word/document.xml', Buffer.from(xml), method)), 'Week 1: Cells & membranes\nWeek 2: Osmosis\n9/8 | Meiosis');
  assert.equal(await docxText(new Uint8Array([1, 2, 3, 4])), null, 'not a zip');
  assert.equal(await docxText(zip('other.xml', Buffer.from(xml), 8)), null, 'a zip with no document');
  const res = matchSyllabus(m, await docxText(zip('word/document.xml', Buffer.from(xml), 8)), 2);
  assert.deepEqual(res.rows.map((r) => r.ideas.map((x) => x.id)).flat().includes('osmosis'), true);
});
check('adding to a class keeps what is assigned, adds each lesson once, in order, with no due date', () => {
  const had = [{ slug: 'a', due: '2026-12-01', flashcards: true }, { slug: 'b', due: null }];
  const r = mergeAssignments(had, ['c', 'a', 'd', 'c']);
  assert.deepEqual(r.list, [{ slug: 'a', due: '2026-12-01', flashcards: true }, { slug: 'b', due: null, flashcards: false }, { slug: 'c', due: null, flashcards: false }, { slug: 'd', due: null, flashcards: false }]);
  assert.deepEqual(r.added, ['c', 'd']); assert.deepEqual(r.already, ['a']);
  const full = mergeAssignments(Array.from({ length: MAX_ASSIGNMENTS }, (_, i) => ({ slug: `l${i}`, due: null })), ['x']);
  assert.equal(full.list.length, MAX_ASSIGNMENTS); assert.deepEqual(full.dropped, ['x']);
  assert.deepEqual(mergeAssignments(undefined, []).list, []);
});

// ------------------------------------------------------------------ the promises the pages make
console.log('the promises the pages make');
check('what is typed or pasted is never put in a request or in the address', () => {
  const start = readFileSync('src/lib/start-page.ts', 'utf8');
  const teach = readFileSync('src/lib/teach-match.ts', 'utf8');
  const urls = (src) => [...src.matchAll(/(?:fetch|json|api)\(\s*(`[^`]*`|'[^']*'|"[^"]*")/g)].map((x) => x[1]);
  // Every request in the student page is a GET for a static file named without the typed words.
  for (const u of urls(start)) assert.ok(/^['`]\/(graph\.json|ideas\/lessons\.json|start\/lessons\.json|graph\/\$\{id\}\.json)['`]$/.test(u), `start-page.ts requests ${u}`);
  const channels = /history\.(push|replace)State|location\.(href|search|hash)\s*=|location\.assign|sendBeacon|XMLHttpRequest|WebSocket|localStorage|sessionStorage|document\.cookie|\.submit\(|requestSubmit/;
  assert.ok(!channels.test(start), 'start-page.ts touches the address, storage or another channel');
  assert.ok(!/encodeURIComponent\((q|typed|input\.value)/.test(start), 'a typed word is put in a link');
  // The teacher page: static files, and (when switched on) the classes API with ticked lesson slugs only.
  for (const u of urls(teach)) assert.ok(/^['`]\/(graph\.json|ideas\/lessons\.json|start\/lessons\.json|graph\/all\.json|api\/teacher\/me|api\/classes\/\$\{encodeURIComponent\(id\)\}\/(brief|assignments))['`]$/.test(u), `teach-match.ts requests ${u}`);
  assert.ok(!channels.test(teach), 'teach-match.ts touches the address, storage or another channel');
  assert.ok(/\{ assignments: merged\.list \}/.test(teach) && !/text\.value[^;]*api\(|api\([^;]*typed/.test(teach), 'only the assignment list is sent');
  assert.ok(/export const ADD_TO_CLASS = false;/.test(teach), 'adding to a class is off until it has been tried on a real class');
  assert.ok(/noAnalytics/.test(readFileSync('src/pages/teach/match/index.astro', 'utf8')), 'no third-party script where a syllabus is pasted');
  assert.ok(/const SHOW_AI_PLANNER_LINK = false;/.test(readFileSync('src/pages/teach/match/index.astro', 'utf8')), 'the link to the AI planner is off');
  // The privacy pages say what these tools do, and tell the two syllabus tools apart.
  const tp = readFileSync('src/pages/teach/privacy/index.astro', 'utf8'), pp = readFileSync('src/pages/privacy/index.astro', 'utf8');
  assert.ok(/id="matcher"/.test(tp) && /runs in your browser/.test(tp) && /The AI planner/.test(tp) && /does send your syllabus/.test(tp));
  assert.ok(/never sent to us/.test(pp) && /remembers it/.test(pp) && /Start simple/.test(pp));
  assert.ok(!/Nothing on the site for this yet/.test(teach), 'the teacher page claims the site has nothing, which it cannot know');
});
check('the question box never repeats the typed words, always carries the help line, and stays unlinked until its help words are approved', () => {
  const page = readFileSync('src/pages/start/index.astro', 'utf8');
  const code = readFileSync('src/lib/start-page.ts', 'utf8').replace(/\/\*[\s\S]*?\*\/|^\s*\/\/.*$/gm, '');
  // No reply is built from what was typed: not the no-match line, not the closest line, not the status.
  assert.ok(!/esc\(\s*(q|typed|input\.value)\s*\)|\$\{\s*(q|typed|input\.value)\s*\}|“\$\{/.test(code), 'start-page.ts writes the typed words onto the page');
  assert.ok(!/stomach, nerves|one or two plain/.test(code), 'a tip under a failed question can read as flippant');
  assert.ok(/\{HELP\.line\}/.test(page) && /href=\{HELP\.href\}/.test(page), 'the permanent help line is on the page');
  assert.ok(/<BaseLayout[^>]*\bnoindex\b/.test(page), '/start/ is noindex until the help words are approved');
  assert.ok(/<BaseLayout[^>]*\bnoindex\b/.test(readFileSync('src/pages/start/help/index.astro', 'utf8')));
  for (const f of ['src/pages/ideas/index.astro', 'src/pages/teach/index.astro', 'src/pages/sitemap.xml.ts']) assert.ok(!/["'`]\/start\//.test(readFileSync(f, 'utf8')), `${f} links /start/`);
  // The help words: one constant, plain, with no single adult named as the only one, and US numbers said to be US.
  const all = [HELP.line, HELP.urgent.heading, ...HELP.urgent.lines, HELP.urgent.status, HELP.page.intro, ...HELP.page.steps.flat(), HELP.page.foot];
  for (const t of all) { assert.ok(t.length <= 240, t); assert.ok(!/should not have|shouldn't have|not allowed|wrong to|your fault\b(?<!not your fault)/i.test(t), t); assert.ok(!/—/.test(t), t); }
  assert.ok(/adult you trust/.test(HELP.line) && /not a person/.test(HELP.line));
  for (const t of all) if (/\b(911|988|1-800)/.test(t)) assert.ok(/United States/.test(t), `a phone number without its country: ${t}`);
  assert.ok(!all.some((t) => /\b(tell|ask) (a|your) parent\b(?!s?,)/i.test(t)), 'a parent is named as the only adult');
  assert.ok(withNumbers('call 988 now').includes('href="tel:988"'));
});
check('with scripts off, blocked or late, nothing on either page can submit what was typed', () => {
  // A browser sends a form's named fields by itself: on Enter, or on a button press before the page's
  // script has run. So these pages have no form at all, their boxes have no name, and their buttons do
  // nothing until the script switches them on.
  for (const f of ['src/pages/start/index.astro', 'src/pages/start/help/index.astro', 'src/pages/teach/match/index.astro']) {
    const html = readFileSync(f, 'utf8').replace(/^---[\s\S]*?^---/m, '').replace(/<!--[\s\S]*?-->/g, '').replace(/\{\/\*[\s\S]*?\*\/\}/g, '');
    assert.ok(!/<form\b/i.test(html), `${f} has a <form>`);
    assert.ok(!/\b(action|formaction|method)\s*=/i.test(html), `${f} has a form action or method`);
    assert.ok(!/type="submit"/i.test(html), `${f} has a submit button`);
    for (const tag of html.match(/<(input|textarea)\b[^>]*>/gi) ?? []) {
      const typedInto = /<textarea/i.test(tag) || /type="(search|text)"/i.test(tag);
      if (typedInto) assert.ok(!/\bname\s*=/i.test(tag), `${f}: a box someone types into has a name, so a form could send it: ${tag}`);
    }
    for (const tag of html.match(/<button\b[^>]*>/gi) ?? []) {
      assert.ok(/type="button"/.test(tag), `${f}: ${tag} is not type="button"`);
      if (/data-(st-go|st-try|tm-go|tm-sample)/.test(tag)) assert.ok(/\bdisabled\b/.test(tag), `${f}: ${tag} works before the script has run`);
    }
    if (!f.includes('/help/')) assert.ok(/<noscript>/.test(html), `${f} says nothing when scripts are off`);
  }
});
check('the pages say only what is true, in the site\'s words', () => {
  for (const f of ['src/pages/start/index.astro', 'src/lib/start-page.ts', 'src/pages/teach/match/index.astro', 'src/lib/teach-match.ts']) {
    const src = readFileSync(f, 'utf8');
    const shown = src.replace(/\/\*[\s\S]*?\*\/|^\s*\/\/.*$/gm, '');
    const word = /\b(easier|harder|level up|beginner|advanced|dumbed|streak|leaderboard|lessons? (to go|remaining|left))\b/i.exec(shown);
    assert.ok(!word, `${f}: "${word?.[0]}" ranks the reader or counts what is left`);
    assert.ok(!/—/.test(shown.replace(/title="[^"]*"/g, '')), `${f}: an em-dash in copy`);
  }
});

for (const run of pending) await run();
console.log(`\n${passed} passed${process.exitCode ? ', some FAILED' : ''}`);
