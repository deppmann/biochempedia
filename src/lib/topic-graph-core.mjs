/* The hop graph: the logic every reader of src/data/topic-graph.json shares, with no Node and no
   Astro imports, so the same code runs in three places: the site build (src/lib/topic-graph.ts),
   the public endpoint (/graph.json) and the offline tools and tests (scripts/topic-graph/).

   The graph file holds only ids and reader-facing notes. Titles, courses, levels and film details
   are handed in here by the caller (from the content collection at build time, from the lesson
   files in the tools), so the graph cannot drift from the lessons.

   A lesson with no record, a rung whose lesson is missing or unpublished, and an anchor that no
   longer matches a heading are all normal: each is skipped or degraded, never an error. */
import GithubSlugger from 'github-slugger';

// ------------------------------------------------------------------ heading ids

/** A heading's text as the page shows it, from its Markdown/MDX source line. */
export function headingText(raw) {
  return String(raw)
    .replace(/\s+#+\s*$/, '')
    .replace(/!\[([^\]]*)\]\([^)]*\)/g, '$1')
    .replace(/\[([^\]]+)\]\([^)]*\)/g, '$1')
    .replace(/<\/?[A-Za-z][^>]*>/g, '')
    .replace(/\{[^}]*\}/g, '')
    .replace(/`([^`]*)`/g, '$1')
    .replace(/(\*\*|__)(.+?)\1/g, '$2')
    .replace(/(^|[^\w*])\*([^*\s][^*]*?)\*(?=[^\w*]|$)/g, '$1$2')
    .replace(/(^|[^\w])_([^_\s][^_]*?)_(?=[^\w]|$)/g, '$1$2')
    .replace(/\\([\\`*_{}[\]()#+\-.!<>|~])/g, '$1')
    .replace(/&amp;/g, '&').replace(/&lt;/g, '<').replace(/&gt;/g, '>').replace(/&nbsp;/g, ' ').replace(/&quot;/g, '"').replace(/&#39;/g, "'")
    // What the page's Markdown pipeline does to the text before ids are made: typographic dashes
    // (which the id then drops) and keyboard subscripts such as E_K (src/lib/rehype-sub-sup.mjs).
    .replace(/---/g, '\u2014').replace(/--/g, '\u2013')
    .replace(/(?<![\p{L}\p{N}_.])([\p{L}\p{N}]{1,5})[_^]\{?([\p{L}\p{N}+\u2212-]{1,8})\}?(?![\p{L}\p{N}_])/gu, (_m, base, script) => (GREEK_WORDS[base] ?? base) + script)
    .trim();
}
const GREEK_WORDS = { pi: 'π', Pi: 'Π', psi: 'ψ', Psi: 'Ψ', tau: 'τ', Delta: 'Δ', delta: 'δ', lambda: 'λ', mu: 'μ', sigma: 'σ', Sigma: 'Σ', alpha: 'α', beta: 'β', gamma: 'γ', theta: 'θ', omega: 'ω' };

/**
 * Every heading of a lesson body, in order, with the id the built page gives it. The site's
 * Markdown pipeline names headings with github-slugger, one counter per page, so a repeated
 * heading gets "-1", "-2". scripts/check-topic-graph.mjs compares these ids with the built pages.
 * @param {string} body MDX source without frontmatter
 * @returns {{ depth: number, text: string, id: string, line: number }[]}
 */
export function headingIds(body) {
  const slugger = new GithubSlugger();
  const out = [];
  let fence = false;
  const lines = String(body).split('\n');
  for (let i = 0; i < lines.length; i++) {
    const line = lines[i];
    if (/^\s*(```|~~~)/.test(line)) { fence = !fence; continue; }
    if (fence) continue;
    const m = /^(#{1,6})\s+(.+?)\s*$/.exec(line);
    if (!m) continue;
    const text = headingText(m[2]);
    out.push({ depth: m[1].length, text, id: slugger.slug(text), line: i });
  }
  return out;
}

// ------------------------------------------------------------------ search folding

/** British spellings the lessons use, folded to one form so "colour" finds "color" and back. */
const SPELLING = [
  [/\b(col|behavi|tum|fav|flav|od|neighb|vap|lab|hum|harb|rum)our/g, '$1or'],
  [/\b(fib|cent|lit|met|theat|calib|tit)re(s?)\b/g, '$1er$2'],
  [/(\w{3,})is(e|ed|es|ing|ation|ations|er|ers)\b/g, '$1iz$2'],
  [/(\w{3,})ys(e|ed|es|ing)\b/g, '$1yz$2'],
  [/\bh?aem/g, 'hem'], [/\boes/g, 'es'], [/\bfoet/g, 'fet'], [/\bfaec/g, 'fec'], [/paed/g, 'ped'], [/anaem/g, 'anem'], [/leuk?aem/g, 'leukem'],
  [/sulph/g, 'sulf'], [/\bmould/g, 'mold'], [/\bgrey/g, 'gray'], [/\bmoult/g, 'molt'], [/ll(ed|ing)\b/g, 'l$1'],
];

/** Fold a phrase for matching: lower case, no accents, no punctuation, one spelling. The same
 *  function is applied to the index and to the query, so it only has to be consistent. */
export function fold(s) {
  let t = String(s ?? '').toLowerCase().normalize('NFKD').replace(/[̀-ͯ]/g, '').replace(/[^a-z0-9]+/g, ' ').trim();
  for (const [re, to] of SPELLING) t = t.replace(re, to);
  return t.replace(/\s+/g, ' ').trim();
}

const STOP = new Set(['a', 'an', 'the', 'of', 'in', 'on', 'to', 'do', 'does', 'is', 'are', 'and', 'or', 'how', 'why', 'what', 'when', 'where', 'my', 'your', 'you', 'i', 'it', 'for', 'with', 'from', 'at', 'by', 'be', 'get', 'can']);
const tokens = (folded) => folded.split(' ').filter((w) => w && !STOP.has(w));

/**
 * Rank concepts for a typed query against an index from api.searchIndex(). Whole-phrase and name
 * matches come first; then the share of the query's words found in a name or alias. Returns ids.
 * It is small on purpose: a consumer may ship it to the browser beside /graph.json.
 */
export function searchConcepts(index, query, limit = 8) {
  const q = fold(query);
  if (!q) return [];
  const qt = tokens(q);
  const scored = [];
  for (const row of index) {
    let best = 0;
    row.terms.forEach((term, i) => {
      const isName = i === 0;
      let s = 0;
      if (term === q) s = isName ? 100 : 90;
      else if (term.startsWith(q) || term.includes(` ${q}`) || q.includes(term)) s = isName ? 70 : 60;
      else if (qt.length) {
        const tt = tokens(term);
        const hit = qt.filter((w) => tt.some((x) => x === w || (w.length >= 4 && x.startsWith(w)) || (x.length >= 4 && w.startsWith(x)))).length;
        if (hit) s = (hit / qt.length) * (isName ? 50 : 40) + (hit === qt.length ? 10 : 0);
      }
      if (s > best) best = s;
    });
    if (best > 0) scored.push({ id: row.id, score: best + Math.min(row.levels.length, 5) * 0.1 });
  }
  return scored.sort((a, b) => b.score - a.score || a.id.localeCompare(b.id)).slice(0, limit).map((x) => x.id);
}

// ------------------------------------------------------------------ the joined view

/**
 * @typedef {{ slug: string, title: string, course: string, courseTitle: string, stage: string, stageTitle: string, rank: number, order?: number, hook?: string, headingIds?: Set<string> | string[] }} LessonInfo
 * @typedef {{ key: string, title: string, lesson: string, id?: string | null, durationSec: number, href: string, poster: string, kind?: string }} FilmInfo
 */

/**
 * Join a graph with the site's lessons and films.
 * @param {any} graph the parsed src/data/topic-graph.json (or anything of that shape)
 * @param {{ stages: { key: string, title: string }[], lessons: Map<string, LessonInfo>, films: Map<string, FilmInfo>, courses?: { slug: string, title: string, stage: string }[] }} site
 */
export function makeTopicGraph(graph, site) {
  const { stages, lessons, films } = site;
  const all = graph?.concepts ?? {};
  const areas = graph?.areas ?? [];
  const records = graph?.lessons ?? {};
  const stageTitle = (key) => stages.find((s) => s.key === key)?.title ?? key;
  const areaName = (id) => areas.find((a) => a.id === id)?.name ?? id;
  const hasAnchor = (l, anchor) => {
    if (!anchor) return false;
    const ids = l.headingIds;
    if (!ids) return true;                       // nothing to check against: trust the file
    return Array.isArray(ids) ? ids.includes(anchor) : ids.has(anchor);
  };
  const position = (l) => [l.rank, site.courses ? site.courses.findIndex((c) => c.slug === l.course) : 0, l.order ?? 0, l.slug];
  const byPosition = (a, b) => { const x = position(a), y = position(b); return x[0] - y[0] || x[1] - y[1] || x[2] - y[2] || String(x[3]).localeCompare(String(y[3])); };

  const concept = (id) => (all[id] ? { id, ...all[id] } : undefined);
  const concepts = Object.keys(all).map((id) => ({ id, ...all[id] }));

  /** The concepts a lesson belongs to, core first. Empty for a lesson with no record. */
  function conceptsOf(slug) {
    const out = [];
    for (const id of records[slug]?.concepts ?? []) {
      const c = all[id];
      const r = c?.rungs.find((x) => x.lesson === slug);
      if (c && r) out.push({ id, name: c.name, label: c.short ?? c.name, area: c.area, role: r.role, ...(r.anchor ? { anchor: r.anchor } : {}), ...(r.adds ? { adds: r.adds } : {}) });
    }
    // the record's own order is kept: the lesson's main idea first, then its other ideas, then what it uses
    return out.sort((a, b) => (a.role === b.role ? 0 : a.role === 'core' ? -1 : 1));
  }

  /** A concept's films joined with the catalog, lowest level first. Unknown keys are skipped. */
  function filmsFor(id) {
    const c = all[id];
    if (!c) return [];
    return c.films
      .flatMap((key, i) => {
        const f = films.get(key);
        const l = f ? lessons.get(f.lesson) : undefined;
        return f && l ? [{ ...f, lessonTitle: l.title, course: l.course, stage: l.stage, stageTitle: l.stageTitle, rank: l.rank, i, l }] : [];
      })
      .sort((a, b) => byPosition(a.l, b.l) || a.i - b.i)
      .map(({ i: _i, l: _l, ...f }) => f);
  }

  function joinRungs(id, role) {
    const c = all[id];
    if (!c) return [];
    const mine = filmsFor(id);
    return c.rungs
      .filter((r) => !role || r.role === role)
      .flatMap((r) => {
        const l = lessons.get(r.lesson);
        if (!l) return [];                          // missing or unpublished: skipped, never guessed at
        const anchor = hasAnchor(l, r.anchor) ? r.anchor : undefined;
        const { headingIds: _h, ...info } = l;
        return [{ ...info, lesson: r.lesson, role: r.role, ...(anchor ? { anchor } : {}), ...(r.adds ? { adds: r.adds } : {}), href: `/lessons/${l.slug}/${anchor ? `#${anchor}` : ''}`, films: mine.filter((f) => f.lesson === l.slug) }];
      })
      .sort(byPosition);
  }

  /**
   * A concept's ladder: its core rungs, lowest level first, each with the lesson's title, course
   * and level, the concept's films from that lesson, and the size of the step up to it:
   * `stepFromBelow` is how many levels above the nearest lower rung this one sits (1 = the next
   * level, 3 = two levels are missing in between; null on the lowest level).
   */
  function ladder(id) {
    const rungs = joinRungs(id, 'core');
    const ranks = [...new Set(rungs.map((r) => r.rank))].sort((a, b) => a - b);
    return rungs.map((r) => {
      const i = ranks.indexOf(r.rank);
      return { ...r, stepFromBelow: i > 0 ? r.rank - ranks[i - 1] : null, stepToAbove: i < ranks.length - 1 ? ranks[i + 1] - r.rank : null };
    });
  }

  /** Lessons that lean on the idea without teaching it ("also comes up in"), lowest level first. */
  const usedBy = (id) => joinRungs(id, 'uses');

  /** The ladder as one row per level. With `withGaps`, levels that have no lesson are included
   *  (empty, `gap: true` when they lie between two levels that do), so a hole can be drawn honestly. */
  function ladderByLevel(id, withGaps = false) {
    const rungs = ladder(id);
    const ranks = rungs.map((r) => r.rank);
    const lo = Math.min(...ranks), hi = Math.max(...ranks);
    return stages
      .map((s, rank) => ({ stage: s.key, stageTitle: s.title, rank, rungs: rungs.filter((r) => r.rank === rank), gap: false }))
      .map((g) => ({ ...g, gap: !g.rungs.length && rungs.length > 0 && g.rank > lo && g.rank < hi }))
      .filter((g) => withGaps || g.rungs.length);
  }

  /** Where a concept's ladder starts and stops, and the levels missing in between. */
  function span(id) {
    const rows = ladderByLevel(id, true);
    const have = rows.filter((g) => g.rungs.length);
    return { levels: have.map((g) => g.stage), lowest: have[0]?.stage ?? null, highest: have[have.length - 1]?.stage ?? null, gaps: rows.filter((g) => g.gap).map((g) => g.stage) };
  }

  /**
   * From one lesson, for each idea it teaches (core rungs only): the nearest level below and
   * above that has a lesson on the same idea, and the sideways hops to neighbouring ideas.
   *   down / up        the first lesson at that level, with `jump` (levels moved; 1 = next door)
   *   downAll / upAll  every lesson at that level (a rung can hold more than one)
   *   beside           other lessons on this idea at the reader's own level
   *   sideways         neighbouring ideas with the one-line reason and `to`: the lesson on that
   *                    idea nearest the reader's level (same level first, then below, then above)
   * No lesson below is a real, honest state ("no simpler version yet"): `down` is then undefined.
   */
  function hops(slug) {
    const here = lessons.get(slug);
    if (!here) return [];
    const out = [];
    for (const c of conceptsOf(slug)) {
      if (c.role !== 'core') continue;
      const rungs = ladder(c.id);
      const below = rungs.filter((r) => r.rank < here.rank);
      const above = rungs.filter((r) => r.rank > here.rank);
      const downRank = below.length ? below[below.length - 1].rank : null;
      const upRank = above.length ? above[0].rank : null;
      const downAll = below.filter((r) => r.rank === downRank).map((r) => ({ ...r, jump: here.rank - r.rank }));
      const upAll = above.filter((r) => r.rank === upRank).map((r) => ({ ...r, jump: r.rank - here.rank }));
      const sideways = (all[c.id].near ?? []).flatMap((n) => {
        const t = all[n.id];
        if (!t) return [];
        const theirs = ladder(n.id).filter((r) => r.slug !== slug);
        const to = theirs.slice().sort((a, b) => {
          const da = Math.abs(a.rank - here.rank) * 2 + (a.rank > here.rank ? 1 : 0);
          const db = Math.abs(b.rank - here.rank) * 2 + (b.rank > here.rank ? 1 : 0);
          return da - db;
        })[0];
        return [{ id: n.id, name: t.name, label: t.short ?? t.name, blurb: t.blurb, area: t.area, why: n.why, ...(to ? { to: { ...to, jump: to.rank - here.rank } } : {}) }];
      });
      out.push({
        id: c.id, name: c.name, label: c.label, area: c.area, ...(c.anchor ? { anchor: c.anchor } : {}), ...(c.adds ? { adds: c.adds } : {}),
        ...(downAll.length ? { down: downAll[0] } : {}), downAll,
        ...(upAll.length ? { up: upAll[0] } : {}), upAll,
        beside: rungs.filter((r) => r.rank === here.rank && r.slug !== slug),
        sideways,
      });
    }
    return out;
  }

  /** One row per concept for search over names and everyday phrases: `terms` are folded (see
   *  fold()), the name first, then the aliases. Pair it with searchConcepts(). */
  function searchIndex() {
    return concepts.map((c) => {
      const s = span(c.id);
      return { id: c.id, name: c.name, label: c.short ?? c.name, blurb: c.blurb, area: c.area, areaName: areaName(c.area), terms: [fold(c.name), ...c.aliases.map(fold)], aliases: c.aliases, levels: s.levels, films: filmsFor(c.id).length };
    });
  }

  /**
   * The graph for browsers (/graph/all.json, and one area's share in /graph/<area>.json): compact. Lessons, films and courses are
   * written once in tables and pointed at by index, because a lesson sits on more than one rung.
   *   stages   [key, title]
   *   areas    [id, name]
   *   courses  [slug, title, stage index]
   *   lessons  [slug, title, course index]                      (only lessons that have a record)
   *   films    [key, title, lesson index, seconds, film id or 0]  (0 = the lesson's first film)
   *   concepts { id, n name, h short display name (absent when the name is short), b blurb, a area index, s subject (absent = biology), q aliases,
   *              r rungs [lesson index, 0 core | 1 uses, note, anchor], f film indexes,
   *              x near [concept index, why] }
   * Rungs are sorted lowest level first; a level is lessons[i] -> courses[j] -> stages[k].
   * `only` (a list of concept ids) limits the concepts (one area's file): the tables then hold only
   * what those concepts use, and near targets are written as concept ids, since a neighbour may
   * live in another file.
   */
  function clientGraph(only) {
    const ids = (only ?? Object.keys(all)).filter((id) => all[id]);
    const allIds = Object.keys(all);
    const stageIdx = new Map(stages.map((s, i) => [s.key, i]));
    const courseRows = [], courseIdx = new Map();
    const lessonRows = [], lessonIdx = new Map();
    const filmRows = [], filmIdx = new Map();
    const course = (l) => {
      if (!courseIdx.has(l.course)) { courseIdx.set(l.course, courseRows.length); courseRows.push([l.course, l.courseTitle, stageIdx.get(l.stage) ?? -1]); }
      return courseIdx.get(l.course);
    };
    const lesson = (l) => {
      if (!lessonIdx.has(l.slug)) { lessonIdx.set(l.slug, lessonRows.length); lessonRows.push([l.slug, l.title, course(l)]); }
      return lessonIdx.get(l.slug);
    };
    // Tables in a fixed order (level, course, lesson) so the file is stable between builds.
    const used = new Set(ids.flatMap((id) => all[id].rungs.map((r) => r.lesson)));
    for (const l of [...used].map((s) => lessons.get(s)).filter(Boolean).sort(byPosition)) lesson(l);
    const out = ids.map((id) => {
      const c = all[id];
      const rungs = [...joinRungs(id, 'core'), ...joinRungs(id, 'uses')];
      const fs = filmsFor(id).map((f) => {
        if (!filmIdx.has(f.key)) { filmIdx.set(f.key, filmRows.length); filmRows.push([f.key, f.title, lessonIdx.get(f.lesson), Math.round(f.durationSec), f.id ?? 0]); }
        return filmIdx.get(f.key);
      });
      return {
        id, n: c.name, ...(c.short ? { h: c.short } : {}), b: c.blurb, a: areas.findIndex((a) => a.id === c.area), ...(c.subject && c.subject !== 'biology' ? { s: c.subject } : {}),
        q: c.aliases,
        r: rungs.map((r) => (r.role === 'core' ? [lessonIdx.get(r.slug), 0, r.adds ?? '', ...(r.anchor ? [r.anchor] : [])] : [lessonIdx.get(r.slug), 1])),
        f: fs,
        x: (c.near ?? []).filter((n) => all[n.id]).map((n) => [only ? n.id : allIds.indexOf(n.id), n.why]),
      };
    });
    return { v: 1, updated: graph.updated, stages: stages.map((s) => [s.key, s.title]), areas: areas.map((a) => [a.id, a.name]), courses: courseRows, lessons: lessonRows, films: filmRows, concepts: out };
  }

  /**
   * The small index (/graph.json): enough to search every idea by name or everyday phrase and to
   * know which file holds the rest.
   *   covered, live   how many live lessons have a record so far, of how many (the graph fills in over time)
   *   stages          [key, title]
   *   areas           [id, name, number of concepts]; the area's ladders are in /graph/<id>.json
   *   concepts        { id, n name, h short display name (absent when the name is short), a area index, l levels, b blurb, q aliases, f number of films }
   *                   `l` is a bit mask of the levels that have a core lesson (bit 0 = stages[0])
   *   lessons         { slug: [concept indexes] } for the ideas each lesson TEACHES (core rungs only), main idea first
   */
  function clientIndex() {
    const ids = Object.keys(all);
    const at = new Map(ids.map((id, i) => [id, i]));
    const byLesson = {};
    const rows = ids.map((id) => {
      const c = all[id];
      let mask = 0;
      for (const r of c.rungs) {
        const l = lessons.get(r.lesson);
        if (!l || r.role !== 'core') continue;
        mask |= 1 << l.rank;
        (byLesson[l.slug] ??= []).push(at.get(id));
      }
      return { id, n: c.name, ...(c.short ? { h: c.short } : {}), a: areas.findIndex((a) => a.id === c.area), l: mask, b: c.blurb, q: c.aliases, f: filmsFor(id).length };
    });
    return {
      v: 1, updated: graph.updated,
      covered: Object.keys(records).filter((s) => lessons.has(s)).length, live: lessons.size,
      files: { area: '/graph/{area}.json', all: '/graph/all.json' },
      stages: stages.map((s) => [s.key, s.title]),
      areas: areas.map((a) => [a.id, a.name, rows.filter((r) => areas[r.a]?.id === a.id).length]),
      concepts: rows,
      lessons: Object.fromEntries(Object.keys(byLesson).sort().map((s) => { const order = records[s]?.concepts ?? []; return [s, [...byLesson[s]].sort((x, y) => order.indexOf(ids[x]) - order.indexOf(ids[y]))]; })),
    };
  }

  return { graph, areas, areaName, stageTitle, concepts, concept, conceptsOf, ladder, usedBy, ladderByLevel, span, hops, filmsFor, searchIndex, clientGraph, clientIndex };
}

/** Undo clientGraph(): the readable form of /graph.json, for a script that fetched it. */
export function expandClientGraph(g) {
  const lessons = g.lessons.map(([slug, title, ci]) => ({ slug, title, course: g.courses[ci][0], courseTitle: g.courses[ci][1], stage: g.stages[g.courses[ci][2]]?.[0] ?? null, rank: g.courses[ci][2] }));
  const films = g.films.map(([key, title, li, seconds, id]) => ({ key, title, lesson: lessons[li].slug, seconds, href: id ? `/watch/${lessons[li].slug}/${id}/` : `/watch/${lessons[li].slug}/` }));
  return g.concepts.map((c) => ({
    id: c.id, name: c.n, ...(c.h ? { short: c.h } : {}), blurb: c.b, area: g.areas[c.a]?.[0] ?? null, subject: c.s ?? 'biology', aliases: c.q,
    rungs: c.r.map(([li, role, adds, anchor]) => ({ ...lessons[li], role: role ? 'uses' : 'core', ...(adds ? { adds } : {}), ...(anchor ? { anchor } : {}) })),
    films: c.f.map((i) => films[i]),
    near: c.x.map(([t, why]) => ({ id: typeof t === 'number' ? g.concepts[t].id : t, why })),
  }));
}
