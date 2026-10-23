import type { IconArt } from '../signaling-icons';

/* Card icons for the grade 7 Life Science course (Virginia SOL), Units 5 to 8.
   Same engraving hand as signaling-icons.ts: 56 x 56, navy ink, gold accent, concrete pictures a
   12-year-old recognises at a glance. */

const c = (x: number, y: number, r: number) => `<circle cx="${x}" cy="${y}" r="${r}" />`;
const p = (d: string, extra = '') => `<path d="${d}" ${extra}/>`;
const GF = 'style="fill:var(--ddp-color-secondary)"';
const GS = 'style="stroke:var(--ddp-color-secondary)" fill="none" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"';
const gd = (x: number, y: number, r = 3) => `<circle cx="${x}" cy="${y}" r="${r}" ${GF} />`;
const gp = (d: string, extra = '') => `<path d="${d}" ${GS} ${extra}/>`;
const dot = (x: number, y: number, r = 2.2) => `<circle cx="${x}" cy="${y}" r="${r}" fill="currentColor" stroke="none" />`;

/** A five-petal flower centred on (x, y). */
const flower = (x: number, y: number, gold = false) => {
  const pet = Array.from({ length: 5 }, (_, i) => {
    const a = (i * 72 - 90) * Math.PI / 180;
    const px = +(x + 5.2 * Math.cos(a)).toFixed(1), py = +(y + 5.2 * Math.sin(a)).toFixed(1);
    return gold ? `<circle cx="${px}" cy="${py}" r="3.6" ${GF} />` : c(px, py, 3.6);
  }).join('');
  return pet + (gold ? '' : dot(x, y, 1.6));
};
/** An oak leaf pointing up with its base at (x, y), scaled by s. */
const oak = (x: number, y: number, s: number, extra = '') =>
  `<path d="M0 14 C-5 12 -4 9 -7 8 C-4 6 -6 3 -8 0 C-4 0 -3 -3 -5 -6 C-2 -5 -1 -7 0 -12 C1 -7 2 -5 5 -6 C3 -3 4 0 8 0 C6 3 4 6 7 8 C4 9 5 12 0 14 Z M0 14 V4" transform="translate(${x} ${y - 14 * s}) scale(${s})" ${extra} vector-effect="non-scaling-stroke" />`;
/** A moth with its body at (x, y). */
const moth = (x: number, y: number, extra = '') => {
  const half = 'M-1.6 -4 C-6 -11 -14 -8 -14 -2 C-9 1 -4 1 -1.6 0 Z M-1.6 1 C-10 2 -13 9 -9 12 C-4 12 -2 7 -1.6 3 Z';
  return `<g transform="translate(${x} ${y}) scale(1.05)" ${extra}><path d="${half}" /><path d="${half}" transform="scale(-1 1)" /><path d="M0 -6 C-2.2 -6 -2.2 11 0 11 C2.2 11 2.2 -6 0 -6 Z M-1 -7 L-4 -12 M1 -7 L4 -12" /></g>`;
};
/** A scalloped, frilly lichen patch. */
const rosette = (cx = 28, cy = 28, R = 19, n = 10) => {
  const rr = +(R * Math.sin(Math.PI / n) * 1.15).toFixed(1), pts = Array.from({ length: n + 1 }, (_, i) => {
    const a = (i / n) * 2 * Math.PI;
    return [+(cx + R * Math.cos(a)).toFixed(1), +(cy + R * Math.sin(a)).toFixed(1)];
  });
  return `M${pts[0][0]} ${pts[0][1]}` + pts.slice(1).map(([x, y]) => ` A ${rr} ${rr} 0 0 1 ${x} ${y}`).join('') + ' Z';
};
/** A four-petal floret. */
const floret = (x: number, y: number) => c(x, y, 4.6);
/** Hydrangea florets packed into a ball, centred (28, 22). */
const ball = () => {
  const out: [number, number][] = [];
  for (let row = -2; row <= 2; row++) for (let col = -3; col <= 3; col++) {
    const x = 28 + col * 10.5 + (row % 2 ? 5.25 : 0), y = 22 + row * 9.2;
    if (Math.hypot(x - 28, y - 22) <= 17) out.push([x, y]);
  }
  return out;
};

export const ICONS: Record<string, IconArt> = {
  'predators-and-prey': {
    label: 'A wolf paw print beside the gold cloven hoof print of the moose it hunts',
    ink: `<ellipse cx="17" cy="42" rx="7" ry="5.5" />` + `<ellipse cx="8" cy="31" rx="2.8" ry="3.8" transform="rotate(-25 8 31)" />` + `<ellipse cx="14" cy="25" rx="2.8" ry="3.8" />` + `<ellipse cx="21" cy="25" rx="2.8" ry="3.8" />` + `<ellipse cx="27" cy="31" rx="2.8" ry="3.8" transform="rotate(25 27 31)" />`,
    gold: `<path d="M34 11 C28 13 28 28 33 39 C38 37 39 28 39 22 C39 15 38 11 34 11 Z M48 11 C54 13 54 28 49 39 C44 37 43 28 43 22 C43 15 44 11 48 11 Z" ${GF} />`,
  },
  'competition-and-cooperation': {
    label: 'A test tube holding two kinds of paramecium, one in gold, as in Gause\'s crowded tube',
    ink: p('M20 6 V40 a8 8 0 0 0 16 0 V6 M16 6 H40') + p('M20 17 H36', 'opacity="0.55"')
      + `<ellipse cx="27" cy="44" rx="5.5" ry="3" transform="rotate(-20 27 44)" />` + c(32, 36, 1.2),
    gold: `<ellipse cx="29" cy="28" rx="5" ry="2.8" transform="rotate(20 29 28)" ${GF} />`,
  },
  'living-together-symbiosis': {
    label: 'A branch with frilly leafy lichen patches growing on its bark, one patch in gold, a fungus and an alga living as one',
    ink: p('M3 36 H46 M3 44 H46') + `<ellipse cx="46" cy="40" rx="3" ry="4" />` + p('M12 40 V42 M22 38 V43 M38 39 V42', 'opacity="0.55"') + p(rosette(13, 28, 6.5, 8)) + p(rosette(46, 28, 6, 8)),
    gold: gp(rosette(29, 26, 9, 10)) + gd(29, 26, 2),
  },
  'habitat-and-niche': {
    label: 'A spruce tree with a small gold warbler perched at its own level among the branches',
    ink: p('M24 4 L16 18 H21 L12 32 H19 L8 48 H40 L29 32 H36 L27 18 H32 Z') + p('M24 48 V53'),
    gold: `<ellipse cx="46" cy="27" rx="4.8" ry="3.1" ${GF} />` + gd(51, 24.5, 2.3) + gp('M41 27 L37 29 M44 31 V34 M47 31 V34'),
  },
  'land-and-water-ecosystems': {
    label: 'Mountains with a river winding down and widening into the sea, gold waves where fresh water turns salty',
    ink: p('M3 24 L13 8 L20 17 L27 6 L37 24') + p('M23 24 C23 32 14 32 14 39 C14 43 10 45 5 46 M28 24 C28 31 21 32 22 38 C23 43 32 43 51 46'),
    gold: gp('M9 51 q3 -3 6 0 t6 0 t6 0 t6 0 t6 0 t6 0'),
  },
  'adaptations-for-survival': {
    label: 'A snowshoe hare sitting with long ears and big hind feet, a gold snowflake above it',
    ink: `<ellipse cx="30" cy="39" rx="15" ry="10" />` + c(13, 31, 6.2) + p('M12 25 C9 13 11 7 14 6 C17 8 17 18 17 26 M17 26 C20 15 23 10 26 11 C27 15 24 23 21 29')
      + p('M35 48 H50 C50 42 46 40 42 40') + dot(9.5, 30, 1.3),
    gold: gp('M43 5 V15 M38.7 7.5 L47.3 12.5 M38.7 12.5 L47.3 7.5'),
  },
  'daily-and-seasonal-rhythms': {
    label: 'A monarch butterfly with veined wings spread, its gold body between them, flying south for winter',
    ink: p('M26 27 C20 14 8 8 4 12 C4 22 12 28 26 28 Z M26 29 C14 29 8 36 10 44 C18 46 26 40 26 29 Z')
      + p('M26 27 L10 14 M26 28 L7 20 M26 29 L11 40 M26 30 L18 44')
      + `<g transform="translate(56 0) scale(-1 1)">` + p('M26 27 C20 14 8 8 4 12 C4 22 12 28 26 28 Z M26 29 C14 29 8 36 10 44 C18 46 26 40 26 29 Z')
      + p('M26 27 L10 14 M26 28 L7 20 M26 29 L11 40 M26 30 L18 44') + `</g>` + p('M28 18 L24 10 M28 18 L32 10'),
    gold: gp('M28 19 V46'),
  },
  'populations-rise-and-fall': {
    label: 'A bar chart of counts that rise and fall from year to year, the low winter count in gold',
    ink: p('M6 51 V6 M6 51 H52') + `<rect x="11" y="24" width="7" height="27" />` + `<rect x="21" y="12" width="7" height="39" />` + `<rect x="31" y="30" width="7" height="21" />`,
    gold: `<rect x="41" y="40" width="7" height="11" ${GF} />`,
  },
  'eutrophication-and-big-changes': {
    label: 'A fish with crossed-out eyes lying dead below a gold scum of algae on the water surface',
    ink: `<g transform="rotate(170 28 38)">` + p('M10 38 C16 30 30 30 40 38 C30 46 16 46 10 38 Z M40 38 L50 30 V46 Z') + p('M17 35 l3.5 3.5 M20.5 35 l-3.5 3.5') + `</g>` + dot(14, 24, 1.3) + dot(20, 49, 1.3),
    gold: gp('M4 14 q4 -4 8 0 t8 0 t8 0 t8 0 t8 0 t8 0'),
  },
  'people-change-habitats': {
    label: 'A blue catfish with its long gold whiskers, a big fish put into Virginia rivers',
    ink: p('M9 32 C9 25 19 23 29 25 C38 27 42 29 48 25 L46 33 L48 41 C42 37 38 39 29 41 C19 43 9 40 9 32 Z') + p('M25 25 L28 18 L34 26') + dot(15, 29.5, 1.5),
    gold: gp('M9 33 C5 35 4 39 3 44 M11 37 C9 41 9 46 7 50 M9 29 C5 28 3 24 3 21'),
  },
  'restoring-ecosystems': {
    label: 'A bald eagle\'s head in profile with a hooked gold beak, a bird that recovered after DDT was banned',
    ink: p('M21 21 C22 8 38 6 42 16 C44 22 42 28 42 31') + p('M18 34 q3 3 6 0 t6 0 t6 0 t6 0') + p('M17 34 C16 42 18 48 22 53 H46 C44 45 44 38 42 31') + dot(27, 19, 1.8) + p('M22 15 L32 17'),
    gold: `<path d="M22 19 C12 17 7 24 9 37 C11 32 14 30 18 31 L23 27 Z" ${GF} />`,
  },
  'dna-the-code-of-life': {
    label: 'A strawberry with a gold strand of DNA pulled out of it',
    ink: p('M28 53 C14 45 7 33 9 25 C13 21 22 23 28 23 C34 23 43 21 47 25 C49 33 42 45 28 53 Z') + p('M28 23 L19 15 L24 18 L28 10 L32 18 L37 15 Z')
      + dot(18, 31, 1.3) + dot(28, 29, 1.3) + dot(38, 31, 1.3) + dot(23, 38, 1.3) + dot(33, 38, 1.3) + dot(28, 45, 1.3),
    gold: gp('M44 3 C50 7 38 10 44 14 C50 18 38 21 44 24 M44 3 C38 7 50 10 44 14 C38 18 50 21 44 24'),
  },
  'reproduction-and-meiosis': {
    label: 'A strawberry plant sending out a gold runner that roots a new plantlet',
    ink: p('M14 52 V40 M14 44 C6 44 4 36 5 32 C11 32 14 36 14 44 M14 44 C22 44 24 36 23 32 C17 32 14 36 14 44 M14 40 C10 34 12 28 14 26 C16 28 18 34 14 40')
      + p('M44 52 V45 M44 47 C39 47 38 42 38.5 40 C42 40 44 42 44 47 M44 47 C49 47 50 42 49.5 40 C46 40 44 42 44 47') + p('M3 52 H53', 'opacity="0.55"'),
    gold: gp('M16 49 C24 38 36 38 43 49'),
  },
  'predicting-traits': {
    label: 'Four pea flowers in a square, three drawn in ink and one in gold, the one in four that differs',
    ink: flower(15, 15) + flower(41, 15) + flower(15, 41),
    gold: flower(41, 41, true),
  },
  'inherited-or-acquired': {
    label: 'A hydrangea head packed with florets, a few in gold, the colour that depends on the soil',
    ink: ball().map(([x, y]) => floret(x, y)).join('') + p('M28 40 V53 M28 49 C21 49 16 46 14 41 C21 41 26 44 28 49'),
    gold: gd(28, 22, 4.6) + gd(17.5, 22, 4.6),
  },
  'mutations-and-variation': {
    label: 'Three oak leaves lined up on a ruler, all different sizes and shapes, one picked out in gold',
    ink: oak(10, 44, 0.85) + oak(47, 44, 1.02) + p('M3 51 H53 M8 49 V53 M18 49 V53 M28 49 V53 M38 49 V53 M48 49 V53'),
    gold: oak(28, 44, 1.32, GS),
  },
  'natural-selection-in-action': {
    label: 'A dark peppered moth, easy to spot, beside a pale gold-outlined moth resting on a light tree trunk',
    ink: p('M13 2 V54 M43 2 V54') + p('M18 10 V16 M37 30 V36', 'opacity="0.55"') + moth(28, 16, 'fill="currentColor"'),
    gold: moth(28, 43, `style="stroke:var(--ddp-color-secondary)" fill="none" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"`),
  },
  'evidence-for-change': {
    label: 'A fan-ribbed scallop fossil resting on gold layers of rock',
    ink: p('M28 47 L9 22 C9 8 47 8 47 22 Z') + p('M28 47 L16 14 M28 47 L22 10 M28 47 L28 9 M28 47 L34 10 M28 47 L40 14') + p('M28 47 L19 43 L22 37 M28 47 L37 43 L34 37'),
    gold: gp('M4 52 q6 -2 12 0 t12 0 t12 0 t12 0'),
  },
  'extinction-and-survival': {
    label: 'A spiny chestnut burr holding a gold chestnut, the tree the blight nearly erased',
    ink: c(28, 30, 12) + p(Array.from({ length: 16 }, (_, i) => { const a = i * Math.PI / 8, f = (r: number) => `${+(28 + r * Math.cos(a)).toFixed(1)} ${+(30 + r * Math.sin(a)).toFixed(1)}`; return `M${f(12)} L${f(19)}`; }).join(' '))
      + `<ellipse cx="28" cy="30" rx="6" ry="9" />`,
    gold: `<ellipse cx="28" cy="30" rx="3.6" ry="6.4" ${GF} />`,
  },
};
