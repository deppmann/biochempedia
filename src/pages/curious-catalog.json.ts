import { getCollection } from 'astro:content';
import { COURSES } from '../data/courses';

/**
 * The curiosity router's catalog: one compact record per published lesson
 * (slug, course, title, hook), plus each course's level. Built with the site and
 * read by the Worker (worker/curious.js) through the ASSETS binding, which turns
 * it into the cached system-prompt block and also uses it to check every slug the
 * model returns. It is public like the rest of the site (the same facts are in
 * /search-index.json), and it contains nothing about visitors.
 *
 * The order is fixed (course order, then lesson order, then slug) and nothing in
 * it changes between builds unless a lesson does, so the prompt built from it is
 * byte-identical from request to request, which is what prompt caching needs.
 */
const LEVEL: Record<string, string> = {
  families: 'ages 5-10, hands-on, for a parent or teacher',
  highschool: 'grades 7-12',
  foundation: 'first-year college',
  core: 'core upper-level college',
  elective: 'upper-level elective',
  advanced: 'advanced, research-based',
};

/** One line, no pipes (the Worker's separator), trimmed at a word near `max` characters. */
const tidy = (s: string, max: number) => {
  const one = s.replace(/\s+/g, ' ').replace(/\|/g, '/').trim();
  if (one.length <= max) return one;
  const cut = one.slice(0, max);
  return cut.slice(0, Math.max(cut.lastIndexOf(' '), max - 20)).replace(/[ ,;:.\-–—]+$/, '') + '…';
};

export async function GET(): Promise<Response> {
  const lessons = await getCollection('lessons', ({ data }) => import.meta.env.DEV || !data.draft);
  const courses: { s: string; t: string; level: string; mcat: boolean }[] = [];
  const records: [string, string, string, string][] = [];
  for (const course of COURSES) {
    const mine = lessons
      .filter((l) => l.data.course === course.slug)
      .sort((a, b) => (a.data.order ?? 999) - (b.data.order ?? 999) || a.data.slug.localeCompare(b.data.slug));
    if (!mine.length) continue;
    courses.push({ s: course.slug, t: course.title, level: LEVEL[course.tier] ?? course.tier, mcat: !!course.mcat });
    for (const l of mine) {
      const d = l.data;
      const hook = d.hook ?? d.summary.split(/(?<=[.?!])\s+/)[0];
      records.push([d.slug, course.slug, tidy(d.title, 90), tidy(hook, 150)]);
    }
  }
  return new Response(JSON.stringify({ courses, lessons: records }), {
    headers: { 'Content-Type': 'application/json; charset=utf-8' },
  });
}
