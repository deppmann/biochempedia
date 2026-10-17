/* Card icons for the Genetics and Developmental Neuroscience lessons, drawn in
   the same engraving hand as signaling-icons.ts (56 x 56, navy ink, gold accent). */
import type { IconArt } from '../signaling-icons';
import { ICONS as GENETICS } from './genetics';
import { ICONS as DN1 } from './dn1';
import { ICONS as DN2 } from './dn2';
import { ICONS as DN3 } from './dn3';

export const LESSON_ICONS: Record<string, IconArt> = { ...GENETICS, ...DN1, ...DN2, ...DN3 };
