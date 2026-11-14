/* The film catalog (2026-11-13): every film on the site, derived at build time from the sources
   that already exist, so nobody keeps a list by hand. A film appears here the moment its lesson,
   method or profile ships.

   Sources, in the order a reader meets them:
   - lesson films: each published lesson's `explainer` (its first film) and `films[]` (its second
     film, or, in the lessons cut into a series, each further part). Biology Together films are the
     same frontmatter fields; they are labelled "activity film" because those pages are activities
     a grown-up runs, not lessons.
   - scientist profile films: `scientists[].film` in the lesson frontmatter (shown in the profile's
     pop-up on the lesson page, which opens from #lb-sci-<n>).
   - methods library films: src/data/methods.ts listedMethods(). A method film that reuses a lesson
     film (the same file) is not listed twice: the lesson film carries `method` instead.
   Left out on purpose: the homepage films (/explainers/home/) and the teachers' talk films, which
   are about the site rather than the science.

   Media paths are kept exactly as the frontmatter gives them (/explainers/...): the edge worker
   serves them from R2 or the static assets (wrangler.jsonc), so no host is written here.

   Used by /films/ (the library page) and /films.json (the same list for programs). */
import { getCollection } from 'astro:content';
import { COURSES, unitsFor } from '../data/courses';
import { STAGES, stageOf } from '../data/stages';
import { listedMethods, methodHref } from '../data/methods';
import { watchHref } from './films';
import rewrittenList from '../data/recently-rewritten.json';

export type FilmKind = 'first' | 'second' | 'series' | 'activity' | 'profile' | 'method';

/** Reader-facing names, in the order the kind filter lists them. */
export const KIND_LABELS: Record<FilmKind, string> = {
  first: 'First film',
  second: 'Second film',
  series: 'Film series',
  activity: 'Activity film',
  profile: 'Scientist profile',
  method: 'Method film',
};
/** The same, for a count: "146 second films". */
export const KIND_PLURALS: Record<FilmKind, string> = {
  first: 'first films',
  second: 'second films',
  series: 'films in a series',
  activity: 'activity films',
  profile: 'scientist profiles',
  method: 'method films',
};
export const KIND_ORDER = Object.keys(KIND_LABELS) as FilmKind[];

/** The badge on a card: the kind, or "Part 2 of 4" in a series. */
export const kindBadge = (f: Pick<CatalogFilm, 'kind' | 'part'>) => (f.part ? `Part ${f.part.n} of ${f.part.of}` : KIND_LABELS[f.kind]);

/** A film's key for "watched" marks: its file under /explainers/ without ".mp4" (src/lib/film-progress.ts). */
export const filmKey = (src: string) => src.replace(/^\/explainers\//, '').replace(/\.mp4$/, '');

/** One page per level (2026-11-14), so /films/ itself can stay light: /films/high-school/. */
export const filmLevelHref = (stage: string) => `/films/${stage}/`;
/** A course's films back to back: /films/play/genetics/. */
export const filmPlayHref = (course: string) => `/films/play/${course}/`;

export interface CatalogFilm {
  /** Stable id: lesson:<slug>, lesson:<slug>:<film-id>, profile:<slug>:<file>, method:<slug>. */
  id: string;
  title: string;
  kind: FilmKind;
  /** In a lesson cut into a series: which part this is, counting the first film as part 1. */
  part?: { n: number; of: number };
  /** Course slug; null for a method film (the methods library spans every course). */
  course: string | null;
  courseTitle: string;
  /** Stage key from src/data/stages.ts; null for a method film. */
  stage: string | null;
  stageTitle: string;
  /** Lesson the film belongs to (lesson, activity and profile films). */
  lesson?: string;
  lessonTitle?: string;
  /** Where the film sits on its lesson page: #explainer, #sx-film-<id> or the profile pop-up. */
  lessonHref?: string;
  /** The film's own page: /watch/... for lesson films, the method page, or the lesson deep link. */
  href: string;
  /** Running position for the default "course order" sort: stage, course, lesson, film. */
  position: number;
  durationSec: number;
  poster: string;
  src: string;
  captions: string;
  /** One line: the lesson's hook (or its summary's first sentence), the method summary, or the
   *  scientist's contribution. */
  description: string;
  takeaways?: string[];
  /** YYYY-MM-DD, when the lesson is in src/data/recently-rewritten.json. */
  rewritten?: string;
  /** Set when this lesson film is also the methods library's film for a method. */
  method?: { slug: string; name: string };
}

const firstSentence = (s: string) => s.replace(/\s+/g, ' ').trim().split(/(?<=[.?!])\s+/)[0];
const rewrittenOn = new Map((rewrittenList as { slug: string; date: string }[]).map((r) => [r.slug, r.date]));
const stageTitle = (key: string) => STAGES.find((s) => s.key === key)?.title ?? key;

let cache: Promise<CatalogFilm[]> | undefined;

/** Every film, in course order (stage, course, unit, lesson; within a lesson: first film, later
 *  films, profiles). Method films come last. */
export function filmCatalog(): Promise<CatalogFilm[]> {
  cache ??= build();
  return cache;
}

/** How many films the site has: the one number every page that states a total uses (the homepage
 *  hero and tally, /films/, /progress/, /updates/), so they cannot drift apart (2026-11-14). */
export async function filmTotal(): Promise<number> {
  return (await filmCatalog()).length;
}

async function build(): Promise<CatalogFilm[]> {
  const lessons = await getCollection('lessons', ({ data }) => !data.draft);
  const methods = listedMethods();
  const methodBySrc = new Map(methods.map((m) => [m.film!.src, m]));
  const stageRank = new Map(STAGES.map((s, i) => [s.key, i]));
  const out: CatalogFilm[] = [];
  const seen = new Set<string>();

  // Courses in stage order, then in their order in courses.ts (the order /courses/ shows).
  const courses = COURSES.map((c, i) => ({ c, i, stage: stageOf(c) }))
    .sort((a, b) => (stageRank.get(a.stage)! - stageRank.get(b.stage)!) || a.i - b.i);

  let position = 0;
  for (const { c, stage } of courses) {
    const mine = lessons.filter((l) => l.data.course === c.slug);
    const ordered = unitsFor(c, mine).flatMap((u) => u.entries.map((e) => e.l));
    for (const l of ordered) {
      const d = l.data;
      const lessonPage = `/lessons/${d.slug}/`;
      const common = {
        course: c.slug, courseTitle: c.title, stage, stageTitle: stageTitle(stage),
        lesson: d.slug, lessonTitle: d.title,
        description: firstSentence(d.hook ?? d.summary),
        rewritten: rewrittenOn.get(d.slug),
      };
      const isActivity = c.tier === 'families';
      const total = (d.explainer ? 1 : 0) + d.films.length;
      const series = d.films.length > 1;
      const lessonFilms = [
        ...(d.explainer ? [{ f: d.explainer, id: null as string | null, anchor: 'explainer' }] : []),
        ...d.films.map((f) => ({ f, id: f.id as string | null, anchor: `sx-film-${f.id}` })),
      ];
      lessonFilms.forEach(({ f, id, anchor }, i) => {
        if (seen.has(f.src)) return;
        seen.add(f.src);
        const m = methodBySrc.get(f.src);
        const kind: FilmKind = isActivity ? 'activity' : id === null ? 'first' : series ? 'series' : 'second';
        out.push({
          ...common,
          id: id ? `lesson:${d.slug}:${id}` : `lesson:${d.slug}`,
          title: f.title,
          kind,
          ...(series && !isActivity ? { part: { n: i + 1, of: total } } : {}),
          lessonHref: `${lessonPage}#${anchor}`,
          href: watchHref(d.slug, id),
          position: position++,
          durationSec: f.durationSec,
          poster: f.poster,
          src: f.src,
          captions: f.captions,
          ...(f.takeaways?.length ? { takeaways: f.takeaways } : {}),
          ...(m ? { method: { slug: m.slug, name: m.name } } : {}),
        });
      });
      d.scientists.forEach((s, i) => {
        if (!s.film || seen.has(s.film.src)) return;
        seen.add(s.film.src);
        const deep = `${lessonPage}#lb-sci-${i}`;
        out.push({
          ...common,
          id: `profile:${d.slug}:${s.film.src.split('/').pop()!.replace(/\.mp4$/, '')}`,
          title: s.name,
          kind: 'profile',
          lessonHref: deep,
          href: deep,
          position: position++,
          durationSec: s.film.durationSec,
          poster: s.film.poster,
          src: s.film.src,
          captions: s.film.captions,
          description: firstSentence(s.contribution),
        });
      });
    }
  }

  for (const m of methods) {
    const f = m.film!;
    if (seen.has(f.src)) continue; // already listed as its lesson's film
    seen.add(f.src);
    out.push({
      id: `method:${m.slug}`,
      title: f.title,
      kind: 'method',
      course: null,
      courseTitle: 'Methods library',
      stage: null,
      stageTitle: 'Methods library',
      href: methodHref(m.slug),
      position: position++,
      durationSec: f.durationSec,
      poster: f.poster,
      src: f.src,
      captions: f.captions,
      description: m.summary,
      method: { slug: m.slug, name: m.name },
    });
  }
  return out;
}
