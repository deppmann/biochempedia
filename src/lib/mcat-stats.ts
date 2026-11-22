/* Lightweight, browser-only MCAT practice history for the stats view.
   It is separate from review progress: each submitted answer is one observation, while
   the review queue continues to track first-try mastery. */

export const MCAT_STATS_KEY = 'stemhop:mcat-stats:v1';
export interface McatAnswerRecord { t: number; subject: string; correct: boolean }
const LIMIT = 5000;

function valid(value: unknown): value is McatAnswerRecord[] {
  return Array.isArray(value) && value.every((r) => r && typeof r === 'object'
    && Number.isFinite(r.t) && typeof r.subject === 'string'
    && typeof r.correct === 'boolean');
}

export function readMcatStats(): McatAnswerRecord[] {
  try {
    const raw = window.localStorage.getItem(MCAT_STATS_KEY);
    if (!raw) return [];
    const parsed: unknown = JSON.parse(raw);
    return valid(parsed) ? parsed : [];
  } catch { return []; }
}

/** Record one answered question. Subject is an MCAT category such as `1A`. */
export function recordMcatAnswer(subject: string, correct: boolean, at = Date.now()): void {
  if (!subject || !Number.isFinite(at)) return;
  try {
    const history = readMcatStats();
    history.push({ t: at, subject, correct });
    window.localStorage.setItem(MCAT_STATS_KEY, JSON.stringify(history.slice(-LIMIT)));
  } catch { /* storage blocked or full: this visit still works */ }
}
