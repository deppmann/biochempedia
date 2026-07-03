import type { Pathway } from '../types';

/* =============================================================================
   AMINO ACID CATABOLISM — burning protein for fuel (hand-authored, cross-checked
   against src/content/lessons/protein-turnover-amino-acid-catabolism/lesson.mdx,
   Act 2 "nitrogen is toxic, so cage it" + Act 3 "carbon is too valuable to waste").

   The organizing logic (lesson slide "Where Does the Nitrogen Go?"): every amino
   acid splits into TWO problems. The α-amino nitrogen is a liability — free
   ammonia is neurotoxic — so it is collected onto glutamate, shuttled safely in
   blood as alanine/glutamine, and locked into urea in the liver. The carbon
   skeleton is valuable fuel and enters central metabolism at seven doors, either
   glucogenic (→ glucose) or ketogenic (→ ketones); only Leu & Lys are purely
   ketogenic. Steps 1–4 are the shared nitrogen-handling core; steps 5–6 are the
   carbon fates + the muscle→liver shuttle.

   doubleAfter: 0 — nothing splits into two counted halves here, so no ×2 ledger.
   ============================================================================ */

export const aminoAcidCatabolism: Pathway = {
  id: 'amino-acid-catabolism',
  name: 'Amino Acid Catabolism',
  emoji: '🥩',
  tagline: 'Rip the nitrogen off, cage it as urea, then burn the leftover carbon. Waste not.',
  blurb:
    'Every amino acid is two problems in one: a toxic amino group and a valuable carbon skeleton. Strip the nitrogen (PLP-dependent transamination → glutamate → free ammonia), package it into non-toxic urea in the liver, and feed the carbons into central metabolism as glucose or ketones. Diet plus your own muscle protein, disassembled for fuel.',
  difficulty: 3,
  location: 'Liver (nitrogen disposal & urea) + muscle (transamination, alanine export)',
  netYield: 'No fixed ATP tally — carbon skeletons enter at 7 doors (glucogenic → glucose, ketogenic → ketones); nitrogen disposal COSTS 4 high-energy bonds per urea',
  start: 'Amino acids (diet + muscle protein)',
  startShort: 'Amino acids',
  startEmoji: '🥩',
  doubleAfter: 0, // nothing splits into two separately counted halves
  lessonSlug: 'protein-turnover-amino-acid-catabolism',
  steps: [
    {
      n: 1,
      product: 'Glutamate + a new α-keto acid (nitrogen collected)',
      short: 'Transamination',
      enzyme: 'Aminotransferases (ALT, AST) — PLP / vitamin B₆',
      irreversible: false,
      emoji: '🔁',
      fact: 'The nitrogen funnel. An aminotransferase hands the α-amino group from many different amino acids onto α-ketoglutarate, collecting all that nitrogen onto ONE carrier — glutamate — and leaving the amino acid’s carbon skeleton as an α-keto acid. Every transaminase uses PLP (vitamin B₆) for its Schiff-base swap: see PLP, think amino-group transfer. Near-equilibrium and reversible. ALT and AST leak into blood when hepatocytes die, which is why they sit on every liver panel.',
    },
    {
      n: 2,
      product: 'Glutamate (the single nitrogen collection point)',
      short: 'Glutamate',
      enzyme: 'Convergence step (no new enzyme — the funnel’s outlet)',
      irreversible: false,
      emoji: '🫗',
      fact: 'All roads lead to glutamate. Diverse amino acids channel their nitrogen into this one pool, so the cell only needs ONE enzyme downstream to actually release the ammonia. Glutamate is the hub between "collect the nitrogen" and "commit it to disposal."',
    },
    {
      n: 3,
      product: 'α-Ketoglutarate + free NH₄⁺ (ammonia released)',
      short: 'Deamination',
      enzyme: 'Glutamate dehydrogenase (GDH)',
      tokens: { nadh: 1 },
      irreversible: true,
      committed: true,
      emoji: '💥',
      fact: 'Oxidative deamination — the committed nitrogen-disposal step. GDH strips the nitrogen off glutamate as FREE ammonium (NH₄⁺) and regenerates α-ketoglutarate so the transaminases can collect again. It uses NAD(P)⁺ → NAD(P)H. Essentially irreversible in the release direction, and allosterically activated by ADP/GDP (low energy → burn amino acids) and inhibited by ATP/GTP. This is the ammonia that feeds the urea cycle.',
    },
    {
      n: 4,
      product: 'Glutamine (safe, 2-nitrogen blood courier)',
      short: 'Glutamine',
      enzyme: 'Glutamine synthetase',
      tokens: { atp: -1 },
      irreversible: false,
      emoji: '🚚',
      fact: 'Ammonia is toxic, so tissues rarely move it free. Glutamine synthetase adds a SECOND amino group onto glutamate (costing 1 ATP), making glutamine — the most abundant free amino acid in blood and the body’s non-toxic, two-nitrogen courier. It ferries nitrogen to the liver (for urea) and kidney (for acid-base), and rapidly dividing gut/immune cells burn it as fuel.',
    },
    {
      n: 5,
      product: 'Carbon skeletons → 7 entry points (glucogenic vs ketogenic)',
      short: 'Carbon fork',
      enzyme: 'Many pathway-specific enzymes (skeleton-dependent)',
      irreversible: false,
      emoji: '🍴',
      fact: 'The carbon side of the story. After the nitrogen is gone, all 20 skeletons enter central metabolism at just SEVEN doors. GLUCOGENIC skeletons land on pyruvate, oxaloacetate, α-ketoglutarate, succinyl-CoA, or fumarate → can be rebuilt into glucose. KETOGENIC skeletons land on acetyl-CoA or acetoacetyl-CoA → ketones only. Only Leucine & Lysine are PURELY ketogenic (they enter as acetyl-CoA, and pyruvate dehydrogenase is irreversible, so there is no path back to glucose). Ile, Phe, Thr, Trp, and Tyr are both.',
    },
    {
      n: 6,
      product: 'Alanine → liver (glucose–alanine / Cahill cycle)',
      short: 'Alanine cycle',
      enzyme: 'Alanine aminotransferase (ALT)',
      irreversible: false,
      emoji: '🔄',
      fact: 'How working muscle ships its nitrogen home. Muscle transaminates its collected nitrogen onto pyruvate to make alanine — non-toxic — which travels in blood to the liver. There the liver strips the nitrogen back off (into the urea cycle) and turns the leftover pyruvate into glucose, which returns to muscle. Alanine is the nitrogen shuttle, glucose the energy shuttle, running opposite directions. Your brain, in a real sense, pays its bills with your biceps.',
    },
  ],
  regulators: [
    {
      name: 'Aminotransferases (transamination)',
      role: 'Near-equilibrium, so not a real throttle — it just funnels nitrogen onto glutamate wherever concentrations push it. PLP (B₆) is the shared cofactor; ALT/AST are clinical markers of hepatocyte injury, not control points.',
    },
    {
      name: 'Glutamate dehydrogenase (GDH)',
      role: 'The committed release step and the one true allosteric switch here. ↑ by ADP/GDP (low energy charge → dump nitrogen, burn amino acids); ↓ by ATP/GTP (energy-replete → hold on). "Off" when the cell is full.',
    },
    {
      name: 'Overall catabolic drive (hormonal / dietary)',
      role: 'Amino-acid catabolism is INDUCED by fasting (muscle protein → alanine → hepatic gluconeogenesis) and by a high-protein diet (excess amino acids can’t be stored, so they’re burned and their nitrogen excreted).',
    },
    {
      name: 'CPS-I (urea-cycle gate, downstream)',
      role: 'The rate-limiting step of the urea cycle that receives the ammonia. Activated only when N-acetylglutamate (NAG) is present — a feedforward signal built from acetyl-CoA + glutamate that says "nitrogen is arriving, open the gate."',
    },
  ],
  scenarios: [
    {
      id: 'aac-highprotein',
      emoji: '🍗',
      title: 'You ate an enormous steak',
      scene:
        'A big protein load just arrived. Amino acids can’t be warehoused the way glucose (glycogen) and fat (triglyceride) can, so the excess has to be burned — and that means dealing with a flood of nitrogen.',
      hormones: 'Dietary amino-acid load ↑ · catabolism induced',
      flux: 'up',
      decisions: [
        {
          q: 'What happens to amino-acid catabolism after a high-protein meal?',
          choices: [
            'Ramps UP — excess amino acids can’t be stored, so they’re burned',
            'Shuts down — the body stores the extra amino acids as "protein reserve"',
          ],
          answer: 0,
          why: 'There is no dedicated storage form for amino acids. Any surplus beyond what’s needed for protein synthesis is catabolized: carbon burned or made into glucose/fat, nitrogen sent to urea.',
        },
        {
          q: 'The α-amino groups from all these amino acids are collected onto…',
          choices: [
            'Glutamate, via PLP-dependent transamination',
            'Directly onto urea, skipping any carrier',
          ],
          answer: 0,
          why: 'Transaminases move each amino group onto α-ketoglutarate → glutamate, the single collection point. Only then does GDH release free ammonia. Nitrogen is never dumped straight into urea.',
        },
        {
          q: 'Why must the liver ramp UP the urea cycle now?',
          choices: [
            'To detoxify the rising ammonia before it reaches the brain',
            'To store the extra nitrogen as ammonia for later use',
          ],
          answer: 0,
          why: 'Free ammonia is neurotoxic — it can’t be stored or allowed to accumulate. N-acetylglutamate rises with the amino-acid load and switches on CPS-I, accelerating ureagenesis to cage the nitrogen.',
        },
      ],
      teach:
        'HIGH PROTEIN = no storage option → burn the surplus. Nitrogen funnels onto glutamate, GDH releases ammonia, and the urea cycle (feedforward-activated by NAG) revs up to package it safely. Carbon skeletons feed gluconeogenesis, the TCA cycle, or fat synthesis.',
    },
    {
      id: 'aac-fasting',
      emoji: '🌙',
      title: 'Overnight fast — the brain still needs glucose',
      scene:
        'Blood glucose is drifting down and liver glycogen is running low, but the brain must keep getting glucose. The body starts disassembling muscle protein to supply gluconeogenic carbon — and to do it, the nitrogen has to travel safely from muscle to liver.',
      hormones: 'Glucagon ↑ · insulin ↓ · gluconeogenesis on',
      flux: 'up',
      decisions: [
        {
          q: 'In what form does muscle ship the nitrogen from its catabolized protein to the liver?',
          choices: [
            'Alanine (the glucose–alanine / Cahill cycle)',
            'Free ammonia dissolved in blood',
          ],
          answer: 0,
          why: 'Muscle transaminates its nitrogen onto pyruvate to make alanine, which is non-toxic. Free ammonia in the blood would be neurotoxic; the body almost never transports it that way.',
        },
        {
          q: 'What does the liver do with the pyruvate skeleton of that alanine?',
          choices: [
            'Runs gluconeogenesis to make glucose for the brain',
            'Burns it fully to CO₂ for its own ATP',
          ],
          answer: 0,
          why: 'The glucose–alanine cycle exists to hand the liver gluconeogenic carbon: alanine → pyruvate → glucose, which is exported back to muscle and brain. The nitrogen it carried goes into urea.',
        },
        {
          q: 'Which allosteric signal keeps glutamate dehydrogenase releasing nitrogen during the fast?',
          choices: [
            'ADP/GDP (low energy charge → catabolize amino acids)',
            'ATP/GTP (high energy charge → shut GDH off)',
          ],
          answer: 0,
          why: 'A fasting, energy-hungry liver has a low energy charge. ADP and GDP allosterically activate GDH, so glutamate keeps giving up its nitrogen and feeding the urea cycle. ATP/GTP would do the opposite.',
        },
      ],
      teach:
        'FASTING = mobilize muscle protein. The glucose–alanine cycle carries nitrogen to the liver as harmless alanine; the liver makes glucose from the pyruvate and cages the nitrogen as urea. GDH stays active because the energy charge is low (ADP/GDP on).',
    },
    {
      id: 'aac-endurance',
      emoji: '🏃',
      title: 'Hour 3 of a long run',
      scene:
        'Endurance exercise. Working muscle is generating amino-group nitrogen (from branched-chain amino acids and protein) and pyruvate at the same time. It needs to unload the nitrogen without poisoning itself.',
      hormones: 'Sustained work · glucose–alanine cycle active',
      flux: 'up',
      decisions: [
        {
          q: 'How does exercising muscle package nitrogen for export?',
          choices: [
            'Onto pyruvate to make alanine, sent to the liver',
            'Onto oxaloacetate to make urea inside the muscle',
          ],
          answer: 0,
          why: 'The glucose–alanine cycle again: muscle combines its amino nitrogen with pyruvate to make alanine and ships it out. Muscle has no urea cycle, so it cannot make urea itself.',
        },
        {
          q: 'Why can’t muscle just make urea and be done with it?',
          choices: [
            'Muscle lacks the urea-cycle enzymes — ureagenesis is a liver (and partly kidney) job',
            'Muscle makes urea but can’t excrete it, so it exports alanine instead',
          ],
          answer: 0,
          why: 'The urea cycle enzymes (CPS-I, OTC, etc.) are expressed in liver, not skeletal muscle. Muscle therefore exports its nitrogen as alanine (or glutamine) for the liver to handle.',
        },
      ],
      teach:
        'ENDURANCE EXERCISE = the glucose–alanine cycle in full swing. Muscle offloads waste nitrogen as non-toxic alanine and gets glucose back from the liver — a round trip where alanine and glucose run in opposite directions. Muscle can’t make urea; only the liver can.',
    },
    {
      id: 'aac-starvation',
      emoji: '🕰️',
      title: 'Day 20 of starvation',
      scene:
        'Prolonged starvation. Early on, the body cannibalized muscle protein hard for gluconeogenesis. But muscle is finite — losing too much of it is lethal. The body needs to protect its remaining protein.',
      hormones: 'Ketone bodies ↑ · protein sparing engaged',
      flux: 'down',
      decisions: [
        {
          q: 'What happens to the rate of muscle-protein catabolism late in starvation?',
          choices: [
            'It DROPS — the body spares protein as the brain shifts to ketone bodies',
            'It keeps climbing — protein is the brain’s preferred fuel to the end',
          ],
          answer: 0,
          why: 'Sustained protein breakdown at the early rate would be fatal. As ketone bodies rise and the brain adapts to using them, demand for gluconeogenesis (and thus for amino-acid carbon) falls, sparing muscle protein.',
        },
        {
          q: 'What lets the brain reduce its glucose demand and spare protein?',
          choices: [
            'It burns ketone bodies for much of its energy instead of glucose',
            'It switches to burning fatty acids directly across the blood–brain barrier',
          ],
          answer: 0,
          why: 'The brain cannot use long-chain fatty acids (they don’t cross the barrier well), but it adapts to oxidize ketone bodies made from fat. Less glucose needed → less gluconeogenesis → less muscle sacrificed.',
        },
      ],
      teach:
        'LATE STARVATION = protein sparing. Early starvation burns muscle for glucose, but that can’t last — so the brain shifts to ketone bodies, dropping its glucose demand and slowing amino-acid catabolism. The switch buys survival time by protecting the muscle you still have.',
    },
    {
      id: 'aac-liverfail',
      emoji: '🧠',
      title: 'Advanced liver failure — confusion and asterixis',
      scene:
        'A patient with cirrhosis becomes confused and drowsy, with a flapping tremor of the outstretched hands. Blood ammonia is high. The failing liver can no longer keep up with nitrogen disposal.',
      hormones: 'Hepatic urea capacity ↓↓ · ammonia ↑',
      flux: 'down',
      decisions: [
        {
          q: 'Why does ammonia rise when the liver fails?',
          choices: [
            'The urea cycle (a liver pathway) can’t convert enough ammonia to urea',
            'Muscle stops making alanine, so ammonia has nowhere to go',
          ],
          answer: 0,
          why: 'Ureagenesis happens in the liver. When hepatocytes fail, the cycle can’t clear the incoming nitrogen, so ammonia — the toxic intermediate — accumulates in blood.',
        },
        {
          q: 'How does high ammonia injure the brain?',
          choices: [
            'Astrocytes trap it as glutamine and swell, causing brain edema',
            'Ammonia dissolves the myelin sheath of neurons directly',
          ],
          answer: 0,
          why: 'Astrocytes detoxify ammonia by making glutamine; the osmotic load makes them swell, producing cerebral edema and the encephalopathy (confusion, asterixis). This is the neurotoxicity that the urea cycle exists to prevent.',
        },
        {
          q: 'A rational treatment lowers gut ammonia. Which fits?',
          choices: [
            'Restrict dietary protein and give agents that trap/excrete nitrogen (e.g. lactulose, scavengers)',
            'Give a high-protein diet to push the urea cycle harder',
          ],
          answer: 0,
          why: 'Less protein in = less ammonia generated. Lactulose acidifies the colon to trap ammonia as ammonium and speed its excretion; nitrogen scavengers route nitrogen out by alternate paths. Loading MORE protein would worsen the encephalopathy.',
        },
      ],
      teach:
        'LIVER FAILURE = the nitrogen-disposal factory is offline. Ammonia climbs because only the liver runs the urea cycle; astrocytes swell trapping it as glutamine → hepatic encephalopathy. Treat by cutting nitrogen input and trapping/excreting ammonia. This is the whole point of caging nitrogen as urea.',
    },
  ],
  diseases: [
    {
      id: 'pku',
      name: 'Phenylketonuria (PKU)',
      emoji: '🍼',
      vignette:
        'A newborn misses screening and later shows developmental delay, microcephaly, eczema, and a musty (mousy) body odor. Blood phenylalanine is markedly elevated; tyrosine is low. The parents are told to strictly avoid aspartame.',
      suspects: [
        'Phenylalanine hydroxylase (PAH)',
        'Homogentisate oxidase',
        'Branched-chain α-ketoacid dehydrogenase',
        'Cystathionine β-synthase',
      ],
      answer: 0,
      accumulates: 'Phenylalanine (and phenylketones — phenylpyruvate, etc.), which are toxic to the developing brain',
      missing: 'Tyrosine (now an essential amino acid, since it can’t be made from Phe)',
      teach:
        'Phenylalanine hydroxylase normally converts phenylalanine → tyrosine (using the BH₄ cofactor). Block it and phenylalanine piles up, spilling into phenylketones that damage the developing brain → intellectual disability, microcephaly, mousy odor. Because tyrosine can no longer be made from Phe, it becomes essential. Treatment is dietary: low-phenylalanine diet, tyrosine supplementation, sometimes sapropterin (BH₄); avoid aspartame (it’s a Phe source). Caught by newborn screening around day 2, it’s a preventable catastrophe.',
      pearl: 'PKU = defective phenylalanine hydroxylase → high Phe, mousy odor, avoid aspartame; Tx = low-Phe diet + tyrosine.',
    },
    {
      id: 'msud',
      name: 'Maple Syrup Urine Disease (MSUD)',
      emoji: '🍁',
      vignette:
        'A neonate feeds poorly, becomes lethargic, and develops seizures. The urine and cerumen smell distinctly of maple syrup / burnt sugar. Labs show elevated branched-chain amino acids (isoleucine, leucine, valine) and their α-keto acids.',
      suspects: [
        'Branched-chain α-ketoacid dehydrogenase (BCKD)',
        'Phenylalanine hydroxylase (PAH)',
        'Glutamate dehydrogenase (GDH)',
        'Arginase',
      ],
      answer: 0,
      accumulates: 'Branched-chain amino acids (Ile, Leu, Val) and their α-keto acids — neurotoxic, especially leucine',
      missing: 'Onward catabolism of the branched-chain skeletons into the TCA cycle',
      teach:
        'Branched-chain α-ketoacid dehydrogenase decarboxylates the α-keto acids of isoleucine, leucine, and valine after transamination. When it’s deficient, the branched-chain amino acids and their keto acids back up — the keto acids give urine its maple-syrup smell, and leucine is neurotoxic, causing lethargy, seizures, and (untreated) death. Management is a lifelong diet restricted in the branched-chain amino acids. (Mnemonic: I Love Vermont maple syrup → Ile, Leu, Val.)',
      pearl: 'MSUD = defective branched-chain α-ketoacid dehydrogenase → Ile/Leu/Val + keto acids build up → maple-syrup urine, neurotoxic leucine.',
    },
    {
      id: 'alkaptonuria',
      name: 'Alkaptonuria',
      emoji: '⚫',
      vignette:
        'An adult notices their urine turns black after sitting out, and over the years develops dark pigmentation of the ear cartilage and arthritis. Otherwise they are relatively well. This is the disorder Archibald Garrod used in 1902 to coin "inborn error of metabolism."',
      suspects: [
        'Homogentisate oxidase',
        'Phenylalanine hydroxylase (PAH)',
        'Cystathionine β-synthase',
        'Ornithine transcarbamylase (OTC)',
      ],
      answer: 0,
      accumulates: 'Homogentisic acid (a tyrosine-degradation intermediate) — oxidizes to a black pigment',
      missing: 'Complete breakdown of the tyrosine carbon skeleton',
      teach:
        'Homogentisate oxidase acts in the tyrosine degradation pathway. Without it, homogentisic acid accumulates; on standing (air oxidation) it darkens urine to black, and over a lifetime it deposits in cartilage (ochronosis) and joints, causing arthritis. Clinically it is far milder than PKU or MSUD — its importance is historical: Garrod recognized its recessive inheritance and coined "inborn error of metabolism," launching biochemical genetics (one gene → one missing enzyme → one chemical consequence).',
      pearl: 'Alkaptonuria = homogentisate oxidase deficiency → black urine + ochronotic arthritis; benign, but the disease that launched biochemical genetics.',
    },
    {
      id: 'homocystinuria',
      name: 'Homocystinuria',
      emoji: '🦴',
      vignette:
        'A young patient is tall and lanky with long fingers, has downward-dislocated lenses, and suffers early thromboembolic events. Plasma and urine homocysteine are markedly elevated; methionine is high. Some cases improve dramatically with high-dose vitamin B₆.',
      suspects: [
        'Cystathionine β-synthase (CBS)',
        'Phenylalanine hydroxylase (PAH)',
        'Homogentisate oxidase',
        'Branched-chain α-ketoacid dehydrogenase',
      ],
      answer: 0,
      accumulates: 'Homocysteine (and methionine) — homocysteine damages vessel walls and connective tissue',
      missing: 'Conversion of homocysteine onward to cystathionine → cysteine',
      teach:
        'Cystathionine β-synthase condenses homocysteine with serine to make cystathionine (a PLP/B₆-dependent step) on the route from methionine to cysteine. When it’s deficient, homocysteine builds up — damaging connective tissue and endothelium — giving a Marfan-like habitus, DOWNWARD lens dislocation (vs upward in Marfan), thromboembolism, and intellectual disability. Because the enzyme uses PLP, B₆-responsive cases improve on high-dose vitamin B₆; management otherwise restricts methionine and supplements cysteine, folate, and B₁₂.',
      pearl: 'Homocystinuria = cystathionine β-synthase deficiency → high homocysteine, downward lens dislocation, clots; some are vitamin-B₆ responsive.',
    },
  ],
  quiz: [
    {
      tag: 'basics',
      stem: 'In the transamination of most amino acids, the α-amino group is transferred onto which acceptor, and which cofactor is required?',
      choices: [
        'Onto α-ketoglutarate (forming glutamate); requires pyridoxal phosphate (PLP / vitamin B₆)',
        'Onto oxaloacetate (forming aspartate); requires biotin',
        'Directly onto ammonia (forming glutamine); requires NAD⁺',
        'Onto pyruvate (forming alanine); requires thiamine pyrophosphate (TPP)',
      ],
      answer: 0,
      rationale:
        'Aminotransferases move the α-amino group onto α-ketoglutarate, generating glutamate (the nitrogen collection point) plus the corresponding α-keto acid. Every such reaction uses PLP (vitamin B₆) to form the Schiff-base intermediate — "see PLP, think amino-group transfer." Biotin runs carboxylations, TPP runs oxidative decarboxylations, and free ammonia is released later by GDH, not during transamination.',
    },
    {
      tag: 'basics',
      stem: 'Which enzyme performs oxidative deamination, releasing free ammonium from the central nitrogen carrier?',
      choices: [
        'Glutamate dehydrogenase, acting on glutamate to yield α-ketoglutarate + NH₄⁺',
        'Alanine aminotransferase, acting on alanine to yield pyruvate + NH₄⁺',
        'Glutamine synthetase, acting on glutamate to yield glutamine + NH₄⁺',
        'Carbamoyl phosphate synthetase I, acting on glutamate to yield urea + NH₄⁺',
      ],
      answer: 0,
      rationale:
        'Glutamate dehydrogenase (GDH) is the enzyme that actually liberates free ammonium, converting glutamate back to α-ketoglutarate using NAD(P)⁺. Transaminases only MOVE amino groups (they don’t release free ammonia); glutamine synthetase ADDS a second amino group (the opposite direction); and CPS-I consumes ammonia to start the urea cycle rather than producing it.',
    },
    {
      tag: 'basics',
      stem: 'Why must nitrogen be collected onto glutamate and shuttled as alanine or glutamine rather than transported as free ammonia?',
      choices: [
        'Free ammonia is neurotoxic, so it is carried in non-toxic amino-acid form',
        'Free ammonia is too large to cross cell membranes',
        'Glutamate and glutamine store more energy than ammonia',
        'Ammonia cannot dissolve in blood plasma',
      ],
      answer: 0,
      rationale:
        'Ammonia is neurotoxic — at high levels it causes astrocyte swelling and encephalopathy — so the body almost never moves it free. It is collected onto glutamate and shuttled safely as alanine (glucose–alanine cycle) and glutamine (the abundant two-nitrogen courier). Ammonia is small and quite soluble; the issue is toxicity, not size or solubility.',
    },
    {
      tag: 'energetics',
      stem: 'Which pair of amino acids is PURELY ketogenic, and what makes a purely ketogenic amino acid unable to yield net glucose?',
      choices: [
        'Leucine and lysine — they enter as acetyl-CoA, and pyruvate dehydrogenase is irreversible',
        'Glutamate and glutamine — they enter as α-ketoglutarate',
        'Alanine and serine — they enter as pyruvate',
        'Aspartate and asparagine — they enter as oxaloacetate',
      ],
      answer: 0,
      rationale:
        'Leucine and lysine are the only two purely ketogenic amino acids; their carbons enter as acetyl-CoA (or acetoacetyl-CoA). Because pyruvate dehydrogenase is irreversible, acetyl-CoA cannot be turned back into pyruvate, so there is no net path to glucose. Glutamate/glutamine (α-KG), alanine/serine (pyruvate), and aspartate/asparagine (OAA) all enter as glucogenic intermediates and CAN yield net glucose.',
    },
    {
      tag: 'energetics',
      stem: 'After their nitrogen is removed, the carbon skeletons of the 20 amino acids enter central metabolism at how many distinct entry points?',
      choices: [
        'Seven (pyruvate, acetyl-CoA, acetoacetyl-CoA, α-ketoglutarate, succinyl-CoA, fumarate, oxaloacetate)',
        'Two (only pyruvate and acetyl-CoA)',
        'Twenty (one unique entry point per amino acid)',
        'Four (only the TCA-cycle intermediates)',
      ],
      answer: 0,
      rationale:
        'All 20 skeletons funnel into just seven doors: pyruvate, acetyl-CoA, and acetoacetyl-CoA plus the TCA intermediates α-ketoglutarate, succinyl-CoA, fumarate, and oxaloacetate. Grouping by entry point (not memorizing each amino acid) collapses the map — and the entry point, not the amino acid’s identity, determines glucogenic vs ketogenic fate.',
    },
    {
      tag: 'regulation',
      stem: 'Glutamate dehydrogenase is the committed nitrogen-release step. Which allosteric signal ACTIVATES it, matching its physiological job?',
      choices: [
        'ADP/GDP — a low energy charge that signals "burn amino acids for fuel"',
        'ATP/GTP — a high energy charge that signals "fuel is plentiful"',
        'Citrate — signaling that the TCA cycle is saturated',
        'Fructose-2,6-bisphosphate — the glycolytic activator',
      ],
      answer: 0,
      rationale:
        'GDH is allosterically activated by ADP and GDP (low energy charge → the cell needs to catabolize amino acids) and inhibited by ATP and GTP (energy-replete → hold the nitrogen). Citrate and fructose-2,6-bisphosphate regulate other pathways (TCA/lipogenesis and glycolysis) and are not GDH effectors.',
    },
    {
      tag: 'regulation',
      stem: 'Why is transamination itself a poor place to REGULATE flux through amino-acid catabolism?',
      choices: [
        'It runs near equilibrium and reversibly, so it just funnels nitrogen rather than gating it',
        'It irreversibly commits nitrogen to disposal, leaving no room for control',
        'It consumes ATP, which the cell cannot spare for regulation',
        'It occurs only in muscle, where regulation is impossible',
      ],
      answer: 0,
      rationale:
        'Transamination is near-equilibrium and reversible, so nudging it just lets it slide back — it channels nitrogen onto glutamate wherever concentrations push, rather than acting as a throttle. The real control point is the far-from-equilibrium, committed release by glutamate dehydrogenase (and, downstream, CPS-I in the urea cycle).',
    },
    {
      tag: 'integration',
      stem: 'A fasting marathon runner exports alanine from muscle while the liver increases glucose output; a tracer on the alanine nitrogen later appears in urea. Which sequence best describes the nitrogen’s path?',
      choices: [
        'Liver transaminates alanine to pyruvate, nitrogen enters glutamate, GDH releases NH₄⁺, and CPS-I fixes it into the urea cycle',
        'Muscle converts alanine directly to urea and exports it to the kidney',
        'Alanine is oxidized to CO₂ in the liver, releasing its nitrogen as nitrate',
        'Alanine donates its nitrogen to oxaloacetate, forming aspartate that is excreted unchanged',
      ],
      answer: 0,
      rationale:
        'In the glucose–alanine cycle, muscle ships nitrogen to the liver as alanine. Hepatic ALT converts alanine → pyruvate (feeding gluconeogenesis, hence the rising glucose output) and transfers the amino group to α-ketoglutarate → glutamate; GDH then releases NH₄⁺, which CPS-I fixes to begin the urea cycle — so the tracer ends up in urea. Muscle has no urea cycle, nitrogen isn’t excreted as nitrate, and aspartate isn’t excreted intact.',
    },
    {
      tag: 'disease',
      stem: 'A newborn has elevated blood phenylalanine, low tyrosine, a mousy body odor, and developmental delay. Which enzyme is deficient, and what dietary advice follows?',
      choices: [
        'Phenylalanine hydroxylase — restrict phenylalanine, supplement tyrosine, avoid aspartame',
        'Homogentisate oxidase — restrict tyrosine only',
        'Cystathionine β-synthase — supplement high-dose vitamin B₆',
        'Branched-chain α-ketoacid dehydrogenase — restrict isoleucine, leucine, and valine',
      ],
      answer: 0,
      rationale:
        'This is PKU: phenylalanine hydroxylase can’t convert Phe → Tyr, so Phe (and phenylketones) accumulate and injure the developing brain, while tyrosine becomes essential. Management is a low-phenylalanine diet with tyrosine supplementation, and avoiding aspartame (a phenylalanine source). The other enzymes give alkaptonuria, homocystinuria, and MSUD respectively — different metabolites and different diets.',
    },
    {
      tag: 'disease',
      stem: 'A neonate has poor feeding, lethargy, seizures, and urine that smells of maple syrup, with elevated isoleucine, leucine, and valine. Which enzyme is deficient?',
      choices: [
        'Branched-chain α-ketoacid dehydrogenase',
        'Phenylalanine hydroxylase',
        'Glutamate dehydrogenase',
        'Ornithine transcarbamylase',
      ],
      answer: 0,
      rationale:
        'This is maple syrup urine disease (MSUD): branched-chain α-ketoacid dehydrogenase fails to decarboxylate the α-keto acids of Ile, Leu, and Val (after their transamination), so the branched-chain amino acids and their keto acids accumulate — giving the maple-syrup odor and neurotoxicity (leucine is especially toxic). Treatment restricts the branched-chain amino acids. The other enzymes produce PKU, altered ammonia handling, and a urea-cycle disorder, not this pattern.',
    },
  ],
  funFact:
    'Your brain, in a real sense, pays its energy bills with your biceps: during a fast, muscle protein is disassembled, its nitrogen shipped to the liver as harmless alanine, and its carbon rebuilt into the glucose your neurons burn. The bar-tailed godwit runs this to an extreme — it flies ~11,000 km nonstop over the Pacific and, late in the flight, catabolizes its own flight muscle for glucose, for TCA refilling, and even for metabolic water, excreting the leftover nitrogen as uric acid to save every drop.',
};
