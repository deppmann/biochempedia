# Contributing a lesson to Biochempedia

A lesson is **one folder**. To add lesson #2, you copy the example folder, fill in
the data, write the prose, and open a pull request. The build checks your work.

You do **not** need to touch any component or page — every interactive piece (the
3D viewers, the plotter, the embeds, the quiz, the sources footer) renders
automatically from the data you put in the lesson's frontmatter.

---

## 1. Set up

```bash
git clone --recurse-submodules https://github.com/deppmann/biochempedia
cd biochempedia
npm install
npm run dev          # opens http://localhost:4321
```

(The `--recurse-submodules` pulls the shared `brand/` package the build imports.
Already cloned? Run `git submodule update --init`.)

## 2. Copy the example folder

```bash
cp -r src/content/lessons/enzyme-kinetics src/content/lessons/your-topic
```

Rename nothing inside except what you edit. Each lesson is
`src/content/lessons/<slug>/lesson.mdx`.

## 3. Fill in the frontmatter (the data)

The frontmatter (the block between the `---` lines at the top of `lesson.mdx`) is
the **single source of truth** for the lesson. It is validated against
[`src/schema.ts`](src/schema.ts) at build time. Fields:

| Field | What it is |
|---|---|
| `title`, `slug`, `summary` | Lesson title, URL slug (match the folder name), one-paragraph summary. |
| `objectives[]`, `estMinutes` | 3–4 "what you'll learn" bullets and a rough time-on-page — they power the orientation card at the top of the lesson. |
| `courseChapter` | The course slide-deck title this maps to (e.g. "Mechanisms and Inhibitors"). |
| `order` | Sort order on the home page. |
| `scientists[]` | `{ name, dates, contribution, profileSourceAnchor, quotes[] }`. Quotes must be **verbatim** from the book/record; `profileSourceAnchor` cites where. |
| `techniques[]` | `{ name, blurb }` for the "how we measure it" panel. |
| `structures[]` | `{ label, source, id, note, caption }`. `source` is `"rcsb"` (a PDB ID) or `"pubchem"` (a CID). **Never anything else.** |
| `podcast` | `{ platform: "spotify", url, title, note }`. A show or episode `open.spotify.com` URL. |
| `videos[]` | `{ title, youtubeId, sourceNote }`. `youtubeId` is the 11-char id, not a URL. |
| `simulations[]` | `{ type, ref, title, attribution, caption }`. `type:"phet"` → `ref` is the HTML5 sim URL; `type:"local"` → `ref` is a registered component name. |
| `practiceQuestions[]`, `mcatQuestions[]` | `{ stem, choices[], answer, rationale }`. `answer` is the **0-based index** of the correct choice. |
| `images[]` | `{ src, alt, aiGenerated, factCheckedBy, credit }`. See the integrity rules below. Prefer leaving this **empty** and using live structures. |
| `lectureSlides[]` | `{ src, alt, title, notes, audio, source, credit, reviewedBy }`. Slides from your own deck with presenter `notes` (and an optional narrated `audio` voiceover) shown beneath. `reviewedBy` is **required** — name who confirmed the slide is accurate AND copyright-clean (your own content, no reproduced publisher figures), or the build fails. |
| `corpusTags[]` | Tags reserved for the future AI tutor. Add a few; they aren't rendered yet. |

### Where to find the IDs

- **PDB ID** (macromolecule): search https://www.rcsb.org. Verify it loads — paste it
  at `https://www.rcsb.org/structure/<ID>`. Example: `1LYZ` (lysozyme).
- **PubChem CID** (small molecule): search https://pubchem.ncbi.nlm.nih.gov; the CID
  is the number in the URL. Example: `439174` (N-acetylglucosamine).
- **YouTube id**: the `v=...` part of a watch URL. Use reputable channels and credit them.
- **PhET sim**: must be an **HTML5** sim (some old ones are Java and won't embed). The
  embeddable URL looks like
  `https://phet.colorado.edu/sims/html/<name>/latest/<name>_all.html`.
- **Spotify**: any `open.spotify.com/show/...` or `.../episode/...` URL.

## 4. Write the prose (the body)

Everything **below** the closing `---` is the lesson's plain-language explanation,
in Markdown: the concept, and how the technique works. Keep it to a readable
column. You don't embed components here — the structures, plotter, videos, quiz,
and sources render in their own sections automatically, in this order:

> orientation card → prose → techniques → **from the lecture** → structures → simulations → scientists → watch & listen → self-test → Sources & Integrity

## 4b. Make it easy to use (and to hear)

A lesson should be quick to get into and reachable in more than one way:

- **Orientation:** fill `objectives[]` and `estMinutes` — they render a "What
  you'll learn" card plus an auto-generated **"On this page"** jump menu, so a
  student can see the payoff and skip straight to the simulation or the quiz.
- **Narrate your slides.** Give each `lectureSlides[]` entry an `audio` clip so
  students can *listen* as well as read. Generate it with ElevenLabs (key in the
  podcast project's `.env`, `ELEVENLABS_API_KEY`) using the lab's narrator voice
  **Sarah** (`EXAVITQu4vr4xnSDxMaL`), model `eleven_multilingual_v2`, written
  from the slide's presenter notes; save the mp3 under
  `public/slides/<slug>/audio/`. (We do **not** clone Chris's voice.)
- **Render slides** from a deck with `pdftoppm -png -r 150 -f <page> -l <page>
  slides-clean.pdf out`.

## 5. Integrity rules (the build enforces these)

- **No AI-drawn structures, ever.** Use a real `rcsb`/`pubchem` id.
- **AI images need a human.** An image with `aiGenerated: true` **must** have a
  non-empty `factCheckedBy`, or the build fails. Non-AI images need a `credit`.
- **Every question needs an `answer` + `rationale`,** and the answer must point at a
  real choice, or the build fails.
- **Only allowed sources.** See [LICENSING.md](LICENSING.md). No Tymoczko textbook,
  no publisher figures, no real AAMC questions.

## 6. Check it, then open a PR

```bash
npm run build        # runs `astro check` + builds. MUST pass — this IS the gate.
```
If the build fails, read the message — it tells you exactly which field is wrong.
When it passes and `npm run dev` looks right, commit and open a pull request.

That's it. Copy the folder, fill the schema, write the prose, make the build pass.
