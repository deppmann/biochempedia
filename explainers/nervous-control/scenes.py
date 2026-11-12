"""Nervous control: every response has a running time (Biochemistrypedia organismal biology film).

COLOUR MAP (one colour per concept, whole film, same as the lesson)
  GOLD   = the signal pulse that travels the route
  TEAL   = receptor            BLUE   = sensory neuron (and nerve time in the timer bar)
  GREY   = integrating centre  ORANGE = motor neuron
  RED    = effector muscle     WHITE  = a synapse (tick)
  hatched GREY = junction + muscle delay at the end of a timer bar
"""
import os
import numpy as np
from bp_style import *  # noqa: F401,F403

ORANGE = "#F29E4C"
BRIGHT_OR = "#FFC27A"
CORD_GREY = "#B8BFCC"
SKIN = "#2a2f3a"
NERVE = "#C9CED8"


# ------------------------------------------------------------------ helpers
def W(x, y):
    """World coordinates of the leg picture (shifted right so it fills the frame)."""
    return np.array([x + 1.0, y, 0.0])


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
    return Rectangle(width=x1 - x0, height=h, stroke_color=color, stroke_width=2,
                     fill_color=color, fill_opacity=op).move_to(P((x0 + x1) / 2, y))


# ------------------------------------------------------------------ leg world
K = W(1.5, 0.6)
S_PT = W(0.5, 0.98)
SENS = [W(0.5, 0.98), W(-0.2, 1.7), W(-3.95 + 0.0, 1.7)]
SENS = [P(S_PT[0], S_PT[1]), W(-0.2, 1.7), W(-4.0, 1.7)]
MOTOR = [W(-3.95, 0.1), W(-2.9, 0.1), W(-1.6, 0.4)]
STN = [S_PT, W(-2.2, 1.7), W(-4.4, 0.9) + P(0.0, 0.0), W(-3.4, 0.1), W(-1.0, 0.45)]
STN[2] = W(-5.4, 0.9)
CORD_C = W(-5.4, 0.7)
STN_COL = [TEAL, BLUE, CORD_GREY, ORANGE, RED]
TOP_X = [-5.4, -2.7, 0.0, 2.7, 5.4]


def leg_parts():
    thigh = RoundedRectangle(corner_radius=0.5, width=4.6, height=1.3, stroke_color=GREY, stroke_width=3,
                             fill_color=SKIN, fill_opacity=1).move_to(W(-0.5, 0.6))
    quad = Ellipse(width=3.2, height=0.7, color=RED, stroke_width=3, fill_opacity=0.28).move_to(W(-0.6, 0.45))
    shin = RoundedRectangle(corner_radius=0.35, width=0.85, height=2.8, stroke_color=GREY, stroke_width=3,
                            fill_color=SKIN, fill_opacity=1).move_to(W(1.5, -0.5))
    foot = RoundedRectangle(corner_radius=0.15, width=1.0, height=0.35, stroke_color=GREY, stroke_width=3,
                            fill_color=SKIN, fill_opacity=1).move_to(W(1.9, -1.75))
    lower = VGroup(shin, foot)
    cap = Circle(radius=0.22, stroke_color=GREY, stroke_width=3, fill_color=SKIN, fill_opacity=1).move_to(W(1.95, 0.6))
    return thigh, quad, lower, cap


def cord_mob():
    return RoundedRectangle(corner_radius=0.4, width=0.9, height=3.6, stroke_color=CORD_GREY, stroke_width=4,
                            fill_color=CORD_GREY, fill_opacity=0.22).move_to(CORD_C)


def inner_cord(blue=True, orange=True):
    g = VGroup()
    if blue:
        g.add(pline([W(-4.95, 1.7), W(-5.4, 1.25)], BLUE, 7))
    if orange:
        g.add(pline([W(-5.4, 0.55), W(-4.95, 0.1)], ORANGE, 7))
    return g


def tick():
    return Rectangle(width=0.5, height=0.14, stroke_width=0, fill_color=WHITE, fill_opacity=1).move_to(W(-5.4, 0.9))


def station(i, filled):
    d = Circle(radius=0.22 if i != 2 else 0.3, stroke_color=STN_COL[i] if filled else GREY, stroke_width=4,
               fill_color=STN_COL[i], fill_opacity=1 if filled else 0.0).move_to(STN[i])
    return d


def hammer():
    handle = Line(W(4.6, 2.4), W(2.55, 0.2), color=GREY, stroke_width=8)
    head = RoundedRectangle(corner_radius=0.1, width=0.5, height=0.8, stroke_color=TEXT, stroke_width=3,
                            fill_color=GREY, fill_opacity=1).move_to(W(2.4, 0.1))
    return VGroup(handle, head)


def top_labels():
    texts = [("receptor", TEAL), ("sensory\nneuron", BLUE), ("integrating\ncentre", CORD_GREY),
             ("motor\nneuron", ORANGE), ("effector", RED)]
    labs = [T(t, 28, c, line_spacing=0.8).move_to(P(TOP_X[i], 3.1)) for i, (t, c) in enumerate(texts)]
    arrs = [Arrow(P((TOP_X[i] + TOP_X[i + 1]) / 2 - 0.3, 3.1), P((TOP_X[i] + TOP_X[i + 1]) / 2 + 0.3, 3.1), buff=0,
                  color=GREY, stroke_width=4, tip_length=0.2) for i in range(4)]
    return labs, arrs


def frog_world(near=True, far=False, bar1=True, bar2=False):
    """Frog calf muscle, its nerve and the electrodes; same coordinates in every Helmholtz scene."""
    out = {}
    out["muscle"] = Ellipse(width=2.4, height=2.6, color=RED, stroke_width=4, fill_opacity=0.35).move_to(P(4.6, 1.3))
    out["nerve"] = pline([P(3.4, 1.3), P(-5.6, 1.3)], NERVE, 16)

    def electrode(x, name):
        stick = Line(P(x, 2.75), P(x, 1.45), color=YELLOW, stroke_width=6)
        tip = Dot(P(x, 1.45), radius=0.1, color=YELLOW)
        lab = T(name, 28, YELLOW).move_to(P(x, 3.2))
        return VGroup(stick, tip, lab)
    out["near_e"] = electrode(1.4, "near")
    out["far_e"] = electrode(-1.3, "far")
    return out


BX0 = -5.5
Y1, Y2 = -1.3, -2.6
BH = 0.9
N1, N2, BLK = 1.6, 3.76, 1.4


def bar1_parts():
    return rect(BX0, BX0 + N1, Y1, BH, BLUE), hatch(BX0 + N1, BX0 + N1 + BLK, Y1, BH)


def bar2_parts():
    return rect(BX0, BX0 + N2, Y2, BH, BLUE), hatch(BX0 + N2, BX0 + N2 + BLK, Y2, BH)


def spark(pos):
    g = VGroup(*[Line(pos + 0.12 * np.array([np.cos(a), np.sin(a), 0]), pos + 0.42 * np.array([np.cos(a), np.sin(a), 0]),
                      color=YELLOW, stroke_width=5) for a in np.linspace(0, 2 * np.pi, 8, endpoint=False)])
    return g


# timer bar for the leg (milliseconds, model)
BAR_Y = -3.15
MS = 0.62
BX = -5.9
SX0, SX1 = BX, BX + 8.3 * MS
TX1 = SX1 + 1.0 * MS
MX1 = TX1 + 8.3 * MS
EX1 = MX1 + 1.5 * MS


def leg_bar(y=BAR_Y, h=0.5):
    return VGroup(rect(SX0, SX1, y, h, BLUE), rect(SX1, TX1, y, h, WHITE, 1.0), rect(TX1, MX1, y, h, ORANGE),
                  hatch(MX1, EX1, y, h))


class S00Title(TitleCard):
    LESSON = "Nervous Control: A First Look"
    TITLE = "Every Response Has a Running Time"


import random as _random


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


_orig_setup = SpokenScene.setup


def _setup(self):
    _orig_setup(self)
    _add_motes(self)


SpokenScene.setup = _setup
NarratedScene.setup = lambda self: (Scene.setup(self), _add_motes(self) if type(self).__name__ == "S09Pause" else None)[0]


# ------------------------------------------------------------------ s01
class S01Hook(SpokenScene):
    def construct(self):
        thigh, quad, lower, cap = leg_parts()
        ham = hammer().shift(UR * 0.9)
        self.add(thigh, quad, lower, cap)
        self.play(FadeIn(ham), run_time=0.5)
        self.play(ham.animate.shift(DL * 0.9), run_time=0.4, rate_func=rush_into)
        self.at("leg")
        self.play(Rotate(lower, angle=0.9, about_point=K), ham.animate.shift(UR * 0.9), run_time=0.7, rate_func=rush_from)
        self.wait(0.6)
        self.play(Rotate(lower, angle=-0.9, about_point=K), run_time=1.3)
        self.at("How long")
        face = Circle(radius=0.9, stroke_color=TEXT, stroke_width=5, fill_color=BG, fill_opacity=1)
        btn = Rectangle(width=0.3, height=0.22, stroke_width=0, fill_color=TEXT, fill_opacity=1).next_to(face, UP, buff=0)
        hand = Line(ORIGIN, UP * 0.7, color=YELLOW, stroke_width=6)
        q = T("?", 56, YELLOW).move_to(DOWN * 0.15)
        sw = VGroup(face, btn, q, hand).move_to(P(5.4, 2.2))
        hand.put_start_and_end_on(sw[0].get_center(), sw[0].get_center() + UP * 0.7)
        hand.add_updater(lambda m, dt: m.rotate(-dt * 2.0, about_point=face.get_center()))
        self.play(FadeIn(sw, scale=0.7), run_time=0.6)
        self.add(ripple(face.get_center(), YELLOW, 0.95, 1.5, 2.0))
        self.finish()


# ------------------------------------------------------------------ s02
class S02Route(SpokenScene):
    def construct(self):
        thigh, quad, lower, cap = leg_parts()
        cord = cord_mob()
        self.add(thigh, quad, lower, cap)
        self.play(FadeIn(cord), run_time=0.8)
        self.at("five stations")
        dots = [station(i, False) for i in range(5)]
        for i, d in enumerate(dots):
            breathe(d, 2.4, 0.5, 1.0, i * 0.5, stroke=True)
        rings = [ripple(STN[i], CORD_GREY, 0.25, 1.0, 2.5, i * 0.5) for i in range(5)]
        self.add(*rings)
        self.play(LaggedStart(*[FadeIn(d, scale=0.5) for d in dots], lag_ratio=0.5), run_time=1.6)
        self.at("receptor")
        self.play(dots[0].animate.set_fill(TEAL, 1).set_stroke(TEAL), run_time=0.5)
        dots[0].clear_updaters(); dots[0].set_opacity(1)
        self.remove(rings[0])
        self.add(ripple(STN[0], TEAL, 0.25, 0.9))
        lab = T("receptor:\nmuscle spindle", 28, TEAL, line_spacing=0.8).move_to(P(5.2, 2.0))
        con = Line(STN[0] + P(0.3, 0.05, ), P(3.6, 1.8), color=TEAL, stroke_width=3)
        self.play(FadeIn(lab), Create(con), run_time=0.8)
        self.at("Then")
        sens = pline(SENS, BLUE, 8)
        gd = Dot(radius=0.15, color=GOLD).move_to(SENS[0])
        self.add(gd)
        self.play(Create(sens, rate_func=linear), MoveAlongPath(gd, sens, rate_func=linear), run_time=2.9)
        self.remove(gd)
        sl = T("sensory neuron", 28, BLUE).move_to(P(-1.2, 2.35))
        self.play(FadeIn(sl), dots[1].animate.set_fill(BLUE, 1).set_stroke(BLUE), run_time=0.5)
        dots[1].clear_updaters(); dots[1].set_opacity(1)
        self.remove(rings[1])
        self.at("spinal cord")
        cl = T("spinal cord", 28, CORD_GREY).move_to(CORD_C + P(0, -2.2))
        self.play(FadeIn(cl), cord.animate.set_stroke(WHITE), run_time=0.5)
        self.play(cord.animate.set_stroke(CORD_GREY), run_time=0.5)
        self.add(runner(SENS, GOLD, 2.4, 0.0))
        self.finish()


# ------------------------------------------------------------------ s03
class S03Route2(SpokenScene):
    def construct(self):
        thigh, quad, lower, cap = leg_parts()
        cord = cord_mob()
        sens = pline(SENS, BLUE, 8)
        dots = [station(0, True), station(1, True), station(2, False), station(3, False), station(4, False)]
        inner_b = inner_cord(True, False)
        self.add(thigh, quad, lower, cap, cord, sens, inner_b, *dots)
        self.add(ripple(STN[0], TEAL, 0.25, 0.9))
        labs, arrs = top_labels()
        self.play(FadeIn(labs[0]), FadeIn(arrs[0]), FadeIn(labs[1]), run_time=0.6)
        breathe(dots[2], 1.8, 0.4, 1.0, stroke=True)
        self.at("integrating")
        self.play(FadeIn(arrs[1]), FadeIn(labs[2]), cord.animate.set_stroke(WHITE), run_time=0.6)
        dots[2].clear_updaters()
        self.play(dots[2].animate.set_fill(CORD_GREY, 1).set_opacity(1), cord.animate.set_stroke(CORD_GREY), run_time=0.4)
        self.at("crosses one synapse")
        tk = tick()
        gd = Dot(radius=0.15, color=GOLD).move_to(W(-4.95, 1.7))
        self.add(gd)
        self.play(gd.animate.move_to(W(-5.4, 1.25)), run_time=0.5, rate_func=linear)
        self.play(FadeIn(tk, scale=2.0), gd.animate.move_to(W(-5.4, 0.55)), run_time=0.7, rate_func=linear)
        syn = T("1 synapse", 28, WHITE).move_to(W(-5.4, -1.6))
        self.play(FadeIn(syn), Flash(tk, color=WHITE, flash_radius=0.5), run_time=0.7)
        self.at("A motor neuron")
        self.play(FadeIn(arrs[2]), FadeIn(labs[3]), run_time=0.4)
        mot = pline(MOTOR, ORANGE, 8)
        ib = inner_cord(False, True)
        self.add(ib)
        self.play(Create(mot, rate_func=linear), gd.animate.move_to(MOTOR[0]), run_time=0.5, rate_func=linear)
        gd.clear_updaters()
        self.remove(gd)
        gd2 = Dot(radius=0.15, color=GOLD).move_to(MOTOR[0])
        self.add(gd2)
        self.play(MoveAlongPath(gd2, mot, rate_func=linear), run_time=2.0)
        self.remove(gd2)
        self.play(dots[3].animate.set_fill(ORANGE, 1).set_stroke(ORANGE), run_time=0.3)
        self.at("Then the effector")
        self.play(FadeIn(arrs[3]), FadeIn(labs[4]), dots[4].animate.set_fill(RED, 1).set_stroke(RED), run_time=0.5)
        self.at("contracts")
        self.play(quad.animate.set_fill(RED, 0.8).stretch_to_fit_width(2.5), Rotate(lower, angle=0.9, about_point=K),
                  run_time=0.6)
        self.wait(0.4)
        self.play(quad.animate.set_fill(RED, 0.28).stretch_to_fit_width(3.2), Rotate(lower, angle=-0.9, about_point=K),
                  run_time=0.9)
        self.finish()


# ------------------------------------------------------------------ neuron world (s04, s05)
NY = 0.2
BODY_C = P(-4.6, NY)
NODES = [-3.65] + [-3.45 + i * 1.15 + 1.0 + 0.075 for i in range(4)] + [2.3]


def neuron():
    body = Circle(radius=0.95, stroke_color=ORANGE, stroke_width=5, fill_color=ORANGE, fill_opacity=0.28).move_to(BODY_C)
    nucleus = Circle(radius=0.35, stroke_color=ORANGE, stroke_width=3, fill_color=ORANGE, fill_opacity=0.6).move_to(BODY_C)
    dend = VGroup()
    for dy in (1.9, 0.7, -0.7, -1.9):
        a = BODY_C + P(-0.85, dy * 0.3)
        b = P(-6.3, NY + dy)
        dend.add(pline([a, (a + b) / 2 + P(0, dy * 0.1), b], ORANGE, 6))
        dend.add(pline([(a + b) / 2 + P(0, dy * 0.1), b + P(0.4, 0.5 * np.sign(dy))], ORANGE, 4))
    axon = pline([P(-3.65, NY), P(2.3, NY)], ORANGE, 16)
    myelin = VGroup(*[RoundedRectangle(corner_radius=0.18, width=1.0, height=0.75, stroke_color="#E9D9C0", stroke_width=2,
                                       fill_color="#E9D9C0", fill_opacity=0.55).move_to(P(-3.45 + i * 1.15 + 0.5, NY))
                      for i in range(5)])
    terms = VGroup(*[pline([P(2.3, NY), P(2.9, NY + dy * 0.5), P(3.45, NY + dy)], ORANGE, 6) for dy in (0.95, 0.0, -0.95)])
    bulbs = VGroup(*[Dot(P(3.6, NY + dy), radius=0.16, color=ORANGE) for dy in (0.95, 0.0, -0.95)])
    muscle = RoundedRectangle(corner_radius=0.2, width=1.8, height=3.4, stroke_color=RED, stroke_width=4,
                              fill_color=RED, fill_opacity=0.3).move_to(P(5.15, NY))
    return dict(body=body, nucleus=nucleus, dend=dend, axon=axon, myelin=myelin, terms=terms, bulbs=bulbs, muscle=muscle)


def hop(s):
    k = len(NODES) - 1
    i = min(int(s * k), k - 1)
    f = s * k - i
    g = min(1, max(0, (f - 0.15) / 0.7))
    g = g * g * (3 - 2 * g)
    return NODES[i] + (NODES[i + 1] - NODES[i]) * g


def make_pulse(offset, period=6.8, travel=4.4):
    p = Rectangle(width=0.26, height=1.0, stroke_width=0, fill_color=BRIGHT_OR, fill_opacity=1).move_to(P(NODES[0], NY))
    p.t = offset

    def up(m, dt):
        m.t += dt
        s = (m.t % period) / travel
        if s <= 1:
            m.move_to(P(hop(s), NY)); m.set_opacity(1)
        else:
            m.set_opacity(0)
    p.add_updater(up)
    return p


class S04Neuron(SpokenScene):
    def construct(self):
        n = neuron()
        allg = VGroup(*n.values())
        tiny = allg.copy().scale(0.15).move_to(P(-0.5, NY))
        self.add(tiny)
        self.play(Transform(tiny, allg), run_time=2.4)
        self.remove(tiny)
        self.add(allg)
        ml = T("motor neuron", 32, ORANGE).move_to(P(-0.5, 2.9))
        self.play(FadeIn(ml), run_time=0.4)
        self.at("dendrites")
        self.play(FadeOut(ml), run_time=0.3)
        for k, dy in enumerate((1.9, 0.7, -0.7, -1.9)):
            self.add(runner([P(-6.3, NY + dy), BODY_C + P(-0.85, dy * 0.3)], GOLD, 2.0, k * 0.5, r=0.13))
        l1 = T("dendrites", 28, ORANGE).move_to(P(-5.2, 3.0))
        self.play(FadeIn(l1), n["dend"].animate.set_stroke(BRIGHT_OR, 9), run_time=0.7)
        self.play(n["dend"].animate.set_stroke(ORANGE, 6), run_time=0.8)
        self.at("cell body")
        l2 = T("cell body", 28, ORANGE).move_to(P(-4.6, -1.55))
        self.play(FadeOut(l1), FadeIn(l2), Indicate(n["body"], color=BRIGHT_OR, scale_factor=1.1), run_time=1.0)
        self.at("One long axon")
        l3 = T("axon", 28, ORANGE).move_to(P(-0.6, 1.1))
        self.play(FadeOut(l2), FadeIn(l3), run_time=0.5)
        self.at("carries the signal")
        self.add(make_pulse(0.0, 5.0, 3.6), make_pulse(2.5, 5.0, 3.6))
        self.at("sometimes a meter")
        br = DoubleArrow(P(-3.4, -0.95), P(2.3, -0.95), buff=0, color=TEXT, stroke_width=4, tip_length=0.2)
        bl = T("sometimes a metre or more", 28, TEXT).move_to(P(-0.55, -1.55))
        self.play(FadeOut(l3), GrowFromCenter(br), FadeIn(bl), run_time=0.9)
        self.at("terminals")
        l4 = T("terminals", 28, ORANGE).move_to(P(3.2, 1.9))
        self.play(FadeOut(br), FadeOut(bl), FadeIn(l4), n["terms"].animate.set_stroke(BRIGHT_OR, 9),
                  n["bulbs"].animate.set_color(BRIGHT_OR), run_time=0.8)
        self.finish()


class S05Impulse(SpokenScene):
    def construct(self):
        n = neuron()
        self.add(*n.values())
        # pulses: 4 identical bars hopping from node to node
        def hop(s):
            k = len(NODES) - 1
            i = min(int(s * k), k - 1)
            f = s * k - i
            g = min(1, max(0, (f - 0.15) / 0.7))
            g = g * g * (3 - 2 * g)
            return NODES[i] + (NODES[i + 1] - NODES[i]) * g
        pulses = []
        for j in range(4):
            p = Rectangle(width=0.26, height=1.0, stroke_width=0, fill_color=BRIGHT_OR, fill_opacity=1).move_to(P(NODES[0], NY))
            p.t = j * 1.7

            def up(m, dt):
                m.t += dt
                ph = m.t % 6.8
                s = ph / 4.4
                if s <= 1:
                    m.move_to(P(hop(s), NY)); m.set_opacity(1)
                else:
                    m.set_opacity(0)
            p.add_updater(up)
            pulses.append(p)
        self.add(*pulses)
        self.at("all or none")
        top = DashedLine(P(-3.6, NY + 0.5), P(2.3, NY + 0.5), color=BRIGHT_OR, stroke_width=3)
        bot = DashedLine(P(-3.6, NY - 0.5), P(2.3, NY - 0.5), color=BRIGHT_OR, stroke_width=3)
        ao = T("all-or-none", 30, BRIGHT_OR).move_to(P(-1.2, 1.45))
        self.play(Create(top), Create(bot), FadeIn(ao), run_time=1.0)
        self.at("short bare gaps")
        gaps = VGroup(*[Rectangle(width=0.15, height=0.9, stroke_width=0, fill_color=WHITE, fill_opacity=0.9).move_to(P(NODES[i], NY))
                        for i in range(1, 5)])
        self.play(FadeOut(ao), FadeIn(gaps), run_time=0.6)
        self.play(FadeOut(gaps), run_time=0.8)
        self.at("myelin")
        ml = T("myelin", 30, "#E9D9C0").move_to(P(-0.6, -1.0))
        pt = Line(P(-0.6, -0.8), P(-0.6, NY - 0.3), color="#E9D9C0", stroke_width=3)
        self.play(FadeIn(ml), Create(pt), run_time=0.7)
        self.at("At most synapses")
        self.play(FadeOut(ml), FadeOut(pt), FadeOut(top), FadeOut(bot), run_time=0.6)
        # transmitter dots crossing the gap
        for k, dy in enumerate((0.95, 0.0, -0.95)):
            for d in range(2):
                dot = Dot(radius=0.09, color=YELLOW).move_to(P(3.75, NY + dy))
                dot.t = k * 0.5 + d * 1.1

                def up(m, dt, dy=dy):
                    m.t += dt
                    f = (m.t % 2.2) / 2.2
                    m.move_to(P(3.75 + 0.65 * f, NY + dy)); m.set_opacity(min(1, f * 6, (1 - f) * 6))
                dot.add_updater(up)
                self.add(dot)
        self.at("releases")
        cs = T("chemical synapse", 30, YELLOW).move_to(P(4.4, 2.8))
        self.play(FadeIn(cs), run_time=0.6)
        self.finish()


# ------------------------------------------------------------------ Helmholtz (s06-s11)
class S06Helmholtz(SpokenScene):
    def construct(self):
        w = frog_world()
        yr = T("1850", 48, GOLD, font=TITLE_FONT).move_to(P(-5.3, 3.1))
        self.play(FadeIn(w["muscle"]), Create(w["nerve"], rate_func=linear), run_time=1.8)
        self.add(runner([P(3.4, 1.3), P(-5.6, 1.3)], GOLD, 3.0, 0.0))
        self.at("In 1850")
        self.play(FadeIn(yr), run_time=0.8)
        self.at("stimulated")
        self.play(FadeIn(w["near_e"], shift=DOWN * 0.3), run_time=0.6)
        self.at("nerve", nth=0)
        sp = spark(P(1.4, 1.3))
        pulse = Dot(radius=0.17, color=GOLD).move_to(P(1.4, 1.3))
        b1, h1 = bar1_parts()
        self.add(pulse)
        self.play(FadeIn(sp, run_time=0.2), run_time=0.2)
        self.play(MoveAlongPath(pulse, pline([P(1.4, 1.3), P(3.4, 1.3)], GOLD), rate_func=linear),
                  GrowFromEdge(b1, LEFT, rate_func=linear), FadeOut(sp), run_time=1.25)
        self.remove(pulse)
        self.play(w["muscle"].animate.stretch_to_fit_width(1.8), FadeIn(h1), run_time=0.5)
        self.play(w["muscle"].animate.stretch_to_fit_width(2.4), run_time=0.5)
        self.finish()


def far_scene_base(scene, near_dim=True):
    w = frog_world()
    b1, h1 = bar1_parts()
    scene.add(w["muscle"], w["nerve"], w["near_e"], b1, h1)
    w["near_e"].set_opacity(0.45)
    return w, b1, h1


class S07Far(SpokenScene):
    def construct(self):
        w, b1, h1 = far_scene_base(self)
        self.add(runner([P(3.4, 1.3), P(-5.6, 1.3)], GOLD, 3.0, 0.0, 0.1))
        self.at("farther up")
        self.play(FadeIn(w["far_e"], shift=DOWN * 0.3), run_time=0.7)
        self.at("and timed")
        b2, h2 = bar2_parts()
        sp = spark(P(-1.3, 1.3))
        pulse = Dot(radius=0.17, color=GOLD).move_to(P(-1.3, 1.3))
        self.add(pulse)
        self.play(FadeIn(sp), run_time=0.2)
        self.play(MoveAlongPath(pulse, pline([P(-1.3, 1.3), P(3.4, 1.3)], GOLD), rate_func=linear),
                  GrowFromEdge(b2, LEFT, rate_func=linear), FadeOut(sp), run_time=2.94)
        self.remove(pulse)
        self.play(w["muscle"].animate.stretch_to_fit_width(1.8), FadeIn(h2), run_time=0.4)
        self.play(w["muscle"].animate.stretch_to_fit_width(2.4), run_time=0.4)
        self.at("later")
        e1, e2 = BX0 + N1 + BLK, BX0 + N2 + BLK
        d1 = DashedLine(P(e1, Y1 + 0.3), P(e1, Y2 - 0.3), color=YELLOW, stroke_width=3)
        d2 = DashedLine(P(e2, Y1 - 0.3), P(e2, Y2 + 0.3), color=YELLOW, stroke_width=3)
        ar = DoubleArrow(P(e1, Y1 + 0.0), P(e2, Y1 + 0.0), buff=0, color=YELLOW, stroke_width=4, tip_length=0.2).shift(UP * 0.55)
        self.play(Create(d1), Create(d2), run_time=0.8)
        self.play(FadeIn(ar), run_time=0.6)
        self.finish()


def full_frog(scene, ends=True):
    w = frog_world()
    b1, h1 = bar1_parts()
    b2, h2 = bar2_parts()
    w["near_e"].set_opacity(0.45)
    scene.add(w["muscle"], w["nerve"], w["near_e"], w["far_e"], b1, h1, b2, h2)
    e1, e2 = BX0 + N1 + BLK, BX0 + N2 + BLK
    d1 = DashedLine(P(e1, Y1 + 0.3), P(e1, Y2 - 0.3), color=YELLOW, stroke_width=3)
    d2 = DashedLine(P(e2, Y1 - 0.3), P(e2, Y2 + 0.3), color=YELLOW, stroke_width=3)
    scene.add(d1, d2)
    return w, b1, h1, b2, h2, d1, d2


class S08Predict(SpokenScene):
    def construct(self):
        w, b1, h1, b2, h2, d1, d2 = full_frog(self)
        breathe(h1, 2.0, 0.5, 1.0)
        breathe(h2, 2.0, 0.5, 1.0)
        self.at("junction")
        lab = T("junction + muscle", 30, GREY).move_to(P(1.4, Y1))
        ln = Line(P(BX0 + N1 + BLK + 0.1, Y1), P(-0.5, Y1), color=GREY, stroke_width=3)
        self.play(FadeIn(lab), Create(ln), run_time=0.8)
        self.at("nerve alone")
        self.play(Indicate(b1, color=WHITE, scale_factor=1.08), Indicate(b2, color=WHITE, scale_factor=1.08), run_time=1.2)
        self.at("Which part")
        q = T("?", 80, YELLOW, weight=BOLD).move_to(P((BX0 + N1 + BLK + BX0 + N2 + BLK) / 2, (Y1 + Y2) / 2))
        self.play(FadeIn(q, scale=1.5), run_time=0.6)
        self.add(breathe(q, 1.6, 0.6, 1.0))
        self.finish()


class S09Pause(NarratedScene):
    def construct(self):
        w, b1, h1, b2, h2, d1, d2 = full_frog(self)
        lab = T("junction + muscle", 30, GREY).move_to(P(1.4, Y1))
        ln = Line(P(BX0 + N1 + BLK + 0.1, Y1), P(-0.5, Y1), color=GREY, stroke_width=3)
        q = T("?", 80, YELLOW, weight=BOLD).move_to(P((BX0 + N1 + BLK + BX0 + N2 + BLK) / 2, (Y1 + Y2) / 2))
        self.add(lab, ln, q)
        breathe(h1, 1.6, 0.05, 1.0)
        breathe(h2, 1.6, 0.05, 1.0, 0.3)
        breathe(q, 1.2, 0.1, 1.0)
        self.add(runner([P(-1.3, 1.3), P(3.4, 1.3)], GOLD, 2.0, 0.0, r=0.25))
        self.finish()


class S10Reveal(SpokenScene):
    def construct(self):
        w, b1, h1, b2, h2, d1, d2 = full_frog(self)
        self.add(runner([P(-1.3, 1.3), P(1.4, 1.3)], GOLD, 1.6, 0.0, r=0.25))
        breathe(h1, 1.6, 0.1, 1.0)
        breathe(h2, 1.6, 0.1, 1.0, 0.3)
        q = T("?", 80, YELLOW, weight=BOLD).move_to(P((BX0 + N1 + BLK + BX0 + N2 + BLK) / 2, (Y1 + Y2) / 2))
        lab = T("junction + muscle", 30, GREY).move_to(P(1.4, Y1))
        ln = Line(P(BX0 + N1 + BLK + 0.1, Y1), P(-0.5, Y1), color=GREY, stroke_width=3)
        self.add(lab, ln, q)
        self.at("The difference")
        self.play(FadeOut(q), Indicate(d1, color=WHITE), Indicate(d2, color=WHITE), run_time=1.2)
        self.at("so they cancel")
        h1.clear_updaters(); h2.clear_updaters(); h1.set_opacity(1); h2.set_opacity(1)
        shared = rect(BX0, BX0 + N1, Y2, BH, BLUE)
        self.add(shared)
        self.play(FadeOut(h1), FadeOut(h2), FadeOut(b1), FadeOut(lab), FadeOut(ln), FadeOut(d1), FadeOut(d2),
                  FadeOut(w["near_e"][2]), FadeOut(w["far_e"][2]), run_time=1.2)
        self.play(FadeOut(shared), run_time=0.8)
        self.at("extra")
        extra_x0 = BX0 + N1
        extra_x1 = BX0 + N2
        ex = rect(extra_x0, extra_x1, Y2, BH, BLUE, 1.0)
        # b2 stays for the shared part; replace by bright extra piece
        self.remove(b2)
        shared2 = rect(BX0, extra_x0, Y2, BH, BLUE)
        self.add(shared2)
        self.add(ex)
        self.play(FadeOut(shared2), ex.animate.set_stroke(WHITE, 4), run_time=0.9)
        dl = T("extra delay", 30, BLUE).move_to(P((extra_x0 + extra_x1) / 2, Y2 - 0.65))
        self.play(FadeIn(dl), run_time=0.5)
        self.at("extra length")
        br = Brace(Line(P(-1.3, 0.9), P(1.4, 0.9)), DOWN, color=YELLOW)
        bt = T("extra length", 30, YELLOW).next_to(br, DOWN, buff=0.1)
        link = DashedLine(br.get_bottom() + DOWN * 0.45, P((extra_x0 + extra_x1) / 2, Y2 + 0.45), color=YELLOW, stroke_width=3)
        self.play(GrowFromCenter(br), FadeIn(bt), run_time=0.8)
        self.play(Create(link), run_time=0.8)
        self.finish()


class S11Speed(SpokenScene):
    def construct(self):
        w = frog_world()
        extra_x0, extra_x1 = BX0 + N1, BX0 + N2
        ex = rect(extra_x0, extra_x1, Y2, BH, BLUE, 1.0)
        ex.set_stroke(WHITE, 4)
        w["near_e"][2].set_opacity(0); w["far_e"][2].set_opacity(0)
        br = Brace(Line(P(-1.3, 0.9), P(1.4, 0.9)), DOWN, color=YELLOW)
        bt = T("extra length", 30, YELLOW).next_to(br, DOWN, buff=0.1)
        self.add(w["muscle"], w["nerve"], w["near_e"], w["far_e"], ex, br, bt)
        self.add(runner([P(-5.6, 1.3), P(3.4, 1.3)], GOLD, 9.0 / 2.2, 0.0))
        eq = M("v = difference in distance / difference in time", 28, TEXT)
        eq.move_to(P(0.3, -0.5))
        fit(eq, 12.4)
        self.play(Write(eq), run_time=2.4)
        self.at("Helmholtz found")
        res = T("frog nerve: a few tens of m per s", 32, YELLOW).move_to(P(0.3, -1.4))
        self.play(FadeIn(res, shift=UP * 0.1), run_time=0.8)
        self.at("car")
        body = RoundedRectangle(corner_radius=0.12, width=1.4, height=0.42, stroke_color=TEXT, stroke_width=3,
                                fill_color=GREY, fill_opacity=0.7)
        cab = RoundedRectangle(corner_radius=0.1, width=0.75, height=0.32, stroke_color=TEXT, stroke_width=3,
                               fill_color=GREY, fill_opacity=0.7).next_to(body, UP, buff=-0.02)
        wh = VGroup(Circle(radius=0.15, stroke_color=TEXT, fill_color=BG, fill_opacity=1, stroke_width=3).move_to(body.get_center() + P(-0.4, -0.2)),
                    Circle(radius=0.15, stroke_color=TEXT, fill_color=BG, fill_opacity=1, stroke_width=3).move_to(body.get_center() + P(0.4, -0.2)))
        car = VGroup(body, cab, wh).move_to(P(-6.2, -3.3))
        car.t = 0.0

        def up(m, dt):
            m.t += dt
            x = -6.0 + (m.t * 2.2) % 12.0
            m.move_to(P(x, -3.3))
        car.add_updater(up)
        self.play(FadeIn(car), run_time=0.4)
        self.finish()


# ------------------------------------------------------------------ s12-s14 back to the leg
def leg_world_full(scene, kicked=False):
    thigh, quad, lower, cap = leg_parts()
    cord = cord_mob()
    sens = pline(SENS, BLUE, 8)
    mot = pline(MOTOR, ORANGE, 8)
    dots = [station(i, True) for i in range(5)]
    tk = tick()
    ib = inner_cord()
    grp = VGroup(thigh, quad, lower, cap, cord, sens, mot, ib, tk, *dots)
    scene.add(grp)
    return grp, dict(lower=lower, quad=quad)


class S12Sum(SpokenScene):
    def construct(self):
        thigh, quad, lower, cap = leg_parts()
        cord = cord_mob()
        sens = pline(SENS, BLUE, 8)
        mot = pline(MOTOR, ORANGE, 8)
        dots = [station(i, True) for i in range(5)]
        tk = tick()
        ib = inner_cord()
        grp = VGroup(thigh, quad, lower, cap, cord, sens, mot, ib, *dots)
        self.play(FadeIn(grp), run_time=0.8)
        self.add(ripple(STN[0], TEAL, 0.25, 0.9))
        # bar pieces
        b_s = rect(SX0, SX1, BAR_Y, 0.5, BLUE)
        b_t = rect(SX1, TX1, BAR_Y, 0.5, WHITE, 1.0)
        b_m = rect(TX1, MX1, BAR_Y, 0.5, ORANGE)
        b_e = hatch(MX1, EX1, BAR_Y, 0.5)
        self.at("Each axon's time")
        gd = Dot(radius=0.17, color=GOLD).move_to(SENS[0])
        self.add(gd)
        self.play(MoveAlongPath(gd, sens, rate_func=linear), GrowFromEdge(b_s, LEFT, rate_func=linear), run_time=1.8)
        self.at("length divided")
        ls = T("length / speed", 28, BLUE).move_to(P((SX0 + SX1) / 2, BAR_Y + 0.55))
        self.play(FadeIn(ls), run_time=0.5)
        self.add(ripple(STN[2], CORD_GREY, 0.3, 0.9))
        self.at("each synapse")
        self.add(tk)
        self.play(FadeIn(b_t, scale=2.0), Flash(tk, color=WHITE, flash_radius=0.5), run_time=0.6)
        lt = T("about 1 ms, model", 28, WHITE).move_to(P((SX1 + TX1) / 2 + 0.2, BAR_Y + 1.15))
        lt_l = Line(P((SX1 + TX1) / 2, BAR_Y + 0.3), P((SX1 + TX1) / 2 + 0.1, BAR_Y + 0.9), color=WHITE, stroke_width=3)
        self.play(FadeIn(lt), Create(lt_l), run_time=0.5)
        gd2 = Dot(radius=0.17, color=GOLD).move_to(MOTOR[0])
        self.add(gd2)
        self.play(MoveAlongPath(gd2, mot, rate_func=linear), GrowFromEdge(b_m, LEFT, rate_func=linear), run_time=1.8)
        lm = T("length / speed", 28, ORANGE).move_to(P((TX1 + MX1) / 2, BAR_Y + 0.55))
        self.play(FadeIn(lm), FadeOut(lt), FadeOut(lt_l), run_time=0.4)
        self.at("The junction")
        self.play(FadeIn(b_e), run_time=0.5)
        le = T("junction + muscle", 24, GREY).move_to(P(5.45, BAR_Y + 1.0))
        self.play(FadeIn(le), Rotate(lower, angle=0.9, about_point=K), run_time=0.7)
        self.play(Rotate(lower, angle=-0.9, about_point=K), run_time=0.9)
        self.finish()


class S13Total(SpokenScene):
    def construct(self):
        thigh, quad, lower, cap = leg_parts()
        cord = cord_mob()
        sens = pline(SENS, BLUE, 8)
        mot = pline(MOTOR, ORANGE, 8)
        dots = [station(i, True) for i in range(5)]
        tk = tick()
        ib = inner_cord()
        world = VGroup(thigh, quad, lower, cap, cord, sens, mot, ib, tk, *dots)
        bar = leg_bar()
        self.add(world, bar)
        BY = 0.9
        self.play(FadeOut(world), bar.animate.shift(UP * (BY - BAR_Y)), run_time=1.3)
        self.add(runner([P(SX0, BY), P(EX1, BY)], GOLD, 4.0, 0.0, r=0.17))
        mid = lambda a, b: (a + b) / 2
        l1 = T("sensory 8.3 ms", 28, BLUE).move_to(P(mid(SX0, SX1), BY + 0.7))
        l2 = T("synapse 1 ms", 28, WHITE).move_to(P(mid(SX1, TX1) + 0.1, BY + 1.45))
        l2l = Line(P(mid(SX1, TX1), BY + 0.3), P(mid(SX1, TX1) + 0.1, BY + 1.15), color=WHITE, stroke_width=3)
        l3 = T("motor 8.3 ms", 28, ORANGE).move_to(P(mid(TX1, MX1) + 0.3, BY + 0.7))
        l4 = T("junction + muscle\nabout 1.5 ms", 28, GREY, line_spacing=0.8).move_to(P(5.0, BY - 0.8))
        self.at("legs add up")
        self.play(FadeIn(l1), FadeIn(l2), Create(l2l), FadeIn(l3), FadeIn(l4), run_time=1.0)
        self.at("just under")
        tot = T("total about 19 ms", 34, TEXT).move_to(P(-0.2, -0.45))
        self.play(FadeIn(tot), run_time=0.6)
        self.at("measured")
        ms = T("measured: tap to muscle's electrical\nresponse, about 20 ms", 30, YELLOW, line_spacing=0.8).move_to(P(0.0, -1.5))
        self.play(FadeIn(ms), run_time=0.8)
        self.at("tap")
        sl = Rectangle(width=0.45, height=0.5, stroke_color=GREY, stroke_width=3, fill_opacity=0).move_to(P(SX0 - 0.23, BY))
        sl.set_stroke(GREY, 3)
        nd = T("not drawn: tap to spindle firing (small)", 28, GREY)
        nd.move_to(P(-6.6 + nd.width / 2, -2.6))
        ndl = Line(P(SX0 - 0.23, BY - 0.3), P(-6.2, -2.3), color=GREY, stroke_width=3)
        self.play(Create(sl), run_time=0.5)
        self.play(FadeIn(nd), Create(ndl), run_time=0.8)
        self.at("kick")
        self.play(FadeOut(nd), FadeOut(ndl), FadeOut(sl), run_time=0.5)
        ka = Arrow(P(EX1 + 0.05, BY), P(6.75, BY), buff=0, color=GREY, stroke_width=5, tip_length=0.2)
        kt = T("visible kick:\nlater", 28, GREY, line_spacing=0.8).move_to(P(5.6, BY + 0.95))
        self.play(Create(ka), FadeIn(kt), run_time=0.8)
        self.at("Nearly all")
        ax = T("axons: about 87% of the model sum", 32, TEXT).move_to(P(0.0, -2.5))
        self.play(FadeOut(ka), FadeOut(kt), FadeOut(tot), bar[1].animate.set_opacity(0.3), bar[3].animate.set_opacity(0.3),
                  FadeOut(l2), FadeOut(l2l), FadeOut(l4), FadeIn(ax), run_time=0.9)
        self.play(Indicate(bar[0], color=WHITE, scale_factor=1.05), Indicate(bar[2], color=WHITE, scale_factor=1.05), run_time=1.2)
        self.finish()


class S14Rule(SpokenScene):
    def construct(self):
        BY = 0.9
        old = leg_bar(BY)
        self.add(old)
        # five stations
        dots = VGroup(*[Circle(radius=0.28, stroke_color=STN_COL[i], fill_color=STN_COL[i], fill_opacity=1, stroke_width=3)
                        for i in range(5)])
        dots.arrange(RIGHT, buff=1.1).move_to(P(0, 3.0))
        lines = VGroup(*[Line(dots[i].get_right(), dots[i + 1].get_left(), color=GOLD, stroke_width=4) for i in range(4)])
        tr = ValueTracker(0.0)
        X0 = -4.6
        YB = 1.5

        def mk():
            sw = 3.0 + 2.0 * tr.get_value()
            return VGroup(rect(X0, X0 + sw, YB, 0.5, BLUE), rect(X0 + sw, X0 + sw + 0.45, YB, 0.5, WHITE, 1.0),
                          rect(X0 + sw + 0.45, X0 + sw + 3.45, YB, 0.5, ORANGE),
                          hatch(X0 + sw + 3.45, X0 + sw + 4.15, YB, 0.5))
        new = mk()
        self.play(ReplacementTransform(old, new), FadeIn(dots), FadeIn(lines), run_time=1.6)
        self.remove(new)
        bar = always_redraw(mk)
        self.add(bar)
        self.at("its time")
        e1 = T("response time ≈ sum of (length ÷ speed) for each axon", 32, TEXT)
        e2 = T("+ synapses in the cord × about 1 ms", 32, TEXT)
        e3 = T("+ end delays", 32, TEXT)
        eq = VGroup(e1, e2, e3).arrange(DOWN, buff=0.28, aligned_edge=LEFT).move_to(P(0, -0.65))
        fit(eq, 12.2)
        self.play(Write(e1), run_time=1.6)
        self.play(Write(e2), run_time=1.0)
        self.play(Write(e3), run_time=0.6)
        tag = T("simple model", 28, TEAL).move_to(P(5.0, -2.1))
        self.at("Change a length")
        track = Line(P(-3.0, -2.7), P(3.0, -2.7), color=GREY, stroke_width=5)
        knob = Dot(radius=0.2, color=YELLOW).move_to(P(-3.0, -2.7))
        knob.add_updater(lambda m: m.move_to(P(-3.0 + 6.0 * tr.get_value(), -2.7)))
        sl = T("length", 28, BLUE).move_to(P(-4.6, -2.7))
        self.play(FadeIn(track), FadeIn(knob), FadeIn(sl), FadeIn(tag), run_time=0.6)
        self.play(tr.animate.set_value(1.0), run_time=2.0)
        self.play(tr.animate.set_value(0.2), run_time=1.5)
        self.play(tr.animate.set_value(1.0), run_time=1.5)
        self.finish()


class S15End(EndCard):
    LINE = "A response is a route; its time sums its legs."
