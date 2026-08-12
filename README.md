# Biochempedia

An interactive, **integrity-first** biochemistry learning site for BIOL 3030 at the
University of Virginia — the deliverable for Prof. Chris Deppmann's AI Catalyst
grant, *"Biochempedia: An AI Tutor and Interactive Textbook."*

Every molecular structure is loaded **live from a public database** (nothing is
drawn by an AI). Every simulation is something a student can poke. Every question
carries a verified answer and an explanation. The content is built from twenty
years of lectures and the scientist stories in *The Molecule Hunters*.

> **Status:** 30 lessons, all published — the one-semester sequence, an opening
> interlude on vitalism, and two closing supplements (nucleotide metabolism,
> integration of metabolism). 34 pages, 305 lecture slides, ~60 original
> interactive islands, 407 live structure references. The AI tutor and "talk to a
> scientist" features are intentionally **deferred** (see below). The Metabolism
> Arcade is held back from v1 and lives on `origin/five-game-redesign`.

## What's in a lesson

Every lesson is one folder — `src/content/lessons/<slug>/lesson.mdx` — validated
against the typed schema in `src/schema.ts`. Copy a folder to start a new one.
`enzyme-kinetics` is the reference implementation:

- The concept explained plainly (from Chris's lecture notes) plus a generated
  "how we measure it" techniques panel.
- **Live, rotatable Mol\* structures** loaded by accession ID from RCSB PDB
  (macromolecules) and PubChem (small molecules) — for this lesson, hen egg-white
  lysozyme (PDB `1LYZ`) and its substrate (CID `439174`).
- **Original interactive islands** — here, a Michaelis–Menten plotter with
  draggable Km/Vmax, a live Lineweaver–Burk double-reciprocal, and a
  competitive-inhibitor overlay — plus a **PhET** embed.
- **Scientist cards** with verbatim quotes from *The Molecule Hunters*.
- **Spotify** and **YouTube** media, embedded from source and never rehosted.
- A self-test of original practice and MCAT-style questions, each with a verified
  key and rationale.
- **Lecture slides** with presenter notes and narration, each naming the person who
  screened it for accuracy and copyright.
- An auto-generated **Sources & Integrity** panel listing every ID, attribution, and
  media source in that lesson.

## Stack

- **Astro 5** (static-first; islands only where interactive) + `@astrojs/mdx`
- **Content Collections + Zod** — the typed lesson schema *is* the integrity gate
- **Tailwind v4** (via `@tailwindcss/vite`) + a stubbed `deppmann-brand` token layer
- **Mol\*** for 3D structures · **PhET** (iframe) · YouTube/Spotify (iframe)

## Run it

```bash
git clone --recurse-submodules https://github.com/deppmann/biochempedia
cd biochempedia
npm install
npm run dev        # http://localhost:4321
npm run build      # astro check + build; FAILS if any integrity field is missing
```

> The shared brand (`@deppmann/brand`) is vendored as the **`brand/` git
> submodule**; the build imports `brand/tokens.css`, so clone with
> `--recurse-submodules` (or run `git submodule update --init`). Already cloned
> without it? `git submodule update --init`.

The Mol* viewer bundle is vendored from `node_modules` into `public/vendor/` by a
`predev`/`prebuild` hook (`npm run sync:molstar`); it's gitignored and regenerated.

## The integrity gate

The build **fails** if:
- an image has `aiGenerated: true` without a `factCheckedBy`,
- a question is missing its `answer` or `rationale`, or points at a choice index
  that doesn't exist,
- a structure's `id` isn't well-formed for its `source` (a 4-character PDB code for
  `rcsb`, an all-digit CID for `pubchem`),
- a lecture slide doesn't name who screened it, or
- a PhET sim isn't attributed to PhET.

Local asset and link references are checked separately by `scripts/check-assets.mjs`,
which fails the build on any broken local reference. What the build does **not** do is
confirm that a remote accession still resolves — that is a periodic manual audit, last
run 2026-08-01 against the live RCSB and PubChem APIs (378 unique IDs, all resolving).

See [`IMAGE_POLICY.md`](IMAGE_POLICY.md), [`LICENSING.md`](LICENSING.md), and
[`src/schema.ts`](src/schema.ts).

## Add a lesson

Copy the lesson folder, fill the schema, write the prose, make the build pass, open
a PR. Full walkthrough in [`CONTRIBUTING.md`](CONTRIBUTING.md).

## Deferred (not in this version)

The **AI tutor** and **scientist-persona chat** are intentionally not built yet — a
tutor that is confidently wrong would do real harm. When added, they will be
RAG-grounded in the course material, carry an "AI — verify" banner, and reuse the
research project's retrieval module.

## Deploy target

A **Cloudflare Worker** (Workers Builds), git-connected to `main` — a push builds
and deploys automatically, ~1–2 min. Static Astro build, output `dist/`.
**Public**; no Cloudflare Access (the members/corpus surfaces are the gated ones).

- Worker origin: `biochempedia.deppmann.workers.dev`
- Public canonical domain: **`biochemistrypedia.com`** (Cloudflare Registrar,
  Cloudflare nameservers, same account as the Worker)

`site` in [`astro.config.mjs`](astro.config.mjs) must equal the public canonical
domain — canonical links, OG urls, and `/sitemap.xml` all derive from it, and
`public/robots.txt` hardcodes the sitemap URL alongside it. Change all three
together or search engines get pointed at a host that isn't bound.

The brand comes from the real [`deppmann-brand`](https://github.com/deppmann/deppmann-brand)
package via the `brand/` submodule; [`src/styles/tokens.css`](src/styles/tokens.css)
aliases those tokens onto the components' `--ddp-*` names.

> **DNS guardrail (from the Phase-0 decisions):** `deppmannlab.com` apex/www stay
> on **Netlify, DNS-only** — never proxy Netlify through Cloudflare. That domain
> is not involved in this deploy: `biochemistrypedia.com` is a separate
> Cloudflare-registered zone. Full ecosystem decisions live in the brand repo's
> `DECISIONS.md`, which still describes the older `biochempedia.deppmannlab.com`
> plan and wants updating.

## License

Code: **MIT** ([LICENSE](LICENSE)). Lesson narrative & scientist profiles are the
authors' IP ([NOTICE](NOTICE)) — fork the code, bring your own content.

🤖 Scaffolded with [Claude Code](https://claude.com/claude-code).
