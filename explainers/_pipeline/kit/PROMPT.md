You are animating {n_films} short narrated teaching film(s) for biochemistrypedia.com, a free biology course site. Each film has its own folder in this workspace:

{film_list}

The narration is already written, fact-checked and recorded. Your job is the animation code only: one file, `scenes.py`, in each folder.

These films teach by showing a process happen. A student should be able to follow the idea with the sound off: the thing the narrator describes is the thing that moves. A tidy diagram of labelled boxes that sits still while the narrator talks is a failed film, even if every label is correct.

Do the films one at a time, in the order listed. For each film:

1. Work inside that film's folder and run every command from there.
2. Read `TASK.md` and `BRIEF.md` in full and do exactly what they say. Read `script.json`, `audio/words.json`, the docstrings of `../_pipeline/bp_style.py` and `../_pipeline/bp_parts.py`, and `lesson_for_context.mdx` (the numbers come from it). If there is a `reference_old_scenes.py`, reuse its colour map and its model and plotting helpers, not its pacing or layout.
3. Write the plan comment block TASK.md asks for, then `scenes.py`. Render, and fix errors until the render runs to the end.
4. After every render: read `layout_report.json` and fix every issue in it; run the linter; extract the frames, open every PNG, and write `frame_review.md` with one line per frame. Then go through the frames a second time looking only for the faults listed below. Fix everything you logged and render again. At most four render rounds per film; use them.
5. Write `film_author.json` as TASK.md says.

What the picture must do:
- Every spoken scene has a subject that changes because of what the narrator is saying, and the change is computed: a random walk that actually walks, a concentration profile that actually falls off with depth, items actually drawn at random with a fixed seed, a counter or clock that actually runs. Do not stand in for a process with a flat filled shape, an empty box or a caption.
- The motion the linter measures must be that motion. No decorative or ambient movement of any kind: no background dots, stars, motes, drifting texture, shimmer, or pulsing that the narration does not call for. Anything of that kind is read by a student as a claim. If a scene comes out still, animate its subject, or hold a moving subject over from the previous beat.
- The subject fills most of the frame's height. Do not shrink the main action to make room for captions, and do not leave half the frame empty.
- Show only what the script says. Do not add extra examples, extra runs, extra draws or labels of your own, even helpful ones: every number on screen must be one the narration or the `visual` note gives, or one computed for exactly the case it describes.
- A number and its marker always agree. If a label says 0.60, the dot sits at 0.60 in the same frame. Drive both from one tracker.
- No black or empty frame while the narrator is speaking. Do not fade a scene out before its narration ends; the last picture of a scene holds until the next scene starts.
- Counters stop where the script says they stop.

Faults to hunt for on the second pass through the frames:
- any text touching or covering other text, a number, a tick label, a marker or a shape's outline;
- a label left over from an earlier beat, or two values for the same quantity on screen at once;
- a number that disagrees with the bar, dot or needle that shows it;
- anything cut off by the frame edge or within about 2% of it;
- a black frame, or a frame where the narrator is speaking and nothing on screen has changed since the frame before;
- a frame whose subject occupies less than about a third of the frame;
- grey or low-opacity text, or text smaller than its neighbours for no reason;
- a cue that lands after the narrator has finished saying the thing;
- anything on screen that the narration does not say, or that contradicts it.

Rules that override anything else:
- Edit only `scenes.py` in each film folder, plus the files TASK.md tells you to create. Never change `script.json`, anything in `audio/`, or anything in `_pipeline/`.
- Stay inside this workspace. Do not read other folders on this machine for example films.
- Use the commands exactly as TASK.md gives them, with the paths it gives. Do not install anything and do not create a virtual environment; the renderer finds its own animation tools.
- The linter and layout numbers are checks on the film, not the goal. Do not add anything whose purpose is to change a number, and do not mark things `layout_ok` to silence a real overlap. If you cannot reach a target honestly, leave it short and say so in `film_author.json`.
- Your own frame review has passed faulty frames before. When in doubt, log the fault.
- The last scene of each film is the standard end card and nothing else: `class SxxEnd(EndCard): LINE = "..."` with no `construct` override. LINE must be, word for word, the take-home line given in the last scene of `script.json`.
- No molecular structures. Every curve is computed from the lesson's numbers, never sketched; anything not computed is labelled "schematic".
- Run renders in the foreground and wait for each to finish. Never kill a process.
- If a step fails and you cannot fix it, stop and say exactly what failed. Do not skip a scene or leave a placeholder.

When all films are done, reply with a short table: film, rendered or not, duration in seconds, render rounds used, the three linter numbers (frozen %, longest still, median ink %), layout issues left, the number of faults logged and the number left open, and anything you think a reviewer should look at.
