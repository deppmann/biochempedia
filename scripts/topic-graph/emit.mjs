#!/usr/bin/env node
/**
 * Hop graph: write the prompt files for a fill, stage by stage, into a staging folder.
 *
 * A fill is done by readers (models, or people) who each get one prompt file and write their
 * answer as JSON into the same staging folder; ingest.mjs then checks and merges the answers.
 * This tool writes the prompts and a MANIFEST.json per stage (which prompt, which lessons or
 * concepts, how long, where the answer goes). The words come from prompts.mjs.
 *
 *   node scripts/topic-graph/emit.mjs propose      --staging <dir> [--batch-size 8] [--course <slug>] [--missing]
 *   node scripts/topic-graph/emit.mjs canonicalize --staging <dir> [--cross]
 *   node scripts/topic-graph/emit.mjs near         --staging <dir> [--all]
 *   node scripts/topic-graph/emit.mjs verify       --staging <dir> [--sample 4] [--all] [--budget 45000]
 *   node scripts/topic-graph/emit.mjs status       --staging <dir>
 *   node scripts/topic-graph/emit.mjs mock <propose|canonicalize|cross|near|verify> --staging <dir>
 *        writes deterministic stand-in ANSWERS for that stage (some deliberately broken), to prove
 *        the plumbing end to end without a reader. Never use it on a real staging folder.
 *
 * Calls no model. Reads the staging folder's base.json (the graph the fill starts from) when it is
 * there, else src/data/topic-graph.json.
 */
import { readFileSync, writeFileSync, existsSync, mkdirSync, rmSync } from 'node:fs';
import { join, isAbsolute } from 'node:path';
import { createHash } from 'node:crypto';
import { ROOT, AREAS, loadGraphSite, readGraph, emptyGraph, registryOf, serializeGraph } from './lib.mjs';
import { buildDigests } from './digest.mjs';
import { proposeBatchPrompt, canonicalizePrompt, nearPrompt, verifyPrompt } from './prompts.mjs';
import { ingest, readStaging, ticketOf } from './ingest.mjs';

const argv = process.argv.slice(2);
const cmd = argv[0];
const flag = (f) => argv.includes(f);
const opt = (f, d) => { const i = argv.indexOf(f); return i >= 0 ? argv[i + 1] : d; };
const abs = (p) => (isAbsolute(p) ? p : join(ROOT, p));
if (!cmd || !opt('--staging')) { console.error('usage: emit.mjs <propose|canonicalize|near|verify|status|mock> --staging <dir>   (see the header of this file)'); process.exit(2); }
const S = abs(opt('--staging'));
mkdirSync(S, { recursive: true });
const tokens = (text) => Math.round(text.length / 4);
const site = await loadGraphSite();
const baseFile = join(S, 'base.json');
if (!existsSync(baseFile)) { writeFileSync(baseFile, serializeGraph(readGraph() ?? emptyGraph())); console.log(`emit: saved the starting graph as ${baseFile}`); }
const base = JSON.parse(readFileSync(baseFile, 'utf8'));
const stage = (name) => { const d = join(S, 'prompts', name); mkdirSync(d, { recursive: true }); return d; };
const answers = (name) => { const d = join(S, name); mkdirSync(d, { recursive: true }); return d; };
const state = (stages) => ingest({ base, site, staging: readStaging(S), stages });
const manifest = (dir, rows, extra = {}) => writeFileSync(join(dir, 'MANIFEST.json'), JSON.stringify({ stage: dir.split('/').pop(), written: new Date().toISOString().slice(0, 10), ...extra, items: rows }, null, 1) + '\n');
const stageOf = (slug) => site.lessons.get(slug)?.stage ?? '?';

/** A lesson's current record as proposal entries (what a reader is asked to keep unless wrong). */
function existingEntries(graph, slug) {
  const out = [];
  for (const [id, c] of Object.entries(graph.concepts)) {
    const r = c.rungs.find((x) => x.lesson === slug);
    if (!r) continue;
    out.push(r.role === 'core' ? { id, role: 'core', anchor: r.anchor ?? null, adds: r.adds, films: c.films.filter((k) => site.films.get(k)?.lesson === slug) } : { id, role: 'uses' });
  }
  return out.sort((a, b) => (a.role === b.role ? 0 : a.role === 'core' ? -1 : 1));
}

/** A course's lessons cut into batches along unit boundaries, at most `size` lessons each. */
function batchesOf(course, size) {
  const mine = [...site.lessons.values()].filter((l) => l.course === course.slug).sort((a, b) => a.n - b.n);
  const units = [];
  for (const l of mine) { const u = units[units.length - 1]; if (u && u.name === l.unit) u.lessons.push(l); else units.push({ name: l.unit, lessons: [l] }); }
  const out = [];
  let cur = [];
  for (const u of units) {
    if (u.lessons.length > size) {
      if (cur.length) { out.push(cur); cur = []; }
      const parts = Math.ceil(u.lessons.length / size), per = Math.ceil(u.lessons.length / parts);
      for (let i = 0; i < u.lessons.length; i += per) out.push(u.lessons.slice(i, i + per));
      continue;
    }
    if (cur.length + u.lessons.length > size) { out.push(cur); cur = []; }
    cur.push(...u.lessons);
  }
  if (cur.length) out.push(cur);
  return out;
}

const clip = (s, n) => { const t = String(s ?? '').replace(/\s+/g, ' ').trim(); return t.length <= n ? t : t.slice(0, n).replace(/\s+\S*$/, '') + '…'; };
function courseMap(course) {
  const mine = [...site.lessons.values()].filter((l) => l.course === course.slug).sort((a, b) => a.n - b.n);
  const ci = site.courseInfo.get(course.slug);
  const L = [`Course "${course.title}" (${course.slug}), level ${ci.rank} ${ci.stage}, ${mine.length} lessons.`];
  let unit = null;
  for (const l of mine) { if (l.unit !== unit) { unit = l.unit; L.push(`  [${unit || 'other'}]`); } L.push(`    ${l.n}. ${l.slug} | ${clip(l.title, 80)} | ${clip(l.hook, 110)}`); }
  return L.join('\n');
}

// ------------------------------------------------------------------ propose

if (cmd === 'propose') {
  const dir = stage('propose');
  const size = Number(opt('--batch-size', 8));
  const digests = buildDigests(site);
  const registry = registryOf(base, site);
  const out = answers('proposals');
  const rows = [];
  for (const course of site.COURSES) {
    if (opt('--course') && opt('--course') !== course.slug) continue;
    let n = 0;
    for (const batch of batchesOf(course, size)) {
      n++;
      const todo = flag('--missing') ? batch.filter((l) => !existsSync(join(out, `${l.slug}.json`))) : batch;
      if (!todo.length) continue;
      const id = `${course.slug}-${String(n).padStart(2, '0')}`;
      const text = proposeBatchPrompt(todo.map((l) => digests.get(l.slug)), registry, {
        existingBySlug: Object.fromEntries(todo.map((l) => [l.slug, existingEntries(base, l.slug)]).filter(([, e]) => e.length)),
        courseMap: courseMap(course), answerDir: out, root: ROOT,
      });
      writeFileSync(join(dir, `${id}.md`), text);
      rows.push({ id, prompt: join(dir, `${id}.md`), course: course.slug, level: site.courseInfo.get(course.slug).stage, lessons: todo.map((l) => l.slug), withRecord: todo.filter((l) => base.lessons?.[l.slug]).length, tokens: tokens(text), answers: todo.map((l) => join(out, `${l.slug}.json`)) });
    }
  }
  manifest(dir, rows, { answersIn: out, registryConcepts: registry.length });
  for (const r of rows) console.log(`${r.id.padEnd(34)} ${String(r.lessons.length).padStart(2)} lessons  ~${String(Math.round(r.tokens / 1000)).padStart(3)}k tokens  ${r.prompt}`);
  const t = rows.reduce((a, r) => a + r.tokens, 0);
  console.log(`propose: ${rows.length} prompt(s) for ${rows.reduce((a, r) => a + r.lessons.length, 0)} lesson(s); ~${Math.round(t / 1000)}k tokens of prompt in all, largest ~${Math.round(Math.max(0, ...rows.map((r) => r.tokens)) / 1000)}k. Manifest: ${join(dir, 'MANIFEST.json')}`);
}

// ------------------------------------------------------------------ canonicalize

else if (cmd === 'canonicalize') {
  const dir = stage('canonicalize');
  const out = answers('canonical');
  const lessonRow = (r) => { const l = site.lessons.get(r.lesson); return { lesson: r.lesson, title: l?.title ?? '?', stage: l?.stage ?? '?', rank: l?.rank ?? 9, role: r.role, adds: r.adds, anchor: r.anchor }; };
  const sortRungs = (rungs) => rungs.map(lessonRow).sort((a, b) => a.rank - b.rank || (a.role === b.role ? 0 : a.role === 'core' ? -1 : 1));
  const rows = [];
  if (flag('--cross')) {
    const s = state({ near: false, verify: false });
    const registry = registryOf(s.graph, site);
    const text = canonicalizePrompt({ area: '_cross', proposed: [] }, registry, { digestDir: join(S, 'digests'), answerFile: join(out, '_cross.json') });
    writeFileSync(join(dir, '_cross.md'), text);
    rows.push({ id: '_cross', prompt: join(dir, '_cross.md'), concepts: registry.length, tokens: tokens(text), answer: join(out, '_cross.json') });
    console.log(`canonicalize --cross: ${registry.length} concepts, ~${Math.round(tokens(text) / 1000)}k tokens  ${join(dir, '_cross.md')}`);
    const prior = existsSync(join(dir, 'MANIFEST.json')) ? JSON.parse(readFileSync(join(dir, 'MANIFEST.json'), 'utf8')).items.filter((x) => x.id !== '_cross') : [];
    manifest(dir, [...prior, ...rows], { answersIn: out });
  } else {
    const s = state({ canonical: false, near: false, verify: false });
    const registry = registryOf({ ...base, concepts: Object.fromEntries(Object.entries(s.info.afterProposals).filter(([id]) => base.concepts[id])) }, site);
    for (const a of AREAS) {
      const proposed = [...s.info.pending].filter(([id, pn]) => pn.area === a.id && s.info.afterProposals[id]).sort(([x], [y]) => x.localeCompare(y))
        .map(([id, pn]) => ({ id, defs: pn.defs, rungs: sortRungs(s.info.afterProposals[id].rungs) }));
      if (!proposed.length) continue;
      const existing = Object.entries(s.info.afterProposals).filter(([id, c]) => base.concepts[id] && c.area === a.id).sort(([x], [y]) => x.localeCompare(y))
        .map(([id, c]) => ({ id, inRegistry: true, defs: [{ name: c.name, blurb: c.blurb, area: c.area, aliases: c.aliases }], rungs: sortRungs(c.rungs) }));
      const text = canonicalizePrompt({ area: a.id, proposed, existing }, registry, { digestDir: join(S, 'digests'), answerFile: join(out, `${a.id}.json`) });
      writeFileSync(join(dir, `${a.id}.md`), text);
      rows.push({ id: a.id, prompt: join(dir, `${a.id}.md`), proposedIds: proposed.length, rungs: proposed.reduce((n, p) => n + p.rungs.length, 0), tokens: tokens(text), answer: join(out, `${a.id}.json`) });
      console.log(`${a.id.padEnd(20)} ${String(proposed.length).padStart(3)} new ids  ~${String(Math.round(tokens(text) / 1000)).padStart(3)}k tokens  ${join(dir, `${a.id}.md`)}`);
    }
    manifest(dir, rows, { answersIn: out });
    console.log(`canonicalize: ${rows.length} area prompt(s). After their answers are in, run "emit.mjs canonicalize --cross" for the pass across areas.`);
  }
}

// ------------------------------------------------------------------ near

else if (cmd === 'near') {
  const dir = stage('near');
  const out = answers('near');
  const s = state({ verify: false });
  const registry = registryOf(s.graph, site);
  const rows = [];
  for (const a of AREAS) {
    const mine = registry.filter((c) => c.area === a.id).map((c) => ({ ...c, near: s.graph.concepts[c.id].near })).filter((c) => flag('--all') || !c.near.length);
    if (!mine.length) continue;
    const ids = new Set(mine.map((c) => c.id));
    const hints = s.info.relations.filter((h) => ids.has(h.a) || ids.has(h.b)).filter((h) => s.graph.concepts[h.a] && s.graph.concepts[h.b] && h.a !== h.b);
    const text = nearPrompt(a.id, mine, registry, { hints, answerFile: join(out, `${a.id}.json`) });
    writeFileSync(join(dir, `${a.id}.md`), text);
    rows.push({ id: a.id, prompt: join(dir, `${a.id}.md`), concepts: mine.length, hints: hints.length, tokens: tokens(text), answer: join(out, `${a.id}.json`) });
    console.log(`${a.id.padEnd(20)} ${String(mine.length).padStart(3)} concepts  ~${String(Math.round(tokens(text) / 1000)).padStart(3)}k tokens  ${join(dir, `${a.id}.md`)}`);
  }
  manifest(dir, rows, { answersIn: out });
  console.log(`near: ${rows.length} area prompt(s) for ${rows.reduce((n, r) => n + r.concepts, 0)} concept(s)${flag('--all') ? '' : ' with no sideways hop yet (use --all to rewrite every concept)'}.`);
}

// ------------------------------------------------------------------ verify

else if (cmd === 'verify') {
  const dir = stage('verify');
  const out = answers('verify');
  const s = state({ verify: false });
  const digests = buildDigests(site);
  const every = Number(opt('--sample', 4));
  const budget = Number(opt('--budget', 45000));
  const picked = [];
  for (const [id, c] of Object.entries(s.graph.concepts)) {
    const core = c.rungs.filter((r) => r.role === 'core');
    const levels = new Set(core.map((r) => site.lessons.get(r.lesson)?.rank)).size;
    const sampled = parseInt(createHash('sha256').update(id).digest('hex').slice(0, 6), 16) % every === 0;
    if (!(flag('--all') || levels >= 2 || sampled)) continue;
    const ticket = ticketOf(id, c);
    const answer = join(out, `${id}.json`);
    if (existsSync(answer) && !flag('--force')) { try { if (JSON.parse(readFileSync(answer, 'utf8')).ticket === ticket) continue; } catch { /* rewrite the prompt */ } }
    const text = verifyPrompt({ id, ...c, ticket, rungs: c.rungs.map((r) => ({ ...r, stage: stageOf(r.lesson) })), films: c.films.map((k) => ({ key: k, title: site.films.get(k)?.title ?? '?' })) }, digests, { answerFile: answer, root: ROOT });
    writeFileSync(join(dir, `${id}.md`), text);
    picked.push({ id, prompt: join(dir, `${id}.md`), levels, coreRungs: core.length, why: levels >= 2 ? 'spans levels' : 'sample', ticket, tokens: tokens(text), answer });
  }
  // batches a single judge can hold: by area order (the file's order), filled up to the token budget
  const batches = [];
  let cur = { concepts: [], tokens: 0 };
  for (const p of picked) { if (cur.concepts.length && cur.tokens + p.tokens > budget) { batches.push(cur); cur = { concepts: [], tokens: 0 }; } cur.concepts.push(p.id); cur.tokens += p.tokens; }
  if (cur.concepts.length) batches.push(cur);
  manifest(dir, picked, { answersIn: out, batches: batches.map((b, i) => ({ batch: i + 1, ...b })) });
  const total = Object.keys(s.graph.concepts).length;
  console.log(`verify: ${picked.length} of ${total} concept(s) to judge (${picked.filter((p) => p.why === 'spans levels').length} spanning two or more levels, ${picked.filter((p) => p.why === 'sample').length} sampled 1 in ${every} from the rest); ${batches.length} batch(es) of at most ~${Math.round(budget / 1000)}k tokens; largest single prompt ~${Math.round(Math.max(0, ...picked.map((p) => p.tokens)) / 1000)}k. Manifest: ${join(dir, 'MANIFEST.json')}`);
}

// ------------------------------------------------------------------ status

else if (cmd === 'status') {
  const st = readStaging(S);
  const s = ingest({ base, site, staging: st });
  const pend = [...s.info.pending.keys()];
  console.log(`staging ${S}`);
  console.log(`  base graph: ${Object.keys(base.concepts).length} concepts, ${Object.keys(base.lessons).length} lesson records`);
  console.log(`  proposals: ${st.proposals.length} of ${site.lessons.size} lessons; missing ${site.lessons.size - new Set(st.proposals.map((p) => p.name)).size}`);
  console.log(`  canonical files: ${st.canonical.map((f) => f.name).join(', ') || 'none'}; new ids proposed: ${pend.length}`);
  console.log(`  near files: ${st.near.map((f) => f.name).join(', ') || 'none'}; verdict files: ${st.verify.length}`);
  console.log(`  merged graph right now: ${Object.keys(s.graph.concepts).length} concepts, ${Object.keys(s.graph.lessons).length} lesson records; ${s.log.rejected.length} rejected item(s); ${s.validation.errors.length} error(s)`);
  const missing = [...site.lessons.keys()].filter((x) => !st.proposals.some((p) => p.name === x));
  if (missing.length && missing.length <= 60) console.log(`  lessons with no proposal: ${missing.join(', ')}`);
}

// ------------------------------------------------------------------ mock answers (plumbing test only)

else if (cmd === 'mock') {
  const which = argv[1];
  if (!existsSync(join(S, 'MOCK'))) { console.error(`mock: refusing to write stand-in answers into ${S}: it has no MOCK marker file. Create one (touch ${join(S, 'MOCK')}) only in a throwaway staging folder.`); process.exit(2); }
  const AREA_OF = { 'biology-together': 'diversity', 'life-science': 'ecosystems', 'high-school-biology': 'cells', 'organismal-biology': 'plants', 'cell-biology': 'cells', genetics: 'genes', 'ecology-evolution': 'evolution', biochemistry: 'molecules', neuroscience: 'nervous-system', physiology: 'body', signaling: 'signaling', 'developmental-neuroscience': 'development', 'sensory-systems': 'senses' };
  const write = (kind, name, data) => writeFileSync(join(answers(kind), `${name}.json`), JSON.stringify(data, null, 1) + '\n');
  if (which === 'propose') {
    let i = 0, broken = 0;
    for (const l of site.lessons.values()) {
      i++;
      const have = existingEntries(base, l.slug);
      const first = [...l.h2][0] ?? null;
      const concepts = [...have];
      if (!have.some((e) => e.role === 'core')) {
        concepts.push({
          id: `mock-${l.slug}`.slice(0, 48).replace(/-$/, ''), role: 'core', anchor: l.rank === 0 ? 'the-big-idea' : first,
          new: { name: `Mock idea ${i}`, blurb: `A stand-in idea for lesson number ${i}, written by the plumbing test.`, area: AREA_OF[l.course] ?? 'methods', aliases: [`mock question ${i}`, `mock term ${i}`] },
          adds: `Stand-in note ${i}: the case in the first section.`, films: l.filmList.slice(0, 1).map((f) => f.key), why: 'Mock.',
        });
      }
      if (i % 7 === 0 && !concepts.some((e) => e.id === 'diffusion') && base.concepts.diffusion) concepts.push({ id: 'diffusion', role: 'uses' });
      // deliberate faults, so the rejection paths run: a bad anchor, a film from another lesson, a vague note, an unknown id
      if (i % 53 === 0) { concepts[concepts.length - 1].anchor = 'no-such-section'; broken++; }
      if (i % 61 === 0) { concepts.push({ id: 'mock-unknown-idea', role: 'uses' }); broken++; }
      if (i % 67 === 0 && concepts[0].role === 'core') { concepts[0] = { ...concepts[0], films: [...(concepts[0].films ?? []), 'action-potential/no-such-film'] }; broken++; }
      if (i % 71 === 0) { concepts.push({ id: `mock-vague-${i}`, role: 'core', anchor: first, new: { name: `Mock vague idea ${i}`, blurb: 'A stand-in idea whose note is vague on purpose.', area: 'methods', aliases: ['mock vague a ' + i, 'mock vague b ' + i] }, adds: 'Covers the topic in more detail.', films: [] }); broken++; }
      write('proposals', l.slug, { lesson: l.slug, hash: l.contentHash, opened_lesson: false, concepts, relations: i % 9 === 0 && concepts.length > 1 ? [{ a: concepts[0].id, b: concepts[1].id, note: 'Mock relation.' }] : [], notes: '' });
    }
    console.log(`mock propose: ${i} proposal file(s) written, ${broken} with a deliberate fault.`);
  } else if (which === 'canonicalize') {
    const s = state({ canonical: false, near: false, verify: false });
    let files = 0, merges = 0;
    for (const a of AREAS) {
      const ids = [...s.info.pending].filter(([id, pn]) => pn.area === a.id && s.info.afterProposals[id]).map(([id]) => id).sort();
      if (!ids.length) continue;
      const concepts = [], drop = [];
      // merge each run of three into the first, keep the rest as they are, and drop one
      for (let i = 0; i < ids.length; i++) {
        if (i === ids.length - 1 && ids.length > 4 && ids.length % 3 !== 1) { drop.push({ id: ids[i], why: 'Mock drop: stands in for a topic that is not an idea.' }); continue; }
        if (i % 3 === 0) concepts.push({ id: ids[i], merge: [ids[i]] });
        else { concepts[concepts.length - 1].merge.push(ids[i]); merges++; }
      }
      write('canonical', a.id, { area: a.id, concepts, drop, rungs: [], notes: 'mock' });
      files++;
    }
    console.log(`mock canonicalize: ${files} area file(s) written, ${merges} merge(s).`);
  } else if (which === 'cross') {
    const s = state({ near: false, verify: false });
    const ids = Object.keys(s.graph.concepts).filter((id) => id.startsWith('mock-'));
    const pair = ids.length >= 2 ? [ids[0], ids[ids.length - 1]] : [];
    write('canonical', '_cross', { area: '_cross', concepts: pair.length ? [{ id: pair[0], merge: pair }] : [], drop: [], rungs: [], notes: 'mock' });
    console.log(`mock cross: ${pair.length ? `merged ${pair[1]} into ${pair[0]}` : 'nothing to merge'}.`);
  } else if (which === 'near') {
    const s = state({ verify: false });
    const ids = Object.keys(s.graph.concepts);
    let files = 0;
    for (const a of AREAS) {
      const mine = ids.filter((id) => s.graph.concepts[id].area === a.id && !s.graph.concepts[id].near.length);
      if (!mine.length) continue;
      const near = {};
      mine.forEach((id, i) => {
        const to = ids[(ids.indexOf(id) + 1) % ids.length], to2 = ids[(ids.indexOf(id) + 7) % ids.length];
        near[id] = [{ id: to, why: 'A stand-in reason that names one shared mechanism in one sentence.' }, ...(to2 !== to && to2 !== id ? [{ id: to2, why: 'A second stand-in reason, also one sentence.' }] : [])];
        if (i === 0) near[id].push({ id, why: 'A hop to itself, which must be rejected.' });
        if (i === 1) near[id].push({ id: to2 === id ? to : ids[(ids.indexOf(id) + 3) % ids.length], why: 'This one mirrors the other, which is an analogy formula.' });
      });
      write('near', a.id, { area: a.id, near });
      files++;
    }
    console.log(`mock near: ${files} area file(s) written.`);
  } else if (which === 'verify') {
    const dir = join(S, 'prompts', 'verify', 'MANIFEST.json');
    if (!existsSync(dir)) { console.error('mock verify: run "emit.mjs verify" first (the mock answers the prompts it listed).'); process.exit(2); }
    const items = JSON.parse(readFileSync(dir, 'utf8')).items;
    const s = state({ verify: false });
    let n = 0, wrong = 0, notCore = 0, notes = 0, stale = 0;
    for (const it of items) {
      const c = s.graph.concepts[it.id];
      if (!c) continue;
      n++;
      const core = c.rungs.filter((r) => r.role === 'core');
      const rungs = core.map((r) => ({ lesson: r.lesson, verdict: 'ok' }));
      if (n % 5 === 0 && core.length >= 2) { rungs[rungs.length - 1] = { lesson: core[core.length - 1].lesson, verdict: 'wrong', why: 'Mock verdict: stands in for a lesson about a different idea.' }; wrong++; }
      else if (n % 7 === 0 && core.length >= 2) { rungs[0] = { lesson: core[0].lesson, verdict: 'not-core', why: 'Mock verdict: stands in for a lesson that only leans on the idea.' }; notCore++; }
      else if (n % 11 === 0) { rungs[0] = { lesson: core[0].lesson, verdict: 'note', adds: `Stand-in replacement note ${n}, naming one case.`, why: 'Mock verdict.' }; notes++; }
      let ticket = it.ticket;
      if (n % 23 === 0) { ticket = 'stale00000'; stale++; }
      write('verify', it.id, { concept: it.id, ticket, same_idea: true, rungs, bad_anchors: [], bad_films: [], bad_aliases: n % 13 === 0 && c.aliases.length > 2 ? [{ alias: c.aliases[c.aliases.length - 1], why: 'Mock: stands in for a phrase that is a different idea.' }] : [], notes: 'mock' });
    }
    console.log(`mock verify: ${n} verdict file(s) written: ${wrong} with a wrong rung, ${notCore} with a demotion, ${notes} with a replaced note, ${stale} with a stale ticket.`);
  } else { console.error('mock: say propose, canonicalize, cross, near or verify.'); process.exit(2); }
}

else if (cmd === 'clean') {
  // remove the prompt files of every stage (answers are never removed by this tool)
  if (existsSync(join(S, 'prompts'))) rmSync(join(S, 'prompts'), { recursive: true });
  console.log(`clean: removed ${join(S, 'prompts')}`);
}

else { console.error(`Unknown command "${cmd}".`); process.exit(2); }
