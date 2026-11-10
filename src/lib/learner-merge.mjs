// Merge rules for learner sync, shared by the worker (worker/learner.js) and the
// browser (src/lib/learner.ts) so both sides always agree.
//
// Notebook (biochempedia:notebook:v1 items): per id, the record with the larger
// `updated` wins, tombstones (deleted: true) included. A tie keeps the first side.
// Tombstones older than 90 days are dropped.
//
// Progress (biochempedia:progress:v1): per lesson keep the earliest first visit `v`
// and the latest done mark `d`; per question keep the record with the larger `t`.
//
// Removals travel as timestamps, so "undo" on one device is not put back by the next sync:
//   lesson `u`   when "done" was last unticked. A `u` at or after `d` removes the done mark.
//   `pathAt`     when the path was last chosen or cleared. The side with the later one wins,
//                a cleared path included. With no `pathAt` on either side (records written
//                before 2026-11-10) the second argument's path wins when it has one.
//   `reset`      when "reset progress" was last pressed. Lessons and questions not touched
//                since then are dropped, as is a path not chosen since then.
// `last` has no timestamp: the second argument's value wins when it has one, and it is kept
// only while its lesson record exists.

const TOMBSTONE_MS = 90 * 86_400_000;

const isObj = (x) => !!x && typeof x === 'object' && !Array.isArray(x);

/** True for something shaped like a notebook item. */
export function validNoteItem(x, id) {
  return isObj(x) && typeof x.id === 'string' && x.id.length <= 64 && (id === undefined || x.id === id)
    && (x.kind === 'highlight' || x.kind === 'note') && typeof x.slug === 'string'
    && typeof x.updated === 'number' && Number.isFinite(x.updated);
}

/** Merge two `items` maps. Returns a new map. */
export function mergeNotebookItems(a, b, now = Date.now()) {
  const out = {};
  for (const side of [a, b]) {
    if (!isObj(side)) continue;
    for (const [id, it] of Object.entries(side)) {
      if (!validNoteItem(it, id)) continue;
      const cur = out[id];
      if (!cur || it.updated > cur.updated) out[id] = it;
    }
  }
  for (const [id, it] of Object.entries(out)) {
    if (it.deleted === true && now - it.updated > TOMBSTONE_MS) delete out[id];
  }
  return out;
}

/** True for something shaped like the progress object. */
export function validProgress(p) {
  return isObj(p) && p.v === 1 && isObj(p.lessons) && isObj(p.items);
}

const num = (x) => (typeof x === 'number' && Number.isFinite(x) ? x : undefined);

/** Merge two progress objects. Either may be missing. Returns a new object. */
export function mergeProgress(a, b) {
  const A = validProgress(a) ? a : { v: 1, lessons: {}, items: {} };
  const B = validProgress(b) ? b : { v: 1, lessons: {}, items: {} };
  const out = { v: 1, lessons: {}, items: {} };
  const reset = Math.max(num(A.reset) ?? 0, num(B.reset) ?? 0);
  if (reset) out.reset = reset;

  const aAt = num(A.pathAt), bAt = num(B.pathAt);
  let path, pathAt;
  if (aAt === undefined && bAt === undefined) path = typeof B.path === 'string' ? B.path : A.path;
  else {
    const from = (bAt ?? -Infinity) >= (aAt ?? -Infinity) ? B : A;   // a tie keeps the second side, as before
    path = from.path; pathAt = num(from.pathAt);
  }
  if (reset && (pathAt === undefined || pathAt <= reset)) { path = undefined; pathAt = undefined; }
  if (typeof path === 'string') out.path = path;
  if (pathAt !== undefined) out.pathAt = pathAt;
  const last = typeof B.last === 'string' ? B.last : A.last;

  for (const side of [A.lessons, B.lessons]) {
    for (const [slug, rec] of Object.entries(side)) {
      if (!isObj(rec)) continue;
      const v = num(rec.v);
      const d = num(rec.d);
      const u = num(rec.u);
      if (v === undefined && d === undefined) continue;
      const cur = out.lessons[slug];
      if (!cur) { out.lessons[slug] = { v: v ?? d, ...(d !== undefined ? { d } : {}), ...(u !== undefined ? { u } : {}) }; continue; }
      if (v !== undefined && v < cur.v) cur.v = v;
      if (d !== undefined && (cur.d === undefined || d > cur.d)) cur.d = d;
      if (u !== undefined && (cur.u === undefined || u > cur.u)) cur.u = u;
    }
  }
  for (const [slug, rec] of Object.entries(out.lessons)) {
    if (rec.u !== undefined && rec.d !== undefined) {
      if (rec.u >= rec.d) delete rec.d; else delete rec.u;   // whichever happened last stands
    }
    if (reset && Math.max(rec.v, rec.d ?? 0, rec.u ?? 0) <= reset) delete out.lessons[slug];
  }
  if (typeof last === 'string' && (!reset || out.lessons[last])) out.last = last;
  for (const side of [A.items, B.items]) {
    for (const [id, it] of Object.entries(side)) {
      if (!isObj(it) || num(it.t) === undefined) continue;
      if (reset && it.t <= reset) continue;
      const cur = out.items[id];
      if (!cur || it.t > cur.t) out.items[id] = it;
    }
  }
  return out;
}

/** Stable comparison, so a merge that changed nothing does not rewrite storage. */
export function sameJson(a, b) {
  return JSON.stringify(sortKeys(a)) === JSON.stringify(sortKeys(b));
}
function sortKeys(x) {
  if (Array.isArray(x)) return x.map(sortKeys);
  if (!isObj(x)) return x;
  return Object.fromEntries(Object.keys(x).sort().map((k) => [k, sortKeys(x[k])]));
}
