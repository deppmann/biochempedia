/* Reading time, worked out from the lesson itself when the site is built.

   The hand-set `estMinutes` did not move when lessons were rewritten at twice the length, so
   college lessons no longer use it. The estimate here is:
     words in the main text ÷ 150   (a study pace for dense science, slower than casual reading)
     + 1 minute for each "Predict." prompt in the text
     + 3 minutes for each simulation
   "Going deeper" is counted on its own and shown as optional. Quiz questions at the finish line
   are not included.

   Since 2026-11-20 the recipe itself lives in src/lib/lesson-time.ts, which also counts films and
   Side Hop reading. lessonMinutes() below is the reading part alone; wholeMinutes() is the whole
   lesson, and is what the site prints.

   Ages 5–10 activity guides and the grade 7 and high school lessons keep their hand-set figure:
   there it is the time the activity or the class period takes, not time spent reading. */
import { courseOf } from '../data/courses';
import { readingSeconds, wholeSeconds, minutesOf, HAND_SET_TIERS } from './lesson-time';
import { sideHopsFor } from './side-hops';

export interface LessonMinutes {
  /** Minutes for the main text, or the hand-set figure for school and family lessons. */
  core: number;
  /** Extra minutes for "Going deeper", 0 when the lesson has none. */
  optional: number;
}

interface LessonLike {
  body?: string;
  data: { course: string; estMinutes?: number; simulations: unknown[] };
}

/** Reading only (no films, no stories). The study planner adds the films a plan picks to this. */
export function lessonMinutes(l: LessonLike): LessonMinutes | undefined {
  const tier = courseOf(l.data.course).tier;
  if (HAND_SET_TIERS.includes(tier) || !l.body) {
    return l.data.estMinutes ? { core: l.data.estMinutes, optional: 0 } : undefined;
  }
  const sec = readingSeconds(l.body, l.data.simulations.length);
  return { core: minutesOf(sec.core), optional: Math.round(sec.optional / 60) };
}

interface WholeLike {
  body?: string;
  data: {
    slug: string; course: string; estMinutes?: number; simulations: unknown[];
    explainer?: { title: string; durationSec: number }; films: { title: string; durationSec: number }[];
  };
}

/**
 * The whole lesson in minutes: reading, every film and the Side Hop reading, or the hand-set class
 * period when that is longer. This is the figure the lesson page's control prints on its last stop,
 * and the one course cards, /catalog.json, the Markdown copies and JSON-LD timeRequired print too
 * (src/lib/lesson-time.ts has the recipe).
 */
export function wholeMinutes(l: WholeLike): number | undefined {
  const d = l.data;
  if (!l.body && !d.estMinutes) return undefined;
  const hops = sideHopsFor(d.slug);
  return minutesOf(wholeSeconds({
    tier: courseOf(d.course).tier, body: l.body ?? '', estMinutes: d.estMinutes, simulations: d.simulations.length,
    explainer: d.explainer, films: d.films,
    stories: hops ? { hops: hops.hops } : undefined,
  }).whole);
}

/** "~31 min", for cards and lists. */
export const minutesLabel = (m: number | undefined) => (m ? `~${m} min` : undefined);
