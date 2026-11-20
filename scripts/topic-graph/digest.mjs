#!/usr/bin/env node
/**
 * Hop graph, step 0: one compact digest per lesson, for whoever (a model or a person) decides which
 * ideas the lesson teaches. A digest is what a careful reader would note on one page: where the lesson
 * sits, its hook, summary and objectives, every section heading WITH the id the built page gives it,
 * how each section opens, the sentences that carry its numbers, the explain-at-my-level texts, each
 * film's key, title and take-homes, the hand-written ladder links and the lesson-links neighbours.
 * It holds nothing from the graph itself, so a second reader can judge the graph blind from it.
 *
 *   node scripts/topic-graph/digest.mjs                       every live lesson
 *   node scripts/topic-graph/digest.mjs --only a,b            named lessons
 *   options: --out <dir> (default node_modules/.cache/topic-graph/digests), --md (also write <slug>.md,
 *            the text a prompt shows), --print <slug> (print one digest as text and write nothing)
 *
 * Reads lesson files only; calls no model; needs no build.
 */
import { writeFileSync, mkdirSync, readFileSync, existsSync } from 'node:fs';
import { join } from 'node:path';
import { fileURLToPath } from 'node:url';
import { plain, DATA_FILE as LINKS_FILE } from '../lesson-links/lib.mjs';
import { loadGraphSite, sectionsOf, leadSentences, filmOpening, CACHE_DIR, ROOT } from './lib.mjs';

const oneLine = (s) => String(s ?? '').replace(/\s+/g, ' ').trim();

/** Up to `n` sentences of a section that carry a number, a unit or a named case: the raw material
 *  for a note that says what THIS lesson adds. The opening sentences are skipped (already shown). */
function factSentences(text, lead, n = 2) {
  const out = [];
  for (const s of oneLine(text).split(/(?<=[.?!])\s+(?=[A-Z0-9"“(])/)) {
    if (out.length >= n) break;
    if (s.length < 30 || s.length > 320 || lead.includes(s)) continue;
    if (/\d[\d,.]*\s?(%|percent|°|mV|mM|nm|µm|μm|mm|cm|m\b|km|g\b|kg|mg|L\b|mL|ms|s\b|seconds?|minutes?|hours?|days?|years?|times|fold|cells?|genes?|species|people|ATP)|\b\d{2,}[\d,]*\b|\b(in|by) (1[5-9]|20)\d\d\b/.test(s)) out.push(s);
  }
  return out;
}

/** The digest of one lesson. `links` is src/data/lesson-links.json (or null). */
export function buildDigest(l, site, links) {
  const d = l.fm ?? {};
  const title = (slug) => site.lessons.get(slug)?.title;
  const named = (slugs) => (slugs ?? []).filter((s) => site.lessons.has(s)).map((s) => ({ slug: s, title: title(s), level: site.lessons.get(s).stage }));
  const sections = sectionsOf(l.body).map((s) => {
    const lead = leadSentences(s.text, l.rank === 0 && /^(the-big-idea|why-it-works)$/.test(s.id) ? 4 : 2, l.rank === 0 ? 640 : 420);
    return { id: s.id, heading: s.heading, lead, facts: factSentences(s.text, lead), words: s.words, ...(s.sub.length ? { sub: s.sub.map((x) => x.text) } : {}) };
  });
  const firstH2 = l.body.search(/^##\s/m);
  const opening = leadSentences(plain(firstH2 > 0 ? l.body.slice(0, firstH2) : ''), 3, 600);
  const rec = links?.lessons?.[l.slug];
  const ladder = {
    ...(l.ladder?.grade7?.length ? { grade7: named(l.ladder.grade7) } : {}),
    ...(l.ladder?.biology?.length ? { highSchool: named(l.ladder.biology) } : {}),
    ...(l.ladder?.college?.length ? { college: named(l.ladder.college) } : {}),
    ...(l.activity?.stepUp?.length ? { stepUp: named(l.activity.stepUp) } : {}),
    ...(l.ladder?.essentialQuestion ? { essentialQuestion: oneLine(l.ladder.essentialQuestion) } : {}),
  };
  const thin = [];
  if (!l.objectives.length) thin.push('no objectives');
  if (sections.filter((s) => s.words > 40 && !s.lead).length) thin.push('some sections open with a figure or a tool, not prose');
  if (sections.length >= 9) thin.push(`${sections.length} sections`);
  if (l.rank === 0) thin.push('an activity page: every activity has the same eight headings, so only the-big-idea is a useful anchor');
  if (l.filmList.length >= 3) thin.push(`${l.filmList.length} films: choose per concept by title and take-homes`);
  return {
    slug: l.slug, hash: l.contentHash, title: l.title,
    course: l.course, courseTitle: l.courseTitle, stage: l.stage, stageTitle: l.stageTitle, rank: l.rank,
    n: l.n, of: l.of, unit: l.unit || null,
    reader: l.rank === 0 ? 'the grown-up who runs the activity with a child aged 5 to 10' : `a ${l.stageTitle.toLowerCase()} student`,
    hook: oneLine(d.hook ?? l.hook), summary: l.summary, objectives: l.objectives.map(oneLine),
    ...(d.activity?.bigIdea ? { bigIdea: oneLine(d.activity.bigIdea) } : {}),
    ...(opening ? { opening } : {}),
    sections,
    levels: (d.explainLevels ?? []).map((e) => ({ level: e.level, label: e.label, text: oneLine(e.text) })),
    films: l.filmList.map((f) => ({
      key: f.key, title: f.title, seconds: Math.round(f.durationSec ?? 0),
      ...(l.rank === 0 ? { kind: 'activity film (shows the grown-up how to run it)' } : {}),
      ...(f.takeaways.length ? { takeaways: f.takeaways.map(oneLine) } : filmOpening(f) ? { opens: filmOpening(f) } : {}),
    })),
    ...(Object.keys(ladder).length ? { ladder } : {}),
    ...(rec ? { links: { before: named(rec.before.map((x) => x.slug)).map(({ slug, title: t }) => ({ slug, title: t })), after: named(rec.after.map((x) => x.slug)).map(({ slug, title: t }) => ({ slug, title: t })) } } : {}),
    ...(d.corpusTags?.length ? { tags: d.corpusTags } : {}),
    file: `src/content/lessons/${l.dir}/lesson.mdx`,
    bodyWords: sections.reduce((n, s) => n + s.words, 0),
    ...(thin.length ? { openTheLessonIf: thin } : {}),
  };
}

/** A digest as the text a reader is shown. */
export function digestText(d) {
  const L = [];
  L.push(`LESSON ${d.slug}   (content hash ${d.hash})`);
  L.push(`Title: ${d.title}`);
  L.push(`Where: ${d.courseTitle} (${d.course}), level ${d.rank} ${d.stage} "${d.stageTitle}"; lesson ${d.n} of ${d.of}${d.unit ? `, unit "${d.unit}"` : ''}.`);
  L.push(`Its reader: ${d.reader}.`);
  L.push(`Hook: ${d.hook}`);
  L.push(`Summary: ${d.summary}`);
  if (d.bigIdea) L.push(`The big idea (as the page states it): ${d.bigIdea}`);
  if (d.objectives.length) L.push('Objectives:\n' + d.objectives.map((o) => `  - ${o}`).join('\n'));
  if (d.opening) L.push(`How the lesson opens: ${d.opening}`);
  L.push('Sections (## headings; the id in [brackets] is the anchor; then how the section opens, then sentences that carry its numbers):');
  for (const s of d.sections) {
    L.push(`  [${s.id}] ${s.heading}  (${s.words} words)`);
    if (s.sub?.length) L.push(`      inside it: ${s.sub.join(' / ')}`);
    if (s.lead) L.push(`      opens: ${s.lead}`);
    for (const f of s.facts ?? []) L.push(`      fact: ${f}`);
  }
  if (d.levels.length) {
    L.push('The same lesson explained at other levels (text on the page):');
    for (const e of d.levels) L.push(`  ${e.label} (${e.level}): ${e.text}`);
  }
  if (d.films.length) {
    L.push('Films (key | title | what it shows):');
    for (const f of d.films) L.push(`  ${f.key} | "${f.title}"${f.kind ? ` | ${f.kind}` : ''}${f.takeaways ? ` | take-homes: ${f.takeaways.join(' ')}` : f.opens ? ` | no take-homes listed; it opens: ${f.opens}` : ''}`);
  } else L.push('Films: none.');
  if (d.ladder) {
    const row = (label, list) => (list?.length ? `  ${label}: ${list.map((x) => `${x.slug} ("${x.title}")`).join('; ')}` : '');
    L.push('Hand-written ladder links on the page (often "nearest lesson", not always "same idea"):');
    for (const r of [row('one step down, grade 7', d.ladder.grade7), row('one step up, high school', d.ladder.highSchool), row('college lessons that take it further', d.ladder.college), row('one step up from the activity, grade 7', d.ladder.stepUp)].filter(Boolean)) L.push(r);
    if (d.ladder.essentialQuestion) L.push(`  essential question: ${d.ladder.essentialQuestion}`);
  }
  if (d.links && (d.links.before.length || d.links.after.length)) {
    L.push('Lesson links on the page (prerequisites and next steps, not "same idea"):');
    if (d.links.before.length) L.push(`  before: ${d.links.before.map((x) => `${x.slug} ("${x.title}")`).join('; ')}`);
    if (d.links.after.length) L.push(`  after: ${d.links.after.map((x) => `${x.slug} ("${x.title}")`).join('; ')}`);
  }
  if (d.tags?.length) L.push(`Author's free-text tags (uncontrolled, a hint only): ${d.tags.join(', ')}`);
  L.push(`Full text: ${d.file}  (about ${d.bodyWords} words)`);
  if (d.openTheLessonIf?.length) L.push(`Open the full text before deciding, because: ${d.openTheLessonIf.join('; ')}.`);
  return L.join('\n');
}

/** Digests for a site, by slug. */
export function buildDigests(site, slugs) {
  const links = existsSync(LINKS_FILE) ? JSON.parse(readFileSync(LINKS_FILE, 'utf8')) : null;
  const out = new Map();
  for (const slug of slugs ?? [...site.lessons.keys()]) out.set(slug, buildDigest(site.lessons.get(slug), site, links));
  return out;
}

// ------------------------------------------------------------------ run

if (process.argv[1] && fileURLToPath(import.meta.url) === process.argv[1]) {
  const argv = process.argv.slice(2);
  const opt = (f, d) => { const i = argv.indexOf(f); return i >= 0 ? argv[i + 1] : d; };
  const site = await loadGraphSite();
  if (opt('--print')) {
    const l = site.lessons.get(opt('--print'));
    if (!l) { console.error(`Not a live lesson: ${opt('--print')}`); process.exit(2); }
    console.log(digestText(buildDigests(site, [l.slug]).get(l.slug)));
    process.exit(0);
  }
  const only = opt('--only')?.split(',');
  const unknown = (only ?? []).filter((s) => !site.lessons.has(s));
  if (unknown.length) { console.error(`Not live lessons: ${unknown.join(', ')}`); process.exit(2); }
  const out = opt('--out') ? (opt('--out').startsWith('/') ? opt('--out') : join(ROOT, opt('--out'))) : join(CACHE_DIR, 'digests');
  mkdirSync(out, { recursive: true });
  const digests = buildDigests(site, only);
  let chars = 0;
  for (const [slug, d] of digests) {
    writeFileSync(join(out, `${slug}.json`), JSON.stringify(d, null, 1) + '\n');
    const text = digestText(d);
    chars += text.length;
    if (argv.includes('--md')) writeFileSync(join(out, `${slug}.md`), text + '\n');
  }
  console.log(`digest: ${digests.size} lesson(s) written to ${out}; about ${Math.round(chars / 4 / digests.size)} tokens each as text, ${Math.round(chars / 4 / 1000)}k in all.`);
}
