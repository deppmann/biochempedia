/* Film search (2026-11-22): finds a film on its own, not only through its lesson's title.

   Plain functions with no DOM, so the film library (/films/), the run page (/films/run/), the site
   search box (src/components/SiteSearch.astro) and the Node check (scripts/test-film-search.mjs) all
   run this one matcher on the same two files:
     /films/list.json    the cards: title, kind, course, level, lesson title (film-cards.ts ListFilm)
     /films/search.json  what else a film can be found by (src/lib/film-search-data.ts): its field,
                         the ideas its lesson teaches, the method it shows, its take-homes and the
                         rarer words of its transcript.
   Without search.json (not loaded yet, or it failed) a search reads titles, lessons, courses and
   levels only.

   How a query is read:
   - "film", "films", "video", "clip" ask for films, which is everything here: they are dropped.
   - "method(s)", "technique(s)" keep method films (and lesson films the methods library reuses);
     "activity", "profile"/"scientist", "first film", "second chapter", "chapter 2", "series" keep
     that kind; "high school", "grade 7", "graduate", "college", "kids" keep that level. These are
     filters, not words a title must hold. A filter that leaves nothing is read as plain words again.
   - Little words ("how", "the", "of") are dropped unless the query is nothing else.
   - Every remaining word must be found somewhere in the film's record: exactly, as a plural or
     singular, as the start of a longer word ("mito"), or one letter off ("mitochondira"; two off for
     long words). Films with every word come first, best first; films with all but one word follow,
     marked as partial.

   Ranking: each word scores by the best place it was found (title 10, lesson or method name 7,
   field up to 5, ideas and course 4, search phrases 3, take-homes 2, level and kind 2, transcript 1),
   times how well it matched (exact 1, plural 0.95, start of a word 0.75, a typo 0.6). The whole
   query inside the title, the lesson title or the method name adds a bonus. Ties keep course order. */

export const W = { title: 10, lesson: 7, method: 7, field: 5, idea: 4, course: 4, phrase: 3, take: 2, level: 2, kind: 2, transcript: 1 };
export const QUALITY = { exact: 1, plural: 0.95, prefix: 0.75, typo: 0.6 };
/** Partial matches (all words but one) listed after the full ones, at most this many. */
export const PARTIAL_MAX = 30;
/** Field weights in search.json run up to 1.5 (course 1, its ideas' areas or a method's category 0.5): this is full weight. */
export const FIELD_TOP = 1.5;

const LITTLE = new Set('a an and are as at be by can do does for from how in into is it its of on or so that the their then there this to was what when where which who why will with your you about'.split(' '));
const FILM_WORDS = new Set(['film', 'films', 'video', 'videos', 'movie', 'movies', 'clip', 'clips', 'watch', 'animation', 'animations']);

/** The kinds of film a query can ask for, and the levels. Each is [phrase words, value]. Longer phrases first. */
const KIND_PHRASES = [
  [['second', 'chapter'], 'second'], [['second', 'film'], 'second'], [['second', 'films'], 'second'], [['chapter', '2'], 'second'], [['chapter', 'two'], 'second'],
  [['part', '2'], 'second'], [['first', 'film'], 'first'], [['first', 'films'], 'first'], [['first', 'chapter'], 'first'], [['chapter', '1'], 'first'], [['chapter', 'one'], 'first'],
  [['how', 'we', 'know'], 'method'],
  [['method'], 'method'], [['methods'], 'method'], [['technique'], 'method'], [['techniques'], 'method'],
  [['activity'], 'activity'], [['activities'], 'activity'],
  [['profile'], 'profile'], [['profiles'], 'profile'], [['scientist'], 'profile'], [['scientists'], 'profile'],
  [['series'], 'series'],
];
const LEVEL_PHRASES = [
  [['high', 'school'], ['high-school']], [['grade', '7'], ['grade-7']], [['7th', 'grade'], ['grade-7']], [['middle', 'school'], ['grade-7']], [['seventh', 'grade'], ['grade-7']],
  [['grad', 'school'], ['graduate']], [['graduate'], ['graduate']],
  [['ages', '5', '10'], ['ages-5-10']], [['kids'], ['ages-5-10']], [['children'], ['ages-5-10']], [['k', '5'], ['ages-5-10']],
  [['intro', 'college'], ['starting-college']], [['college'], ['starting-college', 'college-core', 'college-further']],
];
/** Words each level can also be found by (its title is used too). */
const LEVEL_WORDS = {
  'ages-5-10': 'kids children young', 'grade-7': 'grade seventh middle school', 'high-school': 'high school',
  'starting-college': 'college intro introductory', 'college-core': 'college core', 'college-further': 'college advanced', graduate: 'graduate grad advanced',
};
const KIND_WORDS = { first: 'first chapter', second: 'second chapter', series: 'series part', activity: 'activity', profile: 'profile scientist', method: 'method technique' };

export const fold = (s) => String(s ?? '').normalize('NFD').replace(/[̀-ͯ]/g, '').toLowerCase();
export const tokens = (s) => fold(s).split(/[^a-z0-9]+/).filter((w) => w.length > 1 || /\d/.test(w));

/** Singular form, roughly: "synapses" and "synapse" meet, as do "mitochondria"/"mitochondrion" no. */
export function stem(w) {
  if (w.length < 4) return w;
  if (/ies$/.test(w) && w.length > 4) return `${w.slice(0, -3)}y`;
  if (/(ss|us|is)$/.test(w)) return w;
  if (/(sses|xes|ches|shes|zes)$/.test(w)) return w.slice(0, -2);
  if (/s$/.test(w)) return w.slice(0, -1);
  return w;
}

/** Edit distance with swaps, stopping early once past `max`. */
export function distance(a, b, max = 2) {
  if (Math.abs(a.length - b.length) > max) return max + 1;
  const d = Array.from({ length: a.length + 1 }, (_, i) => [i]);
  for (let j = 1; j <= b.length; j++) d[0][j] = j;
  for (let i = 1; i <= a.length; i++) {
    let row = Infinity;
    for (let j = 1; j <= b.length; j++) {
      const c = a[i - 1] === b[j - 1] ? 0 : 1;
      d[i][j] = Math.min(d[i - 1][j] + 1, d[i][j - 1] + 1, d[i - 1][j - 1] + c);
      if (i > 1 && j > 1 && a[i - 1] === b[j - 2] && a[i - 2] === b[j - 1]) d[i][j] = Math.min(d[i][j], d[i - 2][j - 2] + 1);
      row = Math.min(row, d[i][j]);
    }
    if (row > max) return max + 1;
  }
  return d[a.length][b.length];
}

/** How a query word `q` meets an indexed word `t`: a quality from QUALITY, or 0. `typos` allows the
 *  one-letter-off match (not used against transcript words, where it would find too much). */
export function quality(q, t, typos = true) {
  if (q === t) return QUALITY.exact;
  if (stem(q) === stem(t)) return QUALITY.plural;
  if (q.length >= 3 && t.startsWith(q)) return QUALITY.prefix;
  if (typos && q.length >= 5 && t.length >= 4) {
    const max = q.length >= 8 ? 2 : 1;
    if (q[0] === t[0] && distance(q, t, max) <= max) return QUALITY.typo;
  }
  return 0;
}

/**
 * Reads a query: its content words, and the kind and level filters it asks for.
 * @param {string} q
 * @returns {{ words: string[], kind: string, levels: string[], dropped: string[] }}
 */
export function parseQuery(q) {
  let ws = tokens(q);
  const dropped = [];
  let kind = '';
  let levels = [];
  const take = (phrases, set) => {
    for (const [ph, v] of phrases) {
      for (let i = 0; i + ph.length <= ws.length; i++) {
        if (ph.every((p, k) => ws[i + k] === p)) {
          if (set(v)) { dropped.push(...ws.slice(i, i + ph.length)); ws = [...ws.slice(0, i), ...ws.slice(i + ph.length)]; }
          return;
        }
      }
    }
  };
  // Two passes for each, so "first film" and "methods" in one query both count.
  for (let n = 0; n < 2; n++) take(KIND_PHRASES, (v) => (kind && kind !== v ? false : ((kind = v), true)));
  for (let n = 0; n < 2; n++) take(LEVEL_PHRASES, (v) => (levels.length ? false : ((levels = v), true)));
  const filmWords = ws.filter((w) => FILM_WORDS.has(w));
  ws = ws.filter((w) => !FILM_WORDS.has(w));
  const kept = ws.filter((w) => !LITTLE.has(w));
  return { words: kept.length ? kept : ws, kind, levels, dropped: [...dropped, ...filmWords] };
}

/* ---- the index */

const cache = new WeakMap();

/**
 * Builds (once per pair of objects) the word index for a film list and its search data.
 * @param {{ films: any[], courses?: Record<string,string>, levels?: Record<string,string> }} list
 * @param {any} [data] /films/search.json, or null
 */
export function prepare(list, data = null) {
  const key = data ?? list;
  let per = cache.get(list);
  if (!per) cache.set(list, (per = new WeakMap()));
  const hit = per.get(key);
  if (hit) return hit;

  const films = list.films;
  const courses = list.courses ?? {};
  const levels = list.levels ?? {};
  const fields = data?.fields ?? {};
  /** word -> Map(film index -> best weight) */
  const vocab = new Map();
  const titles = [];
  const isMethod = [];
  const add = (i, text, w) => {
    for (const t of tokens(text)) {
      let m = vocab.get(t);
      if (!m) vocab.set(t, (m = new Map()));
      if ((m.get(i) ?? 0) < w) m.set(i, w);
    }
  };
  films.forEach((f, i) => {
    const x = data?.films?.[f.f] ?? null;
    const lesson = x && x.L !== undefined ? data.lessons[x.L] : null;
    add(i, f.t, W.title);
    if (f.l) add(i, f.l, W.lesson);
    if (x?.m) add(i, x.m, W.method);
    if (f.c && courses[f.c]) add(i, courses[f.c], W.course);
    if (f.s) add(i, `${levels[f.s] ?? ''} ${LEVEL_WORDS[f.s] ?? ''}`, W.level);
    add(i, `${f.b ?? ''} ${KIND_WORDS[f.k] ?? ''}`, W.kind);
    // Fields: "neuroscience:0.83 cell-biology:0.4"; a film's own (a method film) or its lesson's.
    const fd = x?.fd ?? lesson?.fd ?? '';
    for (const part of fd.split(' ').filter(Boolean)) {
      const [k, v] = part.split(':');
      const w = Math.round(W.field * Math.min(1, (Number(v) || 0) / FIELD_TOP) * 100) / 100;
      if (w > 0) add(i, fields[k] ?? k.replace(/-/g, ' '), w);
    }
    if (lesson?.i) add(i, lesson.i, W.idea);
    if (lesson?.w) add(i, lesson.w, W.phrase);
    if (x?.x) add(i, x.x, W.take);
    if (f.th) add(i, f.th, W.take);
    if (x?.tr) add(i, x.tr, W.transcript);
    titles.push({ t: fold(f.t).replace(/[^a-z0-9]+/g, ' '), l: fold(`${f.l ?? ''} ${x?.m ?? ''}`).replace(/[^a-z0-9]+/g, ' ') });
    isMethod.push(f.k === 'method' || !!x?.m);
  });
  const index = { films, vocab, words: [...vocab.keys()], titles, isMethod, hasData: !!data };
  per.set(key, index);
  return index;
}

/** Score of each film for one query word: Map(film index -> score). */
function wordScores(index, q) {
  const out = new Map();
  for (const t of index.words) {
    if (t[0] !== q[0] && !(q.length >= 5 && t.length >= 4)) continue; // a typo keeps the first letter too
    const base = quality(q, t, true);
    if (!base) continue;
    for (const [i, w] of index.vocab.get(t)) {
      // A typo against a transcript word is too loose: such a word is not counted.
      if (base === QUALITY.typo && w <= W.transcript) continue;
      const s = w * base;
      if ((out.get(i) ?? 0) < s) out.set(i, s);
    }
  }
  return out;
}

/**
 * Searches the films.
 * @param {ReturnType<typeof prepare>} index
 * @param {string} q
 * @param {{ kind?: string, level?: string, course?: string, partial?: boolean }} [opts] filters chosen outside the query
 * @returns {{ films: any[], full: number, kind: string, levels: string[], words: string[], scores: Map<any, number> }}
 */
export function searchFilms(index, q, opts = {}) {
  const parsed = parseQuery(q);
  const attempt = (words, kind, levels) => {
    const keep = (f, i) => {
      if (opts.kind && !(opts.kind === 'method' ? index.isMethod[i] : f.k === opts.kind)) return false;
      if (opts.level && f.s !== opts.level) return false;
      if (opts.course && f.c !== opts.course) return false;
      if (kind === 'method' && !index.isMethod[i]) return false;
      if (kind === 'second' && f.k !== 'second' && f.k !== 'series') return false;
      if (kind && kind !== 'method' && kind !== 'second' && f.k !== kind) return false;
      if (levels.length && !levels.includes(f.s)) return false;
      return true;
    };
    const scores = new Map();
    if (!words.length) {
      const out = index.films.filter(keep);
      for (const f of out) scores.set(f, 0);
      return { films: out, full: out.length, scores };
    }
    const per = words.map((w) => wordScores(index, w));
    const phrase = words.join(' ');
    const rows = [];
    index.films.forEach((f, i) => {
      if (!keep(f, i)) return;
      let n = 0;
      let s = 0;
      for (const m of per) { const v = m.get(i); if (v) { n++; s += v; } }
      if (!n) return;
      if (words.length > 1 || n === words.length) {
        const tt = ` ${index.titles[i].t} `;
        const ll = ` ${index.titles[i].l} `;
        if (tt.includes(` ${phrase} `)) s += 10; else if (tt.includes(` ${phrase}`)) s += 6;
        else if (ll.includes(` ${phrase} `)) s += 6;
      }
      rows.push({ f, i, n, s });
    });
    const need = words.length;
    const full = rows.filter((r) => r.n === need).sort((a, b) => b.s - a.s || a.i - b.i);
    const part = opts.partial === false || need < 2 ? []
      : rows.filter((r) => r.n === need - 1).sort((a, b) => b.s - a.s || a.i - b.i).slice(0, PARTIAL_MAX);
    for (const r of [...full, ...part]) scores.set(r.f, r.s);
    return { films: [...full, ...part].map((r) => r.f), full: full.length, scores };
  };

  let { words, kind, levels } = parsed;
  let r = attempt(words, kind, levels);
  // A filter that leaves nothing: read its words as plain words again ("scientific method").
  if (!r.films.length && (kind || levels.length)) {
    words = parsed.words.concat(parsed.dropped.filter((w) => !FILM_WORDS.has(w) && !LITTLE.has(w)));
    kind = '';
    levels = [];
    r = attempt(words, kind, levels);
  }
  return { ...r, kind, levels, words };
}
