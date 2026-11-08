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
/** A cube drawn in oblique view: front face at (x, y), side s, depth d. */
const cube = (x: number, y: number, s: number, d: number) =>
  `M${x} ${y} H${x + s} V${y + s} H${x} Z M${x} ${y} L${x + d} ${y - d} H${x + s + d} L${x + s} ${y} M${x + s + d} ${y - d} V${y + s - d} L${x + s} ${y + s}`;

export const ICONS: Record<string, IconArt> = {
  'organism-problems': {
    label: 'A leaf pore between two guard cells: carbon dioxide comes in and water vapour leaves through the same gold opening',
    ink: `<ellipse cx="28" cy="31" rx="13" ry="17" />` + p('M28 19 Q35 31 28 43 Q21 31 28 19 Z') + p('M28 14 V19 M28 43 V48')
      + p('M5 6 L14 15 M14 9 V15 H8')
      + p('M42 15 L51 6 M45 6 H51 V12') + dot(49, 18, 1.4) + dot(53, 14, 1.4),
    gold: `<path d="M28 21 Q33.5 31 28 41 Q22.5 31 28 21 Z" ${GF} />`,
  },
  'size-and-scaling': {
    label: 'A small gold cube beside a large one: the small cube has far more surface for each unit of volume',
    ink: p(cube(22, 22, 24, 8)),
    gold: gp(cube(4, 36, 11, 4)),
  },
  'microbes-protists-fungi': {
    label: 'A mushroom with its thread-like hyphae spreading through the soil, and a small gold rod-shaped bacterium with its flagellum',
    ink: p('M7 31 Q7 15 21 15 Q35 15 35 31 Z') + p('M17 31 V44 M25 31 V44 M17 44 H25')
      + p('M17 44 Q11 48 4 49 M21 44 V53 M25 44 Q31 48 39 50 M21 50 L14 54 M30 47 L34 53'),
    gold: `<rect x="35" y="7" width="12" height="6" rx="3" ${GF} />` + gp('M47 10 q1.5 -2.2 3 0 q1.5 2.2 3 0'),
  },
  'animal-body-plans': {
    label: 'A segmented worm seen from above, cut by a gold dashed line into matching left and right halves',
    ink: `<rect x="18" y="4" width="20" height="48" rx="10" />` + p('M18 17 H38 M18 25 H38 M18 33 H38 M18 41 H38')
      + dot(23.5, 10, 1.6) + dot(32.5, 10, 1.6),
    gold: gp('M28 1 V55', 'stroke-dasharray="3 3"'),
  },
  'plant-diversity-life-cycles': {
    label: 'A leafy moss shoot, the haploid gametophyte, with the gold stalk and capsule of the diploid sporophyte growing from its tip',
    ink: p('M28 54 V30') + p('M28 50 L19 45 M28 50 L37 45 M28 43 L20 38 M28 43 L36 38 M28 36 L22 32 M28 36 L34 32')
      + p('M28 54 L23 56 M28 54 L33 56'),
    gold: gp('M28 30 Q28.5 19 34 13') + `<ellipse cx="36.5" cy="9" rx="3" ry="5.2" transform="rotate(35 36.5 9)" ${GF} />`,
  },
  'tissues-and-homeostasis': {
    label: 'A thermometer held at its gold set level by a loop of feedback arrows running round it',
    ink: `<rect x="24" y="6" width="8" height="32" rx="4" />` + c(28, 43, 6) + p('M33 20 H36')
      + p(`M14 42 Q4 28 14 13 ${ah(14.5, 12.5, 'u', 3)}`) + p(`M42 13 Q52 28 42 42 ${ah(41.5, 43, 'd', 3)}`),
    gold: gd(28, 43, 3.8) + gp('M28 40 V20'),
  },
  'nervous-control': {
    label: 'A reflex arc: a sensory fibre from the skin enters the back of the spinal cord, links through the grey matter, and a motor fibre leaves the front for a muscle',
    ink: `<ellipse cx="37" cy="28" rx="16" ry="13" />` + p('M30 19 Q33 23 33 28 Q33 33 30 37 M44 19 Q41 23 41 28 Q41 33 44 37 M33 28 H41')
      + p('M2 8 Q5 5 8 8 Q11 11 14 8') + `<ellipse cx="9" cy="47" rx="6.5" ry="4.2" />` + dot(19, 10.5, 2.4),
    gold: gp('M8 9 Q20 9 31 18') + gp('M31 19 Q34 28 31 36') + gp('M31 37 Q24 47 15.5 47'),
  },
  'endocrine-system': {
    label: 'A gland releasing gold hormone into a blood vessel, which carries it to a distant target cell',
    ink: `<ellipse cx="12" cy="13" rx="8" ry="6" />` + p('M3 29 H53 M3 41 H53') + c(44, 13, 7) + p('M41 20.5 Q44 23 47 20.5'),
    gold: gd(14, 22.5, 1.9) + gd(18, 35, 1.9) + gd(28, 35, 1.9) + gd(38, 35, 1.9) + gd(44, 25.5, 1.9),
  },
  thermoregulation: {
    label: 'A small mammal making heat inside its body (gold) and losing it from its surface as rising wavy lines',
    ink: `<ellipse cx="25" cy="37" rx="15" ry="10" />` + c(43, 31, 6) + c(41, 24, 2.8) + dot(45, 30, 1.3)
      + p('M10 39 Q3 42 5 49') + p('M18 46 V51 M32 46 V51')
      + p('M17 22 q-2 -2.5 0 -5 q2 -2.5 0 -5 M25 22 q-2 -2.5 0 -5 q2 -2.5 0 -5 M33 22 q-2 -2.5 0 -5 q2 -2.5 0 -5'),
    gold: gd(25, 37, 4.5),
  },
  'circulation-and-heart': {
    label: 'A four-chambered heart as blocks, two atria above two ventricles; the left ventricle, on the viewer\'s right, has the thick gold wall that drives blood round the body',
    ink: `<rect x="9" y="7" width="18" height="13" rx="3" /><rect x="29" y="7" width="18" height="13" rx="3" /><rect x="9" y="23" width="18" height="26" rx="4" />`
      + p('M14 7 V2 M42 7 V2'),
    gold: `<rect x="30.5" y="24.5" width="15" height="23" rx="3.5" style="stroke:var(--ddp-color-secondary)" fill="none" stroke-width="3.2" />`,
  },
  'blood-and-vessels': {
    label: 'A thick-walled artery and a thin-walled vein cut across, above a capillary just wide enough for one gold red blood cell',
    ink: c(14, 18, 10) + c(14, 18, 5.5) + `<ellipse cx="40" cy="18" rx="12" ry="9" /><ellipse cx="40" cy="18" rx="10" ry="7" />`
      + p('M5 40 H51 M5 50 H51'),
    gold: `<ellipse cx="28" cy="45" rx="4.2" ry="3.4" ${GF} />`,
  },
  'gas-exchange': {
    label: 'Water and blood flowing past each other in opposite directions across a gill, the countercurrent that keeps oxygen moving into the blood',
    ink: p('M5 12 H51 M5 26 H51 M5 30 H51 M5 44 H51') + p(`M12 19 H42 ${ah(43, 19, 'r', 3)}`),
    gold: gp(`M44 37 H14 ${ah(13, 37, 'l', 3)}`),
  },
  'oxygen-transport': {
    label: 'The S-shaped oxygen dissociation curve of hemoglobin in gold, with a dashed copy shifted to the right as in the Bohr effect',
    ink: p('M8 6 V48 H52') + p('M9 47 C29 46 27 19 38 14 C42 12 46 11 51 11', 'stroke-dasharray="2 3"'),
    gold: gp('M9 47 C22 46 21 15 31 11 C37 9 44 8 51 8'),
  },
};

export const COURSE: Record<string, IconArt> = { 'course:organismal-biology': {
    label: "A heart outline with a seedling's first two leaves sprouting from its top, animal and plant in one",
    ink: p('M28 52 C19 45 8 37 8 26 C8 19 13 14 19 14 C23.5 14 26.5 17 28 20 C29.5 17 32.5 14 37 14 C43 14 48 19 48 26 C48 37 37 45 28 52 Z'),
    gold: gp('M28 20 V9') + `<path d="M28 11 Q21 3 15 7 Q21 13 28 11 Z" ${GF} /><path d="M28 11 Q35 3 41 7 Q35 13 28 11 Z" ${GF} />`,
  } };
