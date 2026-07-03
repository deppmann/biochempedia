import type { Pathway } from '../types';

/* =============================================================================
   CALVIN CYCLE — the "dark reactions" (a misnomer twice over: it runs in
   daylight AND it can't run without the light reactions). Hand-authored,
   cross-checked against src/content/lessons/calvin-cycle/lesson.mdx.

   The engine SPENDS ATP + NADPH here — it does NOT make them. Tokens are
   authored per single molecule and are NEGATIVE (consumed). We deliberately
   set `doubleAfter: 0` (no ledger doubling): the "three turns per net G3P"
   accounting is prose, not a fake ×2 gimmick — see netYield and the step facts.
   The real per-CO₂ bill is 3 ATP + 2 NADPH because the reduction stage runs
   twice per CO₂ (two 3-PGA per fixation); we state that in words rather than
   faking a split tile. Six steps across three stages: fixation, reduction,
   regeneration. RuBisCO's carboxylation is the committed, rate-limiting step.
   ============================================================================ */

export const calvinCycle: Pathway = {
  id: 'calvin-cycle',
  name: 'Calvin Cycle',
  emoji: '🌿',
  tagline: 'Eats air, spends the light reactions’ paycheck, builds you out of sky.',
  blurb:
    'The chloroplast’s carbon-welding loop. It cashes in ATP and NADPH from the light reactions to bolt CO₂ onto a 5-carbon sugar, reduce it to a triose, and rebuild the acceptor so the loop never stops. Three turns, three CO₂, one net G3P — the origin of nearly every carbon in your body.',
  difficulty: 2,
  location: 'Chloroplast stroma',
  netYield: '3 CO₂ → 1 net G3P costs 9 ATP + 6 NADPH (spent on carbon, not made). Per CO₂: 3 ATP + 2 NADPH; per hexose: 18 ATP + 12 NADPH.',
  start: 'RuBP + CO₂',
  startShort: 'RuBP + CO₂',
  startEmoji: '🌬️',
  doubleAfter: 0, // NO ledger doubling — the reduction stage runs twice per CO₂; that lives in prose, not a fake ×2
  lessonSlug: 'calvin-cycle',
  steps: [
    {
      n: 1,
      product: '2 × 3-Phosphoglycerate',
      short: '2× 3-PGA',
      enzyme: 'RuBisCO (carboxylation)',
      irreversible: true,
      committed: true,
      emoji: '🐢',
      fact: 'STAGE 1 — Fixation. THE committed, rate-limiting step. RuBP forms a C2–C3 enediol; CO₂ adds at C2 → an unstable 6-carbon intermediate that splits into two 3-PGA. Costs NO ATP or NADPH — the bill comes later. The most abundant protein on Earth, yet notoriously slow (~3 turnovers/sec) and also an oxygenase (photorespiration). Needs a SEPARATE CO₂ as a Lys-201 carbamate + Mg²⁺ to switch on — the activating CO₂ is not the substrate CO₂.',
    },
    {
      n: 2,
      product: '1,3-Bisphosphoglycerate',
      short: '1,3-BPG',
      enzyme: 'Phosphoglycerate kinase',
      tokens: { atp: -1 },
      emoji: '💸',
      fact: 'STAGE 2 — Reduction begins. SPENDS 1 ATP to prime the carboxylate as a mixed anhydride. Glycolysis’ payoff step run in reverse. Runs TWICE per CO₂ (once per 3-PGA), so a full turn spends 2 ATP here.',
    },
    {
      n: 3,
      product: 'Glyceraldehyde-3-phosphate',
      short: 'G3P',
      enzyme: 'G3P dehydrogenase (NADPH)',
      tokens: { nadph: -1 },
      emoji: '🔻',
      fact: 'SPENDS 1 NADPH — the only true reduction in the cycle. NADPH (not NADH!) delivers electrons straight from Photosystem I to build the triose sugar, releasing Pᵢ. Also runs twice per CO₂ → 2 NADPH per turn.',
    },
    {
      n: 4,
      product: 'G3P pool (1 exits, 5 recycle)',
      short: 'G3P → sugar',
      enzyme: 'Triose-phosphate partition',
      emoji: '🍬',
      fact: 'The bookkeeping fork. Three turns make SIX G3P, but only ONE leaves as net product (→ fructose-6-P → hexose → sucrose or starch). The other five (15 carbons) head into regeneration. Miss this and the ledger never balances.',
    },
    {
      n: 5,
      product: 'Ribulose-5-phosphate',
      short: 'Ru5P',
      enzyme: 'Aldolase / transketolase (sugar shuffle)',
      emoji: '🔀',
      fact: 'STAGE 3 — Regeneration. Five G3P (15 C) are reshuffled by aldolase and transketolase, with FBPase & SBPase clipping phosphates, into three 5-carbon ribulose-5-P (15 C — the books balance). The transketolase/aldolase reshuffles are near-equilibrium (reversible); the irreversible, light-activated control points here are the phosphatases FBPase & SBPase.',
    },
    {
      n: 6,
      product: 'Ribulose-1,5-bisphosphate',
      short: 'RuBP',
      enzyme: 'Phosphoribulokinase (PRK)',
      tokens: { atp: -1 },
      irreversible: true,
      emoji: '♻️',
      fact: 'SPENDS the last ATP to rebuild the CO₂ acceptor RuBP, closing the loop. This regeneration ATP (no NADPH) is exactly why the cycle needs ATP and NADPH in a 3:2 ratio, not 1:1. PRK is switched ON by reduced thioredoxin in light, OFF in the dark.',
    },
  ],
  regulators: [
    { name: 'Stromal pH & Mg²⁺', role: 'Light pumps H⁺ into the thylakoid lumen → stromal pH rises ~7→8, and Mg²⁺ flows out into the stroma. Both favor the Lys-201 carbamate → RuBisCO ON. Dark reverses it.' },
    { name: 'Ferredoxin → thioredoxin', role: 'PSI makes reduced ferredoxin → reduced thioredoxin, which breaks a regulatory disulfide on FBPase, SBPase, PRK, and RuBisCO activase → all switch ON in light. At dusk O₂ re-oxidizes thioredoxin → disulfides reform → cycle stalls.' },
    { name: 'RuBisCO activase', role: 'An ATP-burning AAA+ chaperone that pries inhibitory sugar phosphates off RuBisCO so the enzyme can carbamylate and work. Light-activated via thioredoxin.' },
    { name: 'RuBisCO (committed step)', role: 'The rate-limiter. Activated by the CO₂/Mg²⁺ carbamate; competes with O₂ for the active site (oxygenase = photorespiration) — high CO₂ favors carboxylation.' },
  ],
  scenarios: [
    {
      id: 'cc-bright-light',
      emoji: '☀️',
      title: 'High noon, well-watered leaf',
      scene: 'Bright light floods the chloroplast. The light reactions are pumping protons and cranking out ATP and NADPH. Stomata are open, CO₂ is plentiful.',
      hormones: 'Stromal pH ↑ · Mg²⁺ ↑ · thioredoxin reduced',
      flux: 'up',
      decisions: [
        {
          q: 'Which way should the Calvin cycle run right now?',
          choices: ['Ramp UP — fuel and reducing power are abundant', 'Shut DOWN — save the RuBP for later'],
          answer: 0,
          why: 'Light means the light reactions are supplying ATP + NADPH, the two things the cycle spends. Plenty of fuel arriving → fix carbon.',
        },
        {
          q: 'How does light actually switch RuBisCO and its partners ON?',
          choices: [
            'Rising stromal pH + Mg²⁺ favor the Lys-201 carbamate, and reduced thioredoxin unlocks the regulatory enzymes',
            'Light directly binds RuBisCO’s active site as a substrate',
            'ATP allosterically phosphorylates RuBisCO to activate it',
            'CO₂ is only used to build the carbamate, never as substrate',
          ],
          answer: 0,
          why: 'Three stromal signals: pH ~7→8, Mg²⁺ into the stroma, and ferredoxin→thioredoxin reducing disulfides on FBPase, SBPase, PRK, and RuBisCO activase. Light reshapes the surroundings; it never touches the active site directly.',
        },
      ],
      teach: 'LIGHT = ON. The light reactions deliver ATP + NADPH and, through pH/Mg²⁺ shifts and reduced thioredoxin, flip the regulatory enzymes on. The plant wires its sugar factory straight to the sun.',
    },
    {
      id: 'cc-darkness',
      emoji: '🌙',
      title: 'The sun goes down',
      scene: 'Night falls. Photosystem I stops feeding electrons to ferredoxin. No new ATP, no new NADPH is being made by the light reactions.',
      hormones: 'Thioredoxin re-oxidized · pH & Mg²⁺ fall back',
      flux: 'off',
      decisions: [
        {
          q: 'What happens to the Calvin cycle in the dark?',
          choices: [
            'It stalls — no ATP/NADPH to spend, and the enzymes switch off',
            'It speeds up to store carbon for the night',
            'It reverses to make ATP',
            'Nothing changes — it’s the "dark reactions," so darkness is its home',
          ],
          answer: 0,
          why: 'The "dark reactions" name is misleading. In the dark the light reactions quit supplying ATP + NADPH, so the cycle has nothing to spend. It would be wasteful to run — so the plant shuts it off.',
        },
        {
          q: 'Why do FBPase, SBPase, and PRK go quiet at night?',
          choices: [
            'O₂ re-oxidizes thioredoxin → their regulatory disulfides reform → enzymes lock shut',
            'Stromal pH crashes below 5 and denatures them',
            'CO₂ can no longer diffuse into the chloroplast at night',
            'RuBP covalently bonds to the thylakoid membrane',
          ],
          answer: 0,
          why: 'With no reduced ferredoxin, thioredoxin is re-oxidized; its target enzymes reform their disulfides and switch off. pH doesn’t crash to 5, CO₂ diffusion isn’t light-gated, and RuBP doesn’t bond to the membrane.',
        },
      ],
      teach: 'DARK = OFF. No light reactions → no ATP/NADPH and no reduced thioredoxin → the regulatory enzymes lock shut. Running the cycle now would just burn fuel the plant can’t replace.',
    },
    {
      id: 'cc-photorespiration',
      emoji: '💨',
      title: 'Low CO₂, high O₂ inside the leaf',
      scene: 'It’s hot and the leaf has been fixing carbon fast. CO₂ near RuBisCO is dropping while O₂ (a light-reaction byproduct) is climbing. RuBisCO faces a fork.',
      hormones: 'CO₂/O₂ ratio ↓ at the active site',
      flux: 'down',
      decisions: [
        {
          q: 'What does RuBisCO do when O₂ wins its active site?',
          choices: [
            'Acts as an oxygenase → RuBP → one 3-PGA + one 2-phosphoglycolate (wasteful)',
            'Fixes two CO₂ at once for double yield',
            'Makes ATP to compensate',
            'Shuts off permanently until CO₂ returns',
          ],
          answer: 0,
          why: 'RuBisCO’s name ends in "oxygenase" for a reason. With O₂, it splits RuBP into 3-PGA + 2-phosphoglycolate — no carbon fixed, and salvaging the glycolate actually releases CO₂. This is photorespiration.',
        },
        {
          q: 'Which change most directly cuts this carbon loss?',
          choices: [
            'Raise CO₂ at the active site (e.g., a CO₂-concentrating mechanism)',
            'Lower stromal Mg²⁺',
            'Reduce the NADPH supplied by the light reactions',
            'Inhibit RuBisCO activase to keep more enzyme RuBP-bound',
          ],
          answer: 0,
          why: 'Carboxylation and oxygenation compete for the same site, so flooding it with CO₂ tips the balance back toward fixation. Lowering Mg²⁺ or NADPH, or inhibiting activase, just cripples the cycle overall.',
        },
      ],
      teach: 'PHOTORESPIRATION = RuBisCO’s oxygenase side-reaction, worst when CO₂ is low and O₂ is high. It burns carbon and energy for zero sugar. The fix is to raise local CO₂ — exactly what C4 and CAM plants engineer.',
    },
    {
      id: 'cc-hot-dry',
      emoji: '🌵',
      title: 'Hot, dry midday — stomata shut to save water',
      scene: 'A desert afternoon. To avoid drying out, the plant closes its stomata. But now fresh CO₂ can’t get in, internal CO₂ falls, and O₂ builds up — prime conditions for photorespiration.',
      hormones: 'Stomata closed · internal CO₂ ↓ · O₂ ↑',
      flux: 'down',
      decisions: [
        {
          q: 'How do C4 plants (corn, sugarcane) beat photorespiration in the heat?',
          choices: [
            'PEP carboxylase fixes CO₂ in mesophyll cells and concentrates it around RuBisCO in bundle-sheath cells (spatial separation)',
            'Their RuBisCO has mutated away its oxygenase site',
            'They lack RuBisCO entirely and use PEP carboxylase for everything',
            'They run the whole Calvin cycle only at night',
          ],
          answer: 0,
          why: 'C4 = separation in SPACE. PEP carboxylase (high CO₂ affinity, no oxygenase) fixes CO₂ to malate in mesophyll, ships it to bundle-sheath cells, and releases concentrated CO₂ to flood RuBisCO. C4 still has RuBisCO and still runs the Calvin cycle by day.',
        },
        {
          q: 'And CAM plants (cacti, agave, pineapple)?',
          choices: [
            'They separate it in TIME — open stomata at night to store CO₂ as malate, then release it to the cycle by day with stomata shut',
            'They keep stomata open all day like C3 plants',
            'They abandon the Calvin cycle and ferment sugar instead',
            'They fix CO₂ and build glucose entirely at night',
          ],
          answer: 0,
          why: 'CAM = separation in TIME. Capture CO₂ into malate at night (cool, humid, stomata open), then run the Calvin cycle by day behind closed stomata using that stored CO₂ — conserving water. Same 18 ATP + 12 NADPH per glucose.',
        },
      ],
      teach: 'HOT & DRY = closed stomata = a photorespiration trap. C4 pumps CO₂ in SPACE (mesophyll → bundle-sheath); CAM pumps it in TIME (night storage → daytime release). Both lean on PEP carboxylase to concentrate CO₂ around RuBisCO.',
    },
  ],
  diseases: [
    {
      id: 'cc-no-light',
      name: 'Chloroplast troubleshooting · the cycle stalls in the dark',
      emoji: '🌑',
      vignette:
        'A chloroplast prep was fixing ¹⁴CO₂ happily in the light. Moved into complete darkness, net CO₂ fixation halts within minutes even though CO₂ is still present. Which process is the culprit?',
      suspects: [
        'Loss of light reactions → no ATP/NADPH and thioredoxin re-oxidizes (enzymes off)',
        'RuBisCO denatured by a stromal pH crash to below 5',
        'CO₂ can no longer diffuse into the chloroplast in the dark',
        'RuBP became covalently bonded to the thylakoid membrane',
      ],
      answer: 0,
      accumulates: 'Whatever RuBP/intermediates remain, unspent — the cycle simply stops',
      missing: 'ATP + NADPH (the light reactions’ output) and reduced thioredoxin',
      teach:
        'The Calvin cycle spends ATP + NADPH but makes neither. In the dark the light reactions stop supplying them, and reduced ferredoxin disappears, so thioredoxin is re-oxidized and FBPase/SBPase/PRK/RuBisCO activase reform their disulfides and switch off. The stroma also loses its light-driven pH and Mg²⁺ shifts. CO₂ diffusion isn’t light-gated, pH doesn’t crash to 5, and RuBP doesn’t bond the membrane.',
      pearl: 'The "dark reactions" cannot run in the dark — they run on the light reactions’ paycheck (ATP + NADPH) and the thioredoxin light-switch.',
    },
    {
      id: 'cc-photorespiration',
      name: 'Chloroplast troubleshooting · O₂ high, CO₂ low',
      emoji: '💨',
      vignette:
        'On a hot afternoon the leaf is losing fixed carbon and making 2-phosphoglycolate. Internal CO₂ is low and O₂ is high. Which side-reaction is bleeding the plant’s carbon?',
      suspects: [
        'RuBisCO’s oxygenase reaction (photorespiration)',
        'Phosphoribulokinase spending too much ATP',
        'G3P dehydrogenase running in reverse',
        'PEP carboxylase over-fixing CO₂',
      ],
      answer: 0,
      accumulates: '2-Phosphoglycolate (from the oxygenase reaction) → salvage even releases CO₂',
      missing: 'Fixed carbon / net sugar — no G3P gained from that turn',
      teach:
        'RuBisCO is a carboxylase AND an oxygenase competing for the same active site. When CO₂ is low and O₂ is high, O₂ wins and RuBP is split into one 3-PGA + one 2-phosphoglycolate — no carbon fixed, and salvaging the glycolate releases CO₂. On a scorching day a plant can lose ~a quarter of its fixed carbon this way. Raising local CO₂ (C4/CAM) is the fix.',
      pearl: 'Photorespiration = RuBisCO grabs O₂ instead of CO₂ → 2-phosphoglycolate, wasted carbon and energy; high CO₂ suppresses it.',
    },
    {
      id: 'cc-hot-dry-stomata',
      name: 'Chloroplast troubleshooting · hot, dry, stomata shut',
      emoji: '🌵',
      vignette:
        'A desert plant thrives at midday heat with almost no photorespiration, despite closed stomata. Its neighbor, an ordinary C3 plant, wilts and loses carbon. What adaptation explains the desert plant’s success?',
      suspects: [
        'A CO₂-concentrating mechanism (C4 spatial or CAM temporal) using PEP carboxylase',
        'A RuBisCO that has lost its oxygenase active site',
        'Running glycolysis instead of the Calvin cycle',
        'Fixing carbon without any RuBisCO at all',
      ],
      answer: 0,
      accumulates: 'Malate (the 4-carbon CO₂ shuttle/store made by PEP carboxylase)',
      missing: 'Nothing productive — the adaptation PREVENTS the carbon loss C3 plants suffer',
      teach:
        'When stomata close to save water, internal CO₂ drops and O₂ rises — a photorespiration trap. C4 plants (corn, sugarcane) separate fixation in SPACE: PEP carboxylase fixes CO₂ to malate in mesophyll, shuttles it to bundle-sheath cells, and floods RuBisCO with concentrated CO₂. CAM plants (cacti, agave, pineapple) separate it in TIME: fix CO₂ into malate at night, release it to the Calvin cycle by day behind shut stomata. Both still use RuBisCO and the Calvin cycle; they just pre-concentrate CO₂.',
      pearl: 'C4 = CO₂ pump in space (mesophyll→bundle-sheath); CAM = CO₂ pump in time (night store→day release). PEP carboxylase does the initial fixing in both.',
    },
  ],
  quiz: [
    {
      tag: 'energetics',
      stem: 'Per CO₂ fixed by the Calvin cycle, what is the correct consumption of ATP and NADPH?',
      choices: [
        'Consumes 3 ATP and 2 NADPH',
        'Produces 3 ATP and 2 NADPH',
        'Consumes 2 ATP and 3 NADPH',
        'Consumes 1 ATP and 1 NADPH',
      ],
      answer: 0,
      rationale:
        'The cycle SPENDS ATP + NADPH (it makes neither). Reduction uses ATP:NADPH 1:1, but regeneration (phosphoribulokinase) spends an extra ATP with no NADPH, tipping the per-CO₂ total to 3 ATP + 2 NADPH. Per hexose that scales to 18 ATP + 12 NADPH.',
    },
    {
      tag: 'energetics',
      stem: 'Why does the Calvin cycle consume ATP and NADPH in a 3:2 ratio rather than 1:1 per CO₂?',
      choices: [
        'An extra ATP is spent during regeneration (phosphoribulokinase) beyond the 1:1 used in reduction',
        'The reduction stage uses two ATP for every NADPH',
        'Fixation by RuBisCO itself consumes one ATP per CO₂',
        'NADPH is partially recycled, lowering its apparent count',
      ],
      answer: 0,
      rationale:
        'Reduction (PGA kinase + G3P dehydrogenase) uses ATP and NADPH 1:1. Regeneration then spends additional ATP — notably at phosphoribulokinase — with no NADPH, tipping the per-CO₂ total to 3:2. Fixation by RuBisCO costs neither ATP nor NADPH, and NADPH is not recycled within the cycle.',
    },
    {
      tag: 'basics',
      stem: 'Which enzyme catalyzes the committed, rate-limiting carboxylation step of the Calvin cycle, and what does it produce?',
      choices: [
        'RuBisCO — RuBP + CO₂ → two molecules of 3-phosphoglycerate',
        'Phosphoribulokinase — ribulose-5-P + ATP → RuBP',
        'G3P dehydrogenase — 1,3-BPG + NADPH → G3P',
        'PEP carboxylase — PEP + CO₂ → oxaloacetate',
      ],
      answer: 0,
      rationale:
        'RuBisCO carboxylates RuBP: CO₂ adds to a C2–C3 enediol, forming an unstable 6-carbon intermediate that splits into two 3-PGA. This is the committed, rate-limiting step and it costs no ATP or NADPH. Phosphoribulokinase, G3P dehydrogenase, and PEP carboxylase run elsewhere (or in C4/CAM).',
    },
    {
      tag: 'basics',
      stem: 'A student is told RuBisCO "needs CO₂ to work but also fixes CO₂." Which statement resolves this correctly?',
      choices: [
        'One CO₂ forms a carbamate on Lys-201 that binds Mg²⁺ to activate the enzyme; a different CO₂ is the substrate fixed onto RuBP',
        'The activating CO₂ is fixed first, then transferred to RuBP',
        'Both CO₂ molecules are reduced by NADPH to form sugar',
        'CO₂ binds only the small regulatory subunits and never the active site',
      ],
      answer: 0,
      rationale:
        'A separate CO₂ reacts with Lys-201 on the large subunit to form a carbamate that chelates Mg²⁺ and builds the catalytic site. The substrate CO₂ then adds to the RuBP enediol at C2. Confusing the activating and substrate CO₂ is the classic error; NADPH reduces 1,3-BPG, not CO₂ directly.',
    },
    {
      tag: 'basics',
      stem: 'Three turns of the Calvin cycle fix three CO₂ and produce six G3P, yet only one G3P is counted as the net product. What becomes of the other five?',
      choices: [
        'They are reshuffled by aldolase and transketolase to regenerate three molecules of RuBP',
        'They are oxidized back to CO₂ to drive regeneration',
        'They are exported as sucrose immediately',
        'They are reduced further to glucose inside the stroma',
      ],
      answer: 0,
      rationale:
        'Five G3P (15 carbons) are rearranged by aldolase and transketolase, with FBPase/SBPase and phosphoribulokinase, into three 5-carbon RuBP (15 carbons) to regenerate the acceptor. Carbon is conserved, not oxidized to CO₂. Only the single net G3P leaves to build hexose.',
    },
    {
      tag: 'regulation',
      stem: 'An actively photosynthesizing chloroplast is moved from light into complete darkness. Which change best explains why the Calvin cycle stalls within minutes?',
      choices: [
        'Oxygen re-oxidizes thioredoxin, reforming disulfides that inactivate FBPase, SBPase, PRK, and RuBisCO activase',
        'CO₂ can no longer diffuse into the chloroplast in the dark',
        'Stromal pH drops below 5, denaturing RuBisCO',
        'RuBP becomes covalently bonded to the thylakoid membrane',
      ],
      answer: 0,
      rationale:
        'In the dark the light reactions stop making reduced ferredoxin, so thioredoxin is re-oxidized; its target enzymes reform their regulatory disulfides and switch off. The stroma also loses its light-driven pH and Mg²⁺ shifts. CO₂ diffusion is not light-gated, pH does not crash to 5, and RuBP does not bond the membrane.',
    },
    {
      tag: 'regulation',
      stem: 'Which set of stromal changes accompanies illumination and activates the Calvin cycle?',
      choices: [
        'Stromal pH rises (~7→8), Mg²⁺ rises, and thioredoxin is reduced',
        'Stromal pH falls, Mg²⁺ falls, and thioredoxin is oxidized',
        'Stromal pH rises, Mg²⁺ falls into the thylakoid lumen, and thioredoxin is oxidized',
        'Only ATP levels change; pH, Mg²⁺, and thioredoxin are irrelevant',
      ],
      answer: 0,
      rationale:
        'Light pumps H⁺ into the thylakoid lumen, raising stromal pH from ~7 to ~8; Mg²⁺ flows out of the lumen into the stroma to balance charge; and PSI-driven reduced ferredoxin generates reduced thioredoxin. The pH/Mg²⁺ shift favors the Lys-201 carbamate, and thioredoxin switches on the regulatory enzymes.',
    },
    {
      tag: 'disease',
      stem: 'On a hot day a C3 leaf closes its stomata to conserve water. Why does this drive carbon loss through photorespiration?',
      choices: [
        'Closed stomata lower internal CO₂ and raise O₂, so RuBisCO’s oxygenase reaction wins → RuBP → 3-PGA + 2-phosphoglycolate',
        'Closed stomata trap heat that denatures RuBisCO into an oxygenase',
        'Closed stomata block ATP export, forcing the cycle to burn RuBP',
        'Closed stomata acidify the stroma, activating photorespiration enzymes',
      ],
      answer: 0,
      rationale:
        'With stomata shut, fresh CO₂ can’t enter, internal CO₂ falls, and O₂ (a light-reaction byproduct) builds up. O₂ then out-competes CO₂ at RuBisCO’s active site, and the oxygenase reaction makes one 3-PGA plus one 2-phosphoglycolate — no carbon fixed, and salvage even releases CO₂.',
    },
    {
      tag: 'integration',
      stem: 'A mutant RuBisCO shows a markedly increased oxygenase-to-carboxylase ratio at a given CO₂/O₂. Holding light and temperature constant, which intervention most directly reduces the plant’s carbon loss to photorespiration?',
      choices: [
        'Raising the CO₂ concentration at the active site (e.g., a CO₂-concentrating mechanism)',
        'Lowering the stromal Mg²⁺ concentration',
        'Decreasing the NADPH supplied by the light reactions',
        'Inhibiting RuBisCO activase to keep more enzyme RuBP-bound',
      ],
      answer: 0,
      rationale:
        'Carboxylation and oxygenation compete for the same active site, so raising local CO₂ (as C4/CAM mechanisms do) shifts the balance toward carboxylation and cuts photorespiratory loss. Lowering Mg²⁺ impairs carbamylation; cutting NADPH starves reduction; inhibiting activase leaves RuBisCO RuBP-locked and inactive.',
    },
    {
      tag: 'integration',
      stem: 'Two desert plants: Plant X opens stomata only at night, fixing CO₂ into malate it stores and decarboxylates by day with stomata shut. Plant Y keeps stomata open by day and uses separate mesophyll and bundle-sheath cells. Which statement is correct?',
      choices: [
        'Plant X uses CAM (temporal separation) and Plant Y uses C4 (spatial separation); both rely on PEP carboxylase for the initial fixation',
        'Plant X is C4 and conserves water by separating fixation in space',
        'Both avoid RuBisCO entirely and fix all carbon with PEP carboxylase',
        'Plant Y conserves more water than Plant X because it keeps stomata closed at night',
      ],
      answer: 0,
      rationale:
        'Night capture into malate with daytime decarboxylation behind closed stomata is CAM (temporal separation). Mesophyll/bundle-sheath spatial separation is C4. Both use PEP carboxylase for the initial fixation and both still run the Calvin cycle (and RuBisCO). Plant Y (C4) keeps stomata open by day, so it does not out-conserve the night-fixing CAM plant on water.',
    },
  ],
  funFact:
    'RuBisCO is the most abundant protein on Earth and pulls roughly 100 billion tons of carbon out of the air every year — yet each copy fixes only about three CO₂ molecules per second. The entire global food supply runs on the slowest famous enzyme in biology, and plants compensate by making so much of it that it’s about a quarter of all the protein in a leaf.',
};
