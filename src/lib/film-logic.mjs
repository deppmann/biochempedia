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
