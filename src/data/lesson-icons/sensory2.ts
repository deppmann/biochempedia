import type { IconArt } from '../signaling-icons';

const c = (x: number, y: number, r: number) => `<circle cx="${x}" cy="${y}" r="${r}" />`;
const p = (d: string, extra = '') => `<path d="${d}" ${extra}/>`;
const GF = 'style="fill:var(--ddp-color-secondary)"';
const GS = 'style="stroke:var(--ddp-color-secondary)" fill="none" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"';
const gd = (x: number, y: number, r = 3) => `<circle cx="${x}" cy="${y}" r="${r}" ${GF} />`;
const gp = (d: string, extra = '') => `<path d="${d}" ${GS} ${extra}/>`;
const dot = (x: number, y: number, r = 2.2) => `<circle cx="${x}" cy="${y}" r="${r}" fill="currentColor" stroke="none" />`;
const ah = (x: number, y: number, dir: 'r' | 'l' | 'u' | 'd', s = 3) =>
  dir === 'r' ? `M${x - s} ${y - s} L${x} ${y} L${x - s} ${y + s}`
  : dir === 'l' ? `M${x + s} ${y - s} L${x} ${y} L${x + s} ${y + s}`
  : dir === 'u' ? `M${x - s} ${y + s} L${x} ${y} L${x + s} ${y + s}`
  : `M${x - s} ${y - s} L${x} ${y} L${x + s} ${y - s}`;
const DASH = 'stroke-dasharray="2 3.5"';
const hex = (x: number, y: number, r: number) =>
  `M${x + r} ${y} L${x + r / 2} ${y + r * 0.866} L${x - r / 2} ${y + r * 0.866} L${x - r} ${y} L${x - r / 2} ${y - r * 0.866} L${x + r / 2} ${y - r * 0.866} Z`;

/* A starburst amacrine cell: eight dendrites that each fork, with output swellings at the tips. */
const rad = (deg: number, r: number, cx = 28, cy = 26) => [cx + r * Math.cos((deg * Math.PI) / 180), cy + r * Math.sin((deg * Math.PI) / 180)].map((v) => +v.toFixed(1));
const starBranch = (deg: number) => {
  const [x0, y0] = rad(deg, 3.6), [x1, y1] = rad(deg, 11), [xa, ya] = rad(deg - 17, 19), [xb, yb] = rad(deg + 17, 19);
  return { d: `M${x0} ${y0} L${x1} ${y1} L${xa} ${ya} M${x1} ${y1} L${xb} ${yb}`, tips: [[xa, ya], [xb, yb]] };
};
/* The cochlea as an Archimedean spiral, unrolled from its apex out to the base. */
const spiralPt = (t: number) => [28 + (1.5 + 1.2 * t) * Math.cos(t + Math.PI), 29 + (1.5 + 1.2 * t) * Math.sin(t + Math.PI)].map((v) => +v.toFixed(1));
const spiral = Array.from({ length: 53 }, (_, i) => spiralPt((i * 5 * Math.PI) / 52));

export const ICONS: Record<string, IconArt> = {
  'vagal-sensory-neurons': {
    label: 'The nodose ganglion: vagal sensory cell bodies sending one branch up to the brainstem and others down to the organs, one picked out in gold',
    ink: `<ellipse cx="28" cy="21" rx="13" ry="8" />` + c(20.5, 21, 2.6) + c(35.5, 21.5, 2.6)
      + p(`M28 13 V4 ${ah(28, 3.5, 'u', 3)}`) + p('M23 28.5 C19 37 13 44 7 52') + p('M33 28.5 C37 37 43 44 49 52'),
    gold: gd(28, 20, 2.8) + gp('M28 29 V45') + gp('M23 48 C23 44 33 44 33 48'),
  },
  'gut-brain-sensing': {
    label: 'A gold sensor cell in the gut lining reaching a foot out to touch a vagal nerve fibre beneath it',
    ink: p('M4 9 V34 M14 9 V34 M42 9 V34 M52 9 V34 M4 34 H18 M38 34 H52')
      + p('M5.5 9 V5 M8.5 9 V5 M11.5 9 V5 M44.5 9 V5 M47.5 9 V5 M50.5 9 V5')
      + p('M3 46 C18 47 30 44 53 44'),
    gold: gp('M26 9 H30 C31 15 35 20 35 27 C35 32 33 34 31 35.5 L38 41.5 L35.5 43.5 L27.5 37 C22 37 19 33 19 27 C19 20 24 15 26 9 Z'),
  },
  'retinal-cell-types': {
    label: 'One retinal cell type tiling the retina in an even mosaic of dendritic fields, with the gold bodies of a second type spaced out between them',
    ink: c(28, 28, 7.5) + c(44, 28, 7.5) + c(12, 28, 7.5) + c(20, 14, 7.5) + c(36, 14, 7.5) + c(20, 42, 7.5) + c(36, 42, 7.5)
      + dot(28, 28, 1.6) + dot(44, 28, 1.6) + dot(12, 28, 1.6) + dot(20, 14, 1.6) + dot(36, 14, 1.6) + dot(20, 42, 1.6) + dot(36, 42, 1.6),
    gold: gd(20, 23.4, 2.2) + gd(36, 23.4, 2.2) + gd(28, 37, 2.2) + gd(12, 37, 2.2) + gd(44, 37, 2.2),
  },
  'direction-selectivity': {
    label: 'A starburst amacrine cell, eight forked dendrites around a small body; motion outward along the gold branch, under the gold arrow, makes that branch release most',
    ink: c(28, 26, 3.6) + [45, 90, 135, 180, 225, 270, 315].map((a) => p(starBranch(a).d) + starBranch(a).tips.map(([x, y]) => dot(x, y, 1.5)).join('')).join(''),
    gold: gp(starBranch(0).d) + starBranch(0).tips.map(([x, y]) => gd(x, y, 1.9)).join('') + gp(`M8 52 H46 ${ah(47, 52, 'r', 3)}`),
  },
  iprgcs: {
    label: 'A ganglion cell that senses light itself, its sparse dendrites catching gold sunlight directly, its axon running to the body clock',
    ink: c(15, 36, 4.5) + p('M12 32.5 L5 24 M18 32 L25 22 L31 18 M25 22 L23 14')
      + p('M19.5 37 C27 39 31 40 35.5 40') + c(44, 40, 8) + p('M44 40 V35 M44 40 L47.5 42'),
    gold: gd(42, 11, 3.4) + gp('M42 3.5 V2 M42 18.5 V20 M34.5 11 H33 M49.5 11 H51 M36.7 5.7 L35.6 4.6 M47.3 5.7 L48.4 4.6')
      + gp('M36.5 16 L32 20', DASH),
  },
  'photoreceptor-adaptation-and-degeneration': {
    label: 'A rod\'s outer segment of stacked discs, the top ones gold where light has bleached the pigment, beside a neighbour fading away',
    ink: `<rect x="14" y="4" width="16" height="28" rx="3" />` + p('M16.5 21 H27.5 M16.5 25.5 H27.5 M16.5 16.5 H27.5')
      + p('M22 32 V35') + `<rect x="16" y="35" width="12" height="10" rx="5" />` + p('M22 45 V51 M18 51 H26')
      + p('M38 10 H48 V30 H38 Z M43 30 V36 M39 40 H47', DASH),
    gold: gp('M16.5 8 H27.5 M16.5 12.2 H27.5'),
  },
  'hair-cell-transduction-channel': {
    label: 'Two stereocilia joined by a tip link; a push toward the taller one pulls open the gold channel at the shorter one\'s tip',
    ink: p('M35 53 V13 C35 8.5 42 8.5 42 13 V53') + p('M17 53 V25 C17 20.5 24 20.5 24 25 V53')
      + p('M22.5 21.2 L35 14') + p(`M33 4 H46 ${ah(47, 4, 'r', 2.8)}`),
    gold: gd(21, 21.6, 2.3) + gp(`M20.5 28 V38 ${ah(20.5, 39, 'd', 2.6)}`),
  },
  'cochlear-amplifier': {
    label: 'An outer hair cell that lengthens and shortens with sound, the gold prestin motors packed in its side wall',
    ink: `<rect x="18" y="11" width="18" height="34" rx="6" />` + p('M21.5 11 L19.5 5 M27 11 V3.5 M32.5 11 L34.5 5')
      + p('M27 45 V51') + p(`M46 13 V43 ${ah(46, 12, 'u', 3)} ${ah(46, 44, 'd', 3)}`),
    gold: gd(18, 17, 1.6) + gd(18, 23, 1.6) + gd(18, 29, 1.6) + gd(18, 35, 1.6) + gd(18, 41, 1.6)
      + gd(36, 17, 1.6) + gd(36, 23, 1.6) + gd(36, 29, 1.6) + gd(36, 35, 1.6) + gd(36, 41, 1.6),
  },
  'hearing-loss-and-repair': {
    label: 'A virus shell carrying a gold replacement gene toward a hair cell, the approach behind gene therapy for inherited deafness',
    ink: `<rect x="7" y="27" width="16" height="25" rx="7" />` + p('M10 27 L9 21 M15 27 V18.5 M20 27 L21 21') + c(15, 42, 3)
      + p(hex(40, 15, 10)) + p('M33 27 L26 32.5 M30.5 32.8 L26 32.5 L27.5 28.3'),
    gold: gp('M34 15 q1.5 -3.5 3 0 t3 0 t3 0 t3 0'),
  },
  'vestibular-system': {
    label: 'An otolith organ: gold crystals weigh down a gel layer that slides when the head tilts, bending the hair bundles beneath it',
    ink: `<rect x="7" y="35" width="12" height="16" rx="5" /><rect x="22" y="35" width="12" height="16" rx="5" /><rect x="37" y="35" width="12" height="16" rx="5" />`
      + p('M11 35 L14 27 M13 35 L16.5 27 M15 35 L19 27 M26 35 L29 27 M28 35 L31.5 27 M30 35 L34 27 M41 35 L44 27 M43 35 L46.5 27 M45 35 L49 27')
      + `<rect x="9" y="18" width="43" height="9" rx="2" />` + p(`M4 8 H15 ${ah(16, 8, 'r', 2.8)}`),
    gold: [[13, 14, 20], [20, 13.5, -25], [27, 14.2, 40], [34, 13.6, -10], [41, 14, 30], [47.5, 13.8, -35]]
      .map(([x, y, a]) => `<rect x="${x - 2}" y="${y - 2}" width="4" height="4" rx="0.7" ${GF} transform="rotate(${a} ${x} ${y})" />`).join(''),
  },
  'olfactory-receptor-choice': {
    label: 'A row of odorant receptor genes on a chromosome, only one of them switched on in each smell neuron, drawn in gold',
    ink: p('M3 36 H53') + `<rect x="5" y="32" width="6" height="8" rx="1.5" /><rect x="13.5" y="32" width="6" height="8" rx="1.5" /><rect x="22" y="32" width="6" height="8" rx="1.5" /><rect x="39" y="32" width="6" height="8" rx="1.5" /><rect x="47.5" y="32" width="6" height="8" rx="1.5" />`
      + c(14, 15, 4.5) + p('M11 11.5 L8 6 M14 10.5 V4.5 M17 11.5 L20 6 M14 19.5 V24'),
    gold: `<rect x="30.5" y="32" width="6" height="8" rx="1.5" ${GF} />` + gp(`M33.5 30 V22 H42 ${ah(43, 22, 'r', 2.8)}`),
  },
  'olfactory-bulb-and-cortex': {
    label: 'Axons from smell neurons that share one receptor converging on a single gold glomerulus, where a mitral cell picks up the signal',
    ink: p('M8 4 C14 13 20 17 24 21 M20 3 C22 11 25 15 26.5 19.5 M36 3 C34 11 31 15 29.5 19.5 M48 4 C42 13 36 17 32 21')
      + c(9, 32, 5) + c(47, 32, 5) + p('M24 48 L28 41 L32 48 Z') + p('M28 41 V33.5 M28 48 V53'),
    gold: `<circle cx="28" cy="26.5" r="7" ${GS} />`,
  },
  'taste-coding': {
    label: 'Three taste cells, each wired to its own line to the brain; the gold one carries sweet and nothing else',
    ink: `<ellipse cx="13" cy="22" rx="4.5" ry="9" /><ellipse cx="43" cy="22" rx="4.5" ry="9" />`
      + p('M13 31 V44 M43 31 V44') + c(13, 48, 3.2) + c(43, 48, 3.2)
      + p('M10 9 L13 4 L16 9 Z') + `<rect x="40" y="4.5" width="6" height="5" rx="1" />`,
    gold: `<ellipse cx="28" cy="22" rx="4.5" ry="9" ${GS} />` + gp('M28 31 V44') + gd(28, 48, 3.2) + gp(hex(28, 7, 3.2)),
  },
  'multisensory-and-prediction': {
    label: 'Signals from the eye and the ear converging on one neuron, whose gold response to both together is larger than to either alone',
    ink: p('M3 14 Q11 6 19 14 Q11 22 3 14 Z') + c(11, 14, 2.6)
      + p('M7 35 C7 29 17 28 17 36 C17 42 11 42 11 47 C11 50 8 51 7 49') + p('M11 36 C11 33.5 14 33.5 14 36.5')
      + p('M20.5 15 L32.5 25 M19 38 L32.5 31') + c(37.5, 28, 5.5),
    gold: gp('M43 28 H45.5 L48 16 L50.5 28 H53'),
  },
  'sensory-prostheses': {
    label: 'The coiled cochlea with the gold contacts of an implant\'s electrode array spaced along its outer turns, the lead running out at the base',
    ink: p(`M${spiral.map(([x, y]) => `${x} ${y}`).join(' L')}`),
    gold: [7, 8, 9, 10, 11, 12, 13].map((t) => gd(...(spiralPt(t * 1.12) as [number, number]), 1.9)).join('')
      + gp(`M${spiralPt(5 * Math.PI).join(' ')} L53 47`),
  },
};
