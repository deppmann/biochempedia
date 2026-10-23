/**
 * Shared data for the /teachers section.
 *
 * Every number on these pages comes from the talk brief ("Fast Tools, Slow Thinking",
 * UVA teacher workshop, 24 Oct 2026), its fact files, or a file in this repository that is
 * named next to it, and each one is listed with its source and year on /teachers/sources
 * (see teacher-sources.ts). Nothing here is estimated. If something was never measured,
 * the page says "not measured".
 */

/**
 * The short explainer video the first version of the hub embedded. The hub no longer uses it
 * (the talk deck is embedded instead); /teachers/demo still shows it if the files exist.
 */
export const TALK_VIDEO = {
  dir: '/explainers/teachers-fast-tools-slow-thinking',
  src: '/explainers/teachers-fast-tools-slow-thinking/explainer.mp4',
  poster: '/explainers/teachers-fast-tools-slow-thinking/poster.jpg',
  captions: '/explainers/teachers-fast-tools-slow-thinking/explainer.vtt',
};

/** The public talk deck and its PDF. Refresh with scripts/refresh-teachers-deck.mjs. */
export const TALK = {
  title: 'Fast Tools, Slow Thinking',
  deck: '/teachers/talk/',
  pdf: '/teachers/Fast_Tools_Slow_Thinking.pdf',
};

/** Links shared by the workshop organizers. Google "ouid" parameters are stripped on purpose. */
export const WORKSHOP_LINKS = [
  { label: 'Workshop slides', href: 'https://docs.google.com/presentation/d/1fYs3pOcIeT1v3ZCq0Nba7MJAbhLvvTXjf6EfNF_sISU/edit?usp=sharing' },
  { label: 'Participant-generated resources folder', href: 'https://drive.google.com/drive/folders/1Ddo7MU7mqIyv2xmie92qUAbd4-2EsxCI?usp=sharing' },
  { label: 'VDOE Life Science and Biology resources', href: 'https://drive.google.com/drive/folders/1nxB_oD96PMBMyhqLxYGoOe3PSarvc07a?usp=drive_link' },
  { label: 'High School Biology folder', href: 'https://drive.google.com/drive/folders/1e4JWQOl6B5P-O-84nPl0B96MVSJX_lhh?usp=sharing' },
  { label: 'How-to guide for getting started with generative AI', href: 'https://docs.google.com/document/d/13OUQcej9-WfdL-YXB_ow-Lh7uuP_nGpEAqyZfifUj5U/edit?tab=t.0' },
  { label: 'Prompt library', href: 'https://docs.google.com/document/d/1ob3XcAyp4dVO03DuVWTuVg2SEF9iIV6h/edit?usp=sharing' },
  { label: 'Virginia Science Standards of Learning', href: 'https://www.doe.virginia.gov/teaching-learning-assessment/k-12-standards-instruction/science/standards-of-learning' },
  { label: 'GoOpenVA science plans', href: 'https://goopenva.org/groups/virginia-science/23/651/' },
];

/**
 * The five things the talk asks of any AI tool in a classroom (deck board "Close").
 * `look` is the one-line "what to look for" used on the printable checklist.
 */
export const COMMITMENTS = [
  {
    lead: 'The student tries first.',
    rest: 'It never gives the answer before they commit.',
    look: 'Does it ask for a prediction and a reason before it explains anything? Try it as a student: type "just tell me the answer" and see what happens.',
  },
  {
    lead: 'The teacher sees every exchange.',
    rest: '',
    look: 'Can I see every exchange my students have with it, not a summary? Who else can see them, and when are they deleted?',
  },
  {
    lead: 'It meets each student at their level.',
    rest: 'And tells the teacher who is falling behind.',
    look: 'Can the same task come with more or less support? Does it tell me who is falling behind soon enough for me to do something about it?',
  },
  {
    lead: 'It looks at reasoning.',
    rest: 'And gives second chances.',
    look: 'Does it credit a good reason attached to a wrong answer? Does its score follow the quality of the reasoning, or just how much a student wrote? (My own rater followed length.)',
  },
  {
    lead: 'Everything it makes is checked.',
    rest: 'Mistakes are fixed in public.',
    look: 'Who checked it, and against what? Is there a visible way to report an error and a record of what was changed?',
  },
];

/**
 * Five shifts from the talk (deck boards Shift 1 to 5). NOW is what is happening; NEXT is where
 * the talk thinks it goes. `built` says honestly whether the NEXT part exists yet.
 */
export const SHIFTS = [
  {
    n: 1,
    title: 'The answer is free. The trail is the evidence.',
    side: 'slow' as const,
    now: 'Blue-book sales are reportedly up 80% at Berkeley, because nobody trusts a take-home essay. One study found AI detectors flagged 61% of TOEFL essays, written by non-native English speakers, as AI-written.',
    next: 'How a student got to an answer will count more than what they handed in: the prediction, the reason, the revisions. In my graduate course, 22% of answers were revised after the reveal, and I can see that.',
    teacher: 'You stop guessing from the final product and start reading how a student actually thought.',
    built: 'Partly built: my pre-work records the trail.',
  },
  {
    n: 2,
    title: 'Your students’ AI reads the lesson before they do.',
    side: 'slow' as const,
    now: 'A 2025 study gave students an unguarded GPT-4. Practice scores went up 48%; once the AI was taken away, exam scores fell 17%. A tutor with guardrails, one that would not hand over the answer, did not show that harm.',
    next: 'Lessons written for two readers: the student and their AI tutor. The lesson tells the tutor what to do (ask before you tell), and it is a tutor the teacher controls and can see, every exchange.',
    teacher: 'A tutor that slows the student down, and a window into what they said to it and why.',
    built: 'Not built yet. It is where I want to take the site.',
  },
  {
    n: 3,
    title: 'Materials are easy now. Your attention is the scarce thing.',
    side: 'fast' as const,
    now: 'Teachers who use AI every week save about 5.9 hours a week, mostly on preparation.',
    next: 'Each morning you know which three students to see, and what to ask them: a short list of moves, not a dashboard. This is not new. Just-in-Time Teaching did it in 1999 and stayed small, probably because reading 150 answers overnight takes too long. That is the part AI makes cheap.',
    teacher: 'A view of where each student’s thinking stands before class starts. Check any AI summary against the raw answers.',
    built: 'In use in my graduate courses; I read and send the notes myself.',
  },
  {
    n: 4,
    title: 'Meet every student where they are.',
    side: 'slow' as const,
    now: 'In one grade, students’ levels vary widely. In Delhi, software that taught each student at their own level raised math scores 0.36 standard deviations in 4.5 months. That is one study; Teaching at the Right Level is strong in some places and modest in others, so I hold it loosely.',
    next: 'Every student is checked as they go: sent to a review lesson when they need it, free to race ahead when they are ready, and the teacher is told the moment someone falls behind.',
    teacher: 'You know who needs the review before the test tells you.',
    built: 'A first step is built: a depth ladder on every high school Biology lesson, from grade 7 up to college, and a switch for how much help a student gets. The checking and routing are not.',
  },
  {
    n: 5,
    title: 'Their questions become the curriculum.',
    side: 'slow' as const,
    now: 'Interest in science falls from about age 9 to 17. Curiosity questions drop from about 2.4 per two hours in kindergarten to about 0.5 in grade 5. And we teach to the test.',
    next: 'Students’ own questions are part of the course, and exploring earns credit, not just answering. In my class the same few students asked most of them, so the quiet ones need a way in too.',
    teacher: 'A question is the clearest look at what a student is really thinking about.',
    built: 'Questions are collected in my graduate course; nothing yet answers them all.',
  },
];

/** The three moves that blunt Goodhart's law in a classroom (deck board "Habit"). */
export const MOVES = [
  { lead: 'Measure the thing itself.', rest: 'The reasoning, not a stand-in for it.' },
  { lead: 'Many small looks, not one big test.', rest: 'Low stakes, so nothing is worth gaming. A wrong answer argued well costs nothing in my pre-work.' },
  { lead: 'A person reads it.', rest: 'Judgment, not just a score.' },
];

/** Appended to every prompt, so each one protects the thinking and refuses to invent. */
export const GUARD = `Rules for this task:
- Grade or comment on the quality of the reasoning, not on whether the final answer is correct. A wrong answer argued well is a good answer.
- Do not invent sources, citations, quotations, statistics or standards. If you are not sure something is true, say "I am not sure" instead of guessing.
- Do not do the students' thinking for them. Ask questions or point to where to look; do not hand over the answer unless I ask for an answer key.
- Keep it short and in plain language for a middle or high school class.
- Anything you produce is a draft for me to check before it reaches a student.`;

export interface TeacherPrompt {
  id: string;
  title: string;
  /** What slow-thinking habit this protects. */
  protects: string;
  /** Square-bracket fields are for the teacher to fill in before pasting. */
  body: string;
  /** True if the teacher pastes student writing into it (triggers the privacy reminder). */
  studentText?: boolean;
}

export const PROMPTS: TeacherPrompt[] = [
  {
    id: 'predict-reveal',
    title: 'Predict-then-reveal pre-work on a Virginia SOL topic',
    protects: 'Students commit to a guess and a reason before they see anything.',
    body: `You are helping me write pre-work for my [grade] biology class on this topic: [paste the Virginia SOL biology standard text or your own topic description].

Write 5 predict-then-reveal items. For each item give me:
1. A short scenario or data description a student can read in under a minute (no outside knowledge needed beyond what we have covered: [list what you have taught]).
2. A prediction question with 3 or 4 choices. Make the wrong choices tempting for a real, named misconception, and tell me which misconception each one targets.
3. A prompt that asks the student to write one or two sentences on why they chose it, BEFORE they see anything else.
4. A "reveal" paragraph with the real answer and a short explanation.
5. A one-line note for me on what a good reason looks like and what a weak reason looks like.

Do not write any question whose answer is stated in its own stem.`,
  },
  {
    id: 'misconception-check',
    title: 'Draft a misconception check',
    protects: 'It finds the wrong idea the student is actually holding, instead of rewarding a lucky guess.',
    body: `My [grade] class is learning: [topic]. List the 5 most common student misconceptions about this topic that are documented in biology education. For each one:
1. State the misconception in the words a student would use.
2. Write one short question where a student holding that misconception would pick a specific wrong answer, and a student without it would not.
3. Write a one-sentence follow-up that asks the student to explain their thinking, without telling them they are wrong.

If you are not confident a misconception is a well-documented one, mark it "less certain". Do not name studies or authors unless you are sure they exist.`,
  },
  {
    id: 'where-you-split',
    title: 'Turn anonymous answers into a "where you split" summary',
    protects: 'The room sees its own words, and learns in the first minute that the pre-work was read.',
    studentText: true,
    body: `Below are anonymous answers from my class to this question: [paste the question]. Each answer includes the student's reason. All names and IDs have been removed.

[paste anonymous answers, one per line]

Please:
1. Group the answers by the idea behind them, not by whether they are right. Give each group a plain label.
2. For each group, tell me how many answers are in it and quote one short phrase from the students' own words (copy exactly; do not rewrite).
3. Point out the single most useful split in the room: the place where two reasonable groups disagree.
4. Suggest one question I could ask out loud that makes the two groups argue with each other without telling them who is right.
5. Tell me anything in the answers you could not interpret, rather than guessing.

Only use what is in the answers above. If there are fewer than 8 answers, say that the picture is thin.`,
  },
  {
    id: 'check-summary',
    title: 'Check an AI summary against the raw answers',
    protects: 'It catches the AI telling you a student did nothing when they did.',
    studentText: true,
    body: `I will give you (A) an AI-written summary of one student's pre-work and (B) the raw anonymous answers it was based on. Your job is to audit the summary.

(A) Summary: [paste]
(B) Raw answers: [paste]

List every statement in the summary that is NOT supported by the raw answers, every statement that contradicts them, and anything important in the raw answers that the summary left out. Pay special attention to any claim of "no activity", "did not complete", or "struggled", and check each against the raw text. Quote the raw text that supports your finding. If everything is supported, say so.`,
  },
  {
    id: 'focus-note',
    title: 'A short focus note for one student, from their own answers',
    protects: 'Each student gets a custom start, and it is built from their thinking, not from a template.',
    studentText: true,
    body: `Here is one student's pre-work: the questions, what the student predicted, the reason they wrote, and their confidence before and after. The name and ID have been removed.

[paste one student's anonymous answers]

Write a focus note to the student of 120 to 200 words, in a warm, direct voice, with three parts:
- Where you are: one or two sentences on what the student seems to understand, based only on their answers.
- One or two things you said: quote or closely paraphrase a specific point from their own reasoning that was good or interesting.
- Two or three things to focus on in class: phrased as questions to think about, not as corrections.

Do not say a student did or did not do the work unless it is clearly shown in the text above. If the text is too thin to write a note, say so and write nothing else. I will add the student's name, compare the note with their raw answers, and send it myself.`,
  },
  {
    id: 'route-wrong-answer',
    title: 'Send a wrong answer back to a specific lesson section',
    protects: 'A miss becomes a pointer to where to look, not a verdict.',
    body: `Here is a question I use and the lesson or reading it belongs to.

Question and choices: [paste]
Lesson or reading text (or its list of section headings): [paste]

For each WRONG choice:
1. Describe the thinking that would lead a student to pick it.
2. Name the one section of the lesson (by its heading) that a student should reread, and say in one sentence what to look for there. Do not give the answer.
3. Write a one-line question the student can ask themselves after rereading.

Use only the section headings and text I pasted. If no section addresses a wrong choice, say so; do not make one up.`,
  },
  {
    id: 'three-levels',
    title: 'One idea at three levels',
    protects: 'The science stays the same while the depth changes, so a student who moves up or down a level is not learning something that later has to be taken back.',
    body: `Take this one idea from my [grade] class: [the idea, in one sentence].

Write it three times: for grade 7 Life Science, for high school Biology, and for a first-year college course. The science must be the same at all three levels. A lower level may leave things out, but it must not say anything the next level would have to take back. If a simple wording would be wrong (not just incomplete), choose different wording and tell me why.

After each version add two lines:
- "Leaves out:" what this level skips.
- "New words:" vocabulary that appears at this level for the first time.

Finally, write one question about the idea that a student could answer using any of the three versions, so the whole class can discuss it together.

Do not invent studies, numbers or examples I cannot check. If you are unsure of a claim, mark it "check this".`,
  },
  {
    id: 'supports',
    title: 'Supports without changing the task',
    protects: 'Every student does the same thinking. Only the help differs, and none of the help gives away the answer.',
    body: `Here is a task for my [grade] class, exactly as students will see it:

[paste the task]

Do not change the task and do not make it easier. Write three supports a student can choose to use, and keep the task identical with all of them:
1. A word bank of the terms a student needs, with no definitions or hints that give away the answer.
2. Sentence frames that organize the thinking (for example "I predict ... because ..."), with no science content filled in.
3. A list of labels for a diagram, in alphabetical order, for students to place themselves. Do not place them.

Then check your own work: list anything in the supports that tells a student what the answer is, and rewrite it so it does not.`,
  },
  {
    id: 'reasoning-rubric',
    title: 'A rubric that grades reasoning, not correctness',
    protects: 'A wrong answer argued well earns full credit for thinking.',
    body: `Write a 4-level rubric for grading student reasoning on this task: [paste the prediction question].

The rubric must score the reasoning only. It must give the same credit to a wrong prediction with a careful reason as to a right prediction with a careful reason. Describe each level in one sentence a student could understand, using observable features such as: names a mechanism, uses evidence given in the problem, states what would change their mind, or notices a competing explanation.

Then give me two short example student reasons for each level: one attached to a correct answer and one attached to a wrong answer. Mark the examples as invented illustrations.`,
  },
  {
    id: 'keystone',
    title: 'A "state the rule and what would prove it wrong" item',
    protects: 'Students must say what evidence would change their mind, which is the opposite of recalling a fact.',
    body: `For this topic in my [grade] biology class: [topic], write 3 "keystone" prompts. Each one asks the student to do two things in writing:
1. State, in their own words, the general rule or idea behind what we just studied.
2. Describe a finding or experimental result that would prove their rule wrong.

For each, give me a short note on what a strong answer contains and one common weak answer. Do not write model answers longer than two sentences. Base everything on standard introductory biology; flag anything that is a simplification.`,
  },
  {
    id: 'stuck-note',
    title: 'Turn a "where I\'m stuck" note into a next question',
    protects: 'The student says in writing where they are stuck before anything is explained. You get a question to ask back, not an answer to hand over.',
    studentText: true,
    body: `A student wrote this note about where they are stuck. Name and ID removed.

Topic: [topic]
Stuck note: [paste]

Do not explain the topic. Instead:
1. Say in one sentence what you think the student is actually confused about, and how sure you are.
2. Write two questions I could ask them that would help them find the way out themselves.
3. Suggest one thing in our materials for them to reread ([list your readings]), described by heading, not by page number.

If the note is too vague to work with (fewer than about 25 words, or no specific confusion), tell me what to ask the student to add.`,
  },
  {
    id: 'oral-check',
    title: 'Two or three questions to ask a student out loud',
    protects: 'A short conversation checks whether the reasoning is the student\'s own, without a test and without a detector.',
    studentText: true,
    body: `Below is one student's written reasoning about this question: [paste the question]. The name and ID have been removed.

[paste the student's reasoning]

I want to talk with this student for about two minutes. Write 2 or 3 questions I can ask out loud. Each one should:
- ask the student to explain one step in their own words, or say what finding would change their mind;
- be easy for a student who did the thinking, and hard for a student who pasted someone else's answer.

This is a conversation, not a test. Do not tell me whether the reasoning is right, and do not write answers. If the writing is too short to build questions from, say so instead.`,
  },
  {
    id: 'question-ledger',
    title: 'Sort your students\' own questions into a curiosity list',
    protects: 'Students\' questions become part of the course instead of disappearing.',
    studentText: true,
    body: `Below are questions my students asked this week about [topic], with names removed. Some are about the lesson; some go beyond it.

[paste the anonymous questions, one per line]

1. Group them: questions about the lesson itself; questions that connect to medicine, health or everyday life; questions that go deeper into the science; questions nobody can answer yet.
2. For each group, pick the one question that would make the best 3-minute opener for my next class, and say why.
3. For questions that go beyond what we teach, suggest where a student could look to explore it (describe the kind of source; do not invent specific titles or links).
4. Do not answer the questions yourself. The point is for the class to work on them.`,
  },
  {
    id: 'fact-check',
    title: 'Fact-check a generated passage, claim by claim',
    protects: 'Humans verify what AI drafts. This prompt makes the check visible instead of trusting a smooth paragraph.',
    body: `Below is a passage that was written by an AI tool for my students. Treat it as untrusted.

[paste passage]

1. Split the passage into separate factual claims, numbered.
2. For each claim, label it: "well established", "imprecise or oversimplified", "probably wrong", or "I cannot tell".
3. For anything not "well established", say what is wrong or missing and propose a corrected sentence.
4. Do not give a source, a date, a name, or a number unless you are certain of it. When you are not, write "needs a source" and tell me what to search for.
5. At the end, list the 3 claims I should check against my textbook first.

Be suspicious. Assume there are at least three problems in the passage, and say honestly if you find fewer.`,
  },
  {
    id: 'level-up',
    title: 'Move up a level of abstraction',
    protects: 'It is about ambition, not about speed. Use the time saved to ask a bigger question, not to do the same lesson faster.',
    body: `I have just finished building this: [describe a lesson, a unit, or an activity you already have].

Help me go up one level of abstraction. Suggest 5 more ambitious versions of the same goal, for example: one lesson becoming a whole unit, a standard question becoming a question that points each student back to the specific section they need, or a one-class activity that other teachers could reuse. For each, tell me:
1. What I would have to build.
2. Which part still needs a human expert to check before students see it.
3. The biggest way it could go wrong.

Be realistic about what one teacher can maintain. Do not invent tools or products; if you suggest software, describe the kind of tool rather than naming a product.`,
  },
];

/**
 * Every course on the site, in the order the hub lists them. The hub reads each course's
 * lesson count from the lesson collection, so a count here can never go stale.
 */
export const COURSE_LINKS = [
  { slug: 'life-science', label: 'Life Science (grade 7)' },
  { slug: 'high-school-biology', label: 'Biology (high school)' },
  { slug: 'organismal-biology', label: 'Organismal Biology' },
  { slug: 'cell-biology', label: 'Cell Biology' },
  { slug: 'genetics', label: 'Genetics and Molecular Biology' },
  { slug: 'ecology-evolution', label: 'Ecology and Evolution' },
  { slug: 'biochemistry', label: 'Biochemistry' },
  { slug: 'neuroscience', label: 'Neuroscience' },
  { slug: 'signaling', label: 'Cell Signaling' },
  { slug: 'developmental-neuroscience', label: 'Developmental Neuroscience' },
  { slug: 'sensory-systems', label: 'Sensory Systems' },
];
