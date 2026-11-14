/* Lesson links: shared, model-free helpers (2026-11-14).

   src/data/lesson-links.json holds, for each live lesson, what was worked out ONCE and offline
   by a model (scripts/lesson-links/generate.mjs) so the static site can use it for free:
     before     up to 3 lessons to review first (true prerequisites), each with a one-line reason
     after      up to 3 lessons to study next
     elsewhere  up to 4 resources elsewhere on the site: a film in another course (film:<lesson>),
                a lesson's simulation (sim:<lesson>) or a method film (method:<slug>)
     search     8 to 15 phrases a student might type that the lesson answers but its title and
                headings do not contain; they feed the title index as a low-weight field

   This file loads the site's lessons, courses and methods from source (no build needed), and
   holds the mechanical rules every record must pass. The generator uses them to clean what the
   model wrote; scripts/check-lesson-links.mjs uses them in CI so a broken record fails the
   build, not the page. Nothing here calls a model. */

import { readdirSync, readFileSync, existsSync } from 'node:fs';
import { join } from 'node:path';
import { createHash } from 'node:crypto';
import yaml from 'js-yaml';

export const ROOT = process.cwd();
export const DATA_FILE = join(ROOT, 'src', 'data', 'lesson-links.json');
const LESSON_DIR = join(ROOT, 'src', 'content', 'lessons');

export const MAX = { before: 3, after: 3, elsewhere: 4, searchMin: 8, searchMax: 15 };

/** Split an .mdx file into its frontmatter and body. */
export function splitMdx(src) {
  const m = /^---\n([\s\S]*?)\n---\n?([\s\S]*)$/.exec(src);
  return m ? { fm: m[1], body: m[2] } : { fm: '', body: src };
}

/** The hash a record is tied to: the lesson file as committed. */
export const hashOf = (src) => createHash('sha256').update(src).digest('hex').slice(0, 16);

/** Markdown/MDX source to the plain text a reader sees, roughly. */
export function plain(md) {
  return md
    .replace(/^import .*$/gm, ' ')
    .replace(/\{\/\*[\s\S]*?\*\/\}/g, ' ')
    .replace(/<details[\s\S]*?<\/details>/g, ' ')            // folded worked answers
    .replace(/\b(caption|alt)="([^"]*)"/g, ' $2. ')           // keep figure captions as text
    .replace(/<\/?[A-Za-z][^>]*>/g, ' ')
    .replace(/!\[([^\]]*)\]\([^)]*\)/g, '$1')
    .replace(/\[([^\]]+)\]\([^)]*\)/g, '$1')
    .replace(/^\s*>\s?/gm, '')
    .replace(/\*\*|`/g, '')
    .replace(/[ \t]+/g, ' ')
    .replace(/\n{3,}/g, '\n\n')
    .trim();
}

/** ## and ### headings of a body, outside code fences. */
export function headingsOf(body) {
  const out = [];
  let fence = false;
  for (const line of body.split('\n')) {
    if (/^\s*```/.test(line)) fence = !fence;
    const m = !fence && /^(#{2,3})\s+(.+?)\s*$/.exec(line);
    if (m) out.push(m[2].replace(/\*\*|`|\{#[^}]*\}/g, '').trim());
  }
  return out;
}

const firstSentence = (s) => String(s ?? '').replace(/\s+/g, ' ').trim().split(/(?<=[.?!])\s+/)[0];

/** Everything the generator and the checker need, from source files. */
export async function loadSite() {
  const { COURSES } = await import(join(ROOT, 'src/data/courses.ts'));
  const { STAGES, stageOf } = await import(join(ROOT, 'src/data/stages.ts'));
  const { listedMethods, allMethodsFor } = await import(join(ROOT, 'src/data/methods.ts'));
  const stageRank = new Map(STAGES.map((s, i) => [s.key, i]));
  const courseInfo = new Map(COURSES.map((c, i) => [c.slug, { ...c, idx: i, stage: stageOf(c), rank: stageRank.get(stageOf(c)), stageTitle: STAGES.find((s) => s.key === stageOf(c)).title }]));

  const lessons = new Map();
  for (const dir of readdirSync(LESSON_DIR).sort()) {
    const file = join(LESSON_DIR, dir, 'lesson.mdx');
    if (!existsSync(file)) continue;
    const src = readFileSync(file, 'utf8');
    const { fm, body } = splitMdx(src);
    const d = yaml.load(fm) ?? {};
    if (d.draft) continue;
    const course = courseInfo.get(d.course ?? 'biochemistry');
    if (!course) continue;
    lessons.set(d.slug, {
      slug: d.slug, title: d.title, course: course.slug, courseTitle: course.title, rank: course.rank,
      stage: course.stage, stageTitle: course.stageTitle, tier: course.tier, courseIdx: course.idx,
      order: d.order ?? 999, hook: d.hook ?? firstSentence(d.summary), idea: firstSentence(d.summary),
      summary: String(d.summary ?? '').replace(/\s+/g, ' ').trim(), objectives: d.objectives ?? [],
      headings: headingsOf(body), body, hash: hashOf(src),
      film: d.explainer ? { title: d.explainer.title, takeaways: d.explainer.takeaways ?? [] } : null,
      films: (d.films ?? []).map((f) => ({ title: f.title, takeaways: f.takeaways ?? [] })),
      sims: (d.simulations ?? []).filter((s) => s.type === 'local').map((s) => s.title.split('(')[0].trim()),
      ladder: d.ladder ?? null, activity: d.activity ?? null,
      methodsShown: allMethodsFor(d.slug).map((m) => m.slug),
    });
  }
  // Position within the course: the same order as the course page and the lesson page's nav.
  for (const c of COURSES) {
    const mine = [...lessons.values()].filter((l) => l.course === c.slug).sort((a, b) => a.order - b.order || a.slug.localeCompare(b.slug));
    mine.forEach((l, i) => { l.n = i + 1; l.of = mine.length; l.unit = c.units.find((u) => u.slugs.includes(l.slug))?.name ?? ''; });
  }
  const methods = new Map(listedMethods().map((m) => [m.slug, { slug: m.slug, name: m.name, summary: m.summary }]));
  return { COURSES, STAGES, courseInfo, lessons, methods };
}

/** What a resource id points at, or null when it does not exist. */
export function resolveResource(id, site) {
  const [kind, key] = String(id).split(':');
  if (kind === 'method') { const m = site.methods.get(key); return m ? { kind, key, lesson: null, title: m.name } : null; }
  const l = site.lessons.get(key);
  if (!l) return null;
  if (kind === 'film') return l.film ? { kind, key, lesson: l, title: l.film.title } : null;
  if (kind === 'sim') return l.sims.length ? { kind, key, lesson: l, title: l.sims[0] } : null;
  return null;
}

// ------------------------------------------------------------------ the rules

/** Words that say nothing about the connection. */
const VAGUE = /\b(is|are|also) (related|relevant|connected)\b|\brelated (topic|lesson|material)\b|\bsimilar (topic|ideas?)\b|\bcovers? (a )?related\b|\bfor more (on|about) this\b/i;
/** A filler reason ("Not applicable") or a link that rests on an analogy or a contrast, not a real dependency. */
const FILLER = /\bnot (applicable|used|valid|relevant|needed|a fit|a direct follow)|\bplaceholder\b|^\s*(n\/?a|none|skip)\b|\bskip\b|does ?n[o']t (fit|teach|belong|match|relate|build on)|no (direct|real|clear) (link|connection)|wrong match|should not be listed/i;
const ANALOGY = /\b(parallels?|mirrors?|analog(y|ous)|same [\w-]+(?: [\w-]+)? (logic|idea|reasoning)|same (logic|idea)|useful contrast|by contrast|in contrast|contrasts? with|similar to how)\b/i;
/** A phrase must not ask for medical advice. */
const MEDICAL = /\b(should i (take|stop|eat|see)|is it safe|safe to|dos(e|age)|how much .* (take|should)|cure for|treat(ment)? for my|my (doctor|symptoms?|child'?s? (rash|fever))|do i have|am i (sick|pregnant)|diagnos|side effects? of|prescri|overdose|home remed|medicine for|pills? for)\b/i;
/** Commercial products and test-prep companies (Chris: never name or oppose prep companies). */
const BRANDS = /\b(kaplan|princeton review|uworld|magoosh|blueprint|examkrackers|next step|altius|jack westin|khan academy|quizlet|chegg|anki|coursera|tylenol|advil|motrin|aleve|aspirin|ibuprofen|acetaminophen|gatorade|red bull|monster energy|coca[- ]?cola|pepsi|ozempic|wegovy|mounjaro|prozac|zoloft|viagra|adderall|ritalin|benadryl|claritin|zyrtec|lipitor|epipen|neosporin|clorox|lysol|miracle[- ]?gro|roundup|23andme|ancestry\.com|apple watch|fitbit|tiktok|youtube|google|chatgpt)\b|[®™]/i;

export const sentenceCount = (s) => (String(s).trim().match(/[.?!](\s|$)/g) ?? []).length;
const words = (s) => String(s).trim().split(/\s+/).filter(Boolean).length;

/** Problems with one reason, '' if none. Younger readers get shorter reasons. */
export function reasonProblem(reason, lesson) {
  const r = String(reason ?? '').trim();
  if (!r) return 'empty reason';
  if (sentenceCount(r) > 1) return 'more than one sentence';
  const max = lesson.rank <= 1 ? 22 : 30;
  if (words(r) > max) return `longer than ${max} words`;
  if (VAGUE.test(r)) return 'vague ("related")';
  if (FILLER.test(r)) return 'filler reason';
  if (ANALOGY.test(r)) return 'an analogy or contrast, not a real connection';
  return '';
}

export function phraseProblem(p, lesson) {
  const s = String(p ?? '').trim();
  if (!s) return 'empty';
  const w = words(s);
  if (w < 1 || w > 10) return 'length';
  if (/\bspell/i.test(s)) return 'says "spelled" instead of just misspelling';
  if (MEDICAL.test(s)) return 'medical-advice query';
  if (BRANDS.test(s)) return 'names a product or company';
  const n = (x) => x.toLowerCase().replace(/[^a-z0-9 ]+/g, ' ').replace(/\s+/g, ' ').trim();
  const np = n(s);
  if (!np) return 'empty';
  const inTitle = [lesson.title, ...lesson.headings].some((h) => n(h).includes(np));
  if (inTitle) return 'already in the title or a heading';
  return '';
}

/**
 * Clean one record against the rules. Returns { record, dropped } where `dropped` lists every item
 * removed and why. The generator keeps the cleaned record; the checker fails when anything would be
 * dropped from the committed file.
 */
export function cleanRecord(slug, rec, site) {
  const me = site.lessons.get(slug);
  const dropped = [];
  const drop = (what, why) => dropped.push(`${what}: ${why}`);
  const out = { hash: rec.hash, generated: rec.generated, before: [], after: [], elsewhere: [], search: [] };
  const used = new Set([slug]);

  for (const it of rec.before ?? []) {
    const l = site.lessons.get(it.slug);
    const why = !l ? 'no such live lesson' : used.has(it.slug) ? (it.slug === slug ? 'self' : 'duplicate')
      : l.course === me.course && l.n >= me.n ? 'comes later in the same course'
      : l.course !== me.course && l.rank > me.rank ? `higher level (${l.stageTitle}) cannot be review-first`
      : reasonProblem(it.why, me);
    if (why) { drop(`before ${it.slug}`, why); continue; }
    if (out.before.length >= MAX.before) { drop(`before ${it.slug}`, 'over the limit'); continue; }
    used.add(it.slug); out.before.push({ slug: it.slug, why: it.why.trim() });
  }
  for (const it of rec.after ?? []) {
    const l = site.lessons.get(it.slug);
    const why = !l ? 'no such live lesson' : used.has(it.slug) ? (it.slug === slug ? 'self' : 'duplicate or also review-first')
      : l.course === me.course && l.n <= me.n ? 'comes earlier in the same course (a prerequisite, not next)'
      : l.course !== me.course && l.rank < me.rank ? `lower level (${l.stageTitle}) is not "next"`
      : l.rank > me.rank + 1 ? `more than one level up (${l.stageTitle})`
      : reasonProblem(it.why, me);
    if (why) { drop(`after ${it.slug}`, why); continue; }
    if (out.after.length >= MAX.after) { drop(`after ${it.slug}`, 'over the limit'); continue; }
    used.add(it.slug); out.after.push({ slug: it.slug, why: it.why.trim() });
  }
  const seenRes = new Set();
  for (const it of rec.elsewhere ?? []) {
    const r = resolveResource(it.id, site);
    const why = !r ? 'no such resource' : seenRes.has(it.id) ? 'duplicate'
      : r.lesson && r.lesson.slug === slug ? 'self'
      : r.lesson && used.has(r.lesson.slug) ? 'its lesson is already listed above'
      : r.lesson && r.lesson.course === me.course ? 'same course (reachable through the course)'
      : r.lesson && r.lesson.rank > me.rank + 1 ? `more than one level up (${r.lesson.stageTitle})`
      : r.kind === 'method' && me.methodsShown.includes(r.key) ? 'already shown under "How we measure it"'
      : reasonProblem(it.why, me);
    if (why) { drop(`elsewhere ${it.id}`, why); continue; }
    if (out.elsewhere.length >= MAX.elsewhere) { drop(`elsewhere ${it.id}`, 'over the limit'); continue; }
    seenRes.add(it.id); out.elsewhere.push({ id: it.id, why: it.why.trim() });
  }
  const seenP = new Set();
  for (const p of rec.search ?? []) {
    const k = String(p).toLowerCase().trim();
    const why = seenP.has(k) ? 'duplicate' : phraseProblem(p, me);
    if (why) { drop(`search "${p}"`, why); continue; }
    if (out.search.length >= MAX.searchMax) { drop(`search "${p}"`, 'over the limit'); continue; }
    seenP.add(k); out.search.push(String(p).trim());
  }
  return { record: out, dropped };
}

// ------------------------------------------------------------------ the prompt material

const clip = (s, max) => {
  const one = String(s ?? '').replace(/\s+/g, ' ').replace(/\|/g, '/').trim();
  if (one.length <= max) return one;
  const cut = one.slice(0, max);
  return cut.slice(0, Math.max(cut.lastIndexOf(' '), max - 15)).replace(/[ ,;:.\-–—]+$/, '') + '…';
};

/** The catalog block: every live lesson and method film, in a fixed order (byte-stable, so it caches). */
export function catalogText(site) {
  const lines = [];
  lines.push('LEVELS (lowest to highest): ' + site.STAGES.map((s, i) => `${i} ${s.title}`).join('; ') + '.');
  lines.push('');
  lines.push('LESSONS. One line each: slug | position in its course | title | hook | F: its film\'s title (and take-homes) | S: its simulation.');
  for (const c of site.COURSES) {
    const mine = [...site.lessons.values()].filter((l) => l.course === c.slug).sort((a, b) => a.n - b.n);
    if (!mine.length) continue;
    const ci = site.courseInfo.get(c.slug);
    lines.push('');
    lines.push(`## Course "${c.title}" (${c.slug}), level ${ci.rank} ${ci.stageTitle}, ${mine.length} lessons`);
    let unit = null;
    for (const l of mine) {
      if (l.unit !== unit) { unit = l.unit; lines.push(`# unit: ${unit || '(other)'}`); }
      const film = l.film ? `F: "${clip(l.film.title, 60)}"${l.film.takeaways.length ? ` (${clip(l.film.takeaways.slice(0, 2).join(' '), 150)})` : ''}` : '';
      lines.push([l.slug, l.n, clip(l.title, 80), clip(l.hook, 110), film, l.sims.length ? `S: ${clip(l.sims[0], 50)}` : ''].filter((x) => x !== '').join(' | '));
    }
  }
  lines.push('');
  lines.push('METHOD FILMS (id | name | what it is for):');
  for (const m of site.methods.values()) lines.push(`method:${m.slug} | ${m.name} | ${clip(m.summary, 100)}`);
  return lines.join('\n');
}

/** What the model reads about one lesson. `full` sends the lesson text; otherwise a Skim-level digest. */
export function lessonDigest(l, site, { full = true } = {}) {
  const ladder = l.ladder ? [
    l.ladder.grade7?.length ? `grade 7 lessons one step down (already linked on the page): ${l.ladder.grade7.join(', ')}` : '',
    l.ladder.biology?.length ? `high school lessons one step up (already linked): ${l.ladder.biology.join(', ')}` : '',
    l.ladder.college?.length ? `college lessons that take it further (already linked): ${l.ladder.college.join(', ')}` : '',
  ].filter(Boolean) : [];
  const step = l.activity?.stepUp?.length ? [`grade 7 lessons one step up (already linked): ${l.activity.stepUp.join(', ')}`] : [];
  const films = [l.film, ...l.films].filter(Boolean);
  const parts = [
    `LESSON slug: ${l.slug}`,
    `Course: ${l.courseTitle} (${l.course}), level ${l.rank} ${l.stageTitle}; lesson ${l.n} of ${l.of}${l.unit ? `, unit "${l.unit}"` : ''}.`,
    `Title: ${l.title}`,
    `Hook: ${l.hook}`,
    `Summary: ${l.summary}`,
    l.objectives.length ? `Objectives:\n${l.objectives.map((o) => `- ${o}`).join('\n')}` : '',
    `Section headings: ${l.headings.join(' / ')}`,
    films.length ? `Films: ${films.map((f) => `"${f.title}"${f.takeaways.length ? ` (take-homes: ${f.takeaways.join(' ')})` : ''}`).join('; ')}` : '',
    l.sims.length ? `Its own simulations: ${l.sims.join('; ')}` : '',
    l.methodsShown.length ? `Method films already shown on this page (do not suggest): ${l.methodsShown.map((m) => `method:${m}`).join(', ')}` : '',
    ...ladder, ...step,
    full ? `\nLESSON TEXT:\n${plain(l.body)}` : '',
  ];
  return parts.filter(Boolean).join('\n');
}
