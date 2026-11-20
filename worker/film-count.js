// The film counter: POST /api/film-count
//
// A count of how many times each film is started and how many times it is watched to the end,
// across everyone, so the site's owner can see which films are used (worker/admin.js). The page
// sends one small message the first time a film starts on a device and one the first time it is
// watched there (src/lib/film-progress.ts).
//
//   POST /api/film-count   {k: "<film key>", e: "s" | "w" | "sw"}   -> 204, always
//
// WHAT IS KEPT: one row per film per day with two numbers (film_counts, migration 0009):
// film key, day, started, watched. Nothing else.
//
// WHAT IS NOT: this file never reads a cookie, never looks up an account, a class or a student,
// and writes no log line. The page sends the message without cookies at all (credentials "omit"),
// so there is nothing here to look anyone up with. A row holds no address, no device and no time
// of day, so it is not possible to work out from the table who watched what.
//
// The one thing held about the sender is the rate limit, as everywhere else on the site: a count
// per connection under a one-way hash of the IP address, salted so it cannot be matched to any
// other table, deleted within a day (worker/util.js allow()). It records how many messages came
// from that connection, never which films.
//
// The answer is the same 204 whatever happens (counted, unknown film, over the limit, table not
// there yet), so the route tells a caller nothing and the page never has to handle a failure.
// Until migration 0009 is applied the table does not exist and nothing at all is written.

import { sha256Hex } from './auth.js';
import { DAY, fail, sameOrigin, allow } from './util.js';
import { loadUsageCatalog } from './usage-catalog.js';

export const FILM_COUNT_PATH = '/api/film-count';
// A school shares one address, and a class starting a film together sends a message each, so the
// per-connection limits are roomy. The site-wide one is a backstop for the database.
const PER_MIN = 120;
const PER_DAY = 4000;
const SITE_PER_MIN = 1500;
const MAX_BODY = 400;
const EVENTS = { s: [1, 0], w: [0, 1], sw: [1, 1] };

const quiet = () => new Response(null, { status: 204, headers: { 'Cache-Control': 'no-store' } });

// Does the table exist? Asked of the database itself, so the day the migration is applied the
// counter starts with no deploy. "Yes" is remembered for good, "no" for a minute.
const ready = new WeakMap();
export async function filmCountsReady(db) {
  const m = ready.get(db);
  if (m && (m.yes || Date.now() - m.at < 60_000)) return m.yes;
  let yes = false;
  try { await db.prepare('SELECT 1 FROM film_counts LIMIT 0').first(); yes = true; } catch { yes = false; }
  ready.set(db, { yes, at: Date.now() });
  return yes;
}

export async function handleFilmCount(request, env) {
  if (request.method !== 'POST') return fail(404, 'Not found.');
  if (!sameOrigin(request)) return fail(403, 'Bad request origin.');
  // The message is tiny. Anything bigger is dropped, measured here and not taken from a header.
  if (Number(request.headers.get('Content-Length') || 0) > MAX_BODY) return quiet();
  let b = null;
  try { const text = await request.text(); if (text.length <= MAX_BODY) b = JSON.parse(text); } catch { /* not JSON: dropped below */ }
  const key = typeof b?.k === 'string' && b.k.length <= 200 ? b.k : '';
  const add = typeof b?.e === 'string' && Object.hasOwn(EVENTS, b.e) ? EVENTS[b.e] : null;
  const db = env.CLASSES;
  if (!key || !add || !db) return quiet();
  try {
    if (!(await filmCountsReady(db))) return quiet();
    // Only a film the site really has. This is what keeps junk, and anything a person typed, out of the table.
    const catalog = await loadUsageCatalog(env, request);
    if (!catalog.films.has(key)) return quiet();
    const ip = await sha256Hex('film|' + (request.headers.get('CF-Connecting-IP') || 'local'));
    if (!(await allow(db, `film:m:${ip}`, PER_MIN, 60_000))) return quiet();
    if (!(await allow(db, `film:d:${ip}`, PER_DAY, DAY))) return quiet();
    if (!(await allow(db, 'film:g:min', SITE_PER_MIN, 60_000))) return quiet();
    await db.prepare(
      `INSERT INTO film_counts (film_key, day, started, watched) VALUES (?1, ?2, ?3, ?4)
         ON CONFLICT (film_key, day) DO UPDATE SET started = started + excluded.started, watched = watched + excluded.watched`)
      .bind(key, new Date().toISOString().slice(0, 10), add[0], add[1]).run();
  } catch { /* a count is never worth an error on someone's page */ }
  return quiet();
}
