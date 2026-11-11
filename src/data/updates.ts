/* =============================================================================
   Updates: what has changed on the site, and what is next  (/updates/)
   -----------------------------------------------------------------------------
   One milestone per thing a visitor would notice, written in plain words. A
   milestone gathers the pull requests behind it; internal tooling with nothing
   to see is left out. Courses get one line each, never lesson by lesson.

   A milestone with `course` takes its lesson count from the live catalog at build
   time, so the number on the page can't go stale, and the pace chart counts that
   course's lessons from its `date`.

   Add a milestone when a notable pull request merges, then refresh the pull
   request dates for the chart:  node scripts/updates-prs.mjs
   ============================================================================ */

export type UpdateKind = 'course' | 'tools' | 'teachers' | 'media' | 'quality' | 'site';

export const KIND_LABEL: Record<UpdateKind, string> = {
  course: 'New courses',
  tools: 'Learning tools',
  teachers: 'For teachers',
  media: 'Films and figures',
  quality: 'Checking and rewriting',
  site: 'The site',
};

export interface Milestone {
  /** The day it went live (YYYY-MM-DD). */
  date: string;
  kind: UpdateKind;
  title: string;
  /** One or two plain sentences: what a visitor can now do or see. */
  text: string;
  /** Pull requests behind it; empty for work merged before the site used them. */
  prs: number[];
  /** For a new course: its slug in src/data/courses.ts. */
  course?: string;
}

export const MILESTONES: Milestone[] = [
  { date: '2026-06-12', kind: 'site', title: 'The first lesson', prs: [1, 3],
    text: 'Enzyme kinetics, written as the model for every lesson after it, and the bare frame of the site.' },
  { date: '2026-08-01', kind: 'course', title: 'Biochemistry goes live', prs: [], course: 'biochemistry',
    text: 'The first course: lessons, films, practice questions and live 3D structures.' },
  { date: '2026-08-12', kind: 'site', title: 'A name and an address', prs: [],
    text: 'The site becomes Biochemistrypedia at biochemistrypedia.com, with automatic checks on every change and a corrections form on every lesson.' },
  { date: '2026-10-09', kind: 'tools', title: 'The Metabolism Arcade', prs: [4, 8, 9, 10, 11, 12],
    text: 'Six games for learning the metabolic pathways, tuned by a student playtester. The metabolism lessons now lead into them, with warm-ups and unit reviews.' },
  { date: '2026-10-11', kind: 'course', title: 'Cell Signaling', prs: [], course: 'signaling',
    text: 'The first advanced elective: how cells sense and answer signals, built out to current research.' },
  { date: '2026-10-17', kind: 'course', title: 'Developmental Neuroscience', prs: [13], course: 'developmental-neuroscience',
    text: 'How a nervous system builds itself, from the neural plate to wiring and pruning.' },
  { date: '2026-10-17', kind: 'course', title: 'Genetics and Molecular Biology', prs: [15, 17], course: 'genetics',
    text: 'The first core course of the biology degree, with a second fact-check before release.' },
  { date: '2026-10-18', kind: 'course', title: 'Cell Biology', prs: [20], course: 'cell-biology',
    text: 'Membranes, organelles, the cytoskeleton and the cell cycle, each with a film and a simulation.' },
  { date: '2026-10-18', kind: 'course', title: 'Ecology and Evolution', prs: [21], course: 'ecology-evolution',
    text: 'Populations, communities and natural selection, with a simulation in every lesson.' },
  { date: '2026-10-18', kind: 'teachers', title: 'Resources for teachers', prs: [24, 82, 83],
    text: 'A teachers’ page: a demo, how the site is built and checked, and a guide for building something like it.' },
  { date: '2026-10-19', kind: 'media', title: 'Figures across the courses', prs: [22, 25, 27, 28, 29, 30, 39, 44, 45],
    text: 'Illustrations in the lessons of every course so far, each checked against its lesson.' },
  { date: '2026-10-19', kind: 'course', title: 'Neuroscience', prs: [34], course: 'neuroscience',
    text: 'The core neuroscience course: neurons, synapses, circuits and systems.' },
  { date: '2026-10-19', kind: 'course', title: 'Sensory Systems', prs: [40, 41, 43, 47, 49], course: 'sensory-systems',
    text: 'An advanced elective on how each sense turns the world into signals.' },
  { date: '2026-10-19', kind: 'course', title: 'Organismal Biology', prs: [38, 46], course: 'organismal-biology',
    text: 'The first Foundations course, for the first two years of a biology degree.' },
  { date: '2026-10-19', kind: 'quality', title: 'A second fact-check and a clarity pass', prs: [26, 32, 33, 35, 36, 42, 54, 55],
    text: 'Every course is checked by a second AI model from a different company, and confusing passages are rewritten.' },
  { date: '2026-10-19', kind: 'tools', title: 'The methods library', prs: [58, 60, 61, 62, 63, 64, 65, 66, 67, 68],
    text: 'Short films on lab methods, from patch clamp to cryo-EM. A method named in a lesson opens its film in a pop-out player.' },
  { date: '2026-10-19', kind: 'site', title: 'A catalog by level', prs: [37],
    text: 'Courses sorted by where they sit in a degree, with an MCAT tag on the ones the exam covers.' },
  { date: '2026-10-20', kind: 'course', title: 'High school Biology', prs: [69, 70, 71, 72, 73, 74, 75], course: 'high-school-biology',
    text: 'A full high school course mapped to the Virginia standards, with a depth switch for extra support.' },
  { date: '2026-10-23', kind: 'course', title: 'Life Science, grade 7', prs: [77, 78, 79, 80, 81], course: 'life-science',
    text: 'A middle school course, one step down the ladder from high school Biology.' },
  { date: '2026-10-25', kind: 'tools', title: 'Paths and a review queue', prs: [85],
    text: 'Suggested paths through the courses, progress saved in your browser, and a queue of questions to review.' },
  { date: '2026-10-25', kind: 'teachers', title: 'Teacher classes', prs: [86, 87],
    text: 'A teacher can make a class, assign lessons and read a morning brief of the answers. Students join with a nickname, no email. Schools can group their teachers.' },
  { date: '2026-10-26', kind: 'teachers', title: 'Feedback on written answers', prs: [88],
    text: 'Optional AI feedback on students’ written answers, using the teacher’s own key, with the teacher able to review it first.' },
  { date: '2026-10-26', kind: 'course', title: 'Physiology', prs: [89, 93, 98], course: 'physiology',
    text: 'How the body’s systems work and keep each other in balance.' },
  { date: '2026-10-26', kind: 'course', title: 'Biology Together, ages 5 to 10', prs: [90, 91, 92, 94, 95, 97, 99, 100], course: 'biology-together',
    text: 'Hands-on activities a parent or teacher does with a child, with setup films and safety notes.' },
  { date: '2026-10-26', kind: 'tools', title: 'MCAT practice', prs: [96],
    text: 'Passage-based practice sets in the style of the exam, a diagnostic, and practice by topic.' },
  { date: '2026-10-30', kind: 'quality', title: 'Checked against the review literature', prs: [101, 102, 103, 104, 105, 108, 109, 112, 114, 115, 120, 129, 130, 132, 134, 135, 136, 137, 138, 141, 150, 151],
    text: 'Every course is checked against published review articles, and the films and figures are corrected to match.' },
  { date: '2026-10-30', kind: 'site', title: 'A new front door and full-text search', prs: [107, 110, 111, 122],
    text: 'A new homepage and course catalog, figures you can tap to enlarge, search across every lesson, and an Under review tag on anything still being checked.' },
  { date: '2026-11-01', kind: 'quality', title: 'Lessons lead with the main idea', prs: [116, 117, 119, 121, 123, 125, 131, 133, 139, 140, 142, 143, 144, 145, 146, 147, 148, 149, 175],
    text: 'Lessons and films are reordered so the main finding comes first and the detail follows.' },
  { date: '2026-11-01', kind: 'media', title: 'A new narration voice', prs: [118, 124, 128],
    text: 'Films are re-voiced with a warmer narration voice.' },
  { date: '2026-11-03', kind: 'quality', title: 'Expert-teacher rewrites', prs: [153, 154, 155, 156, 157, 158, 159, 160, 161, 162, 163, 164, 165, 169, 172, 173, 174],
    text: 'Neuroscience, Sensory Systems and Developmental Neuroscience are rewritten the way the best teacher of each topic would teach it: build the idea, predict before the reveal, and longer films in chapters.' },
  { date: '2026-11-03', kind: 'tools', title: 'Ask a curious question', prs: [168],
    text: 'Type a question and the site suggests the lessons that answer it.' },
  { date: '2026-11-04', kind: 'tools', title: 'Flashcards', prs: [170, 171, 177],
    text: 'A deck beside each rewritten lesson that brings back the cards you miss.' },
  { date: '2026-11-04', kind: 'media', title: 'The Oxygen Bargain', prs: [178],
    text: 'A film on oxygen and the origin of mitochondria.' },
  { date: '2026-11-05', kind: 'tools', title: 'Friendlier math', prs: [180, 181, 182, 183, 184],
    text: 'Equation Cards that walk through each formula, a math toolkit page, and tables that read well on a phone.' },
  { date: '2026-11-06', kind: 'tools', title: 'Listen, highlight and take notes', prs: [185],
    text: 'Lessons read aloud, highlights and a notebook, and an optional learner account that keeps them the same on all your devices.' },
  { date: '2026-11-07', kind: 'quality', title: 'Biochemistry rewritten', prs: [179, 186, 187, 188, 189, 190, 191],
    text: 'Every Biochemistry lesson gets the expert-teacher rewrite, with new figures, simulations and flashcards.' },
  { date: '2026-11-08', kind: 'site', title: 'Faster to the lesson', prs: [192, 195, 196],
    text: 'A contents list in every lesson, links from lessons to MCAT practice, a shelf of recently rewritten lessons, and a homepage and lesson page that get you to the material sooner.' },
  { date: '2026-11-11', kind: 'quality', title: 'Cell Biology rewritten', prs: [221, 223, 224, 225, 226, 228, 229, 230],
    text: 'All 26 Cell Biology lessons get the expert-teacher rewrite: one guiding idea built step by step, prediction checks, new figures and a flashcard deck. Each lesson also has a new film of about five minutes, with its take-home written underneath.' },
  { date: '2026-11-11', kind: 'media', title: 'New films for thirteen Biochemistry lessons', prs: [227, 231, 232],
    text: 'Thirteen Biochemistry lessons, from water and weak bonds to the citric acid cycle, have a new, slower film that walks through the lesson’s main idea, with the take-home written underneath.' },
  { date: '2026-11-10', kind: 'site', title: 'Meet Hex', prs: [219],
    text: 'The hexagon in the logo now has a face. Hex waves from the header, thinks on a search that finds nothing, and cheers when you finish a quiz. There is a page about it at /hex/.' },
  { date: '2026-11-10', kind: 'site', title: 'A more playful site', prs: [216],
    text: 'Faint pond life drifts behind the homepage and course pages, cards lift when you point at them, a sprout grows taller with each level, and a water bear walks above the footer.' },
  { date: '2026-11-10', kind: 'teachers', title: 'A front door for teachers, and a clear licence', prs: [210, 217],
    text: 'The Teachers page now opens with three choices: courses for schools, standards maps, and making a class. Lessons, figures and films are under a Creative Commons licence (CC BY-NC-SA 4.0), explained in plain words at /license/.' },
  { date: '2026-11-10', kind: 'tools', title: 'Search that admits when it finds nothing', prs: [214],
    text: 'A made-up or badly misspelled word no longer returns unrelated lessons.' },
  { date: '2026-11-09', kind: 'site', title: 'A page for every film, and MCAT in the menu', prs: [206],
    text: 'Every film has its own page and there is a Films index. MCAT practice is in the main menu, a lesson shows its reading time and a link to continue where you stopped, and shared links show a proper preview.' },
  { date: '2026-11-10', kind: 'teachers', title: 'A QR code for every lesson, and reading levels', prs: [220],
    text: 'Each lesson has a “Share with your class” button that shows a QR code to put the lesson on students’ phones. The Teachers page lists who each course was written for and its reading grade, and the Films page has a box to find a film by word.' },
  { date: '2026-11-10', kind: 'media', title: 'More figures in Signaling and Developmental Neuroscience', prs: [218],
    text: 'About a hundred new illustrations across 50 lessons that had one picture or none, each drawn for one section and checked against the lesson by a second reviewer before it went in.' },
  { date: '2026-11-09', kind: 'site', title: 'Easier for AI assistants to read and cite', prs: [203],
    text: 'Every lesson now has a plain-text copy for AI assistants, with a site guide at /llms.txt and a catalog of every course, so when an assistant answers a question from a lesson it can quote it accurately and link back to it.' },
  { date: '2026-11-09', kind: 'quality', title: 'Physiology rewritten', prs: [202, 204, 205],
    text: 'Physiology lessons get the expert-teacher rewrite: one guiding idea built step by step, prediction checks, new figures and a flashcard deck. All 30 lessons are done, and each lesson now has a read-aloud voice.' },
  { date: '2026-11-09', kind: 'site', title: 'A plainer headline and a tidier footer', prs: [201],
    text: 'The homepage now opens with “From a first question to current research,” and the footer is shorter, with links grouped into Learn, Teach, This site and From the lab.' },
  { date: '2026-11-09', kind: 'tools', title: 'Abbreviations explained, and a feed for this page', prs: [200],
    text: 'Abbreviations in lessons are spelled out at their first use in each section, and tapping one shows what it stands for. This page now has a feed you can follow, and each change under a milestone is described in plain words.' },
  { date: '2026-11-08', kind: 'site', title: 'This page', prs: [198, 199],
    text: 'A record of what has changed on the site, how fast it is being built, and where it is going next.' },
  { date: '2026-11-08', kind: 'site', title: 'Privacy for learners and classes, spelled out', prs: [197],
    text: 'The privacy pages explain how an optional learner account and a teacher’s class stay separate, and why a class never needs an account.' },
  { date: '2026-11-08', kind: 'teachers', title: 'Flashcards in the teacher’s brief', prs: [193],
    text: 'A teacher can assign a lesson’s flashcards and see the cards the class misses most.' },
  { date: '2026-11-08', kind: 'media', title: 'A figure in every Neuroscience lesson', prs: [194],
    text: 'Figures drawn so a reader skimming the lesson still gets the point of each section.' },
];

/* Where we're going. General and without dates: a direction, not a promise.
   Waiting for Chris's read, so the page shows it with an Under review tag. */
export const ROADMAP_UNDER_REVIEW = true;
export const ROADMAP: { when: string; items: { title: string; text: string }[] }[] = [
  {
    when: 'Next few weeks',
    items: [
      { title: 'Expert-teacher rewrites for more courses', text: 'Genetics and Cell Signaling next, then the Foundations and school courses.' },
      { title: 'A figure in every lesson', text: 'Every course, drawn so a skimming reader gets the point of each section.' },
      { title: 'Flashcards for every rewritten course', text: 'Each rewritten lesson gets its own deck.' },
    ],
  },
  {
    when: 'Coming months',
    items: [
      { title: 'More MCAT practice', text: 'Passage sets beyond biochemistry, across biology, physiology and the other sciences the exam covers.' },
      { title: 'The sciences beyond biology', text: 'Stand-alone courses in general chemistry, organic chemistry and physics.' },
      { title: 'More of the biology degree', text: 'The rest of the first two years, and further electives such as cell death.' },
    ],
  },
];
