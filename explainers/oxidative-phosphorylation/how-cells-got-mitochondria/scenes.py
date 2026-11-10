"""How Your Cells Got Mitochondria: web film (16:9), levelled-up look (2026-11-09).

ONE CARRIED WORLD: one cell in cross-section that fills the frame, with a thin time scrubber under
it. The film opens on the modern cell, rewinds it into two strangers, runs it forward again and
ends on the opening frame. Every scene rebuilds the world from a named preset (MOD, ANC, WHY ...),
so objects sit in the same place across cuts, and all ambient motion is a function of one global
clock (now()), so breathing, drifting and turning carry across cuts without a jump.

COLOR MAP (one colour per concept, both cuts)
  BLUE    the host, and what is the host's (outline, arms, nucleus, the host's bead ring)
  PINK    the guest lineage (bacterium, every mitochondrion, its beads wherever they end up, 13 tiles)
  YELLOW  energy (the chain: a row of yellow blocks, its running spark, ATP sparks)
  TEAL    hydrogen            RED   oxygen            GREEN  a clue that matches
  GOLD    not settled in science (every "?" badge and its words)
  GREY    what is gone or did not happen (lost beads, the "digested" ghost); never text
  TEXT    words and neutral things (labels, scrubber, 'free bacteria' branches, question cards)

No molecular structures: DNA is a ring of beads, the chain is a row of blocks, proteins are tiles,
O2 / H2 / ATP are labelled tokens. Bead counts 40 = 15 lost + 12 moved + 13 kept are schematic
(tagged so on screen); only the 13 is a fact. The scrubber is tagged "not to scale".

REUSABLE BUILDERS (the vertical social cut imports these; all take position and size):
  make_backdrop(w, h)            layered gradient water with light shafts
  Specks(w=, h=)                 drifting specks and soft bokeh, three depths
  Cell(x, y, w, h, arm=, arms=)  breathing host / modern-cell outline, glow, graded fill, arms that hug
  Shimmer(cell)                  soft light pools drifting inside the cell
  Nucleus(x, y, r)               solid or dashed circle with a gold "?" on its rim
  Ring(host, angles, color, Rk, brk)   bead ring (DNA) that turns and follows its host
  Guest(x, y, L, H, bean=, fold=)      the pink rod / bean with double outline, chain, spark, tiles
  Sparks(guest, cell), MiniSparks(beans), O2Stream(guest, t0)   particle fields
  Scrubber(x0=, x1=, y=)         the time line with knob, gold band and fossil tick
  gold_badge(r), o2_token(r), h2_bubble(r), star(r), rod_outline(...)
  ambient helpers: now(), start_clock(scene), pulse(mob), Tw(f, rt), Proc.tw(rt, **attrs)
"""
import json
import math
import os
import random
from pathlib import Path

import numpy as np
from bp_style import *

PINK = "#F0739B"
FW, FH = config.frame_width, config.frame_height
CARD_Y = 3.15                       # the clear band above the cell where question cards sit
UNIT = Circle(radius=1).points.copy()
_WHITE = ManimColor("#FFFFFF")


# ───────────────────────────── clock and tweening ─────────────────────────────
def _scene_starts():
    """Start time of every scene in the whole film, so ambient motion is continuous across cuts."""
    try:
        a = Path(os.environ.get("KX_AUDIO", "audio"))
        if not a.is_absolute():
            a = Path(os.environ["KX_SCRIPT"]).parent / a
        d = json.loads((a / "durations.json").read_text())
    except Exception:
        return {}
    out, t = {}, 0.0
    for k, v in d.items():
        out[k] = t
        t += float(v) + 0.4
    return out


T0 = _scene_starts()
_CLK = {"t": 0.0}


def now():
    """Film time in seconds (not scene time). Every ambient motion reads this."""
    return _CLK["t"]


def start_clock(scene, z=-95):
    _CLK["t"] = T0.get(os.environ.get("KX_SCENE_ID", ""), 0.0)
    tick = VMobject().set_z_index(z)
    tick.add_updater(lambda m, dt: _CLK.__setitem__("t", _CLK["t"] + dt))
    scene.add(tick)
    return tick


def Tw(f, rt=1.0, rate=smooth):
    """An animation that calls f(alpha). Used to tween plain attributes of the procedural objects."""
    return UpdateFromAlphaFunc(VectorizedPoint(), lambda m, a: f(a), run_time=rt, rate_func=rate, remover=True)


class Proc:
    """A procedural object: plain attributes, redrawn every frame by an updater on self.mob."""

    def tw(self, rt=1.0, rate=smooth, **to):
        st = {}

        def f(a):
            if not st:
                if a <= 0:
                    return
                for k in to:
                    v = getattr(self, k)
                    st[k] = np.array(v, dtype=float) if isinstance(v, (list, tuple, np.ndarray)) else float(v)
            for k, v in to.items():
                setattr(self, k, st[k] + (np.asarray(v, dtype=float) - st[k]) * a if isinstance(st[k], np.ndarray) else st[k] + (v - st[k]) * a)
        return Tw(f, rt, rate)

    def set(self, **kw):
        for k, v in kw.items():
            setattr(self, k, v)
        return self

    def _live(self):
        self.mob.add_updater(lambda m, dt: self.draw())
        self.draw()


def lerp(a, b, t):
    return a + (b - a) * t


def P3(x, y=None):
    return np.array([x[0], x[1], 0.0]) if y is None else np.array([x, y, 0.0])


def rot2(v, ang):
    c, s = math.cos(ang), math.sin(ang)
    return np.array([c * v[0] - s * v[1], s * v[0] + c * v[1], 0.0])


def place(pts, x, y, ang=0.0):
    c, s = math.cos(ang), math.sin(ang)
    out = np.empty_like(pts)
    out[:, 0] = x + c * pts[:, 0] - s * pts[:, 1]
    out[:, 1] = y + s * pts[:, 0] + c * pts[:, 1]
    out[:, 2] = 0
    return out


def closed(p):
    return np.vstack([p, p[:1]])


def poly_pts(polys):
    """Bezier points for several separate polylines in ONE VMobject (cheap to redraw every frame)."""
    out = []
    for p in polys:
        p = np.asarray(p, dtype=float)
        a, b = p[:-1], p[1:]
        out.append(np.stack([a, a + (b - a) / 3, a + 2 * (b - a) / 3, b], 1).reshape(-1, 3))
    return np.concatenate(out) if out else np.zeros((0, 3))


def circ(p, r):
    return UNIT * r + np.array([p[0], p[1], 0.0])


BEND = 0.045
FOLDS = [(0.12, 0.40), (0.31, 0.36), (0.5, 0.17), (0.69, 0.36), (0.88, 0.40)]


def bean_pts(C, S, L, H, H0=None, bean=0.0, pinch=0.0, fold=0.0):
    """Outline of the guest in its own frame: a rod (bean=0) that rounds into a kidney bean (bean=1),
    narrows at the waist (pinch) and folds its upper edge into waves (fold, used for the inner line)."""
    H0 = H if H0 is None else H0
    e = 2.0 / (2.9 - 0.5 * bean)
    U = np.sign(C) * np.abs(C) ** e
    V = np.sign(S) * np.abs(S) ** e
    Y = 0.5 * H * V * (1 - pinch * np.exp(-(U / 0.3) ** 2))
    if fold > 0:                                  # five finger-like folds hang from the upper edge
        q = 0.5 * (U + 1)
        prof = sum(d * np.exp(-((q - qk) / 0.036) ** 2) for qk, d in FOLDS)
        Y = Y - np.where(S > 0, fold * H * prof * np.abs(V), 0.0)
    Y = Y + bean * BEND * H0 * (1 - 2 * U ** 2)
    return np.stack([0.5 * L * U, Y, np.zeros_like(U)], 1)


# ───────────────────────────── the world: builders ─────────────────────────────
def make_backdrop(w=None, h=None, z=-100):
    """Full-bleed layered water: a three-stop vertical gradient and slanted light shafts. Static."""
    w = w or config.frame_width
    h = h or config.frame_height
    top, mid, bot = ManimColor("#0F2C40"), ManimColor("#0B1826"), ManimColor("#070B12")
    n = 32
    bands = VGroup()
    for i in range(n):
        f = i / (n - 1)
        col = interpolate_color(top, mid, f / 0.55) if f < 0.55 else interpolate_color(mid, bot, (f - 0.55) / 0.45)
        bands.add(Rectangle(width=w + 0.2, height=h / n + 0.03, stroke_width=0, fill_color=col, fill_opacity=1)
                  .move_to([0, h / 2 - (i + 0.5) * h / n, 0]))
    shafts = VGroup(*[
        Polygon([x, h / 2, 0], [x + wd, h / 2, 0], [x + wd - 2.8, -h / 2, 0], [x - 3.4, -h / 2, 0],
                stroke_width=0, fill_color="#5FB7D4", fill_opacity=op)
        for x, wd, op in [(-w * 0.34, 1.3, 0.035), (-w * 0.02, 0.8, 0.028), (w * 0.24, 1.6, 0.032), (w * 0.44, 0.7, 0.025)]])
    return VGroup(bands, shafts).set_z_index(z)


class Specks(Proc):
    """Dim specks drifting left to right behind everything, in three depths (far, near, soft bokeh)."""

    def __init__(self, n=60, w=None, h=None, seed=11, z=-90):
        rng = random.Random(seed)
        self.w = (w or config.frame_width) + 0.8
        self.h = h or config.frame_height
        self.a = 1.0
        self.layers = []
        spec = [(n // 2, .015, .03, .10, .18, .40, "#9CC7D8"), (n // 3, .03, .05, .20, .32, .50, "#BFE3EE"),
                (n - n // 2 - n // 3, .10, .22, .30, .45, .06, "#8FD0E6")]
        for cnt, r0, r1, v0, v1, op, col in spec:
            P = [(rng.uniform(0, self.w), rng.uniform(-self.h / 2, self.h / 2), rng.uniform(r0, r1),
                  rng.uniform(v0, v1), rng.uniform(0, TAU)) for _ in range(cnt)]
            self.layers.append((VMobject(stroke_width=0, fill_color=col, fill_opacity=op), P))
        self.mob = VGroup(*[m for m, _ in self.layers]).set_z_index(z)
        self._live()

    def draw(self):
        t = now()
        for m, P in self.layers:
            m.set_points(np.concatenate([circ((((x0 + v * t) % self.w) - self.w / 2, y0 + 0.14 * math.sin(0.35 * t + ph)), r)
                                         for x0, y0, r, v, ph in P]))


class Cell(Proc):
    """The host: a breathing outline with a soft glow, a graded fill and thin branching arms.
    arm 0..1 grows the arms; grab[i] 0..1 pulls arm i from free swaying to hug[i]() -> (control, tip)."""
    ARMS = [(13, 1.0, 0.0), (-13, 1.0, 2.1), (-48, 0.8, 4.0), (152, 0.6, 1.2), (-140, 0.6, 3.3)]

    def __init__(self, x=0.0, y=0.0, w=11.6, h=5.7, arm=0.0, color=BLUE, n=160, arms=None, arm_len=1.2, z=-60):
        self.x, self.y, self.w, self.h, self.arm = x, y, w, h, arm
        self.a, self.lit, self.warm, self.wob, self.sweep = 1.0, 0.0, 0.0, 1.0, 0.0
        self.sq = 2.3                      # superellipse exponent: 2 is an ellipse, 6 hugs a rectangle
        self.arms = arms or self.ARMS
        self.arm_len = arm_len
        k = len(self.arms)
        self.grab, self.alen, self.hug = np.zeros(k), np.ones(k), [None] * k
        self.alen[:2] = 0.8
        self.flinches = []
        self.col = ManimColor(color)
        th = np.linspace(0, TAU, n, endpoint=False)
        self.TH, self.CT, self.ST = th, np.cos(th), np.sin(th)
        self.glow = [VMobject(fill_opacity=0) for _ in range(3)]
        self.fills = [VMobject(stroke_width=0, fill_color=c) for c in ("#17506E", "#1C6485", "#2379A0", "#2B8DB8")]
        self.warmm, self.rim, self.hi, self.glint = VMobject(), VMobject(), VMobject(), VMobject()
        self.armm = [VMobject(cap_style=CapStyleType.ROUND, joint_type=LineJointType.ROUND) for _ in self.arms]
        self.mob = VGroup(VGroup(*self.glow, *self.fills).set_z_index(z),
                          VGroup(self.warmm, self.rim, self.hi, self.glint).set_z_index(z + 10),
                          VGroup(*self.armm).set_z_index(-12))
        self._live()

    def _delta(self, th, t):
        d = self.wob * (0.014 * np.sin(3 * th + 0.9 * t) + 0.013 * np.sin(5 * th - 0.8 * t + 1.3) + 0.010 * np.sin(4 * th + 0.6 * t + 2.1) + 0.012 * math.sin(0.7 * t))
        for a0, t0, amp in self.flinches:
            age = t - t0
            if 0 <= age < 1.4:
                dd = np.angle(np.exp(1j * (th - a0)))
                d = d - amp * np.exp(-(dd / 0.22) ** 2) * math.exp(-3 * age) * math.cos(13 * age)
        return d

    def pt_at(self, deg, k=1.0):
        th = np.array([math.radians(deg)])
        e = 2 / self.sq
        u = np.sign(np.cos(th)) * np.abs(np.cos(th)) ** e
        v = np.sign(np.sin(th)) * np.abs(np.sin(th)) ** e
        d = self._delta(th, now())
        return np.array([self.x + 0.5 * self.w * u[0] * (1 + d[0]) * k, self.y + 0.5 * self.h * v[0] * (1 + d[0]) * k, 0.0])

    def at(self, u, v):
        """A point in the cell's own coordinates (u, v in -1..1)."""
        return np.array([self.x + 0.5 * self.w * u, self.y + 0.5 * self.h * v, 0.0])

    def flinch(self, deg, amp=0.09):
        self.flinches.append((math.radians(deg), now(), amp))

    def draw(self):
        t = now()
        a = max(0.0, self.a)
        d = self._delta(self.TH, t)
        e = 2 / self.sq
        U, V = np.sign(self.CT) * np.abs(self.CT) ** e, np.sign(self.ST) * np.abs(self.ST) ** e
        ring = lambda k: closed(np.stack([self.x + 0.5 * self.w * U * (1 + d) * k, self.y + 0.5 * self.h * V * (1 + d) * k, 0 * d], 1))
        pts = ring(1.0)
        col = interpolate_color(self.col, _WHITE, 0.45 * self.lit) if self.lit > 0.01 else self.col
        for m, (wd, op) in zip(self.glow, [(30, .05), (18, .08), (10, .12)]):
            m.set_points_as_corners(pts)
            m.set_stroke(col, width=wd * (1 + 0.5 * self.lit), opacity=min(1, a * op * (1 + 1.6 * self.lit)))
        for m, (k, op) in zip(self.fills, [(1.0, .30), (.86, .16), (.68, .12), (.46, .10)]):
            m.set_points_as_corners(pts if k == 1.0 else ring(k))
            m.set_fill(opacity=min(1, a * op * (1 + 0.5 * self.lit)))
        self.warmm.set_points_as_corners(pts)
        self.warmm.set_stroke(YELLOW, width=16, opacity=a * 0.20 * self.warm)
        self.rim.set_points_as_corners(pts)
        self.rim.set_stroke(col, width=6, opacity=a)
        self.hi.set_points_as_corners(ring(0.972))
        self.hi.set_stroke("#BFEFFF", width=1.5, opacity=a * 0.35)
        if 0.0 < self.sweep < 1.0:
            n = len(self.TH)
            i0 = int(self.sweep * n)
            idx = [(i0 + j) % n for j in range(-9, 10)]
            self.glint.set_points_as_corners(pts[idx])
            self.glint.set_stroke("#FFFFFF", width=9, opacity=a * math.sin(PI * self.sweep) ** 0.5)
        else:
            self.glint.set_stroke(opacity=0)
        # arms
        for i, (m, (deg, ln, ph)) in enumerate(zip(self.armm, self.arms)):
            length = self.arm_len * ln * self.arm * self.alen[i]
            g = float(self.grab[i])
            if length < 0.04 and g < 0.02:
                m.set_stroke(opacity=0)
                continue
            b = self.pt_at(deg)
            nrm = np.array([(b[0] - self.x) / (self.w / 2) ** 2, (b[1] - self.y) / (self.h / 2) ** 2, 0.0])
            nrm = nrm / (np.linalg.norm(nrm) + 1e-9)
            perp = np.array([-nrm[1], nrm[0], 0.0])
            sway = 0.24 * math.sin(0.8 * t + ph)
            tip = b + length * rot2(nrm, sway)
            ctl = b + 0.5 * length * rot2(nrm, -0.6 * sway) + perp * 0.12 * length * math.sin(1.1 * t + ph)
            if g > 0.01 and self.hug[i] is not None:
                hc, ht = self.hug[i]()
                tip, ctl = lerp(tip, P3(ht), g), lerp(ctl, P3(hc), g)
            s = np.linspace(0, 1, 14)[:, None]
            main = (1 - s) ** 2 * b + 2 * (1 - s) * s * ctl + s ** 2 * tip
            polys = [main]
            for s0, turn, f in ((0.5, 0.9, 0.38), (0.78, -0.8, 0.26)):
                tl = f * length * (1 - g)
                if tl > 0.03:
                    p = (1 - s0) ** 2 * b + 2 * (1 - s0) * s0 * ctl + s0 ** 2 * tip
                    tg = 2 * (1 - s0) * (ctl - b) + 2 * s0 * (tip - ctl)
                    tg = tg / (np.linalg.norm(tg) + 1e-9)
                    polys.append(np.array([p, p + tl * rot2(tg, turn + 0.3 * math.sin(0.9 * t + ph + s0))]))
            m.set_points(poly_pts(polys))
            m.set_stroke(col, width=6, opacity=a)


class Shimmer(Proc):
    """Soft light pools that drift slowly inside the cell: depth, and motion in every frame."""

    def __init__(self, cell, n=4, z=-56):
        self.cell, self.n, self.a = cell, n, 1.0
        self.layers = [VMobject(stroke_width=0, fill_color="#6FD3F2", fill_opacity=0.02) for _ in range(7)]
        rng = random.Random(21)
        self.motes = []
        while len(self.motes) < 30:                      # fine grains of cytoplasm that drift with the cell
            u, v = rng.uniform(-0.8, 0.8), rng.uniform(-0.8, 0.8)
            if abs(u) ** 2.3 + abs(v) ** 2.3 < 0.6:
                self.motes.append((u, v, rng.uniform(0.018, 0.042), rng.uniform(0, TAU), rng.uniform(0.25, 0.6)))
        self.grain = VMobject(stroke_width=0, fill_color="#BFEFFF", fill_opacity=0.3)
        self.mob = VGroup(*self.layers, self.grain).set_z_index(z)
        self._live()

    def draw(self):
        t, c = now(), self.cell
        cs = [(c.x + 0.30 * c.w * math.sin(0.21 * t + 1.9 * i), c.y + 0.24 * c.h * math.sin(0.17 * t + 2.7 * i + 1),
               0.24 * c.h * (1 + 0.18 * math.sin(0.4 * t + i))) for i in range(self.n)]
        for m, k in zip(self.layers, (1.0, 0.88, 0.76, 0.64, 0.52, 0.4, 0.28)):
            m.set_points(np.concatenate([circ((x, y), r * k) for x, y, r in cs]))
            m.set_fill(opacity=0.02 * self.a * min(1.0, c.a))
        self.grain.set_points(np.concatenate([circ(c.at(u + 0.07 * math.sin(w * t + ph), v + 0.09 * math.sin(0.8 * w * t + 2 * ph)), r)
                                              for u, v, r, ph, w in self.motes]))
        self.grain.set_fill(opacity=0.30 * self.a * min(1.0, c.a))


def gold_badge(r=0.3):
    """The gold '?': the film's mark for 'not settled in science'."""
    halo = Circle(radius=r * 1.4, stroke_width=0, fill_color=GOLD, fill_opacity=0.14)
    c = Circle(radius=r, stroke_color=GOLD, stroke_width=4, fill_color="#33290F", fill_opacity=0.95)
    q = T("?", size=max(28, int(r * 112)), color=GOLD, weight=BOLD).move_to(c)
    g = VGroup(halo, c, q)
    g.h0 = g.height
    return g


def pulse(mob, amp=0.07, period=2.4, phase=0.0):
    """Ambient helper: a slow breathing of size. Reads mob.h0 so a tween can still resize the object."""
    if not hasattr(mob, "h0"):
        mob.h0 = mob.height
    mob.add_updater(lambda m, dt: m.scale_to_fit_height(max(1e-3, m.h0 * (1 + amp * math.sin(TAU * now() / period + phase)))))
    return mob


def set_dim(mob, k):
    """Scale the opacity of a whole label or badge relative to how it was built."""
    for m in mob.family_members_with_points():
        if not hasattr(m, "_bo"):
            m._bo = (m.get_fill_opacity(), m.get_stroke_opacity())
        m.set_fill(opacity=m._bo[0] * k)
        m.set_stroke(opacity=m._bo[1] * k)
    mob._dim = k
    return mob


def dim(mob, k, rt=0.8):
    k0 = getattr(mob, "_dim", 1.0)
    return Tw(lambda a: set_dim(mob, lerp(k0, k, a)), rt)


def rescale(mob, factor, rt=0.8, edge=ORIGIN):
    st = {"s": 1.0}

    def f(a):
        s = lerp(1.0, factor, a)
        mob.scale(s / st["s"], about_point=mob.get_critical_point(edge))
        st["s"] = s
    return Tw(f, rt)


class Nucleus(Proc):
    """The host's nucleus: a solid circle (solid, sdraw) or a dashed one that is still debated (dash, ddraw, q)."""

    def __init__(self, x=0.0, y=0.0, r=1.25, z=-40):
        self.x, self.y, self.r = x, y, r
        self.solid, self.sdraw, self.dash, self.ddraw, self.q, self.a, self.lit = 1.0, 1.0, 0.0, 1.0, 0.0, 1.0, 0.0
        self.col = ManimColor(BLUE)
        self.glow = VMobject(fill_opacity=0)
        self.fill = VMobject(stroke_width=0, fill_color="#2F7FB6")
        self.core = VMobject(stroke_width=0, fill_color="#58C4DD")
        self.line = VMobject(fill_opacity=0)
        self.dashm = VMobject(fill_opacity=0)
        self.badge = gold_badge(0.24)
        self._qa = None
        self.mob = VGroup(self.glow, self.fill, self.core, self.line, self.dashm, self.badge).set_z_index(z)
        self.badge.set_z_index(z + 30)
        self._live()

    def anchor(self, du=0.0, dv=0.0):
        return np.array([self.x + du * self.r, self.y + dv * self.r, 0.0])

    def size(self):
        return self.r

    def draw(self):
        a, r, c = max(0.0, self.a), self.r, np.array([self.x, self.y, 0.0])
        col = interpolate_color(self.col, _WHITE, 0.45 * self.lit) if self.lit > 0.01 else self.col
        sa = a * self.solid
        full = c + r * np.stack([np.cos(np.linspace(0, TAU, 73)), np.sin(np.linspace(0, TAU, 73)), np.zeros(73)], 1)
        th = PI / 2 - np.linspace(0, TAU * max(0.002, self.sdraw), 72)
        arc = c + r * np.stack([np.cos(th), np.sin(th), 0 * th], 1)
        self.line.set_points_as_corners(arc)
        self.line.set_stroke(col, width=4.5, opacity=sa)
        self.glow.set_points_as_corners(arc)
        self.glow.set_stroke(col, width=16 * (1 + 0.5 * self.lit), opacity=sa * 0.10 * (1 + 2 * self.lit))
        fa = sa * max(0.0, (self.sdraw - 0.6) / 0.4)
        self.fill.set_points_as_corners(full)
        self.fill.set_fill(opacity=fa * (0.20 + 0.15 * self.lit))
        self.core.set_points_as_corners((full - c) * 0.6 + c)
        self.core.set_fill(opacity=fa * 0.08)
        nd = 26
        k = self.ddraw * nd
        polys = []
        for i in range(nd):
            f = min(1.0, max(0.0, k - i))
            if f <= 0.02:
                break
            t0 = PI / 2 - TAU * i / nd
            tt = t0 - np.linspace(0, TAU / nd * 0.55 * f, 5)
            polys.append(c + r * np.stack([np.cos(tt), np.sin(tt), 0 * tt], 1))
        if polys and a * self.dash > 0.01:
            self.dashm.set_points(poly_pts(polys))
            self.dashm.set_stroke(col, width=4, opacity=a * self.dash)
        else:
            self.dashm.set_stroke(opacity=0)
        qa = round(a * self.q, 2)
        self.badge.scale_to_fit_height(self.badge.h0 * (1 + 0.07 * math.sin(TAU * now() / 2.4)))
        self.badge.move_to(c + r * np.array([math.cos(0.75), math.sin(0.75), 0]))
        if qa != self._qa:
            self._qa = qa
            self.badge.set_opacity(qa)
            self.badge[0].set_fill(opacity=0.14 * qa)


class Ring(Proc):
    """A closed ring of beads (DNA) that turns slowly and follows its host (a Guest or a Nucleus).
    Never a helix. Beads can be let go (live[i] = False) and animated on their own."""

    def __init__(self, host, angles, color, Rk, brk, dv=-0.03, period=40.0, z=-15, a=1.0, groups=None):
        self.host, self.Rk, self.brk, self.dv, self.period, self.a, self.lit = host, Rk, brk, dv, period, a, 0.0
        self.ang = np.array(angles, dtype=float)
        n = len(self.ang)
        self.n = n
        self.cols = [ManimColor(color)] * n if isinstance(color, (str, ManimColor)) else [ManimColor(c) for c in color]
        self.live = [True] * n
        self.ba, self.hl = np.ones(n), np.zeros(n)
        self.grp = groups or [None] * n          # name of an attribute that scales that bead's opacity
        self.tight, self.ang2, self.Rk2, self.brk2 = 0.0, None, Rk, brk
        self.beads = [VMobject(stroke_width=0, fill_color=c, fill_opacity=1) for c in self.cols]
        self.thread = VMobject(fill_opacity=0)
        self._key = [None] * n
        self.mob = VGroup(self.thread, *self.beads).set_z_index(z)
        self._live()

    def geom(self):
        c = self.host.anchor(0.0, self.dv)
        s = self.host.size()
        return c, lerp(self.Rk, self.Rk2, self.tight) * s, lerp(self.brk, self.brk2, self.tight) * s

    def angle(self, i):
        a = self.ang[i] if self.ang2 is None else lerp(self.ang[i], self.ang2[i], self.tight)
        return a + TAU * now() / self.period

    def pos(self, i):
        c, R, _ = self.geom()
        a = self.angle(i)
        return c + R * np.array([math.cos(a), math.sin(a), 0.0])

    def draw(self):
        c, R, br = self.geom()
        op = max(0.0, self.a) * max(0.0, getattr(self.host, "a", 1.0))
        self.thread.set_points(circ(c, R))
        self.thread.set_stroke(self.cols[0], width=1.5, opacity=0.4 * op)
        for i, b in enumerate(self.beads):
            if not self.live[i]:
                continue
            o = op * self.ba[i] * (getattr(self, self.grp[i], 1.0) if self.grp[i] else 1.0)
            h = max(self.hl[i], self.lit)
            key = (round(o, 2), round(h, 2))
            if o < 0.01:
                if self._key[i] != key:
                    b.set_fill(opacity=0)
                    self._key[i] = key
                continue
            a = self.angle(i)
            b.set_points(circ((c[0] + R * math.cos(a), c[1] + R * math.sin(a)), br * (1 + 0.6 * h)))
            if self._key[i] != key:
                b.set_fill(interpolate_color(self.cols[i], _WHITE, 0.6 * h), opacity=min(1.0, o))
                self._key[i] = key


class Guest(Proc):
    """The guest: a pink rod with a double outline that rounds into a bean and folds its inner line.
    Carries the chain (a row of yellow blocks with a running spark) and, later, 13 pink tiles."""
    NB = 20
    GAPS = [0, 1, 3, 4, 6, 7, 9, 10, 12, 13, 15, 16, 18]

    def __init__(self, x=0.0, y=0.0, L=2.0, H=0.95, bean=0.0, fold=0.0, a=1.0, detail=1.0, chain=0.0, spark=0.0,
                 ang=0.0, dota=0.0, color=PINK, n=140, z=-20, seed=0.0, **extra):
        self.x, self.y, self.L, self.H, self.bean, self.fold, self.a = x, y, L, H, bean, fold, a
        self.detail, self.chain, self.spark, self.ang, self.dota = detail, chain, spark, ang, dota
        self.pinch, self.lit, self.tiles, self.warm, self.sil, self.bob, self.rowglow, self.loop = 0.0, 0.0, 0.0, 0.0, 0.0, 1.0, 0.0, 0.0
        self.surge = -1.0
        self.ph = seed * 1.7
        self.col = ManimColor(color)
        th = np.linspace(0, TAU, n, endpoint=False)
        self.C, self.S = np.cos(th), np.sin(th)
        th2 = np.linspace(0, TAU, 2 * n, endpoint=False)
        self.C2, self.S2 = np.cos(th2), np.sin(th2)
        self.glow = [VMobject(fill_opacity=0) for _ in range(2)]
        self.warmm = VMobject(fill_opacity=0)
        self.body, self.inner = VMobject(), VMobject()
        self.rowg = VMobject(fill_opacity=0)
        self.blocks = VMobject(stroke_width=0, fill_color=YELLOW)
        self.hot = VMobject(stroke_width=0, fill_color="#FFF7C2")
        self.tilem = VMobject(stroke_color="#FFE3EC", stroke_width=1.5, fill_color=PINK)
        self.sp = [VMobject(stroke_width=0, fill_color=c) for c in (YELLOW, "#FFFBE0")]
        self.dot = VMobject(stroke_width=0, fill_color=color)
        self.cx, self.cy, self.ca = x, y, ang
        self.rowc = np.zeros((self.NB, 3))
        self._hid = False
        for k, v in extra.items():
            setattr(self, k, v)
        self.mob = VGroup(*self.glow, self.warmm, self.body, self.inner, self.rowg, self.blocks, self.hot, self.tilem,
                          *self.sp, self.dot).set_z_index(z)
        self._live()

    # geometry helpers used by rings, sparks and scenes
    def center(self):
        return np.array([self.cx, self.cy, 0.0])

    def anchor(self, du=0.0, dv=0.0):
        return self.center() + rot2([du * self.L, (dv + BEND * self.bean) * self.H], self.ca)

    def size(self):
        return self.H

    def rowpoint(self, f):
        """A point on the chain, f in 0..1 from its left end to its right end."""
        f = min(1.0, max(0.0, f)) * (self.NB - 1)
        i = min(self.NB - 2, int(f))
        return lerp(self.rowc[i], self.rowc[i + 1], f - i)

    def gappos(self, k):
        j = self.GAPS[k]
        return 0.5 * (self.rowc[j] + self.rowc[j + 1])

    def draw(self):
        t, a = now(), max(0.0, self.a)
        H, L = self.H * (1 + 0.05 * self.lit), self.L * (1 + 0.05 * self.lit)
        ang = self.ang + self.bob * 0.035 * math.sin(0.55 * t + self.ph)
        cx = self.x + self.bob * 0.03 * H * math.sin(0.7 * t + 1.3 * self.ph) + self.loop * 0.34 * math.cos(0.8 * t)
        cy = self.y + self.bob * 0.035 * H * math.sin(0.9 * t + self.ph) + self.loop * 0.2 * math.sin(0.8 * t)
        self.cx, self.cy, self.ca = cx, cy, ang
        # the chain's geometry is always known (sparks start from it even when it is not drawn)
        m = 0.075 * H
        Li, Hi = L - 2 * m, H - 2 * m
        nexp = 2.9 - 0.5 * self.bean
        us = np.linspace(-0.74, 0.74, self.NB)
        pitch = 0.5 * Li * 1.48 / (self.NB - 1)
        bw, bh = 0.55 * pitch, 0.085 * H
        ry = -0.5 * Hi * (1 - np.abs(us) ** nexp) ** (1 / nexp) + self.bean * BEND * H * (1 - 2 * us ** 2) + 0.03 * H + bh / 2
        self.rowc = place(np.stack([0.5 * Li * us, ry, 0 * us], 1), cx, cy, ang)
        if a < 0.004:
            if not self._hid:
                for mob in self.mob:
                    mob.set_stroke(opacity=0)
                    mob.set_fill(opacity=0)
                self._hid = True
            return
        self._hid = False
        col = interpolate_color(self.col, _WHITE, 0.4 * self.lit) if self.lit > 0.01 else self.col
        out = closed(place(bean_pts(self.C, self.S, L, H, H, self.bean, self.pinch), cx, cy, ang))
        sw = min(4.5, 2.2 + 1.1 * H)
        for mob, (wd, op) in zip(self.glow, [(18, .05), (9, .09)]):
            mob.set_points_as_corners(out)
            mob.set_stroke(col, width=wd * sw / 4.5 * (1 + 0.6 * self.lit), opacity=min(1, a * op * (1 + 2.5 * self.lit)))
        self.warmm.set_points_as_corners(out)
        self.warmm.set_stroke(YELLOW, width=12, opacity=a * 0.25 * self.warm)
        self.body.set_points_as_corners(out)
        self.body.set_stroke(col, width=sw, opacity=a)
        self.body.set_fill(col, opacity=min(1, a * (0.14 + 0.36 * self.sil + 0.25 * self.lit)))
        da = a * self.detail
        if da > 0.01:
            self.inner.set_points_as_corners(closed(place(bean_pts(self.C2, self.S2, Li, Hi, H, self.bean, self.pinch, self.fold), cx, cy, ang)))
            self.inner.set_stroke(col, width=0.7 * sw, opacity=da)
            self.inner.set_fill(col, opacity=da * 0.10)
        else:
            self.inner.set_stroke(opacity=0)
            self.inner.set_fill(opacity=0)
        ca = a * self.chain
        if ca > 0.01:
            ex, ey = rot2([bw / 2, 0], ang), rot2([0, bh / 2], ang)
            box = lambda c, kx=1.0, ky=1.0: np.array([c - ex * kx - ey * ky, c + ex * kx - ey * ky, c + ex * kx + ey * ky, c - ex * kx + ey * ky, c - ex * kx - ey * ky])
            self.blocks.set_points(poly_pts([box(c) for c in self.rowc]))
            self.blocks.set_fill(interpolate_color(ManimColor(YELLOW), ManimColor("#FFF7C2"), 0.6 * self.rowglow), opacity=ca * (0.85 + 0.15 * self.rowglow))
            self.rowg.set_points_as_corners(self.rowc)
            self.rowg.set_stroke(YELLOW, width=6 + 60 * bh, opacity=ca * 0.28 * self.rowglow)
            f = ((t / 2.2 + 0.13 * self.ph) % 1.0) if self.surge < 0 else self.surge
            sa = ca * (self.spark if self.surge < 0 else 1.0)
            if sa > 0.01:
                j = f * (self.NB - 1)
                near = [i for i in range(self.NB) if abs(i - j) < 1.3]
                self.hot.set_points(poly_pts([box(self.rowc[i], 1.15, 1.15) for i in near]))
                self.hot.set_fill(opacity=sa)
                p = self.rowpoint(f)
                k = 1.0 if self.surge < 0 else 1.8
                self.sp[0].set_points(circ(p, 1.1 * bh * k))
                self.sp[0].set_fill(opacity=0.35 * sa)
                self.sp[1].set_points(circ(p, 0.42 * bh * k))
                self.sp[1].set_fill(opacity=sa)
            else:
                self.hot.set_fill(opacity=0)
                self.sp[0].set_fill(opacity=0)
                self.sp[1].set_fill(opacity=0)
            nt = int(round(self.tiles))
            if nt > 0:
                self.tilem.set_points(poly_pts([box(self.gappos(k), 0.58, 0.9) for k in range(min(13, nt))]))
                self.tilem.set_fill(opacity=ca)
                self.tilem.set_stroke(opacity=ca)
            else:
                self.tilem.set_fill(opacity=0)
                self.tilem.set_stroke(opacity=0)
        else:
            for mob in (self.blocks, self.hot, self.tilem, self.sp[0], self.sp[1]):
                mob.set_fill(opacity=0)
            self.tilem.set_stroke(opacity=0)
            self.rowg.set_stroke(opacity=0)
        if a * self.dota > 0.01:
            self.dot.set_points(circ(self.anchor(0, -0.5 * BEND * self.bean), 0.13 * H))
            self.dot.set_fill(opacity=a * self.dota)
        else:
            self.dot.set_fill(opacity=0)


def split(p, c):
    """Replace a fully pinched bean p by its two halves p and c (the same picture), ready to drift apart."""
    d = rot2([p.L / 4, 0], p.ang)
    for k in ("H", "bean", "fold", "a", "detail", "chain", "spark", "ang", "sil", "dota", "warm", "rowglow"):
        setattr(c, k, getattr(p, k))
    c.L = p.L = p.L / 2 * 1.04
    c.x, c.y, p.x, p.y = p.x + d[0], p.y + d[1], p.x - d[0], p.y - d[1]
    p.pinch = c.pinch = 0.0


def rod_outline(x, y, L, H, ang=0.0, color="#FFE3EC", width=5, n=100):
    """The ancient guest as a bright outline (used when the film says 'descend from that guest')."""
    th = np.linspace(0, TAU, n, endpoint=False)
    pts = closed(place(bean_pts(np.cos(th), np.sin(th), L, H), x, y, ang))
    inner = closed(place(bean_pts(np.cos(th), np.sin(th), L - 0.16 * H, H * 0.84), x, y, ang))
    g = VGroup(VMobject(fill_opacity=0).set_points_as_corners(pts).set_stroke(PINK, width=width * 4, opacity=0.18),
               VMobject(fill_opacity=0).set_points_as_corners(pts).set_stroke(color, width=width),
               VMobject(fill_opacity=0).set_points_as_corners(inner).set_stroke(color, width=width * 0.55))
    return g.set_z_index(12)


def flicker(mob, rt=1.1):
    """The outline flickers on, holds and melts away."""
    base = [(m.get_stroke_opacity(), m) for m in mob]

    def f(a):
        env = min(1.0, a / 0.2) * min(1.0, (1 - a) / 0.35)
        k = env * (0.72 + 0.28 * math.sin(38 * a))
        for o, m in base:
            m.set_stroke(opacity=o * max(0.0, k))
    return Tw(f, rt, linear)


def star(r=0.12, color=YELLOW):
    halo = Circle(radius=r * 1.9, stroke_width=0, fill_color=color, fill_opacity=0.18)
    s = Star(n=4, outer_radius=r, inner_radius=r * 0.38, stroke_width=0, fill_color="#FFF3B0", fill_opacity=1)
    return VGroup(halo, s)


def o2_token(r=0.36):
    halo = Circle(radius=r * 1.45, stroke_width=0, fill_color=RED, fill_opacity=0.16)
    c = Circle(radius=r, stroke_color="#FFC2BB", stroke_width=2, fill_color=RED, fill_opacity=0.95)
    t = T("O₂", size=28, color="#2A0E0C", weight=BOLD).move_to(c)
    return VGroup(halo, c, t).set_z_index(10)


def h2_bubble(r=0.36):
    halo = Circle(radius=r * 1.4, stroke_width=0, fill_color=TEAL, fill_opacity=0.12)
    c = Circle(radius=r, stroke_color=TEAL, stroke_width=3.5, fill_color="#0E3A40", fill_opacity=0.85)
    t = T("H₂", size=28, color=TEAL, weight=BOLD).move_to(c)
    return VGroup(halo, c, t).set_z_index(10)


class Sparks(Proc):
    """Yellow sparks that rise from the chain. spread 0..1 sends them through the whole cell;
    toward 0..1 bends them to self.target (the nucleus). Two of them carry the word ATP when lab = 1."""

    def __init__(self, guest, cell, n=12, period=2.8, labels=2, seed=3, z=-6):
        rng = random.Random(seed)
        self.g, self.cell, self.n, self.P = guest, cell, n, period
        self.a, self.spread, self.toward, self.lab, self.rate = 0.0, 0.0, 0.0, 0.0, 1.0
        self.target = np.zeros(3)
        # odd sparks leave the left end of the row and stay left of the bead ring; even ones the right end, and stay right
        self.par = [(rng.uniform(0.03, 0.27), rng.uniform(-0.85, 0.05), rng.uniform(-0.8, 0.8), rng.uniform(0, TAU)) if i % 2 else
                    (rng.uniform(0.73, 0.97), rng.uniform(0.6, 0.9), rng.uniform(-0.8, 0.8), rng.uniform(0, TAU)) for i in range(n)]
        for i, (f, uc, vc) in enumerate([(0.82, 0.8, 0.62), (0.18, -0.12, 0.78)][:labels]):      # the two that carry the word ATP
            self.par[i] = (f, uc, vc, self.par[i][3])
        self.stars = [star(0.11) for _ in range(n)]
        self.txt = [T("ATP", size=28, color=YELLOW, weight=BOLD) for _ in range(labels)]
        self._k = [None] * n
        self._h = [None] * n
        self._kt = [None] * labels
        self.mob = VGroup(*self.stars, *self.txt).set_z_index(z)
        for m in self.mob:
            m.set_opacity(0)
        self._live()

    def draw(self):
        t, g = now(), self.g
        for i, s in enumerate(self.stars):
            f, uc, vc, ph = self.par[i]
            age = ((t / self.P + i / self.n) % 1.0)
            env = min(1.0, age / 0.12) * min(1.0, (1 - age) / 0.3)
            o = round(self.a * max(0.0, g.a) * env * (1.0 if i / self.n < self.rate else 0.0), 2)
            tx = self.txt[i] if i < len(self.txt) else None
            if o < 0.01:
                if self._k[i] != 0:
                    s.set_opacity(0)
                    self._k[i] = 0
                if tx is not None and self._kt[i] != 0:
                    tx.set_opacity(0)
                    self._kt[i] = 0
                continue
            side = 1.0 if f > 0.5 else -1.0
            o0 = g.rowpoint(f) + rot2([0.0, 0.11 * g.H], g.ca)             # born just above the row, never on its tiles
            e = age ** 0.8
            rise = 0.20 + 0.42 * g.H
            up = np.array([0.10 * rise * math.sin(ph + 2.2 * age) + side * 0.07 * g.L, rise, 0.0]) * e      # up, and away from the ring
            tgt = lerp(self.cell.at(uc, vc), self.target + np.array([0.3 * math.cos(ph), 0.3 * math.sin(ph), 0]), self.toward)
            p = o0 + up * (1 - self.spread) + (tgt - o0) * self.spread * e
            hs = round(min(0.42, max(0.2, 0.15 * g.H)), 2)
            if self._h[i] != hs:
                s.scale_to_fit_height(hs)
                self._h[i] = hs
            s.move_to(p)
            if self._k[i] != o:
                s[0].set_fill(opacity=0.18 * o)
                s[1].set_fill(opacity=o)
                self._k[i] = o
            if tx is not None:
                # the word shows only once the spark is clear of the row (and, when spreading, of the bean);
                # the one from the right end would cross the whole bean to get out, so it stays a plain spark then
                ot = round(o * self.lab * min(1.0, max(0.0, (age - lerp(0.38, 0.62, self.spread)) / 0.12)) * (1.0 if side < 0 else 1.0 - self.spread), 2)
                tx.move_to(p + np.array([side * 0.56, 0.02, 0]))
                if self._kt[i] != ot:
                    tx.set_opacity(ot)
                    self._kt[i] = ot


class MiniSparks(Proc):
    """Two small sparks rising from each of many small beans (every mitochondrion is making ATP)."""

    def __init__(self, beans, per=2, period=1.9, z=-6):
        self.beans, self.per, self.P, self.a = beans, per, period, 0.0
        self.m = VMobject(stroke_width=0, fill_color="#FFF3B0")
        self.mob = VGroup(self.m).set_z_index(z)
        self._live()

    def draw(self):
        t = now()
        cs = []
        for j, b in enumerate(self.beans):
            o = self.a * b.a * b.warm
            if o < 0.05:
                continue
            for k in range(self.per):
                age = (t / self.P + 0.37 * j + k / self.per) % 1.0
                r = 0.07 * math.sin(PI * age) * o
                if r > 0.01:
                    cs.append(circ((b.cx + (k - 0.5) * 0.3 * b.L + 0.08 * math.sin(5 * age + j), b.cy + 0.3 * b.H + 0.75 * age), r))
        if cs:
            self.m.set_points(np.concatenate(cs))
            self.m.set_fill(opacity=0.95)
        else:
            self.m.set_fill(opacity=0)


class O2Stream(Proc):
    """Oxygen arriving at the chain: red O2 tokens come in from the right, land on the yellow row,
    and every landing pops a yellow ATP spark. A function of film time, so it carries across a cut."""

    def __init__(self, guest, t0, n=6, gap=0.6, travel=1.7, x_from=None, z=-3):
        self.g, self.t0, self.n, self.gap, self.travel, self.a = guest, t0, n, gap, travel, 1.0
        self.x_from = (config.frame_width / 2 + 0.6) if x_from is None else x_from
        self.stop = None                   # film time after which no new token sets out
        self.tok = [o2_token(0.34) for _ in range(n)]
        self.pop = [star(0.15) for _ in range(n)]
        self.txt = [T("ATP", size=28, color=YELLOW, weight=BOLD) for _ in range(n)]
        self.h0 = self.tok[0].height
        self.mob = VGroup(*self.tok, *self.pop, *self.txt).set_z_index(z)
        for m in self.mob:
            m.set_opacity(0)
        self._ko, self._kp, self._kt = [None] * n, [None] * n, [None] * n
        self._live()

    def draw(self):
        t = now() - self.t0
        P = self.n * self.gap
        for i in range(self.n):
            tk, pp, tx = self.tok[i], self.pop[i], self.txt[i]
            lt = t - i * self.gap
            cyc = math.floor(lt / P) if lt >= 0 else -1
            age = lt - cyc * P if lt >= 0 else -1.0
            if self.stop is not None and self.t0 + i * self.gap + cyc * P > self.stop:
                age = -1.0
            f = 0.10 + 0.28 * ((0.37 * (i + 1) + 0.23 * cyc) % 1.0) + (0.52 if (i + cyc) % 2 else 0.0)
            land = self.g.rowpoint(f)
            y0 = self.g.cy + (((i * 0.61 + cyc * 0.29) % 1.0) - 0.35) * 3.2
            # the token
            o = 0.0
            if 0 <= age < self.travel:
                s = age / self.travel
                e = smooth(s)
                start = np.array([self.x_from, y0, 0.0])
                ctl = np.array([lerp(self.x_from, land[0], 0.45), y0 + 0.5, 0.0])
                p = (1 - e) ** 2 * start + 2 * (1 - e) * e * ctl + e ** 2 * land
                k = 1.0 - 0.72 * max(0.0, (s - 0.6) / 0.4)
                o = round(self.a * min(1.0, (1 - s) / 0.1), 2)
                tk.scale_to_fit_height(self.h0 * k)
                tk.move_to(p)
            if self._ko[i] != o:
                tk.set_opacity(o)
                tk[0].set_fill(opacity=0.16 * o)
                self._ko[i] = o
            # the spark that pops where it landed
            po = 0.0
            if self.travel <= age < self.travel + 1.5:
                s = (age - self.travel) / 1.5
                po = round(self.a * min(1.0, s / 0.08) * min(1.0, (1 - s) / 0.3), 2)
                side = 1.0 if f > 0.5 else -1.0
                e = s ** 0.75
                q = land + np.array([side * 0.52 * self.g.L * e, 0.62 * self.g.H * math.sin(0.5 * PI * e) + 0.12, 0.0])
                pp.move_to(q)
                tx.move_to(q + np.array([side * 0.55, 0.0, 0.0]))
                to = round(po * min(1.0, max(0.0, (s - 0.5) / 0.15)), 2)
                if self._kt[i] != to:
                    tx.set_opacity(to)
                    self._kt[i] = to
            elif self._kt[i] != 0:
                tx.set_opacity(0)
                self._kt[i] = 0
            if self._kp[i] != po:
                pp[0].set_fill(opacity=0.18 * po)
                pp[1].set_fill(opacity=po)
                self._kp[i] = po


TODAY, TICKX, KBAND, K18, SCRUB_Y = 5.0, -1.3, -2.7, 4.0, -2.85


class Scrubber(Proc):
    """The time scrubber: 'long ago' ... 'today', a knob, a gold band ('when? uncertain') and one fossil
    tick. Tagged 'not to scale'. The knob creeps a little whenever it is not being moved on purpose.
    words 1..0 fades everything but the bare line, its end words and the knob (the gold band and its
    badge, the fossil tick, 'not to scale'): used while the knob rests at 'today' and the picture is
    about something else."""

    def __init__(self, x0=-4.45, x1=TODAY, y=-2.85, band=(-4.2, -0.4), tickx=TICKX, size=28, z=-5):
        self.x0, self.x1, self.y, self.b0, self.b1, self.tickx = x0, x1, y, band[0], band[1], tickx
        self.a, self.grow, self.knob, self.band, self.tick, self.words = 1.0, 1.0, x1, 0.0, 0.0, 1.0
        self.fn = None
        self.line = VMobject(fill_opacity=0)
        self.bandm = VMobject(stroke_width=0, fill_color=GOLD)
        self.bandl = VMobject(fill_opacity=0)
        self.tickm = VMobject(fill_opacity=0)
        self.kh = VMobject(stroke_width=0, fill_color=TEXT)
        self.kn = VMobject(stroke_color=BG, stroke_width=3, fill_color=TEXT)
        self.ago = T("long ago", size=size).next_to([x0, y, 0], LEFT, buff=0.22)
        self.today = T("today", size=size).next_to([x1, y, 0], RIGHT, buff=0.42)
        self.nts = T("not to scale", size=size).move_to([lerp(x0, x1, 0.86), y - 0.48, 0])
        self.bq = T("when? uncertain", size=size, color=GOLD).move_to([0.5 * (band[0] + band[1]) + 0.25, y - 0.48, 0])
        self.bb = gold_badge(0.19).next_to(self.bq, LEFT, buff=0.14)
        self._k = None
        self.mob = VGroup(self.bandm, self.bandl, self.line, self.tickm, self.kh, self.kn, self.ago, self.today, self.nts,
                          self.bq, self.bb).set_z_index(z)
        self._live()

    def draw(self):
        t, a, y = now(), max(0.0, self.a), self.y
        wa = a * max(0.0, min(1.0, self.words))
        if self.fn is not None:
            self.knob = self.fn()
        xe = lerp(self.x0, self.x1, self.grow)
        self.line.set_points_as_corners([[self.x0, y, 0], [xe, y, 0]])
        self.line.set_stroke(TEXT, width=3.5, opacity=a * 0.9)
        if self.band > 0.01 and wa > 0.01:
            c, hw = 0.5 * (self.b0 + self.b1), 0.5 * (self.b1 - self.b0) * min(1.0, self.band * 1.6)
            sh = 0.5 + 0.5 * math.sin(1.3 * t)
            self.bandm.set_points_as_corners([[c - hw, y - 0.17, 0], [c + hw, y - 0.17, 0], [c + hw, y + 0.17, 0], [c - hw, y + 0.17, 0], [c - hw, y - 0.17, 0]])
            self.bandm.set_fill(opacity=wa * (0.26 + 0.10 * sh))
            self.bandl.set_points(poly_pts([[[c - hw, y - 0.17, 0], [c + hw, y - 0.17, 0]], [[c - hw, y + 0.17, 0], [c + hw, y + 0.17, 0]]]))
            self.bandl.set_stroke(GOLD, width=2, opacity=wa * 0.9)
        else:
            self.bandm.set_fill(opacity=0)
            self.bandl.set_stroke(opacity=0)
        self.tickm.set_points_as_corners([[self.tickx, y - 0.26 * self.tick, 0], [self.tickx, y + 0.26 * self.tick, 0]])
        self.tickm.set_stroke(TEXT, width=4, opacity=wa * min(1.0, 3 * self.tick))
        kx = min(self.knob, xe) + 0.07 * math.sin(0.45 * t)
        ka = a * min(1.0, self.grow * 3)
        self.kh.set_points(circ((kx, y), 0.30 * (1 + 0.12 * math.sin(1.7 * t))))
        self.kh.set_fill(opacity=0.20 * ka)
        self.kn.set_points(circ((kx, y), 0.16))
        self.kn.set_fill(opacity=ka)
        self.kn.set_stroke(opacity=ka)
        ba = max(0.0, min(1.0, self.band * 2 - 1))
        key = (round(a, 2), round(self.grow, 2), round(ba, 2), round(wa, 2))
        if key != self._k:
            self._k = key
            self.ago.set_opacity(a * min(1.0, self.grow * 4))
            self.today.set_opacity(a * max(0.0, min(1.0, self.grow * 4 - 3)))
            self.nts.set_opacity(wa * max(0.0, min(1.0, self.grow * 4 - 3)))
            self.bq.set_opacity(wa * ba)
            self.bb.set_opacity(wa * ba)
            self.bb[0].set_fill(opacity=0.14 * wa * ba)


# ───────────────────────────── presets: the world's named states ─────────────────────────────
def mix(P, **over):
    out = {k: dict(v) for k, v in P.items()}
    for k, v in over.items():
        out.setdefault(k, {}).update(v)
    return out


def zoomed(P, k, c0, c1, **over):
    """The same world pushed in (or pulled back) by k, with point c0 carried to c1."""
    out = {}
    for name, d in P.items():
        d = dict(d)
        if "x" in d and "y" in d:
            d["x"], d["y"] = c1[0] + (d["x"] - c0[0]) * k, c1[1] + (d["y"] - c0[1]) * k
        for s in ("w", "h", "r", "L", "H"):
            if s in d:
                d[s] = d[s] * k
        out[name] = d
    return mix(out, **over)


_rng = random.Random(40)
_idx = list(range(40))
_rng.shuffle(_idx)
LOST, MOVED, KEPT = sorted(_idx[:15]), sorted(_idx[15:27]), sorted(_idx[27:])        # 40 = 15 + 12 + 13 (schematic)
A40 = np.array([TAU * i / 40 for i in range(40)])
KEPT_A = A40[KEPT]
C13 = float(np.mean(KEPT_A - TAU * np.arange(13) / 13))
A13 = TAU * np.arange(13) / 13 + C13
R40K, B40K, R13K, B13K, RFK, BFK = 0.25, 0.0165, 0.19, 0.031, 0.24, 0.024
PINK_SLOTS = [0, 1, 3, 4, 6, 7, 9, 10, 12, 13, 15, 16]           # half-steps of the nucleus ring that take a pink bead
BLUE_X = [2, 5, 8, 11, 14, 17]                                   # half-steps that take an extra blue bead in s20

MOD = dict(    # the opening frame: the modern cell
    cell=dict(x=0.0, y=-0.35, w=11.6, h=5.7, arm=0.0, a=1.0, warm=0.0, sq=2.3, wob=1.0),
    nuc=dict(x=-3.4, y=-0.15, r=1.25, solid=1.0, sdraw=1.0, dash=0.0, ddraw=1.0, q=0.0, a=1.0),
    nring=dict(a=1.0, Rk=0.62, pk=0.0, bx=0.0),
    g=dict(x=2.0, y=-0.3, L=4.6, H=2.4, bean=1.0, fold=1.0, a=1.0, detail=1.0, chain=1.0, spark=1.0, ang=0.0, sil=0.0,
           dota=0.0, tiles=0.0, warm=0.0, rowglow=0.0, loop=0.0),
    r13=dict(a=1.0), rfull=dict(a=0.0), rk=dict(a=0.0, tight=0.0),
    s0=dict(x=0.3, y=1.72, L=1.25, H=0.62, a=1.0, ang=0.12),
    s1=dict(x=3.6, y=1.45, L=1.25, H=0.62, a=1.0, ang=-0.2),
    s2=dict(x=3.6, y=1.45, L=1.25, H=0.62, a=0.0, ang=-0.2),
    scrub=dict(a=0.0, grow=1.0, knob=TODAY, band=0.0, tick=0.0, words=1.0),
    sparks=dict(a=0.0, spread=0.0, toward=0.0, lab=0.0),
)
MOD3 = mix(MOD, s1=dict(x=3.15, y=1.6, L=1.0, H=0.56, ang=-0.1), s2=dict(x=4.3, y=1.15, L=1.0, H=0.56, a=1.0, ang=-0.5))
UP3 = zoomed(MOD3, 0.8, (0, -0.35), (0, 0.5), scrub=dict(a=1.0, knob=TICKX, tick=1.0))
_GONE = dict(x=5.0, y=0.45, L=0.6, H=0.3, a=0.0)
ANC = mix(UP3,                                                    # two strangers, far apart
          cell=dict(x=-2.4, y=0.3, w=6.8, h=4.6, arm=1.0),
          nuc=dict(x=-3.5, y=0.25, r=1.05, solid=0.0, dash=1.0, ddraw=0.0, q=0.0),
          g=dict(x=5.0, y=0.45, L=2.6, H=1.25, bean=0.0, fold=0.0, a=0.35, chain=0.0, spark=0.0),
          r13=dict(a=0.0), rfull=dict(a=1.0), s0=_GONE, s1=_GONE, s2=_GONE,
          scrub=dict(knob=KBAND, band=1.0, tick=1.0))
ANC2 = mix(ANC, nuc=dict(ddraw=1.0, q=1.0))
GIN = mix(ANC2, g=dict(x=4.0, y=0.35, a=1.0, chain=1.0, spark=1.0), sparks=dict(a=0.7))
# s05: pushed in on the guest (about 5 x 2.4), the host cropped at the left edge; the scrubber rests while we look closely
G5 = zoomed(GIN, 1.9, (4.0, 0.35), (2.6, 0.0), cell=dict(arm_len=1.9), scrub=dict(a=0.0))
ENC = mix(GIN, cell=dict(x=-0.2, y=0.2, w=8.0, h=4.9), nuc=dict(x=-1.9, y=0.2, r=1.1), g=dict(x=1.3, y=0.25),
          sparks=dict(a=0.0))                                     # the guest is inside the host, and the pair is centred
MRG = mix(ENC, cell=dict(x=0.0, y=0.3, w=10.4, h=4.9, arm=0.3), nuc=dict(x=-3.2, y=0.3, r=1.15), g=dict(x=1.7, y=0.3, L=3.2, H=1.5))
PUSH = mix(MRG, cell=dict(x=0.0, y=0.0, w=13.9, h=7.72, arm=0.0, a=0.75, sq=7.0, wob=0.3), nuc=dict(x=-5.5, a=0.0),
           g=dict(x=-4.55, y=0.4, L=3.3, H=1.85, bean=1.0, fold=0.7, detail=0.0, chain=0.0, spark=0.0, sil=1.0),
           rfull=dict(a=0.0), scrub=dict(knob=TODAY, words=0.0))
CLUE4 = mix(PUSH, g=dict(x=-5.45, y=0.4, L=1.65, H=1.3, detail=1.0, sil=0.25), rfull=dict(a=1.0))
MEET, ROOT = (0.0, -0.35), (0.0, -2.2)
TIPS = [(-5.15, 2.2), (-3.25, 2.2), (-0.95, 2.2), (0.95, 2.2), (3.25, 2.2), (5.15, 2.2)]
PAIRS = [(-4.2, 1.0), (0.0, 1.0), (4.2, 1.0)]
TREE = mix(PUSH, cell=dict(a=0.5), g=dict(x=MEET[0], y=MEET[1], L=3.0, H=1.4, bean=0.0, fold=0.0, detail=1.0, chain=1.0, spark=1.0, sil=0.0),
           rfull=dict(a=1.0))
IDEA = mix(TREE, cell=dict(x=0.0, y=0.3, w=10.4, h=4.9, a=1.0, sq=2.3, wob=1.0), nuc=dict(x=-3.65, y=0.3, r=1.0, a=1.0), g=dict(x=0.4, y=0.9, L=4.4, H=2.2))      # the host keeps its bead ring, dashed circle and "?"
WHY = mix(IDEA, cell=dict(x=-1.6, y=0.2, w=6.8, h=4.6, arm=1.0), nuc=dict(x=-2.7, y=0.15, r=1.05, a=1.0, dash=1.0, ddraw=1.0, q=1.0, solid=0.0),
          g=dict(x=3.1, y=0.2, L=2.6, H=1.25), scrub=dict(knob=KBAND, words=1.0))
GEN0 = mix(WHY, cell=dict(x=0.0, y=0.3, w=10.4, h=4.9, arm=0.0), nuc=dict(x=-3.3, y=0.3, r=1.15), g=dict(x=2.3, y=0.3, L=5.0, H=2.5),
           rfull=dict(a=0.0))
GEN1 = mix(GEN0, nuc=dict(solid=1.0, sdraw=1.0, dash=0.0, q=0.0), nring=dict(pk=1.0), g=dict(bean=1.0, H=2.7, fold=0.6),
           rk=dict(a=1.0), scrub=dict(knob=K18, words=0.0))
ZOOM = zoomed(GEN1, 1.45, (2.3, 0.3), (0.5, 0.2), g=dict(tiles=13.0), rk=dict(tight=1.0), scrub=dict(knob=TODAY),
              sparks=dict(a=1.0, lab=1.0), cell=dict(x=0.0, y=0.0, w=13.9, h=7.72, sq=7.0, a=0.75, wob=0.3), nuc=dict(a=0.0))
PAY = mix(GEN1, g=dict(tiles=13.0), rk=dict(tight=1.0), scrub=dict(knob=TODAY), sparks=dict(a=1.0, lab=1.0))
MANY = mix(PAY, cell=dict(x=0.0, y=0.2, w=12.4, h=5.1, warm=0.6), nuc=dict(r=1.5), nring=dict(Rk=0.72, bx=1.0),
           g=dict(detail=0.0, chain=0.0, spark=0.0, dota=1.0, warm=1.0), rk=dict(a=0.0), sparks=dict(a=1.0, spread=1.0, toward=0.6, lab=0.0),
           s2=dict(a=0.0))
MODF = mix(MOD, nring=dict(pk=1.0), g=dict(tiles=13.0))           # the opening frame again, seen with new eyes

# the 16 mitochondria of s20: index bits pick bottom/top, right/left, then a place in that quarter
_Q = {(0, 0): [(2.6, -0.3), (3.8, -1.15), (4.25, -0.2), (2.4, -1.4)], (1, 0): [(2.75, 0.75), (3.9, 1.55), (4.2, 0.75), (2.5, 1.85)],
      (0, 1): [(1.2, -0.35), (-0.35, -0.3), (0.95, -1.45), (-0.5, -1.4)], (1, 1): [(1.25, 0.75), (-0.3, 0.8), (1.0, 1.9), (-0.5, 1.85)]}
_jr = random.Random(16)
P16 = [(x + _jr.uniform(-0.13, 0.13), y + _jr.uniform(-0.1, 0.1)) for x, y in [_Q[(i & 1, (i >> 1) & 1)][i >> 2] for i in range(16)]]
A16 = [_jr.uniform(-0.6, 0.6) for _ in range(16)]
STAGE = [(5.0, 2.7), (3.3, 1.75), (2.3, 1.2), (1.6, 0.82), (1.1, 0.56)]


def stage_pos(j, k):
    """Where bean j sits when there are 2**k beans: the middle of its descendants."""
    m = [P16[i] for i in range(16) if i % (2 ** k) == j]
    return (sum(p[0] for p in m) / len(m), sum(p[1] for p in m) / len(m))


class World:
    """Builds the carried world in a named state and adds it to the scene."""

    def __init__(self, scene, preset):
        self.sc = scene
        scene.add(make_backdrop())
        start_clock(scene)
        self.specks = Specks()
        self.cell = Cell()
        self.shim = Shimmer(self.cell)
        self.nuc = Nucleus()
        half = TAU / 36
        angs = [TAU * i / 18 for i in range(18)] + [TAU * k / 18 + half for k in PINK_SLOTS] + [TAU * k / 18 + half for k in BLUE_X]
        self.nring = Ring(self.nuc, angs, [BLUE] * 18 + [PINK] * 12 + [BLUE] * 6, Rk=0.62, brk=0.047, dv=0.0, z=-38,
                          groups=[None] * 18 + ["pk"] * 12 + ["bx"] * 6)
        self.nring.pk, self.nring.bx = 0.0, 0.0
        self.g = Guest(n=150)
        self.r13 = Ring(self.g, A13, PINK, R13K, B13K)
        self.rfull = Ring(self.g, [TAU * i / 26 for i in range(26)], PINK, RFK, BFK)
        self.rk = Ring(self.g, KEPT_A, PINK, R40K, B40K)
        self.rk.ang2, self.rk.Rk2, self.rk.brk2 = A13, R13K, B13K
        self.small = [Guest(bean=1.0, detail=0.0, dota=1.0, n=70, seed=i + 1) for i in range(3)]
        self.sparks = Sparks(self.g, self.cell)
        self.scrub = Scrubber()
        self.objs = dict(cell=self.cell, nuc=self.nuc, nring=self.nring, g=self.g, r13=self.r13, rfull=self.rfull, rk=self.rk,
                         s0=self.small[0], s1=self.small[1], s2=self.small[2], scrub=self.scrub, sparks=self.sparks)
        self.set(preset)
        self.veil_a = 0.0
        self.veil = Rectangle(width=FW + 1, height=FH + 1, stroke_width=0, fill_color=BG, fill_opacity=0).set_z_index(-1)
        self.veil.add_updater(lambda m, dt: m.set_fill(opacity=self.veil_a() if callable(self.veil_a) else self.veil_a))
        for o in (self.specks, self.cell, self.shim, self.nuc, self.nring, self.g, self.r13, self.rfull, self.rk, *self.small,
                  self.sparks, self.scrub):
            o.draw()
            scene.add(o.mob)
        scene.add(self.veil)

    def set(self, preset):
        for k, d in preset.items():
            self.objs[k].set(**d)
        return self

    def to(self, preset, rt=1.5, rate=smooth, only=None, skip=()):
        return [self.objs[k].tw(rt, rate, **d) for k, d in preset.items() if (only is None or k in only) and k not in skip]

    def cradle(self):
        """Arms 0 and 1 reach round the guest; as it is drawn inside they close behind it."""
        c, g = self.cell, self.g
        edge = lambda: c.x + 0.5 * c.w

        def hug(sign):
            def f():
                e = min(1.0, max(0.0, (edge() + 0.9 - g.cx) / 2.4))
                gc = g.center()
                tip = lerp(gc + np.array([0.52 * g.L, sign * 0.22 * g.H, 0]), np.array([edge() + 0.2, c.y + sign * 0.03, 0]), e)
                ctl = lerp(gc + np.array([-0.1 * g.L, sign * (0.66 * g.H + 0.1), 0]), np.array([edge() + 0.35, c.y + sign * 0.7, 0]), e)
                return ctl, tip
            return f
        c.hug[0], c.hug[1] = hug(1), hug(-1)


# ───────────────────────────── labels ─────────────────────────────
def label(text, size=34, color=TEXT, pos=(0, 0), weight=MEDIUM, **kw):
    return T(text, size=size, color=color, weight=weight, **kw).move_to(P3(pos)).set_z_index(20)


def label2(lines, size=28, color=TEXT, pos=(0, 0), weight=MEDIUM, buff=0.13):
    """A short label on two centred lines (for names too long for one line at a readable size)."""
    g = VGroup(*[T(t, size=size, color=color, weight=weight) for t in lines]).arrange(DOWN, buff=buff)
    return g.move_to(P3(pos)).set_z_index(20)


def card(text, size=44, color=TEXT, x=0.0, y=CARD_Y, **kw):
    return T(text, size=size, color=color, weight=SEMIBOLD, **kw).move_to([x, y, 0]).set_z_index(22)


Q_HOOK = "A separate living thing?"
P_MITO, P_NUCL, P_OWN = (2.0, -1.85), (-2.1, -1.85), (2.65, -1.85)      # one line; the nucleus label clear of the cell outline, and a clear gap before the bean's label


class StageMixin:
    def world(self, preset):
        self.W = World(self, preset)
        return self.W

    def gap(self, phrase, lead=0.2, nth=0, floor=0.3):
        """Seconds from now until the narrator reaches a phrase (to make a move fill the wait)."""
        return max(floor, self.t_of(phrase, nth) - lead - self.elapsed())

    def rest(self, back=0.0):
        return max(0.05, self.narration_s + 0.4 - self.elapsed() - back)


class Stage(StageMixin, SpokenScene):
    pass


class Quiet(StageMixin, NarratedScene):
    pass


# ═════════════════════════════ scenes ═════════════════════════════
class S00Hook(Stage):
    def construct(self):
        W = self.world(zoomed(MOD, 0.92, (0, -0.35), (0, -0.35)))
        q = card(Q_HOOK)
        self.play(*W.to(MOD, 2.4, rate=rush_from, only=("cell", "nuc", "g", "s0", "s1", "s2")))
        self.at("separate living thing")
        self.play(W.g.tw(1.1, there_and_back, lit=1.0), Write(q, run_time=0.6))
        self.at("Your mitochondria")
        l1 = label("mitochondria", 34, PINK, P_OWN)
        self.play(Write(l1, run_time=0.6), W.g.tw(0.9, there_and_back, lit=0.6))
        self.at("their own DNA")
        self.play(W.r13.tw(1.2, there_and_back, lit=1.0), Transform(l1, label("their own DNA", 34, PINK, P_OWN), run_time=0.8))
        self.at("in your nucleus")
        l3 = label("DNA in your nucleus", 34, BLUE, P_NUCL)
        self.play(W.nring.tw(1.2, there_and_back, lit=1.0), W.nuc.tw(1.2, there_and_back, lit=0.7), Write(l3, run_time=0.6))
        self.at("pinching in two")
        s1, s2 = W.small[1], W.small[2]
        self.play(s1.tw(0.7, rush_into, pinch=1.0))
        split(s1, s2)
        self.play(s1.tw(0.8, **MOD3["s1"]), s2.tw(0.8, **MOD3["s2"]))
        self.at("Why would")
        self.play(FadeOut(l1, run_time=0.6), FadeOut(l3, run_time=0.6), q.animate(run_time=1.1, rate_func=there_and_back).scale(1.1),
                  W.g.tw(1.1, there_and_back, lit=1.0))
        self.finish()


class S01Title(Quiet):
    """The title, after the hook: in whole in 0.3 s, held 1.3 s, out in 0.4 s. The cell never leaves."""
    TITLE = "How Your Cells Got Mitochondria"

    def construct(self):
        W = self.world(MOD3)
        q = card(Q_HOOK)
        self.add(q)
        t0 = now()
        W.veil_a = lambda: 0.80 * min(1.0, (now() - t0) / 0.3) * (1 - smooth(min(1.0, max(0.0, (now() - t0 - 1.6) / 0.6))))
        brand = T("BIOCHEMISTRYPEDIA", size=28, color=TEAL, weight=BOLD)
        title = T(self.TITLE, size=54, font=TITLE_FONT)
        fit(title, max_w=11.5)
        rule = Line(LEFT * 1.2, RIGHT * 1.2, color=GOLD, stroke_width=4)
        g = VGroup(brand, title, rule).arrange(DOWN, buff=0.36).move_to([0, 0.1, 0]).set_z_index(30)
        self.play(FadeOut(q, run_time=0.3), FadeIn(g, run_time=0.3))
        self.wait(1.3)
        self.play(FadeOut(g, run_time=0.4))
        self.finish()


def fossil_labels():
    y = SCRUB_Y
    a = M(">1.5 billion years", size=32).move_to([TICKX, y + 0.5, 0]).set_z_index(20)
    b = label("oldest widely accepted eukaryote fossils", 28, TEXT, (TICKX - 0.35, y - 0.68))
    return a, b


EUK = lambda: label("eukaryotes: cells like ours", 32, TEXT, (0, CARD_Y))


class S02Old(Stage):
    def construct(self):
        W = self.world(mix(MOD3, scrub=dict(a=1.0, grow=0.0, knob=TODAY)))
        self.play(*W.to(UP3, 0.95, skip=("scrub",)))
        self.at("very old story")
        self.play(W.scrub.tw(1.6, grow=1.0))
        self.at("Eukaryotes")
        euk = EUK()
        self.play(Write(euk, run_time=0.6), W.cell.tw(1.4, there_and_back, lit=0.8))
        self.at("oldest")
        f1, f2 = fossil_labels()
        self.play(W.scrub.tw(1.5, knob=TICKX), W.scrub.tw(0.6, tick=1.0))
        self.play(Write(f1, run_time=0.6), FadeIn(f2, shift=UP * 0.1, run_time=0.9))
        self.finish()


def rewind_to_strangers(W, rt):
    """The modern cell comes apart into the host (with arms) and the dim rod at the right edge."""
    g, c = W.g, W.cell
    gx, gy = g.x, g.y
    small = [s.tw(rt * 0.4, x=gx, y=gy, a=0.0, L=0.6, H=0.3) for s in W.small]
    return small + [
        g.tw(rt, x=ANC["g"]["x"], y=ANC["g"]["y"], a=0.35), g.tw(rt * 0.6, bean=0.0, fold=0.0, L=ANC["g"]["L"], H=ANC["g"]["H"], chain=0.0, spark=0.0),
        W.r13.tw(rt * 0.5, a=0.0), W.rfull.tw(rt * 0.5, a=1.0),
        c.tw(rt, **{k: ANC["cell"][k] for k in "xywh"}), Succession(Wait(rt * 0.35), c.tw(rt * 0.65, arm=1.0)),
        W.nuc.tw(rt, **{k: ANC["nuc"][k] for k in "xyr"}), W.nuc.tw(rt * 0.6, solid=0.0)]


class S03Rewind(Stage):
    def construct(self):
        W = self.world(UP3)
        euk = EUK()
        f1, f2 = fossil_labels()
        self.add(euk, f1, f2)
        self.at("uncertain", lead=0.5)
        self.play(FadeOut(euk, run_time=0.5), FadeOut(f1, run_time=0.5), FadeOut(f2, run_time=0.5), W.scrub.tw(1.2, band=1.0))
        self.at("rewind")
        W.nuc.set(dash=1.0, ddraw=0.0)
        self.play(W.scrub.tw(1.4, knob=KBAND), *rewind_to_strangers(W, 2.7))
        self.at("two strangers", lead=0.0)
        self.play(W.cell.tw(1.0, there_and_back, lit=1.0), W.g.tw(1.0, there_and_back, lit=1.0))
        self.finish()


ARCH_LONG = lambda: label("most likely an archaeon", 34, BLUE, (-2.4, 3.12))
NUC_LAB = lambda: label2(["nucleus yet?", "debated"], 30, GOLD, (-1.05, 0.85))


class S04Host(Stage):
    def construct(self):
        W = self.world(ANC)
        self.wait(0.3)
        self.play(W.cell.tw(1.6, there_and_back, lit=0.7))
        self.at("most likely an archaeon")
        arch = ARCH_LONG()
        self.play(Write(arch, run_time=0.6))
        self.at("single celled")
        self.play(W.cell.tw(1.7, linear, sweep=1.0))
        W.cell.sweep = 0.0
        self.at("a nucleus")
        self.play(W.nuc.tw(0.5, ddraw=1.0))
        self.play(W.nuc.tw(0.4, ddraw=0.2))
        self.play(W.nuc.tw(0.5, ddraw=1.0), W.nuc.tw(0.5, q=1.0))
        nl = NUC_LAB()
        self.play(Write(nl, run_time=0.6))
        self.finish()


ARCH = lambda: label("archaeon", 30, BLUE, (-2.4, 3.12))
BAC = lambda: label("a bacterium", 34, PINK, (4.0, 2.75))
REL = lambda: label2(["alphaproteobacteria", "relative"], 28, TEXT, (4.0, 1.98))
# the same three names while s05 is pushed in on the guest (G5)
ARCH_IN = lambda: label("archaeon", 30, BLUE, (-5.3, 2.3))
BAC_IN = lambda: label("a bacterium", 34, PINK, (2.6, 3.0))
REL_IN = lambda: label2(["alphaproteobacteria", "relative"], 28, TEXT, (2.6, 2.08))


def chain_line():
    ch = label("a chain: energy from food", 28, YELLOW, (2.6, 2.3))
    pr = label("probably", 28, GOLD, (2.45, 1.72))
    b = gold_badge(0.19).next_to(pr, RIGHT, buff=0.14).set_z_index(20)
    return ch, VGroup(pr, b)


def oxygen_bits():
    toks = [o2_token().move_to(P3(p)) for p in [(5.85, -1.0), (5.95, 0.9), (6.0, -2.15)]]
    oxy = VGroup(gold_badge(0.24), label("oxygen? maybe", 28, GOLD, (0, 0))).arrange(RIGHT, buff=0.16).move_to([3.0, -1.95, 0]).set_z_index(20)
    return toks, oxy


class S05Guest(Stage):
    def construct(self):
        W = self.world(ANC2)
        g = W.g
        arch, nl = ARCH_LONG(), NUC_LAB()
        self.add(arch, nl)
        # push in on the second stranger: it fills the frame, and the host is cropped at the left edge
        arch_in = ARCH_IN()
        self.play(FadeOut(arch, run_time=0.5), FadeOut(nl, run_time=0.5), W.scrub.tw(0.7, a=0.0),
                  *W.to(G5, 1.9, only=("cell", "nuc")), g.tw(1.9, a=1.0, **{k: G5["g"][k] for k in ("x", "y", "L", "H")}),
                  g.tw(1.9, there_and_back, ang=0.25), Succession(Wait(1.3), FadeIn(arch_in, run_time=0.6)))
        bac = BAC_IN()
        self.play(Write(bac, run_time=0.6))
        self.at("alpha")
        rel = REL_IN()
        self.play(Write(rel, run_time=0.6))
        self.wait(0.5)
        self.play(g.tw(1.0, there_and_back, lit=0.7))
        self.at("probably respire")
        self.play(g.tw(1.2, chain=1.0), g.tw(1.2, there_and_back, rowglow=1.0))
        self.at("a chain")
        ch, prob = chain_line()
        self.play(Transform(rel, ch, run_time=0.8), g.tw(0.5, spark=1.0), W.sparks.tw(1.0, a=0.7),
                  Succession(Wait(0.5), FadeIn(prob, shift=UP * 0.1, run_time=0.6)))
        pulse(prob[1])
        self.at("pulled energy")
        self.play(g.tw(1.2, there_and_back, rowglow=1.0))
        # one thing at a time: the chain line leaves as the oxygen and its badge arrive
        self.at("used oxygen", lead=0.9)
        prob[1].clear_updaters()
        toks, oxy = oxygen_bits()
        ends = [t.get_center() for t in toks]
        for t in toks:
            t.shift(RIGHT * 2.6)
        self.play(FadeOut(rel, run_time=0.5), FadeOut(prob, run_time=0.5),
                  *[t.animate(run_time=1.5, rate_func=rush_from).move_to(e) for t, e in zip(toks, ends)],
                  Succession(Wait(0.8), FadeIn(oxy, scale=0.8, run_time=0.6)))
        pulse(oxy[0])
        for i, t in enumerate(toks):
            t.add_updater(lambda m, dt, i=i, e=ends[i]: m.move_to(e + np.array([0.08 * math.sin(0.9 * now() + i), 0.10 * math.sin(1.2 * now() + 2 * i), 0])))
        self.finish()


HOST = lambda size=48, x=-3.4, y=1.9: label("HOST", size, BLUE, (x, y), weight=BOLD)
GUEST_W = lambda pos, size=48: label("GUEST", size, PINK, pos, weight=BOLD)
Q_NEXT = "What happens next?"


class S06Enclose(Stage):
    def construct(self):
        W = self.world(G5)
        g, c = W.g, W.cell
        W.cradle()
        arch, bac, rel = ARCH_IN(), BAC_IN(), REL()
        toks, oxy = oxygen_bits()
        self.add(arch, bac, *toks, oxy)
        # pull back to both strangers; the oxygen leaves and the plain names return
        self.play(*[FadeOut(t, shift=RIGHT * 0.8, run_time=0.5) for t in toks], FadeOut(oxy, run_time=0.4),
                  *W.to(GIN, 0.65, only=("cell", "nuc", "g")), c.tw(0.65, arm_len=1.2), W.sparks.tw(0.6, a=0.0), W.scrub.tw(0.65, a=1.0),
                  Transform(arch, ARCH(), run_time=0.65), Transform(bac, BAC(), run_time=0.65), FadeIn(rel, run_time=0.55))
        self.at("long names", lead=0.1)
        self.play(*[Wiggle(m, scale_value=1.08, rotation_angle=0.02 * TAU, run_time=0.9) for m in (arch, bac, rel)])
        self.at("the host and the guest", lead=0.5)
        host, guest = HOST(), GUEST_W((4.0, 1.5))
        self.play(ReplacementTransform(arch, host, run_time=0.7), ReplacementTransform(bac, guest, run_time=0.7),
                  FadeOut(rel, target_position=guest, scale=0.3, run_time=0.6), c.tw(0.7, there_and_back, lit=0.7))
        self.play(g.tw(0.6, there_and_back, lit=0.8))
        self.at("Somehow")
        how = VGroup(gold_badge(0.24), label("how? one proposed way", 28, GOLD, (0, 0)))
        how.arrange(RIGHT, buff=0.16).move_to([3.5, -1.2, 0]).set_z_index(20)          # right under the curling arms
        lift = {"y": 1.15}                                                             # the word rides higher while the arms wrap
        guest.add_updater(lambda m, dt: m.move_to(g.center() + UP * lift["y"]))
        self.play(g.tw(1.3, x=2.3, y=0.3), c.tw(1.5, grab=[1.0, 1.0, 0, 0, 0]), Tw(lambda a: lift.__setitem__("y", lerp(1.15, 1.65, a)), 0.8),
                  Succession(Wait(0.6), FadeIn(how, shift=UP * 0.1, run_time=0.7)))
        pulse(how[0])
        self.at("enclose the guest", lead=0.1)
        self.play(g.tw(1.2, x=-0.6, y=0.3), Succession(Wait(0.6), c.tw(0.6, linear, sweep=1.0)),
                  Succession(Wait(0.6), Tw(lambda a: lift.__setitem__("y", lerp(1.65, 1.15, a)), 0.6)))
        c.sweep = 0.0
        self.at("do you expect", lead=0.65)
        how[0].clear_updaters()
        self.play(c.tw(0.6, grab=[0, 0, 0, 0, 0]), FadeOut(how, run_time=0.5), *W.to(ENC, 1.3, only=("cell", "nuc", "g")),
                  host.animate(run_time=1.3).move_to(HOST(x=-1.9)), Succession(Wait(0.4), Write(card(Q_NEXT), run_time=0.6)))
        self.finish()


def host_guest_labels(sc, W):
    host, guest = HOST(x=-1.9), GUEST_W((0, 0))
    guest.add_updater(lambda m, dt: m.move_to(W.g.center() + UP * 1.15))
    guest.update(0)
    sc.add(host, guest)
    return host, guest


class S07Hold(Quiet):
    def construct(self):
        W = self.world(ENC)
        host_guest_labels(self, W)
        q = card(Q_NEXT)
        self.add(q)
        self.play(W.g.tw(1.2, loop=1.0), q.animate(run_time=2.0, rate_func=there_and_back).scale(1.06))
        self.play(W.cell.tw(1.8, there_and_back, lit=0.35))
        self.finish()


class S08Stayed(Stage):
    def construct(self):
        W = self.world(mix(ENC, g=dict(loop=1.0)))
        g, c = W.g, W.cell
        host, guest = host_guest_labels(self, W)
        q = card(Q_NEXT)
        self.add(q)
        self.play(FadeOut(q, run_time=0.5), g.tw(0.5, loop=0.0))
        # the fate that did NOT happen: a grey ghost is digested, and the word is struck out (one strike, through the word)
        ghost = rod_outline(g.cx, g.cy, g.L, g.H, color="#9AA3B2", width=4)
        ghost[0].set_stroke(GREY, opacity=0.12)
        gp = np.array([0.5, -1.33, 0.0])
        ghost.generate_target()
        ghost.target.scale(0.8).move_to(gp)
        self.add(ghost)
        self.play(MoveToTarget(ghost, run_time=0.6))
        rng = random.Random(8)
        bits = VGroup(*[Dot(gp + np.array([1.0 * math.cos(a), 0.46 * math.sin(a), 0]), radius=rng.uniform(0.05, 0.09), color=GREY)
                        for a in np.linspace(0, TAU, 16, endpoint=False)]).set_z_index(12)
        tag = label("digested", 28, TEXT, (-1.6, -1.5))                     # readable first, in TEXT
        self.play(FadeOut(ghost, run_time=0.4), FadeIn(bits, run_time=0.3), FadeIn(tag, run_time=0.4),
                  *[b.animate(run_time=0.8, rate_func=rush_from).shift([rng.uniform(-0.3, 0.3), rng.uniform(-0.35, 0.1), 0]).scale(0.5) for b in bits])
        self.at("instead", lead=0.1)
        strike = Line(tag.get_left() + LEFT * 0.12, tag.get_right() + RIGHT * 0.12, color=GREY, stroke_width=5).set_z_index(21)
        self.play(Create(strike, run_time=0.5), tag.animate(run_time=0.5).set_color("#9AA3B2"))      # greyed as the strike lands
        self.at("stayed", lead=0.45)
        guest.clear_updaters()
        stay = label("it stayed", 44, PINK, g.center() + UP * 1.15, weight=BOLD)
        self.play(FadeOut(VGroup(bits, tag, strike), run_time=0.5), g.tw(1.3, there_and_back, lit=1.0), Transform(guest, stay, run_time=0.8))
        self.at("Two strangers")
        self.play(FadeOut(host, run_time=0.7), *W.to(MRG, 2.0, only=("cell", "nuc", "g")),
                  guest.animate(run_time=2.0).move_to([MRG["g"]["x"], MRG["g"]["y"] + 1.3, 0]))
        self.finish()


def slot_column():
    slots = VGroup(*[RoundedRectangle(width=4.55, height=0.72, corner_radius=0.16, stroke_color=GREEN, stroke_width=3.5,
                                      fill_color=GREEN, fill_opacity=0.0).move_to([0.1, 1.45 - 0.9 * i, 0]) for i in range(4)]).set_z_index(18)
    qs = VGroup(*[T("?", size=32, color=GREEN, weight=BOLD).move_to(s) for s in slots]).set_z_index(20)
    return slots, qs


SLOT_WORDS = ["two membranes", "own DNA", "bacteria-like ribosomes", "divide by pinching"]
MLAB = lambda: label("mitochondrion, today", 30, PINK, (-4.3, 2.1))
RLAB = lambda: label2(["guest's free relative,", "today"], 28, TEXT, (4.3, 2.15))
Q_LEAVE = "What would it leave behind?"


def free_relative(**kw):
    return Guest(**{**dict(x=4.6, y=0.4, L=3.0, H=1.5, bean=0.0, detail=0.0, seed=2.3), **kw})


class S09Traces(Stage):
    def construct(self):
        W = self.world(MRG)
        g = W.g
        stay = label("it stayed", 44, PINK, (MRG["g"]["x"], MRG["g"]["y"] + 1.3), weight=BOLD)
        self.add(stay)
        mid = mix(PUSH, g=dict(x=0.0, y=0.2, L=6.0, H=3.3, detail=1.0, chain=1.0, spark=1.0, sil=0.0), rfull=dict(a=1.0), scrub=dict(knob=KBAND, words=1.0))
        self.play(FadeOut(stay, run_time=0.5), *W.to(mid, 1.7, skip=("nuc",)), W.nuc.tw(0.6, a=0.0), W.nuc.tw(1.7, x=-5.5))
        self.at("Your mitochondria", lead=0.1)
        ml = label("mitochondrion, today", 34, PINK, (0, 2.6))
        self.play(Write(ml, run_time=0.6))
        self.at("that guest")
        rod = rod_outline(g.x, g.y, 5.5, 2.4, width=6)
        self.add(rod)
        self.play(flicker(rod, 1.3), g.tw(1.3, there_and_back, lit=0.5))
        self.remove(rod)
        self.at("so long afterwards")
        self.play(W.scrub.tw(1.4, knob=TODAY), W.scrub.tw(1.0, words=0.0), g.tw(1.4, detail=0.0, chain=0.0, spark=0.0, sil=1.0), W.rfull.tw(1.0, a=0.0))
        self.at("a bacterium", lead=0.7)
        rel = free_relative(x=9.5, sil=1.0)
        self.add(rel.mob)
        rl = RLAB()
        self.play(g.tw(1.4, **{k: PUSH["g"][k] for k in ("x", "y", "L", "H")}), Transform(ml, MLAB(), run_time=1.4),
                  rel.tw(1.4, rush_from, x=4.6), Succession(Wait(0.8), FadeIn(rl, shift=UP * 0.1, run_time=0.6)))
        self.at("leave behind", lead=0.6)
        slots, qs = slot_column()
        self.play(LaggedStart(*[Create(s) for s in slots], lag_ratio=0.2, run_time=1.0), Write(card(Q_LEAVE, 40), run_time=0.6))
        self.play(LaggedStart(*[FadeIn(q, scale=0.5) for q in qs], lag_ratio=0.2, run_time=0.6))
        self.finish()


def slot_pulse(qs):
    for i, q in enumerate(qs):
        q.h0 = q.height
        q.add_updater(lambda m, dt, i=i: m.scale_to_fit_height(m.h0 * (1 + 0.45 * max(0.0, math.sin(TAU * (now() / 2.0 - i * 0.2))) ** 3)))


class S10Hold(Quiet):
    def construct(self):
        W = self.world(PUSH)
        rel = free_relative(sil=1.0)
        slots, qs = slot_column()
        q = card(Q_LEAVE, 40)
        self.add(rel.mob, MLAB(), RLAB(), slots, qs, q)
        slot_pulse(qs)
        self.play(q.animate(run_time=2.2, rate_func=there_and_back).scale(1.06))
        self.play(W.g.tw(1.8, there_and_back, lit=0.3), rel.tw(1.8, there_and_back, lit=0.3))
        self.finish()


class Dots(Proc):
    """Ribosomes: a scatter of small dots that stay with their host."""

    def __init__(self, host, uv, rk=0.035, color="#FFC2D4", z=-14):
        self.host, self.uv, self.rk, self.a = host, uv, rk, 0.0
        self.m = VMobject(stroke_width=0, fill_color=color)
        self.mob = VGroup(self.m).set_z_index(z)
        self._live()

    def points(self):
        return [self.host.anchor(u, v) for u, v in self.uv]

    def draw(self):
        o = self.a * self.host.a
        if o < 0.01:
            self.m.set_fill(opacity=0)
            return
        r = self.rk * self.host.H
        self.m.set_points(np.concatenate([circ(p, r) for p in self.points()]))
        self.m.set_fill(opacity=o)


RIBO_UV = [(-0.36, -0.28), (-0.30, 0.10), (-0.20, -0.36), (-0.12, 0.30), (-0.04, -0.33), (0.08, 0.31), (0.16, -0.36), (0.26, 0.12), (0.33, -0.27), (0.38, 0.02)]
HALF = dict(A1=dict(x=-5.45, y=0.4, L=1.65, H=1.3), A2=dict(x=-3.65, y=0.4, L=1.65, H=1.3),
            B1=dict(x=3.75, y=0.4, L=1.5, H=1.15), B2=dict(x=5.45, y=0.4, L=1.5, H=1.15))


def fill_slot(slots, qs, i):
    w = label(SLOT_WORDS[i], 28, TEXT, slots[i].get_center())
    return [slots[i].animate(run_time=0.6).set_fill(GREEN, opacity=0.28), ReplacementTransform(qs[i], w, run_time=0.6)], w


def half_uv(side):
    """Ribosome dots of one half after a division (same places on screen as before it)."""
    return [((u - 0.25 * side) * 2 / 1.04, v) for u, v in RIBO_UV if u * side > 0]


class S11Clues(Stage):
    def construct(self):
        W = self.world(PUSH)
        g = W.g
        rel = free_relative(sil=1.0)
        slots, qs = slot_column()
        q, ml, rl = card(Q_LEAVE, 40), MLAB(), RLAB()
        self.add(rel.mob, ml, rl, slots, qs, q)
        slot_pulse(qs)
        rB = Ring(rel, [TAU * i / 26 for i in range(26)], PINK, RFK, BFK, a=0.0)
        dA, dB = Dots(g, RIBO_UV), Dots(rel, RIBO_UV)
        self.add(rB.mob, dA.mob, dB.mob)
        self.play(FadeOut(q, run_time=0.6), Transform(ml, label("most mitochondria", 34, TEXT, (-4.3, 2.1)), run_time=0.8))
        self.at("two membranes")
        an, w1 = fill_slot(slots, qs, 0)
        self.play(g.tw(0.9, detail=1.0, sil=0.25), rel.tw(0.9, detail=1.0, sil=0.25), g.tw(1.2, there_and_back, lit=0.8),
                  rel.tw(1.2, there_and_back, lit=0.8), *an)
        self.at("their own DNA")
        an, w2 = fill_slot(slots, qs, 1)
        self.play(W.rfull.tw(0.7, a=1.0), rB.tw(0.7, a=1.0), W.rfull.tw(1.2, there_and_back, lit=1.0), rB.tw(1.2, there_and_back, lit=1.0), *an)
        self.at("ribosomes")
        self.play(dA.tw(0.7, a=1.0), dB.tw(0.7, a=1.0))
        self.at("build proteins", lead=0.1)
        threads, moves = VGroup(), []
        rng = random.Random(5)
        for d in (dA, dB):
            for p in d.points():
                dr = rot2([0.5, 0], rng.uniform(0.3, 2.8))
                pts = [p + dr * s + rot2(dr, PI / 2) * 0.12 * math.sin(7 * s) for s in np.linspace(0, 1, 9)]
                th = VMobject(stroke_color=PINK, stroke_width=3, fill_opacity=0).set_points_smoothly(pts).set_z_index(-13)
                threads.add(th)
                moves.append(Succession(Create(th, run_time=0.5), th.animate(run_time=0.6).shift(dr * 0.8).set_stroke(opacity=0)))
        an, w3 = fill_slot(slots, qs, 2)
        self.play(LaggedStart(*moves, lag_ratio=0.03), Succession(Wait(0.9), AnimationGroup(*an)))
        self.remove(threads)
        self.at("pinching in two", lead=0.5)
        A2, B2 = Guest(a=0.0, n=140, seed=3.1), Guest(a=0.0, seed=4.2)
        rA2 = Ring(A2, [TAU * i / 26 for i in range(26)], PINK, RFK, BFK)
        rB2 = Ring(B2, [TAU * i / 26 for i in range(26)], PINK, RFK, BFK)
        self.add(A2.mob, B2.mob, rA2.mob, rB2.mob)
        self.play(g.tw(0.8, rush_into, pinch=1.0), rel.tw(0.8, rush_into, pinch=1.0))
        split(g, A2)
        split(rel, B2)
        dA2, dB2 = Dots(A2, half_uv(1)), Dots(B2, half_uv(1))
        dA.uv, dB.uv = half_uv(-1), half_uv(-1)
        dA2.a = dB2.a = 1.0
        self.add(dA2.mob, dB2.mob)
        an, w4 = fill_slot(slots, qs, 3)
        self.play(g.tw(0.8, **HALF["A1"]), A2.tw(0.8, **HALF["A2"]), rel.tw(0.8, **HALF["B1"]), B2.tw(0.8, **HALF["B2"]), *an)
        self.finish()


def tree_lines():
    """The gene tree, drawn from the tips back: six lines join in pairs, then meet at one point."""
    twigs = VGroup(*[Line([x, y - 0.42, 0], P3(PAIRS[i // 2]), color=PINK, stroke_width=6) for i, (x, y) in enumerate(TIPS)])
    limbs = VGroup(*[Line(P3(p), P3(MEET), color=PINK, stroke_width=6) for p in PAIRS])
    return twigs.set_z_index(-25), limbs.set_z_index(-25)


def bacteria_branches():
    stem = Line(P3(MEET), P3(ROOT), color=TEXT, stroke_width=5)
    br = VGroup(Line([0, -1.15, 0], [-2.9, -0.45, 0], color=TEXT, stroke_width=4), Line([0, -1.6, 0], [3.1, -0.8, 0], color=TEXT, stroke_width=4),
                Line([0, -1.9, 0], [-3.2, -1.6, 0], color=TEXT, stroke_width=4))
    lab = label("free bacteria", 28, TEXT, (-4.5, -1.02))
    return stem.set_z_index(-25), br.set_z_index(-25), lab


TAGS = lambda: [label(w, 28, TEXT, (p[0], 3.15)) for w, p in zip(("animals", "plants", "fungi"), PAIRS)]
SCHEM = lambda: label("gene tree (schematic)", 28, TEXT, (4.2, -1.9))
ONCE = lambda: label("suggests: once", 32, TEXT, (-4.6, 0.25))
ONE_GUEST = lambda: label("one guest", 40, PINK, (4.45, -0.15), weight=BOLD)      # right of the rod, between the limb above and the branch below


def backing(g, color="#0E2434", z=-22):
    """An opaque copy of a guest's outline drawn under it, so the tree's lines do not show through its pale fill."""
    m = VMobject(stroke_width=0, fill_color=color, fill_opacity=0).set_z_index(z)
    m.k = 1.0

    def upd(mob, dt=0):
        if g.a * mob.k < 0.02 or len(g.body.points) == 0:
            mob.set_fill(opacity=0)
        else:
            mob.set_points(g.body.points.copy())
            mob.set_fill(opacity=min(1.0, g.a * mob.k))
    m.add_updater(upd)
    return m
TIP = dict(L=1.5, H=0.78, bean=1.0, detail=0.0, dota=1.0, sil=0.0, fold=0.0, a=1.0)


def make_tips():
    return [Guest(x=x, y=y, n=70, seed=i + 5, **TIP) for i, (x, y) in enumerate(TIPS)]


class S12Once(Stage):
    def construct(self):
        W = self.world(CLUE4)
        g = W.g
        A2, B1, B2 = Guest(seed=3.1, bean=1.0, fold=0.7, sil=0.25, **HALF["A2"]), free_relative(sil=0.25, detail=1.0, **HALF["B1"]), \
            free_relative(sil=0.25, detail=1.0, seed=4.2, **HALF["B2"])
        ring = lambda h: Ring(h, [TAU * i / 26 for i in range(26)], PINK, RFK, BFK)
        rs = [ring(A2), ring(B1), ring(B2)]
        ds = [Dots(g, half_uv(-1)), Dots(A2, half_uv(1)), Dots(B1, half_uv(-1)), Dots(B2, half_uv(1))]
        for d in ds:
            d.a = 1.0
        slots, _ = slot_column()
        slots.set_fill(GREEN, opacity=0.28)
        words = VGroup(*[label(w, 28, TEXT, s.get_center()) for w, s in zip(SLOT_WORDS, slots)])
        ml, rl = label("most mitochondria", 34, TEXT, (-4.3, 2.1)), RLAB()
        self.add(A2.mob, B1.mob, B2.mob, *[r.mob for r in rs], *[d.mob for d in ds], slots, words, ml, rl)
        # everything but one mitochondrion leaves
        self.play(B1.tw(1.1, rush_into, x=10.0), B2.tw(1.1, rush_into, x=12.0), A2.tw(0.9, a=0.0, x=-1.5),
                  VGroup(slots, words, rl).animate(run_time=1.1, rate_func=rush_into).shift(RIGHT * 9), FadeOut(ml, run_time=0.6),
                  *[d.tw(0.6, a=0.0) for d in ds], W.rfull.tw(0.8, a=0.0), W.cell.tw(1.1, a=0.5))
        self.remove(slots, words, rl)
        self.at("from genes", lead=0.3)
        tips = make_tips()
        for t in tips[1:]:
            t.y = 5.0
            self.add(t.mob)
        self.play(g.tw(1.2, x=TIPS[0][0], y=TIPS[0][1], **TIP), LaggedStart(*[t.tw(0.9, y=TIPS[0][1]) for t in tips[1:]], lag_ratio=0.18))
        self.at("the family tree")
        twigs, limbs = tree_lines()
        sch = SCHEM()
        self.play(LaggedStart(*[Create(l) for l in twigs], lag_ratio=0.1, run_time=0.9), FadeIn(sch, run_time=0.8))
        self.play(LaggedStart(*[Create(l) for l in limbs], lag_ratio=0.15, run_time=0.9))
        tags = TAGS()
        beans = [g] + tips[1:]
        for i, cue in enumerate(("animals", "plants", "fungi")):
            self.at(cue, lead=0.15)
            self.play(Write(tags[i], run_time=0.45), beans[2 * i].tw(0.5, there_and_back, lit=1.0), beans[2 * i + 1].tw(0.5, there_and_back, lit=1.0))
        self.at("on one branch", lead=0.3)
        stem, br, fb = bacteria_branches()
        node = Dot(P3(MEET), radius=0.16, color=PINK).set_z_index(-24)
        self.play(Create(stem, run_time=0.8), FadeIn(node, scale=0.3, run_time=0.5))
        self.play(LaggedStart(*[Create(b) for b in br], lag_ratio=0.25, run_time=1.0), FadeIn(fb, run_time=0.8))
        self.at("only once", lead=0.4)
        once = ONCE()
        halo = Circle(radius=0.2, color=PINK, stroke_width=6).move_to(P3(MEET)).set_z_index(-24)
        self.play(Write(once, run_time=0.6), halo.animate(run_time=1.2).scale(5).set_stroke(opacity=0), node.animate(run_time=0.6, rate_func=there_and_back).scale(1.8))
        self.remove(halo)
        self.at("Every")
        runners = VGroup(*[Dot(radius=0.11, color="#FFE3EC").set_z_index(-23) for _ in TIPS])
        paths = [VMobject().set_points_as_corners([[x, y - 0.42, 0], P3(PAIRS[i // 2]), P3(MEET)]) for i, (x, y) in enumerate(TIPS)]
        self.play(*[b.tw(0.8, there_and_back, lit=1.0) for b in beans])
        self.play(*[MoveAlongPath(r, p, run_time=self.gap("single guest", lead=0.5), rate_func=smooth) for r, p in zip(runners, paths)])
        self.remove(runners)
        rod = Guest(x=MEET[0], y=MEET[1], L=0.4, H=0.2, a=0.0, chain=1.0, spark=1.0, n=140)
        rr = Ring(rod, [TAU * i / 26 for i in range(26)], PINK, RFK, BFK)
        self.add(backing(rod), rod.mob, rr.mob)                # the rod is drawn IN FRONT of the branches
        self.play(rod.tw(0.7, a=1.0, L=TREE["g"]["L"], H=TREE["g"]["H"]), rod.tw(1.2, there_and_back, lit=1.0), FadeOut(node, run_time=0.5),
                  Write(ONE_GUEST(), run_time=0.6))             # 'suggests: once' stays: the hedge holds while the firmest claim is on screen
        self.finish()


class S13Idea(Stage):
    def construct(self):
        W = self.world(TREE)
        g = W.g
        tips = make_tips()
        twigs, limbs = tree_lines()
        stem, br, fb = bacteria_branches()
        tags, sch, one, once = TAGS(), SCHEM(), ONE_GUEST(), ONCE()
        back = backing(g)
        self.add(back, *[t.mob for t in tips], twigs, limbs, stem, br, fb, *tags, sch, one, once)
        self.at("the idea to keep", lead=0.5)
        # the tree runs in reverse INTO the guest while the host is already coming back around it, with its
        # bead ring, dashed circle and "?" (the frame is never just the small rod)
        self.play(*[t.tw(1.1, rush_into, x=MEET[0], y=MEET[1], a=0.0, L=0.4, H=0.2) for t in tips],
                  *[Uncreate(l, run_time=1.0) for l in (*twigs, *limbs)], *[FadeOut(m, run_time=0.7) for m in (*tags, sch, one, once, fb)],
                  *[Uncreate(l, run_time=0.8) for l in (stem, *br)],
                  *W.to(IDEA, 1.9, only=("cell",)), W.nuc.tw(1.9, **{k: IDEA["nuc"][k] for k in "xyr"}),
                  Succession(Wait(0.7), W.nuc.tw(1.0, a=1.0)),
                  Succession(Wait(0.6), AnimationGroup(*W.to(IDEA, 1.4, only=("g",)), g.tw(1.4, there_and_back, lit=0.6))),
                  Succession(Wait(1.0), Tw(lambda a: setattr(back, "k", 1 - a), 0.5)))
        self.remove(back)
        self.at("your cells invented")
        self.play(W.cell.tw(1.4, there_and_back, lit=1.0))
        # the guiding sentence starts on "It is a guest", is whole as the narrator finishes, and is carried into s14
        self.at("guess", lead=0.3)
        sen = idea_sentence()
        self.play(g.tw(1.4, there_and_back, lit=1.0), Write(sen, run_time=0.6))
        self.finish()


def idea_sentence():
    return T("A guest that stayed.", size=48, font=TITLE_FONT, t2c={"guest": PINK}).move_to([IDEA["g"]["x"], -1.05, 0]).set_z_index(22)


def why_badges():
    hb, ob = gold_badge(0.28), gold_badge(0.28)
    hw, ow = label("hydrogen?", 34, TEAL, (0, 0), weight=BOLD), label("oxygen?", 34, RED, (0, 0), weight=BOLD)
    hg = VGroup(hb, hw).arrange(RIGHT, buff=0.3).move_to([-4.7, CARD_Y - 0.05, 0]).set_z_index(21)
    og = VGroup(ow, ob).arrange(RIGHT, buff=0.3).move_to([4.8, CARD_Y - 0.05, 0]).set_z_index(21)
    return hg, og


WHY_TOP = lambda size=36: label("why? still debated", size, GOLD, (0, CARD_Y), weight=SEMIBOLD)
GUEST_POS = (5.55, 0.2)


def why_world(sc, preset=WHY):
    W = sc.world(preset)
    W.cradle()
    W.cell.grab[:2] = 0.55
    return W


def orbiters(center, radius):
    """A teal bubble and a red dot that circle a gold badge (and only the badge: they never cross its word)."""
    orb_h = Circle(radius=0.11, stroke_color=TEAL, stroke_width=3, fill_color="#0E3A40", fill_opacity=1).set_z_index(23)
    orb_o = Circle(radius=0.11, stroke_width=0, fill_color=RED, fill_opacity=1).set_z_index(23)
    orb_h.add_updater(lambda m, dt: m.move_to(center("h") + radius() * np.array([math.cos(2.2 * now()), math.sin(2.2 * now()), 0])))
    orb_o.add_updater(lambda m, dt: m.move_to(center("o") + radius() * np.array([math.cos(-2.2 * now() + 1), math.sin(-2.2 * now() + 1), 0])))
    orb_h.update(0)
    orb_o.update(0)
    return orb_h, orb_o


class S14Why(Stage):
    def construct(self):
        W = self.world(IDEA)
        g, c = W.g, W.cell
        W.cradle()
        sen = idea_sentence()
        self.add(sen)                                   # the guiding sentence holds through "But why did the partnership begin?"
        self.at("partnership")
        self.play(c.tw(1.2, there_and_back, lit=0.6), g.tw(1.2, there_and_back, lit=0.6))
        self.at("Go back")
        host, guest = HOST(40, -2.6, 1.8), GUEST_W(GUEST_POS, 40)
        nq = label("nucleus yet?", 30, GOLD, (0, 0))    # the bare "?" on the dashed circle gets its words back for two seconds
        set_dim(nq, 0.0)
        nq.add_updater(lambda m, dt: m.next_to(W.nuc.badge, RIGHT, buff=0.16))
        self.add(nq)
        self.play(Succession(Wait(0.3), FadeOut(sen, run_time=0.6)), W.scrub.tw(1.5, knob=KBAND, words=1.0),
                  *W.to(WHY, 2.4, only=("cell", "nuc", "g")), Succession(Wait(1.2), c.tw(1.2, grab=[0.55, 0.55, 0, 0, 0])),
                  Succession(Wait(1.8), AnimationGroup(FadeIn(host, run_time=0.6), FadeIn(guest, run_time=0.6))),
                  Succession(Wait(1.3), dim(nq, 1.0, 0.5)))
        self.at("still debated", lead=1.0)
        self.play(dim(nq, 0.0, 0.5))
        self.remove(nq)
        self.at("debated", lead=0.4)
        top = WHY_TOP()
        self.play(Write(top, run_time=0.6))
        self.at("two of the ideas", lead=0.5)
        hg, og = why_badges()
        for grp in (hg, og):
            grp.save_state()
            grp.scale(0.3).move_to([0.6, 0.6, 0]).set_opacity(0)
        self.play(Restore(hg, run_time=1.2, path_arc=-0.6), Restore(og, run_time=1.2, path_arc=0.6))
        self.finish()


SOCKET = (0.4, 0.2)
H2_AT, O2_AT = 0.2, 8.1          # seconds into s15 / s16 at which the first hydrogen bubble / the first oxygen for the guest sets out


def socket():
    s = Circle(radius=0.44, stroke_color=TEAL, stroke_width=4, fill_color=TEAL, fill_opacity=0.06).move_to(P3(SOCKET)).set_z_index(-18)
    return DashedVMobject(s, num_dashes=14).set_z_index(-18), s


class H2Stream(Proc):
    """Hydrogen bubbles leave the guest one after another, cross into the host and drop into its socket."""

    def __init__(self, guest, t0, n=4, gap=0.8, travel=2.4, z=10):
        self.g, self.t0, self.n, self.gap, self.travel, self.a = guest, t0, n, gap, travel, 1.0
        self.tok = [h2_bubble(0.5) for _ in range(n)]
        self.h0 = self.tok[0].height
        self.mob = VGroup(*self.tok).set_z_index(z)
        for m in self.mob:
            m.set_opacity(0)
        self._k = [None] * n
        self._live()

    def draw(self):
        t = now() - self.t0
        P = self.n * self.gap
        end = P3(SOCKET)
        for i, tk in enumerate(self.tok):
            lt = t - i * self.gap
            age = lt % P if lt >= 0 else -1.0
            o = 0.0
            if 0 <= age < self.travel:
                s = age / self.travel
                e = s
                start = self.g.center() + np.array([-0.5, 0.5, 0])
                ctl = np.array([1.6, 1.5 + 0.25 * math.sin(i), 0.0])
                p = (1 - e) ** 2 * start + 2 * (1 - e) * e * ctl + e ** 2 * end
                o = round(self.a * min(1.0, s / 0.12) * min(1.0, (1 - s) / 0.12), 2)
                tk.scale_to_fit_height(self.h0 * (0.6 + 0.4 * min(1.0, s / 0.2)) * (1 - 0.3 * max(0.0, (s - 0.8) / 0.2)))
                tk.move_to(p)
            if self._k[i] != o:
                tk.set_opacity(o)
                tk[0].set_fill(opacity=0.12 * o)
                tk[1].set_fill(opacity=0.85 * o)
                self._k[i] = o


def h_arrow():
    arr = CurvedArrow([3.6, 1.05, 0], [1.2, 1.4, 0], angle=1.0, color=TEAL, stroke_width=9, tip_length=0.38).set_z_index(15)
    lab = label2(["guest's waste", "feeds the host"], 30, TEXT, (3.75, -1.4), buff=0.09)      # below the guest, away from both badges
    return arr, lab


def badge_focus(hg, og, which):
    """Bring one hypothesis badge forward and dim the other (which = 'h', 'o' or None for equal)."""
    for grp, me in ((hg, "h"), (og, "o")):
        set_dim(grp, 1.0 if which is None or which == me else 0.3)
        grp.scale(1.18 if which == me else 1.0, about_edge=LEFT if me == "h" else RIGHT)


class S15Hydrogen(Stage):
    def construct(self):
        W = why_world(self)
        g, c = W.g, W.cell
        host, guest, top = HOST(40, -2.6, 1.8), GUEST_W(GUEST_POS, 40), WHY_TOP()
        hg, og = why_badges()
        st = H2Stream(g, T0.get("s15_hydrogen", 0.0) + H2_AT)
        self.add(host, guest, top, hg, og, st.mob)
        self.at("hydrogen hypothesis", lead=0.3)
        self.play(rescale(hg, 1.18, 0.8, LEFT), dim(og, 0.3), Transform(top, WHY_TOP(28), run_time=0.8),
                  g.tw(0.8, chain=0.1, spark=0.0), W.scrub.tw(0.8, a=0.0))     # the guest's oxygen chain dims; the resting scrubber leaves
        self.at("lived on hydrogen")
        sock, sfill = socket()
        self.play(Create(sock, run_time=0.9), c.tw(1.2, there_and_back, lit=0.5))
        pulse(sock, 0.10, 1.6)
        self.at("gave off hydrogen", lead=0.5)
        self.play(g.tw(1.0, there_and_back, lit=0.8))
        self.wait(1.0)
        sfill.set_stroke(opacity=0)
        self.add(sfill)
        self.play(sfill.animate(run_time=0.8).set_fill(TEAL, opacity=0.45), c.tw(1.0, there_and_back, lit=0.8))
        self.at("depend on the guest", lead=0.6)
        arr, lab = h_arrow()
        self.play(Create(arr, run_time=0.9), FadeIn(lab, shift=DOWN * 0.1, run_time=0.9), c.tw(1.2, x=c.x + 0.12))
        self.finish()


class O2Feed(Proc):
    """Oxygen for s16 / s17: big red dots drift in from the right and the top and the guest takes every one of them."""
    STARTS = [(1.6, 0), (4.5, 1), (-1.5, 0), (5.4, 1), (1.3, 0), (3.2, 1)]      # (y or x, from the right (0) / from the top (1))

    def __init__(self, guest, t0, n=6, gap=0.6, travel=1.9, z=10):
        self.g, self.t0, self.n, self.gap, self.travel, self.a = guest, t0, n, gap, travel, 1.0
        self.tok = [o2_token(0.45) for _ in range(n)]
        self.h0 = self.tok[0].height
        self.mob = VGroup(*self.tok).set_z_index(z)
        for m in self.mob:
            m.set_opacity(0)
        self._k = [None] * n
        self._live()

    def draw(self):
        t = now() - self.t0
        P = self.n * self.gap
        for i, tk in enumerate(self.tok):
            lt = t - i * self.gap
            age = lt % P if lt >= 0 else -1.0
            o = 0.0
            if 0 <= age < self.travel:
                s = age / self.travel
                e = smooth(s)
                v, top = self.STARTS[i % len(self.STARTS)]
                start = np.array([v, FH / 2 + 0.6, 0.0]) if top else np.array([FW / 2 + 0.6, v, 0.0])
                end = self.g.center() + np.array([0.2, 0.0, 0.0])
                ctl = np.array([start[0] * 0.55 + end[0] * 0.45, start[1] * 0.45 + end[1] * 0.55 + 0.6, 0.0])
                p = (1 - e) ** 2 * start + 2 * (1 - e) * e * ctl + e ** 2 * end
                o = round(self.a * min(1.0, (1 - s) / 0.12), 2)
                tk.scale_to_fit_height(self.h0 * (1 - 0.7 * max(0.0, (s - 0.7) / 0.3)))
                tk.move_to(p)
            if self._k[i] != o:
                tk.set_opacity(o)
                tk[0].set_fill(opacity=0.16 * o)
                self._k[i] = o


def shield(c):
    """A soft blue protected zone round the host's right, top and bottom, in front of the incoming oxygen's path."""
    pts = np.array([c.pt_at(d, 1.09) for d in np.linspace(-78, 78, 60)])
    return VGroup(VMobject(fill_opacity=0).set_points_smoothly(pts).set_stroke(BLUE, width=34, opacity=0.16),
                  VMobject(fill_opacity=0).set_points_smoothly(pts).set_stroke("#BFEFFF", width=8, opacity=0.9)).set_z_index(-11)


def contact_ring(p):
    """A red ring that flashes out from the point where oxygen touches the host."""
    r = Circle(radius=0.25, stroke_color=RED, stroke_width=6, fill_opacity=0).move_to(p).set_z_index(24)
    return r


class S16Oxygen(Stage):
    def construct(self):
        W = why_world(self)
        g, c = W.g, W.cell
        c.x += 0.12
        g.chain, g.spark = 0.1, 0.0                          # as s15 ended: the guest's oxygen chain still dimmed
        W.scrub.a = 0.0
        host, guest, top = HOST(40, -2.6, 1.8), GUEST_W(GUEST_POS, 40), WHY_TOP(28)
        hg, og = why_badges()
        badge_focus(hg, og, "h")
        sock, sfill = socket()
        sfill.set_stroke(opacity=0).set_fill(TEAL, opacity=0.45)
        st = H2Stream(g, T0.get("s15_hydrogen", 0.0) + H2_AT)
        arr, lab = h_arrow()
        feed = O2Feed(g, T0.get("s16_oxygen", 0.0) + O2_AT)
        feed.a = 0.0
        self.add(host, guest, top, hg, og, sock, sfill, st.mob, arr, lab, feed.mob)
        # reset first: the hydrogen picture is fully gone before any oxygen appears
        self.play(st.tw(0.5, a=0.0), *[FadeOut(m, run_time=0.6) for m in (sock, sfill, arr, lab)], c.tw(0.7, x=c.x - 0.12),
                  rescale(hg, 1 / 1.18, 0.7, LEFT), dim(hg, 0.3, 0.7), rescale(og, 1.18, 0.7, RIGHT), dim(og, 1.0, 0.7),
                  g.tw(0.7, chain=1.0, spark=1.0))
        self.remove(st.mob)
        self.at("protection", lead=0.3)
        self.play(og[1].animate(run_time=1.0, rate_func=there_and_back).scale(1.25), g.tw(1.0, there_and_back, lit=0.4))
        self.at("Oxygen can damage", lead=0.3)
        hits = [(152, np.array([-7.7, 2.3, 0])), (-100, np.array([-3.6, -4.6, 0]))]
        toks = [o2_token(0.45).move_to(p) for _, p in hits]
        ends = [c.pt_at(d, 1.04) for d, _ in hits]
        self.add(*toks)
        base = self.gap("harmed the host", lead=0.1)

        def touch(deg, pos):
            done = []

            def f(a):
                if not done and a > 0:
                    done.append(1)
                    c.flinch(deg, 0.17)
                    ring = contact_ring(pos)
                    self.add(ring)
                    ring.add_updater(lambda m, dt, st={"t": 0.0}: (st.__setitem__("t", st["t"] + dt), m.set_width(0.5 + 1.8 * st["t"]),
                                                                  m.set_stroke(opacity=max(0.0, 1 - st["t"] / 0.5)), None)[-1])
            return Tw(f, 0.05)

        self.play(*[Succession(t.animate(run_time=base + 0.9 * i, rate_func=linear).move_to(e), touch(d, e),
                               Tw(lambda a: c.__setattr__("lit", 0.9 * (1 - a)), 0.6), FadeOut(t, scale=0.3, run_time=0.4))
                    for i, (t, e, (d, _)) in enumerate(zip(toks, ends, hits))])
        self.at("consumed oxygen", lead=0.0)
        feed.a = 1.0
        self.play(g.tw(1.2, there_and_back, lit=0.9))
        self.at("shielded")
        sh = shield(c)
        self.play(FadeIn(sh, run_time=0.9))
        self.finish()


class RelStream(Proc):
    """Schematic hydrogen bubbles passing from the lab-grown relative to its partner microbe."""

    def __init__(self, x0, x1, y, t0, n=4, gap=0.7, travel=2.0, z=26):
        self.x0, self.x1, self.y, self.t0, self.n, self.gap, self.travel, self.a = x0, x1, y, t0, n, gap, travel, 1.0
        self.tok = [h2_bubble(0.4) for _ in range(n)]
        self.mob = VGroup(*self.tok).set_z_index(z)
        for m in self.mob:
            m.set_opacity(0)
        self._k = [None] * n
        self._live()

    def draw(self):
        t = now() - self.t0
        P = self.n * self.gap
        for i, tk in enumerate(self.tok):
            lt = t - i * self.gap
            age = lt % P if lt >= 0 else -1.0
            o = 0.0
            if 0 <= age < self.travel:
                s = age / self.travel
                o = round(self.a * min(1.0, s / 0.1) * min(1.0, (1 - s) / 0.1), 2)
                tk.move_to([lerp(self.x0, self.x1, s), self.y + 0.12 * math.sin(3 * s + i), 0])
            if self._k[i] != o:
                tk.set_opacity(o)
                tk[0].set_fill(opacity=0.12 * o)
                tk[1].set_fill(opacity=0.85 * o)
                self._k[i] = o


def relative_panel():
    """Two simple shapes, drawn as a schematic: a lab-grown relative of the host and a partner microbe."""
    cell = Ellipse(width=4.2, height=3.0, stroke_color=BLUE, stroke_width=6, fill_color=BLUE, fill_opacity=0.22).move_to([-3.6, 0.45, 0])
    mic = RoundedRectangle(corner_radius=0.55, width=2.7, height=1.6, stroke_color="#7BD389", stroke_width=6,
                           fill_color="#7BD389", fill_opacity=0.22).move_to([3.7, 0.45, 0])
    l1 = label("lab-grown relative", 34, BLUE, (-3.6, -1.5), weight=SEMIBOLD)
    l2 = label("partner microbe", 34, "#7BD389", (3.7, -1.5), weight=SEMIBOLD)
    tag = label("schematic", 28, TEXT, (0, -2.55))
    for m in (cell, mic):
        m.set_z_index(25)
    return VGroup(cell, mic, l1, l2, tag)


class S17Open(Stage):
    def construct(self):
        W = why_world(self)
        g, c = W.g, W.cell
        W.scrub.a = 0.0
        host, guest, top = HOST(40, -2.6, 1.8), GUEST_W(GUEST_POS, 40), WHY_TOP(28)
        hg, og = why_badges()
        badge_focus(hg, og, "o")
        sh = shield(c)
        feed = O2Feed(g, T0.get("s16_oxygen", 0.0) + O2_AT)
        self.add(host, guest, top, hg, og, sh, feed.mob)
        hb, ob = hg[0], og[1]
        cen, rad = {"h": hb, "o": ob}, {"r": ORBIT_R}
        orb_h, orb_o = orbiters(lambda k: cen[k].get_center(), lambda: rad["r"])
        orb_h.set_opacity(0)
        orb_o.set_opacity(0)
        self.add(orb_h, orb_o)
        self.play(feed.tw(0.7, a=0.0), FadeOut(sh, run_time=0.8),
                  dim(hg, 1.0), rescale(og, 1 / 1.18, 0.8, RIGHT),
                  Tw(lambda a: (orb_h.set_opacity(a), orb_o.set_opacity(a)), 0.8))
        self.remove(feed.mob)
        pulse(hb, 0.09, 1.8)
        pulse(ob, 0.09, 1.8, PI)
        self.at("neither is proven", lead=0.4)
        self.play(Transform(top, label("neither is proven", 40, TEXT, (0, CARD_Y), weight=SEMIBOLD), run_time=0.7))
        self.at("A close relative", lead=0.6)
        panel = relative_panel()
        self.play(Tw(lambda a: setattr(W, "veil_a", 0.95 * a), 0.8),
                  FadeOut(host, run_time=0.6), FadeOut(guest, run_time=0.6),
                  dim(hg, 0.35, 0.8), dim(og, 0.35, 0.8),
                  Tw(lambda a: (orb_h.set_opacity(1 - a), orb_o.set_opacity(1 - a)), 0.6))
        self.play(FadeIn(panel, run_time=0.6))
        self.at("trading hydrogen", lead=0.2)
        rs = RelStream(-1.3, 2.3, 0.45, now() + 0.1)
        self.add(rs.mob)
        self.at("partnerships like this", lead=0.3)
        self.play(panel[1].animate(run_time=0.9, rate_func=there_and_back).scale(1.06))
        self.finish()


ORBIT_R, ORBIT_BIG = 0.47, 0.74          # the dots circle the gold badge only (a small one, then the merged big one)


def BIG_Q():
    return gold_badge(0.42).move_to([0, 3.0, 0]).set_z_index(21)


SCHEM_TAG = lambda: label("schematic: not a gene count", 28, TEXT, (2.3, CARD_Y))
ORG_LAB = lambda: label("organelle", 34, PINK, (2.3, -1.3))
NUCL_LAB = lambda: label("nucleus", 32, BLUE, (-3.25, -1.2))


class S18Genes(Stage):
    def construct(self):
        W = why_world(self)
        g, c, nuc, nr = W.g, W.cell, W.nuc, W.nring
        W.scrub.a = 0.0
        nr.pk = 1.0
        nr.ba[18:30] = 0.0
        host, guest, big = HOST(40, -2.6, 1.8), GUEST_W(GUEST_POS, 40), BIG_Q()
        orb_h, orb_o = orbiters(lambda k: big.get_center(), lambda: ORBIT_BIG)
        r40 = Ring(g, A40, PINK, R40K, B40K, a=0.0)
        tag = SCHEM_TAG()                                    # s17 now ends on the lab-relative panel, so the old '?' and labels are not drawn here
        self.add(r40.mob)
        self.play(
                  c.tw(0.8, grab=[0, 0, 0, 0, 0]), W.scrub.tw(0.8, a=1.0),
                  *W.to(GEN0, 2.2, only=("cell", "nuc", "g")), W.rfull.tw(1.4, a=0.0), Succession(Wait(0.9), r40.tw(1.2, a=1.0)),
                  Succession(Wait(1.4), FadeIn(tag, shift=DOWN * 0.1, run_time=0.8)))
        self.at("Over time")
        tA, tB, k0 = self.elapsed(), self.narration_s + 0.3, W.scrub.knob
        W.scrub.fn = lambda: lerp(k0, K18, min(1.0, max(0.0, (self.elapsed() - tA) / (tB - tA))))
        nuc.set(solid=1.0, sdraw=0.0)
        self.play(nuc.tw(0.9, sdraw=1.0), nuc.tw(0.9, dash=0.0), nuc.tw(0.7, q=0.0), W.scrub.tw(0.9, words=0.0))
        self.at("an organelle", lead=0.3)
        org = ORG_LAB()
        self.play(g.tw(1.5, bean=1.0, H=2.7, fold=0.6), Succession(Wait(0.6), Write(org, run_time=0.6)))
        self.play(g.tw(1.2, there_and_back, lit=0.5))
        self.at("Many of its")

        def lose(i, k):
            b, st = r40.beads[i], {}

            def f(a):
                if not st:
                    if a <= 0:
                        return
                    r40.live[i] = False
                    c, _, br = r40.geom()
                    d = b.get_center() - c
                    st["p"], st["d"], st["r"] = b.get_center(), d / (np.linalg.norm(d) + 1e-9), br
                p = st["p"] + st["d"] * 0.6 * (1 - (1 - a) ** 2) + np.array([0.0, -0.25 * a * a, 0.0])
                b.set_points(circ(p, st["r"] * (1 + 0.6 * min(1.0, a * 4))))
                b.set_fill(interpolate_color(ManimColor(PINK), ManimColor("#A9B1BF"), min(1.0, a * 4)), opacity=min(1.0, 2.5 * (1 - a)))
            return Tw(f, 1.4, linear)
        self.play(LaggedStart(*[lose(i, k) for k, i in enumerate(LOST)], lag_ratio=0.12, run_time=self.gap("Others moved", lead=0.25)))
        nl = NUCL_LAB()

        def move(i, j):
            b, st = r40.beads[i], {}

            def f(a):
                if not st:
                    if a <= 0:
                        return
                    r40.live[i] = False
                    st["p"] = b.get_center()
                tgt = nr.pos(18 + j)
                p = st["p"] + (tgt - st["p"]) * a + np.array([0, 0.7 * math.sin(PI * a), 0])
                b.set_points(circ(p, lerp(B40K * g.H, nr.geom()[2], a)))
                if a >= 1:
                    b.set_fill(opacity=0)
                    nr.ba[18 + j] = 1.0
            return Tw(f, 1.0)
        self.play(LaggedStart(*[move(i, j) for j, i in enumerate(MOVED)], lag_ratio=0.09, run_time=self.rest(0.25)), Write(nl, run_time=0.6))
        self.finish()


def count_texts(pos):
    return VGroup(*[M(str(i + 1), size=64, color=PINK).move_to(pos).set_opacity(0) for i in range(13)]).set_z_index(20)


MT_LAB = lambda: label("human mtDNA: 13 proteins", 34, PINK, (0.5, CARD_Y))
RESP_LAB = lambda: label("respiration + making ATP", 30, YELLOW, (0.5, -1.92))
COUNT_POS = (2.5, 0.05)


class S19Thirteen(Stage):
    def construct(self):
        W = self.world(mix(GEN1, sparks=dict(lab=1.0)))
        g, rk = W.g, W.rk
        tag, org, nl = SCHEM_TAG(), ORG_LAB(), NUCL_LAB()
        self.add(tag, org, nl)
        self.play(W.scrub.tw(1.0, knob=TODAY), FadeOut(org, run_time=0.5), FadeOut(nl, run_time=0.5),
                  *W.to(mix(ZOOM, g=dict(tiles=0.0)), 1.9, only=("cell", "g")), W.nuc.tw(0.6, a=0.0), W.nuc.tw(1.9, x=ZOOM["nuc"]["x"]),
                  tag.animate(run_time=1.9).move_to([0.5, CARD_Y, 0]), Succession(Wait(0.7), rk.tw(1.5, tight=1.0)))
        self.at("Human")
        self.play(rk.tw(1.3, there_and_back, lit=0.8))
        self.at("encodes", lead=0.1)
        nums = count_texts(P3(COUNT_POS))
        self.add(nums)

        def count(a):
            k = min(12, int(a * 13))
            rk.hl[:] = 0
            if a < 1:
                rk.hl[k] = 1.0
            for i, n in enumerate(nums):
                n.set_opacity(1.0 if i == k else 0.0)
        self.play(Tw(count, 1.8, linear), FadeOut(tag, run_time=0.5), Succession(Wait(0.3), FadeIn(MT_LAB(), run_time=0.6)))
        self.at("All 13", lead=0.3)
        tiles = VGroup(*[Rectangle(width=0.1, height=0.28, stroke_color="#FFE3EC", stroke_width=1.5, fill_color=PINK, fill_opacity=1).move_to(rk.pos(i)).set_z_index(-7)
                         for i in range(13)]).set_opacity(0)
        self.add(tiles)

        def fly(k):
            tile, st = tiles[k], {}

            def f(a):
                if not st:
                    if a <= 0:
                        return
                    st["p"] = rk.pos(k)
                    rk.hl[k] = 1.0
                    tile.set_opacity(1)
                tile.move_to(st["p"] + (g.gappos(k) - st["p"]) * a + np.array([0.3 * math.sin(PI * a), 0, 0]))
                rk.hl[k] = max(0.0, 1 - 2 * a)
                if a >= 1:
                    tile.set_opacity(0)
                    g.tiles = max(g.tiles, k + 1)
            return Tw(f, 0.55)
        self.play(LaggedStart(*[fly(k) for k in range(13)], lag_ratio=0.1))
        self.at("respiration", lead=0.3)
        rl = RESP_LAB()
        g.surge = 0.0
        self.play(g.tw(1.2, linear, surge=1.0), Write(rl, run_time=0.6), FadeOut(nums, run_time=0.6))
        g.surge = -1.0
        self.at("making ATP")
        self.play(W.sparks.tw(1.0, a=1.0), g.tw(1.2, rowglow=0.5))
        self.at("powers your cells", lead=0.3)
        self.play(g.tw(1.4, there_and_back, rowglow=1.0), g.tw(1.4, there_and_back, lit=0.5))
        self.finish()


IDEA_BADGE = lambda: VGroup(gold_badge(0.26), label("one idea, still argued over", 32, GOLD, (0, 0))).arrange(RIGHT, buff=0.18).move_to([0, CARD_Y, 0]).set_z_index(21)


def sixteen(W, k=4, arrange=True):
    """The 16 mitochondria of the payoff. Bean 0 is the big one; two others are the world's small beans."""
    beans = [W.g] + [None] * 15
    beans[3], beans[5] = W.small[0], W.small[1]
    for i in range(1, 16):
        if beans[i] is None:
            beans[i] = Guest(bean=1.0, detail=0.0, dota=1.0, n=70, seed=i * 0.9, a=0.0)
    for i, b in enumerate(beans):
        if arrange and i < 2 ** k:
            x, y = stage_pos(i, k)
            b.set(x=x, y=y, L=STAGE[k][0], H=STAGE[k][1], a=1.0, warm=1.0, ang=A16[i], bean=1.0, pinch=0.0)
            if i:
                b.set(detail=0.0, dota=1.0)
    return beans


def inner_membranes(nuc_xy=(-3.3, 0.3)):
    c = P3(nuc_xy)
    arc = lambda R, d: VMobject(fill_opacity=0).set_points_smoothly([c + R * np.array([math.cos(a), math.sin(a), 0]) for a in np.radians(np.linspace(180 - d, 180 + d, 24))]).set_stroke(BLUE, width=4.5)
    return VGroup(arc(1.8, 52), arc(2.1, 46)).set_z_index(-39)


class S20Payoff(Stage):
    def construct(self):
        W = self.world(mix(ZOOM))
        g, c, nuc, nr, sp = W.g, W.cell, W.nuc, W.nring, W.sparks
        sp.target = P3(-3.3, 0.3)
        mt, rl = MT_LAB(), RESP_LAB()
        self.add(mt, rl)
        g.rowglow = 0.5
        self.play(*[FadeOut(m, run_time=0.5) for m in (mt, rl)], *W.to(PAY, 1.7, only=("cell", "g")), sp.tw(0.5, lab=0.0),
                  nuc.tw(1.7, **{k: PAY["nuc"][k] for k in "xyr"}), Succession(Wait(1.0), nuc.tw(0.7, a=1.0)))
        self.play(c.tw(0.9, there_and_back, lit=0.9), nuc.tw(0.9, there_and_back, lit=0.9))
        self.at("most of your", lead=0.6)
        most = label("most of your ATP", 32, YELLOW, (1.6, -1.42), weight=SEMIBOLD)
        self.play(sp.tw(1.6, spread=1.0), c.tw(1.6, warm=0.6), Write(most, run_time=0.6))
        self.at("One influential idea", lead=0.4)
        idea = IDEA_BADGE()
        self.play(FadeOut(most, run_time=0.6), FadeIn(idea, shift=DOWN * 0.15, run_time=0.9))
        pulse(idea[0])
        self.at("goes further")
        self.play(g.tw(1.4, there_and_back, rowglow=1.0), c.tw(1.4, there_and_back, warm=1.0))
        self.at("many mitochondria", lead=0.5)
        beans = sixteen(W, 0, arrange=False)
        for b in beans[1:]:
            b.a = 0.0
            if b not in W.small:
                self.add(b.mob)
        ms = MiniSparks(beans)
        ms.a = 1.0
        self.add(ms.mob)
        self.play(g.tw(0.5, detail=0.0, chain=0.0, spark=0.0, dota=1.0, warm=1.0), W.rk.tw(0.5, a=0.0), g.tw(0.5, rush_into, pinch=1.0))
        for k in range(4):
            if k:
                self.play(*[beans[j].tw(0.3, rush_into, pinch=1.0) for j in range(2 ** k)])
            for j in range(2 ** k):
                split(beans[j], beans[j + 2 ** k])
            L, H = STAGE[k + 1]
            self.play(*[beans[j].tw(0.45, x=stage_pos(j, k + 1)[0], y=stage_pos(j, k + 1)[1], L=L, H=H, ang=A16[j])
                        for j in range(2 ** (k + 1))])
        self.at("larger genomes", lead=0.3)
        self.play(nuc.tw(1.5, r=1.5), nr.tw(1.5, Rk=0.72, bx=1.0), sp.tw(1.2, toward=0.6), nr.tw(1.5, there_and_back, lit=0.6))
        self.at("more complex lives", lead=0.3)
        mem = inner_membranes()
        self.play(c.tw(1.4, x=0.0, y=0.2, w=12.4, h=5.1), LaggedStart(*[Create(m) for m in mem], lag_ratio=0.3, run_time=1.5))
        self.finish()


class S21Answer(Stage):
    def construct(self):
        W = self.world(MANY)
        g, c, sp = W.g, W.cell, W.sparks
        sp.target = P3(-3.3, 0.3)
        beans = sixteen(W, 4)
        for b in beans[1:]:
            if b not in W.small:
                self.add(b.mob)
        ms = MiniSparks(beans)
        ms.a = 1.0
        mem, idea = inner_membranes(), IDEA_BADGE()
        self.add(ms.mob, mem, idea)
        pulse(idea[0])
        self.at("look again", lead=0.45)
        own = label("their own DNA", 34, PINK, P_OWN)
        back = mix(MODF, scrub=dict(a=0.0, words=0.0))      # the bare scrubber fades; its words do not flash back
        self.play(FadeOut(idea, run_time=0.6), FadeOut(mem, run_time=0.8), ms.tw(0.6, a=0.0),
                  *[b.tw(1.0, a=0.0, x=lerp(b.x, 2.0, 0.6), y=lerp(b.y, -0.3, 0.6)) for b in beans[1:] if b not in W.small],
                  *[b.tw(1.4, warm=0.0) for b in W.small], *W.to(back, 1.4, only=("cell", "nuc", "nring", "g", "s0", "s1", "scrub", "sparks")),
                  Succession(Wait(0.6), W.r13.tw(0.8, a=1.0)), Succession(Wait(0.9), FadeIn(own, run_time=0.5)))
        self.at("Why would")
        q = card(Q_HOOK)
        self.play(Write(q, run_time=0.6))
        self.wait(0.6)
        self.play(g.tw(1.2, there_and_back, lit=0.7))
        self.at("its ancestor", lead=0.3)
        rod = rod_outline(g.x, g.y, 4.2, 1.7)
        self.add(rod)
        ans = answer_card()
        self.play(flicker(rod, 1.4), FadeOut(q, run_time=0.4), Succession(Wait(0.2), FadeIn(ans, run_time=0.5)))      # whole before "was one"; it holds into s22
        self.remove(rod)
        self.finish()


def answer_card():
    return T("Its ancestor was one.", size=44, weight=SEMIBOLD, t2c={"ancestor": PINK}).move_to([0, CARD_Y, 0]).set_z_index(22)


CHAIN_PTR = lambda: Line([2.0, -1.59, 0], [2.0, -1.33, 0], color=YELLOW, stroke_width=4).set_z_index(20)
INHERIT = lambda: label("inherited from the guest", 32, TEXT, P_MITO)


class S22Return(Stage):
    def construct(self):
        W = self.world(MODF)
        g, c = W.g, W.cell
        q, own = answer_card(), label("their own DNA", 34, PINK, P_OWN)
        self.add(q, own)
        o2 = O2Stream(g, now())
        self.add(o2.mob)
        self.play(FadeOut(own, run_time=0.6))            # the answer line stays through "Every breath you take"
        self.at("a chain", lead=0.4)
        ch, ptr = label("the chain", 32, YELLOW, P_MITO, weight=SEMIBOLD), CHAIN_PTR()
        self.play(FadeOut(q, run_time=0.5), g.tw(0.8, rowglow=0.8), Write(ch, run_time=0.6), Create(ptr, run_time=0.5))
        self.at("inherited", lead=0.0)
        self.play(Transform(ch, INHERIT(), run_time=0.8))
        self.at("ancient guest")
        self.play(g.tw(1.2, there_and_back, lit=0.5))
        self.at("Your mitochondria")
        self.play(c.tw(1.0, a=0.6), W.nuc.tw(1.0, a=0.6))
        self.at("began as a guest", lead=0.1)
        rod = rod_outline(g.x, g.y, 4.2, 1.7)
        self.add(rod)
        self.play(flicker(rod, 1.3))
        self.remove(rod)
        self.at("never left", lead=0.1)
        self.play(g.tw(1.5, there_and_back, lit=1.0))
        self.finish()


class S23End(Quiet):
    """End card: the take-home sentence on two lines over the living cell at 10%. No new oxygen sets out."""
    LINES = ["Your mitochondria descend from", "one bacterial guest that stayed."]

    def construct(self):
        W = self.world(mix(MODF, cell=dict(a=0.6), nuc=dict(a=0.6), g=dict(rowglow=0.8)))
        ch, ptr = INHERIT(), CHAIN_PTR()
        o2 = O2Stream(W.g, T0.get("s22_return", 0.0))
        o2.stop = now() - 0.6
        self.add(ch, ptr, o2.mob)
        t0 = now()
        W.veil_a = lambda: 0.90 * min(1.0, (now() - t0) / 0.5)
        for m in (ch, ptr):
            m.add_updater(lambda m, dt: m.set_opacity(max(0.0, 1 - (now() - t0) / 0.4)))
        lines = VGroup(*[T(t, size=48, font=TITLE_FONT) for t in self.LINES]).arrange(DOWN, buff=0.3)
        fit(lines, max_w=11.5)
        sub = T("biochemistrypedia.com", size=28, color=TEAL, weight=SEMIBOLD)
        VGroup(lines, sub).arrange(DOWN, buff=0.55).move_to([0, 0.1, 0]).set_z_index(30)
        self.play(FadeIn(lines, shift=UP * 0.15, run_time=0.9))
        self.play(FadeIn(sub, run_time=0.5))
        self.finish()
