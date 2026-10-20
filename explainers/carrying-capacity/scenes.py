"""Carrying capacity moves with conditions  (Biochemistrypedia explainer, high school Biology)

Timed to the SPOKEN words: every self.at("...") cue waits for that phrase in audio/words.json.

COLOR MAP (one color per concept, whole video)
  BLUE   = the population: crab tokens, crab-count bars, the population curve
  GREEN  = biotic factors, and things that RAISE carrying capacity
  ORANGE = abiotic factors
  RED    = limits and things that LOWER carrying capacity
  GOLD   = carrying capacity (dashed line) and the film's question
  TEAL   = the winter survey (site marks, dredge)
  PURPLE = what people do (crabbing)
  GREY   = outlines, axes, labels
Crab tokens are an illustration, not counts. The J bars use the lesson's own bacteria numbers
(10, 20, 40, 80, 160, 320 per 30-minute step). The S curve and the moving carrying capacity are a
MODEL SKETCH in made-up units (logistic curve computed here), labelled as such, never a measurement.
The survey bars in the first scene are not to scale and carry no counts.
"""
import numpy as np
from bp_style import *  # noqa: F401,F403

ORANGE = "#F29E4C"
PURPLE = "#B58CD9"
CTEAL = "#3FB8C0"
GOLDC = "#F2C94C"


def crab(s=1.0):
    body = RoundedRectangle(corner_radius=0.08, width=0.36, height=0.26, stroke_color=BLUE, stroke_width=2.5,
                            fill_color=BLUE, fill_opacity=0.35)
    return VGroup(body).scale(s)


def arrow_to(a, b, color, w=6):
    return Arrow(a, b, color=color, stroke_width=w, buff=0.0, max_tip_length_to_length_ratio=0.3)


# ---- the model sketch (made-up units) --------------------------------------------------------
K0 = 8.0


def logistic(t):
    return K0 / (1 + np.exp(-1.1 * (t - 4.0)))


def wob(t):
    return 0.3 * np.clip((t - 6.0) / 3.0, 0, 1) * np.sin(2.4 * t)


def f_pop(t):
    return logistic(t) + wob(t)


def smooth(x):
    x = np.clip(x, 0, 1)
    return x * x * (3 - 2 * x)


def K_of_t(t):
    t = np.asarray(t, dtype=float)
    return K0 + (9.2 - K0) * smooth((t - 7.0) / 1.4) + (5.6 - 9.2) * smooth((t - 10.0) / 1.8)


def make_axes():
    ax = Axes(x_range=[0, 13, 1], y_range=[0, 10, 1], x_length=8.4, y_length=4.9,
              axis_config={"include_ticks": False, "include_numbers": False, "color": GREY, "stroke_width": 3,
                           "tip_width": 0.2, "tip_height": 0.2}, tips=True)
    ax.move_to([2.4, -0.45, 0])
    xl = T("time", 24, GREY).next_to(ax.x_axis, DOWN, buff=0.12).align_to(ax.x_axis, RIGHT)
    yl = T("population size", 24, GREY).next_to(ax.y_axis, UP, buff=0.12).align_to(ax.y_axis, LEFT)
    nt = T("model sketch, made-up units", 22, GREY).next_to(ax, DOWN, buff=0.45)
    nt.move_to([ax.get_center()[0], nt.get_center()[1], 0])
    return ax, VGroup(xl, yl), nt


def curve(ax, f, a, b, color=BLUE, w=6):
    return ax.plot(lambda t: float(f(t)), x_range=[a, b, 0.05], color=color, stroke_width=w, use_smoothing=False)


def poly(ax, ts, ys, color, w=6):
    m = VMobject(stroke_color=color, stroke_width=w, fill_opacity=0)
    m.set_points_as_corners([ax.c2p(t, y) for t, y in zip(ts, ys)])
    return m


def kline(ax, a=0, b=13, y=K0, color=GOLDC):
    return DashedLine(ax.c2p(a, y), ax.c2p(b, y), color=color, stroke_width=5, dash_length=0.18)


class S00Title(TitleCard):
    LESSON = "Populations and Carrying Capacity"
    TITLE = "Carrying Capacity Moves With Conditions"


# ---------------------------------------------------------------------------------------------
class S01Puzzle(SpokenScene):
    """the survey and the puzzle: the Bay is the same size, the crab count is not."""

    def construct(self):
        bay = RoundedRectangle(corner_radius=0.5, width=4.8, height=4.0, stroke_color=GREY, stroke_width=4,
                               fill_color=GREY, fill_opacity=0.08).move_to([-3.6, 0.45, 0])
        baylab = T("Chesapeake Bay (schematic)", 24, GREY).next_to(bay, DOWN, buff=0.15)
        marks = VGroup(*[Dot(radius=0.06, color=CTEAL).move_to([-5.45 + 0.42 * (i % 9), 2.0 - 0.42 * (i // 9) * 1.0 - 0.0, 0])
                         for i in range(9 * 7)])
        marks.move_to(bay.get_center() + [0, 0.2, 0])
        for m in marks:
            pass
        self.at("Every winter")
        self.play(FadeIn(bay), FadeIn(baylab), run_time=1.0)

        dredge = Arrow([-5.7, -1.2, 0], [-1.6, -1.2, 0], color=CTEAL, stroke_width=7, buff=0)
        dlab = T("dredge dragged along the bottom", 24, CTEAL).next_to(bay, UP, buff=0.18)
        self.at("drag dredges")
        self.play(GrowArrow(dredge), FadeIn(dlab, shift=DOWN * 0.1), run_time=1.6)

        slab = T("about 1,500 sites (marks not to scale)", 24, CTEAL).next_to(baylab, DOWN, buff=0.12)
        self.at("They sample blue crabs")
        self.play(LaggedStart(*[FadeIn(m, scale=0.4) for m in marks], lag_ratio=0.02), FadeIn(slab), run_time=2.0)

        base = -1.55
        b1 = Rectangle(width=1.2, height=2.0, stroke_color=BLUE, stroke_width=3, fill_color=BLUE, fill_opacity=0.45)
        b2 = Rectangle(width=1.2, height=3.3, stroke_color=BLUE, stroke_width=3, fill_color=BLUE, fill_opacity=0.45)
        b1.move_to([2.3, base + 1.0, 0])
        b2.move_to([4.4, base + 1.65, 0])
        l1 = T("one winter", 24, TEXT).next_to(b1, DOWN, buff=0.1)
        l2 = T("next winter", 24, TEXT).next_to(b2, DOWN, buff=0.12)
        ylab = T("estimated crabs", 24, BLUE).move_to([3.35, 3.0, 0])
        self.at("From one winter")
        self.play(GrowFromEdge(b1, DOWN), FadeIn(l1), FadeIn(ylab), run_time=0.9)
        self.play(GrowFromEdge(b2, DOWN), FadeIn(l2), run_time=0.9)

        gap = DoubleArrow([5.5, base + 2.0, 0], [5.5, base + 3.3, 0], color=GOLDC, stroke_width=5, buff=0,
                          max_tip_length_to_length_ratio=0.4)
        guide = DashedLine([2.9, base + 2.0, 0], [5.5, base + 2.0, 0], color=GREY, stroke_width=3)
        glab = T("more than 100 million", 24, GOLDC).next_to(gap, UP, buff=0.08).shift(LEFT * 0.35)
        glab.move_to([glab.get_center()[0], base + 3.3 + 0.0, 0]).shift(UP * 0.0)
        self.at("more than")
        self.play(Create(guide), GrowArrow(gap), run_time=0.7)
        glab.next_to(gap, UP, buff=0.12)
        glab.shift(LEFT * (max(0, glab.get_right()[0] - 6.5)))
        self.play(FadeIn(glab, shift=DOWN * 0.1), run_time=0.5)
        note = T("estimates, bars not to scale", 22, GREY).move_to([3.5, -2.55, 0])
        self.play(FadeIn(note), run_time=0.4)

        q = T("How many crabs can the Bay hold?", 36, GOLD, weight=BOLD).move_to([0, -3.3, 0])
        self.at("So how many")
        self.play(FadeIn(q, shift=UP * 0.15), run_time=0.8)
        self.finish()


# ---------------------------------------------------------------------------------------------
class S02Factors(SpokenScene):
    """population, biotic and abiotic factors, limiting factor."""

    def construct(self):
        box = RoundedRectangle(corner_radius=0.25, width=4.6, height=3.6, stroke_color=BLUE, stroke_width=4,
                               fill_color=BLUE, fill_opacity=0.07).move_to([-3.8, 0.55, 0])
        crabs = VGroup(*[crab(1.1).move_to(box.get_center() + [(i % 4 - 1.5) * 0.9, (1 - i // 4) * 0.85, 0])
                         for i in range(12)])
        plab = T("population", 40, BLUE, weight=BOLD).next_to(box, UP, buff=0.15)
        sub = T("one species, same place, same time", 24, TEXT).next_to(box, DOWN, buff=0.15)
        self.at("A population is")
        self.play(FadeIn(box), LaggedStart(*[FadeIn(c, scale=0.5) for c in crabs], lag_ratio=0.06), FadeIn(plab),
                  run_time=1.8)
        self.play(FadeIn(sub), run_time=0.6)
        nt = T("crab tokens, not counts", 22, GREY).next_to(sub, DOWN, buff=0.1)
        self.play(FadeIn(nt), run_time=0.3)

        self.at("The blue crabs in the Bay")
        self.play(Indicate(box, color=BLUE, scale_factor=1.04), run_time=1.0)

        # biotic
        bh = T("biotic: living", 30, GREEN, weight=BOLD)
        b1 = chip("predators", GREEN, 26)
        b2 = chip("disease", GREEN, 26)
        bg = VGroup(bh, VGroup(b1, b2).arrange(RIGHT, buff=0.3)).arrange(DOWN, buff=0.22).move_to([3.5, 2.05, 0])
        a1 = arrow_to([0.9, 2.05, 0], [-1.35, 1.35, 0], GREEN)
        self.at("Biotic factors are")
        self.play(FadeIn(bh, shift=LEFT * 0.1), run_time=0.5)
        self.at("like predators")
        self.play(FadeIn(b1, shift=LEFT * 0.2), FadeIn(b2, shift=LEFT * 0.2), GrowArrow(a1), run_time=0.9)

        oh = T("abiotic: nonliving", 30, ORANGE, weight=BOLD)
        o1 = chip("temperature", ORANGE, 26)
        o2 = chip("salinity (salt level)", ORANGE, 26)
        og = VGroup(oh, VGroup(o1, o2).arrange(DOWN, buff=0.2)).arrange(DOWN, buff=0.22).move_to([3.5, -0.75, 0])
        a2 = arrow_to([0.9, -0.2, 0], [-1.35, -0.2, 0], ORANGE)
        self.at("Abiotic factors are")
        self.play(FadeIn(oh, shift=LEFT * 0.1), run_time=0.5)
        self.at("like temperature")
        self.play(FadeIn(o1, shift=LEFT * 0.2), FadeIn(o2, shift=LEFT * 0.2), GrowArrow(a2), run_time=0.9)

        ll = T("limiting factor: keeps a population from growing larger", 28, RED, weight=BOLD).move_to([0, -3.35, 0])
        self.at("A limiting factor")
        self.play(FadeIn(ll, shift=UP * 0.1), box.animate.set_stroke(RED, 5), run_time=0.9)
        self.play(Indicate(a1, color=RED), Indicate(a2, color=RED), run_time=1.0)
        self.finish()


# ---------------------------------------------------------------------------------------------
class S03Exp(SpokenScene):
    """exponential growth from the lesson's own numbers: 10, 20, 40, 80, 160, 320."""

    def construct(self):
        vals = [10, 20, 40, 80, 160, 320]
        base = -2.35
        H = 4.0
        xs = [-4.5 + 1.8 * i for i in range(6)]
        floor = Line([-5.5, base, 0], [5.5, base, 0], color=GREY, stroke_width=3)
        steps = VGroup(*[M(str(i), 28, GREY).move_to([xs[i], base - 0.35, 0]) for i in range(6)])
        axl = T("steps of 30 minutes", 24, GREY).move_to([0, base - 0.9, 0])

        c1 = chip("dish: 10 bacteria, fresh food", BLUE, 26).move_to([-3.1, 3.1, 0])
        c2 = T("each one splits in two every 30 minutes", 24, TEXT).move_to([3.0, 3.1, 0])

        bars, labs = [], []
        for i, v in enumerate(vals):
            h = H * v / 320
            b = Rectangle(width=1.0, height=h, stroke_color=BLUE, stroke_width=3, fill_color=BLUE, fill_opacity=0.45)
            b.move_to([xs[i], base + h / 2, 0])
            lab = M(str(v), 28, TEXT).next_to(b, UP, buff=0.1)
            bars.append(b)
            labs.append(lab)
        self.at("Suppose")
        self.play(FadeIn(c1, shift=DOWN * 0.1), Create(floor), FadeIn(steps), FadeIn(axl), GrowFromEdge(bars[0], DOWN), FadeIn(labs[0]), run_time=1.4)
        self.at("Each one splits")
        self.play(FadeIn(c2, shift=DOWN * 0.1), run_time=0.8)

        self.at("Now there are")
        self.play(*[AnimationGroup(GrowFromEdge(bars[i], DOWN), FadeIn(labs[i])) for i in range(1, 6)], lag_ratio=0.45,
                  run_time=4.2)

        ex = chip("exponential growth", BLUE, 30).move_to([-3.2, 2.05, 0])
        self.at("This is exponential")
        self.play(FadeIn(ex, scale=0.8), run_time=0.7)

        jc = ParametricFunction(lambda t: np.array([-4.5 + 1.8 * t, base + H * (10 * 2 ** t) / 320, 0]), t_range=[0, 5, 0.02],
                                color=BLUE, stroke_width=7)
        jl = T("J shape", 40, BLUE, weight=BOLD).move_to([-2.4, 0.5, 0])
        self.at("On a graph")
        self.play(Create(jc), run_time=1.6)
        self.play(FadeIn(jl, scale=0.8), run_time=0.5)

        nr = T("no real population can keep this up for long", 26, RED).move_to([0, -3.5, 0])
        self.at("No real population")
        self.play(FadeOut(axl), FadeIn(nr, shift=UP * 0.1), run_time=0.8)
        self.finish()


# ---------------------------------------------------------------------------------------------
class S04Logistic(SpokenScene):
    """limits bend the J into an S that levels near carrying capacity (model sketch)."""

    def construct(self):
        ax, lbls, nt = make_axes()
        self.play(Create(ax), FadeIn(lbls), FadeIn(nt), run_time=0.8)
        segA = curve(ax, f_pop, 0, 4.0, BLUE)
        jt = T("J shape", 34, BLUE, weight=BOLD).move_to(ax.c2p(2.2, 5.2))
        self.play(Create(segA), FadeIn(jt), run_time=0.9)

        lim = chip("limits: food, competition, disease", RED, 26).move_to([-3.9, 2.55, 0])
        lim.move_to([ax.c2p(5.3, 0)[0] - 1.0, 3.2, 0])
        self.at("Food runs short")
        self.play(FadeIn(lim, shift=DOWN * 0.1), run_time=0.7)

        segB = curve(ax, f_pop, 4.0, 8.0, BLUE)
        st = T("S shape", 34, BLUE, weight=BOLD).move_to(ax.c2p(2.2, 5.2))
        self.at("bends into")
        self.play(Create(segB), FadeOut(jt), FadeIn(st), run_time=2.2)

        kl = kline(ax, 0, 13)
        kt = chip("carrying capacity", GOLDC, 28)
        kt.move_to(ax.c2p(3.6, 9.15))
        self.at("The level it settles")
        self.play(Create(kl), FadeIn(kt, shift=DOWN * 0.1), run_time=1.0)

        self.at("Carrying capacity is the largest")
        self.play(Indicate(kt, color=GOLDC, scale_factor=1.12), run_time=1.0)

        eq = chip("births and deaths about equal", TEXT, 24).move_to(ax.c2p(9.1, 4.2))
        self.at("births and deaths")
        self.play(FadeIn(eq, shift=UP * 0.1), run_time=0.7)

        segC = curve(ax, f_pop, 8.0, 13.0, BLUE)
        self.at("go up and down")
        self.play(Create(segC), run_time=2.4)

        de = chip("dynamic equilibrium", BLUE, 28).move_to(ax.c2p(9.1, 2.5))
        self.at("dynamic equilibrium")
        self.play(FadeIn(de, shift=UP * 0.1), run_time=0.7)
        self.finish()


# ---------------------------------------------------------------------------------------------
def prior_scene(scene):
    """rebuild the end state of S04 in the same place (axes, S curve to t=7, gold line)."""
    ax, lbls, nt = make_axes()
    cur = curve(ax, f_pop, 0, 7.0, BLUE)
    kl = kline(ax, 0, 7)
    kt = chip("carrying capacity", GOLDC, 28).move_to(ax.c2p(3.6, 9.15))
    scene.add(ax, lbls, nt, cur, kl, kt)
    return ax, lbls, nt, cur, kl, kt


def delayed(anim, delay):
    return Succession(Wait(max(0.01, delay)), anim)


def model_ext(ax):
    """the model sketch after t=7: K steps up then down; the population follows (logistic step, made-up units)."""
    ts = np.arange(7.0, 13.0001, 0.05)
    Kv = K_of_t(ts)
    Nv = np.zeros_like(ts)
    N = float(logistic(7.0))
    for i in range(len(ts)):
        if i:
            N += 0.05 * 1.1 * N * (1 - N / Kv[i])
        Nv[i] = N
    Nv = Nv + wob(ts)
    cut = int(round((10.0 - 7.0) / 0.05))
    return ts, Kv, Nv, cut


class S05Moves(SpokenScene):
    """the gold line is not fixed: it rises and falls with conditions, and the population follows."""

    def construct(self):
        ax, lbls, nt, cur, kl, kt = prior_scene(self)
        ts, Kv, Nv, cut = model_ext(ax)
        K1d = DashedVMobject(poly(ax, ts[:cut + 1], Kv[:cut + 1], GOLDC, 5), num_dashes=14, dashed_ratio=0.62)
        N1 = poly(ax, ts[:cut + 1], Nv[:cut + 1], BLUE, 6)
        K2d = DashedVMobject(poly(ax, ts[cut:], Kv[cut:], GOLDC, 5), num_dashes=14, dashed_ratio=0.62)
        N2 = poly(ax, ts[cut:], Nv[cut:], BLUE, 6)

        self.at("not one number")
        self.play(Indicate(kt, color=GOLDC, scale_factor=1.12), run_time=1.0)

        up = T("raise it", 28, GREEN, weight=BOLD).move_to([-5.9, 2.9, 0])
        g1 = chip("more food", GREEN, 22)
        g2 = chip("a mild winter", GREEN, 22)
        g3 = chip("more hiding places", GREEN, 22)
        gs = VGroup(g1, g2, g3).arrange(DOWN, buff=0.15, aligned_edge=LEFT).next_to(up, DOWN, buff=0.18).align_to(up, LEFT)
        t0 = self.t_of("More food") - 0.2
        d2 = self.t_of("a mild winter") - 0.2 - t0
        d3 = self.t_of("more hiding places") - 0.2 - t0
        self.at("More food")
        self.play(FadeIn(up), FadeIn(g1, shift=RIGHT * 0.2), Create(K1d), Create(N1),
                  delayed(FadeIn(g2, shift=RIGHT * 0.2), d2), delayed(FadeIn(g3, shift=RIGHT * 0.2), d3),
                  run_time=max(3.2, d3 + 1.0), rate_func=linear)

        down = T("lower it", 28, RED, weight=BOLD).move_to([-5.9, -0.45, 0])
        r1 = chip("a hard freeze", RED, 22)
        r2 = chip("loss of marsh grass", RED, 22)
        rs = VGroup(r1, r2).arrange(DOWN, buff=0.15, aligned_edge=LEFT).next_to(down, DOWN, buff=0.18).align_to(down, LEFT)
        t1 = self.t_of("A hard freeze") - 0.2
        d5 = self.t_of("loss of marsh grass") - 0.2 - t1
        self.at("A hard freeze")
        self.play(FadeIn(down), FadeIn(r1, shift=RIGHT * 0.2), Create(K2d), Create(N2),
                  delayed(FadeIn(r2, shift=RIGHT * 0.2), d5), run_time=max(3.0, d5 + 1.0), rate_func=linear)

        pp = chip("crabbing removes crabs", PURPLE, 22).move_to([-4.6, -3.05, 0])
        self.at("People change it")
        self.play(FadeIn(pp, shift=UP * 0.1), run_time=0.8)
        end = ax.c2p(12.6, Nv[-1] + 0.1)
        rm = Arrow(end + [0, 1.2, 0], end + [0, 0.35, 0], color=PURPLE, stroke_width=7, buff=0)
        self.at("Crabbing removes")
        self.play(GrowArrow(rm), run_time=0.7)
        self.finish()


# ---------------------------------------------------------------------------------------------
class S06Answer(SpokenScene):
    """answer in plain words, then the rule."""

    def construct(self):
        q = T("How many crabs can the Bay hold?", 38, GOLD, weight=BOLD).move_to([0, 3.15, 0])
        self.at("So how many crabs")
        self.play(FadeIn(q, shift=DOWN * 0.1), run_time=0.8)

        ax = Axes(x_range=[0, 13, 1], y_range=[0, 10, 1], x_length=5.6, y_length=3.8,
                  axis_config={"include_ticks": False, "include_numbers": False, "color": GREY, "stroke_width": 3,
                               "tip_width": 0.18, "tip_height": 0.18}, tips=True).move_to([3.8, -0.35, 0])
        nt = T("model sketch, made-up units", 22, GREY).next_to(ax, DOWN, buff=0.3)
        cur = curve(ax, f_pop, 0, 7.0, BLUE)
        kl = kline(ax, 0, 7)
        c1 = chip("a largest number\nit can support", GOLDC, 26)
        c2 = chip("that number moves\nwith conditions", GREEN, 26)
        c3 = chip("probably why the crab\ncount rises and falls", BLUE, 26)
        chain = VGroup(c1, c2, c3).arrange(DOWN, buff=0.6, aligned_edge=LEFT).move_to([-4.2, -0.25, 0])
        ar1 = Arrow(c1.get_bottom(), c2.get_top(), color=GREY, buff=0.08, stroke_width=5)
        ar2 = Arrow(c2.get_bottom(), c3.get_top(), color=GREY, buff=0.08, stroke_width=5)

        self.at("There is a largest")
        self.play(FadeIn(c1, shift=RIGHT * 0.2), Create(ax), FadeIn(nt), Create(cur), Create(kl), run_time=1.8)

        ts, Kv, Nv, cut = model_ext(ax)
        K1d = DashedVMobject(poly(ax, ts[:cut + 1], Kv[:cut + 1], GOLDC, 5), num_dashes=14, dashed_ratio=0.62)
        N1 = poly(ax, ts[:cut + 1], Nv[:cut + 1], BLUE, 6)
        K2d = DashedVMobject(poly(ax, ts[cut:], Kv[cut:], GOLDC, 5), num_dashes=14, dashed_ratio=0.62)
        N2 = poly(ax, ts[cut:], Nv[cut:], BLUE, 6)
        self.at("But that number moves")
        self.play(GrowArrow(ar1), FadeIn(c2, shift=RIGHT * 0.2), Create(K1d), Create(N1), run_time=1.6)
        self.play(Create(K2d), Create(N2), run_time=1.6)

        self.at("This is probably why")
        self.play(GrowArrow(ar2), FadeIn(c3, shift=RIGHT * 0.2), run_time=0.9)

        self.at("Remember this rule")
        self.play(FadeOut(VGroup(q, chain, ar1, ar2, ax, nt, cur, kl, K1d, N1, K2d, N2)), run_time=0.8)
        rule = T("Carrying capacity is not fixed.", 52, GOLD, font=TITLE_FONT).move_to([0, 0.5, 0])
        fit(rule, max_w=11.8)
        sub = T("It moves with the environment.", 40, TEXT, font=TITLE_FONT).move_to([0, -0.7, 0])
        self.at("Carrying capacity is not fixed")
        self.play(FadeIn(rule, shift=UP * 0.15), run_time=0.9)
        self.at("It moves with")
        self.play(FadeIn(sub, shift=UP * 0.15), run_time=0.8)
        self.finish()


class S07End(EndCard):
    LINE = "Carrying capacity is not fixed."
