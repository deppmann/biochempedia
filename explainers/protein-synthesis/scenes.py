"""From DNA to protein: how one letter changes a protein  (Biochemistrypedia high school Biology explainer)

COLOR MAP (one color per concept, whole video)
  BLUE   = DNA (letters, strands)
  ORANGE = RNA (messenger RNA letters)
  GREEN  = amino acids and the amino acid chain
  YELLOW = the one changed letter / the changed amino acid (GAG -> GTG, Glu -> Val)
  RED    = stop codon
  PINK   = red blood cell
  TEAL   = the copying enzyme
  PURPLE = transfer RNA (tRNA)
  GREY   = membranes, outlines, ribosome, labels
"""
import numpy as np
from bp_style import *  # noqa: F401,F403

ORANGE = "#F29E4C"
PINK = "#F48FB1"
PURPLE = "#B58CD9"
BLOCK = 0.62


def blk(ch, color, w=BLOCK, size=26):
    """one lettered block."""
    r = RoundedRectangle(corner_radius=0.08, width=w, height=w, stroke_color=color, stroke_width=3,
                         fill_color=color, fill_opacity=0.2)
    return VGroup(r, M(ch, size, color).move_to(r))


def row(letters, color, w=BLOCK, size=26, gap=0.0):
    g = VGroup(*[blk(c, color, w, size) for c in letters]).arrange(RIGHT, buff=gap)
    return g


def box_around(mob, color=TEXT, pad=0.1, sw=3):
    return SurroundingRectangle(mob, color=color, buff=pad, stroke_width=sw, corner_radius=0.12)


def arr(a, b, color=GREY, w=5, tip=0.2):
    return Arrow(a, b, buff=0.06, color=color, stroke_width=w, tip_length=tip,
                 max_tip_length_to_length_ratio=0.45, max_stroke_width_to_length_ratio=12)


def sickle(color=PINK, scale=1.0):
    a = Arc(radius=0.9, start_angle=PI * 0.15, angle=PI * 1.15, stroke_color=color, stroke_width=22)
    a.set_cap_style(CapStyleType.ROUND)
    return a.scale(scale)


def disc(color=PINK, scale=1.0):
    c = Circle(radius=0.85, stroke_color=color, stroke_width=6, fill_color=color, fill_opacity=0.25)
    return c.scale(scale)


class S00Title(TitleCard):
    LESSON = "From DNA to Protein"
    TITLE = "How One Letter Changes a Protein"


# ---------------------------------------------------------------------------------------------
class S01Gene(SpokenScene):
    """hemoglobin gene spot GAG -> GTG; round cell -> sickle cell; the question."""

    def construct(self):
        bar = RoundedRectangle(corner_radius=0.12, width=11.0, height=0.5, stroke_color=BLUE, stroke_width=3,
                               fill_color=BLUE, fill_opacity=0.2).move_to([0, 2.9, 0])
        bar_lbl = T("hemoglobin gene (DNA)", 26, BLUE).next_to(bar, UP, buff=0.12)
        self.at("one spot")
        self.play(FadeIn(bar), FadeIn(bar_lbl), run_time=0.7)
        spot = Rectangle(width=0.4, height=0.5, stroke_color=YELLOW, stroke_width=4, fill_opacity=0).move_to([0, 2.9, 0])
        blocks = row("GAG", BLUE, w=0.95, size=40).move_to([0, 1.3, 0])
        guide = VGroup(Line(spot.get_bottom() + LEFT * 0.2, blocks.get_corner(UL) + UP * 0.05, color=GREY, stroke_width=2),
                       Line(spot.get_bottom() + RIGHT * 0.2, blocks.get_corner(UR) + UP * 0.05, color=GREY, stroke_width=2))
        self.play(Create(spot), run_time=0.4)
        self.play(Create(guide), FadeIn(blocks, shift=DOWN * 0.15), run_time=0.6)
        who = T("most people", 28, TEXT).next_to(blocks, DOWN, buff=0.25)
        self.at("In most people")
        self.play(FadeIn(who), run_time=0.4)
        gtg = row("GTG", BLUE, w=0.95, size=40).move_to(blocks)
        gtg[1].set_color(YELLOW)
        gtg[1][0].set_stroke(YELLOW).set_fill(YELLOW, 0.3)
        who2 = T("some people", 28, YELLOW).next_to(blocks, DOWN, buff=0.25)
        self.at("In some people")
        self.play(ReplacementTransform(blocks[1], gtg[1]), ReplacementTransform(who, who2), run_time=0.7)
        self.play(Indicate(gtg[1], color=YELLOW, scale_factor=1.25), run_time=0.6)

        cell = disc().move_to([-3.2, -0.9, 0])
        cell_lbl = T("red blood cell: soft, round", 26, PINK).next_to(cell, DOWN, buff=0.3)
        self.at("soft round red blood cell")
        self.play(FadeIn(cell, scale=0.9), FadeIn(cell_lbl), run_time=0.6)
        sk = sickle().move_to([3.2, -0.9, 0])
        sk_lbl = T("sickle cell: stiff, curved", 26, PINK).next_to(sk, DOWN, buff=0.3)
        ar = arr([-1.8, -0.9, 0], [1.9, -0.9, 0], YELLOW)
        self.at("stiff curved sickle shape")
        self.play(GrowArrow(ar), run_time=0.4)
        self.play(FadeIn(sk, scale=0.9), FadeIn(sk_lbl), run_time=0.6)
        self.at("How can one letter change a whole cell")
        q = T("How can one letter change a whole cell?", 36, font=TITLE_FONT).move_to([0, -3.15, 0])
        self.play(FadeIn(q, shift=UP * 0.15), run_time=0.6)
        self.at("The answer starts")
        self.play(*[FadeOut(m) for m in [bar, bar_lbl, spot, guide, blocks[0], blocks[2], gtg[1], who2, cell, cell_lbl, sk, sk_lbl, ar]],
                  q.animate.move_to([0, 0, 0]), run_time=0.8)
        self.wait(0.6)
        self.play(FadeOut(q), run_time=0.4)
        self.finish()


# ---------------------------------------------------------------------------------------------
class S02Copy(SpokenScene):
    """DNA stays in the nucleus; an enzyme copies one gene into messenger RNA."""

    def construct(self):
        cell = RoundedRectangle(corner_radius=0.5, width=12.2, height=5.2, stroke_color=GREY, stroke_width=3).move_to([0, -0.5, 0])
        nuc = Ellipse(width=6.4, height=4.4, stroke_color=GREY, stroke_width=4, fill_color=GREY, fill_opacity=0.12).move_to([-2.6, -0.5, 0])
        nuc_lbl = T("nucleus", 28, GREY).move_to([-2.6, -2.35, 0])
        d1 = Rectangle(width=4.6, height=0.18, stroke_width=0, fill_color=BLUE, fill_opacity=0.9).move_to([-2.6, 0.4, 0])
        d2 = Rectangle(width=4.6, height=0.18, stroke_width=0, fill_color=BLUE, fill_opacity=0.9).move_to([-2.6, -0.1, 0])
        rungs = VGroup(*[Line([x, 0.4, 0], [x, -0.1, 0], color=BLUE, stroke_width=3) for x in np.arange(-4.7, -0.4, 0.4)])
        dna = VGroup(d1, d2, rungs)
        dna_lbl = T("DNA", 28, BLUE).next_to(dna, DOWN, buff=0.2)
        self.play(FadeIn(cell), FadeIn(nuc), FadeIn(nuc_lbl), run_time=0.6)
        self.play(FadeIn(dna), FadeIn(dna_lbl), run_time=0.6)
        out = T("proteins are built\noutside the nucleus", 28, GREY, line_spacing=0.9).move_to([3.6, 0.6, 0])
        out2 = T("(in the cytoplasm)", 24, GREY).next_to(out, DOWN, buff=0.15)
        self.at("proteins are built outside")
        self.play(FadeIn(out), FadeIn(out2), run_time=0.7)

        gene = Rectangle(width=1.5, height=0.7, stroke_color=BLUE, stroke_width=4, fill_opacity=0).move_to([-2.6, 0.15, 0])
        copy_lbl = T("a copy", 28, ORANGE)
        self.at("So the cell first makes a copy")
        rna = Rectangle(width=1.5, height=0.2, stroke_width=0, fill_color=ORANGE, fill_opacity=1).move_to([-2.6, -1.0, 0])
        copy_lbl.next_to(rna, DOWN, buff=0.2)
        self.play(Create(gene), run_time=0.4)
        self.play(FadeIn(rna, shift=DOWN * 0.3), FadeIn(copy_lbl), run_time=0.7)

        head = T("transcription", 36, font=TITLE_FONT, color=TEAL).move_to([0, 3.1, 0])
        self.at("Transcription is the first stage")
        self.play(FadeIn(head, shift=DOWN * 0.1), run_time=0.5)
        enz = chip("enzyme", TEAL, 26).move_to([-2.6, 1.0, 0])
        self.at("An enzyme copies one gene")
        self.play(FadeIn(enz, shift=DOWN * 0.2), Indicate(gene, color=TEAL), run_time=0.7)
        rna_lbl = T("RNA", 28, ORANGE).next_to(rna, DOWN, buff=0.2)
        self.at("into a strand of")
        self.play(ReplacementTransform(copy_lbl, rna_lbl), run_time=0.5)
        self.at("This copy is called")
        m_lbl = T("messenger RNA (mRNA)", 28, ORANGE).move_to(rna_lbl)
        self.play(ReplacementTransform(rna_lbl, m_lbl), Indicate(rna, color=ORANGE), run_time=0.7)
        self.finish()


# ---------------------------------------------------------------------------------------------
PAIRS = [("A", "U"), ("T", "A"), ("C", "G"), ("G", "C")]


class S03Pair(SpokenScene):
    """the template strand is paired letter by letter into mRNA; mRNA leaves through a pore."""

    def construct(self):
        mem = VGroup(
            Rectangle(width=0.3, height=1.9, stroke_color=GREY, stroke_width=3, fill_color=GREY, fill_opacity=0.35).move_to([1.7, 2.2, 0]),
            Rectangle(width=0.3, height=3.3, stroke_color=GREY, stroke_width=3, fill_color=GREY, fill_opacity=0.35).move_to([1.7, -1.9, 0]))
        # gap between y=1.25 and y=-0.0 : pore
        mem[1].move_to([1.7, -1.75, 0])   # spans -3.4..-0.1
        mem[0].move_to([1.7, 2.35, 0])   # spans 1.4..3.3
        nuc_lbl = T("nucleus", 28, GREY).move_to([0.4, 3.1, 0])
        cyt_lbl = T("cytoplasm", 28, GREY).move_to([4.8, 3.1, 0])
        dna = row("TACCTC", BLUE).move_to([-3.0, 2.0, 0])
        dna_lbl = T("DNA template strand", 26, BLUE).next_to(dna, UP, buff=0.12)
        dna_lbl.move_to([-3.0, 2.85, 0])
        self.at("The enzyme reads one")
        self.play(FadeIn(mem), FadeIn(nuc_lbl), FadeIn(cyt_lbl), run_time=0.5)
        self.play(FadeIn(dna), FadeIn(dna_lbl), run_time=0.5)
        rna = row("AUGGAG", ORANGE).move_to([-3.0, 0.7, 0])
        rna_lbl = T("messenger RNA", 26, ORANGE).move_to([-3.0, -0.15, 0])
        links = VGroup(*[Line(dna[i].get_bottom(), rna[i].get_top(), color=GREY, stroke_width=3) for i in range(6)])
        self.at("pairs a new")
        self.play(LaggedStart(*[AnimationGroup(Create(links[i]), FadeIn(rna[i], shift=UP * 0.15)) for i in range(6)],
                              lag_ratio=0.35), FadeIn(rna_lbl), run_time=2.0)

        title = T("DNA letter  →  RNA letter", 26, GREY).move_to([-3.0, -1.2, 0])
        self.play(FadeIn(title), run_time=0.3)
        chips = VGroup()
        for i, (a, b) in enumerate(PAIRS):
            c = VGroup(blk(a, BLUE, 0.6, 26), T("→", 28, GREY), blk(b, ORANGE, 0.6, 26)).arrange(RIGHT, buff=0.18)
            chips.add(c)
        chips.arrange_in_grid(rows=2, cols=2, buff=(0.7, 0.3)).move_to([-3.0, -2.55, 0])
        self.at("letter A pairs with U")
        self.play(FadeIn(chips[0]), run_time=0.4)
        self.at("T pairs with A")
        self.play(FadeIn(chips[1]), run_time=0.4)
        self.at("C pairs with G")
        self.play(FadeIn(chips[2]), run_time=0.4)
        self.at("G pairs with C")
        self.play(FadeIn(chips[3]), run_time=0.4)
        self.at("uses U where")
        note = T("RNA: U in place of T", 28, ORANGE).move_to([4.0, 0.6, 0])
        self.play(Indicate(rna[1], color=ORANGE, scale_factor=1.3), FadeIn(note), run_time=0.8)

        pore = T("pore", 26, GREY).move_to([1.7, 0.95, 0])
        pore.shift(UP * 0.0)
        self.at("leaves the nucleus through pores")
        # make room: pore label sits above the gap, rna row moves through it
        grp = VGroup(rna, rna_lbl)
        self.play(FadeOut(note), FadeOut(links), FadeOut(title), FadeOut(chips), run_time=0.4)
        self.play(FadeIn(pore), run_time=0.3)
        self.play(grp.animate.move_to([4.6, 0.7, 0]), run_time=1.6)
        rna_lbl.next_to(rna, DOWN, buff=0.15)
        self.wait(0.4)
        self.finish()


# ---------------------------------------------------------------------------------------------
CODONS = ["AUG", "GAG", "GAA", "UUU", "UGA"]
AAS = ["Met", "Glu", "Glu", "Phe", None]


def mrna_row(y=0.5, w=0.6, size=26):
    r = row("".join(CODONS), ORANGE, w=w, size=size)
    return r.move_to([0, y, 0])


def codon_box(r, i, color=TEXT):
    g = VGroup(*r[3 * i:3 * i + 3])
    return box_around(g, color, pad=0.07, sw=3)


class S04Read(SpokenScene):
    """a ribosome reads the mRNA a codon at a time; tRNA brings amino acids; chain grows."""

    def construct(self):
        r = mrna_row(y=-0.2)
        r_lbl = T("messenger RNA", 26, ORANGE).move_to([3.0, -0.95, 0])
        self.play(FadeIn(r), FadeIn(r_lbl), run_time=0.6)
        cyt = T("cytoplasm", 28, GREY).to_corner(UL, buff=0.5)
        # ribosome around the first two codons
        ribo = RoundedRectangle(corner_radius=0.55, width=3.84, height=1.5, stroke_color=GREY, stroke_width=5, fill_color=GREY, fill_opacity=0.18)
        ribo.move_to(VGroup(*r[0:6]).get_center())
        ribo_lbl = T("ribosome", 28, GREY).move_to([-2.7, -1.35, 0])
        self.at("A ribosome in the cytoplasm")
        self.play(FadeIn(cyt), FadeIn(ribo, scale=1.1), FadeIn(ribo_lbl), run_time=0.7)

        boxes = [codon_box(r, i) for i in range(5)]
        self.at("three letters at a time")
        self.play(Create(boxes[0]), run_time=0.4)
        self.play(ReplacementTransform(boxes[0].copy(), boxes[1]), run_time=0.4)
        self.play(ReplacementTransform(boxes[1].copy(), boxes[2]), run_time=0.4)
        self.play(FadeOut(boxes[2]), FadeOut(boxes[0]), FadeOut(boxes[1]), run_time=0.2)
        cb = codon_box(r, 0, YELLOW)
        cb_lbl = T("codon", 28, YELLOW).move_to([-3.6, 1.35, 0])
        ribo_lbl2 = ribo_lbl
        self.at("Each group of three letters is a codon")
        # shift the ribosome label aside so the codon label has room
        self.play(Create(cb), run_time=0.4)
        self.play(FadeIn(cb_lbl), run_time=0.3)
        cb2 = codon_box(r, 1, YELLOW)
        self.play(Create(cb2), run_time=0.4)
        self.at("one amino acid, or for stop")
        self.wait(0.3)

        trs, aas = VGroup(), VGroup()
        for i, name in enumerate(["Met", "Glu"]):
            cx = r[3 * i + 1].get_center()[0]
            trna = chip("tRNA", PURPLE, 24).move_to([cx, -2.45, 0])
            aa = chip(name, GREEN, 26).move_to([cx, -3.3, 0])
            trs.add(trna); aas.add(aa)
        self.at("brings the matching amino acid")
        self.play(FadeIn(trs[0], shift=UP * 0.3), FadeIn(aas[0], shift=UP * 0.3), run_time=0.6)
        self.play(FadeIn(trs[1], shift=UP * 0.3), FadeIn(aas[1], shift=UP * 0.3), run_time=0.6)
        t_lbl = T("transfer RNA + amino acid", 24, PURPLE).move_to([3.0, -2.8, 0])
        self.play(FadeIn(t_lbl), run_time=0.3)
        self.at("joins the amino acids into a chain")
        link = Line(aas[0].get_right(), aas[1].get_left(), color=GREEN, stroke_width=6)
        self.play(FadeOut(t_lbl), FadeOut(trs), Create(link), run_time=0.6)
        ch_lbl = T("amino acid chain", 28, GREEN).move_to([3.0, -2.8, 0])
        self.play(FadeIn(ch_lbl), run_time=0.4)
        self.wait(0.5)
        self.play(*[FadeOut(m) for m in [r, r_lbl, cyt, ribo, ribo_lbl, cb, cb_lbl, cb2, aas, link, ch_lbl]], run_time=0.5)
        self.finish()


# ---------------------------------------------------------------------------------------------
class S05Chain(SpokenScene):
    """the codon chart in action: Met, Glu, Glu, Phe, stop; the chain is released and folds."""

    def construct(self):
        r = mrna_row(y=2.0, w=0.75, size=30)
        r_lbl = T("messenger RNA", 26, ORANGE).move_to([0, 3.0, 0])
        self.play(FadeIn(r), FadeIn(r_lbl), run_time=0.5)
        boxes = [codon_box(r, i) for i in range(5)]
        chips = [None] * 5
        arrows = [None] * 5

        def show(i, text, color, label=None):
            cx = r[3 * i + 1].get_center()[0]
            c = chip(text, color, 32).move_to([cx, 0.3, 0])
            a = arr([cx, 1.35, 0], [cx, 0.8, 0], color, 4, 0.16)
            chips[i], arrows[i] = c, a
            anims = [Create(boxes[i]), GrowArrow(a), FadeIn(c, shift=DOWN * 0.15)]
            return anims

        self.at("stands for methionine")
        self.play(*show(0, "Met", GREEN), run_time=0.7)
        start = T("start", 26, GREEN).next_to(chips[0], DOWN, buff=0.15)
        self.at("usual start")
        self.play(FadeIn(start), run_time=0.4)
        self.at("The codons")
        self.play(*show(1, "Glu", GREEN), run_time=0.5)
        self.play(*show(2, "Glu", GREEN), run_time=0.5)
        glu = T("glutamic acid", 26, GREEN).move_to([(chips[1].get_center()[0] + chips[2].get_center()[0]) / 2, -0.55, 0])
        self.play(FadeIn(glu), run_time=0.4)
        self.at("UUU stands")
        self.play(*show(3, "Phe", GREEN), run_time=0.6)
        self.at("means stop")
        self.play(*show(4, "STOP", RED), run_time=0.6)
        nothing = T("adds no amino acid", 26, RED).move_to([chips[4].get_center()[0] - 0.2, -0.55, 0])
        self.at("It adds no amino acid")
        self.play(FadeIn(nothing), run_time=0.4)

        # chain is released: the four chips slide down and link
        self.at("the chain is released")
        keep = [chips[0], chips[1], chips[2], chips[3]]
        self.play(FadeOut(start), FadeOut(glu), FadeOut(nothing), FadeOut(chips[4]), FadeOut(VGroup(*[a for a in arrows if a])),
                  FadeOut(VGroup(*boxes)), FadeOut(r), FadeOut(r_lbl), run_time=0.5)
        tgt = [[-2.4 + 1.6 * k, -1.2, 0] for k in range(4)]
        self.play(*[keep[k].animate.move_to(tgt[k]) for k in range(4)], run_time=0.8)
        links = VGroup(*[Line(keep[k].get_right() + RIGHT * 0.0, keep[k + 1].get_left(), color=GREEN, stroke_width=6) for k in range(3)])
        self.play(Create(links), run_time=0.4)
        lbl = T("amino acid chain", 28, GREEN).move_to([0, -2.1, 0])
        self.play(FadeIn(lbl), run_time=0.3)
        self.at("folds into a shape")
        # fold: chips regroup into a compact 2x2 blob
        pos = [[-0.9, 0.5, 0], [0.9, 0.5, 0], [0.9, -1.0, 0], [-0.9, -1.0, 0]]
        blob = RoundedRectangle(corner_radius=0.7, width=4.4, height=3.5, stroke_color=GREEN, stroke_width=4,
                                fill_color=GREEN, fill_opacity=0.1).move_to([0, -0.25, 0])
        self.play(*[keep[k].animate.move_to(pos[k]) for k in range(4)], FadeOut(links), FadeOut(lbl), run_time=0.9)
        newlinks = VGroup(Line(keep[0].get_right(), keep[1].get_left(), color=GREEN, stroke_width=6),
                          Line(keep[1].get_bottom(), keep[2].get_top(), color=GREEN, stroke_width=6),
                          Line(keep[2].get_left(), keep[3].get_right(), color=GREEN, stroke_width=6))
        self.play(Create(newlinks), FadeIn(blob), run_time=0.6)
        pl = T("protein", 30, GREEN).move_to([0, 2.0, 0])
        self.at("lets the protein work")
        self.play(FadeIn(pl), run_time=0.4)
        self.wait(0.5)
        self.play(FadeOut(VGroup(*keep, newlinks, blob, pl)), run_time=0.5)
        self.finish()


# ---------------------------------------------------------------------------------------------
class S06Change(SpokenScene):
    """GAG vs GTG: DNA -> mRNA -> amino acid -> hemoglobin behaviour."""

    def construct(self):
        xs = [-3.2, -0.6, 1.6, 4.5]
        heads = ["coding strand", "mRNA codon", "amino acid", "hemoglobin"]
        cols = [BLUE, ORANGE, GREEN, GREY]
        hd = VGroup(*[T(h, 24, c).move_to([x, 2.9, 0]) for h, x, c in zip(heads, xs, cols)])
        sub = T("beta-globin chain, amino acid 6 (usual numbering)", 22, GREY).move_to([0, 3.4, 0])
        self.play(FadeIn(hd), FadeIn(sub), run_time=0.5)
        lab1 = T("usual", 26, TEXT).move_to([-5.7, 1.4, 0])
        # row 1
        d1 = row("GAG", BLUE, w=0.62).move_to([xs[0], 1.4, 0])
        m1 = row("GAG", ORANGE, w=0.62).move_to([xs[1], 1.4, 0])
        a1 = chip("Glu", GREEN, 28).move_to([xs[2], 1.4, 0])
        ar1 = [arr([xs[0] + 1.1, 1.4, 0], [xs[1] - 1.1, 1.4, 0]), arr([xs[1] + 1.1, 1.4, 0], [xs[2] - 0.75, 1.4, 0])]
        g1l = T("glutamic acid", 22, GREEN).next_to(a1, DOWN, buff=0.12)
        self.at("In the usual numbering")
        self.play(FadeIn(lab1), FadeIn(d1), run_time=0.5)
        self.at("glutamic acid, coded by")
        self.play(GrowArrow(ar1[0]), FadeIn(m1), GrowArrow(ar1[1]), FadeIn(a1), FadeIn(g1l), run_time=1.0)

        lab2 = T("sickle allele", 26, YELLOW).move_to([-5.5, -0.7, 0])
        d2 = row("GTG", BLUE, w=0.62).move_to([xs[0], -0.7, 0])
        d2[1][1].set_color(YELLOW)
        d2[1][0].set_stroke(YELLOW).set_fill(YELLOW, 0.3)
        self.at("In the sickle allele")
        self.play(FadeIn(lab2), FadeIn(d2), run_time=0.5)
        m2 = row("GUG", ORANGE, w=0.62).move_to([xs[1], -0.7, 0])
        m2[1][1].set_color(YELLOW)
        m2[1][0].set_stroke(YELLOW).set_fill(YELLOW, 0.3)
        a2 = chip("Val", YELLOW, 28).move_to([xs[2], -0.7, 0])
        g2l = T("valine", 22, YELLOW).next_to(a2, DOWN, buff=0.12)
        ar2 = [arr([xs[0] + 1.1, -0.7, 0], [xs[1] - 1.1, -0.7, 0]), arr([xs[1] + 1.1, -0.7, 0], [xs[2] - 0.75, -0.7, 0])]
        cnote = T("coding strand matches the mRNA\nletter for letter, with T where mRNA has U", 24, GREY, line_spacing=0.9).move_to([-2.2, -1.95, 0])
        self.at("The coding strand matches")
        self.play(FadeIn(cnote), run_time=0.4)
        self.at("So the codon")
        self.play(GrowArrow(ar2[0]), FadeIn(m2), run_time=0.5)
        self.at("valine takes its place")
        self.play(GrowArrow(ar2[1]), FadeIn(a2), FadeIn(g2l), run_time=0.7)

        # hemoglobin behaviour
        sep = VGroup(*[RoundedRectangle(corner_radius=0.15, width=0.55, height=0.55, stroke_color=GREY, stroke_width=3,
                                        fill_color=GREY, fill_opacity=0.25) for _ in range(3)]).arrange(RIGHT, buff=0.35).move_to([xs[3], 1.4, 0])
        sep_l = T("stay separate", 22, GREY).next_to(sep, DOWN, buff=0.12)
        rod = RoundedRectangle(corner_radius=0.2, width=2.4, height=0.55, stroke_color=YELLOW, stroke_width=3,
                               fill_color=YELLOW, fill_opacity=0.25).move_to([xs[3], -0.7, 0])
        rod_l = T("stiff rods", 22, YELLOW).next_to(rod, DOWN, buff=0.12)
        self.at("Hemoglobin with valine")
        self.play(FadeIn(sep), FadeIn(sep_l), run_time=0.4)
        self.at("can stick into stiff rods")
        self.play(FadeIn(rod, scale=0.8), FadeIn(rod_l), run_time=0.6)
        note = T("mostly when oxygen is low", 24, YELLOW).move_to([4.2, -2.0, 0])
        self.at("mostly when oxygen is low")
        self.play(FadeIn(note), run_time=0.4)
        concl = T("one changed letter  →  can change one amino acid  →  can change the shape", 28, TEXT).move_to([0, -3.0, 0])
        fit(concl, max_w=12.2)
        self.at("One changed letter can change one amino acid")
        self.play(FadeIn(concl, shift=UP * 0.1), run_time=0.6)
        self.finish()


class S07End(EndCard):
    LINE = "One changed letter can change one amino acid."
