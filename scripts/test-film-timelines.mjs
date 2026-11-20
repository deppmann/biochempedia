#!/usr/bin/env node
/* Tests for the film timelines (scripts/film-timelines/lib.mjs): scene matching on small fixtures,
   including the caption quirks found in the real films; the lesson outline; the rule that a mapped
   figure never appears before the film has given the answer it shows; and the coverage of the real
   library, which must be the same on every run.

   Run: node scripts/test-film-timelines.mjs   (in `npm test` and in CI) */
import { join } from 'node:path';
import { fileURLToPath } from 'node:url';
import { parseVtt, transcriptLines, sceneTimes, timingStatus, lessonOutline, filmRegion, applyMap, saidAt, jsxAttrs } from './film-timelines/lib.mjs';
import { coverage } from './film-timelines/report.mjs';

const ROOT = join(fileURLToPath(new URL('.', import.meta.url)), '..');
let failed = 0;
let passed = 0;
const ok = (cond, name, detail = '') => { if (cond) passed++; else { failed++; console.error(`✗ ${name}${detail ? `: ${detail}` : ''}`); } };
const eq = (a, b, name) => ok(JSON.stringify(a) === JSON.stringify(b), name, `got ${JSON.stringify(a)}, wanted ${JSON.stringify(b)}`);

const vtt = (rows) => `WEBVTT\n\n${rows.map(([a, b, t], i) => `${i + 1}\n00:00:${a.toFixed(3).padStart(6, '0')} --> 00:00:${b.toFixed(3).padStart(6, '0')}\n${t}`).join('\n\n')}\n`;

/* ---- captions */
{
  const cues = parseVtt(vtt([[3.4, 5.38, 'Remember the <b>salted</b> cucumber?'], [6.7, 9.9, 'The first film showed a drift, from crowded to less'], [9.9, 14.2, 'crowded. This time, salt &amp; water.']]));
  eq(cues.length, 3, 'parseVtt reads three cues');
  eq(cues[0], { start: 3.4, end: 5.38, text: 'Remember the salted cucumber?' }, 'parseVtt drops tags and keeps times');
  eq(cues[2].text, 'crowded. This time, salt & water.', 'parseVtt decodes entities');
  const lines = transcriptLines(cues);
  eq(lines.length, 2, 'a sentence split over two cues is one transcript line');
  eq(lines[1].start, 6.7, 'the joined line keeps the start of its first cue');
}

/* ---- scene times */
const SCRIPT = {
  scenes: [
    { id: 's00_title', silent: 3, narration: '' },
    { id: 's01_hook', narration: 'Every dye particle moves at random. So why does colour spread?' },
    { id: 's02_predict', narration: 'Which way will more dots cross? Pause and decide.' },
    { id: 's03_pause', silent: 5, narration: '' },
    { id: 's04_reveal', narration: 'On average, more cross from left to right.' },
    { id: 's05_rule', narration: 'So here is the rule. Particles move at random.' },
    { id: 's06_end', silent: 4, narration: '' },
  ],
};
const CUES = parseVtt(vtt([
  [3.4, 6.0, 'Every dye particle moves at random.'],
  [6.5, 9.0, 'So why does colour spread?'],
  [10.0, 13.0, 'Which way will more dots cross?'],
  [13.4, 15.0, 'Pause and decide.'],
  [20.2, 24.0, 'On average, more cross from left to right.'],
  [25.0, 27.0, 'So here is the rule.'],
  [27.5, 30.0, 'Particles move at random.'],
]));
{
  const t = sceneTimes(SCRIPT, CUES, 34);
  eq(t.scenes.map((s) => s.start), [0, 3.4, 10, 15, 20.2, 25, 30], 'every scene gets its start');
  eq([t.spoken, t.matched], [4, 4], 'four spoken scenes, four found');
  eq(timingStatus(t), 'timed', 'status is timed');
  eq(t.scenes.map((s) => s.kind), ['title', 'spoken', 'question', 'pause', 'spoken', 'spoken', 'end'], 'kinds: the scene before a pause is the question');
  eq(t.questions, [{ scene: 's02_predict', pause: 's03_pause', reveal: 's04_reveal', start: 10, revealStart: 20.2, text: 'Which way will more dots cross? Pause and decide.' }], 'the question and where its answer starts');
  eq(t.scenes[5].end, 30, 'a scene ends where the next starts');
  eq(t.scenes[6].end, 34, 'the last scene ends with the film');
}
{
  // "Particles move at random" is also how the film ends: the hook must not be pulled there, and the
  // rule scene must not be matched to the hook's cue.
  const t = sceneTimes({ scenes: [{ id: 'a', narration: 'Particles move at random. That is all.' }, { id: 'b', narration: 'Now a tank.' }, { id: 'c', narration: 'Particles move at random. Again.' }] },
    parseVtt(vtt([[1, 3, 'Particles move at random.'], [3.2, 4, 'That is all.'], [5, 6, 'Now a tank.'], [7, 9, 'Particles move at random.'], [9.2, 10, 'Again.']])), 11);
  eq(t.scenes.map((s) => s.start), [1, 5, 7], 'a repeated phrase is matched in order, never backwards');
}
{
  // The quirk in the real captions: the spoken form of a number leaks into the cue ("about minus −65 mV"),
  // and a scene can open with a figure the voice text spells out.
  const script = { scenes: [
    { id: 'rest', tts: 'The trace starts flat. This is rest, at about minus 65 millivolts.', caption: 'The trace starts flat. This is rest, at about −65 mV.', narration: 'The trace starts flat. This is rest, at about −65 mV.' },
    { id: 'peak', tts: 'Plus 40 millivolts is the peak of the spike.', caption: '+40 mV is the peak of the spike.', narration: '+40 mV is the peak of the spike.' },
    { id: 'year', tts: 'Nineteen thirty-nine. Hodgkin and Huxley recorded this.', narration: '1939. Hodgkin and Huxley recorded this.' },
  ] };
  const cues = parseVtt(vtt([[1, 2.2, 'The trace starts flat.'], [2.5, 5, 'This is rest, at about minus −65 mV.'], [6, 9, 'Plus +40 mV is the peak of the spike.'], [10, 11, 'Nineteen thirty-nine.'], [11.2, 14, 'Hodgkin and Huxley recorded this.']]));
  const t = sceneTimes(script, cues, 15);
  eq(t.scenes.map((s) => s.start), [1, 6, 10], 'spoken numbers: each scene still starts with its cue');
  eq(t.matched, 3, 'spoken numbers: all three found');
}
{
  // One sentence split over two cues, and the next scene begins inside the second cue.
  const script = { scenes: [{ id: 'a', narration: 'The drift runs from crowded to less crowded.' }, { id: 'b', narration: 'This time the crowded particle is salt.' }] };
  const cues = parseVtt(vtt([[1, 5, 'The drift runs from crowded to less'], [5, 9, 'crowded. This time the crowded particle is salt.']]));
  const t = sceneTimes(script, cues, 10);
  ok(t.scenes[1].start > 5 && t.scenes[1].start < 6, 'a scene that begins inside a cue starts after the words before it', String(t.scenes[1].start));
}
{
  // The voice text spells an abbreviation out ("B R D U"); the caption prints it. The scene is found by
  // its next words and starts with its cue.
  const cues = parseVtt(vtt([[1, 3, 'Here is a cell with a wall.'], [4, 6, 'BrdU marks new DNA.'], [7, 9, 'Now count the labelled cells.']]));
  const spelled = sceneTimes({ scenes: [{ id: 'a', narration: 'Here is a cell with a wall.' }, { id: 'b', narration: 'B R D U marks new DNA.' }, { id: 'c', narration: 'Now count the labelled cells.' }] }, cues, 10);
  eq(spelled.scenes.map((s) => s.start), [1, 4, 7], 'a spelled-out abbreviation: the scene starts with its cue');
  // A scene whose words are not in the captions at all joins the scene before it; nothing later is thrown off.
  const t = sceneTimes({ scenes: [{ id: 'a', narration: 'Here is a cell with a wall.' }, { id: 'b', narration: 'A line that the captions never carried.' }, { id: 'c', narration: 'Now count the labelled cells.' }] }, cues, 10);
  eq(t.scenes.map((s) => s.start), [1, null, 7], 'an unfound scene has no start of its own');
  eq([t.matched, t.spoken], [2, 3], 'two of three found');
  eq(timingStatus(t), 'untimed', 'two in three is below the bar for a timeline');
  eq(t.scenes[0].end, 7, 'the scene before an unfound one runs on to the next found scene');
}
{
  // A question that names the thing its answer opens with: three matching words inside the question's
  // own cue must not be taken for the start of the answer.
  const t = sceneTimes({ scenes: [{ id: 'q', narration: 'Which part should face the receptor: the SH2 cup or an SH3 grip?' }, { id: 'q_pause', silent: 4, narration: '' }, { id: 'r', narration: 'The SH2 cup closes around the receptor.' }] },
    parseVtt(vtt([[1, 6, 'Which part should face the receptor: the SH2 cup or an SH3 grip?'], [7, 9, 'Keep your choice in mind.'], [12, 15, 'The SH2 cup closes around the receptor.']])), 16);
  eq(t.scenes.map((s) => s.start), [1, 9, 12], 'the answer starts at its own cue, not inside the question');
  eq(t.questions[0]?.revealStart, 12, 'so the question stays up until the film answers');
  const n = sceneTimes({ scenes: [{ id: 'a', tts: 'You need six to ten earthworms.', narration: 'You need six to ten earthworms.' }] }, parseVtt(vtt([[1, 4, 'You need 6 to 10 earthworms.']])), 5);
  eq(n.scenes[0].start, 1, 'small numbers match whether spelled or printed');
}
eq(timingStatus({ spoken: 10, matched: 9 }), 'partial', 'nine in ten is a partial timeline');
eq(saidAt(CUES, 'more cross from left to right'), 20.2, 'saidAt finds the cue in which the film says a phrase');
eq(saidAt(CUES, 'more cross from right to left'), null, 'saidAt refuses words the film does not say');

/* ---- the lesson */
const MDX = `---
title: "T"
---
import LessonFigure from '../../../components/LessonFigure.astro';

## Explore: change the salt

Text.

<LessonFigure src="/figures/x/one.webp" width={1200} height={800} keyItems={["water", "salt"]} alt="AI-generated illustration: one." caption="First &amp; foremost." />

## Explain: water crosses a *choosy* membrane

<LessonFilm film={frontmatter.films[0]} />

### When does the drift stop?

<ScaffoldFigure src="/figures/x/two.webp" width={1200} height={800} keyItems={["water", "salt"]} given={[0]} alt="AI-generated illustration: two." caption="Second." />

\`\`\`
## not a heading
\`\`\`

## Explore: change the salt

<LessonFilm film={frontmatter.films[1]} />

<LessonFigure src="/figures/x/three.svg" alt="AI-generated illustration: three." caption="Third." />
`;
{
  const o = lessonOutline(MDX);
  eq(o.headings.map((h) => h.id), ['explore-change-the-salt', 'explain-water-crosses-a-choosy-membrane', 'when-does-the-drift-stop', 'explore-change-the-salt-1'], 'heading ids match the lesson page (inline marks dropped, repeats numbered, code skipped)');
  eq(o.films.map((f) => [f.index, f.heading]), [[0, 'explain-water-crosses-a-choosy-membrane'], [1, 'explore-change-the-salt-1']], 'each film sits under a heading');
  eq(o.figures.map((f) => [f.src, f.scaffold, f.keyItems.length, f.caption]), [['/figures/x/one.webp', false, 2, 'First & foremost.'], ['/figures/x/two.webp', true, 0, 'Second.'], ['/figures/x/three.svg', false, 0, 'Third.']], 'figures: a scaffold figure keeps its key words back');
  const first = filmRegion(o, null);
  eq([first.section?.id, first.figures.map((f) => f.src)], ['explore-change-the-salt', ['/figures/x/one.webp']], 'the opening film covers the lesson up to the next film');
  const second = filmRegion(o, 0);
  eq([second.section?.id, second.sections.map((s) => s.id), second.figures.map((f) => f.src)], ['explain-water-crosses-a-choosy-membrane', ['explain-water-crosses-a-choosy-membrane'], ['/figures/x/two.webp']], 'a later film covers from its heading to the next film');
  eq(filmRegion(o, 1).figures.map((f) => f.src), ['/figures/x/three.svg'], 'the last film covers to the end');
  eq(jsxAttrs(`<X a="1" b={2} c={["x","y"]} d={'q'} />`), { a: '1', b: 2, c: ['x', 'y'], d: 'q' }, 'jsxAttrs reads strings, numbers and lists');
}

/* ---- maps: a figure never comes before the answer it shows */
{
  const times = sceneTimes(SCRIPT, CUES, 34);
  const outline = lessonOutline(MDX);
  const base = () => ({
    film: 'x/explainer',
    checked: { by: 'test', on: '2026-11-20' },
    parts: [
      { from: 's00_title', title: 'A drop spreads' },
      { from: 's02_predict', question: true },
      { from: 's04_reveal', title: 'The answer, and why' },
      { from: 's05_rule', title: 'The rule', section: 'explore-change-the-salt', term: { word: 'Rule', def: 'Particles move at random' }, figure: { src: '/figures/x/one.webp', answers: 's02_predict' } },
    ],
  });
  const run = (edit) => { const m = base(); edit?.(m); return applyMap(m, times, outline, 'x/explainer', CUES); };
  const good = run();
  eq(good.problems, [], 'a sound map has no problems');
  eq(good.parts.map((p) => p.start), [0, 10, 20.2, 25], 'parts start with their scenes (the first at zero)');
  eq(good.parts[1].question, 'Which way will more dots cross? Pause and decide.', 'a question part carries the film\'s own words');
  eq(good.parts[3].figure.alt, 'AI-generated illustration: one.', 'figure text is copied from the lesson');
  eq(good.parts[3].term.at, 27.5, 'a word comes up at the cue in which the film says it');
  const bad = (edit, re, name) => { const r = run(edit); ok(r.problems.some((p) => re.test(p)), name, JSON.stringify(r.problems)); };
  bad((m) => { m.parts[0].figure = { src: '/figures/x/one.webp', answers: 's02_predict' }; }, /before the film gives the answer/, 'REFUSED: a figure that answers the question, shown before the reveal');
  bad((m) => { m.parts[1].figure = { src: '/figures/x/one.webp', answers: null }; }, /question part carries only/, 'REFUSED: a figure on the question itself');
  bad((m) => { delete m.parts[3].figure.answers; }, /must say what it gives away/, 'REFUSED: a figure with no judgement recorded');
  bad((m) => { m.parts[3].figure.answers = 's05_rule'; }, /not a question scene/, 'REFUSED: "answers" naming a scene that asks nothing');
  bad((m) => { m.parts.splice(2, 0, { from: 's03_pause', title: 'Thinking' }); }, /between the question/, 'REFUSED: a part that begins between a question and its answer');
  bad((m) => { m.parts.splice(1, 1); }, /needs a part for it/, 'REFUSED: a map that swallows the film\'s question');
  bad((m) => { delete m.parts[1].question; m.parts[1].title = 'Which way?'; }, /mark the part "question"/, 'REFUSED: a question scene not marked as one');
  bad((m) => { m.parts[2].from = 's05_rule'; m.parts.pop(); }, /must start at its reveal scene/, 'REFUSED: the part after a question starting later than the reveal');
  bad((m) => { m.parts[3].figure.src = '/figures/x/nine.webp'; }, /not a figure in this lesson/, 'REFUSED: a figure the lesson does not have');
  bad((m) => { m.parts[3].section = 'no-such-heading'; }, /no heading with the id/, 'REFUSED: a section the lesson does not have');
  bad((m) => { m.parts[3].term.def = 'Particles always move left'; }, /not the film's own words/, 'REFUSED: a definition the film does not say');
  bad((m) => { m.parts[3].from = 's09_nope'; }, /no scene with that id/, 'REFUSED: a scene the film does not have');
  bad((m) => { m.parts.reverse(); }, /film order|first part must start/, 'REFUSED: parts out of order');
  bad((m) => { m.parts[3].note = 'x'; }, /unknown field/, 'REFUSED: a field the format does not have');
  bad((m) => { delete m.checked; }, /"checked" must say/, 'REFUSED: a map nobody signed');
}

/* ---- the real library */
{
  const a = coverage(ROOT);
  const b = coverage(ROOT);
  eq(JSON.stringify(a), JSON.stringify(b), 'the coverage report is the same on every run');
  const s = a.byStatus;
  ok(a.films > 900, 'the catalog walk finds the films', String(a.films));
  ok((s.timed ?? 0) + (s.mapped ?? 0) >= Math.floor(a.films * 0.9), 'at least nine films in ten are fully timed', JSON.stringify(s));
  ok(!s.none, 'every film has captions', JSON.stringify(s));
  ok(a.scenes.matched / a.scenes.spoken > 0.99, 'more than 99 in 100 spoken scenes are found', JSON.stringify(a.scenes));
  eq(a.rows.filter((r) => r.mapProblems.length).map((r) => r.key), [], 'no map on disk has a problem');
  for (const key of ['diffusion-and-osmosis/explainer', 'diffusion-and-osmosis/chapter-2', 'action-potential/explainer']) {
    eq(a.rows.find((r) => r.key === key)?.status, 'mapped', `${key} is mapped`);
  }
  console.log(`  coverage: ${JSON.stringify(s)} of ${a.films} films; ${a.withQuestion} ask a question; scenes ${a.scenes.matched}/${a.scenes.spoken}`);
}

if (failed) { console.error(`✗ test-film-timelines: ${failed} failed, ${passed} passed`); process.exit(1); }
console.log(`✓ test-film-timelines: ${passed} checks passed.`);
