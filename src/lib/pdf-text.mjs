/* Read the text of a PDF in the browser, for the syllabus matcher (/teach/match/).

   The reading is done by Mozilla's PDF.js (the npm package pdfjs-dist), bundled with the site and
   loaded only when a teacher opens a PDF, so the page stays light for everyone else. Both the
   library and its worker are the site's own files (Vite gives the worker its own hashed URL);
   nothing is loaded from another site and the PDF never leaves the device. Only text is read:
   no page is drawn, so PDF.js asks for no fonts, character maps or image decoders.

   A PDF holds words as scattered pieces with a position each, not as lines. The matcher reads a
   schedule line by line, so linesFromItems() puts the pieces back into lines by their height on
   the page, left to right, with " | " where a wide gap marks a table column (the same mark the
   Word reader uses for table cells).

   pdfText() returns { text, pages, read }. A scanned PDF has pictures of words and no text, so
   its text comes back empty: the page then says "paste the text". It throws when the file is not
   a PDF that can be opened (damaged, or locked with a password). */

export const MAX_PAGES = 60;

/** Lines of text from one page's PDF.js text items ({ str, transform, width, height }). */
export function linesFromItems(items) {
  const bits = [];
  for (const it of items ?? []) {
    if (!it || typeof it.str !== 'string' || !it.str.trim()) continue;
    const t = it.transform ?? [1, 0, 0, 1, 0, 0];
    // The size of the type: the item's height, or the scale of its matrix when the height is missing.
    const size = Math.abs(it.height) || Math.hypot(t[2], t[3]) || Math.hypot(t[0], t[1]) || 10;
    bits.push({ str: it.str, x: t[4], y: t[5], w: Math.abs(it.width) || 0, size });
  }
  // Top of the page first (PDF heights are measured from the bottom).
  bits.sort((a, b) => b.y - a.y || a.x - b.x);
  const lines = [];
  for (const b of bits) {
    const line = lines[lines.length - 1];
    // The same line when the baselines are within about half a letter's height of each other.
    if (line && Math.abs(line.y - b.y) <= Math.max(2, Math.min(line.size, b.size) * 0.5)) line.bits.push(b);
    else lines.push({ y: b.y, size: b.size, bits: [b] });
  }
  return lines.map((line) => {
    line.bits.sort((a, b) => a.x - b.x);
    let out = '', end = null;
    for (const b of line.bits) {
      if (end !== null) {
        const gap = b.x - end;
        const size = Math.min(line.size, b.size);
        // A gap wider than two letters' height is a table column; a small one is a space between words.
        if (gap > size * 2) out = `${out.trimEnd()} | `;
        else if (gap > size * 0.15 && !/\s$/.test(out) && !/^\s/.test(b.str)) out += ' ';
      }
      out += b.str;
      end = b.x + b.w;
    }
    return out.replace(/\s+/g, ' ').trim();
  }).filter(Boolean);
}

/** PDF.js and its worker, loaded on first use. The "legacy" build runs in older browsers too. */
let libP;
const loadLib = () => (libP ??= Promise.all([
  import('pdfjs-dist/legacy/build/pdf.min.mjs'),
  import('pdfjs-dist/legacy/build/pdf.worker.min.mjs?url'),
]).then(([lib, worker]) => { lib.GlobalWorkerOptions.workerSrc = worker.default; return lib; })
  .catch((e) => { libP = undefined; throw e; }));

/**
 * The text of a PDF, a line of the page a line of text, pages one after another.
 * `lib` is for tests (PDF.js already loaded); the browser leaves it out.
 */
export async function pdfText(data, { maxChars = 200000, maxPages = MAX_PAGES, lib } = {}) {
  const pdfjs = lib ?? await loadLib();
  const task = pdfjs.getDocument({
    data: data instanceof Uint8Array ? data : new Uint8Array(data),
    // Text only, and nothing fetched: no eval, no fonts from the system or the network, no script in the PDF run.
    isEvalSupported: false, useSystemFonts: false, disableFontFace: true, enableXfa: false, stopAtErrors: false,
  });
  try {
    const doc = await task.promise;
    const read = Math.min(doc.numPages, maxPages);
    const out = [];
    let chars = 0;
    for (let n = 1; n <= read && chars < maxChars; n++) {
      const page = await doc.getPage(n);
      const content = await page.getTextContent();
      const lines = linesFromItems(content.items);
      page.cleanup();
      if (!lines.length) continue;
      const text = lines.join('\n');
      out.push(text);
      chars += text.length + 1;
    }
    return { text: out.join('\n').slice(0, maxChars), pages: doc.numPages, read };
  } finally {
    await task.destroy().catch(() => {});
  }
}
