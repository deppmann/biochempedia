#!/usr/bin/env python3
"""Kokoro-82M (voice af_heart) worker for scripts/listen-render.mjs.

Loads the model once, then reads jobs from stdin, one JSON object per line:
    {"text": "...", "out": "/abs/path/clip.wav"}
For each job it writes a 24 kHz mono 16-bit WAV to "out" and prints one line to stdout:
    {"out": "...", "seconds": 12.3}            on success
    {"out": "...", "error": "message"}          on failure
It exits when stdin closes. Same call as ~/expedition-v2/scripts/kokoro_tts.py
(text -> PCM16), kept in this repo so the render does not depend on another project.
Run with ~/.venvs/kokoro/bin/python.
"""
import json
import sys
import wave

import numpy as np
from kokoro import KPipeline

RATE = 24000
pipe = KPipeline(lang_code="a", repo_id="hexgrad/Kokoro-82M")
print(json.dumps({"ready": True}), flush=True)

for line in sys.stdin:
    line = line.strip()
    if not line:
        continue
    job = json.loads(line)
    try:
        chunks = [audio for _, _, audio in pipe(job["text"], voice="af_heart", speed=1.0)]
        pcm = np.concatenate([np.asarray(c, dtype=np.float32) for c in chunks]) if chunks else np.zeros(1, np.float32)
        data = (np.clip(pcm, -1, 1) * 32767).astype("<i2").tobytes()
        with wave.open(job["out"], "wb") as w:
            w.setnchannels(1)
            w.setsampwidth(2)
            w.setframerate(RATE)
            w.writeframes(data)
        print(json.dumps({"out": job["out"], "seconds": round(len(pcm) / RATE, 2)}), flush=True)
    except Exception as e:  # report and keep going; the render script retries on its next run
        print(json.dumps({"out": job.get("out"), "error": str(e)[:300]}), flush=True)
