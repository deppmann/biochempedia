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
import { getPathway } from '../data';
import type { LessonCtx } from './launch';

const MEDAL_EMOJI: Record<Medal, string> = { none: '', bronze: '🥉', silver: '🥈', gold: '🥇' };
const MEDAL_LABEL: Record<Medal, string> = { none: '', bronze: 'Bronze', silver: 'Silver', gold: 'Gold' };

/** Strip decorative emoji (the arcade chrome stays calm; games may still pass
 *  emoji in their text and the shell quietly drops them). */
const EMOJI_RE = /[\p{Extended_Pictographic}\u{1F3FB}-\u{1F3FF}\u200D\uFE0F]+\s*/gu;
export function plain(s: string): string {
  return s.replace(EMOJI_RE, '').replace(/\s{2,}/g, ' ').trim();
}

/** Pathways whose own `lessonSlug` points at a broader chapter but which have
 *  a dedicated lesson of their own. */
const LESSON_OVERRIDE: Record<string, string> = { gluconeogenesis: 'gluconeogenesis' };

/** Display names for lessons that cover more than one pathway. */
const LESSON_TITLE: Record<string, string> = {
  'integration-of-metabolism': 'Integration of Metabolism',
  'fatty-acid-degradation': 'Fatty Acid Degradation',
  'protein-turnover-amino-acid-catabolism': 'Amino Acid Catabolism',
};

export interface LessonLink { title: string; href: string }

/** Lesson link for a pathway id (also used by games that pass `lessons`). */
export function lessonFor(pathwayId: string): LessonLink | null {
  const p = getPathway(pathwayId);
  if (!p) return null;
  const slug = LESSON_OVERRIDE[pathwayId] ?? p.lessonSlug;
  return slug ? { title: LESSON_TITLE[slug] ?? p.name, href: `/lessons/${slug}/` } : null;
}

export interface ResultOpts {
  recordId: string;
  mode: ModeId;
  won: boolean;
  medal: Medal;
  score: number;
  headline: string;
  lines: Array<[string, string]>;
  funFact?: string;
  /** Optional lesson links to offer after the run. If omitted, the shell derives
   *  one from `recordId` when it is a pathway id. */
  lessons?: LessonLink[];
  /** Shorthand for a single lesson link ("Read the lesson →"). */
  lessonHref?: string;
  replay: () => void;
}

export interface Shell {
  root: HTMLElement;
  stage: HTMLElement;
  /** Swap the stage contents (with entrance + scroll-to-top). */
  setStage(node: HTMLElement): void;
  /** Set the breadcrumb + wire the Back button (not rendered at all if onBack omitted). */
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

export function createShell(root: HTMLElement, goHome: () => void, lesson?: LessonCtx): Shell {
  initSound();

  // The Back button is created once but only attached to the DOM while there is
  // somewhere to go back to (no hidden placeholder, so the title never gets a gap).
  const back = el('button.arc-back', { type: 'button', 'aria-label': 'Back' }, '‹ Back');
  const crumb = el('div.arc-crumb', null, 'Metabolism Arcade');
  const streak = el('span.arc-stat');
  const atp = el('span.arc-stat');
  const mute = el('button.arc-mute', { type: 'button' });
  const syncMute = () => {
    mute.textContent = isMuted() ? 'Sound off' : 'Sound on';
    mute.setAttribute('aria-label', isMuted() ? 'Unmute sound' : 'Mute sound');
    mute.setAttribute('aria-pressed', String(isMuted()));
  };
  mute.addEventListener('click', () => { setMuted(!isMuted()); syncMute(); if (!isMuted()) sfx.select(); });
  syncMute();

  // Opened from a lesson: the Back button always returns there, and says so.
  const lessonHref = lesson ? `/lessons/${lesson.slug}/` : '';
  const fromNote = lesson ? el('span.arc-from', null, `from Lesson ${lesson.n}`) : null;
  const hud = el('header.arc-hud', null, crumb, ...(fromNote ? [fromNote] : []), el('div.arc-stats', null, streak, atp, mute));
  const stage = el('div.arc-stage');
  const mascotEl = el('div.arc-mascot', { 'aria-hidden': 'true' }, '⚡');
  const bubbleEl = el('div.arc-bubble', { role: 'status', 'aria-live': 'polite' });
  root.append(hud, stage, el('div.arc-mascot-wrap', null, bubbleEl, mascotEl));

  let backHandler: (() => void) | null = null;
  if (lesson) {
    back.textContent = `‹ ${plain(lesson.title).split(":")[0].trim()}`;
    back.setAttribute('aria-label', `Back to the ${plain(lesson.title)} lesson`);
  }
  back.addEventListener('click', () => {
    sfx.select();
    if (lesson) { window.location.href = lessonHref; return; }
    backHandler?.();
  });

  function syncStats(): void {
    const s = store.studyStreak();
    streak.hidden = s < 1; // new players: no "0-day streak"
    streak.textContent = `${s}-day streak`;
    streak.title = 'Days in a row you have played';
    atp.textContent = `${store.totalAtp().toLocaleString()} ATP`;
    atp.title = 'Lifetime ATP earned';
  }

  function setCrumb(text: string, onBack?: () => void): void {
    crumb.textContent = plain(text);
    backHandler = onBack ?? null;
    if (onBack || lesson) { if (!back.isConnected) hud.insertBefore(back, crumb); }
    else back.remove();
    syncStats();
  }

  function setMascot(text: string, _face = '⚡'): void {
    // One steady mascot glyph; the face argument is accepted for compatibility.
    bubbleEl.textContent = plain(text);
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
    setMascot(quip(o.won ? 'win' : 'lose'));

    const card = el('div.arc-results.card');
    const badge = o.medal !== 'none'
      ? el(`div.arc-results-medal.is-${o.medal}`, { 'aria-hidden': 'true' }, '★')
      : (o.won ? el('div.arc-results-medal.is-cleared', { 'aria-hidden': 'true' }, '✓') : null);
    if (badge) card.append(badge);
    card.append(
      el('h2.arc-results-head', null, plain(o.headline)),
      el('p.arc-results-medaltext', null, o.medal !== 'none' ? `${MEDAL_LABEL[o.medal].toUpperCase()} MEDAL` : (o.won ? 'Cleared' : 'Give it another run')),
    );
    const stats = el('dl.arc-results-stats');
    for (const [k, v] of o.lines) {
      // "❤️❤️🖤" style life meters become a plain count.
      const hearts = /^(❤️?)+$/u.test(v) ? (v.match(/❤/gu) ?? []).length : -1;
      stats.append(el('dt', null, plain(k)), el('dd', null, hearts >= 0 ? `${hearts} of 3` : (plain(v) || 'none')));
    }
    stats.append(el('dt', null, 'ATP banked'), el('dd', null, o.score.toLocaleString()));
    card.append(stats);
    if (o.funFact) card.append(el('p.arc-results-fact', null, el('strong', null, 'Did you know — '), o.funFact));

    // Optional "keep learning" links to the matching lesson(s).
    let links: LessonLink[] = o.lessons ?? [];
    if (!links.length && o.lessonHref) links = [{ title: '', href: o.lessonHref }];
    if (!links.length) { const l = lessonFor(o.recordId); if (l) links = [l]; }
    if (links.length && !lesson) {
      const row = el('p.arc-results-lessons', null, links.length > 1 ? 'Review the lessons: ' : '');
      links.forEach((l, i) => {
        if (i) row.append(' · ');
        row.append(el('a.arc-lesson-link', { href: l.href }, links.length === 1
          ? (l.title ? `Read the ${l.title} lesson →` : 'Read the lesson →')
          : `${l.title || 'Lesson'} →`));
      });
      card.append(row);
    }

    const actions = el('div.arc-results-actions');
    const again = el('button.arc-btn', { type: 'button' }, 'Play again');
    again.addEventListener('click', () => { sfx.select(); o.replay(); });
    if (lesson) {
      // Opened from a lesson: send the student onward, or back to it.
      const next = lesson.nextSlug
        ? el('a.arc-btn.is-primary', { href: `/lessons/${lesson.nextSlug}/` }, `Next: ${plain(lesson.nextTitle ?? 'next lesson').split(':')[0].trim()} →`)
        : el('a.arc-btn.is-primary', { href: '/#lessons' }, 'All lessons');
      actions.append(next, el('a.arc-btn', { href: lessonHref }, 'Back to the lesson'), again);
    } else {
      again.classList.add('is-primary');
      const homeBtn = el('button.arc-btn', { type: 'button' }, 'All games');
      homeBtn.addEventListener('click', () => { sfx.select(); goHome(); });
      actions.append(again, homeBtn);
    }
    card.append(actions);

    const overlay = el('div.arc-overlay');
    overlay.append(card);
    setStage(overlay);
    if (o.medal === 'gold') confettiBurst(card);
  }

  function pathwayPicker(opts: { title: string; sub: string; pathways: Pathway[]; mode: ModeId; onPick: (p: Pathway) => void; onBack: () => void }): void {
    setCrumb(plain(opts.title), opts.onBack);
    setMascot('Pick a pathway to play.');
    const wrap = el('div.arc-home');
    wrap.append(el('p.arc-eyebrow', null, plain(opts.title)), el('p.arc-lede', null, opts.sub));
    const grid = el('div.arc-cabinets');
    for (const p of opts.pathways) {
      const best = store.getBest(p.id, opts.mode);
      const cab = el('button.arc-cabinet', { type: 'button' });
      cab.append(
        el('span.arc-cab-name', null, p.name),
        el('span.arc-cab-tag', null, p.tagline),
        el('span.arc-cab-meta', null,
          el('span.arc-stars', { 'aria-label': `Difficulty ${p.difficulty} of 3` }, '★'.repeat(p.difficulty) + '☆'.repeat(3 - p.difficulty)),
          best ? el(`span.arc-cab-medal.is-${best.medal}`, null, `${best.medal !== 'none' ? MEDAL_LABEL[best.medal] + ' · ' : ''}${best.score.toLocaleString()}`) : el('span.arc-cab-cleared', null, 'new')),
        el('span.arc-cab-play', { 'aria-hidden': 'true' }, 'Play →'),
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
