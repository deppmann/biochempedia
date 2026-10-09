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

FFMPEG = "/Users/deppmann/miniconda3/bin/ffmpeg"
FFPROBE = "/Users/deppmann/miniconda3/bin/ffprobe"
SHARED = Path(__file__).resolve().parent
_model = None


def dur(p):
    return float(subprocess.run([FFPROBE, "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", str(p)],
                                capture_output=True, text=True, check=True).stdout)


def ff(args):
    r = subprocess.run([FFMPEG, "-loglevel", "error", "-y", *args], capture_output=True, text=True)
    if r.returncode:
        sys.exit("ffmpeg: " + r.stderr[:400])


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
    out = [list(w) for w in words]
    for op, i1, i2, j1, j2 in difflib.SequenceMatcher(None, a, b, autojunk=False).get_opcodes():
        if op == "equal":
            for k in range(i2 - i1):
                out[i1 + k][2] = nt[j1 + k]
        elif op == "replace" and (i2 - i1) == (j2 - j1) and (i2 - i1) <= 3:
            if difflib.SequenceMatcher(None, "".join(a[i1:i2]), "".join(b[j1:j2])).ratio() >= 0.6:
                for k in range(i2 - i1):
                    out[i1 + k][2] = nt[j1 + k]
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


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--dir", required=True)
    ap.add_argument("--master", default="hq")
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
            cues += cues_from(respell(words_for(d / "audio" / f"{s['id']}.wav"), s["narration"]), t0)
        t0 += L
    for i in range(len(cues) - 1):   # let each cue linger until the next starts, at most 0.8 s extra
        cues[i][1] = min(max(cues[i][1], cues[i][0] + 1.0), cues[i + 1][0], cues[i][1] + 0.8)
    web = d / "web"; web.mkdir(exist_ok=True)
    ff(["-i", str(master), "-vf", "fps=30,format=yuv420p", "-c:v", "libx264", "-preset", "slow", "-crf", "27",
        "-tune", "animation", "-c:a", "aac", "-b:a", "96k", "-ac", "1", "-movflags", "+faststart", str(web / "explainer.mp4")])
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
