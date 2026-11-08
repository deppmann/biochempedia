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
const rect = (x: number, y: number, w: number, h: number, r = 2) => `<rect x="${x}" y="${y}" width="${w}" height="${h}" rx="${r}" />`;
/** A water drop with its point at (x, y) and a round belly of radius r below it. */
const drop = (x: number, y: number, r: number) =>
  `M${x} ${y} Q${x + r} ${y + r * 1.35} ${x + r} ${y + r * 1.9} A${r} ${r} 0 0 1 ${x - r} ${y + r * 1.9} Q${x - r} ${y + r * 1.35} ${x} ${y} Z`;
/** The point at angle a (degrees, 0 = right, clockwise on screen) on a circle. */
const pol = (cx: number, cy: number, r: number, a: number) => {
  const t = (a * Math.PI) / 180;
  return [+(cx + r * Math.cos(t)).toFixed(1), +(cy + r * Math.sin(t)).toFixed(1)] as const;
};

const HEART = 'M28 52 C19 45 8 37 8 26 C8 19 13 14 19 14 C23.5 14 26.5 17 28 20 C29.5 17 32.5 14 37 14 C43 14 48 19 48 26 C48 37 37 45 28 52 Z';

export const COURSE: Record<string, IconArt> = { 'course:physiology': {
    label: 'A heart outline with a gold arterial pressure wave, one pulse with its small notch, running across it',
    ink: p(HEART),
    gold: gp('M2 40 H11 C15 40 16 21 21 21 C25 21 26 31 29 31 C30.5 31 31 32.5 32 34 C35 38 38 40 42 40 H54'),
  } };

export const ICONS: Record<string, IconArt> = {
  'body-fluid-compartments': {
    label: 'Three boxes nested one inside another for the fluid compartments of the body, with a gold water drop in the innermost',
    ink: rect(4, 8, 48, 44, 4) + rect(10, 14, 36, 32, 3) + rect(16, 20, 24, 20, 2.5),
    gold: `<path d="${drop(28, 24, 4.6)}" ${GF} />`,
  },
  'endocrine-axes-and-testing': {
    label: 'Three boxes stacked in a chain, hypothalamus, pituitary and gland, joined by arrows, with a gold feedback arrow looping back to the top',
    ink: rect(12, 4, 24, 11, 3) + rect(12, 23, 24, 11, 3) + rect(12, 42, 24, 11, 3)
      + p(`M24 15 V21 ${ah(24, 22.2, 'd', 2.6)} M24 34 V40 ${ah(24, 41.2, 'd', 2.6)}`),
    gold: gp(`M36 47.5 H48 V9.5 H38 ${ah(37.5, 9.5, 'l', 2.8)}`),
  },
  'thyroid-hormone': {
    label: 'A butterfly-shaped thyroid gland with a gold flame above its bridge for metabolic rate',
    ink: p('M28 29 C24 19 13 14 9 18 C5 25 9 40 19 45 C25 47 27 41 28 37 C29 41 31 47 37 45 C47 40 51 25 47 18 C43 14 32 19 28 29 Z'),
    gold: `<path d="M28 3 C30.5 7 33 9 32 13 C31.5 16 30 17.5 28 17.5 C26 17.5 24.5 16 24.5 13 C24.5 10.5 26.5 9.5 27 6.5 C27.3 5 27.6 3.8 28 3 Z" ${GF} />`,
  },
  'adrenal-glands': {
    label: 'A kidney with a small adrenal gland capping its upper end, the gold medulla in the middle and the cortex round it',
    ink: p('M30 18 C43 18 51 27 51 37 C51 48 42 55 31 55 C24 55 19 51 20 46 C21 42 22 40 22 36 C22 32 21 30 20 26 C19 21 24 18 30 18 Z')
      + p('M19 17 C19 8 27 3 35 4 C42 5 45 11 43 17 Z'),
    gold: `<path d="M26 15 C26 11 30 9 34 9.5 C37.5 10 38.5 13 37.5 15 Z" ${GF} />`,
  },
  'insulin-glucagon-glucose': {
    label: 'A seesaw balanced on a gold glucose drop, with an up arrow at one end and a down arrow at the other',
    ink: p('M5 33 L51 24') + p(`M10 26 V8 ${ah(10, 8, 'u', 3)}`) + p(`M46 7 V17 ${ah(46, 18, 'd', 3)}`) + p('M16 54 H40'),
    gold: `<path d="${drop(28, 28, 7)}" ${GF} />`,
  },
  'calcium-phosphate-bone': {
    label: 'A long bone with a scooped pit on its shaft where bone is being remodelled, and a gold Ca label beneath',
    ink: p('M10 12 C10 5 2 4 2 10 C2 13 5 15 8 16 C5 17 2 19 2 22 C2 28 10 28 10 21 H20 Q27 11 34 21 H46 C46 28 54 28 54 22 C54 19 51 17 48 16 C51 15 54 13 54 10 C54 4 46 5 46 12 Z'),
    gold: `<text x="28" y="49" text-anchor="middle" font-family="Georgia, 'Times New Roman', serif" font-size="17" font-weight="700" ${GF} stroke="none">Ca</text>`,
  },
  'skeletal-muscle-mechanics': {
    label: 'A striped muscle bundle above a length-tension curve, a hump with its flat gold optimum',
    ink: p('M3 14 C13 3 43 3 53 14 C43 25 13 25 3 14 Z') + p('M10 14 H46 M14 10 H42 M14 18 H42') + p('M20 9 V19 M28 8 V20 M36 9 V19')
      + p('M8 30 V52 H52') + p('M13 50 C18 44 20 40 24 39 H31 C35 40 38 44 43 50'),
    gold: gp('M24 39 H31'),
  },
  'smooth-muscle': {
    label: 'Spindle-shaped smooth muscle cells in a ring round the hollow centre of a small artery, one of them gold',
    ink: Array.from({ length: 8 }, (_, i) => {
      const a = i * 45 - 90;
      const [x, y] = pol(28, 28, 20, a);
      return i === 0 ? '' : `<path d="M-7.5 0 Q0 -3.4 7.5 0 Q0 3.4 -7.5 0 Z" transform="translate(${x} ${y}) rotate(${a + 90})" />`;
    }).join('') + p('M28 17 A11 11 0 1 1 27.9 17', 'stroke-dasharray="2 3.4"'),
    gold: (() => {
      const [x, y] = pol(28, 28, 20, -90);
      return `<path d="M-7.5 0 Q0 -3.4 7.5 0 Q0 3.4 -7.5 0 Z" transform="translate(${x} ${y})" ${GF} />`;
    })(),
  },
  'cardiac-electrophysiology-ecg': {
    label: 'An ECG trace on grid lines, a small P wave, a tall gold QRS spike and a rounded T wave',
    ink: p('M4 12 H52 M4 24 H52 M4 36 H52 M4 48 H52 M10 6 V52 M22 6 V52 M34 6 V52 M46 6 V52', 'opacity="0.28" stroke-width="1"')
      + p('M3 36 H9 Q12 28 15 36 H20 M33 36 H37 Q43 22 49 36 H53'),
    gold: gp('M20 36 L22 39 L26 9 L30 45 L33 36'),
  },
  'pressure-volume-loops': {
    label: 'A pressure-volume loop on axes, filling along the bottom, pressure rising, ejection across the top, and a gold arrow showing it runs counterclockwise',
    ink: p(`M7 5 V49 H52 ${ah(7, 5, 'u', 3)} ${ah(52, 49, 'r', 3)}`)
      + p('M16 40 Q29 45 43 41 L45 15 Q38 9 29 11 Q21 12 18 20 Z'),
    gold: gp(`M36 29 A5.5 5.5 0 1 0 30.5 34.5 ${ah(31.5, 34.5, 'r', 2.4)}`),
  },
  'cardiac-output-venous-return': {
    label: 'A rising cardiac function curve crossing a falling venous return line, with a gold dot at their crossing',
    ink: p(`M7 5 V49 H52`) + p('M10 46 C18 44 22 28 30 24 C38 20 44 19 50 18') + p('M10 12 L50 46'),
    gold: gd(26, 27.3, 3.6),
  },
  'resistance-compliance-local-flow': {
    label: 'A vessel branching in two, the upper branch narrowed to an arteriole with a gold flow arrow, the lower branch wide with a plain one',
    ink: p('M3 24 H12 C20 24 22 9.5 32 9.5 H52') + p('M52 14.5 H34 C27 14.5 25 24 23 30') + p('M23 30 C25 36 28 40 36 40 H52') + p('M3 36 H12 C20 36 22 52 32 52 H52')
      + p(`M5 30 H11 ${ah(12, 30, 'r', 2.6)}`) + p(`M36 46 H48 ${ah(49, 46, 'r', 3)}`),
    gold: gp(`M38 12 H47 ${ah(48, 12, 'r', 2)}`),
  },
  'capillary-exchange-and-lymph': {
    label: 'A capillary with small arrows leaving and entering through its wall, and a blind-ended lymph vessel below it taking up fluid on a gold arrow',
    ink: p('M3 5 H53 M3 15 H53') + p(`M12 18 V33 ${ah(12, 34, 'd', 3)}`) + p(`M20 18 V27 ${ah(20, 28, 'd', 2.6)}`) + p(`M44 35 V20 ${ah(44, 19, 'u', 3)}`)
      + p('M12 41 H53 M12 52 H53 M12 41 C4 41 4 52 12 52'),
    gold: gp(`M31 23 V37 ${ah(31, 38, 'd', 3)}`),
  },
  'blood-pressure-regulation': {
    label: 'A pressure dial with a gold needle, and a feedback arrow looping round it from below back to the top',
    ink: c(28, 28, 12.5)
      + [-150, -120, -90, -60, -30].map((a) => { const [x1, y1] = pol(28, 28, 12.5, a); const [x2, y2] = pol(28, 28, 9, a); return p(`M${x1} ${y1} L${x2} ${y2}`); }).join('')
      + p('M28 51 A23 23 0 0 1 28 5') + p(ah(29, 5, 'r', 3)) + p('M28 51 V40.5'),
    gold: gp('M28 28 L35.5 20.5') + gd(28, 28, 2),
  },
  'blood-cells-and-hemostasis': {
    label: 'Red blood cells seen edge-on as pinched biconcave discs above a loose gold mesh of fibrin strands that has caught one of them',
    ink: ['M-8 0 C-8 -5 -5 -5.5 -2.5 -3 Q0 -2 2.5 -3 C5 -5.5 8 -5 8 0 C8 5 5 5.5 2.5 3 Q0 2 -2.5 3 C-5 5.5 -8 5 -8 0 Z']
      .map((d) => `<path d="${d}" transform="translate(11 9)" /><path d="${d}" transform="translate(28 7) rotate(8)" /><path d="${d}" transform="translate(45 9)" /><path d="${d}" transform="translate(28 37) rotate(-10)" />`).join(''),
    gold: (() => {
      const ring = (r: number) => Array.from({ length: 8 }, (_, i) => pol(28, 37, r, i * 45 + 22.5)).map(([x, y], i) => `${i ? 'L' : 'M'}${x} ${y}`).join(' ') + ' Z';
      const spokes = Array.from({ length: 8 }, (_, i) => { const [x1, y1] = pol(28, 37, 8, i * 45 + 22.5); const [x2, y2] = pol(28, 37, 17, i * 45 + 22.5); return `M${x1} ${y1} L${x2} ${y2}`; }).join(' ');
      const st = 'style="stroke:var(--ddp-color-secondary)" fill="none" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"';
      return `<path d="${spokes} ${ring(12.5)} ${ring(17)}" ${st} />`;
    })(),
  },
};
