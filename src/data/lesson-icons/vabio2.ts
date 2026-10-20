import type { IconArt } from '../signaling-icons';

/* Card icons for the high school Biology course (Virginia SOL), Units 4 to 7.
   Same engraving hand as signaling-icons.ts: 56 x 56, navy ink, gold accent. DNA is only ever a
   ladder or a ribbon, never a chemical structure. */

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
const DASH = 'stroke-dasharray="2.5 3.5"';
const sun = (x: number, y: number) => gd(x, y, 3.6)
  + gp(`M${x} ${y - 8} V${y - 6} M${x - 8} ${y} H${x - 6} M${x + 6} ${y} H${x + 8} M${x - 5.7} ${y - 5.7} L${x - 4.3} ${y - 4.3} M${x + 5.7} ${y - 5.7} L${x + 4.3} ${y - 4.3}`);

export const ICONS: Record<string, IconArt> = {
  'dna-structure-and-copying': {
    label: 'A DNA ladder unzipping from the top, each opened side getting a new gold partner strand',
    ink: p('M22 52 V30 L12 5 M34 52 V30 L44 5') + p('M22 35 H34 M22 41 H34 M22 47 H34'),
    gold: gp('M25.5 28 L16.5 6.5 M30.5 28 L39.5 6.5'),
  },
  'discovering-dna-structure': {
    label: 'The double helix drawn as a twisted ladder, studied under a gold magnifying glass',
    ink: p('M17 4 C17 16 39 16 39 28 C39 40 17 40 17 52 M39 4 C39 16 17 16 17 28 C17 40 39 40 39 52')
      + p('M18.5 7 H37.5 M21 24.5 H35 M21 31.5 H35 M18.5 49 H37.5'),
    gold: `<circle cx="43" cy="38" r="7" ${GS} />` + gp('M48 43 L53 48'),
  },
  'protein-synthesis': {
    label: 'A ribosome riding along a strand of messenger RNA, a gold chain of amino acids growing out of it',
    ink: p('M3 41 H53') + p('M10 41 V44 M17 41 V44 M24 41 V44 M31 41 V44 M38 41 V44 M45 41 V44')
      + `<ellipse cx="28" cy="30" rx="12" ry="8" /><ellipse cx="28" cy="47" rx="9" ry="4.5" />`,
    gold: gd(28, 18.5, 2.4) + gd(24, 13.5, 2.4) + gd(27, 8.5, 2.4) + gd(32.5, 5.5, 2.4),
  },
  'meiosis-and-variation': {
    label: 'One cell dividing twice into four sex cells, each with half the chromosomes, one sex cell picked out in gold',
    ink: c(28, 11, 7) + p('M25.5 8 V14 M30.5 8 V14')
      + p('M28 18 V25 M9 31 V28 H48 V31 M22.5 28 V31 M35.5 28 V31')
      + c(9, 40, 5.5) + c(22.5, 40, 5.5) + c(35.5, 40, 5.5) + p('M9 37 V43 M22.5 37 V43 M35.5 37 V43'),
    gold: `<circle cx="48" cy="40" r="5.5" ${GS} />` + gp('M48 37 V43'),
  },
  'punnett-squares': {
    label: 'A Punnett square: alleles from each parent along the top and side, the box with two recessive alleles in gold',
    ink: `<rect x="15" y="15" width="36" height="36" rx="1.5" />` + p('M33 15 V51 M15 33 H51')
      + dot(24, 8, 3) + c(42, 8, 3) + dot(8, 24, 3) + c(8, 42, 3),
    gold: `<rect x="36" y="36" width="12" height="12" rx="2" ${GF} />`,
  },
  'beyond-dominance': {
    label: "A patch of a roan calf's coat seen up close: red hairs and white hairs, in ink and gold, growing side by side",
    ink: `<rect x="8" y="8" width="40" height="40" rx="5" />` + p('M14 13 C15 24 13 34 14 43 M24 13 C25 24 23 34 24 43 M34 13 C35 24 33 34 34 43 M43 13 C44 24 42 34 43 43'),
    gold: gp('M19 13 C20 24 18 34 19 43 M29 13 C30 24 28 34 29 43 M38.5 13 C39.5 24 37.5 34 38.5 43'),
  },
  'genetic-engineering': {
    label: 'A ring of bacterial plasmid DNA with a gold gene spliced into it',
    ink: c(28, 30, 16) + c(28, 30, 12) + p('M17 14 L14.5 10.5 M39 14 L41.5 10.5'),
    gold: gp('M18 17.5 A16 16 0 0 1 38 17.5') + gp('M20.5 21 A12 12 0 0 1 35.5 21'),
  },
  'building-a-tree-of-life': {
    label: 'A cladogram: branches leave a main line at shared ancestors, one branch point marked in gold',
    ink: p('M6 51 L47 10 M14 43 V9 M24 33 V9 M35 22 V9') + dot(14, 7.5, 2) + dot(24, 7.5, 2) + dot(35, 7.5, 2) + dot(48, 8.5, 2),
    gold: gd(24, 33, 2.8) + gp('M27.5 33.5 L31 30', 'opacity="0.8"'),
  },
  'domains-and-kingdoms': {
    label: 'Life splitting three ways from a gold common root: two kinds of rod-shaped microbe and a cell with a nucleus',
    ink: p('M28 52 V37 M28 37 L11 20 M28 37 V20 M28 37 L45 20')
      + `<rect x="3" y="9" width="16" height="8" rx="4" /><rect x="20" y="9" width="16" height="8" rx="4" />`
      + p('M23 9 V17 M27 9 V17 M31 9 V17', 'opacity="0.6"') + c(45, 13, 6.5) + c(45, 13, 2.4),
    gold: gd(28, 37, 3),
  },
  'classification-changes': {
    label: 'Five kingdom boxes rearranged into three domain bands, a gold arrow showing the change',
    ink: `<rect x="5" y="6" width="9" height="7" rx="1.5" /><rect x="5" y="15.5" width="9" height="7" rx="1.5" /><rect x="5" y="25" width="9" height="7" rx="1.5" /><rect x="5" y="34.5" width="9" height="7" rx="1.5" /><rect x="5" y="44" width="9" height="7" rx="1.5" />`
      + `<rect x="33" y="7" width="5.5" height="43" rx="2" /><rect x="40.5" y="7" width="5.5" height="43" rx="2" /><rect x="48" y="7" width="5.5" height="43" rx="2" />`,
    gold: gp(`M18 28.5 H28 ${ah(29, 28.5, 'r', 3)}`),
  },
  'evidence-for-evolution': {
    label: 'Layers of rock with a shark tooth near the top and a gold fossil whale bone deeper down',
    ink: `<rect x="6" y="8" width="44" height="42" rx="2" />` + p('M6 19 Q28 16 50 19 M6 30 Q28 27 50 30 M6 41 Q28 38 50 41')
      + p('M14 15.5 L17 11 L19 16 Z'),
    gold: gp('M21 35 H35') + gd(19.8, 33.6, 1.8) + gd(19.8, 36.4, 1.8) + gd(36.2, 33.6, 1.8) + gd(36.2, 36.4, 1.8),
  },
  'variation-and-survival': {
    label: "An African elephant's head in profile with a gold tusk; under poaching, tuskless females became far more common",
    ink: p('M14 22 C13 11 23 6 31 8 C39 10 43 18 41 26 C40 32 37 35 37 41 C37 47 39 50 43 52')
      + p('M25 14 C15 16 11 30 19 38 C23 40 27 36 27 30') + dot(33, 18, 1.8),
    gold: gp('M35 32 C38.5 36 44 36.5 48 33'),
  },
  'natural-selection-and-speciation': {
    label: 'A Galapagos ground finch with a deep gold beak beside the large, hard seed it can crack',
    ink: c(23, 24, 12.5) + dot(25, 20, 1.8) + p('M13 33 C10 43 18 51 30 49 C37 48 40 42 38 35')
      + `<ellipse cx="47" cy="45" rx="5" ry="3.8" />` + p('M44 44 Q47 42.5 50 44', 'opacity="0.6"'),
    gold: `<path d="M35 18 L50 25 L35 32 Z" ${GF} />`,
  },
  'carrying-capacity': {
    label: 'A Chesapeake blue crab under a gold dashed line: the most crabs the Bay can hold',
    ink: `<g transform="translate(0 4)">` + p('M10 33 C14 25 42 25 46 33 C42 39 14 39 10 33 Z') + p('M10 33 L4 29 M46 33 L52 29')
      + p('M15 28 C10 24 8 19 11 14 M41 28 C46 24 48 19 45 14') + p('M11 14 C8 11 8 7 11 5 C12 8 14 10 16 10 C15 12 13 13.5 11 14 Z M45 14 C48 11 48 7 45 5 C44 8 42 10 40 10 C41 12 43 13.5 45 14 Z')
      + p('M16 38 L10 45 M22 39 L18 47 M34 39 L38 47 M40 38 L46 45') + dot(25, 29, 1.3) + dot(31, 29, 1.3) + `</g>`,
    gold: gp('M4 5 H52', DASH),
  },
  'energy-in-ecosystems': {
    label: 'An energy pyramid of four feeding levels, each much smaller than the one below, with the gold sun as the source',
    ink: p('M8 51 L30 7 L52 51 Z') + p('M14 39 H46 M20 27 H40 M26 15 H34'),
    gold: sun(10, 10),
  },
  'matter-cycles': {
    label: 'A carbon atom, shown as a gold dot, cycling between a tree, the air and the ground as rain falls',
    ink: p('M4 50 H52') + p('M14 50 V38') + c(14, 31, 7.5)
      + p('M33 15 a5 5 0 0 1 9 -4 a5 5 0 0 1 9 4 a4 4 0 0 1 0 8 H33 a4 4 0 0 1 0 -8 Z')
      + p('M38 27 V31 M44 27 V35 M50 27 V31', 'opacity="0.7"') + p(`M22 26 C26 17 29 15 33 17 ${ah(33, 17, 'r', 2.5)}`),
    gold: gd(44, 40, 2.6) + gd(27, 19.5, 2.1) + gp(`M44 44 V49`, 'opacity="0.6"'),
  },
  'succession-in-virginia': {
    label: 'An old field growing back: grasses, then a young pine, then a tall oak, in the gold light of the sun',
    ink: p('M4 50 H52') + p('M7 50 L6 43 M9.5 50 V41 M12 50 L13 43')
      + p('M18 44 L25 26 L32 44 Z M25 44 V50') + p('M43 50 V37') + c(43, 27, 10),
    gold: sun(11, 12),
  },
  'chesapeake-under-pressure': {
    label: 'A Chesapeake oyster shell with its growth ridges, resting above a gold ripple of Bay water',
    ink: p('M12 41 C5 30 12 11 28 8 C35 6.5 39 9 42 8 C49 12 52 21 47 30 C43 38 35 44 25 46.5 C19 47.5 14.5 45 12 41 Z')
      + p('M16 39 C13 29 19 18 30 14.5 M20 40.5 C19.5 31 26 22.5 37 20 M25 42 C27 34 33 28.5 42 26.5'),
    gold: gp('M4 52 q4 -3 8 0 t8 0 t8 0 t8 0 t8 0 t8 0'),
  },
};
