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
/** A sperm whose head sits at (x, y) and points along angle a (degrees); tail trails behind. */
const sperm = (x: number, y: number, a: number, gold = false) =>
  `<g transform="translate(${x} ${y}) rotate(${a})"><ellipse cx="0" cy="0" rx="2.8" ry="1.9" ${gold ? GF : ''} />`
  + `<path d="M-2.8 0 q-2 -2.2 -4 0 q-2 2.2 -4 0 q-2 -2.2 -4 0" ${gold ? GS : ''} /></g>`;

export const ICONS: Record<string, IconArt> = {
  'digestive-systems': {
    label: 'A schematic gut: a tube leading into a stomach pouch, then winding on as intestine toward the exit, with a gold mouthful in the stomach',
    ink: p('M22 3 V11') + p('M22 11 C12 14 12 27 24 28 C34 29 40 22 37 15 C35 10 28 9 22 11 Z')
      + p('M37 21 Q48 25 42 32 Q34 36 20 35 Q12 37 15 42 Q19 46 34 44 Q44 43 41 48 L34 53'),
    gold: gd(25, 19.5, 3.2),
  },
  osmoregulation: {
    label: 'A sea fish surrounded by grains of salt, holding on to its gold drop of body water',
    ink: p('M7 31 Q22 17 38 31 Q22 45 7 31 Z') + p('M38 31 L48 23 V39 Z') + dot(13, 29, 1.5)
      + p('M4 8 q4 -3 8 0 q4 3 8 0 q4 -3 8 0 q4 3 8 0 q4 -3 8 0 q4 3 8 0')
      + `<g stroke-width="1.4"><rect x="8" y="15" width="3" height="3" /><rect x="43" y="13" width="3" height="3" /><rect x="27" y="14" width="3" height="3" /><rect x="10" y="46" width="3" height="3" /><rect x="40" y="47" width="3" height="3" /><rect x="50" y="42" width="3" height="3" /></g>`,
    gold: `<path d="M23 24.5 C21 28 19.5 30 19.5 32 A3.5 3.5 0 0 0 26.5 32 C26.5 30 25 28 23 24.5 Z" ${GF} />`,
  },
  kidney: {
    label: 'A kidney drawn as a bean, its ureter leaving from the inner notch and carrying off a gold drop of urine',
    ink: p('M28 5 C14 4 8 17 9 29 C10 43 19 52 30 49 C36 47 37 40 33 36 C30 33 30 26 33 23 C37 19 39 6 28 5 Z')
      + p('M22 21 L32 29 L22 37') + p('M32 29 Q41 33 41 45'),
    gold: `<path d="M41 46 C39.5 49 38 50.5 38 52 A3 3 0 0 0 44 52 C44 50.5 42.5 49 41 46 Z" ${GF} />`,
  },
  'innate-immunity': {
    label: 'A phagocyte reaching out with two arms of its surface to swallow a gold bacterium',
    ink: p('M40 38 C36 47 18 49 11 39 C4 29 11 12 26 12 C34 12 38 15 40 18')
      + p('M40 18 C46 16 52 18 52 22.5 M40 38 C46 40 52 37.5 52 33.5') + `<ellipse cx="22" cy="30" rx="6" ry="4.5" />`,
    gold: `<rect x="38" y="24" width="12" height="8" rx="4" ${GF} />`,
  },
  'adaptive-immunity': {
    label: 'A Y-shaped antibody whose two arms each grip the same gold antigen',
    ink: p('M25 53 V32 L12 18 M31 53 V32 L44 18 M28 33 V53') + p('M21 30 L9 18 M35 30 L47 18'),
    gold: gd(9.5, 12.5, 3.6) + gd(46.5, 12.5, 3.6),
  },
  'muscle-and-movement': {
    label: 'One sarcomere: thin filaments anchored at the two Z lines overlap the gold thick filaments that pull them toward the centre',
    ink: p('M8 9 V47 M48 9 V47') + p('M8 17 H25 M8 28 H25 M8 39 H25 M48 17 H31 M48 28 H31 M48 39 H31'),
    gold: gp('M17 22.5 H39 M17 33.5 H39'),
  },
  'animal-reproduction': {
    label: 'An egg cell with sperm swimming toward it, the gold one reaching its surface first',
    ink: c(31, 30, 14) + c(31, 30, 17.5, 'stroke-dasharray="2 3"') + c(34, 28, 4) + sperm(42, 9, 120) + sperm(48, 48, -135),
    gold: sperm(12, 30, 0, true),
  },
  'animal-development': {
    label: 'An early embryo folding inward at one spot during gastrulation, the gold inner layer forming the primitive gut',
    ink: p('M20 46 C6 40 6 14 28 8 C50 14 50 40 36 46 Q34 48 32.5 44.5 C42 38 42 20 28 14 C14 20 14 38 23.5 44.5 Q22 48 20 46 Z')
      + p(`M28 55 V50 ${ah(28, 49, 'u', 2.6)}`),
    gold: gp('M23.5 44.5 C25 34 23 23 28 21 C33 23 31 34 32.5 44.5'),
  },
  'plant-body-and-growth': {
    label: 'A tree trunk cut across: rings of wood inside, bark outside, and the gold growing layer between them',
    ink: c(28, 28, 23) + c(28, 28, 19.5) + c(28, 28, 13.5) + c(28, 28, 8.5) + c(28, 28, 4) + dot(28, 28, 1.4)
      + p('M28 5 V8.5 M49.5 32 L46 31 M8 39 L11 37.5'),
    gold: c(28, 28, 17.5, GS),
  },
  'plant-transport': {
    label: "Water drawn up a plant's stem from its roots to the leaves, where it evaporates",
    ink: p('M28 50 V12') + p('M28 50 L20 55 M28 50 V55 M28 50 L36 55') + p('M6 48 H50')
      + p('M28 15 Q18 5 9 11 Q18 18 28 15 Z') + p('M28 15 Q38 5 47 11 Q38 18 28 15 Z')
      + dot(7, 4, 1.3) + dot(13, 2, 1.3) + dot(43, 2, 1.3) + dot(49, 4, 1.3),
    gold: gp(`M34 44 V21 ${ah(34, 20, 'u', 3)}`),
  },
  'plant-nutrition': {
    label: 'A pea root with round gold nodules where nitrogen-fixing bacteria live',
    ink: p('M6 6 H50') + p('M28 6 V53') + p('M28 18 Q20 22 11 31 M28 27 Q36 31 45 39 M28 38 Q20 42 15 51'),
    gold: gd(19, 23.5, 3.2) + gd(38, 32.5, 3.2) + gd(21, 44.5, 3) + gd(31.5, 47, 2.6),
  },
  'plant-signals': {
    label: 'A seedling shoot lit from one side by a gold lamp, bending toward it in the zone below its tip',
    ink: p('M6 50 H40') + p('M22 50 V33 Q22 23 33 16') + p('M33 16 L35.5 13 L36 17.5 Z') + p('M22 50 L17 54 M22 50 L27 54'),
    gold: gd(48, 10, 4) + gp('M42 13 L39 14.5 M44 17 L41 20 M47 18 L46 22'),
  },
  'plant-reproduction': {
    label: 'A pistil with a gold pollen grain on its stigma, its pollen tube growing down the style to an ovule',
    ink: `<ellipse cx="28" cy="43" rx="11" ry="9" />` + p('M25.5 34.3 V12 M30.5 34.3 V12') + p('M21 12 H35 Q37 9 34 7 H22 Q19 9 21 12 Z')
      + c(28, 45, 3.5),
    gold: gd(35, 4, 2.8) + gp('M33 6 Q28 9 28 14 V41'),
  },
};
