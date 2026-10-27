/* One JSON file per published lesson with its quiz, for the review queue
   (/review/). The queue only knows question ids and lesson slugs (kept in the
   browser, src/lib/progress.ts); it fetches the files for the lessons that have
   questions due. Each question carries the section that teaches it. */
import type { APIRoute } from 'astro';
import { getCollection, render } from 'astro:content';
import { itemId } from '../../lib/progress';
import { anchorsFor } from '../../lib/quiz-anchors';
import { openItems } from '../../lib/open-items';
import { courseOf } from '../../data/courses';

export async function getStaticPaths() {
  const lessons = await getCollection('lessons', ({ data }) => !data.draft);
  return lessons.map((entry) => ({ params: { slug: entry.data.slug }, props: { entry } }));
}

export const GET: APIRoute = async ({ props }) => {
  const { entry } = props as { entry: Awaited<ReturnType<typeof getCollection<'lessons'>>>[number] };
  const { headings } = await render(entry);
  const qs = [...entry.data.practiceQuestions, ...entry.data.mcatQuestions];
  const anchors = anchorsFor(entry.body ?? '', headings, qs);
  const body = {
    slug: entry.data.slug,
    title: entry.data.title,
    course: courseOf(entry.data.course).title,
    // Grade level for AI feedback wording: 7 (grade 7), 10 (high school) or 13 (college). The ages 5–10
    // activities are read by the parent or teacher, so their feedback is worded for an adult reader at grade 7.
    grade: courseOf(entry.data.course).tier === 'families' ? 7 : courseOf(entry.data.course).tier === 'highschool' ? (courseOf(entry.data.course).ladderStep === 1 ? 7 : 10) : 13,
    open: openItems(entry.body ?? ''),
    items: qs.map((q, i) => ({
      id: itemId(entry.data.slug, q.stem),
      mcat: i >= entry.data.practiceQuestions.length,
      stem: q.stem,
      choices: q.choices,
      answer: q.answer,
      rationale: q.rationale,
      anchor: anchors[i],
    })),
  };
  return new Response(JSON.stringify(body), { headers: { 'Content-Type': 'application/json' } });
};
