#!/usr/bin/env node
/* Calendar (/calendar/): the arithmetic, offline. No browser, no network.

   What is pinned here:
   - a parent's or a learner's plan stores no date, so nothing can be late: every date is worked
     out from today, nothing is ever placed before today, and a skipped day leaves no gap or mark;
   - days are whole calendar days, so time zones and daylight-saving changes cannot move one;
   - "Later" and "Not this week" last for the visit only, keep the order, and undo exactly;
   - the MCAT path puts each passage set after the lessons it draws on;
   - a test date that cannot be reached is said as arithmetic, with hours a week;
   - a class plan skips days off and never puts two classes on one day;
   - the calendar file is valid iCalendar (RFC 5545): one repeating entry that ends, no alarm.

   Run: node scripts/test-calendar.mjs   (Node 22.18+ reads the .ts file directly) */
import assert from 'node:assert/strict';
import { readFileSync, existsSync, readdirSync } from 'node:fs';
import { fileURLToPath } from 'node:url';
import * as E from '../src/lib/calendar/engine.ts';

let n = 0;
const check = (name, fn) => { fn(); n++; console.log(`  ok  ${name}`); };
const path = (p) => fileURLToPath(new URL(p, import.meta.url));

/* ---------- fixtures ---------- */
const act = (s, materials = [`thing for ${s}`], extra = {}) => ({ s, t: `Act ${s}`, hook: 'h', unit: 'U', u: 0, min: 25, setting: 'either', adult: 'Stay close.', materials, safety: ['Stay close.'], ...extra });
const ACTS = ['a', 'b', 'c', 'd', 'e', 'f', 'g'].map((s) => act(s));
const lesson = (s, n, m = 30, fs = 420) => ({ s, t: `Lesson ${s}`, u: 0, n, m, fs, fc: fs ? 2 : 0 });
const COURSE = { s: 'physiology', t: 'Physiology', level: 'College', school: false, units: ['One'], lessons: [1, 2, 3, 4, 5, 6, 7, 8].map((i) => lesson(`p${i}`, i)) };
const MCAT = {
  steps: [
    { s: 'biochemistry', t: 'Biochemistry', why: '', optional: false, lessons: [1, 2, 3, 4].map((i) => lesson(`b${i}`, i)) },
    { s: 'cell-biology', t: 'Cell Biology', why: '', optional: false, lessons: [1, 2, 3].map((i) => lesson(`c${i}`, i)) },
    { s: 'sensory-systems', t: 'Sensory Systems', why: '', optional: true, lessons: [1, 2].map((i) => lesson(`s${i}`, i)) },
  ],
  sets: [
    { id: 'one', title: 'One', lessons: ['b2'] },
    { id: 'two', title: 'Two', lessons: ['b1', 'c2', 'b3'] },
    { id: 'three', title: 'Three', lessons: ['s1'] },
    { id: 'four', title: 'Four', lessons: ['b4', 'c1'] },
  ],
  scope: '', links: [], diagnostic: 20,
};
const none = new Set();

console.log('Calendar: days');
check('a day is a real calendar day or it is refused', () => {
  assert.ok(E.isIso('2026-11-20'));
  for (const bad of ['2026-02-30', '2026-13-01', '2026-1-1', 'tomorrow', '', null, 20261120]) assert.equal(E.isIso(bad), false, String(bad));
});
check('adding days crosses daylight-saving changes, month ends and leap days without skipping or repeating', () => {
  assert.equal(E.addDays('2026-03-07', 1), '2026-03-08');   // US clocks go forward
  assert.equal(E.addDays('2026-03-08', 1), '2026-03-09');
  assert.equal(E.addDays('2026-10-31', 1), '2026-11-01');   // US clocks go back
  assert.equal(E.addDays('2026-11-01', 1), '2026-11-02');
  assert.equal(E.addDays('2026-03-28', 2), '2026-03-30');   // Europe
  assert.equal(E.addDays('2028-02-28', 1), '2028-02-29');
  assert.equal(E.addDays('2026-12-31', 1), '2027-01-01');
  let d = '2026-01-01';
  for (let i = 0; i < 800; i++) { const next = E.addDays(d, 1); assert.equal(E.daysBetween(d, next), 1); assert.equal(E.dow(next), (E.dow(d) + 1) % 7); d = next; }
  assert.equal(E.daysBetween('2026-01-01', d), 800);
});
check('"today" is the day where the person is: one instant, three places, two dates', () => {
  const t = new Date('2026-11-21T04:30:00Z');
  assert.equal(E.todayIso(t, 'America/New_York'), '2026-11-20');
  assert.equal(E.todayIso(t, 'America/Los_Angeles'), '2026-11-20');
  assert.equal(E.todayIso(t, 'Europe/London'), '2026-11-21');
  assert.equal(E.todayIso(t, 'Asia/Tokyo'), '2026-11-21');
  assert.equal(E.todayIso(t, 'Pacific/Kiritimati'), '2026-11-21');
  // the hour that happens twice, and the hour that does not happen
  assert.equal(E.todayIso(new Date('2026-11-01T05:30:00Z'), 'America/New_York'), '2026-11-01');
  assert.equal(E.todayIso(new Date('2026-11-01T06:30:00Z'), 'America/New_York'), '2026-11-01');
  assert.equal(E.todayIso(new Date('2026-03-08T06:59:00Z'), 'America/New_York'), '2026-03-08');
  assert.equal(E.todayIso(new Date('2026-03-08T07:01:00Z'), 'America/New_York'), '2026-03-08');
  assert.match(E.todayIso(), /^\d{4}-\d{2}-\d{2}$/);
});
check('weeks start on Monday, and a Sunday belongs to the week before it', () => {
  assert.equal(E.mondayOf('2026-11-20'), '2026-11-16');
  assert.equal(E.mondayOf('2026-11-22'), '2026-11-16');   // Sunday
  assert.equal(E.mondayOf('2026-11-23'), '2026-11-23');
  assert.equal(E.mondayOf('2027-01-01'), '2026-12-28');   // across a year
});
check('the days of a rhythm start at today, never before it', () => {
  assert.deepEqual(E.rhythmDays([6], '2026-11-20', 2), ['2026-11-21', '2026-11-28']);
  assert.deepEqual(E.rhythmDays([6], '2026-11-21', 1), ['2026-11-21']);      // today counts
  assert.deepEqual(E.rhythmDays([6], '2026-11-22', 1), ['2026-11-28']);      // the day after waits a week
  assert.deepEqual(E.rhythmDays([1, 3, 5], '2026-11-20', 4), ['2026-11-20', '2026-11-23', '2026-11-25', '2026-11-27']);
  assert.deepEqual(E.rhythmDays([], '2026-11-20', 3), []);
  assert.equal(E.daysPhrase([6]), 'Saturdays');
  assert.equal(E.daysPhrase([5, 1, 3]), 'Mondays, Wednesdays and Fridays');
  assert.equal(E.onDays([1, 2, 3, 4, 5]), 'Monday to Friday');
  assert.equal(E.onDays([0, 6]), 'on Saturdays and Sundays');
});

console.log('Calendar: with a child');
check('the first visit is Saturdays, the next activity, and no dates on what follows', () => {
  const v = E.parentView(ACTS, E.newParent(), '2026-11-20');
  assert.equal(v.date, '2026-11-21');
  assert.equal(v.next.s, 'a');
  assert.deepEqual(v.after.map((x) => x.act.s), ['b', 'c', 'd', 'e']);
  assert.ok(v.after.every((x) => x.date === undefined), 'no future dates until the family picks days');
  const picked = E.parentView(ACTS, { ...E.newParent(), days: [3, 6] }, '2026-11-20');
  assert.deepEqual(picked.after.map((x) => x.date), ['2026-11-25', '2026-11-28', '2026-12-02', '2026-12-05']);
});
check('for every day of two years and every rhythm, nothing is placed before today', () => {
  const sets = [[6], [0], [3, 6], [1, 2, 3, 4, 5], [0, 1, 2, 3, 4, 5, 6]];
  let today = '2026-01-01';
  for (let i = 0; i < 730; i++, today = E.addDays(today, 1)) {
    for (const days of sets) {
      const v = E.parentView(ACTS, { ...E.newParent(), days }, today);
      assert.ok(v.date >= today && E.daysBetween(today, v.date) <= 6, `${today} ${days}`);
      assert.ok(days.includes(E.dow(v.date)));
      let prev = v.date;
      for (const a of v.after) { assert.ok(a.date > prev); prev = a.date; }
    }
  }
});
check('a skipped day leaves no gap and no mark: the same plan, opened later, simply starts from that day', () => {
  const plan = { ...E.newParent(), days: [6] };
  const before = JSON.stringify(plan);
  const a = E.parentView(ACTS, plan, '2026-11-20');
  const b = E.parentView(ACTS, plan, '2026-12-14');          // three Saturdays went by
  assert.equal(a.next.s, b.next.s, 'the same activity is still next');
  assert.equal(b.date, '2026-12-19');
  assert.equal(JSON.stringify(plan), before, 'looking changes nothing');
  assert.equal(E.holdsDate(plan), false);
});
check('with no day set, nothing is dated at all', () => {
  const v = E.parentView(ACTS, { ...E.newParent(), days: [] }, '2026-11-20');
  assert.equal(v.date, undefined);
  assert.equal(v.next.s, 'a');
  assert.ok(v.after.every((x) => x.date === undefined));
});
check('"Not this week" moves the activity to the next day of the rhythm, for this visit only', () => {
  const plan = E.newParent();
  const v = E.parentView(ACTS, plan, '2026-11-20', { skip: true });
  assert.equal(v.freed, '2026-11-21');
  assert.equal(v.date, '2026-11-28');
  assert.equal(v.next.s, 'a', 'the same activity, not the next one');
  assert.deepEqual(plan, E.newParent(), 'nothing was written to the plan');
});
check('"We did it" moves the next one up; "Put it back" returns it; a pick comes first and the one it replaces follows', () => {
  let p = E.parentDid(E.newParent(), ACTS[0]);
  assert.deepEqual(p.done, ['a']);
  assert.equal(E.parentQueue(ACTS, p)[0].s, 'b');
  p = E.parentUndid(p, 'a');
  assert.equal(E.parentQueue(ACTS, p)[0].s, 'a');
  p = E.parentPick(ACTS, p, 'e');
  assert.deepEqual(E.parentQueue(ACTS, p).map((a) => a.s), ['e', 'a', 'b', 'c', 'd', 'f', 'g']);
  p = E.parentPick(ACTS, p, 'g');
  assert.deepEqual(E.parentQueue(ACTS, p).map((a) => a.s).slice(0, 3), ['g', 'e', 'a']);
  p = E.parentDid(p, ACTS[6]);
  assert.deepEqual(E.parentQueue(ACTS, p).map((a) => a.s).slice(0, 2), ['e', 'a']);
  // doing every one ends the queue without an error
  for (const a of ACTS) p = E.parentDid(p, a);
  const end = E.parentView(ACTS, p, '2026-11-20');
  assert.equal(end.next, undefined);
  assert.equal(end.done.length, ACTS.length);
});
check('the gather list keeps every line word for word, in each guide\'s order; identical lines appear once', () => {
  const x = act('x', ['Paper and a pencil', 'A jar', '12 to 20 large dry beans from the grocery store']);
  const y = act('y', ['A spoon', 'Paper and a pencil', 'A magnifier (optional)']);
  const lines = E.gather([x, y]);
  assert.deepEqual(lines.map((l) => l.text), ['Paper and a pencil', 'A jar', '12 to 20 large dry beans from the grocery store', 'A spoon', 'A magnifier (optional)']);
  assert.deepEqual(lines[0].for.map((a) => a.s), ['x', 'y']);
  // a tick is forgotten when its activity is done, since the things were used
  let p = { ...E.newParent(), have: { [E.lineKey('A jar')]: 1, [E.lineKey('A spoon')]: 1 } };
  p = E.parentDid(p, x);
  assert.deepEqual(Object.keys(p.have), [E.lineKey('A spoon')]);
});

console.log('Calendar: for myself');
check('with no days ticked a learner sees Next, Then, After that, and no date anywhere', () => {
  const v = E.studentView(E.courseItems(COURSE), none, { days: [] }, '2026-11-20');
  assert.equal(v.dated, false);
  assert.equal(v.top.date, undefined);
  assert.deepEqual([v.top, ...v.rows].map((r) => r.sitting.items[0].key), ['p1', 'p2', 'p3']);
  assert.ok(v.rows.every((r) => r.date === undefined));
});
check('with days ticked, lessons sit on those days from today on, one a day, in order', () => {
  const v = E.studentView(E.courseItems(COURSE), none, { days: [1, 3, 5] }, '2026-11-20'); // a Friday
  assert.deepEqual([v.top, ...v.rows].map((r) => [r.sitting.items[0].key, r.date]), [['p1', '2026-11-20'], ['p2', '2026-11-23'], ['p3', '2026-11-25']]);
  const sat = E.studentView(E.courseItems(COURSE), none, { days: [1, 3, 5] }, '2026-11-21');
  assert.equal(sat.top.date, '2026-11-23', 'a day that is not a study day shows the next one, nothing before today');
  assert.equal(sat.top.sitting.items[0].key, 'p1');
});
check('done lessons leave the queue; "Start at" skips what a class has already covered', () => {
  const v = E.studentView(E.courseItems(COURSE), new Set(['p1', 'p3']), { days: [] }, '2026-11-20');
  assert.deepEqual([v.top, ...v.rows].map((r) => r.sitting.items[0].key), ['p2', 'p4', 'p5']);
  assert.deepEqual(E.courseItems(COURSE, 'p6').map((i) => i.key), ['p6', 'p7', 'p8']);
  const end = E.studentView(E.courseItems(COURSE), new Set(COURSE.lessons.map((l) => l.s)), { days: [1] }, '2026-11-20');
  assert.equal(end.top, undefined);
});
check('"Later" empties today, moves the same lesson to the next study day, and keeps the order', () => {
  const items = E.courseItems(COURSE);
  const plan = { days: [1, 3, 5] };
  const before = E.studentView(items, none, plan, '2026-11-20');
  const after = E.studentView(items, none, plan, '2026-11-20', { later: true });
  assert.equal(after.emptied, '2026-11-20');
  assert.equal(after.top.date, '2026-11-23');
  assert.deepEqual([after.top, ...after.rows].map((r) => r.sitting.items[0].key), [before.top, ...before.rows].map((r) => r.sitting.items[0].key));
  // on a day that is not a study day there is nothing to move
  const off = E.studentView(items, none, plan, '2026-11-21', { later: true });
  assert.equal(off.emptied, undefined);
  assert.equal(off.top.date, '2026-11-23');
});
check('"Later" and "Not this week" are never saved, and "Put it back" restores the page exactly', () => {
  const start = { state: { v: 1, student: { ...E.newStudent(), plan: 'physiology', days: [1, 3, 5] }, parent: E.newParent() }, visit: {} };
  const saved = JSON.stringify(start.state);
  const s1 = E.step(start, (m) => { m.visit.later = true; return m; });
  assert.equal(JSON.stringify(s1.model.state), saved, 'the saved plan did not change');
  assert.equal(s1.model.visit.later, true);
  assert.deepEqual(s1.undo, start, 'undo is the model as it was');
  const s2 = E.step(s1.model, (m) => { m.visit.skip = true; return m; });
  assert.equal(JSON.stringify(s2.model.state), saved);
  // a change to the plan undoes to the plan before it, and the original is not touched
  const s3 = E.step(start, (m) => { m.state.parent = E.parentDid(m.state.parent, ACTS[0]); return m; });
  assert.deepEqual(s3.model.state.parent.done, ['a']);
  assert.deepEqual(s3.undo.state.parent.done, []);
  assert.deepEqual(start.state.parent.done, []);
  // the next day, the visit is gone and the lesson is simply today's
  const tomorrow = E.studentView(E.courseItems(COURSE), none, { days: [1, 3, 5] }, '2026-11-23', {});
  assert.equal(tomorrow.top.date, '2026-11-23');
  assert.equal(tomorrow.top.sitting.items[0].key, 'p1');
});
check('something done today uses today: the next lesson waits for the next study day', () => {
  const v = E.studentView(E.courseItems(COURSE), new Set(['p1']), { days: [1, 3, 5] }, '2026-11-20', { spent: true });
  assert.equal(v.spent, true);
  assert.equal(v.top.sitting.items[0].key, 'p2');
  assert.equal(v.top.date, '2026-11-23');
});
check('honest minutes: reading plus film for a college lesson; a school lesson is its class period', () => {
  const [it] = E.courseItems(COURSE);
  assert.equal(E.itemMinutes(it), 37);
  const school = E.courseItems({ ...COURSE, school: true })[0];
  assert.equal(E.itemMinutes(school), 30);
  assert.equal(E.filmMin(20), 1);
  assert.equal(E.filmMin(0), 0);
});

console.log('Calendar: the MCAT path');
check('the diagnostic comes first, courses follow the path, and each passage set follows the last lesson it draws on', () => {
  const keys = E.mcatItems(MCAT, { out: [], opt: [] }).map((i) => i.key);
  assert.deepEqual(keys, ['mcat:diagnostic', 'b1', 'b2', 'mcat:set:one', 'b3', 'b4', 'c1', 'mcat:set:four', 'c2', 'mcat:set:two', 'c3']);
});
check('unticking a course closes the plan up and moves or drops its passage sets; the optional course is out until ticked', () => {
  const noCell = E.mcatItems(MCAT, { out: ['cell-biology'], opt: [] }).map((i) => i.key);
  assert.deepEqual(noCell, ['mcat:diagnostic', 'b1', 'b2', 'mcat:set:one', 'b3', 'mcat:set:two', 'b4', 'mcat:set:four']);
  const noBio = E.mcatItems(MCAT, { out: ['biochemistry'], opt: [] }).map((i) => i.key);
  assert.deepEqual(noBio, ['mcat:diagnostic', 'c1', 'mcat:set:four', 'c2', 'mcat:set:two', 'c3']);
  const withSens = E.mcatItems(MCAT, { out: [], opt: ['sensory-systems'] }).map((i) => i.key);
  assert.deepEqual(withSens.slice(-3), ['s1', 'mcat:set:three', 's2']);
});
check('sittings pack in order, never straddle two courses, and leave the diagnostic alone', () => {
  const items = E.mcatItems(MCAT, { out: [], opt: [] });
  const one = E.sittings(items, 0);
  assert.ok(one.every((s) => s.items.length === 1));
  const hour = E.sittings(items, 90);
  assert.deepEqual(hour[0].items.map((i) => i.key), ['mcat:diagnostic']);
  for (const s of hour) assert.equal(new Set(s.items.map((i) => i.group)).size, 1, 'one course in a sitting');
  assert.deepEqual(hour.flatMap((s) => s.items.map((i) => i.key)), items.map((i) => i.key), 'nothing reordered or lost');
  assert.ok(hour.some((s) => s.items.length > 1));
  for (const s of hour) assert.equal(s.min, s.items.reduce((a, i) => a + E.itemMinutes(i), 0));
});
if (existsSync(path('../dist/calendar/student/mcat/index.html'))) {
  check('on the built site: real lessons, the site\'s own path order, every built passage set after its lessons', () => {
    const html = readFileSync(path('../dist/calendar/student/mcat/index.html'), 'utf8');
    const data = JSON.parse(html.match(/<script type="application\/json" id="cal-data">([\s\S]*?)<\/script>/)[1]).mcat;
    const pathsTs = readFileSync(path('../src/data/paths.ts'), 'utf8');
    const mcatBlock = pathsTs.slice(pathsTs.indexOf("id: 'mcat'"), pathsTs.indexOf("id: 'major'"));
    const order = [...mcatBlock.matchAll(/course: '([a-z-]+)'/g)].map((m) => m[1]);
    assert.deepEqual(data.steps.map((s) => s.s), order, 'the course order is the one in src/data/paths.ts');
    assert.ok(mcatBlock.includes('MCAT_SCOPE_NOTE') && data.scope.length > 40 && html.includes(data.scope.replace(/&/g, '&amp;')), 'the scope note is on the page word for word');
    const setsDir = path('../src/content/mcat-sets/');
    const sets = readdirSync(setsDir).filter((f) => f.endsWith('.json')).map((f) => JSON.parse(readFileSync(setsDir + f, 'utf8')));
    assert.equal(data.sets.length, sets.length);
    const items = E.mcatItems(data, { out: [], opt: data.steps.filter((s) => s.optional).map((s) => s.s) });
    const at = new Map(items.map((i, k) => [i.key, k]));
    assert.equal(items[0].key, 'mcat:diagnostic');
    for (const s of sets) {
      const me = at.get(E.setKey(s.id));
      assert.ok(me !== undefined, `${s.id} is in the plan`);
      for (const l of s.lessons) assert.ok(at.get(l.slug) < me, `${s.id} comes after ${l.slug}`);
    }
    const lessons = items.filter((i) => i.kind === 'lesson');
    assert.ok(lessons.length > 150 && lessons.every((i) => i.t && i.read > 0), 'real titles and minutes');
    // the default plan leaves the optional course out
    assert.ok(!E.mcatItems(data, { out: [], opt: [] }).some((i) => i.group === 'sensory-systems'));
  });
  check('on the built site: every guide\'s safety notes reach the parent page word for word, and no model wrote anything', () => {
    const html = readFileSync(path('../dist/calendar/parent/index.html'), 'utf8');
    const acts = JSON.parse(html.match(/<script type="application\/json" id="cal-data">([\s\S]*?)<\/script>/)[1]).activities;
    assert.ok(acts.length >= 30);
    for (const a of acts) {
      const mdx = readFileSync(path(`../src/content/lessons/${a.s}/lesson.mdx`), 'utf8');
      const note = mdx.match(/<SafetyNote[^>]*>([\s\S]*?)<\/SafetyNote>/)[1];
      const want = note.trim().split(/\n(?=- )/).map((s) => s.replace(/^\s*-\s*/, '').replace(/\s+/g, ' ').trim());
      assert.deepEqual(a.safety, want, `${a.s}: safety notes`);
      assert.ok(a.safety.length >= 3);
      // The guide's frontmatter is YAML: undo its quote escapes and line folds before comparing.
      const plain = (s) => s.replace(/\\"/g, '"').replace(/''/g, "'").replace(/\s+/g, ' ');
      const front = plain(mdx);
      for (const m of a.materials) assert.ok(front.includes(plain(m)), `${a.s}: "${m.slice(0, 40)}" is the guide's own line`);
      assert.ok(front.includes(plain(a.adult)), `${a.s}: the grown-up's line`);
    }
  });
} else {
  console.log('  --  built-site checks skipped (no dist/; run npm run build first)');
}

console.log('Calendar: a test date');
const mcatAll = (sit) => E.sittings(E.mcatItems(MCAT, { out: [], opt: [] }), sit);
const brute = (all, days, today) => E.rhythmDays(days, today, all.length).at(-1);
check('no date, no arithmetic; no days, no rhythm to count; a date that has passed is said plainly', () => {
  assert.equal(E.reach(mcatAll(0), [1, 3], '2026-11-20', undefined).kind, 'none');
  assert.equal(E.reach(mcatAll(0), [], '2026-11-20', '2027-05-14').kind, 'no-days');
  assert.equal(E.reach(mcatAll(0), [1, 3], '2026-11-20', '2026-11-20').kind, 'passed');
  assert.equal(E.reach(mcatAll(0), [1, 3], '2026-11-20', '2026-02-30').kind, 'none');
});
check('the day the lessons end is the last sitting laid on the person\'s days, for every rhythm', () => {
  for (const days of [[1], [6], [1, 3, 5], [0, 2, 4, 6], [0, 1, 2, 3, 4, 5, 6]]) {
    for (const today of ['2026-11-20', '2026-11-21', '2026-11-22', '2027-02-27', '2026-03-06']) {
      const all = mcatAll(0);
      assert.equal(E.reach(all, days, today, '2030-01-01').end, brute(all, days, today), `${days} from ${today}`);
    }
  }
});
check('a date the rhythm reaches leaves whole weeks to spare; one it only just reaches is called close', () => {
  const all = mcatAll(0);                                     // 11 sittings, Mondays and Thursdays
  const end = brute(all, [1, 4], '2026-11-20');
  const fits = E.reach(all, [1, 4], '2026-11-20', E.addDays(end, 30));
  assert.deepEqual([fits.kind, fits.spare, fits.end], ['fits', 4, end]);
  assert.equal(E.reach(all, [1, 4], '2026-11-20', E.addDays(end, 13)).kind, 'close');
  assert.equal(E.reach(all, [1, 4], '2026-11-20', end).kind, 'close');
});
check('a date the rhythm cannot reach gives weeks past it and the hours a week that would, never a countdown', () => {
  const all = mcatAll(0);
  const end = brute(all, [1], '2026-11-20');                  // one a week: eleven weeks
  const r = E.reach(all, [1], '2026-11-20', E.addDays(end, -28));
  assert.equal(r.kind, 'beyond');
  assert.equal(r.over, 4);
  assert.ok(r.hoursNeeded > r.hoursNow && r.hoursNow >= 1);
  const total = all.reduce((a, s) => a + s.min, 0);
  const weeks = E.daysBetween('2026-11-20', E.addDays(end, -28)) / 7;
  assert.ok(r.hoursNeeded * weeks * 60 >= total, 'that many hours a week really does bring it inside');
  assert.equal(E.reach(all, [1], '2026-11-20', '2026-11-23').kind, 'far-beyond', 'three days away is not a pace anyone could keep');
  for (const v of Object.values(r)) assert.ok(typeof v !== 'number' || v >= 0, 'no number here can go below zero');
});

console.log('Calendar: for my class');
const setup = (over = {}) => ({ from: '2026-11-16', meet: [1, 2, 3, 4, 5], per: 1, breaks: [], moved: [], ...over });
check('one lesson a meeting, on class days only, in order, never two classes on a day', () => {
  const ms = E.meetings(COURSE.lessons, setup());
  assert.deepEqual(ms.map((m) => m.date), ['2026-11-16', '2026-11-17', '2026-11-18', '2026-11-19', '2026-11-20', '2026-11-23', '2026-11-24', '2026-11-25']);
  assert.deepEqual(ms.map((m) => m.lessons[0].s), COURSE.lessons.map((l) => l.s));
  const mwf = E.meetings(COURSE.lessons, setup({ meet: [1, 3, 5] }));
  assert.ok(mwf.every((m) => [1, 3, 5].includes(E.dow(m.date))));
  assert.equal(new Set(mwf.map((m) => m.date)).size, mwf.length);
});
check('days with no class are skipped, including a break that runs over a weekend and a year end', () => {
  const ms = E.meetings(COURSE.lessons, setup({ breaks: [{ from: '2026-11-25', to: '2026-11-27', label: 'Thanksgiving' }, { from: '2026-11-18', to: '2026-11-18', label: 'Workday' }] }));
  assert.deepEqual(ms.map((m) => m.date), ['2026-11-16', '2026-11-17', '2026-11-19', '2026-11-20', '2026-11-23', '2026-11-24', '2026-11-30', '2026-12-01']);
  const winter = E.meetings(COURSE.lessons, setup({ from: '2026-12-17', breaks: [{ from: '2026-12-21', to: '2027-01-01', label: 'Winter break' }] }));
  assert.deepEqual(winter.map((m) => m.date).slice(0, 4), ['2026-12-17', '2026-12-18', '2027-01-04', '2027-01-05']);
});
check('"Move today back one class" leaves today open and moves every later lesson one class; undoing closes it up', () => {
  const base = E.meetings(COURSE.lessons, setup());
  const moved = E.meetings(COURSE.lessons, setup({ moved: ['2026-11-18'] }));
  assert.equal(moved[2].kind, 'open');
  assert.deepEqual(moved.filter((m) => m.kind === 'lesson').map((m) => m.lessons[0].s), base.map((m) => m.lessons[0].s), 'same lessons, same order');
  assert.equal(moved[3].lessons[0].s, base[2].lessons[0].s);
  assert.equal(moved.at(-1).date, '2026-11-26', 'the plan ends one class later');
  assert.deepEqual(E.meetings(COURSE.lessons, setup({ moved: [] })), base);
  // a moved day that is not a class day changes nothing
  assert.deepEqual(E.meetings(COURSE.lessons, setup({ moved: ['2026-11-21'] })), base);
});
check('two lessons a meeting, and one lesson over two meetings', () => {
  const two = E.meetings(COURSE.lessons, setup({ per: 2 }));
  assert.equal(two.length, 4);
  assert.deepEqual(two[0].lessons.map((l) => l.s), ['p1', 'p2']);
  const half = E.meetings(COURSE.lessons, setup({ per: 0.5 }));
  assert.equal(half.length, 16);
  assert.deepEqual(half.slice(0, 4).map((m) => [m.lessons[0].s, m.part]), [['p1', 1], ['p1', 2], ['p2', 1], ['p2', 2]]);
});
check('weeks group by Monday, and a week names its days off; a first visit lays the sample from today so it is never stale', () => {
  const s = setup({ breaks: [{ from: '2026-11-25', to: '2026-11-27', label: 'Thanksgiving break' }] });
  const wk = E.weeks(E.meetings(COURSE.lessons, s), s);
  assert.deepEqual(wk.map((w) => w.monday), ['2026-11-16', '2026-11-23', '2026-11-30']);
  assert.deepEqual(wk[1].breaks, [{ label: 'Thanksgiving break', days: ['2026-11-25', '2026-11-26', '2026-11-27'] }]);
  assert.equal(E.spanWords(wk[1].breaks[0].days), 'Wednesday to Friday');
  assert.equal(E.spanWords(['2026-11-27']), 'Friday');
  for (const today of ['2026-11-20', '2027-03-07', '2028-02-29']) {
    const d = E.teacherSetup(undefined, today);
    assert.equal(d.from, E.addDays(E.mondayOf(today), -7));
    assert.equal(d.per, 1, 'one lesson a meeting unless the teacher says otherwise');
    assert.ok(E.meetings(Array.from({ length: 30 }, (_, i) => lesson(`m${i}`, i + 1)), d).some((m) => m.date >= today));
  }
});

console.log('Calendar: the calendar file');
const ics = (over = {}) => E.rhythmIcs({
  name: 'STEMhop: Biology Together', summary: 'Biology Together activity (STEMhop)',
  text: 'A hands-on activity for ages 5 to 10 with a grown-up. This entry names no activity, so it stays right if you skip a week or do two; what is next, and what to gather, are on this page:',
  url: 'https://stemhop.com/calendar/parent/', days: [6], from: '2026-11-20', count: 12, uid: 'test-1@stemhop.com', now: new Date('2026-11-20T15:04:05Z'), ...over,
});
/** A small RFC 5545 reader: unfold, split, and check the rules a calendar app enforces on import. */
function readIcs(text) {
  assert.ok(text.endsWith('\r\n'), 'ends with CRLF');
  assert.ok(!/[^\r]\n/.test(text) && !/\r[^\n]/.test(text), 'every line ends CRLF, nothing bare');
  for (const raw of text.split('\r\n')) assert.ok(Buffer.byteLength(raw, 'utf8') <= 75, `a line is over 75 octets: ${raw}`);
  const lines = text.replace(/\r\n[ \t]/g, '').split('\r\n').filter(Boolean);
  const stack = [];
  const props = [];
  for (const l of lines) {
    const m = l.match(/^([A-Z][A-Z0-9-]*)((?:;[A-Z-]+=[^;:]+)*):(.*)$/);
    assert.ok(m, `not a content line: ${l}`);
    if (m[1] === 'BEGIN') stack.push(m[3]);
    else if (m[1] === 'END') assert.equal(stack.pop(), m[3], 'BEGIN and END pair up');
    else props.push({ in: stack.at(-1), name: m[1], params: m[2], value: m[3] });
  }
  assert.equal(stack.length, 0);
  assert.equal(lines[0], 'BEGIN:VCALENDAR');
  assert.equal(lines.at(-1), 'END:VCALENDAR');
  const get = (where, name) => props.filter((p) => p.in === where && p.name === name);
  return { props, get, one: (where, name) => { const v = get(where, name); assert.equal(v.length, 1, `${where} has exactly one ${name}`); return v[0]; } };
}
check('it is valid iCalendar: required properties, CRLF, lines folded at 75 octets, text escaped', () => {
  const f = readIcs(ics());
  assert.equal(f.one('VCALENDAR', 'VERSION').value, '2.0');
  assert.ok(f.one('VCALENDAR', 'PRODID').value.length > 3);
  assert.ok(f.one('VEVENT', 'UID').value.includes('@'));
  assert.match(f.one('VEVENT', 'DTSTAMP').value, /^\d{8}T\d{6}Z$/);
  const start = f.one('VEVENT', 'DTSTART');
  assert.equal(start.params, ';VALUE=DATE');
  assert.equal(start.value, '20261121', 'the first Saturday from today');
  assert.equal(f.one('VEVENT', 'DTEND').value, '20261122', 'an all-day entry ends the next day');
  const text = f.one('VEVENT', 'DESCRIPTION').value;
  assert.ok(text.includes('\\,') && text.includes('\\;') && text.includes('\\n'), 'commas, semicolons and the line break are escaped');
  assert.ok(!/(^|[^\\])[,;]/.test(text), 'no bare comma or semicolon in text');
  assert.equal(f.one('VEVENT', 'URL').value, 'https://stemhop.com/calendar/parent/');
});
check('one repeating entry that ends by itself, on the right days, with no alarm and no person in it', () => {
  const f = readIcs(ics({ days: [5, 1, 3], count: 23 }));
  assert.equal(f.props.filter((p) => p.in === 'VEVENT' && p.name === 'UID').length, 1, 'one entry');
  const rule = Object.fromEntries(f.one('VEVENT', 'RRULE').value.split(';').map((kv) => kv.split('=')));
  assert.deepEqual(rule, { FREQ: 'WEEKLY', COUNT: '23', BYDAY: 'MO,WE,FR' });
  assert.equal(f.one('VEVENT', 'DTSTART').value, '20261120', 'a Friday: the first of those days from today');
  const whole = ics({ days: [5, 1, 3], count: 23 });
  for (const never of ['VALARM', 'ATTENDEE', 'ORGANIZER', 'mailto:', 'UNTIL']) assert.ok(!whole.includes(never), `no ${never}`);
  assert.equal(f.one('VEVENT', 'TRANSP').value, 'TRANSPARENT', 'it does not mark the day as busy');
  // the count is kept within sensible bounds, and no days means no file
  assert.match(ics({ count: 5000 }), /COUNT=104;/);
  assert.match(ics({ count: 0 }), /COUNT=1;/);
  assert.equal(ics({ days: [] }), '');
});
check('the first day of the entry always falls on one of its days, so no calendar app adds a stray first day', () => {
  let today = '2026-11-16';
  for (let i = 0; i < 14; i++, today = E.addDays(today, 1)) {
    for (const days of [[0], [6], [2, 4], [1, 2, 3, 4, 5]]) {
      const start = readIcs(ics({ days, from: today })).one('VEVENT', 'DTSTART').value;
      const iso = `${start.slice(0, 4)}-${start.slice(4, 6)}-${start.slice(6)}`;
      assert.ok(iso >= today && days.includes(E.dow(iso)), `${today} ${days} -> ${iso}`);
    }
  }
});
check('long and non-English text folds between characters, never inside one', () => {
  const f = ics({ summary: 'Étude — biología 生物学 '.repeat(8).trim(), name: 'x' });
  const got = readIcs(f).one('VEVENT', 'SUMMARY').value;
  assert.equal(got, 'Étude — biología 生物学 '.repeat(8).trim());
  assert.ok(!Buffer.from(f, 'utf8').toString('utf8').includes('�'));
  assert.equal(E.foldLine('a'.repeat(200)).split('\r\n ').map((s) => s.length).join(','), '75,74,51');
});

console.log('Calendar: what is kept on the device');
check('a parent\'s and a learner\'s saved plan never holds a date, whatever they do', () => {
  let p = E.newParent();
  p = { ...p, days: [3, 6], list: 3, have: { [E.lineKey('A jar')]: 1 } };
  p = E.parentDid(p, ACTS[0]);
  p = E.parentPick(ACTS, p, 'e');
  p = E.parentUndid(p, 'a');
  const s = { ...E.newStudent(), plan: 'mcat', days: [1, 3, 5], start: { physiology: 'p6' }, sit: 180, out: ['cell-biology'], opt: ['sensory-systems'], marks: ['mcat:diagnostic', 'mcat:set:one'] };
  const state = E.cleanState(JSON.parse(JSON.stringify({ v: 1, parent: p, student: s })));
  assert.deepEqual(state.parent, p);
  assert.deepEqual(state.student, s);
  assert.equal(E.holdsDate(state.parent), false);
  assert.equal(E.holdsDate(state.student), false);
  // the checker itself notices every shape a date could take
  for (const d of ['2026-11-20', '2026-11-20T10:00:00Z', '11/20/2026', '20261120', 1795197432634, 1795197432, 20777, { x: ['2026-1-5'] }, { '2026-11-20': 1 }]) assert.equal(E.holdsDate(d), true, JSON.stringify(d));
});
check('anything date-like that reaches storage by another road is dropped on the way back in', () => {
  const dirty = {
    v: 1,
    parent: { days: [6, 9, 'x'], order: ['a', '2026-11-20', 7], done: ['b'], have: { abc: 1, '2026-11-20': 1 }, list: 2, doneOn: { a: '2026-11-20' }, skip: '2026-11-21', start: 1795197432634 },
    student: { plan: 'physiology', days: [1], start: { physiology: 'p6', when: '2026-11-20' }, sit: 61, out: [], opt: [], marks: ['mcat:diagnostic'], test: '2027-05-14', later: '2026-11-20', last: 1795197432634 },
    extra: '2026-11-20',
  };
  const clean = E.cleanState(dirty);
  assert.equal(E.holdsDate(clean.parent), false);
  assert.equal(E.holdsDate(clean.student), false);
  assert.deepEqual(clean.parent, { order: ['a'], done: ['b'], have: { abc: 1 }, days: [6], list: 2 });
  assert.deepEqual(clean.student, { days: [1], start: { physiology: 'p6' }, sit: 0, out: [], opt: [], marks: ['mcat:diagnostic'], plan: 'physiology' });
  assert.deepEqual(Object.keys(clean).sort(), ['parent', 'student', 'v']);
  for (const junk of [null, 'x', 7, [], { parent: 'no' }]) assert.deepEqual(E.cleanState(junk), { v: 1 });
});
check('the test date, "Later" and "Not this week" live in the visit, and the page saves only the plan', () => {
  const src = readFileSync(path('../src/lib/calendar/client.ts'), 'utf8');
  const writes = [...src.matchAll(/localStorage\.setItem\((.*?)\);/g)].map((m) => m[1]);
  assert.deepEqual(writes.sort(), ["KEY, '{\"v\":1}'", 'KEY, JSON.stringify(model.state)'].sort(), 'two writes: a probe that is removed at once, and the plan');
  assert.ok(!/sessionStorage|document\.cookie|fetch\(|XMLHttpRequest|sendBeacon/.test(src), 'no other store, and no network request');
  assert.ok(/model\.visit\.test = /.test(src) && /model\.visit\.later = true/.test(src) && /model\.visit\.skip = true/.test(src));
  assert.ok(!/state\.(student|parent)[^;\n]*\.(test|later|skip)\b/.test(src), 'none of them is put in the saved plan');
  assert.match(src, /const KEY = 'stemhop:calendar:v1'/);
});
check('only a class plan keeps dates, and it is checked on the way in', () => {
  const t = E.cleanState({ teacher: { course: 'high-school-biology', from: '2026-11-16', meet: [1, 3, 5, 8], per: 0.5, breaks: [{ from: '2026-11-25', to: '2026-11-27', label: 'Thanks<b>giving' }, { from: '2026-12-01', to: '2026-11-01', label: 'backwards' }, { from: 'x', to: 'y' }], moved: ['2026-11-18', 'soon', '2026-11-18'] } }).teacher;
  assert.deepEqual(t, { moved: ['2026-11-18'], course: 'high-school-biology', from: '2026-11-16', meet: [1, 3, 5], per: 0.5, breaks: [{ from: '2026-11-25', to: '2026-11-27', label: 'Thanksbgiving' }] });
});
check('the email switch is off, and nothing in the calendar sends anything', () => {
  assert.match(readFileSync(path('../src/lib/calendar/flags.ts'), 'utf8'), /export const EMAIL_OPT_IN = false;/);
  const wr = readFileSync(path('../wrangler.jsonc'), 'utf8');
  assert.ok(!/"triggers"\s*:/.test(wr), 'no scheduler was added');
  assert.ok(!/scheduled\s*\(/.test(readFileSync(path('../worker/index.js'), 'utf8')), 'no scheduled handler was added');
});

console.log(`\n${n} checks passed.`);
