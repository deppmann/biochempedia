import type { Pathway } from '../types';

/* =============================================================================
   GLYCOLYSIS — the exemplar pathway (hand-authored, cross-checked against
   src/content/lessons/glycolysis/lesson.mdx). Ten steps, glucose → 2 pyruvate,
   net +2 ATP / +2 NADH. `doubleAfter: 4` makes the ledger double every yield
   after the aldolase cleavage, exactly as the lesson insists students must.
   ============================================================================ */

export const glycolysis: Pathway = {
  id: 'glycolysis',
  name: 'Glycolysis',
  emoji: '🍬',
  tagline: 'Spend a little ATP to make a lot. The oldest hustle in biology.',
  blurb:
    'One glucose becomes two pyruvate in ten cytosolic steps — no oxygen required. Two ATP invested up front, four earned in the payoff, two NADH banked. Fast, ancient, and running in nearly every cell alive.',
  difficulty: 2,
  location: 'Cytosol',
  netYield: 'Net +2 ATP, +2 NADH per glucose',
  start: 'Glucose',
  startShort: 'Glucose',
  startEmoji: '🍬',
  doubleAfter: 4, // aldolase splits 6C → two 3C; everything after counts ×2
  lessonSlug: 'glycolysis',
  steps: [
    {
      n: 1,
      product: 'Glucose-6-phosphate',
      short: 'G6P',
      enzyme: 'Hexokinase',
      tokens: { atp: -1 },
      irreversible: true,
      emoji: '🔒',
      fact: 'Spends 1 ATP. Induced fit clamps shut around glucose to exclude water (no futile hydrolysis), and the charge traps the sugar inside the cell. Product-inhibited by G6P.',
      misconception: { grab: 'ATP', why: 'Trap! Hexokinase is a kinase that SPENDS ATP (−1) here — the investment phase. Don’t bank a +ATP; pay the toll.' },
    },
    {
      n: 2,
      product: 'Fructose-6-phosphate',
      short: 'F6P',
      enzyme: 'Phosphoglucose isomerase',
      emoji: '🔄',
      fact: 'Aldose → ketose. A freely reversible isomerization that sets up a symmetric molecule the cell can later cut cleanly in half.',
    },
    {
      n: 3,
      product: 'Fructose-1,6-bisphosphate',
      short: 'F1,6BP',
      enzyme: 'Phosphofructokinase-1 (PFK-1)',
      tokens: { atp: -1 },
      irreversible: true,
      committed: true,
      emoji: '🚦',
      fact: 'THE committed step. Spends the 2nd ATP. Master throttle: inhibited by ATP & citrate, activated by AMP & fructose-2,6-bisphosphate. Once past here, the sugar is going all the way.',
    },
    {
      n: 4,
      product: 'DHAP + Glyceraldehyde-3-P',
      short: 'DHAP + G3P',
      enzyme: 'Aldolase',
      emoji: '✂️',
      fact: 'The big split: one 6-carbon sugar → two 3-carbon trioses. From here on, every yield counts ×2.',
    },
    {
      n: 5,
      product: 'Glyceraldehyde-3-phosphate (×2)',
      short: 'G3P ×2',
      enzyme: 'Triose phosphate isomerase',
      emoji: '👯',
      fact: 'Converts DHAP into a second G3P so BOTH halves run the payoff phase. The classic TIM-barrel, one of the most catalytically perfect enzymes known.',
    },
    {
      n: 6,
      product: '1,3-Bisphosphoglycerate',
      short: '1,3-BPG',
      enzyme: 'GAPDH',
      tokens: { nadh: 1 },
      emoji: '🔋',
      fact: 'The ONLY oxidation. Grabs inorganic phosphate (Pi, not ATP!) and banks the energy as NADH, forming a high-energy acyl-phosphate via an active-site cysteine.',
      misconception: { grab: 'ATP', why: 'Trap! GAPDH makes NADH using inorganic phosphate (Pi) — NO ATP is made here. The energy is banked in the high-energy 1,3-BPG for step 7 to cash.' },
    },
    {
      n: 7,
      product: '3-Phosphoglycerate',
      short: '3-PG',
      enzyme: 'Phosphoglycerate kinase',
      tokens: { atp: 1 },
      emoji: '💰',
      fact: 'First payoff! Substrate-level phosphorylation hands the phosphate straight to ADP → ATP. No membrane, no oxygen, just one enzyme.',
    },
    {
      n: 8,
      product: '2-Phosphoglycerate',
      short: '2-PG',
      enzyme: 'Phosphoglycerate mutase',
      emoji: '📍',
      fact: 'Moves the phosphate from C3 to C2 — repositioning it so the next step can make a truly high-energy compound.',
    },
    {
      n: 9,
      product: 'Phosphoenolpyruvate',
      short: 'PEP',
      enzyme: 'Enolase',
      emoji: '⚡',
      fact: 'A dehydration traps PEP as a high-energy enol — the highest phosphoryl-transfer potential in the whole pathway.',
    },
    {
      n: 10,
      product: 'Pyruvate',
      short: 'Pyruvate',
      enzyme: 'Pyruvate kinase',
      tokens: { atp: 1 },
      irreversible: true,
      emoji: '🏁',
      fact: 'Second payoff & the finish line. Irreversible and regulated (feed-forward activated by fructose-1,6-bisphosphate). Pyruvate’s fate is the real bottleneck — it must regenerate NAD⁺.',
    },
  ],
  regulators: [
    { name: 'Hexokinase', role: 'Step 1 gate. Product-inhibited by its own G6P — a simple "stop if backed up" brake.' },
    { name: 'PFK-1', role: 'The committed step & master throttle. ↑ by AMP and fructose-2,6-BP; ↓ by ATP, citrate, and low pH.' },
    { name: 'PFK-2 / FBPase-2', role: 'Sets fructose-2,6-BP. Insulin (fed) ↑ it → glycolysis ON. Glucagon (fasting, via PKA) ↓ it → glycolysis OFF.' },
    { name: 'Pyruvate kinase', role: 'Step 10 gate. Feed-forward activated by F-1,6-BP; in liver, phosphorylated OFF by glucagon.' },
  ],
  scenarios: [
    {
      id: 'gly-fed',
      emoji: '🥞',
      title: 'You demolished a pancake breakfast',
      scene: 'Blood glucose is spiking. The pancreas is dumping insulin. Your liver needs to pull glucose out of the blood and burn/store it.',
      hormones: 'Insulin ↑ · glucagon ↓',
      flux: 'up',
      decisions: [
        {
          q: 'Which way should glycolysis run right now?',
          choices: ['Ramp UP — burn the incoming glucose', 'Shut DOWN — save glucose for later'],
          answer: 0,
          why: 'Fed state = plenty of fuel arriving. The liver runs glycolysis forward to use and store the glucose flood.',
        },
        {
          q: 'What happens to fructose-2,6-bisphosphate?',
          choices: ['Rises (insulin activates PFK-2)', 'Falls (glucagon activates FBPase-2)'],
          answer: 0,
          why: 'Insulin → dephosphorylates the bifunctional enzyme → PFK-2 active → F-2,6-BP RISES → PFK-1 turns ON. This is the switch that says "fed."',
        },
        {
          q: 'PFK-1 activity?',
          choices: ['Activated', 'Inhibited'],
          answer: 0,
          why: 'High F-2,6-BP is the most potent activator of PFK-1. Glycolysis floors it.',
        },
      ],
      teach: 'FED = insulin high → F-2,6-BP high → PFK-1 ON → glycolysis runs forward. The liver clears the glucose spike. This is the reciprocal opposite of the fasting/gluconeogenesis program.',
    },
    {
      id: 'gly-sprint',
      emoji: '🏃',
      title: 'Sprinting for the bus',
      scene: 'Your leg muscles need ATP NOW — faster than blood can deliver oxygen. Mitochondria can’t keep up. ADP and AMP are climbing.',
      hormones: 'Local energy charge falling (AMP ↑)',
      flux: 'up',
      decisions: [
        {
          q: 'Glycolytic flux in the sprinting muscle?',
          choices: ['Way UP — it’s the fast anaerobic ATP source', 'Down — muscle waits for oxygen'],
          answer: 0,
          why: 'Anaerobic glycolysis is the only way to make ATP fast without oxygen. Muscle leans on it hard during a sprint.',
        },
        {
          q: 'What activates PFK-1 here?',
          choices: ['AMP (rising as ATP is spent)', 'Citrate (rising from the TCA cycle)'],
          answer: 0,
          why: 'AMP rises when ATP is consumed and signals "low energy — go!" It activates PFK-1. Citrate would signal the opposite (fuel is plentiful).',
        },
        {
          q: 'To keep running, pyruvate must become…',
          choices: ['Lactate (regenerates NAD⁺ so GAPDH can keep firing)', 'Acetyl-CoA (needs oxygen)'],
          answer: 0,
          why: 'With no oxygen, lactate dehydrogenase reoxidizes NADH → NAD⁺, keeping the fixed NAD⁺ pool available for GAPDH. The lactate isn’t the fatigue — it’s the rescue.',
        },
      ],
      teach: 'SPRINT = high ATP demand, low O₂. AMP activates PFK-1, glycolysis floods, and lactate fermentation regenerates NAD⁺ so the pathway doesn’t stall. Lactate travels to the liver (Cori cycle) to be rebuilt into glucose.',
    },
    {
      id: 'gly-fast',
      emoji: '😴',
      title: 'Overnight fast — 12 hours since dinner',
      scene: 'Blood glucose is drifting down. The brain still needs glucose. The pancreas switches from insulin to glucagon, and the liver’s job flips: MAKE glucose, don’t burn it.',
      hormones: 'Glucagon ↑ · insulin ↓',
      flux: 'down',
      decisions: [
        {
          q: 'Should the LIVER run glycolysis now?',
          choices: ['No — shut it down and make glucose instead', 'Yes — burn glucose for energy'],
          answer: 0,
          why: 'The fasting liver’s job is to EXPORT glucose to the brain. Burning it via glycolysis would be self-defeating. Glycolysis off, gluconeogenesis on.',
        },
        {
          q: 'Fructose-2,6-bisphosphate level?',
          choices: ['Low (glucagon → PKA → FBPase-2 active)', 'High (as in the fed state)'],
          answer: 0,
          why: 'Glucagon activates PKA, which phosphorylates the bifunctional enzyme to its FBPase-2 mode → F-2,6-BP FALLS → PFK-1 off, FBPase-1 on. Glycolysis brakes, gluconeogenesis accelerates.',
        },
      ],
      teach: 'FASTING = glucagon high → F-2,6-BP low → PFK-1 OFF in the liver. The same switch that turned glycolysis ON when fed turns it OFF when fasting — reciprocal regulation so the two opposite pathways never run a futile cycle at once.',
    },
    {
      id: 'gly-rbc',
      emoji: '🩸',
      title: 'A red blood cell, any time of day',
      scene: 'This cell has no mitochondria and no nucleus. Glycolysis is its ENTIRE energy economy — there is no backup plan.',
      hormones: 'n/a — RBC has no oxidative option',
      flux: 'up',
      decisions: [
        {
          q: 'How does an RBC make ATP?',
          choices: ['Glycolysis only (→ lactate)', 'Oxidative phosphorylation'],
          answer: 0,
          why: 'No mitochondria = no TCA cycle, no electron transport chain. The RBC lives entirely on glycolytic (substrate-level) ATP and exports lactate.',
        },
        {
          q: 'If you block lactate dehydrogenase in an RBC, what stalls the pathway?',
          choices: ['NAD⁺ can’t be regenerated → GAPDH halts', 'ATP piles up and activates PFK-1'],
          answer: 0,
          why: 'LDH is the RBC’s only way to reoxidize NADH → NAD⁺. Block it and the small fixed NAD⁺ pool empties, GAPDH (step 6) stalls, and ATP production stops within seconds.',
        },
      ],
      teach: 'The RBC is the purest case: glycolysis is the whole show, and its ceiling is set by NAD⁺ regeneration via lactate — not by glucose supply.',
    },
    {
      id: 'gly-diabetes',
      emoji: '🍭',
      title: 'Uncontrolled Type 1 diabetes',
      scene: 'Blood glucose is sky-high, but there’s almost no insulin. The liver can’t "hear" that fuel is abundant — it reads the low insulin as starvation.',
      hormones: 'Insulin ↓↓ · glucagon ↑ (unopposed)',
      flux: 'down',
      decisions: [
        {
          q: 'What does the liver do with glycolysis despite the high blood glucose?',
          choices: ['Keeps it OFF — it "thinks" it’s starving', 'Runs it hard — glucose is everywhere'],
          answer: 0,
          why: 'Regulation follows the HORMONE signal, not the raw glucose level. No insulin → F-2,6-BP stays low → glycolysis off, gluconeogenesis on. The liver dumps even MORE glucose into already-flooded blood.',
        },
      ],
      teach: 'This is why diabetic hyperglycemia is so vicious: the fuel gauge (insulin) is broken, so the liver keeps producing glucose in the middle of a glucose flood. Hormonal context beats substrate concentration.',
    },
  ],
  diseases: [
    {
      id: 'pk-def',
      name: 'Pyruvate kinase deficiency',
      emoji: '🩸',
      vignette:
        'A newborn has jaundice and a chronic hemolytic anemia. Red cells are being destroyed. Labs show elevated 2,3-BPG and NO mitochondrial compensation is possible in these cells.',
      suspects: ['Pyruvate kinase', 'Hexokinase', 'GAPDH', 'Aldolase'],
      answer: 0,
      accumulates: 'Upstream glycolytic intermediates (incl. 2,3-BPG)',
      missing: 'ATP (the RBC’s only energy source)',
      teach:
        'Pyruvate kinase runs the final ATP-making step. In a red cell — which depends ENTIRELY on glycolysis — losing PK means a chronic ATP shortfall. Without ATP the membrane pumps fail, the cell stiffens and is destroyed in the spleen → hemolytic anemia. Upstream intermediates back up, including 2,3-BPG (which conveniently right-shifts hemoglobin, easing O₂ delivery).',
      pearl: 'PK deficiency = the most common inherited glycolytic enzyme defect → chronic hemolytic anemia in the mitochondria-free RBC.',
    },
    {
      id: 'arsenic',
      name: 'Arsenate poisoning (a mechanism, not a gene)',
      emoji: '☠️',
      vignette:
        'A patient is exposed to arsenate (AsO₄³⁻). Glycolysis keeps consuming glucose and even keeps making NADH — but the ATP yield collapses.',
      suspects: ['GAPDH / phosphoglycerate kinase couple (step 6→7)', 'Pyruvate kinase (step 10)', 'Hexokinase (step 1)', 'Enolase (step 9)'],
      answer: 0,
      accumulates: 'A useless 1-arseno-3-phosphoglycerate that hydrolyzes spontaneously',
      missing: 'The step-7 ATP (substrate-level phosphorylation is uncoupled)',
      teach:
        'Arsenate mimics inorganic phosphate. GAPDH incorporates it in place of Pi, but the arseno-product hydrolyzes on its own before phosphoglycerate kinase can hand the phosphate to ADP. Oxidation still happens (NADH is still made) but the ATP of step 7 is lost — "arsenolysis" uncouples the payoff.',
      pearl: 'Classic mechanism question: arsenate uncouples substrate-level phosphorylation at GAPDH/PGK — oxidation continues, ATP does not.',
    },
  ],
  quiz: [
    {
      tag: 'energetics',
      stem: 'Per molecule of glucose completely converted to two pyruvate by glycolysis, what is the NET yield of ATP and NADH?',
      choices: ['Net +2 ATP and +2 NADH', 'Net +4 ATP and +2 NADH', 'Net +2 ATP and +4 NADH', 'Net +6 ATP and +2 NADH'],
      answer: 0,
      rationale:
        'Spend 2 ATP up front (hexokinase, PFK-1), make 4 gross in the payoff (PGK + PK, each ×2), and bank 2 NADH (GAPDH ×2). Net ATP = 4 − 2 = +2. The +4 gross and +2 NADH are correct in isolation — which is exactly why they’re distractors.',
    },
    {
      tag: 'regulation',
      stem: 'Which set lists the three irreversible, regulated steps of glycolysis, and which is the committed step?',
      choices: [
        'Hexokinase, PFK-1, pyruvate kinase; committed step = PFK-1',
        'Hexokinase, aldolase, pyruvate kinase; committed step = hexokinase',
        'Isomerase, PFK-1, enolase; committed step = enolase',
        'Hexokinase, PFK-1, GAPDH; committed step = GAPDH',
      ],
      answer: 0,
      rationale:
        'The three far-from-equilibrium (large −ΔG) steps are hexokinase, PFK-1, and pyruvate kinase. PFK-1 is the committed step: its product F-1,6-BP is dedicated to glycolysis, and PFK-1 is the primary regulatory enzyme.',
    },
    {
      tag: 'energetics',
      stem: 'At what point does each downstream reaction begin to occur twice per glucose (the "×2" counting)?',
      choices: [
        'After aldolase (step 4) splits F-1,6-BP into two 3-carbon molecules',
        'After hexokinase (step 1) phosphorylates glucose',
        'After GAPDH (step 6) produces NADH',
        'After pyruvate kinase (step 10) makes pyruvate',
      ],
      answer: 0,
      rationale:
        'Aldolase cleaves one 6-carbon sugar into two trioses; TPI funnels DHAP into a second G3P. From step 6 on, both halves run the payoff, so every product doubles. Miss the doubling and you’ll under-count the ledger.',
    },
    {
      tag: 'basics',
      stem: 'GAPDH catalyzes glycolysis’s only oxidation. What is the source of the phosphate it adds to the substrate?',
      choices: ['Inorganic phosphate (Pi), not ATP', 'A phosphate from ATP', 'A phosphate from GTP', 'A phosphate released from NADH'],
      answer: 0,
      rationale:
        'GAPDH couples aldehyde oxidation to attachment of inorganic phosphate (Pi), making the high-energy acyl-phosphate 1,3-BPG and reducing NAD⁺ → NADH. No ATP/GTP is spent — the energy comes from the oxidation, which is why the next step can then make ATP.',
    },
    {
      tag: 'integration',
      stem: 'A glucose unit released from glycogen enters as glucose-6-phosphate at step 2, bypassing hexokinase. Assuming full conversion to two pyruvate, what is the net ATP yield?',
      choices: ['+3 ATP', '+2 ATP', '+4 ATP', '+1 ATP'],
      answer: 0,
      rationale:
        'Bypassing hexokinase saves one of the two invested ATP (only PFK-1 still spends one). Payoff is unchanged at +4 gross. Net = 4 − 1 = +3 ATP. This is why glycogen-derived glucose is slightly more efficient than free glucose.',
    },
    {
      tag: 'disease',
      stem: 'A red blood cell relies exclusively on glycolysis and holds a small, fixed NAD⁺ pool. If lactate dehydrogenase is inhibited (with no electron transport chain available), why does glycolytic ATP production rapidly halt?',
      choices: [
        'NAD⁺ can’t be regenerated from NADH, so GAPDH (step 6) can’t proceed',
        'ATP accumulates and activates PFK-1, accelerating consumption',
        'Pyruvate can’t enter the citric acid cycle, stopping substrate-level phosphorylation',
        'Lactate directly phosphorylates ADP, depleting inorganic phosphate',
      ],
      answer: 0,
      rationale:
        'LDH is the RBC’s only route to reoxidize NADH → NAD⁺. Block it and the fixed NAD⁺ pool empties; GAPDH stalls; the payoff phase can’t run; ATP stops. The RBC has no mitochondrial alternative.',
    },
    {
      tag: 'regulation',
      stem: 'In the FED state, which change best explains why liver glycolysis speeds up?',
      choices: [
        'Insulin raises fructose-2,6-bisphosphate, which activates PFK-1',
        'Glucagon raises fructose-2,6-bisphosphate, which activates PFK-1',
        'Insulin lowers fructose-2,6-bisphosphate, which activates FBPase-1',
        'Epinephrine phosphorylates PFK-1 directly to activate it',
      ],
      answer: 0,
      rationale:
        'Insulin (fed) dephosphorylates the bifunctional PFK-2/FBPase-2 enzyme, switching it to PFK-2 mode → F-2,6-BP rises → PFK-1 (and thus glycolysis) is activated. Glucagon does the reciprocal opposite.',
    },
    {
      tag: 'basics',
      stem: 'Why is a reaction that sits NEAR equilibrium a poor place for the cell to regulate a pathway?',
      choices: [
        'Nudging it just lets it slide back — only a far-from-equilibrium (irreversible) step can be held shut',
        'Near-equilibrium reactions release too much heat to control',
        'Enzymes at equilibrium can’t bind allosteric effectors',
        'Near-equilibrium steps never produce ATP',
      ],
      answer: 0,
      rationale:
        'Control requires being able to STOP flow. A near-equilibrium reaction runs either direction and re-equilibrates instantly, so throttling it accomplishes nothing. The three glycolytic control points are precisely the three far-from-equilibrium, effectively irreversible steps.',
    },
  ],
  funFact:
    'Glycolysis is so ancient and universal it predates oxygen in Earth’s atmosphere — the same ten steps run in your neurons, in brewer’s yeast, and in bacteria that have never met O₂.',
};
