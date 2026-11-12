"""Same Auxin, Opposite Bends  (plant-signals, film 2 of 2)

Keeps film 1's COLOUR MAP: auxin = GOLD dots (GOLD band where it piles up); light = BLUE arrow; lit flank PALE
green; shaded flank ORANGE; gravity = GREY down-arrow; PIN carriers = TEAL gates; starch statoliths = dark BROWN
grains; shoot curve ORANGE, root curve DEEP BROWN. Every curve is computed from one bell-shaped model and marked
schematic. Helpers (Film, Shoot, dots, rays, lamp) are borrowed from film 1's scenes.py.
"""
import importlib.util
import os
from pathlib import Path

import numpy as np
from bp_style import *  # noqa: F401,F403


def _load_film1():
    cands = []
    if os.environ.get("KX_SCRIPT"):
        cands.append(Path(os.environ["KX_SCRIPT"]).resolve().parent.parent / "scenes.py")
    cands.append(Path.cwd().parent / "scenes.py")
    if "__file__" in globals():
        cands.append(Path(__file__).resolve().parent.parent / "scenes.py")
    for p in cands:
        if p.exists():
            spec = importlib.util.spec_from_file_location("film1_scenes", p)
            m = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(m)
            return m
    raise RuntimeError("film 1 scenes.py not found")


F1 = _load_film1()
Shoot, rays, lamp, tracker_op, lab, smooth, jig = F1.Shoot, F1.rays, F1.lamp, F1.tracker_op, F1.lab, F1.smooth, F1.jig
_Base = F1.Film


class Film(_Base):
    """Film 1's scene base plus a field of slowly drifting motes behind everything (never a dead frame)."""
    MOTES = True

    def setup(self):
        super().setup()
        if not self.MOTES:
            return
        rng = np.random.RandomState(abs(hash(os.environ.get("KX_SCENE_ID", "x"))) % 9999)
        ms = VGroup()
        for _ in range(22):
            d = Dot(radius=rng.uniform(0.05, 0.1), color=rng.choice([TEAL, GREY, TEXT])).set_opacity(rng.uniform(0.18, 0.35))
            d.move_to([rng.uniform(-7, 7), rng.uniform(-4, 4), 0])
            d.v = (rng.uniform(-0.25, 0.25), rng.uniform(0.15, 0.4))

            def drift(m, dt):
                m.shift([m.v[0] * dt, m.v[1] * dt, 0])
                if m.get_y() > 4.1:
                    m.shift(DOWN * 8.2)
                if abs(m.get_x()) > 7.2:
                    m.shift(LEFT * 14.4 * np.sign(m.get_x()))
            d.add_updater(drift)
            ms.add(d)
        ms.set_z_index(-10)
        self.add(ms)


PALE, ORANGE, LEAF, SILVER = F1.PALE, F1.ORANGE, F1.LEAF, F1.SILVER

GRAV = "#B8BFC8"
BODY = {"shoot": "#4f9a5e", "root": "#d6c496"}
SEEDC = "#C9A66B"
BROWN = "#5a3a1e"
DEEPBROWN = "#6B3A1A"
WARM = "#E8801F"
CELLC = "#efe6c4"
WALL = "#9c8760"
PANEL = "#F3ECD6"
INK = "#2b2b2b"
GOOD = "#6FCF6F"
BAD = "#FF7A6B"


# --------------------------------------------------------------------------- organs
class Organ:
    """A shoot (heading right) or root (heading left) lying on its side. u > 0 is the upper flank at tilt 0."""
    Z0, Z1 = 0.35, 0.9
    ROWS = ((-0.5, -0.18, "lo"), (-0.18, 0.18, ""), (0.18, 0.5, "up"))

    def __init__(self, scene, kind, base, L, w, K=10, bend=0.0, op=1.0, tilt=0.0, pivot=None, edge=BG,
                 cells=0.0, band=0.0, fill=None):
        self.kind, self.sg = kind, (1 if kind == "shoot" else -1)
        self.h0 = 0.0 if kind == "shoot" else float(np.pi)
        self.base = np.array([base[0], base[1], 0.0])
        self.pivot = None if pivot is None else np.array([pivot[0], pivot[1], 0.0])
        self.w, self.K, self.N, self.edge = w, K, K * 4, edge
        self.fill = fill or BODY[kind]
        for nm, v in (("L", L), ("bend", bend), ("op", op), ("tilt", tilt), ("cells", cells), ("band", band),
                      ("hl_lo", 0.0), ("hl_up", 0.0)):
            t = ValueTracker(v)
            setattr(self, nm, t)
            scene.add(t)
        self._key = None
        self._val = None
        self.body = always_redraw(self._draw)
        self.bandm = always_redraw(self._draw_band)
        scene.add(self.body, self.bandm)

    def cl(self):
        tl = self.tilt.get_value()
        key = (round(self.L.get_value(), 4), round(self.bend.get_value(), 4), round(tl, 4))
        if key == self._key:
            return self._val
        L, bend = key[0], key[1]
        if self.pivot is None:
            b = self.base.copy()
        else:
            d = self.base - self.pivot
            c, s = np.cos(tl), np.sin(tl)
            b = self.pivot + np.array([c * d[0] - s * d[1], s * d[0] + c * d[1], 0.0])
        head = self.h0 + tl
        N = self.N
        pts, ths = [b], [head]
        ds = L / N
        for i in range(1, N + 1):
            th = head + bend * smooth(((i - 0.5) / N - self.Z0) / (self.Z1 - self.Z0))
            pts.append(pts[-1] + np.array([np.cos(th), np.sin(th), 0.0]) * ds)
            ths.append(head + bend * smooth((i / N - self.Z0) / (self.Z1 - self.Z0)))
        self._key, self._val = key, (np.array(pts), np.array(ths))
        return self._val

    def point(self, s, u=0.0):
        pts, ths = self.cl()
        f = float(np.clip(s, 0, 1)) * self.N
        i = min(int(f), self.N - 1)
        r = f - i
        p = pts[i] * (1 - r) + pts[i + 1] * r
        th = ths[i] * (1 - r) + ths[i + 1] * r
        n = self.sg * np.array([-np.sin(th), np.cos(th), 0.0])
        return p + n * u * self.w

    def _edge(self, i, u):
        pts, ths = self.cl()
        th = ths[i]
        return pts[i] + self.sg * np.array([-np.sin(th), np.cos(th), 0.0]) * u * self.w

    def _poly(self, i0, i1, a, b, fill, stroke, sw, o, fo=0.95):
        A = [self._edge(i, a) for i in range(i0, i1 + 1)]
        B = [self._edge(i, b) for i in range(i0, i1 + 1)]
        return Polygon(*(A + B[::-1]), stroke_color=stroke, stroke_width=sw, stroke_opacity=o,
                       fill_color=fill, fill_opacity=fo * o)

    def _draw(self):
        o = self.op.get_value()
        if o < 0.02:
            return VGroup(Dot(ORIGIN, radius=0.001).set_opacity(0))
        c = self.cells.get_value()
        g = VGroup()
        for (a, b, nm) in self.ROWS:
            hl = self.hl_lo.get_value() if nm == "lo" else (self.hl_up.get_value() if nm == "up" else 0.0)
            sc = interpolate_color(ManimColor(self.fill), ManimColor(self.edge), c)
            if hl > 0.01:
                sc = interpolate_color(sc, ManimColor(YELLOW), min(1, hl))
            for k in range(self.K):
                g.add(self._poly(4 * k, 4 * k + 4, a, b, self.fill, sc, 3 + 2 * hl, o))
        return g

    def _draw_band(self):
        b = self.band.get_value() * self.op.get_value()
        if b < 0.02:
            return VGroup(Dot(ORIGIN, radius=0.001).set_opacity(0))
        return self._poly(2, self.N, -0.5, -0.28, GOLD, GOLD, 1, 1.0, fo=0.5 * b).set_stroke(opacity=0)


def gdots(scene, n, posfn, op=None, r=0.09):
    def build():
        c = scene.clock.get_value()
        o = 1.0 if op is None else op.get_value()
        g = VGroup(Dot(ORIGIN, radius=0.001).set_opacity(0))
        if o < 0.02:
            return g
        for i in range(n):
            p, m = posfn(i, c)
            if o * m > 0.02:
                d = Dot(p, radius=r, color=GOLD, stroke_width=2, stroke_color="#3a2a05")
                d.set_opacity(min(1, o * m))
                g.add(d)
        return g
    m = always_redraw(build)
    scene.add(m)
    return m


def flank_dots(scene, org, n, P, op, seed=1, r=0.11):
    rng = np.random.RandomState(seed)
    sp = [(rng.uniform(0.12, 0.95), rng.uniform(-0.38, 0.38), rng.uniform(-0.46, -0.36)) for _ in range(n)]

    def pf(i, c):
        s, u0, u1 = sp[i]
        u = u0 + (u1 - u0) * smooth(P.get_value())
        s = 0.1 + ((s - 0.1 + 0.05 * c) % 0.87)
        j = np.array([0.12 * np.sin(c * 0.9 + i * 1.7), 0.08 * np.cos(c * 0.8 + i * 2.3), 0.0])
        return org.point(s, u) + j, float(np.sin(np.pi * (s - 0.1) / 0.87) ** 0.4)
    return gdots(scene, n, pf, op, r)


def garrow(x, y0, y1, color=GRAV):
    return Arrow([x, y0, 0], [x, y1, 0], buff=0, color=color, stroke_width=9, tip_length=0.35)


def seed_mob(sh, center=(0, 0.4)):
    return always_redraw(lambda: Ellipse(width=1.5, height=1.0, fill_color=SEEDC, fill_opacity=1, stroke_color=WALL,
                                         stroke_width=3).rotate(sh.tilt.get_value()).move_to([center[0], center[1], 0])
                         .set_opacity(sh.op.get_value()))


def world(scene, bs=0.0, br=0.0, band=0.0, tilt=0.0, L=5.4):
    piv = (0, 0.4)
    sh = Organ(scene, "shoot", (0.6, 0.4), L, 1.4, bend=bs, tilt=tilt, pivot=piv, band=band)
    rt = Organ(scene, "root", (-0.6, 0.4), L, 1.4, bend=br, tilt=tilt, pivot=piv, band=band)
    sd = seed_mob(sh)
    scene.add(sd)
    return sh, rt, sd


def grav_world(scene):
    a = garrow(0, -0.9, -2.7)
    t = lab("gravity", 1.55, -1.8, 28, GRAV)
    scene.add(a, t)
    return a, t


# --------------------------------------------------------------------------- root tip / cell
RC = np.array([-3.0, 0.0, 0.0])
CC = np.array([3.3, 0.0, 0.0])
SIL = [(-1.2, 1.7), (1.2, 1.7), (1.2, 0.0), (1.0, -0.8), (0.5, -1.4), (0.0, -1.7), (-0.5, -1.4), (-1.0, -0.8), (-1.2, 0.0)]
GRAINS = [(x, -1.5) for x in (-1.2, -0.6, 0.0, 0.6, 1.2)] + [(x, -0.97) for x in (-0.9, -0.3, 0.3, 0.9)]


def rot(v, a):
    c, s = np.cos(a), np.sin(a)
    return np.array([c * v[0] - s * v[1], s * v[0] + c * v[1], 0.0])


class Tip:
    def __init__(self, scene, tilt=0.0, glow=0.0, root_op=1.0, cell_op=0.0, cs=1.0, G=0.0, D=1.0, gop=0.0, link=0.0):
        self.s = scene
        for nm, v in (("tilt", tilt), ("glow", glow), ("root_op", root_op), ("cell_op", cell_op), ("cs", cs),
                      ("G", G), ("D", D), ("gop", gop), ("link", link)):
            t = ValueTracker(v)
            setattr(self, nm, t)
            scene.add(t)
        self.mobs = [always_redraw(self._root), always_redraw(self._links), always_redraw(self._cell),
                     always_redraw(self._grains)]
        scene.add(*self.mobs)

    def _root(self):
        o = self.root_op.get_value()
        if o < 0.02:
            return VGroup(Dot(ORIGIN, radius=0.001).set_opacity(0))
        tl = self.tilt.get_value()
        c = self.s.clock.get_value()
        sil = Polygon(*[RC + np.array([x, y, 0]) for x, y in SIL], stroke_color=WALL, stroke_width=4,
                      fill_color=BODY["root"], fill_opacity=0.95 * o).round_corners(0.25)
        gl = self.glow.get_value() * (0.8 + 0.2 * np.sin(c * 3))
        cols = VGroup()
        for xi in (-0.55, 0.0, 0.55):
            for yy in (-0.35, -0.9):
                r = Rectangle(width=0.55, height=0.55, stroke_color=interpolate_color(ManimColor(WALL), ManimColor(YELLOW), self.glow.get_value()),
                              stroke_width=3, fill_color=interpolate_color(ManimColor(CELLC), ManimColor(YELLOW), 0.6 * gl),
                              fill_opacity=0.95 * o).move_to(RC + np.array([xi, yy, 0]))
                cols.add(r)
        g = VGroup(sil, cols)
        g.rotate(tl, about_point=RC)
        return g

    def _links(self):
        l = self.link.get_value()
        if l < 0.02:
            return VGroup(Dot(ORIGIN, radius=0.001).set_opacity(0))
        cs = self.cs.get_value()
        a = Line(RC + np.array([0.83, -0.1, 0]), CC + np.array([-1.8, 1.8, 0]) * cs, color=YELLOW, stroke_width=3).set_opacity(0.8 * l)
        b = Line(RC + np.array([0.83, -1.15, 0]), CC + np.array([-1.8, -1.8, 0]) * cs, color=YELLOW, stroke_width=3).set_opacity(0.8 * l)
        return VGroup(a, b)

    def _cell(self):
        o = self.cell_op.get_value()
        if o < 0.02:
            return VGroup(Dot(ORIGIN, radius=0.001).set_opacity(0))
        cs = self.cs.get_value()
        tl = self.tilt.get_value()
        sq = Square(3.6 * cs, stroke_color=WALL, stroke_width=5, fill_color=CELLC, fill_opacity=0.97 * o).move_to(CC)
        sq.set_stroke(opacity=o)
        wall = Line(CC + np.array([-1.8, -1.8, 0]) * cs, CC + np.array([1.8, -1.8, 0]) * cs, color="#8a6d3b", stroke_width=14).set_opacity(o)
        g = VGroup(sq, wall)
        g.rotate(tl, about_point=CC)
        return g

    def _grains(self):
        gop = self.gop.get_value()
        g = VGroup(Dot(ORIGIN, radius=0.001).set_opacity(0))
        if gop < 0.02 or self.cell_op.get_value() < 0.02:
            return g
        cs, tl, G, D = self.cs.get_value(), self.tilt.get_value(), self.G.get_value(), self.D.get_value()
        c = self.s.clock.get_value()
        for i, (x, y) in enumerate(GRAINS):
            q = np.array([x, y, 0.0])
            gi = smooth(np.clip(G * 1.45 - 0.05 * i, 0, 1))
            di = smooth(np.clip(D * 1.45 - 0.05 * i, 0, 1))
            p = rot(q, tl) * (1 - gi) + q * gi
            p = p + np.array([0, (1 - di) * 1.4, 0])
            p = p + np.array([0.012 * np.sin(c * 2 + i), 0.012 * np.cos(c * 2.3 + i), 0])
            g.add(Circle(radius=0.27 * cs, stroke_color="#2e1d0e", stroke_width=2, fill_color=BROWN,
                         fill_opacity=min(1, di * 3) * gop).move_to(CC + p * cs).set_stroke(opacity=min(1, di * 3) * gop))
        return g


def tip_extras(scene):
    a = garrow(-5.9, 1.2, -1.2)
    t = lab("gravity", -5.9, -1.75, 28, GRAV)
    scene.add(a, t)
    return a, t


# --------------------------------------------------------------------------- plot (cream card)
X0, XS, Y0, YS, SIG = -5.6, 0.66, -2.2, 4.0, 1.3
MU_S = 6.6


def PX(a, g):
    return np.array([X0 + a * XS, Y0 + YS * g, 0.0])


def gval(a, mu):
    return float(np.exp(-(a - mu) ** 2 / (2 * SIG ** 2)))


class Plot:
    def __init__(self, scene, mu_r=2.4, ps=1.0, pr=1.0, dim=1.0, axes=True):
        self.s = scene
        self.mu_r, self.ps, self.pr, self.dim = (ValueTracker(v) for v in (mu_r, ps, pr, dim))
        scene.add(self.mu_r, self.ps, self.pr, self.dim)
        self.panel = Rectangle(width=13.9, height=7.5, stroke_width=0, fill_color=PANEL, fill_opacity=1).move_to([0, 0, 0])
        self.axes = VGroup(
            Arrow([-5.9, Y0, 0], [1.3, Y0, 0], buff=0, color=INK, stroke_width=5, tip_length=0.22),
            Arrow([-5.9, Y0, 0], [-5.9, 2.7, 0], buff=0, color=INK, stroke_width=5, tip_length=0.22))
        self.xl = lab("auxin level (log scale)", -2.3, -2.8, 28, INK)
        self.yl = lab("growth", -6.5, 0.2, 28, INK).rotate(PI / 2)
        self.note = lab("schematic shapes and positions", -2.3, -3.4, 24, INK)
        self.cs = always_redraw(lambda: self._curve(MU_S, self.ps, WARM, 0.0))
        self.cr = always_redraw(lambda: self._curve(self.mu_r.get_value(), self.pr, DEEPBROWN, 0.0))
        self.ls = always_redraw(lambda: self._clabel("shoot", MU_S, self.ps, "#C9650F", 1))
        self.lr = always_redraw(lambda: self._clabel("root", self.mu_r.get_value(), self.pr, DEEPBROWN, -1))
        scene.add(self.panel)
        if axes:
            scene.add(self.axes, self.xl, self.yl, self.note)
        scene.add(self.cs, self.cr, self.ls, self.lr)

    def _curve(self, mu, prog, col, _):
        p = prog.get_value()
        if p < 0.03:
            return VGroup(Dot(ORIGIN, radius=0.001).set_opacity(0))
        f = ParametricFunction(lambda a: PX(a, gval(a, mu)), t_range=[0.15, 0.15 + p * 9.7, 0.08], color=col, stroke_width=8)
        f.set_stroke(opacity=self.dim.get_value())
        return f

    def _clabel(self, text, mu, prog, col, side):
        if prog.get_value() < 0.97:
            return VGroup(Dot(ORIGIN, radius=0.001).set_opacity(0))
        t = lab(text, 0, 0, 30, col)
        t.move_to(PX(mu, 0.0) + np.array([1.05 * side, 3.8, 0]))
        t.set_opacity(self.dim.get_value())
        return t


def mini_organs(scene, bs=0.0, br=0.0, bs_band=0.0, br_band=0.0, op=1.0, labels=True):
    sh = Organ(scene, "shoot", (1.6, 1.0), 4.5, 1.0, K=8, bend=bs, op=op, edge="#5a4a2a", cells=1, band=bs_band)
    rt = Organ(scene, "root", (6.5, -0.9), 4.5, 1.0, K=8, bend=br, op=op, edge="#5a4a2a", cells=1, band=br_band)
    flank_dots(scene, sh, 9, sh.band, sh.op, seed=51)
    flank_dots(scene, rt, 9, rt.band, rt.op, seed=52)
    ls = lab("shoot", 2.3, 2.2, 30, "#C9650F")
    lr = lab("root", 5.7, -1.95, 30, DEEPBROWN)
    if labels:
        scene.add(ls, lr)
    return sh, rt, ls, lr


def marker(scene, mu, a_tr, color=GOLD):
    def halo():
        a = a_tr.get_value()
        c = scene.clock.get_value()
        return Circle(radius=0.32 + 0.1 * np.sin(c * 4), color=INK, stroke_width=4).set_stroke(opacity=0.6).set_fill(opacity=0).move_to(
            PX(a, gval(a, mu() if callable(mu) else mu)))
    scene.add(always_redraw(halo))
    return always_redraw(lambda: Dot(PX(a_tr.get_value(), gval(a_tr.get_value(), mu() if callable(mu) else mu)), radius=0.2,
                                     color=GOLD, stroke_width=4, stroke_color="#3a2a05").set_z_index(5))


# --------------------------------------------------------------------------- big organ poses
def big_root(scene, bend=0.0, band=1.0, cells=0.0):
    r = Organ(scene, "root", (4.6, 0.3), 9.2, 2.0, K=12, bend=bend, band=band, cells=cells, edge="#3a3320")
    return r


def big_shoot(scene, bend=0.0, band=1.0, cells=0.0):
    return Organ(scene, "shoot", (-4.6, 0.3), 9.2, 2.0, K=12, bend=bend, band=band, cells=cells, edge="#16301c")


# =========================================================================== scenes
class S00Title(TitleCard):
    TITLE = "Same Auxin, Opposite Bends"
    LESSON = "Auxin and Plant Hormones"


class S01Hook(Film):
    def construct(self):
        piv = (0, 0.4)
        sh = Organ(self, "shoot", (0.6, 0.4), 1.8, 1.4, tilt=PI / 2, pivot=piv, op=0)
        rt = Organ(self, "root", (-0.6, 0.4), 1.8, 1.4, tilt=PI / 2, pivot=piv, op=0)
        sd = seed_mob(sh)
        self.add(sd)
        self.play(sh.op.animate.set_value(1), rt.op.animate.set_value(1), run_time=0.8)
        self.play(sh.tilt.animate.set_value(0), rt.tilt.animate.set_value(0), sh.L.animate.set_value(5.4),
                  rt.L.animate.set_value(5.4), run_time=1.9, rate_func=smooth)
        ga, gt = grav_world(self)
        self.play(FadeIn(ga), FadeIn(gt), run_time=0.5)
        self.at("shoot turns up")
        self.play(sh.bend.animate.set_value(0.9), run_time=1.5, rate_func=smooth)
        self.at("root turns down")
        self.play(rt.bend.animate.set_value(1.0), run_time=1.6, rate_func=smooth)
        self.at("both gather")
        dop = tracker_op(self, 0)
        P = ValueTracker(0)
        self.add(P)
        flank_dots(self, sh, 12, P, dop, seed=3)
        flank_dots(self, rt, 12, P, dop, seed=4)
        self.play(dop.animate.set_value(1), run_time=0.5)
        self.play(P.animate.set_value(1), sh.band.animate.set_value(1), rt.band.animate.set_value(1), run_time=2.4, rate_func=smooth)
        self.at("how can one signal")
        q = lab("?", 0, 2.9, 80, YELLOW)
        q.add_updater(lambda m: m.move_to([0, 2.9 + 0.1 * np.sin(self.clock.get_value() * 3), 0]))
        self.play(FadeIn(q, scale=1.4), run_time=0.7)
        self.finish()


class S02Link(Film):
    def construct(self):
        sh = Shoot(self, 1.0, by=-3.5, h=5.0, cells=1, split=1)
        lp = lamp()
        self.add(lp)
        rop = tracker_op(self, 0)
        rays(self, -5.1, -1.4, [0.4, 1.4, 2.4], rop)
        Mv, G, dop = ValueTracker(0), ValueTracker(0), tracker_op(self, 0)
        self.add(Mv, G)
        rng = np.random.RandomState(7)
        spec = [(rng.uniform(0.2, 0.9), rng.uniform(0.08, 0.42)) for _ in range(12)]

        def pf(i, c):
            s0, u0 = spec[i]
            m = smooth(Mv.get_value())
            u = -u0 * (1 - 2 * m) if i < 6 else u0
            s = s0 * (1 - 0.8 * smooth(G.get_value()))
            return sh.point(s, u) + jig(i, c, 1.2) * 1.5, 1.0
        gdots(self, 12, pf, dop)
        self.play(FadeIn(lp), rop.animate.set_value(1), dop.animate.set_value(1), run_time=1.0)
        self.at("light moving")
        self.play(Mv.animate.set_value(1), run_time=1.8, rate_func=smooth)
        self.at("shaded flank")
        sl = lab("shaded flank", 4.4, -0.2, 28, ORANGE)
        self.play(FadeIn(sl), run_time=0.5)
        self.at("which grew faster")
        self.play(sh.bend.animate.set_value(0.55), run_time=2.0, rate_func=smooth)
        self.at("gravity moves")
        A = Arrow([-5.3, 1.4, 0], [-3.3, 1.4, 0], buff=0, color=BLUE, stroke_width=9, tip_length=0.35)
        self.play(rop.animate.set_value(0), FadeOut(sl), sh.bend.animate.set_value(0), FadeIn(A), run_time=1.6)
        self.at("same gold dots")
        gl = lab("gravity", -4.3, -0.6, 28, GRAV)
        self.play(Rotate(A, angle=-PI / 2, about_point=A.get_center()), A.animate.set_color(GRAV), FadeIn(gl),
                  run_time=1.4)
        self.play(G.animate.set_value(1), run_time=2.2, rate_func=smooth)
        self.at("this time though")
        up = Arrow([5.4, 0.2, 0], [5.4, 1.6, 0], buff=0, color=TEXT, stroke_width=8, tip_length=0.3)
        dn = Arrow([5.4, -0.2, 0], [5.4, -1.6, 0], buff=0, color=TEXT, stroke_width=8, tip_length=0.3)
        self.at("the shoot")
        t1 = lab("shoot", 6.1, 1.2, 28, TEXT)
        self.play(FadeIn(up), FadeIn(t1), run_time=0.5)
        self.at("the root")
        t2 = lab("root", 6.1, -1.2, 28, TEXT)
        self.play(FadeIn(dn), FadeIn(t2), run_time=0.5)
        self.finish()


class S03Sense(Film):
    def construct(self):
        tp = Tip(self, root_op=0)
        self.play(tp.root_op.animate.set_value(1), run_time=1.2)
        self.at("which way is down")
        a, t = tip_extras(self)
        self.play(FadeIn(a), FadeIn(t), run_time=0.6)
        self.at("in the root cap")
        rc = lab("root cap", -3.0, 2.55, 28, TEXT)
        self.play(FadeIn(rc), run_time=0.6)
        self.at("central cells")
        self.play(tp.glow.animate.set_value(1), run_time=0.9)
        self.at("columella cells")
        cl = lab("columella cells", -3.0, -2.6, 28, YELLOW)
        self.play(FadeIn(cl), run_time=0.6)
        self.at("hold plastids")
        tp.cs.set_value(0.3)
        self.play(tp.cell_op.animate.set_value(1), tp.link.animate.set_value(1), tp.cs.animate.set_value(1), run_time=1.1, rate_func=smooth)
        self.at("plastids packed")
        tp.gop.set_value(1)
        tp.D.set_value(0)
        self.play(tp.D.animate.set_value(1), run_time=1.3, rate_func=linear)
        self.at("dense starch")
        pl = lab("plastids packed with starch", 3.3, -2.65, 28, TEXT)
        self.play(FadeIn(pl), run_time=0.6)
        self.finish()


class S04Settle(Film):
    def construct(self):
        tp = Tip(self, cell_op=1, gop=1)
        tip_extras(self)
        self.wait(0.3)
        self.play(tp.tilt.animate.set_value(-PI / 2), run_time=1.6, rate_func=smooth)
        self.at("heavy plastids")
        self.play(tp.G.animate.set_value(1), run_time=2.6, rate_func=smooth)
        self.at("they act as statoliths")
        st = lab("statoliths:\none gravity sensor", 3.3, -2.95, 28, TEXT)
        self.play(FadeIn(st), run_time=0.7)
        self.finish()


class Gates:
    HALF = 1.8

    def __init__(self, scene, op=0.0, P=0.0, dop=0.0):
        self.s = scene
        self.op, self.P, self.dop = ValueTracker(op), ValueTracker(P), ValueTracker(dop)
        scene.add(self.op, self.P, self.dop)
        self.p0 = [-1.0 + 0.5 * k for k in range(8)]
        self.p1 = [(k - 3.5) * 0.12 for k in range(8)]
        scene.add(always_redraw(self._gates), always_redraw(self._dots))

    def pn(self, p):
        h = self.HALF
        p = ((p + 0.5) % 4) - 0.5
        if p < 0.5:
            return CC + np.array([p * 2 * h, -h, 0]), np.array([0, -1, 0]), 0
        if p < 1.5:
            return CC + np.array([h, -h + (p - 0.5) * 2 * h, 0]), np.array([1, 0, 0]), 1
        if p < 2.5:
            return CC + np.array([h - (p - 1.5) * 2 * h, h, 0]), np.array([0, 1, 0]), 0
        return CC + np.array([-h, h - (p - 2.5) * 2 * h, 0]), np.array([-1, 0, 0]), 1

    def _p(self, k):
        return self.p0[k] + (self.p1[k] - self.p0[k]) * smooth(self.P.get_value())

    def _gates(self):
        o = self.op.get_value()
        g = VGroup(Dot(ORIGIN, radius=0.001).set_opacity(0))
        if o < 0.02:
            return g
        for k in range(8):
            pos, n, vert = self.pn(self._p(k))
            r = RoundedRectangle(corner_radius=0.1, width=0.62, height=0.3, stroke_color=TEAL, stroke_width=2,
                                 fill_color=TEAL, fill_opacity=o).move_to(pos)
            if vert:
                r.rotate(PI / 2)
            r.set_stroke(opacity=o)
            g.add(r)
        return g

    def _dots(self):
        o = self.dop.get_value()
        g = VGroup(Dot(ORIGIN, radius=0.001).set_opacity(0))
        if o < 0.02:
            return g
        c = self.s.clock.get_value()
        for k in range(8):
            pos, n, _ = self.pn(self._p(k))
            for j in range(2):
                f = (c * 0.35 + j * 0.5 + k * 0.13) % 1
                d = Dot(pos + n * (-0.9 + 2.1 * f), radius=0.1, color=GOLD, stroke_width=2, stroke_color="#3a2a05")
                d.set_opacity(o * float(np.sin(np.pi * f) ** 0.5))
                g.add(d)
        return g


class S05Pin(Film):
    def construct(self):
        tp = Tip(self, tilt=-PI / 2, cell_op=1, G=1, D=1, gop=1)
        tip_extras(self)
        gt = Gates(self)
        self.play(gt.op.animate.set_value(1), run_time=0.6)
        self.at("oxen leaves cells")
        self.play(gt.dop.animate.set_value(1), run_time=0.6)
        self.at("pin proteins")
        pl = lab("PIN proteins", 3.3, -3.45, 28, TEAL)
        self.play(FadeIn(pl), run_time=0.5)
        self.at("arabidopsis")
        ar = lab("Arabidopsis", -3.0, -2.6, 28, TEXT)
        self.play(FadeIn(ar), run_time=0.5)
        self.at("pin 3")
        p3 = lab("PIN3", 3.3, -3.45, 28, TEAL)
        self.play(ReplacementTransform(pl, p3), run_time=0.5)
        self.at("moves quickly")
        self.play(gt.P.animate.set_value(1), run_time=self.left(1.0), rate_func=smooth)
        self.finish()


class S06Flow(Film):
    def construct(self):
        sh, rt, sd = world(self)
        self.add(*grav_world(self))
        dop = tracker_op(self, 0)
        Pr, Ps = ValueTracker(0), ValueTracker(0)
        self.add(Pr, Ps)
        flank_dots(self, rt, 14, Pr, dop, seed=11)
        flank_dots(self, sh, 14, Ps, dop, seed=12)
        self.play(dop.animate.set_value(1), run_time=0.7)
        self.at("flows toward")
        self.play(Pr.animate.set_value(1), rt.band.animate.set_value(1), run_time=2.8, rate_func=smooth)
        self.at("in the shoot")
        self.play(Ps.animate.set_value(1), sh.band.animate.set_value(1), run_time=2.4, rate_func=smooth)
        self.finish()


def predict_card(scene, timer=False):
    r = big_root(scene)
    scene.add(garrow(-6.1, 0.9, -1.9), lab("gravity", -6.0, -2.5, 28, GRAV))
    dop = tracker_op(scene, 1)
    P = ValueTracker(1)
    scene.add(P)
    flank_dots(scene, r, 14, P, dop, seed=21)
    return r, P, dop


class S07Predict(Film):
    def construct(self):
        r = big_root(self, band=0.0)
        self.add(garrow(-6.1, 0.9, -1.9), lab("gravity", -6.0, -2.5, 28, GRAV))
        r.op.set_value(0)
        dop = tracker_op(self, 0)
        P = ValueTracker(0)
        self.add(P)
        flank_dots(self, r, 14, P, dop, seed=21)
        self.play(r.op.animate.set_value(1), run_time=1.4)
        self.play(dop.animate.set_value(1), run_time=0.8)
        self.at("now apply it to the root")
        rl = lab("root", 3.9, 1.95, 34, TEXT)
        self.play(FadeIn(rl), run_time=0.6)
        self.at("oxen piles up")
        self.play(P.animate.set_value(1), r.band.animate.set_value(1), run_time=2.2, rate_func=smooth)
        self.at("does that flank")
        qt = lab("Lower flank: faster or slower than the top?", -0.8, 3.1, 32, YELLOW)
        self.play(FadeIn(qt), run_time=0.8)
        self.at("faster")
        a1 = Arrow([-0.5, -1.55, 0], [-3.6, -1.55, 0], buff=0, color=GOOD, stroke_width=9, tip_length=0.35)
        l1 = lab("faster?", -2.0, -2.3, 34, GOOD)
        self.play(Create(a1), FadeIn(l1), run_time=0.8)
        self.at("slower")
        a2 = Arrow([2.9, -1.55, 0], [2.0, -1.55, 0], buff=0, color=BAD, stroke_width=9, tip_length=0.3)
        l2 = lab("slower?", 2.4, -2.3, 34, BAD)
        self.play(Create(a2), FadeIn(l2), run_time=0.8)
        self.finish()


class S08Pause(Film):
    def construct(self):
        r = big_root(self)
        self.add(garrow(-6.1, 0.9, -1.9), lab("gravity", -6.0, -2.5, 28, GRAV))
        dop = tracker_op(self, 1)
        P = ValueTracker(1)
        self.add(P)
        flank_dots(self, r, 14, P, dop, seed=21)
        self.add(lab("Lower flank: faster or slower than the top?", -0.8, 3.1, 32, YELLOW), lab("root", 3.9, 1.95, 34, TEXT))
        self.add(Arrow([-0.5, -1.55, 0], [-3.6, -1.55, 0], buff=0, color=GOOD, stroke_width=9, tip_length=0.35),
                 lab("faster?", -2.0, -2.3, 34, GOOD),
                 Arrow([2.9, -1.55, 0], [2.0, -1.55, 0], buff=0, color=BAD, stroke_width=9, tip_length=0.3),
                 lab("slower?", 2.4, -2.3, 34, BAD))
        T_ = ValueTracker(1)
        self.add(T_)
        T_.add_updater(lambda m, dt: m.set_value(max(0, m.get_value() - dt / 4.8)))
        ctr = np.array([5.9, 2.9, 0])
        self.add(Circle(radius=0.55, color=GREY, stroke_width=3).move_to(ctr))
        self.add(always_redraw(lambda: Arc(radius=0.55, start_angle=PI / 2, angle=-TAU * max(0.001, T_.get_value()),
                                           color=YELLOW, stroke_width=7).move_arc_center_to(ctr)))
        self.add(always_redraw(lambda: lab(str(int(np.ceil(T_.get_value() * 5 - 1e-6))), ctr[0], ctr[1], 28, YELLOW)))
        self.wait(self.left(0.05))
        self.finish()


class S09Reveal(Film):
    def construct(self):
        r = big_root(self, cells=0.0)
        self.add(garrow(-6.1, 0.9, -1.9), lab("gravity", -6.0, -2.5, 28, GRAV))
        dop = tracker_op(self, 1)
        P = ValueTracker(1)
        self.add(P)
        flank_dots(self, r, 14, P, dop, seed=21)
        s_ = lab("Slower.", 0, 3.0, 56, YELLOW)
        self.play(Write(s_), run_time=0.9)
        # growth arrows along each flank (grow in the direction of growth)
        lo, up = ValueTracker(0), ValueTracker(0)
        self.add(lo, up)

        def arr(u, ln, col):
            def b():
                l = ln.get_value() / 9.2
                if l < 0.02:
                    return VGroup(Dot(ORIGIN, radius=0.001).set_opacity(0))
                return Arrow(r.point(0.32, u), r.point(0.32 + l, u), buff=0, color=col, stroke_width=8, tip_length=0.28)
            return always_redraw(b)
        self.add(arr(-0.85, lo, BAD), arr(0.85, up, GOOD))
        self.at("in the root")
        self.play(r.cells.animate.set_value(1), run_time=1.4)
        self.at("inhibits elongation")
        self.play(lo.animate.set_value(1.0), FadeOut(s_), run_time=1.3)
        self.at("lower epidermal cells")
        ep = lab("epidermal cells", 3.0, -2.3, 28, YELLOW)
        ln = Line([3.0, -1.9, 0], r.point(0.17, -0.5), color=YELLOW, stroke_width=3)
        self.play(r.hl_lo.animate.set_value(1), FadeIn(ep), Create(ln), run_time=0.8)
        self.at("the upper flank outgrows it")
        self.play(up.animate.set_value(3.2), r.bend.animate.set_value(1.0), r.L.animate.set_value(9.5),
                  run_time=3.2, rate_func=smooth)
        self.finish()


class S10Shoot(Film):
    def construct(self):
        r = big_shoot(self, cells=1.0)
        self.add(garrow(6.1, 0.9, -1.9), lab("gravity", 6.0, -2.5, 28, GRAV))
        dop = tracker_op(self, 1)
        P = ValueTracker(1)
        self.add(P)
        flank_dots(self, r, 14, P, dop, seed=31)
        lo, up = ValueTracker(0), ValueTracker(0)
        self.add(lo, up)

        def arr(u, ln, col):
            def b():
                l = ln.get_value() / 9.2
                if l < 0.02:
                    return VGroup(Dot(ORIGIN, radius=0.001).set_opacity(0))
                return Arrow(r.point(0.32, u), r.point(0.32 + l, u), buff=0, color=col, stroke_width=8, tip_length=0.28)
            return always_redraw(b)
        self.add(arr(-0.85, lo, GOOD), arr(0.85, up, GREY))
        self.wait(0.5)
        self.at("speeds elongation")
        self.play(lo.animate.set_value(3.2), up.animate.set_value(1.0), run_time=1.5)
        self.at("of the lower flank")
        fl = lab("lower flank", 1.0, -2.3, 28, YELLOW)
        ln = Line([1.0, -1.9, 0], r.point(0.55, -0.5), color=YELLOW, stroke_width=3)
        self.play(FadeIn(fl), Create(ln), r.hl_lo.animate.set_value(1), run_time=0.6)
        self.play(r.bend.animate.set_value(0.9), run_time=2.6, rate_func=smooth)
        self.finish()


# ------------------------------------------------------------------ plot scenes
class S11Curves(Film):
    def construct(self):
        t = lab("Why opposite answers?", 0, 0.3, 56, TEXT)
        self.play(Write(t), run_time=1.4)
        self.at("plot growth")
        pl = Plot(self, mu_r=4.8, ps=0.0, pr=0.0, axes=False)
        pl.panel.set_opacity(0)
        self.play(FadeOut(t), pl.panel.animate.set_opacity(1), run_time=0.8)
        self.play(Create(pl.axes), FadeIn(pl.yl), run_time=0.9)
        self.at("oxen level")
        self.play(FadeIn(pl.xl), run_time=0.6)
        self.at("each organ")
        sh, rt, ls, lr = mini_organs(self, op=0, labels=False)
        self.play(sh.op.animate.set_value(1), FadeIn(ls), FadeIn(pl.note), run_time=0.8)
        self.play(pl.ps.animate.set_value(1), run_time=self.room("each curve", lo=0.5), rate_func=linear)
        self.at("each curve")
        self.play(rt.op.animate.set_value(1), FadeIn(lr), run_time=0.6)
        self.play(pl.pr.animate.set_value(1), run_time=self.left(0.5), rate_func=linear)
        self.finish()


def plot_state(scene, mu_r=2.4, bs=0.0, br=0.0, bsb=0.0, brb=0.0):
    pl = Plot(scene, mu_r=mu_r)
    sh, rt, ls, lr = mini_organs(scene, bs, br, bsb, brb)
    return pl, sh, rt, ls, lr


class S12Left(Film):
    def construct(self):
        pl, sh, rt, ls, lr = plot_state(self, mu_r=4.8)
        self.at("much lower oxen levels")
        self.play(pl.mu_r.animate.set_value(2.4), run_time=2.4, rate_func=smooth)
        self.at("so the roots curve")
        xr, xs = X0 + 2.4 * XS, X0 + MU_S * XS
        da = DoubleArrow([xr, 2.5, 0], [xs, 2.5, 0], buff=0, color=INK, stroke_width=5, tip_length=0.25)
        dl = lab("far lower auxin for roots", (xr + xs) / 2, 3.1, 28, INK)
        self.play(Create(da), FadeIn(dl), run_time=1.2)
        self.finish()


class S13ShootSlope(Film):
    def construct(self):
        pl, sh, rt, ls, lr = plot_state(self)
        ring = Circle(radius=0.22, color=INK, stroke_width=5)
        A = ValueTracker(1.0)
        self.add(A)
        ring.add_updater(lambda m: m.move_to(PX(A.get_value(), gval(A.get_value(), MU_S))))
        self.play(FadeIn(ring), run_time=0.3)
        self.play(A.animate.set_value(9.0), run_time=1.6, rate_func=linear)
        self.play(FadeOut(ring), run_time=0.2)
        ring2 = Circle(radius=0.22, color=INK, stroke_width=5)
        B = ValueTracker(1.0)
        self.add(B)
        ring2.add_updater(lambda m: m.move_to(PX(B.get_value(), gval(B.get_value(), 2.4))))
        self.play(FadeIn(ring2), run_time=0.2)
        self.play(B.animate.set_value(9.0), run_time=1.5, rate_func=linear)
        self.play(FadeOut(ring2), run_time=0.2)
        self.at("rising slope")
        a_s = ValueTracker(5.6)
        self.add(a_s)
        mk = marker(self, MU_S, a_s)
        pa = lab("position assumed (schematic)", -2.3, 3.15, 26, INK)
        self.play(FadeIn(mk, scale=1.8), FadeIn(pa), run_time=0.6)
        self.at("more oxen means")
        self.play(a_s.animate.set_value(6.0), sh.bend.animate.set_value(0.6), sh.band.animate.set_value(1),
                  sh.L.animate.set_value(4.8), run_time=self.left(0.6), rate_func=smooth)
        self.finish()


class S14RootSlope(Film):
    def construct(self):
        pl, sh, rt, ls, lr = plot_state(self, bs=0.6, bsb=1.0)
        sh.L.set_value(4.8)
        a_s = ValueTracker(6.0)
        a_r = ValueTracker(3.4)
        self.add(a_s, a_r)
        mk = marker(self, MU_S, a_s)
        pa = lab("position assumed (schematic)", -2.3, 3.15, 26, INK)
        self.add(mk, pa)
        self.at("past its peak")
        mr = marker(self, 2.4, a_r)
        self.play(FadeIn(mr, scale=1.8), run_time=0.7)
        self.at("more oxen means")
        self.play(a_r.animate.set_value(3.65), rt.bend.animate.set_value(0.9), rt.band.animate.set_value(1),
                  run_time=2.6, rate_func=smooth)
        self.at("same kind of signal")
        ob = lab("opposite bends", 4.1, 0.1, 34, INK)
        self.play(FadeIn(ob), run_time=0.7)
        self.finish()


class S15Scope(Film):
    def construct(self):
        pl, sh, rt, ls, lr = plot_state(self, bs=0.6, br=0.9, bsb=1.0, brb=1.0)
        sh.L.set_value(4.8)
        mk1 = marker(self, MU_S, ValueTracker(6.0))
        mk2 = marker(self, 2.4, ValueTracker(3.65))
        self.add(mk1, mk2)
        self.play(pl.dim.animate.set_value(0.35), sh.op.animate.set_value(0), rt.op.animate.set_value(0), FadeOut(ls), FadeOut(lr),
                  FadeOut(mk1), FadeOut(mk2), run_time=1.4)
        self.at("the sign of each bend")
        bg = Rectangle(width=5.4, height=1.2, stroke_width=0, fill_color=PANEL, fill_opacity=0.95).move_to([-2.6, 0.4, 0])
        sn = lab("sign, not cause", -2.6, 0.4, 48, INK)
        self.play(FadeIn(bg), FadeIn(sn), run_time=0.8)
        self.at("each tissue turns")
        t1 = lab("each tissue has its own\ngrowth machinery", 3.9, 1.6, 30, INK)
        self.play(FadeIn(t1), run_time=0.8)
        self.at("why roots are so sensitive")
        t2 = lab("gravity sensing worked out\nin Arabidopsis seedlings", 3.9, -1.2, 30, INK)
        self.play(FadeIn(t2), run_time=0.8)
        self.at("still not fully")
        q = lab("?", -4.0, 2.7, 72, INK)
        self.play(FadeIn(q, scale=1.5), run_time=0.7)
        self.finish()


class S16Rule(Film):
    def construct(self):
        sh, rt, sd = world(self)
        self.add(*grav_world(self))
        dop = tracker_op(self, 0)
        P = ValueTracker(0)
        self.add(P)
        flank_dots(self, rt, 14, P, dop, seed=41)
        flank_dots(self, sh, 14, P, dop, seed=42)
        self.play(dop.animate.set_value(1), run_time=1.0)
        self.at("light or gravity")
        la = Arrow([-6.4, 2.9, 0], [-4.6, 2.9, 0], buff=0, color=BLUE, stroke_width=9, tip_length=0.32)
        ll = lab("light", -3.6, 2.9, 28, BLUE)
        self.play(Create(la), FadeIn(ll), run_time=0.8)
        self.at("gravity")
        ins = VGroup(Square(1.9, stroke_color=WALL, stroke_width=4, fill_color=CELLC, fill_opacity=0.97),
                     Line([-0.95, -0.95, 0], [0.95, -0.95, 0], color=BLUE, stroke_width=0))
        gr = VGroup(*[Circle(radius=0.16, stroke_color="#2e1d0e", stroke_width=2, fill_color=BROWN, fill_opacity=1)
                      .move_to([-0.6 + 0.3 * k, -0.7, 0]) for k in range(5)])
        gt = VGroup(*[RoundedRectangle(corner_radius=0.06, width=0.4, height=0.18, stroke_color=TEAL, fill_color=TEAL,
                                       fill_opacity=1).move_to([-0.5 + 0.5 * k, -0.95, 0]) for k in range(3)])
        cell = VGroup(ins, gr, gt).move_to([-0.3, 2.5, 0])
        cl = lab("statoliths, PIN3", 2.4, 2.5, 28, TEAL)
        self.play(FadeIn(cell), FadeIn(cl), run_time=0.9)
        self.at("moves oxen to one flank")
        self.play(P.animate.set_value(1), sh.band.animate.set_value(1), rt.band.animate.set_value(1), run_time=2.4, rate_func=smooth)
        self.at("faster")
        fa = lab("faster", 3.6, -1.3, 34, GOOD)
        self.play(FadeIn(fa), sh.bend.animate.set_value(0.9), run_time=1.8, rate_func=smooth)
        self.at("slower")
        sl = lab("slower", -1.6, -1.3, 34, BAD)
        self.play(FadeIn(sl), rt.bend.animate.set_value(1.0), run_time=1.5, rate_func=smooth)
        self.finish()


class S17End(EndCard):
    LINE = "More auxin on the lower flank: shoots grow faster there, roots slower."
