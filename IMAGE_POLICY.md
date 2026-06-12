# Image & Structure Integrity Policy

Biochempedia teaches biochemistry. A confidently-wrong picture does real harm, so
the project is built so that **bad visual content cannot ship** — the rules below
are enforced by the build, not by good intentions.

## The rules

### 1. Molecular structures: only from a real accession ID. No exceptions.
Every 3D structure is loaded **live** by accession ID:
- **macromolecules** → RCSB Protein Data Bank (`source: "rcsb"`, coordinate data CC0)
- **small molecules** → PubChem (`source: "pubchem"`)

There is **no way to express an AI-drawn or hand-rolled structure** in the schema —
the `structures[]` field only accepts `source: "rcsb" | "pubchem"` plus an `id`.
An AI is never asked to draw a molecule, ever. If a structure won't load, the
viewer shows a link to the source database — it never invents geometry.

### 2. AI-generated images: flagged + human-verified, or the build fails.
An AI-generated raster image is allowed **only if** its frontmatter entry has:
```yaml
- src: "/path/to/figure.png"
  alt: "descriptive alt text"
  aiGenerated: true
  factCheckedBy: "Jane Student"   # a real human who checked it for accuracy
```
If `aiGenerated: true` and `factCheckedBy` is missing or empty, **`npm run build`
fails** (try it — see the demo below). Unreviewed AI images do not ship.

### 3. Mechanism diagrams: original or CC-licensed-with-attribution.
A non-AI image must declare where it came from via a `credit` field — either
`"Original — <name>"` or a CC license plus attribution. A non-AI image with no
`credit` also fails the build.

### 4. The exemplar lesson uses zero raster images — on purpose.
The enzyme-kinetics lesson renders every structure live (Mol*/PubChem) and draws
its kinetics plots from equations in the browser. There is nothing to fact-check.
This is the recommended default: **prefer live data and generated plots over
static figures.**

## How the enforcement works

The gate lives in [`src/schema.ts`](src/schema.ts) as Zod `superRefine` checks on
the `images`, `structures`, and `question` shapes. Astro validates every lesson's
frontmatter against this schema during `astro build`, so any violation aborts the
build with a clear message.

### Demo: prove it fails
Add a lesson (or temp fixture) with this frontmatter and run `npm run build`:
```yaml
images:
  - src: "/x.png"
    alt: "an AI image with no fact-checker"
    aiGenerated: true       # no factCheckedBy → build fails
practiceQuestions:
  - stem: "Q with no rationale"
    choices: ["a", "b"]
    answer: 0               # no rationale → build fails
```
The build stops with:
```
images.0.factCheckedBy: aiGenerated:true requires a non-empty factCheckedBy.
                        Unreviewed AI images are not allowed.
practiceQuestions.0.rationale: Required
```

## Questions, too
Every practice and MCAT-style question must carry a correct `answer` (a valid
index into its `choices`) **and** a `rationale`. A question missing either fails
the build. MCAT-style items are **original** to this site and are never real AAMC
questions.

See also [`LICENSING.md`](LICENSING.md) for the allowed/banned source list.
