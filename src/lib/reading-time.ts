/* Reading time, worked out from the lesson itself when the site is built.

   The hand-set `estMinutes` did not move when lessons were rewritten at twice the length, so
   college lessons no longer use it. The estimate here is:
     words in the main text ÷ 150   (a study pace for dense science, slower than casual reading)
     + 1 minute for each "Predict." prompt in the text
     + 3 minutes for each simulation
   "Going deeper" is counted on its own and shown as optional. Quiz questions at the finish line
   are not included.

   Ages 5–10 activity guides and the grade 7 and high school lessons keep their hand-set figure:
   there it is the time the activity or the class period takes, not time spent reading. */
import { courseOf } from '../data/courses';

const WPM = 150;
const PER_PREDICT = 1;
const PER_SIM = 3;

function words(mdx: string): number {
  const text = mdx
    .replace(/^import .*$/gm, ' ')
    .replace(/```[\s\S]*?```/g, ' ')
    .replace(/<[^>]+>/g, ' ')
    .replace(/\{[^{}]*\}/g, ' ');
  return (text.match(/[A-Za-z0-9][A-Za-z0-9'’-]*/g) ?? []).length;
}

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

export function lessonMinutes(l: LessonLike): LessonMinutes | undefined {
  const tier = courseOf(l.data.course).tier;
  if (tier === 'families' || tier === 'highschool' || !l.body) {
    return l.data.estMinutes ? { core: l.data.estMinutes, optional: 0 } : undefined;
  }
  // Split off "## Going deeper" (up to the next ## heading, if any).
  const [before, after] = l.body.split(/^## Going deeper.*$/m, 2);
  let core = before;
  let deeper = '';
  if (after !== undefined) {
    const next = after.search(/^## /m);
    deeper = next === -1 ? after : after.slice(0, next);
    if (next !== -1) core += after.slice(next);
  }
  const predicts = (core.match(/\*\*Predict\.\*\*/g) ?? []).length;
  const minutes = words(core) / WPM + predicts * PER_PREDICT + l.data.simulations.length * PER_SIM;
  return { core: Math.max(1, Math.round(minutes)), optional: Math.round(words(deeper) / WPM) };
}

/** "~31 min", for cards and lists. */
export const minutesLabel = (m: LessonMinutes | undefined) => (m ? `~${m.core} min` : undefined);
