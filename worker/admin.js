// The owner's totals: GET /api/admin/stats
//
// How the site is used, for the one person who runs it. Counts only. The page that shows them is
// /admin/ (src/pages/admin/index.astro), a plain static page; this route is the only gated part.
//
// THE GATE (see WHO GETS IN, above the route at the foot of this file, for the owner's own
// account; this part is the second way in). A Worker secret, ADMIN_TOKEN (`npx wrangler secret put ADMIN_TOKEN`; it is never in
// the repository or in wrangler.jsonc). It must arrive in an "Authorization: Bearer ..." header.
//   - The secret must be 24 to 512 printable characters with no spaces (what a header can carry).
//     Not set, not of that shape, wrong, or missing: the route answers exactly what any unknown
//     /api/ path answers (404 "Not found."), by returning null so worker/api.js falls through.
//   - A request with ANY query string is refused the same way, even with the right header.
//     Cloudflare's request log records web addresses, so a secret must never ride in one. If the
//     secret appears anywhere in a query string, a warning is logged (without the value) so the
//     owner knows to replace it.
//   - The comparison is constant-time (both sides are hashed first, so length is not leaked).
//   - A request with neither a Bearer header nor a learner cookie costs nothing: no database
//     work. One with a Bearer header is counted, twenty a minute per connection; over that, 404.
//   - Cache-Control: no-store, no CORS headers, GET only.
//
// AGGREGATES ONLY, BY CONSTRUCTION. Every SQL statement below is a COUNT or a SUM, most with a
// GROUP BY on a fixed column. No statement selects a name, an email, a nickname, an answer, a
// note, a class or group name, a code or an id. The per-lesson statements are joined, inside
// SQL, to the site's own list of lessons, so a lesson key that somebody typed is never read into
// the Worker at all. The only strings in the reply are dates and the site's own keys for levels,
// courses, lessons and films (worker/usage-catalog.js); a made-up course is counted as "other".
//
// ONE COUNT A DAY, NOT WHEN THE READER ASKS. The finished reply is kept (admin_snapshots,
// migration 0009) and served unchanged until it is about 20 hours old; only then does the next
// request make a new one. So a reader cannot pick two moments a few minutes apart and compare
// them. The figures are as they stood WHEN THE COUNT WAS MADE (the reply carries that time):
// accounts, classes and seats made before the start of that site day (US Eastern), with roles,
// progress and "last active" as they were at that moment. Film and lesson-suggester days leave
// the day of the count out. There is no scheduled job in this change; a fixed time of day would
// be better still. Until migration 0009 is applied the route stays shut (404), secret or not,
// because without the table every request would be a fresh count.
//
// HELD UNTIL FIVE MORE. A count made the day after one known person signs up would show that
// person's answer as the only change. So the breakdowns of learners (role, sign-in method, the
// lesson lists) are carried forward unchanged, marked with the date they were made, until the
// site has at least 5 more learner accounts than when they were last published. The breakdowns
// of classes (course, level, join mode, size, extras, what is assigned) are held the same way
// until 5 more teachers have a class. What is still possible: when a held breakdown is
// republished, the change is the sum of at least five people's answers, and a plain total
// (accounts, teachers) still moves by one when one person joins.
//
// THE SMALL-CELL RULE (K = 5), applied to people, not rows.
//   1. Shown as they are, however small: two plain totals only, learner accounts and teacher
//      accounts. The totals of classes and class seats are shown only when at least 5 different
//      teachers have a class; with fewer, a class total would describe those few teachers.
//   2. Everything else that describes a group is a cell, and a cell of 1 to 4 is sent as null
//      (the page prints "under 5"). Zero is sent as 0. That covers every split (role, sign-in
//      method, course, level, join mode, size, kind of answer), every "in the last 7 or 30 days"
//      figure (one three-way split per kind: last 7 days, 8 to 30, older), every weekly count of
//      new accounts, classes or seats, and the counts of school groups, saved plans and class lists.
//   3. A cell that counts classes or seats is hidden unless at least 5 different TEACHERS stand
//      behind it, and a cell that counts answers unless 5 different students in 5 different
//      classes do. That includes weekly new classes and seats, seat status and seats seen. One teacher's five periods are one person, not five.
//   4. No subtraction. A split is all or nothing: if any cell in it must be hidden, every cell
//      with anyone in it is hidden (see split()). A hidden level hides its courses. No published sum includes a hidden row,
//      and no exact count sits beside a hidden split that it would give away (teachers are one
//      three-way split; a lesson is listed only if both the learners who opened it and the
//      learners who did not are 0 or at least 5).
//   5. Role is never crossed with lessons, films or anything else, and across time only in the
//      held form above.
//   6. Film counts and the lesson suggester's daily counts are not cells. Their rows were never
//      tied to an account, a class or a device (worker/film-count.js), so there is nobody a small
//      number could point at. They are also not exact: the film counter takes anonymous
//      messages, so anyone can send it false ones. The page says so.
//
// NEVER SUMMED: learner accounts, teacher accounts and class seats are three separate things.
// One person can be in two of them, and nothing links the rows, so adding them would count
// people twice. They are reported as separate lines.

import { sha256Hex, readCookie } from './auth.js';
import { DAY, clientKey, allow } from './util.js';
import { loadUsageCatalog } from './usage-catalog.js';
import { filmCountsReady, siteDay } from './film-count.js';
import { roleReady, getLearner, LEARNER_COOKIE } from './learner.js';

export const ADMIN_PATH = '/api/admin/stats';
export const SMALL = 5;
const SECRET_SHAPE = /^[\x21-\x7e]{24,512}$/;
const WEEK = 7 * DAY;
const WEEKS = 26;
const DAYS = 30;
const PER_MIN = 20;
const REPLY_KEY = 'reply:v3';    // change when the reply's shape changes, so an old reply is not served
const HOLD_KEY = 'hold:v1';      // what was last published of the held breakdowns, and the totals then (never sent)
const KEEP_MS = 20 * 3_600_000;  // a kept reply is served until it is this old
const STEP = 5;                  // held breakdowns are republished after this many more people

// ---- the gate ---------------------------------------------------------------------------
async function sameSecret(a, b) {
  const [x, y] = await Promise.all([sha256Hex(a), sha256Hex(b)]);
  let diff = 0;
  for (let i = 0; i < x.length; i++) diff |= x.charCodeAt(i) ^ y.charCodeAt(i);
  return diff === 0;
}

/** The secret, or '' when it is not set or could never be sent in a header (then the route stays shut). */
export const adminSecret = (env) => {
  const s = typeof env.ADMIN_TOKEN === 'string' ? env.ADMIN_TOKEN : '';
  return SECRET_SHAPE.test(s) ? s : '';
};

// ---- small cells ------------------------------------------------------------------------
const int = (v) => (Number.isFinite(Number(v)) ? Math.max(0, Math.round(Number(v))) : 0);

/**
 * Cells that add up to a total a reader may know (rule 4). `force` names cells to hide whatever
 * their size (rule 3: too few people behind them). Returns the same keys, with null for hidden.
 *
 * All or nothing, on purpose. If no cell is small or forced, every cell is shown. Otherwise EVERY
 * cell that has anyone in it is hidden, and only the empty cells stay as 0. Hiding just the small
 * cell and "the next smallest" is not enough: a reader who knows that rule can sometimes still
 * work a hidden cell out (5, 4, 4 with a total of 13 was such a case), and scripts/test-admin.mjs
 * checks every split of up to four cells against exactly that reader. Two leftovers would still be
 * given away by the zeros, so then the zeros are hidden too: when only one cell has anyone in it,
 * and when every cell that has anyone has exactly one.
 * Known limit: with five or more cells that ALL hold exactly one, a reader who knows the total
 * knows each is one. Nothing more can be hidden there; it comes with showing the total at all.
 */
export function split(cells, force = []) {
  const keys = Object.keys(cells);
  const n = Object.fromEntries(keys.map((k) => [k, int(cells[k])]));
  const filled = keys.filter((k) => n[k] > 0);
  if (!filled.some((k) => n[k] < SMALL || force.includes(k))) return n;
  const giveaway = filled.length === 1 || filled.every((k) => n[k] === 1);
  return Object.fromEntries(keys.map((k) => [k, n[k] > 0 || giveaway ? null : 0]));
}
/** A stand-alone count: 1 to 4 is hidden. */
export const cell = (n) => (n === null || n === undefined ? null : int(n) >= 1 && int(n) < SMALL ? null : int(n));
/** One number that is part of a known total: shown only if both it and the rest are 0 or at least 5. */
export const part = (n, total, forced = false) => split({ yes: n, no: Math.max(0, int(total) - int(n)) }, forced ? ['yes'] : []).yes;

/** A split inside a split: courses inside levels. `parentOf(key)` gives a cell's level. */
export function nestedSplit(cells, parentOf, forceChild = [], forceParent = []) {
  const parents = {};
  for (const [k, n] of Object.entries(cells)) parents[parentOf(k)] = (parents[parentOf(k)] || 0) + int(n);
  const byParent = split(parents, forceParent);
  const byChild = {};
  for (const p of Object.keys(parents)) {
    const mine = Object.fromEntries(Object.entries(cells).filter(([k]) => parentOf(k) === p));
    if (byParent[p] === null) for (const k of Object.keys(mine)) byChild[k] = null;
    else Object.assign(byChild, split(mine, forceChild));
  }
  return { byParent, byChild };
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

const isoDay = (ms) => new Date(ms).toISOString().slice(0, 10);
/** Monday 00:00 UTC of the week holding `ms`. */
const weekStart = (ms) => { const d = Math.floor(ms / DAY); return (d - ((d + 3) % 7)) * DAY; };
/** The first instant of the site's today (US Eastern), in ms: everything is counted up to here. */
export function startOfSiteDay(now) {
  const day = siteDay(now);
  let t = Date.parse(`${day}T00:00:00Z`) + 4 * 3_600_000;        // midnight Eastern is 04:00 or 05:00 UTC
  if (siteDay(t) !== day) t += 3_600_000;
  return t;
}
const addDays = (day, k) => isoDay(Date.parse(`${day}T12:00:00Z`) + k * DAY);

/** New rows in each of the last 26 weeks, each week a cell. With `teacherOf` (SQL giving the row's teacher), a week also needs 5 different teachers behind it. */
async function byWeek(db, from, col, asOf, teacherOf = null) {
  const first = weekStart(asOf - 1) - (WEEKS - 1) * WEEK;
  const got = await rows(db, `SELECT CAST((${col} - ?1) / ${WEEK} AS INTEGER) AS w, COUNT(*) AS n${teacherOf ? `, COUNT(DISTINCT ${teacherOf}) AS t` : ''} FROM ${from} WHERE ${col} >= ?1 AND ${col} < ?2 GROUP BY w`, first, asOf);
  if (!got) return null;
  const n = new Map(got.map((r) => [int(r.w), r]));
  const weeks = Array.from({ length: WEEKS }, (_, i) => isoDay(first + i * WEEK));
  const force = teacherOf ? weeks.filter((_, i) => n.has(i) && int(n.get(i).t) < SMALL) : [];
  const cells = split(Object.fromEntries(weeks.map((w, i) => [w, int(n.get(i)?.n)])), force);
  return weeks.map((week) => ({ week, n: cells[week] }));
}

/** A split of the classes by `expr`, hidden where fewer than 5 different teachers stand behind a cell (rule 3). */
async function classCells(db, expr, asOf, from = 'classes c') {
  const got = await rows(db, `SELECT ${expr} AS k, COUNT(*) AS n, COUNT(DISTINCT c.teacher_id) AS t FROM ${from} WHERE c.created_at < ?1 GROUP BY k`, asOf);
  return got ? got.map((r) => ({ k: String(r.k), n: int(r.n), t: int(r.t) })) : null;
}
function classSplit(got, keys) {
  if (!got) return null;
  const cells = Object.fromEntries(keys.map((k) => [k, 0]));
  const force = [];
  for (const r of got) if (Object.hasOwn(cells, r.k)) { cells[r.k] = r.n; if (r.t < SMALL) force.push(r.k); }
  return split(cells, force);
}

// ---- the numbers ------------------------------------------------------------------------
/** A fresh count. Returns the reply and the two totals the holds are measured against (those are never sent). */
export async function buildStats(db, env, request, now = Date.now()) {
  let catalog = { levels: [], courses: new Map(), lessons: new Map(), films: new Set() };
  try { catalog = await loadUsageCatalog(env, request); } catch { /* no catalog: totals only, nothing named */ }
  const asOf = startOfSiteDay(now);                 // rows made before the start of the site's day
  const today = siteDay(now);
  const d7 = asOf - 7 * DAY, d30 = asOf - 30 * DAY;
  const lessonKeys = JSON.stringify([...catalog.lessons.keys()]);

  // Learner accounts.
  const learnersTotal = await count(db, 'SELECT COUNT(*) AS n FROM learners WHERE created_at < ?', asOf);
  const hasRole = await roleReady(db);
  const roleRows = hasRole ? await rows(db, "SELECT COALESCE(role, 'unset') AS k, COUNT(*) AS n FROM learners WHERE created_at < ? GROUP BY k", asOf) : null;
  const roleOf = (k) => int(roleRows?.find((r) => r.k === k)?.n);
  const how = await one(db,
    `SELECT SUM(CASE WHEN g = 1 AND p = 0 THEN 1 ELSE 0 END) AS google, SUM(CASE WHEN g = 0 AND p = 1 THEN 1 ELSE 0 END) AS passkey,
            SUM(CASE WHEN g = 1 AND p = 1 THEN 1 ELSE 0 END) AS both, SUM(CASE WHEN g = 0 AND p = 0 THEN 1 ELSE 0 END) AS neither
       FROM (SELECT (l.google_sub IS NOT NULL) AS g, EXISTS (SELECT 1 FROM learner_passkeys k WHERE k.learner_id = l.id) AS p FROM learners l WHERE l.created_at < ?)`, asOf);
  const withNotes = await count(db, "SELECT COUNT(*) AS n FROM learner_data d JOIN learners l ON l.id = d.learner_id WHERE l.created_at < ? AND d.notebook_json NOT IN ('{}', '')", asOf);
  const RECENT = (col) => `CASE WHEN ${col} >= ${d7} THEN 'last7' WHEN ${col} >= ${d30} THEN 'days8to30' ELSE 'older' END`;
  const BUCKETS = ['last7', 'days8to30', 'older'];
  const activeRows = await rows(db, `SELECT ${RECENT('last_active_at')} AS k, COUNT(*) AS n FROM learners WHERE created_at < ? GROUP BY k`, asOf);
  const bucketed = (got) => Object.fromEntries(BUCKETS.map((k) => [k, int(got?.find((r) => r.k === k)?.n)]));
  const learners = learnersTotal === null ? null : {
    total: learnersTotal,
    active: activeRows ? split(bucketed(activeRows)) : null,
    newByWeek: await byWeek(db, 'learners', 'created_at', asOf),
    role: roleRows ? split({ student: roleOf('student'), parent: roleOf('parent'), teacher: roleOf('teacher'), unset: roleOf('unset') }) : null,
    signIn: how ? split({ google: int(how.google), passkey: int(how.passkey), both: int(how.both), neither: int(how.neither) }) : null,
    withNotes: withNotes === null ? null : split({ yes: withNotes, no: Math.max(0, learnersTotal - withNotes) }),
  };

  // Lessons, across signed-in learners (their synced progress). One row per lesson the site has:
  // how many learners have it at all, and how many have it marked done. The join to the site's
  // own lesson list happens in SQL, so a key somebody typed never leaves the database.
  const SAFE = "CASE WHEN json_valid(d.progress_json) THEN d.progress_json ELSE '{}' END";
  const lessonRows = learnersTotal === null ? null : await rows(db,
    `SELECT j.key AS slug, COUNT(*) AS n,
            SUM(CASE WHEN j.type = 'object' AND json_extract(j.value, '$.d') IS NOT NULL THEN 1 ELSE 0 END) AS done
       FROM learner_data d JOIN learners l ON l.id = d.learner_id AND l.created_at < ?2, json_each(${SAFE}, '$.lessons') j
       JOIN json_each(?1) c ON c.value = j.key GROUP BY j.key`, lessonKeys, asOf);
  let lessons = null;
  if (lessonRows) {
    const opened = [];
    let hidden = 0;
    for (const r of lessonRows) {
      if (!catalog.lessons.has(r.slug)) continue;
      const n = int(r.n);
      // Listed only if those who opened it AND those who did not are each 0 or at least 5 (rule 4).
      if (n >= SMALL && part(n, learnersTotal) !== null) opened.push({ slug: r.slug, opened: n, finished: part(int(r.done), n) });
      else if (n >= 1) hidden++;
    }
    opened.sort((a, b) => b.opened - a.opened || (a.slug < b.slug ? -1 : 1));
    lessons = { opened: opened.slice(0, 200), hidden: cell(hidden) };
  }

  // Teachers: one three-way split, so no exact count sits beside a hidden one.
  const teachersTotal = await count(db, 'SELECT COUNT(*) AS n FROM teachers WHERE created_at < ?', asOf);
  const verified = await count(db, 'SELECT COUNT(*) AS n FROM teachers WHERE created_at < ? AND email_verified_at IS NOT NULL', asOf);
  const withClass = await count(db, 'SELECT COUNT(DISTINCT teacher_id) AS n FROM classes WHERE created_at < ?', asOf);
  const withActive = await count(db, 'SELECT COUNT(DISTINCT teacher_id) AS n FROM classes WHERE created_at < ?1 AND last_activity_at >= ?2', asOf, d30);
  const teachers = teachersTotal === null ? null : {
    total: teachersTotal,
    newByWeek: await byWeek(db, 'teachers', 'created_at', asOf),
    verified: verified === null ? null : split({ yes: verified, no: Math.max(0, teachersTotal - verified) }),
    classes: withClass === null || withActive === null ? null
      : split({ active30: withActive, idle: Math.max(0, withClass - withActive), none: Math.max(0, teachersTotal - withClass) }),
  };

  // Classes. Every cell here is hidden unless at least 5 different teachers stand behind it.
  const classesTotal = await count(db, 'SELECT COUNT(*) AS n FROM classes WHERE created_at < ?', asOf);
  // With fewer than 5 teachers behind the site's classes, nothing about classes or seats is shown, the totals included.
  const enoughTeachers = (withClass ?? 0) >= SMALL;
  let classes = null;
  if (classesTotal !== null) {
    const courseCells = {}, courseT = {}, levelT = {};
    const levelOf = (k) => catalog.courses.get(k) || 'other';
    for (const r of (await classCells(db, 'c.course', asOf)) || []) {
      const k = catalog.courses.has(r.k) ? r.k : 'other';
      courseCells[k] = (courseCells[k] || 0) + r.n;
      // Teachers cannot be added across rows without counting one twice, so take the largest row: never too many.
      courseT[k] = Math.max(courseT[k] || 0, r.t);
      levelT[levelOf(k)] = Math.max(levelT[levelOf(k)] || 0, r.t);
    }
    const few = (t) => Object.keys(t).filter((k) => t[k] < SMALL);
    const nest = nestedSplit(courseCells, levelOf, few(courseT), few(levelT));
    const yesNo = (cond) => classCells(db, `CASE WHEN ${cond} THEN 'yes' ELSE 'no' END`, asOf).then((g) => classSplit(g, ['yes', 'no']));
    const SIZED = "(SELECT x.teacher_id, x.created_at, (SELECT COUNT(*) FROM students s WHERE s.class_id = x.id AND s.status = 'active') AS sz FROM classes x) c";
    classes = {
      total: enoughTeachers || classesTotal === 0 ? classesTotal : null,
      active: classSplit(await classCells(db, RECENT('c.last_activity_at'), asOf), BUCKETS),
      newByWeek: await byWeek(db, 'classes', 'created_at', asOf, 'teacher_id'),
      byLevel: nest.byParent,
      byCourse: nest.byChild,
      joinMode: classSplit(await classCells(db, 'c.join_mode', asOf), ['open', 'approve', 'roster', 'locked']),
      size: classSplit(await classCells(db, "CASE WHEN c.sz = 0 THEN 'none' WHEN c.sz < 10 THEN 's1to9' WHEN c.sz < 30 THEN 's10to29' ELSE 's30up' END", asOf, SIZED), ['none', 's1to9', 's10to29', 's30up']),
      withAssignments: await yesNo('EXISTS (SELECT 1 FROM assignments a WHERE a.class_id = c.id)'),
      inGroup: await yesNo('c.group_id IS NOT NULL'),
      aiFeedbackOn: await yesNo('c.ai_enabled = 1'),
    };
  }

  // Class seats. Every figure needs 5 different teachers behind it, like the classes they sit in.
  const SEATS = 'students s JOIN classes c ON c.id = s.class_id';
  const seatsTotal = await count(db, 'SELECT COUNT(*) AS n FROM students WHERE created_at < ?', asOf);
  const seatCells = async (expr, keys) => {
    const got = await rows(db, `SELECT ${expr} AS k, COUNT(*) AS n, COUNT(DISTINCT c.teacher_id) AS t FROM ${SEATS} WHERE s.created_at < ?1 GROUP BY k`, asOf);
    return classSplit(got ? got.map((r) => ({ k: String(r.k), n: int(r.n), t: int(r.t) })) : null, keys);
  };
  const seats = seatsTotal === null ? null : {
    total: enoughTeachers || seatsTotal === 0 ? seatsTotal : null,
    seen: await seatCells(RECENT('COALESCE(s.last_seen_at, 0)'), BUCKETS),
    newByWeek: await byWeek(db, SEATS, 's.created_at', asOf, 'c.teacher_id'),
    status: await seatCells('s.status', ['active', 'pending']),
  };

  // What teachers assign: a lesson is listed once 5 different teachers have assigned it.
  const assignRows = await rows(db,
    `SELECT a.lesson_slug AS slug, COUNT(*) AS n, COUNT(DISTINCT c.teacher_id) AS t
       FROM assignments a JOIN classes c ON c.id = a.class_id AND c.created_at < ?2
       JOIN json_each(?1) k ON k.value = a.lesson_slug GROUP BY a.lesson_slug`, lessonKeys, asOf);
  // Class work in the last 30 days, by kind: shown only with 5 different students in 5 different classes behind it.
  const kinds = Object.fromEntries(['quiz', 'idea', 'cer', 'done', 'stuck'].map((k) => [k, 0]));
  const thin = [];
  for (const r of (await rows(db,
    `SELECT a.kind AS k, COUNT(*) AS n, COUNT(DISTINCT a.student_id) AS st, COUNT(DISTINCT s.class_id) AS cl
       FROM answers a JOIN students s ON s.id = a.student_id WHERE a.updated_at >= ?1 AND a.updated_at < ?2 GROUP BY a.kind`, d30, asOf)) || []) {
    if (!Object.hasOwn(kinds, r.k)) continue;
    kinds[r.k] = int(r.n);
    if (int(r.st) < SMALL || int(r.cl) < SMALL) thin.push(r.k);
  }
  const assigned = assignRows ? assignRows.filter((r) => catalog.lessons.has(r.slug)) : null;
  const classWork = {
    assigned: assigned ? assigned.filter((r) => int(r.t) >= SMALL).map((r) => ({ slug: r.slug, classes: int(r.n), teachers: int(r.t) }))
      .sort((a, b) => b.teachers - a.teachers || b.classes - a.classes || (a.slug < b.slug ? -1 : 1)).slice(0, 200) : null,
    hidden: assigned ? cell(assigned.filter((r) => int(r.t) < SMALL).length) : null,
    answers30: split(kinds, thin),
  };

  const groups = {
    total: cell(await count(db, 'SELECT COUNT(*) AS n FROM groups WHERE created_at < ?', asOf)),
  };

  // Films (rule 6: anonymous by construction, and approximate). Whole days only: today is left out.
  let films = null;
  if (await filmCountsReady(db)) {
    const first30 = addDays(today, -DAYS), first7 = addDays(today, -7);
    const tot = async (from) => {
      const r = await one(db, 'SELECT COALESCE(SUM(started), 0) AS s, COALESCE(SUM(watched), 0) AS w FROM film_counts WHERE day >= ?1 AND day < ?2', from, today);
      return r ? { started: int(r.s), watched: int(r.w) } : null;
    };
    const perDay = new Map(((await rows(db, 'SELECT day, SUM(started) AS s, SUM(watched) AS w FROM film_counts WHERE day >= ?1 AND day < ?2 GROUP BY day', first30, today)) || []).map((r) => [r.day, r]));
    const perFilm = (await rows(db,
      `SELECT film_key AS k, SUM(started) AS s, SUM(watched) AS w,
              SUM(CASE WHEN day >= ?1 THEN started ELSE 0 END) AS s30, SUM(CASE WHEN day >= ?1 THEN watched ELSE 0 END) AS w30
         FROM film_counts WHERE day < ?2 GROUP BY film_key`, first30, today)) || [];
    const since = await one(db, 'SELECT MIN(day) AS d FROM film_counts WHERE day < ?', today);
    films = {
      since: typeof since?.d === 'string' && /^\d{4}-\d{2}-\d{2}$/.test(since.d) ? since.d : null,
      last7: await tot(first7),
      last30: await tot(first30),
      all: await tot('0000-00-00'),
      byDay: Array.from({ length: DAYS }, (_, i) => { const day = addDays(today, i - DAYS); const r = perDay.get(day); return { day, started: int(r?.s), watched: int(r?.w) }; }),
      byFilm: perFilm.filter((r) => catalog.films.has(r.k))
        .map((r) => ({ film: r.k, started: int(r.s), watched: int(r.w), started30: int(r.s30), watched30: int(r.w30) }))
        .sort((a, b) => b.started - a.started || b.watched - a.watched || (a.film < b.film ? -1 : 1)).slice(0, 1500),
    };
  }

  // The lesson suggester's own daily counters (calls only; its days are site days too). Today is left out.
  const routerRows = await rows(db, "SELECT period, calls, errors, blocked FROM router_budget WHERE period LIKE 'd%' AND period >= ?1 AND period < ?2", 'd' + addDays(today, -DAYS), 'd' + today);
  let router = null;
  if (routerRows) {
    const by = new Map(routerRows.map((r) => [r.period, r]));
    router = {
      byDay: Array.from({ length: DAYS }, (_, i) => { const day = addDays(today, i - DAYS); const r = by.get('d' + day); return { day, calls: int(r?.calls), errors: int(r?.errors), blocked: int(r?.blocked) }; }),
    };
  }

  // Study planner: present only once its own migration is applied. Saved items only (whole-site totals).
  // One learner can save many plans and one teacher many lists, so each needs 5 different people behind it.
  const plans = await one(db, 'SELECT COUNT(*) AS n, COUNT(DISTINCT learner_id) AS p FROM learner_plans WHERE created_at < ?', asOf);
  const lists = await one(db, 'SELECT COUNT(*) AS n, COUNT(DISTINCT teacher_id) AS p FROM class_resource_lists WHERE created_at < ?', asOf);
  const behind = (r) => (r === null ? null : int(r.n) === 0 ? 0 : int(r.p) >= SMALL ? int(r.n) : null);
  const planner = plans === null ? null : { savedPlans: behind(plans), classLists: behind(lists) };

  const stats = {
    generated: new Date(now).toISOString(),
    asOf: addDays(today, -1),
    smallCell: SMALL,
    on: { role: hasRole, films: films !== null, catalog: catalog.lessons.size > 0 },
    learners, lessons, teachers, classes, seats, classWork, groups, films, router, planner,
  };
  return { stats, base: { learners: learnersTotal ?? 0, teachers: withClass ?? 0 } };
}

// ---- held until five more -----------------------------------------------------------------
// The parts of a reply that are carried forward (see the header). `pick` takes the pieces out of
// a reply, `put` writes them back into one. A piece that comes back null (its query failed, or its
// table is not there) is never taken into the hold: the old piece is kept. Otherwise one failed
// query on a day the block is republished would force the whole block out again at the next
// count, one day later, and that one day's change could be one person's.
const HELD = {
  learners: {
    pick: (s) => ({ role: s.learners?.role ?? null, signIn: s.learners?.signIn ?? null, withNotes: s.learners?.withNotes ?? null, lessons: s.lessons ?? null }),
    put: (s, h, day) => { if (s.learners) { s.learners.role = h.role; s.learners.signIn = h.signIn; s.learners.withNotes = h.withNotes; s.learners.splitsAsOf = day; } s.lessons = h.lessons; },
  },
  teachers: {
    pick: (s) => { const c = s.classes || {}; return { byLevel: c.byLevel ?? null, byCourse: c.byCourse ?? null, joinMode: c.joinMode ?? null, size: c.size ?? null, withAssignments: c.withAssignments ?? null, inGroup: c.inGroup ?? null, aiFeedbackOn: c.aiFeedbackOn ?? null, assigned: s.classWork.assigned ?? null, hidden: s.classWork.hidden ?? null, hiddenKnown: s.classWork.assigned !== null }; },
    put: (s, h, day) => {
      if (s.classes) Object.assign(s.classes, { byLevel: h.byLevel, byCourse: h.byCourse, joinMode: h.joinMode, size: h.size, withAssignments: h.withAssignments, inGroup: h.inGroup, aiFeedbackOn: h.aiFeedbackOn, splitsAsOf: day });
      s.classWork.assigned = h.assigned; s.classWork.hidden = h.hidden;
    },
  },
};

/** Put the held breakdowns into a fresh reply, republishing a block only when its total has grown by 5. Returns the new hold record. */
export function applyHold(stats, base, prev) {
  const next = {};
  for (const [name, block] of Object.entries(HELD)) {
    const fresh = block.pick(stats);
    const old = prev?.[name];
    if (old && base[name] < old.base + STEP) {
      block.put(stats, old.held, old.day);
      next[name] = old;
      continue;
    }
    // A release. Keep the old piece wherever the fresh one is missing. ("hidden" is null both when it failed and
    // when it is a small count, so it follows the list it belongs to.)
    const held = {};
    for (const k of Object.keys(fresh)) held[k] = fresh[k] ?? old?.held?.[k] ?? null;
    if (name === 'teachers' && fresh.hiddenKnown) held.hidden = fresh.hidden;
    next[name] = { base: base[name], day: stats.asOf, held };
    block.put(stats, held, stats.asOf);
  }
  return next;
}

// ---- one count a day ---------------------------------------------------------------------
const snapshotsReady = async (db) => (await one(db, 'SELECT 1 AS n FROM admin_snapshots LIMIT 0')) !== null;

/** The reply as text: the kept one while it is under about 20 hours old, else a new count, kept. */
export async function dailyReply(db, env, request, now = Date.now()) {
  const kept = await one(db, 'SELECT body, made_at FROM admin_snapshots WHERE day = ?', REPLY_KEY);
  if (kept?.body && now - int(kept.made_at) < KEEP_MS && now >= int(kept.made_at)) return kept.body;
  let prev = null;
  try { prev = JSON.parse((await one(db, 'SELECT body FROM admin_snapshots WHERE day = ?', HOLD_KEY))?.body || 'null'); } catch { prev = null; }
  const { stats, base } = await buildStats(db, env, request, now);
  const hold = applyHold(stats, base, prev);
  const body = JSON.stringify(stats);
  // Two rows only, each replaced in place, so there is no "delete the other days" step to race with.
  await db.batch([
    db.prepare('INSERT OR REPLACE INTO admin_snapshots (day, body, made_at) VALUES (?, ?, ?)').bind(REPLY_KEY, body, now),
    db.prepare('INSERT OR REPLACE INTO admin_snapshots (day, body, made_at) VALUES (?, ?, ?)').bind(HOLD_KEY, JSON.stringify(hold), now),
    db.prepare('DELETE FROM admin_snapshots WHERE day NOT IN (?, ?)').bind(REPLY_KEY, HOLD_KEY),
  ]);
  return body;
}

// ---- the route --------------------------------------------------------------------------
// WHO GETS IN. Two ways, and anyone else gets the unknown-path 404.
//
//   1. The owner's own account. A signed-in LEARNER session (the ordinary bp_learner cookie) whose
//      account is linked to Google and whose email, as Google itself reported it at sign-in, is one
//      of the addresses in the ADMIN_EMAILS var (wrangler.jsonc). The email column is only ever
//      written from a Google ID token whose signature was checked and whose email_verified claim is
//      true (worker/learner.js verifyGoogleIdToken): there is no route by which a person can type
//      an email into a learner account. A passkey-only account has no email at all, a display name
//      is never looked at, and teacher accounts and class seats are different tables and different
//      cookies that this code does not read. The match is exact after trimming and lower-casing:
//      no dot or plus-tag folding, no domain match. The request must come from the site's own
//      pages (Sec-Fetch-Site / Origin), so another site cannot ask through the owner's browser.
//   2. The ADMIN_TOKEN secret in an Authorization header, as before. Unset unless the owner sets it.
//
// A request that carries neither a well-formed learner cookie nor a Bearer header does no
// database work at all.

/** The addresses in ADMIN_EMAILS that are plain, whole email addresses, lower-cased. Empty means nobody. */
export function adminEmails(env) {
  return String(typeof env.ADMIN_EMAILS === 'string' ? env.ADMIN_EMAILS : '').split(',')
    .map((e) => e.trim().toLowerCase()).filter((e) => /^[^\s@,<>"]+@[^\s@,<>"]+\.[a-z]{2,}$/.test(e));
}

/** True for a GET that this site's own page made. A browser says where a request came from; a cross-site one is refused. */
function fromThisSite(request, url) {
  const site = request.headers.get('Sec-Fetch-Site');
  if (site && site !== 'same-origin') return false;
  const origin = request.headers.get('Origin');
  return !origin || origin === url.origin;
}

/** Is this request the owner, signed in with Google as one of the ADMIN_EMAILS addresses? */
async function ownerSession(request, env, db, url) {
  const allowed = adminEmails(env);
  if (!allowed.length || !fromThisSite(request, url)) return false;
  if (!/^[0-9a-f]{64}$/.test(readCookie(request, LEARNER_COOKIE) || '')) return false;   // no cookie: no database work
  const l = await getLearner(db, request);
  // Both must be there: a Google link, and the email Google vouched for. Nothing else about the account counts.
  if (!l || !l.google_sub || typeof l.email !== 'string') return false;
  return allowed.includes(l.email.trim().toLowerCase());
}

/** A Response for an allowed GET /api/admin/stats; null for everything else (the caller's own 404 follows). */
export async function handleAdmin(request, env, db, path, method, url) {
  if (path !== ADMIN_PATH || method !== 'GET') return null;
  const secret = adminSecret(env);
  if (url.search) {
    if (secret) {
      let q = url.search;
      try { q = decodeURIComponent(url.search); } catch { /* keep it as sent */ }
      if (q.includes(secret) || url.search.includes(secret)) console.warn('admin: the ADMIN_TOKEN secret arrived in a web address, which the request log keeps. Replace it: npx wrangler secret put ADMIN_TOKEN');
    }
    return null;
  }
  let ok = false;
  const m = secret && /^Bearer ([\x21-\x7e]{1,512})$/.exec(request.headers.get('Authorization') || '');
  if (m) {
    if (!(await allow(db, 'admin:' + (await clientKey(request)), PER_MIN, 60_000))) return null;
    ok = await sameSecret(m[1], secret);
  }
  if (!ok && await ownerSession(request, env, db, url)) {
    // Counted only once we know it is the owner, so nobody else's visit writes anything.
    ok = await allow(db, 'admin:' + (await clientKey(request)), PER_MIN, 60_000);
  }
  if (!ok) return null;
  if (!(await snapshotsReady(db))) return null;                  // before migration 0009 the route stays shut
  return new Response(await dailyReply(db, env, request), { headers: { 'Content-Type': 'application/json; charset=utf-8', 'Cache-Control': 'no-store', Vary: 'Cookie, Authorization' } });
}
