# Biochempedia — Design Philosophy

The guiding principle, applied throughout the site:

## Progressive disclosure — compact by default, expand on demand

A lesson should feel like a tidy, scannable index — not a wall of full-width
blocks the student has to scroll past. Heavy or secondary content is **collapsed
into a compact, summarized item that the student opens when they want it.** This
keeps the page short, keeps the student in control, and (for media) keeps the
page fast.

### How each element applies it

| Element | Compact (default) | Expanded (on demand) |
|---|---|---|
| **Lecture slides** | A **slideshow** — one slide at a time, prev/next + dots + counter | Notes collapse under "Presenter notes"; audio plays inline |
| **Scientists** | A card: portrait + name + one-line contribution | Click → full story (from the book) + verbatim quotes + source |
| **Questions** | A **stepper** — one question at a time, progress bar, score | Pick an answer → instant verdict + rationale |
| **YouTube** | A thumbnail with a play button | Click → the iframe loads (lazy) and plays |
| **PhET** | A "Launch the interactive" panel | Click → the sim iframe loads |
| **Sources & Integrity** | A single collapsed line | Click → the full provenance manifest |

### What stays prominent (deliberately)

Not everything should be hidden. The **concept prose**, the **live Mol\*
structure**, and the **original Michaelis–Menten plotter** are the heart of the
lesson and stay open — they're what the student came for. Progressive disclosure
is for the *supporting* material around them.

### Practical rules

- **One thing open at a time, by the student's choice.** Default to collapsed.
- **Summaries must stand alone** — the collapsed state should tell the student
  whether it's worth opening.
- **Lazy-load heavy media** (video/sim iframes) behind a click — never load a
  player the student hasn't asked for.
- **Use native `<details>`/`<summary>`** where a simple toggle suffices (it's
  keyboard- and screen-reader-accessible for free); reach for a JS island only
  when you need a stepper/slideshow.

This philosophy should run through every future lesson — see
[`CONTRIBUTING.md`](CONTRIBUTING.md).
