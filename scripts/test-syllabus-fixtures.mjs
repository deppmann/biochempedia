/* Fixtures for scripts/test-syllabus.mjs: what people type, and what real syllabi look like.

   QUESTIONS   [what a learner typed, the idea(s) that are a right answer]. An empty list means
               the honest answer is "nothing on the site for this yet".
   HELD_OUT    the same shape, written after the matcher was tuned and never tuned against.
   SYLLABI     eight course outlines written the messy way real ones are, each line of the
               schedule labelled with the ideas that are right for it ([] = the site has nothing,
               or the line is housekeeping). A label lists every acceptable idea; the matcher is
               wrong when it returns one that is not listed. */

export const QUESTIONS = [
  // a twelve-year-old
  ['why do leaves change color', ['leaf-pigments', 'seasonal-responses', 'seasonal-rhythms']],
  ['why do leaves change color in the fall', ['leaf-pigments', 'seasonal-responses', 'seasonal-rhythms']],
  ['why are plants green', ['leaf-pigments', 'photosynthesis']],
  ['how do plants make food', ['photosynthesis']],
  ['how do plants eat', ['photosynthesis', 'plant-mineral-nutrition']],
  ['what is DNA', ['dna-structure']],
  ['what is dna made of', ['dna-structure']],
  ['what is a cell', ['cell-theory', 'organelles']],
  ['parts of a cell', ['organelles']],
  ['how do vaccines work', ['immunity']],
  ['how vaccines work', ['immunity']],
  ['why do we get sick', ['germ-theory', 'immunity', 'viruses', 'bacteria']],
  ['what are germs', ['germ-theory', 'bacteria', 'viruses']],
  ['why do we breathe', ['breathing', 'gas-exchange', 'cellular-respiration']],
  ['how does the heart work', ['circulation', 'cardiac-cycle']],
  ['why is blood red', ['oxygen-transport', 'red-blood-cells']],
  ['how do muscles work', ['muscle-contraction']],
  ['why do i look like my parents', ['inheritance']],
  ['how do we see color', ['colour-vision']],
  ['how do ears work', ['hearing']],
  ['what do bees do for flowers', ['pollination']],
  ['food chain', ['food-webs']],
  ['what is a habitat', ['habitat']],
  ['why did the dinosaurs die', ['mass-extinction', 'extinction']],
  ['how do seeds grow', ['seed-germination', 'plant-life-cycle', 'seeds-and-fruits']],
  ['water cycle', ['water-cycle']],
  ['what is photosynthesis', ['photosynthesis']],
  ['how does digestion work', ['digestion']],
  ['why do we sleep', ['sleep-regulation', 'sleep-stages']],
  ['how do birds know when to fly south', ['seasonal-responses', 'seasonal-rhythms']],
  // high school
  ['mitosis', ['cell-division']],
  ['mitosis vs meiosis', ['cell-division', 'meiosis']],
  ['punnett square', ['inheritance']],
  ['natural selection', ['natural-selection']],
  ['how does evolution work', ['natural-selection', 'evidence-for-evolution']],
  ['cell membrane', ['cell-membrane']],
  ['osmosis', ['osmosis']],
  ['diffusion and osmosis', ['diffusion', 'osmosis']],
  ['cellular respiration', ['cellular-respiration']],
  ['protein synthesis', ['gene-to-protein']],
  ['transcription and translation', ['gene-to-protein']],
  ['enzymes', ['enzymes']],
  ['how do enzymes speed up reactions', ['enzymes']],
  ['homeostasis', ['homeostasis']],
  ['carbon cycle', ['carbon-cycle']],
  ['how do antibiotics stop working', ['antibiotic-resistance']],
  ['what is a virus', ['viruses']],
  ['taxonomy', ['classification']],
  ['properties of water', ['properties-of-water']],
  ['macromolecules', ['macromolecules']],
  // a pre-med, an undergraduate
  ['sodium pump', ['active-transport', 'resting-membrane-potential', 'electrochemical-gradient']],
  ['sodium potassium pump', ['active-transport', 'resting-membrane-potential', 'electrochemical-gradient']],
  ['action potential', ['action-potential']],
  ['resting membrane potential', ['resting-membrane-potential']],
  ['krebs cycle', ['citric-acid-cycle']],
  ['electron transport chain', ['chemiosmosis', 'cellular-respiration']],
  ['oxidative phosphorylation', ['chemiosmosis']],
  ['glycolysis', ['glycolysis']],
  ['hemoglobin oxygen dissociation curve', ['oxygen-transport']],
  ['michaelis menten', ['enzymes']],
  ['g protein coupled receptors', ['gpcr-signaling']],
  ['hardy weinberg equilibrium', ['hardy-weinberg']],
  ['loop of henle', ['concentrating-urine', 'kidney']],
  ['frank starling', ['cardiac-output', 'cardiac-cycle']],
  ['long term potentiation', ['long-term-potentiation']],
  ['apoptosis', ['cell-death']],
  ['pcr', ['pcr']],
  ['crispr', ['genetic-engineering']],
  ['beta oxidation', ['fatty-acid-oxidation']],
  ['acid base balance', ['acid-base-balance']],
  // misspellings and loose typing
  ['photosynthsis', ['photosynthesis']],
  ['osmossis', ['osmosis']],
  ['mitocondria', ['cellular-respiration', 'endosymbiosis', 'organelles', 'chemiosmosis']],
  ['natrual selection', ['natural-selection']],
  ['imune system', ['immunity']],
  ['nuerons', ['neuron-structure', 'neuron-doctrine', 'action-potential']],
  ['DNA replicaton', ['dna-replication']],
  ['Homeostasis!!', ['homeostasis']],
  ['  MEIOSIS  ', ['meiosis']],
  ['haemoglobin', ['oxygen-transport']],
  // not on the site: the honest answer is nothing
  ['why is the sky blue', []],
  ['quantum chromodynamics', []],
  ['how do airplanes fly', []],
  ['french revolution', []],
  ['quadratic formula', []],
  ['how to balance a chemical equation', []],
  ['black holes', []],
  ['who won the world series', []],
  ['asdf qwer', []],
  ['newtons laws of motion', []],
];

export const HELD_OUT = [
  ['why do onions make you cry', []],
  ['how do fish breathe underwater', ['gas-exchange', 'breathing']],
  ['why do we need to eat', ['digestion', 'cellular-respiration', 'metabolic-rate', 'atp', 'hunger-and-appetite']],
  ['what is a gene', ['inheritance', 'dna-structure', 'gene-to-protein']],
  ['how does the brain send messages', ['action-potential', 'synapse', 'neurotransmitters', 'neuron-structure']],
  ['why do we have two eyes', []],
  ['what makes something alive', ['characteristics-of-life']],
  ['decomposers', ['decomposers']],
  ['what is an ecosystem', ['ecosystem']],
  ['invasive species', ['invasive-species']],
  ['why does my heart beat faster when i run', ['cardiac-output', 'circulation', 'baroreflex', 'oxygen-uptake', 'autonomic-nervous-system']],
  ['dominant and recessive', ['inheritance']],
  ['how are fossils evidence for evolution', ['evidence-for-evolution']],
  ['stem cells', ['stem-cells']],
  ['how do kidneys filter blood', ['kidney']],
  ['insulin and blood sugar', ['blood-sugar']],
  ['how does a nerve impulse travel', ['action-potential']],
  ['citric acid cycle', ['citric-acid-cycle']],
  ['gluconeogenesis', ['gluconeogenesis']],
  ['synaptic transmission', ['synapse', 'neurotransmitters']],
  ['meosis', ['meiosis']],
  ['enzime', ['enzymes']],
  ['evoluton', ['natural-selection', 'evidence-for-evolution', 'regulatory-evolution', 'coevolution']],
  ['what is climate change', ['climate-change']],
  ['how do plants drink water', ['plant-water-transport', 'plant-parts']],
  ['the nitrogen cycle', ['nitrogen-cycle']],
  ['how does the stock market work', []],
  ['pythagorean theorem', []],
  ['what causes cancer', ['cancer', 'oncogene', 'tumour-suppressor', 'mutation']],
  ['why do we feel pain', ['pain', 'touch-and-pain-pathways']],
  ['epigenetics', ['epigenetics']],
  ['how does hearing work', ['hearing', 'hair-cells']],
  ['what is ATP', ['atp']],
  ['speciation', ['speciation']],
  ['genetic drift', ['genetic-drift']],
  ['why do we get goosebumps', []],
];

/* Each syllabus: the class level (0 ages 5 to 10 … 6 graduate), the text as a teacher would
   paste it, and `lines`: [a piece of the line that picks it out, the ideas that are right for it].
   A schedule line that is not listed must get no match at all. */
export const SYLLABI = [
  {
    name: 'Grade 7 life science (pacing guide)', level: 1,
    text: `Life Science 7 - Pacing Guide 2026-27
Mrs. Alvarez   Room 214   alvarez@example.org
Supplies: composition notebook, colored pencils, 2 glue sticks
Grading: Tests 40%, Labs 30%, Classwork 20%, Homework 10%
Late work loses 10% per day. Phones stay in backpacks.

Quarter 1
Week 1 (Aug 24-28): Welcome, lab safety contract, scientific method
Week 2: Characteristics of living things (LS.1)
Week 3: Cell theory & microscopes
Week 4: Plant and animal cells - organelles (cell project due Fri)
Week 5: Cell membrane, diffusion and osmosis  ** egg lab **
Week 6: Photosynthesis (LS.4)
Week 7: Cellular respiration; Unit 1 Test
Week 8: Cell division - mitosis
Week 9: Levels of organization: cells, tissues, organs, organ systems
Quarter 2
Week 10: Classification / dichotomous keys
Week 11: Heredity - Punnett squares
Week 12: DNA and genes
Week 13: Thanksgiving break - no school
Week 14: Adaptations and natural selection
Week 15: Fossil record & evidence of change over time
Week 16: Ecosystems - biotic and abiotic factors
Week 17: Food webs and energy pyramids
Week 18: Midterm review + Midterm
Quarter 3
Week 19: Water cycle, carbon cycle, nitrogen cycle
Week 20: Populations and limiting factors
Week 21: Symbiosis; predator-prey relationships
Week 22: Biomes
Week 23: Human impact on the environment (watershed project)
Week 24: SOL review`,
    lines: [
      ['Characteristics of living things', ['characteristics-of-life']],
      ['Cell theory & microscopes', ['cell-theory', 'microscopy']],
      ['Plant and animal cells', ['organelles', 'cell-theory']],
      ['Cell membrane, diffusion and osmosis', ['cell-membrane', 'diffusion', 'osmosis']],
      ['Photosynthesis (LS.4)', ['photosynthesis']],
      ['Cellular respiration; Unit 1 Test', ['cellular-respiration']],
      ['Cell division - mitosis', ['cell-division']],
      ['Levels of organization', ['levels-of-organization']],
      ['Classification / dichotomous keys', ['classification', 'dichotomous-key']],
      ['Heredity - Punnett squares', ['inheritance']],
      ['DNA and genes', ['dna-structure', 'inheritance', 'gene-to-protein']],
      ['Adaptations and natural selection', ['adaptation', 'natural-selection']],
      ['Fossil record', ['evidence-for-evolution']],
      ['Ecosystems - biotic and abiotic', ['ecosystem']],
      ['Food webs and energy pyramids', ['food-webs']],
      ['Water cycle, carbon cycle, nitrogen cycle', ['water-cycle', 'carbon-cycle', 'nitrogen-cycle']],
      ['Populations and limiting factors', ['limiting-factors', 'population-growth']],
      ['Symbiosis; predator-prey', ['symbiosis', 'predation']],
      ['Biomes', ['climate']],
      ['Human impact on the environment', ['human-impact-on-ecosystems', 'nutrient-pollution', 'conservation']],
    ],
  },
  {
    name: 'Virginia high school biology', level: 2,
    text: `BIOLOGY I  /  Course Syllabus
Instructor: Mr. D. Okafor     Email: dokafor@example.org     Planning: 3rd block
Text: Miller & Levine Biology (class set)
Students will investigate and understand the Virginia Biology Standards of Learning (BIO.1 - BIO.8).
Grade scale: A 90-100, B 80-89, C 70-79, D 60-69

COURSE OUTLINE
Unit 1  Scientific investigation; lab safety (BIO.1)  -  1 week
Unit 2  Biochemistry: properties of water, macromolecules, enzymes (BIO.2)  -  3 weeks
Unit 3  Cell structure and function; prokaryotes vs eukaryotes (BIO.3)
Unit 4  Cell transport: diffusion, osmosis, active transport
Unit 5  Cell energy: photosynthesis and cellular respiration
          *** Benchmark 1 ***
Unit 6  Cell cycle and mitosis; cancer
Unit 7  Meiosis and sexual reproduction
Unit 8  Mendelian genetics, pedigrees
Unit 9  DNA structure and replication
Unit 10 Protein synthesis (transcription, translation); mutations
Unit 11 Biotechnology and genetic engineering
          Winter Break Dec 21 - Jan 1
Unit 12 Evolution: natural selection, evidence for evolution, speciation (BIO.7)
Unit 13 Classification and the diversity of life (BIO.6): bacteria, viruses, fungi
Unit 14 Human body systems and homeostasis
Unit 15 Ecology: populations, communities, ecosystems, succession (BIO.8)
Unit 16 SOL Review and SOL test`,
    lines: [
      ['Biochemistry: properties of water', ['properties-of-water', 'macromolecules', 'enzymes']],
      ['Cell structure and function', ['organelles', 'cell-theory', 'bacteria']],
      ['Cell transport', ['diffusion', 'osmosis', 'active-transport', 'cell-membrane']],
      ['Cell energy', ['photosynthesis', 'cellular-respiration']],
      ['Cell cycle and mitosis', ['cell-division', 'cancer', 'cell-cycle-engine', 'cell-cycle-checkpoints']],
      ['Meiosis and sexual reproduction', ['meiosis', 'sexual-and-asexual-reproduction']],
      ['Mendelian genetics, pedigrees', ['inheritance', 'pedigree-analysis']],
      ['DNA structure and replication', ['dna-structure', 'dna-replication']],
      ['Protein synthesis', ['gene-to-protein', 'mutation']],
      ['Biotechnology and genetic engineering', ['genetic-engineering']],
      ['Evolution: natural selection', ['natural-selection', 'evidence-for-evolution', 'speciation']],
      ['Classification and the diversity of life', ['classification', 'bacteria', 'viruses', 'fungi', 'biodiversity']],
      ['Human body systems and homeostasis', ['homeostasis', 'levels-of-organization']],
      ['Ecology: populations', ['population-growth', 'ecosystem', 'ecological-succession']],
    ],
  },
  {
    name: 'AP-style biology', level: 3,
    text: `AP Biology 2026-2027 — Tentative Schedule
Dr. Lindqvist | lindqvist@example.org | Tutoring Tu/Th 3:15
Required: Campbell Biology in Focus, 3rd ed. ISBN 978-0000000000
This is a college-level course. Expect 5-7 hours of work outside class each week.

Date | Topic | Reading
9/1 | Course intro, summer assignment quiz |
9/3 | Chemistry of life: water and hydrogen bonding | Ch 2
9/8 | Carbon and the macromolecules | Ch 3
9/10 | Protein structure & folding | Ch 3
9/15 | Enzymes; Enzyme catalysis lab | Ch 6
9/17 | Unit 1 Exam |
9/22 | Tour of the cell - organelles, endomembrane system | Ch 4
9/24 | Membrane structure; fluid mosaic model | Ch 5
9/29 | Passive & active transport; water potential | Ch 5
10/1 | Cell communication: signal transduction pathways | Ch 5
10/6 | Feedback and homeostasis |
10/8 | Cellular respiration: glycolysis, Krebs, ETC | Ch 7
10/13 | Fermentation | Ch 7
10/15 | Photosynthesis: light reactions and Calvin cycle | Ch 8
10/20 | Cell cycle, mitosis, checkpoints | Ch 9
10/22 | Meiosis and genetic variation | Ch 10
10/27 | Mendel and the gene idea; chi-square | Ch 11
10/29 | Linkage, sex-linked traits, nondisjunction | Ch 12
11/3 | DNA replication | Ch 13
11/5 | Gene expression: transcription & translation | Ch 14
11/10 | Regulation of gene expression: operons, epigenetics | Ch 15
11/12 | Biotechnology: PCR, gel electrophoresis, CRISPR | Ch 13
11/17 | Natural selection; Hardy-Weinberg | Ch 19, 21
11/19 | Phylogeny and speciation | Ch 20, 22
11/24 | No class - Thanksgiving
12/1 | Ecology: population growth models | Ch 40
12/3 | Community ecology, energy flow, biodiversity | Ch 41-42
12/8 | Review for final
12/15 | FINAL EXAM 8:00 AM`,
    lines: [
      ['Chemistry of life: water', ['properties-of-water', 'weak-interactions']],
      ['Carbon and the macromolecules', ['macromolecules']],
      ['Protein structure & folding', ['protein-structure', 'protein-folding']],
      ['Enzymes; Enzyme catalysis lab', ['enzymes']],
      ['Tour of the cell', ['organelles', 'secretory-pathway']],
      ['Membrane structure; fluid mosaic', ['cell-membrane']],
      ['Passive & active transport', ['active-transport', 'diffusion', 'osmosis', 'plant-water-transport']],
      ['Cell communication', ['cell-signaling']],
      ['Feedback and homeostasis', ['homeostasis', 'positive-feedback']],
      ['Cellular respiration: glycolysis', ['cellular-respiration', 'glycolysis', 'citric-acid-cycle', 'chemiosmosis']],
      ['Fermentation', ['fermentation']],
      ['Photosynthesis: light reactions', ['photosynthesis']],
      ['Cell cycle, mitosis, checkpoints', ['cell-division', 'cell-cycle-checkpoints', 'cell-cycle-engine']],
      ['Meiosis and genetic variation', ['meiosis', 'variation']],
      ['Mendel and the gene idea', ['inheritance', 'chi-square-test']],
      ['Linkage, sex-linked traits', ['genetic-linkage', 'sex-linkage', 'aneuploidy']],
      ['DNA replication | Ch 13', ['dna-replication']],
      ['Gene expression: transcription', ['gene-to-protein']],
      ['Regulation of gene expression', ['gene-regulation', 'epigenetics']],
      ['Biotechnology: PCR', ['pcr', 'genetic-engineering']],
      ['Natural selection; Hardy-Weinberg', ['natural-selection', 'hardy-weinberg']],
      ['Phylogeny and speciation', ['phylogenetic-trees', 'speciation']],
      ['Ecology: population growth', ['population-growth']],
      ['Community ecology, energy flow', ['food-webs', 'biodiversity', 'primary-production', 'competition']],
    ],
  },
  {
    name: 'Intro cell biology (college)', level: 4,
    text: `BIOL 2100: Cell Biology — Spring
Lecture MWF 10:00-10:50, Gilmer 190. Office hours W 1-3 or by appointment.
Prerequisites: BIOL 1010 and CHEM 1410. 3 credits.
Exams (3 x 20%), final (25%), problem sets (15%). No make-up exams without a documented excuse.
Academic integrity: all work must be your own; see the honor code.

Lecture schedule (subject to change)
1. Jan 14  Introduction; how we see cells: light and fluorescence microscopy
2. Jan 16  Membrane lipids and the bilayer
3. Jan 21  Membrane proteins, topology
4. Jan 23  Transport across membranes: channels, carriers, pumps
5. Jan 26  Protein sorting I: signal sequences & the ER
6. Jan 28  Protein sorting II: nuclear import/export
7. Jan 30  Vesicular traffic: ER to Golgi, secretion
8. Feb 2   Endocytosis and lysosomes
9. Feb 4   Protein quality control, the unfolded protein response
10. Feb 6  Ubiquitin and the proteasome; autophagy
    Feb 9  EXAM 1 (lectures 1-10)
11. Feb 11 Actin and cell migration
12. Feb 13 Microtubules, dynamic instability
13. Feb 16 Motor proteins: kinesin, dynein, myosin
14. Feb 18 Cilia and flagella
15. Feb 20 Cell junctions and adhesion; ECM
16. Feb 23 Cell signaling principles; GPCRs
17. Feb 25 Receptor tyrosine kinases, Ras/MAPK
18. Feb 27 The cell cycle: cyclins and CDKs
19. Mar 2  Checkpoints; mitosis mechanics
    Mar 9-13 Spring break
20. Mar 16 Apoptosis
21. Mar 18 Stem cells and reprogramming
22. Mar 20 Cancer: oncogenes and tumor suppressors
23. Mar 23 Mitochondria and chloroplasts: origins, energy conversion
    Mar 25 EXAM 2`,
    lines: [
      ['light and fluorescence microscopy', ['microscopy', 'fluorescent-reporters']],
      ['Membrane lipids and the bilayer', ['cell-membrane', 'lipid-asymmetry', 'lipids']],
      ['Membrane proteins, topology', ['membrane-protein-topology', 'cell-membrane']],
      ['Transport across membranes', ['active-transport', 'ion-channels']],
      ['Protein sorting I', ['protein-sorting', 'secretory-pathway']],
      ['Protein sorting II', ['protein-sorting', 'nuclear-transport']],
      ['Vesicular traffic', ['vesicle-transport', 'secretory-pathway']],
      ['Endocytosis and lysosomes', ['endocytosis', 'autophagy']],
      ['Protein quality control', ['protein-quality-control', 'cell-stress-response']],
      ['Ubiquitin and the proteasome', ['protein-degradation', 'autophagy']],
      ['Actin and cell migration', ['cell-migration', 'cytoskeleton']],
      ['Microtubules, dynamic instability', ['dynamic-instability', 'cytoskeleton']],
      ['Motor proteins', ['motor-proteins']],
      ['Cilia and flagella', ['cilia']],
      ['Cell junctions and adhesion', ['cell-adhesion', 'tight-junction', 'extracellular-matrix', 'epithelium']],
      ['Cell signaling principles', ['cell-signaling', 'gpcr-signaling']],
      ['Receptor tyrosine kinases', ['receptor-tyrosine-kinase', 'ras-mapk-cascade']],
      ['The cell cycle: cyclins', ['cell-cycle-engine', 'cell-division']],
      ['Checkpoints; mitosis mechanics', ['cell-cycle-checkpoints', 'cell-division']],
      ['Apoptosis', ['cell-death']],
      ['Stem cells and reprogramming', ['stem-cells', 'cell-reprogramming']],
      ['Cancer: oncogenes', ['cancer', 'oncogene', 'tumour-suppressor']],
      ['Mitochondria and chloroplasts', ['endosymbiosis', 'chemiosmosis', 'cellular-respiration', 'organelles', 'photosynthesis']],
    ],
  },
  {
    name: 'Genetics (college)', level: 4,
    text: `GENETICS (BIO 305)    Fall Semester
Professor: R. Banerjee, Ph.D.    Office: LSB 3.214    Phone: 555-0142
Textbook: any recent genetics text is fine; problem sets are posted on Canvas each Friday.
Attendance is expected. Clickers count for 5% of your grade.

Wk  Topic(s)                                              Problems
1   Mendel's laws; probability and the chi-square test      PS1
2   Extensions of Mendel: incomplete dominance, epistasis   PS2
3   Pedigree analysis; sex linkage                          PS3
4   Meiosis, nondisjunction and aneuploidy
5   Linkage and recombination mapping                       PS4
6   EXAM I; bacterial genetics: conjugation, transduction
7   DNA structure; replication                              PS5
8   Mutation and DNA repair
9   Transcription, RNA processing, the genetic code         PS6
10  Fall break (no class Mon/Tue); gene regulation in prokaryotes - lac operon
11  Eukaryotic gene regulation; chromatin and epigenetics   PS7
12  EXAM II; genomics: sequencing and genome assembly
13  Recombinant DNA, PCR, CRISPR                            PS8
14  Population genetics: Hardy-Weinberg, drift, selection
15  Quantitative traits and heritability; GWAS              PS9
16  Cancer genetics; review`,
    lines: [
      ["Mendel's laws", ['inheritance', 'chi-square-test']],
      ['Extensions of Mendel', ['epistasis', 'inheritance']],
      ['Pedigree analysis; sex linkage', ['pedigree-analysis', 'sex-linkage']],
      ['Meiosis, nondisjunction', ['meiosis', 'aneuploidy']],
      ['Linkage and recombination mapping', ['genetic-linkage']],
      ['bacterial genetics', ['bacterial-gene-transfer']],
      ['DNA structure; replication', ['dna-structure', 'dna-replication']],
      ['Mutation and DNA repair', ['mutation', 'dna-repair']],
      ['Transcription, RNA processing', ['gene-to-protein', 'rna-processing']],
      ['gene regulation in prokaryotes', ['gene-regulation']],
      ['Eukaryotic gene regulation', ['gene-regulation', 'epigenetics', 'transcription-factors']],
      ['genomics: sequencing', ['dna-sequencing', 'genome-assembly']],
      ['Recombinant DNA, PCR, CRISPR', ['genetic-engineering', 'pcr']],
      ['Population genetics', ['hardy-weinberg', 'genetic-drift', 'natural-selection']],
      ['Quantitative traits and heritability', ['complex-traits', 'heritability', 'gwas']],
      ['Cancer genetics', ['cancer', 'oncogene', 'tumour-suppressor']],
    ],
  },
  {
    name: 'Human physiology (college)', level: 5,
    text: `PHSL 3050 Human Physiology
Meets TR 9:30-10:45. Lab sections meet separately; see the lab syllabus.
Your grade: 4 exams @ 22.5% each, 10% quizzes.
Email me at physiology-course@example.edu with "PHSL 3050" in the subject line.

Tentative calendar
Tue Aug 26 - Homeostasis and feedback control
Thu Aug 28 - Membrane transport, body fluid compartments
Tue Sep 2 - Resting membrane potential
Thu Sep 4 - Action potentials & conduction
Tue Sep 9 - Synaptic transmission; neuromuscular junction
Thu Sep 11 - Skeletal muscle: excitation-contraction coupling
Tue Sep 16 - Smooth and cardiac muscle
Thu Sep 18 - Autonomic nervous system
Tue Sep 23 - EXAM 1
Thu Sep 25 - Cardiac electrophysiology, the ECG
Tue Sep 30 - Cardiac cycle; cardiac output
Thu Oct 2 - Hemodynamics: pressure, flow, resistance
Tue Oct 7 - Regulation of arterial pressure (baroreflex)
Thu Oct 9 - Capillary exchange and edema
Tue Oct 14 - Reading day, no class
Thu Oct 16 - Mechanics of breathing; surfactant
Tue Oct 21 - Gas exchange and O2/CO2 transport
Thu Oct 23 - Control of ventilation
Tue Oct 28 - EXAM 2
Thu Oct 30 - Glomerular filtration, renal clearance
Tue Nov 4 - Tubular reabsorption; concentrating the urine
Thu Nov 6 - Acid-base physiology
Tue Nov 11 - Potassium and calcium balance
Thu Nov 13 - GI motility and secretion
Tue Nov 18 - Digestion & absorption
Thu Nov 20 - Endocrine pancreas: insulin, glucagon
Tue Nov 25 - Hypothalamus and pituitary; thyroid
Tue Dec 2 - Adrenal; reproductive physiology
Thu Dec 4 - Thermoregulation and exercise`,
    lines: [
      ['Homeostasis and feedback control', ['homeostasis']],
      ['Membrane transport, body fluid', ['active-transport', 'body-water-compartments', 'osmosis', 'diffusion']],
      ['Resting membrane potential', ['resting-membrane-potential']],
      ['Action potentials & conduction', ['action-potential', 'myelin', 'passive-membrane-signals']],
      ['Synaptic transmission', ['synapse', 'neurotransmitters']],
      ['Skeletal muscle', ['muscle-contraction']],
      ['Smooth and cardiac muscle', ['smooth-muscle-contraction', 'muscle-contraction']],
      ['Autonomic nervous system', ['autonomic-nervous-system']],
      ['Cardiac electrophysiology', ['electrocardiogram']],
      ['Cardiac cycle; cardiac output', ['cardiac-cycle', 'cardiac-output']],
      ['Hemodynamics', ['blood-flow-resistance']],
      ['Regulation of arterial pressure', ['baroreflex', 'pressure-natriuresis']],
      ['Capillary exchange and edema', ['capillary-exchange', 'edema']],
      ['Mechanics of breathing', ['breathing', 'surfactant']],
      ['Gas exchange and O2', ['gas-exchange', 'oxygen-transport', 'carbon-dioxide-transport']],
      ['Control of ventilation', ['control-of-breathing', 'breathing']],
      ['Glomerular filtration', ['kidney', 'renal-autoregulation']],
      ['Tubular reabsorption', ['kidney', 'concentrating-urine']],
      ['Acid-base physiology', ['acid-base-balance']],
      ['Potassium and calcium balance', ['potassium-balance', 'calcium-balance']],
      ['GI motility and secretion', ['gut-motility', 'stomach-acid', 'digestive-control']],
      ['Digestion & absorption', ['digestion']],
      ['Endocrine pancreas', ['blood-sugar']],
      ['Hypothalamus and pituitary', ['hypothalamic-pituitary-axes', 'thyroid-hormone']],
      ['Adrenal; reproductive', ['adrenal-glands', 'menstrual-cycle', 'spermatogenesis']],
      ['Thermoregulation and exercise', ['body-temperature', 'oxygen-uptake']],
    ],
  },
  {
    name: 'Neuroscience (college)', level: 5,
    text: `NESC 2010 — Introduction to Neuroscience
Instructors: two faculty share the course; contact the course coordinator first.
Readings are from Purves, Neuroscience 6e. Lecture slides are posted the night before.
There are three midterms and a cumulative final. The lowest midterm is dropped.

Module 1: Neural signaling
  Lecture 1 - Neurons and glia; the neuron doctrine
  Lecture 2 - The resting potential (Purves ch. 2)
  Lecture 3 - The action potential; voltage-gated channels
  Lecture 4 - Myelin and saltatory conduction
  Lecture 5 - Synapses and neurotransmitter release
  Lecture 6 - Neurotransmitters and their receptors
  Lecture 7 - Synaptic integration; inhibition
  Lecture 8 - LTP, LTD and learning
  ** Midterm 1 **
Module 2: Sensation
  Lecture 9 - Sensory transduction and coding
  Lecture 10 - Touch and proprioception
  Lecture 11 - Pain
  Lecture 12 - The eye and phototransduction
  Lecture 13 - Central visual pathways; color
  Lecture 14 - Hearing: hair cells and the cochlea
  Lecture 15 - Vestibular system
  Lecture 16 - Smell and taste
  ** Midterm 2 **
Module 3: Movement and beyond
  Lecture 17 - Motor units and spinal reflexes
  Lecture 18 - Basal ganglia & cerebellum
  Lecture 19 - Sleep and circadian rhythms
  Lecture 20 - Memory systems; the hippocampus
  Lecture 21 - Reward, dopamine and addiction
  Lecture 22 - Language and lateralization
  Lecture 23 - Development: axon guidance, critical periods
  Lecture 24 - Neurodegenerative disease`,
    lines: [
      ['Neurons and glia', ['neuron-structure', 'glia', 'neuron-doctrine']],
      ['The resting potential', ['resting-membrane-potential']],
      ['The action potential; voltage-gated', ['action-potential', 'ion-channels']],
      ['Myelin and saltatory conduction', ['myelin']],
      ['Synapses and neurotransmitter release', ['synapse', 'neurotransmitters']],
      ['Neurotransmitters and their receptors', ['neurotransmitters', 'receptors']],
      ['Synaptic integration; inhibition', ['synaptic-integration', 'inhibition']],
      ['LTP, LTD and learning', ['long-term-potentiation']],
      ['Sensory transduction and coding', ['sensory-transduction', 'sensory-coding']],
      ['Touch and proprioception', ['touch', 'proprioception']],
      ['Lecture 11 - Pain', ['pain']],
      ['The eye and phototransduction', ['vision', 'light-adaptation', 'sensory-transduction']],
      ['Central visual pathways', ['vision', 'colour-vision']],
      ['Hearing: hair cells', ['hearing', 'hair-cells', 'cochlear-amplifier']],
      ['Vestibular system', ['sense-of-balance']],
      ['Smell and taste', ['smell', 'taste', 'flavour']],
      ['Motor units and spinal reflexes', ['motor-unit-recruitment', 'stretch-reflex']],
      ['Basal ganglia & cerebellum', ['basal-ganglia', 'cerebellum']],
      ['Sleep and circadian rhythms', ['sleep-regulation', 'sleep-stages', 'circadian-rhythm']],
      ['Memory systems', ['memory-systems', 'memory-consolidation']],
      ['Reward, dopamine', ['reward-prediction-error', 'wanting-vs-liking']],
      ['Language and lateralization', ['aphasia', 'hemispheric-lateralization']],
      ['Development: axon guidance', ['axon-guidance', 'critical-period']],
      ['Neurodegenerative disease', ['neurodegeneration']],
    ],
  },
  {
    name: 'Biochemistry (college)', level: 5,
    text: `CHEM/BIOL 4410 Biochemistry I — schedule of topics
Lectures: M W F 11-11:50. Discussion sections begin the second week.
Text: Lehninger Principles of Biochemistry (8th), chapters noted below.
Grading is not curved. Regrade requests must be submitted in writing within one week.

M 8/25   Water, weak interactions, pH and buffers (Ch. 2)
W 8/27   Amino acids (Ch. 3)
F 8/29   Peptides; protein primary structure
W 9/3    Secondary, tertiary and quaternary structure (Ch. 4)
F 9/5    Protein folding and misfolding
M 9/8    Protein purification and characterization
W 9/10   Hemoglobin: oxygen binding, allostery (Ch. 5)
F 9/12   Enzyme kinetics: Michaelis-Menten (Ch. 6)
M 9/15   Enzyme mechanisms and inhibition
W 9/17   Regulation of enzymes: zymogens, phosphorylation
F 9/19   EXAM 1
M 9/22   Carbohydrates and glycobiology (Ch. 7)
W 9/24   Lipids, membranes (Ch. 10-11)
F 9/26   Bioenergetics: free energy, ATP (Ch. 13)
M 9/29   Glycolysis (Ch. 14)
W 10/1   Gluconeogenesis; pentose phosphate pathway
F 10/3   Glycogen metabolism and its regulation
M 10/6   Citric acid cycle (Ch. 16)
W 10/8   Electron transport and oxidative phosphorylation (Ch. 19)
F 10/10  EXAM 2
M 10/13  Fatty acid oxidation; ketone bodies (Ch. 17)
W 10/15  Fatty acid and cholesterol synthesis (Ch. 21)
F 10/17  Amino acid catabolism and the urea cycle (Ch. 18)
M 10/20  Nucleotide metabolism (Ch. 22)
W 10/22  Integration of metabolism: fed and fasted states; AMPK, mTOR
F 10/24  Review / catch-up`,
    lines: [
      ['Water, weak interactions', ['properties-of-water', 'weak-interactions', 'ph-and-buffers', 'hydrophobic-effect']],
      ['Amino acids (Ch. 3)', ['amino-acids']],
      ['Peptides; protein primary structure', ['protein-structure', 'amino-acids']],
      ['Secondary, tertiary', ['protein-structure']],
      ['Protein folding and misfolding', ['protein-folding', 'protein-quality-control']],
      ['Protein purification', ['protein-purification', 'identifying-proteins']],
      ['Hemoglobin: oxygen binding', ['oxygen-transport', 'allostery']],
      ['Enzyme kinetics', ['enzymes']],
      ['Enzyme mechanisms and inhibition', ['enzymes']],
      ['Regulation of enzymes', ['zymogen-activation', 'protein-phosphorylation', 'allostery', 'enzymes']],
      ['Carbohydrates and glycobiology', ['carbohydrates', 'sugar-coat']],
      ['Lipids, membranes', ['lipids', 'cell-membrane']],
      ['Bioenergetics', ['free-energy', 'atp']],
      ['Glycolysis (Ch. 14)', ['glycolysis']],
      ['Gluconeogenesis; pentose', ['gluconeogenesis', 'pentose-phosphate-pathway']],
      ['Glycogen metabolism', ['blood-sugar', 'carbohydrates']],
      ['Citric acid cycle', ['citric-acid-cycle']],
      ['Electron transport and oxidative', ['chemiosmosis']],
      ['Fatty acid oxidation; ketone', ['fatty-acid-oxidation', 'ketone-bodies']],
      ['Fatty acid and cholesterol synthesis', ['fatty-acid-synthesis', 'cholesterol']],
      ['Amino acid catabolism', ['amino-acid-catabolism', 'urea-cycle']],
      ['Nucleotide metabolism', ['nucleotide-metabolism']],
      ['Integration of metabolism', ['fasting-and-starvation', 'ampk-energy-sensing', 'mtor-growth-control']],
    ],
  },
];

/* Three more outlines, written after the matcher and its textbook names were settled and never
   tuned against: the honest measure of how a syllabus nobody has seen will fare. */
export const SYLLABI_HELD_OUT = [
  {
    name: 'Honors biology, block schedule (held out)', level: 2,
    text: `Honors Biology — Semester Plan (4x4 block)
Ms. T. Nakamura · nakamura@example.org · Remind code on the board
Materials: 3-ring binder, calculator. Retakes allowed within 5 school days.

Day 1-2    Class procedures, safety quiz, graphing skills
Day 3-6    Atoms, bonds & water
Day 7-10   Carbohydrates, lipids, proteins, nucleic acids
Day 11-13  Enzymes and activation energy (toothpickase lab)
Day 14     TEST: Biochemistry
Day 15-18  Microscopy; prokaryotic and eukaryotic cells
Day 19-21  The plasma membrane and homeostasis
Day 22-24  ATP & photosynthesis
Day 25-27  Aerobic and anaerobic respiration
Day 28     TEST: Cells and energy
Day 29-32  DNA replication, the cell cycle
Day 33-36  From DNA to protein
Day 37-40  Meiosis; Mendel's peas; dihybrid crosses
Day 41-42  Human genetic disorders and karyotypes
Day 43     Midterm
Day 44-48  Darwin's theory; mechanisms of evolution
Day 49-51  Cladograms and classification
Day 52-55  Viruses and bacteria; the immune response
Day 56-60  Plant structure and transport
Day 61-66  Ecology: energy flow, cycles of matter, population dynamics
Day 67-70  Human impacts and conservation
Day 71-72  Review / Final`,
    lines: [
      ['Atoms, bonds & water', ['properties-of-water', 'weak-interactions']],
      ['Carbohydrates, lipids, proteins', ['carbohydrates', 'lipids', 'protein-structure', 'dna-structure', 'macromolecules']],
      ['Enzymes and activation energy', ['enzymes', 'free-energy']],
      ['Microscopy; prokaryotic', ['microscopy', 'bacteria', 'organelles', 'cell-theory']],
      ['The plasma membrane and homeostasis', ['cell-membrane', 'homeostasis']],
      ['ATP & photosynthesis', ['atp', 'photosynthesis']],
      ['Aerobic and anaerobic respiration', ['cellular-respiration', 'fermentation']],
      ['DNA replication, the cell cycle', ['dna-replication', 'cell-division', 'cell-cycle-engine']],
      ['From DNA to protein', ['gene-to-protein']],
      ['Meiosis; Mendel', ['meiosis', 'inheritance']],
      ['Human genetic disorders', ['aneuploidy', 'pedigree-analysis', 'inheritance', 'mutation']],
      ["Darwin's theory", ['natural-selection', 'evidence-for-evolution']],
      ['Cladograms and classification', ['phylogenetic-trees', 'classification']],
      ['Viruses and bacteria', ['viruses', 'bacteria', 'immunity']],
      ['Plant structure and transport', ['plant-parts', 'plant-water-transport', 'phloem-transport']],
      ['Ecology: energy flow', ['food-webs', 'population-growth', 'carbon-cycle', 'nitrogen-cycle', 'water-cycle']],
      ['Human impacts and conservation', ['human-impact-on-ecosystems', 'conservation']],
    ],
  },
  {
    name: 'Ecology and evolution (college, held out)', level: 4,
    text: `BIOL 3020  Ecology & Evolution  —  topics by week
Prof. Hartmann. Lectures TTh; discussion F. Three exams, one field report (20%).
Readings posted on the course site. Please silence phones.

Week 1  What is evolution? Darwin and Wallace
Week 2  Variation, heritability and the response to selection
Week 3  Genetic drift and effective population size
Week 4  Gene flow; Hardy-Weinberg as a null model
Week 5  Species concepts and speciation
Week 6  Reading trees; homology versus convergence      (Exam 1 Thursday)
Week 7  Molecular evolution and the molecular clock
Week 8  Life history evolution
Week 9  Population growth: exponential and logistic
Week 10 Competition and the niche
Week 11 Predation, parasitism, mutualism                 (Exam 2 Thursday)
Week 12 Community structure: succession and disturbance
Week 13 Island biogeography and metapopulations
Week 14 Ecosystem ecology: primary production, nutrient cycling
Week 15 Global change; conservation biology`,
    lines: [
      ['What is evolution', ['natural-selection', 'evidence-for-evolution']],
      ['Variation, heritability', ['variation', 'heritability', 'natural-selection', 'artificial-selection']],
      ['Genetic drift and effective', ['genetic-drift', 'effective-population-size']],
      ['Gene flow; Hardy-Weinberg', ['gene-flow', 'hardy-weinberg']],
      ['Species concepts and speciation', ['species-concepts', 'speciation']],
      ['Reading trees; homology', ['phylogenetic-trees', 'homology-and-convergence']],
      ['Molecular evolution', ['molecular-clock', 'selection-in-genes', 'dna-comparison']],
      ['Life history evolution', ['life-history-trade-offs']],
      ['Population growth: exponential', ['population-growth']],
      ['Competition and the niche', ['competition', 'niche']],
      ['Predation, parasitism, mutualism', ['predation', 'symbiosis']],
      ['Community structure', ['ecological-succession', 'disturbance-and-diversity']],
      ['Island biogeography', ['island-biogeography', 'metapopulation']],
      ['Ecosystem ecology', ['primary-production', 'nitrogen-cycle', 'carbon-cycle', 'ecosystem']],
      ['Global change; conservation', ['climate-change', 'conservation']],
    ],
  },
  {
    name: 'Anatomy and physiology, community college (held out)', level: 4,
    text: `BIO 142 Human Anatomy & Physiology II
Lab meets in S-210. Closed-toe shoes required in lab at all times.
Grades: lecture exams 60%, lab practicals 25%, homework 15%.
If you need accommodations, contact Disability Services in the first two weeks.

Session 1: Blood - composition, red cells, hemostasis
Session 2: Heart anatomy; conduction system and ECG
Session 3: Cardiac cycle, cardiac output
Session 4: Blood vessels and blood pressure
Session 5: Lymphatic system; innate and adaptive immunity
Session 6: Lecture Exam 1
Session 7: Respiratory anatomy; pulmonary ventilation
Session 8: Gas exchange and transport
Session 9: Digestive tract; chemical digestion
Session 10: Nutrition and metabolism; body temperature
Session 11: Lecture Exam 2
Session 12: Urinary system: nephron function
Session 13: Fluid, electrolyte and acid-base balance
Session 14: Male and female reproductive systems
Session 15: Pregnancy and human development
Session 16: Final Exam (cumulative)`,
    lines: [
      ['Blood - composition', ['red-blood-cells', 'blood-clotting', 'oxygen-transport']],
      ['Heart anatomy; conduction', ['circulation', 'electrocardiogram']],
      ['Cardiac cycle, cardiac output', ['cardiac-cycle', 'cardiac-output']],
      ['Blood vessels and blood pressure', ['blood-flow-resistance', 'baroreflex', 'pressure-natriuresis', 'circulation']],
      ['Lymphatic system', ['immunity']],
      ['Respiratory anatomy', ['breathing']],
      ['Gas exchange and transport', ['gas-exchange', 'oxygen-transport', 'carbon-dioxide-transport']],
      ['Digestive tract', ['digestion']],
      ['Nutrition and metabolism', ['body-temperature', 'metabolic-rate']],
      ['Urinary system', ['kidney']],
      ['Fluid, electrolyte', ['acid-base-balance', 'body-water-compartments', 'potassium-balance', 'osmoregulation']],
      ['Male and female reproductive', ['menstrual-cycle', 'spermatogenesis', 'sexual-differentiation']],
      ['Pregnancy and human development', ['pregnancy', 'early-embryo', 'fertilization']],
    ],
  },
];

/* The review panel's own questions and syllabus lines (round 1 of the review of this feature),
   added as written, before any fix was tuned on them. An empty list means the honest answer is
   "nothing here", and for PANEL_SENSITIVE the page must answer with the calm fixed message and
   no lesson: questions a child or a teenager types about health, feelings or their own body. */
export const PANEL_SENSITIVE = [
  'what is depression', 'depression', 'what is addiction', 'how do babies get made', 'where do babies come from', 'how are babies made',
  'what happens when you die', 'why do I have a period', 'how do I tell my parents', 'do vaccines cause autism', 'are GMOs safe',
  'how do I hurt myself', 'why do I feel sad all the time', 'why do i wet the bed', 'why are drugs addictive', 'puberty', 'how are twins made',
];
export const PANEL_QUESTIONS = [
  ['what does the mitochondria do', ['organelles', 'cellular-respiration', 'chemiosmosis']],
  ['what is a gene', ['inheritance', 'dna-structure', 'gene-to-protein']],
  ['genes', ['inheritance', 'dna-structure', 'gene-to-protein']],
  ['what are genes', ['inheritance', 'dna-structure', 'gene-to-protein']],
  // one common word that is half of a compound name: never a confident answer
  ['power', []], ['speed', []], ['resistance', []], ['environment', []], ['nature', []], ['frequency', []], ['repair', []], ['birth', []],
  ['size', []], ['place', []], ['duration', []], ['export', []], ['mark', []], ['forward', []], ['learning', []],
  // a one-word synonym must not decide a longer question about something else
  ['why are my eyes blue', ['inheritance', 'complex-traits', 'genes-and-environment']],
  ['eye color genetics', ['inheritance', 'complex-traits', 'genes-and-environment']],
  ['why do i have my moms eyes', ['inheritance', 'complex-traits', 'genes-and-environment']],
  ['what is a carrier of a disease', ['inheritance', 'pedigree-analysis', 'sex-linkage']],
  ['carrier of sickle cell', ['inheritance', 'pedigree-analysis', 'sex-linkage', 'mutation']],
  ['lung cancer', ['cancer']], ['thyroid cancer', ['cancer']], ['fossil fuels', []], ['restriction enzymes', ['genetic-engineering']],
  ['pink eye', []], ['google translate', []], ['t cells and b cells', ['immunity', 't-cell-receptor-signaling']],
  ['are viruses alive', ['viruses', 'characteristics-of-life']], ['what is pH', ['ph-and-buffers', 'acid-base-balance']],
  ['how do hormones work', ['hypothalamic-pituitary-axes', 'receptors', 'nuclear-receptors', 'cell-signaling', 'thyroid-hormone']],
  ['what is the difference between mitosis and meiosis', ['meiosis', 'cell-division']],
  ['whats the difference between mitosis and meiosis', ['meiosis', 'cell-division']],
  ['how do plants eat', ['photosynthesis', 'plant-mineral-nutrition']],
  ['how do antibiotics work', ['antibiotic-resistance']],
  // things the site teaches that got "nothing"
  ['how does the stomach digest food', ['digestion', 'stomach-acid']],
  ['how do nerves send messages', ['action-potential', 'synapse', 'neurotransmitters']],
  ['how do we taste sour', ['taste', 'flavour']],
  ['what eats what in a forest', ['food-webs', 'predation']],
  ['why do people get diabetes', ['blood-sugar']], ['diabetes', ['blood-sugar']],
  ['why do i look like my mom', ['inheritance']],
  ['ribosomes', ['gene-to-protein', 'organelles']],
  ['competitive inhibition', ['enzymes']],
  ['hiv', ['viruses', 'immunity']],
  ['why do my muscles burn when i sprint', ['fermentation', 'muscle-fatigue', 'glycolysis']],
  ['motor cortex', ['cortical-areas', 'localization-of-function', 'corticospinal-tract']],
  ['does a tree die in winter', ['seasonal-rhythms', 'seasonal-responses']],
  // what held up
  ['how do plants drink water', ['plant-water-transport', 'plant-parts']], ['krebs cycle', ['citric-acid-cycle']],
  ['renal clearance', ['kidney']], ['henderson hasselbalch', ['ph-and-buffers', 'acid-base-balance']],
  ['how do cells talk to each other', ['cell-signaling']], ['virus vs bacteria', ['viruses', 'bacteria']],
  ['punnett square', ['inheritance']], ['how does the eye see color', ['colour-vision', 'vision']],
  ['how do muscles get tired', ['muscle-fatigue']],
  ['black hole', []], ['volcanoes', []], ['why do cats purr', []],
];
export const PANEL_SYLLABI = [
  {
    name: 'Panel: high school pacing guide', level: 2,
    text: `Biology pacing guide
Ms. Private  room 214  private@example.org
Homework: Study Island + Quizlet every night

Aug 24-28 Welcome, procedures, lab safety contract
Aug 26 Welcome!! What is life? Characteristics of living things
Sep 14-18 Nature of science and experimental design
Sep 21-25 Macromolecules
Sep 28 Macromolecules (carbs, lipids, proteins, nucleic acids)
Oct 5 Cells!! prokaryotic vs. eukaryotic; organelles
Oct 7 Prokaryotic and eukaryotic cells, organelles
Oct 9 Cells!! prokaryote v eukaryote, organelles LAB: microscope
Oct 12 The cell: prokaryotes vs eukaryotes, organelles
Sept 11 Membranes & transport (diffusion/osmosis/active transport)
Oct 23 Gene expression (lac operon)
Unit 6 - Earth's changing surface: weathering, erosion, plate tectonics
Nov 2 reproductive system & puberty
Nov 4 drugs and alcohol
Nov 9 AP exam prep; sex education unit
SOL LS.1, LS.2, LS.3
May 10 SOL testing window
May 20 Final projects - teach the class`,
    lines: [
      ['What is life? Characteristics', ['characteristics-of-life']],
      ['Sep 21-25 Macromolecules', ['macromolecules']],
      ['Macromolecules (carbs', ['macromolecules', 'carbohydrates', 'lipids', 'protein-structure', 'dna-structure']],
      ['Cells!! prokaryotic vs. eukaryotic', ['organelles', 'bacteria', 'cell-theory']],
      ['Prokaryotic and eukaryotic cells, organelles', ['organelles', 'bacteria', 'cell-theory']],
      ['prokaryote v eukaryote', ['organelles', 'bacteria', 'cell-theory', 'microscopy']],
      ['The cell: prokaryotes vs eukaryotes', ['organelles', 'bacteria', 'cell-theory']],
      ['Membranes & transport', ['cell-membrane', 'diffusion', 'osmosis', 'active-transport']],
      ['Gene expression (lac operon)', ['gene-to-protein', 'gene-regulation']],
    ],
  },
  {
    name: 'Panel: college physiology schedule', level: 5,
    text: `Physiology schedule
1/20 | Water, pH and buffers (Ch 3) | 3
2/20 | Smooth & cardiac muscle compared | 9
2/25 | Renal II: reabsorption & secretion; the loop & countercurrent | 20
2/27 | GI motility and secretion; absorption | 21
3/2 | GI: motility, secretion, digestion & absorption | 22
3/4 | Kidney: secretion and reabsorption | 23`,
    lines: [
      ['Water, pH and buffers', ['ph-and-buffers', 'properties-of-water']],
      ['Smooth & cardiac muscle', ['smooth-muscle-contraction', 'muscle-contraction']],
      ['Renal II', ['kidney', 'concentrating-urine']],
      ['GI motility and secretion', ['gut-motility', 'digestion', 'stomach-acid', 'digestive-control']],
      ['GI: motility, secretion', ['gut-motility', 'digestion', 'stomach-acid', 'digestive-control']],
      ['Kidney: secretion', ['kidney']],
    ],
  },
];

/* Round 2 of the review: the panel's fresh wording, added as quoted before any fix.
   R2_HELP      clear self-harm, abuse or danger wording. The narrow detector should catch most; none
                may ever be answered with a confident lesson. (What it misses still has the page's
                permanent help line.)
   R2_BIOLOGY   biology questions the first gate wrongly refused: they must be matched like any other.
   R2_QUESTIONS [question, right ideas]; [] = no confident answer is right.
   R2_SYLLABI   lines the teacher matcher got wrong. */
export const R2_HELP = [
  'my friend wants to kill herself', 'I think my friend is going to kill himself', 'someone at school keeps hitting me', 'my dad hurts me when he is mad',
  'a grown up touched my private parts', 'someone is hurting me', 'i am scared to go home', 'i feel unsafe', 'i hate my life', 'life is not worth living',
  'I do not want to live', 'i want to kms', 'sucide', 'i dont want to be here anymore', 'how many pills would it take to die', 'i want to end it all', 'how to die',
  'i wish i was dead', 'i cant stop cutting', 'someone at school hurts me', 'my mom hurts me', 'i get hit at home', 'im scared of my stepdad', 'kms', 'unalive',
  'i feel like dying', 'how many pills does it take to die', 'i feel like killing myself', 'my friend says she wants to die', 'i dont wanna be alive',
  'how to take my own life', 'i want to disappear forever', 'my dad beats me', 'someone touched my private parts', 'i was raped', 'my stepdad hits my mom',
  'how to overdose', 'how many pills to overdose', "I don't want to be here anymore", 'my dad hits my mom', 'my stepdad hurts me', 'i want to kil myself',
  'what is the best way to stop breathing', 'my dad hits me', 'i want to kill myself', 'my uncle touches me', 'I wish I was dead',
];
export const R2_BIOLOGY = [
  'how do babies grow', 'how do babies get eye color', 'how are babies born', 'how does alcohol fermentation work in yeast', 'alcohol dehydrogenase mechanism',
  'what is the dose response curve', 'what is dosage compensation in X inactivation', 'how do bacteria become resistant to drugs and antibiotics',
  'how do drugs and receptors interact', 'how is Down syndrome diagnosed with a karyotype', 'what is hCG in a pregnancy test', 'how do anabolic steroids affect muscle',
  'how do flowers have sex', 'how do plants get high yields', 'what is a virgin birth in aphids', 'how does smoking damage the lungs', "do I have my mother's genes",
  'dose response curve', 'how does yeast make alcohol', 'how is sex determined in turtles', 'how does smoking cause lung cancer', 'reward circuitry and addiction',
  'neural basis of anxiety', 'what neurotransmitter is low in depression', 'how do opioids cause respiratory depression', 'how is type 1 diabetes diagnosed',
  'how is cancer diagnosed', 'how do bacteria have sex', 'how does the liver break down alcohol', 'what are the side effects of photosynthesis', 'is the ocean safe for coral',
  'why do we get periods of rapid evolution', 'do I have DNA in my hair', 'do I have bacteria in my stomach', 'are all bacteria dangerous', 'how do identical twins happen',
  'how do babies breathe before they are born', 'how do weed killers work on plants', 'prenatal diagnosis karyotype', 'how does a pregnancy test detect hCG',
  'how does smoking cause mutations in lung cells', 'how do steroids get into a cell', 'what is depression', 'why do I have a period', 'puberty', 'why do we die',
];
export const R2_QUESTIONS = [
  ['how do worms breathe', ['gas-exchange', 'breathing']],
  ['how do i grow taller', []], ['how do i get taller', []], ['why am i so short', []],
  ['lysosome', ['organelles', 'autophagy', 'endocytosis']],
  ['transpiration pull', ['plant-water-transport', 'stomata-and-water-loss']],
  ['how does the body use fat', ['fatty-acid-oxidation', 'lipids', 'fasting-and-starvation', 'digestion']],
  ['plants and animals', []],
  ['innate vs adaptive immunity', ['immunity']],
  ['brain and neurons', ['neuron-structure', 'nervous-system-organization', 'neuron-doctrine']],
  ['what is ATP and why do cells need it', ['atp']],
  ['how do bees pollinate flowers', ['pollination']], ['how do flowers get pollinated', ['pollination']],
  ['how is blood circulated', ['circulation']], ['how do birds migrate', ['seasonal-responses', 'seasonal-rhythms']],
  ['Why Do Sprouting Peas Get Warm?', ['cellular-respiration', 'seed-germination', 'metabolic-rate']],
  ['why am i so fat', []], ['i am fat', []], ['why do I get fat', []],
  ['will i get cancer', ['cancer']], ['how do you know if you have cancer', ['cancer']],
  ['how do periods work', ['menstrual-cycle']],
  ['i am sick', []], ['why do i hear voices', []], ['cutting', []], ['why do I have hair down there', []],
  ['i cant sleep at night', ['circadian-rhythm', 'sleep-regulation', 'sleep-stages']],
  ['why do i sweat so much', ['body-temperature', 'skin']],
  ['how do we smell things', ['smell']],
];
export const R2_SYLLABI = [
  {
    name: 'Round 2: anatomy and physiology', level: 4,
    text: `PHYS 2010 Human Physiology - schedule (subject to change)
Text: Silverthorn, Human Physiology 8e (optional)
Lec | Date | Topic | Reading
1 | 1/20 | Special senses: vision, hearing & balance | 10
2 | 1/22 | Autonomic NS: sympathetic vs parasympathetic | 11
3 | 1/27 | Digestion & absorption of carbs, fats, proteins | 21
4 | 2/3 | EXAM 1 (lectures 1-8) |
5 | 2/5 | Exercise physiology - integrating systems | 25
6 | 2/10 | Mental health & the stress response | 26
7 | 2/12 | Symbiosis (mutualism etc.) | 27
8 | 2/17 | Vitamins, minerals etc. | 22
9 | 2/19 | Weather, climate, etc | 28
10 | 2/24 | Special topics in ecology | 29
FINAL EXAM: Thursday 5/8, 9am-12pm, cumulative`,
    lines: [
      ['Special senses', ['vision', 'hearing', 'sense-of-balance']],
      ['Autonomic NS', ['autonomic-nervous-system']],
      ['Digestion & absorption of carbs', ['digestion']],
      ['Symbiosis (mutualism', ['symbiosis']],
      ['Weather, climate', ['climate']],
    ],
  },
  {
    name: 'Round 2: high school, topics that look like housekeeping', level: 2,
    text: `Week 3: Review of mitosis
Week 6: Final stages of meiosis
Week 7: Test crosses and dihybrid crosses
Week 9: The break-down of glucose
Week 10: Welcome to the nervous system
Lecture 14: Buffer systems and pH
Week 11: Fossils & evidence for evolution / benchmark
Week 12: Microscopes -- how to focus
2 | 8/31, 9/2 | Chemistry review – water, pH, macromolecules | Microscope use
Week 13: Unit test
Week 14: Winter break`,
    lines: [
      ['Review of mitosis', ['cell-division']],
      ['Final stages of meiosis', ['meiosis']],
      ['Test crosses', ['inheritance']],
      ['break-down of glucose', ['glycolysis', 'cellular-respiration']],
      ['Welcome to the nervous system', ['nervous-system-organization']],
      ['Buffer systems and pH', ['ph-and-buffers', 'acid-base-balance']],
      ['Fossils & evidence', ['evidence-for-evolution']],
      ['Microscopes -- how to focus', ['microscopy']],
      ['Chemistry review', ['properties-of-water', 'ph-and-buffers', 'macromolecules', 'microscopy']],
    ],
  },
];

/* Round 3 of the review: more sentences that ask for help (the detector is still a small extra;
   the help line in every reply is what the page relies on), biology that must stay biology, and
   two matcher slips with their neighbours. */
export const R3_HELP = [
  'i want to poison myself', 'i want to hang myself', 'how do i drown myself', 'i want to starve myself', 'i want to be dead', 'i wish i could die',
  'i want to jump off a building', 'I want to sleep forever', 'i want to go to sleep and never wake up', 'i wish i was never born', 'everyone would be happier without me',
  'how do you hang yourself', 'i want to stop breathing', 'help me', 'i need help', 'who can i talk to', 'i want my life to end', 'my best friend says she doesnt want to live',
  'i am being hit', 'my dad choked me', 'i am being abused', 'i want my heart to stop', 'my brother kicks me',
];
export const R3_NOT_HELP = [
  'suicide gene therapy', 'cell suicide', 'help me understand photosynthesis', 'i need help with mitosis', 'how do enzymes help digestion', 'what happens when cells die',
  'how does a fish jump off the water', 'why do muscles get hit by lactic acid',
];
export const R3_LINES = [
  // [a syllabus line, ideas that are right, ideas that must not appear]
  ['Unit 4 Day 2: Test crosses', ['inheritance'], ['meiosis']],
  ['Test crosses and pedigrees', ['inheritance', 'pedigree-analysis'], ['meiosis']],
  ['Monohybrid and test crosses', ['inheritance'], ['meiosis']],
  ['Unit 5: Final stages of mitosis', ['cell-division'], []],
  ['Body organization', [], ['organizer']],
  ['Cell organization', [], ['organizer']],
  ['How the body is organized', [], ['organizer']],
  ['Unit 3: Graphic organizers for cell parts', ['organelles'], ['organizer']],
  ['CNS organization; sleep & memory', [], ['organizer']],
  ['Baroreceptor reflex', ['baroreflex'], ['stretch-reflex']],
];
