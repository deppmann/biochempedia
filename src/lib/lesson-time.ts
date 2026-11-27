/* One recipe for how long a lesson takes, used everywhere the site prints a lesson's time:
   the "How long have you got?" control on the lesson page, the "About this lesson" parts list,
   course cards, /catalog.json and the Markdown copies, and JSON-LD timeRequired.

     reading   words in the main text / 150 (a study pace for dense science)
               + 1 minute for each "Predict." prompt + 3 minutes for each simulation
               ("Going deeper" is counted on its own and stated as optional)
     films     the sum of durationSec from the lesson's frontmatter
     stories   Side Hops: title and body words / 150
     skim      the main idea, headings, figure captions and film take-homes at 200 words a minute,
               plus 10 seconds to look at each figure
     self-test always stated apart ("when you want it"), never added to a length

   Ages 5 to 10 activity guides and the grade 7 and high school lessons carry a hand-set figure:
   the time the activity or the class period takes. For those the whole-lesson figure is the
   hand-set one, unless text, films and stories add up to more.

   Each kind of thing is summed in unrounded seconds and rounded once, and that one figure is the
   figure everywhere: a lesson's films are "19 minutes" on the Films stop, in the Lesson stop's
   sentence and on the "Play all films" button. The Films stop is the films' minutes plus the
   stories' minutes, so the sentence under it always adds up to its number. Inside the whole lesson,
   reading is what is left of the whole-lesson figure after films and stories.

   This file imports nothing, so scripts/test-lesson-time.mjs can load it in plain Node. */

export type StopId = 'skim' | 'stories' | 'films' | 'lesson';

export interface TimeFilm { title: string; durationSec: number; takeaways?: string[] }

export interface TimeInput {
  /** The course tier ('families', 'highschool', or a college tier). */
  tier: string;
  /** The lesson's MDX body. */
  body: string;
  estMinutes?: number;
  /** How many simulations the frontmatter lists. */
  simulations: number;
  explainer?: TimeFilm;
  films: TimeFilm[];
  /** Self-test questions (practice plus MCAT-style). */
  questions: number;
  /** The ## headings from render(), in order. */
  h2: { slug: string; text: string }[];
  /** Words in the skim: headings, figure captions, the main idea and film take-homes. */
  skimWords: number;
  /** Figures the skim shows (10 seconds each to look at). */
  skimFigures?: number;
  stories?: { hops: { afterHeading: string; title: string; text: string }[] };
}

export interface Stop {
  id: StopId;
  /** Whole minutes, as printed on the control. */
  min: number;
  /** The word under the minutes. */
  name: string;
  /** A few plain words under the name, for a stop whose name does not explain itself. */
  hint?: string;
}

export interface Part {
  /** The heading's anchor, or null for the text above the first heading. */
  slug: string | null;
  text: string;
  /** Minutes of reading and film in this part, as printed. */
  min: number;
  films: { title: string; sec: number }[];
  /** Title of the Side Hop that closes this part, if one does. */
  story?: string;
  optional: boolean;
  /** Whole minutes from the top of the lesson to the end of this part. */
  upTo: number;
  /** True when a sitting ends after this part: a good place to stop. */
  landing: boolean;
}

const WPM = 150;
const SKIM_WPM = 200;
const PER_SKIM_FIGURE = 10;
const PER_PREDICT = 60;
const PER_SIM = 180;
/** A long lesson gets a place to stop at the first section break past this many minutes. */
const SITTING_MIN = 18;
/** Lessons shorter than this are one sitting. */
const LONG_MIN = 30;

export const HAND_SET_TIERS = ['families', 'highschool'];

/** Words of running text in a piece of MDX (imports, code, tags and {expressions} left out). */
export function wordsOf(mdx: string): number {
  const text = mdx
    .replace(/^import .*$/gm, ' ')
    .replace(/```[\s\S]*?```/g, ' ')
    .replace(/<[^>]+>/g, ' ')
    .replace(/\{[^{}]*\}/g, ' ');
  return (text.match(/[A-Za-z0-9][A-Za-z0-9'’-]*/g) ?? []).length;
}

/** The body without "## Going deeper" (which runs to the next ## heading), and that section alone. */
export function splitDeeper(body: string): { core: string; deeper: string } {
  const [before, after] = body.split(/^## Going deeper.*$/m, 2);
  if (after === undefined) return { core: before, deeper: '' };
  const next = after.search(/^## /m);
  return next === -1 ? { core: before, deeper: after } : { core: before + after.slice(next), deeper: after.slice(0, next) };
}

const predictsIn = (mdx: string) => (mdx.match(/\*\*Predict\.\*\*/g) ?? []).length;

/** Seconds of reading in the main text. `extras` adds the Predict prompts and simulations. */
export function readingSeconds(body: string, simulations: number, extras = true): { core: number; optional: number } {
  const { core, deeper } = splitDeeper(body);
  const sec = (wordsOf(core) / WPM) * 60 + (extras ? predictsIn(core) * PER_PREDICT + simulations * PER_SIM : 0);
  return { core: sec, optional: (wordsOf(deeper) / WPM) * 60 };
}

/** Whole minutes for printing: never 0. */
export const minutesOf = (sec: number) => Math.max(1, Math.round(sec / 60));

/** "2:55" */
export const clock = (sec: number) => {
  const s = Math.round(sec);
  return `${Math.floor(s / 60)}:${String(s % 60).padStart(2, '0')}`;
};

/**
 * Split a printed total into parts that add up to it. Each part is rounded down, and the minutes
 * left over go to the parts with the largest remainders, so "about 45 of reading and 19 of film"
 * under a "64 min" stop is always true.
 */
export function split(totalMin: number, secs: number[]): number[] {
  const sum = secs.reduce((n, s) => n + s, 0);
  if (!sum) return secs.map(() => 0);
  const exact = secs.map((s) => (s / sum) * totalMin);
  const out = exact.map((x) => Math.floor(x));
  let left = totalMin - out.reduce((n, x) => n + x, 0);
  const order = exact.map((x, i) => ({ i, r: x - Math.floor(x) })).sort((a, b) => b.r - a.r);
  for (const { i } of order) { if (left <= 0) break; out[i] += 1; left -= 1; }
  return out;
}

/** The pieces of a lesson's time in seconds, and the whole-lesson figure. Enough for a card. */
export function wholeSeconds(i: Pick<TimeInput, 'tier' | 'body' | 'estMinutes' | 'simulations' | 'explainer' | 'films' | 'stories'>) {
  const handSet = HAND_SET_TIERS.includes(i.tier);
  // A hand-set lesson's tasks and simulations are part of the class period, not extra reading.
  const read = readingSeconds(i.body, i.simulations, !handSet);
  const film = [...(i.explainer ? [i.explainer] : []), ...i.films].reduce((n, f) => n + f.durationSec, 0);
  const stories = (i.stories?.hops ?? []).reduce((sec, hop) => sec + wordsOf(`${hop.title} ${hop.text}`) / WPM * 60, 0);
  const sum = read.core + film + stories;
  const set = handSet && i.estMinutes ? i.estMinutes * 60 : 0;
  return {
    handSet, read: read.core, optional: read.optional, film, stories, sum,
    /** Seconds for the whole lesson. */
    whole: Math.max(set, sum),
    /** The hand-set figure in minutes, when that is what the whole-lesson figure is. */
    period: set && set >= sum ? i.estMinutes! : 0,
  };
}

export function lessonTime(i: TimeInput) {
  const w = wholeSeconds(i);
  const guide = i.tier === 'families';
  const noun = guide ? 'activity' : 'lesson';
  const films = [...(i.explainer ? [i.explainer] : []), ...i.films];
  const hasStories = !!i.stories && i.stories.hops.length > 0;

  // ---- the stops: fixed order, and a stop the lesson lacks is absent --------------------------
  // An activity guide has no skim: its short stop is the set-up film. Everything else has one.
  const stops: Stop[] = [];
  const skimSec = Math.max(60, (i.skimWords / SKIM_WPM) * 60 + (i.skimFigures ?? 0) * PER_SKIM_FIGURE);
  const filmMin = films.length ? minutesOf(w.film) : 0;
  const storyMin = hasStories ? minutesOf(w.stories) : 0;
  if (!guide) stops.push({ id: 'skim', min: minutesOf(skimSec), name: 'Skim' });
  if (hasStories) stops.push({ id: 'stories', min: storyMin, name: 'Stories' });
  if (films.length) stops.push({ id: 'films', min: filmMin + storyMin, name: films.length === 1 ? 'Film' : 'Films' });
  stops.push({ id: 'lesson', min: minutesOf(w.whole), name: guide ? 'Activity' : 'Lesson' });

  // ---- the lesson, part by part ---------------------------------------------------------------
  const chunks: { heading: boolean; body: string }[] = [{ heading: false, body: '' }];
  let fence = false;
  for (const line of i.body.split('\n')) {
    if (/^\s*(```|~~~)/.test(line)) fence = !fence;
    if (!fence && /^##\s+\S/.test(line)) chunks.push({ heading: true, body: '' });
    else chunks[chunks.length - 1].body += line + '\n';
  }
  // Heading text from render() has smart quotes; Side Hops data keeps the lesson's plain ones.
  const plainQuotes = (t: string) => t.replace(/[‘’]/g, "'").replace(/[“”]/g, '"');
  const hopAfter = new Map((i.stories?.hops ?? []).map((h) => [plainQuotes(h.afterHeading), h.title]));
  let simsLeft = w.handSet ? 0 : i.simulations;
  let run = i.explainer ? i.explainer.durationSec : 0;
  const parts: (Part & { sec: number })[] = [];
  let hi = 0;
  for (const c of chunks) {
    const h = c.heading ? i.h2[hi++] : undefined;
    if (!c.heading && !c.body.trim()) continue;
    const text = h?.text ?? 'Opening';
    const optional = /^Going deeper/i.test(text);
    const inFilms = [...c.body.matchAll(/<LessonFilm\s+film=\{frontmatter\.films\[(\d+)\]\}/g)]
      .map((m) => i.films[Number(m[1])]).filter(Boolean)
      .map((f) => ({ title: f.title, sec: f.durationSec }));
    // A simulation sits where its island is placed in the text (a client: directive).
    const sims = Math.min((c.body.match(/\bclient:(?:load|visible|idle|only)/g) ?? []).length, simsLeft);
    simsLeft -= sims;
    const sec = (wordsOf(c.body) / WPM) * 60 + (w.handSet ? 0 : predictsIn(c.body) * PER_PREDICT + sims * PER_SIM)
      + inFilms.reduce((n, f) => n + f.sec, 0);
    if (!optional) run += sec;
    parts.push({ slug: h?.slug ?? null, text, min: minutesOf(sec), sec, films: inFilms, story: hopAfter.get(plainQuotes(text)), optional, upTo: minutesOf(run), landing: false });
  }
  // Sittings: only where the lesson is long enough to need them, and never on a hand-set lesson
  // (a class period is one sitting by design).
  if (!w.handSet && run / 60 >= LONG_MIN) {
    let acc = i.explainer ? i.explainer.durationSec : 0;
    let done = acc;
    const main = parts.filter((p) => !p.optional);
    main.forEach((p, n) => {
      acc += p.sec;
      done += p.sec;
      if (acc / 60 >= SITTING_MIN && (run - done) / 60 >= 8 && n < main.length - 1) { p.landing = true; acc = 0; }
    });
  }

  // ---- the parts of each count, as printed, adding up to the stop's number -------------------
  const lessonMin = minutesOf(w.whole);
  const readMin = Math.max(0, lessonMin - filmMin - storyMin);

  return {
    stops,
    noun,
    guide,
    handSet: w.handSet,
    /** The hand-set class-period or activity figure, when that is what the whole length is. */
    period: w.period,
    /** Whole-lesson minutes: the figure every card and list prints. */
    whole: lessonMin,
    /** Minutes of reading inside the whole lesson: what is left of `whole` after `filmMin` and `storyMin`. */
    readMin,
    /** Reading and films together, for a hand-set lesson's "the rest is doing" note. */
    sumMin: minutesOf(w.sum),
    optional: Math.round(w.optional / 60),
    filmCount: films.length,
    /** Minutes of film, the same figure wherever it is printed. */
    filmMin,
    filmSec: Math.round(w.film),
    storyCount: i.stories?.hops.length ?? 0,
    /** Minutes of Side Hop reading, the same figure wherever it is printed. */
    storyMin,
    quiz: i.questions,
    takeCount: films.filter((f) => f.takeaways?.length).length,
    parts: parts.map(({ sec: _sec, ...p }) => p),
    sittings: parts.filter((p) => p.landing).length + 1,
  };
}

export type LessonTime = ReturnType<typeof lessonTime>;
