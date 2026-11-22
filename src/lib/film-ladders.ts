/* The ladders the film library plays (2026-11-22): see /films/ladders.json (src/pages/films/ladders.json.ts)
   for the shape. Used by that file and by the ladder picker on /films/. */
import { allIdeas, runOf } from './hop';
import { filmCatalog, filmKey } from './film-catalog';

export type LadderFilm = [key: string, title: string, href: string, rank: number, seconds: number, poster: string];
export interface FilmLadder {
  id: string;
  name: string;
  short: string;
  area: string;
  rungs: { slug: string; title: string; href: string; rank: number; courseTitle: string; adds?: string }[];
  films: LadderFilm[];
}

let cache: Promise<FilmLadder[]> | undefined;
/** Every ladder the film library can play, in the hop graph's order (by area). */
export function filmLadders(): Promise<FilmLadder[]> {
  cache ??= (async () => {
    const catalog = await filmCatalog();
    const lessonFilms = new Map<string, typeof catalog>();
    for (const f of catalog) {
      if (!f.lesson || !f.href.startsWith('/watch/') || !['first', 'second', 'series'].includes(f.kind)) continue;
      if (!lessonFilms.has(f.lesson)) lessonFilms.set(f.lesson, []);
      lessonFilms.get(f.lesson)!.push(f);
    }
    for (const list of lessonFilms.values()) list.sort((a, b) => a.position - b.position);

    const ladders: FilmLadder[] = [];
    for (const i of await allIdeas()) {
      if (!i.play) continue;
      const run = runOf(i.films);
      const lessons: { slug: string; rank: number }[] = [];
      for (const f of run) if (!lessons.some((l) => l.slug === f.lesson)) lessons.push({ slug: f.lesson, rank: f.rank });
      const films: LadderFilm[] = [];
      for (const l of lessons) {
        for (const f of lessonFilms.get(l.slug) ?? []) {
          films.push([filmKey(f.src), f.title, f.href, l.rank, Math.round(f.durationSec), f.poster]);
        }
      }
      // A rung for every level the films sit at, so each thumbnail has a rung to stand on.
      const ranks = new Set(i.rungs.map((r) => r.rank));
      if (films.length < 2 || films.some((f) => !ranks.has(f[3]))) continue;
      ladders.push({
        id: i.id,
        name: i.name,
        short: i.short,
        area: i.areaName,
        rungs: i.rungs.map((r) => ({ slug: r.slug, title: r.title, href: r.href, rank: r.rank, courseTitle: r.courseTitle, ...(r.adds ? { adds: r.adds } : {}) })),
        films,
      });
    }
    return ladders;
  })();
  return cache;
}
