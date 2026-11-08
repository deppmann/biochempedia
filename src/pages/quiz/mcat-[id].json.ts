/* Review-queue data for MCAT passage sets, in the same shape as a lesson's
   /quiz/<slug>.json, plus the passage so a missed question comes back with it. */
import type { APIRoute } from 'astro';
import { SETS, type McatSet } from '../../lib/mcat';
import { itemId } from '../../lib/progress';

export function getStaticPaths() {
  return SETS.map((s) => ({ params: { id: s.id }, props: { set: s } }));
}

export const GET: APIRoute = ({ props }) => {
  const { set } = props as { set: McatSet };
  const slug = `mcat-${set.id}`;
  return new Response(JSON.stringify({
    slug, title: set.title, course: 'MCAT practice', grade: 13, open: [],
    passage: set.passage, figures: set.figures ?? [], setUrl: `/mcat/${set.id}/`,
    items: set.questions.map((q) => ({
      id: itemId(slug, q.stem), mcat: true, stem: q.stem, choices: q.choices, answer: q.answer,
      rationale: q.why[q.answer], lessonSlug: q.lesson.slug,
      anchor: q.lesson.anchor ? { id: q.lesson.anchor, text: 'the lesson section' } : null,
    })),
  }), { headers: { 'Content-Type': 'application/json' } });
};
