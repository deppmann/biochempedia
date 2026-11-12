"""Where the Balance Sits: one tank of warmth, carried through the film.

COLOR MAP (same in every scene and in the second film)
  ORANGE = heat made, M (tap, arrows)
  YELLOW = heat gained from sun or rock, G (tap, arrows)
  BLUE   = the dry leak, C (outlet; its WIDTH is conductance)
  CYAN   = evaporation, E (pale wisps)
  RED    = body temperature Tb (tank level and thermometer)
  GREY   = air temperature Ta (dashed line) and the gap Tb - Ta (double-headed bar)
  TEXT   = labels
The tank level is computed: Tb moves by k * (M + G - E - C * (Tb - Ta)). Numbers are illustrative.
"""
import numpy as np
from bp_style import *  # noqa: F401,F403

ORANGE = "#F2994A"
CYAN = "#A7ECF2"
FUR = "#C9A27E"
P = lambda x, y: np.array([x, y, 0.0])


def lvl(T):
    return (T - 10.0) / 40.0


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


def worldA(Tb=39.0, Ta=30.0, M=6.5, G=2.5, C=1.0, E=0.0, k=0.5, integrate=True):
    s = Sim(Tb=Tb, Ta=Ta, M=M, G=G, C=C, E=E, k=k, integrate=integrate)
    s.flow("M", lambda: [(-4.8, 3.25), (-1.7, 3.25), (-1.7, s.yT() + 0.05)], ORANGE, lambda: rflow(s.M.get_value()),
           pipe=[(-4.8, 3.25), (-1.7, 3.25), (-1.7, 2.55)], seed=1)
    s.flow("G", lambda: [(2.9, 3.25), (-0.5, 3.25), (-0.5, s.yT() + 0.05)], YELLOW, lambda: rflow(s.G.get_value()),
           pipe=[(2.9, 3.25), (-0.5, 3.25), (-0.5, 2.55)], seed=2)
    dr = [(-0.4, s.bot), (-0.4, -3.2), (2.2, -3.2)]
    s.flow("D", lambda: dr, BLUE, lambda: rflow(s.leak()), pipe=dr, pipe_w=lambda: 20 * s.C.get_value(), seed=3)
    s.flow("E", lambda: [(0.0, s.yT()), (0.0, 2.45), (1.6, 2.45), (2.5, 2.1)], CYAN, lambda: rflow(s.E.get_value() * 4),
           pipe=[(0.0, 2.45), (1.6, 2.45)], rmax=0.1, seed=4)
    s.valveM = valve(-3.1, 3.25, ORANGE)
    s.valveG = valve(1.5, 3.25, YELLOW)
    return s


def valve(x, y, color):
    c = Circle(radius=0.2, color=color, stroke_width=5).set_fill(BG_DARK, 1).move_to(P(x, y))
    h = Line(P(x - 0.22, y + 0.3), P(x + 0.22, y + 0.3), color=color, stroke_width=6)
    st = Line(P(x, y + 0.2), P(x, y + 0.3), color=color, stroke_width=6)
    return VGroup(c, h, st)


BG_DARK = "#0f1117"


def add_world(sc, s, fur=None, flows=("M", "G", "D", "E")):
    sc.add(s.base())
    for n in flows:
        sc.add(s.flows[n])


def sun(x, y, r=0.35):
    core = Circle(radius=r, color=YELLOW, stroke_width=3).set_fill(YELLOW, 0.9)
    rays = VGroup(*[Line(P(0, 0) + r * 1.25 * np.array([np.cos(a), np.sin(a), 0]), P(0, 0) + r * 1.75 * np.array([np.cos(a), np.sin(a), 0]),
                         color=YELLOW, stroke_width=5) for a in np.linspace(0, 2 * PI, 9)[:-1]])
    g = VGroup(core, rays).move_to(P(x, y))
    g.add_updater(lambda m, dt: rays.rotate(dt * 0.5, about_point=core.get_center()))
    return g


def rock(x, y, w=1.4, h=0.55, warm=False):
    r = Ellipse(width=w, height=h, color="#8A6F55" if warm else "#6B6458", stroke_width=3).set_fill("#8A6F55" if warm else "#6B6458", 0.95)
    return r.move_to(P(x, y))


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


def iguana(x, y, s=1.0):
    col = "#7FA05A"
    body = Ellipse(width=2.6 * s, height=0.85 * s, stroke_width=0).set_fill(col, 1)
    head = Ellipse(width=1.0 * s, height=0.6 * s, stroke_width=0).set_fill(col, 1).shift(RIGHT * 1.45 * s + UP * 0.1 * s)
    tail = Polygon(P(-1.1 * s, 0.25 * s), P(-1.1 * s, -0.25 * s), P(-3.0 * s, -0.55 * s), stroke_width=0).set_fill(col, 1)
    spikes = VGroup(*[Triangle(stroke_width=0).set_fill("#5E7C41", 1).scale(0.12 * s).shift(RIGHT * (i * 0.4 * s) + UP * 0.45 * s) for i in range(-2, 3)])
    legs = VGroup(*[Line(P(dx * s, -0.3 * s), P((dx + 0.2) * s, -0.7 * s), color=col, stroke_width=7) for dx in (-0.7, 0.8)])
    eye = Dot(radius=0.05 * s, color="#222222").shift(RIGHT * 1.6 * s + UP * 0.22 * s)
    g = VGroup(legs, tail, body, spikes, head, eye)
    return g.move_to(P(x, y))


def flame(x, y, size=1.0):
    ts = np.linspace(0, 2 * PI, 40)
    pts = [P(0.45 * np.sin(t) * np.sin(t / 2), -0.7 * np.cos(t)) for t in ts]
    outer = VMobject().set_points_smoothly(pts + [pts[0]]).set_stroke(width=0).set_fill(ORANGE, 0.95)
    inner = outer.copy().scale(0.55).shift(DOWN * 0.15).set_fill(YELLOW, 0.95)
    g = VGroup(outer, inner).scale(size).move_to(P(x, y))
    g.base_size, g.t = size, 0.0
    cy = g.get_bottom()[1]

    def fl(m, dt):
        m.t += dt
        m.stretch_to_fit_height(m.base_size * 1.4 * (1 + 0.08 * np.sin(7 * m.t)), about_edge=DOWN)
    g.add_updater(fl)
    return g


class Sc(SpokenScene):
    def until(self, t):
        rest = t - self.elapsed()
        if rest > 0.02:
            self.wait(rest)

    def rt(self, f):
        return min(max(0.4, self.beat(f)), 1.2)


def desert(sc, full=True):
    """The s01 picture. Returns its parts; with full=True everything is added at once."""
    ground = Line(P(-6.8, -2.25), P(6.8, -2.25), color="#6B5A47", stroke_width=6)
    rk = rock(-3.3, -1.75, 4.6, 0.8, warm=True)
    sn = sun(-5.4, 2.7, 0.4)
    ig = iguana(-3.2, -0.85, 1.0)
    shade = RoundedRectangle(corner_radius=0.3, width=4.6, height=3.1, stroke_width=0).set_fill("#1B1F2A", 1).move_to(P(3.6, -0.7))
    mo = mouse(3.6, -1.35, 1.0)
    lair = T("air 30 °C", 32, GREY).move_to(P(0, 2.7))
    lig = T("iguana 40 °C", 32, RED).move_to(P(-3.2, 1.2))
    lmo = T("mouse 37 °C", 32, RED).move_to(P(3.6, 1.2))
    tag = T("illustrative numbers", 24, GREY).move_to(P(0, 2.1))
    fi = flame(-3.2, 0.2, 0.45)
    fm = flame(3.6, 0.0, 0.9)
    q = T("?", 150, YELLOW, weight=BOLD).move_to(P(0, -0.1))
    card = T("Warmer than the air: how?", 40, TEXT, font=TITLE_FONT).move_to(P(0, -3.15))
    d = dict(ground=ground, rock=rk, sun=sn, ig=ig, shade=shade, mo=mo, lair=lair, lig=lig, lmo=lmo, tag=tag, fi=fi, fm=fm, q=q, card=card)
    if full:
        sc.add(*d.values())
    return d


class S00Title(TitleCard):
    LESSON = "Heat Balance and Body Temperature"
    TITLE = "Where the Balance Sits"


class S01Question(Sc):
    def construct(self):
        d = desert(self, full=False)
        self.add(d["ground"])
        self.play(FadeIn(d["rock"]), FadeIn(d["sun"]), run_time=1.2)
        self.at("a basking iguana")
        self.play(FadeIn(d["ig"], shift=DOWN * 0.3), run_time=1.0)
        self.at("warmer than the air")
        self.play(FadeIn(d["lair"]), FadeIn(d["lig"]), FadeIn(d["tag"]), run_time=0.9)
        self.at("So is a mouse")
        self.play(FadeIn(d["shade"]), FadeIn(d["mo"], shift=DOWN * 0.3), run_time=1.0)
        self.at("nearby")
        self.play(FadeIn(d["lmo"]), run_time=0.8)
        self.at("makes far less heat")
        self.play(FadeIn(d["fi"], scale=0.5), run_time=0.8)
        self.at("than the mouse")
        self.play(FadeIn(d["fm"], scale=0.5), run_time=0.8)
        self.at("How can both")
        self.play(FadeIn(d["q"], scale=0.4), FadeIn(d["card"]), run_time=1.0)
        self.finish()


class S02Tank(Sc):
    def construct(self):
        d = desert(self, full=True)
        s = worldA(Tb=20.0, M=0.0, G=0.0, C=0.0, E=0.0, k=0.9)
        s.vis["fill"].set_value(0)
        s.vis["thermo"].set_value(0)
        for n in ("M", "G", "D", "E"):
            s.fv[n].set_value(0)
        self.add(s.clock)
        others = [m for k, m in d.items() if k != "mo"]
        self.play(*[FadeOut(m) for m in others], FadeTransform(d["mo"], s.walls), run_time=1.8)
        self.add(s.fill, s.mercury, s.thermo)
        self.at("The level in the tank")
        self.play(s.vis["fill"].animate.set_value(1), s.vis["thermo"].animate.set_value(1), run_time=1.2)
        lab = T("body temperature", 30, RED).move_to(P(-3.25, -3.3))
        self.play(FadeIn(lab), run_time=0.6)
        self.at("Heat flows in")
        self.add(s.flows["M"], s.flows["G"], s.valveM, s.valveG)
        self.play(s.fv["M"].animate.set_value(1), s.fv["G"].animate.set_value(1),
                  s.M.animate.set_value(5.5), s.G.animate.set_value(1.5), FadeIn(s.valveM), FadeIn(s.valveG), run_time=1.0)
        self.at("heat leaks out")
        self.add(s.flows["D"])
        self.play(s.fv["D"].animate.set_value(1), s.C.animate.set_value(1.0), run_time=1.0)
        self.at("settles where")
        self.wait(1.2)
        st = VGroup(T("steady: in = out", 30, TEXT), T("(schematic)", 26, GREY)).arrange(DOWN, buff=0.12).move_to(P(4.3, 0.0))
        self.at("match")
        self.play(FadeIn(st), run_time=0.8)
        self.finish()


class S03Inflows(Sc):
    def construct(self):
        s = worldA(Tb=37.0, M=5.5, G=1.5, C=1.0, E=0.0)
        add_world(self, s, flows=("M", "G", "D"))
        self.add(s.valveM, s.valveG)
        sn = sun(3.55, 3.25)
        self.add(sn)
        self.at("Two taps fill")
        self.play(Indicate(s.valveM, color=ORANGE), Indicate(s.valveG, color=YELLOW), run_time=1.2)
        lm = VGroup(T("M, heat made", 30, ORANGE), T("(metabolism)", 28, ORANGE)).arrange(DOWN, buff=0.1).move_to(P(-5.2, 2.45))
        self.at("The orange tap")
        self.play(FadeIn(lm), s.M.animate.set_value(6.5), Indicate(s.valveM, color=ORANGE), run_time=1.5)
        lg = VGroup(T("G, heat gained", 30, YELLOW), T("(sun, rock)", 28, YELLOW)).arrange(DOWN, buff=0.1).move_to(P(4.7, 2.0))
        self.at("The yellow tap")
        self.play(FadeIn(lg), s.G.animate.set_value(2.5), Indicate(s.valveG, color=YELLOW), run_time=1.5)
        rk = rock(5.6, 3.1, 1.2, 0.5, warm=True)
        ar = Arrow(P(5.0, 3.1), P(4.1, 3.2), buff=0, color=YELLOW, stroke_width=6)
        self.at("sunlight")
        self.play(Indicate(sn, color=YELLOW), run_time=0.8)
        self.at("warm rock")
        self.play(FadeIn(rk, shift=LEFT * 0.2), GrowArrow(ar), run_time=1.0)
        self.finish()


class S04Leak(Sc):
    def construct(self):
        s = worldA(Tb=39.0, M=6.5, G=2.5, C=1.0, E=0.0)
        add_world(self, s, flows=("M", "G", "D"))
        self.add(s.valveM, s.valveG, sun(3.55, 3.25))
        s.vis["air"].set_value(0)
        s.vis["gap"].set_value(0)
        self.add(s.air())
        lc = VGroup(T("dry leak", 30, BLUE)).move_to(P(4.4, -3.2))
        self.at("The blue outlet")
        self.play(Indicate(s.flows["D"], color=BLUE), FadeIn(lc), run_time=1.0)
        lc2 = VGroup(T("C, conductance", 30, BLUE), T("= width of the dry leak", 28, BLUE)).arrange(DOWN, buff=0.08).move_to(P(4.6, -3.05))
        self.at("Its width is conductance")
        self.play(FadeOut(lc), FadeIn(lc2), run_time=0.8)
        self.at("how readily heat escapes")
        self.play(s.C.animate.set_value(1.7), run_time=1.3)
        self.wait(0.6)
        self.play(s.C.animate.set_value(0.6), run_time=1.3)
        self.wait(0.4)
        self.play(s.C.animate.set_value(1.0), run_time=1.0)
        eq = M("dry leak = C × (Tb − Ta)", 28, TEXT, t2c={"C": BLUE, "Tb": RED, "Ta": GREY}).move_to(P(3.9, 0.9))
        fit(eq, max_w=5.6)
        eq.move_to(P(3.9, 0.9))
        self.at("The flow also grows")
        self.play(FadeIn(eq), s.vis["air"].animate.set_value(1), s.vis["gap"].animate.set_value(1), run_time=1.2)
        note = VGroup(T("Ta: effective dry surroundings", 24, GREY), T("each heat load counted once (simple model)", 24, GREY)).arrange(DOWN, buff=0.08, aligned_edge=LEFT)
        fit(note, max_w=5.7)
        note.move_to(P(3.85, -1.6))
        self.at("gap between body and air")
        self.play(s.Ta.animate.set_value(22.0), FadeIn(note), run_time=1.3)
        self.play(s.Ta.animate.set_value(30.0), run_time=0.8)
        self.finish()


def mouse_scene(sc, s):
    """Mouse on cool ground, right of the tank (s05)."""
    ground = Rectangle(width=4.8, height=0.95, stroke_width=0).set_fill("#2A2E3A", 1).move_to(P(4.4, -1.48))
    m = mouse(4.8, -0.35, 0.95)
    return ground, m


class S05Routes(Sc):
    def construct(self):
        s = worldA(Tb=39.0, M=6.5, G=2.5, C=1.0, E=0.0)
        add_world(self, s, flows=("M", "G", "D"))
        self.add(s.valveM, s.valveG, sun(3.55, 3.25), s.air())
        ground, mo = mouse_scene(self, s)
        self.at("Three routes")
        self.play(FadeIn(ground), FadeIn(mo, shift=DOWN * 0.2), run_time=1.2)
        rad = Arrow(P(4.3, 0.45), P(4.3, 1.6), buff=0, color=BLUE, stroke_width=7)
        lr = T("radiation", 30, BLUE).move_to(P(5.65, 1.15))
        self.at("Radiation")
        self.play(GrowArrow(rad), FadeIn(lr), run_time=0.9)
        con = Arrow(P(4.3, -1.0), P(4.3, -1.8), buff=0, color=BLUE, stroke_width=7)
        lc = T("conduction", 30, BLUE).move_to(P(5.65, -1.45))
        self.at("conduction")
        self.play(GrowArrow(con), FadeIn(lc), run_time=0.9)
        wave = VGroup(*[FunctionGraph(lambda x, y0=y0: y0 + 0.07 * np.sin(8 * (x - 1.6)), x_range=[1.6, 3.0], color=BLUE, stroke_width=5) for y0 in (-0.1, 0.2)])
        wtip = VGroup(*[Triangle(color=BLUE, stroke_width=0).set_fill(BLUE, 1).scale(0.11).rotate(-PI / 2).move_to(P(3.1, y0)) for y0 in (-0.1, 0.2)])
        cv = VGroup(wave, wtip)
        lv = T("convection", 30, BLUE).move_to(P(2.5, 0.8))
        self.at("convection")
        self.play(Create(wave), FadeIn(wtip), FadeIn(lv), run_time=1.0)
        self.at("Each can run in or out")
        for a in (rad, con, cv):
            self.play(Rotate(a, PI), run_time=0.7)
        self.wait(0.2)
        net = T("net dry exchange", 30, BLUE).move_to(P(4.6, -3.2))
        self.at("so the leak is their net")
        self.play(FadeIn(net), Indicate(s.flows["D"], color=BLUE), run_time=1.0)
        rk = rock(5.7, 3.1, 1.2, 0.5, warm=True)
        ar = Arrow(P(5.0, 3.1), P(4.1, 3.2), buff=0, color=YELLOW, stroke_width=6)
        lg = T("counted once, in G", 30, YELLOW).move_to(P(5.0, 2.35))
        self.at("Sunlight and a warm rock")
        self.play(FadeIn(rk), GrowArrow(ar), run_time=1.0)
        self.at("in the yellow tap")
        self.play(FadeIn(lg), Indicate(s.valveG, color=YELLOW), run_time=0.9)
        self.finish()


class S06Evap(Sc):
    def construct(self):
        s = worldA(Tb=39.0, M=6.5, G=2.5, C=1.0, E=0.0)
        s.fv["E"].set_value(0)
        add_world(self, s)
        self.add(s.valveM, s.valveG, sun(3.55, 3.25), s.air())
        self.at("A fourth outlet")
        self.play(s.E.animate.set_value(1.2), s.fv["E"].animate.set_value(1), run_time=1.5)
        le = T("E, evaporation", 30, CYAN).move_to(P(4.3, 1.75))
        self.at("evaporation")
        self.play(FadeIn(le), run_time=0.7)
        dr = Ellipse(width=0.35, height=0.5, color=CYAN, stroke_width=3).set_fill(CYAN, 0.7).move_to(P(2.3, -0.55))
        skin = Line(P(1.6, -0.9), P(3.2, -0.9), color="#B58B7A", stroke_width=8)
        vap = Flow(lambda: [(2.3, -0.4), (2.5, 0.2), (2.7, 0.7)], lambda: 0.6, CYAN, n=6, rmax=0.09, seed=7)
        self.at("Water turning to vapor")
        self.play(FadeIn(skin), FadeIn(dr), run_time=0.8)
        self.add(vap)
        self.play(dr.animate.scale(0.4), run_time=2.0)
        head = Circle(radius=0.65, stroke_width=0).set_fill("#C9A27E", 1).move_to(P(5.3, 0.4))
        snout = Ellipse(width=0.9, height=0.5, stroke_width=0).set_fill("#B48B62", 1).move_to(P(4.85, 0.2))
        ear = Ellipse(width=0.35, height=0.7, stroke_width=0).set_fill("#7A5A3A", 1).move_to(P(5.65, 0.8))
        tongue = Ellipse(width=0.2, height=0.45, stroke_width=0).set_fill("#E58A9A", 1).move_to(P(4.9, -0.12))
        eye = Dot(radius=0.06, color="#222222").move_to(P(5.1, 0.55))
        dog = VGroup(head, snout, ear, tongue, eye)
        pant = Flow(lambda: [(4.55, 0.0), (4.0, 0.5), (3.4, 1.1)], lambda: 0.7, CYAN, n=6, rmax=0.09, seed=8)
        self.at("panting")
        self.play(FadeIn(dog), run_time=0.8)
        self.add(pant)
        self.at("In practice")
        oa = Arrow(P(0.35, 2.45), P(1.6, 2.45), buff=0, color=CYAN, stroke_width=8)
        self.play(GrowArrow(oa), run_time=0.8)
        bar = RoundedRectangle(corner_radius=0.1, width=0.5, height=1.3, color=CYAN, stroke_width=4).move_to(P(3.3, -2.5))
        lvl_bar = VMobject().set_stroke(width=0)
        self.drain_t = 0.0

        def bar_up(m, dt):
            self.drain_t += dt
            f = max(0.05, 1 - 0.1 * self.drain_t)
            y0 = -3.15
            m.set_points_as_corners([P(3.1, y0), P(3.5, y0), P(3.5, y0 + 1.3 * f), P(3.1, y0 + 1.3 * f), P(3.1, y0)])
            m.set_fill(CYAN, 0.8)
        lvl_bar.add_updater(bar_up)
        lw = T("water spent", 30, CYAN).move_to(P(5.1, -2.5))
        self.at("and it costs water")
        self.play(FadeIn(bar), FadeIn(lw), run_time=0.8)
        self.add(lvl_bar)
        self.finish()


class Beam:
    def __init__(self, px=3.4, py=1.5, half=1.6, hang=2.1):
        self.px, self.py, self.half, self.hang = px, py, half, hang
        self.ang = ValueTracker(-0.22)
        self.beam = Line(P(0, 0), P(1, 0), color=TEXT, stroke_width=8)
        self.piv = Triangle(color=TEXT, stroke_width=4).set_fill(TEXT, 1).scale(0.25).move_to(P(px, py - 0.25))
        self.lp = VGroup(chip("M", ORANGE, 30), chip("G", YELLOW, 30)).arrange(DOWN, buff=0.1)
        self.rp = VGroup(chip("C (Tb − Ta)", BLUE, 28), chip("E", CYAN, 30)).arrange(DOWN, buff=0.1)
        self.ll = VGroup(*[Line(P(0, 0), P(0.1, 0)) for _ in range(4)])
        self.rl = VGroup(*[Line(P(0, 0), P(0.1, 0)) for _ in range(4)])
        for l in (*self.ll, *self.rl):
            l.set_stroke(GREY, 3)
        self.clock = Mobject()
        self.clock.add_updater(self._upd)
        self.all = Group(self.clock, self.beam, self.piv, self.ll, self.rl, self.lp, self.rp)

    def _upd(self, m):
        a = self.ang.get_value()
        c, s_ = np.cos(a), np.sin(a)
        lft = P(self.px - self.half * c, self.py - self.half * s_)
        rgt = P(self.px + self.half * c, self.py + self.half * s_)
        self.beam.put_start_and_end_on(lft, rgt)
        for e, pan, lines in ((lft, self.lp, self.ll), (rgt, self.rp, self.rl)):
            pan.move_to(e + DOWN * (self.hang - pan.height / 2 - 0.08))
            hw = pan.width / 2 + 0.1
            lines[0].put_start_and_end_on(e + LEFT * hw, e + RIGHT * hw)
            lines[1].put_start_and_end_on(e + LEFT * hw, e + LEFT * hw + DOWN * self.hang)
            lines[2].put_start_and_end_on(e + RIGHT * hw, e + RIGHT * hw + DOWN * self.hang)
            lines[3].put_start_and_end_on(e + LEFT * hw + DOWN * self.hang, e + RIGHT * hw + DOWN * self.hang)


class S07Rule(Sc):
    def construct(self):
        s = worldA(Tb=37.8, M=6.5, G=2.5, C=1.0, E=1.2)
        add_world(self, s)
        self.add(s.valveM, s.valveG, sun(3.55, 3.25), s.air())
        b = Beam()
        b.ang.set_value(-0.25)
        self.at("So the level sits")
        self.play(FadeIn(b.all), run_time=1.2)
        e1 = M("M + G = C × (Tb − Ta) + E", 28, TEXT, t2c={"M": ORANGE, "G": YELLOW, "C": BLUE, "E": CYAN, "Tb": RED, "Ta": GREY})
        fit(e1, max_w=5.9)
        e1.move_to(P(3.8, -1.9))
        e2 = M("Tb − Ta = (M + G − E) ÷ C", 28, TEXT, t2c={"M": ORANGE, "G": YELLOW, "C": BLUE, "E": CYAN, "Tb": RED, "Ta": GREY})
        fit(e2, max_w=5.9)
        e2.move_to(P(3.8, -1.9))
        self.at("heat in equals heat out")
        self.play(b.ang.animate.set_value(0.0).set_rate_func(lambda t: 1 - np.exp(-5 * t) * np.cos(9 * t) if t < 1 else 1), FadeIn(e1), run_time=2.4)
        self.at("Body temperature rises")
        self.play(FadeTransform(e1, e2), Indicate(s.gapbar, color=YELLOW, scale_factor=1.3), run_time=1.6)
        self.at("minus evaporation")
        self.play(Indicate(s.flows["E"], color=CYAN), run_time=1.0)
        self.at("divided by conductance")
        self.play(Indicate(s.flows["D"], color=BLUE), run_time=1.2)
        self.finish()


def split(Tb_l=40.0, Tb_r=37.0, left=True, right=True, kl=0.6):
    """Two tanks side by side: iguana (left) and mouse (right)."""
    g = dict(w=2.4, h=3.6, bot=-1.9)
    sl = Sim(cx=-3.7, Tb=Tb_l, Ta=30.0, M=2.0, G=19.0, C=2.0, E=1.0, k=kl, thermo_dx=0.7, **g)
    sr = Sim(cx=3.7, Tb=Tb_r, Ta=30.0, M=7.8, G=0.2, C=1.0, E=1.0, k=kl, thermo_dx=-0.7, **g)
    sl.gx, sr.gx = sl.R - 0.4, sr.R - 0.4
    # left: orange from left, yellow from sun above and rock below, leak out the left wall
    sl.flow("M", lambda: [(-6.6, 0.4), (-4.9, 0.4)], ORANGE, lambda: rflow(sl.M.get_value()), pipe=[(-6.6, 0.4), (-4.9, 0.4)], seed=1)
    sl.flow("G", lambda: [(-3.7, 2.85), (-3.7, sl.yT() + 0.05)], YELLOW, lambda: rflow(sl.G.get_value() / 2), pipe=[(-3.7, 2.85), (-3.7, 1.9)], seed=2, rmax=0.1)
    sl.flow("G2", lambda: [(-3.7, -2.7), (-3.7, -1.85)], YELLOW, lambda: rflow(sl.G.get_value() / 2), seed=5, rmax=0.1)
    dl = [(-4.9, -1.4), (-6.4, -1.4)]
    sl.flow("D", lambda: dl, BLUE, lambda: rflow(sl.leak()), pipe=dl, pipe_w=lambda: 20 * sl.C.get_value(), seed=3)
    sr.flow("M", lambda: [(6.6, 0.4), (4.9, 0.4)], ORANGE, lambda: rflow(sr.M.get_value()), pipe=[(6.6, 0.4), (4.9, 0.4)], seed=1)
    sr.flow("G", lambda: [(3.7, 2.85), (3.7, sr.yT() + 0.05)], YELLOW, lambda: rflow(sr.G.get_value()), pipe=[(3.7, 2.85), (3.7, 1.9)], seed=2)
    dr = [(4.9, -1.4), (6.4, -1.4)]
    sr.flow("D", lambda: dr, BLUE, lambda: rflow(sr.leak()), pipe=dr, pipe_w=lambda: 20 * sr.C.get_value(), seed=3)
    sl.flows["G2"].vis = sl.fv["G"]
    sl.air_lab.add_updater(lambda m: m.move_to(P(-5.55, sl.yA() + 0.0)))
    sr.air_lab.add_updater(lambda m: m.move_to(P(5.55, sr.yA() + 0.0)))
    return sl, sr


def add_split(sc, sl, sr, dim_r=False):
    for s in (sl, sr):
        sc.add(s.base(), s.air())
        for f in s.flows.values():
            sc.add(f)


class S08Iguana(Sc):
    def construct(self):
        sl, sr = split(Tb_l=30.0, Tb_r=30.0)
        sr.integrate = False
        sl.G.set_value(0.0)
        sl.integrate = True
        for n in ("M", "G", "D"):
            sr.fv[n].set_value(0)
        add_split(self, sl, sr)
        sn = sun(-3.7, 3.3)
        rk = rock(-3.7, -2.45, 2.6, 0.6, warm=True)
        dim = Rectangle(width=7.0, height=8.0, stroke_width=0).set_fill(BG_DARK, 0.65).move_to(P(3.5, 0))
        self.add(dim)
        lbl = VGroup(T("40 °C", 32, RED), T("(illustrative)", 26, RED)).arrange(DOWN, buff=0.05).move_to(P(-1.8, 2.5))
        sl.fv["M"].set_value(0)
        self.at("orange tap runs small")
        self.play(sl.fv["M"].animate.set_value(1), run_time=1.0)
        self.at("yellow tap pours")
        self.play(FadeIn(sn), sl.G.animate.set_value(19.0), run_time=1.6)
        self.at("and the rock below")
        self.play(FadeIn(rk), run_time=0.8)
        self.at("lifts it well above")
        self.play(FadeIn(lbl), run_time=0.8)
        self.finish()


def fur_ring(s, tracker, skip):
    s.air_off = 0.65  # keep the 'air' label clear of the fur ticks
    L, R, B, top = s.L, s.R, s.bot, s.top
    pts = []
    perim = [(L, y) for y in np.linspace(B + 0.2, top - 0.2, 12)] + [(R, y) for y in np.linspace(B + 0.2, top - 0.2, 12)] \
        + [(x, B) for x in np.linspace(L + 0.2, R - 0.2, 8)]
    lines = VGroup()
    for (x, y) in perim:
        if skip(x, y):
            continue
        nx = -1 if x == L else (1 if x == R else 0)
        ny = -1 if (y == B and x not in (L, R)) else 0
        l = Line(P(x, y), P(x + nx * 0.2, y + ny * 0.2), color=FUR, stroke_width=6)
        l.nv = (nx, ny)
        l.k = 0.75 + 0.5 * ((hash((round(x, 2), round(y, 2))) % 7) / 7.0)
        l.tw = 0.12 * (((hash((round(y, 2), round(x, 2))) % 5) - 2) / 2.0)
        l.p0 = (x, y)
        lines.add(l)

    def upd(m):
        ln = tracker.get_value()
        for l in m:
            x, y = l.p0
            l.put_start_and_end_on(P(x, y), P(x + (l.nv[0] + l.tw * l.nv[1]) * ln * l.k, y + (l.nv[1] + l.tw * l.nv[0]) * ln * l.k))
    lines.add_updater(upd)
    return lines


class S09Mouse(Sc):
    def construct(self):
        sl, sr = split(Tb_l=40.0, Tb_r=30.0)
        sl.integrate = False
        sr.C.set_value(2.0)
        sr.k = 0.6
        sr.fv["M"].set_value(0)
        add_split(self, sl, sr)
        sn = sun(-3.7, 3.3)
        rk = rock(-3.7, -2.45, 2.6, 0.6, warm=True)
        sn2 = sun(3.7, 3.3, 0.25)
        dim = Rectangle(width=7.0, height=8.0, stroke_width=0).set_fill(BG_DARK, 0.65).move_to(P(-3.5, 0))
        l1 = VGroup(T("40 °C", 32, RED), T("(illustrative)", 26, RED)).arrange(DOWN, buff=0.05).move_to(P(-1.8, 2.5))
        l2 = VGroup(T("37 °C", 32, RED), T("(illustrative)", 26, RED)).arrange(DOWN, buff=0.05).move_to(P(1.8, 2.5))
        self.add(sn, rk, l1, sn2)
        self.add(dim)
        self.at("The mouse has almost no yellow tap")
        self.play(dim.animate.set_opacity(0.65), run_time=0.1)
        self.wait(0.5)
        self.at("Its orange tap runs strong")
        self.play(sr.fv["M"].animate.set_value(1), run_time=1.0)
        furt = ValueTracker(0.3)
        fur = fur_ring(sr, furt, lambda x, y: False)
        self.at("fur keeps")
        self.play(FadeIn(fur), sr.C.animate.set_value(1.0), run_time=1.6)
        self.at("Its own metabolism")
        self.play(FadeIn(l2), run_time=0.8)
        self.finish()


class S10Names(Sc):
    def construct(self):
        sl, sr = split(Tb_l=40.0, Tb_r=37.0)
        sl.integrate = False
        sr.integrate = False
        add_split(self, sl, sr)
        furt = ValueTracker(0.3)
        self.add(fur_ring(sr, furt, lambda x, y: False))
        self.add(sun(-3.7, 3.3), rock(-3.7, -2.45, 2.6, 0.6, warm=True), sun(3.7, 3.3, 0.25))
        l1 = VGroup(T("40 °C", 32, RED), T("(illustrative)", 26, RED)).arrange(DOWN, buff=0.05).move_to(P(-1.8, 2.5))
        l2 = VGroup(T("37 °C", 32, RED), T("(illustrative)", 26, RED)).arrange(DOWN, buff=0.05).move_to(P(1.8, 2.5))
        self.add(l1, l2)
        a = VGroup(T("ectotherm", 36, YELLOW, weight=BOLD), T("mostly G (outside heat)", 30, YELLOW)).arrange(DOWN, buff=0.08).move_to(P(-3.7, -3.25))
        b = VGroup(T("endotherm", 36, ORANGE, weight=BOLD), T("mostly M (own metabolism)", 30, ORANGE)).arrange(DOWN, buff=0.08).move_to(P(3.7, -3.25))
        self.at("ectotherm")
        self.play(FadeIn(a, shift=UP * 0.2), run_time=1.0)
        self.at("endotherm")
        self.play(FadeIn(b, shift=UP * 0.2), run_time=1.0)
        tag = VGroup(T("cold-blooded", 30, GREY), T("= cold?", 30, GREY)).arrange(DOWN, buff=0.1).move_to(P(0, 0.3))
        strike = Line(tag.get_left() + LEFT * 0.1, tag.get_right() + RIGHT * 0.1, color=RED, stroke_width=7).move_to(tag)
        self.at("not how warm")
        self.play(FadeIn(tag), run_time=0.6)
        self.play(Create(strike), run_time=0.6)
        self.play(FadeOut(tag), FadeOut(strike), run_time=0.8)
        self.finish()


def mouse_world(Ta=30.0, Tb=37.0, M=7.8, G=0.2, E=1.0, C=1.0, k=0.8, integrate=True):
    s = worldA(Tb=Tb, Ta=Ta, M=M, G=G, C=C, E=E, k=k, integrate=integrate)
    return s


def fur_A(s, furt):
    return fur_ring(s, furt, lambda x, y: y == s.bot and abs(x + 0.4) < 0.45)


def dial_slot(x, y, q=True):
    c = Circle(radius=0.55, color=GREY, stroke_width=5)
    t = T("?", 44, YELLOW).move_to(c) if q else Dot(radius=0.0)
    return VGroup(c, t).move_to(P(x, y))


class S11Predict(Sc):
    def construct(self):
        s = mouse_world()
        add_world(self, s)
        self.add(s.valveM, s.valveG, sun(3.55, 3.25), s.air())
        furt = ValueTracker(0.28)
        self.add(fur_A(s, furt))
        self.at("Now move the mouse")
        self.play(s.Ta.animate.set_value(15.0), run_time=3.0)
        self.at("The gap widens")
        self.play(Indicate(s.gapbar, color=YELLOW, scale_factor=1.3), run_time=1.0)
        self.at("heat leaks faster")
        self.play(Indicate(s.flows["D"], color=BLUE), run_time=1.0)
        d1, d2 = dial_slot(2.6, -0.3), dial_slot(5.3, -0.3)
        card = T("Two ways to hold the level?", 34, TEXT, font=TITLE_FONT)
        fit(card, max_w=5.6)
        card.move_to(P(3.7, 1.0))
        self.at("Name two ways")
        self.play(FadeIn(d1), FadeIn(d2), FadeIn(card), run_time=1.2)
        self.finish()


class S12Pause(NarratedScene):
    def construct(self):
        s = mouse_world(Ta=15.0, Tb=22.0)
        add_world(self, s)
        self.add(s.valveM, s.valveG, sun(3.55, 3.25), s.air())
        furt = ValueTracker(0.28)
        self.add(fur_A(s, furt))
        d1, d2 = dial_slot(2.6, -0.3), dial_slot(5.3, -0.3)
        card = T("Two ways to hold the level?", 34, TEXT, font=TITLE_FONT)
        fit(card, max_w=5.6)
        card.move_to(P(3.7, 1.0))
        self.add(d1, d2, card)
        ring = Circle(radius=0.4, color=GOLD, stroke_width=7).move_to(P(4.0, -1.7))
        base = Circle(radius=0.4, color=GREY, stroke_width=3).move_to(P(4.0, -1.7))
        self.add(base)
        self.play(Create(ring), run_time=4.4, rate_func=linear)
        self.finish()


class S13Reveal(Sc):
    def construct(self):
        s = mouse_world(Ta=15.0, Tb=22.0, k=0.9)
        add_world(self, s)
        self.add(s.valveM, s.valveG, sun(3.55, 3.25), s.air())
        furt = ValueTracker(0.28)
        self.add(fur_A(s, furt))
        d1, d2 = dial_slot(2.6, -0.3), dial_slot(5.3, -0.3)
        self.add(d1, d2)

        def needle_dial(x, y):
            c = Circle(radius=0.55, color=GOLD, stroke_width=5)
            n = Line(P(0, 0), P(0.4, 0.0), color=GOLD, stroke_width=6)
            return VGroup(c, n).move_to(P(x, y))
        n1, n2 = needle_dial(2.6, -0.3), needle_dial(5.3, -0.3)
        t1 = VGroup(T("make more", 30, ORANGE), T("heat", 30, ORANGE)).arrange(DOWN, buff=0.05).move_to(P(2.6, -1.35))
        t2 = VGroup(T("narrow", 30, BLUE), T("the leak", 30, BLUE)).arrange(DOWN, buff=0.05).move_to(P(5.3, -1.35))
        self.at("Make more heat")
        self.play(FadeOut(d1), FadeIn(n1), FadeIn(t1), run_time=0.8)
        self.at("opening the orange tap")
        self.play(s.M.animate.set_value(12.0), Rotate(n1[1], 1.6, about_point=n1[0].get_center()), run_time=1.6)
        self.at("Or narrow the leak")
        self.play(FadeOut(d2), FadeIn(n2), FadeIn(t2), run_time=0.8)
        vess = Line(P(4.6, -2.45), P(6.2, -2.45), color=RED, stroke_width=22)
        skin = Line(P(4.6, -2.75), P(6.2, -2.75), color="#B58B7A", stroke_width=8)
        lv = T("skin blood vessel", 28, RED).move_to(P(5.4, -3.2))
        self.at("closing skin blood vessels")
        self.play(FadeIn(vess), FadeIn(skin), FadeIn(lv), Rotate(n2[1], 1.6, about_point=n2[0].get_center()), run_time=0.8)
        self.play(vess.animate.set_stroke(width=6), s.C.animate.set_value(0.5), run_time=1.6)
        self.at("fluffing the fur")
        self.play(furt.animate.set_value(0.55), run_time=1.4)
        self.at("Every dial")
        labs = [
            (T("shivering, brown fat → M", 28, ORANGE), P(-4.7, 2.6)),
            (T("basking → G", 28, YELLOW), P(4.9, 2.0)),
            (T("fur, skin blood flow → C", 28, BLUE), P(4.0, -3.4)),
            (T("sweating, panting → E", 28, CYAN), P(4.6, 1.2)),
        ]
        for i, (lb, pos) in enumerate(labs):
            fit(lb, max_w=4.4)
            lb.move_to(pos)
        self.play(FadeOut(t1), FadeOut(t2), FadeOut(vess), FadeOut(skin), FadeOut(lv), FadeOut(n1), FadeOut(n2), run_time=0.5)
        for i, (lb, pos) in enumerate(labs):
            self.play(FadeIn(lb), run_time=0.5)
            self.wait(1.0)
        self.finish()


def small_world(Tb=37.0, k=0.5, integrate=True):
    s = Sim(cx=-2.9, w=2.0, h=3.2, bot=-2.0, Tb=Tb, Ta=30.0, M=7.8, G=0.2, C=1.0, E=1.0, k=k, integrate=integrate, thermo_dx=-0.7)
    s.flow("M", lambda: [(-6.0, 2.3), (-3.5, 2.3), (-3.5, s.yT() + 0.05)], ORANGE, lambda: rflow(s.M.get_value()),
           pipe=[(-6.0, 2.3), (-3.5, 2.3), (-3.5, 1.5)], seed=1)
    dr = [(-2.5, -2.0), (-2.5, -3.0), (-0.8, -3.0)]
    s.flow("D", lambda: dr, BLUE, lambda: rflow(s.leak()), pipe=dr, pipe_w=lambda: 20 * s.C.get_value(), seed=3)
    s.flow("E", lambda: [(-2.2, s.yT()), (-2.2, 1.55), (-1.4, 1.9)], CYAN, lambda: rflow(s.E.get_value() * 4), rmax=0.1, seed=4)
    s.valveM = valve(-4.9, 2.3, ORANGE)
    return s


def body_outline():
    body = Ellipse(width=7.4, height=4.8, color=TEXT, stroke_width=5).move_to(P(-1.9, -0.4))
    head = Circle(radius=1.2, color=TEXT, stroke_width=5).move_to(P(3.0, 0.4))
    ear = Circle(radius=0.4, color=TEXT, stroke_width=5).move_to(P(3.5, 1.65))
    tail = ArcBetweenPoints(P(-5.5, -0.9), P(-6.6, 0.3), angle=1.0).set_stroke(TEXT, 5)
    return VGroup(tail, body, head, ear)


class S14Controller(Sc):
    def construct(self):
        sw = worldA(Tb=37.8, M=6.5, G=2.5, C=1.0, E=1.2)
        add_world(self, sw)
        self.add(sw.valveM, sw.valveG, sun(3.55, 3.25))
        s = small_world()
        qs = VGroup(T("?", 60, YELLOW).move_to(P(-3.1, 3.45)), T("?", 60, YELLOW).move_to(P(2.8, -3.0)))
        self.at("Who turns the taps")
        self.play(FadeIn(qs), Indicate(sw.valveM, color=ORANGE), Indicate(sw.flows["D"], color=BLUE), run_time=1.1)
        ol = body_outline()
        self.play(FadeOut(Group(*self.mobjects)), run_time=0.6)
        self.clear()
        self.add(s.base(), s.flows["M"], s.flows["D"], s.flows["E"], s.valveM)
        self.play(Create(ol), run_time=0.8)
        skin_pts = [P(-1.9 + 3.7 * np.cos(a), -0.4 + 2.4 * np.sin(a)) for a in (0.3, 0.9, 1.5, 2.3, 3.5, 4.6)]
        skin_dots = VGroup(*[Dot(p, radius=0.12, color=GOLD) for p in skin_pts])
        core_dots = VGroup(*[Dot(p, radius=0.12, color=RED) for p in (P(0.0, 0.2), P(-0.4, -1.1), P(0.6, -0.5))])
        blk = RoundedRectangle(corner_radius=0.12, width=1.3, height=0.8, color=GOLD, stroke_width=5).set_fill(GOLD, 0.2).move_to(P(3.0, 0.5))
        self.at("Sensors in the skin")
        self.play(FadeIn(skin_dots, lag_ratio=0.15), run_time=1.2)
        self.at("deep in the body")
        self.play(FadeIn(core_dots, lag_ratio=0.15), run_time=1.0)
        self.at("report to a controller")
        lines = VGroup(*[Line(d.get_center(), blk.get_left() if d.get_x() < 2.0 else blk.get_bottom(), color=GREY, stroke_width=2.5) for d in list(skin_dots) + list(core_dots)])
        self.play(Create(lines), FadeIn(blk), run_time=1.5)
        lab = VGroup(T("preoptic area (hypothalamus)", 28, GOLD), T("controller", 28, GOLD)).arrange(DOWN, buff=0.1)
        fit(lab, max_w=6.2)
        lab.move_to(P(3.6, 3.1))
        self.at("In mammals")
        self.play(FadeIn(lab), run_time=1.0)
        dial = VGroup(Circle(radius=0.5, color=GOLD, stroke_width=5), Line(P(0, 0), P(0.35, 0.2), color=GOLD, stroke_width=6)).move_to(P(5.4, 0.2))
        dl = VGroup(T("target", 28, GOLD), T("temperature", 28, GOLD)).arrange(DOWN, buff=0.05).move_to(P(5.4, -1.0))
        self.at("It chooses")
        self.play(FadeIn(dial), FadeIn(dl), run_time=1.0)
        self.play(Rotate(dial[1], -0.6, about_point=dial[0].get_center()), run_time=0.8)
        c1 = DashedLine(blk.get_top() + LEFT * 0.3, P(-4.9, 2.55), color=GOLD, stroke_width=4)
        c2 = DashedLine(blk.get_bottom() + LEFT * 0.3, P(-1.6, -2.9), color=GOLD, stroke_width=4)
        self.at("target temperature")
        self.play(Create(c1), Create(c2), run_time=1.2)
        self.finish()


class S15Skin(Sc):
    def construct(self):
        s = small_world(integrate=False)
        self.add(s.base(), s.flows["M"], s.flows["D"], s.flows["E"], s.valveM)
        ol = body_outline()
        skin_pts = [P(-1.9 + 3.7 * np.cos(a), -0.4 + 2.4 * np.sin(a)) for a in (0.3, 0.9, 1.5, 2.3, 3.5, 4.6)]
        skin_dots = VGroup(*[Dot(p, radius=0.12, color=GOLD) for p in skin_pts])
        core_dots = VGroup(*[Dot(p, radius=0.12, color=RED) for p in (P(0.0, 0.2), P(-0.4, -1.1), P(0.6, -0.5))])
        blk = RoundedRectangle(corner_radius=0.12, width=1.3, height=0.8, color=GOLD, stroke_width=5).set_fill(GOLD, 0.2).move_to(P(3.0, 0.5))
        lines = VGroup(*[Line(d.get_center(), blk.get_left() if d.get_x() < 2.0 else blk.get_bottom(), color=GREY, stroke_width=2.5) for d in list(skin_dots) + list(core_dots)])
        c1 = DashedLine(blk.get_top() + LEFT * 0.3, P(-4.9, 2.55), color=GOLD, stroke_width=4)
        c2 = DashedLine(blk.get_bottom() + LEFT * 0.3, P(-1.6, -2.9), color=GOLD, stroke_width=4)
        self.add(ol, lines, skin_dots, core_dots, blk, c1, c2)
        core_lab = T("core", 28, RED).move_to(P(-4.6, -2.65))
        self.add(core_lab)
        self.at("Skin sensors give")
        self.play(Indicate(skin_dots, color=YELLOW, scale_factor=1.6), run_time=1.5)
        gust = VGroup(*[FunctionGraph(lambda x, y0=y0: y0 + 0.08 * np.sin(8 * x), x_range=[0.0, 1.8], color=GREY, stroke_width=5).rotate(-PI / 2 + 0.3).shift(P(0.8 + dx, 3.2 - 0.8)) for y0, dx in ((0, 0), (0, 0.6), (0, 1.2))])
        self.at("Cold air on the skin")
        self.play(FadeIn(gust, shift=DOWN * 0.5), run_time=0.6)
        pulses = VGroup(*[Dot(skin_dots[i].get_center(), radius=0.14, color=YELLOW) for i in (0, 1, 2)])
        self.add(pulses)
        self.play(*[p.animate.move_to(blk.get_left()) for p in pulses], skin_dots.animate.set_color(YELLOW), FadeOut(gust), run_time=0.7)
        self.remove(pulses)
        self.at("can start heat")
        self.play(s.C.animate.set_value(0.6), Indicate(c2, color=BLUE), run_time=1.5)
        note = T("skin warns first (feed-forward)", 30, GOLD)
        fit(note, max_w=6.0)
        note.move_to(P(2.8, -3.3))
        self.at("before the core")
        self.play(FadeIn(note), Indicate(s.thermo, color=RED, scale_factor=1.0), run_time=1.0)
        self.finish()


class S16End(EndCard):
    LINE = "Body temperature sits where heat in equals heat out."
