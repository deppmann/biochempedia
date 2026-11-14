#!/usr/bin/env python3
"""Regression suite for layout_check.py: every FAIL scene must report its defect, every PASS scene must not.

    ~/.venvs/manim/bin/python explainers/_pipeline/tests/layout/run_tests.py [-k Covered] [--jobs 4]

Each scene runs as Manim --dry_run (no video) with the check on, exactly as in a render. Exit status 0
when every expectation holds. Add a pair here whenever a frame checker finds a defect the check missed.
"""
import argparse
import json
import os
import subprocess
import sys
import tempfile
from pathlib import Path

HERE = Path(__file__).resolve().parent
PIPE = HERE.parents[1]
MANIM = Path.home() / ".venvs/manim/bin/manim"

# scene -> list of (kind, severity, in_motion) that MUST be reported (counted, not transient or suppressed).
# PASS scenes expect no counted errors and no counted warnings at all, plus any extra conditions below.
FAIL = {
    "FailCovered": [("covered", "error", False)],
    "FailStraddle": [("straddle", "error", False)],
    "FailArrowIntoChip": [("straddle", "error", False)],
    "FailChipChip": [("box_overlap", "error", False)],
    "FailOverflow": [("overflow", "error", False)],
    "FailEdge": [("edge", "error", False)],
    "FailShapeEdge": [("edge", "warning", False)],
    "FailSmall": [("small", "error", False)],
    "FailEndCard": [("small", "error", False)],
    "FailOutside": [("outside", "error", False)],
    "FailContrast": [("contrast", "warning", False)],
    "FailNear": [("near", "warning", False)],
    "FailTextOverlap": [("text_overlap", "error", False)],
    "FailCrossfade": [("text_overlap", "warning", True)],
    "FailMovingToken": [("covered", "warning", True)],
}
PASS = ["PassCovered", "PassInsideRing", "PassStraddle", "PassArrowIntoChip", "PassChipChip", "PassOverflow",
        "PassEdge", "PassShapeEdge", "PassSmall", "PassEndCard", "PassOutside", "PassContrast", "PassNear",
        "PassCrossfade", "PassMovingToken", "PassLayoutOk", "PassHiddenLetter", "PassBoxedLabel", "PassTiles"]
EXTRA = {"PassLayoutOk": lambda iss: any(i.get("suppressed") and i["kind"] == "covered" for i in iss) or
         "the opted-out crossing should still be listed as suppressed"}
# the EndCard draws the brand line at 22 pt and the mascot; it must still be clean when the LINE fits


def run(scene, work):
    out = work / f"{scene}.jsonl"
    env = {**os.environ, "KX_DURATION": "3.0", "KX_SCENE_ID": scene, "KX_LAYOUT_OUT": str(out),
           "PYTHONPATH": os.pathsep.join(filter(None, [str(PIPE), str(HERE), os.environ.get("PYTHONPATH")]))}
    cmd = [str(MANIM), "-ql", "--dry_run", "--progress_bar", "none", "-v", "ERROR",
           "--media_dir", str(work / f"media-{scene}"), str(HERE / "scenes.py"), scene]
    return scene, out, subprocess.Popen(cmd, env=env, cwd=work, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("-k", default="", help="only scenes whose name contains this")
    ap.add_argument("--jobs", type=int, default=4)
    ap.add_argument("-v", action="store_true", help="print every issue")
    a = ap.parse_args()
    names = [n for n in list(FAIL) + PASS if a.k in n]
    work = Path(tempfile.mkdtemp(prefix="layout-tests-"))
    results, running, todo = {}, [], list(names)
    while todo or running:
        while todo and len(running) < a.jobs:
            running.append(run(todo.pop(0), work))
        scene, out, p = running.pop(0)
        so, se = p.communicate()
        if p.returncode:
            results[scene] = None
            print(f"{scene}: manim failed\n{(se or so)[-800:]}")
            continue
        recs = [json.loads(l) for l in out.read_text().splitlines() if l.strip()] if out.exists() else []
        results[scene] = [i for r in recs for i in r["issues"]]
    bad = 0
    for n in names:
        iss = results.get(n)
        if iss is None:
            bad += 1
            continue
        counted = [i for i in iss if not i.get("transient") and not i.get("suppressed")]
        msgs = []
        if n in FAIL:
            for kind, sev, motion in FAIL[n]:
                if not any(i["kind"] == kind and i["severity"] == sev and bool(i.get("in_motion")) == motion for i in counted):
                    msgs.append(f"expected {sev} {kind}{' in motion' if motion else ''}")
        else:
            if counted:
                msgs.append("expected clean, got " + "; ".join(f"{i['severity']} {i['kind']}: {i['text']} / {i['with']}" for i in counted))
            chk = EXTRA.get(n)
            if chk:
                r = chk(iss)
                if r is not True:
                    msgs.append(r)
        status = "ok  " if not msgs else "FAIL"
        bad += bool(msgs)
        print(f"{status} {n}" + ("" if not msgs else ": " + " | ".join(msgs)))
        if a.v:
            for i in iss:
                print(f"       {i['severity']} {i['kind']} t={i['t_first']} dur={i.get('duration_s')} "
                      f"{'transient ' if i.get('transient') else ''}{'suppressed ' if i.get('suppressed') else ''}"
                      f"{i['text']!r} / {i['with']} -> {i.get('hint', '')}")
    print(f"{len(names) - bad}/{len(names)} passed")
    sys.exit(1 if bad else 0)


if __name__ == "__main__":
    main()
