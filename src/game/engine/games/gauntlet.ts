/* =============================================================================
   MCAT GAUNTLET — the cram tool (kept from the original arcade).
   -----------------------------------------------------------------------------
   Timed rapid-fire across every pathway. Not a "game" in the new set's sense —
   it's the deliberate spaced-timed-retrieval drill for test week. Boss health,
   lives, combos, keyboard play. Reuses each pathway's quiz[].

   Two things make it fair to the MCAT student:
   - SCOPE: items flagged `mcat: false` in the pathway data (detailed mechanisms,
     plant Calvin-cycle specifics, deep regulatory isoforms, exact stoichiometries
     …) are great for the course but beyond the exam. A start-screen toggle picks
     "MCAT scope" (default) or "Full course".
   - TIME: each question gets its own clock — easy items are short, hard items
     are long — derived from the item's tag and how much there is to read.
   ============================================================================ */
import type { Pathway, QuizItem, QuizTag } from '../../types';
import { el, shuffle, prefersReducedMotion } from '../dom';
import { sfx } from '../sound';
import type { Shell, LessonLink } from '../shell';
import { lessonFor } from '../shell';
import type { Medal } from '../storage';
import { getPref, setPref } from '../storage';

type Scope = 'mcat' | 'full';
type Level = 1 | 2 | 3;
const LEVEL_NAME: Record<Level, string> = { 1: 'Easy', 2: 'Medium', 3: 'Hard' };
const ROUND = 15;

interface GItem extends QuizItem {
  pid: string;
  level: Level;
  secs: number;
}

function shuffledChoices(choices: string[], answer: number): { choices: string[]; answer: number } {
  const order = shuffle(choices.map((_, i) => i));
  return { choices: order.map((i) => choices[i]), answer: order.indexOf(answer) };
}

const words = (s: string) => s.trim().split(/\s+/).filter(Boolean).length;
const TAG_WEIGHT: Record<QuizTag, number> = { basics: 0, energetics: 1, disease: 1, regulation: 1.5, integration: 2 };

/** Difficulty from the item's tag + how much there is to read (or a manual override). */
export function levelOf(q: QuizItem): Level {
  if (q.difficulty) return q.difficulty;
  const w = words(q.stem) + q.choices.reduce((n, c) => n + words(c), 0);
  const d = (q.tag ? TAG_WEIGHT[q.tag] : 1) + (w < 45 ? 0 : w < 75 ? 0.5 : 1);
  return d < 1.25 ? 1 : d < 2.25 ? 2 : 3;
}

/** Seconds on the clock: reading time (~4.5 words/s) + thinking time by difficulty. */
export function secondsFor(q: QuizItem, level: Level = levelOf(q)): number {
  const w = words(q.stem) + q.choices.reduce((n, c) => n + words(c), 0);
  const think: Record<Level, number> = { 1: 9, 2: 15, 3: 22 };
  return Math.min(60, Math.max(15, Math.round(w / 4.5 + think[level])));
}

function eligible(pathways: Pathway[], scope: Scope): Array<{ p: Pathway; items: QuizItem[] }> {
  return pathways
    .map((p) => ({ p, items: p.quiz.filter((q) => scope === 'full' || q.mcat !== false) }))
    .filter((x) => x.items.length > 0);
}

function bankSize(pathways: Pathway[], scope: Scope): number {
  return eligible(pathways, scope).reduce((n, x) => n + x.items.length, 0);
}

/** 15 questions, dealt round-robin across pathways so one topic can't dominate. */
function buildBank(pathways: Pathway[], scope: Scope): GItem[] {
  const piles = shuffle(eligible(pathways, scope)).map((x) => ({ p: x.p, items: shuffle(x.items) }));
  const pool: GItem[] = [];
  while (pool.length < ROUND && piles.some((x) => x.items.length)) {
    for (const x of piles) {
      const q = x.items.pop();
      if (!q) continue;
      const level = levelOf(q);
      pool.push({ ...q, stem: `[${x.p.name}] ${q.stem}`, pid: x.p.id, level, secs: secondsFor(q, level) });
      if (pool.length >= ROUND) break;
    }
  }
  return shuffle(pool);
}

const fmtClock = (s: number) => `${Math.floor(s / 60)}:${String(Math.ceil(s) % 60).padStart(2, '0')}`.replace(/^(\d+):60$/, (_, m) => `${+m + 1}:00`);
const livesText = (n: number) => `Lives ${'● '.repeat(Math.max(0, n))}${'○ '.repeat(Math.max(0, 3 - n))}`.trim();

export function launchGauntlet(shell: Shell, pathways: Pathway[]): void {
  let keyHandler: ((e: KeyboardEvent) => void) | null = null;
  let timer: number | null = null;
  const stop = () => { if (timer != null) { clearInterval(timer); timer = null; } };
  const cleanup = () => { stop(); if (keyHandler) { document.removeEventListener('keydown', keyHandler); keyHandler = null; } };

  /* ---- start screen: scope toggle ------------------------------------- */
  function start(): void {
    cleanup();
    shell.setCrumb('MCAT Gauntlet', () => { cleanup(); shell.goHome(); });
    shell.setMascot('Pick your scope, then beat the clock.');
    let scope: Scope = getPref<Scope>('gauntlet-scope', 'mcat') === 'full' ? 'full' : 'mcat';

    const wrap = el('div.arc-home.arc-gauntlet-start');
    wrap.append(
      el('p.arc-eyebrow', null, 'Cram tool'),
      el('h1.arc-title', null, 'MCAT Gauntlet'),
      el('p.arc-lede', null, `${ROUND} timed questions, three lives, one boss. Easy questions get a short clock and hard ones a long one, so the pressure matches the difficulty.`),
    );

    const group = el('div.arc-scope', { role: 'radiogroup', 'aria-label': 'Question scope' });
    const note = el('p.arc-scope-note', { role: 'status' });
    const defs: Array<{ id: Scope; name: string; desc: string }> = [
      { id: 'mcat', name: 'MCAT scope', desc: 'Only what the exam is likely to ask.' },
      { id: 'full', name: 'Full course', desc: 'Adds the deeper BIOL 3030 material: enzyme mechanisms, plant carbon fixation, exact stoichiometries.' },
    ];
    const inputs: HTMLInputElement[] = [];
    const sync = () => {
      const n = bankSize(pathways, scope);
      note.textContent = scope === 'mcat'
        ? `${n} questions in the bank. Beyond-MCAT items are hidden.`
        : `${n} questions in the bank, including ${n - bankSize(pathways, 'mcat')} beyond-MCAT items.`;
      inputs.forEach((i) => { i.closest('label')?.classList.toggle('is-on', i.value === scope); });
    };
    for (const d of defs) {
      const input = el('input', { type: 'radio', name: 'gauntlet-scope', value: d.id }) as HTMLInputElement;
      input.checked = d.id === scope;
      input.addEventListener('change', () => { scope = d.id; setPref('gauntlet-scope', scope); sfx.select(); sync(); });
      inputs.push(input);
      group.append(el('label.arc-scope-opt', null, input,
        el('span.arc-scope-text', null, el('span.arc-scope-name', null, d.name), el('span.arc-scope-desc', null, d.desc))));
    }
    wrap.append(group, note);

    const go = el('button.arc-btn.is-primary', { type: 'button' }, 'Start the Gauntlet');
    go.addEventListener('click', () => { sfx.select(); play(scope); });
    wrap.append(go);
    sync();
    shell.setStage(wrap);
  }

  /* ---- the run ---------------------------------------------------------- */
  function play(scope: Scope): void {
    const bank = buildBank(pathways, scope);
    const total = bank.length;
    let idx = 0, hearts = 3, combo = 0, maxCombo = 0, score = 0, correct = 0;
    const missed = new Set<string>();

    shell.setCrumb('MCAT Gauntlet', () => { cleanup(); start(); });

    function renderQ(): void {
      const q = bank[idx];
      const view = shuffledChoices(q.choices, q.answer);
      shell.setMascot(combo >= 3 ? `${combo}x combo — the MCAT is sweating.` : 'Boss battle! Answer fast, keep the combo.');
      let timeLeft = q.secs;
      const wrap = el('div.arc-blitz');
      const bossfill = el('div.arc-bosshp-fill');
      bossfill.style.width = `${(1 - correct / total) * 100}%`;
      wrap.append(el('div.arc-blitz-top', null,
        el('div.arc-boss', null,
          el('div.arc-boss-meta', null, el('span.arc-boss-name', null, 'The MCAT'), el('div.arc-bosshp', { 'aria-hidden': 'true' }, bossfill))),
        el('div.arc-blitz-status', null,
          el('span.arc-hearts', { 'aria-label': `${hearts} lives left` }, livesText(hearts)),
          el('span.arc-combo', null, combo >= 2 ? `${combo}x combo` : ''))));

      // Per-question clock: big number + bar, labelled with the difficulty that set it.
      const clockNum = el('span.arc-clock-num', { role: 'timer' }, fmtClock(q.secs));
      const timeFill = el('div.arc-timerfill');
      wrap.append(el('div.arc-clock', null,
        el('span.arc-clock-level.is-' + q.level, null, `${LEVEL_NAME[q.level]} · ${q.secs}s`),
        clockNum));
      wrap.append(el('div.arc-timerbar', { 'aria-hidden': 'true' }, timeFill));
      wrap.append(el('p.arc-blitz-count', null, `Question ${idx + 1} of ${total}`, q.tag ? el('span.arc-qtag', null, q.tag) : el('span')));
      wrap.append(el('p.arc-blitz-stem', null, q.stem));
      const opts = el('div.arc-options.arc-blitz-opts');
      const why = el('div.arc-teachbox');
      let answered = false;
      view.choices.forEach((c, ci) => {
        const b = el('button.arc-opt.arc-opt-keyed', { type: 'button' },
          el('span.arc-optnum', { 'aria-hidden': 'true' }, String(ci + 1)), el('span.arc-opttext', null, c));
        b.addEventListener('click', () => answer(ci, b));
        opts.append(b);
      });
      wrap.append(opts, why);

      function answer(ci: number | null, btn: HTMLElement | null): void {
        if (answered) return;
        answered = true; stop();
        const right = ci === view.answer;
        Array.from(opts.children).forEach((child, k) => {
          const b = child as HTMLButtonElement;
          b.disabled = true;
          if (k === view.answer) b.classList.add('is-correct');
          else if (btn && b === btn) b.classList.add('is-wrong');
        });
        if (right) {
          correct++; combo++; maxCombo = Math.max(maxCombo, combo);
          score += 100 * Math.min(combo, 5) + Math.round((timeLeft / q.secs) * 100) + 20 * q.level;
          sfx.correct();
          if (combo >= 3) { sfx.streak(); shell.setMascot('On fire!'); } else shell.setMascot('Nice.');
          bossfill.style.width = `${(1 - correct / total) * 100}%`;
        } else {
          combo = 0; hearts--; sfx.wrong(); missed.add(q.pid);
          shell.setMascot(ci == null ? 'Time! The boss got a hit in.' : 'Not quite.');
        }
        why.className = `arc-teachbox is-shown card ${right ? 'is-ok' : 'is-bad'}`;
        const done = hearts <= 0 || idx + 1 >= total;
        const next = el('button.arc-btn.is-primary', { type: 'button' }, hearts <= 0 ? 'See results →' : idx + 1 >= total ? 'Finish →' : 'Next →');
        next.addEventListener('click', () => { sfx.select(); if (done) finish(); else { idx++; renderQ(); } });
        why.append(el('p.arc-why-head', null, right ? '✓ Correct' : ci == null ? 'Out of time' : '✗ Not quite'), el('p.arc-teach-text', null, q.rationale), next);
        why.scrollIntoView?.({ behavior: prefersReducedMotion() ? 'auto' : 'smooth', block: 'nearest' });
      }

      if (keyHandler) document.removeEventListener('keydown', keyHandler);
      keyHandler = (e: KeyboardEvent): void => {
        const t = e.target as HTMLElement | null;
        if (t && (t.tagName === 'INPUT' || t.tagName === 'TEXTAREA')) return;
        if (/^[1-9]$/.test(e.key)) {
          const list = Array.from(opts.querySelectorAll<HTMLButtonElement>('.arc-opt'));
          if (list.length && list.every((o) => !o.disabled)) { const tgt = list[+e.key - 1]; if (tgt) { e.preventDefault(); tgt.click(); } }
        } else if (e.key === 'Enter' && answered) {
          const n = why.querySelector<HTMLButtonElement>('.arc-btn.is-primary'); if (n && (t?.tagName !== 'BUTTON')) { e.preventDefault(); n.click(); }
        }
      };
      document.addEventListener('keydown', keyHandler);

      shell.setStage(wrap);
      const startT = Date.now();
      timeFill.style.width = '100%';
      timer = window.setInterval(() => {
        timeLeft = Math.max(0, q.secs - (Date.now() - startT) / 1000);
        const frac = timeLeft / q.secs;
        timeFill.style.width = `${frac * 100}%`;
        clockNum.textContent = fmtClock(timeLeft);
        const state = timeLeft <= 5 || frac < 0.25 ? 'is-low' : frac < 0.5 ? 'is-mid' : '';
        timeFill.className = `arc-timerfill ${state}`;
        clockNum.className = `arc-clock-num ${state}`;
        if (timeLeft <= 0) answer(null, null);
      }, 100);
    }

    function finish(): void {
      cleanup();
      const won = correct >= total;
      const medal: Medal = won && hearts === 3 ? 'gold' : won ? 'silver' : correct >= Math.ceil(total * 0.6) ? 'bronze' : 'none';
      if (won && hearts > 0) score += 200;
      // Offer lessons for what you missed; if you missed nothing, for what you played.
      const pids = missed.size ? [...missed] : [...new Set(bank.map((b) => b.pid))];
      const seen = new Set<string>();
      const lessons: LessonLink[] = [];
      for (const pid of pids) {
        const l = lessonFor(pid);
        if (l && !seen.has(l.href)) { seen.add(l.href); lessons.push(l); }
        if (lessons.length >= 3) break;
      }
      shell.showResults({
        recordId: 'gauntlet', mode: 'gauntlet', won,
        medal, score,
        headline: won && hearts === 3 ? 'Flawless victory' : won ? 'The MCAT, defeated' : hearts <= 0 ? 'The MCAT won… this time' : 'Time up',
        lines: [['Scope', scope === 'mcat' ? 'MCAT' : 'Full course'], ['Correct', `${correct}/${total}`], ['Best combo', `${maxCombo}x`], ['Lives left', `${Math.max(0, hearts)} of 3`]],
        lessons,
        replay: () => start(),
      });
    }

    renderQ();
  }

  start();
}
