/* Where a film's idea lives at other levels, and what sits next door (2026-11-20).

   The theater on /watch/ shows this under every film. It asks one question, hopsFor(lesson), and
   draws whatever comes back, so the source behind the answer can change without the page changing.

   Today's source is what is already written and checked on main:
     - the authored depth ladder in the lesson frontmatter (activity.stepUp, ladder.grade7,
       ladder.biology, ladder.college), read in both directions, so a college lesson named by a high
       school lesson offers that high school lesson back as the simpler one;
     - src/data/lesson-links.json (before, after, and films elsewhere on the site), each with its
       one-line reason.
   When the shared concept graph is merged, replace the body of hopsFor() with a lookup in it; the
   returned shape is what the graph's ladder and sideways hops already are.

   Rules that do not depend on the source: a level is never a prerequisite and never a rank. The two
   directions are called "Simpler" and "Deeper"; nothing here orders the viewer. */
import { getCollection } from 'astro:content';
import { courseOf } from '../data/courses';
import { STAGES, stageOf } from '../data/stages';
import { watchHref } from './films';
import links from '../data/lesson-links.json';

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
}
export interface FilmHops {
  /** The lesson the film belongs to. */
  here: { lesson: string; lessonTitle: string; stage: string; stageTitle: string };
  /** The same idea with less machinery, nearest level first. */
  simpler: Hop[];
  /** The same idea taken further, nearest level first. */
  deeper: Hop[];
  /** Neighbouring ideas. */
  sideways: { before: Hop[]; after: Hop[]; elsewhere: Hop[] };
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
        film: d.explainer ? { key: filmKey(d.explainer.src), title: d.explainer.title, href: watchHref(d.slug), durationSec: d.explainer.durationSec } : undefined,
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

/** Simpler, deeper and sideways for the lesson a film belongs to. Null when the lesson is not published. */
export async function hopsFor(lesson: string): Promise<FilmHops | null> {
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
    sideways: { before, after, elsewhere: side(elsewhere).filter((h) => !taken.has(h.lesson) && h.film) },
  };
}
