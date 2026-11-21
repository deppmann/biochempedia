/* The mini syllabus, in the browser (/start/). Loads three small static files once, matches what
   was typed (src/lib/syllabus-match.mjs), builds the path (src/lib/start-path.mjs) and draws it,
   with the shared ladder (src/lib/hop-ladder.mjs) for "every level".

   What this file must never do: send what was typed anywhere, or put it in the address. The only
   requests are GETs for static files whose names do not depend on the typed words except through
   the matched idea's area (/graph/<area>.json). */
import { buildMatcher, matchQuestion } from './syllabus-match.mjs';
import { ideaFromArea, buildPath, timeFrom, TIMES } from './start-path.mjs';
import { ladderHtml, wireLadders } from './hop-ladder.mjs';
import { LEVEL_KEYS, LEVEL_SHORT, inSentence, gapLine, andList } from './hop-words.mjs';
import { readPrefs, writePrefs } from './prefs';

type Matcher = ReturnType<typeof buildMatcher>;
const esc = (s: unknown) => String(s ?? '').replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;').replace(/"/g, '&quot;');
const json = (url: string) => fetch(url).then((r) => { if (!r.ok) throw new Error(url); return r.json(); });

let matcherP: Promise<Matcher> | undefined;
const loadMatcher = () => (matcherP ??= Promise.all([json('/graph.json'), json('/ideas/lessons.json'), json('/start/lessons.json')])
  .then(([g, l, x]) => buildMatcher(g, l, x)).catch((e) => { matcherP = undefined; throw e; }));
const areaCache = new Map<string, Promise<any>>();
const loadArea = (id: string) => { if (!areaCache.has(id)) areaCache.set(id, json(`/graph/${id}.json`).catch((e) => { areaCache.delete(id); throw e; })); return areaCache.get(id)!; };

const KIND: Record<string, string> = { film: 'Watch', skim: 'Skim', lesson: 'Read', activity: 'Do' };
const KIND_NOTE: Record<string, string> = { skim: 'the main idea, the figures and the take-homes', lesson: 'its films included', activity: 'with a grown-up; its film included' };

export function start() {
  const form = document.querySelector<HTMLFormElement>('[data-st-form]');
  const input = document.querySelector<HTMLInputElement>('#st-q');
  const outEl = document.querySelector<HTMLElement>('[data-st-out]');
  const statusEl = document.querySelector<HTMLElement>('[data-st-status]');
  const levelEl = document.querySelector<HTMLSelectElement>('[data-st-level]');
  const radios = Array.from(document.querySelectorAll<HTMLInputElement>('input[name="st-time"]'));
  if (!form || !input || !outEl || !statusEl || !levelEl) return;
  const out: HTMLElement = outEl, status: HTMLElement = statusEl, levelSel: HTMLSelectElement = levelEl;

  // The site-wide preferences pick the defaults; choosing here sets them.
  const prefs = readPrefs();
  let level = prefs.level ? LEVEL_KEYS.indexOf(prefs.level) : -1;
  let time: string = timeFrom(prefs.time);
  levelSel.value = level >= 0 ? LEVEL_KEYS[level] : '';
  radios.forEach((r) => { r.checked = r.value === time; });

  /** What is on show: the ideas, main one first, and how many of them the path covers. */
  let shown: { ids: string[]; together: number; prefer: (string | undefined)[]; others: { id: string; name: string }[]; typed: string } | null = null;
  let run = 0;

  const say = (text: string) => { status.textContent = text; };
  const minutesOnControl = (stops: Record<string, number> | null) => {
    for (const t of TIMES) {
      const el = document.querySelector<HTMLElement>(`[data-st-min="${t}"]`);
      if (el) el.textContent = stops ? `about ${stops[t]} min` : '';
    }
  };

  async function draw(focus: boolean) {
    if (!shown) return;
    const mine = ++run;
    let m: Matcher;
    try { m = await loadMatcher(); } catch { return fail(); }
    const metas = shown.ids.map((id) => m.byId.get(id)).filter(Boolean) as any[];
    if (!metas.length) { out.innerHTML = ''; return; }
    let ideas: any[];
    try {
      ideas = (await Promise.all(metas.slice(0, Math.max(1, shown.together)).map(async (it) => ideaFromArea(await loadArea(m.areas[it.area][0]), it.id, m.minutes)))).filter(Boolean);
    } catch { return fail(); }
    if (mine !== run || !ideas.length) return;
    const path = buildPath(ideas, { level: level >= 0 ? level : null, time: time as any, prefer: shown.prefer });
    if (!path) return;
    minutesOnControl(path.stops);

    const names = ideas.map((i) => i.name);
    const main = ideas[0];
    const short = inSentence(main.id, main.label);
    const where = path.moved && level >= 0
      ? `${gapLine(short, [level])} This path is at ${esc(path.level)} level.`
      : path.rank === 0 && main.rungs.every((r: any) => r.rank === 0) ? 'So far this is taught only as a hands-on activity for ages 5 to 10, which a grown-up runs.'
      : level < 0 ? `This path starts at ${esc(path.level)} level, the simplest lesson on it. Pick your level above to change that.` : '';
    const steps = path.steps.map((s: any) => `<li class="st-step st-${s.kind}">
        <span class="st-kind">${KIND[s.kind]}</span>
        <span class="st-what"><a href="${esc(s.href)}">${esc(s.title)}</a>${ideas.length > 1 ? ` <span class="st-of">${esc(LEVEL_SHORT[s.rank])}</span>` : ''}
          ${KIND_NOTE[s.kind] ? `<span class="st-hint">${KIND_NOTE[s.kind]}</span>` : ''}
          ${s.part ? `<a class="st-part" href="${esc(s.part)}">Go straight to the part on ${esc(inSentence(s.idea, ideas.find((i) => i.id === s.idea)?.label ?? ''))}</a>` : ''}</span>
        <span class="st-len">${esc(s.length)}</span></li>`).join('');
    const side = (dir: 'Simpler' | 'Deeper', r: any) => r ? `<li><span class="st-dir">${dir}</span> <a href="${esc(r.href)}">${esc(r.title)}</a> <span class="st-of">${esc(r.level)}${r.minutes ? `, ${r.minutes} min` : ''}</span>${r.film ? ` · <a href="${esc(r.film.href)}" aria-label="film ${esc(r.film.length)}: ${esc(r.film.title)}">film ${esc(r.film.length)}</a>` : ''}${r.adds ? `<span class="st-adds">${esc(r.adds)}</span>` : ''}</li>` : '';
    const beside = path.down || path.up
      ? `<h3>The same idea, one level away</h3><ul class="st-beside">${side('Simpler', path.down)}${side('Deeper', path.up)}</ul>${!path.down ? '<p class="st-quiet">Nothing simpler on the site yet.</p>' : ''}${!path.up ? '<p class="st-quiet">Nothing deeper on the site yet.</p>' : ''}`
      : '<p class="st-quiet">This is the only level it is taught at so far.</p>';
    const ladders = ideas.map((it, k) => `<details class="st-ladder"${ideas.length === 1 && it.rungs.length <= 1 ? ' hidden' : ''}><summary>${ideas.length > 1 ? `${esc(it.name)}: every level` : 'See every level'}</summary>${ladderHtml({ id: it.id, name: it.name, short: inSentence(it.id, it.label), rungs: it.rungs }, { hereRank: path.rank, hereLabel: level >= 0 && !path.moved ? 'the level you chose' : 'where this path is', hex: k === 0, window: false, facts: true })}<p class="st-quiet"><a href="/ideas/${esc(it.id)}/">${esc(it.name)}: its films and the ideas next door</a></p></details>`).join('');
    const near = main.near.map((n: any) => m.byId.get(n.id)).filter((x: any) => x && x.lessons.length).slice(0, 4);
    const nextDoor = near.length ? `<h3>Ideas next door</h3><p class="st-chips">${near.map((n: any) => `<button type="button" class="st-chip" data-st-idea="${esc(n.id)}">${esc(n.label)}</button>`).join('')}</p>` : '';
    const others = shown.others.length ? `<p class="st-other">Not what you meant? ${andList(shown.others.map((o) => `<button type="button" class="st-link" data-st-idea="${esc(o.id)}">${esc(o.name)}</button>`), 'or')}. You can also <a href="/search/">search inside every lesson</a>.</p>` : `<p class="st-other">Not what you meant? <a href="/search/">Search inside every lesson</a> or <a href="/ideas/#every-idea">see every idea</a>.</p>`;

    out.innerHTML = `<section class="st-result" aria-labelledby="st-h">
      <h2 id="st-h" tabindex="-1">${esc(andList(names))}</h2>
      <p class="st-blurb">${esc(ideas.map((i) => i.blurb).join(' '))}</p>
      <p class="st-sum">${path.steps.length === 1 ? 'One step' : 'A short path'} at ${esc(path.level)} level, about ${path.minutes} ${path.minutes === 1 ? 'minute' : 'minutes'}.</p>
      <ol class="st-steps">${steps}</ol>
      ${where ? `<p class="st-quiet">${where}</p>` : ''}
      ${beside}
      ${ladders}
      ${nextDoor}
      ${others}
    </section>`;
    wireLadders(out);
    say(`${andList(names)}: ${path.steps.length} ${path.steps.length === 1 ? 'step' : 'steps'} at ${path.level} level, about ${path.minutes} minutes.`);
    if (focus) out.querySelector<HTMLElement>('#st-h')?.focus({ preventScroll: false });
  }

  function fail() {
    out.innerHTML = '<p class="st-none">The list of ideas did not load. Check your connection and try again, or <a href="/ideas/">browse the ideas</a>.</p>';
    say('The list of ideas did not load.');
  }

  async function ask(typed: string) {
    const q = typed.trim();
    if (!q) { shown = null; out.innerHTML = ''; say(''); minutesOnControl(null); return; }
    const mine = ++run;
    let m: Matcher;
    try { m = await loadMatcher(); } catch { return fail(); }
    if (mine !== run) return;
    const res = matchQuestion(m, q);
    if (res.kind === 'match') {
      const n = Math.max(1, res.together);
      shown = { ids: res.ideas.slice(0, n).map((r: any) => r.id), together: n, prefer: res.ideas.slice(0, n).map((r: any) => r.lesson), others: res.ideas.slice(n, n + 3).map((r: any) => ({ id: r.id, name: r.name })), typed: q };
      return draw(true);
    }
    shown = null;
    minutesOnControl(null);
    if (res.kind === 'closest') {
      out.innerHTML = `<div class="st-none"><p>Nothing here on “${esc(q)}” itself yet. The closest ${res.ideas.length === 1 ? 'idea' : 'ideas'} so far:</p>
        <p class="st-chips">${res.ideas.map((r: any) => `<button type="button" class="st-chip" data-st-idea="${esc(r.id)}">${esc(r.name)}</button>`).join('')}</p>
        <p>If none of those is it, <a href="/search/">search inside every lesson</a> or <a href="/ideas/#every-idea">see every idea</a>.</p></div>`;
      say(`Nothing on ${q} itself yet. ${res.ideas.length} close ${res.ideas.length === 1 ? 'idea' : 'ideas'} offered.`);
    } else {
      out.innerHTML = `<div class="st-none"><p>Nothing here matches “${esc(q)}” yet. The site is all biology so far: chemistry, physics and math are not built.</p>
        <p>Try one word, like cells or energy. Or <a href="/search/">search inside every lesson</a>, or <a href="/ideas/#every-idea">see every idea</a>.</p></div>`;
      say('Nothing matches yet.');
    }
  }

  function openIdea(id: string, focus = true) {
    shown = { ids: [id], together: 1, prefer: [], others: [], typed: '' };
    draw(focus);
  }

  form.addEventListener('submit', (e) => { e.preventDefault(); ask(input.value); });
  input.addEventListener('focus', () => { loadMatcher().catch(() => {}); }, { once: true });
  levelSel.addEventListener('change', () => {
    level = levelSel.value ? LEVEL_KEYS.indexOf(levelSel.value) : -1;
    writePrefs({ level: levelSel.value || null });
    draw(false);
  });
  radios.forEach((r) => r.addEventListener('change', () => {
    if (!r.checked) return;
    time = r.value;
    writePrefs({ time });
    draw(false);
  }));
  document.addEventListener('click', (e) => {
    const t = (e.target as HTMLElement | null)?.closest<HTMLElement>('[data-st-try], [data-st-idea]');
    if (!t) return;
    if (t.dataset.stTry) { input.value = t.dataset.stTry; ask(input.value); return; }
    if (t.dataset.stIdea) { input.value = ''; openIdea(t.dataset.stIdea); }
  });

  // ?idea=<id>: a link from another page straight to an idea's path.
  const preset = new URLSearchParams(location.search).get('idea');
  if (preset && /^[a-z0-9]+(-[a-z0-9]+)*$/.test(preset)) openIdea(preset, false);
}
