/* "Play a ladder" on /films/ (2026-11-22). The viewer picks an idea; the site's one ladder drawing
   (src/lib/hop-ladder.mjs, as on lesson, idea and film pages) is drawn for it, and the idea's films
   fly onto their rungs as small thumbnails, simplest level first. A thumbnail plays its film in the
   player beside the ladder, and Hex stands on that film's rung.

   "Play the ladder" plays every film of the ladder in order, from the first film or from the one
   the viewer picked ("Play on from here"), both chapters of each lesson, the next film starting
   when one ends. This is the one place a film starts by itself, and only because the viewer asked
   for the whole ladder; "Stop" ends it, and outside a ladder run nothing advances (the run page's
   rule, src/lib/film-run.ts).

   The address keeps the ladder and the place: /films/?ladder=<idea id>&at=<film number, from 1>,
   so a link opens the same ladder at the same film. Nothing plays until the viewer presses play.

   Motion: the thumbnails fly out of the picker onto their rungs, once per ladder opened. Under
   reduced motion they are simply there. Hex lands with the drawing's own short drop (hop.css). */
import { ladderHtml, wireLadders } from './hop-ladder.mjs';
import { LEVEL_KEYS, LEVEL_LABEL } from './hop-words.mjs';
import { isWatched, loadFilms, onFilmsChange } from './film-progress';

type Film = [key: string, title: string, href: string, rank: number, seconds: number, poster: string];
interface Ladder {
  id: string;
  name: string;
  short: string;
  area: string;
  rungs: { slug: string; title: string; href: string; rank: number; courseTitle: string; adds?: string }[];
  films: Film[];
}

const clock = (s: number) => `${Math.floor(s / 60)}:${String(Math.round(s) % 60).padStart(2, '0')}`;
const minutes = (films: Film[]) => Math.max(1, Math.round(films.reduce((t, f) => t + f[4], 0) / 60));

let data: Promise<Ladder[] | null> | undefined;
const load = () => (data ??= fetch('/films/ladders.json')
  .then((r) => (r.ok ? r.json() : null))
  .then((j) => (j?.ladders as Ladder[]) ?? null)
  .catch(() => null));

export function filmLadder(): void {
  const root = document.querySelector<HTMLElement>('[data-flx]');
  if (!root) return;
  const $ = <T extends HTMLElement>(sel: string) => root.querySelector<T>(sel)!;
  const form = $<HTMLFormElement>('[data-flx-pick]');
  const select = $<HTMLSelectElement>('select');
  const go = $<HTMLButtonElement>('[data-flx-go]');
  const stage = $('[data-flx-stage]');
  const rail = $('[data-flx-ladder]');
  const v = $<HTMLVideoElement>('video');
  const title = $('[data-flx-title]');
  const meta = $('[data-flx-meta]');
  const page = $<HTMLAnchorElement>('[data-flx-page]');
  const say = $('[data-flx-say]');
  const sum = $('[data-flx-sum]');
  const btnAll = $<HTMLButtonElement>('[data-flx-all]');
  const btnHere = $<HTMLButtonElement>('[data-flx-here]');
  const btnPrev = $<HTMLButtonElement>('[data-flx-prev]');
  const btnNext = $<HTMLButtonElement>('[data-flx-next]');
  const btnStop = $<HTMLButtonElement>('[data-flx-stop]');
  const still = window.matchMedia('(prefers-reduced-motion: reduce)');

  // With scripts the picker opens the ladder here; without them it opens the run page.
  go.hidden = true;

  let L: Ladder | null = null;
  let at = 0;
  let drawnRank = -1;
  let running = false;

  const setAddress = () => {
    const p = new URLSearchParams(location.search);
    if (L) { p.set('ladder', L.id); p.set('at', String(at + 1)); } else { p.delete('ladder'); p.delete('at'); }
    const qs = p.toString();
    const url = `${location.pathname}${qs ? `?${qs}` : ''}${location.hash}`;
    if (url !== location.pathname + location.search + location.hash) history.replaceState(history.state, '', url);
  };

  const thumbs = () => [...rail.querySelectorAll<HTMLButtonElement>('.flx-th')];
  const thumb = (i: number) => rail.querySelector<HTMLButtonElement>(`.flx-th[data-i="${i}"]`);
  /** A title inside a sentence: no second full stop after a title that ends in ? or !. */
  const said = (t: string) => (/[.?!]$/.test(t) ? t : `${t}.`);

  /** Draw the ladder with Hex on the current film's rung, and put each film's thumbnail on its rung. */
  function draw(fly: boolean): void {
    if (!L) return;
    const focused = (document.activeElement as HTMLElement | null)?.closest?.('.flx-th') ? Number((document.activeElement as HTMLElement).dataset.i) : -1;
    const rank = L.films[at][3];
    rail.innerHTML = ladderHtml(
      { id: L.id, name: L.name, short: L.short, rungs: L.rungs },
      { hereRank: rank, hereLabel: 'the film in the player', hex: true, window: false, facts: false, from: null, play: null },
    );
    wireLadders(rail);
    drawnRank = rank;
    const ranks = [...new Set(L.films.map((f) => f[3]))];
    for (const r of ranks) {
      const host = rail.querySelector(`.hl-level[data-hop-level="${LEVEL_KEYS[r]}"] .hl-text`);
      if (!host) continue;
      const ol = document.createElement('ol');
      ol.className = 'flx-thumbs';
      ol.setAttribute('aria-label', `Films at ${LEVEL_LABEL[r].toLowerCase()}`);
      L.films.forEach((f, i) => {
        if (f[3] !== r) return;
        const li = document.createElement('li');
        const b = document.createElement('button');
        b.type = 'button';
        b.className = 'flx-th';
        b.dataset.i = String(i);
        b.title = `${f[1]} · ${clock(f[4])}`;
        const img = document.createElement('img');
        img.src = f[5];
        img.alt = '';
        img.width = 96;
        img.height = 54;
        img.decoding = 'async';
        const n = document.createElement('span');
        n.className = 'flx-th-n';
        n.setAttribute('aria-hidden', 'true');
        n.textContent = String(i + 1);
        const t = document.createElement('span');
        t.className = 'visually-hidden';
        t.textContent = `Film ${i + 1} of ${L!.films.length}: ${f[1]}, ${clock(f[4])}`;
        const seen = document.createElement('span');
        seen.className = 'visually-hidden flx-seen';
        b.append(img, n, t, seen);
        li.append(b);
        ol.append(li);
      });
      host.append(ol);
    }
    mark();
    if (focused >= 0) thumb(focused)?.focus({ preventScroll: true });
    if (fly && !still.matches) flyIn();
  }

  /** The thumbnails leave the picker and land on their rungs, in ladder order. */
  function flyIn(): void {
    const from = select.getBoundingClientRect();
    const fx = from.left + from.width / 2;
    const fy = from.top + from.height / 2;
    const list = thumbs().sort((a, b) => Number(a.dataset.i) - Number(b.dataset.i));
    const step = Math.min(90, 1400 / Math.max(1, list.length));
    list.forEach((b, k) => {
      const r = b.getBoundingClientRect();
      const dx = fx - (r.left + r.width / 2);
      const dy = fy - (r.top + r.height / 2);
      const spin = k % 2 ? 14 : -14;
      b.animate(
        [
          { transform: `translate(${dx}px, ${dy}px) scale(0.25) rotate(${spin}deg)`, opacity: 0 },
          { opacity: 1, offset: 0.35 },
          { transform: 'translate(0, -6px) scale(1.08) rotate(0deg)', offset: 0.8 },
          { transform: 'none', opacity: 1 },
        ],
        { duration: 620, delay: k * step, easing: 'cubic-bezier(.2,.8,.25,1)', fill: 'backwards' },
      );
    });
  }

  /** Mark the film in the player and the films watched on this device. */
  function mark(): void {
    if (!L) return;
    const rec = loadFilms();
    for (const b of thumbs()) {
      const i = Number(b.dataset.i);
      if (i === at) b.setAttribute('aria-current', 'true'); else b.removeAttribute('aria-current');
      const seen = isWatched(rec, L.films[i][0]);
      b.classList.toggle('is-seen', seen);
      b.querySelector('.flx-seen')!.textContent = seen ? ' (watched)' : '';
    }
  }
  onFilmsChange(mark);

  function controls(): void {
    if (!L) return;
    btnPrev.disabled = at === 0;
    btnNext.disabled = at === L.films.length - 1;
    btnAll.hidden = running;
    btnHere.hidden = running || at === 0;
    btnStop.hidden = !running;
  }

  /** Put film i in the player (paused); Hex moves to its rung. */
  function show(i: number): void {
    if (!L) return;
    at = Math.max(0, Math.min(L.films.length - 1, i));
    const f = L.films[at];
    v.pause();
    v.poster = f[5];
    const showing = [...v.textTracks].some((t) => t.mode === 'showing');
    v.src = `/explainers/${f[0]}.mp4`;
    v.preload = 'metadata';
    const track = document.createElement('track');
    track.kind = 'captions'; track.srclang = 'en'; track.label = 'English';
    track.src = `/explainers/${f[0]}.vtt`;
    if (showing) track.default = true;
    v.querySelector('track')?.replaceWith(track);
    if (showing) track.addEventListener('load', () => { for (const t of v.textTracks) t.mode = 'showing'; }, { once: true });
    v.dataset.listenFilm = f[1];
    v.dataset.filmTitle = f[1];
    v.dataset.listenFilmSec = String(f[4]);
    v.setAttribute('aria-label', `Film: ${f[1]}`);
    title.textContent = f[1];
    meta.textContent = `Film ${at + 1} of ${L.films.length} · ${LEVEL_LABEL[f[3]]} · ${clock(f[4])}`;
    page.href = f[2];
    if (f[3] !== drawnRank) draw(false); else mark();
    controls();
    setAddress();
  }

  const play = () => v.play().catch(() => { say.textContent = 'Press play on the film to start.'; });

  function runFrom(i: number): void {
    if (!L) return;
    running = true;
    show(i);
    say.textContent = at === 0
      ? `Playing the ladder: ${L.films.length} films, about ${minutes(L.films)} minutes. Stop whenever you like.`
      : `Playing the ladder from film ${at + 1} of ${L.films.length}. Stop whenever you like.`;
    void play();
  }

  function stop(): void {
    running = false;
    v.pause();
    controls();
    say.textContent = `Stopped at film ${at + 1} of ${L?.films.length ?? 0}.`;
    btnAll.focus();
  }

  async function open(id: string, start = 0, fly = true): Promise<void> {
    const all = await load();
    if (!all) { sum.textContent = 'Could not load the ladders. Each idea’s page has its ladder.'; return; }
    const next = all.find((x) => x.id === id);
    if (!next) { sum.textContent = 'There is no ladder of films by that name.'; return; }
    running = false;
    L = next;
    if (select.value !== id) select.value = id;
    const levels = new Set(L.films.map((f) => f[3])).size;
    sum.textContent = `${L.name}: ${L.films.length} films at ${levels} levels, about ${minutes(L.films)} minutes, simplest at the foot of the ladder. Pick a film, or play the whole ladder.`;
    stage.hidden = false;
    drawnRank = -1;
    at = Math.max(0, Math.min(L.films.length - 1, start));
    draw(fly);
    show(at);
    say.textContent = '';
  }

  /* ---- wiring */
  form.addEventListener('submit', (e) => { e.preventDefault(); if (select.value) void open(select.value); });
  select.addEventListener('change', () => { if (select.value) void open(select.value); });
  rail.addEventListener('click', (e) => {
    const b = (e.target as HTMLElement).closest<HTMLButtonElement>('.flx-th');
    if (!b) return;
    show(Number(b.dataset.i));
    if (running) say.textContent = `Playing the ladder from film ${at + 1}.`;
    void play();
  });
  // Arrow keys move along the films in ladder order (Right or Up: the next film, deeper; Left or
  // Down: the one before, simpler), Home and End to the first and last film.
  rail.addEventListener('keydown', (e) => {
    const b = (e.target as HTMLElement).closest<HTMLButtonElement>('.flx-th');
    if (!b || !L) return;
    const k = Number(b.dataset.i);
    const to = { ArrowRight: k + 1, ArrowUp: k + 1, ArrowLeft: k - 1, ArrowDown: k - 1, Home: 0, End: L.films.length - 1 }[e.key];
    const t = to === undefined ? null : thumb(to);
    if (!t) return;
    e.preventDefault();
    t.focus();
  });
  btnAll.addEventListener('click', () => runFrom(0));
  btnHere.addEventListener('click', () => runFrom(at));
  btnPrev.addEventListener('click', () => { const was = running || !v.paused; show(at - 1); if (was) void play(); });
  btnNext.addEventListener('click', () => { const was = running || !v.paused; show(at + 1); if (was) void play(); });
  btnStop.addEventListener('click', stop);
  v.addEventListener('ended', () => {
    if (!L) return;
    const nx = L.films[at + 1];
    if (running && nx) {
      show(at + 1);
      say.textContent = `Now playing film ${at + 1} of ${L.films.length}: ${said(nx[1])}`;
      void play();
      return;
    }
    if (running) {
      running = false;
      controls();
      say.textContent = `That was the whole ladder: ${L.films.length} films, about ${minutes(L.films)} minutes.`;
      return;
    }
    say.textContent = nx ? `Next on the ladder: ${said(nx[1])} Press Next, or Play on from here to keep going.` : 'That was the last film on this ladder.';
  });

  /* ---- a link that names a ladder opens it at its film, paused */
  const params = new URLSearchParams(location.search);
  const id = params.get('ladder') ?? '';
  if (/^[a-z0-9-]{1,80}$/.test(id)) {
    const n = Math.floor(Number(params.get('at')) || 1) - 1;
    void open(id, n, false).then(() => root.scrollIntoView({ block: 'start', behavior: still.matches ? 'auto' : 'smooth' }));
  }
}
