/* Finding a highlighted passage again, and wrapping it in <mark>s.

   A highlight is stored as text, not as a DOM path: the exact quote, plus up to
   32 characters before it (prefix) and after it (suffix). On page load we
   search the lesson text for the quote. If it appears more than once, the
   prefix and suffix pick the occurrence whose surroundings match best.

   Whitespace is ignored when matching: the text is compared with every space,
   tab and line break removed, so a re-flowed paragraph, a selection that ran
   across two paragraphs, or an edit that only changed spacing still matches.
   If the quote itself is no longer in the text, the highlight cannot be placed
   and the caller marks it "this passage changed".

   A passage that crosses element boundaries (bold, a link, two paragraphs) is
   wrapped piece by piece: one <mark> per text node, all sharing data-hl. */

/** Parts of the lesson body that are never highlighted or searched. */
export const EXCLUDE = [
  'input', 'textarea', 'select', 'option', 'button', 'label',
  'video', 'audio', 'iframe', 'canvas', 'svg', 'object', 'embed',
  'script', 'style', 'noscript', 'template', 'summary',
  'astro-island', '.card', '.design-answer', '[data-design-item]',
  '.katex-mathml', '[contenteditable]', '[data-no-hl]', '[aria-hidden="true"]',
].join(',');

const WS = /\s/;

export interface TextIndex {
  nodes: Text[];
  /** The lesson text with all whitespace removed. */
  stripped: string;
  /** For each stripped character: which node, and the offset in that node. */
  nodeOf: Int32Array;
  offOf: Int32Array;
  /** Where each node starts in `stripped`. */
  nodeStart: Int32Array;
}

export function strip(s: string): string {
  return s.replace(/\s+/g, '');
}

export function collapse(s: string): string {
  return s.replace(/\s+/g, ' ').trim();
}

export function excluded(node: Node, root: Element): boolean {
  const el = node.nodeType === 1 ? (node as Element) : node.parentElement;
  if (!el) return true;
  const hit = el.closest(EXCLUDE);
  return !!hit && root.contains(hit);
}

export function buildIndex(root: Element): TextIndex {
  const nodes: Text[] = [];
  const w = document.createTreeWalker(root, NodeFilter.SHOW_TEXT, {
    acceptNode: (n) => (excluded(n, root) ? NodeFilter.FILTER_REJECT : NodeFilter.FILTER_ACCEPT),
  });
  let n: Node | null;
  let total = 0;
  while ((n = w.nextNode())) {
    nodes.push(n as Text);
    total += (n as Text).data.length;
  }
  const nodeOf = new Int32Array(total);
  const offOf = new Int32Array(total);
  const nodeStart = new Int32Array(nodes.length + 1);
  const parts: string[] = [];
  let k = 0;
  nodes.forEach((t, i) => {
    nodeStart[i] = k;
    const d = t.data;
    let piece = '';
    for (let j = 0; j < d.length; j++) {
      if (WS.test(d[j])) continue;
      piece += d[j];
      nodeOf[k] = i;
      offOf[k] = j;
      k++;
    }
    parts.push(piece);
  });
  nodeStart[nodes.length] = k;
  return { nodes, stripped: parts.join(''), nodeOf: nodeOf.subarray(0, k), offOf: offOf.subarray(0, k), nodeStart };
}

/** Number of non-whitespace characters in node i before `offset`, as a stripped index. */
function strippedAt(idx: TextIndex, i: number, offset: number): number {
  const d = idx.nodes[i].data;
  let c = 0;
  for (let j = 0; j < Math.min(offset, d.length); j++) if (!WS.test(d[j])) c++;
  return idx.nodeStart[i] + c;
}

/** The stripped [start, end) covered by a DOM range, or null if it covers no lesson text. */
export function rangeToOffsets(idx: TextIndex, range: Range): [number, number] | null {
  let first = -1, last = -1;
  for (let i = 0; i < idx.nodes.length; i++) {
    if (range.intersectsNode(idx.nodes[i])) {
      if (first < 0) first = i;
      last = i;
    } else if (first >= 0) break;
  }
  if (first < 0) return null;
  const s = strippedAt(idx, first, idx.nodes[first] === range.startContainer ? range.startOffset : 0);
  const e = strippedAt(idx, last, idx.nodes[last] === range.endContainer ? range.endOffset : idx.nodes[last].data.length);
  return e > s ? [s, e] : null;
}

/** Readable text around a stripped span: the passage itself plus ≤32 characters either side. */
export function describe(idx: TextIndex, s: number, e: number) {
  const nodeText = (from: number, to: number) => {
    // Raw text (with its spaces) between stripped positions, joined across nodes.
    if (to <= from) return '';
    const a = idx.nodeOf[from], ao = idx.offOf[from];
    const b = idx.nodeOf[to - 1], bo = idx.offOf[to - 1] + 1;
    let out = '';
    for (let i = a; i <= b; i++) {
      const d = idx.nodes[i].data;
      const piece = d.slice(i === a ? ao : 0, i === b ? bo : d.length);
      // Separate text from different blocks (two paragraphs) with a space.
      if (out && i > a && blockOf(idx.nodes[i]) !== blockOf(idx.nodes[i - 1])) out += ' ';
      out += piece;
    }
    return out;
  };
  const quote = collapse(nodeText(s, e));
  const before = collapse(nodeText(Math.max(0, s - 48), s));
  const after = collapse(nodeText(e, Math.min(idx.stripped.length, e + 48)));
  return { quote, prefix: before.slice(-32), suffix: after.slice(0, 32) };
}

const BLOCK = 'p,li,h1,h2,h3,h4,h5,h6,blockquote,td,th,dt,dd,figcaption,pre,div,details,section';
function blockOf(t: Text): Element | null {
  return t.parentElement?.closest(BLOCK) ?? null;
}

/** Find a quote in the lesson text; returns the stripped [start, end) of the best match. */
export function locate(idx: TextIndex, quote: string, prefix: string, suffix: string): [number, number] | null {
  const q = strip(quote);
  if (!q) return null;
  const text = idx.stripped;
  const p = strip(prefix), x = strip(suffix);
  let best: [number, number] | null = null;
  let bestScore = -1;
  for (let i = text.indexOf(q); i >= 0; i = text.indexOf(q, i + 1)) {
    let sp = 0;
    while (sp < p.length && i - 1 - sp >= 0 && text[i - 1 - sp] === p[p.length - 1 - sp]) sp++;
    let sx = 0;
    const j = i + q.length;
    while (sx < x.length && j + sx < text.length && text[j + sx] === x[sx]) sx++;
    const score = sp + sx;
    if (score > bestScore) { bestScore = score; best = [i, j]; }
    if (score === p.length + x.length) break;
  }
  return best;
}

/** Wrap the stripped span [s, e) in marks. Returns the marks, in document order. */
export function wrap(idx: TextIndex, s: number, e: number, make: () => HTMLElement): HTMLElement[] {
  if (e <= s) return [];
  const a = idx.nodeOf[s], ao = idx.offOf[s];
  const b = idx.nodeOf[e - 1], bo = idx.offOf[e - 1] + 1;
  const out: HTMLElement[] = [];
  for (let i = a; i <= b; i++) {
    let node = idx.nodes[i];
    const from = i === a ? ao : 0;
    const to = i === b ? bo : node.data.length;
    if (!node.data.slice(from, to).trim()) continue;
    if (to < node.data.length) node.splitText(to);
    if (from > 0) node = node.splitText(from);
    const m = make();
    node.parentNode!.insertBefore(m, node);
    m.appendChild(node);
    out.push(m);
  }
  return out;
}

/** Remove the marks for one highlight (or all, when id is omitted), keeping their text. */
export function unwrap(root: Element, id?: string) {
  const sel = id ? `mark.bp-hl[data-hl="${CSS.escape(id)}"]` : 'mark.bp-hl';
  const parents = new Set<Node>();
  for (const m of Array.from(root.querySelectorAll(sel))) {
    const parent = m.parentNode;
    if (!parent) continue;
    while (m.firstChild) parent.insertBefore(m.firstChild, m);
    parent.removeChild(m);
    parents.add(parent);
  }
  parents.forEach((p) => p.normalize());
}
