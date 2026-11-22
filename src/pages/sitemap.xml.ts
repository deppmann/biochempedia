import type { APIContext } from 'astro';
import { PATHS } from '../data/paths';
import { getCollection } from 'astro:content';
import { METHODS } from '../data/methods';
import { SETS as MCAT_SETS } from '../lib/mcat';
import { allFilms } from '../lib/films';
import { SITE_ORIGIN } from '../lib/site-host.mjs';
import { allIdeas } from '../lib/hop';
import { learnerCourses } from '../lib/calendar/data';

/**
 * Hand-rolled sitemap (no @astrojs/sitemap — Astro deps are pinned). Lists the
 * static pages plus every non-draft lesson, using the canonical `site` from
 * astro.config.mjs. Prerendered to /sitemap.xml at build time.
 */
export async function GET(context: APIContext): Promise<Response> {
  const base = (context.site?.href ?? SITE_ORIGIN).replace(/\/$/, '');
  const lessons = (await getCollection('lessons')).filter((l) => !l.data.draft);
  // A course page exists only once the course has a published lesson.
  const courses = [...new Set(lessons.map((l) => l.data.course))];
  const paths = [
    '/', '/courses/', '/about/', '/updates/', '/fun/', '/play/', '/contact/', '/search/', '/license/', '/under-review/',
    '/math-toolkit/', '/privacy/', '/hex/', '/contributors/',
    '/teachers/', '/teachers/talk-notes/', '/teachers/demo/', '/teachers/how-its-built/',
    '/teachers/do-it-yourself/', '/teachers/checklist/', '/teachers/sources/', '/teachers/talk/',
    '/teachers/life-science/', '/teachers/biology/',
    '/teach/', '/teach/privacy/', '/join/',
    '/mcat/', '/mcat/diagnostic/', '/mcat/practice/', ...MCAT_SETS.map((s) => `/mcat/${s.id}/`),
    '/paths/', ...PATHS.map((p) => `/paths/${p.id}/`),
    ...courses.map((c) => `/courses/${c}/`),
    ...lessons.map((l) => `/lessons/${l.data.slug}/`),
    '/methods/', ...METHODS.map((m) => `/methods/${m.slug}/`),
    '/films/', ...(await allFilms()).map((f) => f.href),
    // The calendar (approved 2026-11-22). Its email-design preview stays out: it is a design page, not a tool.
    '/calendar/', '/calendar/parent/', '/calendar/student/', '/calendar/student/mcat/', '/calendar/teacher/',
    ...(await learnerCourses()).flatMap((c) => [`/calendar/student/${c.s}/`, `/calendar/teacher/${c.s}/`]),
    // Find an idea, and one page per idea the hop graph holds.
    '/ideas/', ...(await allIdeas()).map((i) => `/ideas/${i.id}/`),
  ];
  const body =
    '<?xml version="1.0" encoding="UTF-8"?>\n' +
    '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n' +
    paths.map((p) => `  <url><loc>${base}${p}</loc></url>`).join('\n') +
    '\n</urlset>\n';
  return new Response(body, { headers: { 'Content-Type': 'application/xml; charset=utf-8' } });
}
