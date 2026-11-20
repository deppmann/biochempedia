#!/usr/bin/env node
/**
 * The minutes recipe and the stop rules of "How long have you got?" on the lesson page.
 * No build and no network: it loads src/lib/lesson-time.ts, lesson-copy.ts and lesson-stop.mjs
 * directly (Node 22.18+ reads the .ts files as they are).
 *
 * Run: node scripts/test-lesson-time.mjs   (also run by CI)
 */
import assert from 'node:assert/strict';
import { lessonTime, wholeSeconds, readingSeconds, minutesOf, split, clock } from '../src/lib/lesson-time.ts';
import { linesFor, endingsFor } from '../src/lib/lesson-copy.ts';
import { chooseStop } from '../src/lib/lesson-stop.mjs';

let n = 0;
const check = (name, fn) => { fn(); n++; console.log(`ok  ${name}`); };
const words = (k) => Array.from({ length: k }, () => 'word').join(' ');
const film = (title, durationSec, takeaways) => ({ title, durationSec, takeaways });
const base = { tier: 'college', estMinutes: undefined, simulations: 0, films: [], questions: 0, h2: [], skimWords: 300 };
const ids = (t) => t.stops.map((s) => s.id);
const minOf = (t, id) => t.stops.find((s) => s.id === id).min;

// ---------------------------------------------------------------- the recipe
check('reading: words / 150, a minute per Predict, three per simulation, "Going deeper" apart', () => {
  const body = `${words(1500)}\n\n**Predict.** ${words(0)}\n\n## Going deeper\n\n${words(300)}\n\n## After\n\n${words(150)}`;
  const r = readingSeconds(body, 2);
  // 1500 + "Predict" (1 word) + 150 after + heading words are not counted as headings here: allow the few extra words.
  assert.ok(Math.abs(r.core - ((1651 / 150) * 60 + 60 + 360)) < 5, String(r.core));
  assert.ok(Math.abs(r.optional - 120) < 2);
  assert.equal(readingSeconds(body, 2, false).core < r.core - 400, true, 'a hand-set lesson adds no extras');
});

check('one rounding: seconds are summed, then rounded once', () => {
  // 3 films of 100 s are 5 minutes, not 2 + 2 + 2 = 6.
  const t = lessonTime({ ...base, body: words(150), explainer: film('a', 100), films: [film('b', 100), film('c', 100)] });
  assert.equal(minOf(t, 'films'), 5);
  assert.equal(t.whole, 6);   // 60 s of reading + 300 s of film
  assert.equal(minutesOf(10), 1, 'never 0 minutes');
  assert.equal(clock(175.6), '2:56');
});

check('the parts printed under a stop add up to its number', () => {
  assert.deepEqual(split(11, [7.4 * 60, 3.8 * 60]), [7, 4]);
  assert.deepEqual(split(10, [0, 600]), [0, 10]);
  for (const [a, b, c] of [[1130, 470, 229], [2702, 1139, 0], [845, 196, 226], [61, 42, 0]]) {
    const total = minutesOf(a + b + c);
    assert.equal(split(total, [a, b, c]).reduce((x, y) => x + y, 0), total);
  }
  // Turning Signals Off in the prototype said "Films 11 min" over 8 + 4.
  const t = lessonTime({ ...base, body: words(2800), explainer: film('a', 230), films: [film('b', 238)], stories: { audioSec: 229, hops: [] } });
  assert.equal(t.filmMin + t.storyMore, t.stops.find((s) => s.id === 'films')?.min ?? t.filmMin + t.storyMore);
  assert.equal(t.readMin + t.filmInLesson + t.storyInLesson, t.whole);
});

check('the whole-lesson figure is the same from the card recipe and the page recipe', () => {
  const i = { ...base, body: words(3000), simulations: 1, explainer: film('a', 200), films: [film('b', 220)] };
  assert.equal(minutesOf(wholeSeconds(i).whole), lessonTime(i).whole);
  assert.equal(lessonTime(i).whole, Math.round((3000 / 150) * 60 / 60 + 3 + 420 / 60));
});

check('a school lesson keeps its class period, unless text and films add up to more', () => {
  const school = { ...base, tier: 'highschool', estMinutes: 40, explainer: film('a', 180), films: [film('b', 180)] };
  const t = lessonTime({ ...school, body: words(1500) });
  assert.equal(t.whole, 40); assert.equal(t.period, 40); assert.equal(t.sumMin, 16);
  const long = lessonTime({ ...school, body: words(9000) });
  assert.equal(long.whole, 66); assert.equal(long.period, 0);
  assert.equal(lessonTime({ ...school, body: words(1500) }).sittings, 1, 'a class period is one sitting');
});

check('a long lesson gets places to stop; a short one does not', () => {
  const sec = (k) => `## Part ${k}\n\n${words(1500)}\n`;
  const h2 = [1, 2, 3, 4, 5].map((k) => ({ slug: `part-${k}`, text: `Part ${k}` }));
  const t = lessonTime({ ...base, body: [1, 2, 3, 4, 5].map(sec).join('\n'), h2 });
  assert.equal(t.parts.length, 5);
  assert.deepEqual(t.parts.map((p) => p.landing), [false, true, false, true, false]);
  assert.deepEqual(t.parts.map((p) => p.upTo), [10, 20, 30, 40, 50]);
  assert.equal(lessonTime({ ...base, body: sec(1), h2: h2.slice(0, 1) }).sittings, 1);
});

// ---------------------------------------------------------------- which stops a lesson gets
check('stops: every lesson has a skim and the lesson; films and stories only where they exist', () => {
  assert.deepEqual(ids(lessonTime({ ...base, body: words(900) })), ['skim', 'lesson']);
  assert.deepEqual(ids(lessonTime({ ...base, body: words(900), explainer: film('a', 200) })), ['skim', 'films', 'lesson']);
  const full = lessonTime({ ...base, body: words(900), explainer: film('a', 200), films: [film('b', 200)], stories: { audioSec: 230, hops: [{ afterHeading: 'x', title: 'y' }] } });
  assert.deepEqual(ids(full), ['skim', 'stories', 'films', 'lesson']);
  assert.deepEqual(full.stops.map((s) => s.name), ['Skim', 'Stories', 'Films', 'Lesson']);
  assert.equal(lessonTime({ ...base, body: words(900), explainer: film('a', 200) }).stops[1].name, 'Film');
});

check('an ages 5 to 10 guide has Film and Activity, and one stop when it has no film', () => {
  const guide = { ...base, tier: 'families', estMinutes: 20, body: words(600) };
  const t = lessonTime({ ...guide, explainer: film('Set up', 41.7) });
  assert.deepEqual(t.stops, [{ id: 'films', min: 1, name: 'Film' }, { id: 'lesson', min: 20, name: 'Activity' }]);
  assert.deepEqual(ids(lessonTime(guide)), ['lesson'], 'nothing to choose between: the page shows no control');
});

// ---------------------------------------------------------------- the sentences
check('sentences: numbers add up, and no sentence counts what is left', () => {
  const t = lessonTime({ ...base, body: words(2800), explainer: film('a', 230, ['x']), films: [film('b', 238, ['y'])], stories: { audioSec: 229, hops: [{ afterHeading: 'x', title: 'y' }, { afterHeading: 'z', title: 'w' }, { afterHeading: 'q', title: 'r' }] } });
  const l = linesFor(t, { figures: 3 });
  assert.equal(l.films, `Both films, ${t.filmMin} minutes, then three short stories told aloud, ${t.storyMore} more.`);
  assert.match(l.skim, /^The main idea, the figures and what the films show\. Tap a heading to read that part\.$/);
  assert.match(l.lesson, /^All of it: about \d+ minutes of reading, \d+ of film and \d+ of stories\.$/);
  const school = lessonTime({ ...base, tier: 'highschool', estMinutes: 40, body: words(1500), explainer: film('a', 180), films: [film('b', 180)] });
  assert.equal(linesFor(school, { figures: 1 }).lesson, 'All of it: about 40 minutes in class, both films included.');
  const guide = lessonTime({ ...base, tier: 'families', estMinutes: 20, body: words(600), explainer: film('Set up', 41.7) });
  assert.equal(linesFor(guide, { figures: 0 }).films, 'The film, 42 seconds, for the grown-up to look at before the activity.');
  assert.equal(linesFor(guide, { figures: 0 }).lesson, 'All of it, done with a child: about 20 minutes, the film included.');
  assert.deepEqual(endingsFor(t), { skim: 'That is the skim.', stories: 'Those are the stories.', films: 'That is both films.' });
  for (const s of [...Object.values(l), ...Object.values(endingsFor(t))]) assert.doesNotMatch(s, /\bleft\b|to go\b|remaining|\bof \d+\b/i);
});

// ---------------------------------------------------------------- which stop opens
const ALL = ['skim', 'stories', 'films', 'lesson'];
const go = (o) => chooseStop({ stops: ALL, hash: '', search: '', saved: null, legacy: null, inClass: false, guide: false, ...o });

check('nothing saved: the whole lesson', () => {
  assert.deepEqual(go({}), { stop: 'lesson', why: '' });
  assert.deepEqual(go({ saved: 'lesson' }), { stop: 'lesson', why: '' });
  assert.deepEqual(go({ saved: 'nonsense' }), { stop: 'lesson', why: '' });
  assert.deepEqual(chooseStop({}), { stop: 'lesson', why: '' });
});

check('a saved choice opens the next lesson the same way', () => {
  assert.deepEqual(go({ saved: 'films' }), { stop: 'films', why: 'remembered' });
  assert.deepEqual(go({ saved: 'skim' }), { stop: 'skim', why: 'remembered' });
});

check('a saved stop this lesson lacks: the skim, with the reason', () => {
  assert.deepEqual(go({ stops: ['skim', 'films', 'lesson'], saved: 'stories' }), { stop: 'skim', why: 'noStories' });
  assert.deepEqual(go({ stops: ['skim', 'lesson'], saved: 'films' }), { stop: 'skim', why: 'noFilm' });
  assert.deepEqual(go({ stops: ['lesson'], saved: 'films' }), { stop: 'lesson', why: '' });
});

check('a link to a place in the text always opens the whole lesson, and says so only when it changed something', () => {
  assert.deepEqual(go({ saved: 'skim', hash: '#going-deeper' }), { stop: 'lesson', why: 'deepLink' });
  assert.deepEqual(go({ search: '?time=skim', hash: '#hl-abc' }), { stop: 'lesson', why: 'deepLink' });
  assert.deepEqual(go({ saved: 'stories', search: '?pagefind-highlight=osmosis' }), { stop: 'lesson', why: 'deepLink' });
  assert.deepEqual(go({ hash: '#sx-q-3' }), { stop: 'lesson', why: '' });
  assert.deepEqual(go({ saved: 'films', hash: '#top' }), { stop: 'films', why: 'remembered' });
  assert.deepEqual(go({ saved: 'films', hash: '#explainer' }), { stop: 'films', why: 'remembered' });
});

check('?time= opens that stop for the visit and beats the saved choice', () => {
  assert.deepEqual(go({ saved: 'skim', search: '?time=films' }), { stop: 'films', why: '' });
  assert.deepEqual(go({ search: '?supports=2&time=stories' }), { stop: 'stories', why: '' });
  assert.deepEqual(go({ stops: ['skim', 'lesson'], saved: 'skim', search: '?time=films' }), { stop: 'skim', why: 'remembered' }, 'a stop this lesson lacks is ignored');
});

check('a device in a class opens the whole lesson, unless the link carries ?time=', () => {
  assert.deepEqual(go({ saved: 'skim', inClass: true }), { stop: 'lesson', why: 'inClass' });
  assert.deepEqual(go({ inClass: true }), { stop: 'lesson', why: '' });
  assert.deepEqual(go({ saved: 'skim', inClass: true, search: '?time=films' }), { stop: 'films', why: '' });
});

check('an activity guide ignores a choice saved on a science lesson', () => {
  const guide = { stops: ['films', 'lesson'], guide: true };
  assert.deepEqual(go({ ...guide, saved: 'films' }), { stop: 'lesson', why: '' });
  assert.deepEqual(go({ ...guide, saved: 'skim' }), { stop: 'lesson', why: '' });
  assert.deepEqual(go({ ...guide, search: '?time=films' }), { stop: 'films', why: '' });
});

check('the old per-lesson choice is a fallback only', () => {
  assert.deepEqual(go({ legacy: 'hops' }), { stop: 'stories', why: 'remembered' });
  assert.deepEqual(go({ legacy: 'films' }), { stop: 'films', why: 'remembered' });
  assert.deepEqual(go({ legacy: 'hops', saved: 'lesson' }), { stop: 'lesson', why: '' });
  assert.deepEqual(go({ legacy: 'hops', saved: 'skim' }), { stop: 'skim', why: 'remembered' });
});

console.log(`\n${n} checks passed.`);
