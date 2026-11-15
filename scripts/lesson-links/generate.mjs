#!/usr/bin/env node
/**
 * Lesson links generator (2026-11-14): asks a model, once per lesson and offline, for "review first",
 * "study next", "elsewhere on the site" and search phrases, cleans the answer against the rules in
 * ./lib.mjs and writes it to src/data/lesson-links.json. The site reads that file at build time, so
 * no model runs when a student visits.
 *
 *   node scripts/lesson-links/generate.mjs --only <slug>[,<slug>…]   refresh named lessons (direct call)
 *   node scripts/lesson-links/generate.mjs --all                      every lesson that is missing or whose
 *                                                                      file changed (Message Batches, half price)
 *   options: --force (ignore the hash), --part elsewhere (replace only that list, keep the rest), --sync / --batch (choose the API), --skim (send a Skim-level
 *            digest instead of the whole text), --effort low|medium (default low), --mock (no API:
 *            a deterministic stand-in, for testing the pipeline), --dry (print what would run),
 *            --resume <batch id> (collect a batch that was already sent)
 *
 * Needs ANTHROPIC_API_KEY in the environment (never written anywhere). Raw answers and a cost ledger go
 * to node_modules/.cache/lesson-links/ (not committed). The catalog of lessons and method films is the
 * cached prefix of every request, so it is billed in full only once per batch.
 *
 * Calls the HTTP API with fetch, as the Worker does, so the repo gains no dependency.
 */
import { readFileSync, writeFileSync, existsSync, mkdirSync, appendFileSync } from 'node:fs';
import { join } from 'node:path';
import { loadSite, catalogText, lessonDigest, cleanRecord, DATA_FILE, ROOT } from './lib.mjs';

export const MODEL = 'claude-sonnet-5-5';
const API = 'https://api.anthropic.com/v1';
const VERSION = '2026-10-21';
/** US dollars per million tokens, standard tier (platform.claude.com pricing, checked 2026-11-14). Batch halves all of it. */
const PRICE = { input: 2, output: 10, cacheWrite1h: 4, cacheWrite5m: 2.5, cacheRead: 0.1 };

const argv = process.argv.slice(2);
const flag = (f) => argv.includes(f);
const opt = (f, d) => { const i = argv.indexOf(f); return i >= 0 ? argv[i + 1] : d; };
const effort = opt('--effort', 'medium');
const LOG = join(ROOT, 'node_modules', '.cache', 'lesson-links');
mkdirSync(LOG, { recursive: true });

const SYSTEM_RULES = `You link lessons on Biochemistrypedia, a free biology website. Its courses run from hands-on activities for ages 5 to 10 (written for the grown-up) through grade 7, high school, college and graduate school. The catalog below lists every live lesson and every method film. For ONE lesson, given in the user message, you choose four things.

1. review_first: up to 3 lessons a student should know BEFORE this one: true prerequisites whose ideas this lesson uses and does not re-teach. Only lessons at the same level or a lower level. Inside the same course, only lessons that come earlier. At high school and below, prefer the lesson one level down that taught the same idea. An empty list is better than a weak link. Never more advanced material.

2. next: up to 3 lessons that build directly on this one. Inside the same course, only later lessons, and prefer the one that really uses this idea over simply the next lesson in order (the page already links the next lesson). In another course, the same level or exactly one level up, never lower and never two levels up; when you go one level up, the reason says the lesson takes the idea further.

3. elsewhere: up to 4 resources in OTHER courses that bear on this lesson. Ids: film:<slug> (the film of that lesson; only lessons with an F: entry), sim:<slug> (that lesson's simulation; only lessons marked S), method:<slug> (a method film from the list). Never this lesson, never a lesson you already chose in 1 or 2, never more than one level above this lesson, and never a method film the user message says is already on the page.

Only real, direct connections: a contrast, an analogy or a shared general skill is not a prerequisite and not a reason to list something. A method film belongs only if this lesson's own content uses that method. An elsewhere item must teach or show the same specific idea; "gives the bigger picture" or "places it in context" is not enough. Judge a film only by its title and take-homes in the catalog: if they do not show that it covers the idea, leave it out. Most lessons have only one or two good elsewhere items, and some have none. Fewer, sure links beat more, loose ones. When nothing fits a list, return it empty; never fill a slot with a placeholder such as "Not applicable".

Every reason is ONE sentence of at most 20 words (at most 16 for levels 0 and 1), in plain words a reader of this lesson's level understands. It names the real idea that joins the two (for example: "You need the Nernst equation from there to work out the resting potential here."). Never write "is related to" or "covers similar ideas". Do not name the other item's course or level in the reason (the page shows them), and do not restate its title. For level 0 activities, write reasons for the grown-up.

4. search_phrases: 8 to 15 things a student might really type into a search box when this lesson is the answer, whose words are NOT already in the lesson's title or section headings. Mix everyday questions ("why do i get tired when i run"), everyday names for technical terms ("goosebumps", "brain freeze"), one or two common misspellings of key terms, written as a student would type them (for mitosis, write just "mytosis"; never the words "spelled" or "misspelled"), and short exam-style keyword strings. Lower case, 1 to 8 words each, one idea each. Each must be specific to this lesson: leave out a phrase another lesson in the catalog answers better. Never a request for medical advice (no doses, symptoms, treatments, "should i"), and never a brand, product, company or test-prep name.

Use only slugs and ids that appear in the catalog, copied exactly. Accuracy matters more than filling the lists.

CATALOG
`;

const SCHEMA = {
  type: 'object',
  additionalProperties: false,
  required: ['review_first', 'next', 'elsewhere', 'search_phrases'],
  properties: {
    review_first: { type: 'array', items: { type: 'object', additionalProperties: false, required: ['slug', 'reason'], properties: { slug: { type: 'string' }, reason: { type: 'string' } } } },
    next: { type: 'array', items: { type: 'object', additionalProperties: false, required: ['slug', 'reason'], properties: { slug: { type: 'string' }, reason: { type: 'string' } } } },
    elsewhere: { type: 'array', items: { type: 'object', additionalProperties: false, required: ['id', 'reason'], properties: { id: { type: 'string' }, reason: { type: 'string' } } } },
    search_phrases: { type: 'array', items: { type: 'string' } },
  },
};

function params(lesson, site, catalog) {
  return {
    model: MODEL,
    max_tokens: 8000,
    thinking: { type: 'adaptive' },
    output_config: { effort, format: { type: 'json_schema', schema: SCHEMA } },
    system: [{ type: 'text', text: SYSTEM_RULES + catalog, cache_control: { type: 'ephemeral', ttl: '1h' } }],
    messages: [{ role: 'user', content: lessonDigest(lesson, site, { full: !flag('--skim') }) + '\n\n' + levelRule(lesson, site) + '\n\nChoose the links and phrases for this lesson.' }],
  };
}

/** The levels each list may draw from, spelled out for this lesson (the rules in lib.mjs enforce them). */
function levelRule(l, site) {
  const name = (r) => `${r} ${site.STAGES[r].title}`;
  const upTo = (r) => Array.from({ length: Math.min(r, site.STAGES.length - 1) + 1 }, (_v, i) => name(i)).join(', ');
  const up = Math.min(l.rank + 1, site.STAGES.length - 1);
  return `This lesson is level ${name(l.rank)}, lesson ${l.n} of ${l.of} in ${l.courseTitle}. Allowed levels: review_first ${upTo(l.rank)} (in this course, only lessons 1 to ${l.n - 1}); next ${l.rank === up ? name(l.rank) : `${name(l.rank)} or ${name(up)}`} (in this course, only lessons ${l.n + 1} to ${l.of}); elsewhere ${upTo(up)}, in other courses only.`;
}

const headers = () => {
  const key = process.env.ANTHROPIC_API_KEY;
  if (!key) { console.error('ANTHROPIC_API_KEY is not set.'); process.exit(2); }
  return { 'content-type': 'application/json', 'x-api-key': key, 'anthropic-version': VERSION };
};

async function api(path, body, method = body ? 'POST' : 'GET') {
  for (let attempt = 0; ; attempt++) {
    const r = await fetch(`${API}${path}`, { method, headers: headers(), body: body ? JSON.stringify(body) : undefined });
    if (r.ok) return r;
    const text = await r.text();
    if ((r.status === 429 || r.status >= 500) && attempt < 4) { await new Promise((ok) => setTimeout(ok, 2000 * 2 ** attempt)); continue; }
    throw new Error(`${method} ${path}: ${r.status} ${text.slice(0, 400)}`);
  }
}

/** Dollars for one response's usage. `batch` halves it. */
function cost(u, batch) {
  const c = u.cache_creation ?? {};
  const w1h = c.ephemeral_1h_input_tokens ?? 0;
  const w5m = c.ephemeral_5m_input_tokens ?? Math.max(0, (u.cache_creation_input_tokens ?? 0) - w1h);
  const d = ((u.input_tokens ?? 0) * PRICE.input + (u.output_tokens ?? 0) * PRICE.output + w1h * PRICE.cacheWrite1h + w5m * PRICE.cacheWrite5m + (u.cache_read_input_tokens ?? 0) * PRICE.cacheRead) / 1e6;
  return batch ? d / 2 : d;
}

/** A message's JSON answer, or an error string. */
function answerOf(msg) {
  if (msg.stop_reason === 'refusal') return { error: `refusal (${msg.stop_details?.category ?? 'no category'})` };
  if (msg.stop_reason === 'max_tokens') return { error: 'hit max_tokens' };
  const text = (msg.content ?? []).filter((b) => b.type === 'text').map((b) => b.text).join('');
  try { return { json: JSON.parse(text) }; } catch { return { error: `not JSON: ${text.slice(0, 120)}` }; }
}

function mockAnswer(l, site) {
  const same = [...site.lessons.values()].filter((x) => x.course === l.course);
  const prev = same.find((x) => x.n === l.n - 1);
  const next = same.find((x) => x.n === l.n + 2);
  return {
    review_first: prev ? [{ slug: prev.slug, reason: `You use the main idea of "${prev.title}" again here.` }] : [],
    next: next ? [{ slug: next.slug, reason: `It builds on this lesson's main idea.` }] : [],
    elsewhere: [],
    search_phrases: [`mock phrase for ${l.slug}`],
  };
}

// ------------------------------------------------------------------ run

const site = await loadSite();
const catalog = catalogText(site);
const data = existsSync(DATA_FILE) ? JSON.parse(readFileSync(DATA_FILE, 'utf8')) : { lessons: {} };

let targets;
const PILOT = ['alive-or-not', 'predicting-traits', 'diffusion-and-osmosis', 'respiration-and-atp', 'punnett-squares', 'adaptive-immunity', 'mendels-peas', 'cell-death', 'island-biogeography', 'action-potential', 'citric-acid-cycle', 'gtpase-switches'];
if (opt('--only')) targets = opt('--only').split(',');
else if (flag('--pilot')) targets = PILOT.filter((s) => site.lessons.has(s));
else if (flag('--all')) targets = [...site.lessons.keys()];
else if (!opt('--resume')) { console.error('Say --only <slugs>, --pilot, --all or --resume <batch id>.'); process.exit(2); }
if (targets) {
  const unknown = targets.filter((s) => !site.lessons.has(s));
  if (unknown.length) { console.error(`Not live lessons: ${unknown.join(', ')}`); process.exit(2); }
  if (!flag('--force')) targets = targets.filter((s) => data.lessons[s]?.hash !== site.lessons.get(s).hash);
  console.log(`${targets.length} lesson(s) to generate${flag('--force') ? '' : ' (missing or changed)'}.`);
  if (flag('--dry') || !targets.length) { console.log(targets.join('\n')); process.exit(0); }
}

const stamp = new Date().toISOString().replace(/[:.]/g, '-');
const ledger = join(LOG, 'ledger.jsonl');
const answers = new Map();   // slug -> { json } | { error }
let spent = 0;
const tokens = { input: 0, output: 0, cacheWrite: 0, cacheRead: 0 };
const tally = (u, batch, slug) => {
  const d = cost(u, batch);
  spent += d;
  tokens.input += u.input_tokens ?? 0; tokens.output += u.output_tokens ?? 0;
  tokens.cacheWrite += u.cache_creation_input_tokens ?? 0; tokens.cacheRead += u.cache_read_input_tokens ?? 0;
  appendFileSync(ledger, JSON.stringify({ at: stamp, slug, batch, usd: +d.toFixed(5), usage: u }) + '\n');
};

if (flag('--mock')) {
  for (const s of targets) answers.set(s, { json: mockAnswer(site.lessons.get(s), site) });
} else if (opt('--resume') || (!flag('--sync') && (flag('--batch') || targets.length > 3))) {
  let id = opt('--resume');
  if (!id) {
    const requests = targets.map((s) => ({ custom_id: s, params: params(site.lessons.get(s), site, catalog) }));
    const b = await (await api('/messages/batches', { requests })).json();
    id = b.id;
    console.log(`Batch ${id} sent (${requests.length} requests). Collect later with --resume ${id} if this stops.`);
    appendFileSync(join(LOG, 'batches.log'), `${stamp} ${id} ${requests.length}\n`);
  }
  let b;
  for (;;) {
    b = await (await api(`/messages/batches/${id}`)).json();
    if (b.processing_status === 'ended') break;
    console.log(`  ${new Date().toISOString().slice(11, 19)} ${JSON.stringify(b.request_counts)}`);
    await new Promise((ok) => setTimeout(ok, 30_000));
  }
  const text = await (await fetch(b.results_url, { headers: headers() })).text();
  writeFileSync(join(LOG, `batch-${id}.jsonl`), text);
  for (const line of text.split('\n').filter(Boolean)) {
    const r = JSON.parse(line);
    if (r.result.type !== 'succeeded') { answers.set(r.custom_id, { error: `${r.result.type}: ${JSON.stringify(r.result.error ?? '').slice(0, 200)}` }); continue; }
    tally(r.result.message.usage, true, r.custom_id);
    answers.set(r.custom_id, answerOf(r.result.message));
  }
} else {
  for (const s of targets) {
    const msg = await (await api('/messages', params(site.lessons.get(s), site, catalog))).json();
    writeFileSync(join(LOG, `sync-${s}-${stamp}.json`), JSON.stringify(msg, null, 1));
    tally(msg.usage, false, s);
    answers.set(s, answerOf(msg));
  }
}

// ------------------------------------------------------------------ clean and write

const today = new Date().toISOString().slice(0, 10);
const report = [];
let failed = 0;
for (const [slug, a] of answers) {
  const l = site.lessons.get(slug);
  if (!l || a.error) { failed++; report.push(`FAIL ${slug}: ${a.error ?? 'not a live lesson'}`); continue; }
  const j = a.json;
  const raw = {
    hash: l.hash, generated: today,
    before: (j.review_first ?? []).map((x) => ({ slug: x.slug, why: x.reason })),
    after: (j.next ?? []).map((x) => ({ slug: x.slug, why: x.reason })),
    elsewhere: (j.elsewhere ?? []).map((x) => ({ id: x.id, why: x.reason })),
    search: j.search_phrases ?? [],
  };
  // --part elsewhere: replace only the elsewhere list, keeping the rest of the existing record.
  const prior = data.lessons[slug];
  if (opt('--part') === 'elsewhere' && prior) Object.assign(raw, { before: prior.before, after: prior.after, search: prior.search });
  const { record, dropped } = cleanRecord(slug, raw, site);
  data.lessons[slug] = record;
  report.push(`ok   ${slug}: ${record.before.length}/${record.after.length}/${record.elsewhere.length} links, ${record.search.length} phrases${dropped.length ? `; dropped ${dropped.join('; ')}` : ''}`);
}
writeFileSync(join(LOG, `report-${stamp}.txt`), report.join('\n') + '\n');

const lessons = Object.fromEntries(Object.keys(data.lessons).sort().map((k) => [k, data.lessons[k]]));
const out = {
  version: 1,
  model: flag('--mock') ? 'mock' : MODEL,
  updated: today,
  about: 'Written once per lesson, offline, by scripts/lesson-links/generate.mjs and cleaned by its rules (scripts/lesson-links/lib.mjs); checked in CI by scripts/check-lesson-links.mjs. A record is tied to its lesson file by hash: refresh with --only <slug> after the lesson changes.',
  lessons,
};
writeFileSync(DATA_FILE, JSON.stringify(out, null, 1) + '\n');
console.log(report.join('\n'));
console.log(`\n${answers.size - failed} written, ${failed} failed. Spent $${spent.toFixed(4)}; tokens ${JSON.stringify(tokens)}.`);
if (answers.size) console.log(`Per lesson: $${(spent / answers.size).toFixed(4)}.`);
process.exit(failed ? 1 : 0);
