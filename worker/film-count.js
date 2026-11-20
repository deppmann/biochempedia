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
// The request itself reaches the site like any other request (an address, a browser name), and
// the page asks the browser not to say which page it was on (referrerPolicy "no-referrer").
//
// The one thing held about the sender is the rate limit, as everywhere else on the site: a count
// per connection under a one-way hash of the IP address, deleted within a day (worker/util.js
// allow()). It records how many messages came from that connection, never which films. The hash
// is keyed with a Worker secret when one is set (RATE_SALT if present, else ADMIN_TOKEN or
// KEY_ENCRYPTION_KEY), so someone holding the table cannot find an address by hashing every
// possible one. With no secret set it falls back to a fixed prefix, which only keeps these keys
// apart from other tables' and can be reversed by trying every address; set one of the secrets.
//
// NOT EXACT. Anyone can post to this route, so the counts can be pushed up by a script, and a
// flood can use up the site-wide allowance so that honest views in that minute are not counted.
// The limits below bound the damage; they cannot prevent it. The owner's page says so.
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
const PER_DAY = 1500;
const SITE_PER_MIN = 1500;
const MAX_BODY = 400;
const SITE_TZ = 'America/New_York';

/** The site's day, YYYY-MM-DD in US Eastern time: what a film_counts row is filed under. */
export const siteDay = (ms = Date.now()) => new Date(ms).toLocaleDateString('en-CA', { timeZone: SITE_TZ });

/** At most MAX_BODY bytes of the body as text, or null. Stops reading as soon as it is too long. */
async function smallBody(request) {
  if (!request.body) return '';
  const reader = request.body.getReader();
  const parts = [];
  let size = 0;
  try {
    for (;;) {
      const { done, value } = await reader.read();
      if (done) break;
      size += value.byteLength;
      if (size > MAX_BODY) { await reader.cancel().catch(() => {}); return null; }
      parts.push(value);
    }
  } catch { return null; }
  const all = new Uint8Array(size);
  let at = 0;
  for (const p of parts) { all.set(p, at); at += p.byteLength; }
  return new TextDecoder().decode(all);
}
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

/** The rate-limit key for this connection: a one-way hash of the address, keyed with a Worker secret when there is one. */
export async function filmClientKey(request, env) {
  const salt = env.RATE_SALT || env.ADMIN_TOKEN || env.KEY_ENCRYPTION_KEY || '';
  return sha256Hex(`film|${salt}|${request.headers.get('CF-Connecting-IP') || 'local'}`);
}

export async function handleFilmCount(request, env) {
  if (request.method !== 'POST') return fail(404, 'Not found.');
  if (!sameOrigin(request)) return fail(403, 'Bad request origin.');
  // The message is tiny. Anything bigger is dropped, and the reading stops at the limit, so a
  // body with no stated length cannot make the Worker hold more than this.
  if (Number(request.headers.get('Content-Length') || 0) > MAX_BODY) return quiet();
  let b = null;
  try { const text = await smallBody(request); if (text !== null) b = JSON.parse(text); } catch { /* not JSON: dropped below */ }
  const key = typeof b?.k === 'string' && b.k.length <= 200 ? b.k : '';
  const add = typeof b?.e === 'string' && Object.hasOwn(EVENTS, b.e) ? EVENTS[b.e] : null;
  const db = env.CLASSES;
  if (!key || !add || !db) return quiet();
  try {
    if (!(await filmCountsReady(db))) return quiet();
    // Only a film the site really has. This is what keeps junk, and anything a person typed, out of the table.
    const catalog = await loadUsageCatalog(env, request);
    if (!catalog.films.has(key)) return quiet();
    // The site-wide allowance first: once it is used up, a flood from fresh addresses costs one row update each, not new rows.
    if (!(await allow(db, 'film:g:min', SITE_PER_MIN, 60_000))) return quiet();
    const ip = await filmClientKey(request, env);
    if (!(await allow(db, `film:m:${ip}`, PER_MIN, 60_000))) return quiet();
    if (!(await allow(db, `film:d:${ip}`, PER_DAY, DAY))) return quiet();
    await db.prepare(
      `INSERT INTO film_counts (film_key, day, started, watched) VALUES (?1, ?2, ?3, ?4)
         ON CONFLICT (film_key, day) DO UPDATE SET started = started + excluded.started, watched = watched + excluded.watched`)
      .bind(key, siteDay(), add[0], add[1]).run();
  } catch { /* a count is never worth an error on someone's page */ }
  return quiet();
}
