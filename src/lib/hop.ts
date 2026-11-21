/* Hopping, at build time: what the hop sentence on a lesson and the pages under /ideas/ show.

   Everything here is joined from files when the site is built: the hop graph (src/lib/topic-graph.ts),
   each lesson's own short versions at other levels (frontmatter explainLevels), the hand-picked
   ladder links on school lessons (frontmatter ladder, activity.stepUp), reading time, films and
   practice-question counts. No model runs and nothing is fetched when someone visits.

   The words are in hop-words.mjs; this file only gathers facts. */
import { getCollection } from 'astro:content';
import { COURSES, courseOf } from '../data/courses';
import { stageOf } from '../data/stages';
import { SETS as MCAT_SETS } from './mcat';
import { lessonMinutes } from './reading-time';
import { concept, concepts, hops, ladder, usedBy, filmsFor, areaName, areas, stageRank, type LadderRung, type JoinedFilm } from './topic-graph';
import { headingIds } from './topic-graph-core.mjs';
import { lessonSentence, authoredLinks, inSentence, maskOf, QUICK_DOWN, QUICK_UP, QUICK_NAME, readTime } from './hop-words.mjs';

export interface Rung {
  slug: string;
  title: string;
  /** The lesson, at the section that teaches the idea when the graph names one. */
  href: string;
  course: string;
  courseTitle: string;
  rank: number;
  /** What this level adds, from the graph. */
  adds?: string;
  minutes?: number;
  /** The idea's first film from this lesson. */
  film?: { href: string; seconds: number; title: string };
  /** MCAT-style practice questions on this lesson. */
  questions: number;
  /** Virginia standards codes, on school lessons and activities. */
  sol: string[];
}
export interface Idea {
  id: string;
  name: string;
  /** The name as it reads inside a sentence. */
  short: string;
  blurb: string;
  area: string;
  areaName: string;
  aliases: string[];
  /** Levels with a lesson, as a bit mask (bit 0 = ages 5 to 10). */
  mask: number;
  rungs: Rung[];
  near: { id: string; name: string; short: string; why: string; mask: number }[];
  uses: Rung[];
  films: JoinedFilm[];
  /** "Play the ladder": present when the idea has films at two or more levels. */
  play?: { href: string; n: number; minutes: number; from: number; to: number };
}

interface Facts { minutes?: number; questions: number; sol: string[]; unit: string; rank: number; sections: Record<string, number>; data: any }

let factsCache: Promise<Map<string, Facts>> | undefined;
/** Per live lesson: reading time, practice questions, standards codes, unit and frontmatter. */
export function lessonFacts(): Promise<Map<string, Facts>> {
  factsCache ??= (async () => {
    const out = new Map<string, Facts>();
    const unitOf = new Map<string, string>();
    for (const c of COURSES) for (const u of c.units) for (const s of u.slugs) unitOf.set(s, u.name);
    const passage = new Map<string, number>();
    for (const st of MCAT_SETS) for (const q of st.questions) passage.set(q.lesson.slug, (passage.get(q.lesson.slug) ?? 0) + 1);
    for (const l of await getCollection('lessons', ({ data }) => !data.draft)) {
      const d = l.data as any;
      const tier = courseOf(d.course).tier;
      const own = tier !== 'highschool' && tier !== 'families' ? (d.mcatQuestions?.length ?? 0) : 0;
      out.set(d.slug, {
        minutes: lessonMinutes(l as any)?.core,
        questions: own + (passage.get(d.slug) ?? 0),
        sol: d.ladder?.sol ?? d.activity?.sol ?? [],
        unit: unitOf.get(d.slug) ?? '',
        rank: stageRank(stageOf(courseOf(d.course))),
        sections: sectionWords(l.body ?? ''),
        data: d,
      });
    }
    return out;
  })();
  return factsCache;
}

async function toRung(r: Pick<LadderRung, 'slug' | 'title' | 'href' | 'course' | 'courseTitle' | 'rank' | 'adds'> & { films?: JoinedFilm[] }): Promise<Rung> {
  const f = (await lessonFacts()).get(r.slug);
  const film = r.films?.[0];
  return {
    slug: r.slug, title: r.title, href: r.href, course: r.course, courseTitle: r.courseTitle, rank: r.rank, adds: r.adds,
    minutes: f?.minutes, questions: f?.questions ?? 0, sol: f?.sol ?? [],
    ...(film ? { film: { href: film.href, seconds: Math.round(film.durationSec), title: film.title } } : {}),
  };
}

/* "Play the ladder": an idea's films in order from the simplest level to the deepest, as a run with
   a stated end. The run page (/films/run/) is the film library's; until it reads ?idea=, the link
   opens the first film's own page and carries the idea, so that page or a later one can offer the
   rest. The list itself is /ideas/film-runs.json. To switch every link to the run page, change
   this one function to `/films/run/?idea=${id}`. */
/** OFF until the film run page (/films/run/) reads ?idea=<id>. While it is off no page offers a run
 *  of films it cannot deliver; /ideas/film-runs.json still lists each idea's films in order. */
export const PLAY_LADDER = false;
export const playHref = (id: string, firstFilmHref: string) => `${firstFilmHref}${firstFilmHref.includes('?') ? '&' : '?'}idea=${id}`;

/** Words in each `##` section of a lesson, by the section's id: how the main idea of a lesson is chosen. */
export function sectionWords(body: string): Record<string, number> {
  const heads = headingIds(body).filter((h) => h.depth === 2);
  const lines = body.split('\n');
  const out: Record<string, number> = {};
  heads.forEach((h, i) => { out[h.id] = lines.slice(h.line + 1, heads[i + 1]?.line ?? lines.length).join(' ').split(/\s+/).length; });
  return out;
}

const ideaCache = new Map<string, Promise<Idea | undefined>>();
const maskCache = new Map<string, Promise<number>>();
const maskFor = (id: string): Promise<number> => {
  if (!maskCache.has(id)) maskCache.set(id, ladder(id).then((rs) => maskOf([...new Set(rs.map((r) => r.rank))])));
  return maskCache.get(id)!;
};

/** One idea with its ladder, simplest first, gaps said in words. undefined when no live lesson teaches it. */
export function idea(id: string): Promise<Idea | undefined> {
  if (!ideaCache.has(id)) ideaCache.set(id, (async () => {
    const c = concept(id);
    if (!c) return undefined;
    const rungs = await Promise.all((await ladder(id)).map(toRung));
    if (!rungs.length) return undefined;
    const short = inSentence(id, c.name);
    const ranks = [...new Set(rungs.map((r) => r.rank))].sort((a, b) => a - b);
    const films = await filmsFor(id);
    const filmRanks = [...new Set(films.map((f) => f.rank))].sort((a, b) => a - b);
    const near = [];
    for (const n of c.near) {
      const t = concept(n.id);
      const m = t ? await maskFor(n.id) : 0;
      if (t && m) near.push({ id: n.id, name: t.name, short: inSentence(n.id, t.name), why: n.why, mask: m });
    }
    return {
      id, name: c.name, short, blurb: c.blurb, area: c.area, areaName: areaName(c.area), aliases: c.aliases,
      mask: maskOf(ranks), rungs, near,
      uses: await Promise.all((await usedBy(id)).map(toRung)),
      films,
      ...(PLAY_LADDER && filmRanks.length > 1 ? { play: { href: playHref(id, films[0].href), n: films.length, minutes: Math.max(1, Math.round(films.reduce((t, f) => t + f.durationSec, 0) / 60)), from: filmRanks[0], to: filmRanks[filmRanks.length - 1] } } : {}),
    };
  })());
  return ideaCache.get(id)!;
}

/** Every idea that has a live lesson, in the graph's order (by area). */
export async function allIdeas(): Promise<Idea[]> {
  return (await Promise.all(concepts.map((c) => idea(c.id)))).filter((x): x is Idea => Boolean(x));
}
export { areas };

// ------------------------------------------------------------------ one lesson

export interface Quick {
  key: string;
  /** "The grade 7 version" */
  label: string;
  time: string;
  paras: string[];
}
type Seg = { t: string; href?: string; quick?: string; k?: string };
export interface LessonHop {
  slug: string;
  title: string;
  rank: number;
  ideas: (Idea & { sideways: { id: string; name: string; why: string; lesson?: { title: string; href: string; rank: number } }[] })[];
  lines: { teaches: Seg[]; simpler?: Seg[]; deeper?: Seg[]; next?: Seg[] };
  /** The short version that opens under the sentence. */
  quickDown?: Quick;
  /** The other short versions, listed inside the panel. */
  quickRest: Quick[];
  /** "See every level", or "See nearby ideas" when every idea here is taught at one level only. */
  more: string;
  /** Hand-picked ladder links the graph does not already show, so none is lost. */
  extra: { label: string; items: { title: string; href: string }[] }[];
  /** Levels (0 ages 5 to 10, 1 grade 7, 2 high school, 3 college, 4 graduate) where a hand-picked lesson exists,
   *  so a ladder does not say "no lesson" there. */
  also: number[];
  /** Titles of the lessons a reader can hop here from, for the arrival line. */
  from: Record<string, string>;
}

const paras = (t: string) => t.split(/\n\n+/).map((p) => p.trim()).filter(Boolean);
function quick(levels: { level: string; text: string }[] | undefined, key: string | null | undefined): Quick | undefined {
  const l = key ? levels?.find((x) => x.level === key) : undefined;
  if (!l || !key) return undefined;
  return { key, label: (QUICK_NAME as Record<string, string[]>)[key]?.[0] ?? l.level, time: readTime(l.text.split(/\s+/).length), paras: paras(l.text) };
}

/** A hop link from one lesson to another: the top of the lesson, carrying where the reader came from. */
export const hopHref = (to: string, from: string) => `/lessons/${to}/?from=${from}`;

const hopCache = new Map<string, Promise<LessonHop | undefined>>();
/** Everything the hop sentence and its panel show on one lesson. undefined for a lesson that is not live. */
export function lessonHop(slug: string): Promise<LessonHop | undefined> {
  if (!hopCache.has(slug)) hopCache.set(slug, (async () => {
    const facts = await lessonFacts();
    const me = facts.get(slug);
    if (!me) return undefined;
    const d = me.data;
    const course = courseOf(d.course);
    const rank = stageRank(stageOf(course));
    const lessons = new Map([...facts.entries()].map(([s, f]) => [s, { title: f.data.title as string, rank: f.rank, order: f.data.order as number | undefined, ladder: f.data.ladder, activity: f.data.activity }]));
    const authored = authoredLinks(slug, lessons);
    const said = lessonSentence(await hops(slug), { slug, title: d.title, rank, courseTitle: course.title, explainLevels: d.explainLevels, sections: me.sections, authored });
    const mine = said.ideas as Awaited<ReturnType<typeof hops>>;
    const ideas: LessonHop['ideas'] = [];
    const from: Record<string, string> = {};
    for (const h of mine) {
      const v = await idea(h.id);
      if (!v) continue;
      for (const r of v.rungs) if (r.slug !== slug) from[r.slug] = r.title;
      const sideways = h.sideways.map((s) => {
        if (s.to) from[s.to.slug] = s.to.title;
        return { id: s.id, name: s.name, why: s.why, ...(s.to ? { lesson: { title: s.to.title, href: hopHref(s.to.slug, slug), rank: s.to.rank } } : {}) };
      });
      ideas.push({ ...v, sideways });
    }
    const quickDown = quick(d.explainLevels, said.quickDown);
    const more = said.more;
    const lines = said.lines as LessonHop['lines'];

    const rest = [said.quickDown ? null : QUICK_DOWN[rank], QUICK_UP[rank], rank === 1 ? 'bio2' : null, 'eli5']
      .filter((k, i, a) => k && k !== quickDown?.key && a.indexOf(k) === i)
      .map((k) => quick(d.explainLevels, k))
      .filter((q): q is Quick => Boolean(q));

    const shown = new Set([slug, ...ideas.flatMap((i) => i.rungs.map((r) => r.slug))]);
    const titled = (label: string, slugs: string[] = []) => {
      const items = [];
      for (const s of slugs) {
        const f = facts.get(s);
        if (f && !shown.has(s)) { items.push({ title: f.data.title as string, href: hopHref(s, slug) }); shown.add(s); from[s] = f.data.title; }
      }
      return items.length ? [{ label, items }] : [];
    };
    // Hand-picked links that are not on these ladders: close to the idea, not claimed as the same idea.
    const extra: LessonHop['extra'] = [];
    const also: number[] = [];
    for (const [label, band, ranks] of [['at grade 7', 1, [1]], ['at high school', 2, [2]], ['at college', 3, [3, 4, 5]]] as const) {
      const list = [...authored.down, ...authored.up].filter((x) => (ranks as readonly number[]).includes(x.rank));
      if (list.length) also.push(band);
      extra.push(...titled(`Close to this, ${label}`, list.map((x) => x.slug)));
    }
    return { slug, title: d.title, rank, ideas, lines, quickDown, quickRest: rest, more, extra, also, from };
  })());
  return hopCache.get(slug)!;
}
