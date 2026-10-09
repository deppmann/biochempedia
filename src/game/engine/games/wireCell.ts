/* =============================================================================
   WIRE THE CELL — a Zachlike metabolic construction puzzle.
   A demand ("burn glucose for ≥30 ATP, O₂ available"). Place the pathway MODULES
   that form a complete chain from the fuel to the goal; a module only FIRES if
   its inputs are produced upstream. Hit RUN: a deterministic token-balance solve
   tallies ATP vs the target (OxPhos cashes carriers at 2.5/NADH, 1.5/FADH₂, only
   with O₂). Each failed RUN costs points; the balance sheet says what broke.
   Puzzle data + solver live in ./wireCellLogic (pure, unit-testable).
   ============================================================================ */
import { NETMAP } from '../../data/netmap';
import { el } from '../dom';
import { sfx } from '../sound';
import type { Shell } from '../shell';
import type { Medal } from '../storage';
import { DEMANDS, SHORT_NAME, diagnose, puzzleMedal, puzzleScore, solve } from './wireCellLogic';
import type { WireMod } from './wireCellLogic';

const nodeInfo = (id: string) => NETMAP.nodes.find((n) => n.id === id);

interface Tally { score: number; solved: number; firstTry: number; fails: number; medals: Medal[]; }

/** Optionally start at a given puzzle id; the run continues through the later ones. */
export function launchWireCell(shell: Shell, startPuzzle?: string): void {
  const i = startPuzzle ? DEMANDS.findIndex((d) => d.id === startPuzzle) : -1;
  const start = i < 0 ? 0 : i;
  play(shell, start, start, { score: 0, solved: 0, firstTry: 0, fails: 0, medals: [] });
}

function play(shell: Shell, startIdx: number, demandIdx: number, tally: Tally): void {
  const d = DEMANDS[demandIdx];
  const placed = new Set<string>();
  let fails = 0;
  type Phase = 'edit' | 'failed' | 'won';
  let phase: Phase = 'edit';
  let result: ReturnType<typeof solve> | null = null;

  shell.setCrumb('Wire the Cell', () => shell.goHome());
  shell.setMascot(`Puzzle ${demandIdx + 1} of ${DEMANDS.length}. Build the line, then hit RUN.`, '🔌');

  const wrap = el('div.arc-wire');
  const failsEl = el('span.arc-wire-fails');
  wrap.append(el('div.arc-dx-top', null,
    el('span.arc-reg-progress', null, `Puzzle ${demandIdx + 1}/${DEMANDS.length}`),
    el('span.arc-wire-par', null, `par: ${d.par} modules`),
    failsEl));

  const fuelNames = d.fuels.map((f) => f.name).join(' + ');
  const scene = el('div.arc-scene.card');
  scene.append(el('div', null, el('h3.arc-scene-title', null, d.title),
    el('p.arc-scene-text', null, d.scene),
    el('p.arc-wire-goal', null,
      el('span.arc-chip', null, `Fuel: ${fuelNames}`),
      el('span.arc-chip', null, d.o2 ? 'O₂ available' : (d.o2Note ?? 'No O₂')),
      el('span.arc-chip.is-goal', null, `Goal: ${d.goal.label}`))));
  wrap.append(scene);

  wrap.append(el('p.arc-wire-lbl', null, 'Tap modules to add or remove them. A module only fires if its inputs arrive from upstream. Modules always appear in pathway order.'));
  const palette = el('div.arc-wire-palette');
  const countEl = el('span');
  const btns = new Map<string, { btn: HTMLElement; state: HTMLElement }>();
  for (const m of d.mods) {
    const info = nodeInfo(m.nodeId);
    const state = el('span.arc-wire-mod-state', null, '');
    const btn = el('button.arc-wire-mod', { type: 'button', 'data-mod': m.nodeId, 'aria-pressed': 'false' },
      el('span.arc-wire-mod-ico', { 'aria-hidden': 'true' }, info?.emoji ?? ''),
      el('span.arc-wire-mod-name', null, SHORT_NAME[m.nodeId] ?? info?.name ?? m.nodeId),
      el('span.arc-wire-mod-yield', null, yieldHint(m)),
      state);
    btn.addEventListener('click', () => {
      if (phase === 'won') return;
      if (placed.has(m.nodeId)) placed.delete(m.nodeId); else placed.add(m.nodeId);
      sfx.select();
      // any edit invalidates the last run: drop stale results, return to edit phase
      phase = 'edit'; result = null;
      render();
    });
    btns.set(m.nodeId, { btn, state });
    palette.append(btn);
  }
  wrap.append(palette);

  const runBtn = el('button.arc-btn.is-primary.arc-wire-run', { type: 'button' }, 'RUN the cell');
  const retryBtn = el('button.arc-btn.arc-wire-retry', { type: 'button' }, 'Retry: edit the wiring');
  wrap.append(el('div.arc-wire-controls', null, countEl, runBtn, retryBtn));
  const balance = el('div.arc-wire-balance');
  wrap.append(balance);

  runBtn.addEventListener('click', () => run());
  retryBtn.addEventListener('click', () => { phase = 'edit'; result = null; sfx.select(); render(); });

  /** Single source of truth: every visual state is derived from placed/phase/result. */
  function render(): void {
    countEl.textContent = `${placed.size} placed`;
    failsEl.textContent = fails ? `${fails} failed run${fails > 1 ? 's' : ''}` : '';
    for (const m of d.mods) {
      const b = btns.get(m.nodeId);
      if (!b) continue;
      const isPlaced = placed.has(m.nodeId);
      b.btn.className = 'arc-wire-mod';
      b.btn.setAttribute('aria-pressed', String(isPlaced));
      (b.btn as HTMLButtonElement).disabled = phase === 'won';
      b.state.textContent = '';
      if (isPlaced) b.btn.classList.add('is-placed');
      if (isPlaced && result) {
        const ok = result.fired.has(m.nodeId) || (m.cashier && result.oxphosCashed);
        if (ok) { b.btn.classList.remove('is-placed'); b.btn.classList.add('is-fired'); b.state.textContent = 'firing'; }
        else { b.btn.classList.remove('is-placed'); b.btn.classList.add('is-stranded'); b.state.textContent = m.cashier ? (d.o2 ? 'no carriers' : (d.o2Note ?? 'no O₂').toLowerCase()) : 'stranded'; }
      }
    }
    runBtn.hidden = phase !== 'edit';
    (runBtn as HTMLButtonElement).disabled = placed.size === 0;
    retryBtn.hidden = phase !== 'failed';
    if (phase === 'edit') { balance.className = 'arc-wire-balance'; balance.innerHTML = ''; }
  }

  function run(): void {
    const res = solve(d, placed);
    result = res;
    const won = res.won;
    phase = won ? 'won' : 'failed';
    if (!won) fails += 1;
    render();

    balance.className = 'arc-wire-balance is-shown card';
    balance.innerHTML = '';
    const g = d.goal;
    const rows: Array<[string, string]> = [];
    if (g.atp !== undefined) {
      rows.push(['Substrate-level ATP', fmt(res.slpAtp)]);
      rows.push(['Cashed at OxPhos', res.oxphosCashed ? `+${res.cashed.toFixed(1)} (${res.nadh} NADH, ${res.fadh2} FADH₂)` : (res.nadh + res.fadh2 ? `0, carriers wasted (${res.nadh} NADH, ${res.fadh2} FADH₂)` : '0')]);
      rows.push(['Total ATP', `${res.atp % 1 ? res.atp.toFixed(1) : res.atp} / ${g.atp} target`]);
    }
    if (g.nadph !== undefined) rows.push(['Net NADPH', `${res.nadphNet} / ${g.nadph} target`]);
    if (g.make) rows.push([g.make.label, res.made ? 'produced' : 'not produced']);
    if (g.atp === undefined) rows.push(['Net ATP cost', fmt(res.atp)]);
    rows.push(['Modules used', `${placed.size} (par ${d.par})`]);
    const sheet = el('dl.arc-wire-sheet');
    for (const [k, v] of rows) sheet.append(el('dt', null, k), el('dd', null, v));
    balance.append(el('p.arc-wire-verdict', null, won ? 'It flows!' : 'Not there yet'), sheet);

    if (won) {
      sfx.correct(); shell.setMascot('It flows! Beautiful wiring.', '🔌');
      const perfect = placed.size <= d.par && res.noWaste;
      const pts = puzzleScore(perfect, fails);
      const medal = puzzleMedal(pts);
      balance.append(el('p.arc-wire-teach', null, d.teachWin));
      const note = `${medal[0].toUpperCase()}${medal.slice(1)} medal, +${pts}. ` +
        (perfect ? 'Par or better, no waste.' : `Try it in ${d.par} modules with nothing stranded for more.`) +
        (fails ? ` (${fails} failed run${fails > 1 ? 's' : ''} cost ${(perfect ? 500 : 300) - pts > 0 ? (perfect ? 500 : 300) - pts : 0} points.)` : ' First try!');
      const last = demandIdx + 1 >= DEMANDS.length;
      const next = el('button.arc-btn.is-primary', { type: 'button' }, last ? 'See results' : 'Next puzzle');
      next.addEventListener('click', () => {
        sfx.select();
        const t: Tally = {
          score: tally.score + pts, solved: tally.solved + 1, firstTry: tally.firstTry + (fails === 0 ? 1 : 0),
          fails: tally.fails + fails, medals: [...tally.medals, medal],
        };
        if (last) finish(shell, startIdx, t); else play(shell, startIdx, demandIdx + 1, t);
      });
      balance.append(el('p.arc-wire-medal', null, note), next);
    } else {
      sfx.wrong(); shell.setMascot('The line’s broken, so read what went wrong.', '😵');
      const why = diagnose(d, placed, res);
      const list = el('ul.arc-wire-fail');
      for (const w of why) list.append(el('li', null, w));
      balance.append(
        el('p.arc-wire-lbl2', null, 'What went wrong'), list,
        el('p.arc-wire-teach', null, d.teachLose),
        el('p.arc-wire-medal', null, `Failed run ${fails}: each one lowers this puzzle’s medal (−100 points). Fix the wiring and run again.`));
    }
  }

  render();
  shell.setStage(wrap);
}

function finish(shell: Shell, startIdx: number, t: Tally): void {
  const n = DEMANDS.length - startIdx; // puzzles in this run
  const medal: Medal = t.score >= n * 450 ? 'gold' : t.score >= n * 300 ? 'silver' : 'bronze';
  shell.showResults({
    recordId: 'wire', mode: 'wire', won: true, medal, score: t.score,
    headline: medal === 'gold' ? 'Master cell-wirer!' : 'Cell wired',
    lines: [
      ['Puzzles', `${t.solved} solved`],
      ['Solved first try', `${t.firstTry} / ${n}`],
      ['Failed runs', String(t.fails)],
      ['Puzzle medals', t.medals.map((m) => m[0].toUpperCase()).join(' ')],
    ],
    funFact: 'Every one of those ATP totals, 32 from glucose and 106 from palmitate, is the real number the MCAT asks you to reconstruct. You just built the machine that makes it.',
    replay: () => launchWireCell(shell, DEMANDS[startIdx].id),
  });
}

function yieldHint(m: WireMod): string {
  if (m.cashier) return 'cashes NADH/FADH₂ → ATP (needs O₂)';
  const parts: string[] = [];
  if (m.atp) parts.push(`${m.atp > 0 ? '+' : ''}${m.atp} ATP`);
  if (m.nadh) parts.push(`${m.nadh} NADH`);
  if (m.fadh2) parts.push(`${m.fadh2} FADH₂`);
  if (m.nadph) parts.push(`${m.nadph > 0 ? '+' : ''}${m.nadph} NADPH`);
  if (m.requiresO2) parts.push('needs O₂');
  return parts.join(' · ') || 'routing';
}
function fmt(n: number): string { return n > 0 ? `+${n}` : String(n); }
