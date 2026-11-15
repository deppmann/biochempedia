/* Hex, the mascot (src/components/Hex.astro), holds one prop per subject area. Every course so
   far is biology or biochemistry; physics and math get theirs when those courses exist.
   Since 2026-11-14 every course also has its own look (COURSE_HEX below): a pose and a prop that
   say what the course is about, drawn in src/data/hex-art.ts. */
import type { HexCoursePose, HexCourseProp } from './hex-art';

export type HexPose = 'stand' | 'wave' | 'lean' | 'think' | 'cheer' | 'sleep' | HexCoursePose;
export type HexProp = 'leaf' | 'flask' | 'pendulum' | 'compass' | 'camera' | HexCourseProp;
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

export interface CourseHex {
  pose: HexPose;
  prop: HexProp;
  /** Short accessible name, "Hex ..." */
  label: string;
}

/* One Hex per course (2026-11-14), so a student can tell the courses apart by their Hex. Keyed by
   course slug; `mcat` and `methods` are the MCAT practice hub and the methods library. Order is the
   order of the character sheet on /hex/. */
export const COURSE_HEX: Record<string, CourseHex> = {
  'biology-together': { pose: 'wave', prop: 'magnifier', label: 'Hex waving, holding a big magnifying glass' },
  'life-science': { pose: 'carry', prop: 'seedling', label: 'Hex carrying a potted seedling on its head' },
  'high-school-biology': { pose: 'lookup', prop: 'crab', label: 'Hex holding up a blue crab' },
  'organismal-biology': { pose: 'kneel', prop: 'snail', label: 'Hex crouching beside a snail on a leaf' },
  'cell-biology': { pose: 'peer', prop: 'microscope', label: 'Hex peering into a microscope' },
  genetics: { pose: 'hold', prop: 'helix', label: 'Hex holding a double helix like a staff' },
  'ecology-evolution': { pose: 'lookup', prop: 'binoculars', label: 'Hex with binoculars and a finch on its head' },
  biochemistry: { pose: 'lookup', prop: 'bubbling-flask', label: 'Hex holding up a bubbling flask' },
  neuroscience: { pose: 'lookup', prop: 'neuron-kite', label: 'Hex flying a neuron like a kite' },
  physiology: { pose: 'hold', prop: 'stethoscope', label: 'Hex holding a stethoscope' },
  signaling: { pose: 'lookup', prop: 'antenna', label: 'Hex with a receptor on its head, catching a signal' },
  'developmental-neuroscience': { pose: 'reach', prop: 'growth-cone', label: 'Hex walking an axon whose growth cone reaches for a cue' },
  'sensory-systems': { pose: 'point', prop: 'eye-chart', label: 'Hex pointing at an eye chart' },
  mcat: { pose: 'stand', prop: 'pencil-stopwatch', label: 'Hex with a pencil and a stopwatch' },
  methods: { pose: 'hold', prop: 'pipette', label: 'Hex holding a pipette' },
};

/** A course's own Hex; a course without one yet holds its subject's prop. */
export function hexFor(courseSlug: string): CourseHex {
  const prop = hexPropFor(courseSlug);
  return COURSE_HEX[courseSlug] ?? { pose: 'stand', prop, label: prop === 'flask' ? 'Hex holding a flask' : 'Hex holding a leaf' };
}
