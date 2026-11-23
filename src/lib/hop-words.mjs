/* Hopping, in words: every phrase the site uses to say "the same idea at another level".

   One pure module (no Astro, no Node), so the lesson page, the idea pages, the search script in
   the browser and scripts/test-hop.mjs all build their sentences from the same templates.

   The rules the words keep (see /ideas/ and the hop sentence on a lesson):
   - "Simpler" and "Deeper" describe the explanation, never the reader. No "easier", no "level up",
     no up or down as rank.
   - A level is named so its own readers know it: the three college bands are "a first college
     course", "college core" and "upper-level college", and a lesson's own sentence names its course.
   - A gap is said plainly, once, with the size of the step in words.
   - Nothing counts what a reader has or has not done. */

export const LEVEL_KEYS = ['ages-5-10', 'grade-7', 'high-school', 'starting-college', 'college-core', 'college-further', 'graduate'];
export const rankOf = (key) => LEVEL_KEYS.indexOf(key);

/** In brackets after a lesson title, and in lists: "(grade 7)". */
export const LEVEL_SHORT = ['ages 5 to 10', 'grade 7', 'high school', 'a first college course', 'college core', 'upper-level college', 'graduate level'];
/** As the label of a rung. */
export const LEVEL_LABEL = ['Ages 5 to 10', 'Grade 7', 'High school', 'College, a first course', 'College, the core', 'College, upper level', 'Graduate'];
/** "No lesson … yet": the level with its preposition. */
const LEVEL_AT = ['for ages 5 to 10', 'at grade 7', 'at high school', 'in a first college course', 'in the college core', 'in upper-level college', 'at graduate level'];
/** The kind of course, after its name: "in Physiology, an upper-level college course". */
const COURSE_KIND = [null, null, null, 'a first college course', 'a core college course', 'an upper-level college course', 'a graduate course'];

const NUM = ['no', 'one', 'two', 'three', 'four', 'five', 'six', 'seven'];
export const numWord = (n) => NUM[n] ?? String(n);
export const cap = (s) => s.charAt(0).toUpperCase() + s.slice(1);

/** "a", "a and b", "a, b and c". */
export function andList(items, word = 'and') {
  if (items.length <= 1) return items.join('');
  return `${items.slice(0, -1).join(', ')} ${word} ${items[items.length - 1]}`;
}

// ------------------------------------------------------------------ an idea's name inside a sentence

/* An idea's display name (the graph's `short`, or its name when that is already short) is written
   as a heading. Inside a sentence a bracket or gloss goes and the first letter drops, unless the
   word is a name or an abbreviation. The few entries below are names that need an article, or
   read as a clause, after "This lesson teaches". Pass the display name: `c.short ?? c.name`. */
const IN_SENTENCE = {
  'perturbation-and-rescue': 'rescue experiments',
  'retinal-degeneration': 'retinal degeneration',
  'needed-versus-enough': 'necessity and sufficiency',
  'corticospinal-tract': 'the corticospinal tract',
  'electrochemical-gradient': 'the electrochemical gradient',
  'plant-life-cycle': 'the plant life cycle',
  'germ-theory': 'the germ theory of disease',
  'neuronal-polarity': 'neuronal polarity',
  'gene-to-protein': 'how a gene becomes a protein',
  'regulators-and-conformers': 'regulators and conformers',
  'forward-and-reverse-genetics': 'forward and reverse genetics',
  'basal-ganglia': 'the basal ganglia',
  'pentose-phosphate-pathway': 'the pentose phosphate pathway',
  'resting-membrane-potential': 'the resting potential',
  'pressure-natriuresis': 'the kidney and long-term blood pressure',
  'origin-of-modern-humans': 'the origin of modern humans',
  'nervous-system-organization': 'how the nervous system is laid out',
  'effective-population-size': 'effective population size',
};
const KEEP_CAPITAL = /^(Rho|Hardy|Neanderthal|Rett|Notch|Wnt|Hox|Hedgehog|G protein|Fragile X|Piezo)\b/;
export function inSentence(id, name) {
  if (IN_SENTENCE[id]) return IN_SENTENCE[id];
  let s = String(name).replace(/\s*\([^)]*\)/g, '').trim();
  s = s.split(/:\s|, the /)[0].trim();
  const first = s.split(/[\s-]/)[0];
  // An abbreviation or a mixed-case symbol (ATP, DNA, mTOR, pH, NF-κB, GTPase) stays as written.
  if (KEEP_CAPITAL.test(s) || /[A-Z0-9Ͱ-Ͽ]/.test(first.slice(1)) || /^[a-z]/.test(s)) return s;
  return s.charAt(0).toLowerCase() + s.slice(1);
}

// ------------------------------------------------------------------ levels and steps

/** Levels strictly between two ranks. */
export function between(a, b) {
  const lo = Math.min(a, b), hi = Math.max(a, b);
  const out = [];
  for (let r = lo + 1; r < hi; r++) out.push(r);
  return out;
}

/* For the size of a step the three college bands count as one place: most ideas are taught in
   one college course, so "nothing in the college core yet" after every college link would be noise.
   The level's own name already says which kind of college course it is. */
const BAND = [0, 1, 2, 3, 3, 3, 4];
const BAND_AT = ['for ages 5 to 10', 'at grade 7', 'at high school', 'at college level', 'at graduate level'];

/** The honest size of a step, for after a lesson's level. '' when nothing lies between. */
export function stepNote(from, to) {
  const gap = between(BAND[from], BAND[to]);
  if (!gap.length) return '';
  if (gap.length === 1) return `nothing ${BAND_AT[gap[0]]} yet`;
  return 'a big step: nothing in between yet';
}

/** "(grade 7)", "(upper-level college, a big step: nothing in between yet)". */
export function levelNote(from, to) {
  const step = stepNote(from, to);
  return `(${LEVEL_SHORT[to]}${step ? (step.startsWith('a big') ? ', ' : '; ') + step : ''})`;
}

/** "No lesson on osmosis at high school yet." / "… at these three levels yet." */
export function gapLine(idea, ranks) {
  if (ranks.length === 1) return `No lesson on ${idea} ${LEVEL_AT[ranks[0]]} yet.`;
  if (ranks.length === 2) return `No lesson on ${idea} ${LEVEL_AT[ranks[0]]} or ${LEVEL_AT[ranks[1]]} yet.`;
  return `No lesson on ${idea} at these ${numWord(ranks.length)} levels yet.`;
}

/** Ranks from a bit mask (bit 0 = ages 5 to 10), lowest first. */
export const ranksOf = (mask) => LEVEL_KEYS.map((_, i) => i).filter((i) => mask & (1 << i));
export const maskOf = (ranks) => ranks.reduce((m, r) => m | (1 << r), 0);

/** The sentence that stands for the picture: "Taught at four levels: grade 7, …". */
export function taughtAt(mask) {
  const ranks = ranksOf(mask);
  if (!ranks.length) return '';
  if (ranks.length === 1) return `Taught at one level so far: ${LEVEL_SHORT[ranks[0]]}.`;
  return `Taught at ${numWord(ranks.length)} levels: ${andList(ranks.map((r) => LEVEL_SHORT[r]))}.`;
}
/**
 * The same sentence over a ladder drawn for one lesson. That ladder can carry a rung the idea's own
 * record does not have: a lesson picked by hand for the lesson being read (`picked`, as ranks). The
 * sentence then counts every rung the reader sees, so it agrees with the ladder's "Show all three
 * levels" button, and says which rung was picked by hand. With nothing picked it is taughtAt(mask).
 * @param {number} mask levels where the idea is taught
 * @param {number[]} [picked] levels of the hand-picked rungs
 */
export function shownAt(mask, picked = []) {
  const extra = [...new Set(picked)].filter((r) => r >= 0 && r < LEVEL_KEYS.length && !(mask & (1 << r))).sort((a, b) => a - b);
  if (!extra.length) return taughtAt(mask);
  const ranks = ranksOf(mask | maskOf(extra));
  const one = extra.length === 1;
  return `${cap(numWord(ranks.length))} levels here: ${andList(ranks.map((r) => LEVEL_SHORT[r]))}. `
    + `The ${one ? 'lesson' : 'lessons'} ${andList(extra.map((r) => LEVEL_AT[r]))} ${one ? 'was' : 'were'} picked by hand for this lesson.`;
}
/** For a browse list: "Taught at 4 levels" in words, short. */
export function levelCount(mask) {
  const ranks = ranksOf(mask);
  return ranks.length === 1 ? `One level: ${LEVEL_SHORT[ranks[0]]}` : `${cap(numWord(ranks.length))} levels`;
}

/** Said once on an idea's page, about the ends of its ladder. '' when the ladder reaches the end. */
export function edgeLines(mask) {
  const ranks = ranksOf(mask);
  if (!ranks.length) return { below: '', above: '' };
  const lo = ranks[0], hi = ranks[ranks.length - 1];
  return {
    below: lo > 0 ? `Nothing simpler on the site yet. The first place it is taught is ${LEVEL_SHORT[lo]}.` : '',
    above: hi < 6 ? (ranks.length === 1 ? 'Nothing deeper on the site yet.' : `Nothing deeper on the site yet. The last place it is taught is ${LEVEL_SHORT[hi]}.`) : '',
  };
}

// ------------------------------------------------------------------ the short versions inside a lesson

/* Every lesson carries short explanations of itself at other levels (frontmatter explainLevels,
   written once, offline). Which one is "one level simpler" and "one level deeper" for a lesson at
   each level; the simpler one opens in place under the hop sentence. */
/* OFF: waits on Chris. When true, a short version that does not read at least two grades easier than
   its lesson is offered as "Short version" instead of under "Simpler" (src/lib/hop.ts passes
   quickNotSimpler to lessonSentence). On 2026-11-23 that was 337 of 349 lessons, so it is a
   site-wide wording change; the list is production/short-versions-not-simpler.json. */
export const RELABEL_NOT_SIMPLER = false;
export const QUICK_DOWN = [null, null, 'grade7', 'highschool', 'highschool', 'highschool', 'college'];
export const QUICK_UP = ['grade7', 'highschool', 'bio2', 'grad', 'grad', 'grad', null];
export const QUICK_NAME = {
  eli5: ['The plainest version', 'plain-words'],
  grade7: ['The grade 7 version', 'grade 7'],
  highschool: ['The high school version', 'high school'],
  bio2: ['Where Biology II takes it', 'Biology II'],
  college: ['The college version', 'college'],
  grad: ['The graduate version', 'graduate'],
};
export const readTime = (words) => { const m = Math.max(1, Math.round(words / 200)); return `about ${m} ${m === 1 ? 'minute' : 'minutes'} to read`; };

// ------------------------------------------------------------------ the hop sentence, as segments

/* A line is a list of segments so a page can draw links and a test can read plain text:
     { t }                 plain text
     { t, href }           a lesson link
     { t, quick }          the control that opens a short version in place (quick = its key)
     { t, k: 'dir' }       "Simpler:" / "Deeper:"
     { t, k: 'note' }      a bracketed level note
   The three lines are set as one short paragraph: at most four lines on a 390 px phone. */

/** The closed sentence may not run past this many characters (about four phone lines). */
export const SENTENCE_MAX = 210;

/**
 * The links a person chose by hand for a lesson, which the sentence uses before anything the
 * graph suggests: a school lesson's ladder (frontmatter `ladder`), an ages 5 to 10 guide's step up
 * (`activity.stepUp`), and for a college lesson the high school lessons that name it.
 * @param {string} slug
 * @param {Map<string, { title: string, rank: number, order?: number, ladder?: any, activity?: any }>} lessons live lessons
 * @returns {{ down: { slug: string, title: string, rank: number }[], up: { slug: string, title: string, rank: number }[] }}
 */
export function authoredLinks(slug, lessons) {
  const me = lessons.get(slug);
  if (!me) return { down: [], up: [] };
  const near = (slugs = []) => slugs.map((s) => (lessons.get(s) && s !== slug ? { slug: s, title: lessons.get(s).title, rank: lessons.get(s).rank } : null)).filter(Boolean);
  const lad = me.ladder ?? {};
  let down = near(lad.grade7).filter((x) => x.rank < me.rank);
  const up = [...near(me.activity?.stepUp), ...near(lad.biology), ...near(lad.college)].filter((x) => x.rank > me.rank);
  if (me.rank >= 3) {
    const back = [...lessons.entries()].filter(([, l]) => l.rank === 2 && (l.ladder?.college ?? []).includes(slug)).sort((a, b) => (a[1].order ?? 99) - (b[1].order ?? 99));
    down = [...down, ...back.map(([s, l]) => ({ slug: s, title: l.title, rank: l.rank }))];
  }
  return { down, up };
}

/**
 * @typedef {{ slug: string, title: string, rank: number }} Near
 */

/**
 * The hop sentence for one lesson. The page (src/lib/hop.ts) and scripts/test-hop.mjs both come
 * through here, so what is tested is what is shown.
 *
 * The sentence and the ladder that opens under it agree by construction:
 * - The idea named is the lesson's main idea: the first one in the graph's record for the lesson.
 * - Simpler and Deeper are the nearest rungs of that idea's own ladder.
 * - A link chosen by hand (authored) overrides the rung: among those at the nearest level, one
 *   that is on the ladder is preferred. One that is not on the ladder is returned in `also`, and
 *   the ladder draws it on its rung as "picked for this lesson".
 * - A lesson on another idea is never named here; its ladder is in the panel.
 * A side with no lesson is left out.
 *
 * @param {any[]} hops api.hops(slug): one entry per idea the lesson teaches, main idea first
 * @param {{ slug: string, title?: string, rank: number, courseTitle: string, explainLevels?: { level: string }[],
 *   authored?: { down: Near[], up: Near[] }, quickNotSimpler?: boolean }} lesson
 *   quickNotSimpler: the short version does not read at least two grades easier than the lesson
 *   (simplerCheck in src/lib/readability.ts). It is then offered as a "Short version", never under "Simpler".
 */
export function lessonSentence(hops, lesson) {
  const ideas = hops;
  const main = ideas[0];
  const key = QUICK_DOWN[lesson.rank];
  const quickDown = key && (lesson.explainLevels ?? []).some((x) => x.level === key) ? key : undefined;
  const authored = lesson.authored ?? { down: [], up: [] };
  const more = ideas.some((h) => h.down || h.up) || authored.down.length || authored.up.length ? 'See every level' : 'See nearby ideas';
  const href = (slug) => `/lessons/${slug}/?from=${lesson.slug}`;
  const dist = (r) => Math.abs(r.rank - lesson.rank);
  const also = [];

  const pick = (dir) => {
    if (!main) return null;
    const rungs = dir === 'down' ? main.downAll : main.upAll;
    const mine = authored[dir] ?? [];
    if (mine.length) {
      const nearest = Math.min(...mine.map(dist));
      const at = mine.filter((m) => dist(m) === nearest);
      const onLadder = at.find((m) => rungs.some((r) => r.slug === m.slug) || (dir === 'down' ? main.downAll : main.upAll).some((r) => r.slug === m.slug));
      const near = onLadder ?? at[0];
      if (!onLadder) also.push(near);
      return { near, byHand: true };
    }
    return main[dir] ? { near: main[dir], byHand: false } : null;
  };
  const down = pick('down');
  const up = pick('up');
  // Cut a long title at its subtitle, unless both sides would then read the same.
  const cut = (t) => t.split(/: | — /)[0];
  const sameCut = down && up && cut(down.near.title) === cut(up.near.title);

  const build = (tight) => {
    const name = (near) => ((tight >= 2 && !sameCut) || tight >= 6 ? cut(near.title) : near.title);
    const what = main ? inSentence(main.id, main.label ?? main.name) : '';
    const out = {};
    if (!main) return out;
    if (lesson.rank === 0) {
      out.teaches = [{ t: `An activity for ages 5 to 10 about ${what}.` }];
      // Only a school lesson is offered from a guide for young children.
      if (up && up.near.rank <= 2) out.next = [{ t: 'Next, for an older child:', k: 'dir' }, { t: ' ' }, { t: name(up.near), href: href(up.near.slug) }, { t: ' ' }, { t: `(${LEVEL_SHORT[up.near.rank]})`, k: 'note' }, { t: '.' }];
      return out;
    }
    // The level is never dropped; the course name goes first.
    out.teaches = [{ t: tight >= 4 ? `${cap(what)}, ${LEVEL_SHORT[lesson.rank].replace(/^a /, '')}${lesson.rank <= 2 ? ' level' : ''}.`
      : lesson.rank <= 2 ? `This lesson teaches ${what} at ${LEVEL_SHORT[lesson.rank]} level.`
      : tight >= 3 ? `This lesson teaches ${what} (${LEVEL_SHORT[lesson.rank]}).` : `This lesson teaches ${what} in ${lesson.courseTitle}, ${COURSE_KIND[lesson.rank]}.` }];
    const plainShort = Boolean(lesson.quickNotSimpler);
    const quick = !quickDown ? undefined
      : plainShort ? { t: tight >= 5 ? 'read it here' : `read the ${QUICK_NAME[quickDown][1]} version here`, quick: quickDown }
      : { t: tight >= 5 ? 'read a short version here' : `read a short ${QUICK_NAME[quickDown][1]} version here`, quick: quickDown };
    // A short version that is no easier to read than the lesson is short, not simpler: it gets its
    // own label, after the simpler lesson when there is one.
    const shortSegs = quick && plainShort ? [{ t: 'Short version:', k: 'dir', short: true }, { t: ' ' }, quick, { t: '.' }] : null;
    // A college reader whose only simpler lesson is an activity for young children gets the short
    // version here; the activity is on the ladder.
    if (down && !(down.near.rank === 0 && lesson.rank >= 3 && quick)) {
      const lvl = down.near.rank === 0 ? '(a hands-on activity)' : `(${LEVEL_SHORT[down.near.rank]})`;
      out.simpler = [{ t: 'Simpler:', k: 'dir' }, { t: ' ' }, { t: name(down.near), href: href(down.near.slug) }, { t: ' ' }, { t: lvl, k: 'note' }, ...(quick && !shortSegs ? [{ t: ', or ' }, quick] : []), { t: '.' }, ...(shortSegs ? [{ t: ' ' }, ...shortSegs] : [])];
    } else if (quick) {
      out.simpler = shortSegs ?? [{ t: 'Simpler:', k: 'dir' }, { t: ' ' }, quick, { t: '.' }];
    }
    if (up) {
      const step = !up.byHand && tight < 1 ? stepNote(lesson.rank, up.near.rank) : '';
      out.deeper = [{ t: 'Deeper:', k: 'dir' }, { t: ' ' }, { t: name(up.near), href: href(up.near.slug) }, { t: ' ' }, { t: `(${LEVEL_SHORT[up.near.rank]}${step ? (step.startsWith('a big') ? ', ' : '; ') + step : ''})`, k: 'note' }, { t: '.' }];
    }
    return out;
  };
  const length = (l) => ['teaches', 'simpler', 'deeper', 'next'].reduce((n, k) => n + (l[k] ? plain(l[k]).length + 1 : 0), 0);
  // Say less, in a fixed order, until the paragraph fits four phone lines: the step note, then the
  // subtitles of the lessons named, then the course's name, then "This lesson teaches", and last
  // the level word in "a short … version". The levels of the lessons and the short version stay.
  let lines = build(0), tight = 0;
  // (only if all that is not enough are two lessons with one main title both cut to it)
  while (tight < 6 && length(lines) > SENTENCE_MAX) lines = build(++tight);
  return { lines, more, quickDown, ideas, also, length: length(lines), tight };
}

export const plain = (segs) => (segs ?? []).map((s) => s.t).join('');

/** The one-line form for a film card or a search result: "Osmosis, high school. Also at: grade 7 and college core." */
export function compactLine({ name, mask, here }) {
  const ranks = ranksOf(mask);
  if (here === undefined || here === null) return `${name}. ${taughtAt(mask)}`;
  const others = ranks.filter((r) => r !== here);
  if (!others.length) return `${name}, ${LEVEL_SHORT[here]}: the only level so far.`;
  return `${name}, ${LEVEL_SHORT[here]}. Also at: ${andList(others.map((r) => LEVEL_SHORT[r]))}.`;
}
