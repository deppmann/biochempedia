/* Decisions the film pages make, as plain functions (2026-11-21), so they can be tested in Node
   without a browser (scripts/test-film-logic.mjs). The pages do the looking and the drawing; these
   say what should be in view.

   Used by src/lib/theater-client.ts (the theater on /watch/) and src/lib/film-run.ts (/films/run/). */
import { prepare, searchFilms, tokens } from './film-search.mjs';

/**
 * What the companion shows at second `t`.
 *   parts      [{ start }] for a film with a hand-checked map (in film order), else []
 *   questions  [{ start, until }]: the film asks at `start` and gives its answer at `until`
 *   ended      the film has played to its end
 * Returns { part, asking }: the index of the part being played (-1 with no parts) and the index of
 * the question the film is waiting on (-1 when it is not waiting). A question is up from the second
 * it is asked until the second its answer starts, and never once the film has ended.
 */
export function companionAt(t, parts, questions, ended = false) {
  let part = parts.length ? 0 : -1;
  parts.forEach((p, k) => { if (p.start <= t + 0.05) part = k; });
  let asking = -1;
  if (!ended) questions.forEach((q, k) => { if (t + 0.05 >= q.start && t < q.until) asking = k; });
  return { part, asking };
}

/**
 * Whether a panel that should change may change now, given where keyboard focus is.
 *   'none'   focus is outside the companion: change
 *   'link'   someone is on a link in the panel: hold it until they move on
 *   'pause'  focus is on the panel's own "Pause the film" button, left there by pressing it: change,
 *            and move focus to the companion first, so the button is never removed while focused
 * Returns { change, moveFocus }.
 */
export function swapRule(focus) {
  if (focus === 'link') return { change: false, moveFocus: false };
  return { change: true, moveFocus: focus === 'pause' };
}

/** The pause button's words, from the player's real state. Pressing it does what it says. */
export function pauseLabel({ paused, started }) {
  if (!paused) return 'Pause the film';
  return started ? 'Carry on' : 'Play the film';
}

/**
 * The films of a run and where it ends: whole films from index `from` of `queue`, while the next
 * would end no more than `slack` seconds past the budget; always at least one; stop at the first
 * that does not fit. With no budget, every film from `from`. Films are { f, d } (key, seconds).
 * @template {{ f: string, d: number }} T
 * @param {T[]} queue
 * @param {number} from
 * @param {number} minutes
 * @param {number} [slack]
 * @returns {{ films: T[], seconds: number }}
 */
export function runFilms(queue, from, minutes, slack = 60) {
  const films = [];
  let seconds = 0;
  for (const f of queue.slice(Math.max(0, from))) {
    if (minutes && films.length && seconds + f.d > minutes * 60 + slack) break;
    films.push(f);
    seconds += f.d;
  }
  return { films, seconds };
}

/**
 * Where a run opens: at its first film not yet watched on this device (the first film when all are
 * watched), and, when that film was left part-way, at the second it was left, paused.
 *   films     the run's films, [{ f, d }]
 *   watched   has(key) for films watched
 *   partials  [{ f, t, d }] films started and not finished
 * Returns { index, at }: `at` is 0 unless the film has a saved place at least 5 seconds in and
 * more than 2 seconds from its end.
 * @param {{ f: string, d: number }[]} films
 * @param {{ has(key: string): boolean }} watched
 * @param {{ f: string, t: number, d?: number }[]} [partials]
 */
export function runPlace(films, watched, partials = []) {
  let index = films.findIndex((f) => !watched.has(f.f));
  if (index === -1) index = 0;
  const film = films[index];
  const p = film && partials.find((x) => x.f === film.f);
  const at = p && p.t >= 5 && p.t < (film.d || p.d || 0) - 2 ? Math.floor(p.t) : 0;
  return { index, at };
}

/** A sentence that ends with a title: no second full stop after a title that ends its own sentence. */
export const endWith = (title) => `${title}${/[.?!]$/.test(title) ? '' : '.'}`;

/* ---- which films a view holds, and which of them a run plays. ONE matcher: the library draws what
   matchFilms() returns and the run plays runQueue() of the same arguments, so the two cannot
   disagree (they once did: the library searched the questions people ask and the run did not). */

const collator = new Intl.Collator('en', { sensitivity: 'base', numeric: true });
const COMPARE = {
  course: (a, b) => a.i - b.i,
  short: (a, b) => a.d - b.d || a.i - b.i,
  long: (a, b) => b.d - a.d || a.i - b.i,
  // Newest rewrites first; films whose lesson has no rewrite date follow, in course order.
  new: (a, b) => ((b.r ?? '') > (a.r ?? '') ? 1 : (b.r ?? '') < (a.r ?? '') ? -1 : 0) || a.i - b.i,
  az: (a, b) => collator.compare(a.t, b.t) || a.i - b.i,
};

/**
 * The films a view selects, in its order. `films` are the entries of /films/list.json; `view` is
 * { q, sort, level, course, kind }; `data` is /films/search.json (src/lib/film-search.mjs reads it),
 * or null when it is not loaded (a search then reads titles, lessons, courses and levels only). An
 * older map of lesson title -> question words is still accepted.
 * A search is read by src/lib/film-search.mjs: kind and level words act as filters, every other word
 * must be found somewhere in the film's record, best match first; films with all but one word follow.
 * With an order chosen ("Shortest first"), the full matches take that order and the partial ones follow.
 * The returned array carries `full`: how many of its films have every word (the rest are partial).
 * @template {{ f?: string, t: string, l?: string, s: string, c: string, k: string, d: number, i: number, r?: string }} T
 * @param {T[]} films
 * @param {{ q: string, sort: string, level: string, course: string, kind: string }} view
 * @param {any} [data]
 * @param {{ courses?: Record<string, string>, levels?: Record<string, string> }} [names] course and level titles, so they can be searched
 * @returns {T[] & { full: number }}
 */
export function matchFilms(films, view, data = null, names = {}) {
  const keep = (f) => (!view.level || f.s === view.level) && (!view.course || f.c === view.course);
  const q = String(view.q ?? '').trim();
  if (!q || !tokens(q).length) {
    const out = films.filter((f) => keep(f) && (!view.kind || f.k === view.kind));
    out.sort(COMPARE[view.sort] ?? COMPARE.course);
    return Object.assign(out, { full: out.length });
  }
  const index = prepare(listFor(films, names), searchDataFor(films, data));
  const r = searchFilms(index, q, { kind: view.kind, level: view.level, course: view.course });
  let out = r.films;
  if (view.sort && view.sort !== 'course' && COMPARE[view.sort]) out = [...out.slice(0, r.full).sort(COMPARE[view.sort]), ...out.slice(r.full)];
  return Object.assign([...out], { full: r.full });
}

/* The index is built once per film list: the same array (and names) gets the same wrapper. */
const lists = new WeakMap();
function listFor(films, names) {
  let l = lists.get(films);
  if (!l || l.courses !== names.courses || l.levels !== names.levels) lists.set(films, (l = { films, courses: names.courses, levels: names.levels }));
  return l;
}
/* An older ideas map ({ lesson title: words }) as search data. */
const legacy = new WeakMap();
function searchDataFor(films, data) {
  if (!data || data.v) return data;
  let d = legacy.get(data);
  if (d) return d;
  const lessons = [];
  const at = new Map();
  const out = {};
  films.forEach((f) => {
    if (!f.l || !data[f.l]) return;
    if (!at.has(f.l)) { at.set(f.l, lessons.length); lessons.push({ w: data[f.l] }); }
    out[f.f] = { L: at.get(f.l) };
  });
  d = { v: 1, fields: {}, lessons, films: out };
  legacy.set(data, d);
  return d;
}

/**
 * The films of a view that a run plays, in the view's order: lesson films (with a page of their own
 * under /watch/) and method films (since 2026-11-22: "neuroscience methods" plays), not scientist
 * profiles, which open in their lesson, and without the ages 5 to 10 films,
 * which show a grown-up how to set up an activity, unless that level or kind was asked for or the
 * view holds nothing else.
 * @template {{ h: string, k: string }} T
 * @param {T[]} matched
 * @param {{ level: string, kind: string }} view
 * @returns {T[]}
 */
export function runnableFilms(matched, view) {
  const young = view.level === 'ages-5-10' || view.kind === 'activity' || matched.every((f) => f.k === 'activity');
  return matched.filter((f) => (f.h.startsWith('/watch/') || f.k === 'method') && (young || f.k !== 'activity'));
}

/** What a run of a view plays: runnableFilms(matchFilms(...)). The library's offer and /films/run/ both call this.
 * @template {{ t: string, l?: string, s: string, c: string, k: string, d: number, i: number, r?: string, h: string }} T
 * @param {T[]} films
 * @param {{ q: string, sort: string, level: string, course: string, kind: string }} view
 * @param {any} [ideas] /films/search.json (or an older lesson-title map), or null
 * @param {{ courses?: Record<string, string>, levels?: Record<string, string> }} [names]
 * @returns {T[]}
 */
export const runQueue = (films, view, ideas = null, names = {}) => {
  const m = matchFilms(films, view, ideas, names);
  // A run plays the films with every word; partial matches only when nothing has them all.
  return runnableFilms(m.full ? m.slice(0, m.full) : m, view);
};
