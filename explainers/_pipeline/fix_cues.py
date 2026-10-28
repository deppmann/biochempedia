#!/usr/bin/env python3
"""Make every self.at("cue") in scenes.py match the transcript in audio/words.json (2026-10-27).

Usage: python3 fix_cues.py FILM_DIR [--dry]
Scene classes are matched to script.json scenes in order. A cue whose words are not spoken (after the
previous cue, as SpokenScene requires) is replaced by the transcript words at the closest fuzzy match.
"""
import difflib, json, re, sys
from pathlib import Path

d = Path(sys.argv[1]); dry = "--dry" in sys.argv
norm = lambda w: re.sub(r"[^a-z0-9']", "", w.lower())
ids = [s["id"] for s in json.load(open(d / "script.json"))["scenes"]]
words = json.load(open(d / "audio" / "words.json"))
src = (d / "scenes.py").read_text()
camel = lambda i: "".join(p[:1].upper() + p[1:] for p in re.split(r"[_-]", i))
allc = list(re.finditer(r"^class (\w+)\(", src, re.M))
sid_of = {c: i for i in ids for c in (i, camel(i))}
classes = allc
out, last, changed = [], 0, []
for k, m in enumerate(classes):
    end = classes[k + 1].start() if k + 1 < len(classes) else len(src)
    body = src[m.start():end]; sid = sid_of.get(m.group(1))
    if sid is None:
        out.append(body); continue
    wl = [(w[2], norm(w[2])) for w in words.get(sid, []) if norm(w[2])]
    toks = [t for _, t in wl]; pos = 0

    def repl(mm):
        global pos
        phrase = mm.group(2); q = [norm(p) for p in phrase.split() if norm(p)]
        hits = [i for i in range(pos, len(toks) - len(q) + 1) if toks[i:i + len(q)] == q]
        if hits:
            pos = hits[0] + 1; return mm.group(0)
        best, bi = 0, None
        for n in range(max(1, len(q) - 1), len(q) + 2):
            for i in range(pos, len(toks) - n + 1):
                r = difflib.SequenceMatcher(None, " ".join(q), " ".join(toks[i:i + n])).ratio()
                if r > best: best, bi, bn = r, i, n
        if bi is None or best < 0.5:
            changed.append((sid, phrase, None, best)); return mm.group(0)
        new = " ".join(wl[j][0].strip(".,;:?!\"'") for j in range(bi, bi + bn))
        pos = bi + 1; changed.append((sid, phrase, new, round(best, 2)))
        return f'{mm.group(1)}"{new}"'
    out.append(re.sub(r'(self\.(?:at|t_of)\()"([^"]+)"', repl, body))
for c in changed: print(*c, sep=" | ")
if not dry:
    (d / "scenes.py").write_text(src[:classes[0].start()] + "".join(out))
sys.exit(1 if any(c[2] is None for c in changed) else 0)
