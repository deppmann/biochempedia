"""What a Microscope Can Show (cell theory evidence, film 1).

COLOUR MAP (kept for both films, matches the lesson's size-ladder figure)
  EYE limit            = GREY dashed line, eye icon
  LIGHT-MICROSCOPE     = GOLD solid line, light-microscope icon
  ELECTRON-MICROSCOPE  = PURPLE dashed line, electron-microscope icon
  dots, cell walls     = dark BLUE (on the cream microscope view)
  blur                 = soft BLUE haze (layered translucent discs of a Gaussian spread, schematic)
  GAP COUNTER          = top left, micrometers
"""
import math
import numpy as np
from bp_style import *  # noqa: F401,F403

PURPLE = "#B58CD9"
CREAM = "#EDE4D0"
INK = "#1F4FA8"        # dark blue on the cream view
BROWN = "#B08A5A"

VC = np.array([1.9, -0.35, 0.0])
VR = 3.1
U = 5.0                # screen units per micrometer inside the view
SIG = 0.5              # blur spread (units): two points separate at gap = 2 sigma = 1.0 unit = 0.2 um
HK = [0.4, 0.7, 0.95, 1.2]

CC = np.array([0.0, -0.5, 0.0])
CR = 2.9

LX0, LX1 = -3.6, -2.2
LY = [3.3 - 1.1 * i for i in range(7)]
LAB = ["1 mm", "100 µm", "10 µm", "1 µm", "0.1 µm", "10 nm", "1 nm"]


def yl(size_um):
    return 3.3 - 1.1 * (3.0 - math.log10(size_um))


Y_EYE, Y_LM, Y_EM = yl(100.0), yl(0.2), yl(0.0015)


def breathe(m, amp=0.03, per=3.2, phase=0.0):
    m._bs, m._bt = 1.0, 0.0

    def f(mob, dt):
        mob._bt += dt
        s = 1 + amp * math.sin(2 * math.pi * mob._bt / per + phase)
        mob.scale(s / mob._bs)
        mob._bs = s
    m.add_updater(f)
    return m


def shimmer(m, amp=0.18, per=2.4):
    m._st = 0.0

    def f(mob, dt):
        mob._st += dt
        mob.set_stroke(opacity=1 - amp + amp * math.sin(2 * math.pi * mob._st / per))
    m.add_updater(f)
    return m


def view_circle(center, r, rim=GOLD):
    disc = Circle(radius=r, stroke_color=TEXT, stroke_width=6, fill_color=CREAM, fill_opacity=1).move_to(center)
    arc = Arc(radius=r + 0.14, start_angle=0, angle=1.1, stroke_color=rim, stroke_width=7)
    arc.move_arc_center_to(center)
    arc.add_updater(lambda m, dt: m.rotate(0.7 * dt, about_point=center))
    return VGroup(disc, arc)


def pair_mob(gtr, mtr, atr, center=VC):
    m = mtr.get_value()
    g = gtr.get_value() * U * m
    a = atr.get_value()
    grp = VGroup()
    for sx in (-1, 1):
        c = center + RIGHT * sx * g / 2
        for k in HK:
            grp.add(Circle(radius=SIG * k * m, stroke_width=0, fill_color=INK, fill_opacity=0.2 * a).move_to(c))
    for sx in (-1, 1):
        grp.add(Circle(radius=0.12 * m, stroke_width=0, fill_color="#14307A", fill_opacity=a).move_to(center + RIGHT * sx * g / 2))
    return grp


def honey(center, r, w=0.8, h=0.58):
    grp = VGroup()
    rows = int(2 * r / h) + 1
    for j in range(rows):
        y = center[1] - r + 0.2 + j * h
        off = (w / 2) if j % 2 else 0
        for i in range(-8, 9):
            x = center[0] + i * w + off
            cs = [(x + sx * w / 2 - center[0], y + sy * h / 2 - center[1]) for sx in (-1, 1) for sy in (-1, 1)]
            if all(math.hypot(a, b) < r - 0.12 for a, b in cs):
                grp.add(Rectangle(width=w, height=h, stroke_color=INK, stroke_width=3.5, fill_opacity=0).move_to([x, y, 0]))
    return grp


def eye_icon(h=0.9, color=GREY):
    o = Ellipse(width=1.3, height=0.7, stroke_color=color, stroke_width=4, fill_opacity=0)
    iris = Circle(radius=0.2, stroke_color=color, stroke_width=4, fill_color=color, fill_opacity=0.5)
    return VGroup(o, iris).scale_to_fit_height(h)


def lm_icon(h=1.4, color=GOLD):
    kw = dict(stroke_color=color, stroke_width=3, fill_color=color, fill_opacity=0.35)
    base = Rectangle(width=1.0, height=0.14, **kw).shift(DOWN * 0.7)
    pillar = Rectangle(width=0.14, height=1.1, **kw).shift(RIGHT * 0.3 + DOWN * 0.15)
    stage = Rectangle(width=0.6, height=0.07, **kw).shift(LEFT * 0.1 + DOWN * 0.35)
    tube = Rectangle(width=0.26, height=0.85, **kw).rotate(0.35).shift(LEFT * 0.05 + UP * 0.15)
    eyep = Rectangle(width=0.16, height=0.22, **kw).rotate(0.35).shift(RIGHT * 0.14 + UP * 0.66)
    return VGroup(base, pillar, stage, tube, eyep).scale_to_fit_height(h)


def em_icon(h=1.4, color=PURPLE):
    kw = dict(stroke_color=color, stroke_width=3, fill_color=color, fill_opacity=0.35)
    col = Rectangle(width=0.5, height=1.3, **kw).shift(UP * 0.1)
    rings = VGroup(*[Ellipse(width=0.7, height=0.14, **kw).shift(UP * (0.45 - 0.35 * i)) for i in range(3)])
    base = Rectangle(width=1.0, height=0.25, **kw).shift(DOWN * 0.7)
    screen = Rectangle(width=0.38, height=0.3, **kw).shift(RIGHT * 0.6 + DOWN * 0.7)
    return VGroup(col, rings, base, screen).scale_to_fit_height(h)


def dropper(color=PURPLE):
    kw = dict(stroke_color=color, stroke_width=3, fill_color=color, fill_opacity=0.35)
    bulb = Circle(radius=0.2, **kw).shift(UP * 0.55)
    tube = Rectangle(width=0.16, height=0.7, **kw)
    tip = Triangle(**kw).scale(0.08).rotate(PI).shift(DOWN * 0.42)
    drop = Circle(radius=0.07, **kw).shift(DOWN * 0.72)
    return VGroup(bulb, tube, tip, drop)


def cross(center, s=0.28):
    return VGroup(Line(center + UL * s, center + DR * s), Line(center + UR * s, center + DL * s)).set_stroke(RED, 7)


def left_panel(gval, mval=0.0, slider=False):
    gtr = ValueTracker(gval)
    out = {"gtr": gtr}
    out["read"] = always_redraw(lambda: M(f"gap {gtr.get_value():.2f} µm", 34, TEXT).move_to([-4.2, 3.05, 0]))
    out["track"] = Rectangle(width=2.8, height=0.22, stroke_color=GREY, stroke_width=2, fill_opacity=0).move_to([-4.2, 2.25, 0])
    out["fill"] = always_redraw(lambda: Rectangle(width=max(0.01, 2.8 * min(gtr.get_value(), 0.3) / 0.3), height=0.22, stroke_width=0,
                                                  fill_color=BLUE, fill_opacity=0.9).move_to([-5.6, 2.25, 0], aligned_edge=LEFT))
    tx = -5.6 + 2.8 * (0.2 / 0.3)
    out["tick"] = VGroup(Line([tx, 2.0, 0], [tx, 2.5, 0], color=GOLD, stroke_width=6),
                         T("light microscope", 26, GOLD).move_to([-3.9, 1.5, 0]),
                         T("limit about 0.2 µm", 26, GOLD).move_to([-3.9, 1.1, 0]))
    if slider:
        out["slabel"] = T("magnification", 28, TEXT).move_to([-4.2, 0.2, 0])
        out["strack"] = VGroup(Line([-5.6, -0.5, 0], [-2.8, -0.5, 0], color=GREY, stroke_width=6),
                               T("x1", 28, TEXT).move_to([-5.6, -1.05, 0]), T("x3", 28, TEXT).move_to([-2.8, -1.05, 0]))
        mtr = ValueTracker(mval)
        out["mtr"] = mtr
        out["knob"] = always_redraw(lambda: Circle(radius=0.2, stroke_color=GOLD, stroke_width=4, fill_color=GOLD,
                                                   fill_opacity=0.8).move_to([-5.6 + 2.8 * mtr.get_value(), -0.5, 0]))
    return out


class Ladder:
    def __init__(self):
        self.rails = VGroup(Line([LX0, LY[0] + 0.25, 0], [LX0, LY[6] - 0.25, 0], color=TEXT, stroke_width=5),
                            Line([LX1, LY[0] + 0.25, 0], [LX1, LY[6] - 0.25, 0], color=TEXT, stroke_width=5))
        self.rungs = [VGroup(Line([LX0, y, 0], [LX1, y, 0], color=TEXT, stroke_width=5),
                             T(LAB[i], 28, TEXT).move_to([LX0 - 0.15, y, 0], aligned_edge=RIGHT)) for i, y in enumerate(LY)]
        self.tags = [T("÷10", 24, GREY).move_to([(LX0 + LX1) / 2, (LY[i] + LY[i + 1]) / 2, 0]) for i in range(6)]
        self.eye_line = DashedLine([LX1, Y_EYE, 0], [1.3, Y_EYE, 0], color=GREY, stroke_width=6, dash_length=0.2)
        self.lm_line = Line([LX1, Y_LM, 0], [1.3, Y_LM, 0], color=GOLD, stroke_width=7)
        self.em_line = DashedLine([LX1, Y_EM, 0], [1.3, Y_EM, 0], color=PURPLE, stroke_width=6, dash_length=0.2)
        self.eye = eye_icon(0.7).move_to([1.8, Y_EYE, 0])
        self.lm = lm_icon(1.1).move_to([1.8, Y_LM, 0])
        self.em = em_icon(1.1).move_to([1.8, Y_EM, 0])

        def lab(a, b, c, y, x0=2.5):
            g = VGroup(T(a, 26, c), T(b, 26, c)).arrange(DOWN, aligned_edge=LEFT, buff=0.08)
            g.move_to([x0 + g.width / 2, y, 0])
            return g
        self.eye_t = lab("eye", "about 0.1 mm", GREY, Y_EYE, 2.8)
        self.lm_t = lab("light microscope", "about 0.2 µm", GOLD, Y_LM)
        self.em_t = lab("electron microscope", "1 to 2 nm", PURPLE, Y_EM)

    def all_static(self):
        return VGroup(self.rails, *self.rungs, *self.tags, self.eye_line, self.lm_line, self.em_line,
                      self.eye, self.lm, self.em, self.eye_t, self.lm_t, self.em_t)


class S00Title(TitleCard):
    LESSON = "The Cell Theory and Its Evidence"
    TITLE = "What a Microscope Can Show"


class S01Question(SpokenScene):
    def construct(self):
        head = T("1665: Hooke's cork (schematic)", 32, TEXT).move_to([0, 3.4, 0])
        block = Rectangle(width=2.4, height=1.6, stroke_color=BROWN, stroke_width=4, fill_color=BROWN, fill_opacity=0.5).move_to([-4.7, -1.2, 0])
        slc = Rectangle(width=2.4, height=0.14, stroke_color=BROWN, stroke_width=3, fill_color="#D9B988", fill_opacity=1).move_to([-4.7, -0.33, 0])
        self.play(FadeIn(block), FadeIn(slc), run_time=0.8)
        self.play(slc.animate.move_to([-4.7, 1.0, 0]).rotate(0.2), FadeIn(head), run_time=1.6, rate_func=smooth)
        self.at("rows")
        view = view_circle(CC, CR)
        self.play(GrowFromCenter(view), run_time=1.0)
        hc = honey(CC, CR)
        self.play(LaggedStart(*[Create(b) for b in hc], lag_ratio=0.04, run_time=1.8))
        self.at("cork")
        self.play(FadeOut(block), FadeOut(slc), run_time=0.8)
        self.at("called the boxes cells")
        pick = [hc[i] for i in range(0, len(hc), 5)]
        lab = T("cells", 40, YELLOW, weight=BOLD).move_to([4.7, 0.2, 0])
        self.play(LaggedStart(*[Indicate(b, color=YELLOW, scale_factor=1.25) for b in pick], lag_ratio=0.12, run_time=2.0), FadeIn(lab))
        self.at("What decides")
        self.play(FadeOut(lab), run_time=0.4)
        q1 = VGroup(T("?", 64, YELLOW, weight=BOLD), T("what can a", 30, TEXT), T("tool show?", 30, TEXT)).arrange(DOWN, buff=0.15).move_to([4.8, 0.4, 0])
        self.play(FadeIn(q1, shift=LEFT * 0.2), run_time=0.8)
        self.at("And why")
        q2 = VGroup(T("?", 64, YELLOW, weight=BOLD), T("why was seeing", 30, TEXT), T("not enough?", 30, TEXT)).arrange(DOWN, buff=0.15).move_to([-4.8, 0.4, 0])
        self.play(FadeIn(q2, shift=RIGHT * 0.2), run_time=0.8)
        for q in (q1, q2):
            breathe(q[0], 0.08, 2.4)
        self.at("We start")
        self.play(Indicate(view[0], color=GOLD, scale_factor=1.03), run_time=1.2)
        self.finish()


class S02Words(SpokenScene):
    def construct(self):
        ml = T("magnification", 40, YELLOW, weight=BOLD).move_to([-3.4, 3.1, 0])
        rl = T("resolution", 40, GOLD, weight=BOLD).move_to([3.4, 3.1, 0])
        div = Line([0, 3.6, 0], [0, -3.6, 0], color=GREY, stroke_width=2)
        self.play(Create(div), run_time=0.6)
        self.at("Magnification is")
        self.play(FadeIn(ml, shift=DOWN * 0.2), run_time=0.7)
        sq = Square(side_length=0.9, stroke_color=INK, stroke_width=6, fill_color=INK, fill_opacity=0.35).move_to([-3.4, -0.3, 0])
        x1 = T("x1", 56, TEXT, weight=BOLD).move_to([-3.4, -2.9, 0])
        self.play(FadeIn(sq), FadeIn(x1), run_time=0.8)
        self.at("larger an image")
        x3 = T("x3", 56, TEXT, weight=BOLD).move_to([-3.4, -3.2, 0])
        self.play(sq.animate.scale(3.0).move_to([-3.4, 0.3, 0]), Transform(x1, x3), run_time=2.6)
        breathe(sq, 0.03, 2.6)
        self.at("Resolution is")
        self.play(FadeIn(rl, shift=DOWN * 0.2), run_time=0.7)
        gap = 1.9
        d1 = Circle(radius=0.2, stroke_width=0, fill_color="#6FA8FF", fill_opacity=1).move_to([3.4 - gap / 2, 0.8, 0])
        d2 = Circle(radius=0.2, stroke_width=0, fill_color="#6FA8FF", fill_opacity=1).move_to([3.4 + gap / 2, 0.8, 0])
        self.play(FadeIn(d1), FadeIn(d2), run_time=0.8)
        self.at("smallest distance")
        arr = DoubleArrow(d1.get_right() + RIGHT * 0.05, d2.get_left() + LEFT * 0.05, color=GOLD, buff=0.05, stroke_width=6, tip_length=0.2)
        self.play(GrowFromCenter(arr), run_time=0.9)
        self.at("two separate points")
        t = VGroup(T("smallest gap that", 30, TEXT), T("still looks like two", 30, TEXT)).arrange(DOWN, buff=0.12).move_to([3.4, -1.2, 0])
        self.play(FadeIn(t, shift=UP * 0.15), run_time=0.8)
        ph = {"t": 0.0}

        def sway(m, dt):
            ph["t"] += dt
            g = gap + 0.35 * math.sin(2 * math.pi * ph["t"] / 3.0)
            d1.move_to([3.4 - g / 2, 0.8, 0])
            d2.move_to([3.4 + g / 2, 0.8, 0])
            m.become(DoubleArrow(d1.get_right() + RIGHT * 0.05, d2.get_left() + LEFT * 0.05, color=GOLD, buff=0.05, stroke_width=6, tip_length=0.2))
        arr.add_updater(sway)
        self.finish()


class S03Dots(SpokenScene):
    def construct(self):
        def gapf(t):
            if t < 13.4:
                return 0.05 + 0.03 * t / 13.4
            return 0.08 + 0.22 * min(1.0, (t - 13.4) / 7.2)
        P = left_panel(0.05)
        gtr = P["gtr"]
        drv = Mobject()
        drv.add_updater(lambda m: gtr.set_value(gapf(self.elapsed())))
        self.add(drv)
        view = view_circle(VC, VR)
        mtr, atr = ValueTracker(1.0), ValueTracker(0.0)
        content = always_redraw(lambda: pair_mob(gtr, mtr, atr))
        self.play(GrowFromCenter(view), run_time=1.0)
        self.add(content, P["read"], P["fill"])
        self.play(atr.animate.set_value(1.0), run_time=1.0)
        sch = T("schematic blur", 24, GREY).move_to([-4.2, -3.4, 0])
        self.play(FadeIn(P["track"]), FadeIn(sch), run_time=0.6)
        self.at("ordinary light")
        self.play(FadeIn(P["tick"]), run_time=0.8)
        self.at("A micrometer")
        um = T("1 µm = 1/1000 mm", 30, YELLOW).move_to([-4.2, -2.4, 0])
        self.play(FadeIn(um, shift=UP * 0.15), run_time=0.8)
        self.at("The dots start close")
        self.play(Indicate(content, color=INK, scale_factor=1.12), run_time=1.0)
        self.at("Slowly")
        self.play(Indicate(P["read"], color=YELLOW, scale_factor=1.1), run_time=1.0)
        self.at("Near a gap")
        self.play(Indicate(P["tick"][0], color=YELLOW, scale_factor=1.8), run_time=1.2)
        self.finish()


class S04Why(SpokenScene):
    def construct(self):
        sch = T("schematic", 24, GREY).move_to([-5.6, 3.5, 0])
        yc = 2.0
        lens = Ellipse(width=0.5, height=2.4, stroke_color=TEAL, stroke_width=5, fill_color=TEAL, fill_opacity=0.18).move_to([-1.2, yc, 0])
        lens_t = T("lens opening", 26, TEAL).move_to([-1.2, 0.55, 0])
        ys = [yc + d for d in (-0.8, -0.4, 0, 0.4, 0.8)]
        rays = VGroup(*[Line([-6.2, y, 0], [-1.2, y, 0], color=YELLOW, stroke_width=3).set_stroke(opacity=0.55) for y in ys])
        fan = ValueTracker(0.0)
        far = VGroup(*[Line([-1.2, y, 0], [5.2, y + (y - yc) * 0.7, 0], color=YELLOW, stroke_width=3).set_stroke(opacity=0.5) for y in ys])
        photons = VGroup()
        for i, y in enumerate(ys):
            for k in range(3):
                d = Circle(radius=0.07, stroke_width=0, fill_color=YELLOW, fill_opacity=1)
                d._y, d._p = y, k / 3 + i * 0.07
                photons.add(d)
        clock = {"t": 0.0}

        def fly(m, dt):
            clock["t"] += dt
            for d in m:
                u = (clock["t"] * 0.16 + d._p) % 1.0
                x = -6.2 + u * 11.4
                if x < -1.2:
                    d.move_to([x, d._y, 0])
                    d.set_fill(opacity=1)
                else:
                    d.move_to([x, d._y + (d._y - yc) * 0.7 * (x + 1.2) / 6.4, 0])
                    d.set_fill(opacity=fan.get_value())
        photons.add_updater(fly)
        self.play(FadeIn(sch), FadeIn(lens), FadeIn(rays), run_time=1.0)
        self.add(photons)
        gtr = ValueTracker(3.4)
        htr = ValueTracker(0.0)
        cy = -1.9
        halos = always_redraw(lambda: VGroup(*[Circle(radius=0.7 * k * htr.get_value() + 0.001, stroke_width=0, fill_color=BLUE, fill_opacity=0.22)
                                              .move_to([sx * gtr.get_value() / 2, cy, 0]) for sx in (-1, 1) for k in HK]))
        dots = always_redraw(lambda: VGroup(*[Circle(radius=0.14, stroke_width=0, fill_color=BLUE, fill_opacity=1)
                                              .move_to([sx * gtr.get_value() / 2, cy, 0]) for sx in (-1, 1)]))
        self.add(halos, dots)
        self.at("blurs")
        bl = T("blurs the finest details", 32, TEXT).move_to([0, -3.4, 0])
        self.play(FadeIn(bl, shift=UP * 0.1), run_time=0.8)
        self.at("Light spreads")
        self.play(FadeIn(far), fan.animate.set_value(1.0), FadeIn(lens_t), run_time=1.8)
        self.at("So each point")
        self.play(htr.animate.set_value(1.0), run_time=2.0)
        self.at("and close smudges")
        self.play(gtr.animate.set_value(0.45), run_time=2.6, rate_func=smooth)
        self.finish()


class S05Predict(SpokenScene):
    def construct(self):
        P = left_panel(0.15, mval=0.0, slider=True)
        gtr = P["gtr"]
        mtr, atr = ValueTracker(1.0), ValueTracker(0.0)
        view = view_circle(VC, VR)
        content = always_redraw(lambda: pair_mob(gtr, mtr, atr))
        self.add(view, P["read"], P["track"], P["fill"], P["tick"], content)
        self.play(atr.animate.set_value(1.0), run_time=1.0)
        self.at("Now set")
        self.play(Indicate(P["read"], color=YELLOW, scale_factor=1.1), run_time=1.2)
        self.at("They look like one")
        self.play(Indicate(content, color=INK, scale_factor=1.12), run_time=1.2)
        self.at("We triple")
        self.play(FadeIn(P["slabel"]), FadeIn(P["strack"]), FadeIn(P["knob"]), run_time=0.8)
        self.play(P["mtr"].animate.set_value(0.88), run_time=2.2)
        self.at("Will you see")
        q = T("one dot or two?", 54, YELLOW, weight=BOLD).move_to([VC[0], 3.3, 0])
        self.play(FadeIn(q, shift=DOWN * 0.2), run_time=0.9)
        self.finish()


class S06Pause(NarratedScene):
    def construct(self):
        P = left_panel(0.15, mval=0.88, slider=True)
        gtr = P["gtr"]
        mtr, atr = ValueTracker(1.0), ValueTracker(1.0)
        view = view_circle(VC, VR)
        content = always_redraw(lambda: pair_mob(gtr, mtr, atr))
        q = T("one dot or two?", 54, YELLOW, weight=BOLD).move_to([VC[0], 3.3, 0])
        self.add(view, content, P["read"], P["track"], P["fill"], P["tick"], P["slabel"], P["strack"], P["knob"], q)
        tmr = ValueTracker(0.0)
        ring = always_redraw(lambda: Arc(radius=0.35, start_angle=PI / 2, angle=-TAU * max(0.001, 1 - tmr.get_value()),
                                         stroke_color=YELLOW, stroke_width=8).move_arc_center_to([-5.9, -3.2, 0]))
        self.add(ring)
        self.play(tmr.animate.set_value(1.0), run_time=5.0, rate_func=linear)
        self.finish()


class S07Reveal(SpokenScene):
    def construct(self):
        P = left_panel(0.15, mval=0.88, slider=True)
        gtr = P["gtr"]
        mtr, atr = ValueTracker(1.0), ValueTracker(1.0)
        view = view_circle(VC, VR)
        content = always_redraw(lambda: pair_mob(gtr, mtr, atr))
        self.add(view, content, P["read"], P["track"], P["fill"], P["tick"], P["slabel"], P["strack"], P["knob"])
        self.play(P["mtr"].animate.set_value(1.0), mtr.animate.set_value(3.0), run_time=2.4)
        self.at("The blur got bigger")
        self.play(Indicate(P["read"], color=YELLOW, scale_factor=1.1), run_time=1.2)
        self.at("Making the image bigger")
        self.play(Indicate(P["tick"][0], color=YELLOW, scale_factor=1.8), run_time=1.2)
        self.at("Magnification makes")
        l1 = VGroup(T("magnification:", 28, YELLOW, weight=BOLD), T("bigger image", 28, TEXT)).arrange(DOWN, aligned_edge=LEFT, buff=0.08).move_to([-4.2, -2.1, 0])
        self.play(Write(l1), run_time=1.6)
        self.at("Resolution decides")
        l2 = VGroup(T("resolution:", 28, GOLD, weight=BOLD), T("how much detail", 28, TEXT)).arrange(DOWN, aligned_edge=LEFT, buff=0.08).move_to([-4.2, -3.2, 0])
        self.play(Write(l2), run_time=1.6)
        self.finish()


class S08Rule(SpokenScene):
    def construct(self):
        box = RoundedRectangle(corner_radius=0.2, width=11.4, height=2.5, stroke_color=GOLD, stroke_width=4, fill_color=GOLD, fill_opacity=0.06).move_to([0, 1.95, 0])
        self.play(Create(box), run_time=1.4)
        lines = VGroup(T("A tool shows a detail only if", 40, TEXT), T("the detail is larger than", 40, TEXT),
                       T("the tool's limit.", 40, GOLD, weight=BOLD)).arrange(DOWN, buff=0.14).move_to(box)
        self.at("A tool shows")
        self.play(AddTextLetterByLetter(lines[0]), run_time=1.5)
        self.play(AddTextLetterByLetter(lines[1]), run_time=1.3)
        self.play(AddTextLetterByLetter(lines[2]), run_time=1.0)
        self.at("Enlarging")
        blob = VGroup(*[Circle(radius=0.6 * k, stroke_width=0, fill_color=BLUE, fill_opacity=0.22) for k in (0.5, 0.75, 1.0, 1.2)]).move_to([-4.2, -1.1, 0])
        glass = VGroup(Circle(radius=0.55, stroke_color=TEXT, stroke_width=5, fill_opacity=0), Line([0.4, -0.4, 0], [0.9, -0.9, 0], color=TEXT, stroke_width=8)).move_to([-2.9, -1.0, 0])
        self.play(FadeIn(blob), FadeIn(glass), run_time=0.8)
        self.play(blob.animate.scale(1.7), run_time=1.6)
        breathe(blob, 0.03, 2.8)
        tag1 = VGroup(T("enlarging adds", 30, TEXT), T("no detail", 30, TEXT)).arrange(DOWN, buff=0.1).move_to([-3.4, -3.05, 0])
        self.play(FadeIn(tag1, shift=UP * 0.1), run_time=0.8)
        self.at("A whole cell")
        cell = Circle(radius=1.1, stroke_color=BLUE, stroke_width=7, fill_opacity=0).move_to([3.5, -1.2, 0])
        haze = VGroup(*[Circle(radius=0.2 * k + 0.1, stroke_width=0, fill_color=BLUE, fill_opacity=0.18).move_to(cell.get_center() + p)
                        for p, k in [(LEFT * 0.35 + UP * 0.2, 1.2), (RIGHT * 0.4 + UP * 0.1, 1.0), (DOWN * 0.4, 1.3), (RIGHT * 0.1 + UP * 0.45, 0.8)]])
        self.play(Create(cell), run_time=1.0)
        self.play(FadeIn(haze), run_time=1.0)
        breathe(haze, 0.05, 2.6)
        tag2 = VGroup(T("cell: clear", 30, TEXT), T("parts: not", 30, TEXT)).arrange(DOWN, buff=0.1).move_to([3.5, -3.05, 0])
        sch = T("schematic", 22, GREY).move_to([5.9, -3.4, 0])
        self.play(FadeIn(tag2, shift=UP * 0.1), FadeIn(sch), run_time=0.8)
        self.finish()


class S09Ladder(SpokenScene):
    def construct(self):
        L = Ladder()
        icons = [eye_icon(1.5), lm_icon(2.0), em_icon(2.0)]
        xs = [-3.6, 0.0, 3.6]
        names = [("eye", GREY), ("light microscope", GOLD), ("electron microscope", PURPLE)]
        row = VGroup()
        for b, x, (n, c) in zip(icons, xs, names):
            b.move_to([x, 0.5, 0])
            row.add(VGroup(b, T(n, 28, c).move_to([x, -1.2, 0])))
        self.play(LaggedStart(*[FadeIn(r, shift=UP * 0.2) for r in row], lag_ratio=0.3, run_time=2.4))
        for i, r in enumerate(row):
            breathe(r, 0.04, 2.4, phase=i)
        self.at("Picture a ladder")
        self.play(FadeOut(row), run_time=0.7)
        self.play(Create(L.rails), run_time=0.6)
        self.play(LaggedStart(*[FadeIn(r) for r in L.rungs], lag_ratio=0.3, run_time=1.6))
        self.at("each rung")
        self.play(LaggedStart(*[FadeIn(t, shift=UP * 0.1) for t in L.tags], lag_ratio=0.3, run_time=2.0))
        self.at("Your eye's limit")
        self.play(Create(L.eye_line), FadeIn(L.eye), FadeIn(L.eye_t), run_time=1.6)
        self.at("light microscope's gold")
        self.play(Create(L.lm_line), FadeIn(L.lm), FadeIn(L.lm_t), run_time=1.6)
        self.at("electron microscope's line")
        self.play(Create(L.em_line), FadeIn(L.em), FadeIn(L.em_t), run_time=1.6)
        for ln in (L.eye_line, L.lm_line, L.em_line):
            shimmer(ln, 0.25, 2.2)
        self.finish()


class S10Cork(SpokenScene):
    def construct(self):
        L = Ladder()
        L.all_static().remove(*L.tags) if False else None
        self.add(VGroup(L.rails, *L.rungs, L.eye_line, L.lm_line, L.em_line, L.eye, L.lm, L.em, L.eye_t, L.lm_t, L.em_t))
        for ln in (L.eye_line, L.lm_line, L.em_line):
            shimmer(ln, 0.25, 2.2)
        cx = (LX0 + LX1) / 2
        cell = Rectangle(width=0.8, height=0.7, stroke_color=INK, stroke_width=6, fill_color=CREAM, fill_opacity=1).move_to([6.0, 1.2, 0])
        ctag = VGroup(T("Hooke's cork cell", 26, BLUE), T("(schematic position)", 26, GREY)).arrange(DOWN, aligned_edge=LEFT, buff=0.06)
        ctag.move_to([2.5 + ctag.width / 2 + 0.4, 1.2, 0])
        self.play(cell.animate.move_to([cx, 1.2, 0]), run_time=1.4, rate_func=smooth)
        self.play(FadeIn(ctag), run_time=0.6)
        eye_arr = Arrow(L.eye.get_left() + DOWN * 0.1, cell.get_right() + UP * 0.1, color=GREY, buff=0.1, stroke_width=5)
        xx = cross(eye_arr.get_center())
        lm_arr = Arrow(L.lm.get_left() + UP * 0.1, cell.get_right() + DOWN * 0.15, color=GOLD, buff=0.1, stroke_width=5)
        self.at("make out")
        self.play(Create(eye_arr), run_time=0.6)
        self.play(FadeIn(xx), Create(lm_arr), run_time=0.8)
        pts = VGroup(*[Circle(radius=0.16, stroke_width=0, fill_color=YELLOW, fill_opacity=1) for _ in range(6)])
        p0, p1 = lm_arr.get_start(), lm_arr.get_end()
        pc = {"t": 0.0}

        def flow(m, dt):
            pc["t"] += dt
            for i, d in enumerate(m):
                u = (pc["t"] * 0.35 + i / 6) % 1.0
                d.move_to(p0 + (p1 - p0) * u)
        pts.add_updater(flow)
        self.add(pts)
        shimmer(cell, 0.3, 2.0)
        breathe(L.lm, 0.10, 2.0)
        breathe(L.em, 0.10, 2.4, 1.0)
        breathe(L.eye, 0.10, 2.2, 2.0)
        self.at("spacing")
        sp = DoubleArrow(cell.get_left() + DOWN * 0.55, cell.get_right() + DOWN * 0.55, color=YELLOW, buff=0, stroke_width=5, tip_length=0.15)
        stag = T("outlines and spacing", 28, YELLOW).move_to([4.3, 0.3, 0])
        self.play(GrowFromCenter(sp), FadeIn(stag), run_time=1.0)
        self.at("better resolution")
        self.play(Indicate(L.lm_line, color=YELLOW, scale_factor=1.0), Indicate(L.em_line, color=YELLOW, scale_factor=1.0), run_time=1.4)
        self.at("more contrast")
        dr = dropper().move_to([-0.2, -2.0, 0])
        dl = T("more contrast", 28, PURPLE).move_to([1.4, -2.0, 0])
        self.play(FadeIn(dr, shift=DOWN * 0.2), FadeIn(dl), run_time=0.8)
        clk = {"t": 0.0}
        drop = dr[3]

        def drip(m, dt):
            clk["t"] += dt
            u = (clk["t"] * 0.5) % 1.0
            m.move_to([dr.get_center()[0], -1.65 - 0.9 * u, 0])
            m.set_fill(opacity=1 - u)
        drop.add_updater(drip)
        self.at("later tools")
        self.play(Indicate(L.em, color=YELLOW, scale_factor=1.2), run_time=1.2)
        self.finish()


class S11NotEnough(SpokenScene):
    def construct(self):
        head = T("1665: Hooke's cork (schematic)", 32, TEXT).move_to([0, 3.4, 0])
        view = view_circle(CC, CR)
        hc = honey(CC, CR)
        self.add(head, view)
        self.play(FadeIn(hc), run_time=1.0)
        self.at("But look at what")
        self.play(Indicate(hc, color=INK, scale_factor=1.03), run_time=1.2)
        self.at("Empty walls")
        t1 = VGroup(T("walls of", 34, RED), T("dead cells", 34, RED)).arrange(DOWN, buff=0.1).move_to([-4.8, 0.4, 0])
        self.play(FadeIn(t1, shift=RIGHT * 0.2), run_time=1.0)
        self.at("One material")
        t2 = VGroup(T("one material,", 34, YELLOW), T("one plant", 34, YELLOW)).arrange(DOWN, buff=0.1).move_to([4.8, 0.4, 0])
        self.play(FadeIn(t2, shift=LEFT * 0.2), run_time=1.0)
        self.at("That cannot show")
        self.play(FadeOut(head), run_time=0.3)
        bub = RoundedRectangle(corner_radius=0.3, width=8.6, height=0.9, stroke_color=TEXT, stroke_width=4, fill_color=BG, fill_opacity=1).move_to([-0.6, 3.15, 0])
        bt = T("all living things are made of cells?", 32, TEXT).move_to(bub)
        self.play(FadeIn(bub), FadeIn(bt), run_time=1.0)
        self.at("made of cells")
        stamp = VGroup(RoundedRectangle(corner_radius=0.1, width=1.9, height=0.7, stroke_color=GREY, stroke_width=5, fill_opacity=0),
                       T("not yet", 32, GREY, weight=BOLD)).move_to([5.3, 3.0, 0]).rotate(-0.18)
        self.play(FadeIn(stamp, scale=1.6), run_time=0.6)
        self.finish()


def cells_patch(w, h, n, seed):
    rng = np.random.RandomState(seed)
    g = VGroup()
    for _ in range(n):
        g.add(Circle(radius=rng.uniform(0.08, 0.14), stroke_color=INK, stroke_width=3, fill_opacity=0).move_to(
            [rng.uniform(-w / 2 + 0.2, w / 2 - 0.2), rng.uniform(-h / 2 + 0.2, h / 2 - 0.2), 0]))
    return g


class S12Believe(SpokenScene):
    def construct(self):
        lh = T("making out cells", 34, GOLD, weight=BOLD).move_to([-3.4, 3.2, 0])
        rh = T("building the theory", 34, YELLOW, weight=BOLD).move_to([3.4, 3.2, 0])
        div = Line([0, 3.7, 0], [0, -0.3, 0], color=GREY, stroke_width=2)
        self.add(div)
        self.play(FadeIn(lh, shift=DOWN * 0.2), run_time=0.8)
        lm = lm_icon(2.2).move_to([-3.4, 1.4, 0])
        gl = Line([-5.8, 0.2, 0], [-1.0, 0.2, 0], color=GOLD, stroke_width=7)
        self.play(FadeIn(lm), Create(gl), run_time=1.4)
        breathe(lm, 0.03, 2.8)
        shimmer(gl, 0.25, 2.2)
        self.at("Building the theory")
        self.play(FadeIn(rh, shift=DOWN * 0.2), run_time=0.8)
        self.at("comparing many kinds")
        panels = VGroup()
        for i, n in enumerate(["leaf", "tadpole", "pond drop"]):
            r = RoundedRectangle(corner_radius=0.15, width=1.85, height=1.7, stroke_color=GREY, stroke_width=3, fill_color=CREAM, fill_opacity=1)
            p = cells_patch(1.85, 1.7, 5 + i, 10 + i).move_to(r)
            lab = T(n, 24, TEXT).next_to(r, DOWN, buff=0.1)
            panels.add(VGroup(r, p, lab))
        panels.arrange(RIGHT, buff=0.2).move_to([3.4, 1.35, 0])
        self.play(LaggedStart(*[FadeIn(p, shift=UP * 0.15) for p in panels], lag_ratio=0.45, run_time=2.2))
        for i, p in enumerate(panels):
            breathe(p[1], 0.05, 2.5 + 0.3 * i)
        self.at("testing where")
        q = VGroup(T("where do new cells", 30, YELLOW), T("come from?", 30, YELLOW)).arrange(DOWN, buff=0.1).move_to([3.4, -0.7, 0])
        self.play(FadeIn(q, shift=UP * 0.15), run_time=0.9)
        self.at("About 175 years")
        tl = Line([-5.8, -2.8, 0], [5.8, -2.8, 0], color=GREY, stroke_width=5)
        a = T("1665", 32, TEXT).move_to([-5.4, -3.4, 0])
        b = T("1838 to 1839", 32, TEXT).move_to([4.9, -3.4, 0])
        self.play(Create(tl), FadeIn(a), run_time=0.8)
        prog = Line([-5.8, -2.8, 0], [-5.8, -2.8, 0], color=YELLOW, stroke_width=9)
        self.add(prog)
        yrs = T("about 175 years", 34, YELLOW, weight=BOLD).move_to([0, -2.25, 0])
        self.play(FadeIn(yrs), run_time=0.6)
        self.play(prog.animate.put_start_and_end_on([-5.8, -2.8, 0], [5.8, -2.8, 0]),
                  run_time=max(1.5, self.t_of("alike") - self.elapsed()), rate_func=linear)
        self.play(FadeIn(b), run_time=0.6)
        self.finish()


class S13End(EndCard):
    LINE = "A detail shows only if it is larger than the tool's limit."
