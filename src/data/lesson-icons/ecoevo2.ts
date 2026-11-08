import type { IconArt } from '../signaling-icons';

const c = (x: number, y: number, r: number) => `<circle cx="${x}" cy="${y}" r="${r}" />`;
const p = (d: string, extra = '') => `<path d="${d}" ${extra}/>`;
const GF = 'style="fill:var(--ddp-color-secondary)"';
const GS = 'style="stroke:var(--ddp-color-secondary)" fill="none" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"';
const gd = (x: number, y: number, r = 3) => `<circle cx="${x}" cy="${y}" r="${r}" ${GF} />`;
const gp = (d: string, extra = '') => `<path d="${d}" ${GS} ${extra}/>`;
const ah = (x: number, y: number, dir: 'r' | 'l' | 'u' | 'd', s = 3) =>
  dir === 'r' ? `M${x - s} ${y - s} L${x} ${y} L${x - s} ${y + s}`
  : dir === 'l' ? `M${x + s} ${y - s} L${x} ${y} L${x + s} ${y + s}`
  : dir === 'u' ? `M${x - s} ${y + s} L${x} ${y} L${x + s} ${y + s}`
  : `M${x - s} ${y - s} L${x} ${y} L${x + s} ${y - s}`;
/** A small solid ink dot. */
const dot = (x: number, y: number, r = 1.7) => `<circle cx="${x}" cy="${y}" r="${r}" fill="currentColor" stroke="none" />`;

export const ICONS: Record<string, IconArt> = {
  'population-growth': {
    label: 'Two growth curves: one shooting up without limit, the other levelling off at the carrying capacity',
    ink: p('M8 6 V48 H50') + p('M10 46 C24 45 30 36 34 8') + p('M10 46 C24 45 26 22 48 22'),
    gold: gp('M10 18 H50', 'stroke-dasharray="3 3.5"'),
  },
  'spatial-populations': {
    label: 'A landscape of habitat patches, some occupied and some empty, with one disperser moving between them',
    ink: c(12, 13, 6) + c(43, 11, 5) + c(28, 31, 5.5) + c(11, 43, 5) + c(44, 43, 6.5)
      + p(`M34 31 Q40 28 42 21 ${ah(42.6, 20, 'u', 2.6)}`, 'stroke-dasharray="2 3"'),
    gold: gd(12, 13, 4) + gd(44, 43, 4.5) + gd(28, 31, 3.5),
  },

  'competition': {
    label: 'Two species’ lines of zero growth crossing on a graph, the crossing point where both persist',
    ink: p('M8 6 V48 H50') + p('M10 12 L46 44') + p('M10 30 L50 38'),
    gold: gd(33.3, 34.8, 3.6),
  },
  'predation': {
    label: 'Predator and prey numbers cycling around each other in a closed loop',
    ink: p('M8 6 V48 H50') + `<ellipse cx="30" cy="27" rx="16" ry="12" />` + p(ah(27, 15, 'l', 3.4)),
    gold: gd(30, 27, 3.4),
  },

  'mutualism-parasitism-coevolution': {
    label: 'A plant whose roots carry swollen nodules where bacteria live',
    ink: p('M6 26 H50') + p('M28 26 V8 M28 16 Q20 8 15 12 Q21 18 28 16 M28 12 Q35 4 41 8 Q35 14 28 12')
      + p('M28 26 V48 M28 32 Q20 36 14 44 M28 36 Q36 40 42 47'),
    gold: gd(19.5, 37.2, 3) + gd(36.5, 41.3, 3) + gd(28, 44, 2.6),
  },
  'diversity-and-succession': {
    label: 'Grass, then shrubs, then trees growing back over time on cleared ground',
    ink: p('M5 48 H51') + p('M7 48 L9 42 M11 48 V41 M15 48 L13 42')
      + p('M24 48 V40') + c(24, 35, 5.5)
      + p('M42 48 V30') + p('M42 10 L34 30 H50 Z'),
    gold: gp(`M8 34 Q20 14 33 16 ${ah(33.5, 16, 'r', 2.8)}`),
  },
  'island-biogeography': {
    label: 'A small island with a palm tree, new species arriving across the sea',
    ink: p('M22 44 Q36 32 50 44') + p('M37 38 Q35 28 38 18 M38 18 Q32 13 26 16 M38 18 Q44 12 50 15 M38 18 Q34 21 29 25 M38 18 Q43 21 47 26')
      + p('M4 48 Q8 45 12 48 T20 48 T28 48 T36 48 T44 48 T52 48'),
    gold: gp(`M5 34 H21 ${ah(22, 34, 'r', 3.2)}`, 'stroke-dasharray="0"') + gd(6, 34, 2.4),
  },

  'energy-flow': {
    label: 'A pyramid of trophic levels, each smaller than the one below, with sunlight entering at the base',
    ink: `<rect x="6" y="38" width="44" height="10" rx="1.5" />` + `<rect x="14" y="26" width="28" height="10" rx="1.5" />`
      + `<rect x="22" y="14" width="12" height="10" rx="1.5" />`,
    gold: gd(45, 12, 4.5) + gp('M45 3 V5 M54 12 H52 M51.4 5.6 L50 7 M38.6 5.6 L40 7 M51.4 18.4 L50 17'),
  },

  'nutrient-cycling': {
    label: 'A tree and the soil beneath it joined by a loop: nutrients taken up by the roots and returned as fallen leaves',
    ink: p('M6 40 H50') + p('M28 40 V27 M28 32 L23 27 M28 30 L33 25') + p('M20 26 Q14 25 16 18 Q15 10 23 10 Q27 4 33 9 Q41 9 40 17 Q43 25 36 26 Z')
      + p('M28 40 L24 46 M28 40 L32 46'),
    gold: gp(`M44 14 Q53 28 44 44 ${ah(44.4, 44, 'd', 3)}`) + gp(`M12 44 Q3 28 12 14 ${ah(12, 13.6, 'u', 3)}`),
  },

  'biodiversity-ecosystem-function': {
    label: 'Two plots: one sown with a single species, the other with several, which grows more',
    ink: `<rect x="5" y="30" width="20" height="18" rx="1.5" />` + `<rect x="31" y="30" width="20" height="18" rx="1.5" />`
      + c(11, 36, 2.5) + c(19, 36, 2.5) + c(11, 43, 2.5) + c(19, 43, 2.5)
      + c(37, 36, 2.5) + p('M42 33.5 L45.5 39 H38.5 Z M47 40 V46 M44 43 H50') + dot(37, 44, 1.8),
    gold: gp(`M41 25 V8 ${ah(41, 8, 'u', 3.5)}`),
  },
  'global-change': {
    label: 'A mountain with a band of temperature moving up its slope over time',
    ink: p('M4 48 L28 10 L52 48 Z') + p('M13 34 H43', 'stroke-dasharray="2 3"'),
    gold: gp('M18.5 26 H37.5') + gp(`M46 40 V22 ${ah(46, 22, 'u', 3)}`),
  },
  'conservation': {
    label: 'A shield protecting a young tree',
    ink: p('M28 6 L47 12 V27 C47 39 38 46 28 50 C18 46 9 39 9 27 V12 Z') + p('M28 42 V28 M28 34 L23 30'),
    gold: gd(28, 23, 6.5),
  },
  'ecoevo-evidence-workshop': {
    label: 'A water sample drawn from a pond, with a question mark: no detection is not proof of absence',
    ink: `<ellipse cx="28" cy="48" rx="22" ry="4" />` + p('M18 4 H38 M20 4 V33 Q20 41 28 41 Q36 41 36 33 V4') + p('M20 13 Q24 11 28 13 T36 13'),
    gold: gp('M23.5 21 Q23.5 16.5 28 16.5 Q32.5 16.5 32.5 21 Q32.5 24.5 28 26.5 V29.5') + gd(28, 35, 2.2),
  },



};
