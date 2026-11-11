/**
 * rewritten — "Rewritten on Nov 10, 2026: new text, figures and flashcards." (2026-11-11)
 *
 * A returning student needs to know the text, figures or flashcards changed under their old
 * highlights. The lesson page shows this line under the title, built at deploy time from
 * src/data/recently-rewritten.json (written by scripts/rewritten-shelf.mjs after each level-up
 * merge; the homepage "Recently rewritten" strip reads the same file). An entry's optional `new`
 * list says what changed; with none, the line says "new text".
 */
import list from '../data/recently-rewritten.json';

export type NewPart = 'text' | 'figures' | 'flashcards' | 'film';
interface Entry { slug: string; date: string; new?: NewPart[] }
const ORDER: NewPart[] = ['text', 'figures', 'flashcards', 'film'];
const WORD: Record<NewPart, string> = { text: 'text', figures: 'figures', flashcards: 'flashcards', film: 'film' };
const MONTHS = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'];

/** "new text, figures and flashcards" */
export function whatsNew(parts: NewPart[] | undefined): string {
  const p = ORDER.filter((k) => (parts?.length ? parts : ['text']).includes(k)).map((k) => WORD[k]);
  const words = p.length > 1 ? `${p.slice(0, -1).join(', ')} and ${p[p.length - 1]}` : p[0];
  return `new ${words}`;
}

export function rewrittenFor(slug: string): { date: string; label: string; note: string } | undefined {
  const e = (list as Entry[]).find((r) => r.slug === slug);
  if (!e) return undefined;
  const [y, m, d] = e.date.split('-').map(Number);
  return { date: e.date, label: `${MONTHS[m - 1]} ${d}, ${y}`, note: whatsNew(e.new) };
}
