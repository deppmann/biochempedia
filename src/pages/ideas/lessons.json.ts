/* /ideas/lessons.json: what the idea search needs beyond /graph.json. One row per live lesson:
   [slug, title, level (0 = ages 5 to 10 … 6 = graduate), Virginia standards codes, unit name].
   With it "Find an idea" can match a lesson's title, a standards code such as BIO.3d and a
   unit's name, and can link each level of a result straight to its lesson. Static, built with the
   site; nothing about visitors. Rows may gain columns at the end, never lose or reorder them. */
import type { APIRoute } from 'astro';
import { COURSES } from '../../data/courses';
import { stageOf } from '../../data/stages';
import { stageRank } from '../../lib/topic-graph';
import { lessonFacts } from '../../lib/hop';

export const GET: APIRoute = async () => {
  const facts = await lessonFacts();
  const order = new Map(COURSES.map((c, i) => [c.slug, i]));
  const rows = [...facts.entries()]
    .map(([slug, f]) => {
      const course = COURSES.find((c) => c.slug === f.data.course);
      return { slug, title: f.data.title as string, rank: course ? stageRank(stageOf(course)) : -1, sol: f.sol, unit: f.unit, c: order.get(f.data.course) ?? 99 };
    })
    .filter((r) => r.rank >= 0)
    .sort((a, b) => a.rank - b.rank || a.c - b.c || a.slug.localeCompare(b.slug))
    .map((r) => [r.slug, r.title, r.rank, r.sol, r.unit]);
  return new Response(JSON.stringify({ v: 1, lessons: rows }), { headers: { 'Content-Type': 'application/json; charset=utf-8' } });
};
