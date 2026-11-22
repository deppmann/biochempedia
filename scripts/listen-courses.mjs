// Courses whose lessons get Kokoro narration (Listen + Equation Card "Read aloud").
// Chris, 2026-11-06: never the device voice; every levelled-up course gets Kokoro.
// Chris, 2026-11-21: "I want to make sure that all the lessons are listenable" — every course is voiced.
// Used by scripts/listen-render.mjs (what to render) and scripts/check-listen.mjs (what must have clips).
import { readFileSync, readdirSync, existsSync } from 'node:fs';
import { join } from 'node:path';

export const POLISHED = new Set([
  'biochemistry', 'neuroscience', 'physiology', 'developmental-neuroscience', 'sensory-systems', 'cell-biology', 'genetics', 'ecology-evolution', 'organismal-biology', 'high-school-biology', 'life-science', 'biology-together', 'signaling',
]);

// Courses with a level-up under way. Their lessons not yet levelled (production-record stage other than
// "shipped") are about to get new text, so they wait: listen-render skips them unless named with --only,
// and check-listen warns instead of failing. The level-up voices each lesson as it ships. Remove a
// course from this set when its level-up is finished.
export const LEVEL_UP_UNDERWAY = new Set([]);

/** Slugs waiting for their level-up before they are voiced (read from production/record). */
export function waitingForLevelUp(root = '.') {
  const dir = join(root, 'production/record');
  const out = new Set();
  if (!existsSync(dir)) return out;
  for (const f of readdirSync(dir).filter((x) => x.endsWith('.jsonl'))) {
    for (const line of readFileSync(join(dir, f), 'utf8').split('\n')) {
      if (!line.trim()) continue;
      const r = JSON.parse(line);
      if (LEVEL_UP_UNDERWAY.has(r.course) && r.stage !== 'shipped') out.add(r.slug);
    }
  }
  return out;
}
