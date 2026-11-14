/* /films/list.json (2026-11-14): the film catalog, cut down to what a card shows, for the /films/
   page. That page sends only its first 60 cards as HTML and fetches this the first time a visitor
   filters, sorts, searches or asks for more. Paths stay site-relative (no host), as in the lesson
   frontmatter. Programs should use /films.json, which has every field and absolute URLs. */
import type { APIRoute } from 'astro';
import { filmCatalog, filmKey, kindBadge } from '../../lib/film-catalog';
import { STAGES } from '../../data/stages';

export const GET: APIRoute = async () => {
  const all = await filmCatalog();
  const courses: Record<string, string> = {};
  for (const f of all) if (f.course) courses[f.course] = f.courseTitle;
  const levels = Object.fromEntries(STAGES.filter((s) => all.some((f) => f.stage === s.key)).map((s) => [s.key, s.title]));
  const films = all.map((f) => ({
    f: filmKey(f.src),
    t: f.title,
    k: f.kind,
    b: kindBadge(f),
    c: f.course ?? '',
    s: f.stage ?? '',
    ...(f.lessonTitle ? { l: f.lessonTitle } : {}),
    h: f.href,
    o: f.poster,
    d: Math.round(f.durationSec),
    ...(f.rewritten ? { r: f.rewritten } : {}),
    ...(f.takeaways?.[0] ? { th: f.takeaways[0] } : {}),
    i: f.position,
  }));
  return new Response(JSON.stringify({ count: films.length, courses, levels, films }), {
    headers: { 'Content-Type': 'application/json; charset=utf-8' },
  });
};
