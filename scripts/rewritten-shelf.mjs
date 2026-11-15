// rewritten-shelf: write src/data/recently-rewritten.json for the homepage "Recently rewritten" strip
// and the "Rewritten on <date>: new text, figures and flashcards" line under each lesson title
// (src/lib/rewritten.ts).
//
//   node scripts/rewritten-shelf.mjs      # after the ship step has updated the production record
//
// Source (2026-11-15): the production record only (production/record/*.jsonl, see
// scripts/production-record.mjs). A lesson is on the shelf when its row says the level-up shipped
// (stage "shipped", levelUp.shipped = the date the rewrite reached the site); `new` is the row's
// `changed` list. Lessons flagged "safety-skipped" are left off (Chris, 2026-11-15), and so are drafts.
// No private notes, file times or git history are read, so every machine and a fresh clone write the
// same file. To fix a wrong date or sentence, change the row:
//   node scripts/production-record.mjs set <slug> shipped=YYYY-MM-DD changed=text,flashcards,film
import { writeFileSync } from 'node:fs';
import { join } from 'node:path';
import { ROOT, readRecord, readTree, shelf } from './production-record.mjs';

const OUT = join(ROOT, 'src/data/recently-rewritten.json');
const list = shelf(readRecord(), await readTree());
writeFileSync(OUT, JSON.stringify(list, null, 1) + '\n');
console.log(`rewritten-shelf: ${list.length} rewritten lessons; newest ${list[0]?.date ?? 'none'}.`);
