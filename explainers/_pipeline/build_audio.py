#!/usr/bin/env python3
"""Build the narration track for one Biochemistrypedia explainer from the lesson's OWN slide audio.

    build_audio.py --script script.json --out audio/ [--dry-run] [--engine eleven|gemini|say]

--engine gemini speaks "tts" scenes with Gemini text-to-speech (gemini-3.1-flash-tts-preview, voice
Charon; about 17 cents for a three-minute film). The Cell Signaling films use it (C. Deppmann,
2026-10-10: it is cheaper). The biochemistry films use the default, ElevenLabs Sarah. Never switch
to gemini-3.8-flash-tts: it reads the style line aloud.

--engine say speaks "tts" scenes with the free macOS voice, for drafts: scenes cue on spoken
phrases, so a video drafted this way re-times itself when the real narration replaces it
(re-run build_audio.py without the flag, then align.py). Draft audio has its own cache.

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
import argparse, base64, hashlib, json, re, subprocess, sys, time, urllib.error, urllib.request, wave
from pathlib import Path

import yaml

REPO = Path(__file__).resolve().parents[2]   # this checkout (was ~/biochempedia, which breaks in worktrees)
FFMPEG = "/Users/deppmann/miniconda3/bin/ffmpeg"
SARAH = "EXAVITQu4vr4xnSDxMaL"
TTS_CHAR_CAP = 4000   # hard cap per video on paid narration characters
GEMINI_MODEL = "gemini-3.1-flash-tts-preview"   # not 3.8: it reads the style line aloud
GEMINI_VOICE = "Charon"
GEMINI_STYLE = ("Read this aloud in a clear, calm, even voice at a moderate pace, "
                "as a narrator for a science explainer video:")
GEMINI_USD_PER_CHAR = 32 / 11.6 * 20.0 / 1e6   # 32 audio tokens/s, 11.6 chars/s, $20 per million audio tokens (measured 2026-10-02)


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


def key(name="ELEVENLABS_API_KEY"):
    t = (Path.home() / ".zshrc").read_text()
    m = re.search(r"^\s*(?:export\s+)?" + name + r"=(?:\"([^\"]*)\"|'([^']*)'|(\S+))", t, re.M)
    return next(g for g in m.groups() if g)


def gemini(text, out_wav):
    body = {"contents": [{"parts": [{"text": f"{GEMINI_STYLE} {text}"}]}],
            "generationConfig": {"responseModalities": ["AUDIO"], "speechConfig": {
                "voiceConfig": {"prebuiltVoiceConfig": {"voiceName": GEMINI_VOICE}}}}}
    req = urllib.request.Request(
        f"https://generativelanguage.googleapis.com/v1beta/models/{GEMINI_MODEL}:generateContent",
        json.dumps(body).encode(), {"x-goog-api-key": key("GEMINI_API_KEY"), "Content-Type": "application/json"},
        method="POST")
    for attempt in range(6):
        try:
            d = json.loads(urllib.request.urlopen(req, timeout=240).read())
            audio = next((p["inlineData"] for p in (d.get("candidates") or [{}])[0].get("content", {}).get("parts", [])
                          if "inlineData" in p), None)
            if audio and audio.get("data"):
                break
            raise urllib.error.URLError("no audio in response: " + json.dumps(d)[:160])
        except (urllib.error.HTTPError, urllib.error.URLError) as e:
            if (isinstance(e, urllib.error.HTTPError) and e.code not in (429, 500, 502, 503)) or attempt == 5:
                raise
            time.sleep(8 * (attempt + 1))
    rate = (re.search(r"rate=(\d+)", audio.get("mimeType", "")) or [None, "24000"])[1]
    ff(["-f", "s16le", "-ar", rate, "-ac", "1", "-i", "pipe:0", "-ar", "48000", "-ac", "1", str(out_wav)],
       base64.b64decode(audio["data"]))


def eleven(text, out_wav):
    body = {"text": text, "model_id": "eleven_multilingual_v2",
            "voice_settings": {"stability": 0.5, "similarity_boost": 0.75}}
    req = urllib.request.Request(f"https://api.elevenlabs.io/v1/text-to-speech/{SARAH}",
                                 json.dumps(body).encode(),
                                 {"xi-api-key": key(), "Content-Type": "application/json", "Accept": "audio/mpeg"},
                                 method="POST")
    for attempt in range(8):   # ElevenLabs allows few concurrent requests: back off on 429/5xx
        try:
            mp3 = urllib.request.urlopen(req, timeout=180).read()
            break
        except urllib.error.HTTPError as e:
            if e.code not in (429, 500, 502, 503) or attempt == 7:
                raise
            time.sleep(10 * (attempt + 1))
    ff(["-f", "mp3", "-i", "pipe:0", "-ar", "48000", "-ac", "1", str(out_wav)], mp3)


def say(text, out_wav):
    """Free draft voice (macOS). Never ship a video narrated this way.

    Speaks one sentence at a time and writes <wav>.words.json with estimated word times
    (each sentence's measured length shared out by word length), so a draft can be cued and
    previewed without a speech-to-text pass. Real narration is timed by align.py instead.
    """
    sentences = [x for x in re.split(r"(?<=[.!?])\s+", text.strip()) if x]
    parts, words, t0 = [], [], 0.0
    for n, sent in enumerate(sentences):
        aiff = out_wav.with_name(f"{out_wav.stem}.{n}.aiff")
        part = out_wav.with_name(f"{out_wav.stem}.{n}.wav")
        r = subprocess.run(["say", "-v", "Samantha", "-o", str(aiff), sent], capture_output=True)
        if r.returncode:
            sys.exit("say: " + r.stderr.decode(errors="replace")[:300])
        ff(["-i", str(aiff), "-ar", "48000", "-ac", "1", "-af", "apad=pad_dur=0.25", str(part)])
        aiff.unlink()
        d = secs(part)
        toks = sent.split()
        total = sum(len(w) + 1 for w in toks) or 1
        t = t0
        for w in toks:
            dw = (d - 0.25) * (len(w) + 1) / total
            words.append([round(t, 2), round(t + dw, 2), w])
            t += dw
        t0 += d
        parts.append(part)
    listing = out_wav.with_suffix(".txt")
    listing.write_text("".join(f"file '{p.resolve()}'\n" for p in parts))
    ff(["-f", "concat", "-safe", "0", "-i", str(listing), "-ar", "48000", "-ac", "1", str(out_wav)])
    for p in parts + [listing]:
        p.unlink()
    out_wav.with_suffix(".words.json").write_text(json.dumps(words))


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--script", required=True)
    ap.add_argument("--out", required=True)
    ap.add_argument("--dry-run", action="store_true")
    ap.add_argument("--engine", choices=["eleven", "gemini", "say"])
    a = ap.parse_args()
    sp = Path(a.script)
    script = json.loads(sp.read_text())
    out = Path(a.out); out.mkdir(parents=True, exist_ok=True)
    notes = lesson_notes(script["lesson"])
    tts_chars = sum(len(s["tts"]) for s in script["scenes"] if s.get("tts"))
    if tts_chars and not a.engine:   # no default: two of the three engines cost money
        sys.exit("this script has narration to synthesize: pass --engine eleven, gemini or say")
    a.engine = a.engine or "eleven"
    cost = {"eleven": "ElevenLabs quota", "gemini": f"Gemini, about ${tts_chars * GEMINI_USD_PER_CHAR:.2f}", "say": "free draft voice"}[a.engine]
    print(f"narration characters this video: {tts_chars} (cap {TTS_CHAR_CAP}; {cost})")
    if tts_chars > TTS_CHAR_CAP:
        sys.exit("over the character cap; shorten the tts text")
    if a.dry_run:
        return
    durs, problems, est = {}, [], {}
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
            if "notes" not in s:   # once align.py has run, narration holds the transcript: keep it
                s["narration"] = speakable(slide.get("notes"))
            s["slideTitle"] = slide.get("title", "")
        elif "tts" in s:
            cache = out / {"eleven": ".tts", "gemini": ".tts-gemini", "say": ".tts-say"}[a.engine] / (hashlib.sha256(s["tts"].encode()).hexdigest()[:16] + ".wav")
            cache.parent.mkdir(exist_ok=True)
            if not cache.exists():
                {"eleven": eleven, "gemini": gemini, "say": say}[a.engine](s["tts"], cache)
            ff(["-i", str(cache), str(w)])
            s["narration"] = speakable(s.get("caption") or s["tts"])   # "caption": the same words spelled for the eye (SOCS, NF-κB) when "tts" spells them for the voice
            if a.engine == "say":
                est[s["id"]] = json.loads(cache.with_suffix(".words.json").read_text())
        else:
            problems.append(f"{s['id']}: needs one of silent / clip / tts")
            continue
        durs[s["id"]] = round(secs(w), 3)
    if problems:
        sys.exit("\n".join(problems))
    (out / "durations.json").write_text(json.dumps(durs, indent=1))
    sp.write_text(json.dumps(script, indent=1, ensure_ascii=False))
    (out / "ENGINE").write_text(a.engine + "\n")   # which voice these wavs hold; "say" means draft
    if a.engine == "say":   # estimated word times, in the shape align.py writes
        (out / "words.json").write_text(json.dumps({s["id"]: est.get(s["id"], []) for s in script["scenes"]}))
    print(f"{len(durs)} scenes, {sum(durs.values()):.1f}s total narration+cards ({a.engine})")


if __name__ == "__main__":
    main()
