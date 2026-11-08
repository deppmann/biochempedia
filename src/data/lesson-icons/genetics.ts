import type { IconArt } from '../signaling-icons';

const c = (x: number, y: number, r: number) => `<circle cx="${x}" cy="${y}" r="${r}" />`;
const p = (d: string, extra = '') => `<path d="${d}" ${extra}/>`;
const GF = 'style="fill:var(--ddp-color-secondary)"';
const GS = 'style="stroke:var(--ddp-color-secondary)" fill="none" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"';
const GS4 = 'style="stroke:var(--ddp-color-secondary)" fill="none" stroke-width="4" stroke-linecap="round" stroke-linejoin="round"';
const gd = (x: number, y: number, r = 3) => `<circle cx="${x}" cy="${y}" r="${r}" ${GF} />`;
const gp = (d: string) => `<path d="${d}" ${GS} />`;
const ah = (x: number, y: number, dir: 'r' | 'l' | 'u' | 'd', s = 3) =>
  dir === 'r' ? `M${x - s} ${y - s} L${x} ${y} L${x - s} ${y + s}`
  : dir === 'l' ? `M${x + s} ${y - s} L${x} ${y} L${x + s} ${y + s}`
  : dir === 'u' ? `M${x - s} ${y + s} L${x} ${y} L${x + s} ${y + s}`
  : `M${x - s} ${y - s} L${x} ${y} L${x + s} ${y - s}`;
/** A duplicated chromosome: two sister arms pinched at the centre (x, y), half-height h. */
const xd = (x: number, y: number, h: number, w = 6) =>
  `M${x - w} ${y - h} Q${x + w - 1.6} ${y} ${x - w} ${y + h} M${x + w} ${y - h} Q${x - w + 1.6} ${y} ${x + w} ${y + h}`;
/** A wrinkled pea: a circle with a puckered rim. */
const wrinkled = (cx: number, cy: number, r: number) => {
  const n = 48; let d = '';
  for (let i = 0; i <= n; i++) {
    const t = (i / n) * 2 * Math.PI, rr = r + 1.3 * Math.sin(7 * t);
    d += `${i ? 'L' : 'M'}${(cx + rr * Math.cos(t)).toFixed(2)} ${(cy + rr * Math.sin(t)).toFixed(2)} `;
  }
  return d + 'Z';
};
/** A small solid ink dot. */
const dot = (x: number, y: number, r = 1.7) => `<circle cx="${x}" cy="${y}" r="${r}" fill="currentColor" stroke="none" />`;
/** A single chromosome, upright: two capsules meeting at the centromere. */
const chrom = (x: number, style = '') =>
  `<rect x="${x - 4.5}" y="10" width="9" height="13" rx="4.5" ${style}/><rect x="${x - 4.5}" y="25" width="9" height="22" rx="4.5" ${style}/>`;

export const ICONS: Record<string, IconArt> = {
  'mendels-peas': {
    label: 'A round pea crossed with a wrinkled pea',
    ink: p(wrinkled(41, 28, 9.5)) + p('M24.5 25 L30.5 31 M30.5 25 L24.5 31'),
    gold: gd(12.5, 28, 8),
  },
  'chromosomes-and-meiosis': {
    label: 'A dividing cell whose spindle pulls a pair of matching chromosomes apart, one toward each pole',
    ink: `<ellipse cx="28" cy="28" rx="24" ry="20" />` + dot(7.5, 28, 2.6) + dot(48.5, 28, 2.6) + p(xd(18.5, 28, 11, 6))
      + p('M8 28 H17 M47 28 H38'),
    gold: gp(xd(37.5, 28, 11, 6)),
  },
  'probability-and-crosses': {
    label: 'A four-square cross grid with one square in four picked out',
    ink: `<rect x="8" y="8" width="40" height="40" rx="2" />` + p('M28 8 V48 M8 28 H48'),
    gold: `<rect x="31.5" y="31.5" width="13" height="13" rx="1.5" ${GF} />`,
  },
  'extending-mendel': {
    label: 'A full flower colour, a blended half colour and no colour: incomplete dominance',
    ink: c(10, 28, 7) + c(28, 28, 7) + c(46, 28, 7) + p('M10 38 V46 M28 38 V46 M46 38 V46'),
    gold: gd(10, 28, 5) + `<path d="M28 23 A5 5 0 0 0 28 33 Z" ${GF} />`,
  },
  'pedigrees': {
    label: 'A pedigree: a father and mother with two children, one son affected',
    ink: `<rect x="8" y="9" width="12" height="12" />` + c(42, 15, 6) + p('M20 15 H36 M28 15 V27 M16 27 H40 M16 27 V33 M40 27 V33') + c(16, 40, 6),
    gold: `<rect x="34" y="34" width="12" height="12" ${GF} />`,
  },
  'sex-linkage-and-beyond': {
    label: 'A long X chromosome and a short Y chromosome side by side, a gene marked on the X',
    ink: c(28, 28, 21) + `<rect x="15.5" y="12" width="9" height="11" rx="4.5" /><rect x="15.5" y="25" width="9" height="19" rx="4.5" />`
      + `<rect x="32" y="20" width="9" height="7" rx="3.5" /><rect x="32" y="29" width="9" height="13" rx="3.5" />`,
    gold: `<rect x="15" y="33" width="10" height="4" ${GF} />`,
  },
  'chromosome-changes': {
    label: 'Three copies of one chromosome where there should be two',
    ink: chrom(13) + chrom(28),
    gold: chrom(43, GS),
  },
  'linkage-and-mapping': {
    label: 'Two matching chromosomes crossing over and swapping ends',
    ink: p('M6 17 H18 C26 17 30 39 38 39 H50') + dot(10, 17, 2.2) + dot(46, 39, 2.2),
    gold: gp('M6 39 H18 C26 39 30 17 38 17 H50'),
  },
  'three-point-mapping': {
    label: 'A gene map with three genes and the distances between them, the middle gene found by a double crossover',
    ink: p('M6 34 H50 M10 30 V38 M46 30 V38') + p('M10 26 Q16 16 22 26 M22 26 Q34 10 46 26') + p('M10 42 Q28 54 46 42', 'stroke-dasharray="1.5 4"'),
    gold: gd(22, 34, 3.6),
  },
  'complementation-and-pathways': {
    label: 'Two broken copies of a pathway, each one covering the gap in the other',
    ink: p('M8 15 H18 M26 15 H48 M8 41 H30 M38 41 H48'),
    gold: gp(`M22 36 V21 ${ah(22, 20, 'u', 2.6)}`) + gp(`M34 20 V35 ${ah(34, 36, 'd', 2.6)}`),
  },
  'bacterial-and-phage-genetics': {
    label: 'A virus perched on a bacterium, its DNA passing inside',
    ink: `<rect x="6" y="30" width="44" height="19" rx="9.5" />` + p('M28 4 L33.2 7 V13 L28 16 L22.8 13 V7 Z M28 16 V27 M28 27 L22 31 M28 27 L34 31'),
    gold: gp('M28 33 Q32 36.5 28 40 Q24 43.5 28 47'),
  },
  'dna-the-genetic-material': {
    label: 'A test tube with a glass rod lifting out a wad of DNA',
    ink: p('M14 10 V40 A7 7 0 0 0 28 40 V10 M14 28 H28') + p('M46 5 L22.5 35'),
    gold: `<ellipse cx="21.5" cy="36.5" rx="4.6" ry="3.4" transform="rotate(-52 21.5 36.5)" ${GF} />`,
  },
  'dna-replication': {
    label: 'A replication fork: the old strands part and a new strand is laid along each',
    ink: p('M6 25 H22 L48 11 M6 31 H22 L48 45'),
    gold: gp('M30.5 25.6 L48 16.4') + gp('M30.5 30.4 L48 39.6'),
  },
  'mutation': {
    label: 'A row of units, one changed by a strike',
    ink: c(8, 34, 4) + c(18, 34, 4) + c(28, 34, 4) + c(48, 34, 4) + p('M41 6 L35 15 H41 L35 24'),
    gold: `<rect x="34" y="30" width="8" height="8" rx="1" ${GF} />`,
  },
  'dna-repair-and-recombination': {
    label: 'A damaged stretch of one strand cut out and filled in again against its partner',
    ink: p('M6 22 H50 M6 33 H19 M37 33 H50 M19 30 V36 M37 30 V36') + p('M16 42 Q28 52 40 42'),
    gold: `<path d="M22 33 H34" ${GS4} />`,
  },
  'transcription': {
    label: 'DNA opened into a bubble, with an RNA copy peeling away from it',
    ink: p('M6 26 H17 Q28 14 39 26 H50 M6 32 H17 Q28 44 39 32 H50'),
    gold: gp('M22 30 Q30 30 34 20 L39 9'),
  },
  'rna-processing': {
    label: 'Two coding pieces joined after the piece between them loops out and is cut away',
    ink: `<rect x="6" y="32" width="14" height="10" rx="2" />` + `<rect x="36" y="32" width="14" height="10" rx="2" />` + p('M20 37 H36') ,
    gold: gp('M20 34 C16 8 40 8 36 34'),
  },
  'genetic-code-and-translation': {
    label: 'A ribosome reading along a messenger RNA and building a chain',
    ink: p('M5 45 H51') + `<ellipse cx="28" cy="39" rx="12" ry="4.5" />` + `<ellipse cx="28" cy="27" rx="15" ry="7.5" />`,
    gold: gd(30, 13.5, 2.8) + gd(36, 9, 2.8) + gd(43, 7, 2.8),
  },
  'lac-operon': {
    label: 'A repressor lifted off the DNA by a sugar, letting the genes beside it be read',
    ink: p('M5 40 H51') + `<rect x="26" y="35" width="11" height="10" rx="1.5" />` + `<rect x="39" y="35" width="11" height="10" rx="1.5" />` + `<rect x="6" y="14" width="15" height="11" rx="4" />` + p(`M13.5 37 V29 ${ah(13.5, 28, 'u', 2.4)}`),
    gold: gd(24, 11, 3.6),
  },
  'eukaryotic-regulation': {
    label: 'DNA wound on beads, one bead carrying chemical marks that set whether the gene is used',
    ink: c(10, 34, 6.5) + c(28, 34, 6.5) + c(46, 34, 6.5) + p('M3.5 42 Q10 46 16.5 34 M16.5 34 Q22 46 34.5 34 M34.5 34 Q40 46 52 42'),
    gold: gp('M28 27.5 V16 M28 27.5 L37 19') + gd(28, 13, 3) + gd(39, 17, 3),
  },
  'cancer-genetics': {
    label: 'Two copies of a gene, each knocked out by its own hit',
    ink: `<rect x="6" y="13" width="44" height="8" rx="4" />` + `<rect x="6" y="35" width="44" height="8" rx="4" />`,
    gold: gp('M15 10 L23 24 M23 10 L15 24') + gp('M33 32 L41 46 M41 32 L33 46'),
  },
  'recombinant-dna-and-pcr': {
    label: 'A circular plasmid with a foreign piece of DNA spliced into it',
    ink: c(28, 28, 17) + p('M38.5 14.2 L43.6 10.6 M38.5 41.8 L43.6 45.4'),
    gold: `<path d="M41.3 17.3 A17 17 0 0 1 41.3 38.7" ${GS4} />`,
  },
  'sequencing-and-genomes': {
    label: 'Many short overlapping reads assembled into one long genome',
    ink: p('M8 10 H24 M30 10 H46 M15 18 H33 M22 26 H40 M8 26 H16 M36 18 H48 M12 34 H28 M32 34 H48'),
    gold: `<path d="M8 44 H48" ${GS4} />`,
  },
  'crispr-and-functional-genomics': {
    label: 'Scissors guided to one spot on the DNA and cutting it',
    ink: p('M6 38 H25 M31 38 H50 M6 45 H25 M31 45 H50'),
    gold: `<circle cx="20" cy="9" r="4.5" ${GS} />` + `<circle cx="36" cy="9" r="4.5" ${GS} />` + gp('M22.5 13 L31 32 M33.5 13 L25 32'),
  },
  'population-genetics': {
    label: 'Allele frequencies drifting over generations, one reaching fixation and one lost',
    ink: p('M8 47 V9 M8 47 H50') + p('M9 28 L15 26 L21 32 L27 29 L33 37 L39 41 L45 46', 'stroke-dasharray="1.5 3.5"') + p('M8 10 H50', 'stroke-dasharray="1.5 4" stroke-width="1"'),
    gold: gp('M9 28 L15 23 L21 26 L27 18 L33 20 L39 12 L44 10 H49'),
  },
  'complex-traits-and-gwas': {
    label: 'A genome-wide scan: one tower of signals rising above the significance line',
    ink: p('M8 47 H50') + p('M8 17 H50', 'stroke-dasharray="1.5 3.5"')
      + dot(11, 42) + dot(14, 38) + dot(17, 43) + dot(20, 36) + dot(23, 41) + dot(26, 39) + dot(29, 43) + dot(42, 40) + dot(45, 36) + dot(48, 42) + dot(39, 37),
    gold: gd(34, 10, 2.4) + gd(32, 20, 2.2) + gd(36, 25, 2.2) + gd(33.5, 31, 2.2) + gd(35, 38, 2.2),
  },
};
