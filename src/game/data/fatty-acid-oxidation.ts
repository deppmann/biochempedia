import type { Pathway } from '../types';

/* =============================================================================
   FATTY ACID β-OXIDATION — hand-authored, cross-checked against
   src/content/lessons/fatty-acid-degradation/lesson.mdx. We model ONE trip
   through the machinery: activation (2 ATP toll), the carnitine gate (the
   regulated, committed import step), then ONE round of the four-step spiral
   (dehydrogenase → hydratase → dehydrogenase → thiolase) that clips off one
   acetyl-CoA and one FADH₂ and one NADH. `doubleAfter: 0` — nothing doubles;
   the "doubling" here is the SPIRAL repeating, tracked by netYield, not the
   engine. Palmitate (C16) → 8 acetyl-CoA in 7 rounds.
   ============================================================================ */

export const fattyAcidOxidation: Pathway = {
  id: 'fatty-acid-oxidation',
  name: 'Fatty Acid β-Oxidation',
  emoji: '🔥',
  tagline: 'Pay a 2-ATP cover charge, then chop the fat two carbons at a time.',
  blurb:
    'The body’s long-term fuel gets unlocked, activated at a 2-ATP toll, smuggled into the mitochondrion on carnitine, then chopped two carbons at a time. Each turn of the four-step spiral banks 1 FADH₂, 1 NADH, and 1 acetyl-CoA. Palmitate nets about 106 ATP — dense enough to fast for a year.',
  difficulty: 3,
  location: 'Mitochondrial matrix (after the carnitine shuttle)',
  netYield: 'Per round: 1 FADH₂, 1 NADH, 1 acetyl-CoA. Palmitate (C16) → 8 acetyl-CoA, 7 FADH₂, 7 NADH over 7 rounds; ≈106 net ATP after the 2-ATP activation toll.',
  start: 'Fatty acid (e.g. palmitate)',
  startShort: 'Palmitate',
  startEmoji: '🧈',
  doubleAfter: 0, // nothing doubles per pass; the SPIRAL repeats (tracked in netYield)
  lessonSlug: 'fatty-acid-degradation',
  steps: [
    {
      n: 1,
      product: 'Fatty acyl-CoA (activated)',
      short: 'Acyl-CoA',
      enzyme: 'Acyl-CoA synthetase (fatty acid thiokinase)',
      tokens: { atp: -2 },
      irreversible: true,
      emoji: '🔌',
      fact: 'Activation. ATP is split all the way to AMP + PPᵢ (not ADP + Pᵢ); hydrolyzing the PPᵢ to 2 Pᵢ makes it irreversible and costs 2 high-energy bonds — so the toll is 2 ATP equivalents, the most-missed line in the ledger.',
    },
    {
      n: 2,
      product: 'Fatty acylcarnitine → acyl-CoA inside the matrix',
      short: 'Acylcarnitine',
      enzyme: 'Carnitine shuttle (CPT-I → translocase → CPT-II)',
      irreversible: true,
      committed: true,
      emoji: '🚪',
      fact: 'THE regulated, committed gate. Acyl-CoA is too charged to cross the inner membrane, so CPT-I swaps CoA for carnitine. CPT-I is inhibited by malonyl-CoA (the first committed intermediate of fatty-acid SYNTHESIS) — reciprocal control so the cell never builds and burns fat at once.',
    },
    {
      n: 3,
      product: 'trans-Δ²-enoyl-CoA',
      short: 'Enoyl-CoA',
      enzyme: 'Acyl-CoA dehydrogenase (VLCAD/LCAD/MCAD/SCAD)',
      tokens: { fadh2: 1 },
      emoji: '⚡',
      fact: 'Spiral step 1. Oxidizes between C2 and C3, installing a trans double bond and handing two electrons to FAD → 1 FADH₂. Chain-length isozymes split the work; MCAD is the famous failure point.',
    },
    {
      n: 4,
      product: 'L-3-hydroxyacyl-CoA',
      short: '3-OH-acyl',
      enzyme: 'Enoyl-CoA hydratase (crotonase)',
      emoji: '💧',
      fact: 'Spiral step 2. Water adds across the new double bond with strict stereochemistry, placing an OH on the β-carbon (C3). No cofactor — it just sets up the next oxidation.',
    },
    {
      n: 5,
      product: '3-ketoacyl-CoA',
      short: '3-keto-acyl',
      enzyme: 'L-3-hydroxyacyl-CoA dehydrogenase',
      tokens: { nadh: 1 },
      emoji: '🔋',
      fact: 'Spiral step 3. Oxidizes the β-hydroxyl to a ketone, reducing NAD⁺ → 1 NADH. The new carbonyl polarizes the C2–C3 bond, priming it for cleavage.',
    },
    {
      n: 6,
      product: 'Acetyl-CoA + acyl-CoA shortened by 2C',
      short: 'Acetyl-CoA',
      enzyme: 'β-ketothiolase (3-ketoacyl-CoA thiolase)',
      emoji: '✂️',
      fact: 'Spiral step 4. A second CoA attacks the β-keto carbon and cleaves off the terminal two carbons as acetyl-CoA, leaving an acyl-CoA that is 2 carbons shorter and re-enters at the dehydrogenase. This is the "spiral": repeat until the chain is gone.',
    },
  ],
  regulators: [
    {
      name: 'CPT-I (carnitine palmitoyltransferase I)',
      role: 'THE rate-controlling, committed import gate. Inhibited by malonyl-CoA. When the cell is building fat (malonyl-CoA high), the gate shuts and burning stops.',
    },
    {
      name: 'Malonyl-CoA / acetyl-CoA carboxylase (ACC)',
      role: 'Malonyl-CoA is the first committed intermediate of fatty-acid SYNTHESIS. Its rise (ACC active — insulin, high citrate) closes CPT-I. This is the reciprocal switch between synthesis and degradation.',
    },
    {
      name: 'Glucagon / epinephrine (fasting, sprinting)',
      role: 'Via cAMP → PKA in adipose, mobilize fatty acids (phosphorylate perilipin + HSL) AND, in liver, lower malonyl-CoA → CPT-I opens → β-oxidation ON.',
    },
    {
      name: 'Insulin (fed)',
      role: 'Keeps ACC active and malonyl-CoA high → CPT-I stays shut, β-oxidation OFF. Also suppresses adipose lipolysis so fewer fatty acids are released.',
    },
  ],
  scenarios: [
    {
      id: 'fao-fed',
      emoji: '🍔',
      title: 'You just ate a big burger',
      scene: 'Blood glucose and insulin are up. Fuel is abundant. The liver is in build-and-store mode, running fatty-acid synthesis, not degradation.',
      hormones: 'Insulin ↑ · glucagon ↓',
      flux: 'off',
      decisions: [
        {
          q: 'Which way should β-oxidation run right now?',
          choices: ['Essentially OFF — fuel is plentiful, and the liver is making fat', 'Full speed — burn every fatty acid available'],
          answer: 0,
          why: 'Fed state = build and store. Insulin keeps ACC active, so malonyl-CoA is high, CPT-I is shut, and long-chain fatty acids can’t even get into the matrix to be burned.',
        },
        {
          q: 'What is malonyl-CoA doing to CPT-I?',
          choices: ['Malonyl-CoA is HIGH → inhibits CPT-I → import blocked', 'Malonyl-CoA is low → CPT-I wide open'],
          answer: 0,
          why: 'ACC (active under insulin) makes malonyl-CoA, the first committed intermediate of fatty-acid synthesis. It directly inhibits CPT-I so the cell doesn’t burn what it’s busy building.',
        },
        {
          q: 'Why is shutting the gate the smart move here?',
          choices: ['It prevents a futile synthesis/degradation cycle', 'It saves carnitine, which is in short supply after a meal'],
          answer: 0,
          why: 'Running synthesis and β-oxidation at the same time would just spin ATP in a circle. Reciprocal control via malonyl-CoA guarantees only one runs at a time.',
        },
      ],
      teach: 'FED = insulin high → ACC active → malonyl-CoA high → CPT-I inhibited → β-oxidation essentially OFF. The gate (CPT-I), not the spiral enzymes, is where the fed/fasted decision is enforced.',
    },
    {
      id: 'fao-fast',
      emoji: '🌙',
      title: 'Overnight fast — 14 hours since dinner',
      scene: 'Blood glucose is drifting down. Glucagon rises. Adipose starts releasing free fatty acids into the blood, and the liver switches to burning fat and making ketones.',
      hormones: 'Glucagon ↑ · insulin ↓',
      flux: 'up',
      decisions: [
        {
          q: 'What happens to malonyl-CoA and CPT-I in the fasting liver?',
          choices: ['Malonyl-CoA falls → CPT-I opens → fatty acids pour into the matrix', 'Malonyl-CoA rises → CPT-I opens even wider'],
          answer: 0,
          why: 'Fasting turns ACC down, malonyl-CoA falls, and CPT-I is released from inhibition. The import gate opens and β-oxidation ramps.',
        },
        {
          q: 'How do the fatty acids even get to the liver from adipose?',
          choices: ['Released by lipolysis, riding through plasma clamped to serum albumin', 'Dissolved freely in plasma as sodium salts'],
          answer: 0,
          why: 'Glucagon/epinephrine → cAMP → PKA phosphorylates perilipin and HSL, freeing fatty acids. They’re so insoluble they ride on albumin, roughly six or seven per protein.',
        },
        {
          q: 'What does the liver do with the flood of acetyl-CoA it can’t fully burn?',
          choices: ['Packages it into ketone bodies (acetoacetate, D-3-hydroxybutyrate) to export', 'Converts it directly into glucose for the brain'],
          answer: 0,
          why: 'When acetyl-CoA piles up faster than the TCA cycle takes it, the liver makes ketone bodies for the brain and heart. It cannot make net glucose from even-chain acetyl-CoA — two carbons in, two carbons out as CO₂.',
        },
      ],
      teach: 'FASTING = glucagon high → malonyl-CoA low → CPT-I open → β-oxidation ON, and the surplus acetyl-CoA becomes exportable ketones. The same cAMP-PKA cascade that empties glycogen also mobilizes fat.',
    },
    {
      id: 'fao-marathon',
      emoji: '🏃',
      title: 'Hour three of a marathon',
      scene: 'Glycogen is nearly gone. Sustained, aerobic, low-intensity effort. Muscle needs a steady, oxygen-fueled supply of ATP for the long haul.',
      hormones: 'Epinephrine ↑ · insulin ↓ · AMPK active',
      flux: 'up',
      decisions: [
        {
          q: 'What is the dominant muscle fuel deep into a long endurance effort?',
          choices: ['Fatty acids via β-oxidation (the high-yield, aerobic fuel)', 'Anaerobic glycolysis to lactate'],
          answer: 0,
          why: 'Once glycogen runs low, endurance muscle leans on fat. β-oxidation needs oxygen (the carriers must reach the ETC), which is fine at a sustainable pace — this is not a sprint.',
        },
        {
          q: 'Why does β-oxidation open up during sustained exercise?',
          choices: ['Malonyl-CoA falls (ACC down) → CPT-I opens → more import', 'Carnitine synthesis spikes and drags acyl groups in'],
          answer: 0,
          why: 'Low insulin and AMPK signaling lower malonyl-CoA, releasing CPT-I. Import — not the spiral enzymes — is the throttle, so opening the gate is what raises flux.',
        },
      ],
      teach: 'ENDURANCE = the same lever as fasting: malonyl-CoA down, CPT-I open, fat flooding in. Fat is the marathon fuel precisely because it is so energy-dense (≈106 ATP per palmitate) — but it burns only aerobically.',
    },
    {
      id: 'fao-mcad',
      emoji: '🍼',
      title: 'A toddler with a stomach bug won’t eat',
      scene: 'A previously healthy child skips meals during an illness and becomes lethargic. Glucose is low, but — strangely — ketones are inappropriately low too, and plasma medium-chain acylcarnitines are elevated.',
      hormones: 'Fasting physiology, but fat can’t be burned',
      flux: 'off',
      decisions: [
        {
          q: 'Why are ketones LOW when this fasting child is hypoglycemic?',
          choices: ['β-oxidation is blocked, so there’s no acetyl-CoA surplus to make ketones', 'The liver is exporting all its ketones to the brain, emptying the blood'],
          answer: 0,
          why: 'Normal fasting makes lots of ketones. "Hypoketotic" hypoglycemia is the tell that fat oxidation itself is broken — no β-oxidation, no acetyl-CoA flood, no ketogenesis.',
        },
        {
          q: 'The elevated medium-chain acylcarnitines point the finger at which step?',
          choices: ['Medium-chain acyl-CoA dehydrogenase (MCAD), spiral step 1', 'The carnitine shuttle (CPT-I)'],
          answer: 0,
          why: 'The chain length that piles up localizes the block. Medium chains backing up as acylcarnitines = MCAD, the step-1 dehydrogenase for that chain-length window.',
        },
      ],
      teach: 'This is MCAD deficiency (~1 in 10,000): a child who is fine when fed but crashes on a fast because they cannot burn fat or make ketones. Once misfiled as SIDS, it is now caught on the newborn heel-prick by its acylcarnitine signature.',
    },
    {
      id: 'fao-dka',
      emoji: '🫁',
      title: 'Uncontrolled diabetes — fruity breath in the ER',
      scene: 'A patient with almost no insulin arrives confused, breathing hard, with a sweet fruity odor on the breath. Blood glucose is very high, yet the liver is burning fat as if starving.',
      hormones: 'Insulin ↓↓ · glucagon ↑ (unopposed)',
      flux: 'up',
      decisions: [
        {
          q: 'Why is β-oxidation running hard despite sky-high blood glucose?',
          choices: ['No insulin → malonyl-CoA stays low → CPT-I open → the liver "reads" starvation', 'High glucose directly forces fat oxidation via mass action'],
          answer: 0,
          why: 'Regulation follows the HORMONE, not the raw glucose. Without insulin, ACC stays off, malonyl-CoA stays low, CPT-I stays open, and fat pours into the matrix regardless of the glucose flood.',
        },
        {
          q: 'What is the fruity smell on the breath?',
          choices: ['Acetone, from spontaneous decarboxylation of acetoacetate', 'D-3-hydroxybutyrate, exhaled directly from the blood'],
          answer: 0,
          why: 'Acetoacetate spontaneously decarboxylates to acetone, which is volatile and exhaled. D-3-hydroxybutyrate is the dominant BLOOD ketone but isn’t volatile — it’s not what you smell.',
        },
      ],
      teach: 'DKA is unbraked fasting physiology: no insulin means malonyl-CoA can’t rise to shut CPT-I, so fat burns unchecked, acetyl-CoA floods, and ketones overwhelm the blood’s buffering. The same chemistry that lets someone fast for a year becomes an emergency when nothing holds the gate.',
    },
  ],
  diseases: [
    {
      id: 'mcad-def',
      name: 'MCAD deficiency (medium-chain acyl-CoA dehydrogenase)',
      emoji: '🍼',
      vignette:
        'A 10-month-old, well until now, becomes lethargic and hypoglycemic during a viral illness with poor feeding. Ketones are inappropriately LOW for the degree of hypoglycemia (hypoketotic). Newborn screening had flagged elevated medium-chain acylcarnitines.',
      suspects: [
        'Medium-chain acyl-CoA dehydrogenase (MCAD)',
        'CPT-I (carnitine palmitoyltransferase I)',
        'Acyl-CoA synthetase (activation)',
        'β-ketothiolase (spiral step 4)',
      ],
      answer: 0,
      accumulates: 'Medium-chain fatty acyl-CoA / acylcarnitines',
      missing: 'Acetyl-CoA from medium chains → no ketones during a fast',
      teach:
        'MCAD runs spiral step 1 for medium-chain substrates. Lose it and a child who is perfectly fine when fed cannot burn medium-chain fat during a fast, so blood glucose crashes and — the tell — no acetyl-CoA surplus means no ketones. The chain length that backs up as acylcarnitine pinpoints the enzyme. Once misread as SIDS; now caught on the newborn heel-prick by its acylcarnitine signature.',
      pearl: 'Hypoketotic hypoglycemia + medium-chain acylcarnitines = MCAD, the most common inherited β-oxidation defect (~1:10,000). Management is brutally simple: avoid fasting.',
    },
    {
      id: 'primary-carnitine-def',
      name: 'Primary carnitine deficiency (OCTN2 transporter)',
      emoji: '🚚',
      vignette:
        'A young child has recurrent hypoketotic hypoglycemia, a dilated cardiomyopathy, and muscle weakness. Plasma AND tissue carnitine levels are very low. Supplementing carnitine dramatically improves the picture.',
      suspects: [
        'Plasma-membrane carnitine transporter (OCTN2)',
        'Medium-chain acyl-CoA dehydrogenase (MCAD)',
        'Enoyl-CoA hydratase (crotonase)',
        'Acetyl-CoA carboxylase (ACC)',
      ],
      answer: 0,
      accumulates: 'Long-chain fatty acyl-CoA stranded in the cytosol (can’t be loaded onto carnitine)',
      missing: 'Carnitine itself → the shuttle can’t carry acyl groups into the matrix',
      teach:
        'Without carnitine (here, because the OCTN2 transporter can’t reabsorb it, so it’s lost in urine), the shuttle has no carrier. Long-chain acyl groups can’t be handed from CoA onto carnitine, so they never reach the matrix — long-chain β-oxidation stalls even though every enzyme is intact. Heart and skeletal muscle, which love fat as fuel, suffer most (cardiomyopathy, weakness).',
      pearl: 'The one β-oxidation defect that gets BETTER with carnitine supplementation — because the missing piece is the carrier, not an enzyme.',
    },
    {
      id: 'cpt2-def',
      name: 'CPT-II deficiency',
      emoji: '💪',
      vignette:
        'A teenage athlete gets recurrent episodes of muscle pain and dark (myoglobin-colored) urine after prolonged exercise or fasting — never at rest, always after a long aerobic effort. Creatine kinase spikes during attacks. Enzyme assay confirms the matrix-side transferase is deficient.',
      suspects: [
        'Carnitine palmitoyltransferase II (CPT-II, matrix side)',
        'Pyruvate kinase',
        'Acyl-CoA dehydrogenase (spiral step 1)',
        'Glucose-6-phosphatase',
      ],
      answer: 0,
      accumulates: 'Long-chain acylcarnitines (imported but can’t be handed back to CoA in the matrix)',
      missing: 'Matrix acyl-CoA → long-chain β-oxidation for ATP during sustained effort',
      teach:
        'CPT-II sits on the matrix side and regenerates acyl-CoA from acylcarnitine after import. Lose it and muscle can’t burn long-chain fat during exactly the states that demand it — prolonged exercise and fasting — so muscle fibers break down (rhabdomyolysis → myoglobinuria). The adult muscle form is the most common inherited disorder of lipid metabolism in skeletal muscle.',
      pearl: 'Exercise/fasting-induced rhabdomyolysis with myoglobinuria in a young adult = think CPT-II. Symptoms appear on demand for fat fuel, not at rest.',
    },
  ],
  quiz: [
    {
      tag: 'energetics',
      stem: 'Fatty-acid activation by acyl-CoA synthetase is written as costing "2 ATP." Why 2 rather than 1, when only one ATP is consumed?',
      choices: [
        'ATP is hydrolyzed to AMP + PPᵢ, and the PPᵢ is then split to 2 Pᵢ, consuming a second high-energy bond',
        'Two ATP molecules bind the active site at once',
        'One ATP activates the fatty acid and a second attaches carnitine',
        'The reaction is reversible and must be driven twice',
      ],
      answer: 0,
      rationale:
        'The synthetase splits ATP all the way to AMP + pyrophosphate (not ADP + Pᵢ). Hydrolyzing the PPᵢ to 2 Pᵢ makes the step irreversible and consumes a second high-energy phosphoanhydride bond, so the honest cost is 2 ATP equivalents. Carnitine attachment costs no ATP; only one ATP binds; the step is pulled forward, not run twice.',
    },
    {
      tag: 'basics',
      stem: 'A drug that blocks carnitine palmitoyltransferase I (CPT-I) would MOST directly impair which process?',
      choices: [
        'Entry of long-chain acyl groups into the mitochondrial matrix',
        'Hydrolysis of triacylglycerol in the adipocyte',
        'Reduction of acetoacetate to D-3-hydroxybutyrate',
        'Phosphorylation of glycerol in the liver',
      ],
      answer: 0,
      rationale:
        'CPT-I sits on the outer mitochondrial membrane and transfers the acyl group from CoA onto carnitine — the first committed step of importing long-chain fatty acids for β-oxidation. Block it and acyl-CoA is stranded in the cytosol. It does not touch adipose lipolysis, ketone-body interconversion, or glycerol kinase.',
    },
    {
      tag: 'energetics',
      stem: 'Complete β-oxidation of one palmitate (C16), counting only the spiral itself (not downstream TCA/ETC), yields how many acetyl-CoA, FADH₂, and NADH?',
      choices: [
        '8 acetyl-CoA, 7 FADH₂, 7 NADH',
        '8 acetyl-CoA, 8 FADH₂, 8 NADH',
        '16 acetyl-CoA, 16 FADH₂, 16 NADH',
        '7 acetyl-CoA, 7 FADH₂, 7 NADH',
      ],
      answer: 0,
      rationale:
        'A C16 chain becomes 8 two-carbon acetyl-CoA, but that takes only 7 rounds — the final round splits a 4-carbon unit into two acetyl-CoA at once. Each round makes one FADH₂ and one NADH, so 7 of each, not 8. The classic trap is matching the FADH₂/NADH count to the acetyl-CoA count.',
    },
    {
      tag: 'basics',
      stem: 'In the four-step β-oxidation spiral, which step produces FADH₂, and which produces NADH?',
      choices: [
        'Acyl-CoA dehydrogenase makes FADH₂; L-3-hydroxyacyl-CoA dehydrogenase makes NADH',
        'Enoyl-CoA hydratase makes FADH₂; thiolase makes NADH',
        'Acyl-CoA dehydrogenase makes NADH; the hydratase makes FADH₂',
        'Thiolase makes FADH₂; acyl-CoA dehydrogenase makes NADH',
      ],
      answer: 0,
      rationale:
        'Step 1 (acyl-CoA dehydrogenase) installs the trans-Δ² double bond and reduces FAD → FADH₂. Step 3 (L-3-hydroxyacyl-CoA dehydrogenase) oxidizes the β-hydroxyl to a ketone and reduces NAD⁺ → NADH. The hydratase (step 2) and thiolase (step 4) move no cofactors — hydration and thiolytic cleavage, respectively.',
    },
    {
      tag: 'regulation',
      stem: 'A compound strongly activates hepatic acetyl-CoA carboxylase (ACC). What is the most likely immediate effect on mitochondrial fatty-acid oxidation, and by what mechanism?',
      choices: [
        'Decreased oxidation, because elevated malonyl-CoA inhibits CPT-I and blocks import',
        'Increased oxidation, because more acetyl-CoA is available as substrate',
        'Increased oxidation, because carnitine synthesis is stimulated',
        'Unchanged, because ACC acts only in the cytosol',
      ],
      answer: 0,
      rationale:
        'ACC makes malonyl-CoA, the first committed intermediate of fatty-acid synthesis and a direct inhibitor of CPT-I. Raising malonyl-CoA closes the carnitine import gate, so long-chain fatty acids can’t enter the matrix and oxidation falls. This reciprocal control prevents simultaneous synthesis and degradation. Acetyl-CoA is a product, not the limiting substrate; ACC’s cytosolic location is exactly why its product can act on the outer-membrane CPT-I.',
    },
    {
      tag: 'regulation',
      stem: 'Which single control point most directly determines whether long-chain β-oxidation runs, and what is the physiological logic of its inhibitor?',
      choices: [
        'CPT-I, inhibited by malonyl-CoA so the cell never burns fat while synthesizing it',
        'Thiolase, inhibited by acetyl-CoA so the spiral stops when the TCA cycle is full',
        'Acyl-CoA synthetase, inhibited by AMP so activation halts when energy is low',
        'The hydratase, inhibited by NADH so oxidation slows when carriers are reduced',
      ],
      answer: 0,
      rationale:
        'The carnitine shuttle (CPT-I) is the committed, rate-controlling import step, and malonyl-CoA — the first committed intermediate of fatty-acid synthesis — inhibits it. That linkage enforces reciprocity: when synthesis is on (malonyl-CoA high), import is shut. The other pairings are invented; the spiral enzymes are not the primary regulatory switch.',
    },
    {
      tag: 'disease',
      stem: 'An infant has fasting hypoglycemia with inappropriately LOW ketones and elevated medium-chain acylcarnitines. Which defect best explains the combination?',
      choices: [
        'Medium-chain acyl-CoA dehydrogenase (MCAD) deficiency, stalling β-oxidation of medium chains and starving ketogenesis of acetyl-CoA',
        'Glucose-6-phosphatase deficiency, blocking hepatic glucose output',
        'HMG-CoA reductase deficiency, blocking cholesterol synthesis',
        'Acetyl-CoA carboxylase overactivity, raising malonyl-CoA',
      ],
      answer: 0,
      rationale:
        'Low ketones during fasting hypoglycemia (hypoketotic) says fat oxidation itself is broken — normal fasting makes plenty of ketones. Accumulated medium-chain acylcarnitines localize the block to MCAD, spiral step 1 for those chains; with β-oxidation stalled, there’s no acetyl-CoA surplus to make ketones. G6Pase deficiency gives hypoglycemia with normal/high ketones; HMG-CoA reductase is cholesterol synthesis; raising malonyl-CoA would inhibit CPT-I but wouldn’t give a medium-chain acylcarnitine signature.',
    },
    {
      tag: 'integration',
      stem: 'Why can odd-chain fatty acids contribute to net glucose synthesis while even-chain fatty acids cannot?',
      choices: [
        'Odd-chain oxidation ends in propionyl-CoA → succinyl-CoA, which replenishes the TCA cycle (anaplerosis) so oxaloacetate can be siphoned off to gluconeogenesis; even chains yield only acetyl-CoA (2 C in, 2 C out as CO₂)',
        'Even-chain fatty acids are oxidized in peroxisomes, which lack gluconeogenic enzymes',
        'Odd-chain fatty acids skip the carnitine shuttle and enter the cytosol directly',
        'Odd-chain fatty acids are activated without an ATP cost, leaving energy for gluconeogenesis',
      ],
      answer: 0,
      rationale:
        'Even-chain oxidation makes only acetyl-CoA; the two carbons entering the TCA cycle are matched by two lost as CO₂, so there’s no net oxaloacetate to seed gluconeogenesis. Odd-chain oxidation leaves a final propionyl-CoA, converted (biotin, then B12 enzymes) to succinyl-CoA, which is anaplerotic: it adds net carbon to the cycle, so oxaloacetate can be withdrawn to seed gluconeogenesis. Location, the shuttle, and activation cost are not the basis of the distinction.',
    },
    {
      tag: 'integration',
      stem: 'After ~40 days of total starvation, daily protein breakdown falls from roughly 75 g/day to about 20 g/day. What adaptation most directly accounts for this protein sparing?',
      choices: [
        'The brain shifts much of its fuel use to ketone bodies, cutting its demand for glucose made from amino acids',
        'Hepatic gluconeogenesis rises to supply more glucose to the brain',
        'Red blood cells begin oxidizing fatty acids to spare glucose',
        'Muscle switches to oxidizing branched-chain amino acids exclusively',
      ],
      answer: 0,
      rationale:
        'Early in a fast the brain runs on glucose, which the liver makes largely from amino acids (muscle protein), so proteolysis is high. As ketones rise, the brain shifts much of its fuel to D-3-hydroxybutyrate, cutting glucose demand and therefore the need to break down protein — the Cahill protein-sparing adaptation. More gluconeogenesis would need MORE protein; RBCs lack mitochondria and can’t oxidize fat or ketones; muscle BCAA oxidation alone doesn’t drop whole-body proteolysis this much.',
    },
    {
      tag: 'disease',
      stem: 'A patient in diabetic ketoacidosis has a sweet, fruity odor on the breath. Which molecule is responsible and how is it formed?',
      choices: [
        'Acetone, formed by spontaneous decarboxylation of acetoacetate',
        'D-3-hydroxybutyrate, exhaled directly from the blood',
        'Acetyl-CoA, released from the liver into the airways',
        'Ethanol, from fermentation of excess glucose',
      ],
      answer: 0,
      rationale:
        'Acetoacetate spontaneously decarboxylates to acetone, which is volatile and exhaled — the classic "acetone breath," repeatedly mistaken for alcohol. D-3-hydroxybutyrate is the dominant BLOOD ketone but isn’t volatile; acetyl-CoA is membrane-impermeant and not exhaled; human ketogenesis makes no ethanol.',
    },
  ],
  funFact:
    'Fat is so energy-dense that a 27-year-old Scotsman, Angus Barbieri, fasted for 382 days on water, tea, and vitamins — dropping from 456 to 180 pounds. For over a year his brain ran largely on D-3-hydroxybutyrate made from his own body fat: β-oxidation is a year of brain fuel waiting to be unlocked.',
};
