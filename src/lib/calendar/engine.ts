/* =============================================================================
   The calendar's arithmetic. Pure: no page, no storage, no network, no imports,
   so scripts/test-calendar.mjs can run every rule here under Node.

   The one rule everything else follows from: a parent's or a learner's plan
   stores NO date. It stores an order (a queue) and a rhythm (which weekdays).
   Every date on the page is worked out again from today each time the page is
   drawn, so a day that goes by leaves no gap and no mark, and nothing can be
   late. A class meets on real days, so only the teacher's plan keeps dates.

   Dates are calendar days as 'YYYY-MM-DD' strings. All arithmetic is done on
   whole days in UTC, so a daylight-saving change can never move or repeat one.
   ============================================================================ */

export type Iso = string;

/* ---------- dates ---------- */

const pad = (n: number) => String(n).padStart(2, '0');
const DAY = 86_400_000;
const utc = (s: Iso) => { const [y, m, d] = s.split('-').map(Number); return Date.UTC(y, m - 1, d); };
const fromUtc = (ms: number) => { const d = new Date(ms); return `${d.getUTCFullYear()}-${pad(d.getUTCMonth() + 1)}-${pad(d.getUTCDate())}`; };

export const isIso = (s: unknown): s is Iso => typeof s === 'string' && /^\d{4}-\d{2}-\d{2}$/.test(s) && fromUtc(utc(s)) === s;
export const addDays = (s: Iso, n: number): Iso => fromUtc(utc(s) + n * DAY);
/** 0 = Sunday. */
export const dow = (s: Iso) => new Date(utc(s)).getUTCDay();
export const daysBetween = (a: Iso, b: Iso) => Math.round((utc(b) - utc(a)) / DAY);
export const mondayOf = (s: Iso) => addDays(s, -((dow(s) + 6) % 7));

/** The calendar day it is for the person looking: their own zone, or a named one. */
export function todayIso(now: Date = new Date(), timeZone?: string): Iso {
  if (!timeZone) return `${now.getFullYear()}-${pad(now.getMonth() + 1)}-${pad(now.getDate())}`;
  const parts = new Intl.DateTimeFormat('en-US', { timeZone, year: 'numeric', month: '2-digit', day: '2-digit' }).formatToParts(now);
  const get = (t: string) => parts.find((p) => p.type === t)?.value ?? '';
  return `${get('year')}-${get('month')}-${get('day')}`;
}

export const WD = ['Sunday', 'Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday'];
export const MON = ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December'];
/** Monday first, the order the day boxes are shown in. */
export const WEEK_ORDER = [1, 2, 3, 4, 5, 6, 0];

const parts = (s: Iso) => { const d = new Date(utc(s)); return { wd: d.getUTCDay(), m: d.getUTCMonth(), d: d.getUTCDate(), y: d.getUTCFullYear() }; };
/** "Saturday, November 21" */
export const longDate = (s: Iso) => { const p = parts(s); return `${WD[p.wd]}, ${MON[p.m]} ${p.d}`; };
/** "November 21" */
export const monthDay = (s: Iso) => { const p = parts(s); return `${MON[p.m]} ${p.d}`; };
/** "Sat, Nov 21" */
export const shortDate = (s: Iso) => { const p = parts(s); return `${WD[p.wd].slice(0, 3)}, ${MON[p.m].slice(0, 3)} ${p.d}`; };
/** "May 14, 2027" */
export const fullDate = (s: Iso) => { const p = parts(s); return `${MON[p.m]} ${p.d}, ${p.y}`; };
export const weekday = (s: Iso) => WD[dow(s)];

const cleanDays = (days: number[]) => [...new Set(days.filter((d) => Number.isInteger(d) && d >= 0 && d <= 6))].sort((a, b) => WEEK_ORDER.indexOf(a) - WEEK_ORDER.indexOf(b));

/** "Saturdays", "Mondays, Wednesdays and Fridays", "Monday to Friday", "every day" */
export function daysPhrase(days: number[]): string {
  const d = cleanDays(days);
  if (d.length === 7) return 'every day';
  if (d.length === 5 && [1, 2, 3, 4, 5].every((x) => d.includes(x))) return 'Monday to Friday';
  const names = d.map((x) => WD[x] + 's');
  if (names.length <= 1) return names[0] ?? '';
  return names.slice(0, -1).join(', ') + ' and ' + names[names.length - 1];
}

/** In a sentence: "on Saturdays", "Monday to Friday", "every day". */
export function onDays(days: number[]): string {
  const p = daysPhrase(days);
  return /s$/.test(p) ? `on ${p}` : p;
}

/** The first `n` days on those weekdays, from `from` on (inclusive). */
export function rhythmDays(days: number[], from: Iso, n: number): Iso[] {
  const d = cleanDays(days);
  const out: Iso[] = [];
  if (!d.length) return out;
  for (let i = 0; out.length < n && i < n * 7 + 7; i++) {
    const x = addDays(from, i);
    if (d.includes(dow(x))) out.push(x);
  }
  return out;
}

const NUM = ['no', 'one', 'two', 'three', 'four', 'five', 'six', 'seven', 'eight', 'nine', 'ten', 'eleven', 'twelve'];
export const num = (n: number) => NUM[n] ?? String(n);
export const cap = (s: string) => (s ? s[0].toUpperCase() + s.slice(1) : s);
/** 66 -> "1:06" */
export const clock = (sec: number) => { const s = Math.round(sec); return `${Math.floor(s / 60)}:${pad(s % 60)}`; };
export const filmMin = (sec: number) => (sec > 0 ? Math.max(1, Math.round(sec / 60)) : 0);

/* ---------- what the pages are built from (written when the site is built) ---------- */

export interface Activity {
  s: string; t: string; hook: string; unit: string; u: number;
  /** Hands-on minutes, the guide's own figure. */
  min: number;
  /** The guide's follow-up line, word for word. */
  follow?: string;
  setting: 'indoors' | 'outdoors' | 'either';
  /** The guide's line for the grown-up, word for word. */
  adult: string;
  /** What to gather, each line word for word, in the guide's order. */
  materials: string[];
  /** The guide's safety notes, each one word for word. */
  safety: string[];
  poster?: string;
  film?: { sec: number; href: string };
}

export interface Lesson {
  s: string; t: string;
  /** Unit index and the lesson's number in its course. */
  u: number; n: number;
  /** Minutes to read, or the class period for a school lesson. */
  m: number;
  /** Film seconds (every chapter) and how many films. */
  fs: number; fc: number;
  watch?: string;
  hook?: string;
  /** Standards codes, as the lesson gives them. */
  sol?: string;
  /** An authored lower rung: the same idea one level down. */
  down?: { s: string; t: string; level: string };
}

export interface CourseData { s: string; t: string; level: string; school: boolean; units: string[]; lessons: Lesson[] }
export interface McatStep { s: string; t: string; why: string; optional: boolean; lessons: Lesson[] }
export interface McatSet { id: string; title: string; lessons: string[] }
export interface McatData { steps: McatStep[]; sets: McatSet[]; scope: string; links: { label: string; href: string }[]; diagnostic: number }

/* ---------- what is kept on the device: `stemhop:calendar:v1` ---------- */

export interface ParentPlan {
  /** The weekdays that suit. Absent = Saturdays (the starting suggestion); [] = no set day. */
  days?: number[];
  /** Activities the family moved to the front, in their order. The rest follow in course order. */
  order: string[];
  /** Activities done together, oldest first. No dates. */
  done: string[];
  /** Ticked supply lines, by a hash of the line. */
  have: Record<string, 1>;
  /** How many coming activities the gather list covers. */
  list?: 1 | 2 | 3;
}
export interface StudentPlan {
  /** A course slug, or 'mcat'. */
  plan?: string;
  /** The weekdays the person studies. [] = no set days, so nothing is dated. */
  days: number[];
  /** Where to start in a course: course slug -> lesson slug. */
  start: Record<string, string>;
  /** MCAT: minutes in a sitting. 0 = one lesson at a time. */
  sit: number;
  /** MCAT: courses left out, and optional courses put in. */
  out: string[];
  opt: string[];
  /** Things marked done here that are not lessons (the diagnostic, passage sets). */
  marks: string[];
}
export interface Break { from: Iso; to: Iso; label: string }
/** The teacher's sample. A class meets on real days, so this is the one plan that keeps dates. */
export interface TeacherPlan {
  course?: string;
  from?: Iso;
  meet?: number[];
  /** 1 = one lesson a meeting, 2 = two lessons a meeting, 0.5 = one lesson over two meetings. */
  per?: number;
  breaks?: Break[];
  /** Days turned into open days by "Move today back one class". */
  moved: Iso[];
}
export interface CalState { v: 1; parent?: ParentPlan; student?: StudentPlan; teacher?: TeacherPlan }

export const newParent = (): ParentPlan => ({ order: [], done: [], have: {} });
export const newStudent = (): StudentPlan => ({ days: [], start: {}, sit: 0, out: [], opt: [], marks: [] });
export const newTeacher = (): TeacherPlan => ({ moved: [] });

const SLUG = /^[a-z0-9][a-z0-9:-]{0,79}$/;
/** A lesson, course or item name: letters, digits and hyphens, and never anything shaped like a date. */
const isSlug = (s: unknown): s is string => typeof s === 'string' && SLUG.test(s) && !/\d{4}-\d|\d{8}/.test(s);
const slugs = (x: unknown, max = 400): string[] => (Array.isArray(x) ? [...new Set(x.filter(isSlug))].slice(0, max) : []);
const dayList = (x: unknown): number[] => (Array.isArray(x) ? cleanDays(x as number[]) : []);
export const SIT_SIZES = [0, 60, 90, 120, 180];
export const PER_CHOICES = [1, 0.5, 2];

/** Whatever was read from storage, made safe: unknown fields dropped, every value checked. */
export function cleanState(raw: unknown): CalState {
  const o = (raw && typeof raw === 'object' ? raw : {}) as Record<string, any>;
  const out: CalState = { v: 1 };
  const p = o.parent;
  if (p && typeof p === 'object') {
    const have: Record<string, 1> = {};
    if (p.have && typeof p.have === 'object') for (const k of Object.keys(p.have).slice(0, 600)) if (/^[a-z0-9]{1,12}$/.test(k)) have[k] = 1;
    out.parent = { order: slugs(p.order), done: slugs(p.done), have };
    if (Array.isArray(p.days)) out.parent.days = dayList(p.days);
    if (p.list === 2 || p.list === 3) out.parent.list = p.list;
  }
  const s = o.student;
  if (s && typeof s === 'object') {
    const start: Record<string, string> = {};
    if (s.start && typeof s.start === 'object') for (const [k, v] of Object.entries(s.start).slice(0, 40)) if (isSlug(k) && isSlug(v)) start[k] = v;
    out.student = { days: dayList(s.days), start, sit: SIT_SIZES.includes(s.sit) ? s.sit : 0, out: slugs(s.out, 20), opt: slugs(s.opt, 20), marks: slugs(s.marks) };
    if (isSlug(s.plan)) out.student.plan = s.plan;
  }
  const t = o.teacher;
  if (t && typeof t === 'object') {
    out.teacher = { moved: Array.isArray(t.moved) ? [...new Set((t.moved as unknown[]).filter(isIso))].sort().slice(0, 200) : [] };
    if (isSlug(t.course)) out.teacher.course = t.course;
    if (isIso(t.from)) out.teacher.from = t.from;
    if (Array.isArray(t.meet) && dayList(t.meet).length) out.teacher.meet = dayList(t.meet);
    if (PER_CHOICES.includes(t.per)) out.teacher.per = t.per;
    if (Array.isArray(t.breaks)) {
      out.teacher.breaks = (t.breaks as any[])
        .filter((b) => b && isIso(b.from) && isIso(b.to) && b.to >= b.from)
        .slice(0, 60)
        .map((b) => ({ from: b.from, to: b.to, label: String(b.label ?? '').replace(/[<>]/g, '').slice(0, 60) }))
        .sort((a, b) => a.from.localeCompare(b.from));
    }
  }
  return out;
}

/** True if a stored value holds anything that could be a date: a day string, a time string, or a
 *  number big enough to be a timestamp or a day count. The tests run this over every parent and
 *  student plan the page can save. */
export function holdsDate(x: unknown): boolean {
  if (typeof x === 'string') return /\d{4}-\d{1,2}-\d{1,2}|\d{1,2}\/\d{1,2}\/\d{2,4}|\d{8}|T\d{2}:\d{2}/.test(x);
  if (typeof x === 'number') return Math.abs(x) >= 1000;
  if (Array.isArray(x)) return x.some(holdsDate);
  if (x && typeof x === 'object') return Object.entries(x).some(([k, v]) => holdsDate(k) || holdsDate(v));
  return false;
}

/* ---------- parent: a queue of activities and a rhythm ---------- */

export const PARENT_DEFAULT_DAYS = [6];
export const parentDays = (p: ParentPlan) => p.days ?? PARENT_DEFAULT_DAYS;

/** The activities still to do: the family's own picks first, then the course's order. */
export function parentQueue(acts: Activity[], plan: ParentPlan): Activity[] {
  const by = new Map(acts.map((a) => [a.s, a]));
  const own = plan.order.filter((s) => by.has(s) && !plan.done.includes(s));
  return [...own.map((s) => by.get(s)!), ...acts.filter((a) => !own.includes(a.s) && !plan.done.includes(a.s))];
}

export interface ParentView {
  days: number[];
  /** The day the first card is for. Absent when no day is set. */
  date?: Iso;
  /** A day left open by "Not this week" (this visit only). */
  freed?: Iso;
  next?: Activity;
  after: { act: Activity; date?: Iso }[];
  /** Coming dates are shown only when the family picked the days themselves. */
  datedAfter: boolean;
  done: Activity[];
  queue: Activity[];
}

/** `skip` is "Not this week": it lives for this visit only and is never stored. */
export function parentView(acts: Activity[], plan: ParentPlan, today: Iso, opts: { skip?: boolean } = {}): ParentView {
  const days = parentDays(plan);
  const queue = parentQueue(acts, plan);
  const slots = rhythmDays(days, today, 6 + (opts.skip ? 1 : 0));
  const freed = opts.skip && slots.length ? slots.shift() : undefined;
  const by = new Map(acts.map((a) => [a.s, a]));
  const datedAfter = plan.days !== undefined && days.length > 0;
  return {
    days, freed, queue, datedAfter,
    date: slots[0],
    next: queue[0],
    after: queue.slice(1, 5).map((act, i) => ({ act, date: datedAfter ? slots[i + 1] : undefined })),
    done: plan.done.map((s) => by.get(s)).filter((a): a is Activity => !!a),
  };
}

/** A short stable key for a supply line, so the same words tick once. */
export function lineKey(text: string): string {
  let h = 2166136261;
  const s = text.toLowerCase().replace(/\s+/g, ' ').trim();
  for (let i = 0; i < s.length; i++) { h ^= s.charCodeAt(i); h = Math.imul(h, 16777619); }
  return (h >>> 0).toString(36);
}

export interface GatherLine { key: string; text: string; for: Activity[] }
/** One list for the coming activities: every line word for word, in each guide's own order.
 *  Nothing is grouped or reworded; a line two guides write identically appears once. */
export function gather(acts: Activity[]): GatherLine[] {
  const lines = new Map<string, GatherLine>();
  for (const a of acts) for (const text of a.materials) {
    const key = lineKey(text);
    const have = lines.get(key);
    if (have) { if (!have.for.includes(a)) have.for.push(a); } else lines.set(key, { key, text, for: [a] });
  }
  return [...lines.values()];
}

export function parentDid(plan: ParentPlan, act: Activity): ParentPlan {
  const have = { ...plan.have };
  for (const m of act.materials) delete have[lineKey(m)];
  return { ...plan, done: [...plan.done.filter((s) => s !== act.s), act.s], order: plan.order.filter((s) => s !== act.s), have };
}
export const parentUndid = (plan: ParentPlan, slug: string): ParentPlan => ({ ...plan, done: plan.done.filter((s) => s !== slug) });
/** "Choose a different one": the pick comes next; the one it replaces follows it. */
export function parentPick(acts: Activity[], plan: ParentPlan, slug: string): ParentPlan {
  const without = { ...plan, done: plan.done.filter((s) => s !== slug) };
  const head = parentQueue(acts, without)[0];
  const order = [slug, ...(head && head.s !== slug ? [head.s] : []), ...plan.order.filter((s) => s !== slug && s !== head?.s)];
  return { ...without, order };
}

/* ---------- student: a course in order, or the MCAT path ---------- */

export interface Item {
  key: string;
  kind: 'lesson' | 'set' | 'diag';
  t: string;
  href: string;
  /** Reading minutes (or the class period), film seconds, film count. */
  read: number; filmSec: number; films: number;
  watch?: string;
  school: boolean;
  hook?: string;
  /** "Physiology, lesson 8" */
  where: string;
  /** Sittings never straddle two groups (courses on the MCAT path). */
  group: string;
  unit: string;
  down?: Lesson['down'];
}

/** Honest minutes for one thing. A school lesson's films play inside its class period. */
export const itemMinutes = (it: Item) => (it.school ? it.read : it.read + filmMin(it.filmSec));

export function courseItems(c: CourseData, from?: string): Item[] {
  let lessons = c.lessons;
  const at = from ? lessons.findIndex((l) => l.s === from) : -1;
  if (at > 0) lessons = lessons.slice(at);
  return lessons.map((l) => lessonItem(l, c.t, c.school, c.s, c.units[l.u] ?? ''));
}
const lessonItem = (l: Lesson, course: string, school: boolean, group: string, unit: string): Item => ({
  key: l.s, kind: 'lesson', t: l.t, href: `/lessons/${l.s}/`, read: l.m, filmSec: l.fs, films: l.fc, watch: l.watch,
  school, hook: l.hook, where: `${course}, lesson ${l.n}`, group, unit, down: l.down,
});

export const DIAG_KEY = 'mcat:diagnostic';
export const setKey = (id: string) => `mcat:set:${id}`;

/** Which courses of the path are in the plan: required ones unless left out, optional ones if put in. */
export const mcatIncluded = (m: McatData, plan: Pick<StudentPlan, 'out' | 'opt'>) =>
  m.steps.filter((s) => (s.optional ? plan.opt.includes(s.s) : !plan.out.includes(s.s)));

/** The MCAT path, laid end to end from what is built: the diagnostic, then each course in the
 *  path's order, with each passage set placed after the last lesson in the plan that it draws on. */
export function mcatItems(m: McatData, plan: Pick<StudentPlan, 'out' | 'opt'>): Item[] {
  const steps = mcatIncluded(m, plan);
  const order = steps.flatMap((s) => s.lessons.map((l) => l.s));
  const after = new Map<string, McatSet[]>();
  for (const set of m.sets) {
    const at = Math.max(...set.lessons.map((s) => order.indexOf(s)));
    if (at < 0) continue;
    after.set(order[at], [...(after.get(order[at]) ?? []), set]);
  }
  const items: Item[] = [{
    key: DIAG_KEY, kind: 'diag', t: `The diagnostic: ${m.diagnostic} questions`, href: '/mcat/diagnostic/', read: 30, filmSec: 0, films: 0,
    school: false, hook: 'A practice check, not a predictor of your score. It shows which topics to give more room.', where: 'Start here', group: 'start', unit: 'Start here',
  }];
  for (const st of steps) for (const l of st.lessons) {
    items.push({ ...lessonItem(l, st.t, false, st.s, st.t), down: undefined });
    for (const set of after.get(l.s) ?? []) {
      items.push({ key: setKey(set.id), kind: 'set', t: `Passage practice: ${set.title}`, href: `/mcat/${set.id}/`, read: 8, filmSec: 0, films: 0, school: false, where: `${st.t}, a passage with data`, group: st.s, unit: st.t });
    }
  }
  return items;
}

export interface Sitting { items: Item[]; min: number; read: number; film: number }
const sittingOf = (items: Item[]): Sitting => ({
  items,
  min: items.reduce((a, i) => a + itemMinutes(i), 0),
  read: items.reduce((a, i) => a + i.read, 0),
  film: items.reduce((a, i) => a + filmMin(i.filmSec), 0),
});

/** Pack what is open into sittings of about `size` minutes, in order. size 0 = one thing at a time.
 *  A sitting never straddles two courses, and the diagnostic sits alone. */
export function sittings(open: Item[], size: number): Sitting[] {
  const out: Sitting[] = [];
  let cur: Item[] = [];
  let used = 0;
  const flush = () => { if (cur.length) out.push(sittingOf(cur)); cur = []; used = 0; };
  for (const it of open) {
    const m = itemMinutes(it);
    const fits = size > 0 && cur.length > 0 && cur[0].group === it.group && it.kind !== 'diag' && used + m <= size * 1.15;
    if (!fits) flush();
    cur.push(it); used += m;
    if (size <= 0 || it.kind === 'diag') flush();
  }
  flush();
  return out;
}

export interface StudentView {
  dated: boolean;
  /** The first card, and the day it sits on when days are set. */
  top?: { sitting: Sitting; date?: Iso };
  /** Then, After that. */
  rows: { sitting: Sitting; date?: Iso }[];
  /** Today, left open by "Later" (this visit only). */
  emptied?: Iso;
  /** Today already holds something done, so the next thing sits on the next day. */
  spent: boolean;
  all: Sitting[];
}

/**
 * Lay what is open on the person's days, from today on. Nothing is ever placed before today.
 * `later`: today was moved along with "Later" (this visit only, never stored).
 * `spent`: something in this plan was already done today, so today is used.
 */
export function studentView(items: Item[], done: ReadonlySet<string>, plan: { days: number[]; sit?: number }, today: Iso, opts: { later?: boolean; spent?: boolean } = {}): StudentView {
  const all = sittings(items.filter((i) => !done.has(i.key)), plan.sit ?? 0);
  const days = cleanDays(plan.days);
  const dated = days.length > 0;
  let slots: Iso[] = [];
  let emptied: Iso | undefined;
  let spent = false;
  if (dated) {
    slots = rhythmDays(days, today, 4);
    if (slots[0] === today && (opts.later || opts.spent)) {
      if (opts.later) emptied = today; else spent = true;
      slots.shift();
    }
  }
  const at = (i: number) => (all[i] ? { sitting: all[i], date: dated ? slots[i] : undefined } : undefined);
  return { dated, top: at(0), rows: [at(1), at(2)].filter((x): x is { sitting: Sitting; date: Iso | undefined } => !!x), emptied, spent, all };
}

export interface Reach {
  kind: 'none' | 'no-days' | 'passed' | 'fits' | 'close' | 'beyond' | 'far-beyond';
  /** The day the last sitting lands on at this rhythm. */
  end?: Iso;
  /** Whole weeks between that day and the test, when it fits. */
  spare?: number;
  /** Whole weeks the lessons run past the test. */
  over?: number;
  hoursNow?: number;
  hoursNeeded?: number;
}

/** Does this rhythm reach a test date? Arithmetic only: the sittings laid on the person's days
 *  from today. It never says "ready", and it is worked out only when a date is given. */
export function reach(all: Sitting[], days: number[], today: Iso, test: Iso | undefined, skipToday = false): Reach {
  if (!test || !isIso(test)) return { kind: 'none' };
  if (test <= today) return { kind: 'passed' };
  const d = cleanDays(days);
  if (!d.length) return { kind: 'no-days' };
  if (!all.length) return { kind: 'fits', end: today, spare: Math.floor(daysBetween(today, test) / 7) };
  const first = skipToday ? addDays(today, 1) : today;
  // The n-th study day from `first`, without walking every day.
  const lead = rhythmDays(d, first, d.length);
  const n = all.length - 1;
  const end = addDays(lead[n % d.length], Math.floor(n / d.length) * 7);
  if (end <= test) {
    const spare = Math.floor(daysBetween(end, test) / 7);
    return { kind: spare >= 2 ? 'fits' : 'close', end, spare };
  }
  const total = all.reduce((a, s) => a + s.min, 0);
  const hoursNow = Math.max(1, Math.round((total / all.length) * d.length / 60));
  const weeks = daysBetween(today, test) / 7;
  const hoursNeeded = Math.ceil(total / 60 / weeks);
  const over = Math.max(1, Math.ceil(daysBetween(test, end) / 7));
  if (weeks < 1 || hoursNeeded > 40) return { kind: 'far-beyond', end, over };
  return { kind: 'beyond', end, over, hoursNow, hoursNeeded: Math.max(hoursNeeded, hoursNow + 1) };
}

/* ---------- this visit only: "Later", "Not this week", and one step of undo ---------- */

/** What the page holds besides the saved plan. None of it is stored, so a day moved along
 *  with "Later" leaves no trace the next time the page is opened. */
export interface Visit { later?: boolean; skip?: boolean; test?: Iso }
export interface Model { state: CalState; visit: Visit }
export interface Step { model: Model; undo: Model }
/** Apply a change and keep what was there before, so "Put it back" restores it exactly. */
export function step(model: Model, change: (m: Model) => Model): Step {
  const undo: Model = JSON.parse(JSON.stringify(model));
  return { model: change(JSON.parse(JSON.stringify(model))), undo };
}

/* ---------- teacher: a course laid on the days a class meets ---------- */

export const inBreak = (d: Iso, breaks: Break[]) => breaks.find((b) => d >= b.from && d <= b.to);

export interface TeacherSetup { from: Iso; meet: number[]; per: number; breaks: Break[]; moved: Iso[] }
/** The sample's starting setup, worked out from today so it never goes stale. */
export function teacherSetup(plan: TeacherPlan | undefined, today: Iso): TeacherSetup {
  const mon = mondayOf(today);
  return {
    from: plan?.from ?? addDays(mon, -7),
    meet: plan?.meet?.length ? plan.meet : [1, 2, 3, 4, 5],
    per: plan?.per ?? 1,
    breaks: plan?.breaks ?? [{ from: addDays(mon, 11), to: addDays(mon, 11), label: 'Teacher workday (a sample day off)' }],
    moved: plan?.moved ?? [],
  };
}

export interface Meeting {
  date: Iso;
  /** 'open' = a class day with nothing planned, because today was moved back one class. */
  kind: 'lesson' | 'open';
  lessons: Lesson[];
  /** For one lesson over two meetings: 1 or 2. */
  part?: number;
}

export function meetings(lessons: Lesson[], s: TeacherSetup): Meeting[] {
  const out: Meeting[] = [];
  const meet = cleanDays(s.meet);
  if (!meet.length || !isIso(s.from)) return out;
  let li = 0;
  let part = 0;
  for (let i = 0; li < lessons.length && i < 1500; i++) {
    const d = addDays(s.from, i);
    if (!meet.includes(dow(d)) || inBreak(d, s.breaks)) continue;
    if (s.moved.includes(d)) { out.push({ date: d, kind: 'open', lessons: [] }); continue; }
    if (s.per === 0.5) {
      part++;
      out.push({ date: d, kind: 'lesson', lessons: [lessons[li]], part });
      if (part === 2) { li++; part = 0; }
    } else {
      const take = s.per === 2 ? 2 : 1;
      out.push({ date: d, kind: 'lesson', lessons: lessons.slice(li, li + take) });
      li += take;
    }
  }
  return out;
}

export interface Week { monday: Iso; meetings: Meeting[]; breaks: { label: string; days: Iso[] }[] }
/** The plan grouped by week (Monday first), with each week's days off named in its heading. */
export function weeks(ms: Meeting[], s: TeacherSetup): Week[] {
  if (!ms.length) return [];
  const meet = cleanDays(s.meet);
  const out: Week[] = [];
  const last = ms[ms.length - 1].date;
  for (let mon = mondayOf(ms[0].date); mon <= last; mon = addDays(mon, 7)) {
    const sun = addDays(mon, 6);
    const off = new Map<string, Iso[]>();
    for (let i = 0; i < 7; i++) {
      const d = addDays(mon, i);
      const b = meet.includes(dow(d)) ? inBreak(d, s.breaks) : undefined;
      if (b) off.set(b.label, [...(off.get(b.label) ?? []), d]);
    }
    out.push({ monday: mon, meetings: ms.filter((m) => m.date >= mon && m.date <= sun), breaks: [...off].map(([label, days]) => ({ label, days })) });
  }
  return out;
}

/** "Wednesday to Friday", "Friday", "Monday and Wednesday" */
export function spanWords(days: Iso[]): string {
  if (!days.length) return '';
  const run = days.every((d, i) => i === 0 || daysBetween(days[i - 1], d) === 1);
  if (days.length === 1) return weekday(days[0]);
  if (run && days.length > 2) return `${weekday(days[0])} to ${weekday(days[days.length - 1])}`;
  return days.map(weekday).slice(0, -1).join(', ') + ' and ' + weekday(days[days.length - 1]);
}

/* ---------- "Add to my calendar": a file made in the browser, sent nowhere ---------- */

const BYDAY = ['SU', 'MO', 'TU', 'WE', 'TH', 'FR', 'SA'];
const icsText = (s: string) => s.replace(/\\/g, '\\\\').replace(/;/g, '\\;').replace(/,/g, '\\,').replace(/\r?\n/g, '\\n');

/** Fold a content line at 75 octets (RFC 5545 3.1), never inside a character. */
export function foldLine(line: string): string {
  const enc = new TextEncoder();
  const out: string[] = [];
  let cur = '';
  let bytes = 0;
  for (const ch of line) {
    const n = enc.encode(ch).length;
    if (bytes + n > (out.length ? 74 : 75)) { out.push(cur); cur = ''; bytes = 0; }
    cur += ch; bytes += n;
  }
  out.push(cur);
  return out.join('\r\n ');
}

export interface RhythmFile {
  /** Calendar name and the entry's title. */
  name: string; summary: string;
  /** What the entry says, and the page it links back to. */
  text: string; url: string;
  days: number[];
  /** The first day is the first of those weekdays from here on. */
  from: Iso;
  /** How many times it repeats, so it ends by itself. */
  count: number;
  uid: string;
  /** When the file was made (UTC). */
  now: Date;
}

/** One repeating all-day entry on the person's days. It names no activity and no lesson, so it
 *  stays true when a day is skipped; it ends after `count` times; it sets no alarm. */
export function rhythmIcs(o: RhythmFile): string {
  const days = cleanDays(o.days);
  if (!days.length) return '';
  const start = rhythmDays(days, o.from, 1)[0];
  const d8 = (s: Iso) => s.replace(/-/g, '');
  const stamp = o.now.toISOString().replace(/[-:]/g, '').replace(/\.\d+Z$/, 'Z');
  const count = Math.max(1, Math.min(104, Math.round(o.count)));
  const lines = [
    'BEGIN:VCALENDAR',
    'VERSION:2.0',
    'PRODID:-//STEMhop//Calendar//EN',
    'CALSCALE:GREGORIAN',
    'METHOD:PUBLISH',
    `X-WR-CALNAME:${icsText(o.name)}`,
    'BEGIN:VEVENT',
    `UID:${o.uid}`,
    `DTSTAMP:${stamp}`,
    `DTSTART;VALUE=DATE:${d8(start)}`,
    `DTEND;VALUE=DATE:${d8(addDays(start, 1))}`,
    `RRULE:FREQ=WEEKLY;COUNT=${count};BYDAY=${[...days].sort((a, b) => a - b).map((x) => BYDAY[x]).join(',')}`,
    `SUMMARY:${icsText(o.summary)}`,
    `DESCRIPTION:${icsText(`${o.text}\n${o.url}`)}`,
    `URL:${o.url}`,
    'TRANSP:TRANSPARENT',
    'END:VEVENT',
    'END:VCALENDAR',
  ];
  return lines.map(foldLine).join('\r\n') + '\r\n';
}
