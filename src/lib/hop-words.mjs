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

/* The graph's names are written as headings ("Cells, the unit of life", "Nerve signals (the action
   potential)"). Inside a sentence the bracket and the gloss go, and the first letter drops unless
   the word is a name or an abbreviation. A few names are clauses and take their bracketed term, or
   a wording of their own. */
const IN_SENTENCE = {
  'perturbation-and-rescue': 'rescue experiments',
  'retinal-degeneration': 'retinal degeneration',
  'temporal-identity': 'how birth time sets a neuron’s identity',
  'needed-versus-enough': 'necessity and sufficiency',
  'fasting-and-starvation': 'the fed, fasting and starving states',
  'experimental-unit': 'the experimental unit',
  'hemispheric-lateralization': 'which hemisphere speaks',
  'corticospinal-tract': 'the corticospinal tract',
  'characteristics-of-life': 'what makes something alive',
  'sleep-stages': 'sleep stages',
  'signal-shape': 'the shape of a signal',
  'localization-of-function': 'localization of function',
  'lateral-inhibition': 'lateral inhibition',
  'imperfect-detection': 'imperfect detection',
  'electrochemical-gradient': 'the electrochemical gradient',
  'plant-life-cycle': 'the plant life cycle',
  'germ-theory': 'the germ theory of disease',
  'neuronal-polarity': 'neuronal polarity',
  'gene-to-protein': 'how a gene becomes a protein',
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
export const SENTENCE_MAX = 215;

/**
 * The links a person chose by hand for a lesson, which the sentence uses before anything the
 * graph suggests: a school lesson's ladder (frontmatter `ladder`), an ages 5 to 10 guide's step up
 * (`activity.stepUp`), and for a college lesson the high school lessons that name it.
 * @param {string} slug
 * @param {Map<string, { title: string, rank: number, order?: number, ladder?: any, activity?: any }>} lessons live lessons
 * @returns {{ down: Near[], up: Near[] }}  Near = { slug, title, rank }
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
 * The ideas a lesson teaches, main idea first. The rule: the idea named in the lesson's own title
 * (by the share of the idea's words found there); when the title names none, or two equally, the
 * idea whose section of the lesson is the longest (the graph names the section that teaches each
 * idea; `sections` gives each section's length in words); then the graph's own order.
 */
export function orderIdeas(hops, lesson = {}) {
  const t = ` ${String(lesson.title ?? '').toLowerCase().replace(/[^a-z0-9]+/g, ' ')} `;
  const words = (name) => inSentence('', name).toLowerCase().replace(/[^a-z0-9]+/g, ' ').split(' ').filter((w) => w.length > 3 && !/^(what|that|with|from|their|into|your|this|have|make|makes|does)$/.test(w));
  const inTitle = (h) => { const w = words(h.name); return w.length ? w.filter((x) => t.includes(` ${x}`) || t.includes(` ${x.replace(/s$/, '')}`)).length / w.length : 0; };
  const size = (h) => (h.anchor && lesson.sections ? lesson.sections[h.anchor] ?? 0 : 0);
  return hops.map((h, i) => ({ h, i, size: size(h), title: inTitle(h) })).sort((a, b) => b.title - a.title || b.size - a.size || a.i - b.i).map((x) => x.h);
}

/**
 * The hop sentence for one lesson. The page (src/lib/hop.ts) and scripts/test-hop.mjs both come
 * through here, so what is tested is what is shown.
 *
 * Which lesson a side names, in order: a link chosen by hand (authored), nearest level first;
 * otherwise, across the ideas the lesson teaches, the lesson nearest in level, the main idea
 * winning a tie. When that lesson is on another idea than the one named, the line says which.
 * A side with no lesson is left out.
 *
 * @param {any[]} hops api.hops(slug): one entry per idea the lesson teaches
 * @param {{ slug: string, title?: string, rank: number, courseTitle: string, explainLevels?: { level: string }[],
 *   sections?: Record<string, number>, authored?: { down: Near[], up: Near[] } }} lesson
 */
export function lessonSentence(hops, lesson) {
  const ideas = orderIdeas(hops, lesson);
  const key = QUICK_DOWN[lesson.rank];
  const quickDown = key && (lesson.explainLevels ?? []).some((x) => x.level === key) ? key : undefined;
  const authored = lesson.authored ?? { down: [], up: [] };
  const more = ideas.some((h) => h.down || h.up) || authored.down.length || authored.up.length ? 'See every level' : 'See nearby ideas';
  const href = (slug) => `/lessons/${slug}/?from=${lesson.slug}`;
  // A long lesson title gives up its subtitle before the sentence gives up anything else of use.
  const name = (near, tight) => (tight >= 4 ? near.title.split(/: | \u2014 /)[0] : near.title);
  const dist = (r) => Math.abs(r.rank - lesson.rank);

  const pick = (dir) => {
    const mine = authored[dir] ?? [];
    if (mine.length) return { near: mine.slice().sort((a, b) => dist(a) - dist(b))[0], tag: '', byHand: true };
    let best = null;
    ideas.forEach((h, i) => { if (h[dir] && (!best || dist(h[dir]) < dist(best.near))) best = { near: h[dir], tag: i > 0 ? inSentence(h.id, h.name) : '', byHand: false }; });
    return best;
  };
  const dirSeg = (word, p) => ({ t: p.tag ? `${word}, for ${p.tag}:` : `${word}:`, k: 'dir' });

  const build = (tight) => {
    const main = ideas.length ? inSentence(ideas[0].id, ideas[0].name) : '';
    const out = {};
    if (!ideas.length) return out;
    if (lesson.rank === 0) {
      out.teaches = [{ t: `This activity is about ${main} for ages 5 to 10.` }];
      const up = pick('up');
      // Only a school lesson is offered from a guide for young children.
      if (up && up.near.rank <= 2) out.next = [{ t: 'Next, for an older child:', k: 'dir' }, { t: ' ' }, { t: name(up.near, tight), href: href(up.near.slug) }, { t: ' ' }, { t: `(${LEVEL_SHORT[up.near.rank]})`, k: 'note' }, { t: '.' }];
      return out;
    }
    out.teaches = [{ t: lesson.rank <= 2 ? `This lesson teaches ${main} at ${LEVEL_SHORT[lesson.rank]} level.` : (tight >= 5 ? `This lesson teaches ${main}.` : `This lesson teaches ${main} in ${lesson.courseTitle}${tight >= 2 ? '' : `, ${COURSE_KIND[lesson.rank]}`}.`) }];
    const quick = quickDown ? { t: tight >= 3 ? 'read a short version here' : `read a short ${QUICK_NAME[quickDown][1]} version here`, quick: quickDown } : undefined;
    const down = pick('down');
    // A college reader whose only simpler lesson is an activity for young children gets the short
    // version here; the activity is on the ladder.
    if (down && !(down.near.rank === 0 && lesson.rank >= 3 && quick)) {
      const lvl = down.near.rank === 0 ? '(a hands-on activity)' : `(${LEVEL_SHORT[down.near.rank]})`;
      out.simpler = [dirSeg('Simpler', down), { t: ' ' }, { t: name(down.near, tight), href: href(down.near.slug) }, ...(tight < 7 ? [{ t: ' ' }, { t: lvl, k: 'note' }] : []), ...(quick && tight < 6 ? [{ t: ', or ' }, quick] : []), { t: '.' }];
    } else if (quick) {
      out.simpler = [{ t: 'Simpler:', k: 'dir' }, { t: ' ' }, quick, { t: '.' }];
    }
    const up = pick('up');
    if (up) {
      // The size of the step is said only for a lesson the graph chose, and only when it is true
      // of the whole lesson (the nearest lesson on any of its ideas).
      const step = !up.byHand && tight < 1 ? stepNote(lesson.rank, up.near.rank) : '';
      out.deeper = [dirSeg('Deeper', up), { t: ' ' }, { t: name(up.near, tight), href: href(up.near.slug) }, ...(tight < 7 ? [{ t: ' ' }, { t: `(${LEVEL_SHORT[up.near.rank]}${step ? (step.startsWith('a big') ? ', ' : '; ') + step : ''})`, k: 'note' }] : []), { t: '.' }];
    }
    return out;
  };
  const length = (l) => ['teaches', 'simpler', 'deeper', 'next'].reduce((n, k) => n + (l[k] ? plain(l[k]).length + 1 : 0), 0);
  // Say less, in a fixed order, until the paragraph fits four phone lines: the step note goes
  // first, then the kind of course, the level word in "a short … version", the subtitles of the
  // lessons named, the course, and last the short version's own control (it is then listed with
  // the other short versions when the levels are opened).
  let lines = build(0), tight = 0;
  // (after those: the short version's own control, which is then listed with the other short
  // versions when the levels are opened, and last the levels in brackets)
  while (tight < 7 && length(lines) > SENTENCE_MAX) lines = build(++tight);
  const quickInSentence = ['simpler'].some((k) => (lines[k] ?? []).some((x) => x.quick));
  return { lines, more, quickDown: quickInSentence ? quickDown : undefined, ideas, length: length(lines), tight };
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
