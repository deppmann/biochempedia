#!/usr/bin/env python3
"""Offline self-test for make_web.py: caption guard and Hex-stamp corner check. No ffmpeg, no model.
    python3 explainers/_pipeline/tests/test_make_web.py
"""
import sys
from pathlib import Path
import numpy as np
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
import make_web as mw

SCENE = {"id": "s1", "narration": "RNA polymerase II transcribes messenger RNA from protein-coding genes. "
         "RNA polymerase III makes transfer RNAs and five S ribosomal RNA. "
         "MicroRNA precursors are made by polymerase two as well, in about 12 steps.",
         "tts": "RNA polymerase two transcribes messenger RNA from protein coding genes."}
EMPTY = {"id": "s2", "narration": ""}
fails = 0


def check(name, cue, scene, want):
    global fails
    got = bool(mw.keep_narrated([[0, 1, cue]], scene))
    ok = got == want
    fails += not ok
    print(f"{'ok  ' if ok else 'FAIL'} {name}: kept={got} (want {want})")


print("-- caption guard")
check("invented, words of the scene, wrong order (Polymerase II)",
      "Polymerase II makes transfer RNAs and microRNA precursors.", SCENE, False)
check("verbatim", "RNA polymerase II transcribes messenger RNA from protein-coding genes.", SCENE, True)
check("ASR spellings", "RNA polymerize two transcribes messenger RNA from protein coding genes", SCENE, True)
check("numeral for number word", "RNA polymerase 2 transcribes messenger RNA", SCENE, True)
check("numerals in the middle", "made by polymerase 2 as well, in about twelve steps.", SCENE, True)
check("hyphen vs space", "from protein coding genes.", SCENE, True)
check("partial real cue (first half)", "RNA polymerase III makes transfer RNAs", SCENE, True)
check("stock hallucination", "Thanks for watching, please visit www dot example dot org", SCENE, False)
check("empty-narration scene", "RNA polymerase II transcribes messenger RNA", EMPTY, False)

print("-- repeated cues")
L = "Mating pattern alone changes genotype frequencies, not allele frequencies."
sc = {"id": "s3", "narration": L + " Selection changes allele frequencies."}
r = mw.keep_narrated([[0, 3, L], [3, 6, L], [6, 8, "Selection changes allele frequencies."]], sc)
ok = len(r) == 2 and r[0][1] == 6
fails += not ok; print(f"{'ok  ' if ok else 'FAIL'} said once, emitted twice: merged ({len(r)} cues, first ends {r[0][1]})")
sc2 = {"id": "s4", "narration": "Again and again. Again and again."}
r = mw.keep_narrated([[0, 2, "Again and again."], [2, 4, "Again and again."]], sc2)
fails += len(r) != 2; print(f"{'ok  ' if len(r) == 2 else 'FAIL'} said twice, emitted twice: both kept")

print("-- corner occupancy")
H, W = 90, 160
bg = np.array(mw.BG_RGB, dtype=np.uint8)
blank = np.tile(bg, (H, W, 1))
x0, y0, x1, y1 = mw.stamp_rect(W, H)
chip = blank.copy(); chip[y0 + 2:y0 + 8, x0 + 3:x0 + 20] = (200, 200, 220)       # a legend chip in the corner
mid = blank.copy(); mid[40:60, 20:80] = (255, 255, 255)                          # content elsewhere
faint = blank.copy(); faint[y0:y1, x0:x1] += 6                                  # compression noise
occ = mw.corner_occupied(np.stack([blank, chip, mid, faint]))
print("occupied:", occ.tolist())
for got, want, n in zip(occ.tolist(), [False, True, False, False], ["blank", "chip", "content elsewhere", "faint noise"]):
    fails += got != want
    print(f"{'ok  ' if got == want else 'FAIL'} {n}")
# 2 fps, 40 s film, corner busy 2-22 s, end card at 38 s
o = np.zeros(80, bool); o[4:44] = True
r = mw.clear_ranges(o, 2, 38.0)
print("clear ranges:", r)
fails += not (r and r[-1][0] >= 22 and r[-1][1] <= 38 and all(b - a >= mw.MIN_CLEAR for a, b in r))
o2 = np.zeros(80, bool); o2[10:14] = True   # 2 s busy in the middle: two long ranges
print("mid-gap ranges:", mw.clear_ranges(o2, 2, 38.0))
o3 = np.zeros(80, bool); o3[10:12] = True; o3[14:16] = True  # clear gap of 1.5 s minus trims is too short to stamp
print("flicker gap ranges:", mw.clear_ranges(o3, 2, 38.0))
print("filter:", mw.stamp_filter(1080, 38.0, ranges=[(0.0, 1.75), (22.25, 37.0)])[-110:])
print("FAILURES:", fails)
sys.exit(1 if fails else 0)
