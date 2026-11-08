/* One small JSON file per lesson deck, for the teacher's class brief (/teach/class/):
   it names the cards a class marked "Again" most, so it needs each card's front.
   Cloze markup is stripped to plain text. Static, written at build; no model runs. */
import type { APIRoute } from 'astro';
import { clozeParts, type Deck } from '../../lib/flashcards';

const DECKS = import.meta.glob<{ default: Deck }>('../../data/flashcards/*.json', { eager: true });

function plainFront(front: string): string {
  const z = clozeParts(front);
  const text = z ? `${z.before}${z.answer}${z.after}` : front;
  return text.replace(/\{\{c\d+::([\s\S]+?)(?:::[\s\S]+?)?\}\}/g, '$1').replace(/\s+/g, ' ').trim();
}

export async function getStaticPaths() {
  return Object.values(DECKS).map((m) => m.default).filter((d) => d.slug && d.cards?.length)
    .map((deck) => ({ params: { slug: deck.slug }, props: { deck } }));
}

export const GET: APIRoute = async ({ props }) => {
  const { deck } = props as { deck: Deck };
  const body = { slug: deck.slug, title: deck.title, cards: deck.cards.map((c) => ({ id: c.id, front: plainFront(c.front) })) };
  return new Response(JSON.stringify(body), { headers: { 'Content-Type': 'application/json' } });
};
