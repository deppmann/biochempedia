import type { IconArt } from '../signaling-icons';

const c = (x: number, y: number, r: number, extra = '') => `<circle cx="${x}" cy="${y}" r="${r}" ${extra}/>`;
const p = (d: string, extra = '') => `<path d="${d}" ${extra}/>`;
const GF = 'style="fill:var(--ddp-color-secondary)"';
const GS = 'style="stroke:var(--ddp-color-secondary)" fill="none" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"';
const gd = (x: number, y: number, r = 3) => `<circle cx="${x}" cy="${y}" r="${r}" ${GF} />`;
const gp = (d: string, extra = '') => `<path d="${d}" ${GS} ${extra}/>`;
const dot = (x: number, y: number, r = 1.7) => `<circle cx="${x}" cy="${y}" r="${r}" fill="currentColor" stroke="none" />`;
const ah = (x: number, y: number, dir: 'r' | 'l' | 'u' | 'd', s = 3) =>
  dir === 'r' ? `M${x - s} ${y - s} L${x} ${y} L${x - s} ${y + s}`
  : dir === 'l' ? `M${x + s} ${y - s} L${x} ${y} L${x + s} ${y + s}`
  : dir === 'u' ? `M${x - s} ${y + s} L${x} ${y} L${x + s} ${y + s}`
  : `M${x - s} ${y - s} L${x} ${y} L${x + s} ${y - s}`;
const rect = (x: number, y: number, w: number, h: number, r = 2) => `<rect x="${x}" y="${y}" width="${w}" height="${h}" rx="${r}" />`;
const drop = (x: number, y: number, r: number) =>
  `M${x} ${y} Q${x + r} ${y + r * 1.35} ${x + r} ${y + r * 1.9} A${r} ${r} 0 0 1 ${x - r} ${y + r * 1.9} Q${x - r} ${y + r * 1.35} ${x} ${y} Z`;
const pol = (cx: number, cy: number, r: number, a: number) => {
  const t = (a * Math.PI) / 180;
  return [+(cx + r * Math.cos(t)).toFixed(1), +(cy + r * Math.sin(t)).toFixed(1)] as const;
};
/** A circular arc from angle a0 to a1 (clockwise on screen) ending in an arrowhead. */
const arcArrow = (cx: number, cy: number, r: number, a0: number, a1: number, s = 3.2) => {
  const [x0, y0] = pol(cx, cy, r, a0);
  const [x1, y1] = pol(cx, cy, r, a1);
  const d = ((a1 + 90) * Math.PI) / 180; // travel direction at the tip
  const back = (turn: number) => [x1 - s * Math.cos(d + turn), y1 - s * Math.sin(d + turn)].map((v) => +v.toFixed(1));
  const [lx, ly] = back(0.55);
  const [rx, ry] = back(-0.55);
  return `M${x0} ${y0} A${r} ${r} 0 ${a1 - a0 > 180 ? 1 : 0} 1 ${x1} ${y1} M${lx} ${ly} L${x1} ${y1} L${rx} ${ry}`;
};

export const ICONS: Record<string, IconArt> = {
  'lung-mechanics-surfactant': {
    label: 'A pair of lungs with the windpipe above, and a single gold air sac drawn larger beside them',
    ink: p('M21 3 V13 M21 13 L15 19 M21 13 L27 19')
      + p('M19 11 C12 12 5 22 4 32 C4 38 10 40 15 38 C19 37 20 33 20 29 Z')
      + p('M23 11 C30 12 37 22 38 32 C38 38 33 40 29 39 C25 38 23 36 23 33 C23 30 25 28 23 25 Z')
      + p('M35 39 L38 42', 'stroke-dasharray="1.5 3"'),
    gold: `<circle cx="45" cy="46" r="8" style="stroke:var(--ddp-color-secondary)" fill="none" stroke-width="2" />` + gp('M40.5 44 Q41 41.5 43.5 40.5'),
  },
  'ventilation-perfusion': {
    label: 'An air sac with an arrow of air breathing in on one side and, beside it, a curved capillary carrying a gold arrow of blood flow',
    ink: c(22, 33, 12) + p('M19 21 V6 M25 21 V6') + p(`M22 4 V15 ${ah(22, 16, 'd', 3)}`)
      + p('M36 21 A17 17 0 0 1 36 45 M41 16.5 A23 23 0 0 1 41 49.5 M36 21 L41 16.5 M36 45 L41 49.5'),
    gold: gp(`M38.5 19 A20 20 0 0 1 38.5 47 ${ah(38.5, 47.4, 'd', 2.8)}`),
  },
  'control-of-breathing': {
    label: 'A high mountain peak with a gold arrow of breath rising to thin air beside it',
    ink: p('M3 51 L19 22 L26 34 L35 13 L53 51 Z') + p('M30.5 22 L35 28 L39 22') + p('M12 34 L19 29 L22 33')
      + p('M6 8 q3 -3 6 0 t6 0 M6 14 q3 -3 6 0 t6 0'),
    gold: gp(`M46 30 V10 ${ah(46, 9.5, 'u', 3)}`),
  },
  'glomerular-filtration': {
    label: 'A cup-shaped capsule round a gold tuft of looping capillaries, with a vessel arrow entering at the top and another leaving at the bottom',
    ink: p('M15.7 18 A20 20 0 1 1 15.7 38') + p(`M3 21 H18 ${ah(19, 21, 'r', 3)}`) + p(`M19 36 H3 ${ah(2.5, 36, 'l', 3)}`),
    gold: gp('M19 24 C24 17 36 17 38 24 C40 31 28 28 30 34 C32 40 44 38 43 30 C42 25 37 24 33 26'),
  },
  'tubular-transport-diuretics': {
    label: 'A kidney tubule cut along its length, with arrows crossing the wall out of the channel and one gold arrow crossing into it',
    ink: p('M3 16 H53 M3 22 H53 M3 34 H53 M3 40 H53') + p(`M14 28 V8 ${ah(14, 8, 'u', 3)}`) + p(`M26 28 V8 ${ah(26, 8, 'u', 3)}`) + p(`M4 28 H8 M49 28 H53`),
    gold: gp(`M42 50 V30 ${ah(42, 29.5, 'u', 3)}`),
  },
  'water-sodium-potassium': {
    label: 'A balance with a Na plus tag under one pan and a K plus tag under the other, and a gold water drop above the post',
    ink: p('M28 14 V48 M20 50 H36 M8 17 H48') + p('M8 17 L3 31 M8 17 L13 31 M48 17 L43 31 M48 17 L53 31') + p('M2 31 Q8 37 14 31 Z M42 31 Q48 37 54 31 Z')
      + `<text x="8" y="51" text-anchor="middle" font-family="Georgia, 'Times New Roman', serif" font-size="10" font-weight="700" fill="currentColor" stroke="none">Na<tspan dy="-4" font-size="7">+</tspan></text>`
      + `<text x="48" y="51" text-anchor="middle" font-family="Georgia, 'Times New Roman', serif" font-size="10" font-weight="700" fill="currentColor" stroke="none">K<tspan dy="-4" font-size="7">+</tspan></text>`,
    gold: `<path d="${drop(28, 1.5, 4)}" ${GF} />`,
  },
  'acid-base-balance': {
    label: 'A small balance above a pH scale bar, with a gold pointer resting near the middle of the scale',
    ink: p('M28 4 V20 M22 21 H34 M9 8 H47') + p('M9 8 L5 17 M9 8 L13 17 M47 8 L43 17 M47 8 L51 17') + p('M4 17 Q9 22 14 17 M42 17 Q47 22 52 17')
      + rect(4, 38, 48, 11, 3) + p('M12 38 V43 M20 38 V43 M28 38 V43 M36 38 V43 M44 38 V43'),
    gold: `<path d="M24 26 H32 L28 35 Z" ${GF} />`,
  },
  'gut-motility-secretion': {
    label: 'A length of gut with a ring of contraction squeezing it and a gold arrow showing the wave moving the contents on',
    ink: p('M3 14 H14 C20 14 20 22 26 22 C32 22 32 14 38 14 H53') + p('M3 38 H14 C20 38 20 30 26 30 C32 30 32 38 38 38 H53') + c(44, 26, 5.5),
    gold: gp(`M8 48 H46 ${ah(47, 48, 'r', 3.2)}`),
  },
  'absorption-and-liver': {
    label: 'A liver above a loop of gut, with a gold portal vein arrow carrying absorbed food from the gut up to it',
    ink: p('M3 22 C3 12 13 6 25 6 C39 6 50 10 53 19 C53 23 45 23 37 27 C31 30 29 38 19 38 C9 38 3 32 3 22 Z')
      + p('M4 48 q4 -7 8 0 t8 0 t8 0 t8 0 t8 0 t8 0'),
    gold: gp(`M36 46 C36 42 35 38 33 35 ${ah(32.8, 33.5, 'u', 3.2)}`),
  },
  'lymphoid-organs-immune-traffic': {
    label: 'A bean-shaped lymph node with two vessels arriving at the top and one gold vessel leaving at its notch',
    ink: p('M6 28 C6 15 18 11 29 11 C42 11 51 17 51 27 C51 35 45 39 39 37 C35 36 33 33 28 33 C23 33 21 37 17 38 C10 39 6 35 6 28 Z')
      + p(`M15 3 V10 ${ah(15, 10.5, 'd', 2.6)} M26 3 V8 ${ah(26, 8.5, 'd', 2.6)}`) + dot(17, 24) + dot(24, 20) + dot(32, 22) + dot(40, 25) + dot(28, 26.5),
    gold: gp(`M28 33 V52 ${ah(28, 52.5, 'd', 3.2)}`),
  },
  'skin-and-human-heat': {
    label: 'A block of skin in three layers with a sweat gland duct reaching the surface, a gold sweat drop above it and wavy lines of heat rising',
    ink: rect(4, 20, 48, 33, 2) + p('M4 27 H52 M4 40 H52')
      + p('M38 40 C33 37 42 34 36 31 C34 29 38 28 38 20') + `<ellipse cx="38" cy="45" rx="4" ry="3" />` + dot(10, 46) + dot(18, 48) + dot(26, 46)
      + p('M10 16 q-2 -2.4 0 -4.8 q2 -2.4 0 -4.8 M18 16 q-2 -2.4 0 -4.8 q2 -2.4 0 -4.8 M26 16 q-2 -2.4 0 -4.8 q2 -2.4 0 -4.8'),
    gold: `<path d="${drop(38, 2.5, 3.6)}" ${GF} />`,
  },
  'sexual-differentiation-testis': {
    label: 'A small gonad with two ducts leaving it, one gold and kept, the other drawn in broken fading dashes',
    ink: `<ellipse cx="28" cy="9" rx="13" ry="6.5" />` + dot(24, 9, 1.4) + dot(30, 8, 1.4) + dot(34, 10, 1.4) + p('M35 15 C37 20 36 24 36 28') + p('M37 32 C38 36 36.5 38 37 41', 'opacity="0.75"') + p('M37.5 45 L37.5 47', 'opacity="0.5"') + p('M37.5 51 L37.5 52', 'opacity="0.35"'),
    gold: gp('M21 15 C16 24 24 31 19 39 C16 45 21 49 19 54'),
  },
  'ovarian-cycle-fertility': {
    label: 'Two curved arrows chasing each other round a follicle that holds a gold egg',
    ink: c(28, 28, 8) + p(arcArrow(28, 28, 21, 205, 295) + ' ' + arcArrow(28, 28, 21, 25, 115)),
    gold: gd(30, 30, 3.2),
  },
  'pregnancy-birth-lactation': {
    label: 'A flat disc of placenta with fine villi beneath it and a gold umbilical cord winding up from its centre',
    ink: p('M4 38 C4 29 15 27 28 27 C41 27 52 29 52 38 C52 43 41 46 28 46 C15 46 4 43 4 38 Z')
      + p('M12 46 V52 M12 49 L9 52 M20 47 V54 M20 51 L17 54 M28 47 V54 M28 51 L25 54 M36 47 V54 M36 51 L33 54 M44 46 V52 M44 49 L47 52'),
    gold: gp('M28 27 C20 22 36 17 28 12 C22 8 31 6 28 2'),
  },
  'exercise-physiology': {
    label: 'A running figure drawn in a few strokes, with a gold heart-rate line beneath its feet',
    ink: c(32, 7, 3.6) + p('M30 13 L25 29') + p('M29.5 16 L21 22 L16 18 M29.5 16 L38 22 L43 17')
      + p('M25 29 L34 34 L36 43 M25 29 L18 37 L10 35'),
    gold: gp('M3 52 H14 L17 47 L21 56 L24 52 H33 L36 49 L39 55 L41 52 H53'),
  },
};
