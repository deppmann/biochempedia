/* The theater in the browser (2026-11-20): makes a /watch/ page follow its film.

   Everything it shows is already in the page's HTML (src/pages/watch/[...path].astro); this only
   chooses what is in view for the second the film is at. Rules it keeps:
     - nothing plays until the viewer presses play, or taps a part or a sentence (which is a press);
     - while the film waits on its own question, only the question is up;
     - a word comes up when the film says it, a figure when its part starts, never earlier;
     - the panel is never swapped out from under a link someone is on, and a control is never
       removed while it has focus (focus is moved to the companion first);
     - nothing below the companion moves when the companion changes height: a reader parked on the
       list of parts or the transcript stays where they are;
     - part changes are not announced aloud (they would talk over the narration): the list of parts
       carries aria-current instead. One sentence is announced, when the film ends;
     - nothing is stored. The watched record is trackFilms() in BaseLayout.

   Reviewer hooks: ?t=<seconds> puts the page in the state it has at that second (the film itself is
   left alone);
   ?state=end shows the end of the film. ?film=<key>&at=<seconds> is the site's resume link
   (resumeFromLink in film-progress.ts does the seek; this adds "Press play to start at m:ss."). */

import { companionAt, pauseLabel, swapRule } from './film-logic.mjs';

const clock = (sec: number) => `${Math.floor(sec / 60)}:${String(Math.floor(sec % 60)).padStart(2, '0')}`;

export function theater(): void {
  const root = document.querySelector<HTMLElement>('[data-th]');
  const v = root?.querySelector<HTMLVideoElement>('video');
  if (!root || !v) return;
  const $$ = <T extends HTMLElement>(sel: string) => [...root.querySelectorAll<T>(sel)];
  const $ = <T extends HTMLElement>(sel: string) => root.querySelector<T>(sel);
  const num = (el: HTMLElement, k: string) => Number(el.dataset[k]);
  const params = new URLSearchParams(location.search);
  const duration = Number(root.dataset.duration) || 0;
  const lastReveal = Number(root.dataset.lastReveal) || 0;

  const companion = $('[data-th-companion]')!;
  const screen = $('[data-th-screen]')!;
  const panels = $$('[data-th-panel]');
  const rows = $$<HTMLButtonElement>('[data-th-go]');
  const questions = $$('[data-th-question]');
  const rest = $('[data-th-rest]');
  const figs = $<HTMLDetailsElement>('[data-th-figs]');
  const terms = $$('[data-at]');
  const lines = $$('[data-th-lines] > li');
  const segs = $$('.th-seg');
  const bar = $('[data-th-bar]');
  const next = $('[data-th-next]')!;
  const status = $('[data-th-status]')!;
  const transcript = $<HTMLDetailsElement>('[data-th-transcript]');

  root.classList.add('th-live', 'th-ready');
  // The site's header stays at the top of the window; the pinned screen sits under it.
  const header = document.querySelector<HTMLElement>('.site-header');
  if (header && getComputedStyle(header).position === 'sticky') root.style.setProperty('--th-top', `${header.offsetHeight}px`);
  let ended = params.get('state') === 'end';
  next.hidden = !ended;
  // A figure of the lesson may show what the film is about to ask, so the fold waits for the film's
  // last answer. (With scripts off it is a closed fold the viewer opens by choice.)
  if (figs && lastReveal > 0) figs.hidden = true;

  /* ---- going to a second: a tap on a part, a segment or a sentence is the viewer's press. */
  const playFrom = (t: number) => {
    const go = () => { try { v.currentTime = t; } catch { /* not seekable yet */ } void v.play().catch(() => {}); };
    if (v.readyState >= 1) go();
    else { v.addEventListener('loadedmetadata', go, { once: true }); v.preload = 'metadata'; v.load(); }
    sync(t);
  };

  /* ---- the companion. What should show at a second, and whether it may change under the current
     focus, are decided in film-logic.mjs (tested in scripts/test-film-logic.mjs). */
  const partTimes = panels.map((p) => ({ start: num(p, 't') }));
  const askTimes = questions.map((q) => ({ start: num(q, 't'), until: num(q, 'until') }));
  companion.tabIndex = -1;
  const focusKind = (within: HTMLElement): 'none' | 'link' | 'pause' => {
    const el = document.activeElement as HTMLElement | null;
    if (!el || !within.contains(el) || el === companion) return 'none';
    if (el.matches('[data-th-pause]')) return 'pause';
    // Held for someone moving through the page by keyboard. A link clicked with a mouse (opened in a
    // new tab, say) keeps focus too, and must not freeze the companion for the rest of the film.
    return el.matches(':focus-visible') ? 'link' : 'none';
  };
  /* A change of the companion's height must not move what is below it when the reader is below it:
     measure the first thing after the companion before and after, and take the difference out of
     the scroll position at once. */
  const below = $('[data-th-list], .th-take, [data-th-transcript], [data-hop-area]');
  const steady = (change: () => void) => {
    // "Below it" means the companion's top is off the top of what can be seen (above the pinned screen,
    // or the site's header): then what follows the companion is what the reader is looking at.
    const pinned = getComputedStyle(screen).position === 'sticky';
    const edge = pinned ? screen.getBoundingClientRect().bottom : header && getComputedStyle(header).position === 'sticky' ? header.getBoundingClientRect().bottom : 0;
    const parked = !!below && companion.getBoundingClientRect().top < edge;
    const before = parked ? below!.getBoundingClientRect().top : 0;
    change();
    if (parked) {
      const moved = below!.getBoundingClientRect().top - before;
      if (moved) window.scrollBy({ top: moved, behavior: 'instant' as ScrollBehavior });
    }
  };

  let part = -1;
  let wanted = -1;
  let asked = -2;
  const draw = (i: number, asking: number) => {
    // The list of parts always says where the film is, even while the panel is being held.
    if (i !== wanted) rows.forEach((r, k) => { if (k === i) r.setAttribute('aria-current', 'true'); else r.removeAttribute('aria-current'); });
    wanted = i;
    if (panels.length && i !== part) {
      const rule = part === -1 ? { change: true, moveFocus: false } : swapRule(focusKind(panels[part]));
      if (rule.change) {
        if (rule.moveFocus) companion.focus({ preventScroll: true });
        steady(() => { part = i; panels.forEach((p, k) => p.classList.toggle('is-now', k === i)); });
      }
    }
    if (questions.length && asking !== asked) {
      // The question leaving: never from under its own focused button, and never the lesson link
      // from under someone who is on it.
      // A question arriving always shows, with its pause button; only the lesson link is kept back
      // from hiding while someone is on it.
      const leaving = asked >= 0 ? questions[asked] : null;
      const rule = swapRule(leaving ? focusKind(leaving) : 'none');
      if (rule.change) {
        if (rule.moveFocus) companion.focus({ preventScroll: true });
        steady(() => {
          questions.forEach((q, k) => { q.hidden = k !== asking; });
          if (rest) rest.hidden = asking !== -1 && focusKind(rest) !== 'link';
        });
        asked = asking;
      }
    } else if (rest && asking !== -1 && !rest.hidden && focusKind(rest) !== 'link') {
      steady(() => { rest.hidden = true; });
    }
  };
  companion.addEventListener('focusout', () => {
    requestAnimationFrame(() => { if (!companion.contains(document.activeElement) || document.activeElement === companion) sync(v.ended ? duration : v.currentTime || lastT); });
  });

  let line = -1;
  let lastT = 0;
  function sync(t: number): void {
    lastT = t;
    const now = companionAt(t, partTimes, askTimes, ended);
    draw(now.part, now.asking);
    for (const el of terms) el.hidden = t + 0.05 < num(el, 'at');
    if (figs && figs.hidden && (ended || (lastReveal > 0 && t >= lastReveal))) steady(() => { figs.hidden = false; });
    // The parts bar: which segment the film is in, and how far along.
    if (bar) {
      bar.style.setProperty('--th-p', `${duration ? Math.min(100, (t / duration) * 100) : 0}%`);
      let s = 0;
      segs.forEach((b, k) => { if (num(b, 't') <= t + 0.05) s = k; });
      segs.forEach((b, k) => b.classList.toggle('is-now', k === s));
    }
    // The transcript keeps its place; it scrolls inside its own box, never the page.
    let l = -1;
    lines.forEach((li, k) => { if (num(li, 't') <= t + 0.05) l = k; });
    if (l !== line) {
      lines[line]?.classList.remove('is-now');
      lines[line]?.removeAttribute('aria-current');
      line = l;
      const li = lines[l];
      if (li) {
        li.classList.add('is-now');
        li.setAttribute('aria-current', 'true');
        const box = li.parentElement!;
        if (transcript?.open && !box.matches(':hover') && !box.contains(document.activeElement)) {
          box.scrollTop = Math.max(0, li.offsetTop - box.offsetTop - box.clientHeight / 3);
        }
      }
    }
  }

  /* ---- neither the pinned screen nor the site's header sits on top of what has keyboard focus */
  root.addEventListener('focusin', (e) => {
    const el = e.target as HTMLElement;
    if (screen.contains(el) || el === companion) return;
    requestAnimationFrame(() => {
      const pinned = getComputedStyle(screen).position === 'sticky';
      const edge = pinned ? screen.getBoundingClientRect().bottom : header && getComputedStyle(header).position === 'sticky' ? header.getBoundingClientRect().bottom : 0;
      if (!edge) return;
      const top = el.getBoundingClientRect().top;
      if (top < edge + 8) window.scrollBy(0, top - edge - 12);
    });
  });

  /* ---- controls made from the printed list */
  // A press on the part that is playing pauses it (Space on the row should not rewind the film);
  // any other row plays from its start.
  rows.forEach((r, k) => r.addEventListener('click', () => {
    if (k === wanted && !v.paused) v.pause();
    else if (k === wanted && started && !v.ended) void v.play().catch(() => {}); // a second press carries on, it does not rewind
    else playFrom(num(r, 't'));
  }));
  for (const li of lines) {
    const time = li.querySelector('.th-time');
    if (time) {
      const b = document.createElement('button');
      b.type = 'button';
      b.className = 'th-time';
      b.textContent = time.textContent;
      b.setAttribute('aria-label', `Play from ${time.textContent}`);
      time.replaceWith(b);
    }
    // Not when the click ends a text selection: someone copying a sentence is not asking to seek.
    li.addEventListener('click', () => { if (window.getSelection()?.isCollapsed !== false) playFrom(num(li, 't')); });
  }

  /* ---- the film */
  const startAt = $('[data-th-startat]');
  v.addEventListener('timeupdate', () => { if (!v.seeking) sync(v.currentTime); });
  v.addEventListener('seeked', () => sync(v.currentTime));
  let started = false;
  v.addEventListener('play', () => {
    started = true;
    // is-started pins the screen on a phone: from the first play until the film ends, paused or not,
    // so pausing to read a sentence does not send the film off the screen.
    root.classList.add('is-playing', 'is-started');
    if (startAt) startAt.hidden = true;
    if (ended) { ended = false; }
  });
  v.addEventListener('pause', () => root.classList.remove('is-playing'));
  v.addEventListener('ended', () => {
    ended = true;
    root.classList.remove('is-playing', 'is-started');
    // If the companion is in view, Where next arrives in view under it; a reader further down is not moved.
    steady(() => { next.hidden = false; });
    sync(duration);
    endTop = below ? below.getBoundingClientRect().top : null;
    const take = $<HTMLDetailsElement>('details[data-th-take]');
    if (take) take.open = true;
    status.textContent = 'The film has ended. Where next is showing now.';
  });

  /* ---- "Pause and decide" comes with a way to pause that is right there. */
  const pauses = $$<HTMLButtonElement>('[data-th-pause]');
  // The words follow the player's real state, whoever changed it (this button, the player's own, a key).
  const paintPause = () => { for (const b of pauses) b.textContent = pauseLabel({ paused: v.paused, started }); };
  for (const b of pauses) b.addEventListener('click', () => { if (v.paused) void v.play().catch(() => {}); else v.pause(); });
  v.addEventListener('play', paintPause);
  v.addEventListener('pause', paintPause);
  paintPause();

  /* ---- "Cards ready" (CardsPrompt.astro) appears after the player; it belongs in Where next. */
  let endTop: number | null = null;
  const slot = $('[data-th-cards]');
  if (slot && root.dataset.cardsLesson) {
    new MutationObserver(() => {
      const box = document.querySelector<HTMLElement>('.cards-prompt');
      if (!box || box.parentElement === slot) return;
      const sticky = header && getComputedStyle(header).position === 'sticky' ? header.getBoundingClientRect().bottom : 0;
      const parked = !!below && companion.getBoundingClientRect().top < sticky;
      slot.append(box);
      // Back to where things stood when the film ended (remembered there), no more and no less.
      if (parked && endTop !== null) window.scrollBy({ top: below!.getBoundingClientRect().top - endTop, behavior: 'instant' as ScrollBehavior });
    }).observe(document.body, { childList: true, subtree: true });
  }

  /* ---- hops keep the way back: "Back to the film you were watching, at 1:02". Carried in the link
     (the page's address, the film's key and the second), stored nowhere. No words are taken from the
     address: a link could otherwise put any text on the page. */
  root.addEventListener('click', (e) => {
    const a = (e.target as Element).closest?.('a[href]') as HTMLAnchorElement | null;
    // Only a plain click that leaves this page in this tab; a new tab leaves this one as it is.
    if (!a || e.defaultPrevented || e.button !== 0 || e.metaKey || e.ctrlKey || e.shiftKey || e.altKey || a.target === '_blank' || a.origin !== location.origin) return;
    const t = Math.floor(v.currentTime || 0);
    if (t < 5 || v.ended) return;
    if (a.matches('[data-th-hop]') && a.pathname.startsWith('/watch/')) {
      const u = new URL(a.href);
      u.searchParams.set('back', location.pathname);
      u.searchParams.set('backF', root.dataset.film ?? '');
      u.searchParams.set('backAt', String(t));
      a.href = u.pathname + u.search;
    }
    // The browser's own Back then opens this film at the same second, paused, whichever link was followed.
    history.replaceState(history.state, '', `${location.pathname}?film=${encodeURIComponent(root.dataset.film ?? '')}&at=${t}`);
  });
  const back = params.get('back') ?? '';
  const backF = params.get('backF') ?? '';
  const backAt = Math.floor(Number(params.get('backAt')));
  const backBox = $('[data-th-back]');
  if (backBox && /^\/watch\/[a-z0-9-]+\/(?:[a-z0-9-]+\/)?$/.test(back) && /^[a-z0-9-]+\/[a-z0-9-]+$/.test(backF) && backAt > 0 && backAt < 3600) {
    const a = document.createElement('a');
    a.href = `${back}?film=${encodeURIComponent(backF)}&at=${backAt}`;
    a.textContent = `Back to the film you were watching, at ${clock(backAt)}`;
    backBox.append(a);
    backBox.hidden = false;
  }

  /* ---- where the page starts */
  const at = Number(params.get('at'));
  const hook = Number(params.get('t'));
  if (params.get('film') === root.dataset.film && at > 0 && at < duration - 2) {
    if (startAt) { startAt.querySelector('[data-th-startat-time]')!.textContent = clock(at); startAt.hidden = false; }
    sync(at);
  } else if (params.has('t') && hook >= 0 && hook <= duration) {
    // The reviewer's hook shows the page as it is at that second. It does not touch the film, so it
    // cannot leave a "where you stopped" behind.
    sync(hook);
  } else sync(ended ? duration : 0);
}
