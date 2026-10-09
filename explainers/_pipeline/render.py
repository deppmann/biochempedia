#!/usr/bin/env python3
"""Render one Manim scene per script scene, mux with narration, concatenate to an mp4.

Usage:
    render.py --script script.json --scenes scenes.py --audio DIR --out out.mp4 [--quality l|m|h]

Scene id -> class name: the id converted to CamelCase ("s01_problem" -> "S01Problem": split on
_ and -, capitalize the first letter of each part); an exact-name match (class s01_problem) is
also accepted. A missing class, wav or duration fails before any rendering, naming the scene.
KX_DURATION is set per scene from DIR/durations.json; PYTHONPATH includes this directory so
scenes.py can `from kx_manim import NarratedScene`. Each scene video is padded (last frame held)
to the audio length, never the reverse. KX_SCRIPT / KX_SCENE_ID name the script and the scene (xm.XMScene uses them to time sentences).
Quality m = 720p30. Output: H.264 + AAC, yuv420p, +faststart.
"""
import argparse
import json
import os
import re
import shutil
import subprocess
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
MANIM = Path.home() / ".venvs/manim/bin/manim"
FFMPEG = shutil.which("ffmpeg") or "/Users/deppmann/miniconda3/bin/ffmpeg"
FFPROBE = shutil.which("ffprobe") or "/Users/deppmann/miniconda3/bin/ffprobe"
QUALITY = {"l": ("-ql", "480p15"), "m": ("-qm", "720p30"), "h": ("-qh", "1080p60")}


def camel(scene_id):
    return "".join(p[:1].upper() + p[1:] for p in re.split(r"[_\-\s]+", scene_id) if p)


def duration(path):
    r = subprocess.run([FFPROBE, "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", str(path)],
                       capture_output=True, text=True, check=True)
    return float(r.stdout.strip())


def run(cmd, **kw):
    r = subprocess.run(cmd, capture_output=True, text=True, **kw)
    if r.returncode:
        sys.exit(f"command failed: {' '.join(map(str, cmd[:3]))} ...\n{(r.stderr or r.stdout)[-1500:]}")
    return r


def main():
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("--script", required=True)
    ap.add_argument("--scenes", required=True)
    ap.add_argument("--audio", required=True)
    ap.add_argument("--out", required=True)
    ap.add_argument("--quality", choices=QUALITY, default="l")
    a = ap.parse_args()

    scenes_py, audio, out = Path(a.scenes).resolve(), Path(a.audio).resolve(), Path(a.out).resolve()
    ids = [s["id"] for s in json.loads(Path(a.script).read_text())["scenes"]]
    classes = set(re.findall(r"^class\s+(\w+)", scenes_py.read_text(), re.M))
    durs = json.loads((audio / "durations.json").read_text()) if (audio / "durations.json").exists() else {}

    problems, cls = [], {}
    for i in ids:
        cls[i] = next((c for c in (i, camel(i)) if c in classes), None)
        if not cls[i]:
            problems.append(f"{i}: no class {camel(i)!r} (or {i!r}) in {scenes_py.name}")
        if i not in durs or not (audio / f"{i}.wav").exists():
            problems.append(f"{i}: missing {i}.wav / durations.json entry in {audio}")
    if problems:
        sys.exit("cannot render:\n  " + "\n  ".join(problems))
    if not MANIM.exists():
        sys.exit(f"{MANIM} not found: run setup_video.sh first")

    flag, qdir = QUALITY[a.quality]
    work = out.parent / f".render-{out.stem}"
    work.mkdir(parents=True, exist_ok=True)
    parts = []
    for n, i in enumerate(ids, 1):
        print(f"[{n}/{len(ids)}] {i} -> {cls[i]} ({durs[i]:.1f}s narration)", flush=True)
        env = {**os.environ, "KX_DURATION": str(durs[i]), "KX_SCRIPT": str(Path(a.script).resolve()), "KX_SCENE_ID": i,
               "PYTHONPATH": os.pathsep.join(filter(None, [str(HERE), str(scenes_py.parent), os.environ.get("PYTHONPATH")]))}
        run([str(MANIM), flag, "--progress_bar", "none", "-v", "WARNING", "--media_dir", str(work / "media"),
             str(scenes_py), cls[i]], env=env)
        vid = work / "media/videos" / scenes_py.stem / qdir / f"{cls[i]}.mp4"
        if not vid.exists():
            sys.exit(f"{i}: manim finished but {vid} is missing")
        wav = audio / f"{i}.wav"
        v, au = duration(vid), duration(wav)
        total = max(v, au)
        seg = work / f"{i}.mp4"
        # Hold the last video frame up to the audio length; pad audio with silence up to the video length.
        run([FFMPEG, "-loglevel", "error", "-y", "-i", str(vid), "-i", str(wav), "-filter_complex",
             f"[0:v]tpad=stop_mode=clone:stop_duration={max(0.0, au - v) + 0.1:.3f},format=yuv420p[v];[1:a]apad[a]",
             "-map", "[v]", "-map", "[a]", "-t", f"{total:.3f}", "-c:v", "libx264", "-preset", "medium", "-crf", "18",
             "-c:a", "aac", "-b:a", "160k", "-ar", "48000", "-ac", "2", str(seg)])
        parts.append(seg)

    listing = work / "concat.txt"
    listing.write_text("".join(f"file '{p}'\n" for p in parts))
    out.parent.mkdir(parents=True, exist_ok=True)
    run([FFMPEG, "-loglevel", "error", "-y", "-f", "concat", "-safe", "0", "-i", str(listing),
         "-c", "copy", "-movflags", "+faststart", str(out)])
    print(f"done: {duration(out):.1f}s -> {out}")


if __name__ == "__main__":
    main()
