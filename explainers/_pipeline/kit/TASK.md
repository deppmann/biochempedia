# Animate one teaching film: "{film_title}"

This folder is one film for the lesson "{lesson_title}" on biochemistrypedia.com, a free biology course site. The narration is written, fact-checked and recorded. You write the animation: one file, `scenes.py`, in this folder. Run every command from this folder.

## What is here
- `script.json`: the narration. Each scene has `tts` (spoken) and a `visual` note saying what the animation must show. Scenes with `silent` are the title card, the thinking pause and the end card. **Do not change script.json.**
- `audio/`: the recorded narration, one wav per scene, `durations.json`, and `words.json` giving each scene's spoken words and their times. The transcript writes numbers as digits and may spell acronyms letter by letter.
- `BRIEF.md`: the house rules for these films. Read all of it.
{reference_line}
- `lesson_for_context.mdx`: the lesson the film belongs to. Context only; the numbers in the film come from here.
- `../_pipeline/`: the shared code. Read the docstrings of `bp_style.py` and `bp_parts.py` first, and `examples/components_demo/scenes.py` for how the parts are used. Do not change anything in `_pipeline/`.

## Write `scenes.py`
1. Start with a comment block: the COLOUR MAP for the whole film (one colour per concept), the one picture of the world the film carries from scene to scene, and for every spoken scene one line saying WHAT CHANGES on screen and what it is computed from. If a scene's line is "labels appear", redesign the scene. Then `from bp_parts import *`.
2. One class per scene in `script.json`, named after the scene id in CamelCase (`{example_id}` becomes `{example_class}`).
   - `{first_class}(TitleCard)` sets `LESSON = "{lesson_title}"` and `TITLE` = the `title` in script.json. Nothing else: the title card is standard.
   - Spoken scenes subclass `SpokenScene`. Time each beat with `self.at("phrase")`. Every phrase must appear, in order, in that scene's words in `audio/words.json`, compared in lower case without punctuation, with numbers as the transcript writes them. Its first occurrence in the scene must be the moment you mean. End each scene with `self.finish()`.
   - A `silent` pause scene in the middle holds the question just asked on screen for its whole duration: use `PredictPause` from `bp_parts.py`.
   - The last scene is `class {end_class}(EndCard): LINE = "..."` with no `construct` override. LINE is the take-home line in the last scene of script.json, word for word.
3. Build from the parts in `bp_parts.py` where one fits (`Plot`, `Readout`, `counter`, `dial`, `TwoPanel`, `Ledger`, `question_card`, `place_label`, `swap`, `caption`, `scope_tag`). Draw by hand only the lesson's own picture.
4. Show what each `visual` note says, in sync with the words: show before you tell; one new thing at a time; the subject itself moves; carry objects from scene to scene where the story continues (rebuild them in the same place); fill the frame with the main action. Draw nothing the narration does not say, and add no extra examples, runs or numbers of your own.
5. Keep everything inside the frame (x from -6.3 to 6.3, y from -3.5 to 3.5). Labels that name the subject are size 28 or larger (22 is the floor, for axis ticks only), in TEXT or a concept colour at full opacity, never grey. Real symbols: µm, ×, ÷, ². No molecular structures, no LaTeX. Every curve, dot and number on screen is computed in the code from the lesson's numbers, with fixed integer random seeds (`np.random.default_rng(7)`, never `hash()`); anything not computed is labelled "schematic".
6. A number and the marker that shows it must always agree: drive both from one `ValueTracker`. Never leave the frame black or empty while the narrator is speaking: do not fade a scene out before its narration ends.

## Render, check, look, fix
7. Render a draft and fix every error until it runs to the end (run it in the foreground and wait):

   `python3 ../_pipeline/render.py --script script.json --scenes scenes.py --audio audio --out draft.mp4 --quality l`

   The render prints a `layout check:` line and writes `layout_report.json`. Open it. Every issue under `"issues"` (text overlapping text, a line through a label, text at the frame edge, text too small) is a fault to fix, with the scene, the time and the exact text. Bring it to 0 issues. Set `obj.layout_ok = True` only for a thing that is truly meant to pass behind a label, and say so in `film_author.json`. To recheck layout without a full render:

   `python3 ../_pipeline/layout_check.py --script script.json --scenes scenes.py --audio audio`

8. Lint the draft (one JSON line):

   `PYTHONPATH=../_pipeline python3 ../_pipeline/film_lint.py draft.mp4`

   Aim for `frozen_pct` under 10, `longest_freeze_s` 6 or less, `ink_median_pct` 15 or more, and no flags. These numbers are a check on the film, not the goal. They must come from the subject itself: the simulation running, particles that ARE the thing being explained, a clock or gauge turning, a tracker moving along a curve, one shape growing into the next. **No decorative motion or filler**: no background dots, stars, motes, drifting texture, pulsing or wiggling that the narration does not call for. A film that reaches the numbers that way has failed. If you cannot reach a target honestly, leave it short and say so.
9. Extract one frame every 3 seconds and look at every one:

   `mkdir -p frames && {ffmpeg} -y -loglevel error -i draft.mp4 -vf fps=1/3,scale=960:-1 frames/f_%03d.png`

   For each frame, write one line in `frame_review.md`: the frame number, what is on screen, and every fault you see (or "clean"). Then fix the faults. Look for: text touching other text, a number or a shape; a label or value left over from an earlier beat; two values for one quantity; anything cut off; a black or nearly empty frame while the narrator speaks; a subject smaller than a third of the frame; a cue that lands late; a number that disagrees with its marker; anything the narration does not say. At most four render rounds.
10. Make a contact sheet for the reviewer:

   `{ffmpeg} -y -loglevel error -i draft.mp4 -vf "fps=1/4,scale=480:-1,tile=6x12" -frames:v 1 contact.png`

## Hand in
Edit only `scenes.py`, and create `draft.mp4`, `layout_report.json`, `frames/`, `frame_review.md`, `contact.png` and `film_author.json`:

`{"film": "{film_id}", "scenes": [ids], "rendered": true|false, "duration_s": ..., "lint": {the linter's JSON}, "layout_issues": <number left in layout_report.json>, "render_rounds": ..., "wall_minutes": ..., "model": "model and thinking level", "open_faults": [faults you did not fix], "notes": "anything the reviewer should look at"}`

End with one line: rendered or not, and the duration.
