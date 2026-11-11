/**
 * skim — the "skim version" of a lesson, worked out at deploy time (2026-11-11).
 *
 * A long lesson carries its take-home messages in a few figures and their captions (figure
 * philosophy: the caption is the take-home). A student revising the night before wants only those.
 * skimOf() reads the lesson's MDX body in order and returns each main (##) section with the figures
 * that sit in it: src, alt, caption and the callout words (keyItems). The lesson page links the
 * result, and /lessons/<slug>/skim/ renders it as a plain page that works on phones and with
 * JavaScript off.
 *
 * Section headings come from Astro's render() headings (depth 2, in order), so the text and anchor
 * match the full lesson exactly. Figures above the first ## heading go in a section with no heading.
 */

export interface SkimFigure { src: string; alt: string; caption: string; keyItems: string[]; width: number; height: number }
export interface SkimSection { text: string | null; slug: string | null; figures: SkimFigure[] }
export interface Skim { sections: SkimSection[]; figureCount: number; words: number; minutes: number }

interface Heading { depth: number; slug: string; text: string }

const FIG_OPEN = /<(LessonFigure|ScaffoldFigure)\b/;

/** Parse one figure tag's props. Lesson MDX writes them as name="..." strings, numbers as
 *  name={1200}, and keyItems={["a", "b"]}. */
function parseFigure(tag: string): SkimFigure | null {
  const str = (name: string) => (new RegExp(`\\b${name}="([^"]*)"`).exec(tag) || [])[1] ?? '';
  const num = (name: string, d: number) => Number((new RegExp(`\\b${name}=\\{(\\d+)\\}`).exec(tag) || [])[1] ?? d);
  const src = str('src');
  if (!src) return null;
  let keyItems: string[] = [];
  const k = /\bkeyItems=\{(\[[\s\S]*?\])\}/.exec(tag);
  if (k) {
    try { keyItems = (JSON.parse(k[1]) as unknown[]).filter((x): x is string => typeof x === 'string'); }
    catch { keyItems = [...k[1].matchAll(/"([^"]*)"/g)].map((m) => m[1]); }
  }
  return { src, alt: str('alt'), caption: str('caption'), keyItems, width: num('width', 1200), height: num('height', 800) };
}

export function skimOf(body: string, headings: Heading[]): Skim {
  const h2 = headings.filter((h) => h.depth === 2);
  const sections: SkimSection[] = [{ text: null, slug: null, figures: [] }];
  let h2i = 0;
  let fence = false;
  const lines = body.split('\n');
  for (let i = 0; i < lines.length; i++) {
    const line = lines[i];
    if (/^\s*(```|~~~)/.test(line)) { fence = !fence; continue; }
    if (fence) continue;
    const m = /^##\s+(.+?)\s*#*\s*$/.exec(line);
    if (m) {
      const h = h2[h2i++];
      sections.push({ text: h?.text ?? m[1].replace(/[*_`]/g, ''), slug: h?.slug ?? null, figures: [] });
      continue;
    }
    if (FIG_OPEN.test(line)) {
      // A figure tag can run over several lines; read on to its closing "/>".
      let tag = line.slice(line.search(FIG_OPEN));
      while (!/\/>/.test(tag) && i + 1 < lines.length) tag += '\n' + lines[++i];
      const f = parseFigure(tag);
      if (f) sections[sections.length - 1].figures.push(f);
    }
  }
  const out = sections[0].figures.length ? sections : sections.slice(1);
  const figureCount = out.reduce((n, s) => n + s.figures.length, 0);
  const words = out.reduce((n, s) => n + (s.text ?? '').split(/\s+/).length
    + s.figures.reduce((w, f) => w + f.caption.split(/\s+/).length + f.keyItems.join(' ').split(/\s+/).length, 0), 0);
  return { sections: out, figureCount, words, minutes: Math.max(1, Math.round(words / 200)) };
}
