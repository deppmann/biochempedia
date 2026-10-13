/* =============================================================================
   Card icons for the Cell Signaling lessons
   -----------------------------------------------------------------------------
   One small engraving per lesson, in the same hand as the biochemistry icons in
   LessonIcon.astro: a 56 x 56 box, navy single-weight linework (`ink`, drawn in
   currentColor) and one or two gold accents (`gold`). Each is a diagram of the
   lesson's idea (a switch, a relay, a membrane, a trace), never a molecular
   structure. LessonIcon looks a slug up here before its own list.
   ============================================================================ */

export interface IconArt {
  /** What the picture shows, for screen readers. */
  label: string;
  /** Elements stroked in the ink colour (inside one <g>). */
  ink: string;
  /** Gold accents, each element carrying its own style. */
  gold: string;
}

const c = (x: number, y: number, r: number) => `<circle cx="${x}" cy="${y}" r="${r}" />`;
const p = (d: string, extra = '') => `<path d="${d}" ${extra}/>`;
const GF = 'style="fill:var(--ddp-color-secondary)"';
const GS = 'style="stroke:var(--ddp-color-secondary)" fill="none" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"';
/** A gold dot. */
const gd = (x: number, y: number, r = 3) => `<circle cx="${x}" cy="${y}" r="${r}" ${GF} />`;
/** A gold stroke. */
const gp = (d: string) => `<path d="${d}" ${GS} />`;
/** An arrowhead whose tip is at (x, y), pointing right, left, up or down. */
const ah = (x: number, y: number, dir: 'r' | 'l' | 'u' | 'd', s = 3) =>
  dir === 'r' ? `M${x - s} ${y - s} L${x} ${y} L${x - s} ${y + s}`
  : dir === 'l' ? `M${x + s} ${y - s} L${x} ${y} L${x + s} ${y + s}`
  : dir === 'u' ? `M${x - s} ${y + s} L${x} ${y} L${x + s} ${y + s}`
  : `M${x - s} ${y - s} L${x} ${y} L${x + s} ${y - s}`;
/** A membrane: two parallel lines across the box at height y. */
const mem = (y: number, x1 = 6, x2 = 50) => p(`M${x1} ${y} H${x2} M${x1} ${y + 5} H${x2}`);

export const SIGNALING_ICONS: Record<string, IconArt> = {
  'signals-and-distance': {
    label: 'Two cells far apart, a signal crossing the gap between them',
    ink: c(12, 42, 6) + c(44, 14, 6) + p('M17 37 Q22 18 38 16', 'stroke-dasharray="1.5 4"'),
    gold: gd(25, 24, 3.2),
  },
  'finding-a-signal': {
    label: 'A cluster of nerve cells with a halo of fibres growing out of it',
    ink: c(28, 28, 7) + p('M28 17 V7 M28 39 V49 M17 28 H7 M39 28 H49 M20.2 20.2 L13 13 M35.8 20.2 L43 13 M20.2 35.8 L13 43 M35.8 35.8 L43 43'),
    gold: gd(28, 28, 3.2),
  },
  'binding-and-dose-response': {
    label: 'An S-shaped dose–response curve with its half-maximal point marked',
    ink: p('M10 47 V9 M10 47 H49') + p('M11 44 C28 44 26 14 48 14'),
    gold: gd(28.5, 29, 3.2),
  },
  'receptor-field-guide': {
    label: 'Four kinds of receptor set in one membrane',
    ink: mem(25) + p('M9 34 V21 L12 18 L15 21 V34') + p('M23 36 V19 M27 36 V19 M21 16 L23 19 M29 16 L27 19') + p('M35 20 V35 M40 20 V35') + c(46, 43, 4),
    gold: gd(37.5, 13, 2.8) + gd(12, 12, 2.2),
  },
  'signaling-circuits': {
    label: 'Three steps in a row, the last one feeding back to shut off the first',
    ink: c(11, 34, 5) + c(28, 34, 5) + c(45, 34, 5) + p(`M16 34 H22 ${ah(23, 34, 'r', 2.5)} M33 34 H39 ${ah(40, 34, 'r', 2.5)}`),
    gold: gp('M45 28 C45 10 11 10 11 24 M7 24 H15'),
  },
  'phosphorylation-switch': {
    label: 'A protein with one phosphate added, the mark that switches it',
    ink: `<rect x="9" y="24" width="28" height="18" rx="8" />` + p('M34 26 L39 20') + p(`M14 14 Q22 8 30 13 ${ah(30.5, 13.2, 'r', 2.6)}`),
    gold: gd(43, 16, 5.2),
  },
  'gtpase-switches': {
    label: 'A timer: a switch that turns itself off after a set time',
    ink: c(28, 31, 15) + p('M28 31 V20 M24 10 H32 M28 10 V16 M40 19 L43 16'),
    gold: `<path d="M28 31 L28 19 A12 12 0 0 1 38.4 25 Z" ${GF} />`,
  },
  'ubiquitin-and-proteolysis': {
    label: 'A tagged protein fed into a barrel that cuts it into pieces',
    ink: `<rect x="29" y="14" width="13" height="28" rx="4" />` + p('M29 23 H42 M29 33 H42 M8 28 H29 M46 22 H50 M46 28 H51 M46 34 H50'),
    gold: gd(12, 20, 2.6) + gd(17.5, 16, 2.6) + gd(23, 12, 2.6) + gp('M9.5 26 L11 22.5'),
  },
  'protein-interaction-modules': {
    label: 'A protein made of separate modules, one of them gripping a partner',
    ink: p('M8 30 H48') + c(14, 30, 5.5) + `<rect x="23" y="24.5" width="11" height="11" rx="2" />` + p('M39 24 H47 V28 H43.5 V32 H47 V36 H39 Z') + p('M28.5 24.5 V17'),
    gold: gd(28.5, 13, 4),
  },
  'adaptors-and-scaffolds': {
    label: 'Three proteins held in a row on one scaffold',
    ink: c(13, 22, 5.5) + c(28, 22, 5.5) + c(43, 22, 5.5) + p(`M19.5 22 H21.5 ${ah(22, 22, 'r', 2.2)} M34.5 22 H36.5 ${ah(37, 22, 'r', 2.2)} M13 28 V34 M28 28 V34 M43 28 V34`),
    gold: `<rect x="6" y="34" width="44" height="7" rx="3.5" ${GF} />`,
  },
  'lipid-anchors-and-addresses': {
    label: 'A protein held at a membrane by a lipid tail',
    ink: mem(14) + c(28, 40, 8),
    gold: gp('M28 32 L25 28 L31 25 L25 21 L31 17 L28 14'),
  },
  'gpcrs-and-g-proteins': {
    label: 'A receptor that crosses the membrane seven times, with its G protein below',
    ink: mem(20) + p('M8 15 V30 Q8 34 11 34 Q14 34 14 30 V15 Q14 11 17 11 Q20 11 20 15 V30 Q20 34 23 34 Q26 34 26 30 V15 Q26 11 29 11 Q32 11 32 15 V30 Q32 34 35 34 Q38 34 38 30 V15 Q38 11 41 11 Q44 11 44 15 V34') + c(30, 44, 4.2) + c(38, 46, 3.2),
    gold: gd(46, 40, 4.6),
  },
  'camp-and-pka': {
    label: 'A small messenger binds a kinase and its two halves come apart',
    ink: `<rect x="20" y="18" width="16" height="10" rx="3" />` + c(13, 42, 5.5) + c(43, 42, 5.5) + p(`M23 29 L17 36 ${ah(16, 37.4, 'd', 2.4)} M33 29 L39 36 ${ah(40, 37.4, 'd', 2.4)}`),
    gold: gd(24, 14, 2.8) + gd(32, 14, 2.8),
  },
  'plc-ip3-dag-pkc': {
    label: 'One membrane lipid cut in two: one half stays in the membrane, one half leaves',
    ink: mem(13) + p(`M24 18 L18 12 M24 12 L18 18`) + p(`M27 15.5 H44 ${ah(45, 15.5, 'r', 2.6)}`) + p(`M21 22 V38 ${ah(21, 39, 'd', 2.6)}`) + p('M10 48 Q21 40 32 48'),
    gold: gd(21, 30, 3.2),
  },
  'calcium-signaling': {
    label: 'A trace of sharp, repeated calcium spikes',
    ink: p('M8 46 V10 M8 46 H50') + p('M9 42 H14 L17 16 L20 42 H26 L29 16 L32 42 H38 L41 16 L44 42 H49'),
    gold: gd(17, 14, 2.6) + gd(29, 14, 2.6) + gd(41, 14, 2.6),
  },
  'turning-signals-off': {
    label: 'An off switch, and a signal falling back to rest',
    ink: p('M19 17 A13 13 0 1 0 37 17') + p('M8 49 H13 C22 49 20 44 28 44 C36 44 38 49 48 49', 'stroke-dasharray="1.5 3.5"'),
    gold: gp('M28 9 V25'),
  },
  'senses-and-cgmp': {
    label: 'An eye, struck by a ray of light',
    ink: p('M7 30 Q28 12 49 30 Q28 48 7 30 Z') + c(28, 30, 7) + p('M40 8 L34 17 M46 12 L39 20'),
    gold: gd(28, 30, 3.2),
  },
  'receptor-tyrosine-kinases': {
    label: 'Two receptors brought together by one signal, each marking the other',
    ink: mem(22) + p('M23 14 V44 M33 14 V44 M19 11 L23 14 M37 11 L33 14'),
    gold: `<rect x="22" y="6" width="12" height="6" rx="3" ${GF} />` + gd(18.5, 38, 2.6) + gd(37.5, 38, 2.6) + gd(18.5, 46, 2.6) + gd(37.5, 46, 2.6),
  },
  'ras-to-mapk': {
    label: 'Three kinases in a row, each switching on the next',
    ink: c(13, 13, 5.5) + c(28, 28, 5.5) + p(`M17.5 17.5 L22.5 22.5 ${ah(23.4, 23.4, 'r', 0)} M20.2 23.6 H23.6 V20.2 M32.5 32.5 L37.5 37.5 M35.2 38.6 H38.6 V35.2`),
    gold: gd(43, 43, 6),
  },
  'pi3k-akt-insulin': {
    label: 'A marked lipid in the membrane, and a kinase that docks on it',
    ink: mem(15) + c(28, 36, 8) + p(`M28 46 V50 ${ah(28, 51, 'd', 2.4)}`),
    gold: gd(28, 23, 3.4) + gp('M24 15 L26 20 M28 14 V19.5 M32 15 L30 20'),
  },
  'mtor-and-ampk': {
    label: 'A balance weighing growth against the energy to pay for it',
    ink: p('M28 14 V40 M20 46 H36 M28 40 L22 46 M28 40 L34 46 M9 20 L47 14') + p('M5 32 Q9.5 37 14 32 M9.5 20 L5 32 M9.5 20 L14 32') + p('M42 27 Q46.5 32 51 27 M46.5 14 L42 27 M46.5 14 L51 27'),
    gold: gd(46.5, 25, 3) + gd(28, 12, 2.6),
  },
  'jak-stat': {
    label: 'A short path: a pair of proteins goes straight from the membrane to the nucleus',
    ink: mem(8) + c(28, 43, 9) + p(`M28 24 V31 ${ah(28, 32, 'd', 2.6)}`),
    gold: gd(24.5, 19, 3.6) + gd(31.5, 19, 3.6),
  },
  'tgf-beta-and-smads': {
    label: 'Three proteins that join into one complex and enter the nucleus',
    ink: c(21, 16, 5) + c(35, 16, 5) + p(`M28 30 V36 ${ah(28, 37, 'd', 2.6)}`) + p('M8 50 Q28 34 48 50'),
    gold: gd(28, 23.5, 5),
  },
  'wnt-signaling': {
    label: 'A protein kept low by constant destruction, and allowed to build up when the signal comes',
    ink: p('M8 46 H49') + `<rect x="13" y="38" width="9" height="8" />` + `<rect x="34" y="18" width="9" height="28" />` + p(`M24 32 L30 26 M27 25.4 H30.6 V29`),
    gold: `<rect x="34" y="12" width="9" height="6" ${GF} />`,
  },
  'notch-signaling': {
    label: 'Two cells touching; a piece cut from the receptor travels to the nucleus',
    ink: `<rect x="5" y="14" width="20" height="28" rx="5" />` + `<rect x="31" y="14" width="20" height="28" rx="5" />` + p('M21 28 H35') + c(43, 34, 3.5),
    gold: gp(`M37 26 L40 30 ${ah(40.6, 30.8, 'd', 0)}`) + gd(37, 24.5, 2.4),
  },
  'hedgehog-and-cilium': {
    label: 'A cell with one thin antenna, and the signal inside it',
    ink: p('M6 48 Q6 32 23 32 V12 Q23 7 28 7 Q33 7 33 12 V32 Q50 32 50 48'),
    gold: gd(28, 14, 3) + gd(28, 24, 2.2),
  },
  'integrins-and-rho-gtpases': {
    label: 'A cell gripping a surface, with fibres pulling between its footholds',
    ink: p('M6 44 H50 M9 48 L12 44 M17 48 L20 44 M25 48 L28 44 M33 48 L36 44 M41 48 L44 44') + p('M10 40 Q12 18 28 18 Q44 18 46 40') + p('M15 38 L26 24 M41 38 L30 24 M17 38 H39'),
    gold: `<rect x="10" y="39" width="8" height="5" ${GF} />` + `<rect x="38" y="39" width="8" height="5" ${GF} />`,
  },
  'tlr-and-nf-kb': {
    label: 'A horseshoe-shaped sensor catching a piece of a microbe, and an alarm going out',
    ink: p('M17 30 V19 A11 11 0 0 1 39 19 V30') + p('M28 38 V46 M19 38 L14 45 M37 38 L42 45') + p('M10 30 H46'),
    gold: `<path d="M28 13 l1.8 4.2 4.4 .5 -3.3 3 1 4.4 -3.9 -2.3 -3.9 2.3 1 -4.4 -3.3 -3 4.4 -.5 z" ${GF} />`,
  },
  'antigen-receptors-and-checkpoints': {
    label: 'One cell showing a fragment to another, with a brake beside the receptor',
    ink: p('M6 9 Q28 19 50 9 M6 47 Q28 37 50 47') + p('M22 14 V20 M19 20 H25') + p('M22 41 V30 M22 30 L18 25 M22 30 L26 25'),
    gold: gp('M36 41 V27 M31 27 H41') + gd(22, 22.6, 2),
  },
  'ion-channels-as-receptors': {
    label: 'A pore through the membrane, with ions streaming through it',
    ink: p('M6 24 H22 M34 24 H50 M6 32 H22 M34 32 H50 M22 18 V38 M34 18 V38'),
    gold: gd(28, 10, 2.6) + gd(28, 20, 2.6) + gd(28, 30, 2.6) + gd(28, 40, 2.6) + gd(22, 47, 2.2) + gd(34, 47, 2.2),
  },
  'nuclear-receptors': {
    label: 'A hormone that enters the cell and meets its receptor on the DNA',
    ink: c(30, 32, 16) + p('M19 36 Q23 31 27 36 T35 36 T43 36') + `<rect x="25" y="24" width="10" height="9" rx="2" />` + p(`M8 8 L17 17 M13.6 17.6 H17.6 V13.6`),
    gold: gd(30, 19.5, 3),
  },
  'signaling-to-the-nucleus': {
    label: 'A signal passing through a pore into the nucleus',
    ink: p('M22 12.6 A17 17 0 1 0 34 12.6') + p('M22 9 V16 M34 9 V16') + p(`M28 4 V20 ${ah(28, 21, 'd', 2.6)}`),
    gold: gd(28, 31, 4),
  },
  'stress-signals': {
    label: 'A warning sign with a tangled, misfolded chain inside it',
    ink: p('M28 8 L49 45 H7 Z') + p('M21 38 Q24 32 28 38 T35 38'),
    gold: gp('M28 20 V28') + gd(28, 32, 1.6),
  },
  'death-receptors-bcl2-caspases': {
    label: 'A cell breaking itself up into small sealed parcels',
    ink: c(25, 31, 13, ) + c(41, 16, 5) + c(46, 34, 3.6) + c(37, 47, 3) + p('M19 26 L24 31 M24 26 L19 31'),
    gold: gd(41, 16, 2) + gd(29, 36, 2.4),
  },
  'shape-of-a-signal': {
    label: 'Two traces of the same signal: one brief, one held',
    ink: p('M8 47 V9 M8 47 H50') + p('M9 42 H14 C18 42 17 22 21 22 C25 22 25 42 30 42 H49', 'stroke-dasharray="1.5 3.5"'),
    gold: gp('M9 42 H14 C18 42 17 16 22 16 H49'),
  },
  'endocytosis-and-signaling-endosomes': {
    label: 'A membrane folding inward and pinching off a vesicle with its cargo',
    ink: p('M6 14 H21 Q24 14 24 18 Q20 28 28 28 Q36 28 32 18 Q32 14 35 14 H50') + c(28, 42, 7) + p(`M28 30 V33`),
    gold: gd(28, 22, 2.6) + gd(28, 42, 3),
  },
  'long-distance-signaling-in-neurons': {
    label: 'A nerve cell with a long axon, and a signal carried back along it',
    ink: c(12, 30, 7) + p('M19 30 H44 M44 30 L50 24 M44 30 L50 36 M7 24 L4 20 M7 36 L4 40 M12 23 V18'),
    gold: gd(36, 30, 3.2) + gp(`M30 22 H22 ${ah(21, 22, 'l', 2.4)}`),
  },
  'exosomes-and-extracellular-vesicles': {
    label: 'Small sealed parcels released by one cell and drifting toward another',
    ink: p('M6 8 Q22 28 6 48 M50 8 Q34 28 50 48') + c(22, 18, 3) + c(26, 38, 3.4) + c(35, 24, 2.6),
    gold: gd(29, 29, 3.6),
  },
  'reverse-signaling': {
    label: 'Two cells in contact, each sending a signal into the other',
    ink: c(11, 28, 7) + c(45, 28, 7) + p(`M20 23 H35 ${ah(36, 23, 'r', 2.6)}`),
    gold: gp(`M36 33 H21 ${ah(20, 33, 'l', 2.6)}`),
  },
  'how-signaling-evolved': {
    label: 'A branching tree of descent',
    ink: p('M28 49 V36 M28 36 L14 24 M28 36 L42 24 M14 24 V12 M14 24 L6 16 M42 24 L36 12 M42 24 L49 14') + c(14, 9, 2.6) + c(6, 13, 2.6) + c(36, 9, 2.6),
    gold: gd(49.5, 11, 3.2),
  },
  'oncogenes': {
    label: 'A switch stuck in the on position',
    ink: `<rect x="9" y="19" width="38" height="18" rx="9" />` + p('M14 45 L20 41 M22 47 L26 42 M17 12 L21 15'),
    gold: gd(38, 28, 6.2),
  },
  'drugs-against-a-part': {
    label: 'A drug shaped to fit one pocket of one protein',
    ink: p('M36.5 16.5 A15 15 0 1 0 39.5 36 L30 28 Z'),
    gold: `<path d="M34 28 L46 20 L46 36 Z" ${GF} />`,
  },
  'detecting-a-signal': {
    label: 'A blot: lanes of bands, one of them picked out',
    ink: `<rect x="8" y="9" width="40" height="38" rx="3" />` + p('M13 18 H21 M24 18 H32 M35 18 H43 M13 27 H21 M35 27 H43 M13 38 H21 M24 38 H32'),
    gold: gp('M24 27 H32') + gp('M35 38 H43'),
  },
  'hacking-the-cell': {
    label: 'Light falling on an engineered channel in a membrane',
    ink: p('M6 30 H22 M34 30 H50 M6 37 H22 M34 37 H50 M22 25 V42 M34 25 V42') + p(`M28 33 V46 ${ah(28, 47, 'd', 2.6)}`),
    gold: gp('M28 6 V17 M17 8 L22 18 M39 8 L34 18'),
  },
};
