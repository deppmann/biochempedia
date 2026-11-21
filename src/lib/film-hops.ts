/* Where a film's idea lives at other levels, and what sits next door (2026-11-20).

   The theater on /watch/ shows this under every film. It asks one question, hopsFor(lesson, film),
   and draws whatever comes back.

   Source, in order:
     1. the hop graph (src/lib/topic-graph.ts), when it has an idea for the lesson: the idea's ladder
        gives Simpler and Deeper, with each rung's note on what that level adds; its sideways hops give
        the ideas next door, each with its reason; its films, in level order, give "play this idea
        at every level";
     2. otherwise what was on main before the graph: the authored depth ladder in the lesson
        frontmatter (read in both directions) and src/data/lesson-links.json (before, after, films
        elsewhere).

   Rules that do not depend on the source: a level is never a prerequisite and never a rank. The two
   directions are called "Simpler" and "Deeper"; nothing here orders the viewer. An ages 5 to 10
   lesson's film shows a grown-up how to set up an activity; it is never offered as a film that
   teaches the idea, so that rung links the activity itself. */
import { getCollection } from 'astro:content';
import { courseOf } from '../data/courses';
import { STAGES, stageOf } from '../data/stages';
import { watchHref } from './films';
import links from '../data/lesson-links.json';
import { hops as graphHops, ladder as graphLadder, filmsFor, conceptsOf, type LadderRung } from './topic-graph';

export interface Hop {
  lesson: string;
  lessonTitle: string;
  /** Stage key and its reader-facing name. */
  stage: string;
  stageTitle: string;
  /** The lesson's opening film, when it has one: where "Watch" goes. */
  film?: { key: string; title: string; href: string; durationSec: number };
  lessonHref: string;
  /** One line on why this hop, when the source gives one. */
  why?: string;
  /** From the graph: what this level adds to the idea. */
  adds?: string;
  /** For a neighbouring idea from the graph: the idea's name. */
  idea?: string;
}
export interface FilmHops {
  /** The lesson the film belongs to. */
  here: { lesson: string; lessonTitle: string; stage: string; stageTitle: string };
  /** The same idea with less machinery, nearest level first. */
  simpler: Hop[];
  /** The same idea taken further, nearest level first. */
  deeper: Hop[];
  /** Neighbouring ideas. From the graph they are in `near`; from the older data in the other three. */
  sideways: { near: Hop[]; before: Hop[]; after: Hop[]; elsewhere: Hop[] };
  /** The idea this film is about, when the graph has one, and every idea its lesson teaches. */
  idea?: { id: string; name: string };
  ideas: string[];
  /** The idea's films from the simplest level to the deepest, when they span two or more levels:
   *  what /films/run/?idea=<id> plays. */
  everyLevel?: { href: string; films: number; minutes: number; levels: number };
}

type LinkRec = { before: { slug: string; why: string }[]; after: { slug: string; why: string }[]; elsewhere: { id: string; why: string }[] };

interface Node {
  slug: string; title: string; stage: string; rank: number;
  film?: Hop['film'];
  /** Authored ladder neighbours, as written (direction is worked out from the levels). */
  ladder: string[];
}

let cache: Promise<Map<string, Node>> | undefined;
const filmKey = (src: string) => src.replace(/^\/explainers\//, '').replace(/\.mp4$/, '');

function nodes(): Promise<Map<string, Node>> {
  cache ??= (async () => {
    const lessons = await getCollection('lessons', ({ data }) => !data.draft);
    const map = new Map<string, Node>();
    for (const l of lessons) {
      const d = l.data;
      const stage = stageOf(courseOf(d.course));
      map.set(d.slug, {
        slug: d.slug, title: d.title, stage, rank: STAGES.findIndex((s) => s.key === stage),
        // (not for an ages 5 to 10 activity, whose film is the grown-up's set-up)
        film: d.explainer && stage !== 'ages-5-10' ? { key: filmKey(d.explainer.src), title: d.explainer.title, href: watchHref(d.slug), durationSec: d.explainer.durationSec } : undefined,
        ladder: [...(d.activity?.stepUp ?? []), ...(d.ladder?.grade7 ?? []), ...(d.ladder?.biology ?? []), ...(d.ladder?.college ?? [])],
      });
    }
    // Read every authored link in both directions.
    for (const n of [...map.values()]) for (const other of n.ladder) {
      const o = map.get(other);
      if (o && !o.ladder.includes(n.slug)) o.ladder.push(n.slug);
    }
    return map;
  })();
  return cache;
}

const stageTitle = (key: string) => STAGES.find((s) => s.key === key)?.title ?? key;
const hop = (n: Node, why?: string): Hop => ({
  lesson: n.slug, lessonTitle: n.title, stage: n.stage, stageTitle: stageTitle(n.stage),
  film: n.film, lessonHref: `/lessons/${n.slug}/`, ...(why ? { why } : {}),
});

/* The data that was on main before the graph. */
async function authored(lesson: string): Promise<FilmHops | null> {
  const map = await nodes();
  const me = map.get(lesson);
  if (!me) return null;
  const rungs = me.ladder.map((s) => map.get(s)).filter((n): n is Node => !!n && n.slug !== lesson);
  const near = (a: Node, b: Node) => Math.abs(a.rank - me.rank) - Math.abs(b.rank - me.rank) || a.title.localeCompare(b.title);
  const simpler = rungs.filter((n) => n.rank < me.rank).sort(near).map((n) => hop(n));
  const deeper = rungs.filter((n) => n.rank > me.rank).sort(near).map((n) => hop(n));
  const onLadder = new Set(rungs.map((n) => n.slug));

  const rec = (links.lessons as Record<string, LinkRec>)[lesson];
  const side = (items: { slug: string; why: string }[] = []) => items
    .map((x) => ({ n: map.get(x.slug), why: x.why }))
    .filter((x): x is { n: Node; why: string } => !!x.n && x.n.slug !== lesson && !onLadder.has(x.n.slug))
    .map((x) => hop(x.n, x.why));
  const elsewhere = (rec?.elsewhere ?? [])
    .filter((x) => x.id.startsWith('film:'))
    .map((x) => ({ slug: x.id.slice(5), why: x.why }));
  const before = side(rec?.before);
  const after = side(rec?.after);
  const taken = new Set([...before, ...after].map((h) => h.lesson));
  return {
    here: { lesson: me.slug, lessonTitle: me.title, stage: me.stage, stageTitle: stageTitle(me.stage) },
    simpler,
    deeper,
    sideways: { near: [], before, after, elsewhere: side(elsewhere).filter((h) => !taken.has(h.lesson) && h.film) },
    ideas: [],
  };
}

/** The films of an idea that teach it, simplest level first (set-up films for grown-ups left out). */
export async function ideaFilms(id: string) {
  return (await filmsFor(id)).filter((f) => f.kind !== 'activity' && f.href.startsWith('/watch/')).sort((a, b) => a.rank - b.rank);
}

const fromRung = (r: LadderRung, extra: Partial<Hop> = {}): Hop => {
  const f = r.films.find((x) => x.kind !== 'activity' && x.href.startsWith('/watch/'));
  return {
    lesson: r.slug, lessonTitle: r.title, stage: r.stage, stageTitle: r.stageTitle,
    film: f ? { key: f.key, title: f.title, href: f.href, durationSec: f.durationSec } : undefined,
    lessonHref: r.href, ...(r.adds ? { adds: r.adds } : {}), ...extra,
  };
};

/**
 * Simpler, deeper and sideways for a film. `lesson` is the film's lesson; `film` is its key (the file
 * under /explainers/ without ".mp4"), used to pick which of the lesson's ideas the film is about.
 * Null when the lesson is not published.
 */
export async function hopsFor(lesson: string, film?: string): Promise<FilmHops | null> {
  const old = await authored(lesson);
  if (!old) return null;
  const mine = await graphHops(lesson);
  const ideas = (await conceptsOf(lesson)).map((c) => c.id);
  if (!mine.length) return { ...old, ideas };
  // The idea this film shows: the first of the lesson's ideas whose films include it; else the lesson's first idea.
  let pick = mine[0];
  if (film) for (const h of mine) if ((await filmsFor(h.id)).some((f) => f.key === film)) { pick = h; break; }
  const rungs = (await graphLadder(pick.id)).filter((r) => r.role === 'core' && r.slug !== lesson);
  const me = old.here;
  const rank = (k: string) => STAGES.findIndex((s) => s.key === k);
  const near = (a: LadderRung, b: LadderRung) => Math.abs(a.rank - rank(me.stage)) - Math.abs(b.rank - rank(me.stage)) || a.order - b.order;
  const simpler = rungs.filter((r) => r.rank < rank(me.stage)).sort(near).map((r) => fromRung(r));
  const deeper = rungs.filter((r) => r.rank > rank(me.stage)).sort(near).map((r) => fromRung(r));
  const sideways = pick.sideways.filter((n) => n.to).map((n) => fromRung(n.to!, { idea: n.name, why: n.why }));
  const films = await ideaFilms(pick.id);
  const levels = new Set(films.map((f) => f.stage)).size;
  return {
    here: me,
    // Where the graph has no rung on one side, the authored ladder still may.
    simpler: simpler.length ? simpler : old.simpler,
    deeper: deeper.length ? deeper : old.deeper,
    sideways: { near: sideways, before: sideways.length ? [] : old.sideways.before, after: sideways.length ? [] : old.sideways.after, elsewhere: sideways.length ? [] : old.sideways.elsewhere },
    idea: { id: pick.id, name: pick.name },
    ideas,
    ...(levels >= 2 ? { everyLevel: { href: `/films/run/?idea=${encodeURIComponent(pick.id)}`, films: films.length, minutes: Math.max(1, Math.round(films.reduce((s, f) => s + f.durationSec, 0) / 60)), levels } } : {}),
  };
}
