/* =============================================================================
   MIXING BOARD — discrete-tick reciprocal regulation.
   -----------------------------------------------------------------------------
   You are the liver/muscle's regulators. Each tick shows a body STATE; set every
   hormone/effector/enzyme to the right level, route flux the correct way, and —
   the marquee lesson — NEVER run glycolysis and gluconeogenesis at once (futile
   cycle). A near-equilibrium enzyme is INERT (can't be throttled — the ΔG point).
   Polarity only, deliberately no invented kinetics (per the design critic).
   Effector table authored inline for the glycolysis ⇄ gluconeogenesis pair.
   ============================================================================ */
import { el } from '../dom';
import { sfx } from '../sound';
import type { Shell } from '../shell';
import type { Medal } from '../storage';

type StateId = 'fed' | 'fasted' | 'sprint' | 'diabetes';

interface MState {
  id: StateId; emoji: string; tissue: string; title: string; scene: string;
  requiredFlux: 'glycolysis' | 'gluconeogenesis'; teach: string;
}
const STATES: MState[] = [
  { id: 'fed', emoji: '🥞', tissue: 'LIVER', title: 'Fed — you just ate', requiredFlux: 'glycolysis',
    scene: 'Blood glucose is spiking, the pancreas is pouring out insulin. The liver should USE and store the incoming glucose.',
    teach: 'FED: insulin → PFK-2 active → F-2,6-BP HIGH → PFK-1 ON and FBPase-1 OFF, so incoming glucose is directed into glycolysis (and storage) rather than made. Note ATP/citrate may well be high after a meal, but it is not what decides things here: F-2,6-BP overrides ATP/citrate inhibition of PFK-1, so the energy-charge control is not scored in this state.' },
  { id: 'fasted', emoji: '⏳', tissue: 'LIVER', title: 'Fasted — 14 hours since dinner', requiredFlux: 'gluconeogenesis',
    scene: 'Blood glucose is drifting down; glucagon is rising. The brain still needs glucose — the liver must MAKE and export it.',
    teach: 'FASTED: glucagon → PKA → F-2,6-BP LOW → PFK-1 OFF, FBPase-1 ON → gluconeogenesis. ATP and citrate are HIGH here, not low: adipose fat floods the liver, β-oxidation makes ATP, NADH and acetyl-CoA, and gluconeogenesis is an ATP CONSUMER (about 6 ATP-equivalents per glucose). High ATP/citrate also inhibits PFK-1, and acetyl-CoA activates pyruvate carboxylase, so everything points the same way.' },
  { id: 'sprint', emoji: '🏃', tissue: 'MUSCLE', title: 'Sprint — muscle, no oxygen', requiredFlux: 'glycolysis',
    scene: 'Contracting muscle needs ATP NOW. AMP is climbing as ATP is spent. (Muscle lacks glucose-6-phosphatase, so it can’t export glucose — gluconeogenesis to blood glucose is a liver job.)',
    teach: 'SPRINT: ATP is being spent faster than it is made, so ATP is LOW and AMP rises. AMP activates PFK-1 and relieves ATP inhibition, so glucose is pushed through glycolysis for fast anaerobic ATP. Muscle PFK-2 is not under glucagon control and F-2,6-BP plays a minor role here, so that control and glucagon are not scored. Muscle makes no glucose for export, so FBPase-1 stays off.' },
  { id: 'diabetes', emoji: '🍭', tissue: 'LIVER', title: 'Uncontrolled Type 1 diabetes', requiredFlux: 'gluconeogenesis',
    scene: 'Blood glucose is sky-high — but there’s almost no insulin, and glucagon is unopposed. Does the liver read the glucose, or the hormones?',
    teach: 'DIABETES trap: regulation follows the HORMONE, not the substrate. No insulin and unopposed glucagon → F-2,6-BP LOW → the liver runs gluconeogenesis and dumps MORE glucose into already-flooded blood. Uncontrolled lipolysis sends fat to the liver, and hard β-oxidation keeps ATP and citrate HIGH, just like fasting, which further inhibits PFK-1 and fuels gluconeogenesis. Hormone beats substrate.' },
];

interface Control {
  id: string; name: string; sub: string; options: [string, string]; rule: string;
  /** Per-state answer: 0/1 = the scored option index; -1 = not decisive in that state (unscored, either answer is fine). */
  correct: Record<StateId, 0 | 1 | -1>;
  /** Shown after commit for states where `correct` is -1. */
  neutral?: Partial<Record<StateId, string>>;
  enzyme?: 'pfk1' | 'fbpase1';
  inert?: boolean;
}
const CONTROLS: Control[] = [
  { id: 'insulin', name: 'Insulin', sub: 'fed-state hormone', options: ['LOW', 'HIGH'], rule: 'HIGH only when fed (fuel abundant); LOW when fasting, sprinting, or diabetic (no insulin).',
    correct: { fed: 1, fasted: 0, sprint: 0, diabetes: 0 } },
  { id: 'glucagon', name: 'Glucagon', sub: 'fasting hormone', options: ['LOW', 'HIGH'], rule: 'HIGH when fasting/diabetic (make glucose); LOW when fed. Reciprocal to insulin. Muscle has no glucagon receptor, so it is not scored in the sprint.',
    correct: { fed: 0, fasted: 1, sprint: -1, diabetes: 1 },
    neutral: { sprint: 'Skeletal muscle has no glucagon receptor, so glucagon is not a regulator here.' } },
  { id: 'f26bp', name: 'Fructose-2,6-BP', sub: 'the master allosteric switch', options: ['LOW', 'HIGH'], rule: 'Set by PFK-2/FBPase-2 under hormones, mainly in liver. Insulin → HIGH → PFK-1 on, FBPase-1 off. Glucagon → LOW → gluconeogenesis. Not decisive in sprinting muscle, where AMP and falling ATP drive PFK-1 directly.',
    correct: { fed: 1, fasted: 0, sprint: -1, diabetes: 0 },
    neutral: { sprint: 'The muscle PFK-2 isoform is not glucagon-responsive; in exercise AMP and falling ATP are the main PFK-1 drivers, so F-2,6-BP is not the deciding signal.' } },
  { id: 'amp', name: 'AMP', sub: 'low-energy signal', options: ['LOW', 'HIGH'], rule: 'Rises only when ATP is being spent fast: HIGH in a sprinting muscle, LOW when fed, fasting or diabetic (liver ATP is high). Activates PFK-1; inhibits FBPase-1.',
    correct: { fed: 0, fasted: 0, sprint: 1, diabetes: 0 } },
  { id: 'atpcit', name: 'ATP / citrate', sub: 'fuel-plenty signal', options: ['LOW', 'HIGH'], rule: 'HIGH ATP/citrate inhibits PFK-1 (no need for more ATP) and, via acetyl-CoA from fat oxidation, activates pyruvate carboxylase. HIGH in the fasted or diabetic liver, where β-oxidation runs hard and gluconeogenesis spends ATP. LOW in sprinting muscle (ATP spent, AMP up). Not scored in the fed liver: insulin-driven F-2,6-BP overrides it.',
    correct: { fed: -1, fasted: 1, sprint: 0, diabetes: 1 },
    neutral: { fed: 'Either setting is fine. In the fed liver, insulin-driven F-2,6-BP overrides ATP/citrate inhibition of PFK-1, so energy charge is not what drives glycolysis here.' } },
  { id: 'pfk1', name: 'PFK-1', sub: 'glycolysis committed enzyme', options: ['OFF', 'ON'], rule: 'The committed step of glycolysis. ON when glucose should be directed into glycolysis (fed liver, sprinting muscle); OFF when the liver is making glucose (fasted / diabetic). In the fasted liver it is shut off by low F-2,6-BP and high ATP/citrate together.',
    correct: { fed: 1, fasted: 0, sprint: 1, diabetes: 0 }, enzyme: 'pfk1' },
  { id: 'fbpase1', name: 'FBPase-1', sub: 'gluconeogenesis enzyme', options: ['OFF', 'ON'], rule: 'The gluconeogenic counter to PFK-1. ON only when the liver makes glucose (fasted / diabetic). Reciprocal — never on together with PFK-1.',
    correct: { fed: 0, fasted: 1, sprint: 0, diabetes: 1 }, enzyme: 'fbpase1' },
  { id: 'pgi', name: 'Phosphoglucose isomerase', sub: 'near-equilibrium step', options: ['—', '—'], rule: 'A near-equilibrium reaction runs whichever way flux needs — you CAN’T throttle it. Regulation only works at the far-from-equilibrium (committed) steps.',
    correct: { fed: 0, fasted: 0, sprint: 0, diabetes: 0 }, inert: true },
];

export function launchMixingBoard(shell: Shell): void {
  let idx = 0, score = 0, correctCount = 0, totalControls = 0, futiles = 0;

  shell.setCrumb('🎛️ Mixing Board', () => shell.goHome());

  function renderState(): void {
    const st = STATES[idx];
    const picks: Record<string, 0 | 1 | null> = {};
    for (const c of CONTROLS) picks[c.id] = c.inert ? null : null;
    let committed = false;
    shell.setMascot(`Tick ${idx + 1} of ${STATES.length}. Read the body, set the board.`, st.emoji);

    const wrap = el('div.arc-mix');
    wrap.append(el('div.arc-dx-top', null,
      el('span.arc-reg-progress', null, `Tick ${idx + 1}/${STATES.length}`),
      el('span.arc-mix-tissue', null, st.tissue)));

    const scene = el('div.arc-scene.card');
    scene.append(el('div.arc-scene-emoji', { 'aria-hidden': 'true' }, st.emoji),
      el('div', null, el('h3.arc-scene-title', null, st.title), el('p.arc-scene-text', null, st.scene)));
    wrap.append(scene);

    // live flux meter
    const fluxEl = el('div.arc-mix-flux');
    const updateFlux = () => {
      const pfk = picks['pfk1'], fb = picks['fbpase1'];
      let txt = '', cls = '';
      if (pfk === 1 && fb === 1) { txt = 'FUTILE CYCLE: both on! You’re burning ATP for nothing.'; cls = 'is-futile'; }
      else if (pfk === 1) { txt = 'Flux: GLYCOLYSIS (glucose directed into the pathway)'; cls = 'is-glyc'; }
      else if (fb === 1) { txt = 'Flux: GLUCONEOGENESIS (making glucose)'; cls = 'is-gng'; }
      else { txt = 'Flux: stalled. Set an enzyme.'; cls = ''; }
      fluxEl.className = `arc-mix-flux ${cls}`;
      fluxEl.textContent = txt;
    };

    wrap.append(el('p.arc-mix-lbl', null, 'Set every control for this state, then commit. “Flux toward glycolysis” means glucose is being directed into glycolysis rather than stored or made. Some controls are not decisive in every state; set your best judgment.'));
    const grid = el('div.arc-mix-controls');
    for (const c of CONTROLS) {
      const row = el('div.arc-mix-control');
      row.append(el('div.arc-mix-control-head', null,
        el('span.arc-mix-control-name', null, c.name),
        el('span.arc-mix-control-sub', null, c.sub)));
      if (c.inert) {
        row.classList.add('is-inert');
        row.append(el('div.arc-mix-inert', null, 'Near-equilibrium: can’t be throttled'));
      } else {
        const seg = el('div.arc-mix-seg', { 'data-control': c.id });
        c.options.forEach((opt, oi) => {
          const b = el('button.arc-mix-opt', { type: 'button' }, opt);
          b.addEventListener('click', () => {
            if (committed) return;
            picks[c.id] = oi as 0 | 1;
            Array.from(seg.children).forEach((ch) => ch.classList.remove('is-sel'));
            b.classList.add('is-sel');
            sfx.select();
            if (c.enzyme) updateFlux();
          });
          seg.append(b);
        });
        row.append(seg);
      }
      grid.append(row);
    }
    wrap.append(grid, fluxEl);
    updateFlux();

    const commit = el('button.arc-btn.is-primary.arc-mix-commit', { type: 'button' }, 'Commit the board');
    wrap.append(commit);
    const reveal = el('div.arc-teachbox');
    wrap.append(reveal);

    commit.addEventListener('click', () => {
      if (committed) return;
      // require all non-inert set
      const unset = CONTROLS.filter((c) => !c.inert && picks[c.id] == null);
      if (unset.length) { shell.setMascot(`Set all controls first (${unset.length} left).`, '🎛️'); sfx.wrong(); return; }
      committed = true;
      let roundCorrect = 0, roundTotal = 0;
      const neutralNotes: string[] = [];
      for (const c of CONTROLS) {
        if (c.inert) continue;
        const key = c.correct[st.id];
        const seg = grid.querySelector(`[data-control="${c.id}"]`);
        if (key === -1) {
          // unscored: either setting is fine
          if (seg) {
            (Array.from(seg.children) as HTMLButtonElement[]).forEach((b) => { b.disabled = true; });
            seg.parentElement?.classList.add('is-neutral');
            seg.parentElement?.append(el('div.arc-mix-neutral', null, 'Not decisive here'));
          }
          if (c.neutral?.[st.id]) neutralNotes.push(`${c.name}: ${c.neutral[st.id]}`);
          continue;
        }
        roundTotal++;
        const ok = picks[c.id] === key;
        if (ok) roundCorrect++;
        if (seg) {
          const btns = Array.from(seg.children) as HTMLButtonElement[];
          btns.forEach((b, bi) => { b.disabled = true; if (bi === key) b.classList.add('is-correct'); else if (bi === picks[c.id]) b.classList.add('is-wrong'); });
        }
      }
      const futile = picks['pfk1'] === 1 && picks['fbpase1'] === 1;
      if (futile) futiles++;
      correctCount += roundCorrect; totalControls += roundTotal;
      const base = roundCorrect * 60;
      const fluxRight = (st.requiredFlux === 'glycolysis' && picks['pfk1'] === 1 && picks['fbpase1'] === 0) ||
        (st.requiredFlux === 'gluconeogenesis' && picks['fbpase1'] === 1 && picks['pfk1'] === 0);
      const roundScore = Math.max(0, base + (fluxRight ? 120 : 0) - (futile ? 200 : 0));
      score += roundScore;

      reveal.className = 'arc-teachbox is-shown card';
      reveal.append(
        el('p.arc-mix-verdict', null, futile ? 'FUTILE CYCLE! PFK-1 and FBPase-1 were both ON — the cell burns ATP making and breaking the same bond for nothing.' :
          fluxRight ? `Correct routing: ${st.requiredFlux} for this state.` : `Wrong net direction: this state needs ${st.requiredFlux}.`),
        el('p.arc-mix-score', null, `${roundCorrect}/${roundTotal} controls right · +${roundScore}`),
        el('p.arc-teach-text', null, st.teach),
        ...neutralNotes.map((n) => el('p.arc-teach-text.arc-mix-neutral-note', null, n)),
      );
      if (futile) { sfx.lose(); shell.setMascot('Futile cycle! Reciprocal regulation exists precisely to stop that.', '😵'); }
      else if (fluxRight && roundCorrect === roundTotal) { sfx.streak(); shell.setMascot('Perfect board. Textbook control.', '🎛️'); }
      else { sfx.correct(); shell.setMascot('Committed — see what the board should read.', '🎛️'); }

      const next = el('button.arc-btn.is-primary', { type: 'button' }, idx + 1 < STATES.length ? 'Next tick →' : 'See results →');
      next.addEventListener('click', () => { sfx.select(); idx++; if (idx < STATES.length) renderState(); else finish(); });
      reveal.append(next);
      reveal.scrollIntoView?.({ block: 'nearest' });
    });

    shell.setStage(wrap);
  }

  function finish(): void {
    const frac = totalControls ? correctCount / totalControls : 0;
    const medal: Medal = frac >= 0.95 && futiles === 0 ? 'gold' : frac >= 0.8 && futiles === 0 ? 'silver' : frac >= 0.6 ? 'bronze' : 'none';
    shell.showResults({
      recordId: 'mixing', mode: 'mixing', won: frac >= 0.6, medal, score,
      headline: frac >= 0.95 && futiles === 0 ? 'Master of metabolic control!' : futiles > 0 ? 'Watch those futile cycles' : 'Board committed',
      lines: [['Controls correct', `${correctCount}/${totalControls}`], ['Futile cycles run', String(futiles)], ['States', String(STATES.length)]],
      funFact: 'Reciprocal regulation is why fructose-2,6-bisphosphate exists: one molecule flips PFK-1 on and FBPase-1 off at the same time, so a liver cell can never waste ATP running glycolysis and gluconeogenesis at once.',
      replay: () => launchMixingBoard(shell),
    });
  }

  renderState();
}
