/* Find an idea: the search behind /ideas/, with no Astro and no Node, so the browser and
   scripts/test-hop.mjs run the same code.

   It reads two small static files: /graph.json (every idea's name, one-line description, everyday
   phrases and levels, and which ideas each lesson teaches) and /ideas/lessons.json (lesson titles,
   levels, Virginia standards codes and unit names). Nothing is sent anywhere; a query never
   leaves the page.

   What it tolerates: capitals, accents, British or American spelling (the graph's own fold()),
   plurals, a missing or swapped letter in a longer word, and level words tacked on ("osmosis grade 7").
   What it refuses to do: pass off a loose match as an answer. A result reached only through a stray
   word is marked `closest`, and the page says there is nothing on the query itself yet. */
import { fold } from './topic-graph-core.mjs';

const STOP = new Set(['a', 'an', 'the', 'of', 'in', 'on', 'to', 'do', 'does', 'did', 'is', 'are', 'was', 'and', 'or', 'how', 'why', 'what', 'when', 'where', 'which', 'who', 'my', 'your', 'you', 'i', 'we', 'it', 'its', 'for', 'with', 'from', 'at', 'by', 'be', 'get', 'can', 'that', 'this', 'into', 'about', 'make', 'makes', 'work', 'works', 'have', 'has', 'so', 'me', 'us', 'our', 'their', 'they', 'there', 'as', 'if', 'not', 'no', 'some', 'thing', 'things']);
/* Level words a person adds to a query; they choose a level, not an idea. */
const LEVEL_WORDS = /\b(for (kids|children|beginners|dummies)|grade (7|seven)|7th grade|middle school|high school|college|university|graduate|grad school|mcat|simple|simply|explained|explain|eli5|basics|lesson|lessons|film|films|video|videos)\b/g;

/** One word to a form that plurals share: cells → cell, viruses → virus, bodies → body. */
export function stem(w) {
  if (w.length <= 3) return w;
  if (w.endsWith('ies') && w.length > 4) return `${w.slice(0, -3)}y`;
  if (w.endsWith('sses')) return w.slice(0, -2);
  if (/(us|ch|sh|x|z)es$/.test(w)) return w.slice(0, -2);
  if (w.endsWith('s') && !/(ss|us|is)$/.test(w)) return w.slice(0, -1);
  return w;
}
const words = (folded) => folded.split(' ').filter((w) => w && !STOP.has(w)).map(stem);

/** True when two words differ by one slip: a wrong, missing, extra or swapped letter. */
export function oneSlip(a, b) {
  if (a === b) return true;
  const la = a.length, lb = b.length;
  if (Math.abs(la - lb) > 1) return false;
  let i = 0;
  while (i < la && i < lb && a[i] === b[i]) i++;
  if (la === lb) {
    if (a.slice(i + 1) === b.slice(i + 1)) return true;                                   // one wrong letter
    return a[i] === b[i + 1] && a[i + 1] === b[i] && a.slice(i + 2) === b.slice(i + 2);   // two swapped
  }
  return la > lb ? a.slice(i + 1) === b.slice(i) : a.slice(i) === b.slice(i + 1);         // one missing or extra
}
/** How well a typed word matches an indexed one: 1 exact, 0.9 a prefix either way, 0.7 a slip, 0 no. */
function wordMatch(q, t) {
  if (q === t) return 1;
  if (q.length >= 4 && t.startsWith(q)) return 0.9;
  if (t.length >= 4 && q.startsWith(t) && q.length - t.length <= 3) return 0.9;
  if (q.length >= 5 && t.length >= 5 && q[0] === t[0] && oneSlip(q, t)) return 0.7;
  if (q.length >= 9 && t.length >= 9 && q.slice(0, 3) === t.slice(0, 3) && Math.abs(q.length - t.length) <= 2) {
    // A long word may carry two slips; check by removing one slip at a time is costly, so compare halves.
    const h = Math.floor(q.length / 2);
    if (oneSlip(q.slice(0, h), t.slice(0, h)) && (oneSlip(q.slice(h), t.slice(h)) || oneSlip(q.slice(h), t.slice(h + t.length - q.length)))) return 0.6;
  }
  return 0;
}

/** A Virginia standards code as typed ("BIO.3d", "ls 2 e", "LS.2") to one form: "bio3d". '' when it is not one. */
export function solCode(s) {
  const m = /^\s*(bio|ls|k|[1-4])\s*\.?\s*(\d{1,2})\s*([a-z])?\s*$/i.exec(String(s));
  if (!m) return '';
  if (!/^(bio|ls)$/i.test(m[1]) && !/\./.test(s)) return '';     // "3 5" is not a code; "3.5 b" is
  return `${m[1]}${m[2]}${m[3] ?? ''}`.toLowerCase();
}

/**
 * Join the two files into one index.
 * @param {any} g /graph.json
 * @param {{ lessons: [slug: string, title: string, rank: number, sol: string[], unit: string][] } | null} extra /ideas/lessons.json
 */
export function buildIndex(g, extra) {
  const lessons = new Map((extra?.lessons ?? []).map(([slug, title, rank, sol, unit]) => [slug, { slug, title, rank, sol, unit }]));
  const ideas = g.concepts.map((c, i) => ({
    i, id: c.id, name: c.n, blurb: c.b, area: c.a, mask: c.l, films: c.f, aliases: c.q,
    fName: fold(c.n), wName: words(fold(c.n)),
    fAliases: c.q.map(fold),
    wBlurb: words(fold(c.b)),
    lessons: [],
  }));
  for (const [slug, list] of Object.entries(g.lessons ?? {})) {
    const l = lessons.get(slug);
    if (!l) continue;
    const entry = { ...l, fTitle: fold(l.title), wTitle: words(fold(l.title)), fUnit: fold(l.unit), codes: l.sol.map((c) => solCode(c)).filter(Boolean) };
    for (const ci of list) ideas[ci]?.lessons.push(entry);
  }
  for (const it of ideas) it.lessons.sort((a, b) => a.rank - b.rank);
  return { ideas, areas: g.areas, hasLessons: lessons.size > 0 };
}

const coverage = (qw, tw) => {
  if (!qw.length || !tw.length) return 0;
  let sum = 0;
  for (const q of qw) { let best = 0; for (const t of tw) { const m = wordMatch(q, t); if (m > best) best = m; } sum += best; }
  return sum / qw.length;
};

/**
 * Rank ideas for a typed query.
 * @returns {{ q: string, code: string, results: { id: string, name: string, score: number,
 *   why: { kind: 'name' | 'phrase' | 'lesson' | 'unit' | 'code' | 'about', text: string, slug?: string },
 *   exact: boolean, closest: boolean }[] }}
 */
export function search(index, query, limit = 8) {
  const raw = fold(query);
  const code = solCode(query);
  if (!raw) return { q: '', code: '', results: [] };
  // "osmosis grade 7" asks for osmosis; keep the level words only if nothing else is left.
  const stripped = raw.replace(LEVEL_WORDS, ' ').replace(/\s+/g, ' ').trim();
  const q = stripped || raw;
  const qw = words(q);
  const out = [];
  for (const it of index.ideas) {
    let score = 0, why = null;
    const take = (s, w) => { if (s > score) { score = s; why = w; } };

    if (code) {
      for (const l of it.lessons) {
        const hit = l.codes.find((c) => c === code || (c.startsWith(code) && /^[a-z]$/.test(c.slice(code.length))));
        if (hit) take(92, { kind: 'code', text: l.title, slug: l.slug, code: l.sol[l.codes.indexOf(hit)] });
      }
      if (score) out.push({ id: it.id, name: it.name, score: score + it.i * -0.0001, why, exact: false, closest: false });
      continue;
    }

    // The idea's own name.
    if (it.fName === q || it.wName.join(' ') === qw.join(' ')) take(100, { kind: 'name', text: it.name });
    else if (q.length >= 3 && (it.fName.startsWith(`${q} `) || it.fName.includes(` ${q} `) || it.fName.endsWith(` ${q}`))) take(82, { kind: 'name', text: it.name });
    else if (it.fName.length >= 4 && ` ${q} `.includes(` ${it.fName} `)) take(80, { kind: 'name', text: it.name });
    else if (q.length >= 3 && !q.includes(' ') && it.fName.split(' ').some((w) => w.startsWith(q))) take(64, { kind: 'name', text: it.name });
    else { const c = coverage(qw, it.wName); if (c >= 0.5) take(c >= 0.99 ? 78 : 30 + c * 30, { kind: 'name', text: it.name }); }

    // An everyday phrase someone might type.
    it.fAliases.forEach((a, k) => {
      const w = { kind: 'phrase', text: it.aliases[k] };
      if (a === q) take(96, w);
      else if (q.length >= 4 && ` ${a} `.includes(` ${q} `)) take(qw.length > 1 ? 74 : 58, w);
      else if (a.length >= 6 && ` ${q} `.includes(` ${a} `)) take(72, w);
      else { const c = coverage(qw, words(a)); if (c >= 0.6) take(c >= 0.99 ? (qw.length > 1 ? 70 : 52) : 22 + c * 30, w); }
    });

    // A lesson on its ladder, or the unit that lesson is in.
    for (const l of it.lessons) {
      const w = { kind: 'lesson', text: l.title, slug: l.slug };
      if (l.fTitle === q) take(88, w);
      else if (q.length >= 4 && ` ${l.fTitle} `.includes(` ${q} `)) take(66, w);
      else { const c = coverage(qw, l.wTitle); if (c >= 0.75) take(c >= 0.99 ? 62 : 20 + c * 30, w); }
      if (l.fUnit && (l.fUnit === q || (q.length >= 5 && ` ${l.fUnit} `.includes(` ${q} `)))) take(l.fUnit === q ? 56 : 46, { kind: 'unit', text: l.unit, slug: l.slug });
    }

    // Its one-line description: the weakest evidence.
    const cb = coverage(qw, it.wBlurb);
    if (cb >= 0.99 && qw.length) take(qw.length > 1 ? 44 : 34, { kind: 'about', text: it.blurb });

    if (score > 0) out.push({ id: it.id, name: it.name, score: score + Math.min(bits(it.mask), 5) * 0.1, why, exact: score >= 95, closest: false });
  }
  out.sort((a, b) => b.score - a.score || a.name.localeCompare(b.name));
  // Honest about a loose match: if nothing matched by name, exact phrase or lesson title, the best
  // row is "closest so far", not an answer.
  if (out.length && !code && out[0].score < 60) out.forEach((r) => { r.closest = true; });
  return { q, code, results: out.slice(0, limit) };
}
const bits = (m) => { let n = 0; for (let x = m; x; x >>= 1) n += x & 1; return n; };
