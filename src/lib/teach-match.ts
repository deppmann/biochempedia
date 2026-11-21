/* The teacher's syllabus matcher, in the browser (/teach/match/).

   Reads the pasted text or a local file, matches it with src/lib/syllabus-match.mjs and draws the
   rows. The only requests it makes are GETs for the site's own static index files, until the
   teacher presses "Add ticked lessons to a class": then it asks the classes API who is signed in,
   reads that class's assignments and sends the list back with the ticked lesson slugs added.
   The syllabus text is never part of any request, and is not stored. */
import { buildMatcher, matchSyllabus } from './syllabus-match.mjs';
import { mergeAssignments } from './syllabus-assign.mjs';
import { docxText } from './docx-text.mjs';
import { LEVEL_SHORT, LEVEL_LABEL, LEVEL_KEYS, andList, inSentence } from './hop-words.mjs';
import { readPrefs } from './prefs';

type Matcher = ReturnType<typeof buildMatcher>;
interface Lesson { slug: string; title: string; rank: number }
interface Info { course: string; film?: { href: string; sec: number }; adds: Map<string, string> }

const esc = (s: unknown) => String(s ?? '').replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;').replace(/"/g, '&quot;');
const json = (url: string) => fetch(url).then((r) => { if (!r.ok) throw new Error(url); return r.json(); });
const mmss = (s: number) => `${Math.floor(s / 60)}:${String(Math.round(s) % 60).padStart(2, '0')}`;
const MAX_CHARS = 200000;

let dataP: Promise<{ m: Matcher; info: Map<string, Info> }> | undefined;
/** The matcher, plus each lesson's course, first film and "what this level adds" notes (from /graph/all.json). */
const load = () => (dataP ??= Promise.all([json('/graph.json'), json('/ideas/lessons.json'), json('/start/lessons.json'), json('/graph/all.json')]).then(([g, l, x, all]) => {
  const info = new Map<string, Info>();
  all.lessons.forEach(([slug, , ci]: [string, string, number]) => info.set(slug, { course: all.courses[ci][1], adds: new Map() }));
  for (const [, , li, sec, fid] of all.films as [string, string, number, number, string | 0][]) {
    const slug = all.lessons[li][0];
    const it = info.get(slug)!;
    if (!it.film || !fid) it.film = { href: `/watch/${slug}/${fid ? `${fid}/` : ''}`, sec };
  }
  for (const c of all.concepts) for (const r of c.r) if (r[1] === 0 && r[2]) info.get(all.lessons[r[0]][0])?.adds.set(c.id, r[2]);
  return { m: buildMatcher(g, l, x), info };
}).catch((e) => { dataP = undefined; throw e; }));

export function start() {
  const root = document.querySelector<HTMLElement>('[data-tm]');
  if (!root) return;
  const $ = <T extends HTMLElement>(s: string) => root.querySelector<T>(s)!;
  const form = $<HTMLFormElement>('[data-tm-form]');
  const text = $<HTMLTextAreaElement>('#tm-text');
  const levelSel = $<HTMLSelectElement>('[data-tm-level]');
  const file = $<HTMLInputElement>('[data-tm-file]');
  const fileErr = $('[data-tm-file-err]');
  const status = $('[data-tm-status]');
  const result = $('[data-tm-result]');
  const rowsEl = $('[data-tm-rows]');
  const msg = $('[data-tm-msg]');
  const box = $('[data-tm-assign-box]');

  // The level the visitor already chose on this device is the starting guess; this page does not change it.
  const saved = LEVEL_KEYS.indexOf(readPrefs().level ?? '');
  if (saved >= 0) levelSel.value = String(saved);

  let last: { res: ReturnType<typeof matchSyllabus>; level: number; m: Matcher; info: Map<string, Info> } | null = null;

  // ---- a local file: read here, never uploaded ----
  file.addEventListener('change', async () => {
    fileErr.textContent = '';
    const f = file.files?.[0];
    if (!f) return;
    const name = f.name.toLowerCase();
    try {
      let got: string | null;
      if (name.endsWith('.docx')) got = await docxText(await f.arrayBuffer());
      else if (name.endsWith('.pdf') || f.type === 'application/pdf') { fileErr.textContent = 'This page cannot read a PDF yet. Open the PDF, select the schedule, copy it and paste it into the box.'; file.value = ''; return; }
      else if (name.endsWith('.doc') || name.endsWith('.pages') || name.endsWith('.rtf') || name.endsWith('.odt')) got = null;
      else got = await f.text();
      if (!got || !got.trim() || /\u0000/.test(got.slice(0, 2000))) { fileErr.textContent = 'That file could not be read here. Open it, copy the schedule and paste it into the box.'; file.value = ''; return; }
      text.value = got.slice(0, MAX_CHARS);
      status.textContent = `${f.name} was read on this computer. Check the text, then press Match my syllabus.`;
      text.focus();
    } catch {
      fileErr.textContent = 'That file could not be read here. Open it, copy the schedule and paste it into the box.';
    }
    file.value = '';
  });
  $('[data-tm-sample]').addEventListener('click', () => {
    text.value = JSON.parse(document.querySelector('[data-tm-sample-text]')?.textContent || '""');
    form.requestSubmit();
  });

  // ---- drawing ----
  const lessonRow = (l: Lesson & { ideas?: string[] }, ticked: boolean, info: Map<string, Info>, m: Matcher, tag = 'at') => {
    const i = info.get(l.slug);
    const min = m.minutes[l.slug]?.[0];
    const facts = [LEVEL_SHORT[l.rank], i?.course, min ? `${min} min` : ''].filter(Boolean).map(esc);
    if (i?.film) facts.push(`<a href="${esc(i.film.href)}">film ${mmss(i.film.sec)}</a>`);
    const id = `tm-${rowN}-${tag}-${l.slug}`;
    const adds = (l.ideas ?? []).map((x) => i?.adds.get(x)).find(Boolean);
    return `<li class="tm-lesson"><input type="checkbox" id="${esc(id)}" data-tm-pick="${esc(l.slug)}" data-title="${esc(l.title)}" data-level="${esc(LEVEL_SHORT[l.rank])}" data-min="${min ?? ''}"${ticked ? ' checked' : ''} autocomplete="off" />
      <div><label for="${esc(id)}">${esc(l.title)}</label> <a class="tm-open" href="/lessons/${esc(l.slug)}/" target="_blank" rel="noopener" aria-label="Open ${esc(l.title)} in a new tab">open</a>
      <span class="tm-facts">${facts.join(' · ')}</span>${adds ? `<span class="tm-adds">${esc(adds)}</span>` : ''}</div></li>`;
  };
  let rowN = 0;

  function draw() {
    if (!last) return;
    const { res, level, m, info } = last;
    const here = LEVEL_SHORT[level];
    const nameOf = (id: string) => inSentence(id, m.byId.get(id)?.label ?? id);
    rowsEl.innerHTML = res.rows.map((row: any) => {
      rowN = row.n;
      const head = `<p class="tm-topic">${esc(row.raw)}</p>`;
      if (row.kind === 'admin') return `<li class="tm-rowi tm-admin">${head}<p class="tm-quiet">No topic to match on this line.</p></li>`;
      if (!row.ideas.length) {
        const maybe = row.maybe.map((x: any) => {
          const ls = [...x.at, ...(x.at.length ? [] : [...x.down, ...x.up])].slice(0, 2);
          return ls.length ? `<div class="tm-maybe"><p class="tm-side">Might fit: <a href="/ideas/${esc(x.id)}/">${esc(x.name)}</a> <span>not ticked, because the match is loose</span></p><ul class="tm-lessons">${ls.map((l: Lesson) => lessonRow({ ...l, ideas: [x.id] }, false, info, m, 'maybe')).join('')}</ul></div>` : '';
        }).join('');
        return `<li class="tm-rowi tm-nothing">${head}<p class="tm-none">Nothing on the site for this yet.</p>${maybe}</li>`;
      }
      const L = row.lessons;
      const ideas = `<p class="tm-ideah">Matched to ${row.ideas.map((x: any) => `<a href="/ideas/${esc(x.id)}/">${esc(x.name)}</a>`).join(', ')}</p>`;
      const missing = L.missing.length ? `<p class="tm-none">No lesson on ${esc(andList(L.missing.map(nameOf)))} at ${esc(here)} level yet.</p>` : '';
      return `<li class="tm-rowi">${head}${ideas}
        ${L.at.length ? `<ul class="tm-lessons">${L.at.map((l: Lesson) => lessonRow(l, true, info, m)).join('')}</ul>` : ''}${missing}
        ${L.down.length ? `<p class="tm-side">For review, one level simpler</p><ul class="tm-lessons">${L.down.map((l: Lesson) => lessonRow(l, false, info, m, 'down')).join('')}</ul>` : ''}
        ${L.up.length ? `<p class="tm-side">For stretch, one level deeper</p><ul class="tm-lessons">${L.up.map((l: Lesson) => lessonRow(l, false, info, m, 'up')).join('')}</ul>` : ''}</li>`;
    }).join('');
    const none = res.topics - res.matched;
    $('[data-tm-sum]').textContent = res.topics
      ? `${res.topics} ${res.topics === 1 ? 'topic' : 'topics'} read from your syllabus, for a ${LEVEL_LABEL[level].toLowerCase()} class. ${res.matched} matched${none ? `; for ${none} the site has nothing yet, or the match was not sure enough to show` : ''}. Lessons at your level are ticked. Untick what you will not use.`
      : 'No topics were found in that text. Paste the part of the syllabus that lists topics by week or by day, one per line.';
    const sk = $<HTMLDetailsElement>('[data-tm-skipped]');
    sk.hidden = !res.skipped.length;
    sk.querySelector('summary')!.textContent = `${res.skipped.length} ${res.skipped.length === 1 ? 'line was' : 'lines were'} left out as course information, not topics`;
    sk.querySelector('ul')!.innerHTML = res.skipped.map((l: string) => `<li>${esc(l)}</li>`).join('');
    result.hidden = false;
    box.hidden = true;
    msg.textContent = '';
  }

  form.addEventListener('submit', async (e) => {
    e.preventDefault();
    const typed = text.value.slice(0, MAX_CHARS);
    if (!typed.trim()) { status.textContent = 'Paste your syllabus in the box first, or press Try a sample.'; text.focus(); return; }
    status.textContent = 'Matching on this computer…';
    try {
      const { m, info } = await load();
      const level = Number(levelSel.value);
      last = { res: matchSyllabus(m, typed, level), level, m, info };
      draw();
      status.textContent = `Matched ${last.res.matched} of ${last.res.topics} topics.`;
      $('[data-tm-h]').focus();
    } catch {
      status.textContent = 'The list of lessons did not load. Check your connection and press the button again. Your syllabus is still in the box.';
    }
  });
  levelSel.addEventListener('change', () => { if (last && text.value.trim()) form.requestSubmit(); });

  // ---- what is ticked ----
  const picked = () => {
    const seen = new Set<string>();
    return Array.from(rowsEl.querySelectorAll<HTMLInputElement>('[data-tm-pick]:checked')).filter((c) => (seen.has(c.dataset.tmPick!) ? false : (seen.add(c.dataset.tmPick!), true)));
  };
  // The same lesson can sit under two topics: ticking one ticks the other.
  rowsEl.addEventListener('change', (e) => {
    const t = e.target as HTMLInputElement;
    if (!t.dataset?.tmPick) return;
    rowsEl.querySelectorAll<HTMLInputElement>(`[data-tm-pick="${CSS.escape(t.dataset.tmPick)}"]`).forEach((c) => { c.checked = t.checked; });
    msg.textContent = '';
  });

  function listText(): string {
    const lines: string[] = [];
    rowsEl.querySelectorAll<HTMLElement>('.tm-rowi').forEach((li) => {
      lines.push(li.querySelector('.tm-topic')?.textContent ?? '');
      const mine = Array.from(li.querySelectorAll<HTMLInputElement>('[data-tm-pick]:checked'));
      if (li.classList.contains('tm-admin')) { /* the line alone */ }
      else if (!mine.length) lines.push(li.classList.contains('tm-nothing') ? '  (nothing on STEMhop for this yet)' : '  (no lesson chosen)');
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

  // ---- add to a class: the one step that talks to the server, and only when pressed ----
  const api = async (path: string, body?: unknown, method = 'GET') => {
    try {
      const r = await fetch(path, { method, credentials: 'same-origin', headers: method === 'GET' ? {} : { 'Content-Type': 'application/json' }, body: method === 'GET' ? undefined : JSON.stringify(body) });
      return { ok: r.ok, status: r.status, data: await r.json().catch(() => ({})) as any };
    } catch { return { ok: false, status: 0, data: {} as any }; }
  };
  $('[data-tm-assign]').addEventListener('click', async () => {
    const slugs = picked().map((c) => c.dataset.tmPick!);
    box.hidden = false;
    if (!slugs.length) { box.innerHTML = '<p class="tm-quiet">Tick at least one lesson first.</p>'; return; }
    box.innerHTML = '<p class="tm-quiet">Checking your classes…</p>';
    const me = await api('/api/teacher/me');
    if (me.status === 401) { box.innerHTML = '<p>Adding to a class needs a teacher account. <a href="/teach/" target="_blank" rel="noopener">Sign in or make one in a new tab</a>, then come back here and press the button again. Your list stays on this page.</p>'; return; }
    if (!me.ok) { box.innerHTML = '<p>Your classes could not be reached just now. The list above still works: copy or print it.</p>'; return; }
    const classes: { id: string; name: string }[] = me.data.classes ?? [];
    if (!classes.length) { box.innerHTML = '<p>You have no class yet. <a href="/teach/classes/" target="_blank" rel="noopener">Make one in a new tab</a>, then press the button again.</p>'; return; }
    box.innerHTML = `<label class="tm-level">Which class?<select data-tm-class>${classes.map((c) => `<option value="${esc(c.id)}">${esc(c.name)}</option>`).join('')}</select></label>
      <button class="tc-btn" type="button" data-tm-send>Add ${slugs.length} ${slugs.length === 1 ? 'lesson' : 'lessons'} to this class</button>
      <p class="tm-quiet">Only the ticked lessons are sent, not your syllabus. They join what is already assigned, with no due date; nothing already assigned changes. Students in the class will see them.</p><p class="tc-error" data-tm-send-err role="alert"></p>`;
    box.querySelector<HTMLSelectElement>('[data-tm-class]')?.focus();
    box.querySelector('[data-tm-send]')!.addEventListener('click', async (ev) => {
      const btn = ev.currentTarget as HTMLButtonElement;
      const id = box.querySelector<HTMLSelectElement>('[data-tm-class]')!.value;
      const err = box.querySelector<HTMLElement>('[data-tm-send-err]')!;
      btn.disabled = true;
      const brief = await api(`/api/classes/${encodeURIComponent(id)}/brief`);
      if (!brief.ok || !Array.isArray(brief.data.assignments)) { err.textContent = 'That class could not be read. Nothing was changed.'; btn.disabled = false; return; }
      const now = picked().map((c) => c.dataset.tmPick!);
      const merged = mergeAssignments(brief.data.assignments, now);
      if (!merged.added.length) { box.innerHTML = '<p>Those lessons are already assigned to that class. Nothing was changed.</p>'; return; }
      const put = await api(`/api/classes/${encodeURIComponent(id)}/assignments`, { assignments: merged.list }, 'PUT');
      if (!put.ok) { err.textContent = put.data.error || 'Could not save. Nothing was changed.'; btn.disabled = false; return; }
      const name = classes.find((c) => c.id === id)?.name ?? 'the class';
      box.innerHTML = `<p class="tc-ok">Added ${merged.added.length} ${merged.added.length === 1 ? 'lesson' : 'lessons'} to ${esc(name)}${merged.already.length ? `; ${merged.already.length} were already assigned` : ''}${merged.dropped.length ? `; ${merged.dropped.length} did not fit (a class holds 400)` : ''}. <a href="/teach/class/?id=${encodeURIComponent(id)}&tab=assign">Open the class to set due dates</a></p>`;
    });
  });
}
