import type { IconArt } from '../signaling-icons';

/* Card icons for the high school Biology course (Virginia SOL), Units 1 to 3, and the course card.
   Same engraving hand as signaling-icons.ts: 56 x 56, navy ink, gold accent, concrete pictures a
   grade 7-12 reader recognises at a glance. */

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
/** A water drop with its tip at (x, y). */
const drop = (x: number, y: number) => `M${x} ${y} C${x + 2.5} ${y + 4} ${x + 3.5} ${y + 5.5} ${x + 3.5} ${y + 7} a3.5 3.5 0 0 1 -7 0 C${x - 3.5} ${y + 5.5} ${x - 2.5} ${y + 4} ${x} ${y} Z`;
const petal = 'M28 25 C19 22 15.5 12 21 6.5 Q24.5 9 28 7.5 Q31.5 9 35 6.5 C40.5 12 37 22 28 25 Z';

export const ICONS: Record<string, IconArt> = {
  'water-and-life': {
    label: 'A beaker of water with measuring marks, its surface drawn as a gold ripple',
    ink: p('M13 9 H43 M16 9 V45 Q16 50 21 50 H35 Q40 50 40 45 V9') + p('M40 31 H35.5 M40 39 H35.5')
      + dot(23, 37, 1.4) + dot(29, 42, 1.4) + dot(27, 33, 1.2),
    gold: gp('M16 24 q3 -2.4 6 0 t6 0 t6 0 t6 0'),
  },
  'macromolecules': {
    label: 'A sandwich in side view: bread, lettuce and a gold layer of cheese, food made of the big molecules of life',
    ink: p('M7 23 C7 13 17 11 28 11 C39 11 49 13 49 23 Z') + p('M7 27 q3.5 3 7 0 t7 0 t7 0 t7 0 t7 0 t7 0')
      + `<rect x="7" y="38" width="42" height="9" rx="3" />` + dot(20, 17, 1) + dot(30, 15.5, 1) + dot(38, 18, 1),
    gold: `<rect x="8" y="32" width="40" height="4.5" rx="1.5" ${GF} />`,
  },
  'enzymes-at-work': {
    label: 'A pineapple with a gold crown of leaves, the fruit whose enzyme keeps gelatin from setting',
    ink: `<ellipse cx="28" cy="37" rx="12" ry="15" />`
      + p('M21 30 L25 34 L29 30 L33 34 L37 30 M19 38 L23 42 L27 38 L31 42 L35 38 L37 40 M22 46 L26 49 L30 46 L34 49'),
    gold: gp('M28 22 V7 M28 22 L21.5 9.5 M28 22 L34.5 9.5 M28 22 L17 14.5 M28 22 L39 14.5'),
  },
  'photosynthesis-energy-capture': {
    label: 'A leaf with its veins, lit by a gold sun',
    ink: p('M14 48 C14 28 28 16 48 14 C48 34 36 48 14 48 Z') + p('M14 48 L42 20')
      + p('M23 39 V31 M23 39 H31 M31 31 V24 M31 31 H38'),
    gold: gd(13, 13, 4.2) + gp('M13 4 V6 M4 13 H6 M6.5 6.5 L8 8 M19.5 6.5 L18 8 M6.5 19.5 L8 18'),
  },
  'respiration-and-atp': {
    label: 'A mitochondrion with its folded inner membrane, and a gold spark of energy released from food',
    ink: `<ellipse cx="28" cy="32" rx="22" ry="13" />` + p('M10 32 Q13.5 24 17 32 T24 32 T31 32 T38 32 T45 32'),
    gold: gp('M44 3 L39 11 H45 L40 19'),
  },
  'cell-theory-evidence': {
    label: 'A light microscope with a gold slide on its stage',
    ink: p('M12 50 H40 M34 50 C34 42 38 34 34 25') + p('M19 11 L29 7 L35 23 L25 27 Z') + p('M17 6 L27 2')
      + p('M18 36 H40') + p('M26 27 L27.5 31'),
    gold: gp('M21 33 H33'),
  },
  'organelles-as-a-system': {
    label: 'A cell with its nucleus and the stacked Golgi, sending out gold vesicles of protein',
    ink: `<ellipse cx="28" cy="28" rx="24" ry="20" />` + c(17, 28, 7) + c(17, 28, 2.4)
      + p('M31 18 Q38 22 31 26 M33.5 15.5 Q42 22 33.5 28.5 M36 13.5 Q46 22 36 30.5'),
    gold: gd(43, 35, 2.6) + gd(37, 40, 2.1) + gd(46, 26, 1.8),
  },
  'crossing-the-membrane': {
    label: 'A cucumber slice with its seeds, a gold drop of water leaving it as it sits in salty water',
    ink: c(26, 30, 20) + c(26, 30, 16.5)
      + `<ellipse cx="26" cy="22" rx="1.6" ry="3" /><ellipse cx="26" cy="38" rx="1.6" ry="3" />`
      + `<ellipse cx="18.5" cy="26" rx="1.6" ry="3" transform="rotate(-60 18.5 26)" /><ellipse cx="33.5" cy="26" rx="1.6" ry="3" transform="rotate(60 33.5 26)" />`
      + `<ellipse cx="18.5" cy="34" rx="1.6" ry="3" transform="rotate(60 18.5 34)" /><ellipse cx="33.5" cy="34" rx="1.6" ry="3" transform="rotate(-60 33.5 34)" />`,
    gold: `<path d="${drop(48, 4)}" ${GF} />` + gp(`M43 12 L46 9`),
  },
  'homeostasis-in-action': {
    label: 'A thermometer whose gold column holds steady at the set point',
    ink: p('M24 37 V9 a4 4 0 0 1 8 0 V37 a8 8 0 1 1 -8 0 Z') + p('M36 14 H40 M36 20 H42 M36 26 H40 M36 32 H40'),
    gold: gd(28, 43, 4.6) + gp('M28 38 V20'),
  },
  'cell-cycle-and-mitosis': {
    label: 'An animal cell pinching into two, each half with its own chromosomes, gold arrows marking the furrow',
    ink: p('M28 15 C20 7 6 11 6 28 C6 45 20 49 28 41 C36 49 50 45 50 28 C50 11 36 7 28 15 Z')
      + p('M14 24 V32 M19 24 V32 M37 24 V32 M42 24 V32'),
    gold: gp(`M28 3 V9 ${ah(28, 10, 'd', 2.5)}`) + gp(`M28 53 V47 ${ah(28, 46, 'u', 2.5)}`),
  },
  'one-cell-or-many': {
    label: 'A paramecium, one cell fringed with cilia, its oral groove curving in and a gold vacuole inside',
    ink: p('M10 30 C8 18 20 12 32 14 C44 16 50 24 46 34 C42 44 26 46 16 42 C12 40 11 35 10 30 Z')
      + p('M30 31 C26 35 22 36 18 34')
      + p('M10 22 L6.5 20 M16 15 L13.5 12 M24 12.5 L23 9 M33 13 L34 9.5 M41 15.5 L43.5 12.5 M47 22 L50.5 20 M48.5 31 L52 31.5 M44 40 L47 43 M35 45 L36 48.5 M25 46 L24 49.5 M16 43 L13.5 46 M10.5 35 L7 37'),
    gold: `<circle cx="37" cy="25" r="3.6" ${GS} />` + gd(37, 25, 1.4),
  },
  'living-or-not': {
    label: 'A rod-shaped bacterium with its whip-like flagellum beside a much smaller virus, a protein coat around gold genes',
    ink: `<rect x="5" y="24" width="27" height="14" rx="7" />` + p('M11 31 q3 -4 6 0 t6 0')
      + p('M32 32 C36 38 40 28 44 34 C47 38 50 34 52 36')
      + p('M44 6 L50 9.5 V16.5 L44 20 L38 16.5 V9.5 Z'),
    gold: gp('M42 10.5 q2 1.5 0 3 t1.5 3'),
  },
  'how-microbes-multiply': {
    label: 'A bacterium splitting in two by binary fission, a gold copy of its chromosome in each half',
    ink: p('M10 21 H24 Q28 25 32 21 H46 a7 7 0 0 1 0 14 H32 Q28 31 24 35 H10 a7 7 0 0 1 0 -14 Z')
      + p(`M15 13 H41 ${ah(42, 13, 'r', 2.5)} M15 43 H41 ${ah(42, 43, 'r', 2.5)}`, 'opacity="0.55"'),
    gold: `<circle cx="16" cy="28" r="3.4" ${GS} /><circle cx="40" cy="28" r="3.4" ${GS} />`,
  },
  'microbes-in-ecosystems': {
    label: 'A bean plant pulled up to show root nodules where bacteria live, one nodule picked out in gold',
    ink: p('M4 15 H52') + p('M28 15 V5 M28 9 q-6 -4 -10 0 M28 9 q6 -4 10 0')
      + p('M28 15 C28 27 24 35 26 51 M28 23 C34 29 40 31 46 39 M27 31 C20 35 14 37 10 45')
      + c(41, 32, 3) + c(14, 39.5, 2.6) + c(33, 27, 2.2),
    gold: gd(26, 43, 3.4),
  },
  'germs-vaccines-antibiotics': {
    label: 'A vaccine syringe with a gold dose in its barrel',
    ink: `<g transform="rotate(-35 28 28)"><rect x="10" y="24" width="26" height="9" rx="1.2" />`
      + p('M3 28.5 H10 M3 24.5 V32.5 M36 25.5 V31.5 M36 28.5 H53 M16 24 V27 M21 24 V27 M26 24 V27') + `</g>`,
    gold: `<g transform="rotate(-35 28 28)"><rect x="27" y="25.6" width="8.4" height="5.8" ${GF} /></g>`,
  },
};

export const COURSE: Record<string, IconArt> = { 'course:high-school-biology': {
  label: "The flowering dogwood, Virginia's state flower: four notched petal-like bracts around a gold cluster of tiny flowers",
  ink: `<g>${p(petal)}<g transform="rotate(90 28 28)">${p(petal)}</g><g transform="rotate(180 28 28)">${p(petal)}</g><g transform="rotate(270 28 28)">${p(petal)}</g></g>`,
  gold: gd(28, 28, 3) + gd(24.2, 26.2, 1.5) + gd(31.8, 26.2, 1.5) + gd(26, 31.8, 1.5) + gd(30.5, 31.6, 1.5),
} };
