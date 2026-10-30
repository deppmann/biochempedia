/* The per-course numbers shared by the homepage chooser and the /courses/ catalog.
   A course appears only once it has a published lesson. */
import { getCollection } from 'astro:content';
import { COURSE_ICONS } from '../data/course-icons';
import { COURSES, unitsFor, type Course } from '../data/courses';

export interface CourseCard {
  c: Course;
  lessons: number;
  units: number;
  films: number;
  sims: number;
  questions: number;
  icon: string;
  unitNames: string[];
}

export async function courseCards(): Promise<{ cards: CourseCard[]; lessonCount: number }> {
  const allLessons = (await getCollection('lessons')).filter((l) => !l.data.draft);
  // An empty catalog must never ship quietly. It happened once in development: a
  // stale content cache served lessons parsed before `course` existed, the course
  // filter matched nothing, and the page rendered with no chapters and no error.
  if (!allLessons.some((l) => l.data.course === 'biochemistry')) {
    throw new Error('Catalog: no biochemistry lessons found. If you just changed src/schema.ts, delete node_modules/.astro/data-store.json and rebuild.');
  }
  const cards = COURSES.map((c) => {
    const mine = allLessons.filter((l) => l.data.course === c.slug);
    const units = unitsFor(c, mine);
    return {
      c,
      lessons: mine.length,
      units: units.length,
      films: mine.reduce((n, l) => n + (l.data.explainer ? 1 : 0) + l.data.films.length, 0),
      sims: mine.reduce((n, l) => n + l.data.simulations.length, 0),
      questions: mine.reduce((n, l) => n + l.data.practiceQuestions.length + l.data.mcatQuestions.length, 0),
      /* A course's own icon if it has one, else its first lesson's icon. */
      icon: COURSE_ICONS[`course:${c.slug}`] ? `course:${c.slug}` : (units[0]?.entries[0]?.l.data.slug ?? c.slug),
      unitNames: units.map((u) => u.name),
    };
  }).filter((k) => k.lessons > 0);
  return { cards, lessonCount: allLessons.length };
}

export const plural = (n: number, one: string, many: string) => `${n} ${n === 1 ? one : many}`;
