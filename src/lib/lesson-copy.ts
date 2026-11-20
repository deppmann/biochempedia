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

/** The one sentence under the control for each stop: what the stop holds. */
export function linesFor(t: LessonTime, o: { figures: number }): Record<StopId, string> {
  const n = t.filmCount;
  const stories = t.storyCount ? `${say(t.storyCount)} short ${plural(t.storyCount, 'story', 'stories')}` : '';

  // ---- Skim
  const skimHas = [
    'the main idea',
    o.figures ? (o.figures === 1 ? 'the figure' : 'the figures') : '',
    t.takeCount ? `what ${n === 1 ? 'the film shows' : 'the films show'}` : '',
  ].filter(Boolean);
  const skim = `${cap(skimHas.length > 1 ? list(skimHas) : 'the main idea and the headings')}. Tap a heading to read that part.`;

  // ---- Stories
  const storiesLine = t.storyCount
    ? `${cap(stories)} from real life that go with this ${t.noun}. About ${mins(t.storyMin)} to hear, or read them below.`
    : '';

  // ---- Films. A film under a minute and a half is given in seconds: "1 minute" for 42 seconds is not honest.
  const filmLen = t.filmSec < 90 ? `${t.filmSec} seconds` : mins(t.filmMin);
  let films = '';
  if (n === 1) {
    films = t.guide ? `The film, ${filmLen}, for the grown-up to look at before the activity.`
      : t.storyCount ? `The film, ${filmLen}, then ${stories} told aloud, ${t.storyMore} more.`
      : t.takeCount ? `The film, ${filmLen}, and what to take from it.` : `The film, ${filmLen}.`;
  } else if (n > 1) {
    films = t.storyCount
      ? `${cap(theFilms(n))}, ${mins(t.filmMin)}, then ${stories} told aloud, ${t.storyMore} more.`
      : `${cap(theFilms(n))} in order, ${mins(t.filmMin)}.${t.takeCount === n ? ' Each one ends with what to take from it.' : ''}`;
  }

  // ---- The whole thing
  let lesson: string;
  if (t.period) {
    const included = [n ? theFilms(n) : '', stories].filter(Boolean).join(' and ');
    lesson = t.guide
      ? `All of it, done with a child: about ${mins(t.period)}${included ? `, ${included} included` : ''}.`
      : `All of it: about ${mins(t.period)} in class${included ? `, ${included} included` : ''}.`;
  } else {
    const bits = [`${mins(t.readMin)} of reading`, n ? `${t.filmInLesson} of film` : '', t.storyCount ? `${t.storyInLesson} of stories` : ''].filter(Boolean);
    lesson = `All of it: about ${list(bits)}.`;
    if (t.sittings > 1) {
      const stopsN = t.sittings - 1;
      lesson += ` There ${stopsN === 1 ? 'is a place' : `are ${say(stopsN)} places`} to stop, and your place is kept.`;
    }
  }
  return { skim, stories: storiesLine, films, lesson };
}

/** What the page says at the end of each shorter stop: what was done, never what is left. */
export function endingsFor(t: LessonTime): Record<'skim' | 'stories' | 'films', string> {
  const n = t.filmCount;
  return {
    skim: 'That is the skim.',
    stories: 'Those are the stories.',
    films: n === 1 ? 'That is the film.' : `That is ${theFilms(n)}.`,
  };
}

/** Sentences the page script says. */
export const SAID = {
  legend: 'How long have you got?',
  carry: 'The next lesson will open this way too.',
  remembered: 'Opened the way you left the last lesson.',
  noStories: 'No stories on this lesson yet, so this is the skim.',
  noFilm: 'No film on this lesson, so this is the skim.',
  deepLink: 'That link goes to a place in the text, so the whole lesson is open.',
  inClass: 'You are in a class on this device, so the whole lesson is open.',
  landing: 'A good place to stop. Your place is kept.',
  readPart: 'Read this part',
  foldPart: 'Fold it again',
} as const;
