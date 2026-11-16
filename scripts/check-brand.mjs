#!/usr/bin/env node
/* Brand check (2026-11-15): the site is STEMhop. Fails if the old name, "Biochemistrypedia" in any
   capitalisation, appears in what the build ships to readers and agents (every .html, .txt, .json,
   .xml and .md file under dist/) outside the allow-list below.

   What does not count as the name:
     - an address: biochemistrypedia.com, grad.biochemistrypedia.com and the like (the old domain stays
       registered for good; the site's own address is PRIMARY_HOST in src/lib/site-host.mjs);
     - the frozen identifiers, which are spelled "biochempedia" (localStorage keys, the Worker, R2, D1,
       the package name) and so never match.

   The allow-list is every place the old name is meant to stay. Each entry is an exact phrase; add one
   only for history or for something renaming would break, and say why.

   Run after `npm run build`:  node scripts/check-brand.mjs */
import { readdirSync, readFileSync, statSync, existsSync } from 'node:fs';
import { join, relative } from 'node:path';

const DIST = new URL('../dist/', import.meta.url).pathname;

const ALLOW = [
  // The footer's quiet note, on every page (src/layouts/BaseLayout.astro).
  'Formerly Biochemistrypedia.',
  // The paragraph on the name, /about/ (src/pages/about.astro).
  'gave the site its first name, Biochemistrypedia.',
  // History: the 2026-08-12 milestone and the rename milestone (src/data/updates.ts), shown on
  // /updates/, in its Atom feed and in the About page's latest-updates box.
  'The site becomes Biochemistrypedia at',
  'Biochemistrypedia becomes STEMhop',
  // History: a source label for the teachers' talk (src/data/teacher-sources.ts).
  'Biochemistrypedia repository history',
  // Frozen: the Anki deck name in flashcard exports (src/lib/flashcards.ts). Renaming it would make
  // learners' re-imports land in a second deck beside their existing one, losing their schedules.
  'Biochemistrypedia::',
];

/* The name, not followed by ".com" and not preceded by "." (a subdomain) or "@" (an email address). */
const NAME = /(?<![.@\w])biochemistrypedia(?!\.com)(?![\w-])/gi;
const EXT = /\.(html|txt|json|xml|md)$/;

function* walk(dir) {
  for (const name of readdirSync(dir)) {
    const p = join(dir, name);
    if (statSync(p).isDirectory()) {
      if (name === 'pagefind' || name === '_astro' || name === 'vendor') continue; // search index chunks, bundles, Mol*
      yield* walk(p);
    } else if (EXT.test(name)) yield p;
  }
}

if (!existsSync(DIST)) {
  console.error('check-brand: dist/ is missing. Run `npm run build` first.');
  process.exit(1);
}

let files = 0;
const hits = [];
for (const file of walk(DIST)) {
  files++;
  let text = readFileSync(file, 'utf8');
  if (!/biochemistrypedia/i.test(text)) continue;
  for (const phrase of ALLOW) text = text.split(phrase).join('');
  for (const m of text.matchAll(NAME)) {
    const at = m.index ?? 0;
    hits.push(`${relative(DIST, file)}: …${text.slice(Math.max(0, at - 60), at + 60).replace(/\s+/g, ' ')}…`);
    if (hits.length > 200) break;
  }
}

if (hits.length) {
  console.error(`check-brand: the old name "Biochemistrypedia" appears ${hits.length} time(s) in built files outside the allow-list:`);
  for (const h of hits.slice(0, 50)) console.error('  ' + h);
  if (hits.length > 50) console.error(`  …and ${hits.length - 50} more.`);
  console.error('Rename it to STEMhop, or, if it is history or a frozen identifier, add the exact phrase to ALLOW in scripts/check-brand.mjs with the reason.');
  process.exit(1);
}
console.log(`check-brand: ${files} built files, no stray "Biochemistrypedia".`);
