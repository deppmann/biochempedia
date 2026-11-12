"""The Price of Cold (film 2 of Thermoregulation): the cost of holding body temperature as the air cools.

COLOR MAP (identical to film 1, "Where the Balance Sits")
  ORANGE = heat made, M (tap, dots, curves)
  YELLOW = heat gained, G (tap)
  BLUE   = the dry leak, C (outlet; its WIDTH is conductance)
  CYAN   = evaporation, E (pale wisps)
  RED    = body temperature Tb (tank level and thermometer)
  GREY   = air temperature Ta (dashed line) and the gap Tb - Ta (double-headed bar)
  TEXT   = labels
Every curve is computed from M = C x (Tb - Ta) with invented mouse-like values:
  Tb = 37, basal rate = 1 unit, floor conductance Cmin = BASAL / (Tb - Tlc),
  mouse Tlc = 28, arctic animal Tlc = 5, tropical animal Tlc = 33.
"""
import numpy as np
from bp_style import *  # noqa: F401,F403

ORANGE = "#F2994A"
CYAN = "#A7ECF2"
FUR = "#C9A27E"
BG_DARK = "#0f1117"
P = lambda x, y: np.array([x, y, 0.0])


def lvl(T):
    return (T + 5.0) / 45.0


def rflow(v):
    return 0.0 if v < 0.05 else min(1.0, 0.1 + v / 20.0)


class Flow(VGroup):
    """Dots drifting along a path; speed and size follow rate(); vis is a ValueTracker 0..1."""

    def __init__(self, pts, rate, color, vis=None, n=10, pipe=None, pipe_w=None, pipe_op=0.35, rmax=0.07, seed=0):
        super().__init__()
        self.pts, self.rate, self.vis, self.rmax = pts, rate, vis or ValueTracker(1), rmax
        self.pipe_w = pipe_w
        self.pipe = None
        if pipe is not None:
            self.pipe = VMobject().set_points_as_corners([P(*p) for p in pipe]).set_stroke(color, 20, opacity=pipe_op)
            self.pipe_op = pipe_op
            self.add(self.pipe)
        self.dots = VGroup()
        rng = np.random.RandomState(seed)
        for i in range(n):
            d = Dot(radius=0.05, color=color)
            d.u = (i + rng.rand() * 0.5) / n
            d.off = rng.uniform(-1, 1)
            self.dots.add(d)
        self.add(self.dots)
        self.add_updater(self._tick)

    def _tick(self, m, dt):
        v = self.vis.get_value()
        if self.pipe is not None:
            w = self.pipe_w() if self.pipe_w else 20
            self.pipe.set_stroke(width=w, opacity=self.pipe_op * v)
        pts = [P(*p) for p in self.pts()]
        seg = [np.linalg.norm(pts[i + 1] - pts[i]) for i in range(len(pts) - 1)]
        L = max(sum(seg), 0.3)
        r = self.rate() * v
        for d in self.dots:
            d.u = (d.u + dt * (0.5 + 1.3 * r) / L) % 1.0
            s = d.u * L
            i = 0
            while i < len(seg) - 1 and s > seg[i]:
                s -= seg[i]
                i += 1
            a, b = pts[i], pts[i + 1]
            t = s / max(seg[i], 1e-6)
            pos = a + (b - a) * min(t, 1)
            dirv = (b - a) / max(seg[i], 1e-6)
            perp = np.array([-dirv[1], dirv[0], 0])
            d.move_to(pos + perp * d.off * (0.03 + 0.06 * r))
            d.set_width(2 * (0.03 + self.rmax * r))
            op = 0.0 if r < 0.02 else min(1.0, 5 * d.u, 5 * (1 - d.u))
            d.set_opacity(op)


class Sim:
    def __init__(self, cx=-1.0, w=2.8, h=4.4, bot=-2.3, Tb=37.0, Ta=30.0, M=0.0, G=0.0, C=1.0, E=0.0, k=0.5,
                 integrate=True, thermo_dx=-0.85, labels=True, gap_inside="right"):
        self.cx, self.w, self.h, self.bot = cx, w, h, bot
        self.L, self.R, self.top = cx - w / 2, cx + w / 2, bot + h
        self.Tb, self.Ta, self.M, self.G, self.C, self.E = [ValueTracker(v) for v in (Tb, Ta, M, G, C, E)]
        self.k, self.integrate, self.t = k, integrate, 0.0
        self.vis = {n: ValueTracker(1) for n in ("fill", "thermo", "air", "gap")}
        self.fv = {n: ValueTracker(1) for n in ("M", "G", "G2", "D", "E")}
        self.flows = {}
        yT = self.yT
        self.walls = VMobject().set_points_as_corners([P(self.L, self.top), P(self.L, bot), P(self.R, bot), P(self.R, self.top)]).set_stroke(TEXT, 8)
        self.fill = VMobject().set_stroke(width=0)
        self.fill.add_updater(self._fill)
        tx = cx + (-(w / 2) + thermo_dx) if thermo_dx < 0 else cx + (w / 2) + thermo_dx
        self.tx = tx
        tube = RoundedRectangle(corner_radius=0.15, width=0.3, height=h, stroke_color=TEXT, stroke_width=4).move_to(P(tx, bot + h / 2))
        bulb = Circle(radius=0.27, color=TEXT, stroke_width=4).set_fill(RED, 0.95).move_to(P(tx, bot - 0.08))
        self.mercury = VMobject().set_stroke(width=0)
        self.mercury.add_updater(self._merc)
        self.thermo = VGroup(tube, bulb)
        def _thermo_op(m):
            v = self.vis["thermo"].get_value()
            m[0].set_stroke(opacity=v)
            m[1].set_stroke(opacity=v)
            m[1].set_fill(RED, opacity=0.95 * v)
        self.thermo.add_updater(_thermo_op)
        self.clock = Mobject()
        self.clock.add_updater(self._step)
        # air line (dashes) and gap bar
        self.dashes = VGroup(*[Line(P(0, 0), P(0.1, 0), color=GREY, stroke_width=5) for _ in range(14)])
        self.dashes.add_updater(self._dash)
        self.gapbar = VMobject()
        self.gapbar.add_updater(self._gap)
        self.air_lab = T("air", 28, GREY)
        self.gap_lab = T("gap", 28, GREY)
        self.air_lab.add_updater(self._airlab)
        self.gap_lab.add_updater(self._gaplab)
        self.gx = self.R - 0.45
        self.labels = labels

    def y(self, T):
        return self.bot + self.h * min(max(lvl(T), 0.0), 1.05)

    def yT(self):
        return self.y(self.Tb.get_value())

    def yA(self):
        return self.y(self.Ta.get_value())

    def leak(self):
        return max(0.0, self.C.get_value() * (self.Tb.get_value() - self.Ta.get_value()))

    def _step(self, m, dt):
        self.t += dt
        if self.integrate:
            Tb = self.Tb.get_value()
            d = self.M.get_value() + self.G.get_value() - self.E.get_value() - self.C.get_value() * (Tb - self.Ta.get_value())
            self.Tb.set_value(Tb + self.k * d * dt)

    def _fill(self, m, dt):
        yT = self.yT()
        xs = np.linspace(self.L, self.R, 16)[::-1]
        top = [P(x, yT + 0.04 * np.sin(2.4 * x + 2.0 * self.t)) for x in xs]
        pts = [P(self.L, self.bot), P(self.R, self.bot)] + top
        m.set_points_as_corners(pts + [pts[0]])
        m.set_fill(RED, opacity=0.5 * self.vis["fill"].get_value())

    def _merc(self, m, dt):
        yT, x = self.yT(), self.tx
        m.set_points_as_corners([P(x - 0.07, self.bot), P(x + 0.07, self.bot), P(x + 0.07, yT), P(x - 0.07, yT), P(x - 0.07, self.bot)])
        m.set_fill(RED, opacity=0.95 * self.vis["thermo"].get_value())

    def _dash(self, m):
        y = self.yA()
        a, b = self.L - 0.2, self.R + 0.2
        n = len(m)
        step = (b - a) / n
        v = self.vis["air"].get_value()
        for i, d in enumerate(m):
            d.put_start_and_end_on(P(a + i * step + 0.03, y), P(a + (i + 1) * step - 0.08, y))
            d.set_stroke(opacity=v)

    def _gap(self, m):
        a, b = self.yA(), self.yT()
        v = self.vis["gap"].get_value()
        if abs(b - a) < 0.15 or v < 0.02:
            m.become(VMobject())
            return
        m.become(DoubleArrow(P(self.gx, a), P(self.gx, b), buff=0, color=GREY, stroke_width=7, tip_length=0.2,
                             max_tip_length_to_length_ratio=0.4).set_opacity(v))

    def _airlab(self, m):
        m.move_to(P(self.R + 0.2 + m.width / 2 + getattr(self, 'air_off', 0.05), self.yA()))
        m.set_opacity(self.vis["air"].get_value())

    def _gaplab(self, m):
        m.move_to(P(self.gx - 0.15 - m.width / 2, (self.yA() + self.yT()) / 2))
        m.set_opacity(self.vis["gap"].get_value() if abs(self.yT() - self.yA()) > 0.45 else 0)

    def flow(self, name, pts, color, rate, pipe=None, pipe_w=None, rmax=0.07, seed=0):
        f = Flow(pts, rate, color, vis=self.fv[name], pipe=pipe, pipe_w=pipe_w, rmax=rmax, seed=seed)
        self.flows[name] = f
        return f

    def base(self):
        return Group(self.clock, self.fill, self.walls, self.mercury, self.thermo)

    def air(self):
        return VGroup(self.dashes, self.gapbar, self.air_lab, self.gap_lab)




def valve(x, y, color):
    c = Circle(radius=0.2, color=color, stroke_width=5).set_fill(BG_DARK, 1).move_to(P(x, y))
    h = Line(P(x - 0.22, y + 0.3), P(x + 0.22, y + 0.3), color=color, stroke_width=6)
    st = Line(P(x, y + 0.2), P(x, y + 0.3), color=color, stroke_width=6)
    return VGroup(c, h, st)


BG_DARK = "#0f1117"




def mouse(x, y, s=1.0):
    col = "#B9B2A6"
    body = Ellipse(width=2.2 * s, height=1.15 * s, stroke_width=0).set_fill(col, 1)
    head = Ellipse(width=0.95 * s, height=0.8 * s, stroke_width=0).set_fill(col, 1).shift(LEFT * 1.15 * s + UP * 0.12 * s)
    ear = Circle(radius=0.24 * s, stroke_width=0).set_fill("#D9A7A0", 1).shift(LEFT * 0.95 * s + UP * 0.55 * s)
    eye = Dot(radius=0.05 * s, color="#222222").shift(LEFT * 1.4 * s + UP * 0.2 * s)
    nose = Dot(radius=0.06 * s, color="#D9A7A0").shift(LEFT * 1.62 * s + UP * 0.1 * s)
    tail = ArcBetweenPoints(P(1.05 * s, -0.1 * s), P(2.0 * s, 0.45 * s), angle=-1.2).set_stroke("#D9A7A0", 5)
    legs = VGroup(Ellipse(width=0.4 * s, height=0.22 * s, stroke_width=0).set_fill(col, 1).shift(LEFT * 0.5 * s + DOWN * 0.55 * s),
                  Ellipse(width=0.4 * s, height=0.22 * s, stroke_width=0).set_fill(col, 1).shift(RIGHT * 0.6 * s + DOWN * 0.55 * s))
    g = VGroup(legs, tail, body, head, ear, eye, nose)
    return g.move_to(P(x, y))




# ---------------------------------------------------------------- the model
TB, BMR = 37.0, 1.0
CM = {"mouse": BMR / 9.0, "fox": BMR / 32.0, "trop": BMR / 4.0}


def Cof(Ta, cm):
    return max(cm, BMR / max(TB - Ta, 0.5))


def Mof(Ta, cm):
    return Cof(Ta, cm) * (TB - Ta)


def tlc(cm):
    return TB - BMR / cm


# ---------------------------------------------------------------- the plot (one world, carried)
SX, SY = 6.8 / 45.0, 5.2 / 5.5


def X(Ta):
    return -0.6 + (Ta + 5.0) * SX


def Y(M):
    return -2.6 + M * SY


def pt(Ta, M):
    return P(X(Ta), Y(M))


def axes_parts():
    xax = Line(pt(-5, 0), pt(40, 0), color=TEXT, stroke_width=5)
    yax = Line(pt(-5, 0), pt(-5, 5.5), color=TEXT, stroke_width=5)
    ylab = T("heat made (M)", 28, ORANGE).rotate(PI / 2).move_to(P(-1.08, 0.0))
    xlab = T("air temperature (Ta)", 28, GREY).move_to(P(2.8, -3.45))
    cold = T("cold", 26, GREY).move_to(P(-0.1, -3.45))
    warm = T("warm", 26, GREY).move_to(P(6.0, -3.45))
    return dict(xax=xax, yax=yax, ylab=ylab, xlab=xlab, cold=cold, warm=warm)


def tag():
    t = T("computed, invented values", 22, GREY)
    fit(t, max_w=3.5)
    return t.move_to(P(5.05, 3.2))


def dot_at(Ta, cm=CM["mouse"]):
    return Dot(pt(Ta, Mof(Ta, cm)), radius=0.09, color=ORANGE)


def flat_line(cm=CM["mouse"], op=1.0, w=7):
    return Line(pt(37, BMR), pt(tlc(cm), BMR), color=ORANGE, stroke_width=w).set_stroke(opacity=op)


def limb_line(cm=CM["mouse"], op=1.0, w=7, to=-5):
    return Line(pt(tlc(cm), BMR), pt(to, Mof(to, cm)), color=ORANGE, stroke_width=w).set_stroke(opacity=op)


def dash_ext(op=1.0):
    return DashedLine(pt(28, BMR), pt(37, 0), color=ORANGE, stroke_width=6, dash_length=0.14).set_stroke(opacity=op)


def band():
    w = X(37) - X(28)
    return Rectangle(width=w, height=Y(5.5) - Y(0), stroke_width=0).set_fill(GREY, 0.18).move_to(P((X(28) + X(37)) / 2, (Y(0) + Y(5.5)) / 2))


MOUSE_TA = [36, 34, 32, 30, 28, 25, 22, 19, 16, 13, 10, 7, 4, 1, -2]


# ---------------------------------------------------------------- the tank world
def tank(Ta=36.0, cm=CM["mouse"], fur=0.1, sync=True, furn=12):
    s = Sim(cx=-4.4, w=2.2, h=3.3, bot=-1.6, Tb=TB, Ta=Ta, integrate=False, thermo_dx=-0.9)
    s.cm, s.fur, s.furvis = ValueTracker(cm), ValueTracker(fur), ValueTracker(1)
    s.sync = Mobject()

    def _sync(m, dt=0):
        ta, c = s.Ta.get_value(), s.cm.get_value()
        s.C.set_value(Cof(ta, c))
        s.M.set_value(Mof(ta, c))

    if sync:
        s.sync.add_updater(_sync)
        _sync(None)
    s.flow("M", lambda: [(-6.0, 2.55), (-4.9, 2.55), (-4.9, s.yT() + 0.05)], ORANGE,
           lambda: min(1.0, 0.12 + 0.2 * s.M.get_value()),
           pipe=[(-6.0, 2.55), (-4.9, 2.55), (-4.9, 1.95)], pipe_w=lambda: min(46, 6 + 10 * s.M.get_value()), seed=1)
    dr = [(-4.5, s.bot), (-4.5, -2.55), (-2.0, -2.55)]
    s.flow("D", lambda: dr, BLUE, lambda: min(1.0, 0.12 + 0.2 * s.leak()), pipe=dr,
           pipe_w=lambda: min(42, 90 * s.C.get_value()), seed=3)
    s.valveM = valve(-5.5, 2.55, ORANGE)
    # fur strands along the left wall and the bottom (not at the outlet)
    n = furn
    ys = np.linspace(s.bot + 0.25, s.top - 0.15, n)
    xs = [x for x in np.linspace(s.L + 0.3, s.R - 0.3, 6) if abs(x + 4.5) > 0.45]
    strands = VGroup(*[Line(P(0, 0), P(0.1, 0), color=FUR, stroke_width=4) for _ in range(n + len(xs))])
    strands.n, strands.xs, strands.ys = n, xs, ys

    def _fur(m):
        ln = 0.06 + 0.5 * s.fur.get_value()
        op = s.furvis.get_value()
        for i, d in enumerate(m):
            if i < m.n:
                d.put_start_and_end_on(P(s.L, m.ys[i]), P(s.L - ln, m.ys[i] + 0.35 * ln))
            else:
                x = m.xs[i - m.n]
                d.put_start_and_end_on(P(x, s.bot), P(x + 0.35 * ln, s.bot - ln))
            d.set_stroke(opacity=op)

    strands.add_updater(_fur)
    s.furs = strands
    s.vis["air"].set_value(1)
    s.gap_lab.font_size = 28
    rng = np.random.RandomState(7)
    bub = VGroup(*[Dot(radius=0.09, color="#F7B7AE") for _ in range(22)])
    for d in bub:
        d.u, d.x, d.sp = rng.rand(), rng.uniform(-0.9, 0.9), rng.uniform(0.12, 0.3)

    def _bub(m, dt):
        top = s.yT() - 0.1
        for d in m:
            d.u = (d.u + dt * d.sp) % 1.0
            d.move_to(P(s.cx + d.x + 0.08 * np.sin(6 * d.u), s.bot + 0.15 + d.u * max(top - s.bot - 0.15, 0.1)))
            d.set_opacity(0.45 * s.vis["fill"].get_value() * min(1, 4 * d.u, 4 * (1 - d.u)))

    bub.add_updater(_bub)
    s.bub = bub
    return s


def put_tank(sc, s, air=True):
    sc.add(s.sync, s.base(), s.bub, s.flows["M"], s.flows["D"], s.valveM, s.furs)
    if air:
        sc.add(s.air())


def tank_vis(s, v, keys=("fill", "thermo", "air", "gap")):
    return [s.vis[k].animate.set_value(v) for k in keys] + [s.fv["M"].animate.set_value(v), s.fv["D"].animate.set_value(v), s.furvis.animate.set_value(v)]


# ---------------------------------------------------------------- the chamber (scene 1)
def air_thermo(ta):
    tube = RoundedRectangle(corner_radius=0.15, width=0.3, height=3.0, stroke_color=TEXT, stroke_width=4).move_to(P(-2.6, -0.3))
    fill = VMobject().set_stroke(width=0)

    def f(m):
        y = -1.8 + 3.0 * min(max(lvl(ta.get_value()), 0.0), 1.0)
        m.set_points_as_corners([P(-2.67, -1.8), P(-2.53, -1.8), P(-2.53, y), P(-2.67, y), P(-2.67, -1.8)])
        m.set_fill(GREY, 0.95)

    fill.add_updater(f)
    lab = T("air", 28, GREY).move_to(P(-2.6, 1.55))
    return VGroup(tube, fill, lab)


def chamber(ta):
    box = RoundedRectangle(corner_radius=0.3, width=4.3, height=4.3, stroke_color=TEXT, stroke_width=6).move_to(P(-4.15, -0.15))
    mo = mouse(-4.6, -1.6, 0.75)
    th = air_thermo(ta)
    fin = Flow(lambda: None, None, GREY) if False else None
    ain = [(-5.4, 3.0), (-5.4, 1.2)]
    aout = [(-3.4, 1.2), (-3.4, 3.0)]
    f1 = Flow(lambda: ain, lambda: 0.4, GREY, pipe=ain, pipe_w=lambda: 14, seed=5)
    f2 = Flow(lambda: aout, lambda: 0.4, GREY, pipe=aout, pipe_w=lambda: 14, seed=6)
    return box, mo, th, f1, f2


# ---------------------------------------------------------------- animals (scene 9)
def fox(x, y, s=1.0):
    col = "#EDE7DC"
    tail = Ellipse(width=1.5 * s, height=0.7 * s, stroke_width=0).set_fill(col, 1).rotate(0.5).shift(RIGHT * 1.35 * s + UP * 0.15 * s)
    body = Ellipse(width=2.1 * s, height=1.0 * s, stroke_width=0).set_fill(col, 1)
    ruff = Ellipse(width=1.0 * s, height=0.95 * s, stroke_width=0).set_fill(col, 1).shift(LEFT * 0.85 * s + UP * 0.1 * s)
    head = Ellipse(width=0.85 * s, height=0.62 * s, stroke_width=0).set_fill(col, 1).shift(LEFT * 1.3 * s + UP * 0.28 * s)
    ear = Triangle(stroke_width=0).set_fill(col, 1).scale(0.16 * s).shift(LEFT * 1.15 * s + UP * 0.7 * s)
    eye = Dot(radius=0.045 * s, color="#222222").shift(LEFT * 1.45 * s + UP * 0.35 * s)
    nose = Dot(radius=0.06 * s, color="#222222").shift(LEFT * 1.72 * s + UP * 0.28 * s)
    legs = VGroup(*[Line(P(dx * s, -0.35 * s), P(dx * s, -0.7 * s), color="#C9C2B5", stroke_width=7) for dx in (-0.55, -0.25, 0.5, 0.8)])
    return VGroup(legs, tail, body, ruff, head, ear, eye, nose).move_to(P(x, y))


def tropical(x, y, s=1.0):
    col = "#C9A27E"
    body = Ellipse(width=1.7 * s, height=0.55 * s, stroke_width=0).set_fill(col, 1)
    head = Ellipse(width=0.6 * s, height=0.45 * s, stroke_width=0).set_fill(col, 1).shift(LEFT * 0.95 * s + UP * 0.12 * s)
    ear = Circle(radius=0.12 * s, stroke_width=0).set_fill("#D9A7A0", 1).shift(LEFT * 0.85 * s + UP * 0.38 * s)
    eye = Dot(radius=0.04 * s, color="#222222").shift(LEFT * 1.1 * s + UP * 0.18 * s)
    tail = ArcBetweenPoints(P(0.8 * s, 0.0), P(1.9 * s, 0.5 * s), angle=-1.0).set_stroke(col, 4)
    legs = VGroup(*[Line(P(dx * s, -0.25 * s), P(dx * s, -0.65 * s), color=col, stroke_width=4) for dx in (-0.5, -0.25, 0.4, 0.65)])
    leaves = VGroup(*[Ellipse(width=0.9 * s, height=0.35 * s, stroke_width=0).set_fill(GREEN, 0.85).rotate(a).shift(P(dx * s, -0.78 * s)) for a, dx in ((0.5, -0.9), (-0.4, 0.0), (0.6, 0.9))])
    return VGroup(leaves, legs, tail, body, head, ear, eye).move_to(P(x, y))


def mini_tank(x, y, fur=False):
    walls = VMobject().set_points_as_corners([P(x - 0.4, y + 0.6), P(x - 0.4, y - 0.6), P(x + 0.4, y - 0.6), P(x + 0.4, y + 0.6)]).set_stroke(TEXT, 6)
    fill = Rectangle(width=0.8, height=0.9, stroke_width=0).set_fill(RED, 0.5).move_to(P(x, y - 0.6 + 0.45))
    tap = Line(P(x - 0.2, y + 1.0), P(x - 0.2, y + 0.1), color=ORANGE, stroke_width=14)
    return VGroup(fill, walls, tap)


class Sc(SpokenScene):
    pass


def step_to(sc, tracker, v, rt=0.3, hold=0.0, *extra):
    sc.play(tracker.animate.set_value(v), *extra, run_time=rt)
    if hold > 0:
        sc.wait(hold)


def add_axes(sc, a, keys=("xax", "yax", "ylab", "xlab", "cold", "warm")):
    sc.add(*[a[k] for k in keys])


def mouse_curve(op=1.0, dash=True, dots=True):
    g = [flat_line(op=op), limb_line(op=op)]
    if dash:
        g.append(dash_ext(op))
    if dots:
        g += [dot_at(t) for t in MOUSE_TA]
    return g


class S00Title(TitleCard):
    LESSON = "Heat Balance and Body Temperature"
    TITLE = "The Price of Cold"


class S01Question(Sc):
    def construct(self):
        ta = ValueTracker(36)
        box, mo, th, f1, f2 = chamber(ta)
        a = axes_parts()
        self.add(th)
        self.play(FadeIn(box), FadeIn(mo), run_time=1.0)
        self.at("chamber")
        self.add(f1, f2)
        self.wait(0.8)
        self.at("cool the air")
        step_to(self, ta, 34, 0.3, 0.3)
        self.at("one step at a time")
        for v in (32, 30):
            step_to(self, ta, v, 0.3, 0.4)
        self.at("what happens to the heat")
        q = T("?", 110, YELLOW, weight=BOLD).move_to(P(0.9, 0.4))
        q.t = 0.0

        def bob(m, dt):
            m.t += dt
            m.move_to(P(0.9, 0.4 + 0.15 * np.sin(3 * m.t)))

        q.add_updater(bob)
        self.play(Create(a["xax"]), Create(a["yax"]), FadeIn(a["ylab"]), FadeIn(a["xlab"]), FadeIn(a["cold"]), FadeIn(a["warm"]), FadeIn(q), run_time=1.4)
        for v in (28, 26):
            step_to(self, ta, v, 0.3, 0.5)
        self.at("and why does nothing happen")
        card = T("Cooler air: when does the mouse pay?", 36, TEXT, font=TITLE_FONT)
        fit(card, max_w=10.5)
        card.move_to(P(0, 3.3))
        self.play(FadeIn(card), run_time=0.8)
        for v in (24, 22):
            step_to(self, ta, v, 0.3, 0.5)
        self.finish()


class S02Link(Sc):
    def construct(self):
        ta = ValueTracker(22)
        box, mo, th, f1, f2 = chamber(ta)
        a = axes_parts()
        q = T("?", 110, YELLOW, weight=BOLD).move_to(P(0.9, 0.4))
        card = T("Cooler air: when does the mouse pay?", 36, TEXT, font=TITLE_FONT)
        fit(card, max_w=10.5)
        card.move_to(P(0, 3.3))
        self.add(box, mo, th, f1, f2, q, card)
        add_axes(self, a)
        self.play(FadeOut(q), FadeOut(card), run_time=0.8)
        s = tank(Ta=36.0, cm=CM["mouse"], sync=False)
        s.C.set_value(0.2)
        s.M.set_value(1.0)
        s.vis["air"].set_value(0)
        s.vis["gap"].set_value(0)
        for k in ("M", "D"):
            s.fv[k].set_value(0)
        s.vis["fill"].set_value(0)
        s.vis["thermo"].set_value(0)
        s.furvis.set_value(0)
        self.at("drew the body")
        self.add(s.base(), s.furs)
        self.remove(th, f1, f2)
        self.play(FadeOut(mo), FadeTransform(box, s.walls),
                  s.vis["fill"].animate.set_value(1), s.vis["thermo"].animate.set_value(1), s.furvis.animate.set_value(1), run_time=1.8)
        self.at("flows in through the orange tap")
        self.add(s.flows["M"], s.valveM)
        lm = T("heat made, M", 28, ORANGE).move_to(P(-5.2, 3.4))
        self.play(FadeIn(s.valveM), s.fv["M"].animate.set_value(1), FadeIn(lm), run_time=1.0)
        self.at("blue outlet")
        self.add(s.flows["D"])
        ld = T("dry leak, C", 28, BLUE).move_to(P(-3.6, -3.3))
        self.play(s.fv["D"].animate.set_value(1), FadeIn(ld), run_time=1.0)
        self.at("whose width can change")
        self.play(s.C.animate.set_value(0.38), run_time=0.9)
        self.play(s.C.animate.set_value(0.1), run_time=0.9)
        self.play(s.C.animate.set_value(0.2), run_time=0.6)
        self.at("now we watch")
        s.flow("G", lambda: [(-2.4, 2.55), (-3.6, 2.55), (-3.6, s.yT() + 0.05)], YELLOW, lambda: 0.3,
               pipe=[(-2.4, 2.55), (-3.6, 2.55), (-3.6, 1.95)], pipe_w=lambda: 14, seed=2)
        s.flow("E", lambda: [(-4.1, s.yT()), (-4.1, 2.3)], CYAN, lambda: 0.3, rmax=0.1, seed=4)
        vg = valve(-3.0, 2.55, YELLOW)
        self.add(s.flows["G"], s.flows["E"], vg)
        s.fv["G"].set_value(0)
        s.fv["E"].set_value(0)
        self.play(FadeIn(vg), s.fv["G"].animate.set_value(1), s.fv["E"].animate.set_value(1), run_time=0.8)
        lg = T("no sun in the chamber", 26, YELLOW).move_to(P(-1.6, 3.3))
        le = VGroup(T("evaporation left", 24, CYAN), T("out (model)", 24, CYAN)).arrange(DOWN, buff=0.12).move_to(P(-2.1, 1.95))
        self.play(s.fv["G"].animate.set_value(0), s.fv["E"].animate.set_value(0.25), FadeIn(lg), FadeIn(le), run_time=1.2)
        self.finish()


def cursor(s, cm=CM["mouse"]):
    ring = Circle(radius=0.35, color=YELLOW, stroke_width=7)
    ring.t = 0.0

    def u(m, dt):
        m.t += dt
        ta = s.Ta.get_value()
        m.move_to(pt(ta, Mof(ta, cm)))
        m.set_width(0.7 * (1 + 0.45 * np.sin(5 * m.t)))
        m.set_stroke(opacity=0.55 + 0.4 * np.sin(5 * m.t + 1))

    ring.add_updater(u)
    return ring


def stage(sc, s, a, dots=(), air=True, curve=False, extra=()):
    put_tank(sc, s, air=air)
    add_axes(sc, a)
    sc.add(tag())
    for d in dots:
        sc.add(dot_at(d))
    sc.add(*extra)
    sc.add(cursor(s))


class S03Measure(Sc):
    def construct(self):
        s = tank(Ta=36.0)
        s.vis["air"].set_value(0)
        s.vis["gap"].set_value(0)
        a = axes_parts()
        put_tank(self, s)
        add_axes(self, a)
        self.add(cursor(s))
        self.at("leave out sun")
        self.play(s.vis["air"].animate.set_value(1), s.vis["gap"].animate.set_value(1), FadeIn(tag()), run_time=1.0)
        self.at("so heat made must match")
        bar = Line(P(2.0, 1.5), P(6.0, 1.5), color=TEXT, stroke_width=6)
        piv = Triangle(stroke_width=0).set_fill(GREY, 1).scale(0.22).move_to(P(4.0, 1.2))
        lM = T("M", 44, ORANGE).move_to(P(2.6, 2.0))
        lC = T("C × (Tb − Ta)", 32, BLUE).move_to(P(5.0, 2.0))
        beam = VGroup(bar, lM, lC)
        self.play(FadeIn(piv), FadeIn(beam), run_time=0.8)
        self.play(Rotate(beam, 0.12, about_point=P(4.0, 1.5)), run_time=0.4)
        self.play(Rotate(beam, -0.12, about_point=P(4.0, 1.5)), run_time=0.5)
        self.at("from the oxygen")
        gl = T("oxygen used → heat made", 26, TEXT).move_to(P(-2.3, 3.4))
        gbox = RoundedRectangle(corner_radius=0.1, width=3.0, height=0.34, stroke_color=TEXT, stroke_width=3).move_to(P(-2.3, 2.9))
        gfill = Rectangle(width=0.1, height=0.28, stroke_width=0).set_fill(ORANGE, 0.95)

        def gf(m):
            w = max(0.05, 2.9 * s.M.get_value() / 5.5)
            m.stretch_to_fit_width(w)
            m.move_to(P(-3.75 + w / 2, 2.9))

        gfill.add_updater(gf)
        self.play(FadeIn(gl), FadeIn(gbox), FadeIn(gfill), run_time=0.9)
        self.at("at each step")
        self.play(FadeOut(beam), FadeOut(piv), run_time=0.6)
        self.at("plot one orange point")
        for t in (36, 34, 32):
            self.play(FadeIn(dot_at(t), shift=DOWN * 0.6), run_time=0.45)
            if t != 32:
                step_to(self, s.Ta, t - 2, 0.5)
        self.wait(0.5)
        self.finish()


class S04Flat(Sc):
    def construct(self):
        s = tank(Ta=32.0)
        a = axes_parts()
        stage(self, s, a, dots=(36, 34, 32))
        s.furvis.set_value(1)
        self.at("at first")
        self.play(Indicate(s.valveM, color=ORANGE), run_time=1.0)
        self.at("the mouse holds")
        step_to(self, s.Ta, 30, 1.6)
        self.add(dot_at(30))
        self.play(FadeIn(self.mobjects[-1], shift=DOWN * 0.5), run_time=0.4)
        self.at("without making extra heat")
        step_to(self, s.Ta, 28, 1.6)
        d = dot_at(28)
        self.play(FadeIn(d, shift=DOWN * 0.5), run_time=0.4)
        self.at("instead it narrows")
        self.play(Indicate(s.flows["D"], color=BLUE, scale_factor=1.15), run_time=1.5)
        self.at("skin vessels close")
        ic = Line(P(1.7, 2.35), P(2.7, 2.35), color=RED, stroke_width=14)
        ic.add_updater(lambda m: m.set_stroke(width=max(3, 40 * s.C.get_value())))
        vl = T("skin vessels close", 28, TEXT).move_to(P(4.9, 2.35))
        self.play(FadeIn(ic), FadeIn(vl), run_time=0.8)
        self.at("fur lifts")
        self.play(s.fur.animate.set_value(0.7), run_time=1.5)
        self.finish()


class S05Tnz(Sc):
    def construct(self):
        s = tank(Ta=28.0, fur=0.7)
        a = axes_parts()
        stage(self, s, a, dots=(36, 34, 32, 30, 28))
        self.at("flat stretch")
        fl = flat_line()
        bd = band()
        self.play(Create(fl), FadeIn(bd), run_time=1.5)
        self.at("zone")
        zl = VGroup(T("thermoneutral", 28, TEXT), T("zone", 28, TEXT)).arrange(DOWN, buff=0.22).move_to(P(5.0, 2.0))
        self.play(FadeIn(zl), run_time=0.8)
        self.at("the resting rate")
        self.play(Indicate(fl, color=YELLOW, scale_factor=1.0), run_time=1.0)
        self.at("basal metabolic rate")
        bl = T("basal metabolic rate (BMR)", 28, ORANGE)
        fit(bl, max_w=5.2)
        bl.move_to(P(3.7, -0.9))
        self.play(FadeIn(bl), run_time=0.8)
        self.at("measured at rest")
        self.play(Indicate(bl, color=ORANGE, scale_factor=1.08), run_time=1.5)
        self.finish()


def carry_flat(sc):
    sc.add(flat_line(), band())
    for t in (36, 34, 32, 30, 28):
        sc.add(dot_at(t))


class S06Floor(Sc):
    def construct(self):
        s = tank(Ta=29.0, fur=0.7)
        a = axes_parts()
        stage(self, s, a)
        carry_flat(self)
        self.at("only get so narrow")
        self.play(s.Ta.animate.set_value(28.0), Indicate(s.flows["D"], color=BLUE, scale_factor=1.15), run_time=1.6)
        self.at("lower critical temperature")
        ln = DashedLine(pt(28, 0), pt(28, 2.4), color=GREY, stroke_width=4)
        tl = VGroup(T("lower critical", 28, TEXT), T("temperature", 28, TEXT)).arrange(DOWN, buff=0.22).move_to(P(2.8, 0.7))
        self.play(Create(ln), FadeIn(tl), run_time=1.5)
        self.at("our model mouse reaches")
        cl = VGroup(Line(P(-3.95, -2.25), P(-3.95, -2.85), color=TEXT, stroke_width=6), Line(P(-3.05, -2.25), P(-3.05, -2.85), color=TEXT, stroke_width=6))
        self.play(Create(cl), run_time=1.0)
        self.at("its conductance is at its minimum")
        ml = T("model: C at its minimum", 28, BLUE).move_to(P(-4.0, -3.4))
        self.play(FadeIn(ml), Indicate(s.flows["D"], color=BLUE, scale_factor=1.2), run_time=1.5)
        self.finish()


class S07Climb(Sc):
    def construct(self):
        s = tank(Ta=28.0, fur=0.7)
        a = axes_parts()
        stage(self, s, a)
        carry_flat(self)
        self.add(DashedLine(pt(28, 0), pt(28, 2.4), color=GREY, stroke_width=4))
        cl = VGroup(Line(P(-3.95, -2.25), P(-3.95, -2.85), color=TEXT, stroke_width=6), Line(P(-3.05, -2.25), P(-3.05, -2.85), color=TEXT, stroke_width=6))
        self.add(cl)
        self.at("below that")
        pts = [25, 22, 19, 16, 13, 10, 7, 4, 1, -2]
        self.play(s.Ta.animate.set_value(25), FadeIn(dot_at(25), shift=DOWN * 0.4), run_time=1.0)
        ml = VGroup(T("model: C held", 28, BLUE), T("at minimum", 28, BLUE)).arrange(DOWN, buff=0.18).move_to(P(4.6, 0.3))
        self.play(FadeIn(ml), run_time=0.7)
        self.play(s.Ta.animate.set_value(22), FadeIn(dot_at(22), shift=DOWN * 0.4), run_time=1.2)
        self.at("now only the orange tap")
        self.play(Indicate(s.valveM, color=ORANGE), s.Ta.animate.set_value(19), FadeIn(dot_at(19), shift=DOWN * 0.4), run_time=1.2)
        self.play(s.Ta.animate.set_value(16), FadeIn(dot_at(16), shift=DOWN * 0.4), run_time=1.0)
        self.at("each degree colder")
        a1, a2 = pt(13, Mof(13, CM["mouse"])), pt(12, Mof(12, CM["mouse"]))
        tri = Polygon(a1, P(a2[0], a1[1]), a2, color=YELLOW, stroke_width=4).set_fill(YELLOW, 0.4)
        big = tri.copy().scale(6).move_to(P(4.9, 1.9))
        bl = T("one degree colder: + C", 26, YELLOW)
        fit(bl, max_w=3.6)
        bl.next_to(big, DOWN, buff=0.15)
        self.play(s.Ta.animate.set_value(13), FadeIn(dot_at(13), shift=DOWN * 0.4), FadeIn(tri), run_time=1.0)
        self.play(TransformFromCopy(tri, big), FadeIn(bl), s.Ta.animate.set_value(10), FadeIn(dot_at(10), shift=DOWN * 0.4), run_time=1.5)
        self.at("so the points climb")
        for t in (7, 4, 1, -2):
            self.play(s.Ta.animate.set_value(t), FadeIn(dot_at(t), shift=DOWN * 0.4), run_time=0.5)
        self.play(Create(limb_line(w=5)), run_time=1.0)
        self.finish()


class S08Extend(Sc):
    def construct(self):
        s = tank(Ta=-2.0, fur=0.7)
        a = axes_parts()
        stage(self, s, a)
        carry_flat(self)
        self.add(limb_line(), *[dot_at(t) for t in MOUSE_TA[5:]])
        self.at("extend that line")
        self.play(s.Ta.animate.set_value(28), run_time=2.4)
        d = dash_ext()
        self.play(Create(d), run_time=1.5)
        self.at("reaches zero at body temperature")
        tk = Line(pt(37, 0) + DOWN * 0.15, pt(37, 0) + UP * 0.15, color=RED, stroke_width=6)
        tl = T("Ta = Tb", 28, RED).move_to(P(X(37), -2.95))
        self.play(Create(tk), FadeIn(tl), run_time=1.0)
        self.at("only arithmetic")
        el = T("extrapolation only", 26, TEXT).move_to(P(2.3, -2.15))
        self.play(FadeIn(el), run_time=1.0)
        self.at("a living animal")
        self.play(Indicate(flat_line(), color=ORANGE), s.Ta.animate.set_value(32), run_time=2.5)
        self.finish()


def plot_full(sc, op=1.0, dots=True, dash=True):
    for m in mouse_curve(op=op, dash=dash, dots=dots):
        sc.add(m)


class S09Scholander(Sc):
    def construct(self):
        s = tank(Ta=32.0, fur=0.7)
        a = axes_parts()
        stage(self, s, a)
        plot_full(self)
        cr = T("Scholander, Irving and colleagues, 1950", 28, TEXT)
        fit(cr, max_w=6.4)
        cr.move_to(P(-3.3, 3.4))
        self.at("measured curves like this")
        self.play(FadeIn(cr), Indicate(flat_line(), color=YELLOW), run_time=1.2)
        self.play(s.Ta.animate.set_value(10), run_time=1.5)
        self.at("they plotted")
        self.play(Indicate(a["ylab"], color=YELLOW), Indicate(a["xlab"], color=YELLOW), run_time=1.5)
        self.at("for mammals")
        self.play(*tank_vis(s, 0), FadeOut(s.walls), FadeOut(s.valveM), run_time=1.0)
        self.remove(s.base(), s.bub, s.flows["M"], s.flows["D"], s.furs, s.air(), s.sync, *[m for m in self.mobjects if isinstance(m, Circle) and m.get_color() == ManimColor(YELLOW) and len(m.updaters) > 0])
        fx, tr = fox(-5.0, 1.3, 1.0), tropical(-5.0, -1.7, 1.0)
        snow = Ellipse(width=3.0, height=0.4, stroke_width=0).set_fill("#DDE6EE", 0.9).move_to(P(-5.0, 0.7))
        self.at("the arctic")
        self.play(FadeIn(snow), FadeIn(fx, shift=RIGHT * 0.6), FadeIn(mini_tank(-2.4, 1.3)), run_time=1.2)
        self.at("the tropics")
        self.play(FadeIn(tr, shift=RIGHT * 0.6), FadeIn(mini_tank(-2.4, -1.7)), run_time=1.2)
        sl = VGroup(T("same basal rate and body", 26, TEXT), T("temperature (assumed)", 26, TEXT)).arrange(DOWN, buff=0.06).move_to(P(-3.9, -3.3))
        self.play(FadeIn(sl), run_time=0.8)
        self.finish()


def fox_stage(sc, cm_val, Ta, fur=1.2):
    s = tank(Ta=Ta, cm=cm_val, fur=fur)
    return s


class S10Predict(Sc):
    def construct(self):
        a = axes_parts()
        add_axes(self, a)
        plot_full(self)
        fx, tr = fox(-5.0, 1.3, 1.0), tropical(-5.0, -1.7, 1.0)
        snow = Ellipse(width=3.0, height=0.4, stroke_width=0).set_fill("#DDE6EE", 0.9).move_to(P(-5.0, 0.7))
        sl = VGroup(T("same basal rate and body", 26, TEXT), T("temperature (assumed)", 26, TEXT)).arrange(DOWN, buff=0.06).move_to(P(-3.9, -3.3))
        m1, m2 = mini_tank(-2.4, 1.3), mini_tank(-2.4, -1.7)
        old = [fx, tr, snow, sl, m1, m2]
        self.add(*old)
        s = tank(Ta=10.0, cm=CM["mouse"], fur=0.7)
        for k in ("fill", "thermo", "air", "gap"):
            s.vis[k].set_value(0)
        for k in ("M", "D"):
            s.fv[k].set_value(0)
        s.furvis.set_value(0)
        put_tank(self, s)
        self.remove(s.walls, s.valveM)
        dots = [m for m in self.mobjects if isinstance(m, Dot) and m.get_color() is not None]
        self.at("thicker fur")
        self.play(*[FadeOut(o) for o in old], run_time=0.7)
        self.play(*tank_vis(s, 1), FadeIn(s.walls), FadeIn(s.valveM), run_time=0.7)
        self.play(s.cm.animate.set_value(CM["fox"]), s.fur.animate.set_value(1.2), run_time=2.5)
        self.at("same basal rate")
        self.play(Indicate(s.flows["D"], color=BLUE, scale_factor=1.15), run_time=1.5)
        self.at("does the bend move")
        card = T("Thicker fur: bend colder or warmer?", 36, TEXT, font=TITLE_FONT)
        fit(card, max_w=10.5)
        card.move_to(P(0, 3.3))
        line = DashedLine(pt(36, BMR), pt(-5, BMR), color=GREY, stroke_width=5)
        q = T("?", 70, YELLOW, weight=BOLD)
        q.t = 0.0

        def scan(m, dt):
            m.t += dt
            m.move_to(pt(14 + 12 * np.sin(1.6 * m.t), BMR) + UP * 0.5)

        q.add_updater(scan)
        self.play(FadeIn(card), Create(line), FadeIn(q), run_time=1.2)
        self.finish()


def pred_stage(sc, with_ring=False):
    a = axes_parts()
    add_axes(sc, a)
    sc.add(tag())
    sc.add(flat_line(op=0.35), limb_line(op=0.35))
    s = tank(Ta=10.0, cm=CM["fox"], fur=1.2)
    put_tank(sc, s)
    return s


class S11Pause(NarratedScene):
    def construct(self):
        a = axes_parts()
        add_axes(self, a)
        self.add(flat_line(op=0.35), limb_line(op=0.35))
        s = tank(Ta=10.0, cm=CM["fox"], fur=1.2)
        put_tank(self, s)
        card = T("Thicker fur: bend colder or warmer?", 36, TEXT, font=TITLE_FONT)
        fit(card, max_w=10.5)
        card.move_to(P(0, 3.3))
        line = DashedLine(pt(36, BMR), pt(-5, BMR), color=GREY, stroke_width=5)
        q = T("?", 70, YELLOW, weight=BOLD).move_to(pt(14, BMR) + UP * 0.5)
        self.add(card, line, q)
        base = Circle(radius=0.4, color=GREY, stroke_width=3).move_to(P(4.4, 1.6))
        ring = Circle(radius=0.4, color=GOLD, stroke_width=7).move_to(P(4.4, 1.6))
        self.add(base)
        self.play(Create(ring), run_time=4.4, rate_func=linear)
        self.finish()


def fox_curve(cm=CM["fox"], op=1.0, w=7):
    return VGroup(flat_line(cm, op, w), limb_line(cm, op, w))


def trace_curve(tr, cm):
    m = VMobject().set_stroke(ORANGE, 8)

    def upd(mm):
        ta = min(tr.get_value(), 35.99)
        t0 = tlc(cm)
        pts = [pt(36, BMR)]
        if ta < t0:
            pts += [pt(t0, BMR), pt(ta, Mof(ta, cm))]
        else:
            pts += [pt(ta, BMR)]
        mm.set_points_as_corners(pts)

    m.add_updater(upd)
    upd(m)
    return m


class S12Reveal(Sc):
    def construct(self):
        a = axes_parts()
        add_axes(self, a)
        self.add(tag())
        self.add(flat_line(op=0.35), limb_line(op=0.35))
        s = tank(Ta=10.0, cm=CM["fox"], fur=1.2)
        put_tank(self, s)
        self.add(s.furs)
        self.at("colder")
        self.play(s.Ta.animate.set_value(36), run_time=1.0)
        tc = trace_curve(s.Ta, CM["fox"])
        self.add(tc)
        self.at("a narrower outlet")
        self.play(s.Ta.animate.set_value(5), run_time=4.3, rate_func=linear)
        self.at("only across a bigger gap")
        self.play(Indicate(s.gapbar, color=YELLOW, scale_factor=1.3), run_time=1.5)
        self.at("below the bend")
        self.play(s.Ta.animate.set_value(-5), run_time=2.2, rate_func=linear)
        self.at("shallower")
        lb = T("gentler climb", 28, ORANGE).move_to(P(1.2, -0.9))
        self.play(FadeIn(lb), run_time=0.8)
        self.finish()


def three_curves(sc, trop=True):
    sc.add(flat_line(CM["mouse"], 0.5), limb_line(CM["mouse"], 0.5))
    sc.add(flat_line(CM["fox"]), limb_line(CM["fox"]))


def trop_limb(op=1.0, w=7):
    t0 = tlc(CM["trop"])
    ta_end = TB - 5.5 / CM["trop"]
    return VGroup(Line(pt(37, BMR), pt(t0, BMR), color=ORANGE, stroke_width=w), Line(pt(t0, BMR), pt(ta_end, 5.5), color=ORANGE, stroke_width=w)).set_stroke(opacity=op)


def curve_labels():
    return VGroup(T("tropical", 28, TEXT).move_to(P(1.4, 2.4)), T("mouse", 28, TEXT).move_to(P(0.55, 1.6)), T("arctic", 28, TEXT).move_to(P(0.5, -1.0)))


class S13Overlay(Sc):
    def construct(self):
        a = axes_parts()
        add_axes(self, a)
        self.add(tag())
        three_curves(self)
        s = tank(Ta=-5.0, cm=CM["fox"], fur=1.2)
        put_tank(self, s)
        self.add(s.furs)
        self.play(s.Ta.animate.set_value(36), run_time=14.0, rate_func=linear) if False else None
        self.at("that is the pattern")
        tp = trop_limb()
        self.play(Create(tp), s.Ta.animate.set_value(10), run_time=2.5)
        self.play(FadeIn(curve_labels()), run_time=0.8)
        self.at("thick furred arctic mammals")
        arr = DoubleArrow(pt(33, 0.25), pt(5, 0.25), buff=0, color=TEXT, stroke_width=5, tip_length=0.2)
        al = T("flat in colder air", 26, TEXT).move_to(P(2.9, -1.95))
        self.play(GrowArrow(arr), FadeIn(al), s.Ta.animate.set_value(20), run_time=2.0)
        self.at("into far colder air")
        self.play(Indicate(flat_line(CM["fox"]), color=YELLOW, scale_factor=1.0), s.Ta.animate.set_value(30), run_time=2.0)
        self.at("the difference lay mainly")
        tx = VGroup(T("difference: mainly", 28, TEXT), T("insulation (C),", 28, BLUE), T("not basal rate", 28, ORANGE)).arrange(DOWN, buff=0.08).move_to(P(5.2, 1.8))
        self.play(FadeIn(tx), FadeOut(arr), FadeOut(al), s.Ta.animate.set_value(36), run_time=1.5)
        self.at("not in a higher basal rate")
        self.play(s.Ta.animate.set_value(0), Indicate(flat_line(CM["fox"]), color=ORANGE, scale_factor=1.0), run_time=2.5)
        self.finish()


class S14Wrap(Sc):
    def construct(self):
        a = axes_parts()
        add_axes(self, a)
        self.add(tag())
        s = tank(Ta=0.0, cm=CM["fox"], fur=1.2)
        put_tank(self, s)
        self.add(s.furs)
        cur = VGroup(flat_line(CM["mouse"]), limb_line(CM["mouse"]), flat_line(CM["fox"]), limb_line(CM["fox"]), trop_limb())
        self.add(cur, curve_labels())
        self.at("so the curve is the heat balance")
        self.play(cur.animate.set_stroke(opacity=0.3), run_time=1.0)
        bal = VGroup(T("M", 38, ORANGE), T("=", 38, TEXT), T("C", 38, BLUE), T("×", 38, TEXT), T("(Tb − Ta)", 38, GREY)).arrange(RIGHT, buff=0.2).move_to(P(0.3, 3.25))
        self.play(FadeIn(bal), run_time=1.0)
        self.at("plotted against the air")
        self.play(Indicate(a["xlab"], color=YELLOW), run_time=1.2)
        self.at("conductance sets where the bend falls")
        bends = VGroup(*[Dot(pt(tlc(CM[k]), BMR), radius=0.16, color=BLUE) for k in ("trop", "mouse", "fox")])
        self.play(FadeIn(bends, scale=0.3), run_time=1.0)
        self.play(Indicate(bends, color=BLUE, scale_factor=1.5), run_time=1.0)
        self.at("and how steeply")
        end = P(-2.0, -2.55)
        mids = {"fox": pt(0, Mof(0, CM["fox"])), "mouse": pt(20, Mof(20, CM["mouse"])), "trop": pt(24, Mof(24, CM["trop"]))}
        lines = {k: Line(end, v, color=BLUE, stroke_width=3).set_stroke(opacity=0.0) for k, v in mids.items()}
        self.add(*lines.values())
        for k in ("fox", "mouse", "trop"):
            lines[k].set_stroke(opacity=1.0)
            self.play(s.cm.animate.set_value(CM[k]), lines[k].animate.set_stroke(opacity=1.0), run_time=0.9)
            self.wait(0.5)
            lines[k].set_stroke(opacity=0.25)
        self.at("climbs below it")
        self.play(Indicate(limb_line(CM["mouse"]), color=BLUE), run_time=1.2)
        self.finish()


class S15End(EndCard):
    LINE = "Conductance sets where cold starts to cost, and how much."
