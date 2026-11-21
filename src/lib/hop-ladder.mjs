/* The ladder: the site's one picture of hopping. An upright ladder with a rung for each level
   where an idea is taught; each rung carries its lesson and the note on what that level adds, and
   Hex stands on the rung the reader is on.

   One pure function per size, returning HTML (inline SVG plus real text, no image), so the same
   drawing is made at build time (src/components/hop/Ladder.astro) and at run time by any client
   script that has graph data (the idea search does; the film theater can). Styles: src/styles/hop.css.

     ladderHtml(idea, opts)   full: the ladder that houses the material
     ladderGlyph(mask, opts)  compact or tiny: the ladder as a small mark beside a line of text

   What the drawing promises, and the code keeps:
   - Hex marks "you are here". It is not a score: nothing fills, counts or unlocks, and every rung
     is drawn the same whether or not the reader has been there.
   - Up the ladder is deeper, down is simpler (the words stay "Simpler" and "Deeper"). The markup is
     written as it is drawn, deepest rung first, so the eye, the Tab key and a screen reader all
     move the same way; the list's label says the order.
   - With `window`, only the reader's rung and the rung below it are shown at first, so a phone
     opens on the reader's own rung with Hex on it, never on a deeper rung. One button shows the
     rest and stays in place.
   - A level with no lesson is one short line between two rungs, with the rails broken: honest and small. */
import { LEVEL_KEYS, LEVEL_LABEL, LEVEL_SHORT, numWord, andList } from './hop-words.mjs';

const esc = (s) => String(s ?? '').replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;').replace(/"/g, '&quot;');
const mmss = (s) => `${Math.floor(s / 60)}:${String(Math.round(s) % 60).padStart(2, '0')}`;

/* For a gap the three college bands are one place (see stepNote in hop-words.mjs). */
const BAND = [0, 1, 2, 3, 3, 3, 4];
const BAND_AT = ['for ages 5 to 10', 'at grade 7', 'at high school', 'at college level', 'at graduate level'];

/* Hex, standing: the same drawing as the "stand" pose in src/components/Hex.astro (navy line, gold
   bonds and feet), as a string so a client script can place it. Keep the two in step. */
export const HEX_STAND = '<svg class="hl-hex" viewBox="0 0 64 72" width="38" height="43" aria-hidden="true" focusable="false">'
  + '<path class="hl-hex-ink" d="M27 48 L25.5 60 M37 48 L38.5 60"/><path class="hl-hex-gold" d="M22.5 61 H27.5 M36.5 61 H41.5"/>'
  + '<path class="hl-hex-ink" d="M14.7 32 L8 39 M49.3 32 L56 39"/>'
  + '<path class="hl-hex-ink hl-hex-body" d="M32 10 L49.3 20 L49.3 40 L32 50 L14.7 40 L14.7 20 Z"/>'
  + '<path class="hl-hex-gold" d="M32 14.8 L45.2 22.4 M45.2 37.6 L32 45.2 M18.8 37.6 L18.8 22.4"/>'
  + '<circle class="hl-hex-fill" cx="26.5" cy="28" r="2.2"/><circle class="hl-hex-fill" cx="37.5" cy="28" r="2.2"/>'
  + '<path class="hl-hex-ink hl-hex-thin" d="M28 34.5 Q32 38.5 36 34.5"/></svg>';

/** The rails and the rung of one row. Percent heights let the rails run the row's full height. */
const art = (kind, hex) => `<span class="hl-art" aria-hidden="true"><svg class="hl-svg" width="56" height="100%" focusable="false">`
  + `<line class="hl-rail${kind === 'gap' ? ' hl-broken' : ''}" x1="12" y1="0" x2="12" y2="100%"/><line class="hl-rail${kind === 'gap' ? ' hl-broken' : ''}" x1="44" y1="0" x2="44" y2="100%"/>`
  + (kind === 'gap' ? '' : '<line class="hl-rung" x1="12" y1="38" x2="44" y2="38"/>')
  + (kind === 'here' ? '<line class="hl-rung-gold" x1="14" y1="38" x2="42" y2="38"/>' : '')
  + `</svg>${hex ? HEX_STAND : ''}</span>`;

/**
 * The rows of a ladder, simplest first: one per level that has a lesson, and one short gap row
 * wherever a whole level (grade 7, high school, all of college) lies between two rungs with no lesson.
 * @param {number[]} [also] levels the page links by hand elsewhere: no gap is claimed there
 * @param {{ short?: string, name: string, rungs: Rung[] }} idea  rungs: { rank, slug, title, href, courseTitle, adds?, minutes?, film?, questions?, sol? }
 */
export function ladderRows(idea, also = []) {
  const ranks = [...new Set(idea.rungs.map((r) => r.rank))].sort((a, b) => a - b);
  const rows = [];
  ranks.forEach((rank, i) => {
    if (i > 0) {
      const missing = [];
      for (let b = BAND[ranks[i - 1]] + 1; b < BAND[rank]; b++) if (!also.includes(b)) missing.push(b);
      if (missing.length) rows.push({ kind: 'gap', text: missing.length > 2 ? `No lesson on ${idea.short ?? 'this idea'} at the ${numWord(missing.length)} levels in between yet.` : `No lesson on ${idea.short ?? 'this idea'} ${andList(missing.map((b) => BAND_AT[b]), 'or')} yet.` });
    }
    rows.push({ kind: 'level', rank, rungs: idea.rungs.filter((r) => r.rank === rank) });
  });
  return rows;
}

/**
 * The full ladder.
 * @param {{ id: string, name: string, short?: string, rungs: Rung[] }} idea
 * @param {{
 *   here?: string | null,     slug of the lesson the reader is on: Hex stands on its rung, the lesson is in bold, not a link
 *   hereRank?: number | null, or only a level (a film, a chosen level): Hex stands on that rung if it exists
 *   hereLabel?: string,       words after the level's name on that rung when there is no lesson ("the level you chose")
 *   hex?: boolean,            draw Hex (default true). Pass false for a second ladder in the same view: one Hex in view
 *   window?: boolean,         show the reader's rung and the rung below it first (default: true when `here` is set)
 *   facts?: boolean,          course, minutes, film and practice questions under each lesson (default true)
 *   from?: string | null,     lesson links carry ?from=<slug> and go to the top of the lesson (default: `here`)
 *   also?: number[],          levels (0 ages 5 to 10, 1 grade 7, 2 high school, 3 college, 4 graduate) that the page
 *                             links by hand elsewhere: the ladder then does not say "no lesson" there
 *   play?: { href: string, n: number, minutes: number, from: number, to: number } | null   the "Play the ladder" link
 * }} [o]
 * @returns {string} HTML
 */
export function ladderHtml(idea, o = {}) {
  const { here = null, hex = true, facts = true, play = null, also = [], hereLabel = '' } = o;
  const from = o.from === undefined ? here : o.from;
  const rows = ladderRows(idea, also);
  const levels = rows.filter((r) => r.kind === 'level');
  const hereRank = here ? idea.rungs.find((r) => r.slug === here)?.rank ?? null : o.hereRank ?? null;
  const onLadder = hereRank !== null && levels.some((r) => r.rank === hereRank);
  // The window: the reader's rung and the rung below it, where a reader at a blind spot looks
  // first. On the lowest rung, the rung above. Nobody scrolls past a deeper rung to find their own.
  const at = levels.findIndex((r) => r.rank === hereRank);
  const near = new Set(at < 0 ? [] : [levels[at].rank, (levels[at - 1] ?? levels[at + 1])?.rank]);
  near.delete(undefined);
  const windowed = (o.window ?? Boolean(here)) && onLadder && levels.length > near.size;
  const far = (rank) => windowed && !near.has(rank);
  const gapFar = (i) => windowed && (rows[i - 1]?.kind === 'level' && far(rows[i - 1].rank) || rows[i + 1]?.kind === 'level' && far(rows[i + 1].rank));

  const lesson = (r) => {
    const mine = r.slug === here;
    const href = from && !mine ? `/lessons/${r.slug}/?from=${from}` : r.href;
    const f = [];
    if (facts) {
      if (r.courseTitle) f.push(esc(r.courseTitle));
      if (r.minutes) f.push(`about ${r.minutes} min`);
      if (r.film) f.push(`<a href="${esc(r.film.href)}" aria-label="film ${mmss(r.film.seconds)}: ${esc(r.film.title)}">film ${mmss(r.film.seconds)}</a>`);
      if (r.questions) f.push(`<a href="/mcat/practice/?lesson=${esc(r.slug)}" aria-label="${r.questions} practice ${r.questions === 1 ? 'question' : 'questions'} on ${esc(r.title)}">${r.questions} practice ${r.questions === 1 ? 'question' : 'questions'}</a>`);
      if (r.sol?.length) f.push(`Virginia ${esc(r.sol.join(', '))}`);
    }
    return `<div class="hl-lesson${mine ? ' is-here' : ''}">`
      + (mine ? `<p class="hl-title"><strong>${esc(r.title)}</strong> <span class="hl-this">· this lesson</span></p>` : `<p class="hl-title"><a href="${esc(href)}">${esc(r.title)}</a>${r.also ? ' <span class="hl-this">· also at this level, picked for this lesson</span>' : ''}</p>`)
      + (r.adds ? `<p class="hl-adds">${esc(r.adds)}</p>` : '')
      + (r.rank === 0 && !mine ? '<p class="hl-adds hl-grownup">A grown-up runs this one; its safety notes are in the guide.</p>' : '')
      + (f.length ? `<p class="hl-facts">${f.join(' · ')}</p>` : '')
      + '</div>';
  };

  // Drawn as it is written: the deepest rung first, the simplest at the foot.
  const html = rows.map((row, i) => row.kind === 'gap'
    ? `<li class="hl-row hl-gap${gapFar(i) ? ' hl-far' : ''}">${art('gap')}<p class="hl-gap-t">${esc(row.text)}</p></li>`
    : `<li class="hl-row hl-level${row.rank === hereRank ? ' hl-here' : ''}${far(row.rank) ? ' hl-far' : ''}" data-hop-level="${LEVEL_KEYS[row.rank]}">${art(row.rank === hereRank ? 'here' : 'level', hex && row.rank === hereRank)}`
      + `<div class="hl-text"><p class="hl-lvl">${esc(LEVEL_LABEL[row.rank])}${row.rank === hereRank && !here && hereLabel ? `<span class="hl-you"> · ${esc(hereLabel)}</span>` : ''}<span class="hl-you" data-hop-you hidden> · the level you chose</span></p>${row.rungs.map(lesson).join('')}</div></li>`).reverse().join('');

  const n = numWord(levels.length);
  const all = windowed ? `<p class="hl-all"><button type="button" class="hl-all-btn" data-hl-all aria-expanded="false" data-more="Show all ${n} levels" data-fewer="Show fewer levels">Show all ${n} levels</button></p>` : '';
  const playLink = play ? `<p class="hl-play"><a href="${esc(play.href)}">Play the ladder</a><span> · ${play.n} films, about ${play.minutes} min, from ${esc(LEVEL_SHORT[play.from])} to ${esc(LEVEL_SHORT[play.to])}. Each film waits for you to press play.</span></p>` : '';
  return `<div class="hop-ladder hl-full${windowed ? ' hl-windowed' : ''}" data-hop-ladder="${esc(idea.id)}">${all}<ol class="hl-rows" aria-label="${esc(idea.name)}: lessons from the deepest level to the simplest">${html}</ol>${playLink}</div>`;
}

/**
 * Wire the "Show all levels" button of every windowed ladder under `root`. The button stays where
 * it is and keeps focus; it says what it will do next. Safe to call again.
 * @param {ParentNode} [root]
 */
export function wireLadders(root = document) {
  root.querySelectorAll('[data-hl-all]').forEach((btn) => {
    if (btn.hasAttribute('data-wired')) return;
    btn.setAttribute('data-wired', '');
    btn.addEventListener('click', () => {
      const ladder = btn.closest('.hop-ladder');
      if (!ladder) return;
      const open = ladder.classList.toggle('hl-windowed') === false;
      btn.setAttribute('aria-expanded', String(open));
      btn.textContent = btn.getAttribute(open ? 'data-fewer' : 'data-more');
    });
  });
}

/**
 * The ladder as a small mark: seven places from ages 5 to 10 (bottom) to graduate (top), a rung
 * where the idea has a lesson, and a gold hexagon on `here`. A picture only (aria-hidden): the
 * words beside it must say the same thing (compactLine() or taughtAt() in hop-words.mjs).
 * @param {number} mask levels with a lesson (bit 0 = ages 5 to 10)
 * @param {{ here?: number | null, size?: 'compact' | 'tiny' }} [o]  compact 20×44 px, tiny 14×31 px
 */
export function ladderGlyph(mask, o = {}) {
  const { here = null, size = 'compact' } = o;
  const y = (rank) => 39 - rank * 5.6;
  let s = '<line class="hl-rail" x1="5" y1="2" x2="5" y2="42"/><line class="hl-rail" x1="15" y1="2" x2="15" y2="42"/>';
  for (let r = 0; r < 7; r++) if (mask & (1 << r)) s += `<line class="hl-rung" x1="5" y1="${y(r).toFixed(1)}" x2="15" y2="${y(r).toFixed(1)}"/>`;
  if (here !== null && here >= 0) {
    const c = y(here);
    const pts = [0, 1, 2, 3, 4, 5].map((k) => `${(10 + 4.6 * Math.sin((k * Math.PI) / 3)).toFixed(1)},${(c - 4.6 * Math.cos((k * Math.PI) / 3)).toFixed(1)}`).join(' ');
    s += `<polygon class="hl-mark" points="${pts}"/>`;
  }
  const [w, h] = size === 'tiny' ? [14, 31] : [20, 44];
  return `<svg class="hop-ladder hl-glyph hl-${size}" viewBox="0 0 20 44" width="${w}" height="${h}" aria-hidden="true" focusable="false">${s}</svg>`;
}
