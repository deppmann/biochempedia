/* =============================================================================
   Card icons for whole courses on the home page
   -----------------------------------------------------------------------------
   A course card normally borrows the icon of its first lesson. A course listed
   here gets its own instead, in the same engraving hand (56 x 56 box, navy ink,
   gold accents; see signaling-icons.ts). Keyed `course:<course slug>`.
   ============================================================================ */
import type { IconArt } from './signaling-icons';
import { COURSE as CELLBIO_COURSE } from './lesson-icons/cellbio1';
import { COURSE as ECOEVO_COURSE } from './lesson-icons/ecoevo1';

const GF = 'style="fill:var(--ddp-color-secondary)"';
const GS = 'style="stroke:var(--ddp-color-secondary)" fill="none" stroke-width="1.75" stroke-linecap="round"';

export const COURSE_ICONS: Record<string, IconArt> = {
  ...CELLBIO_COURSE,
  ...ECOEVO_COURSE,
  'course:genetics': {
    label: "A pea pod cut open on three plain peas and one gold one, Mendel's 3 to 1",
    ink: `<g transform="rotate(-38 28 28)">
      <path d="M2 26 Q28 2 54 26 Q28 50 2 26 Z" />
      <path d="M54 26 q3.5 -1.5 3.5 -5.5 q0 -2.6 -2.6 -2.8" />
      <circle cx="16" cy="26" r="4.7" />
      <circle cx="25" cy="26" r="4.7" />
      <circle cx="43" cy="26" r="4.7" />
    </g>`,
    gold: `<g transform="rotate(-38 28 28)"><circle cx="34" cy="26" r="4.7" ${GF} /></g>`,
  },
  'course:developmental-neuroscience': {
    label: 'A young neuron whose growth cone reaches toward a gold guidance cue',
    ink: `<circle cx="12" cy="43" r="6.2" />
      <path d="M7.4 38.8 L3.5 35 M6.3 45.6 L2.5 48 M11 49.2 L10 54 M16.8 47.2 L20 51.5" />
      <path d="M17.6 40 C25 37 25 29 31.5 24.5" />
      <path d="M31.5 24.5 C31 21 33 18.5 36 18 C38.5 19 39 22 37.5 25 C35.5 26.5 33 26.5 31.5 24.5 Z" />
      <path d="M34.6 18.4 L36 13.4 M37.2 19.2 L40.8 15.2 M38.6 22 L43.4 20.6 M37.5 25 L42 26.6" />`,
    gold: `<circle cx="50" cy="6" r="3.2" ${GF} />
      <path d="M44.1 7 A6 6 0 0 0 49 11.9" ${GS} />
      <path d="M40.6 7.6 A9.5 9.5 0 0 0 48.4 15.4" ${GS} opacity="0.55" />`,
  },
};
