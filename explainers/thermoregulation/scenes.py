"""Heat made, heat lost, set point: body temperature as a balance (Biochemistrypedia explainer)

Timed to the SPOKEN words (self.at cues). Only the lesson's routes, numbers and statements are drawn.
The thermoneutral-zone curves in s04 are invented shapes "in this sketch" (relative units); the
numbers in s05 are the lesson's invented practice numbers, computed from its equation.

COLOR MAP (one color per concept, whole video)
  ORANGE = heat: made, flowing, or lost (arrows, heat production, the plotted lines)
  BLUE   = the surroundings: air, sun-and-rock side, "cold" outside; also the body outline
  GREEN  = the thermoneutral zone / basal rate
  GOLD   = the set point (and the controller)
  RED    = raised or crossed-out things: fever (up), "not explained by cooling"
  YELLOW = the thing in play (highlight, dots)
  GREY   = axes, notes, legends
  TEXT   = labels and equations
"""
import numpy as np
from bp_style import *  # noqa: F401,F403

ORANGE = "#F2994A"
HEAT, AIR, ZONE, SETP, UP_C, HI = ORANGE, BLUE, GREEN, GOLD, RED, YELLOW


def body(w=3.4, h=2.0, label=None, size=28, color=AIR):
    r = RoundedRectangle(corner_radius=0.25, width=w, height=h, stroke_color=color, stroke_width=3.5,
                         fill_color=color, fill_opacity=0.10)
    g = VGroup(r)
    if label:
        g.add(T(label, size, TEXT).move_to(r))
    return g


def arrow(a, b, color=HEAT, sw=7, tip=0.28, both=False):
    cls = DoubleArrow if both else Arrow
    return cls(np.array(a, dtype=float), np.array(b, dtype=float), buff=0, color=color, stroke_width=sw,
               max_tip_length_to_length_ratio=0.3, max_stroke_width_to_length_ratio=12, tip_length=tip)


def tag(text, x, y, size=22, color=GREY):
    return T(text, size, color).move_to([x, y, 0])


class Sc(SpokenScene):
    def rt(self, f):
        return min(max(0.4, self.beat(f)), 1.1)


# ---------------------------------------------------------------- title / end
class S00Title(TitleCard):
    LESSON = "Metabolic Rate and Body Temperature"
    TITLE = "Heat Made, Heat Lost, Set Point"


class S07End(EndCard):
    LINE = "In an endotherm at steady state, heat made equals heat lost."


# ---------------------------------------------------------------- s01
class S01Question(Sc):
    def construct(self):
        bx = body(6.0, 3.4, None).move_to([0, 0.2, 0])
        name = T("desert iguana", 32, TEXT).move_to(bx[0].get_top() + DOWN * 0.5)
        temp = M("near or above 37 °C", 30, HEAT).move_to(bx[0].get_center() + DOWN * 0.15)
        sub = T("in the active day", 24, GREY).next_to(temp, DOWN, buff=0.15)
        self.play(Create(bx[0]), FadeIn(name), run_time=0.8)
        self.at("warmer than you are")
        self.play(FadeIn(temp, shift=UP * 0.1), FadeIn(sub), run_time=self.rt(0.06))
        self.at("So what does")
        cold = T("cold-blooded = ?", 34, HI).move_to([0, 3.15, 0])
        self.play(FadeIn(cold, shift=DOWN * 0.1), run_time=self.rt(0.05))
        self.at("the heat an animal makes")
        a_in = arrow([-6.1, 0.2, 0], [-3.1, 0.2, 0])
        l_in = T("heat made?", 30, HEAT).move_to([-4.6, 0.8, 0])
        self.play(GrowArrow(a_in), FadeIn(l_in), run_time=self.rt(0.05))
        self.at("the heat it loses")
        a_out = arrow([3.1, 0.2, 0], [6.1, 0.2, 0])
        l_out = T("heat lost?", 30, HEAT).move_to([4.6, 0.8, 0])
        self.play(GrowArrow(a_out), FadeIn(l_out), run_time=self.rt(0.05))
        self.at("or a controller")
        ctrl = chip("controller?", SETP, size=30).move_to([0, -2.9, 0])
        link = arrow([0, -2.35, 0], [0, -1.55, 0], color=SETP, sw=5, tip=0.2)
        self.play(FadeIn(ctrl, shift=UP * 0.1), GrowArrow(link), run_time=self.rt(0.05))
        self.at("Metabolic rate is")
        self.play(FadeOut(cold), FadeOut(ctrl), FadeOut(link), FadeOut(temp), FadeOut(sub),
                  run_time=self.rt(0.05))
        mr = chip("metabolic rate = energy used per unit of time", ORANGE, size=30).move_to([0, 3.0, 0])
        unit = T("in watts: joules per second", 24, GREY).move_to([0, -2.9, 0])
        self.play(FadeIn(mr, shift=DOWN * 0.1), FadeIn(unit), run_time=self.rt(0.05))
        self.at("nearly all of it")
        heat_in = T("nearly all of it ends up as heat", 28, HEAT).move_to(bx[0].get_center() + DOWN * 0.1)
        self.play(FadeIn(heat_in), bx[0].animate.set_stroke(HEAT).set_fill(HEAT, opacity=0.25),
                  run_time=self.rt(0.06))
        self.finish()


# ---------------------------------------------------------------- s02
class S02Sources(Sc):
    def construct(self):
        L, R = -3.5, 3.5
        title_l = T("Endotherm", 36, TEXT).move_to([L, 3.1, 0])
        sub_l = T("mammals and birds", 26, GREY).move_to([L, 2.55, 0])
        title_r = T("Ectotherm", 36, TEXT).move_to([R, 3.1, 0])
        sub_r = T("desert iguana", 26, GREY).move_to([R, 2.55, 0])
        bl = body(5.4, 3.0).move_to([L, -0.2, 0])
        br = body(5.4, 3.0).move_to([R, -0.2, 0])
        self.play(Create(bl[0]), Create(br[0]), FadeIn(title_l), FadeIn(sub_l), run_time=0.5)
        self.at("their own metabolism")
        met = chip("own metabolism", HEAT, size=32).move_to(bl[0].get_center())
        self.play(FadeIn(met, scale=0.8), bl[0].animate.set_fill(HEAT, opacity=0.2), run_time=self.rt(0.05))
        self.at("held in by insulation")
        ins = RoundedRectangle(corner_radius=0.3, width=5.8, height=3.4, stroke_color=GREY, stroke_width=10,
                               fill_opacity=0).move_to(bl[0])
        ins_l = T("insulation", 26, GREY).move_to([L, -2.3, 0])
        self.play(Create(ins), FadeIn(ins_l), run_time=self.rt(0.06))
        self.at("Ectotherms like the desert")
        self.play(FadeIn(title_r), FadeIn(sub_r), run_time=self.rt(0.04))
        self.at("from outside")
        sun = chip("sun", AIR, size=30).move_to([R - 1.2, 1.9, 0])
        rock = chip("warm rock", AIR, size=30).move_to([R + 0.9, -2.6, 0])
        a1 = arrow([R - 1.2, 1.5, 0], [R - 1.2, 0.5, 0], color=HEAT, sw=8, tip=0.3)
        a2 = arrow([R + 0.9, -2.2, 0], [R + 0.9, -1.45, 0], color=HEAT, sw=8, tip=0.3)
        self.play(FadeIn(sun), GrowArrow(a1), run_time=self.rt(0.06))
        self.play(FadeIn(rock), GrowArrow(a2), br[0].animate.set_fill(HEAT, opacity=0.2), run_time=self.rt(0.06))
        note = T("a heat source, not a cold animal", 30, HI).move_to([0, -3.4, 0])
        self.at("does not mean a cold")
        self.play(FadeIn(note, shift=UP * 0.1), run_time=self.rt(0.05))
        self.finish()


# ---------------------------------------------------------------- s03
class S03Routes(Sc):
    def construct(self):
        bx = body(4.4, 2.2, "body", size=34).move_to([0, 0.5, 0])
        self.play(Create(bx[0]), FadeIn(bx[1]), run_time=0.3)
        self.at("Heat leaves the body")
        # radiation: up
        a_rad = arrow([0, 1.75, 0], [0, 3.0, 0], both=True)
        l_rad = T("Radiation", 32, TEXT).move_to([0, 3.35, 0])
        surf = Rectangle(width=4.4, height=0.36, stroke_color=GREY, stroke_width=2, fill_color=GREY,
                         fill_opacity=0.35).move_to([0, -1.75, 0])
        surf_l = T("surface", 24, GREY).move_to(surf)
        a_con = arrow([0, -0.65, 0], [0, -1.5, 0], both=True, sw=7, tip=0.25)
        l_con = T("Conduction", 32, TEXT).move_to([0, -2.45, 0])
        a_cv = arrow([2.45, 0.5, 0], [5.8, 0.5, 0], both=True)
        l_cv = T("Convection", 32, TEXT).move_to([4.1, 1.15, 0])
        a_ev = arrow([-2.45, 0.5, 0], [-5.8, 0.5, 0])
        l_ev = T("Evaporation", 32, TEXT).move_to([-4.1, 1.15, 0])
        self.at("Radiation is emission")
        self.play(GrowFromCenter(a_rad), FadeIn(l_rad), run_time=self.rt(0.06))
        self.at("Conduction passes")
        self.play(FadeIn(surf), FadeIn(surf_l), GrowFromCenter(a_con), FadeIn(l_con), run_time=self.rt(0.06))
        self.at("Convection is")
        wl = T("moving air or water", 24, AIR).move_to([4.1, -0.15, 0])
        self.play(GrowFromCenter(a_cv), FadeIn(l_cv), run_time=self.rt(0.05))
        self.play(FadeIn(wl), run_time=self.rt(0.03))
        self.at("Evaporation carries")
        self.play(GrowArrow(a_ev), FadeIn(l_ev), run_time=self.rt(0.06))
        vl = T("water turns to vapour", 24, AIR).move_to([-4.1, -0.15, 0])
        self.play(FadeIn(vl), run_time=self.rt(0.03))
        self.at("The first three run either way")
        key1 = VGroup(arrow([0, 0, 0], [0.9, 0, 0], both=True, sw=5, tip=0.16),
                      T("either way", 26, GREY)).arrange(RIGHT, buff=0.2).move_to([-3.3, -3.25, 0])
        self.play(Indicate(VGroup(a_rad, a_con, a_cv), color=HI, scale_factor=1.06), FadeIn(key1),
                  run_time=self.rt(0.08))
        self.at("Evaporation only removes heat")
        key2 = VGroup(arrow([0, 0, 0], [0.9, 0, 0], sw=5, tip=0.16), T("out only, and costs water", 26, GREY)
                      ).arrange(RIGHT, buff=0.2).move_to([2.6, -3.25, 0])
        self.play(Indicate(a_ev, color=HI, scale_factor=1.1), FadeIn(key2), run_time=self.rt(0.08))
        self.finish()


# ---------------------------------------------------------------- s04
def zone_curve(L, B, s, U, su):
    def f(x):
        if x < L:
            return B + s * (L - x)
        if x <= U:
            return B
        return B + su * (x - U)
    return f


class S04Zone(Sc):
    def construct(self):
        ax = Axes(x_range=[0, 10, 1], y_range=[0, 6, 1], x_length=9.6, y_length=4.6,
                  axis_config={"color": GREY, "include_ticks": False, "include_numbers": False, "stroke_width": 3},
                  tips=True).move_to([0.8, 0.45, 0])
        xl = T("air temperature", 26, GREY).move_to(ax.c2p(5, 0) + DOWN * 1.5)
        yl = T("resting metabolic rate", 26, GREY).rotate(PI / 2).next_to(ax.y_axis, LEFT, buff=0.25)
        note = T("in this sketch: relative units, invented shapes", 24, GREY).move_to([0.8, 3.45, 0])
        self.play(Create(ax), FadeIn(xl), FadeIn(yl), FadeIn(note), run_time=0.9)
        B, L, U, s, su = 1.4, 4.4, 8.0, 0.75, 1.2
        f = zone_curve(L, B, s, U, su)
        flat = ax.plot(f, x_range=[L, U], color=ZONE, stroke_width=7)
        cold = ax.plot(f, x_range=[0.05, L], color=HEAT, stroke_width=7)
        hot = ax.plot(f, x_range=[U, 9.4], color=HEAT, stroke_width=7)
        self.at("Inside the")
        zone_l = T("thermoneutral zone", 26, ZONE).move_to(ax.c2p((L + U) / 2, B + 0.62))
        self.play(Create(flat), FadeIn(zone_l), run_time=self.rt(0.06))
        self.at("at basal metabolic rate")
        bmr = T("basal rate", 26, ZONE).move_to(ax.c2p((L + U) / 2, B - 0.55))
        self.play(FadeIn(bmr), run_time=self.rt(0.03))
        self.at("Below the lower critical")
        vl = DashedLine(ax.c2p(L, 0), ax.c2p(L, B + 0.1), color=GREY, stroke_width=3)
        ll = T("lower critical\ntemperature", 22, GREY, line_spacing=0.8).move_to(ax.c2p(L, 0) + DOWN * 0.6)
        self.play(Create(vl), Create(cold), FadeIn(ll), run_time=self.rt(0.08))
        self.at("Above the upper critical")
        vu = DashedLine(ax.c2p(U, 0), ax.c2p(U, B + 0.1), color=GREY, stroke_width=3)
        ul = T("upper critical\ntemperature", 22, GREY, line_spacing=0.8).move_to(ax.c2p(U, 0) + DOWN * 0.6)
        self.play(Create(vu), Create(hot), FadeIn(ul), run_time=self.rt(0.08))
        self.at("panting and sweating")
        pan = T("panting, sweating", 26, HEAT).move_to(ax.c2p(8.5, 3.9))
        self.play(FadeIn(pan), run_time=self.rt(0.03))
        self.at("In 1950")
        tag1 = T("thin fur\n(tropical)", 24, HEAT, line_spacing=0.8).move_to(ax.c2p(2.9, 4.5))
        self.play(FadeOut(pan), FadeIn(tag1), run_time=self.rt(0.04))
        self.at("arctic mammals stay")
        L2, s2 = 1.9, 0.38
        f2 = zone_curve(L2, B, s2, U, su)
        arc = ax.plot(f2, x_range=[0.05, L], color=AIR, stroke_width=7)
        tag2 = T("thick fur\n(arctic)", 24, AIR, line_spacing=0.8).move_to(ax.c2p(0.95, 0.75))
        self.play(Create(arc), FadeIn(tag2), run_time=self.rt(0.07))
        self.at("stay flat")
        vl2 = DashedLine(ax.c2p(L2, 0), ax.c2p(L2, B + 0.1), color=AIR, stroke_width=3)
        self.play(Create(vl2), run_time=self.rt(0.05))
        self.at("much colder air")
        la = Arrow(ax.c2p(L - 0.3, 0.55), ax.c2p(L2 + 0.35, 0.55), buff=0, color=HI, stroke_width=6)
        self.play(GrowArrow(la), run_time=self.rt(0.06))
        self.finish()


# ---------------------------------------------------------------- s05
class S05Numbers(Sc):
    def construct(self):
        ax = Axes(x_range=[10, 30, 5], y_range=[0, 0.6, 0.2], x_length=6.9, y_length=4.9,
                  axis_config={"color": GREY, "stroke_width": 3, "include_numbers": False, "include_ticks": True,
                               "tick_size": 0.08}, tips=False).move_to([2.5, -0.35, 0])
        xt = VGroup(*[M(str(v), 24, GREY).move_to(ax.c2p(v, 0) + DOWN * 0.32) for v in (10, 20, 30)])
        yt = VGroup(*[M(f"{v:.1f}", 24, GREY).move_to(ax.c2p(10, v) + LEFT * 0.55) for v in (0.2, 0.4, 0.6)])
        xl = T("air temperature (°C)", 26, GREY).move_to(ax.c2p(20, 0) + DOWN * 0.9)
        yl = T("heat production (W)", 26, GREY).rotate(PI / 2).move_to(ax.c2p(10, 0.3) + LEFT * 1.15)
        inv = T("invented numbers, below the lower critical temperature", 24, GREY).move_to([2.0, 3.4, 0])
        slope = T("steepness approximates conductance:\nhow readily heat leaks out\nper degree of difference", 24, HEAT,
                  line_spacing=0.8).move_to(ax.c2p(24.5, 0.5))
        self.play(Create(ax), FadeIn(xt), FadeIn(yt), FadeIn(xl), FadeIn(yl), FadeIn(inv), run_time=0.25)
        C1, C2 = 0.020, 0.010
        l1 = ax.plot(lambda x: C1 * (37 - x), x_range=[10, 30], color=HEAT, stroke_width=7)
        self.at("The steepness of the cold limb")
        self.play(Create(l1), run_time=0.7)
        self.at("thermal conductance")
        self.play(FadeIn(slope), run_time=0.6)
        self.at("These numbers are invented")
        self.play(Indicate(inv, color=HI, scale_factor=1.05), run_time=self.rt(0.05))
        self.at("small endotherm holds")
        c1 = M("C = 0.020 W per K", 26, HEAT).move_to([-4.35, 2.5, 0])
        b1 = M("body 37 °C", 26, TEXT).move_to([-4.35, 1.8, 0])
        self.play(FadeIn(c1), FadeIn(b1), FadeOut(slope), run_time=self.rt(0.05))

        def mark(Ta, col=HI):
            y = C1 * (37 - Ta)
            d = Dot(ax.c2p(Ta, y), color=col, radius=0.11)
            v = DashedLine(ax.c2p(Ta, 0), ax.c2p(Ta, y), color=col, stroke_width=3)
            h = DashedLine(ax.c2p(10, y), ax.c2p(Ta, y), color=col, stroke_width=3)
            return d, v, h

        self.at("the gap is")
        d1, v1, h1 = mark(27)
        gap1 = M("37 − 27 = 10 K", 26, TEXT).move_to([-4.35, 0.7, 0])
        self.play(Create(v1), Create(d1), Create(h1), FadeIn(gap1), run_time=self.rt(0.06))
        self.at("so it makes")
        r1 = M("0.20 W", 30, HI, weight=BOLD).next_to(d1, UP, buff=0.4).shift(RIGHT * 0.2)
        self.play(FadeIn(r1, scale=1.2), run_time=self.rt(0.04))
        self.at("the gap is", nth=1)
        d2, v2, h2 = mark(17)
        gap2 = M("37 − 17 = 20 K", 26, TEXT).move_to([-4.35, -0.1, 0])
        self.play(Create(v2), Create(d2), Create(h2), FadeIn(gap2), run_time=self.rt(0.06))
        self.at("so it makes", nth=1)
        r2 = M("0.40 W", 30, HI, weight=BOLD).next_to(d2, UR, buff=0.2)
        self.play(FadeIn(r2, scale=1.2), run_time=self.rt(0.04))
        self.at("Fluff the fur")
        c2 = M("C = 0.010 W per K", 26, AIR).move_to([-4.35, -1.3, 0])
        l2 = ax.plot(lambda x: C2 * (37 - x), x_range=[10, 30], color=AIR, stroke_width=7)
        self.play(FadeIn(c2), Create(l2), run_time=self.rt(0.07))
        self.at("that cost drops back")
        d3 = Dot(ax.c2p(17, C2 * 20), color=AIR, radius=0.11)
        r3 = M("0.20 W", 30, AIR, weight=BOLD).next_to(d3, DL, buff=0.2)
        self.play(FadeIn(d3, scale=1.5), FadeIn(r3), run_time=self.rt(0.06))
        self.finish()


# ---------------------------------------------------------------- s06
class S06Setpoint(Sc):
    def construct(self):
        ax_x = -2.8
        scale = Arrow([ax_x, -3.1, 0], [ax_x, 3.2, 0], buff=0, color=GREY, stroke_width=4, tip_length=0.25)
        sl = T("body temperature", 26, GREY).rotate(PI / 2).move_to([ax_x - 0.55, 0, 0])
        nts = T("not to scale", 24, GREY).move_to([ax_x + 1.8, -3.25, 0])
        line = Line([ax_x + 0.3, 0, 0], [ax_x + 3.8, 0, 0], color=SETP, stroke_width=9)
        lab = T("set point", 32, SETP).next_to(line, UP, buff=0.12).align_to(line, LEFT)
        grp = VGroup(line, lab)
        self.play(Create(scale), FadeIn(sl), FadeIn(nts), run_time=0.3)
        self.at("A set point is")
        self.play(Create(line), FadeIn(lab), run_time=self.rt(0.05))
        self.at("In fever")
        f = chip("fever: raised", UP_C, size=32).move_to([4.2, 1.8, 0])
        self.play(grp.animate.shift(UP * 1.8), FadeIn(f, shift=UP * 0.1), run_time=self.rt(0.07))
        self.at("In torpor")
        t = chip("torpor: drops", AIR, size=32).move_to([4.2, -1.8, 0])
        self.play(grp.animate.shift(DOWN * 3.6), FadeOut(f), FadeIn(t, shift=DOWN * 0.1), run_time=self.rt(0.07))
        self.at("In hibernating American")
        left = VGroup(scale, sl, nts, grp, t)
        self.play(FadeOut(left), run_time=0.6)
        base_y, H = -2.7, 4.6
        b1 = Rectangle(width=2.0, height=H, stroke_color=ZONE, stroke_width=3, fill_color=ZONE, fill_opacity=0.45
                       ).move_to([-4.2, base_y + H / 2, 0])
        b1l = VGroup(T("basal rate", 26, ZONE), T("100%", 28, ZONE)).arrange(DOWN, buff=0.1).next_to(b1, DOWN, buff=0.15)
        b2 = Rectangle(width=2.0, height=H * 0.25, stroke_color=HEAT, stroke_width=3, fill_color=HEAT, fill_opacity=0.5
                       ).move_to([-1.5, base_y + H * 0.125, 0])
        b2l = VGroup(T("black bear", 26, HEAT), T("25%", 28, HEAT)).arrange(DOWN, buff=0.1).next_to(b2, DOWN, buff=0.15)
        hdr = T("hibernating American black bear", 30, TEXT).move_to([-2.85, 3.3, 0])
        self.play(FadeIn(hdr), FadeIn(b1), FadeIn(b1l), run_time=0.6)
        self.at("metabolism fell to")
        self.play(FadeIn(b2), FadeIn(b2l), run_time=0.6)
        self.at("body temperature stayed")
        bt = VGroup(T("body temperature", 30, GOLD), T("30 to 36 °C", 30, GOLD)).arrange(DOWN, buff=0.12)
        bb = RoundedRectangle(corner_radius=0.14, width=bt.width + 0.5, height=bt.height + 0.4, stroke_color=GOLD,
                              stroke_width=2.5, fill_color=GOLD, fill_opacity=0.16)
        band = VGroup(bb, bt.move_to(bb)).move_to([3.5, 1.5, 0])
        self.play(FadeIn(band, shift=LEFT * 0.1), run_time=self.rt(0.05))
        self.at("Cooling alone does not")
        ncl = T("not explained by\ncooling alone", 32, UP_C, line_spacing=0.85).move_to([3.5, -0.9, 0])
        self.play(FadeIn(ncl, shift=UP * 0.1), run_time=self.rt(0.05))
        self.at("Keep one rule")
        everything = VGroup(b1, b1l, b2, b2l, hdr, band, ncl)
        self.play(FadeOut(everything), run_time=self.rt(0.04))
        eq1 = chip("heat made", HEAT, size=44).move_to([-2.6, 1.2, 0])
        eqs = T("=", 52, TEXT).move_to([0, 1.2, 0])
        eq2 = chip("heat lost", HEAT, size=44).move_to([2.6, 1.2, 0])
        ss = T("for an endotherm, at steady state", 30, GREY).move_to([0, 0.0, 0])
        sp = chip("the temperature it defends can shift", SETP, size=38).move_to([0, -1.4, 0])
        self.at("endotherm at steady state")
        self.play(FadeIn(eq1), FadeIn(eqs), FadeIn(eq2), FadeIn(ss), run_time=self.rt(0.05))
        self.at("the temperature it defends")
        self.play(FadeIn(sp, shift=UP * 0.1), run_time=self.rt(0.05))
        self.finish()
