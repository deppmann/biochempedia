/* Match plain words to the ideas the site teaches: the one matcher behind the student's
   "What are you trying to understand?" box (/start/), the teacher's syllabus matcher
   (/teach/match/) and any other box that wants the same answer (the homepage's teachers' door
   can call matchSyllabus()).

   Pure JavaScript, no Astro, no Node, no network: the browser and scripts/test-syllabus.mjs run
   this same file. It reads three small static files the site already ships or builds:
     /graph.json           every idea's name, one-line description and everyday phrases
     /ideas/lessons.json   lesson titles, levels and unit names
     /start/lessons.json   per lesson: minutes, and the phrases a student might type
   Nothing a person types or pastes is sent anywhere. No model is asked anything.

   How a match is decided (the short version; the long one is in the functions below):
   1. The text is folded (case, accents, spelling), small words dropped, words cut to a root.
   2. Every idea has TERMS: its name and the parts of its name, its everyday phrases, a few
      textbook names (syllabus-synonyms.mjs), and the titles and search phrases of the lessons
      that teach it.
   3. A term fits when the text and the term explain EACH OTHER: the share of the text's words
      found in the term, times the share of the term's words found in the text, each word weighted
      by how rare it is. "Properties of water" does not fit "Land and Water Ecosystems": one
      shared common word explains neither side.
   4. A whole term found inside a longer line ("Ch. 7 Membranes: diffusion, osmosis") also fits.
   5. Above SURE the idea is an answer. Between MAYBE and SURE it is "might fit" and is never
      shown as an answer. Below that there is no match, and the page says so.

   A wrong match costs more trust than a missing one, so the thresholds lean toward silence. */
import { fold } from './topic-graph-core.mjs';
import { SYNONYMS } from './syllabus-synonyms.mjs';

export const SURE = 0.74;
export const MAYBE = 0.5;
const LEAD_RARE = 0.76;

// ------------------------------------------------------------------ words

const STOP = new Set(('a an the of in on to do does did is are was were and or how why what when where which who whom whose my your you i we it its '
  + 'for with from at by be been being get gets can could would should will that this these those into about so me us our their they them there as if '
  + 'not no some any thing things really actually exactly mean means happen happens work works working make makes made vs versus than then '
  + 'have has had come comes go goes making use uses used need needs let lets tell explain understand know learn want trying try like just also very much many '
  + 'between through during after before under over up down out off again still even each every all both other another such per via am im s t dont doesnt').split(' '));

/** A word's plural-free form: cells → cell, viruses → virus, bodies → body. */
export function stem(w) {
  if (w.length <= 3) return w;
  if (w.endsWith('ies') && w.length > 4) return `${w.slice(0, -3)}y`;
  if (w.endsWith('sses')) return w.slice(0, -2);
  if (/(us|ch|sh|x|z)es$/.test(w)) return w.slice(0, -2);
  if (w.endsWith('s') && !/(ss|us|is)$/.test(w)) return w.slice(0, -1);
  return w;
}

const SUFFIXES = ['ization', 'ational', 'ation', 'ition', 'ular', 'tion', 'sion', 'ment', 'ness', 'ance', 'ence', 'ity', 'ous', 'ive', 'ing', 'ary', 'ion', 'ism',
  'al', 'ic', 'ed', 'er', 'ar', 'um', 'us', 'on', 'e', 'y', 'a'];
/* Roots that the suffix rule would get wrong, or that two spellings of one word should share. */
const ROOTS = {
  mitochondria: 'mitochondri', mitochondrion: 'mitochondri', mitochondrial: 'mitochondri', bacteria: 'bacteri', bacterium: 'bacteri', bacterial: 'bacteri',
  nuclei: 'nucleus', nucleus: 'nucleus', nuclear: 'nucleus', nucleic: 'nucleic', nucleotide: 'nucleotid', fungi: 'fung', fungus: 'fung', fungal: 'fung',
  virus: 'vir', viral: 'vir', gene: 'gene', genetic: 'genetic', genetics: 'genetic', genome: 'genom', genomic: 'genom', genomics: 'genom',
  evolve: 'evolu', evolved: 'evolu', evolving: 'evolu', evolution: 'evolu', evolutionary: 'evolu', inherit: 'inherit', inherited: 'inherit', heredity: 'inherit', hereditary: 'inherit',
  organ: 'organ', organism: 'organism', organic: 'organic', organelle: 'organell', organization: 'organiz', organize: 'organiz', organized: 'organiz',
  muscle: 'muscl', muscular: 'muscl', nerve: 'nerv', nervous: 'nerv', neural: 'neur', neuron: 'neuron', neuronal: 'neuron', neurone: 'neuron',
  autumn: 'fall', fall: 'fall', tire: 'tire', tired: 'tire', tiring: 'tire', tires: 'tire',
  breathe: 'breath', breathing: 'breath', breath: 'breath', respire: 'respir', respiration: 'respir', respiratory: 'respir',
  die: 'death', dies: 'death', dying: 'death', dead: 'death', death: 'death', sight: 'vision', vision: 'vision', visual: 'vision',
  hear: 'hear', hearing: 'hear', smell: 'smell', taste: 'taste', eat: 'eat', eating: 'eat', food: 'food', grow: 'grow', growth: 'grow', growing: 'grow',
  cell: 'cell', cellular: 'cell', plant: 'plant', animal: 'animal', protein: 'protein', species: 'species', analysis: 'analys', synapse: 'synap', synaptic: 'synap',
  mitosis: 'mitos', mitotic: 'mitos', meiosis: 'meios', meiotic: 'meios', photosynthesis: 'photosynthes', photosynthetic: 'photosynthes', photosynthesize: 'photosynthes',
  immune: 'immun', immunity: 'immun', immunology: 'immun', vaccine: 'vaccin', vaccination: 'vaccin', vaccinate: 'vaccin',
  mendel: 'mendel', mendelian: 'mendel', darwin: 'darwin', darwinian: 'darwin', enzyme: 'enzym', enzymatic: 'enzym', hormone: 'hormon', hormonal: 'hormon',
  ecology: 'ecolog', ecological: 'ecolog', ecosystem: 'ecosystem', color: 'color', colors: 'color', leaf: 'leaf', leaves: 'leaf', teeth: 'tooth', feet: 'foot',
  diffusion: 'diffus', diffuse: 'diffus', osmosis: 'osmos', osmotic: 'osmos', digest: 'digest', digestion: 'digest', digestive: 'digest',
  reproduce: 'reproduc', reproduction: 'reproduc', reproductive: 'reproduc', mutate: 'mutat', mutation: 'mutat', mutant: 'mutat',
  flower: 'flower', flowers: 'flower', flow: 'flow', number: 'number', water: 'water', center: 'center', paper: 'paper', layer: 'layer', finger: 'finger', cancer: 'cancer', ether: 'ether',
  neurodegenerative: 'neurodegener', neurodegeneration: 'neurodegener', vesicle: 'vesic', vesicular: 'vesic', vesicles: 'vesic',
  transcription: 'transcript', translation: 'translat', replication: 'replicat', replicate: 'replicat',
};
/** A word's root, so "immune" meets "immunity" and "vaccines" meets "vaccination". Rough on purpose. */
export function rootOf(word) {
  if (ROOTS[word]) return ROOTS[word];
  const w = stem(word);
  if (ROOTS[w]) return ROOTS[w];
  if (w.length <= 4 || /\d/.test(w)) return w;
  for (const s of SUFFIXES) if (w.endsWith(s) && w.length - s.length >= 4) return w.slice(0, -s.length);
  return w;
}

/* Words a syllabus or a question leans on that say little about WHICH idea: they count for less. */
const GENERIC = new Set(('introduction intro overview basic review part continued cont structure function system process type kind role example '
  + 'concept principle topic study biology biological science scientific life living human body organism theory model level important general '
  + 'different major common simple form effect cause control regulation mechanism pathway analysis method technique approach application physiology anatomy chemistry mechanics disease disorder').split(' ').map((w) => rootOf(w)));

/** True when two words differ by one slip: a wrong, missing, extra or swapped letter. */
export function oneSlip(a, b) {
  if (a === b) return true;
  const la = a.length, lb = b.length;
  if (Math.abs(la - lb) > 1) return false;
  let i = 0;
  while (i < la && i < lb && a[i] === b[i]) i++;
  if (la === lb) {
    if (a.slice(i + 1) === b.slice(i + 1)) return true;
    return a[i] === b[i + 1] && a[i + 1] === b[i] && a.slice(i + 2) === b.slice(i + 2);
  }
  return la > lb ? a.slice(i + 1) === b.slice(i) : a.slice(i) === b.slice(i + 1);
}
/** Two slips in a long word: compare the halves. */
function twoSlips(a, b) {
  if (a.length < 9 || b.length < 9 || a[0] !== b[0] || Math.abs(a.length - b.length) > 2) return false;
  const h = Math.floor(a.length / 2);
  for (const k of [h - 1, h, h + 1]) {
    if (k < 1 || k > b.length - 1) continue;
    if (oneSlip(a.slice(0, h), b.slice(0, k)) && oneSlip(a.slice(h), b.slice(k))) return true;
  }
  return false;
}

/** The words of a text that carry meaning: [{ w: as folded, s: stem, r: root }]. */
export function tokens(text) {
  const out = [];
  for (const w of fold(text).split(' ')) {
    if (!w || STOP.has(w)) continue;
    const s = stem(w);
    if (STOP.has(s)) continue;
    out.push({ w, s, r: rootOf(w) });
  }
  return out;
}

/** How well a typed word fits an indexed one: 1 the same word, 0.9 the same root, 0.78 a slip, 0.62 two slips in a long word. */
function wordFit(q, t) {
  if (q.s === t.s) return 1;
  if (q.r === t.r) return 0.9;
  if (q.w.length >= 5 && t.w.length >= 5 && q.w[0] === t.w[0] && (oneSlip(q.s, t.s) || oneSlip(q.w, t.w))) return 0.78;
  if (twoSlips(q.w, t.w)) return 0.62;
  return 0;
}

// ------------------------------------------------------------------ the index

/**
 * @typedef {{ i: number, id: string, name: string, label: string, blurb: string, area: number, mask: number, lessons: { slug: string, title: string, rank: number, unit: string }[] }} Idea
 * @typedef {{ toks: { w: string, s: string, r: string }[], idea: number, kind: 'name' | 'phrase' | 'textbook' | 'lesson' | 'asked', weight: number, text: string, slug?: string, whole: boolean }} Term
 */

const KIND_WEIGHT = { name: 1, textbook: 0.97, phrase: 0.96, part: 0.92, lesson: 0.9, asked: 0.8, half: 0.77 };
/* For a syllabus a loose reading is not good enough: a lesson's search phrase or half a name may suggest, never decide. */
const STRICT_WEIGHT = { ...KIND_WEIGHT, asked: 0.7, half: 0.72 };

/** The parts of a name: "Cell division (mitosis)" → whole ["Cell division (mitosis)", "Cell division"], part ["mitosis"].
 *  A bracket that lists examples ("(cadherins and integrins)") and the halves of an "and" name are `half`: hints, not names. */
function nameParts(name) {
  const whole = new Set([name]), part = new Set(), half = new Set();
  const bare = name.replace(/\s*\([^)]*\)/g, '').trim();
  if (bare) whole.add(bare);
  for (const m of name.matchAll(/\(([^)]*)\)/g)) {
    const items = m[1].split(/,| and | or /).map((x) => x.trim()).filter((x) => x.length > 1);
    if (items.length === 1) part.add(items[0]); else for (const x of items) half.add(x);
  }
  const cut = bare.split(/:\s+|, the /).map((x) => x.trim()).filter((x) => x.length > 2);
  if (cut.length > 1) for (const x of cut) part.add(x);
  for (const p of [bare, ...cut]) { const hs = p.split(/ and |, /); if (hs.length > 1) for (const h of hs) if (h.trim().length > 2) half.add(h.trim()); }
  for (const x of whole) { part.delete(x); half.delete(x); }
  for (const x of part) half.delete(x);
  // "Digestion and absorption": the first half of a two-part name usually names the idea by itself.
  const two = bare.split(' and ');
  const lead = two.length === 2 && !bare.includes(',') && !bare.includes(':') ? two[0].replace(/^the /i, '').trim() : '';
  return { whole: [...whole], part: [...part], half: [...half], lead };
}

/**
 * Join the site's files into one matcher.
 * @param {any} g /graph.json
 * @param {{ lessons: [slug: string, title: string, rank: number, sol: string[], unit: string][] }} lessonFile /ideas/lessons.json
 * @param {{ lessons: Record<string, [whole: number, skim: number, phrases: string[]]> } | null} [extra] /start/lessons.json
 */
export function buildMatcher(g, lessonFile, extra = null) {
  const rows = new Map((lessonFile?.lessons ?? []).map(([slug, title, rank, sol, unit]) => [slug, { slug, title, rank, unit: unit ?? '', sol: sol ?? [] }]));
  /** @type {Idea[]} */
  const ideas = g.concepts.map((c, i) => ({ i, id: c.id, name: c.n, label: c.h ?? c.n, blurb: c.b, area: c.a, mask: c.l, films: c.f, lessons: [] }));
  const byId = new Map(ideas.map((it) => [it.id, it]));
  /** @type {Term[]} */
  const terms = [];
  const add = (idea, kind, text, slug, whole = true) => {
    const toks = tokens(text);
    if (!toks.length || toks.length > 12) return;
    // "What do plants need?" is not the word "plants": a phrase the small words reduce to one word is left out.
    if (toks.length === 1 && kind !== 'textbook' && fold(text).split(' ').length >= 3) return;
    terms.push({ toks, idea, kind, text, whole, ...(slug ? { slug } : {}) });
  };
  const leads = [];
  g.concepts.forEach((c, i) => {
    const parts = nameParts(c.n);
    for (const p of parts.whole) add(i, 'name', p);
    for (const p of parts.part) add(i, 'part', p);
    for (const p of parts.half) add(i, 'half', p);
    if (parts.lead) leads.push([i, parts.lead]);
    if (c.h && c.h !== c.n) add(i, 'part', c.h);
    add(i, 'part', c.id.replace(/-/g, ' '));
    for (const a of c.q) add(i, 'phrase', a);
    for (const s of SYNONYMS[c.id] ?? []) add(i, 'textbook', s);
  });
  // A lesson's title and search phrases speak for the ideas it teaches: the main idea first.
  for (const [slug, list] of Object.entries(g.lessons ?? {})) {
    const l = rows.get(slug);
    if (!l) continue;
    list.forEach((ci, k) => { if (ideas[ci]) ideas[ci].lessons.push({ ...l, main: k === 0 }); });
    const main = list[0];
    if (main === undefined || !ideas[main]) continue;
    { const tp = nameParts(l.title); for (const p of [...tp.whole, ...tp.part]) add(main, 'lesson', p, slug); }
    for (const p of extra?.lessons?.[slug]?.[2] ?? []) add(main, 'asked', p, slug);
  }
  for (const it of ideas) it.lessons.sort((a, b) => a.rank - b.rank);

  // How rare a root is, over the names and phrases (one count per idea).
  const seen = new Map();
  terms.forEach((t) => { for (const k of t.toks) { if (!seen.has(k.r)) seen.set(k.r, new Set()); seen.get(k.r).add(t.idea); } });
  const N = ideas.length;
  const idf = new Map([...seen].map(([r, set]) => [r, Math.log(1 + N / set.size)]));
  const maxIdf = Math.log(1 + N);
  // Rarity is squeezed into 0.4 to 1, so a common word ("plant") still counts: a phrase that shares only
  // the rare word of a two-word question does not explain the question.
  const weightOf = (tok) => (0.4 + 0.6 * (idf.get(tok.r) ?? maxIdf) / maxIdf) * (GENERIC.has(tok.r) ? 0.3 : 1);
  // root → terms, and every indexed token once, for words typed with a slip.
  const byRoot = new Map();
  terms.forEach((t, ti) => { for (const k of new Set(t.toks.map((x) => x.r))) { if (!byRoot.has(k)) byRoot.set(k, []); byRoot.get(k).push(ti); } });
  const vocab = new Map();
  for (const t of terms) for (const k of t.toks) if (!vocab.has(k.s)) vocab.set(k.s, k);
  for (const t of terms) t.sum = t.toks.reduce((n, k) => n + weightOf(k), 0);
  // A leading half counts as a name when it is a rare word or a phrase ("homeostasis", "blood flow"), not a common one ("genes").
  for (const [i, text] of leads) {
    const tk = tokens(text);
    if (!tk.length || /^(how|why|what|switching|forward|grades)\b/i.test(text) || (tk.length === 1 && weightOf(tk[0]) < LEAD_RARE)) continue;
    const t = { toks: tk, idea: i, kind: 'part', text, whole: true };
    t.sum = tk.reduce((n, k) => n + weightOf(k), 0);
    terms.push(t);
    for (const k of new Set(tk.map((x) => x.r))) { if (!byRoot.has(k)) byRoot.set(k, []); byRoot.get(k).push(terms.length - 1); }
  }
  // Every word of an idea's own names, for "this piece is already inside that idea".
  const own = ideas.map(() => new Set());
  for (const t of terms) if (t.kind === 'name' || t.kind === 'part' || t.kind === 'textbook') for (const k of t.toks) own[t.idea].add(k.r);
  return { ideas, byId, terms, byRoot, vocab: [...vocab.values()], weightOf, own, single: new Set(terms.filter((t) => t.toks.length === 1 && (t.kind === 'name' || t.kind === 'part' || t.kind === 'textbook')).map((t) => t.toks[0].r)), maxIdf: 1, coreOf: g.lessons ?? {}, minutes: extra?.lessons ?? {}, areas: g.areas, stages: g.stages };
}

// ------------------------------------------------------------------ matching one piece of text

/**
 * Rank ideas for one short piece of text: a question, or one topic from a syllabus.
 * @returns {{ id: string, name: string, score: number, sure: boolean, why: { kind: string, text: string, slug?: string }, lesson?: string }[]}
 */
export function matchText(m, text, limit = 5, strict = false) {
  const W = strict ? STRICT_WEIGHT : KIND_WEIGHT;
  const q = tokens(text);
  if (!q.length) return [];
  // Which indexed roots each typed word could be: itself, or a near spelling.
  const fits = q.map((qt) => {
    const out = new Map();
    if (m.byRoot.has(qt.r)) out.set(qt.r, 1);
    // A near spelling is tried when the word is unknown, or known only from a stray phrase or two.
    if ((m.byRoot.get(qt.r)?.length ?? 0) < 3 && qt.w.length >= 5) {
      for (const v of m.vocab) { const f = wordFit(qt, v); if (f >= 0.6 && f > (out.get(v.r) ?? 0)) out.set(v.r, f); }
    }
    return out;
  });
  const cand = new Set();
  fits.forEach((f) => { for (const r of f.keys()) for (const ti of m.byRoot.get(r) ?? []) cand.add(ti); });
  const qSum = q.reduce((n, k) => n + m.weightOf(k), 0);
  const qSpecific = q.some((k) => !GENERIC.has(k.r));
  if (!qSpecific) return [];
  const best = new Map();

  for (const ti of cand) {
    const t = m.terms[ti];
    // The share of the text the term explains, and of the term the text explains.
    let qHit = 0, exactAll = true;
    for (const qt of q) { let b = 0; for (const tt of t.toks) { const f = wordFit(qt, tt); if (f > b) b = f; } qHit += b * m.weightOf(qt); if (b < 0.9) exactAll = false; }
    let tHit = 0, tAll = true;
    for (const tt of t.toks) { let b = 0; for (const qt of q) { const f = wordFit(qt, tt); if (f > b) b = f; } tHit += (b >= 0.6 ? 1 : 0) * m.weightOf(tt); if (b < 0.9) tAll = false; }
    const qCov = qHit / qSum, tCov = tHit / (t.sum || 1);
    let fit = qCov * tCov;
    // A question may carry a few extra words the phrase lacks ("…in the fall"): soften the term side a little.
    if (!strict) fit = Math.max(fit, qCov * (0.4 + 0.6 * tCov) * 0.97);
    // The whole term sits inside a longer line, in order: "Ch 7 membranes: diffusion and osmosis".
    if (tAll && !exactAll && (t.kind === 'name' || t.kind === 'textbook' || ((t.kind === 'lesson' || t.kind === 'phrase' || t.kind === 'part') && t.toks.length >= 2)) && inOrder(q, t.toks)) {
      const specific = t.toks.some((k) => !GENERIC.has(k.r) && m.weightOf(k) >= 0.7);
      const inside = (t.toks.length >= 2 ? 0.95 : specific ? 0.9 : 0.55) * (0.55 + 0.45 * Math.min(1, qCov * 2.2));
      if (inside > fit) fit = inside;
    }
    const score = fit * W[t.kind];
    if (score < 0.3) continue;
    const own = t.slug ? 0 : score;
    const prev = best.get(t.idea);
    if (!prev) best.set(t.idea, { score, term: t, cover: qCov, lesson: t.slug, lessonScore: t.slug ? score : 0, own });
    else {
      if (t.slug && score > prev.lessonScore) { prev.lesson = t.slug; prev.lessonScore = score; }
      if (own > prev.own) prev.own = own;
      if (score > prev.score) { prev.score = score; prev.term = t; prev.cover = qCov; }
    }
  }
  // A lesson's title or search phrase was filed under the lesson's main idea. If another idea the
  // same lesson teaches matches the words by its own name, the phrase was about that one.
  for (const [i, b] of best) {
    if (!b.term.slug || b.own >= b.score - 0.05) continue;
    const mates = (m.coreOf[b.term.slug] ?? []).filter((j) => j !== i && best.has(j) && best.get(j).own >= MAYBE && best.get(j).own > b.own + 0.1);
    if (!mates.length) continue;
    const to = mates.sort((x, y) => best.get(y).own - best.get(x).own)[0];
    const tb = best.get(to);
    if (b.score > tb.score) { tb.score = b.score; tb.lesson = b.term.slug; tb.lessonScore = b.score; }
    b.score = Math.max(b.own, MAYBE);
  }
  const out = [...best].map(([i, b]) => {
    const it = m.ideas[i];
    return {
      id: it.id, name: it.name, score: Math.min(1, b.score), sure: b.score >= SURE, cover: b.cover, words: b.term.toks.map((k) => k.r),
      why: { kind: b.term.kind, text: b.term.text, ...(b.term.slug ? { slug: b.term.slug } : {}) },
      ...(b.lesson && b.lessonScore >= b.score * 0.92 ? { lesson: b.lesson } : {}),
    };
  }).filter((r) => r.score >= MAYBE && m.byId.get(r.id).lessons.length);
  out.sort((a, b) => b.score - a.score || best.get(m.byId.get(b.id).i).own - best.get(m.byId.get(a.id).i).own || bits(m.byId.get(b.id).mask) - bits(m.byId.get(a.id).mask) || a.name.localeCompare(b.name));
  return out.slice(0, limit);
}
const bits = (x) => { let n = 0; for (let v = x; v; v >>= 1) n += v & 1; return n; };

/** True when the term's words appear in the text next to each other and in order. */
function inOrder(q, toks) {
  outer: for (let i = 0; i + toks.length <= q.length; i++) {
    for (let k = 0; k < toks.length; k++) if (wordFit(q[i + k], toks[k]) < 0.9) continue outer;
    return true;
  }
  return false;
}

// ------------------------------------------------------------------ a student's question

/**
 * What a learner typed, to an answer the page can stand behind.
 *   kind 'match'    `ideas[0]` is the answer; the rest are other readings worth offering
 *   kind 'closest'  nothing matched well: `ideas` are "might fit", never shown as the answer
 *   kind 'none'     nothing close; offer search and the list of ideas
 */
export function matchQuestion(m, text) {
  const cleaned = String(text ?? '').replace(/\b(for (kids|children|beginners|dummies)|in (simple|plain) (words|terms|english)|eli5|please|simply|quick(ly)?)\b/gi, ' ');
  let found = matchText(m, cleaned, 6);
  // "photosynthesis and respiration": two ideas asked for at once.
  const parts = splitTopics(cleaned);
  if (parts.length > 1 && !(found[0]?.score >= 0.93 && found[0].cover >= 0.8)) {
    const each = parts.map((forms) => forms.map((f) => matchText(m, f, 2)[0]).find((r) => r?.sure)).filter(Boolean);
    if (each.length > 1 || (each.length === 1 && !found[0]?.sure)) {
      const ids = new Set(each.map((r) => r.id));
      found = [...each, ...found.filter((r) => !ids.has(r.id))];
      return { kind: 'match', ideas: dedupe(found).slice(0, 6), together: each.length > 1 ? each.length : 1 };
    }
  }
  if (!found.length) return { kind: 'none', ideas: [], together: 0 };
  if (!found[0].sure) return { kind: 'closest', ideas: found.slice(0, 3), together: 0 };
  return { kind: 'match', ideas: found, together: 1 };
}
const dedupe = (list) => { const s = new Set(); return list.filter((r) => (s.has(r.id) ? false : (s.add(r.id), true))); };

// ------------------------------------------------------------------ a syllabus

/* Lines that are a course's housekeeping, not its science. */
const ADMIN = /\b(exam|midterm|mid term|final|quiz|quizzes|test day|unit test|chapter test|unit \d+ (test|exam|quiz)|test|review( day| session| for)?|holiday|no class|no school|no lab|no lecture|break|thanksgiving|labor day|memorial day|mlk|martin luther king|columbus day|indigenous peoples|veterans day|presidents day|juneteenth|easter|recess|teacher work ?day|early release|snow day|conference|registration|add ?\/ ?drop|withdraw|reading day|study day|commencement|syllabus|course (overview|introduction|intro|policies|expectations|logistics)|welcome|orientation|icebreaker|lab safety|safety (contract|rules|training|quiz)|office hours|make ?up|catch ?up|flex day|buffer|tbd|tba|to be (announced|determined)|presentations?|poster session|project (due|work|day|proposal)|paper due|report due|homework|problem set|worksheet|assignment|due\b|sol (review|test)|ap exam|state test|benchmark|field trip|guest (lecture|speaker)|pre ?test|post ?test|study guide|check ?in|wrap ?up|course evaluations?)\b/i;
/* Lines from the top of a syllabus: who, where, how it is graded. */
const POLICY = /@|https?:|www\.|\b(instructor|professor|teacher:|email|e-mail|phone|room\b|office|textbook|required (text|materials)|isbn|edition|grading|grade scale|grades?:|points|percent|%|attendance|late work|academic (integrity|honesty)|honor code|plagiarism|accommodation|disabilit|prerequisite|credits?\b|credit hours|learning (outcomes|objectives)|course description|tardy|cell ?phones?|supplies|materials needed|canvas|blackboard|google classroom|schoology|meeting time|class meets|section \d|semester|fall 20|spring 20|policy|policies)\b/i;

const MONTH = '(jan(uary)?|feb(ruary)?|mar(ch)?|apr(il)?|may|june?|july?|aug(ust)?|sept?(ember)?|oct(ober)?|nov(ember)?|dec(ember)?)';
const DAY = '(mon(day)?|tues?(day)?|wed(nesday)?|thu(rs)?(day)?|fri(day)?|sat(urday)?|sun(day)?|m|t|w|th|r|f|mw|mwf|tr|tth)';
/* What a schedule line starts with before its topic: "Week 3:", "9/14", "Mon Sep 14 -", "Ch. 5", "12.", "Unit 2 Day 4". */
const LEAD = new RegExp('^\\s*(?:[-*•·▪◦>|]+\\s*)?(?:'
  + '(?:week|wk|day|unit|module|lecture|lec|class|session|lesson|meeting|topic|part|quarter|q|block|period)\\s*#?\\s*\\d+[a-z]?(?:\\s*(?:-|–|to|&|and|\\/)\\s*\\d+)?'
  + `|(?:${DAY}\\.?,?\\s+)?${MONTH}\\.?\\s+\\d{1,2}(?:st|nd|rd|th)?(?:\\s*(?:-|–|to)\\s*(?:${MONTH}\\.?\\s+)?\\d{1,2}(?:st|nd|rd|th)?)?(?:,?\\s*20\\d\\d)?`
  + `|(?:${DAY}\\.?,?\\s+)?\\d{1,2}\\/\\d{1,2}(?:\\/\\d{2,4})?(?:\\s*(?:-|–|to)\\s*\\d{1,2}\\/\\d{1,2}(?:\\/\\d{2,4})?)?`
  + `|${DAY}\\.?(?=\\s*[:\\-–|\\t])`
  + '|\\(?\\d{1,3}[.)](?!\\d)'
  + '|[ivx]{1,5}[.)]'
  + '|[a-h][.)]'
  + ')\\s*(?:[:.\\-–—|,\\t]+\\s*)?', 'i');
/* Chapter and page references anywhere in a line. */
const REFS = /\(?\b(?:ch(?:apter|ap|s)?\.?|sec(?:tion)?\.?|pp?\.?|pages?|readings?:?|read:?|campbell|text(?:book)?:?|openstax|sol)\s*:?\s*\d+(?:\.\d+)*[a-z]?(?:\s*(?:-|–|,|&|and|to)\s*\d+(?:\.\d+)*[a-z]?)*\)?:?/gi;
const STANDARD = /\(?\b(?:BIO|LS|PS|ES|HS-LS|MS-LS)[.\- ]?\d+(?:[.\-]?[a-z0-9]+)*\)?:?/gi;
const TAIL = /\s*[-–—:|]\s*(?:lab|lecture|discussion|activity|notes|video|worksheet|part\s*[ivx\d]+|cont(?:inued|['’]d|\.)?|day\s*\d+|\d+\s*(?:days?|weeks?|periods?|blocks?))\s*$/i;

/** One syllabus line down to the words that name its topic. */
export function cleanTopic(line) {
  let s = String(line).replace(/ /g, ' ');
  for (let k = 0; k < 4; k++) { const n = s.replace(LEAD, '').replace(/^\s*\([^)]*\d[^)]*\)\s*[:.\-–]?\s*/, ''); if (n === s) break; s = n; }
  s = s.replace(REFS, ' ').replace(STANDARD, ' ');
  s = s.replace(/\((?:cont(?:inued|['’]d|\.)?|part\s*[ivx\d]+|\d+\s*(?:days?|weeks?|periods?|blocks?))\)/gi, ' ');
  for (let k = 0; k < 2; k++) s = s.replace(TAIL, '');
  s = s.replace(/^\s*(?:lab|lecture|discussion|activity|topic|unit|module|reading|video|intro(?:duction)? to|introduction:|overview of)\s*[:\-–]?\s+/i, '');
  return s.replace(/\s+/g, ' ').replace(/^[\s:;,.\-–—|]+|[\s:;,\-–—|]+$/g, '').trim();
}

/** "Mitosis and meiosis; cancer" → the topics in it. Keeps a phrase whole when splitting leaves a bare generic word. */
export function splitTopics(text) {
  const s = String(text).replace(/\s+/g, ' ').trim();
  const rough = s.split(/\s*(?:[;,/|•()]|\s[-–—]\s|:\s|\band\b|&|\bvs\.?\b|\bversus\b|\bplus\b|\+)\s*/i).map((p) => p.trim()).filter(Boolean);
  if (rough.length <= 1) return rough.map((p) => [p]);
  const out = [];
  for (let i = 0; i < rough.length; i++) {
    const p = rough[i];
    const n = tokens(p).length;
    if (!n) continue;
    // Each piece is tried in a fuller form first: "DNA replication and repair" also asks for
    // "DNA repair", "fatty acid and cholesterol synthesis" for "fatty acid synthesis".
    const forms = [];
    const next = rough[i + 1], prev = rough[i - 1];
    if (n <= 2 && next) { const nt = fold(next).split(' '); if (nt.length >= 2) forms.push(`${p} ${nt[nt.length - 1]}`); }
    if (n === 1 && prev) { const pt = fold(prev).split(' '); if (pt.length >= 2) forms.push(`${pt.slice(0, -1).join(' ')} ${p}`); }
    if (n >= 2) forms.unshift(p); else forms.push(p);
    out.push(forms);
  }
  return out;
}

/**
 * Read a pasted syllabus into rows, in its own order.
 * @returns {{ rows: { n: number, raw: string, topic: string, kind: 'topic' | 'admin' }[], skipped: string[] }}
 *   `skipped` are lines that read as policies, contact details or prose, in order.
 */
export function parseSyllabus(text) {
  const lines = String(text ?? '').replace(/\r\n?/g, '\n').split('\n').map((l) => l.replace(/\t+/g, ' | ').replace(/\s+/g, ' ').trim());
  const marked = lines.filter((l) => l && LEAD.test(l) && l.replace(LEAD, '').trim().length > 2).length;
  // With a real schedule in the text, only its lines (and short lines under them) are topics.
  const strict = marked >= 4;
  const rows = [], skipped = [];
  let inSchedule = false, n = 0;
  for (const line of lines) {
    if (!line) { continue; }
    if (/^(week|date|day|unit|topic|lecture)s?\s*\|\s*(topic|date|reading|chapter|subject|content)/i.test(line) || /^[-=_|\s]{4,}$/.test(line)) continue;
    const hasLead = LEAD.test(line) && line.replace(LEAD, '').trim().length > 2;
    const words = line.split(' ').length;
    const prose = words >= 14 && /[a-z]{3}\. [A-Z]|[a-z]{3}\.$/.test(line);
    if (/^(course )?(schedule|calendar|outline|topics|sequence|pacing|scope and sequence|tentative schedule)\b.{0,40}$/i.test(line)) { inSchedule = true; continue; }
    if (!hasLead && (POLICY.test(line) || prose || line.length > 170)) { skipped.push(line); if (!strict) inSchedule = false; continue; }
    if (strict && !hasLead && !inSchedule && !rows.length) { skipped.push(line); continue; }
    if (hasLead) inSchedule = true;
    // A table row may hold several cells: the topic is the cell with the most to say.
    let body = line;
    if (line.includes(' | ')) {
      const cells = line.split(' | ').map((c) => c.trim()).filter(Boolean);
      const scored = cells.map((c) => ({ c, t: cleanTopic(c) })).filter((x) => x.t && !/^\d+$/.test(x.t));
      const pick = scored.find((x) => !ADMIN.test(x.c) && tokens(x.t).length) ?? scored[0];
      if (!pick) continue;
      if (cells.some((c) => ADMIN.test(c)) && !scored.some((x) => !ADMIN.test(x.c) && tokens(x.t).length >= 1 && !/^(ch|chapter|pp|read)/i.test(x.c))) body = cells.find((c) => ADMIN.test(c)) ?? pick.c;
      else body = pick.c;
    }
    const topic = cleanTopic(body);
    if (!topic || topic.length < 3 || /^\d[\d\s.,/-]*$/.test(topic)) { if (line.length > 3) skipped.push(line); continue; }
    if (!hasLead && strict && words > 12) { skipped.push(line); continue; }
    // "Exam I; bacterial genetics" and "Organelles (cell project due Fri)": drop the housekeeping, keep the science.
    let kind = 'topic', said = topic;
    if (ADMIN.test(topic)) {
      const keep = topic.split(/\s*(?:;|\(|\)|\*{2,}|\s[-–—]\s|\s\+\s|,)\s*/).filter((p) => p && !ADMIN.test(p) && tokens(p).some((k) => !GENERIC.has(k.r)));
      if (keep.length) said = keep.join('; '); else kind = 'admin';
    }
    rows.push({ n: n++, raw: line, topic: said, kind });
  }
  return { rows, skipped };
}

/**
 * The ideas one syllabus topic names. Only sure matches come back as `ideas`; `maybe` holds
 * what might fit, for a row the page shows unticked and labelled.
 */
export function matchTopic(m, topic) {
  const whole = matchText(m, topic, 4, true);
  const sure = [];
  const maybe = [];
  const take = (r, from) => { if (!sure.some((x) => x.id === r.id)) sure.push({ ...r, from }); };
  // The whole line is one idea's name, near enough: stop there.
  const settled = whole[0]?.sure && whole[0].score >= 0.9 && whole[0].cover >= 0.8;
  if (settled) {
    take(whole[0], topic);
    if (whole[1]?.sure && whole[1].score >= whole[0].score - 0.02 && whole[1].cover >= 0.8) take(whole[1], topic);
  } else {
    for (const forms of splitTopics(topic)) {
      let got = null, near = null;
      for (const f of forms) {
        // A bare common word left over from a split ("plant" from "plant and animal cells") is not a topic.
        if (forms.length > 1) { const tk = tokens(f); if (tk.length === 1 && m.weightOf(tk[0]) < 0.75 && !m.single.has(tk[0].r)) continue; }
        const r = matchText(m, f, 2, true);
        if (r[0]?.sure) { got = { r: r[0], f }; break; }
        if (r[0] && !near) near = { r: r[0], f };
      }
      if (got) take(got.r, got.f);
      else if (near) maybe.push({ ...near.r, from: near.f });
    }
    // A name that runs across the pieces ("Cells, tissues, organs and organ systems").
    if (whole[0]?.sure && whole[0].score >= 0.9) take(whole[0], topic);
    else if (!sure.length && whole[0]?.sure) take(whole[0], topic);
  }
  if (!sure.length && whole[0] && !whole[0].sure) maybe.unshift({ ...whole[0], from: topic });
  // "Regulation of gene expression" is not also "gene expression": a match whose words all sit
  // inside a longer match is dropped.
  const lead = whole[0]?.sure && whole[0].score >= 0.9 ? m.own[m.byId.get(whole[0].id).i] : null;
  const kept = sure.filter((a) => !sure.some((b) => b !== a && b.words.length > a.words.length && a.words.every((w) => b.words.includes(w)))
    && !(lead && a.id !== whole[0].id && a.words.every((w) => lead.has(w))));
  const ids = new Set(kept.map((r) => r.id));
  return { ideas: kept.slice(0, 3), maybe: dedupe(maybe.filter((r) => !ids.has(r.id))).slice(0, kept.length ? 0 : 2) };
}

// ------------------------------------------------------------------ lessons at a level

/**
 * For one idea and one level: the lessons at that level, the nearest simpler ones and the
 * nearest deeper ones. `rungs` are the idea's core lessons with a rank each (any order).
 */
export function pickRungs(rungs, level, prefer) {
  const at = rungs.filter((r) => r.rank === level);
  const lower = rungs.filter((r) => r.rank < level), higher = rungs.filter((r) => r.rank > level);
  const downRank = lower.length ? Math.max(...lower.map((r) => r.rank)) : -1;
  const upRank = higher.length ? Math.min(...higher.map((r) => r.rank)) : -1;
  const first = (list) => (prefer ? [...list].sort((a, b) => Number(b.slug === prefer) - Number(a.slug === prefer)) : list);
  return { at: first(at), down: first(lower.filter((r) => r.rank === downRank)), up: first(higher.filter((r) => r.rank === upRank)) };
}

/** The level to start on when the reader has not said: the simplest lesson that is not an activity for young children. */
export function defaultLevel(rungs) {
  const ranks = [...new Set(rungs.map((r) => r.rank))].sort((a, b) => a - b);
  return ranks.find((r) => r >= 1) ?? ranks[0] ?? -1;
}

/**
 * Match a whole syllabus. The one call a page needs.
 * @param {ReturnType<typeof buildMatcher>} m
 * @param {string} text the pasted syllabus
 * @param {number} level the class's level, 0 (ages 5 to 10) to 6 (graduate)
 * @returns {{ rows: { n: number, raw: string, topic: string, kind: 'topic' | 'admin',
 *   ideas: { id: string, name: string, score: number, why: any, at: any[], down: any[], up: any[] }[],
 *   maybe: { id: string, name: string, at: any[], down: any[], up: any[] }[] }[], skipped: string[], matched: number, topics: number }}
 */
export function matchSyllabus(m, text, level) {
  const { rows, skipped } = parseSyllabus(text);
  const first = rows.map((row) => (row.kind === 'admin' ? { ideas: [], maybe: [] } : matchTopic(m, row.topic)));
  // What the course is about, from its clearest matches. A loose match from an area the rest of
  // the syllabus never touches ("pressure flow" as phloem, in a physiology course) is a guess.
  const areaCount = new Map();
  let strong = 0;
  for (const r of first) for (const x of r.ideas) if (x.score >= 0.93) { const a = m.byId.get(x.id).area; areaCount.set(a, (areaCount.get(a) ?? 0) + 1); strong++; }
  const stray = (x) => strong >= 8 && x.why.kind !== 'name' && x.why.kind !== 'textbook' && x.score < 0.985 && (areaCount.get(m.byId.get(x.id).area) ?? 0) / strong < 0.05;
  const join = (x) => ({ ...x, ...pickRungs(m.byId.get(x.id).lessons, level, x.lesson) });
  const out = rows.map((row, i) => {
    const r = first[i];
    const ideas = r.ideas.filter((x) => !stray(x));
    const maybe = ideas.length ? [] : [...r.ideas.filter(stray), ...r.maybe].slice(0, 2);
    return { ...row, ideas: ideas.map(join), maybe: maybe.map(join) };
  });
  // What a row shows: its lessons once each, however many of its ideas they teach. `missing` are
  // the ideas with no lesson at the class's level (said plainly, never hidden by another idea's lesson).
  for (const row of out) {
    const group = (key, skip) => {
      const list = [];
      for (const it of row.ideas) for (const l of it[key]) {
        if (skip.has(l.slug)) continue;
        const have = list.find((x) => x.slug === l.slug);
        if (have) have.ideas.push(it.id); else list.push({ slug: l.slug, title: l.title, rank: l.rank, ideas: [it.id] });
      }
      return list;
    };
    const at = group('at', new Set());
    const atSlugs = new Set(at.map((l) => l.slug));
    const down = group('down', atSlugs).sort((a, b) => b.rank - a.rank).slice(0, 3);
    const up = group('up', new Set([...atSlugs, ...down.map((l) => l.slug)])).sort((a, b) => a.rank - b.rank).slice(0, 3);
    row.lessons = { at: at.slice(0, 5), down, up, missing: row.ideas.filter((it) => !it.at.length).map((it) => it.id) };
  }
  const topics = out.filter((r) => r.kind === 'topic');
  return { rows: out, skipped, topics: topics.length, matched: topics.filter((r) => r.ideas.length).length };
}
