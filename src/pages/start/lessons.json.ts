/* /start/lessons.json: what the mini syllabus (/start/) and the teacher's syllabus matcher
   (/teach/match/) need beyond /graph.json and /ideas/lessons.json. One entry per live lesson:

     slug: [whole-lesson minutes, skim minutes (0 when the lesson has no skim), phrases]

   The minutes are the lesson page's own ("How long have you got?", src/lib/lesson-time.ts), so a
   path's total agrees with what the lesson then says. The phrases are what a student might type
   that the lesson answers in other words (src/data/lesson-links.json, written offline); the
   matcher (src/lib/syllabus-match.mjs) reads them in the browser. Static, built with the site;
   nothing about visitors. Entries may gain items at the end, never lose or reorder them. */
import type { APIRoute } from 'astro';
import { getCollection, render } from 'astro:content';
import { courseOf } from '../../data/courses';
import lessonLinks from '../../data/lesson-links.json';
import { lessonTime } from '../../lib/lesson-time';
import { skimOf, mainIdeaOf, filmTakeawaysOf, wordsIn } from '../../lib/skim';
import { sideHopsFor } from '../../lib/side-hops';

export const GET: APIRoute = async () => {
  const phrases = lessonLinks.lessons as Record<string, { search?: string[] }>;
  const out: Record<string, [number, number, string[]]> = {};
  const lessons = (await getCollection('lessons', ({ data }) => !data.draft)).sort((a, b) => a.data.slug.localeCompare(b.data.slug));
  for (const entry of lessons) {
    const d = entry.data;
    const { headings } = await render(entry);
    const body = entry.body ?? '';
    // The same sums as the lesson page (src/pages/lessons/[...slug].astro), so the figures agree.
    const skim = skimOf(body, headings);
    const skimWords = skim.words + wordsIn(mainIdeaOf(d).text) + filmTakeawaysOf(d).reduce((n, f) => n + wordsIn(f.takeaways.join(' ')), 0);
    const hops = sideHopsFor(d.slug);
    const time = lessonTime({
      tier: courseOf(d.course).tier, body, estMinutes: d.estMinutes, simulations: d.simulations.length,
      explainer: d.explainer, films: d.films, questions: 0,
      h2: headings.filter((h) => h.depth === 2), skimWords, skimFigures: [...body.matchAll(/<LessonFigure\b/g)].length,
      stories: hops ? { audioSec: hops.audio.durationSec, hops: hops.hops } : undefined,
    });
    out[d.slug] = [time.whole, time.stops.find((s) => s.id === 'skim')?.min ?? 0, phrases[d.slug]?.search ?? []];
  }
  return new Response(JSON.stringify({ v: 1, lessons: out }), { headers: { 'Content-Type': 'application/json; charset=utf-8' } });
};
