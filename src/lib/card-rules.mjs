/* The card rules every flashcard on the site must pass, with no dependencies, so the same rules run in
   three places: the deck validator (scripts/flashcards/lib.mjs, CI), the Worker that drafts personal
   cards from a learner's highlights (worker/helper.js), and the browser that keeps them.

   What is NOT here: whether the card's quote is in its lesson. The deck validator checks that against
   the lesson source; the Worker checks it against the lesson's Markdown copy. */

export const LEVELS = { 1: 'Recall', 2: 'Explain', 3: 'Apply', 4: 'Integrate' };
export const TYPES = ['cloze', 'qa', 'predict', 'experiment', 'calc'];
export const GOALS = ['lesson', 'course', 'mcat'];

/** Normalise for matching: what plain() does to whitespace and quotes, on any string. */
export const norm = (t) => t.replace(/[“”]/g, '"').replace(/[‘’]/g, "'").replace(/\*\*|`/g, '').replace(/\s+/g, ' ').trim();

/** Shape rules for one card (everything but "is the quote in the lesson"). Returns { errors, warnings }. */
export function checkCardShape(c) {
  const errors = [];
  const warnings = [];
  const where = `card ${c?.id ?? '?'}`;
  if (!c || typeof c !== 'object') return { errors: [`${where}: not a card`], warnings };
  if (!TYPES.includes(c.type)) errors.push(`${where}: type "${c.type}" not one of ${TYPES.join(', ')}`);
  if (![1, 2, 3, 4].includes(c.level)) errors.push(`${where}: level must be 1–4`);
  if (!Array.isArray(c.goals) || !c.goals.length || c.goals.some((g) => !GOALS.includes(g))) errors.push(`${where}: goals must be from ${GOALS.join(', ')}`);
  if (!c.front || (c.type !== 'cloze' && !c.back)) errors.push(`${where}: front and back are required`);
  if (c.type === 'cloze' && !/\{\{c\d::[^}]+\}\}/.test(c.front ?? '')) errors.push(`${where}: a cloze front needs {{c1::…}}`);
  if (c.type !== 'cloze' && /\{\{c\d::/.test(c.front ?? '')) errors.push(`${where}: cloze markup on a ${c.type} card`);
  if ((c.front ?? '').length > 400) warnings.push(`${where}: front is ${c.front.length} characters (aim for under 300)`);
  if ((c.back ?? '').length > 600) warnings.push(`${where}: back is ${c.back.length} characters (aim for under 400)`);
  if (!c.quote) errors.push(`${where}: no source quote`);
  else if (/^\s*\||\|.*\|/.test(c.quote)) errors.push(`${where}: quote spans table markup (|); quote one cell or a sentence instead`);
  return { errors, warnings };
}
