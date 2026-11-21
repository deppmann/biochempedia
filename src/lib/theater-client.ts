/* The theater in the browser (2026-11-20): makes a /watch/ page follow its film.

   Everything it shows is already in the page's HTML (src/pages/watch/[...path].astro); this only
   chooses what is in view for the second the film is at. Rules it keeps:
     - nothing plays until the viewer presses play, or taps a part or a sentence (which is a press);
     - while the film waits on its own question, only the question is up;
     - a word comes up when the film says it, a figure when its part starts, never earlier;
     - the panel is never swapped out from under keyboard focus;
     - part changes are not announced aloud (they would talk over the narration): the list of parts
       carries aria-current instead. One sentence is announced, when the film ends;
     - nothing is stored. The watched record is trackFilms() in BaseLayout.

   Reviewer hooks: ?t=<seconds> puts the page in the state it has at that second without playing;
   ?state=end shows the end of the film. ?film=<key>&at=<seconds> is the site's resume link
   (resumeFromLink in film-progress.ts does the seek; this adds "Press play to start at m:ss."). */

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
  const panels = $$('[data-th-panel]');
  const rows = $$<HTMLButtonElement>('[data-th-go]');
  const questions = $$('[data-th-question]');
  const rest = $('[data-th-rest]');
  const figs = $<HTMLDetailsElement>('[data-th-figs]');
  const terms = $$('[data-at]');
  const lines = $$('[data-th-lines] > li');
  const segs = $$<HTMLButtonElement>('.th-seg');
  const bar = $('[data-th-bar]');
  const next = $('[data-th-next]')!;
  const status = $('[data-th-status]')!;
  const transcript = $<HTMLDetailsElement>('[data-th-transcript]');

  root.classList.add('th-live');
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

  /* ---- the companion */
  let part = -1;
  let wanted = -1;
  const showPart = (i: number) => {
    part = i;
    panels.forEach((p, k) => p.classList.toggle('is-now', k === i));
    rows.forEach((r, k) => { if (k === i) r.setAttribute('aria-current', 'true'); else r.removeAttribute('aria-current'); });
  };
  const setPart = (i: number) => {
    wanted = i;
    if (i === part) return;
    // Someone is on a link in the panel: leave it where it is until they move on.
    if (part !== -1 && companion.contains(document.activeElement)) return;
    showPart(i);
  };
  companion.addEventListener('focusout', () => {
    requestAnimationFrame(() => {
      if (companion.contains(document.activeElement)) return;
      if (wanted !== part) showPart(wanted);
      if (rest) sync(v.currentTime);
    });
  });

  let line = -1;
  function sync(t: number): void {
    if (panels.length) {
      let i = 0;
      panels.forEach((p, k) => { if (num(p, 't') <= t + 0.05) i = k; });
      setPart(i);
    }
    for (const el of terms) el.hidden = t + 0.05 < num(el, 'at');
    if (questions.length) {
      let asking = false;
      for (const q of questions) {
        const on = t + 0.05 >= num(q, 't') && t < num(q, 'until') && !ended;
        q.hidden = !on;
        asking ||= on;
      }
      // Not while someone is on the lesson link: it stays until they move on.
      if (rest) rest.hidden = asking && !rest.contains(document.activeElement);
    }
    if (figs && figs.hidden && (ended || (lastReveal > 0 && t >= lastReveal))) figs.hidden = false;
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

  /* ---- the pinned screen never sits on top of what has keyboard focus */
  const screen = $('[data-th-screen]')!;
  root.addEventListener('focusin', (e) => {
    const el = e.target as HTMLElement;
    if (getComputedStyle(screen).position !== 'sticky' || screen.contains(el)) return;
    requestAnimationFrame(() => {
      const edge = screen.getBoundingClientRect().bottom;
      const top = el.getBoundingClientRect().top;
      if (top < edge + 8) window.scrollBy(0, top - edge - 12);
    });
  });

  /* ---- controls made from the printed list */
  for (const r of rows) r.addEventListener('click', () => playFrom(num(r, 't')));
  for (const b of segs) b.addEventListener('click', () => playFrom(num(b, 't')));
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
    li.addEventListener('click', () => playFrom(num(li, 't')));
  }

  /* ---- the film */
  const startAt = $('[data-th-startat]');
  v.addEventListener('timeupdate', () => { if (!v.seeking) sync(v.currentTime); });
  v.addEventListener('seeked', () => sync(v.currentTime));
  v.addEventListener('play', () => {
    root.classList.add('is-playing');
    if (startAt) startAt.hidden = true;
    if (ended) { ended = false; }
  });
  v.addEventListener('pause', () => root.classList.remove('is-playing'));
  v.addEventListener('ended', () => {
    ended = true;
    root.classList.remove('is-playing');
    next.hidden = false;
    sync(duration);
    const take = $<HTMLDetailsElement>('details[data-th-take]');
    if (take) take.open = true;
    status.textContent = 'The film has ended. Where next is under the film.';
  });

  /* ---- "Cards ready" (CardsPrompt.astro) appears after the player; it belongs in Where next. */
  const slot = $('[data-th-cards]');
  if (slot && root.dataset.cardsLesson) {
    new MutationObserver(() => {
      const box = document.querySelector('.cards-prompt');
      if (box && box.parentElement !== slot) slot.append(box);
    }).observe(document.body, { childList: true, subtree: true });
  }

  /* ---- hops keep the way back: "Back to <film>, at 1:02". Carried in the link, stored nowhere. */
  const title = $('[data-th-title]')?.textContent ?? '';
  for (const a of $$<HTMLAnchorElement>('a[data-th-hop]')) {
    a.addEventListener('click', () => {
      const t = Math.floor(v.currentTime || 0);
      if (t < 5 || !a.pathname.startsWith('/watch/')) return;
      const u = new URL(a.href);
      u.searchParams.set('back', location.pathname);
      u.searchParams.set('backAt', String(t));
      u.searchParams.set('backT', title);
      a.href = u.pathname + u.search;
    });
  }
  const back = params.get('back') ?? '';
  const backAt = Math.floor(Number(params.get('backAt')));
  const backBox = $('[data-th-back]');
  const m = /^\/watch\/([a-z0-9-]+)\/(?:([a-z0-9-]+)\/)?$/.exec(back);
  if (backBox && m && backAt > 0 && backAt < 3600) {
    const a = document.createElement('a');
    a.href = `${back}?film=${encodeURIComponent(`${m[1]}/${m[2] ?? 'explainer'}`)}&at=${backAt}`;
    const name = (params.get('backT') ?? '').slice(0, 120).trim();
    a.textContent = `Back to ${name || 'the film you were watching'}, at ${clock(backAt)}`;
    backBox.append(a);
    backBox.hidden = false;
  }

  /* ---- where the page starts */
  const at = Number(params.get('at'));
  const hook = Number(params.get('t'));
  if (params.get('film') === root.dataset.film && at > 0 && at < duration) {
    if (startAt) { startAt.querySelector('[data-th-startat-time]')!.textContent = clock(at); startAt.hidden = false; }
    sync(at);
  } else if (params.has('t') && hook >= 0 && hook <= duration) {
    const seek = () => { try { v.currentTime = hook; } catch { /* stays at the start */ } };
    if (v.readyState >= 1) seek(); else { v.addEventListener('loadedmetadata', seek, { once: true }); v.preload = 'metadata'; }
    sync(hook);
  } else sync(ended ? duration : 0);
}
