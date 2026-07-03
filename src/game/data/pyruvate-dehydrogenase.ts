import type { Pathway } from '../types';

/* =============================================================================
   PYRUVATE DEHYDROGENASE COMPLEX — "the bridge" (hand-authored, cross-checked
   against src/content/lessons/pyruvate-dehydrogenase/lesson.mdx). One physical
   ~10-MDa machine, three enzymes (E1/E2/E3), five coenzymes (TPP, lipoamide,
   CoA, FAD, NAD⁺). Net per pyruvate: 1 acetyl-CoA, 1 CO₂, 1 NADH — irreversible.
   We model the catalytic components as ordered steps and the five coenzymes as
   facts. Tokens land the CO₂ at E1 (decarboxylation) and the NADH at E3 (the
   ONLY NADH-producing step). doubleAfter: 0 — this small pathway never doubles;
   the "×2 per glucose" note is carried in netYield and the quiz. The exam trap
   (NADH is made only at E3, NOT at the E1 oxidation) is flagged everywhere.
   ============================================================================ */

export const pyruvateDehydrogenase: Pathway = {
  id: 'pyruvate-dehydrogenase',
  name: 'Pyruvate Dehydrogenase (the bridge)',
  emoji: '🌉',
  tagline: 'A one-way gate: pyruvate walks in, acetyl-CoA walks out, and there is no walking back.',
  blurb:
    'The irreversible bridge from glycolysis to the citric acid cycle. One giant complex — three enzymes, five coenzymes, a 14-Å swinging arm — strips a carbon off pyruvate as CO₂ and banks one NADH, handing the surviving two carbons to CoA as acetyl-CoA. Cross the gate and you can never make glucose from it again.',
  difficulty: 2,
  location: 'Mitochondrial matrix',
  netYield: 'Per pyruvate: 1 NADH, 1 CO₂, 1 acetyl-CoA (×2 per glucose)',
  start: 'Pyruvate',
  startShort: 'Pyruvate',
  startEmoji: '🍇',
  doubleAfter: 0, // small linear pathway — nothing doubles within it (2 pyruvate/glucose is noted in netYield)
  lessonSlug: 'pyruvate-dehydrogenase',
  steps: [
    {
      n: 1,
      product: 'Pyruvate (mitochondrial matrix)',
      short: 'Pyruvate → matrix',
      enzyme: 'Mitochondrial pyruvate carrier (MPC)',
      emoji: '🚪',
      fact: 'The geographic move. Pyruvate made by glycolysis in the cytosol is carried across the inner mitochondrial membrane into the matrix, where the complex waits. Nothing is consumed or produced yet — but PDC lives in the matrix, not the cytosol.',
    },
    {
      n: 2,
      product: 'Hydroxyethyl-TPP + CO₂',
      short: 'HE-TPP + CO₂',
      enzyme: 'E1 · pyruvate dehydrogenase (TPP, Mg²⁺)',
      tokens: { co2: 1 },
      irreversible: true,
      committed: true,
      emoji: '💨',
      fact: 'THE irreversible, committed step. The C2 carbanion (ylide) of thiamine pyrophosphate attacks pyruvate’s carbonyl and the carboxyl carbon leaves as CO₂ — a large negative ΔG, the carbon gone as gas, and animals have no enzyme to put it back. E1 is also the principal control point (PDK/PDP act here).',
    },
    {
      n: 3,
      product: 'Acetyl-lipoamide',
      short: 'Acetyl-lipoamide',
      enzyme: 'E1 · pyruvate dehydrogenase',
      emoji: '⚠️',
      fact: 'THE EXAM TRAP. Still on E1: the hydroxyethyl unit is oxidized to an acetyl group and handed to lipoamide, reducing its S–S disulfide to a dithiol. The electrons now sit on the lipoamide arm — NOT on NAD⁺ — so no NADH is made here, even though this looks like "the oxidation."',
    },
    {
      n: 4,
      product: 'Acetyl-CoA + dihydrolipoamide',
      short: 'Acetyl-CoA',
      enzyme: 'E2 · dihydrolipoyl transacetylase',
      emoji: '🎁',
      fact: 'The payoff. The ~14-Å swinging lipoamide arm carries the acetyl group to the E2 core, which transfers it to coenzyme A — forming the high-energy thioester acetyl-CoA (~−31 kJ/mol, near ATP). Acetyl-CoA is released; the arm is left reduced and must be reset.',
    },
    {
      n: 5,
      product: 'Lipoamide (S–S) + FADH₂ (bound)',
      short: 'Reset arm',
      enzyme: 'E3 · dihydrolipoamide dehydrogenase (FAD)',
      emoji: '🔁',
      fact: 'E3 reoxidizes the dithiol back to the lipoamide disulfide, resetting the arm. The electrons pass to E3’s tightly bound FAD, making FADH₂ transiently — but this FADH₂ never leaves the enzyme. It is an internal relay, which is why PDC’s net carrier is NADH, not FADH₂.',
    },
    {
      n: 6,
      product: 'NADH + H⁺ (FAD regenerated)',
      short: 'NADH',
      enzyme: 'E3 · dihydrolipoamide dehydrogenase (NAD⁺)',
      tokens: { nadh: 1 },
      emoji: '🔋',
      fact: 'The ONLY NADH-producing step in the whole complex. Electrons move from bound FADH₂ to NAD⁺, making NADH and regenerating FAD. No molecular O₂ is used here — PDC needs aerobic conditions only because the electron-transport chain must regenerate NAD⁺ downstream.',
    },
  ],
  regulators: [
    { name: 'E1 (pyruvate dehydrogenase)', role: 'The gate itself and the master control point. Allosterically inhibited by its own products (ATP, NADH, acetyl-CoA) and activated by ADP and pyruvate.' },
    { name: 'PDH kinase (PDK)', role: 'The OFF switch. Phosphorylates a serine on E1 → PDC off. Itself stimulated by the "plenty" signals: high ATP/ADP, NADH/NAD⁺, and acetyl-CoA/CoA ratios. Note: here phosphorylation INACTIVATES.' },
    { name: 'PDH phosphatase (PDP)', role: 'The ON switch. Removes the phosphate from E1 → PDC on. Activated by Ca²⁺ (and Mg²⁺); the fed-state insulin signal also drives PDC toward the active, dephosphorylated form.' },
    { name: 'Ca²⁺ (muscle axis)', role: 'The excitation–fuel link. The same Ca²⁺ that triggers muscle contraction activates PDP → E1 dephosphorylated → acetyl-CoA surges exactly when ATP is needed.' },
  ],
  scenarios: [
    {
      id: 'pdh-fed',
      emoji: '🍝',
      title: 'Fed and rested after a big carb dinner',
      scene: 'Blood glucose is up, insulin is high, and glycolysis is pouring pyruvate into the mitochondria. The cell wants to burn it and, when full, to store the surplus as fat.',
      hormones: 'Insulin ↑ · glucagon ↓',
      flux: 'up',
      decisions: [
        {
          q: 'Which way is PDC pushed in the well-fed state?',
          choices: ['ON — dephosphorylate E1 and burn the incoming pyruvate', 'OFF — phosphorylate E1 and spare pyruvate'],
          answer: 0,
          why: 'Fed = fuel arriving. Insulin favors the active, dephosphorylated form of E1, so pyruvate flows to acetyl-CoA for the TCA cycle — and any surplus acetyl-CoA seeds fatty-acid synthesis for storage.',
        },
        {
          q: 'Which enzyme sets E1 to its ACTIVE state here?',
          choices: ['PDH phosphatase (PDP) — removes the phosphate', 'PDH kinase (PDK) — adds a phosphate'],
          answer: 0,
          why: 'PDP dephosphorylates E1 and turns PDC ON. PDK does the opposite. Remember the direction: phosphorylation INACTIVATES PDC.',
        },
        {
          q: 'If ATP, NADH, and acetyl-CoA all start climbing as you finish digesting, what happens to PDC?',
          choices: ['It gets throttled back — those products are inhibitors and they activate PDK', 'It speeds up — products are activators'],
          answer: 0,
          why: 'ATP, NADH, and acetyl-CoA are the "we have plenty" signals. They allosterically inhibit E1 AND stimulate PDK, so the gate closes once demand is met — even in the fed state.',
        },
      ],
      teach: 'FED = insulin high → PDP favored → E1 dephosphorylated → PDC ON, pyruvate burned to acetyl-CoA. But the fast allosteric layer overrides on top: once ATP/NADH/acetyl-CoA build up, they inhibit E1 and fire up PDK, closing the gate. Supply opens it; product satiety closes it.',
    },
    {
      id: 'pdh-sprint',
      emoji: '🏃',
      title: 'Sprinting — muscle screaming for ATP',
      scene: 'Contracting muscle floods its cytosol with Ca²⁺, ADP is climbing as ATP is spent, and there is plenty of pyruvate arriving from a maxed-out glycolysis.',
      hormones: 'Ca²⁺ ↑ · ADP ↑ · energy charge falling',
      flux: 'up',
      decisions: [
        {
          q: 'What does the Ca²⁺ surge do to PDC in contracting muscle?',
          choices: ['Activates PDP → dephosphorylates E1 → PDC ON', 'Activates PDK → phosphorylates E1 → PDC OFF'],
          answer: 0,
          why: 'Ca²⁺ activates PDH phosphatase (PDP), which strips the inhibitory phosphate off E1. The same Ca²⁺ signal that triggers contraction unlocks the fuel — acetyl-CoA surges into the TCA cycle right when it is needed.',
        },
        {
          q: 'Which allosteric signals reinforce turning PDC ON here?',
          choices: ['ADP and pyruvate (both activators)', 'ATP and acetyl-CoA (both activators)'],
          answer: 0,
          why: 'ADP ("we are hungry") and pyruvate (abundant substrate) both activate E1 and blunt PDK. ATP and acetyl-CoA are the inhibitory "we have plenty" signals — the opposite.',
        },
      ],
      teach: 'SPRINT = high ATP demand + Ca²⁺ surge. Ca²⁺→PDP→E1 dephosphorylated (ON), and rising ADP/pyruvate pile on as allosteric activators while PDK is quiet. The excitation–contraction Ca²⁺ signal doubles as a "burn fuel now" signal — elegant coupling of the trigger and the fuel.',
    },
    {
      id: 'pdh-fast',
      emoji: '😴',
      title: 'Overnight fast — liver in glucose-sparing mode',
      scene: 'Glucose is drifting down, glucagon is up, and the liver is oxidizing fatty acids. β-oxidation is flooding the matrix with acetyl-CoA and NADH, and the liver needs to SAVE its pyruvate to rebuild glucose.',
      hormones: 'Glucagon ↑ · insulin ↓ · acetyl-CoA & NADH ↑ (from fat)',
      flux: 'down',
      decisions: [
        {
          q: 'Should the fasting liver run PDC and burn its pyruvate to acetyl-CoA?',
          choices: ['No — keep PDC OFF and spare pyruvate for gluconeogenesis', 'Yes — burn pyruvate for energy'],
          answer: 0,
          why: 'The fasting liver needs to EXPORT glucose. Burning pyruvate via PDC (which is irreversible) would waste the very carbon it needs for gluconeogenesis. PDC off; pyruvate is routed to oxaloacetate instead (pyruvate carboxylase).',
        },
        {
          q: 'What turns PDC OFF here, and via what signals?',
          choices: ['PDK is switched on by the high acetyl-CoA/NADH from fat oxidation', 'PDP is switched on by high acetyl-CoA/NADH'],
          answer: 0,
          why: 'β-oxidation raises acetyl-CoA and NADH, which stimulate PDK to phosphorylate and inactivate E1. This is exactly the point of the Randle cycle: burning fat shuts down carbohydrate (pyruvate) oxidation.',
        },
        {
          q: 'Because PDC is irreversible, how does gluconeogenesis get around it?',
          choices: ['It bypasses PDC entirely — pyruvate carboxylase then PEPCK', 'It runs PDC backward: acetyl-CoA → pyruvate'],
          answer: 0,
          why: 'Acetyl-CoA can never be turned back into pyruvate — no enzyme runs PDC in reverse. Gluconeogenesis detours: pyruvate carboxylase (pyruvate → oxaloacetate) and PEPCK. This is also why you cannot make net glucose from fat.',
        },
      ],
      teach: 'FASTING = glucagon high, fat being burned. High acetyl-CoA/NADH turn PDK ON → E1 phosphorylated → PDC OFF, sparing pyruvate for gluconeogenesis. Because the gate is irreversible, gluco­neogenesis must detour around it (pyruvate carboxylase + PEPCK) — and fat, which enters as acetyl-CoA past the gate, cannot become net glucose.',
    },
    {
      id: 'pdh-warburg',
      emoji: '🦠',
      title: 'A tumor cell under the Warburg effect',
      scene: 'A rapidly dividing cancer cell takes up huge amounts of glucose and spits out lactate even though oxygen is plentiful. HIF-1α is driving overexpression of PDK.',
      hormones: 'HIF-1α ↑ → PDK ↑ (aerobic glycolysis)',
      flux: 'off',
      decisions: [
        {
          q: 'With PDK chronically overexpressed, what state is E1 stuck in?',
          choices: ['Phosphorylated and inactive — pyruvate can’t become acetyl-CoA', 'Dephosphorylated and hyperactive — too much acetyl-CoA'],
          answer: 0,
          why: 'PDK phosphorylates E1 and switches PDC OFF. Chronically high PDK locks E1 phosphorylated, so pyruvate is diverted away from the TCA cycle.',
        },
        {
          q: 'Where does the un-processed pyruvate go, and why does the cell like that?',
          choices: ['To lactate — regenerating NAD⁺ for fast glycolysis and supplying biosynthetic carbon', 'To CO₂ via a bypass around PDC'],
          answer: 0,
          why: 'Blocked from acetyl-CoA, pyruvate is reduced to lactate (regenerating NAD⁺ so glycolysis keeps flying) and carbon is freed for building new biomass. Fast ATP + building blocks is exactly what a dividing cell wants.',
        },
      ],
      teach: 'WARBURG = PDC regulation hijacked. HIF-1α drives PDK up, E1 stays phosphorylated and OFF, and pyruvate goes to lactate even with oxygen around. The tumor trades efficient ATP for speed plus biosynthetic carbon. This is why PDK inhibitors like dichloroacetate (which force PDC back on) are studied as anticancer agents.',
    },
    {
      id: 'pdh-refeed',
      emoji: '🍚',
      title: 'Refeeding a malnourished, alcohol-dependent patient',
      scene: 'A severely malnourished patient arrives; a resident is about to hang a glucose IV. Thiamine (B1) stores are depleted — and B1 is the source of TPP, the coenzyme E1 cannot work without.',
      hormones: 'Thiamine (B1) depleted → E1 barely functional',
      flux: 'down',
      decisions: [
        {
          q: 'What should be given BEFORE the glucose, and why?',
          choices: ['Thiamine (B1) — without TPP, E1 fails and a glucose load drives lactic acidosis', 'Extra glucose — the cell just needs more substrate'],
          answer: 0,
          why: 'Thiamine → TPP, the E1 coenzyme. In deficiency PDC is barely holding on. Flood the cell with glucose (→ pyruvate) and it backs up into lactate → dangerous lactic acidosis (refeeding syndrome). Give thiamine first, then glucose.',
        },
        {
          q: 'Which single PDC coenzyme is the missing link in this patient?',
          choices: ['TPP (from thiamine/B1) at E1', 'NAD⁺ (from niacin/B3) at E3'],
          answer: 0,
          why: 'Four of PDC’s five coenzymes come from B vitamins, but the deficiency here is specifically thiamine → TPP at E1. Without it the very first catalytic step (decarboxylation) stalls.',
        },
      ],
      teach: 'REFEEDING = the clinical face of PDC wiring. Thiamine makes TPP; TPP powers E1. In a B1-depleted patient PDC is failing, so a glucose load produces pyruvate that cannot be processed and spills into lactate. Order of operations saves the patient: thiamine BEFORE glucose. The same one-cofactor logic explains beriberi and Wernicke’s encephalopathy.',
    },
  ],
  diseases: [
    {
      id: 'pdh-deficiency',
      name: 'Pyruvate dehydrogenase (E1) deficiency',
      emoji: '🧠',
      vignette:
        'An infant has poor feeding, developmental delay, and neurologic signs. Labs show a persistent lactic acidosis with an elevated pyruvate (normal lactate:pyruvate ratio). Symptoms ease slightly on a high-fat, low-carbohydrate (ketogenic) diet.',
      suspects: ['E1 (pyruvate dehydrogenase)', 'Pyruvate carboxylase', 'Lactate dehydrogenase', 'Pyruvate kinase'],
      answer: 0,
      accumulates: 'Pyruvate and lactate (the gate is shut, so pyruvate backs up and is reduced to lactate)',
      missing: 'Acetyl-CoA from carbohydrate — the brain’s main aerobic fuel supply stalls',
      teach:
        'A defective E1 cannot convert pyruvate to acetyl-CoA, so pyruvate accumulates and is shunted to lactate → lactic acidosis. The brain, which leans heavily on glucose-derived acetyl-CoA, is hit hardest → neurologic disease. A ketogenic diet helps because ketone bodies (and fatty acids) generate acetyl-CoA DOWNSTREAM of the block — bypassing the broken gate. Most cases are X-linked (PDHA1, the E1α gene).',
      pearl: 'PDH deficiency = neurologic disease + lactic acidosis in an infant; the ketogenic diet helps by feeding acetyl-CoA past the block.',
    },
    {
      id: 'arsenite',
      name: 'Arsenite (or mercury) poisoning',
      emoji: '☠️',
      vignette:
        'A patient with chronic arsenic exposure develops encephalopathy and a peripheral neuropathy, with an unexplained lactic acidosis. Multiple α-ketoacid dehydrogenase reactions appear impaired at once.',
      suspects: ['Dihydrolipoamide (the E2 swinging arm)', 'TPP on E1', 'Bound FAD on E3', 'Coenzyme A'],
      answer: 0,
      accumulates: 'Pyruvate and lactate (and other α-ketoacids upstream of the frozen complexes)',
      missing: 'Acetyl-CoA (the complex is locked and cannot turn over)',
      teach:
        'Arsenite (As³⁺) and mercury (Hg²⁺) bridge the two adjacent –SH groups of the reduced dihydrolipoamide, clamping the swinging arm so it can no longer shuttle the acetyl group and reset. PDC freezes; brain and heart — most dependent on its flux — are hit first. TPP is a thiazolium/diphosphate (not a vicinal dithiol), and FAD/CoA are not dithiol targets, which is why the arm is the answer. The same dithiol trap hits α-ketoglutarate dehydrogenase too.',
      pearl: 'Arsenite/mercury target the vicinal DITHIOL of lipoamide — a poison mechanism, not a gene. Lipoamide-bearing complexes freeze together.',
    },
    {
      id: 'thiamine-def',
      name: 'Thiamine (B1) deficiency — beriberi / Wernicke',
      emoji: '🍺',
      vignette:
        'A chronic alcohol user presents with confusion, ophthalmoplegia, and ataxia (Wernicke’s), plus a high-output cardiac picture on exam. Blood lactate is elevated. Symptoms improve dramatically after a vitamin is administered.',
      suspects: ['Thiamine → TPP (E1 coenzyme)', 'Niacin → NAD⁺ (E3 acceptor)', 'Riboflavin → FAD (E3 prosthetic group)', 'Pantothenate → CoA (E2 acceptor)'],
      answer: 0,
      accumulates: 'Pyruvate and lactate (E1 cannot decarboxylate pyruvate)',
      missing: 'Functional TPP → the first catalytic step of PDC stalls',
      teach:
        'Thiamine (B1) is the precursor of TPP, the coenzyme E1 needs to decarboxylate pyruvate. Without it, the gate barely opens: pyruvate and lactate accumulate, and glucose-dependent nerves and the heart suffer — beriberi (dry = neuro, wet = cardiac) and Wernicke’s encephalopathy. This is the mechanistic root of the clinical rule "give thiamine BEFORE glucose," since a glucose load in a deficient patient forces pyruvate into lactate.',
      pearl: 'B1 → TPP → E1. Deficiency = beriberi/Wernicke + lactic acidosis. Thiamine before glucose, always.',
    },
  ],
  quiz: [
    {
      tag: 'basics',
      stem: 'Which equation correctly gives the NET reaction catalyzed by the pyruvate dehydrogenase complex?',
      choices: [
        'Pyruvate + CoA + NAD⁺ → acetyl-CoA + CO₂ + NADH + H⁺',
        'Pyruvate + CoA + FAD → acetyl-CoA + CO₂ + FADH₂',
        'Acetyl-CoA + CO₂ + NADH → pyruvate + CoA + NAD⁺',
        'Pyruvate + CoA + NAD⁺ + ATP → acetyl-CoA + CO₂ + NADH + ADP',
      ],
      answer: 0,
      rationale:
        'PDC is an oxidative decarboxylation: pyruvate loses its carboxyl carbon as CO₂, the surviving two carbons join CoA as acetyl-CoA, and NAD⁺ is reduced to NADH. FADH₂ is only a transient enzyme-bound relay at E3, never a net product, so the FAD equation is wrong. The reverse reaction does not occur in animals (irreversible), and PDC neither consumes nor makes ATP.',
    },
    {
      tag: 'basics',
      stem: 'At which point in the PDC mechanism is NADH actually produced?',
      choices: [
        'At E3, when electrons are finally passed from bound FADH₂ to NAD⁺',
        'At E1, when pyruvate is decarboxylated and CO₂ is released',
        'At E1, when the hydroxyethyl group is oxidized and transferred to lipoamide',
        'At E2, when the acetyl group is transferred to coenzyme A',
      ],
      answer: 0,
      rationale:
        'The single NADH is made only at the very end, at E3, where electrons held first on lipoamide and then on E3’s bound FAD (as FADH₂) are finally handed to NAD⁺. The E1 decarboxylation releases CO₂ but no NADH; the E1 oxidation reduces lipoamide (a classic trap — it LOOKS like the oxidation but makes no NADH); E2 makes acetyl-CoA. Only the E3 handoff to NAD⁺ yields NADH.',
    },
    {
      tag: 'energetics',
      stem: 'Per molecule of GLUCOSE fully processed through glycolysis and then PDC, how much CO₂ and NADH does the PDC step alone contribute?',
      choices: [
        '2 CO₂ and 2 NADH (one of each per pyruvate, ×2 pyruvate)',
        '1 CO₂ and 1 NADH',
        '6 CO₂ and 2 NADH',
        '2 CO₂ and 2 FADH₂',
      ],
      answer: 0,
      rationale:
        'PDC yields 1 CO₂ + 1 NADH + 1 acetyl-CoA per pyruvate. Glycolysis makes two pyruvate per glucose, so the bridge step contributes 2 CO₂ and 2 NADH per glucose. The 6 CO₂ figure belongs to full oxidation (glucose → 6 CO₂ across glycolysis + PDC + TCA), and FADH₂ is not a net PDC product.',
    },
    {
      tag: 'energetics',
      stem: 'Why is the thioester bond of acetyl-CoA considered "high-energy" (hydrolysis ≈ −31 kJ/mol, near ATP), unlike an ordinary oxygen ester (≈ −21 kJ/mol)?',
      choices: [
        'Sulfur is larger than oxygen and stabilizes the carbonyl poorly by resonance, leaving the thioester strained',
        'The bond stores energy in coenzyme A itself, which is the valuable part of the molecule',
        'The sulfur atom forms an extra covalent bond to the carbonyl oxygen',
        'Thioesters release a phosphate group on hydrolysis, like ATP does',
      ],
      answer: 0,
      rationale:
        'Sulfur’s larger orbitals overlap the carbonyl carbon poorly, so its lone pairs cannot lend the resonance stabilization an oxygen ester enjoys. The thioester is left strained — like a wound spring — so hydrolysis releases more free energy. The energy is in the BOND, not the CoA handle, and no phosphate is involved.',
    },
    {
      tag: 'regulation',
      stem: 'During vigorous muscle contraction, cytosolic Ca²⁺ rises. How does this affect PDC?',
      choices: [
        'Ca²⁺ activates PDP, which dephosphorylates E1 and turns PDC ON',
        'Ca²⁺ activates PDK, which phosphorylates E1 and turns PDC OFF',
        'Ca²⁺ inhibits PDP, so E1 stays phosphorylated and PDC turns OFF',
        'Ca²⁺ binds acetyl-CoA and relieves product inhibition of E1',
      ],
      answer: 0,
      rationale:
        'Calcium activates pyruvate dehydrogenase phosphatase (PDP), which removes the inhibitory phosphate from E1 and switches PDC ON — coupling the contraction signal to a surge of acetyl-CoA for ATP. PDK is the kinase that turns PDC OFF, and Ca²⁺ acts on PDP, not PDK. Ca²⁺ does not bind acetyl-CoA.',
    },
    {
      tag: 'regulation',
      stem: 'In the covalent regulation of PDC, what is the direction of the phosphorylation switch?',
      choices: [
        'PDK phosphorylates E1 to INACTIVATE it; PDP removes the phosphate to activate it',
        'PDK phosphorylates E1 to activate it; PDP removes the phosphate to inactivate it',
        'Phosphorylation of E2 activates the complex; dephosphorylation inactivates it',
        'Phosphorylation and dephosphorylation both act on E3 with no net effect',
      ],
      answer: 0,
      rationale:
        'Here phosphorylation INACTIVATES (same convention as glycogen synthase): PDH kinase adds a phosphate to a serine on E1 and shuts PDC off, while PDH phosphatase removes it and turns PDC on. PDK is itself stimulated by the high-energy "plenty" signals — ATP, NADH, and acetyl-CoA — reinforcing the allosteric brake. The switch is on E1, not E2 or E3.',
    },
    {
      tag: 'regulation',
      stem: 'Which set correctly pairs the ALLOSTERIC activators and inhibitors of PDC?',
      choices: [
        'Activators: ADP and pyruvate · Inhibitors: ATP, NADH, and acetyl-CoA',
        'Activators: ATP and acetyl-CoA · Inhibitors: ADP and pyruvate',
        'Activators: NADH and acetyl-CoA · Inhibitors: Ca²⁺ and ADP',
        'Activators: citrate and NAD⁺ · Inhibitors: pyruvate and CoA',
      ],
      answer: 0,
      rationale:
        'The products themselves are the fast inhibitors — ATP, NADH, and acetyl-CoA all say "we have plenty, slow down." ADP and pyruvate are the activators: "we are hungry / substrate is here, speed up." These same product signals also stimulate PDK, so the allosteric and covalent layers point the same direction.',
    },
    {
      tag: 'disease',
      stem: 'A resident is about to start a glucose IV on a severely malnourished, alcohol-dependent patient. Based on PDC biochemistry, what should be given FIRST and why?',
      choices: [
        'Thiamine (B1), because without TPP the E1 step fails and a glucose load drives lactic acidosis',
        'Niacin (B3), because NAD⁺ must be supplied before the gate can open',
        'Lipoic acid, because the swinging arm is depleted in malnutrition',
        'Acetyl-CoA, because PDC needs its product to prime the reaction',
      ],
      answer: 0,
      rationale:
        'Thiamine is the precursor of TPP, the coenzyme E1 needs to decarboxylate pyruvate. In a thiamine-deficient patient PDC is already failing; a glucose load floods the cell with pyruvate it cannot process, so it backs up into lactate → lactic acidosis (refeeding syndrome). Give thiamine before glucose. Acetyl-CoA is the product, not a primer; niacin/NAD⁺ is not limiting here; lipoic acid is synthesized endogenously.',
    },
    {
      tag: 'disease',
      stem: 'A patient with a genetic E3 (dihydrolipoamide dehydrogenase) deficiency has lactic acidosis. E3 is shared by PDC, the α-ketoglutarate dehydrogenase complex, and the branched-chain α-ketoacid dehydrogenase complex. Which observation best fits losing this shared subunit?',
      choices: [
        'Multiple oxidative decarboxylations fail at once, because E3 regenerates oxidized lipoamide in all three complexes',
        'Only pyruvate metabolism is impaired, since E3 is unique to PDC',
        'Acetyl-CoA accumulates because E2 cannot release it',
        'NAD⁺ is overproduced, driving excessive flux through all three complexes',
      ],
      answer: 0,
      rationale:
        'E3 is the common dihydrolipoamide dehydrogenase shared by all three α-ketoacid dehydrogenase complexes; its job is to reoxidize the dithiol lipoamide (via FAD to NAD⁺). Losing E3 stalls all three, so the defect is not unique to pyruvate metabolism. Without E3 the arm stays reduced and cannot reset, so acetyl-CoA does NOT accumulate, and NADH formation is impaired (not overproduced) — contributing to the lactic acidosis as pyruvate is shunted to lactate.',
    },
    {
      tag: 'integration',
      stem: 'Why must gluconeogenesis bypass PDC using pyruvate carboxylase and PEPCK rather than simply running PDC in reverse?',
      choices: [
        'The PDC reaction is essentially irreversible in animals because of its large negative free-energy change',
        'PDC is located in the cytosol, where gluconeogenesis cannot reach it',
        'PDC directly requires molecular O₂, which is absent during fasting',
        'Acetyl-CoA is too small a molecule to re-enter the pathway',
      ],
      answer: 0,
      rationale:
        'The oxidative decarboxylation has a large negative ΔG and no animal enzyme reverses it, so acetyl-CoA cannot be turned back into pyruvate. Gluconeogenesis therefore detours (pyruvate carboxylase → oxaloacetate, then PEPCK). PDC is in the matrix, not the cytosol; irreversibility (not localization or molecule size) is the reason; and PDC uses no O₂ directly — it needs aerobic conditions only so the ETC can regenerate NAD⁺. This is also why net glucose cannot be made from fat.',
    },
  ],
  funFact:
    'The pyruvate dehydrogenase complex is bigger than a ribosome — roughly 10 megadaltons of protein — and it runs an assembly line where a single 14-Å lipoamide "robot arm," tethered to a lysine, physically swings the carbon between three active sites so the intermediate never once touches the surrounding water.',
};
