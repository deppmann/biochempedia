# Biochempedia

An interactive, **integrity-first** biochemistry learning site for BIOL 3030 at the
University of Virginia — the deliverable for Prof. Chris Deppmann's AI Catalyst
grant, *"Biochempedia: An AI Tutor and Interactive Textbook."*

Every molecular structure is loaded **live from a public database** (nothing is
drawn by an AI). Every simulation is something a student can poke. Every question
carries a verified answer and an explanation. The content is built from twenty
years of lectures and the scientist stories in *The Molecule Hunters*.

> **Status:** First version. **One fully-finished exemplar lesson** —
> *Enzyme Kinetics / Michaelis–Menten* — plus the site skeleton, the typed lesson
> schema, and the build-time integrity gate. The AI tutor and "talk to a
> scientist" features are intentionally **deferred** (see below).

## What's in the exemplar lesson

`src/content/lessons/enzyme-kinetics/lesson.mdx`

- The concept explained plainly (from Chris's CH07/CH08 slide notes) + a
  "how the technique works" section (assays, initial velocity, Km/Vmax).
- A **live, rotatable Mol\* structure** — hen egg-white lysozyme (PDB `1LYZ`) —
  and the **PubChem** small-molecule view of its substrate (CID `439174`).
- An **original Michaelis–Menten plotter** (v vs [S] with draggable/typed Km & Vmax,
  a live Lineweaver–Burk double-reciprocal, and a competitive-inhibitor overlay)
  plus a **PhET** embed.
- 4 grounded **scientist cards** with verbatim book quotes (Fischer, Michaelis &
  Menten, Koshland, Phillips).
- A **Spotify** episode embed + 2 curated **YouTube** embeds.
- A self-test quiz: **5 original practice + 3 original MCAT-style** questions, each
  with a verified key and rationale.
- An auto-generated **Sources & Integrity** footer listing every ID, attribution,
  and media source.

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
- a question is missing its `answer` or `rationale`,
- a structure isn't from a real `rcsb`/`pubchem` accession ID, or
- a PhET sim isn't attributed to PhET.

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

Cloudflare Pages at `biochempedia.deppmannlab.com` — **public** (no Cloudflare
Access; the members/corpus surfaces are the gated ones). Static Astro build,
output `dist/`. The brand comes from the real [`deppmann-brand`](https://github.com/deppmann/deppmann-brand)
package via the `brand/` submodule; [`src/styles/tokens.css`](src/styles/tokens.css)
aliases those tokens onto the components' `--ddp-*` names.

> **DNS guardrail (from the Phase-0 decisions):** the public `deppmannlab.com`
> apex/www stay on **Netlify, DNS-only** — never proxy Netlify through
> Cloudflare. Only the subdomains get Cloudflare Pages. Full ecosystem decisions
> live in the brand repo's `DECISIONS.md`.

## License

Code: **MIT** ([LICENSE](LICENSE)). Lesson narrative & scientist profiles are the
authors' IP ([NOTICE](NOTICE)) — fork the code, bring your own content.

🤖 Scaffolded with [Claude Code](https://claude.com/claude-code).
