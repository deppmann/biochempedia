// The owner's totals: GET /api/admin/stats
//
// How the site is used, for the one person who runs it. Counts only. The page that shows them is
// /admin/ (src/pages/admin/index.astro), a plain static page; this route is the only gated part.
//
// THE GATE. A Worker secret, ADMIN_TOKEN (`npx wrangler secret put ADMIN_TOKEN`; it is never in
// the repository or in wrangler.jsonc). It must arrive in an "Authorization: Bearer ..." header.
//   - Secret not set, shorter than 24 characters, wrong, or missing: the route answers exactly
//     what any unknown /api/ path answers (404 "Not found."), so it does not show that it exists.
//     It does that by returning null and letting worker/api.js fall through to its own 404.
//   - A request with ANY query string is refused the same way, even with the right header.
//     Cloudflare's request log records web addresses, so a secret must never ride in one. If the
//     real secret does turn up in a query string, a warning is logged (without the value) so the
//     owner knows to replace it.
//   - The comparison is constant-time (both sides are hashed first, so length is not leaked).
//   - Twenty requests a minute per connection, counted as everywhere else; over that, 404.
//   - Cache-Control: no-store, no CORS headers, GET only.
//
// AGGREGATES ONLY, BY CONSTRUCTION. Every SQL statement below is a COUNT or a SUM, most with a
// GROUP BY on a fixed column. No statement selects a name, an email, a nickname, an answer, a
// note, a class or group name, a code or an id, so no row about a person or a class is ever read
// into the Worker, let alone sent. The only strings in the reply are dates and the site's own
// keys for levels, courses, lessons and films, and each key is checked against the site's
// catalog (worker/usage-catalog.js) before it is used: a "course" or "lesson" that somebody
// typed is counted under "other" or dropped, never echoed.
//
// THE SMALL-CELL RULE (K = 5). A count of 1, 2, 3 or 4 can point at a person or at one class.
//   1. Whole-site totals of one kind of thing are shown as they are, however small: learner
//      accounts, teachers, classes, class seats, how many were active in 7 or 30 days, and how
//      many were made each week. They carry no attribute, so they say nothing about anyone.
//   2. Any count that describes a SUBGROUP is a cell: by role, by sign-in method, by course, by
//      level, by join mode, by lesson, with or without notes, and so on. A cell of 1 to 4 is
//      sent as null (the page prints "under 5"). Zero is sent as 0.
//   3. Cells that add up to a published total could be worked out by subtraction. So when
//      exactly one cell of a split is hidden, the next smallest is hidden too, and when the
//      whole split adds up to 1 to 4, every cell is hidden. Classes by course sit inside classes
//      by level, and the same is done one level down (a hidden level hides its courses).
//   4. Role is never crossed with anything: not with time, not with lessons, not with films.
//   5. Per-lesson lists (opened or finished by signed-in learners, assigned by classes) include
//      only lessons with at least 5; the reply says how many lessons were left out, not which.
//   6. Film counts are not cells. A film_counts row holds a film, a day and two numbers and was
//      never tied to an account, a class or a device (worker/film-count.js), so there is nobody
//      a small number could point at. They are sent as they are. The same goes for the
//      curiosity router's daily call counts, which were always anonymous.
//
// NEVER SUMMED: learner accounts, teacher accounts and class seats are three separate things.
// One person can be in two of them, and nothing links the rows, so adding them would count
// people twice. They are reported as separate lines.

import { sha256Hex } from './auth.js';
import { DAY, json, clientKey, allow } from './util.js';
import { loadUsageCatalog } from './usage-catalog.js';
import { filmCountsReady } from './film-count.js';
import { roleReady } from './learner.js';

export const ADMIN_PATH = '/api/admin/stats';
export const SMALL = 5;
const MIN_SECRET = 24;
const WEEK = 7 * DAY;
const WEEKS = 26;
const DAYS = 30;
const PER_MIN = 20;

// ---- the gate ---------------------------------------------------------------------------
async function sameSecret(a, b) {
  const [x, y] = await Promise.all([sha256Hex(a), sha256Hex(b)]);
  let diff = 0;
  for (let i = 0; i < x.length; i++) diff |= x.charCodeAt(i) ^ y.charCodeAt(i);
  return diff === 0;
}

export const adminSecret = (env) => {
  const s = typeof env.ADMIN_TOKEN === 'string' ? env.ADMIN_TOKEN.trim() : '';
  return s.length >= MIN_SECRET ? s : '';
};

// ---- small cells ------------------------------------------------------------------------
const int = (v) => (Number.isFinite(Number(v)) ? Math.max(0, Math.round(Number(v))) : 0);
/** One cell: 1 to 4 is hidden. */
export const cell = (n) => (n >= 1 && n < SMALL ? null : int(n));

/** Cells that add up to a published total (rule 3). */
export function split(cells) {
  const keys = Object.keys(cells);
  const total = keys.reduce((s, k) => s + int(cells[k]), 0);
  const out = {};
  for (const k of keys) out[k] = total >= 1 && total < SMALL ? null : cell(int(cells[k]));
  const hidden = keys.filter((k) => out[k] === null);
  if (hidden.length === 1) {
    const rest = keys.filter((k) => out[k] !== null).sort((a, b) => out[a] - out[b] || (a < b ? -1 : 1));
    if (rest.length) out[rest[0]] = null;
  }
  return out;
}

/** A split inside a split: courses inside levels. `parentOf(key)` gives a cell's level. */
export function nestedSplit(cells, parentOf) {
  const parents = {};
  for (const [k, n] of Object.entries(cells)) parents[parentOf(k)] = (parents[parentOf(k)] || 0) + int(n);
  const byParent = split(parents);
  const byChild = {};
  for (const p of Object.keys(parents)) {
    const mine = Object.fromEntries(Object.entries(cells).filter(([k]) => parentOf(k) === p));
    if (byParent[p] === null) for (const k of Object.keys(mine)) byChild[k] = null;
    else Object.assign(byChild, split(mine));
  }
  return { byParent, byChild };
}

/** A per-lesson list: only rows with at least SMALL, and how many were left out. */
function listed(rows, known, extra = () => ({})) {
  const list = [];
  let hidden = 0;
  for (const r of rows) {
    if (!known.has(r.slug)) continue;
    const n = int(r.n);
    if (n >= SMALL) list.push({ slug: r.slug, n, ...extra(r, n) });
    else if (n >= 1) hidden++;
  }
  list.sort((a, b) => b.n - a.n || (a.slug < b.slug ? -1 : 1));
  return { list: list.slice(0, 200), hidden };
}

// ---- reading the database ---------------------------------------------------------------
// A table or column that is not there yet (a migration not applied) gives null, not an error.
async function rows(db, sql, ...args) {
  try { return (await db.prepare(sql).bind(...args).all()).results || []; } catch { return null; }
}
async function one(db, sql, ...args) {
  try { return (await db.prepare(sql).bind(...args).first()) || {}; } catch { return null; }
}
const count = async (db, sql, ...args) => { const r = await one(db, sql, ...args); return r ? int(r.n) : null; };

/** Monday 00:00 UTC of the week holding `ms`. */
const weekStart = (ms) => { const d = Math.floor(ms / DAY); return (d - ((d + 3) % 7)) * DAY; };
const isoDay = (ms) => new Date(ms).toISOString().slice(0, 10);

/** How many rows of `table` were made in each of the last 26 weeks (a whole-site series, rule 1). */
async function byWeek(db, table, col, now) {
  const first = weekStart(now) - (WEEKS - 1) * WEEK;
  const got = await rows(db, `SELECT CAST((${col} - ?1) / ${WEEK} AS INTEGER) AS w, COUNT(*) AS n FROM ${table} WHERE ${col} >= ?1 GROUP BY w`, first);
  if (!got) return null;
  const n = new Map(got.map((r) => [int(r.w), int(r.n)]));
  return Array.from({ length: WEEKS }, (_, i) => ({ week: isoDay(first + i * WEEK), n: n.get(i) || 0 }));
}

// ---- the numbers ------------------------------------------------------------------------
export async function buildStats(db, env, request, now = Date.now()) {
  let catalog = { levels: [], courses: new Map(), lessons: new Map(), films: new Set() };
  try { catalog = await loadUsageCatalog(env, request); } catch { /* no catalog: totals only, nothing named */ }
  const d7 = now - 7 * DAY, d30 = now - 30 * DAY;
  const day30 = isoDay(now - (DAYS - 1) * DAY), day7 = isoDay(now - 6 * DAY);

  // Learner accounts.
  const learnersTotal = await count(db, 'SELECT COUNT(*) AS n FROM learners');
  const hasRole = await roleReady(db);
  const roleRows = hasRole ? await rows(db, "SELECT COALESCE(role, 'unset') AS k, COUNT(*) AS n FROM learners GROUP BY k") : null;
  const roleOf = (k) => int(roleRows?.find((r) => r.k === k)?.n);
  const how = await one(db,
    `SELECT SUM(CASE WHEN g = 1 AND p = 0 THEN 1 ELSE 0 END) AS google, SUM(CASE WHEN g = 0 AND p = 1 THEN 1 ELSE 0 END) AS passkey,
            SUM(CASE WHEN g = 1 AND p = 1 THEN 1 ELSE 0 END) AS both, SUM(CASE WHEN g = 0 AND p = 0 THEN 1 ELSE 0 END) AS neither
       FROM (SELECT (l.google_sub IS NOT NULL) AS g, EXISTS (SELECT 1 FROM learner_passkeys k WHERE k.learner_id = l.id) AS p FROM learners l)`);
  const withNotes = await count(db, "SELECT COUNT(*) AS n FROM learner_data WHERE notebook_json NOT IN ('{}', '')");
  const SAFE = "CASE WHEN json_valid(d.progress_json) THEN d.progress_json ELSE '{}' END";
  const withProgress = await count(db, `SELECT COUNT(*) AS n FROM learner_data d WHERE EXISTS (SELECT 1 FROM json_each(${SAFE}, '$.lessons'))`);
  const twoWay = (yes) => (learnersTotal === null || yes === null ? null : split({ yes, no: Math.max(0, learnersTotal - yes) }));
  const learners = learnersTotal === null ? null : {
    total: learnersTotal,
    active7: await count(db, 'SELECT COUNT(*) AS n FROM learners WHERE last_active_at >= ?', d7),
    active30: await count(db, 'SELECT COUNT(*) AS n FROM learners WHERE last_active_at >= ?', d30),
    newByWeek: await byWeek(db, 'learners', 'created_at', now),
    role: roleRows ? split({ student: roleOf('student'), parent: roleOf('parent'), teacher: roleOf('teacher'), unset: roleOf('unset') }) : null,
    signIn: how ? split({ google: int(how.google), passkey: int(how.passkey), both: int(how.both), neither: int(how.neither) }) : null,
    withNotes: twoWay(withNotes),
    withProgress: twoWay(withProgress),
  };

  // Lessons, across signed-in learners (their synced progress). One row per lesson: how many
  // learners have it at all, and how many have it marked done.
  const lessonRows = await rows(db,
    `SELECT j.key AS slug, COUNT(*) AS n,
            SUM(CASE WHEN j.type = 'object' AND json_extract(j.value, '$.d') IS NOT NULL THEN 1 ELSE 0 END) AS done
       FROM learner_data d, json_each(${SAFE}, '$.lessons') j GROUP BY j.key`);
  let lessons = null;
  if (lessonRows) {
    const known = lessonRows.filter((r) => catalog.lessons.has(r.slug));
    const l = listed(known, catalog.lessons, (r, n) => ({ finished: split({ yes: int(r.done), no: Math.max(0, n - int(r.done)) }).yes }));
    lessons = {
      opens: known.reduce((s, r) => s + int(r.n), 0),
      finishes: known.reduce((s, r) => s + int(r.done), 0),
      opened: l.list.map(({ slug, n, finished }) => ({ slug, opened: n, finished })),
      hidden: l.hidden,
    };
  }

  // Teachers, classes and class seats: three more separate lines.
  const teachersTotal = await count(db, 'SELECT COUNT(*) AS n FROM teachers');
  const verified = await count(db, 'SELECT COUNT(*) AS n FROM teachers WHERE email_verified_at IS NOT NULL');
  const withClass = await count(db, 'SELECT COUNT(DISTINCT teacher_id) AS n FROM classes');
  const teachers = teachersTotal === null ? null : {
    total: teachersTotal,
    newByWeek: await byWeek(db, 'teachers', 'created_at', now),
    verified: verified === null ? null : split({ yes: verified, no: Math.max(0, teachersTotal - verified) }),
    withClass: withClass === null ? null : split({ yes: withClass, no: Math.max(0, teachersTotal - withClass) }),
    withActiveClass30: await count(db, 'SELECT COUNT(DISTINCT teacher_id) AS n FROM classes WHERE last_activity_at >= ?', d30),
  };

  const classesTotal = await count(db, 'SELECT COUNT(*) AS n FROM classes');
  let classes = null;
  if (classesTotal !== null) {
    const courseCells = {};
    for (const r of (await rows(db, 'SELECT course AS k, COUNT(*) AS n FROM classes GROUP BY course')) || []) {
      const k = catalog.courses.has(r.k) ? r.k : 'other';
      courseCells[k] = (courseCells[k] || 0) + int(r.n);
    }
    const nest = nestedSplit(courseCells, (k) => catalog.courses.get(k) || 'other');
    const modes = Object.fromEntries(['open', 'approve', 'roster', 'locked'].map((k) => [k, 0]));
    for (const r of (await rows(db, 'SELECT join_mode AS k, COUNT(*) AS n FROM classes GROUP BY join_mode')) || []) if (Object.hasOwn(modes, r.k)) modes[r.k] = int(r.n);
    const yesNo = async (sql) => { const n = await count(db, sql); return n === null ? null : split({ yes: n, no: Math.max(0, classesTotal - n) }); };
    const size = await one(db,
      `SELECT SUM(CASE WHEN n = 0 THEN 1 ELSE 0 END) AS none, SUM(CASE WHEN n BETWEEN 1 AND 9 THEN 1 ELSE 0 END) AS s1to9,
              SUM(CASE WHEN n BETWEEN 10 AND 29 THEN 1 ELSE 0 END) AS s10to29, SUM(CASE WHEN n >= 30 THEN 1 ELSE 0 END) AS s30up
         FROM (SELECT (SELECT COUNT(*) FROM students s WHERE s.class_id = c.id AND s.status = 'active') AS n FROM classes c)`);
    classes = {
      total: classesTotal,
      active7: await count(db, 'SELECT COUNT(*) AS n FROM classes WHERE last_activity_at >= ?', d7),
      active30: await count(db, 'SELECT COUNT(*) AS n FROM classes WHERE last_activity_at >= ?', d30),
      newByWeek: await byWeek(db, 'classes', 'created_at', now),
      byLevel: nest.byParent,
      byCourse: nest.byChild,
      joinMode: split(modes),
      size: size ? split({ none: int(size.none), s1to9: int(size.s1to9), s10to29: int(size.s10to29), s30up: int(size.s30up) }) : null,
      withAssignments: await yesNo('SELECT COUNT(DISTINCT class_id) AS n FROM assignments'),
      inGroup: await yesNo('SELECT COUNT(*) AS n FROM classes WHERE group_id IS NOT NULL'),
      aiFeedbackOn: await yesNo('SELECT COUNT(*) AS n FROM classes WHERE ai_enabled = 1'),
    };
  }

  const seatsTotal = await count(db, 'SELECT COUNT(*) AS n FROM students');
  const pending = await count(db, "SELECT COUNT(*) AS n FROM students WHERE status = 'pending'");
  const seats = seatsTotal === null ? null : {
    total: seatsTotal,
    seen7: await count(db, 'SELECT COUNT(*) AS n FROM students WHERE last_seen_at >= ?', d7),
    seen30: await count(db, 'SELECT COUNT(*) AS n FROM students WHERE last_seen_at >= ?', d30),
    newByWeek: await byWeek(db, 'students', 'created_at', now),
    status: pending === null ? null : split({ active: Math.max(0, seatsTotal - pending), pending }),
  };

  // What teachers assign (one count per lesson: how many classes), and how much class work comes in.
  const assignRows = await rows(db, 'SELECT lesson_slug AS slug, COUNT(*) AS n FROM assignments GROUP BY lesson_slug');
  const kinds = Object.fromEntries(['quiz', 'idea', 'cer', 'done', 'stuck'].map((k) => [k, 0]));
  for (const r of (await rows(db, 'SELECT kind AS k, COUNT(*) AS n FROM answers WHERE updated_at >= ? GROUP BY kind', d30)) || []) if (Object.hasOwn(kinds, r.k)) kinds[r.k] = int(r.n);
  const assigned = assignRows ? listed(assignRows, catalog.lessons) : null;
  const classWork = {
    assignments: assignRows ? assignRows.reduce((s, r) => s + int(r.n), 0) : null,
    assigned: assigned ? assigned.list.map(({ slug, n }) => ({ slug, classes: n })) : null,
    hidden: assigned ? assigned.hidden : null,
    answers30: split(kinds),
  };

  const groups = {
    total: await count(db, 'SELECT COUNT(*) AS n FROM groups'),
    members: await count(db, "SELECT COUNT(*) AS n FROM group_members WHERE status = 'active'"),
  };

  // Films (rule 6: anonymous by construction, so sent as they are). Null until migration 0009.
  let films = null;
  if (await filmCountsReady(db)) {
    const tot = async (from) => {
      const r = await one(db, 'SELECT COALESCE(SUM(started), 0) AS s, COALESCE(SUM(watched), 0) AS w FROM film_counts WHERE day >= ?', from);
      return r ? { started: int(r.s), watched: int(r.w) } : null;
    };
    const perDay = new Map(((await rows(db, 'SELECT day, SUM(started) AS s, SUM(watched) AS w FROM film_counts WHERE day >= ? GROUP BY day', day30)) || []).map((r) => [r.day, r]));
    const perFilm = (await rows(db,
      `SELECT film_key AS k, SUM(started) AS s, SUM(watched) AS w,
              SUM(CASE WHEN day >= ?1 THEN started ELSE 0 END) AS s30, SUM(CASE WHEN day >= ?1 THEN watched ELSE 0 END) AS w30
         FROM film_counts GROUP BY film_key`, day30)) || [];
    const since = await one(db, 'SELECT MIN(day) AS d FROM film_counts');
    films = {
      since: typeof since?.d === 'string' && /^\d{4}-\d{2}-\d{2}$/.test(since.d) ? since.d : null,
      last7: await tot(day7),
      last30: await tot(day30),
      all: await tot('0000-00-00'),
      byDay: Array.from({ length: DAYS }, (_, i) => { const day = isoDay(now - (DAYS - 1 - i) * DAY); const r = perDay.get(day); return { day, started: int(r?.s), watched: int(r?.w) }; }),
      byFilm: perFilm.filter((r) => catalog.films.has(r.k))
        .map((r) => ({ film: r.k, started: int(r.s), watched: int(r.w), started30: int(r.s30), watched30: int(r.w30) }))
        .sort((a, b) => b.started - a.started || b.watched - a.watched || (a.film < b.film ? -1 : 1)).slice(0, 1500),
    };
  }

  // The curiosity router's own daily counters (calls only; its days are US Eastern dates).
  const dayKey = (ms) => 'd' + new Date(ms).toLocaleDateString('en-CA', { timeZone: 'America/New_York' });
  const routerRows = await rows(db, "SELECT period, calls, errors, blocked FROM router_budget WHERE period LIKE 'd%' AND period >= ?", dayKey(now - (DAYS - 1) * DAY));
  let router = null;
  if (routerRows) {
    const by = new Map(routerRows.map((r) => [r.period, r]));
    const all = await one(db, "SELECT COALESCE(SUM(calls), 0) AS n FROM router_budget WHERE period LIKE 'm%'");
    router = {
      callsAll: all ? int(all.n) : null,
      byDay: Array.from({ length: DAYS }, (_, i) => { const p = dayKey(now - (DAYS - 1 - i) * DAY); const r = by.get(p); return { day: p.slice(1), calls: int(r?.calls), errors: int(r?.errors), blocked: int(r?.blocked) }; }),
    };
  }

  // Planner and study helpers: present only once their own migrations are applied.
  const monthsCalls = (table) => count(db, `SELECT COALESCE(SUM(calls), 0) AS n FROM ${table} WHERE period LIKE 'm%'`);
  const plannerCalls = await monthsCalls('planner_budget');
  const helperCalls = await monthsCalls('helper_budget');
  const planner = plannerCalls === null ? null : {
    callsAll: plannerCalls,
    savedPlans: await count(db, 'SELECT COUNT(*) AS n FROM learner_plans'),
    classLists: await count(db, 'SELECT COUNT(*) AS n FROM class_resource_lists'),
  };
  const helpers = helperCalls === null ? null : { callsAll: helperCalls };

  return {
    generated: new Date(now).toISOString(),
    smallCell: SMALL,
    on: { role: hasRole, films: films !== null, catalog: catalog.lessons.size > 0 },
    learners, lessons, teachers, classes, seats, classWork, groups, films, router, planner, helpers,
  };
}

// ---- the route --------------------------------------------------------------------------
/** A Response for an allowed GET /api/admin/stats; null for everything else (the caller's own 404 follows). */
export async function handleAdmin(request, env, db, path, method, url) {
  if (path !== ADMIN_PATH || method !== 'GET') return null;
  const secret = adminSecret(env);
  if (!secret) return null;
  if (!(await allow(db, 'admin:' + (await clientKey(request)), PER_MIN, 60_000))) return null;
  if (url.search) {
    for (const v of url.searchParams.values()) {
      if (v && await sameSecret(v, secret)) console.warn('admin: the ADMIN_TOKEN secret arrived in a web address, which the request log keeps. Replace it: npx wrangler secret put ADMIN_TOKEN');
    }
    return null;
  }
  const m = /^Bearer ([\x21-\x7e]{1,512})$/.exec(request.headers.get('Authorization') || '');
  if (!m || !(await sameSecret(m[1], secret))) return null;
  return json(await buildStats(db, env, request));
}
