/* Wire the Cell — pure puzzle data + solver (no DOM), so it can be brute-force tested. */

export interface WireMod {
  nodeId: string;
  needs: string[];       // metabolites that must be available upstream (or from a fuel)
  produces?: string;
  atp: number;           // substrate-level ATP-equiv (baked for THIS puzzle's scale)
  nadh?: number;
  fadh2?: number;
  nadph?: number;
  cashier?: boolean;     // OxPhos: converts pooled carriers -> ATP (only with O2 + mitochondria)
  requiresO2?: boolean;
  blocked?: string;      // if set, the module cannot fire in this scenario; the text explains why
}
export interface WireGoal {
  label: string;
  atp?: number;                                   // total ATP-equiv >= this
  nadph?: number;                                 // net NADPH >= this
  make?: { metabolite: string; label: string };   // metabolite must be produced
}
export interface WireDemand {
  id: string;
  title: string;
  scene: string;
  fuels: Array<{ name: string; entry: string }>;
  o2: boolean;
  o2Note?: string;
  goal: WireGoal;
  par: number;
  teachWin: string;
  teachLose: string;
  mods: WireMod[];
}

/** Canonical module order: pathway order through metabolism. Same for every puzzle. */
export const CANON = ['glycolysis', 'fermentation', 'ppp', 'pdh', 'tca', 'oxphos',
  'betaOxidation', 'ketogenesis', 'gluconeogenesis', 'fattyAcidSynthesis'];
const canonIdx = (id: string) => { const i = CANON.indexOf(id); return i < 0 ? 99 : i; };

/** Metabolite pools that only ONE placed module can consume (no double-counting the same acetyl-CoA). */
const POOLS = ['acetylCoA'];

export const SHORT_NAME: Record<string, string> = {
  glycolysis: 'Glycolysis', fermentation: 'Lactate fermentation', ppp: 'Pentose phosphate pathway',
  pdh: 'Pyruvate dehydrogenase', tca: 'Citric acid cycle', oxphos: 'Oxidative phosphorylation',
  betaOxidation: 'β-Oxidation', ketogenesis: 'Ketogenesis', gluconeogenesis: 'Gluconeogenesis',
  fattyAcidSynthesis: 'Fatty acid synthesis',
};
export const MET_LABEL: Record<string, string> = {
  glucose: 'glucose', pyruvate: 'pyruvate', acetylCoA: 'acetyl-CoA', lactate: 'lactate', palmitate: 'palmitate',
  ribose5p: 'ribose-5-phosphate', nadph: 'NADPH', ketoneBodies: 'ketone bodies', carriers: 'reduced carriers',
};
const ml = (id: string) => MET_LABEL[id] ?? id;

const glyc = (): WireMod => ({ nodeId: 'glycolysis', needs: ['glucose'], produces: 'pyruvate', atp: 2, nadh: 2 });
const ferm = (): WireMod => ({ nodeId: 'fermentation', needs: ['pyruvate'], produces: 'lactate', atp: 0 });
const pdh = (): WireMod => ({ nodeId: 'pdh', needs: ['pyruvate'], produces: 'acetylCoA', atp: 0, nadh: 2, requiresO2: true });
const tca = (atp = 2, nadh = 6, fadh2 = 2): WireMod => ({ nodeId: 'tca', needs: ['acetylCoA'], produces: 'carriers', atp, nadh, fadh2, requiresO2: true });
const oxphos = (): WireMod => ({ nodeId: 'oxphos', needs: [], atp: 0, cashier: true });
const ppp = (nadph: number, produces = 'ribose5p'): WireMod => ({ nodeId: 'ppp', needs: ['glucose'], produces, atp: 0, nadph });
const beta = (): WireMod => ({ nodeId: 'betaOxidation', needs: ['palmitate'], produces: 'acetylCoA', atp: -2, nadh: 7, fadh2: 7, requiresO2: true });
const keto = (): WireMod => ({ nodeId: 'ketogenesis', needs: ['acetylCoA'], produces: 'ketoneBodies', atp: 0 });

export const DEMANDS: WireDemand[] = [
  {
    id: 'glucose-aerobic', title: 'Burn glucose, all-out',
    scene: 'A resting cell with plenty of oxygen wants every last ATP from one glucose. Wire the full aerobic line.',
    fuels: [{ name: 'Glucose', entry: 'glucose' }], o2: true,
    goal: { label: '≥ 30 ATP', atp: 30 }, par: 4,
    teachWin: 'The full aerobic line: substrate-level ATP is a rounding error; OxPhos cashing the 10 NADH + 2 FADH₂ is where about 90% of the yield lives.',
    teachLose: 'Without the bridge, the cycle, or OxPhos, the NADH never becomes ATP: you leave almost all the energy on the table.',
    mods: [glyc(), pdh(), tca(), oxphos(), ferm(), ppp(2)],
  },
  {
    id: 'sprint-anaerobic', title: 'Sprint, no oxygen',
    scene: 'Muscle is contracting faster than blood delivers O₂, so OxPhos is dead. Get ATP anyway, and don’t let glycolysis stall for lack of NAD⁺.',
    fuels: [{ name: 'Glucose', entry: 'glucose' }], o2: false, o2Note: 'No O₂',
    goal: { label: '≥ 2 ATP', atp: 2 }, par: 2,
    teachWin: 'Fermentation makes zero ATP itself: its job is regenerating NAD⁺ so glycolysis keeps firing for that net +2. That is the whole anaerobic economy.',
    teachLose: 'Glycolysis stalls without a way to regenerate NAD⁺. No fermentation and no O₂ means GAPDH backs up and even the +2 ATP disappears.',
    mods: [glyc(), ferm(), pdh(), tca(), oxphos()],
  },
  {
    id: 'rbc', title: 'The red blood cell',
    scene: 'A mature red blood cell has no mitochondria at all, yet it must make ATP and keep NADPH flowing to regenerate glutathione and defend hemoglobin from oxidative damage.',
    fuels: [{ name: 'Glucose', entry: 'glucose' }], o2: false, o2Note: 'No mitochondria',
    goal: { label: '≥ 2 ATP and ≥ 2 NADPH', atp: 2, nadph: 2 }, par: 3,
    teachWin: 'The RBC lives on glycolysis alone, ending in lactate to recycle NAD⁺, with a slice of glucose diverted through the pentose phosphate pathway for NADPH. G6PD deficiency breaks exactly that second branch.',
    teachLose: 'Two demands, two branches: glycolysis plus lactate for ATP (no mitochondria means no O₂ route), and the pentose phosphate pathway for NADPH.',
    mods: [glyc(), ferm(), ppp(2), pdh(), tca(), oxphos()],
  },
  {
    id: 'hypoxia-fuel', title: 'Oxygen-starved tissue',
    scene: 'A clot has cut off the blood supply. The tissue still holds both glucose and palmitate. With O₂ gone, which fuel can still make ATP, and how?',
    fuels: [{ name: 'Glucose', entry: 'glucose' }, { name: 'Palmitate', entry: 'palmitate' }], o2: false, o2Note: 'No O₂ (hypoxia)',
    goal: { label: '≥ 2 ATP', atp: 2 }, par: 2,
    teachWin: 'Fat is the richest fuel but is useless without O₂: β-oxidation, the cycle and OxPhos all depend on the ETC reoxidizing NADH and FADH₂. Only glycolysis, ending in lactate, runs anaerobically.',
    teachLose: 'Fatty acids cannot be burned anaerobically, because β-oxidation’s NADH and FADH₂ pile up with nowhere to go. Use the fuel whose pathway can regenerate NAD⁺ without O₂.',
    mods: [glyc(), ferm(), tca(), oxphos(), beta()],
  },
  {
    id: 'palmitate-aerobic', title: 'Torch a fat',
    scene: 'A fasting cell breaks down palmitate (C16). Route the fat all the way to CO₂ and water: fat is the densest fuel there is.',
    fuels: [{ name: 'Palmitate', entry: 'palmitate' }], o2: true,
    goal: { label: '≥ 100 ATP', atp: 100 }, par: 3,
    teachWin: 'Fat is the densest fuel: −2 to activate, then 7 rounds feed 8 acetyl-CoA to the cycle, and OxPhos cashes 31 NADH + 15 FADH₂ for about 106 ATP.',
    teachLose: 'β-oxidation only makes carriers. With no cycle plus OxPhos to cash them (and O₂), the fat’s energy stays locked up.',
    mods: [beta(), tca(8, 24, 8), oxphos(), keto(), glyc()],
  },
  {
    id: 'fasting-ketones', title: 'Fasting liver makes ketones',
    scene: 'Two days into a fast, the liver is flooded with fatty acids. It must export ketone bodies for the brain and still pay its own energy bills.',
    fuels: [{ name: 'Palmitate', entry: 'palmitate' }], o2: true,
    goal: { label: 'Ketone bodies and ≥ 20 ATP', atp: 20, make: { metabolite: 'ketoneBodies', label: 'Ketone bodies' } }, par: 3,
    teachWin: 'In fasting, oxaloacetate is pulled into gluconeogenesis, so the cycle cannot absorb all the acetyl-CoA and it spills into ketone bodies. The liver’s own ATP comes mainly from the NADH and FADH₂ made by β-oxidation itself (7 + 7 per palmitate, about 28 ATP at OxPhos, minus 2 for activation). It exports ketones but cannot use them (no thiophorase).',
    teachLose: 'Two outputs, three modules: β-oxidation makes the acetyl-CoA and the carriers, ketogenesis turns the acetyl-CoA into an exportable fuel, and OxPhos cashes the carriers to power the liver. The cycle is not an option here, because oxaloacetate is committed to gluconeogenesis.',
    mods: [glyc(), ppp(2), { ...tca(8, 24, 8), blocked: 'oxaloacetate is being pulled into gluconeogenesis, so the cycle can’t take this acetyl-CoA. That is exactly why it spills into ketone bodies.' }, oxphos(), beta(), keto()],
  },
  {
    id: 'cori-liver', title: 'Liver rebuilds glucose from lactate',
    scene: 'Lactate arrives from working muscle (the Cori cycle). Gluconeogenesis costs 6 ATP-equivalents per glucose, so the liver must also burn something to pay for it. Fatty acids are on hand.',
    fuels: [{ name: 'Lactate', entry: 'lactate' }, { name: 'Palmitate', entry: 'palmitate' }], o2: true,
    goal: { label: 'Make glucose and stay ≥ 30 ATP net', atp: 30, make: { metabolite: 'glucose', label: 'Glucose' } }, par: 4,
    teachWin: 'Gluconeogenesis is expensive (4 ATP + 2 GTP per glucose) and is powered by fat oxidation in the liver. Muscle spends ATP-poor glycolysis; the liver pays the bill and returns the glucose.',
    teachLose: 'Gluconeogenesis alone leaves the cell in the red. Something must generate net ATP, so oxidize the fat all the way through the cycle and OxPhos.',
    mods: [{ nodeId: 'gluconeogenesis', needs: ['lactate'], produces: 'glucose', atp: -6 }, tca(8, 24, 8), oxphos(), beta(), keto()],
  },
  {
    id: 'store-fat', title: 'Store the surplus',
    scene: 'Fed and flush with glucose, the cell wants to BUILD fat for storage. You’ll need carbon (acetyl-CoA) AND reducing power (NADPH), from two different places.',
    fuels: [{ name: 'Glucose', entry: 'glucose' }], o2: true,
    goal: { label: 'Build palmitate', make: { metabolite: 'palmitate', label: 'Palmitate' } }, par: 4,
    teachWin: 'Building fat needs BOTH carbon as acetyl-CoA (glucose to PDH) and reducing power as NADPH (from the pentose phosphate pathway). It COSTS ATP and NADPH: storage is an investment.',
    teachLose: 'Fatty-acid synthase needs acetyl-CoA AND NADPH at once. Miss either supply line (PDH for carbon, PPP for NADPH) and nothing gets built.',
    mods: [glyc(), pdh(), ppp(14, 'nadph'), { nodeId: 'fattyAcidSynthesis', needs: ['acetylCoA', 'nadph'], produces: 'palmitate', atp: -7, nadph: -14 }, oxphos()],
  },
  {
    id: 'dividing-cell', title: 'A cell about to divide',
    scene: 'Before mitosis a cell must copy its DNA and build membrane. That takes ribose-5-phosphate for nucleotides, NADPH for biosynthesis, and plenty of ATP, all from glucose with O₂ available.',
    fuels: [{ name: 'Glucose', entry: 'glucose' }], o2: true,
    goal: { label: 'Ribose-5-P, ≥ 2 NADPH, ≥ 20 ATP', atp: 20, nadph: 2, make: { metabolite: 'ribose5p', label: 'Ribose-5-phosphate' } }, par: 5,
    teachWin: 'Proliferating cells split glucose: the pentose phosphate pathway supplies ribose-5-P and NADPH, while glycolysis, PDH, the cycle and OxPhos supply ATP. (Here each path is scored at its own scale, a simplification of real flux splitting.)',
    teachLose: 'Three needs, two routes: the pentose phosphate pathway for ribose and NADPH, and the full aerobic line (glycolysis, PDH, cycle, OxPhos) for ATP.',
    mods: [glyc(), ferm(), ppp(2), pdh(), tca(), oxphos()],
  },
].map((d) => ({ ...d, mods: [...d.mods].sort((a, b) => canonIdx(a.nodeId) - canonIdx(b.nodeId)) }));

export interface SolveResult {
  fired: Set<string>; slpAtp: number; nadh: number; fadh2: number; cashed: number;
  oxphosCashed: boolean; atp: number; made: boolean; nadphNet: number; noWaste: boolean;
  won: boolean; available: Set<string>; stalled: boolean; conflicts: Record<string, string>;
}

export function solve(d: WireDemand, placed: Set<string>): SolveResult {
  const available = new Set<string>(d.fuels.map((f) => f.entry));
  const fired = new Set<string>();
  const poolTaken = new Map<string, string>();
  const conflicts: Record<string, string> = {};
  // Pool arbitration: the earliest pathway-order placed, runnable consumer owns each pool.
  for (const pool of POOLS) {
    const owner = d.mods.find((m) => placed.has(m.nodeId) && !m.blocked && !(m.requiresO2 && !d.o2) && m.needs.includes(pool));
    if (owner) poolTaken.set(pool, owner.nodeId);
  }
  let changed = true;
  while (changed) {
    changed = false;
    for (const m of d.mods) {
      if (m.cashier || !placed.has(m.nodeId) || fired.has(m.nodeId)) continue;
      if (m.blocked) continue;
      if (m.requiresO2 && !d.o2) continue;
      if (m.needs.every((n) => available.has(n))) {
        const clash = m.needs.find((n) => POOLS.includes(n) && poolTaken.get(n) !== m.nodeId);
        if (clash) { conflicts[m.nodeId] = poolTaken.get(clash)!; continue; }
        fired.add(m.nodeId);
        if (m.produces) available.add(m.produces);
        changed = true;
      }
    }
  }
  let slpAtp = 0, nadh = 0, fadh2 = 0, nadphNet = 0;
  for (const m of d.mods) {
    if (!fired.has(m.nodeId)) continue;
    slpAtp += m.atp || 0; nadh += m.nadh || 0; fadh2 += m.fadh2 || 0; nadphNet += m.nadph || 0;
  }
  const ox = d.mods.find((m) => m.cashier);
  const oxPlaced = !!ox && placed.has(ox.nodeId);
  const oxphosCashed = oxPlaced && d.o2 && nadh + fadh2 > 0;
  const cashed = oxphosCashed ? nadh * 2.5 + fadh2 * 1.5 : 0;

  // Glycolytic ATP only counts if its NADH is reoxidized (OxPhos with O2, or fermentation).
  let stallAdj = 0, stalled = false;
  const g = d.mods.find((m) => m.nodeId === 'glycolysis');
  if (g && fired.has('glycolysis') && !(oxphosCashed || fired.has('fermentation'))) { stallAdj = -(g.atp || 0); stalled = true; }
  const atp = slpAtp + cashed + stallAdj;

  const gl = d.goal;
  const made = gl.make ? available.has(gl.make.metabolite) : true;
  const blockedPlaced = d.mods.some((m) => m.blocked && placed.has(m.nodeId));
  const won = !blockedPlaced && made && (gl.atp === undefined || atp >= gl.atp) && (gl.nadph === undefined || nadphNet >= gl.nadph);
  const noWaste = !blockedPlaced && placed.size <= d.par && [...placed].every((id) => fired.has(id) || (ox && id === ox.nodeId && oxphosCashed));
  return { fired, slpAtp, nadh, fadh2, cashed, oxphosCashed, atp, made, nadphNet, noWaste, won, available, stalled, conflicts };
}

/** Plain-language list of what went wrong (empty when solved). */
export function diagnose(d: WireDemand, placed: Set<string>, res: SolveResult): string[] {
  const out: string[] = [];
  if (placed.size === 0) return ['Nothing is placed yet. Tap modules to build a line from the fuel to the goal.'];
  for (const m of d.mods) {
    if (!placed.has(m.nodeId)) continue;
    const nm = SHORT_NAME[m.nodeId] ?? m.nodeId;
    if (m.cashier) {
      if (res.oxphosCashed) continue;
      if (!d.o2) out.push(`${nm}: ${d.o2Note ?? 'no O₂'}, so electrons have no final acceptor and nothing is cashed.`);
      else out.push(`${nm}: no NADH or FADH₂ ever reaches it. Something upstream is missing.`);
    } else if (!res.fired.has(m.nodeId)) {
      if (m.blocked) out.push(`${nm}: ${m.blocked}`);
      else if (res.conflicts[m.nodeId]) out.push(`${nm}: the same acetyl-CoA is already consumed by ${SHORT_NAME[res.conflicts[m.nodeId]] ?? res.conflicts[m.nodeId]}; one pool can't be burned twice.`);
      else if (m.requiresO2 && !d.o2) out.push(`${nm}: needs O₂ (${(d.o2Note ?? 'none here').toLowerCase()}), so it cannot run.`);
      else {
        const missing = m.needs.filter((n) => !res.available.has(n)).map(ml);
        out.push(`${nm}: unmet input, no ${missing.join(' or ') || 'substrate'} reaches it.`);
      }
    }
  }
  if (res.stalled) out.push('Glycolysis stalls: its NADH is never reoxidized (no OxPhos with O₂, no lactate fermentation), so its ATP is lost.');
  const gl = d.goal;
  if (gl.make && !res.made) out.push(`${gl.make.label} is never produced by your line.`);
  if (gl.atp !== undefined && res.atp < gl.atp) out.push(`ATP short by ${fmtN(gl.atp - res.atp)} (${fmtN(res.atp)} of ${gl.atp}).`);
  if (gl.nadph !== undefined && res.nadphNet < gl.nadph) out.push(`NADPH short: ${res.nadphNet} of ${gl.nadph}.`);
  return out;
}
const fmtN = (n: number) => (Number.isInteger(n) ? String(n) : n.toFixed(1));

/** Score for a solved puzzle given failed RUNs so far. */
export function puzzleScore(perfect: boolean, fails: number): number {
  return Math.max(100, (perfect ? 500 : 300) - 100 * fails);
}
export function puzzleMedal(score: number): 'gold' | 'silver' | 'bronze' {
  return score >= 450 ? 'gold' : score >= 300 ? 'silver' : 'bronze';
}
