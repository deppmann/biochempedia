/* =============================================================================
   METABOLIC AUTOPSY — hidden-block deduction (the Wordle/Mastermind of defects).
   -----------------------------------------------------------------------------
   One enzyme is secretly deficient. Test metabolites down the ladder — substrate
   ACCUMULATES upstream of the block (HIGH), product is STARVED downstream (LOW) —
   run a confirmatory assay, then ACCUSE the enzyme in the fewest tests. The
   single most transferable clinical-biochem heuristic, turned into a logic game.
   Block point is derived by matching a real disease's deficient enzyme to a step;
   "mystery samples" (a random blocked step) fill out the case load on any pathway.
   ============================================================================ */
import type { Pathway, Disease } from '../../types';
import { el, shuffle } from '../dom';
import { sfx } from '../sound';
import type { Shell } from '../shell';
import type { Medal } from '../storage';

function norm(s: string): string {
  return s.toLowerCase().replace(/[^a-z0-9]/g, '');
}

/* Poisons / uncouplers / multi-enzyme "couples" are NOT clean single-step blocks —
   glycolysis keeps flowing (arsenate) or the lesion isn't a metabolite dam — so the
   upstream-HIGH/downstream-LOW deduction would MIS-TEACH. Exclude them from Autopsy. */
const NOT_A_CLEAN_BLOCK = /(couple|poison|mechanism|uncoupl|arsen|cyanide|rotenone|oligomycin|antimycin|2,?4-?dnp|dinitrophenol|malonate|toxin|inhibit|fluoroacet)/i;

/** Find the 0-based step index whose enzyme matches a disease's deficient enzyme. */
function deriveBlockStep(d: Disease, p: Pathway): number {
  const correct = d.suspects[d.answer] ?? '';
  if (NOT_A_CLEAN_BLOCK.test(correct) || NOT_A_CLEAN_BLOCK.test(d.name)) return -1;
  if (typeof d.blockStep === 'number' && d.blockStep >= 0 && d.blockStep < p.steps.length) return d.blockStep;
  const target = norm(correct);
  if (!target) return -1;
  let best = -1;
  p.steps.forEach((s, i) => {
    const e = norm(s.enzyme);
    if (best < 0 && (e === target || e.includes(target) || target.includes(e))) best = i;
  });
  return best;
}

interface Case {
  blockStep: number;      // 0-based index into p.steps
  title: string;
  chart: string;          // the vignette / sample description
  named: boolean;
  accumulates: string;    // what the confirmatory assay reveals
  pearl?: string;
  teach?: string;
}

function buildCases(p: Pathway): Case[] {
  const cases: Case[] = [];
  const usedSteps = new Set<number>();
  // named disease cases first (richest), where the block maps to a step
  for (const d of shuffle(p.diseases)) {
    const b = deriveBlockStep(d, p);
    if (b >= 0 && !usedSteps.has(b)) {
      usedSteps.add(b);
      cases.push({
        blockStep: b, title: d.name, chart: d.vignette, named: true,
        accumulates: d.accumulates ?? `${p.steps[b].short} and everything upstream`,
        pearl: d.pearl, teach: d.teach,
      });
    }
  }
  // fill to 4 rounds with "mystery samples" (a random un-used blocked step)
  const candidates = shuffle(p.steps.map((_, i) => i).filter((i) => !usedSteps.has(i)));
  while (cases.length < 4 && candidates.length) {
    const b = candidates.pop()!;
    usedSteps.add(b);
    const upstream = b === 0 ? p.startShort : p.steps[b - 1].short;
    cases.push({
      blockStep: b,
      title: `Lab sample`,
      chart: `An unlabeled sample of ${p.name.toLowerCase()} intermediates. One enzyme is deficient — the classic pattern is showing. Localize the block.`,
      named: false,
      accumulates: `${upstream} (the substrate just upstream of the block)`,
    });
  }
  return cases.slice(0, 4);
}

export function launchAutopsy(shell: Shell, pathways: Pathway[]): void {
  const eligible = pathways.filter((p) => p.steps.length >= 3);
  shell.pathwayPicker({
    title: '🔬 Metabolic Autopsy',
    sub: 'One enzyme is secretly broken. Test the ladder, read the accumulate/deplete pattern, and prove the block in the fewest tests.',
    pathways: eligible, mode: 'autopsy',
    onBack: () => shell.goHome(),
    onPick: (p) => play(shell, pathways, p),
  });
}

function play(shell: Shell, pathways: Pathway[], p: Pathway): void {
  const cases = buildCases(p);
  let caseIdx = 0, lives = 3, score = 0, totalTests = 0, solved = 0;

  shell.setCrumb(`🔬 Metabolic Autopsy · ${p.name}`, () => launchAutopsy(shell, pathways));

  // metabolite ladder: pos 0 = start, pos i = product of step i
  const metaboliteAt = (i: number) => (i === 0 ? { name: p.start, short: p.startShort } : { name: p.steps[i - 1].product, short: p.steps[i - 1].short });
  const N = p.steps.length;

  function renderCase(): void {
    const c = cases[caseIdx];
    let tests = 0, assayed = false, accused = false;
    // known reads: pos -> 'high'|'low'|undefined
    const reads: Record<number, 'high' | 'low'> = {};
    shell.setMascot(`Case ${caseIdx + 1} of ${cases.length}. Where does the trail go cold?`, '🔬');

    const wrap = el('div.arc-autopsy');
    wrap.append(el('div.arc-dx-top', null,
      el('span.arc-reg-progress', null, `Case ${caseIdx + 1}/${cases.length}`),
      el('span.arc-autopsy-lives', { 'aria-label': `${lives} lives` }, '❤️'.repeat(lives) + '🖤'.repeat(3 - lives)),
      el('span.arc-autopsy-tests', null, 'tests: ', el('strong', { 'data-tests': '' }, '0'))));

    const chart = el('div.arc-chart.card');
    chart.append(el('div.arc-chart-emoji', { 'aria-hidden': 'true' }, c.named ? '🧑‍⚕️' : '🧪'),
      el('div', null, el('p.arc-chart-label', null, c.named ? 'PATIENT CHART' : 'UNLABELED SAMPLE'), el('p.arc-chart-vignette', null, c.chart)));
    wrap.append(chart);

    wrap.append(el('p.arc-autopsy-prompt', null, 'Assay a metabolite — ',
      el('span.arc-hi', null, 'HIGH'), ' = it pooled up (you’re upstream of the block); ',
      el('span.arc-lo', null, 'LOW'), ' = it’s starved (downstream). The block is where HIGH turns to LOW.'));

    // ladder of testable metabolites
    const ladder = el('div.arc-ladder');
    const testsEl = wrap.querySelector<HTMLElement>('[data-tests]')!;
    for (let i = 0; i <= N; i++) {
      const m = metaboliteAt(i);
      const cell = el('button.arc-ladder-cell', { type: 'button', 'data-pos': i });
      cell.append(el('span.arc-ladder-name', null, m.short));
      cell.append(el('span.arc-ladder-read', null, '?'));
      cell.addEventListener('click', () => testMetabolite(i, cell));
      ladder.append(cell);
      if (i < N) ladder.append(el('span.arc-ladder-arrow', { 'aria-hidden': 'true' }, '↓'));
    }
    wrap.append(ladder);

    // confirmatory assay
    const assayBtn = el('button.arc-btn.arc-autopsy-assay', { type: 'button' }, '🧪 Run confirmatory assay (costs a test)');
    const assayOut = el('p.arc-autopsy-assayout');
    assayBtn.addEventListener('click', () => {
      if (accused || assayed) return;
      assayed = true; tests++; totalTests++; testsEl.textContent = String(tests);
      sfx.tick();
      (assayBtn as HTMLButtonElement).disabled = true;
      assayOut.className = 'arc-autopsy-assayout is-shown';
      assayOut.textContent = `Assay: ${c.accumulates} reads HIGH — consistent with a block right after it.`;
    });
    wrap.append(assayBtn, assayOut);

    // accuse
    wrap.append(el('p.arc-autopsy-accuse-lbl', null, 'When you’re sure, accuse the deficient enzyme:'));
    const accuseWrap = el('div.arc-autopsy-suspects');
    const teach = el('div.arc-teachbox');
    p.steps.forEach((s, i) => {
      const b = el('button.arc-opt.arc-autopsy-suspect', { type: 'button' }, `${i + 1}. ${s.enzyme}`);
      b.addEventListener('click', () => accuse(i, s.enzyme));
      accuseWrap.append(b);
    });
    wrap.append(accuseWrap, teach);

    function testMetabolite(pos: number, cell: HTMLElement): void {
      if (accused || reads[pos] !== undefined) return;
      tests++; totalTests++; testsEl.textContent = String(tests);
      const r: 'high' | 'low' = pos <= c.blockStep ? 'high' : 'low';
      reads[pos] = r;
      cell.classList.add(r === 'high' ? 'is-high' : 'is-low', 'is-tested');
      const readEl = cell.querySelector('.arc-ladder-read')!;
      readEl.textContent = r === 'high' ? '⬆ HIGH' : '⬇ LOW';
      sfx.tick();
    }

    function accuse(i: number, enzyme: string): void {
      if (accused) return;
      const right = i === c.blockStep;
      if (!right) {
        lives--; sfx.wrong();
        const btn = Array.from(accuseWrap.children)[i] as HTMLButtonElement;
        btn.classList.add('is-wrong'); btn.disabled = true;
        shell.setMascot('Wrong suspect — the pattern says otherwise.', '😵');
        wrap.querySelector('.arc-autopsy-lives')!.textContent = '❤️'.repeat(Math.max(0, lives)) + '🖤'.repeat(3 - Math.max(0, lives));
        if (lives <= 0) reveal(false);
        return;
      }
      accused = true; solved++; sfx.correct();
      Array.from(accuseWrap.children).forEach((ch) => ((ch as HTMLButtonElement).disabled = true));
      (Array.from(accuseWrap.children)[i] as HTMLElement).classList.add('is-correct');
      // score: fewer tests = better
      const caseScore = Math.max(120, 700 - tests * 55);
      score += caseScore;
      reveal(true, enzyme, caseScore);
    }

    function reveal(win: boolean, enzyme?: string, caseScore?: number): void {
      accused = true;
      const up = c.blockStep === 0 ? p.startShort : p.steps[c.blockStep - 1].short;
      const down = p.steps[c.blockStep].short;
      teach.className = 'arc-teachbox is-shown card';
      teach.append(
        el('p.arc-dx-verdict', null, win ? `✓ ${enzyme} — nailed it in ${tests} test${tests === 1 ? '' : 's'} (+${caseScore})` : `✗ Out of lives. It was ${p.steps[c.blockStep].enzyme}.`),
        el('p.arc-dx-line', null, el('strong', null, 'The pattern: '), `${up} accumulates (HIGH) → ${down} is starved (LOW). The block is the enzyme between them: ${p.steps[c.blockStep].enzyme}.`),
      );
      if (c.teach) teach.append(el('p.arc-teach-text', null, c.teach));
      if (c.pearl) teach.append(el('p.arc-dx-pearl', null, '💊 ', el('strong', null, 'Pearl: '), c.pearl));
      const next = el('button.arc-btn.is-primary', { type: 'button' }, caseIdx + 1 < cases.length && lives > 0 ? 'Next case →' : 'See results →');
      next.addEventListener('click', () => {
        sfx.select();
        if (caseIdx + 1 < cases.length && lives > 0) { caseIdx++; renderCase(); }
        else finish();
      });
      teach.append(next);
      teach.scrollIntoView?.({ block: 'nearest' });
    }

    shell.setStage(wrap);
  }

  function finish(): void {
    const frac = cases.length ? solved / cases.length : 0;
    const efficiency = solved > 0 ? totalTests / solved : 99;
    const medal: Medal = frac >= 0.999 && efficiency <= 5 ? 'gold' : frac >= 0.999 ? 'silver' : frac >= 0.5 ? 'bronze' : 'none';
    shell.showResults({
      recordId: p.id, mode: 'autopsy', won: frac >= 0.5, medal, score,
      headline: frac >= 0.999 ? (efficiency <= 5 ? 'Attending-level diagnosis!' : 'All cases solved') : 'Cases closed',
      lines: [['Solved', `${solved}/${cases.length}`], ['Avg tests/case', solved ? efficiency.toFixed(1) : '—'], ['Lives left', '❤️'.repeat(Math.max(0, lives)) || 'none']],
      funFact: p.funFact,
      replay: () => play(shell, pathways, p),
    });
  }

  renderCase();
}
