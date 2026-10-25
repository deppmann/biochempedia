/* "I'm here for…" paths. Each path is an ordered list of courses (slugs from
   courses.ts) plus a few honest notes. The choice is remembered on the
   learner's device only (src/lib/progress.ts); nothing here needs an account.

   Keep notes factual and modest: say what is not built yet, never compare the
   site with any commercial test-prep product. */

export interface PathStep {
  course: string;
  /** Why this course sits here on the path (one line). */
  why: string;
  optional?: boolean;
}

export interface LearningPath {
  id: string;
  /** Short label for the chooser card. */
  label: string;
  title: string;
  who: string;
  blurb: string;
  steps: PathStep[];
  notes?: { text: string; links?: { label: string; href: string }[] }[];
  extras?: { label: string; href: string }[];
}

export const PATHS: LearningPath[] = [
  {
    id: 'mcat',
    label: 'Get ready for the MCAT',
    title: 'Preparing for the MCAT',
    who: 'Pre-med and pre-health students',
    blurb: 'The biology and biochemistry the exam leans on, in a sensible order, with original MCAT-style questions at the end of every lesson and a review queue that brings back what you missed.',
    steps: [
      { course: 'biochemistry', why: 'Biochemistry runs through both science sections that test biology.' },
      { course: 'cell-biology', why: 'Cells, membranes, transport and signaling, which sit under most passages.' },
      { course: 'genetics', why: 'Inheritance, gene expression and the experiments that show how we know.' },
      { course: 'organismal-biology', why: 'How whole organisms work: organ systems, physiology and homeostasis.' },
      { course: 'neuroscience', why: 'Neurons, synapses and systems, for the biology and the psychology sections.' },
      { course: 'sensory-systems', why: 'Sensation and perception in depth, a topic the psychology section tests.', optional: true },
    ],
    notes: [
      {
        text: 'The exam also tests general and organic chemistry, physics, psychology and sociology, and critical reading (CARS). Those courses are not built here yet.',
      },
      {
        text: 'The official practice materials and the fee assistance program come from the exam’s maker, the AAMC.',
        links: [
          { label: 'AAMC: prepare for the MCAT exam', href: 'https://students-residents.aamc.org/prepare-mcat-exam/prepare-mcat-exam' },
          { label: 'AAMC Fee Assistance Program', href: 'https://students-residents.aamc.org/fee-assistance-program/fee-assistance-program' },
        ],
      },
    ],
    extras: [{ label: 'Play the Metabolism Arcade', href: '/play' }],
  },
  {
    id: 'major',
    label: 'Follow a biology major',
    title: 'Following a biology major',
    who: 'College students, or anyone who wants the degree’s worth of biology',
    blurb: 'The courses in the order a biology major takes them: a foundation, then the core, then electives that go deeper.',
    steps: [
      { course: 'organismal-biology', why: 'Foundation: how living things are built and how they work.' },
      { course: 'cell-biology', why: 'Core: the cell, its parts and how they cooperate.' },
      { course: 'genetics', why: 'Core: genes, inheritance and gene expression.' },
      { course: 'ecology-evolution', why: 'Core: populations, communities and the history of life.' },
      { course: 'biochemistry', why: 'Core: the chemistry that runs the cell.' },
      { course: 'neuroscience', why: 'Core: the nervous system from molecules to behavior.' },
      { course: 'signaling', why: 'Elective: how cells talk to each other.', optional: true },
      { course: 'developmental-neuroscience', why: 'Elective: how a nervous system builds itself.', optional: true },
      { course: 'sensory-systems', why: 'Advanced elective: touch, sight, sound, smell and taste.', optional: true },
    ],
  },
  {
    id: 'curious',
    label: 'Learn for the love of it',
    title: 'Learning for the love of it',
    who: 'Lifelong learners, parents, anyone curious',
    blurb: 'No exam, no order you have to follow. Start with whatever you have wondered about. The films are a good way in, and the quizzes are there if you want them.',
    steps: [
      { course: 'ecology-evolution', why: 'Why there are so many kinds of living things, and how they shape each other.' },
      { course: 'neuroscience', why: 'How a brain makes a mind, from one neuron up.' },
      { course: 'sensory-systems', why: 'How you touch, see, hear, smell and taste the world.' },
      { course: 'organismal-biology', why: 'How bodies, plants and animals actually work.' },
      { course: 'cell-biology', why: 'The world inside a cell.' },
    ],
    extras: [
      { label: 'Play the Metabolism Arcade', href: '/play' },
      { label: 'The methods library: how scientists find things out', href: '/methods/' },
    ],
  },
  {
    id: 'school',
    label: 'I’m in grades 7 to 12',
    title: 'Middle and high school',
    who: 'Students in grades 7 to 12, following the Virginia standards',
    blurb: 'Grade 7 Life Science, then high school Biology. Every lesson has a switch for how much help you get, and a ladder that shows the idea one level down and one level up.',
    steps: [
      { course: 'life-science', why: 'Grade 7: cells, ecosystems, heredity and change.' },
      { course: 'high-school-biology', why: 'High school: the full Virginia Biology course, BIO.1 to BIO.8.' },
      { course: 'cell-biology', why: 'Ready for more? The college course, one step up the ladder.', optional: true },
    ],
  },
  {
    id: 'teach',
    label: 'Teach with it',
    title: 'Teaching with it',
    who: 'Teachers, homeschooling parents, tutors',
    blurb: 'Free to use with your classes. Set the level of help for a whole class with one link, and see the standards map for each course.',
    steps: [
      { course: 'life-science', why: 'Grade 7, mapped to Virginia’s Life Science standards.' },
      { course: 'high-school-biology', why: 'High school Biology, mapped to BIO.1 to BIO.8.' },
      { course: 'organismal-biology', why: 'An introductory college course, for advanced students.', optional: true },
    ],
    extras: [
      { label: 'Resources for teachers', href: '/teachers/' },
      { label: 'High school Biology for teachers', href: '/teachers/biology/' },
      { label: 'Life Science for teachers', href: '/teachers/life-science/' },
    ],
  },
];

export const pathOf = (id: string | undefined) => PATHS.find((p) => p.id === id);
