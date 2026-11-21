/* The mini syllabus, in the browser (/start/). Loads three small static files once, matches what
   was typed (src/lib/syllabus-match.mjs), builds the path (src/lib/start-path.mjs) and draws it,
   with the shared ladder (src/lib/hop-ladder.mjs) for "every level".

   What this file must never do: send what was typed anywhere, put it in the address or in
   storage, or write it back onto the page (a child may have typed something that is not a biology
   question, and reading it back in a search box's voice is wrong whatever comes after it). The only requests are GETs for static files; the one whose name depends on the answer
   is the matched idea's area (/graph/<area>.json), never the words. */
import { buildMatcher, matchQuestion } from './syllabus-match.mjs';
import { ideaFromArea, buildPath, timeFrom, TIMES } from './start-path.mjs';
import { ladderHtml, wireLadders } from './hop-ladder.mjs';
import { LEVEL_KEYS, LEVEL_SHORT, inSentence, gapLine, andList } from './hop-words.mjs';
import { readPrefs, writePrefs } from './prefs';
import { HELP, withNumbers } from './start-help.mjs';

type Matcher = ReturnType<typeof buildMatcher>;
const esc = (s: unknown) => String(s ?? '').replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;').replace(/"/g, '&quot;');
const json = (url: string) => fetch(url).then((r) => { if (!r.ok) throw new Error(url); return r.json(); });
const minutes = (n: number) => `${n} ${n === 1 ? 'minute' : 'minutes'}`;

let matcherP: Promise<Matcher> | undefined;
const loadMatcher = () => (matcherP ??= Promise.all([json('/graph.json'), json('/ideas/lessons.json'), json('/start/lessons.json')])
  .then(([g, l, x]) => buildMatcher(g, l, x)).catch((e) => { matcherP = undefined; throw e; }));
const areaCache = new Map<string, Promise<any>>();
const loadArea = (id: string) => { if (!areaCache.has(id)) areaCache.set(id, json(`/graph/${id}.json`).catch((e) => { areaCache.delete(id); throw e; })); return areaCache.get(id)!; };

const KIND: Record<string, string> = { film: 'Watch', skim: 'Skim', lesson: 'Read', activity: 'Do' };
const KIND_NOTE: Record<string, string> = { skim: 'the main idea, the figures and the take-homes', lesson: 'its films included' };
const WAYS_OUT = '<a href="/search/">search inside every lesson</a> or <a href="/ideas/#every-idea">see every idea</a>';

interface Shown { ids: string[]; together: number; prefer: (string | undefined)[]; others: { id: string; name: string }[]; pin?: number }

export function start() {
  const input = document.querySelector<HTMLInputElement>('#st-q');
  const go = document.querySelector<HTMLButtonElement>('[data-st-go]');
  const outEl = document.querySelector<HTMLElement>('[data-st-out]');
  const statusEl = document.querySelector<HTMLElement>('[data-st-status]');
  const levelEl = document.querySelector<HTMLSelectElement>('[data-st-level]');
  const radios = Array.from(document.querySelectorAll<HTMLInputElement>('input[name="st-time"]'));
  if (!input || !go || !outEl || !statusEl || !levelEl) return;
  const out: HTMLElement = outEl, status: HTMLElement = statusEl, levelSel: HTMLSelectElement = levelEl;

  // The site-wide preferences pick the defaults; choosing here sets them.
  const prefs = readPrefs();
  let level = prefs.level ? LEVEL_KEYS.indexOf(prefs.level) : -1;
  let time: string = timeFrom(prefs.time);
  levelSel.value = level >= 0 ? LEVEL_KEYS[level] : '';
  radios.forEach((r) => { r.checked = r.value === time; });

  let shown: Shown | null = null;
  let run = 0;

  const say = (text: string) => { status.textContent = text; };
  const minutesOnControl = (stops: Record<string, number> | null) => {
    for (const t of TIMES) {
      const el = document.querySelector<HTMLElement>(`[data-st-min="${t}"]`);
      // When every choice comes to the same length (an activity is one thing), the numbers would only confuse.
      const same = stops && new Set(Object.values(stops)).size === 1;
      if (el) el.textContent = stops && !same ? `about ${stops[t]} min` : '';
    }
  };
  /** Something to see at once: on a slow connection the first answer takes a few seconds. */
  const busy = () => { out.setAttribute('aria-busy', 'true'); if (!out.querySelector('.st-result')) { out.innerHTML = '<p class="st-quiet st-busy">Finding a path…</p>'; say('Finding a path…'); } };
  const settle = () => out.removeAttribute('aria-busy');
  /** Bring the answer to the top of the screen, under the site's header. */
  const reveal = (focus: boolean) => {
    const h = out.querySelector<HTMLElement>('[data-st-top]');
    if (!h) return;
    const calm = window.matchMedia?.('(prefers-reduced-motion: reduce)').matches;
    h.scrollIntoView({ block: 'start', behavior: calm ? 'auto' : 'smooth' });
    if (focus) h.focus({ preventScroll: true });
  };

  function fail() {
    settle();
    out.innerHTML = '<p class="st-none" tabindex="-1" data-st-top>The list of ideas did not load. Check your connection and try again, or <a href="/ideas/">browse the ideas</a>.</p>';
    say('The list of ideas did not load.');
  }
  function nothing(html: string, spoken: string, focus = true) {
    settle();
    shown = null;
    minutesOnControl(null);
    out.innerHTML = `<div class="st-none" tabindex="-1" data-st-top>${html}</div>`;
    // After the help message nothing else follows it: not the page's own closing links.
    out.toggleAttribute('data-help', html.includes('st-urgent'));
    say(spoken);
    reveal(focus);
  }

  async function draw(focus: boolean, move = true) {
    if (!shown) return;
    const mine = ++run;
    const wasOpen = new Set(Array.from(out.querySelectorAll<HTMLDetailsElement>('details.st-ladder[open]')).map((d) => d.dataset.idea));
    busy();
    let m: Matcher;
    try { m = await loadMatcher(); } catch { return fail(); }
    const metas = shown.ids.map((id) => m.byId.get(id)).filter((x: any) => x && x.lessons.length) as any[];
    if (!metas.length) return nothing(`<p>That link names an idea this site does not have. You can ${WAYS_OUT}.</p>`, 'That idea is not on the site.', focus);
    let ideas: any[];
    try {
      ideas = (await Promise.all(metas.slice(0, Math.max(1, shown.together)).map(async (it) => ideaFromArea(await loadArea(m.areas[it.area][0]), it.id, m.minutes)))).filter(Boolean);
    } catch { return fail(); }
    if (mine !== run || !ideas.length) return;
    // An answer found through one lesson's own search phrase is that lesson: the path is built at its level.
    const pinned = shown.pin !== undefined && shown.pin !== level;
    const path = buildPath(ideas, { level: shown.pin !== undefined ? shown.pin : level >= 0 ? level : null, time: time as any, prefer: shown.prefer });
    if (!path) return;
    settle();
    minutesOnControl(path.stops);

    const main = ideas[0];
    const short = inSentence(main.id, main.label);
    const heading = ideas.length > 1 ? andList(ideas.map((i, k) => (k === 0 ? i.name : inSentence(i.id, i.label)))) : main.name;
    const activity = path.steps[0]?.kind === 'activity';
    const onlyActivity = main.rungs.every((r: any) => r.rank === 0);
    const oneLevel = new Set(main.rungs.map((r: any) => r.rank)).size === 1;
    const where = pinned ? `This is the lesson that answers those words. It is ${esc(path.levelAt)}.`
      : path.moved && level >= 0 ? `${gapLine(short, [level])} This path is ${esc(path.levelAt)}.`
      : onlyActivity ? 'So far this is taught only as a hands-on activity for ages 5 to 10.'
      : level < 0 ? `This path starts ${esc(path.levelAt)}, the first full lesson on it. Pick your level above to change that.` : '';
    const steps = path.steps.map((s: any) => `<li class="st-step st-${s.kind}">
        <span class="st-kind">${KIND[s.kind]}</span>
        <span class="st-what"><a class="st-go" href="${esc(s.href)}">${esc(s.title)}</a>${ideas.length > 1 ? ` <span class="st-of">${esc(LEVEL_SHORT[s.rank])}</span>` : ''}
          ${s.kind === 'activity' ? `<span class="st-hint">An activity for ages 5 to 10, run by a grown-up. The guide has the safety notes${s.filmLength ? ` and starts with a short film (${esc(s.filmLength)})` : ''}.</span>` : KIND_NOTE[s.kind] ? `<span class="st-hint">${KIND_NOTE[s.kind]}</span>` : ''}
          ${s.part ? `<a class="st-part" href="${esc(s.part)}">Go straight to the part on ${esc(inSentence(s.idea, ideas.find((i) => i.id === s.idea)?.label ?? ''))}</a>` : ''}</span>
        <span class="st-len">${esc(s.length)}</span></li>`).join('');
    const side = (dir: 'Simpler' | 'Deeper', r: any) => r ? `<li><span class="st-dir">${dir}</span> <a href="${esc(r.href)}">${esc(r.title)}</a> <span class="st-of">${esc(r.level)}${r.minutes ? `, ${r.minutes} min` : ''}</span>${r.film && r.rank > 0 ? ` · <a class="st-filmlink" href="${esc(r.film.href)}" aria-label="film ${esc(r.film.length)}: ${esc(r.film.title)}">film ${esc(r.film.length)}</a>` : ''}${r.adds ? `<span class="st-adds">${esc(r.adds)}</span>` : ''}${r.rank === 0 ? '<span class="st-adds">An activity run by a grown-up. The guide has the safety notes.</span>' : ''}</li>` : '';
    const beside = path.down || path.up
      ? `<h3>The same idea, simpler and deeper</h3><ul class="st-beside">${side('Simpler', path.down)}${side('Deeper', path.up)}</ul>${!path.down ? '<p class="st-quiet">Nothing simpler on the site yet.</p>' : ''}${!path.up ? '<p class="st-quiet">Nothing deeper on the site yet.</p>' : ''}`
      : onlyActivity ? '' : '<p class="st-quiet">This is the only level it is taught at so far.</p>';
    const ladders = ideas.map((it, k) => `<details class="st-ladder" data-idea="${esc(it.id)}"${ideas.length === 1 && oneLevel ? ' hidden' : ''}${wasOpen.has(it.id) ? ' open' : ''}><summary>${ideas.length > 1 ? `${esc(it.name)}: every level` : 'See every level'}</summary>${ladderHtml({ id: it.id, name: it.name, short: inSentence(it.id, it.label), rungs: it.rungs }, { hereRank: path.rank, hereLabel: level >= 0 && !path.moved ? 'the level you chose' : 'where this path is', hex: k === 0, window: false, facts: true })}<p class="st-quiet"><a href="/ideas/${esc(it.id)}/">${esc(it.name)}: its films and the ideas next door</a></p></details>`).join('');
    const near = main.near.map((n: any) => m.byId.get(n.id)).filter((x: any) => x && x.lessons.length).slice(0, 4);
    const nextDoor = near.length ? `<h3 class="st-next">Ideas next door</h3><p class="st-chips">${near.map((n: any) => `<button type="button" class="st-chip" data-st-idea="${esc(n.id)}">${esc(n.label)}</button>`).join('')}</p>` : '';
    const others = shown.others.length ? `<p class="st-other">Not what you meant? ${andList(shown.others.map((o) => `<button type="button" class="st-link" data-st-idea="${esc(o.id)}" data-st-other>${esc(o.name)}</button>`), 'or')}. You can also ${WAYS_OUT}.</p>` : `<p class="st-other">Not what you meant? You can ${WAYS_OUT}.</p>`;

    const size = `${path.steps.length === 1 ? 'One step' : path.minutes <= 15 ? 'A short path' : `A path of ${path.steps.length} steps`} ${esc(path.levelAt)}, about ${minutes(path.minutes)}.${activity && level === 0 ? ' Do it with a grown-up.' : ''}`;
    out.removeAttribute('data-help');
    out.innerHTML = `<section class="st-result" aria-labelledby="st-h">
      <h2 id="st-h" tabindex="-1" data-st-top>${esc(heading)}</h2>
      <p class="st-blurb">${esc(ideas.map((i) => i.blurb).join(' '))}</p>
      <p class="st-sum">${size}</p>
      <ol class="st-steps">${steps}</ol>
      ${where ? `<p class="st-quiet st-where">${where}</p>` : ''}
      ${beside}
      ${ladders}
      ${nextDoor}
      ${others}
    </section>`;
    wireLadders(out);
    // The heading takes focus and is read then; the status line adds only what the heading does not say.
    say(`${path.steps.length} ${path.steps.length === 1 ? 'step' : 'steps'} ${path.levelAt}, about ${minutes(path.minutes)}.`);
    if (move) reveal(focus);
  }

  async function ask(typed: string) {
    const q = typed.trim();
    if (!q) { shown = null; out.innerHTML = ''; say('Type a question or a word first.'); minutesOnControl(null); input!.focus(); return; }
    const mine = ++run;
    busy();
    let m: Matcher;
    try { m = await loadMatcher(); } catch { return fail(); }
    if (mine !== run) return;
    const res = matchQuestion(m, q);
    if (res.kind === 'match') {
      const n = Math.max(1, res.together);
      const top: any = res.ideas[0];
      const via = n === 1 && top.viaLesson ? m.byId.get(top.id)?.lessons.find((l: any) => l.slug === top.viaLesson) : null;
      shown = { ids: res.ideas.slice(0, n).map((r: any) => r.id), together: n, prefer: via ? [via.slug] : res.ideas.slice(0, n).map((r: any) => r.lesson), others: res.ideas.slice(n, n + 3).map((r: any) => ({ id: r.id, name: r.name })), ...(via ? { pin: via.rank } : {}) };
      return draw(true);
    }
    if (res.kind === 'help') {
      // The help comes first and alone: no lesson, no chips, and the words are not repeated.
      const u = HELP.urgent;
      return nothing(`<div class="st-urgent"><h2>${esc(u.heading)}</h2>${u.lines.map((l: string) => `<p>${withNumbers(l, esc)}</p>`).join('')}<p><a href="${esc(HELP.href)}">${esc(HELP.linkText)}</a></p></div>`, u.status);
    }
    if (res.kind === 'closest') {
      return nothing(`<p>I am not sure which idea that is. ${res.ideas.length === 1 ? 'This is the closest one' : 'These are the closest'}:</p>
        <p class="st-chips">${res.ideas.map((r: any) => `<button type="button" class="st-chip" data-st-idea="${esc(r.id)}">${esc(r.name)}</button>`).join('')}</p>
        <p>If that is not it, you can ${WAYS_OUT}.</p>`, `No sure match. ${res.ideas.length} close ${res.ideas.length === 1 ? 'idea' : 'ideas'} offered.`);
    }
    return nothing(`<p>I could not match that to an idea yet. You can ${WAYS_OUT}.</p>`, 'No match yet. You can search inside every lesson or see every idea.');
  }

  function openIdea(id: string, focus = true, keep = false) {
    // From "Not what you meant?" the question stays in the box and the other readings stay on offer.
    const others = keep && shown ? [...shown.ids.map((x) => ({ id: x, name: '' })), ...shown.others].filter((o) => o.id !== id) : [];
    shown = { ids: [id], together: 1, prefer: [], others: [] };
    if (others.length) loadMatcher().then((m) => { if (shown && shown.ids[0] === id) { shown.others = others.map((o) => ({ id: o.id, name: m.byId.get(o.id)?.name ?? o.name })).filter((o) => o.name).slice(0, 3); } }).catch(() => {}).finally(() => draw(focus));
    else draw(focus);
  }

  go.addEventListener('click', () => ask(input.value));
  input.addEventListener('keydown', (e) => { if (e.key === 'Enter' && !e.isComposing) { e.preventDefault(); ask(input.value); } });
  // Fetch the index once the page is idle, so the first answer does not wait for it.
  const warm = () => { loadMatcher().catch(() => {}); };
  if ('requestIdleCallback' in window) (window as any).requestIdleCallback(warm, { timeout: 4000 }); else setTimeout(warm, 1500);
  levelSel.addEventListener('change', () => {
    level = levelSel.value ? LEVEL_KEYS.indexOf(levelSel.value) : -1;
    writePrefs({ level: levelSel.value || null });
    draw(false, false);
  });
  radios.forEach((r) => r.addEventListener('change', () => {
    if (!r.checked) return;
    time = r.value;
    writePrefs({ time });
    draw(false, false);
  }));
  document.addEventListener('click', (e) => {
    const t = (e.target as HTMLElement | null)?.closest<HTMLElement>('[data-st-try], [data-st-idea]');
    if (!t) return;
    if (t.dataset.stTry) { input.value = t.dataset.stTry; ask(input.value); return; }
    if (t.dataset.stIdea) {
      const keep = t.hasAttribute('data-st-other');
      if (!keep) input.value = '';
      openIdea(t.dataset.stIdea, true, keep);
    }
  });
  // The page is live: switch on what the script drives.
  go.disabled = false;
  document.querySelectorAll<HTMLButtonElement>('[data-st-try]').forEach((b) => { b.disabled = false; });

  // ?idea=<id>: a link from another page straight to an idea's path.
  const preset = (new URLSearchParams(location.search).get('idea') ?? '').trim().toLowerCase().replace(/\/+$/, '');
  if (/^[a-z0-9]+(-[a-z0-9]+)*$/.test(preset)) openIdea(preset, false);
  else if (preset) nothing(`<p>That link names an idea this site does not have. You can ${WAYS_OUT}.</p>`, 'That idea is not on the site.', false);
  // Words typed while the page was still loading are answered now.
  else if (input.value.trim()) ask(input.value);
}
