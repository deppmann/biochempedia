#!/usr/bin/env node
/**
 * Hop graph, the top-up: put ONE new or rewritten lesson into the graph. This is the step that keeps
 * the graph filling itself in: run it when a lesson ships or is rewritten, next to refreshing its
 * lesson links. CI names every live lesson with no record and every record older than its lesson.
 *
 *   node scripts/topic-graph/assign.mjs --list                 which lessons need it (no record, or stale)
 *   node scripts/topic-graph/assign.mjs --emit <slug>          print the prompt for one lesson (give it to any
 *                                                              capable model or person; save the JSON answer)
 *   node scripts/topic-graph/assign.mjs --apply <answer.json>  check that answer and merge it into the graph
 *   node scripts/topic-graph/assign.mjs --call <slug>[,<slug>] ask the model directly and merge the answer
 *                                                              (needs ANTHROPIC_API_KEY; never written anywhere)
 *   node scripts/topic-graph/assign.mjs --mock <slug>          a stand-in answer, to test the plumbing
 *   options: --dry (report, write nothing), --out <file> (default src/data/topic-graph.json),
 *            --full (send the whole lesson text with --emit or --call, not only its digest),
 *            --max-uses <n>, --effort low|medium
 *
 * The prompt is assignPrompt() in prompts.mjs; the answer goes through the same checks as every other
 * answer (ingest.mjs). A lesson's answer REPLACES that lesson's rungs and nothing else. A new concept
 * goes in as written, so the report lists it: read it.
 *
 * --call uses the HTTP API with fetch, as scripts/lesson-links/generate.mjs does, so the repo gains no
 * dependency.
 */
import { readFileSync, writeFileSync, mkdirSync } from 'node:fs';
import { join, isAbsolute } from 'node:path';
import { plain } from '../lesson-links/lib.mjs';
import { ROOT, GRAPH_FILE, CACHE_DIR, LIMITS, loadGraphSite, readGraph, emptyGraph, registryOf, serializeGraph } from './lib.mjs';
import { buildDigests } from './digest.mjs';
import { assignPrompt } from './prompts.mjs';
import { ingest, ingestReport } from './ingest.mjs';

/** The model family the lesson links use (scripts/lesson-links/generate.mjs). */
const MODEL = 'claude-sonnet-5-5';
const API = 'https://api.anthropic.com/v1';
const VERSION = '2026-10-21';

const argv = process.argv.slice(2);
const flag = (f) => argv.includes(f);
const opt = (f, d) => { const i = argv.indexOf(f); return i >= 0 ? argv[i + 1] : d; };
const abs = (p) => (isAbsolute(p) ? p : join(ROOT, p));
const outFile = opt('--out') ? abs(opt('--out')) : GRAPH_FILE;

const site = await loadGraphSite();
const graph = readGraph(outFile) ?? readGraph() ?? emptyGraph();

if (flag('--list')) {
  const missing = [...site.lessons.keys()].filter((s) => !graph.lessons[s]);
  const stale = Object.entries(graph.lessons).filter(([s, r]) => site.lessons.has(s) && r.hash !== site.lessons.get(s).contentHash).map(([s]) => s);
  console.log(`no record (${missing.length}): ${missing.join(', ') || 'none'}`);
  console.log(`stale (${stale.length}): ${stale.join(', ') || 'none'}`);
  process.exit(0);
}

const need = (slug) => { const l = site.lessons.get(slug); if (!l) { console.error(`Not a live lesson: ${slug}`); process.exit(2); } return l; };

/** The prompt for one lesson, with the ladders it may join and the record it has now. */
function promptFor(slug) {
  const l = need(slug);
  const digest = buildDigests(site, [slug]).get(slug);
  const existing = Object.entries(graph.concepts).flatMap(([id, c]) => {
    const r = c.rungs.find((x) => x.lesson === slug);
    if (!r) return [];
    return [r.role === 'core' ? { id, role: 'core', anchor: r.anchor ?? null, adds: r.adds, films: c.films.filter((k) => site.films.get(k)?.lesson === slug) } : { id, role: 'uses' }];
  });
  // Ladders the lesson is likeliest to join: the ones it is on now, and those of the lessons its page already links to.
  const linked = new Set([slug, ...Object.values(digest.ladder ?? {}).flatMap((v) => (Array.isArray(v) ? v.map((x) => x.slug) : [])), ...(digest.links?.before ?? []).map((x) => x.slug), ...(digest.links?.after ?? []).map((x) => x.slug)]);
  const ladders = Object.entries(graph.concepts)
    .filter(([, c]) => c.rungs.some((r) => r.role === 'core' && linked.has(r.lesson)))
    .map(([id, c]) => ({ id, rungs: c.rungs.filter((r) => r.role === 'core' && r.lesson !== slug).map((r) => ({ lesson: r.lesson, stage: site.lessons.get(r.lesson)?.stage ?? '?', adds: r.adds })) }))
    .filter((c) => c.rungs.length);
  return assignPrompt(digest, registryOf(graph, site), { existing, ladders, ...(flag('--full') ? { body: plain(l.body) } : {}) });
}

/** A model's reply as a JSON object (a code fence around it is tolerated). */
function parseAnswer(text) {
  let t = String(text).trim();
  const fence = /```(?:json)?\s*\n([\s\S]*?)\n```/.exec(t);
  if (fence) t = fence[1];
  const a = t.indexOf('{'), b = t.lastIndexOf('}');
  return JSON.parse(a >= 0 && b > a ? t.slice(a, b + 1) : t);
}

/** Check answers and merge them. Returns the exit code. */
function apply(answers) {
  const staging = { proposals: [], canonical: [], verify: [], problems: [], near: [] };
  for (const a of answers) {
    staging.proposals.push({ file: `proposals/${a.lesson}.json`, name: String(a.lesson), data: a });
    if (a.near && typeof a.near === 'object') staging.near.push({ file: `near/${a.lesson}.json`, name: String(a.lesson), data: { area: '_assign', near: a.near } });
  }
  const result = ingest({ base: graph, site, staging, maxUses: Number(opt('--max-uses', LIMITS.usesPerProposal)) });
  const made = [...result.info.pending.keys()].filter((id) => result.graph.concepts[id]);
  console.log(ingestReport(result, site, { title: `Hop graph top-up: ${answers.map((a) => a.lesson).join(', ')}` }).split('\n').filter((_ln, i, all) => i < 6 || all.slice(0, i).some((x) => x.startsWith('CHANGES APPLIED'))).join('\n'));
  if (made.length) console.log(`NEW CONCEPTS (read these; there was no merging step): ${made.map((id) => `${id} "${result.graph.concepts[id].name}"`).join('; ')}`);
  if (result.validation.errors.length) { console.error('assign: the merged graph breaks a rule; nothing was written.'); return 1; }
  const applied = answers.filter((a) => result.graph.lessons[a.lesson] && !result.log.rejected.some((r) => r.file === `proposals/${a.lesson}.json` && r.item === '(whole file)'));
  if (flag('--dry')) { console.log('assign: --dry, nothing written.'); return applied.length === answers.length ? 0 : 1; }
  writeFileSync(outFile, serializeGraph(result.graph));
  console.log(`assign: wrote ${outFile}; ${applied.length} of ${answers.length} lesson(s) applied.`);
  return applied.length === answers.length ? 0 : 1;
}

if (opt('--emit')) {
  console.log(promptFor(opt('--emit')));
} else if (opt('--apply')) {
  const data = parseAnswer(readFileSync(abs(opt('--apply')), 'utf8'));
  process.exit(apply(Array.isArray(data) ? data : [data]));
} else if (opt('--mock')) {
  const answers = opt('--mock').split(',').map((slug) => {
    const l = need(slug);
    const first = [...l.h2][0] ?? null;
    return {
      lesson: slug, hash: l.contentHash, opened_lesson: false,
      concepts: [{ id: `mock-${slug}`.slice(0, 48).replace(/-$/, ''), role: 'core', anchor: l.rank === 0 && l.h2.has('the-big-idea') ? 'the-big-idea' : first, adds: 'Stand-in note: the case in the first section.', films: l.filmList.slice(0, 1).map((f) => f.key), new: { name: `Mock idea of ${slug}`.slice(0, 60), blurb: 'A stand-in idea written by the plumbing test.', area: 'methods', aliases: [`mock question ${slug}`, `mock term ${slug}`] } }],
      near: Object.keys(graph.concepts).length ? { [`mock-${slug}`.slice(0, 48).replace(/-$/, '')]: [{ id: Object.keys(graph.concepts)[0], why: 'A stand-in reason that names one shared mechanism.' }] } : undefined,
      relations: [], notes: 'mock',
    };
  });
  if (!opt('--out') && !flag('--dry')) { console.error('assign --mock writes stand-in data: say --dry, or --out <a scratch file>.'); process.exit(2); }
  process.exit(apply(answers));
} else if (opt('--call')) {
  const key = process.env.ANTHROPIC_API_KEY;
  if (!key) { console.error('ANTHROPIC_API_KEY is not set. Use --emit and --apply to work without it.'); process.exit(2); }
  const headers = { 'content-type': 'application/json', 'x-api-key': key, 'anthropic-version': VERSION };
  const api = async (body) => {
    for (let attempt = 0; ; attempt++) {
      const r = await fetch(`${API}/messages`, { method: 'POST', headers, body: JSON.stringify(body) });
      if (r.ok) return r.json();
      const text = await r.text();
      if ((r.status === 429 || r.status >= 500) && attempt < 4) { await new Promise((ok) => setTimeout(ok, 2000 * 2 ** attempt)); continue; }
      throw new Error(`POST /messages: ${r.status} ${text.slice(0, 400)}`);
    }
  };
  mkdirSync(CACHE_DIR, { recursive: true });
  const stamp = new Date().toISOString().replace(/[:.]/g, '-');
  const answers = [];
  for (const slug of opt('--call').split(',')) {
    const prompt = promptFor(slug);
    // Everything before the lesson (rules, examples, registry) is the same for every lesson, so it is the cached prefix.
    const cut = prompt.indexOf('\nTHE LESSON\n');
    const msg = await api({
      model: MODEL, max_tokens: 8000, thinking: { type: 'adaptive' }, output_config: { effort: opt('--effort', 'medium') },
      system: [{ type: 'text', text: prompt.slice(0, cut), cache_control: { type: 'ephemeral', ttl: '1h' } }],
      messages: [{ role: 'user', content: prompt.slice(cut) + '\nReturn the JSON object only.' }],
    });
    writeFileSync(join(CACHE_DIR, `assign-${slug}-${stamp}.json`), JSON.stringify(msg, null, 1));
    if (msg.stop_reason === 'refusal' || msg.stop_reason === 'max_tokens') { console.error(`${slug}: no answer (${msg.stop_reason})`); continue; }
    try { answers.push(parseAnswer((msg.content ?? []).filter((b) => b.type === 'text').map((b) => b.text).join(''))); }
    catch (e) { console.error(`${slug}: the reply was not JSON (${String(e.message).slice(0, 80)}); raw reply kept in ${CACHE_DIR}`); }
  }
  process.exit(answers.length ? apply(answers) : 1);
} else {
  console.error('Say --list, --emit <slug>, --apply <file>, --call <slugs> or --mock <slug>. See the header of this file.');
  process.exit(2);
}
