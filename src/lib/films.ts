/* Every lesson film, as a list, for the pages that give each film its own address:
   /watch/<lesson>/            the lesson's opening film (`explainer` in the frontmatter)
   /watch/<lesson>/<film-id>/  each further film (`films[].id`)
   and the /films/ index. Published lessons only. The methods library has its own pages
   (/methods/<slug>/), so its films are not repeated here.

   Only what the frontmatter names becomes a page. Other files beside a film (for example a
   vertical cut saved as <film-id>-social.mp4) are ignored. */
import { getCollection } from 'astro:content';

export interface FilmEntry {
  /** Lesson slug. */
  lesson: string;
  lessonTitle: string;
  course: string;
  /** Lesson order within its course. */
  order: number;
  /** The lesson's one-line hook. */
  hook: string;
  /** Film id; null for the lesson's opening film. */
  id: string | null;
  /** /watch/... address, with a trailing slash. */
  href: string;
  src: string;
  captions: string;
  poster: string;
  title: string;
  durationSec: number;
  narration: string;
  factCheckedBy?: string;
}

export const watchHref = (lesson: string, id?: string | null) => (id ? `/watch/${lesson}/${id}/` : `/watch/${lesson}/`);

/** "3:09" */
export const filmClock = (sec: number) => `${Math.floor(sec / 60)}:${String(Math.round(sec % 60)).padStart(2, '0')}`.replace(/:60$/, ':59');

/** ISO 8601 duration for JSON-LD: "PT3M9S". */
export const filmIsoDuration = (sec: number) => {
  const s = Math.round(sec);
  return `PT${Math.floor(s / 60)}M${s % 60}S`;
};

export async function allFilms(): Promise<FilmEntry[]> {
  const lessons = await getCollection('lessons', ({ data }) => !data.draft);
  return lessons
    .sort((a, b) => (a.data.order ?? 99) - (b.data.order ?? 99))
    .flatMap((l) => {
      const d = l.data;
      const base = {
        lesson: d.slug, lessonTitle: d.title, course: d.course, order: d.order ?? 99,
        hook: d.hook ?? d.summary.split(/(?<=[.?!])\s+/)[0],
      };
      const pick = (f: NonNullable<typeof d.explainer>) => ({
        src: f.src, captions: f.captions, poster: f.poster, title: f.title, durationSec: f.durationSec,
        narration: f.narration, factCheckedBy: f.factCheckedBy,
      });
      return [
        ...(d.explainer ? [{ ...base, id: null, href: watchHref(d.slug), ...pick(d.explainer) }] : []),
        ...d.films.map((f) => ({ ...base, id: f.id, href: watchHref(d.slug, f.id), ...pick(f) })),
      ];
    });
}
