/* Addy the ATP — the arcade mascot's running commentary. Silly on top, correct
   underneath. Pulled at random so replays stay fresh. */
import { shuffle } from './dom';

type Bucket =
  | 'correct'
  | 'wrong'
  | 'streak'
  | 'win'
  | 'lose'
  | 'placeStart'
  | 'idle';

const LINES: Record<Bucket, string[]> = {
  correct: [
    'Chef’s kiss. That’s textbook.',
    'Clean phosphoryl transfer. Nice.',
    'The reviewers would approve.',
    'Enzyme employee of the month.',
    'You and this pathway are in equilibrium. The good kind.',
    'Substrate-level swagger.',
    'That’s the good ΔG.',
  ],
  wrong: [
    'Oof. That enzyme is on strike.',
    'Nope — that reaction ran backwards.',
    'The cell felt that one.',
    'Denatured. Try again.',
    'Not quite — check the cofactors.',
    'That’s a futile cycle, my friend.',
  ],
  streak: [
    '🔥 On a roll! Flux is FLOWING.',
    '🔥 Combo! The mitochondria are cheering.',
    '🔥 Unstoppable. Save some ATP for the rest of us.',
    '🔥 Now THAT is metabolic control.',
  ],
  win: [
    'GOLD. You basically ARE the pathway now.',
    'Study section: fund it. 🏆',
    'The MCAT never saw you coming.',
    'Homeostasis achieved. Beautifully.',
  ],
  lose: [
    'The cell survived… barely. Run it back.',
    'Apoptosis avoided. Let’s try again.',
    'Even Krebs failed a few times. Reload.',
    'Shake it off — NAD⁺ regenerates, and so do you.',
  ],
  placeStart: [
    'Here we go — feed me metabolites.',
    'Load the substrate. Let’s make some ATP.',
    'Assembly line’s open. What’s first?',
  ],
  idle: [
    'Pick a pathway and let’s play.',
    'Fun fact: you have ~500g of ATP in you right now, recycled thousands of times a day.',
    'Ready when you are.',
  ],
};

const pools: Partial<Record<Bucket, string[]>> = {};

export function quip(bucket: Bucket): string {
  let pool = pools[bucket];
  if (!pool || pool.length === 0) pool = pools[bucket] = shuffle(LINES[bucket]);
  return pool.pop() as string;
}
