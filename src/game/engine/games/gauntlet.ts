/* =============================================================================
   MCAT GAUNTLET — the cram tool (kept from the original arcade).
   -----------------------------------------------------------------------------
   Timed rapid-fire across every pathway. Not a "game" in the new set's sense —
   it's the deliberate spaced-timed-retrieval drill for test week. Boss health,
   hearts, combos, keyboard play. Reuses each pathway's quiz[].
   ============================================================================ */
import type { Pathway, QuizItem } from '../../types';
import { el, shuffle, prefersReducedMotion } from '../dom';
import { sfx } from '../sound';
import type { Shell } from '../shell';
import type { Medal } from '../storage';

function shuffledChoices(choices: string[], answer: number): { choices: string[]; answer: number } {
  const order = shuffle(choices.map((_, i) => i));
  return { choices: order.map((i) => choices[i]), answer: order.indexOf(answer) };
}

function buildBank(pathways: Pathway[]): QuizItem[] {
  const pool: QuizItem[] = [];
  for (const p of pathways) for (const q of shuffle(p.quiz).slice(0, 2)) pool.push({ ...q, stem: `[${p.name}] ${q.stem}` });
  return shuffle(pool).slice(0, 15);
}

export function launchGauntlet(shell: Shell, pathways: Pathway[]): void {
  const bank = buildBank(pathways);
  const total = bank.length;
  let idx = 0, hearts = 3, combo = 0, maxCombo = 0, score = 0, correct = 0;
  const PER_Q = 22;
  let timer: number | null = null;
  const stop = () => { if (timer != null) { clearInterval(timer); timer = null; } };

  shell.setCrumb('🎓 MCAT Gauntlet', () => { stop(); shell.goHome(); });

  function renderQ(): void {
    const q = bank[idx];
    const view = shuffledChoices(q.choices, q.answer);
    shell.setMascot(combo >= 3 ? `🔥 ${combo}× combo — the MCAT is sweating!` : 'Boss battle! Answer fast, keep the combo.', '🎓');
    let timeLeft = PER_Q;
    const wrap = el('div.arc-blitz');
    const bossfill = el('div.arc-bosshp-fill');
    bossfill.style.width = `${(1 - correct / total) * 100}%`;
    wrap.append(el('div.arc-blitz-top', null,
      el('div.arc-boss', null, el('span.arc-boss-face', { 'aria-hidden': 'true' }, '🎓'),
        el('div.arc-boss-meta', null, el('span.arc-boss-name', null, 'The MCAT'), el('div.arc-bosshp', null, bossfill))),
      el('div.arc-blitz-status', null,
        el('span.arc-hearts', { 'aria-label': `${hearts} lives` }, '❤️'.repeat(hearts) + '🖤'.repeat(3 - hearts)),
        el('span.arc-combo', null, combo >= 2 ? `⚡ ${combo}×` : ''))));
    const timeFill = el('div.arc-timerfill');
    wrap.append(el('div.arc-timerbar', null, timeFill));
    wrap.append(el('p.arc-blitz-count', null, `Q${idx + 1} of ${total}`, q.tag ? el('span.arc-qtag', null, q.tag) : el('span')));
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
        score += 100 * Math.min(combo, 5) + Math.round(timeLeft * 5);
        sfx.correct();
        if (combo >= 3) { sfx.streak(); shell.setMascot('🔥 On fire!', '🔥'); } else shell.setMascot('Nice.', '⚡');
        bossfill.style.width = `${(1 - correct / total) * 100}%`;
      } else { combo = 0; hearts--; sfx.wrong(); shell.setMascot(ci == null ? 'Time! The boss got a hit in.' : 'Not quite.', '😵'); }
      why.className = `arc-teachbox is-shown card ${right ? 'is-ok' : 'is-bad'}`;
      const done = hearts <= 0 || idx + 1 >= total;
      const next = el('button.arc-btn.is-primary', { type: 'button' }, hearts <= 0 ? 'See results →' : idx + 1 >= total ? 'Finish →' : 'Next →');
      next.addEventListener('click', () => { sfx.select(); if (done) finish(); else { idx++; renderQ(); } });
      why.append(el('p.arc-why-head', null, right ? '✓ Correct' : ci == null ? '⏱️ Out of time' : '✗ Not quite'), el('p.arc-teach-text', null, q.rationale), next);
      why.scrollIntoView?.({ behavior: prefersReducedMotion() ? 'auto' : 'smooth', block: 'nearest' });
    }

    document.removeEventListener('keydown', keyHandler);
    document.addEventListener('keydown', keyHandler);
    function keyHandler(e: KeyboardEvent): void {
      const t = e.target as HTMLElement | null;
      if (t && (t.tagName === 'INPUT' || t.tagName === 'TEXTAREA')) return;
      if (/^[1-9]$/.test(e.key)) {
        const list = Array.from(opts.querySelectorAll<HTMLButtonElement>('.arc-opt'));
        if (list.length && list.every((o) => !o.disabled)) { const tgt = list[+e.key - 1]; if (tgt) { e.preventDefault(); tgt.click(); } }
      } else if (e.key === 'Enter' && answered) {
        const n = why.querySelector<HTMLButtonElement>('.arc-btn.is-primary'); if (n && (t?.tagName !== 'BUTTON')) { e.preventDefault(); n.click(); }
      }
    }

    shell.setStage(wrap);
    const startT = Date.now();
    timeFill.style.width = '100%';
    timer = window.setInterval(() => {
      timeLeft = Math.max(0, PER_Q - (Date.now() - startT) / 1000);
      timeFill.style.width = `${(timeLeft / PER_Q) * 100}%`;
      timeFill.style.background = timeLeft < 6 ? '#c0392b' : timeLeft < 12 ? 'var(--ddp-color-secondary)' : 'var(--ddp-color-accent)';
      if (timeLeft <= 0) answer(null, null);
    }, 100);
  }

  function finish(): void {
    stop();
    document.removeEventListener('keydown', () => {});
    const won = correct >= total;
    const medal: Medal = won && hearts === 3 ? 'gold' : won ? 'silver' : correct >= Math.ceil(total * 0.6) ? 'bronze' : 'none';
    if (won && hearts > 0) score += 200;
    shell.showResults({
      recordId: 'gauntlet', mode: 'gauntlet', won,
      medal, score,
      headline: won && hearts === 3 ? 'FLAWLESS VICTORY!' : won ? 'The MCAT, defeated!' : hearts <= 0 ? 'The MCAT won… this time' : 'Time up',
      lines: [['Correct', `${correct}/${total}`], ['Best combo', `${maxCombo}×`], ['Lives left', '❤️'.repeat(Math.max(0, hearts)) || 'none']],
      replay: () => launchGauntlet(shell, pathways),
    });
  }

  renderQ();
}
