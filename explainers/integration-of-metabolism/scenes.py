"""Integration of metabolism: how the body switches fuels  (Biochemistrypedia explainer)

Through-line: the body defends blood glucose in a fixed order (diet -> glycogen -> new glucose),
and in starvation ketone bodies spare the muscle protein that the brain would otherwise cost.

Timed to the SPOKEN words: self.at("phrase") waits until the narrator starts that phrase
(word timestamps in audio/words.json, from the real narration audio).

COLOR MAP (one color per concept, whole video)
  YELLOW = glucose (dietary glucose, blood glucose, the 120 g / 40 g the brain needs)
  ORANGE = glycogen
  PINK   = gluconeogenesis / new glucose
  TEAL   = fatty acids (and the acetyl-CoA made from them)
  GREEN  = ketone bodies
  RED    = muscle protein (the cost), barriers, blocked steps
  BRAIN  = the brain (periwinkle)
  BLUE   = insulin        PURPLE = glucagon
  GOLD   = "you are here" on the fed -> starving strip
  GREY   = axes, structure, organs, de-emphasized things
No molecular structures are drawn anywhere: only labelled chips, flows, blocks and plots.
"""
import numpy as np
from bp_style import *  # noqa: F401,F403

config.disable_caching = True

ORANGE = "#F2994A"
PINK = "#F06FA0"
TEAL_FA = "#3FB8C0"
BRAIN = "#8FA8FF"
PURPLE = "#B58CD9"
INSULIN = BLUE


# ---------------------------------------------------------------------------------------------
# helpers
# ---------------------------------------------------------------------------------------------
def arr(a, b, color=GREY, w=5, tip=0.2):
    return Arrow(np.array(a, dtype=float), np.array(b, dtype=float), color=color, stroke_width=w,
                 buff=0.0, tip_length=tip, max_tip_length_to_length_ratio=0.45)


def xmark(center, size=0.2, color=RED, w=7):
    c = np.array(center, dtype=float)
    return VGroup(Line(c + [-size, -size, 0], c + [size, size, 0], color=color, stroke_width=w),
                  Line(c + [-size, size, 0], c + [size, -size, 0], color=color, stroke_width=w))


def sg(x):
    return 1.0 / (1.0 + np.exp(-x))


def organ(text, pos, w, h=0.95, size=32, color=GREY, label_color=TEXT):
    box = RoundedRectangle(corner_radius=0.16, width=w, height=h, stroke_color=color, stroke_width=3,
                           fill_color=color, fill_opacity=0.1)
    lab = T(text, size, label_color)
    g = VGroup(box, lab.move_to(box))
    return g.move_to(pos)


STATES = [("Fed", "0–4 h"), ("Early fasting", "4–16 h"), ("Fasting", "1–2 days"),
          ("Starvation", "days and beyond")]


def make_strip(y=-3.05, h=0.85, big=False, active=()):
    """The four-state fed -> starving strip. active = indices lit in GOLD."""
    total, gap = 12.3, 0.1
    w = (total - 3 * gap) / 4
    segs = []
    for i, (a, b) in enumerate(STATES):
        box = RoundedRectangle(corner_radius=0.12, width=w, height=h, stroke_color=GREY, stroke_width=2,
                               fill_color=GOLD, fill_opacity=0)
        lab = VGroup(T(a, 32 if big else 24, TEXT), T(b, 24 if big else 22, GREY)).arrange(DOWN, buff=0.04).move_to(box)
        segs.append(VGroup(box, lab))
    g = VGroup(*segs).arrange(RIGHT, buff=gap).move_to([0, y, 0])
    for i in active:
        g[i][0].set_stroke(GOLD, 4).set_fill(GOLD, 0.2)
    return g


def dim(c):
    return [c[0].animate.set_stroke(opacity=0.3).set_fill(opacity=0.03), c[1].animate.set_opacity(0.3)]


def undim(c):
    return [c[0].animate.set_stroke(opacity=1).set_fill(opacity=0.16), c[1].animate.set_opacity(1)]


def solid(c):
    """A chip with an opaque backing so lines behind it do not show through."""
    back = c[0].copy().set_fill(BG, 1).set_stroke(width=0)
    return VGroup(back, c)


def seg_on(seg):
    return seg[0].animate.set_stroke(GOLD, 4).set_fill(GOLD, 0.2)


def seg_off(seg):
    return seg[0].animate.set_stroke(GREY, 2).set_fill(GOLD, 0)


def dots_along(scene, line, color, n=3, rt=1.4, r=0.1, lag=0.35):
    ds = [Dot(line.get_start(), radius=r, color=color) for _ in range(n)]
    scene.add(*ds)
    scene.play(LaggedStart(*[MoveAlongPath(d, line, rate_func=linear) for d in ds], lag_ratio=lag), run_time=rt)
    scene.play(*[FadeOut(d, scale=0.4) for d in ds], run_time=0.2)


def pile(center, rows=4, cols=3):
    blocks = VGroup(*[Rectangle(width=0.46, height=0.4, stroke_width=0, fill_color=RED, fill_opacity=0.85)
                      for _ in range(rows * cols)]).arrange_in_grid(rows=rows, cols=cols, buff=0.06)
    blocks.move_to(center)
    outline = DashedRectangle(blocks, color=GREY) if False else Rectangle(
        width=blocks.width + 0.2, height=blocks.height + 0.2, stroke_color=GREY, stroke_width=2,
        fill_opacity=0).move_to(blocks)
    outline.set_stroke(opacity=0.5)
    return blocks, outline


BRAIN_X, WALL_X = 5.0, 3.35


def brain_chip(y=0.5):
    box = RoundedRectangle(corner_radius=0.16, width=2.0, height=1.3, stroke_color=BRAIN, stroke_width=3.5,
                           fill_color=BRAIN, fill_opacity=0.16)
    return VGroup(box, T("brain", 34, BRAIN).move_to(box)).move_to([BRAIN_X, y, 0])


def wall(y0=-0.6, y1=1.6):
    return DashedLine([WALL_X, y0, 0], [WALL_X, y1, 0], color=GREY, stroke_width=5, dash_length=0.14)


# ---------------------------------------------------------------------------------------------
class S00Title(TitleCard):
    LESSON = "Integration of metabolism"
    TITLE = "How the body switches fuels"


# ---------------------------------------------------------------------------------------------
class S01TimedSequence(SpokenScene):
    """Pathway chips -> not all at once -> opposites form a futile cycle -> a timed sequence."""

    def construct(self):
        names = [("glycolysis", YELLOW), ("gluconeogenesis", PINK), ("β-oxidation", TEAL_FA),
                 ("ketogenesis", GREEN), ("glycogen synthesis", ORANGE), ("glycogen breakdown", ORANGE)]
        chips = [chip(n, c, size=26) for n, c in names]
        pos = [(-4.2, 1.5), (0, 1.5), (4.2, 1.5), (-4.2, -0.3), (0, -0.3), (4.2, -0.3)]
        for c, p in zip(chips, pos):
            c.move_to([p[0], p[1], 0])

        self.play(LaggedStart(*[FadeIn(c, scale=0.8) for c in chips], lag_ratio=0.3), run_time=2.6)
        self.at("whole time you read it")
        self.play(LaggedStart(*[Indicate(c, scale_factor=1.07, color=TEXT) for c in chips], lag_ratio=0.12),
                  run_time=1.2)
        self.at("but not all at once")
        self.play(*[a for i in (1, 2, 3, 5) for a in dim(chips[i])], run_time=0.8)

        # opposites: glycolysis and gluconeogenesis as two arrows between glucose and pyruvate
        self.at("Many of them")
        glc = chip("glucose", YELLOW, size=28).move_to([-3.7, 0.7, 0])
        pyr = chip("pyruvate", GREY, size=28).move_to([3.7, 0.7, 0])
        top = arr([-2.5, 1.25, 0], [2.5, 1.25, 0], YELLOW)
        bot = arr([2.5, 0.15, 0], [-2.5, 0.15, 0], PINK)
        self.play(*[FadeOut(chips[i]) for i in (2, 3, 4, 5)], *undim(chips[1]), run_time=0.3)
        self.play(chips[0].animate.move_to([0, 2.05, 0]), chips[1].animate.move_to([0, -0.55, 0]),
                  FadeIn(glc), FadeIn(pyr), run_time=0.7)
        self.at("that would cancel")
        self.play(GrowArrow(top), GrowArrow(bot), run_time=0.8)
        self.at("futile cycle")
        fc = T("futile cycle", 30, RED, weight=BOLD).move_to([0, 0.7, 0])
        loop = Polygon([-2.5, 1.25, 0], [2.5, 1.25, 0], [3.0, 0.7, 0], [2.5, 0.15, 0], [-2.5, 0.15, 0],
                       [-3.0, 0.7, 0], stroke_width=0)
        dot = Dot([-2.5, 1.25, 0], radius=0.12, color=YELLOW)
        self.add(dot)
        self.play(FadeIn(fc), MoveAlongPath(dot, loop, rate_func=linear), run_time=1.0)
        self.play(FadeOut(dot), run_time=0.1)

        # a timed sequence
        self.at("so the body switches")
        strip = make_strip(y=0.5, h=1.5, big=True)
        tline = arr([-6.1, -0.6, 0], [6.1, -0.6, 0], GREY, w=4)
        tlab = T("time", 28, GREY).move_to([0, -1.15, 0])
        self.play(FadeOut(VGroup(chips[0], chips[1], glc, pyr, top, bot, fc)), run_time=0.45)
        self.play(LaggedStart(*[FadeIn(s, shift=UP * 0.15) for s in strip], lag_ratio=0.25), run_time=1.1)
        self.at("in a timed sequence")
        self.play(GrowArrow(tline), FadeIn(tlab), run_time=1.0)
        self.at("from fed")
        self.play(seg_on(strip[0]), run_time=0.4)
        self.at("to fasting")
        self.play(seg_off(strip[0]), seg_on(strip[1]), seg_on(strip[2]), run_time=0.5)
        self.at("to starving")
        self.play(seg_off(strip[1]), seg_off(strip[2]), seg_on(strip[3]), run_time=0.5)
        self.finish()


# ---------------------------------------------------------------------------------------------
class S02GlucoseRelay(SpokenScene):
    """Stacked-area: where blood glucose comes from over the first day of fasting."""

    def construct(self):
        def raw_diet(t):
            return 1.6 * sg(-(t - 3.0) / 0.6)

        def raw_gly(t):
            # the liver is net storing glycogen while the meal is absorbed, so glycogenolysis only
            # takes over as dietary glucose fades (~4 h); about 1/8 of supply is left at 24 h
            return (0.02 + sg((t - 3.9) / 0.7)) * (1 - sg((t - 17.5) / 3.5))

        def raw_gng(t):
            return 0.03 + sg((t - 9.5) / 3.5)

        def shares(t):
            a, b, c = raw_diet(t), raw_gly(t), raw_gng(t)
            s = a + b + c
            return a / s, b / s, c / s

        def d_top(t):
            return shares(t)[0]

        def g_top(t):
            s = shares(t)
            return s[0] + s[1]

        grid = np.linspace(0, 24, 2401)
        diff = [shares(t)[1] - shares(t)[2] for t in grid]
        t_cross = next(grid[i] for i in range(1, len(grid)) if diff[i - 1] > 0 >= diff[i])

        ax = Axes(x_range=[0, 24, 4], y_range=[0, 1, 0.25], x_length=6.6, y_length=3.7,
                  axis_config={"include_numbers": False, "include_ticks": False, "color": GREY,
                               "stroke_width": 3}, tips=False)
        ax.shift(np.array([-5.6, -1.5, 0]) - ax.c2p(0, 0))
        xticks = VGroup(*[M(str(h), 22, GREY).move_to(ax.c2p(h, 0) + DOWN * 0.3) for h in range(0, 25, 4)])
        xlab = T("hours since the meal", 24, GREY).move_to(ax.c2p(12, 0) + DOWN * 0.78)
        ylab = T("share of blood glucose supply", 22, GREY).rotate(PI / 2).move_to([-6.15, ax.c2p(0, 0.5)[1], 0])
        heading = T("Where blood glucose comes from", 34, font=TITLE_FONT).move_to([-2.3, 3.2, 0])
        strip = make_strip(active=(0,))

        tt = ValueTracker(0.05)

        def band(lo, hi, color):
            def f():
                tm = tt.get_value()
                n = max(3, int(tm / 0.2) + 2)
                ts = np.linspace(0, tm, n)
                top = [ax.c2p(t, hi(t)) for t in ts]
                bot = [ax.c2p(t, lo(t)) for t in ts[::-1]]
                return Polygon(*top, *bot, stroke_width=0, fill_color=color, fill_opacity=0.88)
            return always_redraw(f)

        b_diet = band(lambda t: 0.0, d_top, YELLOW)
        b_gly = band(d_top, g_top, ORANGE)
        b_gng = band(g_top, lambda t: 1.0, PINK)
        cursor = always_redraw(lambda: VGroup(
            Line(ax.c2p(tt.get_value(), 0), ax.c2p(tt.get_value(), 1.0), color=TEXT, stroke_width=2.5),
            Dot(ax.c2p(tt.get_value(), 1.0), radius=0.07, color=TEXT)))

        # hormone bars
        BY, BH = -1.7, 1.5

        def ins(t):
            return 0.12 + 0.88 * sg((t - 1.5) / 0.3) * sg(-(t - 4.0) / 0.4)

        def glu(t):
            return 0.12 + 0.88 * sg((t - 5.5) / 0.5)

        def bar(fn, x, color):
            def f():
                h = max(0.05, fn(tt.get_value()) * BH)
                return Rectangle(width=0.9, height=h, stroke_width=0, fill_color=color, fill_opacity=0.9
                                 ).move_to([x, BY + h / 2, 0])
            return always_redraw(f)

        bar_i, bar_g = bar(ins, 3.4, INSULIN), bar(glu, 5.3, PURPLE)
        base = Line([2.6, BY, 0], [6.1, BY, 0], color=GREY, stroke_width=3)
        lab_i = T("insulin", 24, INSULIN).move_to([3.4, BY - 0.4, 0])
        lab_g = T("glucagon", 24, PURPLE).move_to([5.3, BY - 0.4, 0])

        # --- build ------------------------------------------------------------------------
        self.play(FadeIn(heading), Create(ax), FadeIn(xticks), FadeIn(xlab), FadeIn(ylab), run_time=1.8)
        self.play(FadeIn(strip), run_time=0.6)
        self.at("handing blood glucose")
        self.add(b_diet, b_gly, b_gng, cursor)
        self.at("Right after eating")
        self.play(FadeIn(base), FadeIn(bar_i), FadeIn(bar_g), FadeIn(lab_i), FadeIn(lab_g), run_time=0.8)
        self.at("glucose floods in")
        self.play(tt.animate.set_value(1.0), run_time=1.3, rate_func=linear)
        self.at("insulin rises", lead=0.55)
        self.play(tt.animate.set_value(3.0), run_time=1.5, rate_func=linear)
        diet_lab = T("dietary glucose", 22, BG, weight=BOLD).rotate(PI / 2).move_to(
            ax.c2p(1.55, d_top(1.55) / 2))
        self.play(FadeIn(diet_lab), run_time=0.4)

        # store
        self.at("is store")
        store = T("STORE", 36, INSULIN, weight=BOLD).move_to([4.35, 2.6, 0])
        self.play(FadeIn(store, scale=1.2), run_time=0.5)
        self.at("liver lays down glycogen")
        c1 = chip("liver lays down\nglycogen", ORANGE, size=22).move_to([4.35, 1.65, 0])
        self.play(FadeIn(c1, shift=DOWN * 0.15), run_time=0.5)
        self.at("muscle takes up glucose")
        c2 = chip("muscle takes up\nglucose", YELLOW, size=22).move_to([4.35, 0.5, 0])
        self.play(FadeIn(c2, shift=DOWN * 0.15), run_time=0.5)

        # early fasting
        self.at("From 4 to 16 hours")
        v4 = DashedLine(ax.c2p(4, 0), ax.c2p(4, 1.0) + UP * 0.15, color=GOLD, stroke_width=3, dash_length=0.1)
        v16 = DashedLine(ax.c2p(16, 0), ax.c2p(16, 1.0) + UP * 0.15, color=GOLD, stroke_width=3, dash_length=0.1)
        self.play(FadeOut(store), FadeOut(c1), FadeOut(c2), seg_off(strip[0]), seg_on(strip[1]),
                  Create(v4), Create(v16), xticks[1].animate.set_color(GOLD), xticks[4].animate.set_color(GOLD),
                  tt.animate.set_value(3.6), run_time=1.3, rate_func=linear)
        self.at("no more dietary glucose")
        self.play(tt.animate.set_value(5.0), run_time=1.9, rate_func=linear)
        self.at("and glucagon rises", lead=0.5)
        self.play(tt.animate.set_value(7.2), run_time=1.6, rate_func=linear)
        self.at("The liver now maintains")
        gly_lab = T("glycogen", 24, BG, weight=BOLD).move_to(ax.c2p(7.4, 0.33))
        c3 = chip("liver breaks down\nglycogen", ORANGE, size=22).move_to([4.35, 1.65, 0])
        self.play(FadeIn(c3, shift=DOWN * 0.15), tt.animate.set_value(11.0), run_time=2.8, rate_func=linear)
        self.play(FadeIn(gly_lab), run_time=0.3)
        self.at("is finite")
        self.play(tt.animate.set_value(24.0), run_time=3.1, rate_func=linear)
        gng_lab = T("new glucose", 24, BG, weight=BOLD).move_to(ax.c2p(19.0, 0.62))
        self.play(FadeIn(gng_lab), run_time=0.4)

        # roughly equal by the end of an overnight fast
        self.at("By the end of an overnight fast")
        xc = ax.c2p(t_cross, 0)[0]
        lo, mid, hi = ax.c2p(t_cross, d_top(t_cross))[1], ax.c2p(t_cross, g_top(t_cross))[1], ax.c2p(t_cross, 1.0)[1]
        vx = DashedLine([xc, ax.c2p(0, 0)[1], 0], [xc, hi + 0.15, 0], color=TEXT, stroke_width=2.5, dash_length=0.1)
        ov = T("overnight", 24, TEXT).move_to([xc, hi + 0.4, 0])
        ba = DoubleArrow([xc, lo + 0.04, 0], [xc, mid - 0.04, 0], color=TEXT, stroke_width=5, buff=0,
                         tip_length=0.15, max_tip_length_to_length_ratio=0.45)
        bb = DoubleArrow([xc, mid + 0.04, 0], [xc, hi - 0.04, 0], color=TEXT, stroke_width=5, buff=0,
                         tip_length=0.15, max_tip_length_to_length_ratio=0.45)
        self.play(Create(vx), FadeIn(ov), run_time=0.8)
        self.at("making new glucose")
        self.play(GrowFromCenter(bb), Indicate(gng_lab, scale_factor=1.15, color=TEXT), run_time=0.9)
        self.at("glycogen breakdown", nth=0)
        self.play(GrowFromCenter(ba), Indicate(gly_lab, scale_factor=1.15, color=TEXT), run_time=0.9)
        self.finish()


# ---------------------------------------------------------------------------------------------
class S03Fasting(SpokenScene):
    """Liver makes glucose from lactate, alanine, glycerol; adipose releases fatty acids."""

    def construct(self):
        strip = make_strip(active=(1,))
        liver_box = RoundedRectangle(corner_radius=0.16, width=3.0, height=1.4, stroke_color=GREY, stroke_width=3,
                                     fill_color=GREY, fill_opacity=0.1)
        liver_t = T("liver", 34, TEXT).move_to(liver_box.get_center() + UP * 0.28)
        liver = VGroup(liver_box, liver_t).move_to([0, 1.4, 0])
        liver_t.move_to(liver_box.get_center() + UP * 0.28)
        muscle = organ("muscle", [-4.7, -1.2, 0], 2.2)
        adipose = organ("adipose", [4.7, -1.2, 0], 2.4)

        self.play(FadeIn(strip), LaggedStart(FadeIn(liver), FadeIn(muscle), FadeIn(adipose), lag_ratio=0.4),
                  run_time=1.5)
        self.at("at one to two days")
        self.play(seg_off(strip[1]), seg_on(strip[2]), run_time=0.6)

        # glycogen gauge drains
        self.at("With glycogen spent")
        gv = ValueTracker(1.0)
        gl = T("glycogen", 24, ORANGE).move_to([-3.7, 2.7, 0])
        gbox = RoundedRectangle(corner_radius=0.06, width=1.8, height=0.3, stroke_color=ORANGE, stroke_width=2.5
                                ).move_to([-3.7, 2.25, 0])

        def gfill():
            w = max(0.001, 1.72 * gv.get_value())
            return Rectangle(width=w, height=0.2, stroke_width=0, fill_color=ORANGE, fill_opacity=0.9
                             ).move_to(gbox.get_left() + RIGHT * (0.04 + w / 2))
        gf = always_redraw(gfill)
        self.play(FadeIn(gl), FadeIn(gbox), FadeIn(gf), run_time=0.4)
        self.play(gv.animate.set_value(0.0), run_time=1.1)

        # glucose out
        self.at("makes glucose from scratch")
        out = arr([0, 2.1, 0], [0, 2.7, 0], YELLOW)
        bg = chip("blood glucose", YELLOW, size=26).move_to([0, 3.05, 0])
        self.play(GrowArrow(out), FadeIn(bg), run_time=0.7)
        self.at("gluconeogenesis")
        gng = T("gluconeogenesis", 24, PINK).move_to(liver_box.get_center() + DOWN * 0.3)
        self.play(FadeIn(gng), liver_box.animate.set_stroke(PINK, 4).set_fill(PINK, 0.14), run_time=0.7)

        # substrates
        self.at("drawing on lactate")
        L = arr([-4.4, -0.7, 0], [-1.5, 1.0, 0])
        lt = T("lactate", 24, TEXT).move_to([-3.2, 0.62, 0])
        self.play(GrowArrow(L), FadeIn(lt), run_time=0.5)
        dots_along(self, Line(L.get_start(), L.get_end()), TEXT, n=2, rt=0.7)
        self.at("the amino acid alanine")
        A = arr([-3.55, -0.9, 0], [-1.0, 0.7, 0])
        at_ = T("alanine", 24, TEXT).move_to([-1.85, -0.5, 0])
        self.play(GrowArrow(A), FadeIn(at_), run_time=0.5)
        dots_along(self, Line(A.get_start(), A.get_end()), TEXT, n=2, rt=0.7)
        self.at("and glycerol")
        G = arr([4.4, -0.7, 0], [1.5, 1.0, 0])
        gt = T("glycerol", 24, TEXT).move_to([3.2, 0.62, 0])
        self.play(GrowArrow(G), FadeIn(gt), run_time=0.5)
        dots_along(self, Line(G.get_start(), G.get_end()), TEXT, n=2, rt=0.7)

        # fatty acids
        self.at("adipose tissue releases")
        self.play(Indicate(adipose, scale_factor=1.08, color=TEAL_FA), run_time=0.8)
        self.at("free fatty acids")
        F1 = arr([3.5, -1.35, 0], [-3.6, -1.35, 0], TEAL_FA)
        F2 = arr([3.5, -1.0, 0], [0.7, 0.72, 0], TEAL_FA)
        ft = T("free fatty acids", 24, TEAL_FA).move_to([0, -1.85, 0])
        self.play(GrowArrow(F1), GrowArrow(F2), FadeIn(ft), run_time=1.0)
        d1 = Line(F1.get_start(), F1.get_end())
        d2 = Line(F2.get_start(), F2.get_end())
        dots = [Dot(d1.get_start(), radius=0.1, color=TEAL_FA) for _ in range(3)] + \
               [Dot(d2.get_start(), radius=0.1, color=TEAL_FA) for _ in range(2)]
        self.add(*dots)
        self.play(LaggedStart(*[MoveAlongPath(d, l, rate_func=linear) for d, l in zip(dots, [d1, d1, d1, d2, d2])],
                              lag_ratio=0.3), run_time=1.2)
        self.play(*[FadeOut(d, scale=0.4) for d in dots], run_time=0.2)
        self.at("major fuel for muscle and liver")
        self.play(muscle[0].animate.set_stroke(TEAL_FA, 5), liver_box.animate.set_stroke(TEAL_FA, 5),
                  run_time=0.7)
        self.finish()


# ---------------------------------------------------------------------------------------------
ROW = 0.15   # vertical position of the main row in S04 / S05


class S04BrainProblem(SpokenScene):
    """Brain needs 120 g glucose; fatty acids bound to albumin are kept out; so muscle protein pays."""

    def construct(self):
        strip = make_strip(active=(3,))
        heading = T("The brain in starvation", 32, font=TITLE_FONT).move_to([-6.0, 3.2, 0], aligned_edge=LEFT)
        brain = brain_chip(ROW)
        line = Arrow([-5.9, ROW, 0], [WALL_X - 0.15, ROW, 0], color=GREY, stroke_width=3, buff=0, tip_length=0.18)
        blood = T("blood", 24, GREY).move_to([-5.2, ROW + 0.45, 0])
        wl = wall(ROW - 0.5, ROW + 0.5)
        wl_lab = T("barrier", 22, GREY).move_to([WALL_X, ROW - 0.75, 0])

        self.play(FadeIn(strip), run_time=0.6)
        self.at("the brain")
        self.play(FadeIn(heading), FadeIn(brain, scale=0.9), run_time=0.9)
        self.at("problem child")
        self.play(Indicate(brain, scale_factor=1.1, color=BRAIN), run_time=0.9)
        self.at("It normally burns")
        self.play(Create(line), FadeIn(blood), Create(wl), FadeIn(wl_lab), run_time=0.9)
        self.at("120")
        need = VGroup(M("120 g", 40, YELLOW), T("glucose per day", 24, YELLOW)).arrange(DOWN, buff=0.1
                                                                                         ).move_to([BRAIN_X, 1.95, 0])
        self.play(FadeIn(need, shift=DOWN * 0.15), run_time=0.5)
        gd = Line([-3.0, ROW, 0], [BRAIN_X - 1.05, ROW, 0])
        dots = [Dot(gd.get_start(), radius=0.11, color=YELLOW) for _ in range(4)]
        self.add(*dots)
        self.play(LaggedStart(*[MoveAlongPath(d, gd, rate_func=linear) for d in dots], lag_ratio=0.3),
                  run_time=2.6)
        self.play(*[FadeOut(d, scale=0.4) for d in dots], run_time=0.2)

        # fatty acids + albumin
        self.at("long chain fatty acids")
        ffa = solid(chip("fatty acid", TEAL_FA, size=24)).move_to([-5.0, ROW, 0])
        self.play(FadeIn(ffa, shift=RIGHT * 0.2), run_time=0.4)
        self.play(ffa.animate.move_to([-1.8, ROW, 0]), run_time=1.5, rate_func=linear)
        self.at("bound to albumin")
        alb = solid(chip("albumin", GREY, size=22)).next_to(ffa, UP, buff=0.08)
        self.play(FadeIn(alb, shift=DOWN * 0.1), run_time=0.4)
        self.play(ffa.animate.shift(RIGHT * 3.5), alb.animate.shift(RIGHT * 3.5), run_time=1.2, rate_func=linear)
        self.at("largely kept out")
        x = xmark([WALL_X, ROW, 0], 0.22)
        keep = T("kept out", 26, RED).move_to([2.0, ROW - 0.85, 0])
        self.play(Create(x), FadeIn(keep), ffa.animate.shift(LEFT * 1.4), alb.animate.shift(LEFT * 1.4),
                  run_time=0.8)

        # glucose-only option: the muscle pays
        self.at("If glucose were the only option")
        self.play(*[FadeOut(m) for m in (line, blood, wl, wl_lab, x, keep, ffa, alb)], run_time=0.8)
        self.at("the body would make")
        liver_box = RoundedRectangle(corner_radius=0.16, width=2.9, height=1.3, stroke_color=PINK, stroke_width=3.5,
                                     fill_color=PINK, fill_opacity=0.14)
        liver = VGroup(liver_box, T("liver", 32, TEXT).move_to(liver_box.get_center() + UP * 0.25)
                       ).move_to([-1.0, ROW, 0])
        out = arr([0.55, ROW, 0], [BRAIN_X - 1.2, ROW, 0], YELLOW, w=6)
        self.play(FadeIn(liver, scale=0.9), GrowArrow(out), run_time=0.7)
        self.at("all 120 grams")
        gd2 = Line(out.get_start(), out.get_end())
        dots2 = [Dot(gd2.get_start(), radius=0.11, color=YELLOW) for _ in range(3)]
        self.add(*dots2)
        self.play(Indicate(need, scale_factor=1.12, color=YELLOW),
                  LaggedStart(*[MoveAlongPath(d, gd2, rate_func=linear) for d in dots2], lag_ratio=0.3),
                  run_time=1.2)
        self.play(*[FadeOut(d, scale=0.4) for d in dots2], run_time=0.15)
        self.at("by gluconeogenesis")
        gng = T("gluconeogenesis", 24, PINK).move_to(liver_box.get_center() + DOWN * 0.28)
        self.play(FadeIn(gng), run_time=0.5)

        self.at("The main raw material")
        blocks, outline = pile([-5.0, ROW, 0])
        pa = arr([-4.0, ROW, 0], [-2.55, ROW, 0], RED, w=6)
        self.play(FadeIn(blocks, lag_ratio=0.05), FadeIn(outline), GrowArrow(pa), run_time=1.2)
        self.at("muscle protein")
        pl = T("muscle protein", 24, RED).move_to([-5.0, ROW - 1.45, 0])
        self.play(FadeIn(pl), run_time=0.5)
        self.at("consume yourself")
        order = list(range(len(blocks) - 1, -1, -1))
        self.play(LaggedStart(*[AnimationGroup(blocks[i].animate.move_to(liver.get_center()).scale(0.3)
                                                .set_opacity(0)) for i in order],
                              lag_ratio=0.12), run_time=2.3)
        self.finish()


# ---------------------------------------------------------------------------------------------
class S05Ketones(SpokenScene):
    """Ketones cross; liver makes them from fatty-acid acetyl-CoA; brain glucose need 120 -> 40 g."""

    def construct(self):
        strip = make_strip(active=(3,))
        heading = T("Ketone bodies", 32, GREEN, font=TITLE_FONT).move_to([-6.0, 3.2, 0], aligned_edge=LEFT)
        brain = brain_chip(ROW)
        wl = wall(ROW - 0.6, ROW + 0.6)

        gv = ValueTracker(120.0)
        g_lab = T("glucose needed", 24, YELLOW).move_to([1.5, 3.15, 0], aligned_edge=LEFT)
        g_num = always_redraw(lambda: M(f"{gv.get_value():.0f} g/day", 26, YELLOW).next_to(g_lab, RIGHT, buff=0.2))
        g_box = Rectangle(width=4.0, height=0.3, stroke_color=GREY, stroke_width=2).move_to([3.5, 2.7, 0])

        def gbar():
            w = max(0.01, 3.92 * gv.get_value() / 120.0)
            return Rectangle(width=w, height=0.22, stroke_width=0, fill_color=YELLOW, fill_opacity=0.9
                             ).move_to(g_box.get_left() + RIGHT * (0.04 + w / 2))
        g_bar = always_redraw(gbar)

        kv = ValueTracker(0.0)
        k_lab = T("ketone bodies burned", 24, GREEN).move_to([1.5, 2.2, 0], aligned_edge=LEFT)
        k_box = Rectangle(width=4.0, height=0.3, stroke_color=GREY, stroke_width=2).move_to([3.5, 1.75, 0])

        def kbar():
            w = max(0.01, 3.92 * kv.get_value())
            return Rectangle(width=w, height=0.22, stroke_width=0, fill_color=GREEN, fill_opacity=0.9
                             ).move_to(k_box.get_left() + RIGHT * (0.04 + w / 2))
        k_bar = always_redraw(kbar)

        self.play(FadeIn(strip), FadeIn(heading), FadeIn(brain), Create(wl), FadeIn(g_lab), FadeIn(g_box),
                  run_time=1.4)
        self.add(g_num, g_bar)
        self.wait(0.1)

        self.at("They are small")
        kdot = Dot([1.2, ROW, 0], radius=0.17, color=GREEN)
        klab = T("ketone body", 26, GREEN).move_to([1.2, ROW + 0.55, 0])
        self.play(FadeIn(kdot, scale=0.5), FadeIn(klab), run_time=0.5)
        self.at("water soluble")
        sol = T("small, water-soluble", 24, GREEN).move_to([1.2, ROW - 0.6, 0])
        self.play(FadeIn(sol), run_time=0.5)
        self.at("they cross into the brain")
        self.play(FadeOut(klab), FadeOut(sol), kdot.animate.move_to([BRAIN_X - 0.9, ROW, 0]), run_time=0.9)
        self.play(FadeOut(kdot, scale=0.3), brain[0].animate.set_stroke(GREEN, 6), run_time=0.4)
        self.play(brain[0].animate.set_stroke(BRAIN, 3.5), run_time=0.3)

        # the liver makes them
        self.at("the liver converts")
        liver_r = RoundedRectangle(corner_radius=0.16, width=6.4, height=2.3, stroke_color=GREY, stroke_width=3,
                                   fill_color=GREY, fill_opacity=0.07).move_to([-1.2, ROW, 0])
        liver_l = T("liver", 28, TEXT).move_to(liver_r.get_corner(UL) + RIGHT * 0.65 + DOWN * 0.3)
        self.play(FadeIn(liver_r), FadeIn(liver_l), run_time=0.7)
        self.at("fatty acid derived")
        fa = chip("fatty acids", TEAL_FA, size=24).move_to([-2.9, ROW + 2.05, 0])
        ac = chip("acetyl-CoA", TEAL_FA, size=24).move_to([-2.9, ROW, 0])
        a1 = arr([-2.9, ROW + 1.7, 0], [-2.9, ROW + 0.45, 0], TEAL_FA)
        self.play(FadeIn(fa, shift=DOWN * 0.1), GrowArrow(a1), FadeIn(ac), run_time=0.9)
        self.at("into ketone bodies")
        kb = chip("ketone bodies", GREEN, size=24).move_to([-0.1, ROW, 0])
        a2 = arr([-1.75, ROW, 0], [-1.35, ROW, 0], TEAL_FA, w=5, tip=0.15)
        self.play(GrowArrow(a2), FadeIn(kb), run_time=0.8)
        self.at("and exports them")
        ex = arr([1.35, ROW, 0], [WALL_X - 0.1, ROW, 0], GREEN, w=6)
        self.play(GrowArrow(ex), run_time=0.5)
        exl = Line([1.4, ROW, 0], [BRAIN_X - 1.05, ROW, 0])
        dd = [Dot(exl.get_start(), radius=0.12, color=GREEN) for _ in range(3)]
        self.add(*dd)
        self.play(LaggedStart(*[MoveAlongPath(d, exl, rate_func=linear) for d in dd], lag_ratio=0.3), run_time=1.5)
        self.play(*[FadeOut(d, scale=0.4) for d in dd], run_time=0.2)

        # the brain adapts
        self.at("the brain adapts")
        self.play(FadeIn(k_lab), FadeIn(k_box), FadeIn(k_bar), kv.animate.set_value(0.6), run_time=1.5)
        self.at("cutting its glucose")
        self.play(gv.animate.set_value(40.0), run_time=2.2)

        # protein sparing
        self.at("protein sparing effect")
        self.play(*[FadeOut(m) for m in (liver_r, liver_l, fa, ac, a1, a2, kb, ex)], run_time=0.5)
        cap = T("muscle protein used to make glucose", 24, RED).move_to([-2.75, 2.3, 0])
        blocksA, outA = pile([-4.3, 0.75, 0])
        blocksB, outB = pile([-1.2, 0.75, 0])
        la = VGroup(T("glucose only", 24, TEXT), M("120 g/day", 24, YELLOW)).arrange(DOWN, buff=0.08
                                                                                  ).move_to([-4.3, -0.85, 0])
        lb = VGroup(T("with ketone bodies", 24, GREEN), M("40 g/day", 24, YELLOW)).arrange(DOWN, buff=0.08
                                                                                        ).move_to([-1.2, -0.85, 0])
        self.play(FadeIn(cap), FadeIn(blocksA), FadeIn(outA), FadeIn(blocksB), FadeIn(outB), FadeIn(la),
                  FadeIn(lb), run_time=0.6)
        self.at("decides whether")
        drainA = [blocksA[i] for i in range(len(blocksA) - 1, -1, -1)]
        drainB = [blocksB[i] for i in range(len(blocksB) - 1, len(blocksB) - 5, -1)]
        self.play(LaggedStart(*[FadeOut(b, scale=0.3) for b in drainA], lag_ratio=0.12),
                  LaggedStart(*[FadeOut(b, scale=0.3) for b in drainB], lag_ratio=0.4), run_time=2.0)
        self.play(outB.animate.set_stroke(GREEN, 4), run_time=0.5)
        self.finish()


# ---------------------------------------------------------------------------------------------
class S06Export(SpokenScene):
    """Liver makes ketone bodies but lacks SCOT, so everything is exported."""

    def construct(self):
        strip = make_strip(active=(3,))
        cont = RoundedRectangle(corner_radius=0.2, width=5.4, height=4.7, stroke_color=GREY, stroke_width=3,
                                fill_color=GREY, fill_opacity=0.07).move_to([-3.3, 0.45, 0])
        liver_l = T("liver", 30, TEXT).move_to(cont.get_corner(UL) + RIGHT * 0.7 + DOWN * 0.35)
        kchip = chip("ketone bodies", GREEN, size=26).move_to([-3.3, 1.75, 0])

        self.play(FadeIn(strip), FadeIn(cont), FadeIn(liver_l), run_time=0.6)
        self.at("ketone bodies")
        self.play(FadeIn(kchip, scale=0.8), run_time=0.6)

        self.at("cannot use them")
        aa = chip("acetoacetate", GREEN, size=24).move_to([-3.3, 0.55, 0])
        down = arr([-3.3, 0.18, 0], [-3.3, -0.35, 0], GREY, w=4, tip=0.16)
        coa = chip("acetoacetyl-CoA", GREY, size=24).move_to([-3.3, -0.85, 0])
        self.play(FadeIn(aa), GrowArrow(down), FadeIn(coa), run_time=0.9)
        self.at("It lacks")
        sc = T("SCOT", 28, RED, weight=BOLD).move_to([-2.35, -0.08, 0])
        xm = xmark([-3.3, -0.08, 0], 0.17)
        self.play(FadeIn(sc), Create(xm), run_time=0.6)
        self.at("the enzyme that reactivates")
        self.play(Indicate(sc, scale_factor=1.2, color=RED), run_time=0.7)
        self.at("so it can be burned")
        bl = T("could then be burned", 22, GREY).move_to([-3.3, -1.45, 0])
        self.play(FadeIn(bl), run_time=0.5)

        self.at("everything it produces")
        self.play(Indicate(kchip, scale_factor=1.12, color=GREEN), run_time=0.9)
        self.at("shipped out")
        brain = organ("brain", [4.1, 1.9, 0], 1.9, label_color=BRAIN, color=BRAIN)
        heart = organ("heart", [4.1, 0.4, 0], 1.9)
        muscle = organ("muscle", [4.1, -1.1, 0], 1.9)
        ends = [(2.95, 1.9), (2.95, 0.5), (2.95, -1.0)]
        arrows = [arr([-1.95, 1.75, 0], [e[0], e[1], 0], GREEN, w=5) for e in ends]
        self.at("to the brain")
        self.play(FadeIn(brain), GrowArrow(arrows[0]), run_time=0.5)
        self.at("heart")
        self.play(FadeIn(heart), GrowArrow(arrows[1]), run_time=0.5)
        self.at("and muscle")
        self.play(FadeIn(muscle), GrowArrow(arrows[2]), run_time=0.5)
        self.at("export business")
        ds = []
        for a in arrows:
            l = Line(a.get_start(), a.get_end())
            d = Dot(l.get_start(), radius=0.1, color=GREEN)
            ds.append((d, l))
        self.add(*[d for d, _ in ds])
        self.play(*[MoveAlongPath(d, l, rate_func=linear) for d, l in ds], run_time=1.0)
        self.play(*[FadeOut(d, scale=0.4) for d, _ in ds], run_time=0.2)
        self.finish()


# ---------------------------------------------------------------------------------------------
class S07End(EndCard):
    LINE = "Ketone bodies let the brain run while muscle is spared."
