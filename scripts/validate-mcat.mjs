#!/usr/bin/env node
/**
 * Validate MCAT passage sets (src/content/mcat-sets/*.json) against the format rules
 * of docs/expansion/mcat/RUBRIC.md. Run: node scripts/validate-mcat.mjs [file…]
 * Exits 1 on any failure. Also run in CI with the other checks.
 *
 * It checks what a machine can: schema, four choices, one key, the length cue, banned
 * options, explanation-shape parity, numeric ordering, answer spread, skill mix, word
 * count, figure data, and that every lesson link points at a real lesson and heading.
 * Whether an item is a good MCAT question is for the blind solvers and the judge.
 */
import { readdir, readFile } from 'node:fs/promises';
import { join } from 'node:path';
import GithubSlugger from 'github-slugger';

const DIR = join(process.cwd(), 'src', 'content', 'mcat-sets');
const LESSONS = join(process.cwd(), 'src', 'content', 'lessons');
const CATS = /^(1[ABCD]|2[ABC]|3[AB]|4[ABCDE]|5[ABCDE])$/;
const BANNED = /\b(all of the above|none of the above|both [abcd] and [abcd])\b/i;
const errors = [];
const warns = [];
const err = (f, m) => errors.push(`${f}: ${m}`);
const warn = (f, m) => warns.push(`${f}: ${m}`);

const anchorCache = new Map();
async function anchorsOf(slug) {
  if (!anchorCache.has(slug)) {
    try {
      const body = await readFile(join(LESSONS, slug, 'lesson.mdx'), 'utf8');
      const s = new GithubSlugger();
      const set = new Set();
      for (const m of body.matchAll(/^#{2,3}\s+(.+?)\s*$/gm)) set.add(s.slug(m[1].replace(/[*_`]/g, '')));
      anchorCache.set(slug, set);
    } catch { anchorCache.set(slug, null); }
  }
  return anchorCache.get(slug);
}

const words = (t) => String(t).trim().split(/\s+/).filter(Boolean).length;
const numeric = (c) => { const m = /^\s*[−-]?\d+(\.\d+)?/.exec(c.replace('−', '-')); return m ? parseFloat(m[0].replace('−', '-')) : null; };

async function checkLink(f, where, link) {
  if (!link || !link.slug) return err(f, `${where}: missing lesson link`);
  const a = await anchorsOf(link.slug);
  if (!a) return err(f, `${where}: no lesson "${link.slug}"`);
  if (link.anchor && !a.has(link.anchor)) err(f, `${where}: lesson "${link.slug}" has no heading anchor "${link.anchor}"`);
}

async function checkSet(f, s) {
  for (const k of ['id', 'section', 'title', 'categories', 'passage', 'source', 'questions', 'lessons']) if (s[k] === undefined) err(f, `missing "${k}"`);
  if (!['bb', 'cp'].includes(s.section)) err(f, 'section must be "bb" or "cp"');
  if (s.id && !/^[a-z0-9-]+$/.test(s.id)) err(f, 'id must be lowercase-dashed');
  for (const c of s.categories ?? []) if (!CATS.test(c)) err(f, `bad category ${c}`);
  const pw = (s.passage ?? []).reduce((n, p) => n + words(p), 0);
  if (pw < 250 || pw > 450) err(f, `passage is ${pw} words (250–450)`);
  if (!/illustrative|adapted from|data from|based on/i.test(s.source ?? '')) err(f, 'source line must cite the study or say the data are illustrative');
  for (const l of s.lessons ?? []) await checkLink(f, 'set lesson', l);
  for (const fig of s.figures ?? []) {
    if (fig.type === 'table') {
      if (!Array.isArray(fig.columns) || !Array.isArray(fig.rows) || !fig.rows.every((r) => r.length === fig.columns.length)) err(f, `table ${fig.id}: rows must match columns`);
    } else if (['line', 'bar', 'scatter'].includes(fig.type)) {
      if (!fig.xLabel || !fig.yLabel || !Array.isArray(fig.series) || !fig.series.every((sr) => Array.isArray(sr.points) && sr.points.every((p) => p.length >= 2 && p.every((v) => typeof v === 'number' || v === null)))) err(f, `figure ${fig.id}: needs xLabel, yLabel and numeric series points`);
    } else err(f, `figure ${fig.id}: unknown type ${fig.type}`);
    if (!fig.caption) err(f, `figure ${fig.id}: needs a caption`);
  }
  const qs = s.questions ?? [];
  if (qs.length < 4 || qs.length > 6) err(f, `${qs.length} questions (4–6)`);
  const skills = qs.map((q) => q.skill);
  if (!skills.includes(4)) err(f, 'no SIRS 4 (data) question');
  if (!skills.includes(3)) err(f, 'no SIRS 3 (design) question');
  if (!skills.includes(2)) err(f, 'no SIRS 2 question');
  if (skills.filter((x) => x === 1).length > 2) err(f, 'more than two SIRS 1 questions');
  const pos = {};
  let longestCorrect = 0;
  for (const [i, q] of qs.entries()) {
    const w = `q${i + 1}`;
    if (!Array.isArray(q.choices) || q.choices.length !== 4) { err(f, `${w}: needs exactly 4 choices`); continue; }
    if (!Number.isInteger(q.answer) || q.answer < 0 || q.answer > 3) err(f, `${w}: answer must be 0–3`);
    if (![1, 2, 3, 4].includes(q.skill)) err(f, `${w}: skill must be 1–4`);
    if (!CATS.test(q.category ?? '')) err(f, `${w}: bad category`);
    if (!q.stem || words(q.stem) < 6) err(f, `${w}: stem too short`);
    if (!Array.isArray(q.why) || q.why.length !== 4 || q.why.some((x) => !x || words(x) < 4)) err(f, `${w}: needs a rationale for each of the 4 choices ("why")`);
    await checkLink(f, w, q.lesson);
    pos[q.answer] = (pos[q.answer] ?? 0) + 1;
    const L = q.choices.map((c) => c.length);
    const k = L[q.answer];
    const others = L.filter((_, j) => j !== q.answer);
    if (k >= Math.max(...others)) longestCorrect++;
    if (k > 1.3 * Math.max(...others)) err(f, `${w}: correct choice is over 30% longer than every other choice`);
    if (q.choices.some((c) => BANNED.test(c))) err(f, `${w}: banned option (all/none of the above, both A and B)`);
    const bec = q.choices.map((c) => /\bbecause\b/i.test(c));
    if (bec.some(Boolean) && !bec.every(Boolean)) err(f, `${w}: "because" appears in some choices but not all`);
    const abs = q.choices.map((c) => /\b(always|never)\b/i.test(c));
    if (abs.some(Boolean) && !abs[q.answer] && abs.filter(Boolean).length === 3) warn(f, `${w}: absolutes only in the wrong choices`);
    const nums = q.choices.map(numeric);
    if (nums.every((x) => x !== null)) {
      const asc = nums.every((x, j) => j === 0 || x >= nums[j - 1]);
      const desc = nums.every((x, j) => j === 0 || x <= nums[j - 1]);
      if (!asc && !desc) err(f, `${w}: numeric choices must be in order`);
    }
  }
  if (qs.length && longestCorrect > Math.ceil(qs.length / 3)) err(f, `correct choice is the longest in ${longestCorrect} of ${qs.length} questions (max ${Math.ceil(qs.length / 3)})`);
  for (const [p, n] of Object.entries(pos)) if (n > 2) err(f, `answer position ${'ABCD'[p]} used ${n} times (max 2)`);
}

const args = process.argv.slice(2);
let files;
try { files = args.length ? args : (await readdir(DIR)).filter((x) => x.endsWith('.json')).map((x) => join(DIR, x)); } catch { files = []; }
const ids = new Set();
for (const f of files) {
  let s;
  try { s = JSON.parse(await readFile(f, 'utf8')); } catch (e) { err(f, `not valid JSON: ${e.message}`); continue; }
  if (ids.has(s.id)) err(f, `duplicate id ${s.id}`);
  ids.add(s.id);
  await checkSet(f.split('/').pop(), s);
}
for (const w of warns) console.warn('warn:', w);
if (errors.length) { for (const e of errors) console.error('✗', e); console.error(`✗ validate-mcat: ${errors.length} problem(s) in ${files.length} set(s)`); process.exit(1); }
console.log(`✓ validate-mcat: ${files.length} passage set(s) pass the format rules.`);
