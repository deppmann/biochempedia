/* The theater's view of one film, at build time (2026-11-20): scene times, the film's own questions,
   the part of the lesson it goes with, and, where a hand-checked map exists, its named parts with
   figures on cue. All of it comes from scripts/film-timelines/lib.mjs, which reads files already in
   the repository and calls no model. See scripts/film-timelines/README.md. */
import * as timelines from '../../scripts/film-timelines/lib.mjs';

/* The module is plain JavaScript shared with the check, the report and the tests; its shape is stated here. */
type FilmTimeline = (root: string, film: { key: string; lesson: string | null; index: number | null; duration: number }) => {
  status: Theater['status']; lines: Theater['lines']; region: Theater['region']; parts: TheaterPart[];
  times: { questions: TheaterQuestion[] } | null;
};
const filmTimeline = (timelines as unknown as { filmTimeline: FilmTimeline }).filmTimeline;

export interface TheaterFigure { src: string; alt: string; caption: string; width: number; height: number; keyItems: string[]; scaffold: boolean }
export interface TheaterPart {
  from: string;
  start: number;
  end: number | null;
  /** A question part carries only the film's question and when its answer starts. */
  question?: string;
  revealStart?: number;
  title?: string;
  section?: { id: string; text: string };
  term?: { word: string; def: string; at: number };
  figure?: TheaterFigure;
}
export interface TheaterQuestion { scene: string; reveal: string; start: number; revealStart: number; text: string }
export interface Theater {
  key: string;
  status: 'mapped' | 'timed' | 'partial' | 'captions' | 'none';
  /** Transcript lines (whole sentences), each with the second it starts. */
  lines: { start: number; end: number; text: string }[];
  questions: TheaterQuestion[];
  region: { section: { id: string; text: string } | null; sections: { id: string; text: string }[]; figures: TheaterFigure[] };
  parts: TheaterPart[];
}

/** `index` is the film's place in the lesson's `films` (null for the opening film). */
export function theaterFor(film: { src: string; lesson: string; durationSec: number }, index: number | null): Theater {
  const key = film.src.replace(/^\/explainers\//, '').replace(/\.mp4$/, '');
  const t = filmTimeline(process.cwd(), { key, lesson: film.lesson, index, duration: film.durationSec });
  return { key, status: t.status, lines: t.lines, questions: t.times?.questions ?? [], region: t.region, parts: t.parts };
}

/** The film's question as the theater prints it: the film's own words, without its closing
 *  "Pause and decide." (the theater says that itself, once). */
export const questionText = (text: string) => text.replace(/\s*(Pause and (decide|think|predict)[^.?!]*[.?!]?)\s*$/i, '').trim();
