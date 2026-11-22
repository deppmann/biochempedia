/**
 * Typed search (2026-11-22): films, methods, Side Hops, flashcards, simulations and the math toolkit,
 * each found and ranked on its own, from the same Pagefind index as the lessons.
 *
 * Lessons keep their own, tuned ranking (src/lib/lesson-search.ts). This file searches every OTHER
 * type: one Pagefind query per ticked type, narrowed by the `type` filter (and the course, when a
 * course chip is on), so each group has its own count and its own best-first order. What the index
 * holds and how a record is weighted (title over heading over script): src/lib/search-records.mjs.
 *
 * Like the lesson search it is framework-free (no DOM), so the /search/ tick boxes
 * (src/components/SearchTypes.astro), the films page (src/components/FilmScriptSearch.astro) and Node
 * checks can share it.
 *
 * What a query can be:
 *   words      every word must be in the record, as typed, as the start of a longer word ("mito"),
 *              or one letter off (two for long words): "zebrafsh" still finds "zebrafish". Pagefind
 *              itself has no typo tolerance: for a word it does not know, it shortens the word until
 *              something starts with what is left, so matchedWords/realMatches below keep only the
 *              records whose matched words are really close to the ones typed (as the lesson search does).
 *   "a phrase" in quotes: those words next to each other, exactly.
 * When nothing has every word of a two- to four-word query, records with all but one are offered,
 * marked as partial.
 */
import { norm, wordMatch, textQuery, RANKING, type Pf, type PfData, type PfResult } from './lesson-search';
import { SEARCH_TYPES, secondsOfId, filmAt } from './search-records.mjs';

export type TypeKey = 'lesson' | 'ladder' | 'film' | 'sidehop' | 'method' | 'flashcards' | 'sim' | 'toolkit';
export const TYPES = SEARCH_TYPES as { key: TypeKey; label: string; one: string; many: string; group: 'main' | 'more' }[];
export const ALL_TYPES = TYPES.map((t) => t.key);
export const typeOf = (k: string) => TYPES.find((t) => t.key === k);

/** A place inside a hit where the words are: a film's line (with the second it is said at), a
 *  section, or the record's best excerpt. `html` is Pagefind's excerpt, escaped, with <mark>s. */
export interface Line { label: string; url: string; html: string; at: number | null }

export interface TypedHit {
  type: TypeKey;
  title: string;
  url: string;
  kicker: string;
  /** Course · level · lesson, as known. */
  where: string;
  ladder?: string;
  poster?: string;
  dur?: number;
  /** A ladder: how many films it plays. */
  films?: number;
  lines: Line[];
  partial: boolean;
}

export interface Group {
  type: TypeKey;
  /** How many records of this type match (every word, or all but one when `partial`). */
  count: number;
  partial: boolean;
  hits: TypedHit[];
  /** Results not drawn yet, in rank order. */
  rest: PfResult[];
}

/** How many hits a group shows at first, and adds per "Show more". */
export const GROUP_PAGE = 5;
/** Pages read to tell a typo from a word nobody wrote (see realMatches). */
const TYPO_CHECK = 12;

const bare = (s: string): string => norm(s).replace(/[^\p{L}\p{N}]+/gu, '');

/** Reads the URL's search state: ?q=…&types=film,sidehop. No `types` means every type. */
export function readState(search: string): { q: string; types: TypeKey[] } {
  const p = new URLSearchParams(search);
  const raw = p.get('types');
  const types = raw == null ? [...ALL_TYPES] : raw.split(',').filter((t): t is TypeKey => (ALL_TYPES as string[]).includes(t));
  return { q: p.get('q') ?? '', types };
}
/** The query string for a state; `types` is left out when every type is on. */
export function writeState(base: string, q: string, types: TypeKey[]): string {
  const p = new URLSearchParams(base);
  if (q) p.set('q', q); else p.delete('q');
  if (types.length === ALL_TYPES.length) p.delete('types'); else p.set('types', ALL_TYPES.filter((t) => types.includes(t)).join(','));
  const s = p.toString();
  return s ? `?${s}` : '';
}

export function createTypedSearch(loadPagefind: () => Promise<Pf | null>) {
  let configured = false;
  const dataOf = new WeakMap<PfResult, Promise<PfData>>();
  const fetchData = (r: PfResult): Promise<PfData> => {
    let p = dataOf.get(r);
    if (!p) { p = r.data(); dataOf.set(r, p); }
    return p;
  };
  const pagefind = async (): Promise<Pf | null> => {
    const pf = await loadPagefind();
    if (pf && !configured) {
      configured = true;
      // The same options the lesson search sets (one Pagefind per page), so the order of loading does not matter.
      await pf.options({ highlightParam: 'pagefind-highlight', ranking: RANKING });
    }
    return pf;
  };

  async function matchedWords(r: PfResult): Promise<Set<string>> {
    const d = await fetchData(r);
    const text = d.raw_content ?? d.content ?? '';
    const all = text.includes('​') ? text.split('​') : text.split(/[\r\n\s]+/g);
    const out = new Set<string>();
    const add = (w: string | undefined) => {
      if (!w) return;
      for (const piece of norm(w).split(/[^\p{L}\p{N}]+/u)) if (piece) out.add(piece);
      out.add(bare(w));
    };
    for (const i of r.words) add(all[i]);
    for (const f of r.matchedMetaFields ?? []) for (const w of (d.meta?.[f] ?? '').split(/\s+/)) add(w);
    return out;
  }

  /** Keeps only records where every query word was really matched (or is one or two letters off). */
  async function realMatches(results: PfResult[], terms: string[]): Promise<PfResult[]> {
    const want = terms.map(bare).filter(Boolean);
    if (!results.length || !want.length) return results;
    const check = async (r: PfResult, close: boolean) => {
      const words = [...(await matchedWords(r))];
      return want.every((t) => words.some((w) => { const m = wordMatch(t, w); return m === 'yes' || (close && m === 'close'); }));
    };
    if (await check(results[0], false)) return results;
    const top = results.slice(0, TYPO_CHECK);
    const keep = await Promise.all(top.map((r) => check(r, true)));
    return top.filter((_r, i) => keep[i]);
  }

  /** One hit, from its fragment: the record's fields and the lines where the words are. */
  async function toHit(type: TypeKey, r: PfResult, partial: boolean): Promise<TypedHit> {
    const d = await fetchData(r);
    const m = d.meta ?? {};
    const url = d.url.replace(/^.*?(?=\/(?:lessons|watch|methods|math-toolkit|films)\/)/, '');
    const marks = (h: string) => new Set((h.match(/<mark>.*?<\/mark>/g) ?? []).map((x) => x.toLowerCase())).size;
    const subs = (d.sub_results ?? []).filter((s) => /<mark>/.test(s.excerpt));
    const lines: Line[] = [...subs]
      .sort((a, b) => marks(b.excerpt) - marks(a.excerpt))
      .slice(0, 2)
      .map((s) => {
        const id = s.anchor?.id ?? /#([^#]+)$/.exec(s.url)?.[1] ?? '';
        const at = secondsOfId(id);
        const subUrl = s.url.replace(/^.*?(?=\/(?:lessons|watch|methods|math-toolkit|films)\/)/, '');
        const link = at != null && m.filmKey ? filmAt(url, m.filmKey, at) : subUrl;
        const label = at != null ? `at ${s.title}` : s.title === m.title ? '' : s.title;
        return { label, url: link, html: s.excerpt, at };
      });
    if (!lines.length && d.excerpt) lines.push({ label: '', url, html: d.excerpt, at: null });
    const where = [m.courseTitle, m.levelTitle, m.lesson && m.lesson !== m.title ? m.lesson : ''].filter(Boolean).join(' · ');
    return {
      type,
      title: m.title ?? url,
      url,
      kicker: m.kicker ?? typeOf(type)?.one ?? '',
      where,
      ...(m.ladder ? { ladder: m.ladder } : {}),
      ...(m.poster ? { poster: m.poster } : {}),
      ...(m.dur ? { dur: Number(m.dur) } : {}),
      ...(m.films ? { films: Number(m.films) } : {}),
      lines,
      partial,
    };
  }

  /** Searches one type. */
  async function searchType(pf: Pf, raw: string, type: TypeKey, scope: string): Promise<Group> {
    const q = textQuery(raw);
    const phrase = raw.includes('"');
    const terms = q.replace(/"/g, ' ').split(/\s+/).filter(Boolean);
    const filters: Record<string, string> = { type };
    if (scope !== 'all') filters.course = scope;
    const real = (rs: PfResult[], ts: string[]) => (phrase ? Promise.resolve(rs) : realMatches(rs, ts));
    let results = await real((await pf.search(q, { filters })).results, terms);
    let partial = false;
    if (!results.length && !phrase && terms.length >= 2 && terms.length <= 4) {
      const subsets = terms.map((_, i) => terms.filter((_x, j) => j !== i));
      const found = await Promise.all(subsets.map((s) => pf.search(s.join(' '), { filters }).then((r) => real(r.results, s))));
      const seen = new Set<string>();
      results = found.flat().sort((a, b) => b.score - a.score).filter((r) => (seen.has(r.id) ? false : (seen.add(r.id), true)));
      partial = results.length > 0;
    }
    const first = results.slice(0, GROUP_PAGE);
    const hits = await Promise.all(first.map((r) => toHit(type, r, partial)));
    return { type, count: results.length, partial, hits, rest: results.slice(GROUP_PAGE) };
  }

  /** Every ticked type except lessons, in TYPES order. Resolves to null when there is no index here. */
  async function search(raw: string, types: TypeKey[], scope = 'all'): Promise<Group[] | null> {
    const query = raw.trim();
    if (!query) return [];
    const pf = await pagefind();
    if (!pf) return null;
    const want = TYPES.map((t) => t.key).filter((k) => k !== 'lesson' && types.includes(k));
    return Promise.all(want.map((t) => searchType(pf, query, t, scope)));
  }

  /** The next page of a group, in place. */
  async function more(g: Group): Promise<void> {
    const next = g.rest.splice(0, GROUP_PAGE);
    g.hits.push(...(await Promise.all(next.map((r) => toHit(g.type, r, g.partial)))));
  }

  return { search, more, load: pagefind };
}

/** The browser's Pagefind, loaded once per page (the same module the lesson search imports). */
let pfPromise: Promise<Pf | null> | null = null;
export const browserPagefind = (): Promise<Pf | null> => (pfPromise ??= (async () => {
  try {
    const url = '/pagefind/pagefind.js';
    return (await import(/* @vite-ignore */ url)) as Pf;
  } catch { return null; }
})());

/** Is every word of the query in this title (as a word start, a plural or a near miss)? A ladder whose
 *  title matches is listed above the single films (Chris, 2026-11-22: ladders come up in searches). */
export function titleHas(title: string, query: string): boolean {
  const words = norm(title).split(/[^\p{L}\p{N}]+/u).filter(Boolean);
  const terms = norm(textQuery(query)).replace(/"/g, ' ').split(/\s+/).map(bare).filter(Boolean);
  return terms.length > 0 && terms.every((t) => words.some((w) => wordMatch(t, w) !== 'no'));
}

/** "1:15" */
export const clockOf = (sec: number) => `${Math.floor(sec / 60)}:${String(Math.floor(sec % 60)).padStart(2, '0')}`;
