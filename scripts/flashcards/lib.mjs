/* Shared, dependency-free helpers for lesson flashcards.

   Used by scripts/check-flashcards.mjs (CI) and by the generation tools in this
   folder. Nothing here calls a model.

   A deck lives at src/data/flashcards/<slug>.json. Every card carries a `quote`:
   a short span copied verbatim from the lesson body as a reader sees it. The
   quote does two jobs. It grounds the card (a card whose quote is not in the
   lesson is rejected), and on the page it is what "Show in lesson" scrolls to
   and highlights.

   Regeneration is incremental. The deck stores a hash of each section's text;
   when a lesson is edited, only cards whose section changed need a model again. */

import { createHash } from 'node:crypto';
// The per-card rules are shared with the Worker that drafts a learner's personal cards (worker/helper.js).
import { LEVELS, TYPES, GOALS, norm, checkCardShape } from '../../src/lib/card-rules.mjs';

export { LEVELS, TYPES, GOALS, norm };

/** Split an .mdx file into its raw frontmatter and body. */
export function splitMdx(src) {
  const m = /^---\n([\s\S]*?)\n---\n?([\s\S]*)$/.exec(src);
  return m ? { fm: m[1], body: m[2] } : { fm: '', body: src };
}

/** Markdown/MDX source → the text a reader sees, roughly as the browser's textContent.
 *  Good enough to check that a quote is really in the lesson. */
export function plain(md) {
  return md
    .replace(/^import .*$/gm, ' ')
    .replace(/<summary>(.*?)<\/summary>/g, ' ¶ ')     // a fold label is not lesson text, and no quote may span it
    .replace(/<\/?[A-Za-z][^>]*>/g, ' ')        // HTML and component tags
    .replace(/\{\/\*[\s\S]*?\*\/\}/g, ' ')      // MDX comments
    .replace(/!\[([^\]]*)\]\([^)]*\)/g, '$1')
    .replace(/\[([^\]]+)\]\([^)]*\)/g, '$1')    // links keep their text
    .replace(/^#{1,6}\s+/gm, '')
    .replace(/^\s*>\s?/gm, '')
    .replace(/^\s*(?:[-*+]|\d+\.)\s+/gm, '')
    .replace(/\*\*|`/g, '')
    .replace(/\*([^*\n]+)\*/g, '$1')
    .replace(/[“”]/g, '"').replace(/[‘’]/g, "'")
    .replace(/\s+/g, ' ')
    .trim();
}


/** The body's ## / ### sections, in order, with their source and plain text. */
export function sections(body) {
  const out = [];
  let fence = false;
  let cur = { heading: '(opening)', depth: 1, src: '' };
  out.push(cur);
  for (const line of body.split('\n')) {
    if (/^\s*```/.test(line)) fence = !fence;
    const m = !fence && /^(#{2,3})\s+(.+?)\s*$/.exec(line);
    if (m) { cur = { heading: m[2], depth: m[1].length, src: '' }; out.push(cur); continue; }
    cur.src += line + '\n';
  }
  return out.map((s) => ({ ...s, text: plain(s.src), hash: hash(plain(s.src)) })).filter((s) => s.text);
}

export const hash = (t) => createHash('sha256').update(t).digest('hex').slice(0, 12);

/** Which section holds this quote (null if none). */
export function sectionOf(secs, quote) {
  const q = norm(quote);
  return secs.find((s) => s.text.includes(q)) ?? null;
}

/** Validate a deck against its lesson. Returns { errors, warnings, stale }. */
export function checkDeck(deck, body) {
  const errors = [];
  const warnings = [];
  const secs = sections(body);
  const ids = new Set();
  if (!Array.isArray(deck.cards) || deck.cards.length === 0) errors.push('deck has no cards');
  for (const c of deck.cards ?? []) {
    const where = `card ${c.id ?? '?'}`;
    if (!c.id || ids.has(c.id)) errors.push(`${where}: missing or duplicate id`);
    ids.add(c.id);
    const shape = checkCardShape(c);
    errors.push(...shape.errors);
    warnings.push(...shape.warnings);
    if (c.quote && !shape.errors.some((e) => e.includes('quote')) && !sectionOf(secs, c.quote)) errors.push(`${where}: quote not found in the lesson body: "${c.quote.slice(0, 70)}…"`);
  }
  // Staleness: a section the deck's cards came from has changed since generation.
  const now = new Map(secs.map((s) => [s.heading, s.hash]));
  const stale = Object.entries(deck.sectionHashes ?? {}).filter(([h, v]) => now.get(h) !== v).map(([h]) => h);
  return { errors, warnings, stale };
}
