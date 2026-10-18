"""Drift, gene flow and competing explanations (Biochemistrypedia explainer)

COLOR MAP (one color per concept, whole video)
  BLUE   = allele A (the allele whose frequency we follow); also the resident population's frequency
  YELLOW = the other allele (B)
  PURPLE = drift: chance sampling and the scatter it makes
  ORANGE = gene flow: migrants and the frequency shift they cause
  GREEN  = selection (a consistent shift, carriers doing better)
  TEXT   = the expected / pooled-mean level (no push either way)
  GREY   = flies, boxes, axes, labels, de-emphasized
"""
import numpy as np
from bp_style import *  # noqa: F401,F403

PURPLE = "#B58CD9"
ORANGE = "#F29E4C"


# ------------------------------------------------------------------ helpers
def wf_lines(n, gens, copies, seed, p0=0.5, s=0.0):
    """Neutral (or weakly selected) Wright-Fisher style sampling, n lines, gens generations."""
    rng = np.random.default_rng(seed)
    out = np.zeros((n, gens + 1))
    out[:, 0] = p0
    for g in range(gens):
        p = out[:, g]
        q = p * (1 + s) / (1 + s * p) if s else p
        out[:, g + 1] = rng.binomial(copies, q) / copies
    return out


def line_through(pts, color, w=2, op=1.0):
    m = VMobject(stroke_color=color, stroke_width=w, stroke_opacity=op)
    m.set_points_as_corners([np.array(p, float) for p in pts])
    return m


def dot(r, color, op=0.9):
    return Circle(radius=r, stroke_color=color, stroke_width=2, fill_color=color, fill_opacity=op)


def freq_bar(p, w=4.0, h=0.32):
    b = Rectangle(width=max(w * p, 0.01), height=h, stroke_width=0, fill_color=BLUE, fill_opacity=0.9)
    y = Rectangle(width=max(w * (1 - p), 0.01), height=h, stroke_width=0, fill_color=YELLOW, fill_opacity=0.9)
    b.move_to(ORIGIN, aligned_edge=LEFT).shift(LEFT * w / 2)
    y.next_to(b, RIGHT, buff=0)
    return VGroup(b, y)


def make_cells(freqs, cols=11, cw=0.9, ch=0.34, px=1.0, py=0.46, cx=0.0, cy=-0.05):
    n = len(freqs)
    rows = (n + cols - 1) // cols
    cells = VGroup()
    for i, p in enumerate(freqs):
        r, c = divmod(i, cols)
        x = cx + (c - (cols - 1) / 2) * px
        y = cy + ((rows - 1) / 2 - r) * py
        a = Rectangle(width=max(cw * p, 0.004), height=ch, stroke_width=0, fill_color=BLUE, fill_opacity=0.9)
        b = Rectangle(width=max(cw * (1 - p), 0.004), height=ch, stroke_width=0, fill_color=YELLOW, fill_opacity=0.9)
        a.move_to([x - cw / 2, y, 0], aligned_edge=LEFT)
        b.next_to(a, RIGHT, buff=0)
        cells.add(VGroup(a, b))
    return cells


class S00Title(TitleCard):
    LESSON = "Drift, gene flow and competing explanations"
    TITLE = "Chance spreads, gene flow shifts"


# ------------------------------------------------------------------ scene 1
class S01Bottles(SpokenScene):
    def construct(self):
        lines = wf_lines(107, 19, 18, seed=11)
        end = lines[:, -1]
        # sixteen parents
        flies = VGroup(*[dot(0.24, GREY) for _ in range(16)]).arrange_in_grid(2, 8, buff=0.3).move_to([0, 0.4, 0])
        flies_lbl = T("16 parents each generation", 34, GREY).next_to(flies, DOWN, buff=0.5)
        self.at("kept 16 fruit")
        self.play(LaggedStart(*[FadeIn(f, scale=0.5) for f in flies], lag_ratio=0.06), FadeIn(flies_lbl), run_time=1.6)
        # 107 bottles
        start = make_cells([0.5] * 107)
        head = T("107 lines, each starting at 0.5", 30, TEXT).move_to([0, 3.15, 0])
        legend = VGroup(
            VGroup(Square(0.26, stroke_width=0, fill_color=BLUE, fill_opacity=0.9), T("allele A", 24, BLUE)).arrange(RIGHT, buff=0.15),
            VGroup(Square(0.26, stroke_width=0, fill_color=YELLOW, fill_opacity=0.9), T("allele B", 24, YELLOW)).arrange(RIGHT, buff=0.15),
        ).arrange(RIGHT, buff=0.8).move_to([0, -3.15, 0])
        self.at("He ran 107")
        self.play(FadeOut(flies), FadeOut(flies_lbl), run_time=0.5)
        self.play(LaggedStart(*[FadeIn(c, scale=0.6) for c in start], lag_ratio=0.012), FadeIn(legend), run_time=2.0)
        self.at("same frequency")
        self.play(FadeIn(head, shift=DOWN * 0.1), run_time=0.5)
        # nineteen generations
        endc = make_cells(list(end))
        head2 = T("after 19 generations (in this sketch)", 30, PURPLE).move_to([0, 3.15, 0])
        self.at("After 19 generations")
        self.play(ReplacementTransform(head, head2), Transform(start, endc), run_time=1.8)
        self.at("many bottles held only one allele")
        fixed = VGroup(*[SurroundingRectangle(start[i], buff=0.04, color=TEXT, stroke_width=3, corner_radius=0.03)
                         for i in range(107) if end[i] <= 0.0 or end[i] >= 1.0])
        self.play(Create(fixed), run_time=1.0)
        self.finish()


# ------------------------------------------------------------------ scene 2
class S02Poll(SpokenScene):
    def construct(self):
        rng = np.random.default_rng(3)
        boxL = RoundedRectangle(corner_radius=0.2, width=4.9, height=3.2, stroke_color=GREY, stroke_width=3).move_to([-3.4, 0.7, 0])
        boxR = RoundedRectangle(corner_radius=0.2, width=4.9, height=3.2, stroke_color=GREY, stroke_width=3).move_to([3.4, 0.7, 0])
        cols = [BLUE] * 36 + [YELLOW] * 24
        rng.shuffle(cols)
        pool = VGroup(*[dot(0.15, c) for c in cols]).arrange_in_grid(6, 10, buff=0.12).move_to(boxL)
        pool.scale_to_fit_width(4.4).move_to(boxL)
        lblL = T("the true vote", 30, TEXT).next_to(boxL, UP, buff=0.25)
        lblR = T("a poll of 20", 30, TEXT).next_to(boxR, UP, buff=0.25)
        barL = freq_bar(0.6, 4.4).next_to(boxL, DOWN, buff=0.35)
        self.at("Think of an election poll")
        self.play(Create(boxL), FadeIn(lblL), run_time=0.5)
        self.play(LaggedStart(*[FadeIn(d, scale=0.5) for d in pool], lag_ratio=0.01), FadeIn(barL), run_time=1.2)
        # draw 20: 8 blue, 12 yellow
        bi = [i for i, c in enumerate(cols) if c == BLUE]
        yi = [i for i, c in enumerate(cols) if c == YELLOW]
        pick = list(rng.choice(bi, 8, replace=False)) + list(rng.choice(yi, 12, replace=False))
        rng.shuffle(pick)
        copies = VGroup(*[pool[i].copy() for i in pick])
        targets = VGroup(*[dot(0.17, cols[i]) for i in pick]).arrange_in_grid(4, 5, buff=0.2).move_to(boxR)
        barR = freq_bar(0.4, 4.4).next_to(boxR, DOWN, buff=0.35)
        self.at("Ask 20 people")
        self.play(Create(boxR), FadeIn(lblR), *[Indicate(pool[i], color=TEXT, scale_factor=1.5) for i in pick], run_time=0.9)
        self.play(*[ReplacementTransform(copies[k], targets[k]) for k in range(20)], run_time=1.6)
        self.play(FadeIn(barR), run_time=0.5)
        self.at("just small")
        self.play(Indicate(VGroup(boxR, targets), color=TEXT, scale_factor=1.04), run_time=0.8)
        self.at("Each generation is a poll")
        lblL2 = T("parents' gene copies", 30, TEXT).move_to(lblL)
        lblR2 = T("offspring's gene copies", 30, TEXT).move_to(lblR)
        self.play(Transform(lblL, lblL2), Transform(lblR, lblR2), run_time=0.8)
        self.at("random sample")
        self.play(*[Indicate(t, color=PURPLE, scale_factor=1.35) for t in targets], run_time=0.9)
        self.at("genetic drift")
        drift_lbl = T("chance change: drift", 32, PURPLE, weight=BOLD).move_to([0, -2.1, 0])
        gap = Arrow(barL.get_right() + DOWN * 0.0, barR.get_left(), color=PURPLE, buff=0.15, stroke_width=6)
        self.play(GrowArrow(gap), FadeIn(drift_lbl), run_time=0.8)
        self.at("no difference in fitness")
        chipf = chip("no difference in fitness needed", GREY, size=28).move_to([0, -3.05, 0])
        self.play(FadeIn(chipf, shift=UP * 0.15), run_time=0.6)
        self.finish()


# ------------------------------------------------------------------ scene 3
class S03Flow(SpokenScene):
    def construct(self):
        fx = lambda f: -5.0 + 10.0 * f
        y0 = 0.1
        axis = Line([fx(0), y0, 0], [fx(1), y0, 0], color=GREY, stroke_width=4)
        ticks = VGroup()
        for f in (0, 0.5, 1):
            ticks.add(Line([fx(f), y0 - 0.12, 0], [fx(f), y0 + 0.12, 0], color=GREY, stroke_width=4))
            ticks.add(M(f"{f:g}", 24, GREY).move_to([fx(f), y0 - 0.45, 0]))
        axlbl = T("frequency of allele A", 24, GREY).move_to([0, y0 - 0.95, 0])
        note = T("illustrative numbers", 22, GREY).move_to([0, 3.3, 0])
        self.at("Gene flow is the movement")
        self.play(Create(axis), FadeIn(ticks), FadeIn(axlbl), FadeIn(note), run_time=1.0)
        res = dot(0.26, BLUE, 1.0).move_to([fx(0.6), y0, 0])
        res_l = T("residents 0.6", 28, BLUE).next_to(res, UP, buff=0.5)
        imm = dot(0.26, ORANGE, 1.0).move_to([fx(0.2), y0, 0])
        imm_l = T("immigrants 0.2", 28, ORANGE).next_to(imm, UP, buff=0.5)
        self.at("pulls their frequencies")
        pull = Arrow(imm.get_right(), res.get_left(), color=ORANGE, buff=0.12, stroke_width=6)
        self.play(FadeIn(res, scale=0.5), FadeIn(imm, scale=0.5), run_time=0.6)
        self.play(GrowArrow(pull), run_time=0.7)
        self.at("residents carry")
        self.play(FadeIn(res_l), run_time=0.4)
        self.at("and immigrants")
        self.play(FadeIn(imm_l), run_time=0.4)
        self.at("breeding pool")
        pool_bar = VGroup(
            Rectangle(width=4.5, height=0.34, stroke_width=0, fill_color=BLUE, fill_opacity=0.85),
            Rectangle(width=0.5, height=0.34, stroke_width=0, fill_color=ORANGE, fill_opacity=0.95)).arrange(RIGHT, buff=0)
        pool_bar.move_to([0, 1.95, 0])
        pool_l = T("breeding pool: 0.90 residents, 0.10 immigrants", 26, TEXT).next_to(pool_bar, UP, buff=0.18)
        self.play(FadeIn(pool_bar), FadeIn(pool_l), run_time=0.7)
        self.at("mixed frequency")
        eq = M("0.90 x 0.60 + 0.10 x 0.20 = 0.56", 30, TEXT).move_to([0, -2.1, 0])
        ghost = DashedLine([fx(0.6), y0 - 0.34, 0], [fx(0.6), y0 + 0.34, 0], color=GREY, stroke_width=3)
        res_l2 = T("after migration 0.56", 28, BLUE).next_to([fx(0.56), y0, 0], UP, buff=0.5)
        self.play(ReplacementTransform(res_l, res_l2), FadeIn(eq), FadeIn(ghost), res.animate.move_to([fx(0.56), y0, 0]),
                  FadeOut(pull), run_time=1.4)
        self.at("That drop")
        brace_l = T("-0.04", 30, ORANGE, weight=BOLD).move_to([fx(0.64), y0 - 0.75, 0])
        shift_arrow = Arrow([fx(0.6), y0 - 0.55, 0], [fx(0.56), y0 - 0.55, 0], color=ORANGE, buff=0, stroke_width=6, tip_length=0.18)
        self.play(GrowArrow(shift_arrow), FadeIn(brace_l.shift(DOWN * 0.0)), FadeOut(axlbl), run_time=0.7)
        self.at("same way every time")
        again = T("same result every time", 30, ORANGE).move_to([0, -3.1, 0])
        self.play(FadeIn(again), run_time=0.4)
        for _ in range(2):
            self.play(res.animate.move_to([fx(0.6), y0, 0]), run_time=0.35)
            self.play(res.animate.move_to([fx(0.56), y0, 0]), run_time=0.35)
        self.at("helps or harms")
        c1 = chip("helps", ORANGE, size=30).move_to([-2.0, -3.1, 0])
        c2 = chip("harms", ORANGE, size=30).move_to([2.0, -3.1, 0])
        self.play(FadeOut(again), FadeIn(c1, shift=UP * 0.1), FadeIn(c2, shift=UP * 0.1), run_time=0.7)
        self.finish()


# ------------------------------------------------------------------ scene 4
class S04Scatter(SpokenScene):
    def construct(self):
        rng = np.random.default_rng(5)
        lo, hi = 0.2, 0.9
        fx = lambda f: -5.5 + (f - lo) / (hi - lo) * 11.0
        ya = -2.4
        axis = Line([fx(lo), ya, 0], [fx(hi), ya, 0], color=GREY, stroke_width=4)
        ticks = VGroup()
        for f in (0.3, 0.5, 0.7, 0.9):
            ticks.add(Line([fx(f), ya - 0.1, 0], [fx(f), ya + 0.1, 0], color=GREY, stroke_width=3))
            ticks.add(M(f"{f:g}", 22, GREY).move_to([fx(f), ya - 0.4, 0]))
        sketch = T("in this sketch: simulated draws", 22, GREY).move_to([0, 3.35, 0])
        self.at("Now sample")
        self.play(Create(axis), FadeIn(ticks), FadeIn(sketch), run_time=0.9)

        def strip(n, y, col):
            vals = np.clip(rng.binomial(n, 0.56, 45) / n, lo + 0.01, hi - 0.01)
            ds = VGroup(*[dot(0.13, col, 0.85).move_to([fx(v), y + rng.uniform(-0.3, 0.3), 0]) for v in vals])
            return ds

        s200 = strip(200, 1.2, PURPLE)
        l200 = T("200 gene copies drawn", 28, PURPLE).move_to([-3.6, 2.1, 0])
        self.at("drawing 200")
        self.play(FadeIn(l200), LaggedStart(*[FadeIn(d, scale=0.3) for d in s200], lag_ratio=0.03), run_time=1.8)
        self.at("expected frequency")
        ex = DashedLine([fx(0.56), 2.5, 0], [fx(0.56), ya, 0], color=TEXT, stroke_width=3)
        ex_l = T("expected 0.56", 26, TEXT).next_to(ex, UP, buff=0.08)
        self.play(Create(ex), FadeIn(ex_l), run_time=0.8)
        self.at("scatter around it")
        b1 = VGroup(Line([fx(0.525), 0.45, 0], [fx(0.595), 0.45, 0], color=PURPLE, stroke_width=5),
                    Line([fx(0.525), 0.37, 0], [fx(0.525), 0.53, 0], color=PURPLE, stroke_width=5),
                    Line([fx(0.595), 0.37, 0], [fx(0.595), 0.53, 0], color=PURPLE, stroke_width=5))
        b1_l = T("about 3.5 points", 26, PURPLE).next_to(b1, RIGHT, buff=0.3)
        self.play(Create(b1), FadeIn(b1_l), run_time=0.8)
        s20 = strip(20, -0.75, PURPLE)
        l20 = T("20 gene copies drawn", 28, PURPLE).move_to([-3.6, 0.0, 0])
        self.at("only 20 copies")
        self.play(FadeIn(l20), LaggedStart(*[FadeIn(d, scale=0.3) for d in s20], lag_ratio=0.03), run_time=1.6)
        self.at("11 points")
        b2 = VGroup(Line([fx(0.449), -1.95, 0], [fx(0.671), -1.95, 0], color=PURPLE, stroke_width=5),
                    Line([fx(0.449), -2.03, 0], [fx(0.449), -1.87, 0], color=PURPLE, stroke_width=5),
                    Line([fx(0.671), -2.03, 0], [fx(0.671), -1.87, 0], color=PURPLE, stroke_width=5))
        b2_l = T("about 11 points", 26, PURPLE).next_to(b2, RIGHT, buff=0.3)
        self.play(Create(b2), FadeIn(b2_l), run_time=0.8)
        self.at("Ten times fewer")
        rule = T("10 times fewer copies: about 3 times the scatter", 28, TEXT, weight=BOLD).move_to([0, -3.2, 0])
        self.play(FadeOut(VGroup(ticks[1], ticks[3], ticks[5], ticks[7])), FadeIn(rule), run_time=0.8)
        self.finish()


# ------------------------------------------------------------------ scene 5
class S05Lines(SpokenScene):
    def construct(self):
        gens = 19
        lines = wf_lines(107, gens, 18, seed=2)
        X0, X1, Y0, Y1 = -6.0, 1.6, -2.2, 2.2
        fx = lambda g: X0 + (X1 - X0) * g / gens
        fy = lambda p: Y0 + (Y1 - Y0) * p
        frame = VGroup(Line([X0, Y0, 0], [X1, Y0, 0], color=GREY, stroke_width=4),
                       Line([X0, Y0, 0], [X0, Y1, 0], color=GREY, stroke_width=4))
        ylab = VGroup(*[M(t, 22, GREY).move_to([X0 - 0.35, fy(float(t)), 0]) for t in ("0", "0.5", "1")])
        xlab = T("generation (0 to 19)", 24, GREY).move_to([(X0 + X1) / 2, Y0 - 0.45, 0])
        sketch = T("in this sketch: simulated lines", 22, GREY).move_to([(X0 + X1) / 2, 3.15, 0])
        self.at("Back to")
        self.play(Create(frame), FadeIn(ylab), FadeIn(xlab), FadeIn(sketch), run_time=0.9)
        allm = [line_through([[fx(g), fy(v), 0] for g, v in enumerate(l)], PURPLE, 1.6, 0.5) for l in lines]
        one = line_through([[fx(g), fy(v), 0] for g, v in enumerate(lines[0])], TEXT, 4, 1.0)
        self.at("Any one line")
        self.play(Create(one), run_time=1.4)
        self.at("Across 107 lines")
        self.play(one.animate.set_stroke(PURPLE, 1.6, 0.5), LaggedStart(*[Create(m) for m in allm], lag_ratio=0.02), run_time=3.0)
        mean = lines.mean(axis=0)
        meanline = line_through([[fx(g), fy(v), 0] for g, v in enumerate(mean)], TEXT, 6, 1.0)
        rc = 4.3
        c_spread = chip("spreads toward 0 and 1", PURPLE, size=26).move_to([rc, 1.4, 0])
        c_flat = chip("pooled mean: no shift", TEXT, size=26).move_to([rc, 0.2, 0])
        self.at("spread toward 0 and 1")
        self.play(FadeIn(c_spread, shift=LEFT * 0.2), run_time=0.6)
        self.at("no systematic change")
        self.play(Create(meanline), FadeIn(c_flat, shift=LEFT * 0.2), run_time=1.0)
        self.at("drift prediction")
        c_pred = chip("the drift prediction", PURPLE, size=28).move_to([rc, -1.3, 0])
        self.play(FadeIn(c_pred, scale=0.9), run_time=0.6)
        # effective size
        self.at("how large an ideal population")
        fade_items = VGroup(c_spread, c_flat, c_pred)
        sizes = [0.26, 0.15, 0.3, 0.12, 0.22, 0.32, 0.1, 0.2, 0.28, 0.14, 0.24, 0.12, 0.3, 0.18, 0.26, 0.1]
        flies = VGroup(*[dot(r, GREY) for r in sizes]).arrange_in_grid(2, 8, buff=0.12).move_to([rc, 1.5, 0])
        flies.scale_to_fit_width(3.9).move_to([rc, 1.7, 0])
        fl = T("16 breeding flies", 26, GREY).next_to(flies, DOWN, buff=0.2)
        self.play(FadeOut(fade_items), FadeIn(flies), FadeIn(fl), run_time=0.8)
        ideal = VGroup(*[dot(0.2, BLUE) for _ in range(9)]).arrange_in_grid(3, 3, buff=0.18).move_to([rc, -1.0, 0])
        il = T("ideal population: 9.0", 26, BLUE).next_to(ideal, DOWN, buff=0.2)
        self.at("mean answer was")
        self.play(FadeIn(ideal, scale=0.5), FadeIn(il), run_time=0.8)
        self.at("did not contribute equally")
        self.play(*[Indicate(d, color=TEXT, scale_factor=1.2) for d in flies], run_time=1.0)
        self.finish()


# ------------------------------------------------------------------ scene 6
class S06Test(SpokenScene):
    def construct(self):
        gens = 19
        # puzzle strip
        isl = VGroup(T("island", 28, TEXT), freq_bar(0.85, 2.6, 0.3)).arrange(RIGHT, buff=0.3)
        mai = VGroup(T("mainland", 28, TEXT), freq_bar(0.15, 2.6, 0.3)).arrange(RIGHT, buff=0.3)
        puzzle = VGroup(isl, mai).arrange(RIGHT, buff=1.0).move_to([0, 3.4, 0])
        sk = T("in this sketch", 22, GREY).move_to([0, 2.88, 0])
        self.at("Suppose an allele")
        self.play(FadeIn(puzzle, shift=DOWN * 0.15), run_time=1.0)
        self.play(FadeIn(sk), run_time=0.3)

        pw, ph = 3.9, 3.0
        cx = [-4.3, 0.0, 4.3]
        cy = 0.4

        def panel(i, col, title):
            x = cx[i]
            fr = VGroup(Line([x - pw / 2, cy - ph / 2, 0], [x + pw / 2, cy - ph / 2, 0], color=GREY, stroke_width=3),
                        Line([x - pw / 2, cy - ph / 2, 0], [x - pw / 2, cy + ph / 2, 0], color=GREY, stroke_width=3))
            t = chip(title, col, size=28).move_to([x, cy + ph / 2 + 0.55, 0])
            return fr, t

        mx = lambda i, g: cx[i] - pw / 2 + pw * g / gens
        my = lambda p: cy - ph / 2 + ph * p

        # drift panel
        fr0, t0 = panel(0, PURPLE, "Drift")
        d = wf_lines(8, gens, 18, seed=21)
        dl = VGroup(*[line_through([[mx(0, g), my(v), 0] for g, v in enumerate(l)], PURPLE, 2.5, 0.8) for l in d])
        dm = DashedLine([mx(0, 0), my(0.5), 0], [mx(0, gens), my(0.5), 0], color=TEXT, stroke_width=4)
        dc = T("scatter both ways,\nmean stays", 24, PURPLE).move_to([cx[0], cy - ph / 2 - 0.65, 0])
        self.at("Drift predicts")
        self.play(Create(fr0), FadeIn(t0), run_time=0.6)
        self.play(LaggedStart(*[Create(l) for l in dl], lag_ratio=0.1), Create(dm), run_time=2.0)
        self.play(FadeIn(dc), run_time=0.4)
        # selection panel
        fr1, t1 = panel(1, GREEN, "Selection")
        sl_ = wf_lines(8, gens, 40, seed=4, s=0.28)
        sl = VGroup(*[line_through([[mx(1, g), my(v), 0] for g, v in enumerate(l)], GREEN, 2.5, 0.8) for l in sl_])
        sc = T("same shift;\ncarriers do better", 24, GREEN).move_to([cx[1], cy - ph / 2 - 0.65, 0])
        self.at("Selection predicts")
        self.play(Create(fr1), FadeIn(t1), run_time=0.6)
        self.play(LaggedStart(*[Create(l) for l in sl], lag_ratio=0.1), run_time=2.0)
        self.play(FadeIn(sc), run_time=0.4)
        # gene flow panel
        fr2, t2 = panel(2, ORANGE, "Gene flow")
        src = [0.2] * 6 + [0.7] * 7 + [0.3] * 7
        p = 0.2
        f_pts, s_pts = [], []
        for g in range(gens + 1):
            f_pts.append([mx(2, g), my(p), 0])
            s_pts.append([mx(2, g), my(src[g]), 0])
            p = 0.6 * p + 0.4 * src[g]
        gsrc = line_through(s_pts, ORANGE, 3, 0.9)
        gsrc = DashedVMobject(gsrc, num_dashes=30)
        gfq = line_through(f_pts, BLUE, 4, 1.0)
        gc = T("tracks the amount\nand source of immigrants", 24, ORANGE).move_to([cx[2], cy - ph / 2 - 0.65, 0])
        self.at("Gene flow predicts")
        self.play(Create(fr2), FadeIn(t2), run_time=0.6)
        self.play(Create(gsrc), Create(gfq), run_time=2.0)
        self.play(FadeIn(gc), run_time=0.4)
        self.at("neutral null is a model")
        # tools
        c1 = chip("replicates", GREY, size=28)
        c2 = chip("neutral null", GREY, size=28)
        c3 = chip("independent fitness assay", GREY, size=28)
        VGroup(c1, c2, c3).arrange(RIGHT, buff=0.5).move_to([0, -3.1, 0])
        self.at("keep this rule")
        self.at("Use replicates")
        self.play(FadeIn(c1, shift=UP * 0.1), run_time=0.5)
        self.at("neutral null", nth=1)
        self.play(FadeIn(c2, shift=UP * 0.1), run_time=0.5)
        self.at("independent fitness assay")
        self.play(FadeIn(c3, shift=UP * 0.1), run_time=0.5)
        self.finish()


class S07End(EndCard):
    LINE = "Replicates, a neutral null and a fitness assay separate drift from selection."
