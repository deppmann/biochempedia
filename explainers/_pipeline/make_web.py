#!/usr/bin/env python3
"""Package one rendered explainer for the website: web mp4, poster, and captions from the REAL speech.

    <fw-venv>/bin/python make_web.py --dir <video dir> [--master hq]

Captions: each scene's audio/<id>.wav is transcribed with faster-whisper (word timestamps, cached in
_shared/stt/wav-<sha>.json). Word spellings are taken from script.json's narration wherever the two
agree word-for-word or nearly so (fixes "km" → "Km", "Lavinthal" → "Levinthal"); where the narration
text differs from what was said, the transcript wins, so captions always match the audio.
Scene offsets come from the rendered segments in .render-<master>/<id>.mp4.
Writes <dir>/web/explainer.mp4 (1080p30, CRF 27, AAC 96k mono, faststart), poster.jpg, explainer.vtt.
"""
import argparse, difflib, hashlib, json, re, subprocess, sys
from pathlib import Path
import numpy as np

from fftools import FFMPEG, FFPROBE
SHARED = Path(__file__).resolve().parent
_model = None


def dur(p):
    return float(subprocess.run([FFPROBE, "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", str(p)],
                                capture_output=True, text=True, check=True).stdout)


def ff(args):
    r = subprocess.run([FFMPEG, "-loglevel", "error", "-y", *args], capture_output=True, text=True)
    if r.returncode:
        sys.exit("ffmpeg: " + r.stderr[:400])


STAMP = Path(__file__).resolve().parent / "kit" / "hex_stamp.png"


def height(p):
    return int(subprocess.run(["ffprobe", "-v", "error", "-select_streams", "v:0", "-show_entries", "stream=height",
                               "-of", "csv=p=0", str(p)], capture_output=True, text=True).stdout.strip() or 1080)


STAMP_FRAC, STAMP_MARGIN = 0.07, 0.028
BG_RGB = (0x0f, 0x11, 0x17)      # kx_manim.BG, the film background
OCCUPIED_AFTER = 1.0             # total seconds the corner may be occupied before the stamp is made conditional
MIN_CLEAR = 1.5                  # a stamped range must be at least this long (s), so the mark does not flicker


def stamp_rect(w, h, aspect=232 / 240):
    """Stamp rectangle (x0, y0, x1, y1) in pixels of a w x h frame, plus a small safety margin."""
    sh = max(2, round(h * STAMP_FRAC / 2) * 2)
    sw, m, pad = round(sh * aspect), round(h * STAMP_MARGIN), round(h * 0.012)
    return max(0, w - sw - m - pad), max(0, m - pad), w, min(h, m + sh + pad)


def corner_occupied(frames, bg=BG_RGB, tol=28, frac=0.004):
    """frames: uint8 array (N, H, W, 3) of downscaled frames. True per frame if anything is drawn in the
    stamp's rectangle: more than `frac` of its pixels differ from the background by over `tol` in any channel."""
    f = np.asarray(frames)
    x0, y0, x1, y1 = stamp_rect(f.shape[2], f.shape[1])
    reg = f[:, y0:y1, x0:x1, :].astype(int)
    diff = (np.abs(reg - np.array(bg)).max(axis=3) > tol).mean(axis=(1, 2))
    return diff > frac


def clear_ranges(occupied, fps, end_t, min_clear=MIN_CLEAR):
    """Time ranges [(a, b)] before end_t where the corner is clear, at least min_clear long. A sample covers
    [i/fps, (i+1)/fps); the range is trimmed 0.25 s each side of an occupied stretch."""
    rngs, start = [], None
    n = len(occupied)
    for i in range(n + 1):
        occ = i == n or bool(occupied[i])
        t = i / fps
        if not occ and start is None:
            start = t
        elif occ and start is not None:
            a, b = start + (0.25 if start > 0 else 0), min(t, end_t) - (0.25 if t < end_t and i < n else 0)
            if b - a >= min_clear:
                rngs.append((round(a, 2), round(b, 2)))
            start = None
    return rngs


def sample_corner(master, fps=2, width=320):
    """Downscaled frames of the master at `fps` per second, as uint8 (N, H, W, 3)."""
    wh = subprocess.run([FFPROBE, "-v", "error", "-select_streams", "v:0", "-show_entries", "stream=width,height",
                         "-of", "csv=p=0", str(master)], capture_output=True, text=True).stdout.strip().split(",")
    w0, h0 = int(wh[0]), int(wh[1])
    w, h = width, max(2, round(width * h0 / w0 / 2) * 2)
    raw = subprocess.run([FFMPEG, "-loglevel", "error", "-i", str(master), "-vf", f"fps={fps},scale={w}:{h}",
                          "-f", "rawvideo", "-pix_fmt", "rgb24", "-"], capture_output=True).stdout
    return np.frombuffer(raw, dtype=np.uint8)[: len(raw) // (w * h * 3) * w * h * 3].reshape(-1, h, w, 3)


def stamp_plan(master, end_t, fps=2):
    """None = stamp everywhere until end_t (corner free, or occupied for <= OCCUPIED_AFTER s in total);
    otherwise the list of clear (start, end) ranges in which to stamp. Prints what is skipped."""
    occ = corner_occupied(sample_corner(master, fps))
    occ_s = float(occ[: int(end_t * fps)].sum()) / fps
    if occ_s <= OCCUPIED_AFTER:
        return None
    rngs = clear_ranges(occ, fps, end_t)
    skipped, t = [], 0.0
    for a, b in rngs + [(end_t, end_t)]:
        if a - t > 0.05:
            skipped.append(f"{t:.1f}-{a:.1f}s")
        t = b
    print(f"  Hex stamp: corner occupied {occ_s:.1f} s; stamping only in {len(rngs)} clear ranges, skipping "
          + ", ".join(skipped))
    return rngs


def stamp_filter(h, end_t, frac=STAMP_FRAC, margin=STAMP_MARGIN, alpha=0.6, ranges=None):
    """The brand mark: a small Hex in the top right corner (the corner films use least), faded, on every
    frame until the end card starts (Hex is already on the end card), or only in `ranges` when the film
    draws in that corner."""
    sh, m = max(2, round(h * frac / 2) * 2), round(h * margin)
    en = f"lt(t,{end_t:.2f})" if ranges is None else "+".join(f"between(t,{a:.2f},{b:.2f})" for a, b in ranges)
    return (f"[1:v]scale=-2:{sh},format=rgba,colorchannelmixer=aa={alpha}[hx];"
            f"[0:v]fps=30[b];[b][hx]overlay=W-w-{m}:{m}:enable='{en}',format=yuv420p[v]")


def words_for(wav):
    h = hashlib.sha256(Path(wav).read_bytes()).hexdigest()[:16]
    cache = SHARED / "stt" / f"wav-{h}.json"
    if cache.exists():
        return json.loads(cache.read_text())
    global _model
    if _model is None:
        from faster_whisper import WhisperModel
        _model = WhisperModel("small.en", device="cpu", compute_type="int8")
    raw = subprocess.run([FFMPEG, "-loglevel", "error", "-i", str(wav), "-f", "f32le", "-ac", "1", "-ar", "16000", "-"],
                         capture_output=True).stdout
    segs, _ = _model.transcribe(np.frombuffer(raw, dtype=np.float32), word_timestamps=True, beam_size=5)
    w = [[round(x.start, 2), round(x.end, 2), x.word.strip()] for s in segs for x in s.words]
    cache.parent.mkdir(exist_ok=True)
    cache.write_text(json.dumps(w))
    return w


key = lambda t: re.sub(r"[^a-z0-9]", "", t.lower())


def respell(words, narration):
    """Replace whisper tokens with the narration's spelling where they line up."""
    nt = narration.split()
    a, b = [key(w[2]) for w in words], [key(t) for t in nt]
    out = []
    for op, i1, i2, j1, j2 in difflib.SequenceMatcher(None, a, b, autojunk=False).get_opcodes():
        if op == "equal":
            out += [[*words[i1 + k][:2], nt[j1 + k]] for k in range(i2 - i1)]
        elif op == "replace" and (i2 - i1) == (j2 - j1) and (i2 - i1) <= 3 and \
                difflib.SequenceMatcher(None, "".join(a[i1:i2]), "".join(b[j1:j2])).ratio() >= 0.6:
            out += [[*words[i1 + k][:2], nt[j1 + k]] for k in range(i2 - i1)]
        elif op == "replace" and (i2 - i1) <= 6 and (j2 - j1) <= 6:
            # Kokoro (2026-10-31) spells acronyms as letters and garbles some words ("FODU entrainment"
            # for "photoentrainment"): the narration is what was sent to the voice, so show its words,
            # spread over the time the transcript's words took.
            t0, t1 = words[i1][0], words[i2 - 1][1]
            lens = [len(t) + 1 for t in nt[j1:j2]]; tot = sum(lens); t = t0
            for tok, n in zip(nt[j1:j2], lens):
                out.append([round(t, 2), round(t + (t1 - t0) * n / tot, 2), tok]); t += (t1 - t0) * n / tot
        elif op in ("replace", "delete"):
            out += [list(w) for w in words[i1:i2]]
    return out


def ts(t):
    h, rem = divmod(max(t, 0), 3600)
    m, s = divmod(rem, 60)
    return f"{int(h):02d}:{int(m):02d}:{s:06.3f}"


def cues_from(words, offset, max_chars=84):
    cues, cur = [], []
    def flush():
        if cur:
            cues.append([offset + cur[0][0], offset + cur[-1][1], " ".join(w[2] for w in cur)])
            cur.clear()
    for w in words:
        if cur and len(" ".join(x[2] for x in cur)) + 1 + len(w[2]) > max_chars:
            flush()
        cur.append(w)
        text = " ".join(x[2] for x in cur)
        abbrev = re.fullmatch(r"([A-Z]|[a-z]\.[a-z]|e\.g|i\.e|vs|Dr|St|Mr|Mrs|etc|approx|Fig)\.", w[2])
        if re.search(r"[.!?][”\"')]*$", w[2]) and not abbrev and len(text) >= 18:
            flush()
    flush()
    return cues


_NUMW = {w: str(i) for i, w in enumerate("zero one two three four five six seven eight nine ten eleven twelve thirteen fourteen fifteen sixteen seventeen eighteen nineteen twenty".split())}


def toks(text):
    """Comparable word tokens: lower-case, hyphens and slashes split, number words and digits alike."""
    out = []
    for t in re.split(r"[\s\-/\u2013\u2014]+", text or ""):
        k = re.sub(r"[^a-z0-9]", "", t.lower())
        if k:
            out.append(_NUMW.get(k, k))
    return out


def _same(a, b):
    return a == b or (len(a) > 3 and len(b) > 3 and difflib.SequenceMatcher(None, a, b).ratio() >= 0.8)


def best_run(cue, narr):
    """Best in-order, near-contiguous alignment of the cue's words to a run of the narration's words.
    For each start in the narration, take the longest common subsequence (words equal up to small spelling
    differences) of the cue and a window of len(cue)+slack narration words; the window is what makes the
    run contiguous, the subsequence is what makes it ordered. Returns (matched/len(cue), start, end)."""
    n = len(cue)
    if not n or not narr:
        return 0.0, 0, 0
    win = n + 1 + n // 10
    best = (0.0, 0, 0)
    for j in range(len(narr)):
        if not any(_same(cue[0], narr[j + k]) for k in range(min(3, len(narr) - j))) and \
           not any(_same(c, narr[j]) for c in cue[:3]):
            continue
        w = narr[j:j + win]
        prev = [0] * (len(w) + 1)
        for c in cue:
            cur = [0]
            for k, x in enumerate(w):
                cur.append(prev[k] + 1 if _same(c, x) else max(prev[k + 1], cur[k]))
            prev = cur
        r = prev[-1] / n
        if r > best[0]:
            best = (r, j, min(len(narr), j + win))
    return best


MIN_RUN = 0.75  # share of a cue's words that must line up, in order, inside one narration run


def times_said(ws, narr):
    """How many times the word run `ws` occurs (spelling-tolerant, exact order) in the narration words."""
    n = len(ws)
    return sum(all(_same(a, b) for a, b in zip(ws, narr[j:j + n])) for j in range(len(narr) - n + 1)) if n else 0


def merge_repeats(cues, scene):
    """The recognizer sometimes emits one spoken line as two consecutive identical cues. A cue that repeats the
    previous cue's text is merged into it (the earlier cue stretches to the later one's end) unless the
    narration says that text at least twice. Returns the cues without the repeats."""
    narrs = [toks(scene.get(f)) for f in ("narration", "tts")]
    out = []
    for c in cues:
        ws = toks(c[2])
        if out and ws and ws == toks(out[-1][2]) and max(times_said(ws, nw) for nw in narrs) < 2:
            print(f"  merged repeated cue in {scene['id']} at {c[0]:.1f}s: {c[2]!r}")
            out[-1][1] = max(out[-1][1], c[1])
        else:
            out.append(c)
    return out


def keep_narrated(cues, scene):
    """Drop cues the narrator does not say. Speech recognition invents text ("please visit www .x .org",
    "thanks for watching", or a sentence rebuilt from words of the scene: "Polymerase II makes transfer RNAs
    and microRNA precursors") over silent stretches. A cue stays only if at least 75% of its words align,
    in order and within one run of the scene's narration (or tts), allowing spelling differences and
    numerals for number words. No narration, no cues. (Silence is not tested separately: recognizer
    timestamps cannot say reliably where the audio is quiet, and an invented cue has no run to align to.)"""
    narrs = [toks(scene.get(f)) for f in ("narration", "tts")]
    kept = []
    for c in cues:
        ws = toks(c[2])
        r = max((best_run(ws, nw)[0] for nw in narrs if nw), default=0.0)
        if ws and r >= MIN_RUN:
            kept.append(c)
        else:
            print(f"  dropped invented cue in {scene['id']} at {c[0]:.1f}s: {c[2]!r}")
    return merge_repeats(kept, scene)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--dir", required=True)
    ap.add_argument("--master", default="hq")
    ap.add_argument("--no-stamp", action="store_true", help="leave the Hex mark off the web film")
    a = ap.parse_args()
    d = Path(a.dir)
    script = json.loads((d / "script.json").read_text())
    segdir, master = d / f".render-{a.master}", d / f"{a.master}.mp4"
    if not master.exists():
        sys.exit(f"missing {master}")
    t0, cues, poster_t = 0.0, [], None
    for s in script["scenes"]:
        L = dur(segdir / f"{s['id']}.mp4")
        if s.get("narration"):
            if poster_t is None:
                poster_t = t0 + L * 0.55
            cues += keep_narrated(cues_from(respell(words_for(d / "audio" / f"{s['id']}.wav"), s["narration"]), t0), s)
        end_t = t0          # start of the last scene (the Hex end card), where the mark stops
        t0 += L
    for i in range(len(cues) - 1):   # let each cue linger until the next starts, at most 0.8 s extra
        cues[i][1] = min(max(cues[i][1], cues[i][0] + 1.0), cues[i + 1][0], cues[i][1] + 0.8)
    web = d / "web"; web.mkdir(exist_ok=True)
    enc = ["-c:v", "libx264", "-preset", "slow", "-crf", "27", "-tune", "animation", "-c:a", "aac", "-b:a", "96k",
           "-ac", "1", "-movflags", "+faststart", str(web / "explainer.mp4")]
    plan = None
    if not (a.no_stamp or not STAMP.exists()):
        plan = stamp_plan(master, end_t)
        if plan == []:
            print("  Hex stamp: corner never clear for long enough; no stamp")
    if a.no_stamp or not STAMP.exists() or plan == []:
        ff(["-i", str(master), "-vf", "fps=30,format=yuv420p"] + enc)
    else:
        ff(["-i", str(master), "-i", str(STAMP), "-filter_complex", stamp_filter(height(master), end_t, ranges=plan),
            "-map", "[v]", "-map", "0:a?"] + enc)
    ff(["-ss", f"{poster_t or 4:.2f}", "-i", str(master), "-frames:v", "1", "-vf", "scale=1280:-2", "-q:v", "3",
        str(web / "poster.jpg")])
    (web / "explainer.vtt").write_text("WEBVTT\n\n" + "\n".join(
        f"{i}\n{ts(x)} --> {ts(y)}\n{t}\n" for i, (x, y, t) in enumerate(cues, 1)))
    mb = (web / "explainer.mp4").stat().st_size / 1e6
    print(f"{d.name}: web mp4 {mb:.1f} MB, {dur(web / 'explainer.mp4'):.1f}s, {len(cues)} cues")
    if mb > 24:
        sys.exit("web mp4 over 24 MB (Cloudflare asset limit 25 MiB): raise CRF")


if __name__ == "__main__":
    main()
