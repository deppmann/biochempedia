/* Films watched, on this device only (2026-11-14). No account.

   One thing does leave the device, and it says nothing about the viewer: the first time a film
   is started here, and the first time it is watched, the page tells the site's film counter
   which film (countFilm below; worker/film-count.js). The message carries the film and nothing
   else, is sent without cookies, and the counter keeps only a per-film, per-day tally.

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
     q   course slug -> the film and second the viewer was at in that course's play-in-order queue
     b   badges earned on this device (src/lib/badges.ts), keyed "<type>:<subject>" (2026-11-14) */

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
  /** The course's name, for "Pick up where you left off" on the homepage (from 2026-11-14). */
  course?: string;
}
export interface FilmRecord {
  v: 1;
  w: Record<string, number>;
  p: Partial[];
  q: Record<string, QueuePlace>;
  b?: Record<string, EarnedBadge>;
}
/** A badge earned on this device. What each type means lives in src/lib/badges.ts. */
export interface EarnedBadge {
  type: string;
  /** What it was earned for (a course slug) and that thing's name. */
  subject: string;
  subjectTitle: string;
  /** When it was earned (ms). */
  at: number;
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
  /** The film's length in seconds, for "about N min left" (from 2026-11-14). */
  d?: number;
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

// ---- the anonymous film count ---------------------------------------------------------------
/* Which films this device has already reported as started, so each is counted once per device:
   { v: 1, s: { filmKey: 1 } }. A film leaves the list once it is watched (the watched mark above
   then does the remembering). With storage blocked nothing is remembered, so a film counts once
   per page instead. */
const COUNTED_KEY = 'stemhop:films:counted:v1';
/** A film counts as started once it has played this many seconds. */
const STARTED_AT = 3;
const sentThisPage = new Set<string>();

function countedStarts(): Record<string, 1> {
  try {
    const r = JSON.parse(window.localStorage.getItem(COUNTED_KEY) ?? 'null');
    if (r && r.v === 1 && r.s && typeof r.s === 'object') return r.s;
  } catch { /* blocked or damaged */ }
  return {};
}
function saveCountedStarts(s: Record<string, 1>): void {
  try {
    if (Object.keys(s).length) window.localStorage.setItem(COUNTED_KEY, JSON.stringify({ v: 1, s }));
    else window.localStorage.removeItem(COUNTED_KEY);
  } catch { /* blocked */ }
}

/**
 * Tell the counter that a film was started ('s') or watched ('w') for the first time on this
 * device. Fire and forget: no cookies go with it (credentials "omit"), the answer is ignored, and
 * any failure is silent. A film watched without a counted start (the viewer skipped to the end)
 * is sent as both, so "watched" never runs ahead of "started".
 */
function countFilm(key: string, what: 's' | 'w'): void {
  if (sentThisPage.has(`${what}:${key}`)) return;
  sentThisPage.add(`${what}:${key}`);
  const starts = countedStarts();
  let e: 's' | 'w' | 'sw' = what;
  if (what === 's') {
    if (starts[key]) return;
    starts[key] = 1;
    saveCountedStarts(starts);
  } else {
    if (!starts[key] && !sentThisPage.has(`s:${key}`)) e = 'sw';
    sentThisPage.add(`s:${key}`);
    if (starts[key]) { delete starts[key]; saveCountedStarts(starts); }
  }
  if (import.meta.env?.DEV) return;   // the counter is part of the Worker, which `astro dev` does not run
  try {
    fetch('/api/film-count', {
      method: 'POST',
      credentials: 'omit',
      keepalive: true,
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ k: key, e }),
    }).catch(() => { /* offline or blocked: this one is not counted */ });
  } catch { /* no fetch: nothing to do */ }
}

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

/** Keep a badge, once: a badge already earned keeps its first date. Returns the stored badge. */
export function recordBadge(badge: EarnedBadge): EarnedBadge {
  const r = loadFilms();
  const id = `${badge.type}:${badge.subject}`;
  const had = r.b?.[id];
  if (had) return had;
  r.b = { ...(r.b ?? {}), [id]: badge };
  saveFilms(r, false);
  return badge;
}

/** Forget every film watched and every place saved (the "Clear everything" button on /progress/). */
export function clearFilms(): void {
  try { window.localStorage.removeItem(FILMS_KEY); window.localStorage.removeItem(COUNTED_KEY); } catch { /* nothing stored */ }
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
      if (!isWatched(loadFilms(), key)) { markWatched(key); countFilm(key, 'w'); }
      return;
    }
    // First few seconds played, for a film not watched here before: counted once as started.
    if (v.currentTime >= STARTED_AT && !sentThisPage.has(`s:${key}`)) {
      if (isWatched(loadFilms(), key)) sentThisPage.add(`s:${key}`);
      else countFilm(key, 's');
    }
    const now = Date.now();
    if (now - lastSave < 4000 || v.currentTime < 5 || !Number.isFinite(d)) return;
    lastSave = now;
    const title = v.dataset.filmTitle || v.dataset.listenFilm
      || v.closest('figure')?.querySelector('figcaption')?.textContent?.replace(/^\s*Watch\s+/, '').replace(/\s*·\s*\d+:\d+\s*$/, '').trim()
      || document.title.replace(/\s+—\s+STEMhop$/, '');
    const poster = v.getAttribute('poster') ?? '';
    const course = v.closest<HTMLElement>('[data-course-title]')?.dataset.courseTitle;
    savePartial({ f: key, t: Math.floor(v.currentTime), d: Math.round(d), title, href: hrefFor(key), poster, at: now, ...(course ? { course } : {}) });
  };
  document.addEventListener('timeupdate', onTime, true);
  document.addEventListener('ended', onTime, true);
}

/** The link back to an unfinished film, opening it paused at the second the viewer stopped
 *  (resumeFromLink below reads ?film= and ?at=). The play-in-order page reopens at its own saved place. */
export function resumeHref(x: Partial): string {
  if (x.href.startsWith('/films/play/') || x.t < 5) return x.href;
  const [path, hash = ''] = x.href.split('#');
  return `${path}${path.includes('?') ? '&' : '?'}film=${encodeURIComponent(x.f)}&at=${Math.floor(x.t)}${hash ? `#${hash}` : ''}`;
}

/**
 * ?film=<key>&at=<seconds> on a page with that film: load the film and set it to that second,
 * paused, and bring it into view. Nothing plays until the viewer presses play. Films inside a
 * pop-up (a scientist profile) are left alone.
 */
export function resumeFromLink(): void {
  const params = new URLSearchParams(location.search);
  const key = params.get('film');
  const at = Number(params.get('at'));
  if (!key || !Number.isFinite(at) || at <= 0) return;
  const v = [...document.querySelectorAll<HTMLVideoElement>('video')].find((x) => filmKeyOf(x.currentSrc || x.querySelector('source')?.src || '') === key);
  if (!v || v.closest('dialog')) return;
  const box = v.closest('details');
  if (box && !box.open) box.open = true;
  const seek = () => { if (at < v.duration - 2) v.currentTime = at; };
  if (v.readyState >= 1) seek();
  else { v.addEventListener('loadedmetadata', seek, { once: true }); v.preload = 'metadata'; v.load(); }
  v.scrollIntoView({ block: 'center' });
}
