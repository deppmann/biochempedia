# Film brief

House rules for animating a levelled-up teaching film. The script and narration are final; you write `scenes.py`. The commands are in `TASK.md`. Where a rule below is about writing the script (sentence length, pace, pauses, the hook), it is already done: animate what the script says.

## What is wrong with the films we have (measured, `film_lint.py`, 2026-11-09)
- **The voice races.** Kokoro at speed 1.0 speaks about 170 words a minute while it is speaking.
- **The picture sits still.** In a typical film 55-60% of the running time is a frozen frame.
- **The frame is mostly empty.** Small chips and thin grey labels float in a dark frame.
- **Scenes are lists.** Labels fade in one by one; nothing turns into anything.
- **No hook, no return.** Films open on a title card and close on a restatement.

## The ten rules
1. **Hook first.** The first 5 seconds are a picture and a question a stranger would want answered.
   The title card comes after the hook, or lasts at most 2 seconds.
2. **One guiding idea.** One sentence, said once in full near the middle, and returned to in the last
   scene in different words. Everything in the film serves it; cut what does not.
3. **Slow the voice, not the film.** Put `"pace": {"speed": 0.9, "gap": 0.35}` at the top of
   script.json (build_audio.py slows Kokoro and adds a breath after each sentence). Write sentences
   of 18 words or fewer. A scene is 8-20 seconds of speech and makes one point.
4. **Show, then tell.** The thing appears and settles before the narrator names it.
5. **Something always moves.** No frame frozen for more than 4 seconds, except a deliberate thinking
   pause. Use slow ambient motion (drifting particles, a rising gauge, shimmering water) driven by
   updaters, and make every change a transformation of what is already there.
6. **One world, carried.** Pick one picture of the world for the film (for example a cross-section of
   sky, sea and seabed with an oxygen gauge and a time scrubber) and change IT through the film.
   Do not cut to a new layout of chips for each scene. Rebuild carried objects in the same place.
7. **Fill the frame, raise the contrast.** The subject fills at least 60% of the frame height.
   Labels are size 28 or larger (34 or larger in a vertical cut), at most 5 words, in TEXT or a
   concept colour at full opacity. No grey-on-dark captions. At most 6 things on screen.
8. **Honest pictures.** Every graph, gauge or timeline is computed or marked "schematic". Keep every
   hedge the lesson keeps ("may", "debated", "about"). If it is on screen, it is a claim.
   Never draw a molecular structure.
9. **Two predict pauses at most** in a web film: a question card, then 4-5 seconds of near-silence
   with the question still on screen. None in a social cut.
10. **End on the idea.** The end card is the take-home sentence (12 words or fewer), never the title.

## Length
A web film is 3 to 4.5 minutes, 16:9. The length is set by the narration.

## Animation rules for `scenes.py`
- `from bp_style import *` and follow every rule in its docstring. The ones that matter most:
  **never draw a molecular structure** (no rings, bonds, atoms or ribbon shapes: use labelled
  chips, simple blobs, membranes as bars, arrows, timelines, and plots computed from equations);
  one colour per concept for the whole film, listed in a COLOR MAP comment at the top; everything
  inside the safe frame; nothing overlapping; text at `size` 22 or more; no subtitles drawn in.
- One class per scene id, named in CamelCase (`s03_cut` is `S03Cut`). `S00Title(TitleCard)` sets
  `LESSON` (the lesson's title) and `TITLE` (the film's title). `S07End(EndCard)` sets `LINE`
  (the rule to keep, 12 words or fewer, taken from the narration).
- Narrated scenes subclass `SpokenScene`. Cue every change with `self.at("two to four words the
  narrator says in this scene")`. The phrase must be in that scene's `tts` text, in order. Use
  plain words for cues: not numbers, symbols or names a speech-to-text program could spell another
  way, because the final narration is timed from a transcript. End each scene with `self.finish()`.
- Make it move. Things should appear when they are named, transform into what they become, and
  hold still while the sentence lands. A scene that is a list of labels fading in has failed.
  Carry objects from one scene to the next where the story continues (rebuild them in the same
  place at the start of the next scene).
- No LaTeX. Text only (`T`, `M`, `chip`).

What the pilot films taught (two authors made the same film; these are the differences that mattered):
- **Draw the idea as a shape that acts.** The better film drew the reading domain as a small cup
  that closes on a phosphate badge, so "the same domain is used twice" was something you could
  see: one grip on the receptor, then two grips between the partners. A chip with a name on it
  cannot do that. Find the one part in your film whose action is the point, and give it a shape.
- **Show the puzzle, do not state it.** Question-mark boxes for the unknown path, a crossed-out
  "new protein" box for the drug: the opening scene should pose the question in the picture.
- **Use the frame.** The main action must fill most of the frame's height in every scene where it
  is the subject. Do not keep a fixed stage (membrane at the top, nucleus at the bottom) for the
  whole film if most scenes use only the middle of it. Zoom the layout to where the action is,
  and bring the rest back when it is needed.
- **Stay on the one idea.** Do not add a closing scene on how the pathway is switched off, or on
  disease, unless that is the idea of the film.
- **Draw nothing the narration does not say.** One pilot greyed out a gene when a protein left
  it, which the lesson never states. If it is on screen, it is a claim.
- **Clear the old answer before showing a new question.** When a scene steps through cases
  ("with no A", "with no B"), reset every result on screen to a neutral state in the same
  animation that brings in the new case label, and reveal the new result only on the narrator's
  words. One pilot left the previous case's green "ON" lamp under the next case's label for two
  seconds, which showed the opposite of the lesson. Check each such change at four frames a second.
- **Count what you draw.** If the narration says "one protein" and two copies are on screen,
  label it so that the count is not contradicted ("one protein: STAT").

