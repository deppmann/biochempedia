#!/usr/bin/env python3
"""Build the narration track for one Biochemistrypedia explainer from the lesson's OWN slide audio.

    build_audio.py --script script.json --out audio/ [--dry-run]

script.json:
  {"lesson": "<slug>", "title": "...", "scenes": [
     {"id": "s00_title", "silent": 3.0},
     {"id": "s01_xxx", "clip": "/slides/<slug>/audio/<name>.mp3", "visual": "..."},   # one slide clip per scene
     {"id": "s02_xxx", "tts": "Text to speak", "visual": "..."},                       # vitalism only (no slide audio)
     {"id": "s09_end", "silent": 3.5}]}

For a "clip" scene the narration text is pulled from that slide's `notes` in the lesson.mdx (the
clip was generated from those notes), written back into script.json as "narration", and used for
captions. "tts" scenes are spoken with ElevenLabs Sarah (EXAVITQu4vr4xnSDxMaL, eleven_multilingual_v2),
the site's narrator voice per CONTRIBUTING.md; cached by text hash; --dry-run prints characters only.
Writes audio/<id>.wav (48 kHz mono) and audio/durations.json.
"""
import argparse, hashlib, json, re, subprocess, sys, urllib.request, wave
from pathlib import Path

import yaml

REPO = Path.home() / "biochempedia"
FFMPEG = "/Users/deppmann/miniconda3/bin/ffmpeg"
SARAH = "EXAVITQu4vr4xnSDxMaL"
TTS_CHAR_CAP = 4000   # hard cap per video on ElevenLabs characters


def ff(args, data=None):
    r = subprocess.run([FFMPEG, "-loglevel", "error", "-y", *args], input=data, capture_output=True)
    if r.returncode:
        sys.exit("ffmpeg: " + r.stderr.decode(errors="replace")[:400])


def secs(p):
    with wave.open(str(p)) as w:
        return w.getnframes() / w.getframerate()


def lesson_notes(slug):
    text = (REPO / f"src/content/lessons/{slug}/lesson.mdx").read_text()
    fm = yaml.safe_load(text.split("\n---", 1)[0].lstrip("-\n"))
    return {s["audio"]: s for s in fm.get("lectureSlides", []) if s.get("audio")}


def speakable(t):
    t = re.sub(r"\*\*?([^*]+)\*\*?", r"\1", t or "")
    return re.sub(r"\s+", " ", t).strip()


def key():
    t = (Path.home() / ".zshrc").read_text()
    m = re.search(r"^\s*(?:export\s+)?ELEVENLABS_API_KEY=(?:\"([^\"]*)\"|'([^']*)'|(\S+))", t, re.M)
    return next(g for g in m.groups() if g)


def eleven(text, out_wav):
    body = {"text": text, "model_id": "eleven_multilingual_v2",
            "voice_settings": {"stability": 0.5, "similarity_boost": 0.75}}
    req = urllib.request.Request(f"https://api.elevenlabs.io/v1/text-to-speech/{SARAH}",
                                 json.dumps(body).encode(),
                                 {"xi-api-key": key(), "Content-Type": "application/json", "Accept": "audio/mpeg"},
                                 method="POST")
    mp3 = urllib.request.urlopen(req, timeout=120).read()
    ff(["-f", "mp3", "-i", "pipe:0", "-ar", "48000", "-ac", "1", str(out_wav)], mp3)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--script", required=True)
    ap.add_argument("--out", required=True)
    ap.add_argument("--dry-run", action="store_true")
    a = ap.parse_args()
    sp = Path(a.script)
    script = json.loads(sp.read_text())
    out = Path(a.out); out.mkdir(parents=True, exist_ok=True)
    notes = lesson_notes(script["lesson"])
    tts_chars = sum(len(s["tts"]) for s in script["scenes"] if s.get("tts"))
    print(f"ElevenLabs characters this video: {tts_chars} (cap {TTS_CHAR_CAP})")
    if tts_chars > TTS_CHAR_CAP:
        sys.exit("over the ElevenLabs cap; shorten the tts text")
    if a.dry_run:
        return
    durs, problems = {}, []
    for s in script["scenes"]:
        w = out / f"{s['id']}.wav"
        if "silent" in s:
            ff(["-f", "lavfi", "-i", "anullsrc=r=48000:cl=mono", "-t", str(s["silent"]), str(w)])
            s["narration"] = ""
        elif "clip" in s:
            slide = notes.get(s["clip"])
            if not slide:
                problems.append(f"{s['id']}: {s['clip']} is not a narrated slide in {script['lesson']}")
                continue
            ff(["-i", str(REPO / "public" / s["clip"].lstrip("/")), "-ar", "48000", "-ac", "1", str(w)])
            s["narration"] = speakable(slide.get("notes"))
            s["slideTitle"] = slide.get("title", "")
        elif "tts" in s:
            cache = out / ".tts" / (hashlib.sha256(s["tts"].encode()).hexdigest()[:16] + ".wav")
            cache.parent.mkdir(exist_ok=True)
            if not cache.exists():
                eleven(s["tts"], cache)
            ff(["-i", str(cache), str(w)])
            s["narration"] = speakable(s["tts"])
        else:
            problems.append(f"{s['id']}: needs one of silent / clip / tts")
            continue
        durs[s["id"]] = round(secs(w), 3)
    if problems:
        sys.exit("\n".join(problems))
    (out / "durations.json").write_text(json.dumps(durs, indent=1))
    sp.write_text(json.dumps(script, indent=1, ensure_ascii=False))
    print(f"{len(durs)} scenes, {sum(durs.values()):.1f}s total narration+cards")


if __name__ == "__main__":
    main()
