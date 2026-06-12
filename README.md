# biochempedia

**Biochempedia** — a public teaching platform from the Deppmann Lab, at
**`biochempedia.deppmannlab.com`**. This repo is the Phase-0 scaffold: an
on-brand landing page plus the shared brand. The lessons come next.

## Host & gate decisions

- **Host:** Cloudflare Pages (static Astro build, output `dist/`).
- **Gate:** **public** — no Cloudflare Access. (Members/corpus are gated;
  Biochempedia is the open teaching surface.)
- **DNS:** `biochempedia.deppmannlab.com` is a Cloudflare Pages custom domain.
  The public `deppmannlab.com` stays on **Netlify (DNS-only)** —
  **never proxy Netlify through Cloudflare.**
- **Brand:** consumes [`@deppmann/brand`](https://github.com/deppmann/deppmann-brand)
  via the `brand/` git submodule (tokens + shared `Footer`).
- **Repo visibility:** public.

Full ecosystem decisions + kill switches: brand repo `DECISIONS.md`.

## What it will be (not built here)

A teaching platform built to be honest about what it knows:

- One finished **exemplar lesson** first (enzyme kinetics / Michaelis–Menten) +
  a content pipeline, then scale with the student.
- **Real molecular structures** rendered from RCSB PDB / PubChem via Mol\* —
  never AI-generated geometry.
- Citation-faithful explanations; a visible guardrail that flags any cited claim
  not in the retrieved set.
- Cross-links to *The Molecule Hunters* (book) and the *We Are Biochemistry*
  podcast so the three surfaces share one narrative spine.

## Develop

```bash
git clone --recurse-submodules https://github.com/deppmann/biochempedia.git
cd biochempedia
npm install
npm run dev
npm run build   # → dist/
```

Forgot submodules? `git submodule update --init --recursive`.

## Deploy

Cloudflare Pages → connect this repo → build `npm run build`, output `dist`,
**Git submodules: On**. Add custom domain `biochempedia.deppmannlab.com`. No
Access application (public).

## Contributing

Edit content/pages, open a PR — don't push to `main`. Brand changes (color,
type, footer) go in the **brand** repo, not here.
