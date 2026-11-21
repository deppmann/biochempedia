/* =============================================================================
   The calendar in the browser. It reads the plan kept on this device, draws the
   page for today, and keeps every change on this device. It makes no network
   request and sends nothing anywhere.

   After every action: one sentence is said (a polite live region, and the same
   words on the page), and focus moves to the control that undoes it.

   Storage: `stemhop:calendar:v1` (this page's own, see store.ts), the role in
   the shared `stemhop:prefs:v1` (written only when a role link is pressed), and
   the site's existing progress record, read for done lessons and written only
   through progress.ts setDone(). Every read and write is wrapped: with storage
   blocked the page works for this visit and says so.
   ============================================================================ */
import { readPrefs, writePrefs, type Role as PrefRole } from '../prefs';
import { load as loadProgress, setDone, CHANGE_EVENT, STORAGE_KEY as PROGRESS_KEY } from '../progress';
import {
  cap, num, type Activity, type CalState, type CourseData, type Iso, type McatData, type Model,
  cleanState, courseItems, isIso, longDate, mcatItems, newParent, newStudent, newTeacher, onDays, parentDays,
  parentDid, parentPick, parentQueue, parentUndid, parentView, pinTeacher, rhythmIcs, studentView, teacherSetup, todayIso, weekday, daysBetween,
} from './engine';
import { end, renderParent, renderStudent, renderTeacher, type Role, type Said, type Ui } from './render';
import { EMAIL_OPT_IN } from './flags';
import { CAL_KEY as KEY, CAL_EVENT } from './store';

const PREF_OF: Record<Role, PrefRole> = { parent: 'parent', student: 'student', teacher: 'teacher' };
const SIT_SAY: Record<number, string> = { 60: 'about an hour', 90: 'about an hour and a half', 120: 'about two hours', 180: 'about three hours' };
const PER_SAY: Record<string, string> = { '1': 'One lesson a meeting', '0.5': 'One lesson over two meetings', '2': 'Two lessons a meeting' };

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
  /* A course picked from the "For myself" list is remembered, like a role. */
  const plan = (e.target as HTMLElement | null)?.closest?.<HTMLAnchorElement>('a[data-plan]')?.dataset.plan;
  if (plan) {
    try {
      const s = readState();
      (s.student ??= newStudent()).plan = plan;
      window.localStorage.setItem(KEY, JSON.stringify(s));
    } catch { /* blocked: the address still says which plan */ }
  }
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

  /* The three doors: go straight to the role this device already chose. (A small script in the
     page's frame does this first, before this file has loaded; this is the same rule again.) */
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

  /* ?today=YYYY-MM-DD pins the date, for checking the page while it is being built. Never on the live site. */
  const local = import.meta.env.DEV || /^(localhost|127\.0\.0\.1|\[::1\])$/.test(location.hostname);
  const pinned = local && isIso(q.get('today'));
  let today: Iso = pinned ? q.get('today')! : todayIso();
  let model: Model = { state: state0, visit: {} };
  const kept = canKeep();
  const hex = document.getElementById('cal-hex')?.innerHTML ?? '';
  const status = document.getElementById('cal-status');
  const reduced = () => { try { return window.matchMedia('(prefers-reduced-motion: reduce)').matches; } catch { return true; } };

  let said: Said | undefined;
  let err: Ui['err'];
  let undoFn: (() => void) | undefined;
  let undoFocus: string | undefined;
  /** What "Put it back" says once it has been pressed. */
  let undoSaid = 'Put back.';
  /** Things marked done on this page during this visit (so the page works with storage blocked). */
  const doneHere = new Map<string, string>();
  const undoneHere = new Set<string>();
  /** Lessons whose done mark was taken off and put back here: their fresh timestamp is not "done today". */
  const remarked = new Set<string>();

  const planKey = data.mcat ? 'mcat' : data.course?.s ?? '';
  const planItems = () => (data.mcat ? mcatItems(data.mcat, model.state.student ?? newStudent()) : data.course ? courseItems(data.course) : []);

  function progress(): { done: Set<string>; today: string[] } {
    const done = new Set<string>(model.state.student?.marks ?? []);
    const todayTitles: string[] = [];
    let lessons: Record<string, { d?: number; u?: number } | null> = {};
    try { lessons = loadProgress().lessons ?? {}; } catch { /* storage blocked */ }
    const titles = new Map(planItems().map((i) => [i.key, i.t]));
    for (const [slug, r] of Object.entries(lessons)) {
      if (!r || typeof r !== 'object' || !r.d || (r.u && r.u > r.d) || undoneHere.has(slug)) continue;
      done.add(slug);
      if (titles.has(slug) && !remarked.has(slug) && !pinned && todayIso(new Date(r.d)) === today) todayTitles.push(titles.get(slug)!);
    }
    for (const [k, t] of doneHere) { done.add(k); if (t && !todayTitles.includes(t)) todayTitles.push(t); }
    return { done, today: todayTitles };
  }

  function save() {
    try { window.localStorage.setItem(KEY, JSON.stringify(model.state)); } catch { /* blocked: this visit only */ }
  }

  function draw() {
    const ui: Ui = { today, said, kept, email: EMAIL_OPT_IN, hex, err };
    if (role === 'parent') return renderParent(data.activities ?? [], model.state.parent ?? newParent(), model.visit, ui);
    if (role === 'student') {
      const p = progress();
      return renderStudent({ course: data.course, mcat: data.mcat, choices: data.choices ?? [] }, model.state.student ?? newStudent(), p.done, model.visit, { ...ui, doneToday: p.today });
    }
    return renderTeacher(data.course!, data.choices ?? [], model.state.teacher, ui);
  }

  /** Where focus is now, as something that can be found again after the page is redrawn. */
  function focusNow(): string | undefined {
    const a = document.activeElement as HTMLInputElement | null;
    if (!a || !root.contains(a)) return undefined;
    if (a.dataset.fid) return `[data-fid="${a.dataset.fid}"]`;
    if (a.name) return a.type === 'checkbox' || a.type === 'radio' ? `input[name="${a.name}"][value="${a.value}"]` : `[name="${a.name}"]`;
    if (a.dataset.have) return `input[data-have="${a.dataset.have}"]`;
    if (a.tagName === 'SUMMARY') return `details[data-fold="${(a.parentElement as HTMLElement).dataset.fold}"] > summary`;
    const href = a.getAttribute('href');
    if (a.tagName === 'A' && href && !/["\\]/.test(href)) return `a[href="${href}"]`;
    return undefined;
  }

  let drawn = false;
  function render(focus?: string, moving = false) {
    const paint = () => {
      const open = drawn ? [...root.querySelectorAll<HTMLDetailsElement>('details[open][data-fold]')].map((d) => d.dataset.fold) : [];
      // A field being filled in keeps what was typed when the page around it is redrawn.
      const typed = drawn ? [...root.querySelectorAll<HTMLInputElement>('input[name="bfrom"], input[name="bto"], input[name="blabel"]')].map((i) => [i.name, i.value] as const) : [];
      drawn = true;
      root.innerHTML = draw();
      for (const k of open) { const d = root.querySelector<HTMLDetailsElement>(`details[data-fold="${k}"]`); if (d) d.open = true; }
      for (const [n, v] of typed) { const i = root.querySelector<HTMLInputElement>(`input[name="${n}"]`); if (i && v) i.value = v; }
      root.classList.add('cal-js');
      if (focus) {
        const el = root.querySelector<HTMLElement>(focus) ?? root.querySelector<HTMLElement>('[data-fid="title"]') ?? root.querySelector<HTMLElement>('h1');
        el?.focus({ preventScroll: false });
        // The sentence beside the focused control comes into view with it (the site header is sticky).
        el?.closest('.cal-said, .cal-card')?.scrollIntoView({ block: 'nearest' });
      }
    };
    type Transition = { ready?: Promise<unknown>; finished?: Promise<unknown>; updateCallbackDone?: Promise<unknown> };
    const vt = (document as Document & { startViewTransition?: (cb: () => void) => Transition }).startViewTransition;
    if (moving && vt && !reduced()) {
      // A second action can cut a transition short; that is not an error.
      const tr = vt.call(document, paint);
      for (const pr of [tr?.ready, tr?.finished, tr?.updateCallbackDone]) pr?.catch(() => {});
    } else paint();
  }
  /** Redraw because something changed elsewhere (a lesson page, another tab, midnight): keep the person's place. */
  const refresh = () => render(focusNow());

  function say(text: string) {
    if (!status) return;
    status.textContent = '';
    window.setTimeout(() => { status.textContent = text; }, 60);
  }

  /** Make a change, keep it, say what happened, and put focus on the way back. */
  function act(change: () => void, s: Said, opts: { from?: string; undo?: () => void; focus?: string; noUndo?: boolean; back?: string } = {}) {
    const before: Model = JSON.parse(JSON.stringify(model));
    change();
    save();
    err = undefined;
    undoFn = opts.noUndo ? undefined : opts.undo ?? (() => { model = before; save(); });
    undoFocus = opts.from;
    undoSaid = opts.back ?? 'Put back.';
    said = opts.noUndo ? { text: s.text } : s;
    render(opts.focus ?? (said.undo ? '[data-fid="undo"]' : opts.from ? `[data-fid="${opts.from}"]` : undefined), true);
    say(s.text);
  }

  function undo() {
    if (!undoFn) return;
    undoFn();
    undoFn = undefined;
    err = undefined;
    said = { text: undoSaid };
    render(undoFocus ? `[data-fid="${undoFocus}"]` : 'h1', true);
    say(undoSaid);
  }

  /** Something the person has to put right: said aloud, and shown beside the field. */
  function complain(at: NonNullable<Ui['err']>['at'], text: string, focus: string) {
    err = { at, text };
    said = undefined;
    render(focus);
    say(text);
  }

  /** "Go" pressed with the plan already showing: the panel closes, focus stays findable, and a word is said. */
  function already() {
    const d = root.querySelector<HTMLDetailsElement>('details[data-fold="set"]');
    if (d) { d.open = false; d.querySelector('summary')?.focus(); }
    say('You are already on this one.');
  }
  const P = () => (model.state.parent ??= newParent());
  const S = () => { const s = (model.state.student ??= newStudent()); if (planKey) s.plan = planKey; return s; };
  /* The first change a teacher makes pins the first class and the breaks that are on screen. */
  const T = () => { const t = pinTeacher((model.state.teacher ??= newTeacher()), today); if (data.course) t.course = data.course.s; return t; };
  const checked = (name: string) => [...root.querySelectorAll<HTMLInputElement>(`input[name="${name}"]:checked`)].map((i) => Number(i.value));
  const field = (name: string) => (root.querySelector<HTMLInputElement>(`[name="${name}"]`)?.value ?? '').trim();
  const sameInput = (t: HTMLInputElement | HTMLSelectElement) => (t.type === 'checkbox' || t.type === 'radio' ? `input[name="${t.name}"][value="${t.value}"]` : `[name="${t.name}"]`);
  const itemsNow = () => {
    const st = model.state.student ?? newStudent();
    return data.mcat ? mcatItems(data.mcat, st) : courseItems(data.course!, st.start[planKey]);
  };
  const sizing = () => { const st = model.state.student ?? newStudent(); return { days: st.days, sit: data.mcat ? st.sit : 0 }; };

  render();
  reveal();

  /* ---------- the two dates a person may type ----------
     A date field fires "change" on every keystroke that leaves a whole date. Redrawing then would
     replace the field under the person's fingers. So while a date is being typed nothing is
     redrawn; the date is taken once, when they press Enter or leave the field. A date chosen from
     the picker (no typing) is taken at once. */
  const DATES = ['tfrom', 'stest'];
  /** Lists whose choice redraws the page. Arrowing or typing through one must not redraw on every key. */
  const LISTS = ['sstart', 'ssit', 'tper'];
  let typing = '';
  /** Redraw the parts of the page named, leaving everything else (the field in hand, the button
   *  about to be pressed) exactly as it is. */
  function patch(selectors: string[]) {
    const fresh = document.createElement('div');
    fresh.innerHTML = draw();
    for (const sel of selectors) {
      const now = root.querySelector(sel);
      const next = fresh.querySelector(sel);
      if (now && next) now.replaceWith(next);
    }
  }
  /* A redraw that is owed but must wait a moment: when a field is left by pressing a button, the
     button has to live until the press lands. Whatever acts next runs the owed redraw first. */
  let owed: (() => void) | undefined;
  let owedTimer = 0;
  const owe = (fn: () => void) => { settle(); owed = fn; owedTimer = window.setTimeout(settle, 400); };
  function settle() {
    window.clearTimeout(owedTimer);
    const fn = owed;
    owed = undefined;
    fn?.();
  }
  let testTimer = 0;

  function commitDate(t: HTMLInputElement, later = false) {
    typing = '';
    window.clearTimeout(testTimer);
    if (t.name === 'tfrom') {
      const now = teacherSetup(model.state.teacher, today).from;
      if (t.value === now) return;
      if (!isIso(t.value)) {
        // Emptied or half typed: the plan keeps its date, and says so.
        t.value = now;
        window.setTimeout(() => { if (!isIso(t.value)) t.value = now; }, 0);   // some browsers clear a half-typed date after this runs
        said = { text: `The first class is still ${longDate(now)}.` };
        patch(['.cal-note-slot']);
        say(said.text);
        return;
      }
      const p = T();
      p.from = t.value;
      p.moved = [];
      save();
      err = undefined;
      undoFn = undefined;
      said = { text: `The first class is ${longDate(t.value)}.` };
      say(said.text);
      const redraw = () => { patch(['.cal-set > summary', '.cal-note-slot', '.cal-cols', '.cal-print-head']); root.querySelector('.cal-set-body .cal-err')?.remove(); };
      if (later) owe(redraw); else redraw();
    } else if (t.name === 'stest') {
      const v = isIso(t.value) ? t.value : undefined;
      if (v === model.visit.test) return;
      model.visit.test = v;
      patch(['#cal-reach']);   // only the sentence under the field; the field and the page stay put
      say(root.querySelector('#cal-reach')?.textContent ?? '');
    }
  }
  root.addEventListener('keydown', (e) => {
    const t = e.target as HTMLInputElement;
    if (LISTS.includes(t.name)) {
      if (e.key === 'Enter') { if (typing === t.name) { typing = ''; changed(t); } }
      else if (e.key !== 'Tab' && e.key !== 'Escape') typing = t.name;
      return;
    }
    if (!DATES.includes(t.name)) return;
    if (e.key === 'Enter') { e.preventDefault(); commitDate(t); return; }
    if (e.key !== 'Tab') typing = t.name;
  });
  /* A test date typed in full answers by itself a second after the last key. */
  root.addEventListener('input', (e) => {
    const t = e.target as HTMLInputElement;
    if (t.name !== 'stest') return;
    window.clearTimeout(testTimer);
    if (isIso(t.value) && t.value.slice(0, 4) >= today.slice(0, 4)) testTimer = window.setTimeout(() => { if (root.contains(t)) { const keep = typing; commitDate(t); typing = keep; } }, 1000);
  });
  root.addEventListener('focusout', (e) => {
    const t = e.target as HTMLInputElement;
    if (typing !== t.name) return;
    if (DATES.includes(t.name)) commitDate(t, true);
    else if (LISTS.includes(t.name)) { typing = ''; const v = t.value; owe(() => { const now = root.querySelector<HTMLSelectElement>(`select[name="${t.name}"]`); if (now) { now.value = v; changed(now as unknown as HTMLInputElement, focusNow()); } }); }
  });
  /** A date or a list still in hand is taken, and any owed redraw done, before anything else acts. */
  const flush = (except?: string) => {
    if (typing && typing !== except) {
      const i = root.querySelector<HTMLInputElement>(`[name="${typing}"]`);
      const name = typing;
      typing = '';
      if (i && DATES.includes(name)) commitDate(i); else if (i) changed(i, focusNow());
    }
    settle();
  };

  /* ---------- changes ---------- */
  root.addEventListener('change', (e) => {
    const t = e.target as HTMLInputElement;
    flush(t.name);
    if (typing === t.name && LISTS.includes(t.name)) return;   // being arrowed or typed through: taken on Enter or on leaving
    changed(t);
  });
  function changed(t: HTMLInputElement, focus?: string) {
    if (t.dataset.have) {
      const p = P();
      if (t.checked) p.have[t.dataset.have] = 1; else delete p.have[t.dataset.have];
      save();
      // The tick is the change. An older sentence about something else comes down.
      said = undefined;
      root.querySelector('.cal-note-slot .cal-said')?.remove();
      return;
    }
    const here = focus ?? sameInput(t);
    switch (t.name) {
      case 'tfrom':
      case 'stest':
        if (typing !== t.name) commitDate(t);
        return;
      case 'pdays': {
        const d = checked('pdays');
        act(() => { P().days = d; model.visit.skip = false; }, { text: d.length ? `${d.length === 1 ? 'One activity a week' : `${cap(num(d.length))} a week`}, ${onDays(d)}.` : 'No set day. The next activity is here when you are.' }, { focus: here, noUndo: true });
        return;
      }
      case 'plist':
        act(() => { const n = Number(t.value); const p = P(); if (n === 2 || n === 3) p.list = n; else delete p.list; }, { text: t.value === '1' ? 'The list is for this activity.' : `The list is for the next ${t.value === '2' ? 'two' : 'three'} activities.` }, { focus: here, noUndo: true });
        return;
      case 'sdays': {
        const d = checked('sdays');
        act(() => { S().days = d; model.visit.later = false; }, { text: d.length ? `Dates added, counted from today, ${onDays(d)}.` : 'No set days. Nothing is dated.' }, { focus: here, noUndo: true });
        return;
      }
      case 'sstart':
        act(() => { const s = S(); if (t.value) s.start[planKey] = t.value; else delete s.start[planKey]; }, { text: 'Starting there. Earlier lessons are still in the whole course, below.' }, { focus: here, noUndo: true });
        return;
      case 'ssit':
        act(() => { S().sit = Number(t.value); }, { text: Number(t.value) ? `Each sitting now holds ${SIT_SAY[Number(t.value)] ?? 'about that long'}.` : 'One lesson at a time now.' }, { focus: here, noUndo: true });
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
      case 'tmeet': {
        const d = checked('tmeet');
        if (!d.length) { complain('meet', 'A class needs at least one day.', here); return; }
        act(() => { T().meet = d; }, { text: `The class meets ${onDays(d)}.` }, { focus: here, noUndo: true });
        return;
      }
      case 'tper':
        act(() => { T().per = Number(t.value); }, { text: `${PER_SAY[t.value] ?? 'The pace changed'} now. Every later date moved with it.` }, { focus: here, noUndo: true });
        return;
      /* The two lists that lead to another page (splan, tcourse) do nothing on change:
         each has a button beside it, so arrowing or typing through the list never navigates. */
    }
  }

  root.addEventListener('click', (e) => {
    const b = (e.target as HTMLElement).closest<HTMLElement>('[data-act]');
    if (!b) return;
    flush();
    switch (b.dataset.act) {
      case 'undo': undo(); return;
      case 'print': window.print(); return;
      case 'ics': makeFile(); return;
      case 'choose': openDialog('cal-choose'); return;
      case 'email': openDialog('cal-email'); return;
      case 'go-plan': {
        const v = field('splan');
        if (!v) return;
        if (v === planKey) { already(); return; }
        (model.state.student ??= newStudent()).plan = v;
        save();
        location.replace(`/calendar/student/${v}/`);
        return;
      }
      case 'go-course': {
        const v = field('tcourse');
        if (!v) return;
        if (v === data.course?.s) { already(); return; }
        T().course = v;   // an open day is a fact about the class's calendar, so it stays when the course changes
        save();
        location.replace(`/calendar/teacher/${v}/`);
        return;
      }
      case 'forget': {
        // Everything the calendar keeps, and who it is for, so the next person starts clean.
        let role0: PrefRole | undefined;
        try { role0 = readPrefs().role; } catch { role0 = undefined; }
        const text = role === 'parent' ? 'Your days, your ticks and what you did together are forgotten on this device.'
          : role === 'student' ? 'Your days and choices are forgotten on this device. Lessons you marked done stay marked.'
          : 'Your class days and breaks are forgotten on this device.';
        act(() => { model.state = { v: 1 }; model.visit = {}; }, { text, undo: 'Put it back', undoName: 'Put it back: keep it after all' }, { from: 'forget', back: 'Kept after all.' });
        const restore = undoFn;
        try { window.localStorage.removeItem(KEY); } catch { /* blocked */ }
        writePrefs({ role: null });   // only who the calendar is for; other saved choices are left alone
        undoFn = () => { restore?.(); if (role0) writePrefs({ role: role0 }); };
        return;
      }
      /* parent */
      case 'did': {
        const acts = data.activities ?? [];
        const a = acts.find((x) => x.s === b.dataset.s);
        if (!a) return;
        const next = parentQueue(acts, parentDid(P(), a))[0];
        // Done on the activity day itself: today is used, so the next one sits on the next chosen day (this visit only).
        const onDay = parentView(acts, P(), today, { skip: model.visit.skip, used: model.visit.used }).date === today;
        act(() => { model.state.parent = parentDid(P(), a); model.visit.skip = false; if (onDay) model.visit.used = true; }, { text: `Done together: ${end(a.t)}${next ? ` The next one is ${end(next.t)}` : ''}`, undo: 'Put it back', undoName: `Put it back: ${a.t} is not done yet` }, { from: 'did', back: `${a.t} is back as the next activity.` });
        return;
      }
      case 'undid': {
        const a = (data.activities ?? []).find((x) => x.s === b.dataset.s);
        if (!a) return;
        act(() => { model.state.parent = parentUndid(P(), a.s); }, { text: `${a.t} is back in the plan.`, undo: 'Undo', undoName: `Undo: ${a.t} stays done` }, { from: 'title', back: `${a.t} stays done.` });
        return;
      }
      case 'skip': {
        if (model.visit.skip) return;
        const v = parentView(data.activities ?? [], P(), today, { skip: true, used: model.visit.used });
        if (!v.next || !v.date || !v.freed) return;
        // The line that says so holds its own "Put it back", so nothing else on the page can take it away.
        model.visit.skip = true;
        said = undefined; err = undefined; undoFn = undefined;
        render('[data-fid="unskip"]', true);
        say(`Nothing ${daysBetween(today, v.freed) === 0 ? 'today' : `this ${weekday(v.freed)}`}. ${v.next.t} waits for ${longDate(v.date)}.`);
        return;
      }
      case 'unskip': {
        model.visit.skip = false;
        const a = parentView(data.activities ?? [], P(), today, { used: model.visit.used }).next;
        said = { text: a ? `${a.t} is back on its day.` : 'Put back.' };
        render('[data-fid="skip"]', true);
        say(said.text);
        return;
      }
      /* student */
      case 'done': {
        const p = progress();
        const view = studentView(itemsNow(), p.done, sizing(), today, { later: model.visit.later, spent: !!p.today.length });
        const s = view.top?.sitting;
        if (!s) return;
        const its = s.items;
        const name = its.length > 1 ? `${its.length} lessons` : its[0].t;
        const apply = (on: boolean) => {
          const st = S();
          for (const it of its) {
            if (it.kind === 'lesson') { try { setDone(it.key, on); } catch { /* blocked */ } if (on) undoneHere.delete(it.key); else undoneHere.add(it.key); }
            else st.marks = on ? [...new Set([...st.marks, it.key])] : st.marks.filter((k) => k !== it.key);
            if (on) doneHere.set(it.key, it.t); else doneHere.delete(it.key);
          }
          model.visit.later = false;
        };
        const nx = view.rows[0]?.sitting.items[0]?.t;
        act(() => apply(true), { text: `Done: ${end(name)}${nx ? ` Next: ${end(nx)}` : ''}`, undo: 'Undo', undoName: `Undo: ${name} is not done` }, { from: 'done', undo: () => { apply(false); save(); }, back: `${name} is not done.` });
        return;
      }
      case 'undone': {
        const k = b.dataset.key!;
        const it = planItems().find((i) => i.key === k);
        if (!it) return;
        const apply = (on: boolean) => {
          const st = S();
          if (it.kind === 'lesson') {
            try { setDone(k, on); } catch { /* blocked */ }
            if (on) { undoneHere.delete(k); remarked.add(k); } else undoneHere.add(k);
          } else st.marks = on ? [...new Set([...st.marks, k])] : st.marks.filter((x) => x !== k);
          if (!on) doneHere.delete(k);
        };
        act(() => apply(false), { text: `${it.t} is back in the plan.`, undo: 'Undo', undoName: `Undo: ${it.t} stays done` }, { from: 'title', undo: () => { apply(true); save(); }, back: `${it.t} stays done.` });
        return;
      }
      case 'later': {
        if (model.visit.later) return;
        const p = progress();
        const v = studentView(itemsNow(), p.done, sizing(), today, { later: true });
        const to = v.top?.date;
        model.visit.later = true;
        said = undefined; err = undefined; undoFn = undefined;   // the emptied card says it, and holds its own "Put it back"
        render('[data-fid="unlater"]', true);
        say(to ? `Moved to ${daysBetween(today, to) === 1 ? 'tomorrow' : longDate(to)}.` : 'Moved to your next study day.');
        return;
      }
      case 'unlater': {
        model.visit.later = false;
        const p = progress();
        const top = studentView(itemsNow(), p.done, sizing(), today, { spent: !!p.today.length }).top?.sitting.items[0]?.t;
        said = { text: top ? `${top} is back on today.` : 'Put back.' };
        render('[data-fid="later"]', true);
        say(said.text);
        return;
      }
      /* teacher */
      case 'lost':
        act(() => { const t = T(); t.moved = [...new Set([...t.moved, today])].sort(); }, { text: 'Moved back one class from today. Every later lesson moved with it.' }, { focus: '[data-fid="undo"]', noUndo: true });
        return;
      case 'unlost': {
        const d = b.dataset.d ?? today;
        act(() => { const t = T(); t.moved = t.moved.filter((x) => x !== d); }, { text: 'Put back. Every later lesson moved up one class.' }, { focus: d === today ? '[data-fid="lost"]' : `[data-fid="row-${d}"]`, noUndo: true });
        return;
      }
      case 'addbreak': {
        const from = field('bfrom');
        const to = field('bto') || from;
        if (!isIso(from)) { complain('break-from', 'Give the break a first day.', '[name="bfrom"]'); return; }
        if (!isIso(to) || to < from) { complain('break-to', 'The last day of a break cannot be before its first day.', '[name="bto"]'); return; }
        const label = field('blabel').replace(/[<>]/g, '') || 'No class';
        const next = [...teacherSetup(model.state.teacher, today).breaks, { from, to, label }].sort((a, z) => a.from.localeCompare(z.from));
        const at = next.findIndex((x) => x.from === from && x.to === to && x.label === label);
        for (const n of ['bfrom', 'bto', 'blabel']) { const i = root.querySelector<HTMLInputElement>(`[name="${n}"]`); if (i) i.value = ''; }
        act(() => { T().breaks = next; }, { text: 'Added. Lessons on those days moved to the next class.' }, { focus: `[data-fid="unbreak-${at}"]`, noUndo: true });
        return;
      }
      case 'unbreak':
        act(() => { const t = T(); t.breaks = (t.breaks ?? []).filter((_, i) => i !== Number(b.dataset.i)); }, { text: 'Removed. The plan closed up.' }, { focus: '[name="bfrom"]', noUndo: true });
        return;
    }
  });

  /* ---------- dialogs (native) ---------- */
  function openDialog(id: string) {
    const d = document.getElementById(id) as HTMLDialogElement | null;
    if (d && !d.open) d.showModal();
  }
  /** A press on the dimmed page behind a dialog, not on the dialog's own padding. */
  const outside = (d: HTMLDialogElement, e: MouseEvent) => {
    const r = d.getBoundingClientRect();
    return e.target === d && (e.clientX < r.left || e.clientX > r.right || e.clientY < r.top || e.clientY > r.bottom);
  };
  const choose = document.getElementById('cal-choose') as HTMLDialogElement | null;
  choose?.addEventListener('click', (e) => {
    if (outside(choose, e)) { choose.close(); return; }
    const b = (e.target as HTMLElement).closest<HTMLElement>('[data-act]');
    if (b?.dataset.act === 'close') choose.close();
    if (b?.dataset.act === 'pick' && b.dataset.s) {
      const acts = data.activities ?? [];
      const pick = acts.find((a) => a.s === b.dataset.s);
      const old = parentQueue(acts, P())[0];
      choose.close();
      if (!pick || pick.s === old?.s) { root.querySelector<HTMLElement>('[data-fid="choose"]')?.focus(); return; }
      act(() => { model.state.parent = parentPick(acts, P(), pick.s); model.visit.skip = false; }, { text: `Next: ${end(pick.t)}${old ? ` Then: ${end(old.t)}` : ''}`, undo: 'Put it back', undoName: `Put it back: ${old?.t ?? 'the plan'} comes first again` }, { from: 'choose', back: old ? `${old.t} comes first again.` : 'Put back.' });
    }
  });
  const email = document.getElementById('cal-email') as HTMLDialogElement | null;
  email?.addEventListener('click', (e) => { if ((e.target as HTMLElement).closest('[data-act="close"]') || outside(email, e)) email.close(); });
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

  /* ---------- keep in step: the lesson pages, another tab, Back, "Clear everything", midnight ---------- */
  const reread = () => { model = { state: readState(), visit: model.visit }; said = undefined; err = undefined; undoFn = undefined; refresh(); };
  window.addEventListener(CHANGE_EVENT, () => { if (role === 'student') refresh(); });
  window.addEventListener(CAL_EVENT, reread);
  window.addEventListener('storage', (e) => {
    if (e.key === KEY || e.key === null) reread();
    else if (e.key === PROGRESS_KEY && role === 'student') refresh();
  });
  // Back from a lesson: the browser may show this page from its cache, as it was before the lesson was done.
  window.addEventListener('pageshow', (e) => { if (e.persisted) reread(); });
  document.addEventListener('visibilitychange', () => {
    if (document.hidden) return;
    const now = pinned ? today : todayIso();
    if (now !== today) {
      today = now;
      model.visit = { test: model.visit.test };
      for (const k of [...doneHere.keys()]) doneHere.set(k, '');   // still done, but not done today
      reread();
    }
  });
}
