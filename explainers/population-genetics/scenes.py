"""Population genetics: why dominant alleles do not spread  (Biochemistrypedia explainer)

Timed to the SPOKEN words: every self.at("...") cue waits for that phrase in audio/words.json.

COLOR MAP (one color per concept, whole video)
  BLUE    = allele M, and the MM genotype
  YELLOW  = allele N, and the NN genotype
  GREEN   = the heterozygote MN, and "no departure / holds"
  PURPLE  = a person who shows the dominant trait (scene 1 only)
  TEAL    = expected counts (Hardy-Weinberg)
  ORANGE  = observed counts
  RED     = "no", a broken assumption, a force acting on the population
  GOLD    = highlight outline around the M copies
  GREY    = outlines, labels, de-emphasized
"""
import numpy as np
from bp_style import *  # noqa: F401,F403

PURPLE = "#B58CD9"
ORANGE = "#F29E4C"
P = 0.5425
Q = 0.4575


# ---------------------------------------------------------------------------------------------
# helpers
# ---------------------------------------------------------------------------------------------
def person_row(n_trait, n=10, r=0.26, gap=0.78):
    dots = VGroup(*[Circle(radius=r, stroke_width=2, stroke_color=PURPLE if i < n_trait else GREY,
                           fill_color=PURPLE if i < n_trait else GREY, fill_opacity=0.9 if i < n_trait else 0.35)
                    for i in range(n)])
    dots.arrange(RIGHT, buff=gap - 2 * r)
    return dots


def split_bar(frac, width, height, ml=True, size=34, show_letters=True):
    """horizontal bar: blue M part (p) and yellow N part (q), left to right."""
    wp, wq = width * frac, width * (1 - frac)
    a = Rectangle(width=wp, height=height, stroke_color=BLUE, stroke_width=3, fill_color=BLUE, fill_opacity=0.35)
    b = Rectangle(width=wq, height=height, stroke_color=YELLOW, stroke_width=3, fill_color=YELLOW, fill_opacity=0.35)
    a.move_to(ORIGIN).align_to(ORIGIN, LEFT).shift(LEFT * width / 2)
    b.next_to(a, RIGHT, buff=0)
    la = M("p", size, BLUE, weight=BOLD).move_to(a)
    lb = M("q", size, YELLOW, weight=BOLD).move_to(b)
    g = VGroup(a, b, la, lb)
    g.a, g.b, g.la, g.lb = a, b, la, lb
    return g


def allele_dot(kind, r=0.15):
    c = BLUE if kind == "M" else YELLOW
    return Circle(radius=r, stroke_color=c, stroke_width=2, fill_color=c, fill_opacity=0.9)


SQ = 4.8          # side of the Hardy-Weinberg square
SQC = np.array([-1.7, -0.5, 0.0])


def build_square():
    """the area model. returns a group with named parts."""
    wp, wq = SQ * P, SQ * Q
    x0, y0 = SQC[0] - SQ / 2, SQC[1] + SQ / 2
    cells = {}
    spec = [("MM", 0, 0, wp, wp, BLUE), ("NM", 1, 0, wq, wp, GREEN), ("MN", 0, 1, wp, wq, GREEN), ("NN", 1, 1, wq, wq, YELLOW)]
    for name, cx, cy, w, h, col in spec:
        px = x0 + (wp if cx else 0)
        py = y0 - (wp if cy else 0)
        r = Rectangle(width=w, height=h, stroke_color=col, stroke_width=3, fill_color=col, fill_opacity=0.0)
        r.move_to([px + w / 2, py - h / 2, 0])
        cells[name] = r
    g = VGroup(*cells.values())
    g.cells = cells
    return g


def cell_label(cell, geno, expr, col):
    t1 = T(geno, 28, col, weight=BOLD)
    t2 = M(expr, 26, TEXT)
    return VGroup(t1, t2).arrange(DOWN, buff=0.12).move_to(cell)


def square_heads():
    """egg heads above the columns and sperm heads left of the rows."""
    sq = build_square()
    c = sq.cells
    egg_m = chip("egg M  p", BLUE, size=24, pad=0.14).next_to(c["MM"], UP, buff=0.18)
    egg_n = chip("egg N  q", YELLOW, size=24, pad=0.14).next_to(c["NM"], UP, buff=0.18)
    sp_m = chip("sperm M  p", BLUE, size=24, pad=0.14).next_to(c["MM"], LEFT, buff=0.18)
    sp_n = chip("sperm N  q", YELLOW, size=24, pad=0.14).next_to(c["MN"], LEFT, buff=0.18)
    return VGroup(egg_m, egg_n, sp_m, sp_n)


class S00Title(TitleCard):
    LESSON = "Population genetics"
    TITLE = "Why dominant alleles do not spread"


# ---------------------------------------------------------------------------------------------
class S01Question(SpokenScene):
    """rows of people with the trait creeping up the generations; red no."""

    def construct(self):
        ys = [2.05, 0.8, -0.45, -1.7]
        rows = [person_row(3), person_row(5), person_row(7), person_row(9)]
        for r, y in zip(rows, ys):
            r.move_to([1.2, y, 0])
        labs = [T(s, 26, GREY) for s in ("generation 1", "generation 2", "generation 3", "almost everyone")]
        for l, y in zip(labs, ys):
            l.move_to([-4.6, y, 0])
        leg = VGroup(
            Circle(radius=0.17, stroke_color=PURPLE, fill_color=PURPLE, fill_opacity=0.9, stroke_width=2),
            T("shows the dominant trait", 24, PURPLE),
            Circle(radius=0.17, stroke_color=GREY, fill_color=GREY, fill_opacity=0.35, stroke_width=2),
            T("does not", 24, GREY)).arrange(RIGHT, buff=0.2).move_to([0.6, -3.05, 0])
        qmark = M("?", 56, YELLOW, weight=BOLD).move_to([5.75, -1.7, 0])

        self.at("dominant allele")
        guess = chip("the naive guess", RED, size=26).move_to([1.2, 3.2, 0])
        self.play(FadeIn(leg), FadeIn(guess), run_time=0.5)
        self.at("heterozygotes")
        self.play(FadeIn(labs[0]), LaggedStart(*[FadeIn(d, scale=0.6) for d in rows[0]], lag_ratio=0.08), run_time=1.0)
        self.at("generation by generation")
        self.play(FadeIn(labs[1]), LaggedStart(*[FadeIn(d, scale=0.6) for d in rows[1]], lag_ratio=0.06), run_time=0.9)
        self.play(FadeIn(labs[2]), LaggedStart(*[FadeIn(d, scale=0.6) for d in rows[2]], lag_ratio=0.06), run_time=0.9)
        self.at("almost everyone")
        self.play(FadeIn(labs[3]), LaggedStart(*[FadeIn(d, scale=0.6) for d in rows[3]], lag_ratio=0.05),
                  FadeIn(qmark, scale=1.4), run_time=1.1)
        self.at("mathematician")
        hardy = chip("G. H. Hardy, 1908", GOLD, size=26).to_corner(UR, buff=0.5)
        self.play(FadeIn(hardy, shift=DOWN * 0.15), run_time=0.6)
        self.at("His answer was no")
        no = M("no", 72, RED, weight=BOLD).move_to([5.75, 0.2, 0])
        cross = VGroup(Line([-5.7, 2.9, 0], [6.6, -2.3, 0], color=RED, stroke_width=8),
                       Line([-5.7, -2.3, 0], [6.6, 2.9, 0], color=RED, stroke_width=8)).set_opacity(0.0)
        self.play(FadeIn(no, scale=1.5), qmark.animate.set_opacity(0.2), run_time=0.7)
        self.wait(self.beat(0.05))
        self.at("starting point")
        self.play(FadeOut(VGroup(*rows, *labs, leg, no, qmark, hardy, guess)), run_time=0.6)
        end = T("population genetics", 50, font=TITLE_FONT).move_to([0, 0.2, 0])
        self.play(Write(end), run_time=1.0)
        self.finish()


# ---------------------------------------------------------------------------------------------
class S02Pool(SpokenScene):
    """a pool of M and N copies sorts into a bar split p and q."""

    def construct(self):
        rng = np.random.default_rng(7)
        center = np.array([-3.5, 0.5, 0.0])
        pts = []
        gx = np.linspace(-1.9, 1.9, 11)
        for x in gx:
            for y in gx:
                if x * x + y * y < 2.05 ** 2:
                    pts.append([x + rng.uniform(-0.12, 0.12), y + rng.uniform(-0.12, 0.12)])
        rng.shuffle(pts)
        n = len(pts)
        nm = int(round(n * P))
        dots = VGroup(*[allele_dot("M" if i < nm else "N", 0.15).move_to(center + [p[0], p[1], 0]) for i, p in enumerate(pts)])
        rng.shuffle(dots.submobjects)
        ring = Circle(radius=2.45, stroke_color=GREY, stroke_width=4).move_to(center)
        plab = T("one pool of eggs and sperm", 24, GREY).next_to(ring, DOWN, buff=0.25)

        self.at("every egg")
        self.play(Create(ring), FadeIn(plab), LaggedStart(*[FadeIn(d, scale=0.5) for d in dots], lag_ratio=0.01), run_time=1.8)
        self.at("two alleles")
        lm = chip("M", BLUE, size=30)
        ln = chip("N", YELLOW, size=30)
        leg = VGroup(lm, ln).arrange(RIGHT, buff=0.4).move_to([3.4, 3.0, 0])
        self.play(FadeIn(leg, shift=DOWN * 0.1), run_time=0.6)
        self.at("fraction of copies that are M")
        bar = split_bar(P, 6.2, 1.1).move_to([3.4, 1.4, 0])
        self.play(FadeIn(bar.a, shift=RIGHT * 0.3), FadeIn(bar.la), run_time=0.8)
        self.at("that are N")
        self.play(FadeIn(bar.b, shift=RIGHT * 0.3), FadeIn(bar.lb), run_time=0.8)
        self.at("p plus q")
        br = Brace(VGroup(bar.a, bar.b), UP, color=GREY, buff=0.12)
        eq = M("p + q = 1", 34, TEXT).next_to(br, UP, buff=0.12)
        self.play(FadeOut(leg), run_time=0.3)
        self.play(GrowFromCenter(br), FadeIn(eq), run_time=0.7)
        self.at("In a sample of")
        chp = chip("sample of 1,000 people", GREY, size=26).move_to([3.4, -0.5, 0])
        self.play(FadeIn(chp, shift=UP * 0.1), run_time=0.6)
        self.at("counting copies gives")
        pv = M("p = 0.5425", 34, BLUE, weight=BOLD)
        qv = M("q = 1 - p = 0.4575", 34, YELLOW, weight=BOLD)
        vals = VGroup(pv, qv).arrange(DOWN, buff=0.35, aligned_edge=LEFT).move_to([3.4, -2.2, 0])
        self.play(FadeIn(pv, shift=UP * 0.1), run_time=0.7)
        self.play(FadeIn(qv, shift=UP * 0.1), run_time=0.7)
        self.finish()


# ---------------------------------------------------------------------------------------------
class S03Square(SpokenScene):
    """the pool bar becomes the sides of a square; its areas are the genotype proportions."""

    def construct(self):
        sq = build_square()
        heads = square_heads()
        c = sq.cells
        self.at("drawing one egg")
        self.play(Create(VGroup(*[c[k] for k in c]).set_fill(opacity=0.0)), run_time=0.9)
        self.play(FadeIn(heads, shift=DOWN * 0.1), run_time=0.8)

        self.at("p times p")
        l_mm = cell_label(c["MM"], "MM", "p × p", BLUE)
        self.play(c["MM"].animate.set_fill(BLUE, 0.35), FadeIn(l_mm), run_time=0.7)
        self.at("two ways")
        self.play(Indicate(VGroup(c["MN"], c["NM"]), color=GREEN, scale_factor=1.03), run_time=0.8)
        self.at("has chance pq")
        l_mn = cell_label(c["MN"], "MN", "p q", GREEN)
        self.play(c["MN"].animate.set_fill(GREEN, 0.35), FadeIn(l_mn), run_time=0.7)
        self.at("reverse has chance")
        l_nm = cell_label(c["NM"], "MN", "q p", GREEN)
        self.play(c["NM"].animate.set_fill(GREEN, 0.35), FadeIn(l_nm), run_time=0.7)

        panel_x = 4.3
        tit = T("Hardy-Weinberg proportions", 26, GREY).move_to([panel_x, 2.6, 0])
        self.at("These are")
        self.play(FadeIn(tit), run_time=0.5)
        self.at("mm is")
        c_mm = chip("MM = p²", BLUE, size=36).move_to([panel_x, 1.4, 0])
        self.play(TransformFromCopy(c["MM"], c_mm), run_time=0.8)
        self.at("2pq")
        c_mn = chip("MN = 2pq", GREEN, size=36).move_to([panel_x, 0.0, 0])
        both = VGroup(c["MN"], c["NM"])
        self.play(TransformFromCopy(both, c_mn), run_time=0.9)
        self.at("and nn")
        l_nn = cell_label(c["NN"], "NN", "q × q", YELLOW)
        self.play(c["NN"].animate.set_fill(YELLOW, 0.35), FadeIn(l_nn), run_time=0.7)
        self.at("q squared")
        c_nn = chip("NN = q²", YELLOW, size=36).move_to([panel_x, -1.4, 0])
        self.play(TransformFromCopy(c["NN"], c_nn), run_time=0.8)
        self.finish()


# ---------------------------------------------------------------------------------------------
class S04Count(SpokenScene):
    """count the M copies: the M column of the square adds up to p."""

    def construct(self):
        sq = build_square()
        heads = square_heads()
        c = sq.cells
        cols = {"MM": (BLUE, "MM", "p × p"), "NM": (GREEN, "MN", "q p"), "MN": (GREEN, "MN", "p q"), "NN": (YELLOW, "NN", "q × q")}
        labs = VGroup(*[cell_label(c[k], g, e, col) for k, (col, g, e) in cols.items()])
        for k, (col, g, e) in cols.items():
            c[k].set_fill(col, 0.35)
        self.add(sq, heads, labs)

        self.at("count the M copies")
        # the M-from-the-egg column: MM and NM cells are in the left column (egg M)
        left = VGroup(c["MM"], c["MN"])
        box = SurroundingRectangle(left, color=GOLD, buff=0.04, stroke_width=7)
        # dim everything outside the column
        out = VGroup(c["NM"], c["NN"], labs[1], labs[3])
        self.play(Create(box), out.animate.set_opacity(0.3), run_time=0.9)

        x = 4.3
        f1 = M("p² + pq", 44, GOLD, weight=BOLD).move_to([x, 2.6, 0])
        self.at("fraction is")
        self.play(FadeIn(f1, shift=UP * 0.1), run_time=0.7)
        self.at("p times p plus q")
        f2 = M("= p (p + q)", 44, TEXT).move_to([x, 1.6, 0])
        self.play(FadeIn(f2, shift=UP * 0.1), run_time=0.7)
        self.at("Since p plus q")
        f3 = M("p + q = 1", 34, GREY).move_to([x, 0.7, 0])
        self.play(FadeIn(f3, shift=UP * 0.1), run_time=0.6)
        self.at("simply p")
        f4 = M("= p", 60, GREEN, weight=BOLD).move_to([x, -0.35, 0])
        self.play(FadeIn(f4, scale=1.3), run_time=0.7)

        self.at("allele frequency has not moved")
        w = 4.2
        l1 = T("this generation", 24, GREY).move_to([x - w / 2 + 0.9, -1.35, 0])
        b1 = split_bar(P, w, 0.55, size=26).move_to([x, -1.85, 0])
        l2 = T("next generation", 24, GREY).move_to([x - w / 2 + 0.95, -2.55, 0])
        b2 = split_bar(P, w, 0.55, size=26).move_to([x, -3.05, 0])
        self.play(FadeIn(l1), FadeIn(b1), run_time=0.6)
        self.play(FadeIn(l2), FadeIn(b2), run_time=0.6)
        self.at("whatever they were before")
        self.play(Indicate(VGroup(b1, b2), color=GREEN, scale_factor=1.04), run_time=0.8)
        self.finish()


# ---------------------------------------------------------------------------------------------
class S05Null(SpokenScene):
    """assumptions of the null model, then observed against expected counts."""

    def construct(self):
        items = ["large population", "random mating at this locus", "no selection", "no mutation", "no migration", "no drift"]
        chips = [chip(s, GREY, size=34, pad=0.28) for s in items]
        grid = VGroup(*chips)
        grid.arrange_in_grid(rows=3, cols=2, buff=(1.5, 0.75)).move_to([0.3, 1.0, 0])
        marks = []
        for ch in chips:
            m = VGroup()
            marks.append(m)
        self.at("population is large")
        self.play(FadeIn(chips[0], shift=RIGHT * 0.2), FadeIn(marks[0]), run_time=0.5)
        self.at("mating is random")
        self.play(FadeIn(chips[1], shift=RIGHT * 0.2), FadeIn(marks[1]), run_time=0.5)
        self.at("no selection")
        self.play(FadeIn(chips[2], shift=RIGHT * 0.2), FadeIn(marks[2]), run_time=0.4)
        self.play(FadeIn(chips[3], shift=RIGHT * 0.2), FadeIn(marks[3]), run_time=0.4)
        self.play(FadeIn(chips[4], shift=RIGHT * 0.2), FadeIn(marks[4]), run_time=0.4)
        self.play(FadeIn(chips[5], shift=RIGHT * 0.2), FadeIn(marks[5]), run_time=0.4)
        self.at("Real populations break these")
        cap = T("real populations can break any of these", 32, RED).move_to([0, -1.5, 0])
        self.play(FadeIn(cap, shift=UP * 0.1), run_time=0.8)
        self.at("null model")
        nm = chip("Hardy-Weinberg = null model", TEAL, size=34).move_to([0, -2.8, 0])
        self.play(FadeIn(nm, shift=UP * 0.15), run_time=0.7)

        self.at("In our sample")
        self.play(FadeOut(VGroup(grid, nm, cap)), run_time=0.6)

        # observed vs expected
        scale = 0.0085
        base = -2.3
        obs = [298, 489, 213]
        exp = [294.3, 496.4, 209.3]
        names = ["MM", "MN", "NN"]
        gx = [-5.2, -2.6, 0.0]
        base_line = Line([-6.4, base, 0], [1.2, base, 0], color=GREY, stroke_width=3)
        ob_bars, ex_bars, ob_l, ex_l, gl = [], [], [], [], []
        for x, o, e, nme in zip(gx, obs, exp, names):
            bo = Rectangle(width=0.95, height=o * scale, stroke_color=ORANGE, stroke_width=3, fill_color=ORANGE, fill_opacity=0.4)
            bo.move_to([x - 0.55, base + o * scale / 2, 0])
            be = Rectangle(width=0.95, height=e * scale, stroke_color=TEAL, stroke_width=3, fill_color=TEAL, fill_opacity=0.4)
            be.move_to([x + 0.55, base + e * scale / 2, 0])
            ob_bars.append(bo); ex_bars.append(be)
            ob_l.append(M(f"{o}", 24, ORANGE).next_to(bo, UP, buff=0.1))
            ex_l.append(M(f"{e}", 24, TEAL).next_to(be, UP, buff=0.1))
            gl.append(T(nme, 28, TEXT).move_to([x, base - 0.4, 0]))
        self.play(Create(base_line), FadeIn(VGroup(*gl)), run_time=0.6)
        self.at("observed counts")
        key1 = chip("observed", ORANGE, size=26).move_to([-4.2, 3.2, 0])
        self.play(FadeIn(key1), *[GrowFromEdge(b, DOWN) for b in ob_bars], run_time=0.9)
        self.play(FadeIn(VGroup(*ob_l)), run_time=0.4)
        self.at("expected ones")
        key2 = chip("expected", TEAL, size=26).move_to([-1.6, 3.2, 0])
        self.play(FadeIn(key2), *[GrowFromEdge(b, DOWN) for b in ex_bars], run_time=0.9)
        self.play(FadeIn(VGroup(*ex_l)), run_time=0.4)

        # chi-square panel
        px = 3.9
        self.at("square is")
        chi = M("chi-square = 0.22", 28, TEXT, weight=BOLD).move_to([px, 2.2, 0])
        scale_len = 4.0
        x0 = px - scale_len / 2
        u = scale_len / 4.5
        axis = Line([x0, 0.3, 0], [x0 + scale_len, 0.3, 0], color=GREY, stroke_width=4)
        t0 = M("0", 24, GREY).move_to([x0, -0.1, 0])
        mark = Triangle(color=ORANGE, fill_color=ORANGE, fill_opacity=1).scale(0.14).rotate(PI).move_to([x0 + 0.22 * u, 0.55, 0])
        self.play(FadeIn(chi, shift=DOWN * 0.1), Create(axis), FadeIn(t0), FadeIn(mark, shift=DOWN * 0.2), run_time=0.9)
        self.at("critical value")
        crit = Line([x0 + 3.84 * u, 0.0, 0], [x0 + 3.84 * u, 0.9, 0], color=RED, stroke_width=6)
        cl = M("3.84", 26, RED, weight=BOLD).move_to([x0 + 3.84 * u, -0.35, 0])
        ct = T("critical value", 24, RED).move_to([px + 0.2, 1.35, 0])
        self.play(Create(crit), FadeIn(cl), FadeIn(ct), run_time=0.8)
        self.at("one degree of freedom")
        df = T("1 degree of freedom", 26, GREY).move_to([px, -1.2, 0])
        self.play(FadeIn(df), run_time=0.5)
        self.at("no evidence of departure")
        ok = chip("no evidence of departure", GREEN, size=26).move_to([px, -2.4, 0])
        self.play(FadeIn(ok, shift=UP * 0.1), run_time=0.7)
        self.finish()


# ---------------------------------------------------------------------------------------------
class S06Rule(SpokenScene):
    """dominance acts inside a person; to change frequencies something must act on the population."""

    def construct(self):
        # one person with two alleles
        body = Circle(radius=1.0, stroke_color=PURPLE, stroke_width=4, fill_color=PURPLE, fill_opacity=0.15).move_to([-4.6, 2.4, 0])
        d1 = allele_dot("M", 0.2).move_to(body.get_center() + LEFT * 0.35)
        d2 = allele_dot("N", 0.2).move_to(body.get_center() + RIGHT * 0.35)
        plab = T("inside one person", 26, PURPLE).next_to(body, RIGHT, buff=0.35)
        self.at("Dominance describes")
        self.play(FadeIn(body, scale=0.8), FadeIn(d1), FadeIn(d2), FadeIn(plab), run_time=0.9)

        bar = split_bar(P, 10.0, 1.6, size=40).move_to([0, 0.0, 0])
        self.at("how common they become")
        com = T("how common each allele is in the population", 28, GREY).move_to([0, -1.25, 0])
        self.play(FadeIn(bar), FadeIn(com), run_time=0.9)
        self.at("something has to act")
        arrow = Arrow([3.2, 2.7, 0], [1.2, 0.9, 0], color=RED, stroke_width=8, buff=0.0)
        act = chip("something acts on the population", RED, size=28).move_to([3.4, 3.1, 0])
        new = split_bar(0.38, 10.0, 1.6, size=40).move_to([0, 0.0, 0])
        self.play(FadeIn(act), GrowArrow(arrow), run_time=0.7)
        self.play(ReplacementTransform(bar, new), run_time=1.0)
        self.at("Keep this rule")
        bar2 = split_bar(P, 10.0, 1.6, size=40).move_to([0, 0.0, 0])
        self.play(FadeOut(VGroup(act, arrow)), ReplacementTransform(new, bar2), run_time=0.9)
        self.at("With nothing acting")
        hold = chip("nothing acts: p stays put", GREEN, size=36).move_to([0, -2.7, 0])
        self.play(FadeIn(hold, shift=UP * 0.15), run_time=0.7)
        self.finish()


class S07End(EndCard):
    LINE = "With nothing acting, allele frequencies stay put."
