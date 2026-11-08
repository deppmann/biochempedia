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

export const ICONS: Record<string, IconArt> = {
  'nervous-system-map': {
    label: 'A side view of the brain with the spinal cord running down from it and nerves branching off the cord to one side',
    ink: p('M10 25 C3 21 4 10 14 6.5 C22 4 34 4 41 8 C47 12 47 20 43 23.5 C40 26 36 26 33 25 C29 28 21 28 16 27 C14 26.5 12 26 10 25 Z')
      + p('M14 18 C20 15 26 16 32 13.5') + p('M36.5 25.5 C38.5 29.5 44 29 44 23')
      + p('M34 34 L44 37 L51 42 M34.5 42 L45 46 M35 49.5 L43 52'),
    gold: gp('M33 25.5 C33 34 34.5 42 35 52'),
  },
  'neurons-and-glia-at-work': {
    label: 'A neuron whose axon is wrapped in two myelin sheaths, the spike starting at the segment next to the cell body',
    ink: c(11, 28, 5.5) + p('M7 24 L4 19 M7.5 32 L4 37 M10.5 22.5 L10 17 M16.5 28 H48 M48 28 L52 23.5 M48 28 L52 32.5')
      + `<rect x="24" y="24" width="10" height="8" rx="3" /><rect x="37" y="24" width="10" height="8" rx="3" />`,
    gold: `<rect x="16" y="25.5" width="6.5" height="5" rx="2.5" ${GF} />`,
  },
  'resting-membrane-passive': {
    label: 'The membrane drawn as a circuit: a resistor and a battery in one branch, a capacitor in the other',
    ink: p('M10 10 H46 M10 46 H46') + p('M18 10 V14 L14 16.5 L22 20 L14 23.5 L22 27 L18 29.5 V33 M18 38 V46')
      + p('M38 10 V24 M31 24 H45 M31 30 H45 M38 30 V46'),
    gold: gp('M11 33 H25 M14.5 38 H21.5'),
  },
  'action-potential': {
    label: 'One action potential rising past a dashed threshold line, overshooting and dipping below rest before it recovers',
    ink: p('M6 7 V50 H51') + p('M9 30 H51', DASH),
    gold: gp('M9 39 H17 C19 39 20 37 21 33 L25 9 C25.6 6.5 27.2 6.5 28 9 L32 39 C33 45 35 45.5 38 44.5 C42 43 45 40 50 40'),
  },
  'synaptic-transmission': {
    label: 'A nerve terminal full of vesicles, one of them fusing and releasing its packet of transmitter toward the next cell',
    ink: p('M12 5 V19 C12 32 44 32 44 19 V5') + c(20, 14, 3.4) + c(30, 11, 3.4) + c(37, 18, 3.4) + p('M7 44 Q28 38 49 44'),
    gold: gp('M23.8 28.6 A4 4 0 1 1 32.2 28.6') + gd(24, 36, 1.8) + gd(28, 37.5, 1.8) + gd(32, 36, 1.8),
  },
  'transmitter-systems': {
    label: 'A drug sitting in a receptor\'s binding pocket, keeping the transmitter above from reaching it',
    ink: p('M5 26 H19 V38 H37 V26 H51 M5 46 H51') + c(28, 9, 4) + p(`M28 14.5 V19 ${ah(28, 20, 'd', 2.4)}`),
    gold: `<rect x="21.5" y="25.5" width="13" height="10" rx="2" ${GF} />`,
  },
  'synaptic-integration': {
    label: 'Two excitatory inputs and one inhibitory input converging on a cell body, which sends one output down its axon',
    ink: c(28, 31, 7) + p('M5 12 L21 25.5 M5 50 L21.5 36.5') + dot(22.2, 26.4, 2.4) + dot(22.6, 35.6, 2.4)
      + p(`M35 31 H48 ${ah(49, 31, 'r', 3)}`),
    gold: gp('M28 4 V20 M23 20.5 H33'),
  },
  'synaptic-plasticity': {
    label: 'Responses measured over time jump to a higher level after a brief burst of stimulation and stay there',
    ink: p('M7 7 V49 H51') + dot(12, 38) + dot(17, 38) + dot(22, 38) + dot(32, 21) + dot(37, 22) + dot(42, 21) + dot(47, 22),
    gold: gp('M24 10 V17 M27 10 V17 M30 10 V17'),
  },
  'sensory-coding': {
    label: 'A weak, a medium and a strong stimulus, each coded as a train of spikes that grows denser with strength',
    ink: p('M22 9 V19 M33 9 V19 M44 9 V19')
      + p('M20 23 V33 M26 23 V33 M32 23 V33 M38 23 V33 M44 23 V33 M50 23 V33')
      + p('M20 37 V47 M23.5 37 V47 M27 37 V47 M30.5 37 V47 M34 37 V47 M37.5 37 V47 M41 37 V47 M44.5 37 V47 M48 37 V47 M51.5 37 V47'),
    gold: gd(9, 14, 1.8) + gd(9, 28, 3) + gd(9, 42, 4.4),
  },
  retina: {
    label: 'Light striking a rod photoreceptor, which passes its signal through a bipolar cell to a ganglion cell and out along its axon',
    ink: `<rect x="22.5" y="5" width="11" height="17" rx="5.5" />` + p('M28 22 V26') + c(28, 30, 4) + p('M28 34 V37') + c(28, 42.5, 5.5)
      + p(`M33.5 42.5 H48 ${ah(49, 42.5, 'r', 2.8)}`),
    gold: gp('M6 8 L16 12 M6 17 L16 17'),
  },
  'visual-cortex': {
    label: 'An elongated receptive field with flanking zones, a tilted bar of light lying along its long axis',
    ink: `<g transform="rotate(35 28 28)"><ellipse cx="28" cy="28" rx="13" ry="22" />${p('M21 15 V41 M35 15 V41', 'stroke-dasharray="2 3.5"')}</g>`,
    gold: `<g transform="rotate(35 28 28)"><path d="M28 11 V45" style="stroke:var(--ddp-color-secondary)" fill="none" stroke-width="4" stroke-linecap="round" /></g>`,
  },
  'hearing-and-balance': {
    label: 'A hair cell topped by a staircase of stiff hairs, linked at their tips and bent by a push',
    ink: `<rect x="13" y="31" width="30" height="19" rx="8" />` + p('M19 31 V24 M25 31 V19 M31 31 V14 M37 31 V9')
      + p(`M42 13 H50 ${ah(51, 13, 'r', 2.6)}`),
    gold: gp('M19 24 L25 19 M25 19 L31 14 M31 14 L37 9'),
  },
  'touch-and-pain': {
    label: 'A sharp pin pressing on the skin above the branched endings of a pain fibre',
    ink: p('M4 23 Q14 19 24 23 Q34 27 44 23 Q49 21 52 22') + p('M28 52 V39 M28 39 L19 30 M28 39 V29 M28 39 L37 30'),
    gold: gp('M28 7 V18 M25 15 L28 19 L31 15') + gd(28, 6, 2.6),
  },
  'smell-and-taste': {
    label: 'A taste bud of tall receptor cells opening through a pore, with chemicals arriving at it',
    ink: p('M24.5 18 C12 20 8 36 14 47 H42 C48 36 44 20 31.5 18') + p('M21 46 C18 36 21 27 25.5 21 M35 46 C38 36 35 27 30.5 21 M28 46 V22')
      + p('M21 47 V52 M35 47 V52'),
    gold: gd(23, 8, 2.2) + gd(33, 6, 2.2) + gd(28, 12.5, 2.2),
  },
};

export const COURSE: Record<string, IconArt> = { 'course:neuroscience': {
    label: 'A side view of the brain with a nerve impulse running through it',
    ink: p('M10 38 C2 32 3 15 15 9 C25 4 41 5 48 12 C54 18 54 30 49 34 C46 37 41 37 37 36 C34 41 25 42 18 40 C15 39 12 39 10 38 Z')
      + p('M34 40 L37 52') + p('M39 36.6 C42 42.5 50 41.5 50.5 33.5'),
    gold: gp('M9 25 H20 L24 13 L28 34 L31 25 H47'),
  } };
