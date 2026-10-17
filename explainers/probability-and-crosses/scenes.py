"""How far can a count stray?  (Biochemistrypedia explainer, Genetics: probability and crosses)

COLOR MAP (one colour per concept, whole film)
  BLUE   = observed counts
  YELLOW = expected counts (what the ratio predicts)
  TEAL   = the chi-square statistic (our value, the pieces that add to it)
  GREEN  = the p-value (area of chance deviations at least this big)
  RED    = the critical value / things the p-value is NOT / crossed-out claims
  GOLD   = coins (probability scatter)
  GREY   = axes, labels, structure
"""
import math, random
import numpy as np
from bp_style import *  # noqa: F401,F403

COLS = [-3.2, -0.9, 1.4, 3.7]
BARW = 1.3


def bars(vals, scale, base, cols=COLS, w=BARW, color=BLUE):
    g = VGroup()
    for v, x in zip(vals, cols):
        r = Rectangle(width=w, height=v * scale, stroke_color=color, stroke_width=3,
                      fill_color=color, fill_opacity=0.35)
        r.move_to([x, base + v * scale / 2, 0])
        g.add(r)
    return g


def ticks(vals, scale, base, cols=COLS, w=1.8, sw=6):
    return VGroup(*[Line([x - w / 2, base + v * scale, 0], [x + w / 2, base + v * scale, 0],
                         color=YELLOW, stroke_width=sw) for v, x in zip(vals, cols)])


def rowlabel(text, y, color, x=-5.6):
    return T(text, 24, color).move_to([x, y, 0])


def rownums(vals, y, color, cols=COLS, size=26):
    return VGroup(*[M(str(v), size, color).move_to([x, y, 0]) for v, x in zip(vals, cols)])


def cross(mob, color=RED):
    c = Circle(radius=0.3, stroke_color=color, stroke_width=5, fill_color=BG, fill_opacity=1)
    c.move_to(mob.get_left() + LEFT * 0.55)
    a = Line(c.get_center() + UL * 0.15, c.get_center() + DR * 0.15, color=color, stroke_width=6)
    b = Line(c.get_center() + DL * 0.15, c.get_center() + UR * 0.15, color=color, stroke_width=6)
    return VGroup(c, a, b)


def pdf3(x):
    return math.sqrt(x) * math.exp(-x / 2) / math.sqrt(2 * math.pi)


def make_plot(w, h, center):
    ax = Axes(x_range=[0, 12, 1], y_range=[0, 0.27, 0.1], x_length=w, y_length=h, tips=False,
              axis_config={"include_numbers": False, "include_ticks": False, "color": GREY, "stroke_width": 3})
    ax.move_to(center)
    curve = ax.plot(pdf3, x_range=[0.001, 12], color=TEXT, stroke_width=4)
    area = ax.get_area(curve, x_range=[1.78, 12], color=GREEN, opacity=0.45)
    tail = ax.get_area(curve, x_range=[7.81, 12], color=RED, opacity=0.7)
    mine = DashedLine(ax.c2p(1.78, 0), ax.c2p(1.78, pdf3(1.78)), color=TEAL, stroke_width=5)
    crit = Line(ax.c2p(7.81, 0), ax.c2p(7.81, 0.11), color=RED, stroke_width=5)
    return ax, curve, area, tail, mine, crit


class S00Title(TitleCard):
    LESSON = "Probability, crosses and the chi-square test"
    TITLE = "How Far Can a Count Stray?"


MENDEL = [315, 108, 101, 32]
MEXP = [312.75, 104.25, 104.25, 34.75]
OBS = [98, 28, 26, 8]
EXP = [90, 30, 30, 10]


# ---------------------------------------------------------------------------------------------
class S01Stray(SpokenScene):
    def construct(self):
        sc, base = 0.0125, -1.0
        b = bars(MENDEL, sc, base)
        names = VGroup(*[T(n, 22, GREY).move_to([x, -1.4, 0]) for n, x in zip(
            ["round yellow", "round green", "wrinkled yellow", "wrinkled green"], COLS)])
        lab1, lab2 = rowlabel("counted", -2.1, BLUE), rowlabel("predicted", -2.8, YELLOW)
        n1 = rownums(MENDEL, -2.1, BLUE)
        n2 = VGroup(*[M(str(v), 26, YELLOW).move_to([x, -2.8, 0]) for v, x in zip(MEXP, COLS)])
        seeds = T("556 seeds", 28, TEXT).move_to([-5.4, 3.0, 0])
        self.at("Mendel counted")
        self.play(FadeIn(seeds), run_time=0.5)
        self.at("hybrid peas")
        self.play(*[GrowFromEdge(r, DOWN) for r in b], FadeIn(names), FadeIn(lab1), FadeIn(n1), run_time=1.2)
        tk = ticks(MEXP, sc, base)
        self.at("predicts")
        self.play(Create(tk), FadeIn(lab2), FadeIn(n2), run_time=1.2)
        self.at("He counted")
        self.play(Indicate(n1[0], color=BLUE, scale_factor=1.3), Indicate(n2[0], color=YELLOW, scale_factor=1.3), run_time=1.2)
        self.at("None of")
        self.play(*[Indicate(m, color=BLUE, scale_factor=1.25) for m in n1[1:]],
                  *[Indicate(m, color=YELLOW, scale_factor=1.25) for m in n2[1:]], run_time=1.2)
        q = T("How far can a count\nstray?", 36, TEXT, font=TITLE_FONT).move_to([2.6, 2.2, 0])
        self.at("how far")
        self.play(FadeIn(q, shift=UP * 0.1), run_time=0.8)
        self.finish()


# ---------------------------------------------------------------------------------------------
class S02Scatter(SpokenScene):
    def construct(self):
        random.seed(4)
        xs = [(-4.05 + 0.9 * i) for i in range(10)]

        def coins(pattern):
            g = VGroup()
            for p, x in zip(pattern, xs):
                g.add(Circle(radius=0.32, stroke_color=GOLD, stroke_width=4, fill_color=GOLD,
                             fill_opacity=0.9 if p else 0.0).move_to([x, 0.9, 0]))
            return g
        pats = [[random.random() < 0.5 for _ in range(10)] for _ in range(4)]
        c = coins(pats[0])
        lbl = T("ten coin tosses", 30, GOLD).move_to([0, -0.2, 0])
        prob = M("9 : 3 : 3 : 1  =  probabilities", 34, YELLOW).move_to([0, 2.6, 0])
        self.at("A ratio is a probability")
        self.play(FadeIn(prob), run_time=0.6)
        self.at("scatter around")
        self.play(FadeIn(c), FadeIn(lbl), run_time=0.6)
        for p in pats[1:]:
            n = coins(p)
            self.play(Transform(c, n), run_time=0.4)
            self.wait(0.6)
        self.at("one number")
        self.wait(0.1)
        # to the bars
        sc, base = 0.04, -1.0
        b = bars(OBS, sc, base)
        ratio = rowlabel("ratio", -1.45, GREY)
        rn = VGroup(*[M(s, 28, GREY).move_to([x, -1.45, 0]) for s, x in zip("9331", COLS)])
        lab = rowlabel("observed", -2.1, BLUE)
        nums = rownums(OBS, -2.1, BLUE)
        tot = chip("160 plants", TEXT, 26).move_to([-5.2, 3.0, 0])
        self.at("dihybrid")
        self.play(FadeOut(c), FadeOut(lbl), FadeOut(prob), run_time=0.5)
        self.play(FadeIn(tot), *[GrowFromEdge(r, DOWN) for r in b], FadeIn(ratio), FadeIn(rn), run_time=1.0)
        self.at("It gives")
        self.play(FadeIn(lab), FadeIn(nums), run_time=0.8)
        q = M("fits 9 : 3 : 3 : 1 ?", 40, YELLOW).move_to([2.2, 2.3, 0])
        self.at("Does it fit")
        self.play(FadeIn(q, shift=UP * 0.1), run_time=0.7)
        self.finish()


# ---------------------------------------------------------------------------------------------
class S03Expected(SpokenScene):
    def construct(self):
        sc, base = 0.04, -1.0
        b = bars(OBS, sc, base)
        ratio = rowlabel("ratio", -1.45, GREY)
        rn = VGroup(*[M(s, 28, GREY).move_to([x, -1.45, 0]) for s, x in zip("9331", COLS)])
        lab = rowlabel("observed", -2.1, BLUE)
        nums = rownums(OBS, -2.1, BLUE)
        tot = chip("160 plants", TEXT, 26).move_to([-5.2, 3.0, 0])
        self.add(b, ratio, rn, lab, nums, tot)
        elab = rowlabel("expected", -2.75, YELLOW)
        tk = ticks(EXP, sc, base)
        en = rownums(EXP, -2.75, YELLOW)

        def deriv(s):
            return M(s, 38, YELLOW).move_to([2.2, 2.4, 0])
        self.at("find the expected")
        self.play(FadeIn(elab), run_time=0.5)
        self.at("Multiply the total")
        self.play(Indicate(tot, color=TEXT), run_time=0.9)
        d = deriv("160 × 9/16 = 90")
        self.at("9 sixteenths")
        self.play(FadeIn(d), Create(tk[0]), FadeIn(en[0]), run_time=0.8)
        d2 = deriv("160 × 3/16 = 30")
        self.at("Three sixteenths")
        self.play(Transform(d, d2), Create(tk[1]), Create(tk[2]), FadeIn(en[1]), FadeIn(en[2]), run_time=0.8)
        d3 = deriv("160 × 1/16 = 10")
        self.at("One sixteenth")
        self.play(Transform(d, d3), Create(tk[3]), FadeIn(en[3]), run_time=0.8)
        self.at("each observed count")
        self.play(FadeOut(d), run_time=0.4)
        self.play(*[Indicate(r, color=BLUE, scale_factor=1.05) for r in b], run_time=1.0)
        self.finish()


# ---------------------------------------------------------------------------------------------
class S04Distance(SpokenScene):
    def construct(self):
        cx = [-4.65, -1.55, 1.55, 4.65]
        sc, base = 0.0135, 1.9
        cards = VGroup(*[RoundedRectangle(corner_radius=0.15, width=2.9, height=4.0, stroke_color=GREY,
                                          stroke_width=2, fill_opacity=0).move_to([x, 1.4, 0]) for x in cx])
        b = bars(OBS, sc, base, cx, w=0.9)
        tk = ticks(EXP, sc, base, cx, w=1.2, sw=5)
        vs = VGroup()
        for o, e, x in zip(OBS, EXP, cx):
            vs.add(VGroup(M(str(o), 26, BLUE), T("vs", 22, GREY), M(str(e), 26, YELLOW)).arrange(RIGHT, buff=0.2).move_to([x, 1.5, 0]))
        parts = []
        for o, e, x in zip(OBS, EXP, cx):
            p1, p2, p3 = M(f"({o}−{e})", 26), M("2", 18), M(f"/{e}", 26)
            g = VGroup(p1, p2, p3).arrange(RIGHT, buff=0.03)
            p2.shift(UP * 0.14)
            g.move_to([x, 0.8, 0])
            parts.append((p1, p2, p3))
        res = VGroup(*[M(s, 30, TEAL, weight=BOLD).move_to([x, 0.05, 0]) for s, x in zip(
            ["0.711", "0.133", "0.533", "0.400"], cx)])
        sm = M("0.711 + 0.133 + 0.533 + 0.400", 34, TEAL)
        sm.move_to([0, -1.5, 0]); fit(sm, 11.5)
        total = T("chi-square = 1.78", 54, TEAL, weight=BOLD).move_to([0, -2.7, 0])
        hd = T("chi-square", 54, TEAL, weight=BOLD).move_to([0, 2.7, 0])
        ob = Rectangle(width=1.3, height=2.2, stroke_color=BLUE, stroke_width=3, fill_color=BLUE, fill_opacity=0.35).move_to([-2.2, -0.4, 0])
        ol = T("observed", 28, BLUE).next_to(ob, DOWN, buff=0.25)
        ex = Line([-2.85, 1.7, 0], [-1.55, 1.7, 0], color=YELLOW, stroke_width=7)
        el = T("expected", 28, YELLOW).next_to(ex, UP, buff=0.2)
        self.at("Pearson's")
        self.play(FadeIn(hd), run_time=0.6)
        self.play(FadeIn(ob), FadeIn(ol), run_time=0.6)
        self.play(Create(ex), FadeIn(el), run_time=0.6)
        self.at("measures the distance")
        dist = DoubleArrow([-0.9, 0.7, 0], [-0.9, 1.7, 0], color=TEAL, stroke_width=6, buff=0)
        dl = T("distance", 32, TEAL).next_to(dist, RIGHT, buff=0.2)
        self.play(Create(dist), FadeIn(dl), run_time=0.8)
        self.at("For each class")
        self.play(*[FadeOut(m) for m in (hd, ob, ol, ex, el, dist, dl)], FadeIn(cards), run_time=0.7)
        self.play(*[GrowFromEdge(r, DOWN) for r in b], Create(tk), FadeIn(vs), run_time=1.2)
        self.at("observed minus expected")
        self.play(*[FadeIn(p[0]) for p in parts], run_time=0.7)
        self.at("square it")
        self.play(*[FadeIn(p[1]) for p in parts], run_time=0.5)
        self.at("divide by")
        self.play(*[FadeIn(p[2]) for p in parts], run_time=0.5)
        self.at("The four classes")
        self.play(LaggedStart(*[FadeIn(r, shift=DOWN * 0.1) for r in res], lag_ratio=0.6), run_time=2.4)
        self.at("Add them up")
        self.play(FadeIn(sm, shift=DOWN * 0.1), run_time=0.8)
        self.at("chi square is")
        self.play(FadeIn(total, scale=0.9), run_time=0.7)
        self.finish()


# ---------------------------------------------------------------------------------------------
class S05Toobig(SpokenScene):
    def construct(self):
        # part A: degrees of freedom
        chips = VGroup(*[chip(str(v), BLUE, 46) for v in OBS]).arrange(RIGHT, buff=0.6).move_to([-2.4, 1.3, 0])
        tot = chip("total 160", TEXT, 40).move_to([4.3, 1.3, 0])
        df = T("4 classes − 1 = 3 degrees of freedom", 46).move_to([0, -0.8, 0])
        tag = T("set", 30, YELLOW).next_to(chips[3], DOWN, buff=0.15)
        self.at("four classes")
        self.play(FadeIn(chips, shift=DOWN * 0.1), run_time=0.8)
        self.at("4 minus 1")
        self.play(FadeIn(df), run_time=0.7)
        self.at("Once three counts")
        self.play(*[Indicate(c, color=BLUE, scale_factor=1.2) for c in chips[:3]], FadeIn(tot), run_time=1.2)
        self.at("the fourth is set")
        self.play(chips[3][0].animate.set_stroke(YELLOW), chips[3][1].animate.set_color(YELLOW), FadeIn(tag), run_time=0.6)
        # part B: the curve
        ax, curve, area, tail, mine, crit = make_plot(10, 4.2, [0.3, -0.7, 0])
        clab = T("how often chance gives each value", 24, GREY).move_to([3.6, 1.2, 0])
        xl = T("chi-square", 24, GREY).next_to(ax.c2p(12, 0), DOWN, buff=0.1).shift(LEFT * 0.8)
        d3 = T("3 df", 30, TEXT).move_to([-5.6, 2.9, 0])
        self.at("how big is too big")
        self.play(FadeOut(chips), FadeOut(tot), FadeOut(tag), ReplacementTransform(df, d3), run_time=0.7)
        self.play(Create(ax), run_time=0.6)
        self.at("A table shows")
        self.play(Create(curve), FadeIn(clab), FadeIn(xl), run_time=1.6)
        cl = T("critical value 7.81", 26, RED).move_to(ax.c2p(7.81, 0.14))
        cl.shift(RIGHT * 0.3)
        self.at("critical value")
        self.play(Create(crit), FadeIn(tail), FadeIn(cl), run_time=0.9)
        ml = T("1.78", 28, TEAL, weight=BOLD).move_to(ax.c2p(1.78, 0)).shift(DOWN * 0.35)
        self.at("Our")
        self.play(Create(mine), FadeIn(ml), run_time=0.8)
        pl = T("p about 0.62", 30, TEXT, weight=BOLD).move_to(ax.c2p(4.0, 0.045))
        self.at("The p value")
        self.play(FadeIn(area), FadeIn(pl), FadeOut(tail), run_time=1.0)
        self.finish()


# ---------------------------------------------------------------------------------------------
class S06Rule(SpokenScene):
    def construct(self):
        ax, curve, area, tail, mine, crit = make_plot(6.6, 4.4, [-3.2, -0.5, 0])
        pl = T("p = 0.62", 30, TEXT, weight=BOLD).move_to(ax.c2p(4.2, 0.05))
        ml = T("1.78", 26, TEAL, weight=BOLD).move_to(ax.c2p(1.78, 0)).shift(DOWN * 0.32)
        cond = chip("if 9:3:3:1 and every assumption hold", GREY, 26).move_to([-3.2, 2.9, 0])
        fit(cond, 6.6)
        self.at("A p value is")
        self.play(Create(ax), Create(curve), run_time=0.8)
        self.play(FadeIn(area), Create(mine), FadeIn(ml), run_time=0.8)
        self.at("if the hypothesis")
        self.play(FadeIn(cond, shift=DOWN * 0.1), run_time=0.7)
        pbig = M("p = 0.62", 54, GREEN, weight=BOLD).move_to([3.4, 2.4, 0])
        unr = T("unremarkable", 38, GREEN).move_to([3.4, 1.4, 0])
        self.at("A p of")
        self.play(FadeIn(pbig, shift=UP * 0.1), run_time=0.7)
        self.at("unremarkable")
        self.play(FadeIn(unr), run_time=0.6)
        c1 = chip("chance the hypothesis is true", TEXT, 26).move_to([3.7, 0.1, 0])
        self.at("not the probability")
        self.play(FadeIn(c1), run_time=0.5)
        x1 = cross(c1)
        self.play(Create(x1), run_time=0.5)
        c2 = chip("proof", TEXT, 32).move_to([3.7, -1.2, 0])
        self.at("does not prove")
        self.play(FadeIn(c2), run_time=0.5)
        x2 = cross(c2)
        self.play(Create(x2), run_time=0.5)
        c3 = chip("fail to reject", GREEN, 36).move_to([3.7, -2.5, 0])
        self.at("fail to reject")
        self.play(FadeIn(c3, scale=0.9), run_time=0.6)
        self.finish()


class S07End(EndCard):
    LINE = "A large p-value means no reason to reject, not proof."
