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

/** The ideas a lesson teaches, as the sentence names them: two at most, then "and one more idea".
 *  A name with "and" inside it ("pH and buffers") gets a clearer join. */
export function ideaList(ideas) {
  // A name with a comma inside it ("cells, tissues, organs and organ systems") cannot share a list.
  const shown = ideas.slice(0, 2).some((x) => x.includes(',')) ? ideas.slice(0, 1) : ideas.slice(0, 2);
  const rest = ideas.length - shown.length;
  const inner = shown.some((x) => / and /.test(x));
  if (rest > 0) return `${shown.join(', ')}${shown.length > 1 || inner || shown[0].includes(',') ? ',' : ''} and ${numWord(rest)} more ${rest === 1 ? 'idea' : 'ideas'}`;
  if (shown.length === 2) return inner ? `${shown[0]}, and also ${shown[1]}` : `${shown[0]} and ${shown[1]}`;
  return shown.join('');
}

/** The first line of the hop sentence. `ideas` are in-sentence names, main idea first. */
export function teachesLine({ rank, courseTitle, ideas }) {
  const what = ideaList(ideas);
  if (rank === 0) return `This activity is about ${what} for ages 5 to 10.`;
  if (rank <= 2) return `This lesson teaches ${what} at ${LEVEL_SHORT[rank]} level.`;
  return `This lesson teaches ${what} in ${courseTitle}, ${COURSE_KIND[rank]}.`;
}

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
     { t, k: 'note' }      a bracketed level note */

/**
 * @param {{ rank: number, courseTitle: string, slug: string,
 *   ideas: { short: string, down?: Near, up?: Near, downMore?: number, upMore?: number }[],
 *   quickDown?: string, more: 'See every level' | 'See nearby ideas' }} l
 *   Near = { title, href, rank }
 * @returns {{ teaches: Seg[], simpler?: Seg[], deeper?: Seg[], next?: Seg[] }}
 */
export function hopSentence(l) {
  const names = l.ideas.map((i) => i.short);
  const out = { teaches: [{ t: teachesLine({ rank: l.rank, courseTitle: l.courseTitle, ideas: names }) }] };
  if (!l.ideas.length) return out;

  // One lesson a side: the main idea's neighbour, or the first idea that has one.
  const pick = (dir) => {
    const i = l.ideas.findIndex((x) => x[dir]);
    if (i < 0) return undefined;
    return { near: l.ideas[i][dir], tag: i > 0 && l.ideas.length > 1 ? l.ideas[i].short : '' };
  };
  const note = (p) => {
    let n = levelNote(l.rank, p.near.rank);
    if (p.tag) n = `${n.slice(0, -1)}, for ${p.tag})`;
    return n;
  };
  // Other lessons on that side are one tap away under "See every level"; the sentence names one.
  const more = () => [];

  // Ages 5 to 10: the page is for a grown-up running an activity. Only a school lesson is offered.
  if (l.rank === 0) {
    const up = pick('up');
    if (up && up.near.rank <= 2) out.next = [{ t: 'Next, for an older child:', k: 'dir' }, { t: ' ' }, { t: up.near.title, href: up.near.href }, { t: ' ' }, { t: `(${LEVEL_SHORT[up.near.rank]})`, k: 'note' }, { t: '.' }];
    return out;
  }

  const down = pick('down');
  const quick = l.quickDown ? { t: `read a short ${QUICK_NAME[l.quickDown][1]} version here`, quick: l.quickDown } : undefined;
  // A college reader whose only simpler lesson is an activity for young children gets the short
  // version here; the activity is on the ladder under "See every level".
  const showDown = down && !(down.near.rank === 0 && l.rank >= 3 && quick);
  if (showDown) {
    const lead = down.near.rank === 0 ? [{ t: 'a hands-on activity for ages 5 to 10, ' }, { t: down.near.title, href: down.near.href }, ...(stepNote(l.rank, 0) ? [{ t: ' ' }, { t: `(${stepNote(l.rank, 0)})`, k: 'note' }] : [])]
      : [{ t: down.near.title, href: down.near.href }, { t: ' ' }, { t: note(down), k: 'note' }];
    out.simpler = [{ t: 'Simpler:', k: 'dir' }, { t: ' ' }, ...lead, ...more(down), ...(quick ? [{ t: ', or ' }, quick] : []), { t: '.' }];
  } else if (quick) {
    out.simpler = [{ t: 'Simpler:', k: 'dir' }, { t: ' ' }, quick, { t: '.' }];
  }
  const up = pick('up');
  if (up) out.deeper = [{ t: 'Deeper:', k: 'dir' }, { t: ' ' }, { t: up.near.title, href: up.near.href }, { t: ' ' }, { t: note(up), k: 'note' }, ...more(up), { t: '.' }];
  return out;
}

/**
 * The ideas a lesson teaches, main idea first. The graph lists them in no order of importance, so:
 * an idea named in the lesson's own title comes first, then the idea taught at the most levels
 * (the one with somewhere to hop to).
 */
export function orderIdeas(hops, title) {
  const t = ` ${String(title).toLowerCase().replace(/[^a-z0-9]+/g, ' ')} `;
  const words = (name) => inSentence('', name).toLowerCase().replace(/[^a-z0-9]+/g, ' ').split(' ').filter((w) => w.length > 3 && !/^(what|that|with|from|their|into|your|this|have|make|makes|does)$/.test(w));
  const score = (h) => {
    const w = words(h.name);
    const inTitle = w.length ? w.filter((x) => t.includes(` ${x}`) || t.includes(` ${x.replace(/s$/, '')}`)).length / w.length : 0;
    const levels = (h.down ? 1 : 0) + (h.up ? 1 : 0);
    return inTitle * 10 + levels;
  };
  return hops.map((h, i) => ({ h, i, s: score(h) })).sort((a, b) => b.s - a.s || a.i - b.i).map((x) => x.h);
}

/**
 * The hop sentence for one lesson, straight from the graph's hops(slug). The page (src/lib/hop.ts)
 * and scripts/test-hop.mjs both come through here, so what is tested is what is shown.
 * @param {any[]} hops api.hops(slug): one entry per idea the lesson teaches
 * @param {{ slug: string, title?: string, rank: number, courseTitle: string, explainLevels?: { level: string }[] }} lesson
 */
export function lessonSentence(hops, lesson) {
  const key = QUICK_DOWN[lesson.rank];
  const quickDown = key && (lesson.explainLevels ?? []).some((x) => x.level === key) ? key : undefined;
  const oneLevel = hops.length > 0 && hops.every((h) => !h.down && !h.up);
  const more = oneLevel ? 'See nearby ideas' : 'See every level';
  hops = orderIdeas(hops, lesson.title ?? '');
  const to = (r) => ({ title: r.title, href: `/lessons/${r.slug}/?from=${lesson.slug}`, rank: r.rank });
  const lines = hopSentence({
    rank: lesson.rank, courseTitle: lesson.courseTitle, slug: lesson.slug, more, quickDown,
    ideas: hops.map((h) => ({
      short: inSentence(h.id, h.name),
      ...(h.down ? { down: to(h.down), downMore: h.downAll.length - 1 } : {}),
      ...(h.up ? { up: to(h.up), upMore: h.upAll.length - 1 } : {}),
    })),
  });
  return { lines, more, quickDown };
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
