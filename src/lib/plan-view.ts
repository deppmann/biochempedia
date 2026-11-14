/* Study plans, browser side (2026-11-14). The server half is worker/planner.js.

   One renderer for every place a plan shows: the learner's planner and saved plans (/plan/),
   a teacher's syllabus match (/teach/syllabus/) and the list students open (/teach/list/).
   A plan is plain data from the Worker: sections (weeks, or a syllabus's topics), each with
   lessons and the films, simulations, method films and flashcards picked for them. Showing a
   plan never calls the model.

   Where a learner stands is worked out here, from what this browser already keeps: lessons
   marked done (src/lib/progress.ts, which syncs with a signed-in account) and films watched
   (src/lib/film-progress.ts). Nothing about it is sent anywhere, except the list of lessons
   done when the learner presses "Re-plan from here". */

export interface PlanFilm { key: string; kind: string; sec: number; title: string; href: string }
export interface PlanItem {
  slug: string; why: string; title: string; hook: string; course: string; courseTitle: string; href: string;
  read: number; films: PlanFilm[]; sims: { i: number; title: string }[];
  methods: { slug: string; name: string; sec: number; href: string }[];
  cardCount: number; cardsHref: string; quiz: number; minutes: number;
}
export interface PlanSection { label: string; focus: string; gap: string; items: PlanItem[]; minutes?: number }
export interface Plan { title?: string; summary?: string; sections: PlanSection[]; gaps?: { topic: string; note: string }[]; minutes?: number }

export interface Ref { slug: string; why: string; films: string[]; sims: number[]; methods: string[]; cards: boolean }
export const toRef = (i: PlanItem): Ref => ({ slug: i.slug, why: i.why, films: i.films.map((f) => f.key), sims: i.sims.map((s) => s.i), methods: i.methods.map((m) => m.slug), cards: i.cardCount > 0 });
export const toRefSections = (p: Plan) => p.sections.map((s) => ({ label: s.label, focus: s.focus, gap: s.gap, items: s.items.map(toRef) }));

export const fmtLen = (sec: number) => `${Math.floor(sec / 60)}:${String(Math.round(sec % 60)).padStart(2, '0')}`;
export function fmtMin(m: number) {
  const r = Math.max(0, Math.round(m));
  if (r < 60) return `${r} min`;
  const h = Math.floor(r / 60), mm = r % 60;
  return mm ? `${h} h ${mm} min` : `${h} h`;
}
export const sectionMinutes = (s: PlanSection) => s.items.reduce((n, i) => n + i.minutes, 0);
export const planMinutes = (p: Plan) => p.sections.reduce((n, s) => n + sectionMinutes(s), 0);

type Kids = (Node | string | null | undefined | false)[];
export function el<K extends keyof HTMLElementTagNameMap>(tag: K, props: Record<string, unknown> = {}, ...kids: Kids): HTMLElementTagNameMap[K] {
  const e = document.createElement(tag);
  for (const [k, v] of Object.entries(props)) {
    if (v === undefined || v === null || v === false) continue;
    if (k === 'class') e.className = String(v);
    else if (k.startsWith('data-') || k.startsWith('aria-') || k === 'role' || k === 'for') e.setAttribute(k, String(v));
    else (e as unknown as Record<string, unknown>)[k] = v;
  }
  for (const c of kids) if (c !== null && c !== undefined && c !== false) e.append(c);
  return e;
}

export interface RenderOpts {
  /** Reorder and remove buttons (and, with labels: true, editable section names). */
  editable?: boolean;
  labels?: boolean;
  onChange?: () => void;
  /** Done marks and watched films, for a saved learner plan. */
  done?: (slug: string) => boolean;
  watched?: (key: string) => boolean;
  /** 1-based; that section is marked "This week". */
  currentWeek?: number;
  /** Time per section and in total (learner plans). */
  times?: boolean;
  emptyNote?: string;
}

/** Draws the plan into `host` (replacing what is there). Editing changes `plan` in place, then redraws. */
export function renderPlan(host: HTMLElement, plan: Plan, o: RenderOpts = {}) {
  host.replaceChildren();
  const redraw = () => { renderPlan(host, plan, o); o.onChange?.(); };
  const all = plan.sections.flatMap((s, si) => s.items.map((it, ii) => ({ si, ii, it })));
  const move = (si: number, ii: number, dir: -1 | 1) => {
    const flat = all.findIndex((x) => x.si === si && x.ii === ii);
    const to = all[flat + dir];
    const sec = plan.sections[si];
    const [item] = sec.items.splice(ii, 1);
    if (to && to.si === si) sec.items.splice(ii + dir, 0, item);
    else if (dir === -1 && si > 0) plan.sections[si - 1].items.push(item);
    else if (dir === 1 && si < plan.sections.length - 1) plan.sections[si + 1].items.unshift(item);
    else sec.items.splice(ii, 0, item);
    redraw();
  };
  plan.sections.forEach((s, si) => {
    const mins = sectionMinutes(s);
    const label = o.labels && o.editable
      ? el('input', { type: 'text', class: 'pl-label-input', value: s.label, maxLength: 100, 'aria-label': `Name of part ${si + 1}`, oninput: (e: Event) => { s.label = (e.target as HTMLInputElement).value; o.onChange?.(); } })
      : el('h3', { class: 'pl-label' }, s.label);
    const doneHere = o.done ? s.items.filter((i) => o.done!(i.slug)).length : 0;
    const head = el('header', { class: 'pl-sec-head' },
      label,
      s.focus ? el('span', { class: 'pl-focus' }, s.focus) : null,
      o.currentWeek === si + 1 ? el('span', { class: 'pl-pill now' }, 'This week') : null,
      o.done && s.items.length ? el('span', { class: 'pl-pill' + (doneHere === s.items.length ? ' good' : '') }, `${doneHere} of ${s.items.length} done`) : null,
      o.times && mins ? el('span', { class: 'pl-time' }, `about ${fmtMin(mins)}`) : null,
    );
    const list = el('ol', { class: 'pl-items' });
    s.items.forEach((it, ii) => {
      const isDone = o.done?.(it.slug) ?? false;
      const res = el('ul', { class: 'pl-res', 'aria-label': 'What to use' });
      for (const f of it.films) {
        const seen = o.watched?.(f.key);
        res.append(el('li', {}, el('a', { href: f.href, class: 'pl-chip film' + (seen ? ' seen' : '') }, el('span', { 'aria-hidden': 'true' }, seen ? '✓ ' : '▶ '), `${f.title} `, el('span', { class: 'pl-len' }, fmtLen(f.sec)), seen ? el('span', { class: 'visually-hidden' }, ' (watched)') : null)));
      }
      for (const m of it.methods) res.append(el('li', {}, el('a', { href: m.href, class: 'pl-chip method' }, el('span', { 'aria-hidden': 'true' }, '▶ '), `Method: ${m.name} `, el('span', { class: 'pl-len' }, fmtLen(m.sec)))));
      for (const sm of it.sims) res.append(el('li', {}, el('a', { href: it.href, class: 'pl-chip sim' }, el('span', { 'aria-hidden': 'true' }, '◆ '), `Simulation: ${sm.title}`)));
      if (it.cardCount) res.append(el('li', {}, el('a', { href: it.cardsHref, class: 'pl-chip cards' }, el('span', { 'aria-hidden': 'true' }, '▤ '), `Flashcards (${it.cardCount})`)));
      const tools = o.editable ? el('div', { class: 'pl-tools' },
        el('button', { type: 'button', class: 'pl-tool', 'aria-label': `Move ${it.title} earlier`, title: 'Earlier', onclick: () => move(si, ii, -1), disabled: si === 0 && ii === 0 }, '↑'),
        el('button', { type: 'button', class: 'pl-tool', 'aria-label': `Move ${it.title} later`, title: 'Later', onclick: () => move(si, ii, 1), disabled: si === plan.sections.length - 1 && ii === s.items.length - 1 }, '↓'),
        el('button', { type: 'button', class: 'pl-tool rm', 'aria-label': `Remove ${it.title}`, title: 'Remove', onclick: () => { s.items.splice(ii, 1); redraw(); } }, '✕'),
      ) : null;
      list.append(el('li', { class: 'pl-item' + (isDone ? ' done' : '') },
        el('div', { class: 'pl-main' },
          el('p', { class: 'pl-title-row' },
            el('a', { href: it.href, class: 'pl-title' }, it.title),
            isDone ? el('span', { class: 'pl-pill good' }, 'Done') : null),
          el('p', { class: 'pl-meta' }, `${it.courseTitle} · read ${it.read} min${o.times ? ` · about ${fmtMin(it.minutes)} in all` : ''}`),
          it.why ? el('p', { class: 'pl-why' }, it.why) : null,
          res.childElementCount ? res : null),
        tools));
    });
    host.append(el('section', { class: 'pl-sec' + (o.currentWeek === si + 1 ? ' now' : '') },
      head,
      s.gap ? el('p', { class: 'pl-gap' }, el('strong', {}, 'Gap: '), s.gap) : null,
      s.items.length ? list : (!s.gap ? el('p', { class: 'pl-empty' }, o.emptyNote ?? 'Nothing here now.') : null)));
  });
  if (plan.gaps?.length) {
    host.append(el('section', { class: 'pl-sec pl-gaps' },
      el('h3', { class: 'pl-label' }, 'Not on the site yet'),
      el('ul', {}, ...plan.gaps.map((g) => el('li', {}, el('strong', {}, g.topic), g.note ? ` — ${g.note}` : '')))));
  }
}

// ---- where a learner stands -------------------------------------------------------------------
export interface Standing { week: number; weeks: number; open: { week: number; n: number }[]; ahead: number; done: number; total: number }
const WEEK_MS = 7 * 86_400_000;

export function standing(plan: Plan, start: number, done: (slug: string) => boolean, now = Date.now()): Standing {
  const weeks = plan.sections.length;
  const week = Math.max(1, Math.floor((now - start) / WEEK_MS) + 1);
  const open: { week: number; n: number }[] = [];
  let ahead = 0, d = 0, total = 0;
  plan.sections.forEach((s, i) => {
    const n = s.items.filter((it) => !done(it.slug)).length;
    total += s.items.length; d += s.items.length - n;
    if (i + 1 < week && n) open.push({ week: i + 1, n });
    if (i + 1 > week) ahead += s.items.length - n;
  });
  return { week, weeks, open, ahead, done: d, total };
}

/** Plain, calm wording: what is open, never how late. */
export function standingText(s: Standing): string[] {
  const lines: string[] = [];
  if (s.total && s.done === s.total) return ['Every lesson in this plan is marked done.'];
  if (s.week > s.weeks) lines.push(`The plan's ${s.weeks} week${s.weeks === 1 ? ' is' : 's are'} behind you.`);
  else lines.push(`This is week ${s.week} of ${s.weeks}.`);
  if (s.open.length) {
    const parts = s.open.map((o, i) => `${o.n} ${i === 0 ? (o.n === 1 ? 'lesson' : 'lessons') : ''} from week ${o.week}`.replace(/\s+/g, ' '));
    const list = parts.length > 1 ? `${parts.slice(0, -1).join(', ')} and ${parts.at(-1)}` : parts[0];
    const n = s.open.reduce((a, o) => a + o.n, 0);
    lines.push(`${list.charAt(0).toUpperCase()}${list.slice(1)} ${n === 1 ? 'is' : 'are'} still open.`);
  } else if (s.week <= s.weeks) lines.push('Everything from earlier weeks is done.');
  if (s.ahead) lines.push(`You have also done ${s.ahead} lesson${s.ahead === 1 ? '' : 's'} from later weeks.`);
  return lines;
}

// ---- the planner's switch -------------------------------------------------------------------
export interface Status { on: boolean; saved: boolean; capped?: 'day' | 'month'; maxGoal?: number; maxKnown?: number; maxWeeks?: number; maxHours?: number; maxText?: number; maxPdfBytes?: number; maxPdfPages?: number; maxPlans?: number; perDay?: number; mock?: boolean }
let statusMemo: Promise<Status> | undefined;
export function plannerStatus(): Promise<Status> {
  statusMemo ??= fetch('/api/plan/status', { credentials: 'same-origin' })
    .then(async (r) => { const d = await r.json().catch(() => ({})); return { ...d, on: r.ok && !!d.on, saved: !!d.saved }; })
    .catch(() => ({ on: false, saved: false }));
  return statusMemo;
}
export const cappedText = (c?: string) => c === 'month'
  ? 'The planner has used its allowance for this month and will be back next month. Saved plans still work.'
  : 'The planner has used its allowance for today and will be back tomorrow. Saved plans still work.';

/** Calls the API like src/lib/classroom.ts does. */
export async function planApi<T = Record<string, unknown>>(path: string, body?: unknown, method = body === undefined ? 'GET' : 'POST'): Promise<{ ok: boolean; status: number; data: T & { error?: string; capped?: string; signin?: boolean } }> {
  try {
    const r = await fetch(path, { method, credentials: 'same-origin', headers: method === 'GET' ? {} : { 'Content-Type': 'application/json' }, body: method === 'GET' ? undefined : JSON.stringify(body ?? {}) });
    const data = await r.json().catch(() => ({}));
    return { ok: r.ok, status: r.status, data };
  } catch {
    return { ok: false, status: 0, data: { error: 'Could not reach the site. Check your connection and try again.' } as T & { error: string } };
  }
}

/** While a plan is being made (10 to 60 seconds): steps that advance on a timer, so the wait is visible. */
export function progressSteps(host: HTMLElement, steps: string[], note = 'Usually 10 to 30 seconds; a long plan can take about a minute.') {
  host.replaceChildren();
  const items = steps.map((s) => el('li', {}, s));
  const bar = el('div', { class: 'pl-bar', role: 'progressbar', 'aria-label': 'Making the plan', 'aria-valuemin': 0, 'aria-valuemax': 100 }, el('span', {}));
  host.append(bar, el('ol', { class: 'pl-steps' }, ...items), el('p', { class: 'pl-hint' }, note));
  host.hidden = false;
  const t0 = Date.now();
  const tick = () => {
    const sec = (Date.now() - t0) / 1000;
    const pct = Math.min(95, 100 * (1 - Math.exp(-sec / 18)));
    (bar.firstElementChild as HTMLElement).style.width = `${pct}%`;
    bar.setAttribute('aria-valuenow', String(Math.round(pct)));
    const cur = Math.min(items.length - 1, Math.floor(sec / 6));
    items.forEach((li, k) => { li.className = k < cur ? 'done' : k === cur ? 'now' : ''; });
  };
  tick();
  const timer = setInterval(tick, 500);
  return () => { clearInterval(timer); host.hidden = true; };
}
