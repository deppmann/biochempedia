/* A view of the film library (2026-11-20): which films a set of choices selects, in what order,
   and which of them fit a time budget. Shared by /films/ (which shows the view) and /films/run/
   (which plays it), so the two cannot disagree. Browser code; the data is /films/list.json.

   The view lives in the query string, with the names the library has always used:
     q      search words            sort   course | short | long | new | az
     level  a stage key             course a course slug        kind  a film kind
   plus, for a run: t = 10 | 20 | 30 (minutes). */
import type { FilmList, ListFilm } from './film-cards';
import { isWatched, type FilmRecord } from './film-progress';

export const FIELDS = ['q', 'sort', 'level', 'course', 'kind'] as const;
export type Field = (typeof FIELDS)[number];
export type View = Record<Field, string>;
export const SORTS = ['course', 'short', 'long', 'new', 'az'];
export const BUDGETS = [10, 20, 30];
/** A run may end this many seconds past its budget, never more. */
export const SLACK = 60;

export const fold = (s: string) => s.normalize('NFD').replace(/[̀-ͯ]/g, '').toLowerCase();

export function readView(search: string, list?: FilmList): View {
  const p = new URLSearchParams(search);
  const v = Object.fromEntries(FIELDS.map((f) => [f, (p.get(f) ?? '').trim()])) as View;
  if (!SORTS.includes(v.sort)) v.sort = 'course';
  if (list) {
    // A value the library does not have (an old or mistyped link) is ignored.
    if (v.level && !(v.level in list.levels)) v.level = '';
    if (v.course && !(v.course in list.courses)) v.course = '';
    if (v.kind && !list.films.some((f) => f.k === v.kind)) v.kind = '';
  }
  return v;
}
export const isDefault = (v: View) => !v.q && !v.level && !v.course && !v.kind && v.sort === 'course';
export function viewQuery(v: View, extra: Record<string, string> = {}): string {
  const p = new URLSearchParams();
  for (const f of FIELDS) if (v[f] && !(f === 'sort' && v[f] === 'course')) p.set(f, v[f]);
  for (const [k, x] of Object.entries(extra)) if (x) p.set(k, x);
  const qs = p.toString();
  return qs ? `?${qs}` : '';
}

/** What a search reads for each lesson besides titles: the questions people ask about it
 *  (/films/ideas.json, loaded the first time someone uses the search box). */
export type Ideas = Record<string, string>;

const collator = new Intl.Collator('en', { sensitivity: 'base', numeric: true });
const COMPARE: Record<string, (a: ListFilm, b: ListFilm) => number> = {
  course: (a, b) => a.i - b.i,
  short: (a, b) => a.d - b.d || a.i - b.i,
  long: (a, b) => b.d - a.d || a.i - b.i,
  // Newest rewrites first; films whose lesson has no rewrite date follow, in course order.
  new: (a, b) => ((b.r ?? '') > (a.r ?? '') ? 1 : (b.r ?? '') < (a.r ?? '') ? -1 : 0) || a.i - b.i,
  az: (a, b) => collator.compare(a.t, b.t) || a.i - b.i,
};

/** The films a view selects, in its order. A search matches when every word is in the film's title,
 *  its lesson's title or, once loaded, the questions people ask about that lesson; films matched by
 *  title come first. */
export function select(list: FilmList, v: View, ideas?: Ideas | null): ListFilm[] {
  const words = fold(v.q).split(/\s+/).filter((w) => w.length > 1 || /\d/.test(w));
  const byTitle = new Set<ListFilm>();
  const out = list.films.filter((f) => {
    if (v.level && f.s !== v.level) return false;
    if (v.course && f.c !== v.course) return false;
    if (v.kind && f.k !== v.kind) return false;
    if (!words.length) return true;
    const title = fold(`${f.t} ${f.l ?? ''}`);
    if (words.every((w) => title.includes(w))) { byTitle.add(f); return true; }
    const idea = f.l && ideas ? `${title} ${ideas[f.l] ?? ''}` : '';
    return !!idea && words.every((w) => idea.includes(w));
  });
  out.sort(COMPARE[v.sort] ?? COMPARE.course);
  if (words.length && byTitle.size && byTitle.size < out.length) return [...out.filter((f) => byTitle.has(f)), ...out.filter((f) => !byTitle.has(f))];
  return out;
}

/** The films a run plays, before any time budget: the view, without the Biology Together films
 *  (those set up an activity a grown-up runs; they are no use back to back) unless that level, its
 *  course or that kind was asked for, and without scientist profiles and method films, which open on
 *  other pages. */
export function runnable(films: ListFilm[], v: View): ListFilm[] {
  const young = v.level === 'ages-5-10' || v.kind === 'activity' || films.every((f) => f.k === 'activity');
  return films.filter((f) => f.h.startsWith('/watch/') && (young || f.k !== 'activity'));
}

/**
 * The time-budget rule (the same as the play-in-order page, 2026-11-15): start at the first film not
 * yet watched on this device, add whole films while the next would end no more than a minute past
 * the budget, always at least one, and stop at the first film that does not fit (never skip ahead
 * to a shorter one). With no budget: every film from the first unwatched one.
 */
export function fit(queue: ListFilm[], minutes: number, record: FilmRecord): { films: ListFilm[]; seconds: number; from: number } {
  let from = queue.findIndex((f) => !isWatched(record, f.f));
  if (from === -1) from = 0;
  const films: ListFilm[] = [];
  let seconds = 0;
  for (const f of queue.slice(from)) {
    if (minutes && films.length && seconds + f.d > minutes * 60 + SLACK) break;
    films.push(f);
    seconds += f.d;
  }
  return { films, seconds, from };
}

export const clock = (sec: number) => `${Math.floor(sec / 60)}:${String(Math.round(sec % 60)).padStart(2, '0')}`.replace(/:60$/, ':59');
const n = (k: number, w: string) => `${k.toLocaleString('en-US')} ${w}${k === 1 ? '' : 's'}`;
/** "about 3 hours 45 minutes", "about 9 minutes". */
export function about(seconds: number): string {
  const m = Math.max(1, Math.round(seconds / 60));
  if (m < 60) return `about ${n(m, 'minute')}`;
  const h = Math.floor(m / 60);
  const r = Math.round((m % 60) / 5) * 5;
  return r === 60 ? `about ${n(h + 1, 'hour')}` : `about ${n(h, 'hour')}${r ? ` ${r} minutes` : ''}`;
}
export const filmsWord = (k: number) => n(k, 'film');
/** "3 films, 10 minutes. It ends after Which Way Does the Water Go?" (no second full stop after a
 *  title that ends its own sentence). */
export function runSentence(films: ListFilm[], seconds: number): string {
  const last = films[films.length - 1]?.t ?? '';
  return `${filmsWord(films.length)}, ${n(Math.max(1, Math.round(seconds / 60)), 'minute')}. It ends after ${last}${/[.?!]$/.test(last) ? '' : '.'}`;
}
