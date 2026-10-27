"""Exercise physiology: oxygen uptake is flow times extraction  (Biochemistrypedia explainer)

Timed to the SPOKEN words: every self.at("...") cue waits for that phrase in audio/words.json.

COLOR MAP (one color per concept, whole video)
  GREEN  = oxygen uptake (VO2), the AREA of the rectangle
  BLUE   = flow: cardiac output, the heart, blood delivered (the rectangle's WIDTH)
  ORANGE = extraction: arterial minus mixed-venous oxygen content (the rectangle's HEIGHT)
  PURPLE = muscle: what working muscle could accept
  YELLOW = the question and the ceiling
  RED    = a caution: "not settled", "did not test"
  GREY   = axes, structure, labels, the resting reference
All numbers are the lesson's own (illustrative unless the lesson says otherwise).
"""
import numpy as np
from bp_style import *  # noqa: F401,F403

PURPLE = "#B58CD9"
ORANGE = "#F29E4C"

# axes of the "Fick rectangle": width = cardiac output (L/min), height = extraction (mL O2 per L)
O1 = np.array([-4.8, -2.55, 0.0])
SX1, SY1 = 0.32, 0.0285


def arr(a, b, color=GREY, w=5, tip=0.2):
    return Arrow(a, b, buff=0.06, color=color, stroke_width=w, tip_length=tip,
                 max_tip_length_to_length_ratio=0.45, max_stroke_width_to_length_ratio=12)


def fick_axes(O, sx, sy, xmax=20.0, ymax=165.0, titles=True, size=22):
    """Two axes with ticks. Returns VGroup; .xt/.yt are the title labels."""
    xl = Line(O, O + RIGHT * xmax * sx, color=GREY, stroke_width=3)
    yl = Line(O, O + UP * ymax * sy, color=GREY, stroke_width=3)
    g = VGroup(xl, yl)
    for v in (5, 10, 15, 20):
        p = O + RIGHT * v * sx
        g.add(Line(p, p + DOWN * 0.1, color=GREY, stroke_width=3), T(str(v), size, GREY).next_to(p + DOWN * 0.1, DOWN, buff=0.08))
    for v in (50, 100, 150):
        p = O + UP * v * sy
        g.add(Line(p, p + LEFT * 0.1, color=GREY, stroke_width=3), T(str(v), size, GREY).next_to(p + LEFT * 0.1, LEFT, buff=0.08))
    xt = T("cardiac output (L/min)", 24, BLUE).move_to([O[0] + 10 * sx, O[1] - 0.78, 0])
    yt = T("extraction (mL O₂ per L)", 24, ORANGE).rotate(PI / 2).move_to([O[0] - 1.1, O[1] + 80 * sy, 0])
    g.xt, g.yt = xt, yt
    return g


def frect(O, sx, sy, q, e, color=GREEN, fill=0.35, sw=4):
    r = Rectangle(width=q * sx, height=e * sy, stroke_color=color, stroke_width=sw, fill_color=color, fill_opacity=fill)
    return r.move_to(O + np.array([q * sx / 2, e * sy / 2, 0]))


def xline(O, sx, q, color=BLUE, w=9):
    return Line(O, O + RIGHT * q * sx, color=color, stroke_width=w)


def yline(O, sy, e, color=ORANGE, w=9):
    return Line(O, O + UP * e * sy, color=color, stroke_width=w)


def eq_top(parts=5, size=34):
    """VO2 = cardiac output x extraction, in the concept colours (first `parts` pieces)."""
    pcs = [T("VO₂", size, GREEN, weight=BOLD), T("=", size), T("cardiac output", size, BLUE),
           T("×", size), T("extraction", size, ORANGE)][:parts]
    return VGroup(*pcs).arrange(RIGHT, buff=0.28).move_to([0, 3.05, 0])


def col(lines, x=2.0, y0=2.2, gap=0.62, max_w=4.2):
    """Right-hand column: list of (text, color[, size]) -> list of Mobjects, left aligned at x."""
    out = []
    for i, ln in enumerate(lines):
        txt, c = ln[0], ln[1]
        size = ln[2] if len(ln) > 2 else 24
        m = M(txt, size, c)
        fit(m, max_w=max_w)
        m.move_to([x, y0 - i * gap, 0]).align_to([x, 0, 0], LEFT)
        out.append(m)
    return out


class S00Title(TitleCard):
    LESSON = "Exercise: the whole body at work"
    TITLE = "Oxygen uptake is flow times extraction"


# ---------------------------------------------------------------------------------------------
class S01Ceiling(SpokenScene):
    def construct(self):
        base_y, x0, x1 = -2.55, -6.0, -0.7
        base = Line([x0, base_y, 0], [x1, base_y, 0], color=GREY, stroke_width=3)
        # bars: rest = 1 unit (0.4), maximal = 10 units (4.0)
        rest = Rectangle(width=1.4, height=0.4, stroke_color=GREEN, stroke_width=4, fill_color=GREEN, fill_opacity=0.35)
        rest.move_to([-4.6, base_y + 0.2, 0])
        mx = Rectangle(width=1.4, height=4.0, stroke_color=GREEN, stroke_width=4, fill_color=GREEN, fill_opacity=0.35)
        mx.move_to([-2.0, base_y + 2.0, 0])
        lb_rest = T("at rest", 24, GREY).next_to(base, DOWN, buff=0.18).set_x(-4.6)
        lb_max = T("maximal run", 24, GREY).next_to(base, DOWN, buff=0.18).set_x(-2.0)
        v_rest = T("about 250 mL/min", 24, GREEN).move_to([-4.3, base_y + 0.85, 0])
        v_max = T("10 or more times as much", 24, GREEN).move_to([-2.6, base_y + 4.55, 0])
        fit(v_max, max_w=4.6)
        self.add(base)
        self.at("at rest")
        self.play(GrowFromEdge(rest, DOWN), FadeIn(lb_rest), run_time=0.7)
        self.play(FadeIn(v_rest, shift=UP * 0.1), run_time=0.4)
        self.at("maximal run")
        self.play(FadeIn(lb_max), GrowFromEdge(mx, DOWN), run_time=1.6)
        self.at("or more times")
        self.play(FadeIn(v_max, shift=UP * 0.1), run_time=0.5)

        # the chain of links, top to bottom, in the lesson's order
        names = ["lungs", "heart", "blood", "capillaries", "mitochondrion"]
        ys = [2.75, 1.4, 0.05, -1.3, -2.65]
        chips = [chip(n, GREY, size=26).move_to([3.7, y, 0]) for n, y in zip(names, ys)]
        links = [arr(chips[i].get_bottom(), chips[i + 1].get_top(), GREY) for i in range(4)]
        cues = ["the lungs", "the heart", "the blood", "the capillaries", "before a"]
        for i, c in enumerate(cues):
            self.at(c)
            anims = [FadeIn(chips[i], shift=DOWN * 0.15)]
            if i > 0:
                anims.append(GrowArrow(links[i - 1]))
            self.play(*anims, run_time=0.45)
        # the question, drawn: a dashed ceiling over the tall bar and a question mark at every link
        ceil = DashedLine([-3.05, base_y + 4.0, 0], [0.1, base_y + 4.0, 0], color=YELLOW, stroke_width=5)
        ceil_lb = T("ceiling", 28, YELLOW, weight=BOLD).move_to([1.0, base_y + 4.0, 0])
        qs = [T("?", 40, YELLOW, weight=BOLD).move_to([c.get_right()[0] + 0.45, c.get_center()[1], 0]) for c in chips]
        self.at("which link")
        self.play(Create(ceil), FadeIn(ceil_lb), run_time=0.5)
        self.play(LaggedStart(*[FadeIn(q, scale=0.5) for q in qs], lag_ratio=0.15), run_time=0.9)
        self.play(LaggedStart(*[Indicate(c, color=YELLOW, scale_factor=1.08) for c in chips], lag_ratio=0.2), run_time=1.4)
        self.finish()


# ---------------------------------------------------------------------------------------------
class S02Fick(SpokenScene):
    def construct(self):
        O, sx, sy = O1, SX1, SY1
        ax = fick_axes(O, sx, sy)
        parts = eq_top(5)
        vo2, eq, co, times, ext = parts
        self.at("two factors")
        self.play(Create(VGroup(*[m for m in ax])), run_time=1.0)
        self.at("equals cardiac output")
        self.play(FadeIn(vo2), FadeIn(eq), FadeIn(co, shift=RIGHT * 0.2), FadeIn(ax.xt), run_time=0.8)
        self.at("extracted from each")
        self.play(FadeIn(times), FadeIn(ext, shift=LEFT * 0.2), FadeIn(ax.yt), run_time=0.8)
        # what extraction is
        r = col([("extraction = CaO₂ − CvO₂", ORANGE), ("(mL O₂ per L of blood)", GREY, 22)], y0=2.15, gap=0.5)
        r[0][-4:].set_color(ORANGE)
        self.at("arterial oxygen content")
        self.play(FadeIn(r[0], shift=LEFT * 0.2), run_time=0.6)
        self.at("oxygen content minus")
        self.play(Indicate(r[0], color=ORANGE, scale_factor=1.05), run_time=0.7)
        self.at("oxygen per")
        self.play(FadeIn(r[1]), Indicate(ax.yt, color=ORANGE, scale_factor=1.05), run_time=0.7)
        ill = T("illustrative numbers", 22, GREY).move_to([4.0, -3.05, 0])
        self.at("illustrative numbers")
        self.play(FadeIn(ill), run_time=0.5)
        rows = col([("200 − 150 = 50 mL/L", ORANGE), ("cardiac output 5.0 L/min", BLUE, 22), ("5.0 × 50 = 250 mL/min", GREEN)],
                   x=1.8, y0=0.95, gap=0.62, max_w=4.5)
        lq = xline(O, sx, 5.0)
        le = yline(O, sy, 50)
        rect = frect(O, sx, sy, 5.0, 50)
        area_lb = T("area = oxygen uptake", 24, GREEN).move_to([-1.3, O[1] + 25 * sy, 0])
        self.at("cardiac output is")
        self.play(Create(lq), FadeIn(rows[1], shift=LEFT * 0.2), run_time=0.7)
        self.at("and extraction is")
        self.play(Create(le), FadeIn(rows[0], shift=LEFT * 0.2), run_time=0.7)
        self.at("gives")
        self.play(FadeIn(rect), FadeIn(rows[2], shift=LEFT * 0.2), FadeIn(area_lb), run_time=0.9)
        self.play(Indicate(rect, color=GREEN, scale_factor=1.12), run_time=0.8)
        self.finish()


# ---------------------------------------------------------------------------------------------
class S03Max(SpokenScene):
    def construct(self):
        O, sx, sy = O1, SX1, SY1
        ax = fick_axes(O, sx, sy)
        eq = eq_top(5)
        ill = T("illustrative numbers", 22, GREY).move_to([4.0, -3.05, 0])
        # rebuild the end of the last scene: the resting rectangle, in the same place
        rest = frect(O, sx, sy, 5.0, 50)
        lq, le = xline(O, sx, 5.0), yline(O, sy, 50)
        self.add(ax, ax.xt, ax.yt, eq, ill, rest, lq, le)
        grow = frect(O, sx, sy, 5.0, 50, fill=0.3)           # the rectangle that will stretch
        grow_q, grow_e = xline(O, sx, 5.0), yline(O, sy, 50)
        out = Rectangle(width=5.0 * sx, height=50 * sy, stroke_color=TEXT, stroke_width=4, fill_opacity=0).move_to(rest)
        rest_lb = T("rest", 22, TEXT).move_to(rest)
        self.remove(rest, lq, le)
        self.add(grow, grow_q, grow_e, out, rest_lb)

        self.at("maximal exercise")
        self.play(Indicate(out, color=TEXT, scale_factor=1.1), run_time=0.8)
        rows = col([("195 beats/min", BLUE), ("× 100 mL/beat", BLUE), ("= 19.5 L/min", BLUE)], y0=2.2, gap=0.6)
        self.at("heart rate is")
        self.play(FadeIn(rows[0], shift=LEFT * 0.2), run_time=0.5)
        self.at("stroke volume is")
        self.play(FadeIn(rows[1], shift=LEFT * 0.2), run_time=0.5)
        self.at("cardiac output reaches")
        self.play(FadeIn(rows[2], shift=LEFT * 0.2),
                  Transform(grow, frect(O, sx, sy, 19.5, 50, fill=0.3)), Transform(grow_q, xline(O, sx, 19.5)), run_time=1.6)
        f1 = M("×3.9", 26, BLUE, weight=BOLD).next_to(rows[2], RIGHT, buff=0.25)
        self.at("rise of")
        self.play(FadeIn(f1, scale=1.3), run_time=0.5)
        rows2 = col([("CaO₂ 200 − CvO₂ 40", ORANGE), ("= 160 mL/L", ORANGE)], y0=0.35, gap=0.6)
        self.at("extraction rises")
        self.play(FadeIn(rows2[0], shift=LEFT * 0.2), FadeIn(rows2[1], shift=LEFT * 0.2),
                  Transform(grow, frect(O, sx, sy, 19.5, 160, fill=0.3)), Transform(grow_e, yline(O, sy, 160)), run_time=1.8)
        f2 = M("×3.2", 26, ORANGE, weight=BOLD).next_to(rows2[1], RIGHT, buff=0.25)
        self.at("rise of", nth=1)
        self.play(FadeIn(f2, scale=1.3), run_time=0.5)
        tot = col([("3.9 × 3.2 = 12.5", GREEN, 28), ("= 3,120 mL/min", GREEN, 28)], y0=-1.3, gap=0.65)
        big = T("oxygen uptake: 3,120 mL/min", 26, GREEN, weight=BOLD).move_to([O[0] + 19.5 * sx / 2 + 0.2, O[1] + 105 * sy, 0])
        self.at("together they make")
        self.play(FadeIn(tot[0], shift=LEFT * 0.2), FadeIn(tot[1], shift=LEFT * 0.2), FadeIn(big), run_time=0.9)
        self.play(Indicate(grow, color=GREEN, scale_factor=1.03), run_time=0.9)
        self.finish()


# ---------------------------------------------------------------------------------------------
class S04Leg(SpokenScene):
    def construct(self):
        q = T("Which factor sets the ceiling?", 34, YELLOW, font=TITLE_FONT).move_to([0, 3.0, 0])
        self.at("which factor")
        self.play(Write(q), run_time=1.2)
        # two legs as labelled blocks: one works, one rests
        work = RoundedRectangle(corner_radius=0.2, width=2.6, height=3.0, stroke_color=PURPLE, stroke_width=4,
                                fill_color=PURPLE, fill_opacity=0.3).move_to([-4.8, 0.6, 0])
        rest = RoundedRectangle(corner_radius=0.2, width=2.6, height=3.0, stroke_color=GREY, stroke_width=3,
                                fill_color=GREY, fill_opacity=0.15).move_to([-2.0, 0.6, 0])
        wl = T("working leg:\none quadriceps", 22, PURPLE).move_to(work)
        rl = T("other leg:\nat rest", 22, GREY).move_to(rest)
        subj = T("five healthy subjects", 24, TEXT).move_to([-3.4, 2.5, 0])
        self.at("had five healthy subjects")
        self.play(FadeIn(subj, shift=DOWN * 0.1), run_time=0.5)
        self.at("kick one leg")
        self.play(FadeIn(work), FadeIn(rest), FadeIn(wl), FadeIn(rl), run_time=0.8)
        self.play(work.animate.shift(UP * 0.12), run_time=0.25)
        self.play(work.animate.shift(DOWN * 0.12), run_time=0.25)
        self.at("one quadriceps")
        self.play(Indicate(wl, color=PURPLE, scale_factor=1.1), run_time=0.8)
        # flow out of the working leg, measured at the femoral vein
        vein = Rectangle(width=0.22, height=1.1, stroke_color=BLUE, stroke_width=3, fill_color=BLUE, fill_opacity=0.35).move_to([-4.8, -1.45, 0])
        flow_arrow = arr([-4.8, -1.15, 0], [-4.8, -2.1, 0], BLUE)
        vl = T("femoral vein: flow by\ncold-saline thermodilution", 22, BLUE).move_to([-2.5, -1.7, 0])
        self.at("flow to that leg")
        self.play(FadeIn(vein), GrowArrow(flow_arrow), FadeIn(vl), run_time=0.9)
        # the flow gauge rises with workload to the average 5.7 L/min
        gx, gy0, k = 1.2, -2.5, 0.5
        gb = Line([gx - 0.6, gy0, 0], [gx + 0.6, gy0, 0], color=GREY, stroke_width=3)
        gauge = Rectangle(width=1.0, height=0.05, stroke_color=BLUE, stroke_width=3, fill_color=BLUE, fill_opacity=0.4).move_to([gx, gy0 + 0.025, 0])
        gl = T("workload rises (10 to 60 W)", 22, GREY).move_to([gx, gy0 - 0.4, 0])
        g_top = Rectangle(width=1.0, height=5.7 * k, stroke_color=BLUE, stroke_width=3, fill_color=BLUE, fill_opacity=0.4).move_to([gx, gy0 + 5.7 * k / 2, 0])
        g_val = T("flow rose with\nworkload to an\naverage of 5.7 L/min", 22, BLUE, weight=BOLD).move_to([gx + 0.1, gy0 + 5.7 * k + 0.85, 0])
        wl_arrow = arr([gx - 0.95, gy0 + 0.3, 0], [gx - 0.95, gy0 + 5.7 * k - 0.2, 0], GREY)
        self.add(gb, gauge)
        self.play(FadeIn(gl), run_time=0.3)
        self.play(Transform(gauge, g_top), GrowArrow(wl_arrow), run_time=1.6)
        self.play(FadeIn(g_val, shift=UP * 0.1), run_time=0.5)
        # the estimate per kilogram
        est = VGroup(T("estimated maximal", 22, PURPLE), T("perfusion: about", 22, PURPLE),
                     T("2.5 L per kg of", 22, PURPLE), T("active muscle per min", 22, PURPLE)).arrange(DOWN, aligned_edge=LEFT, buff=0.14)
        est.move_to([4.6, 0.8, 0]).align_to([3.3, 0, 0], LEFT)
        self.at("maximal perfusion")
        self.play(FadeIn(est, shift=LEFT * 0.2), run_time=0.9)
        caution = chip("did not test\nwhole-body exercise", RED, size=24)
        caution.move_to([4.7, -1.5, 0])
        self.at("did not test")
        self.play(FadeIn(caution, shift=UP * 0.15), run_time=0.7)
        self.finish()


# ---------------------------------------------------------------------------------------------
class S05Argument(SpokenScene):
    def construct(self):
        k = 0.075           # bar height per L/min
        by = -2.5
        base = Line([-0.4, by, 0], [6.1, by, 0], color=GREY, stroke_width=3)
        self.add(base)
        # left column: the lesson's worked numbers
        left = col([("20 kg of muscle (made up)", PURPLE, 26), ("80% of 19.5 L/min (made up)", BLUE, 26), ("= 15.6 L/min reaches it", BLUE, 26)],
                   x=-6.2, y0=2.5, gap=0.62, max_w=5.6)
        self.at("running uses")
        self.play(FadeIn(left[0], shift=RIGHT * 0.2), run_time=0.6)
        self.at("the heart's")
        self.play(FadeIn(left[1], shift=RIGHT * 0.2), run_time=0.5)
        self.at("reaches it")
        self.play(FadeIn(left[2], shift=RIGHT * 0.2), run_time=0.5)
        heart = Rectangle(width=1.6, height=15.6 * k, stroke_color=BLUE, stroke_width=4, fill_color=BLUE, fill_opacity=0.35).move_to([4.6, by + 15.6 * k / 2, 0])
        h_lb = T("heart sends", 24, BLUE).move_to([4.6, by - 0.35, 0])
        h_val = T("15.6 L/min", 24, BLUE, weight=BOLD).move_to([4.6, by + 15.6 * k + 0.35, 0])
        mus = Rectangle(width=1.6, height=50 * k, stroke_color=PURPLE, stroke_width=4, fill_color=PURPLE, fill_opacity=0.35).move_to([1.5, by + 50 * k / 2, 0])
        m_lb = T("muscle could accept", 24, PURPLE).move_to([1.5, by - 0.35, 0])
        m_val = T("50 L/min", 24, PURPLE, weight=BOLD).move_to([1.5, by + 50 * k + 0.35, 0])
        calc = col([("2.5 L/kg/min (one-leg study)", PURPLE, 26), ("× 20 kg = 50 L/min", PURPLE, 26)], x=-6.2, y0=0.45, gap=0.62, max_w=5.6)
        self.at("one leg rate")
        self.play(FadeIn(calc[0], shift=RIGHT * 0.2), run_time=0.6)
        self.at("could accept")
        self.play(GrowFromEdge(mus, DOWN), FadeIn(m_lb), FadeIn(calc[1], shift=RIGHT * 0.2), run_time=1.4)
        self.play(FadeIn(m_val, shift=UP * 0.1), run_time=0.4)
        self.at("heart sends")
        self.play(GrowFromEdge(heart, DOWN), FadeIn(h_lb), run_time=1.0)
        self.play(FadeIn(h_val, shift=UP * 0.1), run_time=0.4)
        # three times
        gap = DoubleArrow([3.05, by + 15.6 * k, 0], [3.05, by + 50 * k, 0], color=YELLOW, stroke_width=5, tip_length=0.2, buff=0)
        ratio = T("3.2 times", 30, YELLOW, weight=BOLD).move_to([4.7, 0.75, 0])
        ratio2 = T("what the heart sends", 24, YELLOW).move_to([4.7, 0.25, 0])
        self.at("three times")
        self.play(GrowArrow(gap), FadeIn(ratio), FadeIn(ratio2), run_time=0.9)
        ceil = DashedLine([0.4, by + 15.6 * k, 0], [6.0, by + 15.6 * k, 0], color=YELLOW, stroke_width=5)
        concl = chip("in this example the\nheart sets the ceiling", YELLOW, size=24)
        concl.move_to([-3.9, -1.55, 0])
        self.at("this example")
        self.play(Create(ceil), FadeIn(concl, shift=UP * 0.15), run_time=0.9)
        self.play(Indicate(concl, color=YELLOW, scale_factor=1.05), run_time=0.8)
        self.finish()


# ---------------------------------------------------------------------------------------------
class S06Rule(SpokenScene):
    def construct(self):
        O = np.array([-5.0, -2.55, 0.0]); sx, sy = 0.27, 0.023
        ax = fick_axes(O, sx, sy, xmax=20.0, ymax=165.0)
        eq = eq_top(5)
        rect = frect(O, sx, sy, 19.5, 160)
        self.add(ax, ax.xt, ax.yt, eq)
        self.play(FadeIn(rect), run_time=0.5)
        lq = xline(O, sx, 19.5, w=18)
        lbl = VGroup(T("oxygen delivery (cardiac output × arterial O₂ content),", 22, BLUE),
                     T("mainly cardiac output", 22, BLUE)).arrange(DOWN, buff=0.08).move_to([O[0] + 10 * sx + 0.15, 2.05, 0])
        fit(lbl, max_w=6.4)
        self.at("healthy people doing")
        self.play(Create(lq), run_time=0.7)
        self.at("oxygen delivery")
        self.play(Indicate(eq[2], color=BLUE, scale_factor=1.12), FadeIn(lbl), run_time=0.9)
        a = chip("16 untrained men,\n6 weeks of training", GREY, size=24)
        b = chip("red-cell volume back to baseline:\npeak VO₂ back to pretraining level", BLUE, size=24)
        b2 = chip("removing blood also lowers blood\nvolume and preload, so it cannot\nseparate capacity from volume", RED, size=24)
        c = chip("a later study, 12 untrained adults,\n10 weeks: gain preserved, not settled", RED, size=24)
        for m, y in ((a, 2.05), (b, 0.85), (b2, -0.95), (c, -2.45)):
            fit(m, max_w=5.5)
            m.move_to([3.55, y, 0])
        tag = T("authors' report", 22, GREY).next_to(b, DOWN, buff=0.1)
        self.at("one training")
        self.play(FadeIn(a, shift=LEFT * 0.2), run_time=0.7)
        self.at("authors report")
        self.play(FadeIn(b, shift=LEFT * 0.2), FadeIn(tag), run_time=0.8)
        self.at("removing blood")
        self.play(FadeIn(b2, shift=LEFT * 0.2), run_time=0.8)
        self.at("later study")
        self.play(FadeIn(c, shift=LEFT * 0.2), run_time=0.7)
        self.at("not settled")
        self.play(Indicate(c, color=RED, scale_factor=1.04), run_time=0.8)
        self.at("oxygen uptake is")
        self.play(FadeOut(a), FadeOut(b), FadeOut(b2), FadeOut(c), FadeOut(tag), run_time=0.6)
        rule = T("flow × extraction", 42, TEXT, font=TITLE_FONT).move_to([3.5, 0.9, 0])
        self.at("uptake is flow")
        self.play(Write(rule), run_time=1.0)
        pts = T("in whole-body exercise at sea level,\nthe evidence points mainly to flow", 26, BLUE).move_to([3.5, -0.3, 0])
        self.at("points mainly")
        self.play(FadeIn(pts, shift=UP * 0.1), Indicate(lq, color=BLUE), Indicate(eq[2], color=BLUE, scale_factor=1.12), run_time=0.9)
        self.finish()


class S07End(EndCard):
    LINE = "Oxygen uptake is flow times extraction."
