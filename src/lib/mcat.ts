/* MCAT practice data, read at build time.

   Passage sets: src/content/mcat-sets/*.json, written to docs/expansion/mcat/RUBRIC.md and
   checked by scripts/validate-mcat.mjs (in the build), two blind solvers and a judge.
   Discrete items: the original MCAT-style questions already in the college lessons,
   grouped by topic. All originals; none comes from the AAMC or any prep company. */

import { getCollection } from 'astro:content';
import { courseOf } from '../data/courses';
import { LESSON_CATEGORY } from '../data/mcat-lesson-categories';

export interface McatFigure {
  id: string;
  type: 'table' | 'line' | 'bar' | 'scatter';
  caption: string;
  columns?: string[];
  rows?: (string | number)[][];
  xLabel?: string;
  yLabel?: string;
  xTicks?: string[];
  series?: { name: string; points: (number | null)[][]; error?: number[] }[];
}
export interface McatQuestion {
  id: string; stem: string; choices: string[]; answer: number; skill: 1 | 2 | 3 | 4;
  category: string; why: string[]; lesson: { slug: string; anchor?: string };
}
export interface McatSet {
  id: string; section: 'bb' | 'cp'; title: string; categories: string[];
  lessons: { slug: string; anchor?: string }[]; passage: string[]; figures?: McatFigure[];
  source: string; questions: McatQuestion[];
}

const files = import.meta.glob<{ default: McatSet }>('../content/mcat-sets/*.json', { eager: true });
export const SETS: McatSet[] = Object.values(files).map((m) => m.default).sort((a, b) => a.section.localeCompare(b.section) || a.categories[0].localeCompare(b.categories[0]) || a.title.localeCompare(b.title));

export const SECTION: Record<string, string> = {
  bb: 'Biological and Biochemical Foundations',
  cp: 'Chemical and Physical Foundations',
};

/* Short names for the AAMC content categories this site covers (paraphrased). */
export const CATEGORY: Record<string, string> = {
  '1A': 'Proteins and enzymes',
  '1B': 'Genetic information',
  '1C': 'Heredity and evolution',
  '1D': 'Bioenergetics and metabolism',
  '2A': 'Cells and membranes',
  '2B': 'Prokaryotes and viruses',
  '2C': 'Cell division and development',
  '3A': 'Nervous and endocrine systems',
  '3B': 'Organ systems',
  '5A': 'Water, acids and bases',
  '5C': 'Separation and purification',
  '5D': 'Biomolecule structure',
  '5E': 'Thermodynamics and kinetics',
  '6A': 'Sensation and perception',
};

export const SKILL: Record<number, string> = {
  1: 'Concepts',
  2: 'Reasoning',
  3: 'Research design',
  4: 'Data',
};

/* Topic for a discrete lesson question. Biochemistry, Genetics and Cell Biology are split by
   lesson; the other courses take one category each. */
const BIOCHEM_1D = new Set(['metabolism-basic-concepts', 'glycolysis', 'gluconeogenesis', 'pyruvate-dehydrogenase', 'citric-acid-cycle', 'oxidative-phosphorylation', 'proton-motive-force', 'light-reactions', 'calvin-cycle', 'pentose-phosphate-pathway', 'fatty-acid-degradation', 'fatty-acid-synthesis', 'lipid-synthesis', 'protein-turnover-amino-acid-catabolism', 'nucleotide-metabolism', 'integration-of-metabolism', 'digestion']);
const BIOCHEM_5D = new Set(['water-weak-bonds', 'amino-acids', 'carbohydrates', 'lipids']);
const BY_LESSON = new Set(['genetics', 'cell-biology']);
const BY_COURSE: Record<string, string> = {
  'ecology-evolution': '1C', 'organismal-biology': '3B', physiology: '3B',
  neuroscience: '3A', 'sensory-systems': '6A',
};

/* Graduate courses whose questions go past what the exam asks. They stay out of topic practice,
   the topic counts and the diagnostic unless the reader turns on "Beyond the exam" on
   /mcat/practice/. Sensory Systems stays in, as 6A. */
export const BEYOND_COURSES = ['signaling', 'developmental-neuroscience'];
export const BEYOND_LABEL = 'Beyond the exam';
export const beyondTopic = (course: string) => `beyond:${course}`;
export const isBeyond = (course: string) => BEYOND_COURSES.includes(course);

export function topicFor(course: string, slug: string): string {
  if (isBeyond(course)) return beyondTopic(course);
  if (course === 'biochemistry') return BIOCHEM_1D.has(slug) ? '1D' : BIOCHEM_5D.has(slug) ? '5D' : '1A';
  if (BY_LESSON.has(course)) {
    const t = LESSON_CATEGORY[slug];
    // A new Genetics or Cell Biology lesson fails the build until someone reads it and adds it to the map.
    if (!t || !CATEGORY[t]) throw new Error(`MCAT: lesson "${slug}" (${course}) has no content category in src/data/mcat-lesson-categories.ts.`);
    return t;
  }
  return BY_COURSE[course] ?? '1A';
}

export interface Discrete { slug: string; lessonTitle: string; course: string; topic: string; beyond: boolean; stem: string; choices: string[]; answer: number; rationale: string; idx: number }

/** Every MCAT-style question in published college lessons, with the graduate courses flagged `beyond`. */
export async function discreteItems(): Promise<Discrete[]> {
  const lessons = await getCollection('lessons', ({ data }) => !data.draft && courseOf(data.course).tier !== 'highschool' && courseOf(data.course).tier !== 'families');
  return lessons.flatMap((l) => l.data.mcatQuestions.map((q, i) => ({
    slug: l.data.slug, lessonTitle: l.data.title, course: l.data.course, topic: topicFor(l.data.course, l.data.slug), beyond: isBeyond(l.data.course),
    stem: q.stem, choices: q.choices, answer: q.answer, rationale: q.rationale, idx: i,
  })));
}

/** The questions that count as MCAT practice: everything except the graduate courses. */
export async function examItems(): Promise<Discrete[]> {
  return (await discreteItems()).filter((d) => !d.beyond);
}

/** The diagnostic: how many questions it draws from each topic. Its length is the sum. */
export const DIAGNOSTIC_PLAN: [string, number][] = [['1A', 3], ['1D', 3], ['5D', 2], ['2A', 3], ['1B', 2], ['1C', 2], ['3A', 3], ['3B', 2]];
export const DIAGNOSTIC_LENGTH = DIAGNOSTIC_PLAN.reduce((n, [, k]) => n + k, 0);

/** The length cue (correct choice the longest) makes an item easier than intended; the diagnostic avoids those. */
export const cueFree = (d: { choices: string[]; answer: number }) => {
  const L = d.choices.map((c) => c.length);
  return L[d.answer] < Math.max(...L.filter((_, i) => i !== d.answer));
};
