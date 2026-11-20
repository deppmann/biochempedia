# Film timelines

What the theater on `/watch/` knows about a film, and where it comes from. No model is called here,
at build time or on a visit.

## What is worked out by rule, for every film

`lib.mjs` reads three things that are already in the repository:

| File | Gives |
|---|---|
| `explainers/<lesson>/[<film-id>/]script.json` | the film's scenes, in order (no times) |
| `public/explainers/<lesson>/<name>.vtt` | the captions: one timed cue per sentence |
| `src/content/lessons/<lesson>/lesson.mdx` | the lesson's headings, where each film is placed, its figures |

From them it derives:

- **Scene times.** A spoken scene starts at the caption cue that opens with its first words. A silent
  scene (title card, thinking pause, end card) starts where the scene before it stops speaking. The
  matching rules, and the caption quirks they handle, are in the comment on `sceneTimes()`.
- **The film's own questions.** A spoken scene followed by a thinking pause is a question; its answer
  starts with the next spoken scene. While the film waits, the theater shows the question and nothing
  else.
- **The part of the lesson the film goes with.** From the heading the film is placed under to the
  heading of the lesson's next film. The theater links that heading, and lists that stretch's figures
  in a fold that stays shut until the film has given its last answer.
- **A transcript that follows the film**, one line per sentence.

`node scripts/film-timelines/report.mjs` prints the coverage (`--list` names every film that is not
fully timed and why; `--json` gives everything).

## What needs a person: figures on cue

Which lesson figure belongs at which moment of a film is a judgement, and a wrong one can show the
answer to a question the film is about to ask. So a figure is tied to a moment only by a
**hand-checked map**, one file per film:

`src/data/film-maps/<lesson>/<name>.json` (`<name>` is the film's file name: `explainer`, or the film id)

```json
{
  "film": "diffusion-and-osmosis/chapter-2",
  "checked": { "by": "who checked it, and against what", "on": "2026-11-20", "note": "why each figure is where it is" },
  "parts": [
    { "from": "s00_title", "title": "Where did the water come from?" },
    { "from": "s03_tank", "title": "Same tank, salt held back", "section": "explain-water-crosses-a-choosy-membrane" },
    { "from": "s06_predict", "question": true },
    { "from": "s08_reveal", "title": "The answer, and why" },
    { "from": "s09_osmosis", "title": "Osmosis, named",
      "term": { "word": "Osmosis", "def": "drift of water across a selectively permeable membrane" },
      "figure": { "src": "/figures/diffusion-and-osmosis/membrane-water-salt-oxygen.webp", "answers": "s06_predict" } }
  ]
}
```

- `from`: a scene id from the film's `script.json`. A part runs from that scene to the next part.
- `title`: at most 60 characters. It names the topic and **never states an answer**: every title is
  visible in the list of parts before the film reaches it. ("The answer, and why", not the answer.)
- `question: true`: required on every scene the film pauses after. A question part carries nothing
  else; the theater prints the film's own words.
- `section`: a heading id on the lesson page.
- `term`: a word and its definition. The definition must be a run of words the film actually says;
  the word appears when the film says them.
- `figure.src`: one of the lesson's own figures. Its alt text, caption and key words are copied from
  the lesson at build time, never retyped (a `ScaffoldFigure`'s key words are left out, because the
  lesson asks the student to supply them).
- `figure.answers`: **required**. The id of the question scene whose answer the figure shows, or
  `null` if the checker judged that it shows none. A figure that answers a question cannot be placed
  before that question's reveal scene.

`node scripts/check-film-timelines.mjs` refuses a map that breaks any rule (CI runs it), and a map
with a problem is never used by the page: the film falls back to the plain theater.

### Filling the rest (a later, offline pass)

For each film: `node scripts/film-timelines/worksheet.mjs <lesson>/<name>` prints what a checker
needs on one screen: every scene with its start time, its narration and what is on screen, the
film's questions and where each answer starts, and the lesson's figures (file, caption, alt text,
the heading each sits under). A draft map can be proposed from that by any means; what makes it a
map is the check by a reader who has the film's script in front of them and answers, for each
figure, two questions:

1. Has the film, by the time this part starts, already said what this figure shows?
2. Does the figure show the answer to a question this film asks, or to one a later film of the same
   lesson asks? If a later film's, leave the figure out of this film.

Then: `node scripts/check-film-timelines.mjs`, and watch the page at the cue times
(`/watch/<lesson>/[<id>/]?t=<seconds>` puts the page in the state it has at that second).
