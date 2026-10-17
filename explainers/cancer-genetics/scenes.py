"""Cancer as a genetic disease: one hit inherited, one hit rare  (Biochemistrypedia explainer)

Timed to the SPOKEN words: every self.at("...") cue waits for that phrase in audio/words.json.

COLOR MAP (one color per concept, whole video)
  RED    = the broken (mutant) copy of RB1, a hit
  GREEN  = the working copy of RB1
  YELLOW = the second hit as an event (the thing that strikes)
  ORANGE = a tumor: a tumor cell, a tumor in an eye, an affected person
  TEAL   = a probability with no tumor / numbers that are computed
  GREY   = outlines, axes, healthy cells, labels
"""
import numpy as np
from math import exp, factorial
from bp_style import *  # noqa: F401,F403

ORANGE = "#F29E4C"


# ---------------------------------------------------------------------------------------------
# helpers
# ---------------------------------------------------------------------------------------------
def cell(center, s=1.0, l=RED, r=GREEN, outline=GREY, fill=0.0):
    """A cell as a rounded square holding the two copies of RB1 as two small bars."""
    center = np.array(center, float)
    box = RoundedRectangle(corner_radius=0.12 * s, width=s, height=s, stroke_color=outline, stroke_width=3,
                           fill_color=outline, fill_opacity=fill).move_to(center)
    lb = RoundedRectangle(corner_radius=0.05 * s, width=0.14 * s, height=0.58 * s, stroke_width=0,
                          fill_color=l, fill_opacity=1).move_to(center + LEFT * 0.17 * s)
    rb = RoundedRectangle(corner_radius=0.05 * s, width=0.14 * s, height=0.58 * s, stroke_width=0,
                          fill_color=r, fill_opacity=1).move_to(center + RIGHT * 0.17 * s)
    g = VGroup(box, lb, rb)
    g.box, g.lb, g.rb = box, lb, rb
    return g


def tumorize(c):
    """animations: the working copy is hit, the cell becomes a tumor cell."""
    return [c.rb.animate.set_fill(RED, 1), c.box.animate.set_stroke(ORANGE).set_fill(ORANGE, 0.4)]


def grid_cells(rows=4, cols=9, pitch=1.3, cy=-0.3, s=1.0):
    cells = []
    for i in range(rows):
        for j in range(cols):
            x = (j - (cols - 1) / 2) * pitch
            y = cy + ((rows - 1) / 2 - i) * pitch
            cells.append(cell([x, y, 0], s))
    return cells


def legend(y=-3.42):
    a = RoundedRectangle(corner_radius=0.03, width=0.11, height=0.4, stroke_width=0, fill_color=RED, fill_opacity=1)
    ta = T("broken copy", 22, RED)
    b = RoundedRectangle(corner_radius=0.03, width=0.11, height=0.4, stroke_width=0, fill_color=GREEN, fill_opacity=1)
    tb = T("working copy", 22, GREEN)
    sq = RoundedRectangle(corner_radius=0.06, width=0.4, height=0.4, stroke_color=ORANGE, stroke_width=3,
                          fill_color=ORANGE, fill_opacity=0.4)
    tc = T("tumor cell", 22, ORANGE)
    g = VGroup(VGroup(a, ta).arrange(RIGHT, buff=0.15), VGroup(b, tb).arrange(RIGHT, buff=0.15),
               VGroup(sq, tc).arrange(RIGHT, buff=0.15)).arrange(RIGHT, buff=0.8)
    return g.move_to([0, y, 0])


def hit_dot():
    return Circle(radius=0.14, stroke_width=0, fill_color=YELLOW, fill_opacity=1)


def eye(center, tumor=False, s=1.0):
    center = np.array(center, float)
    body = Ellipse(width=1.3 * s, height=0.78 * s, stroke_color=GREY, stroke_width=3, fill_color=BG, fill_opacity=1).move_to(center)
    iris = Circle(radius=0.2 * s, stroke_color=GREY, stroke_width=3, fill_color=GREY, fill_opacity=0.35).move_to(center)
    g = VGroup(body, iris)
    if tumor:
        dot = Circle(radius=0.14 * s, stroke_width=0, fill_color=ORANGE, fill_opacity=1).move_to(center + RIGHT * 0.38 * s + DOWN * 0.03 * s)
        g.add(dot)
    return g


def eyes(center, tl, tr, s=1.0):
    center = np.array(center, float)
    return VGroup(eye(center + LEFT * 0.85 * s, tl, s), eye(center + RIGHT * 0.85 * s, tr, s))


def bracket(x0, x1, y, color, tick=0.18):
    return VGroup(Line([x0, y - tick, 0], [x0, y, 0], color=color, stroke_width=4),
                  Line([x0, y, 0], [x1, y, 0], color=color, stroke_width=4),
                  Line([x1, y, 0], [x1, y - tick, 0], color=color, stroke_width=4))


def arr(a, b, color=GREY, w=5):
    return Arrow(a, b, buff=0.08, color=color, stroke_width=w, tip_length=0.22,
                 max_tip_length_to_length_ratio=0.45, max_stroke_width_to_length_ratio=12)


TUMOR_IDX = [7, 14, 29]   # the same three cells in s01 and s02


class S00Title(TitleCard):
    LESSON = "Cancer as a genetic disease"
    TITLE = "One hit inherited, one hit rare"


# ---------------------------------------------------------------------------------------------
class S01Puzzle(SpokenScene):
    """one cell with a broken copy -> every cell has it -> yet only a few tumors."""

    def construct(self):
        big = cell([0, 0.2, 0], 3.0)
        self.play(FadeIn(big, scale=0.9), run_time=0.8)
        self.at("inherits one broken copy")
        lbl = T("broken copy", 30, RED).next_to(big, LEFT, buff=0.5)
        ptr = arr(lbl.get_right() + RIGHT * 0.05, big.lb.get_left() + LEFT * 0.05, RED)
        self.play(FadeIn(lbl), GrowArrow(ptr), run_time=0.7)
        self.at("sits in every cell")
        cells = grid_cells()
        self.play(FadeOut(lbl), FadeOut(ptr), ReplacementTransform(big, cells[0]),
                  LaggedStart(*[GrowFromCenter(c) for c in cells[1:]], lag_ratio=0.04), run_time=2.0)
        lg = legend()
        self.play(FadeIn(lg), run_time=0.5)
        self.at("whole eye")
        q = T("is the whole eye a tumor?", 34, YELLOW).move_to([0, 3.1, 0])
        self.play(FadeIn(q, shift=DOWN * 0.1), run_time=0.6)
        self.at("only a few tumors")
        a = [tumorize(cells[i]) for i in TUMOR_IDX]
        q2 = T("only a few tumors", 34, ORANGE).move_to([0, 3.1, 0])
        self.play(*[x for g in a for x in g], ReplacementTransform(q, q2), run_time=0.9)
        self.finish()


class S02Second(SpokenScene):
    """first hit inherited; one working copy is enough; a rare second hit makes a tumor cell."""

    def construct(self):
        cells = grid_cells()
        lg = legend()
        self.add(*cells, lg)
        top = T("first hit: inherited, in every cell", 34, RED).move_to([0, 3.1, 0])
        self.at("only the first of two steps")
        self.play(FadeIn(top, shift=DOWN * 0.1), run_time=0.6)
        self.at("two copies of the gene")
        self.play(*[Indicate(VGroup(cells[i].lb, cells[i].rb), color=TEXT, scale_factor=1.5) for i in (3, 20, 31)], run_time=1.0)
        self.at("one working copy")
        top2 = T("one working copy: enough brake", 34, GREEN).move_to([0, 3.1, 0])
        self.play(ReplacementTransform(top, top2),
                  *[Indicate(cells[i].rb, color=GREEN, scale_factor=1.6) for i in (3, 20, 31)], run_time=1.0)
        self.at("second hit that removes")
        top3 = T("second hit removes the working copy", 34, YELLOW).move_to([0, 3.1, 0])
        dots = [hit_dot().move_to(cells[i].rb.get_center() + UP * 0.85) for i in TUMOR_IDX]
        self.play(ReplacementTransform(top2, top3), *[FadeIn(d) for d in dots], run_time=0.6)
        self.play(*[d.animate.move_to(cells[i].rb.get_center()) for d, i in zip(dots, TUMOR_IDX)], run_time=0.6)
        anims = [x for i in TUMOR_IDX for x in tumorize(cells[i])]
        self.play(*anims, *[Flash(cells[i], color=YELLOW, flash_radius=0.8) for i in TUMOR_IDX],
                  *[FadeOut(d) for d in dots], run_time=0.8)
        self.at("That second hit is rare")
        top4 = T("the second hit is rare", 34, YELLOW).move_to([0, 3.1, 0])
        self.play(ReplacementTransform(top3, top4), run_time=0.6)
        self.at("only a few cells")
        ring = [SurroundingRectangle(cells[i], color=ORANGE, buff=0.12, stroke_width=3) for i in TUMOR_IDX]
        self.play(*[Create(r) for r in ring], run_time=0.7)
        self.at("only those cells become tumor")
        self.play(*[FadeOut(r) for r in ring], run_time=0.4)
        self.finish()


class S03Count(SpokenScene):
    """Poisson bars for a mean of 1.5 tumors per eye."""

    def construct(self):
        m = 1.5
        probs = [exp(-m) * m ** k / factorial(k) for k in range(7)]
        base, hscale, pitch, bw = -2.5, 10.7, 1.45, 1.05
        x0 = -(6 * pitch) / 2
        xs = [x0 + k * pitch for k in range(7)]
        self.at("count the second hits")
        t0 = T("model: mean 1.5 tumors per eye", 34, TEXT).move_to([0, 3.3, 0])
        axis = Line([x0 - 0.9, base, 0], [xs[-1] + 0.9, base, 0], color=GREY, stroke_width=3)
        ticks = VGroup(*[M(str(k), 26, GREY).move_to([xs[k], base - 0.38, 0]) for k in range(7)])
        axlab = T("tumors in one eye", 26, GREY).move_to([0, base - 0.95, 0])
        self.play(FadeIn(t0, shift=DOWN * 0.1), Create(axis), FadeIn(ticks), FadeIn(axlab), run_time=0.8)
        self.at("independent second hit")
        dots = VGroup(*[hit_dot().scale(1.4).move_to([(i - 2) * 1.2, 0.9, 0]) for i in range(5)])
        dl = T("each tumor comes from its own independent second hit", 28, YELLOW).move_to([0, 0.1, 0])
        self.play(LaggedStart(*[FadeIn(d, scale=0.5) for d in dots], lag_ratio=0.15), FadeIn(dl), run_time=1.0)
        self.at("averages")
        self.play(Indicate(t0, color=YELLOW, scale_factor=1.08), run_time=0.8)
        self.at("tumors then follows")
        self.play(FadeOut(dots), FadeOut(dl), run_time=0.4)
        bars = []
        for k, p in enumerate(probs):
            b = Rectangle(width=bw, height=p * hscale, stroke_width=2, stroke_color=GREY, fill_color=GREY, fill_opacity=0.45)
            b.move_to([xs[k], base + p * hscale / 2, 0])
            bars.append(b)
        self.play(LaggedStart(*[GrowFromEdge(b, DOWN) for b in bars], lag_ratio=0.12), run_time=1.6)
        self.at("no tumor in one eye")
        v0 = M("0.223", 38, TEAL).move_to([xs[0], base + probs[0] * hscale + 0.45, 0])
        self.play(bars[0].animate.set_stroke(TEAL).set_fill(TEAL, 0.6), FadeIn(v0, shift=UP * 0.1), run_time=0.7)
        self.at("at least one")
        br = bracket(xs[1] - 0.5, xs[6] + 0.5, base + 4.1, ORANGE)
        v1 = VGroup(T("at least one:", 32, ORANGE), M("0.777", 38, ORANGE)).arrange(RIGHT, buff=0.3).move_to([(xs[1] + xs[6]) / 2 + 0.6, base + 4.7, 0])
        self.play(*[b.animate.set_stroke(ORANGE).set_fill(ORANGE, 0.45) for b in bars[1:]], Create(br), FadeIn(v1), run_time=0.8)
        self.finish()


class S04Eyes(SpokenScene):
    """two eyes, three outcomes, penetrance."""

    def construct(self):
        cx = [-3.9, 0.0, 3.9]
        base, hs = -2.1, 3.0 / 60.4
        pct = [60.4, 34.7, 5.0]
        names = ["tumors in both eyes", "tumor in one eye only", "no tumor in either eye"]
        colors = [ORANGE, ORANGE, TEAL]
        flags = [(True, True), (True, False), (False, False)]
        self.at("both eyes together")
        pair = eyes([0, 0.3, 0], False, False, 1.8)
        self.play(FadeIn(pair, scale=0.9), run_time=0.7)
        self.at("eyes are independent")
        ind = T("each eye on its own", 32, GREY).move_to([0, -1.2, 0])
        self.play(FadeIn(ind), run_time=0.5)

        def column(i):
            bar = Rectangle(width=2.2, height=max(pct[i] * hs, 0.04), stroke_width=2, stroke_color=colors[i],
                            fill_color=colors[i], fill_opacity=0.5)
            bar.move_to([cx[i], base + max(pct[i] * hs, 0.04) / 2, 0])
            v = M(f"{pct[i]:.1f}%", 34, colors[i]).move_to([cx[i], base - 0.5, 0])
            d = T(names[i], 24, GREY).move_to([cx[i], base - 1.05, 0])
            return bar, v, d

        # column 1: both eyes
        self.at("Tumors in both eyes")
        e0 = eyes([cx[0], 1.95, 0], True, True, 1.15)
        b, v, d = column(0)
        self.play(FadeOut(ind), ReplacementTransform(pair, e0), run_time=0.8)
        self.play(GrowFromEdge(b, DOWN), FadeIn(v), FadeIn(d), run_time=0.8)
        self.at("one eye only")
        e1 = eyes([cx[1], 1.95, 0], True, False, 1.15)
        b1, v1, d1 = column(1)
        self.play(FadeIn(e1), run_time=0.4)
        self.play(GrowFromEdge(b1, DOWN), FadeIn(v1), FadeIn(d1), run_time=0.8)
        self.at("No tumor in either eye")
        e2 = eyes([cx[2], 1.95, 0], False, False, 1.15)
        b2, v2, d2 = column(2)
        self.play(FadeIn(e2), run_time=0.4)
        self.play(GrowFromEdge(b2, DOWN), FadeIn(v2), FadeIn(d2), run_time=0.8)
        self.at("of carriers get")
        br = bracket(cx[0] - 1.7, cx[1] + 1.7, 2.85, ORANGE)
        lab = T("in this model, about 95% of carriers get a tumor", 28, ORANGE).move_to([(cx[0] + cx[1]) / 2, 3.4, 0])
        self.play(Create(br), FadeIn(lab), run_time=0.8)
        self.at("penetrance")
        pen = T("penetrance", 34, GOLD, weight=BOLD).move_to([cx[2], 3.0, 0])
        self.play(FadeIn(pen, shift=DOWN * 0.1), run_time=0.6)
        self.finish()


class S05Sporadic(SpokenScene):
    """no inherited copy: two rare hits in the same cell."""

    def construct(self):
        xs = [-4.2, 0.0, 4.2]
        y = 1.5
        c1 = cell([xs[0], y, 0], 2.0, GREEN, GREEN)
        l1 = T("no inherited hit", 26, GREY).move_to([xs[0], y - 1.5, 0])
        self.at("no inherited copy")
        self.play(FadeIn(c1, scale=0.9), FadeIn(l1), run_time=0.7)
        self.at("Both rare hits")
        c2 = cell([xs[1], y, 0], 2.0, RED, GREEN)
        c3 = cell([xs[2], y, 0], 2.0, RED, RED, ORANGE, 0.4)
        a1 = arr([xs[0] + 1.25, y, 0], [xs[1] - 1.25, y, 0], YELLOW)
        a2 = arr([xs[1] + 1.25, y, 0], [xs[2] - 1.25, y, 0], YELLOW)
        d1 = hit_dot().move_to([xs[0] + 1.9, y + 0.55, 0]).scale(1.2)
        d2 = hit_dot().move_to([xs[1] + 1.9, y + 0.55, 0]).scale(1.2)
        h1 = T("first hit", 26, YELLOW).move_to([(xs[0] + xs[1]) / 2, y + 0.75, 0])
        h2 = T("second hit", 26, YELLOW).move_to([(xs[1] + xs[2]) / 2, y + 0.75, 0])
        self.play(GrowArrow(a1), FadeIn(h1), run_time=0.5)
        self.play(FadeIn(c2, scale=0.9), run_time=0.5)
        self.play(GrowArrow(a2), FadeIn(h2), run_time=0.5)
        self.at("same cell")
        self.play(FadeIn(c3, scale=0.9), Flash(c3, color=YELLOW, flash_radius=1.3), run_time=0.7)
        l3 = T("both hits in one cell", 26, ORANGE).move_to([xs[2], y - 1.5, 0])
        self.play(FadeIn(l3), run_time=0.4)
        self.at("expected number of tumors")
        n1 = VGroup(T("expected tumors per eye:", 30, GREY), M("0.0001", 34, TEAL)).arrange(RIGHT, buff=0.3).move_to([0, -1.7, 0])
        self.play(FadeIn(n1, shift=UP * 0.1), run_time=0.6)
        self.at("tumor in each eye")
        n2 = VGroup(T("tumor in each eye:", 30, GREY), T("about 1 in 100 million", 34, TEAL)).arrange(RIGHT, buff=0.3).move_to([0, -2.6, 0])
        self.play(FadeIn(n2, shift=UP * 0.1), run_time=0.6)
        self.at("these tumors are single")
        keep = VGroup(c1, l1, c2, c3, a1, a2, h1, h2, l3, n1, n2)
        self.play(FadeOut(keep), run_time=0.5)
        ee = eyes([0, 1.5, 0], True, False, 2.0)
        sl = T("single and one-sided", 34, ORANGE).move_to([0, -0.2, 0])
        self.play(FadeIn(ee), FadeIn(sl), run_time=0.7)
        self.at("found later")
        tl = arr([-5.2, -1.8, 0], [5.2, -1.8, 0], GREY)
        tlab = T("found later", 30, GREY).move_to([3.9, -2.4, 0])
        self.play(GrowArrow(tl), FadeIn(tlab), run_time=0.8)
        self.at("pile up")
        k1 = VGroup(hit_dot().scale(1.3).move_to([-2.2, -1.8, 0]), T("hit", 24, YELLOW).move_to([-2.2, -1.3, 0]))
        k2 = VGroup(hit_dot().scale(1.3).move_to([0.2, -1.8, 0]), T("hit", 24, YELLOW).move_to([0.2, -1.3, 0]))
        self.play(FadeIn(k1, shift=DOWN * 0.1), run_time=0.4)
        self.play(FadeIn(k2, shift=DOWN * 0.1), run_time=0.4)
        self.finish()


class S06Rule(SpokenScene):
    """pedigree (dominant) beside one cell (recessive)."""

    def construct(self):
        S = 0.62

        def sym(x, y, sq, aff):
            col = ORANGE if aff else GREY
            if sq:
                s = Square(side_length=S, stroke_color=col, stroke_width=3, fill_color=col, fill_opacity=0.9 if aff else 0)
            else:
                s = Circle(radius=S / 2, stroke_color=col, stroke_width=3, fill_color=col, fill_opacity=0.9 if aff else 0)
            return s.move_to([x, y, 0])

        yI, yII, yIII = 2.3, 0.5, -1.4
        f = sym(-4.6, yI, True, True)
        mo = sym(-2.9, yI, False, False)
        m1 = Line(f.get_right(), mo.get_left(), color=GREY, stroke_width=3)
        mid1 = (f.get_right() + mo.get_left()) / 2
        kx = [-5.8, -4.3, -2.8]
        ks = [sym(kx[0], yII, True, True), sym(kx[1], yII, False, False), sym(kx[2], yII, False, True)]
        sib = Line([kx[0], yII + 0.95, 0], [kx[2], yII + 0.95, 0], color=GREY, stroke_width=3)
        d1 = Line(mid1, [mid1[0], yII + 0.95, 0], color=GREY, stroke_width=3)
        drops = VGroup(*[Line([x, yII + 0.95, 0], [x, yII + 0.31, 0], color=GREY, stroke_width=3) for x in kx])
        p = sym(-1.3, yII, True, False)
        m2 = Line(ks[2].get_right(), p.get_left(), color=GREY, stroke_width=3)
        mid2 = (ks[2].get_right() + p.get_left()) / 2
        gx = [-2.8, -1.3]
        gk = [sym(gx[0], yIII, False, True), sym(gx[1], yIII, True, False)]
        sib2 = Line([gx[0], yIII + 0.95, 0], [gx[1], yIII + 0.95, 0], color=GREY, stroke_width=3)
        d2 = Line(mid2, [mid2[0], yIII + 0.95, 0], color=GREY, stroke_width=3)
        drops2 = VGroup(*[Line([x, yIII + 0.95, 0], [x, yIII + 0.31, 0], color=GREY, stroke_width=3) for x in gx])
        ped = VGroup(f, mo, m1, d1, sib, drops, *ks, p, m2, d2, sib2, drops2, *gk)
        pl = T("in the family: dominant", 32, ORANGE).move_to([-3.4, -2.75, 0])
        key = VGroup(sym(0, 0, True, True).scale(0.55), T("affected", 22, ORANGE)).arrange(RIGHT, buff=0.15).move_to([-3.4, -3.35, 0])

        self.at("In a family")
        self.play(FadeIn(VGroup(f, mo, m1)), run_time=0.5)
        self.play(Create(d1), Create(sib), Create(drops), FadeIn(VGroup(*ks)), run_time=0.6)
        self.play(Create(m2), FadeIn(p), run_time=0.4)
        self.play(Create(d2), Create(sib2), Create(drops2), FadeIn(VGroup(*gk)), run_time=0.5)
        self.at("looks dominant")
        self.play(FadeIn(pl), FadeIn(key), run_time=0.5)
        self.at("children inherit it")
        self.play(Indicate(VGroup(*ks), color=ORANGE, scale_factor=1.1), run_time=0.9)
        self.at("inside one cell")
        c = cell([3.6, 1.0, 0], 3.0, RED, GREEN)
        cl = T("in the cell: recessive", 32, GREEN).move_to([3.6, -1.15, 0])
        ln = T("one hit: healthy cell", 26, GREY).move_to([3.6, -1.75, 0])
        self.play(FadeIn(c, scale=0.9), run_time=0.7)
        self.at("allele is recessive")
        self.play(FadeIn(cl), FadeIn(ln), run_time=0.6)
        self.at("A pedigree follows risk")
        self.play(Indicate(ped, color=ORANGE, scale_factor=1.03), run_time=0.9)
        self.at("A cell counts copies")
        self.play(Indicate(VGroup(c.lb, c.rb), color=TEXT, scale_factor=1.3), run_time=0.9)
        self.finish()


class S07End(EndCard):
    LINE = "First hit inherited: dominant in the family, recessive in the cell."
