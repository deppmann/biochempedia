# The hop graph

The site teaches the same ideas at several levels. Osmosis is in a grade 7 lesson, a high school
lesson and three college lessons. The hop graph is the one place that says so: which **ideas**
(concepts) the site teaches, which lessons teach each one, and what each level adds. With it a
reader on any lesson can hop one level down to a simpler lesson on the same idea, one level up to
a deeper one, or sideways to a neighbouring idea.

The graph lives in `src/data/topic-graph.json`. It is written offline, checked in, and read when
the site is built. No model runs when someone visits a page.

## What is in the file

- **Concept**: an idea a learner could ask for by name, with a one-sentence description, an area
  (a shelf for browsing) and a few everyday phrases people type when that idea is the answer.
- **Rungs**: the lessons on a concept.
  - `core`: the lesson is a place to learn the idea at its level. It carries a short note on what
    that level adds, and the section of the lesson to land on. A concept's core rungs, sorted by
    level, are its ladder.
  - `uses`: the lesson leans on the idea without teaching it. Shown as "also comes up in", never
    on a ladder.
  - A prerequisite is neither. The site's lesson links already carry "before this".
- **Films**: the films that show the idea, chosen one concept at a time.
- **Near**: sideways hops to other ideas, each with a one-sentence reason.
- **Lessons**: for each lesson with a record, the concepts it is on and a hash of the teaching
  text the record was written from.

Titles, courses and levels are not stored. The site joins them at build time
(`src/lib/topic-graph.ts`), so the graph cannot drift from the lessons.

Three things are true on purpose:

- A lesson with no record is normal. It works everywhere by course and level.
- A gap is information. Some ladders skip levels, and some ideas are taught at one level only.
  "No simpler version yet" is an honest thing for a page to say.
- A wrong rung is worse than a missing one. When in doubt, a rung is left out.

## How it is made

Readers (AI models; a person can do the same job) go through the lessons and answer in JSON. Every
answer is checked by `ingest.mjs` against the lessons and the wording rules before anything is
merged. The stages:

1. **Digest** (`digest.mjs`). One page per lesson: where it sits, hook, summary, objectives, every
   section with the id the built page gives it, how each section opens, the explain-at-my-level
   texts, each film's key, title and take-homes, and the links already on the page.
2. **Propose** (`prompts.mjs` `proposePrompt`). For each lesson, a reader names 1 to 3 ideas it
   teaches and up to 2 it leans on, reusing ids that already exist.
3. **Canonicalize** (`canonicalizePrompt`). Area by area, proposals that are one idea are merged
   into one id, and different ideas are kept apart. Then one pass looks across areas.
4. **Near** (`nearPrompt`). Sideways hops are written for each concept.
5. **Verify** (`verifyPrompt`). A reader who did not write the entry is shown a concept and the
   digests of its lessons and asked: is this one idea at every rung, and is each rung really a
   place to learn it? A rung judged wrong is removed and logged. It is not argued with.
6. **Review** (`review/<name>.json` in the staging folder). Whoever reads the result writes
   corrections as one more answer file: a rung to add, move or reword, a concept to make or merge,
   a sideways hop to add, each with its reason. It is applied after the verdicts and goes through
   the same checks.
7. **Ingest** (`ingest.mjs`). Merges everything in one fixed order and prints a report: what the
   graph now holds, every change applied, and every item rejected with its reason.

`emit.mjs` writes the prompt files for each stage into a staging folder, with a manifest that says
where each answer goes. `dry-run.sh` runs all of it with stand-in answers to test the plumbing.

```sh
node scripts/topic-graph/digest.mjs --print diffusion-and-osmosis   # read one digest
node scripts/topic-graph/emit.mjs propose --staging .graph-staging/fill
node scripts/topic-graph/ingest.mjs --staging .graph-staging/fill --dry
sh scripts/topic-graph/dry-run.sh                                     # the whole pipeline, stand-in answers
```

## How one lesson is topped up

When a lesson is new or rewritten:

```sh
node scripts/topic-graph/assign.mjs --list                  # lessons with no record, or a stale one
node scripts/topic-graph/assign.mjs --emit <slug> > prompt.txt
# give prompt.txt to a capable model, save its JSON answer as answer.json
node scripts/topic-graph/assign.mjs --apply answer.json     # checks it, merges it, prints a report
```

With an API key in the environment, `assign.mjs --call <slug>` does the middle step itself. The
answer replaces that lesson's rungs and nothing else. If it creates a new concept, the report lists
it: read it, because the top-up has no merging step.

## How it is checked

`node scripts/check-topic-graph.mjs` runs in CI on every push.

It **fails** on a broken record: a lesson or film that does not exist or is not live, a concept
with no lesson that teaches it, a bad or repeated id, an alias that is another concept's name, a
note, description or reason that is too long or breaks the wording rules (no product, company or
test names, nothing phrased as medical advice, no analogy formulas, no dashes used as punctuation),
or a file that is not in the order the tools write.

The medical-advice and analogy rules are the lesson-links rules read with allowances for the graph
(`medicalAdvice` and `analogyFormula` in `lib.mjs`). The graph's copy names science, so "dose-response
curve", "dosage compensation", "parallel fibres", "mirror drawing" and "analogous structures" pass.
A dose or a treatment asked for ("what dose", "should I take", "how to treat my") and an analogy
formula ("is like a", "think of it as", "mirrors", "parallels", "by contrast") still fail. Lesson
links keeps its own, stricter rules for search phrases.

Two concepts with one name are a failure in the committed graph and in any ingest that writes. In
a `--dry` ingest before the canonicalize stage has answered they are a warning: two readers gave
one idea two ids, and merging them is that stage's job. Its prompts list the pairs under
"ONE NAME, TWO IDS", and `emit.mjs status` shows them.

It only **warns**, listing each lesson, when:

- a live lesson has no record;
- a record was written before its lesson's teaching text last changed. The hash covers the hook,
  summary, objectives, headings and body prose, so a new quiz question or a credit line does not
  count;
- a rung's section anchor no longer matches a heading. The link then goes to the top of the
  lesson. When the site has been built, anchors are checked against the built pages.

`node scripts/test-topic-graph.mjs` tests every rule with a good and a bad case, the merge, and
every function of the build-time API, against the real lessons.

## What the site gets

- `src/lib/topic-graph.ts`, at build time: `conceptsOf(slug)`, `concept(id)`, `ladder(id)`,
  `ladderByLevel(id, withGaps)`, `usedBy(id)`, `hops(slug)` (down, up and sideways for each idea a
  lesson teaches, with the size of each jump), `filmsFor(id)`, `searchIndex()`.
- `/graph.json`: a small index for browsers. Every idea's name, description, phrases and levels,
  and which ideas each lesson teaches.
- `/graph/<area>.json`: one area's ladders, notes, films and sideways hops.
  `/graph/all.json`: everything in one file.
- `node scripts/topic-graph/size.mjs` prints how big those files are and how big they will get.

## Files

| File | What it does |
|---|---|
| `lib.mjs` | Loads the site (through the lesson-links loader), the content hash, the areas, the rules, `validateGraph` |
| `digest.mjs` | One digest per lesson |
| `prompts.mjs` | The words used to ask a model, in one place |
| `emit.mjs` | Writes prompt files and manifests for a fill; stand-in answers for testing |
| `ingest.mjs` | Checks answers and merges them; the report |
| `assign.mjs` | The single-lesson top-up |
| `size.mjs` | Size of the browser files |
| `dry-run.sh` | The whole pipeline with stand-in answers |
| `fixtures/seed-graph.json` | The 34 hand-written concepts the first fill started from; the tests edit copies of it |
| `../check-topic-graph.mjs` | The CI check |
| `../test-topic-graph.mjs` | The tests |
| `../../src/lib/topic-graph-core.mjs` | The logic shared by the site, the endpoint and the tools |
