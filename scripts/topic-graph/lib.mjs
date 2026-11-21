/* The hop graph: shared, model-free helpers.

   src/data/topic-graph.json says which IDEAS the site teaches and where: a concept ("osmosis") has
   a ladder of lessons that teach it at different levels (its `core` rungs, each with a short note on
   what that level adds), lessons that lean on it (`uses`), the films that show it, and sideways hops
   to neighbouring ideas (`near`). It is written offline, checked in, and read at build time; no
   model runs when someone visits. See README.md in this folder.

   This file loads the site from source (through the lesson-links loader, so the two tools cannot
   disagree about what a live lesson is), holds the rules every part of the graph must pass, and
   puts a graph into its one fixed order. The tools use the rules to clean what a model wrote;
   scripts/check-topic-graph.mjs uses them in CI. Nothing here calls a model. */

import { readFileSync, existsSync } from 'node:fs';
import { join } from 'node:path';
import { createHash } from 'node:crypto';
import { loadSite, plain, ROOT, sentenceCount, words, VAGUE, FILLER, ANALOGY, MEDICAL, BRANDS } from '../lesson-links/lib.mjs';
import { headingIds, makeTopicGraph, fold } from '../../src/lib/topic-graph-core.mjs';

export { ROOT, fold, makeTopicGraph, headingIds };
export const GRAPH_FILE = join(ROOT, 'src', 'data', 'topic-graph.json');
export const CACHE_DIR = join(ROOT, 'node_modules', '.cache', 'topic-graph');

/** The shelves a concept can sit on: one each, for browsing. Names are written for a grade 7 reader. */
export const AREAS = [
  { id: 'cells', name: 'Cells' },
  { id: 'molecules', name: 'Molecules of life' },
  { id: 'energy', name: 'Energy and metabolism' },
  { id: 'genes', name: 'Genes and heredity' },
  { id: 'evolution', name: 'Evolution' },
  { id: 'diversity', name: 'The variety of life' },
  { id: 'ecosystems', name: 'Ecosystems' },
  { id: 'plants', name: 'Plants' },
  { id: 'body', name: 'How bodies work' },
  { id: 'microbes-immunity', name: 'Microbes and immunity' },
  { id: 'nervous-system', name: 'Nerves and the brain' },
  { id: 'senses', name: 'Senses' },
  { id: 'signaling', name: 'Signals between cells' },
  { id: 'development', name: 'Growth and development' },
  { id: 'methods', name: 'How we know' },
];
export const SUBJECTS = ['biology'];
export const ROLES = ['core', 'uses'];

export const LIMITS = {
  blurbWords: 22, addsWords: 14, whyWords: 22, nameChars: 60, idChars: 48,
  /** A concept whose name is longer than `shortOver` characters carries a `short` display name of at most `shortChars`. */
  shortChars: 26, shortOver: 24,
  aliasMin: 2, aliasMax: 5, aliasWords: 12, nearMax: 4,
  corePerLesson: 3, usesPerLesson: 4,
  /** What a reader may propose for one lesson in a fill (the graph itself allows usesPerLesson). */
  usesPerProposal: 2,
  areasMin: 12, areasMax: 16,
};

export const ABOUT = 'Which ideas the site teaches and where. Each concept lists the lessons that teach it at each level (core, with a note on what that level adds), lessons that lean on it (uses), the films that show it and neighbouring ideas (near). Written offline by AI models from the lessons themselves (scripts/topic-graph), merged into one id per idea, read again by a second model that did not write it, and checked in CI by scripts/check-topic-graph.mjs. A lesson record is tied to the lesson\'s teaching text by hash; refresh with scripts/topic-graph/assign.mjs after a rewrite. Titles, courses and levels are not stored here: the site joins them at build time.';

// ------------------------------------------------------------------ the site, with what the graph needs

/** A film's key: its path under /explainers/ without ".mp4" (the same key "watched" marks use). */
export const filmKey = (src) => String(src).replace(/^\/explainers\//, '').replace(/\.mp4$/, '');

const oneLine = (s) => String(s ?? '').replace(/\s+/g, ' ').trim();

/**
 * The hash a record is tied to: the lesson's TEACHING text only (hook, summary, objectives,
 * headings and the body prose a reader sees). Quiz questions, film and simulation credits,
 * dates and every other frontmatter field are left out on purpose, so a scripted branding
 * replace or a new practice question does not mark the record stale; a rewritten section or a
 * reworded heading does.
 */
export function contentHash(l) {
  const parts = [
    oneLine(l.fm?.hook ?? ''), oneLine(l.summary), ...(l.objectives ?? []).map(oneLine),
    ...headingIds(l.body).map((h) => `${'#'.repeat(h.depth)} ${h.text}`),
    plain(l.body).replace(/\s+/g, ' '),
  ];
  return createHash('sha256').update(parts.join('\n')).digest('hex').slice(0, 16);
}

/** The first `n` sentences of a block of prose. */
export function leadSentences(text, n = 2, max = 420) {
  const t = oneLine(text);
  if (!t) return '';
  const parts = t.split(/(?<=[.?!])\s+(?=[A-Z0-9"“(])/);
  let out = parts.slice(0, n).join(' ');
  if (out.length > max) out = out.slice(0, max).replace(/\s+\S*$/, '') + '…';
  return out;
}

/** Each `##` section of a body: heading, the id the built page gives it, and the prose under it
 *  (up to the next `##`; `###` headings inside it are listed as `sub`). */
export function sectionsOf(body) {
  const heads = headingIds(body);
  const lines = String(body).split('\n');
  const h2 = heads.filter((h) => h.depth === 2);
  return h2.map((h, i) => {
    const end = i + 1 < h2.length ? h2[i + 1].line : lines.length;
    const inner = lines.slice(h.line + 1, end);
    const sub = heads.filter((x) => x.depth === 3 && x.line > h.line && x.line < end).map((x) => ({ text: x.text, id: x.id }));
    const prose = plain(inner.filter((ln) => !/^#{1,6}\s/.test(ln)).join('\n'));
    return { heading: h.text, id: h.id, sub, text: prose, words: words(prose) };
  });
}

/**
 * loadSite() from scripts/lesson-links, plus what the graph needs on each lesson: the content
 * hash, heading ids, films with their keys, and one table of every lesson film by key.
 */
export async function loadGraphSite() {
  const site = await loadSite();
  const films = new Map();
  for (const l of site.lessons.values()) {
    const d = l.fm ?? {};
    l.contentHash = contentHash(l);
    l.heads = headingIds(l.body);
    l.h2 = new Set(l.heads.filter((h) => h.depth === 2).map((h) => h.id));
    l.filmList = [
      ...(d.explainer?.src ? [{ ...d.explainer, id: null }] : []),
      ...(d.films ?? []).filter((f) => f.src),
    ].map((f, i) => ({
      key: filmKey(f.src), id: f.id ?? null, title: f.title, takeaways: f.takeaways ?? [], captions: f.captions ?? null,
      durationSec: f.durationSec, poster: f.poster, lesson: l.slug, n: i,
      href: f.id ? `/watch/${l.slug}/${f.id}/` : `/watch/${l.slug}/`,
    }));
    for (const f of l.filmList) if (!films.has(f.key)) films.set(f.key, f);
  }
  site.films = films;
  return site;
}

/** The shape src/lib/topic-graph-core.mjs wants, from a loaded site. */
export function coreSite(site) {
  const lessons = new Map([...site.lessons.values()].map((l) => [l.slug, {
    slug: l.slug, title: l.title, course: l.course, courseTitle: l.courseTitle, stage: l.stage, stageTitle: l.stageTitle, rank: l.rank, order: l.n, hook: l.hook, headingIds: l.h2,
  }]));
  const courses = site.COURSES.map((c) => ({ slug: c.slug, title: c.title, stage: site.courseInfo.get(c.slug).stage }));
  return { stages: site.STAGES.map((s) => ({ key: s.key, title: s.title })), lessons, films: site.films, courses };
}

/** The first sentences a film says, from its captions file (for films with no take-homes listed). */
export function filmOpening(f, n = 3) {
  const file = f.captions ? join(ROOT, 'public', f.captions) : null;
  if (!file || !existsSync(file)) return '';
  const text = readFileSync(file, 'utf8').split('\n')
    .filter((ln) => ln.trim() && !/^WEBVTT|^NOTE\b|-->|^\d+$/.test(ln.trim()))
    .map((ln) => ln.replace(/<[^>]+>/g, '').trim()).join(' ');
  return leadSentences(text, n, 360);
}

export const readGraph = (file = GRAPH_FILE) => (existsSync(file) ? JSON.parse(readFileSync(file, 'utf8')) : null);
export const emptyGraph = () => ({ version: 1, updated: new Date().toISOString().slice(0, 10), about: ABOUT, areas: AREAS.map((a) => ({ ...a })), concepts: {}, lessons: {} });

// ------------------------------------------------------------------ the wording rules

export const KEBAB = /^[a-z0-9]+(-[a-z0-9]+)*$/;
/** A note that says nothing about what the lesson adds. */
export const ADDS_VAGUE = /\b(deeper dive|deep dive|explores?|advanced concepts?|in more detail|more detail|more depth|in depth|in-depth|is related|related topic|covers?|overview of|introduction to|introduces?|learn about|a closer look|takes? (it|this) further|builds? on)\b/i;
/** Names the graph's reader-facing copy never carries, beyond the list lesson links already enforce. */
export const EXTRA_NAMES = /\b(jell-?o|mcat)\b/i;
const HYPE = /\b(amazing|incredible|fascinating|awesome|mind-?blowing|delve|revolutionary|game-?chang\w+)\b/i;

// The medical-advice and analogy rules come from lesson links, where they judge search phrases a
// student types and one-line reasons. The graph's copy is different: it NAMES science, so it says
// "dose-response curve", "dosage compensation", "parallel fibres" and "mirror drawing". Lesson links
// keeps its rules as they are; the graph reads them with the allowances below. Each allowance lets
// a plain scientific word through and leaves the advice frame or the analogy formula failing.

/** "dose" not followed by the word that makes it a term of science (dose-response, dosage compensation). */
const DOSE = String.raw`dos(?:e|age)s?(?![- ](?:response|dependen|compensation|effect|sensitiv|curve))`;
/** A dose asked for, not named: "what dose", "safe dosage", "how much ... dose", "dose for my child". */
const DOSE_ADVICE = new RegExp(String.raw`\b(?:what|safe|safest|recommended|my|your|child'?s?) (?:is (?:the|a) )?(?:[\w-]+ )?${DOSE}\b|\bhow (?:much|many|big) (?:[\w-]+ ){0,3}${DOSE}\b|\b${DOSE} (?:for|to give) (?:my|me|your|a child|a baby|kids?|children|babies|adults?|toddlers?|dogs?|cats?)\b`, 'i');
/** A treatment asked for: "how to treat my rash", "cure your cold". ("How doctors treat cancer" is a topic.) */
const TREAT_ADVICE = /\bhow (?:to|do i|can i|should i|do you|can you) (?:treat|cure)\b|\b(?:treat|cure|heal)(?:ing)? (?:my|your)\b/i;
/**
 * True when a string is phrased as a request for medical advice. The lesson-links rule, except
 * that the bare words "dose" and "dosage" pass (they are judged by DOSE_ADVICE instead), plus the
 * "how to treat my" frame, which lesson links does not look for.
 */
export function medicalAdvice(s) {
  const t = String(s ?? '');
  // "where it is safe to act" describes; "is it safe to take" asks. Only the asking frame is advice.
  const plainSafe = t.replace(/(?<!\bis it )\bsafe to (?!take|eat|drink|use|give|swallow|touch|mix|stop|swim|breathe)/gi, 'fine to ');
  return MEDICAL.test(plainSafe.replace(/\bdos(?:e|age)\b/gi, 'amount')) || DOSE_ADVICE.test(t) || TREAT_ADVICE.test(t);
}

const DET = String.raw`(?:the|a|an|how|what|that|this|those|these|its|their|each|our|every)`;
/** Words the lesson-links analogy rule stops on that are plain vocabulary here. */
const PLAIN_SCIENCE = [
  // "parallel" as a description (parallel fibres, in parallel, runs parallel to the surface). Still an
  // analogy: the verb ("parallels X", "parallel the ...") and the noun ("a parallel to", "a close parallel with").
  new RegExp(String.raw`\bparallel\b(?! ${DET}\b)(?!(?<=\b(?:a|an|one|close|direct|clear|striking|exact|obvious) parallel) (?:to|with|between|in|for)\b)`, 'gi'),
  // "mirror" as a thing (mirror drawing, mirror image, mirror neurons). Still an analogy: the verb ("mirrors X", "mirror the ...").
  new RegExp(String.raw`\bmirror\b(?! ${DET}\b)`, 'gi'),
  // analogous structures are a term of evolution, set against homologous ones
  /\banalogous(?= (?:traits?|structures?|organs?|features?|characters?|limbs?|wings?)\b)|(?<=\bhomologous (?:and|or|versus|vs\.?) )analogous\b/gi,
  // stimulus contrast in vision ("changes in contrast")
  /(?<=\b(?:changes?|differences?|increases?|decreases?|steps?|variations?|rise|fall|drop|gain) )in contrast\b/gi,
];
/** The simile formulas lesson links does not look for: "X is like a Y", "works like a", "think of it as". */
const SIMILE = /\b(?:is|are|was|were) (?:a (?:bit|little|lot) |much |just |rather |somewhat |more |very much )?like (?:a|an|the|how|what|when)\b|\bworks? (?:just |much )?like (?:a|an|the)\b|\bthink of (?:it|this|that|them|these|those|(?:(?:a|an|the|each|every|your) )?[\w-]+(?: [\w-]+)?) as\b/i;
/**
 * True when a string rests on an analogy or a contrast formula instead of saying what happens. The
 * lesson-links rule read past the plain scientific uses above, plus the simile formulas.
 */
export function analogyFormula(s) {
  let t = String(s ?? '');
  for (const re of PLAIN_SCIENCE) t = t.replace(re, 'plain');
  return ANALOGY.test(t) || SIMILE.test(t);
}

/** Problems any reader-facing string can have. Returns a list of reasons, empty when clean. */
export function copyProblems(s) {
  const t = String(s ?? '');
  const out = [];
  if (!t.trim()) out.push('empty');
  if (/[—–]/.test(t)) out.push('dash character (use a comma, a colon or two sentences)');
  if (/\p{Extended_Pictographic}/u.test(t)) out.push('emoji');
  // "the next step" in lower case is plain English here; lesson links stops on it as a company name.
  if (BRANDS.test(t.replace(/\bnext step\b/g, 'following step')) || EXTRA_NAMES.test(t)) out.push('names a product, company or test');
  if (medicalAdvice(t)) out.push('medical-advice phrasing');
  if (HYPE.test(t)) out.push('hype word');
  if (/\s{2,}|^\s|\s$/.test(t)) out.push('stray whitespace');
  return out;
}

export function idProblem(id) {
  if (typeof id !== 'string' || !KEBAB.test(id)) return 'id is not kebab-case (lower-case letters, digits, single hyphens)';
  if (id.length > LIMITS.idChars) return `id longer than ${LIMITS.idChars} characters`;
  return '';
}
export function nameProblem(name) {
  const p = copyProblems(name);
  if (p.length) return p[0];
  if (name.length > LIMITS.nameChars) return `name longer than ${LIMITS.nameChars} characters`;
  if (/[.?!]$/.test(name)) return 'name ends with punctuation';
  return '';
}
export function shortProblem(short, name) {
  const p = copyProblems(short);
  if (p.length) return p[0];
  if (short.length > LIMITS.shortChars) return `short name longer than ${LIMITS.shortChars} characters`;
  if (name != null && short.length >= name.length) return 'short name is not shorter than the name';
  if (/[.?!:,;(]$/.test(short)) return 'short name ends with punctuation';
  return '';
}
export function blurbProblem(blurb) {
  const p = copyProblems(blurb);
  if (p.length) return p[0];
  if (sentenceCount(blurb) !== 1) return 'blurb is not one sentence';
  if (words(blurb) > LIMITS.blurbWords) return `blurb is ${words(blurb)} words (limit ${LIMITS.blurbWords})`;
  if (analogyFormula(blurb)) return 'analogy formula';
  return '';
}
export function addsProblem(adds) {
  const p = copyProblems(adds);
  if (p.length) return p[0];
  if (words(adds) > LIMITS.addsWords) return `note is ${words(adds)} words (limit ${LIMITS.addsWords})`;
  if (ADDS_VAGUE.test(adds)) return 'vague note (says "covers" or "more detail" instead of naming the case, experiment or number)';
  if (VAGUE.test(adds) || FILLER.test(adds)) return 'vague or filler note';
  if (analogyFormula(adds)) return 'analogy formula';
  return '';
}
export function whyProblem(why) {
  const p = copyProblems(why);
  if (p.length) return p[0];
  if (sentenceCount(why) !== 1) return 'reason is not one sentence';
  if (words(why) > LIMITS.whyWords) return `reason is ${words(why)} words (limit ${LIMITS.whyWords})`;
  if (analogyFormula(why)) return 'analogy or contrast formula (name a shared mechanism or a real case instead)';
  if (VAGUE.test(why) || FILLER.test(why)) return 'vague or filler reason';
  return '';
}
export function aliasProblem(alias) {
  const p = copyProblems(alias);
  if (p.length) return p[0];
  if (words(alias) > LIMITS.aliasWords) return `alias longer than ${LIMITS.aliasWords} words`;
  if (/[.!]$/.test(alias)) return 'alias ends with punctuation';
  if (/\bspell/i.test(alias)) return 'says "spelled"';
  return '';
}

// ------------------------------------------------------------------ one fixed order

/**
 * Put a graph into its one canonical order and rebuild the reverse index, so the same content
 * always gives the same bytes: concepts by area then id; a concept's rungs core first, then by
 * level, course and place in the course; films in the same order; aliases and near as written.
 * Lesson records keep their hash (a lesson that has rungs but no hash yet gets `hashFor(slug)`).
 */
export function normalizeGraph(graph, site, { hashFor } = {}) {
  const areaIdx = new Map(graph.areas.map((a, i) => [a.id, i]));
  const pos = (slug) => { const l = site.lessons.get(slug); return l ? [l.rank, l.courseIdx, l.n] : [99, 99, 999]; };
  const cmpLesson = (a, b) => { const x = pos(a), y = pos(b); return x[0] - y[0] || x[1] - y[1] || x[2] - y[2] || a.localeCompare(b); };
  const ids = Object.keys(graph.concepts).sort((a, b) => ((areaIdx.get(graph.concepts[a].area) ?? 99) - (areaIdx.get(graph.concepts[b].area) ?? 99)) || a.localeCompare(b));
  const concepts = {};
  const index = {};
  for (const id of ids) {
    const c = graph.concepts[id];
    const rungs = [...c.rungs].sort((a, b) => (a.role === b.role ? 0 : a.role === 'core' ? -1 : 1) || cmpLesson(a.lesson, b.lesson))
      .map((r) => (r.role === 'core' ? { lesson: r.lesson, role: 'core', ...(r.anchor ? { anchor: r.anchor } : {}), adds: r.adds } : { lesson: r.lesson, role: r.role }));
    const films = [...c.films].sort((a, b) => {
      const fa = site.films.get(a), fb = site.films.get(b);
      return cmpLesson(fa?.lesson ?? a.split('/')[0], fb?.lesson ?? b.split('/')[0]) || (fa?.n ?? 0) - (fb?.n ?? 0) || a.localeCompare(b);
    });
    concepts[id] = { name: c.name, ...(c.short ? { short: c.short } : {}), blurb: c.blurb, area: c.area, subject: c.subject ?? 'biology', aliases: [...(c.aliases ?? [])], rungs, films, near: (c.near ?? []).map((n) => ({ id: n.id, why: n.why })) };
    for (const r of rungs) (index[r.lesson] ??= { core: [], uses: [] })[r.role === 'core' ? 'core' : 'uses'].push(id);
  }
  const lessons = {};
  const slugs = new Set([...Object.keys(index), ...Object.keys(graph.lessons ?? {})]);
  for (const slug of [...slugs].sort()) {
    const prior = graph.lessons?.[slug];
    const hash = prior?.hash ?? hashFor?.(slug);
    // Order within a lesson is data: the main idea first (see mainIdeaOrder). What the record already
    // says is kept, core before uses; an idea the record does not list yet goes after its kind.
    const at = new Map((prior?.concepts ?? []).map((id, i) => [id, i]));
    const keep = (ids) => [...ids].sort((a, b) => (at.get(a) ?? 1e6) - (at.get(b) ?? 1e6));
    const list = index[slug] ? [...keep(index[slug].core), ...keep(index[slug].uses)] : [];
    if (!list.length && !prior) continue;
    lessons[slug] = { hash, concepts: list };
  }
  return { version: 1, updated: graph.updated, about: graph.about ?? ABOUT, areas: graph.areas.map((a) => ({ id: a.id, name: a.name })), concepts, lessons };
}

/**
 * The ideas of one lesson, main idea first. A lesson's main idea is the core idea its title names:
 * the one whose name, short name or id shares the most words with the lesson's title and slug.
 * Ties go to the idea whose anchored section is longer, then to the section that comes first on
 * the page. Uses follow, by id. It is a rule, not a judgment, so it gives the same
 * answer every time; a review file can overrule it for one lesson ("order").
 */
export function mainIdeaOrder(slug, graph, site) {
  const l = site.lessons.get(slug);
  const mine = Object.entries(graph.concepts).flatMap(([id, c]) => c.rungs.filter((r) => r.lesson === slug).map((r) => ({ id, c, r })));
  if (!l) return mine.map((m) => m.id);
  const stemOf = (w) => w.replace(/ies$/, 'y').replace(/(es|s)$/, '');
  const wordsOf = (s) => new Set(fold(s).split(' ').filter((w) => w.length > 2).map(stemOf));
  const title = wordsOf(`${l.title} ${slug.replace(/-/g, ' ')}`);
  const sections = sectionsOf(l.body);
  const score = (m) => {
    const w = wordsOf(`${m.c.name} ${m.c.short ?? ''} ${m.id.replace(/-/g, ' ')}`);
    const hit = [...w].filter((x) => title.has(x)).length;
    const i = sections.findIndex((s) => s.id === m.r.anchor);
    return [hit, i >= 0 ? sections[i].words : 0, i >= 0 ? -i : -99];
  };
  const core = mine.filter((m) => m.r.role === 'core').map((m) => ({ ...m, s: score(m) })).sort((a, b) => b.s[0] - a.s[0] || b.s[1] - a.s[1] || b.s[2] - a.s[2] || a.id.localeCompare(b.id));
  return [...core.map((m) => m.id), ...mine.filter((m) => m.r.role !== 'core').map((m) => m.id).sort()];
}

export const serializeGraph = (graph) => JSON.stringify(graph, null, 1) + '\n';

// ------------------------------------------------------------------ the check

/**
 * Every rule a committed graph must pass. Returns { errors, warnings, notes, stats }.
 *   errors    a broken record: the build must not ship it
 *   warnings  honest states that need attention but must not block anyone: a live lesson with no
 *             record, a record older than its lesson's teaching text, an anchor that no longer
 *             matches a heading (the link falls back to the top of the lesson)
 * `opts.builtHeadings(slug)` may return the h2 ids of the BUILT page (a Set) so anchors are
 * checked against what readers get; without it they are checked against ids computed from source.
 * `opts.namesPending` (ingest only, before the canonicalize stage has answered) turns "two ids
 * with one name" from an error into a warning; the pairs are returned as `sameName` either way.
 */
export function validateGraph(graph, site, opts = {}) {
  const errors = [], warnings = [], notes = [];
  const E = (m) => errors.push(m), W = (m) => warnings.push(m);
  const stats = { concepts: 0, core: 0, uses: 0, films: 0, near: 0, anchors: 0, lessons: 0 };
  if (!graph || typeof graph !== 'object') return { errors: ['not a graph'], warnings, notes, stats, sameName: [] };
  if (graph.version !== 1) E(`version is ${graph.version}, expected 1`);
  if (!/^\d{4}-\d{2}-\d{2}$/.test(graph.updated ?? '')) E('header has no updated date');
  if (typeof graph.about !== 'string' || !graph.about) E('header has no about text');
  else for (const p of copyProblems(graph.about).filter((x) => x !== 'hype word')) E(`about: ${p}`);
  const areas = Array.isArray(graph.areas) ? graph.areas : [];
  if (areas.length < LIMITS.areasMin || areas.length > LIMITS.areasMax) E(`${areas.length} areas (expected ${LIMITS.areasMin} to ${LIMITS.areasMax})`);
  const areaIds = new Set();
  for (const a of areas) {
    if (!KEBAB.test(a?.id ?? '')) E(`area id "${a?.id}" is not kebab-case`);
    if (areaIds.has(a.id)) E(`area "${a.id}" listed twice`);
    areaIds.add(a.id);
    if (!a.name || copyProblems(a.name).length) E(`area "${a.id}": bad name`);
  }
  const concepts = graph.concepts && typeof graph.concepts === 'object' ? graph.concepts : {};
  const names = new Map();
  const sameName = [];
  for (const [id, c] of Object.entries(concepts)) {
    const k = fold(c?.name ?? '');
    if (!names.has(k)) { names.set(k, id); continue; }
    sameName.push({ id, other: names.get(k), name: c.name });
    // Two readers who each met an idea first often give it one name under two ids. Giving each idea one
    // id is the canonicalize stage's job, so before that stage has answered this is work still to do;
    // in a graph that is about to be written, or one that is committed, it is a broken record.
    if (opts.namesPending) W(`${id}: same name as ${names.get(k)} ("${c.name}"): the canonicalize stage must merge the two or rename one; this fails the final ingest`);
    else E(`${id}: same name as ${names.get(k)} ("${c.name}")`);
  }
  const aliasOwner = new Map();
  const labels = new Map(names);
  const want = {};
  const coreBy = {}, usesBy = {};
  for (const [id, c] of Object.entries(concepts)) {
    stats.concepts++;
    const ip = idProblem(id);
    if (ip) E(`${id}: ${ip}`);
    const missing = ['name', 'blurb', 'area', 'subject', 'aliases', 'rungs', 'films', 'near'].filter((k) => c?.[k] == null);
    if (missing.length) { E(`${id}: missing ${missing.join(', ')}`); continue; }
    if (!Array.isArray(c.aliases) || !Array.isArray(c.rungs) || !Array.isArray(c.films) || !Array.isArray(c.near)) { E(`${id}: aliases, rungs, films and near must be lists`); continue; }
    if (!SUBJECTS.includes(c.subject)) E(`${id}: subject "${c.subject}" is not one of ${SUBJECTS.join(', ')}`);
    if (!areaIds.has(c.area)) E(`${id}: unknown area "${c.area}"`);
    const np = nameProblem(c.name); if (np) E(`${id}: name: ${np}`);
    if (c.short != null) {
      const sp = typeof c.short !== 'string' ? 'not a string' : shortProblem(c.short, c.name); if (sp) E(`${id}: short name: ${sp}`);
      const k = fold(c.short ?? '');
      if (labels.has(k) && labels.get(k) !== id) E(`${id}: short name "${c.short}" is the name or short name of ${labels.get(k)}`);
      labels.set(k, id);
    } else if (c.name.length > LIMITS.shortOver) W(`${id}: the name is ${c.name.length} characters and has no short display name`);
    const bp = blurbProblem(c.blurb); if (bp) E(`${id}: blurb: ${bp}`);
    if (c.aliases.length > LIMITS.aliasMax) E(`${id}: ${c.aliases.length} aliases (limit ${LIMITS.aliasMax})`);
    if (c.aliases.length < LIMITS.aliasMin) W(`${id}: only ${c.aliases.length} alias(es); a concept needs ${LIMITS.aliasMin} to ${LIMITS.aliasMax} everyday phrases to be found`);
    for (const a of c.aliases) {
      const ap = aliasProblem(a); if (ap) E(`${id}: alias "${a}": ${ap}`);
      const k = fold(a);
      const named = names.get(k);
      if (named && named !== id) E(`${id}: alias "${a}" is the name of ${named}`);
      if (named === id) E(`${id}: alias "${a}" repeats the concept's own name`);
      if (aliasOwner.has(k) && aliasOwner.get(k) !== id) E(`${id}: alias "${a}" is also an alias of ${aliasOwner.get(k)} (give each phrase to one concept)`);
      else if (aliasOwner.get(k) === id) E(`${id}: alias "${a}" listed twice`);
      aliasOwner.set(k, id);
    }
    const seen = new Set();
    let cores = 0;
    for (const r of c.rungs) {
      const l = site.lessons.get(r?.lesson);
      if (!l) { E(`${id}: "${r?.lesson}" is not a live lesson (drafted, renamed or removed)`); continue; }
      if (seen.has(r.lesson)) E(`${id}: ${r.lesson} listed twice`);
      seen.add(r.lesson);
      (want[r.lesson] ??= []).push(id);
      if (!ROLES.includes(r.role)) { E(`${id}/${r.lesson}: role "${r.role}"`); continue; }
      if (r.role === 'core') {
        cores++; stats.core++; (coreBy[r.lesson] ??= []).push(id);
        if (!r.adds) E(`${id}/${r.lesson}: core rung without a note on what this level adds`);
        else { const p = addsProblem(r.adds); if (p) E(`${id}/${r.lesson}: ${p}: "${r.adds}"`); }
        if (r.anchor != null) {
          stats.anchors++;
          if (typeof r.anchor !== 'string' || !r.anchor) E(`${id}/${r.lesson}: empty anchor`);
          else {
            const built = opts.builtHeadings?.(r.lesson);
            const ok = built ? built.has(r.anchor) : l.h2.has(r.anchor);
            if (!ok) W(`${id}/${r.lesson}: anchor #${r.anchor} is not a section heading of ${built ? 'the built page' : 'the lesson'} any more; the link falls back to the top of the lesson`);
            // It matches the page and works in a browser; listed so nobody is surprised by it in a link.
            else if (!/^[a-z0-9-]+$/.test(r.anchor)) notes.push(`${id}/${r.lesson}: anchor #${r.anchor} has non-ASCII characters`);
          }
        }
      } else {
        stats.uses++; (usesBy[r.lesson] ??= []).push(id);
        if (r.adds != null || r.anchor != null) E(`${id}/${r.lesson}: a uses rung carries a note or an anchor`);
      }
    }
    if (!cores) E(`${id}: no core rung (no lesson teaches it)`);
    const fseen = new Set();
    for (const k of c.films) {
      stats.films++;
      const f = site.films.get(k);
      if (fseen.has(k)) E(`${id}: film ${k} listed twice`);
      fseen.add(k);
      if (!f) { E(`${id}: film ${k} is not a film of any live lesson`); continue; }
      const rung = c.rungs.find((r) => r.lesson === f.lesson);
      if (!rung) E(`${id}: film ${k} belongs to ${f.lesson}, which is not a rung of this concept`);
      else if (rung.role !== 'core') W(`${id}: film ${k} is from a uses rung`);
    }
    if (c.near.length > LIMITS.nearMax) E(`${id}: ${c.near.length} sideways hops (limit ${LIMITS.nearMax})`);
    if (!c.near.length) W(`${id}: no sideways hop yet`);
    const nseen = new Set();
    for (const x of c.near) {
      stats.near++;
      if (!concepts[x?.id]) { E(`${id}: sideways hop to "${x?.id}", which is not a concept`); continue; }
      if (x.id === id) E(`${id}: sideways hop to itself`);
      if (nseen.has(x.id)) E(`${id}: sideways hop to ${x.id} listed twice`);
      nseen.add(x.id);
      const p = whyProblem(x.why); if (p) E(`${id} -> ${x.id}: ${p}: "${x.why}"`);
    }
  }
  // the reverse index
  const records = graph.lessons && typeof graph.lessons === 'object' ? graph.lessons : {};
  stats.lessons = Object.keys(records).length;
  const stale = [];
  for (const [slug, ids] of Object.entries(want)) {
    const got = records[slug]?.concepts;
    if (!Array.isArray(got) || JSON.stringify([...got].sort()) !== JSON.stringify([...ids].sort())) E(`lessons["${slug}"] does not match the rungs that name it`);
    else { const roles = got.map((id) => concepts[id].rungs.find((r) => r.lesson === slug)?.role); if (roles.lastIndexOf('core') > roles.indexOf('uses') && roles.includes('uses')) E(`lessons["${slug}"]: ideas the lesson teaches must come before ideas it uses (main idea first)`); }
  }
  for (const [slug, rec] of Object.entries(records)) {
    const l = site.lessons.get(slug);
    if (!l) { E(`lessons["${slug}"]: not a live lesson (drafted, renamed or removed): delete its record`); continue; }
    if (!Array.isArray(rec.concepts)) { E(`lessons["${slug}"]: concepts is not a list`); continue; }
    if (!want[slug] && rec.concepts.length) E(`lessons["${slug}"] lists concepts but no rung names it`);
    if (!/^[0-9a-f]{16}$/.test(rec.hash ?? '')) E(`lessons["${slug}"]: no hash`);
    else if (rec.hash !== l.contentHash) stale.push(slug);
    if (!rec.concepts.length) notes.push(`${slug}: read, with no idea filed`);
  }
  for (const [slug, ids] of Object.entries(coreBy)) if (ids.length > LIMITS.corePerLesson) W(`${slug} is core for ${ids.length} concepts (${ids.join(', ')}); a lesson that is "about" that many has not been read closely`);
  for (const [slug, ids] of Object.entries(usesBy)) if (ids.length > LIMITS.usesPerLesson) W(`${slug} uses ${ids.length} concepts (limit ${LIMITS.usesPerLesson})`);
  const uncovered = [...site.lessons.keys()].filter((s) => !records[s]).sort();
  if (stale.length) W(`${stale.length} record(s) were written before their lesson's teaching text last changed; refresh each with node scripts/topic-graph/assign.mjs --emit <slug>:\n      ${wrapList(stale)}`);
  if (uncovered.length) W(`${uncovered.length} live lesson(s) have no record yet (they still work everywhere, by course and level):\n      ${wrapList(uncovered)}`);
  return { errors, warnings, notes, stats, stale, uncovered, sameName };
}

export const wrapList = (list, width = 110) => {
  const lines = [''];
  for (const s of list) { if (lines[lines.length - 1].length + s.length + 2 > width) lines.push(''); lines[lines.length - 1] += (lines[lines.length - 1] ? ', ' : '') + s; }
  return lines.join('\n      ');
};

// ------------------------------------------------------------------ what the graph looks like (the report)

/** Every hand-written ladder and stepUp edge on the site, as [from, to, kind] with both ends live. */
export function authoredEdges(site) {
  const out = [];
  for (const l of site.lessons.values()) {
    for (const k of ['grade7', 'biology', 'college']) for (const t of l.ladder?.[k] ?? []) out.push([l.slug, t, `ladder.${k}`]);
    for (const t of l.activity?.stepUp ?? []) out.push([l.slug, t, 'stepUp']);
  }
  return out;
}

/** The registry a reader is given: every concept's id, name, blurb, area and where its ladder stands. */
export function registryOf(graph, site) {
  return Object.entries(graph.concepts).map(([id, c]) => {
    const core = c.rungs.filter((r) => r.role === 'core' && site.lessons.has(r.lesson));
    const ranks = [...new Set(core.map((r) => site.lessons.get(r.lesson).rank))].sort((a, b) => a - b);
    return { id, name: c.name, blurb: c.blurb, area: c.area, aliases: c.aliases, levels: ranks.map((r) => site.STAGES[r].key), lessons: core.map((r) => r.lesson) };
  });
}

/** Numbers and lists for the report: spans, gaps, coverage, and the recall test against the authored ladder. */
export function describeGraph(graph, site) {
  const api = makeTopicGraph(graph, coreSite(site));
  const spans = api.concepts.map((c) => {
    const s = api.span(c.id);
    const core = c.rungs.filter((r) => r.role === 'core');
    return { id: c.id, name: c.name, area: c.area, levels: s.levels, gaps: s.gaps, core: core.length, uses: c.rungs.length - core.length, lessons: core.map((r) => r.lesson) };
  });
  const bySpan = {};
  for (const s of spans) (bySpan[s.levels.length] ??= []).push(s.id);
  const coreOf = (slug) => new Set(Object.entries(graph.concepts).filter(([, c]) => c.rungs.some((r) => r.lesson === slug && r.role === 'core')).map(([id]) => id));
  const anyOf = (slug) => new Set(graph.lessons[slug]?.concepts ?? []);
  const edges = authoredEdges(site);
  const recall = { edges: edges.length, bothCovered: 0, shareCore: 0, shareAny: 0, shareNone: [] };
  for (const [a, b, kind] of edges) {
    if (!graph.lessons[a] || !graph.lessons[b]) continue;
    recall.bothCovered++;
    const ca = coreOf(a), cb = coreOf(b);
    if ([...ca].some((x) => cb.has(x))) { recall.shareCore++; recall.shareAny++; continue; }
    const aa = anyOf(a), ab = anyOf(b);
    if ([...aa].some((x) => ab.has(x))) { recall.shareAny++; continue; }
    recall.shareNone.push({ from: a, to: b, kind });
  }
  const covered = Object.keys(graph.lessons).filter((s) => site.lessons.has(s));
  const byCourse = site.COURSES.map((c) => {
    const mine = [...site.lessons.values()].filter((l) => l.course === c.slug);
    return { course: c.slug, lessons: mine.length, covered: mine.filter((l) => graph.lessons[l.slug]).length };
  }).filter((x) => x.lessons);
  return {
    concepts: spans.length,
    coreRungs: spans.reduce((n, s) => n + s.core, 0),
    usesRungs: spans.reduce((n, s) => n + s.uses, 0),
    films: api.concepts.reduce((n, c) => n + c.films.length, 0),
    near: api.concepts.reduce((n, c) => n + c.near.length, 0),
    lessonsCovered: covered.length,
    lessonsLive: site.lessons.size,
    notCovered: [...site.lessons.keys()].filter((s) => !graph.lessons[s]).sort(),
    byCourse,
    singleLesson: spans.filter((s) => s.core === 1).map((s) => s.id),
    bySpan,
    withGaps: spans.filter((s) => s.gaps.length).map((s) => ({ id: s.id, gaps: s.gaps })),
    byArea: graph.areas.map((a) => ({ area: a.id, concepts: spans.filter((s) => s.area === a.id).length })),
    recall,
    spans,
  };
}

/** The report as text. */
export function reportText(d, site) {
  const L = [];
  const stage = (k) => site.STAGES.find((s) => s.key === k)?.title ?? k;
  L.push(`Concepts ${d.concepts}; core rungs ${d.coreRungs}; uses rungs ${d.usesRungs}; film links ${d.films}; sideways hops ${d.near}.`);
  L.push(`Lessons covered ${d.lessonsCovered} of ${d.lessonsLive}; not covered ${d.notCovered.length}.`);
  L.push('By course: ' + d.byCourse.map((c) => `${c.course} ${c.covered}/${c.lessons}`).join('; ') + '.');
  L.push('By area: ' + d.byArea.map((a) => `${a.area} ${a.concepts}`).join('; ') + '.');
  L.push('Ladders by span (levels with a core lesson):');
  for (const n of Object.keys(d.bySpan).sort((a, b) => b - a)) L.push(`  ${n} level(s): ${d.bySpan[n].length}${d.bySpan[n].length <= 40 ? `  ${d.bySpan[n].join(', ')}` : ''}`);
  L.push(`Concepts taught by a single lesson: ${d.singleLesson.length}${d.singleLesson.length ? `\n      ${wrapList(d.singleLesson)}` : ''}`);
  L.push(`Ladders with a missing level in the middle: ${d.withGaps.length}`);
  for (const g of d.withGaps) L.push(`  ${g.id}: no lesson at ${g.gaps.map(stage).join(', ')}`);
  const r = d.recall;
  L.push(`Recall against the hand-written ladder (${r.edges} ladder and stepUp links; ${r.bothCovered} with both lessons covered):`);
  L.push(`  share a core concept ${r.shareCore}; share any concept ${r.shareAny}; share none ${r.shareNone.length}.`);
  L.push('  "Share none" is a list to read, not a score: many hand links are loose "nearest lesson" links.');
  for (const m of r.shareNone) L.push(`    ${m.from} -> ${m.to}  (${m.kind})`);
  if (d.notCovered.length) L.push(`Lessons not covered:\n      ${wrapList(d.notCovered)}`);
  return L.join('\n');
}
