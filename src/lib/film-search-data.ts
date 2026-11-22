/* What a film can be found by besides its card (2026-11-22), for /films/search.json. Built from data
   that already exists; nobody tags films by hand.

   - Field: each course names its field(s) in COURSE_FIELDS below (one line per course, not per film),
     and the topic graph (src/data/topic-graph.json) adds the areas of the ideas a lesson teaches
     ("Nerves and the brain" counts toward neuroscience). A method film has no course: its fields are
     the average over the lessons that cite the method (src/data/methods.ts `lessons`), plus a little
     from the method's own category. So "neuroscience methods" finds the methods neuroscience lessons
     use, strongest first.
   - Ideas: the names and aliases of the topic-graph concepts the lesson teaches.
   - Phrases: the questions people ask about the lesson (src/data/lesson-links.json `search`).
   - Method: the method's name, other names and the terms lessons use for it.
   - Take-homes and the one-line description.
   - Transcript: up to TRANSCRIPT_MAX of the film's rarer caption words (in at most RARE_DF films),
     so a word said in a film finds it without shipping every transcript.
   Words already in a film's title or lesson title are left out of the other fields to keep it small. */
import { filmCatalog, filmKey, type CatalogFilm } from './film-catalog';
import { METHODS, type MethodCategory } from '../data/methods';
import { transcriptFor } from './film-transcript';
import graph from '../data/topic-graph.json';
import links from '../data/lesson-links.json';

/** Field key -> the words it is found by. */
export const FIELDS: Record<string, string> = {
  neuroscience: 'neuroscience neurobiology neuro',
  'cell-biology': 'cell biology',
  biochemistry: 'biochemistry',
  genetics: 'genetics genomics',
  'ecology-evolution': 'ecology evolution',
  physiology: 'physiology',
  development: 'developmental biology development',
  signaling: 'cell signaling signalling',
  immunology: 'immunology immune microbiology',
  plants: 'plant biology botany',
  biology: 'biology life science',
};
const COURSE_FIELDS: Record<string, string[]> = {
  'biology-together': ['biology'],
  'life-science': ['biology'],
  'high-school-biology': ['biology'],
  'organismal-biology': ['biology'],
  'cell-biology': ['cell-biology'],
  genetics: ['genetics'],
  'ecology-evolution': ['ecology-evolution'],
  biochemistry: ['biochemistry'],
  neuroscience: ['neuroscience'],
  physiology: ['physiology'],
  signaling: ['signaling', 'cell-biology'],
  'developmental-neuroscience': ['neuroscience', 'development'],
  'sensory-systems': ['neuroscience'],
};
const AREA_FIELDS: Record<string, string[]> = {
  cells: ['cell-biology'], molecules: ['biochemistry'], energy: ['biochemistry'], genes: ['genetics'],
  evolution: ['ecology-evolution'], diversity: ['ecology-evolution'], ecosystems: ['ecology-evolution'],
  plants: ['plants'], body: ['physiology'], 'microbes-immunity': ['immunology'], 'nervous-system': ['neuroscience'],
  senses: ['neuroscience'], signaling: ['signaling'], development: ['development'],
};
const CATEGORY_FIELDS: Record<MethodCategory, string[]> = {
  molecules: ['biochemistry'], genes: ['genetics'], 'cells-imaging': ['cell-biology'],
  physiology: ['neuroscience', 'physiology'], 'organisms-fields': ['ecology-evolution'], data: [],
};
/** A field below this weight is not kept. */
const FIELD_MIN = 0.35;
export const TRANSCRIPT_MAX = 20;
/** At most this many take-home words a film. */
const TAKE_MAX = 25;
const RARE_DF = 25;

const fold = (s: string) => s.normalize('NFD').replace(/[̀-ͯ]/g, '').toLowerCase();
const words = (s: string) => fold(s).split(/[^a-z0-9]+/).filter((w) => w.length > 2);
const STOP = new Set(('about above after again against also because been before being below between both cannot could does doing down during each even every from further have having here into itself just more most much must never only other over same should some such than that their them then there these they this those through under until very were what when where which while whose with would your yours'
  + ' make makes made take takes took gets give gives given here like look looks back know need needs right next first second still keeps keep comes come goes going thing things something nothing means mean whole part parts'
  + ' answer question pause think predict watch film picture shows show showing used uses using once ones another enough really little').split(' '));

type Fd = Map<string, number>;
/* Weights are not capped at 1 here: a method that neuroscience lessons cite and whose category is
   "Neurons and physiology" ranks above one they only cite. film-search.mjs scales them (FIELD_TOP). */
const fdString = (m: Fd) => [...m].filter(([, v]) => v >= FIELD_MIN).sort((a, b) => b[1] - a[1]).map(([k, v]) => `${k}:${Math.round(v * 100) / 100}`).join(' ');

export interface FilmSearchData {
  v: 1;
  fields: Record<string, string>;
  /** Per lesson: ideas (i), phrases (w), fields (fd). */
  lessons: { i?: string; w?: string; fd?: string }[];
  /** Per film key: its lesson (L, an index into lessons), method words (m), own fields (fd, method
   *  films), take-home words (x), transcript words (tr). */
  films: Record<string, { L?: number; m?: string; fd?: string; x?: string; tr?: string }>;
}

export async function filmSearchData(): Promise<FilmSearchData> {
  const films = await filmCatalog();
  const concepts = graph.concepts as Record<string, { name: string; short?: string; aliases?: string[]; area: string }>;
  const glessons = graph.lessons as Record<string, { concepts: string[] }>;
  const phrases = links.lessons as Record<string, { search?: string[] }>;

  /* Each lesson's fields: its course's, then the areas of its ideas (by share, up to 0.7). */
  const lessonCourse = new Map<string, string>();
  for (const f of films) if (f.lesson && f.course) lessonCourse.set(f.lesson, f.course);
  const lessonFields = (slug: string, course?: string): Fd => {
    const m: Fd = new Map();
    for (const k of COURSE_FIELDS[course ?? lessonCourse.get(slug) ?? ''] ?? []) m.set(k, 1);
    const cs = glessons[slug]?.concepts ?? [];
    for (const c of cs) {
      for (const k of AREA_FIELDS[concepts[c]?.area ?? ''] ?? []) m.set(k, (m.get(k) ?? 0) + 0.5 / cs.length);
    }
    return m;
  };

  const lessons: FilmSearchData['lessons'] = [];
  const lessonIndex = new Map<string, number>();
  const out: FilmSearchData['films'] = {};
  const own = (f: CatalogFilm) => new Set(words(`${f.title} ${f.lessonTitle ?? ''}`));
  const keepNew = (text: string, have: Set<string>, max = Infinity, min = 3) => {
    const seen = new Set<string>();
    for (const w of words(text)) if (w.length >= min && !have.has(w) && !STOP.has(w)) seen.add(w);
    return [...seen].slice(0, max).join(' ');
  };

  for (const f of films) {
    if (!f.lesson || lessonIndex.has(f.lesson)) continue;
    const have = new Set(words(f.lessonTitle ?? ''));
    const cs = glessons[f.lesson]?.concepts ?? [];
    const ideas = cs.flatMap((c) => [concepts[c]?.name ?? '', concepts[c]?.short ?? '', ...(concepts[c]?.aliases ?? [])]).join(' ');
    const rec: FilmSearchData['lessons'][number] = {};
    const i = keepNew(ideas, have);
    if (i) rec.i = i;
    const w = keepNew((phrases[f.lesson]?.search ?? []).join(' '), new Set([...have, ...words(ideas)]));
    if (w) rec.w = w;
    const fd = fdString(lessonFields(f.lesson, f.course ?? undefined));
    if (fd) rec.fd = fd;
    lessonIndex.set(f.lesson, lessons.length);
    lessons.push(rec);
  }

  /* Transcript words: count in how many films each word is said, keep a film's rarest. */
  const said = new Map<string, string[]>();
  const df = new Map<string, number>();
  for (const f of films) {
    const paras = transcriptFor(f.captions);
    if (!paras) continue;
    const ws = [...new Set(words(paras.join(' ')).filter((w) => w.length > 3 && !STOP.has(w) && !/^\d+$/.test(w)))];
    said.set(f.src, ws);
    for (const w of ws) df.set(w, (df.get(w) ?? 0) + 1);
  }

  const methodBySlug = new Map(METHODS.map((m) => [m.slug, m]));
  for (const f of films) {
    const rec: FilmSearchData['films'][string] = {};
    if (f.lesson) rec.L = lessonIndex.get(f.lesson);
    const have = own(f);
    const m = f.method ? methodBySlug.get(f.method.slug) : undefined;
    if (m) {
      rec.m = [...new Set(words([m.name, ...(m.aka ?? []), ...(m.terms ?? [])].join(' ')))].join(' ');
      for (const w of words(rec.m)) have.add(w);
      if (!f.course) {
        // A method film's fields: the lessons that cite it, averaged, plus its category at half weight.
        const sum: Fd = new Map();
        const cited = m.lessons.filter((s) => lessonCourse.has(s));
        // Each citing lesson counts once per field (its course or its ideas, at most 1): a share of the lessons.
        for (const s of cited) for (const [k, v] of lessonFields(s)) sum.set(k, (sum.get(k) ?? 0) + Math.min(1, v) / cited.length);
        for (const k of CATEGORY_FIELDS[m.category]) sum.set(k, (sum.get(k) ?? 0) + 0.5);
        const fd = fdString(sum);
        if (fd) rec.fd = fd;
      }
    }
    const x = keepNew([f.description, ...(f.takeaways ?? [])].join(' '), have, TAKE_MAX, 4);
    if (x) rec.x = x;
    const ws = said.get(f.src);
    if (ws) {
      const rare = ws.filter((w) => !have.has(w) && (df.get(w) ?? 0) <= RARE_DF)
        .sort((a, b) => (df.get(a)! - df.get(b)!) || (a < b ? -1 : 1))
        .slice(0, TRANSCRIPT_MAX);
      if (rare.length) rec.tr = rare.join(' ');
    }
    out[filmKey(f.src)] = rec;
  }
  return { v: 1, fields: FIELDS, lessons, films: out };
}
