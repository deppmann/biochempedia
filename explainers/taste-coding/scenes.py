"""Taste coding: a synapse made of a channel  (Biochemistrypedia explainer)

COLOR MAP (one color per concept, whole video)
  BLUE   = taste receptors on the type II cell (sweet, bitter, umami)
  YELLOW = ATP
  TEAL   = CALHM1 channel (and its activation curve)
  PURPLE = CALHM3 (and the CALHM1 + CALHM3 activation curve)
  GREEN  = the nerve fibre and its ATP receptor
  RED    = absent / deleted / not supported (crossed vesicles, knockout results)
  GREY   = cell outlines, membranes, axes, de-emphasised labels
"""
import numpy as np
from bp_style import *  # noqa: F401,F403

PURPLE = "#B58CD9"


def cross(c, s=0.2, color=RED, w=5):
    return VGroup(Line(c + np.array([-s, -s, 0]), c + np.array([s, s, 0]), color=color, stroke_width=w),
                  Line(c + np.array([-s, s, 0]), c + np.array([s, -s, 0]), color=color, stroke_width=w))


def atp(size=22):
    c = chip("ATP", YELLOW, size=size, pad=0.1, fill_opacity=0.3)
    back = RoundedRectangle(corner_radius=0.14, width=c[0].width, height=c[0].height, stroke_width=0,
                            fill_color=BG, fill_opacity=1).move_to(c[0])
    return VGroup(back, *c)


class Stage:
    """Type II cell on the left, nerve fibre on the right, gap between. Built fresh in each scene."""

    def __init__(self, yc=-0.2, H=5.4, labels=True):
        self.yc, self.H = yc, H
        self.cell = Ellipse(width=4.2, height=H, stroke_color=GREY, stroke_width=4,
                            fill_color=GREY, fill_opacity=0.10).move_to([-3.9, yc, 0])
        self.fibre = RoundedRectangle(corner_radius=0.5, width=1.8, height=H + 0.4, stroke_color=GREEN, stroke_width=4,
                                      fill_color=GREEN, fill_opacity=0.10).move_to([4.9, yc, 0])
        self.cell_lbl = T("type II taste cell", 26, GREY).move_to([-3.9, yc + H / 2 + 0.38, 0])
        self.fib_lbl = T("nerve fibre", 26, GREEN).move_to([4.9, yc + (H + 0.4) / 2 + 0.38, 0])
        self.rec = VGroup(*[chip(n, BLUE, size=24, pad=0.14).move_to([-4.85, yc + dy, 0])
                            for n, dy in (("sweet", 0.85), ("bitter", 0), ("umami", -0.85))])
        self.patch = RoundedRectangle(corner_radius=0.1, width=0.36, height=1.6, stroke_color=GREY, stroke_width=3,
                                      fill_color=GREY, fill_opacity=0.35).move_to([-1.8, yc, 0])
        self.chan = RoundedRectangle(corner_radius=0.12, width=0.5, height=1.1, stroke_color=TEAL, stroke_width=4,
                                     fill_color=TEAL, fill_opacity=0.45).move_to([-1.8, yc, 0])
        self.chan_lbl = T("channel", 24, TEAL).move_to([-0.55, yc + 1.15, 0])
        self.fnotch = RoundedRectangle(corner_radius=0.1, width=0.4, height=1.2, stroke_color=GREEN, stroke_width=4,
                                       fill_color=GREEN, fill_opacity=0.5).move_to([4.0, yc, 0])
        self.fnotch_lbl = T("ATP receptor", 24, GREEN).move_to([2.9, yc + 1.15, 0])
        self.atps_in = VGroup(*[atp().move_to([-2.95, yc + dy, 0]) for dy in (0.7, 0, -0.7)])
        self.atps_out = [[3.15, yc + dy, 0] for dy in (0.5, 0, -0.5)]

    def base(self):
        return [self.cell, self.fibre, self.cell_lbl, self.fib_lbl]

    def release(self, scene, t=2.0, pause=0.3):
        """ATP chips leave through the channel and settle at the fibre's receptor."""
        anims = []
        for i, a in enumerate(self.atps_in):
            path = VMobject().set_points_as_corners([a.get_center(), [-1.8, self.yc + (1 - i) * 0.0, 0],
                                                     self.atps_out[i]])
            anims.append(MoveAlongPath(a, path, run_time=t, rate_func=smooth))
        scene.play(LaggedStart(*anims, lag_ratio=0.25), run_time=t + 0.5)


class S00Title(TitleCard):
    LESSON = "Taste from tongue to cortex"
    TITLE = "A synapse made of a channel"


# ---------------------------------------------------------------------------------------------
class S01Gap(SpokenScene):
    def construct(self):
        st = Stage()
        mouse = T("in mouse", 26, GREY).move_to([0, -3.35, 0])
        self.at("taste cell")
        self.play(FadeIn(st.cell), FadeIn(st.cell_lbl), FadeIn(st.fibre), FadeIn(st.fib_lbl), run_time=1.0)
        self.play(LaggedStart(*[FadeIn(r, shift=RIGHT * 0.15) for r in st.rec], lag_ratio=0.25), FadeIn(mouse), run_time=1.2)
        # vesicles, crossed out
        ves = VGroup(*[Circle(radius=0.17, stroke_color=GREY, stroke_width=3, fill_color=GREY, fill_opacity=0.2)
                       .move_to([-2.7, st.yc + dy, 0]) for dy in (0.6, 0, -0.6)])
        self.at("no conventional")
        crosses = VGroup(*[cross(v.get_center(), 0.26) for v in ves])
        vlbl = T("no vesicular synapse", 26, RED).move_to([0.9, st.yc + 1.9, 0])
        self.play(FadeIn(ves), run_time=0.5)
        self.play(Create(crosses), FadeIn(vlbl), run_time=0.8)
        self.at("how does")
        q = chip("?", YELLOW, size=64, pad=0.35).move_to([1.0, st.yc, 0])
        d1 = DashedLine([-1.5, st.yc, 0], [q.get_left()[0] - 0.1, st.yc, 0], color=GREY, stroke_width=4)
        d2 = DashedLine([q.get_right()[0] + 0.1, st.yc, 0], [3.8, st.yc, 0], color=GREY, stroke_width=4)
        self.play(Create(d1), Create(d2), GrowFromCenter(q), run_time=1.0)
        self.at("mouse result")
        self.play(Indicate(mouse, color=YELLOW, scale_factor=1.15), run_time=1.0)
        self.finish()


class S02Atp(SpokenScene):
    def construct(self):
        st = Stage()
        mouse = T("in mouse", 26, GREY).move_to([0, -3.35, 0])
        self.add(*st.base(), mouse)
        self.add(st.rec)
        self.at("receptors for sweet")
        self.play(*[Indicate(r, color=BLUE, scale_factor=1.12) for r in st.rec], run_time=1.2)
        self.play(FadeIn(st.atps_in), run_time=0.6)
        self.at("it releases")
        self.play(FadeIn(st.patch), FadeIn(st.chan), FadeIn(st.chan_lbl), run_time=0.8)
        st.release(self, t=2.0)
        self.at("beside it carries")
        self.play(FadeIn(st.fnotch), FadeIn(st.fnotch_lbl), run_time=0.8)
        self.finish()


class S03Calhm1(SpokenScene):
    def construct(self):
        st = Stage()
        mouse = T("in mouse", 26, GREY).move_to([0, -3.35, 0])
        self.add(*st.base(), mouse, st.rec, st.patch, st.chan, st.chan_lbl, st.fnotch, st.fnotch_lbl)
        # normal case: ATP already released and resting at the receptor
        for a, p in zip(st.atps_in, st.atps_out):
            a.move_to(p)
        self.add(st.atps_in)
        new_lbl = chip("CALHM1", TEAL, size=26, pad=0.12).move_to([-0.55, st.yc + 1.15, 0])
        self.at("is required")
        self.play(FadeOut(st.chan_lbl), FadeIn(new_lbl), run_time=0.8)
        case = T("wild-type mouse", 26, GREY).move_to([0.9, st.yc - 1.9, 0])
        self.play(FadeIn(case), run_time=0.6)
        self.at("knockout mice")
        ko = T("Calhm1 knockout", 26, RED).move_to([0.9, st.yc - 1.9, 0])
        # one animation: clear the previous answer and switch to the knockout case
        fresh = VGroup(*[atp().move_to([-2.95, st.yc + dy, 0]) for dy in (0.7, 0, -0.7)])
        self.play(FadeOut(st.atps_in), FadeOut(st.chan), FadeOut(new_lbl), FadeOut(case), run_time=0.5)
        self.play(FadeIn(ko), FadeIn(fresh), run_time=0.6)
        self.at("Without that channel")
        x = cross([-1.8, st.yc, 0], 0.5, RED, 7)
        res = T("no ATP release", 26, RED).move_to([0.7, st.yc + 0.0, 0])
        self.play(Create(x), FadeIn(res), run_time=0.9)
        self.at("Sour and salty")
        ss = T("sour, salty: mostly normal", 24, GREY).move_to([0.9, -2.75, 0])
        self.play(FadeIn(ss), run_time=0.7)
        self.at("does not mean")
        ss2 = T("sodium: CALHM use not excluded", 24, YELLOW).move_to([0.9, -2.75, 0])
        self.play(FadeOut(ss), FadeIn(ss2), run_time=0.8)
        self.finish()


def make_axes():
    ax = Axes(x_range=[0, 1500, 500], y_range=[0, 1.35, 1], x_length=6.4, y_length=4.6,
              axis_config={"color": GREY, "stroke_width": 3, "include_tip": False, "include_ticks": True,
                           "tick_size": 0.08}, y_axis_config={"include_ticks": False})
    ax.move_to([2.7, -0.3, 0])
    ticks = VGroup()
    for v in (0, 500, 1000, 1500):
        ticks.add(M(str(v), 22, GREY).next_to(ax.c2p(v, 0), DOWN, buff=0.15))
    xl = T("time after activation (ms)", 24, GREY).next_to(ax, DOWN, buff=0.62)
    yl = T("relative activation", 24, GREY).rotate(PI / 2).next_to(ax, LEFT, buff=0.25)
    skt = T("in this sketch", 26, YELLOW).move_to([2.7, 2.7, 0])
    return ax, VGroup(ticks, xl, yl), skt


def curve(ax, tau, color, T_end=1500):
    return ax.plot(lambda t: 1 - np.exp(-t / tau), x_range=[0, T_end, 2.0], color=color, stroke_width=6, use_smoothing=False)


def membrane_panel(with3=False, x=-4.3, y=0.0):
    bar = RoundedRectangle(corner_radius=0.1, width=3.4, height=0.3, stroke_color=GREY, stroke_width=3,
                           fill_color=GREY, fill_opacity=0.35).move_to([x, y, 0])
    c1 = chip("CALHM1", TEAL, size=22, pad=0.12, fill_opacity=0.3)
    c1.move_to([x - (0.85 if with3 else 0.0), y + 0.65, 0])
    return bar, c1


class S04Slow(SpokenScene):
    def construct(self):
        ax, lbls, skt = make_axes()
        bar, c1 = membrane_panel()
        who = T("mouse N2a cells", 26, GREY).move_to([-4.3, 2.3, 0])
        who2 = T("whole-cell voltage clamp", 24, GREY).move_to([-4.3, 1.75, 0])
        self.at("puzzle remained")
        self.play(FadeIn(bar), FadeIn(c1, shift=DOWN * 0.2), run_time=0.9)
        self.at("alone is slow")
        self.play(Create(ax), FadeIn(lbls), FadeIn(skt), run_time=1.2)
        cv = curve(ax, 500, TEAL)
        self.at("recorded by")
        self.play(FadeIn(who), FadeIn(who2), run_time=0.7)
        self.at("it activated")
        self.play(Create(cv), run_time=3.5, rate_func=linear)
        dot = Dot(ax.c2p(500, 1 - np.exp(-1)), color=YELLOW, radius=0.11)
        vl = DashedLine(ax.c2p(500, 0), ax.c2p(500, 1 - np.exp(-1)), color=YELLOW, stroke_width=3)
        tl = VGroup(T("time constant", 24, YELLOW), T("above 500 ms", 24, YELLOW),
                    T("(drawn at 500 ms)", 22, GREY)).arrange(DOWN, aligned_edge=LEFT, buff=0.1)
        tl.move_to([ax.c2p(560, 0)[0] + tl.width / 2, ax.c2p(0, 0.28)[1], 0])
        note = VGroup()
        self.play(Create(vl), FadeIn(dot), FadeIn(tl), FadeIn(note), run_time=0.8)
        self.at("holds the membrane")
        self.play(Indicate(who2, color=YELLOW, scale_factor=1.05), run_time=0.9)
        self.finish()


class S05Calhm3(SpokenScene):
    def construct(self):
        ax, lbls, skt = make_axes()
        bar, c1 = membrane_panel()
        cv1 = curve(ax, 500, TEAL).set_stroke(opacity=0.5)
        vl = DashedLine(ax.c2p(500, 0), ax.c2p(500, 1 - np.exp(-1)), color=GREY, stroke_width=3)
        dot = Dot(ax.c2p(500, 1 - np.exp(-1)), color=GREY, radius=0.1)
        tl = VGroup(T("above 500 ms", 24, TEAL), T("(drawn at 500 ms)", 22, GREY)).arrange(DOWN, aligned_edge=LEFT, buff=0.08)
        tl.move_to([ax.c2p(560, 0)[0] + tl.width / 2 + 0.1, ax.c2p(0, 0.28)[1], 0])
        graph = VGroup(ax, lbls, skt, cv1, vl, dot, tl)
        # left panel starts as the taste-bud deletion case
        case = VGroup(T("Calhm3 deleted,", 26, RED), T("mouse taste buds", 26, RED)).arrange(DOWN, buff=0.1).move_to([-4.3, 2.2, 0])
        res = VGroup(T("ATP release:", 26, RED), T("abolished", 26, RED)).arrange(DOWN, buff=0.1).move_to([-4.3, 0.7, 0])
        self.at("colleagues deleted")
        self.play(FadeIn(case), run_time=0.7)
        self.at("was abolished")
        self.play(FadeIn(res), run_time=0.7)
        # new case: clear the old result in the same animation
        self.at("cultured cells")
        who = T("mouse N2a cells", 26, GREY).move_to([-4.3, 2.3, 0])
        c1b = chip("CALHM1", TEAL, size=22, pad=0.12, fill_opacity=0.3).move_to([-4.3 - 0.85, 0.65, 0])
        c3 = chip("CALHM3", PURPLE, size=22, pad=0.12, fill_opacity=0.3).move_to([-4.3 + 0.85, 0.65, 0])
        self.play(FadeOut(case), FadeOut(res), FadeIn(graph), FadeIn(who), FadeIn(bar), FadeIn(c1b), FadeIn(c3, shift=DOWN * 0.2),
                  run_time=1.0)
        self.at("activated in about")
        cv3 = curve(ax, 10, PURPLE)
        self.play(Create(cv3), run_time=1.2)
        t10 = VGroup(T("time constant about 10 ms", 24, PURPLE), T("(drawn at 10 ms)", 22, GREY)).arrange(DOWN, aligned_edge=LEFT, buff=0.06)
        t10.move_to([ax.c2p(80, 0)[0] + t10.width / 2, ax.c2p(0, 1.2)[1], 0])
        self.play(FadeIn(t10), run_time=0.6)
        self.at("speed-up of")
        ratio = VGroup(T("500 / 10:", 28, YELLOW), T("more than fifty-fold", 28, YELLOW)).arrange(DOWN, buff=0.1).move_to([-4.3, -1.3, 0])
        self.play(FadeIn(ratio, shift=UP * 0.1), run_time=0.8)
        self.at("rapid gating")
        self.play(Indicate(c3, color=PURPLE, scale_factor=1.12), run_time=0.9)
        self.finish()


class S06Rule(SpokenScene):
    def construct(self):
        st = Stage(yc=-0.2, H=4.0)
        # raise the stage a little less than default so the rule fits below
        lim1 = chip("times depend on voltage and protocol", GREY, size=24, pad=0.15).move_to([-3.3, 3.0, 0])
        lim2 = chip("cultured cells, not a living animal", YELLOW, size=24, pad=0.15).move_to([3.3, 3.0, 0])
        mouse = T("in mouse type II taste cells: ATP leaves through CALHM channels", 24, GREY).move_to([0, -3.1, 0])
        self.at("limits in mind")
        self.play(FadeIn(lim1, shift=DOWN * 0.1), run_time=0.7)
        self.at("cultured cells")
        self.play(FadeIn(lim2, shift=DOWN * 0.1), run_time=0.7)
        self.at("the rule to keep")
        self.play(FadeOut(lim1), FadeOut(lim2), run_time=0.5)
        self.play(FadeIn(VGroup(*st.base(), st.rec, st.patch, st.chan, st.fnotch, st.fnotch_lbl, st.atps_in, mouse)),
                  run_time=1.0)
        self.at("leaves through")
        st.release(self, t=1.8)
        c13 = VGroup(chip("CALHM1", TEAL, size=22, pad=0.1), chip("CALHM3", PURPLE, size=22, pad=0.1)
                     ).arrange(RIGHT, buff=0.2).move_to([-0.1, st.yc + 1.2, 0])
        self.play(FadeIn(c13), run_time=0.7)
        self.at("speeds the gating")
        self.play(Indicate(c13[1], color=PURPLE, scale_factor=1.15), run_time=1.0)
        self.finish()


class S07End(EndCard):
    LINE = "ATP leaves through CALHM channels; CALHM3 speeds the gating."
