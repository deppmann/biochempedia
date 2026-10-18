/**
 * check-figures: every <LessonFigure> in a lesson must point at a file that exists under
 * public/, and its alt text must disclose that it is AI-generated (IMAGE_POLICY.md rule 8).
 */
import { readdir, readFile } from 'node:fs/promises';
import { existsSync } from 'node:fs';
import { join } from 'node:path';

const LESSONS = join(process.cwd(), 'src', 'content', 'lessons');
const failures = [];
let count = 0;
for (const dir of (await readdir(LESSONS, { withFileTypes: true })).filter((d) => d.isDirectory())) {
  const file = join(LESSONS, dir.name, 'lesson.mdx');
  if (!existsSync(file)) continue;
  const text = await readFile(file, 'utf8');
  for (const m of text.matchAll(/<LessonFigure\s[\s\S]*?\/>/g)) {
    count++;
    const src = /src="([^"]+)"/.exec(m[0])?.[1];
    const alt = /alt="([^"]+)"/.exec(m[0])?.[1];
    if (!src || !existsSync(join('public', src))) failures.push(`${dir.name}: figure file missing (${src})`);
    if (!alt || !alt.startsWith('AI-generated illustration:')) failures.push(`${dir.name}: alt must start "AI-generated illustration:" (${src})`);
    if (!/caption="[^"]+"/.test(m[0])) failures.push(`${dir.name}: figure has no caption (${src})`);
  }
}
for (const f of failures) console.error(`✗ check-figures: ${f}`);
if (failures.length) process.exit(1);
console.log(`✓ check-figures: ${count} lesson illustration(s), all present and disclosed.`);
