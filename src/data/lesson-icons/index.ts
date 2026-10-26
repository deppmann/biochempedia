/* Card icons for the Genetics, Developmental Neuroscience, Cell Biology, Ecology and Evolution, Neuroscience, Organismal Biology, Physiology, Sensory Systems, high school Biology and grade 7 Life Science lessons, drawn in
   the same engraving hand as signaling-icons.ts (56 x 56, navy ink, gold accent). */
import type { IconArt } from '../signaling-icons';
import { ICONS as GENETICS } from './genetics';
import { ICONS as DN1 } from './dn1';
import { ICONS as DN2 } from './dn2';
import { ICONS as DN3 } from './dn3';
import { ICONS as CB1 } from './cellbio1';
import { ICONS as CB2 } from './cellbio2';
import { ICONS as EE1 } from './ecoevo1';
import { ICONS as EE2 } from './ecoevo2';
import { ICONS as NC1 } from './neuro1';
import { ICONS as NC2 } from './neuro2';
import { ICONS as OB1 } from './organismal1';
import { ICONS as OB2 } from './organismal2';
import { ICONS as PH1 } from './physio1';
import { ICONS as PH2 } from './physio2';
import { ICONS as SS1 } from './sensory1';
import { ICONS as SS2 } from './sensory2';
import { ICONS as VB1 } from './vabio1';
import { ICONS as VB2 } from './vabio2';
import { ICONS as LS1 } from './lifesci1';
import { ICONS as LS2 } from './lifesci2';

export const LESSON_ICONS: Record<string, IconArt> = { ...GENETICS, ...DN1, ...DN2, ...DN3, ...CB1, ...CB2, ...EE1, ...EE2, ...NC1, ...NC2, ...OB1, ...OB2, ...PH1, ...PH2, ...SS1, ...SS2, ...VB1, ...VB2, ...LS1, ...LS2 };
