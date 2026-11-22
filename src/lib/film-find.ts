/* Films for the site search box (src/components/SiteSearch.astro), 2026-11-22: the same two files and
   the same matcher as the film library (src/lib/film-search.mjs), loaded once, the first time the box
   is used. A film is found on its own, not only through its lesson. */
import type { FilmList, ListFilm } from './film-cards';
import { prepare, searchFilms } from './film-search.mjs';

export interface FilmFinder { list: FilmList; data: unknown }
let once: Promise<FilmFinder | null> | undefined;

export function loadFilmFinder(): Promise<FilmFinder | null> {
  once ??= Promise.all([
    fetch('/films/list.json').then((r) => (r.ok ? (r.json() as Promise<FilmList>) : null)),
    // Without search.json the films are still found by title, lesson, course and level.
    fetch('/films/search.json').then((r) => (r.ok ? r.json() : null)).catch(() => null),
  ]).then(([list, data]) => (list ? { list, data } : null)).catch(() => null)
    .then((r) => { if (!r) once = undefined; return r; });
  return once;
}

/** The films for a query: those with every word first (`full` of them), then those with all but one. */
export function findFilms(f: FilmFinder, q: string, course = ''): { films: ListFilm[]; full: number; kind: string } {
  const r = searchFilms(prepare(f.list, f.data), q, course && course !== 'all' ? { course } : {});
  return { films: r.films as ListFilm[], full: r.full, kind: r.kind };
}
