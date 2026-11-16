/* The subjects STEMhop is meant to cover (2026-11-15, the homepage's "Pick a subject").
   Biology is the only one with lessons; its numbers on the homepage are counted from the lessons,
   never typed here. A coming subject is a name and a line, shown as "Coming" and never as a link,
   until it has a course. When one opens, give it `live: true` and a page, and the homepage tile
   follows. */

export interface Subject {
  key: string;
  name: string;
  live: boolean;
  /** For a coming subject: what to use until it exists. Plain text; `link` is added after it. */
  note?: string;
  link?: { before: string; text: string; href: string; after: string };
}

export const SUBJECTS: Subject[] = [
  { key: 'biology', name: 'Biology', live: true },
  { key: 'chemistry', name: 'Chemistry', live: false, note: 'Not built yet. Until then, Biochemistry is under Biology.' },
  { key: 'physics', name: 'Physics', live: false, note: 'Not built yet.' },
  {
    key: 'mathematics',
    name: 'Mathematics and statistics',
    live: false,
    note: 'Not built yet.',
    link: { before: 'The ', text: 'math toolkit', href: '/math-toolkit', after: ' covers the math inside the biology lessons.' },
  },
  { key: 'psychology', name: 'Psychology and sociology', live: false, note: 'Not built yet. Brain and behaviour start in Neuroscience, under Biology.' },
];

export const COMING_SUBJECTS = SUBJECTS.filter((s) => !s.live);
