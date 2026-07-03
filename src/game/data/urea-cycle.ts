import type { Pathway } from '../types';

/* =============================================================================
   UREA CYCLE — nitrogen disposal (hand-authored, cross-checked against
   src/content/lessons/protein-turnover-amino-acid-catabolism/lesson.mdx, Act 2).
   Two waste nitrogens + one bicarbonate → one urea. Five enzymes across two
   compartments: CPS-I and OTC in the mitochondrion, then ASS, ASL, and arginase
   in the cytosol. Ornithine is Krebs's WHEEL — consumed at step 2, regenerated
   at step 5 — so it turns catalytically and never runs out. `doubleAfter: 0`
   because nothing splits; one lap of the wheel makes exactly one urea.
   Costs four high-energy phosphate bonds per urea (2 ATP at CPS-I, and ATP → AMP
   + PPᵢ at ASS = 2 more). Only the liver runs the full cycle.
   ============================================================================ */

export const ureaCycle: Pathway = {
  id: 'urea-cycle',
  name: 'Urea Cycle',
  emoji: '🚽',
  tagline: 'Ammonia is poison. Package two toxic nitrogens into one flushable molecule.',
  blurb:
    'Free ammonia is neurotoxic, so the liver locks two waste nitrogens plus a bicarbonate into one molecule of urea. Five steps, two compartments, four high-energy bonds spent — and ornithine turns like a wheel, consumed early and handed back at the end.',
  difficulty: 3,
  location: 'Liver (mitochondria → cytosol)',
  netYield: 'Costs 4 high-energy phosphate bonds to package 2 nitrogens as 1 urea',
  start: 'NH₄⁺ + HCO₃⁻',
  startShort: 'NH₄⁺ + HCO₃⁻',
  startEmoji: '☠️',
  doubleAfter: 0, // a cycle, not a split — one lap = one urea, no yields double
  lessonSlug: 'protein-turnover-amino-acid-catabolism',
  steps: [
    {
      n: 1,
      product: 'Carbamoyl phosphate',
      short: 'Carbamoyl-P',
      enzyme: 'Carbamoyl phosphate synthetase I (CPS-I)',
      tokens: { atp: -2 },
      irreversible: true,
      committed: true,
      emoji: '🚦',
      fact: 'THE committed, rate-limiting step. Mitochondrial. Condenses free NH₄⁺ + HCO₃⁻ into carbamoyl phosphate at the cost of 2 ATP — the first two of the four high-energy bonds per urea. Fires ONLY when N-acetylglutamate (NAG) is present.',
    },
    {
      n: 2,
      product: 'Citrulline',
      short: 'Citrulline',
      enzyme: 'Ornithine transcarbamylase (OTC)',
      emoji: '🎡',
      fact: 'Mitochondrial. Hands the carbamoyl group to ornithine, building citrulline (which is then exported to the cytosol). Ornithine is Krebs’s catalytic WHEEL — consumed here, regenerated at the very end. OTC deficiency is the most common urea cycle disorder (X-linked).',
    },
    {
      n: 3,
      product: 'Argininosuccinate',
      short: 'Arg-succinate',
      enzyme: 'Argininosuccinate synthetase (ASS)',
      tokens: { atp: -2 },
      irreversible: true,
      emoji: '🔗',
      fact: 'Cytosolic. Aspartate donates the SECOND nitrogen of urea. ATP is cleaved to AMP + PPᵢ, and hydrolysis of the pyrophosphate makes this one step cost two high-energy bonds — completing the four per urea.',
    },
    {
      n: 4,
      product: 'Arginine + fumarate',
      short: 'Arg + fumarate',
      enzyme: 'Argininosuccinate lyase (ASL)',
      emoji: '⚙️',
      fact: 'Cytosolic. Cleaves the molecule into arginine and fumarate. The fumarate is the gear that meshes this cycle with the TCA cycle (the "Krebs bicycle"): fumarate → malate → OAA links nitrogen disposal to gluconeogenesis.',
    },
    {
      n: 5,
      product: 'Urea + ornithine',
      short: 'Urea + Orn',
      enzyme: 'Arginase',
      irreversible: true,
      emoji: '🏁',
      fact: 'Cytosolic finish line. Hydrolyzes arginine to release urea — the final nitrogen waste, headed for the kidney — and regenerates ornithine, which re-enters the mitochondrion to turn the wheel again. Only the liver expresses the full set.',
    },
  ],
  regulators: [
    {
      name: 'N-acetylglutamate (NAG)',
      role: 'The master ON switch. Made by NAG synthase from acetyl-CoA + glutamate and amplified by arginine; it allosterically activates CPS-I. No NAG → the whole cycle stalls at the committed step. A feedforward signal that says "nitrogen is arriving."',
    },
    {
      name: 'CPS-I',
      role: 'The rate-limiting, committed enzyme (step 1). Its rate is set entirely by NAG availability — that is where flux through the whole cycle is controlled.',
    },
    {
      name: 'Substrate supply (glutamate / aspartate / ornithine)',
      role: 'Short-term throttle. More amino-acid catabolism → more glutamate (raises NAG) and more aspartate (feeds the 2nd nitrogen at ASS), so a protein load speeds the cycle by mass action.',
    },
    {
      name: 'Long-term enzyme induction',
      role: 'Slow control. A sustained high-protein diet OR starvation (catabolizing body protein) induces higher levels of all five enzymes over days; a low-protein diet lowers them.',
    },
  ],
  scenarios: [
    {
      id: 'urea-highprotein',
      emoji: '🥩',
      title: 'You just crushed a giant steak',
      scene:
        'A flood of dietary amino acids hits the liver. Their carbon skeletons are useful fuel, but the amino nitrogen is a liability — free ammonia is toxic and has to be caged fast.',
      hormones: 'High amino-acid load · NAG rising',
      flux: 'up',
      decisions: [
        {
          q: 'Which way should the urea cycle run after a big protein meal?',
          choices: ['Ramp UP — dispose of the incoming nitrogen', 'Shut DOWN — conserve nitrogen for building'],
          answer: 0,
          why: 'A protein load delivers far more nitrogen than the body can reuse. The excess amino groups must be caged as urea, so ureagenesis ramps up.',
        },
        {
          q: 'What allosterically activates CPS-I to open the gate?',
          choices: [
            'N-acetylglutamate (NAG), which rises with glutamate + arginine',
            'Citrate spilling out of the TCA cycle',
            'A rising AMP:ATP ratio',
            'Fructose-2,6-bisphosphate',
          ],
          answer: 0,
          why: 'NAG (from acetyl-CoA + glutamate, amplified by arginine) is the dedicated activator of CPS-I. More amino-acid catabolism → more glutamate → more NAG → the committed step opens. Citrate, AMP, and F-2,6-BP belong to other pathways.',
        },
        {
          q: 'Where does the SECOND nitrogen of urea come from?',
          choices: [
            'Aspartate, at the argininosuccinate synthetase step',
            'A second molecule of free ammonia at CPS-I',
            'Glutamine hydrolysis inside the mitochondrion',
            'The bicarbonate that started the cycle',
          ],
          answer: 0,
          why: 'The first nitrogen enters as free NH₄⁺ at CPS-I; the second is donated by aspartate at ASS (step 3). Bicarbonate supplies the carbon and oxygen, not a nitrogen.',
        },
      ],
      teach:
        'HIGH PROTEIN = lots of amino nitrogen to dump. Glutamate rises → NAG rises → CPS-I opens → the cycle floods. Nitrogen #1 comes in as ammonia (CPS-I), nitrogen #2 from aspartate (ASS), and over days the liver even induces more of all five enzymes.',
    },
    {
      id: 'urea-fasting',
      emoji: '😴',
      title: 'Day 3 of a fast — burning your own muscle',
      scene:
        'No food is coming in. To keep the brain supplied, muscle protein is being catabolized for gluconeogenesis. That releases a steady stream of amino-acid nitrogen that still has to go somewhere.',
      hormones: 'Glucagon ↑ · muscle proteolysis ↑',
      flux: 'up',
      decisions: [
        {
          q: 'What happens to urea-cycle flux during a prolonged fast?',
          choices: [
            'It stays UP — muscle breakdown still floods the liver with nitrogen',
            'It shuts OFF — no dietary protein means no nitrogen to dispose of',
          ],
          answer: 0,
          why: 'Fasting is a trap for the intuition: even with NO food, the body is catabolizing its OWN protein for glucose, so amino-acid nitrogen keeps arriving and must still be caged as urea. Starvation actually induces the urea-cycle enzymes.',
        },
        {
          q: 'The carbon skeleton of muscle alanine, once its nitrogen is stripped in the liver, is used for…',
          choices: [
            'Gluconeogenesis — pyruvate → glucose for the brain',
            'Immediate re-synthesis into new muscle protein',
            'Storage as hepatic glycogen only',
            'Excretion alongside the urea',
          ],
          answer: 0,
          why: 'In the glucose-alanine cycle, muscle ships nitrogen as alanine; the liver transaminates it back to pyruvate (→ glucose for the brain) and routes the nitrogen into urea. Carbon becomes glucose, nitrogen becomes urea.',
        },
      ],
      teach:
        'FASTING is the counterintuitive one: the urea cycle stays UP because you are disposing of nitrogen from your OWN catabolized muscle. Alanine and glutamine ferry that nitrogen to the liver, which caged it as urea while turning the carbon into glucose — your brain quite literally runs on your biceps.',
    },
    {
      id: 'urea-fedcarb',
      emoji: '🍚',
      title: 'A big bowl of white rice, no protein',
      scene:
        'A pure-carbohydrate meal. Insulin is up, glucose is plentiful, and there is very little incoming amino-acid nitrogen to deal with.',
      hormones: 'Insulin ↑ · low amino-acid load',
      flux: 'down',
      decisions: [
        {
          q: 'Relative to a steak dinner, urea-cycle flux after a carb-only meal is…',
          choices: [
            'Lower — little nitrogen is arriving to dispose of',
            'Higher — insulin directly drives ureagenesis',
            'Identical — the cycle runs at a fixed constitutive rate',
            'Zero — the enzymes are switched off entirely',
          ],
          answer: 0,
          why: 'Flux tracks the nitrogen load. A carb meal delivers little amino nitrogen, so less glutamate, less NAG, and a quieter CPS-I. The cycle idles rather than switching off — a baseline of protein turnover always needs disposal.',
        },
      ],
      teach:
        'FED-CARB = relatively DOWN. With little incoming nitrogen, glutamate and NAG stay low and CPS-I idles. The cycle never fully stops — everyday protein turnover always generates some nitrogen — but it runs far below the post-steak surge.',
    },
    {
      id: 'urea-liverfailure',
      emoji: '🫀',
      title: 'Acute liver failure',
      scene:
        'A patient with fulminant hepatitis becomes confused and drowsy, progressing toward coma. Blood ammonia is markedly elevated. The urea cycle machinery is failing.',
      hormones: 'n/a — organ-level failure',
      flux: 'down',
      decisions: [
        {
          q: 'Why does blood ammonia rise when the liver fails?',
          choices: [
            'Only the liver runs the full urea cycle, so nitrogen can no longer be caged as urea',
            'The kidney normally makes urea and takes over when the liver fails',
            'Muscle stops making ammonia, so it backs up in blood',
            'Failed hepatocytes actively pump ammonia into the blood',
          ],
          answer: 0,
          why: 'The complete urea cycle exists essentially only in the liver. Lose hepatic function and there is no other organ to convert ammonia to urea, so ammonia accumulates in the blood.',
        },
        {
          q: 'Why is the rising ammonia dangerous to the brain?',
          choices: [
            'Astrocytes trap it as glutamine and swell → cerebral edema and encephalopathy',
            'Ammonia is inert but blocks glucose uptake by neurons',
            'Ammonia is converted to urea inside neurons, poisoning them',
            'It acidifies the blood, and low pH directly kills neurons',
          ],
          answer: 0,
          why: 'Astrocytes detoxify ammonia by making glutamine (glutamate + NH₃). The osmotic load swells the astrocytes, causing cerebral edema — the basis of hepatic encephalopathy. It also drains α-ketoglutarate/glutamate pools.',
        },
      ],
      teach:
        'LIVER FAILURE = the cycle FAILS. Because only the liver makes urea, hepatic failure lets ammonia climb. Astrocytes mop it up as glutamine and swell → cerebral edema and encephalopathy. Emergency management mirrors the inborn errors: restrict protein, give nitrogen scavengers, and dialyze in a crisis.',
    },
  ],
  diseases: [
    {
      id: 'otc-deficiency',
      name: 'Ornithine transcarbamylase (OTC) deficiency',
      emoji: '🧬',
      vignette:
        'A previously well male infant becomes lethargic and vomits within days of birth, then develops seizures. Labs: markedly HIGH plasma ammonia, LOW citrulline, and HIGH urinary orotic acid. Family history suggests an X-linked pattern.',
      suspects: [
        'Ornithine transcarbamylase (OTC)',
        'Carbamoyl phosphate synthetase I (CPS-I)',
        'Argininosuccinate lyase (ASL)',
        'Arginase',
      ],
      answer: 0,
      accumulates: 'Ammonia and carbamoyl phosphate — the latter spills into pyrimidine synthesis → orotic acid',
      missing: 'Citrulline (and everything downstream of it)',
      teach:
        'OTC condenses carbamoyl phosphate with ornithine to make citrulline. Lose OTC and citrulline can’t be made (LOW citrulline), while the carbamoyl phosphate piling up behind the block overflows into cytosolic pyrimidine synthesis → HIGH urinary orotic acid. It is the MOST common urea cycle disorder and the only X-linked one. Contrast CPS-I deficiency: also low citrulline, but NO orotic aciduria, because carbamoyl phosphate is never made in excess.',
      pearl: 'Hyperammonemia + LOW citrulline + HIGH orotic acid + X-linked = OTC deficiency (most common UCD).',
    },
    {
      id: 'cps1-deficiency',
      name: 'Carbamoyl phosphate synthetase I (CPS-I) deficiency',
      emoji: '🚦',
      vignette:
        'A neonate presents with severe hyperammonemia, lethargy, and poor feeding. Labs: LOW citrulline — but urinary orotic acid is NORMAL/LOW, not elevated. Inheritance is autosomal recessive.',
      suspects: [
        'Carbamoyl phosphate synthetase I (CPS-I)',
        'Ornithine transcarbamylase (OTC)',
        'Argininosuccinate synthetase (ASS)',
        'N-acetylglutamate synthase (NAGS)',
      ],
      answer: 0,
      accumulates: 'Ammonia (nitrogen can’t even enter the cycle)',
      missing: 'Carbamoyl phosphate → and therefore citrulline and everything downstream',
      teach:
        'CPS-I is the entry point: it fixes ammonia into carbamoyl phosphate. Lose it and nitrogen can’t enter the cycle at all → severe hyperammonemia and LOW citrulline. The discriminator from OTC deficiency is orotic acid: because carbamoyl phosphate is NOT made in excess (the enzyme that makes it is the one that’s broken), it can’t spill into pyrimidine synthesis, so orotic acid is NOT elevated. NAGS deficiency looks biochemically identical to CPS-I deficiency (no NAG → CPS-I can’t fire).',
      pearl: 'Hyperammonemia + low citrulline + NORMAL orotic acid = CPS-I (or NAGS) deficiency, not OTC.',
    },
    {
      id: 'asl-deficiency',
      name: 'Argininosuccinate lyase (ASL) deficiency · argininosuccinic aciduria',
      emoji: '⚙️',
      vignette:
        'An infant has hyperammonemia and failure to thrive. A metabolite not normally detectable — argininosuccinate — is markedly elevated in blood and urine. Citrulline is moderately elevated as well.',
      suspects: [
        'Argininosuccinate lyase (ASL)',
        'Arginase',
        'Ornithine transcarbamylase (OTC)',
        'Carbamoyl phosphate synthetase I (CPS-I)',
      ],
      answer: 0,
      accumulates: 'Argininosuccinate (and, upstream, citrulline)',
      missing: 'Arginine and fumarate (so the TCA link is lost too)',
      teach:
        'ASL cleaves argininosuccinate into arginine + fumarate. Block it and argininosuccinate — a compound with no other fate — accumulates and spills into urine (argininosuccinic aciduria), the diagnostic fingerprint. Citrulline backs up too. Losing the fumarate output also weakens the "Krebs bicycle" link to the TCA cycle. Management: give arginine (now essential) plus nitrogen scavengers.',
      pearl: 'Argininosuccinate in the urine = ASL deficiency — the metabolite names the enzyme.',
    },
  ],
  quiz: [
    {
      tag: 'basics',
      stem: 'The urea cycle spans two cellular compartments. Which two enzymes run inside the mitochondrion?',
      choices: [
        'Carbamoyl phosphate synthetase I (CPS-I) and ornithine transcarbamylase (OTC)',
        'Argininosuccinate synthetase (ASS) and argininosuccinate lyase (ASL)',
        'Ornithine transcarbamylase (OTC) and arginase',
        'CPS-I and arginase',
      ],
      answer: 0,
      rationale:
        'The first two steps — CPS-I (fixing ammonia into carbamoyl phosphate) and OTC (making citrulline) — occur in the mitochondrial matrix. Citrulline is then exported to the cytosol, where ASS, ASL, and arginase complete the cycle. Compartmentalization is regulation.',
    },
    {
      tag: 'energetics',
      stem: 'How many high-energy phosphate bonds are consumed to synthesize one molecule of urea, and where?',
      choices: [
        'Four: 2 ATP at CPS-I, plus ATP → AMP + PPᵢ (= 2 bonds) at argininosuccinate synthetase',
        'Two: only the 2 ATP spent at CPS-I',
        'Three: 2 ATP at CPS-I plus 1 ATP → ADP at OTC',
        'Six: 2 ATP at each of CPS-I, ASS, and arginase',
      ],
      answer: 0,
      rationale:
        'CPS-I spends 2 ATP (→ 2 ADP + 2 Pᵢ). Argininosuccinate synthetase spends one ATP but cleaves it to AMP + PPᵢ, and hydrolysis of the pyrophosphate makes that step cost the equivalent of two high-energy bonds. 2 + 2 = 4 per urea. OTC and arginase spend no ATP.',
    },
    {
      tag: 'regulation',
      stem: 'Which molecule is the primary allosteric activator of the rate-limiting urea-cycle enzyme, and what does its presence signal?',
      choices: [
        'N-acetylglutamate (NAG) activates CPS-I; it signals that amino-acid nitrogen is arriving',
        'Fructose-2,6-bisphosphate activates CPS-I; it signals the fed state',
        'Citrate activates OTC; it signals a full TCA cycle',
        'AMP activates arginase; it signals low energy charge',
      ],
      answer: 0,
      rationale:
        'CPS-I is the committed, rate-limiting step and it is essentially inactive without N-acetylglutamate (NAG). NAG is made from acetyl-CoA + glutamate (and amplified by arginine), so rising glutamate from amino-acid catabolism is a feedforward "nitrogen is coming" signal. F-2,6-BP and citrate belong to carbohydrate metabolism.',
    },
    {
      tag: 'integration',
      stem: 'A nitrogen tracer placed on the amino group of muscle alanine later appears in urea. Which sequence describes its journey?',
      choices: [
        'Alanine → liver; transaminated to pyruvate, nitrogen → glutamate → NH₄⁺ (glutamate dehydrogenase) → fixed by CPS-I → urea',
        'Alanine is converted directly to urea within the muscle, then exported',
        'Alanine → kidney, where the full urea cycle detoxifies it to urea',
        'Alanine donates its nitrogen to fumarate in the liver, which is excreted unchanged',
      ],
      answer: 0,
      rationale:
        'In the glucose-alanine cycle, muscle ships nitrogen as alanine. Hepatic ALT converts alanine → pyruvate (feeding gluconeogenesis) and moves the amino group to α-ketoglutarate → glutamate. Glutamate dehydrogenase releases NH₄⁺, which CPS-I fixes to start the urea cycle. Muscle lacks the urea cycle; only the liver makes urea.',
    },
    {
      tag: 'disease',
      stem: 'A male neonate has hyperammonemia, LOW plasma citrulline, and HIGH urinary orotic acid. Which enzyme is deficient?',
      choices: [
        'Ornithine transcarbamylase (OTC)',
        'Carbamoyl phosphate synthetase I (CPS-I)',
        'Argininosuccinate synthetase (ASS)',
        'Arginase',
      ],
      answer: 0,
      rationale:
        'OTC makes citrulline, so its loss lowers citrulline; the carbamoyl phosphate that piles up behind the block overflows into cytosolic pyrimidine synthesis, raising orotic acid. CPS-I deficiency also lowers citrulline but does NOT raise orotic acid (carbamoyl phosphate isn’t made in excess). ASS deficiency (citrullinemia) RAISES citrulline. This X-linked triad = OTC deficiency, the most common UCD.',
    },
    {
      tag: 'disease',
      stem: 'Two neonates both show hyperammonemia with low citrulline. Infant A has high urinary orotic acid; infant B has normal orotic acid. What single fact best explains the difference?',
      choices: [
        'In OTC deficiency (A), excess carbamoyl phosphate spills into pyrimidine synthesis; in CPS-I deficiency (B), carbamoyl phosphate is never made in excess',
        'Infant A has a defect in pyrimidine synthesis unrelated to the urea cycle',
        'Infant B has a milder OTC mutation, so less orotic acid is produced',
        'Orotic acid is only elevated when arginase is also deficient',
      ],
      answer: 0,
      rationale:
        'Orotic acid is the discriminator between the two proximal urea-cycle defects. OTC deficiency (A) blocks the step AFTER carbamoyl phosphate, so carbamoyl phosphate accumulates and overflows into cytosolic pyrimidine synthesis → orotic acid. CPS-I deficiency (B, like NAGS deficiency) breaks the enzyme that MAKES carbamoyl phosphate, so none accumulates and orotic acid stays normal.',
    },
    {
      tag: 'integration',
      stem: 'Argininosuccinate lyase produces arginine and fumarate. What is the significance of the fumarate?',
      choices: [
        'It links the urea cycle to the TCA cycle (the "Krebs bicycle"): fumarate → malate → OAA feeds gluconeogenesis',
        'It is the direct precursor of urea in the final step',
        'It regenerates ornithine so the cycle can turn again',
        'It is the second nitrogen donor for the next round',
      ],
      answer: 0,
      rationale:
        'Fumarate is the gear meshing nitrogen disposal with carbon metabolism. It enters the TCA cycle and is converted fumarate → malate → oxaloacetate, coupling ureagenesis to gluconeogenesis and to regeneration of aspartate (the second nitrogen donor). Urea itself comes from arginase (arginine hydrolysis), and ornithine — not fumarate — is the regenerated carrier.',
    },
    {
      tag: 'basics',
      stem: 'Hans Krebs titrated ornithine to lower and lower amounts, yet urea output held steady — one ornithine drove ~20 ureas. What does this reveal about ornithine’s role?',
      choices: [
        'Ornithine is a catalyst (a "wheel") — consumed at OTC (step 2) and regenerated at arginase (step 5)',
        'Ornithine is the direct nitrogen source for urea and is consumed stoichiometrically',
        'Ornithine is an allosteric inhibitor that slows the cycle when abundant',
        'Ornithine is the final excreted waste product of the cycle',
      ],
      answer: 0,
      rationale:
        'A reactant fed in at one step and returned unspent at another is not a fuel but a wheel. Ornithine is consumed by OTC (step 2) to make citrulline and regenerated by arginase (step 5) alongside urea, so a small pool turns over many times. This catalytic-cycle insight is exactly how Krebs recognized the first metabolic cycle.',
    },
    {
      tag: 'regulation',
      stem: 'A patient on a sustained high-protein diet gradually develops greater urea-synthesizing capacity than a patient on a low-protein diet. What mechanism best accounts for this LONG-TERM difference?',
      choices: [
        'Induction (increased expression) of the urea-cycle enzymes over days',
        'A permanent allosteric activation of CPS-I by dietary protein',
        'Covalent phosphorylation of arginase by insulin',
        'Irreversible inhibition of the enzymes on a low-protein diet',
      ],
      answer: 0,
      rationale:
        'Beyond the fast allosteric control by NAG, sustained changes in nitrogen load adjust the AMOUNT of enzyme: a chronic high-protein diet (and, notably, starvation, which catabolizes body protein) induces higher levels of all five urea-cycle enzymes over days, while a low-protein diet lowers them. This is transcriptional/translational induction, not allosteric or covalent modulation.',
    },
    {
      tag: 'disease',
      stem: 'Why does severe hyperammonemia cause cerebral edema and encephalopathy?',
      choices: [
        'Astrocytes detoxify ammonia by making glutamine; the osmotic load swells them, and α-ketoglutarate/glutamate pools are drained',
        'Ammonia is directly converted to urea inside neurons, and the urea is toxic',
        'Ammonia lowers blood pH so severely that neurons die from acidosis',
        'Ammonia blocks the blood-brain barrier, starving neurons of glucose',
      ],
      answer: 0,
      rationale:
        'Astrocytes trap ammonia by combining it with glutamate to form glutamine. The accumulating glutamine draws water in osmotically, swelling astrocytes → cerebral edema. Consuming glutamate/α-ketoglutarate also disrupts neurotransmitter and TCA pools. This is the basis of hepatic encephalopathy; treatment restricts protein and gives nitrogen scavengers (benzoate/phenylacetate) plus arginine.',
    },
  ],
  funFact:
    'Ornithine is the ultimate reusable tool: Krebs found that one molecule can drive about twenty ureas because it is handed back intact at the end of every lap. The urea cycle was the first metabolic cycle ever discovered (1932) — the template for recognizing that biology runs in loops, not straight lines.',
};
