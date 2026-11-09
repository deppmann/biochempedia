/**
 * rehype-abbr — make abbreviations in lesson prose readable without scrolling back.
 *
 * For each lesson (src/content/lessons/<slug>/lesson.mdx), in each section (a section starts at an <h2>):
 *   - the FIRST use of an abbreviation is spelled out: "ACTH" becomes "adrenocorticotropic hormone (ACTH)",
 *     unless the section already gives the full name, or the use is the definition itself ("full name (ACTH)");
 *   - every use is wrapped in <abbr class="ab" title="full name">, which shows the full name on hover, and
 *     as a small note on tap (the lesson page's script).
 *
 * Where the words come from: src/data/abbreviations.json, one shared list for every course. `common` terms
 * (DNA, ATP, GABA…) are labelled but never spelled out. A lesson that defines an abbreviation itself, as
 * "nerve growth factor (NGF)", uses its own wording in that lesson, and can add abbreviations the shared
 * list leaves out (a definition is accepted only when the initials match, so "building block (BrdU)"
 * is not taken as a definition).
 *
 * The inserted words carry data-no-hl, so saved highlights (src/lib/highlight-anchor.ts) still match the
 * lesson text. It runs after rehype-listen, so Listen's paragraph hashes and recorded clips are unchanged.
 * It never touches headings, links, code, buttons, figures, MDX components, or text already in <abbr>,
 * and in tables and captions it labels without spelling out, to keep cells short.
 */
import { readFileSync } from 'node:fs';

const LIST = JSON.parse(readFileSync(new URL('../data/abbreviations.json', import.meta.url), 'utf8'));

const SKIP_TAGS = new Set(['h1', 'h2', 'h3', 'h4', 'h5', 'h6', 'a', 'code', 'pre', 'kbd', 'samp', 'script', 'style',
  'svg', 'math', 'button', 'figure', 'summary', 'sup', 'sub', 'cite', 'abbr', 'dialog', 'nav', 'label']);
const NO_EXPAND = new Set(['table', 'thead', 'tbody', 'tr', 'td', 'th', 'figcaption', 'caption']);
const BLOCKS = new Set(['p', 'li', 'td', 'th', 'dd', 'dt', 'figcaption', 'blockquote']);
const isJsx = (n) => typeof n.type === 'string' && n.type.startsWith('mdx');
const escape = (s) => s.replace(/[.*+?^${}()|[\]\\]/g, '\\$&');

/** An abbreviation-shaped token: starts with a capital, has at least two capitals or digits after it. */
const TOKEN = /^[A-Z][A-Za-z0-9β-]{1,11}$/;
const capsOf = (ab) => [...ab].filter((c) => /[A-Z0-9]/.test(c)).join('').toLowerCase();

/** Does `phrase` spell out `ab`? Either the words' initials are the abbreviation's capitals in order
 *  ("nerve growth factor" → NGF), or it is one word that contains them in order ("deoxycorticosterone" → DOC). */
function spells(ab, phrase) {
  const caps = capsOf(ab);
  if (caps.length < 2) return false;
  // Chemical locants ("11-deoxycorticosterone", "2,3-bisphosphoglycerate") are not part of the initials.
  const parts = phrase.toLowerCase().replace(/(^|\s)[0-9,′']+-/g, '$1').split(/[\s-]+/).filter(Boolean);
  if (parts.map((p) => p[0]).join('') === caps) return true;
  if (parts.length !== 1) return false;
  const word = parts[0];
  if (word[0] !== caps[0]) return false;
  let i = 0;
  for (const ch of word) if (ch === caps[i]) i++;
  return i === caps.length && word.length > caps.length + 2;
}

/** The shortest run of words before "(ABBR)" that spells it out, or null. */
function definitionBefore(ab, before) {
  const words = before.replace(/\s+$/, '').split(/\s+/).slice(-8);
  for (let k = 1; k <= words.length; k++) {
    const phrase = words.slice(-k).join(' ').replace(/^[^A-Za-z0-9]+/, '').replace(/[^A-Za-z0-9)]+$/, '');
    if (phrase && spells(ab, phrase)) return phrase;
  }
  return null;
}

function textOf(node) {
  if (node.type === 'text') return node.value;
  if (isJsx(node)) return '';
  return (node.children || []).map(textOf).join('');
}

const pluralize = (s) => (/(s|us)$/.test(s) ? s : /[^aeiou]y$/.test(s) ? s.slice(0, -1) + 'ies' : s + 's');
// "cAMP response…" and "c-Jun…" keep their case at the start of a sentence.
const capitalize = (s) => (/^[a-z][A-Z-]/.test(s) ? s : s.charAt(0).toUpperCase() + s.slice(1));

export default function rehypeAbbr({ terms = LIST.terms, common = LIST.common } = {}) {
  const shared = { ...terms, ...common };
  const commonSet = new Set(Object.keys(common));

  return (tree, file) => {
    const path = (file.path || (file.history && file.history[0]) || '').split('\\').join('/');
    if (!/lessons\/[^/]+\/lesson\.mdx$/.test(path)) return;

    // 1. The lesson's own definitions: "full name (ABBR)" anywhere in its prose.
    const local = {};
    const scan = (node) => {
      if (isJsx(node)) return;
      if (node.type === 'element' && BLOCKS.has(node.tagName)) {
        const t = textOf(node);
        for (const m of t.matchAll(/\(([A-Z][A-Za-z0-9β-]{1,11}?)(s?)\)/g)) {
          const ab = m[1];
          if (!TOKEN.test(ab) || capsOf(ab).length < 2 || local[ab]) continue;
          let def = definitionBefore(ab, t.slice(0, m.index));
          if (!def) continue;
          // "Natural killer (NK) cells…" at the start of a sentence: the capital belongs to the sentence, not the name.
          const lead = t.slice(0, m.index).trimEnd();
          const startsSentence = /(^|[.!?:]["”’)]?\s+)$/.test(lead.slice(0, lead.length - def.length));
          if (startsSentence && /^[A-Z][a-z]/.test(def)) def = def.charAt(0).toLowerCase() + def.slice(1);
          local[ab] = m[2] && def.endsWith('s') ? def.slice(0, -1) : def;
        }
      }
      (node.children || []).forEach(scan);
    };
    scan(tree);

    const words = { ...shared, ...local };
    const keys = Object.keys(words).sort((a, b) => b.length - a.length);
    if (!keys.length) return;
    const RE = new RegExp(`(?<![A-Za-z0-9-])(${keys.map(escape).join('|')})(s?)(?![A-Za-z0-9α-ω])`, 'g');

    let defined = new Set();
    let sectionText = '';
    let block = { text: '', full: '' };

    const process = (value, noExpand) => {
      const out = [];
      let last = 0;
      let pending = '';
      RE.lastIndex = 0;
      for (let m; (m = RE.exec(value)); ) {
        const [tok, ab, plural] = m;
        const full = words[ab];
        const before = value.slice(0, m.index);
        const after = value.charAt(m.index + tok.length);
        const lowerSeen = (sectionText + before).toLowerCase();
        if (!defined.has(ab) && (lowerSeen.includes(full.toLowerCase()) || block.full.includes(full.toLowerCase()))) defined.add(ab);
        const isDefinition = /\(\s*$/.test(before) && after === ')';
        let chunk = value.slice(last, m.index);
        const abbr = { type: 'element', tagName: 'abbr', properties: { className: ['ab'], title: full }, children: [{ type: 'text', value: tok }] };
        if (isDefinition) {
          defined.add(ab);
          pending += chunk;
          out.push({ type: 'text', value: pending }, abbr);
          pending = '';
        } else if (!noExpand && !commonSet.has(ab) && !defined.has(ab) && !/[-'’/]/.test(after) && !/\(\s*$/.test(before)) {
          defined.add(ab);
          let spelled = plural ? pluralize(full) : full;
          const prefix = (block.text + pending + before).trimEnd();
          if (prefix === '' || /[.!?:]["”’)]?$/.test(prefix)) spelled = capitalize(spelled);
          // "a ACTH surge" → "an adrenocorticotropic hormone (ACTH) surge": the article follows the spelled-out word.
          const art = /\b(a|an|A|An) $/.exec(chunk);
          if (art) {
            const vowel = /^[aeiou]/i.test(spelled);
            const want = vowel ? 'an' : 'a';
            const fixed = art[1][0] === art[1][0].toUpperCase() ? capitalize(want) : want;
            chunk = chunk.slice(0, art.index) + fixed + ' ';
          }
          pending += chunk;
          out.push(
            { type: 'text', value: pending },
            { type: 'element', tagName: 'span', properties: { className: ['ab-x'], dataNoHl: '' }, children: [{ type: 'text', value: `${spelled} (` }] },
            abbr,
            { type: 'element', tagName: 'span', properties: { className: ['ab-x'], dataNoHl: '' }, children: [{ type: 'text', value: ')' }] },
          );
          pending = '';
        } else {
          pending += chunk;
          out.push({ type: 'text', value: pending }, abbr);
          pending = '';
        }
        last = m.index + tok.length;
      }
      if (!out.length) return null;
      const rest = value.slice(last);
      if (rest) out.push({ type: 'text', value: rest });
      return out.filter((n) => n.type !== 'text' || n.value !== '');
    };

    const walk = (node, noExpand) => {
      if (!node.children) return;
      const next = [];
      for (const child of node.children) {
        if (child.type === 'text') {
          const parts = process(child.value, noExpand);
          sectionText += child.value;
          block.text += child.value;
          if (parts) next.push(...parts);
          else next.push(child);
          continue;
        }
        if (isJsx(child)) { next.push(child); continue; }
        if (child.type === 'element') {
          if (child.tagName === 'h2') { defined = new Set(); sectionText = ''; }
          if (SKIP_TAGS.has(child.tagName)) {
            const t = textOf(child);
            sectionText += t;
            block.text += t;
          } else {
            const isBlock = BLOCKS.has(child.tagName);
            const saved = block;
            if (isBlock) block = { text: '', full: textOf(child).toLowerCase() };
            walk(child, noExpand || NO_EXPAND.has(child.tagName));
            if (isBlock) block = saved;
          }
        }
        next.push(child);
      }
      node.children = next;
    };

    walk(tree, false);
  };
}
