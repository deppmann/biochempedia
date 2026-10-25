/* Browser-only learner progress. No account, no server, no personal data.

   Everything lives in one localStorage entry on this device. The page must work
   when storage is blocked (private windows, strict settings), so every read and
   write is wrapped and a failure just means "nothing remembered this visit".

   What is kept:
     path     the "I'm here for…" choice (an id from src/data/paths.ts)
     last     the last lesson opened, for "continue where you left off"
     lessons  slug -> { v: first visit, d?: marked done }   (timestamps, ms)
     items    question id -> review state for questions answered in a quiz

   Review schedule: a question missed on the first try comes back after 1 day.
   Each correct review moves it along 1 → 3 → 7 → 21 days; after the 21-day
   review it counts as mastered and leaves the queue. A miss in review starts
   it over at 1 day. */

export const STORAGE_KEY = 'biochempedia:progress:v1';
export const CHANGE_EVENT = 'bp-progress';
const DAY = 86_400_000;
/** Days until the next review, indexed by stage. Stage 4 = mastered. */
export const INTERVALS = [1, 3, 7, 21];

export interface ItemState {
  /** Lesson slug the question belongs to. */
  l: string;
  /** Times answered (first tries in a quiz plus reviews). */
  n: number;
  /** Times answered correctly. */
  c: number;
  /** Review stage: 0–3 waiting, 4 mastered. Absent = never missed. */
  s?: number;
  /** When it is next due (ms), absent when not in the queue. */
  due?: number;
  /** Last answered (ms). */
  t: number;
}

export interface Progress {
  v: 1;
  path?: string;
  last?: string;
  lessons: Record<string, { v: number; d?: number }>;
  items: Record<string, ItemState>;
}

const empty = (): Progress => ({ v: 1, lessons: {}, items: {} });

/** Short stable id for a question: lesson slug + a hash of its stem, so
 *  reordering a quiz keeps everyone's history attached to the right question. */
export function itemId(slug: string, stem: string): string {
  let h = 0x811c9dc5;
  for (let i = 0; i < stem.length; i++) {
    h ^= stem.charCodeAt(i);
    h = Math.imul(h, 0x01000193);
  }
  return `${slug}:${(h >>> 0).toString(36)}`;
}

function valid(p: unknown): p is Progress {
  return !!p && typeof p === 'object' && (p as Progress).v === 1
    && typeof (p as Progress).lessons === 'object' && typeof (p as Progress).items === 'object';
}

export function load(): Progress {
  try {
    const raw = window.localStorage.getItem(STORAGE_KEY);
    if (!raw) return empty();
    const p = JSON.parse(raw);
    return valid(p) ? p : empty();
  } catch {
    return empty();
  }
}

function save(p: Progress): boolean {
  try {
    window.localStorage.setItem(STORAGE_KEY, JSON.stringify(p));
  } catch {
    return false;
  }
  window.dispatchEvent(new CustomEvent(CHANGE_EVENT));
  return true;
}

function update(fn: (p: Progress) => void): Progress {
  const p = load();
  fn(p);
  save(p);
  return p;
}

export function setPath(id: string | null) {
  update((p) => { if (id) p.path = id; else delete p.path; });
}

export function markVisited(slug: string) {
  update((p) => {
    p.lessons[slug] ??= { v: Date.now() };
    p.last = slug;
  });
}

export function setDone(slug: string, done: boolean) {
  update((p) => {
    const rec = (p.lessons[slug] ??= { v: Date.now() });
    if (done) rec.d ??= Date.now(); else delete rec.d;
  });
}

/** A first try in a lesson quiz. A miss puts the question in the review queue. */
export function recordFirstTry(id: string, slug: string, correct: boolean) {
  update((p) => {
    const now = Date.now();
    const it = (p.items[id] ??= { l: slug, n: 0, c: 0, t: now });
    it.n++; it.t = now;
    if (correct) it.c++;
    // Only a miss changes the schedule; a correct first try on something already
    // queued leaves its review where it is.
    if (!correct) { it.s = 0; it.due = now + INTERVALS[0] * DAY; }
  });
}

/** An answer given in the review queue. */
export function recordReview(id: string, slug: string, correct: boolean) {
  update((p) => {
    const now = Date.now();
    const it = (p.items[id] ??= { l: slug, n: 0, c: 0, t: now });
    it.n++; it.t = now;
    if (correct) {
      it.c++;
      it.s = Math.min(4, (it.s ?? 0) + 1);
      if (it.s >= 4) delete it.due; else it.due = now + INTERVALS[it.s] * DAY;
    } else {
      it.s = 0; it.due = now + INTERVALS[0] * DAY;
    }
  });
}

/** Questions waiting in the queue, soonest first. `upTo` = include those due by then. */
export function queued(p: Progress, upTo = Infinity): [string, ItemState][] {
  return Object.entries(p.items)
    .filter(([, it]) => typeof it.due === 'number' && it.due <= upTo)
    .sort((a, b) => a[1].due! - b[1].due!);
}

export const dueNow = (p: Progress) => queued(p, Date.now());

export function exportText(): string {
  return JSON.stringify({ ...load(), exported: new Date().toISOString(), site: 'biochemistrypedia.com' }, null, 1);
}

/** Replace this device's progress with an exported file. Returns false if the file is not one of ours. */
export function importText(text: string): boolean {
  try {
    const p = JSON.parse(text);
    if (!valid(p)) return false;
    const { v, path, last, lessons, items } = p;
    return save({ v, path, last, lessons, items });
  } catch {
    return false;
  }
}

export function clearAll() {
  try { window.localStorage.removeItem(STORAGE_KEY); } catch { /* nothing stored */ }
  window.dispatchEvent(new CustomEvent(CHANGE_EVENT));
}

/** Run `fn` now and whenever progress changes, in this tab or another. */
export function onChange(fn: () => void) {
  fn();
  window.addEventListener(CHANGE_EVENT, fn);
  window.addEventListener('storage', (e) => { if (e.key === STORAGE_KEY || e.key === null) fn(); });
}
