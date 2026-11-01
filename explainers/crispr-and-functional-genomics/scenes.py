"""A cut is not a knockout  (Genetics and Molecular Biology explainer, crispr-and-functional-genomics)

COLOR MAP (one color per concept, whole video)
  YELLOW = Cas9 and the cut
  BLUE   = the 20-nucleotide guide, and the DNA it matches
  ORANGE = the PAM (N G G)
  TEAL   = a repair route (end joining, homology-directed repair)
  PURPLE = added DNA (an inserted base, the supplied template)
  GREEN  = still working: an unedited or in-frame allele
  RED    = frameshifted allele (and the cells with both alleles frameshifted)
  GREY   = DNA, outlines, neutral cells
"""
import numpy as np
from bp_style import *  # noqa: F401,F403

ORANGE = "#F29E4C"
PURPLE = "#B58CD9"
PINK = "#E86FB0"
TEAL_R = "#3FB8C0"
MINUS = "−"


def bchip(text, color=BLUE, size=26, **kw):
    c = chip(text, color, size=size, **kw)
    back = RoundedRectangle(corner_radius=0.14, width=c[0].width, height=c[0].height, stroke_width=0,
                            fill_color=BG, fill_opacity=1).move_to(c[0])
    return VGroup(back, *c)


def arr(a, b, color=GREY, w=5, tip=0.22):
    return Arrow(a, b, buff=0.08, color=color, stroke_width=w, tip_length=tip,
                 max_tip_length_to_length_ratio=0.45, max_stroke_width_to_length_ratio=12)


def seqrow(letters, colors, pitch, y, size, cx=0.0):
    g = VGroup()
    n = len(letters)
    for i, (ch, col) in enumerate(zip(letters, colors)):
        g.add(M(ch, size, col).move_to([cx + (i - (n - 1) / 2) * pitch, y, 0]))
    return g


def cell_grid(n=10, pitch=0.46, center=(0, 0), r=0.15, color=GREY, op=0.55):
    dots = VGroup()
    for j in range(n):
        for i in range(n):
            x = center[0] + (i - (n - 1) / 2) * pitch
            y = center[1] - (j - (n - 1) / 2) * pitch
            dots.add(Circle(radius=r, stroke_color=color, stroke_width=2, fill_color=color, fill_opacity=op).move_to([x, y, 0]))
    return dots


def is_both(i, j):
    """grid cell (column i, row j) has both alleles frameshifted: first 7 columns and first 7 rows."""
    return i < 7 and j < 7


class S00Title(TitleCard):
    LESSON = "Forward and reverse genetics"
    TITLE = "A cut is not a knockout"


# ---------------------------------------------------------------------------------------------
class S01Dish(SpokenScene):
    def construct(self):
        dish = RoundedRectangle(corner_radius=0.5, width=5.4, height=5.4, stroke_color=GREY, stroke_width=3,
                                fill_color=GREY, fill_opacity=0.08).move_to([0, -0.5, 0])
        dots = cell_grid(10, 0.5, (0, -0.5), r=0.17, color=GREY)
        self.at("cut both copies")
        self.play(Create(dish), LaggedStart(*[FadeIn(d, scale=0.5) for d in dots], lag_ratio=0.01), run_time=1.6)
        self.play(*[d.animate.set_color(YELLOW).set_fill(YELLOW, 0.8) for d in dots], run_time=0.5)
        self.play(*[d.animate.set_color(GREY).set_fill(GREY, 0.55) for d in dots], run_time=0.5)
        q = T("Why is half the dish still making the protein?", 32).to_edge(UP, buff=0.35)
        self.at("half the dish")
        self.play(FadeIn(q, shift=DOWN * 0.15), run_time=0.7)
        qm = T("?", 120, YELLOW, weight=BOLD).move_to([0, -0.5, 0])
        self.play(*[d.animate.set_opacity(0.25) for d in dots], FadeIn(qm, scale=0.6), run_time=0.6)
        self.at("one cell")
        pick = dots[44]
        self.play(FadeOut(qm), *[d.animate.set_opacity(0) for d in dots if d is not pick], FadeOut(dish),
                  FadeOut(q), pick.animate.set_opacity(1).set_color(YELLOW), run_time=0.7)
        big = Circle(radius=2.1, stroke_color=GREY, stroke_width=4, fill_color=GREY, fill_opacity=0.14).move_to([0.2, -0.1, 0])
        self.play(ReplacementTransform(pick, big), run_time=0.8)
        bars = VGroup(*[RoundedRectangle(corner_radius=0.1, width=2.9, height=0.42, stroke_color=GREEN, stroke_width=3,
                                         fill_color=GREEN, fill_opacity=0.5) for _ in range(2)])
        bars[0].move_to([0, 0.6, 0]); bars[1].move_to([0, -0.8, 0])
        l1 = T("copy 1 of the gene", 28, GREEN).next_to(big, LEFT, buff=0.35)
        l2 = T("copy 2 of the gene", 28, GREEN).next_to(big, LEFT, buff=0.35)
        l1.set_y(0.6); l2.set_y(-0.8); l2.set_x(l1.get_center()[0])
        self.at("two copies")
        bars.shift(RIGHT*0.2)
        self.play(FadeIn(bars, scale=0.8), FadeIn(l1), FadeIn(l2), run_time=0.8)
        cas = bchip("Cas9", YELLOW, 36)
        cas.move_to([4.6, -0.1, 0])
        self.at("aim")
        self.play(FadeIn(cas, shift=LEFT * 0.2), run_time=0.6)
        a1 = arr(cas.get_left() + UP * 0.1, [1.55, 0.6, 0], YELLOW)
        a2 = arr(cas.get_left() + DOWN * 0.1, [1.55, -0.8, 0], YELLOW)
        self.play(GrowArrow(a1), GrowArrow(a2), run_time=0.6)
        self.at("The cut is the easy part")
        cuts = VGroup(*[VGroup(Line([0.2, y + 0.45, 0], [0.2, y - 0.45, 0], color=YELLOW, stroke_width=7)) for y in (0.6, -0.8)])
        self.play(FadeIn(cuts, scale=1.6), run_time=0.5)
        self.at("real question")
        q2 = T("what does the cell do next?", 34, TEXT).to_edge(DOWN, buff=0.4)
        self.play(FadeIn(q2, shift=UP * 0.15), run_time=0.6)
        self.finish()


# ---------------------------------------------------------------------------------------------
class S02Aim(SpokenScene):
    GUIDE = "CTGAGCATCGGTAACTGCTA"

    def construct(self):
        seq = "AC" + self.GUIDE + "TGG" + "CA"
        pitch = 0.455
        y = 0.3
        cols = [GREY] * 2 + [BLUE] * 20 + [ORANGE] * 3 + [GREY] * 2
        strand = seqrow(seq, cols, pitch, y, 34)

        def px(i):
            return (i - 13) * pitch  # x of letter i (27 letters, centre = index 13)

        cas = VGroup(Ellipse(width=3.6, height=1.2, stroke_color=YELLOW, stroke_width=4, fill_color=YELLOW, fill_opacity=0.2),
                     T("Cas9", 34, YELLOW, weight=BOLD)).move_to([0, 2.9, 0])
        self.play(FadeIn(cas, shift=DOWN * 0.2), run_time=0.7)
        # guide: a blue bar hanging from Cas9 over the 20 matching letters
        gx0, gx1 = px(2) - 0.2, px(21) + 0.2
        gbar = RoundedRectangle(corner_radius=0.12, width=gx1 - gx0, height=0.36, stroke_color=BLUE, stroke_width=3,
                                fill_color=BLUE, fill_opacity=0.35).move_to([(gx0 + gx1) / 2, 1.5, 0])
        stem = Line([(gx0 + gx1) / 2, 2.3, 0], [(gx0 + gx1) / 2, 1.68, 0], color=BLUE, stroke_width=4)
        glabel = T("guide", 28, BLUE).next_to(gbar, UP, buff=0.12).shift(RIGHT * 3.6)
        self.at("aimed by a guide")
        self.play(FadeIn(stem), GrowFromCenter(gbar), FadeIn(glabel), run_time=0.8)
        self.play(FadeIn(strand, lag_ratio=0.04), run_time=1.0)
        # twenty nucleotides
        ticks = VGroup(*[Line([px(i), 1.3, 0], [px(i), 0.82, 0], color=BLUE, stroke_width=2) for i in range(2, 22)])
        n20 = T("20 nucleotides", 32, BLUE).move_to([px(11.5), -0.7, 0])
        self.at("nucleotides long")
        self.play(LaggedStart(*[Create(t) for t in ticks], lag_ratio=0.05), FadeIn(n20, shift=UP * 0.1), run_time=1.6)
        # PAM
        pam_box = RoundedRectangle(corner_radius=0.1, width=3 * pitch + 0.16, height=0.7, stroke_color=ORANGE, stroke_width=3,
                                   fill_opacity=0).move_to([px(23), y, 0])
        pam_lbl = T("PAM", 30, ORANGE, weight=BOLD).next_to(pam_box, DOWN, buff=0.18)
        pam_lbl2 = T("N G G", 28, ORANGE).next_to(pam_lbl, DOWN, buff=0.2)
        self.at("short motif")
        self.play(Create(pam_box), FadeIn(pam_lbl), run_time=0.7)
        self.at("reads")
        self.play(FadeIn(pam_lbl2), run_time=0.5)
        # no PAM: swap the three letters, cross out
        self.at("ignored DNA")
        wrong = seqrow("ACT", [GREY] * 3, pitch, y, 34, cx=px(23))
        self.play(*[ReplacementTransform(strand[22 + k], wrong[k]) for k in range(3)],
                  pam_box.animate.set_stroke(RED), pam_lbl.animate.set_color(RED),
                  FadeOut(pam_lbl2), run_time=0.6)
        x1 = Line(pam_box.get_corner(UL) + DR * 0.05, pam_box.get_corner(DR) + UL * 0.05, color=RED, stroke_width=6)
        x2 = Line(pam_box.get_corner(UR) + DL * 0.05, pam_box.get_corner(DL) + UR * 0.05, color=RED, stroke_width=6)
        note = T("matches the guide, no PAM: ignored", 32, RED).move_to([0, -2.4, 0])
        self.play(Create(x1), Create(x2), cas[0].animate.set_stroke(opacity=0.35).set_fill(opacity=0.07), cas[1].animate.set_opacity(0.35), FadeIn(note), run_time=0.6)
        # restore the PAM, then the cut
        right = seqrow("TGG", [ORANGE] * 3, pitch, y, 34, cx=px(23))
        self.at("In the original test")
        self.play(FadeOut(x1), FadeOut(x2), FadeOut(note), cas[0].animate.set_stroke(opacity=1).set_fill(opacity=0.2), cas[1].animate.set_opacity(1),
                  *[ReplacementTransform(wrong[k], right[k]) for k in range(3)],
                  pam_box.animate.set_stroke(ORANGE), pam_lbl.animate.set_color(ORANGE), run_time=0.7)
        cx = (px(18) + px(19)) / 2
        cut = Line([cx, 1.0, 0], [cx, -0.3, 0], color=YELLOW, stroke_width=7)
        br = VMobject(color=YELLOW, stroke_width=4).set_points_as_corners(
            [[px(19) - 0.2, -0.5, 0], [px(19) - 0.2, -0.67, 0], [px(21) + 0.2, -0.67, 0], [px(21) + 0.2, -0.5, 0]])
        # keep the "20 nucleotides" label clear: move it up beside the guide
        self.play(FadeOut(n20), run_time=0.3)
        three = T("cut: 3 base pairs from the PAM (original test)", 30, YELLOW).move_to([px(20) - 1.6, -1.25, 0])
        self.at("three base pairs")
        self.play(Create(cut), Create(br), FadeIn(three), run_time=0.8)
        self.at("upstream")
        self.finish()


# ---------------------------------------------------------------------------------------------
ROWS = [  # label, kind, delta, percent
    ("unedited", "wt", 0, 10),
    (MINUS + "1 bp", "del", 1, 35),
    ("+1 bp", "ins", 1, 25),
    (MINUS + "3 bp", "del", 3, 15),
    (MINUS + "6 bp", "del", 6, 5),
    (MINUS + "7 bp", "del", 7, 10),
]
SQ, SP, NSQ = 0.27, 0.31, 14


def allele_row(kind, d, x0, y):
    """a strand of 14 squares: deleted ones are empty outlines, an insertion is one purple square."""
    g = VGroup()
    for i in range(NSQ):
        gone = kind == "del" and i >= NSQ - d - 3 and i < NSQ - 3
        sq = Square(side_length=SQ, stroke_color=GREY, stroke_width=2,
                    fill_color=GREY, fill_opacity=0 if gone else 0.5).move_to([x0 + i * SP, y, 0])
        if gone:
            sq.set_stroke(opacity=0.35)
        g.add(sq)
    if kind == "ins":
        sq = Square(side_length=SQ, stroke_color=PURPLE, stroke_width=3, fill_color=PURPLE, fill_opacity=0.9)
        sq.move_to([x0 + (NSQ - 3) * SP - SP / 2 + 0.0, y + 0.0, 0]).shift(UP * 0)
        # make room: shift the right-hand squares by half a pitch outward
        for i in range(NSQ - 3, NSQ):
            g[i].shift(RIGHT * SP)
        sq.move_to([x0 + (NSQ - 3) * SP, y, 0])
        g.add(sq)
    return g


ROW_Y = [2.2, 1.3, 0.4, -0.5, -1.4, -2.3]
ROW_X0 = -3.6


def rows_group():
    labs, strands = VGroup(), VGroup()
    for (lab, kind, d, pct), y in zip(ROWS, ROW_Y):
        t = T(lab, 26, TEXT)
        t.move_to([ROW_X0 - 0.5 - t.width / 2 - 0.1, y, 0])
        labs.add(t)
        strands.add(allele_row(kind, d, ROW_X0, y))
    return labs, strands


class S03Repair(SpokenScene):
    def construct(self):
        L, R = "ACGTTGCA", "CGGATCAT"
        pitch = 0.64
        y = 1.7
        left = seqrow(L, [GREY] * 8, pitch, y, 46, cx=-3.2)
        right = seqrow(R, [GREY] * 8, pitch, y, 46, cx=3.2)
        flash = Line([0, y + 0.65, 0], [0, y - 0.65, 0], color=YELLOW, stroke_width=7)
        self.play(FadeIn(left), FadeIn(right), Create(flash), run_time=0.9)
        self.at("repairs")
        brk = T("a double-strand break", 32, YELLOW).move_to([0, 0.6, 0])
        self.play(FadeIn(brk, shift=UP * 0.1), run_time=0.5)
        # end joining
        ej = bchip("end joining", TEAL_R, 34).move_to([-3.4, -1.0, 0])
        self.at("end joining")
        self.play(FadeIn(ej, scale=0.9), FadeOut(brk), run_time=0.6)
        nt = T("needs no template", 30, GREY).next_to(ej, DOWN, buff=0.3)
        self.at("needs no template")
        self.play(FadeIn(nt), run_time=0.5)
        # insertion version, then deletion version
        ins = seqrow(L + "T" + R, [GREY] * 8 + [PURPLE] + [GREY] * 8, pitch, y, 46)
        dele = seqrow(L[:-1] + R, [GREY] * 15, pitch, y, 46)
        tag1 = T("insertion", 32, PURPLE).move_to([0, 0.6, 0])
        tag2 = T("deletion", 32, RED).move_to([0, 0.6, 0])
        self.at("insertions")
        self.play(ReplacementTransform(VGroup(left, right, flash), ins), FadeIn(tag1), run_time=0.8)
        self.at("deletions")
        self.play(ReplacementTransform(ins, dele), ReplacementTransform(tag1, tag2), run_time=0.8)
        # homology directed repair
        hdr = bchip("homology-directed repair", TEAL_R, 34).move_to([3.4, -1.0, 0])
        self.at("homology directed")
        self.play(FadeIn(hdr, scale=0.9), run_time=0.6)
        tpl = VGroup(RoundedRectangle(corner_radius=0.1, width=4.2, height=0.8, stroke_color=PURPLE, stroke_width=3,
                                      fill_color=PURPLE, fill_opacity=0.25),
                     T("template you supply", 30, PURPLE))
        tpl[1].move_to(tpl[0])
        tpl.next_to(hdr, DOWN, buff=0.3)
        self.at("template that you supply")
        self.play(FadeIn(tpl, shift=UP * 0.1), run_time=0.6)
        # the pool
        labs, strands = rows_group()
        self.at("sequencing the pool")
        self.play(FadeOut(VGroup(dele, tag2, ej, nt, hdr, tpl)), run_time=0.5)
        self.play(LaggedStart(*[AnimationGroup(FadeIn(a), FadeIn(b)) for a, b in zip(labs, strands)], lag_ratio=0.12),
                  run_time=1.8)
        self.finish()


# ---------------------------------------------------------------------------------------------
class S04Frame(SpokenScene):
    CUES = ["unedited", "lose one", "gain one", "lose three", "lose six", "lose seven"]

    def construct(self):
        labs, strands = rows_group()
        self.add(labs, strands)
        scale = 0.1
        bx0 = 1.4
        frame_rows = [i for i, r in enumerate(ROWS) if r[1] in ("del", "ins") and r[2] % 3 != 0]
        bars, pcts = [], []
        for i, ((lab, kind, d, pct), y) in enumerate(zip(ROWS, ROW_Y)):
            col = GREY
            b = Rectangle(width=pct * scale, height=0.5, stroke_color=col, stroke_width=2, fill_color=col, fill_opacity=0.7)
            b.move_to([bx0 + pct * scale / 2, y, 0])
            p = M(f"{pct}%", 28, TEXT).next_to(b, RIGHT, buff=0.15)
            bars.append(b); pcts.append(p)
        head = T("share of alleles in the pool", 28, GREY).move_to([bx0 + 1.9, 3.0, 0])
        self.at("count the alleles")
        self.play(FadeIn(head), run_time=0.5)
        for i, cue in enumerate(self.CUES):
            self.at(cue)
            self.play(GrowFromEdge(bars[i], LEFT), FadeIn(pcts[i]), run_time=0.5)
        self.at("multiple of three")
        note = T("a length that is not a multiple of 3 shifts the frame", 28, TEXT).move_to([0.5, -3.2, 0])
        self.play(FadeIn(note, shift=UP * 0.1), run_time=0.6)
        self.at("Lose one", nth=1)
        self.play(Indicate(VGroup(bars[1], pcts[1], labs[1]), color=RED, scale_factor=1.05), run_time=0.6)
        self.at("gain one", nth=1)
        self.play(Indicate(VGroup(bars[2], pcts[2], labs[2]), color=RED, scale_factor=1.05), run_time=0.6)
        self.at("lose seven", nth=1)
        self.play(Indicate(VGroup(bars[5], pcts[5], labs[5]), color=RED, scale_factor=1.05), run_time=0.6)
        self.at("all shifted")
        rec = []
        for i in range(6):
            col = RED if i in frame_rows else GREEN
            rec += [bars[i].animate.set_color(col).set_fill(col, 0.7), pcts[i].animate.set_color(col)]
        self.play(*rec, run_time=0.9)
        self.at("Add them up")
        br = VMobject(color=RED, stroke_width=5).set_points_as_corners(
            [[6.35, ROW_Y[1] + 0.3, 0], [6.6, ROW_Y[1] + 0.3, 0], [6.6, ROW_Y[2] - 0.3, 0], [6.35, ROW_Y[2] - 0.3, 0]])
        br2 = VMobject(color=RED, stroke_width=5).set_points_as_corners(
            [[6.35, ROW_Y[5] + 0.3, 0], [6.6, ROW_Y[5] + 0.3, 0], [6.6, ROW_Y[5] - 0.3, 0], [6.35, ROW_Y[5] - 0.3, 0]])
        tot = bchip("35 + 25 + 10 = 70% frameshifted", RED, 32).move_to([0.5, -3.1, 0])
        self.play(FadeOut(note), run_time=0.3)
        self.play(FadeIn(tot, shift=UP * 0.1), run_time=0.7)
        self.finish()


# ---------------------------------------------------------------------------------------------
class S05Both(SpokenScene):
    def construct(self):
        n, pitch = 10, 0.56
        cx, cy = -3.2, -0.45
        dots = cell_grid(n, pitch, (cx, cy), r=0.19, color=GREY)
        left = cx - n * pitch / 2
        top = cy + n * pitch / 2
        self.play(LaggedStart(*[FadeIn(d, scale=0.5) for d in dots], lag_ratio=0.005), run_time=1.0)
        # allele bands
        w7 = 7 * pitch
        vband = Rectangle(width=w7, height=n * pitch, stroke_color=RED, stroke_width=2, fill_color=RED, fill_opacity=0.22
                          ).move_to([left + w7 / 2, cy, 0])
        hband = Rectangle(width=n * pitch, height=w7, stroke_color=RED, stroke_width=2, fill_color=RED, fill_opacity=0.22
                          ).move_to([cx, top - w7 / 2, 0])
        lab1 = T("allele 1: 0.7 frameshifted", 26, RED).move_to([left + w7 / 2, top + 0.4, 0])
        lab2 = T("allele 2: 0.7", 26, RED).rotate(PI / 2).move_to([left - 0.45, top - w7 / 2, 0])
        g1 = T("allele 1", 26, GREY).move_to([cx, top + 0.4, 0])
        g2 = T("allele 2", 26, GREY).rotate(PI / 2).move_to([left - 0.45, cy, 0])
        self.at("two alleles")
        self.play(FadeIn(g1, shift=DOWN * 0.1), FadeIn(g2, shift=RIGHT * 0.1), run_time=0.6)
        self.at("chance that one allele")
        self.play(FadeIn(vband), ReplacementTransform(g1, lab1), run_time=0.8)
        self.at("For both")
        self.play(FadeIn(hband), ReplacementTransform(g2, lab2), run_time=0.8)
        eq = M("0.7 x 0.7 = 0.49", 40, RED).move_to([3.4, 1.4, 0])
        eq_a = M("0.7 x 0.7", 40, RED).move_to(eq.get_left() + RIGHT * 1.65)
        self.at("multiply")
        self.play(FadeIn(eq_a, shift=UP * 0.1), run_time=0.6)
        self.at("is 0 49")
        self.play(ReplacementTransform(eq_a, eq), run_time=0.5)
        self.at("have both alleles")
        anims = []
        for k, d in enumerate(dots):
            i, j = k % n, k // n
            if is_both(i, j):
                anims.append(d.animate.set_color(RED).set_fill(RED, 0.95))
        self.play(*anims, run_time=0.8)
        t1 = T("both alleles frameshifted", 28, RED).move_to([3.4, 0.4, 0])
        self.play(FadeIn(t1), run_time=0.5)
        self.at("About half the cells")
        anims = []
        for k, d in enumerate(dots):
            i, j = k % n, k // n
            if not is_both(i, j):
                anims.append(d.animate.set_color(GREEN).set_fill(GREEN, 0.9))
        self.play(*anims, FadeOut(vband), FadeOut(hband), run_time=0.8)
        t2 = VGroup(T("still carry at least one", 28, GREEN), T("in-frame or unedited allele", 28, GREEN)).arrange(DOWN, buff=0.12).move_to([3.4, -1.0, 0])
        self.play(FadeIn(t2, shift=UP * 0.1), run_time=0.6)
        self.finish()


# ---------------------------------------------------------------------------------------------
class S06Rule(SpokenScene):
    def construct(self):
        c1 = bchip("cut", YELLOW, 36)
        c2 = bchip("mutated allele", PURPLE, 36)
        c3 = bchip("knockout", PINK, 36)
        row = VGroup(c1, c2, c3).arrange(RIGHT, buff=1.1).move_to([0, 2.9, 0])
        a1 = arr(c1.get_right(), c2.get_left(), GREY)
        a2 = arr(c2.get_right(), c3.get_left(), GREY)
        self.at("a cut")
        self.play(FadeIn(c1, shift=UP * 0.1), run_time=0.4)
        self.at("mutated allele")
        self.play(GrowArrow(a1), FadeIn(c2), run_time=0.5)
        self.at("knockout")
        self.play(GrowArrow(a2), FadeIn(c3), run_time=0.5)
        self.at("Only the third")
        gr = T("the only loss of function", 30, TEXT).next_to(c3, DOWN, buff=0.25)
        ul = Rectangle(width=c3.width + 0.3, height=c3.height + 0.3, stroke_color=GOLD, stroke_width=4).move_to(c3)
        self.play(Create(ul), FadeIn(gr), run_time=0.7)
        # the mosaic
        n, pitch = 10, 0.44
        grid = cell_grid(n, pitch, (-3.7, -0.65), r=0.16, color=GREY)
        for k, d in enumerate(grid):
            i, j = k % n, k // n
            col = RED if is_both(i, j) else GREEN
            d.set_color(col).set_fill(col, 0.9)
        self.at("mosaic")
        self.play(LaggedStart(*[FadeIn(d, scale=0.5) for d in grid], lag_ratio=0.005), run_time=0.9)
        mo = T("a mosaic, not a null", 32, TEXT).move_to([-3.7, -3.3, 0])
        self.play(FadeIn(mo, shift=UP * 0.1), run_time=0.5)
        r1 = bchip("derive clones, genotype them", TEXT, 32).move_to([3.0, -0.2, 0])
        r2 = bchip("and check function is gone", TEXT, 32).move_to([3.0, -1.7, 0])
        self.at("Derive clones")
        self.play(FadeIn(r1, shift=LEFT * 0.2), run_time=0.6)
        self.at("function is gone")
        self.play(FadeIn(r2, shift=LEFT * 0.2), run_time=0.6)
        self.finish()


class S07End(EndCard):
    LINE = "Cut, mutation, knockout: three states. Only the knockout is a loss of function."
