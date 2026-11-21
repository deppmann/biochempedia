// Rules shared by scripts/check-side-hops.mjs and scripts/side-hops/import-kit.mjs.

export const KINDS = ['real-world-case', 'true-story', 'see-or-do', 'myth', 'analogy'];
/** A story or a claim needs a source; a comparison or a thing to try may stand alone. */
export const SOURCE_OPTIONAL = ['analogy', 'see-or-do'];

/** The text of each ## heading in a lesson.mdx, as the page shows it. */
export function lessonHeadings(mdx) {
  const body = mdx.replace(/^---\n[\s\S]*?\n---\n/, '');
  const out = [];
  let fenced = false;
  for (const line of body.split('\n')) {
    if (/^\s*(```|~~~)/.test(line)) fenced = !fenced;
    if (fenced) continue;
    const m = /^##\s+(.+?)\s*#*\s*$/.exec(line);
    if (m) out.push(m[1].replace(/\[([^\]]*)\]\([^)]*\)/g, '$1').replace(/<[^>]+>/g, '').replace(/[*`]|\b_|_\b/g, '').trim());
  }
  return out;
}

const text = (v) => typeof v === 'string' && v.trim().length > 0;
const onlyKeys = (o, keys, where, bad) => {
  for (const k of Object.keys(o)) if (!keys.includes(k)) bad(`${where}: unknown field "${k}"`);
  for (const k of keys) if (!(k in o)) bad(`${where}: missing field "${k}"`);
};

/**
 * Every problem with one data file. `fileSlug` is the file's name without .json; `headings` is the
 * lesson's list (null when the lesson does not exist); `audioFound(file)` says whether the audio is on
 * disk or in media-manifest.json (used for pictures too).
 */
export function problemsIn(data, { fileSlug, headings, audioFound }) {
  const out = [];
  const bad = (m) => out.push(m);
  if (typeof data !== 'object' || data === null || Array.isArray(data)) return ['the file is not a JSON object'];
  onlyKeys(data, ['slug', 'updated', 'hops', 'audio'], 'top level', bad);
  if (data.slug !== fileSlug) bad(`slug "${data.slug}" does not match the file name`);
  if (headings === null) bad(`no lesson at src/content/lessons/${data.slug}/lesson.mdx`);
  if (!/^\d{4}-\d{2}-\d{2}$/.test(data.updated ?? '') || Number.isNaN(Date.parse(data.updated))) bad('updated must be a date, YYYY-MM-DD');

  if (!Array.isArray(data.hops) || data.hops.length === 0) bad('hops must be a list with at least one Side Hop');
  else {
    const placed = new Set();
    data.hops.forEach((h, i) => {
      const at = `hop ${i + 1}`;
      if (typeof h !== 'object' || h === null) { bad(`${at}: not an object`); return; }
      onlyKeys(h, ['afterHeading', 'kind', 'title', 'text', 'sources', ...('image' in h ? ['image'] : [])], at, bad);
      if ('image' in h) {
        const im = h.image;
        if (typeof im !== 'object' || im === null) bad(`${at}: image must be an object`);
        else {
          onlyKeys(im, ['file', 'alt', 'caption', 'width', 'height'], `${at}, image`, bad);
          if (!new RegExp(`^side-hops/${fileSlug}-\\d+\\.jpg$`).test(im.file ?? '')) bad(`${at}: image file must be side-hops/${fileSlug}-<n>.jpg`);
          else if (!audioFound(im.file)) bad(`${at}: ${im.file} is in neither public/ nor media-manifest.json`);
          if (!text(im.alt) || !im.alt.startsWith('AI-generated illustration:')) bad(`${at}: image alt must start "AI-generated illustration:"`);
          if (!text(im.caption)) bad(`${at}: image caption is empty`);
          if (!(im.width > 0) || !(im.height > 0)) bad(`${at}: image width and height must be positive numbers`);
        }
      }
      if (!KINDS.includes(h.kind)) bad(`${at}: kind "${h.kind}" is not one of ${KINDS.join(', ')}`);
      if (!text(h.title)) bad(`${at}: title is empty`);
      if (!text(h.text)) bad(`${at}: text is empty`);
      if (!text(h.afterHeading)) bad(`${at}: afterHeading is empty`);
      else {
        if (headings && !headings.includes(h.afterHeading)) bad(`${at}: the lesson has no ## heading "${h.afterHeading}"`);
        if (placed.has(h.afterHeading)) bad(`${at}: a second Side Hop after "${h.afterHeading}"`);
        placed.add(h.afterHeading);
      }
      if (!Array.isArray(h.sources)) { bad(`${at}: sources must be a list`); return; }
      if (h.sources.length === 0 && !SOURCE_OPTIONAL.includes(h.kind)) bad(`${at}: a ${h.kind} needs at least one source`);
      h.sources.forEach((s, j) => {
        const sat = `${at}, source ${j + 1}`;
        if (typeof s !== 'object' || s === null) { bad(`${sat}: not an object`); return; }
        onlyKeys(s, ['citation', 'url'], sat, bad);
        if (!text(s.citation)) bad(`${sat}: citation is empty`);
        let url = null;
        try { url = new URL(s.url); } catch { /* reported next */ }
        if (!url || url.protocol !== 'https:') bad(`${sat}: url must be a full https address (got ${JSON.stringify(s.url)})`);
      });
    });
    if (data.hops.filter((h) => h?.kind === 'analogy').length > 1) bad('more than one analogy in this lesson');
  }

  const a = data.audio;
  if (typeof a !== 'object' || a === null) bad('audio is missing');
  else {
    onlyKeys(a, ['title', 'file', 'durationSec', 'narration', 'transcript'], 'audio', bad);
    if (!text(a.title)) bad('audio: title is empty');
    if (a.file !== `side-hops/${fileSlug}.mp3`) bad(`audio: file must be side-hops/${fileSlug}.mp3`);
    else if (!audioFound(a.file)) bad(`audio: ${a.file} is in neither public/ nor media-manifest.json`);
    if (typeof a.durationSec !== 'number' || !(a.durationSec > 0)) bad('audio: durationSec must be a positive number');
    if (!text(a.narration) || !/\bAI\b/.test(a.narration)) bad('audio: narration must say the voice is AI');
    if (!text(a.transcript)) bad('audio: transcript is empty');
  }
  return out;
}
