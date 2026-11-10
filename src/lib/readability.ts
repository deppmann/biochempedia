/* Reading grade of a lesson, worked out from its text when the site is built.

   The formula is the Flesch-Kincaid grade level:
     0.39 × (words ÷ sentences) + 11.8 × (syllables ÷ words) − 15.59
   It measures sentence length and word length only. It knows nothing about how hard the
   ideas are, so the Teachers page says so under the table that shows these numbers.

   What is counted is the running prose of the lesson body. Left out: frontmatter (Astro has
   already removed it), imports, MDX comments, components and their props, Equation Cards with
   everything inside them, code, equations, tables, headings, images and link addresses.
   Numbers are not counted as words. A hyphenated compound is one word, as in Kincaid's
   original counting rules. An all-capitals abbreviation (ATP, DNA) is read letter by letter,
   so it counts one syllable per letter. */

/** Tags that sit inside a sentence; every other tag ends the text block it is in. */
const INLINE_TAGS = new Set(['sub', 'sup', 'strong', 'em', 'b', 'i', 'a', 'span', 'abbr', 'code', 'mark', 'u', 'small']);
/** Components whose whole contents are left out, not just the tag. */
const DROP_BLOCKS = new Set(['EquationCard', 'script', 'style', 'svg', 'table']);

/** Index just past the `>` that closes the tag starting at `i`, or -1. Skips quoted strings and {braces}. */
function tagEnd(s: string, i: number): number {
  let depth = 0;
  let quote = '';
  for (let j = i + 1; j < s.length; j++) {
    const ch = s[j];
    if (quote) {
      if (ch === '\\') j++;
      else if (ch === quote) quote = '';
    } else if (ch === '"' || ch === "'" || ch === '`') quote = ch;
    else if (ch === '{') depth++;
    else if (ch === '}') depth--;
    else if (ch === '>' && depth <= 0) return j + 1;
  }
  return -1;
}

/** Remove JSX and HTML tags, keeping the text between them (except inside DROP_BLOCKS). */
function stripTags(s: string): string {
  let out = '';
  let i = 0;
  while (i < s.length) {
    const lt = s.indexOf('<', i);
    if (lt === -1) { out += s.slice(i); break; }
    out += s.slice(i, lt);
    const m = /^<\/?([A-Za-z][A-Za-z0-9.]*)/.exec(s.slice(lt, lt + 60));
    const end = m ? tagEnd(s, lt) : -1;
    if (!m || end === -1) { out += '<'; i = lt + 1; continue; } // a bare "<", as in "pH < 7"
    const name = m[1];
    const opening = s[lt + 1] !== '/' && s[end - 2] !== '/';
    i = end;
    if (opening && DROP_BLOCKS.has(name)) {
      const close = s.indexOf(`</${name}>`, end);
      if (close !== -1) i = close + name.length + 3;
    }
    out += INLINE_TAGS.has(name) ? '' : '\n\n';
  }
  return out;
}

/** The lesson body as plain prose: one sentence-bearing unit (paragraph or list item) per line. */
export function proseLines(mdx: string): string[] {
  let s = mdx
    .replace(/\r\n?/g, '\n')
    .replace(/\{\/\*[\s\S]*?\*\/\}/g, ' ') // MDX comments
    .replace(/^(?:`{3,}|~{3,})[\s\S]*?^(?:`{3,}|~{3,})[^\n]*$/gm, ' ') // fenced code
    .replace(/^(?:import|export)\s.*$/gm, ' ');
  s = stripTags(s);
  for (let prev = ''; prev !== s; ) { prev = s; s = s.replace(/\{[^{}]*\}/g, ' '); } // {expressions}
  s = s
    .replace(/\$\$[\s\S]*?\$\$/g, ' ') // display equations
    .replace(/\$[^\s$][^$\n]*[\\^_][^$\n]*\$/g, ' ') // inline TeX (has a \, ^ or _), not prices
    .replace(/`[^`\n]*`/g, ' ') // inline code
    .replace(/!\[[^\]]*\]\([^)]*\)/g, ' ') // images
    .replace(/\[\^[^\]]*\]:?/g, ' ') // footnote marks
    .replace(/\[([^\]]*)\]\([^)]*\)/g, '$1') // links keep their words
    .replace(/https?:\/\/\S+/g, ' ')
    .replace(/&nbsp;|&thinsp;|&ensp;|&emsp;/g, ' ')
    .replace(/&[a-z]+;|&#\d+;/gi, ' ');

  const lines: string[] = [];
  let open = false; // true while the last line can still take a continuation line
  for (const raw of s.split('\n')) {
    let line = raw.trim();
    if (!line) { open = false; continue; }
    if (/^#{1,6}\s/.test(line) || /^\|/.test(line) || /^(?:[-*_]\s*){3,}$/.test(line)) { open = false; continue; } // heading, table row, rule
    const starts = /^(?:>\s*)*(?:[-*+]\s+|\d+[.)]\s+)/.test(line) || /^>/.test(line);
    line = line.replace(/^(?:>\s*)+/, '').replace(/^(?:[-*+]\s+|\d+[.)]\s+)/, '').replace(/^\[[ xX]\]\s+/, '');
    line = line.replace(/\*\*|__|\*|(?<![A-Za-z0-9])_|_(?![A-Za-z0-9])/g, '').trim();
    if (!line) continue;
    if (open && !starts) lines[lines.length - 1] += ' ' + line;
    else lines.push(line);
    open = true;
  }
  return lines;
}

const ABBREVIATIONS = /\b(?:e\.g|i\.e|et al|etc|vs|cf|ca|approx|Fig|Figs|Eq|Dr|Mr|Mrs|Ms|Prof|St|No|vol|pp|sp|spp|U\.S|U\.K)\./g;

function sentenceCount(line: string): number {
  const t = line
    .replace(ABBREVIATIONS, (m) => m.replace(/\./g, ''))
    .replace(/\b([A-Z])\.(?=\s+[A-Z])/g, '$1'); // initials: "J. B. S. Haldane"
  // A full stop, question mark or exclamation mark, then any closing quotes or brackets, then a space.
  const ends = (t.match(/[.!?]+["'’”)\]]*\s+(?=\S)/g) ?? []).length;
  return ends + 1; // the last sentence, whether or not it has a full stop
}

export function syllables(word: string): number {
  let n = 0;
  for (const part of word.split('-')) {
    const letters = part.replace(/[^A-Za-z]/g, '');
    if (!letters) continue;
    if (letters.length >= 2 && letters === letters.toUpperCase()) { n += letters.length; continue; } // ATP, DNA
    let w = letters.toLowerCase();
    if (w.length <= 3) { n += 1; continue; }
    w = w.replace(/(?:[^laeiouy]es|[^laeiouy]ed|[^laeiouy]e)$/, '').replace(/^y/, '');
    n += Math.max(1, (w.match(/[aeiouy]{1,2}/g) ?? []).length);
  }
  return Math.max(1, n);
}

export interface TextCounts { words: number; sentences: number; syllables: number }

export function textCounts(mdx: string): TextCounts {
  const c = { words: 0, sentences: 0, syllables: 0 };
  for (const line of proseLines(mdx)) {
    // A word starts with a letter; numbers and symbols on their own are not counted.
    const words = line.match(/[A-Za-z][A-Za-z'’-]*/g) ?? [];
    if (!words.length) continue;
    c.words += words.length;
    c.sentences += sentenceCount(line);
    for (const w of words) c.syllables += syllables(w.replace(/['’]s?$/, ''));
  }
  return c;
}

/** Flesch-Kincaid grade level, or undefined when there is too little text to measure. */
export function fleschKincaidGrade(mdx: string, minWords = 150): number | undefined {
  const c = textCounts(mdx);
  if (c.words < minWords || !c.sentences) return undefined;
  return 0.39 * (c.words / c.sentences) + 11.8 * (c.syllables / c.words) - 15.59;
}

function quantile(sorted: number[], q: number): number {
  const pos = (sorted.length - 1) * q;
  const lo = Math.floor(pos);
  const hi = Math.ceil(pos);
  return sorted[lo] + (sorted[hi] - sorted[lo]) * (pos - lo);
}

export interface ReadingRange {
  /** 25th percentile of the lessons' grades. */
  low: number;
  /** 75th percentile. */
  high: number;
  median: number;
  /** Lessons measured. */
  lessons: number;
}

/** The middle half of a course's lessons by reading grade: 25th to 75th percentile. */
export function readingRange(bodies: (string | undefined)[]): ReadingRange | undefined {
  const grades = bodies
    .map((b) => (b ? fleschKincaidGrade(b) : undefined))
    .filter((g): g is number => g !== undefined)
    .sort((a, b) => a - b);
  if (!grades.length) return undefined;
  return { low: quantile(grades, 0.25), high: quantile(grades, 0.75), median: quantile(grades, 0.5), lessons: grades.length };
}
