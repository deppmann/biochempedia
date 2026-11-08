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
/** A resting moth seen from above, centred on (x, y), scaled by s. */
const moth = (x: number, y: number, s = 1) => {
  const P = (dx: number, dy: number) => `${(x + dx * s).toFixed(2)} ${(y + dy * s).toFixed(2)}`;
  return `M${P(-1.5, -4)} L${P(-15, 0)} Q${P(-13, 8)} ${P(-1.5, 5)} Z M${P(1.5, -4)} L${P(15, 0)} Q${P(13, 8)} ${P(1.5, 5)} Z`;
};
const mothFeelers = (x: number, y: number, s = 1) =>
  `M${x} ${y - 5 * s} L${x - 3 * s} ${y - 10 * s} M${x} ${y - 5 * s} L${x + 3 * s} ${y - 10 * s}`;

export const ICONS: Record<string, IconArt> = {
  'testing-evolutionary-explanations': {
    label: "A ground finch perched in profile, its deep seed-cracking beak measured for depth",
    ink: c(32, 20, 8) + dot(34.5, 18, 1.8) + p('M25 24 Q13 25 11 35 L4 41 L13 40 Q22 45 31 40 Q38 34 37 27')
      + p('M21 42 V48 M27 42 V48 M6 48 H50') + p('M45 9 V30 M43 9 H47 M43 30 H47', 'stroke-width="1.4"'),
    gold: `<path d="M39 14 Q47 16 51 20 Q47 25 39 27 Z" ${GF} />`,
  },
  'reading-phylogenetic-trees': {
    label: 'A rooted tree with square-cornered branches, the common ancestor of three tips marked',
    ink: p('M5 24 H12 M12 13 V35.5 M12 13 H34 M34 8 V18 M34 8 H49 M34 18 H49 M12 35.5 H24 M24 28 V43 M24 28 H49 M24 43 H36 M36 38 V48 M36 38 H49 M36 48 H49')
      + dot(49, 8, 2) + dot(49, 18, 2) + dot(49, 28, 2) + dot(49, 38, 2) + dot(49, 48, 2),
    gold: gd(24, 35.5, 3.6),
  },
  'selection-in-ecological-context': {
    label: 'A pale moth and a dark moth resting on a tree trunk',
    ink: p('M7 4 V52 M49 4 V52') + p('M13 10 V16 M43 30 V38 M13 40 V46 M41 46 V51', 'stroke-width="1.2"')
      + p(moth(22, 36)) + p('M22 30 V45', 'stroke-width="2.6"') + p(mothFeelers(22, 36)),
    gold: `<path d="${moth(34, 15)}" ${GF} />` + p('M34 9 V24', 'style="stroke:var(--ddp-color-secondary)" fill="none" stroke-width="2.6" stroke-linecap="round"') + p(mothFeelers(34, 15), GS),
  },
  'drift-gene-flow-explanations': {
    label: 'Two populations holding different mixes of two alleles, one migrant carried from one to the other',
    ink: c(14, 34, 11) + c(42, 34, 11)
      + dot(10, 30, 2) + dot(17, 29, 2) + dot(11, 38, 2) + c(18, 38, 2)
      + c(38, 30, 2) + c(45, 30, 2) + c(39, 39, 2) + dot(46, 38, 2),
    gold: gp(`M16 20 Q28 4 40 20 ${ah(40.5, 20.5, 'd', 3)}`) + gd(28, 12.2, 3),
  },
  'molecular-evolution': {
    label: 'A clock from which two gene lineages diverge, gathering differences as they go',
    ink: c(11, 28, 7) + p('M11 28 V23.5 M11 28 H14.5') + p('M18 28 Q22 15 30 15 H50 M18 28 Q22 41 30 41 H50')
      + p('M35 11.5 V18.5 M43 11.5 V18.5 M35 37.5 V44.5 M50 37.5 V44.5'),
    gold: gp('M50 11.5 V18.5 M43 37.5 V44.5'),
  },
  'evolution-of-development': {
    label: 'A stickleback fish with its pelvic spine marked, the part lost in freshwater populations',
    ink: p('M5 27 Q20 12 38 24 L50 16 V38 L38 30 Q20 42 5 27 Z') + dot(12, 25, 1.9) + p('M18 18 L16 9 M26 18 L25 10 M33 21 L34 15'),
    gold: gp('M21 34.5 L15 45'),
  },
  speciation: {
    label: 'One lineage splitting in two with a barrier rising between the branches',
    ink: p('M28 52 V36 Q28 28 16 22 V14 M28 36 Q28 28 40 22 V14') + c(16, 9, 4.5) + c(40, 9, 4.5),
    gold: `<rect x="26" y="4" width="4" height="25" rx="2" ${GF} />`,
  },
  'history-of-life': {
    label: 'Rock layers with a fossil shell bracketed between two dated ash beds',
    ink: p('M4 7 Q16 5 28 7 T52 7 M4 50 Q16 48 28 50 T52 50') + p(spiral(28, 29, 1, 7.5, 2.2)) + p('M4 29 H15 M41 29 H52', 'stroke-width="1.2"'),
    gold: gp('M4 17 Q16 15 28 17 T52 17') + gp('M4 41 Q16 39 28 41 T52 41'),
  },
  'human-evolution': {
    label: 'A human skull in profile above a chromosome carrying one segment inherited from Neanderthals',
    ink: p('M15 21 C14 8 26 3 35 4 C45 5 50 13 49 22 C48 28 44 31 39 31 L30 31 L27 36 L16 36 L14 33 L12 31 L13 28 L10 26 L12 22 Z') + c(18, 23, 2.8) + p('M16 36 V33 M27 31 L30 31', 'stroke-width="1.2"')
      + `<rect x="7" y="40" width="42" height="9" rx="4.5" />`,
    gold: `<rect x="26" y="40" width="10" height="9" ${GF} />`,
  },
  'life-histories': {
    label: 'One energy budget split three ways: growth, upkeep and reproduction',
    ink: c(7, 28, 3) + p('M10 28 H20') + p(`M20 28 C28 28 26 11 36 11 H48 ${ah(49, 11, 'r', 3)}`) + p('M20 28 H40') + c(45, 28, 4.5),
    gold: gp('M20 28 C28 28 26 44 36 44') + gd(41.5, 44, 2.6) + gd(47.5, 40.5, 2.6) + gd(47.5, 47.5, 2.6),
  },
  'climate-and-biomes': {
    label: 'Parallel sunlight striking a globe, square-on at the equator and glancing near the poles',
    ink: c(35, 28, 17) + p('M18 28 H52 M21 18 H49 M21 38 H49', 'stroke-width="1.2"'),
    gold: gp(`M3 16 H13 ${ah(14, 16, 'r', 2.6)} M3 28 H13 ${ah(14, 28, 'r', 2.6)} M3 40 H13 ${ah(14, 40, 'r', 2.6)}`),
  },
  'niches-and-distributions': {
    label: 'A thermal performance curve, rising to an optimum and falling steeply, with its tolerance range marked',
    ink: p('M7 42 V7 M7 42 H50') + p('M11 41 C22 40 27 12 37 12 C42 12 44 28 46 41'),
    gold: gp('M11 50 H46 M11 47 V53 M46 47 V53'),
  },
  demography: {
    label: 'An age pyramid with the reproductive age classes marked',
    ink: p('M28 6 V51') + `<rect x="8" y="45" width="40" height="5" rx="1" /><rect x="13" y="31" width="30" height="5" rx="1" /><rect x="17" y="24" width="22" height="5" rx="1" /><rect x="21" y="17" width="14" height="5" rx="1" /><rect x="24.5" y="10" width="7" height="5" rx="1" />`,
    gold: `<rect x="9.5" y="38" width="37" height="5" rx="1" ${GF} />`,
  },
};


export const COURSE: Record<string, IconArt> = { 'course:ecology-evolution': {
    label: 'A branching tree of lineages whose tips rise into a hilly landscape under the sun',
    ink: p('M28 52 V42 M28 42 Q28 36 16 32 M28 42 Q28 36 40 32 M16 32 Q16 28 9 26 M16 32 Q16 28 22 25 M40 32 Q40 28 34 25 M40 32 Q40 28 47 26')
      + p('M3 25 Q10 19 17 23 Q24 27 31 22 Q39 16 46 22 Q50 25 53 24'),
    gold: gd(40, 9, 4.5),
  } };
