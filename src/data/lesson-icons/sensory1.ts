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
const blade = 'M30.5 22.5 C34 14 41 9.5 49.5 8.5 C46 14.5 40.5 20 33.5 25.5 Z';

export const ICONS: Record<string, IconArt> = {
  'transduction-strategies': {
    label: 'Two ways to turn a stimulus into current: a channel pulled open directly by a tether, and a receptor that works through a messenger cascade',
    ink: p('M3 22 H9.5 M24.5 22 H30 M44 22 H53 M3 34 H9.5 M24.5 34 H30 M44 34 H53')
      + `<rect x="9.5" y="18" width="5" height="20" rx="2" /><rect x="19.5" y="18" width="5" height="20" rx="2" />`
      + p('M12 18 L8 7 M5 9 L8 7 L10 10')
      + p('M30 20 L32.3 36 L34.6 20 L36.9 36 L39.2 20 L41.5 36 L44 20')
      + c(37, 44.5, 3.4) + p('M37 48 L32 53 M37 48 L42 53'),
    gold: gd(37, 11, 3.2) + gd(17, 29, 2) + gp(`M17 40 V47 ${ah(17, 48, 'd', 2.6)}`),
  },
  'mechanotransduction-channels': {
    label: 'A Piezo channel seen from above: three long curved blades sweeping out from a central pore',
    ink: `<g>${p(blade)}<g transform="rotate(120 28 28)">${p(blade)}</g><g transform="rotate(240 28 28)">${p(blade)}</g></g>` + c(28, 28, 6.2),
    gold: gd(28, 28, 3.2),
  },
  'sensory-neuron-atlas': {
    label: 'A dorsal root ganglion opened up: sensory cell bodies of many sizes, one type picked out in gold, the nerve running in and out',
    ink: `<ellipse cx="28" cy="28" rx="19" ry="14" />` + p('M3 28 H9 M47 28 H53')
      + c(19, 23, 4.6) + c(33, 20, 3) + c(39, 31, 4.2) + c(25, 35, 2.4) + c(16, 33, 2.6) + c(41, 22, 2),
    gold: `<circle cx="29.5" cy="28.5" r="3.4" ${GS} />` + gd(29.5, 28.5, 1.3),
  },
  'ltmr-classes': {
    label: 'Three touch fibres rising to the skin, each with its own kind of ending: a thick myelinated one in gold, a thinner myelinated one and a bare one',
    ink: p('M3 9 H53')
      + p('M14 53 V14 M11 12 Q14 16 17 12')
      + p('M28 53 V14 M28 17 L24 12.5 M28 17 L32 12.5')
      + `<rect x="25.8" y="24" width="4.4" height="6" rx="2" /><rect x="25.8" y="35" width="4.4" height="6" rx="2" />`
      + p('M42 53 V16 M42 16 L39 12 M42 16 L45 12 M42 16 V11.5'),
    gold: `<rect x="10.5" y="20" width="7" height="9" rx="3" ${GF} /><rect x="10.5" y="33" width="7" height="9" rx="3" ${GF} />`,
  },
  'merkel-cells': {
    label: 'Two Merkel cells with fine finger-like tips sitting on the gold disc-shaped ending of a touch fibre',
    ink: p('M3 8 C13 4.5 21 11.5 29 8 C37 4.5 45 11.5 53 8')
      + c(20, 26, 5.2) + c(36, 26, 5.2)
      + p('M16.5 22.2 L14.5 19 M20 20.8 V17 M23.5 22.2 L25.5 19 M32.5 22.2 L30.5 19 M36 20.8 V17 M39.5 22.2 L41.5 19'),
    gold: `<rect x="13" y="32.4" width="30" height="3.6" rx="1.8" ${GF} />` + gp('M28 36 C28 42 25 46 26 53'),
  },
  'vibration-corpuscles': {
    label: 'A Pacinian corpuscle: layers of capsule wrapped like an onion around a gold nerve ending, with a vibration beside it',
    ink: `<ellipse cx="26" cy="25" rx="13" ry="20" /><ellipse cx="26" cy="25" rx="9" ry="14.5" /><ellipse cx="26" cy="25" rx="5" ry="9" />`
      + p('M26 45 V53') + p('M42 12 q2.5 -3.5 5 0 t5 0'),
    gold: gp('M26 17 V45'),
  },
  'hairy-skin-and-affective-touch': {
    label: 'A hair in its follicle, ringed by a palisade of nerve endings, with a gold arrow for a slow gentle stroke across the skin',
    ink: p('M3 20 H53') + p('M28 20 L34 4') + p('M23.5 20 V38 Q28 44 32.5 38 V20')
      + p('M18.5 24 V36 M37.5 24 V36 M15 26 V34 M41 26 V34') + p('M15 34 C16 44 40 44 41 34') + p('M28 43 C28 47 25 50 24 53'),
    gold: gp(`M5 15 C10 11 16 11 21 13 ${ah(21.5, 13.2, 'r', 2.6)}`),
  },
  'dorsal-horn-touch': {
    label: 'The dorsal horn drawn as stacked layers, a gold touch fibre curving past the outer layers to branch in the deeper ones',
    ink: p('M8 15 Q28 5 48 15') + p('M10 22 Q28 13 46 22') + p('M12 29 Q28 21 44 29') + p('M14 37 Q28 30 42 37') + p('M17 45 Q28 39 39 45'),
    gold: gp('M3 5 C10 1.5 18 2 21 9 C24 17 25 25 27 33') + gp('M27 33 L22.5 37 M27 33 L31.5 37 M27 33 V39'),
  },
  'touch-in-autism-models': {
    label: 'A mouse reacting to a light touch on its back, the gold ripples drawn far larger than the touch itself',
    ink: p('M10 41 C9 31 19 25 30 26 C39 27 45 31 48 36 L52 39 C50 42 46 43 42 43 L13 43 C11 43 10 42 10 41 Z')
      + c(40, 30, 3.2) + dot(46, 36, 1.3) + p('M10 41 C4 41 3 47 7 50') + p('M18 43 V46 M36 43 V46'),
    gold: gd(26, 22.5, 2) + gp('M19 19 Q26 13.5 33 19') + gp('M14 14 Q26 4.5 38 14', 'opacity="0.55"'),
  },
  thermosensation: {
    label: 'Two channels in the membrane, one opened by heat (a gold flame) and one by cold (a snowflake)',
    ink: p('M3 32 H11 M23 32 H33 M45 32 H53 M3 40 H11 M23 40 H33 M45 40 H53')
      + `<rect x="11" y="28" width="4.6" height="16" rx="2" /><rect x="18.4" y="28" width="4.6" height="16" rx="2" />`
      + `<rect x="33" y="28" width="4.6" height="16" rx="2" /><rect x="40.4" y="28" width="4.6" height="16" rx="2" />`
      + p('M39 6 V22 M32 10 L46 18 M32 18 L46 10 M36.5 6.5 L39 9 L41.5 6.5 M36.5 21.5 L39 19 L41.5 21.5'),
    gold: `<path d="M17 5 C21.5 9.5 23.5 13 22.5 17 C21.5 21 12.5 21 11.5 17 C11 13 13.5 11 14.5 9 C15.5 11 16.5 12 17 12 C17.5 10 17.5 7.5 17 5 Z" ${GF} />`,
  },
  'nociceptors-and-sodium-channels': {
    label: 'A sodium channel seen from above: four voltage-sensing domains around a pore with a gold sodium ion in it, the Nav1.7 channel that pain fibres depend on',
    ink: c(18, 18, 7.5) + c(38, 18, 7.5) + c(18, 38, 7.5) + c(38, 38, 7.5)
      + p('M15 18 H21 M18 15 V21 M35 18 H41 M38 15 V21 M15 38 H21 M18 35 V41 M35 38 H41 M38 35 V41'),
    gold: gd(28, 28, 3.4),
  },
  'spinal-pain-circuits': {
    label: 'The pain gate: a touch fibre drives a gold inhibitory cell that holds back the neuron carrying a pain fibre\'s signal up to the brain',
    ink: c(40, 32, 5.5) + p(`M44 28 L51 19 ${ah(51.5, 18.5, 'u', 2.8)}`)
      + p('M3 48 C16 48 27 42 35 35') + p('M3 9 C13 9 18 12 21 17') + p('M8 9 V5 M13 9.3 V5.5'),
    gold: gd(23.5, 20.5, 3.6) + gp('M27 23 L34.5 28.5 M33 30.5 L36.4 26'),
  },
  itch: {
    label: 'A mast cell under a raised patch of skin releasing gold granules onto a nearby itch fibre',
    ink: p('M3 12 H17 C21 5.5 31 5.5 35 12 H53') + c(17, 31, 7.5)
      + dot(14.5, 29, 1.4) + dot(19, 33.5, 1.4) + dot(14.5, 34, 1.4) + dot(19.5, 28, 1.4)
      + p('M50 53 C43 45 39 36 36 24 M36 24 L32 18.5 M36 24 L38 17.5'),
    gold: gd(27.5, 25.5, 1.8) + gd(30.5, 30.5, 1.8) + gd(27.5, 35, 1.8),
  },
  'chronic-pain': {
    label: 'Pain plotted against stimulus strength: after injury the gold curve shifts left, so a light touch now hurts',
    ink: p('M7 6 V49 H52') + p('M9 47 C25 47 29 41 33 27 C36 16 41 13 50 13') + p('M17 49 V20', DASH),
    gold: gp('M9 47 C13 47 15.5 41 19 27 C22 16 27 13 36 13'),
  },
  proprioception: {
    label: 'A muscle spindle: a gold sensory ending coiled around the middle of the fibres inside the capsule, its axon leaving below',
    ink: p('M3 28 C14 19 42 19 53 28 C42 37 14 37 3 28 Z') + p('M10 26 H46 M10 30 H46') + p('M28 35 C28 42 32 47 30 53'),
    gold: gp('M19 22 C19 34 22 34 22 22 C22 34 25 34 25 22 C25 34 28 34 28 22 C28 34 31 34 31 22 C31 34 34 34 34 22 C34 34 37 34 37 22'),
  },
};

export const COURSE: Record<string, IconArt> = { 'course:sensory-systems': {
  label: 'A sensory neuron: its cell body sits on a short stem, one branch reaching down to a gold receptive ending that picks up a stimulus, the other running on toward the spinal cord',
  ink: c(31, 11, 6.5) + p('M31 17.5 V26') + p(`M14 38 C14 30 17 26 25 26 H50 ${ah(51, 26, 'r', 3)}`)
    + `<rect x="36" y="23.5" width="8" height="5" rx="2.5" />`,
  gold: gp('M14 38 L9 43.5 M14 38 V45 M14 38 L19 43.5')
    + gp('M6 51 Q14 47.5 22 51', 'opacity="0.7"') + gp('M3 55 Q14 50.5 25 55', 'opacity="0.4"'),
} };
