/* =============================================================================
   LEDGER RUSH — dexterity / resource-tally reflex game.
   -----------------------------------------------------------------------------
   Tokens stream off each reaction; BANK the real yields (+ATP, +NADH, and the
   −ATP investment tolls), TOSS the misconception decoys (a phantom "ATP" at
   GAPDH). Keep the running ledger true. After the aldolase split the yields come
   as ONE ×2 card (it adds 2). The fun is being FAST while knowing which token is
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
  h: { sym: '▲', label: 'H⁺' }, // protons pumped across the inner membrane (ETC only)
} as const;
type Kind = keyof typeof KINDS;
const TOKEN_KINDS = Object.keys(KINDS) as Kind[];
const zeroLedger = (): Record<Kind, number> => ({ atp: 0, nadh: 0, fadh2: 0, nadph: 0, gtp: 0, co2: 0, h: 0 });

interface Chip {
  real: boolean;
  kind: Kind;
  sign: 1 | -1;
  /** Units named on the card (e.g. "4 H⁺"). */
  qty: number;
  /** Multiplier badge (×2 after the glycolysis split, ×2 for two electron pairs). */
  amt: number;
  stepN: number;
  enzyme: string;
  /** Position of this card within its step (1-based) and the step's card count. */
  pos: number;
  of: number;
  why: string; // the teaching line (for a decoy: why it's fake; for a real: the fact)
}

/** Net ledger effect of banking this chip. */
const worth = (c: Chip): number => c.sign * c.qty * c.amt;

interface LStep {
  n: number;
  enzyme: string;
  fact: string;
  real: Array<{ kind: Kind; sign: 1 | -1; qty: number; amt: number }>;
  decoy?: { kind: Kind; sign: 1 | -1; qty: number; amt: number; why: string };
}

/**
 * Electron-transport chain: worked through complex by complex. The tally follows ONE
 * NADH and ONE FADH₂ (two electron pairs). Complexes III and IV see BOTH pairs (×2);
 * Complex I sees only NADH's, Complex II only FADH₂'s. 4 H⁺ per ATP -> 16 H⁺ -> 4 ATP
 * (2.5 + 1.5), and the gradient ledger returns to zero.
 */
const ETC_STEPS: LStep[] = [
  {
    n: 1, enzyme: 'Complex I (NADH dehydrogenase)',
    fact: 'NADH hands 2 e⁻ to FMN and an Fe–S relay, then to CoQ. The drop is steep enough to pump 4 H⁺. Blocked by rotenone.',
    real: [{ kind: 'nadh', sign: -1, qty: 1, amt: 1 }, { kind: 'h', sign: 1, qty: 4, amt: 1 }],
    decoy: { kind: 'fadh2', sign: -1, qty: 1, amt: 1, why: 'FADH₂ does not enter at Complex I. It feeds in lower down, at Complex II, which is why it banks fewer protons than NADH.' },
  },
  {
    n: 2, enzyme: 'Complex II (succinate dehydrogenase)',
    fact: 'Succinate to fumarate reduces FAD to FADH₂, which passes its electrons to CoQ. The energy drop is small, so Complex II pumps NO protons. It is also a TCA-cycle enzyme.',
    real: [{ kind: 'fadh2', sign: -1, qty: 1, amt: 1 }],
    decoy: { kind: 'h', sign: 1, qty: 2, amt: 1, why: 'Complex II pumps no protons: FADH₂ electrons enter CoQ with too little free-energy drop to power a pump. That is the reason FADH₂ is worth about 1.5 ATP and NADH about 2.5.' },
  },
  {
    n: 3, enzyme: 'Complex III (cytochrome bc₁)',
    fact: 'The Q cycle pumps 4 H⁺ per electron pair. Both the NADH electrons and the FADH₂ electrons pass here, so the tally is 4 H⁺ twice.',
    real: [{ kind: 'h', sign: 1, qty: 4, amt: 2 }],
    decoy: { kind: 'h', sign: 1, qty: 2, amt: 2, why: 'Complex III pumps 4 H⁺ per electron pair (the Q cycle), not 2.' },
  },
  {
    n: 4, enzyme: 'Complex IV (cytochrome c oxidase)',
    fact: 'Reduces O₂ to water and pumps 2 H⁺ per electron pair (2 more H⁺ are consumed chemically making water). Both electron pairs pass here, so 2 H⁺ twice. Blocked by cyanide.',
    real: [{ kind: 'h', sign: 1, qty: 2, amt: 2 }],
    decoy: { kind: 'atp', sign: 1, qty: 1, amt: 1, why: 'Only ATP synthase makes ATP. Complex IV only pumps protons and reduces O₂ to water.' },
  },
  {
    n: 5, enzyme: 'ATP synthase (Complex V)',
    fact: 'About 4 H⁺ flow back through per ATP (roughly 3 through the c-ring plus 1 for Pi/ADP transport). 16 H⁺ spent gives 4 ATP: 2.5 from the NADH plus 1.5 from the FADH₂.',
    real: [{ kind: 'h', sign: -1, qty: 4, amt: 4 }, { kind: 'atp', sign: 1, qty: 1, amt: 4 }],
    decoy: { kind: 'h', sign: 1, qty: 4, amt: 4, why: 'At ATP synthase protons flow back DOWN the gradient, so they are spent (a minus), not pumped (a plus).' },
  },
];

function entries(t: Tokens): Array<[Kind, number]> {
  return (TOKEN_KINDS.filter((k) => k !== 'h') as Kind[]).map((k) => [k, (t as Record<string, number | undefined>)[k] ?? 0] as [Kind, number]).filter(([, v]) => v !== 0);
}

function toLSteps(p: Pathway): LStep[] {
  if (p.id === 'oxidative-phosphorylation') return ETC_STEPS;
  const out: LStep[] = [];
  for (const s of p.steps) {
    if (!s.tokens) continue;
    const mult = p.doubleAfter > 0 && s.n > p.doubleAfter ? 2 : 1;
    const real: LStep['real'] = [];
    for (const [kind, val] of entries(s.tokens)) {
      for (let i = 0; i < Math.abs(val); i++) real.push({ kind, sign: val > 0 ? 1 : -1, qty: 1, amt: mult });
    }
    let decoy: LStep['decoy'];
    // a decoy: authored misconception if present, else a generated wrong-kind token
    if (s.misconception) {
      const gk = (TOKEN_KINDS.find((k) => KINDS[k].label.toLowerCase() === s.misconception!.grab.toLowerCase()) ?? 'atp');
      decoy = { kind: gk, sign: 1, qty: 1, amt: 1, why: s.misconception.why };
    } else if (real.length) {
      const realKinds = real.map((r) => r.kind);
      const wrong = TOKEN_KINDS.find((k) => !realKinds.includes(k) && (k === 'atp' || k === 'nadh' || k === 'fadh2'));
      if (wrong) {
        const made = [...new Set(realKinds)].map((k) => KINDS[k].label).join(' & ');
        decoy = { kind: wrong, sign: 1, qty: 1, amt: 1, why: `${s.enzyme} makes ${made}, not ${KINDS[wrong].label}.` };
      }
    }
    out.push({ n: s.n, enzyme: s.enzyme, fact: s.fact, real, decoy });
  }
  return out;
}

/** Build the stream of tokens: real (a doubled token is ONE ×2 card) + misconception decoys. */
function buildQueue(p: Pathway): Chip[] {
  const q: Chip[] = [];
  for (const s of toLSteps(p)) {
    const bunch: Chip[] = s.real.map((r) => ({
      real: true, kind: r.kind, sign: r.sign, qty: r.qty, amt: r.amt, stepN: s.n, enzyme: s.enzyme, pos: 0, of: 0,
      why: `${s.enzyme}: ${s.fact}`,
    }));
    if (s.decoy && bunch.length) {
      bunch.push({ real: false, kind: s.decoy.kind, sign: s.decoy.sign, qty: s.decoy.qty, amt: s.decoy.amt, stepN: s.n, enzyme: s.enzyme, pos: 0, of: 0, why: s.decoy.why });
    }
    const sh = shuffle(bunch);
    sh.forEach((c, i) => { c.pos = i + 1; c.of = sh.length; });
    q.push(...sh);
  }
  return q;
}

export function launchLedgerRush(shell: Shell, pathways: Pathway[]): void {
  // Ledger Rush needs steps with cofactor tokens; all 13 qualify but filter defensively.
  const eligible = pathways.filter((p) => p.id === 'oxidative-phosphorylation' || p.steps.some((s) => s.tokens));
  shell.pathwayPicker({
    title: 'Ledger Rush',
    sub: 'Bank the real ATP/NADH, toss the myths, and catch the ×2 cards after the split. How clean can you keep the ledger?',
    pathways: eligible, mode: 'ledger',
    onBack: () => shell.goHome(),
    onPick: (p) => play(shell, pathways, p),
  });
}

function play(shell: Shell, pathways: Pathway[], p: Pathway): void {
  const queue = buildQueue(p);
  const truth = zeroLedger();
  for (const c of queue) if (c.real) truth[c.kind] += worth(c);
  const shownKinds = new Set<Kind>(queue.filter((c) => c.real).map((c) => c.kind));
  const isEtc = p.id === 'oxidative-phosphorylation';

  // Fresh state for every run; nothing here is shared with an earlier session.
  let idx = 0, combo = 0, maxCombo = 0, errors = 0, score = 0, locked = false, disposed = false;
  let pending: (() => void) | null = null; // set while a wrong-answer explanation awaits "Next"
  const ledger = zeroLedger();
  const start = Date.now();
  const timers = new Set<number>();

  shell.setCrumb(`Ledger Rush · ${p.name}`, () => { dispose(); launchLedgerRush(shell, pathways); });
  shell.setMascot('Bank the real yields. Toss the myths.', '⚡');

  const wrap = el('div.arc-lr');
  // top row: progress + combo
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
    if (!shownKinds.has(k) && k !== 'atp' && k !== 'nadh') continue; // show ATP/NADH always, others if used
    const val = el('span.arc-ledger-val', null, '0');
    ledgerCells[k] = val;
    ledgerRow.append(el('span.arc-ledger-item', null, `${KINDS[k].sym} ${KINDS[k].label} `, val));
  }
  wrap.append(ledgerRow);

  if (isEtc) wrap.append(el('p.arc-lr-note', null, 'Tally one NADH and one FADH₂ (two electron pairs). A ×2 card counts twice.'));

  // fork banner
  const fork = el('div.arc-lr-fork', null, 'SPLIT: doubled yields arrive as one ×2 card that counts twice.');
  fork.style.display = 'none';
  wrap.append(fork);

  // the chip stage
  const reaction = el('p.arc-lr-reaction');
  const chipZone = el('div.arc-lr-chipzone');
  wrap.append(reaction, chipZone);

  // action buttons
  const tossBtn = el('button.arc-lr-btn.is-toss', { type: 'button' }, el('span.arc-lr-btn-ico', { 'aria-hidden': 'true' }, '✗'), el('span', null, 'TOSS'), el('kbd', null, '1'));
  const bankBtn = el('button.arc-lr-btn.is-bank', { type: 'button' }, el('span.arc-lr-btn-ico', { 'aria-hidden': 'true' }, '✓'), el('span', null, 'BANK'), el('kbd', null, '2'));
  wrap.append(el('div.arc-lr-actions', null, tossBtn, bankBtn));
  wrap.append(el('p.arc-lr-hint', { html: 'Is this token a <strong>real</strong> yield of the reaction? <strong>BANK</strong> it. A myth? <strong>TOSS</strong> it. (keys 1 = Toss, 2 = Bank, or ← / →)' }));

  // feedback
  const fb = el('div.arc-lr-fb', { role: 'status', 'aria-live': 'polite' });
  const fbText = el('p.arc-lr-fb-text');
  const nextBtn = el('button.arc-btn.is-primary.arc-lr-next', { type: 'button' }, 'Next ▸') as HTMLButtonElement;
  fb.append(fbText, nextBtn);
  wrap.append(fb);

  function later(fn: () => void, ms: number): void {
    const id = window.setTimeout(() => { timers.delete(id); if (!alive()) return; fn(); }, ms);
    timers.add(id);
  }

  /** Remove every listener and timer this run owns. Safe to call repeatedly. */
  function dispose(): void {
    disposed = true;
    document.removeEventListener('keydown', keyHandler);
    for (const id of timers) window.clearTimeout(id);
    timers.clear();
    pending = null;
  }

  /** False once the run is over or the player has left (stage swapped out). */
  function alive(): boolean {
    if (disposed) return false;
    if (!wrap.isConnected) { dispose(); return false; }
    return true;
  }

  function fmt(n: number): string { return n > 0 ? `+${n}` : String(n); }

  function syncLedger(): void {
    for (const k of TOKEN_KINDS) {
      const cell = ledgerCells[k];
      if (cell) cell.textContent = fmt(ledger[k]);
    }
  }

  function renderChip(): void {
    const c = queue[idx];
    progFill.style.width = `${(idx / queue.length) * 100}%`;
    comboEl.textContent = combo >= 2 ? `${combo}× combo` : '';
    fork.style.display = p.doubleAfter > 0 && c.stepN > p.doubleAfter ? 'block' : 'none';
    reaction.textContent = `Step ${c.stepN} · ${c.enzyme} · card ${c.pos} of ${c.of}`;
    chipZone.innerHTML = '';
    const lbl = c.qty > 1 ? `${c.qty} ${KINDS[c.kind].label}` : KINDS[c.kind].label;
    const chip = el(`div.arc-lr-chip.is-${c.sign > 0 ? 'plus' : 'minus'}${c.amt > 1 ? '.is-double' : ''}`);
    chip.append(
      el('span.arc-lr-chip-sign', { 'aria-hidden': 'true' }, c.sign > 0 ? '+' : '−'),
      el('span.arc-lr-chip-sym', { 'aria-hidden': 'true' }, KINDS[c.kind].sym),
      el('span.arc-lr-chip-lbl', null, lbl),
    );
    if (c.amt > 1) chip.append(el('span.arc-lr-chip-mult', { 'aria-hidden': 'true' }, `×${c.amt}`));
    chip.setAttribute('aria-label', `${c.sign > 0 ? 'plus' : 'minus'} ${c.amt > 1 ? `${c.amt} times ` : ''}${lbl} at ${c.enzyme}, card ${c.pos} of ${c.of}`);
    chipZone.append(chip);
    fb.className = 'arc-lr-fb';
    fbText.textContent = '';
    locked = false;
  }

  function advance(): void {
    if (!alive()) return;
    pending = null;
    idx++;
    if (idx >= queue.length) { finish(); return; }
    const old = chipZone.querySelector('.arc-lr-chip');
    if (old && !prefersReducedMotion()) {
      old.classList.add('is-out');
      locked = true;
      later(renderChip, 170);
    } else renderChip();
  }

  function decide(bank: boolean): void {
    if (!alive() || locked || idx >= queue.length) return;
    const c = queue[idx];
    const correct = bank === c.real; // bank a real, or toss a decoy
    locked = true;
    if (correct) {
      combo++; maxCombo = Math.max(maxCombo, combo);
      score += 100 * Math.min(combo, 6);
      if (bank) ledger[c.kind] += worth(c);
      syncLedger();
      sfx.correct();
      if (combo >= 4 && combo % 4 === 0) { sfx.streak(); shell.setMascot('Ledger locked in. Keep going.', '🔥'); }
      later(advance, 120);
    } else {
      errors++; combo = 0;
      sfx.wrong();
      const chip = chipZone.querySelector('.arc-lr-chip');
      if (chip && !prefersReducedMotion()) { chip.classList.remove('arc-shake'); void (chip as HTMLElement).offsetWidth; chip.classList.add('arc-shake'); }
      const what = `${c.sign > 0 ? '+' : '−'}${c.amt > 1 ? `${c.amt}× ` : ''}${c.qty > 1 ? `${c.qty} ` : ''}${KINDS[c.kind].label}`;
      fb.className = 'arc-lr-fb is-shown';
      fbText.textContent = (c.real ? `That was REAL: you dropped a ${what}. ` : 'Myth! ') + c.why;
      nextBtn.textContent = idx + 1 >= queue.length ? 'See results ▸' : 'Next ▸';
      pending = advance;
      shell.setMascot('Check the cofactors.', '😵');
      nextBtn.focus({ preventScroll: true });
    }
  }

  bankBtn.addEventListener('click', () => decide(true));
  tossBtn.addEventListener('click', () => decide(false));
  nextBtn.addEventListener('click', () => { if (pending) pending(); });

  function keyHandler(e: KeyboardEvent): void {
    if (!alive()) return; // stale handler from a run the player already left
    if (e.ctrlKey || e.metaKey || e.altKey) return;
    const t = e.target as HTMLElement | null;
    if (t && (t.tagName === 'INPUT' || t.tagName === 'TEXTAREA' || t.tagName === 'SELECT')) return;
    const toss = e.key === '1' || e.key === 'ArrowLeft';
    const bank = e.key === '2' || e.key === 'ArrowRight';
    if (pending) {
      if (toss || bank || e.key === 'Enter' || e.key === ' ') { e.preventDefault(); pending(); }
      return;
    }
    if (bank) { e.preventDefault(); decide(true); }
    else if (toss) { e.preventDefault(); decide(false); }
  }
  document.addEventListener('keydown', keyHandler);

  function finish(): void {
    dispose();
    progFill.style.width = '100%';
    const secs = Math.round((Date.now() - start) / 1000);
    const speedBonus = Math.max(0, 400 - secs * 6);
    score = Math.max(0, score + speedBonus - errors * 40);
    const ledgerTrue = TOKEN_KINDS.every((k) => ledger[k] === truth[k]);
    const medal: Medal = errors === 0 ? 'gold' : errors <= 2 ? 'silver' : 'bronze';
    const truthStr = TOKEN_KINDS.filter((k) => truth[k] !== 0).map((k) => `${fmt(truth[k])} ${KINDS[k].label}`).join(' · ');
    shell.showResults({
      recordId: p.id, mode: 'ledger', won: true, medal, score,
      headline: errors === 0 ? 'Flawless ledger!' : ledgerTrue ? 'Ledger balanced!' : 'Rush complete',
      lines: [
        ['Mistakes', String(errors)],
        ['Best combo', `${maxCombo}×`],
        ['Time', `${secs}s`],
        ['True net yield', truthStr || (isEtc ? 'gradient balanced (0 H⁺)' : '—')],
        ['Your ledger', ledgerTrue ? '✓ matched' : '✗ off, replay it'],
      ],
      funFact: p.funFact,
      replay: () => play(shell, pathways, p),
    });
  }

  shell.setStage(wrap);
  renderChip();
}
