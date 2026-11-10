#!/usr/bin/env python3
"""Zero-token film lint: measures a finished film from its mp4 and captions, no model in the loop.

    python3 film_lint.py FILM.mp4 [FILM.vtt]          -> one JSON line
Reports: duration; words per minute (from the captions); how much of the film is a frozen picture
(freezes of 5 s or more); the longest freeze; how much of the frame is drawn on ("ink", sampled every
2 s on a 160-px copy); and the share of sampled frames that are nearly empty (ink under 2.5%).
Words per minute is counted from the first spoken word to the last, pauses included: what a viewer
experiences. Freezes that are only the opening or closing card are not counted.
Flags (thresholds from the 2026-11 audits): FAST (over 135 wpm), STATIC (over 35% frozen or a freeze
over 12 s), THIN (median ink under 6%), EMPTY (over 15% of frames nearly empty), SHORT (under 150 s).
"""
import json, re, subprocess, sys
import numpy as np
FF, FP = "/Users/deppmann/miniconda3/bin/ffmpeg", "/Users/deppmann/miniconda3/bin/ffprobe"


def lint(mp4, vtt=None):
    D = float(subprocess.run([FP, "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", mp4], capture_output=True, text=True).stdout or 0)
    r = subprocess.run([FF, "-hide_banner", "-nostats", "-i", mp4, "-vf", "scale=320:-2,freezedetect=n=0.003:d=5", "-an", "-f", "null", "-"], capture_output=True, text=True).stderr
    fr = [float(x) for x in re.findall(r"freeze_duration: ([\d.]+)", r)]
    starts = [float(x) for x in re.findall(r"freeze_start: ([\d.]+)", r)]
    keep = [(a, b) for a, b in zip(starts, fr) if a > 1.0 and a + b < D - 1.0]   # not the title or end card
    starts, fr = [a for a, _ in keep], [b for _, b in keep]
    W, H = 160, 90
    probe = subprocess.run([FP, "-v", "error", "-select_streams", "v:0", "-show_entries", "stream=width,height", "-of", "csv=p=0", mp4], capture_output=True, text=True).stdout.strip().split(",")
    if len(probe) == 2 and int(probe[1]) > int(probe[0]): W, H = 90, 160
    raw = subprocess.run([FF, "-loglevel", "error", "-i", mp4, "-vf", f"fps=1/2,scale={W}:{H},format=gray", "-f", "rawvideo", "-"], capture_output=True).stdout
    f = np.frombuffer(raw, dtype=np.uint8)[: len(raw) // (W * H) * W * H].reshape(-1, H, W).astype(int)
    ink = [float((np.abs(x - np.median(x)) > 18).mean()) for x in f] or [0]
    words, speech, first, last = 0, 0.0, None, 0.0
    if vtt:
        txt = open(vtt).read()
        for a, b, body in re.findall(r"(\d+:\d+:[\d.]+) --> (\d+:\d+:[\d.]+)\n(.+)", txt):
            s = lambda z: sum(float(p) * 60 ** i for i, p in enumerate(reversed(z.split(":"))))
            words += len(body.split()); speech += s(b) - s(a)
            first = s(a) if first is None else first; last = s(b)
    out = dict(duration_s=round(D), wpm=round(words / (last - first) * 60) if first is not None and last > first else None, wpm_overall=round(words / D * 60) if D and words else None,
               frozen_pct=round(100 * sum(fr) / D) if D else 0, longest_freeze_s=round(max(fr or [0])),
               ink_median_pct=round(100 * float(np.median(ink)), 1), empty_pct=round(100 * float(np.mean([i < 0.025 for i in ink]))))
    out["freezes"] = sorted(([round(a), round(b)] for a, b in zip(starts, fr) if b >= 8), key=lambda z: -z[1])[:8]   # [start s, length s], longest first
    fl = []
    if out["wpm"] and out["wpm"] > 135: fl.append("FAST")
    if out["frozen_pct"] > 35 or out["longest_freeze_s"] > 12: fl.append("STATIC")
    if out["ink_median_pct"] < 6: fl.append("THIN")
    if out["empty_pct"] > 15: fl.append("EMPTY")
    if D < 150: fl.append("SHORT")
    out["flags"] = " ".join(fl)
    return out


if __name__ == "__main__":
    print(json.dumps({"film": sys.argv[1], **lint(*sys.argv[1:3])}))
