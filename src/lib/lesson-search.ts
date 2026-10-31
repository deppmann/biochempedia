/**
 * Lesson search: one ranked list of lessons, from the title index and the full text.
 *
 * Framework-free on purpose (no DOM, no Astro): the search box (src/components/SiteSearch.astro), the
 * Node check (scripts/test-search.mjs) and the offline CLI (scripts/search-lessons.mjs) all run this
 * same file against the same index.
 *
 * FOR AI FEATURES. The curiosity router (/api/curious, branch `curiosity-router`, not on main) and
 * the future course planner can call `searchLessons()` in the browser and send the top passages to
 * Claude as retrieval context, so the model answers from the site's own text and links real
 * sections. Each LessonHit carries `spots`: the passages that matched, each with a plain-text excerpt
 * (`excerptText`), where it came from (`label`, `kind`) and a `url` that opens that exact spot with
 * the words highlighted. `formatForModel(hits)` turns hits into a block of text ready to paste into
 * a prompt. Nothing here talks to a server: the index is static files.
 *
 * Where the text comes from (see pagefind.yml and src/pages/lessons/[...slug].astro). A lesson page is
 * indexed from several regions: the prose, the "Explain at my level" texts, the stories, the
 * self-test questions, the "How we measure it" techniques and the film transcripts. A result links to
 * the heading it came from (ids sx-level-*, sx-story-*, sx-q-*, sx-tech-*, sx-film-*), and the lesson
 * page opens the dialog or fold that holds it.
 *
 * How lessons are ranked. Pagefind answers per page with a BM25-style score and the positions of the
 * matched words, before any page text is downloaded. Per lesson, with every part in 0 to 1:
 *
 *   P  Pagefind score, divided by the best score in the same search.
 *   X  nearness of the matched words: neighbouring positions (a phrase, or one word apart for a
 *      small word dropped from the query) count, so "health department" as a phrase beats the two
 *      words in different paragraphs. Only for queries of two or more words.
 *   T  title evidence: the small title index (title, hook, headings, objectives, scientist, technique
 *      and structure names), scaled to the number of words, plus a little more when the query is the
 *      title itself (so "action potential" puts the lesson of that name above one that only uses the words).
 *   C  coverage: the share of the query's words the lesson has. Pagefind needs every word, so a full
 *      match is 1; when fewer than PARTIAL_BELOW lessons have every word, lessons with all but one
 *      word are added with C = (n-1)/n so a misspelled word does not empty the list.
 *
 *   score = C^2 * (W.pf * P + W.near * X + W.title * T)
 *
 * Why these numbers: see RANKING and W below, and scripts/test-search.mjs, which holds the queries
 * they were tuned on.
 */

// ---------------------------------------------------------------- types

/** One record of /search-index.json (src/pages/search-index.json.ts). */
export interface IndexRec { s: string; c: string; n: number; t: string; u: string; k: string; h: string; x: string; g: [string, string][] }
export interface SearchIndex { courses: { s: string; t: string }[]; lessons: IndexRec[] }

/** The slice of Pagefind's client API used here. */
export interface PfSub {
  title: string;
  url: string;
  excerpt: string;
  anchor?: { id: string };
  weighted_locations?: { weight: number; balanced_score: number }[];
}
export interface PfData { url: string; meta: { title?: string }; excerpt: string; sub_results: PfSub[] }
export interface PfResult { id: string; score: number; words: number[]; data(): Promise<PfData> }
export interface Pf {
  options(o: object): Promise<void>;
  search(q: string | null, o?: object): Promise<{ results: PfResult[] }>;
}

/** Where the files come from. The browser engine fetches them; Node scripts read them from dist/. */
export interface Engine {
  index(): Promise<SearchIndex>;
  /** Resolves to null when there is no full-text index (for example in `astro dev` before a build). */
  pagefind(): Promise<Pf | null>;
  /** { Pagefind result id: lesson slug }, written at build time. Optional: see scripts/pagefind-page-map.mjs. */
  pageMap?(): Promise<Record<string, string> | null>;
}

export type SpotKind = 'section' | 'level' | 'story' | 'quiz' | 'method' | 'film' | 'text';

/** A place in a lesson where the words were found. */
export interface Spot {
  /** What a reader sees: the section heading, "Story: …", "Explain at my level: …", "Self-test: question 4",
   *  "How we measure it: …", "Film transcript: …". */
  label: string;
  kind: SpotKind;
  /** Opens that spot, with the words highlighted. */
  url: string;
  excerptText: string;
  /** The same excerpt with the matched words in <mark>. Safe to insert as HTML (Pagefind escapes the text). */
  excerptHtml: string;
}

export interface LessonHit {
  slug: string;
  title: string;
  course: string;
  courseTitle: string;
  /** Unit within the course, and the lesson's number in the course. */
  unit: string;
  n: number;
  hook: string;
  url: string;
  score: number;
  /** Share of the query's words this lesson has (1 = all). */
  coverage: number;
  /** Section headings the title index matched, [text, anchor]. */
  headings: [string, string][];
  spots: Spot[];
  /** The parts of the score, for tuning and tests. */
  parts: { P: number; X: number; T: number; C: number };
}

export interface SearchOptions {
  /** A course slug, or 'all' (default). */
  scope?: string;
  /** How many lessons to return (default 8). */
  limit?: number;
  /** Words of context in each excerpt (Pagefind's default is 30). */
  excerptLength?: number;
}

// ---------------------------------------------------------------- tuning

/** Pagefind ranking. Defaults are pageLength 0.75, termFrequency 1, termSaturation 1.4, termSimilarity 1.
 *  pageLength 0.3: a long lesson is not penalised for being long (a lesson now includes its stories,
 *  levels and quiz, so most pages are long, and the default made the shortest page win a tie).
 *  termSimilarity 3: an exact word outweighs a stem or prefix relative ("department" over "departments").
 *  termSaturation 1.4 and termFrequency 1 are kept: the 11th mention of a word adds little. */
export const RANKING = { pageLength: 0.3, termFrequency: 1, termSaturation: 1.4, termSimilarity: 3 };

/** Weights of the three parts of the score; see the header. */
export const W = { pf: 1, near: 2, title: 1.5 };

/** Below this many full matches, lessons that lack one word are added. */
export const PARTIAL_BELOW = 10;
/** Most lessons added that way (a long tail of "has one of the words" is noise). */
export const PARTIAL_MAX = 10;
/** Most results ranked from Pagefind (the rest of its list is appended in its own order). */
export const RANKED_MAX = 80;
/** Characters before the lesson text is searched. */
export const TEXT_MIN = 3;

// ---------------------------------------------------------------- text helpers

export const norm = (s: string): string => s.toLowerCase().normalize('NFKD').replace(/[̀-ͯ]/g, '').replace(/[‐-―]/g, '-');

/** A token matches at the start of a word ("phos" finds "phosphorylation"), so short queries stay
 *  precise; "mapk" still finds "Ras-to-MAPK" because a hyphen starts a word. */
const hits = (hay: string, tok: string): boolean => {
  let i = hay.indexOf(tok);
  while (i !== -1) {
    if (i === 0 || !/[a-z0-9]/.test(hay[i - 1])) return true;
    i = hay.indexOf(tok, i + 1);
  }
  return false;
};

/** Pagefind needs every word of a query, and little words ("to", "a", "its") occur in every paragraph,
 *  which pulls snippets toward sentences that match only those. They are dropped, unless the query is
 *  in quotes (an exact phrase) or nothing else is left. */
const LITTLE = new Set('a an and are as at be by can do does for from how in into is it its of on or that the this to was were what when where which who why with'.split(' '));
export const textQuery = (raw: string): string => {
  if (raw.includes('"')) return raw;
  const words = raw.split(/\s+/).filter(Boolean);
  const kept = words.filter((w) => !LITTLE.has(w.toLowerCase()));
  return kept.length ? kept.join(' ') : raw;
};

/** Pagefind builds URLs from the folder it was loaded from; in Node that folder is a file: URL. Keep from /lessons/ on. */
const cleanUrl = (u: string): string => u.replace(/^.*?(\/lessons\/)/, '$1');

/** Removes `title` (plus a following full stop or colon) from the start of an excerpt, keeping the other <mark>s. */
const dropLeadingTitle = (html: string, title: string): string => {
  if (!stripMarks(html).startsWith(title)) return html;
  let left = title.length;
  let i = 0;
  while (i < html.length && left > 0) {
    if (html[i] === '<') { i = html.indexOf('>', i) + 1; continue; }
    const ent = /^&(?:amp|lt|gt|quot|#39);/.exec(html.slice(i, i + 6));
    i += ent ? ent[0].length : 1;
    left--;
  }
  return html.slice(i).replace(/^(?:<\/mark>)+/, '').replace(/^[.:]\s*/, '');
};

const stripMarks = (html: string): string =>
  html.replace(/<\/?mark>/g, '').replace(/&(amp|lt|gt|quot|#39);/g, (_m, e: string) => ({ amp: '&', lt: '<', gt: '>', quot: '"', '#39': "'" }[e] ?? _m));

// ---------------------------------------------------------------- the engine in a browser

/** Fetches /search-index.json and imports /pagefind/pagefind.js. Each is loaded once. */
export function browserEngine(base = ''): Engine {
  let index: Promise<SearchIndex> | null = null;
  let pf: Promise<Pf | null> | null = null;
  let map: Promise<Record<string, string> | null> | null = null;
  return {
    index: () => (index ??= fetch(`${base}/search-index.json`).then((r) => {
      if (!r.ok) throw new Error(String(r.status));
      return r.json() as Promise<SearchIndex>;
    })),
    pagefind: () => (pf ??= (async () => {
      try {
        const url = `${base}/pagefind/pagefind.js`;
        return (await import(/* @vite-ignore */ url)) as Pf;
      } catch { return null; }
    })()),
    pageMap: () => (map ??= fetch(`${base}/pagefind/page-map.json`).then((r) => (r.ok ? (r.json() as Promise<Record<string, string>>) : null)).catch(() => null)),
  };
}

// ---------------------------------------------------------------- the search

type Prepared = IndexRec & { nt: string; nh: string; nx: string; ng: string[] };

export interface TitleHit { rec: Prepared; raw: number; /** Extra evidence: the whole query is the title (0.5) or inside it (0.3). */ bonus: number; heads: [string, string][] }

/** One lesson found in the text, before its fragment is downloaded. */
interface Cand {
  slug: string;
  /** Pagefind score divided by the best score of the search it came from. */
  rel: number;
  words: number[];
  cov: number;
  result: PfResult;
}

export interface TextResult {
  state: 'ok' | 'off';
  /** Words searched (little words dropped). */
  terms: string[];
  cands: Cand[];
  /** Pagefind results past RANKED_MAX, in its order. */
  rest: Cand[];
}

export interface Ranked {
  slug: string;
  rec: Prepared;
  score: number;
  coverage: number;
  heads: [string, string][];
  cand: Cand | null;
  parts: LessonHit['parts'];
}

const KINDS: [RegExp, SpotKind][] = [
  [/^sx-level-/, 'level'], [/^sx-story-/, 'story'], [/^sx-q-/, 'quiz'], [/^sx-tech-/, 'method'], [/^sx-film-/, 'film'],
];

export function createLessonSearch(engine: Engine, defaults: { excerptLength?: number } = {}) {
  let prepared: Prepared[] | null = null;
  let courses: SearchIndex['courses'] = [];
  let bySlug = new Map<string, Prepared>();
  const configured = new WeakSet<Pf>();
  const dataOf = new WeakMap<PfResult, Promise<PfData>>();

  const load = async (): Promise<void> => {
    if (prepared) return;
    const idx = await engine.index();
    courses = idx.courses;
    prepared = idx.lessons.map((r) => ({ ...r, nt: norm(r.t), nh: norm(`${r.h} ${r.k} ${r.u}`), nx: norm(r.x), ng: r.g.map((g) => norm(g[0])) }));
    bySlug = new Map(prepared.map((r) => [r.s, r]));
  };
  const courseTitle = (s: string): string => courses.find((c) => c.s === s)?.t ?? s;

  const pagefind = async (): Promise<Pf | null> => {
    const pf = await engine.pagefind();
    if (pf && !configured.has(pf)) {
      configured.add(pf);
      // highlightParam makes each result link carry ?pagefind-highlight=… so the lesson page can mark the words.
      const o: Record<string, unknown> = { highlightParam: 'pagefind-highlight', ranking: RANKING };
      if (defaults.excerptLength) o.excerptLength = defaults.excerptLength;
      await pf.options(o);
    }
    return pf;
  };
  const fetchData = (r: PfResult): Promise<PfData> => {
    let p = dataOf.get(r);
    if (!p) { p = r.data(); dataOf.set(r, p); }
    return p;
  };

  /** Title, hook, heading, objective and name matches. Every word must match somewhere. Instant once the index has loaded. */
  function titleMatches(query: string, scope = 'all'): TitleHit[] {
    const q = norm(query).replace(/"/g, ' ').replace(/\s+/g, ' ').trim();
    if (!q || !prepared) return [];
    const toks = q.split(/\s+/).filter(Boolean);
    const out: TitleHit[] = [];
    for (const r of prepared) {
      if (scope !== 'all' && r.c !== scope) continue;
      let raw = 0;
      let all = true;
      const heads = new Set<number>();
      for (const tok of toks) {
        let s = 0;
        if (hits(r.nt, tok)) s += 10;
        r.ng.forEach((g, i) => { if (hits(g, tok)) { s += 4; heads.add(i); } });
        if (hits(r.nh, tok)) s += 3;
        if (hits(r.nx, tok)) s += 2;
        if (s === 0) { all = false; break; }
        raw += s;
      }
      if (!all) continue;
      // The whole phrase in the title is the best answer there is.
      if (toks.length > 1 && r.nt.includes(q)) raw += 15;
      const bonus = r.nt === q ? 0.5 : toks.length > 1 && r.nt.includes(q) ? 0.3 : 0;
      out.push({ rec: r, raw, bonus, heads: [...heads].slice(0, 3).map((i) => r.g[i]) });
    }
    out.sort((a, b) => b.raw - a.raw || a.rec.c.localeCompare(b.rec.c) || a.rec.n - b.rec.n);
    return out;
  }

  /** Turns Pagefind results into candidates. The lesson of each is known from the page map; without
   *  one, the fragments of the best RANKED_MAX are fetched to learn it and the rest are dropped. */
  async function toCands(results: PfResult[], cov: number): Promise<Cand[]> {
    if (!results.length) return [];
    const best = results[0].score || 1;
    const map = (await engine.pageMap?.()) ?? null;
    const out: Cand[] = [];
    if (map) {
      // A result the map does not know (a map cached from an older build) is looked up from its
      // fragment instead of being dropped.
      const missing: PfResult[] = [];
      for (const r of results) {
        const slug = map[r.id];
        if (slug) out.push({ slug, rel: r.score / best, words: r.words, cov, result: r });
        else missing.push(r);
      }
      const look = missing.slice(0, RANKED_MAX);
      const datas = await Promise.all(look.map(fetchData));
      look.forEach((r, i) => {
        const slug = /\/lessons\/([^/?#]+)/.exec(datas[i].url)?.[1];
        if (slug) out.push({ slug, rel: r.score / best, words: r.words, cov, result: r });
      });
    } else {
      const top = results.slice(0, RANKED_MAX);
      const datas = await Promise.all(top.map(fetchData));
      top.forEach((r, i) => {
        const slug = /\/lessons\/([^/?#]+)/.exec(datas[i].url)?.[1];
        if (slug) out.push({ slug, rel: r.score / best, words: r.words, cov, result: r });
      });
    }
    return out;
  }

  /** Full-text search through Pagefind. Needs the title index loaded only for its scope check. */
  async function textSearch(query: string, scope = 'all'): Promise<TextResult> {
    const raw = query.trim();
    const q = textQuery(raw);
    const terms = q.replace(/"/g, ' ').split(/\s+/).filter(Boolean);
    const pf = await pagefind();
    if (!pf) return { state: 'off', terms, cands: [], rest: [] };
    const opts = scope === 'all' ? {} : { filters: { course: scope } };
    const full = await pf.search(q, opts);
    const cands = await toCands(full.results, 1);
    // Few lessons have every word: also offer the ones that lack a single word (not for an exact phrase).
    if (!raw.includes('"') && terms.length >= 2 && terms.length <= 4 && cands.length < PARTIAL_BELOW) {
      const subsets = terms.length === 2 ? terms.map((t) => [t]) : terms.map((_, i) => terms.filter((_x, j) => j !== i));
      const seen = new Set(cands.map((c) => c.slug));
      const parts = await Promise.all(subsets.map((s) => pf.search(s.join(' '), opts).then((r) => toCands(r.results.slice(0, 40), s.length / terms.length))));
      let added = 0;
      for (const c of parts.flat().sort((a, b) => b.rel * b.cov - a.rel * a.cov)) {
        if (seen.has(c.slug) || added >= PARTIAL_MAX) continue;
        seen.add(c.slug);
        cands.push(c);
        added++;
      }
    }
    return { state: 'ok', terms, cands: cands.slice(0, RANKED_MAX), rest: cands.slice(RANKED_MAX) };
  }

  /** How close together the matched words sit, 0 to 1. Pagefind gives the word positions of every match,
   *  not which query word each was; for a phrase the matches are neighbours. One word apart still counts
   *  well (a small word was dropped from the query), a few apart a little. */
  function nearness(words: number[], nTerms: number): number {
    if (nTerms < 2 || words.length < 2) return 0;
    const p = [...new Set(words)].sort((a, b) => a - b);
    let pairs = 0;
    for (let i = 1; i < p.length; i++) {
      const gap = p[i] - p[i - 1];
      pairs += gap === 1 ? 1 : gap === 2 ? 0.6 : gap <= 5 ? 0.2 : 0;
    }
    // Each further pair adds less; a three-word phrase has two pairs, so it is scaled per pair.
    return 1 - Math.pow(0.5, pairs / (nTerms - 1));
  }

  /** One list from both sources, best first. Pure and synchronous. */
  function rank(query: string, titles: TitleHit[], text: TextResult | null): Ranked[] {
    const raw = query.trim();
    const nTerms = Math.max(1, text?.terms.length || norm(raw).split(/\s+/).filter(Boolean).length);
    const phrase = raw.includes('"');
    const map = new Map<string, Ranked>();
    const get = (slug: string): Ranked | null => {
      let e = map.get(slug);
      if (!e) {
        const rec = bySlug.get(slug);
        if (!rec) return null;
        e = { slug, rec, score: 0, coverage: 0, heads: [], cand: null, parts: { P: 0, X: 0, T: 0, C: 0 } };
        map.set(slug, e);
      }
      return e;
    };
    const toks = norm(raw).split(/\s+/).filter(Boolean).length || 1;
    for (const t of titles) {
      const e = get(t.rec.s)!;
      e.heads = t.heads;
      e.parts.T = Math.min(1, t.raw / (19 * toks)) + t.bonus;
      e.parts.C = 1;
    }
    for (const c of text?.cands ?? []) {
      const e = get(c.slug);
      if (!e) continue;
      e.cand = c;
      e.parts.P = c.rel;
      e.parts.X = phrase ? 0 : nearness(c.words, nTerms);
      e.parts.C = Math.max(e.parts.C, c.cov);
    }
    const out = [...map.values()];
    for (const e of out) {
      const { P, X, T, C } = e.parts;
      e.coverage = C;
      e.score = C * C * (W.pf * P + W.near * X + W.title * T);
    }
    out.sort((a, b) => b.score - a.score || (b.cand?.rel ?? 0) - (a.cand?.rel ?? 0) || a.rec.c.localeCompare(b.rec.c) || a.rec.n - b.rec.n);
    // Beyond the ranked part, Pagefind's own order.
    for (const c of text?.rest ?? []) {
      const e = get(c.slug);
      if (e && !e.cand) { e.cand = c; e.parts.P = c.rel; e.parts.C = c.cov; e.coverage = c.cov; e.score = 0; out.push(e); }
    }
    return out;
  }

  /** Where in a lesson the words were found: the best three sections, each with its excerpt. */
  function spotsOf(d: PfData): Spot[] {
    const subs = d.sub_results.filter((s) => s.excerpt);
    if (!subs.length) {
      return d.excerpt ? [{ label: 'Lesson text', kind: 'text', url: cleanUrl(d.url), excerptText: stripMarks(d.excerpt), excerptHtml: d.excerpt }] : [];
    }
    // Pagefind lists a page's sections in reading order. Best first: the section whose excerpt holds the
    // most different query words, then the one where rare words weigh most (its weights include the
    // region weights, so the prose beats a quiz question on a tie).
    const stem = (m: string) => m.replace(/<\/?mark>/g, '').toLowerCase().replace(/[’']s$/, '').replace(/[^a-z0-9]+$/, '').replace(/s$/, '');
    const distinct = (h: PfSub) => new Set((h.excerpt.match(/<mark>.*?<\/mark>/g) ?? []).map(stem)).size;
    const strength = (h: PfSub) => (h.weighted_locations ?? []).reduce((a, l) => a + l.balanced_score * l.weight, 0);
    return [...subs].sort((a, b) => distinct(b) - distinct(a) || strength(b) - strength(a)).slice(0, 3).map((s) => {
      const id = s.anchor?.id ?? /#(.+)$/.exec(s.url)?.[1] ?? '';
      const kind = KINDS.find(([re]) => re.test(id))?.[1] ?? 'section';
      const label = kind === 'method' ? `How we measure it: ${s.title}` : s.title;
      // A technique's heading is the first words of its excerpt: say it once, in the label.
      const trimmed = kind === 'method' ? dropLeadingTitle(s.excerpt, s.title) : s.excerpt;
      const html = /<mark>/.test(trimmed) ? trimmed : s.excerpt;   // unless that removed the only match
      return { label, kind, url: cleanUrl(s.url), excerptText: stripMarks(html), excerptHtml: html };
    });
  }

  /** Builds the lessons for a slice of a ranked list, downloading each page's fragment for its excerpts. */
  async function hydrate(slice: Ranked[]): Promise<LessonHit[]> {
    const datas = await Promise.all(slice.map((e) => (e.cand ? fetchData(e.cand.result) : Promise.resolve(null))));
    return slice.map((e, i) => ({
      slug: e.slug,
      title: e.rec.t,
      course: e.rec.c,
      courseTitle: courseTitle(e.rec.c),
      unit: e.rec.u,
      n: e.rec.n,
      hook: e.rec.h,
      url: `/lessons/${e.slug}/`,
      score: e.score,
      coverage: e.coverage,
      headings: e.heads,
      spots: datas[i] ? spotsOf(datas[i]!) : [],
      parts: e.parts,
    }));
  }

  return { load, courses: () => courses, courseTitle, titleMatches, textSearch, rank, hydrate };
}

// ---------------------------------------------------------------- the one-call version

const shared = new WeakMap<Engine, ReturnType<typeof createLessonSearch>>();

/** Searches every lesson (or one course) and returns the best `limit`, each with the passages that matched.
 *  In a browser, `engine` defaults to browserEngine(). Never throws for a missing full-text index: the
 *  hits then come from titles and headings alone (their `spots` are empty). */
export async function searchLessons(query: string, opts: SearchOptions & { engine?: Engine } = {}): Promise<LessonHit[]> {
  const engine = opts.engine ?? (defaultEngine ??= browserEngine());
  let s = shared.get(engine);
  if (!s) { s = createLessonSearch(engine, { excerptLength: opts.excerptLength }); shared.set(engine, s); }
  const q = query.trim();
  if (!q) return [];
  await s.load();
  const scope = opts.scope ?? 'all';
  const titles = s.titleMatches(q, scope);
  const text = q.length >= TEXT_MIN ? await s.textSearch(q, scope) : null;
  return s.hydrate(s.rank(q, titles, text).slice(0, opts.limit ?? 8));
}
let defaultEngine: Engine | undefined;

/** Hits as plain text for a prompt: lesson, then each passage with where it is and its link. */
export function formatForModel(hits: LessonHit[], origin = ''): string {
  return hits.map((h) => {
    const head = `${h.title} (${h.courseTitle}) ${origin}${h.url}`;
    const spots = h.spots.length ? h.spots.map((s) => `  - ${s.label}: ${s.excerptText} [${origin}${s.url}]`).join('\n') : `  - ${h.hook}`;
    return `${head}\n${spots}`;
  }).join('\n\n');
}
