/**
 * Every number in the talk "Fast Tools, Slow Thinking" (UVA, 24 Oct 2026) and on the /teachers
 * pages, with where it comes from and what year. Rendered by /teachers/sources.
 *
 * Rules for this file:
 *  - A row needs a source AND a year. If one is missing, the number does not go on the page.
 *  - `how` says how well the number was checked:
 *      primary    checked against the primary source itself
 *      secondary  taken from a secondary report or abstract, not checked against the primary
 *      own        my own data or records (the class numbers are one graduate course, 12 students, anonymized)
 *      site       counted from this site's own repository
 *      history    general historical knowledge
 *  - Groups follow the order of the slides in the talk, then the other /teachers pages.
 */

export type How = 'primary' | 'secondary' | 'own' | 'site' | 'history';

export interface SourceRow {
  /** The number or claim, as it is worded on the page or in the talk. */
  claim: string;
  source: string;
  year: string;
  how: How;
  /** An extra caveat to show under the row. */
  note?: string;
}

export interface SourceGroup {
  id: string;
  /** Slide or page name. */
  title: string;
  /** Shown when the slide has no outside numbers. */
  none?: string;
  rows: SourceRow[];
}

export const HOW_LABEL: Record<How, string> = {
  primary: 'Checked against the primary source',
  secondary: 'Secondary report; not checked against the primary',
  own: 'My own data or records; no outside check',
  site: 'Counted from this site',
  history: 'Well-known background; not re-checked',
};

const COURSE = 'BIOL 7240 / PFN Foundations of Neuroscience I, University of Virginia graduate course, Fall 2026 (12 students, anonymized)';
const REPO = 'Biochemistrypedia repository history and content (origin/main), counted October 23, 2026 at 6:35 pm ET';
const FACTCHECK = 'My fact-check findings for the Cell Signaling course (44 lessons), 2026';

export const SOURCE_GROUPS: SourceGroup[] = [
  {
    id: 'teens',
    title: 'Teens and AI',
    rows: [
      { claim: '54% of US teens used an AI chatbot for schoolwork (fall 2025)', source: 'Pew Research Center, teens and AI', year: '2026 (survey fall 2025)', how: 'primary', note: 'The vote choices in the talk (about 15%, about 35%, more than half) were guesses to vote on, not findings.' },
      { claim: 'About 1 in 10 teens (10%) do all or most of their schoolwork with a chatbot; 21% some; 23% a little', source: 'Pew Research Center, teens and AI (same report)', year: '2026', how: 'primary' },
    ],
  },
  { id: 'landed', title: 'Where I’ve landed', none: 'No outside numbers. These are my own conclusions.', rows: [] },
  {
    id: 'crunch',
    title: 'This is where you work',
    rows: [
      { claim: 'Teachers work about 49 hours a week, around 10 over contract', source: 'RAND, State of the American Teacher', year: '2025', how: 'secondary' },
      { claim: 'Teachers spend about $895 of their own money a year', source: 'AdoptAClassroom, teacher survey (covers the 2024–25 school year)', year: '2025', how: 'primary' },
      { claim: '68% of teachers use AI detectors on student work', source: 'Center for Democracy & Technology, survey of teachers', year: '2023–24', how: 'secondary' },
      { claim: '22.6% of US students were chronically absent', source: 'AEI and Chalkbeat reporting on chronic absence (2024–25 school year)', year: '2026', how: 'primary' },
    ],
  },
  {
    id: 'answerfree',
    title: 'The answer just became free',
    rows: [
      { claim: 'Chegg’s revenue fell from $617.6 million to $376.9 million in one year, down 39%', source: 'Chegg, Form 10-K for fiscal 2025', year: '2025', how: 'primary' },
      { claim: 'College students paid $341 a year for course materials in 2024–25, about half the $701 of 2007–08', source: 'NACS (National Association of College Stores), Student Watch 2024–25', year: '2025', how: 'primary' },
      { claim: 'Publishers’ higher-education revenue was $4.7 billion, up 8.5%', source: 'Association of American Publishers, StatShot annual report', year: '2025', how: 'primary' },
    ],
  },
  {
    id: 'anchor',
    title: 'What we mean by AI',
    rows: [
      { claim: '354 lessons', source: REPO, year: '2026', how: 'site' },
    ],
  },
  {
    id: 'speed',
    title: 'How fast: 17 weeks, then 13 days',
    rows: [
      { claim: 'First commit June 12, 2026. The first 30 lessons took about 17 weeks (to October 10)', source: REPO, year: '2026', how: 'site' },
      { claim: '324 more lessons in 13 days (October 11 to 23)', source: REPO, year: '2026', how: 'site' },
      { claim: '354 lessons, all live, in 11 courses, with 464 films (lesson explainers, scientist profile films and methods films)', source: `${REPO}; films counted from the media manifest`, year: '2026', how: 'site' },
      { claim: 'Grade 7 Life Science: 34 lessons in 8 units (LS.1 to LS.11), planned and released on October 23 (first commit 11:40 am, last lesson merged 6:34 pm ET)', source: REPO, year: '2026', how: 'site' },
      { claim: 'High school Biology: 33 lessons (BIO.1 to BIO.8), all released October 20', source: REPO, year: '2026', how: 'site' },
    ],
  },
  {
    id: 'film',
    title: 'The 60-second film',
    rows: [
      { claim: '354 lessons in 11 courses, 464 short films (repeated from the film’s narration)', source: REPO, year: '2026', how: 'site' },
    ],
  },
  {
    id: 'book',
    title: '500 students wrote a book with me',
    rows: [
      { claim: 'Written with more than 500 students of UVA Biochemistry; 133 profiles of 190 scientists; free as PDF, EPUB and audiobook', source: 'The Molecule Hunters, deppmannlab.com/book (read October 23, 2026)', year: '2026', how: 'primary' },
    ],
  },
  { id: 'rungs', title: 'What building taught me', none: 'No new numbers. 354 lessons is counted above.', rows: [] },
  {
    id: 'checking',
    title: 'Checking: 49 wrong, 453 imprecise',
    rows: [
      { claim: 'An AI fact-checker with web access read 3,468 claims in one course: 49 wrong, 453 imprecise, 287 it could not verify; 841 edits', source: FACTCHECK, year: '2026', how: 'own' },
      { claim: 'Wrong claims per lesson: 4.0 in the first batch (9 lessons), 1.5 in the next, 0.0 to 0.6 in Units 3 to 8 (about 0.3 on average). Said in the talk as "four a lesson at first, under one by the end"', source: FACTCHECK, year: '2026', how: 'own' },
      { claim: 'For Genetics, a second check by a different company’s model found 80 more corrections, for example a trisomy-21 DNA share corrected from 1.5% to 0.8%', source: 'Genetics course fact-check, second-opinion pass (repository commit bf4fc5b)', year: '2026', how: 'own' },
      { claim: 'Expert review takes about 1 to 2 hours per lesson', source: 'My own estimate while reviewing the lessons; not a timed study', year: '2026', how: 'own' },
    ],
  },
  {
    id: 'thursday',
    title: 'Thursday: 2 finished, then 9',
    rows: [
      { claim: 'Pre-work module: 36 steps, about 3 to 4 hours for a careful student. Two of 12 students had finished by Thursday morning; by Friday 8:40 am, nine had and three were partway', source: COURSE, year: '2026', how: 'own', note: 'One small graduate class. Not a sample of any other group.' },
      { claim: 'The “Room” slide: 2 of 8 students said yes, 6 said no, to whether blocking dynein proves TrkA is the cargo', source: COURSE, year: '2026', how: 'own' },
      { claim: 'One predict, argue, reveal cycle took 8 to 10 minutes in the room, not the 4 I had planned', source: COURSE, year: '2026', how: 'own' },
      { claim: 'Lineage of the idea: Just-in-Time Teaching (Novak and colleagues, 1999); formative assessment (Black and Wiliam, 1998)', source: 'Novak et al. 1999; Black and Wiliam 1998', year: '1999; 1998', how: 'history' },
    ],
  },
  {
    id: 'rater',
    title: 'Predict: where they ranked',
    rows: [
      { claim: 'An AI rater’s depth scores tracked answer length (correlation 0.74). The student with the most time on the module ranked second from the bottom of 12', source: COURSE, year: '2026', how: 'own', note: 'My own rater, one course. A warning, not a finding, and not shown for K-12. "Time" is the sum of gaps under 45 minutes between a student’s saved answers, a rough measure.' },
      { claim: 'AI-text detectors flagged 61% of TOEFL essays (written by non-native English speakers) as AI-written', source: 'Liang et al., Patterns', year: '2023', how: 'secondary' },
    ],
  },
  {
    id: 'curiosity',
    title: 'Questions nobody read',
    rows: [
      { claim: 'About a quarter (20 to 25%) of students’ own questions went beyond the lesson; 4 of 12 students asked about 70% of them', source: COURSE, year: '2026', how: 'own' },
    ],
  },
  {
    id: 'shift1',
    title: 'Shift 1: The answer is free. The trail is the evidence.',
    rows: [
      { claim: 'Blue-book sales up 80% at Berkeley over two academic years', source: 'Wall Street Journal report on blue-book sales, as repeated in news coverage (May 2025). I did not see the original article', year: '2025', how: 'secondary' },
      { claim: 'Detectors flagged 61% of TOEFL essays as AI-written', source: 'Liang et al., Patterns', year: '2023', how: 'secondary' },
      { claim: '22% of answers were revised after the reveal', source: COURSE, year: '2026', how: 'own' },
    ],
  },
  {
    id: 'shift2',
    title: 'Shift 2: Your students’ AI reads the lesson before they do.',
    rows: [
      { claim: 'Unguarded GPT-4: practice scores up 48%, later exam scores down 17%', source: 'Bastani et al., Proceedings of the National Academy of Sciences', year: '2025', how: 'secondary' },
      { claim: 'A guarded tutor did not show that harm; a Harvard tutor with guardrails doubled gains on two lessons', source: 'Kestin et al., Scientific Reports', year: '2025', how: 'primary', note: 'All AI-tutor evidence is short-term and not yet replicated.' },
    ],
  },
  {
    id: 'shift3',
    title: 'Shift 3: Materials are easy now. Your attention is the scarce thing.',
    rows: [
      { claim: 'Teachers who use AI every week save about 5.9 hours a week, mostly on preparation', source: 'Gallup and the Walton Family Foundation, teachers and AI', year: '2025', how: 'primary' },
      { claim: 'Just-in-Time Teaching, 1999', source: 'Novak et al., Just-in-Time Teaching', year: '1999', how: 'history' },
    ],
  },
  { id: 'overview', title: 'One idea. Every level.', none: 'A 40-second film with no numbers. It shows one idea at six levels, from toddler to research lab.', rows: [] },
  {
    id: 'shift4',
    title: 'Shift 4: Meet every student where they are.',
    rows: [
      { claim: 'Adaptive software that taught each student at their own level raised math scores 0.36 standard deviations and Hindi 0.22 after about 4.5 months (Mindspark, Delhi). The authors describe "very wide variation in student learning levels within a single grade"', source: 'Muralidharan, Singh and Ganimian, American Economic Review (NBER working paper w22923, abstract)', year: '2019', how: 'primary' },
      { claim: 'Teaching at the Right Level is a "Great Buy"', source: 'Smart Buys report, Global Education Evidence Advisory Panel', year: '2023', how: 'secondary' },
      { claim: 'A later review finds the effects heterogeneous and often modest', source: 'Ardington, Menendez and Thunde, review of Teaching at the Right Level', year: '2026', how: 'secondary' },
      { claim: 'A depth ladder with four steps (grade 7 Life Science, Biology, Biology II, College) on every high school Biology lesson, and a three-setting supports switch', source: REPO, year: '2026', how: 'site' },
    ],
  },
  {
    id: 'shift5',
    title: 'Shift 5: Their questions become the curriculum.',
    rows: [
      { claim: 'Interest in science falls from about age 9 to 17', source: 'Gottfried et al.', year: '2001', how: 'secondary' },
      { claim: 'Curiosity questions: about 2.4 per two hours in kindergarten, about 0.5 in grade 5', source: 'Engel', year: '2011', how: 'secondary' },
    ],
  },
  {
    id: 'goodhart',
    title: 'When a measure becomes a target',
    rows: [
      { claim: 'Goodhart’s law: a statistical regularity tends to collapse once pressure is placed on it for control (UK monetary policy)', source: 'Charles Goodhart', year: '1975', how: 'primary' },
      { claim: '"When a measure becomes a target, it ceases to be a good measure": the common wording, written about examination performance', source: 'Marilyn Strathern, p. 308', year: '1997', how: 'primary' },
      { claim: 'A similar point about social indicators, including test scores', source: 'Donald Campbell. Sources date it 1976 to 1979, so the talk says "in the 1970s"', year: '1970s', how: 'primary' },
      { claim: 'China’s imperial civil-service examinations ran from the Sui dynasty (early 600s) until 1905, about 1,300 years. The talk says "more than a thousand years"', source: 'General historical knowledge', year: '1905', how: 'history' },
    ],
  },
  { id: 'habit', title: 'Understanding is the only thing left worth grading', none: 'No new numbers. "More than 500 students" is sourced under the book slide.', rows: [] },
  {
    id: 'risks',
    title: 'It can go wrong',
    rows: [
      { claim: 'A course AI tutor lowered grades, most for first-generation students', source: 'Liu et al., EdWorkingPaper 26-1598 (University of Maryland trial; not peer-reviewed)', year: '2026', how: 'primary', note: 'Hold it loosely: it has not been through peer review.' },
      { claim: 'Free tools help the already-engaged most', source: 'Reich, on MOOCs', year: '2020', how: 'secondary' },
    ],
  },
  { id: 'close', title: 'What I’d ask of any AI in a classroom', none: 'No numbers. The five commitments are my own.', rows: [] },
  {
    id: 'pages',
    title: 'Other numbers on the /teachers pages',
    rows: [
      { claim: 'A $10,000 grant request (July 2026) said $5,000 would buy three to five complete lessons. It was not selected, and the site was built anyway', source: 'AI Catalyst grant request, July 2026', year: '2026', how: 'own' },
      { claim: 'Model scores, token counts and narration costs in \u201cHow it\u2019s built\u201d', source: 'The project files named next to each figure on that page', year: '2026', how: 'own' },
      { claim: 'Fact-check numbers in the do-it-yourself guide and in \u201cHow it\u2019s built\u201d (3,468 claims, 49 wrong, 453 imprecise, 287 unverifiable, 841 edits; about 4 wrong per lesson at first, under 1 later)', source: FACTCHECK, year: '2026', how: 'own' },
    ],
  },
];
