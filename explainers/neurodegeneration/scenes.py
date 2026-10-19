"""Neurodegeneration: slower worsening is still worsening  (Biochemistrypedia explainer)

Every number on screen is the lesson's own (Clarity AD, CDR-SB, 18 months, adjusted mean changes).

COLOR MAP (one color per concept, whole video)
  BLUE   = the lecanemab arm (drug)
  YELLOW = the placebo arm
  GREEN  = the gap: less worsening / relative slowing
  RED    = worsening (higher score), and the crossed-out wrong readings
  GREY   = axes, zero line, structure, labels
  TEAL   = the paper's reported interval
"""
import numpy as np
from bp_style import *  # noqa: F401,F403

K = 2.4            # frame units per CDR-SB point
Y0 = -2.9          # zero line
DRUG, PLC = 1.21, 1.66


def bar(x, h, color, w=1.6, op=0.45):
    return Rectangle(width=w, height=max(h * K, 0.001), stroke_color=color, stroke_width=3,
                     fill_color=color, fill_opacity=op).move_to([x, Y0 + h * K / 2, 0])


def chart(ax):
    """axis + zero line; returns dict. ax = x of the vertical axis."""
    axis = Line([ax, Y0, 0], [ax, Y0 + 4.9, 0], color=GREY, stroke_width=3)
    zero = Line([ax, Y0, 0], [ax + 5.6, Y0, 0], color=GREY, stroke_width=3)
    z = M("0", 26, GREY).next_to(axis.get_start(), LEFT, buff=0.15)
    up = Arrow([ax - 0.0, Y0 + 3.6, 0], [ax, Y0 + 4.9, 0], buff=0, color=RED, stroke_width=5, tip_length=0.25)
    worse = T("worse", 24, RED).next_to(up, RIGHT, buff=0.12)
    lab = T("change in CDR-SB (points)", 22, GREY).rotate(PI / 2).move_to([ax - 0.6, Y0 + 2.4, 0])
    return dict(axis=axis, zero=zero, z=z, up=up, worse=worse, lab=lab,
                base=VGroup(axis, zero, z, lab), xl=ax + 2.0, xp=ax + 4.6)


class S00Title(TitleCard):
    LESSON = "Neurodegeneration"
    TITLE = "Slower worsening is still worsening"


# ---------------------------------------------------------------------------------------------
class S01Question(SpokenScene):
    def construct(self):
        head = T("Clarity AD trial", 36, font=TITLE_FONT).to_edge(UP, buff=0.5)
        sub = T("18 months", 28, GREY).next_to(head, DOWN, buff=0.2)
        self.at("Clarity")
        self.play(Write(head), run_time=0.8)
        n = M("1,795 people", 52, TEXT).move_to([0, 1.6, 0])
        d = chip("mild cognitive impairment\nor mild dementia due to Alzheimer disease", TEXT, size=30).move_to([0, 0.1, 0])
        am = chip("amyloid confirmed", TEAL, size=30).move_to([0, -1.5, 0])
        self.at("people had")
        self.play(FadeIn(n, shift=UP * 0.1), run_time=0.7)
        self.at("mild cognitive")
        self.play(FadeIn(d, shift=UP * 0.1), run_time=0.7)
        self.at("Amyloid was")
        self.play(FadeIn(am, shift=UP * 0.1), run_time=0.7)

        R = 2.1
        def dial(cx, color):
            c = np.array([cx, -1.4, 0])
            arc = Arc(radius=R, start_angle=PI, angle=-PI, arc_center=c, color=GREY, stroke_width=5)
            ptr = Line(c, c + 1.8 * np.array([np.cos(2.6), np.sin(2.6), 0]), color=color, stroke_width=7)
            hub = Dot(c, radius=0.11, color=color)
            cap = T("rating score", 24, GREY).next_to(c, DOWN, buff=0.35)
            return VGroup(arc, ptr, hub, cap), ptr, c

        gl = chip("lecanemab", BLUE, size=34).move_to([-3.3, 1.9, 0])
        gp = chip("placebo", YELLOW, size=34).move_to([3.3, 1.9, 0])
        dl, pl, cl = dial(-3.3, BLUE)
        dp, pp, cp = dial(3.3, YELLOW)
        self.at("randomly")
        self.play(FadeOut(VGroup(n, d, am)), run_time=0.5)
        self.at("the antibody")
        self.play(FadeIn(gl, shift=DOWN * 0.2), FadeIn(dl), FadeIn(sub), run_time=0.7)
        self.at("a placebo")
        self.play(FadeIn(gp, shift=DOWN * 0.2), FadeIn(dp), run_time=0.7)
        q = T("?", 90, BLUE, weight=BOLD).move_to([-3.3, 0.2, 0])
        self.at("get better")
        self.play(FadeIn(q, scale=0.8), run_time=0.5)
        self.at("They did not")
        self.play(FadeOut(q), run_time=0.3)
        self.at("Both groups got worse")

        def rot(c, ang, col):
            return Line(c, c + 1.8 * np.array([np.cos(ang), np.sin(ang), 0]), color=col, stroke_width=7)
        w1 = T("worse", 30, RED).move_to([-3.3, -3.1, 0])
        w2 = T("worse", 30, RED).move_to([3.3, -3.1, 0])
        self.play(Transform(pl, rot(cl, 1.7, BLUE)), Transform(pp, rot(cp, 1.4, YELLOW)),
                  FadeIn(w1), FadeIn(w2), run_time=1.2)
        self.at("by how much")
        self.play(Indicate(pl, color=BLUE, scale_factor=1.0), Indicate(pp, color=YELLOW, scale_factor=1.0), run_time=0.8)
        self.finish()


# ---------------------------------------------------------------------------------------------
class S02Scale(SpokenScene):
    def construct(self):
        title = T("CDR-SB", 56, font=TITLE_FONT).move_to([0, 2.6, 0])
        full = T("Clinical Dementia Rating, Sum of Boxes", 30, GREY).next_to(title, DOWN, buff=0.25)
        self.at("score called")
        self.play(Write(title), run_time=0.8)
        self.at("Sum of Boxes")
        self.play(FadeIn(full, shift=UP * 0.1), run_time=0.6)
        rater = chip("clinician's rating: cognition and daily function", TEAL, size=26).move_to([0, 0.7, 0])
        self.at("clinician rates")
        self.play(FadeIn(rater, shift=UP * 0.15), run_time=0.7)
        x0, x1, y = -5.5, 5.5, -1.3
        line = Line([x0, y, 0], [x1, y, 0], color=GREY, stroke_width=6)
        t0 = Line([x0, y - 0.2, 0], [x0, y + 0.2, 0], color=GREY, stroke_width=5)
        t1 = Line([x1, y - 0.2, 0], [x1, y + 0.2, 0], color=GREY, stroke_width=5)
        l0 = M("0", 32, TEXT).next_to(t0, DOWN, buff=0.2)
        l1 = M("18", 32, TEXT).next_to(t1, DOWN, buff=0.2)
        self.at("score runs")
        self.play(Create(line), FadeIn(t0), FadeIn(t1), FadeIn(l0), FadeIn(l1), run_time=1.0)
        mark = Dot([x0 + 3.0, y, 0], radius=0.2, color=BLUE)
        ill = T("illustrative", 22, GREY).next_to(mark, DOWN, buff=0.25)
        self.play(FadeIn(mark, scale=0.5), FadeIn(ill), run_time=0.4)
        self.at("Higher means worse")
        arrow = Arrow([-1.5, -2.5, 0], [3.0, -2.5, 0], buff=0, color=RED, stroke_width=7, tip_length=0.3)
        hw = T("higher means worse", 30, RED).next_to(arrow, DOWN, buff=0.2)
        self.play(GrowArrow(arrow), FadeIn(hw), run_time=0.8)
        self.at("a rise")
        self.play(mark.animate.move_to([x0 + 7.0, y, 0]).set_color(RED), ill.animate.move_to([x0 + 7.0, y - 0.45, 0]), run_time=1.2)
        w = T("a rise = a worsening", 30, RED).next_to(mark, UP, buff=0.3)
        self.play(FadeIn(w), run_time=0.4)
        self.finish()


# ---------------------------------------------------------------------------------------------
class S03Bars(SpokenScene):
    def construct(self):
        ax = -2.6
        c = chart(ax)
        self.add(c["base"])
        head = T("Adjusted mean change at 18 months", 30, GREY).to_edge(UP, buff=0.45)
        self.play(FadeIn(head), run_time=0.5)
        self.play(FadeIn(c["up"]), FadeIn(c["worse"]), run_time=0.5)
        bl, bp = bar(c["xl"], DRUG, BLUE), bar(c["xp"], PLC, YELLOW)
        ll = M("+1.21", 30, BLUE).next_to(bl, UP, buff=0.15)
        lp = M("+1.66", 30, YELLOW).next_to(bp, UP, buff=0.15)
        nl = T("lecanemab", 26, BLUE).next_to(c["zero"], DOWN, buff=0.15).set_x(c["xl"])
        np_ = T("placebo", 26, YELLOW).next_to(c["zero"], DOWN, buff=0.15).set_x(c["xp"])
        self.at("were plus")
        self.play(GrowFromEdge(bl, DOWN), FadeIn(nl), run_time=0.9)
        self.play(FadeIn(ll), run_time=0.3)
        self.at("With placebo")
        self.play(GrowFromEdge(bp, DOWN), FadeIn(np_), run_time=0.9)
        self.play(FadeIn(lp), run_time=0.3)
        self.at("Both are rises")
        self.play(Indicate(ll, color=RED), Indicate(lp, color=RED), run_time=0.8)
        self.at("did not improve")
        nx = T("not better", 28, RED).move_to([c["xl"], Y0 - 0.0 + 0.0, 0])
        nxt = T("still above 0", 26, RED).next_to(bl, LEFT, buff=0.0).shift(UP * 0.0)
        top_l = bl.get_top()
        dash = DashedLine(top_l, [c["xp"] - 0.8, top_l[1], 0], color=GREY, stroke_width=3)
        self.play(Create(dash), run_time=0.5)
        self.at("worsened less")
        brace = Brace(Line([c["xp"] + 0.95, top_l[1], 0], [c["xp"] + 0.95, bp.get_top()[1], 0]), direction=RIGHT, color=GREEN)
        gl = T("worsened less", 28, GREEN).next_to(brace, RIGHT, buff=0.15)
        self.play(GrowFromCenter(brace), FadeIn(gl), run_time=0.8)
        self.at("strongest evidence")
        self.play(Indicate(brace, color=GREEN), run_time=0.8)
        self.at("did not stop it")
        mid = (Y0 + top_l[1]) / 2
        st = T("still\nworse", 24, RED).move_to([c["xl"], mid, 0])
        arr = Arrow([c["xl"], Y0 + 0.15, 0], [c["xl"], mid - 0.35, 0], buff=0, color=RED, stroke_width=6, tip_length=0.25)
        self.play(GrowArrow(arr), FadeIn(st), run_time=0.8)
        self.finish()


# ---------------------------------------------------------------------------------------------
def two_bars(ax, split=False):
    c = chart(ax)
    bl = bar(c["xl"], DRUG, BLUE)
    if split:
        low = bar(c["xp"], DRUG, YELLOW)
        topp = Rectangle(width=1.6, height=(PLC - DRUG) * K, stroke_color=GREEN, stroke_width=3, fill_color=GREEN,
                         fill_opacity=0.55).move_to([c["xp"], Y0 + DRUG * K + (PLC - DRUG) * K / 2, 0])
        bp = VGroup(low, topp)
        c["low"], c["topp"] = low, topp
    else:
        bp = bar(c["xp"], PLC, YELLOW)
    ll = M("+1.21", 30, BLUE).next_to(bl, UP, buff=0.15)
    lp = M("+1.66", 30, YELLOW).next_to(bp, UP, buff=0.15)
    nl = T("lecanemab", 26, BLUE).next_to(c["zero"], DOWN, buff=0.15).set_x(c["xl"])
    npl = T("placebo", 26, YELLOW).next_to(c["zero"], DOWN, buff=0.15).set_x(c["xp"])
    c.update(bl=bl, bp=bp, ll=ll, lp=lp, nl=nl, npl=npl)
    c["all"] = VGroup(c["base"], bl, bp, ll, lp, nl, npl, c["up"], c["worse"])
    return c


class S04Absolute(SpokenScene):
    def construct(self):
        ax = -5.3
        c = two_bars(ax)
        self.add(c["all"])
        gap_top = c["bl"].get_top()[1]
        dash = DashedLine([c["xl"], gap_top, 0], [c["xp"] - 0.8, gap_top, 0], color=GREY, stroke_width=3)
        self.add(dash)
        px = 3.7
        title = T("absolute difference", 32, GREEN, weight=BOLD).move_to([px, 2.9, 0])
        self.at("absolute difference")
        self.play(FadeIn(title), run_time=0.5)
        gap = Rectangle(width=1.6, height=(PLC - DRUG) * K, stroke_color=GREEN, stroke_width=3, fill_color=GREEN,
                        fill_opacity=0.55).move_to([c["xp"], Y0 + DRUG * K + (PLC - DRUG) * K / 2, 0])
        self.at("subtraction of two")
        self.play(FadeIn(gap), run_time=0.7)
        eq = M("1.66 − 1.21 = 0.45", 36, TEXT).move_to([px, 1.8, 0])
        less = T("points less worsening", 28, GREEN).next_to(eq, DOWN, buff=0.2)
        self.at("minus", lead=0.9)
        self.play(FadeIn(eq, shift=UP * 0.1), run_time=0.8)
        self.at("points less")
        self.play(FadeIn(less), run_time=0.5)
        paper = T("paper: difference of", 26, TEAL).move_to([px, 0.2, 0])
        pv = M("−0.45 points", 34, TEAL).next_to(paper, DOWN, buff=0.15)
        self.at("The paper reports")
        self.play(FadeIn(paper), FadeIn(pv), run_time=0.7)
        # interval
        xa, xb = 1.5, 5.9
        yy = -1.7
        f = lambda v: xa + (v + 0.67) / 0.44 * (xb - xa)
        ci = Line([f(-0.67), yy, 0], [f(-0.23), yy, 0], color=TEAL, stroke_width=8)
        ca = Line([f(-0.67), yy - 0.15, 0], [f(-0.67), yy + 0.15, 0], color=TEAL, stroke_width=5)
        cb = Line([f(-0.23), yy - 0.15, 0], [f(-0.23), yy + 0.15, 0], color=TEAL, stroke_width=5)
        dot = Dot([f(-0.45), yy, 0], radius=0.16, color=TEXT)
        la = M("−0.67", 26, TEAL).next_to(ca, DOWN, buff=0.2)
        lb = M("−0.23", 26, TEAL).next_to(cb, DOWN, buff=0.2)
        lci = T("95% confidence interval", 26, GREY).move_to([px, yy + 0.8, 0])
        self.at("confidence interval")
        self.play(Create(ci), FadeIn(ca), FadeIn(cb), FadeIn(dot), FadeIn(lci), run_time=0.9)
        self.play(FadeIn(la), FadeIn(lb), run_time=0.5)
        self.finish()


class S05Relative(SpokenScene):
    def construct(self):
        ax = -5.3
        c = two_bars(ax, split=True)
        self.add(c["all"])
        px = 3.7
        title = T("relative slowing", 32, GREEN, weight=BOLD).move_to([px, 2.9, 0])
        self.at("relative slowing")
        self.play(FadeIn(title), run_time=0.5)
        # placebo bar outlined as the whole
        whole = Rectangle(width=1.7, height=PLC * K + 0.08, stroke_color=YELLOW, stroke_width=6, fill_opacity=0).move_to(
            [c["xp"], Y0 + PLC * K / 2, 0])
        base = T("base = placebo change", 28, YELLOW).move_to([px, 1.9, 0])
        self.at("placebo change")
        self.play(Create(whole), FadeIn(base), run_time=0.9)
        self.at("whole decline")
        self.play(Indicate(whole, color=YELLOW, scale_factor=1.0), run_time=0.8)
        frac = VGroup(M("0.45", 38, GREEN), Line(LEFT * 0.8, RIGHT * 0.8, color=TEXT, stroke_width=4), M("1.66", 38, YELLOW)).arrange(DOWN, buff=0.12)
        eq = M("= 0.271", 38, TEXT)
        row = VGroup(frac, eq).arrange(RIGHT, buff=0.3).move_to([px, 0.3, 0])
        self.at("divided by")
        self.play(FadeIn(frac), run_time=0.7)
        self.play(FadeIn(eq, shift=LEFT * 0.1), run_time=0.5)
        pct = M("about 27%", 44, GREEN, weight=BOLD).move_to([px, -1.2, 0])
        self.at("That is about")
        self.play(FadeIn(pct, scale=0.9), run_time=0.7)
        chk = M("1.66 × 0.729 = 1.21", 32, TEXT).move_to([px, -2.4, 0])
        chkl = T("check", 26, GREY).next_to(chk, UP, buff=0.15)
        self.at("Check it")
        self.play(FadeIn(chkl), FadeIn(chk), run_time=0.8)
        self.finish()


class S06Rule(SpokenScene):
    def construct(self):
        ax = -5.3
        c = two_bars(ax, split=True)
        self.add(c["all"])
        gap_top = c["bl"].get_top()[1]
        dash = DashedLine([c["xl"], gap_top, 0], [c["xp"] - 0.8, gap_top, 0], color=GREY, stroke_width=3)
        self.add(dash)
        px = 3.5
        h = T("27% means", 34, GREEN, weight=BOLD).move_to([px, 2.9, 0])
        self.at("what does")
        self.play(FadeIn(h), run_time=0.5)
        cmp_ = chip("two amounts of decline, compared", GREEN, size=28).move_to([px, 2.0, 0])
        self.at("compares two amounts")
        self.play(FadeIn(cmp_, shift=UP * 0.1), Indicate(c["topp"], color=GREEN, scale_factor=1.0), run_time=0.9)
        h2 = T("it is not", 30, RED).move_to([px, 0.9, 0])
        self.play(FadeIn(h2), run_time=0.4)

        def wrong(txt, y):
            ch = chip(txt, RED, size=28)
            xm = VGroup(Line(UL * 0.2, DR * 0.2, color=RED, stroke_width=7), Line(UR * 0.2, DL * 0.2, color=RED, stroke_width=7))
            g = VGroup(xm, ch).arrange(RIGHT, buff=0.2).move_to([px, y, 0])
            return ch, xm
        w1, x1 = wrong("a 27% gain in memory", 0.1)
        w2, x2 = wrong("a fraction of patients helped", -0.8)
        w3, x3 = wrong("anyone's prognosis", -1.7)
        self.at("gain in memory")
        self.play(FadeIn(w1), Create(x1), run_time=0.7)
        self.at("fraction of patients")
        self.play(FadeIn(w2), Create(x2), run_time=0.7)
        self.at("anyone's prognosis")
        self.play(FadeIn(w3), Create(x3), run_time=0.7)
        rule = T("a share of the placebo decline", 30, GREEN, weight=BOLD).move_to([px, -2.75, 0])
        self.at("share of the placebo")
        self.play(FadeIn(rule, shift=UP * 0.1), run_time=0.7)
        self.at("still worsened")
        mid = (Y0 + gap_top) / 2
        st = T("still\nworse", 24, RED).move_to([c["xl"], mid, 0])
        arr = Arrow([c["xl"], Y0 + 0.15, 0], [c["xl"], mid - 0.35, 0], buff=0, color=RED, stroke_width=6, tip_length=0.25)
        self.play(GrowArrow(arr), FadeIn(st), run_time=0.8)
        self.finish()


class S07End(EndCard):
    LINE = "A share of the placebo decline; the treated group still worsened."
