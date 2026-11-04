# Lesson flashcards

Each lesson can have a deck at `src/data/flashcards/<slug>.json`. If a deck exists, the lesson page shows a **Flashcards** button in the rail and in the mobile chips, and `/lessons/<slug>/#flashcards` opens it directly. The pop-out is `src/components/FlashcardDeck.astro`; the schedule and the Anki export are in `src/lib/flashcards.ts`. No model runs on the site: decks are static data written ahead of time.

## What a card is
```json
{"id": "action-potential-c07", "type": "predict", "level": 3, "goals": ["lesson","course","mcat"],
 "front": "…", "back": "…", "why": "optional", "quote": "verbatim span of the lesson", "section": "heading"}
```
- **level** is a ladder of abstraction: 1 Recall, 2 Explain, 3 Apply (predict, calculate, read a record), 4 Integrate (combine sections, extrapolate, design an experiment).
- **goals** feed the "I'm studying to" switch:
  - `lesson`: the core ideas;
  - `course`: what a course exam could ask;
  - `mcat`: MCAT-scope reasoning on original cards.
- **type** is one of cloze, qa, predict, experiment, calc.
- **quote** grounds the card. The validator rejects any card whose quote is not in the lesson. On the page, the quote is what "Show in lesson" and "Highlight the source as I go" find and highlight. If a later edit removes the passage, the page holds the card back until the deck is regenerated.

## Pipeline (per lesson)
1. `node scripts/flashcards/extract.mjs <slug> <work>` takes no tokens. It writes `digest.md`, the lesson body as plain sections plus the objectives and quiz keys, about 35% smaller than the .mdx. It also writes `extract.json`, a scaffold deck built from definitions, rule boxes, Predict boxes and the quiz.
2. **Draft (Sonnet)** from `digest.md` and `extract.json`, following `AUTHOR_BRIEF.md`. Validate with `validate.mjs`.
3. **Arbiter (Opus)** following `ARBITER_BRIEF.md`. It checks every card, re-derives the numbers, and tightens the levels and goal tags.
4. `node scripts/flashcards/finalize.mjs <slug> <deck.json> '<generation record>'` installs the deck. It adds sections and stable ids and records the section hashes.
5. `node scripts/check-flashcards.mjs` runs in CI. It fails on schema errors and warns on drift.

The author, arbiter and judge briefs, and the pilot A/B results, are kept with the private build notes.

## After a lesson is edited
Run `node scripts/flashcards/stale.mjs <slug>`. It lists the sections whose text changed since generation and the cards written from them. Send only those sections and cards back through steps 2–4; the rest of the deck stays as it is. A typical edit touches one or two sections, so a refresh costs a fraction of a full deck.
