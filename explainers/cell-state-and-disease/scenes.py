"""Cell identity, cell state and disease: a mutant clone wins by fate, not speed (Biochemistrypedia explainer)

Timed to the SPOKEN words: every self.at("...") cue waits for that phrase in audio/words.json.

COLOR MAP (one color per concept, whole video)
  BLUE    progenitor cell (a basal cell that divides); the starting count of progenitors
  GREEN   differentiating cell (moves up and is shed); "consistent" tick
  PURPLE  competitive clones around an early lesion (mouse model)
  YELLOW  Notch1-mutant cell or clone, and the grown progenitor count of the clone
  RED     cancer / malignant, the crossed-out idea, the early lesion
  GREY    structure, frames, neutral labels
  TEXT    all other labels and the formula
"""
import random
from bp_style import *


PURPLE = "#B58CE0"


# ---------- helpers ----------
def dot(color, r=0.28, fo=0.45, sw=2.5):
    return Circle(radius=r, stroke_color=color, stroke_width=sw, fill_color=color, fill_opacity=fo)


def cell_grid(cols, rows, sp, center):
    cells = VGroup(*[dot(GREY, r=sp * 0.43, fo=0.18, sw=2) for _ in range(cols * rows)])
    cells.arrange_in_grid(rows=rows, cols=cols, buff=sp * 0.14).move_to(center)
    return cells


def stack(center, mut_cols=(), mut_top=0):
    """Epithelium side view: row 0 = basal progenitors (blue), rows above = differentiating (green)."""
    sp = 0.84
    g = VGroup()
    basal, diff = VGroup(), VGroup()
    for c in range(5):
        col = YELLOW if c in mut_cols else BLUE
        d = dot(col, r=0.34).move_to(center + RIGHT * (c - 2) * sp + DOWN * 1.7)
        basal.add(d)
    for r in range(1, 5):
        for c in range(5):
            d = dot(GREEN, r=0.34, fo=0.4).move_to(center + RIGHT * (c - 2) * sp + DOWN * 1.7 + UP * r * sp)
            diff.add(d)
    return basal, diff


def pair(a, b, c0, gap=0.7, r=0.22):
    x, y = dot(a, r=r), dot(b, r=r)
    x.move_to(c0 + LEFT * gap / 2)
    y.move_to(c0 + RIGHT * gap / 2)
    return VGroup(x, y)


def division_row(y, left_col, right_col, label, x0=-0.6):
    parent = dot(BLUE, r=0.26).move_to(RIGHT * x0 + UP * y)
    arrow = Arrow(parent.get_right() + RIGHT * 0.1, RIGHT * (x0 + 1.5) + UP * y, buff=0, color=GREY, stroke_width=3,
                  max_tip_length_to_length_ratio=0.3)
    kids = pair(left_col, right_col, RIGHT * (x0 + 2.4) + UP * y)
    lab = T(label, size=24).next_to(kids, RIGHT, buff=0.4)
    lab.align_to(RIGHT * 2.9, LEFT)
    return VGroup(parent, arrow, kids, lab)


def cross(mob, color=RED):
    a = Line(mob.get_corner(UL), mob.get_corner(DR), color=color, stroke_width=7)
    b = Line(mob.get_corner(UR), mob.get_corner(DL), color=color, stroke_width=7)
    return VGroup(a, b)


def strike(mob, color=RED):
    return Line(mob.get_left() + LEFT * 0.05, mob.get_right() + RIGHT * 0.05, color=color, stroke_width=7)


def tick(color=GREEN):
    return VMobject(color=color, stroke_width=8).set_points_as_corners(
        [LEFT * 0.22 + UP * 0.0, LEFT * 0.06 + DOWN * 0.18, RIGHT * 0.26 + UP * 0.22])


# ---------- scenes ----------
class S00Title(TitleCard):
    LESSON = "Cell Identity, Cell State and Disease"
    TITLE = "Clones Win by Fate, Not Speed"


class S01Puzzle(SpokenScene):
    def construct(self):
        random.seed(4)
        gl = cell_grid(6, 7, 0.56, LEFT * 4.2 + DOWN * 0.35)
        gr = cell_grid(6, 7, 0.56, LEFT * 0.5 + DOWN * 0.35)
        q = T("Why is it still healthy?", size=34, font=TITLE_FONT).move_to(UP * 3.2 + LEFT * 2.35)
        self.at("Why is this")
        self.play(FadeIn(q, shift=DOWN * 0.1),
                  LaggedStart(*[GrowFromCenter(c) for c in VGroup(gl, gr)], lag_ratio=0.01), run_time=1.6)
        self.at("sequenced normal")
        lab = T("normal oesophagus lining: the range across donors", size=24, color=GREY).move_to(LEFT * 2.35 + UP * 2.15)
        self.play(FadeIn(lab, shift=DOWN * 0.1), run_time=0.5)
        t12 = T("12%", size=30, color=YELLOW).next_to(gl, DOWN, buff=0.2)
        t80 = T("80%", size=30, color=YELLOW).next_to(gr, DOWN, buff=0.2)
        lo = T("low end", size=22, color=GREY).next_to(t12, DOWN, buff=0.08)
        hi = T("high end", size=22, color=GREY).next_to(t80, DOWN, buff=0.08)
        la = list(range(len(gl))); random.shuffle(la)
        ra = list(range(len(gr))); random.shuffle(ra)
        self.at("made up an estimated")
        self.play(*[gl[i].animate.set_color(YELLOW).set_fill(YELLOW, 0.5) for i in la[:5]],
                  FadeIn(t12), FadeIn(lo), run_time=0.9)
        self.at("to 80")
        self.play(*[gr[i].animate.set_color(YELLOW).set_fill(YELLOW, 0.5) for i in ra[:34]],
                  FadeIn(t80), FadeIn(hi), run_time=1.2)
        head = T("Notch1 mutations", size=26, color=YELLOW).move_to(RIGHT * 4.45 + UP * 1.75)
        self.at("also turn up")
        cb = Rectangle(width=1.7, height=0.4, stroke_width=0, fill_color=RED, fill_opacity=0.8)
        cb.move_to(RIGHT * 2.75 + UP * 0.85, aligned_edge=LEFT)
        cl = T("oesophageal cancers", size=24).next_to(cb, DOWN, buff=0.12).align_to(cb, LEFT)
        self.play(FadeIn(head), GrowFromEdge(cb, LEFT), FadeIn(cl), run_time=0.9)
        self.at("this tissue looked normal")
        tag = T("looks normal", size=26, color=GREY).move_to(RIGHT * 4.45 + DOWN * 0.45)
        self.play(FadeIn(tag), run_time=0.5)
        self.at("more common here")
        nb = Rectangle(width=3.4, height=0.4, stroke_width=0, fill_color=YELLOW, fill_opacity=0.85)
        nb.move_to(RIGHT * 2.75 + DOWN * 1.35, aligned_edge=LEFT)
        nl = T("this normal tissue", size=24).next_to(nb, DOWN, buff=0.12).align_to(nb, LEFT)
        self.play(GrowFromEdge(nb, LEFT), FadeIn(nl), run_time=0.9)
        self.finish()


class S02Balance(SpokenScene):
    def construct(self):
        c = LEFT * 4.1
        basal, diff = stack(c)
        frame = DashedVMobject(Rectangle(width=4.4, height=4.7, stroke_color=GREY, stroke_width=2.5)
                               .move_to(c), num_dashes=60)
        self.at("The lining stays")
        self.play(LaggedStart(*[GrowFromCenter(d) for d in diff], lag_ratio=0.02),
                  LaggedStart(*[GrowFromCenter(d) for d in basal], lag_ratio=0.05), run_time=1.5)
        self.at("the same size")
        same = T("same size", size=26, color=GREY).next_to(frame, UP, buff=0.12)
        self.play(Create(frame), FadeIn(same), run_time=1.0)
        self.at("only the basal progenitor")
        blab = T("basal progenitors divide", size=24, color=BLUE).next_to(frame, DOWN, buff=0.12)
        self.play(FadeIn(blab), Indicate(basal, color=BLUE, scale_factor=1.1), run_time=1.0)
        rows = [
            division_row(1.9, BLUE, BLUE, "two progenitors"),
            division_row(0.2, GREEN, GREEN, "two differentiating"),
            division_row(-1.5, BLUE, GREEN, "one of each"),
        ]
        self.at("two progenitors")
        self.play(FadeIn(rows[0][0]), GrowArrow(rows[0][1]), run_time=0.5)
        self.play(TransformFromCopy(rows[0][0], rows[0][2]), FadeIn(rows[0][3]), run_time=0.7)
        self.at("two differentiating daughters")
        self.play(FadeIn(rows[1][0]), GrowArrow(rows[1][1]), run_time=0.5)
        self.play(TransformFromCopy(rows[1][0], rows[1][2]), FadeIn(rows[1][3]), run_time=0.7)
        self.at("one of each")
        self.play(FadeIn(rows[2][0]), GrowArrow(rows[2][1]), run_time=0.5)
        self.play(TransformFromCopy(rows[2][0], rows[2][2]), FadeIn(rows[2][3]), run_time=0.7)
        self.at("these three outcomes")
        bal = T("balanced", size=30, color=TEXT, weight=BOLD).move_to(RIGHT * 3.0 + UP * 3.1)
        rule = Line(bal.get_left() + DOWN * 0.3, bal.get_right() + DOWN * 0.3, color=GOLD, stroke_width=3)
        self.play(FadeIn(bal), Create(rule), run_time=0.8)
        self.at("Differentiating cells move upward")
        top = VGroup(*diff[-5:])
        up = Arrow(c + RIGHT * 2.55 + DOWN * 1.0, c + RIGHT * 2.55 + UP * 2.2, buff=0, color=GREEN, stroke_width=4)
        self.play(GrowArrow(up), diff.animate.shift(UP * 0.35), run_time=1.0)
        self.at("and are shed")
        shed = T("shed", size=26, color=GREEN).next_to(up, UP, buff=0.1)
        self.play(FadeOut(top, shift=UP * 0.6), FadeIn(shed), run_time=0.9)
        self.finish()


class S03Fate(SpokenScene):
    def construct(self):
        c = LEFT * 4.1
        mut = (1, 2, 3)
        basal, diff = stack(c)
        diff.shift(UP * 0.0)
        frame = DashedVMobject(Rectangle(width=4.4, height=4.7, stroke_color=GREY, stroke_width=2.5)
                               .move_to(c), num_dashes=60)
        blab = T("basal progenitors", size=24, color=BLUE).next_to(frame, DOWN, buff=0.12)
        self.add(frame, basal, diff, blab)
        self.at("A mutant clone")
        cl = T("Notch1-mutant clone", size=24, color=YELLOW).next_to(frame, UP, buff=0.12)
        self.play(*[basal[i].animate.set_color(YELLOW).set_fill(YELLOW, 0.5) for i in (2,)], FadeIn(cl), run_time=0.7)
        self.play(*[basal[i].animate.set_color(YELLOW).set_fill(YELLOW, 0.5) for i in (1, 3)], run_time=0.5)
        self.at("tilting that balance")
        self.play(Indicate(VGroup(basal[1], basal[2], basal[3]), color=YELLOW, scale_factor=1.15), run_time=1.0)
        # two question cards
        c1 = chip("Divide faster?", color=TEXT, size=34).move_to(RIGHT * 2.4 + UP * 2.4)
        arc = Arc(radius=0.5, start_angle=0.6, angle=5.0, color=GREY, stroke_width=5)
        arc.add_tip(tip_length=0.2)
        g1 = VGroup(arc).move_to(RIGHT * 2.4 + UP * 1.0)
        self.at("simply divide faster")
        self.play(FadeIn(c1, shift=LEFT * 0.2), Create(g1[0]), run_time=0.8)
        c2 = chip("Daughters differentiate less?", color=TEXT, size=34).move_to(RIGHT * 2.4 + DOWN * 0.5)
        pr = pair(BLUE, GREEN, RIGHT * 2.4 + DOWN * 1.65, gap=1.3, r=0.3)
        self.at("differentiate less")
        self.play(FadeIn(c2, shift=LEFT * 0.2), FadeIn(pr, shift=UP * 0.1), run_time=0.8)
        self.at("Notch signaling")
        note = T("Notch signalling: linked to differentiation", size=22, color=GREY).move_to(RIGHT * 2.4 + DOWN * 2.7)
        self.play(FadeIn(note), run_time=0.8)
        self.at("without a higher division rate")
        x = strike(c1)
        self.play(Create(x), c1[1].animate.set_opacity(0.6), g1.animate.set_opacity(0.4), run_time=0.9)
        self.at("more progenitor daughters")
        newb = dot(BLUE, r=0.3).move_to(pr[1])
        self.play(Transform(pr[1], newb), run_time=0.9)
        self.at("fewer differentiating")
        tk = tick().move_to(RIGHT * 4.5 + DOWN * 1.55)
        cons = T("consistent", size=22, color=GREEN).next_to(tk, DOWN, buff=0.1)
        self.play(Create(tk), FadeIn(cons), run_time=0.8)
        self.finish()


class S04Odds(SpokenScene):
    def construct(self):
        xs = [-3.6, 0.0, 3.6]
        base_y = -1.4
        K = 5.5
        names = ["PP", "PD", "DD"]
        words = ["two progenitors", "one of each", "two differentiating"]
        cols = [(BLUE, BLUE), (BLUE, GREEN), (GREEN, GREEN)]
        axis = Line(LEFT * 5.8 + UP * base_y, RIGHT * 5.8 + UP * base_y, color=GREY, stroke_width=3)
        glyphs = VGroup(*[pair(cols[i][0], cols[i][1], RIGHT * xs[i] + DOWN * 1.9, gap=0.8) for i in range(3)])
        labs = VGroup(*[T(f"{names[i]}: {words[i]}", size=24).move_to(RIGHT * xs[i] + DOWN * 2.65) for i in range(3)])
        f1 = M("m = 2 × p(PP) + p(PD)", size=30).move_to(UP * 3.0)
        probs0 = [0.25, 0.50, 0.25]
        probs1 = [0.35, 0.50, 0.15]

        def bar(i, p):
            col = [BLUE, TEAL, GREEN][i]
            b = Rectangle(width=1.5, height=max(p * K, 0.01), stroke_width=0, fill_color=[BLUE, GREY, GREEN][i],
                          fill_opacity=0.8)
            b.move_to(RIGHT * xs[i] + UP * base_y, aligned_edge=DOWN)
            return b

        def val(i, p):
            return M(f"{p:.2f}", size=28).next_to(bar(i, p), UP, buff=0.12)

        self.at("Count the progenitors")
        self.play(Create(axis), FadeIn(glyphs), FadeIn(labs), run_time=1.2)
        self.at("two times the chance")
        self.play(Write(f1), run_time=1.6)
        self.at("Balanced odds")
        bars = VGroup(*[bar(i, probs0[i]) for i in range(3)])
        vals = VGroup(*[val(i, probs0[i]) for i in range(3)])
        self.play(*[GrowFromEdge(b, DOWN) for b in bars], FadeIn(vals), run_time=1.2)
        self.at("so the count holds")
        f2 = M("= 2 × 0.25 + 0.50 = 0.50 + 0.50 = 1.0", size=28).move_to(UP * 2.25)
        self.play(Write(f2), run_time=1.6)
        self.at("Now tilt the odds")
        bars2 = VGroup(*[bar(i, probs1[i]) for i in range(3)])
        vals2 = VGroup(*[val(i, probs1[i]) for i in range(3)])
        self.play(FadeOut(f2), Transform(bars, bars2), Transform(vals, vals2), run_time=1.6)
        self.at("Then the average becomes")
        f3 = M("= 2 × 0.35 + 0.50 = 0.70 + 0.50 = 1.2", size=28, color=YELLOW).move_to(UP * 2.25)
        self.play(Write(f3), run_time=1.6)
        self.finish()


class S05Growth(SpokenScene):
    def construct(self):
        K = 0.022
        base_y = -2.4
        xs = [-4.2, -1.4, 1.4, 4.2]
        counts = [100, 120, 144, 172.8]
        bars = []
        for i, n in enumerate(counts):
            col = BLUE if i == 0 else YELLOW
            b = Rectangle(width=1.5, height=n * K, stroke_width=0, fill_color=col, fill_opacity=0.8)
            b.move_to(RIGHT * xs[i] + UP * base_y, aligned_edge=DOWN)
            bars.append(b)
        axis = Line(LEFT * 5.6 + UP * base_y, RIGHT * 5.6 + UP * base_y, color=GREY, stroke_width=3)
        glab = [T(s, size=24, color=GREY).move_to(RIGHT * xs[i] + DOWN * 2.75)
                for i, s in enumerate(["start", "generation 1", "generation 2", "generation 3"])]
        v0 = M("100", size=30, color=BLUE).next_to(bars[0], UP, buff=0.12)
        v3 = M("172.8", size=30, color=YELLOW).next_to(bars[3], UP, buff=0.12)
        self.at("Start with 100")
        self.play(Create(axis), GrowFromEdge(bars[0], DOWN), FadeIn(v0), FadeIn(glab[0]), run_time=1.3)
        nodeath = T("no cell death", size=24, color=GREY).move_to(LEFT * 3.4 + UP * 3.1)
        self.at("no cell death")
        self.play(FadeIn(nodeath), run_time=0.5)
        self.at("multiplies the count")
        arrs = []
        for i in range(3):
            a = Arrow(RIGHT * (xs[i] + 0.9) + UP * (base_y + counts[i] * K + 0.45),
                      RIGHT * (xs[i + 1] - 0.9) + UP * (base_y + counts[i + 1] * K + 0.45),
                      buff=0, color=GREY, stroke_width=3, max_tip_length_to_length_ratio=0.25)
            t = M("× 1.2", size=26).next_to(a, UP, buff=0.1)
            arrs.append(VGroup(a, t))
        self.play(GrowFromEdge(bars[1], DOWN), FadeIn(arrs[0]), FadeIn(glab[1]), run_time=0.8)
        self.play(GrowFromEdge(bars[2], DOWN), FadeIn(arrs[1]), FadeIn(glab[2]), run_time=0.8)
        self.play(GrowFromEdge(bars[3], DOWN), FadeIn(arrs[2]), FadeIn(glab[3]), run_time=0.8)
        self.at("no change in cycle time")
        cyc = T("cycle time: unchanged", size=24, color=GREY).move_to(RIGHT * 3.2 + UP * 3.1)
        self.play(FadeIn(cyc), run_time=0.6)
        self.at("After three generations")
        self.play(FadeIn(v3, scale=1.3), run_time=0.9)
        self.at("The model shows")
        sh = SurroundingRectangle(v3, color=YELLOW, buff=0.12)
        self.play(Create(sh), run_time=0.7)
        self.finish()


class S06Rule(SpokenScene):
    def construct(self):
        sp = 0.82
        r1y, r2y = 1.1, -1.5

        def row(y, n=13):
            return VGroup(*[dot(BLUE, r=0.3).move_to(RIGHT * ((i - (n - 1) / 2) * sp) + UP * y) for i in range(n)])

        row1 = row(r1y)
        for i in range(4, 9):
            row1[i].set_color(YELLOW).set_fill(YELLOW, 0.5)
        mal = chip("malignant", color=RED, size=30).move_to(UP * 3.0)
        l1 = T("human oesophagus: NOTCH1-mutant cells", size=24, color=YELLOW).move_to(UP * (r1y + 1.2))
        self.at("A cancer gene mutation")
        self.play(LaggedStart(*[GrowFromCenter(d) for d in row1], lag_ratio=0.03), FadeIn(l1), FadeIn(mal), run_time=1.5)
        self.at("did not make")
        x = strike(mal)
        self.play(Create(x), mal[1].animate.set_opacity(0.6), run_time=0.8)
        self.at("In mouse")
        l1b = T("mouse oesophagus: Notch1-mutant clone", size=24, color=YELLOW).move_to(UP * (r1y + 1.2))
        self.play(FadeOut(mal), FadeOut(x), Transform(l1, l1b), run_time=0.8)
        self.at("clone edge")
        edge = [row1[3], row1[9]]
        self.play(*[e.animate.set_color(GREEN).set_fill(GREEN, 0.4).shift(UP * 0.35) for e in edge], run_time=1.0)
        self.at("differentiated faster")
        nl = T("wild-type neighbours at the clone edge", size=22, color=GREEN).move_to(UP * (r1y - 0.85))
        self.play(*[Indicate(e, color=GREEN, scale_factor=1.25) for e in edge], FadeIn(nl), run_time=0.8)
        row2 = VGroup(*[dot(PURPLE, r=0.3, fo=0.5).move_to(RIGHT * ((i - 6) * sp) + UP * r2y) for i in range(13)])
        lesion = VGroup(*[dot(RED, r=0.3, fo=0.5) for _ in range(3)])
        lesion.arrange(RIGHT, buff=0.22).move_to(UP * r2y)
        for i in (5, 6, 7):
            row2[i].set_opacity(0)
        l2 = T("mouse model: early lesion among competitive clones", size=24, color=GREY).move_to(UP * (r2y + 0.85))
        self.at("early lesions")
        self.play(FadeIn(row2), FadeIn(lesion), FadeIn(l2), run_time=1.0)
        self.at("removed more often")
        self.play(*[FadeOut(d, scale=0.3) for d in lesion], run_time=1.0)
        self.at("not human prevention data")
        m = T("mouse result", size=24, color=GREY).move_to(UP * (r2y - 0.85))
        self.play(FadeIn(m), run_time=0.5)
        self.at("So ask which clones")
        rule = T("Which clones expand, and why?", size=36, font=TITLE_FONT).move_to(DOWN * 3.05)
        self.play(FadeIn(rule, shift=UP * 0.15), run_time=0.8)
        self.finish()


class S07End(EndCard):
    LINE = "Ask which clones expand, and why, not only which mutations."
