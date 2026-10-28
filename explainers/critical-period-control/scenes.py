"""Opening and closing a critical period: a window held by a threshold  (Biochemistrypedia explainer)

COLOR MAP (one color per concept, whole video)
  BLUE   = the closed eye and the cortex response to it
  ORANGE = the open eye and the cortex response to it
  YELLOW = inhibition (GABA, the inhibition meter, parvalbumin cells)
  PURPLE = the GAD enzymes that make GABA
  PINK   = the GABA receptor
  TEAL   = diazepam
  GREEN  = the open window (plasticity possible)
  RED    = missing or blocked: the knockout, and the brakes
  GREY   = structure, frames, labels
"""
import numpy as np
from bp_style import *  # noqa: F401,F403

PURPLE = "#B58CD9"
ORANGE = "#F29E4C"
PINK = "#E58FB8"


# ---------------------------------------------------------------------------------------------
# helpers
# ---------------------------------------------------------------------------------------------
def bchip(text, color=BLUE, size=26, **kw):
    c = chip(text, color, size=size, **kw)
    back = RoundedRectangle(corner_radius=0.14, width=c[0].width, height=c[0].height, stroke_width=0,
                            fill_color=BG, fill_opacity=1).move_to(c[0])
    return VGroup(back, *c)


def arr(a, b, color=GREY, w=5, tip=0.22):
    return Arrow(a, b, buff=0.06, color=color, stroke_width=w, tip_length=tip,
                 max_tip_length_to_length_ratio=0.45, max_stroke_width_to_length_ratio=12)


def inhib(a, b, color=RED, w=5):
    a, b = np.array(a, float), np.array(b, float)
    d = (b - a) / np.linalg.norm(b - a)
    b = b - d * 0.05
    perp = np.array([-d[1], d[0], 0])
    return VGroup(Line(a, b, color=color, stroke_width=w), Line(b + perp * 0.26, b - perp * 0.26, color=color, stroke_width=w + 1))


def eye_open(color):
    return VGroup(Ellipse(width=0.9, height=0.5, stroke_color=color, stroke_width=4, fill_color=color, fill_opacity=0.15),
                  Dot(radius=0.12, color=color))


def eye_shut(color):
    lid = ArcBetweenPoints(LEFT * 0.45, RIGHT * 0.45, angle=-PI / 2.6, stroke_color=color, stroke_width=5)
    lashes = VGroup(*[Line(lid.point_from_proportion(p), lid.point_from_proportion(p) + DOWN * 0.12 + RIGHT * dx,
                           stroke_color=color, stroke_width=3) for p, dx in ((0.2, -0.04), (0.5, 0), (0.8, 0.04))])
    return VGroup(lid, lashes)


BASE = -1.85   # bottom of the cortex-response bars


def mkbar(x, h, color):
    h = max(h, 0.03)
    return Rectangle(width=1.1, height=h, stroke_width=0, fill_color=color, fill_opacity=0.85).move_to([x, BASE + h / 2, 0])


class Panel:
    """Cortex-response panel: two bars (closed eye, open eye), the eyes below them."""

    def __init__(self, cx, title, hc=2.2, ho=2.2, sub="cortex response", subcolor=GREY):
        self.cx = cx
        self.frame = RoundedRectangle(corner_radius=0.2, width=5.4, height=6.5, stroke_color=GREY, stroke_width=2).move_to([cx, -0.1, 0])
        self.title = T(title, 30, TEXT, weight=BOLD).move_to([cx, 2.65, 0])
        self.sub = T(sub, 22, subcolor).move_to([cx, 2.15, 0])
        self.bc = mkbar(cx - 1.0, hc, BLUE)
        self.bo = mkbar(cx + 1.0, ho, ORANGE)
        self.ec = eye_open(BLUE).move_to([cx - 1.0, -2.45, 0])
        self.eo = eye_open(ORANGE).move_to([cx + 1.0, -2.45, 0])
        self.lc = T("closed eye", 22, BLUE).move_to([cx - 1.0, -3.0, 0])
        self.lo = T("open eye", 22, ORANGE).move_to([cx + 1.0, -3.0, 0])
        self.everything = VGroup(self.frame, self.title, self.sub, self.bc, self.bo, self.ec, self.eo, self.lo)

    def close_eye(self):
        self.ec_new = eye_shut(BLUE).move_to(self.ec)
        return AnimationGroup(ReplacementTransform(self.ec, self.ec_new), FadeIn(self.lc))

    def set_bars(self, hc, ho):
        return [Transform(self.bc, mkbar(self.cx - 1.0, hc, BLUE)), Transform(self.bo, mkbar(self.cx + 1.0, ho, ORANGE))]


class S00Title(TitleCard):
    LESSON = "Opening and closing a critical period"
    TITLE = "A window held by a threshold"


# ---------------------------------------------------------------------------------------------
class S01Question(SpokenScene):
    """Young cortex shifts to the open eye; adult barely; what opens the window? age?"""

    def construct(self):
        young = Panel(-3.55, "young mouse")
        adult = Panel(3.55, "adult mouse")
        self.at("Close one eye")
        self.play(FadeIn(young.everything), run_time=0.8)
        self.at("for a few days")
        self.play(young.close_eye(), run_time=0.6)
        self.at("answers that eye")
        self.play(*young.set_bars(0.8, 3.2), run_time=1.2)
        self.at("Do the same to an adult")
        self.play(FadeIn(adult.everything), run_time=0.8)
        self.play(adult.close_eye(), run_time=0.5)
        self.at("far less happens")
        self.play(*adult.set_bars(1.95, 2.3), run_time=0.9)
        self.at("what opens the window")
        q = T("?", 96, YELLOW, weight=BOLD).move_to([0, 0.5, 0])
        self.play(FadeIn(q, scale=0.6), run_time=0.6)
        self.at("simply age")
        agechip = bchip("age?", GREY, 26).move_to([0, -0.7, 0])
        self.play(FadeIn(agechip, shift=UP * 0.15), run_time=0.5)
        self.finish()


# ---------------------------------------------------------------------------------------------
class S02Knockout(SpokenScene):
    """GAD65 is missing; the knockout cortex does not shift."""

    def construct(self):
        pan = Panel(3.55, "knockout mouse")
        self.at("A knockout mouse")
        self.play(FadeIn(pan.everything), run_time=0.8)

        glut = bchip("glutamate", GREY, 26).move_to([-3.2, 2.5, 0])
        g67 = bchip("GAD67", PURPLE, 26).move_to([-4.85, 0.5, 0])
        g65 = bchip("GAD65", PURPLE, 26).move_to([-1.55, 0.5, 0])
        gaba = bchip("GABA", YELLOW, 30).move_to([-3.2, -1.5, 0])
        a1 = arr(glut.get_bottom() + LEFT * 0.4, g67.get_top(), GREY)
        a2 = arr(glut.get_bottom() + RIGHT * 0.4, g65.get_top(), GREY)
        a3 = arr(g67.get_bottom(), gaba.get_left() + UP * 0.2, PURPLE)
        a4 = arr(g65.get_bottom(), gaba.get_right() + UP * 0.2, PURPLE)
        self.at("two enzymes")
        self.play(FadeIn(glut), run_time=0.4)
        self.play(GrowArrow(a1), GrowArrow(a2), FadeIn(g67), FadeIn(g65), run_time=0.7)
        self.play(GrowArrow(a3), GrowArrow(a4), FadeIn(gaba), run_time=0.7)
        note = T("GAD65 supplies GABA\nwhen neurons fire hard", 24, PURPLE, line_spacing=0.8).move_to([-3.2, -3.0, 0])
        self.at("supplies GABA")
        self.play(Indicate(g65, color=PURPLE, scale_factor=1.1), FadeIn(note), run_time=0.8)

        missing = T("missing", 24, RED, weight=BOLD).move_to([0.12, 0.5, 0])
        self.at("without it")
        self.play(FadeIn(missing), g65[1].animate.set_stroke(RED), g65[2].animate.set_color(RED),
                  a4.animate.set_opacity(0.2), run_time=0.8)
        self.at("no shift")
        ns = T("no shift", 24, RED, weight=BOLD).move_to(pan.sub)
        self.play(ReplacementTransform(pan.sub, ns), run_time=0.4)
        self.at("after an eye is closed")
        self.play(pan.close_eye(), run_time=0.5)
        self.at("still respond to vision")
        self.play(Indicate(pan.bc, color=BLUE, scale_factor=1.06), Indicate(pan.bo, color=ORANGE, scale_factor=1.06), run_time=1.0)
        self.at("What failed was the change")
        self.play(Indicate(ns, color=RED, scale_factor=1.15), run_time=0.8)
        self.finish()


# ---------------------------------------------------------------------------------------------
class S03Diazepam(SpokenScene):
    """Diazepam boosts the receptor response; an inhibition meter must pass a threshold."""

    def construct(self):
        ML, MW, MH, MB = 2.6, 1.8, 4.9, -2.65     # meter centre x, width, height, bottom
        def fill(level, color=YELLOW):
            h = max(level * (MH - 0.12), 0.03)
            return Rectangle(width=MW - 0.12, height=h, stroke_width=0, fill_color=color, fill_opacity=0.8).move_to([ML, MB + 0.06 + h / 2, 0])
        outline = Rectangle(width=MW, height=MH, stroke_color=GREY, stroke_width=4).move_to([ML, MB + MH / 2, 0])
        nub = Rectangle(width=0.5, height=0.2, stroke_color=GREY, stroke_width=4).move_to([ML, MB + MH + 0.1, 0])
        level = fill(0.25)
        ty = MB + 0.06 + 0.62 * (MH - 0.12)
        thr = DashedLine([ML - 1.2, ty, 0], [ML + 1.2, ty, 0], color=TEXT, stroke_width=4)
        thr_l = T("threshold", 24, TEXT).move_to([ML - 2.0, ty, 0])
        title = T("inhibition level", 26, YELLOW).move_to([ML, 3.1, 0])
        ko = bchip("knockout", RED, 24).move_to([5.2, 2.0, 0])
        lamp = Circle(radius=0.5, stroke_color=GREY, stroke_width=4, fill_color=GREY, fill_opacity=0.3).move_to([5.2, 0.6, 0])
        wlab = T("window", 24, GREY).move_to([5.2, -0.3, 0])
        wst = T("closed", 24, GREY).move_to([5.2, -0.8, 0])
        rt = VGroup(title, outline, nub, level, thr, thr_l, ko, lamp, wlab, wst)
        self.play(FadeIn(rt), run_time=0.2)

        # receptor
        L1 = RoundedRectangle(corner_radius=0.1, width=1.3, height=0.7, stroke_color=PINK, stroke_width=4, fill_color=PINK, fill_opacity=0.35).move_to([-5.35, 0.3, 0])
        R1 = RoundedRectangle(corner_radius=0.1, width=1.3, height=0.7, stroke_color=PINK, stroke_width=4, fill_color=PINK, fill_opacity=0.35).move_to([-2.85, 0.3, 0])
        rec_l = T("receptor", 22, PINK).move_to([-5.35, -0.35, 0])
        dz = bchip("diazepam", TEAL, 24).move_to([-2.4, 2.9, 0])
        gdot = Circle(radius=0.2, stroke_color=YELLOW, stroke_width=3, fill_color=YELLOW, fill_opacity=0.9).move_to([-4.1, 2.0, 0])
        glab = T("GABA", 24, YELLOW).move_to([-5.3, 2.0, 0])
        self.at("Now add diazepam")
        self.play(FadeIn(dz, shift=DOWN * 0.2), FadeIn(L1), FadeIn(R1), FadeIn(rec_l), FadeIn(gdot), FadeIn(glab), run_time=0.8)
        thin = arr([-4.1, -0.1, 0], [-4.1, -1.9, 0], TEXT, w=3, tip=0.18)
        resp = T("response", 22, TEXT).move_to([-4.1, -2.35, 0])
        self.at("GABA receptor")
        self.play(gdot.animate.move_to([-4.1, 0.3, 0]), run_time=0.5)
        self.play(GrowArrow(thin), FadeIn(resp), run_time=0.4)
        self.at("respond more strongly")
        thick = arr([-4.1, -0.1, 0], [-4.1, -1.9, 0], TEXT, w=12, tip=0.4)
        self.play(dz.animate.move_to([-2.7, 1.25, 0]), run_time=0.5)
        self.play(Transform(thin, thick), run_time=0.6)
        self.at("cannot open")
        alone = T("alone: no response", 22, GREY).move_to([-4.1, -1.2, 0])
        self.play(FadeOut(gdot), FadeOut(thin), FadeOut(resp), run_time=0.3)
        self.play(FadeIn(alone), run_time=0.3)

        # the battery picture; the left side clears and the meter moves to the middle
        left = VGroup(L1, R1, rec_l, glab, alone)
        self.at("smoke detector")
        self.play(FadeOut(left), dz.animate.move_to([-4.6, -1.2, 0]), rt.animate.shift(LEFT * 2.6), run_time=1.0)
        self.play(Indicate(thr, color=TEXT, scale_factor=1.1), Indicate(thr_l, color=TEXT, scale_factor=1.1), run_time=0.8)
        self.at("battery is low")
        self.play(Indicate(level, color=RED, scale_factor=1.05), run_time=0.8)
        da = arr([-3.4, -1.2, 0], [-1.05, -1.2, 0], TEAL, w=6)
        self.at("tops it up")
        new = fill(0.85).shift(LEFT * 2.6)
        self.play(GrowArrow(da), run_time=0.4)
        self.play(Transform(level, new), run_time=1.0)
        lamp_on = Circle(radius=0.5, stroke_color=GREEN, stroke_width=5, fill_color=GREEN, fill_opacity=0.9).move_to(lamp)
        wst_on = T("open", 24, GREEN).move_to(wst)
        self.play(Transform(lamp, lamp_on), ReplacementTransform(wst, wst_on), wlab.animate.set_color(GREEN), run_time=0.6)

        # restores the shift
        bx = 5.0
        mb_c = Rectangle(width=0.8, height=0.8, stroke_width=0, fill_color=BLUE, fill_opacity=0.85).move_to([bx - 0.55, -2.4 + 0.4, 0])
        mb_o = Rectangle(width=0.8, height=2.4, stroke_width=0, fill_color=ORANGE, fill_opacity=0.85).move_to([bx + 0.55, -2.4 + 1.2, 0])
        ml = T("cortex shifts", 24, TEXT).move_to([bx, 0.45, 0])
        mlc = T("closed", 22, BLUE).move_to([bx - 0.55, -2.8, 0])
        mlo = T("open", 22, ORANGE).move_to([bx + 0.55, -2.8, 0])
        self.at("restores the shift")
        self.play(FadeIn(ml), FadeIn(mb_c), FadeIn(mb_o), FadeIn(mlc), FadeIn(mlo), run_time=0.8)
        self.finish()


# ---------------------------------------------------------------------------------------------
class S04NotAge(SpokenScene):
    """Age axis: normal window; knockout opened late by diazepam; normal mouse opened and closed early."""

    def construct(self):
        def X(a):
            return -5.8 + (a - 10) * 0.1967

        def win(a0, a1, y, label=None, opacity=0.55):
            r = RoundedRectangle(corner_radius=0.1, width=X(a1) - X(a0), height=0.5, stroke_color=GREEN, stroke_width=3,
                                 fill_color=GREEN, fill_opacity=opacity).move_to([(X(a0) + X(a1)) / 2, y, 0])
            return r

        ay = -2.4
        axis = Arrow([X(10), ay, 0], [X(70) + 0.2, ay, 0], buff=0, color=GREY, stroke_width=3, tip_length=0.2)
        ticks = VGroup()
        for a in (15, 28, 60):
            ticks.add(Line([X(a), ay - 0.1, 0], [X(a), ay + 0.1, 0], color=GREY, stroke_width=3))
            ticks.add(T(f"P{a}", 22, GREY).move_to([X(a), ay - 0.45, 0]))
        age = T("age", 24, GREY).move_to([5.6, ay - 0.45, 0])
        self.play(Create(axis), FadeIn(ticks), FadeIn(age), run_time=0.8)

        Y1, Y2, Y3 = 2.3, 0.6, -1.4
        l1 = T("normal mouse", 24, TEXT).move_to([X(19), Y1 + 0.5, 0], aligned_edge=LEFT)
        w1 = win(19, 32, Y1)
        w1t = T("window", 22, TEXT).move_to(w1)
        self.at("normal mouse has its window")
        self.play(FadeIn(l1), GrowFromEdge(w1, LEFT), run_time=0.8)
        self.play(FadeIn(w1t), run_time=0.3)

        l3 = T("knockout mouse", 24, RED).move_to([X(19), Y3 + 0.5, 0], aligned_edge=LEFT)
        dash = DashedVMobject(RoundedRectangle(corner_radius=0.1, width=X(70) - X(19), height=0.5, stroke_color=GREEN, stroke_width=3)
                              .move_to([(X(19) + X(70)) / 2, Y3, 0]), num_dashes=70)
        cap = T("capacity kept", 22, GREEN).move_to([-1.2, Y3, 0])
        self.at("Knockouts kept")
        self.play(FadeIn(l3), Create(dash), run_time=1.0)
        self.at("into adulthood")
        self.play(FadeIn(cap), run_time=0.5)

        dz3 = arr([X(60), Y3 + 1.0, 0], [X(60), Y3 + 0.3, 0], TEAL, w=6)
        dz3l = T("diazepam", 22, TEAL).move_to([X(60) + 0.2, Y3 + 1.0, 0], aligned_edge=LEFT)
        w3 = VGroup(*[win(60 + 2.5 * k, 62.5 + 2.5 * k, Y3, opacity=o).set_stroke(width=0 if k else 3)
                      for k, o in enumerate((0.55, 0.4, 0.25, 0.1))])
        w3n = T("duration not shown", 22, GREY).move_to([4.7, Y3 - 0.55, 0])
        self.at("diazepam triggered")
        self.play(GrowArrow(dz3), FadeIn(dz3l), run_time=0.5)
        self.play(GrowFromEdge(w3, LEFT), FadeIn(w3n), run_time=0.7)

        l2 = T("normal mouse, early diazepam", 24, TEXT).move_to([X(15), Y2 + 0.5, 0], aligned_edge=LEFT)
        dz2 = arr([X(15), Y2 - 1.0, 0], [X(15), Y2 - 0.3, 0], TEAL, w=6)
        dz2l = T("diazepam", 22, TEAL).move_to([X(15) + 0.2, Y2 - 1.0, 0], aligned_edge=LEFT)
        w2 = win(15, 25, Y2)
        self.at("In normal young mice")
        self.play(FadeIn(l2), run_time=0.5)
        self.at("before the usual opening")
        self.play(GrowArrow(dz2), FadeIn(dz2l), run_time=0.5)
        self.at("started the window early")
        self.play(GrowFromEdge(w2, LEFT), run_time=1.0)
        end_l = T("ends early (schematic)", 22, GREY).move_to([X(25) + 0.25, Y2, 0], aligned_edge=LEFT)
        self.at("also ended early")
        self.play(FadeIn(end_l), Indicate(w2, color=GREEN, scale_factor=1.04), run_time=0.8)
        self.finish()


# ---------------------------------------------------------------------------------------------
class S05Brakes(SpokenScene):
    """Window held shut by three brakes; lifting one lets the window open."""

    def construct(self):
        WB = -3.2       # window bottom
        HT = 1.2        # window thickness when open
        def winbar(h, op=0.55):
            return Rectangle(width=11.4, height=h, stroke_color=GREEN, stroke_width=3, fill_color=GREEN, fill_opacity=op).move_to([0, WB + h / 2, 0])
        win = winbar(HT)
        wl = T("window", 28, TEXT).move_to([0, WB + HT / 2, 0])
        self.play(FadeIn(win), FadeIn(wl), run_time=0.6)

        # a window that simply faded
        faded = T("faded", 28, GREY).move_to(wl)
        self.at("need")
        self.play(win.animate.set_fill(opacity=0.08).set_stroke(opacity=0.3), ReplacementTransform(wl, faded), run_time=1.2)
        cr = T("machinery remains", 24, GREY).move_to([0, WB + HT + 0.9, 0])
        self.at("machinery")
        self.play(Create(cr), run_time=0.5)
        self.at("held shut by")
        wl = T("window", 28, TEXT).move_to([0, WB + HT / 2, 0])
        self.play(FadeOut(cr), win.animate.set_fill(opacity=0.55).set_stroke(opacity=1), ReplacementTransform(faded, wl), run_time=0.8)

        xs = [-4.2, 0.0, 4.2]
        ytop = [-0.55, 0.5, 0.5]
        def bar_to(i, h):
            return inhib([xs[i], ytop[i], 0], [xs[i], WB + h, 0])
        tbs = [None, None, None]

        # brake 1: matrix net around a parvalbumin cell
        cell = Circle(radius=0.6, stroke_color=YELLOW, stroke_width=4, fill_color=YELLOW, fill_opacity=0.3).move_to([xs[0], 1.5, 0])
        net = VGroup(Circle(radius=0.95, stroke_color=RED, stroke_width=5).move_to(cell), Circle(radius=1.25, stroke_color=RED, stroke_width=5).move_to(cell))
        for k in range(12):
            ang = k * TAU / 12
            d = np.array([np.cos(ang), np.sin(ang), 0])
            net.add(Line(cell.get_center() + d * 0.95, cell.get_center() + d * 1.25, color=RED, stroke_width=4))
        cell_l = T("parvalbumin cell", 22, YELLOW).move_to([xs[0], 3.05, 0])
        net_l = T("matrix net", 24, RED).move_to([xs[0], -0.1, 0])
        self.at("matrix condenses")
        self.play(FadeIn(cell), FadeIn(cell_l), run_time=0.4)
        self.play(Create(net), FadeIn(net_l), run_time=0.8)
        tbs[0] = bar_to(0, 0.9)
        self.play(Create(tbs[0]), Transform(win, winbar(0.9)), wl.animate.move_to([0, WB + 0.45, 0]), run_time=0.7)

        # brake 2: myelin signal -> Nogo receptor
        my = bchip("myelin signal", GREY, 24).move_to([xs[1], 2.2, 0])
        ng = bchip("Nogo receptor", RED, 24).move_to([xs[1], 0.9, 0])
        a_m = arr(my.get_bottom(), ng.get_top(), RED, w=5)
        self.at("Myelin signals")
        self.play(FadeIn(my), run_time=0.4)
        self.at("act through")
        self.play(GrowArrow(a_m), FadeIn(ng), run_time=0.5)
        tbs[1] = bar_to(1, 0.6)
        self.play(Create(tbs[1]), Transform(tbs[0], bar_to(0, 0.6)), Transform(win, winbar(0.6)),
                  wl.animate.move_to([0, WB + 0.3, 0]), run_time=0.6)

        # brake 3: Lynx1 damps nicotinic receptors
        lx = bchip("Lynx1", RED, 24).move_to([xs[2], 2.2, 0])
        nr = bchip("nicotinic receptor", GREY, 24).move_to([xs[2], 0.9, 0])
        a_l = inhib(lx.get_bottom(), nr.get_top(), RED)
        self.at("a protein called")
        self.play(FadeIn(lx), run_time=0.4)
        self.at("nicotinic receptors")
        self.play(Create(a_l), FadeIn(nr), run_time=0.5)
        tbs[2] = bar_to(2, 0.2)
        self.play(Create(tbs[2]), Transform(tbs[0], bar_to(0, 0.2)), Transform(tbs[1], bar_to(1, 0.2)),
                  Transform(win, winbar(0.2)), FadeOut(wl), run_time=0.6)

        # taking away brakes, one by one
        adult = T("adult rodents", 24, GREY).move_to([5.0, 3.05, 0])
        self.at("In adult rodents")
        self.play(FadeIn(adult), run_time=0.4)
        t_each = T("each one alone", 22, GREY).move_to([-2.1, -1.0, 0])
        t_unset = T("how they interact\nis not settled", 22, GREY, line_spacing=0.8).move_to([2.1, -1.0, 0])
        wl = T("plastic", 28, TEXT).move_to([0, WB + HT / 2, 0])
        def lift(parts, others):
            return [FadeOut(p) for p in parts] + [FadeOut(o) for o in others] + [Transform(win, winbar(HT)), FadeIn(wl)]
        def reset(parts, others):
            return [FadeIn(p) for p in parts] + [FadeIn(o) for o in others] + [Transform(win, winbar(0.2)), FadeOut(wl)]
        P1, P2, P3 = [net, net_l, tbs[0]], [ng, a_m, tbs[1]], [lx, a_l, tbs[2]]
        self.at("taking away")
        self.play(*lift(P1, [tbs[1], tbs[2]]), FadeIn(t_each), FadeIn(t_unset), run_time=0.8)
        self.at("kept plasticity")
        self.play(*reset(P1, [tbs[1], tbs[2]]), run_time=0.5)
        self.play(*lift(P2, [tbs[0], tbs[2]]), run_time=0.8)
        self.at("restored it")
        self.play(*reset(P2, [tbs[0], tbs[2]]), run_time=0.5)
        self.play(*lift(P3, [tbs[0], tbs[1]]), run_time=0.8)
        self.finish()


# ---------------------------------------------------------------------------------------------
class S06State(SpokenScene):
    """One plot: inhibition crosses a threshold, the window opens, brakes end it; both ends can move."""

    def construct(self):
        ox, oy = -5.6, -2.3
        ymin, ymax = -2.1, 1.7

        def f(x, x0):
            return ymin + (ymax - ymin) / (1 + np.exp(-(x - x0) / 0.9))

        yt = ymin + 0.6 * (ymax - ymin)

        def parts(x0, xb):
            xc = x0 + 0.9 * np.log(1.5)
            curve = ParametricFunction(lambda t: np.array([t, f(t, x0), 0]), t_range=[ox, 5.4], color=YELLOW, stroke_width=6)
            dot = Dot([xc, yt, 0], radius=0.13, color=TEXT)
            win = RoundedRectangle(corner_radius=0.1, width=xb - xc, height=0.6, stroke_color=GREEN, stroke_width=3,
                                   fill_color=GREEN, fill_opacity=0.55).move_to([(xc + xb) / 2, 2.85, 0])
            g1 = DashedLine([xc, yt, 0], [xc, 2.55, 0], color=GREEN, stroke_width=3)
            g2 = DashedLine([xb, oy, 0], [xb, 2.55, 0], color=RED, stroke_width=3)
            bk = bchip("inhibition\n+ brakes", RED, 22).move_to([xb, oy + 0.75, 0])
            return VGroup(curve, dot, win, g1, g2, bk)

        axes = VGroup(Line([ox, oy, 0], [5.6, oy, 0], color=GREY, stroke_width=3),
                      Line([ox, oy, 0], [ox, 2.0, 0], color=GREY, stroke_width=3))
        yl = T("inhibition", 24, YELLOW).move_to([ox + 1.0, 2.2, 0])
        xl = T("age", 24, GREY).move_to([5.3, oy - 0.4, 0])
        thr = DashedLine([ox, yt, 0], [5.6, yt, 0], color=TEXT, stroke_width=3)
        thr_l = T("threshold", 24, TEXT).move_to([ox + 1.0, yt + 0.4, 0])
        A = parts(-1.5, 2.9)
        self.play(Create(axes), FadeIn(yl), FadeIn(xl), run_time=0.6)
        self.at("reach a threshold")
        self.play(Create(A[0]), run_time=1.0)
        self.play(Create(thr), FadeIn(thr_l), FadeIn(A[1]), run_time=0.4)
        self.at("start the window")
        wlab = T("window", 24, TEXT).move_to(A[2])
        self.play(GrowFromEdge(A[2], LEFT), Create(A[3]), run_time=0.6)
        self.play(FadeIn(wlab), run_time=0.3)
        self.at("breaks")
        self.play(Create(A[4]), FadeIn(A[5]), run_time=0.8)
        self.at("does not shift the cortex")
        self.wait(0.05)
        wlab2 = T("responds to deprivation", 22, TEXT).move_to(A[2])
        self.at("lets the cortex respond")
        self.play(ReplacementTransform(wlab, wlab2), Indicate(A[2], color=GREEN, scale_factor=1.03), run_time=0.8)

        B = parts(-2.8, 3.9)
        gen = bchip("genes", GREY, 24)
        drg = bchip("drugs", GREY, 24)
        exp = bchip("experience", GREY, 24)
        row = VGroup(gen, drg, exp).arrange(RIGHT, buff=0.35).move_to([0, -3.05, 0])
        wlab3 = T("responds to deprivation", 22, TEXT).move_to(B[2])
        self.at("genes")
        self.play(FadeIn(gen), run_time=0.3)
        self.at("drugs")
        self.play(FadeIn(drg), run_time=0.3)
        self.at("experience")
        self.play(FadeIn(exp), run_time=0.3)
        self.at("move both steps")
        self.play(Transform(A, B), ReplacementTransform(wlab2, wlab3), run_time=1.6)
        self.at("mechanism")
        self.wait(0.1)
        wlab4 = T("a state of a circuit", 24, TEXT).move_to(B[2])
        self.at("state of a circuit")
        self.play(ReplacementTransform(wlab3, wlab4), run_time=0.7)
        strike = Line(xl.get_left() + LEFT * 0.1, xl.get_right() + RIGHT * 0.1, color=RED, stroke_width=5)
        self.at("not an age")
        self.play(Create(strike), run_time=0.5)
        self.finish()


class S07End(EndCard):
    LINE = "A critical period is a state of a circuit, not an age."
