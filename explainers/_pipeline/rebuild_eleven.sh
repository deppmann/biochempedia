#!/bin/sh
# Re-voice one film with ElevenLabs and rebuild it (2026-10-27 fact-check fixes).
# Usage: sh rebuild_eleven.sh SLUG   (run at most 5 at a time: Chris's render cap)
set -e
P=$(cd "$(dirname "$0")" && pwd)
cd "$P/../$1"
PYTHONPATH=$P python3 $P/build_audio.py --script script.json --out audio --engine eleven
PYTHONPATH=$P ~/.venvs/stt/bin/python $P/align.py --dir .
python3 $P/fix_cues.py . || true
PYTHONPATH=$P python3 $P/render.py --script script.json --scenes scenes.py --audio audio --out hq.mp4 --quality h
~/.venvs/stt/bin/python $P/make_web.py --dir . --master hq
sed -i "" "s/narration: \"an AI narrator voice (Gemini, Charon)/narration: \"an AI narrator voice (ElevenLabs, Sarah)/" "$P/../../src/content/lessons/$1/lesson.mdx"
cp web/explainer.mp4 web/explainer.vtt web/poster.jpg "$P/../../public/explainers/$1/"
echo "rebuilt $1"
