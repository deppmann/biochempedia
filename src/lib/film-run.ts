/* /films/run/ in the browser (2026-11-20): plays a view of the library in order, or one idea at every
   level (?idea=<id>, 2026-11-21). See the page's header comment for the rules. Nothing is stored; the
   plan is the query string, which also keeps the film a run started at (from=), so a reload gives the
   same run and the same stated end. */
import type { FilmList, ListFilm } from './film-cards';
import { isWatched, loadFilms, onFilmsChange } from './film-progress';
import { BUDGETS, SLACK, about, clock, filmsWord, fit, readView, runSentence, runnable, select, viewQuery } from './film-view';

/* The next film is always offered and never starts by itself (ruling, 2026-11-20): a timer nobody can
   see is worse than the digits it replaced. */

export async function run(): Promise<void> {
  const root = document.querySelector<HTMLElement>('[data-fr]');
  if (!root) return;
  const $ = <T extends HTMLElement>(sel: string) => root.querySelector<T>(sel)!;
  const sum = $('[data-fr-sum]');
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

  let films: ListFilm[] = [];
  let seconds = 0;
  let lead = '';
  const idea = params.get('idea') ?? '';
  if (idea) {
    // One idea, from the simplest level to the deepest: the whole ladder, whatever has been watched.
    if (!/^[a-z0-9-]{1,80}$/.test(idea)) return nothing('There is no idea by that name.');
    let found: { name: string; films: string[] } | null = null;
    try {
      const res = await fetch(`/films/idea/${idea}.json`);
      if (res.ok) found = await res.json();
    } catch { /* treated as not found */ }
    const byKey = new Map(list.films.map((f) => [f.f, f]));
    films = (found?.films ?? []).map((k) => byKey.get(k)).filter((f): f is ListFilm => !!f);
    if (!found || films.length < 2) return nothing('This idea does not have films at more than one level yet.');
    seconds = films.reduce((s, f) => s + f.d, 0);
    lead = `${found.name} at every level, simplest first: `;
    root.querySelector('h1')!.textContent = `${found.name} at every level`;
  } else {
    const matched = select(list, view);
    if (!matched.length) return nothing('No film matches this view.');
    const queue = runnable(matched, view);
    if (!queue.length) return nothing('Nothing in this view plays in a row. Scientist profiles and method films open on their own pages.');
    // A run keeps the film it started at in its address, so a reload plays the same run to the same end.
    const from = queue.findIndex((f) => f.f === params.get('from'));
    if (from >= 0) {
      for (const f of queue.slice(from)) {
        if (minutes && films.length && seconds + f.d > minutes * 60 + SLACK) break;
        films.push(f);
        seconds += f.d;
      }
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
  let at = 0;

  /* The queue lists the next thirty films; a longer run says how many follow, and the list moves on
     with the run. A watched film says so in words, not by colour alone. */
  const SHOWN = 30;
  let first = 0;
  const drawQueue = () => {
    const r = loadFilms();
    queue.setAttribute('start', String(first + 1));
    queue.style.counterReset = `fr ${first}`;
    queue.replaceChildren(...films.slice(first, first + SHOWN).map((f, k) => {
      const i = first + k;
      const li = document.createElement('li');
      const b = document.createElement('button');
      b.type = 'button';
      b.textContent = `${f.t} · ${clock(f.d)}`;
      if (i === at) b.setAttribute('aria-current', 'true');
      if (isWatched(r, f.f)) {
        li.classList.add('is-seen');
        const s = document.createElement('span');
        s.className = 'fr-seen';
        s.textContent = ' · watched';
        b.append(s);
      }
      b.addEventListener('click', () => { show(i); void v.play().catch(() => {}); });
      li.append(b);
      return li;
    }));
    const left = films.length - first - SHOWN;
    restNote.hidden = left <= 0;
    restNote.textContent = left > 0 ? `Then ${left.toLocaleString('en-US')} more ${left === 1 ? 'film' : 'films'}, in order.` : '';
  };
  const marks = () => drawQueue();
  onFilmsChange(marks);

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
    if (i < first || i >= first + SHOWN) first = i;
    drawQueue();
  }
  v.addEventListener('ended', () => {
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
  });
  playNext.addEventListener('click', () => { show(at + 1); title.focus(); void v.play().catch(() => {}); });
  stop.addEventListener('click', () => {
    nextText.textContent = `Stopped here, after ${filmsWord(at + 1)}. Next time you will start at ${films[at + 1].t}.`;
    more.hidden = false;
    more.focus(); // before the button that was pressed goes away
    playNext.hidden = true;
    stop.hidden = true;
  });
  $('[data-fr-stage]').hidden = false;
  show(0);
}
