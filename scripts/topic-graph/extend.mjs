#!/usr/bin/env node
/**
 * Hop graph: look for rungs nobody proposed.
 *
 * The first fill asked "which ideas does this lesson teach?" one lesson at a time, so an idea filed
 * from a college lesson was rarely offered to the high school lesson that also teaches it. This
 * pass asks the other way round: for each idea taught at only one or two levels, which lessons at
 * OTHER levels might teach it too? Candidates are picked without a model, by counting the idea's
 * own words in each lesson's headings, objectives and text; readers then judge each pair, and a
 * second reader who did not propose a rung judges it blind. Precision beats recall: most
 * candidates are meant to be refused.
 *
 *   node scripts/topic-graph/extend.mjs propose --staging <dir> [--per-batch 36] [--max-levels 2] [--top 2] [--pairs <file>]
 *        writes prompts/extend/<nn>.md (+ MANIFEST.json); readers answer in extend/<nn>.json
 *        --pairs: a JSON list of extra [concept id, lesson slug] pairs someone asked to have judged
 *   node scripts/topic-graph/extend.mjs verify --staging <dir> [--per-batch 30]
 *        writes prompts/extend-verify/<nn>.md for every rung proposed; judges answer in extend-verify/<nn>.json
 *   node scripts/topic-graph/extend.mjs apply --staging <dir> [--name 03-extend]
 *        writes review/<name>.json from the rungs that were proposed AND passed the blind check;
 *        ingest.mjs then checks and merges it like any other review file
 *
 * Calls no model.
 */
import { readFileSync, writeFileSync, existsSync, mkdirSync, readdirSync } from 'node:fs';
import { join, isAbsolute } from 'node:path';
import { plain } from '../lesson-links/lib.mjs';
import { ROOT, loadGraphSite, readGraph, fold, LIMITS } from './lib.mjs';
import { buildDigests, digestText } from './digest.mjs';
import { RULES } from './prompts.mjs';

const argv = process.argv.slice(2);
const cmd = argv[0];
const opt = (f, d) => { const i = argv.indexOf(f); return i >= 0 ? argv[i + 1] : d; };
const abs = (p) => (isAbsolute(p) ? p : join(ROOT, p));
if (!cmd || !opt('--staging')) { console.error('usage: extend.mjs <propose|verify|apply> --staging <dir>'); process.exit(2); }
const S = abs(opt('--staging'));
const site = await loadGraphSite();
const graph = readGraph();
const dir = (...p) => { const d = join(S, ...p); mkdirSync(d, { recursive: true }); return d; };
const tokens = (t) => Math.round(t.length / 4);
const readAll = (kind) => (existsSync(join(S, kind)) ? readdirSync(join(S, kind)).filter((f) => f.endsWith('.json')).sort().map((f) => ({ name: f.replace(/\.json$/, ''), data: JSON.parse(readFileSync(join(S, kind, f), 'utf8')) })) : []);
const stageOf = (slug) => site.lessons.get(slug).stage;

const STOP = new Set('a an the of in on to and or how why what when where is are do does it its their your you for with from by at as that this be can into than more most each one two kinds kind things living body cells cell'.split(' '));
const stem = (w) => w.replace(/(ies)$/, 'y').replace(/(es|s)$/, '');
const words = (s) => fold(s).split(' ').filter((w) => w.length > 2 && !STOP.has(w)).map(stem);

/** The idea as a reader is shown it. */
function claim(id) {
  const c = graph.concepts[id];
  const core = c.rungs.filter((r) => r.role === 'core').map((r) => `    ${stageOf(r.lesson).padEnd(16)} ${r.lesson} ("${site.lessons.get(r.lesson).title}"): ${r.adds}`);
  return `IDEA ${id}\n  Name: ${c.name}\n  What it is: ${c.blurb}\n  Also asked as: ${c.aliases.join('; ')}\n  Taught now at:\n${core.join('\n')}`;
}

if (cmd === 'propose') {
  const maxLevels = Number(opt('--max-levels', 2)), top = Number(opt('--top', 2)), per = Number(opt('--per-batch', 36));
  const text = new Map();
  for (const l of site.lessons.values()) text.set(l.slug, { head: fold(`${l.title} ${l.heads.map((h) => h.text).join(' ')}`), mid: fold(`${l.summary} ${l.objectives.join(' ')} ${l.fm.hook ?? ''}`), body: fold(plain(l.body)) });
  const count = (hay, needle) => { if (!needle) return 0; let n = 0, i = 0; while ((i = hay.indexOf(needle, i)) >= 0) { n++; i += needle.length; } return n; };
  const pairs = [];
  for (const [id, c] of Object.entries(graph.concepts)) {
    const core = c.rungs.filter((r) => r.role === 'core');
    const ranks = new Set(core.map((r) => site.lessons.get(r.lesson).rank));
    if (ranks.size > maxLevels) continue;
    const name = c.name.replace(/\(.*?\)/g, ' ');
    const inParens = (c.name.match(/\((.*?)\)/) ?? [])[1] ?? '';
    const phrases = [...new Set([fold(name), fold(id.replace(/-/g, ' ')), ...inParens.split(/,| and /).map(fold), ...c.aliases.filter((a) => a.split(' ').length <= 3).map(fold)])].filter((p) => p.length >= 4);
    const terms = [...new Set([...words(name), ...words(id.replace(/-/g, ' '))])];
    const scored = [];
    for (const l of site.lessons.values()) {
      if (ranks.has(l.rank)) continue;                                  // a level the idea is already taught at
      const t = text.get(l.slug);
      const uses = c.rungs.some((r) => r.lesson === l.slug);
      let s = uses ? 6 : 0;
      for (const p of phrases) s += 6 * Math.min(2, count(t.head, p)) + 3 * Math.min(2, count(t.mid, p)) + Math.min(6, count(t.body, p));
      const hit = terms.filter((w) => t.head.includes(w)).length;
      if (terms.length && hit === terms.length) s += 4;
      if (s >= 9) scored.push({ id, lesson: l.slug, score: s, gap: Math.min(...[...ranks].map((r) => Math.abs(r - l.rank))) });
    }
    scored.sort((a, b) => b.score - a.score || a.gap - b.gap || a.lesson.localeCompare(b.lesson));
    pairs.push(...scored.slice(0, top));
  }
  for (const [id, lesson] of opt('--pairs') ? JSON.parse(readFileSync(abs(opt('--pairs')), 'utf8')) : []) {
    if (graph.concepts[id] && site.lessons.has(lesson) && !pairs.some((p) => p.id === id && p.lesson === lesson) && !graph.concepts[id].rungs.some((r) => r.lesson === lesson && r.role === 'core')) pairs.push({ id, lesson, score: 99, asked: true });
  }
  // batches hold whole lessons together (one digest serves several ideas), in course order
  const order = [...site.lessons.values()].sort((a, b) => a.courseIdx - b.courseIdx || a.n - b.n).map((l) => l.slug);
  pairs.sort((a, b) => order.indexOf(a.lesson) - order.indexOf(b.lesson) || a.id.localeCompare(b.id));
  const digests = buildDigests(site);
  const batches = [];
  for (const p of pairs) { let b = batches[batches.length - 1]; if (!b || (b.length >= per && b[b.length - 1].lesson !== p.lesson)) batches.push(b = []); b.push(p); }
  const out = dir('prompts', 'extend'), ans = dir('extend');
  const rows = batches.map((b, i) => {
    const n = String(i + 1).padStart(2, '0');
    const lessons = [...new Set(b.map((p) => p.lesson))];
    const prompt = `You are looking for MISSING RUNGS in STEMhop's graph of ideas. Each idea below is taught, as far as the graph
knows, at only one or two levels. For each PAIR of an idea and a lesson, decide whether that lesson is also a
place to learn that idea. The pairs were picked by a word count, not by a reader, so MOST of them should be
refused: the lesson mentions the idea, or needs it, without teaching it. A wrong rung is worse than a missing one.

${RULES.site}

${RULES.roles}

Say "core" for a pair ONLY if all three hold:
  1. the lesson has a ## section whose subject is this idea itself (you can name its anchor id);
  2. a reader coming from the idea's existing rung at the level below would learn more about THIS idea there
     (or, when the lesson is the lower level: it is a place to meet the idea for the first time, and the
     existing rung would then take it further);
  3. it is the same idea, not a neighbour, a part, a use or a prerequisite of it.
A passing mention, one item in a list or table, or a paragraph inside a section about something else is "no".
If the idea is the subject of only a short part of a section, it is "no".

${RULES.note}

${RULES.anchor}

${RULES.films}

${RULES.voice}

${RULES.reading}
Lesson file paths are relative to ${ROOT}. Read only: change no file except your answer file.
For every pair you are inclined to accept, OPEN THE LESSON and read the section before you say "core".

YOUR ANSWER: write ${join(ans, `${n}.json`)} holding one JSON object:
{
  "batch": "${n}",
  "pairs": [
    { "id": "<idea id>", "lesson": "<slug>", "verdict": "no", "why": "<a few words>" },
    { "id": "<idea id>", "lesson": "<slug>", "verdict": "core", "anchor": "<section id>", "adds": "<note, at most ${LIMITS.addsWords} words>", "films": ["<film key>"], "why": "<one sentence: which section, and what a reader from the other level learns>" }
  ]
}
One entry for EVERY pair listed, in the order given. JSON only in the file. Then reply with one line: how many core, how many no.

THE PAIRS (${b.length})
${b.map((p) => `  ${p.id}  +  ${p.lesson}  (${stageOf(p.lesson)})`).join('\n')}

THE IDEAS
${[...new Set(b.map((p) => p.id))].map(claim).join('\n\n')}

THE LESSONS (digests)
${lessons.map((s) => `${'='.repeat(100)}\n${digestText(digests.get(s))}`).join('\n\n')}
`;
    writeFileSync(join(out, `${n}.md`), prompt);
    return { batch: n, prompt: join(out, `${n}.md`), answer: join(ans, `${n}.json`), pairs: b.map((p) => [p.id, p.lesson]), lessons: lessons.length, tokens: tokens(prompt) };
  });
  writeFileSync(join(out, 'MANIFEST.json'), JSON.stringify({ stage: 'extend', pairs: pairs.length, items: rows }, null, 1) + '\n');
  for (const r of rows) console.log(`${r.batch}  ${String(r.pairs.length).padStart(3)} pairs  ${String(r.lessons).padStart(3)} lessons  ~${Math.round(r.tokens / 1000)}k tokens  ${r.prompt}`);
  console.log(`extend propose: ${pairs.length} pair(s) over ${new Set(pairs.map((p) => p.id)).size} idea(s) in ${rows.length} batch(es); ${pairs.filter((p) => p.asked).length} asked for by name.`);
}

else if (cmd === 'verify') {
  const per = Number(opt('--per-batch', 30));
  const proposed = readAll('extend').flatMap((f) => (f.data.pairs ?? []).filter((p) => p.verdict === 'core').map((p) => ({ ...p, from: f.name })))
    .filter((p) => graph.concepts[p.id] && site.lessons.has(p.lesson));
  const order = [...site.lessons.values()].sort((a, b) => a.courseIdx - b.courseIdx || a.n - b.n).map((l) => l.slug);
  proposed.sort((a, b) => order.indexOf(a.lesson) - order.indexOf(b.lesson) || a.id.localeCompare(b.id));
  const digests = buildDigests(site);
  const batches = [];
  for (const p of proposed) { let b = batches[batches.length - 1]; if (!b || (b.length >= per && b[b.length - 1].lesson !== p.lesson)) batches.push(b = []); b.push(p); }
  const out = dir('prompts', 'extend-verify'), ans = dir('extend-verify');
  const rows = batches.map((b, i) => {
    const n = String(i + 1).padStart(2, '0');
    const lessons = [...new Set(b.map((p) => p.lesson))];
    const prompt = `You are checking proposed additions to STEMhop's graph of ideas. You did not write them. For each RUNG below,
someone claims that the lesson is a place to learn the idea, at a level where the graph had no lesson for it.
Readers will follow these links to hop to a simpler or a deeper lesson on the same idea, so a wrong link costs
their trust: a wrong rung is worse than a missing one. Judge from the lessons, not from the claim. Do not be
generous; refusing is the safe answer.

${RULES.site}

${RULES.roles}

A rung passes ONLY if all three hold:
  1. the anchor's section (a ## heading of the lesson) has this idea itself as its subject;
  2. a reader coming from the idea's existing rung at the level below would learn more about THIS idea there
     (or, when the new lesson is the lower one: it is a place to meet the idea for the first time);
  3. it is the same idea as the existing rungs teach, not a neighbour, a part, a use or a prerequisite of it.
Then judge the note: is it true to the lesson (its case, experiment or number is really there), specific to
this lesson, at most ${LIMITS.addsWords} words, and pitched at this level's reader?

${RULES.note}

${RULES.voice}

Lesson file paths are relative to ${ROOT}. Read only: change no file except your answer file.
OPEN THE LESSON and read the anchored section for every rung before you answer.

YOUR ANSWER: write ${join(ans, `${n}.json`)} holding one JSON object:
{
  "batch": "${n}",
  "rungs": [
    { "id": "<idea id>", "lesson": "<slug>", "verdict": "ok" },
    { "id": "<idea id>", "lesson": "<slug>", "verdict": "note", "adds": "<your replacement note>", "why": "<what was wrong with the note>" },
    { "id": "<idea id>", "lesson": "<slug>", "verdict": "wrong", "why": "<one sentence>" }
  ]
}
One entry for EVERY rung listed. JSON only in the file. Then reply with one line: how many ok, note, wrong.

THE RUNGS (${b.length})
${b.map((p) => `  ${p.id}  +  ${p.lesson}  (${stageOf(p.lesson)})  anchor #${p.anchor ?? '-'}  note: ${p.adds}  films: ${(p.films ?? []).join(', ') || 'none'}`).join('\n')}

THE IDEAS
${[...new Set(b.map((p) => p.id))].map(claim).join('\n\n')}

THE LESSONS (digests; they hold nothing from the graph)
${lessons.map((s) => `${'='.repeat(100)}\n${digestText(digests.get(s))}`).join('\n\n')}
`;
    writeFileSync(join(out, `${n}.md`), prompt);
    return { batch: n, prompt: join(out, `${n}.md`), answer: join(ans, `${n}.json`), rungs: b.map((p) => [p.id, p.lesson, p.from]), tokens: tokens(prompt) };
  });
  writeFileSync(join(out, 'MANIFEST.json'), JSON.stringify({ stage: 'extend-verify', rungs: proposed.length, items: rows }, null, 1) + '\n');
  for (const r of rows) console.log(`${r.batch}  ${String(r.rungs.length).padStart(3)} rungs  ~${Math.round(r.tokens / 1000)}k tokens  ${r.prompt}`);
  console.log(`extend verify: ${proposed.length} proposed rung(s) in ${rows.length} batch(es).`);
}

else if (cmd === 'apply') {
  const proposed = new Map(readAll('extend').flatMap((f) => (f.data.pairs ?? []).filter((p) => p.verdict === 'core').map((p) => [`${p.id}|${p.lesson}`, p])));
  const verdicts = new Map(readAll('extend-verify').flatMap((f) => (f.data.rungs ?? []).map((v) => [`${v.id}|${v.lesson}`, v])));
  const rungs = [], refused = [], unjudged = [];
  for (const [k, p] of proposed) {
    const v = verdicts.get(k);
    if (!v) { unjudged.push(k); continue; }
    // A lesson teaches at most three ideas. A fourth is refused here, however good: it is the sign of a shared section.
    const coreNow = Object.values(graph.concepts).filter((c) => c.rungs.some((r) => r.lesson === p.lesson && r.role === 'core')).length + rungs.filter((r) => r.lesson === p.lesson).length;
    if ((v.verdict === 'ok' || v.verdict === 'note') && coreNow >= LIMITS.corePerLesson && !graph.concepts[p.id].rungs.some((r) => r.lesson === p.lesson && r.role === 'core')) { refused.push({ pair: k, why: `passed the blind check, but ${p.lesson} already teaches ${LIMITS.corePerLesson} ideas` }); continue; }
    if (v.verdict === 'ok' || (v.verdict === 'note' && typeof v.adds === 'string')) rungs.push({ id: p.id, lesson: p.lesson, role: 'core', anchor: p.anchor ?? null, adds: v.verdict === 'note' ? v.adds : p.adds, films: p.films ?? [], why: `Found by the missing-rung pass and passed the blind check. ${p.why ?? ''}`.trim() });
    else refused.push({ pair: k, why: v.why ?? '' });
  }
  const name = opt('--name', '03-extend');
  writeFileSync(join(dir('review'), `${name}.json`), JSON.stringify({ by: 'The missing-rung pass: rungs a reader proposed for ideas taught at one or two levels, kept only when a second reader who did not propose them passed them.', rungs }, null, 1) + '\n');
  writeFileSync(join(dir('reports'), 'extend.json'), JSON.stringify({ proposed: proposed.size, passed: rungs.length, refused, unjudged }, null, 1) + '\n');
  console.log(`extend apply: ${proposed.size} proposed, ${rungs.length} passed the blind check (${[...verdicts.values()].filter((v) => v.verdict === 'note').length} with a rewritten note), ${refused.length} refused, ${unjudged.length} not judged. Wrote review/${name}.json; run ingest.mjs next.`);
}

else { console.error(`Unknown command "${cmd}".`); process.exit(2); }
