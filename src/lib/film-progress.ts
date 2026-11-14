/* Films watched, on this device only (2026-11-14). No account, no server.

   One localStorage entry, separate from the learner progress record (src/lib/progress.ts), so it
   does not travel with a signed-in learner's sync; adding it there would need a merge rule on the
   server side too. Every read and write is wrapped: with storage blocked (a private window, strict
   settings) nothing is remembered and nothing breaks.

   A film is identified by its file: the path under /explainers/ without ".mp4", for example
   "action-potential/explainer" or "profiles/amino-acids-emil-fischer". The catalog lists each
   file once (src/lib/film-catalog.ts), so the key is unique, and the same key works on a lesson
   page, a /watch/ page, a method page and the play-in-order page.

   What is kept:
     w   key -> when it was first watched to about 90 percent (ms)
     p   the films started and not finished, newest first (at most 12): where the viewer stopped
     q   course slug -> the film and second the viewer was at in that course's play-in-order queue */

export const FILMS_KEY = 'biochempedia:films:v1';
export const FILMS_EVENT = 'bp-films';
/** Played this far, a film counts as watched. */
export const WATCHED_AT = 0.9;
const PARTIAL_MAX = 12;

export interface Partial {
  /** Film key. */
  f: string;
  /** Seconds in, and the film's length. */
  t: number;
  d: number;
  title: string;
  /** Where to go back to: the film's /watch/ page, its method page, the lesson page or the play page. */
  href: string;
  poster: string;
  at: number;
}
export interface FilmRecord {
  v: 1;
  w: Record<string, number>;
  p: Partial[];
  q: Record<string, QueuePlace>;
}
export interface QueuePlace {
  /** Film key and second, and when this was saved (ms). */
  f: string;
  t: number;
  at: number;
  /** For "Keep watching" on /films/: the film's title and poster, and the course's name. */
  title?: string;
  poster?: string;
  courseTitle?: string;
}

const empty = (): FilmRecord => ({ v: 1, w: {}, p: [], q: {} });

export function loadFilms(): FilmRecord {
  try {
    const r = JSON.parse(window.localStorage.getItem(FILMS_KEY) ?? 'null');
    if (r && r.v === 1 && typeof r.w === 'object' && Array.isArray(r.p) && typeof r.q === 'object') return r as FilmRecord;
  } catch { /* blocked or damaged: start empty */ }
  return empty();
}

function saveFilms(r: FilmRecord, notify = true): void {
  try {
    window.localStorage.setItem(FILMS_KEY, JSON.stringify(r));
  } catch {
    return;
  }
  if (notify) window.dispatchEvent(new CustomEvent(FILMS_EVENT));
}

/** "/explainers/action-potential/explainer.mp4" (or a full URL to it) -> "action-potential/explainer". */
export function filmKeyOf(src: string): string | null {
  let path = src;
  try { path = new URL(src, 'https://x.invalid').pathname; } catch { /* keep as given */ }
  const m = /^\/explainers\/(.+)\.mp4$/.exec(path);
  return m ? decodeURIComponent(m[1]) : null;
}

export const isWatched = (r: FilmRecord, key: string) => typeof r.w[key] === 'number';

export function markWatched(key: string): void {
  const r = loadFilms();
  r.w[key] ??= Date.now();
  r.p = r.p.filter((x) => x.f !== key);
  saveFilms(r);
}

function savePartial(entry: Partial): void {
  const r = loadFilms();
  r.p = [entry, ...r.p.filter((x) => x.f !== entry.f)].slice(0, PARTIAL_MAX);
  saveFilms(r, false);
}

/** The play-in-order page's place in a course's queue. */
export function saveQueue(course: string, place: Omit<QueuePlace, 'at'>): void {
  const r = loadFilms();
  r.q[course] = { ...place, t: Math.floor(place.t), at: Date.now() };
  saveFilms(r, false);
}

/** Forget every film watched and every place saved (the "Clear everything" button on /progress/). */
export function clearFilms(): void {
  try { window.localStorage.removeItem(FILMS_KEY); } catch { /* nothing stored */ }
  window.dispatchEvent(new CustomEvent(FILMS_EVENT));
}

/** Run `fn` now and whenever the record changes, in this tab or another. */
export function onFilmsChange(fn: () => void): void {
  fn();
  window.addEventListener(FILMS_EVENT, fn);
  window.addEventListener('storage', (e) => { if (e.key === FILMS_KEY || e.key === null) fn(); });
}

/** The newest film started and not finished, or null. */
export function keepWatching(r: FilmRecord): Partial | null {
  return r.p.find((x) => !isWatched(r, x.f) && x.t >= 5 && x.t < x.d * WATCHED_AT) ?? null;
}

/* Where "Keep watching" should send the viewer back to, worked out from the film's file. */
function hrefFor(key: string): string {
  const here = location.pathname;
  if (here.startsWith('/films/play/')) return here + location.search;
  const method = /^method-([^/]+)\/explainer$/.exec(key);
  if (method) return `/methods/${method[1]}/`;
  const lesson = /^([^/]+)\/([^/]+)$/.exec(key);
  if (lesson && lesson[1] !== 'profiles' && (here.startsWith('/watch/') || here.startsWith('/lessons/'))) {
    return lesson[2] === 'explainer' ? `/watch/${lesson[1]}/` : `/watch/${lesson[1]}/${lesson[2]}/`;
  }
  return here;
}

/* Films about the site itself (the homepage films, the teachers' talk) are not counted. */
const NOT_A_LIBRARY_FILM = /^(home|talk-deck|teachers-[^/]*)\//;

/**
 * Watch every <video> on the page with two listeners on the document (media events do not
 * bubble, but they can be caught on the way down). A film counts as watched at about 90 percent
 * or when it ends; until then, where the viewer stopped is saved every few seconds.
 */
export function trackFilms(): void {
  let lastSave = 0;
  const onTime = (e: Event) => {
    const v = e.target;
    if (!(v instanceof HTMLVideoElement)) return;
    const key = filmKeyOf(v.currentSrc || v.querySelector('source')?.src || '');
    if (!key || NOT_A_LIBRARY_FILM.test(key)) return;
    const d = v.duration;
    if (e.type === 'ended' || (Number.isFinite(d) && d > 0 && v.currentTime >= d * WATCHED_AT)) {
      if (!isWatched(loadFilms(), key)) markWatched(key);
      return;
    }
    const now = Date.now();
    if (now - lastSave < 4000 || v.currentTime < 5 || !Number.isFinite(d)) return;
    lastSave = now;
    const title = v.dataset.filmTitle || v.dataset.listenFilm
      || v.closest('figure')?.querySelector('figcaption')?.textContent?.replace(/^\s*Watch\s+/, '').replace(/\s*·\s*\d+:\d+\s*$/, '').trim()
      || document.title.replace(/\s+—\s+Biochemistrypedia$/, '');
    const poster = v.getAttribute('poster') ?? '';
    savePartial({ f: key, t: Math.floor(v.currentTime), d: Math.round(d), title, href: hrefFor(key), poster, at: now });
  };
  document.addEventListener('timeupdate', onTime, true);
  document.addEventListener('ended', onTime, true);
}
