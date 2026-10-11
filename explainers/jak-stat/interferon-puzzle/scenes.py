"""The interferon puzzle: two laboratories, one missing kinase  (Biochemistrypedia section film)

Timed to the SPOKEN words: every self.at("...") cue waits for that phrase in audio/words.json.

COLOR MAP (one color per concept, whole film)
  YELLOW = interferon, the signal
  BLUE   = Darnell's laboratory (its name tags and arrow)
  PINK   = Stark, Kerr and Pellegrini's laboratory (its name tags and arrow)
  TEAL   = the proteins of the DNA-binding complex (ISGF3), later named STATs
  PURPLE = the kinase (a JAK; TYK2 is one)
  GOLD   = a phosphate (the round "P" badge)
  GREEN  = on / recovered / the genes switched on
  RED    = blocked or lost (the protein-synthesis drug, staurosporine, the lost part of the pathway)
  GREY   = membrane, DNA, labels, the unknown path

No molecular structures: proteins are labelled chips, DNA is a line with blocks on it, a phosphate
is a "P" badge, cells are rounded shapes or circles (an illustration, not to scale).
"""
import numpy as np
from bp_style import *  # noqa: F401,F403

PURPLE = "#B58CD9"
PINK = "#F08BB4"

PY = 0.4                       # y of the path strip (scenes 1 and 4)
IFN_X, GENE_X = -4.9, 5.0
DNA_L, DNA_R = 3.2, 6.4


# ---------------------------------------------------------------------------------------------
# helpers
# ---------------------------------------------------------------------------------------------
def bchip(text, color=BLUE, size=26, pad=0.2, **kw):
    """chip with an opaque backing so lines drawn behind it do not show through."""
    c = chip(text, color, size=size, pad=pad, **kw)
    back = RoundedRectangle(corner_radius=0.14, width=c[0].width, height=c[0].height, stroke_width=0,
                            fill_color=BG, fill_opacity=1).move_to(c[0])
    return VGroup(back, *c)


def arr(a, b, color=GREY, w=5, tip=0.22):
    return Arrow(a, b, buff=0.06, color=color, stroke_width=w, tip_length=tip,
                 max_tip_length_to_length_ratio=0.45, max_stroke_width_to_length_ratio=12)


def inhib(a, b, color=RED, w=6):
    a, b = np.array(a, float), np.array(b, float)
    d = (b - a) / np.linalg.norm(b - a)
    perp = np.array([-d[1], d[0], 0])
    return VGroup(Line(a, b, color=color, stroke_width=w), Line(b + perp * 0.28, b - perp * 0.28, color=color, stroke_width=w + 1))


def pbadge(k=1.0):
    c = Circle(radius=0.2 * k, stroke_color=GOLD, stroke_width=2, fill_color=GOLD, fill_opacity=1)
    return VGroup(c, T("P", 22 * k, BG, weight=BOLD).move_to(c))


def tag(text, color, y=3.35, size=28):
    return T(text, size, color, weight=BOLD).move_to([0, y, 0])


def dna_block(x, label, y, color=GREY, width=2.2, lbl_size=24, lbl_dy=-0.55, lbl_color=None):
    """a short block on a DNA line, with its label underneath."""
    b = Rectangle(width=width, height=0.3, stroke_width=0, fill_color=color, fill_opacity=1).move_to([x, y, 0])
    l = T(label, lbl_size, lbl_color or color).move_to([x, y + lbl_dy, 0])
    return b, l


def genes_end(y=PY, color=GREY, text="genes"):
    """DNA with the genes block, at the right-hand end of the path."""
    dna = Line([DNA_L, y, 0], [DNA_R, y, 0], color=GREY, stroke_width=9)
    blk = Rectangle(width=2.4, height=0.5, stroke_width=0, fill_color=color, fill_opacity=1).move_to([GENE_X, y, 0])
    lbl = T(text, 34, color).move_to([GENE_X, y - 0.8, 0])
    g = VGroup(dna, blk, lbl)
    g.blk, g.lbl = blk, lbl
    return g


def genes_on(g):
    return [g.blk.animate.set_fill(GREEN), g.lbl.animate.set_color(GREEN)]


def genes_off(g):
    return [g.blk.animate.set_fill(GREY), g.lbl.animate.set_color(GREY)]


def unknown_path(y=PY, x0=IFN_X + 1.6, x1=GENE_X - 3.0):
    """a dashed grey arrow with one question mark: the part nobody knew."""
    ln = DashedLine([x0, y, 0], [x1, y, 0], color=GREY, stroke_width=8, dash_length=0.2)
    tip = Triangle(fill_color=GREY, fill_opacity=1, stroke_width=0).scale(0.16).rotate(-PI / 2).move_to([x1 + 0.1, y, 0])
    q = T("?", 110, GREY, weight=BOLD).move_to([(x0 + x1) / 2, y + 0.05, 0])
    qback = Rectangle(width=q.width + 0.5, height=1.0, stroke_width=0, fill_color=BG, fill_opacity=1).move_to(q)
    g = VGroup(ln, tip, qback, q)
    g.q = q
    return g


def ifn_chip(x=IFN_X, y=PY, size=36):
    return bchip("interferon", YELLOW, size).move_to([x, y, 0])


class Film(SpokenScene):
    def outro(self, *anims, run_time=0.4):
        """hold to the end of the narration, then clear what the next scene does not inherit."""
        rest = self.narration_s - 0.02 - self.elapsed()
        if rest > 0:
            self.wait(rest)
        if anims:
            self.play(*anims, run_time=run_time)
        self.finish()


class S00Title(TitleCard):
    LESSON = "Cytokine Receptors and JAK–STAT"
    TITLE = "Two labs, one missing kinase"


# ---------------------------------------------------------------------------------------------
class S01Ends(Film):
    """drug blocks new protein, genes still switch on: the factor is already there. Two ends (the next scene carries them on)."""

    def construct(self):
        ifn = ifn_chip()
        path = unknown_path()
        genes = genes_end()
        self.play(FadeIn(ifn), FadeIn(genes), Create(path[0]), FadeIn(path[1:]), run_time=0.7)

        # the drug: no new protein
        newp = bchip("new protein", GREY, 32).move_to([0.6, 2.7, 0])
        drug = bchip("drug", RED, 32).move_to([-3.2, 2.7, 0])
        self.play(FadeIn(newp), FadeIn(drug), run_time=0.4)
        self.at("any new protein")
        blk = inhib(drug.get_right() + RIGHT * 0.05, newp.get_left() + LEFT * 0.05)
        self.play(Create(blk), run_time=0.4)
        self.play(newp[1].animate.set_stroke(opacity=0.35).set_fill(opacity=0.05), newp[2].animate.set_opacity(0.35), run_time=0.3)

        # genes switch on anyway
        self.at("interferon still switches genes on")
        gar = Arrow([GENE_X - 1.4, PY + 0.7, 0], [GENE_X + 1.4, PY + 0.7, 0], buff=0, color=GREEN, stroke_width=5, tip_length=0.2)
        self.play(*genes_on(genes), GrowArrow(gar), path[0].animate.set_color(GREEN), run_time=0.6)

        # so the factor is already there
        self.at("So the factor must already be in the cell")
        wait = T("already in the cell", 32, GREY).move_to([-0.8, PY - 1.3, 0])
        self.play(Indicate(path.q, color=TEXT, scale_factor=1.3), FadeIn(wait, shift=UP * 0.1), run_time=0.7)

        # clear the drug test, then two ends
        self.at("Two laboratories")
        self.play(FadeOut(VGroup(newp, drug, blk, gar, wait)), *genes_off(genes), path[0].animate.set_color(GREY), run_time=0.5)
        lft = arr([IFN_X + 1.2, PY - 2.0, 0], [IFN_X + 3.8, PY - 2.0, 0], PINK, w=10, tip=0.3)
        rgt = arr([GENE_X - 1.2, PY - 2.0, 0], [GENE_X - 3.8, PY - 2.0, 0], BLUE, w=10, tip=0.3)
        self.at("from opposite ends")
        self.play(GrowArrow(lft), GrowArrow(rgt), run_time=0.7)
        self.outro()


# ---------------------------------------------------------------------------------------------
class S02Darnell(Film):
    """Darnell starts at the gene; ISGF3 binds the shared sequence after tyrosine phosphorylation; staurosporine blocks."""

    def construct(self):
        MEM_Y, DNA_Y = 2.15, -2.6
        # carried over from scene 1: the path, with the two arrows from the two ends
        ifn0, genes0, path0 = ifn_chip(), genes_end(), unknown_path()
        lft = arr([IFN_X + 1.2, PY - 2.0, 0], [IFN_X + 3.8, PY - 2.0, 0], PINK, w=10, tip=0.3)
        rgt = arr([GENE_X - 1.2, PY - 2.0, 0], [GENE_X - 3.8, PY - 2.0, 0], BLUE, w=10, tip=0.3)
        strip = VGroup(ifn0, genes0, path0, lft, rgt)
        self.add(strip)
        self.at("James Darnell's laboratory")
        who0 = T("James Darnell", 34, BLUE, weight=BOLD).move_to([GENE_X - 2.5, PY - 2.8, 0])
        self.play(FadeIn(who0, shift=UP * 0.1), Indicate(rgt, color=BLUE, scale_factor=1.2), run_time=0.6)
        self.at("at the gene")
        self.play(Indicate(genes0[1], color=BLUE, scale_factor=1.15), run_time=0.6)

        mem = RoundedRectangle(corner_radius=0.1, width=12.6, height=0.3, stroke_color=GREY, stroke_width=3,
                               fill_color=GREY, fill_opacity=0.35).move_to([0, MEM_Y, 0])
        dna = Line([-5.8, DNA_Y, 0], [5.8, DNA_Y, 0], color=GREY, stroke_width=7)
        seq = Rectangle(width=0.9, height=0.34, stroke_width=0, fill_color=GREY, fill_opacity=1).move_to([-1.2, DNA_Y, 0])
        gene = Rectangle(width=2.4, height=0.34, stroke_width=0, fill_color=GREY, fill_opacity=1).move_to([2.6, DNA_Y, 0])
        gl = T("genes", 26, GREY).move_to([2.6, DNA_Y - 0.55, 0])
        sl = T("short shared sequence", 26, GREY).move_to([-3.3, DNA_Y - 0.55, 0])

        # a protein complex that binds a short sequence shared by the responsive genes
        self.at("found a protein complex")
        cx = bchip("ISGF3", TEAL, 38).move_to([-1.2, 0.2, 0])
        lab = tag("Darnell's laboratory", BLUE, y=3.45, size=26)
        self.play(FadeOut(strip), FadeOut(who0), FadeIn(mem), Create(dna), FadeIn(lab), run_time=0.6)
        self.play(FadeIn(cx, shift=DOWN * 0.3), run_time=0.5)
        self.at("that binds")
        link = DashedLine(cx.get_bottom() + DOWN * 0.05, [-1.2, DNA_Y + 0.3, 0], color=TEAL, stroke_width=5, dash_length=0.18)
        self.play(Create(link), run_time=0.6)
        self.at("short DNA sequence")
        self.play(FadeIn(seq, scale=1.4), FadeIn(sl), run_time=0.5)
        self.at("shared by")
        self.play(FadeIn(gene), FadeIn(gl), run_time=0.5)

        # August 1992: interferon puts phosphate on tyrosines, and the complex binds
        self.at("In August")
        date = T("August 1992", 28, BLUE, weight=BOLD).move_to([-4.7, 3.45, 0])
        self.play(FadeOut(lab), FadeIn(date), run_time=0.5)
        self.at("Christian Schindler")
        who = T("Schindler, Shuai and colleagues", 24, BLUE).move_to([4.4, 3.45, 0])
        self.play(FadeIn(who), run_time=0.4)
        self.at("interferon puts phosphate")
        ifn = bchip("interferon", YELLOW, 28).move_to([-4.6, MEM_Y + 0.7, 0])
        self.play(FadeIn(ifn, shift=DOWN * 0.2), run_time=0.4)
        self.play(ifn.animate.move_to([-1.2, MEM_Y + 0.7, 0]), run_time=0.5)
        p1 = pbadge().move_to(cx.get_corner(UL) + [0.05, 0.05, 0])
        self.at("its proteins")
        ptxt = T("phosphorylated on tyrosine", 26, GOLD).next_to(cx, LEFT, buff=0.6)
        self.play(FadeIn(p1, scale=1.6), FadeIn(ptxt), run_time=0.6)
        solid = Line(cx.get_bottom() + DOWN * 0.05, [-1.2, DNA_Y + 0.3, 0], color=TEAL, stroke_width=5)
        self.play(Transform(link, solid), run_time=0.4)
        self.play(cx.animate.move_to([-1.2, DNA_Y + 0.85, 0]), p1.animate.move_to([-1.2 - cx.width / 2 + 0.05, DNA_Y + 1.35, 0]),
                  FadeOut(ptxt),
                  Transform(link, Line([-1.2, DNA_Y + 0.5, 0], [-1.2, DNA_Y + 0.3, 0], color=TEAL, stroke_width=5)), run_time=0.9)

        # staurosporine: reset the picture to neutral, then show the block
        self.at("a drug that blocks")
        stau = bchip("staurosporine", RED, 28).move_to([4.3, 0.9, 0])
        self.play(FadeOut(VGroup(p1, link, ifn)), cx.animate.move_to([-1.2, 0.2, 0]), FadeIn(stau, shift=LEFT * 0.2), run_time=0.8)
        self.at("blocks many kinases")
        kin = T("many kinases", 26, PURPLE).move_to([4.3, -0.15, 0])
        self.play(FadeIn(kin), run_time=0.4)
        self.at("stopped the activation")
        ifn2 = bchip("interferon", YELLOW, 28).move_to([-1.2, MEM_Y + 0.7, 0])
        stop = inhib(stau.get_left() + LEFT * 0.05, cx.get_right() + RIGHT * 0.1)
        nop = T("activation blocked", 26, RED).next_to(cx, LEFT, buff=0.5)
        self.play(FadeIn(ifn2, shift=DOWN * 0.2), Create(stop), FadeIn(nop), run_time=0.7)

        # some kinase
        self.at("Some kinase had to act first")
        qk = bchip("kinase  ?", PURPLE, 34).move_to([-1.2, 1.5, 0])
        self.play(FadeOut(VGroup(kin, nop)), FadeIn(qk, shift=DOWN * 0.2), run_time=0.6)
        self.at("it could not say")
        self.play(Indicate(VGroup(*qk[1:]), color=PURPLE, scale_factor=1.15), run_time=0.8)
        self.outro(FadeOut(VGroup(mem, dna, seq, gene, gl, sl, cx, date, who, ifn2, stau, stop, qk)))


# ---------------------------------------------------------------------------------------------
class S03Pellegrini(Film):
    """Stark and Kerr's laboratory: Pellegrini's selection, the mutants, complementation, TYK2."""

    def construct(self):
        lab = tag("Stark and Kerr's laboratory, London", PINK, y=3.4, size=28)
        names = VGroup(T("George Stark and Ian Kerr", 44, PINK, weight=BOLD), T("their laboratory, London", 32, PINK)).arrange(DOWN, buff=0.3).move_to([0, 0.3, 0])
        self.play(FadeIn(names, shift=UP * 0.15), run_time=0.6)
        self.at("started with genetics")
        gen = T("genetics", 56, PINK, weight=BOLD).move_to([0, 0.3, 0])
        self.play(FadeIn(lab, shift=DOWN * 0.1), ReplacementTransform(names, gen), run_time=0.7)

        # Pellegrini's built cell
        self.at("Sandra Pellegrini")
        who = T("Sandra Pellegrini", 30, PINK).move_to([0, 2.6, 0])
        self.play(FadeOut(gen), FadeIn(who), run_time=0.4)
        self.at("built human cells")
        cell = RoundedRectangle(corner_radius=0.9, width=9.2, height=3.9, stroke_color=GREY, stroke_width=4,
                                fill_color=GREY, fill_opacity=0.08).move_to([0, -0.2, 0])
        self.play(FadeIn(cell, scale=0.95), run_time=0.5)
        dna = Line([-3.8, -0.2, 0], [3.8, -0.2, 0], color=GREY, stroke_width=7)
        self.play(Create(dna), run_time=0.4)
        self.at("marker gene")
        mb, ml = dna_block(2.0, "marker gene", -0.2, GREEN, width=1.7, lbl_size=24, lbl_dy=-0.6)
        self.play(FadeIn(mb, scale=1.3), FadeIn(ml), run_time=0.6)
        self.at("responsive DNA")
        rb, rl = dna_block(-1.9, "interferon-responsive DNA", -0.2, YELLOW, width=1.7, lbl_size=24, lbl_dy=-0.6)
        ctl = arr([-1.0, 0.55, 0], [1.1, 0.55, 0], GREY, w=5)
        self.play(FadeIn(rb, scale=1.3), FadeIn(rl), GrowArrow(ctl), run_time=0.6)

        # the survival test
        self.at("Only cells deaf")
        self.play(FadeOut(VGroup(cell, dna, rb, rl, mb, ml, ctl, who)), run_time=0.5)
        rows, cols, sp = 4, 8, 1.05
        dots = VGroup()
        for r in range(rows):
            for c in range(cols):
                d = Circle(radius=0.38, stroke_color=GREEN, stroke_width=3, fill_color=GREEN, fill_opacity=0.25)
                d.move_to([(c - (cols - 1) / 2) * sp, (r - (rows - 1) / 2) * sp + 0.1, 0])
                dots.add(d)
        deaf = [3, 14, 25]
        medium = T("with interferon", 30, YELLOW).move_to([0, 2.65, 0])
        ill = T("illustration, not to scale", 22, GREY).move_to([0, -3.35, 0])
        self.play(FadeIn(dots, lag_ratio=0.02), FadeIn(medium), FadeIn(ill), run_time=0.8)
        self.at("deaf to interferon")
        for i in deaf:
            dots[i].set_stroke(GREY).set_fill(GREY, 0.25)
        self.play(*[dots[i].animate.set_stroke(GREY).set_fill(GREY, 0.3) for i in deaf], run_time=0.5)
        gone = [dots[i] for i in range(len(dots)) if i not in deaf]
        self.play(*[FadeOut(g) for g in gone], run_time=0.8)
        lblD = T("deaf to interferon: survive", 26, GREY).move_to([0, -2.65, 0])
        self.play(FadeIn(lblD), run_time=0.4)

        # a hundred million
        self.at("mutagenized cells")
        cnt = T("about 100,000,000 mutagenized cells screened", 28, PINK).move_to([0, -3.1, 0])
        self.play(FadeOut(medium), FadeOut(ill), FadeOut(lblD), FadeIn(cnt, shift=UP * 0.1), run_time=0.6)

        # each mutant had lost a part
        self.at("Each mutant")
        keep = dots[deaf[1]]
        self.play(FadeOut(VGroup(dots[deaf[0]], dots[deaf[2]], cnt)), keep.animate.scale(1.0).move_to([-5.0, 0.4, 0]), run_time=0.7)
        self.remove(keep)
        mut = bchip("mutant", GREY, 36).move_to([-5.0, 0.4, 0])
        ifn = ifn_chip(-5.0, 2.0, 26)
        genes = genes_end(0.4, text="marker gene")
        left = DashedLine([-3.6, 0.4, 0], [-0.9, 0.4, 0], color=GREY, stroke_width=6, dash_length=0.2)
        gap = Cross(Rectangle(width=0.9, height=0.9), stroke_color=RED, stroke_width=10).scale(0.9).move_to([-0.2, 0.4, 0])
        right = DashedLine([0.5, 0.4, 0], [3.0, 0.4, 0], color=GREY, stroke_width=6, dash_length=0.2)
        self.play(FadeIn(mut), FadeIn(ifn), FadeIn(genes), Create(left), Create(right), run_time=0.7)
        self.at("lost a part")
        lost = T("a part is lost", 34, RED).move_to([-0.2, 1.6, 0])
        self.play(Create(gap), FadeIn(lost, shift=DOWN * 0.1), run_time=0.6)

        # complementation
        self.at("DNA from normal cells")
        nd = bchip("DNA from normal cells", PINK, 32).move_to([-3.4, -2.1, 0])
        self.play(FadeIn(nd, shift=UP * 0.2), run_time=0.5)
        self.play(nd.animate.move_to([-4.0, -0.95, 0]), run_time=0.7)
        self.at("into a mutant")
        self.play(nd.animate.scale(0.6).move_to(mut.get_bottom() + DOWN * 0.15), run_time=0.5)
        self.at("the rare cell")
        rare = T("the rare cell that recovers", 34, GREEN).move_to([0, -2.1, 0])
        self.play(FadeOut(nd), FadeOut(gap), FadeOut(lost), FadeIn(rare, shift=UP * 0.1), *genes_on(genes),
                  left.animate.set_color(GREEN), right.animate.set_color(GREEN), mut[1].animate.set_stroke(GREEN), run_time=0.8)

        # July 1992, Paris, TYK2
        self.at("In July 1992")
        date = T("July 1992 · Paris", 28, PINK, weight=BOLD)
        self.play(FadeOut(rare), ReplacementTransform(lab, date.move_to([0, 3.4, 0])), run_time=0.5)
        self.at("the gene that rescued")
        tk = bchip("TYK2", PURPLE, 40).move_to([-0.2, 0.4, 0])
        self.play(FadeIn(tk, scale=1.5), run_time=0.6)
        self.at("tyk2")
        self.play(Indicate(VGroup(*tk[1:]), color=PURPLE, scale_factor=1.2), run_time=0.8)
        self.outro(FadeOut(VGroup(date, mut, ifn, genes, left, right, tk)))


# ---------------------------------------------------------------------------------------------
class S04Fit(Film):
    """July and August 1992 two weeks apart; a JAK is required, the proteins carry phosphotyrosine; STATs."""

    def construct(self):
        # timeline
        TY = 2.9
        line = Line([-3.6, TY, 0], [3.6, TY, 0], color=GREY, stroke_width=5)
        tj = Dot([-3.0, TY, 0], radius=0.14, color=PINK)
        ta = Dot([3.0, TY, 0], radius=0.14, color=BLUE)
        lj = T("July 1992", 28, PINK, weight=BOLD).next_to(tj, UP, buff=0.3)
        la = T("August 1992", 28, BLUE, weight=BOLD).next_to(ta, UP, buff=0.3)
        two = T("two weeks", 26, GREY).move_to([0, TY - 0.5, 0])
        self.play(Create(line), run_time=0.4)
        self.play(FadeIn(tj), FadeIn(lj), FadeIn(ta), FadeIn(la), FadeIn(two), run_time=0.6)

        # the path, with the two arrows from the two ends
        ifn = ifn_chip(y=-0.3)
        genes = genes_end(-0.3)
        path = unknown_path(-0.3)
        self.play(FadeIn(ifn), FadeIn(genes), FadeIn(path), run_time=0.6)
        self.at("the results fit together")
        lft = arr([IFN_X + 1.2, -1.9, 0], [IFN_X + 3.8, -1.9, 0], PINK, w=10, tip=0.3)
        rgt = arr([GENE_X - 1.2, -1.9, 0], [GENE_X - 3.8, -1.9, 0], BLUE, w=10, tip=0.3)
        self.play(GrowArrow(lft), GrowArrow(rgt), run_time=0.7)
        self.play(lft.animate.shift(RIGHT * 0.7), rgt.animate.shift(LEFT * 0.7), run_time=0.6)

        self.at("is required")
        self.play(FadeOut(two), run_time=0.3)
        jk = bchip("a JAK", PURPLE, 36).move_to([-2.4, 0.9, 0])
        self.play(FadeIn(jk, shift=DOWN * 0.2), run_time=0.6)
        self.at("proteins carry")
        pr = bchip("DNA-binding proteins", TEAL, 32).move_to([2.4, 0.9, 0])
        pp = pbadge().move_to(pr.get_corner(UR) + [-0.1, 0.05, 0])
        ptxt = T("phosphotyrosine", 30, GOLD).move_to([2.4, 1.95, 0])
        self.play(FadeIn(pr, shift=DOWN * 0.2), run_time=0.5)
        self.play(FadeIn(pp, scale=1.6), FadeIn(ptxt), run_time=0.5)

        self.at("named those")
        self.play(FadeOut(ptxt), run_time=0.4)
        st = bchip("STATs", TEAL, 36).move_to(pr.get_center())
        self.play(Transform(pr, st), pp.animate.move_to(st.get_corner(UR) + [-0.05, 0.05, 0]), run_time=0.7)
        full = T("signal transducers and activators of transcription", 32, TEAL).move_to([0, -3.1, 0])
        self.play(FadeIn(full, shift=UP * 0.1), run_time=0.9)
        self.outro()


class S05End(EndCard):
    LINE = "Two opposite routes found a JAK and the STATs."
