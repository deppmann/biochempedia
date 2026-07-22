/* =============================================================================
   Hub — the game-first home of the Metabolism Arcade.
   -----------------------------------------------------------------------------
   Lists the games as big cards; each game owns its own pathway/level select.
   Replaces the old "pick a pathway → 4 basic modes" flow. Games light up here
   as they ship; the timed Gauntlet is kept as the cram tool.
   ============================================================================ */
import type { Pathway } from '../types';
import { el } from './dom';
import { sfx } from './sound';
import { createShell } from './shell';
import type { Shell } from './shell';
import type { ModeId } from './storage';
import { launchLedgerRush } from './games/ledgerRush';
import { launchAutopsy } from './games/autopsy';
import { launchWireCell } from './games/wireCell';
import { launchFluxFoundry } from './games/fluxFoundry';
import { launchMixingBoard } from './games/mixingBoard';
import { launchGauntlet } from './games/gauntlet';

interface GameDef {
  id: ModeId;
  icon: string;
  name: string;
  verb: string;
  blurb: string;
  status: 'live' | 'soon';
  cram?: boolean;
  launch?: (shell: Shell, pathways: Pathway[]) => void;
}

const GAMES: GameDef[] = [
  { id: 'ledger', icon: '⚡', name: 'Ledger Rush', verb: 'Dexterity', status: 'live', launch: launchLedgerRush,
    blurb: 'Bank the real ATP & NADH, toss the misconceptions, catch DOUBLE after the split. A speed drill for the energetics ledger.' },
  { id: 'autopsy', icon: '🔬', name: 'Metabolic Autopsy', verb: 'Deduction', status: 'live', launch: launchAutopsy,
    blurb: 'One enzyme is secretly broken. Order lab tests, read what pools up vs starves, and prove the block in the fewest tests.' },
  { id: 'wire', icon: '🔌', name: 'Wire the Cell', verb: 'Construction', status: 'live', launch: launchWireCell,
    blurb: 'Snap pathway modules together so the tokens balance, hit RUN, and watch the flux flow. A Zachlike metabolism puzzle.' },
  { id: 'foundry', icon: '🏭', name: 'Flux Foundry', verb: 'Engine-builder', status: 'live', launch: launchFluxFoundry,
    blurb: 'Draw a fuel, route its carbon, chase an ATP quota as fed/fasted/sprint events re-price the whole economy. One more run.' },
  { id: 'mixing', icon: '🎛️', name: 'Mixing Board', verb: 'Control', status: 'live', launch: launchMixingBoard,
    blurb: 'You are the cell’s regulators. Set the board so flux lands right for THIS body state — and never run the futile cycle.' },
  { id: 'gauntlet', icon: '🎓', name: 'MCAT Gauntlet', verb: 'Cram tool', status: 'live', cram: true, launch: launchGauntlet,
    blurb: 'Timed rapid-fire across every pathway. The spaced-retrieval drill for the night before test day.' },
];

export function mountHub(root: HTMLElement, pathways: Pathway[]): void {
  let shell: Shell;

  function home(): void {
    shell.setCrumb('Metabolism Arcade', undefined);
    shell.setMascot('Five games, one cell. Pick your poison.', '🧬');
    const wrap = el('div.arc-home');
    wrap.append(
      el('p.arc-eyebrow', null, 'Metabolism Arcade'),
      el('h1.arc-title', null, 'Five ways to ', el('em', null, 'actually'), ' know the pathways.'),
      el('p.arc-lede', null,
        'Not a quiz with a skin. Five different games — a reflex drill, a diagnosis mystery, a wiring puzzle, an engine-builder, and a control board — each one built so the fun comes from the biochemistry itself. Plus a timed cram tool for test week.'),
    );
    const grid = el('div.arc-gamegrid');
    for (const g of GAMES) {
      const card = el(`button.arc-gamecard${g.status === 'soon' ? '.is-soon' : ''}${g.cram ? '.is-cram' : ''}`, { type: 'button' });
      card.append(
        el('span.arc-gamecard-ico', { 'aria-hidden': 'true' }, g.icon),
        el('span.arc-gamecard-verb', null, g.verb),
        el('span.arc-gamecard-name', null, g.name),
        el('span.arc-gamecard-blurb', null, g.blurb),
        el('span.arc-gamecard-cta', null, g.status === 'live' ? 'PLAY ▶' : '🧪 in the lab'),
      );
      card.addEventListener('click', () => {
        sfx.select();
        if (g.status === 'live' && g.launch) g.launch(shell, pathways);
        else comingSoon(g);
      });
      grid.append(card);
    }
    wrap.append(grid);
    wrap.append(el('p.arc-hometip', null, 'Every wrong answer explains itself — that’s the point. Getting it wrong here is how you get it right on test day.'));
    shell.setStage(wrap);
  }

  function comingSoon(g: GameDef): void {
    shell.setCrumb(`${g.icon} ${g.name}`, () => home());
    shell.setMascot('This one’s still on the bench. Soon!', '🧪');
    const wrap = el('div.arc-home');
    wrap.append(
      el('p.arc-eyebrow', null, g.verb),
      el('h1.arc-title', null, g.name),
      el('p.arc-lede', null, g.blurb),
      el('div.arc-soon-card.card', null,
        el('p', { html: '🧪 <strong>In the lab.</strong> This game is being built and biochem-verified right now. Try <strong>Ledger Rush</strong> or the <strong>MCAT Gauntlet</strong> while you wait.' })),
    );
    const back = el('button.arc-btn.is-primary', { type: 'button' }, '‹ Back to all games');
    back.addEventListener('click', () => { sfx.select(); home(); });
    wrap.append(back);
    shell.setStage(wrap);
  }

  shell = createShell(root, home);
  home();
}
