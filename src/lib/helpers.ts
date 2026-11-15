/* Study helpers in the browser: the calls to /api/help/* (worker/helper.js) and the learner's
   personal flashcards.

   Personal cards are kept like the notebook: one localStorage entry on this device, every read and
   write wrapped, so a blocked store means "nothing kept". They are NOT synced to the account (the
   sync carries the notebook and progress only). The flashcard panel (FlashcardDeck.astro) adds them
   to the lesson's own deck, so the same schedule (src/lib/flashcards.ts) reviews both.

     { v: 1, decks: { <lesson slug>: Card[] } }      card ids start with "my-" */
import type { Card } from './flashcards';
import { signedInHint } from './learner';
import { enrolled } from './classroom';

export const MYCARDS_KEY = 'biochempedia:mycards:v1';
export const MYCARDS_EVENT = 'bp-mycards';
const MAX_PER_LESSON = 200;

export type MyCard = Card & { mine: true; added: number };

interface Store { v: 1; decks: Record<string, MyCard[]> }

function load(): Store {
  try {
    const p = JSON.parse(window.localStorage.getItem(MYCARDS_KEY) || 'null');
    if (p && p.v === 1 && p.decks && typeof p.decks === 'object') return p as Store;
  } catch { /* blocked or corrupt */ }
  return { v: 1, decks: {} };
}

function save(s: Store): boolean {
  let ok = true;
  try { window.localStorage.setItem(MYCARDS_KEY, JSON.stringify(s)); } catch { ok = false; }
  try { window.dispatchEvent(new CustomEvent(MYCARDS_EVENT)); } catch { /* no window */ }
  return ok;
}

const validCard = (c: unknown): c is MyCard => {
  const x = c as MyCard;
  return !!x && typeof x.id === 'string' && x.id.startsWith('my-') && typeof x.front === 'string' && typeof x.quote === 'string'
    && (x.type === 'qa' || x.type === 'cloze') && [1, 2, 3, 4].includes(x.level) && Array.isArray(x.goals);
};

export function myCards(slug: string): MyCard[] {
  const list = load().decks[slug];
  return Array.isArray(list) ? list.filter(validCard) : [];
}

/** Add cards (skipping ids already kept). Returns how many were added, or -1 when storage is blocked. */
export function keepCards(slug: string, cards: Card[]): number {
  const s = load();
  const have = new Set((s.decks[slug] || []).map((c) => c.id));
  const add = cards.filter((c) => !have.has(c.id)).map((c) => ({ ...c, mine: true as const, added: Date.now() }));
  s.decks[slug] = [...(s.decks[slug] || []), ...add].slice(-MAX_PER_LESSON);
  return save(s) ? add.length : -1;
}

export function removeCard(slug: string, id: string) {
  const s = load();
  s.decks[slug] = (s.decks[slug] || []).filter((c) => c.id !== id);
  if (!s.decks[slug].length) delete s.decks[slug];
  save(s);
}

// ---- the API ----------------------------------------------------------------------
export interface HelpStatus { on: boolean; signedIn: boolean; features?: string[]; left?: { explain: number; feedback: number; cards: number } }

/** Whether to offer the helpers on this page at all: signed in, not in a teacher's class on this device, and the Worker says on. */
export async function helpStatus(slug: string): Promise<HelpStatus | null> {
  if (!signedInHint() || enrolled()) return null;
  try {
    const r = await fetch(`/api/help?slug=${encodeURIComponent(slug)}`, { credentials: 'same-origin' });
    if (!r.ok) return null;
    const d = await r.json();
    return d?.on && d.signedIn ? d : null;
  } catch { return null; }
}

export type HelpReply = { status: number; data: Record<string, any> };

export async function askHelp(feature: 'explain' | 'feedback' | 'cards', body: Record<string, unknown>): Promise<HelpReply> {
  try {
    const r = await fetch(`/api/help/${feature}`, {
      method: 'POST',
      credentials: 'same-origin',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(body),
    });
    const data = await r.json().catch(() => ({}));
    return { status: r.status, data };
  } catch {
    return { status: 0, data: { error: 'No connection. Try again when you are online.' } };
  }
}
