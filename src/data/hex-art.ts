/* =============================================================================
   Hex in a course's own pose (2026-11-14)
   -----------------------------------------------------------------------------
   Every course has its own Hex: a pose plus a prop that says what the course is
   about (src/data/hex.ts maps course to look). The six basic poses and the
   subject props stay drawn in Hex.astro's template; the course looks are drawn
   here, as SVG markup in the same 72-unit box and the same navy line and gold,
   and Hex.astro inserts them. Kept as strings so one function draws a look for
   the site and for any script that wants the same picture.

   Units: the body is the hexagon centred on (32, 30), feet on y = 61. A prop
   draws its own right arm (and left arm when it needs it) because the hand has
   to meet the prop. Props are stylised icons, never molecular structures.
   ============================================================================ */

export type HexCoursePose = 'peer' | 'kneel' | 'lookup' | 'reach' | 'point' | 'carry' | 'hold';
export type HexCourseProp =
  | 'magnifier' | 'seedling' | 'crab' | 'snail' | 'microscope' | 'helix' | 'binoculars'
  | 'bubbling-flask' | 'neuron-kite' | 'stethoscope' | 'antenna' | 'growth-cone' | 'eye-chart'
  | 'pencil-stopwatch' | 'pipette';

interface PropArt {
  /** Right edge of the drawing (the plain body is 64 wide). */
  w: number;
  /** Extra room to the left of x = 0 and above y = 0. */
  left?: number;
  top?: number;
  /** The right arm, from the shoulder to the hand on the prop; null for none. */
  armR?: string | null;
  /** The left arm, when the prop needs it (default: hanging). */
  armL?: string;
  /** Drawn with the body (moves with it in a lean or a crouch). */
  onBody?: string;
  /** Drawn in the world, outside any lean or crouch. */
  world?: string;
}

const INK = 'class="hex-ink"';
const THIN = 'class="hex-ink hex-thin"';
const FILLED = 'class="hex-ink hex-body"';
const GOLD = 'class="hex-gold"';
const GLINE = 'class="hex-goldline"';
const SOLID = 'class="hex-fill"';

export const PROP_ART: Record<HexCourseProp, PropArt> = {
  /* Biology Together: a big magnifying glass, waved hello with the other hand. */
  magnifier: {
    w: 80,
    armR: 'M49.3 31 L58 34',
    world: `<path class="hex-ink hex-handle" d="M58.5 34.5 L64 27.5" />
      <circle ${FILLED} cx="69.5" cy="21" r="7.4" />
      <path ${GLINE} d="M65.6 19.6 Q66.6 16.2 70 15.6" />`,
  },
  /* Life Science: a seedling in a pot, carried on Hex's head with both hands. */
  seedling: {
    w: 64, top: 15,
    armL: 'M14.7 22 L24.6 2.4',
    armR: 'M49.3 22 L39.4 2.4',
    onBody: `<path ${FILLED} d="M23.6 -1 H40.4 L38 9.6 H26 Z" />
      <path ${INK} d="M22.8 -1 H41.2" />
      <path ${GLINE} d="M32 -1.5 V-8.5" />
      <path class="hex-gold" d="M32 -7.6 C28.6 -7.6 25.6 -9.6 24.6 -13.2 C28.2 -13.4 31.4 -11.6 32 -7.6 Z" />
      <path class="hex-gold" d="M32 -8.6 C35 -9.4 37.4 -12 37.8 -14.8 C34.6 -14.6 32.2 -12.4 32 -8.6 Z" />`,
  },
  /* High School Biology: a Chesapeake blue crab, held up by one claw-free leg. */
  crab: {
    w: 84, top: 4,
    armR: 'M49.3 27 L58.2 19.6',
    world: `<path ${INK} d="M62.2 18 L58.4 20.4 M63.6 19.8 L60.6 23.4 M77.8 18 L81.6 20.4 M76.4 19.8 L79.4 23.4" />
      <path ${INK} d="M63.4 13.2 L60.2 8.2 M76.6 13.2 L79.8 8.2" />
      <path class="hex-gold" d="M60.2 8.2 C56.4 7.6 56 3 58.6 1.2 L60.6 4.6 L62 1 C64.4 3 63.6 7.4 60.2 8.2 Z" />
      <path class="hex-gold" d="M79.8 8.2 C83.6 7.6 84 3 81.4 1.2 L79.4 4.6 L78 1 C75.6 3 76.4 7.4 79.8 8.2 Z" />
      <path ${FILLED} d="M61 15.4 C61 11.4 79 11.4 79 15.4 C79 19.8 61 19.8 61 15.4 Z" />
      <path ${INK} d="M67.4 11.6 V9 M72.6 11.6 V9" />
      <circle ${SOLID} cx="67.4" cy="8.6" r="1.3" /><circle ${SOLID} cx="72.6" cy="8.6" r="1.3" />`,
  },
  /* Organismal Biology: a snail on a leaf, watched from a crouch. */
  snail: {
    w: 86,
    armR: 'M49.3 33 L56.4 39',
    world: `<path ${INK} d="M53.4 60.8 L49.6 62" />
      <path ${FILLED} d="M53.4 60.8 C58 53.6 74 50.6 86.4 51.8 C80.4 59.8 66 64.6 53.4 60.8 Z" />
      <path ${GLINE} d="M54.6 60.4 C64 58 76 55 85.6 52.4" />
      <path ${FILLED} d="M60.6 56.6 C60 52.6 61.4 50.6 63.4 50.6 C64.6 50.6 65 52 65 53.4 L78.6 55.4 C79.4 56.4 78.6 57.4 77 57.4 Z" />
      <path ${INK} d="M62 51.2 L59.6 46.8 M63.8 50.8 L63.6 46.2" />
      <circle ${FILLED} cx="72" cy="48.6" r="6.6" />
      <path ${GLINE} d="M72 48.6 m0 0 q2.6 0 2.6 -2.4 q0 -3 -3.2 -3 q-4 0 -4 4 q0 4.8 5 4.8 q5.2 0 5.4 -5" />`,
  },
  /* Cell Biology: peering into a microscope. */
  microscope: {
    w: 84,
    armR: 'M49.3 33 L56.6 41.6',
    world: `<path ${FILLED} d="M60 61 L62.4 56.4 H79.6 L82 61 Z" />
      <path ${INK} d="M76 56.4 V50 C76 40 73 34 67.4 31.2" />
      <path ${FILLED} d="M55.2 22.4 L60.6 19.8 L69.4 37 L64 39.6 Z" />
      <path ${INK} d="M53.8 21.4 L60.2 18.4" />
      <path ${INK} d="M65.4 39.4 L67 43.2" />
      <path ${INK} d="M58.6 46.2 H76" />
      <path class="hex-goldline hex-slide" d="M62.6 44.6 H70" />
      <circle ${GOLD} cx="79.4" cy="47.6" r="2.2" />`,
  },
  /* Genetics: a double helix held like a staff, gold rungs. */
  helix: {
    w: 78,
    armR: 'M49.3 31 L61.6 32',
    world: `<path ${INK} d="M66 4 C72 8.6 72 13.4 66 18 S60 27.4 66 32 S72 41.4 66 46 S60 55.4 66 60" />
      <path ${INK} d="M66 4 C60 8.6 60 13.4 66 18 S72 27.4 66 32 S60 41.4 66 46 S72 55.4 66 60" />
      <path ${GLINE} d="M61.8 11 H70.2 M61.8 25 H70.2 M61.8 39 H70.2 M61.8 53 H70.2" />`,
  },
  /* Ecology and Evolution: binoculars in hand, a finch with a big gold beak perched on Hex's head. */
  binoculars: {
    w: 80, top: 9,
    armR: 'M49.3 31 L57.6 34',
    onBody: `<path ${SOLID} d="M24.6 4 C25.2 -1.6 29 -4.6 33.4 -4.4 C36.4 -4.2 38.2 -2.4 38.6 0.2 C38.4 3.6 35.6 6.6 31 7.4 L23.4 9.6 L25.6 6.2 Z" />
      <path class="hex-gold" d="M38.4 -2.2 L44.2 0.4 L38.6 2.6 Z" />
      <path ${INK} d="M30.6 7.6 V10.4 M33.4 7 V10.4" />`,
    world: `<path ${INK} d="M66.6 29.4 H69.4" />
      <circle ${FILLED} cx="62.6" cy="33" r="4.8" />
      <circle ${FILLED} cx="73.4" cy="33" r="4.8" />
      <circle ${GOLD} cx="62.6" cy="33" r="2" /><circle ${GOLD} cx="73.4" cy="33" r="2" />`,
  },
  /* Biochemistry: the flask held high, bubbling. */
  'bubbling-flask': {
    w: 82, top: 12,
    armR: 'M49.3 27 L60.8 20',
    world: `<path class="hex-gold" d="M62.4 19 H75.6 L77.6 22.8 Q78.6 26 75.6 26 H62.4 Q59.4 26 60.4 22.8 Z" />
      <path ${INK} d="M65.5 2 H72.5 M66.5 2 V10 L60.4 22.8 Q59.4 26 62.4 26 H75.6 Q78.6 26 77.6 22.8 L71.5 10 V2" />
      <g class="hex-pulse"><circle ${GOLD} cx="69.4" cy="-2.6" r="1.5" /><circle ${GOLD} cx="72.6" cy="-7.4" r="2.1" /></g>`,
  },
  /* Neuroscience: a neuron flown like a kite, its axon the tail. */
  'neuron-kite': {
    w: 92, top: 10,
    armR: 'M49.3 27 L57.6 18.6',
    world: `<path class="hex-ink hex-string" d="M57.8 18.4 Q63 14 68.4 -1.4" />
      <path ${INK} d="M70.4 -6 L67.2 -10 M67.2 -10 L64.2 -9.6 M67.2 -10 L67.4 -12.6 M74.2 -5.4 L78 -9 M78 -9 L80.8 -8 M78 -9 L77.8 -11.8 M67.2 -0.8 L63.4 -0.2" />
      <circle ${FILLED} cx="71.2" cy="-2.4" r="4" />
      <path ${INK} d="M74.6 0 C79 3 78 9 82.6 12 S86.6 21 90.4 22.6" />
      <path class="hex-goldline hex-myelin" d="M76.4 3 L77.4 6.8 M80.4 10.8 L83.4 13.4 M85.6 17.2 L87.4 20.6" />
      <circle ${GOLD} cx="90.8" cy="23" r="1.7" />`,
  },
  /* Physiology: a stethoscope, earpieces up, gold chest piece swinging. */
  stethoscope: {
    w: 82,
    armR: 'M49.3 31 L61.4 30.4',
    world: `<path ${INK} d="M61.6 12.4 V16.4 Q61.6 25 66.6 26.6 Q71.6 25 71.6 16.4 V12.4" />
      <circle ${SOLID} cx="61.6" cy="11.4" r="1.6" /><circle ${SOLID} cx="71.6" cy="11.4" r="1.6" />
      <path ${INK} d="M66.6 26.6 V31 Q66.6 39 73 39.6 Q77.6 40 77.6 44.4" />
      <circle ${FILLED} cx="77.6" cy="48.4" r="4.2" />
      <circle ${GOLD} cx="77.6" cy="48.4" r="2.2" />`,
  },
  /* Cell Signaling: a receptor on Hex's head, a gold signal docking in it, waves arriving. */
  antenna: {
    w: 64, top: 14,
    armR: 'M49.3 32 L56 39',
    onBody: `<path ${INK} d="M32 10 V2 M32 2 L27.6 -3.4 M32 2 L36.4 -3.4" />
      <circle ${GOLD} cx="32" cy="-3" r="2.6" />
      <g class="hex-pulse"><path ${GLINE} d="M40.6 -9.6 Q44.6 -4 40.6 1.6 M45.6 -13 Q51.4 -4 45.6 5" /></g>`,
  },
  /* Developmental Neuroscience: an axon on a leash, its growth cone reaching for a gold cue. */
  'growth-cone': {
    w: 92,
    armR: 'M49.3 29 L58.4 28',
    world: `<path ${INK} d="M58.6 28 C64 29.4 66 27 68.6 23" />
      <path ${FILLED} d="M68.6 23 C64.8 18 67.4 11.8 73.4 11.6 C79.4 11.4 81.6 17 79 21.2 C76.4 24.6 72 25.4 68.6 23 Z" />
      <path ${INK} d="M68.6 14.4 L65.2 9.8 M72 11.8 L71 5.6 M75.8 11.8 L78 5.8 M78.8 14 L83.6 9.8 M80 18.4 L85.8 17" />
      <circle ${GOLD} cx="88" cy="9.6" r="2.6" />
      <path class="hex-goldline hex-cue" d="M84 13.6 L82.6 15 M86.2 15.4 L85.4 17.2" />`,
  },
  /* Sensory Systems: an eye chart on an easel, Hex pointing at the big E. */
  'eye-chart': {
    w: 84,
    armR: 'M49.3 27 L56 21.4',
    armL: 'M14.7 31 L8.6 35.6 L14.4 39.6',
    world: `<path ${INK} d="M65 33 L62.4 61 M78 33 L80.6 61" />
      <rect ${FILLED} x="61.6" y="4.6" width="19.8" height="28.4" rx="1.6" />
      <path class="hex-ink hex-bold" d="M68.4 8.6 V17.4 M68.4 8.6 H75 M68.4 13 H74 M68.4 17.4 H75" />
      <path class="hex-goldline hex-row1" d="M65.6 22.2 H77.4" />
      <path class="hex-ink hex-row2" d="M66.6 26.4 H76.4" />
      <path class="hex-ink hex-row3" d="M67.6 29.8 H75.4" />
      <path ${THIN} d="M55.8 21.6 L64.8 13.4" />`,
  },
  /* MCAT: a pencil in one hand, a stopwatch in the other. */
  'pencil-stopwatch': {
    w: 78, left: 10,
    armR: 'M49.3 31 L60.6 31',
    armL: 'M14.7 32 L7.8 37',
    world: `<g transform="rotate(14 64 30)">
        <rect class="hex-gold" x="60.6" y="6.6" width="6.8" height="5.4" rx="1.4" />
        <path ${INK} d="M60.6 12 H67.4" />
        <path ${FILLED} d="M60.6 12.6 H67.4 V44 L64 51.4 L60.6 44 Z" />
        <path ${INK} d="M60.6 44 H67.4" />
        <path class="hex-fill" d="M62.8 48.8 L64 51.4 L65.2 48.8 Z" />
      </g>
      <circle ${FILLED} cx="-0.2" cy="43" r="6.8" />
      <path ${INK} d="M-0.2 36.2 V34 M-2.4 33.6 H2" />
      <path ${GLINE} d="M-0.2 43 V38.8 M-0.2 43 L2.8 44.8" />`,
  },
  /* Methods library: a micropipette with a gold drop at its tip. */
  pipette: {
    w: 76,
    armR: 'M49.3 31 L61.4 29.6',
    world: `<path ${INK} d="M63.6 4.4 H68.4 M66 4.4 V9.2" />
      <path ${FILLED} d="M62.6 9.2 H69.4 L69 30 Q69 33.4 67.4 34 H64.6 Q63 33.4 63 30 Z" />
      <path ${INK} d="M62.6 14 Q58.8 14.8 59.6 18.4" />
      <path ${GLINE} d="M64.8 20.6 H67.2" />
      <path ${FILLED} d="M64.6 34 L66 47.4 L67.4 34" />
      <path class="hex-gold hex-drop" d="M66 49.4 Q63.8 53 66 54 Q68.2 53 66 49.4 Z" />`,
  },
};

/* Where the eyes look, and how the body sits, in each pose. */
const EYES: Record<string, [number, number]> = {
  stand: [0, 0], wave: [0, 0], peer: [2.2, 0.4], kneel: [1.6, 1.4], lookup: [0.6, -1.8],
  reach: [2, -0.4], point: [1.8, -0.8], carry: [0, -1.8], hold: [1.2, 0],
};

/**
 * The markup inside the svg for a course look: Hex in `pose` with `prop`.
 * Returns the viewBox and its size in Hex units (72 units tall is the body's full height).
 */
export function courseHexMarkup(pose: string, prop?: HexCourseProp) {
  const art: PropArt = prop ? PROP_ART[prop] : { w: 64 };
  const left = art.left ?? 0;
  const top = art.top ?? 0;
  const lean = pose === 'peer';
  const crouch = pose === 'kneel';
  const [ex, ey] = EYES[pose] ?? [0, 0];

  const legs = lean
    ? `<path ${INK} d="M27 48 L31 60 M37 48 L34 60" /><path ${GLINE} d="M29 61 H34 M32 61.2 H37.5" />`
    : crouch
      ? `<path ${INK} d="M27 53 L22.6 56.6 L25.6 60.6 M37 53 L41.4 56.6 L38.4 60.6" /><path ${GLINE} d="M22.8 61 H27.6 M36.4 61 H41.2" />`
      : `<path ${INK} d="M27 48 L25.5 60 M37 48 L38.5 60" /><path ${GLINE} d="M22.5 61 H27.5 M36.5 61 H41.5" />`;

  const armL = pose === 'wave'
    ? `<path class="hex-ink hex-arm-l" d="M14.7 26 L6 15" />`
    : `<path ${INK} d="${art.armL ?? (pose === 'point' ? 'M14.7 31 L8.6 35.6 L14.4 39.6' : 'M14.7 32 L8 39')}" />`;
  const armR = art.armR === null ? '' : `<path ${INK} d="${art.armR ?? 'M49.3 32 L56 39'}" />`;

  const body = `${armL}${armR}
    <path class="hex-ink hex-body" d="M32 10 L49.3 20 L49.3 40 L32 50 L14.7 40 L14.7 20 Z" />
    <path class="hex-goldline hex-bonds" d="M32 14.8 L45.2 22.4 M45.2 37.6 L32 45.2 M18.8 37.6 L18.8 22.4" />
    <g class="hex-eyes"><g transform="translate(${ex} ${ey})"><circle ${SOLID} cx="26.5" cy="28" r="2.2" /><circle ${SOLID} cx="37.5" cy="28" r="2.2" /></g></g>
    <path class="hex-ink hex-thin" d="M${28 + ex / 2} ${34.5 + ey / 3} Q${32 + ex / 2} ${38.5 + ey / 3} ${36 + ex / 2} ${34.5 + ey / 3}" />
    ${art.onBody ?? ''}`;

  const figure = crouch
    ? `${legs}<g transform="translate(0 5)">${body}</g>`
    : lean
      ? `<g transform="rotate(9 32 61)">${legs}${body}</g>`
      : `${legs}${body}`;

  return {
    viewBox: `${-left} ${-top} ${art.w + left} ${72 + top}`,
    width: art.w + left,
    height: 72 + top,
    inner: `<g class="hex-all">${figure}</g>${art.world ?? ''}`,
  };
}
