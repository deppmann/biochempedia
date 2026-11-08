import type { IconArt } from '../signaling-icons';

const c = (x: number, y: number, r: number) => `<circle cx="${x}" cy="${y}" r="${r}" />`;
const p = (d: string, extra = '') => `<path d="${d}" ${extra}/>`;
const GF = 'style="fill:var(--ddp-color-secondary)"';
const GS = 'style="stroke:var(--ddp-color-secondary)" fill="none" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"';
const gd = (x: number, y: number, r = 3) => `<circle cx="${x}" cy="${y}" r="${r}" ${GF} />`;
const gp = (d: string, extra = '') => `<path d="${d}" ${GS} ${extra}/>`;
const ah = (x: number, y: number, dir: 'r' | 'l' | 'u' | 'd', s = 3) =>
  dir === 'r' ? `M${x - s} ${y - s} L${x} ${y} L${x - s} ${y + s}`
  : dir === 'l' ? `M${x + s} ${y - s} L${x} ${y} L${x + s} ${y + s}`
  : dir === 'u' ? `M${x - s} ${y + s} L${x} ${y} L${x + s} ${y + s}`
  : `M${x - s} ${y - s} L${x} ${y} L${x + s} ${y - s}`;

export const ICONS: Record<string, IconArt> = {
  'reelin-and-reeler': {
    label: 'A young neuron climbing a radial fibre toward a band of Reelin under the brain surface',
    ink: p('M6 8 H50') + p('M14 13 V50') + c(26, 40, 5) + p(`M26 35 V22 ${ah(26, 21, 'u', 3)}`) + c(40, 26, 4.5) + p('M40 21.5 V16'),
    gold: gd(22, 13, 2.4) + gd(30, 13, 2.4) + gd(38, 11.5, 2.4) + gd(46, 13, 2.4),
  },
  'tangential-migration': {
    label: 'A section of the forebrain; cells born at its base travel sideways into the cortex',
    ink: p('M6 46 Q6 8 28 8 Q50 8 50 46') + p('M14 46 Q14 17 28 17 Q42 17 42 46') + p('M20 46 Q28 34 36 46'),
    gold: gd(28, 38, 3.2) + gp(`M25 36 Q18 32 18 25 Q18 15 26.5 14 M24.6 12.1 L26.5 14 L24.6 15.9`),
  },
  'neural-crest': {
    label: 'The folded neural plate, with cells leaving from its two crests',
    ink: p('M6 22 H12 Q16 22 19 30 Q28 52 37 30 Q40 22 44 22 H50'),
    gold: gd(15, 16, 3) + gd(41, 16, 3) + gd(9, 12, 2.2) + gd(47, 12, 2.2),
  },
  'neuronal-polarity': {
    label: 'A neuron with several short dendrites and one long axon',
    ink: c(28, 18, 6) + p('M23 14 L15 8 M19 11 L13 13 M33 14 L41 8 M37 11 L43 14 M28 12 V5 M23 21 L14 26 M33 21 L42 26'),
    gold: gp('M28 24 V50 M28 50 L23 52 M28 50 L33 52') + `<rect x="25.5" y="27" width="5" height="7" rx="1.5" ${GF} />`,
  },
  'guidance-cues-and-pioneers': {
    label: 'A pioneer axon with its growth cone leading the way past guidepost cells, a later axon following along it',
    ink: c(10, 44, 4.5) + p('M13.5 41 Q22 30 30 26 Q38 22 41 14 M41 14 L38 8 M41 14 L44 8 M41 14 L47 12') + `<circle cx="20" cy="27" r="2.4" fill="currentColor" />` + `<circle cx="42" cy="28" r="2.4" fill="currentColor" />`,
    gold: gp('M18 49 Q25 36 32 31 Q40 26.5 43.5 19'),
  },
  'netrin-and-dcc': {
    label: 'A cue released from the floor of the spinal cord: one axon grows toward it, another away',
    ink: p(`M12 6 Q12 22 16 34 ${ah(16.6, 36, 'd', 3)}`) + p(`M36 34 Q40 22 42 9 ${ah(42.2, 7, 'u', 3)}`) + p('M14 44 Q28 38 42 44', 'stroke-dasharray="1.5 3.6"'),
    gold: `<rect x="10" y="46" width="36" height="5" rx="2.5" ${GF} />`,
  },
  'crossing-the-midline': {
    label: 'Two axons at the midline: one crosses once and turns up, the other never crosses',
    ink: p(`M6 44 H34 Q42 44 42 34 V12 ${ah(42, 10, 'u', 3)}`) + p(`M6 32 H12 Q18 32 18 24 V12 ${ah(18, 10, 'u', 3)}`),
    gold: gp('M28 6 V50', 'stroke-dasharray="4 4"'),
  },
  'semaphorins': {
    label: 'A growth cone turned back by a repellent cue',
    ink: p(`M14 50 V28 Q14 14 25 14 Q33 14 32 24 ${ah(31.8, 27, 'd', 3)}`) + p('M28 14 L30 9 M23 14.5 L22 9'),
    gold: gd(43, 30, 4) + gp('M43 19 V22 M43 38 V41 M34 30 H37 M49 30 H52'),
  },
  'topographic-maps': {
    label: 'Points on the eye wired in the same order onto the brain, along a graded field',
    ink: p('M14 8 Q4 28 14 48') + p('M12 14 L42 12 M9 28 L42 28 M12 42 L42 44') + p('M42 8 V48'),
    gold: `<path d="M46 8 L50 8 L50 48 L46 48 Z" ${GF} opacity="0.35" />` + `<path d="M46 8 L50 8 L46 48 Z" ${GF} />`,
  },
  'partners-layers-self-avoidance': {
    label: 'Stacked layers, each axon branching in its own layer',
    ink: p('M6 12 H50 M6 24 H50 M6 36 H50', 'stroke-dasharray="1.5 3.6"') + p('M16 50 V36 M10 36 L16 36 L22 36 M10 36 Q13 32 16 36 M22 36 Q19 32 16 36'),
    gold: gp('M38 50 V24 M30 24 H46 M30 24 Q34 18 38 24 M46 24 Q42 18 38 24'),
  },
  'naturally-occurring-death': {
    label: 'A crowd of young neurons, several of them breaking up',
    ink: c(11, 16, 5) + c(28, 16, 5) + c(45, 40, 5) + c(11, 40, 5) + c(28, 40, 5),
    gold: gd(42, 13, 2.2) + gd(48, 15, 1.7) + gd(44, 20, 1.8) + gd(25, 26.5, 1.5) + gd(31, 28.5, 1.8),
  },
  'neurotrophic-hypothesis': {
    label: 'A drop of growth factor added to a neuron, which sends out fibres',
    ink: p('M24 5 H32 M25 5 V18 L28 23 L31 18 V5') + c(28, 40, 5) + p('M23 40 H10 M33 40 H46 M24.5 43.5 L15 51 M31.5 43.5 L41 51 M24.5 36.5 L17 31 M31.5 36.5 L39 31'),
    gold: `<path d="M28 26 Q25.4 29.6 25.4 31.2 A2.6 2.6 0 0 0 30.6 31.2 Q30.6 29.6 28 26 Z" ${GF} />`,
  },
  'trk-and-p75': {
    label: 'Two receptors in one membrane: a paired Trk receptor and the single p75 receptor with a tail',
    ink: p('M6 22 H50 M6 27 H50') + p('M13 14 V40 M20 14 V40') + p('M38 14 V38') + c(38, 43, 4.5),
    gold: gd(16.5, 9, 3.4) + gd(38, 9, 3.4),
  },
  'death-machinery-in-neurons': {
    label: 'A mitochondrion releasing cytochrome c',
    ink: `<rect x="6" y="20" width="36" height="20" rx="10" />` + p('M13 34 V27 Q16 24 19 27 V34 M19 34 Q22 37 25 34 V27 Q28 24 31 27 V34 M31 34 Q34 37 37 34 V28'),
    gold: gd(44, 15, 2.6) + gd(49, 9, 2.2) + gd(48, 21, 2) + gp('M40 21 L42.5 18'),
  },
  'competition-for-targets': {
    label: 'Two axons reach one target: the winner branches richly, the loser withdraws',
    ink: p('M8 9 H48 V17 H8 Z') + c(14, 44, 4.5) + c(42, 44, 4.5) + p('M42 39.5 V30', 'stroke-dasharray="1.5 3.6"'),
    gold: gp('M14 39.5 V24 M14 24 L9 18 M14 24 L19 18 M14 28 L23 19'),
  },
  'retrograde-signal': {
    label: 'A neuron in a two-chamber dish; its axons reach the far chamber and a signal returns from there',
    ink: `<rect x="5" y="10" width="46" height="36" rx="4" />` + p('M27 10 V24 M27 32 V46') + c(14, 28, 4.5) + p('M18.5 26 H27 L44 17 M18.5 30 H27 L44 39'),
    gold: gd(46, 14, 2.4) + gd(46, 42, 2.4) + gp(`M43 28 H33 ${ah(31.5, 28, 'l', 2.6)}`),
  },
  'axon-pruning': {
    label: 'An axon that keeps two branches and lets a third fall apart',
    ink: c(9, 28, 4.5) + p('M13.5 28 H28 M28 28 L44 12 M28 28 L44 44 M44 12 L49 9 M44 12 L50 14 M44 44 L49 47 M44 44 L50 42'),
    gold: gp('M30 28 H49', 'stroke-dasharray="2.5 3.5"'),
  },
};
