import type { Pathway } from '../types';

/* =============================================================================
   GLUCONEOGENESIS — hand-authored, cross-checked against
   src/content/lessons/integration-of-metabolism/lesson.mdx (fed/fasted logic,
   Cori cycle, reciprocal hormonal control) plus the glycolysis lesson/exemplar
   (this is glycolysis run backward) and core biochemistry for the four bypasses.

   Making glucose FROM pyruvate. Glycolysis is a one-way street at its three
   irreversible steps, so gluconeogenesis can't simply reverse them — it detours
   around them with FOUR bypass enzymes (pyruvate carboxylase, PEPCK,
   fructose-1,6-bisphosphatase, glucose-6-phosphatase). The seven reversible
   glycolytic steps in between just run backward, so we collapse them into a
   single "reverse glycolysis" tile and let the four bypasses carry the story.

   ENERGETICS: it takes TWO pyruvate to build ONE glucose, and the bill is 6
   high-energy phosphates per glucose — 4 ATP + 2 GTP — i.e. the expensive
   mirror image of glycolysis's net +2 ATP. `doubleAfter: 0`: rather than model
   the 2-pyruvate stoichiometry with the doubling engine (which was built for
   the glycolytic split), we author the mainline as a single molecule's journey
   and state the "×2 pyruvate per glucose" fact in netYield and the facts.
   ============================================================================ */

export const gluconeogenesis: Pathway = {
  id: 'gluconeogenesis',
  name: 'Gluconeogenesis',
  emoji: '🏗️',
  tagline: 'Glycolysis in reverse, at a steep markup. Spend 6 to un-make what earned you 2.',
  blurb:
    'The liver (and kidney) builds glucose from scratch — starting from pyruvate — to keep your brain fed between meals. It is glycolysis run backward, but four irreversible steps must be bypassed by four dedicated enzymes. Two pyruvate in, one glucose out, and it costs six high-energy phosphates.',
  difficulty: 3,
  location: 'Cytosol + mitochondria + ER (liver and kidney)',
  netYield: 'Costs 6 ATP (4 ATP + 2 GTP) per glucose — the reverse of glycolysis is expensive (2 pyruvate → 1 glucose)',
  start: 'Pyruvate',
  startShort: 'Pyruvate',
  startEmoji: '🍇',
  doubleAfter: 0, // authored per single molecule; 2 pyruvate/glucose noted in netYield & facts
  lessonSlug: 'integration-of-metabolism',
  steps: [
    {
      n: 1,
      product: 'Oxaloacetate',
      short: 'OAA',
      enzyme: 'Pyruvate carboxylase',
      tokens: { atp: -1, co2: -1 },
      irreversible: true,
      committed: true,
      emoji: '🧬',
      fact: 'BYPASS #1, in the mitochondrion. Spends 1 ATP and fixes a CO₂ onto pyruvate. Needs a BIOTIN cofactor (the classic carboxyl carrier) and is allosterically ACTIVATED by acetyl-CoA — the signal that fat is being burned and carbons can be spared for glucose.',
    },
    {
      n: 2,
      product: 'Phosphoenolpyruvate',
      short: 'PEP',
      enzyme: 'PEP carboxykinase (PEPCK)',
      tokens: { gtp: -1, co2: 1 },
      irreversible: true,
      emoji: '⚡',
      fact: 'BYPASS #2. Spends 1 GTP and releases the CO₂ that pyruvate carboxylase just added — a carboxylate-then-decarboxylate trick that pumps enough energy in to make high-energy PEP. (OAA must first leave the mitochondrion, usually shuttled out as malate.) PEPCK is induced by glucagon/cortisol.',
    },
    {
      n: 3,
      product: 'Fructose-1,6-bisphosphate',
      short: 'F1,6BP',
      enzyme: 'Reverse glycolysis (enolase → aldolase)',
      tokens: { atp: -1, nadh: -1 },
      emoji: '🔄',
      fact: 'The easy middle. The near-equilibrium glycolytic steps simply run backward — enolase, PGM, PGK (spends ATP here), GAPDH (spends NADH), TPI, aldolase — no special enzymes needed. This is why only FOUR bypasses matter: the rest of the road is already two-way.',
    },
    {
      n: 4,
      product: 'Fructose-6-phosphate',
      short: 'F6P',
      enzyme: 'Fructose-1,6-bisphosphatase (FBPase-1)',
      irreversible: true,
      emoji: '🚦',
      fact: 'BYPASS #3 — THE key regulated step, the reciprocal mirror of PFK-1. Just hydrolyzes off a phosphate (no ATP made). INHIBITED by AMP and by fructose-2,6-bisphosphate; when F-2,6-BP is low (fasting/glucagon), this enzyme is unleashed and gluconeogenesis flows.',
    },
    {
      n: 5,
      product: 'Glucose-6-phosphate',
      short: 'G6P',
      enzyme: 'Phosphoglucose isomerase',
      emoji: '🔁',
      fact: 'A freely reversible isomerization (ketose → aldose), the exact reverse of glycolysis step 2. Note: G6P is the branch point — it can go to glucose, back into glycolysis, into glycogen, or into the pentose phosphate pathway.',
    },
    {
      n: 6,
      product: 'Glucose',
      short: 'Glucose',
      enzyme: 'Glucose-6-phosphatase',
      irreversible: true,
      emoji: '🏁',
      fact: 'BYPASS #4 & the finish line, in the ER lumen. Hydrolyzes the phosphate off G6P so free glucose can finally leave the cell. Present ONLY in liver and kidney (and gut) — which is exactly why only those organs can export glucose to the blood. Muscle lacks it, so muscle keeps its glucose for itself.',
    },
  ],
  regulators: [
    { name: 'Pyruvate carboxylase', role: 'Bypass #1 & the committed gate. Allosterically REQUIRES acetyl-CoA — high acetyl-CoA (from fatty-acid oxidation in fasting) says "carbons to spare, make glucose."' },
    { name: 'Fructose-1,6-bisphosphatase (FBPase-1)', role: 'The master reciprocal switch, opposite PFK-1. INHIBITED by AMP and fructose-2,6-BP; ACTIVE when energy is low-but-not-that-low and F-2,6-BP is low (fasting).' },
    { name: 'PFK-2 / FBPase-2 (bifunctional)', role: 'Sets fructose-2,6-BP. Glucagon (fasting) → PKA → FBPase-2 mode → F-2,6-BP FALLS → FBPase-1 ON, PFK-1 OFF → gluconeogenesis wins. Insulin does the reverse.' },
    { name: 'PEPCK (transcriptional)', role: 'Bypass #2. Not allosteric — its AMOUNT is set by hormones: glucagon and cortisol INDUCE it (more enzyme = more gluconeogenic capacity); insulin represses it.' },
  ],
  scenarios: [
    {
      id: 'gng-fast',
      emoji: '😴',
      title: 'Overnight fast — the brain still needs glucose',
      scene: 'It has been ~16 hours since dinner. Liver glycogen is nearly spent, but the brain must have glucose. Glucagon is up, insulin is down, and the liver switches jobs: MAKE glucose from lactate, alanine, and glycerol.',
      hormones: 'Glucagon ↑ · insulin ↓',
      flux: 'up',
      decisions: [
        {
          q: 'Which way is the liver running right now?',
          choices: ['Gluconeogenesis UP — build and export glucose', 'Glycolysis UP — burn glucose for the liver’s own ATP'],
          answer: 0,
          why: 'The fasting liver’s job is to EXPORT glucose to the brain. Burning glucose via glycolysis would defeat the purpose. Gluconeogenesis on, glycolysis off — reciprocal control keeps them from running at once.',
        },
        {
          q: 'What happens to fructose-2,6-bisphosphate, and to FBPase-1?',
          choices: ['F-2,6-BP falls → FBPase-1 is de-inhibited (ON)', 'F-2,6-BP rises → FBPase-1 is activated'],
          answer: 0,
          why: 'Glucagon → PKA phosphorylates the bifunctional enzyme to its FBPase-2 mode → F-2,6-BP FALLS. Low F-2,6-BP releases FBPase-1 from inhibition (and shuts PFK-1 off). The same molecule flips both pathways at once.',
        },
        {
          q: 'Fatty acids are being oxidized in the liver, raising acetyl-CoA. What does that do to gluconeogenesis?',
          choices: ['Activates it — acetyl-CoA turns ON pyruvate carboxylase', 'Provides carbons — acetyl-CoA is converted to glucose'],
          answer: 0,
          why: 'Acetyl-CoA is the allosteric ACTIVATOR of pyruvate carboxylase (bypass #1), coupling fat-burning to glucose-making. But it CANNOT become glucose: the pyruvate dehydrogenase step is irreversible, so fat carbons never yield net glucose.',
        },
      ],
      teach: 'FASTING is gluconeogenesis’s home turf: glucagon high → F-2,6-BP low → FBPase-1 unleashed, and fatty-acid-derived acetyl-CoA both activates pyruvate carboxylase AND pays the ATP bill. The liver rebuilds glucose from lactate, alanine, and glycerol and ships it to the brain.',
    },
    {
      id: 'gng-fed',
      emoji: '🥞',
      title: 'You just ate a big meal',
      scene: 'Blood glucose is spiking, insulin is pouring out. There is glucose everywhere. The last thing the liver should do is spend six phosphates making MORE of it.',
      hormones: 'Insulin ↑ · glucagon ↓',
      flux: 'off',
      decisions: [
        {
          q: 'Should gluconeogenesis run in the fed state?',
          choices: ['No — shut it off; glucose is abundant', 'Yes — top up the blood glucose'],
          answer: 0,
          why: 'Making glucose when glucose is already flooding in would be a pointless, expensive futile cycle. Insulin switches the program to glycolysis and storage; gluconeogenesis goes quiet.',
        },
        {
          q: 'How does insulin turn FBPase-1 down?',
          choices: ['It raises F-2,6-BP, which inhibits FBPase-1 (and activates PFK-1)', 'It raises acetyl-CoA, which inhibits FBPase-1'],
          answer: 0,
          why: 'Insulin → dephosphorylation switches the bifunctional enzyme to PFK-2 mode → F-2,6-BP RISES → PFK-1 ON, FBPase-1 OFF. Glycolysis wins; gluconeogenesis is silenced. Acetyl-CoA acts on pyruvate carboxylase, not FBPase-1.',
        },
      ],
      teach: 'FED = insulin high → F-2,6-BP high → FBPase-1 OFF, PFK-1 ON. This is the exact reciprocal opposite of fasting. Because a single messenger (F-2,6-BP) sets both enzymes, the cell never runs both directions at once and wastes ATP in a futile cycle.',
    },
    {
      id: 'gng-cori',
      emoji: '🏃',
      title: 'After the sprint — the Cori cycle',
      scene: 'Your leg muscles just fermented a load of glucose to lactate to power an all-out sprint. That lactate pours into the blood and reaches the liver, which has a job: turn it back into glucose and return it.',
      hormones: 'Systemic — muscle exports lactate, liver reclaims it',
      flux: 'up',
      decisions: [
        {
          q: 'What does the liver do with the lactate arriving from muscle?',
          choices: ['Rebuilds it into glucose via gluconeogenesis (the Cori cycle)', 'Burns it to CO₂ in the liver’s own citric acid cycle'],
          answer: 0,
          why: 'This is the Cori cycle the Coris first mapped: muscle → lactate → blood → liver → glucose → blood → muscle. The liver reclaims the carbon skeleton so it isn’t lost, and returns usable glucose.',
        },
        {
          q: 'Before lactate can enter gluconeogenesis, what must happen to it?',
          choices: ['Lactate dehydrogenase oxidizes it back to pyruvate (making NADH)', 'It is carboxylated directly to oxaloacetate'],
          answer: 0,
          why: 'Lactate isn’t a mainline intermediate — LDH first converts lactate → pyruvate, which then enters at pyruvate carboxylase. The muscle ran LDH forward (to regenerate NAD⁺); the liver runs it in reverse.',
        },
        {
          q: 'Who pays the energetic price of the Cori cycle?',
          choices: ['The liver — it spends 6 ATP-equivalents to remake glucose the muscle burned', 'The muscle — it repays the ATP when the glucose returns'],
          answer: 0,
          why: 'Muscle got 2 net ATP from anaerobic glycolysis; the liver spends 6 to rebuild that glucose. The cycle runs at a net energy LOSS — but it shifts the metabolic burden from over-taxed muscle to the well-fed liver, and salvages the carbon.',
        },
      ],
      teach: 'The Cori cycle is gluconeogenesis as an inter-organ rescue: sprinting muscle offloads its lactate to the liver, which spends 6 high-energy phosphates to rebuild glucose and send it back. It costs energy overall, but it lets muscle keep sprinting and prevents the carbon from being wasted.',
    },
    {
      id: 'gng-starvation',
      emoji: '🍂',
      title: 'Prolonged starvation — days without food',
      scene: 'Glycogen is long gone. Gluconeogenesis has been the sole glucose source for days, and its raw material for the glucose-hungry brain is largely your own muscle protein, arriving as alanine.',
      hormones: 'Glucagon ↑↑ · insulin ↓↓ · cortisol ↑',
      flux: 'up',
      decisions: [
        {
          q: 'Which substrate for gluconeogenesis becomes a survival liability in deep starvation?',
          choices: ['Amino acids from muscle (e.g., alanine) — this consumes muscle protein', 'Glycerol from fat — this consumes essential fat'],
          answer: 0,
          why: 'Sustained gluconeogenesis for the brain’s ~120 g/day glucose demand pulls carbon from muscle protein (the glucose-alanine cycle also hands the liver nitrogen for urea). Burning your own muscle to make sugar can’t continue indefinitely.',
        },
        {
          q: 'What adaptation lets the body dial gluconeogenesis DOWN and spare that muscle?',
          choices: ['The brain shifts to burning ketone bodies, cutting glucose demand from ~120 to ~40 g/day', 'Gluconeogenesis learns to run from acetyl-CoA, using fat instead of protein'],
          answer: 0,
          why: 'Over days the brain adapts to oxidize liver-made ketone bodies, slashing its glucose requirement (~120 → ~40 g/day). Less glucose needed → less gluconeogenesis → less muscle broken down. Acetyl-CoA still cannot make net glucose.',
        },
      ],
      teach: 'In starvation gluconeogenesis is a double-edged sword: it keeps the brain alive but eats muscle protein to do it. The life-saving move is ketone adaptation — the brain switches much of its fuel to ketone bodies, cutting glucose demand and therefore the gluconeogenic drain on muscle. That protein-sparing effect is what lets a person survive weeks.',
    },
    {
      id: 'gng-diabetes',
      emoji: '🍭',
      title: 'Uncontrolled Type 1 diabetes',
      scene: 'Blood glucose is sky-high, yet there is almost no insulin. The liver cannot "hear" that fuel is abundant — it reads the low insulin as fasting and keeps its glucose factory running full tilt.',
      hormones: 'Insulin ↓↓ · glucagon ↑ (unopposed)',
      flux: 'up',
      decisions: [
        {
          q: 'What does the liver do with gluconeogenesis despite the high blood glucose?',
          choices: ['Keeps it running HARD — it "reads" starvation from the low insulin', 'Shuts it off — glucose is obviously abundant'],
          answer: 0,
          why: 'Regulation follows the HORMONE, not the raw glucose level. No insulin → F-2,6-BP stays low → FBPase-1 stays active → the liver dumps still MORE glucose into already-flooded blood. The fuel gauge is broken.',
        },
        {
          q: 'Why does this make hyperglycemia so vicious?',
          choices: ['The liver keeps MAKING glucose in the middle of a glucose flood', 'Glucose is being locked into glycogen and can’t escape'],
          answer: 0,
          why: 'Hormonal context beats substrate concentration. With the insulin signal gone, unopposed glucagon keeps gluconeogenesis and glycogenolysis running, so the liver actively worsens the hyperglycemia rather than damping it.',
        },
      ],
      teach: 'Diabetic hyperglycemia is a signaling failure, not a fuel shortage. Without insulin the liver runs the fasting program — gluconeogenesis full-on — despite abundant glucose, pouring more glucose into the blood. The same broken signal drives unrestrained lipolysis and ketogenesis (diabetic ketoacidosis): the body starving in the middle of plenty.',
    },
  ],
  diseases: [
    {
      id: 'fbpase-def',
      name: 'Fructose-1,6-bisphosphatase deficiency',
      emoji: '🚦',
      vignette:
        'An infant becomes lethargic and tachypneic after a night without feeding or during a mild illness. Labs: hypoglycemia, a HIGH anion gap with lactic acidosis, and elevated ketones. Feeding glucose fixes everything. Between fasts, the child is fine.',
      suspects: ['Fructose-1,6-bisphosphatase (FBPase-1)', 'Pyruvate carboxylase', 'Glucose-6-phosphatase', 'Glucose-6-phosphate dehydrogenase'],
      answer: 0,
      accumulates: 'Fructose-1,6-bisphosphate and upstream three-carbon substrates → lactate (lactic acidosis)',
      missing: 'The ability to make glucose from lactate, alanine, or glycerol (gluconeogenesis is blocked; glycogen still works)',
      teach:
        'FBPase-1 is bypass #3, the key gluconeogenic step. Block it and the liver cannot convert three-carbon precursors (lactate, alanine, glycerol) into glucose. As long as liver glycogen lasts, blood sugar holds — but once an overnight fast or an illness depletes glycogen, there is no gluconeogenic backup: fasting HYPOGLYCEMIA. Meanwhile the gluconeogenic substrates back up and spill into LACTATE, producing a lactic acidosis. Classic triggers: fasting and febrile illness.',
      pearl: 'FBPase-1 deficiency = fasting hypoglycemia + lactic acidosis, but NORMAL response to a glucose meal — because glycogenolysis is intact and only the make-from-scratch route is broken.',
    },
    {
      id: 'g6pase-vg',
      name: 'Von Gierke disease · Glycogen storage disease type Ia',
      emoji: '🫃',
      vignette:
        'A toddler has a huge liver, a doll-like round face, and severe fasting hypoglycemia after even short fasts. Labs: lactic acidosis, HYPERuricemia, and HYPERlipidemia. The liver is stuffed with both glycogen and fat.',
      suspects: ['Glucose-6-phosphatase', 'Fructose-1,6-bisphosphatase', 'Pyruvate carboxylase', 'Muscle glycogen phosphorylase (McArdle)'],
      answer: 0,
      accumulates: 'Glucose-6-phosphate (→ glycogen, lactate, and diverted into fat and the pentose pathway → urate)',
      missing: 'Free glucose export from the liver (both gluconeogenesis AND glycogenolysis dead-end at G6P)',
      teach:
        'Glucose-6-phosphatase is bypass #4 — the FINAL common step of both gluconeogenesis and glycogenolysis. Lose it and G6P can never become free glucose, so the liver cannot export glucose by EITHER route → severe fasting hypoglycemia. The trapped G6P is shunted every other direction: into glycogen (hepatomegaly), into lactate (lactic acidosis), into the pentose phosphate pathway and purine turnover (hyperuricemia → gout), and into fat (hyperlipidemia).',
      pearl: 'Von Gierke (GSD Ia) = the "everything is high" storage disease: hypoglycemia WITH high lactate, high urate, and high lipids — because the block is at the shared exit, G6P → glucose.',
    },
    {
      id: 'pc-def',
      name: 'Pyruvate carboxylase deficiency',
      emoji: '🧬',
      vignette:
        'A neonate has severe lactic acidosis, hypoglycemia, developmental delay, and neurological signs. Blood alanine and lactate are high. The block is at the very first committed step of gluconeogenesis, in the mitochondrion.',
      suspects: ['Pyruvate carboxylase', 'Fructose-1,6-bisphosphatase', 'Glucose-6-phosphatase', 'PEP carboxykinase (PEPCK)'],
      answer: 0,
      accumulates: 'Pyruvate → lactate and alanine (severe lactic acidosis, high alanine)',
      missing: 'Oxaloacetate — so gluconeogenesis can’t start AND the TCA cycle is starved of its acceptor',
      teach:
        'Pyruvate carboxylase (bypass #1) makes oxaloacetate — the entry into gluconeogenesis AND an anaplerotic top-up for the citric acid cycle. Without it, pyruvate cannot enter gluconeogenesis (fasting hypoglycemia) and instead piles up, spilling into lactate and alanine (lactic acidosis). Low OAA also cripples the TCA cycle and hurts the brain, which is why the neurological picture is severe. It needs biotin, so a severe biotin problem can phenocopy it.',
      pearl: 'Pyruvate carboxylase deficiency = hypoglycemia + lactic acidosis + neuro damage; remember it needs BIOTIN and that its product OAA does double duty (gluconeogenesis + TCA anaplerosis).',
    },
  ],
  quiz: [
    {
      tag: 'energetics',
      stem: 'Starting from two molecules of pyruvate, how many high-energy phosphate bonds (ATP + GTP) does the liver spend to synthesize one molecule of glucose?',
      choices: [
        '6 (4 ATP + 2 GTP)',
        '2 (2 ATP)',
        '4 (2 ATP + 2 GTP)',
        '8 (6 ATP + 2 GTP)',
      ],
      answer: 0,
      rationale:
        'Per glucose (two pyruvate): pyruvate carboxylase spends 2 ATP, PEPCK spends 2 GTP, and phosphoglycerate kinase in the reverse-glycolysis leg spends 2 ATP → 4 ATP + 2 GTP = 6 high-energy phosphates. Compare glycolysis, which nets only +2 ATP — making glucose costs far more than breaking it, which is why the two run reciprocally.',
    },
    {
      tag: 'basics',
      stem: 'Glycolysis is largely reversible, yet gluconeogenesis needs four dedicated bypass enzymes. Why can’t the cell simply run glycolysis backward?',
      choices: [
        'Three glycolytic steps are far-from-equilibrium (irreversible), so those three must be bypassed by separate reactions',
        'Every glycolytic enzyme runs in only one direction',
        'The cofactors NAD⁺ and ATP cannot be regenerated in reverse',
        'Glycolysis occurs in the cytosol but gluconeogenesis is entirely mitochondrial',
      ],
      answer: 0,
      rationale:
        'Seven of glycolysis’s ten steps are near-equilibrium and reverse freely. Only the three with a large negative ΔG — hexokinase, PFK-1, and pyruvate kinase — are effectively one-way, and those are exactly the three that gluconeogenesis must route around (pyruvate kinase takes TWO enzymes, pyruvate carboxylase + PEPCK, hence four bypasses total).',
    },
    {
      tag: 'basics',
      stem: 'Pyruvate carboxylase converts pyruvate to oxaloacetate. Which cofactor is essential for this carboxylation, and what allosterically activates the enzyme?',
      choices: [
        'Biotin is the cofactor; acetyl-CoA is the allosteric activator',
        'Thiamine pyrophosphate is the cofactor; ATP is the activator',
        'Lipoic acid is the cofactor; NADH is the activator',
        'Biotin is the cofactor; fructose-2,6-bisphosphate is the activator',
      ],
      answer: 0,
      rationale:
        'Pyruvate carboxylase is a biotin-dependent carboxylase (biotin is the mobile CO₂ carrier). Its obligatory allosteric activator is acetyl-CoA: when fatty-acid oxidation raises acetyl-CoA, it signals that carbons and reducing power are available, so pyruvate should be steered toward glucose (and toward TCA anaplerosis) rather than oxidized.',
    },
    {
      tag: 'regulation',
      stem: 'Fructose-2,6-bisphosphate is the switch that keeps glycolysis and gluconeogenesis from running simultaneously. In the FASTING liver, what are its level and its effect on fructose-1,6-bisphosphatase?',
      choices: [
        'F-2,6-BP is LOW, which relieves inhibition of FBPase-1 (gluconeogenesis ON)',
        'F-2,6-BP is HIGH, which activates FBPase-1 (gluconeogenesis ON)',
        'F-2,6-BP is LOW, which activates PFK-1 (glycolysis ON)',
        'F-2,6-BP is HIGH, which inhibits FBPase-1 (gluconeogenesis OFF)',
      ],
      answer: 0,
      rationale:
        'Fasting → glucagon → PKA phosphorylates the bifunctional PFK-2/FBPase-2 enzyme into FBPase-2 mode → F-2,6-BP FALLS. Low F-2,6-BP simultaneously relieves inhibition of FBPase-1 (gluconeogenesis on) and removes activation of PFK-1 (glycolysis off). One metabolite reciprocally sets both directions.',
    },
    {
      tag: 'regulation',
      stem: 'Only the liver and kidney can release free glucose into the blood, while skeletal muscle cannot — even though muscle stores plenty of glycogen. Which enzyme’s tissue distribution explains this?',
      choices: [
        'Glucose-6-phosphatase, present in liver and kidney but absent in muscle',
        'Hexokinase, present only in muscle',
        'Glycogen phosphorylase, present only in liver',
        'Pyruvate carboxylase, absent in muscle',
      ],
      answer: 0,
      rationale:
        'The final gluconeogenic/glycogenolytic step, G6P → free glucose, requires glucose-6-phosphatase (in the ER of liver, kidney, and gut). Muscle lacks it, so muscle glucose-6-phosphate is trapped and can only be used locally — muscle glycogen serves the muscle, never the bloodstream.',
    },
    {
      tag: 'integration',
      stem: 'Despite generating large amounts of acetyl-CoA, fatty acids cannot provide the carbon for NET glucose synthesis in humans. What is the fundamental reason?',
      choices: [
        'The pyruvate dehydrogenase reaction (pyruvate → acetyl-CoA) is irreversible, so acetyl-CoA cannot be turned back into pyruvate/OAA for net glucose',
        'Acetyl-CoA cannot cross the mitochondrial membrane',
        'Fatty acids are oxidized in peroxisomes, not mitochondria',
        'Acetyl-CoA is consumed entirely by ketogenesis during fasting',
      ],
      answer: 0,
      rationale:
        'Pyruvate → acetyl-CoA (via PDH) is irreversible, so there is no route from acetyl-CoA back to pyruvate. Acetyl-CoA’s two carbons enter the TCA cycle but two carbons are lost as CO₂ before oxaloacetate reforms, so no NET carbon reaches gluconeogenesis. (Glycerol and glucogenic amino acids, by contrast, ARE gluconeogenic — but the fatty-acyl portion of fat is not.)',
    },
    {
      tag: 'integration',
      stem: 'A sprinter’s muscle ferments glucose to lactate; the liver converts that lactate back to glucose. Counting both organs, what is the net ATP balance of one turn of this cycle?',
      choices: [
        'A net LOSS — muscle nets 2 ATP but the liver spends 6 to rebuild the glucose',
        'A net gain of 2 ATP shared between the organs',
        'Exactly break-even (0 ATP)',
        'A net gain of 4 ATP in the liver',
      ],
      answer: 0,
      rationale:
        'This is the Cori cycle. Anaerobic glycolysis in muscle yields +2 ATP; gluconeogenesis in the liver costs 6 ATP-equivalents to rebuild the same glucose. Net, the cycle loses 4 ATP-equivalents — but it shifts the energetic burden to the liver, lets muscle keep contracting anaerobically, and salvages the lactate carbon instead of wasting it.',
    },
    {
      tag: 'disease',
      stem: 'A 9-month-old presents after an overnight fast with hypoglycemia and a lactic acidosis; a glucose drink promptly resolves the episode, and between fasts the child is well with no hepatomegaly. Deficiency of which enzyme best fits?',
      choices: [
        'Fructose-1,6-bisphosphatase',
        'Glucose-6-phosphatase',
        'Pyruvate kinase',
        'Muscle phosphofructokinase',
      ],
      answer: 0,
      rationale:
        'FBPase-1 deficiency blocks gluconeogenesis but leaves glycogenolysis intact, so patients are fine when fed and while glycogen lasts, then develop fasting hypoglycemia with lactic acidosis (three-carbon substrates back up to lactate). The lack of hepatomegaly and the clean response to glucose distinguish it from glucose-6-phosphatase deficiency (Von Gierke), where G6P is trapped and the liver enlarges.',
    },
    {
      tag: 'energetics',
      stem: 'In the pyruvate → PEP bypass, why does the cell first carboxylate pyruvate to oxaloacetate (spending ATP) only to immediately decarboxylate it back at PEPCK (spending GTP)?',
      choices: [
        'The carboxylation/decarboxylation cycle injects enough free energy to drive formation of high-energy PEP, which pyruvate kinase’s reverse reaction cannot supply',
        'Oxaloacetate is needed to carry the phosphate group to PEP',
        'CO₂ is required as a leaving group to reduce NAD⁺',
        'It regenerates biotin for the next round',
      ],
      answer: 0,
      rationale:
        'Reversing pyruvate kinase directly is energetically prohibitive. The two-step detour spends two high-energy phosphates (ATP at pyruvate carboxylase, GTP at PEPCK) and uses transient carboxylation as an energetic lever: adding CO₂ then removing it, coupled to GTP hydrolysis, pumps in enough energy to make phosphoenolpyruvate. The added CO₂ is released at PEPCK, not retained.',
    },
    {
      tag: 'disease',
      stem: 'A neonate has severe hypoglycemia, profound lactic acidosis with high alanine, and neurological injury. Enzyme assay points to a mitochondrial, biotin-dependent enzyme that also feeds the citric acid cycle. Which deficiency is this?',
      choices: [
        'Pyruvate carboxylase',
        'Glucose-6-phosphatase',
        'PEP carboxykinase',
        'Lactate dehydrogenase',
      ],
      answer: 0,
      rationale:
        'Pyruvate carboxylase is the mitochondrial, biotin-dependent first bypass, and its product oxaloacetate is also the TCA cycle’s anaplerotic top-up. Deficiency blocks gluconeogenesis (hypoglycemia) and backs pyruvate up into lactate and alanine (lactic acidosis); low OAA also cripples the TCA cycle, which — together with impaired energy supply — accounts for the severe neurological picture.',
    },
  ],
  funFact:
    'Gluconeogenesis and glycolysis share a road but never drive it both ways at once: a single metabolite, fructose-2,6-bisphosphate, holds one direction open and the other shut. It costs your liver about six ATP to rebuild each glucose that glycolysis tore apart for two — the steepest markup in metabolism, paid nightly so your brain never runs out of sugar while you sleep.',
};
