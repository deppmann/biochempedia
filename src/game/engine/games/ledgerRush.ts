/* =============================================================================
   LEDGER RUSH — dexterity / resource-tally reflex game.
   -----------------------------------------------------------------------------
   Tokens stream off each reaction; BANK the real yields (+ATP, +NADH, and the
   −ATP investment tolls), TOSS the misconception decoys (a phantom "ATP" at
   GAPDH). Keep the running ledger true. After the aldolase split the yields come
   in PAIRS — bank double. The fun is being FAST while knowing which token is
   real; the biochemistry IS the difficulty. Reuses steps[].tokens + doubleAfter.
   ============================================================================ */
import type { Pathway, Tokens } from '../../types';
import { el, shuffle, prefersReducedMotion } from '../dom';
import { sfx } from '../sound';
import type { Shell } from '../shell';
import type { Medal } from '../storage';

const KINDS = {
  atp: { sym: '⚡', label: 'ATP' },
  nadh: { sym: '🔋', label: 'NADH' },
  fadh2: { sym: '🔩', label: 'FADH₂' },
  nadph: { sym: '🟣', label: 'NADPH' },
  gtp: { sym: '🟡', label: 'GTP' },
  co2: { sym: '💨', label: 'CO₂' },
} as const;
type Kind = keyof typeof KINDS;
const TOKEN_KINDS = Object.keys(KINDS) as Kind[];

interface Chip {
  real: boolean;
  kind: Kind;
  sign: 1 | -1;
  stepN: number;
  enzyme: string;
  doubled: boolean;
  why: string; // the teaching line (for a decoy: why it's fake; for a real: the fact)
}

function entries(t: Tokens): Array<[Kind, number]> {
  return TOKEN_KINDS.map((k) => [k, t[k] ?? 0] as [Kind, number]).filter(([, v]) => v !== 0);
}

/** Build the stream of tokens: real (doubled past the split) + misconception decoys. */
function buildQueue(p: Pathway): Chip[] {
  const q: Chip[] = [];
  for (const s of p.steps) {
    const mult = p.doubleAfter > 0 && s.n > p.doubleAfter ? 2 : 1;
    const bunch: Chip[] = [];
    const realKinds: Kind[] = [];
    if (s.tokens) {
      for (const [kind, val] of entries(s.tokens)) {
        realKinds.push(kind);
        const copies = Math.abs(val) * mult;
        for (let i = 0; i < copies; i++) {
          bunch.push({
            real: true, kind, sign: val > 0 ? 1 : -1, stepN: s.n, enzyme: s.enzyme, doubled: mult === 2,
            why: `${s.enzyme}: ${s.fact}`,
          });
        }
      }
      // a decoy: authored misconception if present, else a generated wrong-kind token
      if (s.misconception) {
        const gk = (TOKEN_KINDS.find((k) => KINDS[k].label.toLowerCase() === s.misconception!.grab.toLowerCase()) ?? 'atp');
        bunch.push({ real: false, kind: gk, sign: 1, stepN: s.n, enzyme: s.enzyme, doubled: false, why: s.misconception.why });
      } else if (realKinds.length) {
        const wrong = TOKEN_KINDS.find((k) => !realKinds.includes(k) && (k === 'atp' || k === 'nadh' || k === 'fadh2'));
        if (wrong) {
          const made = realKinds.map((k) => KINDS[k].label).join(' & ');
          bunch.push({ real: false, kind: wrong, sign: 1, stepN: s.n, enzyme: s.enzyme, doubled: false, why: `${s.enzyme} makes ${made}, not ${KINDS[wrong].label}.` });
        }
      }
    }
    q.push(...shuffle(bunch));
  }
  return q;
}

export function launchLedgerRush(shell: Shell, pathways: Pathway[]): void {
  // Ledger Rush needs steps with cofactor tokens; all 13 qualify but filter defensively.
  const eligible = pathways.filter((p) => p.steps.some((s) => s.tokens));
  shell.pathwayPicker({
    title: '⚡ Ledger Rush',
    sub: 'Bank the real ATP/NADH, toss the myths, catch DOUBLE after the split. How clean can you keep the ledger?',
    pathways: eligible, mode: 'ledger',
    onBack: () => shell.goHome(),
    onPick: (p) => play(shell, pathways, p),
  });
}

function play(shell: Shell, pathways: Pathway[], p: Pathway): void {
  const queue = buildQueue(p);
  const truth = { atp: 0, nadh: 0, fadh2: 0, nadph: 0, gtp: 0, co2: 0 } as Record<Kind, number>;
  for (const c of queue) if (c.real) truth[c.kind] += c.sign;

  let idx = 0, combo = 0, maxCombo = 0, errors = 0, score = 0, locked = false;
  const ledger = { atp: 0, nadh: 0, fadh2: 0, nadph: 0, gtp: 0, co2: 0 } as Record<Kind, number>;
  const start = Date.now();

  shell.setCrumb(`⚡ Ledger Rush · ${p.name}`, () => launchLedgerRush(shell, pathways));
  shell.setMascot('Bank the real yields. Toss the myths. Go fast!', '⚡');

  const wrap = el('div.arc-lr');
  // top row: progress + combo + timer
  const progFill = el('div.arc-lr-progfill');
  const comboEl = el('span.arc-lr-combo');
  wrap.append(el('div.arc-lr-top', null,
    el('div.arc-lr-prog', null, progFill),
    comboEl));

  // ledger
  const ledgerCells: Partial<Record<Kind, HTMLElement>> = {};
  const ledgerRow = el('div.arc-ledger');
  ledgerRow.append(el('span.arc-ledger-lbl', null, 'Your ledger'));
  for (const k of TOKEN_KINDS) {
    if (truth[k] === 0 && k !== 'atp' && k !== 'nadh') continue; // show ATP/NADH always, others if used
    const val = el('span.arc-ledger-val', null, '0');
    ledgerCells[k] = val;
    ledgerRow.append(el('span.arc-ledger-item', null, `${KINDS[k].sym} ${KINDS[k].label} `, val));
  }
  wrap.append(ledgerRow);

  // fork banner
  const fork = el('div.arc-lr-fork', null, '✂️ SPLIT! Yields now come in PAIRS — bank double.');
  fork.style.display = 'none';
  wrap.append(fork);

  // the chip stage
  const reaction = el('p.arc-lr-reaction');
  const chipZone = el('div.arc-lr-chipzone');
  wrap.append(reaction, chipZone);

  // action buttons
  const tossBtn = el('button.arc-lr-btn.is-toss', { type: 'button' }, el('span.arc-lr-btn-ico', null, '✗'), el('span', null, 'TOSS'), el('kbd', null, 'F'));
  const bankBtn = el('button.arc-lr-btn.is-bank', { type: 'button' }, el('span.arc-lr-btn-ico', null, '✓'), el('span', null, 'BANK'), el('kbd', null, 'J'));
  wrap.append(el('div.arc-lr-actions', null, tossBtn, bankBtn));
  wrap.append(el('p.arc-lr-hint', { html: 'Is this token a <strong>real</strong> yield of the reaction? <strong>BANK</strong> it. A myth? <strong>TOSS</strong> it. (keys F / J)' }));

  // feedback
  const fb = el('div.arc-lr-fb', { role: 'status', 'aria-live': 'polite' });
  wrap.append(fb);

  function syncLedger(): void {
    for (const k of TOKEN_KINDS) {
      const cell = ledgerCells[k];
      if (cell) cell.textContent = ledger[k] > 0 ? `+${ledger[k]}` : String(ledger[k]);
    }
  }

  function renderChip(): void {
    const c = queue[idx];
    progFill.style.width = `${(idx / queue.length) * 100}%`;
    comboEl.textContent = combo >= 2 ? `🔥 ${combo}× combo` : '';
    fork.style.display = p.doubleAfter > 0 && c.stepN > p.doubleAfter ? 'block' : 'none';
    reaction.textContent = `Step ${c.stepN} · ${c.enzyme}`;
    chipZone.innerHTML = '';
    const chip = el(`div.arc-lr-chip.is-${c.sign > 0 ? 'plus' : 'minus'}${c.doubled ? '.is-double' : ''}`);
    chip.append(
      el('span.arc-lr-chip-sign', { 'aria-hidden': 'true' }, c.sign > 0 ? '+' : '−'),
      el('span.arc-lr-chip-sym', { 'aria-hidden': 'true' }, KINDS[c.kind].sym),
      el('span.arc-lr-chip-lbl', null, KINDS[c.kind].label),
    );
    chip.setAttribute('aria-label', `${c.sign > 0 ? 'plus' : 'minus'} ${KINDS[c.kind].label} at ${c.enzyme}`);
    chipZone.append(chip);
  }

  function decide(bank: boolean): void {
    if (locked || idx >= queue.length) return;
    const c = queue[idx];
    const correct = bank === c.real; // bank a real, or toss a decoy
    locked = true;
    if (correct) {
      combo++; maxCombo = Math.max(maxCombo, combo);
      score += 100 * Math.min(combo, 6);
      if (bank) ledger[c.kind] += c.sign;
      syncLedger();
      sfx.correct();
      if (combo >= 4 && combo % 4 === 0) { sfx.streak(); shell.setMascot('🔥 Ledger locked in! Keep ripping.', '🔥'); }
      fb.className = 'arc-lr-fb';
      fb.textContent = '';
    } else {
      errors++; combo = 0;
      sfx.wrong();
      const chip = chipZone.querySelector('.arc-lr-chip');
      if (chip && !prefersReducedMotion()) { chip.classList.remove('arc-shake'); void (chip as HTMLElement).offsetWidth; chip.classList.add('arc-shake'); }
      fb.className = 'arc-lr-fb is-shown';
      const verdict = c.real
        ? `✗ That was REAL — you dropped a ${c.sign > 0 ? '+' : '−'}${KINDS[c.kind].label}. `
        : `✗ Myth! `;
      fb.textContent = verdict + c.why;
      shell.setMascot('Oof — check the cofactors.', '😵');
    }
    window.setTimeout(() => {
      locked = false;
      idx++;
      if (idx >= queue.length) finish();
      else renderChip();
    }, correct ? 130 : 900);
  }

  bankBtn.addEventListener('click', () => decide(true));
  tossBtn.addEventListener('click', () => decide(false));
  const keyHandler = (e: KeyboardEvent) => {
    const t = e.target as HTMLElement | null;
    if (t && (t.tagName === 'INPUT' || t.tagName === 'TEXTAREA')) return;
    if (e.key === 'j' || e.key === 'J' || e.key === 'ArrowRight' || e.key === ' ') { e.preventDefault(); decide(true); }
    else if (e.key === 'f' || e.key === 'F' || e.key === 'ArrowLeft') { e.preventDefault(); decide(false); }
  };
  document.addEventListener('keydown', keyHandler);

  function finish(): void {
    document.removeEventListener('keydown', keyHandler);
    progFill.style.width = '100%';
    const secs = Math.round((Date.now() - start) / 1000);
    const speedBonus = Math.max(0, 400 - secs * 6);
    score = Math.max(0, score + speedBonus - errors * 40);
    const ledgerTrue = TOKEN_KINDS.every((k) => ledger[k] === truth[k]);
    const medal: Medal = errors === 0 ? 'gold' : errors <= 2 ? 'silver' : 'bronze';
    const truthStr = TOKEN_KINDS.filter((k) => truth[k] !== 0).map((k) => `${truth[k] > 0 ? '+' : ''}${truth[k]} ${KINDS[k].label}`).join(' · ');
    shell.showResults({
      recordId: p.id, mode: 'ledger', won: true, medal, score,
      headline: errors === 0 ? 'Flawless ledger!' : ledgerTrue ? 'Ledger balanced!' : 'Rush complete',
      lines: [
        ['Mistakes', String(errors)],
        ['Best combo', `${maxCombo}×`],
        ['Time', `${secs}s`],
        ['True net yield', truthStr || '—'],
        ['Your ledger', ledgerTrue ? '✓ matched' : '✗ off — replay it'],
      ],
      funFact: p.funFact,
      replay: () => play(shell, pathways, p),
    });
  }

  shell.setStage(wrap);
  renderChip();
}
