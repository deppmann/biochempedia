#!/usr/bin/env python3
"""Hand films to an outside animator (an agent in another tool, working in a folder of its own)
and take its work back. The script and narration stay ours; the animator writes scenes.py only.

    animator_kit.py build   KIT_DIR FILM_DIR [FILM_DIR ...] [--fresh]
    animator_kit.py collect KIT_DIR [--apply]

FILM_DIR is a film folder in this checkout: explainers/<lesson> or explainers/<lesson>/<chapter>.
It must hold script.json. If it has audio/ (wavs, durations.json, words.json) that is copied;
if not, the narration is recorded here with Kokoro and timed (needs ~/.venvs/kokoro and ~/.venvs/stt).

build writes a self-contained KIT_DIR (put it OUTSIDE the repo, so the animator cannot read our
finished films): a copy of this pipeline, and per film script.json, audio/, BRIEF.md, TASK.md,
lesson_for_context.mdx and, unless --fresh, the folder's current scenes.py as reference_old_scenes.py
(the film's earlier version). KIT_DIR/PROMPT.md is the text to paste into the animator.

collect checks that the protected files are untouched, scans each scenes.py for known shortcuts
(decorative motion, unseeded randomness, an end card with its own construct), lints draft.mp4, reads
layout_report.json, and prints one line per film. With --apply it copies each scenes.py back into
its FILM_DIR (the file it replaces is kept as scenes.before_kit.py; do not commit that).
A frame check by a different model family is still required before a film ships.
"""
import argparse
import hashlib
import json
import re
import shutil
import subprocess
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
REPO = HERE.parents[1]
PROTECT = ("script.json", "audio/durations.json", "audio/words.json")
SHORTCUTS = [
    (r"def \w*(mote|ambient|starfield|sparkle|twinkle)\w*\(|add_ambient", "decorative motion helper"),
    (r"hash\(", "random seed from hash() (changes between runs)"),
    (r"default_rng\(\s*\)|random\.seed\(\s*\)|np\.random\.(rand|randn|uniform|normal|choice)\(", "unseeded random numbers"),
    (r"layout_ok\s*=\s*True", "layout_ok opt-out (check each one is justified)"),
]


def sha(p):
    return hashlib.sha256(Path(p).read_bytes()).hexdigest()


def camel(scene_id):
    return "".join(p[:1].upper() + p[1:] for p in re.split(r"[_\-\s]+", scene_id) if p)


def run(cmd, **kw):
    r = subprocess.run([str(c) for c in cmd], capture_output=True, text=True, **kw)
    if r.returncode:
        sys.exit(f"failed: {' '.join(map(str, cmd[:4]))} ...\n{(r.stderr or r.stdout)[-1500:]}")
    return r.stdout


def build(a):
    from fftools import FFMPEG
    kit = Path(a.kit).resolve()
    if REPO in kit.parents or kit == REPO:
        sys.exit("put the kit outside the repo, so the animator cannot read our finished films")
    if kit.exists() and any(kit.iterdir()):
        sys.exit(f"{kit} exists and is not empty: use a new folder for each batch")
    (kit / "_pipeline").mkdir(parents=True)
    for p in HERE.iterdir():
        if p.suffix in (".py", ".sh") and p.name != "animator_kit.py":
            shutil.copy(p, kit / "_pipeline" / p.name)
    if (HERE / "examples").exists():
        shutil.copytree(HERE / "examples", kit / "_pipeline/examples", ignore=shutil.ignore_patterns("__pycache__", "*.mp4", ".render-*"))
    task_t, brief = (HERE / "kit/TASK.md").read_text(), (HERE / "kit/BRIEF.md").read_text()
    films, manifest = [], {"repo": str(REPO), "films": {}}
    for fd in a.films:
        src = Path(fd).resolve()
        rel = src.relative_to(REPO / "explainers").parts
        slug, fid = rel[0], "__".join(rel)
        script_p = src / "script.json"
        if not script_p.exists():
            sys.exit(f"{src}: no script.json")
        script = json.loads(script_p.read_text())
        d = kit / fid
        (d / "audio").mkdir(parents=True)
        shutil.copy(script_p, d / "script.json")
        au = src / "audio"
        ids = [s["id"] for s in script["scenes"]]
        if all((au / f"{i}.wav").exists() for i in ids) and (au / "durations.json").exists() and (au / "words.json").exists():
            for p in list(au.glob("*.wav")) + [au / "durations.json", au / "words.json"]:
                shutil.copy(p, d / "audio" / p.name)
        else:
            print(f"{fid}: recording narration with Kokoro ...", flush=True)
            env = {**__import__("os").environ, "PYTHONPATH": str(HERE)}
            run([sys.executable, HERE / "build_audio.py", "--script", script_p, "--out", d / "audio", "--engine", "kokoro"], env=env)
            run([Path.home() / ".venvs/stt/bin/python", HERE / "align.py", "--dir", d], env=env)
            shutil.copy(script_p, d / "script.json")   # align.py re-writes the file; keep ours byte for byte
            shutil.rmtree(d / "audio/.tts-kokoro", ignore_errors=True)
        lesson_p = REPO / "src/content/lessons" / slug / "lesson.mdx"
        lesson = lesson_p.read_text() if lesson_p.exists() else ""
        if lesson:
            (d / "lesson_for_context.mdx").write_text(lesson)
        m = re.search(r'^title:\s*"?(.*?)"?\s*$', lesson, re.M)
        lesson_title = m.group(1) if m else slug
        ref = next((p for p in (src / "scenes.old.py", src / "scenes.py") if p.exists()), None)
        ref_line = "- No earlier version of this film exists: choose the colour map yourself and list it at the top of `scenes.py`."
        if ref and not a.fresh:
            shutil.copy(ref, d / "reference_old_scenes.py")
            ref_line = ("- `reference_old_scenes.py`: this film's earlier version. Reuse its COLOUR MAP and its model and plotting "
                        "helpers. Do not reuse its pacing or layout: the earlier film went too fast and sat still too long.")
        spoken = [i for i, s in zip(ids, script["scenes"]) if s.get("tts")]
        ex = spoken[min(2, len(spoken) - 1)] if spoken else ids[0]
        task = task_t
        for k, v in {"film_title": script.get("title", fid), "lesson_title": lesson_title, "reference_line": ref_line,
                     "example_id": ex, "example_class": camel(ex), "first_class": camel(ids[0]), "end_class": camel(ids[-1]),
                     "ffmpeg": FFMPEG, "film_id": fid}.items():
            task = task.replace("{" + k + "}", v)
        (d / "TASK.md").write_text(task)
        (d / "BRIEF.md").write_text(brief)
        dur = sum(json.loads((d / "audio/durations.json").read_text()).values())
        manifest["films"][fid] = {"source": str(src), "protected": {p: sha(d / p) for p in PROTECT},
                                  "wavs": {p.name: sha(p) for p in sorted((d / "audio").glob("*.wav"))}}
        films.append(f"- `{fid}/`: \"{script.get('title', fid)}\" ({len(ids)} scenes, about {dur:.0f} s of narration)")
    manifest["pipeline"] = {p.name: sha(p) for p in sorted((kit / "_pipeline").glob("*.py"))}
    (kit / "kit_manifest.json").write_text(json.dumps(manifest, indent=1))
    prompt = (HERE / "kit/PROMPT.md").read_text().replace("{n_films}", str(len(films))).replace("{film_list}", "\n".join(films))
    (kit / "PROMPT.md").write_text(prompt)
    print(f"kit ready: {kit}\n" + "\n".join(films) + f"\nOpen {kit} as the animator's workspace and paste {kit / 'PROMPT.md'}")


def collect(a):
    kit = Path(a.kit).resolve()
    man = json.loads((kit / "kit_manifest.json").read_text())
    changed = [n for n, h in man["pipeline"].items() if not (kit / "_pipeline" / n).exists() or sha(kit / "_pipeline" / n) != h]
    if changed:
        print(f"PIPELINE CHANGED in the kit (results not comparable): {', '.join(changed)}")
    out = {}
    for fid, info in man["films"].items():
        d, r = kit / fid, {"problems": []}
        for p, h in {**info["protected"], **{f"audio/{n}": h for n, h in info["wavs"].items()}}.items():
            if not (d / p).exists() or sha(d / p) != h:
                r["problems"].append(f"protected file changed: {p}")
        sc = d / "scenes.py"
        if not sc.exists():
            r["problems"].append("no scenes.py"); out[fid] = r; continue
        code = sc.read_text()
        r["lines"] = code.count("\n")
        for pat, what in SHORTCUTS:
            n = len(re.findall(pat, code, re.I))
            if n:
                r["problems"].append(f"{what} x{n}")
        script = json.loads((d / "script.json").read_text())
        end_id = script["scenes"][-1]["id"]
        m = re.search(rf"class {camel(end_id)}\(EndCard\):\n((?:    .*\n|\n)*)", code + "\n")
        if not m:
            r["problems"].append("end card is not a plain EndCard subclass")
        elif "def construct" in m.group(1):
            r["problems"].append("end card overrides construct")
        if (d / "draft.mp4").exists():
            lint = json.loads(run([sys.executable, HERE / "film_lint.py", d / "draft.mp4"]))
            r["lint"] = {k: lint[k] for k in ("duration_s", "frozen_pct", "longest_freeze_s", "ink_median_pct", "empty_pct", "flags")}
            if (d / "draft.mp4").stat().st_mtime < sc.stat().st_mtime:
                r["problems"].append("draft.mp4 is older than scenes.py: render again")
        else:
            r["problems"].append("no draft.mp4")
        lr = d / "layout_report.json"
        if lr.exists():
            rep = json.loads(lr.read_text())
            r["layout"] = {"issues": rep["issues_total"], "by_kind": rep["by_kind"]}
        else:
            r["problems"].append("no layout_report.json")
        fa = d / "film_author.json"
        if fa.exists():
            try:
                j = json.loads(fa.read_text())
                r["author"] = {k: j.get(k) for k in ("render_rounds", "wall_minutes", "model", "open_faults", "notes")}
            except Exception:
                r["problems"].append("film_author.json is not valid JSON")
        if a.apply and not any(p.startswith(("protected", "no scenes")) for p in r["problems"]):
            src = Path(info["source"])
            if (src / "scenes.py").exists() and not (src / "scenes.before_kit.py").exists():
                shutil.copy(src / "scenes.py", src / "scenes.before_kit.py")
            shutil.copy(sc, src / "scenes.py")
            r["applied_to"] = str(src)
        out[fid] = r
        L, Y = r.get("lint", {}), r.get("layout", {})
        print(f"{fid}: {L.get('duration_s', '?')} s, frozen {L.get('frozen_pct', '?')}%, longest still {L.get('longest_freeze_s', '?')} s, "
              f"ink {L.get('ink_median_pct', '?')}%, flags '{L.get('flags', '')}', layout issues {Y.get('issues', '?')}, {r.get('lines', 0)} lines"
              + ("" if not r["problems"] else "\n    CHECK: " + "; ".join(r["problems"])) + (f"\n    copied to {r['applied_to']}" if "applied_to" in r else ""))
    (kit / "collect.json").write_text(json.dumps(out, indent=1))
    print(f"details: {kit / 'collect.json'}\nNext: a frame check by a different model family, then one fix round.")


if __name__ == "__main__":
    sys.path.insert(0, str(HERE))
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    sub = ap.add_subparsers(dest="cmd", required=True)
    b = sub.add_parser("build"); b.add_argument("kit"); b.add_argument("films", nargs="+")
    b.add_argument("--fresh", action="store_true", help="do not include the folder's current scenes.py as a reference")
    c = sub.add_parser("collect"); c.add_argument("kit"); c.add_argument("--apply", action="store_true")
    a = ap.parse_args()
    build(a) if a.cmd == "build" else collect(a)
