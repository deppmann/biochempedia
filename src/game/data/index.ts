import type { Pathway } from '../types';
import { glycolysis } from './glycolysis';
import { pyruvateDehydrogenase } from './pyruvate-dehydrogenase';
import { citricAcidCycle } from './citric-acid-cycle';
import { oxidativePhosphorylation } from './oxidative-phosphorylation';
import { pentosePhosphatePathway } from './pentose-phosphate-pathway';
import { glycogenolysis } from './glycogenolysis';
import { gluconeogenesis } from './gluconeogenesis';
import { fattyAcidOxidation } from './fatty-acid-oxidation';
import { ketoneBodies } from './ketone-bodies';
import { fattyAcidSynthesis } from './fatty-acid-synthesis';
import { aminoAcidCatabolism } from './amino-acid-catabolism';
import { ureaCycle } from './urea-cycle';
import { calvinCycle } from './calvin-cycle';

/* The pathway registry. Add a pathway module here and it appears in the arcade —
   cabinet, all four modes, scoring, and storage come for free from the shared
   data model in ../types.ts. Order here is the order of the cabinets, arranged
   to follow the flow of metabolism: the glucose core (glycolysis → bridge →
   cycle → ETC), the branches (PPP, glycogen, gluconeogenesis), fat catabolism
   and its ketone spillover, fat synthesis, then nitrogen (amino-acid catabolism
   → urea disposal), and finally photosynthesis's Calvin cycle. */
export const PATHWAYS: Pathway[] = [
  glycolysis,
  pyruvateDehydrogenase,
  citricAcidCycle,
  oxidativePhosphorylation,
  pentosePhosphatePathway,
  glycogenolysis,
  gluconeogenesis,
  fattyAcidOxidation,
  ketoneBodies,
  fattyAcidSynthesis,
  aminoAcidCatabolism,
  ureaCycle,
  calvinCycle,
];

export function getPathway(id: string): Pathway | undefined {
  return PATHWAYS.find((p) => p.id === id);
}
