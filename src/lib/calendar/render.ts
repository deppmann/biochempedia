/* =============================================================================
   The calendar's three views, as HTML strings. The same functions run when the
   site is built (no date is known then, so the page is drawn without dates and
   is true on any day, with JavaScript off) and in the browser (where today's
   date is known and the plan kept on the device is used).

   Every value that comes from data goes through esc(). Words taken from a guide
   (how long, your part, what to gather, the safety notes) are printed exactly
   as the guide has them.
   ============================================================================ */
import {
  type Activity, type CourseData, type Item, type Iso, type Lesson, type McatData, type ParentPlan, type Reach, type Sitting,
  type StudentPlan, type TeacherPlan, type Meeting, type Visit,
  WD, WEEK_ORDER, addDays, cap, clock, courseItems, daysBetween, daysPhrase, filmMin, fullDate, gather, itemMinutes, longDate,
  mcatIncluded, mcatItems, meetings, mondayOf, monthDay, num, onDays, parentView, reach, shortDate, spanWords, studentView, summerOf, teacherSetup,
  weekday, weeks, DIAG_KEY,
} from './engine';

export const esc = (s: unknown) =>
  String(s ?? '').replace(/[&<>"']/g, (c) => ({ '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#39;' })[c]!);

export type Role = 'parent' | 'student' | 'teacher';

/** What a tap just did: one sentence, and the control that undoes it. */
export interface Said { text: string; undo?: string; undoName?: string }

export interface Ui {
  /** Today, in the browser. Absent when the site is built: then nothing is dated. */
  today?: Iso;
  said?: Said;
  /** False when the browser will not let the page save. */
  kept?: boolean;
  /** The opt-in email button. Off: see flags.ts. */
  email?: boolean;
  /** Asleep Hex, drawn once by the page for the emptied-day card. */
  hex?: string;
  /** Titles of things in this plan already done today. */
  doneToday?: string[];
  /** Something the person has to put right, shown beside the field it is about. */
  err?: { at: 'break-from' | 'break-to' | 'meet'; text: string };
}

const WHERE = { indoors: 'Indoors', outdoors: 'Outdoors', either: 'Indoors or outdoors' } as const;
const WHERE_SHORT = { indoors: 'indoors', outdoors: 'outdoors', either: 'indoors or out' } as const;

/* ---------- shared pieces ---------- */

const ROLE_LINKS: [Role, string, string][] = [
  ['parent', 'With a child', '/calendar/parent/'],
  ['student', 'For myself', '/calendar/student/'],
  ['teacher', 'For my class', '/calendar/teacher/'],
];

export function roleRow(role?: Role): string {
  return `<nav class="cal-roles cal-noprint" aria-label="Who the calendar is for"><ul>${ROLE_LINKS.map(
    ([r, label, href]) => `<li><a href="${href}" data-role="${r}"${r === role ? ' aria-current="page"' : ''}>${label}</a></li>`,
  ).join('')}</ul></nav>`;
}

function noteSlot(ui: Ui): string {
  const s = ui.said;
  if (!s) return '<div class="cal-note-slot"></div>';
  return `<div class="cal-note-slot"><p class="cal-said cal-noprint"><span>${esc(s.text)}</span>${
    s.undo ? ` <button type="button" class="cal-linkbtn" data-act="undo" data-fid="undo" aria-label="${esc(s.undoName ?? s.undo)}">${esc(s.undo)}</button>` : ''
  }</p></div>`;
}

function dayChecks(days: number[], name: string): string {
  return `<div class="cal-days">${WEEK_ORDER.map(
    (d) => `<label class="cal-day"><input type="checkbox" name="${name}" value="${d}"${days.includes(d) ? ' checked' : ''}><span><span aria-hidden="true">${WD[d].slice(0, 3)}</span><span class="visually-hidden">${WD[d]}</span></span></label>`,
  ).join('')}</div>`;
}

const opt = (value: string | number, label: string, on: boolean) => `<option value="${esc(value)}"${on ? ' selected' : ''}>${esc(label)}</option>`;

function keptLine(ui: Ui, what: string, more = ''): string {
  if (!ui.today) return '';
  return `<p class="cal-foot cal-noprint">${
    ui.kept === false
      ? `This browser is not letting the page save anything, so ${what} lasts until you close the page.`
      : `${cap(what)} stays on this device and goes nowhere else.${more}`
  } <button type="button" class="cal-linkbtn" data-act="forget" data-fid="forget">Forget what the calendar keeps here</button></p>`;
}

/** A sentence closed once: no second full stop after a title that ends in one or in a question mark. */
export const end = (s: string) => (/[.?!]$/.test(s) ? s : `${s}.`);

const NOSCRIPT = 'The days are worked out in your browser, and that needs JavaScript. Without it, here is the plan in order. Start anywhere.';

/** "Today, Friday, November 20", "Tomorrow, Saturday, November 21", "Monday, November 23" */
function dateLabel(d: Iso, today: Iso): string {
  const n = daysBetween(today, d);
  return `${n === 0 ? 'Today, ' : n === 1 ? 'Tomorrow, ' : ''}${longDate(d)}`;
}

/* ============================================================================
   Parent: with a child
   ============================================================================ */

function rhythmSentence(days: number[]): string {
  if (!days.length) return 'One activity at a time, on no set day.';
  if (days.length === 1) return `One activity a week, ${onDays(days)}.`;
  return `${cap(num(days.length))} a week, ${onDays(days)}.`;
}

const howLong = (a: Activity) => `About ${a.min} minutes${a.follow ? `, ${a.follow}` : ''}`;

function activityCard(a: Activity, canSkip: boolean): string {
  const safety = a.safety.map((s) => `<li>${esc(s)}</li>`).join('');
  const film = a.film && a.poster
    ? `<a class="cal-poster cal-noprint" href="${esc(a.film.href)}"><img src="${esc(a.poster)}" alt="" width="160" height="90"><span class="cal-poster-cap"><span class="cal-play" aria-hidden="true"></span>Setup film, ${clock(a.film.sec)}<span class="visually-hidden"> for the grown-up</span></span></a>`
    : '';
  return `<article class="cal-card" aria-labelledby="cal-act-t">
  <div class="cal-card-head">
    <div>
      <h2 class="cal-card-t" id="cal-act-t"><a href="/lessons/${esc(a.s)}/" data-fid="title">${esc(a.t)}</a></h2>
      <p class="cal-hook">${esc(a.hook)}</p>
    </div>
    ${film}
  </div>
  <dl class="cal-facts">
    <div><dt>How long</dt><dd>${esc(howLong(a))}</dd></div>
    <div><dt>Where</dt><dd>${WHERE[a.setting]}</dd></div>
    <div><dt>Your part</dt><dd>${esc(a.adult)}</dd></div>
  </dl>
  <details class="cal-fold cal-safety cal-noprint" data-fold="safety"><summary>The guide’s safety notes <span class="cal-count">(${a.safety.length})</span></summary><ul>${safety}</ul></details>
  <div class="cal-do cal-noprint">
    <a class="cal-btn cal-btn-main" href="/lessons/${esc(a.s)}/" data-fid="open">Open the guide</a>
    <button type="button" class="cal-btn" data-js data-act="did" data-s="${esc(a.s)}" data-fid="did" aria-label="We did it: ${esc(a.t)}">We did it</button>
    ${canSkip ? `<button type="button" class="cal-btn" data-js data-act="skip" data-fid="skip" aria-label="Not this week: ${esc(a.t)} waits for the next one">Not this week</button>` : ''}
    <button type="button" class="cal-btn cal-btn-quiet" data-js data-act="choose" data-fid="choose">Choose a different one</button>
  </div>
</article>`;
}

export function renderParent(acts: Activity[], plan: ParentPlan, visit: Visit, ui: Ui): string {
  const today = ui.today;
  const v = parentView(acts, plan, today ?? '2000-01-01', { skip: visit.skip, used: visit.used });
  const a = v.next;
  const date = today ? v.date : undefined;
  const size = a ? `One activity, about ${a.min} minutes, ${WHERE_SHORT[a.setting]}.` : '';

  let h1 = 'The next activity';
  let lede = size;
  if (!a) {
    h1 = 'Every activity, done';
    lede = `You have done all ${acts.length} activities in Biology Together. Each guide links one step up to a matching grade 7 Life Science lesson, where there is one.`;
  } else if (date && today) {
    const n = daysBetween(today, date);
    h1 = n === 0 ? 'Today' : n <= 6 ? `This ${weekday(date)}` : longDate(date);
    lede = n > 6 ? size : `${n === 0 ? longDate(date) : n === 1 ? `Tomorrow, ${monthDay(date)}` : monthDay(date)}. ${size}`;
  } else if (today) {
    lede = `${size} No day is set, so it is here when you are.`;
  }

  const set = today ? `<details class="cal-set cal-noprint" data-fold="set">
    <summary><span>${esc(rhythmSentence(v.days))}</span> <span class="cal-change cal-closed">Change</span><span class="cal-change cal-open">Close</span></summary>
    <div class="cal-set-body">
      <fieldset><legend>Which days suit you?</legend>${dayChecks(v.days, 'pdays')}</fieldset>
      <p class="cal-sub">Pick one, a few, or none. Activities come in the course’s order, and one you don’t get to simply waits.</p>
    </div>
  </details>` : `<p class="cal-plan">${esc(rhythmSentence(v.days))}</p>`;

  /* What to gather: one list, each guide's own lines in its own order. */
  const n = plan.list ?? 1;
  const forActs = v.queue.slice(0, n);
  const lines = gather(forActs);
  const many = forActs.length > 1;
  const gatherHtml = a ? `<section class="cal-gather" aria-labelledby="cal-gather-h">
  <h2 id="cal-gather-h">What to gather</h2>
  <p class="cal-sub">Each line as the guide writes it${many ? ', in each guide’s own order' : ''}.${today ? '<span class="cal-noprint"> Tick what you have; the ticks stay on this device.</span>' : ''}</p>
  ${today && v.queue.length > 1 ? `<fieldset class="cal-seg cal-noprint"><legend>List for</legend>${([1, 2, 3] as const)
    .filter((k) => k <= v.queue.length)
    .map((k) => `<label><input type="radio" name="plist" value="${k}"${k === n ? ' checked' : ''}><span>${k === 1 ? 'This one' : `Next ${num(k)}`}</span></label>`)
    .join('')}</fieldset>` : ''}
  ${forActs.map((act) => {
    const mine = lines.filter((l) => l.for[0] === act);
    if (!mine.length) return '';
    return `${many ? `<h3>For ${esc(act.t)}</h3>` : ''}<ul class="cal-supplies">${mine
      .map((l) => `<li><label class="cal-check"><input type="checkbox" data-have="${l.key}"${plan.have[l.key] ? ' checked' : ''}><span class="cal-box" aria-hidden="true"></span><span class="cal-line">${esc(l.text)}${
        l.for.length > 1 ? `<span class="cal-for">Also for ${l.for.slice(1).map((x) => esc(x.t)).join(' and ')}</span>` : ''
      }${/observation sheet/i.test(l.text) ? `<span class="cal-for">The sheet is in the guide: <a href="/lessons/${esc(act.s)}/">stemhop.com/lessons/${esc(act.s)}/</a></span>` : ''}</span></label></li>`)
      .join('')}</ul>`;
  }).join('')}
  ${forActs.map((x) => `<div class="cal-print-only cal-print-safety"><h3>Safety, from the guide: ${esc(x.t)}</h3><ul>${x.safety.map((s) => `<li>${esc(s)}</li>`).join('')}</ul><p>The steps are in the guide: stemhop.com/lessons/${esc(x.s)}/</p></div>`).join('')}
</section>` : '';

  const count = Math.min(v.queue.length, 12);
  const keep = today && a ? `<section class="cal-keep cal-noprint" aria-labelledby="cal-keep-h">
  <h2 id="cal-keep-h">Keep it where you’ll see it</h2>
  <ul class="cal-keep-list">
    <li><button type="button" class="cal-btn" data-act="print" data-fid="print">Print this week</button><span>For the fridge: the activity, the list to gather, and the guide’s safety notes in full for every activity on the list.</span></li>
    <li>${v.days.length
      ? `<button type="button" class="cal-btn" data-act="ics" data-fid="ics">Add ${esc(daysPhrase(v.days))} to my calendar</button><span>One repeating entry that links back to this page. It names no activity, so it stays right if you skip a week or do two. It repeats ${count === 1 ? 'once' : `${num(count)} times`} and then ends, sets no alarm, and needs no email address.</span>`
      : '<span>A calendar needs a day. Pick one under Change, above, and the calendar file is ready. It needs no email address.</span>'}</li>
    ${ui.email ? '<li><button type="button" class="cal-btn" data-act="email" data-fid="email">Email me two days before</button><span>One short email before each activity day, with the list to gather and the safety notes. Every email has a one-click stop.</span></li>' : ''}
  </ul>
</section>` : '';

  const after = v.after.length ? `<section class="cal-after cal-noprint" aria-labelledby="cal-after-h">
  <h2 id="cal-after-h">After that</h2>
  <ol class="cal-next">${v.after
    .map(({ act, date: d }) => `<li>${d && today ? `<span class="cal-date">${shortDate(d)}</span>` : ''}<span class="cal-next-body"><a href="/lessons/${esc(act.s)}/">${esc(act.t)}</a><span class="cal-meta">${esc(howLong(act))}. ${WHERE[act.setting]}.</span></span></li>`)
    .join('')}</ol>
  <p class="cal-sub">If a day goes by, nothing is lost: the activity waits for the next one.</p>
</section>` : '';

  const done = v.done.length ? `<section class="cal-record cal-noprint" aria-labelledby="cal-done-h">
  <h2 id="cal-done-h">Done together</h2>
  <ul>${[...v.done].reverse()
    .map((d) => `<li><span class="cal-next-body"><a href="/lessons/${esc(d.s)}/">${esc(d.t)}</a></span><button type="button" class="cal-linkbtn" data-act="undid" data-s="${esc(d.s)}" data-fid="undid-${esc(d.s)}" aria-label="Put it back: ${esc(d.t)} returns to the plan">Put it back</button></li>`)
    .join('')}</ul>
</section>` : '';

  const freed = v.freed && a && date ? `<p class="cal-said cal-freed cal-noprint"><span>Nothing ${daysBetween(today!, v.freed) === 0 ? 'today' : `this ${weekday(v.freed)}`}. ${esc(a.t)} waits for ${longDate(date)}.</span> <button type="button" class="cal-linkbtn" data-act="unskip" data-fid="unskip" aria-label="Put it back: ${esc(a.t)} on ${weekday(v.freed)}">Put it back</button></p>` : '';

  return `<div class="cal-page cal-parent">
<header class="cal-top">
  ${roleRow('parent')}
  <h1 tabindex="-1">${esc(h1)}</h1>
  <p class="cal-lede">${esc(lede)}${!a ? ' <a href="/courses/life-science/">Look at grade 7 Life Science</a>' : ''}</p>
  ${set}
</header>
${noteSlot(ui)}
<div class="cal-cols">
  <div class="cal-main">${freed}${a ? activityCard(a, !!date && !v.freed) : ''}</div>
  <div class="cal-side">${gatherHtml}${keep}</div>
  <div class="cal-later">${after}${done}</div>
</div>
<p class="cal-print-only cal-print-foot">From the STEMhop calendar, stemhop.com/calendar/parent/. Biology Together is free, for ages 5 to 10 with a grown-up.</p>
${keptLine(ui, 'this plan')}
${today ? '' : `<noscript><div class="cal-noscript"><p>${NOSCRIPT}</p><ol>${acts.map((x) => `<li><a href="/lessons/${esc(x.s)}/">${esc(x.t)}</a> <span class="cal-meta">${x.min} minutes, ${WHERE_SHORT[x.setting]}</span></li>`).join('')}</ol></div></noscript>`}
</div>`;
}

/** Inside the "Choose a different one" dialog: every activity, by unit. */
export function chooserList(acts: Activity[]): string {
  const units = [...new Set(acts.map((a) => a.unit))];
  return units
    .map((u, i) => `<h3>Unit ${i + 1}: ${esc(u)}</h3><ul class="cal-choose">${acts
      .filter((a) => a.unit === u)
      .map((a) => `<li><button type="button" class="cal-choice" data-act="pick" data-s="${esc(a.s)}"><span class="cal-choice-t">${esc(a.t)}</span><span class="cal-meta">${a.min} minutes, ${WHERE_SHORT[a.setting]}</span></button></li>`)
      .join('')}</ul>`)
    .join('');
}

/* ============================================================================
   Student: for myself
   ============================================================================ */

/** The true size of one thing, in the words that fit what it is. */
export function sizeLine(it: Item): string {
  const film = filmMin(it.filmSec);
  if (it.kind === 'diag') return `About ${it.read} minutes.`;
  if (it.kind === 'set') return `About ${it.read} minutes at exam pace.`;
  if (it.school) return `One class period, about ${it.read} minutes${film ? `, with ${film} ${film === 1 ? 'minute' : 'minutes'} of film` : ''}.`;
  return film ? `About ${it.read + film} minutes: ${it.read} to read, ${film} of film.` : `About ${it.read} minutes to read.`;
}
const sittingSize = (s: Sitting) => (s.items.length === 1 ? sizeLine(s.items[0]) : `About ${s.min} minutes in all${s.film ? `: ${s.read} to read, ${s.film} of film` : ''}.`);
const rowMeta = (s: Sitting) => {
  const one = s.items.length === 1 ? s.items[0] : undefined;
  if (one?.school) return `${one.read} min class period${s.film ? `, ${s.film} min of film` : ''}`;
  return `${s.min} min${s.film ? `: ${s.read} min to read, ${s.film} min of film` : ''}`;
};

const SIT_WORDS: Record<number, string> = { 0: 'one lesson at a time', 60: 'about an hour at a sitting', 90: 'about an hour and a half at a sitting', 120: 'about two hours at a sitting', 180: 'about three hours at a sitting' };

export interface StudentPage {
  /** A course, or the MCAT path. */
  course?: CourseData;
  mcat?: McatData;
  /** Every plan a learner can pick, for the "What to keep up with" list. */
  choices: { s: string; t: string; level: string }[];
}

function topCard(s: Sitting, date: Iso | undefined, ui: Ui, mcat: boolean): string {
  const it = s.items[0];
  const many = s.items.length > 1;
  const today = ui.today;
  const when = date && today ? `<time datetime="${date}">${dateLabel(date, today)}</time>` : 'Next';
  const open = many ? 'Open the first' : it.kind === 'lesson' ? 'Open the lesson' : 'Open it';
  const name = many ? 'this sitting' : it.t;
  const rest = many ? `<p class="cal-also">Also in this sitting:</p><ol class="cal-sit-list">${s.items.slice(1).map((x) => `<li><a href="${esc(x.href)}">${esc(x.t)}</a> <span class="cal-meta">${itemMinutes(x)} min</span></li>`).join('')}</ol>` : '';
  const film = !many && it.watch && it.filmSec ? `<p class="cal-film"><a href="${esc(it.watch)}">Watch the ${it.films > 1 ? 'films' : 'film'} first</a> <span class="cal-meta">(${filmMin(it.filmSec)} min)</span></p>` : '';
  const rung = !many && it.down ? `<p class="cal-rung">The same idea, told more simply, if you want it first: <a href="/lessons/${esc(it.down.s)}/">${esc(it.down.t)}</a> (${esc(it.down.level)}).</p>` : '';
  return `<section class="cal-card" aria-labelledby="cal-top-t">
  <p class="cal-when">${when} <span class="cal-meta"><span aria-hidden="true">·</span> ${esc(it.where)}</span></p>
  <h2 class="cal-card-t" id="cal-top-t"><a href="${esc(it.href)}" data-fid="title">${esc(it.t)}</a></h2>
  ${!many && it.hook ? `<p class="cal-hook">${esc(it.hook)}</p>` : ''}
  ${rest}
  <p class="cal-size">${esc(sittingSize(s))}</p>
  ${film}${rung}
  <div class="cal-do">
    <a class="cal-btn cal-btn-main" href="${esc(it.href)}" data-fid="open">${open}</a>
    <button type="button" class="cal-btn" data-js data-act="done" data-fid="done" aria-label="Done: ${esc(name)}">Done</button>
    ${date && today && date === today ? `<button type="button" class="cal-btn" data-js data-act="later" data-fid="later" aria-label="Later: move ${esc(name)} to the next day">Later</button>` : ''}
  </div>
  ${mcat && it.kind === 'set' ? '<p class="cal-sub">Exam pace is about 8 minutes for a passage like this.</p>' : ''}
</section>`;
}

/** A date with its year when the year is not this one: "March 17" or "March 17, 2027". */
const dateIn = (d: Iso, today: Iso) => (d.slice(0, 4) === today.slice(0, 4) ? monthDay(d) : fullDate(d));

function reachSentence(r: Reach, test: Iso | undefined, today: Iso): string {
  if (!test) return '';
  const t = fullDate(test);
  switch (r.kind) {
    case 'passed': return 'That date is today or has passed. Pick a later one, or leave it empty.';
    case 'no-days': return 'Tick the days you study, under Change at the top, and this line will say when the lessons would end.';
    case 'fits': return `At this rhythm the lessons here end around ${dateIn(r.end!, today)}, before your test on ${t}. The time between is for the subjects this site does not have and for full-length practice.`;
    case 'close': return `At this rhythm the lessons here end around ${dateIn(r.end!, today)}, close to your test on ${t}. That leaves little room for the subjects this site does not have. A longer sitting, another day a week, or leaving out a course you already know would open some.`;
    case 'beyond': {
      const w = r.ways ?? {};
      const ways = [
        w.hours ? `about ${w.hours.needed} hours a week instead of ${w.hours.now}` : '',
        w.course ? 'leaving out a course you already know (untick it above)' : '',
        w.films ? 'reading without the films' : '',
      ].filter(Boolean);
      if (ways.length === 1) return `At this rhythm the lessons here run past ${t}. ${cap(ways[0])} would finish them before it.`;
      const lead = ways.length === 2 ? 'Either of these would finish them before it' : 'Any one of these would finish them before it';
      return `At this rhythm the lessons here run past ${t}. ${lead}: ${ways.slice(0, -1).join('; ')}; or ${ways[ways.length - 1]}.`;
    }
    case 'far-beyond': return `The whole path does not fit before ${t}, and no single change here would make it fit. Untick the courses you already know, above, and start with the ones you need most. Each one stands on its own.`;
    default: return '';
  }
}

export function renderStudent(page: StudentPage, plan: StudentPlan, done: ReadonlySet<string>, visit: Visit, ui: Ui): string {
  const today = ui.today;
  const { course, mcat } = page;
  const key = mcat ? 'mcat' : course!.s;
  const name = mcat ? 'the MCAT path' : course!.t;
  const start = course ? plan.start[course.s] : undefined;
  const items = mcat ? mcatItems(mcat, plan) : courseItems(course!, start);
  const days = today ? plan.days : [];
  const sit = mcat ? plan.sit : 0;
  const v = studentView(items, done, { days, sit }, today ?? '2000-01-01', { later: visit.later, spent: !!ui.doneToday?.length });

  const sentence = `${cap(name)}${mcat ? `, ${SIT_WORDS[sit]}` : ''}, ${days.length ? onDays(days) : 'with no set days'}.`;
  const groups = [...new Set(page.choices.map((c) => c.level))];
  const set = today ? `<details class="cal-set" data-fold="set">
    <summary><span>${esc(sentence)}</span> <span class="cal-change cal-closed">Change</span><span class="cal-change cal-open">Close</span></summary>
    <div class="cal-set-body">
      <label class="cal-field"><span>What to keep up with</span><select name="splan">${groups
        .map((g) => `<optgroup label="${esc(g)}">${page.choices.filter((c) => c.level === g).map((c) => opt(c.s, c.t, c.s === key)).join('')}</optgroup>`)
        .join('')}<optgroup label="A path">${opt('mcat', 'The MCAT path: biology and biochemistry', key === 'mcat')}</optgroup></select></label>
      <button type="button" class="cal-btn cal-go" data-act="go-plan" data-fid="go-plan">Go to it</button>
      <fieldset><legend>Days I usually study <span class="cal-opt">(optional)</span></legend>${dayChecks(days, 'sdays')}</fieldset>
      <p class="cal-sub">Tick days and the lessons get dates, counted from today. Untick them all and the dates go away. Either way, a lesson you don’t get to simply waits.</p>
      ${course ? `<label class="cal-field"><span>Start at</span><select name="sstart">${course.lessons.map((l, i) => opt(i === 0 ? '' : l.s, `${l.n}. ${l.t}`, (start ?? '') === (i === 0 ? '' : l.s))).join('')}</select></label>
      <p class="cal-sub">Start wherever your class is. Earlier lessons stay one tap away.</p>` : `<label class="cal-field"><span>A sitting holds</span><select name="ssit">${Object.entries(SIT_WORDS).map(([k, w]) => opt(k, w.replace(' at a sitting', ''), Number(k) === sit)).join('')}</select></label>`}
    </div>
  </details>` : `<p class="cal-plan">${esc(sentence)}</p>`;

  /* The first card, or the emptied day. */
  let main = '';
  if (v.emptied && today) {
    const to = v.top?.date;
    main += `<section class="cal-card cal-empty" aria-labelledby="cal-empty-t">
  ${ui.hex ?? ''}
  <div>
    <p class="cal-when"><time datetime="${today}">${dateLabel(today, today)}</time></p>
    <h2 class="cal-card-t" id="cal-empty-t">Nothing today.</h2>
    <p>It moved to ${to ? (daysBetween(today, to) === 1 ? 'tomorrow' : `your next study day, ${longDate(to)}`) : 'your next study day'}.</p>
    <button type="button" class="cal-btn" data-act="unlater" data-fid="unlater" aria-label="Put it back: today holds it again">Put it back</button>
  </div>
</section>`;
  }
  if (ui.doneToday?.length) main += `<p class="cal-donetoday">Done today: ${esc(end(ui.doneToday.join(', ')))}</p>`;
  if (v.top && !v.emptied) main += topCard(v.top.sitting, v.top.date, ui, !!mcat);
  if (!v.top) {
    const partial = mcat ? mcatIncluded(mcat, plan).length < mcat.steps.length : !!start;
    const up = course?.up;
    main += `<section class="cal-card"><h2 class="cal-card-t">That is the last lesson in ${esc(name)}${partial ? (mcat ? ', for the courses you kept' : ', from where you started') : ''}.</h2><p>${
      partial ? `${mcat ? 'The courses you left out' : 'Earlier lessons'} are in the whole ${mcat ? 'path' : 'course'}, below. ` : ''
    }${up ? `${esc(up.t)} takes the same ideas further, when you want it.` : 'Where next is yours to pick.'}</p><div class="cal-do">${
      up ? `<a class="cal-btn cal-btn-main" href="/calendar/student/${esc(up.s)}/" data-fid="open">Go on to ${esc(up.t)}</a><a class="cal-btn cal-btn-quiet" href="/courses/">Look at the other courses</a>` : '<a class="cal-btn cal-btn-main" href="/courses/" data-fid="open">Look at the other courses</a>'
    }</div></section>`;
  }

  const rowList = v.emptied && v.top ? [v.top, ...v.rows] : v.rows;
  const labels = ['Then', 'After that', 'And then'];
  const rows = rowList.length ? `<ol class="cal-next cal-then">${rowList
    .map((r, i) => {
      const s = r.sitting;
      const it = s.items[0];
      return `<li><span class="cal-date">${r.date && today ? shortDate(r.date) : labels[i]}</span><span class="cal-next-body"><span><a href="${esc(it.href)}">${esc(it.t)}</a>${s.items.length > 1 ? ` <span class="cal-more">+${s.items.length - 1} more</span>` : ''}</span><span class="cal-meta">${esc(rowMeta(s))}</span></span></li>`;
    })
    .join('')}</ol>` : '';

  /* MCAT: the courses, a test date if the person has one, and what is not here. */
  let side = '';
  if (mcat) {
    const inc = mcatIncluded(mcat, plan).map((s) => s.s);
    const r = reach(items.filter((i) => !done.has(i.key)), sit, days, today ?? '2000-01-01', visit.test, !!v.emptied || v.spent);
    side += `<section class="cal-path" aria-labelledby="cal-path-h">
  <h2 id="cal-path-h">The courses</h2>
  <p class="cal-sub">In the path’s order. Untick a course you already know to leave it out.</p>
  <ul class="cal-courses">${mcat.steps
    .map((s) => `<li><label class="cal-check"><input type="checkbox" name="scourse" value="${esc(s.s)}"${inc.includes(s.s) ? ' checked' : ''}${today ? '' : ' disabled'}><span class="cal-box" aria-hidden="true"></span><span class="cal-line"><strong>${esc(s.t)}</strong>${s.optional ? ' (optional on the path)' : ''}<span class="cal-for">${s.lessons.length} lessons. ${esc(s.why)}</span></span></label></li>`)
    .join('')}</ul>
  ${today ? `<label class="cal-field cal-test"><span>Test date, if you have one <span class="cal-opt">(asked each visit, never saved)</span></span><input type="date" name="stest" value="${esc(visit.test ?? '')}" min="${addDays(today, 1)}"></label>
  <p class="cal-reach" id="cal-reach">${esc(reachSentence(r, visit.test, today))}</p>` : ''}
</section>
<section class="cal-scope" aria-labelledby="cal-scope-h">
  <h2 id="cal-scope-h">Not on STEMhop yet</h2>
  <p>${esc(mcat.scope)} Leave room for them. The diagnostic is a practice check, not a predictor of your score, and every question here was written for this site; none is a real AAMC question.</p>
  <p>The official practice exams and the fee assistance program come from the exam’s maker: ${mcat.links.map((l) => `<a href="${esc(l.href)}" rel="noopener">${esc(l.label)}</a>`).join(' and ')}.</p>
</section>`;
  }
  const open = v.all.length;
  if (today) {
    side += `<section class="cal-keep" aria-labelledby="cal-keep-h">
  <h2 id="cal-keep-h">Keep it where you’ll see it</h2>
  <ul class="cal-keep-list"><li>${days.length && open
    ? `<button type="button" class="cal-btn" data-act="ics" data-fid="ics">Add ${esc(daysPhrase(days))} to my calendar</button><span>One repeating entry on your days that links back to this page. It names no lesson, so it stays right when you get ahead or take a week off. It ends by itself, sets no alarm, and needs no account and no address.</span>`
    : '<span>A calendar needs days. Tick the days you study, under Change at the top, and a calendar file is ready. It needs no account and no address.</span>'}</li></ul>
</section>`;
  }

  /* The whole plan, closed: for finding your place, never a count. */
  const all = mcat ? mcatItems(mcat, plan) : courseItems(course!);
  const nextKey = v.all[0]?.items[0]?.key;
  const unitNames = [...new Set(all.map((i) => i.unit))];
  const whole = `<details class="cal-fold cal-whole" data-fold="whole"${today ? '' : ' open'}>
  <summary><h2>${mcat ? 'The whole path, in order' : 'The whole course, in order'}</h2></summary>
  ${today ? '' : `<noscript><p class="cal-sub">${NOSCRIPT}</p></noscript>`}
  ${unitNames
    .map((u, ui2) => `<h3>${mcat || !course ? esc(u) : `Unit ${ui2 + 1}: ${esc(u)}`}</h3><ol class="cal-plain">${all
      .filter((i) => i.unit === u)
      .map((i) => `<li${i.key === nextKey ? ' class="is-next"' : ''}><a href="${esc(i.href)}">${esc(i.t)}</a>${
        done.has(i.key)
          ? ` <span class="cal-meta">done</span> <button type="button" class="cal-linkbtn" data-js data-act="undone" data-key="${esc(i.key)}" data-fid="undone-${esc(i.key)}" aria-label="Put it back: ${esc(i.t)} is not done">Put it back</button>`
          : i.key === nextKey && today ? ' <span class="cal-meta">next</span>' : ''
      }</li>`)
      .join('')}</ol>`)
    .join('')}
</details>`;

  const lede = mcat
    ? 'The biology and biochemistry the exam leans on, with practice placed after the lessons it draws on. No dates unless you ask for them.'
    : 'One lesson at a time, in the course’s order. No dates unless you ask for them, and a lesson you don’t get to simply waits.';

  return `<div class="cal-page cal-student">
<header class="cal-top">
  ${roleRow('student')}
  <h1 tabindex="-1">${v.top ? (mcat ? 'Next on the MCAT path' : `Next in ${esc(course!.t)}`) : `The end of ${esc(name)}`}</h1>
  <p class="cal-lede">${lede}</p>
  ${set}
</header>
${noteSlot(ui)}
<div class="cal-cols">
  <div class="cal-main">${main}${rows}</div>
  <div class="cal-side">${side}</div>
  <div class="cal-later">${whole}</div>
</div>
${keptLine(ui, 'this plan', ' Lessons you mark done go into your progress, which is saved to your account only if you are signed in.')}
</div>`;
}

/* ============================================================================
   Teacher: for my class (a sample; the real plan belongs inside a class)
   ============================================================================ */

const PER_WORDS: Record<string, string> = { '1': 'one lesson a meeting', '0.5': 'one lesson over two meetings', '2': 'two lessons a meeting' };
const classTime = (l: Lesson) => `About ${l.m} minutes${l.fc ? `, with ${l.fc === 1 ? 'one film' : `${num(l.fc)} films`} (${filmMin(l.fs)} min) inside it` : ''}`;
const breakSpan = (from: Iso, to: Iso) => (from === to ? monthDay(from) : `${monthDay(from)} to ${monthDay(to)}`);

function meetingRow(m: Meeting, today: Iso, print = false): string {
  const cls = m.date < today ? ' class="is-past"' : m.date === today ? ' class="is-today"' : '';
  const date = `<span class="cal-date">${shortDate(m.date)}${m.date === today ? ' <span class="cal-rel">Today</span>' : ''}</span>`;
  if (m.kind === 'open') return `<li${cls}>${date}<span class="cal-next-body"><span>Open day: nothing planned</span>${print ? '' : `<button type="button" class="cal-linkbtn cal-noprint" data-act="unlost" data-d="${m.date}" data-fid="unlost-${m.date}" aria-label="Put it back: ${shortDate(m.date)} holds its lesson again">Put it back</button>`}</span></li>`;
  const part = m.part ? ` <span class="cal-meta">(${m.part === 1 ? 'first' : 'second'} of two classes)</span>` : '';
  const titles = m.lessons.map((l, i) => (print ? esc(l.t) : `<a href="/lessons/${esc(l.s)}/"${i === 0 ? ` data-fid="row-${m.date}"` : ''}>${esc(l.t)}</a>`)).join(' <span class="cal-meta">and</span> ');
  const sol = m.lessons.map((l) => l.sol).filter(Boolean).join('; ');
  return `<li${cls}>${date}<span class="cal-next-body"><span>${titles}${part}</span><span class="cal-meta">${sol ? `SOL ${esc(sol)}` : 'No standard listed'}<span aria-hidden="true"> · </span>${m.lessons.reduce((a, l) => a + l.m, 0)} min</span></span></li>`;
}

export function renderTeacher(course: CourseData, choices: { s: string; t: string; level: string }[], plan: TeacherPlan | undefined, ui: Ui): string {
  const today = ui.today;
  const head = (inner: string) => `<header class="cal-top">
  ${roleRow('teacher')}
  <h1 tabindex="-1">A sample class plan, by date</h1>
  <p class="cal-lede cal-noprint">Try it with your own days. Nothing here is saved to a class or shown to students.</p>
  ${inner}
</header>`;
  const real = `<section class="cal-real cal-noprint" aria-labelledby="cal-real-h">
  <h2 id="cal-real-h">Where this is going</h2>
  <p>This page is a sample. The real plan belongs inside each class, as a “By date” tab beside Assign, so that five sections are five plans and the dates become the due dates your students see. That part is not built yet. Until it is, this page keeps whatever you set here on this device, and it prints.</p>
  <p><a href="/teach/">Classes on STEMhop</a> are free, students use nicknames only, and students never get email.</p>
</section>`;

  if (!today) {
    return `<div class="cal-page cal-teacher">${head(`<p class="cal-plan">${esc(course.t)}, one lesson a meeting.</p>`)}
<div class="cal-cols">
  <div class="cal-main"><section aria-labelledby="cal-order-h">
    <h2 id="cal-order-h">${esc(course.t)}, in order</h2>
    <noscript><p class="cal-sub">${NOSCRIPT}</p></noscript>
    ${course.units.map((u, i) => `<h3>Unit ${i + 1}: ${esc(u)}</h3><ol class="cal-next cal-meet">${course.lessons
      .filter((l) => l.u === i)
      .map((l) => `<li><span class="cal-next-body"><a href="/lessons/${esc(l.s)}/">${esc(l.t)}</a><span class="cal-meta">${l.sol ? `SOL ${esc(l.sol)}` : 'No standard listed'}<span aria-hidden="true"> · </span>${l.m} min</span></span></li>`)
      .join('')}</ol>`).join('')}
  </section></div>
  <div class="cal-side">${real}</div>
</div>
</div>`;
  }

  const s = teacherSetup(plan, today);
  const ms = meetings(course.lessons, s);
  const sentence = `${course.t}, ${PER_WORDS[String(s.per)]}, ${s.meet.length ? onDays(s.meet) : 'on no days yet'}, from ${monthDay(s.from)}.`;
  const groups = [...new Set(choices.map((c) => c.level))];
  const set = `<details class="cal-set cal-noprint" data-fold="set">
    <summary><span>${esc(sentence)}</span> <span class="cal-change cal-closed">Change</span><span class="cal-change cal-open">Close</span></summary>
    <div class="cal-set-body">
      <label class="cal-field"><span>Course</span><select name="tcourse">${groups.map((g) => `<optgroup label="${esc(g)}">${choices.filter((c) => c.level === g).map((c) => opt(c.s, c.t, c.s === course.s)).join('')}</optgroup>`).join('')}</select></label>
      <button type="button" class="cal-btn cal-go" data-act="go-course" data-fid="go-course">Show this course</button>
      <label class="cal-field"><span>First class</span><input type="date" name="tfrom" value="${s.from}"></label>
      <fieldset${ui.err?.at === 'meet' ? ' aria-describedby="cal-err"' : ''}><legend>The class meets on</legend>${dayChecks(s.meet, 'tmeet')}${ui.err?.at === 'meet' ? `<p class="cal-err" id="cal-err">${esc(ui.err.text)}</p>` : ''}</fieldset>
      <label class="cal-field"><span>Pace</span><select name="tper">${Object.entries(PER_WORDS).map(([k, w]) => opt(k, w, Number(k) === s.per)).join('')}</select></label>
      <fieldset class="cal-breaks-set"><legend>Days with no class</legend>
        ${plan?.breaks ? '' : '<p class="cal-sub">Sample breaks. Put in your school’s own.</p>'}
        ${s.breaks.length ? `<ul class="cal-breaks">${s.breaks.map((b, i) => `<li><span>${esc(breakSpan(b.from, b.to))}${b.label ? `: ${esc(b.label)}` : ''}</span> <button type="button" class="cal-linkbtn" data-act="unbreak" data-i="${i}" data-fid="unbreak-${i}" aria-label="Remove: ${esc(b.label || 'this break')}, ${esc(breakSpan(b.from, b.to))}">Remove</button></li>`).join('')}</ul>` : ''}
        <div class="cal-addbreak">
          <label class="cal-field"><span>From</span><input type="date" name="bfrom"${ui.err?.at === 'break-from' ? ' aria-invalid="true" aria-describedby="cal-err"' : ''}></label>
          <label class="cal-field"><span>To <span class="cal-opt">(optional)</span></span><input type="date" name="bto"${ui.err?.at === 'break-to' ? ' aria-invalid="true" aria-describedby="cal-err"' : ''}></label>
          <label class="cal-field"><span>What it is</span><input type="text" name="blabel" maxlength="60" autocomplete="off" aria-describedby="cal-blabel-hint"></label>
          <p class="cal-sub cal-wide" id="cal-blabel-hint">It stays on this computer and prints on the plan. Don’t use student names.</p>
          ${ui.err?.at === 'break-from' || ui.err?.at === 'break-to' ? `<p class="cal-err cal-wide" id="cal-err">${esc(ui.err.text)}</p>` : ''}
          <button type="button" class="cal-btn" data-act="addbreak" data-fid="addbreak">Add a break</button>
        </div>
      </fieldset>
    </div>
  </details>`;

  /* Today. */
  const m = ms.find((x) => x.date === today);
  const next = ms.find((x) => x.date > today && x.kind === 'lesson');
  const nextLine = next ? `Next class: ${longDate(next.date)}, ${esc(end(next.lessons.map((l) => l.t).join(' and ')))}` : '';
  let card: string;
  if (m?.kind === 'lesson') {
    const l = m.lessons[0];
    const two = m.lessons.length > 1;
    card = `<section class="cal-card cal-noprint" aria-labelledby="cal-today-t">
  <p class="cal-when"><time datetime="${today}">Today <span aria-hidden="true">·</span> ${longDate(today)}</time></p>
  <h2 class="cal-card-t" id="cal-today-t">${m.lessons.map((x) => `<a href="/lessons/${esc(x.s)}/">${esc(x.t)}</a>`).join(' <span class="cal-meta">and</span> ')}</h2>
  <p class="cal-hook">Unit ${l.u + 1}: ${esc(course.units[l.u] ?? '')}${m.part ? ` <span aria-hidden="true">·</span> ${m.part === 1 ? 'first' : 'second'} of two classes` : ''}</p>
  <dl class="cal-facts">
    <div><dt>Class time</dt><dd>${two ? m.lessons.map((x) => `${esc(x.t)}: ${classTime(x).toLowerCase()}`).join('. ') : classTime(l)}</dd></div>
    <div><dt>Standard</dt><dd>${m.lessons.map((x) => (x.sol ? `SOL ${esc(x.sol)}` : 'No standard listed')).join('; ')}</dd></div>
  </dl>
  <div class="cal-do cal-noprint">
    <a class="cal-btn cal-btn-main" href="/lessons/${esc(l.s)}/" data-fid="open">Open the lesson</a>
    <button type="button" class="cal-linkbtn" data-act="lost" data-fid="lost">Lost a day? Move today back one class</button>
  </div>
</section>`;
  } else if (m?.kind === 'open') {
    card = `<section class="cal-card cal-noprint" aria-labelledby="cal-today-t">
  <p class="cal-when"><time datetime="${today}">Today <span aria-hidden="true">·</span> ${longDate(today)}</time></p>
  <h2 class="cal-card-t" id="cal-today-t">An open day</h2>
  <p>Nothing is planned today. Every class after it moved back one. ${nextLine}</p>
  <div class="cal-do cal-noprint"><button type="button" class="cal-btn" data-act="unlost" data-d="${today}" data-fid="undo" aria-label="Put it back: today holds its lesson again">Put it back</button></div>
</section>`;
  } else {
    const b = s.breaks.find((x) => today >= x.from && today <= x.to);
    const first = ms[0];
    const last = ms[ms.length - 1];
    const why = !ms.length ? 'Tick at least one day the class meets, under Change, and the plan appears here.'
      : today < first.date ? `The plan starts on ${longDate(first.date)}.`
      : today > last.date ? `The plan ended on ${longDate(last.date)}. Set a new first class under Change to lay it out again.`
      : nextLine;
    card = `<section class="cal-card cal-noprint" aria-labelledby="cal-today-t">
  <p class="cal-when"><time datetime="${today}">Today <span aria-hidden="true">·</span> ${longDate(today)}</time></p>
  <h2 class="cal-card-t" id="cal-today-t">No class today${b?.label ? `: ${esc(b.label)}` : ''}</h2>
  <p>${why}</p>
</section>`;
  }

  /* By date: this week and three more on screen; the rest folded; all of it on paper. */
  const wk = weeks(ms, s);
  const thisMon = mondayOf(today);
  const weekHtml = (w: (typeof wk)[number], print = false) => `<li><h3 class="cal-wk-h">Week of ${monthDay(w.monday)}</h3>${
    w.breaks.map((b) => `<p class="cal-break">No class ${esc(spanWords(b.days))}${b.label ? `: ${esc(b.label)}` : ''}</p>`).join('')
  }${w.meetings.length ? `<ol class="cal-next cal-meet">${w.meetings.map((x) => meetingRow(x, today, print)).join('')}</ol>` : ''}</li>`;
  const shown = wk.filter((w) => w.monday >= thisMon && w.monday <= addDays(thisMon, 21));
  const rest = wk.filter((w) => w.monday > addDays(thisMon, 21));
  const earlier = wk.filter((w) => w.monday < thisMon);
  const lastDay = ms[ms.length - 1]?.date;
  const byDate = ms.length ? `<section class="cal-bydate" aria-labelledby="cal-bydate-h">
  <h2 id="cal-bydate-h">By date</h2>
  <ol class="cal-weeks cal-noprint">${shown.map((w) => weekHtml(w)).join('')}</ol>
  ${rest.length ? `<details class="cal-fold cal-noprint" data-fold="rest"><summary>The rest of the plan, to ${dateIn(lastDay!, today)}</summary><ol class="cal-weeks">${rest.map((w) => weekHtml(w)).join('')}</ol></details>` : ''}
  ${earlier.length ? `<details class="cal-fold cal-noprint" data-fold="earlier"><summary>Earlier weeks</summary><ol class="cal-weeks">${earlier.map((w) => weekHtml(w)).join('')}</ol></details>` : ''}
  <ol class="cal-weeks cal-print-only">${wk.map((w) => weekHtml(w, true)).join('')}</ol>
  <p class="cal-sub">${lastDay ? (lastDay > summerOf(s.from) ? `At this pace the plan runs into summer, to ${fullDate(lastDay)}. A quicker pace or another day a week, under Change, would bring it in.` : `On these days the last lesson lands on ${longDate(lastDay)}, ${lastDay.slice(0, 4)}.`) : ''}</p>
</section>` : '';

  return `<div class="cal-page cal-teacher">
${head(set)}
<p class="cal-print-only cal-print-head">${esc(course.t)}, by date. A sample plan: ${esc(PER_WORDS[String(s.per)])}, ${esc(daysPhrase(s.meet))}, from ${fullDate(s.from)}. Lessons are at stemhop.com/courses/${esc(course.s)}/</p>
${noteSlot(ui)}
<div class="cal-cols">
  <div class="cal-main">${card}${byDate}</div>
  <div class="cal-side">
    <section class="cal-keep cal-noprint" aria-labelledby="cal-keep-h">
      <h2 id="cal-keep-h">Take it with you</h2>
      <ul class="cal-keep-list"><li><button type="button" class="cal-btn" data-act="print" data-fid="print">Print the plan</button><span>Every class by date, with the standard each lesson serves, for a planning binder or the sub folder.</span></li></ul>
    </section>
    ${real}
  </div>
</div>
${keptLine(ui, 'what you set here')}
</div>`;
}

/* ---------- the opt-in email dialog (rendered only when flags.ts turns it on) ---------- */

export const emailDialog = () => `<dialog class="cal-dialog" id="cal-email" aria-labelledby="cal-email-h">
  <form method="dialog" data-email>
    <h2 id="cal-email-h" tabindex="-1">An email two days before</h2>
    <p>One short email before each activity day: what you are doing, how long it takes, what to gather, and the guide’s safety notes. Nothing on other days. After eight emails they stop by themselves, and you can ask again.</p>
    <label class="cal-field"><span>Your email address</span><input type="email" name="address" required autocomplete="email"></label>
    <fieldset class="cal-seg"><legend>When should it arrive?</legend>
      <label><input type="radio" name="when" value="2" checked><span>Two days before</span></label>
      <label><input type="radio" name="when" value="1"><span>The evening before</span></label>
    </fieldset>
    <label class="cal-check"><input type="checkbox" name="adult" required><span class="cal-box" aria-hidden="true"></span><span class="cal-line">I’m the grown-up here, 18 or over.</span></label>
    <p class="cal-sub">To send it, the site has to keep your address and this plan: which activities, on which day. Nothing about your child. Every email has a one-click stop, and stopping deletes it. No email carries a tracking pixel.</p>
    <p class="cal-email-said" role="status"></p>
    <div class="cal-dlg-do"><button type="button" class="cal-btn cal-btn-quiet" data-act="close">Not now</button><button type="submit" class="cal-btn cal-btn-main">Send me a link to confirm</button></div>
  </form>
</dialog>`;

export { DIAG_KEY };
