// Class-slide viewer: an audience window and, with ?presenter=1, a presenter window.
// The two stay in step over a BroadcastChannel, so either can drive. Plain JS, no framework.
// deck.json is built by scripts/build-slides.py; notes.json is served to instructors only.
(() => {
  const SLUG = (location.pathname.match(/^\/slides\/([^/]+)/) || [])[1] || "";
  const PRESENTER = new URLSearchParams(location.search).get("presenter") === "1";
  const $ = (id) => document.getElementById(id);
  const FADE_MS = 200;

  let deck = null, notes = {}, steps = [], idx = 0;
  let isInstructor = false;
  let t0 = null;                 // presenter timer: set by the first navigation
  let black = false;
  let syncing = true;            // the first answer to our hello may move us to the other window's step
  let videoState = { playing: false, t: 0, step: -1 };
  let statusTimer = null;
  const chan = "BroadcastChannel" in window ? new BroadcastChannel("slides-" + SLUG) : null;
  const send = (m) => { try { chan && chan.postMessage(m); } catch {} };

  function showMsg(html) {
    $("msg").innerHTML = html;
    $("msg").hidden = false;
    $("audience").hidden = true;
    $("presenter").hidden = true;
  }

  // ---------- a scaled 1280x720 stage ----------
  // show() swaps in a fresh layer for a step and cross-fades from the old one. Layers are rebuilt
  // each time, so a movie that is left is paused and discarded, never left playing under the next slide.
  function makeStage(box, mode) {   // mode: "audience" | "current" | "preview"
    const stage = document.createElement("div");
    stage.className = "stage";
    box.appendChild(stage);
    let token = 0;

    function fit() {
      const s = Math.min(box.clientWidth / 1280, box.clientHeight / 720) || 1;
      const x = (box.clientWidth - 1280 * s) / 2, y = (box.clientHeight - 720 * s) / 2;
      stage.style.transform = `translate(${x}px, ${y}px) scale(${s})`;
    }
    new ResizeObserver(fit).observe(box);
    fit();

    function drop(layer) {
      layer.querySelectorAll("video").forEach((v) => { try { v.pause(); } catch {} });
      layer.remove();
    }

    function prepare(layer) {
      layer.querySelectorAll("video").forEach((v) => {
        v.setAttribute("playsinline", "");
        if (mode !== "audience") { v.muted = true; v.removeAttribute("controls"); v.removeAttribute("autoplay"); v.preload = "none"; }
      });
    }

    async function ready(layer) {
      const imgs = [...layer.querySelectorAll("img")].filter((i) => !i.complete);
      const vids = [...layer.querySelectorAll("video[poster]")];
      vids.forEach((v) => { const i = new Image(); i.src = new URL(v.getAttribute("poster"), document.baseURI).href; if (!i.complete) imgs.push(i); });
      if (!imgs.length) return;
      await Promise.race([
        Promise.all(imgs.map((i) => (i.decode ? i.decode().catch(() => {}) : Promise.resolve()))),
        new Promise((r) => setTimeout(r, 600)),
      ]);
    }

    return {
      async show(step, animate) {
        const my = ++token;
        for (const l of [...stage.children]) if (l !== stage.lastElementChild) drop(l);
        const old = stage.lastElementChild;
        if (!step) { if (old) drop(old); return; }
        const layer = document.createElement("div");
        layer.className = "layer";
        layer.innerHTML = step.html;
        prepare(layer);
        if (!animate || !old) {
          if (old) drop(old);
          stage.appendChild(layer);
          return;
        }
        layer.classList.add("fading");
        stage.appendChild(layer);
        await ready(layer);
        if (my !== token) return drop(layer);     // a later step already took over
        void layer.offsetWidth;
        layer.classList.remove("fading");
        setTimeout(() => { if (my === token && old.parentNode) drop(old); }, FADE_MS + 40);
      },
      video: () => stage.lastElementChild && stage.lastElementChild.querySelector("video"),
      pauseAll: () => stage.querySelectorAll("video").forEach((v) => { try { v.pause(); } catch {} }),
    };
  }

  let aud = null, cur = null, nxt = null;

  // Images of the next few steps are fetched ahead, so a slide never paints half-loaded.
  function preload(from) {
    for (let i = from; i < Math.min(steps.length, from + 4); i++) {
      for (const m of steps[i].html.matchAll(/assets\/[\w.-]+\.(?:jpg|png)/g)) new Image().src = m[0];
    }
  }

  // ---------- navigation ----------
  function go(n, opts = {}) {
    n = Math.max(0, Math.min(steps.length - 1, n));
    const moved = n !== idx || opts.force;
    if (moved && (aud || cur)) {
      // A movie never keeps playing into the next step.
      if (aud) aud.pauseAll();
      if (cur) cur.pauseAll();
    }
    idx = n;
    history.replaceState(null, "", location.pathname + location.search + "#" + (idx + 1));
    if (moved) videoState = { playing: false, t: 0, step: idx };
    render(moved && !opts.force);
    preload(idx + 1);
    if (!opts.remote) send({ type: "nav", step: idx });
    if (moved && !opts.initial && PRESENTER && t0 === null) t0 = Date.now();
  }
  const next = () => go(idx + 1), prev = () => go(idx - 1);

  function render(animate) {
    const s = steps[idx];
    if (aud) aud.show(s, animate);
    if (cur) {
      cur.show(s, animate);
      nxt.show(steps[idx + 1] || null, false);
      $("p-count").textContent = `Step ${idx + 1} / ${steps.length}`;
      $("p-title").textContent = s.title + (s.step === "a" ? " · prediction" : s.step === "b" ? " · answer" : "");
      const n = steps[idx + 1];
      $("p-next-label").textContent = !n ? "End of deck" : n.slide === s.slide && n.step === "b" ? "Answer" : "Next";
      const sameSlide = renderedSlide === s.slide;
      renderedSlide = s.slide;
      const box = $("p-notes");
      box.textContent = notes[s.slide] || "(no notes for this slide)";
      if (!sameSlide) box.scrollTop = 0;
      const hasVideo = /<video\b/.test(s.html);
      $("p-video").hidden = !hasVideo;
      updateVideoButton();
    }
  }
  let renderedSlide = null;

  // ---------- movies ----------
  function currentVideo() { return (aud || cur).video(); }

  // Audience window: tell the presenter window what the movie is doing.
  function watchVideo() {
    if (!aud) return;
    const v = aud.video();
    if (!v || v._watched) return;
    v._watched = true;
    const report = () => send({ type: "video", step: idx, playing: !v.paused && !v.ended, t: v.currentTime });
    ["play", "pause", "seeked", "ended"].forEach((e) => v.addEventListener(e, report));
    let last = 0;
    v.addEventListener("timeupdate", () => { if (Date.now() - last > 500) { last = Date.now(); report(); } });
  }

  // Only a refusal (no click in this window yet) is worth telling the presenter about; a play()
  // that was cut short by a step change (AbortError) is not.
  const playOrWarn = (v) => v.play().catch((e) => { if (e && e.name === "NotAllowedError") send({ type: "vblocked" }); });

  function toggleVideoHere() {
    const v = aud && aud.video();
    if (!v) return;
    if (v.paused) playOrWarn(v);
    else v.pause();
  }

  function setStatus(msg, ms) {
    $("p-status").textContent = msg || "";
    clearTimeout(statusTimer);
    if (msg && ms) statusTimer = setTimeout(() => { $("p-status").textContent = ""; }, ms);
  }

  function updateVideoButton() {
    const playing = videoState.step === idx && videoState.playing;
    $("p-video").textContent = playing ? "❚❚ Pause" : "▶ Play on screen";
  }

  // Presenter window: ask the audience window to play or pause.
  let pending = null;
  function toggleVideoRemote() {
    if (!cur || $("p-video").hidden) return;
    const want = videoState.step === idx && videoState.playing ? "pause" : "play";
    send({ type: "vcmd", cmd: want, step: idx });
    clearTimeout(pending);
    pending = setTimeout(() => setStatus("No answer from the audience window. Open the slides there (p from that window) and click it once.", 6000), 1500);
  }

  function followVideo(m) {
    if (m.step !== idx) return;
    clearTimeout(pending);
    setStatus("");
    videoState = { playing: m.playing, t: m.t, step: m.step };
    updateVideoButton();
    const v = cur && cur.video();
    if (!v) return;
    if (Math.abs(v.currentTime - m.t) > 0.7) { try { v.currentTime = m.t; } catch {} }
    if (m.playing) v.play().catch(() => {}); else v.pause();
  }

  // ---------- messages between windows ----------
  if (chan) chan.onmessage = (e) => {
    const m = e.data || {};
    if (m.type === "hello") { send({ type: "nav", step: idx, black }); return; }
    if (m.type === "nav") {
      if (!steps.length) return;
      if (m.black !== undefined) setBlack(m.black, true);
      if (m.step !== idx) go(m.step, { remote: true, initial: syncing });
      syncing = false;
    } else if (m.type === "black") setBlack(m.on, true);
    else if (m.type === "vcmd" && aud && m.step === idx) {
      const v = aud.video();
      if (!v) return;
      if (m.cmd === "play") playOrWarn(v); else v.pause();
    } else if (m.type === "video" && cur) followVideo(m);
    else if (m.type === "vblocked" && cur) {
      clearTimeout(pending);
      setStatus("The audience window blocked playback. Click it once, then try again.", 8000);
    }
  };

  // ---------- screen controls ----------
  function setBlack(on, remote) {
    black = on;
    if (aud) $("black").hidden = !on;
    if (cur) setStatus(on ? "Screen is black (b to bring it back)" : "", 0);
    if (!remote) send({ type: "black", on });
  }

  function toggleFullscreen() {
    if (document.fullscreenElement) document.exitFullscreen();
    else document.documentElement.requestFullscreen && document.documentElement.requestFullscreen().catch(() => {});
  }

  let presWin = null;
  function openPresenter() {
    if (!isInstructor || PRESENTER) return;
    if (presWin && !presWin.closed) { presWin.focus(); return; }
    presWin = window.open(location.pathname + "?presenter=1#" + (idx + 1), "slides-presenter-" + SLUG, "popup,width=1400,height=860");
  }

  function toggleHelp(on) {
    const h = $("help");
    h.hidden = on === undefined ? !h.hidden : !on;
  }

  document.addEventListener("keydown", (e) => {
    if (!steps.length || e.ctrlKey || e.metaKey || e.altKey) return;
    let handled = true;
    switch (e.key) {
      case "ArrowRight": case "ArrowDown": case " ": case "PageDown": next(); break;
      case "ArrowLeft": case "ArrowUp": case "PageUp": prev(); break;
      case "Home": go(0); break;
      case "End": go(steps.length - 1); break;
      case "f": case "F": toggleFullscreen(); break;
      case "b": case "B": setBlack(!black); break;
      case "v": case "V": if (PRESENTER) toggleVideoRemote(); else toggleVideoHere(); break;
      case "p": case "P": openPresenter(); break;
      case "?": toggleHelp(); break;
      case "Escape": if (!$("help").hidden) toggleHelp(false); else if (black) setBlack(false); else handled = false; break;
      default: handled = false;
    }
    // Keep the browser (and a focused movie) from also acting on the key.
    if (handled) e.preventDefault();
  }, true);

  // ---------- boot ----------
  async function boot() {
    isInstructor = false;
    try {
      const me = await fetch("/api/me", { credentials: "same-origin" });
      if (me.ok) isInstructor = (await me.json()).role === "instructor";
    } catch {}
    document.body.classList.toggle("student", !isInstructor);

    let dr, nr = null;
    try {
      [dr, nr] = await Promise.all([fetch("deck.json", { credentials: "same-origin" }),
        PRESENTER ? fetch("notes.json", { credentials: "same-origin" }) : null]);
    } catch {
      return showMsg("Could not reach the server. Check the connection and reload.");
    }
    if (dr.status === 401) return showMsg('Sign in first at <a href="/">the Expedition page</a>, then reload this page.');
    if (dr.status === 403) return showMsg("These slides open after class.");
    if (!dr.ok) return showMsg("The slides could not be loaded (" + dr.status + ").");
    if (PRESENTER) {
      if (nr.status === 403) return showMsg('Presenter mode is for instructors. <a href="' + location.pathname + '">Open the slides</a> instead.');
      if (!nr.ok) return showMsg("The speaker notes could not be loaded (" + nr.status + ").");
      notes = await nr.json();
    }
    deck = await dr.json();
    steps = deck.steps;

    if (deck.fonts) {
      const l = document.createElement("link");
      l.rel = "stylesheet"; l.href = deck.fonts;
      document.head.appendChild(l);
    }
    $("deck-css").textContent = deck.css || "";
    document.title = (PRESENTER ? "Presenter · " : "") + deck.title;

    $("msg").hidden = true;
    if (PRESENTER) {
      $("presenter").hidden = false;
      cur = makeStage($("cur-stage"), "current");
      nxt = makeStage($("next-stage"), "preview");
    } else {
      $("audience").hidden = false;
      aud = makeStage($("aud-stage"), "audience");
      // a click on the slide advances; a click on a movie belongs to its controls
      $("aud-stage").addEventListener("click", (e) => { if (!e.target.closest("video")) next(); });
      let idle;
      const wake = () => { document.body.classList.remove("idle"); clearTimeout(idle); idle = setTimeout(() => document.body.classList.add("idle"), 2500); };
      document.addEventListener("mousemove", wake);
      wake();
    }
    // the audience window's movie, once a step has put one on screen
    if (aud) new MutationObserver(watchVideo).observe($("aud-stage"), { childList: true, subtree: true });

    const h = parseInt(location.hash.slice(1), 10);
    go(Number.isFinite(h) ? h - 1 : 0, { initial: true, force: true, remote: true });
    window.addEventListener("hashchange", () => {
      const n = parseInt(location.hash.slice(1), 10);
      if (Number.isFinite(n) && n - 1 !== idx) go(n - 1);
    });
    send({ type: "hello" });
    setTimeout(() => { syncing = false; }, 800);

    if (PRESENTER) {
      $("p-next").onclick = () => { next(); document.activeElement.blur(); };
      $("p-prev").onclick = () => { prev(); document.activeElement.blur(); };
      $("p-video").onclick = () => { toggleVideoRemote(); document.activeElement.blur(); };
      $("p-timer").onclick = () => { t0 = null; tick(); document.activeElement.blur(); };
      const pad = (n) => String(n).padStart(2, "0");
      const tick = () => {
        const s = t0 === null ? 0 : Math.floor((Date.now() - t0) / 1000);
        $("p-timer").textContent = s >= 3600 ? `${Math.floor(s / 3600)}:${pad(Math.floor(s / 60) % 60)}:${pad(s % 60)}` : `${Math.floor(s / 60)}:${pad(s % 60)}`;
        $("p-clock").textContent = new Date().toLocaleTimeString([], { hour: "numeric", minute: "2-digit" });
      };
      tick();
      setInterval(tick, 1000);
    }
  }

  boot();
})();
