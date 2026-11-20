/* /films/ideas.json (2026-11-20): what the library's search reads besides titles. For each lesson
   that has a film: the questions and phrases people use for it ("why does salt make water come out
   of cucumber"), taken from src/data/lesson-links.json, where they were written once, offline, and
   checked. Keyed by lesson title, lower case, so "why do cells swell in water" finds the osmosis
   films. Fetched only when someone first uses the search box. */
import type { APIRoute } from 'astro';
import { filmCatalog } from '../../lib/film-catalog';
import links from '../../data/lesson-links.json';

export const GET: APIRoute = async () => {
  const fold = (s: string) => s.normalize('NFD').replace(/[̀-ͯ]/g, '').toLowerCase();
  const recs = links.lessons as Record<string, { search?: string[] }>;
  const out: Record<string, string> = {};
  for (const f of await filmCatalog()) {
    if (!f.lesson || !f.lessonTitle || out[f.lessonTitle]) continue;
    const s = recs[f.lesson]?.search;
    if (s?.length) out[f.lessonTitle] = fold(s.join(' | '));
  }
  return new Response(JSON.stringify(out), { headers: { 'Content-Type': 'application/json; charset=utf-8' } });
};
