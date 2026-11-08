import { getCollection, render } from 'astro:content';
import { COURSES, courseOf } from '../data/courses';

/**
 * The search index: one small record per published lesson, built with the site
 * and fetched by <SiteSearch> the first time someone types. It holds what a
 * student would search by (title, the one-line hook, objectives, every section
 * heading, the scientists, techniques and structures a lesson names), not the
 * full prose, which keeps the file small enough to load on a phone. It answers the
 * first keystrokes. The full text of every lesson is searched separately by Pagefind
 * (/pagefind/, built after `astro build`; see docs/expansion/mission-2026-10/FULLTEXT_SEARCH.md),
 * which loads only the pieces a query needs. Keep prose out of this file.
 */
export async function GET(): Promise<Response> {
  const lessons = (await getCollection('lessons', ({ data }) => import.meta.env.DEV || !data.draft));
  const records: { s: string; c: string; n: number; t: string; u: string; k: string; h: string; x: string; g: [string, string][] }[] = [];
  for (const course of COURSES) {
    const mine = lessons
      .filter((l) => l.data.course === course.slug)
      .sort((a, b) => (a.data.order ?? 999) - (b.data.order ?? 999));
    for (const [i, l] of mine.entries()) {
      const { headings } = await render(l);
      const d = l.data;
      const unit = course.units.find((u) => u.slugs.includes(d.slug))?.name ?? '';
      records.push({
        s: d.slug,
        c: course.slug,
        n: i + 1,
        t: d.title,
        u: unit,
        k: d.courseChapter,
        h: d.hook ?? d.summary.split(/(?<=[.?!])\s+/)[0],
        // Everything else a query may hit, joined: summary, objectives and names.
        x: [
          d.summary,
          ...d.objectives,
          ...d.scientists.map((p) => p.name),
          ...d.techniques.map((q) => q.name),
          ...d.structures.map((q) => q.label),
        ].filter(Boolean).join(' · '),
        // Section headings, each a place to land: [text, anchor].
        g: headings.filter((g) => g.depth === 2 || g.depth === 3).map((g): [string, string] => [g.text, g.slug]),
      });
    }
  }
  const courses = COURSES.filter((c) => records.some((r) => r.c === c.slug)).map((c) => ({ s: c.slug, t: courseOf(c.slug).title }));
  return new Response(JSON.stringify({ courses, lessons: records }), {
    headers: { 'Content-Type': 'application/json; charset=utf-8' },
  });
}
