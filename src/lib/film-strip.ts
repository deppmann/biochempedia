/* The true-size strip on /films/ (2026-11-20): every film in the library as one sliver, as wide as
   the film is long, in course order, coloured by level. It is a picture of what a choice did, not a
   control: turn a level key and that level's films are laid out again, larger, at the top, with the
   rest of the library dim beneath them, so the size of the choice against the whole is in view. Ask
   for a run and its films are laid along a ruler in true minutes, numbered like the cards, with the
   time limit marked.

   It moves only when the visitor changes the view (about 400 ms), and not at all under reduced
   motion. It is hidden from assistive technology and takes no input: the same facts are in the
   sentence under it ("68 films, about 3 hours 45 minutes"), the level keys and the cards.

   One <canvas>, so 989 films cost one element. */

export interface StripFilm { d: number; level: string }
export interface StripState {
  /** Indexes (into the films given to the strip) brought forward; null for the whole library. */
  on: number[] | null;
  /** For a run: the budget in minutes, drawn as a mark on the ruler (0 for "all of them"). */
  budget?: number;
  /** Number the bricks 1, 2, 3 (a run). */
  numbered?: boolean;
}
interface Rect { x: number; y: number; w: number; h: number; a: number; n: number }

export function filmStrip(canvas: HTMLCanvasElement, films: StripFilm[]) {
  const ctx = canvas.getContext('2d');
  const still = window.matchMedia('(prefers-reduced-motion: reduce)');
  const total = films.reduce((s, f) => s + f.d, 0);
  let W = 0;
  let H = 0;
  let from: Rect[] = [];
  let to: Rect[] = [];
  let state: StripState = { on: null };
  let mark = { x: 0, a: 0, label: '' };
  let markFrom = { ...mark };
  let raf = 0;
  let colours: Record<string, string> = {};
  const readColours = () => {
    const cs = getComputedStyle(canvas);
    colours = {};
    for (const f of films) colours[f.level] ??= cs.getPropertyValue(`--lv-${f.level || 'methods'}`).trim() || '#888';
    colours.ink = cs.getPropertyValue('--ddp-color-ink').trim() || '#222';
    colours.bg = cs.getPropertyValue('--ddp-color-bg').trim() || '#fff';
  };

  /* Bricks in rows, left to right, a brick never split across rows; a small gap where the level changes. */
  const flow = (idx: number[], y0: number, rows: number, rowH: number, gap: number, px: number, a: number, out: Rect[], numbered = false) => {
    let x = 0;
    let row = 0;
    let prev = '';
    idx.forEach((i, k) => {
      const w = Math.max(0.6, films[i].d * px);
      if (prev && films[i].level !== prev) x += Math.min(4, W * 0.006);
      if (x + w > W + 0.5 && row < rows - 1) { row++; x = 0; }
      out[i] = { x, y: y0 + row * (rowH + gap), w: Math.min(w, Math.max(0.6, W - x)), h: rowH, a, n: numbered ? k + 1 : 0 };
      x += w;
      prev = films[i].level;
    });
  };
  const layout = (s: StripState): Rect[] => {
    const out: Rect[] = new Array(films.length);
    const all = films.map((_, i) => i);
    const rowsAll = W < 560 ? 5 : 3;
    const gap = 2;
    if (!s.on) {
      const rowH = (H - gap * (rowsAll - 1)) / rowsAll;
      flow(all, 0, rowsAll, rowH, gap, (W * rowsAll * 0.965) / total, 1, out);
      mark = { x: 0, a: 0, label: '' };
      return out;
    }
    const on = new Set(s.on);
    const rest = all.filter((i) => !on.has(i));
    const restH = rest.length ? Math.max(6, H * 0.16) : 0;
    const topH = H - restH - (rest.length ? 5 : 0);
    const secs = s.on.reduce((t, i) => t + films[i].d, 0) || 1;
    if (s.numbered) {
      // A run: one row, in true minutes. The budget, when there is one, sits at four fifths of the width.
      const span = Math.max(secs, (s.budget ?? 0) * 60) * (s.budget ? 1.25 : 1.02);
      const px = W / span;
      flow(s.on, 0, 1, topH, 0, px, 1, out, true);
      mark = s.budget ? { x: s.budget * 60 * px, a: 1, label: `${s.budget} min` } : { x: 0, a: 0, label: '' };
    } else {
      // A choice: its films as large as they will go in the top band (at most a thumb's width each).
      let rows = 1;
      let px = Math.min(0.5, (W * 0.97) / secs);
      const maxRows = W < 560 ? 4 : 3;
      while (rows < maxRows && secs * px < W * 0.5 * rows && px < 0.5) rows++;
      px = Math.min(0.5, (W * rows * 0.94) / secs);
      if (secs * px > W * rows) px = (W * rows * 0.94) / secs;
      rows = Math.min(maxRows, Math.max(1, Math.ceil((secs * px) / (W * 0.94))));
      const rowH = (topH - gap * (rows - 1)) / rows;
      flow(s.on, 0, rows, rowH, gap, px, 1, out);
      mark = { x: 0, a: 0, label: '' };
    }
    if (rest.length) flow(rest, H - restH, 1, restH, 0, W / (total - secs + 1), 0.3, out);
    return out;
  };

  const draw = (p: number) => {
    if (!ctx) return;
    const dpr = Math.min(3, window.devicePixelRatio || 1);
    ctx.setTransform(dpr, 0, 0, dpr, 0, 0);
    ctx.clearRect(0, 0, W, H);
    const e = p < 0.5 ? 4 * p * p * p : 1 - Math.pow(-2 * p + 2, 3) / 2;
    const mix = (a: number, b: number) => a + (b - a) * e;
    for (let i = 0; i < films.length; i++) {
      const A = from[i] ?? to[i];
      const B = to[i];
      if (!B) continue;
      const w = mix(A.w, B.w);
      ctx.globalAlpha = mix(A.a, B.a);
      ctx.fillStyle = colours[films[i].level];
      const inset = w > 2.4 ? 0.6 : 0;
      ctx.fillRect(mix(A.x, B.x), mix(A.y, B.y), Math.max(0.5, w - inset), mix(A.h, B.h));
      if (B.n && e > 0.7 && w > 15) {
        ctx.globalAlpha = (e - 0.7) / 0.3;
        ctx.fillStyle = colours.bg;
        ctx.font = '600 12px system-ui, sans-serif';
        ctx.textBaseline = 'middle';
        ctx.fillText(String(B.n), mix(A.x, B.x) + 5, mix(A.y, B.y) + mix(A.h, B.h) / 2 + 0.5);
      }
    }
    const ma = mix(markFrom.a, mark.a);
    if (ma > 0.01) {
      const x = Math.min(W - 1, mix(markFrom.x || mark.x, mark.x));
      ctx.globalAlpha = ma;
      ctx.fillStyle = colours.ink;
      ctx.fillRect(x, 0, 1.5, H);
      ctx.font = '12px system-ui, sans-serif';
      ctx.textBaseline = 'top';
      const label = mark.label || markFrom.label;
      const tw = ctx.measureText(label).width;
      ctx.fillText(label, x + 6 + tw > W ? x - tw - 6 : x + 6, 2);
    }
    ctx.globalAlpha = 1;
  };

  const size = () => {
    const r = canvas.getBoundingClientRect();
    if (!r.width) return false;
    W = r.width;
    H = r.height;
    const dpr = Math.min(3, window.devicePixelRatio || 1);
    canvas.width = Math.round(W * dpr);
    canvas.height = Math.round(H * dpr);
    return true;
  };
  const settle = () => { from = to; markFrom = { ...mark }; };
  const set = (s: StripState, animate = true) => {
    cancelAnimationFrame(raf);
    state = s;
    if (!W && !size()) return;
    const prev = to.length ? to : null;
    const prevMark = { ...mark };
    to = layout(s);
    from = prev ?? to;
    markFrom = prevMark;
    if (!animate || !prev || still.matches) { settle(); draw(1); return; }
    const t0 = performance.now();
    const step = (now: number) => {
      const p = Math.min(1, (now - t0) / 400);
      draw(p);
      if (p < 1) raf = requestAnimationFrame(step); else settle();
    };
    raf = requestAnimationFrame(step);
  };
  const redraw = () => { if (size()) { readColours(); to = []; set(state, false); } };
  readColours();
  new ResizeObserver(redraw).observe(canvas);
  window.matchMedia('(prefers-color-scheme: dark)').addEventListener('change', redraw);
  return { set };
}
