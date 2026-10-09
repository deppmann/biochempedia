#!/usr/bin/env python3
"""After build_audio.py: transcribe every scene's audio/<id>.wav (faster-whisper small.en, word timestamps)
into audio/words.json {scene_id: [[start, end, word], ...]}.
For "clip" scenes, script.json "narration" becomes the TRANSCRIPT (what is actually said; the slide notes
are often a different, shorter text) and the notes move to "notes". Fix transcription misspellings in
"narration" by hand afterwards (Km, kcat, names); captions take their spelling from it.
For "tts" scenes, "narration" stays the exact tts text.
Run with the faster-whisper venv:  <fw>/bin/python align.py --dir <video dir>
"""
import argparse, json, subprocess
from pathlib import Path
import numpy as np
from faster_whisper import WhisperModel

ap = argparse.ArgumentParser(); ap.add_argument("--dir", required=True); a = ap.parse_args()
d = Path(a.dir); sp = d / "script.json"; script = json.loads(sp.read_text())
m = WhisperModel("small.en", device="cpu", compute_type="int8")
out = {}
for s in script["scenes"]:
    if s.get("silent") is not None:
        out[s["id"]] = []; continue
    raw = subprocess.run(["/Users/deppmann/miniconda3/bin/ffmpeg", "-loglevel", "error", "-i", str(d / "audio" / f"{s['id']}.wav"),
                          "-f", "f32le", "-ac", "1", "-ar", "16000", "-"], capture_output=True).stdout
    segs, _ = m.transcribe(np.frombuffer(raw, dtype=np.float32), word_timestamps=True, beam_size=5)
    words = [[round(w.start, 2), round(w.end, 2), w.word.strip()] for sg in segs for w in sg.words]
    out[s["id"]] = words
    if "clip" in s:
        if "notes" not in s:
            s["notes"] = s.get("narration", "")
        s["narration"] = " ".join(w[2] for w in words)
(d / "audio" / "words.json").write_text(json.dumps(out))
sp.write_text(json.dumps(script, indent=1, ensure_ascii=False))
print(f"aligned {len(out)} scenes -> {d/'audio'/'words.json'}")
