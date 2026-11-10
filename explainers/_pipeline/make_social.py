#!/usr/bin/env python3
"""Package a vertical (9:16) social cut: burn large word-by-word captions into the picture (most social
video is watched muted) and write web/social.mp4 (1080x1920, 30 fps) plus web/social-poster.jpg.

    ~/.venvs/stt/bin/python make_social.py --dir <film dir> [--script social.json] [--master social_hq] [--max 90]

The master comes from: render.py --script social.json --scenes scenes_social.py --audio audio_social
--out social_hq.mp4 --quality h --vertical. Captions are timed from a transcript of the real audio and
spelled from the script (make_web.respell). Chunks of up to 3 words; the word being spoken is gold.
"""
import argparse, json, re, sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent))
from make_web import words_for, respell, dur, ff

GOLD, WHITE = "&H0043A8D4&", "&H00F0EAE8&"   # ASS colours are BGR


def t(x):
    h, r = divmod(max(x, 0), 3600); m, s = divmod(r, 60)
    return f"{int(h)}:{int(m):02d}:{s:05.2f}"


def chunks(words, n=3, max_chars=18):
    cur = []
    for w in words:
        if cur and (len(cur) >= n or len(" ".join(x[2] for x in cur)) + len(w[2]) + 1 > max_chars or w[0] - cur[-1][1] > 0.6):
            yield cur; cur = []
        cur.append(w)
        if re.search(r"[.!?,;:]$", w[2]):
            yield cur; cur = []
    if cur:
        yield cur


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--dir", required=True); ap.add_argument("--script", default="social.json")
    ap.add_argument("--master", default="social_hq"); ap.add_argument("--audio", default="audio_social")
    ap.add_argument("--max", type=float, default=90.0); ap.add_argument("--y", type=int, default=1500)
    a = ap.parse_args()
    d = Path(a.dir); script = json.loads((d / a.script).read_text())
    master, segdir = d / f"{a.master}.mp4", d / f".render-{a.master}"
    if not master.exists():
        sys.exit(f"missing {master}")
    ev, t0 = [], 0.0
    for s in script["scenes"]:
        L = dur(segdir / f"{s['id']}.mp4")
        if s.get("narration"):
            ws = respell(words_for(d / a.audio / f"{s['id']}.wav"), s["narration"])
            for ch in chunks(ws):
                for i, w in enumerate(ch):
                    end = ch[i + 1][0] if i + 1 < len(ch) else min(w[1] + 0.35, L)
                    txt = " ".join((f"{{\\c{GOLD}}}{x[2]}{{\\c{WHITE}}}" if j == i else x[2]) for j, x in enumerate(ch))
                    ev.append([t0 + w[0], t0 + end, txt])
        t0 += L
    for i in range(len(ev) - 1):          # one caption on screen at a time: never run into the next
        ev[i][1] = max(min(ev[i][1], ev[i + 1][0]), ev[i][0] + 0.05)
    lines = [f"Dialogue: 0,{t(b)},{t(e)},Cap,,0,0,0,,{{\\pos(540,{a.y})}}{x}" for b, e, x in ev]
    ass = d / f"{a.master}.ass"
    ass.write_text("[Script Info]\nScriptType: v4.00+\nPlayResX: 1080\nPlayResY: 1920\nWrapStyle: 2\n\n[V4+ Styles]\n"
                   "Format: Name, Fontname, Fontsize, PrimaryColour, SecondaryColour, OutlineColour, BackColour, Bold, Italic, Underline, StrikeOut, ScaleX, ScaleY, Spacing, Angle, BorderStyle, Outline, Shadow, Alignment, MarginL, MarginR, MarginV, Encoding\n"
                   f"Style: Cap,Avenir Next,78,{WHITE},{WHITE},&H00101010&,&H96000000&,-1,0,0,0,100,100,0,0,1,6,2,5,40,40,40,1\n\n"
                   "[Events]\nFormat: Layer, Start, End, Style, Name, MarginL, MarginR, MarginV, Effect, Text\n" + "\n".join(lines) + "\n")
    web = d / "web"; web.mkdir(exist_ok=True)
    esc = str(ass).replace("\\", "\\\\").replace(":", "\\:").replace("'", "\\'")
    ff(["-i", str(master), "-vf", f"fps=30,scale=1080:1920,ass='{esc}',format=yuv420p", "-c:v", "libx264", "-preset", "slow",
        "-crf", "20", "-c:a", "aac", "-b:a", "128k", "-ac", "2", "-movflags", "+faststart", str(web / "social.mp4")])
    ff(["-ss", f"{min(4.0, t0 / 3):.2f}", "-i", str(web / "social.mp4"), "-frames:v", "1", "-q:v", "3", str(web / "social-poster.jpg")])
    D = dur(web / "social.mp4")
    print(f"{d.name}: social.mp4 {D:.1f}s, {(web / 'social.mp4').stat().st_size / 1e6:.1f} MB, {len(lines)} caption words")
    if D > a.max:
        sys.exit(f"social cut is {D:.0f}s, over the {a.max:.0f}s cap: trim the script")


if __name__ == "__main__":
    main()
