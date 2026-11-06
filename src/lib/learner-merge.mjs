// Merge rules for learner sync, shared by the worker (worker/learner.js) and the
// browser (src/lib/learner.ts) so both sides always agree.
//
// Notebook (biochempedia:notebook:v1 items): per id, the record with the larger
// `updated` wins, tombstones (deleted: true) included. A tie keeps the first side.
// Tombstones older than 90 days are dropped.
//
// Progress (biochempedia:progress:v1): per lesson keep the earliest first visit `v`
// and the latest done mark `d`; per question keep the record with the larger `t`.
// `path` and `last` have no timestamp: the second argument's value wins when it has one.

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
  const path = typeof B.path === 'string' ? B.path : A.path;
  const last = typeof B.last === 'string' ? B.last : A.last;
  if (typeof path === 'string') out.path = path;
  if (typeof last === 'string') out.last = last;

  for (const side of [A.lessons, B.lessons]) {
    for (const [slug, rec] of Object.entries(side)) {
      if (!isObj(rec)) continue;
      const v = num(rec.v);
      const d = num(rec.d);
      if (v === undefined && d === undefined) continue;
      const cur = out.lessons[slug];
      if (!cur) { out.lessons[slug] = { v: v ?? d, ...(d !== undefined ? { d } : {}) }; continue; }
      if (v !== undefined && v < cur.v) cur.v = v;
      if (d !== undefined && (cur.d === undefined || d > cur.d)) cur.d = d;
    }
  }
  for (const side of [A.items, B.items]) {
    for (const [id, it] of Object.entries(side)) {
      if (!isObj(it) || num(it.t) === undefined) continue;
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
