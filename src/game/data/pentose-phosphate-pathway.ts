import type { Pathway } from '../types';

/* =============================================================================
   PENTOSE PHOSPHATE PATHWAY (PPP / hexose monophosphate shunt) — hand-authored,
   cross-checked against src/content/lessons/pentose-phosphate-pathway/lesson.mdx.
   Eight steps from glucose-6-phosphate. Two phases: an IRREVERSIBLE oxidative
   phase (G6PD → lactonase → 6PGD) that banks 2 NADPH + 1 CO₂ and drops off at
   ribulose-5-P, and a REVERSIBLE non-oxidative phase (isomerase/epimerase +
   two transketolase cuts + one transaldolase cut) that reshuffles carbon
   (3 C5 ⇌ 2 F6P + 1 G3P). Net oxidative yield per G6P: 2 NADPH + ribose-5-P.
   Makes NO ATP — and that is the point. `doubleAfter: 0` (nothing doubles; one
   G6P in, one ribulose-5-P out — the non-oxidative reshuffle needs three C5s to
   balance but the single-molecule ledger the engine tracks never splits ×2).
   ============================================================================ */

export const pentosePhosphatePathway: Pathway = {
  id: 'pentose-phosphate-pathway',
  name: 'Pentose Phosphate Pathway',
  emoji: '🔀',
  tagline: 'Skips the ATP entirely and walks off with reducing power and DNA sugar. The anti-glycolysis.',
  blurb:
    'Glucose-6-phosphate can burn for ATP in glycolysis — or take the other fork. The PPP makes no ATP at all; instead it banks NADPH (reducing power for biosynthesis and antioxidant defense) and ribose-5-phosphate (the backbone of every nucleotide). An irreversible oxidative phase makes the NADPH; a reversible non-oxidative phase reshuffles the carbon to match demand.',
  difficulty: 2,
  location: 'Cytosol',
  netYield: '2 NADPH + ribose-5-P per glucose-6-P (oxidative phase); no ATP',
  start: 'Glucose-6-phosphate',
  startShort: 'G6P',
  startEmoji: '🍬',
  doubleAfter: 0, // nothing doubles — single G6P in, single ribulose-5-P out
  lessonSlug: 'pentose-phosphate-pathway',
  steps: [
    {
      n: 1,
      product: '6-Phosphogluconolactone',
      short: '6PGL',
      enzyme: 'Glucose-6-phosphate dehydrogenase (G6PD)',
      tokens: { nadph: 1 },
      irreversible: true,
      committed: true,
      emoji: '🚪',
      fact: 'THE committed, rate-limiting step and the only regulated one. Oxidizes C1 of G6P and reduces NADP⁺ → the first NADPH. Product-inhibited by NADPH, so the cell holds this door shut when reducing power is plentiful.',
    },
    {
      n: 2,
      product: '6-Phosphogluconate',
      short: '6PG',
      enzyme: '6-Phosphogluconolactonase',
      emoji: '🧹',
      fact: 'Hydrolyzes the strained δ-lactone ring open to the linear acid. A quiet housekeeping step — it creeps along on its own, but the enzyme makes it fast and clean.',
    },
    {
      n: 3,
      product: 'Ribulose-5-phosphate + CO₂',
      short: 'Ru5P',
      enzyme: '6-Phosphogluconate dehydrogenase',
      tokens: { nadph: 1, co2: 1 },
      irreversible: true,
      emoji: '💨',
      fact: 'Oxidative decarboxylation: makes the SECOND NADPH and lops off C1 as CO₂ (C6 → C5). Losing that carbon is what locks the whole oxidative phase one-way — you can run a sugar uphill, but you can’t stick a CO₂ back on.',
    },
    {
      n: 4,
      product: 'Ribose-5-phosphate',
      short: 'R5P',
      enzyme: 'Phosphopentose isomerase',
      emoji: '🧬',
      fact: 'Ketose → aldose. This is the biosynthetic exit: ribose-5-P is the sugar backbone of every nucleotide (via PRPP), feeding DNA, RNA, ATP, NAD⁺, and coenzyme A. Reversible — the non-oxidative phase can run backward to make it too.',
    },
    {
      n: 5,
      product: 'Xylulose-5-phosphate',
      short: 'Xu5P',
      enzyme: 'Phosphopentose epimerase',
      emoji: '🔃',
      fact: 'Inverts the configuration at a single carbon (C3) of ribulose-5-P. Ribulose and xylulose are epimers — identical except that one stereocenter — but transketolase demands xylulose, so the small change matters.',
    },
    {
      n: 6,
      product: 'Sedoheptulose-7-P + Glyceraldehyde-3-P',
      short: 'S7P + G3P',
      enzyme: 'Transketolase (TPP)',
      emoji: '✂️',
      fact: 'Molecular scissors: snips a 2-carbon ketol unit off xylulose-5-P and welds it onto ribose-5-P. Requires thiamine pyrophosphate (TPP) — the same cofactor pyruvate dehydrogenase uses. Carbon check: 5 + 5 = 7 + 3.',
    },
    {
      n: 7,
      product: 'Fructose-6-P + Erythrose-4-P',
      short: 'F6P + E4P',
      enzyme: 'Transaldolase',
      emoji: '🔀',
      fact: 'Transfers a 3-carbon dihydroxyacetone unit via an active-site lysine that forms a Schiff base — the exact trick aldolase uses in glycolysis. No external cofactor. Carbon check: 7 + 3 = 6 + 4.',
    },
    {
      n: 8,
      product: 'Fructose-6-P + Glyceraldehyde-3-P',
      short: 'F6P + G3P',
      enzyme: 'Transketolase (TPP)',
      emoji: '🏁',
      fact: 'Second transketolase cut, moving another 2-carbon unit so both end products are ordinary glycolytic intermediates. Carbon check: 4 + 5 = 6 + 3. Net of the non-oxidative phase: 3 C5 sugars ⇌ 2 F6P + 1 G3P.',
    },
  ],
  regulators: [
    {
      name: 'G6PD (glucose-6-phosphate dehydrogenase)',
      role: 'The whole throttle. Rate-limiting, committed, and product-inhibited by NADPH. Spend NADPH → NADP⁺ rises → inhibition lifts → oxidative flux speeds up. Feedback written straight into the active site — no hormone needed.',
    },
    {
      name: 'NADP⁺ / NADPH ratio',
      role: 'The one number that sets flux. High NADPH (reduced pool full) = pathway idles; rising NADP⁺ (after biosynthesis or oxidative stress spends NADPH) = pathway accelerates.',
    },
    {
      name: 'Non-oxidative phase (reversible)',
      role: 'Not throttled — it’s a carbon exchange that runs whichever direction demand points, letting the cell decouple NADPH production from ribose need across four operating modes.',
    },
    {
      name: 'p53 (tumor suppressor)',
      role: 'Restrains the pathway by blocking G6PD from assembling into its active dimer. Lose p53 (the most common cancer mutation) → brake off → PPP flux climbs.',
    },
  ],
  scenarios: [
    {
      id: 'ppp-dividing',
      emoji: '🧫',
      title: 'A cell about to divide',
      scene: 'A crypt cell in your gut is about to replicate its entire genome. It needs ribose-5-phosphate — lots of it — to build the nucleotides for new DNA and RNA. Its NADPH tank is already comfortably full.',
      hormones: 'Growth signals ↑ · NADPH already high',
      flux: 'up',
      decisions: [
        {
          q: 'The cell needs RIBOSE but already has plenty of NADPH. What does it do?',
          choices: [
            'Run the non-oxidative phase BACKWARD to build ribose-5-P from glycolytic intermediates',
            'Run the oxidative phase harder to make more ribose',
          ],
          answer: 0,
          why: 'This is Mode 1, the "ribose builder." With NADPH already high, running the oxidative phase would overproduce NADPH the cell doesn’t need. Instead it runs the reversible non-oxidative reactions in reverse, assembling ribose-5-P from fructose-6-P and glyceraldehyde-3-P pulled from glycolysis — no NADPH made.',
        },
        {
          q: 'Why can the cell run the non-oxidative phase either direction, but not the oxidative phase?',
          choices: [
            'The non-oxidative steps are near-equilibrium and reversible; the oxidative phase lost a carbon as CO₂',
            'The oxidative phase spent ATP that can’t be recovered',
          ],
          answer: 0,
          why: 'The oxidative decarboxylation at 6-phosphogluconate dehydrogenase throws C1 away as CO₂, and you cannot re-add a lost CO₂ — that locks the phase one-way. The transketolase/transaldolase reactions sit near equilibrium and run freely in both directions. (The PPP spends no ATP at all.)',
        },
        {
          q: 'What is ribose-5-phosphate the direct precursor of?',
          choices: ['PRPP, which starts both purine and pyrimidine synthesis', 'Pyruvate, which enters the citric acid cycle'],
          answer: 0,
          why: 'Ribose-5-P is converted to PRPP (5-phosphoribosyl-1-pyrophosphate), the activated sugar that launches nucleotide synthesis — which is exactly why every dividing cell depends on this pathway.',
        },
      ],
      teach: 'DIVIDING CELL, NADPH ALREADY FULL = Mode 1, the "ribose builder." The reversible non-oxidative phase runs backward to make ribose-5-P from glycolytic F6P + G3P without touching the oxidative phase. Reversibility is the feature: it lets the cell get ribose without a NADPH surplus it can’t use.',
    },
    {
      id: 'ppp-fatsynth',
      emoji: '🧈',
      title: 'Liver making fat after a big meal',
      scene: 'You’re fed and insulin is high. Your liver is running fatty-acid synthesis full tilt — and fatty-acid synthase is a ravenous consumer of NADPH. The cell wants maximum reducing power and almost no ribose.',
      hormones: 'Insulin ↑ · NADPH demand ↑↑ · ribose demand low',
      flux: 'up',
      decisions: [
        {
          q: 'The cell needs lots of NADPH but little ribose. How does it run the PPP?',
          choices: [
            'Run the oxidative phase, then use the non-oxidative phase FORWARD to recycle ribose carbons back to G6P',
            'Run only the non-oxidative phase and skip NADPH production',
          ],
          answer: 0,
          why: 'This is Mode 3, the "NADPH baron." Run the oxidative phase for NADPH, then feed the ribulose-5-P through the non-oxidative phase forward to F6P/G3P, convert those back to glucose-6-phosphate, and loop it through the oxidative phase again. Many NADPH, almost no leftover ribose.',
        },
        {
          q: 'Fatty-acid synthesis and cholesterol synthesis need which cofactor as reducing power?',
          choices: ['NADPH', 'NADH'],
          answer: 0,
          why: 'Reductive biosynthesis runs on NADPH, not NADH. The cell keeps the NADP⁺/NADPH pool reduced (~1:10) precisely so donor electrons are always on tap for building molecules — the opposite poise from the catabolic NAD⁺/NADH pool (~1000:1 oxidized).',
        },
      ],
      teach: 'FAT SYNTHESIS = Mode 3, the "NADPH baron." Liver and adipose recycle ribose carbons back through the oxidative phase to squeeze out maximum NADPH for fatty-acid and cholesterol synthesis. The whole thing self-regulates: as NADPH is spent on lipids, NADP⁺ rises and lifts G6PD’s product inhibition.',
    },
    {
      id: 'ppp-oxstress',
      emoji: '🔥',
      title: 'Red cell hit by oxidative stress',
      scene: 'A red blood cell meets an oxidizing drug (a sulfa antibiotic). Reactive oxygen is building. The cell burns through reduced glutathione to neutralize peroxides, and now it must regenerate that glutathione — fast.',
      hormones: 'ROS ↑ · GSH being spent · NADP⁺ rising',
      flux: 'up',
      decisions: [
        {
          q: 'What does the rising oxidative load do to PPP flux?',
          choices: [
            'Speeds it up — spending NADPH raises NADP⁺, which lifts G6PD product inhibition',
            'Slows it down — the cell conserves glucose under stress',
          ],
          answer: 0,
          why: 'Glutathione reductase spends NADPH to regenerate GSH from GSSG. As NADPH is consumed, NADP⁺ climbs, releasing G6PD from product inhibition, so the oxidative phase accelerates to refill the NADPH tank. Demand pulls flux directly.',
        },
        {
          q: 'Why is a red blood cell uniquely dependent on the PPP for this?',
          choices: [
            'It has no mitochondria, so the PPP is its ONLY source of NADPH',
            'It has extra copies of G6PD to make NADPH faster',
          ],
          answer: 0,
          why: 'Red cells have no mitochondria (no other NADPH-generating routes) and no nucleus (can’t transcribe more enzyme). The PPP is their sole NADPH supply, which is why they collapse first when G6PD is weak.',
        },
        {
          q: 'What is NADPH’s ultimate job here?',
          choices: [
            'Regenerate reduced glutathione (GSH) via glutathione reductase',
            'Directly detoxify peroxides on its own',
          ],
          answer: 0,
          why: 'NADPH doesn’t quench ROS itself — it powers glutathione reductase to convert GSSG back to GSH, and GSH (via glutathione peroxidase) is what neutralizes the peroxides. Cut off NADPH and the antioxidant cycle stalls.',
        },
      ],
      teach: 'OXIDATIVE STRESS = PPP floors it. The chain is NADPH → GSH → ROS defense. Spending NADPH raises NADP⁺, which lifts G6PD inhibition and accelerates the oxidative phase. In a red cell — no mitochondria, no nucleus — the PPP is the only NADPH source, so this is the whole antioxidant economy.',
    },
    {
      id: 'ppp-g6pd',
      emoji: '🫘',
      title: 'G6PD-deficient patient eats fava beans',
      scene: 'A patient with G6PD deficiency eats a plate of fava beans. Within a day they develop sudden anemia — red cells are being destroyed. The blood smear shows Heinz bodies and bite cells.',
      hormones: 'Oxidative load ↑↑ · NADPH cannot be replenished',
      flux: 'off',
      decisions: [
        {
          q: 'With G6PD deficient, what happens to the antioxidant defense?',
          choices: [
            'It collapses: G6PD↓ → NADPH↓ → GSH↓ → ROS↑ → Heinz bodies → hemolysis',
            'It stays fine because glycolysis still makes plenty of ATP',
          ],
          answer: 0,
          why: 'The cascade is clean and one-directional. Weak G6PD means too little NADPH; glutathione can’t stay reduced; reactive oxygen accumulates; hemoglobin oxidizes and clumps into Heinz bodies; the spleen culls the damaged cells — a hemolytic crisis. Glycolytic ATP is irrelevant here because the failure is redox, not energy.',
        },
        {
          q: 'Why does the same allele persist at high frequency worldwide?',
          choices: [
            'It protects against malaria — G6PD-deficient red cells are hostile to Plasmodium falciparum',
            'It has no downside in the absence of triggers, so it drifts to high frequency',
          ],
          answer: 0,
          why: 'It’s a balanced polymorphism, the textbook companion to sickle-cell trait. The deficiency risks hemolysis but buys resistance to malaria, so it earned its keep where malaria was endemic. Map the allele and it mirrors the historical range of malaria.',
        },
      ],
      teach: 'G6PD DEFICIENCY = the oxidative phase can’t run, so no NADPH, no glutathione recycling, and oxidative triggers (fava beans, antimalarials, sulfa drugs, infection) shred red cells. Most common enzyme deficiency on Earth (~400 million people), X-linked, persists because it protects against malaria. Screen before prescribing oxidative-stress drugs.',
    },
  ],
  diseases: [
    {
      id: 'g6pd-deficiency',
      name: 'G6PD deficiency (favism)',
      emoji: '🫘',
      vignette:
        'A young man of Mediterranean descent develops sudden fatigue, dark urine, and jaundice a day after eating fava beans. Hemoglobin has dropped; the smear shows Heinz bodies and "bite cells." He recently started an antimalarial (primaquine). It is X-linked.',
      suspects: [
        'Glucose-6-phosphate dehydrogenase (G6PD)',
        'Pyruvate kinase',
        'Glutathione reductase',
        '6-Phosphogluconate dehydrogenase',
      ],
      answer: 0,
      accumulates: 'Oxidized hemoglobin (Heinz bodies) and reactive oxygen species',
      missing: 'NADPH → reduced glutathione (GSH)',
      teach:
        'G6PD runs the committed, rate-limiting first step of the oxidative phase — the red cell’s ONLY source of NADPH (no mitochondria). Weak G6PD → NADPH↓ → glutathione reductase can’t regenerate GSH → peroxides and oxidized hemoglobin accumulate as Heinz bodies → the spleen bites out the damage ("bite cells") and destroys the cells → hemolytic anemia. Triggers: fava beans, primaquine/sulfa drugs, and infection all pile on oxidative stress a weakened cell can’t handle.',
      pearl: 'Most common enzyme deficiency on Earth (~400M), X-linked. Cascade: G6PD↓ → NADPH↓ → GSH↓ → Heinz bodies + bite cells → hemolysis. Persists because it protects against malaria (balanced polymorphism, like sickle trait).',
    },
    {
      id: 'transketolase-thiamine',
      name: 'Thiamine deficiency → transketolase failure (Wernicke–Korsakoff)',
      emoji: '🍺',
      vignette:
        'A patient with chronic alcohol use presents with confusion, ophthalmoplegia (eye-movement paralysis), and ataxia. Red-cell transketolase activity is low but rises sharply when the assay is spiked with thiamine pyrophosphate — the classic diagnostic.',
      suspects: [
        'Transketolase (via thiamine pyrophosphate / vitamin B1)',
        'Glucose-6-phosphate dehydrogenase',
        'Transaldolase',
        'Phosphopentose isomerase',
      ],
      answer: 0,
      accumulates: 'Upstream pentose-phosphate intermediates (non-oxidative shuffle stalls)',
      missing: 'Functional transketolase activity (its TPP cofactor)',
      teach:
        'Transketolase needs thiamine pyrophosphate (TPP), made from vitamin B1. In thiamine deficiency — classically from alcoholism and poor diet — transketolase activity falls, stalling the non-oxidative carbon shuffle. Because transketolase is TPP-dependent and easy to assay in red cells, its activity (and the jump when TPP is added back) is used as a clinical readout of thiamine status. The neurologic syndrome (Wernicke encephalopathy → Korsakoff amnesia) reflects TPP’s broader role, since pyruvate dehydrogenase and α-ketoglutarate dehydrogenase also need TPP.',
      pearl: 'Transketolase is TPP-dependent — the red-cell transketolase assay (± added TPP) is the classic test of thiamine (B1) status. Same cofactor as pyruvate dehydrogenase.',
    },
    {
      id: 'p53-loss-tumor',
      name: 'p53 loss → runaway PPP flux (a mechanism, not a deficiency)',
      emoji: '🧬',
      vignette:
        'A tumor biopsy shows markedly increased pentose phosphate pathway flux and heavy NADPH and nucleotide production. Sequencing reveals a loss-of-function mutation in TP53 (p53), the single most common mutation in human cancer.',
      suspects: [
        'p53 (normally blocks G6PD from forming its active dimer)',
        'G6PD gain-of-function mutation',
        'Citrate overproduction activating G6PD',
        'Elevated NADPH/NADP⁺ ratio stimulating G6PD',
      ],
      answer: 0,
      accumulates: 'NADPH and ribose-5-phosphate (fueling proliferation)',
      missing: 'The p53 brake on G6PD dimerization',
      teach:
        'Wild-type p53 restrains the PPP by preventing G6PD from assembling into its active dimer. Lose p53 and the brake comes off, so G6PD activity and PPP flux climb. Dividing tumor cells want exactly this: they run glycolysis hard (the Warburg effect) AND the PPP hard, because proliferating means needing both nucleotides (ribose-5-P) and NADPH — for lipid/DNA synthesis and for surviving their own oxidative stress. Note the distractors invert the real biology: a higher NADPH/NADP⁺ ratio would INHIBIT G6PD (product inhibition), not stimulate it.',
      pearl: 'Exam line: p53 loss → more PPP flux (p53 normally blocks G6PD dimerization). Dividing/cancer cells run glycolysis AND the PPP hard for NADPH + ribose.',
    },
  ],
  quiz: [
    {
      tag: 'basics',
      stem: 'What are the two principal products of the pentose phosphate pathway, and how much net ATP does it generate?',
      choices: [
        'NADPH and ribose-5-phosphate; no net ATP',
        'NADPH and pyruvate; net +2 ATP',
        'FADH₂ and ribose-5-phosphate; no net ATP',
        'NADH and ribose-5-phosphate; net +2 ATP',
      ],
      answer: 0,
      rationale:
        'The PPP yields NADPH (reducing power for biosynthesis and antioxidant defense) and ribose-5-phosphate (the nucleotide backbone), and it makes no ATP — that is the whole point of taking this fork instead of glycolysis. The NADH option is wrong because the PPP uses the NADP⁺/NADPH couple, not NAD⁺/NADH; pyruvate is a glycolysis product; the PPP makes no FADH₂.',
    },
    {
      tag: 'energetics',
      stem: 'Why is the oxidative phase of the PPP irreversible while the non-oxidative phase is reversible?',
      choices: [
        'The second dehydrogenase releases a carbon as CO₂, which cannot be re-added',
        'The oxidative phase consumes two ATP that cannot be recovered',
        'The transketolase reaction physically cannot run backward',
        'G6PD is product-inhibited by NADP⁺',
      ],
      answer: 0,
      rationale:
        '6-phosphogluconate dehydrogenase performs an oxidative decarboxylation, releasing C1 as CO₂ (G6P C6 → ribulose-5-P C5). A lost CO₂ can’t be stuck back on, so the phase is one-way. The oxidative phase consumes no ATP; transketolase is a near-equilibrium reversible step; and G6PD is inhibited by NADPH (its product), not NADP⁺.',
    },
    {
      tag: 'regulation',
      stem: 'Which statement correctly describes the PRIMARY regulation of the PPP?',
      choices: [
        'G6PD is product-inhibited by NADPH, so rising NADP⁺ accelerates the pathway',
        'It is regulated by phosphofructokinase-1 in response to AMP',
        'Citrate allosterically activates the first enzyme of the pathway',
        'ATP allosterically inhibits transaldolase to slow carbon flux',
      ],
      answer: 0,
      rationale:
        'The throttle is NADP⁺ availability. Glucose-6-phosphate dehydrogenase is product-inhibited by NADPH; when NADPH is spent on biosynthesis or oxidative defense, NADP⁺ rises, the inhibition lifts, and oxidative flux speeds up — feedback written directly into the active site, no hormone needed. PFK-1/AMP, citrate, and ATP-on-transaldolase describe glycolytic controls or invented ones.',
    },
    {
      tag: 'energetics',
      stem: 'The non-oxidative phase converts three five-carbon sugars into which net set of products?',
      choices: [
        'Two fructose-6-phosphate and one glyceraldehyde-3-phosphate',
        'One sedoheptulose-7-phosphate and two erythrose-4-phosphate',
        'Two ribose-5-phosphate and one CO₂',
        'Three fructose-6-phosphate',
      ],
      answer: 0,
      rationale:
        'The net of the non-oxidative phase is 3 C5 ⇌ 2 fructose-6-P (C6) + 1 glyceraldehyde-3-P (C3). Carbon balance confirms it: 3 × 5 = 15 = 2 × 6 + 3. Both products are glycolytic intermediates. Sedoheptulose-7-P and erythrose-4-P are transient intermediates, not net products; the non-oxidative phase makes no CO₂ (that’s the oxidative phase); three F6P would be 18 carbons.',
    },
    {
      tag: 'basics',
      stem: 'A cell keeps its NAD⁺/NADH pool near 1000:1 (oxidized) and its NADP⁺/NADPH pool near 1:10 (reduced). What is the functional reason for maintaining two separate pools?',
      choices: [
        'To let catabolism (needing NAD⁺) and reductive biosynthesis (needing NADPH) run at the same time without one draining the other',
        'To double the cell’s total store of nicotinamide cofactor',
        'Because NADP⁺ cannot be reduced inside mitochondria',
        'Because NAD⁺ and NADPH have different absorption spectra at 340 nm',
      ],
      answer: 0,
      rationale:
        'Abundant oxidized NAD⁺ serves catabolic dehydrogenations; abundant reduced NADPH serves reductive biosynthesis and antioxidant defense. The single phosphate that distinguishes the couples lets enzymes tell them apart, so the high-capacity NAD⁺ pool can’t oxidize away the NADPH the cell built — no futile cycle. Total store, mitochondrial reduction, and absorbance are not the functional rationale.',
    },
    {
      tag: 'disease',
      stem: 'A red blood cell from a patient with G6PD deficiency is exposed to an oxidizing drug. Compared with a normal red cell, which change best explains why it undergoes hemolysis?',
      choices: [
        'It cannot regenerate reduced glutathione because NADPH production is impaired',
        'It cannot make ATP because the PPP is its only energy source',
        'It accumulates lactate because pyruvate kinase is inhibited',
        'It overproduces ribose-5-phosphate, which is toxic to the membrane',
      ],
      answer: 0,
      rationale:
        'Weak G6PD lowers NADPH, and glutathione reductase needs NADPH to regenerate reduced glutathione (GSH) from GSSG. Without GSH, peroxides and oxidized hemoglobin (Heinz bodies) accumulate and the spleen destroys the cell. The PPP makes no ATP (so it’s not the energy source); lactate/pyruvate kinase are glycolysis; and the deficient cell makes less downstream product, not a toxic excess.',
    },
    {
      tag: 'integration',
      stem: 'A rapidly dividing cell needs large amounts of ribose-5-phosphate for nucleotide synthesis but already has abundant NADPH. Which strategy meets this demand most efficiently?',
      choices: [
        'Run the non-oxidative phase in reverse, building ribose-5-P from fructose-6-P and glyceraldehyde-3-P',
        'Run the oxidative phase repeatedly to maximize NADPH and ribose together',
        'Convert ribose-5-P back to glucose-6-P to recycle carbon',
        'Inhibit transketolase to trap five-carbon sugars',
      ],
      answer: 0,
      rationale:
        'This is Mode 1, the "ribose builder": when NADPH is already high, the cell skips the NADPH-generating oxidative phase and runs the reversible non-oxidative reactions backward, assembling ribose-5-P from glycolytic intermediates. Running the oxidative phase would overproduce unneeded NADPH; recycling ribose to G6P is Mode 3 (for maximizing NADPH, the opposite need); inhibiting transketolase builds no net ribose.',
    },
    {
      tag: 'disease',
      stem: 'A tumor shows markedly increased PPP flux, and sequencing reveals loss-of-function of TP53 (p53). What is the most DIRECT mechanistic link between p53 loss and elevated PPP flux?',
      choices: [
        'p53 normally blocks G6PD from forming its active dimer, so losing p53 de-represses G6PD',
        'p53 loss raises the NADPH/NADP⁺ ratio, which stimulates G6PD',
        'p53 loss increases citrate, which activates G6PD',
        'p53 normally phosphorylates transketolase to keep it inactive',
      ],
      answer: 0,
      rationale:
        'Wild-type p53 restrains the pathway by preventing G6PD from assembling into its active dimer; losing p53 removes that brake and raises G6PD activity and PPP flux. A higher NADPH/NADP⁺ ratio would INHIBIT G6PD (product inhibition), not stimulate it; citrate-activating-G6PD is invented; p53 does not phosphorylate transketolase.',
    },
    {
      tag: 'basics',
      stem: 'Both transketolase reactions of the non-oxidative phase require which cofactor, and how does that create a clinical link?',
      choices: [
        'Thiamine pyrophosphate (TPP) from vitamin B1 — so B1 deficiency lowers transketolase activity',
        'Biotin from vitamin B7 — so B7 deficiency lowers transketolase activity',
        'Pyridoxal phosphate from vitamin B6 — so B6 deficiency lowers transketolase activity',
        'Flavin (FAD) from riboflavin — so B2 deficiency lowers transketolase activity',
      ],
      answer: 0,
      rationale:
        'Transketolase is thiamine-pyrophosphate (TPP)-dependent — the same cofactor pyruvate dehydrogenase uses. In thiamine (vitamin B1) deficiency, classically from alcoholism, transketolase activity falls, and the red-cell transketolase assay (with and without added TPP) is a standard test of thiamine status. Biotin, PLP, and FAD serve other enzymes.',
    },
    {
      tag: 'integration',
      stem: 'Compared with glycolysis, glucose-6-phosphate that enters the oxidative PPP loses which carbon as CO₂, a fact exploited to measure how much glucose runs each branch?',
      choices: [
        'C1 — released as CO₂ by 6-phosphogluconate dehydrogenase, whereas glycolysis retains it',
        'C6 — released as CO₂ by G6PD, whereas glycolysis retains it',
        'C3 — released as CO₂ by transketolase, whereas glycolysis retains it',
        'No carbon is lost; the PPP conserves all six carbons of glucose',
      ],
      answer: 0,
      rationale:
        'The oxidative phase removes C1 of glucose as CO₂ at 6-phosphogluconate dehydrogenase, while glycolysis keeps that carbon. Feeding cells glucose labeled at C1 versus C6 (¹³C or ¹⁴C) and following where the label appears in released CO₂ reveals what fraction of glucose ran the PPP versus glycolysis — how the relative flux was first measured in different tissues.',
    },
  ],
  funFact:
    'The PPP makes zero ATP, yet you can’t live without it. Its oxidative phase is one of the few reactions that release CO₂ with no O₂ consumed at all — the electrons from that decarboxylation go onto NADP⁺, not down to oxygen. The same quiet pathway your red cells lean on for antioxidant NADPH is what keeps every dividing cell supplied with the ribose for its next genome.',
};
