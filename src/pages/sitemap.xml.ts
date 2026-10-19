import type { APIContext } from 'astro';
import { getCollection } from 'astro:content';
import { listedMethods } from '../data/methods';

/**
 * Hand-rolled sitemap (no @astrojs/sitemap — Astro deps are pinned). Lists the
 * static pages plus every non-draft lesson, using the canonical `site` from
 * astro.config.mjs. Prerendered to /sitemap.xml at build time.
 */
export async function GET(context: APIContext): Promise<Response> {
  const base = (context.site?.href ?? 'https://biochemistrypedia.com').replace(/\/$/, '');
  const lessons = (await getCollection('lessons')).filter((l) => !l.data.draft);
  // A course page exists only once the course has a published lesson.
  const courses = [...new Set(lessons.map((l) => l.data.course))];
  const paths = [
    '/', '/about', '/fun', '/play', '/contact', '/search/',
    '/teachers', '/teachers/demo', '/teachers/how-its-built',
    ...courses.map((c) => `/courses/${c}/`),
    ...lessons.map((l) => `/lessons/${l.data.slug}/`),
    ...(listedMethods().length > 0 ? ['/methods/', ...listedMethods().map((m) => `/methods/${m.slug}/`)] : []),
  ];
  const body =
    '<?xml version="1.0" encoding="UTF-8"?>\n' +
    '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n' +
    paths.map((p) => `  <url><loc>${base}${p}</loc></url>`).join('\n') +
    '\n</urlset>\n';
  return new Response(body, { headers: { 'Content-Type': 'application/xml; charset=utf-8' } });
}
