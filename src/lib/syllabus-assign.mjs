/* Adding matched lessons to a class's assignments (the teacher's syllabus matcher, /teach/match/).

   The Assign tab saves a class's whole list at once (PUT /api/classes/:id/assignments), so adding
   means: read the list as it is, put the new lessons after it, send the whole list back. Nothing
   already assigned is touched: its due date, its flashcards setting and its place stay as they were.
   New lessons go in with no due date, in the syllabus's order; the teacher sets dates on the
   class's Assign tab. Pure, so scripts/test-syllabus.mjs can check it. */

/** The server takes at most this many rows (worker/api.js). */
export const MAX_ASSIGNMENTS = 400;

/**
 * @param {{ slug: string, due: string | null, flashcards?: boolean }[]} existing
 * @param {string[]} slugs lessons to add, in order
 * @returns {{ list: { slug: string, due: string | null, flashcards: boolean }[], added: string[], already: string[], dropped: string[] }}
 */
export function mergeAssignments(existing, slugs) {
  const list = (existing ?? []).map((a) => ({ slug: a.slug, due: a.due ?? null, flashcards: a.flashcards === true }));
  const have = new Set(list.map((a) => a.slug));
  const added = [], already = [], dropped = [];
  for (const slug of slugs) {
    if (have.has(slug)) { if (!already.includes(slug) && !added.includes(slug)) already.push(slug); continue; }
    if (list.length >= MAX_ASSIGNMENTS) { dropped.push(slug); continue; }
    have.add(slug);
    list.push({ slug, due: null, flashcards: false });
    added.push(slug);
  }
  return { list, added, already, dropped };
}
