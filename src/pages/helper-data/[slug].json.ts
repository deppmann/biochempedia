/* What the study helpers (worker/helper.js) need about one lesson, beyond its Markdown copy
   (/lessons/<slug>.md, the text the model is grounded in): its title, course and level, the
   "explain at my level" versions, and each claim-evidence-reasoning box's task and model answer.
   Static, written at build. Everything in it is already on the lesson page.

   Only lessons the helpers may be offered on get a file (src/lib/helper-lesson.mjs: not Biology
   Together, not grade 7 Life Science), so the Worker refuses the rest. */
import type { APIRoute } from 'astro';
import { getCollection } from 'astro:content';
import { courseOf } from '../../data/courses';
import { helperAllowed, levelLabel, parseCers } from '../../lib/helper-lesson.mjs';

export async function getStaticPaths() {
  const lessons = await getCollection('lessons', ({ data }) => !data.draft && helperAllowed(courseOf(data.course)));
  return lessons.map((entry) => ({ params: { slug: entry.data.slug }, props: { entry } }));
}

export const GET: APIRoute = async ({ props }) => {
  const { entry } = props as { entry: Awaited<ReturnType<typeof getCollection<'lessons'>>>[number] };
  const d = entry.data;
  const course = courseOf(d.course);
  const body = {
    slug: d.slug,
    title: d.title,
    course: course.slug,
    courseTitle: course.title,
    level: levelLabel(course),
    explainLevels: d.explainLevels.map((l) => ({ level: l.level, label: l.label, text: l.text })),
    cers: parseCers(entry.body ?? ''),
  };
  return new Response(JSON.stringify(body), { headers: { 'Content-Type': 'application/json' } });
};
