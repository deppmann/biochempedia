/* A playlist made on the fly (2026-11-22): "Add to playlist" on any film card or film search
   result, a small tray that lists what is queued (reorder, remove, play from any film), and Play,
   which opens /films/run/?list=key,key,...&from=key: the run page that already plays a set of films
   in order, with nothing starting until the viewer presses play.

   Kept on this device only (localStorage, every access in try/catch; without storage the playlist
   lasts until the page is left). No account. The tray is src/components/FilmPlaylist.astro.

   Cards are found by `li.fc[data-f]` (src/lib/film-cards.ts and FilmCard.astro) and by
   `[data-fp-film]` (the site search's film results, which carry their data as attributes). Cards
   drawn later (the library redraws its list) get their button from a MutationObserver. */

export interface PlaylistItem {
  /** Film key (file under /explainers/ without .mp4). */
  f: string;
  t: string;
  /** Poster, length in seconds, the film's own page. */
  o: string;
  d: number;
  h: string;
}

const KEY = 'stemhop:playlist:v1';
export const MAX = 100;
const EVENT = 'stemhop-playlist-change';
let memory: PlaylistItem[] = [];

const valid = (x: unknown): x is PlaylistItem => {
  const i = x as PlaylistItem;
  return !!i && typeof i.f === 'string' && /^[a-z0-9][a-z0-9/._-]{0,160}$/i.test(i.f) && !i.f.includes('..') && typeof i.t === 'string' && typeof i.h === 'string' && i.h.startsWith('/');
};

export function readPlaylist(): PlaylistItem[] {
  try {
    const raw = localStorage.getItem(KEY);
    if (raw === null) return memory;
    const list = JSON.parse(raw);
    return Array.isArray(list) ? list.filter(valid).slice(0, MAX) : [];
  } catch {
    return memory;
  }
}
function write(list: PlaylistItem[]): void {
  memory = list.slice(0, MAX);
  try { localStorage.setItem(KEY, JSON.stringify(memory)); } catch { /* kept in memory for this page */ }
  window.dispatchEvent(new CustomEvent(EVENT));
}
export const inPlaylist = (f: string) => readPlaylist().some((x) => x.f === f);
/** Adds a film at the end; returns false when it was already there or the list is full. */
export function addFilm(item: PlaylistItem): boolean {
  const list = readPlaylist();
  if (list.some((x) => x.f === item.f) || list.length >= MAX) return false;
  write([...list, { f: item.f, t: item.t, o: item.o, d: Math.round(item.d) || 0, h: item.h }]);
  return true;
}
export const removeFilm = (f: string) => write(readPlaylist().filter((x) => x.f !== f));
export function moveFilm(f: string, by: number): void {
  const list = readPlaylist();
  const i = list.findIndex((x) => x.f === f);
  const j = i + by;
  if (i < 0 || j < 0 || j >= list.length) return;
  [list[i], list[j]] = [list[j], list[i]];
  write(list);
}
export const clearPlaylist = () => write([]);
/** The run page for the playlist, starting at film `from` (default the first). */
export function playHref(list: PlaylistItem[], from?: string): string {
  const p = new URLSearchParams();
  p.set('list', list.map((x) => x.f).join(','));
  p.set('from', from ?? list[0]?.f ?? '');
  return `/films/run/?${p.toString().replace(/%2C/g, ',').replace(/%2F/g, '/')}`;
}
export function onPlaylistChange(fn: () => void): void {
  window.addEventListener(EVENT, fn);
  window.addEventListener('storage', (e) => { if (e.key === KEY || e.key === null) fn(); });
}

const clockOf = (s: string) => { const m = /(\d+):(\d\d)/.exec(s); return m ? Number(m[1]) * 60 + Number(m[2]) : 0; };

/** A card's film, read from its markup. */
function itemOf(el: HTMLElement): PlaylistItem | null {
  if (el.dataset.fpFilm) {
    const d = el.dataset;
    return { f: d.fpFilm!, t: d.fpT ?? '', o: d.fpO ?? '', d: Number(d.fpD) || 0, h: d.fpH ?? '/' };
  }
  const a = el.querySelector<HTMLAnchorElement>(':scope > a');
  const img = el.querySelector<HTMLImageElement>('img');
  const t = el.querySelector('.t')?.textContent?.trim() ?? '';
  if (!a || !t || !el.dataset.f) return null;
  return {
    f: el.dataset.f,
    t,
    o: img?.dataset.src || img?.getAttribute('src') || '',
    d: clockOf(el.querySelector('.fc-len')?.textContent ?? ''),
    h: a.getAttribute('href') ?? '/',
  };
}

function paintButton(b: HTMLButtonElement, title: string): void {
  const on = inPlaylist(b.dataset.fpKey!);
  b.setAttribute('aria-pressed', String(on));
  b.setAttribute('aria-label', on ? `In your playlist: ${title}. Press to remove.` : `Add to playlist: ${title}`);
  b.title = on ? 'In your playlist (press to remove)' : 'Add to playlist';
  b.querySelector('.fp-add-i')!.textContent = on ? '✓' : '+';
}

/** Gives every film card under `root` an "Add to playlist" button, now and as cards are drawn. */
export function decorateCards(root: ParentNode = document, say?: (text: string) => void): void {
  const titles = new WeakMap<HTMLButtonElement, string>();
  const decorate = (el: HTMLElement) => {
    if (el.querySelector(':scope > .fp-add')) return;
    const item = itemOf(el);
    if (!item) return;
    const b = document.createElement('button');
    b.type = 'button';
    b.className = 'fp-add';
    b.dataset.fpKey = item.f;
    b.innerHTML = '<span class="fp-add-i" aria-hidden="true">+</span><span class="fp-add-t" aria-hidden="true">Playlist</span>';
    titles.set(b, item.t);
    paintButton(b, item.t);
    b.addEventListener('click', (e) => {
      e.preventDefault();
      e.stopPropagation();
      const now = itemOf(el) ?? item;
      if (inPlaylist(now.f)) { removeFilm(now.f); say?.(`Removed ${now.t} from your playlist.`); }
      else if (addFilm(now)) say?.(`Added ${now.t}. ${readPlaylist().length} in your playlist.`);
      else say?.(`Your playlist is full (${MAX} films).`);
    });
    el.append(b);
  };
  const scan = (n: ParentNode) => n.querySelectorAll<HTMLElement>('li.fc[data-f], [data-fp-film]').forEach(decorate);
  scan(root);
  new MutationObserver((records) => {
    for (const r of records) for (const n of r.addedNodes) {
      if (!(n instanceof HTMLElement)) continue;
      if (n.matches('li.fc[data-f], [data-fp-film]')) decorate(n);
      scan(n);
    }
  }).observe(root instanceof Document ? root.body : (root as Node), { childList: true, subtree: true });
  onPlaylistChange(() => {
    document.querySelectorAll<HTMLButtonElement>('button.fp-add').forEach((b) => paintButton(b, titles.get(b) ?? ''));
  });
}
