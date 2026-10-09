/* =============================================================================
   The metabolic NETWORK map — the cross-pathway layer that Flux Foundry
   (economy roguelite) and Wire the Cell (construction puzzle) both play on.
   -----------------------------------------------------------------------------
   This is deliberately SEPARATE from the per-pathway Step.tokens model:
     • Step.tokens are per-single-molecule INTEGERS (great for the step ledger).
     • Network yields are whole-pathway ATP-EQUIVALENTS as FLOATS, so oxidative
       phosphorylation's ~2.5 ATP/NADH and ~1.5 ATP/FADH₂ ARE representable here.
   Author + MCAT-verify this ONCE; both network games consume it. (Design-critic
   note: this manifest is the single largest content risk in the redesign.)
   ============================================================================ */

export type FuelState = 'fed' | 'fasted' | 'sprint' | 'rest';

export interface Metabolite {
  id: string;
  name: string;
  /** carbon count, for display ("3C"). */
  carbons?: number;
}

/** A pathway/process as a network node with typed input/output metabolites. */
export interface MetNode {
  id: string;
  name: string;
  emoji: string;
  location: string;
  /** Metabolite ids this node CONSUMES to run one pass. */
  inputs: string[];
  /** Metabolite ids this node PRODUCES. */
  outputs: string[];
  /** Net ATP-equivalents produced per pass (FLOAT; negative = net cost). This is
   *  the "yield" the games tally. OxPhos converts carriers → ATP here. */
  atpEquiv: number;
  /** Reduced-carrier output per pass (feed these into OxPhos to cash them). */
  nadh?: number;
  fadh2?: number;
  nadph?: number;
  gtp?: number;
  co2?: number;
  /** Node stalls without O₂ (β-oxidation, TCA→OxPhos chain). */
  requiresO2?: boolean;
  /** A one-way door — the reverse edge is physically undrawable (irreversibility). */
  irreversible?: boolean;
  /** Relative activity multiplier by hormonal state (Flux Foundry re-pricing).
   *  1 = normal, 0 = off, >1 = up-regulated. Missing state = 1. */
  states?: Partial<Record<FuelState, number>>;
  /** One-line teaching note surfaced on hover / in the debrief. */
  note?: string;
}

/** A starting fuel the player can draw (Flux Foundry) or must route (Wire the Cell). */
export interface Fuel {
  id: string;
  name: string;
  emoji: string;
  /** Node id the fuel first enters. */
  entersAt: string;
  /** Rough fully-oxidized ATP yield, for the post-run receipt. */
  atpWhenFullyOxidized: number;
  note: string;
}

export interface NetMap {
  metabolites: Metabolite[];
  nodes: MetNode[];
  fuels: Fuel[];
}
