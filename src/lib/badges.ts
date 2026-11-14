/* Badges, on this device only (2026-11-14). No account, no server, nothing shared.

   A badge is a small, quiet mark for a real milestone: a name, a one-line description, the date it
   was earned and an icon. It is kept in the film record (src/lib/film-progress.ts, field `b`), so
   "Clear everything" on /progress/ removes it with the rest, and like that record it is not synced
   to accounts.

   One type so far:
     films-all   "Watched every film": every film of a course watched to about 90 percent. Shown on
                 the course's map (CourseMap.astro) and listed on /progress/. Earned on the course
                 page or the play-in-order page, the two pages that know the course's full film list.
                 Its date is when the last of those films was watched, not when the page noticed.

   Rules: no streaks, points, ranks, reminders or emails; wording states what was done ("watched"),
   never "completed" or "passed", and never counts down. */
import { loadFilms, recordBadge, type EarnedBadge, type FilmRecord } from './film-progress';

export type BadgeIcon = 'camera';

export interface BadgeType {
  /** Short name on the badge. */
  name: string;
  /** One line under it, for the subject (a course name). */
  describe: (subjectTitle: string) => string;
  /** The same line where the subject's name is already on the badge (a list such as /progress/). */
  short: string;
  icon: BadgeIcon;
}

export const BADGE_TYPES: Record<string, BadgeType> = {
  'films-all': {
    name: 'Watched every film',
    describe: (course) => `Every film in ${course}, watched on this device.`,
    short: 'Every film in the course, watched on this device.',
    icon: 'camera',
  },
};

export const badgeId = (type: string, subject: string) => `${type}:${subject}`;

/** Every badge earned on this device, oldest first. */
export function earnedBadges(r: FilmRecord = loadFilms()): EarnedBadge[] {
  return Object.values(r.b ?? {}).filter((b) => BADGE_TYPES[b.type]).sort((a, b) => a.at - b.at);
}

export function badgeFor(type: string, subject: string, r: FilmRecord = loadFilms()): EarnedBadge | null {
  return r.b?.[badgeId(type, subject)] ?? null;
}

/**
 * "Watched every film" for a course: earned (once) when every film key given is watched.
 * Returns the badge if earned now or before, otherwise null. With storage blocked nothing is kept.
 */
export function checkFilmsBadge(course: string, courseTitle: string, keys: string[]): EarnedBadge | null {
  const r = loadFilms();
  const had = badgeFor('films-all', course, r);
  if (had) return had;
  if (keys.length === 0 || !keys.every((k) => typeof r.w[k] === 'number')) return null;
  const at = Math.max(...keys.map((k) => r.w[k]));
  return recordBadge({ type: 'films-all', subject: course, subjectTitle: courseTitle, at });
}

/** "November 14, 2026" in the reader's language. */
export const badgeDate = (at: number) => new Date(at).toLocaleDateString(undefined, { year: 'numeric', month: 'long', day: 'numeric' });

/** Show the [data-badge="<type>:<subject>"] blocks (Badge.astro) that this device has earned, with their dates. */
export function showBadges(root: ParentNode = document, r: FilmRecord = loadFilms()): number {
  let shown = 0;
  root.querySelectorAll<HTMLElement>('[data-badge]').forEach((el) => {
    const b = r.b?.[el.dataset.badge!];
    el.hidden = !b;
    if (!b) return;
    shown++;
    const t = el.querySelector<HTMLTimeElement>('[data-badge-date]');
    if (t) { t.dateTime = new Date(b.at).toISOString().slice(0, 10); t.textContent = badgeDate(b.at); }
  });
  return shown;
}
