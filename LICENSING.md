# Licensing & Source Policy

This file is the **allow / deny list** for everything that goes into a Biochempedia
lesson. When in doubt, ask before adding a source.

## Code vs. content

| Layer | License |
|---|---|
| Site code, components, build scripts, original simulations | **MIT** (see [LICENSE](LICENSE)) |
| Lesson narrative & scientist profiles | **Authors' IP** — *The Molecule Hunters* / Deppmann lectures (see [NOTICE](NOTICE)). Not MIT. |

## ✅ Allowed source material

- **Prof. Deppmann's own lecture slides & recording scripts** (BIOL 3030).
- **"The Molecule Hunters" / "Biochemists Through Time"** (Deppmann & Oliver) —
  the authors' own book. Quote verbatim and **cite the manuscript** via each
  scientist's `profileSourceAnchor`.
- **"We Are Biochemistry" podcast** — embed from Spotify (show `6gUAeZTYYRPzdAc84Lj4Gt`).
- **RCSB Protein Data Bank** — structure **coordinate data is CC0**. Load live by PDB ID.
- **PubChem** — small-molecule data. Load live by CID.
- **PhET Interactive Simulations** — **CC BY 4.0**. Embed the HTML5 sim and include
  the attribution: *"PhET Interactive Simulations, University of Colorado Boulder,
  https://phet.colorado.edu."* (The schema enforces that a PhET entry actually
  names PhET.)
- **YouTube videos** — embed only (iframe), with a `sourceNote` crediting the channel.
- **Mol\*** viewer — MIT (https://molstar.org).

## ⛔ Banned — never use

- ❌ **The Tymoczko textbook** (*Biochemistry: A Short Course*) — any text or figure.
- ❌ **Publisher slide decks** or instructor resources.
- ❌ **Any copyrighted figure** — diagrams, photos, charts from textbooks, papers,
  or the open web (unless explicitly CC-licensed and attributed).
- ❌ **Real AAMC / MCAT questions.** All MCAT-style items must be **original** and
  labelled "MCAT-style (original)."
- ❌ **AI-drawn molecular structures** — impossible by construction; always use a
  real accession ID.

## Media licenses summary

| Source | License | How we use it |
|---|---|---|
| RCSB PDB coordinates | CC0 | Live load by PDB ID |
| PubChem | (NLM / public) | Live load by CID |
| PhET | CC BY 4.0 | Iframe embed + attribution |
| YouTube | owner's | Iframe embed only |
| Spotify | owner's | Iframe embed only |
| Mol* | MIT | Bundled viewer |

See [IMAGE_POLICY.md](IMAGE_POLICY.md) for how these rules are enforced at build time.
