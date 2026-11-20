/* The film library in the browser (2026-11-20). The page (src/pages/films/index.astro) works without
   this: it lists a film to start with, the level links and the first 60 cards. This makes the page
   answer at once when the visitor turns a control.

   What costs nothing: a level key redraws the strip and the count from data already in the page.
   What is fetched, once, when first needed: /films/list.json (the cards of every film) on the first
   press inside the controls, and /films/ideas.json (the questions people ask, for search) when the
   search box is first used.

   Motion happens only in answer to the visitor: the strip re-lays, and cards that stay in the list
   slide from where they were to where they now are. None of it runs under reduced motion.
   Nothing here is stored. Reading: the watched record (film-progress.ts) and, for the film to start
   with, the level in stemhop:prefs:v1 when the visitor has set one elsewhere on the site.

   performance.mark('fl-tap' | 'fl-drawn' | 'fl-settled') are left in for measuring. */
import { cardHTML, hoverPreviews, liveMarks, markCards, type FilmList, type ListFilm } from './film-cards';
import { loadFilms, keepWatching, onFilmsChange, resumeHref } from './film-progress';
import { filmStrip, type StripFilm } from './film-strip';
import { BUDGETS, FIELDS, about, clock, filmsWord, fit, isDefault, readView, runSentence, runnable, select, viewQuery, type Ideas, type View } from './film-view';

const PAGE = 60;
const esc = (s: string) => s.replace(/[&<>"]/g, (c) => ({ '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;' })[c]!);

export function library(): void {
  const root = document.querySelector<HTMLElement>('[data-fl]');
  if (!root) return;
  const $ = <T extends HTMLElement>(sel: string) => root.querySelector<T>(sel)!;
  const still = window.matchMedia('(prefers-reduced-motion: reduce)');
  const total = Number(root.dataset.total);
  hoverPreviews(root);
  liveMarks(root);

  const form = $<HTMLFormElement>('[data-fl-controls]');
  const listEl = $('[data-fl-list]');
  const status = $('[data-fl-status]');
  const seen = $('[data-fl-seen]');
  const none = $('[data-fl-none]');
  const moreRow = $('[data-fl-more-row]');
  const rest = $('[data-fl-rest]');
  const cap = $('[data-fl-strip-cap]');
  const capAll = cap.textContent ?? '';
  const field = (n: string) => form.elements.namedItem(n) as HTMLInputElement | HTMLSelectElement;

  /* ---- the strip: every film's level and length is in the page (3 characters a film). */
  const stripEl = $('[data-fl-strip]');
  const keys = [...root.querySelectorAll<HTMLAnchorElement>('[data-fl-keys] a')];
  const levelKeys = keys.map((k) => k.dataset.level!).filter(Boolean);
  const stripFilms: StripFilm[] = [];
  const code = stripEl.dataset.d ?? '';
  for (let i = 0; i + 3 <= code.length; i += 3) stripFilms.push({ level: levelKeys[Number(code[i])] ?? '', d: parseInt(code.slice(i + 1, i + 3), 36) });
  const canvas = stripEl.querySelector('canvas')!;
  canvas.hidden = false;
  stripEl.classList.add('is-drawn');
  const strip = filmStrip(canvas, stripFilms);

  /* ---- the full list, when first needed */
  let list: FilmList | null = null;
  let loading: Promise<FilmList | null> | null = null;
  let ideas: Ideas | null = null;
  let ideasLoading: Promise<void> | null = null;
  const ensure = () => (loading ??= fetch('/films/list.json')
    .then((r) => { if (!r.ok) throw new Error(String(r.status)); return r.json() as Promise<FilmList>; })
    .then((d) => (list = d))
    .catch(() => { loading = null; status.textContent = 'Could not load the full list. Each level’s page has every film.'; return null; }));
  const ensureIdeas = () => (ideasLoading ??= fetch('/films/ideas.json')
    .then((r) => (r.ok ? r.json() : null))
    .then((d) => { if (d) { ideas = d as Ideas; if (view.q) void render(false); } })
    .catch(() => { ideasLoading = null; }));
  root.querySelector('.fl-deck')!.addEventListener('pointerdown', () => void ensure(), { once: true, passive: true });
  root.querySelector('.fl-deck')!.addEventListener('focusin', () => void ensure(), { once: true });
  field('q').addEventListener('focus', () => void ensureIdeas(), { once: true });

  /* ---- the view */
  let view: View = readView(location.search);
  if (view.level && !levelKeys.includes(view.level)) view.level = '';
  let limit = PAGE;
  let budget = 0;
  const toForm = () => { for (const f of FIELDS) field(f).value = view[f]; if (view.course || view.kind) $<HTMLDetailsElement>('[data-fl-fold]').open = true; };

  /* The level keys become one group of radios: arrows move and choose, as radios do. */
  const nav = $('[data-fl-keys]');
  nav.setAttribute('role', 'radiogroup');
  const hex = root.querySelector<HTMLElement>('[data-fl-hex]');
  const paintKeys = () => {
    for (const k of keys) {
      const on = (k.dataset.level ?? '') === view.level;
      k.setAttribute('role', 'radio');
      k.setAttribute('aria-checked', String(on));
      k.tabIndex = on ? 0 : -1;
      k.classList.toggle('is-on', on);
      if (on && hex && hex.parentElement !== k) k.prepend(hex);
    }
  };
  const chooseLevel = (level: string, focus = false) => {
    performance.mark('fl-tap');
    view.level = level;
    // A course belongs to one level: choosing another level lets go of it.
    if (view.course && list && list.films.find((f) => f.c === view.course)?.s !== level) view.course = '';
    limit = PAGE;
    toForm();
    paintKeys();
    if (focus) keys.find((k) => k.dataset.level === level)?.focus();
    commit(true);
  };
  for (const k of keys) {
    k.addEventListener('click', (e) => {
      if (e.metaKey || e.ctrlKey || e.shiftKey || e.altKey) return; // a new tab still gets the level's own page
      e.preventDefault();
      chooseLevel(k.dataset.level ?? '');
    });
  }
  nav.addEventListener('keydown', (e) => {
    const i = keys.indexOf(document.activeElement as HTMLAnchorElement);
    if (i === -1) return;
    const to = e.key === 'ArrowRight' || e.key === 'ArrowDown' ? (i + 1) % keys.length
      : e.key === 'ArrowLeft' || e.key === 'ArrowUp' ? (i - 1 + keys.length) % keys.length
      : e.key === 'Home' ? 0 : e.key === 'End' ? keys.length - 1 : e.key === ' ' ? i : -1;
    if (to === -1) return;
    e.preventDefault();
    chooseLevel(keys[to].dataset.level ?? '', true);
  });

  /* ---- drawing */
  const levelOnly = () => !view.q && !view.course && !view.kind;
  const drawStrip = (current: ListFilm[] | null) => {
    if (budget && current && list) {
      const run = fit(runnable(current, view), budget, loadFilms());
      strip.set({ on: run.films.map((f) => f.i), budget, numbered: true });
      cap.textContent = 'These films in true minutes, in the order they play. The line is your time.';
      return run;
    }
    if (isDefault({ ...view, sort: 'course' })) { strip.set({ on: null }); cap.textContent = capAll; return null; }
    const on = current ? current.map((f) => f.i) : stripFilms.map((f, i) => (f.level === view.level ? i : -1)).filter((i) => i !== -1);
    strip.set({ on });
    cap.textContent = `${filmsWord(on.length)} brought forward, with the rest of the ${total.toLocaleString('en-US')} beneath.`;
    return null;
  };
  const say = (n: number, secs: number) => { status.textContent = n ? `${filmsWord(n)}, ${about(secs)}.` : 'No films.'; };

  const groupHTML = (films: ListFilm[], d: FilmList) => {
    const out: string[] = [];
    let cur = '';
    let open = false;
    for (const f of films) {
      const key = f.c || 'methods';
      if (key !== cur) {
        if (open) out.push('</ul></section>');
        cur = key;
        open = true;
        const title = f.c ? d.courses[f.c] : 'Methods library';
        const href = f.c ? `/courses/${f.c}/` : '/methods/';
        const level = f.s ? `<span class="n lv-${esc(f.s)}"><span class="fl-chip"></span>${esc(d.levels[f.s] ?? '')}</span>` : '';
        const play = f.c ? `<a class="play-link" href="/films/play/${esc(f.c)}/">Play these in order</a>` : '';
        out.push(`<section class="course"><div class="course-h"><h2><a class="ch" href="${href}">${esc(title)}</a></h2>${level}${play}</div><ul class="grid in-course">`);
      }
      out.push(cardHTML(f, d));
    }
    if (open) out.push('</ul></section>');
    return out.join('');
  };

  const cardRects = () => {
    const m = new Map<string, DOMRect>();
    const vh = window.innerHeight;
    for (const li of listEl.querySelectorAll<HTMLElement>('li.fc[data-f]')) {
      const r = li.getBoundingClientRect();
      if (r.bottom > -200 && r.top < vh + 200) m.set(li.dataset.f!, r);
    }
    return m;
  };
  /* Cards that stay in the list slide from where they were; new ones fade in. On-screen cards only. */
  const slide = (before: Map<string, DOMRect>) => {
    if (still.matches || !('animate' in Element.prototype)) { performance.mark('fl-settled'); return; }
    const vh = window.innerHeight;
    let last: Animation | null = null;
    let k = 0;
    for (const li of listEl.querySelectorAll<HTMLElement>('li.fc[data-f]')) {
      const r = li.getBoundingClientRect();
      if (r.top > vh + 100) break;
      if (r.bottom < -100) continue;
      const was = before.get(li.dataset.f!);
      const delay = Math.min(k++ * 14, 160);
      last = was
        ? li.animate([{ transform: `translate(${was.left - r.left}px, ${was.top - r.top}px)` }, { transform: 'none' }], { duration: 320, delay, easing: 'cubic-bezier(.2,.7,.2,1)', fill: 'backwards' })
        : li.animate([{ opacity: 0, transform: 'translateY(8px)' }, { opacity: 1, transform: 'none' }], { duration: 240, delay, easing: 'ease-out', fill: 'backwards' });
    }
    if (last) last.finished.then(() => performance.mark('fl-settled'), () => {}); else performance.mark('fl-settled');
  };

  let drawn = 0;
  async function render(animate: boolean): Promise<void> {
    const mine = ++drawn;
    paintKeys();
    // What can be said before the list arrives: a level's size is in the page.
    if (!list && levelOnly()) {
      const idx = stripFilms.map((f, i) => i).filter((i) => !view.level || stripFilms[i].level === view.level);
      say(idx.length, idx.reduce((s, i) => s + stripFilms[i].d, 0));
      if (!budget) drawStrip(null);
    }
    if (!list && isDefault(view) && limit === PAGE && !budget) { paintRun(null); return; } // the page as served
    const d = list ?? await ensure();
    if (!d || mine !== drawn) return;
    view = { ...readView(viewQuery(view), d) };
    const current = select(d, view, ideas);
    const before = animate ? cardRects() : new Map<string, DOMRect>();
    say(current.length, current.reduce((s, f) => s + f.d, 0));
    const run = drawStrip(current);
    paintRun(current, run);
    none.hidden = current.length > 0;
    rest.hidden = true;
    const shown = current.slice(0, limit);
    listEl.innerHTML = view.sort === 'course' && !view.q ? groupHTML(shown, d) : `<ul class="grid">${shown.map((f) => cardHTML(f, d)).join('')}</ul>`;
    if (view.level && view.sort === 'course' && levelOnly()) {
      const pic = listEl.querySelector('li.fc .fc-pic');
      if (pic) { const s = document.createElement('span'); s.className = 'fc-start'; s.textContent = 'Start here'; pic.append(s); }
    }
    markCards(listEl);
    moreRow.hidden = current.length <= limit;
    performance.mark('fl-drawn');
    if (animate) slide(before); else performance.mark('fl-settled');
  }

  /* ---- play them in order, or for a while */
  const runBox = $('[data-fl-run]');
  const runSum = $('[data-fl-run-sum]');
  const runText = $('[data-fl-run-text]');
  const play = $<HTMLAnchorElement>('[data-fl-play]');
  const startBtn = $<HTMLAnchorElement>('[data-fl-run-start]');
  const radios = [...runBox.querySelectorAll<HTMLInputElement>('input[name="fl-t"]')];
  runBox.hidden = false;
  function paintRun(current: ListFilm[] | null, run?: ReturnType<typeof fit> | null): void {
    const q = viewQuery(view);
    // One course, unsearched by level: its own play-in-order page, as before.
    play.href = view.course ? `/films/play/${encodeURIComponent(view.course)}/${viewQuery({ ...view, level: '', course: '', sort: 'course' })}` : `/films/run/${q}`;
    if (!budget || !current) { runSum.hidden = true; return; }
    runSum.hidden = false;
    if (!run || !run.films.length) {
      runText.textContent = 'Nothing in this view plays in a row: scientist profiles and method films open on their own pages.';
      startBtn.hidden = true;
      return;
    }
    startBtn.hidden = false;
    startBtn.href = `/films/run/${viewQuery(view, { t: String(budget) })}`;
    runText.innerHTML = `${esc(runSentence(run.films, run.seconds))}<ol class="fl-run-list">${run.films.map((f) => `<li>${esc(f.t)} <span class="fc-len-t">${clock(f.d)}</span></li>`).join('')}</ol>`;
  }
  for (const r of radios) {
    r.addEventListener('change', () => { performance.mark('fl-tap'); budget = BUDGETS.includes(Number(r.value)) ? Number(r.value) : 0; void render(false); });
  }
  $('[data-fl-run-clear]').addEventListener('click', () => {
    budget = 0;
    for (const r of radios) r.checked = false;
    radios[0]?.focus();
    void render(false);
  });

  /* ---- changes */
  function commit(push: boolean): void {
    const url = `${location.pathname}${viewQuery(view)}`;
    if (url !== location.pathname + location.search) history[push ? 'pushState' : 'replaceState'](null, '', url);
    void render(true);
    startCard();
  }
  const fromForm = () => { for (const f of FIELDS) if (f !== 'level') view[f] = field(f).value.trim(); limit = PAGE; };
  let typing = 0;
  form.addEventListener('input', (e) => {
    if ((e.target as HTMLElement).getAttribute('name') !== 'q') return;
    window.clearTimeout(typing);
    typing = window.setTimeout(() => { performance.mark('fl-tap'); fromForm(); commit(false); }, 140);
  });
  form.addEventListener('change', (e) => {
    if ((e.target as HTMLElement).getAttribute('name') === 'q') return;
    performance.mark('fl-tap');
    fromForm();
    if (view.course && list) view.level = list.films.find((f) => f.c === view.course)?.s ?? view.level;
    commit(true);
  });
  form.addEventListener('submit', (e) => { e.preventDefault(); window.clearTimeout(typing); fromForm(); commit(true); });
  $('[data-fl-more]').addEventListener('click', () => {
    const had = listEl.querySelectorAll('li.fc').length;
    limit += PAGE;
    void render(false).then(() => listEl.querySelectorAll<HTMLAnchorElement>('li.fc > a')[had]?.focus());
  });
  $('[data-fl-clear]').addEventListener('click', () => { view = readView(''); limit = PAGE; toForm(); commit(true); field('q').focus(); });
  window.addEventListener('popstate', () => { view = readView(location.search, list ?? undefined); limit = PAGE; toForm(); void render(false); startCard(); });

  /* ---- a film to start with, or where you stopped */
  type StartPick = { s: string; t: string; h: string; o: string; d: string; m: string; x: string };
  const startEl = $('[data-fl-start]');
  const pool: StartPick[] = JSON.parse(startEl.dataset.pool ?? '[]');
  const surprise = $<HTMLButtonElement>('[data-fl-surprise]');
  const part = (k: string) => startEl.querySelector<HTMLElement>(`[data-fl-start-${k}]`)!;
  let shownPick: StartPick | null = null;
  let stoppedDismissed = false;
  const prefLevel = (): string => {
    try {
      const p = JSON.parse(window.localStorage.getItem('stemhop:prefs:v1') ?? 'null');
      return p && typeof p.level === 'string' && levelKeys.includes(p.level) ? p.level : '';
    } catch { return ''; }
  };
  const poolFor = () => {
    const level = view.level || prefLevel();
    const mine = pool.filter((p) => (level ? p.s === level : p.s !== 'ages-5-10'));
    return mine.length ? mine : pool;
  };
  const fill = (k: { kicker: string; title: string; href: string; poster: string; meta: string; len: string; line: string; go: string }) => {
    part('k').textContent = k.kicker;
    part('t').textContent = k.title;
    startEl.querySelectorAll<HTMLAnchorElement>('[data-fl-start-link]').forEach((a) => (a.href = k.href));
    const img = part('img') as HTMLImageElement;
    if (img.getAttribute('src') !== k.poster) img.src = k.poster;
    part('m').textContent = k.meta;
    part('d').textContent = k.len;
    part('x').textContent = k.line;
    part('watch').textContent = k.go;
  };
  const showPick = (p: StartPick) => { shownPick = p; fill({ kicker: 'A film to start with', title: p.t, href: p.h, poster: p.o, meta: p.m, len: p.d, line: p.x, go: 'Watch' }); };
  function startCard(): void {
    const r = loadFilms();
    const film = stoppedDismissed ? null : keepWatching(r);
    const q = stoppedDismissed ? undefined : Object.entries(r.q).sort((a, b) => b[1].at - a[1].at)[0];
    if (q && q[1].title && (!film || q[1].at >= film.at)) {
      const [course, s] = q;
      fill({ kicker: 'Where you stopped', title: `${s.courseTitle ?? 'Your films'}, in order`, href: `/films/play/${encodeURIComponent(course)}/`, poster: s.poster ?? '', meta: 'Up next', len: s.title!, line: s.t > 4 ? `You stopped at ${clock(s.t)}.` : '', go: 'Carry on' });
      return;
    }
    if (film) {
      fill({ kicker: 'Where you stopped', title: film.title, href: resumeHref(film), poster: film.poster, meta: film.course ?? 'Film', len: clock(film.d), line: `You stopped at ${clock(film.t)} of ${clock(film.d)}.`, go: `Pick up at ${clock(film.t)}` });
      return;
    }
    const mine = poolFor();
    // Keep the film the page was served with unless a level (chosen here, or set on this device) asks for another.
    if (shownPick && mine.includes(shownPick)) return;
    if (!shownPick && !view.level && !prefLevel()) { shownPick = pool.find((p) => p.h === part('t').getAttribute('href')) ?? null; return; }
    showPick(mine[0]);
  }
  surprise.hidden = pool.length < 2;
  surprise.addEventListener('click', () => {
    stoppedDismissed = true;
    const mine = poolFor().filter((p) => p !== shownPick);
    if (mine.length) showPick(mine[Math.floor(Math.random() * mine.length)]);
  });

  /* ---- the record: said only once there is something to say */
  onFilmsChange(() => {
    const n = Object.keys(loadFilms().w).length;
    seen.textContent = n ? `${filmsWord(n)} watched on this device.` : '';
    seen.hidden = n === 0;
  });

  form.hidden = false;
  toForm();
  startCard();
  void render(false);
}
