# Biochempedia — Design Philosophy

The guiding principle, applied throughout the site:

## Read on the left, explore from the rail

A lesson is **a reading column plus a resource rail.** The student reads the
concept text in a comfortable column on the left; everything else — slides,
molecules, simulations, scientist profiles, video, podcast, the quiz, the
sources — lives as **compact thumbnails in a sticky rail on the right.** Tapping
a thumbnail opens that resource in a **full-screen lightbox** over the page;
closing it returns the student exactly where they were reading.

This keeps the page short and scannable (no wall of full-width blocks), keeps the
student in control of what they open, gives each resource the full screen when
it's open, and loads heavy media only when summoned.

### Layout

```
┌────────────────────────────────┬──────────────┐
│  Reading column                 │  Resource    │
│  (concept prose — stays open)   │  rail        │   ── click a thumb ──▶  ┌─────────────┐
│                                 │  · slides    │                         │  Lightbox   │
│  How we measure it (technique)  │  · molecules │                         │  (full      │
│                                 │  · sims      │                         │   screen)   │
│                                 │  · people    │                         └─────────────┘
│                                 │  · watch     │
│                                 │  · quiz      │
│                                 │  · sources   │
└────────────────────────────────┴──────────────┘
   (single column < 900px: rail drops below the text)
```

### Inside each lightbox — compact, progressive components

| Resource | Rail thumbnail | In the lightbox |
|---|---|---|
| **Lecture slides** | first-slide preview | a **slideshow** — one slide at a time, notes + narration per slide |
| **3D molecules** | the RCSB / PubChem image | the **live Mol\*** viewer (loads on open), rotatable |
| **Simulations** | icon | the **Michaelis–Menten plotter** / PhET (iframe loads on open) |
| **Scientists** | the book's **portrait** | the full **profile** — story, verbatim quotes, source |
| **Watch / listen** | YouTube thumbnail / 🎧 | the video (iframe on click) / Spotify player |
| **Test yourself** | 📝 | the quiz **stepper** — one question at a time, progress + score |
| **Sources** | 📚 | the full provenance manifest |

### What stays in the reading column (deliberately)

The **concept prose** and the brief **technique reference** stay inline — that's
the lesson's spine, meant to be read top to bottom. Everything interactive or
heavy is in the rail.

### Practical rules

- **Default to closed.** A resource opens only when the student asks.
- **Thumbnails must stand alone** — a real preview image where one exists (slide,
  structure, portrait, video), a clear icon + label otherwise.
- **Lazy-load heavy media** — the Mol\* viewer initializes on lightbox open;
  video/sim iframes load on click. Never load a player up front.
- **Use native `<dialog>` + `showModal()`** for the lightbox (free focus-trap,
  Esc-to-close, backdrop) and native `<details>` for simple in-place toggles.

This pattern should run through every future lesson — see
[`CONTRIBUTING.md`](CONTRIBUTING.md).
