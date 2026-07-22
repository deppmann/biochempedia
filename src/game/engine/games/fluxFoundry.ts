/* =============================================================================
   FLUX FOUNDRY — a metabolic engine-builder roguelite (the Balatro of biochem).
   -----------------------------------------------------------------------------
   Each round a hormonal EVENT (fed / fasted / sprint / rest) re-prices every fuel
   via the netmap states{} multipliers; you pick one of three drawn FUELS and route
   it through the pathway nodes you OWN to beat an escalating ATP quota; between
   rounds you DRAFT a new node or relic. The physiology IS the strategy: fat is
   king when fasted (×2), glycolysis is throttled in the fasting liver (×0.3), and
   a sprint kills OxPhos so only fermentation scrapes by. Miss the quota → starve.
   ============================================================================ */
import { NETMAP } from '../../data/netmap';
import type { FuelState } from '../../netmap';
import { el, shuffle } from '../dom';
import { sfx } from '../sound';
import type { Shell } from '../shell';
import type { Medal } from '../storage';

interface FoFuel {
  id: string; name: string; emoji: string;
  aerobic: number; anaerobic: number;
  req: string[];      // nodes needed for full aerobic oxidation
  anReq: string[];    // nodes needed for the anaerobic fallback (empty = none)
  entry: string;      // netmap node id (its states{} set the round multiplier)
}
const FUELS: FoFuel[] = [
  { id: 'glucose', name: 'Glucose', emoji: '🍬', aerobic: 32, anaerobic: 2, req: ['glycolysis', 'pdh', 'tca', 'oxphos'], anReq: ['glycolysis', 'fermentation'], entry: 'glycolysis' },
  { id: 'glycogen', name: 'Glycogen', emoji: '🌳', aerobic: 33, anaerobic: 3, req: ['glycogenolysis', 'glycolysis', 'pdh', 'tca', 'oxphos'], anReq: ['glycogenolysis', 'glycolysis', 'fermentation'], entry: 'glycogenolysis' },
  { id: 'palmitate', name: 'Palmitate (fat)', emoji: '🥑', aerobic: 106, anaerobic: 0, req: ['betaOxidation', 'tca', 'oxphos'], anReq: [], entry: 'betaOxidation' },
  { id: 'lactate', name: 'Lactate', emoji: '🥛', aerobic: 15, anaerobic: 0, req: ['pdh', 'tca', 'oxphos'], anReq: [], entry: 'pdh' },
  { id: 'aa', name: 'Amino acid', emoji: '🥩', aerobic: 15, anaerobic: 0, req: ['tca', 'oxphos'], anReq: [], entry: 'tca' },
];

interface Relic { id: string; name: string; desc: string; mult: number; applies: (f: FoFuel, mode: string) => boolean; }
const RELICS: Relic[] = [
  { id: 'etc', name: 'Efficient ETC', desc: '+15% from any aerobic burn', mult: 1.15, applies: (_f, m) => m === 'aerobic' },
  { id: 'carnitine', name: 'Carnitine loading', desc: '+30% from fat', mult: 1.3, applies: (f) => f.id === 'palmitate' },
  { id: 'shuttle', name: 'Malate–aspartate shuttle', desc: '+15% from aerobic carbs', mult: 1.15, applies: (f, m) => m === 'aerobic' && (f.id === 'glucose' || f.id === 'glycogen') },
  { id: 'mito', name: 'Extra mitochondria', desc: '+20% from everything', mult: 1.2, applies: () => true },
];

const STATE_INFO: Record<FuelState, { emoji: string; label: string; note: string }> = {
  fed: { emoji: '🥞', label: 'FED', note: 'Insulin high. Glycolysis floors it; fat-burning idles.' },
  fasted: { emoji: '⏳', label: 'FASTED', note: 'Glucagon high. Fat is king; the liver throttles glycolysis.' },
  sprint: { emoji: '🏃', label: 'SPRINT', note: 'No O₂! OxPhos is dead — only fermentation makes ATP, and not much.' },
  rest: { emoji: '😌', label: 'REST', note: 'Steady state. Everything runs at baseline.' },
};

const DRAFT_NODES = [
  { nodeId: 'betaOxidation', unlocks: 'Palmitate (fat) — huge when fasted' },
  { nodeId: 'glycogenolysis', unlocks: 'Glycogen — a touch better than glucose' },
];

const nodeInfo = (id: string) => NETMAP.nodes.find((n) => n.id === id);

function computeYield(fuel: FoFuel, state: FuelState, owned: Set<string>, relics: Relic[]): { atp: number; mode: 'aerobic' | 'anaerobic' | 'blocked'; sMult: number } {
  const entry = nodeInfo(fuel.entry);
  const sMult = entry?.states?.[state] ?? 1;
  const o2 = state !== 'sprint';
  let base = 0;
  let mode: 'aerobic' | 'anaerobic' | 'blocked' = 'blocked';
  if (o2 && fuel.req.every((n) => owned.has(n))) { base = fuel.aerobic; mode = 'aerobic'; }
  else if (fuel.anReq.length && fuel.anReq.every((n) => owned.has(n))) { base = fuel.anaerobic; mode = 'anaerobic'; }
  else return { atp: 0, mode: 'blocked', sMult };
  let m = sMult;
  for (const r of relics) if (r.applies(fuel, mode)) m *= r.mult;
  return { atp: Math.round(base * m), mode, sMult };
}
const quotaFor = (round: number, state: FuelState): number => {
  // A sprint is brief and anaerobic — you only need a scrape of ATP, and can't make
  // more, so its quota stays low regardless of round (glucose+fermentation clears it).
  if (state === 'sprint') return 4;
  return Math.ceil(16 * Math.pow(1.3, round - 1));
};

/** The draw ALWAYS includes glucose (the universal fuel) + 2 others, so a bad draw
 *  can't instantly starve you — the choice is which fuel is best for THIS state. */
function drawFuels(): FoFuel[] {
  const glucose = FUELS.find((f) => f.id === 'glucose')!;
  const others = shuffle(FUELS.filter((f) => f.id !== 'glucose')).slice(0, 2);
  return shuffle([glucose, ...others]);
}

export function launchFluxFoundry(shell: Shell): void {
  const owned = new Set<string>(['glycolysis', 'pdh', 'tca', 'oxphos', 'fermentation']);
  const relics: Relic[] = [];
  let round = 1, banked = 0;
  const weighted: FuelState[] = ['fed', 'fasted', 'sprint', 'rest', 'fed', 'fasted', 'rest'];

  shell.setCrumb('🏭 Flux Foundry', () => shell.goHome());

  function playRound(): void {
    const state: FuelState = round === 1 ? 'rest' : weighted[Math.floor(Math.random() * weighted.length)];
    const quota = quotaFor(round, state);
    const drawn = drawFuels();
    let picked: FoFuel | null = null;
    shell.setMascot(`Round ${round}. ${STATE_INFO[state].label} — read the room, pick your fuel.`, STATE_INFO[state].emoji);

    const wrap = el('div.arc-foundry');
    wrap.append(el('div.arc-foundry-top', null,
      el('span.arc-foundry-round', null, `Round ${round}`),
      el('span.arc-foundry-quota', null, `Quota: ${quota} ATP`),
      el('span.arc-foundry-bank', null, `Banked: ⚡${banked}`)));

    const ev = el('div.arc-foundry-event.card');
    ev.append(el('span.arc-foundry-event-emoji', { 'aria-hidden': 'true' }, STATE_INFO[state].emoji),
      el('div', null, el('p.arc-foundry-event-label', null, `${STATE_INFO[state].label} state`), el('p.arc-foundry-event-note', null, STATE_INFO[state].note)));
    wrap.append(ev);

    wrap.append(el('p.arc-foundry-lbl', null, 'Draw: pick ONE fuel to run through your engine this round.'));
    const fuelRow = el('div.arc-foundry-fuels');
    const processBtn = el('button.arc-btn.is-primary.arc-foundry-process', { type: 'button', disabled: true }, '⚙ Process fuel');
    for (const f of drawn) {
      const y = computeYield(f, state, owned, relics);
      const card = el(`button.arc-foundry-fuel${y.atp === 0 ? '.is-blocked' : ''}`, { type: 'button' });
      card.append(
        el('span.arc-foundry-fuel-emoji', { 'aria-hidden': 'true' }, f.emoji),
        el('span.arc-foundry-fuel-name', null, f.name),
        el('span.arc-foundry-fuel-yield', null, y.mode === 'blocked' ? '✗ can’t process' : `≈ ${y.atp} ATP · ${y.mode}`),
      );
      card.addEventListener('click', () => {
        picked = f;
        Array.from(fuelRow.children).forEach((c) => c.classList.remove('is-picked'));
        card.classList.add('is-picked');
        (processBtn as HTMLButtonElement).disabled = false;
        sfx.select();
      });
      fuelRow.append(card);
    }
    wrap.append(fuelRow);

    // engine display
    const engine = el('div.arc-foundry-engine');
    engine.append(el('span.arc-foundry-engine-lbl', null, 'Your engine:'));
    for (const id of owned) engine.append(el('span.arc-foundry-chip', null, `${nodeInfo(id)?.emoji ?? '⚗️'} ${nodeInfo(id)?.name ?? id}`));
    for (const r of relics) engine.append(el('span.arc-foundry-chip.is-relic', null, `✨ ${r.name}`));
    wrap.append(engine);
    wrap.append(processBtn);

    const outcome = el('div.arc-foundry-outcome');
    wrap.append(outcome);

    processBtn.addEventListener('click', () => {
      if (!picked) return;
      const y = computeYield(picked, state, owned, relics);
      banked += y.atp;
      (processBtn as HTMLButtonElement).disabled = true;
      Array.from(fuelRow.querySelectorAll('button')).forEach((b) => ((b as HTMLButtonElement).disabled = true));
      const survived = y.atp >= quota;
      outcome.className = 'arc-foundry-outcome is-shown card';
      outcome.append(
        el('p.arc-foundry-outcome-head', null, survived ? `✓ +${y.atp} ATP — quota met!` : `✗ Only ${y.atp} ATP — quota was ${quota}. The cell starves.`),
        el('p.arc-foundry-outcome-note', null, yieldNarr(picked, state, y.mode, y.sMult)),
      );
      if (survived) { sfx.correct(); shell.setMascot('Quota met! Bank it and upgrade.', '🏭'); const b = el('button.arc-btn.is-primary', { type: 'button' }, 'Draft an upgrade →'); b.addEventListener('click', () => { sfx.select(); draft(); }); outcome.append(b); }
      else { finish(); }
    });

    shell.setStage(wrap);
  }

  function draft(): void {
    round++;
    shell.setMascot('Draft one upgrade to grow your engine.', '✨');
    const pool: Array<{ kind: 'node'; nodeId: string; unlocks: string } | { kind: 'relic'; relic: Relic }> = [];
    for (const n of DRAFT_NODES) if (!owned.has(n.nodeId)) pool.push({ kind: 'node', ...n });
    for (const r of RELICS) if (!relics.some((x) => x.id === r.id)) pool.push({ kind: 'relic', relic: r });
    const offer = shuffle(pool).slice(0, 3);
    const wrap = el('div.arc-foundry');
    wrap.append(el('h3.arc-foundry-draft-title', null, `Round ${round - 1} cleared — draft an upgrade`));
    const row = el('div.arc-foundry-draftrow');
    for (const o of offer) {
      const card = el('button.arc-foundry-draft', { type: 'button' });
      if (o.kind === 'node') {
        card.append(el('span.arc-foundry-draft-ico', null, nodeInfo(o.nodeId)?.emoji ?? '⚗️'),
          el('span.arc-foundry-draft-name', null, nodeInfo(o.nodeId)?.name ?? o.nodeId),
          el('span.arc-foundry-draft-desc', null, `Unlocks ${o.unlocks}`));
        card.addEventListener('click', () => { owned.add(o.nodeId); sfx.correct(); playRound(); });
      } else {
        card.append(el('span.arc-foundry-draft-ico', null, '✨'),
          el('span.arc-foundry-draft-name', null, o.relic.name),
          el('span.arc-foundry-draft-desc', null, o.relic.desc));
        card.addEventListener('click', () => { relics.push(o.relic); sfx.correct(); playRound(); });
      }
      row.append(card);
    }
    if (offer.length === 0) {
      const b = el('button.arc-btn.is-primary', { type: 'button' }, 'Onward →');
      b.addEventListener('click', () => playRound());
      row.append(el('p.arc-foundry-lbl', null, 'Engine maxed — press on.'), b);
    }
    wrap.append(row);
    shell.setStage(wrap);
  }

  function finish(): void {
    const survived = round - 1;
    const medal: Medal = survived >= 8 ? 'gold' : survived >= 5 ? 'silver' : survived >= 3 ? 'bronze' : 'none';
    shell.showResults({
      recordId: 'foundry', mode: 'foundry', won: survived >= 3, medal, score: banked,
      headline: survived >= 8 ? 'Metabolic tycoon!' : `Survived ${survived} round${survived === 1 ? '' : 's'}`,
      lines: [['Rounds survived', String(survived)], ['Total ATP banked', `⚡ ${banked.toLocaleString()}`], ['Engine size', `${owned.size} nodes · ${relics.length} relics`]],
      funFact: 'The re-pricing you just felt is real: a fasting body runs on fat because glucagon throttles glycolysis and revs β-oxidation — and a sprinting muscle nets barely 2 ATP/glucose because there’s no O₂ to run OxPhos.',
      replay: () => launchFluxFoundry(shell),
    });
  }

  playRound();
}

function yieldNarr(fuel: FoFuel, state: FuelState, mode: string, sMult: number): string {
  if (mode === 'blocked') return state === 'sprint' && fuel.id === 'palmitate' ? 'Fat needs oxygen — β-oxidation and OxPhos are dead in a sprint. Never burn fat anaerobically.' : 'Your engine can’t route this fuel yet — draft the missing pathway.';
  if (mode === 'anaerobic') return 'Anaerobic: fermentation regenerates NAD⁺ for a measly ~2 ATP/glucose. That’s all a sprint can give.';
  const bonus = sMult > 1 ? `The ${STATE_INFO[state].label} state up-regulates this route (×${sMult}).` : sMult < 1 ? `The ${STATE_INFO[state].label} state throttles this route (×${sMult}) — physiology, not a bug.` : 'Baseline throughput.';
  return `Full aerobic oxidation. ${bonus}`;
}
