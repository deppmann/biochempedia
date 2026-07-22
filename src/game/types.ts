/* =============================================================================
   Metabolism Arcade — shared data model
   -----------------------------------------------------------------------------
   One typed model feeds all four game modes so adding a pathway is "fill in the
   blanks," not "write new code":

     • Build the Pathway   ← steps[]          (order the reactions; watch the ledger)
     • Regulate It         ← scenarios[]      (fed / fasted / sprint / rest / disease)
     • Diagnose It         ← diseases[]       (enzyme-deficiency case files)
     • MCAT Blitz          ← quiz[] (+ auto-generated items from the above)

   ACCURACY IS THE PRODUCT. Every field here is student-facing biochemistry and
   is held to the same bar as the vetted lessons (see CONTRIBUTING.md). Numbers,
   enzymes, cofactors, and disease mechanisms are cross-checked against the
   corresponding lesson in src/content/lessons/ wherever one exists.
   ============================================================================ */

/** Net token change AT a single step, counted for ONE molecule passing through.
 *  Positive = produced, negative = consumed. The ledger applies pathway.doubleAfter
 *  to steps past the split, so author these per-single-molecule and let the engine
 *  double the back half (e.g. glycolysis after aldolase). */
export interface Tokens {
  atp?: number;
  nadh?: number;
  fadh2?: number;
  nadph?: number;
  gtp?: number;
  co2?: number;
}

/** One reaction in a pathway. `product` of step n is the `substrate` of step n+1. */
export interface Step {
  n: number;
  /** Full display name of the metabolite this step PRODUCES. */
  product: string;
  /** Short chip label for the assembly tiles (e.g. "G6P", "F1,6BP"). */
  short: string;
  /** The enzyme catalyzing this step. */
  enzyme: string;
  /** Net cofactor change at this step (per single molecule). */
  tokens?: Tokens;
  /** A far-from-equilibrium, one-way door — where regulation can actually work. */
  irreversible?: boolean;
  /** The committed step (product is dedicated to this pathway). */
  committed?: boolean;
  /** One-liner shown when the tile is placed correctly — a real, exam-useful fact. */
  fact: string;
  /** Emoji "face" for this metabolite — the silly layer. */
  emoji?: string;
  /** LEDGER RUSH: a wrong token a common misconception would grab AT this step
   *  (e.g. an "ATP" at GAPDH). Rejecting it un-learns a specific error. */
  misconception?: { grab: string; why: string };
}

/** A named control point, listed on the Regulate console. */
export interface Regulator {
  name: string;
  /** Plain-language job: what turns it up, what turns it down. */
  role: string;
}

/** A single control decision inside a scenario (multiple choice). */
export interface Decision {
  q: string;
  choices: string[];
  answer: number;
  why: string;
}

/** A physiological scenario for Regulate mode — the "basics + regulation + exercise
 *  + rest + disease" spine the whole game is built around. */
export interface Scenario {
  id: string;
  emoji: string;
  title: string;
  /** The vignette the player reads. */
  scene: string;
  /** Hormonal context line (e.g. "Insulin ↑ · glucagon ↓"). */
  hormones?: string;
  /** Is THIS pathway ramped up, down, or essentially off in this state? */
  flux: 'up' | 'down' | 'off';
  /** The control decisions the player makes. */
  decisions: Decision[];
  /** The payoff explanation shown after the player commits. */
  teach: string;
}

/** An enzyme-deficiency case file for Diagnose mode. */
export interface Disease {
  id: string;
  /** Clinical name (e.g. "Von Gierke disease · Type Ia"). */
  name: string;
  emoji?: string;
  /** Patient vignette + labs, MCAT-style. */
  vignette: string;
  /** Candidate enzymes/steps to choose from — exactly one is the deficiency. */
  suspects: string[];
  answer: number;
  /** What piles up upstream of the block. */
  accumulates?: string;
  /** What the cell can no longer make. */
  missing?: string;
  /** The mechanism: why the symptoms follow from the block. */
  teach: string;
  /** A high-yield one-liner for the flashcard in your head. */
  pearl?: string;
  /** METABOLIC AUTOPSY: 0-based index of the step[] whose enzyme is deficient.
   *  The engine derives "upstream reads HIGH / downstream reads LOW" from this.
   *  Omit for cases with no single clean block point (e.g. a poison/uncoupler). */
  blockStep?: number;
  /** METABOLIC AUTOPSY: named-compound assays beyond position (2,3-BPG, ammonia,
   *  orotic acid…) that let the player confirm the block mechanistically. */
  traces?: Array<{ name: string; result: 'high' | 'low' | 'normal'; tellsYou: string }>;
}

/** MIXING BOARD: one allosteric/hormonal effector on a pathway's regulated step.
 *  Polarity only — deliberately NO invented kinetics (per the design critic). */
export interface Effector {
  /** e.g. "ATP", "AMP", "F-2,6-BP", "citrate", "insulin", "glucagon". */
  name: string;
  /** 0-based index of the step[] (enzyme) it acts on. */
  actsOn: number;
  /** +1 activates, −1 inhibits. */
  polarity: 1 | -1;
  kind: 'allosteric' | 'hormonal';
}

export type QuizTag = 'basics' | 'energetics' | 'regulation' | 'disease' | 'integration';

/** An original MCAT-style item. NEVER a real AAMC question (site policy). */
export interface QuizItem {
  stem: string;
  choices: string[];
  answer: number;
  rationale: string;
  tag?: QuizTag;
}

/** A whole playable pathway. */
export interface Pathway {
  id: string;
  name: string;
  emoji: string;
  /** A silly, true hook for the cabinet ("Spend money to make money"). */
  tagline: string;
  /** One-sentence orientation shown on the mode-select screen. */
  blurb: string;
  /** MCAT weight, 1–3 stars. */
  difficulty: 1 | 2 | 3;
  /** Where in the cell it runs. */
  location: string;
  /** Headline energetics ("Net +2 ATP, +2 NADH per glucose"). */
  netYield: string;
  /** The starting metabolite (the fixed first tile in Build mode). */
  start: string;
  /** Short label + emoji for the starting metabolite tile. */
  startShort: string;
  startEmoji?: string;
  /** After this step index, downstream yields double (e.g. glycolysis aldolase = 4).
   *  0 = never doubles. */
  doubleAfter: number;
  steps: Step[];
  regulators: Regulator[];
  scenarios: Scenario[];
  diseases: Disease[];
  quiz: QuizItem[];
  /** MIXING BOARD: allosteric + hormonal effectors on this pathway's regulated
   *  steps (polarity only). Present for pathways with real regulation to control. */
  effectors?: Effector[];
  /** Optional link back to the matching textbook lesson. */
  lessonSlug?: string;
  /** A closing "whoa" fact for the victory screen. */
  funFact?: string;
}
