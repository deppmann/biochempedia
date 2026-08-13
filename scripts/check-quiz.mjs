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

for (const dir of (await readdir(LESSONS, { withFileTypes: true })).filter((d) => d.isDirectory())) {
  const file = join(LESSONS, dir.name, 'lesson.mdx');
  if (!existsSync(file)) continue;
  const text = await readFile(file, 'utf8');
  // Both practiceQuestions and mcatQuestions carry `answer:` keys; nothing else does.
  const answers = [...text.matchAll(/^\s*answer:\s*(\d+)\s*$/gm)].map((m) => Number(m[1]));
  if (!answers.length) continue;

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
if (failures.length) {
  console.error(`\n✗ check-quiz: answer keys are exploitably biased — a student clicking the same letter scores far above chance:\n`);
  for (const f of failures) console.error(`  ${f}`);
  console.error(`\n  Fix by reordering choices (and updating \`answer:\`), not by rewriting the questions.`);
  console.error(`  Careful: some rationales describe choices BY POSITION ("the last choice") — reread the rationale of every question you reorder.\n`);
  process.exit(1);
}
console.log(`✓ check-quiz: ${totalQ} answer keys, no lesson ≥${HARD * 100}% on one index${warnings.length ? ` (${warnings.length} warning${warnings.length > 1 ? 's' : ''})` : ''}.`);
