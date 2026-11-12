"""Nervous control, film 2: One Synapse or Several (Biochemistrypedia organismal biology film).

COLOUR MAP (same as film 1 and the lesson)
  GOLD = the signal pulse    TEAL = receptor     BLUE = sensory neuron / nerve time
  GREY = integrating centre (cord) and interneurons    ORANGE = motor neuron
  RED = effector muscle      WHITE = a synapse (tick)   hatched GREY = junction + muscle delay
  inhibited muscles fade to pale grey
"""
import os
import random as _random
import numpy as np
from bp_style import *  # noqa: F401,F403

ORANGE = "#F29E4C"
BRIGHT_OR = "#FFC27A"
CORD_GREY = "#B8BFCC"
SKIN = "#2a2f3a"
OFFGREY = "#6c7280"


# ------------------------------------------------------------------ helpers (as film 1)
def P(x, y):
    return np.array([x, y, 0.0])


def pline(pts, color, w=8):
    m = VMobject()
    m.set_points_as_corners([np.array(p, float) for p in pts])
    m.set_stroke(color, w)
    m.set_fill(opacity=0)
    return m


def poly_pt(pts, s):
    pts = [np.array(p, float) for p in pts]
    L = [np.linalg.norm(b - a) for a, b in zip(pts, pts[1:])]
    d = max(0.0, min(1.0, s)) * sum(L)
    for a, b, l in zip(pts, pts[1:], L):
        if d <= l:
            return a + (b - a) * (d / l if l else 0)
        d -= l
    return pts[-1]


def runner(pts, color=GOLD, period=2.4, delay=0.0, r=0.15):
    dot = Dot(radius=r, color=color).move_to(pts[0])
    dot.t = delay

    def up(m, dt):
        m.t += dt
        f = (m.t % period) / period
        m.move_to(poly_pt(pts, f))
        m.set_opacity(min(1, f * 8, (1 - f) * 8))
    dot.add_updater(up)
    return dot


def ripple(c, color, r0=0.25, r1=0.8, period=1.8, delay=0.0):
    ring = Circle(radius=r0, color=color, stroke_width=4).move_to(c)
    ring.t = delay

    def up(m, dt):
        m.t += dt
        f = (m.t % period) / period
        m.become(Circle(radius=r0 + (r1 - r0) * f, color=color, stroke_width=4).move_to(c).set_stroke(opacity=1 - f))
    ring.add_updater(up)
    return ring


def breathe(mob, period=2.4, lo=0.45, hi=1.0, delay=0.0, stroke=False):
    mob.t = delay

    def up(m, dt):
        m.t += dt
        o = lo + (hi - lo) * (0.5 + 0.5 * np.sin(2 * np.pi * m.t / period))
        if stroke:
            m.set_stroke(opacity=o)
        else:
            m.set_opacity(o)
    mob.add_updater(up)
    return mob


def hatch(x0, x1, y, h=0.5, color=GREY):
    box = Rectangle(width=x1 - x0, height=h, stroke_color=color, stroke_width=2, fill_color=color, fill_opacity=0.25)
    box.move_to(P((x0 + x1) / 2, y))
    g = VGroup(box)
    lo, hi = y - h / 2, y + h / 2
    x = x0 - h
    while x < x1:
        a, b = x, x + h
        ya, yb = lo, hi
        if a < x0:
            ya = lo + (x0 - a)
            a = x0
        if b > x1:
            yb = hi - (b - x1)
            b = x1
        if yb > ya:
            g.add(Line(P(a, ya), P(b, yb), color=color, stroke_width=2.5))
        x += 0.22
    return g


def rect(x0, x1, y, h, color, op=0.85):
    return Rectangle(width=max(x1 - x0, 0.001), height=h, stroke_color=color, stroke_width=2,
                     fill_color=color, fill_opacity=op).move_to(P((x0 + x1) / 2, y))


_orig_setup = SpokenScene.setup


def _add_motes(self):
    rng = _random.Random(os.environ.get("KX_SCENE_ID", "x"))
    W_, H_ = config.frame_width, config.frame_height
    motes = VGroup()
    for _ in range(22):
        d = Dot(radius=rng.uniform(0.05, 0.11), color=rng.choice([TEAL, GREY, TEXT])).set_opacity(rng.uniform(0.18, 0.42))
        d.move_to([rng.uniform(-W_ / 2, W_ / 2), rng.uniform(-H_ / 2, H_ / 2), 0])
        d.v = (rng.uniform(-0.25, 0.25), rng.uniform(0.15, 0.4))

        def drift(m, dt, W_=W_, H_=H_):
            m.shift([m.v[0] * dt, m.v[1] * dt, 0])
            if m.get_y() > H_ / 2 + 0.1:
                m.shift(DOWN * (H_ + 0.2))
            if abs(m.get_x()) > W_ / 2 + 0.1:
                m.shift(LEFT * (W_ + 0.2) * (1 if m.get_x() > 0 else -1))
        d.add_updater(drift)
        motes.add(d)
    motes.set_z_index(-10)
    self.add(motes)


def _setup(self):
    _orig_setup(self)
    _add_motes(self)


SpokenScene.setup = _setup
NarratedScene.setup = lambda self: (Scene.setup(self), _add_motes(self) if type(self).__name__ == "S09Pause" else None)[0]


def dim(g, f):
    for m in g.family_members_with_points():
        m.set_stroke(opacity=m.get_stroke_opacity() * f)
        m.set_fill(opacity=m.get_fill_opacity() * f)
    return g


def kick_loop(d, mkey, period=2.4):
    leg, mus = d["leg"], d[mkey]
    leg.ph, leg.ang = 0.0, 0.0
    mus.ph = 0.0

    def up(m, dt):
        m.ph += dt
        a = -0.9 * max(0.0, np.sin(2 * np.pi * m.ph / period))
        m.rotate(a - m.ang, about_point=m.pivot)
        m.ang = a

    def upm(m, dt):
        m.ph += dt
        m.set_fill(RED, 0.22 + 0.6 * max(0.0, np.sin(2 * np.pi * m.ph / period)))
    leg.add_updater(up)
    mus.add_updater(upm)


def wash(m, lo=0.2, hi=0.5, period=2.0):
    m.wt = 0.0

    def up(x, dt):
        x.wt += dt
        x.set_fill(CORD_GREY, lo + (hi - lo) * (0.5 + 0.5 * np.sin(2 * np.pi * x.wt / period)))
    m.add_updater(up)
    return m


def until(scene, t):
    rest = t - scene.elapsed()
    if rest > 0.02:
        scene.wait(rest)


# ------------------------------------------------------------------ the two-panel world
CK, CT = -3.45, 3.45          # panel centres: knee jerk (left), tack withdrawal (right)
STN_COL = [TEAL, BLUE, CORD_GREY, ORANGE, RED]
TOP_X = [-5.4, -2.7, 0.0, 2.7, 5.4]
BARY = -3.3
SC = 0.095                    # x units per millisecond (both bars, same scale)
BX = {"k": -6.3, "t": 0.5}
SEGS = {"k": [(8.3, BLUE), (1.0, WHITE), (8.3, ORANGE), (1.5, None)],
        "t": [(45.0, BLUE), (3.0, WHITE), (15.0, ORANGE), (1.5, None)]}


def cx_of(k):
    return CK if k == "k" else CT


def pt(cx, x, y):
    return P(cx + x, y)


def tickm(cx, x, y):
    return Rectangle(width=0.1, height=0.38, stroke_width=0, fill_color=WHITE, fill_opacity=1).move_to(pt(cx, x, y))


def ndot(cx, x, y, color, r=0.21):
    return Dot(radius=r, color=color).move_to(pt(cx, x, y))


def cord_box(cx):
    return RoundedRectangle(corner_radius=0.3, width=2.8, height=2.4, stroke_color=CORD_GREY, stroke_width=4,
                            fill_color=CORD_GREY, fill_opacity=0.3).move_to(pt(cx, 0, 0.55))


def muscle(cx, y, h=1.2):
    return Ellipse(width=1.0, height=h + 0.2, color=RED, stroke_width=4, fill_opacity=0.35).move_to(pt(cx, 2.6, y))


def mini_leg(cx):
    top = pt(cx, 2.6, -1.75)
    shin = RoundedRectangle(corner_radius=0.15, width=0.5, height=1.1, stroke_color=GREY, stroke_width=3,
                            fill_color=SKIN, fill_opacity=1).move_to(pt(cx, 2.6, -2.25))
    foot = RoundedRectangle(corner_radius=0.08, width=0.6, height=0.2, stroke_color=GREY, stroke_width=3,
                            fill_color=SKIN, fill_opacity=1).move_to(pt(cx, 2.85, -2.78))
    g = VGroup(shin, foot)
    g.pivot = top
    return g


def label_r(text, cx, y, color=TEXT, size=28):
    t = T(text, size, color)
    t.move_to(P(cx + 3.3 - t.width / 2, y))
    return t


def knee_parts():
    cx = CK
    d = {}
    d["cord"] = cord_box(cx)
    d["rec"] = Circle(radius=0.34, stroke_color=TEAL, stroke_width=4, fill_color=TEAL, fill_opacity=0.25).move_to(pt(cx, -2.3, -0.9))
    d["sens_pts"] = [pt(cx, -2.3, -0.9), pt(cx, -1.7, 0.6), pt(cx, -0.35, 0.6)]
    d["sens"] = pline(d["sens_pts"], BLUE, 11)
    d["bulb"] = ndot(cx, -0.3, 0.6, BLUE, 0.11)
    d["tick1"] = tickm(cx, -0.04, 0.6)
    d["mdot"] = ndot(cx, 0.35, 0.6, ORANGE)
    d["mot_pts"] = [pt(cx, 0.35, 0.6), pt(cx, 1.0, 0.6), pt(cx, 1.3, 1.1), pt(cx, 2.2, 1.1)]
    d["motor"] = pline(d["mot_pts"], ORANGE, 11)
    d["quad"] = muscle(cx, 1.1)
    d["leg"] = mini_leg(cx)
    d["br_pts"] = [pt(cx, -0.9, 0.6), pt(cx, -0.7, -0.05), pt(cx, -0.45, -0.05)]
    d["branch"] = pline(d["br_pts"], BLUE, 4)
    d["IN"] = ndot(cx, -0.25, -0.05, CORD_GREY)
    d["instub"] = pline([pt(cx, -0.1, -0.05), pt(cx, 0.05, -0.05)], CORD_GREY, 4)
    d["minus"] = T("−", 34, WHITE).move_to(pt(cx, 0.17, -0.5))
    d["mdot2"] = ndot(cx, 0.4, -0.05, ORANGE)
    d["mot2_pts"] = [pt(cx, 0.4, -0.05), pt(cx, 1.0, -0.05), pt(cx, 1.3, -0.4), pt(cx, 2.2, -0.4)]
    d["motor2"] = pline(d["mot2_pts"], ORANGE, 11)
    d["ham"] = muscle(cx, -0.4, 1.0)
    return d


def tack_parts():
    cx = CT
    d = {}
    d["cord"] = cord_box(cx)
    d["rec"] = VGroup(*[Dot(radius=0.18, color=TEAL).move_to(pt(cx, -2.6 + dx, -2.0 + dy))
                        for dx, dy in [(0, 0), (0.3, 0.12), (0.12, -0.28)]]).set_opacity(0.4)
    d["sens_pts"] = [pt(cx, -2.6, -2.0), pt(cx, -2.0, -0.9), pt(cx, -1.6, 1.0), pt(cx, -1.25, 1.0)]
    d["sens"] = pline(d["sens_pts"], BLUE, 5)
    d["bulb"] = ndot(cx, -1.2, 1.0, BLUE, 0.1)
    d["IN1"] = ndot(cx, -0.8, 1.0, CORD_GREY)
    d["st1"] = pline([pt(cx, -0.65, 1.0), pt(cx, -0.5, 1.0)], CORD_GREY, 4)
    d["IN2"] = ndot(cx, -0.15, 1.0, CORD_GREY)
    d["st2"] = pline([pt(cx, 0.0, 1.0), pt(cx, 0.2, 1.0)], CORD_GREY, 4)
    d["tk"] = [tickm(cx, -1.0, 1.0), tickm(cx, -0.41, 1.0), tickm(cx, 0.35, 1.0)]
    d["mdot"] = ndot(cx, 0.55, 1.0, ORANGE)
    d["mot_pts"] = [pt(cx, 0.55, 1.0), pt(cx, 1.4, 1.0), pt(cx, 1.7, 1.1), pt(cx, 2.2, 1.1)]
    d["motor"] = pline(d["mot_pts"], ORANGE, 11)
    d["flex"] = muscle(cx, 1.1)
    d["leg"] = mini_leg(cx)
    d["br_pts"] = [pt(cx, -0.8, 0.83), pt(cx, -0.8, 0.2), pt(cx, -0.5, -0.05)]
    d["branch"] = pline(d["br_pts"], CORD_GREY, 4)
    d["IN3"] = ndot(cx, -0.35, -0.05, CORD_GREY)
    d["instub"] = pline([pt(cx, -0.2, -0.05), pt(cx, -0.05, -0.05)], CORD_GREY, 4)
    d["minus"] = T("−", 34, WHITE).move_to(pt(cx, 0.1, -0.5))
    d["mdot2"] = ndot(cx, 0.3, -0.05, ORANGE)
    d["mot2_pts"] = [pt(cx, 0.3, -0.05), pt(cx, 1.0, -0.05), pt(cx, 1.3, -0.4), pt(cx, 2.2, -0.4)]
    d["motor2"] = pline(d["mot2_pts"], ORANGE, 11)
    d["ext"] = muscle(cx, -0.4, 1.0)
    return d


def title_k():
    return T("knee jerk", 40, TEXT).move_to(P(CK, 3.3))


def title_t():
    return T("tack withdrawal", 40, TEXT).move_to(P(CT, 3.3))


def grp(*xs):
    out = VGroup()
    for x in xs:
        if isinstance(x, (list, tuple)):
            out.add(*x)
        else:
            out.add(x)
    return out


def knee_full(d, inhib=True):
    xs = [d["cord"], d["rec"], d["sens"], d["bulb"], d["tick1"], d["mdot"], d["motor"], d["quad"], d["leg"]]
    d["rec"].set_fill(TEAL, 1)
    if inhib:
        xs += [d["branch"], d["IN"], d["instub"], d["minus"], d["mdot2"], d["motor2"], d["ham"]]
        d["ham"].set_fill(OFFGREY, 0.2).set_stroke(OFFGREY)
        d["motor2"].set_stroke(OFFGREY)
        d["mdot2"].set_color(OFFGREY)
    return grp(*xs)


def tack_full(d, chain=True, flexor=True, ext=True):
    d["rec"].set_opacity(1)
    xs = [d["cord"], d["rec"], d["sens"], d["bulb"], d["leg"]]
    if chain:
        xs += [d["IN1"], d["st1"], d["IN2"], d["st2"], d["tk"], d["mdot"]]
    if flexor:
        xs += [d["motor"], d["flex"]]
    if ext:
        xs += [d["branch"], d["IN3"], d["instub"], d["minus"], d["mdot2"], d["motor2"], d["ext"]]
        d["ext"].set_fill(OFFGREY, 0.2).set_stroke(OFFGREY)
        d["motor2"].set_stroke(OFFGREY)
        d["mdot2"].set_color(OFFGREY)
    return grp(*xs)


def route_k(d):
    return [(d["sens_pts"], 8.3), ([d["sens_pts"][-1], d["mot_pts"][0]], 1.0), (d["mot_pts"], 8.3),
            ([d["mot_pts"][-1], d["mot_pts"][-1]], 1.5)]


def route_t(d):
    return [(d["sens_pts"], 45.0), ([d["sens_pts"][-1], d["mot_pts"][0]], 3.0), (d["mot_pts"], 15.0),
            ([d["mot_pts"][-1], d["mot_pts"][-1]], 1.5)]


def route_pos(pieces, t):
    s = 0.0
    for pts, dur in pieces:
        if t <= s + dur:
            return poly_pt(pts, (t - s) / dur)
        s += dur
    return pieces[-1][0][-1]


def bar_parts(k, t, y=BARY, h=0.55):
    x0 = BX[k]
    g = VGroup()
    s = 0.0
    for dur, col in SEGS[k]:
        a, b = min(t, s), min(t, s + dur)
        if b > a + 1e-6:
            xa, xb = x0 + a * SC, x0 + b * SC
            if col is None:
                g.add(hatch(xa, xb, y, h))
            else:
                g.add(rect(xa, xb, y, h, col, 1.0 if (col is WHITE) else 0.85))
        if col is WHITE:
            n = int(round(dur))
            for i in range(n):
                tx = s + i + 0.5
                if t >= tx:
                    xx = x0 + tx * SC
                    g.add(Line(P(xx, y + h / 2), P(xx, y + h / 2 + 0.3), color=WHITE, stroke_width=5))
        s += dur
    return g


def full_bars():
    return VGroup(bar_parts("k", 99), bar_parts("t", 99))


def pulse_on(pieces, tr, color=GOLD, total=None):
    dot = Dot(radius=0.17, color=color)
    tot = sum(d for _, d in pieces)

    def up(m):
        t = tr.get_value()
        m.move_to(route_pos(pieces, t))
        m.set_opacity(1 if 0 < t < tot - 1.5 else 0)
    dot.add_updater(up)
    return dot


def loop_pulse(pts, period, delay=0.0, color=GOLD):
    return runner(pts, color, period, delay)


# ------------------------------------------------------------------ s00
class S00Title(TitleCard):
    LESSON = "Nervous Control: A First Look"
    TITLE = "One Synapse or Several"


# ------------------------------------------------------------------ s01
class S01Hook(SpokenScene):
    def construct(self):
        # left: knee jerk leg (as film 1), right: foot on a tack
        thigh = RoundedRectangle(corner_radius=0.4, width=3.4, height=1.0, stroke_color=GREY, stroke_width=3,
                                 fill_color=SKIN, fill_opacity=1).move_to(P(-3.9, 0.7))
        quad = Ellipse(width=2.4, height=0.55, color=RED, stroke_width=3, fill_opacity=0.28).move_to(P(-4.0, 0.58))
        shin = RoundedRectangle(corner_radius=0.3, width=0.7, height=2.2, stroke_color=GREY, stroke_width=3,
                                fill_color=SKIN, fill_opacity=1).move_to(P(-2.4, -0.5))
        foot = RoundedRectangle(corner_radius=0.12, width=0.9, height=0.3, stroke_color=GREY, stroke_width=3,
                                fill_color=SKIN, fill_opacity=1).move_to(P(-2.05, -1.75))
        lower = VGroup(shin, foot)
        knee = P(-2.4, 0.7)
        hm = VGroup(Line(P(-0.9, 2.6), P(-2.4, 0.9), color=GREY, stroke_width=8),
                    RoundedRectangle(corner_radius=0.1, width=0.45, height=0.7, stroke_color=TEXT, stroke_width=3,
                                     fill_color=GREY, fill_opacity=1).move_to(P(-2.55, 0.75)))
        div = Line(P(0, 3.5), P(0, -3.0), color=GREY, stroke_width=2).set_opacity(0.5)
        self.add(thigh, quad, lower, div)
        self.play(FadeIn(hm, shift=DL * 0.4), run_time=0.8)
        self.at("knee")
        self.play(hm.animate.shift(DL * 0.2), run_time=0.2, rate_func=rush_into)
        self.play(Rotate(lower, angle=-0.9, about_point=knee), hm.animate.shift(UR * 0.5), quad.animate.set_fill(RED, 0.8), run_time=0.5)
        self.play(Rotate(lower, angle=0.9, about_point=knee), quad.animate.set_fill(RED, 0.28), run_time=0.6)
        self.at("leg by leg")
        k_bar = bar_parts("k", 0)
        tr = ValueTracker(0.0)
        kb = always_redraw(lambda: bar_parts("k", tr.get_value(), -2.6))
        self.add(kb)
        self.play(tr.animate.set_value(19.1), FadeOut(hm), run_time=1.1, rate_func=linear)
        # right: foot and tack
        self.at("Now you step")
        floor = Line(P(1.0, -1.9), P(6.4, -1.9), color=GREY, stroke_width=4)
        tack = VGroup(Polygon(P(3.9, -1.9), P(4.3, -1.9), P(4.1, -1.55), color=TEXT, stroke_width=3, fill_color=GREY, fill_opacity=1),
                      Line(P(3.85, -1.55), P(4.35, -1.55), color=TEXT, stroke_width=5))
        shin2 = RoundedRectangle(corner_radius=0.3, width=0.7, height=2.4, stroke_color=GREY, stroke_width=3,
                                 fill_color=SKIN, fill_opacity=1).move_to(P(3.6, 0.0))
        foot2 = RoundedRectangle(corner_radius=0.12, width=1.5, height=0.3, stroke_color=GREY, stroke_width=3,
                                 fill_color=SKIN, fill_opacity=1).move_to(P(4.0, -1.35))
        leg2 = VGroup(shin2, foot2).shift(UP * 1.4)
        self.play(FadeIn(floor), FadeIn(tack), FadeIn(leg2), run_time=0.5)
        self.at("attack")
        self.play(leg2.animate.shift(DOWN * 1.4), run_time=0.4, rate_func=rush_into)
        self.play(Flash(P(4.1, -1.6), color=RED, flash_radius=0.6), leg2.animate.shift(UP * 1.2).rotate(-0.25, about_point=P(3.6, 1.2)), run_time=0.7)
        self.at("Is lifting")
        q = T("?", 110, YELLOW, weight=BOLD).move_to(P(0.0, 0.2))
        self.play(FadeIn(q, scale=0.6), run_time=0.6)
        self.add(breathe(q, 1.6, 0.6, 1.0))
        self.add(ripple(P(0, 0.2), YELLOW, 0.6, 1.4, 2.0))
        self.at("faster")
        self.play(leg2.animate.shift(DOWN * 1.2).rotate(0.25, about_point=P(3.6, 1.2)), run_time=0.6)
        self.play(leg2.animate.shift(UP * 1.2).rotate(-0.25, about_point=P(3.6, 1.2)), run_time=0.8)
        self.finish()


# ------------------------------------------------------------------ s02
class S02Split(SpokenScene):
    def construct(self):
        k, t = knee_parts(), tack_parts()
        tk_, tt_ = title_k(), title_t()
        div = Line(P(0, 3.5), P(0, -3.6), color=GREY, stroke_width=2).set_opacity(0.5)
        base = VGroup(k["cord"], k["rec"], k["quad"], t["cord"], t["rec"], t["flex"])
        k["rec"].set_fill(TEAL, 0.25)
        self.play(FadeIn(div), FadeIn(tk_), FadeIn(tt_), LaggedStart(*[FadeIn(m) for m in base], lag_ratio=0.2), run_time=2.4)
        self.add(ripple(k["rec"].get_center(), TEAL, 0.3, 0.8), ripple(t["rec"].get_center(), TEAL, 0.3, 0.8, 1.8, 0.5))
        self.at("five")
        labs = []
        names = [("receptor", TEAL), ("sensory\nneuron", BLUE), ("integrating\ncentre", CORD_GREY), ("motor\nneuron", ORANGE), ("effector", RED)]
        for i, (nm, c) in enumerate(names):
            labs.append(T(nm, 28, c, line_spacing=0.8).move_to(P(TOP_X[i], 3.1)))
        self.play(FadeOut(tk_), FadeOut(tt_), FadeIn(labs[0]), run_time=0.5)
        until(self, 5.7)
        for d in (k, t):
            d["rec"].set_fill(TEAL, 1) if d is k else d["rec"].set_opacity(1)
        self.play(k["rec"].animate.set_fill(TEAL, 1), t["rec"].animate.set_opacity(1), run_time=0.5)
        self.at("sensory neuron")
        self.play(FadeIn(labs[1]), Create(k["sens"]), Create(t["sens"]), run_time=1.6)
        self.add(loop_pulse(k["sens_pts"], 1.6), loop_pulse(t["sens_pts"], 3.0))
        self.at("integrating")
        self.play(FadeIn(labs[2]), k["cord"].animate.set_stroke(WHITE), t["cord"].animate.set_stroke(WHITE), run_time=0.5)
        self.play(k["cord"].animate.set_stroke(CORD_GREY), t["cord"].animate.set_stroke(CORD_GREY), run_time=0.6)
        self.at("motor neuron")
        self.play(FadeIn(labs[3]), Create(k["motor"]), Create(t["motor"]), run_time=1.0)
        self.at("effector")
        self.play(FadeIn(labs[4]), k["quad"].animate.set_fill(RED, 0.8), t["flex"].animate.set_fill(RED, 0.8), run_time=0.6)
        self.play(k["quad"].animate.set_fill(RED, 0.22), t["flex"].animate.set_fill(RED, 0.22), run_time=0.6)
        self.at("circuits")
        self.play(FadeOut(VGroup(*labs)), FadeIn(tk_), FadeIn(tt_), run_time=0.5)
        self.play(k["cord"].animate.scale(1.08), t["cord"].animate.scale(1.08), run_time=0.8)
        self.play(k["cord"].animate.scale(1 / 1.08), t["cord"].animate.scale(1 / 1.08), run_time=0.8)
        self.at("fibers")
        self.play(Indicate(k["sens"], color=BRIGHT_OR, scale_factor=1.0), Indicate(t["sens"], color=BRIGHT_OR, scale_factor=1.0), run_time=1.4)
        self.play(Indicate(k["motor"], color=BRIGHT_OR, scale_factor=1.0), Indicate(t["motor"], color=BRIGHT_OR, scale_factor=1.0), run_time=1.4)
        self.finish()


def stage_left(scene, d, inhib):
    return knee_full(d, inhib)


# ------------------------------------------------------------------ s03
class S03Knee(SpokenScene):
    def construct(self):
        k, t = knee_parts(), tack_parts()
        tkt = title_k()
        ttt = title_t()
        right = tack_full(t, chain=False, flexor=True, ext=False)
        dim(right, 0.35)
        left = grp(k["cord"], k["rec"], k["sens"], k["motor"], k["quad"], k["leg"])
        k["rec"].set_fill(TEAL, 1)
        self.add(tkt, ttt, right, left, Line(P(0, 3.5), P(0, -3.6), color=GREY, stroke_width=2).set_opacity(0.5))
        self.add(loop_pulse(k["sens_pts"], 2.4))
        wash(k["cord"])
        self.add(ripple(k["rec"].get_center(), TEAL, 0.3, 1.0, 1.6))
        self.at("spindle's sensory fiber")
        self.play(FadeIn(k["bulb"], scale=0.5), FadeIn(k["mdot"], scale=0.5), run_time=0.8)
        self.at("synapses straight")
        gd = Dot(radius=0.17, color=GOLD).move_to(k["sens_pts"][-1])
        self.add(gd)
        self.play(gd.animate.move_to(k["mdot"].get_center()), FadeIn(k["tick1"], scale=2.0), run_time=0.8)
        self.at("one synapse")
        sy = T("1 synapse", 30, WHITE).move_to(pt(CK, -0.3, -1.25))
        self.play(FadeIn(sy), Flash(k["tick1"], color=WHITE, flash_radius=0.5), run_time=0.8)
        self.play(MoveAlongPath(gd, pline(k["mot_pts"], ORANGE)), run_time=1.2, rate_func=linear)
        self.remove(gd)
        self.play(k["quad"].animate.set_fill(RED, 0.85), Rotate(k["leg"], angle=-0.9, about_point=k["leg"].pivot), run_time=0.6)
        self.play(k["quad"].animate.set_fill(RED, 0.22), Rotate(k["leg"], angle=0.9, about_point=k["leg"].pivot), run_time=0.8)
        kick_loop(k, "quad", 2.6)
        self.at("direct path")
        ml = T("monosynaptic", 34, WHITE).move_to(pt(CK, 0, 2.25))
        self.play(FadeIn(ml), run_time=0.6)
        self.add(loop_pulse(k["sens_pts"] + k["mot_pts"], 2.8, 0.0))
        self.play(Indicate(k["tick1"], color=WHITE, scale_factor=1.6), run_time=1.0)
        self.finish()


# ------------------------------------------------------------------ s04
class S04Inhib(SpokenScene):
    def construct(self):
        k, t = knee_parts(), tack_parts()
        right = tack_full(t, chain=False, flexor=True, ext=False)
        dim(right, 0.35)
        k["rec"].set_fill(TEAL, 1)
        left = grp(k["cord"], k["rec"], k["sens"], k["bulb"], k["tick1"], k["mdot"], k["motor"], k["quad"], k["leg"])
        self.add(title_k(), title_t(), right, left, Line(P(0, 3.5), P(0, -3.6), color=GREY, stroke_width=2).set_opacity(0.5))
        self.add(loop_pulse(k["sens_pts"] + k["mot_pts"][1:], 3.0))
        self.at("side branch")
        self.play(Create(k["branch"]), run_time=1.0)
        self.at("interneuron")
        k["ham"].set_fill(RED, 0.22).set_stroke(RED)
        self.play(FadeIn(k["IN"], scale=0.4), Create(k["instub"]), run_time=0.7)
        li = T("interneuron", 28, CORD_GREY).move_to(pt(CK, -0.9, -1.2))
        ll = Line(pt(CK, -0.25, -0.25), pt(CK, -0.6, -0.95), color=CORD_GREY, stroke_width=3)
        self.play(FadeIn(li), Create(ll), run_time=0.6)
        self.add(loop_pulse(k["br_pts"] + [k["IN"].get_center()], 2.0, 0.5))
        self.at("stays inside")
        self.play(k["cord"].animate.set_stroke(WHITE), run_time=0.5)
        self.play(k["cord"].animate.set_stroke(CORD_GREY), run_time=0.8)
        self.at("quiets")
        self.play(FadeIn(k["minus"], scale=1.6), FadeIn(k["mdot2"], scale=0.4), Create(k["motor2"]), FadeIn(k["ham"]), run_time=1.0)
        self.at("hamstring")
        hl = label_r("hamstring", CK, -1.2, TEXT)
        self.play(FadeIn(hl), k["ham"].animate.set_fill(OFFGREY, 0.2).set_stroke(OFFGREY),
                  k["motor2"].animate.set_stroke(OFFGREY), k["mdot2"].animate.set_color(OFFGREY), run_time=1.2)
        self.at("muscle that would oppose")
        qb = label_r("quadriceps", CK, 2.0, TEXT)
        self.play(FadeIn(qb), k["quad"].animate.set_fill(RED, 0.85), Rotate(k["leg"], angle=-0.9, about_point=k["leg"].pivot), run_time=0.7)
        self.play(k["quad"].animate.set_fill(RED, 0.22), Rotate(k["leg"], angle=0.9, about_point=k["leg"].pivot), run_time=1.0)
        self.at("not one wire")
        self.play(FadeOut(li), FadeOut(ll), FadeOut(hl), FadeOut(qb), run_time=0.4)
        self.add(loop_pulse(k["sens_pts"] + k["mot_pts"][1:], 2.4), loop_pulse(k["br_pts"] + [k["IN"].get_center()], 1.6, 0.3))
        self.play(Indicate(k["branch"], color=WHITE, scale_factor=1.0), Indicate(k["motor"], color=WHITE, scale_factor=1.0), run_time=1.4)
        self.finish()


# ------------------------------------------------------------------ s05
class S05Withdraw(SpokenScene):
    def construct(self):
        k, t = knee_parts(), tack_parts()
        left = knee_full(k, True)
        dim(left, 0.35)
        self.add(title_k(), title_t(), left, Line(P(0, 3.5), P(0, -3.6), color=GREY, stroke_width=2).set_opacity(0.5))
        t["rec"].set_opacity(0.4)
        base = grp(t["cord"], t["rec"], t["flex"], t["leg"], t["motor"], t["mdot"])
        self.add(base)
        self.add(runner(k["sens_pts"] + k["mot_pts"][1:], GOLD, 2.4).set_opacity(0.0))
        self.at("tack")
        tack = Polygon(pt(CT, -2.85, -2.85), pt(CT, -2.35, -2.85), pt(CT, -2.6, -2.5), color=TEXT, stroke_width=3,
                       fill_color=GREY, fill_opacity=1)
        self.play(FadeIn(tack, shift=UP * 0.3), run_time=0.8)
        self.at("pain")
        pl = T("pain endings", 28, TEAL).move_to(pt(CT, -0.3, -2.05))
        self.play(t["rec"].animate.set_opacity(1), FadeIn(pl), run_time=0.6)
        self.add(ripple(t["rec"].get_center(), TEAL, 0.3, 0.9), ripple(t["rec"].get_center(), TEAL, 0.3, 0.9, 1.8, 0.9))
        until(self, 4.6)
        self.at("thin sensory")
        self.play(FadeOut(pl), FadeOut(tack), Create(t["sens"]), FadeIn(t["bulb"]), run_time=1.0)
        self.add(loop_pulse(t["sens_pts"], 3.6))
        sl = T("thin fibre", 28, BLUE).move_to(pt(CT, -2.2, 2.05))
        self.play(FadeIn(sl), run_time=0.5)
        self.at("chain")
        self.play(FadeIn(t["IN1"], scale=0.4), Create(t["st1"]), FadeIn(t["tk"][0], scale=2), run_time=0.9)
        self.play(FadeIn(t["IN2"], scale=0.4), Create(t["st2"]), FadeIn(t["tk"][1], scale=2), FadeIn(t["tk"][2], scale=2), run_time=1.0)
        self.add(loop_pulse([t["sens_pts"][-1], t["mot_pts"][0]], 2.0, 0.2))
        self.at("right from")
        self.play(FadeOut(sl), run_time=0.3)
        tl = T("3 synapses", 32, WHITE).move_to(pt(CT, 0, 2.25))
        self.play(FadeIn(tl), *[Flash(x, color=WHITE, flash_radius=0.45) for x in t["tk"]], run_time=1.0)
        self.finish()


# ------------------------------------------------------------------ s06
class S06Flex(SpokenScene):
    def construct(self):
        k, t = knee_parts(), tack_parts()
        left = knee_full(k, True)
        dim(left, 0.35)
        right = tack_full(t, chain=True, flexor=False, ext=False)
        self.add(title_k(), title_t(), left, right, Line(P(0, 3.5), P(0, -3.6), color=GREY, stroke_width=2).set_opacity(0.5))
        self.add(loop_pulse(t["sens_pts"] + [t["mdot"].get_center()], 4.0))
        self.at("drive")
        t["motor"].set_stroke(ORANGE)
        self.play(Create(t["motor"]), FadeIn(t["flex"]), run_time=1.0)
        fl = label_r("flexors", CT, 2.0, TEXT)
        self.play(FadeIn(fl), t["flex"].animate.set_fill(RED, 0.85), run_time=0.6)
        self.at("lift")
        self.add(loop_pulse([t["mdot"].get_center()] + t["mot_pts"], 1.4, 0.0))
        self.play(FadeIn(t["leg"]), run_time=0.3)
        self.play(Rotate(t["leg"], angle=-1.0, about_point=t["leg"].pivot), run_time=1.2)
        self.play(Rotate(t["leg"], angle=1.0, about_point=t["leg"].pivot), t["flex"].animate.set_fill(RED, 0.22), run_time=1.0)
        self.at("Others")
        self.play(FadeOut(fl), Create(t["branch"]), FadeIn(t["IN3"], scale=0.4), Create(t["instub"]), run_time=1.0)
        self.add(loop_pulse(t["br_pts"], 1.8, 0.2))
        self.at("opposing")
        t["ext"].set_fill(RED, 0.22).set_stroke(RED)
        self.play(FadeIn(t["minus"], scale=1.6), FadeIn(t["mdot2"], scale=0.4), Create(t["motor2"]), FadeIn(t["ext"]), run_time=1.0)
        el = label_r("extensors", CT, -1.2, TEXT)
        self.play(FadeIn(el), t["ext"].animate.set_fill(OFFGREY, 0.2).set_stroke(OFFGREY),
                  t["motor2"].animate.set_stroke(OFFGREY), t["mdot2"].animate.set_color(OFFGREY), run_time=1.2)
        self.at("Charles")
        self.play(FadeOut(el), run_time=0.3)
        sh = T("Sherrington:\nreciprocal innervation", 28, YELLOW, line_spacing=0.8).move_to(pt(CT, 1.0, 2.3))
        self.play(FadeIn(sh), run_time=0.8)
        self.add(loop_pulse(t["br_pts"], 1.8, 0.0), loop_pulse([t["mdot"].get_center()] + t["mot_pts"], 1.6, 0.4))
        self.play(Indicate(t["flex"], color=RED, scale_factor=1.15), Indicate(t["ext"], color=WHITE, scale_factor=1.0), run_time=1.6)
        self.finish()


# ------------------------------------------------------------------ s07..s09 world with bars
def both_full():
    k, t = knee_parts(), tack_parts()
    left = knee_full(k, True)
    right = tack_full(t, True, True, True)
    return k, t, left, right


class S07Bars(SpokenScene):
    def construct(self):
        k, t, left, right = both_full()
        div = Line(P(0, 3.5), P(0, -2.9), color=GREY, stroke_width=2).set_opacity(0.5)
        self.add(title_k(), title_t(), left, right, div)
        tr = ValueTracker(0.0)
        bk = always_redraw(lambda: bar_parts("k", tr.get_value()))
        bt = always_redraw(lambda: bar_parts("t", tr.get_value()))
        pk, pt_ = route_k(k), route_t(t)
        gk, gt = pulse_on(pk, tr), pulse_on(pt_, tr)
        k["quad"].add_updater(lambda m: m.set_fill(RED, 0.85 if tr.get_value() > 17.6 else 0.22))
        t["flex"].add_updater(lambda m: m.set_fill(RED, 0.85 if tr.get_value() > 63 else 0.22))
        self.add(bk, bt, gk, gt)
        sl = T("same scale", 28, TEXT).move_to(P(-1.9, BARY))
        self.play(FadeIn(sl), run_time=0.6)
        self.at("together")
        self.play(tr.animate.set_value(64.5), run_time=6.5, rate_func=linear)
        self.at("It has more")
        self.play(FadeOut(sl), *[Flash(P(BX["t"] + (45 + i + 0.5) * SC, BARY + 0.4), color=WHITE, flash_radius=0.3) for i in range(3)], run_time=0.8)
        self.at("ticks")
        self.play(Flash(P(BX["k"] + 8.8 * SC, BARY + 0.4), color=WHITE, flash_radius=0.3), run_time=0.8)
        k["quad"].clear_updaters(); t["flex"].clear_updaters()
        self.finish()


class S08Predict(SpokenScene):
    def construct(self):
        k, t, left, right = both_full()
        div = Line(P(0, 3.5), P(0, -2.9), color=GREY, stroke_width=2).set_opacity(0.5)
        self.add(title_k(), title_t(), left, right, div, full_bars())
        self.add(loop_pulse(route_pts(t), 5.0), loop_pulse(route_pts(k), 2.5))
        self.at("three")
        self.play(*[Flash(x, color=WHITE, flash_radius=0.4) for x in t["tk"]], run_time=0.8)
        self.at("only one")
        self.play(Flash(k["tick1"], color=WHITE, flash_radius=0.4), run_time=0.8)
        self.at("So are")
        q = T("?", 90, YELLOW, weight=BOLD).move_to(P(0, -1.5))
        self.play(FadeIn(q, scale=1.5), run_time=0.6)
        self.add(breathe(q, 1.6, 0.6, 1.0))
        self.add(ripple(P(0, -1.5), YELLOW, 0.5, 1.2, 2.0))
        self.finish()


def route_pts(d):
    return d["sens_pts"] + d["mot_pts"]


class S09Pause(NarratedScene):
    def construct(self):
        k, t, left, right = both_full()
        div = Line(P(0, 3.5), P(0, -2.9), color=GREY, stroke_width=2).set_opacity(0.5)
        q = T("?", 90, YELLOW, weight=BOLD).move_to(P(0, -1.5))
        self.add(title_k(), title_t(), left, right, div, full_bars(), q)
        self.add(breathe(q, 1.6, 0.4, 1.0))
        self.add(ripple(P(0, -1.5), YELLOW, 0.5, 1.2, 2.0))
        for x in t["tk"]:
            self.add(ripple(x.get_center(), WHITE, 0.15, 0.5, 2.0))
        self.add(loop_pulse(route_pts(t), 4.0), loop_pulse(route_pts(k), 2.0))
        self.finish()


# ------------------------------------------------------------------ s10
ROWY = {"sens": 2.0, "syn": 0.8, "mot": -0.4, "end": -1.6}
RX0 = -4.0
RSC = 0.13


def row_bar(key, which):
    segs = {"sens": 0, "syn": 1, "mot": 2, "end": 3}[key]
    dur, col = SEGS[which][segs]
    y = ROWY[key] + (0.24 if which == "k" else -0.24)
    if col is None:
        return hatch(RX0, RX0 + dur * RSC, y, 0.36)
    return rect(RX0, RX0 + dur * RSC, y, 0.36, col, 1.0 if (col is WHITE) else 0.85)


class S10Reveal(SpokenScene):
    def construct(self):
        bars = full_bars()
        self.add(bars)
        names = {"sens": ("sensory", BLUE), "syn": ("synapses", WHITE), "mot": ("motor", ORANGE), "end": ("ends", GREY)}
        rows = {}
        labs = {}
        for key, (nm, c) in names.items():
            labs[key] = T(nm, 30, c).move_to(P(-6.6, ROWY[key]), aligned_edge=LEFT)
            rows[key] = (row_bar(key, "k"), row_bar(key, "t"))
        leg_k = T("knee", 26, TEXT).move_to(P(-4.4 + 0, 3.1))
        self.play(FadeOut(bars), LaggedStart(*[FadeIn(labs[x]) for x in labs], lag_ratio=0.2),
                  *[FadeIn(rows[x][0]) for x in rows], *[FadeIn(rows[x][1]) for x in rows], run_time=2.4)
        sw = VGroup(T("upper bar: knee jerk", 26, TEXT), T("lower bar: withdrawal", 26, TEXT)).arrange(DOWN, aligned_edge=LEFT, buff=0.1)
        sw.move_to(P(3.6, 3.0))
        self.play(FadeIn(sw), run_time=0.6)
        self.at("each synapse")
        nums = {}

        def num(key, which, text):
            r = rows[key][0 if which == "k" else 1]
            n = T(text, 28, TEXT)
            n.move_to(P(r.get_right()[0] + 0.25 + n.width / 2, r.get_center()[1]))
            return n
        s1, s3 = num("syn", "k", "1 ms"), num("syn", "t", "3 ms")
        self.play(FadeIn(s1), FadeIn(s3), Indicate(rows["syn"][0], color=WHITE), Indicate(rows["syn"][1], color=WHITE), run_time=1.6)
        self.at("big difference")
        a, b = num("sens", "k", "8.3 ms"), num("sens", "t", "45 ms")
        self.play(FadeIn(a), FadeIn(b), run_time=0.8)
        self.play(Indicate(rows["sens"][1], color=BRIGHT_OR, scale_factor=1.05), run_time=1.4)
        self.at("conduct")
        m1, m2, e1, e2 = num("mot", "k", "8.3 ms"), num("mot", "t", "15 ms"), num("end", "k", "1.5 ms"), num("end", "t", "1.5 ms")
        self.play(FadeIn(m1), FadeIn(m2), FadeIn(e1), FadeIn(e2), run_time=1.0)
        self.add(runner([P(RX0, 2.24), P(RX0 + RSC * 45, 2.24)], GOLD, 2.6, 0.0, 0.0001))
        self.at("tens of")
        tot = T("totals: about 19 ms and about 65 ms", 32, YELLOW).move_to(P(0, -2.75))
        self.play(FadeIn(tot), run_time=0.8)
        self.play(Indicate(rows["sens"][1], color=BRIGHT_OR, scale_factor=1.05), run_time=1.2)
        self.finish()


# ------------------------------------------------------------------ s11
class S11Thin(SpokenScene):
    def construct(self):
        XA, XB = -5.8, 5.8
        YW, YT = 1.8, 0.3
        wide = RoundedRectangle(corner_radius=0.3, width=XB - XA, height=0.9, stroke_color=BLUE, stroke_width=4,
                                fill_color=BLUE, fill_opacity=0.25).move_to(P(0, YW))
        thin = RoundedRectangle(corner_radius=0.1, width=XB - XA, height=0.22, stroke_color=BLUE, stroke_width=3,
                                fill_color=BLUE, fill_opacity=0.25).move_to(P(0, YT))
        lw = T("wide fibre", 28, BLUE).move_to(P(XA, 2.8), aligned_edge=LEFT)
        lt = T("thin fibre", 28, BLUE).move_to(P(XA, 0.95), aligned_edge=LEFT)
        sch = T("schematic", 26, TEXT).move_to(P(5.5, 3.3))
        tl = T("time", 28, BLUE).move_to(P(-6.6, -1.35), aligned_edge=LEFT)
        wl = T("wide", 26, BLUE).move_to(P(-6.6, -1.95), aligned_edge=LEFT)
        tn = T("thin", 26, BLUE).move_to(P(-6.6, -2.8), aligned_edge=LEFT)
        self.play(FadeIn(wide), FadeIn(thin), FadeIn(lw), FadeIn(lt), FadeIn(sch), FadeIn(wl), FadeIn(tn), run_time=1.2)
        PER = 8.0
        TW, TT = 2.4, 5.2
        clock = ValueTracker(0.0)

        def pos(T_, y, t):
            f = min(1, max(0, t / T_))
            return XA + (XB - XA) * f

        def wpulse():
            t = clock.get_value() % PER
            return Rectangle(width=0.3, height=0.9, stroke_width=0, fill_color=GOLD, fill_opacity=1).move_to(P(pos(TW, YW, t), YW))

        def tpulse():
            t = clock.get_value() % PER
            return Rectangle(width=0.3, height=0.22, stroke_width=0, fill_color=GOLD, fill_opacity=1).move_to(P(pos(TT, YT, t), YT))
        glow_on = ValueTracker(0.0)

        def glowW():
            t = clock.get_value() % PER
            x = pos(TW, YW, t)
            L = 2.4
            return Rectangle(width=L, height=1.4, stroke_width=0, fill_color=YELLOW,
                             fill_opacity=0.28 * glow_on.get_value() * (t < TW)).move_to(P(x + 0.15 + L / 2, YW))

        def glowT():
            t = clock.get_value() % PER
            x = pos(TT, YT, t)
            L = 0.9
            return Rectangle(width=L, height=0.6, stroke_width=0, fill_color=YELLOW,
                             fill_opacity=0.28 * glow_on.get_value() * (t < TT)).move_to(P(x + 0.15 + L / 2, YT))

        def bars():
            t = clock.get_value() % PER
            g = VGroup()
            g.add(rect(-4.5, -4.5 + 1.6 * min(t, TW), -1.95, 0.4, BLUE))
            g.add(rect(-4.5, -4.5 + 1.6 * min(t, TT), -2.8, 0.4, BLUE))
            return g
        self.add(always_redraw(glowW), always_redraw(glowT), always_redraw(wpulse), always_redraw(tpulse), always_redraw(bars))
        self.play(clock.animate.set_value(1.0), run_time=1.0, rate_func=linear)
        self.at("thin axon")
        self.play(glow_on.animate.set_value(1.0), clock.animate.set_value(clock.get_value() + 2.0), run_time=2.0, rate_func=linear)
        self.at("more resistance")
        rl = T("more resistance", 28, YELLOW).move_to(P(-2.2, 0.95), aligned_edge=LEFT)
        self.play(FadeIn(rl), clock.animate.set_value(clock.get_value() + 1.5), run_time=1.5, rate_func=linear)
        self.at("current spreading")
        gl = T("current spreads ahead", 28, YELLOW).move_to(P(2.4, 2.8))
        self.play(FadeIn(gl), clock.animate.set_value(clock.get_value() + 1.5), run_time=1.5, rate_func=linear)
        self.at("travels more slowly")
        self.play(FadeOut(gl), FadeOut(rl), clock.animate.set_value(clock.get_value() + 3.0), run_time=3.0, rate_func=linear)
        self.at("stretches out")
        sl = T("sensory leg: longer time", 28, BLUE).move_to(P(1.5, -1.35))
        self.play(FadeIn(sl), clock.animate.set_value(clock.get_value() + 2.0), run_time=2.0, rate_func=linear)
        self.play(clock.animate.set_value(clock.get_value() + 2.0), run_time=2.0, rate_func=linear)
        self.finish()


# ------------------------------------------------------------------ s12
class S12Caveat(SpokenScene):
    def construct(self):
        X0, Y = -6.2, 0.4
        w = lambda ms: ms * 0.2
        xb, xo, xw, xe = X0 + w(37), X0 + w(37) + w(7), X0 + w(37) + w(7) + w(2), X0 + w(46)
        frame = Rectangle(width=w(46), height=1.3, stroke_color=GREY, stroke_width=2, fill_opacity=0).move_to(P((X0 + xe) / 2, Y))
        title = T("the extra time", 36, TEXT).move_to(P(-4.4, 2.8))
        self.play(FadeIn(title), Create(frame), run_time=1.2)
        self.at("longer motor path")
        o = rect(xb, xo, Y, 1.3, ORANGE)
        ol = T("longer motor path\nabout 7 ms", 28, ORANGE, line_spacing=0.8).move_to(P((xb + xo) / 2 + 0.6, -1.1))
        ol_l = Line(P((xb + xo) / 2, Y - 0.65), P((xb + xo) / 2 + 0.2, -0.55), color=ORANGE, stroke_width=3)
        self.play(GrowFromEdge(o, LEFT), run_time=1.0)
        self.play(FadeIn(ol), Create(ol_l), run_time=0.7)
        self.at("slow fibers")
        b = rect(X0, xb, Y, 1.3, BLUE)
        bl = T("slower sensory leg about 37 ms", 28, BLUE).move_to(P(X0 + 3.7, 1.7))
        self.play(GrowFromEdge(b, LEFT), run_time=1.3)
        self.play(FadeIn(bl), run_time=0.6)
        self.at("not all")
        wt = rect(xo, xw, Y, 1.3, WHITE, 1.0)
        wl = T("extra synapses 2 ms", 28, WHITE).move_to(P(4.3, 1.7))
        wl_l = Line(P((xo + xw) / 2, Y + 0.65), P(3.4, 1.45), color=WHITE, stroke_width=3)
        self.play(FadeIn(wt, scale=2.0), run_time=0.6)
        self.play(FadeIn(wl), Create(wl_l), run_time=0.7)
        self.at("real people")
        dash = DashedLine(P(xe + 0.05, Y), P(6.6, Y), color=YELLOW, stroke_width=4)
        arr = Arrow(P(6.2, Y), P(6.75, Y), buff=0, color=YELLOW, stroke_width=4, tip_length=0.2)
        rl = T("real people: often near\na tenth of a second (schematic)", 28, YELLOW, line_spacing=0.8).move_to(P(2.3, -2.5))
        rl_l = DashedLine(P(5.0, Y - 0.35), P(4.6, -2.0), color=YELLOW, stroke_width=3)
        self.play(Create(dash), FadeIn(arr), run_time=0.8)
        self.play(FadeIn(rl), Create(rl_l), run_time=0.5)
        self.at("fiber speed")
        self.play(Indicate(b, color=BRIGHT_OR, scale_factor=1.0), run_time=1.0)
        self.play(Indicate(o, color=BRIGHT_OR, scale_factor=1.0), run_time=1.0)
        self.finish()


# ------------------------------------------------------------------ s13
def head(cx):
    face = Circle(radius=0.38, stroke_color=TEXT, stroke_width=3, fill_color=SKIN, fill_opacity=1).move_to(P(cx - 1.6, 3.0))
    eyes = VGroup(Dot(radius=0.04, color=TEXT).move_to(P(cx - 1.72, 3.05)), Dot(radius=0.04, color=TEXT).move_to(P(cx - 1.48, 3.05)))
    return VGroup(face, eyes)


def bubble(cx):
    box = RoundedRectangle(corner_radius=0.2, width=2.2, height=0.7, stroke_color=TEXT, stroke_width=3, fill_color=BG, fill_opacity=1).move_to(P(cx + 0.7, 3.1))
    txt = T("I decide", 28, TEXT).move_to(box)
    return VGroup(box, txt)


class S13Somatic(SpokenScene):
    def construct(self):
        k, t, left, right = both_full()
        div = Line(P(0, 3.5), P(0, -3.0), color=GREY, stroke_width=2).set_opacity(0.5)
        ttl = VGroup(title_k(), title_t())
        self.add(ttl, left, right, div)
        self.add(loop_pulse(route_pts(k), 2.2), loop_pulse(route_pts(t), 3.6))
        self.at("skeletal")
        lk = label_r("skeletal muscle", CK, 2.1, RED)
        lt = label_r("skeletal muscle", CT, 2.1, RED)
        self.play(FadeIn(lk), FadeIn(lt), k["quad"].animate.set_fill(RED, 0.85), t["flex"].animate.set_fill(RED, 0.85), run_time=1.0)
        self.at("somatic")
        lk2 = label_r("so: somatic", CK, 2.1, YELLOW)
        lt2 = label_r("so: somatic", CT, 2.1, YELLOW)
        self.play(Transform(lk, lk2), Transform(lt, lt2), run_time=0.8)
        self.play(Indicate(k["quad"], color=RED), Indicate(t["flex"], color=RED), run_time=1.2)
        self.at("Somatic does")
        self.play(FadeOut(lk), FadeOut(lt), run_time=0.4)
        hk, ht = head(CK), head(CT)
        bk_, bt_ = bubble(CK), bubble(CT)
        self.play(FadeOut(ttl), FadeIn(hk), FadeIn(ht), FadeIn(bk_), FadeIn(bt_), run_time=1.0)
        self.at("voluntary")
        self.play(Indicate(bk_, color=YELLOW, scale_factor=1.05), Indicate(bt_, color=YELLOW, scale_factor=1.05), run_time=1.6)
        self.at("Neither")
        xs = VGroup(*[VGroup(Line(b.get_corner(UL) + DR * 0.05, b.get_corner(DR) + UL * 0.05, color=RED, stroke_width=6),
                              Line(b.get_corner(UR) + DL * 0.05, b.get_corner(DL) + UR * 0.05, color=RED, stroke_width=6))
                      for b in (bk_[0], bt_[0])])
        self.play(Create(xs), run_time=1.0)
        self.add(loop_pulse(route_pts(k), 1.5), loop_pulse(route_pts(t), 2.0))
        self.play(Indicate(k["quad"], color=RED), Indicate(t["flex"], color=RED), run_time=1.6)
        self.finish()


# ------------------------------------------------------------------ s14
class S14Rule(SpokenScene):
    def construct(self):
        k, t, left, right = both_full()
        div = Line(P(0, 3.5), P(0, -2.9), color=GREY, stroke_width=2).set_opacity(0.5)
        bars = full_bars()
        old = VGroup(title_k(), title_t(), left, right, div, bars)
        self.add(old)
        # one diagram: receptor - blue fibre - cord - orange fibre - muscle
        Y = 1.7
        rec = Circle(radius=0.3, stroke_color=TEAL, fill_color=TEAL, fill_opacity=1).move_to(P(-5.6, Y))
        sens = pline([P(-5.3, Y), P(-2.2, Y)], BLUE, 8)
        cord = RoundedRectangle(corner_radius=0.3, width=3.0, height=1.6, stroke_color=CORD_GREY, stroke_width=4,
                                fill_color=CORD_GREY, fill_opacity=0.2).move_to(P(0, Y))
        mot = pline([P(2.2, Y), P(5.2, Y)], ORANGE, 8)
        mus = Ellipse(width=0.9, height=1.3, color=RED, stroke_width=4, fill_opacity=0.5).move_to(P(5.7, Y))
        route = VGroup(rec, sens, cord, mot, mus)
        self.play(FadeOut(old), FadeIn(route), run_time=1.6)
        self.add(runner([P(-5.6, Y), P(-2.2, Y), P(2.2, Y), P(5.2, Y)], GOLD, 3.0))
        self.at("synapses set")
        mag_c = Circle(radius=0.55, stroke_color=YELLOW, stroke_width=6, fill_opacity=0).move_to(P(0, Y))
        mag_h = Line(P(0.4, Y - 0.4), P(0.95, Y - 0.95), color=YELLOW, stroke_width=8)
        mag = VGroup(mag_c, mag_h)
        ml = T("synapses: the circuit", 32, YELLOW).move_to(P(0, 0.35))
        self.play(FadeIn(mag, scale=1.4), FadeIn(ml), run_time=1.0)
        self.at("slow fibers")
        ruler = VGroup(Rectangle(width=2.0, height=0.3, stroke_color=TEXT, stroke_width=3, fill_opacity=0),
                       *[Line(P(-0.9 + 0.2 * i, 0.15), P(-0.9 + 0.2 * i, 0.15 - (0.15 if i % 2 else 0.1)), color=TEXT, stroke_width=2) for i in range(10)])
        ruler.move_to(P(-3.8, Y + 1.15))
        fl = T("fibres: most of the time", 32, BLUE).move_to(P(-0.4, 3.35))
        fl2 = T("(in these reflexes)", 28, BLUE).move_to(P(-0.4, 2.85))
        self.play(FadeIn(ruler), FadeIn(fl), FadeIn(fl2), Indicate(sens, color=WHITE, scale_factor=1.0), Indicate(mot, color=WHITE, scale_factor=1.0), run_time=1.6)
        self.at("The sum")
        e1 = T("response time = sum of (length ÷ speed) for each axon", 28, TEXT)
        e2 = T("+ synapses in the cord × about 1 ms", 28, TEXT)
        e3 = T("+ end delays", 28, TEXT)
        eq = VGroup(e1, e2, e3).arrange(DOWN, buff=0.25, aligned_edge=LEFT).move_to(P(0, -1.6))
        fit(eq, 12.4)
        self.play(Write(e1), run_time=1.6)
        self.play(Write(e2), run_time=1.0)
        self.play(Write(e3), run_time=0.6)
        self.play(Indicate(eq, color=YELLOW, scale_factor=1.03), run_time=1.2)
        self.finish()


class S15End(EndCard):
    LINE = "Here, slow fibres, not extra synapses, make most of the gap."
