/* =============================================================================
   The calendar in the browser. It reads the plan kept on this device, draws the
   page for today, and keeps every change on this device. It makes no network
   request and sends nothing anywhere.

   After every action: one sentence is said (a polite live region, and the same
   words on the page), and focus moves to the control that undoes it.

   Storage: `stemhop:calendar:v1` (this page's own), the role in the shared
   `stemhop:prefs:v1` (written only when a role link is pressed), and the site's
   existing progress record, read for done lessons and written only through
   progress.ts setDone(). Every read and write is wrapped: with storage blocked
   the page works for this visit and says so.
   ============================================================================ */
import { readPrefs, writePrefs, type Role as PrefRole } from '../prefs';
import { load as loadProgress, setDone, CHANGE_EVENT } from '../progress';
import {
  cap, num, type Activity, type CalState, type CourseData, type Iso, type McatData, type Model,
  cleanState, courseItems, isIso, longDate, mcatItems, newParent, newStudent, newTeacher, onDays, parentDays,
  parentDid, parentPick, parentQueue, parentUndid, parentView, rhythmIcs, studentView, teacherSetup, todayIso, weekday, daysBetween,
} from './engine';
import { renderParent, renderStudent, renderTeacher, type Role, type Said, type Ui } from './render';
import { EMAIL_OPT_IN } from './flags';

const KEY = 'stemhop:calendar:v1';
/** A title, closed as a sentence: no second full stop after a title that ends in one, or in a question mark. */
const end = (t: string) => (/[.?!]$/.test(t) ? t : `${t}.`);
const PREF_OF: Record<Role, PrefRole> = { parent: 'parent', student: 'student', teacher: 'teacher' };

interface PageData {
  activities?: Activity[];
  course?: CourseData;
  mcat?: McatData;
  choices?: { s: string; t: string; level: string }[];
  lessonCourse?: Record<string, string>;
}

function readState(): CalState {
  try { return cleanState(JSON.parse(window.localStorage.getItem(KEY) ?? 'null')); } catch { return { v: 1 }; }
}
function canKeep(): boolean {
  try {
    if (window.localStorage.getItem(KEY) === null) { window.localStorage.setItem(KEY, '{"v":1}'); window.localStorage.removeItem(KEY); }
    return true;
  } catch { return false; }
}

/* A role link remembers the role, here and on the three-door page. */
document.addEventListener('click', (e) => {
  const a = (e.target as HTMLElement | null)?.closest?.<HTMLAnchorElement>('a[data-role]');
  const r = a?.dataset.role as Role | undefined;
  if (r && PREF_OF[r]) writePrefs({ role: PREF_OF[r] });
});

const root = document.getElementById('cal-root');
const reveal = () => document.documentElement.classList.remove('cal-wait');
try {
  if (root) start(root); else reveal();
} catch {
  reveal(); // the page drawn when the site was built stays as it is
}

function start(root: HTMLElement) {
  const role = root.dataset.role as Role | 'door';
  const q = new URLSearchParams(location.search);
  const state0 = readState();

  /* The three doors: go straight to the role this device already chose. */
  if (role === 'door') {
    const r = readPrefs().role;
    if (r && !q.has('choose')) { location.replace(`/calendar/${r}/`); return; }
    reveal();
    return;
  }

  let data: PageData;
  try { data = JSON.parse(document.getElementById('cal-data')?.textContent ?? '{}'); } catch { reveal(); return; }

  /* "For myself" with no course in the address: the saved plan, else the course last read. */
  if (role === 'student' && !data.course && !data.mcat) {
    const known = new Set([...(data.choices ?? []).map((c) => c.s), 'mcat']);
    let to = state0.student?.plan;
    if (!to || !known.has(to)) { try { to = data.lessonCourse?.[loadProgress().last ?? '']; } catch { to = undefined; } }
    if (to && known.has(to) && !q.has('choose')) { location.replace(`/calendar/student/${to}/`); return; }
    reveal();
    return;
  }
  /* "For my class" with no course in the address: the course this device last picked. */
  if (role === 'teacher' && root.dataset.default === '1') {
    const c = state0.teacher?.course;
    if (c && c !== data.course?.s && (data.choices ?? []).some((x) => x.s === c)) { location.replace(`/calendar/teacher/${c}/`); return; }
  }

  let today: Iso = isIso(q.get('today')) ? q.get('today')! : todayIso();
  const pinned = isIso(q.get('today'));
  let model: Model = { state: state0, visit: {} };
  const kept = canKeep();
  const hex = document.getElementById('cal-hex')?.innerHTML ?? '';
  const status = document.getElementById('cal-status');
  const reduced = () => { try { return window.matchMedia('(prefers-reduced-motion: reduce)').matches; } catch { return true; } };

  let said: Said | undefined;
  let undoFn: (() => void) | undefined;
  let undoFocus: string | undefined;
  /** Things marked done on this page during this visit (so the page works with storage blocked). */
  const doneHere = new Map<string, string>();
  const undoneHere = new Set<string>();

  const planKey = data.mcat ? 'mcat' : data.course?.s ?? '';
  const planItems = () => (data.mcat ? mcatItems(data.mcat, model.state.student ?? newStudent()) : data.course ? courseItems(data.course) : []);

  function progress(): { done: Set<string>; today: string[] } {
    const done = new Set<string>(model.state.student?.marks ?? []);
    const todayTitles: string[] = [];
    let lessons: Record<string, { d?: number; u?: number }> = {};
    try { lessons = loadProgress().lessons; } catch { /* storage blocked */ }
    const titles = new Map(planItems().map((i) => [i.key, i.t]));
    for (const [slug, r] of Object.entries(lessons)) {
      if (!r.d || (r.u && r.u > r.d) || undoneHere.has(slug)) continue;
      done.add(slug);
      if (titles.has(slug) && todayIso(new Date(r.d)) === today && !pinned) todayTitles.push(titles.get(slug)!);
    }
    for (const [k, t] of doneHere) { done.add(k); if (!todayTitles.includes(t)) todayTitles.push(t); }
    return { done, today: todayTitles };
  }

  function save() {
    try { window.localStorage.setItem(KEY, JSON.stringify(model.state)); } catch { /* blocked: this visit only */ }
  }

  function draw() {
    const ui: Ui = { today, said, kept, email: EMAIL_OPT_IN, hex };
    if (role === 'parent') return renderParent(data.activities ?? [], model.state.parent ?? newParent(), model.visit, ui);
    if (role === 'student') {
      const p = progress();
      return renderStudent({ course: data.course, mcat: data.mcat, choices: data.choices ?? [] }, model.state.student ?? newStudent(), p.done, model.visit, { ...ui, doneToday: p.today });
    }
    return renderTeacher(data.course!, data.choices ?? [], model.state.teacher, ui);
  }

  let drawn = false;
  function render(focus?: string, moving = false) {
    const paint = () => {
      const open = drawn ? [...root.querySelectorAll<HTMLDetailsElement>('details[open]')].map((d) => d.className) : [];
      drawn = true;
      root.innerHTML = draw();
      for (const c of open) root.querySelectorAll<HTMLDetailsElement>('details').forEach((d) => { if (d.className === c) d.open = true; });
      root.classList.add('cal-js');
      if (focus) {
        const el = root.querySelector<HTMLElement>(focus) ?? root.querySelector<HTMLElement>('h1');
        el?.focus({ preventScroll: false });
      }
    };
    const vt = (document as Document & { startViewTransition?: (cb: () => void) => unknown }).startViewTransition;
    if (moving && vt && !reduced()) vt.call(document, paint); else paint();
  }

  function say(text: string) {
    if (!status) return;
    status.textContent = '';
    window.setTimeout(() => { status.textContent = text; }, 60);
  }

  /** Make a change, keep it, say what happened, and put focus on the way back. */
  function act(change: () => void, s: Said, opts: { from?: string; undo?: () => void; focus?: string; noUndo?: boolean } = {}) {
    const before: Model = JSON.parse(JSON.stringify(model));
    change();
    save();
    undoFn = opts.noUndo ? undefined : opts.undo ?? (() => { model = before; save(); });
    undoFocus = opts.from;
    said = opts.noUndo ? { text: s.text } : s;
    render(opts.focus ?? (said.undo ? '[data-fid="undo"]' : opts.from ? `[data-fid="${opts.from}"]` : undefined), true);
    say(s.text);
  }

  function undo() {
    if (!undoFn) return;
    undoFn();
    undoFn = undefined;
    said = { text: 'Put back.' };
    render(undoFocus ? `[data-fid="${undoFocus}"]` : 'h1', true);
    say('Put back.');
  }

  const P = () => (model.state.parent ??= newParent());
  const S = () => { const s = (model.state.student ??= newStudent()); if (planKey) s.plan = planKey; return s; };
  const T = () => { const t = (model.state.teacher ??= newTeacher()); if (data.course) t.course = data.course.s; return t; };
  const checked = (name: string) => [...root.querySelectorAll<HTMLInputElement>(`input[name="${name}"]:checked`)].map((i) => Number(i.value));
  const field = (name: string) => (root.querySelector<HTMLInputElement>(`[name="${name}"]`)?.value ?? '').trim();
  const sameInput = (t: HTMLInputElement | HTMLSelectElement) => (t.type === 'checkbox' || t.type === 'radio' ? `input[name="${t.name}"][value="${t.value}"]` : `[name="${t.name}"]`);

  render();
  reveal();

  /* ---------- changes ---------- */
  root.addEventListener('change', (e) => {
    const t = e.target as HTMLInputElement;
    if (t.dataset.have) {
      const p = P();
      if (t.checked) p.have[t.dataset.have] = 1; else delete p.have[t.dataset.have];
      save();
      return; // the tick is the change; nothing else moves
    }
    const here = sameInput(t);
    switch (t.name) {
      case 'pdays': {
        const d = checked('pdays');
        act(() => { P().days = d; model.visit.skip = false; }, { text: d.length ? `${d.length === 1 ? 'One activity a week' : `${cap(num(d.length))} a week`}, ${onDays(d)}.` : 'No set day. The next activity is here when you are.' }, { focus: here, noUndo: true });
        return;
      }
      case 'plist':
        act(() => { const n = Number(t.value); const p = P(); if (n === 2 || n === 3) p.list = n; else delete p.list; }, { text: t.value === '1' ? 'The list is for this activity.' : `The list is for the next ${t.value === '2' ? 'two' : 'three'} activities.` }, { focus: here, noUndo: true });
        return;
      case 'splan': {
        const s = (model.state.student ??= newStudent());
        s.plan = t.value;
        save();
        location.href = `/calendar/student/${t.value}/`;
        return;
      }
      case 'sdays': {
        const d = checked('sdays');
        act(() => { S().days = d; model.visit.later = false; }, { text: d.length ? `Dates added, counted from today, ${onDays(d)}.` : 'No set days. Nothing is dated.' }, { focus: here, noUndo: true });
        return;
      }
      case 'sstart':
        act(() => { const s = S(); if (t.value) s.start[planKey] = t.value; else delete s.start[planKey]; }, { text: 'Starting there. Earlier lessons are still in the whole course, below.' }, { focus: here, noUndo: true });
        return;
      case 'ssit':
        act(() => { S().sit = Number(t.value); }, { text: 'Sittings changed.' }, { focus: here, noUndo: true });
        return;
      case 'scourse': {
        const step = data.mcat?.steps.find((x) => x.s === t.value);
        if (!step) return;
        act(() => {
          const s = S();
          if (step.optional) s.opt = t.checked ? [...new Set([...s.opt, step.s])] : s.opt.filter((x) => x !== step.s);
          else s.out = t.checked ? s.out.filter((x) => x !== step.s) : [...new Set([...s.out, step.s])];
        }, { text: t.checked ? `${step.t} is in the plan.` : `${step.t} is left out. The plan closed up.` }, { focus: here, noUndo: true });
        return;
      }
      case 'stest':
        model.visit.test = isIso(t.value) ? t.value : undefined;
        said = undefined;
        render(here);
        say(root.querySelector('#cal-reach')?.textContent ?? '');
        return;
      case 'tcourse': {
        const tp = (model.state.teacher ??= newTeacher());
        tp.course = t.value;
        tp.moved = [];
        save();
        location.href = t.value === root.dataset.home ? '/calendar/teacher/' : `/calendar/teacher/${t.value}/`;
        return;
      }
      case 'tfrom':
        if (isIso(t.value)) act(() => { const p = T(); p.from = t.value; p.moved = []; }, { text: `The first class is ${longDate(t.value)}.` }, { focus: here, noUndo: true });
        return;
      case 'tmeet': {
        const d = checked('tmeet');
        if (!d.length) { t.checked = true; say('A class needs at least one day.'); return; }
        act(() => { T().meet = d; }, { text: `The class meets ${onDays(d)}.` }, { focus: here, noUndo: true });
        return;
      }
      case 'tper':
        act(() => { T().per = Number(t.value); }, { text: 'Pace changed. Every date after the first class moved with it.' }, { focus: here, noUndo: true });
        return;
    }
  });

  root.addEventListener('click', (e) => {
    const b = (e.target as HTMLElement).closest<HTMLElement>('[data-act]');
    if (!b) return;
    switch (b.dataset.act) {
      case 'undo': undo(); return;
      case 'print': window.print(); return;
      case 'ics': makeFile(); return;
      case 'choose': openDialog('cal-choose'); return;
      case 'email': openDialog('cal-email'); return;
      case 'forget': {
        const r = b.dataset.role as Role;
        act(() => { delete model.state[r]; model.visit = {}; }, { text: 'Forgotten on this device.', undo: 'Put it back', undoName: 'Put it back: keep the plan after all' }, { from: 'forget' });
        return;
      }
      /* parent */
      case 'did': {
        const acts = data.activities ?? [];
        const a = acts.find((x) => x.s === b.dataset.s);
        if (!a) return;
        const next = parentQueue(acts, parentDid(P(), a))[0];
        act(() => { model.state.parent = parentDid(P(), a); model.visit.skip = false; }, { text: `Done together: ${end(a.t)}${next ? ` The next one is ${end(next.t)}` : ''}`, undo: 'Put it back', undoName: `Put it back: ${a.t} is not done yet` }, { from: 'did' });
        return;
      }
      case 'undid': {
        const a = (data.activities ?? []).find((x) => x.s === b.dataset.s);
        if (!a) return;
        act(() => { model.state.parent = parentUndid(P(), a.s); }, { text: `${a.t} is back in the plan.`, undo: 'Undo', undoName: `Undo: ${a.t} stays done` }, { from: 'title' });
        return;
      }
      case 'skip': {
        const v = parentView(data.activities ?? [], P(), today, { skip: true });
        if (!v.next || !v.date || !v.freed) return;
        act(() => { model.visit.skip = true; }, { text: `Nothing ${daysBetween(today, v.freed) === 0 ? 'today' : `this ${weekday(v.freed)}`}. ${v.next.t} waits for ${longDate(v.date)}.`, undo: 'Put it back', undoName: `Put it back: ${v.next.t} on ${weekday(v.freed)}` }, { from: 'skip' });
        return;
      }
      /* student */
      case 'done': {
        const p = progress();
        const view = studentView(itemsNow(), p.done, sizing(), today, { later: model.visit.later, spent: !!p.today.length });
        const s = view.top?.sitting;
        if (!s) return;
        const keys = s.items.map((i) => i);
        const name = keys.length > 1 ? `${keys.length} lessons` : keys[0].t;
        const apply = (on: boolean) => {
          const st = S();
          for (const it of keys) {
            if (it.kind === 'lesson') { try { setDone(it.key, on); } catch { /* blocked */ } if (on) undoneHere.delete(it.key); else undoneHere.add(it.key); }
            else st.marks = on ? [...new Set([...st.marks, it.key])] : st.marks.filter((k) => k !== it.key);
            if (on) doneHere.set(it.key, it.t); else doneHere.delete(it.key);
          }
          model.visit.later = false;
        };
        const nx = view.rows[0]?.sitting.items[0]?.t;
        act(() => apply(true), { text: `Done: ${end(name)}${nx ? ` Next: ${end(nx)}` : ''}`, undo: 'Undo', undoName: `Undo: ${name} is not done` }, { from: 'done', undo: () => { apply(false); save(); } });
        return;
      }
      case 'undone': {
        const k = b.dataset.key!;
        const it = planItems().find((i) => i.key === k);
        if (!it) return;
        const apply = (on: boolean) => {
          const st = S();
          if (it.kind === 'lesson') { try { setDone(k, on); } catch { /* blocked */ } if (on) undoneHere.delete(k); else undoneHere.add(k); }
          else st.marks = on ? [...new Set([...st.marks, k])] : st.marks.filter((x) => x !== k);
          if (!on) doneHere.delete(k);
        };
        act(() => apply(false), { text: `${it.t} is back in the plan.`, undo: 'Undo', undoName: `Undo: ${it.t} stays done` }, { from: 'title', undo: () => { apply(true); save(); } });
        return;
      }
      case 'later': {
        const p = progress();
        const v = studentView(itemsNow(), p.done, sizing(), today, { later: true });
        const to = v.top?.date;
        undoFn = () => { model.visit.later = false; };
        undoFocus = 'later';
        model.visit.later = true;
        said = undefined; // the emptied card says it, and holds "Put it back"
        render('[data-fid="undo"]', true);
        say(to ? `Moved to ${daysBetween(today, to) === 1 ? 'tomorrow' : longDate(to)}.` : 'Moved to the next day.');
        return;
      }
      /* teacher */
      case 'lost':
        act(() => { const t = T(); t.moved = [...new Set([...t.moved, today])].sort(); }, { text: 'Moved back one class from today. Every later lesson moved with it.' }, { focus: '[data-fid="undo"]', undo: () => { const t = T(); t.moved = t.moved.filter((d) => d !== today); save(); } });
        return;
      case 'unlost':
        act(() => { const t = T(); t.moved = t.moved.filter((d) => d !== today); }, { text: 'Put back. Every later lesson moved up one class.' }, { focus: '[data-fid="lost"]', noUndo: true });
        return;
      case 'addbreak': {
        const from = field('bfrom');
        const to = field('bto') || from;
        if (!isIso(from) || !isIso(to) || to < from) {
          say('Give the break a first day, and a last day that is not before it.');
          root.querySelector<HTMLInputElement>('[name="bfrom"]')?.focus();
          return;
        }
        const label = field('blabel').replace(/[<>]/g, '') || 'No class';
        const next = [...teacherSetup(model.state.teacher, today).breaks, { from, to, label }].sort((a, z) => a.from.localeCompare(z.from));
        const at = next.findIndex((x) => x.from === from && x.to === to && x.label === label);
        act(() => { T().breaks = next; }, { text: 'Added. Lessons on those days moved to the next class.' }, { focus: `[data-fid="unbreak-${at}"]`, noUndo: true });
        return;
      }
      case 'unbreak':
        act(() => { const t = T(); t.breaks = teacherSetup(t, today).breaks.filter((_, i) => i !== Number(b.dataset.i)); }, { text: 'Removed. The plan closed up.' }, { focus: '[name="bfrom"]', noUndo: true });
        return;
    }
  });

  const itemsNow = () => {
    const st = model.state.student ?? newStudent();
    return data.mcat ? mcatItems(data.mcat, st) : courseItems(data.course!, st.start[planKey]);
  };
  const sizing = () => { const st = model.state.student ?? newStudent(); return { days: st.days, sit: data.mcat ? st.sit : 0 }; };

  /* ---------- dialogs (native) ---------- */
  function openDialog(id: string) {
    const d = document.getElementById(id) as HTMLDialogElement | null;
    if (d && !d.open) d.showModal();
  }
  const choose = document.getElementById('cal-choose') as HTMLDialogElement | null;
  choose?.addEventListener('click', (e) => {
    const t = e.target as HTMLElement;
    if (t === choose) { choose.close(); return; }
    const b = t.closest<HTMLElement>('[data-act]');
    if (b?.dataset.act === 'close') choose.close();
    if (b?.dataset.act === 'pick' && b.dataset.s) {
      const acts = data.activities ?? [];
      const pick = acts.find((a) => a.s === b.dataset.s);
      const old = parentQueue(acts, P())[0];
      choose.close();
      if (!pick || pick.s === old?.s) { root.querySelector<HTMLElement>('[data-fid="choose"]')?.focus(); return; }
      act(() => { model.state.parent = parentPick(acts, P(), pick.s); }, { text: `Next: ${end(pick.t)}${old ? ` Then: ${end(old.t)}` : ''}`, undo: 'Put it back', undoName: `Put it back: ${old?.t ?? 'the plan'} comes first again` }, { from: 'choose' });
    }
  });
  const email = document.getElementById('cal-email') as HTMLDialogElement | null;
  email?.addEventListener('click', (e) => { if ((e.target as HTMLElement).closest('[data-act="close"]') || e.target === email) email.close(); });
  email?.querySelector('form')?.addEventListener('submit', (e) => {
    e.preventDefault();
    const out = email.querySelector('.cal-email-said');
    if (out) out.textContent = 'Email is not switched on yet. Nothing was sent, and your address was not kept.';
  });

  /* ---------- "Add to my calendar": made here, sent nowhere ---------- */
  function makeFile() {
    const uid = `${(globalThis.crypto?.randomUUID?.() ?? String(Date.now()) + Math.random().toString(36).slice(2))}@stemhop.com`;
    let body = '';
    let file = 'stemhop.ics';
    if (role === 'parent') {
      const p = P();
      const left = parentQueue(data.activities ?? [], p).length;
      body = rhythmIcs({
        name: 'STEMhop: Biology Together', summary: 'Biology Together activity (STEMhop)',
        text: 'A hands-on activity for ages 5 to 10 with a grown-up. This entry names no activity, so it stays right if you skip a week or do two. What is next, how long it takes and what to gather are on this page:',
        url: `${__SITE_ORIGIN__}/calendar/parent/`, days: parentDays(p), from: today, count: Math.min(left, 12), uid, now: new Date(),
      });
      file = 'stemhop-activities.ics';
    } else if (role === 'student') {
      const st = model.state.student ?? newStudent();
      const open = studentView(itemsNow(), progress().done, sizing(), today).all.length;
      const name = data.mcat ? 'the MCAT path' : data.course!.t;
      body = rhythmIcs({
        name: `STEMhop: ${name}`, summary: `Study: ${name} (STEMhop)`,
        text: 'Your next lesson, with its true length, is on this page. This entry names no lesson, so it stays right when you get ahead or take a week off:',
        url: `${__SITE_ORIGIN__}/calendar/student/${planKey}/`, days: st.days, from: today, count: open, uid, now: new Date(),
      });
      file = 'stemhop-study.ics';
    }
    if (!body) return;
    const a = document.createElement('a');
    a.href = URL.createObjectURL(new Blob([body], { type: 'text/calendar;charset=utf-8' }));
    a.download = file;
    document.body.appendChild(a);
    a.click();
    window.setTimeout(() => { URL.revokeObjectURL(a.href); a.remove(); }, 1000);
    said = { text: 'The calendar file was saved to this device. Open it to add the entry to your calendar.' };
    render('[data-fid="ics"]');
    say(said.text);
  }

  /* Keep in step with the lesson pages, another tab, and midnight. */
  window.addEventListener(CHANGE_EVENT, () => { if (role === 'student') render(); });
  window.addEventListener('storage', (e) => {
    if (e.key === KEY || e.key === null) { model = { state: readState(), visit: model.visit }; said = undefined; undoFn = undefined; render(); }
  });
  document.addEventListener('visibilitychange', () => {
    if (document.hidden || pinned) return;
    const now = todayIso();
    if (now !== today) { today = now; model.visit = { test: model.visit.test }; said = undefined; undoFn = undefined; render(); }
  });
}
