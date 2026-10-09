#!/bin/sh
cd "/Users/deppmann/mission-control/work/explainers/2026-10-08-biochempedia/$1" && PYTHONPATH="/Users/deppmann/mission-control/work/explainers/2026-10-08-biochempedia/_shared" python3 $HOME/.claude/skills/karpathy-explainer/scripts/render.py --script script.json --scenes scenes.py --audio audio --out hq.mp4 --quality h > hq.log 2>&1
echo "$1 exit=$? $(tail -1 hq.log)"
