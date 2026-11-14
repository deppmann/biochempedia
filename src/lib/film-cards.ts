/* Film cards in the browser (2026-11-14): the markup src/components/FilmCard.astro renders on the
   server, built from /films/list.json for the cards /films/ loads on demand, plus the two things
   every card list does once scripts run: "watched" marks and the take-home preview on hover. */
import { loadFilms, isWatched, onFilmsChange } from './film-progress';

/** One film in /films/list.json (short keys keep the file small). */
export interface ListFilm {
  /** Film key (file under /explainers/ without .mp4). */
  f: string;
  t: string;
  /** Kind and the card badge ("First film", "Part 2 of 4"). */
  k: string;
  b: string;
  /** Course slug ("" for a method film) and level key ("" for a method film). */
  c: string;
  s: string;
  /** Lesson title, when the film belongs to a lesson. */
  l?: string;
  h: string;
  /** Poster path, length in seconds, rewrite date, first take-home. */
  o: string;
  d: number;
  r?: string;
  th?: string;
  /** Course-order position. */
  i: number;
}
export interface FilmList {
  count: number;
  courses: Record<string, string>;
  levels: Record<string, string>;
  films: ListFilm[];
}

const esc = (s: string) => s.replace(/[&<>"]/g, (c) => ({ '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;' })[c]!);
export const clock = (sec: number) => `${Math.floor(sec / 60)}:${String(Math.round(sec % 60)).padStart(2, '0')}`.replace(/:60$/, ':59');

/** The same markup as FilmCard.astro. */
export function cardHTML(f: ListFilm, list: FilmList): string {
  const course = f.c ? list.courses[f.c] : 'Methods library';
  const level = f.s ? `<span class="fc-s"> · ${esc(list.levels[f.s] ?? '')}</span>` : '';
  return `<li class="fc" data-f="${esc(f.f)}"><a href="${esc(f.h)}"><span class="fc-pic"><img src="${esc(f.o)}" alt="" width="320" height="180" loading="lazy" decoding="async"><span class="fc-kind k-${esc(f.k)}">${esc(f.b)}</span><span class="fc-len"><span class="visually-hidden">Length </span>${clock(f.d)}</span></span><span class="t">${esc(f.t)}</span><span class="m"><span class="fc-c">${esc(course)}</span>${level}</span>${f.l ? `<span class="l">${esc(f.l)}</span>` : ''}</a>${f.th ? `<details class="fc-th"><summary>Take-home</summary><p>${esc(f.th)}</p></details>` : ''}</li>`;
}

/** Add or remove the "Watched" mark on every card under `root`; returns the keys marked. */
export function markCards(root: ParentNode): void {
  const r = loadFilms();
  for (const li of root.querySelectorAll<HTMLElement>('li[data-f]')) {
    const seen = isWatched(r, li.dataset.f!);
    if (seen === li.classList.contains('is-seen')) continue;
    li.classList.toggle('is-seen', seen);
    const pic = li.querySelector('.fc-pic, .pq-pic');
    pic?.querySelector('.fc-seen')?.remove();
    if (seen && pic) {
      const s = document.createElement('span');
      s.className = 'fc-seen';
      s.textContent = '✓ Watched';
      pic.append(s);
    }
  }
}

/** "7 of 26 watched" beside each element with data-seen-of="key key key". */
export function countSeen(root: ParentNode): void {
  const r = loadFilms();
  for (const el of root.querySelectorAll<HTMLElement>('[data-seen-of]')) {
    const keys = el.dataset.seenOf!.split(' ').filter(Boolean);
    const n = keys.filter((k) => isWatched(r, k)).length;
    el.textContent = n ? `${n} of ${keys.length} watched` : '';
    el.hidden = n === 0;
  }
}

/** Marks and counts now and whenever the record changes (in this tab or another). */
export function liveMarks(root: ParentNode = document): void {
  onFilmsChange(() => { markCards(root); countSeen(root); });
}

/** A pointer that can hover opens a card's take-home while it rests on the card. A tap, a click
 *  or Enter on "Take-home" still toggles it as usual, and one opened that way stays open. */
export function hoverPreviews(root: HTMLElement): void {
  if (!window.matchMedia('(hover: hover) and (pointer: fine)').matches) return;
  const byHover = new WeakSet<HTMLDetailsElement>();
  root.addEventListener('pointerover', (e) => {
    const li = (e.target as Element).closest?.('li.fc');
    const d = li?.querySelector<HTMLDetailsElement>('details.fc-th');
    if (!d || d.open) return;
    d.open = true;
    byHover.add(d);
  });
  root.addEventListener('pointerout', (e) => {
    const li = (e.target as Element).closest?.('li.fc');
    if (!li || li.contains(e.relatedTarget as Node | null)) return;
    const d = li.querySelector<HTMLDetailsElement>('details.fc-th');
    if (d && byHover.has(d)) { d.open = false; byHover.delete(d); }
  });
  // Clicking "Take-home" while a hover has it open keeps it open instead of closing it.
  root.addEventListener('click', (e) => {
    const s = (e.target as Element).closest?.('details.fc-th > summary');
    const d = s?.parentElement as HTMLDetailsElement | undefined;
    if (d && byHover.has(d)) { e.preventDefault(); byHover.delete(d); }
  });
}
