/**
 * rehype-listen — mark each readable block of a lesson so the Listen player can read it aloud.
 *
 * Runs AFTER rehype-sub-sup (so <sub>/<sup> already exist). For every paragraph, list item and
 * blockquote paragraph in the lesson prose it adds data-say="<hash>", where hash is the first 12
 * hex digits of sha256(speakable text). It skips anything inside details/summary, tables, figures,
 * code/pre, headings and MDX components (mdxJsx* nodes), which the player does not read.
 *
 * Speakable text is the block's text with <sub>X</sub> read as " sub X", <sup>N</sup> as
 * " to the N", "×" as " times ", "−" as " minus ", and whitespace collapsed.
 *
 * For lesson files (src/content/lessons/<dir>/lesson.mdx) it also writes .listen/<slug>.json, a list
 * of {hash, text} in reading order (duplicates dropped), which scripts/listen-render.mjs turns into
 * Kokoro clips. .listen/ is gitignored. The hash ties a clip to its exact text: edit a paragraph and
 * its old clip is simply no longer used, and that paragraph is skipped until the next render.
 *
 * It also adds each EquationCard's `say` sentence to the same list (2026-11-06), so the card's
 * "Read aloud" button plays a Kokoro clip too. The site never uses the device voice (Chris:
 * "we should never do that").
 */
import { createHash } from 'node:crypto';
import { mkdirSync, writeFileSync } from 'node:fs';
import { fileURLToPath } from 'node:url';

const OUT_DIR = fileURLToPath(new URL('../../.listen/', import.meta.url));
const SKIP_TAGS = new Set(['details', 'summary', 'table', 'figure', 'pre', 'code', 'h1', 'h2', 'h3', 'h4', 'h5', 'h6', 'script', 'style', 'svg', 'math', 'button', 'dialog', 'nav']);
const NO_TEXT = new Set(['script', 'style', 'svg', 'math', 'button']);

const isJsx = (n) => n.type === 'mdxJsxFlowElement' || n.type === 'mdxJsxTextElement';

/** Text a listener should hear for one node (nested lists excluded: they are read on their own). */
function speak(node) {
  if (node.type === 'text') return node.value;
  if (node.type === 'element') {
    if (NO_TEXT.has(node.tagName) || node.tagName === 'ul' || node.tagName === 'ol') return '';
    if (node.tagName === 'br') return ' ';
    const inner = (node.children || []).map(speak).join('');
    if (node.tagName === 'sub') return ` sub ${inner}`;
    if (node.tagName === 'sup') return ` to the ${inner}`;
    return inner;
  }
  if (node.type === 'mdxJsxTextElement') return (node.children || []).map(speak).join('');
  return '';
}

export function speakable(node) {
  return speak(node)
    .replace(/×/g, ' times ')
    .replace(/−/g, ' minus ')
    .replace(/\s+/g, ' ')
    .trim();
}

export const hashOf = (text) => createHash('sha256').update(text).digest('hex').slice(0, 12);

/** What an EquationCard's Read aloud button says: its `say` prop, with notation spoken as words. */
export const cardSpeakable = (say) => String(say || '')
  .replace(/_/g, ' sub ')
  .replace(/×/g, ' times ')
  .replace(/−/g, ' minus ')
  .replace(/\s+/g, ' ')
  .trim();

/** Every EquationCard's say sentence, wherever it sits in the tree. */
function cards(node, out) {
  for (const c of node.children || []) {
    if (isJsx(c) && c.name === 'EquationCard') {
      const a = (c.attributes || []).find((x) => x.type === 'mdxJsxAttribute' && x.name === 'say');
      const text = cardSpeakable(typeof a?.value === 'string' ? a.value : '');
      if (text) out.push({ hash: hashOf(text), text });
    }
    cards(c, out);
  }
}

function mark(node, out) {
  const text = speakable(node);
  if (!text || !/[\p{L}\p{N}]/u.test(text)) return;
  const hash = hashOf(text);
  node.properties = { ...(node.properties || {}), dataSay: hash };
  out.push({ hash, text });
}

function walk(node, out, inQuote = false) {
  for (const c of node.children || []) {
    if (isJsx(c)) continue;
    if (c.type !== 'element') continue;
    if (SKIP_TAGS.has(c.tagName)) continue;
    if (c.tagName === 'p') { mark(c, out); continue; }
    if (c.tagName === 'li') {
      // A loose list item holds paragraphs: mark those. A tight one is read as one block.
      const hasBlocks = (c.children || []).some((k) => k.type === 'element' && k.tagName === 'p');
      if (!hasBlocks) mark(c, out);
      walk(c, out, inQuote);
      continue;
    }
    walk(c, out, inQuote || c.tagName === 'blockquote');
  }
}

/** The lesson slug for a lesson file, or null for any other MDX file. */
function lessonSlug(file) {
  const path = (file.path || file.history?.[0] || '').split('\\').join('/');
  const m = /\/src\/content\/lessons\/([^/]+)\/lesson\.mdx?$/.exec(path);
  if (!m) return null;
  const fm = file.data?.astro?.frontmatter;
  return (fm && typeof fm.slug === 'string' && fm.slug) || m[1];
}

export default function rehypeListen() {
  return (tree, file) => {
    const out = [];
    walk(tree, out);
    cards(tree, out);
    const slug = lessonSlug(file);
    if (!slug) return;
    const seen = new Set();
    const list = out.filter((b) => (seen.has(b.hash) ? false : seen.add(b.hash)));
    try {
      mkdirSync(OUT_DIR, { recursive: true });
      writeFileSync(`${OUT_DIR}${slug}.json`, JSON.stringify(list, null, 1) + '\n');
    } catch { /* a read-only checkout still builds; only the render script needs these files */ }
  };
}
