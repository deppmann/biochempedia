"""What one daily survival number does  (Biochemistrypedia explainer, Ecology and Evolution)

COLOR MAP (one color per concept, whole video)
  PALE_C = the pale morph (typica): dots, bars, share segment
  DARK_C = the dark morph (carbonaria): dots, bars, share segment
  RED    = birds (the agent) and every "not this" reading
  YELLOW = the relative daily survival number and the arithmetic on it
  TEAL   = the dark share among survivors (the result)
  GREY   = frames, axes, labels, the wood
  GREEN  = the directly witnessed attacks (26%)
"""
import numpy as np
from bp_style import *  # noqa: F401,F403

PALE_C = "#E9DFC0"
DARK_C = "#B07A45"
R = 0.909


def moth(color, s=1.0):
    w1 = Ellipse(width=0.62, height=0.34, fill_color=color, fill_opacity=0.95, stroke_color=TEXT, stroke_width=1.5).shift(LEFT * 0.3 + UP * 0.05).rotate(0.25)
    w2 = Ellipse(width=0.62, height=0.34, fill_color=color, fill_opacity=0.95, stroke_color=TEXT, stroke_width=1.5).shift(RIGHT * 0.3 + UP * 0.05).rotate(-0.25)
    b = Ellipse(width=0.16, height=0.5, fill_color=color, fill_opacity=1, stroke_color=TEXT, stroke_width=1.5).shift(DOWN * 0.03)
    return VGroup(w1, w2, b).scale(s)


def cluster(color, cx, cy, s=1.1, dx=1.5, dy=1.5):
    ms = VGroup(*[moth(color, s).move_to([cx + (i - 1) * dx, cy + (0.5 - j) * dy, 0]) for j in range(2) for i in range(3)])
    return ms


def bar(x, h, color, base=-2.5, w=1.4):
    return Rectangle(width=w, height=max(h, 0.02), fill_color=color, fill_opacity=0.9, stroke_color=TEXT, stroke_width=2).move_to([x, base + max(h, 0.02) / 2, 0])


def cross(mob, color=RED):
    return Line(mob.get_left() + LEFT * 0.1, mob.get_right() + RIGHT * 0.1, color=color, stroke_width=4).move_to(mob.get_center())


def share(t):
    return R ** t / (1 + R ** t)


class S00Title(TitleCard):
    LESSON = "Natural selection in ecological context"
    TITLE = "What One Daily Survival Number Does"


# ---------------------------------------------------------------------------------------------
class S01Number(SpokenScene):
    def construct(self):
        pale = cluster(PALE_C, -3.8, 0.8)
        dark = cluster(DARK_C, 3.8, 0.8)
        pl = T("pale (typica)", 28, PALE_C).next_to(pale, DOWN, buff=0.3)
        dl = T("dark (carbonaria)", 28, DARK_C).next_to(dark, DOWN, buff=0.3)
        site = T("peppered moth, near Cambridge", 28, GREY).to_edge(UP, buff=0.5)
        self.at("Near Cambridge")
        self.play(FadeIn(site), LaggedStart(*[FadeIn(m, scale=0.6) for m in list(pale) + list(dark)], lag_ratio=0.04), run_time=0.8)
        bird = chip("birds", RED, 28).move_to([0, 2.5, 0])
        a_d = Arrow(bird.get_right() + DOWN * 0.1, dark.get_top() + UP * 0.05, color=RED, stroke_width=8, buff=0.1)
        a_p = Arrow(bird.get_left() + DOWN * 0.1, pale.get_top() + UP * 0.05, color=RED, stroke_width=2.5, buff=0.1)
        self.at("birds took dark")
        self.play(FadeIn(bird), GrowArrow(a_d), GrowArrow(a_p), run_time=0.8)
        self.at("The moth has a pale form")
        self.play(FadeIn(pl), FadeIn(dl), run_time=0.6)
        self.at("Michael")
        maj = T("Majerus: six years of releases", 26, GREY).move_to([0, -1.7, 0])
        self.play(FadeIn(maj), run_time=0.5)
        self.at("A dark moth survived each day")
        eq = chip("dark = 0.91 × pale, per day", YELLOW, 32).move_to([0, -2.9, 0])
        self.play(FadeOut(maj), FadeOut(bird), FadeOut(a_d), FadeOut(a_p), FadeIn(eq, shift=UP * 0.2), run_time=0.8)
        self.at("wood full of moths")
        wood = RoundedRectangle(corner_radius=0.3, width=12.4, height=4.5, stroke_color=GREY, stroke_width=3).move_to([0, 0.35, 0])
        wl = T("a wood", 26, GREY).next_to(wood, UP, buff=0.12).align_to(wood, LEFT)
        q = T("?", 110, YELLOW, weight=BOLD).move_to([0, 0.8, 0])
        self.play(Create(wood), FadeIn(wl), FadeIn(q, scale=0.5), run_time=0.9)
        self.finish()


# ---------------------------------------------------------------------------------------------
BASE = -2.5
H = 4.4          # bar height for 1,000
XP, XD = -4.6, -1.8


def stage(start_pale=1000, start_dark=1000):
    bp = bar(XP, H * start_pale / 1000, PALE_C, BASE)
    bd = bar(XD, H * start_dark / 1000, DARK_C, BASE)
    base = Line([-6.0, BASE, 0], [0.0, BASE, 0], color=GREY, stroke_width=3)
    lp = T("pale", 28, PALE_C).move_to([XP, BASE - 0.42, 0])
    ld = T("dark", 28, DARK_C).move_to([XD, BASE - 0.42, 0])
    return bp, bd, base, lp, ld


def count(x, h, txt, color):
    return M(txt, 30, color).move_to([x, BASE + h + 0.35, 0])


class S02Wood(SpokenScene):
    def construct(self):
        bp, bd, base, lp, ld = stage(0.001, 0.001)
        self.add(base, lp, ld)
        tag = chip("invented numbers", GREY, 26).move_to([3.3, 2.7, 0])
        self.at("invented numbers")
        self.play(FadeIn(tag), run_time=0.5)
        self.at("wood holds")
        fp = bar(XP, H, PALE_C, BASE)
        np_ = count(XP, H, "1,000", PALE_C)
        self.play(Transform(bp, fp), FadeIn(np_), run_time=0.9)
        self.at("pale moths and")
        fd = bar(XD, H, DARK_C, BASE)
        nd = count(XD, H, "1,000", DARK_C)
        self.play(Transform(bd, fd), FadeIn(nd), run_time=0.9)
        self.at("Say pale moths survive")
        ps = chip("pale: 0.80 survive per day", PALE_C, 28).move_to([3.3, 1.2, 0])
        self.play(FadeIn(ps, shift=LEFT * 0.2), run_time=0.7)
        items = []
        for i, (ph, txt) in enumerate([("no migration", "no migration"), ("no reproduction", "no reproduction"), ("no change in rates", "no change in rates")]):
            c = chip(txt, GREY, 26).move_to([3.3, -0.3 - i * 0.95, 0])
            self.at(ph)
            self.play(FadeIn(c, shift=LEFT * 0.2), run_time=0.5)
        self.finish()


class S03Day(SpokenScene):
    def construct(self):
        bp, bd, base, lp, ld = stage()
        np_ = count(XP, H, "1,000", PALE_C)
        nd = count(XD, H, "1,000", DARK_C)
        self.add(bp, bd, base, lp, ld, np_, nd)
        X0 = 3.4
        l1 = M("dark = 0.909 × pale", 32, YELLOW).move_to([X0, 2.4, 0])
        l2 = M("0.80 × 0.909", 36, YELLOW).move_to([X0, 1.3, 0])
        l3 = M("= 0.7272", 36, YELLOW).next_to(l2, DOWN, buff=0.25).align_to(l2, LEFT)
        self.at("Dark moths survive")
        self.play(FadeIn(l1, shift=LEFT * 0.2), run_time=0.6)
        self.at("So dark daily survival")
        self.play(FadeIn(l2, shift=LEFT * 0.2), run_time=0.6)
        self.at("That is")
        self.play(FadeIn(l3, shift=LEFT * 0.2), run_time=0.5)
        self.at("After one day")
        np2 = count(XP, H * 0.8, "800", PALE_C)
        nd2 = count(XD, H * 0.7272, "727.2", DARK_C)
        self.play(Transform(bp, bar(XP, H * 0.8, PALE_C, BASE)), Transform(bd, bar(XD, H * 0.7272, DARK_C, BASE)),
                  ReplacementTransform(np_, np2), ReplacementTransform(nd, nd2), run_time=1.6)
        self.at("That last figure")
        ex = chip("expected count", YELLOW, 28).move_to([X0, -0.9, 0])
        ar = Arrow(ex.get_left(), nd2.get_right() + RIGHT * 0.05, color=YELLOW, stroke_width=4, buff=0.12)
        self.play(FadeIn(ex), GrowArrow(ar), run_time=0.7)
        self.at("A fraction of a moth")
        ex2 = T("a fraction of a moth\nis an expectation, not a moth", 26, GREY).move_to([X0, -2.2, 0])
        self.play(FadeIn(ex2), run_time=0.7)
        self.finish()


class S04Share(SpokenScene):
    def construct(self):
        bp, bd, base, lp, ld = stage(800, 727.2)
        np2 = count(XP, H * 0.8, "800", PALE_C)
        nd2 = count(XD, H * 0.7272, "727.2", DARK_C)
        self.add(bp, bd, base, lp, ld, np2, nd2)
        CX, W, Y = 3.4, 5.6, 1.7
        def sbar(f):
            d = Rectangle(width=W * f, height=0.8, fill_color=DARK_C, fill_opacity=0.95, stroke_color=TEXT, stroke_width=2)
            p = Rectangle(width=W * (1 - f), height=0.8, fill_color=PALE_C, fill_opacity=0.95, stroke_color=TEXT, stroke_width=2)
            g = VGroup(d, p).arrange(RIGHT, buff=0)
            return g.move_to([CX, Y, 0])
        title = T("dark share of survivors", 28, TEAL).move_to([CX, Y + 0.95, 0])
        s0 = sbar(0.5)
        lab0 = M("50%", 30, TEAL).next_to(s0, DOWN, buff=0.2)
        self.at("Now ask for the dark share")
        self.play(FadeIn(title), FadeIn(s0), FadeIn(lab0), run_time=0.8)
        eq = M("727.2 / (800 + 727.2)", 26, YELLOW).move_to([CX, 0.0, 0])
        eq2 = M("= 0.476", 30, YELLOW).next_to(eq, DOWN, buff=0.2)
        self.at("among the survivors")
        self.play(FadeIn(eq, shift=LEFT * 0.2), run_time=0.7)
        self.at("is 0")
        self.play(FadeIn(eq2), run_time=0.5)
        s1 = sbar(0.476)
        lab1 = M("47.6%", 30, TEAL).next_to(s1, DOWN, buff=0.2)
        self.at("falls from")
        self.play(Transform(s0, s1), ReplacementTransform(lab0, lab1), run_time=1.2)
        self.at("cancel")
        c = M("0.909 / (1 + 0.909)", 26, YELLOW).move_to([CX, -1.9, 0])
        cl = T("0.80 and the 1,000s cancel", 24, GREY).move_to([CX, -2.8, 0])
        self.play(FadeIn(c, shift=LEFT * 0.2), FadeIn(cl), run_time=0.8)
        self.finish()


class S05Compound(SpokenScene):
    def construct(self):
        ax = Axes(x_range=[0, 5, 1], y_range=[30, 50, 5], x_length=8.2, y_length=4.4,
                  axis_config={"color": GREY, "stroke_width": 3, "include_ticks": True, "include_tip": False},
                  ).move_to([-1.9, -0.3, 0])
        xl = VGroup(*[T(str(i), 24, GREY).next_to(ax.c2p(i, 30), DOWN, buff=0.15) for i in range(6)])
        yl = VGroup(*[T(str(v), 24, GREY).next_to(ax.c2p(0, v), LEFT, buff=0.15) for v in (30, 35, 40, 45, 50)])
        xt = T("days", 26, GREY).next_to(xl, DOWN, buff=0.15)
        yt = T("dark share of survivors, %", 26, TEAL).move_to([-1.9, 3.1, 0])
        sk = chip("in this sketch: equal starting numbers", GREY, 24).move_to([3.9, 2.9, 0]) if False else None
        sk = T("in this sketch: equal starting numbers", 24, GREY).move_to([-1.9, -3.35, 0]).align_to(xt, LEFT) if False else T("in this sketch: equal starting numbers", 24, GREY)
        sk.move_to([3.5, 2.7, 0])
        self.add(ax, xl, yl, xt)
        pts = [ax.c2p(t, 100 * share(t)) for t in range(6)]
        dots = [Dot(p, radius=0.11, color=TEAL) for p in pts]
        self.add(yt, sk)
        self.at("The ratio compounds")
        l0 = M("day 0: 50%", 26, TEAL).next_to(dots[0], RIGHT, buff=0.3).shift(UP * 0.3)
        self.play(FadeIn(dots[0], scale=0.5), FadeIn(l0), run_time=0.6)
        self.at("Each extra day")
        l1 = M("day 1: 47.6%", 26, TEAL).next_to(dots[1], RIGHT, buff=0.3).shift(UP * 0.45)
        seg = Line(pts[0], pts[1], color=TEAL, stroke_width=4)
        self.play(Create(seg), FadeIn(dots[1], scale=0.5), FadeIn(l1), run_time=0.7)
        rr = M("× 0.909 each day", 28, YELLOW).move_to([3.5, 1.2, 0])
        self.at("multiplies the dark to pale")
        self.play(FadeIn(rr, shift=LEFT * 0.2), run_time=0.6)
        self.at("again")
        segs = []
        for k in range(2, 5):
            s = Line(pts[k - 1], pts[k], color=TEAL, stroke_width=4)
            self.play(Create(s), FadeIn(dots[k], scale=0.5), run_time=0.3)
        self.at("After five days")
        s5 = Line(pts[4], pts[5], color=TEAL, stroke_width=4)
        r5 = M("0.909⁵ = 0.621", 30, YELLOW).move_to([3.5, 0.0, 0])
        self.play(Create(s5), FadeIn(dots[5], scale=0.5), FadeIn(r5, shift=LEFT * 0.2), run_time=0.9)
        self.at("is then about")
        l5 = M("day 5: 38%", 26, TEAL).next_to(dots[5], DOWN, buff=0.3).shift(LEFT * 0.3)
        self.play(FadeIn(l5), Indicate(dots[5], color=TEAL, scale_factor=1.8), run_time=0.8)
        self.finish()


class S06Limits(SpokenScene):
    def construct(self):
        head = chip("0.091: relative, per day, one site", YELLOW, 30).move_to([0, 3.0, 0])
        self.at("Keep the limits")
        self.play(FadeIn(head, shift=DOWN * 0.2), run_time=0.7)
        self.at("relative and per day")
        self.play(Indicate(head, color=YELLOW, scale_factor=1.06), run_time=0.7)
        names = ["annual decline", "absolute death rate", "all of Britain"]
        row = VGroup(*[chip(n, GREY, 28) for n in names]).arrange(RIGHT, buff=0.5).move_to([0, 1.5, 0])
        xs = []
        for ph, c in zip(["not an annual decline", "not an absolute death rate", "all of Britain"], row):
            self.at(ph)
            x = cross(c)
            self.play(FadeIn(c), run_time=0.35)
            self.play(Create(x), run_time=0.4)
            xs.append(x)
        # witnessed fraction
        W = 8.0
        wit = Rectangle(width=W * 0.26, height=0.7, fill_color=GREEN, fill_opacity=0.85, stroke_color=TEXT, stroke_width=2)
        rest = Rectangle(width=W * 0.74, height=0.7, fill_color=GREY, fill_opacity=0.35, stroke_color=TEXT, stroke_width=2)
        bar_ = VGroup(wit, rest).arrange(RIGHT, buff=0).move_to([0, -0.1, 0])
        t1 = T("disappeared moths", 26, GREY).next_to(bar_, UP, buff=0.15).align_to(bar_, LEFT)
        t2 = T("26% witnessed bird attacks", 26, GREEN).next_to(bar_, DOWN, buff=0.2).align_to(bar_, LEFT)
        self.at("also disappeared")
        self.play(FadeIn(t1), FadeIn(bar_), run_time=0.7)
        self.at("witnessed bird attacks")
        self.play(FadeIn(t2), Indicate(wit, color=GREEN, scale_factor=1.1), run_time=0.8)
        a = chip("morph share", TEAL, 28)
        b = chip("allele frequency", GREY, 28)
        arrow = Arrow(LEFT * 0.7, RIGHT * 0.7, color=GREY, stroke_width=5, buff=0)
        grp = VGroup(a, arrow, b).arrange(RIGHT, buff=0.3).move_to([0, -2.0, 0])
        nyet = T("different", 26, RED, weight=BOLD).next_to(arrow, UP, buff=0.12)
        self.at("A change in morph share")
        self.play(FadeIn(a), run_time=0.5)
        self.at("allele frequency")
        self.play(GrowArrow(arrow), FadeIn(b), FadeIn(nyet), run_time=0.7)
        rule = T("relative daily survival → change in morph share, at one site", 26, YELLOW)
        fit(rule, max_w=11.8)
        rule.move_to([0, -3.15, 0])
        self.at("A relative daily survival compounds")
        self.play(FadeIn(rule, shift=UP * 0.15), run_time=0.8)
        self.finish()


class S07End(EndCard):
    LINE = "Relative daily survival compounds into morph share, at one site."
