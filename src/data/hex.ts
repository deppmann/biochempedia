/* Hex, the mascot (src/components/Hex.astro), holds one prop per subject area. Every course so
   far is biology or biochemistry; physics and math get theirs when those courses exist. */
export type HexPose = 'stand' | 'wave' | 'lean' | 'think' | 'cheer' | 'sleep';
export type HexProp = 'leaf' | 'flask' | 'pendulum' | 'compass' | 'camera';
export const HEX_POSES: HexPose[] = ['stand', 'wave', 'lean', 'think', 'cheer', 'sleep'];

const CHEMISTRY = new Set(['biochemistry']);

export function hexPropFor(courseSlug: string): HexProp {
  return CHEMISTRY.has(courseSlug) ? 'flask' : 'leaf';
}

/* Subject props only. The film library's camera (2026-11-14) is a place prop, not a subject. */
export const HEX_PROPS: { prop: HexProp; subject: string }[] = [
  { prop: 'leaf', subject: 'Biology' },
  { prop: 'flask', subject: 'Chemistry' },
  { prop: 'pendulum', subject: 'Physics' },
  { prop: 'compass', subject: 'Math' },
];
