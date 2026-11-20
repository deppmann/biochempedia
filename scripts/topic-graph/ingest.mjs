#!/usr/bin/env node
/**
 * Hop graph: take what the readers wrote and merge it into src/data/topic-graph.json.
 *
 * A staging folder holds the answers of each stage, one JSON file each:
 *   proposals/<slug>.json    stage 1: the ideas one lesson teaches (prompts.mjs proposePrompt)
 *   canonical/<area>.json    stage 2: one id per idea (canonicalizePrompt); canonical/_cross.json across areas
 *   near/<area>.json         stage 2b: sideways hops (nearPrompt)
 *   verify/<concept>.json    stage 4: the blind check (verifyPrompt)
 *   review/<name>.json       last: corrections by whoever read the result (a person, or the reader who
 *                            arbitrates). Applied after the verdicts, so it does not disturb them:
 *                            { by, concepts: [{ id, new: { name, blurb, area, aliases } }],
 *                              merge: [{ from, into, why }],
 *                              rungs: [{ id, lesson, role: core | uses | drop, anchor, adds, films, why }],
 *                              near: { <id>: [{ id, why }] }   (added to what the concept has) }
 * Every file and every item in it is checked against the lessons and the wording rules. A bad item
 * is rejected with its reason and the rest is kept; nothing is dropped silently. A rung the blind
 * check judged wrong is removed and logged, not argued with.
 *
 * The result is a pure function of the BASE graph and the staging files, in one fixed order, so a
 * rerun gives the same bytes. The base is the committed graph as it stood when the staging folder
 * was first ingested (saved as <staging>/base.json); a lesson's proposal replaces that lesson's
 * rungs, so the tool is also how one lesson is topped up later (assign.mjs).
 *
 *   node scripts/topic-graph/ingest.mjs --staging <dir>            merge and write the graph
 *   node scripts/topic-graph/ingest.mjs --staging <dir> --dry      report only, write nothing
 *   node scripts/topic-graph/ingest.mjs --graph <file>             import a graph-shaped file (a hand-written
 *                                                                  seed) through the same checks, onto an empty graph
 *   options: --out <file> (default src/data/topic-graph.json), --base <file>, --max-uses <n>,
 *            --no-canonical / --no-near / --no-verify (stop before that stage), --date YYYY-MM-DD
 *
 * Exit 0 when the graph was written (rejected items are in the report), 1 when the merged graph
 * would break a rule (nothing is written), 2 for a usage error. Calls no model.
 *
 * Two ids with one name are an error in any run that writes. In a --dry run before the canonicalize
 * stage has answered (--no-canonical, or no canonical file yet) they are a warning, because giving
 * each idea one id is that stage's job; its prompts list the pairs.
 */
import { readFileSync, writeFileSync, existsSync, mkdirSync, readdirSync } from 'node:fs';
import { join, isAbsolute } from 'node:path';
import { createHash } from 'node:crypto';
import { fileURLToPath } from 'node:url';
import {
  ROOT, GRAPH_FILE, AREAS, LIMITS, ROLES, ABOUT, loadGraphSite, readGraph, emptyGraph, normalizeGraph, serializeGraph, validateGraph,
  describeGraph, reportText, idProblem, nameProblem, blurbProblem, addsProblem, whyProblem, aliasProblem, fold,
} from './lib.mjs';

const clone = (x) => JSON.parse(JSON.stringify(x));
const isObj = (x) => x && typeof x === 'object' && !Array.isArray(x);
const AREA_IDS = new Set(AREAS.map((a) => a.id));

/** What a blind judge is shown is what its verdict is tied to: a short fingerprint of the concept. */
export function ticketOf(id, c) {
  const core = c.rungs.filter((r) => r.role === 'core').map((r) => [r.lesson, r.anchor ?? null, r.adds]).sort((a, b) => a[0].localeCompare(b[0]));
  return createHash('sha256').update(JSON.stringify([id, c.name, c.blurb, [...c.aliases].sort(), core, [...c.films].sort()])).digest('hex').slice(0, 10);
}

// ------------------------------------------------------------------ reading a staging folder

/** Every answer file of a staging folder, parsed. Unreadable files are returned in `problems`. */
export function readStaging(dir) {
  const out = { proposals: [], canonical: [], near: [], verify: [], review: [], problems: [] };
  for (const kind of ['proposals', 'canonical', 'near', 'verify', 'review']) {
    const d = join(dir, kind);
    if (!existsSync(d)) continue;
    for (const f of readdirSync(d).filter((x) => x.endsWith('.json')).sort()) {
      const file = `${kind}/${f}`;
      try {
        let text = readFileSync(join(d, f), 'utf8').trim();
        // A reader sometimes wraps its JSON in a code fence; that is not worth losing an answer over.
        const fence = /^```(?:json)?\s*\n([\s\S]*?)\n```$/.exec(text);
        if (fence) text = fence[1];
        out[kind].push({ file, name: f.replace(/\.json$/, ''), data: JSON.parse(text) });
      } catch (e) {
        out.problems.push({ stage: kind, file, item: '(whole file)', reason: `not valid JSON: ${String(e.message).slice(0, 120)}` });
      }
    }
  }
  return out;
}

/** A graph-shaped file as stage answers (one proposal per lesson, one near file), so a hand-written
 *  seed goes through exactly the checks a reader's answer does. Hashes are taken from the lessons. */
export function decomposeGraph(graph, site) {
  const proposals = new Map();
  const defined = new Set();
  const slugs = [...new Set(Object.values(graph.concepts).flatMap((c) => c.rungs.map((r) => r.lesson)))].sort();
  for (const slug of slugs) {
    const entries = [];
    for (const [id, c] of Object.entries(graph.concepts)) {
      const r = c.rungs.find((x) => x.lesson === slug);
      if (!r) continue;
      const e = { id, role: r.role };
      if (!defined.has(id)) { defined.add(id); e.new = { name: c.name, blurb: c.blurb, area: c.area, aliases: [...c.aliases] }; }
      if (r.role === 'core') { e.anchor = r.anchor ?? null; e.adds = r.adds; e.films = c.films.filter((k) => site.films.get(k)?.lesson === slug || (!site.films.has(k) && k.startsWith(`${slug}/`))); }
      entries.push(e);
    }
    entries.sort((a, b) => (a.role === b.role ? 0 : a.role === 'core' ? -1 : 1));
    proposals.set(slug, { lesson: slug, hash: site.lessons.get(slug)?.contentHash ?? 'unknown', opened_lesson: true, concepts: entries, relations: [], notes: '' });
  }
  const near = {};
  for (const [id, c] of Object.entries(graph.concepts)) if (c.near?.length) near[id] = c.near.map((n) => ({ id: n.id, why: n.why }));
  // Films whose lesson is not a rung cannot ride on a proposal; hand them back so the caller can report them.
  const orphanFilms = Object.entries(graph.concepts).flatMap(([id, c]) => c.films.filter((k) => !c.rungs.some((r) => r.role === 'core' && k.startsWith(`${r.lesson}/`))).map((k) => ({ id, film: k })));
  return {
    proposals: [...proposals.values()].map((p) => ({ file: `proposals/${p.lesson}.json`, name: p.lesson, data: p })),
    canonical: [], verify: [], problems: [],
    near: [{ file: 'near/_all.json', name: '_all', data: { area: '_all', near } }],
    orphanFilms,
  };
}

// ------------------------------------------------------------------ the merge

/**
 * True while the canonicalize stage has not answered for this staging folder: it was switched off
 * for this run, or no canonical file is there yet. Until then two new ids may carry one name (two
 * readers named the same idea); a report-only run says so as a warning. A run that writes the
 * graph never treats names as pending.
 */
export const canonicalPending = (staging, stages = {}) => stages.canonical === false || !(staging.canonical ?? []).length;

/**
 * Merge stage answers into a base graph.
 * `namesPending` turns "two ids with one name" from an error into a warning (see canonicalPending).
 * @param {{ base: any, site: any, staging: ReturnType<typeof readStaging>, maxUses?: number, stages?: { canonical?: boolean, near?: boolean, verify?: boolean }, date?: string }} input
 * @returns {{ graph: any, validation: any, log: { rejected: any[], changed: any[], notes: string[] }, info: any }}
 */
export function ingest({ base, site, staging, maxUses = LIMITS.usesPerProposal, stages = {}, date, noteLoose = true, namesPending = false }) {
  const run = { canonical: true, near: true, verify: true, ...stages };
  const log = { rejected: [...(staging.problems ?? [])], changed: [], notes: [] };
  const reject = (stage, file, item, reason) => log.rejected.push({ stage, file, item, reason });
  const change = (stage, what) => log.changed.push({ stage, what });

  const concepts = clone(base.concepts ?? {});
  const baseIds = new Set(Object.keys(concepts));
  const hashes = Object.fromEntries(Object.entries(base.lessons ?? {}).map(([s, r]) => [s, r.hash]));
  const records = new Set(Object.keys(base.lessons ?? {}));     // lessons that have a record (possibly empty)
  const pending = new Map();                                     // new id -> { defs: [{...def, by}], area }
  const relations = [];
  const filmLesson = (k) => site.films.get(k)?.lesson;
  const rungsOf = (slug) => Object.entries(concepts).flatMap(([id, c]) => c.rungs.filter((r) => r.lesson === slug).map((r) => ({ id, ...r })));
  const removeLesson = (id, slug) => { const c = concepts[id]; c.rungs = c.rungs.filter((r) => r.lesson !== slug); c.films = c.films.filter((k) => filmLesson(k) !== slug); };

  // ---------------------------------------------------------------- 1. proposals
  const props = [...(staging.proposals ?? [])].sort((a, b) => a.name.localeCompare(b.name));
  const usable = [];
  for (const p of props) {
    const d = p.data;
    const R = (item, reason) => reject('propose', p.file, item, reason);
    if (!isObj(d)) { R('(whole file)', 'not a JSON object'); continue; }
    if (d.lesson !== p.name) { R('(whole file)', `"lesson" is "${d.lesson}" but the file is named ${p.name}.json`); continue; }
    const l = site.lessons.get(d.lesson);
    if (!l) { R('(whole file)', `"${d.lesson}" is not a live lesson`); continue; }
    if (!/^[0-9a-f]{16}$/.test(d.hash ?? '')) { R('(whole file)', 'no "hash" copied from the digest (the record cannot be tied to the text that was read)'); continue; }
    if (!Array.isArray(d.concepts)) { R('(whole file)', '"concepts" is not a list'); continue; }
    usable.push({ p, d, l });
  }
  // 1a. definitions of new concepts, first valid one wins (lessons in slug order)
  for (const { p, d } of usable) {
    for (const e of d.concepts) {
      if (!isObj(e) || !isObj(e.new) || typeof e.id !== 'string') continue;
      const R = (reason) => reject('propose', p.file, `new concept ${e.id}`, reason);
      if (baseIds.has(e.id)) {
        if (fold(e.new.name ?? '') !== fold(concepts[e.id]?.name ?? '')) R(`"${e.id}" is already a concept ("${concepts[e.id].name}"); the definition "${e.new.name}" was ignored: check it is the same idea`);
        continue;
      }
      const n = e.new;
      const why = idProblem(e.id) || (typeof n.name !== 'string' ? 'no name' : nameProblem(n.name)) || (typeof n.blurb !== 'string' ? 'no blurb' : blurbProblem(n.blurb))
        || (!AREA_IDS.has(n.area) ? `unknown area "${n.area}"` : '')
        || (!Array.isArray(n.aliases) ? 'aliases is not a list' : '');
      if (why) { R(why); continue; }
      const aliases = [];
      for (const a of n.aliases) {
        const ap = typeof a !== 'string' ? 'not a string' : aliasProblem(a) || (fold(a) === fold(n.name) ? 'repeats the name' : aliases.some((x) => fold(x) === fold(a)) ? 'listed twice' : '');
        if (ap) reject('propose', p.file, `${e.id} alias "${a}"`, ap); else aliases.push(a);
      }
      if (aliases.length > LIMITS.aliasMax) { for (const a of aliases.splice(LIMITS.aliasMax)) reject('propose', p.file, `${e.id} alias "${a}"`, `over the limit of ${LIMITS.aliasMax}`); }
      if (aliases.length < LIMITS.aliasMin) { R(`needs ${LIMITS.aliasMin} to ${LIMITS.aliasMax} valid aliases, has ${aliases.length}`); continue; }
      const def = { name: n.name, blurb: n.blurb, area: n.area, aliases, by: d.lesson };
      if (!pending.has(e.id)) pending.set(e.id, { defs: [def], area: n.area });
      else pending.get(e.id).defs.push(def);
    }
  }
  for (const [id, pn] of pending) concepts[id] = { name: pn.defs[0].name, blurb: pn.defs[0].blurb, area: pn.defs[0].area, subject: 'biology', aliases: [...pn.defs[0].aliases], rungs: [], films: [], near: [] };
  // 1b. the rungs
  for (const { p, d, l } of usable) {
    const slug = d.lesson;
    const R = (item, reason) => reject('propose', p.file, item, reason);
    const clean = [];
    const extraAliases = [];
    let core = 0, uses = 0;
    for (const e of d.concepts) {
      if (!isObj(e)) { R('(entry)', 'not an object'); continue; }
      const what = `${e.role ?? '?'} ${e.id}`;
      if (typeof e.id !== 'string' || idProblem(e.id)) { R(what, idProblem(e.id) || 'no id'); continue; }
      if (!concepts[e.id]) { R(what, 'not a registry concept, and no valid definition ("new") for it in any proposal'); continue; }
      if (!ROLES.includes(e.role)) { R(what, `role must be "core" or "uses"`); continue; }
      if (clean.some((x) => x.id === e.id)) { R(what, 'listed twice for this lesson'); continue; }
      if (e.role === 'core') {
        if (typeof e.adds !== 'string' || !e.adds.trim()) { R(what, 'core rung without a note ("adds")'); continue; }
        const ap = addsProblem(e.adds);
        if (ap) { R(what, `${ap}: "${e.adds}"`); continue; }
        if (core >= LIMITS.corePerLesson) { R(what, `over the limit of ${LIMITS.corePerLesson} core concepts for one lesson`); continue; }
        const rung = { id: e.id, lesson: slug, role: 'core', adds: e.adds, films: [] };
        if (e.anchor != null && e.anchor !== '') {
          if (typeof e.anchor === 'string' && l.h2.has(e.anchor.replace(/^#/, ''))) rung.anchor = e.anchor.replace(/^#/, '');
          else R(`${what} anchor`, `"${e.anchor}" is not the id of a ## section of this lesson; the rung was kept without an anchor`);
        }
        for (const k of Array.isArray(e.films) ? e.films : []) {
          if (filmLesson(k) !== slug) R(`${what} film`, `"${k}" is not a film of this lesson`);
          else if (rung.films.includes(k)) R(`${what} film`, `"${k}" listed twice`);
          else rung.films.push(k);
        }
        core++; clean.push(rung);
      } else {
        if (uses >= maxUses) { R(what, `over the limit of ${maxUses} "uses" for one lesson`); continue; }
        if (e.adds != null || (e.anchor != null && e.anchor !== '') || (Array.isArray(e.films) && e.films.length)) log.notes.push(`${p.file}: ${what}: a note, anchor or films on a "uses" entry were ignored`);
        uses++; clean.push({ id: e.id, lesson: slug, role: 'uses' });
      }
      if (Array.isArray(e.aliases) && baseIds.has(e.id)) for (const a of e.aliases.slice(0, 2)) extraAliases.push({ id: e.id, alias: a });
    }
    if (d.concepts.length && !clean.length) { R('(whole file)', 'every entry was rejected; the lesson keeps what it had'); continue; }
    // replace the lesson's rungs
    const before = rungsOf(slug);
    for (const r of before) removeLesson(r.id, slug);
    for (const r of clean) {
      const c = concepts[r.id];
      c.rungs.push(r.role === 'core' ? { lesson: slug, role: 'core', ...(r.anchor ? { anchor: r.anchor } : {}), adds: r.adds } : { lesson: slug, role: 'uses' });
      for (const k of r.films ?? []) if (!c.films.includes(k)) c.films.push(k);
    }
    records.add(slug);
    hashes[slug] = d.hash;
    if (d.hash !== l.contentHash) log.notes.push(`${p.file}: the lesson's teaching text changed after it was read (hash ${d.hash}, now ${l.contentHash}); the record will show as stale`);
    if (!d.concepts.length) log.notes.push(`${p.file}: no idea filed${d.notes ? ` (${String(d.notes).slice(0, 160)})` : ''}`);
    if (before.length) {
      const key = (r) => `${r.role} ${r.id}${r.role === 'core' ? ` #${r.anchor ?? '-'} "${r.adds}"` : ''}`;
      const was = before.map(key).sort(), now = clean.map(key).sort();
      const gone = was.filter((x) => !now.includes(x)), came = now.filter((x) => !was.includes(x));
      if (gone.length || came.length) change('propose', `${slug}: record changed${gone.length ? `; removed: ${gone.join(' | ')}` : ''}${came.length ? `; added: ${came.join(' | ')}` : ''}${d.notes ? `; reader's note: ${String(d.notes).slice(0, 200)}` : ''}`);
    }
    for (const x of extraAliases) {
      const c = concepts[x.id];
      const ap = typeof x.alias !== 'string' ? 'not a string' : aliasProblem(x.alias) || (c.aliases.some((a) => fold(a) === fold(x.alias)) ? 'already an alias' : fold(x.alias) === fold(c.name) ? 'repeats the name' : c.aliases.length >= LIMITS.aliasMax ? `the concept already has ${LIMITS.aliasMax} aliases` : '');
      if (ap) { if (ap !== 'already an alias') R(`${x.id} extra alias "${x.alias}"`, ap); } else { c.aliases.push(x.alias); change('propose', `${x.id}: alias "${x.alias}" added (suggested by ${slug})`); }
    }
    for (const rel of Array.isArray(d.relations) ? d.relations : []) if (isObj(rel) && typeof rel.a === 'string' && typeof rel.b === 'string') relations.push({ a: rel.a, b: rel.b, note: String(rel.note ?? ''), by: slug });
  }
  const afterProposals = { pending: new Map([...pending].map(([id, v]) => [id, { ...v, rungs: clone(concepts[id]?.rungs ?? []) }])), concepts: clone(concepts) };

  // ---------------------------------------------------------------- 2. one id per idea
  const mapped = new Map();                      // old id -> id it was merged into
  const resolve = (id) => { let x = id, n = 0; while (mapped.has(x) && n++ < 20) x = mapped.get(x); return x; };
  const repoint = (from, to) => { for (const c of Object.values(concepts)) for (const n of c.near) if (n.id === from) n.id = to; };
  const mergeInto = (src, dst, file) => {
    const a = concepts[src], b = concepts[dst];
    for (const r of a.rungs) {
      const have = b.rungs.find((x) => x.lesson === r.lesson);
      if (!have) b.rungs.push(r);
      else if (have.role === 'uses' && r.role === 'core') { b.rungs[b.rungs.indexOf(have)] = r; }
      else if (have.role === 'core' && r.role === 'core') change('canonicalize', `${dst}: ${r.lesson} was core for both ${dst} and ${src}; kept the note "${have.adds}" and let go of "${r.adds}" (${file})`);
    }
    for (const k of a.films) if (!b.films.includes(k)) b.films.push(k);
    for (const n of a.near) if (n.id !== dst && !b.near.some((x) => x.id === n.id)) b.near.push(n);
    delete concepts[src];
    mapped.set(src, dst);
    repoint(src, dst);
    change('canonicalize', `${src} merged into ${dst} (${file})`);
  };
  const covered = new Set();
  if (run.canonical) {
    const order = (f) => (f.name === '_cross' ? 999 : AREAS.findIndex((a) => a.id === f.name));
    for (const f of [...(staging.canonical ?? [])].sort((a, b) => order(a) - order(b) || a.name.localeCompare(b.name))) {
      const d = f.data;
      const R = (item, reason) => reject('canonicalize', f.file, item, reason);
      if (!isObj(d)) { R('(whole file)', 'not a JSON object'); continue; }
      if (d.area !== f.name || (f.name !== '_cross' && !AREA_IDS.has(f.name))) { R('(whole file)', `"area" is "${d.area}" but the file is ${f.name}.json (expected an area id or _cross)`); continue; }
      const seenHere = new Set();
      for (const e of Array.isArray(d.concepts) ? d.concepts : []) {
        if (!isObj(e) || typeof e.id !== 'string') { R('(entry)', 'no id'); continue; }
        const what = `concept ${e.id}`;
        if (idProblem(e.id)) { R(what, idProblem(e.id)); continue; }
        const merge = [...new Set((Array.isArray(e.merge) ? e.merge : []).filter((x) => typeof x === 'string'))];
        const target = resolve(e.id);
        let c = concepts[target];
        const fields = {};
        for (const [k, check] of [['name', nameProblem], ['blurb', blurbProblem]]) if (e[k] != null) { const pr = typeof e[k] !== 'string' ? 'not a string' : check(e[k]); if (pr) R(`${what} ${k}`, `${pr}: "${e[k]}"; kept "${c?.[k] ?? '(none)'}"`); else fields[k] = e[k]; }
        if (e.area != null) { if (!AREA_IDS.has(e.area)) R(`${what} area`, `unknown area "${e.area}"`); else fields.area = e.area; }
        if (e.aliases != null) {
          const ok = [];
          for (const a of Array.isArray(e.aliases) ? e.aliases : []) {
            const ap = typeof a !== 'string' ? 'not a string' : aliasProblem(a) || (ok.some((x) => fold(x) === fold(a)) ? 'listed twice' : fold(a) === fold(fields.name ?? c?.name ?? '') ? 'repeats the name' : ok.length >= LIMITS.aliasMax ? `over the limit of ${LIMITS.aliasMax}` : '');
            if (ap) R(`${what} alias "${a}"`, ap); else ok.push(a);
          }
          if (ok.length >= LIMITS.aliasMin) fields.aliases = ok; else if (c) R(`${what} aliases`, `fewer than ${LIMITS.aliasMin} valid aliases given; kept the existing ones`);
        }
        if (!c) {
          if (!fields.name || !fields.blurb || !fields.area || !fields.aliases) { R(what, 'a new id needs a valid name, blurb, area and aliases; this entry was not applied, so the ids it merges stay as they are'); continue; }
          c = concepts[target] = { name: fields.name, blurb: fields.blurb, area: fields.area, subject: 'biology', aliases: fields.aliases, rungs: [], films: [], near: [] };
          change('canonicalize', `${target}: new concept "${c.name}" (${f.file})`);
        } else {
          const gaveAliases = !!fields.aliases;
          for (const [k, v] of Object.entries(fields)) if (JSON.stringify(c[k]) !== JSON.stringify(v)) { if (baseIds.has(target)) change('canonicalize', `${target}: ${k} changed from ${JSON.stringify(c[k])} to ${JSON.stringify(v)} (${f.file})`); c[k] = v; }
          c._aliasesSet = gaveAliases;
        }
        for (const m of merge) {
          if (seenHere.has(m)) { R(what, `"${m}" is merged twice in this file`); continue; }
          seenHere.add(m); covered.add(m);
          const src = resolve(m);
          if (src === target) continue;
          if (!concepts[src]) { R(what, `merge names "${m}", which is not a proposed or existing concept`); continue; }
          if (!c._aliasesSet && e.aliases == null) for (const a of concepts[src].aliases) if (c.aliases.length < LIMITS.aliasMax && !c.aliases.some((x) => fold(x) === fold(a)) && fold(a) !== fold(c.name)) c.aliases.push(a);
          mergeInto(src, target, f.file);
        }
        delete c._aliasesSet;
      }
      for (const e of Array.isArray(d.drop) ? d.drop : []) {
        if (!isObj(e) || typeof e.id !== 'string') { R('(drop entry)', 'no id'); continue; }
        covered.add(e.id);
        const id = resolve(e.id);
        if (!concepts[id]) { R(`drop ${e.id}`, 'not a proposed or existing concept'); continue; }
        if (baseIds.has(id)) { R(`drop ${e.id}`, 'a concept that was already in the graph cannot be dropped here; remove its rungs by hand if it is wrong'); continue; }
        for (const r of concepts[id].rungs) change('canonicalize', `${id} dropped, so ${r.lesson} loses its ${r.role} rung${r.adds ? ` ("${r.adds}")` : ''}: ${e.why ?? 'no reason given'} (${f.file})`);
        if (!concepts[id].rungs.length) change('canonicalize', `${id} dropped: ${e.why ?? 'no reason given'} (${f.file})`);
        delete concepts[id];
        for (const c of Object.values(concepts)) c.near = c.near.filter((n) => n.id !== id);
      }
      for (const e of Array.isArray(d.rungs) ? d.rungs : []) {
        if (!isObj(e)) continue;
        const id = resolve(String(e.id));
        const c = concepts[id];
        const r = c?.rungs.find((x) => x.lesson === e.lesson);
        const what = `rung ${e.id}/${e.lesson}`;
        if (!r) { R(what, 'no such rung'); continue; }
        if (e.role === 'drop') { removeLesson(id, e.lesson); change('canonicalize', `${id}: ${e.lesson} removed (was ${r.role}): ${e.why ?? 'no reason given'} (${f.file})`); }
        else if (e.role === 'uses') { if (r.role === 'core') { delete r.adds; delete r.anchor; r.role = 'uses'; c.films = c.films.filter((k) => filmLesson(k) !== e.lesson); change('canonicalize', `${id}: ${e.lesson} demoted from core to uses: ${e.why ?? 'no reason given'} (${f.file})`); } }
        else if (e.role != null && e.role !== 'core') R(what, `role "${e.role}" (expected "uses" or "drop")`);
        else if (typeof e.adds === 'string') {
          if (r.role !== 'core') R(what, 'a note can only be replaced on a core rung');
          else { const ap = addsProblem(e.adds); if (ap) R(what, `${ap}: "${e.adds}"`); else { change('canonicalize', `${id}/${e.lesson}: note "${r.adds}" replaced by "${e.adds}" (${f.file})`); r.adds = e.adds; } }
        }
      }
      if (f.name !== '_cross') {
        const missed = [...pending].filter(([id, pn]) => pn.area === f.name && !covered.has(id)).map(([id]) => id);
        for (const id of missed) R(`proposed id ${id}`, 'not mentioned in "concepts[].merge" or "drop"; kept as its own concept');
      }
    }
    const areasWithFile = new Set((staging.canonical ?? []).map((f) => f.name));
    const loose = {};
    for (const [id, pn] of pending) if (!areasWithFile.has(pn.area) && concepts[id]) (loose[pn.area] ??= []).push(id);
    if (noteLoose) for (const [area, ids] of Object.entries(loose)) log.notes.push(`area ${area}: ${ids.length} new concept(s) went in as proposed, with no merging step: ${ids.join(', ')}`);
  }

  // ---------------------------------------------------------------- 3. sideways hops
  if (run.near) {
    for (const f of [...(staging.near ?? [])].sort((a, b) => a.name.localeCompare(b.name))) {
      const d = f.data;
      const R = (item, reason) => reject('near', f.file, item, reason);
      if (!isObj(d) || !isObj(d.near)) { R('(whole file)', 'no "near" object'); continue; }
      for (const from of Object.keys(d.near).sort()) {
        const id = resolve(from);
        const c = concepts[id];
        if (!c) { R(`${from}`, 'not a concept'); continue; }
        const ok = [];
        for (const e of Array.isArray(d.near[from]) ? d.near[from] : []) {
          const to = resolve(String(e?.id));
          const what = `${from} -> ${e?.id}`;
          const why = !concepts[to] ? 'the target is not a concept' : to === id ? 'a hop to itself' : ok.some((x) => x.id === to) ? 'listed twice'
            : typeof e.why !== 'string' ? 'no reason' : whyProblem(e.why) ? `${whyProblem(e.why)}: "${e.why}"` : ok.length >= LIMITS.nearMax ? `over the limit of ${LIMITS.nearMax}` : '';
          if (why) R(what, why); else ok.push({ id: to, why: e.why });
        }
        if (ok.length) c.near = ok; else if ((d.near[from] ?? []).length) R(`${from}`, 'no valid hop in the list; kept what the concept had');
      }
    }
  }

  // ---------------------------------------------------------------- 4. keep the graph whole
  const tidy = (stage) => {
    for (const [id, c] of Object.entries(concepts)) {
      if (c.rungs.some((r) => r.role === 'core')) continue;
      for (const r of c.rungs) change(stage, `${id} has no core rung left, so ${r.lesson} loses its uses rung`);
      change(stage, `${id} removed: no lesson teaches it`);
      delete concepts[id];
    }
    for (const [id, c] of Object.entries(concepts)) {
      const keep = [];
      for (const n of c.near) {
        if (!concepts[n.id]) { change(stage, `${id}: sideways hop to ${n.id} removed (that concept is gone)`); continue; }
        if (n.id === id || keep.some((x) => x.id === n.id)) continue;
        if (keep.length >= LIMITS.nearMax) { change(stage, `${id}: sideways hop to ${n.id} removed (over the limit of ${LIMITS.nearMax})`); continue; }
        keep.push(n);
      }
      c.near = keep;
      c.films = c.films.filter((k) => { const ok = c.rungs.some((r) => r.lesson === filmLesson(k)); if (!ok) change(stage, `${id}: film ${k} removed (its lesson is not a rung any more)`); return ok; });
    }
    // an alias belongs to one concept, and is never another concept's name
    const names = new Map(Object.entries(concepts).map(([id, c]) => [fold(c.name), id]));
    const owner = new Map();
    const ids = Object.keys(concepts).sort((a, b) => (baseIds.has(b) - baseIds.has(a)) || a.localeCompare(b));
    for (const id of ids) {
      const c = concepts[id];
      c.aliases = c.aliases.filter((a) => {
        const k = fold(a);
        if (names.has(k) && names.get(k) !== id) { reject(stage, '(merged graph)', `${id} alias "${a}"`, `it is the name of ${names.get(k)}`); return false; }
        if (names.get(k) === id) return false;
        if (owner.has(k) && owner.get(k) !== id) { reject(stage, '(merged graph)', `${id} alias "${a}"`, `already an alias of ${owner.get(k)} (each phrase goes to one concept)`); return false; }
        owner.set(k, id);
        return true;
      });
    }
  };
  tidy('merge');
  const preVerify = clone(concepts);

  // ---------------------------------------------------------------- 5. the blind check
  if (run.verify) {
    for (const f of [...(staging.verify ?? [])].sort((a, b) => a.name.localeCompare(b.name))) {
      const d = f.data;
      const R = (item, reason) => reject('verify', f.file, item, reason);
      if (!isObj(d) || d.concept !== f.name) { R('(whole file)', `"concept" is "${d?.concept}" but the file is ${f.name}.json`); continue; }
      const id = d.concept;
      const c = concepts[id];
      if (!c) { R('(whole file)', `"${id}" is not a concept in the merged graph (merged away, dropped, or never proposed)`); continue; }
      const ticket = ticketOf(id, preVerify[id]);
      if (d.ticket !== ticket) { R('(whole file)', `ticket ${d.ticket ?? '(none)'} does not match ${ticket}: the concept changed after it was judged, so the verdicts were not applied; judge it again`); continue; }
      const core = c.rungs.filter((r) => r.role === 'core');
      const seen = new Set();
      for (const v of Array.isArray(d.rungs) ? d.rungs : []) {
        const r = c.rungs.find((x) => x.lesson === v?.lesson && x.role === 'core');
        const what = `${id}/${v?.lesson}`;
        if (!r) { R(what, 'not a core rung of this concept'); continue; }
        seen.add(r.lesson);
        if (v.verdict === 'ok') continue;
        if (v.verdict === 'wrong') { removeLesson(id, r.lesson); change('verify', `${what}: rung removed (judged wrong): ${v.why ?? 'no reason given'}`); }
        else if (v.verdict === 'not-core') { delete r.adds; delete r.anchor; r.role = 'uses'; c.films = c.films.filter((k) => filmLesson(k) !== r.lesson); change('verify', `${what}: demoted from core to uses: ${v.why ?? 'no reason given'}`); }
        else if (v.verdict === 'note') {
          const ap = typeof v.adds !== 'string' ? 'no replacement note given' : addsProblem(v.adds);
          if (ap) R(`${what} note`, `the judge's replacement was not usable (${ap}); the old note "${r.adds}" stays and needs a rewrite: ${v.why ?? ''}`);
          else { change('verify', `${what}: note "${r.adds}" replaced by "${v.adds}": ${v.why ?? 'no reason given'}`); r.adds = v.adds; }
        } else R(what, `verdict "${v.verdict}" (expected ok, note, not-core or wrong)`);
      }
      for (const r of core) if (!seen.has(r.lesson)) R(`${id}/${r.lesson}`, 'the judge gave no verdict for this rung; it was kept unjudged');
      if (d.same_idea === false && !(d.rungs ?? []).some((v) => v.verdict === 'wrong' || v.verdict === 'not-core')) R(id, 'judged "not one idea" but no rung was marked wrong; nothing was changed: read this concept');
      for (const s of Array.isArray(d.bad_anchors) ? d.bad_anchors : []) { const r = c.rungs.find((x) => x.lesson === s && x.role === 'core'); if (r?.anchor) { change('verify', `${id}/${s}: anchor #${r.anchor} removed (the judge found the idea is not taught in that section)`); delete r.anchor; } }
      for (const b of Array.isArray(d.bad_films) ? d.bad_films : []) { if (c.films.includes(b?.film)) { c.films = c.films.filter((k) => k !== b.film); change('verify', `${id}: film ${b.film} removed: ${b.why ?? 'no reason given'}`); } }
      for (const b of Array.isArray(d.bad_aliases) ? d.bad_aliases : []) { const i = c.aliases.findIndex((a) => fold(a) === fold(b?.alias ?? '')); if (i >= 0) { change('verify', `${id}: alias "${c.aliases[i]}" removed: ${b.why ?? 'no reason given'}`); c.aliases.splice(i, 1); } }
    }
    tidy('verify');
  }

  // ---------------------------------------------------------------- 5b. review: corrections made after reading the result
  if (run.review !== false) {
    for (const f of [...(staging.review ?? [])].sort((a, b) => a.name.localeCompare(b.name))) {
      const d = f.data;
      const R = (item, reason) => reject('review', f.file, item, reason);
      if (!isObj(d)) { R('(whole file)', 'not a JSON object'); continue; }
      for (const e of Array.isArray(d.concepts) ? d.concepts : []) {
        const n = e?.new;
        const what = `new concept ${e?.id}`;
        if (concepts[e?.id]) { R(what, 'already a concept'); continue; }
        const why = idProblem(e?.id) || (!isObj(n) ? 'no definition' : nameProblem(n.name ?? '') || blurbProblem(n.blurb ?? '') || (!AREA_IDS.has(n.area) ? `unknown area "${n.area}"` : '')
          || (!Array.isArray(n.aliases) || n.aliases.length < LIMITS.aliasMin || n.aliases.length > LIMITS.aliasMax ? `needs ${LIMITS.aliasMin} to ${LIMITS.aliasMax} aliases` : n.aliases.map((a) => aliasProblem(a)).find(Boolean) ?? ''));
        if (why) { R(what, why); continue; }
        concepts[e.id] = { name: n.name, blurb: n.blurb, area: n.area, subject: 'biology', aliases: [...n.aliases], rungs: [], films: [], near: [] };
        change('review', `${e.id}: new concept "${n.name}" (${f.file})`);
      }
      for (const m of Array.isArray(d.merge) ? d.merge : []) {
        const from = resolve(String(m?.from)), into = resolve(String(m?.into));
        if (!concepts[from] || !concepts[into] || from === into) { R(`merge ${m?.from} into ${m?.into}`, 'both must be different concepts'); continue; }
        for (const a of concepts[from].aliases) if (concepts[into].aliases.length < LIMITS.aliasMax && !concepts[into].aliases.some((x) => fold(x) === fold(a)) && fold(a) !== fold(concepts[into].name)) concepts[into].aliases.push(a);
        mergeInto(from, into, `${f.file}: ${m.why ?? 'no reason given'}`);
        log.changed[log.changed.length - 1].stage = 'review';
        concepts[into].near = concepts[into].near.filter((n) => n.id !== into);
      }
      for (const e of Array.isArray(d.rungs) ? d.rungs : []) {
        const id = resolve(String(e?.id));
        const c = concepts[id];
        const l = site.lessons.get(e?.lesson);
        const what = `rung ${e?.id}/${e?.lesson}`;
        if (!c) { R(what, 'not a concept'); continue; }
        if (!l) { R(what, 'not a live lesson'); continue; }
        const have = c.rungs.find((x) => x.lesson === l.slug);
        const tail = `: ${e.why ?? 'no reason given'} (${f.file})`;
        if (e.role === 'drop') {
          if (!have) { R(what, 'no such rung'); continue; }
          removeLesson(id, l.slug); change('review', `${id}/${l.slug}: ${have.role} rung removed${tail}`);
        } else if (e.role === 'uses') {
          removeLesson(id, l.slug); c.rungs.push({ lesson: l.slug, role: 'uses' });
          change('review', `${id}/${l.slug}: ${have ? `${have.role} rung set to uses` : 'uses rung added'}${tail}`);
        } else if (e.role === 'core' || (e.role == null && have?.role === 'core')) {
          const adds = e.adds ?? have?.adds;
          const ap = typeof adds !== 'string' ? 'core rung without a note' : addsProblem(adds);
          if (ap) { R(what, `${ap}: "${adds}"`); continue; }
          const anchor = e.anchor === undefined ? have?.anchor : e.anchor;
          if (anchor != null && !l.h2.has(anchor)) { R(what, `"${anchor}" is not the id of a ## section of this lesson`); continue; }
          const films = e.films === undefined ? c.films.filter((k) => filmLesson(k) === l.slug) : e.films;
          const badFilm = (Array.isArray(films) ? films : []).find((k) => filmLesson(k) !== l.slug);
          if (badFilm) { R(what, `"${badFilm}" is not a film of this lesson`); continue; }
          removeLesson(id, l.slug);
          c.rungs.push({ lesson: l.slug, role: 'core', ...(anchor ? { anchor } : {}), adds });
          for (const k of films ?? []) if (!c.films.includes(k)) c.films.push(k);
          change('review', `${id}/${l.slug}: ${have ? (have.role === 'core' ? `core rung rewritten (note was "${have.adds}", now "${adds}")` : 'uses rung raised to core') : `core rung added ("${adds}")`}${tail}`);
        } else R(what, `role "${e.role}" (expected core, uses or drop)`);
      }
      for (const from of Object.keys(isObj(d.near) ? d.near : {}).sort()) {
        const id = resolve(from);
        const c = concepts[id];
        if (!c) { R(`near ${from}`, 'not a concept'); continue; }
        for (const e of Array.isArray(d.near[from]) ? d.near[from] : []) {
          const to = resolve(String(e?.id));
          const why = !concepts[to] ? 'the target is not a concept' : to === id ? 'a hop to itself' : c.near.some((x) => x.id === to) ? 'already a hop'
            : typeof e.why !== 'string' ? 'no reason' : whyProblem(e.why) ? `${whyProblem(e.why)}: "${e.why}"` : c.near.length >= LIMITS.nearMax ? `the concept already has ${LIMITS.nearMax} hops` : '';
          if (why) R(`${from} -> ${e?.id}`, why); else { c.near.push({ id: to, why: e.why }); change('review', `${id}: sideways hop to ${to} added (${f.file})`); }
        }
      }
    }
    tidy('review');
  }

  // ---------------------------------------------------------------- 6. one fixed order, then the rules
  const lessons = {};
  for (const slug of records) if (site.lessons.has(slug) || base.lessons?.[slug]) lessons[slug] = { hash: hashes[slug], concepts: [] };
  let graph = normalizeGraph({ version: 1, updated: date ?? new Date().toISOString().slice(0, 10), about: ABOUT, areas: base.areas?.length ? base.areas : AREAS, concepts, lessons }, site, { hashFor: (slug) => site.lessons.get(slug)?.contentHash });
  const sameAsBase = JSON.stringify({ ...graph, updated: 0 }) === JSON.stringify({ ...normalizeGraph({ ...emptyGraph(), ...clone(base) }, site), about: ABOUT, updated: 0 });
  if (sameAsBase && base.updated && !date) graph.updated = base.updated;
  // Two ids with one name: work for the canonicalize stage while `namesPending`, a broken record otherwise.
  const validation = validateGraph(graph, site, { namesPending });
  return {
    graph, validation, log,
    info: { pending: afterProposals.pending, afterProposals: afterProposals.concepts, preVerify, relations: relations.map((r) => ({ ...r, a: resolve(r.a), b: resolve(r.b) })), mapped, sameAsBase },
  };
}

/** The report as text: what the graph is now, then everything that was changed or rejected. */
export function ingestReport(result, site, { title = 'Hop graph ingest' } = {}) {
  const { graph, validation, log } = result;
  const L = [title, '='.repeat(title.length), ''];
  L.push(reportText(describeGraph(graph, site), site));
  L.push('');
  L.push(`CHANGES APPLIED (${log.changed.length})`);
  for (const stage of ['propose', 'canonicalize', 'near', 'merge', 'verify', 'review']) {
    const mine = log.changed.filter((c) => c.stage === stage);
    if (mine.length) { L.push(`  ${stage} (${mine.length})`); for (const c of mine) L.push(`    ${c.what}`); }
  }
  L.push('');
  L.push(`REJECTED ITEMS (${log.rejected.length}): each was left out for the reason given; everything else in its file was kept`);
  const byReason = {};
  for (const r of log.rejected) L.push(`  [${r.stage}] ${r.file}: ${r.item}: ${r.reason}`), (byReason[r.stage] = (byReason[r.stage] ?? 0) + 1);
  if (log.rejected.length) L.push(`  by stage: ${Object.entries(byReason).map(([k, v]) => `${k} ${v}`).join(', ')}`);
  L.push('');
  L.push(`NOTES (${log.notes.length})`);
  for (const n of log.notes) L.push(`  ${n}`);
  L.push('');
  L.push(`CHECK: ${validation.errors.length} error(s), ${validation.warnings.length} warning(s)`);
  for (const e of validation.errors) L.push(`  FAIL  ${e}`);
  for (const w of validation.warnings) L.push(`  warn  ${w}`);
  return L.join('\n') + '\n';
}

// ------------------------------------------------------------------ run

if (process.argv[1] && fileURLToPath(import.meta.url) === process.argv[1]) {
  const argv = process.argv.slice(2);
  const flag = (f) => argv.includes(f);
  const opt = (f, d) => { const i = argv.indexOf(f); return i >= 0 ? argv[i + 1] : d; };
  const abs = (p) => (p ? (isAbsolute(p) ? p : join(ROOT, p)) : p);
  const stagingDir = abs(opt('--staging'));
  const graphFile = abs(opt('--graph'));
  if (!stagingDir && !graphFile) { console.error('Say --staging <dir> (stage answers) or --graph <file> (import a graph-shaped file). See the header of this file.'); process.exit(2); }
  const outFile = abs(opt('--out')) ?? GRAPH_FILE;
  const site = await loadGraphSite();
  let base, staging, maxUses = Number(opt('--max-uses', LIMITS.usesPerProposal));
  if (graphFile) {
    const src = JSON.parse(readFileSync(graphFile, 'utf8'));
    base = { ...emptyGraph(), ...(Array.isArray(src.areas) && src.areas.length ? { areas: src.areas } : {}) };
    staging = decomposeGraph(src, site);
    for (const o of staging.orphanFilms) staging.problems.push({ stage: 'propose', file: graphFile, item: `${o.id} film ${o.film}`, reason: 'its lesson is not a core rung of the concept' });
    maxUses = Number(opt('--max-uses', LIMITS.usesPerLesson));
  } else {
    if (!existsSync(stagingDir)) { console.error(`No such folder: ${stagingDir}`); process.exit(2); }
    const baseFile = abs(opt('--base')) ?? join(stagingDir, 'base.json');
    if (!existsSync(baseFile)) {
      if (opt('--base')) { console.error(`No such file: ${baseFile}`); process.exit(2); }
      writeFileSync(baseFile, serializeGraph(readGraph(outFile) ?? readGraph() ?? emptyGraph()));
      console.log(`ingest: saved the starting graph as ${baseFile} (every run of this staging folder starts from it)`);
    }
    base = JSON.parse(readFileSync(baseFile, 'utf8'));
    staging = readStaging(stagingDir);
  }
  const stages = { canonical: !flag('--no-canonical'), near: !flag('--no-near'), verify: !flag('--no-verify') };
  // A report-only run of a fill that has not been canonicalized yet may show two ids with one name: that
  // is the next stage's work, so it is a warning and the run exits 0. Any run that writes makes it an error.
  const namesPending = !graphFile && flag('--dry') && canonicalPending(staging, stages);
  const result = ingest({ base, site, staging, maxUses, date: opt('--date'), noteLoose: !graphFile, stages, namesPending });
  const n = (k) => (staging[k] ?? []).length;
  const report = ingestReport(result, site, { title: `Hop graph ingest: ${n('proposals')} proposal(s), ${n('canonical')} canonical file(s), ${n('near')} near file(s), ${n('verify')} verdict file(s), ${n('review')} review file(s)` });
  if (stagingDir) {
    mkdirSync(join(stagingDir, 'reports'), { recursive: true });
    writeFileSync(join(stagingDir, 'reports', 'ingest.txt'), report);
    writeFileSync(join(stagingDir, 'reports', 'ingest.json'), JSON.stringify({ describe: describeGraph(result.graph, site), changed: result.log.changed, rejected: result.log.rejected, notes: result.log.notes, errors: result.validation.errors, warnings: result.validation.warnings }, null, 1) + '\n');
  }
  console.log(flag('--quiet') ? report.split('\n').slice(0, 6).join('\n') : report);
  if (result.validation.errors.length) { console.error(`ingest: the merged graph breaks ${result.validation.errors.length} rule(s); nothing was written.`); process.exit(1); }
  if (flag('--dry')) { console.log('ingest: --dry, nothing written.'); process.exit(0); }
  writeFileSync(outFile, serializeGraph(result.graph));
  console.log(`ingest: wrote ${outFile} (${Object.keys(result.graph.concepts).length} concepts, ${Object.keys(result.graph.lessons).length} lesson records; ${result.log.rejected.length} rejected item(s), ${result.log.changed.length} change(s) logged).`);
}
