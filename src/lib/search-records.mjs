/* Typed search records (2026-11-22): everything on the site worth finding that is not a lesson page.

   The site search has one full-text index, Pagefind's, in /pagefind/. Lesson pages go in as they
   always have (Pagefind reads the built HTML). Everything else goes in as RECORDS: one small HTML
   document per film, method, Side Hop card, flashcard deck and simulation, written
   by src/pages/search-records.json.ts at build time and added to the same index by
   scripts/build-search-index.mjs. Each page and record carries a `type` filter, so one search can be
   narrowed to any set of types (the tick boxes on /search/) and each type ranked on its own.

   A LADDER is one idea taught at several levels, with its films from the simplest level up (the
   films-page ladder player, /films/?ladder=<id>). Its record holds the idea's name, its blurb and
   other names, and the titles of the films and lessons on it.

   This file is plain JavaScript with no Astro or DOM, so the build script, the browser and the Node
   check (scripts/test-search-records.mjs) all read the same definitions.

   Ranking inside a record is Pagefind's: the title is the record's <h1> (weight 7), the lead line
   (the lesson a film belongs to, a method's one-line summary) weighs 3, headings 5, and the body
   (the film's narration, a story's text, a card's front and back) 1. So a word in a title outranks
   the same word in a script.

   Deep links. A film's narration is cut into short runs of one to three sentences, each under a
   heading whose id is `t-<second>` and whose text is the clock ("1:15"). Pagefind returns the run
   that matched as a sub-result with that anchor, and the search turns it into the film's page with
   ?film=<key>&at=<second> (resumeFromLink in src/lib/film-progress.ts seeks there). */

/** The kinds of thing the search can find, in the order the tick boxes list them. `group` puts the
 *  boxes in two rows: what most people come for, then the rest. */
export const SEARCH_TYPES = [
  { key: 'lesson', label: 'Lessons', one: 'lesson', many: 'lessons', group: 'main' },
  { key: 'ladder', label: 'Ladders', one: 'ladder', many: 'ladders', group: 'main' },
  { key: 'film', label: 'Films', one: 'film', many: 'films', group: 'main' },
  { key: 'sidehop', label: 'Side Hops', one: 'Side Hop', many: 'Side Hops', group: 'main' },
  { key: 'method', label: 'Methods', one: 'method', many: 'methods', group: 'more' },
  { key: 'flashcards', label: 'Flashcards', one: 'flashcard deck', many: 'flashcard decks', group: 'more' },
  { key: 'sim', label: 'Simulations', one: 'simulation', many: 'simulations', group: 'more' },
  { key: 'toolkit', label: 'Math toolkit', one: 'math toolkit section', many: 'math toolkit sections', group: 'more' },
];
export const TYPE_KEYS = SEARCH_TYPES.map((t) => t.key);

/** A time anchor in a record, and back. */
export const timeId = (sec) => `t-${Math.max(0, Math.floor(sec))}`;
export const secondsOfId = (id) => {
  const m = /^t-(\d+)$/.exec(id || '');
  return m ? Number(m[1]) : null;
};
export const clock = (sec) => `${Math.floor(sec / 60)}:${String(Math.floor(sec % 60)).padStart(2, '0')}`;

/** The link that plays a film from a second: the film's own page, told which film and where. */
export function filmAt(url, filmKey, sec) {
  const [base, hash] = url.split('#');
  if (!filmKey || sec == null) return url;
  const sep = base.includes('?') ? '&' : '?';
  return `${base}${sep}film=${encodeURIComponent(filmKey)}&at=${sec}${hash ? `#${hash}` : ''}`;
}

const ENTITIES = { '&amp;': '&', '&lt;': '<', '&gt;': '>', '&quot;': '"', '&#39;': "'", '&nbsp;': ' ', '&lrm;': '', '&rlm;': '' };
const toSec = (s) => {
  const p = s.trim().split(':').map(Number);
  return p.length === 3 ? p[0] * 3600 + p[1] * 60 + p[2] : p[0] * 60 + p[1];
};

/** WebVTT cues as short runs with their start second: a run ends at the end of a sentence once it
 *  is RUN_MIN characters long, and never grows past RUN_MAX. Short enough that the run a word is in
 *  is "the line that says it", long enough that a phrase split across two cues is still one run. */
export const RUN_MIN = 90;
export const RUN_MAX = 280;
export function runsFromVtt(vtt) {
  const cues = [];
  for (const block of String(vtt).replace(/\r/g, '').split(/\n{2,}/)) {
    const lines = block.split('\n').map((l) => l.trim()).filter(Boolean);
    if (!lines.length || /^(WEBVTT|NOTE|STYLE|REGION)\b/.test(lines[0])) continue;
    const ti = lines.findIndex((l) => l.includes('-->'));
    if (ti === -1) continue;
    const text = lines.slice(ti + 1).join(' ')
      .replace(/<[^>]+>/g, '')
      .replace(/&(?:amp|lt|gt|quot|#39|nbsp|lrm|rlm);/g, (m) => ENTITIES[m] ?? m)
      .replace(/\s+/g, ' ').trim();
    if (text) cues.push({ start: toSec(lines[ti].split('-->')[0]), text });
  }
  const out = [];
  let cur = null;
  for (const c of cues) {
    if (cur && /[.?!…]["”')\]]*$/.test(cur.text) && cur.text.length >= RUN_MIN) { out.push(cur); cur = null; }
    if (cur && cur.text.length + c.text.length > RUN_MAX) { out.push(cur); cur = null; }
    cur = cur ? { start: cur.start, text: `${cur.text} ${c.text}` } : { start: c.start, text: c.text };
  }
  if (cur) out.push(cur);
  return out;
}

/** Cloze cards ("{{c1::+40 mV}}", "{{c1::answer::hint}}") as plain text. */
export const clozeText = (s) => String(s).replace(/\{\{c\d+::(.*?)(?:::[^}]*)?\}\}/g, '$1');

const esc = (s) => String(s ?? '').replace(/[&<>"]/g, (ch) => ({ '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;' })[ch]);

/**
 * @typedef {object} SearchRecord
 * @property {string} type     one of TYPE_KEYS (not 'lesson': lessons are pages)
 * @property {string} url      where a hit goes (site-relative)
 * @property {string} title
 * @property {string} [lead]   one line under the title (weight 3)
 * @property {string} [kicker] what kind it is, shown above the title ("Second film", "True story")
 * @property {string[]} [courses]  course slugs (a filter: the course chips narrow by it)
 * @property {string} [courseTitle]
 * @property {string} [level]  stage key; [levelTitle] its name
 * @property {string} [levelTitle]
 * @property {string} [lesson] title of the lesson it belongs to
 * @property {string} [ladder] the idea (hop ladder) the lesson teaches, when known
 * @property {string} [poster] picture for the result
 * @property {number} [dur]    length in seconds (films, audio)
 * @property {string} [filmKey] for time links (see filmAt)
 * @property {number} [films]  how many films a ladder plays
 * @property {{ id?: string, h?: string, text: string, w?: number }[]} parts  the body: a part with an
 *   id starts with a heading (a sub-result Pagefind can land on); w is a Pagefind weight
 */

const META_KEYS = ['kicker', 'courseTitle', 'levelTitle', 'lesson', 'ladder', 'poster', 'dur', 'filmKey', 'films'];

/** One record as the HTML document Pagefind indexes. Filters and metadata sit outside the body, so
 *  they are stored but never searched as text. */
export function recordHtml(rec) {
  if (!TYPE_KEYS.includes(rec.type) || rec.type === 'lesson') throw new Error(`search record of unknown type "${rec.type}" (${rec.url})`);
  if (!rec.url || !rec.url.startsWith('/')) throw new Error(`search record without a site-relative url: ${rec.title}`);
  const body = [`<h1>${esc(rec.title)}</h1>`];
  if (rec.lead) body.push(`<p data-pagefind-weight="3">${esc(rec.lead)}</p>`);
  for (const p of rec.parts ?? []) {
    if (p.id) body.push(`<h3 id="${esc(p.id)}">${esc(p.h ?? '')}</h3>`);
    if (p.text) body.push(p.w != null ? `<p data-pagefind-weight="${p.w}">${esc(p.text)}</p>` : `<p>${esc(p.text)}</p>`);
  }
  const tags = [`<span data-pagefind-filter="type">${esc(rec.type)}</span>`];
  for (const c of new Set(rec.courses ?? [])) tags.push(`<span data-pagefind-filter="course">${esc(c)}</span>`);
  if (rec.level) tags.push(`<span data-pagefind-filter="level">${esc(rec.level)}</span>`);
  for (const k of META_KEYS) if (rec[k] != null && rec[k] !== '') tags.push(`<span data-pagefind-meta="${k}">${esc(rec[k])}</span>`);
  return `<!doctype html><html lang="en"><head><title>${esc(rec.title)}</title></head><body><main data-pagefind-body>${body.join('')}</main>${tags.join('')}</body></html>`;
}
