/* Decisions the film pages make, as plain functions (2026-11-21), so they can be tested in Node
   without a browser (scripts/test-film-logic.mjs). The pages do the looking and the drawing; these
   say what should be in view.

   Used by src/lib/theater-client.ts (the theater on /watch/) and src/lib/film-run.ts (/films/run/). */

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

const fold = (s) => String(s).normalize('NFD').replace(/[\u0300-\u036f]/g, '').toLowerCase();
const LITTLE = new Set('a an and are as at be by can do does for from how in into is it its of on or so that the their then there this to was what when where which who why will with your you'.split(' '));
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
 * { q, sort, level, course, kind }; `ideas` maps a lesson title to the words of the questions people
 * ask about it (/films/ideas.json), or is null when that file is not loaded.
 * A search matches when every word is in the film's title or its lesson's title, or starts a word
 * among the lesson's questions; films matched by title come first.
 * @template {{ t: string, l?: string, s: string, c: string, k: string, d: number, i: number, r?: string }} T
 * @param {T[]} films
 * @param {{ q: string, sort: string, level: string, course: string, kind: string }} view
 * @param {Record<string, string> | null} [ideas]
 * @returns {T[]}
 */
export function matchFilms(films, view, ideas = null) {
  // Little words carry no idea ("why do cells swell in water" is cells, swell, water), unless the
  // search is nothing but little words.
  const typed = fold(view.q).split(/[^a-z0-9]+/).filter((w) => w.length > 1 || /\d/.test(w));
  const kept = typed.filter((w) => !LITTLE.has(w));
  const words = kept.length ? kept : typed;
  const byTitle = new Set();
  const out = films.filter((f) => {
    if (view.level && f.s !== view.level) return false;
    if (view.course && f.c !== view.course) return false;
    if (view.kind && f.k !== view.kind) return false;
    if (!words.length) return true;
    const title = fold(`${f.t} ${f.l ?? ''}`);
    if (words.every((w) => title.includes(w))) { byTitle.add(f); return true; }
    // Against the questions people ask, a word must start a word ("atp" is not found inside "adaptation").
    const idea = f.l && ideas ? ` ${title.replace(/[^a-z0-9]+/g, ' ')} ${ideas[f.l] ?? ''}` : '';
    return !!idea && words.every((w) => idea.includes(` ${w}`));
  });
  out.sort(COMPARE[view.sort] ?? COMPARE.course);
  if (words.length && byTitle.size && byTitle.size < out.length) return [...out.filter((f) => byTitle.has(f)), ...out.filter((f) => !byTitle.has(f))];
  return out;
}

/**
 * The films of a view that a run plays, in the view's order: those with a page of their own under
 * /watch/ (scientist profiles and method films open elsewhere), and without the ages 5 to 10 films,
 * which show a grown-up how to set up an activity, unless that level or kind was asked for or the
 * view holds nothing else.
 * @template {{ h: string, k: string }} T
 * @param {T[]} matched
 * @param {{ level: string, kind: string }} view
 * @returns {T[]}
 */
export function runnableFilms(matched, view) {
  const young = view.level === 'ages-5-10' || view.kind === 'activity' || matched.every((f) => f.k === 'activity');
  return matched.filter((f) => f.h.startsWith('/watch/') && (young || f.k !== 'activity'));
}

/** What a run of a view plays: runnableFilms(matchFilms(...)). The library's offer and /films/run/ both call this.
 * @template {{ t: string, l?: string, s: string, c: string, k: string, d: number, i: number, r?: string, h: string }} T
 * @param {T[]} films
 * @param {{ q: string, sort: string, level: string, course: string, kind: string }} view
 * @param {Record<string, string> | null} [ideas]
 * @returns {T[]}
 */
export const runQueue = (films, view, ideas = null) => runnableFilms(matchFilms(films, view, ideas), view);
