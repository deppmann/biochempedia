import type { IconArt } from '../signaling-icons';

/* Card icons for the grade 7 Life Science course (Virginia SOL), Units 1 to 4, and the course card.
   Same engraving hand as signaling-icons.ts: 56 x 56, navy ink, gold accent, concrete pictures a
   12-year-old recognises at a glance. */

const c = (x: number, y: number, r: number) => `<circle cx="${x}" cy="${y}" r="${r}" />`;
const p = (d: string, extra = '') => `<path d="${d}" ${extra}/>`;
const GF = 'style="fill:var(--ddp-color-secondary)"';
const GS = 'style="stroke:var(--ddp-color-secondary)" fill="none" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"';
const gd = (x: number, y: number, r = 3) => `<circle cx="${x}" cy="${y}" r="${r}" ${GF} />`;
const gp = (d: string, extra = '') => `<path d="${d}" ${GS} ${extra}/>`;
const dot = (x: number, y: number, r = 2.2) => `<circle cx="${x}" cy="${y}" r="${r}" fill="currentColor" stroke="none" />`;
/** A water drop with its tip at (x, y). */
const drop = (x: number, y: number) => `M${x} ${y} C${x + 2.5} ${y + 4} ${x + 3.5} ${y + 5.5} ${x + 3.5} ${y + 7} a3.5 3.5 0 0 1 -7 0 C${x - 3.5} ${y + 5.5} ${x - 2.5} ${y + 4} ${x} ${y} Z`;
export const ICONS: Record<string, IconArt> = {
  'cells-everywhere': {
    label: 'A drop of pond water holding tiny living cells, one of them picked out in gold',
    ink: p('M28 4 C34 14 44 24 44 34 a16 16 0 0 1 -32 0 C12 24 22 14 28 4 Z')
      + `<ellipse cx="24" cy="36" rx="6.5" ry="3.6" transform="rotate(-25 24 36)" />` + c(35, 41, 3) + c(33, 31, 1.8),
    gold: gd(23, 45, 2.4),
  },
  'inside-a-cell': {
    label: 'A heart with a gold mitochondrion inside it, the energy factory packed into heart muscle cells',
    ink: p('M28 49 C10 37 6 28 6 20 C6 12 12 8 18 8 C22 8 26 11 28 15 C30 11 34 8 38 8 C44 8 50 12 50 20 C50 28 46 37 28 49 Z'),
    gold: `<ellipse cx="28" cy="27" rx="10" ry="6" ${GS} />` + gp('M21 27 q2 -3 3.5 0 t3.5 0 t3.5 0'),
  },
  'plant-and-animal-cells': {
    label: 'A leafy stalk of celery standing in a glass of water, a gold drop in the water soaking up its cut end',
    ink: p('M14 32 L17 51 H39 L42 32') + p('M14 32 H42', 'opacity="0.55"')
      + p('M18 32 L11 17 H17 L22 32') + p('M25 32 L24 14 H32 L31 32') + p('M34 32 L39 17 H45 L38 32') + p('M28 31 V16', 'opacity="0.55"')
      + p('M9 16 q-3 -4 1 -6 q0 -4 4 -3 q3 -3 6 1 q4 1 2 5 q2 3 -2 4 Z') + p('M23 13 q-3 -4 1 -6 q0 -4 4 -3 q3 -3 6 1 q4 1 2 5 q2 3 -2 4 Z') + p('M37 16 q-3 -4 1 -6 q0 -4 4 -3 q3 -3 6 1 q4 1 2 5 q2 3 -2 4 Z'),
    gold: `<path d="${drop(28, 38)}" ${GF} />`,
  },
  'cells-divide': {
    label: 'An adhesive bandage across a scraped knee, its pad in gold, the spot where new skin cells are made',
    ink: `<g transform="rotate(-35 28 28)"><rect x="3" y="18" width="50" height="20" rx="10" />`
      + c(11, 28, 1) + c(11, 24, 1) + c(11, 32, 1) + c(45, 28, 1) + c(45, 24, 1) + c(45, 32, 1) + `</g>`,
    gold: `<g transform="rotate(-35 28 28)"><rect x="19" y="18" width="18" height="20" ${GF} /></g>`,
  },
  'diffusion-and-osmosis': {
    label: 'A salt shaker sprinkling salt over a puddle, a gold drop of water drawn out',
    ink: `<g transform="rotate(-30 20 22)">` + `<rect x="11" y="6" width="18" height="9" rx="2" />` + dot(16, 10.5, 1) + dot(20, 10.5, 1) + dot(24, 10.5, 1)
      + p('M13 15 C8 21 8 30 11 37 H29 C32 30 32 21 27 15') + `</g>`
      + dot(34, 30, 1.3) + dot(39, 26, 1.3) + dot(37, 35, 1.3) + dot(31, 38, 1.3) + dot(43, 32, 1.3)
      + p('M5 50 q4 -3 8 0 t8 0 t8 0 t8 0 t8 0 t8 0'),
    gold: `<path d="${drop(24, 40)}" ${GF} />`,
  },
  'levels-of-organization': {
    label: 'Three steps up: a single cell, a cluster of cells, then a whole sprouting plant, gold arrows pointing the way',
    ink: c(8, 40, 4) + c(22, 41, 3) + c(30, 41, 3) + c(26, 34, 3) + p('M47 52 V30 M47 44 q-8 -1 -8 -8 q8 0 8 8 M47 38 q8 -1 8 -8 q-8 0 -8 8') + p('M3 54 H53', 'opacity="0.55"'),
    gold: gp('M14 40 H18 M18 40 l-2.5 -2.5 M18 40 l-2.5 2.5 M36 40 H40 M40 40 l-2.5 -2.5 M40 40 l-2.5 2.5'),
  },
  'sorting-living-things': {
    label: 'A vulture soaring on spread wings with a gold name tag, one scientific name for one species',
    ink: p('M28 20 C22 17 14 18 4 24 L8 25 L6 29 L11 28 L11 32 L16 29 L18 33 L23 29 C25 30 26 33 26 36 H30 C30 33 31 30 33 29 L38 33 L40 29 L45 32 L45 28 L50 29 L48 25 L52 24 C42 18 34 17 28 20 Z') + p('M28 20 V13 q-3 -1 -3 -3.5 q3 -2.5 6 0 q0 2.5 -3 3.5') + p('M26 36 L24 44 H32 L30 36'),
    gold: gp('M10 40 H18 L21 44 L18 48 H10 Z') + gd(13, 44, 1.2),
  },
  'domains-kingdoms-and-dna': {
    label: 'A mushroom with gold gills under its cap, a fungus once filed with plants',
    ink: p('M6 28 C6 12 18 6 28 6 C38 6 50 12 50 28 Z') + p('M22 28 C23 38 22 44 20 50 H36 C34 44 33 38 34 28')
      + dot(16, 19, 1.8) + dot(27, 14, 1.8) + dot(38, 18, 1.8) + dot(31, 22, 1.4),
    gold: gp('M10 29 V35 M14 29 V36 M18 29 V37 M38 29 V37 M42 29 V36 M46 29 V35'),
  },
  'photosynthesis-feeds-the-world': {
    label: 'A tall tulip poplar tree next to the tiny gold seed it grew from',
    ink: p('M14 30 C4 28 4 14 14 13 C14 4 30 2 34 10 C44 8 50 20 44 28 C42 31 18 32 14 30 Z') + p('M29 30 V50 M29 42 L23 36 M29 40 L35 34') + p('M4 50 H52'),
    gold: `<ellipse cx="11" cy="46" rx="3" ry="1.8" transform="rotate(-30 11 46)" ${GF} />`,
  },
  'releasing-energy-from-food': {
    label: 'A thermos of sprouting seeds, warmth rising from it as gold wavy lines',
    ink: `<rect x="15" y="17" width="26" height="34" rx="5" />` + `<rect x="18" y="9" width="20" height="8" rx="3" />` + p('M41 23 H47 V39 H41') + p('M15 28 H41 M15 41 H41', 'opacity="0.55"'),
    gold: gp('M22 6 q-3 -2 0 -4 M28 6 q-3 -2 0 -4 M34 6 q-3 -2 0 -4'),
  },
  'photosynthesis-and-respiration-partners': {
    label: 'A water plant with bubbles of oxygen rising from its leaves, under a gold sun',
    ink: p('M26 52 V14 M26 44 q-9 -2 -9 -9 q9 0 9 9 M26 44 q9 -2 9 -9 q-9 0 -9 9 M26 30 q-9 -2 -9 -9 q9 0 9 9 M26 30 q9 -2 9 -9 q-9 0 -9 9')
      + c(40, 14, 2) + c(44, 24, 1.6) + c(46, 8, 1.4) + p('M4 52 H52'),
    gold: gd(10, 10, 4.2) + gp('M10 2 V3 M2 10 H3 M4.5 4.5 L5.5 5.5 M15.5 4.5 L14.5 5.5 M4.5 15.5 L5.5 14.5'),
  },
  'food-webs-and-energy': {
    label: 'An osprey diving to catch a fish, the dive path drawn as a gold dashed line',
    ink: p('M10 16 C16 8 22 10 26 16 C30 10 36 8 42 16 C36 14 30 17 26 24 C22 17 16 14 10 16 Z') + p('M26 24 V28')
      + p('M12 42 C18 34 30 34 38 42 C30 50 18 50 12 42 Z M38 42 L47 35 V49 Z') + dot(19, 40, 1.5),
    gold: gp('M26 30 V33', 'stroke-dasharray="1 3"'),
  },
  'producers-consumers-decomposers': {
    label: 'A fallen leaf on the forest floor with a gold earthworm tunnelling beneath it',
    ink: p('M6 24 C14 8 34 8 50 22 C36 32 16 34 6 24 Z M6 24 L50 22 M20 25 L16 18 M30 24 L28 15 M40 23 L40 17') + p('M4 36 H52')
      + dot(10, 46, 1.4) + dot(48, 44, 1.4) + dot(34, 50, 1.4) + dot(22, 52, 1.4),
    gold: gp('M12 41 q4 -4 8 0 t8 0 t8 0 t8 0'),
  },
  'carbon-and-water-cycles': {
    label: 'A graph of rising and falling carbon dioxide climbing slowly in a gold zigzag, beside a cloud dropping rain',
    ink: p('M7 51 V8 M7 51 H52') + p('M24 12 a5 5 0 0 1 9 -2 a4 4 0 0 1 8 2 a3 3 0 0 1 -2 5.5 H25 a3 3 0 0 1 -1 -5.5 Z') + p('M28 21 l-1.5 3 M34 21 l-1.5 3 M40 21 l-1.5 3'),
    gold: gp('M10 46 L16 40 L20 43 L27 35 L31 38 L38 30 L42 33 L50 25'),
  },
  'nitrogen-for-life': {
    label: 'A soybean plant with three-part leaves and a pod above the soil line, and round gold nodules on its roots below',
    ink: p('M4 28 H52') + p('M28 28 V14') + `<ellipse cx="28" cy="7" rx="3.6" ry="5.5" />` + `<ellipse cx="20.5" cy="13" rx="3.6" ry="5.5" transform="rotate(-65 20.5 13)" />` + `<ellipse cx="35.5" cy="13" rx="3.6" ry="5.5" transform="rotate(65 35.5 13)" />`
      + p('M28 21 L35 19 M35 19 C41 17 47 21 48 27 C42 27 37 24 35 19 Z') + dot(40, 23, 1) + dot(44, 25, 1)
      + p('M28 28 C28 38 26 44 24 53 M28 31 C34 36 40 41 44 51 M27 35 C20 37 14 41 10 48'),
    gold: gd(26.6, 40.5, 2.8) + gd(36, 39, 2.8) + gd(41.5, 46, 2.8) + gd(17, 40, 2.8) + gd(25, 49, 2.6),
  },
};

export const COURSE: Record<string, IconArt> = { 'course:life-science': {
  label: 'A magnifying glass held beside a leaf, showing a single cell with a gold nucleus inside',
  ink: p('M4 28 C4 14 16 5 32 4 C32 18 22 28 4 28 Z M4 28 L24 12') + c(37, 37, 12.5) + p('M46 46 L53 53', 'stroke-width="3.4"') + c(37, 37, 6.5),
  gold: gd(37, 37, 2.6),
} };
