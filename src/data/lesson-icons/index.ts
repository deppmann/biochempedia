/* Card icons for the Genetics, Developmental Neuroscience and Cell Biology lessons, drawn in
   the same engraving hand as signaling-icons.ts (56 x 56, navy ink, gold accent). */
import type { IconArt } from '../signaling-icons';
import { ICONS as GENETICS } from './genetics';
import { ICONS as DN1 } from './dn1';
import { ICONS as DN2 } from './dn2';
import { ICONS as DN3 } from './dn3';
import { ICONS as CB1 } from './cellbio1';
import { ICONS as CB2 } from './cellbio2';

export const LESSON_ICONS: Record<string, IconArt> = { ...GENETICS, ...DN1, ...DN2, ...DN3, ...CB1, ...CB2 };
