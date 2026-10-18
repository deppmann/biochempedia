import type { IconArt } from '../signaling-icons';

const c = (x: number, y: number, r: number) => `<circle cx="${x}" cy="${y}" r="${r}" />`;
const p = (d: string, extra = '') => `<path d="${d}" ${extra}/>`;
const GF = 'style="fill:var(--ddp-color-secondary)"';
const GS = 'style="stroke:var(--ddp-color-secondary)" fill="none" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"';
const gd = (x: number, y: number, r = 3) => `<circle cx="${x}" cy="${y}" r="${r}" ${GF} />`;
const gp = (d: string) => `<path d="${d}" ${GS} />`;
const ah = (x: number, y: number, dir: 'r' | 'l' | 'u' | 'd', s = 3) =>
  dir === 'r' ? `M${x - s} ${y - s} L${x} ${y} L${x - s} ${y + s}`
  : dir === 'l' ? `M${x + s} ${y - s} L${x} ${y} L${x + s} ${y + s}`
  : dir === 'u' ? `M${x - s} ${y + s} L${x} ${y} L${x + s} ${y + s}`
  : `M${x - s} ${y - s} L${x} ${y} L${x + s} ${y - s}`;
/** A small solid ink dot. */
const dot = (x: number, y: number, r = 1.8) => `<circle cx="${x}" cy="${y}" r="${r}" fill="currentColor" stroke="none" />`;
/** A duplicated chromosome as a small X centred at (x, y). */
const xs = (x: number, y: number, h = 4.5, w = 3.2) =>
  `M${x - w} ${y - h} Q${x + w - 1} ${y} ${x - w} ${y + h} M${x + w} ${y - h} Q${x - w + 1} ${y} ${x + w} ${y + h}`;
/** A blebbing cell: a circle with a lumpy rim. */
const blebs = (cx: number, cy: number, r: number) => {
  const n = 60; let d = '';
  for (let i = 0; i <= n; i++) {
    const t = (i / n) * 2 * Math.PI, rr = r + 2.2 * Math.max(0, Math.sin(5 * t));
    d += `${i ? 'L' : 'M'}${(cx + rr * Math.cos(t)).toFixed(2)} ${(cy + rr * Math.sin(t)).toFixed(2)} `;
  }
  return d + 'Z';
};

export const ICONS: Record<string, IconArt> = {
  'cytoskeleton-dynamics': {
    label: 'A microtubule length trace: slow growth, then a sudden collapse, again and again',
    ink: p('M8 48 V8 M8 48 H50') + p('M10 45 L24 17 L25 42 L40 19 L41 37 L49 23'),
    gold: gd(24, 16, 3.2),
  },
  'molecular-motors': {
    label: 'A motor with two heads stepping hand over hand along a beaded filament, a cargo vesicle carried above on a stalk',
    ink: c(8, 46, 3.2) + c(16, 46, 3.2) + c(24, 46, 3.2) + c(32, 46, 3.2) + c(40, 46, 3.2) + c(48, 46, 3.2) + p('M18 37 L24 30 L31 35 M24 30 L31 22') + c(38.5, 14, 9) + p(`M5 22 H15 ${ah(16, 22, 'r', 2.6)}`),
    gold: `<ellipse cx="17" cy="39.5" rx="4.2" ry="3" ${GF} />` + `<ellipse cx="33" cy="36.5" rx="4.2" ry="3" ${GF} />`,
  },
  'migration-and-cilia': {
    label: 'A cell crawling over a surface, its leading edge pushed forward',
    ink: p('M5 46 H51') + p('M40 22 Q30 18 19 27 Q8 35 7 40 Q7 43 12 43 H40') + p(`M8 11 H24 ${ah(25, 11, 'r', 2.6)}`) + dot(16, 43) + dot(28, 43),
    gold: gp('M40 22 Q52 31 40 43'),
  },
  'cell-cycle-control': {
    label: 'The cell cycle as a loop marked off into phases, with one gold latch where the cell commits to the next phase',
    ink: p('M38.0 10.7 A20 20 0 1 1 20.5 9.5') + p('M17.9 12.8 L20.5 9.5 L16.3 8.9') + p('M28.0 12.0 L28.0 4.0 M43.8 30.8 L51.6 32.2 M20.0 41.9 L16.0 48.8 M13.0 22.5 L5.4 19.8'),
    gold: `<path d="M40.4 21.4 L51.0 15.8" style="stroke:var(--ddp-color-secondary)" fill="none" stroke-width="4.5" stroke-linecap="round" />`,
  },
  'checkpoints': {
    label: 'A path held up at a gate until the step before it is finished',
    ink: p(`M5 28 H17 ${ah(18, 28, 'r', 3)}`) + p(`M34 28 H48 ${ah(49, 28, 'r', 3)}`, 'stroke-dasharray="2 4"'),
    gold: `<rect x="23" y="10" width="6" height="36" rx="3" ${GF} />`,
  },
  'mitosis': {
    label: 'A spindle from two poles, its fibres holding the chromosomes in a line at the middle',
    ink: c(7, 28, 2.6) + c(49, 28, 2.6) + p('M9.5 27 L24 17 M9.5 28 H24 M9.5 29 L24 39 M46.5 27 L32 17 M46.5 28 H32 M46.5 29 L32 39') + p(xs(28, 17) + xs(28, 28) + xs(28, 39)),
    gold: gp('M28 8 V12 M28 44 V48'),
  },
  'cytokinesis': {
    label: 'A cell pinched in two by a ring tightening at its middle',
    ink: p('M28 18 C22 8 5 11 5 28 C5 45 22 48 28 38 C34 48 51 45 51 28 C51 11 34 8 28 18 Z') + c(16, 28, 4) + c(40, 28, 4),
    gold: `<ellipse cx="28" cy="28" rx="3" ry="11" ${GS} />`,
  },
  'cell-death': {
    label: 'A dying, blebbing cell raising a flag that says eat me',
    ink: p(blebs(24, 34, 12)) + c(45, 44, 3) + c(46, 34, 2) + p('M30 22 V7'),
    gold: `<path d="M30 7 L43 10.5 L30 14 Z" ${GF} />`,
  },
  'adhesion-and-ecm': {
    label: 'Two cells gripping each other, sitting on a woven matrix',
    ink: `<rect x="6" y="9" width="19" height="25" rx="5" />` + `<rect x="31" y="9" width="19" height="25" rx="5" />` + p('M5 42 Q16.5 50 28 42 T51 42 M5 48 Q16.5 40 28 48 T51 48'),
    gold: gp('M25 15 H31 M25 21.5 H31 M25 28 H31'),
  },
  'epithelia': {
    label: 'A sheet of tall cells on a base, sealed by junctions at the top',
    ink: `<rect x="6" y="16" width="44" height="28" rx="2" />` + p('M17 16 V44 M28 16 V44 M39 16 V44 M4 49 H52') + p('M9 16 V12 M12.5 16 V12 M20 16 V12 M23.5 16 V12 M31 16 V12 M34.5 16 V12 M42 16 V12 M45.5 16 V12'),
    gold: gd(17, 19, 2.6) + gd(28, 19, 2.6) + gd(39, 19, 2.6),
  },
  'stem-cells': {
    label: 'A gut crypt with its stem cells at the bottom, their daughters moving up the walls',
    ink: p('M10 6 V30 Q10 49 28 49 Q46 49 46 30 V6') + p(`M18 32 V13 ${ah(18, 12, 'u', 2.6)} M38 32 V13 ${ah(38, 12, 'u', 2.6)}`),
    gold: gd(20, 42, 3) + gd(28, 44.5, 3) + gd(36, 42, 3),
  },
  'cell-state-and-disease': {
    label: 'Single cells mapped into clusters, one cluster picked out',
    ink: `<ellipse cx="16" cy="18" rx="10" ry="8" stroke-dasharray="2 3.5" />` + `<ellipse cx="40" cy="20" rx="10" ry="8" stroke-dasharray="2 3.5" />`
      + dot(13, 16) + dot(19, 15) + dot(15, 21) + dot(20, 20) + dot(37, 18) + dot(43, 17) + dot(40, 23) + dot(36, 22),
    gold: gd(23, 38, 2.4) + gd(30, 36, 2.4) + gd(27, 43, 2.4) + gd(34, 42, 2.4) + gd(21, 45, 2.4),
  },
  'cellbio-experimental-design': {
    label: 'A sheet of cells being stretched, one cell caught dividing',
    ink: `<rect x="14" y="13" width="28" height="30" rx="2" />` + p('M28 13 V43 M14 28 H42') + p(`M11 28 H5 ${ah(4, 28, 'l', 3)} M45 28 H51 ${ah(52, 28, 'r', 3)}`),
    gold: gd(32, 20.5, 2.4) + gd(38, 20.5, 2.4),
  },
};
