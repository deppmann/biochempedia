/* /films.json: every film on the site (src/lib/film-catalog.ts), for AI agents and other programs.
   Paths are absolute URLs; the /films/ page is the same list for people. */
import type { APIRoute } from 'astro';
import { filmCatalog, KIND_LABELS } from '../lib/film-catalog';
import { SITE } from '../lib/agent-catalog';

export const GET: APIRoute = async () => {
  const abs = (p?: string) => (p ? SITE + p : undefined);
  const films = (await filmCatalog()).map((f) => ({
    id: f.id,
    title: f.title,
    kind: f.kind,
    kindLabel: KIND_LABELS[f.kind],
    ...(f.part ? { part: f.part } : {}),
    course: f.course,
    courseTitle: f.courseTitle,
    level: f.stage,
    levelTitle: f.stageTitle,
    ...(f.lesson ? { lesson: f.lesson, lessonTitle: f.lessonTitle, lessonUrl: abs(f.lessonHref) } : {}),
    url: abs(f.href),
    durationSec: f.durationSec,
    poster: abs(f.poster),
    video: abs(f.src),
    captions: abs(f.captions),
    description: f.description,
    ...(f.takeaways ? { takeaways: f.takeaways } : {}),
    ...(f.rewritten ? { lessonRewritten: f.rewritten } : {}),
    ...(f.method ? { method: { ...f.method, url: `${SITE}/methods/${f.method.slug}/` } } : {}),
  }));
  const body = {
    name: 'Biochemistrypedia films',
    url: `${SITE}/films/`,
    license: 'https://creativecommons.org/licenses/by-nc-sa/4.0/',
    note: 'Animations and narration are AI-generated. Scientist profile films read text from The Molecule Hunters, which is not covered by the CC licence.',
    generated: new Date().toISOString().slice(0, 10),
    count: films.length,
    films,
  };
  return new Response(JSON.stringify(body), { headers: { 'Content-Type': 'application/json; charset=utf-8' } });
};
