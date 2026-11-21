/* Film timelines (2026-11-20): what the theater on /watch/ needs to follow a film as it plays.

   Everything here is worked out from files already in the repository, by rule, with no model:
     explainers/<lesson>/[<film-id>/]script.json   the film's scenes, in order (no times)
     public/explainers/<lesson>/<name>.vtt         the published captions (one cue per sentence, timed)
     src/content/lessons/<lesson>/lesson.mdx       the lesson: its headings, where each film sits, its figures
     src/data/film-maps/<lesson>/<name>.json       optional, written and checked by hand: the film cut into
                                                   named parts, and which lesson figure belongs to which part

   Three steps:
     1. sceneTimes(): each spoken scene's start is the start of the caption cue that opens with the scene's
        first words. A silent scene (title card, thinking pause, end card) starts where the scene before it
        stops speaking. A scene whose words cannot be found joins the scene before it.
     2. lessonOutline() and filmRegion(): the part of the lesson a film goes with is the stretch from the
        heading the film is placed under to the heading of the lesson's next film.
     3. applyMap(): a hand-checked map names the parts and places figures. Without a map no figure is ever
        tied to a moment of the film: which figure fits which second, and whether it gives away an answer the
        film is about to ask for, is a judgement this code does not make.

   Used by src/lib/film-theater.ts (at build time), scripts/film-timelines/report.mjs,
   scripts/check-film-timelines.mjs and scripts/test-film-timelines.mjs. Plain Node, no dependencies beyond
   github-slugger (the same slugger Astro uses for heading ids). */
import { existsSync, readFileSync, readdirSync } from 'node:fs';
import { join } from 'node:path';
import GithubSlugger from 'github-slugger';

/* ------------------------------------------------------------------ captions */

const clock = (s) => {
  const p = s.trim().split(':').map(Number);
  return p.length === 3 ? p[0] * 3600 + p[1] * 60 + p[2] : p[0] * 60 + p[1];
};
const ENTITIES = { '&amp;': '&', '&lt;': '<', '&gt;': '>', '&quot;': '"', '&#39;': "'", '&nbsp;': ' ', '&lrm;': '', '&rlm;': '' };

/** WebVTT text to cues: [{ start, end, text }], in file order. Notes, styles and tags are dropped. */
export function parseVtt(vtt) {
  const cues = [];
  for (const block of String(vtt).replace(/\r/g, '').split(/\n{2,}/)) {
    const lines = block.split('\n').map((l) => l.trim()).filter(Boolean);
    if (!lines.length || /^(WEBVTT|NOTE|STYLE|REGION)\b/.test(lines[0])) continue;
    const ti = lines.findIndex((l) => l.includes('-->'));
    if (ti === -1) continue;
    const [a, b] = lines[ti].split('-->');
    const text = lines.slice(ti + 1).join(' ')
      .replace(/<[^>]+>/g, '')
      .replace(/&(?:amp|lt|gt|quot|#39|nbsp|lrm|rlm);/g, (m) => ENTITIES[m] ?? m)
      .replace(/\s+/g, ' ').trim();
    const start = clock(a);
    const end = clock(b.trim().split(/\s+/)[0]);
    if (text && Number.isFinite(start) && Number.isFinite(end)) cues.push({ start, end, text });
  }
  return cues;
}

/**
 * Cues joined into sentences, for the transcript that follows the film: a caption file breaks a long
 * sentence over two cues ("... from crowded to less" / "crowded. This time, ..."), and a line that
 * starts mid-sentence is a poor thing to tap. A new line starts at each cue that follows the end of
 * a sentence. Each line keeps the start of its first cue.
 */
export function transcriptLines(cues) {
  const out = [];
  let cur = null;
  for (const c of cues) {
    if (cur && !/[.?!…]["”’')\]]*$/.test(cur.text)) { cur.text += ` ${c.text}`; cur.end = c.end; continue; }
    cur = { start: c.start, end: c.end, text: c.text };
    out.push(cur);
  }
  return out;
}

/* ------------------------------------------------------------------ scene times */

/** A word reduced to what survives the trip from script to caption: lower case, letters and digits only. */
const NUMBER_WORDS = { zero: '0', one: '1', two: '2', three: '3', four: '4', five: '5', six: '6', seven: '7', eight: '8', nine: '9', ten: '10', eleven: '11', twelve: '12', twenty: '20', thirty: '30', forty: '40', fifty: '50', sixty: '60', seventy: '70', eighty: '80', ninety: '90' };
export const norm = (w) => {
  const x = w.normalize('NFKD').toLowerCase().replace(/[^a-z0-9]/g, '');
  // The voice text spells small numbers out ("six to ten"); the caption may print them ("6 to 10").
  return Object.hasOwn(NUMBER_WORDS, x) ? NUMBER_WORDS[x] : x;
};
const words = (text) => String(text ?? '').split(/\s+/).map(norm).filter(Boolean);

/* A thinking pause: a silent scene named as a pause and at least three seconds long. A shorter hold
   (a beat after an answer) is not one. */
const isPause = (s) => /pause/i.test(s.id ?? '') && !(typeof s.silent === 'number' && s.silent < 3);
const sceneTexts = (s) => [s.caption, s.narration, s.tts].filter((t) => typeof t === 'string' && t.trim());
const isSpoken = (s) => sceneTexts(s).length > 0;

/**
 * Start and end of every scene.
 *
 * `script` is a parsed script.json, `cues` come from parseVtt, `duration` is the film's length in seconds.
 * Returns { scenes: [{ id, start, end, kind, matched, text }], spoken, matched, questions: [{ scene, pause,
 * reveal, start, sceneStart, revealStart, text }] } where kind is 'title' | 'spoken' | 'question' | 'pause' | 'end' | 'silent'.
 *
 * Matching. The caption file is written from the same script, so a scene's opening words are the opening
 * words of one cue. Three things make that inexact, and each is handled:
 *   - a scene has up to three texts (the on-screen caption, the narration, the text sent to the voice with
 *     numbers spelled out); any of them may be what the cue carries, so each is tried;
 *   - a cue can open with a spoken number the script writes as a figure ("about minus −65 mV"); if the
 *     first words fail, the second to fifth words are tried and the start is the start of that cue;
 *   - a long sentence is split over two cues, so a scene can begin part-way through a cue; then its start
 *     is that cue's start plus the share of the cue already spoken.
 * Scenes are matched in order and never backwards, so a phrase repeated later in the film cannot pull a
 * scene out of place.
 */
export function sceneTimes(script, cues, duration) {
  const stream = []; // every caption word with the cue it sits in and its place in that cue
  cues.forEach((c, ci) => {
    const ws = words(c.text);
    ws.forEach((w, k) => stream.push({ w, ci, k, n: ws.length }));
  });
  const timeAt = (j) => {
    const x = stream[j];
    const c = cues[x.ci];
    return x.k === 0 ? c.start : c.start + ((c.end - c.start) * x.k) / x.n;
  };
  const find = (key, from, to) => {
    if (!key.length) return -1;
    for (let j = from; j <= Math.min(to, stream.length - key.length); j++) {
      let ok = true;
      for (let q = 0; q < key.length; q++) if (stream[j + q].w !== key[q]) { ok = false; break; }
      if (ok) return j;
    }
    return -1;
  };

  const list = (script.scenes ?? []).filter((s) => s && typeof s.id === 'string');
  const out = list.map((s) => ({ id: s.id, start: null, end: null, kind: 'silent', matched: false, text: '' }));
  let p = 0; // first caption word not yet claimed by a scene
  let owed = 0; // words spoken by the scenes since the last one found
  let prevTails = []; // the previous spoken scene's texts, as normalised words
  let spoken = 0;
  let matched = 0;
  list.forEach((s, i) => {
    if (!isSpoken(s)) return;
    spoken++;
    out[i].kind = 'spoken';
    out[i].text = String(s.caption ?? s.narration ?? s.tts).replace(/\s+/g, ' ').trim();
    let best = -1;
    // Look only as far ahead as the scenes since the last match could have spoken, with room to spare,
    // so an opening that fails here cannot be "found" in a later scene that happens to share its words.
    const far = p + Math.ceil(owed * 1.6) + 30;
    for (const text of sceneTexts(s)) {
      const ws = words(text);
      // The opening four words, then three; then the same starting one to four words in.
      for (const skip of [0, 1, 2, 3, 4]) {
        let hit = -1;
        for (const len of [4, 3]) {
          const key = ws.slice(skip, skip + len);
          if (key.length < len) continue;
          const j = find(key, p, far);
          if (j === -1) continue;
          // Where in its cue the match sits. A scene can truly begin part-way through a cue, when one
          // sentence was split over two cues: then the cue's opening words are the last words of the
          // scene before. Otherwise the cue opens with something the script writes differently (a
          // number said aloud), and the scene starts with the cue.
          const k = stream[j].k;
          let at = j;
          if (k > 0 && k <= skip + 2) {
            const lead = stream.slice(j - k, j).map((x) => x.w).join(' ');
            if (!prevTails.some((t) => t.endsWith(lead))) at = j - k;
          }
          // Four words that match beat three: three alone can sit inside the scene before
          // (a question that names the thing the answer opens with).
          // and three words are trusted only where a cue begins.
          if (at >= p && (len === 4 || stream[at].k === 0)) { hit = at; break; }
        }
        if (hit !== -1) { if (best === -1 || hit < best) best = hit; break; }
      }
    }
    owed += Math.max(...sceneTexts(s).map((t) => words(t).length));
    prevTails = sceneTexts(s).map((t) => words(t).join(' '));
    if (best === -1) return;
    out[i].matched = true;
    out[i].start = Math.floor(timeAt(best) * 10 + 1e-6) / 10; // never later than the cue itself
    out[i].j = best;
    matched++;
    owed = Math.max(...sceneTexts(s).map((t) => words(t).length));
    p = best + 1;
  });

  // When the speaking of scene i stops: the end of the cue holding the last caption word before the next
  // matched scene.
  const nextMatched = (i) => { for (let k = i + 1; k < out.length; k++) if (out[k].matched) return out[k]; return null; };
  const speechEnd = (i) => {
    const nx = nextMatched(i);
    const lastWord = nx ? nx.j - 1 : stream.length - 1;
    return lastWord >= 0 ? cues[stream[lastWord].ci].end : 0;
  };
  // Silent scenes: the first starts the film; any other starts when the scene before it stops speaking.
  // A spoken scene that was not found has no start of its own.
  let lastSpoken = -1;
  out.forEach((o, i) => {
    if (o.matched) { lastSpoken = i; return; }
    if (o.kind === 'spoken') return;
    if (lastSpoken === -1) o.start = 0;
    else {
      const prev = out[i - 1];
      // Two silent scenes in a row share the gap; the second has no start of its own.
      // Never later than the next scene found (captions sometimes carry a line spoken over the pause).
      const nx = nextMatched(i);
      o.start = prev.matched ? Math.floor(Math.min(speechEnd(lastSpoken), nx ? nx.start : Infinity) * 10 + 1e-6) / 10 : null;
    }
    o.kind = i === 0 ? 'title' : isPause(list[i]) ? 'pause' : i === out.length - 1 ? 'end' : 'silent';
  });
  // Ends, and a guard: starts must rise. A scene that would start before the one ahead of it loses its start.
  let prevStart = -1;
  for (const o of out) {
    if (o.start === null) continue;
    if (o.start < prevStart) { if (o.matched) matched--; o.start = null; o.matched = false; continue; }
    prevStart = o.start;
  }
  const timed = out.filter((o) => o.start !== null);
  timed.forEach((o, k) => { o.end = k + 1 < timed.length ? timed[k + 1].start : Math.max(duration ?? 0, o.start); });

  // The film's own questions: a spoken scene followed by a thinking pause. The answer starts with the
  // first spoken scene after the pause. A scene that is itself an answer (named reveal or answer) is
  // never a question, whatever follows it.
  // When the scene opens with a lead-in ("Water dots hop at random, both ways. So which way ...?"), the
  // question starts at the caption line that asks (the first with a question mark, or that begins
  // "Predict"), and its text runs from that line on.
  const questions = [];
  out.forEach((o, i) => {
    if (o.kind !== 'pause' || i === 0) return;
    const q = out[i - 1];
    if (q.kind !== 'spoken' || q.start === null || /reveal|answer/i.test(q.id)) return;
    const reveal = out.slice(i + 1).find((x) => x.kind === 'spoken' && x.start !== null);
    if (!reveal) return;
    q.kind = 'question';
    const until = Math.min(o.start ?? reveal.start, reveal.start);
    const mine = cues.filter((c) => c.start >= q.start - 0.05 && c.start < until);
    const k = mine.findIndex((c) => c.text.includes('?') || /^predict\b/i.test(c.text));
    const late = k > 0;
    questions.push({
      scene: q.id, pause: o.id, reveal: reveal.id,
      start: late ? Math.floor(mine[k].start * 10 + 1e-6) / 10 : q.start,
      sceneStart: q.start,
      revealStart: reveal.start,
      text: late ? mine.slice(k).map((c) => c.text).join(' ') : q.text,
    });
  });
  for (const o of out) delete o.j;
  return { scenes: out, spoken, matched, questions };
}

/** How far a film's scenes could be timed: 'timed' (every spoken scene), 'partial' (at least 4 in 5; the
 *  others join the scene before them) or 'untimed'. */
export function timingStatus(t) {
  if (!t || !t.spoken) return 'untimed';
  if (t.matched === t.spoken) return 'timed';
  return t.matched / t.spoken >= 0.8 ? 'partial' : 'untimed';
}

/* ------------------------------------------------------------------ the lesson */

const decode = (s) => s.replace(/&quot;/g, '"').replace(/&#39;|&apos;/g, "'").replace(/&amp;/g, '&').replace(/&lt;/g, '<').replace(/&gt;/g, '>').replace(/&nbsp;/g, ' ');

/** The attributes of a one-line JSX tag: strings as written, {numbers}, {["a","b"]} and {"strings"}. */
export function jsxAttrs(tag) {
  const out = {};
  const re = /([A-Za-z][\w-]*)=(?:"([^"]*)"|\{((?:[^{}]|\{[^{}]*\})*)\})/g;
  let m;
  while ((m = re.exec(tag))) {
    if (m[2] !== undefined) { out[m[1]] = decode(m[2]); continue; }
    const raw = m[3].trim();
    try { out[m[1]] = JSON.parse(raw); } catch {
      const q = /^(['`])([\s\S]*)\1$/.exec(raw);
      out[m[1]] = q ? q[2] : raw;
    }
  }
  return out;
}

/** Heading text as Astro's slugger sees it: inline Markdown and tags removed. */
const headingText = (raw) => raw
  .replace(/\s+#+\s*$/, '')
  .replace(/!\[([^\]]*)\]\([^)]*\)/g, '$1')
  .replace(/\[([^\]]*)\]\([^)]*\)/g, '$1')
  .replace(/<[^>]+>/g, '')
  .replace(/\{[^}]*\}/g, '')
  .replace(/(`+)([^`]*)\1/g, '$2')
  .replace(/(\*\*|__)(.*?)\1/g, '$2')
  .replace(/(^|[^\w*])\*([^*]+)\*/g, '$1$2')
  .replace(/(^|[^\w])_([^_]+)_(?!\w)/g, '$1$2')
  .replace(/\\([\\`*_{}[\]()#+\-.!$])/g, '$1')
  .trim();

/**
 * What the theater needs from a lesson's body: its headings (with the ids the lesson page gives them),
 * where each further film is placed, and its figures. `mdx` is the whole lesson.mdx file.
 */
export function lessonOutline(mdx) {
  const text = String(mdx).replace(/\r/g, '');
  const fm = /^---\n[\s\S]*?\n---\n/.exec(text);
  const body = fm ? text.slice(fm[0].length) : text;
  const slugger = new GithubSlugger();
  const headings = [];
  const films = [];
  const figures = [];
  let fence = null;
  let current = null; // nearest heading above
  body.split('\n').forEach((line, n) => {
    const f = /^\s*(```+|~~~+)/.exec(line);
    if (f) { fence = fence ? (line.trim().startsWith(fence) ? null : fence) : f[1]; return; }
    if (fence) return;
    const h = /^(#{1,6})\s+(.+?)\s*$/.exec(line);
    if (h) {
      const t = headingText(h[2]);
      current = { depth: h[1].length, text: t, id: slugger.slug(t), line: n };
      headings.push(current);
      return;
    }
    const film = /<LessonFilm\s+film=\{frontmatter\.films\[(\d+)\]\}/.exec(line);
    if (film) { films.push({ index: Number(film[1]), heading: current?.id ?? null, line: n }); return; }
    const fig = /<(LessonFigure|ScaffoldFigure)\b[^>]*\/>/.exec(line);
    if (fig) {
      const a = jsxAttrs(fig[0]);
      if (typeof a.src !== 'string') return;
      figures.push({
        src: a.src,
        alt: typeof a.alt === 'string' ? a.alt : '',
        caption: typeof a.caption === 'string' ? a.caption : '',
        width: Number(a.width) || 1200,
        height: Number(a.height) || 800,
        // A scaffold figure asks the student to name its numbered parts, so its key words are an answer
        // the lesson holds back; the theater never prints them.
        scaffold: fig[1] === 'ScaffoldFigure',
        keyItems: fig[1] === 'LessonFigure' && Array.isArray(a.keyItems) ? a.keyItems.map(String) : [],
        heading: current?.id ?? null,
        line: n,
      });
    }
  });
  return { headings, films, figures };
}

/**
 * The part of the lesson a film goes with. `index` is the film's place in the frontmatter's `films`
 * (null for the lesson's opening film, which stands at the top and covers the lesson up to the next film).
 * Returns { section, sections, figures }: the heading the film sits under (null for an opening film
 * that has no heading above the lesson's first one), every h2 from there to the next film, and the
 * figures in that stretch, in lesson order.
 */
export function filmRegion(outline, index) {
  const placed = [...outline.films].sort((a, b) => a.line - b.line);
  const headingLine = (id) => outline.headings.find((h) => h.id === id)?.line ?? 0;
  let from = 0;
  let to = Infinity;
  let section = null;
  if (index === null || index === undefined) {
    if (placed.length) to = Math.min(placed[0].line, headingLine(placed[0].heading) || placed[0].line);
    section = outline.headings.find((h) => h.depth === 2 && h.line < to) ?? null;
  } else {
    const k = placed.findIndex((f) => f.index === index);
    if (k === -1) return { section: null, sections: [], figures: [] };
    const me = placed[k];
    from = me.heading ? headingLine(me.heading) : me.line;
    const nx = placed[k + 1];
    if (nx) to = nx.heading && headingLine(nx.heading) > from ? headingLine(nx.heading) : nx.line;
    section = outline.headings.find((h) => h.id === me.heading) ?? null;
  }
  const inside = (x) => x.line >= from && x.line < to;
  return {
    section: section ? { id: section.id, text: section.text } : null,
    sections: outline.headings.filter((h) => h.depth === 2 && inside(h)).map((h) => ({ id: h.id, text: h.text })),
    figures: outline.figures.filter(inside),
  };
}

/** When the film says `text`: the start of the caption cue in which those words begin, or null. */
export function saidAt(cues, text) {
  const key = words(text);
  if (!key.length) return null;
  const stream = [];
  cues.forEach((c, ci) => { for (const w of words(c.text)) stream.push({ w, ci }); });
  for (let j = 0; j + key.length <= stream.length; j++) {
    let ok = true;
    for (let q = 0; q < key.length; q++) if (stream[j + q].w !== key[q]) { ok = false; break; }
    if (ok) return cues[stream[j].ci].start;
  }
  return null;
}

/* ------------------------------------------------------------------ hand-checked maps */

export const MAPS_DIR = 'src/data/film-maps';

/** Every map on disk: [{ key, file, map }] where key is "<lesson>/<name>". */
export function allMaps(root) {
  const dir = join(root, MAPS_DIR);
  if (!existsSync(dir)) return [];
  const out = [];
  for (const lesson of readdirSync(dir, { withFileTypes: true })) {
    if (!lesson.isDirectory()) continue;
    for (const f of readdirSync(join(dir, lesson.name))) {
      if (!f.endsWith('.json')) continue;
      const file = join(MAPS_DIR, lesson.name, f);
      let map = null;
      let error = null;
      try { map = JSON.parse(readFileSync(join(root, file), 'utf8')); } catch (e) { error = String(e.message ?? e); }
      out.push({ key: `${lesson.name}/${f.replace(/\.json$/, '')}`, file, map, error });
    }
  }
  return out.sort((a, b) => a.key.localeCompare(b.key));
}

/**
 * Check a map against the film and the lesson, and turn it into the parts the theater shows.
 * Returns { parts, problems }. A map with any problem is not used (the film falls back to the plain theater)
 * and scripts/check-film-timelines.mjs fails the build.
 *
 * The rules, each of which exists so that a figure cannot give away an answer:
 *   1. every part starts at a scene that exists and has a start time, and parts are in film order;
 *   2. every question the film asks (a spoken scene followed by a thinking pause) is a part of its own,
 *      marked "question": true, and a question part carries nothing but the film's own question;
 *   3. a figure must be one of the lesson's own figures (its alt text, caption and key words are copied
 *      from the lesson, never retyped);
 *   4. every figure states what it gives away: "answers" is the id of the question scene whose answer the
 *      figure shows, or null when the checker judged that it shows none. A figure that answers a question
 *      may not appear before that question's reveal scene starts;
 *   5. no part begins between a question and its reveal, whatever "answers" says;
 *   6. a section must be a heading of the lesson; a word's definition must be a run of the film's own words,
 *      and the word is shown from the caption line in which the film says them, not before.
 */
export function applyMap(map, times, outline, key, cues = []) {
  const problems = [];
  const bad = (m) => problems.push(m);
  if (!map || typeof map !== 'object') return { parts: [], problems: ['the file is not a JSON object'] };
  if (map.film !== key) bad(`"film" is ${JSON.stringify(map.film)}; the file's place says ${JSON.stringify(key)}`);
  if (!map.checked || typeof map.checked.by !== 'string' || !/^\d{4}-\d{2}-\d{2}$/.test(map.checked.on ?? '')) bad('"checked" must say who checked the map and when: { "by": "...", "on": "YYYY-MM-DD" }');
  if (!Array.isArray(map.parts) || !map.parts.length) return { parts: [], problems: [...problems, '"parts" is empty'] };

  const scene = new Map(times.scenes.map((s, i) => [s.id, { ...s, i }]));
  const figureBySrc = new Map(outline.figures.map((f) => [f.src, f]));
  const headingIds = new Set(outline.headings.map((h) => h.id));
  const questionAt = new Map(times.questions.map((q) => [q.scene, q]));
  const parts = [];
  let prevStart = -1;
  let prevIndex = -1;
  map.parts.forEach((p, n) => {
    const where = `part ${n + 1} (${p?.from ?? '?'})`;
    const s = scene.get(p?.from);
    if (!s) return bad(`${where}: no scene with that id in the film's script`);
    if (s.start === null) return bad(`${where}: that scene has no start time`);
    if (s.i <= prevIndex || s.start < prevStart) return bad(`${where}: parts must be in film order`);
    prevIndex = s.i; prevStart = s.start;
    const q = questionAt.get(p.from);
    if (p.question && !q) bad(`${where}: marked as a question, but the film does not pause after this scene`);
    if (q && !p.question) bad(`${where}: the film asks a question here and pauses; mark the part "question": true`);
    // A question part starts when the film asks (which can be a sentence or two into its scene).
    const part = { from: p.from, start: n === 0 ? 0 : q && p.question ? q.start : s.start };
    if (p.question) {
      for (const k of ['figure', 'term', 'section', 'title']) if (p[k] !== undefined) bad(`${where}: a question part carries only the film's question; remove "${k}"`);
      if (q) Object.assign(part, { question: q.text, revealStart: q.revealStart });
      parts.push(part);
      return;
    }
    if (typeof p.title !== 'string' || !p.title.trim()) bad(`${where}: needs a title`);
    else if (p.title.length > 60) bad(`${where}: the title is longer than 60 characters`);
    part.title = p.title;
    if (p.section !== undefined) {
      if (!headingIds.has(p.section)) bad(`${where}: the lesson has no heading with the id "${p.section}"`);
      else part.section = { id: p.section, text: outline.headings.find((h) => h.id === p.section).text };
    }
    if (p.term !== undefined) {
      const ok = p.term && typeof p.term.word === 'string' && typeof p.term.def === 'string';
      if (!ok) bad(`${where}: "term" needs a "word" and a "def"`);
      else {
        // The definition must be words the film says, and the word comes up when the film says them.
        const at = saidAt(cues, p.term.def);
        if (at === null) bad(`${where}: the definition of "${p.term.word}" is not the film's own words (it must be a run of words from the captions)`);
        else part.term = { word: p.term.word, def: p.term.def, at };
      }
    }
    if (p.figure !== undefined) {
      const fig = p.figure && figureBySrc.get(p.figure.src);
      if (!fig) bad(`${where}: "${p.figure?.src}" is not a figure in this lesson`);
      else if (!fig.alt.startsWith('AI-generated illustration:')) bad(`${where}: the lesson's figure "${fig.src}" lacks the "AI-generated illustration:" alt text`);
      if (!p.figure || !('answers' in p.figure)) bad(`${where}: the figure must say what it gives away: "answers": "<question scene id>" or null`);
      else if (p.figure.answers !== null) {
        const aq = questionAt.get(p.figure.answers);
        if (!aq) bad(`${where}: "answers" names "${p.figure.answers}", which is not a question scene in this film`);
        else if (s.start < aq.revealStart) bad(`${where}: the figure answers ${aq.scene} but would appear at ${s.start}s, before the film gives the answer at ${aq.revealStart}s`);
      }
      if (fig) part.figure = { src: fig.src, alt: fig.alt, caption: fig.caption, width: fig.width, height: fig.height, keyItems: fig.keyItems, scaffold: fig.scaffold };
    }
    // Rule 5: nothing between a question and its reveal.
    for (const tq of times.questions) {
      if (s.start > tq.start && s.start < tq.revealStart) bad(`${where}: starts between the question ${tq.scene} and its answer; a part may not begin there`);
    }
    parts.push(part);
  });
  if (map.parts[0] && scene.get(map.parts[0].from)?.i !== 0) bad(`the first part must start at the film's first scene (${times.scenes[0]?.id})`);
  for (const q of times.questions) if (!map.parts.some((p) => p.from === q.scene)) bad(`the film asks a question at ${q.scene}; the map needs a part for it`);
  // The part after a question must start exactly at the reveal, or the question would stay up over the answer.
  parts.forEach((p, n) => {
    if (p.question === undefined) return;
    const nx = parts[n + 1];
    if (!nx) bad(`part ${n + 1} (${p.from}): a question cannot be the last part`);
    else if (nx.start !== p.revealStart) bad(`part ${n + 2} (${nx.from}): the part after a question must start at its reveal scene (${p.revealStart}s), not ${nx.start}s`);
  });
  parts.forEach((p, n) => { p.end = n + 1 < parts.length ? parts[n + 1].start : null; });
  parts.forEach((p, n) => {
    if (p.term && (p.term.at < p.start || (p.end !== null && p.term.at >= p.end))) bad(`part ${n + 1} (${p.from}): the film defines "${p.term.word}" at ${p.term.at}s, outside this part`);
  });
  const known = new Set(['from', 'title', 'question', 'section', 'term', 'figure']);
  map.parts.forEach((p, n) => { for (const k of Object.keys(p ?? {})) if (!known.has(k)) bad(`part ${n + 1} (${p.from}): unknown field "${k}"`); });
  return { parts, problems };
}

/* ------------------------------------------------------------------ one film, from disk */

const cache = new Map();
const readOnce = (file, parse) => {
  if (!cache.has(file)) {
    let v = null;
    try { if (existsSync(file)) v = parse(readFileSync(file, 'utf8')); } catch { v = null; }
    cache.set(file, v);
  }
  return cache.get(file);
};

/** Where a film's script is: explainers/<lesson>/script.json for a file named explainer, else
 *  explainers/<lesson>/<name>/script.json. */
export const scriptPath = (lesson, name) => (name === 'explainer' ? `explainers/${lesson}/script.json` : `explainers/${lesson}/${name}/script.json`);

/**
 * Everything the theater knows about one film.
 *   key       "<folder>/<name>": the film's file under /explainers/ without ".mp4"
 *   lesson    the lesson slug, or null for a film with no lesson page (a method film)
 *   index     the film's place in the lesson's `films` (null for the opening film or a film that is not placed)
 *   duration  seconds
 * Returns { key, status, why, cues, lines, times, region, parts, mapProblems } where status is
 *   'mapped'    hand-checked parts, with figures on cue
 *   'timed'     every spoken scene has a start; the film's questions are known
 *   'partial'   at least four scenes in five have a start
 *   'captions'  no usable scene times: the transcript still follows the film
 *   'none'      no caption file either
 */
export function filmTimeline(root, { key, lesson = null, index = null, duration = 0 }) {
  const [folder, name] = [key.slice(0, key.lastIndexOf('/')), key.slice(key.lastIndexOf('/') + 1)];
  const cues = readOnce(join(root, 'public/explainers', `${key}.vtt`), parseVtt) ?? [];
  const script = readOnce(join(root, scriptPath(folder, name)), JSON.parse);
  const outline = lesson ? readOnce(join(root, 'src/content/lessons', lesson, 'lesson.mdx'), lessonOutline) : null;
  const region = outline ? filmRegion(outline, index) : { section: null, sections: [], figures: [] };
  const base = { key, cues, lines: transcriptLines(cues), region, times: null, parts: [], mapProblems: [] };
  if (!cues.length) return { ...base, status: 'none', why: 'no caption file' };
  if (!script || !Array.isArray(script.scenes)) return { ...base, status: 'captions', why: 'no script.json for this film' };
  const times = sceneTimes(script, cues, duration);
  const st = timingStatus(times);
  if (st === 'untimed') return { ...base, status: 'captions', why: `only ${times.matched} of ${times.spoken} spoken scenes could be found in the captions` };
  const out = { ...base, times, status: st, why: st === 'timed' ? '' : `${times.spoken - times.matched} of ${times.spoken} spoken scenes not found; each joins the scene before it` };
  const mapFile = join(root, MAPS_DIR, `${key}.json`);
  if (outline && existsSync(mapFile)) {
    let map = null;
    try { map = JSON.parse(readFileSync(mapFile, 'utf8')); } catch { /* reported below */ }
    const { parts, problems } = applyMap(map, times, outline, key, cues);
    if (problems.length) out.mapProblems = problems;
    else { out.parts = parts; out.status = 'mapped'; }
  }
  return out;
}
