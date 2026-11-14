#!/usr/bin/env python3
"""Automatic layout check for the explainer films: catches, in code, what the frame checker finds by eye.

It runs inside every render with no change to scenes.py: NarratedScene (kx_manim.py) samples the
mobjects on screen at the end of every self.play / self.wait (so also at every self.at cue: "at rest"),
and during animations and waits ("in motion": every 0.1 s while a label moves or fades, every 0.25 s
otherwise). It uses Manim's own geometry (glyph outlines, path points sampled along every curve, z-order
and colours), never pixels, and it only reports: it never fails, blocks or changes a render.

Each issue has a severity: "error" (must fix before the film ships) or "warning" (look at it; fix it
if it reads as touching). Kinds, each with the exact text involved:

  errors (at rest)
    text_overlap  two labels' letters touch or overlap
    covered       a stroke (line, arrow, curve, outline, axis, brace, ray) runs through a label's letters,
                  or a filled shape drawn on top of a label covers letters
    straddle      a line or outline runs through a label's own box (chip, pill, ring, card): the box sits
                  on a panel border, a cell outline, an axis or an arrow even though the letters are clear
    box_overlap   two label boxes (chips, pills, cards) overlap, or a label sits on another label's box
    overflow      a label's letters stick out of its own box, pill or ring
    edge          a label (or the box holding it) is cut by the frame edge
    small         rendered font size under 22 (after every scale and fit; EndCard lines included)
    outside       a closed shape drawn in a rectangular panel, stage, board or glass pokes out of it by 0.2+
  warnings
    near          clearance under about 5-7 px at 1080p (label to label 0.05, line to letters 0.04, box to
                  box 0.04 scene units), or a box tight around its own letters
    edge          a label within 2% of the frame edge; a picture shape cut by the frame edge
    outside       a poke-out of 0.06 to 0.2
    contrast      text on a fill whose colour is too close to its own (under 2.5:1), or letters over three or
                  more small shapes (a busy background); one entry per background colour per film
    in motion     (in_motion: true) an overlap or crossing seen only while things move or fade: a cross-fade
                  with old and new letters overlapping for 0.3 s or more, or a moving shape across a label or
                  its box for 1 s or more. Other kinds are judged only where things come to rest.

Shorter in-motion overlaps are "transient": listed apart and not counted. Text drawn in its own
background's colour (hidden on purpose) is not checked.

Every entry names the scene, the film time, both objects (a label by its text; a shape by its type,
colour, position and the label of the group it belongs to), and a hint: which way to move the label and
by about how much, in scene units (the 16:9 frame is 14.22 x 8).

Opt out on purpose (no change to the look): `obj.layout_ok = True` on a label, a shape or any group
that holds them (a dimmed backdrop, a deliberate strike-through, a swarm meant to pass behind labels).
To opt out of one kind only: `obj.layout_ok = "covered"` (or a set of kinds, e.g. {"covered", "near"}).
Opted-out findings are not counted but are still listed under "suppressed" in the report, so a frame
checker can look at exactly those spots: a group-wide layout_ok on a whole world is the commonest way a
real defect slipped through (2026-11-13 corpus).

Outputs: render.py writes layout_report.json beside the draft and prints one summary line. The same
check without encoding video (Manim --dry_run at the draft size; one manim process per scene):

    python3 layout_check.py --script script.json --scenes scenes.py --audio audio [--jobs 4] [--only s03_x]

Regression suite (synthetic scenes, one per defect class, each with a clean twin):
    ~/.venvs/manim/bin/python tests/layout/run_tests.py

Blind spots (left to the frame checker): raster images (ImageMobject) and anything drawn as pixels;
meaning (a label on the wrong thing, a stale label left from an earlier beat, an orphaned last word);
whether an opted-out spot is really fine; contrast against raster or gradient backgrounds; overlaps
between two shapes neither of which is a label or a label's box (a dot on a cell, two curves crossing);
cross-fades shorter than 0.3 s (listed as transient).
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
SAMPLE_DT = 0.25       # seconds between samples during a wait (updaters running)
MOVE_DT = 0.1          # ... and while a label moves or fades, to time cross-fades
SHRINK = 0.12          # glyph boxes are shrunk by this fraction per side before an overlap counts
TRANSIENT_S = 0.3      # in-motion issues shorter than this are transient
NEAR_TEXT = 0.05       # label-to-label clearance (scene units; 0.05 = about 7 px at 1080p)
NEAR_STROKE = 0.04     # line-to-letters clearance (about 5 px at 1080p)
NEAR_BOX = 0.04        # box-to-box clearance
TILE_TOL = 0.06        # boxes overlapping by less than this only share an edge; a line this close to a box's
                       # border runs along it (a highlight frame), not through it
OUT_ERR = 0.2          # "outside": poke-out at which it becomes an error
OUT_MIN = 0.06         # ... and below which it is ignored
CONTRAST_MIN = 2.5
INVISIBLE = 1.1        # text this close to its background colour is hidden on purpose: not checked
# Issues seen only in motion count for these kinds only, and only when they last this long (s);
# a label sliding or growing into place is judged where it comes to rest.
MOTION_KINDS = {"text_overlap": TRANSIENT_S, "covered": 1.0, "straddle": 1.0, "box_overlap": 1.0}
LW = 0.01              # Manim stroke_width 1 = 0.01 scene units (Cairo line-width multiple)
ALL = "all"
# "outside" is judged against rectangular panels, stages, boards, cards and glasses only: a picture's own
# outlines (a tree's branches past its crown, a clock's hands past its rim) poke out on purpose.
PANEL_CLASSES = ("Rectangle", "RoundedRectangle", "Square", "SurroundingRectangle", "BackgroundRectangle")
KINDS = ("text_overlap", "covered", "straddle", "box_overlap", "overflow", "edge", "small", "outside", "near",
         "contrast")

_TEXT_CLASSES = None
_COLOR_NAMES = {"#58C4DD": "blue", "#F5D547": "yellow", "#83C167": "green", "#FC6255": "red", "#8B93A1": "grey",
                "#E8EAF0": "white", "#3FB8C0": "teal", "#D4A843": "gold", "#FFFFFF": "white", "#0F1117": "background"}


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


def _exempt(m):
    """layout_ok value -> frozenset of exempt kinds (ALL for True)."""
    v = getattr(m, "layout_ok", None)
    if not v:
        return frozenset()
    if v is True:
        return frozenset([ALL])
    if isinstance(v, str):
        return frozenset([v])
    try:
        return frozenset(v)
    except TypeError:
        return frozenset([ALL])


def _bbox(pts):
    return np.array([pts[:, 0].min(), pts[:, 1].min(), pts[:, 0].max(), pts[:, 1].max()])


def _op(m, kind):
    try:
        a = m.get_fill_opacities() if kind == "fill" else m.get_stroke_opacities()
        return float(np.max(a)) if len(a) else 0.0
    except Exception:
        return 0.0


def _stroke_w(m):
    try:
        return float(np.max(m.get_stroke_widths()))
    except Exception:
        return float(getattr(m, "stroke_width", 0) or 0)


def _rgb(m, kind):
    try:
        c = m.get_fill_color() if kind == "fill" else m.get_stroke_color()
        return np.array(c.to_rgb(), dtype=float)
    except Exception:
        return np.array([0.9, 0.9, 0.9])


def _hexname(rgb):
    h = "#%02X%02X%02X" % tuple(int(round(255 * float(x))) for x in rgb[:3])
    best, bd = h, 1e9
    for k, n in _COLOR_NAMES.items():
        r = np.array([int(k[i:i + 2], 16) / 255 for i in (1, 3, 5)])
        d = float(np.abs(r - rgb[:3]).sum())
        if d < bd:
            best, bd = n, d
    return best if bd < 0.12 else h


def _lum(rgb):
    c = np.where(rgb <= 0.03928, rgb / 12.92, ((rgb + 0.055) / 1.055) ** 2.4)
    return 0.2126 * c[0] + 0.7152 * c[1] + 0.0722 * c[2]


def _contrast(a, b):
    la, lb = _lum(a), _lum(b)
    return (max(la, lb) + 0.05) / (min(la, lb) + 0.05)


def _curve_samples(pts, step=0.03):
    """Points along a VMobject's cubic Bezier path, about every `step` units."""
    n = len(pts) // 4
    if n == 0:
        return np.zeros((0, 2))
    c = pts[: n * 4].reshape(n, 4, 3)[:, :, :2]
    chord = np.linalg.norm(c[:, 3] - c[:, 0], axis=1) + 0.5 * np.linalg.norm(c[:, 1] - c[:, 0], axis=1) \
        + 0.5 * np.linalg.norm(c[:, 3] - c[:, 2], axis=1)
    k = np.clip(np.ceil(chord / step).astype(int) + 1, 2, 400)
    seg = np.repeat(np.arange(n), k)
    start = np.repeat(np.cumsum(k) - k, k)
    t = ((np.arange(len(seg)) - start) / np.repeat(k - 1, k))[:, None]
    p0, p1, p2, p3 = c[seg, 0], c[seg, 1], c[seg, 2], c[seg, 3]
    return ((1 - t) ** 3) * p0 + 3 * ((1 - t) ** 2) * t * p1 + 3 * (1 - t) * t * t * p2 + t ** 3 * p3


def _inside_poly(pts, poly):
    """Even-odd test of points (N,2) against a closed polygon (M,2)."""
    out = np.zeros(len(pts), dtype=bool)
    if len(pts) == 0 or len(poly) < 3:
        return out
    near = ((pts[:, 0] >= poly[:, 0].min()) & (pts[:, 0] <= poly[:, 0].max())
            & (pts[:, 1] >= poly[:, 1].min()) & (pts[:, 1] <= poly[:, 1].max()))
    if not near.any():
        return out
    if not near.all():
        out[near] = _inside_poly(pts[near], poly)
        return out
    x, y = pts[:, 0][:, None], pts[:, 1][:, None]
    x1, y1 = poly[:, 0][None, :], poly[:, 1][None, :]
    x2, y2 = np.roll(poly[:, 0], -1)[None, :], np.roll(poly[:, 1], -1)[None, :]
    with np.errstate(divide="ignore", invalid="ignore"):
        cross = ((y1 > y) != (y2 > y)) & (x < (x2 - x1) * (y - y1) / (y2 - y1 + 1e-12) + x1)
    return (cross.sum(axis=1) % 2) == 1


def _in_boxes(p, g, pad=0.0):
    """(N,) mask: point p inside any of the boxes g (G,4) grown by pad."""
    if len(p) == 0 or len(g) == 0:
        return np.zeros(len(p), dtype=bool)
    return ((p[:, None, 0] > g[None, :, 0] - pad) & (p[:, None, 0] < g[None, :, 2] + pad)
            & (p[:, None, 1] > g[None, :, 1] - pad) & (p[:, None, 1] < g[None, :, 3] + pad)).any(axis=1)


def _depth(p, boundary, each=False):
    """How far points p lie from a boundary polyline (max, or each); 0 for no points."""
    if len(p) == 0 or len(boundary) == 0:
        return np.zeros(len(p)) if each else 0.0
    d = np.sqrt(((p[:, None, :] - boundary[None, :, :]) ** 2).sum(-1)).min(axis=1)
    return d if each else float(d.max())


def _glyph_gap(g1, g2):
    dx = np.maximum(g1[:, None, 0] - g2[None, :, 2], g2[None, :, 0] - g1[:, None, 2])
    dy = np.maximum(g1[:, None, 1] - g2[None, :, 3], g2[None, :, 1] - g1[:, None, 3])
    d = np.where((dx < 0) & (dy < 0), np.maximum(dx, dy), np.hypot(np.maximum(dx, 0), np.maximum(dy, 0)))
    return float(d.min())


def _longest_run(mask):
    best = cur = 0
    for v in mask:
        cur = cur + 1 if v else 0
        best = max(best, cur)
    return best


def _boxes_hit(a, b, pad=0.0):
    return a[0] - pad < b[2] and b[0] - pad < a[2] and a[1] - pad < b[3] and b[1] - pad < a[3]


def _fmt(v):
    return f"{v:.2f}".rstrip("0").rstrip(".")


class Checker:
    def __init__(self, scene):
        self.scene = scene
        self.sid = os.environ.get("KX_SCENE_ID", type(scene).__name__)
        self.issues = {}
        self.contrast_names = {}
        self.dt = SAMPLE_DT
        self.next_t = 0.0
        self.samples = 0
        self.errors = 0
        self.secs = 0.0
        self.endcard = any(c.__name__ == "EndCard" for c in type(scene).__mro__)

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
        info = {}   # id(leaf) -> (owner text or None, exempt kinds, label of the nearest group holding a text)

        def first_text(m, depth=0):
            if isinstance(m, TC):
                return m
            if depth > 6:
                return None
            for s in m.submobjects:
                r = first_text(s, depth + 1)
                if r is not None:
                    return r
            return None

        def walk(m, owner, ex, grp):
            e = _exempt(m)
            if e:
                ex = ex | e
            if owner is None and isinstance(m, TC):
                owner = m
            if owner is None and len(m.submobjects) > 1:
                ft = first_text(m)
                if ft is not None:
                    grp = ft
            info[id(m)] = (owner, ex, grp)
            for s in m.submobjects:
                walk(s, owner, ex, grp)
        for m in sc.mobjects:
            walk(m, None, frozenset(), None)
        order = extract_mobject_family_members(sc.mobjects, use_z_index=True, only_those_with_points=True)
        texts, shapes = {}, []
        for i, leaf in enumerate(order):
            owner, ex, grp = info.get(id(leaf), (None, frozenset(), None))
            pts = getattr(leaf, "points", None)
            if pts is None or len(pts) == 0:
                continue
            moving = bool(mid and id(leaf) in busy)
            if owner is not None:
                fo = _op(leaf, "fill")
                if fo < 0.25:
                    continue
                t = texts.setdefault(id(owner), {"mob": owner, "glyphs": [], "idx": i, "ex": ex, "moving": False,
                                                  "op": 0.0, "rgb": _rgb(leaf, "fill")})
                t["glyphs"].append(_bbox(pts))
                t["op"] = max(t["op"], fo)
                t["moving"] = t["moving"] or moving
            else:
                fo, so, sw = _op(leaf, "fill"), _op(leaf, "stroke"), _stroke_w(leaf)
                vis_stroke = so >= 0.25 and sw >= 0.8
                if fo < 0.12 and not vis_stroke:
                    continue
                closed = len(pts) >= 8 and float(np.linalg.norm(pts[0] - pts[-1])) < 1e-3
                shapes.append({"mob": leaf, "idx": i, "fo": fo, "fill": fo >= 0.5, "stroke": vis_stroke,
                               "sw": sw * LW if vis_stroke else 0.0, "pts": pts, "closed": closed, "ex": ex,
                               "moving": moving, "grp": grp, "bb": _bbox(pts)})
        return list(texts.values()), shapes

    # ------------------------------------------------------------- sample
    def sample(self, mid=False):
        t0 = _time.time()
        try:
            self._sample(mid)
        except Exception as e:   # never break a render
            self.errors += 1
            if self.errors == 1:
                import traceback
                print(f"[layout_check] {self.sid}: sampling error ignored: {e!r}\n{traceback.format_exc()[-600:]}",
                      file=sys.stderr)
        self.secs += _time.time() - t0

    def tick(self):
        t = self.scene.renderer.time
        if t >= self.next_t:
            # dense sampling only while a label itself moves or fades (to time cross-fades)
            anims = getattr(self.scene, "animations", None) or []
            TC = _text_classes()
            self.dt = MOVE_DT if any(type(a).__name__ != "Wait" and getattr(a, "mobject", None) is not None
                                     and any(isinstance(x, TC) for x in a.mobject.get_family()) for a in anims) else SAMPLE_DT
            self.next_t = t + self.dt
            self.sample(mid=True)

    @staticmethod
    def _samp(sh):
        if "s" not in sh:
            sh["s"] = _curve_samples(sh["pts"])
        return sh["s"]

    @staticmethod
    def _poly(sh):
        if "p" not in sh:
            sh["p"] = _curve_samples(sh["pts"], step=0.08)
        return sh["p"]

    def _shape_name(self, sh):
        m = sh["mob"]
        if sh.get("holds") is not None:
            return f"the box of {sh['holds']['name']!r}"
        col = _hexname(_rgb(m, "stroke" if sh["stroke"] else "fill"))
        c = m.get_center()
        n = f"{type(m).__name__} ({col}{' outline' if sh['stroke'] and not sh['fill'] else ''}) at ({c[0]:.1f}, {c[1]:.1f})"
        g = sh.get("grp")
        if g is not None:
            n += f" in the group with {_label(g)!r}"
        return n

    def _sample(self, mid):
        from manim import config
        self.samples += 1
        now = round(float(self.scene.renderer.time), 2)
        texts, shapes = self._collect(mid)
        W, H = config.frame_width, config.frame_height
        m, mv = EDGE_FRAC * W, EDGE_FRAC_Y * H
        frame = np.array([-W / 2, -H / 2, W / 2, H / 2])
        for t in texts:
            g = np.array(t["glyphs"])
            s = (g[:, 2:] - g[:, :2]) * SHRINK
            t["g0"] = g
            t["g"] = np.hstack([g[:, :2] + s, g[:, 2:] - s])
            t["box"] = np.array([g[:, 0].min(), g[:, 1].min(), g[:, 2].max(), g[:, 3].max()])
            t["name"] = _label(t["mob"])
            t["c"] = (t["box"][:2] + t["box"][2:]) / 2
            t["cont"] = None
            if os.environ.get("KX_LAYOUT_DEBUG"):
                print(f"[layout_check] {now} {t['name']!r} box {np.round(t['box'], 2).tolist()} "
                      f"font {getattr(t['mob'], 'font_size', 0):.1f}", file=sys.stderr)

        # In-motion samples check only what is reported in motion (overlaps and crossings); the rest is judged
        # where things come to rest. This keeps the check under about 20% of a draft render.
        full = not mid
        if full:
            texts = self._visible(texts, shapes)

        # ---- each label's own box: the smallest closed, visible shape around its centre, at most 0.6 bigger per side
        for sh in shapes:
            sh["holds"] = None
        for t in texts:
            b = t["box"]
            tw, th = b[2] - b[0], b[3] - b[1]
            best, best_area = None, 0.0
            for sh in shapes:
                if not sh["closed"] or not (sh["stroke"] or sh["fo"] >= 0.12):
                    continue
                sb = sh["bb"]
                w, h = sb[2] - sb[0], sb[3] - sb[1]
                if w > tw + 1.2 or h > th + 1.2 or not (sb[0] < t["c"][0] < sb[2] and sb[1] < t["c"][1] < sb[3]):
                    continue
                if w * h < 0.25 * tw * th:
                    continue
                if not _inside_poly(t["c"][None, :], self._poly(sh))[0]:
                    continue
                if best is None or w * h < best_area:
                    best, best_area = sh, w * h
            if best is not None and best["stroke"]:   # only a box with a visible border is a "box"; a plain fill is a backing
                t["cont"] = best
                if best["holds"] is None:
                    best["holds"] = t

        boxes = [sh for sh in shapes if sh["holds"] is not None]

        # ---- per label: frame edge, size, overflow
        for t in (texts if full else []):
            b = t["box"]
            cut = b[0] < -W / 2 or b[2] > W / 2 or b[1] < -H / 2 or b[3] > H / 2
            near = b[0] < -W / 2 + m or b[2] > W / 2 - m or b[1] < -H / 2 + mv or b[3] > H / 2 - mv
            if cut or near:
                gap = min(b[0] + W / 2, W / 2 - b[2], b[1] + H / 2, H / 2 - b[3])
                self._add("edge", "error" if cut else "warning", t, None, "cut by the frame edge" if cut else
                          "near the frame edge", now, mid, b, hint=self._edge_hint(b, W, H, m, mv), extra={"gap": round(float(gap), 3)})
            fs = getattr(t["mob"], "font_size", None)
            if fs is not None and fs < MIN_FONT - 0.5:
                h = f"font_size {fs:.0f}: render at {MIN_FONT} or more"
                if self.endcard:
                    h = (f"the EndCard auto-shrank the line to {fs:.0f} pt: put a \\n in LINE at a natural break "
                         "(words unchanged) so each row fits at 40 pt")
                elif abs(getattr(t["mob"], "_font_size", fs) - fs) > 1:
                    h += f" (built at {getattr(t['mob'], '_font_size', fs):.0f}, then scaled down with its group: scale the picture, not the label)"
                self._add("small", "error", t, None, f"font_size {fs:.0f} < {MIN_FONT}", now, mid, b, hint=h)
            c = t["cont"]
            if c is not None:
                poly = self._poly(c)
                g = t["g"]
                corners = np.vstack([g[:, [0, 1]], g[:, [2, 1]], g[:, [0, 3]], g[:, [2, 3]]])
                out = ~_inside_poly(corners, poly)
                if out.mean() > 0.02:
                    cb = c["bb"]
                    need = max(b[2] - b[0] - (cb[2] - cb[0]), b[3] - b[1] - (cb[3] - cb[1]), 0) + 0.3
                    self._add("overflow", "error", t, c, f"letters stick out of its {type(c['mob']).__name__}", now, mid, b,
                              hint=f"widen the box by about {_fmt(need)} (or shorten the label; keep it 24 pt or more)")
                    c["overflowed"] = True

        # ---- label vs label
        for i in range(len(texts)):
            for j in range(i + 1, len(texts)):
                a, c = texts[i], texts[j]
                if not _boxes_hit(a["box"], c["box"], NEAR_TEXT):
                    continue
                gap = _glyph_gap(a["g0"], c["g0"])
                if gap >= (NEAR_TEXT if full else 0.0):
                    continue
                hit = bool(((a["g"][:, None, 0] < c["g"][None, :, 2]) & (c["g"][None, :, 0] < a["g"][:, None, 2])
                            & (a["g"][:, None, 1] < c["g"][None, :, 3]) & (c["g"][None, :, 1] < a["g"][:, None, 3])).any())
                if (a["cont"] is not None and a["cont"] is c["cont"] or not full) and not hit:
                    continue   # two lines in one box (title + value): spacing is the box's business
                mover, other = (a, c) if (a["mob"].get_center()[1] < c["mob"].get_center()[1]) else (c, a)
                self._add("text_overlap" if hit else "near", "error" if hit else "warning", a, c,
                          "letters overlap" if hit else f"letters {_fmt(max(gap, 0))} apart", now, mid, a["box"],
                          hint=self._move_hint(mover, other["box"], NEAR_TEXT, W, H, label=True))

        # ---- label boxes vs other labels and other boxes
        for bx in boxes:
            own = bx["holds"]
            poly = self._poly(bx)
            for t in texts:
                if t is own or t["cont"] is bx or not _boxes_hit(bx["bb"], t["box"], NEAR_BOX):
                    continue
                if t["cont"] is not None:
                    continue   # box vs box below
                cen = np.c_[(t["g"][:, 0] + t["g"][:, 2]) / 2, (t["g"][:, 1] + t["g"][:, 3]) / 2]
                if _inside_poly(cen, poly).any() or _in_boxes(self._samp(bx), t["g"]).any():
                    self._add("box_overlap", "error", t, bx, f"sits on {self._shape_name(bx)}", now, mid, t["box"],
                              hint=self._move_hint(t, bx["bb"], NEAR_BOX, W, H, label=True))
        for i in range(len(boxes)):
            for j in range(i + 1, len(boxes)):
                A, B = boxes[i], boxes[j]
                if not _boxes_hit(A["bb"], B["bb"], NEAR_BOX):
                    continue
                pa, pb = self._poly(A), self._poly(B)
                # overlap deeper than a stroke's width; boxes that only share an edge are not "overlapping"
                ia, ib = pa[_inside_poly(pa, pb)], pb[_inside_poly(pb, pa)]
                depth = max(_depth(ia, pb), _depth(ib, pa))
                inter = depth > TILE_TOL
                ab, bb_ = A["bb"], B["bb"]
                tiled = ((abs(ab[1] - bb_[1]) < 0.03 and abs(ab[3] - bb_[3]) < 0.03
                          and min(abs(ab[2] - bb_[0]), abs(bb_[2] - ab[0])) < TILE_TOL)
                         or (abs(ab[0] - bb_[0]) < 0.03 and abs(ab[2] - bb_[2]) < 0.03
                             and min(abs(ab[3] - bb_[1]), abs(bb_[3] - ab[1])) < TILE_TOL))
                if tiled and not inter:
                    continue   # tiles set edge to edge on purpose (a base pair, a Punnett grid)
                if inter:
                    self._add("box_overlap", "error", A["holds"], B, "boxes overlap", now, mid, A["bb"],
                              hint=self._move_hint(A["holds"], B["bb"], NEAR_BOX, W, H, box=A["bb"]))
                elif full:
                    d = np.sqrt(((pa[:, None, :] - pb[None, :, :]) ** 2).sum(-1)).min() - (A["sw"] + B["sw"]) / 2
                    if d < NEAR_BOX:
                        self._add("near", "warning", A["holds"], B, f"boxes {_fmt(max(d, 0))} apart", now, mid, A["bb"],
                                  hint=self._move_hint(A["holds"], B["bb"], NEAR_BOX, W, H, box=A["bb"]))

        # ---- label boxes against the frame edge
        for bx in (boxes if full else []):
            sb = bx["bb"]
            cut = sb[0] < -W / 2 or sb[2] > W / 2 or sb[1] < -H / 2 or sb[3] > H / 2
            if cut or sb[0] < -W / 2 + m or sb[2] > W / 2 - m or sb[1] < -H / 2 + mv or sb[3] > H / 2 - mv:
                gap = min(sb[0] + W / 2, W / 2 - sb[2], sb[1] + H / 2, H / 2 - sb[3])
                self._add("edge", "error" if cut else "warning", bx["holds"], None,
                          f"its {type(bx['mob']).__name__} " + ("is cut by the frame edge" if cut else "is near the frame edge"),
                          now, mid, sb, hint=self._edge_hint(sb, W, H, m, mv), extra={"gap": round(float(gap), 3)})

        # ---- opaque fills hide whatever was drawn before them (a label's own dark backing, a plate over a line)
        occ = [(o["idx"], o["bb"], o) for o in shapes if o["fo"] >= 0.8]

        # ---- strokes and fills vs labels and label boxes
        for sh in shapes:
            sb = sh["bb"]
            pad = NEAR_STROKE + sh["sw"] / 2
            hit_t = [t for t in texts if _boxes_hit(sb, t["box"], pad)]
            hit_b = [bx for bx in boxes if bx is not sh and bx["holds"] is not None and _boxes_hit(sb, bx["bb"])]
            if not hit_t and not hit_b:
                continue
            samp = self._samp(sh)
            if len(samp) == 0:
                continue
            for t in hit_t:
                own = t["cont"] is sh
                crossed = False
                if sh["stroke"]:
                    p = samp[_in_boxes(samp, t["g"], sh["sw"] / 2)]
                    for oi, ob, o in occ:
                        if len(p) < 2:
                            break
                        if o is not sh and oi > sh["idx"] and _boxes_hit(ob, t["box"]):
                            p = p[~_inside_poly(p, self._poly(o))]
                    crossed = len(p) >= 2
                    if crossed and not (own and sh.get("overflowed")):
                        what = "its own box border" if own else self._shape_name(sh)
                        self._add("covered", "error", t, sh, f"{what} runs through the letters", now, mid, t["box"],
                                  hint=self._move_hint(t, p, NEAR_STROKE + sh["sw"] / 2, W, H, label=True, pts=True,
                                                       own=own))
                    if not crossed and full and len(samp) * 0.03 >= 0.3:   # short marks (axis ticks) may sit close
                        q = samp[_in_boxes(samp, t["g0"], pad)]
                        for oi, ob, o in occ:
                            if len(q) < 2:
                                break
                            if o is not sh and oi > sh["idx"] and _boxes_hit(ob, t["box"]):
                                q = q[~_inside_poly(q, self._poly(o))]
                        if len(q) >= 2:
                            g0 = t["g0"]
                            dx = np.maximum(np.maximum(g0[None, :, 0] - q[:, None, 0], q[:, None, 0] - g0[None, :, 2]), 0)
                            dy = np.maximum(np.maximum(g0[None, :, 1] - q[:, None, 1], q[:, None, 1] - g0[None, :, 3]), 0)
                            gap = max(float(np.hypot(dx, dy).min()) - sh["sw"] / 2, 0.0)
                        if len(q) >= 2:
                            self._add("near", "warning", t, sh, ("its own box border is tight around the letters" if own
                                      else f"{self._shape_name(sh)} passes {_fmt(gap)} from the letters"),
                                      now, mid, t["box"], hint=self._move_hint(t, q, pad, W, H, label=True, pts=True, own=own))
                if sh["fill"] and not crossed and sh["idx"] > t["idx"] and not own:
                    cen = np.c_[(t["g"][:, 0] + t["g"][:, 2]) / 2, (t["g"][:, 1] + t["g"][:, 3]) / 2]
                    if _inside_poly(cen, samp).any():
                        self._add("covered", "error", t, sh, f"filled {self._shape_name(sh)} drawn over the letters",
                                  now, mid, t["box"], hint=self._move_hint(t, sb, NEAR_STROKE, W, H, label=True)
                                  + ", or draw the label after the shape")
            # a line or outline through a label's box (the letters may be clear): the box sits on it
            if sh["stroke"]:
                for bx in hit_b:
                    if sh.get("holds") is not None:
                        continue   # box vs box handled above
                    t = bx["holds"]
                    poly = self._poly(bx)
                    ins = _inside_poly(samp, poly)
                    if ins.all() or not ins.any():
                        continue   # wholly inside (an icon in the chip) or wholly outside
                    if ins.sum() and _depth(samp[ins], self._samp(bx), each=True).max() <= TILE_TOL:
                        continue   # runs along the box's own border (a highlight frame on a grid cell)
                    ins[ins] = _depth(samp[ins], self._samp(bx), each=True) > TILE_TOL
                    bb = bx["bb"]
                    run = _longest_run(ins) * 0.03
                    if run >= 0.35 * min(bb[2] - bb[0], bb[3] - bb[1]):
                        self._add("straddle", "error", t, sh, f"{self._shape_name(sh)} runs through its box", now, mid, bb,
                                  hint=self._move_hint(t, samp[ins], NEAR_BOX, W, H, pts=True, box=bb))

        if not full:
            return
        # ---- shapes that poke out of the panel holding them; picture shapes cut by the frame
        panels = [sh for sh in shapes if sh["closed"] and sh["stroke"] and sh["holds"] is None
                  and type(sh["mob"]).__name__ in PANEL_CLASSES
                  and (sh["bb"][2] - sh["bb"][0]) * (sh["bb"][3] - sh["bb"][1]) >= 2.5 and not sh["moving"]]
        for sh in shapes:
            sb = sh["bb"]
            w, h = sb[2] - sb[0], sb[3] - sb[1]
            big = w >= 0.85 * W or h >= 0.85 * H or w * h >= 0.3 * W * H
            if not big and sh["fo"] + (1 if sh["stroke"] else 0) >= 0.5:
                over = max(-W / 2 - sb[0], sb[2] - W / 2, -H / 2 - sb[1], sb[3] - H / 2)
                if over > 0.02:
                    self._add("edge", "warning", None, sh, f"{self._shape_name(sh)} is cut by the frame edge", now, mid, sb,
                              hint=self._edge_hint(sb, W, H, m, mv))
            if not sh["closed"] or sh["holds"] is not None:
                continue
            for P in panels:
                if P is sh or sh["idx"] < P["idx"]:
                    continue   # a shape drawn behind a panel is scenery, not held by it
                pb = P["bb"]
                if not _boxes_hit(sb, pb) or w * h > 0.6 * (pb[2] - pb[0]) * (pb[3] - pb[1]):
                    continue
                if sb[0] >= pb[0] and sb[1] >= pb[1] and sb[2] <= pb[2] and sb[3] <= pb[3]:
                    continue   # panels are rectangles: inside the bounding box is inside
                ps = self._poly(sh)
                pp = self._poly(P)
                ins = _inside_poly(ps, pp)
                if ins.all():
                    continue
                gx, gy = np.meshgrid(np.linspace(sb[0], sb[2], 14), np.linspace(sb[1], sb[3], 14))
                grid = np.c_[gx.ravel(), gy.ravel()]
                grid = grid[_inside_poly(grid, ps)]
                if len(grid) < 4 or _inside_poly(grid, pp).mean() < 0.7:
                    continue   # mostly outside: not held by this panel (an arrow, a neighbour)
                bd = self._samp(P)
                outp = ps[~ins]
                d = np.sqrt(((outp[:, None, :] - bd[None, ::2, :]) ** 2).sum(-1)).min(axis=1).max()
                if d < OUT_MIN:
                    continue
                self._add("outside", "error" if d >= OUT_ERR else "warning", None, sh,
                          f"{self._shape_name(sh)} sticks out of {self._shape_name(P)} by {_fmt(d)}", now, mid, sb,
                          hint=f"move it inward by about {_fmt(d + 0.1)}, shrink it, or enlarge the panel")

        # ---- contrast: text over a filled shape of too similar a colour, or over a busy patch of small shapes
        for t in texts:
            if t["op"] < 0.6:
                continue
            if t["cr"] < CONTRAST_MIN:
                # one entry per background colour per scene, naming the labels on it
                k = ("contrast", _hexname(t["under"]))
                names = self.contrast_names.setdefault(k, [])
                if t["name"] not in names:
                    names.append(t["name"])
                lab = {"name": ", ".join(repr(n) for n in names[:3]) + (f" and {len(names) - 3} more" if len(names) > 3 else ""),
                       "ex": t["ex"], "moving": t["moving"], "key": f"labels on {_hexname(t['under'])}"}
                self._add("contrast", "warning", lab, None, f"contrast down to {t['cr']:.1f}:1 against a {_hexname(t['under'])} fill",
                          now, mid, t["box"], hint="move the labels onto a plain dark area, give them a backing plate, or change their colour")
            elif t["busy"] >= 3:
                self._add("contrast", "warning", t, None, f"letters over {t['busy']} small shapes (busy background)", now, mid,
                          t["box"], hint="move the label to a clear area or give it a dark backing plate")

    def _visible(self, texts, shapes):
        """Composite the fills under each label (z order) and drop labels drawn in their background's colour."""
        from manim import config as _cfg
        try:
            bg = np.array(_cfg.background_color.to_rgb(), dtype=float)
        except Exception:
            bg = np.array([0.06, 0.07, 0.09])
        keep = []
        for t in texts:
            g = t["g"]
            cen = np.c_[(g[:, 0] + g[:, 2]) / 2, (g[:, 1] + g[:, 3]) / 2]
            col, small = bg.copy(), 0
            for sh in shapes:   # in z order
                if sh["idx"] >= t["idx"] or sh["fo"] < 0.12 or not _boxes_hit(sh["bb"], t["box"]):
                    continue
                ins = _inside_poly(cen, self._poly(sh))
                if ins.mean() >= 0.5:
                    col = col * (1 - sh["fo"]) + _rgb(sh["mob"], "fill") * sh["fo"]
                elif ins.any() and (sh["bb"][2] - sh["bb"][0]) * (sh["bb"][3] - sh["bb"][1]) < 0.25 * (t["box"][2] - t["box"][0]) * (t["box"][3] - t["box"][1]):
                    small += 1
            tc = t["rgb"] * t["op"] + col * (1 - t["op"])
            t["under"], t["cr"], t["busy"] = col, _contrast(tc, col), small
            if _contrast(t["rgb"], col) >= INVISIBLE:
                keep.append(t)
        return keep

    # ------------------------------------------------------------- hints
    def _edge_hint(self, b, W, H, m, mv):
        moves = []
        if b[0] < -W / 2 + m:
            moves.append(f"right {_fmt(-W / 2 + m - b[0] + 0.05)}")
        if b[2] > W / 2 - m:
            moves.append(f"left {_fmt(b[2] - (W / 2 - m) + 0.05)}")
        if b[1] < -H / 2 + mv:
            moves.append(f"up {_fmt(-H / 2 + mv - b[1] + 0.05)}")
        if b[3] > H / 2 - mv:
            moves.append(f"down {_fmt(b[3] - (H / 2 - mv) + 0.05)}")
        return "move " + " and ".join(moves) if moves else "move inward"

    def _move_hint(self, t, obst, margin, W, H, label=False, pts=False, box=None, own=False):
        """Smallest move (up/down/left/right) that clears `obst` (points or a box) from the label (or its box)."""
        if own:
            return "widen or heighten the box (more padding), or shrink the label (not below 24 pt)"
        b = box if box is not None else t["box"]
        if pts:
            p = np.asarray(obst)
            ox0, oy0, ox1, oy1 = p[:, 0].min(), p[:, 1].min(), p[:, 0].max(), p[:, 1].max()
        else:
            ox0, oy0, ox1, oy1 = obst
        cand = {"up": oy1 - b[1] + margin, "down": b[3] - oy0 + margin, "right": ox1 - b[0] + margin,
                "left": b[2] - ox0 + margin}
        room = {"up": H / 2 - b[3], "down": b[1] + H / 2, "right": W / 2 - b[2], "left": b[0] + W / 2}
        ok = sorted((v, k) for k, v in cand.items() if v > 0 and v < room[k] - 0.15)
        if not ok:
            ok = sorted((v, k) for k, v in cand.items() if v > 0)
        if not ok:
            return "move apart"
        s = f"move {t['name']!r} {ok[0][1]} about {_fmt(ok[0][0])}" if t else f"move {ok[0][1]} about {_fmt(ok[0][0])}"
        if len(ok) > 1 and ok[1][0] < 2 * ok[0][0] + 0.2:
            s += f" (or {ok[1][1]} {_fmt(ok[1][0])})"
        return s

    # ------------------------------------------------------------- record
    def _add(self, kind, sev, t, other, what, now, mid, box, hint="", extra=None):
        ex = frozenset()
        moving = False
        if isinstance(t, dict):
            ex |= t["ex"]
            moving |= t["moving"]
            text = t.get("key", t["name"])
        else:
            text = ""
        if isinstance(other, dict):
            ex |= other["ex"]
            moving |= other["moving"]
            if "name" in other:     # another label
                wname = other["name"]
            else:
                wname = what.split(" at (")[0]
        else:
            wname = ""
        suppressed = bool(ex & {ALL, kind})
        if not text and isinstance(other, dict):
            text = self._shape_name(other).split(" at (")[0] if "name" not in other else other["name"]
        k = (kind, text, wname if wname else what.split(" at (")[0], suppressed)
        r = self.issues.get(k)
        if r is None:
            self.issues[k] = r = {"scene": self.sid, "kind": kind, "severity": sev, "text": text, "with": what,
                                  "t_first": now, "t_last": now, "samples": 0, "rest": 0, "mid_s": 0.0, "moving": False,
                                  "at": [round(float((box[0] + box[2]) / 2), 2), round(float((box[1] + box[3]) / 2), 2)],
                                  "hint": hint}
            if suppressed:
                r["suppressed"] = True
        if isinstance(t, dict) and "key" in t:
            r["text"] = t["name"]
            if what < r["with"]:
                r["with"] = what
        if sev == "error" and r["severity"] != "error":
            r["severity"], r["with"], r["hint"] = sev, what, hint
        r["t_last"] = now
        r["samples"] += 1
        if moving:
            r["moving"] = True
        if extra:
            for a, v in extra.items():
                r[a] = min(r.get(a, v), v)
        if not mid:
            r["rest"] += 1
        elif r.get("_last_mid") != now:
            r["mid_s"] += self.dt
            r["_last_mid"] = now

    def flush(self):
        out = os.environ.get("KX_LAYOUT_OUT")
        try:
            rows = []
            for r in self.issues.values():
                rest = r.pop("rest")
                mid_s = r.pop("mid_s")
                r.pop("_last_mid", None)
                if rest:
                    r["transient"] = False
                    r["duration_s"] = round(r["t_last"] - r["t_first"] + SAMPLE_DT, 2)
                else:
                    # seen only while things moved or faded: each in-motion sample stands for its sampling interval
                    dur = round(mid_s, 2)
                    if r["kind"] not in MOTION_KINDS:
                        continue   # judged where it comes to rest
                    r["duration_s"] = dur
                    r["transient"] = dur < MOTION_KINDS[r["kind"]]
                    r["in_motion"] = True
                    if not r["transient"] and r["severity"] == "error":
                        r["severity"] = "warning"
                        r["with"] += " (only while moving or fading)"
                        if r["kind"] == "text_overlap":
                            r["hint"] = "fade the old label out before the new one comes in (bp_parts.swap), or move one"
                rows.append(r)
            rows.sort(key=lambda r: r["t_first"])
            rec = {"scene": self.sid, "end_s": round(float(self.scene.renderer.time), 2), "samples": self.samples,
                   "check_s": round(self.secs, 2), "errors": self.errors, "issues": rows}
            if out:
                with open(out, "a") as f:
                    f.write(json.dumps(rec) + "\n")
        except Exception as e:
            print(f"[layout_check] could not write report: {e!r}", file=sys.stderr)


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
            i.setdefault("severity", "error")
            issues.append(i)
        t = off + r["end_s"]
    # contrast: one entry per background colour for the whole film (a light-ground film is one decision)
    merged, seen = [], {}
    for i in issues:
        if i["kind"] == "contrast" and not i.get("suppressed") and not i["transient"]:
            k = i["with"].split(" against ")[-1]
            if k in seen:
                c = seen[k]
                c["scenes"] = sorted(set(c.get("scenes", [c["scene"]]) + [i["scene"]]))
                c["text"] = c["text"] if len(c["text"]) > 80 else (c["text"] + ", " + i["text"])[:120]
                continue
            seen[k] = i
        merged.append(i)
    issues = merged
    sup = [i for i in issues if i.get("suppressed")]
    live = [i for i in issues if not i.get("suppressed")]
    real = [i for i in live if not i["transient"]]
    errs = [i for i in real if i["severity"] == "error"]
    warns = [i for i in real if i["severity"] != "error"]
    count, wcount = {}, {}
    for i in errs:
        count[i["kind"]] = count.get(i["kind"], 0) + 1
    for i in warns:
        k = i["kind"] + (" in motion" if i.get("in_motion") else "")
        wcount[k] = wcount.get(k, 0) + 1
    order = lambda i: (i["severity"] != "error", i["film_s"])
    rep = {"version": 2, "scenes": len(recs), "errors_total": len(errs), "warnings_total": len(warns),
           "issues_total": len(real), "transient_total": len([i for i in live if i["transient"]]),
           "suppressed_total": len([i for i in sup if not i["transient"]]),
           "by_kind": count, "warnings_by_kind": wcount,
           "check_seconds": round(sum(r.get("check_s", 0) for r in recs), 1),
           "per_scene": {r["scene"]: {"samples": r["samples"], "errors": r["errors"], "end_s": r["end_s"]} for r in recs},
           "issues": sorted(real, key=order), "transient": [i for i in live if i["transient"]],
           "suppressed": [i for i in sup if not i["transient"]]}
    Path(out_json).write_text(json.dumps(rep, indent=1))
    return rep


def summary(rep, path):
    k = ", ".join(f"{v} {n}" for n, v in sorted(rep["by_kind"].items())) or "none"
    w = ", ".join(f"{v} {n}" for n, v in sorted(rep.get("warnings_by_kind", {}).items())) or "none"
    if "errors_total" not in rep:
        return f"layout check: {rep['issues_total']} issues ({k}); {rep['transient_total']} transient; {path}"
    return (f"layout check: {rep['errors_total']} errors ({k}); {rep['warnings_total']} warnings ({w}); "
            f"{rep['transient_total']} transient; {rep['suppressed_total']} suppressed by layout_ok; {path}")


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
    ap.add_argument("--jobs", type=int, default=1, help="scenes checked at once (each is one manim process)")
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
    offsets, t = {}, 0.0
    for i in ids:
        offsets[i] = t
        t += float(durs.get(i, 0)) + 0.4
    todo = []
    for i in ids:
        if only and i not in only:
            continue
        c = next((x for x in (i, camel(i)) if x in classes), None)
        if not c:
            print(f"{i}: no class", file=sys.stderr)
            continue
        env = {**os.environ, "KX_DURATION": str(durs[i]), "KX_SCRIPT": str(script), "KX_SCENE_ID": i, "KX_AUDIO": str(audio),
               "KX_LAYOUT_OUT": str(work / f"{i}.jsonl"),
               "PYTHONPATH": os.pathsep.join(filter(None, [str(here), str(scenes_py.parent), os.environ.get("PYTHONPATH")]))}
        todo.append((i, [str(MANIM), "-ql", "--dry_run", "--progress_bar", "none", "-v", "ERROR",
                         "--media_dir", str(work / f"media-{i}"), str(scenes_py), c], env))
    running = []
    while todo or running:
        while todo and len(running) < max(1, a.jobs):
            i, cmd, env = todo.pop(0)
            running.append((i, subprocess.Popen(cmd, env=env, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)))
        i, p = running.pop(0)
        so, se = p.communicate()
        if p.returncode:
            print(f"{i}: manim failed: {(se or so)[-400:]}", file=sys.stderr)
        elif "[layout_check]" in (se or ""):
            print("\n".join(l for l in se.splitlines() if "layout_check" in l)[:600], file=sys.stderr)
    jl = work / "layout.jsonl"
    with open(jl, "w") as f:
        for i in ids:
            p = work / f"{i}.jsonl"
            if p.exists():
                f.write(p.read_text())
    rep = merge(jl, out, offsets)
    print(summary(rep, out))


if __name__ == "__main__":
    main()
