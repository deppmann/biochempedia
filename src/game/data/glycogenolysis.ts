import type { Pathway } from '../types';

/* =============================================================================
   GLYCOGEN METABOLISM — mainline is glycogenolysis (glycogen BREAKDOWN),
   cross-checked against src/content/lessons/integration-of-metabolism/lesson.mdx
   (the fed→fasted relay, the glucagon→cAMP→PKA reciprocal cascade, the Cori
   cycle) plus the Cori-cycle content in the glycolysis lesson and core biochem.

   The star here is REGULATION, not energetics: phosphorolysis frees glucose-1-P
   WITHOUT spending ATP, and a hormone cascade flips synthesis and breakdown in
   opposite directions in a single stroke. doubleAfter: 0 — one residue at a
   time, nothing splits, so no yield ever doubles.
   ============================================================================ */

export const glycogenolysis: Pathway = {
  id: 'glycogenolysis',
  name: 'Glycogen Metabolism',
  emoji: '🧵',
  tagline: 'The body’s pantry: spool glucose onto a ball when fed, unspool it between meals.',
  blurb:
    'Glycogen is branched glucose storage — the liver’s to steady blood sugar, the muscle’s to fuel itself. Breakdown clips glucose off the ends by phosphorolysis (no ATP spent), and a glucagon/epinephrine → cAMP → PKA cascade flips synthesis off and breakdown on in one reciprocal stroke.',
  difficulty: 2,
  location: 'Cytosol (liver & muscle)',
  netYield: 'Phosphorolysis frees glucose-1-phosphate without spending ATP',
  start: 'Glycogen (n residues)',
  startShort: 'Glycogenₙ',
  startEmoji: '🧶',
  doubleAfter: 0, // linear: one residue is released at a time — nothing ever doubles
  lessonSlug: 'integration-of-metabolism',
  steps: [
    {
      n: 1,
      product: 'Glucose-1-phosphate + Glycogen (n−1)',
      short: 'G1P',
      enzyme: 'Glycogen phosphorylase',
      irreversible: true,
      committed: true,
      emoji: '✂️',
      fact: 'THE regulated step. Uses inorganic phosphate (Pi), not water, to snap off terminal α-1,4 glucoses one at a time — "phosphorolysis." Because the product leaves already phosphorylated as G1P, the cell skips the hexokinase ATP later. Needs pyridoxal phosphate (vitamin B₆) as cofactor; stops 4 residues shy of each α-1,6 branch (the "limit dextrin").',
    },
    {
      n: 2,
      product: 'Debranched linear chain',
      short: 'Debranched',
      enzyme: 'Debranching enzyme (4-α-glucanotransferase + α-1,6-glucosidase)',
      emoji: '🌿',
      fact: 'One bifunctional enzyme, two jobs: it TRANSFERS a block of three glucoses off a stub to a nearby chain end (re-exposing α-1,4 links for phosphorylase), then HYDROLYZES the single α-1,6 branch glucose — releasing it as FREE glucose, not G1P. So most glycogen exits as G1P but the branch points exit as free glucose.',
    },
    {
      n: 3,
      product: 'Glucose-6-phosphate',
      short: 'G6P',
      enzyme: 'Phosphoglucomutase',
      emoji: '📍',
      fact: 'Shuttles the phosphate from C1 to C6, converting G1P → G6P. This is the crossroads: G6P can enter glycolysis (muscle) OR be dephosphorylated for export (liver). Freely reversible — it also runs forward for glycogen synthesis.',
    },
    {
      n: 4,
      product: 'Free glucose → blood (LIVER)',
      short: 'Glucose (liver)',
      enzyme: 'Glucose-6-phosphatase',
      irreversible: true,
      emoji: '🩸',
      fact: 'LIVER-ONLY exit. This ER enzyme strips the phosphate so glucose can cross the membrane into blood for the brain and RBCs. Muscle LACKS it — which is exactly why muscle glycogen is selfish and can never raise blood sugar.',
    },
    {
      n: 5,
      product: 'G6P → glycolysis (MUSCLE)',
      short: 'G6P → ATP',
      enzyme: '(no phosphatase — G6P stays trapped)',
      emoji: '💪',
      fact: 'MUSCLE fate. With no glucose-6-phosphatase, the charged G6P can’t leave the cell, so muscle burns it in-house via glycolysis. Entering as G6P skips hexokinase → net +3 ATP per glucose unit instead of +2. Muscle glycogen fuels muscle, full stop.',
    },
  ],
  regulators: [
    {
      name: 'Glycogen phosphorylase',
      role: 'The mobilizer. Switched ON by phosphorylase kinase (b→a). Muscle isoform is also allosterically activated by AMP (low energy) and Ca²⁺; liver isoform is allosterically INHIBITED by free glucose (the "we’re fine, stop breaking down" brake).',
    },
    {
      name: 'Phosphorylase kinase',
      role: 'The relay. Phosphorylated & activated by PKA; ALSO switched on directly by Ca²⁺/calmodulin — so a muscle action potential (Ca²⁺ spike) turns on breakdown even before hormones arrive.',
    },
    {
      name: 'PKA (cAMP-dependent protein kinase)',
      role: 'The master switch. cAMP (from glucagon in liver, epinephrine in muscle) activates PKA, which turns phosphorylase kinase ON and glycogen synthase OFF in the same stroke — reciprocal control.',
    },
    {
      name: 'Glycogen synthase',
      role: 'The opposite pump. Phosphorylation (by PKA & GSK-3) turns it OFF during breakdown; insulin promotes its dephosphorylation (via PP1) to turn storage back ON. Reciprocal to phosphorylase.',
    },
    {
      name: 'Insulin / PP1',
      role: 'The reset. Insulin (fed) activates protein phosphatase-1, which strips the phosphates off — inactivating phosphorylase and ACTIVATING synthase. Flips the whole system from breakdown to storage.',
    },
  ],
  scenarios: [
    {
      id: 'glyn-fed',
      emoji: '🍚',
      title: 'You just ate a big bowl of rice',
      scene: 'Blood glucose is climbing and insulin is pouring out. The liver and muscle should be STOCKING the pantry, not raiding it.',
      hormones: 'Insulin ↑ · glucagon ↓',
      flux: 'down',
      decisions: [
        {
          q: 'Should glycogen breakdown run right now?',
          choices: ['No — shut breakdown OFF and build glycogen instead', 'Yes — mobilize glycogen for energy'],
          answer: 0,
          why: 'Fed = store. Insulin’s job is to bank the incoming glucose as glycogen. Breaking it down now would be a pointless futile cycle against the food you just ate.',
        },
        {
          q: 'What does insulin do to the phosphorylation switches?',
          choices: [
            'Activates PP1, which DEphosphorylates them → synthase ON, phosphorylase OFF',
            'Activates PKA, which phosphorylates them → phosphorylase ON',
          ],
          answer: 0,
          why: 'Insulin works largely by promoting dephosphorylation via protein phosphatase-1. That single move inactivates phosphorylase AND activates glycogen synthase — reciprocal control, storage direction.',
        },
        {
          q: 'What allosterically brakes LIVER phosphorylase when glucose is abundant?',
          choices: ['Free glucose binding phosphorylase a (an allosteric inhibitor)', 'AMP binding and activating it'],
          answer: 0,
          why: 'In the liver, glucose itself binds phosphorylase and inhibits it — a direct "blood sugar is fine, quit mobilizing" signal that also exposes the enzyme to be switched off by PP1.',
        },
      ],
      teach:
        'FED = insulin high → PP1 active → phosphorylase OFF, synthase ON. The liver and muscle both stock glycogen. This is the reciprocal opposite of the fasting program — one signal, both directions flipped, so you never break down and build at the same time.',
    },
    {
      id: 'glyn-fast',
      emoji: '🌙',
      title: 'Overnight fast — 12 hours since dinner',
      scene: 'Blood glucose is drifting down and the brain still needs it. The pancreas swaps insulin for glucagon, and the LIVER’s job is to feed the blood.',
      hormones: 'Glucagon ↑ · insulin ↓',
      flux: 'up',
      decisions: [
        {
          q: 'In the early-fasting (~4–16 h) window, what mainly keeps blood glucose up?',
          choices: [
            'Hepatic glycogenolysis — the liver breaking down its glycogen',
            'Gluconeogenesis alone — glycogen is irrelevant',
          ],
          answer: 0,
          why: 'In the postabsorptive state the liver defends blood glucose chiefly by glycogenolysis; gluconeogenesis ramps up over the same window (a gradient, not a switch), and liver glycogen is largely gone by ~1 day.',
        },
        {
          q: 'How does glucagon turn on liver breakdown?',
          choices: [
            'cAMP → PKA → phosphorylase kinase ON → phosphorylase ON (and synthase OFF)',
            'It binds phosphorylase directly and reshapes it',
          ],
          answer: 0,
          why: 'Glucagon raises hepatic cAMP → activates PKA → PKA phosphorylates phosphorylase kinase (on) and glycogen synthase (off). One cascade, reciprocal result.',
        },
        {
          q: 'Why can only the LIVER raise blood glucose from its glycogen?',
          choices: [
            'Liver has glucose-6-phosphatase to free glucose; muscle does not',
            'Muscle glycogen is chemically different from liver glycogen',
          ],
          answer: 0,
          why: 'Glucose-6-phosphatase removes the C6 phosphate so glucose can leave the cell. Only liver (and kidney/gut) express it — muscle traps its G6P and burns it locally.',
        },
      ],
      teach:
        'FASTING = glucagon high → cAMP/PKA cascade → liver phosphorylase ON, synthase OFF. Liver glycogen is the FIRST responder to falling blood sugar, buying hours until gluconeogenesis and (much later) ketones take over. Only the liver, with glucose-6-phosphatase, can export the glucose.',
    },
    {
      id: 'glyn-sprint',
      emoji: '🏃',
      title: 'Sprinting for the finish line',
      scene: 'Your quadriceps need ATP RIGHT NOW. A calcium spike just fired the contraction, and ATP is being spent faster than blood can deliver fuel.',
      hormones: 'Epinephrine ↑ · local Ca²⁺ spike · AMP ↑',
      flux: 'up',
      decisions: [
        {
          q: 'What does muscle do with the glucose it liberates from glycogen?',
          choices: [
            'Keeps it — burns G6P in its own glycolysis (no phosphatase to export)',
            'Exports it to the blood to help the whole body',
          ],
          answer: 0,
          why: 'Muscle lacks glucose-6-phosphatase, so its G6P is trapped and fed straight into glycolysis for local ATP. Muscle glycogen is selfish by design.',
        },
        {
          q: 'Beyond epinephrine, what turns on muscle breakdown almost instantly?',
          choices: [
            'The Ca²⁺ that triggers contraction also activates phosphorylase kinase',
            'Glucagon released from the muscle',
          ],
          answer: 0,
          why: 'Phosphorylase kinase has a calmodulin subunit, so the same Ca²⁺ that fires the contraction directly switches on glycogen breakdown — fuel and contraction are coupled. (Muscle barely responds to glucagon; epinephrine is its hormone.)',
        },
        {
          q: 'Which allosteric signal reports "low energy — mobilize!" in muscle?',
          choices: ['AMP (rising as ATP is spent) activates muscle phosphorylase b', 'Glucose (rising) activates it'],
          answer: 0,
          why: 'AMP climbs when ATP is consumed and allosterically activates the muscle phosphorylase b even without full phosphorylation — a fast local override. Glucose inhibition is a liver feature, not muscle.',
        },
      ],
      teach:
        'SPRINT = muscle mobilizes its OWN glycogen. Three signals converge: epinephrine (cAMP/PKA), the contraction’s Ca²⁺ (phosphorylase kinase), and AMP (allosteric). G6P is trapped and burned locally; the lactate produced ships to the liver to be rebuilt into glucose — the Cori cycle.',
    },
    {
      id: 'glyn-stress',
      emoji: '⚡',
      title: 'A car swerves at you — fight-or-flight',
      scene: 'Adrenal glands dump epinephrine into the blood. Every tissue must free fuel FAST, before you’ve even decided to run.',
      hormones: 'Epinephrine ↑↑ (systemic)',
      flux: 'up',
      decisions: [
        {
          q: 'What second messenger does epinephrine (via its β-receptor) raise?',
          choices: ['cAMP → activates PKA', 'cGMP → activates PKG'],
          answer: 0,
          why: 'β-adrenergic receptors are Gs-coupled: they activate adenylyl cyclase → cAMP → PKA, the very same cascade glucagon uses in the liver. Same switch, different hormone and tissue.',
        },
        {
          q: 'Why does one PKA activation amplify into massive glucose release?',
          choices: [
            'It’s an enzyme cascade — each active enzyme activates many of the next',
            'PKA physically shreds the glycogen granule',
          ],
          answer: 0,
          why: 'PKA activates many phosphorylase kinases, each activates many phosphorylases, each clips many glucoses. A tiny hormone signal is amplified thousands-fold — the whole point of a kinase cascade.',
        },
      ],
      teach:
        'STRESS = epinephrine everywhere → cAMP/PKA → breakdown ON in BOTH liver (→ blood glucose) and muscle (→ local ATP). Epinephrine is the "emergency" version of glucagon’s liver cascade, but it acts body-wide and fast, using the same cAMP/PKA machinery.',
    },
  ],
  diseases: [
    {
      id: 'von-gierke',
      name: 'Von Gierke disease · Type I',
      emoji: '🍬',
      vignette:
        'A doll-faced infant with a hugely enlarged liver and a protruding belly. Between feeds she becomes profoundly hypoglycemic, sweaty, and seizure-prone. Labs: fasting hypoglycemia, lactic acidosis, high triglycerides, and hyperuricemia (gout-range).',
      suspects: ['Glucose-6-phosphatase', 'Glycogen phosphorylase (liver)', 'Debranching enzyme', 'Acid α-glucosidase'],
      answer: 0,
      accumulates: 'Glycogen and glucose-6-phosphate in the liver (→ hepatomegaly)',
      missing: 'Free glucose exportable to the blood',
      teach:
        'Glucose-6-phosphatase is the LAST step of both glycogenolysis and gluconeogenesis in the liver. Lose it and the liver can make G6P but can’t free glucose to the blood → severe fasting hypoglycemia despite full glycogen stores. The trapped G6P floods into glycolysis (→ lactic acidosis) and the pentose-phosphate / de novo pathways (→ hypertriglyceridemia and hyperuricemia). Glycogen piles up → the classic huge liver.',
      pearl: 'Von Gierke = the ONLY glycogen storage disease that also blocks gluconeogenesis, because glucose-6-phosphatase is shared. Full glycogen, empty blood sugar.',
    },
    {
      id: 'pompe',
      name: 'Pompe disease · Type II',
      emoji: '💔',
      vignette:
        'A floppy 4-month-old with poor head control, feeding trouble, and a MASSIVELY enlarged heart on chest film. Blood glucose is NORMAL. The problem is muscle, not sugar.',
      suspects: ['Acid α-glucosidase (lysosomal)', 'Glucose-6-phosphatase', 'Muscle glycogen phosphorylase', 'Debranching enzyme'],
      answer: 0,
      accumulates: 'Glycogen inside LYSOSOMES of heart and skeletal muscle',
      missing: 'Lysosomal glycogen turnover (cytosolic breakdown is untouched)',
      teach:
        'Acid α-glucosidase (acid maltase) is the LYSOSOMAL enzyme that degrades the small amount of glycogen that ends up in lysosomes — a pathway completely separate from the cytosolic phosphorylase route. Its loss doesn’t cause hypoglycemia (cytosolic breakdown still works, blood sugar is fine); instead glycogen swells the lysosomes and wrecks cardiac and skeletal muscle → cardiomegaly, hypotonia, early heart failure.',
      pearl: 'Pompe "Pumps the heart out" — lysosomal defect, cardiomegaly, NORMAL blood glucose. The only glycogen storage disease that is a lysosomal storage disease.',
    },
    {
      id: 'cori',
      name: 'Cori disease · Type III',
      emoji: '🌿',
      vignette:
        'A toddler with hepatomegaly and mild fasting hypoglycemia — milder than Von Gierke. Notably NO lactic acidosis and NO hyperuricemia. A muscle biopsy shows glycogen with short, stubby outer branches.',
      suspects: ['Debranching enzyme', 'Glucose-6-phosphatase', 'Acid α-glucosidase', 'Phosphorylase kinase'],
      answer: 0,
      accumulates: 'Limit-dextrin glycogen — abnormal, short-branched (branch points can’t be removed)',
      missing: 'Access to the glucose locked inside the branch points (only the outer chains are recoverable)',
      teach:
        'Debranching enzyme clears the α-1,6 branch points. Without it, phosphorylase chews each outer chain down to 4 residues from a branch and then STALLS — leaving a dense "limit dextrin." Only the outer glucoses are recoverable, so fasting hypoglycemia is milder than Von Gierke, and because gluconeogenesis is intact there’s no lactic acidosis. The tell is the abnormal short-branched glycogen structure.',
      pearl: 'Cori (Type III) = milder Von Gierke with NORMAL lactate and abnormal, short-outer-branch glycogen. Gluconeogenesis still rescues blood sugar.',
    },
    {
      id: 'mcardle',
      name: 'McArdle disease · Type V',
      emoji: '💪',
      vignette:
        'A young adult gets painful muscle cramps and fatigue within minutes of hard exercise, sometimes with dark (cola-colored) urine after. Push through it and things paradoxically improve after ~10 minutes. Blood glucose is completely normal.',
      suspects: ['Muscle glycogen phosphorylase (myophosphorylase)', 'Liver glycogen phosphorylase', 'Glucose-6-phosphatase', 'Acid α-glucosidase'],
      answer: 0,
      accumulates: 'Glycogen in skeletal muscle (can’t be mobilized during exercise)',
      missing: 'Rapid glycogen-derived ATP for exercising muscle',
      teach:
        'The MUSCLE isoform of glycogen phosphorylase is the deficit — the liver isoform is a different gene and is fine, so blood glucose is normal. Muscle can’t tap its glycogen, so during burst exercise it can’t make fast anaerobic ATP → cramps, weakness, and rhabdomyolysis (the cola-colored urine is myoglobin). The "second wind" is real: after ~10 min, blood-borne glucose and free fatty acids arrive and rescue the muscle.',
      pearl: 'McArdle = exercise intolerance + "second wind" + myoglobinuria with NORMAL blood glucose. MUSCLE phosphorylase only — liver is spared.',
    },
  ],
  quiz: [
    {
      tag: 'basics',
      stem: 'Glycogen phosphorylase releases glucose units from glycogen. What does it use to cleave the α-1,4 bond, and in what form does the glucose leave?',
      choices: [
        'Inorganic phosphate (Pi); leaves as glucose-1-phosphate',
        'Water; leaves as free glucose',
        'ATP; leaves as glucose-6-phosphate',
        'UTP; leaves as UDP-glucose',
      ],
      answer: 0,
      rationale:
        'This is phosphorolysis, not hydrolysis: phosphorylase uses Pi to snap the terminal α-1,4 bond, so the glucose exits already phosphorylated as glucose-1-phosphate. That’s the point — the cell gets a phosphorylated sugar without spending an ATP the way hexokinase would.',
    },
    {
      tag: 'energetics',
      stem: 'A glucose unit released from muscle glycogen enters glycolysis as glucose-6-phosphate, bypassing hexokinase. What is the net ATP yield to complete pyruvate compared to starting from free glucose?',
      choices: [
        '+3 ATP (vs +2 from free glucose)',
        '+2 ATP (identical to free glucose)',
        '+4 ATP (no ATP is ever invested)',
        '+1 ATP (phosphorolysis costs an ATP)',
      ],
      answer: 0,
      rationale:
        'Because phosphorolysis delivers glucose-1-P → G6P for free, only PFK-1 still spends an ATP in the investment phase (hexokinase is skipped). Payoff is unchanged at +4 gross, so net = 4 − 1 = +3 ATP. That’s one ATP better than starting from blood glucose.',
    },
    {
      tag: 'basics',
      stem: 'Phosphorylase can only shorten a branch to within 4 residues of an α-1,6 branch point. What does debranching enzyme do with the branch glucose itself, and in what form is it released?',
      choices: [
        'Hydrolyzes the α-1,6 bond, releasing that glucose as FREE glucose',
        'Phosphorolyzes it, releasing glucose-1-phosphate',
        'Transfers it into a lysosome for storage',
        'Oxidizes it directly to CO₂',
      ],
      answer: 0,
      rationale:
        'Debranching enzyme is bifunctional: its transferase moves a 3-residue block to expose more α-1,4 links, then its α-1,6-glucosidase HYDROLYZES the single branch-point glucose, releasing it as free (unphosphorylated) glucose. So ~90% of glycogen exits as G1P and ~10% (the branch points) exits as free glucose.',
    },
    {
      tag: 'integration',
      stem: 'Why can the liver, but not skeletal muscle, use its glycogen to raise blood glucose?',
      choices: [
        'Only the liver has glucose-6-phosphatase to remove the phosphate so glucose can leave the cell',
        'Only the liver stores glycogen; muscle stores none',
        'Muscle glycogen is a different polymer that can’t be broken down',
        'Muscle lacks glycogen phosphorylase entirely',
      ],
      answer: 0,
      rationale:
        'Both tissues break glycogen down to G6P, but a charged phosphosugar can’t cross the plasma membrane. The liver (and kidney/gut) express glucose-6-phosphatase to free glucose for export; muscle does not, so its G6P is trapped and burned locally. Muscle glycogen fuels muscle only.',
    },
    {
      tag: 'regulation',
      stem: 'Glucagon binds the liver and, within minutes, breakdown speeds up while synthesis stops. What is the correct signaling order?',
      choices: [
        'Glucagon → cAMP → PKA → phosphorylase kinase → phosphorylase ON; synthase phosphorylated OFF',
        'Glucagon → cGMP → PKG → phosphorylase ON; synthase ON',
        'Glucagon → PP1 → dephosphorylates phosphorylase ON; synthase OFF',
        'Glucagon → AMPK → phosphorylase kinase OFF; synthase ON',
      ],
      answer: 0,
      rationale:
        'Glucagon raises cAMP, which activates PKA. PKA phosphorylates phosphorylase kinase (activating it → phosphorylase a) AND glycogen synthase (inactivating it). One kinase cascade drives breakdown up and synthesis down simultaneously — reciprocal control.',
    },
    {
      tag: 'regulation',
      stem: 'A muscle fiber fires an action potential and contracts. Which signal switches on glycogen breakdown FASTER than any circulating hormone could?',
      choices: [
        'The Ca²⁺ released for contraction directly activates phosphorylase kinase via its calmodulin subunit',
        'Insulin secreted by the muscle',
        'Glucagon binding the muscle β-receptor',
        'A drop in cytosolic Pi',
      ],
      answer: 0,
      rationale:
        'Phosphorylase kinase contains calmodulin, so the very Ca²⁺ that triggers contraction also switches on glycogen breakdown — coupling fuel supply to demand instantly, without waiting for a hormone. AMP provides a second fast allosteric "low energy" push in muscle.',
    },
    {
      tag: 'regulation',
      stem: 'In the LIVER, which allosteric signal is a physiological INHIBITOR of glycogen phosphorylase, and what does that accomplish?',
      choices: [
        'Free glucose — it signals blood sugar is adequate, so stop mobilizing',
        'AMP — it accelerates breakdown when energy is high',
        'Ca²⁺ — it inhibits phosphorylase to protect glycogen',
        'Citrate — it activates phosphorylase to burn glycogen',
      ],
      answer: 0,
      rationale:
        'The liver isoform is uniquely inhibited by free glucose binding phosphorylase a — a direct "blood sugar is fine, quit breaking down" brake that also primes the enzyme for dephosphorylation by PP1. (AMP activation and Ca²⁺ sensitivity are features of the MUSCLE isoform, tuned to energy charge and contraction, not blood glucose.)',
    },
    {
      tag: 'disease',
      stem: 'A young adult has muscle cramps and fatigue minutes into vigorous exercise, occasional myoglobinuria, but a normal blood glucose and a "second wind" if they slow down. Which enzyme is deficient?',
      choices: [
        'Muscle glycogen phosphorylase (McArdle, Type V)',
        'Glucose-6-phosphatase (Von Gierke, Type I)',
        'Acid α-glucosidase (Pompe, Type II)',
        'Liver glycogen phosphorylase',
      ],
      answer: 0,
      rationale:
        'Exercise intolerance with rhabdomyolysis and a NORMAL blood glucose localizes the defect to muscle-specific glycogen phosphorylase (McArdle). The liver isoform is a separate gene and intact, so systemic glucose is fine. The "second wind" reflects blood glucose and fatty acids arriving to rescue the muscle after ~10 minutes.',
    },
    {
      tag: 'disease',
      stem: 'An infant has severe fasting hypoglycemia, hepatomegaly, lactic acidosis, hypertriglyceridemia, and hyperuricemia. Why does one enzyme defect produce ALL of these together?',
      choices: [
        'Loss of glucose-6-phosphatase traps G6P: no glucose export (hypoglycemia + big liver), and the backed-up G6P floods glycolysis (lactate) and biosynthetic pathways (triglycerides, urate)',
        'Loss of debranching enzyme leaves short-branched glycogen with normal lactate',
        'A lysosomal defect swells the heart while blood glucose stays normal',
        'Muscle phosphorylase loss blocks exercise but spares the liver',
      ],
      answer: 0,
      rationale:
        'Von Gierke (Type I) blocks the shared last step of glycogenolysis AND gluconeogenesis. G6P can’t become blood glucose (→ hypoglycemia, hepatomegaly) and instead pours into glycolysis (→ lactic acidosis) and the pentose-phosphate / lipogenic and purine pathways (→ hypertriglyceridemia, hyperuricemia). One block, a whole syndrome.',
    },
    {
      tag: 'integration',
      stem: 'After a meal, insulin flips the liver from glycogen breakdown back to storage. Mechanistically, how does one signal reverse BOTH directions at once?',
      choices: [
        'Insulin activates protein phosphatase-1, which dephosphorylates the enzymes — inactivating phosphorylase and activating glycogen synthase',
        'Insulin raises cAMP, activating PKA to phosphorylate both enzymes',
        'Insulin degrades phosphorylase and synthesizes new synthase over hours',
        'Insulin binds phosphorylase directly and reshapes its active site',
      ],
      answer: 0,
      rationale:
        'Glucagon’s cascade worked by phosphorylation; insulin works largely by promoting DEphosphorylation through PP1. Removing those phosphates simultaneously switches phosphorylase off and glycogen synthase on — the same reciprocal pair, driven the opposite way, so storage and breakdown never run together.',
    },
  ],
  funFact:
    'Your liver holds only ~100 g of glycogen — about a day’s worth of blood glucose — yet it’s enough to carry you from dinner to breakfast without your brain ever noticing. Muscle stores more (~400 g) but hoards every gram for itself, because it threw away the one enzyme (glucose-6-phosphatase) that could have shared.',
};
