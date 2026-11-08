"""Count the dishes, not the cells: the experimental unit and N  (Biochemistrypedia explainer)

Timed to the SPOKEN words: every self.at("...") cue waits for that phrase in audio/words.json.

COLOR MAP (one color per concept, whole video)
  BLUE   = a cell (an observational unit), cell dots
  YELLOW = an EdU-positive cell
  GREEN  = the right unit: the dish / the independent run as N, and the analysis built on it
  RED    = the wrong unit: cells counted as N, and the shared oddity of one dish
  TEAL   = run 1,  PURPLE = run 2,  ORANGE = run 3   (a run keeps its colour in every scene)
  GREY   = dish outlines, axes, labels, de-emphasized
"""
import numpy as np
from bp_style import *  # noqa: F401,F403

PURPLE = "#B58CD9"
ORANGE = "#F29E4C"
RUNC = [TEAL, PURPLE, ORANGE]

# the lesson's worked data: (control, treated) % EdU+ per run, 200 cells per dish
CTRL = [20, 25, 15]
TRT = [34, 27, 28]
DIFF = [14, 2, 13]
RNG = np.random.default_rng(11)


# ---------------------------------------------------------------------------------------------
# helpers
# ---------------------------------------------------------------------------------------------
def grid_pts(cols, rows, sp, center):
    cx, cy = center
    pts = []
    for r in range(rows):
        for c in range(cols):
            pts.append(np.array([cx + (c - (cols - 1) / 2) * sp, cy + ((rows - 1) / 2 - r) * sp, 0]))
    return pts


def cell_dots(pts, color=BLUE, r=0.04, op=0.85):
    return VGroup(*[Dot(p, radius=r, color=color, fill_opacity=op, stroke_width=0) for p in pts])


def dish_box(w, h, center, color=GREY, fill=0.0, sw=3):
    return RoundedRectangle(corner_radius=0.25, width=w, height=h, stroke_color=color, stroke_width=sw,
                            fill_color=color, fill_opacity=fill).move_to([center[0], center[1], 0])


def arr(a, b, color=GREY, w=5, tip=0.22):
    return Arrow(a, b, buff=0.08, color=color, stroke_width=w, tip_length=tip,
                 max_tip_length_to_length_ratio=0.45, max_stroke_width_to_length_ratio=12)


def bracket(x0, x1, y, color, w=6, cap=0.14):
    return VGroup(Line([x0, y, 0], [x1, y, 0], color=color, stroke_width=w),
                  Line([x0, y - cap, 0], [x0, y + cap, 0], color=color, stroke_width=w),
                  Line([x1, y - cap, 0], [x1, y + cap, 0], color=color, stroke_width=w))


# number-line stage shared by scenes 4 and 5 (differences, in percentage points)
Y_AX, Y_DOT = -2.75, -2.3


def vx(v):
    return -5.0 + (v + 10) * 0.26


def axis_stage():
    line = Line([vx(-10), Y_AX, 0], [vx(30), Y_AX, 0], color=GREY, stroke_width=3)
    ticks = VGroup()
    for v in (-10, 0, 10, 20, 30):
        ticks.add(Line([vx(v), Y_AX - 0.08, 0], [vx(v), Y_AX + 0.08, 0], color=GREY, stroke_width=3))
        ticks.add(M(str(v).replace("-", "−"), 22, GREY).move_to([vx(v), Y_AX - 0.4, 0]))
    zero = DashedLine([vx(0), Y_AX, 0], [vx(0), 1.15, 0], color=GREY, stroke_width=2)
    title = T("treated minus control, points", 22, GREY).move_to([vx(10), Y_AX - 0.85, 0])
    return VGroup(line, ticks, zero, title)


def diff_dots():
    d = VGroup()
    for i, v in enumerate(DIFF):
        y = Y_DOT + (0.3 if i == 2 else 0.0)
        d.add(Dot([vx(v), y, 0], radius=0.12, color=RUNC[i], fill_opacity=1, stroke_width=0))
    return d


def mean_line():
    return Line([vx(9.67), Y_AX, 0], [vx(9.67), 1.15, 0], color=TEXT, stroke_width=3)


def ci_bar():
    return bracket(vx(-6.9), vx(26.2), 0.7, GREEN, w=8, cap=0.2)


class S00Title(TitleCard):
    LESSON = "Designing a cell biology experiment"
    TITLE = "Count the Dishes, Not the Cells"


# ---------------------------------------------------------------------------------------------
class S01Question(SpokenScene):
    """two dishes of 600 cells; p value; how many experiments? one; the shared dish carries its oddity to every cell."""

    def construct(self):
        pts = grid_pts(30, 20, 0.15, (0, 0))
        xs, y0 = -3.3, 0.6
        dS = dish_box(4.7, 3.3, (xs, y0))
        dU = dish_box(4.7, 3.3, (-xs, y0))
        cS = cell_dots([p + np.array([xs, y0, 0]) for p in pts])
        cU = cell_dots([p + np.array([-xs, y0, 0]) for p in pts])
        lS = T("stretched", 26, TEXT).move_to([xs, -1.45, 0])
        lU = T("unstretched", 26, TEXT).move_to([-xs, -1.45, 0])
        stretch = VGroup(arr([xs - 2.38, y0, 0], [xs - 2.9, y0, 0], TEXT, 6, 0.2), arr([xs + 2.38, y0, 0], [xs + 2.9, y0, 0], TEXT, 6, 0.2))
        self.at("A student images")
        self.play(FadeIn(dS), FadeIn(dU), FadeIn(lS), FadeIn(lU), run_time=0.8)
        self.play(FadeIn(cS), FadeIn(cU), FadeIn(stretch), run_time=1.4)
        n1 = T("600 cells", 24, BLUE).move_to([xs, -1.95, 0])
        n2 = T("600 cells", 24, BLUE).move_to([-xs, -1.95, 0])
        self.at("The student scores")
        self.play(FadeIn(n1), FadeIn(n2), run_time=0.5)
        pv = chip("p < 0.0001", GREY, size=32)
        pv.move_to([0, 3.0, 0])
        self.at("p value")
        self.play(FadeIn(pv, shift=DOWN * 0.15), run_time=0.5)
        q = T("How many experiments?", 40, TEXT).move_to([0, 3.0, 0])
        self.at("How many experiments")
        self.play(ReplacementTransform(pv, q), run_time=0.6)
        one = T("1 experiment", 44, GREEN, weight=BOLD).move_to([0, 3.0, 0])
        self.at("experiments is that One")
        self.play(ReplacementTransform(q, one), dS.animate.set_stroke(GREEN, 5), run_time=0.6)
        c1 = chip("same dish", GREY, size=26).move_to([-3.6, -3.0, 0])
        c2 = chip("same pipetting", GREY, size=26).move_to([0.1, -3.0, 0])
        c3 = chip("same afternoon", GREY, size=26).move_to([4.0, -3.0, 0])
        self.at("same dish")
        self.play(FadeIn(c1, shift=UP * 0.1), run_time=0.4)
        self.at("same pipetting")
        self.play(FadeIn(c2, shift=UP * 0.1), run_time=0.4)
        self.at("same afternoon")
        self.play(FadeIn(c3, shift=UP * 0.1), run_time=0.4)
        self.at("that dish was odd")
        self.play(dS.animate.set_fill(RED, 0.22).set_stroke(RED, 5), run_time=0.6)
        self.at("carry the oddity")
        self.play(cS.animate.set_color(RED), run_time=0.9)
        self.finish()


# ---------------------------------------------------------------------------------------------
class S02Unit(SpokenScene):
    """a dish is treated as a whole = experimental unit; cells are observational units; more cells, N stays 1."""

    def construct(self):
        pts = grid_pts(30, 20, 0.15, (0, 0))
        dx, dy = -3.3, 0.2
        order = RNG.permutation(600)
        allpts = [pts[i] + np.array([dx, dy, 0]) for i in order]
        d1 = cell_dots(allpts[:200])
        d2 = cell_dots(allpts[200:400])
        d3 = cell_dots(allpts[400:])
        dish = dish_box(4.7, 3.3, (dx, dy))
        drop = arr([dx, 3.4, 0], [dx, dy + 1.75, 0], TEXT, 7)
        tlab = T("treatment", 26, TEXT).next_to(drop, RIGHT, buff=0.2)
        self.at("Here is the rule")
        self.play(FadeIn(dish), FadeIn(d1), run_time=0.9)
        self.at("assign to a treatment")
        self.play(GrowArrow(drop), FadeIn(tlab), run_time=0.7)
        eu = T("experimental unit", 30, GREEN, weight=BOLD).move_to([3.9, 2.55, 0])
        self.at("experimental unit")
        self.play(dish.animate.set_stroke(GREEN, 6).set_fill(GREEN, 0.12), FadeIn(eu), run_time=0.6)
        chips = [chip("dish", GREEN, size=26), chip("stretch device", GREEN, size=26), chip("mouse", GREEN, size=26)]
        for c, y in zip(chips, (1.7, 0.95, 0.2)):
            c.move_to([3.9, y, 0])
        self.at("a dish")
        self.play(FadeIn(chips[0], shift=LEFT * 0.1), run_time=0.35)
        self.at("stretch device")
        self.play(FadeIn(chips[1], shift=LEFT * 0.1), run_time=0.35)
        self.at("a mouse")
        self.play(FadeIn(chips[2], shift=LEFT * 0.1), run_time=0.35)
        ou = T("observational unit", 30, BLUE, weight=BOLD).move_to([3.9, -0.85, 0])
        self.at("The thing you measure")
        self.play(FadeIn(ou), d1.animate.set_color(BLUE), run_time=0.5)
        cc = chip("cell", BLUE, size=26).move_to([3.9, -1.65, 0])
        self.at("It can be a cell")
        self.play(FadeIn(cc, shift=LEFT * 0.1), run_time=0.4)
        nchip = chip("N = 1", GREEN, size=40).move_to([dx, -2.75, 0])
        self.at("the sample size")
        self.play(FadeIn(nchip, scale=0.9), run_time=0.5)
        self.at("a whole well")
        self.play(Indicate(dish, color=GREEN, scale_factor=1.03), run_time=0.8)
        cnt = M("cells measured: 200", 26, BLUE).move_to([3.9, -2.65, 0])
        self.at("Measuring more cells")
        self.play(FadeIn(cnt), run_time=0.3)
        c400 = M("cells measured: 400", 26, BLUE).move_to(cnt)
        c600 = M("cells measured: 600", 26, BLUE).move_to(cnt)
        self.play(FadeIn(d2), Transform(cnt, c400), run_time=0.9)
        self.play(FadeIn(d3), Transform(cnt, c600), run_time=0.9)
        self.at("It adds no experimental units")
        self.play(Indicate(nchip, color=GREEN, scale_factor=1.15), run_time=0.9)
        self.finish()


# ---------------------------------------------------------------------------------------------
class S03Pooled(SpokenScene):
    """six dishes of 200 cells, EdU-positive cells lit, then every cell pooled and counted as N."""

    def construct(self):
        pts200 = grid_pts(20, 10, 0.15, (0, 0))
        colx = [-2.9, 0.75, 4.4]
        rowy = [1.85, -0.35]
        counts = [CTRL, TRT]
        boxes, dishes, lit_all = [], [[], []], VGroup()
        for r in (0, 1):
            for c in (0, 1, 2):
                ctr = (colx[c], rowy[r])
                boxes.append(dish_box(3.3, 1.8, ctr, RUNC[c], 0.0, 3))
                dots = cell_dots([p + np.array([ctr[0], ctr[1], 0]) for p in pts200], BLUE, 0.04, 0.8)
                dishes[r].append(dots)
                k = int(counts[r][c] * 200 / 100)
                for i in range(k):
                    lit_all.add(dots[i])
        tag = T("made-up data, invented for teaching", 24, GREY).move_to([0, -3.1, 0])
        self.at("made up data set")
        self.play(FadeIn(tag), run_time=0.5)
        rl = [T(f"run {i + 1}", 28, RUNC[i], weight=BOLD).move_to([colx[i], 3.1, 0]) for i in range(3)]
        self.at("Three independent runs")
        self.play(*[FadeIn(b) for b in boxes], *[FadeIn(d) for r in dishes for d in r], *[FadeIn(x) for x in rl], run_time=1.5)
        lc = T("control", 26, GREY).move_to([-5.55, rowy[0], 0])
        lt = T("treated", 26, GREY).move_to([-5.55, rowy[1], 0])
        self.at("one control dish")
        self.play(FadeIn(lc), run_time=0.4)
        self.at("one treated dish")
        self.play(FadeIn(lt), run_time=0.4)
        n200 = T("200 cells per dish", 26, BLUE).move_to([-3.4, -1.95, 0])
        self.at("Two hundred cells")
        self.play(FadeIn(n200), run_time=0.4)
        edu = T("EdU-positive cells", 26, YELLOW).move_to([3.2, -1.95, 0])
        self.at("scored in each dish")
        self.play(lit_all.animate.set_color(YELLOW), FadeIn(edu), run_time=1.0)
        self.at("thymidine")
        # ---- pool: every dot flows into one block per condition -------------------------------
        blk = grid_pts(30, 20, 0.15, (0, 0))
        tg = []
        for r, cx in ((0, -3.4), (1, 3.4)):
            src = VGroup(*[d for dd in dishes[r] for d in dd])
            order = RNG.permutation(600)
            tgt = VGroup(*[src[i].copy().move_to(blk[order[i]] + np.array([cx, 1.15, 0])) for i in range(600)])
            tg.append((src, tgt))
        hc = T("control", 28, TEXT).move_to([-3.4, 3.0, 0])
        ht = T("treated", 28, TEXT).move_to([3.4, 3.0, 0])
        self.at("Now pool the cells")
        self.play(*[FadeOut(x) for x in boxes], *[FadeOut(x) for x in rl], FadeOut(lc), FadeOut(lt), FadeOut(n200),
                  FadeOut(edu), FadeOut(tag), FadeIn(hc), FadeIn(ht),
                  Transform(tg[0][0], tg[0][1]), Transform(tg[1][0], tg[1][1]), run_time=1.5)
        rc = M("120 of 600 = 20.0%", 28, TEXT).move_to([-3.4, -0.75, 0])
        rt = M("178 of 600 = 29.7%", 28, TEXT).move_to([3.4, -0.75, 0])
        self.at("Control is")
        self.play(FadeIn(rc, shift=UP * 0.1), run_time=0.5)
        self.at("Treated is")
        self.play(FadeIn(rt, shift=UP * 0.1), run_time=0.5)
        asn = chip("every cell counted as N", RED, size=26).move_to([0, -1.6, 0])
        self.at("Treat each cell as independent")
        self.play(FadeIn(asn, shift=UP * 0.1), run_time=0.5)
        se = M("SE ≈ 2.5 points", 30, RED).move_to([0, -2.4, 0])
        self.at("standard error")
        self.play(FadeIn(se, shift=UP * 0.1), run_time=0.5)
        z = M("z ≈ 3.9", 30, RED).move_to([0, -3.05, 0])
        self.at("Then z is")
        self.play(FadeIn(z, shift=UP * 0.1), run_time=0.5)
        self.at("It looks decisive")
        self.play(Indicate(z, color=RED, scale_factor=1.2), run_time=0.8)
        self.finish()


# ---------------------------------------------------------------------------------------------
class S04Right(SpokenScene):
    """each run is one paired difference; mean; green runs-as-N bracket vs the red cells-as-N bracket; 95% interval."""

    def construct(self):
        head = chip("the dish is the unit", GREEN, size=30).move_to([0, 3.2, 0])
        stage = axis_stage()
        self.at("That analysis counted cells")
        self.play(FadeIn(stage), run_time=0.8)
        self.at("make the dish the unit")
        self.play(FadeIn(head, shift=DOWN * 0.1), run_time=0.5)
        chips = [chip(f"{TRT[i]} − {CTRL[i]}", RUNC[i], size=28).move_to([x, 2.2, 0]) for i, x in enumerate((-3.3, 0.0, 3.3))]
        self.at("Each run pairs")
        self.play(*[FadeIn(c, shift=DOWN * 0.1) for c in chips], run_time=0.7)
        dots = diff_dots()
        labs = VGroup(M("14", 24, RUNC[0]).move_to([vx(14) + 0.42, Y_DOT, 0]),
                      M("2", 24, RUNC[1]).move_to([vx(2), Y_DOT + 0.4, 0]),
                      M("13", 24, RUNC[2]).move_to([vx(13) - 0.42, Y_DOT + 0.3, 0]))
        self.at("The differences are")
        self.play(*[ReplacementTransform(c, d) for c, d in zip(chips, dots)], FadeOut(head), run_time=1.0)
        self.play(FadeIn(labs), run_time=0.5)
        ml = mean_line()
        mlab = M("mean 9.67", 26, TEXT).move_to([vx(9.67), 1.5, 0])
        self.at("The mean is")
        self.play(Create(ml), FadeIn(mlab), run_time=0.7)
        g = bracket(vx(9.67 - 3.84), vx(9.67 + 3.84), -0.35, GREEN)
        glab = T("runs as N: ±3.84", 24, GREEN).move_to([3.9, -0.35, 0])
        self.at("standard error of")
        self.play(Create(g), FadeIn(glab), run_time=0.8)
        r = bracket(vx(9.7 - 2.5), vx(9.7 + 2.5), -1.05, RED)
        rlab = T("cells as N: ±2.5", 24, RED).move_to([3.9, -1.05, 0])
        self.at("That is larger than")
        self.play(Create(r), FadeIn(rlab), run_time=0.8)
        ci = ci_bar()
        e1 = M("−6.9", 24, GREEN).move_to([vx(-6.9), 0.3, 0])
        e2 = M("26.2", 24, GREEN).move_to([vx(26.2), 0.3, 0])
        cl = T("95% interval", 26, GREEN).move_to([-2.9, 1.5, 0])
        self.at("interval runs from")
        self.play(Create(ci), FadeIn(cl), run_time=0.9)
        self.play(FadeIn(e1), FadeIn(e2), run_time=0.5)
        self.finish()


# ---------------------------------------------------------------------------------------------
class S05More(SpokenScene):
    """interval spans a small decrease to a large increase; p about 0.13 is not no effect; more cells help only a little, more runs do."""

    def construct(self):
        stage = axis_stage()
        dots = diff_dots()
        ml = mean_line()
        ci = ci_bar()
        e1 = M("−6.9", 24, GREEN).move_to([vx(-6.9), 0.3, 0])
        e2 = M("26.2", 24, GREEN).move_to([vx(26.2), 0.3, 0])
        self.add(stage, dots, ml, ci, e1, e2)
        sug = T("suggestive, not shown", 32, TEXT).move_to([0, 3.2, 0])
        self.at("suggestive")
        self.play(FadeIn(sug, shift=DOWN * 0.1), run_time=0.6)
        dec = T("small decrease", 26, TEXT).move_to([vx(-5) - 0.4, 1.75, 0])
        inc = T("large increase", 26, TEXT).move_to([vx(22), 1.75, 0])
        a1 = arr([vx(-6.9) + 0.1, 1.5, 0], [vx(-6.9) + 0.1, 1.15, 0], TEXT, 4, 0.18)
        a2 = arr([vx(26.2) - 0.1, 1.5, 0], [vx(26.2) - 0.1, 1.15, 0], TEXT, 4, 0.18)
        self.at("small decrease")
        self.play(FadeIn(dec), GrowArrow(a1), run_time=0.5)
        self.at("large increase")
        self.play(FadeIn(inc), GrowArrow(a2), run_time=0.5)
        p = chip("p ≈ 0.13", TEXT, size=30).move_to([-1.0, 2.5, 0])
        self.at("The p value")
        self.play(FadeIn(p, shift=DOWN * 0.1), run_time=0.5)
        ne = VGroup(M("≠", 34, TEXT), T("no effect", 30, TEXT)).arrange(RIGHT, buff=0.25).move_to([2.2, 2.5, 0])
        self.at("does not show")
        self.play(FadeIn(ne, shift=LEFT * 0.1), run_time=0.5)
        # ---- more cells per dish help only a little --------------------------------------------------
        fade = [sug, dec, inc, a1, a2, p, ne]
        dx, dy = -3.3, 2.2
        pts = grid_pts(40, 14, 0.07, (dx, dy))
        dish = dish_box(3.3, 1.35, (dx, dy), GREY)
        cells = cell_dots(pts, BLUE, 0.022, 0.8)
        lab = T("2,000 cells per dish", 26, BLUE).move_to([dx, 3.25, 0])
        nh = chip("helps only a little", RED, size=28).move_to([1.6, 2.2, 0])
        self.at("Scoring")
        self.play(*[FadeOut(x) for x in fade + [ml, ci, e1, e2]], FadeIn(dish), FadeIn(cells), FadeIn(lab), run_time=0.9)
        self.play(FadeIn(nh, shift=LEFT * 0.1), run_time=0.5)
        sp = bracket(vx(2), vx(14), -1.45, GREEN)
        splab = T("run-to-run variation", 26, GREEN).move_to([vx(8), -0.95, 0])
        self.at("run to run variation")
        self.play(Create(sp), FadeIn(splab), run_time=0.8)
        # ---- more independent runs ------------------------------------------------------------------
        solid = VGroup(*[RoundedRectangle(corner_radius=0.15, width=1.2, height=0.75, stroke_color=RUNC[i], stroke_width=4,
                                          fill_color=RUNC[i], fill_opacity=0.25) for i in range(3)])
        solid.arrange(RIGHT, buff=0.3)
        more = DashedVMobject(RoundedRectangle(corner_radius=0.15, width=3.2, height=0.75, stroke_color=GREEN, stroke_width=3))
        mt = T("more runs", 28, GREEN).move_to(more)
        ghosts = VGroup(more, mt)
        row = VGroup(solid, ghosts).arrange(RIGHT, buff=0.5).move_to([0, 2.4, 0])
        gl = VGroup()
        self.at("More independent runs")
        self.play(*[FadeOut(x) for x in (dish, cells, lab, nh)], FadeIn(solid), run_time=0.6)
        self.play(Create(more), FadeIn(mt), run_time=1.2)
        self.finish()


# ---------------------------------------------------------------------------------------------
class S06Superplot(SpokenScene):
    """a SuperPlot of the three runs: large run-mean symbols joined across conditions; run 2 is almost flat; N = 3 runs."""

    def construct(self):
        def py(p):
            return -2.4 + p * 0.125

        xc = {"c": -3.2, "t": 0.2}
        offs = [-0.5, 0.0, 0.5]
        ax = VGroup(Line([-4.9, py(0), 0], [1.6, py(0), 0], color=GREY, stroke_width=3),
                    Line([-4.9, py(0), 0], [-4.9, py(40), 0], color=GREY, stroke_width=3))
        for v in (0, 10, 20, 30, 40):
            ax.add(Line([-4.98, py(v), 0], [-4.82, py(v), 0], color=GREY, stroke_width=3))
            ax.add(M(str(v), 22, GREY).move_to([-5.45, py(v), 0]))
        ytitle = T("% EdU-positive", 22, GREY).rotate(PI / 2).move_to([-6.1, py(20), 0])
        lc = T("control", 26, TEXT).move_to([xc["c"], py(0) - 0.45, 0])
        lt = T("treated", 26, TEXT).move_to([xc["t"], py(0) - 0.45, 0])
        self.at("shows all this")
        self.play(FadeIn(ax), FadeIn(ytitle), FadeIn(lc), FadeIn(lt), run_time=1.0)
        syms, lines = [], []
        for i in range(3):
            a = Dot([xc["c"] + offs[i], py(CTRL[i]), 0], radius=0.2, color=RUNC[i], fill_opacity=1, stroke_width=0)
            b = Dot([xc["t"] + offs[i], py(TRT[i]), 0], radius=0.2, color=RUNC[i], fill_opacity=1, stroke_width=0)
            ln = Line(a.get_center(), b.get_center(), color=RUNC[i], stroke_width=4, stroke_opacity=0.8)
            syms.append((a, b))
            lines.append(ln)
        self.at("Each run's mean")
        self.play(*[FadeIn(a, scale=0.6) for a, b in syms], *[FadeIn(b, scale=0.6) for a, b in syms], run_time=0.9)
        leg = VGroup(*[VGroup(Dot(radius=0.14, color=RUNC[i], fill_opacity=1, stroke_width=0), T(f"run {i + 1}", 26, RUNC[i]))
                       .arrange(RIGHT, buff=0.25) for i in range(3)]).arrange(DOWN, buff=0.35, aligned_edge=LEFT).move_to([4.2, 1.3, 0])
        self.at("colored by run")
        self.play(FadeIn(leg), run_time=0.5)
        self.at("The comparison uses")
        self.play(*[Create(l) for l in lines], run_time=1.0)
        # reorder so dots sit above lines
        self.bring_to_front(*[m for pair in syms for m in pair])
        self.at("stands out at once")
        others = [syms[0][0], syms[0][1], syms[2][0], syms[2][1], lines[0], lines[2]]
        self.play(*[m.animate.set_opacity(0.3) for m in others], Indicate(lines[1], color=PURPLE, scale_factor=1.0), run_time=0.9)
        bm = T("barely moved the mean", 26, PURPLE).move_to([4.2, -0.6, 0])
        self.at("barely moved")
        self.play(FadeIn(bm, shift=LEFT * 0.1), run_time=0.5)
        self.at("Keep the rule")
        self.play(*[m.animate.set_opacity(1) for m in others], FadeOut(bm), run_time=0.6)
        n = chip("N = 3 runs", GREEN, size=40).move_to([4.2, -0.35, 0])
        self.at("N is the number")
        self.play(FadeIn(n, scale=0.9), run_time=0.6)
        nc = chip("not 600 cells", RED, size=30).move_to([4.2, -1.5, 0])
        self.at("not the number of cells")
        self.play(FadeIn(nc, shift=UP * 0.1), run_time=0.6)
        self.finish()


class S07End(EndCard):
    LINE = "Count independent runs, not cells."
