#!/usr/bin/env python3
"""Zero-token film planner: turn each film's script, scene code, captions and lint numbers into a
precise, scene-by-scene work order. No model reads anything.

    python3 explainers/_pipeline/film_plan.py --lint docs/expansion/films/lint.jsonl --out docs/expansion/films/plans
    python3 explainers/_pipeline/film_plan.py --lint ... --only history-of-life        # one film, printed

For every lesson-level film (explainers/<slug>/script.json with public/explainers/<slug>/explainer.mp4)
it writes plans/<course>.md (films ordered oldest-and-worst first) and plans/plan.csv.
Each film gets a LEVEL (see docs/expansion/films/PROCESS.md):
  L1 re-pace     no tokens: add "pace" (and "ambient") to script.json, rebuild_kokoro.sh
  L2 patch       a small model applies the listed scene edits (about 60-120k tokens)
  L3 re-author   new script and scenes to BRIEF.md (about 0.5-0.9M tokens); only where L2 cannot fix it
"""
import argparse, csv, json, re, subprocess
from collections import defaultdict
from pathlib import Path

R = Path(".")
norm = lambda w: re.sub(r"[^a-z0-9]", "", w.lower())
camel = lambda i: "".join(p[:1].upper() + p[1:] for p in re.split(r"[_\-\s]+", i) if p)
sec = lambda z: sum(float(p) * 60 ** i for i, p in enumerate(reversed(z.split(":"))))
mmss = lambda t: f"{int(t) // 60}:{int(t) % 60:02d}"


def course_of(slug):
    p = R / "src/content/lessons" / slug / "lesson.mdx"
    if not p.exists():
        return "methods-and-other"
    m = re.search(r'^course:\s*"?([\w-]+)', p.read_text()[:6000], re.M)
    return m.group(1) if m else "biochemistry"


def git_first(p):
    o = subprocess.run(["git", "log", "--format=%cs", "--diff-filter=A", "--", str(p)], capture_output=True, text=True).stdout.split()
    return o[-1] if o else ""


def scene_starts(script, vtt):
    """Start time of each spoken scene, from the caption cues (matched on the scene's first words)."""
    cues = [(sec(a), body) for a, _, body in re.findall(r"(\d+:\d+:[\d.]+) --> (\d+:\d+:[\d.]+)\n(.+)", vtt)]
    starts, k = {}, 0
    for s in script["scenes"]:
        text = s.get("narration") or s.get("tts") or ""
        key = [norm(w) for w in text.split()[:4] if norm(w)]
        if not key:
            continue
        for j in range(k, len(cues)):
            cw = [norm(w) for w in cues[j][1].split() if norm(w)]
            if cw[:len(key)] == key or (len(key) >= 3 and cw[:3] == key[:3]):
                starts[s["id"]] = cues[j][0]; k = j + 1
                break
    return starts


def plan(slug, lint):
    d = R / "explainers" / slug
    script = json.loads((d / "script.json").read_text())
    code = (d / "scenes.py").read_text() if (d / "scenes.py").exists() else ""
    vttp = R / "public/explainers" / slug / "explainer.vtt"
    starts = scene_starts(script, vttp.read_text()) if vttp.exists() else {}
    order = sorted(starts.items(), key=lambda kv: kv[1])
    def scene_at(t):
        cur = None
        for sid, st in order:
            if st <= t + 0.5:
                cur = sid
        return cur
    blocks = {m.group(1): b for m, b in zip(re.finditer(r"^class (\w+)\(", code, re.M), re.split(r"^class \w+\(", code, flags=re.M)[1:])}
    L = lint or {}
    items, score = [], 0
    spoken = [s for s in script["scenes"] if (s.get("tts") or s.get("narration"))]
    clip = any("clip" in s for s in script["scenes"])
    words = sum(len((s.get("tts") or s.get("narration") or "").split()) for s in spoken)

    # pace
    pace_wpm = L.get("wpm_overall") or 0   # words over the whole running time, pauses included
    if pace_wpm >= 122 and not script.get("pace"):
        if clip:
            items.append(("PACE", f"The film runs {pace_wpm} words a minute overall and the narration is recorded slide audio (\"clip\" scenes). Replace each `\"clip\"` with `\"tts\"` holding that scene's `narration` text, then add `\"pace\": {{\"speed\": 0.9, \"gap\": 0.35}}` at the top of script.json and rebuild with rebuild_kokoro.sh."))
        else:
            items.append(("PACE", f"The film runs {pace_wpm} words a minute overall (target 115 or less). Add `\"pace\": {{\"speed\": 0.9, \"gap\": 0.35}}` at the top of script.json and run `sh explainers/_pipeline/rebuild_kokoro.sh {slug}` (no scene edits: cues are word-synced)."))
        score += 2
    # sentences and dense scenes
    for s in spoken:
        text = s.get("tts") or s.get("narration")
        n = len(text.split())
        long = [x.strip() for x in re.split(r"(?<=[.!?])\s+", text) if len(x.split()) > 24]
        for x in long:
            items.append(("SENTENCE", f"`{s['id']}`: a {len(x.split())}-word sentence (\"{' '.join(x.split()[:7])} ...\"). Split it in two at the first natural break; keep every fact and hedge.")); score += 1
        if n > 70:
            items.append(("DENSE", f"`{s['id']}`: {n} words in one scene (about {round(n / 2.4)} s). Split into two scenes at the point where the subject changes, each with its own picture.")); score += 2
    # freezes: one item per scene, since neighbouring freezes are usually one static picture
    fz = defaultdict(list)
    for st, ln in (L.get("freezes") or []):
        fz[scene_at(st) or "?"].append((st, ln))
    for sid, lst in fz.items():
        tot = sum(ln for _, ln in lst)
        when = ", ".join(f"{mmss(st)} for {ln} s" for st, ln in sorted(lst))
        text = next((x.get("tts") or x.get("narration") or "" for x in spoken if x["id"] == sid), "")
        items.append(("FREEZE", f"`{sid}` (\"{' '.join(text.split()[:8])} ...\"): the picture is frozen at {when}. A one-second pulse does not fix this (tested 2026-11-09). Make the scene's subject move for the whole sentence: an updater (drift, flow, a counter or gauge that runs), or build the diagram piece by piece across the sentence instead of all at once. New `self.at()` cues must be in spoken order."))
        score += 2 if tot >= 12 else 1
    # thin scenes: few animation calls for the words spoken
    for s in spoken:
        b = blocks.get(camel(s["id"])) or blocks.get(s["id"]) or ""
        n = len((s.get("tts") or s.get("narration")).split())
        plays, ats = len(re.findall(r"self\.play\(", b)), len(re.findall(r"self\.at\(", b))
        if b and n >= 30 and plays * 14 < n:
            items.append(("THIN", f"`{s['id']}`: {n} words but only {plays} animation{'s' if plays != 1 else ''} ({ats} cues). Give each sentence its own beat: show the thing, then name it.")); score += 2
    # small type
    small = sorted({int(x) for x in re.findall(r"size=(\d+)", code) if int(x) < 22})
    if small:
        lines = [str(i + 1) for i, ln in enumerate(code.split("\n")) if re.search(r"size=(1\d|2[01])\b", ln)][:12]
        items.append(("TYPE", f"Text below the 22 minimum (sizes {small}) at scenes.py lines {', '.join(lines)}{' ...' if len(lines) == 12 else ''}. Raise to 24 or more and shorten the label to fit.")); score += 1
    if re.search(r"set_opacity\(0\.[1-4]\d?\)", code) and re.search(r"T\([^)]*color=GREY", code):
        items.append(("CONTRAST", "Grey labels and low-opacity text are present. Any label a student must read should be TEXT or a concept colour at full opacity.")); score += 1
    # hook, predict, end card
    first = (spoken[0].get("tts") or spoken[0].get("narration")) if spoken else ""
    if spoken and "?" not in " ".join(re.split(r"(?<=[.!?])\s+", first)[:3]) and not any("?" in (s.get("tts") or s.get("narration") or "") for s in spoken[:2]):
        items.append(("HOOK", f"`{spoken[0]['id']}` opens with a statement (\"{' '.join(first.split()[:9])} ...\"). Re-order so the film's question comes in the first two sentences; the answer is usually already in the last scene.")); score += 1
    if not any("?" in (s.get("tts") or s.get("narration") or "") for s in spoken):
        items.append(("PREDICT", "The film never asks the viewer anything. Add one predict beat before the key result: a question sentence, then a `{\"silent\": 4.5}` scene holding the question on screen.")); score += 1
    m = re.search(r"LINE\s*=\s*[\"'](.+?)[\"']", code)
    title = script.get("title", "")
    if m and (norm(m.group(1)) == norm(title) or len(m.group(1).split()) <= 3):
        items.append(("END", f"The end card reads \"{m.group(1)}\", which is a title, not a take-home. Replace LINE with the rule from the last spoken scene (12 words or fewer).")); score += 1
    D = L.get("duration_s") or 0
    flags = (L.get("flags") or "").split()
    if "EMPTY" in flags:
        items.append(("EMPTY", f"{L['empty_pct']}% of sampled frames are nearly empty. Enlarge the main subject to fill at least 60% of the frame height and keep it on screen between beats.")); score += 2
    if "THIN" in flags:
        items.append(("FRAME", f"Median drawn area is {L['ink_median_pct']}% of the frame. Scale the main group up (`.scale_to_fit_height(5.5)`) and move labels onto or beside it.")); score += 1
    template = "setup_template" in code or not code
    n_thin = sum(1 for k, _ in items if k in ("THIN", "FREEZE", "DENSE"))
    if template:
        level = "L1" if items else "ok"
    elif (D and D < 150 and n_thin >= 3) or n_thin >= 7 or ("EMPTY" in flags and n_thin >= 4):
        level = "L3"
    elif any(k not in ("PACE",) for k, _ in items):
        level = "L2"
    elif items:
        level = "L1"
    else:
        level = "ok"
    return dict(film=slug, course=course_of(slug), created=git_first(d / "scenes.py"), title=title, duration_s=D, wpm=L.get("wpm"),
                frozen_pct=L.get("frozen_pct"), words=words, level=level, score=score, items=items, flags=" ".join(flags))


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--lint", required=True); ap.add_argument("--out", default="docs/expansion/films/plans"); ap.add_argument("--only")
    a = ap.parse_args()
    lint = {}
    for ln in open(a.lint):
        try:
            j = json.loads(ln); lint[j["film"]] = j
        except Exception:
            pass
    chaptered = {p.parent.parent.name for p in R.glob("explainers/*/*/script.json")}
    rows = []
    for sp in sorted(R.glob("explainers/*/script.json")):
        slug = sp.parent.name
        if slug.startswith(("_", "bio-")) or (a.only and slug != a.only):
            continue
        mp4 = f"public/explainers/{slug}/explainer.mp4"
        if not (R / mp4).exists():
            continue
        try:
            r = plan(slug, lint.get(mp4)); r["chapters"] = slug in chaptered; rows.append(r)
        except Exception as e:
            print("skip", slug, e)
    if a.only:
        for r in rows:
            print(r["film"], r["level"], r["score"]); [print(" ", k, t) for k, t in r["items"]]
        return
    out = Path(a.out); out.mkdir(parents=True, exist_ok=True)
    with open(out / "plan.csv", "w", newline="") as f:
        w = csv.writer(f); w.writerow("film course created duration_s wpm frozen_pct level score chapters n_items flags".split())
        for r in rows:
            w.writerow([r["film"], r["course"], r["created"], r["duration_s"], r["wpm"], r["frozen_pct"], r["level"], r["score"], int(r["chapters"]), len(r["items"]), r["flags"]])
    by = defaultdict(list)
    for r in rows:
        by[r["course"]].append(r)
    for c, rs in by.items():
        rs.sort(key=lambda r: (r["chapters"], r["created"], -r["score"]))
        lv = defaultdict(int)
        for r in rs:
            lv[r["level"]] += 1
        md = [f"# Film work orders: {c}", "", f"{len(rs)} films. " + ", ".join(f"{k}: {v}" for k, v in sorted(lv.items())) + ". Oldest first, then worst first. Films whose lesson already has a chapter series are listed last.",
              "Made by `explainers/_pipeline/film_plan.py` with no model; see `docs/expansion/films/PROCESS.md` for what L1, L2 and L3 mean and how to run them.", ""]
        for r in rs:
            md.append(f"## {r['film']} — {r['level']}" + (" (lesson has a chapter series)" if r["chapters"] else ""))
            md.append(f"\"{r['title']}\" · made {r['created']} · {mmss(r['duration_s'])} · {r['wpm']} wpm · {r['frozen_pct']}% frozen · {r['words']} words" + (f" · flags: {r['flags']}" if r["flags"] else ""))
            md += [f"{i}. **{k}** {t}" for i, (k, t) in enumerate(r["items"], 1)] or ["Nothing flagged."]
            md.append("")
        (out / f"{c}.md").write_text("\n".join(md))
    lv = defaultdict(int)
    for r in rows:
        lv[(r["level"], r["chapters"])] += 1
    print(len(rows), "films;", dict(lv))


if __name__ == "__main__":
    main()
