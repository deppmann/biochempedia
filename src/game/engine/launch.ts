/* Direct-link resolution for /play?game=…&pathway=…|puzzle=…&from=<lesson slug>.
   Pure (no DOM) so it can be unit-checked from node. */
import type { Pathway } from '../types';
import { DEMANDS } from './games/wireCellLogic';

export const GAME_IDS = ['ledger', 'autopsy', 'wire', 'foundry', 'mixing', 'gauntlet'] as const;
export type GameId = (typeof GAME_IDS)[number];

/** Per-lesson context, generated at build time in play.astro. */
export interface LessonCtx {
  slug: string;
  title: string;
  /** 1-based position in the homepage order. */
  n: number;
  nextSlug?: string;
  nextTitle?: string;
}
export type LessonMap = Record<string, Omit<LessonCtx, 'slug'>>;

export interface LaunchRequest {
  game?: GameId;
  pathway?: string;
  puzzle?: string;
  lesson?: LessonCtx;
}

/** Games whose pathway picker an optional `pathway` param can skip. */
const PATHWAY_GAMES: ReadonlySet<string> = new Set(['ledger', 'autopsy']);

export function resolveLaunch(search: string, pathways: Pathway[], lessons: LessonMap): LaunchRequest {
  const q = new URLSearchParams(search);
  const out: LaunchRequest = {};
  const from = q.get('from');
  if (from && Object.prototype.hasOwnProperty.call(lessons, from)) out.lesson = { slug: from, ...lessons[from] };
  const game = q.get('game');
  if (game && (GAME_IDS as readonly string[]).includes(game)) {
    out.game = game as GameId;
    const pathway = q.get('pathway');
    if (pathway && PATHWAY_GAMES.has(game) && pathways.some((p) => p.id === pathway)) out.pathway = pathway;
    const puzzle = q.get('puzzle');
    if (puzzle && game === 'wire' && DEMANDS.some((d) => d.id === puzzle)) out.puzzle = puzzle;
  }
  return out;
}
