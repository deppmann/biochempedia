import type { Pathway } from '../types';

/* =============================================================================
   KETONE BODIES — ketogenesis in the LIVER, ketolysis in the PERIPHERY
   (hand-authored, cross-checked against the ketone-body section of
   src/content/lessons/fatty-acid-degradation/lesson.mdx). Two acetyl-CoA (from
   β-oxidation) are welded into acetoacetate, exported as its transport form
   β-hydroxybutyrate, and burned back to acetyl-CoA in the brain/muscle. The
   twist the whole thing turns on: the liver MAKES ketones but can't BURN them
   (no SCOT/thiophorase). `doubleAfter: 0` — one acetoacetate is one acetoacetate;
   the "×2" is only the two acetyl-CoA released at the very end of ketolysis, which
   is captured in the ledger of the final step, not by doubling downstream yields.
   ============================================================================ */

export const ketoneBodies: Pathway = {
  id: 'ketone-bodies',
  name: 'Ketone Bodies',
  emoji: '⛽',
  tagline: 'The liver cooks a fuel it can’t eat, so your brain can. Peak altruism.',
  blurb:
    'When glucose runs low, the fasting liver welds surplus acetyl-CoA into acetoacetate and β-hydroxybutyrate — a water-soluble backup fuel the brain, heart, and muscle can burn. The liver makes it but can’t use it (no SCOT), so it exports every drop. Same chemistry that keeps a 40-day faster thinking is what turns lethal in uncontrolled diabetes.',
  difficulty: 2,
  location: 'Liver mitochondria (made) · peripheral mitochondria (used)',
  netYield:
    'Each acetoacetate → 2 acetyl-CoA in the periphery; the liver makes ketones but can’t burn them (no SCOT)',
  start: 'Acetyl-CoA ×2 (from β-oxidation)',
  startShort: 'Acetyl-CoA ×2',
  startEmoji: '🔥',
  doubleAfter: 0, // one acetoacetate stays one; the ×2 acetyl-CoA is booked in step 7's ledger
  lessonSlug: 'fatty-acid-degradation',
  steps: [
    {
      n: 1,
      product: 'Acetoacetyl-CoA',
      short: 'AcAc-CoA',
      enzyme: 'Thiolase (acetyl-CoA acetyltransferase)',
      emoji: '🤝',
      fact: 'KETOGENESIS begins (liver mitochondrion). Two acetyl-CoA are condensed head-to-tail into a 4-carbon acetoacetyl-CoA, releasing one CoA. This is β-oxidation’s thiolase run in reverse — same enzyme family, opposite direction.',
    },
    {
      n: 2,
      product: 'HMG-CoA (3-hydroxy-3-methylglutaryl-CoA)',
      short: 'HMG-CoA',
      enzyme: 'HMG-CoA synthase (mitochondrial, HMGCS2)',
      irreversible: true,
      committed: true,
      emoji: '🚦',
      fact: 'THE committed, rate-limiting step. A third acetyl-CoA is added to build 6-carbon HMG-CoA. This is the MITOCHONDRIAL HMGCS2 — do NOT confuse it with cytosolic HMG-CoA REDUCTASE, the statin target that makes cholesterol. Same intermediate, two compartments, two fates. Classic trap.',
    },
    {
      n: 3,
      product: 'Acetoacetate',
      short: 'AcAc',
      enzyme: 'HMG-CoA lyase',
      emoji: '✂️',
      fact: 'HMG-CoA is cleaved back to acetoacetate plus one acetyl-CoA. Acetoacetate is the primary, "parent" ketone body — a genuine carboxylic acid (a keto-ACID), which is why a flood of it drops blood pH.',
    },
    {
      n: 4,
      product: 'β-Hydroxybutyrate',
      short: 'β-HB',
      enzyme: 'β-hydroxybutyrate dehydrogenase (BDH)',
      tokens: { nadh: -1 },
      emoji: '🚚',
      fact: 'The transport form. Acetoacetate + NADH ⇌ β-hydroxybutyrate + NAD⁺. The β-HB : acetoacetate ratio mirrors the mitochondrial NADH/NAD⁺ ratio — the more reduced the matrix (deep fasting, DKA), the more the pool sits as β-HB. Not a true "ketone" chemically, but the dominant circulating ketone body.',
    },
    {
      n: 5,
      product: 'Acetone (minor, non-enzymatic)',
      short: 'Acetone',
      enzyme: '[spontaneous decarboxylation — no enzyme]',
      tokens: { co2: 1 },
      emoji: '🫁',
      fact: 'A side exit, not a step you regulate. Acetoacetate spontaneously loses CO₂ to become volatile acetone, exhaled as the sweet, fruity "acetone breath" of ketosis — famously mistaken for alcohol on the breath of a patient in DKA.',
    },
    {
      n: 6,
      product: 'Acetoacetyl-CoA (in the periphery)',
      short: 'AcAc-CoA',
      enzyme: 'SCOT (succinyl-CoA:3-ketoacid CoA transferase)',
      irreversible: true,
      emoji: '🔁',
      fact: 'KETOLYSIS, in brain/muscle/heart. β-HB is oxidized back to acetoacetate, then SCOT borrows a CoA from succinyl-CoA to reactivate it. The LIVER LACKS SCOT — so it physically cannot burn its own ketones. That single missing enzyme is why the liver is an obligate exporter: the altruist organ.',
    },
    {
      n: 7,
      product: 'Acetyl-CoA ×2 → TCA cycle',
      short: 'Acetyl-CoA ×2',
      enzyme: 'Thiolase (β-ketothiolase)',
      emoji: '🏁',
      fact: 'The payoff. Thiolase splits acetoacetyl-CoA into TWO acetyl-CoA, which drop straight into the TCA cycle for full oxidation. One acetoacetate → 2 acetyl-CoA of usable fuel in any tissue with mitochondria (so: not red blood cells).',
    },
  ],
  regulators: [
    {
      name: 'HMG-CoA synthase (HMGCS2)',
      role: 'The committed, rate-limiting valve of ketogenesis. ↑ by fasting/starvation (low insulin, high glucagon) and by an acetyl-CoA glut; succinylation/insulin turns it down. Mitochondrial — distinct from the cytosolic reductase of cholesterol synthesis.',
    },
    {
      name: 'Fatty-acid supply (upstream of everything)',
      role: 'Ketone output tracks β-oxidation flux. Fasting → lipolysis → free fatty acids flood the liver → acetyl-CoA piles up → ketogenesis. Low insulin also opens CPT-I (low malonyl-CoA), so fat pours into the mitochondrion in the first place.',
    },
    {
      name: 'Oxaloacetate (OAA) availability',
      role: 'The pivot. In fasting, OAA is pulled into gluconeogenesis, so acetyl-CoA can’t enter the TCA cycle and is diverted into ketones instead. "Fat burns in a carbohydrate flame" — no OAA, no clean acetyl-CoA disposal.',
    },
    {
      name: 'SCOT (thiophorase)',
      role: 'The peripheral gate on ketone USE, present in brain/muscle/heart but ABSENT in liver. Its tissue distribution is the regulation: it decides who gets to burn ketones and enforces that the liver only makes them.',
    },
  ],
  scenarios: [
    {
      id: 'ket-fed',
      emoji: '🍽️',
      title: 'Right after a big carb-heavy meal',
      scene:
        'Insulin is high, glucose is everywhere, and the liver is busy storing fuel. There is no reason to be making a starvation fuel right now.',
      hormones: 'Insulin ↑ · glucagon ↓',
      flux: 'off',
      decisions: [
        {
          q: 'What is ketogenesis doing in the fed state?',
          choices: [
            'Essentially OFF — no need for a backup fuel',
            'Running hard — always make ketones when glucose is high',
          ],
          answer: 0,
          why: 'Fed = insulin high → lipolysis suppressed, malonyl-CoA high (CPT-I shut), OAA plentiful. Acetyl-CoA is scarce AND has a clean TCA exit, so there’s nothing to divert into ketones.',
        },
        {
          q: 'Why doesn’t acetyl-CoA get shunted into ketones here?',
          choices: [
            'Plenty of oxaloacetate means acetyl-CoA burns cleanly in the TCA cycle',
            'Insulin directly activates HMG-CoA synthase',
          ],
          answer: 0,
          why: 'In the fed state OAA is abundant (not siphoned into gluconeogenesis), so acetyl-CoA condenses with it into citrate and runs the TCA cycle normally. Insulin turns HMGCS2 DOWN, not up.',
        },
      ],
      teach:
        'FED = the backup fuel stays in the drawer. High insulin blocks lipolysis and CPT-I, and abundant OAA lets acetyl-CoA burn cleanly, so there is no glut to repackage. Ketogenesis is a fasting program, not a fed one.',
    },
    {
      id: 'ket-overnight',
      emoji: '🌙',
      title: 'Overnight fast — 12–16 hours since dinner',
      scene:
        'Blood glucose is drifting down. Glycogen is running low. Glucagon rises, insulin falls, and the liver starts pulling free fatty acids out of the blood and burning them.',
      hormones: 'Glucagon ↑ · insulin ↓',
      flux: 'up',
      decisions: [
        {
          q: 'What triggers ketone production overnight?',
          choices: [
            'Rising fatty-acid oxidation floods the liver with acetyl-CoA',
            'Rising blood glucose forces the liver to dump excess as ketones',
          ],
          answer: 0,
          why: 'Low insulin/high glucagon → adipose lipolysis → free fatty acids to the liver → β-oxidation → acetyl-CoA piles up faster than the TCA cycle can take it. Glucose is FALLING here, not rising.',
        },
        {
          q: 'Why can’t that acetyl-CoA just run the TCA cycle instead?',
          choices: [
            'Oxaloacetate is being pulled into gluconeogenesis, so acetyl-CoA has nowhere to go',
            'The TCA cycle is switched off entirely during any fast',
          ],
          answer: 0,
          why: 'Fasting diverts OAA into making glucose. With OAA scarce, acetyl-CoA can’t condense into citrate efficiently, so it’s repackaged into ketones. "Fat burns in a carbohydrate flame."',
        },
      ],
      teach:
        'OVERNIGHT FAST = ketogenesis switches on. Low insulin unlocks lipolysis and CPT-I; OAA drains into gluconeogenesis; the resulting acetyl-CoA glut is welded into acetoacetate and β-HB and exported. This is the normal, healthy fasting response — mild ketosis, not ketoacidosis.',
    },
    {
      id: 'ket-starvation',
      emoji: '🏜️',
      title: 'Prolonged starvation — day 3 and beyond',
      scene:
        'Days without food. Muscle protein is being broken down for gluconeogenesis, and that can’t continue forever. Around day 3, the brain starts a critical adaptation.',
      hormones: 'Glucagon ↑↑ · insulin ↓↓',
      flux: 'up',
      decisions: [
        {
          q: 'What does the brain do after ~3 days of starvation?',
          choices: [
            'Shifts much of its fuel use to ketone bodies, sparing glucose and muscle protein',
            'Starts oxidizing fatty acids directly to spare glucose',
          ],
          answer: 0,
          why: 'The brain can’t oxidize long-chain fatty acids (they don’t cross the blood-brain barrier well and neurons don’t run β-oxidation for fuel), but it CAN import and burn β-HB. Shifting to ketones cuts its glucose demand, so less muscle protein is sacrificed for gluconeogenesis (Cahill’s protein-sparing adaptation).',
        },
        {
          q: 'Which cell STILL can’t use ketones, even now?',
          choices: [
            'Red blood cells — no mitochondria, so no ketolysis',
            'Cardiac muscle — it prefers glucose exclusively',
          ],
          answer: 0,
          why: 'Ketolysis (SCOT + thiolase → TCA) is entirely mitochondrial. RBCs have no mitochondria, so they remain obligately glucose-dependent no matter how deep the fast. The heart, by contrast, happily burns ketones.',
        },
      ],
      teach:
        'STARVATION = the brain’s fuel switch. By day ~40, proteolysis falls from ~75 g/day to ~20 g/day as the brain runs largely on β-hydroxybutyrate — the adaptation that let Angus Barbieri fast 382 days. RBCs stay glucose-only throughout (no mitochondria), which sets the floor on how low gluconeogenesis can go.',
    },
    {
      id: 'ket-keto-diet',
      emoji: '🥑',
      title: 'On a strict ketogenic diet',
      scene:
        'Very low carbohydrate, high fat, adequate protein — no fasting, but carbs are kept so low the body behaves as if it were.',
      hormones: 'Insulin chronically low · glucagon relatively ↑',
      flux: 'up',
      decisions: [
        {
          q: 'Why does a low-carb diet produce ketosis without actual starvation?',
          choices: [
            'Low carbs keep insulin low, so the liver runs the same lipolysis → β-oxidation → ketogenesis program',
            'Dietary fat is converted directly to ketones in the gut',
          ],
          answer: 0,
          why: 'Ketogenesis is driven by the insulin/glucagon RATIO and OAA availability, not by an empty stomach per se. Chronically low carbohydrate keeps insulin low, so the fasting fuel program runs even while eating.',
        },
      ],
      teach:
        'KETO DIET = fasting metabolism by other means. Keep carbohydrate low enough and insulin stays low, so fat is mobilized and the liver exports ketones continuously. This is the mechanism behind the 1921 ketogenic diet still used for drug-resistant epilepsy — a controlled, nutritional ketosis, distinct from the uncontrolled acidosis of DKA.',
    },
    {
      id: 'ket-dka',
      emoji: '🚑',
      title: 'Uncontrolled Type 1 diabetes → DKA',
      scene:
        'Almost no insulin. Blood glucose is sky-high, but the cells can’t use it and the liver reads the low insulin as deep starvation — so it makes ketones with the brakes cut.',
      hormones: 'Insulin ↓↓↓ · glucagon ↑ (unopposed)',
      flux: 'up',
      decisions: [
        {
          q: 'Why does DKA produce a dangerous acidosis, not just mild ketosis?',
          choices: [
            'With no insulin to restrain it, ketogenesis runs unchecked and acetoacetate + β-HB accumulate as acids faster than they’re buffered',
            'Ketone bodies are basic and raise blood pH to dangerous levels',
          ],
          answer: 0,
          why: 'Acetoacetate and β-hydroxybutyrate are carboxylic ACIDS. In normal fasting, insulin still puts a ceiling on their production. In T1DM with essentially no insulin, production runs away, overwhelms buffering, and drops blood pH — a true metabolic acidosis.',
        },
        {
          q: 'A nitroprusside urine dipstick reads only weakly positive despite severe DKA. Why can it under-read?',
          choices: [
            'The dipstick detects acetoacetate/acetone but NOT β-hydroxybutyrate, which dominates in DKA',
            'Ketones are fully reabsorbed by the kidney in DKA, so none reach the urine',
          ],
          answer: 0,
          why: 'The classic nitroprusside reaction detects acetoacetate (and acetone), not β-HB. In DKA the highly reduced matrix pushes the pool toward β-HB, so the dipstick can badly UNDER-estimate the true ketone load — and it can paradoxically look "worse" during treatment as β-HB converts back to acetoacetate.',
        },
      ],
      teach:
        'DKA = ketogenesis with the governor removed. No insulin means no ceiling on lipolysis or HMGCS2, so acid ketones flood the blood and drop the pH. Key clinical trap: β-hydroxybutyrate dominates but the nitroprusside dipstick misses it — measure β-HB directly. The same molecules that save a faster’s brain become a lethal acid load here.',
    },
  ],
  diseases: [
    {
      id: 'scot-def',
      name: 'SCOT deficiency (succinyl-CoA:3-ketoacid CoA transferase)',
      emoji: '🔁',
      vignette:
        'An infant has recurrent episodes of severe ketoacidosis, often triggered by fasting or illness, WITH persistently high ketone levels even when well-fed. The liver makes ketones normally; the problem is elsewhere.',
      suspects: [
        'SCOT (the peripheral ketone-activating transferase)',
        'HMG-CoA synthase (mitochondrial, HMGCS2)',
        'HMG-CoA lyase',
        'β-hydroxybutyrate dehydrogenase (BDH)',
      ],
      answer: 0,
      accumulates: 'Acetoacetate and β-hydroxybutyrate (ketones the periphery can’t burn)',
      missing: 'Acetyl-CoA from ketolysis in brain/muscle/heart',
      teach:
        'SCOT is the first committed step of ketone UTILIZATION. Ketogenesis (in the liver) is fine, so ketones are made and exported normally — but the peripheral tissues can’t reactivate them to acetyl-CoA, so ketones pile up and can’t be cleared. The result is permanent ketosis with crippling ketoacidotic crises during any catabolic stress. It’s the mirror image of a ketogenesis defect: too many ketones no one can burn.',
      pearl: 'SCOT deficiency = the periphery can’t USE ketones → persistent/permanent ketosis + fasting ketoacidotic crises (contrast HMGCS2/lyase defects, which fail to MAKE them → hypoketotic hypoglycemia).',
    },
    {
      id: 'dka',
      name: 'Diabetic ketoacidosis · DKA (Type 1 diabetes)',
      emoji: '🩸',
      vignette:
        'A young patient with Type 1 diabetes is nauseated, breathing deeply and rapidly (Kussmaul), with fruity breath. Glucose is 480 mg/dL, arterial pH 7.1, and a high anion gap. The urine dipstick is only mildly positive for ketones.',
      suspects: [
        'Insulin (absolute deficiency → unrestrained ketogenesis)',
        'SCOT (the peripheral ketone transferase)',
        'HMG-CoA lyase',
        'Pyruvate dehydrogenase',
      ],
      answer: 0,
      accumulates: 'Acetoacetate and β-hydroxybutyrate (acids) + glucose',
      missing: 'Insulin’s brake on lipolysis and ketogenesis',
      teach:
        'DKA is not a broken enzyme but a broken SIGNAL: absolute insulin deficiency removes the ceiling on lipolysis and hepatic ketogenesis. Acetoacetate and β-HB are acids, so unchecked production overwhelms buffering → high-anion-gap metabolic acidosis (Kussmaul breathing blows off CO₂ to compensate). The dipstick trap: nitroprusside detects acetoacetate/acetone, not the dominant β-hydroxybutyrate, so it under-reads the true severity.',
      pearl: 'DKA = no insulin → runaway acid ketones → high-anion-gap acidosis; β-HB dominates and the nitroprusside dipstick misses it, so measure β-HB directly.',
    },
    {
      id: 'aka',
      name: 'Alcoholic ketoacidosis (AKA)',
      emoji: '🍷',
      vignette:
        'A malnourished patient with heavy alcohol use, several days of vomiting and poor intake, presents with an anion-gap acidosis and ketones. Blood glucose is LOW or normal — not high — and there’s no diabetes.',
      suspects: [
        'NADH excess from ethanol metabolism (drives the ketone pool toward β-HB and starves gluconeogenesis)',
        'HMG-CoA synthase mutation',
        'Absolute insulin deficiency',
        'SCOT deficiency',
      ],
      answer: 0,
      accumulates: 'β-hydroxybutyrate (heavily favored) and acetoacetate',
      missing: 'Carbohydrate substrate + a normal NADH/NAD⁺ ratio',
      teach:
        'Alcohol metabolism (alcohol → acetaldehyde → acetate by two dehydrogenases) generates a huge NADH load. High NADH/NAD⁺ (1) suppresses gluconeogenesis and (2) shoves the ketone pool strongly toward β-hydroxybutyrate. Combined with starvation (low insulin, depleted glycogen from poor intake), the fasting liver makes ketones — but the glucose is normal or LOW, distinguishing it from DKA. Because β-HB so dominates, the nitroprusside dipstick can again badly under-read.',
      pearl: 'AKA = starvation ketosis + ethanol-driven NADH excess → β-HB-heavy anion-gap acidosis with NORMAL/LOW glucose (vs the hyperglycemia of DKA).',
    },
  ],
  quiz: [
    {
      tag: 'basics',
      stem: 'Ketogenesis and cholesterol synthesis both pass through HMG-CoA. What distinguishes the ketogenic route so the two pathways don’t interfere?',
      choices: [
        'Ketogenic HMG-CoA is made and cleaved by mitochondrial HMG-CoA synthase and lyase; cholesterol synthesis uses cytosolic HMG-CoA reductase',
        'Ketogenesis uses HMG-CoA reductase; cholesterol synthesis uses HMG-CoA synthase',
        'The two use chemically different HMG-CoA isomers',
        'Cholesterol synthesis occurs in the mitochondrion, ketogenesis in the cytosol',
      ],
      answer: 0,
      rationale:
        'Compartmentation keeps them separate. Ketogenesis runs in the mitochondrial matrix (HMGCS2 synthase makes HMG-CoA; HMG-CoA lyase cleaves it to acetoacetate). Cholesterol synthesis runs in the cytosol, where HMG-CoA REDUCTASE (the statin target) reduces HMG-CoA to mevalonate. Same intermediate, different enzymes, different compartments — a classic exam trap.',
    },
    {
      tag: 'basics',
      stem: 'Which enzyme catalyzes the committed, rate-limiting step of ketone body synthesis?',
      choices: [
        'Mitochondrial HMG-CoA synthase (HMGCS2)',
        'Thiolase',
        'HMG-CoA lyase',
        'β-hydroxybutyrate dehydrogenase',
      ],
      answer: 0,
      rationale:
        'Mitochondrial HMG-CoA synthase adds the third acetyl-CoA to make HMG-CoA and is the committed, rate-limiting valve — the point where fasting/glucagon signaling ramps ketogenesis. Thiolase and BDH catalyze reversible flanking steps, and HMG-CoA lyase simply cleaves the product of the committed step.',
    },
    {
      tag: 'integration',
      stem: 'Why does the liver, which produces ketone bodies, remain unable to use them as fuel itself?',
      choices: [
        'It lacks SCOT (succinyl-CoA:3-ketoacid CoA transferase), the enzyme that reactivates acetoacetate for oxidation',
        'It lacks mitochondria in the relevant hepatocytes',
        'It lacks HMG-CoA lyase',
        'Its ketones are immediately exported before they can be oxidized',
      ],
      answer: 0,
      rationale:
        'Ketolysis requires SCOT to transfer CoA from succinyl-CoA onto acetoacetate, forming acetoacetyl-CoA. The liver simply does not express SCOT, so it cannot re-activate the ketones it makes — it is an obligate exporter. It has plenty of mitochondria and a full ketogenic enzyme set; the single missing transferase is the whole story.',
    },
    {
      tag: 'energetics',
      stem: 'In a peripheral tissue with mitochondria, how much acetyl-CoA does one molecule of acetoacetate ultimately yield for the TCA cycle?',
      choices: [
        'Two acetyl-CoA',
        'One acetyl-CoA',
        'Three acetyl-CoA',
        'None — acetoacetate enters the TCA cycle directly',
      ],
      answer: 0,
      rationale:
        'Ketolysis reactivates acetoacetate to acetoacetyl-CoA (via SCOT), and thiolase then splits that 4-carbon unit into TWO acetyl-CoA, each of which enters the TCA cycle. Acetoacetate does not enter the cycle directly; it must be reactivated and cleaved first.',
    },
    {
      tag: 'regulation',
      stem: 'A fasting person’s liver has abundant acetyl-CoA from β-oxidation, yet most of it is diverted into ketones rather than run through the TCA cycle. What best explains the diversion?',
      choices: [
        'Oxaloacetate is being consumed by gluconeogenesis, limiting acetyl-CoA’s entry into the TCA cycle',
        'The TCA cycle enzymes are inhibited by glucagon during fasting',
        'Acetyl-CoA cannot cross into the mitochondrial matrix during fasting',
        'Ketogenesis has a lower activation energy than the citrate synthase reaction',
      ],
      answer: 0,
      rationale:
        'During fasting, oxaloacetate is siphoned into gluconeogenesis, so there isn’t enough OAA for citrate synthase to condense with the large acetyl-CoA pool. The backlog is repackaged into ketone bodies — the meaning of "fat burns in a carbohydrate flame." Acetyl-CoA is generated in the matrix already, and the diversion is about substrate availability, not enzyme inhibition or activation energy.',
    },
    {
      tag: 'basics',
      stem: 'Which ketone body is the predominant form in the circulation, and what determines its ratio to acetoacetate?',
      choices: [
        'β-hydroxybutyrate; its ratio to acetoacetate reflects the mitochondrial NADH/NAD⁺ ratio',
        'Acetone; its ratio reflects the rate of exhalation',
        'Acetoacetate; its ratio reflects blood pH',
        'β-hydroxybutyrate; its ratio is fixed at 1:1 with acetoacetate',
      ],
      answer: 0,
      rationale:
        'β-hydroxybutyrate dominates in blood. Because BDH runs acetoacetate + NADH ⇌ β-HB + NAD⁺, the β-HB:acetoacetate ratio tracks the mitochondrial NADH/NAD⁺ ratio: the more reduced the matrix (deep fasting, DKA, ethanol load), the more the pool sits as β-HB. It is not fixed at 1:1.',
    },
    {
      tag: 'disease',
      stem: 'A patient in diabetic ketoacidosis has a strongly positive clinical picture but a urine nitroprusside dipstick that reads only mildly positive for ketones. What is the best explanation?',
      choices: [
        'The dipstick detects acetoacetate and acetone but not β-hydroxybutyrate, which predominates in DKA',
        'The kidney fully reabsorbs ketone bodies in DKA, so little reaches the urine',
        'Acetone is exhaled so rapidly that no ketones remain in the blood',
        'The dipstick is reading glucose, not ketones',
      ],
      answer: 0,
      rationale:
        'The nitroprusside reaction detects acetoacetate (and acetone) but NOT β-hydroxybutyrate. In DKA the highly reduced mitochondrial matrix pushes the pool toward β-HB, so a dipstick can badly underestimate the true ketone load — and can even appear to worsen during treatment as β-HB is oxidized back to acetoacetate. Direct β-HB measurement is preferred.',
    },
    {
      tag: 'disease',
      stem: 'An infant has recurrent fasting ketoacidotic crises but with INAPPROPRIATELY HIGH ketone levels even between episodes, while hepatic ketone production appears normal. Which defect best fits?',
      choices: [
        'SCOT deficiency — the periphery cannot utilize ketones',
        'MCAD deficiency — β-oxidation of medium chains is blocked',
        'HMG-CoA synthase deficiency — ketones cannot be made',
        'Glucose-6-phosphatase deficiency — hepatic glucose output fails',
      ],
      answer: 0,
      rationale:
        'Persistently HIGH ketones that cannot be cleared point to a ketone-UTILIZATION defect, and SCOT is the committed step of ketolysis. MCAD and HMG-CoA synthase defects instead cause hypoKETOTIC hypoglycemia (too FEW ketones). Glucose-6-phosphatase deficiency (Von Gierke) causes fasting hypoglycemia with a very different metabolite pattern and does not produce a permanent inability to clear ketones.',
    },
    {
      tag: 'integration',
      stem: 'Even during prolonged starvation with high circulating ketones, red blood cells cannot use ketone bodies. Why?',
      choices: [
        'They have no mitochondria, and ketolysis (SCOT and thiolase feeding the TCA cycle) is entirely mitochondrial',
        'They lack the GLUT transporters needed to import ketones',
        'They lack SCOT specifically but retain the rest of the ketolytic machinery',
        'Ketone bodies cannot cross the red-cell membrane',
      ],
      answer: 0,
      rationale:
        'Ketolysis reactivates and cleaves ketones inside the mitochondrion and feeds acetyl-CoA to the TCA cycle — all mitochondrial. Red blood cells have no mitochondria at all, so they remain obligately glucose-dependent regardless of ketone availability. This is exactly why gluconeogenesis can never fully shut off, even in deep starvation.',
    },
    {
      tag: 'regulation',
      stem: 'Which hormonal profile most strongly drives hepatic ketogenesis?',
      choices: [
        'Low insulin with high glucagon',
        'High insulin with low glucagon',
        'High insulin with high glucagon',
        'Low insulin with low glucagon and high cortisol suppression',
      ],
      answer: 0,
      rationale:
        'A low insulin / high glucagon ratio is the ketogenic signal: it releases adipose lipolysis (fatty-acid supply), lowers malonyl-CoA to open CPT-I (fat import), and diverts oxaloacetate into gluconeogenesis so acetyl-CoA is shunted into ketones. High insulin does the opposite — it is the fed, anti-ketogenic state.',
    },
  ],
  funFact:
    'The liver is a fuel factory that can’t eat its own product: it welds acetyl-CoA into ketone bodies for the whole body but lacks SCOT, so it exports every last one. That single missing enzyme is what let Angus Barbieri survive 382 days on water and his own body fat — his liver kept his brain fed on a fuel it could never touch itself.',
};
