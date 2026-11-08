import type { IconArt } from '../signaling-icons';

const c = (x: number, y: number, r: number, extra = '') => `<circle cx="${x}" cy="${y}" r="${r}" ${extra}/>`;
const p = (d: string, extra = '') => `<path d="${d}" ${extra}/>`;
const GF = 'style="fill:var(--ddp-color-secondary)"';
const GS = 'style="stroke:var(--ddp-color-secondary)" fill="none" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"';
const gd = (x: number, y: number, r = 3) => `<circle cx="${x}" cy="${y}" r="${r}" ${GF} />`;
const gp = (d: string) => `<path d="${d}" ${GS} />`;
const dot = (x: number, y: number, r = 1.7) => `<circle cx="${x}" cy="${y}" r="${r}" fill="currentColor" stroke="none" />`;
const ah = (x: number, y: number, dir: 'r' | 'l' | 'u' | 'd', s = 3) =>
  dir === 'r' ? `M${x - s} ${y - s} L${x} ${y} L${x - s} ${y + s}`
  : dir === 'l' ? `M${x + s} ${y - s} L${x} ${y} L${x + s} ${y + s}`
  : dir === 'u' ? `M${x - s} ${y + s} L${x} ${y} L${x + s} ${y + s}`
  : `M${x - s} ${y - s} L${x} ${y} L${x + s} ${y - s}`;
const DASH = 'stroke-dasharray="2 3.5"';

/** An outward spiral around (cx, cy) from radius r0 to r1 over `turns` turns. */
const spiral = (cx: number, cy: number, r0: number, r1: number, turns: number, start = -Math.PI / 2) => {
  const n = Math.round(turns * 48);
  let d = '';
  for (let i = 0; i <= n; i++) {
    const t = i / n, a = start + t * turns * 2 * Math.PI, r = r0 + (r1 - r0) * t;
    d += `${i ? 'L' : 'M'}${(cx + r * Math.cos(a)).toFixed(2)} ${(cy + r * Math.sin(a)).toFixed(2)} `;
  }
  return d.trim();
};

export const ICONS: Record<string, IconArt> = {
  'neuromuscular-junction': {
    label: 'A nerve terminal sitting on a folded muscle surface, with receptors clustered beneath it',
    ink: p('M28 5 V15') + p('M16 25 Q16 15 28 15 Q40 15 40 25 Z') + `<rect x="6" y="32" width="44" height="17" rx="4" />` + p('M17 32 V38 M22.5 32 V38 M28 32 V38 M33.5 32 V38 M39 32 V38'),
    gold: gp('M15 29 H41'),
  },
  'cns-synapses': {
    label: 'A synapse held together by adhesion bridges, wrapped on both sides by an astrocyte',
    ink: p('M16 6 V14 Q16 23 28 23 Q40 23 40 14 V6') + p('M16 50 V42 Q16 33 28 33 Q40 33 40 42 V50') + p('M8 14 Q4 28 8 42 M48 14 Q52 28 48 42'),
    gold: gp('M22 24.5 V31.5 M28 24.5 V31.5 M34 24.5 V31.5'),
  },
  'synapse-elimination': {
    label: 'Three axons reach one muscle fiber; two withdraw and one stays',
    ink: `<rect x="6" y="40" width="44" height="10" rx="5" />` + p('M11 5 Q12 14 15 21', DASH) + c(16, 24, 2.6) + p('M45 5 Q44 14 41 21', DASH) + c(40, 24, 2.6),
    gold: gp('M28 5 V34') + gd(28, 36.5, 3.6),
  },
  'spontaneous-activity': {
    label: 'A sheet of retinal cells with a wave of activity sweeping across it',
    ink: [10, 19, 28, 37, 46].flatMap((y) => [10, 19, 28, 37, 46].map((x) => (x + y <= 38 ? '' : dot(x, y)))).join(''),
    gold: gd(10, 10, 2.4) + gd(19, 10, 2.4) + gd(10, 19, 2.4) + gd(28, 10, 2.4) + gd(19, 19, 2.4) + gd(10, 28, 2.4)
      + gp('M40 5 Q21 21 5 40'),
  },
  'ocular-dominance': {
    label: 'One open eye and one closed eye; the open eye takes over most of the cortical stripes',
    ink: c(16, 12, 6.5) + p('M33.5 12 Q40 17 46.5 12 M36 15 L35 18 M40 16.5 V19.5 M44 15 L45 18') + `<rect x="6" y="26" width="44" height="24" rx="3" />`,
    gold: gd(16, 12, 2.6) + `<rect x="9.5" y="29.5" width="9" height="17" rx="2" ${GF} />` + `<rect x="23.5" y="29.5" width="9" height="17" rx="2" ${GF} />` + `<rect x="37.5" y="29.5" width="9" height="17" rx="2" ${GF} />`,
  },
  'critical-period-control': {
    label: 'A nerve cell enclosed by a net that closes its window of plasticity',
    ink: c(28, 28, 6.5) + p('M28 21.5 V8 M28 34.5 V48 M21.5 28 H8 M34.5 28 H48'),
    gold: gp('M28 13 L41 28 L28 43 L15 28 Z') + gp('M21.5 20.5 L34.5 35.5 M34.5 20.5 L21.5 35.5'),
  },
  'microglia-complement-pruning': {
    label: 'A microglial cell reaching out one process to engulf a tagged synapse',
    ink: c(15, 40, 6.5) + p('M10 45 L6 50 M9.5 36 L5 31') + p('M20 35 L30 25') + p('M29 17 Q29 27 39 27 Q49 27 49 17') + p('M39 5 V11'),
    gold: gd(39, 16, 4.6),
  },
  'sensitive-periods-behavior': {
    label: 'A songbird singing, its song learned during a sensitive period',
    ink: p('M8 38 Q10 24 24 24 Q28 15 35 16 Q39 17 40 21 L46 22 L40 25 Q38 38 24 40 Q14 41 8 38 Z') + p('M8 38 L4 44 M24 40 V48 M30 39 V48') + dot(34.5, 20, 1.4),
    gold: gp('M45 13 Q49 17 48 26') + gp('M49 8 Q55 15 53 29'),
  },
  'origins-of-glia': {
    label: 'One progenitor cell giving rise first to a neuron and then to a star-shaped glial cell',
    ink: c(11, 28, 6) + p(`M17 26 L28 16 M17 30 L28 40`) + c(36, 13, 5) + p('M41 13 H51'),
    gold: gd(38, 41, 3.4) + gp('M38 33 V36.5 M38 45.5 V49 M30 41 H33.5 M42.5 41 H46 M32.5 35.5 L35 38 M41 44 L43.5 46.5 M43.5 35.5 L41 38 M35 44 L32.5 46.5'),
  },
  'myelination': {
    label: 'A cross-section of an axon wrapped in a spiral of myelin by a glial cell',
    ink: c(25, 30, 5) + p(spiral(25, 30, 8, 18, 2.6, -Math.PI / 2)),
    gold: gp('M38 20 Q42 14 45 10') + gd(47, 8, 4),
  },
  'glia-metabolic-partners': {
    label: 'A glial cell passing fuel down its process into an axon',
    ink: c(16, 13, 7) + p('M21 18 Q31 22 33 31') + p('M4 34 H52 M4 45 H52'),
    gold: gd(26, 20.5, 2.2) + gd(31, 25.5, 2.2) + gp(`M38 39.5 H46 ${ah(47, 39.5, 'r', 2.6)}`),
  },
  'injury-and-regeneration': {
    label: 'A cut axon whose stump stops at a wall of scar tissue',
    ink: c(10, 28, 6) + p('M16 28 H29') + c(31.5, 28, 2.6) + p('M49 28 H54', 'stroke-dasharray="1.5 3"'),
    gold: gp('M39 8 L43 14 L39 20 L43 26 L39 32 L43 38 L39 44 L43 50'),
  },
  'adult-neurogenesis': {
    label: 'Two mature neurons with a small newborn neuron budding beside them',
    ink: c(13, 36, 5) + p('M13 31 V14 M13 22 L7 15 M13 22 L19 15 M13 41 V50') + c(30, 36, 5) + p('M30 31 V14 M30 22 L24 15 M30 22 L36 15 M30 41 V50'),
    gold: gd(45, 41, 3.4) + gp('M45 37.5 V32 M45 34 L42 31.5') + gp('M41 15 H50 M45.5 10.5 V19.5'),
  },
  'microcephaly-and-malformations': {
    label: 'A small, smooth brain inside the outline of a brain of normal size',
    ink: p('M7 34 C5 18 18 7 30 8 C44 9 52 20 49 34 C47 44 38 49 28 49 C16 49 8 44 7 34 Z', 'stroke-dasharray="2 3.5"') + p('M18 33 C17 25 23 20 29 20 C36 20 40 26 38 33 C37 37 33 39 28 39 C22 39 18 37 18 33 Z'),
    gold: gp(`M28 11 V16 ${ah(28, 17, 'd', 2.4)}`) + gp(`M10 30 H14.5 ${ah(15.5, 30, 'r', 2.4)}`) + gp(`M46 30 H41.5 ${ah(40.5, 30, 'l', 2.4)}`),
  },
  'synapse-disorders': {
    label: 'A dendrite with healthy mushroom-shaped spines and one long, thin, immature spine',
    ink: p('M4 38 H52 M4 46 H52') + p('M12 38 V30') + `<ellipse cx="12" cy="26" rx="4.5" ry="3.6" />` + p('M44 38 V30') + `<ellipse cx="44" cy="26" rx="4.5" ry="3.6" />`,
    gold: gp('M28 37 Q25 26 29 18 Q31 12 28 9') + gd(28, 8.5, 2),
  },
  'human-brain-expansion': {
    label: 'Three brains of rising size, the largest one deeply folded',
    ink: `<ellipse cx="9" cy="44" rx="4.5" ry="3.5" />` + `<ellipse cx="21" cy="39" rx="7.5" ry="6" />`,
    gold: gp('M28 34 C26 18 34 8 41 8 C50 8 53 20 52 30 C51 40 46 45 40 45 C33 45 29 41 28 34 Z')
      + gp('M33 22 Q37 25 34 29 M40 13 Q43 19 39 24 M47 22 Q43 28 47 34 M37 38 Q41 34 44 39'),
  },
  'organoids': {
    label: 'A small folded ball of brain tissue growing in a culture dish',
    ink: p('M5 38 V44 Q5 50 28 50 Q51 50 51 44 V38') + `<ellipse cx="28" cy="38" rx="23" ry="6" />`,
    gold: `<circle cx="28" cy="25" r="10" ${GS} />` + gp('M22 23 Q25 19 28 22 Q31 25 34 21 M23 29 Q28 32 33 28'),
  },
};
