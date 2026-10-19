/* =============================================================================
   Courses
   -----------------------------------------------------------------------------
   A course is an ordered list of units, and a unit is an ordered list of lesson
   slugs. Membership is by slug (as the homepage units always were) so a typo or
   an unmapped lesson is visible: a lesson whose `course` names a course here but
   whose slug is in none of its units lands in a "New" unit on that course's
   page. It is never silently dropped.

   A lesson says which course it belongs to with `course:` in its frontmatter
   (default "biochemistry"). The homepage shows one card per course, core courses
   first and electives below. Every course has a page at /courses/<slug>/, and
   that page (and its homepage card) exists only once the course has at least one
   published lesson, so adding a course here changes nothing on the live site
   until a lesson in it stops being a draft.
   ============================================================================ */

export interface Unit {
  name: string;
  slugs: string[];
}

export interface Course {
  slug: string;
  title: string;
  /** Where the course sits in a biology degree; the homepage lists each tier separately.
   *  foundation: intro courses for the first two years (1000-2000 level).
   *  core: the 3000-level courses every biology major takes.
   *  elective: 3000-level subjects taken further.
   *  advanced: 4000-level and above, built around current research. */
  tier: 'foundation' | 'core' | 'elective' | 'advanced';
  /** True when the course covers material the MCAT tests; shown as a tag on the homepage card. */
  mcat?: boolean;
  /** One line under the title on the course page and on the homepage card. */
  tagline: string;
  /** A short paragraph for the course page. */
  blurb: string;
  /** Example searches shown in the course page's search box; the site-wide default is used if absent. */
  searchHint?: string;
  units: Unit[];
}

/* Order is the suggested path: within each tier, courses appear in the order a student
   should take them (the homepage numbers the core courses). */
export const COURSES: Course[] = [
  {
    slug: 'organismal-biology',
    title: 'Organismal Biology',
    tier: 'foundation',
    mcat: true,
    tagline: 'How animals and plants are built and how their organs keep them alive.',
    searchHint: 'Try “nephron”, “hemoglobin”, “auxin”…',
    blurb:
      'An introductory course for first- and second-year students. It starts with the problems every organism has to solve and the diversity of ways life solves them, then takes the animal body one system at a time (control, circulation, breathing, digestion, salt and water, immunity, muscle, reproduction and development) and ends with how plants grow, move water and sugar, feed, sense and reproduce.',
    /* Sequence set 2026-10-19, modelled on UVA BIOL 2200 without the laboratory. */
    units: [
      {
        name: 'Organisms and their diversity',
        slugs: ['organism-problems', 'size-and-scaling', 'microbes-protists-fungi', 'animal-body-plans', 'plant-diversity-life-cycles'],
      },
      {
        name: 'Control and constancy',
        slugs: ['tissues-and-homeostasis', 'nervous-control', 'endocrine-system', 'thermoregulation'],
      },
      {
        name: 'Supply and exchange',
        slugs: ['circulation-and-heart', 'blood-and-vessels', 'gas-exchange', 'oxygen-transport', 'digestive-systems'],
      },
      {
        name: 'Water, salts and wastes',
        slugs: ['osmoregulation', 'kidney'],
      },
      {
        name: 'Defense, movement and reproduction',
        slugs: ['innate-immunity', 'adaptive-immunity', 'muscle-and-movement', 'animal-reproduction', 'animal-development'],
      },
      {
        name: 'How plants work',
        slugs: ['plant-body-and-growth', 'plant-transport', 'plant-nutrition', 'plant-signals', 'plant-reproduction'],
      },
    ],
  },
  {
    slug: 'cell-biology',
    title: 'Cell Biology',
    tier: 'core',
    mcat: true,
    tagline: 'How a eukaryotic cell is built, moves things around, divides and lives among other cells.',
    searchHint: 'Try “Golgi”, “kinesin”, “mitosis”…',
    blurb:
      'A core course for biology majors and premedical students. It starts with how cells are measured and how experiments tell mechanisms apart, then follows membranes and compartments, the traffic of proteins and vesicles, the cytoskeleton and motors, the cell cycle, division and cell death, and ends with cells in tissues: adhesion, epithelia, stem cells and cell state.',
    /* Sequence set 2026-10-17 from a curriculum benchmark (six university courses, four textbooks). */
    units: [
      {
        name: 'Seeing and testing cells',
        slugs: ['measured-eukaryotic-cell', 'microscopy-and-images', 'experiments-that-distinguish'],
      },
      {
        name: 'Membranes and compartments',
        slugs: ['membrane-organization-topology', 'membrane-transport', 'organelles-as-environments', 'protein-sorting', 'nuclear-transport', 'quality-control-and-autophagy', 'nuclear-architecture-condensates'],
      },
      {
        name: 'Traffic and movement',
        slugs: ['vesicle-traffic', 'secretory-pathway', 'endocytosis', 'cytoskeleton-dynamics', 'molecular-motors', 'migration-and-cilia'],
      },
      {
        name: 'Division and cell loss',
        slugs: ['cell-cycle-control', 'checkpoints', 'mitosis', 'cytokinesis', 'cell-death'],
      },
      {
        name: 'Cells in tissues',
        slugs: ['adhesion-and-ecm', 'epithelia', 'stem-cells', 'cell-state-and-disease', 'cellbio-experimental-design'],
      },
    ],
  },
  {
    slug: 'genetics',
    title: 'Genetics and Molecular Biology',
    tier: 'core',
    mcat: true,
    tagline: 'How traits are inherited, and how DNA stores, copies and uses the information.',
    searchHint: 'Try “Mendel”, “lac operon”, “CRISPR”…',
    blurb:
      'A core course for biology majors and premedical students. It starts with Mendel and the logic of crosses, follows the gene onto chromosomes and into DNA, then shows how genes are copied, changed, expressed and controlled, how modern tools read and edit genomes, and how genetics works across populations and complex traits.',
    /* Sequence set 2026-10-17 from a curriculum benchmark (six university courses, four textbooks). */
    units: [
      {
        name: 'Inheritance',
        slugs: ['mendels-peas', 'chromosomes-and-meiosis', 'probability-and-crosses', 'extending-mendel', 'pedigrees', 'sex-linkage-and-beyond', 'chromosome-changes'],
      },
      {
        name: 'Mapping and gene function',
        slugs: ['linkage-and-mapping', 'three-point-mapping', 'complementation-and-pathways', 'bacterial-and-phage-genetics'],
      },
      {
        name: 'DNA: copying, changing, repairing',
        slugs: ['dna-the-genetic-material', 'dna-replication', 'mutation', 'dna-repair-and-recombination'],
      },
      {
        name: 'From gene to protein, and its control',
        slugs: ['transcription', 'rna-processing', 'genetic-code-and-translation', 'lac-operon', 'eukaryotic-regulation', 'cancer-genetics'],
      },
      {
        name: 'Tools and genomes',
        slugs: ['recombinant-dna-and-pcr', 'sequencing-and-genomes', 'crispr-and-functional-genomics'],
      },
      {
        name: 'Populations and complex traits',
        slugs: ['population-genetics', 'complex-traits-and-gwas'],
      },
    ],
  },
  {
    slug: 'ecology-evolution',
    title: 'Ecology and Evolution',
    tier: 'core',
    tagline: 'How populations change over generations, and how organisms, populations and ecosystems work together.',
    searchHint: 'Try “finches”, “phylogeny”, “Paine”…',
    blurb:
      'A core course for biology majors and premedical students. It starts with how evolutionary explanations are tested and how to read a tree, follows selection, drift, speciation and the history of life, then moves up the ecological scales: populations, species interactions, communities, ecosystems, and global change and conservation.',
    /* Sequence set 2026-10-17 from a curriculum benchmark (C-ecoevo-benchmark). */
    units: [
      {
        name: 'Evidence and evolutionary reasoning',
        slugs: ['testing-evolutionary-explanations', 'reading-phylogenetic-trees', 'selection-in-ecological-context', 'drift-gene-flow-explanations'],
      },
      {
        name: 'Genomes, development and diversification',
        slugs: ['molecular-evolution', 'evolution-of-development', 'speciation', 'history-of-life', 'human-evolution', 'life-histories'],
      },
      {
        name: 'Environments and populations',
        slugs: ['climate-and-biomes', 'niches-and-distributions', 'demography', 'population-growth', 'spatial-populations'],
      },
      {
        name: 'Interactions and communities',
        slugs: ['competition', 'predation', 'mutualism-parasitism-coevolution', 'diversity-and-succession', 'island-biogeography'],
      },
      {
        name: 'Ecosystem processes',
        slugs: ['energy-flow', 'nutrient-cycling', 'biodiversity-ecosystem-function'],
      },
      {
        name: 'Global change and decisions',
        slugs: ['global-change', 'conservation', 'ecoevo-evidence-workshop'],
      },
    ],
  },
  {
    slug: 'biochemistry',
    title: 'Biochemistry',
    tier: 'elective',
    mcat: true,
    tagline: 'The one-semester sequence: molecules, enzymes, membranes, metabolism.',
    blurb:
      'Thirty lessons that follow a one-semester biochemistry course, from water and weak bonds to the integration of metabolism.',
    /* Course units (approved 2026-08-13). */
    units: [
      { name: 'Foundations', slugs: ['vitalism', 'intro-biochemistry-cell-biology', 'water-weak-bonds'] },
      { name: 'Proteins', slugs: ['amino-acids', 'protein-3d-structure', 'protein-purification-techniques'] },
      { name: 'Enzymes & Binding', slugs: ['enzyme-action-basics', 'enzyme-kinetics', 'protein-binding-allostery'] },
      { name: 'Sugars, Lipids & Membranes', slugs: ['carbohydrates', 'lipids', 'membrane-structure-function'] },
      { name: 'Signaling & Digestion', slugs: ['signal-transduction', 'digestion'] },
      { name: 'Central Metabolism', slugs: ['metabolism-basic-concepts', 'glycolysis', 'gluconeogenesis', 'citric-acid-cycle', 'pyruvate-dehydrogenase', 'oxidative-phosphorylation', 'proton-motive-force'] },
      { name: 'Photosynthesis', slugs: ['light-reactions', 'calvin-cycle'] },
      { name: 'Fuels, Fat & Nitrogen', slugs: ['pentose-phosphate-pathway', 'fatty-acid-degradation', 'fatty-acid-synthesis', 'lipid-synthesis', 'protein-turnover-amino-acid-catabolism'] },
      { name: 'Supplements', slugs: ['nucleotide-metabolism', 'integration-of-metabolism'] },
    ],
  },
  {
    slug: 'neuroscience',
    title: 'Neuroscience',
    tier: 'elective',
    mcat: true,
    tagline: 'How neurons signal, and how circuits of them sense, move, regulate the body, feel, remember and decide.',
    searchHint: 'Try “action potential”, “retina”, “basal ganglia”…',
    blurb:
      'A core course for biology majors and premedical students. It starts with the map of the nervous system and how neurons signal, then synapses and plasticity, the senses, movement, homeostasis and emotion, memory and cognition, and ends with neurodegeneration and how modern experiments test what a circuit does. How the brain is built is taught in Developmental Neuroscience.',
    /* Sequence approved by Chris 2026-10-18: benchmark C-neuro-benchmark (26) plus transmitter systems and neurodegeneration. */
    units: [
      {
        name: 'Neurons and their signals',
        slugs: ['nervous-system-map', 'neurons-and-glia-at-work', 'resting-membrane-passive', 'action-potential'],
      },
      {
        name: 'Synapses and plasticity',
        slugs: ['synaptic-transmission', 'transmitter-systems', 'synaptic-integration', 'synaptic-plasticity'],
      },
      {
        name: 'Sensory systems',
        slugs: ['sensory-coding', 'retina', 'visual-cortex', 'hearing-and-balance', 'touch-and-pain', 'smell-and-taste'],
      },
      {
        name: 'Motor systems',
        slugs: ['motor-units-reflexes', 'basal-ganglia', 'cerebellum'],
      },
      {
        name: 'Homeostasis and affect',
        slugs: ['hypothalamus-autonomic', 'motivation-and-reward', 'emotion-and-stress', 'sleep-and-rhythms'],
      },
      {
        name: 'Cognition and learning',
        slugs: ['memory-systems', 'memory-consolidation', 'language', 'attention-and-decisions'],
      },
      {
        name: 'Evidence and disease',
        slugs: ['neurodegeneration', 'large-scale-neuroscience', 'circuit-experiment-design'],
      },
    ],
  },
  {
    slug: 'signaling',
    title: 'Cell Signaling',
    tier: 'advanced',
    tagline: 'How a cell hears a message and decides what to do next.',
    blurb:
      'An elective that follows the biochemistry course. It starts with the parts every pathway is built from, then takes the pathways one family at a time.',
    units: [
      {
        name: 'How a cell knows anything',
        slugs: ['signals-and-distance', 'finding-a-signal', 'binding-and-dose-response', 'receptor-field-guide', 'signaling-circuits'],
      },
      {
        name: 'The parts: switches and wiring',
        slugs: ['phosphorylation-switch', 'gtpase-switches', 'ubiquitin-and-proteolysis', 'protein-interaction-modules', 'adaptors-and-scaffolds', 'lipid-anchors-and-addresses'],
      },
      {
        name: 'G-protein-coupled receptors and second messengers',
        slugs: ['gpcrs-and-g-proteins', 'camp-and-pka', 'plc-ip3-dag-pkc', 'calcium-signaling', 'turning-signals-off', 'senses-and-cgmp'],
      },
      {
        name: 'Receptors with enzymes attached',
        slugs: ['receptor-tyrosine-kinases', 'ras-to-mapk', 'pi3k-akt-insulin', 'mtor-and-ampk', 'jak-stat', 'tgf-beta-and-smads'],
      },
      {
        name: 'Signals that build and defend an animal',
        slugs: ['wnt-signaling', 'notch-signaling', 'hedgehog-and-cilium', 'integrins-and-rho-gtpases', 'tlr-and-nf-kb', 'antigen-receptors-and-checkpoints'],
      },
      {
        name: 'Channels, the nucleus, and life or death',
        slugs: ['ion-channels-as-receptors', 'nuclear-receptors', 'signaling-to-the-nucleus', 'stress-signals', 'death-receptors-bcl2-caspases'],
      },
      {
        name: 'Space, time and distance',
        slugs: ['shape-of-a-signal', 'endocytosis-and-signaling-endosomes', 'long-distance-signaling-in-neurons', 'exosomes-and-extracellular-vesicles', 'reverse-signaling'],
      },
      {
        name: 'Evolution, disease and tools',
        slugs: ['how-signaling-evolved', 'oncogenes', 'drugs-against-a-part', 'detecting-a-signal', 'hacking-the-cell'],
      },
    ],
  },
  {
    slug: 'developmental-neuroscience',
    title: 'Developmental Neuroscience',
    tier: 'advanced',
    tagline: 'How a nervous system builds itself, one local decision at a time.',
    searchHint: 'Try “netrin”, “Reelin”, “NGF”…',
    blurb:
      'An elective that follows Cell Signaling. It starts with a sheet of embryonic cells and ends with a working, wired brain: how tissue becomes neural, how neurons are made and move, how axons find their targets, why half the neurons die, and how experience refines what the genes began.',
    /* Course units (proposed 2026-10-16, approved by Chris the same day). */
    units: [
      {
        name: 'The problem and the tools',
        slugs: ['wiring-problem', 'neuron-doctrine', 'growth-cone', 'tools-for-development'],
      },
      {
        name: 'Becoming neural',
        slugs: ['the-organizer', 'neural-induction', 'neurulation-and-tube-defects'],
      },
      {
        name: 'Coordinates: patterning the tube',
        slugs: ['hox-and-hindbrain', 'local-organizers', 'shh-bmp-neural-tube', 'motor-neuron-code', 'cortical-areas'],
      },
      {
        name: 'Making neurons',
        slugs: ['radial-glia-progenitors', 'proneural-and-lateral-inhibition', 'asymmetric-division', 'birth-order-and-layers'],
      },
      {
        name: 'Cells on the move',
        slugs: ['radial-migration', 'reelin-and-reeler', 'tangential-migration', 'neural-crest'],
      },
      {
        name: 'Axons find their way',
        slugs: ['neuronal-polarity', 'guidance-cues-and-pioneers', 'netrin-and-dcc', 'crossing-the-midline', 'semaphorins', 'topographic-maps', 'partners-layers-self-avoidance'],
      },
      {
        name: 'Survival and competition',
        slugs: ['naturally-occurring-death', 'neurotrophic-hypothesis', 'trk-and-p75', 'death-machinery-in-neurons', 'competition-for-targets', 'retrograde-signal', 'axon-pruning'],
      },
      {
        name: 'Building synapses',
        slugs: ['neuromuscular-junction', 'cns-synapses', 'synapse-elimination'],
      },
      {
        name: 'Experience refines the wiring',
        slugs: ['spontaneous-activity', 'ocular-dominance', 'critical-period-control', 'microglia-complement-pruning', 'sensitive-periods-behavior'],
      },
      {
        name: 'Glia',
        slugs: ['origins-of-glia', 'myelination', 'glia-metabolic-partners'],
      },
      {
        name: 'Rebuilding, evolving, and going wrong',
        slugs: ['injury-and-regeneration', 'adult-neurogenesis', 'microcephaly-and-malformations', 'synapse-disorders', 'human-brain-expansion', 'organoids'],
      },
    ],
  },
  {
    slug: 'sensory-systems',
    title: 'Sensory Systems',
    tier: 'advanced',
    tagline: 'How touch, pain, itch, the body, sight, sound, smell and taste are sensed, read through current research.',
    searchHint: 'Try “Piezo2”, “Merkel cell”, “TMC1”…',
    blurb:
      'An advanced elective that follows the Neuroscience course. It starts where the textbook account of each sense ends: the genetically defined cell types of the skin, retina, ear, nose and gut, the channels that turn force, heat and chemicals into current, and the circuits that first read them. It covers touch and its receptors in depth, temperature, pain and itch, proprioception and sensing the body from inside, vision, hearing and balance, smell and taste, and ends with how the senses are combined, predicted and restored by prostheses.',
    /* Sequence set 2026-10-19 (starting plan approved by Chris; docs/expansion/SENSORY_AUDIT.md). */
    units: [
      {
        name: 'Transduction and sensory cell types',
        slugs: ['transduction-strategies', 'mechanotransduction-channels', 'sensory-neuron-atlas'],
      },
      {
        name: 'Touch',
        slugs: ['ltmr-classes', 'merkel-cells', 'vibration-corpuscles', 'hairy-skin-and-affective-touch', 'dorsal-horn-touch', 'touch-in-autism-models'],
      },
      {
        name: 'Temperature, pain and itch',
        slugs: ['thermosensation', 'nociceptors-and-sodium-channels', 'spinal-pain-circuits', 'itch', 'chronic-pain'],
      },
      {
        name: 'Proprioception and interoception',
        slugs: ['proprioception', 'vagal-sensory-neurons', 'gut-brain-sensing'],
      },
      {
        name: 'Vision',
        slugs: ['retinal-cell-types', 'direction-selectivity', 'iprgcs', 'photoreceptor-adaptation-and-degeneration'],
      },
      {
        name: 'Hearing and balance',
        slugs: ['hair-cell-transduction-channel', 'cochlear-amplifier', 'hearing-loss-and-repair', 'vestibular-system'],
      },
      {
        name: 'Smell and taste',
        slugs: ['olfactory-receptor-choice', 'olfactory-bulb-and-cortex', 'taste-coding'],
      },
      {
        name: 'Integration and repair',
        slugs: ['multisensory-and-prediction', 'sensory-prostheses'],
      },
    ],
  },
];

/** The course a lesson belongs to. An unknown slug falls back to a bare course
 *  with no units, so its lessons still render and still show up under "New". */
export function courseOf(slug: string): Course {
  return COURSES.find((c) => c.slug === slug) ?? { slug, title: slug, tier: 'elective', tagline: '', blurb: '', units: [] };
}

/** Group a course's lessons into its units, in unit order, keeping each lesson's
 *  running number. Lessons the units do not name are collected under "New". */
export function unitsFor<T extends { data: { slug: string; order?: number } }>(course: Course, lessons: T[]) {
  const sorted = [...lessons].sort((a, b) => (a.data.order ?? 999) - (b.data.order ?? 999));
  const numbered = sorted.map((l, i) => ({ l, n: i + 1 }));
  const mapped = new Set(course.units.flatMap((u) => u.slugs));
  const units = course.units
    .map((u) => ({ name: u.name, entries: numbered.filter(({ l }) => u.slugs.includes(l.data.slug)) }))
    .filter((u) => u.entries.length > 0);
  const unmapped = numbered.filter(({ l }) => !mapped.has(l.data.slug));
  if (unmapped.length > 0) units.push({ name: 'New', entries: unmapped });
  return units;
}

/** Where a course lives. */
export const courseHref = (slug: string) => `/courses/${slug}/`;
