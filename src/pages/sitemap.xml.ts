import type { APIContext } from 'astro';
import { PATHS } from '../data/paths';
import { getCollection } from 'astro:content';
import { METHODS, methodHref } from '../data/methods';
import { methodCourses } from '../lib/method-courses';
import { SETS as MCAT_SETS } from '../lib/mcat';
import { allFilms } from '../lib/films';
import { SITE_ORIGIN } from '../lib/site-host.mjs';
import { allIdeas } from '../lib/hop';
import { learnerCourses } from '../lib/calendar/data';
import { recordFor } from '../lib/production-record';
import { MILESTONES } from '../data/updates';
import updatesPRs from '../data/updates-prs.json';

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
  const lastmod = new Map<string, string>();
  for (const { data } of lessons) {
    const record = recordFor(data.slug);
    const date = record?.levelUp?.shipped ?? record?.sideHops?.updated;
    if (!date) continue;
    lastmod.set(`/lessons/${data.slug}/`, date);
    // Course pages list these lessons and their times. The course catalog and home list the courses.
    for (const path of [`/courses/${data.course}/`, '/courses/', '/']) {
      if (date > (lastmod.get(path) ?? '')) lastmod.set(path, date);
    }
  }
  const updatesDate = [updatesPRs.at(-1)?.d, ...MILESTONES.map((m) => m.date)].filter(Boolean).sort().at(-1);
  if (updatesDate) lastmod.set('/updates/', updatesDate);
  const paths = [
    '/', '/courses/', '/about/', '/updates/', '/fun/', '/play/', '/contact/', '/license/',
    '/math-toolkit/', '/privacy/', '/hex/', '/contributors/',
    '/teachers/', '/teachers/talk-notes/', '/teachers/demo/', '/teachers/how-its-built/',
    '/teachers/do-it-yourself/', '/teachers/checklist/', '/teachers/sources/', '/teachers/talk/',
    '/teachers/life-science/', '/teachers/biology/',
    '/teach/', '/teach/privacy/',
    '/mcat/', '/mcat/diagnostic/', '/mcat/practice/', ...MCAT_SETS.map((s) => `/mcat/${s.id}/`),
    '/paths/', ...PATHS.map((p) => `/paths/${p.id}/`),
    ...courses.map((c) => `/courses/${c}/`),
    ...lessons.map((l) => `/lessons/${l.data.slug}/`),
    '/methods/', ...METHODS.map((m) => methodHref(m.slug)), ...methodCourses(lessons).map((c) => methodHref(c.slug)),
    '/films/', ...(await allFilms()).map((f) => f.href),
    // The calendar (approved 2026-11-22). Its email-design preview stays out: it is a design page, not a tool.
    '/calendar/', '/calendar/parent/', '/calendar/student/', '/calendar/student/mcat/', '/calendar/teacher/',
    ...(await learnerCourses()).flatMap((c) => [`/calendar/student/${c.s}/`, `/calendar/teacher/${c.s}/`]),
    // Find an idea, and one page per idea the hop graph holds.
    '/ideas/', '/start/', ...(await allIdeas()).map((i) => `/ideas/${i.id}/`),
  ];
  const body =
    '<?xml version="1.0" encoding="UTF-8"?>\n' +
    '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n' +
    paths.map((p) => {
      const date = lastmod.get(p);
      const loc = new URL(p, base).href.replace(/&/g, '&amp;');
      return `  <url><loc>${loc}</loc>${date ? `<lastmod>${date}</lastmod>` : ''}</url>`;
    }).join('\n') +
    '\n</urlset>\n';
  return new Response(body, { headers: { 'Content-Type': 'application/xml; charset=utf-8' } });
}
