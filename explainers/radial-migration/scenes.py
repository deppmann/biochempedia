"""Radial migration: the front reaches, the nucleus follows  (Biochemistrypedia explainer)

Timed to the SPOKEN words: every self.at("...") cue waits for that phrase in audio/words.json.

COLOR MAP (one color per concept, whole video)
  BLUE   = the migrating neuron (soma outline, leading process, swelling)
  ORANGE = the nucleus
  YELLOW = centrosome and Golgi
  GREEN  = radial glial fiber (the ladder)
  TEAL   = microtubules (the cage)
  PURPLE = dynein, and LIS1 (its regulator)
  PINK   = myosin II
  RED    = stalled / blocked / the question mark of a failure
  GREY   = ventricle and outer surface, labels, de-emphasized
"""
import numpy as np
from bp_style import *  # noqa: F401,F403

ORANGE = "#F29E4C"
PURPLE = "#B58CD9"
PINK = "#E87FB0"
NEURON_FILL = "#16303c"   # BLUE at about 25 percent over the background, but opaque


# ---------------------------------------------------------------------------------------------
# helpers
# ---------------------------------------------------------------------------------------------
def arr(a, b, color=GREY, w=4, tip=0.2):
    return Arrow(a, b, buff=0.06, color=color, stroke_width=w, tip_length=tip,
                 max_tip_length_to_length_ratio=0.5, max_stroke_width_to_length_ratio=14)


def lab_left(text, color, x, y, tip, size=26):
    """text whose right edge sits at x, with an arrow to `tip`."""
    t = T(text, size, color)
    t.move_to([x - t.width / 2, y, 0])
    a = arr([x + 0.12, y, 0], tip, color)
    return VGroup(t, a)


def lab_right(text, color, x, y, tip, size=26):
    """text whose left edge sits at x, with an arrow to `tip`."""
    t = T(text, size, color)
    t.move_to([x + t.width / 2, y, 0])
    a = arr([x - 0.12, y, 0], tip, color)
    return VGroup(t, a)


def bar(y, x0=-2.6, x1=2.6):
    return RoundedRectangle(corner_radius=0.08, width=x1 - x0, height=0.2, stroke_color=GREY, stroke_width=3,
                            fill_color=GREY, fill_opacity=0.45).move_to([(x0 + x1) / 2, y, 0])


def fiber(x, y0=-3.0, y1=3.0, rungs=False, width=5):
    g = VGroup(Line([x, y0, 0], [x, y1, 0], color=GREEN, stroke_width=width))
    if rungs:
        for y in np.arange(y0 + 0.2, y1, 0.6):
            g.add(Line([x - 0.14, y, 0], [x + 0.14, y, 0], color=GREEN, stroke_width=2.5, stroke_opacity=0.7))
    return g


def chipfix(text, color, size=26):
    c = chip(text, color, size=size)
    back = RoundedRectangle(corner_radius=0.14, width=c[0].width, height=c[0].height, stroke_width=0,
                            fill_color=BG, fill_opacity=1).move_to(c[0])
    return VGroup(back, *c)


def ring(pos, color, r=0.34):
    return Circle(radius=r, stroke_color=color, stroke_width=5).move_to(pos)


class Cell:
    """A migrating neuron drawn from a few trackers (local y, scaled by sc, placed at x, y0)."""
    RX, RY = 0.55, 0.7   # soma half-width and half-height

    def __init__(self, x=0.0, y0=0.0, sc=1.0, soma=-2.4, tip=-0.4, tail=-3.35, ws=0.0, wy=-0.4,
                 cs=-1.45, op=0.0, cs_op=0.0, gg_op=0.0, nuc_op=1.0):
        self.x, self.y0, self.sc = x, y0, sc
        self.t = {k: ValueTracker(v) for k, v in dict(soma=soma, tip=tip, tail=tail, ws=ws, wy=wy, cs=cs,
                                                      op=op, cs_op=cs_op, gg_op=gg_op, nuc_op=nuc_op).items()}
        self.mob = always_redraw(self.build)

    def P(self, x, y):
        return np.array([self.x + self.sc * x, self.y0 + self.sc * y, 0.0])

    def v(self, k):
        return self.t[k].get_value()

    def set(self, **kw):
        for k, val in kw.items():
            self.t[k].set_value(val)

    def to(self, **kw):
        return [self.t[k].animate.set_value(val) for k, val in kw.items()]

    def build(self):
        sc = self.sc
        op = self.v("op")
        if op < 0.02:
            return VGroup()
        soma, tip, tail = self.v("soma"), self.v("tip"), self.v("tail")
        ws, wy, cs = self.v("ws"), self.v("wy"), self.v("cs")
        lw = 10 * sc
        g = VGroup()
        if tail < soma - self.RY - 0.02:
            g.add(Line(self.P(0, tail), self.P(0, soma - self.RY), color=BLUE, stroke_width=lw))
            g.add(Dot(self.P(0, tail), radius=0.09 * sc, color=BLUE))
        if tip > soma + self.RY + 0.02:
            g.add(Line(self.P(0, soma + self.RY), self.P(0, tip), color=BLUE, stroke_width=lw))
            g.add(Dot(self.P(0, tip), radius=0.13 * sc, color=BLUE))
        if ws > 0.03:
            g.add(Ellipse(width=1.0 * ws * sc, height=2.0 * ws * sc, stroke_color=BLUE, stroke_width=5 * sc,
                          fill_color=NEURON_FILL, fill_opacity=1).move_to(self.P(0, wy)))
        g.add(Ellipse(width=2 * self.RX * sc, height=2 * self.RY * sc, stroke_color=BLUE, stroke_width=5 * sc,
                      fill_color=NEURON_FILL, fill_opacity=1).move_to(self.P(0, soma)))
        g.add(Ellipse(width=0.74 * sc, height=1.0 * sc, stroke_color=ORANGE, stroke_width=4 * sc,
                      fill_color=ORANGE, fill_opacity=0.55 * self.v("nuc_op")).set_stroke(opacity=self.v("nuc_op"))
              .move_to(self.P(0, soma)))
        cso, ggo = self.v("cs_op"), self.v("gg_op")
        if cso > 0.02:
            g.add(Dot(self.P(0, cs), radius=0.11 * sc, color=YELLOW).set_opacity(cso))
        if ggo > 0.02:
            for dy in (0.30, 0.42, 0.54):
                g.add(Line(self.P(-0.2, cs + dy), self.P(0.2, cs + dy), color=YELLOW,
                           stroke_width=max(2.5, 5 * sc), stroke_opacity=ggo))
        if op < 0.99:
            for m in g.family_members_with_points():
                m.set_stroke(opacity=m.get_stroke_opacity() * op)
                m.set_fill(opacity=m.get_fill_opacity() * op)
        return g

    # the two strokes, as animation lists ---------------------------------------------------
    def stroke_one(self, soma):
        """leading process extends, swelling forms ahead of the nucleus, centrosome and Golgi move in."""
        return dict(tip=soma + 3.5, ws=1.0, wy=soma + 2.0, cs=soma + 2.35)

    def stroke_two(self, soma):
        return dict(soma=soma + 1.5, ws=0.0, tail=soma + 1.5 - 0.95)


class S00Title(TitleCard):
    LESSON = "Radial migration"
    TITLE = "The Front Reaches, the Nucleus Follows"


# ---------------------------------------------------------------------------------------------
class S01Question(SpokenScene):
    """a cell with no legs at the bottom of a thick wall; its front reaches while its nucleus stays: what pulls it?"""

    def construct(self):
        cell = Cell(x=0, y0=0, soma=-2.2, tip=-1.1, tail=-2.88, op=0)
        self.add(cell.mob)
        self.play(cell.t["op"].animate.set_value(1), run_time=0.8)

        vent = bar(-3.3)
        vent_l = T("ventricle", 26, GREY).move_to([4.3, -3.3, 0])
        self.at("born beside")
        self.play(Create(vent), FadeIn(vent_l, shift=LEFT * 0.15), run_time=0.8)

        outer = bar(3.3)
        outer_l = T("outer surface", 26, GREY).move_to([4.6, 3.3, 0])
        self.at("outer surface")
        self.play(Create(outer), FadeIn(outer_l, shift=LEFT * 0.15), run_time=0.8)

        span = DoubleArrow([-3.5, -3.1, 0], [-3.5, 3.1, 0], color=GREY, stroke_width=4, tip_length=0.22, buff=0)
        span_l = T("thick wall", 26, GREY).move_to([-5.0, 0, 0])
        self.at("thick wall")
        self.play(GrowFromCenter(span), FadeIn(span_l), run_time=0.9)

        fib = fiber(0.62, -3.2, 3.2, width=6)
        fib_l = T("radial glial fiber", 26, GREEN).move_to([3.1, 0.9, 0])
        self.at("radial glial")
        self.play(Create(fib), run_time=1.2)
        self.play(FadeIn(fib_l, shift=LEFT * 0.15), run_time=0.5)

        self.at("front reaching")
        self.play(*cell.to(tip=1.5), run_time=1.8)
        nuc_l = lab_left("nucleus", ORANGE, -1.0, -2.2, [-0.45, -2.2, 0])
        self.at("stays behind")
        halo = Ellipse(width=1.2, height=1.5, stroke_color=ORANGE, stroke_width=4).move_to(cell.P(0, -2.2))
        self.play(FadeIn(nuc_l), Create(halo), run_time=0.7)
        q = T("?", 120, RED, weight=BOLD).move_to([-1.6, -0.6, 0])
        self.at("What pulls")
        self.play(FadeIn(q, scale=0.6), run_time=0.6)
        self.finish()


# ---------------------------------------------------------------------------------------------
class S02Ladder(SpokenScene):
    """the wall strung with parallel fibers; a neuron climbs one in stops and goes while its tip probes out of step."""

    def construct(self):
        vent = bar(-3.0, -5.8, 5.8)
        outer = bar(3.0, -5.8, 5.8)
        vent_l = T("ventricle", 24, GREY).move_to([-4.8, -3.45, 0])
        outer_l = T("outer surface", 24, GREY).move_to([-4.6, 3.45, 0])
        self.add(vent, outer, vent_l, outer_l)

        xs = [-4.6, -2.6, 0.62, 2.8, 4.7]
        fibs = [fiber(x, -2.9, 2.9, rungs=True) for x in xs]
        self.at("keep a long")
        self.play(Create(fibs[2]), run_time=1.4)
        others = [f for i, f in enumerate(fibs) if i != 2]
        self.at("parallel")
        self.play(LaggedStart(*[Create(f) for f in others], lag_ratio=0.25), run_time=1.8)

        cell = Cell(x=0, y0=0, soma=-2.0, tip=-0.9, tail=-2.9, op=0)
        self.add(cell.mob)
        self.at("can climb")
        self.play(cell.t["op"].animate.set_value(1), run_time=0.7)

        # in culture: the wall goes away; one glial fiber and the neuron sit on a coverslip
        slip = RoundedRectangle(corner_radius=0.2, width=7.4, height=6.3, stroke_color=GREY, stroke_width=3,
                                fill_color=GREY, fill_opacity=0.08).move_to([0.3, -0.1, 0])
        slip.set_z_index(-5)
        slip_l = T("coverslip", 26, GREY).move_to([2.9, -2.85, 0])
        cap = T("mouse neurons from the cerebellum, in culture", 26, GREY).move_to([0.3, 3.55, 0])
        self.at("In culture")
        self.play(FadeOut(vent), FadeOut(outer), FadeOut(vent_l), FadeOut(outer_l), *[FadeOut(f) for f in others],
                  run_time=0.8)
        self.play(FadeIn(slip), FadeIn(slip_l), FadeIn(cap, shift=DOWN * 0.1), run_time=0.8)

        # stop and go: the body steps; the tip probes on its own schedule
        go = T("go", 30, GREEN, weight=BOLD).move_to([-1.5, -0.4, 0])
        stop = T("stop", 30, RED, weight=BOLD).move_to([-1.5, -0.4, 0])
        self.at("They moved")
        self.play(FadeIn(go), *cell.to(soma=-1.0, tail=-1.9), run_time=0.7)
        self.play(ReplacementTransform(go, stop), run_time=0.2)
        self.wait(0.3)
        go2 = T("go", 30, GREEN, weight=BOLD).move_to([-1.5, -0.4, 0])
        self.play(ReplacementTransform(stop, go2), *cell.to(soma=0.0, tail=-0.9), run_time=0.7)
        stop2 = T("stop", 30, RED, weight=BOLD).move_to([-1.5, -0.4, 0])
        self.play(ReplacementTransform(go2, stop2), run_time=0.2)
        self.at("extended and retracted")
        self.play(FadeOut(stop2), *cell.to(tip=2.2), run_time=0.7)
        self.play(*cell.to(tip=0.9), run_time=0.6)
        self.at("out of step")
        self.play(*cell.to(tip=2.4), run_time=0.7)
        self.play(*cell.to(tip=1.2), run_time=0.6)
        self.finish()


# ---------------------------------------------------------------------------------------------
def stroke_chips(hot=None, x=5.0):
    c1 = chipfix("stroke 1", TEXT if hot == 1 else GREY, 28).move_to([x, 1.0, 0])
    c2 = chipfix("stroke 2", TEXT if hot == 2 else GREY, 28).move_to([x, -1.0, 0])
    return c1, c2


def lit(c, on):
    col = TEXT if on else GREY
    return [c[1].animate.set_stroke(col).set_fill(col, 0.16), c[2].animate.set_color(col)]


class S03StrokeOne(SpokenScene):
    """zoom on the cell; stroke one: the process extends, a swelling forms, centrosome and Golgi move in."""
    SC, Y0 = 1.15, 0.45

    def construct(self):
        sc = self.SC
        fib = fiber(0.62 * sc, -3.4, 3.4, rungs=True)
        self.add(fib)
        cell = Cell(x=0, y0=self.Y0, sc=sc, soma=-2.4, tip=-0.4, tail=-3.35, op=0)
        self.add(cell.mob)
        P = cell.P
        nuc_l = lab_left("nucleus", ORANGE, -1.1, P(0, -2.4)[1], [-0.72, P(0, -2.4)[1], 0])
        self.play(cell.t["op"].animate.set_value(1), FadeIn(nuc_l), run_time=0.8)
        self.at("nucleokinesis")
        nk = T("nucleokinesis", 34, ORANGE, weight=BOLD).move_to([-4.3, 3.3, 0])
        self.play(FadeIn(nk, shift=DOWN * 0.1), run_time=0.6)

        c1, c2 = stroke_chips(None)
        self.at("stroke cycle")
        self.play(FadeIn(c1, shift=LEFT * 0.2), FadeIn(c2, shift=LEFT * 0.2), run_time=0.7)
        self.at("In stroke")
        self.play(*lit(c1, True), run_time=0.4)

        self.at("leading process extends")
        self.play(*cell.to(tip=1.1), run_time=1.5)
        lp = lab_left("leading process", BLUE, -1.1, P(0, 1.75)[1], [P(-0.1, 0.85)[0], P(0, 0.85)[1], 0])
        self.play(FadeIn(lp), run_time=0.4)

        self.at("A swelling forms")
        self.play(*cell.to(ws=1.0, wy=-0.4), run_time=1.2)
        sw = lab_left("swelling", BLUE, -1.1, P(0, 0.9)[1], [P(-0.38, 0.35)[0], P(0, 0.35)[1], 0])
        self.play(FadeIn(sw), run_time=0.4)

        cell.set(cs=-1.45)
        cs_l = always_redraw(lambda: lab_left("centrosome and Golgi", YELLOW, -1.1, P(0, cell.v("cs") + 0.2)[1],
                                              [-0.3, P(0, cell.v("cs") + 0.2)[1], 0]))
        self.at("The centrosome")
        self.play(cell.t["cs_op"].animate.set_value(1), cell.t["gg_op"].animate.set_value(1), run_time=0.5)
        self.add(cs_l)
        self.at("move forward")
        self.play(*cell.to(cs=-0.05), run_time=1.5)
        self.finish()


class S04StrokeTwo(SpokenScene):
    """stroke two: the nucleus is pulled into the swelling, the tail follows; the cycle repeats; the inchworm."""
    SC, Y0 = 1.15, 0.45

    def construct(self):
        sc = self.SC
        fib = fiber(0.62 * sc, -3.4, 3.4, rungs=True)
        self.add(fib)
        # same state the previous scene ended in
        cell = Cell(x=0, y0=self.Y0, sc=sc, soma=-2.4, tip=1.1, tail=-3.35, ws=1.0, wy=-0.4, cs=-0.05, op=1,
                    cs_op=1, gg_op=1)
        self.add(cell.mob)
        nk = T("nucleokinesis", 34, ORANGE, weight=BOLD).move_to([-4.3, 3.3, 0])
        c1, c2 = stroke_chips(1)
        self.add(nk, c1, c2)

        self.at("In stroke")
        self.play(*lit(c1, False), *lit(c2, True), run_time=0.4)
        self.at("nucleus is pulled")
        self.play(*cell.to(soma=-0.9, ws=0.0), run_time=1.8)
        self.at("trailing part")
        self.play(*cell.to(tail=-1.85), run_time=1.2)

        self.at("cycle repeats")
        self.play(*lit(c1, True), *lit(c2, False), run_time=0.3)
        self.play(*cell.to(**cell.stroke_one(-0.9)), run_time=0.8)
        self.play(*lit(c1, False), *lit(c2, True), *cell.to(**cell.stroke_two(-0.9)), run_time=0.9)

        self.at("inchworm")
        self.wait(0.4)
        r1 = ring(cell.P(0, cell.v("tip")), BLUE)
        self.at("reaches and grips")
        self.play(FadeIn(r1, scale=1.8), run_time=0.4)
        self.play(FadeOut(r1), run_time=0.4)
        r2 = ring(cell.P(0, cell.v("tail")), BLUE)
        self.at("back catches up")
        self.play(FadeIn(r2, scale=1.8), run_time=0.4)
        self.play(FadeOut(r2), run_time=0.4)
        self.finish()


# ---------------------------------------------------------------------------------------------
class S05Pull(SpokenScene):
    """the nucleus in its microtubule cage; dynein walks toward the centrosome and draws the nucleus after it."""

    A, B = 1.0, 1.3          # nucleus half-width and half-height
    TOP = 2.85               # centrosome y

    def curve_x(self, w, y):
        return w * (1 - np.exp(-1.3 * (self.TOP - y)))

    def make_curve(self, w, side):
        ys = np.linspace(self.TOP, -2.9, 40)
        pts = [[side * self.curve_x(w, y), y, 0] for y in ys]
        m = VMobject(stroke_color=TEAL, stroke_width=5)
        m.set_points_smoothly(pts)
        return m

    def construct(self):
        ny = ValueTracker(-0.5)
        nuc = always_redraw(lambda: Ellipse(width=2 * self.A, height=2 * self.B, stroke_color=ORANGE, stroke_width=5,
                                            fill_color=ORANGE, fill_opacity=0.5).move_to([0, ny.get_value(), 0]))
        dyn_op = ValueTracker(0.0)
        offs = [0.75, 0.0, -0.75]

        def dynein():
            g = VGroup()
            o = dyn_op.get_value()
            if o < 0.02:
                return g
            for side in (-1, 1):
                for dy in offs:
                    yb = ny.get_value() + dy
                    bx = self.A * np.sqrt(max(0.0, 1 - (dy / self.B) ** 2))
                    cx = self.curve_x(1.4, yb)
                    g.add(Line([side * bx, yb, 0], [side * cx, yb, 0], color=PURPLE, stroke_width=5, stroke_opacity=o))
                    g.add(Dot([side * cx, yb, 0], radius=0.17, color=PURPLE).set_opacity(o))
            return g
        dyn = always_redraw(dynein)

        cs = Dot([0, self.TOP, 0], radius=0.24, color=YELLOW)
        self.at("What does the pulling")
        self.play(FadeIn(nuc, scale=0.9), FadeIn(cs), run_time=0.8)
        nuc_l = lab_left("nucleus", ORANGE, -2.2, -0.5, [-1.05, -0.5, 0])
        cs_l = lab_left("centrosome", YELLOW, -1.3, 2.85, [-0.3, 2.85, 0])
        self.play(FadeIn(nuc_l), run_time=0.4)
        qq = T("?", 90, RED, weight=BOLD).move_to([0, 1.5, 0])
        self.play(FadeIn(qq, scale=0.6), run_time=0.5)

        curves = [self.make_curve(w, s) for w in (1.4, 1.75) for s in (-1, 1)]
        self.at("microtubules wrapped")
        self.play(FadeOut(qq), LaggedStart(*[Create(c) for c in curves], lag_ratio=0.2), run_time=2.0)
        mt_l = lab_right("microtubules", TEAL, 2.9, -1.6, [self.curve_x(1.75, -1.6) + 0.05, -1.6, 0])
        self.play(FadeIn(mt_l), run_time=0.4)

        self.at("ran forward")
        ups = VGroup(*[arr([s * self.curve_x(1.75, y), y - 0.55, 0], [s * self.curve_x(1.75, y + 0.05), y + 0.35, 0],
                           TEAL, w=6, tip=0.22) for s in (-1, 1) for y in (0.9, -1.4)])
        self.play(FadeIn(ups), run_time=0.7)
        self.at("track")
        self.play(*[c.animate.set_stroke(width=8) for c in curves], run_time=0.5)
        self.play(*[c.animate.set_stroke(width=5) for c in curves], FadeOut(ups), run_time=0.5)

        self.at("is a motor")
        self.add(dyn)
        self.play(dyn_op.animate.set_value(1.0), run_time=0.8)
        dy_l = lab_left("dynein", PURPLE, -3.0, -1.4, [-1.45, -1.25, 0])
        self.play(FadeIn(dy_l), run_time=0.5)
        self.at("minus ends")
        mn = lab_right("minus ends", TEAL, 1.0, 2.2, [0.3, 2.65, 0])
        mn.shift(RIGHT * 0.9)
        self.play(FadeIn(mn), run_time=0.5)
        self.at("sit at the centrosome")
        self.play(FadeIn(cs_l), Indicate(cs, color=YELLOW, scale_factor=1.5), run_time=0.8)

        self.at("draw the nucleus")
        self.play(FadeOut(nuc_l), FadeOut(mt_l), FadeOut(dy_l), ny.animate.set_value(0.65), run_time=2.2)

        my = chipfix("myosin II", PINK, 28).move_to([4.6, -1.0, 0])
        self.at("adds a second")
        self.play(FadeIn(my, shift=LEFT * 0.2), run_time=0.6)
        self.play(Indicate(nuc, color=PINK, scale_factor=1.06), run_time=0.8)
        q = T("where?", 30, PINK).next_to(my, DOWN, buff=0.25)
        self.at("still argued")
        self.play(FadeIn(q, shift=UP * 0.1), run_time=0.6)
        self.finish()


# ---------------------------------------------------------------------------------------------
class S06Break(SpokenScene):
    """three cells: normal follows; LIS1 knocked down: the body does not move; myosin II blocked: process grows, body stops."""

    Y0 = 0.95
    SC = 1.15

    def construct(self):
        xs = [-4.4, 0.0, 4.4]
        cells = [Cell(x=x, y0=self.Y0, sc=self.SC, soma=-2.4, tip=-0.4, tail=-3.35, op=0) for x in xs]
        fibs = [fiber(x + 0.62 * self.SC, -3.0, 2.7, rungs=True) for x in xs]
        for f in fibs:
            f.set_opacity(0)
        for c in cells:
            self.add(c.mob)
        self.add(*fibs)

        def title(text, color, x):
            return T(text, 28, color, weight=BOLD).move_to([x, 3.3, 0])

        def result(text, color, x):
            return T(text, 28, color).move_to([x, -3.4, 0])

        # normal cell: both strokes
        n_t = title("normal", TEXT, xs[0])
        self.at("Normally the nucleus")
        self.play(cells[0].t["op"].animate.set_value(1), fibs[0].animate.set_opacity(1), FadeIn(n_t), run_time=0.7)
        c = cells[0]
        c.set(cs=-1.45)
        self.play(*c.to(tip=1.1, ws=1.0, wy=-0.4, cs_op=1, gg_op=1), run_time=1.2)
        self.play(*c.to(cs=-0.05), run_time=0.6)
        self.play(*c.to(soma=-0.9, ws=0.0, tail=-1.85), run_time=1.3)
        n_r = result("nucleus follows", TEXT, xs[0])
        self.play(FadeIn(n_r), run_time=0.4)

        # LIS1 knockdown: the cell body does not move
        l_t = title("LIS1 knocked down", PURPLE, xs[1])
        self.at("embryonic")
        self.play(cells[1].t["op"].animate.set_value(1), fibs[1].animate.set_opacity(1), FadeIn(l_t), run_time=0.7)
        l_r = result("cell body stops", RED, xs[1])
        self.at("stops moving")
        rs = ring(cells[1].P(0, cells[1].v("soma")), RED, r=0.6)
        self.play(FadeIn(l_r), FadeIn(rs, scale=1.6), run_time=0.7)
        self.play(FadeOut(rs), run_time=0.4)
        self.at("regulates dynein")
        self.play(Indicate(l_t, color=PURPLE, scale_factor=1.12), run_time=0.8)
        note = VGroup(T("one lost copy:", 26, GREY), T("lissencephaly,", 26, GREY), T("a cortex with", 26, GREY),
                      T("reduced folding", 26, GREY)).arrange(DOWN, buff=0.18).move_to([xs[2], 0.3, 0])
        self.at("Losing one copy")
        self.play(FadeIn(note, shift=UP * 0.1), run_time=0.6)

        # myosin II block: the process keeps growing, the body stops
        m_t = title("myosin II blocked", PINK, xs[2])
        self.at("block myosin")
        self.play(FadeOut(note), cells[2].t["op"].animate.set_value(1), fibs[2].animate.set_opacity(1), FadeIn(m_t),
                  run_time=0.7)
        self.at("leading process can")
        self.play(*cells[2].to(tip=1.1), run_time=1.6)
        m_r = result("cell body stops", RED, xs[2])
        self.at("while the cell")
        self.play(FadeIn(m_r), run_time=0.6)

        # the rule
        self.at("The front reaches first")
        rings = [ring(cells[i].P(0, cells[i].v("tip")), BLUE) for i in (0, 2)]
        self.play(*[FadeIn(r, scale=1.8) for r in rings], run_time=0.5)
        self.play(*[FadeOut(r) for r in rings], run_time=0.4)
        self.at("pulled after it")
        r0 = ring(cells[0].P(0, cells[0].v("soma")), ORANGE, r=0.55)
        self.play(FadeIn(r0, scale=1.6), run_time=0.5)
        self.play(FadeOut(r0), run_time=0.4)
        self.finish()


class S07End(EndCard):
    LINE = "The front reaches, and the nucleus is pulled after it."
