import type { IconArt } from '../signaling-icons';

/* Card icons for Biology Together (ages 5 to 10, hands-on activities for families and K-5 classrooms),
   Units 1 to 4, and the course card.
   Same engraving hand as signaling-icons.ts: 56 x 56, navy ink, gold accent, everyday objects a parent
   recognises at a glance. The gold marks the one thing the activity is about. */

const c = (x: number, y: number, r: number) => `<circle cx="${x}" cy="${y}" r="${r}" />`;
const p = (d: string, extra = '') => `<path d="${d}" ${extra}/>`;
const GF = 'style="fill:var(--ddp-color-secondary)"';
const GS = 'style="stroke:var(--ddp-color-secondary)" fill="none" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"';
const gd = (x: number, y: number, r = 3) => `<circle cx="${x}" cy="${y}" r="${r}" ${GF} />`;
const gp = (d: string, extra = '') => `<path d="${d}" ${GS} ${extra}/>`;
const gf = (d: string) => `<path d="${d}" ${GF} />`;
const dot = (x: number, y: number, r = 2.2) => `<circle cx="${x}" cy="${y}" r="${r}" fill="currentColor" stroke="none" />`;
const n1 = (v: number) => +v.toFixed(1);
/** A point on a circle, angle in degrees clockwise from 3 o'clock. */
const pol = (cx: number, cy: number, r: number, deg: number): [number, number] => [n1(cx + r * Math.cos(deg * Math.PI / 180)), n1(cy + r * Math.sin(deg * Math.PI / 180))];
/** A circular arc from angle a0 to a1 (clockwise) and an arrowhead at its end. */
const arcArrow = (cx: number, cy: number, r: number, a0: number, a1: number, s = 3.4) => {
  const [x0, y0] = pol(cx, cy, r, a0), [x1, y1] = pol(cx, cy, r, a1);
  const t = (a1 + 90) * Math.PI / 180, ux = Math.cos(t), uy = Math.sin(t);
  const nx = -uy, ny = ux;
  const b = (k: number) => `${n1(x1 - ux * s + nx * k * s)} ${n1(y1 - uy * s + ny * k * s)}`;
  return `M${x0} ${y0} A${r} ${r} 0 ${a1 - a0 > 180 ? 1 : 0} 1 ${x1} ${y1} M${b(1)} L${x1} ${y1} L${b(-1)}`;
};
/** A tapered leaf from base (x, y), pointing along angle deg, length L, half-width w. */
const leaf = (x: number, y: number, deg: number, L: number, w: number) => {
  const a = deg * Math.PI / 180, ux = Math.cos(a), uy = Math.sin(a), nx = -uy, ny = ux;
  const q = (f: number, k: number) => `${n1(x + ux * L * f + nx * w * k)} ${n1(y + uy * L * f + ny * w * k)}`;
  return `M${x} ${y} C${q(0.25, 1.3)} ${q(0.8, 0.9)} ${q(1, 0)} C${q(0.8, -0.9)} ${q(0.25, -1.3)} ${x} ${y} Z`;
};

export const ICONS: Record<string, IconArt> = {
  'alive-or-not': {
    label: 'A pebble sitting beside a seedling with two gold leaves: one is alive, one is not',
    ink: p('M4 46 C3 37 12 32 21 34 C30 36 32 44 28 48 C23 52 8 52 4 46 Z M11 40 L15 44') + p('M41 52 V30') + p('M4 52 H52'),
    gold: gf('M41 36 C33 36 31 28 33 24 C39 25 42 30 41 36 Z') + gf('M41 31 C49 31 52 23 49 18 C43 20 40 25 41 31 Z'),
  },
  'wake-up-a-seed': {
    label: 'A clear zip bag with a bean in it, a gold root growing down from the bean',
    ink: `<rect x="8" y="6" width="40" height="46" rx="4" />` + p('M8 15 H48', 'stroke-dasharray="2 2.4"')
      + `<ellipse cx="29" cy="28" rx="10" ry="6.6" transform="rotate(-25 29 28)" />` + p('M24 23.5 C27 26 27 28 24.5 30.5', 'opacity="0.55"')
      + dot(14, 24, 1.1) + dot(41, 36, 1.1) + dot(15, 44, 1.1) + dot(42, 22, 1.1),
    gold: gp('M25 33 C24 39 20 41 22 47 M22.5 43 L17 44'),
  },
  'like-parent-not-the-same': {
    label: 'An opened pea pod with a row of peas, one of them a different size and picked out in gold',
    ink: p('M5 30 C8 14 38 8 52 14 C50 32 24 46 5 30 Z') + c(14, 27, 3.6) + c(23, 25, 4.4) + c(41, 23, 3) + p('M5 49 H51 M10 49 V53 M20 49 V53 M30 49 V53 M40 49 V53 M50 49 V53'),
    gold: gd(32, 24.5, 3.9),
  },
  'mystery-feely-bag': {
    label: 'A soft cloth bag with a gathered top and a hand reaching into the opening, the hidden shell inside it in gold',
    ink: p('M24 0 V12 C21 16 21 21 23.5 24.5 q2 3 4.4 1 q2 3 4.4 .5 q2.2 2.5 4.2 -.5 q2 .5 2.7 -2.5 C38.5 19 38 14 36 12 V0') + p('M24 14 C20 14 19 19 22 22.5')
      + `<ellipse cx="30" cy="29" rx="15" ry="4.5" />` + p('M15 29 C8 38 8 47 14 51 C22 54 38 54 46 51 C52 47 52 38 45 29') + p('M17 33 L20 38 M43 33 L40 38', 'opacity="0.55"'),
    gold: gp('M23 50 C20 41 40 41 37 50 Z M30 50 L25 43.5 M30 50 V42.5 M30 50 L35 43.5'),
  },
  'smell-detectives': {
    label: 'A paper cup covered in foil with holes poked in it, curls of gold smell drifting out, and an orange beside it',
    ink: p('M5 34 H31 L29 52 H7 Z') + p('M3 34 H33', 'stroke-width="3"') + dot(11, 38, 1.1) + dot(18, 38, 1.1) + dot(25, 38, 1.1)
      + c(43, 42, 9) + p('M43 33 V51 M34 42 H52 M36.6 35.6 L49.4 48.4 M49.4 35.6 L36.6 48.4', 'opacity="0.55"') + p('M43 33 C43 29 47 27 50 28 C49 32 46 33 43 33 Z'),
    gold: gp('M12 29 C6 24 16 22 12 16 C9 11 17 8 16 4') + gp('M26 29 C20 24 30 22 26 16 C23 11 31 8 30 4'),
  },
  'listening-walk': {
    label: 'An ear with gold arcs of sound arriving from the side',
    ink: p('M30 6 C42 5 49 15 47 26 C45 36 39 38 37 45 C35 52 24 52 23 43') + p('M31 17 C39 16 42 23 38 29 C35 33 32 34 31 40'),
    gold: gp('M16 20 C11 28 11 36 16 44') + gp('M9 14 C1 27 1 37 9 50'),
  },
  'what-plants-need': {
    label: 'Two cups of seedlings, a tall one and a short pale one, under a gold sun',
    ink: p('M5 37 H23 L21 52 H7 Z') + p('M14 37 V22 M14 30 C8 30 6 25 7 22 C11 22 14 25 14 30 M14 25 C20 25 22 20 21 17 C17 17 14 20 14 25')
      + p('M33 37 H51 L49 52 H35 Z') + p('M42 37 V32 M42 34 C38 34 37 32 38 30 C41 30 42 32 42 34', 'opacity="0.55"'),
    gold: gd(28, 12, 4.2) + gp('M28 3 V4 M18 12 H19 M38 12 H37 M21 5 L22 6 M35 5 L34 6'),
  },
  'plant-parts-we-eat': {
    label: 'A carrot plant: leaves above the soil line and the root we eat, in gold, below it',
    ink: p('M4 26 H52') + p('M28 26 V10 M28 22 L20 17 M28 22 L36 17 M28 16 L21 10 M28 16 L35 10 M28 10 L28 4') + p('M20 17 C14 17 12 13 12 10 M36 17 C42 17 44 13 44 10', 'opacity="0.55"'),
    gold: gf('M20 28 L36 28 L28 53 Z'),
  },
  'thirsty-celery': {
    label: 'A celery stalk with leaves standing in a glass of gold-coloured water, a thin gold line rising inside the stalk',
    ink: p('M25 50 V16 M33 50 V16 M25 16 H33') + p('M25 16 C17 17 11 11 14 5 C21 5 26 9 25 16 Z M33 16 C41 17 47 11 44 5 C37 5 32 9 33 16 Z M26 14 C21 9 24 4 29 2 C34 4 37 9 32 14')
      + p('M10 30 L14 52 H44 L48 30'),
    gold: `<path d="M12 38 H46 L44.2 51 H15.8 Z" style="fill:var(--ddp-color-secondary);opacity:.38" />` + gp('M11.5 38 q4.4 -2.4 8.8 0 t8.8 0 t8.8 0 t8.8 0') + gp('M29 46 V22'),
  },
  'leaf-detectives': {
    label: 'A maple leaf with its veins picked out in gold',
    ink: p('M28 41 L19 44 L22 35 L8 30 L16 26 L10 14 L22 18 L24 6 L28 9 L32 6 L34 18 L46 14 L40 26 L48 30 L34 35 L37 44 Z') + p('M28 41 V53'),
    gold: gp('M28 41 V14 M28 38 L14 20 M28 38 L42 20 M26 36 L11 30 M30 36 L45 30'),
  },
  'flower-take-apart': {
    label: 'A flower with its petals opened and gold-tipped stamens in the middle, and one petal pulled off beside it',
    ink: p('M25 30 C10 29 4 16 8 8 C18 9 25 18 25 30 Z M25 30 C40 29 46 16 42 8 C32 9 25 18 25 30 Z') + p('M25 30 V53 M25 46 C19 46 15 42 14 38') + p('M37 52 C37 45 46 43 51 46 C50 51 43 54 37 52 Z'),
    gold: gp('M25 28 L21 16 M25 28 V14 M25 28 L29 16') + gd(21, 14, 2.3) + gd(25, 12, 2.3) + gd(29, 14, 2.3),
  },
  'bean-to-bean': {
    label: 'A bean seed with two gold arrows circling it, a plant that goes round from seed to seed',
    ink: p('M20 19 C30 13 42 21 40 32 C38 42 26 45 20 39 C17 36 22 33 24 30 C26 27 17 25 20 19 Z'),
    gold: gp(arcArrow(28, 28, 23, 200, 330) + ' ' + arcArrow(28, 28, 23, 20, 150)),
  },
  'seeds-on-the-move': {
    label: 'A fuzzy sock with gold burrs stuck to it, seeds that hitch a ride',
    ink: p('M17 4 H37 V27 C37 31 41 33 47 35 C54 38 53 49 46 50 H23 C13 50 13 38 17 31 Z') + p('M17 11 H37') + p('M21 17 V20 M26 17 V20 M31 17 V20', 'opacity="0.55"'),
    gold: gd(30, 25, 2.6) + gp('M30 20.5 V22 M30 28 V29.5 M25.5 25 H27 M33 25 H34.5')
      + gd(24, 40, 2.6) + gp('M24 35.5 V37 M24 43 V44.5 M19.5 40 H21 M27 40 H28.5')
      + gd(41, 43, 2.6) + gp('M41 38.5 V40 M41 46 V47.5 M36.5 43 H38 M44 43 H45.5'),
  },
  'mealworm-metamorphosis': {
    label: 'A segmented mealworm with a gold arrow curving up to the beetle it turns into',
    ink: `<rect x="3" y="41" width="26" height="10" rx="5" />` + p('M10 41 V51 M16 41 V51 M22 41 V51')
      + `<ellipse cx="41" cy="22" rx="7.5" ry="11" transform="rotate(20 41 22)" />` + c(36.5, 8, 2.8) + p('M39 12 L45 33')
      + p('M47 17 L53 14 M48 24 L54 24 M45 31 L51 35 M34 17 L28 14 M33 24 L27 24 M36 31 L30 35'),
    gold: gp('M19 36 C19 29 25 27 30 32 M26.5 33.5 L30 32 L29 28.5'),
  },
};

export const COURSE: Record<string, IconArt> = { 'course:biology-together': {
  label: 'A grown-up and a child standing either side of a gold seedling, looking after it together',
  ink: c(13, 11, 5) + p('M5 52 V31 C5 22 11 19 13 19 C15 19 21 22 21 31 V52') + c(43, 27, 3.8) + p('M36 52 V41 C36 35 41 33 43 33 C45 33 50 35 50 41 V52')
    + p('M21 32 L25 37 M36 42 L31 41') + p('M3 52 H53'),
  gold: gp('M28 52 V32') + gf('M28 42 C21 42 18 35 20 31 C26 32 29 37 28 42 Z') + gf('M28 36 C35 36 38 29 35 25 C29 26 26 31 28 36 Z'),
} };
