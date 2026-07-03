import type { Pathway } from '../types';

/* =============================================================================
   FATTY ACID SYNTHESIS — hand-authored, cross-checked against
   src/content/lessons/fatty-acid-synthesis/lesson.mdx. Cytosolic anabolism that
   is deliberately NOT β-oxidation run backward: citrate shuttle exports acetyl-
   CoA, acetyl-CoA carboxylase (the committed, biotin-dependent, ATP-spending
   step) makes malonyl-CoA, and fatty acid synthase runs the CRDR cycle
   (Condensation, Reduction, Dehydration, Reduction) seven times to build
   palmitate (C16) two carbons at a time. Reducing power is NADPH, not NADH.

   `doubleAfter: 0` — no split, no doubling. Tokens are authored per single
   chain: −1 ATP at ACC (per malonyl-CoA made) and −1 NADPH at each of the two
   reductions. The headline ledger for the full C16 is 8 acetyl-CoA + 7 ATP +
   14 NADPH + 7 HCO₃⁻ → palmitate + 7 CO₂ + 8 CoA + 6 H₂O.
   ============================================================================ */

export const fattyAcidSynthesis: Pathway = {
  id: 'fatty-acid-synthesis',
  name: 'Fatty Acid Synthesis',
  emoji: '🧈',
  tagline: 'Turn one leftover cookie into fat, two carbons at a time. The cell never wastes a snack.',
  blurb:
    'A fed cell stitches spare acetyl-CoA into palmitate in the cytosol — NOT β-oxidation in reverse. Citrate ferries the carbon out, acetyl-CoA carboxylase spends an ATP to commit it, and fatty acid synthase runs the CRDR cycle seven times, burning NADPH to build a 16-carbon chain.',
  difficulty: 3,
  location: 'Cytosol',
  netYield: 'Builds palmitate (C16) 2 carbons at a time; costs 7 ATP (at ACC) + 14 NADPH per chain',
  start: 'Acetyl-CoA (cytosol)',
  startShort: 'Acetyl-CoA',
  startEmoji: '🧱',
  doubleAfter: 0, // no cleavage step — the chain is built up, never split
  lessonSlug: 'fatty-acid-synthesis',
  steps: [
    {
      n: 1,
      product: 'Acetyl-CoA + oxaloacetate (cytosol)',
      short: 'Citrate→AcCoA',
      enzyme: 'ATP-citrate lyase',
      tokens: { atp: -1 },
      emoji: '🚕',
      fact: 'Carbon delivery. Acetyl-CoA is made in the mitochondrion but can’t cross the membrane, so it rides out disguised as citrate; ATP-citrate lyase cleaves citrate back to acetyl-CoA + OAA in the cytosol, spending 1 ATP. Citrate is the "Uber for acetyl groups." Target of the LDL drug bempedoic acid.',
    },
    {
      n: 2,
      product: 'Pyruvate + NADPH (from OAA)',
      short: 'Malic enzyme',
      enzyme: 'Malate dehydrogenase + malic enzyme',
      tokens: { nadph: 1 },
      emoji: '🎁',
      fact: 'The shuttle is a two-for-one: leftover OAA → malate → pyruvate, and malic enzyme banks NADPH on the way. ~8 of the 14 NADPH per palmitate come from here; the pentose phosphate pathway supplies the other 6. Pyruvate returns to the mitochondrion.',
    },
    {
      n: 3,
      product: 'Malonyl-CoA',
      short: 'Malonyl-CoA',
      enzyme: 'Acetyl-CoA carboxylase (ACC)',
      tokens: { atp: -1, co2: -1 },
      irreversible: true,
      committed: true,
      emoji: '🚦',
      fact: 'THE committed, rate-limiting step. A biotin arm acts as a CO₂ taxi (same trick as pyruvate carboxylase), attaching CO₂ to acetyl-CoA for 1 ATP. Once malonyl-CoA exists, the carbon is committed to fat. Activated by citrate + insulin; inhibited by palmitoyl-CoA + glucagon/AMPK. Malonyl-CoA also blocks CPT-I, so the cell never burns and builds fat at once.',
    },
    {
      n: 4,
      product: 'Acetyl-ACP + malonyl-ACP',
      short: 'Load ACP',
      enzyme: 'FAS: malonyl/acetyl transferase (priming)',
      emoji: '🦾',
      fact: 'Both units are loaded onto the acyl carrier protein (ACP) arm of fatty acid synthase — a multidomain homodimer. ACP’s long phosphopantetheine "swinging arm" tethers the growing chain so it never floats free (contrast: β-oxidation uses free CoA).',
    },
    {
      n: 5,
      product: 'β-Ketoacyl-ACP + CO₂',
      short: 'Condense (C)',
      enzyme: 'FAS: β-ketoacyl synthase',
      tokens: { co2: 1 },
      emoji: '🔗',
      fact: 'The C of CRDR. Units join into a 4-carbon β-ketoacyl chain and the malonyl CO₂ — the very one ACC just added — is released. That decarboxylation is the engine: two acetyl units can’t condense directly (uphill), so the cell spends a CO₂ to pull it forward, then takes it right back. CO₂ is a leaving group, not a building block.',
    },
    {
      n: 6,
      product: 'D-3-hydroxyacyl-ACP',
      short: 'Reduce (R)',
      enzyme: 'FAS: β-ketoacyl reductase',
      tokens: { nadph: -1 },
      emoji: '💧',
      fact: 'The first R of CRDR. The keto group is reduced to a hydroxyl using NADPH. Synthesis makes the D-isomer here; β-oxidation runs through the L-isomer — same atoms, opposite stereochemistry, one more sign the two pathways are genuinely separate machines.',
    },
    {
      n: 7,
      product: 'trans-Enoyl-ACP + H₂O',
      short: 'Dehydrate (D)',
      enzyme: 'FAS: dehydratase',
      emoji: '🌊',
      fact: 'The D of CRDR. Water leaves, creating a trans double bond. The chain is now one reduction away from being fully saturated.',
    },
    {
      n: 8,
      product: 'Acyl-ACP (saturated, +2C)',
      short: 'Reduce (R)',
      enzyme: 'FAS: enoyl reductase',
      tokens: { nadph: -1 },
      emoji: '🔁',
      fact: 'The second R of CRDR. A second NADPH saturates the double bond, finishing one turn with a chain 2 carbons longer. The cycle then repeats: each turn spends 1 malonyl-CoA (2C) + 2 NADPH. Seven turns build C16.',
    },
    {
      n: 9,
      product: 'Palmitate (C16) + ACP',
      short: 'Palmitate',
      enzyme: 'FAS: thioesterase',
      emoji: '🏁',
      fact: 'After 7 CRDR cycles the chain hits 16 carbons and thioesterase clips it free as palmitate. Balanced ledger: 8 acetyl-CoA + 7 ATP + 14 NADPH + 7 HCO₃⁻ → palmitate + 7 CO₂ + 8 CoA + 6 H₂O. Elongation past C16 and any double bonds are added later on the ER — and mammals can’t desaturate past C9, so ω-3/ω-6 fats are essential.',
    },
  ],
  regulators: [
    {
      name: 'Acetyl-CoA carboxylase (ACC)',
      role: 'THE switch. Committed step. ↑ by citrate (fuel abundant) & insulin; ↓ by palmitoyl-CoA (product feedback), glucagon/epinephrine, and AMPK phosphorylation. This is where flux is set.',
    },
    {
      name: 'Citrate',
      role: 'Allosteric ON. Polymerizes ACC into active filaments — high citrate signals "carbon is overflowing, store it." Also the shuttle that carries the acetyl carbon out.',
    },
    {
      name: 'Palmitoyl-CoA',
      role: 'Allosteric OFF. The end product depolymerizes ACC filaments — a clean feedback brake ("we have enough fat, stop building").',
    },
    {
      name: 'AMPK',
      role: 'The low-fuel sensor. Rising AMP:ATP activates AMPK → phosphorylates & inactivates ACC → synthesis off, oxidation on. PP2A dephosphorylates ACC to turn it back on. This is where metformin and exercise act.',
    },
    {
      name: 'Malonyl-CoA (→ CPT-I)',
      role: 'The reciprocal lock. ACC’s product inhibits CPT-I, the gate for fatty-acid entry into mitochondria — so committing to synthesis slams the door on β-oxidation. Never build and burn at once.',
    },
    {
      name: 'Insulin / glucagon',
      role: 'The hormonal set-point. Insulin (fed) activates ACC; glucagon & epinephrine (fasting/stress) inhibit it — the same fed/fasted logic as glycolysis, in reciprocal opposition to fat burning.',
    },
  ],
  scenarios: [
    {
      id: 'fas-fed',
      emoji: '🍕',
      title: 'You ate more pizza than you’ll burn',
      scene: 'Blood glucose and fuel are high, insulin is pouring out, and the TCA cycle is backing up with citrate. The liver’s job now: bank the surplus carbon as fat.',
      hormones: 'Insulin ↑ · glucagon ↓ · citrate ↑',
      flux: 'up',
      decisions: [
        {
          q: 'Which way should fatty acid synthesis run right now?',
          choices: ['Ramp UP — store the surplus carbon as fat', 'Shut DOWN — save the carbon for fuel'],
          answer: 0,
          why: 'Fed state = fuel overflowing. Insulin says "store it," and surplus acetyl-CoA gets stitched into palmitate. This is exactly the one-cookie/one-slice-of-pizza chemistry.',
        },
        {
          q: 'What is happening to acetyl-CoA carboxylase (ACC)?',
          choices: [
            'Activated — citrate polymerizes it and insulin (via PP2A) dephosphorylates it ON',
            'Inhibited — AMPK phosphorylates it OFF',
          ],
          answer: 0,
          why: 'High citrate polymerizes ACC into active filaments and insulin promotes its dephosphorylation. Both push the committed step ON, so malonyl-CoA (and fat) is made.',
        },
        {
          q: 'What does the rising malonyl-CoA do to fat burning (CPT-I)?',
          choices: ['Blocks CPT-I → shuts β-oxidation OFF', 'Activates CPT-I → burns fat at the same time'],
          answer: 0,
          why: 'Malonyl-CoA inhibits CPT-I, closing the mitochondrial gate for fatty-acid import. The cell commits to building and refuses to burn simultaneously — no futile cycle.',
        },
      ],
      teach: 'FED = insulin high, citrate high → ACC ON → malonyl-CoA rises → synthesis floors AND CPT-I is blocked so oxidation stops. One switch (ACC) turns building on and burning off at the same instant.',
    },
    {
      id: 'fas-fasted',
      emoji: '😴',
      title: 'Overnight fast — 14 hours since dinner',
      scene: 'Glucose is drifting down, glucagon is up, and the liver needs to release energy, not store it. Building fat now would be self-defeating.',
      hormones: 'Glucagon ↑ · insulin ↓',
      flux: 'off',
      decisions: [
        {
          q: 'Should the liver run fatty acid synthesis now?',
          choices: ['No — shut it down; this is a burn-and-export state', 'Yes — keep banking fat as usual'],
          answer: 0,
          why: 'Fasting = mobilize, don’t store. Glucagon shuts ACC off; the liver oxidizes fat and exports fuel instead of building new palmitate.',
        },
        {
          q: 'With ACC off and malonyl-CoA low, what happens at CPT-I?',
          choices: ['CPT-I is de-repressed → fatty acids enter mitochondria for β-oxidation', 'CPT-I stays blocked → fat can’t be burned'],
          answer: 0,
          why: 'Low malonyl-CoA lifts the brake on CPT-I, so fatty acids flood into the mitochondrion for β-oxidation. The reciprocal switch flips cleanly the other way.',
        },
      ],
      teach: 'FASTED = glucagon high → ACC OFF → malonyl-CoA falls → synthesis is essentially off AND CPT-I opens so β-oxidation runs. The exact reciprocal of the fed state, driven by the same malonyl-CoA lever.',
    },
    {
      id: 'fas-exercise',
      emoji: '🏃',
      title: 'Mid-run, 30 minutes in',
      scene: 'Muscle is spending ATP fast, the AMP:ATP ratio is climbing, and the cell’s low-fuel alarm is going off. Building fat is the last thing it should do.',
      hormones: 'AMP:ATP ↑ · AMPK ON',
      flux: 'off',
      decisions: [
        {
          q: 'What does rising AMP do to ACC?',
          choices: ['Activates AMPK, which phosphorylates and INACTIVATES ACC', 'Activates AMPK, which phosphorylates and ACTIVATES ACC'],
          answer: 0,
          why: 'AMPK is the fuel gauge: high AMP:ATP switches it on, and it phosphorylates ACC to turn it OFF. When energy is scarce, stop construction.',
        },
        {
          q: 'What is the net effect on the build-vs-burn see-saw?',
          choices: ['Synthesis falls and β-oxidation rises', 'Synthesis rises and β-oxidation falls'],
          answer: 0,
          why: 'ACC off → less malonyl-CoA → less synthesis AND CPT-I released → more oxidation. AMPK tilts the whole cell from storing to burning.',
        },
      ],
      teach: 'EXERCISE = high AMP → AMPK ON → ACC OFF. Synthesis stops, oxidation ramps. This is the same node metformin hijacks: raise AMP:ATP, activate AMPK, suppress lipogenesis, derepress fat burning.',
    },
    {
      id: 'fas-metformin',
      emoji: '💊',
      title: 'Type 2 diabetes, first dose of metformin',
      scene: 'The most-prescribed diabetes drug hits Complex I of the mitochondrion, and the cellular AMP:ATP ratio climbs — mimicking a low-energy state even at rest.',
      hormones: 'AMP:ATP ↑ (drug-induced) · AMPK ON',
      flux: 'down',
      decisions: [
        {
          q: 'Metformin raises AMP:ATP. What does that do to ACC and fat metabolism?',
          choices: [
            'AMPK is activated → ACC phosphorylated OFF → synthesis falls, oxidation rises',
            'PP2A is activated → ACC dephosphorylated ON → synthesis rises',
          ],
          answer: 0,
          why: 'A higher AMP:ATP ratio activates AMPK, which inactivates ACC. Less malonyl-CoA means less synthesis and, by relieving the CPT-I block, more oxidation.',
        },
        {
          q: 'Why doesn’t high citrate override the drug here?',
          choices: [
            'AMPK phosphorylation dominates — the covalent OFF signal wins over the allosteric ON',
            'Citrate can’t reach ACC when metformin is present',
          ],
          answer: 0,
          why: 'ACC integrates covalent (phosphorylation) and allosteric (citrate/palmitoyl-CoA) inputs. With AMPK firing, the phosphorylation keeps the enzyme off despite citrate’s push — the low-energy signal takes priority.',
        },
      ],
      teach: 'Metformin → Complex I inhibited → AMP:ATP ↑ → AMPK ON → ACC OFF. Synthesis falls, oxidation rises. A medieval French-lilac remedy and a modern blockbuster meet at exactly the enzyme you just learned.',
    },
    {
      id: 'fas-alcohol',
      emoji: '🍺',
      title: 'A heavy night of drinking',
      scene: 'The liver is metabolizing ethanol, and alcohol dehydrogenase + ALDH are flooding the cytosol and mitochondria with NADH. Fat is piling up in the hepatocytes.',
      hormones: 'NADH:NAD⁺ ↑↑ (redox jammed)',
      flux: 'up',
      decisions: [
        {
          q: 'Why does drinking cause fatty liver even without extra food?',
          choices: [
            'Excess NADH stalls the TCA cycle, shunting acetyl-CoA toward fat and ketones',
            'Ethanol directly activates AMPK, so fat is burned faster',
          ],
          answer: 0,
          why: 'Ethanol metabolism jams the NADH:NAD⁺ ratio. A stalled TCA cycle backs up acetyl-CoA and citrate, which drive fat synthesis and ketogenesis — the classic alcoholic fatty liver.',
        },
        {
          q: 'Where does the excess reducing power for building the fat come from in this state?',
          choices: [
            'NADPH from the pentose phosphate pathway + malic enzyme (NADH itself can’t reduce the chain)',
            'The NADH directly — FAS uses NADH like β-oxidation does',
          ],
          answer: 0,
          why: 'FAS reductions require NADPH, not NADH — that’s the whole "separate currency" point. The reducing equivalents come from the PPP and the malic-enzyme step, not from the ethanol-derived NADH.',
        },
      ],
      teach: 'Alcohol breaks the see-saw from the redox side: a flood of NADH stalls the TCA cycle and pushes acetyl-CoA into fat. Note the currency — FAS still runs on NADPH, underscoring why NADPH ≠ NADH is a real, load-bearing distinction.',
    },
  ],
  diseases: [
    {
      id: 'biotin-def',
      name: 'Biotin deficiency / ACC cofactor loss (the egg-white syndrome)',
      emoji: '🥚',
      vignette:
        'A body-builder eating a dozen RAW egg whites a day develops hair loss, a scaly rash, and neurologic symptoms. A lab classmate reproduces it in rats. Carboxylase reactions across the cell are impaired.',
      suspects: ['Biotin (ACC’s CO₂-carrying cofactor)', 'NADPH (the reducing currency)', 'CoA (the acetyl carrier)', 'ATP-citrate lyase (the export enzyme)'],
      answer: 0,
      accumulates: 'Acetyl-CoA (can’t be carboxylated to malonyl-CoA)',
      missing: 'Malonyl-CoA → no fatty acid synthesis; other biotin carboxylases also fail',
      teach:
        'Raw egg white contains avidin, which binds biotin with a dissociation constant near 10⁻¹⁵ M — one of the tightest bonds in biology — and sequesters the vitamin. Without biotin, ACC can’t carry CO₂, so it can’t make malonyl-CoA and fatty acid synthesis stalls (pyruvate carboxylase and other biotin enzymes fail too). Cooking the egg denatures avidin and frees the biotin. This is the 1927 Wisconsin egg-white experiment that revealed biotin as a vitamin.',
      pearl: 'Raw-egg-white / avidin = biotin sequestration → ACC (and all biotin-dependent carboxylases) fail. Cook the eggs and it resolves.',
    },
    {
      id: 'citrate-lyase-block',
      name: 'ATP-citrate lyase blockade (bempedoic acid, a mechanism)',
      emoji: '🚕',
      vignette:
        'A statin-intolerant patient is started on bempedoic acid to lower LDL. In the liver, the cytosolic supply of the two-carbon building block for both fat and cholesterol synthesis is cut off — upstream of ACC.',
      suspects: [
        'ATP-citrate lyase (citrate → cytosolic acetyl-CoA)',
        'Acetyl-CoA carboxylase (acetyl-CoA → malonyl-CoA)',
        'Fatty acid synthase (chain elongation)',
        'Malic enzyme (NADPH generation)',
      ],
      answer: 0,
      accumulates: 'Citrate (can’t be cleaved in the cytosol)',
      missing: 'Cytosolic acetyl-CoA → less substrate for BOTH fatty acid and cholesterol synthesis',
      teach:
        'ATP-citrate lyase is the Stage-1 export enzyme: it cleaves citrate into cytosolic acetyl-CoA + OAA, feeding both lipogenesis and cholesterol synthesis. Bempedoic acid inhibits it (as an activated form made only in liver), lowering LDL with less muscle effect than statins. Blocking it starves the whole downstream pathway of its 2-carbon bricks, upstream of the committed ACC step.',
      pearl: 'ATP-citrate lyase = the cytosolic acetyl-CoA faucet for fat AND cholesterol; bempedoic acid targets it, liver-selectively, to drop LDL.',
    },
    {
      id: 'efa-deficiency',
      name: 'Essential fatty acid deficiency (the desaturase gap)',
      emoji: '🐟',
      vignette:
        'A patient on long-term fat-free IV nutrition develops a dry, scaly dermatitis and poor wound healing. Their FAS works perfectly and they make plenty of palmitate — yet a whole class of fatty acids is missing.',
      suspects: [
        'ω-6/ω-3 desaturases (absent in mammals past C9)',
        'Fatty acid synthase (chain assembly)',
        'Acetyl-CoA carboxylase (the committed step)',
        'Elongases (chain extension on the ER)',
      ],
      answer: 0,
      accumulates: 'Mead acid (20:3 ω-9) — the tell-tale abnormal substitute',
      missing: 'Linoleate (ω-6) → arachidonate; linolenate (ω-3) → EPA/DHA — both feed eicosanoid signaling and membranes',
      teach:
        'Mammalian desaturases can install a double bond only up to carbon 9 (counting from the carboxyl end); they cannot reach the ω-6 or ω-3 positions. So even a flawless FAS can’t make linoleate or linolenate — those are essential and must be eaten. Deprived, the body substitutes the ω-9 Mead acid, and eicosanoid signaling and skin barrier suffer. Burr & Burr proved this in 1929 with fat-free-diet rats.',
      pearl: 'FAS is fine; the missing enzymes are the ω-6/ω-3 desaturases. Linoleate & linolenate are essential; deficiency raises Mead acid (20:3 ω-9).',
    },
  ],
  quiz: [
    {
      tag: 'basics',
      stem: 'Fatty acid synthesis is often contrasted with β-oxidation. Which set of three features correctly describes SYNTHESIS (not degradation)?',
      choices: [
        'Cytoplasm, ACP carrier, NADPH consumed',
        'Mitochondrion, CoA carrier, NADH produced',
        'Cytoplasm, CoA carrier, FADH₂ produced',
        'Mitochondrion, ACP carrier, NADPH consumed',
      ],
      answer: 0,
      rationale:
        'Synthesis runs in the cytoplasm, carries intermediates on ACP via a phosphopantetheine arm, and consumes NADPH. The mitochondrion/CoA/NADH option is β-oxidation; the other two scramble features from both pathways — exactly the confusion this pathway is built to prevent.',
    },
    {
      tag: 'regulation',
      stem: 'Which reaction is the committed step of fatty acid synthesis, and what cofactor does the enzyme require?',
      choices: [
        'Acetyl-CoA carboxylase making malonyl-CoA; requires biotin',
        'β-Ketoacyl synthase condensing acetyl + malonyl; requires biotin',
        'ATP-citrate lyase cleaving citrate; requires NADPH',
        'Thioesterase releasing palmitate; requires CoA',
      ],
      answer: 0,
      rationale:
        'Acetyl-CoA carboxylase (ACC) carboxylates acetyl-CoA to malonyl-CoA using a biotin cofactor and one ATP; once malonyl-CoA exists the carbon is committed to fat. ATP-citrate lyase is the upstream export step, thioesterase releases the product, and the condensing enzyme is not the regulated commitment point.',
    },
    {
      tag: 'energetics',
      stem: 'Per molecule of palmitate (C16) synthesized from acetyl-CoA, how many NADPH and ATP are consumed?',
      choices: ['14 NADPH and 7 ATP', '16 NADPH and 8 ATP', '8 NADPH and 7 ATP', '7 NADPH and 14 ATP'],
      answer: 0,
      rationale:
        'Full stoichiometry: 8 acetyl-CoA + 7 ATP + 14 NADPH + 7 HCO₃⁻ → palmitate + 7 CO₂ + 8 CoA + 6 H₂O. Fourteen NADPH come from the two reductions across seven CRDR cycles (2 per cycle); seven ATP are spent making the seven malonyl-CoA units at ACC. The other options swap or mis-scale the two currencies.',
    },
    {
      tag: 'basics',
      stem: 'A student claims the CO₂ added by ACC ends up built into the carbon skeleton of palmitate. Why is this incorrect?',
      choices: [
        'The CO₂ is released again during condensation; its decarboxylation drives the otherwise-uphill joining forward',
        'CO₂ is incorporated, but only into the terminal carboxyl group',
        'ACC never adds CO₂ — it adds a hydroxyl group',
        'The CO₂ is reduced to a methyl group by NADPH',
      ],
      answer: 0,
      rationale:
        'The CO₂ attached to make malonyl-CoA is released at condensation, and that decarboxylation is the thermodynamic driving force that makes joining two units favorable. CO₂ is a leaving group, not a building block — the "quarter in a vending machine" you never get back but that makes the snack come out.',
    },
    {
      tag: 'regulation',
      stem: 'Beyond feeding chain elongation, what is malonyl-CoA’s key regulatory action that enforces reciprocal control between fat synthesis and fat breakdown?',
      choices: [
        'It inhibits CPT-I, blocking fatty-acid entry into the mitochondrion for oxidation',
        'It depolymerizes ACC, switching synthesis off',
        'It activates AMPK, slowing synthesis',
        'It activates cytochrome b5 on the ER',
      ],
      answer: 0,
      rationale:
        'Malonyl-CoA inhibits carnitine palmitoyltransferase I (CPT-I), the gate for importing fatty acids into mitochondria for β-oxidation. So the instant the cell commits to synthesis it blocks oxidation — the reciprocal see-saw. (Palmitoyl-CoA, not malonyl-CoA, depolymerizes ACC; AMPK is activated by low energy charge; cytochrome b5 serves desaturases.)',
    },
    {
      tag: 'regulation',
      stem: 'A patient with type 2 diabetes starts metformin, which inhibits mitochondrial Complex I and raises the AMP:ATP ratio. Predict the effect on ACC and fatty-acid metabolism.',
      choices: [
        'AMPK is activated, ACC is phosphorylated and inhibited, so synthesis falls and oxidation rises',
        'Citrate accumulates, polymerizing ACC and increasing synthesis',
        'PP2A is activated, ACC is dephosphorylated and activated, so synthesis rises',
        'Insulin signaling increases, activating ACC and increasing malonyl-CoA',
      ],
      answer: 0,
      rationale:
        'A higher AMP:ATP ratio activates AMPK, which phosphorylates and inactivates ACC. Less ACC activity means less malonyl-CoA, so synthesis falls; less malonyl-CoA also relieves the CPT-I block, so oxidation rises. The distractors all describe activating inputs — the opposite of metformin’s effect through AMPK.',
    },
    {
      tag: 'integration',
      stem: 'A cell line is fed acetyl-CoA uniformly labeled with ¹⁴C and, separately, ¹⁴C-bicarbonate; palmitate is then isolated. Compared with the acetyl-CoA label, what will the bicarbonate label in palmitate show, and why?',
      choices: [
        'Little to no label, because the CO₂ from bicarbonate is released at condensation rather than incorporated',
        'Equal labeling, because both carbons are incorporated into the chain',
        'Heavy labeling at every other carbon, because bicarbonate provides the methylene carbons',
        'Label only in the terminal methyl group, because that is where bicarbonate enters',
      ],
      answer: 0,
      rationale:
        'Bicarbonate’s carbon is fixed by ACC to make malonyl-CoA, but it is released again during condensation, so it is not built into palmitate. The acetyl-CoA carbons all end up in the chain. This isotope result is the classic proof that CO₂ is a leaving group, not a building block.',
    },
    {
      tag: 'integration',
      stem: 'A hepatocyte defect abolishes cytoplasmic malic enzyme activity while the pentose phosphate pathway stays intact and citrate import is normal. What is the most direct consequence for fatty acid synthesis?',
      choices: [
        'About 8 of the 14 NADPH per palmitate are lost, throttling synthesis unless the PPP compensates',
        'Acetyl-CoA can no longer be exported from the mitochondrion',
        'The committed step (ACC) can no longer carboxylate acetyl-CoA',
        'Palmitate cannot be released because thioesterase requires malic enzyme',
      ],
      answer: 0,
      rationale:
        'Malic enzyme supplies roughly 8 of the 14 NADPH per palmitate via the citrate shuttle; the PPP supplies the rest. Losing it cuts a major reducing-power source, limiting synthesis unless the PPP makes up the shortfall. Acetyl-CoA export (ATP-citrate lyase), ACC carboxylation, and thioesterase are all independent of malic enzyme.',
    },
    {
      tag: 'basics',
      stem: 'Fatty acid synthase (FAS) builds palmitate by repeating a four-step cycle. What are the four steps, in order?',
      choices: [
        'Condensation → Reduction → Dehydration → Reduction (CRDR)',
        'Condensation → Dehydration → Reduction → Reduction',
        'Reduction → Condensation → Reduction → Dehydration',
        'Dehydration → Reduction → Condensation → Reduction',
      ],
      answer: 0,
      rationale:
        'The cycle is CRDR: Condensation joins the acetyl/growing chain to a malonyl unit (releasing CO₂), Reduction (NADPH) turns the keto into a hydroxyl, Dehydration removes water to form a trans double bond, and a second Reduction (NADPH) saturates it. Each pass adds 2 carbons; seven passes reach C16.',
    },
    {
      tag: 'disease',
      stem: 'A patient on months of fat-free parenteral nutrition develops scaly dermatitis, and blood work shows rising Mead acid (20:3 ω-9). Their fatty acid synthase is fully functional. What is missing?',
      choices: [
        'Dietary essential fatty acids — mammals lack the ω-6/ω-3 desaturases to make them',
        'Biotin — ACC cannot carboxylate acetyl-CoA',
        'NADPH — the reductions in CRDR cannot proceed',
        'ATP-citrate lyase — acetyl-CoA cannot leave the mitochondrion',
      ],
      answer: 0,
      rationale:
        'Mammalian desaturases place double bonds only up to C9, so linoleate (ω-6) and linolenate (ω-3) are essential and must be eaten. FAS still makes palmitate fine, but without dietary essential fats the body substitutes ω-9 Mead acid and skin/eicosanoid function suffer. The other options would block palmitate synthesis itself, which is intact here.',
    },
  ],
  funFact:
    'The whole assembly line is one enzyme: mammalian fatty acid synthase is a single giant homodimer folding a condensing enzyme, two reductases, a dehydratase, a transferase, and the swinging ACP arm into one machine — so a growing chain is handed from active site to active site seven times without ever floating free.',
};
