import { getCollection } from 'astro:content';
import { COURSES, unitsFor } from '../data/courses';
import { methodsFor, methodHref } from '../data/methods';
import { lessonMinutes } from '../lib/reading-time';
import { watchHref } from '../lib/films';
import { filmKey } from '../lib/film-catalog';

/**
 * The study planner's catalog (worker/planner.js): every published lesson with what it offers,
 * in course and unit order. Built with the site and read by the Worker through the ASSETS binding.
 * The Worker turns it into the cached system-prompt block and uses it to check every lesson,
 * film, simulation and method the model names; it also expands saved plans from it, so a saved
 * plan keeps only references and never needs the model to be shown again.
 *
 * Per lesson: s slug, c course, u unit index, n number in the course, t title, h hook,
 * m reading minutes, f films [key, kind, seconds, title, href], si simulation titles,
 * me method films [slug, name, seconds], k flashcard count, q practice question count.
 * Public like the rest of the site; nothing about visitors. Fixed order, no dates, so the
 * prompt built from it is byte-identical between builds that change no lesson.
 */
const LEVEL: Record<string, string> = {
  families: 'ages 5-10, an activity a grown-up runs',
  highschool: 'grades 7-12',
  foundation: 'first-year college',
  core: 'core upper-level college',
  elective: 'upper-level elective',
  advanced: 'advanced, research-based',
};

const tidy = (s: string, max: number) => {
  const one = s.replace(/\s+/g, ' ').replace(/\|/g, '/').trim();
  if (one.length <= max) return one;
  const cut = one.slice(0, max);
  return cut.slice(0, Math.max(cut.lastIndexOf(' '), max - 20)).replace(/[ ,;:.\-–—]+$/, '') + '…';
};

const DECKS = import.meta.glob<{ default: { slug: string; cards?: unknown[] } }>('../data/flashcards/*.json', { eager: true });
const deckSize = new Map(Object.values(DECKS).map((m) => m.default).filter((d) => d.slug).map((d) => [d.slug, d.cards?.length ?? 0]));

export async function GET(): Promise<Response> {
  const lessons = await getCollection('lessons', ({ data }) => !data.draft);
  const courses: { s: string; t: string; tier: string; level: string; mcat: boolean; units: string[] }[] = [];
  const out: unknown[] = [];
  for (const course of COURSES) {
    const mine = lessons.filter((l) => l.data.course === course.slug);
    if (!mine.length) continue;
    const units = unitsFor(course, mine);
    courses.push({ s: course.slug, t: course.title, tier: course.tier, level: LEVEL[course.tier] ?? course.tier, mcat: !!course.mcat, units: units.map((u) => tidy(u.name, 80)) });
    units.forEach((u, ui) => {
      for (const { l, n } of u.entries) {
        const d = l.data;
        const films: [string, string, number, string, string][] = [];
        if (d.explainer) films.push([filmKey(d.explainer.src), 'first', Math.round(d.explainer.durationSec), tidy(d.explainer.title, 80), watchHref(d.slug)]);
        for (const f of d.films) films.push([filmKey(f.src), d.films.length > 1 ? 'series' : 'second', Math.round(f.durationSec), tidy(f.title, 80), watchHref(d.slug, f.id)]);
        const methods = methodsFor(d.slug)
          .filter((m) => !films.some((f) => m.film && f[0] === filmKey(m.film.src)))
          .map((m) => [m.slug, tidy(m.name, 60), Math.round(m.film!.durationSec), methodHref(m.slug)]);
        out.push({
          s: d.slug, c: course.slug, u: ui, n, t: tidy(d.title, 90),
          h: tidy(d.hook ?? d.summary.split(/(?<=[.?!])\s+/)[0], 150),
          m: lessonMinutes(l)?.core ?? 20,
          f: films,
          si: d.simulations.map((s) => tidy(s.title, 60)),
          me: methods,
          k: deckSize.get(d.slug) ?? 0,
          q: d.practiceQuestions.length,
        });
      }
    });
  }
  return new Response(JSON.stringify({ v: 1, courses, lessons: out }), {
    headers: { 'Content-Type': 'application/json; charset=utf-8' },
  });
}
