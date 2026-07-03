/* =============================================================================
   Metabolism Arcade — the engine
   -----------------------------------------------------------------------------
   Pure vanilla TS. Renders four game modes from the shared Pathway model:
     Build the Pathway · Regulate It · Diagnose It · MCAT Blitz
   State lives in the mountArcade() closure; screens render into a single stage.
   ============================================================================ */
import type { Pathway, Step, QuizItem, Tokens } from '../types';
import { el, clear, shuffle, prefersReducedMotion } from './dom';
import { sfx, isMuted, setMuted, initSound } from './sound';
import * as store from './storage';
import type { Medal, ModeId } from './storage';
import { confettiBurst } from './confetti';
import { quip } from './quips';

type Screen =
  | { name: 'home' }
  | { name: 'modes'; pathway: Pathway }
  | { name: 'play'; pathway: Pathway; mode: ModeId }
  | { name: 'gauntlet' };

const MODES: Array<{ id: ModeId; icon: string; title: string; sub: string }> = [
  { id: 'build', icon: '🧬', title: 'Build the Pathway', sub: 'Order the reactions. Watch the ATP ledger build.' },
  { id: 'regulate', icon: '🎛️', title: 'Regulate It', sub: 'Fed, fasted, sprinting, sleeping, sick — route the flux.' },
  { id: 'diagnose', icon: '🩺', title: 'Diagnose It', sub: 'A patient, some labs. Which enzyme is broken?' },
  { id: 'blitz', icon: '⚡', title: 'MCAT Blitz', sub: 'Timed rapid-fire boss battle. Keep the combo alive.' },
];

const MEDAL_EMOJI: Record<Medal, string> = { none: '', bronze: '🥉', silver: '🥈', gold: '🥇' };

export function mountArcade(root: HTMLElement, pathways: Pathway[]): void {
  initSound();

  const stage = el('div.arc-stage');
  const mascotEl = el('div.arc-mascot', { 'aria-hidden': 'true' });
  const bubbleEl = el('div.arc-bubble', { role: 'status', 'aria-live': 'polite' });

  const hud = buildHud();
  root.append(hud.bar, stage, el('div.arc-mascot-wrap', null, bubbleEl, mascotEl));

  let screen: Screen = { name: 'home' };

  // Keyboard shortcuts: press 1–9 to pick an answer in the single-question modes
  // (Blitz / Gauntlet / Diagnose); Enter advances past a revealed explanation.
  // Multi-question Regulate is intentionally excluded (ambiguous numbering).
  document.addEventListener('keydown', (e) => {
    const t = e.target as HTMLElement | null;
    if (e.metaKey || e.ctrlKey || e.altKey) return;
    if (t && (t.tagName === 'INPUT' || t.tagName === 'TEXTAREA' || t.isContentEditable)) return;
    if (/^[1-9]$/.test(e.key)) {
      const container = stage.querySelector('.arc-blitz-opts') || stage.querySelector('.arc-dx-options');
      if (!container) return;
      const opts = Array.from(container.querySelectorAll<HTMLButtonElement>('.arc-opt'));
      // only act on an unanswered question (nothing disabled yet)
      if (opts.length && opts.every((o) => !o.disabled)) {
        const target = opts[parseInt(e.key, 10) - 1];
        if (target) { e.preventDefault(); target.click(); }
      }
      return;
    }
    if (e.key === 'Enter') {
      if (t && t.tagName === 'BUTTON') return; // let the focused button handle it
      const next = stage.querySelector<HTMLButtonElement>('.arc-teachbox.is-shown .arc-btn.is-primary');
      if (next) { e.preventDefault(); next.click(); }
    }
  });

  function setMascot(text: string, face = '⚡'): void {
    mascotEl.textContent = face;
    bubbleEl.textContent = text;
    bubbleEl.classList.remove('is-pop');
    void bubbleEl.offsetWidth; // restart animation
    if (!prefersReducedMotion()) bubbleEl.classList.add('is-pop');
  }

  // -- HUD -------------------------------------------------------------------
  function buildHud() {
    const back = el('button.arc-back', { type: 'button', 'aria-label': 'Back' }, '‹ Back');
    back.addEventListener('click', () => goBack());
    const crumb = el('div.arc-crumb', null, 'Metabolism Arcade');
    const streak = el('span.arc-stat');
    const atp = el('span.arc-stat');
    const mute = el('button.arc-mute', { type: 'button' });
    const syncMute = () => {
      mute.textContent = isMuted() ? '🔇' : '🔊';
      mute.setAttribute('aria-label', isMuted() ? 'Unmute sound' : 'Mute sound');
    };
    mute.addEventListener('click', () => { setMuted(!isMuted()); syncMute(); if (!isMuted()) sfx.select(); });
    syncMute();
    const stats = el('div.arc-stats', null, streak, atp, mute);
    const bar = el('header.arc-hud', null, back, crumb, stats);
    return { bar, back, crumb, streak, atp, syncStats };
    function syncStats() {
      const s = store.studyStreak();
      streak.textContent = s > 0 ? `🔥 ${s}d` : '🔥 0d';
      streak.title = 'Day study streak';
      atp.textContent = `⚡ ${store.totalAtp().toLocaleString()}`;
      atp.title = 'Lifetime ATP earned';
    }
  }

  function refreshHud(crumbText: string, showBack: boolean): void {
    hud.crumb.textContent = crumbText;
    hud.back.style.visibility = showBack ? 'visible' : 'hidden';
    hud.syncStats();
  }

  function setStage(node: HTMLElement): void {
    clear(stage);
    if (!prefersReducedMotion()) { node.classList.add('arc-in'); }
    stage.append(node);
    // Bring the top of the arcade (its HUD) just below the site's sticky header,
    // so every new screen starts with the Back button and score in view.
    const siteHeader = document.querySelector<HTMLElement>('.site-header');
    const offset = (siteHeader?.offsetHeight ?? 0) + 8;
    const y = root.getBoundingClientRect().top + window.scrollY - offset;
    if (window.scrollY > y + 4 || window.scrollY < y - 200) {
      window.scrollTo({ top: Math.max(0, y), behavior: prefersReducedMotion() ? 'auto' : 'smooth' });
    }
  }

  function goBack(): void {
    sfx.select();
    if (screen.name === 'play') renderModes(screen.pathway);
    else if (screen.name === 'modes' || screen.name === 'gauntlet') renderHome();
  }

  // =========================================================================
  // HOME — pathway cabinets
  // =========================================================================
  function renderHome(): void {
    screen = { name: 'home' };
    refreshHud('Metabolism Arcade', false);
    setMascot(quip('idle'));

    const wrap = el('div.arc-home');
    wrap.append(
      el('p.arc-eyebrow', null, 'Metabolism Arcade'),
      el('h1.arc-title', null, 'Play the pathways. ', el('em', null, 'Actually learn them.')),
      el('p.arc-lede', null,
        'Pick a metabolic pathway and interrogate it four ways — build it step by step, regulate it through a sprint or an all-nighter, diagnose the enzyme that broke, then survive a timed MCAT boss battle. Silly on top. Exam-correct underneath.'),
    );

    const streak = store.studyStreak();
    if (streak > 1) {
      wrap.append(el('p.arc-streakline', null, `🔥 ${streak}-day study streak — keep it lit.`));
    }

    const grid = el('div.arc-cabinets');
    for (const p of pathways) {
      const medal = store.pathwayMedal(p.id);
      const cleared = store.modesCleared(p.id);
      const cab = el('button.arc-cabinet', { type: 'button' });
      cab.append(
        el('span.arc-cab-emoji', { 'aria-hidden': 'true' }, p.emoji),
        el('span.arc-cab-name', null, p.name),
        el('span.arc-cab-tag', null, p.tagline),
        el('span.arc-cab-meta', null,
          el('span.arc-stars', { 'aria-label': `Difficulty ${p.difficulty} of 3` }, '★'.repeat(p.difficulty) + '☆'.repeat(3 - p.difficulty)),
          el('span.arc-cab-cleared', null, `${cleared}/4 modes`),
          medal !== 'none' ? el('span.arc-cab-medal', null, MEDAL_EMOJI[medal]) : el('span'),
        ),
        el('span.arc-cab-play', { 'aria-hidden': 'true' }, 'PLAY ▶'),
      );
      cab.addEventListener('click', () => { sfx.select(); renderModes(p); });
      grid.append(cab);
    }
    // "more coming" ghost cabinet
    grid.append(el('div.arc-cabinet.is-ghost', { 'aria-hidden': 'true' },
      el('span.arc-cab-emoji', null, '🧪'),
      el('span.arc-cab-name', null, 'More coming'),
      el('span.arc-cab-tag', null, 'Urea cycle, ketone bodies, amino-acid catabolism, and the Calvin cycle are next in the queue.'),
    ));
    wrap.append(grid);

    // MCAT Gauntlet — cross-pathway capstone
    const gBest = store.getBest('gauntlet', 'blitz');
    const gauntlet = el('button.arc-gauntlet', { type: 'button' });
    gauntlet.append(
      el('span.arc-gauntlet-ico', { 'aria-hidden': 'true' }, '🎓'),
      el('span.arc-gauntlet-body', null,
        el('span.arc-gauntlet-title', null, 'MCAT Gauntlet'),
        el('span.arc-gauntlet-sub', null, 'One boss battle, questions from every pathway. The cross-pathway thinking the real test rewards.'),
        gBest ? el('span.arc-gauntlet-best', null, `${MEDAL_EMOJI[gBest.medal]} best ${gBest.score.toLocaleString()}`) : el('span'),
      ),
      el('span.arc-gauntlet-go', { 'aria-hidden': 'true' }, 'ENTER ▶'),
    );
    gauntlet.addEventListener('click', () => { sfx.select(); startGauntlet(); });
    wrap.append(gauntlet);

    wrap.append(el('p.arc-hometip', null, 'Tip: every wrong answer explains itself. Getting it wrong here is how you get it right on test day.'));
    setStage(wrap);
  }

  // =========================================================================
  // MODE SELECT
  // =========================================================================
  function renderModes(p: Pathway): void {
    screen = { name: 'modes', pathway: p };
    refreshHud(`${p.emoji} ${p.name}`, true);
    setMascot(`${p.name}. ${p.tagline}`, p.emoji);

    const wrap = el('div.arc-modes');
    const head = el('div.arc-modehead');
    head.append(
      el('span.arc-modehead-emoji', { 'aria-hidden': 'true' }, p.emoji),
      el('div', null,
        el('h2.arc-modehead-name', null, p.name),
        el('p.arc-modehead-blurb', null, p.blurb),
        el('p.arc-modehead-facts', null,
          el('span.arc-chip', null, `📍 ${p.location}`),
          el('span.arc-chip', null, `⚡ ${p.netYield}`),
          p.lessonSlug ? linkChip(`📖 Read the lesson`, `/lessons/${p.lessonSlug}/`) : el('span'),
        ),
      ),
    );
    wrap.append(head);

    const grid = el('div.arc-modegrid');
    for (const m of MODES) {
      const best = store.getBest(p.id, m.id);
      const card = el('button.arc-modecard', { type: 'button' });
      card.append(
        el('span.arc-modecard-ico', { 'aria-hidden': 'true' }, m.icon),
        el('span.arc-modecard-title', null, m.title),
        el('span.arc-modecard-sub', null, m.sub),
        el('span.arc-modecard-best', null,
          best ? `${MEDAL_EMOJI[best.medal]} best ${best.score.toLocaleString()}` : 'not played yet'),
      );
      card.addEventListener('click', () => { sfx.select(); startMode(p, m.id); });
      grid.append(card);
    }
    wrap.append(grid);
    setStage(wrap);
  }

  function startMode(p: Pathway, mode: ModeId): void {
    screen = { name: 'play', pathway: p, mode };
    const label = MODES.find((m) => m.id === mode)!;
    refreshHud(`${p.emoji} ${p.name} · ${label.title}`, true);
    if (mode === 'build') playBuild(p);
    else if (mode === 'regulate') playRegulate(p);
    else if (mode === 'diagnose') playDiagnose(p);
    else playBlitz(p);
  }

  // =========================================================================
  // Shared: results overlay
  // =========================================================================
  interface ResultOpts {
    recordId: string;
    mode: ModeId;
    won: boolean;
    medal: Medal;
    score: number;
    headline: string;
    lines: Array<[string, string]>;
    funFact?: string;
    replay: () => void;
    /** If present, show an "Other modes" button back to this pathway's mode select. */
    modesFor?: Pathway;
  }
  function showResults(o: ResultOpts): void {
    store.recordResult(o.recordId, o.mode, o.score, o.medal, o.score);
    hud.syncStats();
    if (o.medal === 'gold' || o.won) sfx.win(); else sfx.lose();
    setMascot(quip(o.won ? 'win' : 'lose'), o.won ? '🏆' : '⚡');

    const card = el('div.arc-results.card');
    card.append(
      el('div.arc-results-medal', { 'aria-hidden': 'true' }, o.medal !== 'none' ? MEDAL_EMOJI[o.medal] : (o.won ? '🎉' : '🧬')),
      el('h2.arc-results-head', null, o.headline),
      el('p.arc-results-medaltext', null,
        o.medal !== 'none' ? `${o.medal.toUpperCase()} MEDAL` : (o.won ? 'Cleared' : 'Give it another run')),
    );
    const stats = el('dl.arc-results-stats');
    for (const [k, v] of o.lines) stats.append(el('dt', null, k), el('dd', null, v));
    stats.append(el('dt', null, 'ATP banked'), el('dd', null, `⚡ ${o.score.toLocaleString()}`));
    card.append(stats);

    if (o.funFact) {
      card.append(el('p.arc-results-fact', null, el('strong', null, 'Did you know — '), o.funFact));
    }

    const actions = el('div.arc-results-actions');
    const again = el('button.arc-btn.is-primary', { type: 'button' }, '↻ Play again');
    again.addEventListener('click', () => { sfx.select(); o.replay(); });
    if (o.modesFor) {
      const modesBtn = el('button.arc-btn', { type: 'button' }, '◧ Other modes');
      const forPath = o.modesFor;
      modesBtn.addEventListener('click', () => { sfx.select(); renderModes(forPath); });
      actions.append(again, modesBtn);
    } else {
      actions.append(again);
    }
    const homeBtn = el('button.arc-btn', { type: 'button' }, '⌂ Pathways');
    homeBtn.addEventListener('click', () => { sfx.select(); renderHome(); });
    actions.append(homeBtn);
    card.append(actions);

    const overlay = el('div.arc-overlay');
    overlay.append(card);
    setStage(overlay);
    if (o.medal === 'gold') confettiBurst(card);
  }

  // =========================================================================
  // MODE 1 — BUILD THE PATHWAY (assembly line)
  // =========================================================================
  function playBuild(p: Pathway): void {
    setMascot(quip('placeStart'), '🧬');
    const steps = p.steps;
    const N = steps.length;
    let placed = 0;
    let mistakes = 0;
    let streak = 0;
    let locked = false;
    const start = Date.now();

    const wrap = el('div.arc-build');
    wrap.append(el('p.arc-mode-instr', null,
      'Which reaction comes ', el('strong', null, 'next'), '? Tap the tile you think follows. Correct tiles snap onto the line and the ledger updates.'));

    // Ledger
    const ledger = el('div.arc-ledger');
    const ledgerATP = el('span.arc-ledger-val');
    const ledgerNADH = el('span.arc-ledger-val');
    const otherLedger = el('span.arc-ledger-val');
    ledger.append(
      el('span.arc-ledger-lbl', null, 'Running ledger:'),
      el('span.arc-ledger-item', null, '⚡ ATP ', ledgerATP),
      el('span.arc-ledger-item', null, '🔋 NADH ', ledgerNADH),
      otherLedger,
    );

    // The track of slots
    const track = el('div.arc-track');
    const slots: HTMLElement[] = [];
    const startSlot = el('div.arc-slot.is-start.is-filled');
    startSlot.append(el('span.arc-slot-emoji', null, p.startEmoji ?? '🟢'), el('span.arc-slot-name', null, p.startShort));
    track.append(startSlot);
    for (let i = 0; i < N; i++) {
      const slot = el('div.arc-slot', { 'data-i': i });
      slot.append(el('span.arc-slot-num', null, String(i + 1)));
      slots.push(slot);
      track.append(el('span.arc-arrow', { 'aria-hidden': 'true' }, '→'), slot);
    }

    // Fact bubble
    const factBox = el('div.arc-factbox', { role: 'status', 'aria-live': 'polite' });

    // Tray of shuffled tiles
    const tray = el('div.arc-tray');
    const tiles: HTMLElement[] = [];
    for (const s of shuffle(steps)) {
      const tile = el('button.arc-tile', { type: 'button', 'data-n': s.n });
      tile.append(
        el('span.arc-tile-emoji', { 'aria-hidden': 'true' }, s.emoji ?? '⚗️'),
        el('span.arc-tile-prod', null, s.short),
        el('span.arc-tile-enz', null, s.enzyme),
        s.committed ? el('span.arc-tile-flag.is-committed', null, 'committed') :
          s.irreversible ? el('span.arc-tile-flag', null, 'irreversible') : el('span'),
      );
      tile.addEventListener('click', () => attempt(s, tile));
      tiles.push(tile);
      tray.append(tile);
    }

    const hintBtn = el('button.arc-btn.arc-hint', { type: 'button' }, '💡 Hint');
    hintBtn.addEventListener('click', () => {
      if (locked || placed >= N) return;
      const next = steps[placed];
      setFact(`Hint: you need the product of ${next.enzyme}.`, 'hint');
    });

    function updateLedger(): void {
      const t = ledgerAfter(p, placed);
      ledgerATP.textContent = fmt(t.atp);
      ledgerNADH.textContent = fmt(t.nadh);
      const extras: string[] = [];
      if (t.fadh2) extras.push(`FADH₂ ${fmt(t.fadh2)}`);
      if (t.nadph) extras.push(`NADPH ${fmt(t.nadph)}`);
      if (t.gtp) extras.push(`GTP ${fmt(t.gtp)}`);
      if (t.co2) extras.push(`CO₂ ${fmt(t.co2)}`);
      otherLedger.textContent = extras.length ? '· ' + extras.join(' · ') : '';
    }

    function setFact(text: string, kind: 'ok' | 'bad' | 'hint'): void {
      clear(factBox);
      factBox.className = `arc-factbox is-${kind}`;
      factBox.append(el('span', null, text));
    }

    function attempt(s: Step, tile: HTMLElement): void {
      if (locked || placed >= N) return;
      const next = steps[placed];
      if (s.n === next.n) {
        // correct
        locked = true;
        streak++;
        sfx.correct();
        const slot = slots[placed];
        slot.classList.add('is-filled', 'just-placed');
        clear(slot);
        slot.append(el('span.arc-slot-emoji', null, s.emoji ?? '⚗️'), el('span.arc-slot-name', null, s.short));
        tile.classList.add('is-used');
        (tile as HTMLButtonElement).disabled = true;
        placed++;
        updateLedger();
        flyTokens(s, slot);
        setFact(`✓ ${s.enzyme}: ${s.fact}`, 'ok');
        if (streak >= 3 && streak % 3 === 0) { sfx.streak(); setMascot(quip('streak'), '🔥'); }
        else setMascot(quip('correct'), '🧬');
        window.setTimeout(() => {
          locked = false;
          if (placed >= N) finish();
        }, 260);
      } else {
        // wrong
        mistakes++;
        streak = 0;
        sfx.wrong();
        tile.classList.remove('arc-shake'); void tile.offsetWidth; tile.classList.add('arc-shake');
        setFact(`✗ Not next. ${hintText(steps[placed])}`, 'bad');
        setMascot(quip('wrong'), '😵');
      }
    }

    function finish(): void {
      const secs = Math.round((Date.now() - start) / 1000);
      const speedBonus = Math.max(0, 300 - secs * 4);
      const score = Math.max(0, N * 100 - mistakes * 35 + speedBonus);
      const medal: Medal = mistakes === 0 ? 'gold' : mistakes <= 2 ? 'silver' : 'bronze';
      const t = ledgerAfter(p, N);
      showResults({
        recordId: p.id, funFact: p.funFact, modesFor: p, mode: 'build', won: true, medal, score,
        headline: mistakes === 0 ? 'Flawless assembly!' : 'Pathway complete!',
        lines: [
          ['Time', `${secs}s`],
          ['Mistakes', String(mistakes)],
          ['Final ledger', `⚡ ${fmt(t.atp)} ATP · 🔋 ${fmt(t.nadh)} NADH`],
        ],
        replay: () => playBuild(p),
      });
    }

    wrap.append(ledger, track, factBox, el('p.arc-tray-lbl', null, 'Reaction tiles'), tray, hintBtn);
    updateLedger();
    setStage(wrap);
  }

  function flyTokens(s: Step, target: HTMLElement): void {
    if (prefersReducedMotion() || !s.tokens) return;
    const specs: Array<[string, number]> = [];
    if (s.tokens.atp) specs.push(['⚡', s.tokens.atp]);
    if (s.tokens.nadh) specs.push(['🔋', s.tokens.nadh]);
    if (s.tokens.fadh2) specs.push(['🔋', s.tokens.fadh2]);
    if (s.tokens.co2) specs.push(['💨', s.tokens.co2]);
    const rect = target.getBoundingClientRect();
    let k = 0;
    for (const [emoji, n] of specs) {
      const sign = n > 0 ? 'plus' : 'minus';
      const tok = el(`span.arc-token.is-${sign}`, null, `${n > 0 ? '+' : '−'}${emoji}`);
      tok.style.left = `${rect.left + rect.width / 2}px`;
      tok.style.top = `${rect.top}px`;
      tok.style.animationDelay = `${k * 90}ms`;
      document.body.append(tok);
      window.setTimeout(() => tok.remove(), 1100 + k * 90);
      k++;
    }
  }

  // =========================================================================
  // MODE 2 — REGULATE IT (mission control)
  // =========================================================================
  function playRegulate(p: Pathway): void {
    const scenarios = shuffle(p.scenarios);
    let idx = 0;
    let correct = 0;
    let total = 0;
    for (const s of scenarios) total += s.decisions.length;
    let health = 100;

    function renderScenario(): void {
      const sc = scenarios[idx];
      setMascot(`Scenario ${idx + 1} of ${scenarios.length}. Read the body, then route the flux.`, sc.emoji);
      const wrap = el('div.arc-regulate');

      // health + progress
      const hp = el('div.arc-hpbar', { 'aria-label': `Cell health ${health}%` });
      const hpfill = el('div.arc-hpfill');
      hpfill.style.width = `${health}%`;
      hpfill.style.background = health > 60 ? 'var(--ddp-color-accent)' : health > 30 ? 'var(--ddp-color-secondary)' : '#c0392b';
      hp.append(hpfill);
      wrap.append(
        el('div.arc-reg-top', null,
          el('span.arc-reg-progress', null, `Scenario ${idx + 1}/${scenarios.length}`),
          el('span.arc-reg-hplabel', null, '❤️ Cell health'), hp),
      );

      // scenario card
      const scene = el('div.arc-scene.card');
      scene.append(
        el('div.arc-scene-emoji', { 'aria-hidden': 'true' }, sc.emoji),
        el('div', null,
          el('h3.arc-scene-title', null, sc.title),
          el('p.arc-scene-text', null, sc.scene),
          sc.hormones ? el('p.arc-scene-hormones', null, sc.hormones) : el('span'),
        ),
      );
      wrap.append(scene);

      const decWrap = el('div.arc-decisions');
      const teachBox = el('div.arc-teachbox');
      let answeredCount = 0;
      const answered = new Array<boolean>(sc.decisions.length).fill(false);

      sc.decisions.forEach((d, di) => {
        const view = shuffledChoices(d.choices, d.answer);
        const block = el('div.arc-decision');
        block.append(el('p.arc-decision-q', null, `${di + 1}. ${d.q}`));
        const opts = el('div.arc-options');
        const why = el('p.arc-why');
        view.choices.forEach((c, ci) => {
          const b = el('button.arc-opt', { type: 'button' }, c);
          b.addEventListener('click', () => {
            if (answered[di]) return;
            answered[di] = true;
            answeredCount++;
            const right = ci === view.answer;
            if (right) correct++;
            else health = Math.max(0, health - Math.ceil(100 / total));
            hpfill.style.width = `${health}%`;
            hpfill.style.background = health > 60 ? 'var(--ddp-color-accent)' : health > 30 ? 'var(--ddp-color-secondary)' : '#c0392b';
            Array.from(opts.children).forEach((child, k) => {
              const btn = child as HTMLButtonElement;
              btn.disabled = true;
              if (k === view.answer) btn.classList.add('is-correct');
              else if (k === ci) btn.classList.add('is-wrong');
            });
            why.className = `arc-why is-shown ${right ? 'is-ok' : 'is-bad'}`;
            why.textContent = `${right ? '✓ ' : '✗ '}${d.why}`;
            if (right) { sfx.correct(); setMascot(quip('correct'), sc.emoji); }
            else { sfx.wrong(); setMascot(quip('wrong'), '😵'); }
            if (answeredCount === sc.decisions.length) revealTeach();
          });
          opts.append(b);
        });
        block.append(opts, why);
        decWrap.append(block);
      });

      function revealTeach(): void {
        const dir = sc.flux === 'up' ? '⬆️ RAMPED UP' : sc.flux === 'down' ? '⬇️ THROTTLED DOWN' : '⏹️ ESSENTIALLY OFF';
        teachBox.className = 'arc-teachbox is-shown card';
        teachBox.append(
          el('p.arc-teach-flux', null, `In this state, ${p.name} is `, el('strong', null, dir), '.'),
          el('p.arc-teach-text', null, sc.teach),
        );
        const nextBtn = el('button.arc-btn.is-primary', { type: 'button' },
          idx + 1 < scenarios.length ? 'Next scenario →' : 'See results →');
        nextBtn.addEventListener('click', () => {
          sfx.select();
          idx++;
          if (idx < scenarios.length) renderScenario();
          else finish();
        });
        teachBox.append(nextBtn);
        teachBox.scrollIntoView?.({ behavior: prefersReducedMotion() ? 'auto' : 'smooth', block: 'nearest' });
      }

      wrap.append(decWrap, teachBox);
      setStage(wrap);
    }

    function finish(): void {
      const frac = total > 0 ? correct / total : 0;
      const score = correct * 100 + (health >= 100 ? 150 : 0);
      const medal: Medal = frac >= 0.999 ? 'gold' : frac >= 0.8 ? 'silver' : frac >= 0.5 ? 'bronze' : 'none';
      showResults({
        recordId: p.id, funFact: p.funFact, modesFor: p, mode: 'regulate', won: frac >= 0.5, medal, score,
        headline: frac >= 0.999 ? 'Perfect metabolic control!' : health <= 0 ? 'The cell flatlined…' : 'Homeostasis (mostly) held',
        lines: [
          ['Correct decisions', `${correct}/${total}`],
          ['Cell health left', `${health}%`],
          ['Scenarios', String(scenarios.length)],
        ],
        replay: () => playRegulate(p),
      });
    }

    renderScenario();
  }

  // =========================================================================
  // MODE 3 — DIAGNOSE IT (enzyme detective)
  // =========================================================================
  function playDiagnose(p: Pathway): void {
    const cases = shuffle(p.diseases);
    let idx = 0;
    let correct = 0;
    let streak = 0;

    function renderCase(): void {
      const c = cases[idx];
      setMascot(`Case ${idx + 1} of ${cases.length}. Read the chart. Name the broken enzyme.`, '🩺');
      const wrap = el('div.arc-diagnose');
      wrap.append(el('div.arc-dx-top', null,
        el('span.arc-reg-progress', null, `Case ${idx + 1}/${cases.length}`),
        streak > 1 ? el('span.arc-dx-streak', null, `🔥 ${streak} in a row`) : el('span')));

      const chart = el('div.arc-chart.card');
      chart.append(
        el('div.arc-chart-emoji', { 'aria-hidden': 'true' }, c.emoji ?? '🧑‍⚕️'),
        el('div', null,
          el('p.arc-chart-label', null, 'PATIENT CHART'),
          el('p.arc-chart-vignette', null, c.vignette)),
      );
      wrap.append(chart);
      wrap.append(el('p.arc-dx-prompt', null, 'Which enzyme is deficient?'));

      const opts = el('div.arc-dx-options');
      const teach = el('div.arc-teachbox');
      // shuffle suspects but track the correct label
      const correctLabel = c.suspects[c.answer];
      const order = shuffle(c.suspects);
      let answered = false;
      order.forEach((label) => {
        const b = el('button.arc-opt.arc-dx-opt', { type: 'button' }, label);
        b.addEventListener('click', () => {
          if (answered) return;
          answered = true;
          const right = label === correctLabel;
          Array.from(opts.children).forEach((child) => {
            const btn = child as HTMLButtonElement;
            btn.disabled = true;
            if (btn.textContent === correctLabel) btn.classList.add('is-correct');
            else if (btn === b) btn.classList.add('is-wrong');
          });
          if (right) { correct++; streak++; sfx.correct(); setMascot(quip('correct'), '🩺'); }
          else { streak = 0; sfx.wrong(); setMascot(quip('wrong'), '😵'); }
          revealTeach(right);
        });
        opts.append(b);
      });
      wrap.append(opts, teach);

      function revealTeach(right: boolean): void {
        teach.className = 'arc-teachbox is-shown card';
        teach.append(el('p.arc-dx-verdict', null, right ? '✓ Correct diagnosis.' : `✗ It was ${correctLabel}.`));
        if (c.accumulates) teach.append(el('p.arc-dx-line', null, el('strong', null, 'Backs up: '), c.accumulates));
        if (c.missing) teach.append(el('p.arc-dx-line', null, el('strong', null, 'Missing: '), c.missing));
        teach.append(el('p.arc-teach-text', null, c.teach));
        if (c.pearl) teach.append(el('p.arc-dx-pearl', null, '💊 ', el('strong', null, 'Pearl: '), c.pearl));
        const nextBtn = el('button.arc-btn.is-primary', { type: 'button' },
          idx + 1 < cases.length ? 'Next case →' : 'See results →');
        nextBtn.addEventListener('click', () => {
          sfx.select(); idx++;
          if (idx < cases.length) renderCase(); else finish();
        });
        teach.append(nextBtn);
        teach.scrollIntoView?.({ behavior: prefersReducedMotion() ? 'auto' : 'smooth', block: 'nearest' });
      }
      setStage(wrap);
    }

    function finish(): void {
      const frac = cases.length ? correct / cases.length : 0;
      const score = correct * 130;
      const medal: Medal = frac >= 0.999 ? 'gold' : frac >= 0.75 ? 'silver' : frac >= 0.5 ? 'bronze' : 'none';
      showResults({
        recordId: p.id, funFact: p.funFact, modesFor: p, mode: 'diagnose', won: frac >= 0.5, medal, score,
        headline: frac >= 0.999 ? 'Attending-level diagnosis!' : 'Cases closed',
        lines: [['Correct diagnoses', `${correct}/${cases.length}`]],
        replay: () => playDiagnose(p),
      });
    }
    renderCase();
  }

  // =========================================================================
  // MODE 4 — MCAT BLITZ (boss battle)
  // =========================================================================
  function playBlitz(p: Pathway): void {
    bossBattle({
      bank: buildBlitzBank(p),
      bossName: 'The Final Exam',
      bossFace: '👹',
      recordId: p.id,
      funFact: p.funFact,
      modesFor: p,
      replay: () => playBlitz(p),
    });
  }

  interface BossCfg {
    bank: QuizItem[];
    bossName: string;
    bossFace: string;
    recordId: string;
    funFact?: string;
    replay: () => void;
    modesFor?: Pathway;
  }
  function bossBattle(cfg: BossCfg): void {
    const bank = cfg.bank;
    const total = bank.length;
    let idx = 0;
    let hearts = 3;
    let combo = 0;
    let maxCombo = 0;
    let score = 0;
    let correct = 0;
    const PER_Q = 22; // seconds
    let timeLeft = PER_Q;
    let timer: number | null = null;

    function stopTimer(): void { if (timer != null) { clearInterval(timer); timer = null; } }

    function renderQ(): void {
      const q = bank[idx];
      const view = shuffledChoices(q.choices, q.answer);
      setMascot(combo >= 3 ? `🔥 ${combo}x combo — ${cfg.bossName} is sweating!` : 'Boss battle! Answer fast, keep the combo.', cfg.bossFace);
      timeLeft = PER_Q;
      const wrap = el('div.arc-blitz');

      // boss + hearts + combo
      const bossHpPct = (1 - correct / total) * 100;
      const bossbar = el('div.arc-bosshp');
      const bossfill = el('div.arc-bosshp-fill');
      bossfill.style.width = `${bossHpPct}%`;
      bossbar.append(bossfill);
      wrap.append(el('div.arc-blitz-top', null,
        el('div.arc-boss', null, el('span.arc-boss-face', { 'aria-hidden': 'true' }, cfg.bossFace),
          el('div.arc-boss-meta', null, el('span.arc-boss-name', null, cfg.bossName), bossbar)),
        el('div.arc-blitz-status', null,
          el('span.arc-hearts', { 'aria-label': `${hearts} lives` }, '❤️'.repeat(hearts) + '🖤'.repeat(3 - hearts)),
          el('span.arc-combo', null, combo >= 2 ? `⚡ ${combo}x` : ''),
        ),
      ));

      // timer
      const timeWrap = el('div.arc-timerbar');
      const timeFill = el('div.arc-timerfill');
      timeWrap.append(timeFill);
      wrap.append(timeWrap);

      // question
      wrap.append(el('p.arc-blitz-count', null, `Q${idx + 1} of ${total}`, q.tag ? el('span.arc-qtag', null, q.tag) : el('span')));
      wrap.append(el('p.arc-blitz-stem', null, q.stem));
      const opts = el('div.arc-options.arc-blitz-opts');
      const why = el('div.arc-teachbox');
      let answered = false;

      view.choices.forEach((c, ci) => {
        const b = el('button.arc-opt.arc-opt-keyed', { type: 'button' },
          el('span.arc-optnum', { 'aria-hidden': 'true' }, String(ci + 1)),
          el('span.arc-opttext', null, c));
        b.addEventListener('click', () => answer(ci, b));
        opts.append(b);
      });
      const hint = el('p.arc-kbdhint', null);
      hint.innerHTML = 'Tap an answer — or press <kbd>1</kbd>–<kbd>4</kbd>, then <kbd>Enter</kbd> to continue.';
      wrap.append(opts, hint, why);

      function answer(ci: number | null, btn: HTMLElement | null): void {
        if (answered) return;
        answered = true;
        stopTimer();
        const right = ci === view.answer;
        Array.from(opts.children).forEach((child, k) => {
          const b = child as HTMLButtonElement;
          b.disabled = true;
          if (k === view.answer) b.classList.add('is-correct');
          else if (btn && b === btn) b.classList.add('is-wrong');
        });
        if (right) {
          correct++; combo++; maxCombo = Math.max(maxCombo, combo);
          const timeBonus = Math.round(timeLeft * 5);
          score += 100 * Math.min(combo, 5) + timeBonus;
          sfx.correct();
          if (combo >= 3) { sfx.streak(); setMascot(quip('streak'), '🔥'); } else setMascot(quip('correct'), '⚡');
          bossfill.style.width = `${(1 - correct / total) * 100}%`;
        } else {
          combo = 0; hearts--;
          sfx.wrong();
          setMascot(ci == null ? 'Time! The boss got a hit in.' : quip('wrong'), '😵');
        }
        why.className = `arc-teachbox is-shown card ${right ? 'is-ok' : 'is-bad'}`;
        why.append(el('p.arc-why-head', null, right ? '✓ Correct' : (ci == null ? '⏱️ Out of time' : '✗ Not quite')),
          el('p.arc-teach-text', null, q.rationale));
        const done = hearts <= 0 || idx + 1 >= total;
        const nextBtn = el('button.arc-btn.is-primary', { type: 'button' },
          hearts <= 0 ? 'See results →' : idx + 1 >= total ? 'Finish the boss →' : 'Next →');
        nextBtn.addEventListener('click', () => {
          sfx.select();
          if (done) finish();
          else { idx++; renderQ(); }
        });
        why.append(nextBtn);
        why.scrollIntoView?.({ behavior: prefersReducedMotion() ? 'auto' : 'smooth', block: 'nearest' });
      }

      setStage(wrap);

      // start timer
      const startT = Date.now();
      timeFill.style.width = '100%';
      timer = window.setInterval(() => {
        const elapsed = (Date.now() - startT) / 1000;
        timeLeft = Math.max(0, PER_Q - elapsed);
        timeFill.style.width = `${(timeLeft / PER_Q) * 100}%`;
        timeFill.style.background = timeLeft < 6 ? '#c0392b' : timeLeft < 12 ? 'var(--ddp-color-secondary)' : 'var(--ddp-color-accent)';
        if (timeLeft <= 5 && Math.ceil(timeLeft) !== Math.ceil(timeLeft + 0.1)) sfx.tick();
        if (timeLeft <= 0) answer(null, null);
      }, 100);
    }

    function finish(): void {
      stopTimer();
      const won = correct >= total; // boss defeated = cleared the whole bank
      const survived = hearts > 0;
      const medal: Medal = won && hearts === 3 ? 'gold' : won ? 'silver' : correct >= Math.ceil(total * 0.6) ? 'bronze' : 'none';
      score += survived && won ? 200 : 0;
      showResults({
        recordId: cfg.recordId, funFact: cfg.funFact, modesFor: cfg.modesFor,
        mode: 'blitz', won: won,
        medal, score,
        headline: won && hearts === 3 ? 'FLAWLESS VICTORY!' : won ? `${cfg.bossName} defeated!` : hearts <= 0 ? `${cfg.bossName} won… this time` : 'Time up',
        lines: [
          ['Correct', `${correct}/${total}`],
          ['Best combo', `${maxCombo}x`],
          ['Lives left', '❤️'.repeat(Math.max(0, hearts)) || 'none'],
        ],
        replay: cfg.replay,
      });
    }

    renderQ();
  }

  // =========================================================================
  // MCAT GAUNTLET — a cross-pathway boss battle (the capstone cram tool)
  // =========================================================================
  function startGauntlet(): void {
    screen = { name: 'gauntlet' };
    refreshHud('🎓 MCAT Gauntlet', true);
    bossBattle({
      bank: buildGauntletBank(pathways),
      bossName: 'The MCAT',
      bossFace: '🎓',
      recordId: 'gauntlet',
      funFact:
        'The real MCAT never tests one pathway in isolation — it hands you a patient, a lab value, or a marathon and asks how the whole network responds. That’s the muscle this gauntlet builds.',
      replay: startGauntlet,
    });
  }

  // start
  renderHome();
}

// =========================================================================
// Pure helpers
// =========================================================================

/** Cumulative token ledger for the first `count` steps, applying doubleAfter. */
function ledgerAfter(p: Pathway, count: number): Required<Tokens> {
  const acc: Required<Tokens> = { atp: 0, nadh: 0, fadh2: 0, nadph: 0, gtp: 0, co2: 0 };
  for (let i = 0; i < count && i < p.steps.length; i++) {
    const s = p.steps[i];
    if (!s.tokens) continue;
    const mult = p.doubleAfter > 0 && s.n > p.doubleAfter ? 2 : 1;
    acc.atp += (s.tokens.atp ?? 0) * mult;
    acc.nadh += (s.tokens.nadh ?? 0) * mult;
    acc.fadh2 += (s.tokens.fadh2 ?? 0) * mult;
    acc.nadph += (s.tokens.nadph ?? 0) * mult;
    acc.gtp += (s.tokens.gtp ?? 0) * mult;
    acc.co2 += (s.tokens.co2 ?? 0) * mult;
  }
  return acc;
}

function fmt(n: number): string {
  return n > 0 ? `+${n}` : String(n);
}

/** Shuffle a question's choices so the correct answer isn't always in the same
 *  slot (every item is authored with answer:0 for readability). */
function shuffledChoices(choices: string[], answer: number): { choices: string[]; answer: number } {
  const order = shuffle(choices.map((_, i) => i));
  return { choices: order.map((i) => choices[i]), answer: order.indexOf(answer) };
}

function hintText(step: Step): string {
  return `Look for the product of ${step.enzyme}.`;
}

function linkChip(label: string, href: string): HTMLElement {
  const a = el('a.arc-chip.arc-chip-link', { href }) as HTMLAnchorElement;
  a.textContent = label;
  return a;
}

/** Build the cross-pathway MCAT Gauntlet bank: a couple of items from every
 *  pathway, each tagged with its pathway name so students see where it came
 *  from, then shuffled and capped at a boss-length 15. */
function buildGauntletBank(pathways: Pathway[]): QuizItem[] {
  const pool: QuizItem[] = [];
  for (const p of pathways) {
    for (const q of shuffle(p.quiz).slice(0, 2)) {
      pool.push({ ...q, stem: `[${p.name}] ${q.stem}` });
    }
  }
  return shuffle(pool).slice(0, 15);
}

/** Build the blitz bank: the pathway's quiz plus a couple auto-generated items
 *  from its diseases and scenarios, capped and shuffled. */
function buildBlitzBank(p: Pathway): QuizItem[] {
  const bank: QuizItem[] = [...p.quiz];
  // one disease item
  const d = p.diseases[0];
  if (d) {
    bank.push({
      tag: 'disease',
      stem: `${d.vignette} Which enzyme is deficient?`,
      choices: d.suspects,
      answer: d.answer,
      rationale: d.teach,
    });
  }
  return shuffle(bank).slice(0, Math.min(bank.length, 10));
}
