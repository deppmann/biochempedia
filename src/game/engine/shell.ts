/* =============================================================================
   Shell — the shared chrome every game plugs into.
   -----------------------------------------------------------------------------
   The arcade is now GAME-FIRST: a hub lists the games, each game owns its own
   pathway/level selection. The shell provides the HUD (back / title / score /
   mute), a single swappable stage, the mascot, a generic results overlay, and a
   reusable pathway picker — so each game module is just its own core loop.
   ============================================================================ */
import type { Pathway } from '../types';
import { el, clear, prefersReducedMotion } from './dom';
import { sfx, isMuted, setMuted, initSound } from './sound';
import * as store from './storage';
import type { Medal, ModeId } from './storage';
import { confettiBurst } from './confetti';
import { quip } from './quips';

const MEDAL_EMOJI: Record<Medal, string> = { none: '', bronze: '🥉', silver: '🥈', gold: '🥇' };

export interface ResultOpts {
  recordId: string;
  mode: ModeId;
  won: boolean;
  medal: Medal;
  score: number;
  headline: string;
  lines: Array<[string, string]>;
  funFact?: string;
  replay: () => void;
}

export interface Shell {
  root: HTMLElement;
  stage: HTMLElement;
  /** Swap the stage contents (with entrance + scroll-to-top). */
  setStage(node: HTMLElement): void;
  /** Set the breadcrumb + wire the Back button (hidden if onBack omitted). */
  setCrumb(text: string, onBack?: () => void): void;
  /** Mascot line + face. */
  setMascot(text: string, face?: string): void;
  /** Generic results overlay (records score, confetti on gold). */
  showResults(o: ResultOpts): void;
  /** A reusable pathway-select screen. */
  pathwayPicker(opts: { title: string; sub: string; pathways: Pathway[]; mode: ModeId; onPick: (p: Pathway) => void; onBack: () => void }): void;
  /** Go back to the hub home. */
  goHome(): void;
  medalEmoji(m: Medal): string;
}

export function createShell(root: HTMLElement, goHome: () => void): Shell {
  initSound();

  const back = el('button.arc-back', { type: 'button', 'aria-label': 'Back' }, '‹ Back');
  const crumb = el('div.arc-crumb', null, 'Metabolism Arcade');
  const streak = el('span.arc-stat');
  const atp = el('span.arc-stat');
  const mute = el('button.arc-mute', { type: 'button' });
  const syncMute = () => {
    mute.textContent = isMuted() ? '🔇' : '🔊';
    mute.setAttribute('aria-label', isMuted() ? 'Unmute sound' : 'Mute sound');
  };
  mute.addEventListener('click', () => { setMuted(!isMuted()); syncMute(); if (!isMuted()) sfx.select(); });
  syncMute();

  const hud = el('header.arc-hud', null, back, crumb, el('div.arc-stats', null, streak, atp, mute));
  const stage = el('div.arc-stage');
  const mascotEl = el('div.arc-mascot', { 'aria-hidden': 'true' }, '⚡');
  const bubbleEl = el('div.arc-bubble', { role: 'status', 'aria-live': 'polite' });
  root.append(hud, stage, el('div.arc-mascot-wrap', null, bubbleEl, mascotEl));

  let backHandler: (() => void) | null = null;
  back.addEventListener('click', () => { sfx.select(); backHandler?.(); });

  function syncStats(): void {
    const s = store.studyStreak();
    streak.textContent = `🔥 ${s}d`;
    streak.title = 'Day study streak';
    atp.textContent = `⚡ ${store.totalAtp().toLocaleString()}`;
    atp.title = 'Lifetime ATP earned';
  }

  function setCrumb(text: string, onBack?: () => void): void {
    crumb.textContent = text;
    backHandler = onBack ?? null;
    back.style.visibility = onBack ? 'visible' : 'hidden';
    syncStats();
  }

  function setMascot(text: string, face = '⚡'): void {
    mascotEl.textContent = face;
    bubbleEl.textContent = text;
    bubbleEl.classList.remove('is-pop');
    void bubbleEl.offsetWidth;
    if (!prefersReducedMotion()) bubbleEl.classList.add('is-pop');
  }

  function setStage(node: HTMLElement): void {
    clear(stage);
    if (!prefersReducedMotion()) node.classList.add('arc-in');
    stage.append(node);
    const header = document.querySelector<HTMLElement>('.site-header');
    const offset = (header?.offsetHeight ?? 0) + 8;
    const y = root.getBoundingClientRect().top + window.scrollY - offset;
    if (window.scrollY > y + 4 || window.scrollY < y - 200) {
      window.scrollTo({ top: Math.max(0, y), behavior: prefersReducedMotion() ? 'auto' : 'smooth' });
    }
  }

  function showResults(o: ResultOpts): void {
    store.recordResult(o.recordId, o.mode, o.score, o.medal, o.score);
    syncStats();
    if (o.medal === 'gold' || o.won) sfx.win(); else sfx.lose();
    setMascot(quip(o.won ? 'win' : 'lose'), o.won ? '🏆' : '⚡');

    const card = el('div.arc-results.card');
    card.append(
      el('div.arc-results-medal', { 'aria-hidden': 'true' }, o.medal !== 'none' ? MEDAL_EMOJI[o.medal] : (o.won ? '🎉' : '🧬')),
      el('h2.arc-results-head', null, o.headline),
      el('p.arc-results-medaltext', null, o.medal !== 'none' ? `${o.medal.toUpperCase()} MEDAL` : (o.won ? 'Cleared' : 'Give it another run')),
    );
    const stats = el('dl.arc-results-stats');
    for (const [k, v] of o.lines) stats.append(el('dt', null, k), el('dd', null, v));
    stats.append(el('dt', null, 'ATP banked'), el('dd', null, `⚡ ${o.score.toLocaleString()}`));
    card.append(stats);
    if (o.funFact) card.append(el('p.arc-results-fact', null, el('strong', null, 'Did you know — '), o.funFact));

    const actions = el('div.arc-results-actions');
    const again = el('button.arc-btn.is-primary', { type: 'button' }, '↻ Play again');
    again.addEventListener('click', () => { sfx.select(); o.replay(); });
    const homeBtn = el('button.arc-btn', { type: 'button' }, '⌂ All games');
    homeBtn.addEventListener('click', () => { sfx.select(); goHome(); });
    actions.append(again, homeBtn);
    card.append(actions);

    const overlay = el('div.arc-overlay');
    overlay.append(card);
    setStage(overlay);
    if (o.medal === 'gold') confettiBurst(card);
  }

  function pathwayPicker(opts: { title: string; sub: string; pathways: Pathway[]; mode: ModeId; onPick: (p: Pathway) => void; onBack: () => void }): void {
    setCrumb(opts.title, opts.onBack);
    setMascot('Pick a pathway to play.', '🎛️');
    const wrap = el('div.arc-home');
    wrap.append(el('p.arc-eyebrow', null, opts.title), el('p.arc-lede', null, opts.sub));
    const grid = el('div.arc-cabinets');
    for (const p of opts.pathways) {
      const best = store.getBest(p.id, opts.mode);
      const cab = el('button.arc-cabinet', { type: 'button' });
      cab.append(
        el('span.arc-cab-emoji', { 'aria-hidden': 'true' }, p.emoji),
        el('span.arc-cab-name', null, p.name),
        el('span.arc-cab-tag', null, p.tagline),
        el('span.arc-cab-meta', null,
          el('span.arc-stars', { 'aria-label': `Difficulty ${p.difficulty} of 3` }, '★'.repeat(p.difficulty) + '☆'.repeat(3 - p.difficulty)),
          best ? el('span.arc-cab-medal', null, `${MEDAL_EMOJI[best.medal]} ${best.score.toLocaleString()}`) : el('span.arc-cab-cleared', null, 'new')),
        el('span.arc-cab-play', { 'aria-hidden': 'true' }, 'PLAY ▶'),
      );
      cab.addEventListener('click', () => { sfx.select(); opts.onPick(p); });
      grid.append(cab);
    }
    wrap.append(grid);
    setStage(wrap);
  }

  syncStats();
  return { root, stage, setStage, setCrumb, setMascot, showResults, pathwayPicker, goHome, medalEmoji: (m) => MEDAL_EMOJI[m] };
}
