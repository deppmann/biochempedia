/* Refresh src/data/updates-prs.json: the number and merge date of every merged pull
   request, for the pace chart on /updates/. Run by hand after notable merges:
     node scripts/updates-prs.mjs
   Needs the GitHub CLI signed in. The build only reads the JSON, so it never calls GitHub. */
import { execFileSync } from 'node:child_process';
import { writeFileSync } from 'node:fs';

const raw = execFileSync('gh', ['pr', 'list', '--state', 'merged', '--limit', '2000', '--json', 'number,mergedAt,title'], { encoding: 'utf8' });
const prs = JSON.parse(raw)
  .map((p) => ({ n: p.number, d: p.mergedAt.slice(0, 10), t: p.title }))
  .sort((a, b) => a.n - b.n);
writeFileSync(new URL('../src/data/updates-prs.json', import.meta.url), JSON.stringify(prs) + '\n');
console.log(`updates-prs.json: ${prs.length} merged pull requests, last ${prs.at(-1)?.d}`);

// Every change listed under a milestone should have a plain-words line for the page.
import { readFileSync } from 'node:fs';
const src = readFileSync(new URL('../src/data/updates.ts', import.meta.url), 'utf8');
const listed = [...src.matchAll(/prs: \[([0-9, ]*)\]/g)].flatMap((m) => m[1].split(',').map((s) => Number(s.trim())).filter(Boolean));
const notes = JSON.parse(readFileSync(new URL('../src/data/updates-pr-notes.json', import.meta.url), 'utf8'));
const missing = listed.filter((n) => !notes[String(n)]);
if (missing.length) console.log(`No plain-words line yet in src/data/updates-pr-notes.json for: ${missing.map((n) => '#' + n).join(', ')}`);
