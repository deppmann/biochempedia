/* Every sentence the "How long have you got?" control prints, built from the count in
   lesson-time.ts. One place, so the words can be read and changed without hunting through markup.
   Imports nothing, so scripts/test-lesson-time.mjs can check that the numbers in a sentence add up. */
import type { LessonTime, StopId } from './lesson-time';

const NUM = ['no', 'one', 'two', 'three', 'four', 'five', 'six', 'seven', 'eight', 'nine', 'ten'];
/** Small counts as words ("three stories"), larger ones as digits. */
export const say = (n: number) => NUM[n] ?? String(n);
export const plural = (n: number, one: string, many = `${one}s`) => (n === 1 ? one : many);
const cap = (s: string) => s.charAt(0).toUpperCase() + s.slice(1);
const mins = (n: number) => `${n} ${plural(n, 'minute')}`;
const list = (xs: string[]) => (xs.length > 1 ? `${xs.slice(0, -1).join(', ')} and ${xs[xs.length - 1]}` : xs[0]);

/** "both films", "all six films", "the film" */
export const theFilms = (n: number) => (n === 1 ? 'the film' : n === 2 ? 'both films' : `all ${say(n)} films`);

/** Said only where the device can keep a place; the page script takes it off when storage is blocked. */
export const KEPT = ' Your place is kept.';

/** The one sentence under the control for each stop: what the stop holds. */
export function linesFor(t: LessonTime, o: { figures: number; laterLooks?: boolean }): Record<StopId, string> {
  const n = t.filmCount;
  const stories = t.storyCount ? `${say(t.storyCount)} Side ${plural(t.storyCount, 'Hop')}` : '';

  // ---- Skim
  const skimHas = [
    'the main idea',
    o.figures ? (o.figures === 1 ? 'the figure' : 'the figures') : '',
    t.takeCount ? `what ${n === 1 ? 'the film shows' : 'the films show'}` : '',
  ].filter(Boolean);
  const skim = `${cap(skimHas.length > 1 ? list(skimHas) : 'the main idea and the headings')}. Under each heading, "Read this part" opens it.`;

  // ---- Stories
  const storiesLine = t.storyCount
    ? `${cap(stories)} to read alongside this ${t.noun}.`
    : '';

  // ---- Films. A film under a minute and a half is given in seconds: "1 minute" for 42 seconds is not honest.
  const filmLen = t.filmSec < 90 ? `${t.filmSec} seconds` : mins(t.filmMin);
  let films = '';
  if (n === 1) {
    films = t.guide ? `The film, ${filmLen}, and the safety notes, for the grown-up to look at before the activity.`
      : t.storyCount ? `The film, ${filmLen}, with ${stories} to read in about ${mins(t.storyMin)}.`
      : t.takeCount ? `The film, ${filmLen}, and what to take from it.` : `The film, ${filmLen}.`;
  } else if (n > 1) {
    films = t.storyCount
      ? `${cap(theFilms(n))}, ${mins(t.filmMin)}, with ${stories} to read in about ${mins(t.storyMin)}.`
      : `${cap(theFilms(n))} in order, ${mins(t.filmMin)}.${t.takeCount === n ? ' Each one ends with what to take from it.' : ''}`;
  }

  // ---- The whole thing
  let lesson: string;
  if (t.period) {
    // The hand-set figure is the class period or the hands-on time. What it was meant to cover
    // (the films? the tasks?) is not recorded, so the sentence claims no more than the figure.
    lesson = t.guide
      ? `The hands-on part, done with a child: about ${mins(t.period)}${o.laterLooks ? ', then a few quick looks later' : ''}.`
      : `The whole lesson: about ${mins(t.period)}, the length of a class.`;
  } else {
    const bits = [`${mins(t.readMin)} of reading`, n ? `${t.filmMin} of film` : '', t.storyCount ? `${t.storyMin} of stories` : ''].filter(Boolean);
    lesson = `The whole ${t.noun}: about ${list(bits)}`;
    if (t.sittings > 1) {
      const stopsN = t.sittings - 1;
      lesson += `, with ${stopsN === 1 ? 'a place' : `${say(stopsN)} places`} to stop.${KEPT}`;
    } else lesson += '.';
  }
  return { skim, stories: storiesLine, films, lesson };
}

/** What the page says at the end of each shorter stop: what was done, never what is left. */
export function endingsFor(t: LessonTime): Record<'skim' | 'stories' | 'films', string> {
  const n = t.filmCount;
  return {
    skim: 'That is the skim: you have the shape of it.',
    stories: 'Those are the stories. The idea under them is the one the lesson builds.',
    films: t.guide ? 'That is the film. The rest of the activity is the fun part.' : `That is ${theFilms(n)}: the lesson in pictures.`,
  };
}

/** Sentences the page script says. */
export const SAID = {
  legend: 'How long have you got?',
  carry: 'The next lesson will open this way too.',
  // Not every lesson has stories or a film, so the promise names the lessons it is true of.
  carryStories: 'Lessons with stories will open this way too.',
  carryFilms: 'Lessons with films will open this way too.',
  remembered: 'Opened at the length you last chose.',
  noStories: 'No stories on this lesson yet, so this is the skim.',
  noFilm: 'No film on this lesson, so this is the skim.',
  deepLink: 'That link goes to a place in the text, so the whole lesson is open.',
  inClass: 'You are in a class on this device, so the whole lesson is open.',
  supports: 'That link sets the help with the tasks, so the whole lesson is open.',
  landing: 'A good place to stop.',
  kept: KEPT,
  readPart: 'Read this part',
  foldPart: 'Fold it again',
} as const;
