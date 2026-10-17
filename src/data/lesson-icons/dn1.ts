import type { IconArt } from '../signaling-icons';

const c = (x: number, y: number, r: number) => `<circle cx="${x}" cy="${y}" r="${r}" />`;
const p = (d: string, extra = '') => `<path d="${d}" ${extra}/>`;
const GF = 'style="fill:var(--ddp-color-secondary)"';
const GS = 'style="stroke:var(--ddp-color-secondary)" fill="none" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"';
const gd = (x: number, y: number, r = 3) => `<circle cx="${x}" cy="${y}" r="${r}" ${GF} />`;
const gp = (d: string) => `<path d="${d}" ${GS} />`;
const gc = (x: number, y: number, r: number) => `<circle cx="${x}" cy="${y}" r="${r}" ${GS} />`;
const dot = (x: number, y: number, r = 2.4) => `<circle cx="${x}" cy="${y}" r="${r}" fill="currentColor" stroke="none" />`;
const ah = (x: number, y: number, dir: 'r' | 'l' | 'u' | 'd', s = 3) =>
  dir === 'r' ? `M${x - s} ${y - s} L${x} ${y} L${x - s} ${y + s}`
  : dir === 'l' ? `M${x + s} ${y - s} L${x} ${y} L${x + s} ${y + s}`
  : dir === 'u' ? `M${x - s} ${y + s} L${x} ${y} L${x + s} ${y + s}`
  : `M${x - s} ${y - s} L${x} ${y} L${x + s} ${y - s}`;
const DASH = 'stroke-dasharray="1.5 3.5"';

export const ICONS: Record<string, IconArt> = {
  'wiring-problem': {
    label: 'Three cells on each side with many possible connections between them, one chosen connection marked',
    ink: c(9, 12, 3.5) + c(9, 28, 3.5) + c(9, 44, 3.5) + c(47, 12, 3.5) + c(47, 28, 3.5) + c(47, 44, 3.5)
      + p('M13 12 H43 M13 28 H43 M13 44 H43 M12.5 13.5 L43.5 26.5 M12.5 26.5 L43.5 13.5 M12.5 29.5 L43.5 42.5 M12.5 42.5 L43.5 29.5 M12.5 14.5 L43.5 41.5', DASH),
    gold: gp('M12.5 41.5 L43.5 14.5') + gd(9, 44, 2) + gd(47, 12, 2),
  },
  'neuron-doctrine': {
    label: 'Two separate nerve cells, the end of one stopping short of the next at a marked gap',
    ink: c(14, 15, 5.5) + p('M10 11 L6 6 M9 17 L5 20 M15 9.5 L16 5 M18 19 L25 26')
      + c(26.5, 27.5, 2)
      + c(41, 41, 5.5) + p('M37 37 L33 33 M45 45 L50 50 M46.5 39.5 L51 37 M40 46.5 L39 51'),
    gold: gp('M27 35 L35 27'),
  },
  'growth-cone': {
    label: 'An axon ending in a fan-shaped growth cone that reaches out with fine fingers',
    ink: p('M6 50 C14 46 18 40 24 33') + p('M28 19 L25 8 M34 17 L37 6 M39 20 L47 12 M41 27 L50 26 M23 25 L13 20'),
    gold: `<path d="M22 34 C19 26 25 17 33 17 C40 17 44 24 40 30 C37 34 28 37 22 34 Z" ${GF} />`,
  },
  'tools-for-development': {
    label: 'A fine glass needle marking one cell in a small cluster',
    ink: p('M30 27 L50 11 M30 27 L45 6 M45 6 L50 11') + c(11, 38, 6) + c(17, 49, 5) + c(32, 46, 5),
    gold: gc(24, 34, 6.5) + gd(24, 34, 2.6),
  },
  'the-organizer': {
    label: 'A round embryo carrying its own neural tube and a second, grafted one beside it',
    ink: c(28, 28, 22) + p('M14 13 Q10 28 14 43 M20 9 Q16 28 20 47'),
    gold: gp('M36 9 Q40 28 36 47 M42 13 Q46 28 42 43'),
  },
  'neural-induction': {
    label: 'An intact square of cells beside the same cells pulled apart, which turn into neural cells',
    ink: `<rect x="5" y="16" width="18" height="24" rx="2" />` + p('M14 16 V40 M5 24 H23 M5 32 H23') + p(`M26 28 H31 ${ah(32, 28, 'r', 2.6)}`),
    gold: gd(39, 15, 3.4) + gd(48, 23, 3.4) + gd(39, 30, 3.4) + gd(48, 38, 3.4) + gd(39, 44, 3.4),
  },
  'neurulation-and-tube-defects': {
    label: 'A cross-section of the neural plate rising into two folds that curve toward each other over a groove, about to close',
    ink: p('M4 46 H9 C16 46 8 9 19 9 C24 9 26 11 25 14.5 C24 19 21 30 28 38 C35 30 32 19 31 14.5 C30 11 32 9 37 9 C48 9 40 46 47 46 H52'),
    gold: gd(28, 12, 2.6),
  },

  'hox-and-hindbrain': {
    label: 'A row of hindbrain segments with a nested set of gene stripes below, each starting under a different segment',
    ink: p('M6 11 a3.67 3.5 0 0 1 7.33 0 a3.67 3.5 0 0 1 7.33 0 a3.67 3.5 0 0 1 7.33 0 a3.67 3.5 0 0 1 7.33 0 a3.67 3.5 0 0 1 7.33 0 a3.67 3.5 0 0 1 7.33 0')
      + p('M6 19 a3.67 3.5 0 0 0 7.33 0 a3.67 3.5 0 0 0 7.33 0 a3.67 3.5 0 0 0 7.33 0 a3.67 3.5 0 0 0 7.33 0 a3.67 3.5 0 0 0 7.33 0 a3.67 3.5 0 0 0 7.33 0')
      + p('M6 11 V19 M50 11 V19') + p('M13.33 30 H50 M28 42 H50 M35.33 48 H50'),
    gold: gp('M20.67 36 H50'),
  },

  'local-organizers': {
    label: 'The front of the neural tube pinched in at the boundary between midbrain and hindbrain, where an organizer sits',
    ink: p('M7 22 C7 9 24 10 28 20 C32 10 49 9 49 22 M7 34 C7 47 24 46 28 36 C32 46 49 47 49 34 M7 22 Q5 28 7 34 M49 22 Q51 28 49 34'),
    gold: `<path d="M28 18 V38" style="stroke:var(--ddp-color-secondary)" fill="none" stroke-width="3.2" stroke-linecap="round" />`,
  },
  'shh-bmp-neural-tube': {
    label: 'A neural tube in cross-section with a signal source beneath it and stacked domains on each side',
    ink: `<ellipse cx="28" cy="24" rx="13" ry="18" />` + p('M28 13 V35') + p('M16.5 18 H24 M16 26 H24 M17.5 33 H24 M32 18 H39.5 M32 26 H40 M32 33 H38.5'),
    gold: gd(28, 49, 4.2) + gp('M23 41 Q28 43.5 33 41'),
  },
  'motor-neuron-code': {
    label: 'A motor neuron carrying a combination of three factors, its axon reaching a muscle',
    ink: c(16, 28, 9.5) + p('M9.5 21 L6 16 M9.5 35 L6 40 M25.5 28 H41 M41 28 L45 23 M41 28 L45 33') + `<rect x="46" y="15" width="5" height="26" rx="2.5" />`,
    gold: gd(12.5, 25, 2.4) + gd(19.5, 25, 2.4) + gd(16, 31.5, 2.4),
  },
  'cortical-areas': {
    label: 'A side view of the cortex divided into areas, one area marked',
    ink: p('M8 32 C6 17 20 8 33 9 C46 10 52 21 49 31 C47 39 40 42 34 40 C30 45 22 47 16 44 C10 41 8 37 8 32 Z')
      + p('M24 9 C22 20 24 32 27 44 M39 10.5 C37 21 39 31 41 40.5'),
    gold: `<path d="M27 13 C26 22 27 32 29.5 40 C32 39 34.5 38.5 37.5 37.5 C36 30 34.5 21 36 13.2 C33 12.2 30 12.2 27 13 Z" ${GF} />`,
  },

  'radial-glia-progenitors': {
    label: 'Three long progenitor cells spanning the wall, their nuclei moving up and down',
    ink: p('M5 7 H51 M5 49 H51') + p('M12 7 V34 M12 42 V49 M24 7 V21 M24 29 V49 M38 7 V13 M38 21 V49') + c(12, 38, 4) + c(38, 17, 4),
    gold: gd(24, 25, 4.2) + gp(`M30 18 V32 ${ah(30, 17, 'u', 2.5)} ${ah(30, 33, 'd', 2.5)}`),
  },
  'proneural-and-lateral-inhibition': {
    label: 'A ring of equal cells around one that has been picked to become neural',
    ink: c(44, 28, 6) + c(36, 41.9, 6) + c(20, 41.9, 6) + c(12, 28, 6) + c(20, 14.1, 6) + c(36, 14.1, 6),
    gold: gc(28, 28, 7) + gd(28, 28, 3),
  },
  'asymmetric-division': {
    label: 'A cell dividing in two, a protein crescent going to only one daughter',
    ink: p('M28 21.7 A11 11 0 1 0 28 34.3 A11 11 0 1 0 28 21.7') + dot(21, 28, 2) + dot(37, 28, 2),
    gold: `<path d="M15 21.1 A8 8 0 0 0 15 34.9" style="stroke:var(--ddp-color-secondary)" fill="none" stroke-width="3.2" stroke-linecap="round" />`,
  },
  'birth-order-and-layers': {
    label: 'Neurons born later climb past earlier ones to the upper layers of the cortex',
    ink: p('M6 9 H50 M6 21 H50 M6 33 H50 M6 47 H50', '') + p('M14 46 V40') + dot(14, 39, 2.8) + p('M28 46 V29') + dot(28, 27, 2.8),
    gold: gp('M42 46 V17') + gd(42, 15, 3.2),
  },
  'radial-migration': {
    label: 'A young neuron climbing a glial fibre, its centrosome leading and its nucleus following',
    ink: p('M6 7 H50 M6 49 H50') + p('M36 49 V12 M32 7 L36 12 L40 7') + c(26, 37, 5) + p('M26 32 C26 24 30 18 34 14 M26 42 V47'),
    gold: gd(26.3, 27, 2.6) + gp(`M15 34 V18 ${ah(15, 17, 'u', 3)}`),
  },
};
