// The site's own list of levels, courses, lessons and films (src/pages/usage-catalog.json.ts),
// read through the ASSETS binding and kept in memory for ten minutes. The film counter and the
// owner's totals use it as an allow-list: a key that is not in it is never stored and never shown.

const URL_PATH = '/usage-catalog.json';
const KEEP_MS = 10 * 60_000;
let memo = null;

const isObj = (x) => !!x && typeof x === 'object' && !Array.isArray(x);

/** The raw file -> lookups. Anything not shaped as expected is left out. */
export function buildUsageCatalog(raw) {
  const levels = (Array.isArray(raw?.levels) ? raw.levels : []).filter((l) => Array.isArray(l) && typeof l[0] === 'string').map((l) => l[0]);
  const courses = new Map();   // slug -> level key
  for (const [slug, v] of Object.entries(isObj(raw?.courses) ? raw.courses : {})) {
    if (Array.isArray(v) && typeof v[1] === 'string') courses.set(slug, v[1]);
  }
  const lessons = new Map();   // slug -> course slug
  for (const [slug, v] of Object.entries(isObj(raw?.lessons) ? raw.lessons : {})) {
    if (Array.isArray(v) && typeof v[1] === 'string') lessons.set(slug, v[1]);
  }
  const films = new Set(Object.keys(isObj(raw?.films) ? raw.films : {}));
  return { levels, courses, lessons, films };
}

/** Throws when the file cannot be read; callers treat that as "know nothing" and fail closed. */
export async function loadUsageCatalog(env, request) {
  if (memo && Date.now() - memo.at < KEEP_MS) return memo.data;
  const res = await env.ASSETS.fetch(new Request(new URL(URL_PATH, request.url)));
  if (!res.ok) throw new Error(`usage catalog ${res.status}`);
  const data = buildUsageCatalog(await res.json());
  if (!data.films.size && !data.lessons.size) throw new Error('usage catalog empty');
  memo = { at: Date.now(), data };
  return data;
}

export const _resetUsageCatalog = () => { memo = null; };
