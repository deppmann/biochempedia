/* /films/run/ in the browser (2026-11-20): plays a view of the library in order, or one idea at every
   level (?idea=<id>, 2026-11-21). See the page's header comment for the rules. Nothing is stored; the
   plan is the query string, which also keeps the film a run started at (from=), so a reload gives the
   same run and the same stated end. A playlist (?list=key,key&from=key, 2026-11-22) plays its films in
   the order given, from the one chosen. */
import type { FilmList, ListFilm } from './film-cards';
import { isWatched, loadFilms, onFilmsChange } from './film-progress';
import { BUDGETS, SLACK, about, clock, filmsWord, fit, isDefault, loadIdeas, readView, runQueue, runSentence, select, viewQuery } from './film-view';
import { endWith, runFilms, runPlace } from './film-logic.mjs';
import { bindPlayAll } from './film-autoadvance';

/* The next film is offered and does not start by itself (ruling, 2026-11-20): a timer nobody can
   see is worse than the digits it replaced. The one exception is the viewer's own Play all setting
   (2026-11-24, film-autoadvance.ts): with it on, the next film starts when the one playing ends. */

export async function run(): Promise<void> {
  const root = document.querySelector<HTMLElement>('[data-fr]');
  if (!root) return;
  const $ = <T extends HTMLElement>(sel: string) => root.querySelector<T>(sel)!;
  const sum = $('[data-fr-sum]');
  sum.textContent = 'Putting your films in order…';
  const params = new URLSearchParams(location.search);

  let list: FilmList;
  try {
    const res = await fetch('/films/list.json');
    if (!res.ok) throw new Error(String(res.status));
    list = await res.json();
  } catch {
    sum.textContent = 'Could not load the films. Each level’s page lists its films.';
    return;
  }

  // A "keep watching" link made while a run was playing points here with ?film=&at=: send it to the
  // film's own page, which opens at that second.
  const resume = params.get('film');
  if (resume) {
    const f = list.films.find((x) => x.f === resume);
    if (f) { location.replace(`${f.h}?film=${encodeURIComponent(resume)}&at=${Math.floor(Number(params.get('at')) || 0)}`); return; }
  }

  const view = readView(location.search, list);
  const minutes = BUDGETS.includes(Number(params.get('t'))) ? Number(params.get('t')) : 0;
  const back = `/films/${viewQuery(view)}`;
  $<HTMLAnchorElement>('[data-fr-back]').href = back;
  $<HTMLAnchorElement>('[data-fr-more]').href = back;
  const nothing = (text: string) => { sum.textContent = text; };
  const nothingLink = (text: string) => {
    sum.textContent = `${text} `;
    const a = document.createElement('a');
    a.href = '/films/';
    a.textContent = 'Films';
    sum.append(a);
  };

  let films: ListFilm[] = [];
  let seconds = 0;
  let lead = '';
  const idea = params.get('idea') ?? '';
  // A playlist made on this device (src/lib/film-playlist.ts, 2026-11-22): ?list=key,key,...&from=key.
  // It plays in the order given, from the film chosen, whatever has been watched.
  const listed = (params.get('list') ?? '').split(',').filter((k) => /^[a-z0-9][a-z0-9/._-]{0,160}$/i.test(k) && !k.includes('..')).slice(0, 100);
  let startKey = '';
  if (listed.length) {
    const byKey = new Map(list.films.map((f) => [f.f, f]));
    films = listed.map((k) => byKey.get(k)).filter((f): f is ListFilm => !!f);
    if (!films.length) return nothingLink('None of the films in this playlist is on the site any more. Every film is on the films page.');
    seconds = films.reduce((s, f) => s + f.d, 0);
    startKey = params.get('from') ?? '';
    root.querySelector('h1')!.textContent = 'Your playlist';
    document.title = 'Your playlist — STEMhop';
  } else if (idea) {
    // One idea, from the simplest level to the deepest: the whole ladder, whatever has been watched.
    if (!/^[a-z0-9-]{1,80}$/.test(idea)) return nothing('There is no idea by that name.');
    let found: { name: string; films: string[] } | null = null;
    try {
      const res = await fetch(`/films/idea/${idea}.json`);
      if (res.ok) found = await res.json();
    } catch { /* treated as not found */ }
    const byKey = new Map(list.films.map((f) => [f.f, f]));
    films = (found?.films ?? []).map((k) => byKey.get(k)).filter((f): f is ListFilm => !!f);
    // No file: not an idea, or an idea whose films are all at one level.
    if (!found) return nothingLink('There is no run of films for that idea. Every film is on the films page.');
    if (films.length < 2) return nothing('This idea does not have films at more than one level yet.');
    seconds = films.reduce((s, f) => s + f.d, 0);
    // "Simplest first", not "at every level": most ideas have films at two or three of the seven.
    lead = '';
    root.querySelector('h1')!.textContent = `${found.name}, simplest first`;
    document.title = `${found.name}, simplest first — STEMhop`;
  } else {
    // The bare address is the whole library, 45 hours of it: ask for a view instead.
    if (isDefault({ ...view, sort: 'course' }) && !minutes) return nothingLink('Choose a level or a search on the films page, then play it in order.');
    // The same films the library showed for this view: the same matcher, with the same search data.
    const ideas = view.q ? await loadIdeas() : null;
    if (!select(list, view, ideas).length) return nothing('No film matches this view.');
    const queue = runQueue(list, view, ideas);
    if (!queue.length) return nothing('Nothing in this view plays in a row. Scientist profiles open in their lessons.');
    // A run keeps the film it started at in its address, so a reload plays the same run to the same end.
    const from = queue.findIndex((f) => f.f === params.get('from'));
    if (from >= 0) {
      ({ films, seconds } = runFilms(queue, from, minutes, SLACK));
    } else {
      const plan = fit(queue, minutes, loadFilms());
      films = plan.films;
      seconds = plan.seconds;
      params.set('from', films[0].f);
      history.replaceState(null, '', `${location.pathname}?${params}`);
    }
  }
  const totalMin = Math.max(1, Math.round(seconds / 60));
  const length = seconds > 3600 ? about(seconds) : `${totalMin} ${totalMin === 1 ? 'minute' : 'minutes'}`;
  sum.textContent = `${lead}${runSentence(films, seconds)} Nothing plays until you press play.`;

  const v = $<HTMLVideoElement>('video');
  const title = $('[data-fr-title]');
  const meta = $('[data-fr-meta]');
  const page = $<HTMLAnchorElement>('[data-fr-page]');
  const take = $('[data-fr-take]');
  const next = $('[data-fr-next]');
  const nextText = $('[data-fr-next-text]');
  const playNext = $<HTMLButtonElement>('[data-fr-play-next]');
  const stop = $<HTMLButtonElement>('[data-fr-stop]');
  const more = $('[data-fr-more]');
  const queue = $('[data-fr-queue]');
  const restNote = $('[data-fr-rest]');
  const prevBtn = $<HTMLButtonElement>('[data-fr-prev]');
  const nextBtn = $<HTMLButtonElement>('[data-fr-nextbtn]');
  const pos = $('[data-fr-pos]');
  const playAll = bindPlayAll(root.querySelector<HTMLInputElement>('[data-fr-auto]'));
  let at = 0;

  const startAt = $('[data-fr-startat]');
  /* The queue lists the next thirty films; a longer run says how many follow, and the list moves on
     with the run. A watched film says so in words, not by colour alone. */
  let nextPressed = -1000;
  const SHOWN = 30;
  let first = 0;
  let drawnFrom = -1;
  const drawQueue = () => {
    const r = loadFilms();
    queue.setAttribute('start', String(first + 1));
    queue.style.counterReset = `fr ${first}`;
    // The rows are built once for each stretch of thirty and then only marked, so a row that has
    // keyboard focus is never replaced under it.
    if (drawnFrom !== first) {
      drawnFrom = first;
      queue.replaceChildren(...films.slice(first, first + SHOWN).map((f, k) => {
        const i = first + k;
        const li = document.createElement('li');
        const b = document.createElement('button');
        b.type = 'button';
        // An idea's run is its ladder: each row says its level.
        b.textContent = `${idea && f.s ? `${list.levels[f.s]} · ` : ''}${f.t} · ${clock(f.d)}`;
        const s = document.createElement('span');
        s.className = 'fr-seen';
        b.append(s);
        // (Not in the half second after Play next: its box closes, the list moves up under the pointer, and a second click would skip a film.)
        b.addEventListener('click', () => { if (performance.now() - nextPressed < 500) return; show(i); void v.play().catch(() => {}); });
        li.append(b);
        return li;
      }));
    }
    [...queue.children].forEach((li, k) => {
      const i = first + k;
      const b = li.firstElementChild!;
      if (i === at) b.setAttribute('aria-current', 'true'); else b.removeAttribute('aria-current');
      const seen = isWatched(r, films[i].f);
      li.classList.toggle('is-seen', seen);
      b.querySelector('.fr-seen')!.textContent = seen ? ' · watched' : '';
    });
    const longer = films.length > first + SHOWN;
    restNote.hidden = !longer;
    restNote.textContent = longer ? `The run goes on in order to ${endWith(films[films.length - 1].t)}` : '';
  };
  onFilmsChange(drawQueue);

  function show(i: number): void {
    at = i;
    const f: ListFilm = films[i];
    v.pause();
    v.poster = f.o;
    // Captions the viewer turned on stay on for the next film: a new source resets the old track.
    const showing = [...v.textTracks].some((t) => t.mode === 'showing');
    v.src = `/explainers/${f.f}.mp4`;
    v.preload = 'none';
    const track = document.createElement('track');
    track.kind = 'captions'; track.srclang = 'en'; track.label = 'English';
    track.src = `/explainers/${f.f}.vtt`;
    if (showing) track.default = true;
    v.querySelector('track')?.replaceWith(track);
    if (showing) track.addEventListener('load', () => { for (const t of v.textTracks) t.mode = 'showing'; }, { once: true });
    v.dataset.listenFilm = f.t;
    v.dataset.filmTitle = f.t;
    v.dataset.listenFilmSec = String(f.d);
    title.textContent = f.t;
    // A short run says where you are in it; a long one is not a list to get through.
    meta.textContent = `Film ${i + 1}${films.length <= 12 ? ` of ${films.length}` : ''} · ${f.c ? list.courses[f.c] : ''}${f.s ? ` · ${list.levels[f.s]}` : ''} · ${clock(f.d)}`;
    v.setAttribute('aria-label', `Film: ${f.t}`);
    page.href = f.h;
    take.hidden = true;
    take.textContent = f.th ?? '';
    next.hidden = true;
    nextText.textContent = '';
    if (i < first || i >= first + SHOWN) first = i;
    startAt.hidden = true;
    pos.textContent = `Film ${i + 1} of ${films.length}`;
    prevBtn.disabled = i === 0;
    nextBtn.disabled = i >= films.length - 1;
    prevBtn.setAttribute('aria-label', i > 0 ? `Previous film: ${films[i - 1].t}` : 'Previous film');
    nextBtn.setAttribute('aria-label', i < films.length - 1 ? `Next film: ${films[i + 1].t}` : 'Next film');
    drawQueue();
  }
  // Previous and Next: a press is the viewer's own, so the film starts. A button that has just been
  // disabled (the first or last film) hands keyboard focus to the film's title.
  const step = (d: number, btn: HTMLButtonElement) => {
    const i = at + d;
    if (i < 0 || i >= films.length) return;
    nextPressed = performance.now();
    show(i);
    if (btn.disabled) title.focus();
    void v.play().catch(() => {});
  };
  prevBtn.addEventListener('click', () => step(-1, prevBtn));
  nextBtn.addEventListener('click', () => step(1, nextBtn));
  const offer = () => {
    // The film's take-home first; the offer of the next film sits under it.
    take.hidden = !take.textContent;
    const nx = films[at + 1];
    next.hidden = false;
    playNext.hidden = !nx;
    stop.hidden = !nx;
    more.hidden = !!nx;
    if (!nx) {
      nextText.textContent = `That was ${filmsWord(films.length)}, ${length}.`;
      return;
    }
    nextText.textContent = `Next, when you are ready: ${nx.t}, ${clock(nx.d)}.`;
  };
  v.addEventListener('ended', () => {
    const nx = films[at + 1];
    if (!nx || !playAll()) { offer(); return; }
    // Play all: straight on to the next film. If the browser will not start it, the usual offer.
    const i = at + 1;
    show(i);
    nextText.textContent = `Playing all. Now: ${nx.t}, ${clock(nx.d)}.`;
    v.play().catch(() => { if (at === i) nextText.textContent = `Next: ${nx.t}, ${clock(nx.d)}. Press play to start it.`; });
  });
  playNext.addEventListener('click', () => { nextPressed = performance.now(); show(at + 1); title.focus(); void v.play().catch(() => {}); });
  stop.addEventListener('click', () => {
    // True either way: a run reopens at its first film not yet watched (runPlace).
    nextText.textContent = 'Stopped here. Next time this run opens at the first film you have not watched.';
    more.hidden = false;
    more.focus(); // before the button that was pressed goes away
    playNext.hidden = true;
    stop.hidden = true;
  });
  /* Where the run opens: its first film not yet watched on this device, and, if that film was left
     part-way, at that second, paused. A reload or a return therefore carries on, not starts over. */
  const record = loadFilms();
  const chosen = startKey ? films.findIndex((f) => f.f === startKey) : -1;
  const place = chosen >= 0 ? { index: chosen, at: 0 } : runPlace(films, { has: (k: string) => isWatched(record, k) }, record.p);
  $('[data-fr-stage]').hidden = false;
  show(place.index);
  if (place.at > 0) {
    // Only for the film the place belongs to: if another is chosen before this one has loaded, it starts at its start.
    const seek = () => { if (at !== place.index) return; try { v.currentTime = place.at; } catch { /* stays at the start */ } };
    v.addEventListener('loadedmetadata', seek, { once: true });
    v.preload = 'metadata';
    v.load();
    startAt.textContent = `Press play to start at ${clock(place.at)}.`;
    startAt.hidden = false;
    v.addEventListener('play', () => { startAt.hidden = true; }, { once: true });
  }
}
