"""Chance or Control: chapter 2 of the cytokinesis film pair.

COLOR MAP (chapter 1's map, kept exactly, plus the new chapter 2 colours)
  BLUE    spindle microtubules, asters, centrosomes (small squares)
  GREY    membrane / cortex rim
  AMBER   active RhoA band
  MAGENTA actin-myosin ring
  TEXT    chromosomes, questions, coins
  TEAL    generic organelle units ("one copy"), computed plots
  VIOLET  Golgi ribbon
  LIME    mitochondrial network
"""
import math
import random
import numpy as np
from bp_style import *  # noqa: F401,F403

AMBER = "#F0B44D"
MAGENTA = "#E764A8"
VIOLET = "#A98BF0"
LIME = "#A6D854"


def lerp(a, b, x):
    return a + (b - a) * x


def P3(x, y):
    return np.array([x, y, 0.0])


def label(text, size=30, color=TEXT, **kw):
    return T(text, size=size, color=color, weight=MEDIUM, **kw)


def rich(parts, size=28, color=TEXT):
    """Text with raised exponents: parts = [(text, is_superscript), ...]."""
    g = VGroup()
    ref = None
    prev = None
    for txt, sup in parts:
        m = T(txt, size * (0.62 if sup else 1), color, weight=MEDIUM)
        if prev is None:
            ref = m
        else:
            m.next_to(prev, RIGHT, buff=0.04)
            if sup:
                m.align_to(ref, UP).shift(UP * 0.08)
            else:
                m.match_y(ref)
        g.add(m)
        prev = m
    return g


def question_card(text):
    t = label(text, 30)
    box = RoundedRectangle(corner_radius=0.18, width=t.width + 0.6, height=t.height + 0.36,
                           color=TEXT, stroke_width=2, fill_color=BG, fill_opacity=0.93)
    return VGroup(box, t.move_to(box)).move_to([0, 3.15, 0])


def key_copy():
    return VGroup(Dot(radius=0.1, color=TEAL), label("one copy", 28, TEAL)).arrange(RIGHT, buff=0.15).to_corner(DR, buff=0.28)


# ---------------------------------------------------------------- coins
def coin(r=0.22):
    c = Circle(r, color=GOLD, stroke_width=3, fill_color=TEXT, fill_opacity=0.95)
    c.base_w = 2 * r
    return c


def flip(c, run_time=0.8, turns=3):
    return UpdateFromAlphaFunc(c, lambda m, a: m.stretch_to_fit_width(max(0.05, m.base_w * abs(math.cos(a * turns * PI)))),
                               run_time=run_time, rate_func=linear)


def wobble_coin(c, clock, rate=2.2, lo=0.55):
    c.add_updater(lambda m, dt: m.stretch_to_fit_width(m.base_w * (lo + (1 - lo) * abs(math.cos(clock() * rate)))))
    return c


def spin_coin(c, clock, rate=7.0):
    c.add_updater(lambda m, dt: m.stretch_to_fit_width(max(0.05, m.base_w * abs(math.cos(clock() * rate)))))
    return c


# ---------------------------------------------------------------- the daughters (carried through the film)
class Stage:
    """Two daughters joined by a bridge. z = 0 is the large layout, z = 1 the compact one."""

    def __init__(self, z=0.0):
        self.z = ValueTracker(z)
        self.breathe = ValueTracker(0)
        self.breathe.add_updater(lambda m, dt: m.increment_value(dt * 1.1))
        self.parts = Group(always_redraw(self._art), self.breathe)

    def zz(self):
        return self.z.get_value()

    def center(self, side):
        return P3(side * lerp(2.75, 2.0, self.zz()), lerp(-0.5, 1.1, self.zz()))

    def R(self):
        return lerp(2.3, 1.55, self.zz())

    def _art(self):
        R = self.R()
        b = math.sin(self.breathe.get_value()) * 0.02 * R
        cl, cr = self.center(-1), self.center(1)
        kw = dict(color=GREY, stroke_width=7, fill_color=GREY, fill_opacity=0.20)
        bw = 12 + 3 * math.sin(self.breathe.get_value() * 1.7)
        br = Line(cl + RIGHT * (R - 0.1), cr + LEFT * (R - 0.1), color=GREY, stroke_width=bw)
        return VGroup(br, Circle(R + b, **kw).move_to(cl), Circle(R + b, **kw).move_to(cr))


class Glide(Animation):
    """Move one swarm dot to a new home (a side of the stage, or a free point)."""

    def __init__(self, sw, i, side=0, u=None, p=None, lift=0.0, **kw):
        super().__init__(Mobject(), **kw)
        self.sw, self.i, self.side, self.u, self.p, self.lift = sw, i, side, u, p, lift

    def begin(self):
        sw, i = self.sw, self.i
        sw.src[i] = sw.dots[i].get_center().copy()
        sw.side[i] = self.side
        if self.side == 0:
            sw.p0[i] = np.array(self.p, dtype=float)
        else:
            sw.u[i] = np.array(self.u, dtype=float)
        sw.lift[i] = self.lift
        sw.mix[i] = 0.0
        super().begin()

    def interpolate_mobject(self, alpha):
        self.sw.mix[self.i] = self.rate_func(alpha)

    def clean_up_from_scene(self, scene):
        self.sw.mix[self.i] = 1.0
        super().clean_up_from_scene(scene)


class Swarm:
    """Dots that wobble around a home. Time comes from the scene clock so scenes can pick up where the last ended."""

    def __init__(self, scene, stage, n, color=TEAL, radius=0.1, amp=0.06, seed=1, t0=0.0):
        rng = random.Random(seed)
        self.stage, self.n, self.amp = stage, n, amp
        self.clock = lambda: scene.elapsed() + t0
        self.side = [0] * n
        self.u = [np.zeros(2) for _ in range(n)]
        self.p0 = [P3(0, 0) for _ in range(n)]
        self.mix = [1.0] * n
        self.src = [None] * n
        self.lift = [0.0] * n
        self.ph = [(rng.uniform(0, TAU), rng.uniform(0, TAU), rng.uniform(.6, 1.4), rng.uniform(.6, 1.4)) for _ in range(n)]
        self.dots = VGroup(*[Dot(radius=radius, color=color) for _ in range(n)])
        self.driver = Mobject()
        self.driver.add_updater(self._upd)
        self._upd(self.driver, 0)

    def home(self, i):
        if self.side[i] == 0:
            return self.p0[i].copy()
        c = self.stage.center(self.side[i])
        return c + P3(*(self.stage.R() * self.u[i]))

    def _upd(self, _m, dt):
        t = self.clock()
        for i, d in enumerate(self.dots):
            a, b, fa, fb = self.ph[i]
            w = P3(math.sin(t * fa * 1.3 + a), math.cos(t * fb * 1.1 + b)) * self.amp
            p = self.home(i) + w
            m = self.mix[i]
            if m < 1:
                p = self.src[i] * (1 - m) + p * m
                p[1] += self.lift[i] * math.sin(PI * m)
            d.move_to(p)

    def put(self, i, side, u=None, p=None):
        self.side[i] = side
        if side == 0:
            self.p0[i] = np.array(p, dtype=float)
        else:
            self.u[i] = np.array(u, dtype=float)
        self._upd(self.driver, 0)

    def sub(self, idx):
        return VGroup(*[self.dots[i] for i in idx])

    def count(self, side):
        return sum(1 for i in range(self.n) if self.side[i] == side and self.mix[i] >= 0.5)


def tally(stage, sw, side, size=34):
    def f():
        t = T(str(sw.count(side)), size, TEXT, weight=BOLD)
        c = stage.center(side)
        return t.move_to([c[0], c[1] + stage.R() + 0.45, 0])
    return always_redraw(f)


def disc_pt(rng, r=0.82):
    a, rr = rng.uniform(0, TAU), r * math.sqrt(rng.random())
    return np.array([rr * math.cos(a), rr * math.sin(a)])


# Predetermined coin tosses, shared by every scene that carries the dots.
_rng = random.Random(11)
U100 = [disc_pt(_rng) for _ in range(100)]
SIDES100 = [-1, 1, 1, -1, -1, 1, -1, 1, 1, -1, -1, 1, 1, -1, 1, -1]
_left_rest = 47 - SIDES100.count(-1)
_rest = [-1] * _left_rest + [1] * (84 - _left_rest)
_rng.shuffle(_rest)
SIDES100 += _rest


def reservoir_pt(i, z):
    rng = random.Random(100 + i)
    if z == 0:
        return P3(rng.uniform(-.38, .38), rng.uniform(.75, 1.85))
    return P3(rng.uniform(-.5, .5), rng.uniform(1.4, 2.4))


def place_assigned(sw, upto):
    for i in range(upto):
        sw.put(i, SIDES100[i], u=U100[i])


def place_pool(sw, start, stop, z=0):
    for i in range(start, stop):
        sw.put(i, 0, p=reservoir_pt(i, z))


# ---------------------------------------------------------------- chapter 1's cell, parameterised
class CellRig:
    def __init__(self, cx=0.0, cy=-0.5, r=2.75, spindle=True, sep=1.05, dent=0, band=0, ring=0,
                 daughters=0, pole=1.58, sp_op=1.0, rim_dots=True):
        V = ValueTracker
        self.cx, self.cy, self.r, self.k = cx, cy, r, r / 2.75
        self.dent, self.band_op, self.ring_op = V(dent), V(band), V(ring)
        self.sep, self.pole, self.sp_op = V(sep), V(pole), V(sp_op)
        self.glow, self.daughters, self.breathe = V(0), V(daughters), V(0)
        self.dent_x, self.band_x = V(0), V(0)
        self.spindle = spindle
        self.breathe.add_updater(lambda m, dt: m.increment_value(dt * 0.9))
        parts = [always_redraw(self._cell), always_redraw(self._band), always_redraw(self._ring),
                 always_redraw(self._spindle), self.breathe]
        if rim_dots:
            parts.insert(1, always_redraw(self._rim))
        self.parts = Group(*parts)

    def drive(self, t0, fn):
        self.clock = ValueTracker(t0)
        self.clock.add_updater(lambda m, dt: (m.increment_value(dt), fn(self, m.get_value())))
        self.parts.add(self.clock)
        fn(self, t0)

    def q(self):
        return self.daughters.get_value()

    def _y(self, x):
        rr = self.r * (1 + 0.012 * math.sin(self.breathe.get_value()))
        base = math.sqrt(max(rr * rr - (x - self.cx) ** 2, 0.02))
        d = self.dent.get_value() * self.k * math.exp(-((x - (self.cx + self.dent_x.get_value())) / (0.48 * self.k)) ** 2)
        return max(0.12, base - d)

    def dsep(self):
        return lerp(1.4, 2.75, self.q()) * self.k

    def drad(self):
        return lerp(2.0, 2.3, self.q()) * self.k

    def _cell(self):
        if self.q() > 0.01:
            rad, sep = self.drad(), self.dsep()
            br = math.sin(self.breathe.get_value())
            kw = dict(color=GREY, stroke_width=7, fill_color=GREY, fill_opacity=0.20)
            L = Circle(rad + 0.02 * br, **kw).move_to([self.cx - sep, self.cy, 0])
            R = Circle(rad + 0.02 * br, **kw).move_to([self.cx + sep, self.cy, 0])
            b = Line([self.cx - sep + rad - .12, self.cy, 0], [self.cx + sep - rad + .12, self.cy, 0], color=GREY, stroke_width=12)
            return VGroup(b, L, R)
        xs = np.linspace(self.cx - self.r, self.cx + self.r, 150)
        ys = np.array([self._y(x) for x in xs])
        pts = [P3(x, self.cy + y) for x, y in zip(xs, ys)] + [P3(x, self.cy - y) for x, y in zip(xs[::-1], ys[::-1])]
        return Polygon(*pts, color=GREY, stroke_width=7, fill_color=GREY, fill_opacity=0.20)

    def _rim(self):
        if self.q() > 0.01:
            return VGroup()
        out = VGroup()
        bx = self.cx + self.band_x.get_value()
        for x in np.linspace(self.cx - 1.95 * self.k, self.cx + 1.95 * self.k, 13):
            a = math.exp(-((x - bx) / .47) ** 2) * self.band_op.get_value()
            col = interpolate_color(ManimColor(GREY), ManimColor(AMBER), a)
            for s in (-1, 1):
                out.add(Dot([x, self.cy + s * (self._y(x) - .16), 0], radius=.065, color=col))
        return out

    def _arc(self, xc, half, color, width, op, inset):
        xs = np.linspace(max(self.cx - self.r + .05, xc - half), min(self.cx + self.r - .05, xc + half), 35)
        out = VGroup()
        for s in (-1, 1):
            m = VMobject().set_points_smoothly([P3(x, self.cy + s * (self._y(x) - inset)) for x in xs])
            m.set_stroke(color, width=width, opacity=op)
            out.add(m)
        return out

    def _band(self):
        if self.q() > 0.01:
            return VGroup()
        return self._arc(self.cx + self.band_x.get_value(), .5, AMBER, 15, self.band_op.get_value(), .10)

    def _ring(self):
        if self.q() > 0.01:
            return VGroup()
        return self._arc(self.cx + self.dent_x.get_value(), .55, MAGENTA, 7, self.ring_op.get_value(), .27 * self.k)

    @staticmethod
    def cluster(p, scale=1.0):
        return VGroup(*[Line(np.array(p) + [-.12, y - .20, 0], np.array(p) + [.12, y + .20, 0], color=TEXT, stroke_width=5)
                        for y in (-.28, 0, .28)]).scale(scale)

    def pole_pts(self):
        pl = self.pole.get_value() * self.k
        return P3(self.cx - pl, self.cy), P3(self.cx + pl, self.cy)

    def _spindle(self):
        op = self.sp_op.get_value()
        k = self.k
        g = VGroup()
        if not self.spindle or op < 0.01:
            return g
        if self.q() > 0.01:
            sep = self.dsep()
            g.add(Line([self.cx - .38 * k, self.cy, 0], [self.cx + .38 * k, self.cy, 0], color=BLUE, stroke_width=7))
            g.add(self.cluster([self.cx - sep * .8, self.cy, 0], .78 * k), self.cluster([self.cx + sep * .8, self.cy, 0], .78 * k))
            return g.set_opacity(op)
        pa, pb = self.pole_pts()
        for y in (-.28, -.10, .10, .28):
            g.add(Line(pa, [self.cx - .38 * k, self.cy + y * k, 0], color=BLUE, stroke_width=4))
            g.add(Line([self.cx + .38 * k, self.cy + y * k, 0], pb, color=BLUE, stroke_width=4))
        gl = self.glow.get_value()
        for p in (pa, pb):
            for a in np.linspace(0, TAU, 12, endpoint=False):
                g.add(Line(p, p + .68 * k * P3(math.cos(a), math.sin(a)), color=BLUE, stroke_width=2.6, stroke_opacity=.78))
            sq = Square(.2 + .16 * gl, color=interpolate_color(ManimColor(BLUE), ManimColor(WHITE), .5 * gl),
                        fill_color=interpolate_color(ManimColor(BLUE), ManimColor(WHITE), .5 * gl), fill_opacity=1).move_to(p)
            g.add(sq)
        s = self.sep.get_value() * k
        g.add(self.cluster([self.cx - s, self.cy, 0], k), self.cluster([self.cx + s, self.cy, 0], k))
        return g.set_opacity(op) if op < 0.99 else g


def add_rig(scene, rig):
    scene.add(rig.parts)


def anaph(rig, t):
    rig.sep.set_value(1.05 + .03 * t)
    rig.band_op.set_value(.95)
    rig.ring_op.set_value(min(.85, .12 + .045 * t))
    rig.dent.set_value(min(.9, .03 * t))


def scatter_cell(sw, cx, cy, r, seed=3):
    rng = random.Random(seed)
    for i in range(sw.n):
        sw.put(i, 0, p=P3(cx, cy) + P3(*(r * disc_pt(rng, .86))))


# ---------------------------------------------------------------- histogram (computed)
HX0, HX1, HBASE, HMAX = -6.5, 1.2, -2.3, 1.5
KS = list(range(30, 71))
BW = (HX1 - HX0) / len(KS)


def hx(k):
    return HX0 + BW * (k - 30 + .5)


def hist_group():
    pm = [math.comb(100, k) / 2 ** 100 for k in KS]
    mx = max(pm)
    bars = VGroup()
    for k, p in zip(KS, pm):
        r = Rectangle(width=BW * .86, height=max(.02, HMAX * p / mx), stroke_width=0, fill_color=TEAL, fill_opacity=.42)
        r.move_to([hx(k), HBASE + r.height / 2, 0])
        bars.add(r)
    axis = Line([HX0 - .1, HBASE, 0], [HX1 + .1, HBASE, 0], color=GREY, stroke_width=3)
    ticks = VGroup(*[T(str(k), 24, TEXT).move_to([hx(k), HBASE - .3, 0]) for k in (30, 40, 50, 60, 70)])
    title = label("copies in left daughter", 26).move_to([(HX0 + HX1) / 2, HBASE - .72, 0])
    return bars, VGroup(axis, ticks, title)


def bracket_group():
    y = HBASE - 1.1
    xa, xb = hx(40) - BW / 2, hx(60) + BW / 2
    br = VGroup(Line([xa, y, 0], [xb, y, 0], color=TEXT, stroke_width=3),
                Line([xa, y, 0], [xa, y + .1, 0], color=TEXT, stroke_width=3),
                Line([xb, y, 0], [xb, y + .1, 0], color=TEXT, stroke_width=3))
    lab = label("40 to 60: most divisions", 28).move_to([(xa + xb) / 2, y - .3, 0])
    return VGroup(br, lab)


def stmt_group():
    l1 = label("either daughter empty:", 28)
    l2 = rich([("2 × 0.5", 0), ("100", 1), (" = 1.6 × 10", 0), ("−30", 1)], 28)
    g = VGroup(l1, l2).arrange(DOWN, buff=.2, aligned_edge=LEFT).move_to([4.45, -1.7, 0])
    return g


# ---------------------------------------------------------------- strip / mini graph
def mini_graph(dim=1.0):
    x0, x1, yt, yb = -3.6, 3.6, -2.75, -3.65
    pt = lambda n: P3(x0 + (n - 1) / 24 * (x1 - x0), yt + (yb - yt) * (n - 1) * .301 / 7)
    axis = VGroup(Line([x0 - .1, yb, 0], [x1 + .1, yb, 0], color=GREY, stroke_width=3),
                  Line([x0 - .1, yb, 0], [x0 - .1, yt + .1, 0], color=GREY, stroke_width=3))
    curve = Line(pt(1), pt(25), color=TEAL, stroke_width=6).set_opacity(dim)
    tag = label("chance of none, by copies", 24).move_to([4.7, -2.8, 0])
    return VGroup(axis, curve, tag), pt


# ---------------------------------------------------------------- the big computed graph
GX0, GX1, GYT, GYB = -4.9, 6.1, 2.25, -2.85


def gx(n):
    return GX0 + (n - 1) / 24 * (GX1 - GX0)


def gy(p):
    return GYT - (-math.log10(p)) / 7 * (GYT - GYB)


def gpt(n):
    return P3(gx(n), gy(2 * 0.5 ** n))


def big_axes():
    g = VGroup()
    g.add(Line([GX0 - .1, GYB, 0], [GX1 + .2, GYB, 0], color=GREY, stroke_width=3),
          Line([GX0 - .1, GYB, 0], [GX0 - .1, GYT + .1, 0], color=GREY, stroke_width=3))
    for n in (1, 5, 10, 15, 20, 25):
        g.add(T(str(n), 24, TEXT).move_to([gx(n), GYB - .3, 0]))
    for e in (0, 2, 4, 6):
        y = gy(10.0 ** -e)
        g.add(Line([GX0 - .1, y, 0], [GX1 + .2, y, 0], color=GREY, stroke_width=1.5, stroke_opacity=.3))
        t = T("1", 24, TEXT) if e == 0 else rich([("10", 0), (f"−{e}", 1)], 24)
        g.add(t.move_to([GX0 - .55, y, 0]))
    g.add(label("number of copies, n", 28).move_to([(GX0 + GX1) / 2, GYB - .72, 0]))
    ylab = label("chance one daughter gets none", 26).rotate(PI / 2).move_to([-6.55, -.3, 0])
    g.add(ylab)
    g.add(rich([("P(empty) = 2 × 0.5", 0), ("n", 1)], 34).move_to([0, 3.2, 0]))
    return g


def corner_label(text="computed"):
    return label(text, 28).to_corner(UR, buff=.3)


# ---------------------------------------------------------------- mammalian cell contents
def zigzag_segments(x0, x1, y, amp, n):
    pts = [P3(lerp(x0, x1, i / n), y + (amp if i % 2 else -amp)) for i in range(n + 1)]
    return [Line(pts[i], pts[i + 1], color=VIOLET, stroke_width=9) for i in range(n)]


def subdivide(poly, step=.3, color=LIME, w=7):
    segs = []
    for a, b in zip(poly[:-1], poly[1:]):
        a, b = np.array(a), np.array(b)
        n = max(1, int(round(np.linalg.norm(b - a) / step)))
        for i in range(n):
            segs.append(Line(a + (b - a) * i / n, a + (b - a) * (i + 1) / n, color=color, stroke_width=w))
    return segs


NET = [[(-1.2, -.7), (-.6, -.4), (0, -.7), (.6, -.45), (1.2, -.8)], [(-.6, -.4), (-.5, -1.0)],
       [(.6, -.45), (.7, -1.1), (.1, -1.2)]]


def net_segments(cx, cy, s=1.0):
    segs = []
    for poly in NET:
        segs += subdivide([P3(cx + x * s, y) for x, y in poly])
    return segs


TEAL_SPOTS = [(-1.8, .45), (1.8, .45), (-1.6, 1.0), (1.6, 1.0), (-1.5, -.4), (1.5, -.4), (-.9, 2.0), (.9, 2.0),
              (-.5, -1.45), (.8, -1.45), (-1.45, 1.5), (1.45, 1.5)]


def mammal_cell(scene, cx=0.0, cy=0.45, r=2.05, sep=.25, dent=0, with_net=True, ribbon=True, teal=True,
                sp_op=.35, t0=0.0, seed=5):
    rig = CellRig(cx=cx, cy=cy, r=r, sep=sep, sp_op=sp_op, rim_dots=False, dent=dent)
    rig.dent_x.set_value(0)
    ribbon_segs = VGroup(*zigzag_segments(cx - 1.3, cx + 1.3, cy + .9, .17, 14)) if ribbon else VGroup()
    net = VGroup(*net_segments(cx, cy)) if with_net else VGroup()
    dots = None
    if teal:
        dots = Swarm(scene, Stage(), len(TEAL_SPOTS), radius=.09, amp=.07, seed=seed, t0=t0)
        for i, (x, y) in enumerate(TEAL_SPOTS):
            dots.put(i, 0, p=P3(cx + x, cy + y - .45 + .45))
    return rig, ribbon_segs, net, dots


class Base(NarratedScene):
    pass


# =============================================================== scenes
class S00Link(SpokenScene, TitleCard):
    LESSON = "Cytokinesis"
    TITLE = "Chance or Control"

    def construct(self):
        rig = CellRig(); rig.drive(0.0, anaph); add_rig(self, rig)
        sw = Swarm(self, Stage(), 30, radius=.09, amp=.09, seed=21, t0=0.0)
        scatter_cell(sw, 0, -.5, 2.75, seed=21)
        self.add(sw.driver)
        tag = chip("Chapter 1", GREY, 28).to_corner(UR, buff=.35)
        self.play(FadeIn(tag), run_time=.4)
        self.play(Indicate(tag, color=TEXT), run_time=1.0)
        self.play(FadeOut(tag), run_time=.5)
        self.at("splits everything")
        self.play(FadeIn(sw.dots), run_time=1.0)
        self.at("too")
        cut = DashedLine([0, 2.5, 0], [0, -3.3, 0], color=TEXT, dash_length=.15)
        self.play(Create(cut), run_time=1.3, rate_func=linear)
        self.play(Indicate(sw.dots, color=TEXT, scale_factor=1.25), run_time=1.0)
        self.play(FadeOut(cut), run_time=.4)
        self.at("count its organelles")
        q = question_card("Count them out, or leave it to chance?")
        self.play(FadeIn(q, shift=DOWN * .12), run_time=.6)
        self.at("or is chance")
        lab = label("what lands\non each side?", 30).move_to([-4.8, 1.3, 0])
        self.play(FadeIn(lab), run_time=.6)
        self.finish()


class S01Title(NarratedScene):
    def construct(self):
        t0 = 15.05
        rig = CellRig(); rig.drive(t0, anaph); add_rig(self, rig)
        sw = Swarm(self, Stage(), 30, radius=.09, amp=.09, seed=21, t0=t0)
        scatter_cell(sw, 0, -.5, 2.75, seed=21)
        self.add(sw.driver, sw.dots, question_card("Count them out, or leave it to chance?"),
                 label("what lands\non each side?", 30).move_to([-4.8, 1.3, 0]))
        title = T("Chance or Control", 50, font=TITLE_FONT)
        rule = Line(LEFT * 2, RIGHT * 2, color=GOLD, stroke_width=4).next_to(title, DOWN, buff=.12)
        back = RoundedRectangle(corner_radius=.2, width=title.width + .8, height=1.3, fill_color=BG, fill_opacity=.88,
                                stroke_width=0)
        grp = VGroup(back, title, rule)
        title.move_to(back).shift(UP * .12); rule.next_to(title, DOWN, buff=.1)
        grp.move_to([0, -2.35, 0])
        self.play(FadeIn(grp, shift=UP * .12), run_time=1.2)
        self.finish()


class S02Coin(SpokenScene):
    def construct(self):
        t0 = 17.6
        rig = CellRig(); rig.drive(t0, anaph); add_rig(self, rig)
        old = Swarm(self, Stage(), 30, radius=.09, amp=.09, seed=21, t0=t0)
        scatter_cell(old, 0, -.5, 2.75, seed=21)
        self.add(old.driver, old.dots)
        self.play(FadeOut(old.dots), rig.dent.animate.set_value(2.3), rig.sp_op.animate.set_value(0), run_time=2.2)
        rig.clock.clear_updaters()
        self.play(rig.daughters.animate.set_value(1), rig.ring_op.animate.set_value(0), rig.band_op.animate.set_value(0),
                  run_time=1.0)
        stage = Stage()
        self.remove(rig.parts); self.add(stage.parts)
        sw = Swarm(self, stage, 20, radius=.1, amp=.07, seed=7)
        place_pool(sw, 0, 20)
        self.add(sw.driver)
        key = key_copy()
        self.play(FadeIn(sw.dots), FadeIn(key), run_time=.7)
        self.at("Each copy")
        lab = label("each copy: a coin toss", 30).move_to([0, 3.45, 0])
        self.play(FadeIn(lab), run_time=.5)

        def toss(i, x, rt=(.5, .8, .9)):
            c = coin().move_to([x + .55, 2.55, 0])
            return Succession(
                AnimationGroup(Glide(sw, i, 0, p=P3(x, 2.1), run_time=rt[0]), FadeIn(c, run_time=rt[0])),
                flip(c, rt[1]),
                AnimationGroup(Glide(sw, i, SIDES100[i], u=U100[i], lift=.3, run_time=rt[2]), FadeOut(c, run_time=rt[2])))
        self.play(toss(0, 0.0), run_time=2.2)
        self.at("either daughter")
        self.play(toss(1, 0.0), run_time=2.2)
        self.at("on its own")
        xs = [-.9, -.3, .3, .9]
        self.play(AnimationGroup(*[toss(2 + j, xs[j], (.35, .5, .5)) for j in range(4)], lag_ratio=.1))
        self.finish()


class S02bToss(NarratedScene):
    def construct(self):
        stage = Stage(); self.add(stage.parts)
        sw = Swarm(self, stage, 20, radius=.1, amp=.07, seed=7, t0=9.9)
        place_assigned(sw, 6); place_pool(sw, 6, 20)
        self.add(sw.driver, sw.dots, key_copy(), label("each copy: a coin toss", 30).move_to([0, 3.45, 0]))
        tl, tr = tally(stage, sw, -1), tally(stage, sw, 1)
        self.add(tl, tr)

        def toss(i, x):
            c = coin().move_to([x + .55, 2.6, 0])
            return Succession(
                AnimationGroup(Glide(sw, i, 0, p=P3(x, 2.1), run_time=.3), FadeIn(c, run_time=.3)),
                flip(c, .45),
                AnimationGroup(Glide(sw, i, SIDES100[i], u=U100[i], lift=.3, run_time=.45), FadeOut(c, run_time=.45)))
        xs = [-.9, -.3, .3, .9]
        self.play(AnimationGroup(*[toss(6 + j, xs[j % 4]) for j in range(10)], lag_ratio=.22))
        self.finish()


def build_hundred(scene, upto=100):
    stage = Stage(z=1.0); scene.add(stage.parts)
    sw = Swarm(scene, stage, 100, radius=.085, amp=.06, seed=7)
    place_assigned(sw, upto)
    scene.add(sw.driver, sw.dots)
    return stage, sw


class S03Hundred(SpokenScene):
    def construct(self):
        stage = Stage(); self.add(stage.parts)
        sw = Swarm(self, stage, 100, radius=.085, amp=.06, seed=7, t0=13.0)
        place_assigned(sw, 16)
        self.add(sw.driver, sw.sub(range(16)), key_copy())
        tl, tr = tally(stage, sw, -1), tally(stage, sw, 1)
        self.add(tl, tr)
        for i in range(16, 100):
            sw.put(i, 0, p=reservoir_pt(i, 1))
        newd = sw.sub(range(16, 100))
        self.play(stage.z.animate.set_value(1.0), FadeIn(newd), run_time=1.0)
        flick = spin_coin(coin(.2).move_to([0, 2.85, 0]), sw.clock)
        self.add(flick)
        gl = [Glide(sw, i, SIDES100[i], u=U100[i], lift=.25, run_time=.8) for i in range(16, 100)]
        self.play(AnimationGroup(*gl, lag_ratio=.03))
        self.at("give or take")
        bars, rest = hist_group()
        cl = corner_label().to_corner(UL, buff=.3)
        self.play(FadeIn(VGroup(bars, rest), shift=UP * .8), FadeIn(cl), FadeOut(flick), run_time=1.5)
        self.at("Most daughters")
        bright = VGroup(*bars[10:31])
        self.play(bright.animate.set_fill(opacity=.95), run_time=1.0)
        self.at("get forty")
        br = bracket_group()
        self.play(FadeIn(br), run_time=.8)
        self.at("The chance that")
        st = stmt_group()
        self.play(FadeIn(st[0]), run_time=.8)
        self.at("is about")
        self.play(FadeIn(st[1]), run_time=1.0)
        self.at("In practice")
        self.play(Indicate(st[1], color=TEXT, scale_factor=1.08), run_time=1.2)
        bright.add_updater(lambda m, dt: m.set_fill(opacity=.85 + .1 * math.sin(sw.clock() * 3)))
        self.finish()


class S03bSettle(NarratedScene):
    def construct(self):
        stage, sw = build_hundred(self)
        sw.t0 = 0
        self.add(key_copy(), tally(stage, sw, -1), tally(stage, sw, 1))
        bars, rest = hist_group()
        bright = VGroup(*bars[10:31]).set_fill(opacity=.95)
        self.add(bars, rest, bracket_group(), corner_label().to_corner(UL, buff=.3), stmt_group())
        self.play(bright.animate.set_fill(opacity=1).scale(1.0), Indicate(bright, color=TEAL, scale_factor=1.06), run_time=1.4)
        self.finish()


class S04Predict(SpokenScene):
    def construct(self):
        stage, sw = build_hundred(self)
        bars, rest = hist_group()
        bright = VGroup(*bars[10:31]).set_fill(opacity=.95)
        extras = VGroup(bars, rest, bracket_group(), corner_label().to_corner(UL, buff=.3), stmt_group())
        tl, tr = tally(stage, sw, -1), tally(stage, sw, 1)
        self.add(extras, tl, tr)
        self.play(FadeOut(extras), FadeOut(sw.dots), FadeOut(tl), FadeOut(tr), run_time=1.0)
        self.play(stage.z.animate.set_value(0.0), run_time=1.1)
        key = key_copy(); self.add(key)
        two = Swarm(self, stage, 2, radius=.16, amp=.05, seed=2)
        two.put(0, 0, p=P3(-.32, 1.2)); two.put(1, 0, p=P3(.32, 1.2))
        self.add(two.driver)
        self.at("two copies")
        self.play(FadeIn(two.dots), run_time=.6)
        self.at("toss")
        cs = VGroup(coin().move_to([-.55, 2.3, 0]), coin().move_to([.55, 2.3, 0]))
        for c in cs:
            c.add_updater(lambda m, dt: m.move_to([m.get_x(), 2.3 + .06 * math.sin(self.elapsed() * 3 + m.get_x()), 0]))
        self.play(FadeIn(cs), run_time=.6)
        self.at("How often")
        q = question_card("Two copies: how often is one daughter empty?")
        self.play(FadeIn(q, shift=DOWN * .12), run_time=.6)
        self.finish()


class S05Think(NarratedScene):
    def construct(self):
        stage = Stage(); self.add(stage.parts)
        two = Swarm(self, stage, 2, radius=.16, amp=.05, seed=2, t0=8.3)
        two.put(0, 0, p=P3(-.32, 1.2)); two.put(1, 0, p=P3(.32, 1.2))
        cs = VGroup(coin().move_to([-.55, 2.3, 0]), coin().move_to([.55, 2.3, 0]))
        for j, c in enumerate(cs):
            wobble_coin(c, lambda j=j: self.elapsed() + j * .7, rate=2.4)
            c.add_updater(lambda m, dt: m.move_to([m.get_x(), 2.3 + .05 * math.sin(self.elapsed() * 2 + m.get_x()), 0]))
        self.add(two.driver, two.dots, cs, key_copy(), question_card("Two copies: how often is one daughter empty?"))
        self.wait(self.narration_s)


def pair_art(kind, r=.72):
    kw = dict(color=GREY, stroke_width=5, fill_color=GREY, fill_opacity=.2)
    cl = Circle(r, **kw).move_to([-1.15, 0, 0]); cr = Circle(r, **kw).move_to([1.15, 0, 0])
    br = Line([-1.15 + r - .05, 0, 0], [1.15 - r + .05, 0, 0], color=GREY, stroke_width=8)
    pos = {"LL": [(-1.35, .18), (-.95, -.18)], "RR": [(.95, .18), (1.35, -.18)],
           "LR": [(-1.15, 0), (1.15, 0)], "RL": [(1.15, 0), (-1.15, 0)]}[kind]
    dots = VGroup(*[Dot(P3(x, y), radius=.12, color=TEAL) for x, y in pos])
    return VGroup(br, cl, cr, dots), cl, cr


GRID = {"LL": (-3.4, 1.0), "LR": (3.4, 1.0), "RL": (-3.4, -1.95), "RR": (3.4, -1.95)}
CAPS = {"LL": "left, left", "LR": "left, right", "RL": "right, left", "RR": "right, right"}


def build_grid():
    cells = {}
    for k, (x, y) in GRID.items():
        art, cl, cr = pair_art(k)
        cap = label(CAPS[k], 28).move_to([0, 1.1, 0])
        g = VGroup(art, cap).move_to([x, y, 0])
        cells[k] = (g, art, cl, cr)
    return cells


class S06Reveal(SpokenScene):
    def construct(self):
        stage = Stage(); self.add(stage.parts)
        two = Swarm(self, stage, 2, radius=.16, amp=.05, seed=2, t0=12.8)
        two.put(0, 0, p=P3(-.32, 1.2)); two.put(1, 0, p=P3(.32, 1.2))
        q = question_card("Two copies: how often is one daughter empty?")
        key = key_copy()
        self.add(two.driver, two.dots, key, q)
        cells = build_grid()
        self.play(FadeOut(q), FadeOut(two.dots), FadeOut(stage.parts), FadeOut(key), run_time=.5)
        self.play(AnimationGroup(*[FadeIn(cells[k][0], scale=.9) for k in ("LL", "LR", "RL", "RR")], lag_ratio=.25), run_time=2.0)
        key = key_copy(); self.add(key)

        def glow(k):
            g, art, cl, cr = cells[k]
            box = SurroundingRectangle(g, color=TEXT, buff=.15, corner_radius=.15).set_stroke(width=3)
            empty = cr if k == "LL" else cl
            return box, empty

        def quarter(k):
            g = cells[k][0]
            return label("1 in 4", 30).next_to(g, DOWN, buff=.3)
        self.at("can land left")
        b1, e1 = glow("LL")
        self.play(Create(b1), Indicate(e1, color=TEXT, scale_factor=1.15), run_time=1.2)
        self.at("or both right")
        b2, e2 = glow("RR")
        self.play(Create(b2), Indicate(e2, color=TEXT, scale_factor=1.15), run_time=1.2)
        self.at("each happens")
        q1, q2 = quarter("LL"), quarter("RR")
        self.play(FadeIn(q1), FadeIn(q2), run_time=.8)
        self.play(Indicate(q1, color=TEXT), Indicate(q2, color=TEXT), run_time=1.0)
        self.at("Either daughter")
        self.play(Indicate(e1, color=TEXT, scale_factor=1.15), Indicate(e2, color=TEXT, scale_factor=1.15), run_time=1.4)
        self.at("so together")
        gLL = VGroup(cells["LL"][0], b1, q1); gRR = VGroup(cells["RR"][0], b2, q2)
        others = VGroup(cells["LR"][0], cells["RL"][0])
        self.play(FadeOut(others), key.animate.set_opacity(0), gLL.animate.move_to([-2.25, .9, 0]), gRR.animate.move_to([2.25, .9, 0]), run_time=1.3)
        res = label("1 in 4 + 1 in 4 = 1 in 2", 34).move_to([0, -1.5, 0])
        self.play(FadeIn(res, shift=UP * .1), run_time=.8)
        self.finish()


def curve_objs(n_end):
    curve = always_redraw(lambda: Line(gpt(2), gpt(max(2.001, n_end.get_value())), color=TEAL, stroke_width=7))
    steps = always_redraw(lambda: VGroup(*[Dot(gpt(n), radius=.07, color=TEXT) for n in range(3, int(n_end.get_value() + .001) + 1)]))
    return curve, steps


def graph_labels():
    d2 = Dot(gpt(2), radius=.1, color=TEAL)
    l2 = label("2 copies: 1 in 2", 28).next_to(d2, UR, buff=.15)
    d10 = Dot(gpt(10), radius=.11, color=TEAL)
    l10 = label("about 1 in 500", 28).next_to(d10, UR, buff=.15)
    dash = DashedLine([GX0 - .1, gy(1e-6), 0], [GX1 + .2, gy(1e-6), 0], color=TEXT, dash_length=.15, stroke_width=3)
    lm = label("1 in a million", 28).move_to([5.45, gy(1e-6) + .38, 0])
    d21 = Dot(gpt(21), radius=.12, color=TEXT)
    return d2, l2, d10, l10, dash, lm, d21


class S07Curve(SpokenScene):
    def construct(self):
        a = rebuild = None
        # the shrinking pair from chapter 2's last picture, then the graph
        art1, _, _ = pair_art("LL"); art2, _, _ = pair_art("RR")
        icon = VGroup(art1.move_to([-2.25, .9, 0]), art2.move_to([2.25, .9, 0]))
        self.add(icon)
        self.play(icon.animate.scale(.2).move_to([-5.8, 3.2, 0]).set_opacity(0), run_time=1.2)
        ax = big_axes()
        eq = ax[-2]
        n_end = ValueTracker(2)
        curve, steps = curve_objs(n_end)
        d2, l2, d10, l10, dash, lm, d21 = graph_labels()
        self.play(FadeIn(VGroup(*[m for m in ax if m is not eq])), run_time=1.0)
        self.add(corner_label())
        self.at("empty daughter is")
        self.play(FadeIn(eq), run_time=.8)
        self.at("two times")
        self.add(curve, steps)
        self.play(FadeIn(d2), FadeIn(l2), run_time=.8)
        self.at("Each added copy")
        self.play(n_end.animate.set_value(9), run_time=2.7, rate_func=linear)
        self.at("ten copies")
        self.play(n_end.animate.set_value(10), FadeIn(d10), run_time=.6)
        self.play(FadeIn(l10), run_time=.6)
        self.play(Indicate(d10, color=TEXT, scale_factor=1.6), run_time=1.0)
        self.at("At twenty")
        self.play(n_end.animate.set_value(21), run_time=1.8, rate_func=linear)
        self.at("drops below")
        self.play(Create(dash), FadeIn(d21), run_time=.9)
        self.at("in a million")
        self.play(FadeIn(lm), Indicate(d21, color=TEXT, scale_factor=1.6), run_time=.9)
        self.finish()


class S07bCurve(NarratedScene):
    def construct(self):
        ax = big_axes()
        n_end = ValueTracker(21)
        curve, steps = curve_objs(n_end)
        d2, l2, d10, l10, dash, lm, d21 = graph_labels()
        self.add(ax, corner_label(), curve, steps, d2, l2, d10, l10, dash, lm, d21)
        self.play(n_end.animate.set_value(25), run_time=1.0, rate_func=linear)
        self.play(Indicate(d2, color=TEXT, scale_factor=1.7), run_time=.5)
        self.play(Indicate(d10, color=TEXT, scale_factor=1.7), run_time=.5)
        self.play(Indicate(d21, color=TEXT, scale_factor=1.7), run_time=.5)
        self.finish()


def mammal_world(scene, t0=0.0, labels=True, strip=True, dim=.6):
    rig, ribbon, net, dots = mammal_cell(scene, t0=t0)
    add_rig(scene, rig)
    scene.add(dots.driver, dots.dots, ribbon, net)
    out = {"rig": rig, "ribbon": ribbon, "net": net, "dots": dots}
    if strip:
        mg, pt = mini_graph(dim)
        scene.add(mg)
        out["mini"], out["pt"] = mg, pt
    return out


class S08Idea(SpokenScene):
    def construct(self):
        ax = big_axes()
        n_end = ValueTracker(25)
        curve, steps = curve_objs(n_end)
        d2, l2, d10, l10, dash, lm, d21 = graph_labels()
        big = VGroup(ax, curve, steps, d2, l2, d10, l10, dash, lm, d21)
        cornr = corner_label()
        self.add(big, cornr)
        mg, pt = mini_graph(.55)
        rig, ribbon, net, dots = mammal_cell(self)
        add_rig(self, rig)
        name = label("mammalian examples", 30).to_corner(UL, buff=.3)
        key = key_copy()
        self.play(big.animate.scale(.3).move_to([0, -3.2, 0]).set_opacity(0), FadeOut(cornr), FadeIn(mg), FadeIn(rig.parts), FadeIn(name),
                  FadeIn(dots.dots), FadeIn(key), run_time=1.6)
        self.remove(big)
        self.add(dots.driver)
        self.at("safe")
        self.play(Indicate(dots.dots, color=TEAL, scale_factor=1.5), run_time=1.2)
        self.at("connected structure")
        top = label("connected = one unit", 30).to_corner(UR, buff=.3)
        self.play(FadeIn(top), run_time=.6)
        self.at("mammalian")
        self.play(Indicate(rig.parts[0], color=GREY), run_time=1.0)
        self.at("Golgi ribbon")
        self.play(LaggedStart(*[FadeIn(s) for s in ribbon], lag_ratio=.06), run_time=1.2)
        gl = label("Golgi ribbon", 30, VIOLET).move_to([-4.6, 1.35, 0])
        ga = Arrow([-3.25, 1.35, 0], [-1.5, 1.37, 0], buff=0, color=VIOLET, stroke_width=4, tip_length=.15)
        self.play(FadeIn(gl), GrowArrow(ga), run_time=.8)
        self.at("tubular")
        self.play(LaggedStart(*[FadeIn(s) for s in net], lag_ratio=.03), run_time=1.3)
        ml = label("mitochondrial network", 30, LIME).move_to([4.3, -.7, 0])
        ma = Arrow([2.0, -.75, 0], [1.4, -.78, 0], buff=0, color=LIME, stroke_width=4, tip_length=.15)
        self.play(FadeIn(ml), GrowArrow(ma), run_time=.8)
        self.at("To the coin")
        c1 = coin(.2).move_to([0, 1.95, 0]); c2 = coin(.2).move_to([.4, -1.4, 0])
        spin_coin(c1, lambda: self.elapsed()); spin_coin(c2, lambda: self.elapsed() + 1)
        self.play(FadeIn(c1), FadeIn(c2), run_time=.6)
        self.at("single copy")
        p1 = Dot(pt(1), radius=.12, color=TEAL)
        ring = Circle(.25, color=TEAL, stroke_width=4).move_to(pt(1))
        n1 = label("n = 1: always one empty daughter", 28).move_to([-.2, -2.35, 0])
        self.play(FadeIn(p1), Create(ring), FadeIn(n1), run_time=.8)
        self.play(Indicate(ring, color=TEAL, scale_factor=1.6), run_time=1.0)
        self.finish()


def s08_state(scene, break_amt=0.0, t0=0.0, label_on=True):
    w = mammal_world(scene, t0=t0)
    key = key_copy(); scene.add(key)
    return w


class S08bBreak(NarratedScene):
    def construct(self):
        w = mammal_world(self, t0=16.5)
        self.add(key_copy(), label("mammalian examples", 30).to_corner(UL, buff=.3))
        rib = w["ribbon"]
        rng = random.Random(4)
        base = [s.get_center().copy() for s in rib]
        self.play(*[s.animate.shift(P3(rng.uniform(-.1, .1), rng.uniform(-.1, .1))) for s in rib[:5]], run_time=1.5)
        shim = ValueTracker(0)
        self.play(*[s.animate.shift(P3(rng.uniform(-.35, .35), rng.uniform(.0, .35))).rotate(rng.uniform(-.6, .6)) for s in rib[:4]],
                  *[s.animate.shift(P3(rng.uniform(-.08, .08), rng.uniform(-.08, .08))) for s in rib[4:]], run_time=1.4)
        self.finish()


class S09Golgi(SpokenScene):
    def construct(self):
        rig, ribbon, net, dots = mammal_cell(self, t0=19.5)
        add_rig(self, rig)
        self.add(dots.driver, dots.dots, ribbon, net, key_copy())
        rng = random.Random(4)
        for s in ribbon[:4]:
            s.shift(P3(rng.uniform(-.35, .35), rng.uniform(0, .35))).rotate(rng.uniform(-.6, .6))
        rig.sp_op.set_value(.35)
        self.play(*[s.animate.shift(P3(rng.uniform(-.1, .1), rng.uniform(-.12, .12))).rotate(rng.uniform(-.4, .4)) for s in ribbon[4:]], run_time=2.0)
        self.at("In PTK1")
        name = label("PtK1 cells (rat-kangaroo)", 30).to_corner(UL, buff=.3)
        self.play(FadeIn(name), rig.sp_op.animate.set_value(.7), run_time=.8)
        self.play(rig.sep.animate.set_value(.5), run_time=1.4)
        self.at("Golgi ribbon comes")
        scat = [P3(rng.uniform(-1.4, 1.4), 0.45 + rng.uniform(.7, 1.6)) for _ in ribbon]
        self.play(*[s.animate.scale(.45).move_to(p).rotate(rng.uniform(-1, 1)) for s, p in zip(ribbon, scat)], run_time=2.0)
        self.play(rig.sep.animate.set_value(1.0), run_time=1.5)
        self.at("cluster")
        lt, rt = [-1.18, .45], [1.18, .45]
        tg = []
        for i, s in enumerate(ribbon):
            c = lt if i % 2 == 0 else rt
            tg.append(P3(c[0] + rng.uniform(-.45, .45), c[1] + rng.uniform(-.55, .55)))
        self.play(*[s.animate.move_to(p) for s, p in zip(ribbon, tg)], run_time=1.8)
        cl = label("clustered at the poles", 28, VIOLET).move_to([4.6, 3.1, 0])
        self.play(FadeIn(cl), run_time=.6)
        self.at("spindle poles")
        self.play(rig.sep.animate.set_value(1.3), run_time=1.0)
        self.at("After division")
        self.play(FadeOut(cl), rig.dent.animate.set_value(2.2), rig.ring_op.animate.set_value(.9), run_time=1.3)
        self.play(rig.daughters.animate.set_value(1), rig.ring_op.animate.set_value(0), run_time=.5)
        self.at("ribbon reforms")
        rl = label("ribbon reforms", 28, VIOLET).move_to([0, 2.9, 0])
        dsep = rig.dsep()
        anims = []
        for i, s in enumerate(ribbon):
            side = -1 if i % 2 == 0 else 1
            j = i // 2
            anims.append(s.animate.scale(1.0).move_to(P3(side * dsep + (j - 3) * .17, .45 + (.12 if j % 2 else -.12))).set_color(VIOLET))
        self.play(*anims, FadeIn(rl), run_time=1.4)
        self.finish()


def mito_cell(cx, cy, r=2.55):
    rig = CellRig(cx=cx, cy=cy, r=r, spindle=False, rim_dots=False)
    segs = []
    for poly in NET:
        segs += subdivide([P3(cx + x * 1.5, cy + (y + .8) * 1.5) for x, y in poly], step=.45)
    return rig, VGroup(*segs)


def mito_frame(scene, frag, t0=0.0, tube=True):
    rl, nl = mito_cell(-3.5, -.3), mito_cell(3.5, -.3)
    rigL, netL = rl; rigR, netR = nl
    add_rig(scene, rigL); add_rig(scene, rigR)
    scene.add(netL, netR)
    sway = ValueTracker(0)
    sway.add_updater(lambda m, dt: m.increment_value(dt))
    scene.add(sway)
    netR.add_updater(lambda m, dt: m.rotate(.0025 * math.cos(sway.get_value()), about_point=P3(3.5, -.3 + .45 * 1.0)))
    rng = random.Random(9)
    if frag:
        for s in netL:
            s.shift(P3(rng.uniform(-.45, .45), rng.uniform(-.45, .45))).rotate(rng.uniform(-1.2, 1.2)).scale(.8)
    return rigL, rigR, netL, netR


class S10Mito(SpokenScene):
    def construct(self):
        rigL, rigR, netL, netR = mito_frame(self, False)
        self.add(key_copy().set_opacity(0))
        name = label("HeLa cells (human)", 30).to_corner(UL, buff=.3)
        self.play(FadeIn(name), run_time=.8)
        sc = label("schematic", 28).to_corner(UR, buff=.3)
        self.add(sc)
        self.at("broke into fragments")
        ln = label("normal", 30).move_to([-3.5, 2.7, 0])
        self.play(FadeIn(ln), run_time=.5)
        rng = random.Random(9)
        self.play(*[s.animate.shift(P3(rng.uniform(-.45, .45), rng.uniform(-.45, .45))).rotate(rng.uniform(-1.2, 1.2)).scale(.8) for s in netL],
                  run_time=3.0)
        self.at("Without")
        rn = label("no Drp1", 30).move_to([3.5, 2.7, 0])
        self.play(FadeIn(rn), run_time=.6)
        self.at("protein that drives")
        blk = chip("Drp1", LIME, 28).move_to([-3.9, -1.65, 0])
        tube = Line([-4.4, -2.4, 0], [-3.4, -2.4, 0], color=LIME, stroke_width=7)
        self.play(FadeIn(tube), FadeIn(blk, shift=DOWN * .2), run_time=.7)
        pin = Arrow([-3.9, -2.0, 0], [-3.9, -2.35, 0], buff=0, color=LIME, stroke_width=5, tip_length=.15)
        self.play(GrowArrow(pin), run_time=.4)
        self.play(tube.animate.set_points_as_corners([P3(-4.4, -2.4), P3(-3.95, -2.4)]), run_time=.4)
        part2 = Line([-3.85, -2.4, 0], [-3.4, -2.4, 0], color=LIME, stroke_width=7)
        self.add(part2)
        self.play(part2.animate.shift(RIGHT * .3), FadeOut(pin), run_time=.4)
        self.at("fission")
        fl = label("fission", 28, LIME).move_to([-2.5, -1.65, 0])
        self.play(FadeIn(fl), run_time=.5)
        self.at("one cell line")
        tag = label("one cell line: a strong lead", 30).move_to([0, -3.4, 0])
        self.play(FadeIn(tag), run_time=.8)
        self.finish()


class S10bHold(NarratedScene):
    def construct(self):
        rigL, rigR, netL, netR = mito_frame(self, True)
        self.add(label("HeLa cells (human)", 30).to_corner(UL, buff=.3), label("schematic", 28).to_corner(UR, buff=.3),
                 label("normal", 30).move_to([-3.5, 2.7, 0]), label("no Drp1", 30).move_to([3.5, 2.7, 0]),
                 label("one cell line: a strong lead", 30).move_to([0, -3.4, 0]))
        jit = ValueTracker(0)
        netL.add_updater(lambda m, dt: m.shift(P3(.01 * math.sin(self.elapsed() * 2), .01 * math.cos(self.elapsed() * 1.7))))
        self.wait(self.narration_s)


class S11Poles(SpokenScene):
    def construct(self):
        rig = CellRig(cx=0, cy=.35, r=2.3, sep=1.0, band=0.0, ring=.3, dent=.25)
        rig.pole.set_value(1.58)
        add_rig(self, rig)
        self.play(rig.sep.animate.set_value(1.3), run_time=2.6)
        self.at("centrosomes")
        pa, pb = rig.pole_pts()
        lab = label("centrosome", 30, BLUE).move_to([0, 3.2, 0])
        a1 = Arrow([-.6, 2.95, 0], pa + UP * .25, buff=0, color=BLUE, stroke_width=4, tip_length=.15)
        a2 = Arrow([.6, 2.95, 0], pb + UP * .25, buff=0, color=BLUE, stroke_width=4, tip_length=.15)
        self.play(FadeIn(lab), GrowArrow(a1), GrowArrow(a2), rig.glow.animate.set_value(1), run_time=1.2)
        self.at("the spindle carries")
        self.play(rig.pole.animate.set_value(2.0), rig.sep.animate.set_value(1.75), run_time=2.2)
        self.play(FadeOut(a1), FadeOut(a2), FadeOut(lab), rig.glow.animate.set_value(0), run_time=.6)
        self.at("microtubules return")
        c1 = chip("microtubules", BLUE, 28, pad=.15).move_to([-2.6, -2.5, 0])
        c2 = chip("place the cut", AMBER, 28, pad=.15).move_to([2.2, -2.5, 0])
        ar1 = Arrow(c1.get_right(), c2.get_left(), buff=.1, color=GREY, stroke_width=5, tip_length=.18)
        c3 = chip("microtubules", BLUE, 28, pad=.15).move_to([-2.6, -3.3, 0])
        c4 = chip("carry centrosomes", BLUE, 28, pad=.15).move_to([2.6, -3.3, 0])
        ar2 = Arrow(c3.get_right(), c4.get_left(), buff=.1, color=GREY, stroke_width=5, tip_length=.18)
        self.play(rig.band_op.animate.set_value(1), FadeIn(c1), run_time=1.0)
        self.at("place the cut")
        self.play(GrowArrow(ar1), FadeIn(c2), Indicate(rig.parts[1], color=AMBER), run_time=1.0)
        self.at("carry part")
        self.play(FadeIn(c3), GrowArrow(ar2), FadeIn(c4), rig.glow.animate.set_value(1), run_time=1.2)
        self.play(rig.glow.animate.set_value(0), run_time=.6)
        self.finish()


class S12Caution(SpokenScene):
    def construct(self):
        rig = CellRig(cx=-3.4, cy=-.1, r=2.3, spindle=False, dent=.4, ring=.5, band=.5)
        rig.dent_x.set_value(0)
        add_rig(self, rig)
        rng = random.Random(6)
        sw = Swarm(self, Stage(), 12, color=LIME, radius=.1, amp=.07, seed=6)
        for i in range(12):
            sw.put(i, 0, p=P3(-3.4 + rng.choice([-1, 1]) * rng.uniform(1.0, 1.9), -.1 + rng.uniform(-1.3, 1.3)))
        self.add(sw.driver, sw.dots)
        moves = []
        for i in range(12):
            h = sw.p0[i]
            moves.append(Glide(sw, i, 0, p=P3(-3.4 + (h[0] + 3.4) * .45, h[1]), run_time=5.0))
        mv = label("moved", 30, LIME).move_to([-3.4, -3.1, 0])
        self.play(AnimationGroup(*moves), AnimationGroup(Wait(2.3), FadeIn(mv, run_time=.5)), run_time=5.0)
        self.at("not the same")
        stand = Line([3.4, -2.2, 0], [3.4, 1.0, 0], color=TEXT, stroke_width=5)
        beam = Line([1.9, 1.0, 0], [4.9, 1.0, 0], color=TEXT, stroke_width=6)
        pans = VGroup()
        piles = Swarm(self, Stage(), 10, color=LIME, radius=.1, amp=.05, seed=8)
        for j, x in enumerate((1.9, 4.9)):
            pans.add(Line([x, 1.0, 0], [x - .5, .0, 0], color=TEXT, stroke_width=3), Line([x, 1.0, 0], [x + .5, .0, 0], color=TEXT, stroke_width=3),
                     Line([x - .6, .0, 0], [x + .6, .0, 0], color=TEXT, stroke_width=6))
            for m in range(5):
                piles.put(j * 5 + m, 0, p=P3(x - .35 + .18 * m, .2 + (.15 if m % 2 else 0)))
        self.add(piles.driver)
        self.play(Create(stand), Create(beam), Create(pans), FadeIn(piles.dots), run_time=1.6)
        self.at("its share")
        sh = label("shares?", 30).move_to([3.4, -3.1, 0])
        qm = label("?", 60).move_to([3.4, 2.2, 0])
        div = Line([.3, -3.5, 0], [.3, 3.4, 0], color=TEXT, stroke_width=2)
        self.play(FadeIn(sh), FadeIn(qm), Create(div), run_time=1.0)
        self.at("Each claim")
        self.play(Indicate(mv, color=LIME), run_time=1.0)
        self.play(Indicate(sh, color=TEXT), run_time=1.0)
        self.finish()


def summary_contents(cx, cy):
    g = VGroup()
    g.rib = VGroup(*[Line(P3(cx - .7 + .35 * i, cy + 1.0 + (.12 if i % 2 else -.12)), P3(cx - .7 + .35 * (i + 1), cy + 1.0 + (-.12 if i % 2 else .12)),
                           color=VIOLET, stroke_width=8) for i in range(4)])
    g.cent = Square(.22, color=BLUE, fill_color=BLUE, fill_opacity=1).move_to([cx, cy + .25, 0])
    g.lime = VGroup(*[Line(P3(cx + dx, cy + dy), P3(cx + dx + .22, cy + dy + .06), color=LIME, stroke_width=7)
                      for dx, dy in [(-1.1, -.2), (-.7, -.5), (-1.0, -.85), (-.5, -.15), (-.55, -.9)]])
    rng = random.Random(3)
    g.teal = VGroup(*[Dot(P3(cx + .5 + rng.uniform(-.5, .5), cy - .8 + rng.uniform(-.4, .4)), radius=.08, color=TEAL) for _ in range(9)])
    g.add(g.rib, g.cent, g.lime, g.teal)
    return g


def summary_world(scene, finished=True):
    rig = CellRig(cx=0, cy=-.2, r=2.3, spindle=False, rim_dots=False, daughters=1.0 if finished else 0, sp_op=0)
    add_rig(scene, rig)
    return rig


class S13Close(NarratedScene):
    def construct(self):
        rig = CellRig(cx=0, cy=-.2, r=2.3, spindle=False, rim_dots=False, dent=.5, ring=.8)
        add_rig(self, rig)
        lab = label("examples from different cells", 30).move_to([0, 3.3, 0])
        self.add(lab)
        self.play(rig.dent.animate.set_value(2.0), rig.ring_op.animate.set_value(1), run_time=1.3)
        self.play(rig.daughters.animate.set_value(1), rig.ring_op.animate.set_value(0), run_time=.7)
        dsep = rig.dsep()
        cL, cR = summary_contents(-dsep, -.2), summary_contents(dsep, -.2)
        self.play(LaggedStart(FadeIn(cL), FadeIn(cR), lag_ratio=.3), run_time=1.0)
        self.finish()


class S14Return(SpokenScene):
    def construct(self):
        rig = CellRig(cx=0, cy=-.2, r=2.3, spindle=False, rim_dots=False, daughters=1.0)
        add_rig(self, rig)
        dsep = rig.dsep()
        cL, cR = summary_contents(-dsep, -.2), summary_contents(dsep, -.2)
        wob = lambda g: g.add_updater(lambda m, dt: m.shift(P3(.004 * math.sin(self.elapsed() * 2), .004 * math.cos(self.elapsed() * 1.6))))
        wob(cL.teal); wob(cR.teal); wob(cL.lime); wob(cR.lime)
        self.add(cL, cR, label("examples from different cells", 30).move_to([0, 3.3, 0]), key_copy())
        self.at("Chance can share")
        k1 = spin_coin(coin(.2).move_to([-dsep + .5, -.15, 0]), lambda: self.elapsed())
        k2 = spin_coin(coin(.2).move_to([dsep + .5, -.15, 0]), lambda: self.elapsed() + .5)
        self.play(FadeIn(k1), FadeIn(k2), Indicate(cL.teal, color=TEAL), Indicate(cR.teal, color=TEAL), run_time=1.6)
        self.play(FadeOut(k1), FadeOut(k2), run_time=.4)
        self.at("some control")
        gl = [Circle(.35, color=BLUE, stroke_width=6).move_to(c.cent) for c in (cL, cR)]
        self.play(*[Flash(c.cent, color=BLUE, flash_radius=.5) for c in (cL, cR)], run_time=1.2)
        self.at("Chance is safe")
        mg, pt = mini_graph(1.0)
        self.play(FadeIn(mg), run_time=.8)
        self.play(Indicate(mg[1], color=TEAL), run_time=1.0)
        self.at("One connected")
        self.play(Indicate(cL.rib, color=VIOLET, scale_factor=1.2), Indicate(cR.rib, color=VIOLET, scale_factor=1.2), run_time=1.0)
        rng = random.Random(2)
        homes = [(s.get_center().copy()) for s in cL.rib] + [(s.get_center().copy()) for s in cR.rib]
        allr = list(cL.rib) + list(cR.rib)
        self.play(*[s.animate.shift(P3(rng.uniform(-.25, .25), rng.uniform(-.25, .25))).scale(.6) for s in allr], run_time=.8)
        self.play(*[s.animate.move_to(h).scale(1 / .6) for s, h in zip(allr, homes)], run_time=.8)
        self.finish()


class S15End(EndCard):
    LINE = "Chance is safe only for many units; one connected unit needs control."
