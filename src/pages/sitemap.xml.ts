import type { APIContext } from 'astro';
import { getCollection } from 'astro:content';

/**
 * Hand-rolled sitemap (no @astrojs/sitemap — Astro deps are pinned). Lists the
 * static pages plus every non-draft lesson, using the canonical `site` from
 * astro.config.mjs. Prerendered to /sitemap.xml at build time.
 */
export async function GET(context: APIContext): Promise<Response> {
  const base = (context.site?.href ?? 'https://biochempedia.deppmannlab.com').replace(/\/$/, '');
  const lessons = (await getCollection('lessons')).filter((l) => !l.data.draft);
  const paths = ['/', '/about', '/contact', ...lessons.map((l) => `/lessons/${l.data.slug}/`)];
  const body =
    '<?xml version="1.0" encoding="UTF-8"?>\n' +
    '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n' +
    paths.map((p) => `  <url><loc>${base}${p}</loc></url>`).join('\n') +
    '\n</urlset>\n';
  return new Response(body, { headers: { 'Content-Type': 'application/xml; charset=utf-8' } });
}
