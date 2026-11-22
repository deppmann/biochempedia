/* =============================================================================
   The calendar's emails, as designs. NOTHING SENDS THESE. There is no sending
   code, no scheduler and no table in use; the only thing that calls these
   functions is the preview page (/calendar/email-preview/), at build time.

   They are written as plain functions (no page, no storage, no imports beyond
   the calendar's own types) so that the Worker can use the same ones when the
   site's owner has done the steps listed in migrations/0010_calendar_email.sql.

   Rules every design keeps:
   - it goes only to an adult who asked and then confirmed (a parent who ticked
     "18 or over", a teacher's confirmed address, or a signed-in learner, 13 and
     over); never to a student in a class, never to a child;
   - every link has words on it, and the plain-text version says the same thing;
   - one-click stop in every email, and stopping deletes the address;
   - a link that changes anything (move, stop, confirm) opens a page with one
     button; nothing acts when a mail scanner merely follows the link;
   - no tracking pixel and no tracked links;
   - it never says what was missed, and it ends by itself.
   Words taken from a guide (how long, your part, what to gather, the safety
   notes) are printed exactly as the guide has them.
   ============================================================================ */
import type { Activity, Lesson } from './engine';

export interface Mail { subject: string; preheader: string; html: string; text: string }

/** Where the links that change something lead. Each is a page with one button. */
export interface MailLinks { stop: string; move?: string; confirm?: string; plan: string }

const esc = (s: unknown) => String(s ?? '').replace(/[&<>"']/g, (c) => ({ '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#39;' })[c]!);
const WHERE = { indoors: 'Indoors', outdoors: 'Outdoors', either: 'Indoors or outdoors' } as const;
const clock = (sec: number) => `${Math.floor(sec / 60)}:${String(Math.round(sec) % 60).padStart(2, '0')}`;
const min = (sec: number) => Math.max(1, Math.round(sec / 60));

const INK = '#1B2A4A';
const SOFT = '#4a5568';
const TEAL = '#1f6b77';

const p = (html: string, style = '') => `<p style="margin:0 0 14px;line-height:1.55;${style}">${html}</p>`;
const h2 = (text: string) => `<h2 style="margin:26px 0 8px;font-size:17px;line-height:1.3;color:${INK};">${esc(text)}</h2>`;
const link = (href: string, text: string) => `<a href="${esc(href)}" style="color:${TEAL};font-weight:600;">${esc(text)}</a>`;
const button = (href: string, text: string) =>
  `<p style="margin:20px 0;"><a href="${esc(href)}" style="display:inline-block;background:${INK};color:#ffffff;font-weight:600;text-decoration:none;padding:12px 20px;border-radius:999px;">${esc(text)}</a></p>`;
const list = (items: string[]) => `<ul style="margin:0 0 14px;padding-left:20px;line-height:1.55;">${items.map((i) => `<li style="margin:0 0 6px;">${esc(i)}</li>`).join('')}</ul>`;

function page(m: { subject: string; preheader: string; body: string; foot: string[] }): string {
  return `<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<meta name="color-scheme" content="light dark">
<title>${esc(m.subject)}</title>
</head>
<body style="margin:0;padding:0;background:#f6f3ec;">
<div style="display:none;max-height:0;overflow:hidden;">${esc(m.preheader)}</div>
<div style="max-width:560px;margin:0 auto;padding:24px 20px 32px;font-family:-apple-system,BlinkMacSystemFont,'Segoe UI',Roboto,Helvetica,Arial,sans-serif;font-size:16px;color:#222222;background:#ffffff;">
<p style="margin:0 0 18px;font-size:14px;font-weight:700;letter-spacing:0.02em;color:${INK};">STEMhop</p>
${m.body}
<hr style="border:0;border-top:1px solid #dddddd;margin:28px 0 16px;">
${m.foot.map((f) => p(f, `font-size:14px;color:${SOFT};`)).join('\n')}
</div>
</body>
</html>`;
}

const FREE = 'STEMhop is free and has no ads. This email has no tracking pixel, and its links are not tracked.';

/* ---------- parent: two days before an activity day ---------- */

export interface ParentMail {
  origin: string;
  /** "Saturday" */
  day: string;
  act: Activity;
  /** This email's number and the last one: "email 4 of 8". */
  n: number; of: number;
  /** "November 1" */
  askedOn: string;
  links: MailLinks;
}

export function parentMail(m: ParentMail): Mail {
  const a = m.act;
  const guide = `${m.origin}/lessons/${a.s}/`;
  const subject = `${m.day}: ${a.t} (about ${a.min} minutes)`;
  const n = a.materials.length;
  const preheader = `${n === 1 ? 'One thing' : `${n} things`} to gather, and the guide’s safety notes.`;
  const long = `About ${a.min} minutes${a.follow ? `, ${a.follow}` : ''}. ${WHERE[a.setting]}. Ages 5 to 10.`;
  const count = `This is email ${m.n} of ${m.of}. After email ${m.of} they stop by themselves.`;
  const body = [
    `<h1 style="margin:0 0 10px;font-size:26px;line-height:1.2;color:${INK};">${esc(m.day)}: ${esc(a.t)}</h1>`,
    p(esc(a.hook), `color:${SOFT};`),
    p(esc(long)),
    p(`<strong>Your part.</strong> ${esc(a.adult)}`),
    button(guide, `Open the guide: ${a.t}`),
    h2('What to gather'),
    list(a.materials),
    h2('Safety, from the guide'),
    list(a.safety),
    p([a.film ? link(a.film.href.startsWith('http') ? a.film.href : m.origin + a.film.href, `Watch the setup film (${clock(a.film.sec)})`) : '', link(m.links.plan, 'See it on the calendar, and print the sheet')].filter(Boolean).join(' &nbsp;·&nbsp; ')),
    m.links.move ? p(`Not this week? ${link(m.links.move, 'Move it to next week')}, and this same activity comes again then. Nothing else changes.`) : '',
  ].join('\n');
  const foot = [
    esc(count),
    `You asked for these at stemhop.com on ${esc(m.askedOn)}. They go to this address and nobody else. ${link(m.links.stop, 'Stop these emails')}: one click, no sign-in. Stopping deletes your address and the plan kept with it.`,
    FREE,
  ];
  const text = [
    `${m.day}: ${a.t}`, '', a.hook, '', long, `Your part. ${a.adult}`, '', `Open the guide: ${guide}`, '',
    'WHAT TO GATHER', ...a.materials.map((x) => `- ${x}`), '',
    'SAFETY, FROM THE GUIDE', ...a.safety.map((x) => `- ${x}`), '',
    ...(a.film ? [`Watch the setup film (${clock(a.film.sec)}): ${a.film.href.startsWith('http') ? a.film.href : m.origin + a.film.href}`] : []),
    `See it on the calendar, and print the sheet: ${m.links.plan}`, '',
    ...(m.links.move ? [`Not this week? Move it to next week, and this same activity comes again then. Nothing else changes: ${m.links.move}`, ''] : []),
    '--', count,
    `You asked for these at stemhop.com on ${m.askedOn}. They go to this address and nobody else.`,
    `Stop these emails (one click, no sign-in; stopping deletes your address and the plan kept with it): ${m.links.stop}`,
    FREE,
  ].join('\n');
  return { subject, preheader, html: page({ subject, preheader, body, foot }), text };
}

/* ---------- the confirming email (double opt-in): the only one sent before a yes ---------- */

export function confirmMail(m: { origin: string; of: number; links: MailLinks }): Mail {
  const subject = 'Confirm: one email before each activity day';
  const preheader = 'One click, or do nothing and no more email comes.';
  const ask = `Someone, probably you, asked STEMhop to send this address one short email before each Biology Together activity day: the activity, what to gather for it, and the guide’s safety notes. ${m.of} emails, and then they stop by themselves.`;
  const not = 'If that was not you, do nothing. No more email will come, and this address is deleted after a day.';
  const kept = 'What is kept if you say yes: this address, and the plan (which activities, on which day). Nothing about a child. Every email has a one-click stop, and stopping deletes both.';
  const only = 'STEMhop is a free site for learning science. This is the only email you will get unless you press the button.';
  const body = [`<h1 style="margin:0 0 10px;font-size:26px;line-height:1.2;color:${INK};">One click to confirm</h1>`, p(esc(ask)), button(m.links.confirm ?? '#', 'Yes, send them'), p(esc(not)), p(esc(kept))].join('\n');
  const text = ['One click to confirm', '', ask, '', `Yes, send them: ${m.links.confirm ?? ''}`, '', not, '', kept, '', '--', only].join('\n');
  return { subject, preheader, html: page({ subject, preheader, body, foot: [esc(only)] }), text };
}

/* ---------- learner: signed in, 13 and over, on a study day (a later wave) ---------- */

export interface LearnerMail {
  origin: string;
  /** "Monday" */
  day: string;
  course: string;
  lesson: Lesson;
  school: boolean;
  then?: string; after?: string;
  /** "week 3" of at most eight. */
  week: number;
  links: MailLinks;
}

export function learnerMail(m: LearnerMail): Mail {
  const l = m.lesson;
  const film = l.fs ? min(l.fs) : 0;
  const total = m.school ? l.m : l.m + film;
  const size = m.school
    ? `One class period, about ${l.m} minutes${film ? `, with ${film} ${film === 1 ? 'minute' : 'minutes'} of film` : ''}.`
    : film ? `About ${total} minutes: ${l.m} to read, ${film} of film.` : `About ${l.m} minutes to read.`;
  const href = `${m.origin}/lessons/${l.s}/`;
  const subject = `Next in ${m.course}: ${l.t} (about ${total} minutes)`;
  const preheader = `${m.day}, if you want it. ${size}`;
  const next = [m.then ? `Then: ${m.then}.` : '', m.after ? `After that: ${m.after}.` : ''].filter(Boolean).join(' ');
  const calm = 'Did this one already, or not today? There is nothing to do. The next email starts from wherever you are.';
  const ends = `These stop by themselves when the course ends or after eight weeks, whichever comes first. This is week ${m.week}.`;
  const who = 'You asked for these from your STEMhop account. Accounts are for people 13 and over. The address is used for nothing else.';
  const body = [
    p(`${esc(m.day)}, if you want it <span style="color:${SOFT};">· ${esc(m.course)}, lesson ${l.n}</span>`, 'font-size:14px;font-weight:600;'),
    `<h1 style="margin:0 0 10px;font-size:26px;line-height:1.2;color:${INK};">${esc(l.t)}</h1>`,
    l.hook ? p(esc(l.hook), `color:${SOFT};`) : '',
    p(esc(size)),
    button(href, `Open the lesson: ${l.t}`),
    l.watch && film ? p(link(m.origin + l.watch, `Watch the ${l.fc > 1 ? 'films' : 'film'} first (${film} min)`)) : '',
    l.down ? p(`The same idea, told more simply, if you want it first: ${link(`${m.origin}/lessons/${l.down.s}/`, l.down.t)} (${esc(l.down.level)}).`) : '',
    next ? p(esc(next), `color:${SOFT};`) : '',
    p(esc(calm)),
  ].join('\n');
  const foot = [esc(ends), `${link(m.links.plan, 'Change the days')} &nbsp;·&nbsp; ${link(m.links.stop, 'Stop these emails')}: one click, no questions.`, esc(who), FREE];
  const text = [
    `${m.day}, if you want it. ${m.course}, lesson ${l.n}`, '', l.t, ...(l.hook ? [l.hook] : []), '', size, '', `Open the lesson: ${href}`,
    ...(l.watch && film ? [`Watch the ${l.fc > 1 ? 'films' : 'film'} first (${film} min): ${m.origin + l.watch}`] : []),
    ...(l.down ? [`The same idea, told more simply, if you want it first: ${l.down.t} (${l.down.level}): ${m.origin}/lessons/${l.down.s}/`] : []),
    ...(next ? ['', next] : []), '', calm, '', '--', ends, `Change the days: ${m.links.plan}`, `Stop these emails (one click, no questions): ${m.links.stop}`, who, FREE,
  ].join('\n');
  return { subject, preheader, html: page({ subject, preheader, body, foot }), text };
}

/* ---------- teacher: each class morning (with the real class plan, a later step) ---------- */

export interface TeacherMail {
  origin: string;
  className: string;
  /** "Friday" and "Friday, November 20" */
  day: string; date: string;
  unit: string;
  lesson: Lesson;
  /** The projector view for this class and lesson. */
  room: string;
  /** "Monday, November 23, The Cell Cycle and Mitosis" */
  next?: string;
  /** "Wednesday, February 3" */
  ends: string;
  links: MailLinks;
}

export function teacherMail(m: TeacherMail): Mail {
  const l = m.lesson;
  const href = `${m.origin}/lessons/${l.s}/`;
  const subject = `${m.className}, ${m.day}: ${l.t}`;
  const facts = `${m.unit}. About ${l.m} minutes${l.fc ? `, with ${l.fc === 1 ? 'one film' : `${l.fc} films`} (${min(l.fs)} min) inside it` : ''}.${l.sol ? ` SOL ${l.sol}.` : ''}`;
  const preheader = facts;
  const lost = 'and the next email will say what is on. Your students’ due dates move with it.';
  const ends = `These end with the plan, on ${m.ends}. Students never get email from STEMhop.`;
  const who = 'Sent to the address on your teacher account because you asked for it on the class plan.';
  const body = [
    p(`${esc(m.className)} <span style="color:${SOFT};">· ${esc(m.date)}</span>`, 'font-size:14px;font-weight:600;'),
    `<h1 style="margin:0 0 10px;font-size:26px;line-height:1.2;color:${INK};">${esc(l.t)}</h1>`,
    p(esc(facts)),
    button(href, `Open the lesson: ${l.t}`),
    p(link(m.room, 'Room view, for the projector')),
    m.next ? p(`Next class: ${esc(/[.?!]$/.test(m.next) ? m.next : `${m.next}.`)}`, `color:${SOFT};`) : '',
    m.links.move ? p(`Lost a day? ${link(m.links.move, 'Move today back one class')}, ${esc(lost)}`) : '',
  ].join('\n');
  const foot = [esc(ends), `${link(m.links.plan, 'Open the class plan')} &nbsp;·&nbsp; ${link(m.links.stop, 'Stop these emails')}: one click, no questions.`, esc(who), FREE];
  const text = [
    `${m.className}. ${m.date}`, '', l.t, facts, '', `Open the lesson: ${href}`, `Room view, for the projector: ${m.room}`,
    ...(m.next ? ['', `Next class: ${/[.?!]$/.test(m.next) ? m.next : `${m.next}.`}`] : []),
    ...(m.links.move ? ['', `Lost a day? Move today back one class, ${lost} ${m.links.move}`] : []),
    '', '--', ends, `Open the class plan: ${m.links.plan}`, `Stop these emails (one click, no questions): ${m.links.stop}`, who, FREE,
  ].join('\n');
  return { subject, preheader, html: page({ subject, preheader, body, foot }), text };
}
