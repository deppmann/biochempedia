# The hop components

Hopping is the site's own idea: every idea is taught at several levels, and a reader can go one
level simpler or one level deeper. These components draw it. All of them are built from the hop
graph (`src/data/topic-graph.json`, through `src/lib/topic-graph.ts` and `src/lib/hop.ts`) when the
site is built. No model runs and nothing is stored when someone visits.

## The ladder: the shared picture

One drawing, three sizes. Up the ladder is deeper, down is simpler. Hex stands on the rung the
reader is on. Hex marks "you are here" and nothing else: no rung is locked, greyed or filled, and
nothing is counted.

| Size | What it is | Footprint |
|---|---|---|
| `full` | An upright ladder with a rung per level where the idea is taught. Each rung carries its lesson (or lessons), the note on what that level adds and, if asked, course, minutes, film and practice questions. | Up to 40rem wide; 56px of ladder, the rest text. About 110px per rung on a phone. |
| `compact` | The ladder as a mark: seven places, a rung where there is a lesson, a gold hexagon on the reader's level. | 20 by 44px |
| `tiny` | The same mark, for a list. | 14 by 31px |

### In an Astro page

```astro
---
import Ladder from '../components/hop/Ladder.astro';
import { idea } from '../lib/hop';
const osmosis = await idea('osmosis');
---
<Ladder idea={osmosis} here="crossing-the-membrane" />   <!-- full, on a lesson -->
<Ladder idea={osmosis} />                                 <!-- full, no reader: every rung, no Hex -->
<Ladder size="compact" mask={osmosis.mask} hereRank={2} />
<Ladder size="tiny" mask={osmosis.mask} />
```

| Prop | For | Meaning |
|---|---|---|
| `size` | all | `full` (default), `compact`, `tiny` |
| `idea` | full | From `idea(id)` in `src/lib/hop.ts` |
| `mask` | compact, tiny | Levels with a lesson as a bit mask, bit 0 = ages 5 to 10. Defaults to `idea.mask`. `/graph.json` gives it as `l`. |
| `here` | full | Slug of the lesson the reader is on. Hex stands on its rung; the lesson is bold, not a link; other lessons link with `?from=<slug>`. |
| `hereRank` | all | A level, 0 to 6, when there is no lesson: a film's level, a level the reader chose. |
| `hex` | full | Draw Hex (default). Pass `false` on a second ladder in the same view: one Hex in view. |
| `window` | full | Show the reader's rung and the nearest rung each way first, with a "Show all N levels" button. Default: on when `here` is set. This is what keeps a phone from opening on the graduate rungs. |
| `facts` | full | Course, minutes, film and practice questions under each lesson (default on). Turn off where space is tight. |
| `play` | full | Show "Play the ladder" when the idea has films at two or more levels (default on). |

### From a client script

`src/lib/hop-ladder.mjs` has no Astro and no Node in it. Import it in a `<script>` and hand it
graph data (for example from `/graph/<area>.json`; `src/lib/hop-find.ts` shows how to turn that
file's rows into rungs).

```js
import { ladderHtml, ladderGlyph, wireLadders } from '../lib/hop-ladder.mjs';

host.innerHTML = ladderHtml(
  { id: 'osmosis', name: 'Osmosis', short: 'osmosis',
    rungs: [{ slug, title, href, rank, courseTitle, adds, minutes, film: { href, seconds, title }, questions, sol }] },
  { here: null, hereRank: 2, hex: true, window: false, facts: true,
    play: { href, n: 4, minutes: 13, from: 1, to: 5 } },
);
wireLadders(host);                                  // the "Show all levels" button, when windowed
mark.innerHTML = ladderGlyph(mask, { here: 2, size: 'tiny' });
```

To move Hex when the reader picks a rung, draw the ladder again with the new `here` or `hereRank`.
Hex lands with a short drop, off under reduced motion. Never move Hex on a timer.

Load `src/styles/hop.css` on any page that draws a ladder (the Astro components import it).

### Rules for anyone who uses it

- The marks are pictures only (`aria-hidden`). Put the same thing in words beside them:
  `compactLine()` or `taughtAt()` in `src/lib/hop-words.mjs`.
- The markup is written simplest first and stood upright by the styles, so a screen reader, a page
  without styles and a keyboard all go from the simplest level to the deepest.
- The words are "Simpler" and "Deeper". Never "easier", "harder", "level up", or a step number.
- A level with no lesson is one short line with broken rails. Do not stretch it.

## Play the ladder

For an idea with films at two or more levels, `idea.play` is `{ href, n, minutes, from, to }` and the
full ladder shows "Play the ladder · 4 films, about 13 min, from grade 7 to upper-level college."
The films, in order from the simplest level to the deepest, are in `/ideas/film-runs.json`:

```json
{ "v": 1, "link": "/films/run/?idea={id}",
  "runs": { "osmosis": { "name": "Osmosis", "seconds": 767,
    "films": [["diffusion-and-osmosis/chapter-2", "title", "/watch/…/", 1, 196, "diffusion-and-osmosis"]] } } }
```

Each film row is `[film key, title, film page, level 0 to 6, seconds, lesson slug]`. The run page
belongs to the film library. Until it reads `?idea=`, the link opens the first film's own page with
`?idea=<id>` in the address. To point every link at the run page, change `playHref()` in
`src/lib/hop.ts`. A run must say how many films it holds and where it ends, and must wait for the
viewer between films.

## The other pieces

| File | What it is |
|---|---|
| `HopSentence.astro` | Under a lesson's hook: which idea the lesson teaches and at what level, with "Simpler" and "Deeper". "read a short … version here" opens the lesson's own short version in place. "See every level" opens the ladder for each idea, the ideas next door and the other short versions. `variant="line"` is the sentence alone. |
| `HopCompact.astro` | One line for a film card or a search result: the compact ladder and "Osmosis, high school. Also at: grade 7 and a first college course." |
| `HopTrio.astro` | "Simpler / This step / Deeper" for a step of a study path or beside a film. A side with no lesson is left out. |
| `HopStandards.astro` | Essential question and Virginia standards on a school lesson, in plain type. |

The words are all in `src/lib/hop-words.mjs`. `node scripts/test-hop.mjs` runs the sentence over
every lesson and draws a ladder for every idea; `node scripts/test-hop.mjs --print` prints every
sentence for reading. `/ideas/parts/` shows every size on real lessons.
