#!/bin/sh
# Re-voice one film with Kokoro (af_heart, local, free) and rebuild it. C. Deppmann 2026-10-31.
# Usage: sh rebuild_kokoro.sh SLUG   (run at most 5 at a time: Chris's render cap)
# Check the align.py output: Kokoro spells acronyms letter by letter and can drop a plural s,
# so a cue phrase in scenes.py may need the spoken form (fix_cues.py repairs most).
set -e
P=$(cd "$(dirname "$0")" && pwd)
cd "$P/../$1"
PYTHONPATH=$P python3 $P/build_audio.py --script script.json --out audio --engine kokoro
PYTHONPATH=$P ~/.venvs/stt/bin/python $P/align.py --dir .
python3 $P/fix_cues.py . || true
PYTHONPATH=$P python3 $P/render.py --script script.json --scenes scenes.py --audio audio --out hq.mp4 --quality h
~/.venvs/stt/bin/python $P/make_web.py --dir . --master hq
perl -0pi -e 's/narration: "an AI narrator voice \([^)]*\)/narration: "an AI narrator voice (Kokoro, af_heart)/' "$P/../../src/content/lessons/$1/lesson.mdx"
cp web/explainer.mp4 web/explainer.vtt web/poster.jpg "$P/../../public/explainers/$1/"
echo "rebuilt $1"
