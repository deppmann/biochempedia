// The one-time hand-off of browser-only data when the site's address changes (worker/host.js).
// Browser storage belongs to one origin, so after the switch a learner's progress, notebook,
// flashcard schedule, film marks and class code stay behind on biochemistrypedia.com. The old
// host's /handoff/ page reads them and posts them to the new host, whose page asks
// POST /handoff/merge (below) what to write, given what it already holds.
//
// Rules: a key the new host lacks is copied. A key it has is kept as it is (it was written after
// the switch, so it is the newer), except the five records below, which are merged entry by entry
// with the rules the account sync already uses, so nothing newer is overwritten and nothing older
// is lost. Running it twice changes nothing the second time. Only keys that change are returned.
import { mergeNotebookItems, mergeProgress, sameJson } from './learner-merge.mjs';

// Every localStorage key the site writes starts with one of these (inventory, 2026-11-15):
//   biochempedia:progress:v1, :resume:v1, :notebook:v1, :notebook-missing:v1, :cards:v1,
//   :cards:prefs, :films:v1, :mycards:v1, :class:v1, :class-cards:v1, :listen:rate,
//   :listen:film-stops (src/lib/*, src/components/*), bcp-arcade:progress, :prefs, :muted (the
//   arcade, src/game/engine/*), bcp:mcat-beyond (MCAT practice), bp-supports (supports switch),
//   bp-cer:<page path>:<id> (CER answers), bp-design:<slug>:<item> (design answers),
//   bp-teachers-demo-v3 (teacher demo). scripts/test-host.mjs fails if a key outside these
//   prefixes appears in src/.
export const HANDOFF_KEY = /^(biochempedia:|bcp-arcade:|bcp:|bp-)/;
// Not carried: storage probes, the cached account summary (an account signs in again, or is
// carried by the sign-in code; its cache is rebuilt on the first sync), and the hand-off's own
// count of failed tries (biochempedia:handoff:tries, kept on the old origin).
export const HANDOFF_SKIP = /^biochempedia:learner:v1$|^biochempedia:handoff:|:probe$|:test$/;

export const MAX_KEYS = 5000;
// Browsers keep at most 5 MiB of localStorage per origin (MDN, "Storage quotas and eviction
// criteria"), counted in UTF-16 characters by Chromium. The old host's page sends the store as one
// multipart field, so its size on the wire is the store's own size (UTF-8) plus the escaping of
// quotes inside the saved JSON (about a tenth more). A store of up to MAX_STORE_CHARS characters as
// sent is accepted; that is well above what any browser lets the site keep (about 5.2 million
// characters), so in practice everything fits. Above it the page offers a download instead.
export const MAX_STORE_CHARS = 8_000_000;
// The server's cap on the body: the largest store in UTF-8 (non-ASCII text takes up to 3 bytes a
// character) plus the form's few hundred bytes of framing.
export const MAX_BYTES = 26 * 1024 * 1024;

export const carried = (k) => typeof k === 'string' && k.length <= 400 && HANDOFF_KEY.test(k) && !HANDOFF_SKIP.test(k);

const isObj = (x) => !!x && typeof x === 'object' && !Array.isArray(x);
const parse = (s) => { try { return JSON.parse(s); } catch { return undefined; } };
const num = (x) => (typeof x === 'number' && Number.isFinite(x) ? x : undefined);

/** Per key, the later of two records by `field` (a tie keeps `a`). */
function laterEach(a, b, field) {
  const out = {};
  for (const side of [a, b]) {
    if (!isObj(side)) continue;
    for (const [k, v] of Object.entries(side)) {
      if (!isObj(v) || num(v[field]) === undefined) continue;
      if (!out[k] || v[field] > out[k][field]) out[k] = v;
    }
  }
  return out;
}

const MERGERS = {
  // cur = what the new host holds, inc = what came from the old host. Each returns the merged value
  // or undefined to leave the key alone.
  'biochempedia:progress:v1': (cur, inc) => mergeProgress(inc, cur),   // ties keep the new host's
  'biochempedia:notebook:v1': (cur, inc, now) => ({ v: 1, items: mergeNotebookItems(cur?.items, inc?.items, now) }),
  // Flashcard schedule: per card, the state answered last.
  'biochempedia:cards:v1': (cur, inc) => ({ v: 1, cards: laterEach(cur?.cards, inc?.cards, 't') }),
  // Films: watched marks keep the first time; the "keep watching" list and queue places keep the
  // latest; badges keep the first earned.
  'biochempedia:films:v1': (cur, inc) => {
    const w = {};
    for (const side of [cur?.w, inc?.w]) if (isObj(side)) for (const [k, t] of Object.entries(side)) if (num(t) !== undefined && (w[k] === undefined || t < w[k])) w[k] = t;
    const byFilm = {};
    for (const side of [cur?.p, inc?.p]) if (Array.isArray(side)) for (const p of side) if (isObj(p) && typeof p.f === 'string' && num(p.at) !== undefined && (!byFilm[p.f] || p.at > byFilm[p.f].at)) byFilm[p.f] = p;
    const p = Object.values(byFilm).filter((x) => !w[x.f] || w[x.f] < x.at).sort((a, b) => b.at - a.at).slice(0, 12);
    const q = laterEach(cur?.q, inc?.q, 'at');
    const b = {};
    for (const side of [inc?.b, cur?.b]) if (isObj(side)) for (const [k, x] of Object.entries(side)) if (isObj(x) && (!b[k] || (num(x.at) ?? Infinity) < (num(b[k].at) ?? Infinity))) b[k] = x;
    return { v: 1, w, p, q, ...(Object.keys(b).length ? { b } : {}) };
  },
  // Personal flashcards: per lesson, every card from both sides; the new host's copy wins a clash.
  'biochempedia:mycards:v1': (cur, inc) => {
    const decks = {};
    for (const side of [cur?.decks, inc?.decks]) {
      if (!isObj(side)) continue;
      for (const [slug, cards] of Object.entries(side)) {
        if (!Array.isArray(cards)) continue;
        const list = decks[slug] || (decks[slug] = []);
        for (const c of cards) if (isObj(c) && typeof c.id === 'string' && !list.some((x) => x.id === c.id) && list.length < 200) list.push(c);
      }
    }
    return { v: 1, decks };
  },
};

const shapeOk = {
  'biochempedia:progress:v1': (x) => isObj(x),
  'biochempedia:notebook:v1': (x) => isObj(x) && x.v === 1 && isObj(x.items),
  'biochempedia:cards:v1': (x) => isObj(x) && x.v === 1 && isObj(x.cards),
  'biochempedia:films:v1': (x) => isObj(x) && x.v === 1 && isObj(x.w) && Array.isArray(x.p) && isObj(x.q),
  'biochempedia:mycards:v1': (x) => isObj(x) && x.v === 1 && isObj(x.decks),
};

/**
 * current: { key: string } read on the new host for the keys that arrived.
 * incoming: { key: string } sent from the old host.
 * Returns { write: { key: string } }: only what should change on the new host.
 */
export function mergeStorage(current, incoming, now = Date.now()) {
  const write = {};
  if (!isObj(incoming)) return { write };
  const cur = isObj(current) ? current : {};
  let n = 0;
  for (const [k, raw] of Object.entries(incoming)) {
    if (++n > MAX_KEYS) break;
    if (!carried(k) || typeof raw !== 'string') continue;
    const have = typeof cur[k] === 'string' ? cur[k] : null;
    if (have === null) { write[k] = raw; continue; }      // the new host has nothing: copy
    if (have === raw) continue;
    const merge = MERGERS[k];
    if (!merge) continue;                                   // the new host's own value is the newer
    const a = parse(have), b = parse(raw);
    if (!shapeOk[k](b)) continue;                           // nothing usable came: keep what is here
    if (!shapeOk[k](a)) { write[k] = raw; continue; }      // what is here is damaged: take what came
    const merged = merge(a, b, now);
    if (merged !== undefined && !sameJson(merged, a)) write[k] = JSON.stringify(merged);
  }
  return { write };
}
