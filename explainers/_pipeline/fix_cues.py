#!/usr/bin/env python3
"""Make every self.at("cue") in scenes.py match the transcript in audio/words.json (2026-10-27).

Usage: python3 fix_cues.py FILM_DIR [--dry]
Scene classes are matched to script.json scenes in order. A cue whose words are not spoken (after the
previous cue, as SpokenScene requires) is replaced by transcript words at the same point.

2026-10-31 (Kokoro): the scene's script text is aligned to its transcript first, so a cue is found in the
text it was written from and mapped across the alignment. A transcriber that writes "12G3P" for
"twelve G three P" no longer throws later cues off. The replacement is the shortest run of transcript
words, starting at the mapped point, whose first occurrence in the scene is that point (SpokenScene.t_of
takes the first occurrence).
"""
import difflib, json, re, sys
from pathlib import Path

d = Path(sys.argv[1]); dry = "--dry" in sys.argv
# Spoken number words and the digits a transcriber writes for them are the same token (Kokoro, 2026-10-31).
_NUM = {w: str(i) for i, w in enumerate("zero one two three four five six seven eight nine ten eleven twelve thirteen fourteen fifteen sixteen seventeen eighteen nineteen twenty".split())}
_NUM.update(thirty="30", forty="40", fifty="50", sixty="60", seventy="70", eighty="80", ninety="90", hundred="100", thousand="1000", million="1000000")
_n = lambda w: re.sub(r"[^a-z0-9']", "", w.lower())
norm = lambda w: _NUM.get(_n(w), _n(w))
scenes = json.load(open(d / "script.json"))["scenes"]
ids = [s["id"] for s in scenes]
text_of = {s["id"]: s.get("tts") or s.get("narration") or "" for s in scenes}
words = json.load(open(d / "audio" / "words.json"))
src = (d / "scenes.py").read_text()
camel = lambda i: "".join(p[:1].upper() + p[1:] for p in re.split(r"[_-]", i))
classes = list(re.finditer(r"^class (\w+)\(", src, re.M))
sid_of = {c: i for i in ids for c in (i, camel(i))}
out, changed = [], []
# Older films (the biochemistry BP class) time a cue by where it falls in the scene's narration text,
# not by the transcript: there a cue must be a substring of the narration.
narration_mode = "narr.find(phrase)" in src or "text.find(phrase)" in src
narr_of = {s["id"]: s.get("narration") or "" for s in scenes}


def find(seq, q, start):
    return next((i for i in range(start, len(seq) - len(q) + 1) if seq[i:i + len(q)] == q), None)


def find_loose(seq, q, start):
    """find(), or else a window whose letters run together match the cue's ("ATP" against tts "A T P")."""
    i = find(seq, q, start)
    if i is not None:
        return i
    target = "".join(q)
    for i in range(start, len(seq)):
        for n in range(1, len(q) + 4):
            if "".join(seq[i:i + n]) == target:
                return i
    return None


for k, m in enumerate(classes):
    end = classes[k + 1].start() if k + 1 < len(classes) else len(src)
    body = src[m.start():end]; sid = sid_of.get(m.group(1))
    if sid is None:
        out.append(body); continue
    if narration_mode:
        nw = narr_of.get(sid, "").split()
        wl = [(w, norm(w)) for w in nw if norm(w)]
    else:
        wl = [(p, norm(p)) for w in words.get(sid, []) for p in re.split(r"[\u2014\u2013]", w[2]) if norm(p)]
    H = [t for _, t in wl]
    T = [norm(w) for w in re.split(r"[\s\u2014\u2013]+", text_of.get(sid, "")) if norm(w)]
    t2h = {}   # script-token index -> transcript-token index
    for op, i1, i2, j1, j2 in difflib.SequenceMatcher(None, T, H, autojunk=False).get_opcodes():
        for k2 in range(i1, i2):
            t2h[k2] = j1 + (k2 - i1 if op == "equal" else (k2 - i1) * max(j2 - j1, 1) // max(i2 - i1, 1))
    state = {"hpos": 0, "tpos": 0}

    def nth_hit(seq, q, n):
        hits = [i for i in range(len(seq) - len(q) + 1) if seq[i:i + len(q)] == q]
        return hits[n] if len(hits) > n else None

    def repl(mm):
        phrase, rest = mm.group(2), mm.group(3)
        nth = int((re.search(r"nth\s*=\s*(\d+)", rest) or [0, 0])[1])
        rest = re.sub(r",\s*nth\s*=\s*\d+", "", rest)   # a replacement cue is chosen to be the first occurrence
        q = [norm(p) for p in re.split(r"[\s\u2014\u2013]+", phrase) if norm(p)]
        h = nth_hit(H, q, nth)
        if narration_mode and phrase not in narr_of.get(sid, ""):
            h = None
        if "room" in mm.group(1):   # a lookup (time until a cue): spoken anywhere is enough, and it sets no order
            if h is not None:
                return mm.group(0)
            t = find_loose(T, q, 0)
            if t is not None:
                h0 = t2h.get(t, 0)
                for n in range(1, 5):
                    for h in range(h0, min(h0 + 4, len(H) - n + 1)):
                        cand = H[h:h + n]
                        if find(H, cand, 0) == h and len("".join(cand)) >= 3:
                            new = " ".join(wl[j][0].strip(".,;:?!\"'") for j in range(h, h + n))
                            changed.append((sid, phrase, new, "aligned lookup"))
                            return f'{mm.group(1)}"{new}"{rest})'
            changed.append((sid, phrase, None, "lookup not spoken")); return mm.group(0)
        if h is not None and h >= state["hpos"]:   # spoken, and that occurrence comes after the previous cue
            state["hpos"] = h + 1
            t = find(T, q, state["tpos"]); state["tpos"] = t + 1 if t is not None else state["tpos"]
            return mm.group(0)
        t = find_loose(T, q, state["tpos"])
        if t is None:   # not even in the script text: fall back to the closest fuzzy window in the script
            best, t = 0, None
            for i in range(state["tpos"], max(state["tpos"], len(T) - len(q) + 1)):
                r = difflib.SequenceMatcher(None, " ".join(q), " ".join(T[i:i + len(q)])).ratio()
                if r > best: best, t = r, i
            if t is None or best < 0.5:
                changed.append((sid, phrase, None, round(best, 2))); return mm.group(0)
        state["tpos"] = t + 1
        h0 = max(t2h.get(t, state["hpos"]), state["hpos"])
        for n in range(1, 5):
            for h in range(h0, min(h0 + 4, len(H) - n + 1)):
                cand = H[h:h + n]
                if find(H, cand, 0) == h and len("".join(cand)) >= 3:
                    new = " ".join(wl[j][0].strip(".,;:?!\"'") for j in range(h, h + n))
                    state["hpos"] = h + 1; changed.append((sid, phrase, new, "aligned"))
                    return f'{mm.group(1)}"{new}"{rest})'
        changed.append((sid, phrase, None, "no unique window")); return mm.group(0)

    out.append(re.sub(r'(self\.(?:at|t_of|until|room)\()"([^"]+)"([^)]*)\)', repl, body))
for c in changed: print(*c, sep=" | ")
if not dry:
    (d / "scenes.py").write_text(src[:classes[0].start()] + "".join(out))
sys.exit(1 if any(c[2] is None for c in changed) else 0)
