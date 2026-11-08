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
/** A cube: front square at (x, y) of side s, back face offset d up and right. */
const cube = (x: number, y: number, s: number, d: number) =>
  `M${x} ${y} H${x + s} V${y + s} H${x} Z M${x} ${y} L${x + d} ${y - d} H${x + s + d} V${y + s - d} L${x + s} ${y + s} M${x + s} ${y} L${x + s + d} ${y - d}`;
/** A bell-shaped intensity peak centred at cx, from baseline y0 up to height h, width w (sd). */
const bell = (cx: number, y0: number, h: number, w: number, span = 3.2) => {
  let d = '';
  for (let i = 0; i <= 32; i++) {
    const x = cx - span * w + (2 * span * w * i) / 32;
    const y = y0 - h * Math.exp(-((x - cx) ** 2) / (2 * w * w));
    d += `${i ? 'L' : 'M'}${x.toFixed(2)} ${y.toFixed(2)} `;
  }
  return d;
};
/** A point on a circle at angle a (degrees). */
const pt = (cx: number, cy: number, r: number, a: number) =>
  `${(cx + r * Math.cos((a * Math.PI) / 180)).toFixed(2)} ${(cy + r * Math.sin((a * Math.PI) / 180)).toFixed(2)}`;

export const ICONS: Record<string, IconArt> = {
  'measured-eukaryotic-cell': {
    label: 'A small cube and a large cube over a scale bar: how surface and volume change with size',
    ink: p(cube(6, 30, 10, 4)) + p(cube(22, 18, 20, 8)),
    gold: gp('M22 46 H42 M22 43 V49 M42 43 V49'),
  },
  'microscopy-and-images': {
    label: 'Two blurred spots of light overlapping, with the two points that made them',
    ink: p('M5 46 H51') + p(bell(22, 46, 30, 5.2)) + p(bell(34, 46, 30, 5.2)),
    gold: gd(22, 10, 2.8) + gd(34, 10, 2.8),
  },
  'experiments-that-distinguish': {
    label: 'Three bars: normal, lost when a protein is removed, and restored when it is put back',
    ink: p('M7 8 V47 H50') + `<rect x="12" y="14" width="9" height="33" />` + `<rect x="25" y="37" width="9" height="10" />` + p('M27 25 L32 30 M32 25 L27 30'),
    gold: `<rect x="38" y="16" width="9" height="31" ${GF} />`,
  },
  'membrane-organization-topology': {
    label: 'A membrane whose two faces carry different lipids, with one lipid being flipped across',
    ink: p('M5 24 H40 M5 32 H40') + dot(9, 19.5, 2.4) + dot(17, 19.5, 2.4) + dot(25, 19.5, 2.4) + dot(33, 19.5, 2.4)
      + c(9, 36.5, 2.2) + c(17, 36.5, 2.2) + c(25, 36.5, 2.2) + c(33, 36.5, 2.2),
    gold: gp(`M42 37 C52 36 52 20 43 19.5 M46 16.5 L43 19.5 L46 22.5`),
  },
  'membrane-transport': {
    label: 'A pump in a membrane moving molecules uphill, from the side with few to the side with many',
    ink: p('M25 6 V21 M31 6 V21 M25 35 V50 M31 35 V50') + c(28, 28, 7)
      + dot(10, 16) + dot(13, 40) + dot(38, 12) + dot(45, 18) + dot(40, 40) + dot(47, 44) + dot(44, 31),
    gold: gp(`M8 28 H19 M37 28 H46 ${ah(47, 28, 'r', 3.5)}`),
  },
  'organelles-as-environments': {
    label: 'A cell holding separate compartments, one of them filled with acid',
    ink: `<rect x="5" y="6" width="46" height="44" rx="14" />` + c(19, 21, 7) + `<ellipse cx="17" cy="39" rx="6" ry="4" />`,
    gold: `<circle cx="36" cy="34" r="9" ${GS} />` + gd(33, 31, 1.7) + gd(39, 31, 1.7) + gd(33, 37.5, 1.7) + gd(39, 37.5, 1.7),
  },
  'protein-sorting': {
    label: 'A new protein with an address at its front end, sent down one of two routes to its compartment',
    ink: p(`M17 28 H25 L35 16 ${ah(36.5, 14.5, 'r', 0)} M25 28 L35 40`) + p('M32.5 14.2 L36.6 14.2 L36.6 18.3') + p('M32.5 41.8 L36.6 41.8 L36.6 37.7')
      + c(45, 11, 6) + c(45, 11, 3) + `<rect x="39" y="39" width="12" height="10" rx="3" />`,
    gold: `<path d="M6 28 H15" style="stroke:var(--ddp-color-secondary)" fill="none" stroke-width="4" stroke-linecap="round" />`,
  },
  'nuclear-transport': {
    label: 'A double nuclear envelope with two pores: cargo going in through one, RNA coming out through the other',
    ink: p('M24 5 V13 M24 21 V35 M24 43 V51 M31 5 V13 M31 21 V35 M31 43 V51 M24 13 H31 M24 21 H31 M24 35 H31 M24 43 H31')
      + p(`M6 17 H45 ${ah(47, 17, 'r', 3)}`) + p(`M50 39 H11 ${ah(9, 39, 'l', 3)}`),
    gold: gd(14, 17, 3.4) + gd(42, 39, 3),
  },
  'quality-control-and-autophagy': {
    label: 'A cup of double membrane closing around a worn-out mitochondrion',
    ink: p(`M${pt(28, 30, 20, -55)} A20 20 0 1 1 ${pt(28, 30, 20, -125)} L${pt(28, 30, 15, -125)} A15 15 0 1 0 ${pt(28, 30, 15, -55)} Z`),
    gold: `<ellipse cx="28" cy="31" rx="9" ry="5.5" ${GS} />` + gp('M22 31 L25 28 L28 34 L31 28 L34 31'),
  },
  'nuclear-architecture-condensates': {
    label: 'A nucleus divided into chromosome territories, with one droplet that has no membrane',
    ink: c(28, 28, 21) + p('M8 24 Q19 27 21 8') + p('M8.5 34 Q22 32 28 49') + p('M21 26 Q30 22 44 12') ,
    gold: gd(36, 34, 5.5),
  },
  'vesicle-traffic': {
    label: 'A coated vesicle leaving one membrane and zipping into another',
    ink: p('M6 6 Q10 16 10 21 A7 7 0 0 1 10 35 Q10 40 6 50') + p('M15.5 23 L18.5 21 M17 28 H20.5 M15.5 33 L18.5 35') + c(29, 28, 6.5)
      + p('M45 6 V50 M50 6 V50'),
    gold: gp('M35.5 26 Q40 34 45 26 M35.5 30 Q40 22 45 30'),
  },
  'secretory-pathway': {
    label: 'A Golgi stack, with a vesicle leaving it toward the cell surface',
    ink: p('M14 41 Q28 47 42 41') + p('M11 34 Q28 41 45 34') + p('M11 27 Q28 34 45 27') + p('M14 20 Q28 27 42 20')
      + p(`M6 48 V11 ${ah(6, 9, 'u', 3)}`),
    gold: gd(28, 11, 4),
  },
  'endocytosis': {
    label: 'A coated pit drawing in a particle while its receptor is sent back to the surface',
    ink: p('M5 12 H17 Q20 12 20 16 V24 A8 8 0 0 0 36 24 V16 Q36 12 39 12 H51')
      + p('M15 22 H11 M15 29 L11.5 31 M19.5 36 L17 39.5 M28 38 V42 M36.5 36 L39 39.5 M41 29 L44.5 31 M41 22 H45')
      + p(`M30 47 C44 49 50 38 47 22 ${ah(47, 19, 'u', 3)}`),
    gold: gd(28, 23, 4),
  },
};

export const COURSE: Record<string, IconArt> = {
  'course:cell-biology': {
    label: 'A eukaryotic cell with its nucleus and one vesicle',
    ink: `<ellipse cx="28" cy="28" rx="23" ry="19" />` + c(21, 28, 9) + dot(19, 26, 2.4) + `<ellipse cx="38" cy="38" rx="5" ry="3" />`,
    gold: gd(38, 19, 4),
  },
};

