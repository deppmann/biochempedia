import { getCollection } from 'astro:content';
import { COURSES } from '../data/courses';
import { STAGES, stageOf } from '../data/stages';
import { filmCatalog, filmKey } from '../lib/film-catalog';

/**
 * The names the usage counts are checked against: every level, course, published lesson and
 * film on the site, by the key each is counted under. Built with the site.
 *
 * Two readers, both through the same file so they cannot drift apart:
 *   - the Worker (worker/film-count.js and worker/admin.js, through the ASSETS binding) uses it
 *     as an allow-list. A film count is kept only for a film key listed here, and the owner's
 *     totals only ever name a course or lesson listed here, so text somebody typed can never
 *     reach the table or the totals page by posing as a key.
 *   - the totals page (/admin/) uses it to show titles beside the keys.
 *
 * It is public like the rest of the catalog (the same facts are in /films.json and
 * /catalog.json) and holds nothing about visitors.
 *
 *   levels   [[stage key, title], ...] in ladder order
 *   courses  { slug: [title, stage key] }
 *   lessons  { slug: [title, course slug] }
 *   films    { film key: [title, course slug or "" for a methods-library film] }
 */
export async function GET(): Promise<Response> {
  const lessons = await getCollection('lessons', ({ data }) => !data.draft);
  const films = await filmCatalog();
  const live = new Set<string>(lessons.map((l) => l.data.course));
  const courses: Record<string, [string, string]> = {};
  for (const c of COURSES) if (live.has(c.slug)) courses[c.slug] = [c.title, stageOf(c)];
  const lessonMap: Record<string, [string, string]> = {};
  for (const l of [...lessons].sort((a, b) => a.data.slug.localeCompare(b.data.slug))) {
    if (courses[l.data.course]) lessonMap[l.data.slug] = [l.data.title, l.data.course];
  }
  const filmMap: Record<string, [string, string]> = {};
  for (const f of films) filmMap[filmKey(f.src)] = [f.title, f.course ?? ''];
  const used = new Set(Object.values(courses).map(([, stage]) => stage));
  const levels = STAGES.filter((s) => used.has(s.key)).map((s) => [s.key, s.title]);
  return new Response(JSON.stringify({ levels, courses, lessons: lessonMap, films: filmMap }), {
    headers: { 'Content-Type': 'application/json; charset=utf-8' },
  });
}
