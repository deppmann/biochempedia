#!/usr/bin/env python3
"""Re-sync a profile film's narration to the profile story in its lesson (2026-10-31).

Usage: python3 sync_profile_story.py FILM_DIR [--write]
A profile film (explainers/bio-<lesson>-<name>/) reads the profile's story verbatim. When the story is
edited, each spoken scene's tts and narration are replaced by the stretch of the new story that lines
up with it (word alignment). Prints each changed scene; --write saves script.json.
"""
import difflib, json, re, sys
from pathlib import Path
import yaml

d = Path(sys.argv[1]).resolve(); write = "--write" in sys.argv
sc = json.load(open(d / "script.json"))
lesson = d.parent.parent / "src/content/lessons" / sc["lesson"] / "lesson.mdx"
fm = yaml.safe_load(lesson.read_text().split("---")[1])
stem = d.name[len("bio-"):]
sci = next(s for s in fm.get("scientists", []) if (s.get("film") or {}).get("src", "").endswith(f"/{stem}.mp4"))
story = " ".join(sci["story"].split())
spoken = [s for s in sc["scenes"] if s.get("tts")]
old = [w for s in spoken for w in s["tts"].split()]
new = story.split()
owner = [k for k, s in enumerate(spoken) for _ in s["tts"].split()]
norm = lambda w: re.sub(r"[^a-z0-9]", "", w.lower())
o2n = {}
for op, i1, i2, j1, j2 in difflib.SequenceMatcher(None, [norm(w) for w in old], [norm(w) for w in new], autojunk=False).get_opcodes():
    for i in range(i1, i2):
        o2n[i] = j1 + (i - i1 if op == "equal" else (i - i1) * (j2 - j1) // max(i2 - i1, 1))
starts = [next(i for i, k in enumerate(owner) if k == n) for n in range(len(spoken))]
cuts = [0] + [o2n[i] for i in starts[1:]] + [len(new)]
# Snap each cut to the nearest sentence end in the new story (within 12 words), so no scene starts mid-sentence.
ends = {j + 1 for j, w in enumerate(new) if re.search(r"[.?!:]['\"\u201d\u2019)]*$", w)}
for n in range(1, len(cuts) - 1):
    near = [e for e in ends if abs(e - cuts[n]) <= 12 and cuts[n - 1] < e < cuts[n + 1]]
    if near:
        cuts[n] = min(near, key=lambda e: abs(e - cuts[n]))
changed = 0
for n, s in enumerate(spoken):
    text = " ".join(new[cuts[n]:cuts[n + 1]])
    if text != s["tts"]:
        changed += 1
        print(f"== {s['id']}\n- {s['tts']}\n+ {text}\n")
        s["tts"] = text; s["narration"] = text
if write and changed:
    (d / "script.json").write_text(json.dumps(sc, indent=1, ensure_ascii=False) + "\n")
print(f"{d.name}: {changed} scene(s) changed{' (written)' if write and changed else ''}")
