#!/usr/bin/env node
/**
 * Quiz answer-key distribution guard (source-level; needs no build).
 *
 * The failure mode this exists for shipped once for real: two lessons went
 * live with every answer at index 0, so a student clicking the first choice
 * every time scored 100%. QuizBlock renders choices in literal array order —
 * there is deliberately no shuffle, because several rationales describe the
 * choices by position — so the authored order is exactly what students see,
 * and this check is the only thing standing between an author's habit and a
 * degenerate key.
 *
 * FAILS when any lesson with ≥4 questions has ≥75% of its answers on one
 * index. WARNS (without failing) at ≥60%, and when one index carries more
 * than 40% of all answers site-wide.
 *
 * Also WARNS (never fails) with a count of MCAT-style questions whose keyed
 * answer is strictly the longest choice — the same length cue that
 * scripts/validate-mcat.mjs polices on passage sets. A test-wise student can
 * pick the longest choice without knowing the biology. Pass --verbose to list
 * each one.
 *
 * Run: node scripts/check-quiz.mjs   (also run by CI on every push)
 */
import { readdir, readFile } from 'node:fs/promises';
import { existsSync } from 'node:fs';
import { join } from 'node:path';

const LESSONS = join(process.cwd(), 'src', 'content', 'lessons');
const HARD = 0.75; // fail
const SOFT = 0.6; // warn
const SITE_WARN = 0.4;

const site = new Map();
const failures = [];
const warnings = [];

// Length-cue lint for mcatQuestions (warn-only). js-yaml ships with Astro; if it
// ever stops resolving, the lint is skipped rather than failing the check.
let yaml = null;
try { yaml = (await import('js-yaml')).default; } catch { /* lint skipped below */ }
const VERBOSE = process.argv.includes('--verbose');
const cue = { total: 0, longest: 0, over30: 0, byCourse: new Map(), items: [] };
function lintLengthCue(slug, text) {
  const fm = /^---\r?\n([\s\S]*?)\r?\n---/.exec(text);
  if (!fm) return;
  let data;
  try { data = yaml.load(fm[1]); } catch { return; }
  if (!data || data.draft || !Array.isArray(data.mcatQuestions)) return;
  const course = data.course ?? 'biochemistry';
  const c = cue.byCourse.get(course) ?? { total: 0, longest: 0 };
  cue.byCourse.set(course, c);
  for (const [i, q] of data.mcatQuestions.entries()) {
    if (!Array.isArray(q?.choices) || !Number.isInteger(q.answer) || q.choices[q.answer] === undefined) continue;
    const L = q.choices.map((x) => String(x).length);
    const k = L[q.answer];
    const others = Math.max(...L.filter((_, j) => j !== q.answer));
    cue.total++; c.total++;
    if (k > others) { cue.longest++; c.longest++; cue.items.push(`${slug} mcat q${i + 1}: keyed answer is the longest choice (${k} vs ${others} characters)`); }
    if (k > 1.3 * others) cue.over30++;
  }
}

for (const dir of (await readdir(LESSONS, { withFileTypes: true })).filter((d) => d.isDirectory())) {
  const file = join(LESSONS, dir.name, 'lesson.mdx');
  if (!existsSync(file)) continue;
  const text = await readFile(file, 'utf8');
  if (yaml) lintLengthCue(dir.name, text);
  // Both practiceQuestions and mcatQuestions carry `answer:` keys; nothing else does.
  const answers = [...text.matchAll(/^\s*answer:\s*(\d+)\s*$/gm)].map((m) => Number(m[1]));
  if (!answers.length) continue;

  // Rationales must never refer to choices by position — students see letters,
  // the files historically mixed 0- and 1-based counting, and any reorder (or a
  // future shuffle) silently falsifies the reference. Cleaned site-wide on
  // 2026-08-13; this keeps it clean.
  for (const m of text.matchAll(/\bchoices? [0-9]\b|\bthe (?:first|second|third|last) (?:choice|option)\b/gi)) {
    failures.push(`${dir.name}: positional choice reference in text: "…${m[0]}…" — name the choice's content instead`);
  }

  const dist = new Map();
  for (const a of answers) {
    dist.set(a, (dist.get(a) ?? 0) + 1);
    site.set(a, (site.get(a) ?? 0) + 1);
  }
  const [topIdx, topCount] = [...dist.entries()].sort((a, b) => b[1] - a[1])[0];
  const share = topCount / answers.length;
  const letter = 'ABCDEF'[topIdx] ?? `#${topIdx}`;
  const line = `${dir.name}: ${topCount}/${answers.length} answers are "${letter}" (${Math.round(share * 100)}%)`;
  if (answers.length >= 4 && share >= HARD) failures.push(line);
  else if (answers.length >= 4 && share >= SOFT) warnings.push(line);
}

const totalQ = [...site.values()].reduce((a, b) => a + b, 0);
for (const [idx, count] of [...site.entries()].sort()) {
  if (count / totalQ > SITE_WARN) {
    warnings.push(
      `site-wide: index ${idx} ("${'ABCDEF'[idx]}") carries ${count}/${totalQ} answers (${Math.round((count / totalQ) * 100)}%)`
    );
  }
}

for (const w of warnings) console.warn(`⚠ check-quiz: ${w}`);
if (!yaml) console.warn('⚠ check-quiz: length-cue lint skipped (js-yaml not found)');
else if (cue.longest) {
  if (VERBOSE) for (const line of cue.items) console.warn(`⚠ check-quiz: ${line}`);
  const per = [...cue.byCourse.entries()].filter(([, v]) => v.longest).sort((a, b) => b[1].longest / b[1].total - a[1].longest / a[1].total)
    .map(([k, v]) => `${k} ${v.longest}/${v.total}`).join(', ');
  console.warn(`⚠ check-quiz: length cue: the keyed answer is strictly the longest choice in ${cue.longest} of ${cue.total} MCAT-style questions (${cue.over30} by more than 30%). By course: ${per}. Warn-only; run with --verbose to list them.`);
}
if (failures.length) {
  console.error(`\n✗ check-quiz: answer keys are exploitably biased — a student clicking the same letter scores far above chance:\n`);
  for (const f of failures) console.error(`  ${f}`);
  console.error(`\n  Fix by reordering choices (and updating \`answer:\`), not by rewriting the questions.`);
  console.error(`  Careful: some rationales describe choices BY POSITION ("the last choice") — reread the rationale of every question you reorder.\n`);
  process.exit(1);
}
console.log(`✓ check-quiz: ${totalQ} answer keys, no lesson ≥${HARD * 100}% on one index${warnings.length ? ` (${warnings.length} warning${warnings.length > 1 ? 's' : ''})` : ''}.`);
