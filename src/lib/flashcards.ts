/* Lesson flashcards: card types, the spaced-repetition schedule, and Anki export.

   Decks are static data, src/data/flashcards/<slug>.json, written ahead of time
   by the pipeline in scripts/flashcards/ (no model runs on the site). Study state
   is browser-only, like src/lib/progress.ts: one localStorage entry on this
   device, every read and write wrapped so a blocked store just means "nothing
   remembered this visit".

   Schedule: a small SM-2 variant with four answers (Again, Hard, Good, Easy).
   A new card answered Good comes back in 1 day, then 3, then about interval ×
   ease. Again (1 min) and Hard (6 min) on a card still being learned send it
   back into today's session; Again also lowers its ease. Easy jumps
   ahead and raises it. That is enough for one lesson's deck; anyone who wants a
   heavier scheduler can export to Anki. */

export type CardType = 'cloze' | 'qa' | 'predict' | 'experiment' | 'calc';
export type Goal = 'lesson' | 'course' | 'mcat';

export interface Card {
  id: string;
  type: CardType;
  /** 1 Recall · 2 Explain · 3 Apply · 4 Integrate */
  level: 1 | 2 | 3 | 4;
  goals: Goal[];
  front: string;
  back: string;
  why?: string;
  /** Verbatim span of the lesson text this card comes from; "Show in lesson" highlights it. */
  quote: string;
  /** The lesson heading the quote sits under. */
  section?: string;
}

export interface Deck {
  slug: string;
  title: string;
  cards: Card[];
}

export const LEVELS: Record<number, { name: string; hint: string }> = {
  1: { name: 'Recall', hint: 'terms, values, single steps' },
  2: { name: 'Explain', hint: 'why and how, in a sentence' },
  3: { name: 'Apply', hint: 'predict, calculate, read a record' },
  4: { name: 'Integrate', hint: 'combine ideas, extrapolate, design' },
};

export const GOALS: Record<Goal, { name: string; hint: string }> = {
  lesson: { name: 'Understand the lesson', hint: 'the core ideas, for the evening after reading' },
  course: { name: 'Course exam', hint: 'everything an exam on this lesson could ask' },
  mcat: { name: 'MCAT', hint: 'principles, calculations, data and drug predictions (original cards)' },
};

export const STORAGE_KEY = 'biochempedia:cards:v1';
const MIN = 60_000;
const DAY = 86_400_000;

export type Rating = 1 | 2 | 3 | 4; // Again, Hard, Good, Easy

export interface CardState {
  /** Ease factor. */
  e: number;
  /** Current interval in days (0 = still learning today). */
  i: number;
  /** Successful reviews in a row. */
  r: number;
  /** Lapses (Again after it had been learned). */
  l: number;
  /** Next due (ms). */
  due: number;
  /** Last answered (ms). */
  t: number;
}

interface Store { v: 1; cards: Record<string, CardState> }

const key = (slug: string, id: string) => `${slug}:${id}`;

export function loadStore(): Store {
  try {
    const raw = window.localStorage.getItem(STORAGE_KEY);
    const p = raw ? JSON.parse(raw) : null;
    if (p && p.v === 1 && typeof p.cards === 'object') return p as Store;
  } catch { /* storage blocked or corrupt: start empty */ }
  return { v: 1, cards: {} };
}

function saveStore(s: Store) {
  try { window.localStorage.setItem(STORAGE_KEY, JSON.stringify(s)); } catch { /* not remembered this visit */ }
}

export function stateOf(s: Store, slug: string, id: string): CardState | undefined {
  return s.cards[key(slug, id)];
}

/** What a rating would do to a card, without saving: used for the button labels too. */
export function next(st: CardState | undefined, rating: Rating, now = Date.now()): CardState {
  const cur = st ?? { e: 2.5, i: 0, r: 0, l: 0, due: now, t: now };
  let { e, i, r, l } = cur;
  if (rating === 1) {
    if (i >= 1) l++;
    e = Math.max(1.3, e - 0.2);
    return { e, i: 0, r: 0, l, due: now + 1 * MIN, t: now };
  }
  if (rating === 2) {
    e = Math.max(1.3, e - 0.15);
    i = i < 1 ? 0 : Math.max(1, Math.round(i * 1.2));
    return { e, i, r, l, due: i === 0 ? now + 6 * MIN : now + i * DAY, t: now };
  }
  if (rating === 3) {
    i = i < 1 ? 1 : i < 3 ? 3 : Math.round(i * e);
  } else {
    e += 0.15;
    i = i < 1 ? 4 : Math.round(i * e * 1.3);
  }
  return { e, i, r: r + 1, l, due: now + i * DAY, t: now };
}

export function rate(slug: string, id: string, rating: Rating): CardState {
  const s = loadStore();
  const k = key(slug, id);
  s.cards[k] = next(s.cards[k], rating);
  saveStore(s);
  return s.cards[k];
}

export function resetDeck(slug: string) {
  const s = loadStore();
  for (const k of Object.keys(s.cards)) if (k.startsWith(`${slug}:`)) delete s.cards[k];
  saveStore(s);
}

/** "10 min", "1 d", "3 mo": the label under a rating button. */
export function wait(st: CardState, now = Date.now()): string {
  const ms = st.due - now;
  if (ms < 60 * MIN) return `${Math.max(1, Math.round(ms / MIN))} min`;
  const d = Math.round(ms / DAY);
  if (d < 31) return `${d} d`;
  if (d < 365) return `${Math.round(d / 30)} mo`;
  return `${(d / 365).toFixed(1)} y`;
}

/** Split a cloze front into the parts before, inside and after its deletion. */
export function clozeParts(front: string): { before: string; answer: string; hint?: string; after: string } | null {
  const m = /^([\s\S]*?)\{\{c\d+::([\s\S]+?)(?:::([\s\S]+?))?\}\}([\s\S]*)$/.exec(front);
  return m ? { before: m[1], answer: m[2], hint: m[3], after: m[4] } : null;
}

const esc = (t: string) => t.replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;').replace(/[\t\n\r]+/g, ' ');

/** Anki import file (File → Import, a .txt with headers): Cloze and Basic notes in one file,
 *  deck and tags set per row, each back ending with a link to the lesson section. */
export function ankiText(deck: Deck, cards: Card[], site = 'https://biochemistrypedia.com'): string {
  const deckName = `Biochemistrypedia::${deck.title.replace(/::/g, ':')}`;
  const lines = ['#separator:tab', '#html:true', '#notetype column:1', '#deck column:2', '#tags column:5'];
  for (const c of cards) {
    const src = `<br><br><small><a href="${site}/lessons/${deck.slug}/">${esc(deck.title)}${c.section ? ` · ${esc(c.section)}` : ''}</a></small>`;
    const tags = [`biochempedia::${deck.slug}`, `level::${c.level}-${LEVELS[c.level].name.toLowerCase()}`, `type::${c.type}`, ...c.goals.map((g) => `goal::${g}`)].join(' ');
    const extra = [c.back, c.why].filter(Boolean).map((t) => esc(t!)).join('<br><br>');
    if (c.type === 'cloze') lines.push(['Cloze', deckName, esc(c.front), extra + src, tags].join('\t'));
    else lines.push(['Basic', deckName, esc(c.front), extra + src, tags].join('\t'));
  }
  return lines.join('\n') + '\n';
}
