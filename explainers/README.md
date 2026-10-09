# Animated explainers

Source for the narrated explainer videos at the top of the first ten lessons
(`public/explainers/<slug>/`, wired in through each lesson's `explainer:` frontmatter;
policy in [`IMAGE_POLICY.md`](../IMAGE_POLICY.md) rule 7).

Each `<slug>/` holds `script.json` (scenes, the slide clip or narration each one uses, and the
spoken text) and `scenes.py` (one Manim scene per narration clip). `_pipeline/` holds the shared
look (`bp_style.py`), the narration builder, and the packaging step.

Rebuild one video (Manim CE in `~/.venvs/manim`, no LaTeX; faster-whisper for captions):

```bash
cd explainers/<slug>
PYTHONPATH=../_pipeline python3 ../_pipeline/build_audio.py --script script.json --out audio   # skip for amino-acids, protein-3d-structure, enzyme-kinetics: their script.json narration is the transcript of the audio and build_audio would overwrite it with the slide notes
PYTHONPATH=../_pipeline python3 ../_pipeline/render.py --script script.json --scenes scenes.py --audio audio --out hq.mp4 --quality h
python3 ../_pipeline/make_web.py --dir . --master hq   # web mp4, poster, captions from the real speech
```

The narration is each lesson's existing slide audio. Those clips were generated from a longer
script than the presenter notes now shown under the slides, so the captions come from a
transcript of the audio, never from the notes. Captions were proofread by hand after transcription.
