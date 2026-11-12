#!/usr/bin/env python3
"""Automatic layout check for the explainer films: catches, in code, what the frame checker finds by eye.

It runs inside every render with no change to scenes.py: NarratedScene (kx_manim.py) samples the
mobjects on screen at the end of every self.play / self.wait (so also at every self.at cue), and every
0.5 s of scene time during long animations. It uses Manim's own geometry (glyph outlines and path
points), never pixels, and it only reports: it never fails or changes a render.

Issue kinds (each with the exact text involved):
  text_overlap   two labels' letters touch or overlap
  covered        a stroke (line, arrow, curve, outline) runs through a label's letters, or a filled shape
                 drawn on top of a label covers letters. A label inside its own box is fine: the box
                 outline does not cross the letters and its fill is drawn underneath.
  edge           a label is cut by the frame edge (cut) or sits within 2% of the frame width of it (near)
  small          a label below the house minimum (font_size 22; labels a student must read want 28)

Opt out on purpose (no change to the look): `obj.layout_ok = True` on a label, a shape or any group
that holds them (for example a dimmed backdrop, or a swarm that is meant to pass behind labels).
Issues seen only mid-animation and lasting under 0.6 s are marked "transient" (a dot passing a word,
a label sliding into place); the summary counts them separately.

Outputs: render.py writes layout_report.json beside the draft and prints one summary line. The same
check without encoding video (Manim --dry_run at 240p, about 3x faster than a draft render):

    python3 layout_check.py --script script.json --scenes scenes.py --audio audio [--only s03_x,s04_y]

Blind spots: raster images (ImageMobject), anything drawn as pixels; whether a crossing is legible
(a thin faint line through a word is flagged like a thick one); stale text (a label left from an earlier
beat is not judged); objects other than text near the edge; meaning (a label on the wrong thing).
"""
import json
import os
import sys
import time as _time
from pathlib import Path

try:
    import numpy as np
except ImportError:   # merge/summary need no numpy (render.py may run under a bare python3)
    np = None

MIN_FONT = 22          # house minimum (Manim font_size)
EDGE_FRAC = 0.02       # of frame width: closer than this to the left or right edge is "near"
EDGE_FRAC_Y = 0.025    # of frame height, for top and bottom (tuned on five finished films, 2026-11-12)
SAMPLE_DT = 0.5        # seconds between mid-animation samples
SHRINK = 0.12          # glyph boxes are shrunk by this fraction per side before testing
TRANSIENT_S = 0.6

_TEXT_CLASSES = None


def _text_classes():
    global _TEXT_CLASSES
    if _TEXT_CLASSES is None:
        from manim import Text, MarkupText
        cl = [Text, MarkupText]
        try:
            from manim import Paragraph
            cl.append(Paragraph)
        except Exception:
            pass
        _TEXT_CLASSES = tuple(cl)
    return _TEXT_CLASSES


def _label(m):
    for a in ("original_text", "text"):
        v = getattr(m, a, None)
        if isinstance(v, str) and v.strip():
            return " ".join(v.split())[:60]
    return type(m).__name__


def _bbox(pts):
    return np.array([pts[:, 0].min(), pts[:, 1].min(), pts[:, 0].max(), pts[:, 1].max()])


def _op(m, kind):
    try:
        if kind == "fill":
            a = m.get_fill_opacities()
        else:
            a = m.get_stroke_opacities()
        return float(np.max(a)) if len(a) else 0.0
    except Exception:
        return 0.0


def _stroke_w(m):
    try:
        return float(np.max(m.get_stroke_widths()))
    except Exception:
        return float(getattr(m, "stroke_width", 0) or 0)


def _curve_samples(pts):
    """Points along a VMobject's cubic Bezier path, about every 0.03 units."""
    n = len(pts) // 4
    if n == 0:
        return np.zeros((0, 2))
    c = pts[: n * 4].reshape(n, 4, 3)[:, :, :2]
    chord = np.linalg.norm(c[:, 3] - c[:, 0], axis=1) + 0.5 * np.linalg.norm(c[:, 1] - c[:, 0], axis=1) \
        + 0.5 * np.linalg.norm(c[:, 3] - c[:, 2], axis=1)
    k = np.clip(np.ceil(chord / 0.03).astype(int) + 1, 2, 400)
    out = []
    for i in range(n):
        t = np.linspace(0, 1, k[i])[:, None]
        p0, p1, p2, p3 = c[i]
        out.append(((1 - t) ** 3) * p0 + 3 * ((1 - t) ** 2) * t * p1 + 3 * (1 - t) * t * t * p2 + t ** 3 * p3)
    return np.vstack(out)


def _inside_poly(pts, poly):
    """Even-odd test of points (N,2) against a closed polygon (M,2)."""
    x, y = pts[:, 0][:, None], pts[:, 1][:, None]
    x1, y1 = poly[:, 0][None, :], poly[:, 1][None, :]
    x2, y2 = np.roll(poly[:, 0], -1)[None, :], np.roll(poly[:, 1], -1)[None, :]
    with np.errstate(divide="ignore", invalid="ignore"):
        cross = ((y1 > y) != (y2 > y)) & (x < (x2 - x1) * (y - y1) / (y2 - y1 + 1e-12) + x1)
    return (cross.sum(axis=1) % 2) == 1


class Checker:
    def __init__(self, scene):
        self.scene = scene
        self.sid = os.environ.get("KX_SCENE_ID", type(scene).__name__)
        self.issues = {}
        self.next_t = 0.0
        self.samples = 0
        self.errors = 0
        self.secs = 0.0

    # ------------------------------------------------------------- collect
    def _collect(self, mid):
        from manim.utils.family import extract_mobject_family_members
        TC = _text_classes()
        sc = self.scene
        busy = set()
        if mid and getattr(sc, "animations", None):
            for an in sc.animations:
                mob = getattr(an, "mobject", None)
                if mob is not None and type(mob).__name__ != "ValueTracker":
                    busy.update(id(x) for x in mob.get_family())
        info = {}   # id(leaf) -> (owner text or None, ok flag)

        def walk(m, owner, ok):
            ok = ok or bool(getattr(m, "layout_ok", False))
            if owner is None and isinstance(m, TC):
                owner = m
            info[id(m)] = (owner, ok)
            for s in m.submobjects:
                walk(s, owner, ok)
        for m in sc.mobjects:
            walk(m, None, False)
        order = extract_mobject_family_members(sc.mobjects, use_z_index=True, only_those_with_points=True)
        texts, shapes = {}, []
        for i, leaf in enumerate(order):
            owner, ok = info.get(id(leaf), (None, False))
            pts = getattr(leaf, "points", None)
            if pts is None or len(pts) == 0 or ok:
                continue
            if mid and id(leaf) in busy:
                continue
            if owner is not None:
                if _op(leaf, "fill") < 0.25:
                    continue
                t = texts.setdefault(id(owner), {"mob": owner, "glyphs": [], "idx": i})
                t["glyphs"].append(_bbox(pts))
            else:
                fo, so, sw = _op(leaf, "fill"), _op(leaf, "stroke"), _stroke_w(leaf)
                if fo < 0.5 and (so < 0.25 or sw < 0.8):
                    continue
                shapes.append({"mob": leaf, "idx": i, "fo": fo, "fill": fo >= 0.5, "stroke": so >= 0.25 and sw >= 0.8, "pts": pts})
        return list(texts.values()), shapes

    # ------------------------------------------------------------- sample
    def sample(self, mid=False):
        t0 = _time.time()
        try:
            self._sample(mid)
        except Exception as e:   # never break a render
            self.errors += 1
            if self.errors == 1:
                print(f"[layout_check] {self.sid}: sampling error ignored: {e!r}", file=sys.stderr)
        self.secs += _time.time() - t0

    def tick(self):
        t = self.scene.renderer.time
        if t >= self.next_t:
            self.next_t = t + SAMPLE_DT
            self.sample(mid=True)

    def _sample(self, mid):
        from manim import config
        self.samples += 1
        now = round(float(self.scene.renderer.time), 2)
        texts, shapes = self._collect(mid)
        W, H = config.frame_width, config.frame_height
        m, mv = EDGE_FRAC * W, EDGE_FRAC_Y * H
        for t in texts:
            g = np.array(t["glyphs"])
            s = (g[:, 2:] - g[:, :2]) * SHRINK
            t["g"] = np.hstack([g[:, :2] + s, g[:, 2:] - s])
            t["box"] = np.array([g[:, 0].min(), g[:, 1].min(), g[:, 2].max(), g[:, 3].max()])
            t["name"] = _label(t["mob"])
            b = t["box"]
            if os.environ.get("KX_LAYOUT_DEBUG"):
                print(f"[layout_check] {now} {t['name']!r} box {np.round(b, 2).tolist()}", file=sys.stderr)
            cut = b[0] < -W / 2 or b[2] > W / 2 or b[1] < -H / 2 or b[3] > H / 2
            near = b[0] < -W / 2 + m or b[2] > W / 2 - m or b[1] < -H / 2 + mv or b[3] > H / 2 - mv
            if cut or near:
                gap = min(b[0] + W / 2, W / 2 - b[2], b[1] + H / 2, H / 2 - b[3])
                self._add("edge", t["name"], "cut by the frame edge" if cut else "near the frame edge", now, mid, b,
                          extra={"gap": round(float(gap), 3)})
            fs = getattr(t["mob"], "font_size", None)
            if fs is not None and fs < MIN_FONT - 0.5:
                self._add("small", t["name"], f"font_size {fs:.0f} < {MIN_FONT}", now, mid, b)
        # text vs text (glyph boxes)
        for i in range(len(texts)):
            for j in range(i + 1, len(texts)):
                a, c = texts[i], texts[j]
                if not _boxes_hit(a["box"], c["box"]):
                    continue
                if _any_overlap(a["g"], c["g"]):
                    n1, n2 = sorted([a["name"], c["name"]])
                    self._add("text_overlap", n1, n2, now, mid, a["box"])
        # opaque fills hide whatever was drawn before them (a label's own dark backing, a chip over a line)
        occ = [(o["idx"], _bbox(o["pts"]), o) for o in shapes if o["fo"] >= 0.8]
        # text vs shapes
        for sh in shapes:
            pts = sh["pts"]
            sb = _bbox(pts)
            hit = [t for t in texts if _boxes_hit(sb, t["box"])]
            if not hit:
                continue
            # a box or card that holds a label must also keep clear of the frame edge
            if (sb[2] - sb[0]) * (sb[3] - sb[1]) < 0.4 * W * H:
                held = [t for t in hit if sb[0] <= t["box"][0] and sb[1] <= t["box"][1] and sb[2] >= t["box"][2] and sb[3] >= t["box"][3]]
                if held:
                    cut = sb[0] < -W / 2 or sb[2] > W / 2 or sb[1] < -H / 2 or sb[3] > H / 2
                    if cut or sb[0] < -W / 2 + m or sb[2] > W / 2 - m or sb[1] < -H / 2 + mv or sb[3] > H / 2 - mv:
                        gap = min(sb[0] + W / 2, W / 2 - sb[2], sb[1] + H / 2, H / 2 - sb[3])
                        self._add("edge", held[0]["name"], f"its {type(sh['mob']).__name__} "
                                  + ("is cut by the frame edge" if cut else "is near the frame edge"), now, mid, sb,
                                  extra={"gap": round(float(gap), 3)})
            samp = _curve_samples(pts)
            if len(samp) == 0:
                continue
            what = _shape_name(sh["mob"])
            for t in hit:
                g = t["g"]
                crossed = False
                if sh["stroke"]:
                    ins = ((samp[:, None, 0] > g[None, :, 0]) & (samp[:, None, 0] < g[None, :, 2])
                           & (samp[:, None, 1] > g[None, :, 1]) & (samp[:, None, 1] < g[None, :, 3]))
                    p = samp[ins.any(axis=1)]
                    for oi, ob, o in occ:
                        if len(p) < 2:
                            break
                        if oi > sh["idx"] and _boxes_hit(ob, t["box"]):
                            p = p[~_inside_poly(p, o.setdefault("poly", _curve_samples(o["pts"])))]
                    crossed = len(p) >= 2
                    if crossed:
                        self._add("covered", t["name"], f"{what} runs through the letters", now, mid, t["box"])
                if sh["fill"] and not crossed and sh["idx"] > t["idx"]:
                    cen = np.c_[(g[:, 0] + g[:, 2]) / 2, (g[:, 1] + g[:, 3]) / 2]
                    if _inside_poly(cen, samp).any():
                        self._add("covered", t["name"], f"filled {what} drawn over the letters", now, mid, t["box"])

    def _add(self, kind, text, other, now, mid, box, extra=None):
        k = (kind, text, other.split(" at (")[0])
        r = self.issues.get(k)
        if r is None:
            self.issues[k] = r = {"scene": self.sid, "kind": kind, "text": text, "with": other, "t_first": now,
                                  "t_last": now, "samples": 0, "mid_only": True,
                                  "at": [round(float((box[0] + box[2]) / 2), 2), round(float((box[1] + box[3]) / 2), 2)]}
        r["t_last"] = now
        r["samples"] += 1
        if extra:
            for a, v in extra.items():
                r[a] = min(r.get(a, v), v)
        if not mid:
            r["mid_only"] = False

    def flush(self):
        out = os.environ.get("KX_LAYOUT_OUT")
        try:
            rows = []
            for r in self.issues.values():
                r["transient"] = bool(r["mid_only"] and r["t_last"] - r["t_first"] < TRANSIENT_S)
                del r["mid_only"]
                rows.append(r)
            rows.sort(key=lambda r: r["t_first"])
            rec = {"scene": self.sid, "end_s": round(float(self.scene.renderer.time), 2), "samples": self.samples,
                   "check_s": round(self.secs, 2), "errors": self.errors, "issues": rows}
            if out:
                with open(out, "a") as f:
                    f.write(json.dumps(rec) + "\n")
        except Exception as e:
            print(f"[layout_check] could not write report: {e!r}", file=sys.stderr)


def _boxes_hit(a, b):
    return a[0] < b[2] and b[0] < a[2] and a[1] < b[3] and b[1] < a[3]


def _any_overlap(g1, g2):
    return bool(((g1[:, None, 0] < g2[None, :, 2]) & (g2[None, :, 0] < g1[:, None, 2])
                 & (g1[:, None, 1] < g2[None, :, 3]) & (g2[None, :, 1] < g1[:, None, 3])).any())


def _shape_name(m):
    n = type(m).__name__
    c = m.get_center()
    return f"{n} at ({c[0]:.1f}, {c[1]:.1f})"


# ------------------------------------------------------------------ merging and summary
def merge(jsonl, out_json, offsets=None):
    """Merge per-scene records into one report; offsets maps scene id -> start time in the film."""
    try:
        recs = [json.loads(l) for l in Path(jsonl).read_text().splitlines() if l.strip()]
    except Exception:
        recs = []
    issues = []
    t = 0.0
    for r in recs:
        off = (offsets or {}).get(r["scene"], t)
        for i in r["issues"]:
            i["film_s"] = round(off + i["t_first"], 1)
            issues.append(i)
        t = off + r["end_s"]
    real = [i for i in issues if not i["transient"]]
    count = {}
    for i in real:
        count[i["kind"]] = count.get(i["kind"], 0) + 1
    rep = {"version": 1, "scenes": len(recs), "issues_total": len(real), "transient_total": len(issues) - len(real),
           "by_kind": count, "check_seconds": round(sum(r.get("check_s", 0) for r in recs), 1),
           "per_scene": {r["scene"]: {"samples": r["samples"], "errors": r["errors"], "end_s": r["end_s"]} for r in recs},
           "issues": real, "transient": [i for i in issues if i["transient"]]}
    Path(out_json).write_text(json.dumps(rep, indent=1))
    return rep


def summary(rep, path):
    k = ", ".join(f"{v} {n}" for n, v in sorted(rep["by_kind"].items())) or "clean"
    return f"layout check: {rep['issues_total']} issues ({k}); {rep['transient_total']} transient; {path}"


def main():
    import argparse
    import subprocess
    import re
    ap = argparse.ArgumentParser(description="Run the layout check without encoding video.")
    ap.add_argument("--script", required=True)
    ap.add_argument("--scenes", required=True)
    ap.add_argument("--audio", required=True)
    ap.add_argument("--out", default=None, help="default: layout_report.json beside script.json")
    ap.add_argument("--only", default="", help="comma-separated scene ids")
    a = ap.parse_args()
    here = Path(__file__).resolve().parent
    sys.path.insert(0, str(here))
    from render import camel, MANIM
    script = Path(a.script).resolve()
    scenes_py, audio = Path(a.scenes).resolve(), Path(a.audio).resolve()
    ids = [s["id"] for s in json.loads(script.read_text())["scenes"]]
    only = [x for x in a.only.split(",") if x]
    classes = set(re.findall(r"^class\s+(\w+)", scenes_py.read_text(), re.M))
    durs = json.loads((audio / "durations.json").read_text())
    out = Path(a.out) if a.out else script.parent / "layout_report.json"
    work = Path(os.environ.get("TMPDIR", "/tmp")) / f"layout-{os.getpid()}"
    work.mkdir(parents=True, exist_ok=True)
    jl = work / "layout.jsonl"
    offsets, t = {}, 0.0
    for i in ids:
        offsets[i] = t
        t += float(durs.get(i, 0)) + 0.4
    for i in ids:
        if only and i not in only:
            continue
        c = next((x for x in (i, camel(i)) if x in classes), None)
        if not c:
            print(f"{i}: no class", file=sys.stderr)
            continue
        env = {**os.environ, "KX_DURATION": str(durs[i]), "KX_SCRIPT": str(script), "KX_SCENE_ID": i, "KX_AUDIO": str(audio),
               "KX_LAYOUT_OUT": str(jl),
               "PYTHONPATH": os.pathsep.join(filter(None, [str(here), str(scenes_py.parent), os.environ.get("PYTHONPATH")]))}
        r = subprocess.run([str(MANIM), "-ql", "--dry_run", "-r", "426,240", "--progress_bar", "none", "-v", "ERROR",
                            "--media_dir", str(work / "media"), str(scenes_py), c], env=env, capture_output=True, text=True)
        if r.returncode:
            print(f"{i}: manim failed: {(r.stderr or r.stdout)[-400:]}", file=sys.stderr)
    rep = merge(jl, out, offsets)
    print(summary(rep, out))


if __name__ == "__main__":
    main()
