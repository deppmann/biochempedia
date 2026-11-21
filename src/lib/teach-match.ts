/* The teacher's syllabus matcher, in the browser (/teach/match/).

   Reads the pasted text or a local file, matches it with src/lib/syllabus-match.mjs and draws the
   rows. The only requests it makes are GETs for the site's own static index files. The syllabus
   text is never part of any request, never put in the address and never stored.

   "Add ticked lessons to a class" is OFF (ADD_TO_CLASS below). When it is on, pressing it asks the
   classes API who is signed in, reads that class's assignments and sends the list back with the
   ticked lesson slugs added: still never the syllabus. */
import { buildMatcher, matchSyllabus, LEVEL_AT, LEVEL_CLASS } from './syllabus-match.mjs';
import { mergeAssignments } from './syllabus-assign.mjs';
import { docxText } from './docx-text.mjs';
import { LEVEL_SHORT, LEVEL_KEYS, andList, inSentence, gapLine } from './hop-words.mjs';
import { readPrefs } from './prefs';

/* OFF until it has been tried on a real class: it has not yet run against the live server, and it
   reads a class's list and writes it back, so an edit made in another tab in between would be lost.
   Copy and Print do not depend on it. */
export const ADD_TO_CLASS = false;

type Matcher = ReturnType<typeof buildMatcher>;
interface Lesson { slug: string; title: string; rank: number; ideas?: string[]; main?: boolean }
interface Info { course: string; film?: { href: string; sec: number; title: string }; adds: Map<string, string> }

const esc = (s: unknown) => String(s ?? '').replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;').replace(/"/g, '&quot;');
const json = (url: string) => fetch(url).then((r) => { if (!r.ok) throw new Error(url); return r.json(); });
const mmss = (s: number) => `${Math.floor(s / 60)}:${String(Math.round(s) % 60).padStart(2, '0')}`;
const count = (n: number, one: string, many: string) => `${n} ${n === 1 ? one : many}`;
const MAX_CHARS = 200000;

let matcherP: Promise<Matcher> | undefined;
const loadMatcher = () => (matcherP ??= Promise.all([json('/graph.json'), json('/ideas/lessons.json'), json('/start/lessons.json')])
  .then(([g, l, x]) => buildMatcher(g, l, x)).catch((e) => { matcherP = undefined; throw e; }));
let infoP: Promise<Map<string, Info>> | undefined;
/** Each lesson's course, first film and "what this level adds" notes. Bigger, so it is fetched after the rows are drawn. */
const loadInfo = () => (infoP ??= json('/graph/all.json').then((all) => {
  const info = new Map<string, Info>();
  all.lessons.forEach(([slug, , ci]: [string, string, number]) => info.set(slug, { course: all.courses[ci][1], adds: new Map() }));
  for (const [, title, li, sec, fid] of all.films as [string, string, number, number, string | 0][]) {
    const slug = all.lessons[li][0];
    const it = info.get(slug)!;
    if (!it.film || !fid) it.film = { href: `/watch/${slug}/${fid ? `${fid}/` : ''}`, sec, title };
  }
  for (const c of all.concepts) for (const r of c.r) if (r[1] === 0 && r[2]) info.get(all.lessons[r[0]][0])?.adds.set(c.id, r[2]);
  return info;
}).catch((e) => { infoP = undefined; throw e; }));

export function start() {
  const root = document.querySelector<HTMLElement>('[data-tm]');
  if (!root) return;
  const $ = <T extends HTMLElement>(s: string) => root.querySelector<T>(s)!;
  const text = $<HTMLTextAreaElement>('#tm-text');
  const levelSel = $<HTMLSelectElement>('[data-tm-level]');
  const goBtn = $<HTMLButtonElement>('[data-tm-go]');
  const sampleBtn = $<HTMLButtonElement>('[data-tm-sample]');
  const file = $<HTMLInputElement>('[data-tm-file]');
  const fileErr = $('[data-tm-file-err]');
  const status = $('[data-tm-status]');
  const result = $('[data-tm-result]');
  const rowsEl = $('[data-tm-rows]');
  const msg = $('[data-tm-msg]');
  const box = $('[data-tm-assign-box]');
  const elsewhere = $('[data-tm-elsewhere]');

  // The level the visitor already chose on this device is the starting guess; this page does not change it.
  const saved = LEVEL_KEYS.indexOf(readPrefs().level ?? '');
  if (saved >= 0) levelSel.value = String(saved);

  let last: { res: ReturnType<typeof matchSyllabus>; level: number; m: Matcher; typed: string } | null = null;
  let info: Map<string, Info> | null = null;
  // What the teacher changed by hand, kept while the text stays the same: a level change must not undo it.
  const unticked = new Set<string>(), ticked = new Set<string>();
  /** Said aloud and shown while working; after a match the summary says it, so the line is kept for screen readers only. */
  const say = (t: string, quiet = false) => { status.textContent = t; status.classList.toggle('tm-sr', quiet); };

  // ---- a local file: read here, never uploaded ----
  const cannot = 'That file could not be read here. Open it, copy the schedule and paste it in the box.';
  file.addEventListener('change', async () => {
    fileErr.textContent = '';
    say('');
    const f = file.files?.[0];
    if (!f) return;
    // Never over a teacher's own text.
    if (text.value.trim()) { fileErr.textContent = 'The box already has text in it. Clear the box first, then open the file.'; file.value = ''; return; }
    const name = f.name.toLowerCase();
    try {
      let got: string | null;
      if (name.endsWith('.docx')) got = await docxText(await f.arrayBuffer());
      else if (name.endsWith('.pdf') || f.type === 'application/pdf') { fileErr.textContent = 'This page cannot read a PDF yet. Open the PDF, select the schedule, copy it and paste it in the box.'; file.value = ''; return; }
      else if (/\.(doc|pages|rtf|odt)$/.test(name)) got = null;
      else got = await f.text();
      if (!got || !got.trim() || /\u0000/.test(got.slice(0, 2000))) { fileErr.textContent = cannot; file.value = ''; return; }
      text.value = got.slice(0, MAX_CHARS);
      say(`${f.name} was read on this computer. Check the text, then press Find matching lessons.`);
      text.focus();
    } catch { fileErr.textContent = cannot; }
    file.value = '';
  });
  sampleBtn.addEventListener('click', () => {
    // Never over a teacher's own text.
    if (text.value.trim()) { say('The sample would replace what is in the box. Clear the box first if you want to try it.'); text.focus(); return; }
    text.value = JSON.parse(document.querySelector('[data-tm-sample-text]')?.textContent || '""');
    match(true);
  });

  // ---- drawing ----
  let rowN = 0, rowTopic = '';
  const isTicked = (slug: string, dflt: boolean) => (ticked.has(slug) ? true : unticked.has(slug) ? false : dflt);
  const lessonRow = (l: Lesson, dflt: boolean, m: Matcher, tag = 'at', note = '') => {
    const i = info?.get(l.slug);
    const min = m.minutes[l.slug]?.[0];
    const facts = [LEVEL_SHORT[l.rank], i?.course, min ? `${min} min` : ''].filter(Boolean).map(esc);
    if (i?.film) facts.push(`<a class="tm-film" href="${esc(i.film.href)}" aria-label="film ${mmss(i.film.sec)}: ${esc(i.film.title)}">film ${mmss(i.film.sec)}</a>`);
    const id = `tm-${rowN}-${tag}-${l.slug}`;
    const adds = (l.ideas ?? []).map((x) => i?.adds.get(x)).find(Boolean);
    return `<li class="tm-lesson"><input type="checkbox" id="${esc(id)}" aria-describedby="${esc(id)}-f" data-tm-pick="${esc(l.slug)}" data-title="${esc(l.title)}" data-level="${esc(LEVEL_SHORT[l.rank])}" data-min="${min ?? ''}"${isTicked(l.slug, dflt) ? ' checked' : ''} autocomplete="off" />
      <div><label for="${esc(id)}">${esc(l.title)}</label>
      <span class="tm-facts"><span id="${esc(id)}-f">${facts.filter((f) => !f.startsWith('<a')).join(' · ')}${note ? ` · ${note}` : ''}</span>${facts.filter((f) => f.startsWith('<a')).map((f) => ` · ${f}`).join('')}<span class="tm-openwrap"> · <a class="tm-open" href="/lessons/${esc(l.slug)}/" target="_blank" rel="noopener" aria-label="Open ${esc(l.title)} in a new tab">open</a></span></span>
      <span class="tm-url">${esc(location.host)}/lessons/${esc(l.slug)}/</span>${adds ? `<span class="tm-adds">${esc(adds)}</span>` : ''}</div></li>`;
  };
  const group = (label: string, items: string) => `<ul class="tm-lessons" aria-label="${esc(`${label}: ${rowTopic}`)}">${items}</ul>`;

  function draw() {
    if (!last) return;
    const { res, level, m } = last;
    const nameOf = (id: string) => inSentence(id, m.byId.get(id)?.label ?? id);
    let here = 0, away = 0, nothing = 0;
    const best = new Array(7).fill(0);
    rowsEl.innerHTML = res.rows.map((row: any) => {
      rowN = row.n; rowTopic = row.topic;
      const head = `<h3 class="tm-topic">${esc(row.raw)}</h3>`;
      // Housekeeping is shown as written and left alone.
      if (row.kind === 'admin') return `<li class="tm-rowi tm-admin">${head}</li>`;
      if (!row.ideas.length) {
        nothing++;
        const maybe = row.maybe.map((x: any) => {
          const ls: Lesson[] = [...x.at, ...(x.at.length ? [] : [...x.down, ...x.up])].slice(0, 2);
          return ls.length ? `<div class="tm-maybe"><p class="tm-side">It might fit <a href="/ideas/${esc(x.id)}/">${esc(x.name)}</a> <span>not ticked</span></p>${group(`Might fit, ${x.name}`, ls.map((l) => lessonRow({ ...l, ideas: [x.id] }, false, m, 'maybe')).join(''))}</div>` : '';
        }).join('');
        // "Nothing on the site" would be a claim this page cannot check, so it says only what it knows.
        return `<li class="tm-rowi tm-nothing">${head}<p class="tm-none">${maybe ? 'Not sure about this line.' : 'No sure match for this line.'}</p>${maybe}</li>`;
      }
      const L = row.lessons;
      if (L.at.length) here++; else away++;
      for (const r of new Set<number>(row.ideas.flatMap((x: any) => (m.byId.get(x.id)?.lessons ?? []).map((l: Lesson) => l.rank)))) best[r] = (best[r] ?? 0) + 1;
      const ideas = `<p class="tm-ideah">Matched to ${row.ideas.map((x: any) => `<a href="/ideas/${esc(x.id)}/">${esc(x.name)}</a>`).join(', ')}</p>`;
      const missing = L.missing.length ? `<p class="tm-none">${esc(gapLine(andList(L.missing.map(nameOf)), [level]))}</p>` : '';
      return `<li class="tm-rowi">${head}${ideas}
        ${L.at.length ? group('Lessons at your level', L.at.map((l: Lesson) => lessonRow(l, !!l.main, m, 'at', l.main ? '' : 'teaches it along the way, so not ticked')).join('')) : ''}${missing}
        ${L.down.length ? `<p class="tm-side">For review, simpler</p>${group('For review, simpler', L.down.map((l: Lesson) => lessonRow(l, false, m, 'down')).join(''))}` : ''}
        ${L.up.length ? `<p class="tm-side">For stretch, deeper</p>${group('For stretch, deeper', L.up.map((l: Lesson) => lessonRow(l, false, m, 'up')).join(''))}` : ''}</li>`;
    }).join('');

    const at = LEVEL_AT[level];
    const parts = [
      here ? `${count(here, 'has', 'have')} a lesson ${at}` : `none has a lesson ${at}`,
      away ? `${count(away, 'is', 'are')} taught here only at other levels, shown unticked as simpler or deeper` : '',
      nothing ? `for ${nothing} I found no sure match` : '',
    ].filter(Boolean);
    $('[data-tm-sum]').textContent = res.topics
      ? `I read ${count(res.topics, 'topic', 'topics')} for ${LEVEL_CLASS[level]}: ${parts.join('; ')}. Lessons whose main idea is your topic are ticked. Untick any you will not use.`
      : 'No topics were found in that text. Paste the part of the syllabus that lists topics by week or by day, one per line.';
    // When most of the syllabus is taught at another level, say so once and offer it.
    const top = best.indexOf(Math.max(...best));
    const show = res.topics > 0 && top !== level && best[top] >= Math.max(3, here * 2) && away > here;
    elsewhere.hidden = !show;
    elsewhere.innerHTML = show ? `Most of these topics are taught here ${esc(LEVEL_AT[top])}. <button type="button" class="tm-linkbtn" data-tm-level-to="${top}">Show the lessons ${esc(LEVEL_AT[top])}</button>` : '';
    const sk = $<HTMLDetailsElement>('[data-tm-skipped]');
    sk.hidden = !res.skipped.length;
    sk.querySelector('summary')!.textContent = `${count(res.skipped.length, 'line was', 'lines were')} left out as course information, not topics`;
    sk.querySelector('ul')!.innerHTML = res.skipped.map((l: string) => `<li>${esc(l)}</li>`).join('');
    result.hidden = false;
    // With no topics there is nothing to copy or print, and no heading to give it.
    $('[data-tm-tools]').hidden = !res.topics;
    $('[data-tm-h]').hidden = !res.topics;
  }

  /** Match what is in the box. `focus`: move to the results (a press of the button), or stay put (a level change). */
  async function match(focus: boolean) {
    const typed = text.value.slice(0, MAX_CHARS);
    if (!typed.trim()) { say('Paste your syllabus in the box first, or press Try a sample.'); text.focus(); return; }
    say('Matching on this computer…');
    try {
      const m = await loadMatcher();
      const level = Number(levelSel.value);
      if (!last || last.typed !== typed) { ticked.clear(); unticked.clear(); }
      last = { res: matchSyllabus(m, typed, level), level, m, typed };
      draw();
      box.hidden = true; msg.textContent = '';
      say(last.res.topics ? `Done. ${count(last.res.matched, 'topic', 'topics')} matched ${LEVEL_AT[level]} or at another level.` : 'No topics were found in that text.', true);
      if (focus) (last.res.topics ? $('[data-tm-h]') : $('[data-tm-sum]')).focus();
      // Courses, films and the note on what each level adds arrive after the rows; ticks are kept.
      if (!info) loadInfo().then((got) => {
        info = got;
        // The rows are rebuilt with the extra facts: whoever is already in the list stays where they were.
        const at = document.activeElement instanceof HTMLElement && rowsEl.contains(document.activeElement) ? document.activeElement.id : '';
        draw();
        if (at) document.getElementById(at)?.focus({ preventScroll: true });
      }).catch(() => {});
    } catch {
      say('The list of lessons did not load. Check your connection and press the button again. Your syllabus is still in the box.');
    }
  }
  goBtn.addEventListener('click', () => match(true));
  levelSel.addEventListener('change', () => { if (last && text.value.trim()) match(false); });
  elsewhere.addEventListener('click', (e) => {
    const b = (e.target as HTMLElement).closest<HTMLElement>('[data-tm-level-to]');
    if (!b) return;
    levelSel.value = b.dataset.tmLevelTo!;
    match(false).then(() => $('[data-tm-h]').focus());
  });
  text.addEventListener('focus', () => { loadMatcher().catch(() => {}); }, { once: true });

  // ---- what is ticked ----
  const picked = () => {
    const seen = new Set<string>();
    return Array.from(rowsEl.querySelectorAll<HTMLInputElement>('[data-tm-pick]:checked')).filter((c) => (seen.has(c.dataset.tmPick!) ? false : (seen.add(c.dataset.tmPick!), true)));
  };
  // The same lesson can sit under two topics: ticking one ticks the other.
  rowsEl.addEventListener('change', (e) => {
    const t = e.target as HTMLInputElement;
    const slug = t.dataset?.tmPick;
    if (!slug) return;
    rowsEl.querySelectorAll<HTMLInputElement>(`[data-tm-pick="${CSS.escape(slug)}"]`).forEach((c) => { c.checked = t.checked; });
    (t.checked ? ticked : unticked).add(slug);
    (t.checked ? unticked : ticked).delete(slug);
    msg.textContent = '';
    const send = box.querySelector<HTMLElement>('[data-tm-send]');
    if (send) send.textContent = `Add ${count(picked().length, 'lesson', 'lessons')} to this class`;
  });

  function listText(): string {
    const lines: string[] = [];
    rowsEl.querySelectorAll<HTMLElement>('.tm-rowi').forEach((li) => {
      lines.push(li.querySelector('.tm-topic')?.textContent ?? '');
      const mine = Array.from(li.querySelectorAll<HTMLInputElement>('[data-tm-pick]:checked'));
      if (li.classList.contains('tm-admin')) { /* the line alone */ }
      else if (!mine.length) lines.push(li.classList.contains('tm-nothing') ? '  (no sure match on STEMhop)' : '  (no lesson chosen)');
      for (const c of mine) lines.push(`  - ${c.dataset.title} (${c.dataset.level}${c.dataset.min ? `, ${c.dataset.min} min` : ''}) ${location.origin}/lessons/${c.dataset.tmPick}/`);
    });
    return lines.join('\n');
  }
  $('[data-tm-copy]').addEventListener('click', async () => {
    const t = listText();
    try { await navigator.clipboard.writeText(t); msg.textContent = 'Copied. Paste it into your own syllabus or an email.'; }
    catch {
      // No clipboard permission: put the text where it can be copied by hand.
      box.hidden = false;
      box.innerHTML = '<label class="tm-label" for="tm-copy-text">Select all of this and copy it</label><textarea id="tm-copy-text" rows="10" readonly></textarea>';
      const ta = box.querySelector('textarea')!; ta.value = t; ta.focus(); ta.select();
    }
  });
  $('[data-tm-print]').addEventListener('click', () => window.print());

  // ---- add to a class (OFF): the one step that talks to the server, and only when pressed ----
  const assignBtn = $<HTMLButtonElement>('[data-tm-assign]');
  /** Every outcome is written into the box, which is a status region, and takes focus so the next Tab starts there. */
  const tell = (html: string) => { box.hidden = false; box.innerHTML = html; box.focus(); };
  const api = async (path: string, body?: unknown, method = 'GET') => {
    try {
      const r = await fetch(path, { method, credentials: 'same-origin', headers: method === 'GET' ? {} : { 'Content-Type': 'application/json' }, body: method === 'GET' ? undefined : JSON.stringify(body) });
      return { ok: r.ok, status: r.status, data: await r.json().catch(() => ({})) as any };
    } catch { return { ok: false, status: 0, data: {} as any }; }
  };
  if (ADD_TO_CLASS) {
    assignBtn.hidden = false;
    assignBtn.addEventListener('click', async () => {
      const slugs = picked().map((c) => c.dataset.tmPick!);
      if (!slugs.length) return tell('<p>Tick at least one lesson first.</p>');
      tell('<p>Checking your classes…</p>');
      const me = await api('/api/teacher/me');
      if (me.status === 401) return tell('<p>Adding to a class needs a teacher account. <a href="/teach/" target="_blank" rel="noopener">Sign in or make one in a new tab</a>, then come back here and press the button again. Your list stays on this page.</p>');
      if (!me.ok) return tell('<p>Your classes could not be reached just now. The list above still works: copy or print it.</p>');
      const classes: { id: string; name: string }[] = me.data.classes ?? [];
      if (!classes.length) return tell('<p>You have no class yet. <a href="/teach/classes/" target="_blank" rel="noopener">Make one in a new tab</a>, then press the button again.</p>');
      tell(`<label class="tm-level">Which class?<select data-tm-class>${classes.map((c) => `<option value="${esc(c.id)}">${esc(c.name)}</option>`).join('')}</select></label>
        <button class="tc-btn" type="button" data-tm-send>Add ${count(slugs.length, 'lesson', 'lessons')} to this class</button>
        <p class="tm-quiet">Only the ticked lessons are sent, not your syllabus. They join what is already assigned, with no due date; nothing already assigned changes. Students in the class will see them. If the class page is open in another tab, reload it before you change assignments there.</p><p class="tc-error" data-tm-send-err role="alert"></p>`);
      box.querySelector<HTMLSelectElement>('[data-tm-class]')?.focus();
      box.querySelector('[data-tm-send]')!.addEventListener('click', async (ev) => {
        const btn = ev.currentTarget as HTMLButtonElement;
        if (btn.getAttribute('aria-disabled') === 'true') return;
        const id = box.querySelector<HTMLSelectElement>('[data-tm-class]')!.value;
        const err = box.querySelector<HTMLElement>('[data-tm-send-err]')!;
        btn.setAttribute('aria-disabled', 'true');
        const brief = await api(`/api/classes/${encodeURIComponent(id)}/brief`);
        if (!brief.ok || !Array.isArray(brief.data.assignments)) { err.textContent = 'That class could not be read. Nothing was changed.'; btn.removeAttribute('aria-disabled'); return; }
        const merged = mergeAssignments(brief.data.assignments, picked().map((c) => c.dataset.tmPick!));
        if (!merged.added.length) return tell('<p>Those lessons are already assigned to that class. Nothing was changed.</p>');
        const put = await api(`/api/classes/${encodeURIComponent(id)}/assignments`, { assignments: merged.list }, 'PUT');
        if (!put.ok) { err.textContent = put.data.error || 'Could not save. Nothing was changed.'; btn.removeAttribute('aria-disabled'); return; }
        const name = classes.find((c) => c.id === id)?.name ?? 'the class';
        tell(`<p class="tc-ok">Added ${count(merged.added.length, 'lesson', 'lessons')} to ${esc(name)}${merged.already.length ? `; ${merged.already.length} were already assigned` : ''}${merged.dropped.length ? `; ${merged.dropped.length} did not fit (a class holds 400)` : ''}. <a href="/teach/class/?id=${encodeURIComponent(id)}&tab=assign">Open the class to set due dates</a></p>`);
      });
    });
  }

  // The page is live: switch on what the script drives.
  goBtn.disabled = false; sampleBtn.disabled = false; file.disabled = false;
}
