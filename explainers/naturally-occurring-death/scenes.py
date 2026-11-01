"""Naturally occurring neuron death: count across time  (Biochemistrypedia explainer)

Timed to the SPOKEN words: every self.at("...") cue waits for that phrase in audio/words.json.

COLOR MAP (one color per concept, whole video)
  BLUE   = motor neurons that are present / healthy, and the control (intact) side
  RED    = dying or lost neurons, the loss
  YELLOW = the manipulated limb side (operated side, grafted extra leg) and the limb itself
  GREY   = axes, outlines, hypotheses, de-emphasized
"""
import random
import numpy as np
from bp_style import *  # noqa: F401,F403


def arr(a, b, color=GREY, w=5, tip=0.22):
    return Arrow(a, b, buff=0.08, color=color, stroke_width=w, tip_length=tip,
                 max_tip_length_to_length_ratio=0.45, max_stroke_width_to_length_ratio=12)


def bchip(text, color=BLUE, size=26, **kw):
    c = chip(text, color, size=size, **kw)
    back = RoundedRectangle(corner_radius=0.14, width=c[0].width, height=c[0].height, stroke_width=0,
                            fill_color=BG, fill_opacity=1).move_to(c[0])
    return VGroup(back, *c)


def smooth(t):
    t = min(1.0, max(0.0, t))
    return t * t * (3 - 2 * t)


class Plot:
    """a plot frame: origin lower left, u and v run 0..1 across the frame."""

    def __init__(self, x0, y0, w, h):
        self.x0, self.y0, self.w, self.h = x0, y0, w, h

    def P(self, u, v):
        return np.array([self.x0 + u * self.w, self.y0 + v * self.h, 0.0])

    def axes(self):
        return VGroup(Line(self.P(0, 0), self.P(1.0, 0), color=GREY, stroke_width=3),
                      Line(self.P(0, 0), self.P(0, 1.08), color=GREY, stroke_width=3))

    def curve(self, fn, u0, u1, color, w=6, n=70):
        pts = [self.P(u, fn(u)) for u in np.linspace(u0, u1, n)]
        return VMobject(stroke_color=color, stroke_width=w, fill_opacity=0).set_points_as_corners(pts)


# ---- the two schematic histories used in scenes 3 and 6 ----------------------------------------
def hyp_panel(cx, lost, labels=True):
    pl = Plot(cx - 2.8, -2.35, 5.6, 3.4)
    axes = pl.axes()
    xlab = T("time after the operation", 22, GREY).move_to([cx, -2.95, 0])
    ylab = T("healthy motor neurons", 22, GREY).move_to([pl.x0 + 1.55, pl.y0 + pl.h * 1.08 + 0.3, 0])
    ticks = VGroup(*[Line(pl.P(u, 0), pl.P(u, 0) + DOWN * 0.16, color=GREY, stroke_width=3)
                     for u in np.linspace(0.06, 0.94, 9)])
    if lost:
        f_op = lambda u: 0.85 - 0.5 * smooth((u - 0.4) / 0.28)
    else:
        f_op = lambda u: 0.4
    f_in = lambda u: 0.85
    blue = pl.curve(f_in, 0.02, 1.0, BLUE, 8)
    if lost:
        blue_a = pl.curve(f_in, 0.02, 0.4, BLUE, 8)
        blue_b = pl.curve(f_in, 0.4, 1.0, BLUE, 8)
        yel_a = pl.curve(f_op, 0.02, 0.4, YELLOW, 4)
        yel_b = pl.curve(f_op, 0.4, 1.0, YELLOW, 5)
    else:
        blue_a = blue_b = None
        yel_a = yel_b = pl.curve(f_op, 0.02, 1.0, YELLOW, 5)
    sch = T("schematic", 22, GREY).move_to(pl.P(1.0, 1.08) + [-0.65, 0.3, 0])
    dots = VGroup()
    if lost:
        rnd = random.Random(4)
        for i in range(9):
            u = 0.42 + 0.26 * (i / 8) + rnd.uniform(-0.01, 0.01)
            v = 0.1 + 0.22 * rnd.random()
            dots.add(Dot(pl.P(u, v), radius=0.09, color=RED))
    return dict(pl=pl, axes=axes, xlab=xlab, ylab=ylab, ticks=ticks, blue=blue, blue_a=blue_a, blue_b=blue_b,
                yel_a=yel_a, yel_b=yel_b, dots=dots, sch=sch)


def legend():
    c1 = bchip("operated side", YELLOW, 24)
    c2 = bchip("intact side", BLUE, 24)
    c3 = bchip("dying cells", RED, 24)
    VGroup(c1, c2, c3).arrange(RIGHT, buff=0.5).move_to([0, 3.15, 0])
    return c1, c2, c3


# ---------------------------------------------------------------------------------------------
class S00Title(TitleCard):
    LESSON = "Naturally occurring neuron death"
    TITLE = "Count the neurons across time"


# ---------------------------------------------------------------------------------------------
class S01Gone(SpokenScene):
    def construct(self):
        # lattice of neuron dots inside an ellipse
        rnd = random.Random(7)
        cx, cy, a, b = -2.7, -0.1, 2.9, 2.2
        pts = []
        sp = 0.66
        for r, yy in enumerate(np.arange(-b, b + 0.01, sp * 0.866)):
            for xx in np.arange(-a, a + 0.01, sp):
                xo = xx + (sp / 2 if r % 2 else 0)
                if (xo / (a - 0.2)) ** 2 + (yy / (b - 0.2)) ** 2 <= 1:
                    pts.append([cx + xo + rnd.uniform(-0.07, 0.07), cy + yy + rnd.uniform(-0.07, 0.07), 0])
        dots = VGroup(*[Dot(p, radius=0.17, color=BLUE) for p in pts])
        frame = Ellipse(width=2 * a + 0.4, height=2 * b + 0.4, color=GREY, stroke_width=3).move_to([cx, cy, 0])
        cap = T("raw counts for the leg", 26, BLUE).move_to([cx, cy - b - 0.62, 0])
        leg = Ellipse(width=2.4, height=3.4, stroke_color=YELLOW, stroke_width=4, fill_color=YELLOW,
                      fill_opacity=0.22).move_to([4.5, cy, 0])
        leg_l = T("leg", 30, YELLOW).move_to(leg)
        bundle = arr([cx + a + 0.3, cy, 0], [3.2, cy, 0], GREY, 6)
        count = T("20,000", 56, BLUE, weight=BOLD).move_to([cx, cy + b + 0.78, 0])

        self.at("chick embryo")
        self.play(Create(frame), FadeIn(leg), FadeIn(leg_l), run_time=0.8)
        self.at("motor neurons")
        self.play(LaggedStart(*[FadeIn(d, scale=0.4) for d in dots], lag_ratio=0.02), FadeIn(cap),
                  FadeIn(count), run_time=1.5)
        self.play(GrowArrow(bundle), run_time=0.5)
        self.at("By about day")
        idx = list(range(len(dots)))
        rnd.shuffle(idx)
        gone = [dots[i] for i in idx[:round(0.4 * len(dots))]]
        ghosts = VGroup(*[DashedVMobject(Circle(radius=0.17, color=GREY, stroke_width=2).move_to(d.get_center()),
                                         num_dashes=8) for d in gone])
        self.play(*[d.animate.set_color(RED) for d in gone], run_time=0.5)
        count2 = T("12,000", 56, BLUE, weight=BOLD).move_to(count)
        self.at("are left")
        self.play(*[FadeOut(d, scale=0.3) for d in gone], FadeIn(ghosts), ReplacementTransform(count, count2),
                  run_time=1.0)
        self.at("Nothing is wrong")
        ok = T("it has both legs\nand will hatch and walk", 24, GREY, line_spacing=0.9).move_to([4.5, cy - 2.4, 0])
        self.play(Indicate(leg, color=YELLOW, scale_factor=1.05), run_time=0.8)
        self.at("both legs")
        self.play(FadeIn(ok), run_time=0.5)
        q = T("?", 80, RED, weight=BOLD).move_to([cx + 2.55, cy + b + 0.78, 0])
        self.at("where did the neurons go")
        self.play(FadeIn(q, scale=0.5), run_time=0.7)
        self.finish()


# ---------------------------------------------------------------------------------------------
class S02Shelf(SpokenScene):
    def construct(self):
        head = T("Count only at the end", 36, font=TITLE_FONT).move_to([0, 3.0, 0])
        self.at("Suppose you count only")
        self.play(Write(head), run_time=1.0)
        yb = -2.3
        base = Line([3.3, yb, 0], [6.1, yb, 0], color=GREY, stroke_width=3)
        bar = Rectangle(width=1.5, height=2.0, stroke_color=BLUE, stroke_width=3, fill_color=BLUE,
                        fill_opacity=0.5).move_to([4.7, yb + 1.0, 0])
        blab = T("count at the end", 24, BLUE).move_to([4.7, yb - 0.45, 0])
        self.at("and the number is low")
        self.play(Create(base), FadeIn(bar, shift=UP * 0.3), FadeIn(blab), run_time=0.9)
        texts = [("divided too few times", GREY, "divided too few"),
                 ("sent too few to the place counted", GREY, "sent too few"),
                 ("too few became that cell type", GREY, "too few became"),
                 ("made, then lost", RED, "the cells were made")]
        ys = [1.7, 0.45, -0.8, -2.05]
        chips, arrows = [], []
        ends = [-0.55, -0.85, -1.15, -1.45]
        for i, ((txt, col, cue), y) in enumerate(zip(texts, ys)):
            c = bchip(txt, col, 28).move_to([0, y, 0])
            c.align_to([-0.4, 0, 0], RIGHT)
            a = arr(c.get_right(), [3.85, ends[i], 0], col, 4)
            chips.append(c); arrows.append(a)
        for i, (txt, col, cue) in enumerate(texts):
            self.at(cue)
            self.play(FadeIn(chips[i], shift=RIGHT * 0.3), run_time=0.5)
            self.play(GrowArrow(arrows[i]), Indicate(bar, color=BLUE, scale_factor=1.06), run_time=0.7)
        same = T("the same low number", 28, TEXT).move_to([4.7, 0.9, 0])
        self.at("looks the same")
        self.play(*[Indicate(a, color=TEXT, scale_factor=1.0) for a in arrows], FadeIn(same, shift=DOWN * 0.2),
                  run_time=1.0)
        self.finish()


# ---------------------------------------------------------------------------------------------
class S03Series(SpokenScene):
    def construct(self):
        L = hyp_panel(-3.4, False)
        R = hyp_panel(3.4, True)
        c_op, c_in, c_dy = legend()

        self.at("count at many times")
        self.play(Create(L["axes"]), Create(R["axes"]), FadeIn(L["xlab"]), FadeIn(R["xlab"]),
                  FadeIn(L["sch"]), FadeIn(R["sch"]), run_time=1.0)
        wb = bchip("wing bud removed on one side", YELLOW, 26).move_to([0, 3.15, 0])
        self.at("Remove a wing bud")
        self.play(FadeIn(wb, shift=DOWN * 0.15), run_time=0.5)
        self.at("closely spaced stages")
        self.play(LaggedStart(*[GrowFromCenter(t) for t in list(L["ticks"]) + list(R["ticks"])],
                              lag_ratio=0.04), run_time=1.3)
        self.at("operated side with")
        self.play(FadeOut(wb), FadeIn(c_op, shift=DOWN * 0.15), run_time=0.4)
        self.at("the intact side")
        self.play(FadeIn(c_in, shift=DOWN * 0.15), run_time=0.4)
        self.at("Count the healthy")
        self.play(FadeIn(L["ylab"]), FadeIn(R["ylab"]), run_time=0.5)
        self.at("and count the dying")
        self.play(FadeIn(c_dy, shift=DOWN * 0.15), run_time=0.5)
        self.at("dark condensed nuclei")
        self.play(Indicate(c_dy, color=RED, scale_factor=1.12), run_time=0.7)

        tl = T("never made", 32, TEXT, weight=BOLD).move_to([-3.4, 2.15, 0])
        self.at("were never made")
        self.play(FadeIn(tl, shift=DOWN * 0.1), run_time=0.5)
        self.at("is low from the first")
        self.play(Create(L["blue"]), Create(L["yel_a"]), run_time=1.0)
        none = T("no burst of dying cells", 24, RED).move_to(L["pl"].P(0.5, 0.2))
        self.at("with no burst")
        self.play(FadeIn(none), run_time=0.5)

        tr = T("made, then lost", 32, TEXT, weight=BOLD).move_to([3.4, 2.15, 0])
        self.at("made and then lost")
        self.play(FadeIn(tr, shift=DOWN * 0.1), run_time=0.5)
        self.at("start equal")
        self.play(Create(R["blue_a"]), Create(R["yel_a"]), run_time=0.9)
        self.at("Then dying cells appear")
        self.play(LaggedStart(*[FadeIn(d, scale=2) for d in R["dots"]], lag_ratio=0.1), run_time=1.0)
        self.at("falls behind")
        self.play(Create(R["blue_b"]), Create(R["yel_b"]), run_time=1.2)
        self.finish()


# ---------------------------------------------------------------------------------------------
class S04Curve(SpokenScene):
    def construct(self):
        d2u = lambda d: (d - 5.0) / 6.0
        pl = Plot(-4.6, -2.55, 10.0, 4.5)
        top = 22000.0
        n2v = lambda n: n / top

        def fn(u):
            d = u * 6.0 + 5.0
            if d <= 6.5:
                return n2v(20000)
            return n2v(20000 - 8000 * smooth((d - 6.5) / 3.0))

        head = T("Chick motor neurons for the leg, counted in normal embryos", 30, font=TITLE_FONT).move_to([0, 3.25, 0])
        axes = pl.axes()
        ylabs = VGroup(*[T(s, 22, GREY).move_to(pl.P(0, n2v(n)) + LEFT * 0.7) for s, n in
                         (("0", 0), ("12,000", 12000), ("20,000", 20000))])
        xt = VGroup(*[VGroup(Line(pl.P(d2u(d), 0), pl.P(d2u(d), 0) + DOWN * 0.15, color=GREY, stroke_width=3),
                             T(str(d), 22, GREY).move_to(pl.P(d2u(d), 0) + DOWN * 0.45)) for d in (6, 8, 10)])
        xl = T("days of incubation", 22, GREY).move_to(pl.P(0.5, 0) + DOWN * 0.95)
        h20 = DashedLine(pl.P(0, n2v(20000)), pl.P(1.0, n2v(20000)), color=GREY, stroke_width=2)
        h12 = DashedLine(pl.P(0, n2v(12000)), pl.P(1.0, n2v(12000)), color=GREY, stroke_width=2)
        peak = Rectangle(width=pl.w / 6.0, height=pl.h * 1.0, stroke_width=0, fill_color=BLUE, fill_opacity=0.14).move_to(
            (pl.P(d2u(5.5), 0) + pl.P(d2u(6.5), 1.0)) / 2)
        peak_l = T("peak", 24, BLUE).move_to(pl.P(d2u(6.0), 1.0) + UP * 0.3)
        loss = Rectangle(width=pl.w / 2.0, height=pl.h * 1.0, stroke_width=0, fill_color=RED, fill_opacity=0.14).move_to(
            (pl.P(d2u(6.5), 0) + pl.P(d2u(9.5), 1.0)) / 2)
        loss_l = T("most of the loss", 24, RED).move_to(pl.P(d2u(8.0), 1.0) + UP * 0.3)
        c1 = pl.curve(fn, d2u(5.5), d2u(6.5), BLUE, 8, 20)
        c2 = pl.curve(fn, d2u(6.5), 1.0, BLUE, 8, 80)
        br_x = pl.P(0.97, 0)[0]
        y20, y12 = pl.P(0, n2v(20000))[1], pl.P(0, n2v(12000))[1]
        br = VGroup(Line([br_x, y20, 0], [br_x, y12, 0], color=RED, stroke_width=6),
                    Line([br_x - 0.15, y20, 0], [br_x + 0.15, y20, 0], color=RED, stroke_width=6),
                    Line([br_x - 0.15, y12, 0], [br_x + 0.15, y12, 0], color=RED, stroke_width=6))
        br_l = T("about 40% lost", 28, RED, weight=BOLD).move_to([br_x - 1.6, (y20 + y12) / 2 + 0.3, 0])
        note = T("uncorrected counts", 22, GREY).move_to([br_x - 1.6, (y20 + y12) / 2 - 0.2, 0])

        sub = T("curve drawn between the reported counts", 22, GREY).move_to([0, 2.7, 0])
        self.at("counted the death")
        self.play(FadeIn(sub), FadeIn(head), Create(axes), FadeIn(ylabs), FadeIn(xt), FadeIn(xl), run_time=1.3)
        self.at("peaked at just")
        self.play(FadeIn(peak), FadeIn(peak_l), FadeIn(h20), Create(c1), run_time=1.0)
        self.at("settled near")
        self.play(FadeIn(h12), Create(c2), run_time=1.6)
        self.at("a loss of about")
        self.play(Create(br), FadeIn(br_l), FadeIn(note), run_time=0.9)
        self.at("Most of it came")
        self.play(FadeIn(loss), FadeIn(loss_l), run_time=0.9)
        self.finish()


# ---------------------------------------------------------------------------------------------
class S05Graft(SpokenScene):
    def construct(self):
        # cord and legs
        cord = RoundedRectangle(corner_radius=0.2, width=0.45, height=3.4, stroke_color=BLUE, stroke_width=3,
                                fill_color=BLUE, fill_opacity=0.3).move_to([-5.8, 0.15, 0])
        cord_l = T("cord", 24, BLUE).move_to([-5.8, -1.85, 0])
        leg = Ellipse(width=1.8, height=1.1, stroke_color=YELLOW, stroke_width=4, fill_color=YELLOW,
                      fill_opacity=0.22).move_to([-4.25, 1.2, 0])
        leg_l = T("leg", 26, YELLOW).move_to(leg)
        x_leg = DashedVMobject(Ellipse(width=1.8, height=1.1, stroke_color=YELLOW, stroke_width=4).move_to([-4.25, -0.9, 0]),
                               num_dashes=24)
        x_leg_f = Ellipse(width=1.8, height=1.1, stroke_width=0, fill_color=YELLOW, fill_opacity=0.1).move_to([-4.25, -0.9, 0])
        x_leg_l = T("extra leg", 24, YELLOW).move_to([-4.25, -1.75, 0])
        ax1 = Line([-5.55, 0.9, 0], [-5.15, 1.2, 0], color=GREY, stroke_width=4)
        ax2 = Line([-5.55, -0.4, 0], [-5.15, -0.9, 0], color=GREY, stroke_width=4)

        d2u = lambda d: (d - 5.0) / 6.0
        pl = Plot(-2.3, -2.4, 8.0, 4.0)
        f_c = lambda u: 0.78 if u * 6 + 5 <= 6.5 else 0.78 - 0.31 * smooth((u * 6 + 5 - 6.5) / 3.0)
        f_g = lambda u: 0.78 if u * 6 + 5 <= 6.5 else 0.78 - 0.31 * smooth((u * 6 + 5 - 6.5) / 3.0) + 0.12 * smooth((u * 6 + 5 - 6.5) / 3.0)
        axes = pl.axes()
        yl = T("motor neurons", 22, GREY).move_to(pl.P(0, 1.08) + [1.0, 0.3, 0])
        xl = T("days of incubation", 22, GREY).move_to(pl.P(0.5, 0) + DOWN * 0.6)
        ctrl = pl.curve(f_c, d2u(5.5), 1.0, BLUE, 8, 80)
        ctrl_a = pl.curve(f_c, d2u(5.5), d2u(6.8), BLUE, 8, 30)
        ctrl_b = pl.curve(f_c, d2u(6.8), 1.0, BLUE, 8, 60)
        gr_b = pl.curve(f_g, d2u(6.8), 1.0, YELLOW, 6, 60)
        c_c = bchip("control side", BLUE, 24).move_to(pl.P(0.55, 0.2))
        c_g = bchip("grafted side", YELLOW, 24).move_to(pl.P(0.62, 1.0) + UP * 0.35)
        d6x = pl.P(d2u(6.0), 0)[0]
        d6 = DashedLine(pl.P(d2u(6.0), 0), pl.P(d2u(6.0), 1.0), color=GREY, stroke_width=2)
        d6l = T("day 6", 24, GREY).move_to(pl.P(d2u(6.0), 0) + DOWN * 0.25)
        dotc = Dot(pl.P(d2u(6.0), f_c(d2u(6.0))), radius=0.16, color=BLUE)
        ring = Circle(radius=0.26, color=YELLOW, stroke_width=4).move_to(dotc)
        eq = T("equal", 26, TEXT).move_to(pl.P(d2u(6.0), 0.96) + UP * 0.0)
        p_end = pl.P(1.0, f_c(1.0)); g_end = pl.P(1.0, f_g(1.0))
        gap = VGroup(Line(p_end + RIGHT * 0.25, g_end + RIGHT * 0.25, color=TEXT, stroke_width=5),
                     Line(p_end + RIGHT * 0.15, p_end + RIGHT * 0.35, color=TEXT, stroke_width=5),
                     Line(g_end + RIGHT * 0.15, g_end + RIGHT * 0.35, color=TEXT, stroke_width=5))
        gap_l = T("11% to 28% more", 24, YELLOW).next_to(g_end, DOWN, buff=0.0).shift(LEFT * 1.35 + UP * 0.6)
        gap_l.move_to(pl.P(0.8, 0.8))

        self.at("tested the logic")
        self.play(Create(cord), FadeIn(cord_l), FadeIn(leg), FadeIn(leg_l), Create(ax1), run_time=0.9)
        self.at("grafted an extra leg")
        self.play(Create(x_leg), FadeIn(x_leg_f), FadeIn(x_leg_l), Create(ax2), run_time=1.0)
        sch5 = T("schematic", 22, GREY).move_to(pl.P(1.0, 1.08) + [-0.65, 0.3, 0])
        self.play(Create(axes), FadeIn(yl), FadeIn(xl), FadeIn(sch5), run_time=0.8)
        self.at("At day six")
        self.play(Create(d6), FadeIn(d6l), Create(ctrl_a), FadeIn(c_c), run_time=1.0)
        self.at("no more motor neurons")
        self.play(FadeIn(dotc), Create(ring), FadeIn(eq), run_time=0.7)
        self.at("Later")
        self.play(FadeOut(eq), FadeOut(ring), FadeOut(dotc), Create(ctrl_b), run_time=1.2)
        gr_a = pl.curve(f_g, d2u(5.5), d2u(6.8), YELLOW, 4, 30)
        self.at("whose grafts moved")
        self.play(Create(gr_b), FadeIn(c_g), run_time=1.3)
        self.at("it had more")
        self.play(Create(gap), Indicate(c_g, color=YELLOW, scale_factor=1.05), run_time=0.8)
        self.at("About")
        self.play(FadeIn(gap_l), run_time=0.6)
        self.finish()


# ---------------------------------------------------------------------------------------------
class S06Rule(SpokenScene):
    def construct(self):
        yb, H, W = -2.6, 4.0, 1.7
        xs = [-2.6, 0.8]
        keep = [0.6, 0.6]

        def bar(x, kf):
            kept = Rectangle(width=W, height=H * kf, stroke_color=BLUE, stroke_width=3, fill_color=BLUE,
                             fill_opacity=0.5).move_to([x, yb + H * kf / 2, 0])
            lost = Rectangle(width=W, height=H * (1 - kf), stroke_color=RED, stroke_width=3, fill_color=RED,
                             fill_opacity=0.5).move_to([x, yb + H * kf + H * (1 - kf) / 2, 0])
            return kept, lost

        k1, l1 = bar(xs[0], 0.6)
        k2, l2 = bar(xs[1], 0.6)
        made = DashedLine([-4.2, yb + H, 0], [2.3, yb + H, 0], color=GREY, stroke_width=3)
        made_l = T("same number made", 26, GREY).move_to([-0.9, yb + H + 0.42, 0])
        n1 = T("normal", 26, TEXT).move_to([xs[0], yb - 0.4, 0])
        n2 = T("extra leg", 26, YELLOW).move_to([xs[1], yb - 0.4, 0])
        base = Line([-4.2, yb, 0], [2.3, yb, 0], color=GREY, stroke_width=3)
        lab_l = T("lost", 26, RED).move_to([-3.6, yb + H * 0.8, 0]).shift(LEFT * 0.05)
        lab_k = T("kept", 26, BLUE).move_to([-3.6, yb + H * 0.3, 0]).shift(LEFT * 0.05)
        lab_l.move_to([-4.9, yb + H * 0.8, 0]); lab_k.move_to([-4.9, yb + H * 0.3, 0])

        self.at("More target did not")
        self.play(Create(base), FadeIn(k1), FadeIn(l1), FadeIn(k2), FadeIn(l2), FadeIn(n1), FadeIn(n2),
                  FadeIn(lab_l), FadeIn(lab_k), run_time=1.0)
        self.at("more births")
        self.play(Create(made), FadeIn(made_l), run_time=0.8)
        k2n, l2n = bar(xs[1], 0.78)
        self.at("It meant fewer deaths")
        self.play(Transform(k2, k2n), Transform(l2, l2n), run_time=1.2)
        chip_t = bchip("something limited", YELLOW, 28).move_to([4.4, -0.6, 0])
        ar = arr(chip_t.get_left(), [1.8, -0.6, 0], YELLOW, 5)
        self.at("supplies something limited")
        self.play(FadeIn(chip_t, shift=LEFT * 0.3), GrowArrow(ar), run_time=0.8)
        self.at("need to survive")
        self.play(Indicate(k2, color=BLUE, scale_factor=1.04), run_time=0.8)

        covers = VGroup()
        for lost, x in ((l1, xs[0]), (l2, xs[1])):
            r = Rectangle(width=W + 0.04, height=lost.height + 0.04, stroke_width=0, fill_color=GREY,
                          fill_opacity=1).move_to(lost)
            q = T("?", 44, BG, weight=BOLD).move_to(r)
            covers.add(VGroup(r, q))
        self.at("hides its own history")
        self.play(FadeIn(covers), FadeOut(VGroup(chip_t, ar)), run_time=0.8)

        L = hyp_panel(-3.4, False)
        R = hyp_panel(3.4, True)
        c_op, c_in, c_dy = legend()
        tl = T("never made", 32, TEXT, weight=BOLD).move_to([-3.4, 2.15, 0])
        tr = T("made, then lost", 32, TEXT, weight=BOLD).move_to([3.4, 2.15, 0])
        self.at("Count across time")
        old = VGroup(base, k1, l1, k2, l2, made, made_l, n1, n2, lab_l, lab_k, covers)
        self.play(FadeOut(old),
                  FadeIn(L["axes"]), FadeIn(R["axes"]), FadeIn(L["xlab"]), FadeIn(R["xlab"]),
                  FadeIn(L["ylab"]), FadeIn(R["ylab"]), FadeIn(L["ticks"]), FadeIn(R["ticks"]),
                  FadeIn(c_op), FadeIn(c_in), FadeIn(c_dy), FadeIn(L["sch"]), FadeIn(R["sch"]), run_time=1.0)
        self.at("never made from")
        self.play(FadeIn(tl), Create(L["blue"]), Create(L["yel_a"]), run_time=1.0)
        self.at("made and lost")
        self.play(FadeIn(tr), Create(R["blue_a"]), Create(R["yel_a"]), run_time=0.6)
        self.play(FadeIn(R["dots"]), Create(R["blue_b"]), Create(R["yel_b"]), run_time=1.0)
        self.finish()


# ---------------------------------------------------------------------------------------------
class S07End(EndCard):
    LINE = "Count across time to tell never made from lost."
