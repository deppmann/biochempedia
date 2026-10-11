/* =============================================================================
   Courses
   -----------------------------------------------------------------------------
   A course is an ordered list of units, and a unit is an ordered list of lesson
   slugs. Membership is by slug (as the homepage units always were) so a typo or
   an unmapped lesson is visible: a lesson whose `course` names a course here but
   whose slug is in none of its units lands in a "New" unit on that course's
   page. It is never silently dropped.

   A lesson says which course it belongs to with `course:` in its frontmatter
   (default "biochemistry"). Biochemistry is the homepage. Every other course
   gets a page at /courses/<slug>/, and that page exists only once the course has
   at least one published lesson, so adding a course here changes nothing on the
   live site until a lesson in it stops being a draft.
   ============================================================================ */

export interface Unit {
  name: string;
  slugs: string[];
}

export interface Course {
  slug: string;
  title: string;
  /** One line under the title on the course page and on the homepage card. */
  tagline: string;
  /** A short paragraph for the course page. */
  blurb: string;
  units: Unit[];
}

export const COURSES: Course[] = [
  {
    slug: 'biochemistry',
    title: 'Biochemistry',
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
    slug: 'signaling',
    title: 'Cell Signaling',
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
];

/** The course a lesson belongs to. An unknown slug falls back to a bare course
 *  with no units, so its lessons still render and still show up under "New". */
export function courseOf(slug: string): Course {
  return COURSES.find((c) => c.slug === slug) ?? { slug, title: slug, tagline: '', blurb: '', units: [] };
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
