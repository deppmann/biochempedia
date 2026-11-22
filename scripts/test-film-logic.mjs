#!/usr/bin/env node
/* Tests for the film pages' decisions (src/lib/film-logic.mjs): what the theater's companion shows
   through a question, a pause and "Carry on"; what the pause button says; and where a run opens.
   Each case here was a fault a reviewer found in a browser.

   Run: node scripts/test-film-logic.mjs   (in `npm test` and in CI) */
import { companionAt, swapRule, pauseLabel, runFilms, runPlace, endWith, matchFilms, runnableFilms, runQueue } from '../src/lib/film-logic.mjs';

let failed = 0;
let passed = 0;
const eq = (a, b, name) => { if (JSON.stringify(a) === JSON.stringify(b)) passed++; else { failed++; console.error(`✗ ${name}: got ${JSON.stringify(a)}, wanted ${JSON.stringify(b)}`); } };

/* ---- the companion through a question (the second Diffusion and Osmosis film's times) */
const parts = [{ start: 0 }, { start: 26.5 }, { start: 74.6 }, { start: 90 }, { start: 101.2 }, { start: 115.3 }];
const questions = [{ start: 74.6, until: 90 }];
eq(companionAt(0, parts, questions), { part: 0, asking: -1 }, 'before play: the first part, no question');
eq(companionAt(74.5, parts, questions), { part: 1, asking: -1 }, 'just before the film asks: still the part before');
eq(companionAt(74.6, parts, questions), { part: 2, asking: 0 }, 'the film asks: the question part');
eq(companionAt(89.9, parts, questions), { part: 2, asking: 0 }, 'while the film waits: the question stays');
eq(companionAt(90, parts, questions), { part: 3, asking: -1 }, 'the answer starts: the question lets go');
eq(companionAt(120, parts, questions), { part: 5, asking: -1 }, 'later parts follow');
eq(companionAt(80, parts, questions, true), { part: 2, asking: -1 }, 'a film that has ended asks nothing');
eq(companionAt(31, [], [{ start: 29.7, until: 35.2 }]), { part: -1, asking: 0 }, 'a film with no map: the question alone');
eq(companionAt(35.2, [], [{ start: 29.7, until: 35.2 }]), { part: -1, asking: -1 }, 'a film with no map: released at the answer');

/* ---- the panel and keyboard focus. The fault: after "Pause the film" and "Carry on", focus stayed on
   the button, the panel was held as if someone were reading a link, and the companion stayed on the
   question for the rest of the film. */
eq(swapRule('none'), { change: true, moveFocus: false }, 'no focus in the panel: it changes');
eq(swapRule('link'), { change: false, moveFocus: false }, 'focus on a link in the panel: it is held');
eq(swapRule('pause'), { change: true, moveFocus: true }, 'focus on the pause button: the panel changes, and focus is moved first');
{
  // Played through: pause at the question, carry on, and the answer arrives with focus still on the button.
  let shown = companionAt(80, parts, questions).part;
  const next = companionAt(90.2, parts, questions).part;
  const rule = swapRule('pause');
  if (rule.change) shown = next;
  eq(shown, 3, 'after Carry on, the companion moves to the answer part');
}

/* ---- the pause button says what pressing it will do */
eq(pauseLabel({ paused: false, started: true }), 'Pause the film', 'playing: Pause the film');
eq(pauseLabel({ paused: true, started: true }), 'Carry on', 'paused after playing: Carry on');
eq(pauseLabel({ paused: true, started: false }), 'Play the film', 'opened inside a question, never played: Play the film');

/* ---- a run and its place */
const q = [{ f: 'a', d: 183 }, { f: 'b', d: 169 }, { f: 'c', d: 198 }, { f: 'd', d: 240 }, { f: 'e', d: 60 }];
eq(runFilms(q, 0, 10).films.map((f) => f.f), ['a', 'b', 'c'], 'ten minutes: whole films, at most a minute over');
eq(runFilms(q, 0, 10).seconds, 550, 'and its length');
eq(runFilms(q, 1, 10).films.map((f) => f.f), ['b', 'c', 'd'], 'the run starts where it is told to');
eq(runFilms(q, 3, 3).films.map((f) => f.f), ['d'], 'always at least one film');
eq(runFilms(q, 0, 0).films.length, 5, 'no budget: every film');
eq(runFilms(q, 0, 7).films.map((f) => f.f), ['a', 'b'], 'stops at the first film that does not fit, and does not skip ahead to a shorter one');
const run = runFilms(q, 0, 10).films;
eq(runPlace(run, new Set()), { index: 0, at: 0 }, 'a new run opens at its first film');
eq(runPlace(run, new Set(['a', 'b'])), { index: 2, at: 0 }, 'reopened after two films: it opens at the third');
eq(runPlace(run, new Set(['a']), [{ f: 'b', t: 84, d: 169 }]), { index: 1, at: 84 }, 'reloaded in the middle of the second film: that film, at that second');
eq(runPlace(run, new Set(['a']), [{ f: 'b', t: 3, d: 169 }]), { index: 1, at: 0 }, 'a place under five seconds is the start');
eq(runPlace(run, new Set(['a']), [{ f: 'b', t: 168, d: 169 }]), { index: 1, at: 0 }, 'a place in the last two seconds is the start');
eq(runPlace(run, new Set(['a']), [{ f: 'c', t: 50, d: 198 }]), { index: 1, at: 0 }, 'a place saved for a later film does not move the run');
eq(runPlace(run, new Set(['a', 'b', 'c'])), { index: 0, at: 0 }, 'every film watched: back to the first');
eq(runPlace(run, new Set(['b'])), { index: 0, at: 0 }, 'the first unwatched film, not the one after the last watched');

eq(endWith('Which Way Does the Water Go?'), 'Which Way Does the Water Go?', 'no full stop after a title that ends in a question mark');
eq(endWith('The Size Test'), 'The Size Test.', 'a full stop after a plain title');

/* ---- one matcher for the library and the run. The fault: the library searched the questions people
   ask and the run did not, so "sodium pump" showed films, promised a run of three, and the run page
   said "No film matches this view". */
{
  const F = (i, t, l, s, c, k, d, h) => ({ i, t, l, s, c, k, d, h: h ?? `/watch/x${i}/`, f: `x${i}/explainer` });
  const list = [
    F(0, 'Set Up: Thirsty Celery', 'Thirsty Celery', 'ages-5-10', 'together', 'activity', 42),
    F(1, 'Random Moves, One-Way Drift', 'Diffusion and Osmosis', 'grade-7', 'life', 'first', 175),
    F(2, 'Water Drifts to the Saltier Side', 'Diffusion and Osmosis', 'grade-7', 'life', 'second', 196),
    F(3, 'Downhill for Free', 'Crossing the Membrane', 'high-school', 'bio', 'first', 202),
    F(4, 'Two Pushes, One Hill', 'Active Transport', 'college-core', 'cell', 'first', 190),
    F(5, 'Jens Skou', 'Active Transport', 'college-core', 'cell', 'profile', 120, '/lessons/active-transport/#lb-sci-0'),
    F(6, 'Adaptation at the Edge', 'Sensory Adaptation', 'graduate', 'neuro', 'first', 60),
  ];
  const ideas = { 'Crossing the Membrane': 'osmosis red blood cell burst water', 'Active Transport': 'sodium pump atp uphill', 'Thirsty Celery': 'osmosis celery water' };
  const view = (o = {}) => ({ q: '', sort: 'course', level: '', course: '', kind: '', ...o });
  const titles = (a) => a.map((f) => f.i);
  eq(titles(matchFilms(list, view({ q: 'sodium pump' }), ideas)), [4, 5], 'a search through the questions people ask finds the lesson\'s films');
  eq(titles(matchFilms(list, view({ q: 'sodium pump' }), null)), [], 'without that data the same search finds nothing (so both pages must load it)');
  eq(titles(runQueue(list, view({ q: 'sodium pump' }), ideas)), [4], 'the run plays the films of that view that have their own page');
  eq(titles(matchFilms(list, view({ q: 'osmosis' }), ideas)), [1, 2, 0, 3], 'title matches come first, then matches by question, each in course order');
  eq(titles(runQueue(list, view({ q: 'osmosis' }), ideas)), [1, 2, 3], 'the run is that list, in that order, without the grown-up\'s set-up film');
  // Since 2026-11-22 (src/lib/film-search.mjs) a chosen order applies to every film with all the words.
  eq(titles(runQueue(list, view({ q: 'osmosis', sort: 'long' }), ideas)), [3, 2, 1], 'the run follows the order the library shows (longest first)');
  eq(titles(runQueue(list, view({ level: 'ages-5-10' }), ideas)), [0], 'set-up films play when their level is asked for');
  eq(titles(matchFilms(list, view({ q: 'atp' }), ideas)), [4, 5], 'a word must start a word among the questions: "atp" is not found in "Adaptation"');
  eq(titles(matchFilms(list, view({ q: 'why does water' }), ideas)), [2, 0, 3], 'little words are dropped from a search');
  // The property that matters: for every view, the run is exactly the playable part of what the library shows.
  for (const v of [view(), view({ q: 'osmosis' }), view({ q: 'pump', course: 'cell' }), view({ level: 'grade-7', sort: 'short' }), view({ kind: 'profile' }), view({ q: 'zzz' })]) {
    const m = matchFilms(list, v, ideas);
    eq(titles(runQueue(list, v, ideas)), titles(runnableFilms(m.full ? m.slice(0, m.full) : m, v)), `the run is the view (its films with every word): ${JSON.stringify(v)}`);
  }
  eq(titles(runQueue(list, view({ kind: 'profile' }), ideas)), [], 'a view of profiles only has nothing to play in a row');
}

if (failed) { console.error(`✗ test-film-logic: ${failed} failed, ${passed} passed`); process.exit(1); }
console.log(`✓ test-film-logic: ${passed} checks passed.`);
