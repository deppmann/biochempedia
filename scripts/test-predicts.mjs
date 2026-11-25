#!/usr/bin/env node
/**
 * The collector behind "Try the Predict questions again" (src/lib/predicts.ts).
 * No build and no network (Node 22.18+ reads the .ts file as it is).
 *
 * Run: node scripts/test-predicts.mjs
 */
import assert from 'node:assert/strict';
import { readdirSync, readFileSync, existsSync } from 'node:fs';
import { join } from 'node:path';
import { predictSources, predictsOf } from '../src/lib/predicts.ts';

let n = 0;
const check = async (name, fn) => { await fn(); n++; console.log(`ok  ${name}`); };
const box = (label, q, a, summary = 'Check your prediction') => `**${label}.** ${q}\n\n<details>\n<summary>${summary}</summary>\n\n${a}\n\n</details>\n`;

await check('a plain pair, with its section and number', () => {
  const p = predictSources(`## First part\n\nText.\n\n${box('Predict 2', 'What happens?', 'It falls.')}`);
  assert.deepEqual(p, [{ label: 'Predict 2', question: 'What happens?', check: 'Check your prediction', answer: 'It falls.', heading: 'First part' }]);
});
await check('numbered parts under the question are kept; the lesson\'s own fold words are kept', () => {
  const p = predictSources(box('Predict', 'Two things.\n\n1. One?\n2. Two?', 'Yes.\n\n| a | b |\n|---|---|\n| 1 | 2 |', 'Check the table'));
  assert.equal(p.length, 1);
  assert.match(p[0].question, /2\. Two\?$/);
  assert.equal(p[0].check, 'Check the table');
});
await check('left out: no fold straight after, a component, a list step, a fold that never closes', () => {
  assert.equal(predictSources('**Predict.** What?\n\nMore text.\n\n## Next\n\n<details>\n<summary>Check</summary>\n\nA.\n\n</details>').length, 0);
  assert.equal(predictSources('**Predict.** What?\n\n<TreeRemodel />\n\n<details>\n<summary>Check</summary>\n\nA.\n\n</details>').length, 0);
  assert.equal(predictSources(box('Predict', 'What?', 'See this.\n\n<LessonFigure src="/x.webp" width={1200} />')).length, 0);
  assert.equal(predictSources('3. **Predict.** Ask your child what will happen.\n').length, 0);
  assert.equal(predictSources('**Predict.** What?\n\n<details>\n<summary>Check</summary>\n\nA.\n').length, 0);
});
await check('one bad pair does not hide the next good one', () => {
  const p = predictSources(`${box('Predict 1', 'Q1 <Sim />', 'A1')}\n${box('Predict 2', 'Q2', 'A2')}`);
  assert.deepEqual(p.map((x) => x.label), ['Predict 2']);
});
await check('rendered: Markdown, subscripts as in the lesson, and the section anchor', async () => {
  const [p] = await predictsOf(`## Why it's "quiet"\n\n${box('Predict', 'Is E_K **below** rest?', '- yes\n- at 10^-6 M')}`, [{ depth: 2, slug: 'why-its-quiet', text: 'Why it’s “quiet”' }]);
  assert.match(p.questionHtml, /E<sub>K<\/sub> <strong>below<\/strong>/);
  assert.match(p.answerHtml, /<li>yes<\/li>/);
  assert.match(p.answerHtml, /10<sup>/);
  assert.equal(p.sectionSlug, 'why-its-quiet');
});
await check('every lesson: most Predict boxes are collected, none with a component or an empty side', () => {
  const root = join(process.cwd(), 'src', 'content', 'lessons');
  let total = 0, got = 0;
  for (const d of readdirSync(root)) {
    const f = join(root, d, 'lesson.mdx');
    if (!existsSync(f)) continue;
    const body = readFileSync(f, 'utf8').replace(/^---[\s\S]*?\n---\n/, '');
    total += (body.match(/\*\*Predict(?: \d+)?\.\*\*/g) ?? []).length;
    for (const p of predictSources(body)) {
      got++;
      assert.ok(p.question && p.answer, `${d}: empty side`);
      assert.ok(!/<[A-Z]|[{}]/.test(p.question + p.answer), `${d}: a component got through`);
      assert.ok(p.question.split(/\s+/).length <= 160, `${d}: question too long`);
    }
  }
  console.log(`    ${got} of ${total} Predict boxes collected`);
  assert.ok(total === 0 || got / total > 0.9, `only ${got} of ${total} collected`);
});
console.log(`\n${n} checks passed`);
