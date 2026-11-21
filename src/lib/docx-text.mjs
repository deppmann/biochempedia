/* Read the text of a Word file (.docx) in the browser, with nothing but the browser.

   A .docx is a zip; the words are in word/document.xml. This finds that one entry, inflates it
   with the browser's own DecompressionStream, and keeps the text: a paragraph a line, a table row
   a line with " | " between cells. No library is loaded and the file never leaves the device.
   Returns null when the file is not a .docx it can read (old .doc, encrypted, a browser with no
   DecompressionStream): the page then says "paste the text". */

const u16 = (b, o) => b[o] | (b[o + 1] << 8);
const u32 = (b, o) => (b[o] | (b[o + 1] << 8) | (b[o + 2] << 16) | (b[o + 3] << 24)) >>> 0;

/** The bytes of one named entry of a zip, inflated. null when absent or unreadable. */
export async function zipEntry(bytes, name) {
  // The end-of-central-directory record is in the last 64 KB.
  let eocd = -1;
  for (let i = bytes.length - 22; i >= Math.max(0, bytes.length - 65557); i--) if (u32(bytes, i) === 0x06054b50) { eocd = i; break; }
  if (eocd < 0) return null;
  const count = u16(bytes, eocd + 10);
  let p = u32(bytes, eocd + 16);
  const dec = new TextDecoder();
  for (let n = 0; n < count && p + 46 <= bytes.length; n++) {
    if (u32(bytes, p) !== 0x02014b50) return null;
    const method = u16(bytes, p + 10), size = u32(bytes, p + 20), nameLen = u16(bytes, p + 28), extra = u16(bytes, p + 30), comment = u16(bytes, p + 32), local = u32(bytes, p + 42);
    const entry = dec.decode(bytes.subarray(p + 46, p + 46 + nameLen));
    p += 46 + nameLen + extra + comment;
    if (entry !== name) continue;
    if (u32(bytes, local) !== 0x04034b50) return null;
    const start = local + 30 + u16(bytes, local + 26) + u16(bytes, local + 28);
    const data = bytes.subarray(start, start + size);
    if (method === 0) return data;
    if (method !== 8 || typeof DecompressionStream === 'undefined') return null;
    try {
      const stream = new Blob([data]).stream().pipeThrough(new DecompressionStream('deflate-raw'));
      return new Uint8Array(await new Response(stream).arrayBuffer());
    } catch { return null; }
  }
  return null;
}

const ENT = { amp: '&', lt: '<', gt: '>', quot: '"', apos: "'" };

/** word/document.xml to plain lines. */
export function documentXmlToText(xml) {
  return xml
    // Inside a table cell a paragraph end is a space; the cell's end is the separator, the row's end the line.
    .replace(/<w:tc\b[\s\S]*?<\/w:tc>/g, (cell) => `${cell.replace(/<\/w:p>/g, ' ').replace(/<[^>]+>/g, (t) => (/^<w:(tab|br|cr)\b/.test(t) ? ' ' : /^<w:t[ >]|^<\/w:t>/.test(t) ? t : ''))} | `)
    .replace(/<w:tab\b[^>]*\/>/g, '\t')
    .replace(/<w:(br|cr)\b[^>]*\/>/g, '\n')
    .replace(/<\/w:p>/g, '\n')
    .replace(/<\/w:tr>/g, '\n')
    .replace(/<[^>]+>/g, '')
    .replace(/&(amp|lt|gt|quot|apos);/g, (_, k) => ENT[k])
    .replace(/&#(\d+);/g, (_, d) => String.fromCodePoint(Number(d)))
    .replace(/&#x([0-9a-f]+);/gi, (_, h) => String.fromCodePoint(parseInt(h, 16)))
    .replace(/ +\| *\n/g, '\n').replace(/ {2,}/g, ' ')
    .replace(/[ \t]+\n/g, '\n').replace(/\n{3,}/g, '\n\n').trim();
}

/** @param {ArrayBuffer | Uint8Array} file @returns {Promise<string | null>} */
export async function docxText(file) {
  const bytes = file instanceof Uint8Array ? file : new Uint8Array(file);
  const xml = await zipEntry(bytes, 'word/document.xml');
  if (!xml) return null;
  const text = documentXmlToText(new TextDecoder().decode(xml));
  return text || null;
}
