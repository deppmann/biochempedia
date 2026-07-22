/* =============================================================================
   WIRE THE CELL — a Zachlike metabolic construction puzzle.
   -----------------------------------------------------------------------------
   A demand ("burn glucose for ≥30 ATP, O₂ available"). Place the pathway MODULES
   that form a complete chain from the fuel to the goal; a module only FIRES if
   its inputs are produced upstream (forget PDH and TCA can't fire — its acetyl-CoA
   never arrives). Hit RUN: a deterministic token-balance solve tallies ATP vs the
   target, cashing reduced carriers at OxPhos (2.5/NADH, 1.5/FADH₂ — but only with
   O₂). Optimize to par. Numbers are baked from the MCAT-verified netmap totals.
   ============================================================================ */
import { NETMAP } from '../../data/netmap';
import { el } from '../dom';
import { sfx } from '../sound';
import type { Shell } from '../shell';
import type { Medal } from '../storage';

interface WireMod {
  nodeId: string;
  needs: string[];       // carbon metabolites that must be produced upstream (or by the fuel)
  produces?: string;     // what this module makes available downstream
  atp: number;           // substrate-level ATP-equiv contribution (baked for THIS demand's scale)
  nadh?: number;
  fadh2?: number;
  nadph?: number;
  cashier?: boolean;     // OxPhos: converts pooled carriers → ATP (only with O₂)
  decoy?: boolean;       // available but not part of the intended solution
}
interface WireDemand {
  id: string;
  title: string;
  scene: string;
  fuel: { name: string; emoji: string; entry: string };
  o2: boolean;
  goal: { kind: 'atp'; target: number } | { kind: 'make'; metabolite: string; label: string };
  par: number;
  mods: WireMod[];
}

const nodeInfo = (id: string) => NETMAP.nodes.find((n) => n.id === id);

const DEMANDS: WireDemand[] = [
  {
    id: 'glucose-aerobic',
    title: 'Burn glucose, all-out',
    scene: 'A resting cell with plenty of oxygen wants every last ATP from one glucose. Wire the full aerobic line.',
    fuel: { name: 'Glucose', emoji: '🍬', entry: 'glucose' },
    o2: true, goal: { kind: 'atp', target: 30 }, par: 4,
    mods: [
      { nodeId: 'glycolysis', needs: ['glucose'], produces: 'pyruvate', atp: 2, nadh: 2 },
      { nodeId: 'pdh', needs: ['pyruvate'], produces: 'acetylCoA', atp: 0, nadh: 2 },
      { nodeId: 'tca', needs: ['acetylCoA'], produces: 'carriers', atp: 2, nadh: 6, fadh2: 2 },
      { nodeId: 'oxphos', needs: [], atp: 0, cashier: true },
      { nodeId: 'fermentation', needs: ['pyruvate'], produces: 'lactate', atp: 0, decoy: true },
      { nodeId: 'ppp', needs: ['glucose'], produces: 'ribose5p', atp: 0, nadph: 2, decoy: true },
    ],
  },
  {
    id: 'sprint-anaerobic',
    title: 'Sprint — no oxygen',
    scene: 'Muscle is contracting faster than blood delivers O₂. OxPhos is dead. Get ATP anyway — and don’t let glycolysis stall for lack of NAD⁺.',
    fuel: { name: 'Glucose', emoji: '🍬', entry: 'glucose' },
    o2: false, goal: { kind: 'atp', target: 2 }, par: 2,
    mods: [
      { nodeId: 'glycolysis', needs: ['glucose'], produces: 'pyruvate', atp: 2, nadh: 2 },
      { nodeId: 'fermentation', needs: ['pyruvate'], produces: 'lactate', atp: 0 },
      { nodeId: 'pdh', needs: ['pyruvate'], produces: 'acetylCoA', atp: 0, nadh: 2, decoy: true },
      { nodeId: 'tca', needs: ['acetylCoA'], produces: 'carriers', atp: 2, nadh: 6, fadh2: 2, decoy: true },
      { nodeId: 'oxphos', needs: [], atp: 0, cashier: true, decoy: true },
    ],
  },
  {
    id: 'palmitate-aerobic',
    title: 'Torch a fat',
    scene: 'A fasting cell breaks down palmitate (C16). Route the fat all the way to CO₂ and water — fat is the densest fuel there is.',
    fuel: { name: 'Palmitate', emoji: '🥑', entry: 'palmitate' },
    o2: true, goal: { kind: 'atp', target: 100 }, par: 3,
    mods: [
      { nodeId: 'betaOxidation', needs: ['palmitate'], produces: 'acetylCoA', atp: -2, nadh: 7, fadh2: 7 },
      { nodeId: 'tca', needs: ['acetylCoA'], produces: 'carriers', atp: 8, nadh: 24, fadh2: 8 },
      { nodeId: 'oxphos', needs: [], atp: 0, cashier: true },
      { nodeId: 'ketogenesis', needs: ['acetylCoA'], produces: 'ketoneBodies', atp: 0, decoy: true },
      { nodeId: 'glycolysis', needs: ['glucose'], produces: 'pyruvate', atp: 2, nadh: 2, decoy: true },
    ],
  },
  {
    id: 'store-fat',
    title: 'Store the surplus',
    scene: 'Fed and flush with glucose, the cell wants to BUILD fat for storage. You’ll need carbon (acetyl-CoA) AND reducing power (NADPH) — from two different places.',
    fuel: { name: 'Glucose', emoji: '🍬', entry: 'glucose' },
    o2: true, goal: { kind: 'make', metabolite: 'palmitate', label: 'Build palmitate' }, par: 4,
    mods: [
      { nodeId: 'glycolysis', needs: ['glucose'], produces: 'pyruvate', atp: 2, nadh: 2 },
      { nodeId: 'pdh', needs: ['pyruvate'], produces: 'acetylCoA', atp: 0, nadh: 2 },
      { nodeId: 'ppp', needs: ['glucose'], produces: 'nadph', atp: 0, nadph: 14 },
      { nodeId: 'fattyAcidSynthesis', needs: ['acetylCoA', 'nadph'], produces: 'palmitate', atp: -7, nadph: -14 },
      { nodeId: 'oxphos', needs: [], atp: 0, cashier: true, decoy: true },
    ],
  },
];

export function launchWireCell(shell: Shell): void {
  play(shell, 0, 0);
}

function play(shell: Shell, demandIdx: number, runningScore: number): void {
  const d = DEMANDS[demandIdx];
  const placed = new Set<string>();

  shell.setCrumb('🔌 Wire the Cell', () => shell.goHome());
  shell.setMascot(`Puzzle ${demandIdx + 1} of ${DEMANDS.length}. Build the line, then hit RUN.`, '🔌');

  const wrap = el('div.arc-wire');
  wrap.append(el('div.arc-dx-top', null,
    el('span.arc-reg-progress', null, `Puzzle ${demandIdx + 1}/${DEMANDS.length}`),
    el('span.arc-wire-par', null, `par: ${d.par} modules`)));

  const scene = el('div.arc-scene.card');
  scene.append(el('div.arc-scene-emoji', { 'aria-hidden': 'true' }, d.fuel.emoji),
    el('div', null, el('h3.arc-scene-title', null, d.title),
      el('p.arc-scene-text', null, d.scene),
      el('p.arc-wire-goal', null,
        el('span.arc-chip', null, `⛽ Fuel: ${d.fuel.name}`),
        el('span.arc-chip', null, d.o2 ? '🅾️ O₂ available' : '🚫 No O₂'),
        el('span.arc-chip.is-goal', null, d.goal.kind === 'atp' ? `🎯 ≥ ${d.goal.target} ATP` : `🎯 ${d.goal.label}`))));
  wrap.append(scene);

  wrap.append(el('p.arc-wire-lbl', null, 'Tap modules to add them to the line. A module only fires if its inputs arrive from upstream.'));
  const palette = el('div.arc-wire-palette');
  const countEl = el('span');
  for (const m of d.mods) {
    const info = nodeInfo(m.nodeId);
    const btn = el('button.arc-wire-mod', { type: 'button', 'data-mod': m.nodeId });
    btn.append(
      el('span.arc-wire-mod-ico', { 'aria-hidden': 'true' }, info?.emoji ?? '⚗️'),
      el('span.arc-wire-mod-name', null, info?.name ?? m.nodeId),
      el('span.arc-wire-mod-yield', null, yieldHint(m)),
      el('span.arc-wire-mod-state', null, ''));
    btn.addEventListener('click', () => {
      if (placed.has(m.nodeId)) { placed.delete(m.nodeId); btn.classList.remove('is-placed'); }
      else { placed.add(m.nodeId); btn.classList.add('is-placed'); }
      sfx.select();
      countEl.textContent = `${placed.size} placed`;
      balance.className = 'arc-wire-balance';
      balance.innerHTML = '';
    });
    palette.append(btn);
  }
  wrap.append(palette);

  const runBtn = el('button.arc-btn.is-primary.arc-wire-run', { type: 'button' }, '▶ RUN the cell');
  wrap.append(el('div.arc-wire-controls', null, countEl, runBtn));

  const balance = el('div.arc-wire-balance');
  wrap.append(balance);

  runBtn.addEventListener('click', () => run());

  function run(): void {
    const res = solve(d, placed);
    // mark each placed module fired/stranded
    for (const m of d.mods) {
      const btn = palette.querySelector<HTMLElement>(`[data-mod="${m.nodeId}"]`);
      const stateEl = btn?.querySelector('.arc-wire-mod-state');
      if (!btn || !stateEl) continue;
      btn.classList.remove('is-fired', 'is-stranded');
      if (placed.has(m.nodeId)) {
        if (res.fired.has(m.nodeId) || (m.cashier && res.oxphosCashed)) { btn.classList.add('is-fired'); stateEl.textContent = '✓ firing'; }
        else if (m.cashier) { stateEl.textContent = d.o2 ? '· no carriers' : '· no O₂'; btn.classList.add('is-stranded'); }
        else { btn.classList.add('is-stranded'); stateEl.textContent = '✗ stranded'; }
      } else stateEl.textContent = '';
    }
    const won = d.goal.kind === 'atp' ? res.atp >= d.goal.target : res.made;
    balance.className = 'arc-wire-balance is-shown card';
    balance.innerHTML = '';
    const rows: Array<[string, string]> = [];
    if (d.goal.kind === 'atp') {
      rows.push(['Substrate-level ATP', fmt(res.slpAtp)]);
      rows.push(['Cashed at OxPhos', res.oxphosCashed ? `+${res.cashed.toFixed(1)} (${res.nadh} NADH, ${res.fadh2} FADH₂)` : `0 — carriers wasted (${res.nadh} NADH, ${res.fadh2} FADH₂)`]);
      rows.push(['Total ATP', `${res.atp.toFixed(res.atp % 1 ? 1 : 0)} / ${d.goal.target} target`]);
    } else {
      rows.push([d.goal.label, res.made ? '✓ produced' : '✗ not produced — a required module didn’t fire']);
      rows.push(['Net ATP cost', fmt(res.atp)]);
      if (res.nadphNet) rows.push(['NADPH used', String(-res.nadphNet)]);
    }
    rows.push(['Modules used', `${placed.size} (par ${d.par})`]);
    const sheet = el('dl.arc-wire-sheet');
    for (const [k, v] of rows) sheet.append(el('dt', null, k), el('dd', null, v));
    balance.append(
      el('p.arc-wire-verdict', null, won ? '✓ It flows!' : '✗ Not there yet — check the balance sheet.'),
      sheet,
      el('p.arc-wire-teach', null, res.teach),
    );
    if (won) { sfx.correct(); shell.setMascot('It flows! Beautiful wiring.', '🔌'); nextBtn(); }
    else { sfx.wrong(); shell.setMascot('The line’s broken somewhere — read the sheet.', '😵'); }

    function nextBtn(): void {
      const perfect = placed.size <= d.par && res.noWaste;
      const gained = perfect ? 500 : 300;
      const next = el('button.arc-btn.is-primary', { type: 'button' }, demandIdx + 1 < DEMANDS.length ? 'Next puzzle →' : 'See results →');
      next.addEventListener('click', () => {
        sfx.select();
        const score = runningScore + gained;
        if (demandIdx + 1 < DEMANDS.length) play(shell, demandIdx + 1, score);
        else finish(score);
      });
      balance.append(el('p.arc-wire-medal', null, perfect ? `⭐ Par or better — clean build! (+${gained})` : `Solved (+${gained}). Try it in ${d.par} modules for the star.`), next);
    }
  }

  function finish(score: number): void {
    const medal: Medal = score >= DEMANDS.length * 450 ? 'gold' : score >= DEMANDS.length * 300 ? 'silver' : 'bronze';
    shell.showResults({
      recordId: 'wire', mode: 'wire', won: true, medal, score,
      headline: medal === 'gold' ? 'Master cell-wirer!' : 'Cell wired',
      lines: [['Puzzles', `${DEMANDS.length} solved`]],
      funFact: 'Every one of those ATP totals — 32 from glucose, 106 from palmitate — is the real number the MCAT asks you to reconstruct. You just built the machine that makes it.',
      replay: () => play(shell, 0, 0),
    });
  }

  shell.setStage(wrap);
}

function yieldHint(m: WireMod): string {
  if (m.cashier) return 'cashes NADH/FADH₂ → ATP (needs O₂)';
  const parts: string[] = [];
  if (m.atp) parts.push(`${m.atp > 0 ? '+' : ''}${m.atp} ATP`);
  if (m.nadh) parts.push(`${m.nadh} NADH`);
  if (m.fadh2) parts.push(`${m.fadh2} FADH₂`);
  if (m.nadph) parts.push(`${m.nadph > 0 ? '+' : ''}${m.nadph} NADPH`);
  return parts.join(' · ') || 'routing';
}
function fmt(n: number): string { return n > 0 ? `+${n}` : String(n); }

interface SolveResult {
  fired: Set<string>; slpAtp: number; nadh: number; fadh2: number; cashed: number;
  oxphosCashed: boolean; atp: number; made: boolean; nadphNet: number; noWaste: boolean; teach: string;
}

function solve(d: WireDemand, placed: Set<string>): SolveResult {
  const available = new Set<string>([d.fuel.entry]);
  const fired = new Set<string>();
  let changed = true;
  while (changed) {
    changed = false;
    for (const m of d.mods) {
      if (m.cashier || !placed.has(m.nodeId) || fired.has(m.nodeId)) continue;
      if (m.needs.every((n) => available.has(n))) {
        fired.add(m.nodeId);
        if (m.produces) available.add(m.produces);
        changed = true;
      }
    }
  }
  let slpAtp = 0, nadh = 0, fadh2 = 0, nadphNet = 0;
  for (const m of d.mods) {
    if (!fired.has(m.nodeId)) continue;
    slpAtp += m.atp || 0; nadh += m.nadh || 0; fadh2 += m.fadh2 || 0; nadphNet += m.nadph || 0;
  }
  const oxphos = d.mods.find((m) => m.cashier);
  const oxphosPlaced = !!oxphos && placed.has(oxphos.nodeId);
  const oxphosCashed = oxphosPlaced && d.o2 && (nadh + fadh2 > 0);
  const cashed = oxphosCashed ? nadh * 2.5 + fadh2 * 1.5 : 0;

  // NAD⁺-regeneration rule: glycolytic substrate-level ATP only counts if the NADH
  // it makes is reoxidized — by OxPhos (with O₂) OR by fermentation. Else it stalls.
  let stallAdj = 0;
  const glyc = d.mods.find((m) => m.nodeId === 'glycolysis');
  if (glyc && fired.has('glycolysis')) {
    const nadRegen = oxphosCashed || fired.has('fermentation');
    if (!nadRegen) stallAdj = -(glyc.atp || 0); // remove the stranded glycolytic ATP
  }
  const atp = slpAtp + cashed + stallAdj;
  const made = d.goal.kind === 'make' ? available.has(d.goal.metabolite) : false;

  const placedCount = placed.size;
  const noWaste = placedCount <= d.par && [...placed].every((id) => fired.has(id) || (oxphos && id === oxphos.nodeId && oxphosCashed));

  // teaching line
  let teach = '';
  if (d.id === 'glucose-aerobic') teach = oxphosCashed ? 'The full aerobic line: substrate-level ATP is a rounding error; OxPhos cashing the 10 NADH + 2 FADH₂ is where ~90% of the yield lives.' : 'Without OxPhos (or with the bridge/cycle missing), the NADH never becomes ATP — you leave almost all the energy on the table.';
  else if (d.id === 'sprint-anaerobic') teach = fired.has('fermentation') ? 'Fermentation makes zero ATP itself — its job is regenerating NAD⁺ so glycolysis keeps firing for that net +2. That’s the whole anaerobic economy.' : 'Glycolysis stalls without a way to regenerate NAD⁺. No fermentation, no O₂ → GAPDH backs up and even the +2 ATP disappears.';
  else if (d.id === 'palmitate-aerobic') teach = atp >= 100 ? 'Fat is the densest fuel: −2 to activate, then 7 rounds feed 8 acetyl-CoA to the cycle, and OxPhos cashes 31 NADH + 15 FADH₂ → ~106 ATP.' : 'β-oxidation only makes carriers — with no cycle + OxPhos to cash them (and O₂), the fat’s energy stays locked up.';
  else if (d.id === 'store-fat') teach = made ? 'Building fat needs BOTH: carbon as acetyl-CoA (glucose → PDH) and reducing power as NADPH (from the pentose phosphate pathway). It COSTS ATP and NADPH — storage is an investment.' : 'Fatty-acid synthase needs acetyl-CoA AND NADPH at once — miss either supply line (PDH for carbon, PPP for NADPH) and nothing gets built.';

  return { fired, slpAtp, nadh, fadh2, cashed, oxphosCashed, atp, made, nadphNet, noWaste, teach };
}
