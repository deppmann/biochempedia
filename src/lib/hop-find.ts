/* Find an idea, in the browser: fetches the two small index files once, searches as the reader
   types and draws the results. The ranking is src/lib/hop-search.mjs; the words and the strip are
   src/lib/hop-words.mjs, the same ones the static pages use. Nothing is stored and nothing about
   the query is sent anywhere: the address gains ?q= only so the result can be shared. */
import { buildIndex, search } from './hop-search.mjs';
import { ranksOf, LEVEL_SHORT, gapLine, inSentence } from './hop-words.mjs';
import { ladderHtml, ladderGlyph, wireLadders } from './hop-ladder.mjs';

type Index = ReturnType<typeof buildIndex>;
const esc = (s: unknown) => String(s).replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;').replace(/"/g, '&quot;');

let indexP: Promise<Index> | undefined;
const loadIndex = () => (indexP ??= Promise.all([
  fetch('/graph.json').then((r) => r.json()),
  fetch('/ideas/lessons.json').then((r) => r.json()).catch(() => null),
]).then(([g, extra]) => buildIndex(g, extra)).catch((e) => { indexP = undefined; throw e; }));
const areaCache = new Map<string, Promise<any>>();
const loadArea = (id: string) => { if (!areaCache.has(id)) areaCache.set(id, fetch(`/graph/${id}.json`).then((r) => r.json())); return areaCache.get(id)!; };

function whyLine(w: { kind: string; text: string; code?: string }): string {
  switch (w.kind) {
    case 'phrase': return `Matches “${esc(w.text)}”`;
    case 'lesson': return `In the lesson “${esc(w.text)}”`;
    case 'unit': return `In the unit “${esc(w.text)}”`;
    case 'code': return `Virginia ${esc(w.code ?? '')}, in the lesson “${esc(w.text)}”`;
    default: return '';
  }
}

/** One result. The level words link to that level's first lesson. */
function row(index: Index, r: ReturnType<typeof search>['results'][number], level: number): string {
  const it = index.ideas.find((x: any) => x.id === r.id)!;
  const ranks = ranksOf(it.mask);
  const at = ranks.map((rank) => {
    const l = it.lessons.find((x: any) => x.rank === rank);
    return l ? `<a href="/lessons/${esc(l.slug)}/" aria-label="${esc(LEVEL_SHORT[rank])}: ${esc(l.title)}">${esc(LEVEL_SHORT[rank])}</a>` : esc(LEVEL_SHORT[rank]);
  });
  let pref = '';
  if (level >= 0 && ranks.length && !ranks.includes(level)) {
    const below = [...it.lessons].reverse().find((x: any) => x.rank < level);
    pref = `<p class="ideas-res-why">${esc(gapLine('this idea', [level]))}${below ? ` The nearest simpler lesson is <a href="/lessons/${esc(below.slug)}/">${esc(below.title)}</a> (${esc(LEVEL_SHORT[below.rank])}).` : ''}</p>`;
  }
  const why = whyLine(r.why as any);
  return `<li class="ideas-res" data-idea="${esc(r.id)}">
    <h3 class="ideas-res-name">${ladderGlyph(it.mask, { here: level >= 0 && ranks.includes(level) ? level : null })}<a href="/ideas/${esc(r.id)}/">${esc(it.name)}</a></h3>
    ${why ? `<p class="ideas-res-why">${why}</p>` : ''}
    <p class="ideas-res-blurb">${esc(it.blurb)}</p>
    <p class="ideas-res-at">${ranks.length === 1 ? 'Taught at one level so far' : 'Taught at'}: ${at.join(' · ')}.</p>
    ${pref}
    <div data-idea-rungs></div>
  </li>`;
}

/** The best match, opened: its ladder, with what each level adds (one area file). */
async function openRungs(index: Index, id: string, host: Element, level: number, still: () => boolean) {
  const it = index.ideas.find((x: any) => x.id === id)!;
  const area = index.areas[it.area]?.[0];
  if (!area) return;
  let g: any;
  try { g = await loadArea(area); } catch { return; }
  if (!still()) return;
  const c = g.concepts.find((x: any) => x.id === id);
  if (!c) return;
  const stageOf = (li: number) => g.courses[g.lessons[li][2]][2] as number;
  const filmOf = new Map<number, any[]>();
  for (const fi of c.f) { const f = g.films[fi]; if (!filmOf.has(f[2])) filmOf.set(f[2], f); }
  const rungs = c.r.filter((x: any[]) => x[1] === 0).map((x: any[]) => {
    const [slug, title, ci] = g.lessons[x[0]];
    const f = filmOf.get(x[0]);
    return {
      slug, title, rank: stageOf(x[0]), courseTitle: g.courses[ci][1], adds: x[2] || undefined,
      href: `/lessons/${slug}/${x[3] ? `#${x[3]}` : ''}`,
      ...(f ? { film: { href: `/watch/${slug}/${f[4] ? `${f[4]}/` : ''}`, seconds: f[3], title: f[1] } } : {}),
    };
  });
  host.innerHTML = `${ladderHtml({ id, name: it.name, short: inSentence(id, it.name), rungs }, { hereRank: level >= 0 ? level : null, hereLabel: 'the level you chose', hex: true, window: false })}<p class="ideas-res-more"><a href="/ideas/${esc(id)}/">${esc(it.name)}: films, ideas next door and the rest</a></p>`;
  wireLadders(host);
}

export function start() {
  const form = document.querySelector<HTMLFormElement>('[data-ideas-form]');
  const input = document.querySelector<HTMLInputElement>('#ideas-q');
  const outEl = document.querySelector<HTMLElement>('[data-ideas-out]');
  const statusEl = document.querySelector<HTMLElement>('[data-ideas-status]');
  if (!form || !input || !outEl || !statusEl) return;
  const out: HTMLElement = outEl, status: HTMLElement = statusEl;

  let level = -1;
  try { level = ['ages-5-10', 'grade-7', 'high-school', 'starting-college', 'college-core', 'college-further', 'graduate'].indexOf(JSON.parse(localStorage.getItem('stemhop:prefs:v1') ?? 'null')?.level); } catch { /* none */ }

  let run = 0, sayTimer = 0;
  // The status line is for screen readers as much as for eyes: say it once typing has stopped.
  const say = (text: string) => { clearTimeout(sayTimer); sayTimer = window.setTimeout(() => { status.textContent = text; }, 500); };

  async function go(q: string, push: boolean) {
    const mine = ++run;
    const typed = q.trim();
    if (push) {
      try { history.replaceState(null, '', typed ? `/ideas/?q=${encodeURIComponent(typed)}` : '/ideas/'); } catch { /* the search still runs */ }
    }
    if (!typed) { out.innerHTML = ''; clearTimeout(sayTimer); status.textContent = ''; return; }
    let index: Index;
    try { index = await loadIndex(); } catch {
      if (mine === run) { out.innerHTML = `<p class="ideas-none">The list of ideas did not load. Check your connection and try again, or pick an idea from the areas below.</p>`; say('The list of ideas did not load.'); }
      return;
    }
    if (mine !== run) return;
    const res = search(index, typed);
    if (!res.results.length) {
      out.innerHTML = `<p class="ideas-none">Nothing here matches “${esc(typed)}” yet. The ideas so far are all biology. Try one word, like cells or energy, pick an idea from the areas below, or <a href="/search/?q=${encodeURIComponent(typed)}">search the whole site for “${esc(typed)}”</a>, which also looks inside the lessons.</p>`;
      say('No ideas match yet.');
      return;
    }
    const closest = res.results[0].closest;
    const head = res.code
      ? `<p class="ideas-closest">Ideas taught in lessons that carry Virginia ${esc((res.results[0].why as any).code ?? typed)}.</p>`
      : closest ? `<p class="ideas-closest">Closest ${res.results.length === 1 ? 'idea' : 'ideas'} so far. Nothing on “${esc(typed)}” itself yet. <a href="/search/?q=${encodeURIComponent(typed)}">Search inside the lessons</a></p>` : '';
    out.innerHTML = `${head}<h2 class="hop-vh">Ideas that match</h2><ol class="ideas-results">${res.results.map((r) => row(index, r, level)).join('')}</ol>`;
    say(closest ? `Nothing on ${typed} itself yet. ${res.results.length} close ${res.results.length === 1 ? 'idea' : 'ideas'} shown.` : `${res.results.length} ${res.results.length === 1 ? 'idea matches' : 'ideas match'}. First: ${res.results[0].name}.`);
    // The first row opens to its lessons when it is clearly the answer.
    const top = res.results[0];
    if (!closest && (top.score >= 70 || res.results.length === 1)) {
      const host = out.querySelector(`[data-idea="${CSS.escape(top.id)}"] [data-idea-rungs]`);
      if (host) openRungs(index, top.id, host, level, () => mine === run);
    }
  }

  let typeTimer = 0;
  input.addEventListener('input', () => { clearTimeout(typeTimer); typeTimer = window.setTimeout(() => go(input.value, true), 90); });
  input.addEventListener('focus', () => { loadIndex().catch(() => {}); }, { once: true });
  form.addEventListener('submit', (e) => { e.preventDefault(); clearTimeout(typeTimer); go(input.value, true); });
  document.querySelectorAll<HTMLAnchorElement>('[data-ideas-try]').forEach((a) => a.addEventListener('click', (e) => {
    e.preventDefault();
    input.value = a.dataset.ideasTry ?? '';
    go(input.value, true);
    input.focus();
  }));
  const preset = new URLSearchParams(location.search).get('q');
  if (preset) { input.value = preset; go(preset, false); }
}
