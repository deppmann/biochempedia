/**
 * Which Metabolism Arcade games belong to which lesson. One file drives the
 * lesson's Finish line, its "Play it" rail group and phone chip, and the
 * arcade's direct links (/play?game=…&pathway=…|puzzle=…&from=<lesson slug>).
 *
 * `game` ids match GAMES in src/game/engine/hub.ts. `pathway` ids match
 * src/game/data/*.ts; `puzzle` ids match DEMANDS in wireCellLogic.ts.
 * The first entry for a lesson is its main game (the Finish line card); the
 * rest are listed under it as "Also in the arcade". Lessons not listed here
 * get the Finish line without a Play card.
 */
export type GameId = 'ledger' | 'autopsy' | 'wire' | 'foundry' | 'mixing' | 'gauntlet';

export interface LessonGame {
  game: GameId;
  /** For pathway games (Ledger Rush, Autopsy, Gauntlet). */
  pathway?: string;
  /** For Wire the Cell: open this puzzle. */
  puzzle?: string;
  /** Card title, e.g. "Ledger Rush: Glycolysis". */
  title: string;
  /** One line on what you do. */
  blurb: string;
  minutes: number;
}

export const LESSON_GAMES: Record<string, LessonGame[]> = {
  'metabolism-basic-concepts': [
    { game: 'ledger', pathway: 'glycolysis', title: 'Ledger Rush: Glycolysis', blurb: 'Keep the ATP and NADH books for one glucose. Bank the real yields, toss the myths.', minutes: 3 },
    { game: 'foundry', title: 'Flux Foundry', blurb: 'Route fuels through your engine as the body swings between fed, fasted and sprinting.', minutes: 6 },
  ],
  glycolysis: [
    { game: 'ledger', pathway: 'glycolysis', title: 'Ledger Rush: Glycolysis', blurb: 'Bank the real ATP and NADH, toss the myths, catch the doubling after the split.', minutes: 3 },
    { game: 'autopsy', pathway: 'glycolysis', title: 'Metabolic Autopsy: Glycolysis', blurb: 'One enzyme is broken. Read which metabolites pile up and find it in the fewest tests.', minutes: 4 },
  ],
  gluconeogenesis: [
    { game: 'mixing', title: 'Mixing Board', blurb: 'Set insulin, glucagon, F-2,6-BP and the energy signals so the liver runs the right pathway, and never both at once.', minutes: 4 },
    { game: 'wire', puzzle: 'cori-liver', title: 'Wire the Cell: Cori-cycle liver', blurb: 'Rebuild glucose from lactate and find something to pay the 6 ATP bill.', minutes: 3 },
  ],
  'pyruvate-dehydrogenase': [
    { game: 'autopsy', pathway: 'pyruvate-dehydrogenase', title: 'Metabolic Autopsy: PDH', blurb: 'Diagnose a broken step at the bridge from the metabolite pile-up.', minutes: 4 },
    { game: 'ledger', pathway: 'pyruvate-dehydrogenase', title: 'Ledger Rush: PDH', blurb: 'What does one pyruvate really pay out at the bridge?', minutes: 2 },
  ],
  'citric-acid-cycle': [
    { game: 'ledger', pathway: 'citric-acid-cycle', title: 'Ledger Rush: Citric acid cycle', blurb: 'Count every NADH, FADH₂, GTP and CO₂ in one turn, and toss the myths.', minutes: 3 },
    { game: 'autopsy', pathway: 'citric-acid-cycle', title: 'Metabolic Autopsy: Citric acid cycle', blurb: 'Find the broken enzyme in the cycle from what piles up.', minutes: 4 },
  ],
  'oxidative-phosphorylation': [
    { game: 'ledger', pathway: 'oxidative-phosphorylation', title: 'Ledger Rush: Electron transport', blurb: 'Complex by complex: which carriers are spent, how many protons are pumped, and what ATP synthase pays out.', minutes: 3 },
    { game: 'wire', puzzle: 'glucose-aerobic', title: 'Wire the Cell: Burn glucose', blurb: 'Wire the full aerobic line and watch OxPhos cash in the carriers.', minutes: 2 },
  ],
  'proton-motive-force': [
    { game: 'ledger', pathway: 'oxidative-phosphorylation', title: 'Ledger Rush: Electron transport', blurb: 'Track the protons: 10 per NADH, 6 per FADH₂, about 4 per ATP.', minutes: 3 },
  ],
  carbohydrates: [
    { game: 'autopsy', pathway: 'glycogenolysis', title: 'Metabolic Autopsy: Glycogen', blurb: 'A glycogen storage disease case. Find the missing enzyme.', minutes: 4 },
  ],
  'pentose-phosphate-pathway': [
    { game: 'wire', puzzle: 'rbc', title: 'Wire the Cell: Red blood cell', blurb: 'No mitochondria. Make ATP and the NADPH that protects the cell from oxidants.', minutes: 2 },
    { game: 'wire', puzzle: 'dividing-cell', title: 'Wire the Cell: A cell about to divide', blurb: 'Ribose for DNA, NADPH for lipids, and ATP for everything else.', minutes: 3 },
  ],
  'fatty-acid-degradation': [
    { game: 'wire', puzzle: 'palmitate-aerobic', title: 'Wire the Cell: Torch a fat', blurb: 'Wire palmitate all the way to its 106 ATP.', minutes: 2 },
    { game: 'wire', puzzle: 'fasting-ketones', title: 'Wire the Cell: Fasting liver makes ketones', blurb: 'Why the fasting liver sends acetyl-CoA to ketone bodies instead of the cycle.', minutes: 3 },
  ],
  'fatty-acid-synthesis': [
    { game: 'wire', puzzle: 'store-fat', title: 'Wire the Cell: Store the surplus', blurb: 'Turn extra glucose into fat, and find where the NADPH comes from.', minutes: 3 },
    { game: 'ledger', pathway: 'fatty-acid-synthesis', title: 'Ledger Rush: Fatty acid synthesis', blurb: 'The ATP and NADPH bill for one palmitate.', minutes: 3 },
  ],
  'protein-turnover-amino-acid-catabolism': [
    { game: 'autopsy', pathway: 'urea-cycle', title: 'Metabolic Autopsy: Urea cycle', blurb: 'A baby with high ammonia. Find the broken urea-cycle enzyme.', minutes: 4 },
    { game: 'ledger', pathway: 'amino-acid-catabolism', title: 'Ledger Rush: Amino acids', blurb: 'Where the carbons and the nitrogen go.', minutes: 3 },
  ],
  'calvin-cycle': [
    { game: 'ledger', pathway: 'calvin-cycle', title: 'Ledger Rush: Calvin cycle', blurb: 'The ATP and NADPH it takes to fix CO₂.', minutes: 3 },
  ],
  'integration-of-metabolism': [
    { game: 'foundry', title: 'Flux Foundry', blurb: 'Run the whole-body engine through rest, a fast, a feast and a sprint.', minutes: 6 },
    { game: 'mixing', title: 'Mixing Board', blurb: 'You are the liver’s regulators. Read the body state, set the board.', minutes: 4 },
    { game: 'gauntlet', title: 'MCAT Gauntlet', blurb: '15 timed questions across every pathway.', minutes: 6 },
  ],
};

/** Arcade URL for a lesson game; `from` is the lesson slug it was opened from. */
export function gameHref(g: LessonGame, from?: string): string {
  const q = new URLSearchParams({ game: g.game });
  if (g.pathway) q.set('pathway', g.pathway);
  if (g.puzzle) q.set('puzzle', g.puzzle);
  if (from) q.set('from', from);
  return `/play?${q.toString()}`;
}
