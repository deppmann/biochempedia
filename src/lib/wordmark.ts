/* The STEMhop wordmark as markup, in one place (2026-11-15). "STEM" in the site teal, "hop" in navy,
   and the O of "hop" is Hex: the hexagon body, its three gold bonds and its face, drawn from
   src/components/Hex.astro with strokes weighted for type sizes. Below 24 px the heavier Hex-O is
   used (the 32 px favicon drawing), so the face still reads.

   Used by src/components/Wordmark.astro (header, homepage) and by the footer, which belongs to the
   shared brand package and only takes strings, so the markup has to exist as a string as well.
   The whole mark is one image to assistive technology, named "STEMhop". */

export type WordmarkTone = 'page' | 'onDark';

export interface WordmarkOptions {
  /** Font size: a number of px (below 24 picks the heavier Hex-O) or any CSS length, e.g. a clamp().
   *  Leave it out to size the mark from a stylesheet (the header changes size with the screen). */
  size?: number | string;
  /** Force the heavier Hex-O (for a mark sized by a stylesheet to below 24 px). */
  heavy?: boolean;
  /** Colours: 'page' follows light and dark mode; 'onDark' is for the navy footer and the share image. */
  tone?: WordmarkTone;
  /** Draw the dashed hop arc over the h (the homepage hero only). */
  hop?: boolean;
  /** Accessible name. Pass '' when the mark sits inside a link or heading that names it already. */
  label?: string;
  /** Extra class names on the outer span. */
  className?: string;
}

/** The Hex-O at display and header sizes. */
const HEXO = {
  viewBox: '12.6 8.2 38.8 43.6',
  body: 3.4,
  bonds: 'M32 15.4 L44.6 22.7 M44.6 37.3 L32 44.6 M19.4 37.3 L19.4 22.7',
  bondW: 2.4,
  eyes: [26.5, 37.5, 28, 2.7] as const,
  smile: 'M28 34.3 Q32 38.6 36 34.3',
  smileW: 2.4,
};
/** The heavier Hex-O for small sizes (the favicon's 32 px drawing). */
const HEXO_HEAVY = {
  viewBox: '11.5 7.5 41 45',
  body: 4.2,
  bonds: 'M32 16.2 L43.8 23 M43.8 37 L32 43.8 M20.2 37 L20.2 23',
  bondW: 3,
  eyes: [26.3, 37.7, 28.2, 3.2] as const,
  smile: 'M27.6 34.6 Q32 39 36.4 34.6',
  smileW: 3,
};
const HEX = 'M32 10 L49.3 20 L49.3 40 L32 50 L14.7 40 L14.7 20 Z';

export function hexOSvg(heavy = false): string {
  const h = heavy ? HEXO_HEAVY : HEXO;
  const [lx, rx, ey, r] = h.eyes;
  return (
    `<svg class="wm-o" viewBox="${h.viewBox}" aria-hidden="true" focusable="false">` +
    `<path class="wm-o-body" d="${HEX}" stroke-width="${h.body}"/>` +
    `<path class="wm-o-bonds" d="${h.bonds}" stroke-width="${h.bondW}"/>` +
    `<g class="wm-o-eyes"><circle cx="${lx}" cy="${ey}" r="${r}"/><circle cx="${rx}" cy="${ey}" r="${r}"/></g>` +
    `<path class="wm-o-smile" d="${h.smile}" stroke-width="${h.smileW}"/>` +
    `</svg>`
  );
}

const HOP_ARC = '<svg class="wm-arc" viewBox="0 0 107 42" aria-hidden="true" focusable="false"><path class="hop-arc" d="M3 30 Q42 -50 95 50"/></svg>';

const esc = (s: string) => s.replace(/&/g, '&amp;').replace(/"/g, '&quot;').replace(/</g, '&lt;');

export function wordmarkHtml({ size, heavy, tone = 'page', hop = false, label = 'STEMhop', className = '' }: WordmarkOptions = {}): string {
  const cls = ['wm', tone === 'onDark' ? 'wm-on-dark' : '', className].filter(Boolean).join(' ');
  const style = size === undefined ? '' : ` style="font-size:${typeof size === 'number' ? `${size}px` : esc(size)}"`;
  const a11y = label ? ` role="img" aria-label="${esc(label)}"` : ' aria-hidden="true"';
  return (
    `<span class="${cls}"${style}${a11y}>` +
    `<span class="wm-stem">STEM</span>` +
    `<span class="wm-hop">${hop ? HOP_ARC : ''}h${hexOSvg(heavy ?? (typeof size === 'number' && size < 24))}p</span>` +
    `</span>`
  );
}
