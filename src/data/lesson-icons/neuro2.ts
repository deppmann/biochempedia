import type { IconArt } from '../signaling-icons';

const c = (x: number, y: number, r: number) => `<circle cx="${x}" cy="${y}" r="${r}" />`;
const p = (d: string, extra = '') => `<path d="${d}" ${extra}/>`;
const GF = 'style="fill:var(--ddp-color-secondary)"';
const GS = 'style="stroke:var(--ddp-color-secondary)" fill="none" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"';
const gd = (x: number, y: number, r = 3) => `<circle cx="${x}" cy="${y}" r="${r}" ${GF} />`;
const gp = (d: string) => `<path d="${d}" ${GS} />`;
const dot = (x: number, y: number, r = 2.4) => `<circle cx="${x}" cy="${y}" r="${r}" fill="currentColor" stroke="none" />`;
const ah = (x: number, y: number, dir: 'r' | 'l' | 'u' | 'd', s = 3) =>
  dir === 'r' ? `M${x - s} ${y - s} L${x} ${y} L${x - s} ${y + s}`
  : dir === 'l' ? `M${x + s} ${y - s} L${x} ${y} L${x + s} ${y + s}`
  : dir === 'u' ? `M${x - s} ${y + s} L${x} ${y} L${x + s} ${y + s}`
  : `M${x - s} ${y - s} L${x} ${y} L${x + s} ${y - s}`;
const DASH = 'stroke-dasharray="1.5 3.5"';
/** A simple side-view brain outline. */
const BRAIN = 'M10 34 C5 26 9 13 21 10 C29 6 41 8 46 16 C51 22 50 32 44 36 C40 39 34 38 30 40 L28 47 L24 41 C18 41 13 39 10 34 Z';

export const ICONS: Record<string, IconArt> = {
  'motor-units-reflexes': {
    label: 'A leg hanging from the knee, tapped below the kneecap so the lower leg kicks forward',
    ink: p('M5 16 H27 M27 16 V44 H35') + c(27, 16, 3) + p(`M33 50 Q46 46 47 32 ${ah(47.2, 31, 'u', 2.6)}`),
    gold: gp('M50 8 L36 22') + `<rect x="30" y="20" width="10" height="6" rx="2" transform="rotate(-45 35 23)" ${GF} />`,
  },
  'basal-ganglia': {
    label: 'A loop of three stations in which one link brakes the next',
    ink: c(28, 11, 5.5) + c(12, 42, 5.5) + c(44, 42, 5.5)
      + p('M24.5 15.5 L15.5 36 M13 32.4 L15.5 36 L19 33.4') + p(`M18 42 H37 ${ah(38, 42, 'r', 2.6)}`),
    gold: gp('M41.5 37 L32 18.3 M28.4 20.1 L35.6 16.5'),
  },
  'cerebellum': {
    label: 'A Purkinje cell with its flat fan of dendrites, crossed by parallel fibres',
    ink: c(28, 40, 4.5) + p('M28 44.5 V51 M28 35.5 V27 M28 27 L18 18 M28 27 L38 18 M18 18 L12 8 M18 18 L21 7 M38 18 L35 7 M38 18 L44 8 M28 27 V7')
      + p('M6 13 H50', DASH),
    gold: gp('M6 21 H50'),
  },
  'hypothalamus-autonomic': {
    label: 'A gauge whose needle is held at a set point by feedback',
    ink: p('M8 36 A20 20 0 0 1 48 36') + p('M8 36 H48') + p('M28 36 L19 22') + dot(28, 36, 2.6)
      + p(`M14 45 Q28 53 42 45 ${ah(42.5, 44.6, 'u', 0)}`) + p(ah(42, 45, 'r', 2.6)),
    gold: gp('M28 12 V18'),
  },
  'motivation-and-reward': {
    label: 'A dopamine neuron firing a burst at the cue that predicts a drop of reward',
    ink: p('M6 44 H14 L16 40 L18 44 H22 L24 41 L26 44 H40 L42 41 L44 44 H50') + p('M43 10 C43 10 37 18 37 22 A6 6 0 0 0 49 22 C49 18 43 10 43 10 Z'),
    gold: gp('M24 44 L26 14 L28 44 L30 18 L32 44'),
  },
  'emotion-and-stress': {
    label: 'A tone from a speaker paired with a shock: a learned threat',
    ink: p('M7 22 H13 L21 15 V41 L13 34 H7 Z') + p('M26 22 Q29 28 26 34 M31 18 Q36 28 31 38'),
    gold: `<path d="M44 8 L36 29 H43 L39 48 L50 24 H43 L47 8 Z" ${GF} />`,
  },
  'sleep-and-rhythms': {
    label: 'A crescent moon over a night of sleep stages stepping up and down',
    ink: p('M6 30 H14 V38 H20 V46 H28 V34 H34 V42 H42 V30 H50'),
    gold: `<path d="M30 6 A11 11 0 1 0 42 20 A8.5 8.5 0 1 1 30 6 Z" ${GF} />`,
  },
  'memory-systems': {
    label: 'Memory divided into branches like a family tree, one branch marked',
    ink: `<rect x="21" y="6" width="14" height="9" rx="2" />` + p('M28 15 V22 M11 22 H45 M11 22 V31 M28 22 V31 M45 22 V31')
      + `<rect x="5" y="31" width="12" height="9" rx="2" />` + `<rect x="39" y="31" width="12" height="9" rx="2" />`,
    gold: `<rect x="22" y="31" width="12" height="9" rx="2" ${GS} />`,
  },
  'memory-consolidation': {
    label: 'A rat’s path wandering around a square arena, with one place field where a cell fires',
    ink: `<rect x="6" y="6" width="44" height="44" rx="3" />` + p('M12 44 C14 30 24 40 26 30 C28 18 14 22 16 13 C18 8 30 10 34 16 C38 22 44 18 44 28 C44 38 34 36 32 44', 'stroke-width="1.4"'),
    gold: gd(36, 20, 6),
  },
  'language': {
    label: 'A side view of the brain with two language areas joined by a pathway',
    ink: p(BRAIN),
    gold: gd(18, 26, 3.4) + gd(37, 29, 3.4) + gp('M20 22.5 Q28 14 35 25.5'),
  },
  'attention-and-decisions': {
    label: 'Evidence drifting noisily upward until it reaches a decision bound',
    ink: p('M6 12 H50 M6 44 H50', DASH) + p('M6 28 L10 25 L13 30 L17 24 L20 26 L24 20 L27 23 L31 17 L34 19 L38 13'),
    gold: gd(39, 12, 3.6),
  },
  'neurodegeneration': {
    label: 'A neuron with a protein clump inside it, its axon breaking into pieces',
    ink: c(16, 18, 9) + p('M9.5 12 Q6 9 6 4 M7 7.5 L3 7 M17 9 Q19 6 18 3 M22.5 12 Q27 10 30 6 M26 10 L28 13') + p('M23 24 L28 30') + p('M31 33 L35 37 M38 40 L41 43 M44 46 L47 49'),
    gold: gd(14.5, 17, 2.8) + gd(18.5, 20, 2.4) + gd(17.5, 15, 2),
  },
  'large-scale-neuroscience': {
    label: 'A camera’s field of view filled with many neurons, one of them lighting up',
    ink: `<rect x="5" y="5" width="46" height="46" rx="6" />` + c(15, 15, 3.6) + c(29, 13, 3.6) + c(42, 17, 3.6) + c(13, 30, 3.6) + c(41, 32, 3.6) + c(16, 43, 3.6) + c(30, 41, 3.6) + c(43, 44, 3.6),
    gold: gd(27, 28, 4.6),
  },
  'circuit-experiment-design': {
    label: 'An optical fibre shining light onto one neuron to test what it does',
    ink: `<rect x="23" y="4" width="10" height="16" rx="2" />` + c(28, 41, 6) + p('M22 41 H8 M34 41 H48 M28 47 V52'),
    gold: `<path d="M24 22 H32 L40 33 H16 Z" style="fill:var(--ddp-color-secondary);opacity:.55" />` + gp('M24 22 L16 33 M32 22 L40 33'),
  },
};
