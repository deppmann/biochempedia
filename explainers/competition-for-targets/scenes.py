"""A small lead becomes a win  (Developmental Neuroscience, competition for targets)

COLOR MAP (one color per concept, whole video)
  BLUE   = a neuron whose fate is not yet decided
  GREEN  = a winner / a neuron that is protected or survives
  RED    = a loser / a neuron that dies or is pushed toward death
  YELLOW = nerve growth factor (NGF)
  PURPLE = the receptor TrkA (its level)
  ORANGE = the punishment signal (BDNF and NT-4)
  TEAL   = the receptor p75 and the p75-null mouse
  TEXT   = wild-type (white), plain labels
  GOLD   = the question mark and one highlight
  GREY   = target, axons, axes, structure
"""
import numpy as np
from bp_style import *  # noqa: F401,F403
from sim import sim

PURPLE = "#B58CD9"
ORANGE = "#F29E4C"


def P(x, y):
    return np.array([x, y, 0.0])


def soma(p, color=BLUE, r=0.27, op=0.9):
    return Circle(radius=r, stroke_color=color, stroke_width=3, fill_color=color, fill_opacity=op).move_to(p)


def to_state(d, color, op=0.9):
    return d.animate.set_stroke(color, opacity=1.0 if op > 0.3 else op + 0.3).set_fill(color, opacity=op)


def ngf_dot(p, r=0.1):
    return Circle(radius=r, stroke_color=YELLOW, stroke_width=1.5, fill_color=YELLOW, fill_opacity=1).move_to(p)


def arr(a, b, color=GREY, w=5, tip=0.22):
    return Arrow(a, b, buff=0.05, color=color, stroke_width=w, tip_length=tip,
                 max_tip_length_to_length_ratio=0.45, max_stroke_width_to_length_ratio=12)


def vbar(x, base, h, color=PURPLE, w=0.5):
    return Rectangle(width=w, height=max(h, 0.04), stroke_color=color, stroke_width=2, fill_color=color,
                     fill_opacity=0.85).move_to(P(x, base + max(h, 0.04) / 2))


def hbar(x0, y, w, color=PURPLE, h=0.4):
    return Rectangle(width=max(w, 0.04), height=h, stroke_color=color, stroke_width=2, fill_color=color,
                     fill_opacity=0.85).move_to(P(x0 + max(w, 0.04) / 2, y))


def axes_xy(x0, x1, y0, y1, xl, yl):
    ax = VGroup(Line(P(x0, y0), P(x1, y0), color=GREY, stroke_width=3),
                Line(P(x0, y0), P(x0, y1), color=GREY, stroke_width=3))
    xt = T(xl, 24, GREY).move_to(P((x0 + x1) / 2, y0 - 0.5))
    yt = T(yl, 24, GREY).rotate(PI / 2).move_to(P(x0 - 0.55, (y0 + y1) / 2))
    return VGroup(ax, xt, yt)


class S00Title(TitleCard):
    LESSON = "Competition: how a target picks its neurons"
    TITLE = "A small lead becomes a win"


# ---------------------------------------------------------------------------------------------
class S01Which(SpokenScene):
    def construct(self):
        ys = [2.45 - 0.7 * i for i in range(8)]
        bodies = VGroup(*[soma(P(-5.4, y)) for y in ys])
        TX, TL = -0.9, -1.7
        axons = VGroup(*[Line(P(-5.13, y), P(TL, y * 0.75), color=GREY, stroke_width=3) for y in ys])
        target = RoundedRectangle(corner_radius=0.2, width=1.6, height=5.4, stroke_color=GREY, stroke_width=3,
                                  fill_color=GREY, fill_opacity=0.12).move_to(P(TX, 0))
        tlabel = T("target", 26, GREY).move_to(P(TX, -3.15))
        dots = VGroup(*[ngf_dot(P(TX + dx, dy)) for dx, dy in [(-0.2, 0.5), (0.25, -0.1), (-0.1, -0.7)]])
        nchip = chip("NGF", YELLOW, 26).move_to(P(TX, 3.1))

        self.at("A target makes")
        self.play(FadeIn(target), FadeIn(tlabel), run_time=0.8)
        self.at("nerve growth factor")
        self.play(LaggedStart(*[FadeIn(d, scale=0.3) for d in dots], lag_ratio=0.25), FadeIn(nchip, shift=DOWN * 0.2), run_time=1.2)
        self.at("too little")
        self.play(Indicate(dots, color=YELLOW, scale_factor=1.3), run_time=1.0)
        self.at("every sympathetic neuron")
        self.play(LaggedStart(*[FadeIn(b, scale=0.4) for b in bodies], lag_ratio=0.08), run_time=1.0)
        self.play(LaggedStart(*[Create(a) for a in axons], lag_ratio=0.06), run_time=1.2)

        q = T("?", 160, GOLD, weight=BOLD).move_to(P(3.6, 0.0))
        self.at("which neurons get to live")
        self.play(FadeIn(q, scale=0.5), run_time=0.6)

        # even share
        ticks = VGroup(*[ngf_dot(P(-4.85, y + 0.0), 0.06) for y in ys])
        c1 = chip("shared evenly", YELLOW, 26).move_to(P(3.6, 2.4))
        self.at("Share it evenly")
        self.play(FadeOut(q), FadeIn(c1), FadeIn(ticks), run_time=0.7)
        t1 = T("all live, or all die", 28, TEXT).move_to(P(3.6, 1.35))
        self.at("or all die together")
        self.play(FadeIn(t1), *[to_state(b, GREEN) for b in bodies], run_time=0.5)
        self.play(*[to_state(b, RED, 0.5) for b in bodies], run_time=0.6)

        # first come, first served
        c2 = chip("first axon takes all", GREY, 26).move_to(P(3.6, 2.4))
        self.at("If the first axon")
        self.play(FadeOut(c1), FadeOut(t1), FadeOut(ticks), *[to_state(b, BLUE) for b in bodies], run_time=0.6)
        self.play(FadeIn(c2), run_time=0.4)
        mine = VGroup(*[ngf_dot(P(-4.85 + 0.2 * i, ys[0] + 0.0), 0.09) for i in range(3)])
        self.play(FadeOut(dots), to_state(bodies[0], GREEN), FadeIn(mine), run_time=0.8)
        one = ngf_dot(P(-4.85, ys[3]), 0.09)
        self.at("receiving some")
        self.play(FadeIn(one, scale=0.4), run_time=0.5)
        t2 = T("falls behind: how?", 28, GOLD).move_to(P(3.6, 1.35))
        self.at("fall behind")
        self.play(FadeIn(t2), to_state(bodies[3], BLUE, 0.35), run_time=0.9)

        self.at("Something else must")
        self.play(FadeOut(c2), FadeOut(t2), FadeOut(mine), FadeOut(one), *[to_state(b, BLUE) for b in bodies], run_time=0.6)
        q2 = T("?", 160, GOLD, weight=BOLD).move_to(P(3.6, 0.0))
        self.play(FadeIn(q2, scale=0.5), run_time=0.6)
        self.finish()


# ---------------------------------------------------------------------------------------------
class S02Feedback(SpokenScene):
    def construct(self):
        AY, BY = 1.5, -1.5
        A = soma(P(-5.3, AY), BLUE, 0.4)
        B = soma(P(-5.3, BY), BLUE, 0.4)
        TL = 4.7
        axA = Line(P(-4.9, AY), P(TL, AY * 0.6), color=GREY, stroke_width=3)
        axB = Line(P(-4.9, BY), P(TL, BY * 0.6), color=GREY, stroke_width=3)
        target = RoundedRectangle(corner_radius=0.2, width=1.4, height=4.8, stroke_color=GREY, stroke_width=3,
                                  fill_color=GREY, fill_opacity=0.12).move_to(P(5.4, 0))
        tl = T("target", 24, GREY).move_to(P(5.4, -2.9))
        tdots = VGroup(*[ngf_dot(P(5.4 + dx, dy)) for dx, dy in [(-0.25, 0.7), (0.2, 0.2), (-0.15, -0.3), (0.25, -0.8)]])
        tag = T("mouse sympathetic neurons", 24, GREY).move_to(P(-1.0, -3.2))

        self.at("In mouse sympathetic neurons")
        self.play(FadeIn(A), FadeIn(B), Create(axA), Create(axB), FadeIn(target), FadeIn(tl), FadeIn(tag), run_time=1.0)
        self.play(LaggedStart(*[FadeIn(d, scale=0.3) for d in tdots], lag_ratio=0.15), run_time=0.6)

        BX = -4.2
        AB, BB = P(BX, 2.15), P(BX, -0.85)
        lA = T("TrkA", 24, PURPLE).move_to(P(-4.95, 2.15))
        lB = T("TrkA", 24, PURPLE).move_to(P(-4.95, -0.85))
        bA = hbar(BX, 2.15, 1.5)
        bB = hbar(BX, -0.85, 1.5)
        self.at("its own receptor")
        self.play(FadeIn(lA), FadeIn(lB), GrowFromEdge(bA, LEFT), GrowFromEdge(bB, LEFT), run_time=0.9)

        wA = T("with NGF", 24, YELLOW).move_to(P(-5.3, 0.85))
        wB = T("no NGF", 24, GREY).move_to(P(-5.3, -2.3))

        def flow(dots_to, axon, n, y_end):
            ds = [tdots[i].copy() for i in range(n)]
            return ds

        d1, d2 = tdots[0].copy(), tdots[1].copy()
        self.at("rises")
        self.play(FadeIn(wA), d1.animate.move_to(P(-4.6, AY)).set_opacity(1), d2.animate.move_to(P(-4.45, AY)), Transform(bA, hbar(BX, 2.15, 3.2)), run_time=0.6)
        self.at("and without it")
        self.play(FadeIn(wB), run_time=0.5)
        self.at("falls")
        self.play(Transform(bB, hbar(BX, -0.85, 0.5)), run_time=0.7)

        # reset to a small difference
        self.at("So a neuron with a little more")
        self.play(FadeOut(wA), FadeOut(wB), FadeOut(d1), FadeOut(d2),
                  Transform(bA, hbar(BX, 2.15, 1.7)), Transform(bB, hbar(BX, -0.85, 1.4)), run_time=0.9)
        e1, e2, e3 = tdots[0].copy(), tdots[1].copy(), tdots[2].copy()
        self.at("collects more")
        self.play(e1.animate.move_to(P(-4.7, AY)), e2.animate.move_to(P(-4.55, AY)),
                  e3.animate.move_to(P(-4.7, BY)), run_time=1.4)

        c1 = chip("more TrkA", PURPLE, 24).move_to(P(-2.4, 0.15))
        c2 = chip("more NGF collected", YELLOW, 24).move_to(P(2.0, 0.15))
        a1 = arr(P(-1.1, 0.3), P(0.0, 0.3), GREY, 4, 0.18)
        a2 = arr(P(0.0, -0.05), P(-1.1, -0.05), GREY, 4, 0.18)
        self.at("makes still more")
        self.play(Transform(bA, hbar(BX, 2.15, 3.4)), Transform(bB, hbar(BX, -0.85, 1.3)),
                  FadeIn(c1), FadeIn(c2), GrowArrow(a1), GrowArrow(a2), run_time=1.2)
        self.at("pulls further ahead")
        self.play(Transform(bA, hbar(BX, 2.15, 5.6)), Transform(bB, hbar(BX, -0.85, 0.9)), run_time=1.3)
        self.at("positive feedback")
        self.play(Indicate(VGroup(c1, c2), color=GOLD, scale_factor=1.08), run_time=1.0)
        self.finish()


# ---------------------------------------------------------------------------------------------
class S03Stages(SpokenScene):
    def construct(self):
        X0, X1, Y0, Y1 = -5.4, 5.4, -2.4, 2.0
        axes = axes_xy(X0, X1, Y0, Y1, "time", "TrkA level")
        xs = sim(sd=0.01, T=2.6)
        n = xs.shape[1]
        steps = xs.shape[0]

        def curve(i):
            pts = [P(X0 + (X1 - X0) * k / (steps - 1), Y0 + xs[k, i] / 2.15 * (Y1 - Y0 - 0.2)) for k in range(0, steps, 2)]
            return VMobject(stroke_color=BLUE, stroke_width=4).set_points_smoothly(pts)

        curves = VGroup(*[curve(i) for i in range(n)])
        final = xs[-1]
        wins = [i for i in range(n) if final[i] > 1.0]
        loss = [i for i in range(n) if final[i] <= 1.0]
        hero = wins[0]
        supply = chip("fixed NGF supply", YELLOW, 24).move_to(P(0, 3.0))
        names = [("young", "naive", BLUE), ("sens", "sensitization", YELLOW), ("adv", "competitive advantage", PURPLE),
                 ("sel", "selection", GREEN)]
        grey_chips = VGroup(*[chip(t, GREY, 22, 0.16, 0.06) for _, t, _ in names]).arrange(RIGHT, buff=0.22)
        fit(grey_chips, 12.4)
        grey_chips.move_to(P(0, 3.0))

        self.at("In simulations with a fixed")
        sch = T("schematic, not data", 24, GOLD).move_to(P(3.9, -3.1))
        self.play(FadeIn(axes), FadeIn(supply), FadeIn(sch), run_time=0.9)
        self.at("feedback split the neurons")
        self.play(LaggedStart(*[Create(c, rate_func=linear) for c in curves], lag_ratio=0.0), run_time=1.9, rate_func=linear)
        self.at("winners and losers")
        self.play(*[curves[i].animate.set_stroke(GREEN, width=5) for i in wins],
                  *[curves[i].animate.set_stroke(RED, width=4) for i in loss], run_time=0.8)

        hc = curves[hero]
        dot = Dot(hc.point_from_proportion(0.0), radius=0.14, color=TEXT)

        def mv(a, b, rt):
            part = hc.copy().pointwise_become_partial(hc, a, b)
            return MoveAlongPath(dot, part, run_time=rt, rate_func=linear)

        def light(i):
            return Transform(grey_chips[i], chip(names[i][1], names[i][2], 22, 0.16).move_to(grey_chips[i]))

        self.at("A young neuron")
        self.play(FadeOut(supply), FadeIn(grey_chips), FadeIn(dot), run_time=0.6)
        self.play(light(0), mv(0.0, 0.05, 1.0), run_time=1.0)
        self.at("over a threshold")
        self.play(mv(0.05, 0.25, 1.2), run_time=1.2)
        self.at("sensitization")
        self.play(light(1), run_time=0.5)
        self.at("competitive advantage")
        self.play(light(2), mv(0.25, 0.55, 1.2), run_time=1.2)
        self.at("Winning the supply")
        self.play(light(3), mv(0.55, 1.0, 1.5), run_time=1.5)
        self.at("stayed behind lose")
        self.play(*[Indicate(curves[i], color=RED, scale_factor=1.0) for i in loss], run_time=1.0)
        self.finish()


# ---------------------------------------------------------------------------------------------
class S04Punish(SpokenScene):
    def construct(self):
        WX, LX, SY = -4.2, 3.6, 0.3
        W = soma(P(WX, SY), BLUE, 0.85, 0.5)
        L = soma(P(LX, SY), BLUE, 0.85, 0.5)
        bw = hbar(WX - 1.5, -1.3, 3.0)
        bl = hbar(LX - 0.4, -1.3, 0.8)
        tw = T("TrkA", 24, PURPLE).move_to(P(WX, -1.85))
        tL = T("TrkA", 24, PURPLE).move_to(P(LX, -1.85))
        sw = T("strongly supported", 24, GREY).move_to(P(WX, -2.6))
        sl = T("weakly supported", 24, GREY).move_to(P(LX, -2.6))

        self.at("Winners do more")
        self.play(FadeIn(W, scale=0.8), FadeIn(L, scale=0.8), run_time=0.8)
        self.play(GrowFromEdge(bw, LEFT), GrowFromEdge(bl, LEFT), FadeIn(tw), FadeIn(tL), run_time=1.0)
        self.at("Strongly supported neurons")
        self.play(FadeIn(sw), to_state(W, GREEN, 0.5), run_time=0.7)

        cb = chip("BDNF", ORANGE, 26).move_to(P(-1.5, 1.05))
        cn = chip("NT-4", ORANGE, 26).move_to(P(0.5, 1.05))
        self.at("make")
        self.play(FadeIn(cb, shift=RIGHT * 0.6), FadeIn(cn, shift=RIGHT * 0.6), run_time=0.9)

        rec = RoundedRectangle(corner_radius=0.06, width=0.2, height=0.7, stroke_color=TEAL, stroke_width=3,
                               fill_color=TEAL, fill_opacity=0.9).move_to(P(LX - 0.85, SY))
        rl = T("p75", 26, TEAL).move_to(P(LX - 1.5, SY + 1.15))
        arrow = arr(P(-3.15, SY), P(LX - 1.0, SY), ORANGE, 6, 0.28)
        self.at("These act through")
        self.play(FadeIn(rec), FadeIn(rl), run_time=0.5)
        self.play(GrowArrow(arrow), run_time=0.8)
        self.at("weakly supported neighbors")
        self.play(FadeIn(sl), run_time=0.5)
        self.at("can promote death")
        self.play(Indicate(rec, color=TEAL, scale_factor=1.5), to_state(L, RED, 0.3), run_time=1.1)

        self.at("is protected")
        pw = T("protected", 24, GREEN).move_to(P(WX, -2.6))
        ring = Circle(radius=1.05, stroke_color=GREEN, stroke_width=6).move_to(P(WX, SY))
        self.play(Transform(sw, pw), Create(ring), to_state(W, GREEN, 0.7), run_time=0.9)
        self.at("and a neuron poor")
        self.play(Indicate(bl, color=PURPLE, scale_factor=1.2), run_time=0.8)
        self.at("is not")
        pl = T("not protected", 24, RED).move_to(P(LX, -2.6))
        self.play(Transform(sl, pl), to_state(L, RED, 0.45), run_time=0.9)
        self.finish()


# ---------------------------------------------------------------------------------------------
class S05Faster(SpokenScene):
    def construct(self):
        X0, X1, Y0, Y1 = -5.2, 5.0, -2.5, 2.2
        f = 0.4

        def N(t, tau):
            return f + (1 - f) * np.exp(-t / tau)

        def curve(tau, color):
            ts = np.linspace(0, 2.0, 90)
            pts = [P(X0 + (X1 - X0) * t / 2.0, Y0 + 0.35 + N(t, tau) * (Y1 - Y0 - 0.5)) for t in ts]
            return VMobject(stroke_color=color, stroke_width=5).set_points_smoothly(pts), \
                (lambda t: P(X0 + (X1 - X0) * t / 2.0, Y0 + 0.35 + N(t, tau) * (Y1 - Y0 - 0.5)))

        cw, fw = curve(0.18, TEXT)
        cn, fn = curve(0.5, TEAL)
        axes = axes_xy(X0, X1, Y0, Y1, "age", "neurons")
        tag = T("simulation", 26, GREY).move_to(P(-3.0, 2.95))
        lw = T("with punishment", 24, TEXT).move_to(fw(0.3) + P(1.7, -1.0))
        ln = T("without punishment", 24, TEAL).move_to(fn(0.55) + P(1.6, 0.75))

        self.at("Does punishment matter")
        sch = T("schematic, not data", 24, GOLD).move_to(P(3.4, 2.95))
        self.play(FadeIn(axes), FadeIn(sch), run_time=0.9)
        self.at("In simulations")
        self.play(FadeIn(tag), Create(cw, rate_func=linear), run_time=1.3)
        self.at("made the split faster")
        self.play(FadeIn(lw), Indicate(cw, color=TEXT, scale_factor=1.0), run_time=1.2)
        self.at("weak neurons lingered")
        self.play(Create(cn, rate_func=linear), FadeIn(ln), run_time=1.8)

        tag2 = T("mouse", 26, GREY).move_to(tag)
        lw2 = T("wild-type", 24, TEXT).move_to(lw)
        ln2 = T("p75-null", 24, TEAL).move_to(ln)
        self.at("In mice lacking")
        self.play(Transform(tag, tag2), Transform(lw, lw2), Transform(ln, ln2), run_time=0.9)
        self.at("delayed but not prevented")
        lvl = 0.55
        t_w = -0.18 * np.log((lvl - f) / (1 - f))
        t_n = -0.5 * np.log((lvl - f) / (1 - f))
        a_ = arr(fw(t_w) + P(0.05, 0.0), fn(t_n) + P(-0.05, 0.0), GOLD, 5, 0.2)
        a_ = Line(fw(t_w) + P(0.05, 0), fn(t_n) + P(-0.05, 0), color=GOLD, stroke_width=5)
        a_ = DoubleArrow(fw(t_w), fn(t_n), buff=0.05, color=GOLD, stroke_width=5, tip_length=0.2)
        dl = T("delayed, not prevented", 26, TEXT).move_to(P(2.9, 1.3))
        self.play(GrowFromCenter(a_), FadeIn(dl), run_time=1.0)
        self.at("similar level")
        dash = DashedLine(fw(2.0) + P(-3.0, 0), fw(2.0), color=GREY, stroke_width=3)
        sim_l = T("similar final level", 24, GREY).move_to(fw(2.0) + P(-1.4, 0.75))
        self.play(Create(dash), FadeIn(sim_l), run_time=0.9)
        self.at("The losers still die")
        ld = T("losers still die: too little NGF", 26, RED).move_to(P(1.2, -1.5))
        self.play(FadeIn(ld), run_time=0.8)
        self.finish()


# ---------------------------------------------------------------------------------------------
class S06Rule(SpokenScene):
    def construct(self):
        xs = [-4.5 + 1.8 * i for i in range(6)]
        SY, BASE = 1.0, -2.4
        wins = [1, 4]
        h0 = [0.95, 1.15, 0.9, 1.0, 1.12, 0.92]
        bodies = VGroup(*[soma(P(x, SY), BLUE, 0.4, 0.8) for x in xs])
        bars = [vbar(x, BASE, h) for x, h in zip(xs, h0)]
        lab = T("TrkA level", 24, PURPLE).move_to(P(0, -3.05))

        self.at("So a limited supply")
        self.play(LaggedStart(*[FadeIn(b, scale=0.5) for b in bodies], lag_ratio=0.08),
                  *[GrowFromEdge(b, DOWN) for b in bars], FadeIn(lab), run_time=1.4)
        self.at("pick the winners alone")
        self.play(Indicate(bodies, color=BLUE, scale_factor=1.15), run_time=1.2)
        self.at("A small early lead")
        self.play(*[Indicate(bars[i], color=GOLD, scale_factor=1.15) for i in wins], run_time=1.0)
        self.at("the lead grows")
        self.play(*[Transform(bars[i], vbar(xs[i], BASE, 2.7)) for i in wins],
                  *[Transform(bars[i], vbar(xs[i], BASE, 0.7)) for i in range(6) if i not in wins],
                  *[to_state(bodies[i], GREEN, 0.9) for i in wins], run_time=1.6)
        arrows = []
        for w in wins:
            for d in (-1, 1):
                arrows.append(arr(P(xs[w] + d * 0.5, SY), P(xs[w] + d * 1.3, SY), ORANGE, 6, 0.22))
        self.at("Winners punish")
        self.play(LaggedStart(*[GrowArrow(a) for a in arrows], lag_ratio=0.15), run_time=1.0)
        self.at("the split comes faster")
        self.play(*[to_state(bodies[i], RED, 0.35) for i in range(6) if i not in wins],
                  *[Transform(bars[i], vbar(xs[i], BASE, 0.2)) for i in range(6) if i not in wins], run_time=1.0)
        tag = T("one cell type, one species: the mouse sympathetic neuron", 26, TEXT).move_to(P(0, 2.7))
        self.at("one cell type")
        self.play(FadeIn(tag), run_time=0.8)
        self.at("Remember the rule")
        self.play(Indicate(VGroup(*bars), color=GOLD, scale_factor=1.04), run_time=1.2)
        self.finish()


class S07End(EndCard):
    LINE = "Feedback turns a small lead into survival; punishment makes it faster."
