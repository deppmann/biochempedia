import type { Pathway } from '../types';

/* =============================================================================
   CITRIC ACID CYCLE (Krebs / TCA) — hand-authored, cross-checked against
   src/content/lessons/citric-acid-cycle/lesson.mdx. We model ONE turn: a
   2-carbon acetyl-CoA condenses onto 4-carbon oxaloacetate and, eight enzymes
   later, oxaloacetate comes back out unchanged — the single fact most students
   miss. Per acetyl-CoA the turn banks 3 NADH, 1 FADH₂, 1 GTP and releases 2 CO₂.

   `doubleAfter: 0` because we count one turn per acetyl-CoA; glucose feeds TWO
   acetyl-CoA, so double the ledger yourself for the per-glucose number. The
   cycle makes almost no ATP directly — its real product is high-energy
   electrons shipped to the electron transport chain.
   ============================================================================ */

export const citricAcidCycle: Pathway = {
  id: 'citric-acid-cycle',
  name: 'Citric Acid Cycle (Krebs / TCA)',
  emoji: '🌀',
  tagline: 'A roundabout, not a fuel tank. The oxaloacetate you start with is the oxaloacetate you finish with.',
  blurb:
    'One acetyl-CoA condenses onto oxaloacetate and runs a ring of eight mitochondrial enzymes. Two carbons leave as CO₂, but the real haul is electrons — 3 NADH and 1 FADH₂ (plus 1 GTP) — shipped to the electron transport chain, where your ATP is actually minted. Oxaloacetate comes back unchanged every turn: it is a catalyst, not a fuel.',
  difficulty: 3,
  location: 'Mitochondrial matrix (succinate dehydrogenase sits in the inner membrane)',
  netYield: 'Per acetyl-CoA: 3 NADH, 1 FADH₂, 1 GTP, 2 CO₂ (double it per glucose)',
  start: 'Acetyl-CoA + Oxaloacetate',
  startShort: 'AcCoA + OAA',
  startEmoji: '🌀',
  doubleAfter: 0, // one turn per acetyl-CoA; glucose = 2 acetyl-CoA, so double the ledger by hand
  lessonSlug: 'citric-acid-cycle',
  steps: [
    {
      n: 1,
      product: 'Citrate',
      short: 'Citrate',
      enzyme: 'Citrate synthase',
      irreversible: true,
      committed: true,
      emoji: '🤝',
      fact: 'THE committed step. A "synthase" spends no ATP — the energy comes free from cleaving acetyl-CoA’s high-energy thioester. Most exergonic step of the cycle (ΔG°′ ≈ −31.4 kJ/mol), effectively irreversible; it devours oxaloacetate, which is what pulls the whole ring forward.',
    },
    {
      n: 2,
      product: 'Isocitrate',
      short: 'Isocitrate',
      enzyme: 'Aconitase',
      emoji: '🔄',
      fact: 'An isomerization, not a redox step: dehydrate then rehydrate (via cis-aconitate) to move the hydroxyl onto a carbon that CAN be oxidized next. Uses a [4Fe-4S] cluster. Fluoroacetate → fluorocitrate jams it — one of Krebs’s diagnostic poisons.',
    },
    {
      n: 3,
      product: 'α-Ketoglutarate',
      short: 'α-KG',
      enzyme: 'Isocitrate dehydrogenase (IDH)',
      tokens: { nadh: 1, co2: 1 },
      irreversible: true,
      emoji: '🚦',
      fact: 'First oxidative decarboxylation: banks NADH #1 and releases CO₂ #1. The cycle’s RATE-LIMITING step and primary throttle — activated by ADP/Ca²⁺, inhibited by ATP/NADH. Mutant IDH makes the oncometabolite 2-hydroxyglutarate.',
    },
    {
      n: 4,
      product: 'Succinyl-CoA',
      short: 'Succinyl-CoA',
      enzyme: 'α-Ketoglutarate dehydrogenase complex',
      tokens: { nadh: 1, co2: 1 },
      irreversible: true,
      emoji: '🔥',
      fact: 'Second oxidative decarboxylation: NADH #2 and CO₂ #2. Mechanistic twin of pyruvate dehydrogenase — same E1/E2/E3 architecture, same five cofactors (TPP, lipoic acid, CoA, FAD, NAD⁺), same substrate channeling. Second control point: inhibited by NADH & succinyl-CoA, activated by Ca²⁺.',
    },
    {
      n: 5,
      product: 'Succinate',
      short: 'Succinate',
      enzyme: 'Succinyl-CoA synthetase',
      tokens: { gtp: 1 },
      emoji: '💰',
      fact: 'The cycle’s ONLY substrate-level phosphorylation. Cleaving succinyl-CoA’s thioester drives GDP → GTP (ATP in some tissues) through a phosphohistidine intermediate. Note "synthetase" (uses a nucleotide) vs step 1’s "synthase" (none) — the name tells you.',
    },
    {
      n: 6,
      product: 'Fumarate',
      short: 'Fumarate',
      enzyme: 'Succinate dehydrogenase (Complex II)',
      tokens: { fadh2: 1 },
      emoji: '🔌',
      fact: 'The only membrane-bound step — it IS Complex II of the electron transport chain, feeding electrons straight in. Uses FAD, not NAD⁺, because oxidizing a plain C–C bond releases too little energy for NAD⁺. Competitively inhibited by malonate (the classic traffic jam). Succinate is symmetric, so carbon tracking now needs reasoning, not memory.',
    },
    {
      n: 7,
      product: 'L-Malate',
      short: 'L-Malate',
      enzyme: 'Fumarase',
      emoji: '💧',
      fact: 'A stereospecific hydration — adds water across the double bond to make ONLY L-malate. Fumarate hydratase mutations let fumarate accumulate as an oncometabolite (hereditary leiomyomatosis and renal cell cancer).',
    },
    {
      n: 8,
      product: 'Oxaloacetate',
      short: 'OAA',
      enzyme: 'Malate dehydrogenase',
      tokens: { nadh: 1 },
      emoji: '♻️',
      fact: 'Regenerates oxaloacetate and banks NADH #3, closing the ring. Strongly unfavorable in isolation (very positive ΔG°′) — but citrate synthase devours OAA the instant it appears, pulling it forward. OAA comes out exactly as it went in: catalyst, not fuel.',
    },
  ],
  regulators: [
    { name: 'Citrate synthase', role: 'The committed step. Provides the thermodynamic pull; product-inhibited when citrate/ATP back up. Availability of its substrates (acetyl-CoA and oxaloacetate) sets the ceiling on flux.' },
    { name: 'Isocitrate dehydrogenase (IDH)', role: 'The main throttle / rate-limiting step. ↑ by ADP and Ca²⁺ (low energy charge = GO); ↓ by ATP and NADH (rich = STOP).' },
    { name: 'α-Ketoglutarate dehydrogenase', role: 'Second control point. ↓ by its own products NADH and succinyl-CoA; ↑ by Ca²⁺ during exercise. Same GO/STOP logic as IDH.' },
    { name: 'Ca²⁺ (the exercise signal)', role: 'The calcium that drives muscle contraction also directly activates IDH, α-KGDH (and PDH upstream) — matching fuel-burning to demand in real time.' },
    { name: 'Pyruvate carboxylase (anaplerosis)', role: 'Not in the ring, but it refills oxaloacetate (pyruvate + CO₂ → OAA). Feedforward-activated by acetyl-CoA: "fuel is arriving, build more of the jig."' },
  ],
  scenarios: [
    {
      id: 'tca-exercise',
      emoji: '🏋️',
      title: 'Sprinting up the stairs — cardiac & skeletal muscle firing',
      scene: 'Muscle is contracting hard. Every contraction dumps Ca²⁺ into the cytosol and matrix, ATP is being spent fast, and ADP is climbing. The cell needs to burn fuel to match demand.',
      hormones: 'ADP ↑ · Ca²⁺ ↑ · ATP/NADH falling',
      flux: 'up',
      decisions: [
        {
          q: 'Which way should the cycle run right now?',
          choices: ['Ramp UP — burn fuel to regenerate ATP', 'Shut DOWN — conserve intermediates'],
          answer: 0,
          why: 'High ATP demand + low energy charge = GO. The cycle floods to fill NADH/FADH₂ carriers for the ETC, which is where the ATP is actually made.',
        },
        {
          q: 'What does the rising Ca²⁺ do to isocitrate and α-ketoglutarate dehydrogenase?',
          choices: ['Activates both control points', 'Inhibits both control points'],
          answer: 0,
          why: 'Ca²⁺ is the exercise signal: the same ion that drives contraction directly ACTIVATES IDH and α-KGDH (and PDH upstream), so fuel-burning tracks contraction beat-for-beat.',
        },
        {
          q: 'ADP is climbing. Its effect on the cycle?',
          choices: ['Activator — it signals low energy charge (GO)', 'Inhibitor — high phosphate potential (STOP)'],
          answer: 0,
          why: 'ADP means ATP has been spent. It relieves inhibition at IDH and pushes flux up. ATP and NADH are the STOP signals; ADP, NAD⁺ and Ca²⁺ are GO.',
        },
      ],
      teach: 'EXERCISE = GO. Ca²⁺ activates the two dehydrogenase control points while rising ADP (low energy charge) relieves the ATP/NADH brakes. Both signals push flux up so the cycle keeps carriers charged for the ETC. This is the energy-charge rule in its purest form: ATP/NADH = STOP, ADP/Ca²⁺ = GO.',
    },
    {
      id: 'tca-rest',
      emoji: '🛋️',
      title: 'Resting on the couch, well-fed',
      scene: 'You just ate and you are doing nothing. ATP is plentiful, NADH is high, and there is no demand to make more energy. Fuel keeps arriving anyway.',
      hormones: 'ATP ↑ · NADH ↑ · ADP low',
      flux: 'down',
      decisions: [
        {
          q: 'Cycle flux in a rich, resting cell?',
          choices: ['Slowed — the cell is energy-rich, no need to burn', 'Maxed out — spare fuel is arriving'],
          answer: 0,
          why: 'High ATP and NADH are STOP signals. With energy charge high, the cell throttles the cycle down at IDH and α-KGDH rather than burning fuel it does not need.',
        },
        {
          q: 'What happens to the acetyl-CoA and citrate that build up when the cycle is throttled?',
          choices: ['Citrate is exported to the cytosol to seed fatty-acid synthesis', 'They are dumped as waste CO₂'],
          answer: 0,
          why: 'When ATP is high, citrate leaves the mitochondrion and feeds fatty-acid synthesis (store the surplus). The cycle is amphibolic — its intermediates are raw material, not just fuel.',
        },
      ],
      teach: 'REST + FED = STOP. High ATP/NADH slows the cycle at its two dehydrogenase control points. The building-block carbons don’t vanish — surplus citrate exports to build fat, showing the cycle’s amphibolic (dual catabolic/anabolic) nature.',
    },
    {
      id: 'tca-hypoxia',
      emoji: '💨',
      title: 'Oxygen cut off — a clot blocks blood flow',
      scene: 'Tissue is suddenly starved of oxygen. No enzyme of the cycle uses O₂ as a substrate, yet within seconds the whole roundabout grinds to a halt. Why?',
      hormones: 'O₂ ↓↓ · ETC backed up · NADH stuck high',
      flux: 'off',
      decisions: [
        {
          q: 'Is oxygen a direct substrate of any of the eight cycle steps?',
          choices: ['No — O₂ appears in none of the eight reactions', 'Yes — succinate dehydrogenase uses O₂'],
          answer: 0,
          why: 'Look at all eight steps: no O₂. It is the terminal electron acceptor of the ETC, one step removed from the cycle. "Required but not a substrate" is the trick-question answer.',
        },
        {
          q: 'So why does the cycle stall without oxygen?',
          choices: ['The ETC can’t reoxidize NADH → NAD⁺, so the dehydrogenases run out of oxidized carrier', 'CO₂ can’t be released without O₂'],
          answer: 0,
          why: 'No O₂ → ETC backs up → NADH stays reduced → the small fixed NAD⁺ pool empties. Isocitrate DH, α-KG DH and malate DH have no NAD⁺ to reduce, so the ring stops.',
        },
        {
          q: 'Which single step could, in principle, still turn once using its own membrane carrier?',
          choices: ['Succinate dehydrogenase (its FADH₂ passes electrons straight into the chain — it IS Complex II)', 'Citrate synthase'],
          answer: 0,
          why: 'SDH IS Complex II and reduces its own FAD, but with the ETC backed up even that stalls. The point stands: everything downstream of a full ETC freezes because carriers can’t be emptied.',
        },
      ],
      teach: 'HYPOXIA = OFF. Oxygen is never a substrate of the cycle, but it is the ETC’s terminal electron acceptor. Remove it and the ETC can’t regenerate NAD⁺/FAD; the cycle runs out of empty batteries and stalls within seconds. Required, but not a substrate — the highest-yield distinction in the chapter.',
    },
    {
      id: 'tca-anaplerosis',
      emoji: '🧱',
      title: 'A liver cell siphoning intermediates for biosynthesis',
      scene: 'The cell is pulling α-ketoglutarate off to make glutamate and succinyl-CoA off to make heme. Every intermediate removed for building means less oxaloacetate at the end of the turn.',
      hormones: 'Biosynthetic drain ↑ · acetyl-CoA available',
      flux: 'down',
      decisions: [
        {
          q: 'If intermediates are drained for biosynthesis (cataplerosis), what threatens the cycle?',
          choices: ['Oxaloacetate runs low, so citrate synthase can’t start the next turn', 'Too much NADH is made'],
          answer: 0,
          why: 'Draining any intermediate ultimately lowers oxaloacetate. Without OAA to condense with acetyl-CoA, step 1 stalls and the whole cycle slows — the catalyst has been carried off.',
        },
        {
          q: 'How does the cell refill oxaloacetate (anaplerosis)?',
          choices: ['Pyruvate carboxylase adds CO₂ to pyruvate → oxaloacetate', 'Citrate synthase runs backward to make OAA'],
          answer: 0,
          why: 'Pyruvate carboxylase (biotin-dependent) is the chief anaplerotic refill: pyruvate + CO₂ → OAA. Citrate synthase is effectively irreversible and cannot run backward.',
        },
        {
          q: 'What switches pyruvate carboxylase ON?',
          choices: ['Acetyl-CoA (a feedforward "fuel is arriving, build more jig" signal)', 'High ATP directly inhibits it'],
          answer: 0,
          why: 'Acetyl-CoA allosterically activates pyruvate carboxylase: if acetyl-CoA is piling up with nowhere to go, the cell reads it as "need more oxaloacetate" and makes some.',
        },
      ],
      teach: 'AMPHIBOLIC BALANCE. The cycle both burns fuel (catabolic) and donates carbon skeletons for amino acids, heme, and gluconeogenesis (anabolic). Siphoning intermediates = cataplerosis; the counter is anaplerosis, chiefly pyruvate carboxylase (pyruvate + CO₂ → OAA), feedforward-activated by acetyl-CoA to keep oxaloacetate — the catalyst — from running out.',
    },
    {
      id: 'tca-warburg',
      emoji: '🦠',
      title: 'A tumor cell running the Warburg effect',
      scene: 'A cancer cell has plenty of oxygen but is fermenting glucose to lactate anyway, throttling oxidation through the cycle. Some tumors carry mutations right in the cycle’s enzymes.',
      hormones: 'Oncogenic rewiring · aerobic glycolysis favored',
      flux: 'down',
      decisions: [
        {
          q: 'What is the "Warburg effect"?',
          choices: ['Tumors favor glycolysis-to-lactate even when oxygen is plentiful', 'Tumors run the cycle faster than normal cells'],
          answer: 0,
          why: 'Named for Otto Warburg (Krebs’s mentor): cancer cells lean on aerobic glycolysis, dialing DOWN full oxidation through the cycle even with O₂ available — building blocks and fast ATP over efficiency.',
        },
        {
          q: 'Mutant isocitrate dehydrogenase (IDH) in a glioma does what?',
          choices: ['Gains a new activity making the oncometabolite 2-hydroxyglutarate', 'Simply stops working, with no downstream signal'],
          answer: 0,
          why: 'Neomorphic mutant IDH converts α-ketoglutarate to 2-hydroxyglutarate, which scrambles DNA/histone methylation. It’s a gain-of-function lesion — and IDH inhibitors are now approved drugs.',
        },
        {
          q: 'Loss-of-function mutations in succinate dehydrogenase or fumarase cause cancer how?',
          choices: ['Succinate/fumarate pile up as oncometabolites that remodel the epigenome', 'They halt ATP synthesis so cells die'],
          answer: 0,
          why: 'When SDH or fumarase fail, succinate or fumarate accumulate and competitively inhibit α-ketoglutarate–dependent dioxygenases, rewiring gene expression → paragangliomas and kidney cancer.',
        },
      ],
      teach: 'CLINICAL / CANCER. The cycle is also a signaling node. Warburg tumors dial oxidation down in favor of aerobic glycolysis; and three cycle lesions converge on the epigenome — gain-of-function IDH makes 2-hydroxyglutarate, while loss of SDH or fumarase lets succinate/fumarate accumulate as oncometabolites. All three inhibit α-KG–dependent dioxygenases, and that axis is now druggable.',
    },
  ],
  diseases: [
    {
      id: 'pdh-deficiency',
      name: 'Pyruvate dehydrogenase (PDH) complex deficiency',
      emoji: '🧠',
      vignette:
        'An infant has developmental delay, poor muscle tone, and a persistent lactic acidosis that WORSENS after a high-carbohydrate meal. Serum lactate and pyruvate are both high, but pyruvate feeding gives no clinical benefit. A ketogenic (high-fat) diet helps.',
      suspects: ['Pyruvate dehydrogenase complex', 'Succinate dehydrogenase', 'Citrate synthase', 'Malate dehydrogenase'],
      answer: 0,
      accumulates: 'Pyruvate and lactate (pyruvate is shunted to lactate)',
      missing: 'Acetyl-CoA from carbohydrate — the cycle is starved of fuel',
      teach:
        'PDH is the gate that turns pyruvate into acetyl-CoA, the cycle’s fuel. Block it and glucose-derived pyruvate cannot enter the cycle; it piles up and is dumped to lactate → lactic acidosis that a carb load makes worse. The brain, which leans hard on glucose oxidation, suffers most. A ketogenic diet works because fatty acids and ketones make acetyl-CoA by β-oxidation, bypassing the broken PDH gate entirely.',
      pearl: 'PDH deficiency = lactic acidosis + neuro signs that WORSEN on carbs and improve on a ketogenic (high-fat) diet — because fat makes acetyl-CoA without PDH.',
    },
    {
      id: 'fluoroacetate',
      name: 'Fluoroacetate poisoning (a mechanism, not a gene)',
      emoji: '☠️',
      vignette:
        'A ranch worker is exposed to compound 1080 (fluoroacetate) rodenticide. Within an hour: seizures, cardiac arrhythmia, and a lab report showing citrate massively elevated while downstream cycle intermediates run dry. ATP production collapses.',
      suspects: ['Aconitase (blocked by fluorocitrate)', 'Isocitrate dehydrogenase', 'α-Ketoglutarate dehydrogenase', 'Succinyl-CoA synthetase'],
      answer: 0,
      accumulates: 'Citrate (backs up behind the block)',
      missing: 'Everything downstream — isocitrate onward, so no NADH/FADH₂/GTP from the cycle',
      teach:
        'Fluoroacetate is a classic "lethal synthesis": the cell itself converts it (via citrate synthase) to fluorocitrate, a suicide inhibitor that jams aconitase (step 2). Citrate floods behind the block while every downstream intermediate runs dry — exactly the traffic-jam pattern Krebs used to ORDER the cycle. With the cycle stalled, oxidative ATP production fails; heart and brain, the most energy-hungry tissues, fail first.',
      pearl: 'Fluoroacetate → fluorocitrate blocks aconitase → citrate accumulates, downstream drains. The "poison and watch the traffic jam" logic that proved the cycle’s sequence.',
    },
    {
      id: 'sdh-paraganglioma',
      name: 'Succinate dehydrogenase (SDH) deficiency · hereditary paraganglioma',
      emoji: '🧬',
      vignette:
        'A young adult with a family history presents with a catecholamine-secreting paraganglioma. Tumor metabolomics show markedly elevated succinate, and immunostaining for the SDHB subunit is lost. No lactic acidosis crisis — this is a chronic, tumor-driving lesion.',
      suspects: ['Succinate dehydrogenase (Complex II)', 'Fumarase', 'Aconitase', 'Citrate synthase'],
      answer: 0,
      accumulates: 'Succinate (an oncometabolite)',
      missing: 'Fumarate formation at step 6 and the FADH₂ fed into Complex II',
      teach:
        'SDH is both cycle step 6 AND Complex II of the ETC. Loss-of-function mutations let succinate accumulate; the excess succinate leaks to the cytosol and competitively inhibits α-ketoglutarate–dependent dioxygenases, stabilizing HIF and remodeling the epigenome → pseudohypoxic, growth-promoting signaling. The result is paragangliomas/pheochromocytomas, not an acute energy crisis.',
      pearl: 'SDH is the only enzyme shared by the cycle and the ETC (Complex II). Lose it and succinate becomes an ONCOMETABOLITE → hereditary paraganglioma. Same story for fumarase → succinate’s cousin fumarate → kidney cancer.',
    },
  ],
  quiz: [
    {
      tag: 'energetics',
      stem: 'For one acetyl-CoA making one complete turn of the citric acid cycle, what is the correct tally of reduced carriers, high-energy phosphate, and CO₂?',
      choices: [
        '3 NADH, 1 FADH₂, 1 GTP, 2 CO₂',
        '4 NADH, 1 FADH₂, 1 GTP, 2 CO₂',
        '3 NADH, 2 FADH₂, 1 GTP, 3 CO₂',
        '2 NADH, 1 FADH₂, 2 GTP, 2 CO₂',
      ],
      answer: 0,
      rationale:
        'Per acetyl-CoA: NADH from isocitrate DH, α-KG DH, and malate DH (3 total); FADH₂ from succinate DH (1); GTP from succinyl-CoA synthetase (1); CO₂ from the two oxidative decarboxylations (2). Per GLUCOSE you double this (two acetyl-CoA). The distractors miscount one carrier each.',
    },
    {
      tag: 'basics',
      stem: 'A student says the citric acid cycle’s main job is to make ATP directly. What is the best correction?',
      choices: [
        'Its main product is reduced electron carriers (3 NADH + 1 FADH₂); it makes only 1 GTP directly',
        'It makes most of the cell’s ATP via substrate-level phosphorylation at four separate steps',
        'It makes no ATP or GTP at all — all the energy leaves as heat',
        'Its main product is CO₂, which is later converted to ATP in the lungs',
      ],
      answer: 0,
      rationale:
        'The cycle’s real product is high-energy electrons on NADH and FADH₂, cashed later at the ETC. Only one direct high-energy phosphate is made (GTP, at succinyl-CoA synthetase) — the sole substrate-level phosphorylation, not four. The "no GTP at all" and "CO₂ → ATP in the lungs" options are simply false.',
    },
    {
      tag: 'basics',
      stem: 'Oxaloacetate is described as catalytic in the cycle. Which statement best supports that label?',
      choices: [
        'It is regenerated unchanged at the end of each turn, so one molecule can run many turns',
        'It is consumed each turn and must be replaced from glucose',
        'It is the molecule oxidized to the two CO₂ released each turn',
        'It donates the high-energy phosphate that becomes GTP',
      ],
      answer: 0,
      rationale:
        'A catalyst is regenerated unchanged. Oxaloacetate enters at citrate synthase and is reformed at malate dehydrogenase, so a single molecule turns the ring repeatedly; the fuel actually consumed is acetyl-CoA. The GTP phosphate comes from succinyl-CoA’s thioester, and the CO₂ carbons come from the intermediates broadly — not from OAA being burned away.',
    },
    {
      tag: 'basics',
      stem: 'Is molecular oxygen (O₂) a substrate of any step in the citric acid cycle, and if not, why does the cycle still stop within seconds when O₂ is removed?',
      choices: [
        'No — O₂ is in none of the eight steps; removing it backs up the ETC, so NAD⁺/FAD can’t be regenerated and the dehydrogenases stall',
        'Yes — succinate dehydrogenase uses O₂ directly, so that step fails first',
        'Yes — O₂ is a substrate of malate dehydrogenase',
        'No — but CO₂ cannot be released without O₂, blocking isocitrate dehydrogenase',
      ],
      answer: 0,
      rationale:
        'None of the eight reactions use O₂. O₂ is the ETC’s terminal electron acceptor; without it the chain backs up, NADH/FADH₂ stay reduced, the small fixed NAD⁺/FAD pool empties, and the oxidative steps have no oxidized carrier. "Required but not a substrate" is the point. CO₂ release does not need O₂, and neither SDH nor MDH uses O₂ as a substrate.',
    },
    {
      tag: 'regulation',
      stem: 'In a contracting cardiac muscle cell, intracellular Ca²⁺ rises sharply and ADP increases. What is the combined effect on the cycle?',
      choices: [
        'Ca²⁺ activates isocitrate and α-ketoglutarate dehydrogenase, and the rising ADP (low energy charge) further promotes flux — the cycle speeds up',
        'Ca²⁺ and ADP both inhibit the two dehydrogenases, slowing the cycle to conserve fuel',
        'Ca²⁺ inhibits the cycle but ADP overrides it, producing no net change',
        'Ca²⁺ activates citrate synthase only, while ADP has no regulatory role',
      ],
      answer: 0,
      rationale:
        'Energy-charge rule: ADP and Ca²⁺ are GO signals; ATP and NADH are STOP. Ca²⁺ released to drive contraction directly activates IDH and α-KGDH (and PDH), while rising ADP signals low energy charge and relieves inhibition. Both push flux up to match demand. The other options invert the logic or misassign the control points.',
    },
    {
      tag: 'regulation',
      stem: 'Two enzymes are the cycle’s main control points, and one distinct enzyme is the committed step that provides the thermodynamic pull. Which choice pairs these correctly?',
      choices: [
        'Control points = isocitrate DH and α-ketoglutarate DH; committed step = citrate synthase',
        'Control points = citrate synthase and aconitase; committed step = isocitrate DH',
        'Control points = succinate DH and malate DH; committed step = fumarase',
        'Control points = citrate synthase and pyruvate kinase; committed step = α-ketoglutarate DH',
      ],
      answer: 0,
      rationale:
        'The two oxidative decarboxylations — isocitrate dehydrogenase (rate-limiting/primary throttle) and α-ketoglutarate dehydrogenase — are the regulated control points. Citrate synthase is the committed, most-exergonic step that pulls the cycle forward but is distinct from the throttle. Pyruvate kinase belongs to glycolysis, not the cycle.',
    },
    {
      tag: 'disease',
      stem: 'Malonate is added to actively respiring mitochondria. Shortly afterward, which intermediate pattern is expected, and why?',
      choices: [
        'Succinate accumulates while fumarate and downstream intermediates fall — malonate competitively inhibits succinate dehydrogenase',
        'Fumarate accumulates while succinate is depleted, because malonate blocks fumarase',
        'All eight intermediates rise equally because the cycle is a closed loop',
        'Oxaloacetate accumulates because it can no longer be consumed',
      ],
      answer: 0,
      rationale:
        'Malonate (succinate minus one CH₂) is the classic competitive inhibitor of succinate dehydrogenase. Block step 6 and its substrate succinate backs up while fumarate, malate, and OAA run dry — the traffic-jam pattern. A closed loop does not mean uniform accumulation; OAA is downstream of the block, so it falls, not rises.',
    },
    {
      tag: 'disease',
      stem: 'A glioma carries a neomorphic (gain-of-function) mutation in isocitrate dehydrogenase that diverts α-ketoglutarate to 2-hydroxyglutarate instead of running the normal reaction. Beyond epigenetic effects, what is the immediate consequence for the cycle in cells relying on the mutant enzyme?',
      choices: [
        'Loss of the normal oxidative decarboxylation at step 3, reducing forward flux and NADH yield',
        'Increased NADH output from step 3, accelerating the cycle',
        'Accumulation of oxaloacetate from faster malate dehydrogenase activity',
        'No change, because α-ketoglutarate dehydrogenase fully compensates for step 3',
      ],
      answer: 0,
      rationale:
        'Isocitrate dehydrogenase normally performs the rate-limiting oxidative decarboxylation (isocitrate → α-KG + CO₂ + NADH). Diverting α-KG to 2-hydroxyglutarate undercuts forward flux and NADH production at this control point, so the cycle slows. α-KG dehydrogenase acts downstream on α-KG and cannot replace the step-3 reaction; OAA would not accumulate from this lesion.',
    },
    {
      tag: 'integration',
      stem: 'You feed isolated mitochondria acetyl-CoA labeled with ¹⁴C at both acetyl carbons and allow exactly one turn. Where is the ¹⁴C after that single turn?',
      choices: [
        'Retained in the four-carbon intermediates (succinate/malate/OAA); the two CO₂ lost this turn come from oxaloacetate-derived carbons',
        'Entirely released as the two ¹⁴CO₂ molecules during that turn',
        'Split evenly — half in CO₂, half in citrate',
        'Absent from all intermediates, because acetyl-CoA never joins the carbon skeleton',
      ],
      answer: 0,
      rationale:
        'Classic isotope result: the two CO₂ lost in a given turn derive from the oxaloacetate carbons, not the acetyl carbons that just entered. The labeled acetyl carbons stay in the four-carbon skeleton and only exit as CO₂ on later turns. Because the molecule becomes symmetric at succinate (and fumarate), the label distributes across both ends but is retained after one turn — not fully released or absent.',
    },
    {
      tag: 'integration',
      stem: 'Cataplerosis pulls α-ketoglutarate and succinyl-CoA out of the cycle for amino-acid and heme synthesis. If nothing counteracts this drain, why does the cycle slow, and what restores it?',
      choices: [
        'Oxaloacetate falls, starving citrate synthase; pyruvate carboxylase (pyruvate + CO₂ → OAA) refills it (anaplerosis)',
        'NADH falls, starving the ETC; the malate–aspartate shuttle refills NADH',
        'Acetyl-CoA falls, so β-oxidation must speed up to replace it',
        'GTP falls, so succinyl-CoA synthetase runs backward to restore it',
      ],
      answer: 0,
      rationale:
        'Draining any intermediate ultimately lowers oxaloacetate, and without OAA the committed step (citrate synthase) cannot start the next turn. The chief anaplerotic refill is pyruvate carboxylase, adding CO₂ to pyruvate to make OAA, and it is feedforward-activated by acetyl-CoA. This anaplerosis/cataplerosis balance is what makes the cycle amphibolic.',
    },
  ],
  funFact:
    'Hans Krebs first submitted the cycle to Nature in 1937 — and it was rejected for a crowded correspondence column, not on the science. He published it in Enzymologia instead, won the 1953 Nobel Prize, and kept the rejection slip; Nature itself called the rejection an "egregious error" in 1988.',
};
