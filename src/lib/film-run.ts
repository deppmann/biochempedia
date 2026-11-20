/* /films/run/ in the browser (2026-11-20): plays a view of the library in order. See the page's
   header comment for the rules. Nothing is stored; the plan is the query string. */
import type { FilmList, ListFilm } from './film-cards';
import { isWatched, loadFilms, onFilmsChange } from './film-progress';
import { BUDGETS, clock, filmsWord, fit, readView, runSentence, runnable, select, viewQuery } from './film-view';

/* Off: the next film is offered and starts only when asked. On: inside a run the viewer started, the
   next film starts by itself after a still pause of five seconds (no digits), and any touch, key or
   scroll cancels that for good. Chris's call; the calm principles say "offer, don't queue". */
const RUN_ADVANCES = false;

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
  const plan = fit(runnable(select(list, view), view), minutes, loadFilms());
  const films = plan.films;
  if (!films.length) {
    sum.textContent = 'Nothing in this view plays in a row. Scientist profiles and method films open on their own pages.';
    return;
  }
  const totalMin = Math.max(1, Math.round(plan.seconds / 60));
  sum.textContent = `${runSentence(films, plan.seconds)} Nothing plays until you press play.`;

  const v = $<HTMLVideoElement>('video');
  const track = v.querySelector('track')!;
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
  let at = 0;
  let timer = 0;

  queue.innerHTML = '';
  films.forEach((f, i) => {
    const li = document.createElement('li');
    const b = document.createElement('button');
    b.type = 'button';
    b.textContent = `${f.t} · ${clock(f.d)}`;
    b.addEventListener('click', () => { show(i); void v.play().catch(() => {}); });
    li.append(b);
    queue.append(li);
  });
  const marks = () => {
    const r = loadFilms();
    [...queue.children].forEach((li, i) => li.classList.toggle('is-seen', isWatched(r, films[i].f)));
  };
  onFilmsChange(marks);

  const hold = () => { window.clearTimeout(timer); timer = 0; };
  function show(i: number): void {
    hold();
    at = i;
    const f: ListFilm = films[i];
    v.pause();
    v.poster = f.o;
    v.src = `/explainers/${f.f}.mp4`;
    v.preload = 'none';
    track.src = `/explainers/${f.f}.vtt`;
    v.dataset.listenFilm = f.t;
    v.dataset.filmTitle = f.t;
    v.dataset.listenFilmSec = String(f.d);
    title.textContent = f.t;
    meta.textContent = `Film ${i + 1} of ${films.length} · ${f.c ? list.courses[f.c] : ''}${f.s ? ` · ${list.levels[f.s]}` : ''} · ${clock(f.d)}`;
    page.href = f.h;
    take.hidden = true;
    take.textContent = f.th ?? '';
    next.hidden = true;
    [...queue.children].forEach((li, k) => { const b = li.firstElementChild!; if (k === i) b.setAttribute('aria-current', 'true'); else b.removeAttribute('aria-current'); });
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
      nextText.textContent = `That was ${filmsWord(films.length)}, ${totalMin} ${totalMin === 1 ? 'minute' : 'minutes'}.`;
      return;
    }
    nextText.textContent = `Next, when you are ready: ${nx.t}, ${clock(nx.d)}.`;
    if (RUN_ADVANCES) {
      timer = window.setTimeout(() => { show(at + 1); void v.play().catch(() => {}); }, 5000);
      for (const ev of ['pointerdown', 'keydown', 'wheel', 'touchmove'] as const) window.addEventListener(ev, hold, { once: true, passive: true });
    }
  });
  playNext.addEventListener('click', () => { show(at + 1); title.focus(); void v.play().catch(() => {}); });
  stop.addEventListener('click', () => {
    hold();
    nextText.textContent = `Stopped here, after ${filmsWord(at + 1)}. Next time you will start at ${films[at + 1].t}.`;
    playNext.hidden = true;
    stop.hidden = true;
    more.hidden = false;
  });
  // "Cards ready" (CardsPrompt) and anything else that opens over the run cancels a pending start.
  root.addEventListener('bp-cards-open', hold);

  $('[data-fr-stage]').hidden = false;
  show(0);
}
