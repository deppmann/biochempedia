"""Demography and survivorship: count survivors, then count births  (Biochemistrypedia explainer)

COLOR MAP (one color per concept, whole video)
  BLUE   = alive / seen (counts n, survivorship l)
  RED    = deaths (the part of a bar that dies, q)
  GREEN  = daughters (births)
  YELLOW = R0, the result
  GREY   = outlines, axes, birds not seen, captions
"""
import numpy as np
from bp_style import *  # noqa: F401,F403

K = 0.032          # screen units per animal in the bars (scenes 4-5, tall enough for 170)
KB = 0.042         # larger scale for scenes 2-3, where only 100 is needed
BASE = -2.8
BW = 1.0
N = [100, 80, 40, 10, 0]
MX = [0, 1, 2, 1, 0]
XS = [-5.5 + 1.75 * i for i in range(5)]
SX = 4.0           # x of the daughter stack
L_TXT = ["1.0", "0.8", "0.4", "0.1", "0"]
Q_TXT = ["0.20", "0.50", "0.75", "1.00"]


def rect(x, y0, h, w, color, op=0.8):
    return Rectangle(width=w, height=h, stroke_color=color, stroke_width=2.5, fill_color=color,
                     fill_opacity=op).move_to([x, y0 + h / 2, 0])


def blue_bars(k=K, base=BASE, xs=XS, bw=BW):
    return [rect(x, base, max(n * k, 0.03), bw, BLUE) for x, n in zip(xs, N)]


def red_parts(k=K, base=BASE, xs=XS, bw=BW):
    out = []
    for i in range(4):
        d = N[i] - N[i + 1]
        out.append(rect(xs[i], base + N[i + 1] * k, d * k, bw, RED, 0.9))
    return out


def green_blocks(k=K, base=BASE, xs=XS):
    out = {}
    for i in (1, 2, 3):
        h = N[i] * MX[i] * k
        out[i] = rect(xs[i] + 0.8, base, h, 0.5, GREEN, 0.85)
    return out


def stack_segments(k=K, base=BASE, sx=SX, w=1.2):
    segs, y = {}, base
    for i in (1, 2, 3):
        h = N[i] * MX[i] * k
        segs[i] = rect(sx, y, h, w, GREEN, 0.85)
        y += h
    return segs


def axis(base=BASE, xs=XS):
    line = Line([-6.2, base, 0], [2.3, base, 0], color=GREY, stroke_width=3)
    labs = [T(f"age {a}", 24, GREY).move_to([x, base - 0.35, 0]) for a, x in enumerate(xs)]
    return line, VGroup(*labs)


def n_labels(k=K, base=BASE, xs=XS):
    return [M(str(n), 26, BLUE).move_to([x, base + max(n * k, 0.03) + 0.3, 0]) for x, n in zip(xs, N)]


def cap(text, y=3.15, x=-1.9):
    return T(text, 26, GREY).move_to([x, y, 0])


class S00Title(TitleCard):
    LESSON = "Demography and survivorship"
    TITLE = "Count survivors, then count births"


# ---------------------------------------------------------------------------------------------
class S01Birds(SpokenScene):
    """100 banded birds, 60 seen, 40 not: dead, unseen, or elsewhere?"""

    def construct(self):
        cx, cy = -3.4, -0.2
        box = RoundedRectangle(corner_radius=0.2, width=4.9, height=5.3, stroke_color=GREY, stroke_width=3).move_to([cx, cy, 0])
        box_lbl = T("colony", 26, GREY).move_to([cx, 2.85, 0])
        dots = []
        for i in range(100):
            r, c = divmod(i, 10)
            p = [cx + (c - 4.5) * 0.44, cy + (4.5 - r) * 0.44, 0]
            dots.append(Dot(p, radius=0.13, color=TEXT))
        dg = VGroup(*dots)
        tag = T("schematic", 24, GREY).move_to([5.3, 3.2, 0])
        self.add(tag)
        self.at("banded birds")
        self.play(FadeIn(box), FadeIn(box_lbl), LaggedStart(*[FadeIn(d, scale=0.5) for d in dots], lag_ratio=0.008), run_time=1.0)

        seen = [d for i, d in enumerate(dots) if i % 10 < 6]
        unseen = [d for i, d in enumerate(dots) if i % 10 >= 6]
        seen_lbl = T("60 seen next year", 32, BLUE).move_to([3.65, 2.2, 0])
        self.at("60 are seen")
        self.play(*[d.animate.set_color(BLUE) for d in seen], FadeIn(seen_lbl), run_time=0.8)

        un_lbl = T("40 not seen: fate unknown", 30, GREY).move_to([3.65, 1.45, 0])
        self.at("Did 40 die")
        self.play(*[d.animate.set_color(GREY) for d in unseen], FadeIn(un_lbl), run_time=0.8)

        # alive and unseen: twelve dots become blue rings
        hollow_idx = [r * 10 + c for r in range(3) for c in (6, 7, 8, 9)]
        move_idx = [r * 10 + c for r in (5, 6, 7, 8) for c in (8, 9)]
        self.at("alive and unseen")
        alive_lbl = T("some may have died,\nmoved, or been missed", 24, GREY).move_to([3.65, 0.5, 0])
        self.play(*[dots[i].animate.set_color(GREY).set_fill(BG, 1).set_stroke(GREY, 3) for i in hollow_idx], FadeIn(alive_lbl), run_time=0.8)

        box2 = RoundedRectangle(corner_radius=0.2, width=4.4, height=2.2, stroke_color=GREY, stroke_width=3).move_to([3.65, -1.7, 0])
        box2_lbl = T("another colony", 26, GREY).move_to([3.65, -3.15, 0])
        self.at("another colony")
        self.play(FadeIn(box2), FadeIn(box2_lbl), run_time=0.5)
        anims = []
        for j, i in enumerate(move_idx):
            tx = 2.5 + (j % 4) * 0.7
            ty = -1.25 - (j // 4) * 0.8
            anims.append(dots[i].animate.set_color(GREY).set_fill(BG, 1).set_stroke(GREY, 3).move_to([tx, ty, 0]))
        self.play(*anims, run_time=1.2)
        self.at("clean count")
        self.play(Indicate(dg, color=BLUE, scale_factor=1.03), run_time=0.8)
        self.finish()


# ---------------------------------------------------------------------------------------------
class S02Cohort(SpokenScene):
    """number alive at each age."""

    def construct(self):
        line, labs = axis()
        bars = blue_bars(KB)
        nl = n_labels(KB)
        dots = VGroup(*[Dot([-1.9 + (c - 4.5) * 0.34, 0.2 + (4.5 - r) * 0.34, 0], radius=0.1, color=BLUE)
                        for r in range(10) for c in range(10)])
        self.at("cohort is a group")
        c1 = cap("A cohort: individuals born together", y=3.2)
        self.play(FadeIn(c1), LaggedStart(*[FadeIn(d, scale=0.5) for d in dots], lag_ratio=0.01), run_time=1.0)
        self.at("Follow one from birth")
        self.play(Create(line), FadeIn(labs), run_time=0.8)
        self.at("how many are still alive")
        c2 = cap("n = how many are still alive at each age", y=3.2)
        self.play(ReplacementTransform(c1, c2), run_time=0.5)
        self.at("cohort of females")
        c3 = cap("A made-up cohort of females, closed and completely observed", y=3.2)
        self.play(ReplacementTransform(c2, c3), run_time=0.5)

        def grow(i):
            self.play(GrowFromEdge(bars[i], DOWN) if N[i] > 0 else FadeIn(bars[i]), FadeIn(nl[i], shift=DOWN * 0.15), run_time=0.7)
        self.at("starts with")
        self.play(dots.animate.move_to([XS[0], BASE + 1.0, 0]).scale(0.3).set_opacity(0), run_time=0.6)
        grow(0)
        self.at("A year later")
        grow(1)
        self.at("Then 40")
        grow(2)
        self.at("Then 10")
        grow(3)
        self.at("Then none")
        grow(4)
        self.finish()


# ---------------------------------------------------------------------------------------------
class S03Deaths(SpokenScene):
    """survivorship, then deaths over the number alive at the start of the interval."""

    def construct(self):
        line, labs = axis()
        bars = blue_bars(KB)
        nl = n_labels(KB)
        c3 = cap("A made-up cohort of females, closed and completely observed", y=3.2)
        self.add(line, labs, *bars, *nl, c3)

        ll = [T(f"l = {t}", 24, BLUE).move_to([x, 2.35, 0]) for x, t in zip(XS, L_TXT)]
        self.at("Divide each count")
        c4 = cap("l = n divided by the starting 100: survivorship", y=3.2)
        self.play(ReplacementTransform(c3, c4), run_time=0.5)
        self.play(LaggedStart(*[FadeIn(t, shift=DOWN * 0.15) for t in ll], lag_ratio=0.15), run_time=1.2)

        reds = red_parts(KB)
        self.at("count the deaths")
        c5 = cap("deaths in each year", y=3.2)
        self.play(ReplacementTransform(c4, c5), *[FadeOut(t) for t in ll], run_time=0.5)
        self.play(LaggedStart(*[FadeIn(r) for r in reds], lag_ratio=0.2), run_time=1.0)

        self.at("number alive at the start")
        self.play(*[Indicate(b, color=YELLOW, scale_factor=1.04) for b in bars[:4]], run_time=0.9)
        # not by the original 100
        ref = DashedLine([-6.2, BASE + 100 * KB, 0], [2.3, BASE + 100 * KB, 0], color=GREY, dash_length=0.15)
        ref_lbl = T("not the original 100", 24, GREY).move_to([4.1, BASE + 100 * KB, 0])
        self.at("not by the original")
        self.play(Create(ref), FadeIn(ref_lbl), run_time=0.6)

        qs = [T(f"q = {t}", 26, RED).move_to([x, 2.35, 0]) for x, t in zip(XS, Q_TXT)]
        self.at("a fifth die")
        self.play(FadeOut(ref), FadeOut(ref_lbl), FadeIn(qs[0], shift=DOWN * 0.15), run_time=0.5)
        self.at("Then half")
        self.play(FadeIn(qs[1], shift=DOWN * 0.15), run_time=0.5)
        self.at("three quarters")
        self.play(FadeIn(qs[2], shift=DOWN * 0.15), run_time=0.5)
        self.at("Then all")
        self.play(FadeIn(qs[3], shift=DOWN * 0.15), run_time=0.5)
        self.at("rises with age")
        arrow = Arrow([XS[0], 3.0, 0], [XS[3], 3.0, 0], color=RED, buff=0, stroke_width=5)
        self.play(FadeOut(c5), run_time=0.3)
        self.play(GrowArrow(arrow), run_time=0.6)
        self.finish()


# ---------------------------------------------------------------------------------------------
class S04Births(SpokenScene):
    """daughters per surviving female at ages 1, 2, 3 stack into 170 from 100 founders."""

    def construct(self):
        line, labs = axis()
        bars_b = blue_bars(KB)
        nl_b = n_labels(KB)
        reds = red_parts(KB)
        qs = [T(f"q = {t}", 26, RED).move_to([x, 2.35, 0]) for x, t in zip(XS, Q_TXT)]
        arrow = Arrow([XS[0], 3.0, 0], [XS[3], 3.0, 0], color=RED, buff=0, stroke_width=5)
        self.add(line, labs, *bars_b, *nl_b, *reds, *qs, arrow)
        bars = blue_bars()
        nl = n_labels()
        self.at("add the births")
        c = cap("births: daughters per surviving female", y=3.2)
        self.play(*[FadeOut(r) for r in reds], *[FadeOut(q) for q in qs], FadeOut(arrow), FadeIn(c), run_time=0.6)
        self.play(*[ReplacementTransform(a, b) for a, b in zip(bars_b, bars)],
                  *[ReplacementTransform(a, b) for a, b in zip(nl_b, nl)], run_time=0.8)

        gb = green_blocks()
        tags = {1: "80 x 1", 2: "40 x 2", 3: "10 x 1"}
        tag_m = {i: M(tags[i], 24, GREEN).move_to([XS[i] + 0.4, BASE + max(N[i], N[i] * MX[i]) * K + 0.85, 0]) for i in (1, 2, 3)}
        self.at("At age 1")
        self.play(GrowFromEdge(gb[1], DOWN), FadeIn(tag_m[1]), run_time=0.7)
        self.at("At age 2")
        self.play(GrowFromEdge(gb[2], DOWN), FadeIn(tag_m[2]), run_time=0.7)
        self.at("At age 3")
        self.play(GrowFromEdge(gb[3], DOWN), FadeIn(tag_m[3]), run_time=0.7)

        segs = stack_segments()
        self.at("That makes")
        self.play(*[FadeOut(tag_m[i]) for i in (1, 2, 3)],
                  *[ReplacementTransform(gb[i], segs[i]) for i in (1, 2, 3)], run_time=1.6)
        top = BASE + 170 * K
        d_lbl = T("170 daughters", 28, GREEN).move_to([SX, top + 0.4, 0])
        self.at("170 daughters")
        self.play(FadeIn(d_lbl, shift=DOWN * 0.15), run_time=0.6)
        ref = DashedLine([SX - 0.75, BASE + 100 * K, 0], [SX + 0.75, BASE + 100 * K, 0], color=BLUE, dash_length=0.12)
        f_lbl = T("100\nfounders", 24, BLUE).move_to([5.65, BASE + 100 * K, 0])
        self.at("founders")
        self.play(Create(ref), FadeIn(f_lbl), run_time=0.7)
        self.finish()


# ---------------------------------------------------------------------------------------------
class S05Rnought(SpokenScene):
    """R0 = 1.7, what above, below and at one mean."""

    def construct(self):
        line, labs = axis()
        bars = blue_bars()
        nl = n_labels()
        segs = stack_segments()
        top = BASE + 170 * K
        d_lbl = T("170 daughters", 28, GREEN).move_to([SX, top + 0.4, 0])
        ref = DashedLine([SX - 0.75, BASE + 100 * K, 0], [SX + 0.75, BASE + 100 * K, 0], color=BLUE, dash_length=0.12)
        f_lbl = T("100\nfounders", 24, BLUE).move_to([5.65, BASE + 100 * K, 0])
        c = cap("births: daughters per surviving female", y=3.2)
        stack = VGroup(*segs.values(), d_lbl, ref, f_lbl)
        self.add(line, labs, *bars, *nl, c, stack)

        r_lbl = M("R₀ = 1.7", 60, YELLOW).move_to([2.0, 2.4, 0])
        sub = T("daughters per newborn female", 28).move_to([2.0, 1.5, 0])
        self.at("net reproductive rate")
        self.play(FadeOut(VGroup(line, labs, *bars, *nl, c)), stack.animate.shift(LEFT * 9.0), run_time=1.0)
        self.play(FadeIn(r_lbl, shift=DOWN * 0.2), run_time=0.6)
        self.at("daughters per newborn")
        self.play(FadeIn(sub), run_time=0.5)
        per = T("per generation, not per year", 26, GREY).move_to([2.0, 0.85, 0])
        self.at("per generation")
        self.play(FadeIn(per), run_time=0.5)

        # number line, x = -1.5 + 2.8 v
        def px(v):
            return -1.5 + 2.8 * v
        nline = Line([px(0), -1.2, 0], [px(2.5), -1.2, 0], color=GREY, stroke_width=4)
        ticks = VGroup(*[VGroup(Line([px(v), -1.1, 0], [px(v), -1.3, 0], color=GREY, stroke_width=3),
                                M(str(v), 22, GREY).move_to([px(v), -1.6, 0])) for v in (0, 1, 2)])
        self.at("stayed fixed")
        mark = Dot([px(1.7), -1.2, 0], radius=0.15, color=YELLOW)
        m_lbl = M("1.7", 24, YELLOW).move_to([px(1.7), -0.7, 0])
        self.play(Create(nline), FadeIn(ticks), FadeIn(mark, scale=1.5), FadeIn(m_lbl), run_time=0.6)
        grows = T("grows in the long run", 26).move_to([px(1.75), -2.1, 0])
        decl = T("declines", 26).move_to([px(0.5), -2.1, 0])
        repl = T("just replaces itself", 24).move_to([px(1.0), -0.35, 0])
        self.at("above one")
        self.play(FadeIn(grows, shift=UP * 0.1), run_time=0.5)
        self.at("Below one")
        self.play(FadeIn(decl, shift=UP * 0.1), run_time=0.5)
        self.at("At exactly one")
        self.play(FadeIn(repl), Indicate(ticks[1], color=YELLOW), run_time=0.7)
        pred = T("a model's verdict if rates stay fixed, not an observation", 24, GREY).move_to([1.8, -2.95, 0])
        self.at("prediction from assumptions")
        self.play(FadeIn(pred), run_time=0.6)
        self.finish()


# ---------------------------------------------------------------------------------------------
class S06Missing(SpokenScene):
    """missing is not dead; the rule."""

    def construct(self):
        q = Dot([-4.6, 0.2, 0], radius=0.5, color=GREY)
        q_t = T("?", 52, BG, weight=BOLD).move_to(q)
        q_lbl = T("bird not seen", 30, GREY).move_to([-4.6, -0.8, 0])
        self.at("only as good as its counts")
        self.play(FadeIn(q, scale=0.6), FadeIn(q_t), FadeIn(q_lbl), run_time=0.7)

        def branch(text, y, color):
            ch = chip(text, color, size=34).move_to([1.8, y, 0])
            ar = Arrow([-3.9, 0.2, 0], [ch.get_left()[0] - 0.05, y, 0], buff=0.05, color=color, stroke_width=5)
            return ch, ar
        b1 = branch("alive, missed", 2.2, BLUE)
        b2 = branch("alive, gone elsewhere", 0.2, BLUE)
        b3 = branch("dead", -1.8, RED)
        self.at("alive and missed")
        self.play(GrowArrow(b1[1]), FadeIn(b1[0], shift=RIGHT * 0.2), run_time=0.6)
        self.at("alive and gone")
        self.play(GrowArrow(b2[1]), FadeIn(b2[0], shift=RIGHT * 0.2), run_time=0.6)
        self.at("Missing is not dead")
        self.play(GrowArrow(b3[1]), FadeIn(b3[0], shift=RIGHT * 0.2), run_time=0.6)
        self.play(Indicate(VGroup(b1[0], b2[0]), color=BLUE, scale_factor=1.06), run_time=0.8)

        # the table again, compact
        k, base = 0.03, -2.8
        xs = [-5.2 + 1.3 * i for i in range(5)]
        bars = blue_bars(k, base, xs, 0.9)
        reds = red_parts(k, base, xs, 0.9)
        segs = stack_segments(k, base, 2.4, 1.1)
        line = Line([-6.0, base, 0], [0.8, base, 0], color=GREY, stroke_width=3)
        sline = Line([1.6, base, 0], [3.2, base, 0], color=GREY, stroke_width=3)
        b_lbl = T("survivors by age", 28, BLUE).move_to([-2.6, 0.7, 0])
        g_lbl = T("births by age", 28, GREEN).move_to([2.4, base + 170 * k + 0.45, 0])
        r_lbl = M("R₀ = 1.7", 44, YELLOW).move_to([4.75, 0.2, 0])
        old = VGroup(q, q_t, q_lbl, b1[0], b1[1], b2[0], b2[1], b3[0], b3[1])
        self.at("count the survivors")
        self.play(FadeOut(old), Create(line), Create(sline), *[FadeIn(b) for b in bars], *[FadeIn(r) for r in reds],
                  FadeIn(b_lbl), run_time=0.8)
        self.at("and the births")
        self.play(*[FadeIn(s) for s in segs.values()], FadeIn(g_lbl), run_time=0.8)
        self.at("and R0 says")
        hedge = T("if rates stayed fixed", 24, GREY).move_to([4.75, -0.5, 0])
        self.play(FadeIn(r_lbl, shift=DOWN * 0.2), FadeIn(hedge), run_time=0.7)
        self.finish()


class S07End(EndCard):
    LINE = "If rates stay fixed, survivors and births show replacement."
