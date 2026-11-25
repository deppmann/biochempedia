#!/usr/bin/env node
/**
 * The production record: one row per lesson, in production/record/<course>.jsonl (one JSON object per
 * line, sorted by slug; one file per course so parallel batch PRs do not collide). Every tool that asks
 * "where does this lesson stand?" reads it: the homepage shelf (scripts/rewritten-shelf.mjs), the morning
 * heartbeat and the Course Progress dashboard, and the ship step writes it.
 *
 * The repository is public, so a row holds facts only: dates, PR numbers, model FAMILY (never a version),
 * film lengths, deck size, Side Hops count. No costs, no paths, no names, no copied notes. check-production-record.mjs
 * enforces that in CI.
 *
 *   node scripts/production-record.mjs table                    # per-course table
 *   node scripts/production-record.mjs derive                   # refresh the fields the tree determines
 *   node scripts/production-record.mjs set <slug> key=value ... # update one row (pipeline tools, ship step)
 *   node scripts/production-record.mjs get <slug>               # print one row
 *
 * `set` keys (lists are comma-separated; `+=` appends, `-=` removes):
 *   stage=<stage>  started=YYYY-MM-DD  shipped=YYYY-MM-DD  prs=301,305  pr+=340
 *   writer=<family>  gates=openai,claude  gates+=claude
 *   animator.<filmId>=<family>   (filmId as in the films list: explainer, chapter-2, ...)
 *   changed=text,flashcards,film   flags+=no-hex-mark   flags-=lesson-links-stale   subject=biology
 * After `set` the row is validated and the derivable fields refreshed, so it cannot drift from the tree.
 */
import { readFileSync, writeFileSync, readdirSync, existsSync, mkdirSync, unlinkSync } from 'node:fs';
import { join, dirname } from 'node:path';
import { fileURLToPath, pathToFileURL } from 'node:url';
import yaml from 'js-yaml';

export const ROOT = join(dirname(fileURLToPath(import.meta.url)), '..');
export const RECORD_DIR = 'production/record';

export const STAGES = ['live', 'written', 'gated', 'arbitrated', 'regated', 'trimmed', 'voiced', 'animated', 'framechecked', 'shipped'];
export const FAMILIES = ['claude', 'openai', 'gemini', 'unknown'];
export const SUBJECTS = ['biology'];
export const TIERS = ['families', 'highschool', 'foundation', 'core', 'elective', 'advanced'];
export const CHANGED = ['text', 'figures', 'flashcards', 'film'];
/** Open flags. single-film is derived (a shipped level-up still waiting for its film pair; never on a
 *  Biology Together guide, which has one parent film by design); the rest are set. */
export const FLAGS = ['safety-skipped', 'no-notes', 'single-film', 'no-hex-mark', 'lesson-links-stale'];
const KEYS = ['slug', 'course', 'subject', 'tier', 'stage', 'levelUp', 'text', 'films', 'deck', 'listen', 'sideHops', 'changed', 'flags'];
const DATE = /^\d{4}-\d{2}-\d{2}$/;
const SLUG = /^[a-z0-9]+(?:-[a-z0-9]+)*$/;

// ---------------------------------------------------------------- the tree

/** Lesson facts the tree determines: course, films (id, length), deck, Listen clips, tier. */
export async function readTree(root = ROOT) {
  const ldir = join(root, 'src/content/lessons');
  const { COURSES } = await import(pathToFileURL(join(root, 'src/data/courses.ts')).href);
  const tier = new Map(COURSES.map((c) => [c.slug, c.tier]));
  const listenPath = join(root, 'src/data/listen-manifest.json');
  const listen = existsSync(listenPath) ? JSON.parse(readFileSync(listenPath, 'utf8')) : {};
  const lessons = new Map();
  for (const slug of readdirSync(ldir).sort()) {
    const f = join(ldir, slug, 'lesson.mdx');
    if (!existsSync(f)) continue;
    const m = /^---\n([\s\S]*?)\n---/.exec(readFileSync(f, 'utf8'));
    const fm = (m && yaml.load(m[1])) || {};
    const films = [];
    if (fm.explainer) films.push({ id: 'explainer', durationSec: num(fm.explainer.durationSec) });
    for (const x of fm.films || []) films.push({ id: String(x.id), durationSec: num(x.durationSec) });
    const dp = join(root, 'src/data/flashcards', `${slug}.json`);
    let deck = null;
    if (existsSync(dp)) {
      const d = JSON.parse(readFileSync(dp, 'utf8'));
      deck = { cards: (d.cards || []).length, date: (d.generated && d.generated.date) || null };
    }
    const hp = join(root, 'src/data/side-hops', `${slug}.json`);
    let sideHops = null;
    if (existsSync(hp)) {
      const h = JSON.parse(readFileSync(hp, 'utf8'));
      sideHops = { hops: (h.hops || []).length, audioSec: num(h.audio?.durationSec), updated: h.updated };
    }
    const course = fm.course || 'biochemistry';
    lessons.set(slug, {
      course, tier: tier.get(course) || null, draft: fm.draft === true, films, deck, sideHops,
      listen: Array.isArray(listen[slug]) && listen[slug].length ? listen[slug].length : false,
    });
  }
  return { lessons, courseOrder: COURSES.map((c) => c.slug) };
}
const num = (v) => (typeof v === 'number' && Number.isFinite(v) ? v : null);

// ---------------------------------------------------------------- read / write

export function readRecord(root = ROOT) {
  const dir = join(root, RECORD_DIR);
  const rows = [];
  if (!existsSync(dir)) return rows;
  for (const f of readdirSync(dir).filter((x) => x.endsWith('.jsonl')).sort()) {
    readFileSync(join(dir, f), 'utf8').split('\n').forEach((line, i) => {
      if (!line.trim()) return;
      let row;
      try { row = JSON.parse(line); } catch (e) { throw new Error(`${RECORD_DIR}/${f}:${i + 1}: not JSON (${e.message})`); }
      Object.defineProperty(row, '_file', { value: f, enumerable: false });
      rows.push(row);
    });
  }
  return rows;
}

/** Canonical form: fixed key order, sorted lists, optional keys left out when empty. */
export function canonical(r) {
  const o = {};
  o.slug = r.slug; o.course = r.course; o.subject = r.subject || 'biology'; o.tier = r.tier; o.stage = r.stage || 'live';
  if (r.levelUp && (r.levelUp.started || r.levelUp.shipped || (r.levelUp.prs || []).length)) {
    const l = {};
    if (r.levelUp.started) l.started = r.levelUp.started;
    if (r.levelUp.shipped) l.shipped = r.levelUp.shipped;
    l.prs = [...new Set(r.levelUp.prs || [])].sort((a, b) => a - b);
    o.levelUp = l;
  }
  if (r.text) o.text = { writer: r.text.writer || 'unknown', gates: [...(r.text.gates || [])] };
  o.films = (r.films || []).map((f) => ({ id: f.id, durationSec: f.durationSec ?? null, animator: f.animator || 'unknown' }));
  o.deck = r.deck ? { cards: r.deck.cards, date: r.deck.date } : null;
  o.listen = r.listen || false;
  if (r.sideHops) o.sideHops = { hops: r.sideHops.hops, audioSec: r.sideHops.audioSec, updated: r.sideHops.updated };
  if (r.changed && r.changed.length) o.changed = CHANGED.filter((c) => r.changed.includes(c));
  o.flags = FLAGS.filter((f) => (r.flags || []).includes(f));
  return o;
}

export function writeRecord(rows, root = ROOT) {
  const dir = join(root, RECORD_DIR);
  mkdirSync(dir, { recursive: true });
  const by = new Map();
  for (const r of rows) {
    const c = canonical(r);
    if (!by.has(c.course)) by.set(c.course, []);
    by.get(c.course).push(c);
  }
  for (const f of readdirSync(dir).filter((x) => x.endsWith('.jsonl'))) {
    if (!by.has(f.slice(0, -6))) unlinkSync(join(dir, f));
  }
  for (const [course, list] of by) {
    list.sort((a, b) => a.slug.localeCompare(b.slug));
    writeFileSync(join(dir, `${course}.jsonl`), list.map((r) => JSON.stringify(r)).join('\n') + '\n');
  }
}

// ---------------------------------------------------------------- derive

/** Refresh the derivable fields of every row from the tree; add rows for new lessons, drop rows for
 *  lessons that are gone. Returns { rows, added, removed }. */
export function deriveRows(rows, tree) {
  const by = new Map(rows.map((r) => [r.slug, r]));
  const out = [];
  const added = [];
  for (const [slug, t] of tree.lessons) {
    let r = by.get(slug);
    if (!r) { r = { slug, stage: 'live', flags: [] }; added.push(slug); }
    const anim = new Map((r.films || []).map((f) => [f.id, f.animator]));
    const flags = (r.flags || []).filter((f) => f !== 'single-film');
    /* Biology Together guides get one parent film by design (Chris, 2026-11-22), so a shipped guide
       with one film is finished, not waiting for its pair. */
    if ((r.stage === 'shipped') && t.films.length === 1 && t.tier !== 'families') flags.push('single-film');
    out.push(canonical({
      ...r, course: t.course, subject: r.subject || 'biology', tier: t.tier,
      films: t.films.map((f) => ({ ...f, animator: anim.get(f.id) || 'unknown' })),
      deck: t.deck, listen: t.listen, sideHops: t.sideHops, flags,
    }));
  }
  const removed = rows.filter((r) => !tree.lessons.has(r.slug)).map((r) => r.slug);
  return { rows: out, added, removed };
}

// ---------------------------------------------------------------- validate

/** Content that must never reach the public record, checked on the raw text. */
export const FORBIDDEN = [
  [/"(?:usd|cost\w*|price\w*|tokens?|planPct)"\s*:/i, 'a cost key'],
  [/\$\s?\d/, 'a dollar amount'],
  [/\bclaude-[a-z]+-\d/i, 'a Claude model version'],
  [/\bgpt-/i, 'an OpenAI model version'],
  [/\bgemini-\d/i, 'a Gemini model version'],
  [/\/Users\/|\/Volumes\/|\/home\//, 'a local path'],
];

export function forbiddenIn(text) {
  return FORBIDDEN.filter(([re]) => re.test(text)).map(([, what]) => what);
}

export function validateRow(r) {
  const e = [];
  const bad = (m) => e.push(`${r.slug ?? '?'}: ${m}`);
  for (const k of Object.keys(r)) if (!KEYS.includes(k)) bad(`unknown key "${k}"`);
  if (!SLUG.test(r.slug || '')) bad('slug missing or malformed');
  if (typeof r.course !== 'string' || !SLUG.test(r.course)) bad('course missing');
  if (!SUBJECTS.includes(r.subject)) bad(`subject "${r.subject}" not one of ${SUBJECTS}`);
  if (r.tier !== null && !TIERS.includes(r.tier)) bad(`tier "${r.tier}"`);
  if (!STAGES.includes(r.stage)) bad(`stage "${r.stage}" not one of ${STAGES.join(', ')}`);
  if (r.levelUp !== undefined) {
    const l = r.levelUp;
    for (const k of Object.keys(l || {})) if (!['started', 'shipped', 'prs'].includes(k)) bad(`levelUp.${k} unknown`);
    if (l.started !== undefined && !DATE.test(l.started)) bad('levelUp.started is not YYYY-MM-DD');
    if (l.shipped !== undefined && !DATE.test(l.shipped)) bad('levelUp.shipped is not YYYY-MM-DD');
    if (!Array.isArray(l.prs) || l.prs.some((n) => !Number.isInteger(n) || n < 1)) bad('levelUp.prs must be PR numbers');
  }
  if ((r.stage === 'shipped') !== !!(r.levelUp && r.levelUp.shipped)) bad('stage "shipped" and levelUp.shipped go together');
  if (r.text !== undefined) {
    for (const k of Object.keys(r.text || {})) if (!['writer', 'gates'].includes(k)) bad(`text.${k} unknown`);
    if (!FAMILIES.includes(r.text.writer)) bad(`text.writer "${r.text.writer}" not a family (${FAMILIES})`);
    if (!Array.isArray(r.text.gates) || r.text.gates.some((g) => !FAMILIES.includes(g))) bad('text.gates must list families');
  }
  if (!Array.isArray(r.films)) bad('films must be a list');
  else for (const f of r.films) {
    for (const k of Object.keys(f)) if (!['id', 'durationSec', 'animator'].includes(k)) bad(`films[].${k} unknown`);
    if (!SLUG.test(f.id || '')) bad(`film id "${f.id}"`);
    if (f.durationSec !== null && typeof f.durationSec !== 'number') bad(`film ${f.id} durationSec`);
    if (!FAMILIES.includes(f.animator)) bad(`film ${f.id} animator "${f.animator}" not a family`);
  }
  if (r.deck !== null && (typeof r.deck !== 'object' || !Number.isInteger(r.deck.cards) || (r.deck.date !== null && !DATE.test(r.deck.date)))) bad('deck must be null or {cards, date}');
  if (!(r.listen === false || (Number.isInteger(r.listen) && r.listen > 0))) bad('listen must be false or a clip count');
  if (r.sideHops !== undefined) {
    const h = r.sideHops || {};
    for (const k of Object.keys(h)) if (!['hops', 'audioSec', 'updated'].includes(k)) bad(`sideHops.${k} unknown`);
    if (!Number.isInteger(h.hops) || h.hops < 1) bad('sideHops.hops must be a count');
    if (typeof h.audioSec !== 'number' || !(h.audioSec > 0)) bad('sideHops.audioSec must be a length in seconds');
    if (!DATE.test(h.updated || '')) bad('sideHops.updated is not YYYY-MM-DD');
  }
  if (r.changed !== undefined && (!Array.isArray(r.changed) || r.changed.some((c) => !CHANGED.includes(c)))) bad(`changed must list ${CHANGED}`);
  if (!Array.isArray(r.flags) || r.flags.some((f) => !FLAGS.includes(f))) bad(`flags must come from ${FLAGS.join(', ')}`);
  return e;
}

// ---------------------------------------------------------------- views

const skipped = (r) => (r.flags || []).includes('safety-skipped');
export const isLevelled = (r) => r.stage === 'shipped' && !skipped(r);
/** A levelled lesson whose film has had the level-up too: a chapter pair, or "film" in what changed. */
export const filmLevelled = (r) => isLevelled(r) && (r.films.length >= 2 || (r.changed || []).includes('film'));

export function courseTable(rows, courseOrder) {
  const order = [...courseOrder, ...[...new Set(rows.map((r) => r.course))].filter((c) => !courseOrder.includes(c)).sort()];
  return order.map((course) => {
    const rs = rows.filter((r) => r.course === course);
    return {
      course, lessons: rs.length,
      levelled: rs.filter(isLevelled).length,
      skipped: rs.filter(skipped).length,
      filmsLevelled: rs.filter(filmLevelled).length,
      pairs: rs.filter((r) => r.films.length >= 2).length,
      films: rs.reduce((n, r) => n + r.films.length, 0),
      decks: rs.filter((r) => r.deck).length,
      listen: rs.filter((r) => r.listen).length,
    };
  }).filter((t) => t.lessons);
}

export function formatTable(t) {
  const cols = ['course', 'lessons', 'levelled', 'skipped', 'filmsLevelled', 'pairs', 'films', 'decks', 'listen'];
  const tot = Object.fromEntries(cols.map((c) => [c, c === 'course' ? 'TOTAL' : t.reduce((n, r) => n + r[c], 0)]));
  const all = [...t, tot];
  const w = cols.map((c) => Math.max(c.length, ...all.map((r) => String(r[c]).length)));
  const line = (r) => cols.map((c, i) => (i ? String(r[c]).padStart(w[i]) : String(r[c]).padEnd(w[i]))).join('  ');
  return [line(Object.fromEntries(cols.map((c) => [c, c]))), ...t.map(line), line(tot)].join('\n');
}

/** The homepage "Recently rewritten" list: shipped level-ups, newest first. Safety-skipped lessons are
 *  not on it (Chris, 2026-11-15) and neither are drafts. */
export function shelf(rows, tree) {
  return rows
    .filter((r) => isLevelled(r) && r.levelUp.shipped && !(tree && tree.lessons.get(r.slug)?.draft))
    .map((r) => ({ slug: r.slug, date: r.levelUp.shipped, new: r.changed && r.changed.length ? r.changed : ['text'] }))
    .sort((a, b) => b.date.localeCompare(a.date) || a.slug.localeCompare(b.slug));
}

// ---------------------------------------------------------------- set

const list = (v) => (v === '' ? [] : v.split(',').map((s) => s.trim()).filter(Boolean));
function applyList(cur, op, vals) {
  if (op === '=') return vals;
  if (op === '+=') return [...cur, ...vals.filter((v) => !cur.includes(v))];
  return cur.filter((v) => !vals.includes(v));
}

export function setFields(row, pairs) {
  const r = JSON.parse(JSON.stringify(row));
  for (const p of pairs) {
    const m = /^([\w.-]+?)(\+=|-=|=)(.*)$/.exec(p);
    if (!m) throw new Error(`cannot read "${p}" (want key=value)`);
    const [, key, op, val] = m;
    const lu = () => (r.levelUp ||= { prs: [] });
    const tx = () => (r.text ||= { writer: 'unknown', gates: [] });
    if (key === 'stage' && op === '=') r.stage = val;
    else if (key === 'subject' && op === '=') r.subject = val;
    else if ((key === 'started' || key === 'levelUp.started') && op === '=') { if (val) lu().started = val; else if (r.levelUp) delete r.levelUp.started; }
    else if ((key === 'shipped' || key === 'levelUp.shipped') && op === '=') { if (val) lu().shipped = val; else if (r.levelUp) delete r.levelUp.shipped; }
    else if (['prs', 'pr', 'levelUp.prs'].includes(key)) lu().prs = applyList(lu().prs || [], op, list(val).map(Number));
    else if ((key === 'writer' || key === 'text.writer') && op === '=') tx().writer = val;
    else if (key === 'gates' || key === 'text.gates') tx().gates = op === '+=' ? [...tx().gates, ...list(val)] : applyList(tx().gates, op, list(val));
    else if (key === 'changed') r.changed = applyList(r.changed || [], op, list(val));
    else if (key === 'flags' || key === 'flag') r.flags = applyList(r.flags || [], op, list(val));
    else if (key.startsWith('animator.') && op === '=') {
      const id = key.slice('animator.'.length);
      const f = (r.films || []).find((x) => x.id === id);
      if (!f) throw new Error(`${r.slug}: no film "${id}" (films: ${(r.films || []).map((x) => x.id).join(', ') || 'none'}); add it to the lesson first`);
      f.animator = val;
    } else throw new Error(`unknown key or operator in "${p}"`);
  }
  return r;
}

// ---------------------------------------------------------------- CLI

async function main(argv) {
  const [cmd, ...args] = argv;
  if (cmd === 'table') {
    const tree = await readTree();
    console.log(formatTable(courseTable(readRecord(), tree.courseOrder)));
  } else if (cmd === 'derive') {
    const tree = await readTree();
    const { rows, added, removed } = deriveRows(readRecord(), tree);
    const errs = rows.flatMap(validateRow);
    if (errs.length) { console.error(errs.join('\n')); process.exit(1); }
    writeRecord(rows);
    console.log(`production-record: ${rows.length} rows derived${added.length ? `; added ${added.join(', ')}` : ''}${removed.length ? `; removed ${removed.join(', ')}` : ''}.`);
  } else if (cmd === 'get') {
    const r = readRecord().find((x) => x.slug === args[0]);
    if (!r) { console.error(`no row for ${args[0]}`); process.exit(1); }
    console.log(JSON.stringify(r, null, 1));
  } else if (cmd === 'set') {
    const [slug, ...pairs] = args;
    if (!slug || !pairs.length) { console.error('usage: production-record.mjs set <slug> key=value ...'); process.exit(2); }
    const tree = await readTree();
    if (!tree.lessons.has(slug)) { console.error(`no lesson ${slug}`); process.exit(1); }
    const { rows } = deriveRows(readRecord(), tree);
    const i = rows.findIndex((r) => r.slug === slug);
    const next = setFields(rows[i], pairs);
    const { rows: done } = deriveRows([...rows.slice(0, i), next, ...rows.slice(i + 1)], tree);
    const row = done.find((r) => r.slug === slug);
    const errs = [...validateRow(row), ...forbiddenIn(JSON.stringify(row)).map((w) => `${slug}: ${w}`)];
    if (errs.length) { console.error(errs.join('\n')); process.exit(1); }
    writeRecord(done);
    console.log(JSON.stringify(row));
  } else {
    console.error('usage: production-record.mjs table | derive | get <slug> | set <slug> key=value ...');
    process.exit(2);
  }
}

if (import.meta.url === pathToFileURL(process.argv[1] || '').href) {
  main(process.argv.slice(2)).catch((e) => { console.error(e.message || e); process.exit(1); });
}
