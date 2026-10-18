"""Conservation and Restoration: a safe size is a chance  (Biochemistrypedia explainer)

COLOR MAP (one color per concept, whole video)
  TEXT   = an individual animal, sex not stated
  BLUE   = a male
  ORANGE = a female
  YELLOW = chance / probability (dice, percentages)
  RED    = extinct run / fails the target
  GREEN  = meets the target
  PURPLE = effective size Ne
  GREY   = outlines, tracks, de-emphasized
"""
import numpy as np
from bp_style import *  # noqa: F401,F403

ORANGE = "#F29E4C"
PURPLE = "#B58CD9"


def dot(r=0.2, color=TEXT, letter=None, fill=0.9):
    c = Circle(radius=r, stroke_color=color, stroke_width=3, fill_color=color, fill_opacity=fill)
    if letter:
        return VGroup(c, T(letter, int(r * 56), BG, weight=BOLD).move_to(c))
    return VGroup(c)


def dice(side=1.8, color=YELLOW):
    sq = RoundedRectangle(corner_radius=0.2, width=side, height=side, stroke_color=color, stroke_width=5,
                          fill_color=color, fill_opacity=0.18)
    o = side * 0.24
    pips = VGroup(*[Circle(radius=side * 0.075, stroke_width=0, fill_color=color, fill_opacity=1).move_to(sq.get_center() + np.array([dx * o, dy * o, 0]))
                    for dx, dy in [(-1, 1), (1, 1), (0, 0), (-1, -1), (1, -1)]])
    return VGroup(sq, pips)


def arena(w, h, center):
    return RoundedRectangle(corner_radius=0.25, width=w, height=h, stroke_color=GREY, stroke_width=3,
                            fill_color=GREY, fill_opacity=0.08).move_to([center[0], center[1], 0])


def scatter(n, w, h, center, r, color=TEXT, seed=1, min_d=0.0):
    rng = np.random.default_rng(seed)
    pts = []
    tries = 0
    while len(pts) < n and tries < 20000:
        tries += 1
        p = np.array([rng.uniform(-w / 2 + r + 0.1, w / 2 - r - 0.1), rng.uniform(-h / 2 + r + 0.1, h / 2 - r - 0.1)])
        if all(np.linalg.norm(p - q) >= max(min_d, 2.3 * r) for q in pts):
            pts.append(p)
    return VGroup(*[dot(r, color).move_to([center[0] + p[0], center[1] + p[1], 0]) for p in pts])


class S00Title(TitleCard):
    LESSON = "Conservation and restoration"
    TITLE = "A safe size is a chance"


# ---------------------------------------------------------------------------------------------
class S01Question(SpokenScene):
    def construct(self):
        ar = arena(5.4, 5.0, [-3.4, -0.1])
        pop = scatter(14, 5.4, 5.0, [-3.4, -0.1], 0.2, seed=4, min_d=0.8)
        q = T("?", 190, GREY, font=TITLE_FONT).move_to([3.4, 0.5, 0])
        ql = T("how many animals?", 34).move_to([3.4, -1.7, 0])
        self.at("How many animals", lead=0.0)
        self.play(FadeIn(ar), LaggedStart(*[GrowFromCenter(d) for d in pop], lag_ratio=0.06), run_time=1.6)
        self.play(FadeIn(q, scale=0.8), FadeIn(ql), run_time=0.6)
        who = T("Mark Shaffer, 1981", 26, GREY).move_to([3.4, 2.9, 0])
        self.at("Mark Schaeffer")
        self.play(FadeIn(who), run_time=0.5)
        self.at("changing the question")
        self.play(FadeOut(q), FadeOut(ql), run_time=0.5)
        safe = chip("safe", GREY, size=36).move_to([3.4, 1.2, 0])
        doom = chip("doomed", GREY, size=36).move_to([3.4, -1.0, 0])
        self.at("never simply safe")
        self.play(FadeIn(safe, shift=UP * 0.2), FadeIn(doom, shift=UP * 0.2), run_time=0.6)
        self.at("or doomed")
        x1 = VGroup(Line(safe.get_corner(UL), safe.get_corner(DR), color=RED, stroke_width=7),
                    Line(safe.get_corner(DL), safe.get_corner(UR), color=RED, stroke_width=7))
        x2 = VGroup(Line(doom.get_corner(UL), doom.get_corner(DR), color=RED, stroke_width=7),
                    Line(doom.get_corner(DL), doom.get_corner(UR), color=RED, stroke_width=7))
        self.play(Create(x1), Create(x2), run_time=0.6)
        self.at("Chance acts on it")
        d = dice(2.2).move_to([3.4, 0.4, 0])
        dl = T("chance", 36, YELLOW).move_to([3.4, -1.3, 0])
        self.play(FadeOut(safe), FadeOut(doom), FadeOut(x1), FadeOut(x2), FadeOut(who), run_time=0.4)
        self.play(FadeIn(d, scale=0.7), FadeIn(dl), run_time=0.5)
        self.play(Rotate(d, angle=PI / 2, run_time=0.8))
        self.at("small populations")
        gone = VGroup(*pop[5:])
        self.play(FadeOut(gone), Rotate(d, angle=-PI / 2, run_time=1.0), run_time=1.0)
        self.finish()


# ---------------------------------------------------------------------------------------------
class S02Luck(SpokenScene):
    def construct(self):
        self.at("Take an illustration", lead=0.0)
        fem = dot(0.55, ORANGE, "F").move_to([-5.2, 1.5, 0])
        fl = T("last breeding female", 24, ORANGE).next_to(fem, DOWN, buff=0.25)
        fl.shift(RIGHT * 0.5)
        self.play(GrowFromCenter(fem), FadeIn(fl), run_time=0.7)
        xs = [-2.6 + i * 1.7 for i in range(5)]
        young = VGroup(*[Circle(radius=0.5, stroke_color=GREY, stroke_width=3, fill_color=GREY, fill_opacity=0.15).move_to([x, 1.5, 0]) for x in xs])
        qs = VGroup(*[T("?", 36, GREY).move_to(c) for c in young])
        yl = T("five young", 26, GREY).move_to([1.6, 2.6, 0])
        self.at("five young")
        self.play(LaggedStart(*[GrowFromCenter(VGroup(c, q)) for c, q in zip(young, qs)], lag_ratio=0.12), FadeIn(yl), run_time=1.0)
        self.at("all five are male")
        males = VGroup(*[dot(0.5, BLUE, "M").move_to(c) for c in young])
        self.play(LaggedStart(*[ReplacementTransform(VGroup(c, q), m) for c, q, m in zip(young, qs, males)], lag_ratio=0.15), run_time=1.2)
        eq = M("1/2 × 1/2 × 1/2 × 1/2 × 1/2", 36, YELLOW).move_to([0.5, -0.5, 0])
        self.at("one half to the fifth power")
        self.play(Write(eq), run_time=1.4)
        res = M("= 1/32  ≈  3%", 52, YELLOW, weight=BOLD).move_to([0.5, -1.9, 0])
        self.at("one in 32")
        self.play(FadeIn(res, shift=UP * 0.2), run_time=0.6)
        self.at("In a population of thousands")
        self.play(*[FadeOut(m) for m in (fem, fl, yl, males, eq, res)], run_time=0.6)
        a1 = arena(5.6, 4.4, [-3.3, 0.3])
        a2 = arena(5.6, 4.4, [3.3, 0.3])
        big = scatter(150, 5.6, 4.4, [-3.3, 0.3], 0.07, seed=5)
        ten = scatter(10, 5.6, 4.4, [3.3, 0.3], 0.2, seed=6, min_d=1.0)
        l1 = T("thousands", 32).move_to([-3.3, 2.9, 0])
        l2 = T("ten", 32).move_to([3.3, 2.9, 0])
        self.play(FadeIn(a1), FadeIn(a2), FadeIn(big), FadeIn(ten), FadeIn(l1), FadeIn(l2), run_time=0.8)
        t1 = T("luck averages out", 30, YELLOW).move_to([-3.3, -2.5, 0])
        t2 = T("luck decides the outcome", 30, YELLOW).move_to([3.3, -2.5, 0])
        self.at("averages out")
        self.play(FadeIn(t1, shift=UP * 0.15), run_time=0.5)
        self.at("decides the outcome")
        self.play(FadeIn(t2, shift=UP * 0.15), run_time=0.5)
        self.finish()


# ---------------------------------------------------------------------------------------------
class S03Standard(SpokenScene):
    def construct(self):
        mvp = chip("minimum viable population", TEXT, size=32).move_to([0, -3.0, 0])
        self.at("defined a minimum viable population", lead=0.0)
        self.play(FadeIn(mvp, shift=UP * 0.2), run_time=0.7)

        rows = {}

        def slider(name, y, color, knob_x):
            lab = T(name, 30, color).move_to([0, y, 0]).align_to([-6.2, 0, 0], LEFT)
            track = Line([-1.4, y, 0], [2.8, y, 0], color=GREY, stroke_width=6)
            knob = Circle(radius=0.22, stroke_color=color, stroke_width=4, fill_color=color, fill_opacity=0.9).move_to([knob_x, y, 0])
            return lab, track, knob

        # habitat: a chip, not a slider
        hab = chip("a given habitat", GREY, size=30).move_to([2.2, 1.9, 0])
        habl = T("habitat", 30, GREY).move_to([0, 1.9, 0]).align_to([-6.2, 0, 0], LEFT)
        self.at("in a given habitat")
        self.play(FadeIn(habl), FadeIn(hab, shift=LEFT * 0.2), run_time=0.6)

        c_lab, c_tr, c_kn = slider("chance of persisting", 0.5, YELLOW, 0.0)
        c_val = M("chosen", 28, YELLOW).move_to([4.7, 0.5, 0])
        self.at("chosen chance")
        self.play(FadeIn(c_lab), Create(c_tr), GrowFromCenter(c_kn), FadeIn(c_val), run_time=0.7)

        t_lab, t_tr, t_kn = slider("time", -0.9, GREY, -0.2)
        t_lab.set_color(TEXT)
        t_kn.set_stroke(TEXT).set_fill(TEXT, 0.9)
        t_val = M("chosen", 28, TEXT).move_to([4.7, -0.9, 0])
        self.at("for a chosen time")
        self.play(FadeIn(t_lab), Create(t_tr), GrowFromCenter(t_kn), FadeIn(t_val), run_time=0.7)

        tent = T("a tentative example", 24, GREY).move_to([4.6, 1.15, 0])
        self.at("tentative example")
        self.play(FadeIn(tent), run_time=0.4)
        self.at("a 99")
        c_val2 = M("99%", 32, YELLOW, weight=BOLD).move_to(c_val)
        self.play(c_kn.animate.move_to([2.5, 0.5, 0]), Transform(c_val, c_val2), run_time=0.8)
        self.at("lasting")
        t_val2 = M("1,000 years", 28, TEXT, weight=BOLD).move_to([4.5, -0.9, 0])
        self.play(t_kn.animate.move_to([2.5, -0.9, 0]), Transform(t_val, t_val2), run_time=0.8)

        # the answer box
        ans = T("size = ?", 32, TEXT).move_to([4.4, -3.0, 0])
        arrow = Arrow([mvp.get_right()[0] + 0.1, -3.0, 0], [ans.get_left()[0] - 0.1, -3.0, 0], color=GREY, buff=0, stroke_width=5)
        self.play(FadeIn(arrow), FadeIn(ans), run_time=0.4)
        self.at("Change the chance")
        self.play(Indicate(c_kn, color=YELLOW, scale_factor=1.6), Indicate(ans, color=YELLOW), run_time=0.9)
        self.at("or the habitat")
        self.play(Indicate(hab, color=YELLOW, scale_factor=1.15), Indicate(t_kn, color=YELLOW, scale_factor=1.6), run_time=0.9)
        self.at("the answer changes")
        self.play(Indicate(ans, color=YELLOW, scale_factor=1.3), run_time=0.8)
        self.finish()


# ---------------------------------------------------------------------------------------------
GX, GY, CELL = -2.5, 0.0, 0.19


def run_grid():
    cells = VGroup()
    for i in range(1000):
        r, c = divmod(i, 40)
        x = GX - 20 * CELL + (c + 0.5) * CELL
        y = GY + 12.5 * CELL - (r + 0.5) * CELL
        cells.add(Square(side_length=CELL * 0.82, stroke_width=0, fill_color=GREY, fill_opacity=0.45).move_to([x, y, 0]))
    return cells


class S04Runs(SpokenScene):
    def construct(self):
        frame = SurroundingRectangle(Rectangle(width=40 * CELL, height=25 * CELL).move_to([GX, GY, 0]), buff=0.12,
                                     color=GREY, stroke_width=3)
        title = T("one population, run again and again", 28, GREY).move_to([GX, 2.9, 0])
        self.play(Create(frame), FadeIn(title), run_time=0.8)
        cells = run_grid()
        self.at("run it many times")
        self.play(LaggedStart(*[FadeIn(c) for c in cells], lag_ratio=0.0015), run_time=2.2)
        tag = T("invented numbers", 24, GREY).move_to([4.4, 2.9, 0])
        self.at("invented example")
        self.play(FadeIn(tag), run_time=0.4)
        start = VGroup(*[dot(0.1, TEXT).move_to([3.2 + (i % 10) * 0.32, 1.7 - (i // 10) * 0.32, 0]) for i in range(20)])
        sl = T("starts with 20", 26, TEXT).move_to([4.4, 2.2, 0])
        self.at("starts with 20")
        self.play(FadeIn(sl), LaggedStart(*[GrowFromCenter(d) for d in start], lag_ratio=0.04), run_time=0.9)
        runs = T("1,000 runs", 28, TEXT).move_to([4.4, 0.6, 0])
        self.at("The model runs")
        self.play(FadeIn(runs), Indicate(cells, color=TEXT, scale_factor=1.0), run_time=0.8)
        yrs = T("100 years each", 28, TEXT).move_to([4.4, -0.1, 0])
        self.at("over 100 years")
        self.play(FadeIn(yrs), run_time=0.5)
        rng = np.random.default_rng(11)
        idx = sorted(rng.choice(1000, 120, replace=False))
        ext = T("120 reach zero", 30, RED, weight=BOLD).move_to([4.4, -1.1, 0])
        self.at("In 120 runs")
        self.play(LaggedStart(*[cells[i].animate.set_fill(RED, 1.0) for i in idx], lag_ratio=0.02), FadeIn(ext), run_time=1.6)
        frac = M("120 / 1,000 = 12.0%", 28, YELLOW, weight=BOLD).move_to([4.4, -2.1, 0])
        self.at("That is 12")
        self.play(FadeIn(frac, shift=UP * 0.15), run_time=0.6)
        self.finish()


# ---------------------------------------------------------------------------------------------
BX0, BY0, BS = [-4.4, 0.0, 2.2], -1.5, 0.34   # bar centers x, baseline y, units per percent


def bar(i, pct, color):
    h = pct * BS
    return Rectangle(width=1.5, height=h, stroke_color=color, stroke_width=3, fill_color=color, fill_opacity=0.5).move_to([BX0[i] + 0.0, BY0 + h / 2, 0])


class S05Target(SpokenScene):
    def construct(self):
        xs = [-3.8, -1.2, 1.4]
        ax = Line([-5.3, BY0, 0], [2.8, BY0, 0], color=GREY, stroke_width=4)
        ay = Line([-5.3, BY0, 0], [-5.3, BY0 + 13 * BS, 0], color=GREY, stroke_width=4)
        ticks = VGroup(*[VGroup(Line([-5.4, BY0 + v * BS, 0], [-5.2, BY0 + v * BS, 0], color=GREY, stroke_width=3),
                                M(f"{v}", 22, GREY).move_to([-5.75, BY0 + v * BS, 0])) for v in (0, 5, 10)])
        ytitle = T("extinction probability in 100 years (%)", 22, GREY).rotate(PI / 2).move_to([-6.3, BY0 + 2.2, 0])
        tag = T("invented numbers, 1,000 runs per size", 22, GREY).move_to([-1.3, 3.55, 0])
        self.add(ax, ay, ticks, ytitle, tag)

        def mkbar(x, pct, color):
            h = pct * BS
            return Rectangle(width=1.5, height=h, stroke_color=color, stroke_width=3, fill_color=color, fill_opacity=0.5).move_to([x, BY0 + h / 2, 0])

        xl = [T(s, 28).move_to([x, BY0 - 0.4, 0]) for x, s in zip(xs, ["20", "50", "100"])]
        xt = T("starting size", 22, GREY).move_to([-1.3, BY0 - 0.9, 0])
        b0 = mkbar(xs[0], 12.0, YELLOW)
        v0 = M("12.0%", 24, YELLOW).next_to(b0, UP, buff=0.12)
        self.add(b0, v0, xl[0], xt)
        self.at("start from 50", lead=0.0)
        b1 = mkbar(xs[1], 3.7, YELLOW)
        v1 = M("3.7%", 24, YELLOW).next_to(b1, UP, buff=0.12)
        self.play(FadeIn(xl[1]), GrowFromEdge(b1, DOWN), run_time=0.7)
        self.play(FadeIn(v1), run_time=0.3)
        b2 = mkbar(xs[2], 0.8, YELLOW)
        v2 = M("0.8%", 24, YELLOW).next_to(b2, UP, buff=0.12)
        self.at("then from 100")
        self.play(FadeIn(xl[2]), GrowFromEdge(b2, DOWN), run_time=0.7)
        self.play(FadeIn(v2), run_time=0.3)
        self.at("Fewer runs")
        self.play(Indicate(VGroup(v0, v1, v2), color=YELLOW, scale_factor=1.1), run_time=0.7)
        ty = BY0 + 5 * BS
        tline = DashedLine([-5.3, ty, 0], [2.8, ty, 0], color=TEXT, stroke_width=4)
        tlab = T("target: at most 5%", 26, TEXT).move_to([4.6, ty, 0])
        tlab2 = T("in 100 years", 24, GREY).next_to(tlab, DOWN, buff=0.12)
        self.at("target of at most")
        self.play(Create(tline), FadeIn(tlab), FadeIn(tlab2), run_time=0.9)
        f20 = T("fails", 28, RED, weight=BOLD).move_to([4.6, 1.8, 0])
        self.at("20 fails")
        self.play(b0.animate.set_stroke(RED).set_fill(RED, 0.5), v0.animate.set_color(RED), FadeIn(f20), run_time=0.6)
        p50 = T("passes", 28, GREEN, weight=BOLD).move_to([4.6, 1.15, 0])
        self.at("50 passes")
        self.play(b1.animate.set_stroke(GREEN).set_fill(GREEN, 0.5), v1.animate.set_color(GREEN), FadeIn(p50), run_time=0.6)
        self.at("smallest tested size")
        self.play(Indicate(b1, color=GREEN, scale_factor=1.12), run_time=0.8)
        br = Brace(Line([xs[0], BY0 - 1.15, 0], [xs[1], BY0 - 1.15, 0]), direction=DOWN, color=GREY)
        un = T("never run", 26, GREY).next_to(br, DOWN, buff=0.1)
        self.at("were never run")
        self.play(GrowFromCenter(br), FadeIn(un), run_time=0.7)
        self.at("anywhere in that range")
        self.play(Indicate(un, color=YELLOW, scale_factor=1.15), run_time=0.8)
        self.finish()


# ---------------------------------------------------------------------------------------------
class S06Effective(SpokenScene):
    def construct(self):
        # 50 breeding adults: 10 males, 40 females
        dots = VGroup()
        for i in range(50):
            r, c = divmod(i, 10)
            col = BLUE if i < 10 else ORANGE
            dots.add(dot(0.22, col).move_to([-5.8 + c * 0.7, 3.0 - r * 0.6, 0]))
        census = Rectangle(width=7.0, height=0.6, stroke_color=TEXT, stroke_width=3, fill_color=TEXT, fill_opacity=0.25)
        census.move_to([-6.2 + 3.5, -0.6, 0])
        cl = T("census: 50 breeding adults", 28, TEXT).next_to(census, UP, buff=0.12).align_to(census, LEFT)
        eff = Rectangle(width=4.48, height=0.6, stroke_color=PURPLE, stroke_width=3, fill_color=PURPLE, fill_opacity=0.45)
        eff.move_to([-6.2 + 2.24, -2.0, 0])
        el = T("effective size", 28, PURPLE).next_to(eff, DOWN, buff=0.12).align_to(eff, LEFT)
        leg_m = T("10 males", 26, BLUE).move_to([4.3, 3.0, 0])
        leg_f = T("40 females", 26, ORANGE).move_to([4.3, 2.4, 0])
        self.play(FadeIn(dots, lag_ratio=0.03), run_time=1.2)
        self.at("usually smaller than the count")
        self.play(FadeIn(census), FadeIn(cl), run_time=0.6)
        self.at("50 adults breed")
        self.play(FadeIn(leg_m), FadeIn(leg_f), run_time=0.5)
        f1 = M("4 × 10 × 40", 34, YELLOW).move_to([4.3, 1.5, 0])
        f2 = Line([2.6, 1.05, 0], [6.0, 1.05, 0], color=YELLOW, stroke_width=4)
        f3 = M("10 + 40", 34, YELLOW).move_to([4.3, 0.6, 0])
        self.at("4 x 10 x 40")
        self.play(FadeIn(f1), run_time=0.5)
        self.play(Create(f2), FadeIn(f3), run_time=0.4)
        f4 = M("Ne = 32", 48, PURPLE, weight=BOLD).move_to([4.3, -0.9, 0])
        self.at("gives 32")
        self.play(FadeIn(f4, scale=1.2), GrowFromEdge(eff, LEFT), FadeIn(el), run_time=0.8)
        self.at("A target of 100")
        self.play(*[FadeOut(m) for m in (dots, census, cl, eff, el, leg_m, leg_f, f1, f2, f3, f4)], run_time=0.6)
        s = 0.045
        cb = Rectangle(width=160 * s, height=0.8, stroke_color=TEXT, stroke_width=3, fill_color=TEXT, fill_opacity=0.25)
        cb.move_to([-6.0 + 160 * s / 2, -0.9, 0])
        eb = Rectangle(width=100 * s, height=0.8, stroke_color=PURPLE, stroke_width=3, fill_color=PURPLE, fill_opacity=0.45)
        eb.move_to([cb.get_left()[0] + 100 * s / 2, 1.5, 0])
        tl = T("target: effective size of 100", 30, PURPLE).next_to(eb, UP, buff=0.15).align_to(eb, LEFT)
        cl2 = T("about 160 adults, at that sex ratio", 30, TEXT).next_to(cb, UP, buff=0.15).align_to(cb, LEFT)
        self.play(GrowFromEdge(eb, LEFT), FadeIn(tl), run_time=0.8)
        self.at("about 160 adults")
        self.play(GrowFromEdge(cb, LEFT), FadeIn(cl2), run_time=0.9)
        self.at("Keep this rule")
        self.play(*[FadeOut(m) for m in (cb, eb, tl, cl2)], run_time=0.6)
        r1 = T("a safe size is a chance over a time", 44, YELLOW, font=TITLE_FONT).move_to([0, 0.8, 0])
        r2 = T("genetic guidelines count effective size, not heads", 36, PURPLE, font=TITLE_FONT).move_to([0, -0.8, 0])
        fit(r1, max_w=11.8)
        fit(r2, max_w=11.8)
        self.play(FadeIn(r1, shift=UP * 0.15), run_time=0.7)
        self.at("effective size, not heads")
        self.play(FadeIn(r2, shift=UP * 0.15), run_time=0.7)
        self.finish()


class S07End(EndCard):
    LINE = "A safe size is a stated chance over a stated time."
