/* What a visitor has told the site about themselves, on this device only.

   One localStorage entry, `stemhop:prefs:v1`, a JSON object with up to three optional fields:

     role    'student' | 'parent' | 'teacher'
     level   a stage key from src/data/stages.ts ('ages-5-10', 'grade-7', 'high-school',
             'starting-college', 'college-core', 'college-further', 'graduate')
     time    how much the reader wants from a lesson right now (the lesson page defines the values)

   Rules for every page that uses it:
   - It is a hint for picking a sensible default. Every page must work when it is missing, and
     no page may nag for it.
   - Wherever a preference is shown, the reader can change or clear it there.
   - It stays on this device. Nothing here sends it anywhere, and nothing in this entry may ever
     be sent to the server or stored with an account: a level such as "grade-7" says roughly how
     old a child is, and the site promises to ask accounts for no age, grade or school.
   - It is set only by the visitor's own choice on the page that shows it. The optional role on a
     learner account (src/lib/learner.ts) is a separate thing and is never copied in here.
   - "Clear everything" must clear it: call clearPrefs().
   - Every read and write is wrapped: with storage blocked (a private window, strict settings)
     nothing is remembered and nothing breaks.

   Fields this file does not know are kept as they are on a write, so a newer page's field
   survives an older page's save. */

export const PREFS_KEY = 'stemhop:prefs:v1';
/** Fired on `window` after a change in this tab. Other tabs hear the browser's own "storage" event. */
export const PREFS_EVENT = 'stemhop:prefs';

export const ROLES = ['student', 'parent', 'teacher'] as const;
export type Role = (typeof ROLES)[number];

export interface Prefs {
  role?: Role;
  level?: string;
  time?: string;
}

const KEYISH = /^[a-z0-9][a-z0-9-]{0,39}$/;
export const isRole = (x: unknown): x is Role => typeof x === 'string' && (ROLES as readonly string[]).includes(x);

function raw(): Record<string, unknown> {
  try {
    const o = JSON.parse(window.localStorage.getItem(PREFS_KEY) ?? 'null');
    return o && typeof o === 'object' && !Array.isArray(o) ? o : {};
  } catch {
    return {};   // blocked, missing or damaged: no preferences
  }
}

/** The stored preferences, with anything malformed left out. Never throws. */
export function readPrefs(): Prefs {
  const o = raw();
  const out: Prefs = {};
  if (isRole(o.role)) out.role = o.role;
  if (typeof o.level === 'string' && KEYISH.test(o.level)) out.level = o.level;
  if (typeof o.time === 'string' && KEYISH.test(o.time)) out.time = o.time;
  return out;
}

/**
 * Change some preferences and keep the rest. `null` or `undefined` for a field clears it.
 * Returns what is now stored (or, with storage blocked, what would have been). Never throws.
 */
export function writePrefs(patch: { [K in keyof Prefs]?: Prefs[K] | null }): Prefs {
  const next = raw();
  for (const [k, v] of Object.entries(patch)) {
    if (v === null || v === undefined || v === '') delete next[k];
    else next[k] = v;
  }
  try {
    if (Object.keys(next).length) window.localStorage.setItem(PREFS_KEY, JSON.stringify(next));
    else window.localStorage.removeItem(PREFS_KEY);
  } catch { /* storage blocked: the choice lasts for this page only */ }
  try { window.dispatchEvent(new CustomEvent(PREFS_EVENT)); } catch { /* no window events */ }
  return readPrefs();
}

/** Forget every preference on this device. */
export function clearPrefs(): void {
  try { window.localStorage.removeItem(PREFS_KEY); } catch { /* nothing stored */ }
  try { window.dispatchEvent(new CustomEvent(PREFS_EVENT)); } catch { /* no window events */ }
}

/** Run `fn` now and whenever the preferences change, in this tab or another. Returns a function that stops it. */
export function onPrefsChange(fn: (p: Prefs) => void): () => void {
  const run = () => fn(readPrefs());
  const onStorage = (e: StorageEvent) => { if (e.key === PREFS_KEY || e.key === null) run(); };
  run();
  try {
    window.addEventListener(PREFS_EVENT, run);
    window.addEventListener('storage', onStorage);
  } catch { /* no window events */ }
  return () => {
    try {
      window.removeEventListener(PREFS_EVENT, run);
      window.removeEventListener('storage', onStorage);
    } catch { /* nothing to remove */ }
  };
}
