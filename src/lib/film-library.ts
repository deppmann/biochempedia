/* The film library in the browser (2026-11-20). The page (src/pages/films/index.astro) works without
   this: it lists a film to start with, the level links and the first 60 cards. This makes the page
   answer at once when the visitor turns a control.

   What costs nothing: a level key redraws the strip and the count from data already in the page.
   What is fetched, once, when first needed: /films/list.json (the cards of every film) on the first
   press inside the controls, and /films/ideas.json (the questions people ask, for search) when the
   search box is first used.

   The gallery opens on a stack per course (2026-11-21). The stacks are in the page; opening one sets
   the view's course, and its films fly out of the stack. "All courses" brings the stacks back.

   Motion: the strip re-lays; cards that stay in the list slide from where they were to where they
   now are; a stack's films fly out of it; and the stacks deal themselves out once, the first time
   the gallery scrolls into view. None of it runs under reduced motion.
   Nothing here is stored. Reading: the watched record (film-progress.ts) and, for the film to start
   with, the level in stemhop:prefs:v1 when the visitor has set one elsewhere on the site.

   performance.mark('fl-tap' | 'fl-drawn' | 'fl-settled') are left in for measuring. */
import { cardHTML, hoverPreviews, liveMarks, markCards, type FilmList, type ListFilm } from './film-cards';
import { loadFilms, keepWatching, onFilmsChange, resumeHref } from './film-progress';
import { filmStrip, type StripFilm } from './film-strip';
import { readPrefs } from './prefs';
import { BUDGETS, FIELDS, about, clock, filmsWord, fit, isDefault, loadIdeas, readView, runQueue, runSentence, select, viewQuery, type Ideas, type View } from './film-view';

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
  const wait = $('[data-fl-wait]');
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
    .catch(() => { loading = null; return null; }));
  const ensureIdeas = () => (ideasLoading ??= loadIdeas().then((d) => {
    if (d) { ideas = d; if (view.q) void render(false); } else ideasLoading = null;
  }));
  root.querySelector('.fl-deck')!.addEventListener('pointerdown', () => void ensure(), { once: true, passive: true });
  root.querySelector('.fl-deck')!.addEventListener('focusin', () => void ensure(), { once: true });
  listEl.addEventListener('pointerover', () => void ensure(), { once: true, passive: true });
  listEl.addEventListener('focusin', () => void ensure(), { once: true });
  field('q').addEventListener('focus', () => void ensureIdeas(), { once: true });

  /* ---- the view */
  let view: View = readView(location.search);
  if (view.level && !levelKeys.includes(view.level)) view.level = '';
  let limit = Math.max(PAGE, Number(history.state?.limit) || PAGE);
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
  const chooseLevel = (level: string, focus = false, push = true) => {
    performance.mark('fl-tap');
    view.level = level;
    // A level key asks for the level: it lets go of an open course (and of the methods stack).
    view.course = '';
    if (view.kind === 'method') view.kind = '';
    limit = PAGE;
    toForm();
    paintKeys();
    if (focus) keys.find((k) => k.dataset.level === level)?.focus();
    commit(push);
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
    // Arrowing through the keys is one visit to them: Back should not replay every key passed.
    chooseLevel(keys[to].dataset.level ?? '', true, false);
  });

  /* ---- drawing */
  const levelOnly = () => !view.q && !view.course && !view.kind;
  const drawStrip = (current: ListFilm[] | null) => {
    if (budget && current && list) {
      const run = fit(runQueue(list, view, ideas), budget, loadFilms());
      strip.set({ on: run.films.map((f) => f.i), budget, numbered: true });
      cap.textContent = `Your ${budget} minutes, film by film. The line marks ${budget} minutes.`;
      return run;
    }
    if (isDefault({ ...view, sort: 'course' })) { strip.set({ on: null }); cap.textContent = capAll; return null; }
    const on = current ? current.map((f) => f.i) : stripFilms.map((f, i) => (f.level === view.level ? i : -1)).filter((i) => i !== -1);
    if (!on.length) { strip.set({ on: null }); cap.textContent = capAll; return null; }
    strip.set({ on });
    const what = levelOnly() && view.level ? `${keys.find((k) => k.dataset.level === view.level)?.querySelector('.fl-key-t')?.textContent ?? ''}: ` : '';
    cap.textContent = `${what}${on.length.toLocaleString('en-US')} of the library’s ${filmsWord(total)}.`;
    return null;
  };
  // One sentence per change, and only when it changes (the same words written twice are read twice).
  const say = (n: number, secs: number) => {
    const text = n ? `${filmsWord(n)}, ${about(secs)}.` : 'No film matches that.';
    if (status.textContent !== text) status.textContent = text;
  };

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
  const slide = (before: Map<string, DOMRect>, out: DOMRect | null = null) => {
    if (still.matches || !('animate' in Element.prototype)) { performance.mark('fl-settled'); return; }
    if (out) {
      // Out of a stack: each card starts as the stack's top sheet and lands in its place, one after another.
      const head = listEl.querySelector<HTMLElement>('.course-h, .fl-back');
      head?.animate([{ opacity: 0 }, { opacity: 1 }], { duration: 300, easing: 'ease-out' });
      const vh = window.innerHeight;
      let last: Animation | null = null;
      let k = 0;
      for (const li of listEl.querySelectorAll<HTMLElement>('li.fc[data-f]')) {
        const r = li.getBoundingClientRect();
        if (r.top > vh + 100) break;
        const pic = li.querySelector('.fc-pic')?.getBoundingClientRect() ?? r;
        const s = Math.min(1, out.width / pic.width);
        const turn = ((k * 37) % 9) - 4;
        li.style.zIndex = String(200 - k);
        const a = li.animate([
          { transformOrigin: '0 0', transform: `translate(${out.left - pic.left}px, ${out.top - pic.top}px) scale(${s}) rotate(${turn}deg)`, opacity: 0 },
          { transformOrigin: '0 0', opacity: 1, offset: 0.2 },
          { transformOrigin: '0 0', transform: 'none', opacity: 1 },
        ], { duration: 460, delay: Math.min(k * 28, 560), easing: 'cubic-bezier(.2,.7,.2,1)', fill: 'backwards' });
        a.finished.then(() => { li.style.zIndex = ''; }, () => {});
        last = a;
        k++;
      }
      if (last) last.finished.then(() => performance.mark('fl-settled'), () => {}); else performance.mark('fl-settled');
      return;
    }
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

  /* Posters are 35 to 70 KB each and there is one size of them. The browser's own lazy loading reaches
     two or three screens ahead, which on a phone is twenty posters for one tap; this asks for a poster
     when its card is within half a screen. */
  const posters = new IntersectionObserver((entries) => {
    for (const e of entries) {
      if (!e.isIntersecting) continue;
      const img = e.target as HTMLImageElement;
      if (img.dataset.src) { img.src = img.dataset.src; delete img.dataset.src; }
      posters.unobserve(img);
    }
  }, { rootMargin: '50% 0px' });

  // The cards the page was served with get the same rule, at once: otherwise the browser fetches some
  // seventeen posters for cards a screen and a half down, ahead of the list a level tap is waiting for.
  for (const img of listEl.querySelectorAll<HTMLImageElement>('img[loading="lazy"]')) {
    if (img.complete && img.naturalWidth) continue;
    img.dataset.src = img.getAttribute('src') ?? '';
    img.removeAttribute('src');
    img.removeAttribute('loading');
    posters.observe(img);
  }

  /* ---- the stacks: one per course, as the page was served */
  const shelf = $('[data-fl-shelf]');
  const stackEls = [...shelf.querySelectorAll<HTMLElement>('li.fs')];
  const stackCount = (level: string) => stackEls.filter((li) => !level || li.dataset.level === level).length;
  // A level with one course has nothing to choose between: its films are listed, as before.
  const stacksOn = () => !view.q && !view.course && !view.kind && view.sort === 'course' && stackCount(view.level) > 1;
  const moving = () => !still.matches && 'animate' in Element.prototype;
  const EASE = 'cubic-bezier(.2,.7,.2,1)';
  let backLevel = '';
  let origin: { x: number; y: number; w: number; h: number } | null = null; // the stack just opened, in page coordinates
  let closed = ''; // the stack just closed
  let dealt = false;
  /* The stacks leave one pile and land in their places. */
  const deal = () => {
    dealt = true;
    if (!moving()) return;
    const tiles = stackEls.filter((li) => !li.hidden);
    const box = shelf.querySelector('[data-fl-stacks]')!.getBoundingClientRect();
    const first = tiles[0]?.getBoundingClientRect();
    if (!first) return;
    const from = { x: box.left + box.width / 2 - first.width / 2, y: first.top };
    tiles.forEach((li, k) => {
      const r = li.getBoundingClientRect();
      if (r.top > window.innerHeight + 100) return;
      const turn = ((k * 37) % 13) - 6;
      li.style.zIndex = String(tiles.length - k);
      li.animate([
        { transform: `translate(${from.x - r.left}px, ${from.y - r.top}px) rotate(${turn}deg) scale(.86)`, opacity: 0 },
        { opacity: 1, offset: 0.25 },
        { transform: 'none', opacity: 1 },
      ], { duration: 520, delay: 60 + k * 45, easing: EASE, fill: 'backwards' }).finished.then(() => { li.style.zIndex = ''; }, () => {});
    });
  };
  const showStacks = (animate: boolean) => {
    const was = shelf.isConnected;
    const before = new Map<HTMLElement, DOMRect>();
    if (was && animate) for (const li of stackEls) if (!li.hidden) before.set(li, li.getBoundingClientRect());
    if (!was) listEl.replaceChildren(shelf);
    for (const li of stackEls) li.hidden = !!view.level && li.dataset.level !== view.level;
    moreRow.hidden = true;
    none.hidden = true;
    rest.hidden = true;
    wait.hidden = true;
    if (!was) {
      const back = closed && stackEls.find((li) => li.dataset.stack === closed);
      closed = '';
      if (back && !back.hidden) back.querySelector<HTMLAnchorElement>('a')?.focus({ preventScroll: true });
      if (animate) deal();
      return;
    }
    if (!animate || !moving()) return;
    let k = 0;
    for (const li of stackEls) {
      if (li.hidden) continue;
      const r = li.getBoundingClientRect();
      const b = before.get(li);
      const delay = Math.min(k++ * 25, 200);
      if (b) li.animate([{ transform: `translate(${b.left - r.left}px, ${b.top - r.top}px)` }, { transform: 'none' }], { duration: 360, easing: EASE });
      else li.animate([{ opacity: 0, transform: 'translateY(10px) scale(.94)' }, { opacity: 1, transform: 'none' }], { duration: 300, delay, easing: 'ease-out', fill: 'backwards' });
    }
  };
  listEl.addEventListener('click', (e) => {
    const t = e.target as Element;
    if (t.closest('[data-fl-back]')) {
      closed = view.course || 'methods';
      view = { ...readView(''), level: stackCount(backLevel) > 1 ? backLevel : '' };
      limit = PAGE;
      toForm();
      commit(true);
      return;
    }
    const a = t.closest<HTMLAnchorElement>('li.fs > a');
    if (!a || e.metaKey || e.ctrlKey || e.shiftKey || e.altKey) return; // a new tab gets the course's films on its level page
    e.preventDefault();
    performance.mark('fl-tap');
    const li = a.parentElement as HTMLElement;
    const r = li.querySelector('.fs-pile')!.getBoundingClientRect();
    origin = { x: r.left + window.scrollX, y: r.top + window.scrollY, w: r.width, h: r.height };
    backLevel = view.level;
    if (li.dataset.stack === 'methods') view.kind = 'method';
    else { view.course = li.dataset.stack!; view.level = li.dataset.level!; }
    limit = PAGE;
    toForm();
    commit(true);
  });
  // The first time the gallery comes into view, the stacks deal themselves out.
  if (moving() && 'IntersectionObserver' in window) {
    const first = new IntersectionObserver((entries) => {
      if (!entries.some((e) => e.isIntersecting)) return;
      first.disconnect();
      if (!dealt && shelf.isConnected) deal();
    }, { threshold: 0.15 });
    first.observe(shelf);
  }

  let drawn = 0;
  async function render(animate: boolean): Promise<void> {
    const mine = ++drawn;
    // The same search address gives the same films however the page was reached.
    if (view.q && !ideas) void ensureIdeas();
    paintKeys();
    // What can be said before the list arrives: a level's size is in the page.
    if (!list && levelOnly()) {
      const idx = stripFilms.map((f, i) => i).filter((i) => !view.level || stripFilms[i].level === view.level);
      say(idx.length, idx.reduce((s, i) => s + stripFilms[i].d, 0));
      if (!budget) drawStrip(null);
    }
    // The stacks are in the page: they answer before the list arrives.
    const stacks = stacksOn();
    if (stacks) showStacks(animate);
    if (!list && isDefault(view) && !budget) { paintRun(null); return; } // the page as served
    let d = list;
    if (!d) {
      // The count and the strip have already changed; say plainly that the cards have not yet.
      if (!stacks) {
        listEl.setAttribute('aria-busy', 'true');
        wait.hidden = false;
        rest.hidden = true;
      }
      d = await ensure();
      listEl.removeAttribute('aria-busy');
      wait.hidden = true;
      if (!d) {
        if (stacks) return; // the stacks need no list
        // Without the list this page cannot show the view; the level's own page can.
        if (mine === drawn && view.level && levelOnly()) location.href = `/films/${view.level}/`;
        else if (mine === drawn) status.textContent = 'Could not load the full list. Each level’s page has every film.';
        return;
      }
    }
    if (mine !== drawn) return;
    view = { ...readView(viewQuery(view), d) };
    // A course belongs to one level: a link that names both, and disagrees, keeps the level.
    if (view.course && view.level && d.films.find((f) => f.c === view.course)?.s !== view.level) {
      view.course = '';
      toForm();
      history.replaceState(null, '', `${location.pathname}${viewQuery(view)}`);
    }
    const current = select(d, view, ideas);
    say(current.length, current.reduce((s, f) => s + f.d, 0));
    const run = drawStrip(current);
    paintRun(current, run);
    if (stacksOn()) { showStacks(false); performance.mark('fl-drawn'); performance.mark('fl-settled'); return; }
    const before = animate ? cardRects() : new Map<string, DOMRect>();
    none.hidden = current.length > 0;
    rest.hidden = true;
    const shown = current.slice(0, limit);
    // Built off the page, so that no poster is asked for until its card is near the screen (below).
    const built = document.createElement('template');
    // Inside one stack (a course, or the methods library): the way back to all of them comes first.
    const back = view.course || view.kind === 'method' ? '<p class="fl-back"><button type="button" class="fl-btn" data-fl-back><span aria-hidden="true">←</span> All courses</button></p>' : '';
    // A search lists the films with every word first; films with all but one follow under a note (2026-11-22).
    const full = (current as { full?: number }).full ?? current.length;
    const flat = full < shown.length
      ? `${full ? `<ul class="grid">${shown.slice(0, full).map((f) => cardHTML(f, d)).join('')}</ul>` : ''}<p class="fl-partial">${full ? 'These have some of your words, not all:' : 'No film has every word. These have all but one:'}</p><ul class="grid fl-partial-grid">${shown.slice(full).map((f) => cardHTML(f, d)).join('')}</ul>`
      : `<ul class="grid">${shown.map((f) => cardHTML(f, d)).join('')}</ul>`;
    built.innerHTML = back + (view.sort === 'course' && !view.q ? groupHTML(shown, d) : flat);
    for (const img of built.content.querySelectorAll('img')) { img.dataset.src = img.getAttribute('src') ?? ''; img.removeAttribute('src'); img.removeAttribute('loading'); }
    listEl.replaceChildren(built.content);
    const from = origin;
    origin = null;
    let out: DOMRect | null = null;
    if (from) {
      // The films take the stacks' place: bring their top to the top of the screen, then fly them out of the stack.
      const top = listEl.getBoundingClientRect().top;
      if (top < 70 || top > window.innerHeight * 0.55) window.scrollTo({ top: window.scrollY + top - 96, behavior: 'instant' as ScrollBehavior });
      out = new DOMRect(from.x - window.scrollX, from.y - window.scrollY, from.w, from.h);
      listEl.querySelector<HTMLElement>('[data-fl-back]')?.focus({ preventScroll: true });
    }
    for (const img of listEl.querySelectorAll('img[data-src]')) posters.observe(img);
    if (view.level && view.sort === 'course' && levelOnly()) {
      const pic = listEl.querySelector('li.fc .fc-pic');
      if (pic) { const s = document.createElement('span'); s.className = 'fc-start'; s.textContent = 'Start here'; pic.append(s); }
    }
    markCards(listEl);
    moreRow.hidden = current.length <= limit;
    performance.mark('fl-drawn');
    if (animate) slide(before, out); else performance.mark('fl-settled');
  }

  /* ---- play them in order, or for a while */
  const runBox = $('[data-fl-run]');
  const runSum = $('[data-fl-run-sum]');
  const runText = $('[data-fl-run-text]');
  const runList = $('[data-fl-run-list]');
  const play = $<HTMLAnchorElement>('[data-fl-play]');
  const startBtn = $<HTMLAnchorElement>('[data-fl-run-start]');
  const radios = [...runBox.querySelectorAll<HTMLInputElement>('input[name="fl-t"]')];
  runBox.hidden = false;
  function paintRun(current: ListFilm[] | null, run?: ReturnType<typeof fit> | null): void {
    const q = viewQuery(view);
    // Nothing to play in a row (no film matches, or only scientist profiles): offer nothing.
    const can = !current || !list || runQueue(list, view, ideas).length > 0;
    runBox.hidden = !can;
    // The whole library in order is 45 hours; "in order" is offered once a view has been chosen.
    play.hidden = isDefault({ ...view, sort: 'course' });
    play.textContent = view.q ? 'Play these results' : 'Play them in order';
    // One course in course order, not searched: its own play-in-order page, as before. A search always
    // plays on /films/run/, where the same matcher and the same search data decide the films.
    play.href = view.course && view.sort === 'course' && !view.q ? `/films/play/${encodeURIComponent(view.course)}/${viewQuery({ ...view, level: '', course: '', sort: 'course' })}` : `/films/run/${q}`;
    if (!budget || !current) { runSum.hidden = true; return; }
    runSum.hidden = false;
    if (!run || !run.films.length) {
      runText.textContent = 'Nothing in this view plays in a row: scientist profiles open in their lessons.';
      runList.hidden = true;
      startBtn.hidden = true;
      return;
    }
    startBtn.hidden = false;
    startBtn.href = `/films/run/${viewQuery(view, { t: String(budget) })}`;
    runText.textContent = runSentence(run.films, run.seconds);
    runList.innerHTML = run.films.map((f) => `<li>${esc(f.t)} <span class="fc-len-t">${clock(f.d)}</span></li>`).join('');
    runList.hidden = false;
  }
  for (const r of radios) {
    r.addEventListener('change', () => { performance.mark('fl-tap'); budget = BUDGETS.includes(Number(r.value)) ? Number(r.value) : 0; void render(false); });
  }
  // Coming back to this page (Back from a run) the browser may restore a pressed time with no summary.
  window.addEventListener('pageshow', () => { if (!budget) for (const r of radios) r.checked = false; });
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
    if (!ideas) void ensureIdeas();
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
    history.replaceState({ limit }, '', location.href);
    void render(false).then(() => listEl.querySelectorAll<HTMLAnchorElement>('li.fc > a')[had]?.focus());
  });
  $('[data-fl-clear]').addEventListener('click', () => { view = readView(''); limit = PAGE; toForm(); commit(true); field('q').focus(); });
  window.addEventListener('popstate', (e) => { view = readView(location.search, list ?? undefined); limit = Math.max(PAGE, Number(e.state?.limit) || PAGE); toForm(); void render(false); startCard(); });

  /* ---- a film to start with, or where you stopped */
  type StartPick = { s: string; t: string; h: string; o: string; d: string; m: string; x: string };
  const startEl = $('[data-fl-start]');
  const pool: StartPick[] = JSON.parse(startEl.dataset.pool ?? '[]');
  const surprise = $<HTMLButtonElement>('[data-fl-surprise]');
  const part = (k: string) => startEl.querySelector<HTMLElement>(`[data-fl-start-${k}]`)!;
  let shownPick: StartPick | null = null;
  let stoppedDismissed = false;
  const prefLevel = (): string => { const l = readPrefs().level ?? ''; return levelKeys.includes(l) ? l : ''; };
  const poolFor = () => {
    const level = view.level || prefLevel();
    // With no level chosen here and none set on this device: grade 7, where biology starts.
    const mine = pool.filter((p) => p.s === (level || 'grade-7'));
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
    if (!mine.length) return;
    const p = mine[Math.floor(Math.random() * mine.length)];
    showPick(p);
    // The card changes in place, with focus still on the button: say what it now holds.
    $('[data-fl-say]').textContent = `Now showing ${p.t}, ${p.m}, ${p.d}.`;
  });

  /* ---- the record: said only once there is something to say */
  onFilmsChange(() => {
    const n = Object.keys(loadFilms().w).length;
    seen.textContent = n ? `${filmsWord(n)} watched on this device.` : '';
    seen.hidden = n === 0;
  });

  form.hidden = false;
  rest.hidden = true;
  if (view.q) void ensureIdeas();
  toForm();
  startCard();
  void render(false);
}
