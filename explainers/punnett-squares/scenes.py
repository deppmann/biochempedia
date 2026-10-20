"""Mendel and Punnett squares: where the white was hiding  (Biochemistrypedia explainer)

COLOR MAP (one color per concept, whole video)
  PURPLE = the P allele, purple flowers
  WHITE  = the p allele, white flowers
  YELLOW = chance (probability, 1/2, 1/4, 50 percent)
  TEAL   = a vocabulary term label (gene, allele, genotype, phenotype, Punnett square ...)
  GREY   = outlines, cells, DNA bars, generation labels
"""
import numpy as np
from bp_style import *  # noqa: F401,F403

PURPLE = "#B58CD9"
WHITE = "#FFFFFF"


def tok(letter, color, size=0.8, shown=True):
    """An allele token: a rounded square in the allele's colour with its letter."""
    box = RoundedRectangle(corner_radius=0.14, width=size, height=size, stroke_color=color, stroke_width=3,
                           fill_color=color, fill_opacity=0.9)
    lt = T(letter, int(size * 46), BG, weight=BOLD).move_to(box)
    if not shown:
        lt.set_opacity(0)
    g = VGroup(box, lt)
    g.box, g.lt = box, lt
    return g


def swatch(color, size=1.0):
    """A flower-colour swatch (not a drawn flower)."""
    return RoundedRectangle(corner_radius=0.16, width=size, height=size, stroke_color=color, stroke_width=3,
                            fill_color=color, fill_opacity=0.9)


def arr(a, b, color=GREY, w=5, tip=0.22):
    return Arrow(a, b, buff=0.06, color=color, stroke_width=w, tip_length=tip,
                 max_tip_length_to_length_ratio=0.45, max_stroke_width_to_length_ratio=12)


def term(text, size=30, color=TEAL):
    return T(text, size, color, weight=BOLD)


class S00Title(TitleCard):
    LESSON = "Mendel and Punnett squares"
    TITLE = "Where the white was hiding"


# ---------------------------------------------------------------------------------------------
class S01Hidden(SpokenScene):
    """purple x white -> all purple -> self-fertilize -> white returns -> the question."""

    def construct(self):
        # row 1: the cross
        p1 = swatch(PURPLE).move_to([-1.6, 2.9, 0])
        p2 = swatch(WHITE).move_to([1.6, 2.9, 0])
        cross = T("×", 44, GREY).move_to([0, 2.9, 0])
        l1 = T("purple flowers", 24, PURPLE).next_to(p1, DOWN, buff=0.15)
        l2 = T("white flowers", 24, WHITE).next_to(p2, DOWN, buff=0.15)
        g1 = T("cross", 24, GREY).move_to([-5.2, 2.9, 0])
        self.at("with purple flowers")
        self.play(FadeIn(p1, scale=0.9), FadeIn(l1), FadeIn(g1), run_time=0.5)
        self.at("with white flowers")
        self.play(FadeIn(cross), FadeIn(p2, scale=0.9), FadeIn(l2), run_time=0.5)

        # row 2: all purple
        xs = [-1.8, -0.6, 0.6, 1.8]
        r2 = VGroup(*[swatch(PURPLE, 0.9).move_to([x, 0.75, 0]) for x in xs])
        a1 = arr([0, 1.55, 0], [0, 1.3, 0])
        a1.put_start_and_end_on([0, 1.85, 0], [0, 1.3, 0])
        g2 = T("offspring", 24, GREY).move_to([-5.2, 0.75, 0])
        n2 = T("all purple", 26, PURPLE).move_to([4.2, 0.75, 0])
        self.at("Every offspring")
        self.play(GrowArrow(a1), FadeIn(g2), run_time=0.4)
        self.play(LaggedStart(*[FadeIn(s, scale=0.8) for s in r2], lag_ratio=0.15), FadeIn(n2), run_time=0.9)

        # row 3: self-fertilize, white returns
        a2 = arr([0, 0.1, 0], [0, -0.55, 0])
        sf = T("fertilize themselves", 24, GREY).next_to(a2, RIGHT, buff=0.2)
        g3 = T("next generation", 24, GREY).move_to([-5.0, -1.4, 0])
        self.at("fertilized themselves")
        self.play(GrowArrow(a2), FadeIn(sf), FadeIn(g3), run_time=0.5)
        r3 = VGroup(*[swatch(PURPLE if i < 3 else WHITE, 0.9).move_to([x, -1.4, 0]) for i, x in enumerate(xs)])
        # shuffle so white is not always last? keep one white, position fixed for the story
        self.at("White flowers came back")
        self.play(LaggedStart(*[FadeIn(s, scale=0.8) for s in r3], lag_ratio=0.12), run_time=0.8)
        white = r3[3]
        n3a = T("white is back: about 1 in 4 on average", 26, YELLOW)
        n3b = T("any one batch can differ", 22, GREY)
        n3 = VGroup(n3a, n3b).arrange(DOWN, buff=0.12).move_to([0, -2.85, 0])
        self.at("about one plant in four")
        self.play(FadeIn(n3), Indicate(white, color=WHITE, scale_factor=1.25), run_time=0.7)

        # the question
        q1 = T("Why do you look like your parents,", 34, TEXT)
        q1b = T("but not exactly?", 34, TEXT)
        q = VGroup(q1, q1b).arrange(DOWN, buff=0.15).move_to([0, 2.5, 0])
        keep = white
        others = VGroup(p1, p2, cross, l1, l2, g1, a1, g2, n2, a2, sf, g3, n3, r2, VGroup(*r3[:3]))
        self.at("Why do you look")
        self.play(FadeOut(others), keep.animate.scale(1.5).move_to([0, -0.5, 0]), FadeIn(q), run_time=0.9)
        mark = T("?", 56, BG, weight=BOLD).move_to(keep)
        self.play(FadeIn(mark), run_time=0.3)
        q2 = T("How can we predict the odds?", 34, YELLOW).move_to([0, -2.2, 0])
        self.at("predict the odds")
        self.play(FadeIn(q2, shift=UP * 0.15), run_time=0.5)
        self.finish()


# ---------------------------------------------------------------------------------------------
class S02Allele(SpokenScene):
    """DNA -> gene block -> two allele versions -> a cell holding two alleles -> letters."""

    def construct(self):
        # DNA as two parallel bars (never a helix)
        bar1 = Rectangle(width=9.6, height=0.24, stroke_color=GREY, stroke_width=2, fill_color=GREY, fill_opacity=0.5)
        bar2 = bar1.copy()
        bars = VGroup(bar1, bar2).arrange(DOWN, buff=0.18).move_to([0.6, 2.6, 0])
        dna = T("DNA", 28, GREY).move_to([-5.6, 2.6, 0])
        gene_box = Rectangle(width=2.8, height=0.95, stroke_color=TEAL, stroke_width=4, fill_color=TEAL, fill_opacity=0.35)
        gene_box.move_to(bars.get_center())
        gene_lbl = term("gene", 30).next_to(gene_box, UP, buff=0.25)
        self.at("A gene is a section")
        self.play(FadeIn(bars), FadeIn(dna), run_time=0.5)
        self.play(FadeIn(gene_box, scale=0.9), FadeIn(gene_lbl), run_time=0.5)

        # two alleles
        tp = tok("P", PURPLE, 1.0, shown=False).move_to([-2.6, 0.2, 0])
        tw = tok("p", WHITE, 1.0, shown=False).move_to([2.6, 0.2, 0])
        ap = arr(gene_box.get_bottom() + LEFT * 0.7, tp.get_top() + UP * 0.05, TEAL)
        aw = arr(gene_box.get_bottom() + RIGHT * 0.7, tw.get_top() + UP * 0.05, TEAL)
        al_lbl = term("allele", 30).move_to([0, 0.2, 0])
        self.at("one version of a gene")
        self.play(GrowArrow(ap), GrowArrow(aw), FadeIn(tp, scale=0.8), FadeIn(tw, scale=0.8), FadeIn(al_lbl), run_time=0.8)
        lp = T("purple allele", 24, PURPLE).next_to(tp, DOWN, buff=0.12)
        lw = T("white allele", 24, WHITE).next_to(tw, DOWN, buff=0.12)
        self.at("with a purple allele")
        self.play(FadeIn(lp), run_time=0.3)
        self.at("and a white allele")
        self.play(FadeIn(lw), run_time=0.3)

        # a cell with two alleles
        cell = RoundedRectangle(corner_radius=0.5, width=5.4, height=1.9, stroke_color=GREY, stroke_width=4,
                                fill_color=GREY, fill_opacity=0.1).move_to([0, -2.35, 0])
        cl = T("body cell", 24, GREY).next_to(cell, LEFT, buff=0.2)
        c1 = tok("P", PURPLE, 0.8, shown=False).move_to([-1.2, -2.2, 0])
        c2 = tok("p", WHITE, 0.8, shown=False).move_to([1.2, -2.2, 0])
        f1 = T("from parent 1", 22, GREY).move_to([-1.2, -2.95, 0])
        f2 = T("from parent 2", 22, GREY).move_to([1.2, -2.95, 0])
        self.at("body cells carry two alleles")
        self.play(FadeIn(cell), FadeIn(cl), FadeIn(c1, scale=0.8), FadeIn(c2, scale=0.8), run_time=0.7)
        self.at("one from each parent")
        self.play(FadeIn(f1), FadeIn(f2), run_time=0.4)
        self.at("as letters")
        self.play(*[m.lt.animate.set_opacity(1) for m in (tp, tw, c1, c2)], run_time=0.5)
        self.at("capital P")
        self.play(Indicate(tp, color=PURPLE, scale_factor=1.2), run_time=0.5)
        self.at("small p")
        self.play(Indicate(tw, color=WHITE, scale_factor=1.2), run_time=0.5)
        self.finish()


# ---------------------------------------------------------------------------------------------
class S03Dominant(SpokenScene):
    """three genotype cards -> phenotype; dominant, recessive, homozygous, heterozygous; the hidden p."""

    def construct(self):
        cols = {"PP": -2.0, "Pp": 1.5, "pp": 5.0}
        card = {}
        for g, x in cols.items():
            a = tok(g[0], PURPLE if g[0] == "P" else WHITE, 0.8)
            b = tok(g[1], PURPLE if g[1] == "P" else WHITE, 0.8)
            pair = VGroup(a, b).arrange(RIGHT, buff=0.2).move_to([x, 1.5, 0])
            col = PURPLE if "P" in g else WHITE
            ar = arr([x, 0.8, 0], [x, 0.0, 0])
            sw = swatch(col, 1.0).move_to([x, -0.75, 0])
            nm = T("purple" if "P" in g else "white", 26, col).next_to(sw, DOWN, buff=0.15)
            card[g] = dict(pair=pair, ar=ar, sw=sw, nm=nm, a=a, b=b)

        def show(g):
            c = card[g]
            return [FadeIn(c["pair"], scale=0.9), GrowArrow(c["ar"]), FadeIn(c["sw"], scale=0.9), FadeIn(c["nm"])]

        dom = term("dominant", 40).move_to([0, 3.1, 0])
        self.at("A dominant allele")
        self.play(FadeIn(dom), *show("Pp"), run_time=0.9)
        self.play(Indicate(card["Pp"]["a"], color=PURPLE, scale_factor=1.25), run_time=0.6)
        rec = term("recessive", 40).move_to([0, 3.1, 0])
        self.at("A recessive allele")
        self.play(ReplacementTransform(dom, rec), *show("pp"), run_time=0.9)
        self.play(Indicate(VGroup(card["pp"]["a"], card["pp"]["b"]), color=WHITE, scale_factor=1.15), run_time=0.6)

        geno = term("genotype", 30).move_to([-5.1, 1.5, 0])
        self.at("pair of alleles")
        self.play(FadeOut(rec), FadeIn(geno), *show("PP"), run_time=0.8)
        pheno = term("phenotype", 30).move_to([-5.1, -0.75, 0])
        self.at("The trait you can see")
        self.play(FadeIn(pheno), run_time=0.5)
        self.play(*[Indicate(card[g]["sw"], color=TEXT, scale_factor=1.15) for g in cols], run_time=0.7)

        homo1 = term("homozygous", 26).move_to([cols["PP"], -2.7, 0])
        homo2 = term("homozygous", 26).move_to([cols["pp"], -2.7, 0])
        het = term("heterozygous", 26).move_to([cols["Pp"], -2.7, 0])
        self.at("Same")
        self.play(FadeIn(homo1), FadeIn(homo2), run_time=0.5)
        self.at("Different alleles")
        self.play(FadeIn(het), run_time=0.5)
        hid = SurroundingRectangle(card["Pp"]["b"], color=YELLOW, buff=0.1, stroke_width=4)
        hl = T("a white allele is still there", 26, YELLOW).move_to([2.2, 3.1, 0])
        self.at("still carries a white allele")
        self.play(Create(hid), FadeIn(hl), run_time=0.6)
        self.finish()


# ---------------------------------------------------------------------------------------------
class S04Chance(SpokenScene):
    """Pp cell -> two sex cells; probability line 0 to 1; 50 percent each."""

    def construct(self):
        cell = RoundedRectangle(corner_radius=0.45, width=2.8, height=1.3, stroke_color=GREY, stroke_width=4,
                                fill_color=GREY, fill_opacity=0.1).move_to([0, 2.8, 0])
        a = tok("P", PURPLE, 0.8).move_to([-0.55, 2.8, 0])
        b = tok("p", WHITE, 0.8).move_to([0.55, 2.8, 0])
        lbl = T("Pp plant cell", 24, GREY).next_to(cell, LEFT, buff=0.3)
        self.at("makes sex cells")
        self.play(FadeIn(cell), FadeIn(a), FadeIn(b), FadeIn(lbl), run_time=0.7)

        s1 = Circle(radius=0.8, stroke_color=GREY, stroke_width=4, fill_color=GREY, fill_opacity=0.1).move_to([-3.0, 0.5, 0])
        s2 = s1.copy().move_to([3.0, 0.5, 0])
        sl1 = T("sex cell", 24, GREY).next_to(s1, DOWN, buff=0.15)
        sl2 = T("sex cell", 24, GREY).next_to(s2, DOWN, buff=0.15)
        self.at("its two alleles separate")
        self.play(FadeIn(s1), FadeIn(s2), a.animate.move_to(s1.get_center()), b.animate.move_to(s2.get_center()),
                  run_time=1.1)
        self.play(FadeIn(sl1), FadeIn(sl2), run_time=0.3)
        self.at("Each sex cell gets one allele")
        self.play(Indicate(s1, color=PURPLE), Indicate(s2, color=WHITE), run_time=0.7)
        seg = term("law of segregation", 30).move_to([0, 0.5, 0])
        self.at("law of segregation")
        self.play(FadeIn(seg), run_time=0.5)

        # probability line
        line = Line([-4, -2.2, 0], [4, -2.2, 0], color=GREY, stroke_width=5)
        t0 = Line([-4, -2.0, 0], [-4, -2.4, 0], color=GREY, stroke_width=5)
        t1 = Line([4, -2.0, 0], [4, -2.4, 0], color=GREY, stroke_width=5)
        l0 = T("0  never", 26, GREY).move_to([-4, -2.9, 0])
        l1 = T("1  always", 26, GREY).move_to([4, -2.9, 0])
        pr = term("probability", 30).move_to([0, -1.4, 0])
        self.at("Probability is the chance")
        self.play(FadeOut(seg), FadeIn(pr), Create(line), Create(t0), Create(t1), FadeIn(l0), FadeIn(l1), run_time=0.9)
        dot = Dot([0, -2.2, 0], radius=0.16, color=YELLOW)
        half = T("1/2 = 50 percent", 26, YELLOW).move_to([0, -2.9, 0])
        t50a = T("50%", 34, YELLOW, weight=BOLD).next_to(s1, UP, buff=0.3)
        t50b = T("50%", 34, YELLOW, weight=BOLD).next_to(s2, UP, buff=0.3)
        self.at("of carrying capital")
        self.play(FadeIn(dot, scale=1.5), FadeIn(half), FadeIn(t50a), run_time=0.6)
        self.at("small p")
        self.play(FadeIn(t50b), run_time=0.5)
        self.finish()


# ---------------------------------------------------------------------------------------------
class S05Square(SpokenScene):
    """build the 2x2 Punnett square for Pp x Pp, tag 1/4, colour 3 purple 1 white."""

    def construct(self):
        title = term("Punnett square", 40).move_to([0, 3.2, 0])
        S = 2.0
        gx, gy = 0.8, -0.9   # grid centre
        boxes = {}
        for i in range(2):         # i = column (top allele), j = row (side allele)
            for j in range(2):
                r = Rectangle(width=S, height=S, stroke_color=GREY, stroke_width=4, fill_color=GREY, fill_opacity=0.08)
                r.move_to([gx + (i - 0.5) * S, gy + (0.5 - j) * S, 0])
                boxes[(i, j)] = r
        grid = VGroup(*boxes.values())
        self.at("A Punnett square is a grid")
        self.play(FadeIn(title), Create(grid), run_time=0.9)

        top_lbl = T("sex cells of parent one", 24, GREY).move_to([gx, 2.55, 0])
        side_lbl = T("sex cells\nof parent two", 24, GREY, line_spacing=0.8).move_to([-4.6, gy, 0])
        top = [tok("P", PURPLE, 0.7), tok("p", WHITE, 0.7)]
        side = [tok("P", PURPLE, 0.7), tok("p", WHITE, 0.7)]
        for i in range(2):
            top[i].move_to([gx + (i - 0.5) * S, gy + S + 0.65, 0])
            side[i].move_to([gx - S - 0.65, gy + (0.5 - i) * S, 0])
        self.at("across the top")
        self.play(FadeIn(top_lbl), LaggedStart(*[FadeIn(t, scale=0.8) for t in top], lag_ratio=0.3), run_time=0.8)
        self.at("down the side")
        self.play(FadeIn(side_lbl), LaggedStart(*[FadeIn(t, scale=0.8) for t in side], lag_ratio=0.3), run_time=0.8)

        names = {(0, 0): "PP", (1, 0): "Pp", (0, 1): "Pp", (1, 1): "pp"}
        labs = {k: T(v, 46, TEXT, weight=BOLD).move_to(boxes[k]) for k, v in names.items()}
        self.at("Cross two")
        self.wait(0.1)
        self.at("The boxes read")
        t0, t1 = self.t_of("The boxes read"), self.t_of("Each box has")
        for n, k in enumerate([(0, 0), (1, 0), (0, 1), (1, 1)]):
            rest = t0 + (t1 - t0 - 0.2) * n / 4 - self.elapsed()
            if rest > 0.02:
                self.wait(rest)
            self.play(FadeIn(labs[k], scale=0.8), run_time=0.4)

        tags = {k: T("1/4", 26, YELLOW).move_to(boxes[k].get_corner(UR) + DL * 0.35) for k in boxes}
        self.at("Each box has")
        self.play(*[FadeIn(t) for t in tags.values()], run_time=0.6)

        def paint(k, col):
            return [boxes[k].animate.set_fill(col, 0.5).set_stroke(col)]

        r1 = T("3 purple", 34, PURPLE, weight=BOLD).move_to([5.2, 0.2, 0])
        r2 = T("1 white", 34, WHITE, weight=BOLD).move_to([5.2, -1.4, 0])
        self.at("Three boxes look purple")
        self.play(*paint((0, 0), PURPLE), *paint((1, 0), PURPLE), *paint((0, 1), PURPLE), FadeIn(r1), run_time=0.6)
        self.at("One looks white")
        self.play(*paint((1, 1), WHITE), FadeIn(r2), run_time=0.6)
        self.finish()


# ---------------------------------------------------------------------------------------------
class S06Answer(SpokenScene):
    """where the white hid; 1 in 4; chances not certainties; four seeds could hold no white."""

    def construct(self):
        q = T("Where was the white hiding?", 40, TEXT).move_to([0, 3.1, 0])
        self.at("where was the white hiding")
        self.play(FadeIn(q, shift=DOWN * 0.1), run_time=0.5)

        plant = RoundedRectangle(corner_radius=0.3, width=4.0, height=2.5, stroke_color=PURPLE, stroke_width=4,
                                 fill_color=PURPLE, fill_opacity=0.15).move_to([-3.4, 0.6, 0])
        a = tok("P", PURPLE, 0.9).move_to(plant.get_center() + LEFT * 0.7 + UP * 0.45)
        b = tok("p", WHITE, 0.9).move_to(plant.get_center() + RIGHT * 0.7 + UP * 0.45)
        nm = T("Pp plant: purple", 26, PURPLE).next_to(plant, DOWN, buff=0.2)
        self.at("Inside each")
        self.play(FadeIn(plant), FadeIn(a), FadeIn(b), FadeIn(nm), run_time=0.7)
        wl = T("white allele", 26, WHITE).next_to(b, DOWN, buff=0.1)
        self.at("as a white allele")
        self.play(Indicate(b, color=YELLOW, scale_factor=1.3), FadeIn(wl), run_time=0.7)

        # mini square, pp lit
        S = 1.1
        mb = {}
        for i in range(2):
            for j in range(2):
                r = Rectangle(width=S, height=S, stroke_color=GREY, stroke_width=3, fill_color=GREY, fill_opacity=0.08)
                r.move_to([3.4 + (i - 0.5) * S, 0.6 + (0.5 - j) * S, 0])
                mb[(i, j)] = r
        mini = VGroup(*mb.values())
        pp = T("pp", 30, BG, weight=BOLD).move_to(mb[(1, 1)])
        c14 = T("1 in 4", 34, YELLOW, weight=BOLD).move_to([3.4, -1.3, 0])
        self.at("one in four chance")
        self.play(Create(mini), run_time=0.5)
        self.play(mb[(1, 1)].animate.set_fill(WHITE, 0.9).set_stroke(WHITE), FadeIn(pp), FadeIn(c14), run_time=0.6)
        two = T("two white alleles", 26, WHITE).move_to([3.4, 2.15, 0])
        self.at("two white alleles")
        self.play(FadeIn(two), run_time=0.4)

        # the rule
        rule = T("chances, not certainties", 44, YELLOW, font=TITLE_FONT).move_to([0, 2.4, 0])
        self.at("gives chances")
        self.play(FadeOut(VGroup(q, plant, a, b, nm, wl, mini, pp, c14, two)), FadeIn(rule), run_time=0.7)
        seeds = VGroup(*[swatch(PURPLE, 1.0).move_to([x, 0.0, 0]) for x in [-2.25, -0.75, 0.75, 2.25]])
        sl = T("4 seeds from two Pp plants", 28, GREY).move_to([0, -1.1, 0])
        zero = T("0 white: possible", 30, WHITE, weight=BOLD).move_to([0, -2.0, 0])
        self.at("Four seeds")
        self.play(LaggedStart(*[FadeIn(s, scale=0.8) for s in seeds], lag_ratio=0.15), FadeIn(sl), run_time=0.9)
        self.at("no white plants at all")
        self.play(FadeIn(zero), run_time=0.5)
        self.finish()


class S07End(EndCard):
    LINE = "A Punnett square gives chances, not certainties."
