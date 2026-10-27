import type { IconArt } from '../signaling-icons';

/* Card icons for Biology Together (ages 5 to 10, hands-on activities for families and K-5 classrooms),
   Units 5 to 8.
   Same engraving hand as signaling-icons.ts: 56 x 56, navy ink, gold accent, everyday objects a parent
   recognises at a glance. The gold marks the one thing the activity is about. */

const c = (x: number, y: number, r: number) => `<circle cx="${x}" cy="${y}" r="${r}" />`;
const p = (d: string, extra = '') => `<path d="${d}" ${extra}/>`;
const GF = 'style="fill:var(--ddp-color-secondary)"';
const GS = 'style="stroke:var(--ddp-color-secondary)" fill="none" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"';
const gd = (x: number, y: number, r = 3) => `<circle cx="${x}" cy="${y}" r="${r}" ${GF} />`;
const gp = (d: string, extra = '') => `<path d="${d}" ${GS} ${extra}/>`;
/** A thick gold stroke with flat ends. */
const gw = (d: string, w: number) => `<path d="${d}" style="stroke:var(--ddp-color-secondary)" fill="none" stroke-width="${w}" stroke-linecap="butt" />`;
/** A thin gold stroke, for fine roots. */
const gt = (d: string) => `<path d="${d}" style="stroke:var(--ddp-color-secondary)" fill="none" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round" />`;
/** Map (u, v) in 0..1 onto a skewed tray top: P1 (u=0,v=0), P2 (u=1,v=0), P4 (u=0,v=1). */
const tray = (u: number, v: number, lift = 0): string => {
  const P1 = [4, 20], P2 = [34, 8], P4 = [22, 36];
  return `${n1(P1[0] + u * (P2[0] - P1[0]) + v * (P4[0] - P1[0]))} ${n1(P1[1] + u * (P2[1] - P1[1]) + v * (P4[1] - P1[1]) - lift)}`;
};
const gf = (d: string) => `<path d="${d}" ${GF} />`;
const dot = (x: number, y: number, r = 2.2) => `<circle cx="${x}" cy="${y}" r="${r}" fill="currentColor" stroke="none" />`;
const n1 = (v: number) => +v.toFixed(1);
/** An arrowhead whose tip is at (x, y), pointing right, left, up or down. */
const ah = (x: number, y: number, dir: 'r' | 'l' | 'u' | 'd', s = 3) =>
  dir === 'r' ? `M${x - s} ${y - s} L${x} ${y} L${x - s} ${y + s}`
  : dir === 'l' ? `M${x + s} ${y - s} L${x} ${y} L${x + s} ${y + s}`
  : dir === 'u' ? `M${x - s} ${y + s} L${x} ${y} L${x + s} ${y + s}`
  : `M${x - s} ${y - s} L${x} ${y} L${x + s} ${y - s}`;
/** Rows of fish-scale scallops starting at (x0, y0). */
const scales = (x0: number, y0: number, cols: number, rows: number, w = 8) => {
  let d = '';
  for (let r = 0; r < rows; r++) {
    const off = (r % 2) * (w / 2);
    d += `M${x0 + off - (r % 2 ? w : 0) + (r % 2 ? w : 0)} ${y0 + r * (w / 2 + 1)}`;
    for (let k = 0; k < cols - (r % 2); k++) d += ` a${w / 2} ${w / 2} 0 0 0 ${w} 0`;
  }
  return d;
};
/** A spiral shell, centred (cx, cy), from radius r0 to r1 over the given number of turns. */
const spiral = (cx: number, cy: number, r0: number, r1: number, turns: number) => {
  const N = Math.round(turns * 24);
  let d = '';
  for (let i = 0; i <= N; i++) {
    const t = i / N, a = t * turns * 2 * Math.PI, r = r0 + (r1 - r0) * t;
    d += `${i ? ' L' : 'M'}${n1(cx + r * Math.cos(a))} ${n1(cy + r * Math.sin(a))}`;
  }
  return d;
};
/** A wavy outline of a worm: centre line y = y0 + amp sin(...) from x0 to x1, half thickness h. */
const wormY = (x: number, x0: number, x1: number, y0: number, amp: number, waves: number) => y0 + amp * Math.sin(((x - x0) / (x1 - x0)) * waves * 2 * Math.PI);
const worm = (x0: number, x1: number, y0: number, amp: number, waves: number, h: number) => {
  const xs: number[] = [];
  for (let x = x0; x <= x1; x += 2) xs.push(x);
  const top = xs.map(x => `${n1(x)} ${n1(wormY(x, x0, x1, y0, amp, waves) - h)}`);
  const bot = xs.map(x => `${n1(x)} ${n1(wormY(x, x0, x1, y0, amp, waves) + h)}`).reverse();
  return `M${top[0]} L${top.slice(1).join(' L')} A${h} ${h} 0 0 1 ${bot[0]} L${bot.slice(1).join(' L')} A${h} ${h} 0 0 1 ${top[0]} Z`;
};
const wormLine = (x0: number, x1: number, y0: number, amp: number, waves: number, from: number, to: number) => {
  let d = '';
  for (let x = from; x <= to; x += 1) d += `${d ? ' L' : 'M'}${n1(x)} ${n1(wormY(x, x0, x1, y0, amp, waves))}`;
  return d;
};

export const ICONS: Record<string, IconArt> = {
  'fur-feathers-scales': {
    label: 'A feather and a tuft of fur beside a patch of fish scales picked out in gold',
    ink: p('M5 34 C5 19 14 8 29 5 C29 21 19 32 5 34 Z M5 34 L26 9') + p('M10 30 L9 25 M15 25 L14 19 M20 19 L19 14', 'opacity="0.55"')
      + p('M5 51 C6 47 6 44 5 41 M11 51 C12 47 12 44 11 41 M17 51 C18 47 18 44 17 41'),
    gold: gp(scales(26, 34, 3, 4, 8)),
  },
  'beak-buffet': {
    label: 'A bird with a gold cone-shaped beak and a few seeds in front of it, ready to feed',
    ink: c(21, 26, 14) + p('M13 14 L9 5 L19 12') + dot(24, 23, 2) + p('M14 40 C13 46 15 51 19 54') + dot(44, 45, 1.7) + dot(50, 49, 1.7) + dot(40, 51, 1.7),
    gold: gf('M34 20 L53 28 L34 35 Z'),
  },
  'blubber-glove': {
    label: 'A hand in a mitten dipped into a bowl of ice water, a thick gold layer of blubber around the hand',
    ink: p('M23 38 V19 C23 12 33 12 33 19 V38') + p('M5 37 H51') + p('M8 37 C9 55 47 55 48 37') + `<rect x="8" y="32" width="6" height="6" rx="1" transform="rotate(-12 11 35)" />` + `<rect x="42" y="31" width="6" height="6" rx="1" transform="rotate(14 45 34)" />` + p('M16 45 q3 -2 6 0 t6 0 t6 0 t6 0', 'opacity="0.55"'),
    gold: gp('M16 36 V28 L10 24 C8 21 11 18 14 20 L16 22 V15 C16 3 40 3 40 15 V36'),
  },
  'camouflage-hunt': {
    label: 'A lawn of green blades with a yarn worm hiding in it and a bright gold worm lying in the open',
    ink: p('M4 52 Q6 44 3 37 M9 52 Q11 42 10 34 M14 52 Q14 44 18 38 M19 52 Q21 43 20 35 M24 52 Q24 44 28 39 M29 52 Q31 42 30 34 M34 52 Q34 44 38 38 M39 52 Q41 43 40 35 M44 52 Q44 44 48 39 M49 52 Q51 43 50 36')
      + p('M7 47 q3 -3 6 0 t6 0 t6 0', 'opacity="0.55"') + p('M30 46 q3 -3 6 0 t6 0'),
    gold: gp('M10 16 q4 -5 8 0 t8 0 t8 0 t8 0'),
  },
  'backyard-habitat-hunt': {
    label: 'A square of string laid on the grass with an ant, a worm and a tuft of grass inside it',
    ink: c(16, 24, 2.4) + c(22, 24, 3) + c(30, 24, 3.6) + p('M14 22 L11 18 M12 20 L9 19 M22 21 L21 16 M24 27 L25 31 M20 27 L19 31 M32 27 L33 31 M30 21 L35 18') + p('M13 42 q3 -4 6 0 t6 0 t6 0') + p('M42 46 V37 M46 46 L48 38 M38 46 L36 38'),
    gold: gp('M6 6 H50 V50 H6 Z') + gd(6, 6, 2.2) + gd(50, 6, 2.2) + gd(50, 50, 2.2) + gd(6, 50, 2.2),
  },
  'fossil-prints': {
    label: 'A slab of clay with the spiral print of a shell pressed into it, the print in gold',
    ink: `<rect x="4" y="8" width="48" height="38" rx="9" />` + p('M10 49 H46', 'opacity="0.55"'),
    gold: gp(spiral(28, 27, 1.6, 13.5, 2.2)),
  },
  'food-chain-web': {
    label: 'A gold sun feeding a leaf, a grasshopper and a bird in a left to right chain, each arrow pointing to the eater',
    ink: p('M2 51 C2 41 7 35 14 35 C14 44 9 51 2 51 Z M2 51 L11 39')
      + `<ellipse cx="27" cy="46" rx="7" ry="3" transform="rotate(-8 27 46)" />` + c(35, 44, 2.3) + p('M24 45 L22 38 L28 49 M36 42 L39 38')
      + `<ellipse cx="47" cy="46" rx="6" ry="4.4" transform="rotate(-15 47 46)" />` + c(52, 40, 2.8) + p('M54.5 40 L56 41 M41 48 L37 51')
      + p(`M9 33 Q15 23 22 34 ${ah(22.4, 34.6, 'd', 2.4)}`) + p(`M30 37 Q38 25 46 33 ${ah(46.4, 33.6, 'd', 2.4)}`),
    gold: gd(8, 9, 3.8) + gp('M8 2 V3 M1 9 H2 M3 4 L4 5 M13 4 L12 5 M3 14 L4 13') + gp(`M8 15 V28 ${ah(8, 28.6, 'd', 2.4)}`),
  },
  'rot-detectives': {
    label: 'A closed jar of soil with a slice of apple going furry, the gold fuzz of mould on it',
    ink: `<rect x="5" y="12" width="46" height="6" rx="2" />` + p('M8 18 C6 28 6 44 10 50 C12 53 44 53 46 50 C50 44 50 28 48 18') + p('M13 51 C13 38 43 38 43 51 Z') + dot(20, 46, 1.2) + dot(28, 47.5, 1.2) + dot(36, 46, 1.2),
    gold: gp('M17 40 q2 -3 4 0 t4 0 t4 0 t4 0 t4 0'),
  },
  'soil-shake': {
    label: 'A tall jar of shaken muddy water that has settled into layers, the layer marks in gold',
    ink: `<rect x="12" y="4" width="32" height="7" rx="2" />` + p('M14 11 V48 Q14 52 18 52 H38 Q42 52 42 48 V11') + p('M14 20 q3 -2 7 0 t7 0 t7 0 t7 0', 'opacity="0.55"')
      + dot(19, 48, 1.1) + dot(26, 46.5, 1.1) + dot(33, 48, 1.1) + dot(38, 46, 1.1) + dot(22, 41.5, 0.9) + dot(31, 42, 0.9) + dot(20, 27, 1) + dot(30, 25, 1),
    gold: gp('M14 37 H42 M14 44 H42'),
  },
  'earthworm-choices': {
    label: 'An earthworm wriggling across the ground, the pale band near its head in gold, with a water drop beside it',
    ink: p(worm(6, 50, 33, 6, 1.2, 4.2)) + p('M10 52 H46', 'opacity="0.55"') + p('M12 9 C14 13 16 15 16 17 a4 4 0 0 1 -8 0 C8 15 10 13 12 9 Z'),
    gold: gw(wormLine(6, 50, 33, 6, 1.2, 15, 21), 6.4),
  },
  'adopt-a-tree': {
    label: 'A tree bare on one side and leafy on the other, with a gold string wrapped round its trunk to measure it',
    ink: p('M24 52 C26 46 26 38 25 30 M32 52 C30 46 30 38 31 30') + p('M25 34 L14 22 M19 27 L9 26 M14 22 L12 12 M14 22 L21 15 M27 31 L26 20')
      + p('M30 32 C27 22 31 9 41 10 C51 10 54 23 48 30 C44 34 36 35 30 32 Z') + p('M4 52 H52'),
    gold: gp('M24 42 C27 45 30 45 32 42 M24 46 C27 49 30 49 32 46'),
  },
  'sleep-or-travel': {
    label: 'A crescent moon above a bird in flight, a gold dotted path trailing behind it',
    ink: p('M20 4 A13 13 0 1 0 29 26 A10 10 0 1 1 20 4 Z') + p('M25 40 C30 29 39 29 41 38 C43 29 52 29 55 39') + dot(41, 41, 1.6),
    gold: gp('M3 53 C10 53 17 51 23 46', 'stroke-dasharray="1 4.5"'),
  },
  'hidden-leaf-colors': {
    label: 'A strip of coffee filter standing in a jar of green leaf juice, with a green band and a gold band of colour climbing it',
    ink: p('M12 30 V48 Q12 52 16 52 H40 Q44 52 44 48 V30') + p('M12 41 q4 -2 8 0 t8 0 t8 0 t8 0', 'opacity="0.55"')
      + `<rect x="24" y="4" width="10" height="44" rx="1" />` + p('M24 27 H34 M24 30 H34'),
    gold: gw('M25 16 H33 M25 21 H33', 3),
  },
  'watershed-in-a-pan': {
    label: 'A tilted tray of crumpled paper hills with gold streams running down the valleys into one gold pool in the low corner',
    ink: p('M4 20 L34 8 L52 22 L22 36 Z') + p('M4 20 V26 L22 42 L52 28 V22') + p('M22 36 V42')
      + p(`M${tray(0.05, 0.3)} ` + [0.2, 0.35, 0.5, 0.65, 0.8, 0.95].map((u, i) => `L${tray(u, 0.3, i % 2 ? 0 : 4)}`).join(' '))
      + p(`M${tray(0.05, 0.6)} ` + [0.25, 0.4, 0.55, 0.7, 0.85].map((u, i) => `L${tray(u, 0.6, i % 2 ? 0 : 4)}`).join(' ')),
    gold: gp(`M${tray(0.8, 0.34)} Q${tray(0.7, 0.7)} ${tray(0.25, 0.86)}`) + gp(`M${tray(0.5, 0.34)} Q${tray(0.45, 0.7)} ${tray(0.2, 0.86)}`) + gp(`M${tray(0.2, 0.34)} Q${tray(0.1, 0.6)} ${tray(0.1, 0.82)}`)
      + `<ellipse cx="${tray(0.14, 0.9).split(' ')[0]}" cy="${tray(0.14, 0.9).split(' ')[1]}" rx="8" ry="3.6" transform="rotate(-20 ${tray(0.14, 0.9).replace(' ', ' ')})" ${GF} />`,
  },
  'roots-hold-the-soil': {
    label: 'Two blocks of soil on a slope in the rain: bare soil crumbs washing off the left one, grass with fine gold roots holding the right one together',
    ink: p('M3 24 L23 30 V51 H3 Z') + p('M33 24 L53 30 V51 H33 Z') + p('M38 27 Q38 22 36 18 M43 28.5 Q44 22 47 20 M48 29.5 Q48 25 51 23') + p('M6 3 l-1.5 4 M18 5 l-1.5 4 M30 3 l-1.5 4 M42 5 l-1.5 4 M52 3 l-1.5 4')
      + dot(27, 34, 1.5) + dot(29, 40, 1.5) + dot(26, 45, 1.5) + dot(30, 48.5, 1.5) + dot(28, 31, 1.2),
    gold: gt('M38 27 V43 M38 33 L35 38 M38 38 L41 43 M43 28.5 V47 M43 36 L40 41 M43 41 L46 46 M48 29.5 V41 M48 35 L51 39'),
  },
  'creek-critters': {
    label: 'A kitchen strainer held in a stream, with a small gold mayfly nymph beside it',
    ink: c(20, 25, 12) + p('M29 17 L48 5') + p('M10 25 H30 M12 20 H28 M12 30 H28 M15 15 V35 M20 13 V37 M25 15 V35', 'opacity="0.55"') + p('M4 52 q4 -3 8 0 t8 0 t8 0 t8 0 t8 0 t8 0'),
    gold: `<ellipse cx="40" cy="38" rx="7" ry="3.2" transform="rotate(20 40 38)" ${GF} />` + gd(32.5, 35.5, 2.6) + gp('M46 41 L52 44 M46 40 L52 40 M46 38 L52 36 M36 40 L34 46 M40 41 L39 47 M43 42 L44 47'),
  },
};
