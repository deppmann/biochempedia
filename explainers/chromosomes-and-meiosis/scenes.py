"""Chromosomes and meiosis: Mendel's laws are chromosome movements  (Biochemistrypedia explainer)

COLOR MAP (one color per concept, whole video)
  BLUE    = the homolog that carries the capital allele (A, B)
  ORANGE  = the homolog that carries the small allele (a, b)
  NEUTRAL = a chromosome with no allele shown yet
  GREY    = cell outlines, spindle poles and fibres, panel frames
  TEAL    = the name of the stage (S phase, Prophase I, ...)
  GREEN   = haploid cells and finished gametes
  YELLOW  = the highlight: what is being asked, counted or moved
  RED     = the step that does not happen (no S phase before meiosis II)
  TEXT    = the centromere dot and the join between sister chromatids
"""
import numpy as np
from bp_style import *  # noqa: F401,F403

ORANGE = "#F29E4C"
NEUTRAL = "#B8BFCC"
LEN = 2.2
CELLC = np.array([0.0, -0.25, 0.0])


# ---------------------------------------------------------------------------------------------
# helpers
# ---------------------------------------------------------------------------------------------
def bchip(text, color=BLUE, size=26, **kw):
    c = chip(text, color, size=size, **kw)
    back = RoundedRectangle(corner_radius=0.14, width=c[0].width, height=c[0].height, stroke_width=0,
                            fill_color=BG, fill_opacity=1).move_to(c[0])
    return VGroup(back, *c)


def cell(c, r, color=GREY):
    return Circle(radius=r, stroke_color=color, stroke_width=4, fill_color=color, fill_opacity=0.07).move_to(c)


def sister(label, color, L, w=0.26):
    body = RoundedRectangle(corner_radius=w / 2, width=w, height=L, stroke_color=color, stroke_width=3,
                            fill_color=color, fill_opacity=0.4)
    dot = Circle(radius=0.09, stroke_width=0, fill_color=TEXT, fill_opacity=1).move_to(body)
    g = VGroup(body, dot)
    if label:
        g.add(T(label, 26, color, weight=BOLD).next_to(body, UP, buff=0.08))
    g.body, g.dot = body, dot
    return g


class Chrom:
    """A chromosome: one chromatid, or two sister chromatids joined at the centromere."""

    def __init__(self, label, color, L=LEN, rep=True, w=0.26):
        off = w / 2 + 0.04
        if rep:
            self.sis = [sister(label, color, L, w).shift(LEFT * off), sister(label, color, L, w).shift(RIGHT * off)]
            self.join = Line(self.sis[0].dot.get_center(), self.sis[1].dot.get_center(), color=TEXT, stroke_width=6)
        else:
            self.sis = [sister(label, color, L, w)]
            self.join = None

    def mobs(self):
        return self.sis + ([self.join] if self.join is not None else [])

    def cc(self):
        return np.mean([s.body.get_center() for s in self.sis], axis=0)

    def place(self, p):
        v = np.array(p, float) - self.cc()
        for m in self.mobs():
            m.shift(v)
        return self

    def shift(self, v):
        return [m.animate.shift(v) for m in self.mobs()]

    def group(self):
        return VGroup(*self.mobs())


def bracket(x0, x1, y, color=GREY, tick=0.15):
    return VGroup(Line([x0, y + tick, 0], [x0, y, 0], color=color, stroke_width=4),
                  Line([x0, y, 0], [x1, y, 0], color=color, stroke_width=4),
                  Line([x1, y, 0], [x1, y + tick, 0], color=color, stroke_width=4))


def pole(p):
    return Circle(radius=0.14, stroke_color=GREY, stroke_width=3, fill_color=GREY, fill_opacity=0.8).move_to(p)


def fibre(pl, target):
    return Line(pl, target, color=GREY, stroke_width=2.5)


def heading(text, color=TEAL, size=34):
    return T(text, size, color, weight=BOLD).move_to([0, 3.2, 0])


def ring(m, color=YELLOW, r=0.26):
    return Circle(radius=r, stroke_color=color, stroke_width=4).move_to(m.get_center())


class S00Title(TitleCard):
    LESSON = "Chromosomes and meiosis"
    TITLE = "Mendel's laws are chromosome movements"


# ---------------------------------------------------------------------------------------------
class S01Question(SpokenScene):
    """8 chromosomes -> ? -> 4 slots. The unknown box becomes 'meiosis'."""

    def construct(self):
        lc, rc = np.array([-3.6, -0.2, 0]), np.array([4.0, 0.0, 0])
        big = cell(lc, 2.9)
        lens = [1.6, 1.3, 1.1, 0.8]
        spots = [(-1.0, 0.95), (1.0, 0.95), (-1.0, -0.95), (1.0, -0.95)]
        pairs = []
        for L, (x, y) in zip(lens, spots):
            a = sister(None, NEUTRAL, L).move_to(lc + [x - 0.17, y, 0])
            b = sister(None, NEUTRAL, L).move_to(lc + [x + 0.17, y, 0])
            pairs.append(VGroup(a, b))
        n8 = VGroup(M("8", 50, TEXT), T("chromosomes", 30, TEXT)).arrange(RIGHT, buff=0.25, aligned_edge=DOWN).move_to([lc[0], 3.15, 0])

        small = cell(rc, 1.9)
        slots = []
        for (x, y) in [(-0.6, 0.0), (0.6, 0.0), (-0.0, 0.0)][:2]:
            pass
        slot_pos = [(-0.62, 0.62), (0.62, 0.62), (-0.62, -0.62), (0.62, -0.62)]
        for (x, y) in slot_pos:
            box = DashedVMobject(RoundedRectangle(corner_radius=0.2, width=0.55, height=0.95, stroke_color=NEUTRAL, stroke_width=3),
                                 num_dashes=18)
            q = T("?", 34, YELLOW, weight=BOLD)
            slots.append(VGroup(box, q).move_to(rc + [x, y, 0]))
        n4 = VGroup(M("4", 50, TEXT), T("chromosomes", 30, TEXT)).arrange(RIGHT, buff=0.25, aligned_edge=DOWN).move_to([rc[0], 2.55, 0])

        self.at("fruit fly cell")
        self.play(Create(big), run_time=0.7)
        self.play(LaggedStart(*[FadeIn(p, scale=0.8) for p in pairs], lag_ratio=0.25), FadeIn(n8), run_time=1.5)
        self.at("eggs and sperm")
        self.play(Create(small), FadeIn(n4), run_time=0.7)
        self.play(LaggedStart(*[FadeIn(s, scale=0.8) for s in slots], lag_ratio=0.2), run_time=1.0)
        self.at("which four")
        self.play(*[Indicate(s[1], color=YELLOW, scale_factor=1.5) for s in slots], run_time=1.0)
        self.at("Mendel worked")
        ar = Arrow([-0.55, -0.2, 0], [2.0, -0.2, 0], buff=0, color=GREY, stroke_width=6, tip_length=0.28)
        self.play(GrowArrow(ar), run_time=0.8)
        self.at("never saw")
        q = bchip("?", YELLOW, 40).move_to([0.72, -0.2, 0])
        self.play(FadeIn(q, scale=0.7), run_time=0.5)
        self.play(Indicate(VGroup(*q[1:]), color=YELLOW, scale_factor=1.15), run_time=0.8)
        self.at("called meiosis")
        mei = bchip("meiosis", YELLOW, 30).move_to([0.72, -0.2, 0])
        self.play(ReplacementTransform(q, mei), run_time=0.7)
        self.finish()


# ---------------------------------------------------------------------------------------------
class S02Pair(SpokenScene):
    """One pair of homologs: allele colours, then S phase makes sister chromatids joined at a centromere."""

    def construct(self):
        cl = cell(CELLC, 3.0)
        n1 = Chrom(None, NEUTRAL, rep=False).place(CELLC + LEFT * 1.0)
        n2 = Chrom(None, NEUTRAL, rep=False).place(CELLC + RIGHT * 1.0)
        self.play(Create(cl), FadeIn(n1.group()), FadeIn(n2.group()), run_time=1.0)

        self.at("two members")
        br = bracket(-1.15, 1.15, CELLC[1] - 1.45)
        lab = T("homologs", 30, TEXT).next_to(br, DOWN, buff=0.12)
        self.play(Create(br), FadeIn(lab), run_time=0.8)

        self.at("each parent")
        self.play(Indicate(n1.sis[0], color=YELLOW, scale_factor=1.08), run_time=0.6)
        self.play(Indicate(n2.sis[0], color=YELLOW, scale_factor=1.08), run_time=0.6)
        self.at("one gene")
        yb = CELLC[1] + 0.55
        bands = VGroup(*[Rectangle(width=0.26, height=0.16, stroke_width=0, fill_color=YELLOW, fill_opacity=1).move_to([CELLC[0] + x, yb, 0]) for x in (-1.0, 1.0)])
        self.play(FadeIn(bands, scale=1.5), run_time=0.6)
        self.at("capital")
        self.play(FadeOut(bands), run_time=0.3)
        cA = Chrom("A", BLUE, rep=False).place(CELLC + LEFT * 1.0)
        ca = Chrom("a", ORANGE, rep=False).place(CELLC + RIGHT * 1.0)
        self.play(ReplacementTransform(n1.sis[0], cA.sis[0]), FadeOut(br), FadeOut(lab), run_time=0.7)
        self.at("small a")
        self.play(ReplacementTransform(n2.sis[0], ca.sis[0]), run_time=0.7)

        self.at("S phase")
        chS = chip("S phase", TEAL, 30).move_to([0, 3.2, 0])
        rA = Chrom("A", BLUE).place(CELLC + LEFT * 1.0)
        ra = Chrom("a", ORANGE).place(CELLC + RIGHT * 1.0)
        cpA, cpa = cA.sis[0].copy(), ca.sis[0].copy()
        self.add(cpA, cpa)
        self.play(FadeIn(chS, shift=DOWN * 0.2), run_time=0.5)
        self.play(ReplacementTransform(cA.sis[0], rA.sis[0]), ReplacementTransform(cpA, rA.sis[1]),
                  ReplacementTransform(ca.sis[0], ra.sis[0]), ReplacementTransform(cpa, ra.sis[1]),
                  FadeIn(rA.join), FadeIn(ra.join), run_time=1.2)

        self.at("sister chromatids")
        b1 = bracket(-1.0 - 0.3, -1.0 + 0.3, CELLC[1] - 1.45, YELLOW)
        l1 = T("sister\nchromatids", 26, YELLOW).next_to(b1, DOWN, buff=0.12)
        self.play(Create(b1), FadeIn(l1), run_time=0.8)

        self.at("centromeres")
        r1, r2 = ring(rA.join), ring(ra.join)
        self.play(FadeOut(b1), FadeOut(l1), Create(r1), Create(r2), run_time=0.7)
        self.play(Indicate(r1, color=YELLOW, scale_factor=1.3), Indicate(r2, color=YELLOW, scale_factor=1.3), run_time=0.8)
        self.at("still one chromosome")
        bA = bracket(-1.0 - 0.3, -1.0 + 0.3, CELLC[1] - 1.45, YELLOW)
        ba = bracket(1.0 - 0.3, 1.0 + 0.3, CELLC[1] - 1.45, YELLOW)
        t1 = T("one\nchromosome", 22, YELLOW).next_to(bA, DOWN, buff=0.12)
        t2 = T("one\nchromosome", 22, YELLOW).next_to(ba, DOWN, buff=0.12)
        self.play(FadeOut(r1), FadeOut(r2), Create(bA), Create(ba), FadeIn(t1), FadeIn(t2), run_time=0.9)
        self.finish()


# ---------------------------------------------------------------------------------------------
class S03One(SpokenScene):
    """S phase done -> prophase I pairing -> metaphase I facing poles -> anaphase I -> two cells."""

    def construct(self):
        cl = cell(CELLC, 3.0)
        cA = Chrom("A", BLUE).place(CELLC + LEFT * 1.0)
        ca = Chrom("a", ORANGE).place(CELLC + RIGHT * 1.0)
        self.add(cl, *cA.mobs(), *ca.mobs())

        self.at("replication")
        chS = bchip("S phase", TEAL, 26)
        chI = bchip("Meiosis I", TEAL, 26)
        chII = bchip("Meiosis II", TEAL, 26)
        row = VGroup(chS, chI, chII).arrange(RIGHT, buff=1.0).move_to([0, 3.2, 0])
        a1 = Arrow(chS.get_right(), chI.get_left(), buff=0.08, color=GREY, stroke_width=4, tip_length=0.2)
        a2 = Arrow(chI.get_right(), chII.get_left(), buff=0.08, color=GREY, stroke_width=4, tip_length=0.2)
        self.play(FadeIn(chS, scale=0.8), Indicate(VGroup(*cA.sis, *ca.sis), color=YELLOW, scale_factor=1.05), run_time=0.8)
        self.at("two divisions")
        self.play(GrowArrow(a1), FadeIn(chI), GrowArrow(a2), FadeIn(chII), run_time=1.0)

        self.at("In prophase", lead=0.1)
        h = heading("Prophase I")
        self.play(FadeOut(VGroup(row, a1, a2)), FadeIn(h), run_time=0.6)
        self.at("pair along")
        d = 0.38
        self.play(*cA.shift(RIGHT * (1.0 - d)), *ca.shift(LEFT * (1.0 - d)), run_time=1.3)
        self.at("bivalent")
        br = bracket(-d - 0.3, d + 0.3, CELLC[1] - 1.45, YELLOW)
        lab = T("bivalent", 30, YELLOW).next_to(br, DOWN, buff=0.12)
        self.play(Create(br), FadeIn(lab), run_time=0.8)

        self.at("At metaphase", lead=0.1)
        h2 = heading("Metaphase I")
        pl, pr = CELLC + LEFT * 2.85, CELLC + RIGHT * 2.85
        P1, P2 = pole(pl), pole(pr)
        f1 = fibre(pl, cA.cc())
        f2 = fibre(pr, ca.cc())
        for f in (f1, f2):
            f.set_z_index(-1)
        self.play(ReplacementTransform(h, h2), FadeOut(br), FadeOut(lab), FadeIn(P1), FadeIn(P2), Create(f1), Create(f2), run_time=1.2)
        self.at("opposite poles")
        self.play(Indicate(P1, color=YELLOW, scale_factor=1.8), Indicate(P2, color=YELLOW, scale_factor=1.8), run_time=0.9)

        self.at("pulls them apart", lead=0.8)
        h3 = heading("Anaphase I")
        dx = 1.7
        self.play(ReplacementTransform(h2, h3),
                  *cA.shift(LEFT * dx), *ca.shift(RIGHT * dx),
                  f1.animate.put_start_and_end_on(pl, cA.cc() + LEFT * dx),
                  f2.animate.put_start_and_end_on(pr, ca.cc() + RIGHT * dx), run_time=1.6)

        self.at("different cells")
        lcell, rcell = cell(CELLC + LEFT * 3.4, 2.55), cell(CELLC + RIGHT * 3.4, 2.55)
        tgt = 3.4 - (d + dx)
        self.play(FadeOut(cl), FadeOut(P1), FadeOut(P2), FadeOut(f1), FadeOut(f2), FadeIn(lcell), FadeIn(rcell),
                  *cA.shift(LEFT * tgt), *ca.shift(RIGHT * tgt), run_time=1.2)
        self.finish()


# ---------------------------------------------------------------------------------------------
class S04Two(SpokenScene):
    """Two haploid cells, still sisters, no S phase, sisters part -> four products -> segregation."""

    def construct(self):
        lcell, rcell = cell(CELLC + LEFT * 3.4, 2.55), cell(CELLC + RIGHT * 3.4, 2.55)
        cA = Chrom("A", BLUE).place(CELLC + LEFT * 3.4)
        ca = Chrom("a", ORANGE).place(CELLC + RIGHT * 3.4)
        self.add(lcell, rcell, *cA.mobs(), *ca.mobs())

        self.at("centromeres again")
        r1, r2 = ring(cA.join), ring(ca.join)
        self.play(Create(r1), Create(r2), run_time=0.6)
        self.play(Indicate(r1, color=YELLOW, scale_factor=1.3), Indicate(r2, color=YELLOW, scale_factor=1.3), run_time=0.7)
        self.at("already haploid")
        hl = T("haploid", 30, GREEN, weight=BOLD).move_to(CELLC + LEFT * 3.4 + DOWN * 2.95)
        hr = T("haploid", 30, GREEN, weight=BOLD).move_to(CELLC + RIGHT * 3.4 + DOWN * 2.95)
        self.play(FadeOut(r1), FadeOut(r2), FadeIn(hl, shift=UP * 0.15), FadeIn(hr, shift=UP * 0.15), run_time=0.7)
        self.at("two sister chromatids")
        self.play(Indicate(VGroup(*cA.sis), color=YELLOW, scale_factor=1.06), Indicate(VGroup(*ca.sis), color=YELLOW, scale_factor=1.06), run_time=0.9)
        self.at("no copying")
        sp = bchip("S phase", GREY, 28).move_to([0, 2.85, 0])
        x = Cross(sp, stroke_color=RED, stroke_width=7)
        self.play(FadeIn(sp, scale=0.8), run_time=0.4)
        self.play(Create(x), run_time=0.5)

        self.at("pulls the sisters")
        h = heading("Meiosis II")
        cells4 = [cell(CELLC + RIGHT * xx, 1.45) for xx in (-4.65, -1.55, 1.55, 4.65)]
        by = -0.5
        pos = [(cA, 0, -4.65), (cA, 1, -1.55), (ca, 0, 1.55), (ca, 1, 4.65)]
        self.play(FadeOut(sp), FadeOut(x), FadeOut(hl), FadeOut(hr), FadeOut(lcell), FadeOut(rcell), FadeOut(cA.join), FadeOut(ca.join),
                  *[FadeIn(c) for c in cells4], FadeIn(h),
                  *[c.sis[i].animate.shift(np.array([xx, by, 0]) - c.sis[i].body.get_center())
                    for (c, i, xx) in pos], run_time=1.6)

        self.at("carry capital")
        tA = T("two carry A", 30, BLUE).move_to([-3.1, -2.55, 0])
        self.play(FadeIn(tA, shift=UP * 0.15), Indicate(VGroup(cA.sis[0], cA.sis[1]), color=BLUE, scale_factor=1.06), run_time=0.8)
        self.at("carry small")
        ta = T("two carry a", 30, ORANGE).move_to([3.1, -2.55, 0])
        self.play(FadeIn(ta, shift=UP * 0.15), Indicate(VGroup(ca.sis[0], ca.sis[1]), color=ORANGE, scale_factor=1.06), run_time=0.8)
        self.at("law of segregation")
        h2 = heading("Law of segregation", YELLOW)
        self.play(ReplacementTransform(h, h2), run_time=0.7)
        self.finish()


# ---------------------------------------------------------------------------------------------
class S05Second(SpokenScene):
    """Two bivalents on the plate; each flips on its own; two orientations -> two kinds of product each."""

    def construct(self):
        cl = cell(CELLC, 3.0)
        pl, pr = CELLC + LEFT * 2.85, CELLC + RIGHT * 2.85
        P1, P2 = pole(pl), pole(pr)
        d = 0.38
        y1, y2 = 0.9, -1.55
        L1, L2 = 1.8, 1.0
        A = Chrom("A", BLUE, L1).place([-d, y1, 0])
        a = Chrom("a", ORANGE, L1).place([d, y1, 0])
        B = Chrom("B", BLUE, L2).place([-d, y2, 0])
        b = Chrom("b", ORANGE, L2).place([d, y2, 0])
        h = heading("Metaphase I")
        self.add(cl, P1, P2, h, *A.mobs(), *a.mobs())

        self.at("second gene")
        self.play(FadeIn(B.group(), scale=0.8), FadeIn(b.group(), scale=0.8), run_time=0.9)
        self.at("different chromosome")
        note = T("different\nchromosome", 28, TEXT).move_to([4.9, y2, 0])
        arr = Arrow(note.get_left() + LEFT * 0.05, [0.95, y2, 0], buff=0.05, color=GREY, stroke_width=4, tip_length=0.2)
        self.play(FadeIn(note), GrowArrow(arr), run_time=0.8)

        self.at("two ways")
        self.play(FadeOut(note), FadeOut(arr), run_time=0.3)
        self.play(Swap(B.group(), b.group()), run_time=1.0)
        self.at("does not affect")
        self.play(Swap(A.group(), a.group()), run_time=1.0)
        # now: left pole side = a, b ; right = A, B

        self.at("one meiosis")
        h2 = heading("Anaphase I")
        dx = 1.7
        self.play(ReplacementTransform(h, h2),
                  *A.shift(RIGHT * dx), *B.shift(RIGHT * dx), *a.shift(LEFT * dx), *b.shift(LEFT * dx), run_time=1.3)
        self.at("capital A capital B")
        cR = bchip("AB × 2", GREEN, 30).move_to([4.85, -0.25, 0])
        tR = T("after\nmeiosis II", 22, GREY).next_to(cR, DOWN, buff=0.12)
        self.play(FadeIn(cR, shift=LEFT * 0.2), FadeIn(tR), run_time=0.6)
        self.at("small a small b")
        cL = bchip("ab × 2", GREEN, 30).move_to([-4.85, -0.25, 0])
        tL = T("after\nmeiosis II", 22, GREY).next_to(cL, DOWN, buff=0.12)
        self.play(FadeIn(cL, shift=RIGHT * 0.2), FadeIn(tL), run_time=0.6)

        self.at("In another", lead=0.4)
        h3 = heading("Metaphase I")
        self.play(ReplacementTransform(h2, h3), FadeOut(cR), FadeOut(cL), FadeOut(tR), FadeOut(tL),
                  *A.shift(LEFT * dx), *B.shift(LEFT * dx), *a.shift(RIGHT * dx), *b.shift(RIGHT * dx), run_time=1.0)
        self.play(Swap(B.group(), b.group()), run_time=0.9)
        # now: right = A, b ; left = a, B
        self.at("they are")
        h4 = heading("Anaphase I")
        self.play(ReplacementTransform(h3, h4),
                  *A.shift(RIGHT * dx), *b.shift(RIGHT * dx), *a.shift(LEFT * dx), *B.shift(LEFT * dx), run_time=0.6)
        self.at("capital A small b")
        cR2 = bchip("Ab × 2", GREEN, 30).move_to([4.85, -0.25, 0])
        tR2 = T("after\nmeiosis II", 22, GREY).next_to(cR2, DOWN, buff=0.12)
        self.play(FadeIn(cR2, shift=LEFT * 0.2), FadeIn(tR2), run_time=0.6)
        self.at("small a capital B")
        cL2 = bchip("aB × 2", GREEN, 30).move_to([-4.85, -0.25, 0])
        tL2 = T("after\nmeiosis II", 22, GREY).next_to(cL2, DOWN, buff=0.12)
        self.play(FadeIn(cL2, shift=RIGHT * 0.2), FadeIn(tL2), run_time=0.6)
        self.at("crossing over")
        nt = T("no crossing over", 28, GREY).move_to([4.7, 2.5, 0])
        self.play(FadeIn(nt), run_time=0.5)
        self.finish()


# ---------------------------------------------------------------------------------------------
class S06Rule(SpokenScene):
    """Four equal bars -> 2x2x2x2 = 16 by doubling -> three panels carry the rule."""

    def construct(self):
        # ---- phase 1: four equal classes
        self.at("Across many")
        h = T("Across many meioses", 34, TEAL, weight=BOLD).move_to([0, 3.15, 0])
        self.play(FadeIn(h), run_time=0.5)
        k1 = bchip("2 AB + 2 ab", GREEN, 32).move_to([-3.2, 0.2, 0])
        orw = T("or", 30, GREY).move_to([0, 0.2, 0])
        k2 = bchip("2 Ab + 2 aB", GREEN, 32).move_to([3.2, 0.2, 0])
        self.wait(0.3)
        self.play(FadeIn(k1, shift=UP * 0.2), run_time=0.6)
        self.play(FadeIn(orw), FadeIn(k2, shift=UP * 0.2), run_time=0.6)
        base_y, H = -1.5, 3.0
        xs = [-4.2, -1.4, 1.4, 4.2]
        names = ["AB", "Ab", "aB", "ab"]
        base = Line([-5.9, base_y, 0], [5.9, base_y, 0], color=GREY, stroke_width=4)
        bars = [Rectangle(width=1.6, height=H, stroke_color=GREEN, stroke_width=3, fill_color=GREEN, fill_opacity=0.4)
                .move_to([x, base_y + H / 2, 0]) for x in xs]
        nm = [T(n, 36, TEXT, weight=BOLD).move_to([x, base_y - 0.5, 0]) for n, x in zip(names, xs)]
        cap = T("share of all gametes", 28, GREY).move_to([0, -2.9, 0])
        self.at("equally likely")
        self.play(FadeOut(k1), FadeOut(orw), FadeOut(k2), Create(base), *[GrowFromEdge(b, DOWN) for b in bars], *[FadeIn(n) for n in nm], FadeIn(cap), run_time=1.4)
        self.at("one quarter")
        qs = [M("1/4", 34, TEXT).move_to([x, base_y + H + 0.45, 0]) for x in xs]
        self.play(*[FadeIn(q, shift=DOWN * 0.15) for q in qs], run_time=0.8)

        # ---- phase 2: 2 x 2 x 2 x 2 = 16
        self.at("fly has")
        clear1 = [h, base, cap, *bars, *nm, *qs]
        grid = [np.array([(i % 4 - 1.5) * 0.85, (1.5 - i // 4) * 0.85 - 0.35, 0]) for i in range(16)]
        dots = [Circle(radius=0.26, stroke_color=GREEN, stroke_width=3, fill_color=GREEN, fill_opacity=0.5).move_to(g) for g in grid]
        steps = ["2", "2 × 2", "2 × 2 × 2", "2 × 2 × 2 × 2", "2 × 2 × 2 × 2 = 16"]
        txts = [M(s, 46, YELLOW).move_to([0, 2.95, 0]) for s in steps]
        for t in txts:
            t.align_to(txts[-1], LEFT)
            t.set_y(2.95)
        txts[-1].move_to([0, 2.95, 0])
        for t in txts[:-1]:
            t.align_to(txts[-1], LEFT)
        reveal = [(0, 2), (2, 4), (4, 8), (8, 16)]
        self.play(*[FadeOut(m) for m in clear1], FadeIn(dots[0], scale=0.5), FadeIn(dots[1], scale=0.5), FadeIn(txts[0]), run_time=0.7)
        cur = txts[0]
        for k in range(1, 4):
            lo, hi = reveal[k]
            self.play(ReplacementTransform(cur, txts[k]), *[FadeIn(dots[i], scale=0.5) for i in range(lo, hi)], run_time=0.55)
            cur = txts[k]
            self.wait(0.15)
        self.at("chromosome combinations", lead=0.7)
        self.play(ReplacementTransform(cur, txts[4]), run_time=0.8)
        self.at("ignoring crossing")
        nt = T("ignoring crossing over", 28, GREY).move_to([0, -3.0, 0])
        self.play(FadeIn(nt), run_time=0.5)

        # ---- phase 3: the rule in three panels
        self.at("Pairs orient", lead=0.9)
        px = [-4.3, 0.0, 4.3]
        heads = ["Metaphase I", "Anaphase I", "Anaphase II"]
        caps = ["pairs orient\non their own", "homologs\npart", "sisters\npart"]
        boxes, chips, capsT = [], [], []
        for x, hd, cp in zip(px, heads, caps):
            boxes.append(RoundedRectangle(corner_radius=0.2, width=3.95, height=6.2, stroke_color=GREY, stroke_width=3).move_to([x, -0.05, 0]))
            chips.append(chip(hd, TEAL, 28).move_to([x, 2.35, 0]))
            capsT.append(T(cp, 28, TEXT).move_to([x, -2.2, 0]))
        gy = 0.1
        L = 1.9
        # panel 1: two bivalents
        A = Chrom("A", BLUE, L).place([px[0] - 1.38, gy, 0])
        a = Chrom("a", ORANGE, L).place([px[0] - 0.62, gy, 0])
        B = Chrom("B", BLUE, L).place([px[0] + 0.62, gy, 0])
        b = Chrom("b", ORANGE, L).place([px[0] + 1.38, gy, 0])
        # panel 2: one bivalent that will part
        A2 = Chrom("A", BLUE, L).place([px[1] - 0.38, gy, 0])
        a2 = Chrom("a", ORANGE, L).place([px[1] + 0.38, gy, 0])
        # panel 3: one chromosome whose sisters will part
        A3 = Chrom("A", BLUE, L).place([px[2], gy, 0])
        glyphs = VGroup(A.group(), a.group(), B.group(), b.group(), A2.group(), a2.group(), A3.group())
        self.play(FadeOut(nt), *[FadeOut(d) for d in dots], FadeOut(txts[4]), run_time=0.4)
        self.play(*[Create(bx) for bx in boxes], *[FadeIn(c) for c in chips], *[FadeIn(c) for c in capsT], FadeIn(glyphs), run_time=0.8)
        self.at("on their own")
        self.play(boxes[0].animate.set_stroke(YELLOW), Swap(B.group(), b.group()), run_time=1.0)
        self.at("separates homologs")
        self.play(boxes[0].animate.set_stroke(GREY), boxes[1].animate.set_stroke(YELLOW),
                  *A2.shift(LEFT * 0.9), *a2.shift(RIGHT * 0.9), run_time=1.0)
        self.at("separates sisters")
        self.play(boxes[1].animate.set_stroke(GREY), boxes[2].animate.set_stroke(YELLOW), FadeOut(A3.join),
                  A3.sis[0].animate.shift(LEFT * 0.75), A3.sis[1].animate.shift(RIGHT * 0.75), run_time=1.0)
        self.finish()


class S07End(EndCard):
    LINE = "Meiosis one separates homologs. Meiosis two separates sisters."
