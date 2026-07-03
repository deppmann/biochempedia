import type { Pathway } from '../types';

/* =============================================================================
   OXIDATIVE PHOSPHORYLATION (ETC) — hand-authored, cross-checked against
   src/content/lessons/oxidative-phosphorylation/lesson.mdx. This is NOT a
   metabolite-conversion pathway; Build mode asks the player to ORDER the
   electron carriers by increasing reduction potential (E0'), i.e. the
   direction electrons actually flow: NADH/FADH₂ → Complex I → CoQ →
   Complex III → cytochrome c → Complex IV → O₂, with ATP synthase (Complex V)
   as the machine that finally spends the gradient.

   The two-machines idea is the whole point: electron flow and ATP synthesis
   are physically separate, linked only by the proton gradient (Mitchell's
   chemiosmotic coupling). So ATP accounting is kept CONCEPTUAL — no invented
   per-carrier ATP integers, which would mislead. The real numbers
   (~2.5 ATP/NADH, ~1.5/FADH₂, ~4 H⁺/ATP, ~10 vs ~6 H⁺ banked) live in the
   ATP-synthase step's fact and in netYield. doubleAfter: 0 — nothing doubles.
   ============================================================================ */

export const oxidativePhosphorylation: Pathway = {
  id: 'oxidative-phosphorylation',
  name: 'Oxidative Phosphorylation (ETC)',
  emoji: '🏭',
  tagline: 'Two machines, one battery: drop electrons to charge it, flood protons back to cash it.',
  blurb:
    'Electrons fall from NADH and FADH₂ down a five-story redox ladder to O₂. Three of the drops pump protons across the inner membrane, building a gradient; ATP synthase then spends that gradient to mint ATP. Electron flow and ATP-making are separate machines linked only by the proton-motive force — get that, and cyanide, uncouplers, and the FADH₂ tax all make sense.',
  difficulty: 3,
  location: 'Inner mitochondrial membrane',
  netYield: '~2.5 ATP per NADH, ~1.5 per FADH₂ · ~26–28 ATP per glucose from OxPhos (~30–32 total, incl. 4 substrate-level)',
  start: 'NADH / FADH₂ (electrons in)',
  startShort: 'NADH / FADH₂',
  startEmoji: '🔋',
  doubleAfter: 0, // electron flow — nothing splits, nothing doubles
  lessonSlug: 'oxidative-phosphorylation',
  steps: [
    {
      n: 1,
      product: 'Complex I — NADH-Q oxidoreductase',
      short: 'Complex I',
      enzyme: 'Complex I (NADH dehydrogenase)',
      irreversible: true,
      emoji: '🅰️',
      fact: 'The NADH entry point (E0′ ≈ −0.32 V, the penthouse). NADH hands 2 e⁻ to FMN → a relay of ~7 Fe–S clusters → coenzyme Q. A steep drop: pumps ~4 H⁺. Blocked by rotenone. (FADH₂ enters LOWER, via Complex II — see Complex II.)',
    },
    {
      n: 2,
      product: 'Coenzyme Q / ubiquinone',
      short: 'CoQ',
      enzyme: 'Coenzyme Q (mobile lipid carrier)',
      emoji: '🛶',
      fact: 'A small lipid-soluble carrier (E0′ ≈ +0.04 V) that diffuses IN the membrane. It is the common collection point: it accepts electrons from BOTH Complex I (from NADH) and Complex II (from FADH₂/succinate), then ferries them to Complex III as QH₂.',
    },
    {
      n: 3,
      product: 'Complex III — cytochrome bc₁',
      short: 'Complex III',
      enzyme: 'Complex III (cytochrome bc₁)',
      irreversible: true,
      emoji: '🔁',
      fact: 'Runs the Q cycle: QH₂ carries 2 e⁻ but cytochrome c takes only 1 at a time, so it "makes change" — one e⁻ out via the Rieske Fe–S, one looped back through the b hemes. Nets 4 H⁺ pumped. Its lingering semiquinone (Q•⁻) is a top superoxide source. Blocked by antimycin A.',
    },
    {
      n: 4,
      product: 'Cytochrome c',
      short: 'Cyt c',
      enzyme: 'Cytochrome c (mobile carrier)',
      emoji: '🚌',
      fact: 'The shuttle bus (E0′ ≈ +0.25 V). A small, water-soluble single-heme protein loosely bound to the OUTER (intermembrane-space) face of the inner membrane. Not built into a complex — it carries ONE electron at a time from Complex III to Complex IV.',
    },
    {
      n: 5,
      product: 'Complex IV — cytochrome c oxidase',
      short: 'Complex IV',
      enzyme: 'Complex IV (cytochrome c oxidase)',
      tokens: { co2: 0 }, // no CO₂ here — placeholder kept minimal; water is the product, tracked in fact
      irreversible: true,
      committed: true,
      emoji: '💧',
      fact: 'The terminal oxidase and the point of no return: e⁻ pass cyt c → CuA → heme a → the heme a₃/CuB binuclear center, where O₂ (E0′ ≈ +0.82 V, the basement) is reduced to 2 H₂O. The "vise grip" clamps O₂ until all 4 e⁻ arrive so no ROS escape. Per O₂: 8 H⁺ removed (4 pumped, 4 into water). Blocked by cyanide & CO.',
    },
    {
      n: 6,
      product: 'ATP synthase (Complex V) mints ATP',
      short: 'ATP synthase',
      enzyme: 'ATP synthase (Complex V)',
      tokens: { atp: 1 }, // conceptual: the gradient is finally spent as ATP here
      emoji: '⚙️',
      fact: 'The SECOND machine. Protons flood back through it (~4 H⁺/ATP, including the cost of exporting ATP + importing ADP/Pi). NADH banks ~10 H⁺ → ~2.5 ATP; FADH₂ banks only ~6 H⁺ → ~1.5 ATP, because it skipped Complex I. A rotary motor at ~400 ATP/s. Blocked by oligomycin.',
    },
  ],
  regulators: [
    {
      name: 'ADP (acceptor / respiratory control)',
      role: 'THE primary throttle. High ADP (energy spent) speeds respiration; high ATP / low ADP slows it. The chain runs only as fast as ATP synthase draws down the gradient — no ADP to phosphorylate, gradient builds, back-pressure stalls the pumps.',
    },
    {
      name: 'Proton-motive force (the gradient itself)',
      role: 'The coupling currency. A steep gradient back-pressures the pumps and slows electron flow; discharging it (by making ATP, or by a leak) relieves the pressure and lets the chain run faster.',
    },
    {
      name: 'O₂ (terminal electron acceptor)',
      role: 'No O₂ at Complex IV = nowhere for electrons to fall. The whole chain backs up reduced, the gradient collapses, and OxPhos stops. This is why hypoxia and cyanide are functionally the same failure.',
    },
    {
      name: 'Uncouplers (2,4-DNP, thermogenin/UCP1)',
      role: 'Poke a proton leak in the membrane. Protons return WITHOUT passing ATP synthase, so the fall comes out as heat, not ATP. Respiration SPEEDS UP (no back-pressure) while ATP output collapses. Brown fat does this on purpose.',
    },
    {
      name: 'Inhibitors (rotenone, antimycin A, cyanide, oligomycin)',
      role: 'Freeze the chain at one point. Rotenone → CI, antimycin A → CIII, cyanide/CO → CIV, oligomycin → ATP synthase. Everything upstream of a block piles up reduced; everything downstream goes oxidized (the crossover pattern).',
    },
  ],
  scenarios: [
    {
      id: 'oxphos-exercise',
      emoji: '🏋️',
      title: 'Mid-workout — muscle is burning ATP fast',
      scene:
        'Contracting muscle is hydrolyzing ATP faster than at rest, so ADP is piling up in the matrix. Oxygen is still available. The mitochondria need to keep pace.',
      hormones: 'ADP ↑ · ATP:ADP ratio ↓',
      flux: 'up',
      decisions: [
        {
          q: 'What happens to the rate of electron transport?',
          choices: [
            'Speeds up — rising ADP drives faster respiration',
            'Slows down — high demand shuts the chain off',
            'Unchanged — the ETC always runs at a fixed rate',
          ],
          answer: 0,
          why: 'This is acceptor (respiratory) control. ADP is the acceptor for ATP synthase; more ADP means the synthase discharges the gradient faster, relieving back-pressure so the pumps — and electron flow — accelerate.',
        },
        {
          q: 'WHY does electron flow track ADP so tightly?',
          choices: [
            'ATP synthase discharging the gradient relieves back-pressure on the pumps',
            'ADP binds Complex I directly and pushes electrons faster',
            'ADP is oxidized by Complex IV in place of O₂',
          ],
          answer: 0,
          why: 'Electron flow and ATP synthesis are coupled ONLY through the gradient. When ADP lets synthase spend the gradient, the proton-motive force drops, the pumps face less back-pressure, and the chain runs faster. No direct ADP–ETC contact needed.',
        },
      ],
      teach:
        'ACCEPTOR CONTROL: oxidative phosphorylation is demand-driven. The chain does not run flat-out and store ATP; it idles until ADP appears, then matches output to need. The proton gradient is the mechanical link — spending it (via ATP synthase) is what lets the pumps and electron flow speed up.',
    },
    {
      id: 'oxphos-rest',
      emoji: '🛋️',
      title: 'Resting quietly — ATP is plentiful',
      scene:
        'You are sitting still. Little ATP is being spent, so ADP is scarce and ATP is abundant in the matrix. Fuel and O₂ are available.',
      hormones: 'ATP ↑ · ADP ↓',
      flux: 'down',
      decisions: [
        {
          q: 'What is the ETC doing right now?',
          choices: [
            'Idling — with little ADP, the gradient builds and back-pressure slows the pumps',
            'Racing — it always runs at maximum when fuel is present',
            'Fully off — no electrons move at all until you move',
          ],
          answer: 0,
          why: 'Low ADP means ATP synthase has little to phosphorylate, so it barely discharges the gradient. The proton-motive force stays high and back-pressures the pumps, throttling electron flow down to a trickle — but not zero.',
        },
        {
          q: 'What would happen if you added an uncoupler like 2,4-DNP here?',
          choices: [
            'Electron flow would SPEED UP even though ATP output falls',
            'Electron flow would stop because the gradient is gone',
            'Nothing — the chain is already at rest',
          ],
          answer: 0,
          why: 'An uncoupler leaks protons back without passing ATP synthase, removing the back-pressure that was throttling the resting chain. Respiration accelerates and the energy comes out as heat, while ATP synthesis collapses.',
        },
      ],
      teach:
        'REST = high ATP, low ADP → gradient builds → back-pressure throttles the pumps. This is the mirror image of exercise. Note the key insight: a full gradient SLOWS respiration. That is why an uncoupler (which drains the gradient) paradoxically makes a resting mitochondrion breathe harder — as heat, not ATP.',
    },
    {
      id: 'oxphos-cyanide',
      emoji: '☠️',
      title: 'Cyanide exposure',
      scene:
        'A patient inhaled cyanide. Cyanide binds the heme a₃/CuB center of Complex IV. Within minutes they are in crisis despite breathing air normally.',
      hormones: 'n/a — a chemical block, not a hormone signal',
      flux: 'off',
      decisions: [
        {
          q: 'What is the direct effect of blocking Complex IV?',
          choices: [
            'Electrons can’t reach O₂, so the whole chain backs up reduced and the gradient collapses',
            'O₂ is consumed too fast and runs out',
            'ATP synthase runs backward and pumps protons out',
          ],
          answer: 0,
          why: 'Complex IV is the only exit for electrons onto O₂. Block it and every upstream carrier saturates in the reduced state, no more protons are pumped, the proton-motive force dissipates, and oxidative ATP synthesis stops.',
        },
        {
          q: 'Why is a cell "suffocating surrounded by air"?',
          choices: [
            'O₂ is present but cannot be used — the chain can’t hand electrons to it',
            'Cyanide chemically consumes all the O₂ in the blood',
            'Cyanide blocks the lungs from absorbing O₂',
          ],
          answer: 0,
          why: 'O₂ is abundant; the problem is that Complex IV can no longer transfer electrons to it. Oxygen delivery is fine — oxygen USE is dead. That is why cyanide poisoning presents with high venous O₂: the tissues can’t extract it.',
        },
      ],
      teach:
        'Cyanide (and CO) jam the terminal oxidase. The lethal event is loss of the gradient: with no electron exit, the chain saturates reduced, pumping stops, the proton-motive force collapses, and ATP synthase loses its driving force. Cells that live on oxidative ATP fail in minutes — not because O₂ is gone, but because it can’t be used.',
    },
    {
      id: 'oxphos-brownfat',
      emoji: '🐻',
      title: 'A cold newborn (or a hibernating bear) warming up',
      scene:
        'Body temperature is dropping. Brown adipose tissue, packed with mitochondria, switches on its uncoupling protein (UCP1 / thermogenin) to generate heat instead of ATP.',
      hormones: 'Norepinephrine ↑ → UCP1 activated',
      flux: 'up',
      decisions: [
        {
          q: 'What does UCP1 (thermogenin) do to the inner membrane?',
          choices: [
            'Opens a regulated proton leak, letting protons bypass ATP synthase',
            'Blocks Complex IV so electrons can’t reach O₂',
            'Directly hydrolyzes ATP to release heat',
          ],
          answer: 0,
          why: 'UCP1 is a controlled, physiological uncoupler. It lets protons flow back into the matrix without turning ATP synthase, so the energy of the gradient is released as heat.',
        },
        {
          q: 'With UCP1 open, what happens to electron transport and ATP output?',
          choices: [
            'Electron flow rises (no back-pressure); ATP output falls; heat rises',
            'Both electron flow and ATP synthesis stop',
            'ATP output rises because the chain runs faster',
          ],
          answer: 0,
          why: 'Draining the gradient removes back-pressure, so the pumps and electron flow speed up and burn fuel fast — but with protons bypassing the synthase, that energy becomes heat, not ATP. This is non-shivering thermogenesis.',
        },
      ],
      teach:
        'Brown fat is a purpose-built uncoupler. UCP1 does deliberately what the poison 2,4-DNP does lethally: short-circuit the battery so its charge dissipates as heat. Same physics — respiration speeds up, ATP collapses — but here it keeps a newborn or a hibernator alive.',
    },
    {
      id: 'oxphos-reperfusion',
      emoji: '🫀',
      title: 'Reperfusion after a heart attack',
      scene:
        'During ischemia the ETC backed up: NADH and FADH₂ accumulated with no O₂ to accept their electrons, so the carriers sat highly reduced for hours. Now blood flow — and O₂ — is suddenly restored.',
      hormones: 'n/a — the danger is chemical (a ROS burst)',
      flux: 'up',
      decisions: [
        {
          q: 'What happens the instant O₂ floods back onto the reduced chain?',
          choices: [
            'Backed-up electrons dump onto O₂ all at once, producing a burst of superoxide (ROS)',
            'The chain smoothly restarts with no side effects',
            'ATP synthase reverses and destroys the cell’s ATP',
          ],
          answer: 0,
          why: 'Highly reduced carriers with nowhere to have sent their electrons suddenly meet a flood of O₂. The uncontrolled, one-electron reduction of O₂ makes superoxide, mostly at Complex I and the Complex III semiquinone, overwhelming defenses.',
        },
        {
          q: 'Which intervention most directly targets this mechanism?',
          choices: [
            'A mitochondria-targeted antioxidant to neutralize superoxide as O₂ returns',
            'A drug that speeds ATP synthase to use up the electrons',
            'Adding more O₂ to fully oxidize the chain faster',
          ],
          answer: 0,
          why: 'Reperfusion injury is a radical burst, so scavenging the superoxide at its source (Complexes I and III) is the direct fix. Accelerating ATP synthase or adding O₂ does nothing about the ROS — and more O₂ can feed the burst.',
        },
      ],
      teach:
        'The most dangerous hours after an MI or stroke are caused by O₂ RETURNING. A chain frozen reduced during ischemia dumps its queued electrons onto O₂ in a ROS tsunami on reperfusion. Therapies attack the chemistry: gradual reperfusion, therapeutic hypothermia to slow the chain, and mitochondria-targeted antioxidants.',
    },
  ],
  diseases: [
    {
      id: 'cyanide-co',
      name: 'Cyanide / carbon monoxide poisoning (Complex IV)',
      emoji: '☠️',
      vignette:
        'A firefighter pulled from a smoke-filled building is confused and hypotensive, breathing air, yet deteriorating fast. Arterial O₂ is normal — but VENOUS O₂ is strikingly HIGH: the tissues aren’t extracting oxygen. Lactate is climbing.',
      suspects: ['Complex IV (cytochrome c oxidase)', 'Complex I (NADH dehydrogenase)', 'Complex III (cytochrome bc₁)', 'ATP synthase (Complex V)'],
      answer: 0,
      accumulates: 'Reduced upstream carriers (whole chain backs up); lactate (cells fall back on glycolysis)',
      missing: 'Oxidative ATP — electrons can’t reach O₂',
      teach:
        'Cyanide and CO jam the heme a₃/CuB center of Complex IV, the terminal oxidase. Electrons can no longer reach O₂, so the entire chain saturates reduced, proton pumping stops, the gradient collapses, and ATP synthase loses its driving force. O₂ is present but unusable — hence high venous O₂ — and cells crash to glycolysis, spilling lactate.',
      pearl: 'Cyanide/CO = Complex IV block → high venous O₂ + lactic acidosis. The cell suffocates surrounded by air.',
    },
    {
      id: 'rotenone',
      name: 'Rotenone toxicity (Complex I)',
      emoji: '🐟',
      vignette:
        'A worker handling a rotenone-based pesticide (also a classic fish poison) develops fatigue and lactic acidosis. In cultured cells, NADH-linked substrates no longer drive respiration, but adding succinate partially restores O₂ consumption.',
      suspects: ['Complex I (NADH dehydrogenase)', 'Complex IV (cytochrome c oxidase)', 'Coenzyme Q', 'Cytochrome c'],
      answer: 0,
      accumulates: 'NADH and the Complex I Fe–S clusters (reduced); everything downstream goes oxidized',
      missing: 'Electron entry from NADH into the chain',
      teach:
        'Rotenone blocks Complex I, so electrons from NADH can’t reach coenzyme Q. NADH-fed respiration stops. The tell-tale rescue: adding SUCCINATE feeds electrons in at Complex II (below the block), restoring flow to CoQ and O₂ — proof the block is at Complex I specifically, not further down.',
      pearl: 'Rotenone = Complex I block. Succinate (Complex II entry) bypasses it and rescues respiration — a classic crossover experiment.',
    },
    {
      id: 'oligomycin',
      name: 'Oligomycin (ATP synthase block)',
      emoji: '⚙️',
      vignette:
        'In isolated respiring mitochondria, adding oligomycin sharply SLOWS O₂ consumption. Then an uncoupler (2,4-DNP) is added and O₂ consumption ROARS back — but no ATP is made.',
      suspects: ['ATP synthase (Complex V)', 'Complex I (NADH dehydrogenase)', 'Complex IV (cytochrome c oxidase)', 'Complex III (cytochrome bc₁)'],
      answer: 0,
      accumulates: 'Protons in the intermembrane space (a steep, un-discharged gradient)',
      missing: 'ATP — the gradient can’t be spent through the synthase',
      teach:
        'Oligomycin plugs ATP synthase, so protons can’t flow back through it. The gradient piles up and its back-pressure stalls the pumps, slowing electron transport — a beautiful demonstration that flow and phosphorylation are COUPLED via the gradient. Adding an uncoupler drains the gradient another way, so respiration races again (as heat) even though ATP is still zero.',
      pearl: 'Oligomycin blocks ATP synthase → gradient builds → respiration slows. An uncoupler restores respiration but NOT ATP — proving the two machines are linked only by the gradient.',
    },
    {
      id: 'dnp-uncoupling',
      name: '2,4-Dinitrophenol (DNP) uncoupling',
      emoji: '🔥',
      vignette:
        'Someone took DNP as an illicit "fat-burner." They present with dangerous hyperthermia, drenching sweat, tachycardia, and rising lactate. O₂ consumption is markedly elevated, yet they are ATP-starved.',
      suspects: ['Uncoupling — a proton leak across the inner membrane (mechanism, not an enzyme deficiency)', 'Complex IV (cytochrome c oxidase)', 'ATP synthase (Complex V)', 'Complex I (NADH dehydrogenase)'],
      answer: 0,
      accumulates: 'Nothing upstream — electrons flow FAST; instead the gradient is continuously dissipated as heat',
      missing: 'ATP — the proton-motive force is short-circuited before ATP synthase can use it',
      teach:
        'DNP is a lipophilic weak acid that ferries protons straight across the inner membrane, bypassing ATP synthase. The gradient can’t build, so ATP output collapses; with the back-pressure gone, electron transport (and O₂ use) accelerates and the released energy becomes HEAT — hence the lethal hyperthermia. This is exactly what UCP1 does on purpose in brown fat.',
      pearl: 'Uncoupler = high respiration + high heat + LOW ATP. DNP killed dieters; UCP1/thermogenin is the body’s safe version.',
    },
  ],
  quiz: [
    {
      tag: 'basics',
      stem: 'In Mitchell’s chemiosmotic model, where is the energy from electron transport stored before ATP synthase uses it?',
      choices: [
        'As a proton gradient (proton-motive force) across the inner mitochondrial membrane',
        'In a high-energy phosphorylated chemical intermediate that hands its bond to ADP',
        'In the reduced cytochrome c pool waiting at Complex IV',
        'As heat that the inner membrane later recaptures',
      ],
      answer: 0,
      rationale:
        'Chemiosmotic coupling stores the energy as an electrochemical proton gradient across the impermeable inner membrane; ATP synthase then discharges it. The elusive "high-energy chemical intermediate" was the rejected chemical-coupling hypothesis — it was never found. Reduced cytochrome c carries electrons, not the coupling energy, and heat is what an uncoupler WASTES the gradient as.',
    },
    {
      tag: 'basics',
      stem: 'The electron carriers are arranged in the order electrons actually flow. Which sequence is correct from NADH to O₂?',
      choices: [
        'Complex I → CoQ → Complex III → cytochrome c → Complex IV → O₂',
        'Complex I → cytochrome c → Complex III → CoQ → Complex IV → O₂',
        'Complex III → Complex I → CoQ → Complex IV → cytochrome c → O₂',
        'Complex I → CoQ → Complex II → cytochrome c → Complex IV → O₂',
      ],
      answer: 0,
      rationale:
        'Electrons flow by increasing reduction potential: Complex I hands them to the mobile lipid carrier CoQ, CoQ to Complex III, Complex III to the mobile carrier cytochrome c, cytochrome c to Complex IV, and Complex IV to O₂. Complex II is a side-door FEEDER into CoQ (from succinate/FADH₂), not a station between CoQ and cytochrome c.',
    },
    {
      tag: 'energetics',
      stem: 'Why does FADH₂ yield roughly 1.5 ATP while NADH yields roughly 2.5 ATP?',
      choices: [
        'FADH₂ enters at Complex II, which pumps no protons, so it drives fewer pumps than NADH',
        'FADH₂ carries only one electron, so it reduces half as much oxygen',
        'FADH₂ has a more negative reduction potential than NADH and releases less energy',
        'ATP synthase cannot use protons pumped by FADH₂-derived electrons',
      ],
      answer: 0,
      rationale:
        'FADH₂ feeds electrons in at Complex II (succinate dehydrogenase), which has no proton-pumping machinery, so its electrons skip the first pump and bank only ~6 H⁺ versus ~10 for NADH (at ~4 H⁺/ATP → ~1.5 vs ~2.5). Both carriers deliver TWO electrons; FADH₂ actually sits at a more POSITIVE potential; and ATP synthase uses all pumped protons equally.',
    },
    {
      tag: 'energetics',
      stem: 'Approximately how many protons does the cell spend per ATP made by oxidative phosphorylation, and why is it more than ATP synthase’s own mechanical cost?',
      choices: [
        '~4 H⁺/ATP — the extra ~1 pays the transporters that export ATP and import ADP + Pi',
        '~4 H⁺/ATP — all four are consumed inside the synthase’s catalytic sites',
        '~10 H⁺/ATP — one per proton NADH originally banked',
        '~1 H⁺/ATP — the synthase is nearly perfectly efficient',
      ],
      answer: 0,
      rationale:
        'ATP synthase itself needs only ~3 H⁺/ATP, but the adenine nucleotide translocase and phosphate carrier add ~1 more to move ATP out and ADP/Pi in — the true price is ~4 H⁺/ATP. That transport "tax" is why NADH (~10 H⁺) buys ~2.5 ATP and FADH₂ (~6 H⁺) buys ~1.5.',
    },
    {
      tag: 'regulation',
      stem: 'An uncoupler such as 2,4-dinitrophenol makes the inner membrane leaky to protons. What is the immediate effect on electron transport and ATP synthesis?',
      choices: [
        'Electron transport speeds up while ATP synthesis falls and heat rises',
        'Both electron transport and ATP synthesis stop simultaneously',
        'Electron transport stops while ATP synthesis continues from the stored gradient',
        'ATP synthase reverses and begins pumping protons out of the matrix',
      ],
      answer: 0,
      rationale:
        'An uncoupler dissipates the gradient, so protons return without turning ATP synthase and ATP output collapses as heat. Because the gradient no longer back-pressures the pumps, electron transport actually ACCELERATES. This is how brown fat and fever make warmth, and how DNP was dangerously used for weight loss.',
    },
    {
      tag: 'regulation',
      stem: 'In isolated mitochondria respiring normally, adding oligomycin (an ATP synthase inhibitor) causes O₂ consumption to slow sharply. What is the best explanation?',
      choices: [
        'Blocking the synthase lets the gradient build; its back-pressure stalls the proton pumps and slows electron flow',
        'Oligomycin directly inhibits Complex IV, so electrons can’t reach O₂',
        'Oligomycin destroys NADH, removing the electron source',
        'ATP synthase normally consumes O₂, so blocking it lowers O₂ use directly',
      ],
      answer: 0,
      rationale:
        'Flow and phosphorylation are coupled through the gradient. Plug ATP synthase and protons can’t flow back, so the gradient rises and back-pressures the pumps, throttling electron transport (and O₂ use). Adding an uncoupler afterward drains the gradient and respiration races again — with no ATP made — proving the coupling.',
    },
    {
      tag: 'disease',
      stem: 'A patient is exposed to cyanide, which binds the heme a₃/CuB center of Complex IV. Which consequence best explains death within minutes?',
      choices: [
        'Electrons cannot reach O₂, so the chain backs up, the proton gradient collapses, and oxidative ATP synthesis stops',
        'Pyruvate can no longer enter the citric acid cycle, halting acetyl-CoA production',
        'ATP synthase runs in reverse and rapidly hydrolyzes the cell’s ATP pool',
        'Glycolysis is directly inhibited, eliminating substrate-level phosphorylation',
      ],
      answer: 0,
      rationale:
        'Blocking the terminal oxidase prevents electrons from reaching O₂, so every upstream carrier saturates reduced, no more protons are pumped, the proton-motive force dissipates, and ATP synthase loses its driving gradient. Cyanide does not directly block pyruvate entry or glycolysis, and the lethal event is gradient loss, not synthase reversal.',
    },
    {
      tag: 'disease',
      stem: 'A researcher adds antimycin A (a Complex III inhibitor) to actively respiring mitochondria and monitors carrier redox state by spectroscopy. What pattern is expected?',
      choices: [
        'Carriers upstream of Complex III (Complex I, II, CoQ) become reduced; those downstream (cyt c, Complex IV) become oxidized',
        'All carriers become fully oxidized because electron input stops',
        'Only cytochrome c oxidase changes state; the rest are unaffected',
        'All carriers oscillate rapidly between oxidized and reduced states',
      ],
      answer: 0,
      rationale:
        'Antimycin A blocks Complex III. Electrons still enter from NADH/FADH₂ and pile up reduced everywhere upstream of the block (Complexes I and II, CoQ), while everything downstream (cyt c, Complex IV) loses its supply and goes oxidized. This crossover pattern is exactly the inhibitor logic used to establish the order of the chain.',
    },
    {
      tag: 'integration',
      stem: 'In a sealed vesicle, isolated Complex II is supplied with succinate and ubiquinone and the proton gradient is measured, then compared with an identical vesicle running Complex I with NADH. What is observed?',
      choices: [
        'Complex II builds no proton gradient of its own because it lacks proton-pumping subunits',
        'Complex II builds a larger gradient because succinate is a stronger reductant than NADH',
        'Both build identical gradients because both reduce ubiquinone',
        'Complex II builds a gradient only if cytochrome c is also present',
      ],
      answer: 0,
      rationale:
        'Complex II oxidizes succinate and reduces ubiquinone but has NO proton-pumping apparatus, so it generates no gradient itself — precisely why FADH₂-derived electrons yield less ATP. Succinate/FAD is a WEAKER reductant than NADH (more positive E0′), Complex I DOES pump, and cytochrome c acts downstream at Complex III/IV.',
    },
    {
      tag: 'integration',
      stem: 'During reperfusion after a myocardial infarction, the inner-membrane carriers are highly reduced from the ischemic period and O₂ is suddenly restored. Which intervention most directly targets the mechanism of reperfusion injury?',
      choices: [
        'A mitochondria-targeted antioxidant that neutralizes superoxide as O₂ floods back',
        'A glycolytic inhibitor to reduce cytosolic ATP demand',
        'An ATP synthase activator to accelerate ATP production',
        'A drug that increases outer-membrane VDAC permeability',
      ],
      answer: 0,
      rationale:
        'Reperfusion injury arises when backed-up, highly reduced carriers dump electrons onto reintroduced O₂, producing a burst of superoxide (mainly at Complexes I and III) that overwhelms defenses. A mitochondria-targeted antioxidant scavenges that ROS at the source. Inhibiting glycolysis or boosting ATP synthase does not address the radical burst.',
    },
  ],
  funFact:
    'ATP synthase is a molecular rotary motor that spins at ~400 ATP per second — and it has been turning in every respiring cell for roughly two billion years. The oxygen it ultimately hands electrons to began as industrial WASTE dumped by ancient cyanobacteria; life didn’t just survive the poison, it built its most powerful engine around it.',
};
