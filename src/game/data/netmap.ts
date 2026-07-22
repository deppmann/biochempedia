import type { NetMap, Metabolite, MetNode, Fuel } from '../netmap';

/* =============================================================================
   NETMAP — the cross-pathway network the two new ARCADE games play on:
     • Flux Foundry   (economy roguelite): draw a fuel, route it through nodes,
       cash reduced carriers at OxPhos, re-priced each pass by hormonal state.
     • Wire the Cell  (Zachlike construction puzzle): physically wire one node's
       output metabolite id into the next node's input id.

   This file is authored ONCE and MCAT-verified against:
     • the per-pathway Step.tokens in ./glycolysis.ts, ./citric-acid-cycle.ts,
       ./pyruvate-dehydrogenase.ts, ./fatty-acid-oxidation.ts, etc.
     • src/content/lessons/oxidative-phosphorylation/lesson.mdx  (~2.5 ATP/NADH,
       ~1.5 ATP/FADH₂; ~30–32 ATP/glucose; ~2 ATP/glucose by fermentation)
     • src/content/lessons/integration-of-metabolism/lesson.mdx  (whole-network)

   ---------------------------------------------------------------------------
   CONVENTIONS (read before trusting a number)

   1. atpEquiv = ONLY the SUBSTRATE-LEVEL ATP a node mints itself, per pass.
      Reduced carriers are NOT pre-cashed into atpEquiv — they ride out as the
      nadh/fadh2 fields and are converted to ATP by the OxPhos node alone. This
      keeps the network honest: no double-counting, and OxPhos is the jackpot.

   2. FLOATS. atpEquiv is ATP-equivalents, so OxPhos's ~2.5/NADH and ~1.5/FADH₂
      are represented directly, never rounded to integers.

   3. PER-PASS SCALE (stated per node, matching the per-pathway ledgers):
        • glycolysis  — per GLUCOSE (one pass = glucose → 2 pyruvate).
        • PDH         — per PYRUVATE (nadh:1, co2:1). A glucose runs it twice.
        • TCA         — per ACETYL-CoA (nadh:3, fadh2:1, gtp:1, co2:2). ×2/glucose.
        • β-oxidation — per ROUND (nadh:1, fadh2:1, +1 acetyl-CoA). The −2 ATP
                        activation toll is paid ONCE per fatty acid, carried in
                        atpEquiv on this node with a note (not per round).
        • OxPhos      — per (1 NADH + 1 FADH₂) cashing pass: 2.5 + 1.5 = 4.0.
        • gluconeogenesis — per GLUCOSE made (−6 ATP-equiv: 4 ATP + 2 GTP).
      Where a node's scale differs from "per glucose," its note says so.

   4. CYTOSOLIC-NADH SHUTTLE. Glycolysis' 2 NADH are cytosolic; they yield
      ~1.5 ATP each via the glycerol-phosphate shuttle or ~2.5 via
      malate–aspartate. We emit nadh:2 and let OxPhos value them at the ~2.5
      ceiling (matching the ~30–32 "malate–aspartate" total). The glucose fuel
      receipt below uses the ~32 upper figure; the note flags the ~30 shuttle
      floor so neither number is a surprise.

   5. GRAPH WIRING. One node's output metabolite id === the next node's input
      id, so the games can literally draw the edge:
        glycolysis → pyruvate → PDH → acetylCoA → TCA → {nadh,fadh2} → OxPhos.
      Reduced carriers ('nadh','fadh2') are outputs that feed OxPhos inputs.

   6. requiresO2 marks nodes that stall anaerobically (TCA, OxPhos, and — because
      it dead-ends into a backed-up carrier pool without OxPhos — β-oxidation).
      irreversible marks one-way doors (PDH: no acetyl-CoA → glucose; and the
      committed gates of glycolysis / gluconeogenesis / FA synthesis).

   7. states{} are relative activity multipliers (1 = normal, 0 = off) by
      hormonal/energetic context, reflecting reciprocal regulation.
   ============================================================================ */

const metabolites: Metabolite[] = [
  { id: 'glucose', name: 'Glucose', carbons: 6 },
  { id: 'glycogen', name: 'Glycogen (residues)' },
  { id: 'g6p', name: 'Glucose-6-phosphate', carbons: 6 },
  { id: 'g1p', name: 'Glucose-1-phosphate', carbons: 6 },
  { id: 'f6p', name: 'Fructose-6-phosphate', carbons: 6 },
  { id: 'pyruvate', name: 'Pyruvate', carbons: 3 },
  { id: 'lactate', name: 'Lactate', carbons: 3 },
  { id: 'acetylCoA', name: 'Acetyl-CoA', carbons: 2 },
  { id: 'oaa', name: 'Oxaloacetate', carbons: 4 },
  { id: 'citrate', name: 'Citrate', carbons: 6 },
  { id: 'ribose5p', name: 'Ribose-5-phosphate', carbons: 5 },
  { id: 'palmitate', name: 'Palmitate (C16 fatty acid)', carbons: 16 },
  { id: 'fattyAcylCoA', name: 'Fatty acyl-CoA', carbons: 16 },
  { id: 'glycerol', name: 'Glycerol', carbons: 3 },
  { id: 'ketoneBodies', name: 'Ketone bodies (acetoacetate / β-OHB)', carbons: 4 },
  { id: 'aminoAcids', name: 'Amino acids (glucogenic)' },
  { id: 'ammonia', name: 'Ammonia (NH₄⁺)' },
  { id: 'urea', name: 'Urea' },
  { id: 'nadh', name: 'NADH (reduced carrier)' },
  { id: 'fadh2', name: 'FADH₂ (reduced carrier)' },
  { id: 'nadph', name: 'NADPH (reductive-biosynthesis carrier)' },
  { id: 'gtp', name: 'GTP' },
  { id: 'atp', name: 'ATP' },
  { id: 'co2', name: 'Carbon dioxide (CO₂)', carbons: 1 },
  { id: 'o2', name: 'Oxygen (O₂)' },
  { id: 'water', name: 'Water (H₂O)' },
];

const nodes: MetNode[] = [
  {
    id: 'glycolysis',
    name: 'Glycolysis',
    emoji: '🍬',
    location: 'Cytosol',
    inputs: ['glucose'],
    outputs: ['pyruvate', 'nadh', 'atp'],
    atpEquiv: 2, // per glucose: 4 gross (PGK + PK, ×2) − 2 invested (HK + PFK-1)
    nadh: 2, // cytosolic — see shuttle note & OxPhos valuation
    irreversible: true, // HK / PFK-1 / PK are one-way committed gates
    states: { fed: 1.5, fasted: 0.3, sprint: 2, rest: 1 },
    note: 'Per GLUCOSE: net +2 ATP (substrate-level), +2 cytosolic NADH → 2 pyruvate. NADH is cytosolic: ~1.5 ATP each via glycerol-P shuttle or ~2.5 via malate–aspartate; we bank it and let OxPhos value it. Committed gate = PFK-1. Up when fed / sprinting, throttled in the fasting liver (reciprocal with gluconeogenesis).',
  },
  {
    id: 'pdh',
    name: 'Pyruvate Dehydrogenase (bridge)',
    emoji: '🌉',
    location: 'Mitochondrial matrix',
    inputs: ['pyruvate'],
    outputs: ['acetylCoA', 'nadh', 'co2'],
    atpEquiv: 0, // no substrate-level phosphorylation here
    nadh: 1, // PER PYRUVATE (a glucose runs it twice)
    co2: 1,
    requiresO2: true, // only worth running if OxPhos can cash the NADH downstream
    irreversible: true, // no acetyl-CoA → pyruvate → glucose; carbons are committed to oxidation
    states: { fed: 1.2, fasted: 0.4, sprint: 0.3, rest: 1 },
    note: 'PER PYRUVATE: 0 substrate-level ATP, 1 NADH, 1 CO₂ → acetyl-CoA. Irreversible — the reason fatty-acid carbons (which arrive as acetyl-CoA) can never become glucose. OFF in sprint (pyruvate → lactate instead) and in fasting liver (PDK phosphorylates it off to spare pyruvate for gluconeogenesis).',
  },
  {
    id: 'tca',
    name: 'Citric Acid Cycle (TCA / Krebs)',
    emoji: '🔄',
    location: 'Mitochondrial matrix',
    inputs: ['acetylCoA', 'oaa'],
    outputs: ['nadh', 'fadh2', 'gtp', 'co2', 'oaa'],
    atpEquiv: 1, // 1 GTP (substrate-level, succinyl-CoA synthetase) per acetyl-CoA
    nadh: 3, // PER ACETYL-CoA (IDH, α-KGDH, malate DH)
    fadh2: 1, // succinate dehydrogenase (Complex II)
    gtp: 1,
    co2: 2,
    requiresO2: true, // stalls when NADH/FADH₂ can't be reoxidized by the ETC
    states: { fed: 1, fasted: 1, sprint: 0.2, rest: 1 },
    note: 'PER ACETYL-CoA: +1 GTP (substrate-level), 3 NADH, 1 FADH₂, 2 CO₂; OAA is regenerated (catalytic). ×2 per glucose. Stalls anaerobically because it depends on the ETC to reoxidize its carriers. OAA level (drained in fasting for gluconeogenesis) sets the ceiling — the "fat burns in the flame of carbohydrate" bottleneck that spills acetyl-CoA into ketones.',
  },
  {
    id: 'oxphos',
    name: 'Oxidative Phosphorylation (ETC + ATP synthase)',
    emoji: '⚡',
    location: 'Inner mitochondrial membrane',
    inputs: ['nadh', 'fadh2', 'o2'],
    outputs: ['atp', 'water'],
    atpEquiv: 4, // THE cashier: 1 NADH (~2.5) + 1 FADH₂ (~1.5) per cashing pass = 4.0
    requiresO2: true, // O₂ is the terminal electron acceptor; ~0 flux anaerobically
    states: { fed: 1, fasted: 1, sprint: 0.05, rest: 1 },
    note: 'THE jackpot node — consumes reduced carriers and mints ATP: ~2.5 ATP per NADH, ~1.5 per FADH₂ (FLOATS; FADH₂ is lower because Complex II never pumps). atpEquiv=4.0 models one NADH + one FADH₂ cashed together. ~26–28 ATP/glucose here (~30–32 total with the 4 substrate-level). Near-zero in sprint (no O₂ → anaerobic) — the whole reason fermentation exists.',
  },
  {
    id: 'fermentation',
    name: 'Lactate Fermentation',
    emoji: '🥛',
    location: 'Cytosol',
    inputs: ['pyruvate', 'nadh'],
    outputs: ['lactate'],
    atpEquiv: 0, // makes no ATP itself — it REGENERATES NAD⁺ so glycolysis can keep firing
    states: { fed: 0.3, fasted: 0.5, sprint: 3, rest: 0.5 },
    note: 'Per pyruvate: consumes 1 NADH to make lactate, regenerating NAD⁺ so GAPDH (and thus glycolytic ATP) keeps running with no O₂. Makes 0 ATP directly — its value is unblocking glycolysis. This is why anaerobic glycolysis nets only ~2 ATP/glucose. Floods in sprint and in the mitochondria-free RBC; lactate exits to the liver (Cori cycle).',
  },
  {
    id: 'ppp',
    name: 'Pentose Phosphate Pathway',
    emoji: '🧬',
    location: 'Cytosol',
    inputs: ['g6p'],
    outputs: ['nadph', 'ribose5p', 'co2'],
    atpEquiv: 0, // no ATP; the point is NADPH + ribose-5-P
    nadph: 2, // oxidative phase, per G6P (G6PD + 6-phosphogluconate DH)
    co2: 1,
    states: { fed: 1.3, fasted: 0.7, sprint: 0.5, rest: 1 },
    note: 'PER GLUCOSE-6-PHOSPHATE (oxidative phase): 2 NADPH + ribose-5-P + 1 CO₂; NO ATP. NADPH ≠ NADH — it powers reductive biosynthesis (fatty-acid synthesis) and glutathione antioxidant defense, and is NOT cashed by OxPhos. Up when fed (biosynthesis) and under oxidative stress (RBC).',
  },
  {
    id: 'glycogenolysis',
    name: 'Glycogenolysis',
    emoji: '🌳',
    location: 'Cytosol (liver & muscle)',
    inputs: ['glycogen'],
    outputs: ['g1p', 'g6p'],
    atpEquiv: 0, // phosphorolysis frees G1P WITHOUT spending ATP (that's the trick)
    states: { fed: 0.3, fasted: 1.5, sprint: 2, rest: 1 },
    note: 'Phosphorylase cleaves glycogen by PHOSPHOROLYSIS (uses Pi, not ATP) → glucose-1-P → G6P. Because it skips hexokinase, a glycogen-derived glucose nets +3 ATP through glycolysis, not +2. Up in fasting (liver, to export glucose) and sprint (muscle, for local fuel).',
  },
  {
    id: 'gluconeogenesis',
    name: 'Gluconeogenesis',
    emoji: '🏭',
    location: 'Cytosol + mitochondria + ER (liver, kidney)',
    inputs: ['pyruvate', 'lactate', 'aminoAcids', 'glycerol'],
    outputs: ['glucose'],
    atpEquiv: -6, // PER GLUCOSE made: 4 ATP + 2 GTP spent (reverse of glycolysis is expensive)
    irreversible: true, // uses its own bypass gates (PC, PEPCK, FBPase-1, G6Pase) — not simple reversal
    states: { fed: 0.2, fasted: 2, sprint: 0.3, rest: 1 },
    note: 'PER GLUCOSE made: NET −6 ATP-equiv (4 ATP + 2 GTP), from 2 pyruvate/lactate/glucogenic-AA/glycerol. A net CONSUMER — the games must fund it from OxPhos. Reciprocal with glycolysis (never both on: futile cycle). Up in fasting/starvation to feed the brain; requires acetyl-CoA (from β-oxidation) to switch pyruvate carboxylase on.',
  },
  {
    id: 'betaOxidation',
    name: 'Fatty Acid β-Oxidation',
    emoji: '🔥',
    location: 'Mitochondrial matrix (after carnitine shuttle)',
    inputs: ['palmitate', 'fattyAcylCoA'],
    outputs: ['acetylCoA', 'nadh', 'fadh2'],
    atpEquiv: -2, // ACTIVATION toll: 2 ATP-equiv (ATP → AMP + 2 Pi) paid ONCE per fatty acid
    nadh: 1, // PER ROUND
    fadh2: 1, // PER ROUND
    requiresO2: true, // dead-ends into a backed-up carrier pool without OxPhos to cash them
    states: { fed: 0.3, fasted: 2, sprint: 1, rest: 1 },
    note: 'PER ROUND of the spiral: 1 NADH + 1 FADH₂ + 1 acetyl-CoA (0 substrate-level ATP). The atpEquiv −2 is the one-time activation toll (fatty acid → acyl-CoA costs 2 high-energy bonds), NOT per round. Palmitate (C16) = 7 rounds → 8 acetyl-CoA + 7 NADH + 7 FADH₂, ≈106 net ATP once TCA + OxPhos cash it all. Up in fasting; needs O₂ downstream.',
  },
  {
    id: 'ketogenesis',
    name: 'Ketogenesis',
    emoji: '🧪',
    location: 'Liver mitochondria (made) · peripheral tissue (used)',
    inputs: ['acetylCoA'],
    outputs: ['ketoneBodies'],
    atpEquiv: 0, // liver makes ketones but can't use them (no SCOT); no net ATP in the maker
    states: { fed: 0.1, fasted: 2, sprint: 0.3, rest: 0.7 },
    note: 'When β-oxidation floods acetyl-CoA past the TCA\'s OAA-limited ceiling (fasting/low-carb), the liver condenses acetyl-CoA → acetoacetate / β-hydroxybutyrate for export. The liver LACKS SCOT so it can\'t reuse them; brain & muscle re-cleave them to acetyl-CoA for their own TCA. Water-soluble brain fuel that spares glucose in starvation. Runs away in DKA.',
  },
  {
    id: 'fattyAcidSynthesis',
    name: 'Fatty Acid Synthesis',
    emoji: '🧱',
    location: 'Cytosol',
    inputs: ['acetylCoA', 'nadph'],
    outputs: ['palmitate'],
    atpEquiv: -7, // per palmitate: 7 ATP at acetyl-CoA carboxylase (the committed step)
    nadph: -14, // per palmitate: consumes 14 NADPH (supplied by PPP)
    irreversible: true, // ACC is the committed, one-way gate; not a reversal of β-oxidation
    states: { fed: 2, fasted: 0.1, sprint: 0, rest: 0.5 },
    note: 'PER PALMITATE (C16): builds 2 carbons at a time, costing 7 ATP (at ACC) + 14 NADPH (from PPP). A net CONSUMER of ATP and reducing power — the fed-state storage program, reciprocal with β-oxidation (its malonyl-CoA product blocks CPT-I so you don\'t burn and build at once). OFF in fasting/sprint.',
  },
  {
    id: 'ureaCycle',
    name: 'Urea Cycle',
    emoji: '💧',
    location: 'Liver (mitochondria → cytosol)',
    inputs: ['ammonia', 'aminoAcids', 'co2'],
    outputs: ['urea'],
    atpEquiv: -4, // 4 high-energy phosphate bonds to package 2 N as 1 urea
    states: { fed: 1, fasted: 1.3, sprint: 1, rest: 1 },
    note: 'PER UREA: −4 high-energy phosphate bonds (2 ATP → ADP at CPS-I, 1 ATP → AMP + PPi ≈ 2 bonds at argininosuccinate synthetase) to detoxify 2 nitrogens. The nitrogen-disposal sink coupled to glucogenic amino-acid catabolism: amino acids feed carbon skeletons to gluconeogenesis and their nitrogen here. Induced by high-protein diet and fasting muscle-protein breakdown.',
  },
];

const fuels: Fuel[] = [
  {
    id: 'glucose',
    name: 'Glucose',
    emoji: '🍬',
    entersAt: 'glycolysis',
    atpWhenFullyOxidized: 32, // glycolysis 2 + PDH×2 + TCA×2 + OxPhos, malate–aspartate shuttle
    note: '~30–32 ATP fully oxidized (2 substrate-level glycolysis + 2 GTP TCA + ~26–28 OxPhos). ~32 with the malate–aspartate shuttle valuing cytosolic NADH at ~2.5; ~30 with the glycerol-P shuttle (~1.5). Anaerobically (fermentation only): ~2.',
  },
  {
    id: 'glycogen',
    name: 'Glycogen',
    emoji: '🌳',
    entersAt: 'glycogenolysis',
    atpWhenFullyOxidized: 33, // +1 vs free glucose: phosphorolysis skips the hexokinase ATP
    note: 'One residue nets ~+1 ATP over free glucose because phosphorolysis frees glucose-1-P without spending the hexokinase ATP (glycolysis nets +3, not +2). ~33 fully oxidized; the payoff of pre-phosphorylated storage.',
  },
  {
    id: 'palmitate',
    name: 'Palmitate (C16)',
    emoji: '🥑',
    entersAt: 'betaOxidation',
    atpWhenFullyOxidized: 106, // modern P/O: −2 activation, 8 acetyl-CoA, 7 NADH + 7 FADH₂ from spiral
    note: '~106 net ATP (modern P/O). −2 activation toll; 7 β-ox rounds → 8 acetyl-CoA + 7 NADH + 7 FADH₂; TCA on 8 acetyl-CoA adds 8 GTP + 24 NADH + 8 FADH₂; OxPhos cashes 31 NADH (~77.5) + 15 FADH₂ (~22.5). Fat is the densest fuel per carbon.',
  },
  {
    id: 'lactate',
    name: 'Lactate',
    emoji: '🥛',
    entersAt: 'gluconeogenesis',
    atpWhenFullyOxidized: 15, // via lactate → pyruvate → PDH → TCA → OxPhos (one 3C unit)
    note: '~15 ATP if fully oxidized (LDH → pyruvate, then PDH + TCA + OxPhos on one 3C unit: 1 NADH from LDH + 1 from PDH + 4 from TCA carriers + 1 GTP ≈ 15). In the fasting liver it is instead re-forged into glucose (Cori cycle) at a net ATP COST — a fuel or a substrate depending on state.',
  },
  {
    id: 'glucogenicAminoAcid',
    name: 'Glucogenic amino acid',
    emoji: '🥩',
    entersAt: 'gluconeogenesis',
    atpWhenFullyOxidized: 15, // ~ a 3C skeleton oxidized; nitrogen costs 4 ATP at the urea cycle
    note: '~15 ATP if the deaminated carbon skeleton (e.g. alanine → pyruvate) is oxidized through TCA + OxPhos. In fasting it feeds gluconeogenesis instead; either way its nitrogen must be paid off (~−4 ATP) at the urea cycle. The bridge between protein, glucose, and nitrogen disposal.',
  },
  {
    id: 'glycerol',
    name: 'Glycerol',
    emoji: '💧',
    entersAt: 'gluconeogenesis',
    atpWhenFullyOxidized: 16, // glycerol → DHAP → glycolysis payoff + PDH + TCA + OxPhos, minus 1 ATP kinase
    note: '~16–17 ATP fully oxidized (glycerol kinase spends 1 ATP → glycerol-3-P → DHAP → enters glycolysis at the triose stage → pyruvate → PDH + TCA + OxPhos). The lipolysis backbone: the only part of a triglyceride that can become glucose (fatty-acyl carbons cannot).',
  },
];

export const NETMAP: NetMap = {
  metabolites,
  nodes,
  fuels,
};
