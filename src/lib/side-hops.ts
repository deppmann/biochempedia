/* Side Hops (2026-11-18): short true stories, myths and things to try that sit beside a lesson, plus
   one narrated audio segment. Each lesson that has them has one file, src/data/side-hops/<slug>.json,
   written by scripts/side-hops/import-kit.mjs and checked by scripts/check-side-hops.mjs. A lesson
   with no file renders as it always has. The lesson's own text (lesson.mdx) is never edited. */
import type { HexPose } from '../data/hex';

export type SideHopKind = 'real-world-case' | 'true-story' | 'see-or-do' | 'myth' | 'analogy';

export interface SideHop {
  /** The exact text of the ## heading whose section this card closes. */
  afterHeading: string;
  kind: SideHopKind;
  title: string;
  text: string;
  sources: { citation: string; url: string }[];
  /** Optional picture (2026-11-21). The file is side-hops/<slug>-<n>.jpg, kept in R2 like the audio.
   *  alt starts "AI-generated illustration:"; caption is the one-line take-home shown under it. */
  image?: { file: string; alt: string; caption: string; width: number; height: number };
}

export interface SideHopsData {
  slug: string;
  updated: string;
  hops: SideHop[];
  audio: {
    title: string;
    /** Path under the site root, side-hops/<slug>.mp3. Kept in R2, like the films. */
    file: string;
    durationSec: number;
    /** Where the voice comes from, in plain words (shown on the page). */
    narration: string;
    transcript: string;
  };
}

/** What a reader sees for each kind, and the pose Hex takes on that card. */
export const KIND_LOOK: Record<SideHopKind, { label: string; pose: HexPose }> = {
  'real-world-case': { label: 'In real life', pose: 'lean' },
  'true-story': { label: 'True story', pose: 'cheer' },
  'see-or-do': { label: 'Try this', pose: 'wave' },
  myth: { label: 'Myth check', pose: 'think' },
  analogy: { label: 'Picture this', pose: 'stand' },
};

const FILES = import.meta.glob<{ default: SideHopsData }>('../data/side-hops/*.json', { eager: true });

export function sideHopsFor(slug: string): SideHopsData | undefined {
  return Object.values(FILES).map((m) => m.default).find((d) => d.slug === slug);
}
