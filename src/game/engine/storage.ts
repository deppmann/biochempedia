/* Progress + high scores in localStorage. Everything is best-effort: if storage
   is blocked (private mode), the game still plays — it just won't remember. */

export type ModeId =
  | 'build' | 'regulate' | 'diagnose' | 'blitz' // legacy modes
  | 'ledger' | 'autopsy' | 'foundry' | 'mixing' | 'wire' | 'gauntlet'; // the new games
export type Medal = 'none' | 'bronze' | 'silver' | 'gold';

interface Progress {
  /** best[pathwayId][mode] = { score, medal } */
  best: Record<string, Partial<Record<ModeId, { score: number; medal: Medal }>>>;
  /** total ATP earned across all play (the lifetime currency) */
  atp: number;
  /** ISO dates the student played, for the study streak. */
  days: string[];
}

const KEY = 'bcp-arcade:progress';

function load(): Progress {
  try {
    const raw = localStorage.getItem(KEY);
    if (raw) {
      const p = JSON.parse(raw) as Progress;
      return { best: p.best ?? {}, atp: p.atp ?? 0, days: p.days ?? [] };
    }
  } catch {
    /* ignore */
  }
  return { best: {}, atp: 0, days: [] };
}

function save(p: Progress): void {
  try {
    localStorage.setItem(KEY, JSON.stringify(p));
  } catch {
    /* ignore */
  }
}

let state = load();

export const MEDAL_RANK: Record<Medal, number> = { none: 0, bronze: 1, silver: 2, gold: 3 };

export function recordResult(pathwayId: string, mode: ModeId, score: number, medal: Medal, atpEarned: number): void {
  state = load(); // re-read in case another tab wrote
  const p = state;
  p.atp += Math.max(0, atpEarned);
  const forPath = (p.best[pathwayId] ??= {});
  const prev = forPath[mode];
  if (!prev || score > prev.score || MEDAL_RANK[medal] > MEDAL_RANK[prev.medal]) {
    forPath[mode] = {
      score: Math.max(score, prev?.score ?? 0),
      medal: MEDAL_RANK[medal] >= MEDAL_RANK[prev?.medal ?? 'none'] ? medal : (prev?.medal ?? 'none'),
    };
  }
  const today = todayISO();
  if (!p.days.includes(today)) p.days.push(today);
  save(p);
}

export function getBest(pathwayId: string, mode: ModeId): { score: number; medal: Medal } | undefined {
  return load().best[pathwayId]?.[mode];
}

/** Highest medal earned across a pathway's four modes (for the cabinet ring). */
export function pathwayMedal(pathwayId: string): Medal {
  const forPath = load().best[pathwayId];
  if (!forPath) return 'none';
  let best: Medal = 'none';
  for (const v of Object.values(forPath)) {
    if (v && MEDAL_RANK[v.medal] > MEDAL_RANK[best]) best = v.medal;
  }
  return best;
}

export function modesCleared(pathwayId: string): number {
  const forPath = load().best[pathwayId];
  if (!forPath) return 0;
  return Object.values(forPath).filter((v) => v && MEDAL_RANK[v.medal] > 0).length;
}

export function totalAtp(): number {
  return load().atp;
}

/** Consecutive-day study streak ending today (or yesterday). */
export function studyStreak(): number {
  const days = new Set(load().days);
  if (days.size === 0) return 0;
  let streak = 0;
  const d = new Date();
  // allow the streak to still count if they haven't played yet *today*
  if (!days.has(iso(d))) d.setDate(d.getDate() - 1);
  while (days.has(iso(d))) {
    streak++;
    d.setDate(d.getDate() - 1);
  }
  return streak;
}

function iso(d: Date): string {
  return d.toISOString().slice(0, 10);
}
function todayISO(): string {
  return iso(new Date());
}
