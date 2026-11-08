"""Genetic engineering: cut, join, copy a gene  (Biochemistrypedia explainer)

COLOR MAP (one color per concept, whole video)
  YELLOW = the human insulin gene / insulin / copies of the chosen DNA stretch (PCR)
  ORANGE = the plasmid (bacterial DNA that copies itself)
  PURPLE = a cutting tool (restriction enzyme, Cas9)
  GREEN  = joining (DNA ligase) and the sealed result
  TEAL   = vocabulary term labels, sticky ends, a matched sequence
  BLUE   = guide RNA
  RED    = the antibiotic
  GOLD   = year tag, the essential question's key words
  GREY   = cells, DNA bars of other DNA, outlines, side notes
"""
import numpy as np
from bp_style import *  # noqa: F401,F403

PURPLE = "#B58CD9"
ORANGE = "#F29E4C"
SW = 14  # stroke width of plasmid loops


def after(sc, phrase, dt, nth=0):
    """wait until `dt` seconds after the narrator starts `phrase`."""
    target = sc.t_of(phrase, nth) + dt
    rest = target - sc.elapsed()
    if rest > 0.02:
        sc.wait(rest)


def arr(a, b, color=GREY, w=5, tip=0.22):
    return Arrow(a, b, buff=0.06, color=color, stroke_width=w, tip_length=tip,
                 max_tip_length_to_length_ratio=0.45, max_stroke_width_to_length_ratio=12)


def term(text, size=32, color=TEAL):
    return T(text, size, color, weight=BOLD)


def seg(x0, x1, y, color, h=0.5):
    return Rectangle(width=x1 - x0, height=h, stroke_width=0, fill_color=color, fill_opacity=0.95).move_to([(x0 + x1) / 2, y, 0])


def bars(x0, x1, y, color=GREY, h=0.5, gap=0.08):
    """DNA drawn as two parallel bars (never a helix)."""
    return VGroup(seg(x0, x1, y + (h + gap) / 2, color, h), seg(x0, x1, y - (h + gap) / 2, color, h))


def ring_arc(center, r, start_deg, angle_deg, color, w=SW):
    return Arc(radius=r, start_angle=np.radians(start_deg), angle=np.radians(angle_deg), arc_center=center,
               stroke_color=color, stroke_width=w)


def rec_ring(center, r, w=6):
    """a small plasmid loop that carries the yellow gene."""
    return VGroup(ring_arc(center, r, 120, 300, ORANGE, w), ring_arc(center, r, 60, 60, YELLOW, w))


def cell(center, w=1.9, h=1.5, color=GREY):
    return RoundedRectangle(corner_radius=0.5, width=w, height=h, stroke_color=color, stroke_width=4,
                            fill_color=color, fill_opacity=0.08).move_to(center)


class S00Title(TitleCard):
    LESSON = "Engineering genes"
    TITLE = "Cut, join, copy a gene"


# ---------------------------------------------------------------------------------------------
class S01Insulin(SpokenScene):
    """animal insulin -> 1982 bacteria make human insulin -> no human insulin gene -> the questions."""

    def construct(self):
        head = T("for about 60 years, mostly", 30, GREY).move_to([0, 3.0, 0])
        ins = chip("insulin", YELLOW, 44).move_to([3.0, 0.0, 0])
        sub = T("for people with diabetes", 28, GREY).next_to(ins, DOWN, buff=0.3)
        cat = chip("cattle pancreas", GREY, 34).move_to([-3.6, 1.4, 0])
        pig = chip("pig pancreas", GREY, 34).move_to([-3.6, -1.4, 0])
        a1 = arr(cat.get_right(), ins.get_left() + UP * 0.2, GREY)
        a2 = arr(pig.get_right(), ins.get_left() + DOWN * 0.2, GREY)
        self.at("For about")
        self.play(FadeIn(head, shift=DOWN * 0.1), run_time=0.5)
        self.at("insulin for people")
        self.play(FadeIn(ins, scale=0.9), FadeIn(sub), run_time=0.6)
        self.at("pancreases of cattle")
        self.play(FadeIn(cat, shift=RIGHT * 0.2), GrowArrow(a1), run_time=0.6)
        self.at("and pigs")
        self.play(FadeIn(pig, shift=RIGHT * 0.2), GrowArrow(a2), run_time=0.6)

        # 1982: bacteria
        after(self, "and pigs", 1.4)
        old = VGroup(head, ins, sub, cat, pig, a1, a2)
        year = M("1982", 64, GOLD).move_to([0, 3.0, 0])
        fda = T("FDA approves", 30, GREY).next_to(year, RIGHT, buff=0.5)
        bact = cell([-3.2, 0.1, 0], w=4.6, h=2.8)
        bact_l = T("bacteria", 32, GREY).next_to(bact, DOWN, buff=0.25)
        hins = chip("human insulin", YELLOW, 36).move_to([3.6, 0.1, 0])
        a3 = arr(bact.get_right(), hins.get_left(), YELLOW)
        self.play(FadeOut(old), FadeIn(year, scale=0.9), FadeIn(fda), run_time=0.6)
        self.at("approved human insulin")
        self.play(FadeIn(hins, scale=0.9), run_time=0.5)
        self.at("made by bacteria")
        self.play(FadeIn(bact, scale=0.95), FadeIn(bact_l), GrowArrow(a3), run_time=0.7)

        # no human insulin gene
        self.at("Bacteria have no")
        dna = bars(-1.7, 1.7, 0, GREY, h=0.28, gap=0.06)
        dna_l = T("bacterial DNA", 26, GREY)
        self.play(FadeOut(VGroup(year, fda, hins, a3)), bact.animate.scale(1.25).move_to([0, -0.7, 0]),
                  FadeOut(bact_l), run_time=0.7)
        dna.move_to(bact.get_center() + UP * 0.1)
        dna_l.next_to(dna, DOWN, buff=0.3)
        self.play(FadeIn(dna), FadeIn(dna_l), run_time=0.5)
        box = DashedVMobject(Rectangle(width=2.6, height=1.0, stroke_color=YELLOW, stroke_width=4), num_dashes=24)
        q = T("?", 44, YELLOW, weight=BOLD)
        gbox = VGroup(box, q).move_to([0, 3.0, 0])
        glab = T("human insulin gene", 30, YELLOW).next_to(gbox, RIGHT, buff=0.3)
        self.at("human insulin gene")
        self.play(FadeIn(gbox, scale=0.9), FadeIn(glab), run_time=0.6)
        self.at("get into a microbe")
        self.play(gbox.animate.move_to([0, 1.9, 0]), glab.animate.next_to([0, 1.9, 0], RIGHT, buff=1.45), run_time=0.9)
        self.play(Indicate(q, color=YELLOW, scale_factor=1.4), run_time=0.6)

        # the essential question
        self.at("And can we design life")
        self.play(FadeOut(VGroup(bact, dna, dna_l, gbox, glab)), run_time=0.6)
        e1 = T("Can we design life,", 46, GOLD, font=TITLE_FONT)
        e2 = T("and how should we decide", 40, TEXT, font=TITLE_FONT)
        e3 = T("when we should?", 40, TEXT, font=TITLE_FONT)
        eq = VGroup(e1, e2, e3).arrange(DOWN, buff=0.3).move_to([0, 0.2, 0])
        self.play(FadeIn(e1, shift=UP * 0.15), run_time=0.6)
        self.at("how should we decide")
        self.play(FadeIn(e2, shift=UP * 0.15), run_time=0.5)
        self.at("when we should")
        self.play(FadeIn(e3, shift=UP * 0.15), run_time=0.5)
        self.finish()


# ---------------------------------------------------------------------------------------------
A, B_, C1, C2, TL = -6.0, 6.0, -2.3, 2.3, 0.55
YT, YB, BH = 0.4, -0.3, 0.62


def build_dna(gene_color=YELLOW):
    """DNA as two parallel bars cut at two staggered sites; returns left, middle (gene), right pieces and the tails."""
    lt = seg(A, C1, YT, GREY, BH)
    lb = seg(A, C1, YB, GREY, BH)
    lbt = seg(C1, C1 + TL, YB, GREY, BH)        # left piece, bottom tail
    mtt = seg(C1, C1 + TL, YT, gene_color, BH)  # middle piece, top tail
    mt = seg(C1 + TL, C2, YT, gene_color, BH)
    mb = seg(C1 + TL, C2, YB, gene_color, BH)
    mbt = seg(C2, C2 + TL, YB, gene_color, BH)  # middle piece, bottom tail
    rtt = seg(C2, C2 + TL, YT, GREY, BH)        # right piece, top tail
    rt = seg(C2 + TL, B_, YT, GREY, BH)
    rb = seg(C2 + TL, B_, YB, GREY, BH)
    return VGroup(lt, lb, lbt), VGroup(mtt, mt, mb, mbt), VGroup(rtt, rt, rb)


GENE_SCALE = 1.4
GENE_POS = np.array([0.0, -0.2, 0.0])


class S02Cut(SpokenScene):
    """DNA bars with a gene piece -> restriction enzyme cuts at two matching short sequences -> sticky ends."""

    def construct(self):
        ge = term("genetic engineering", 36).move_to([0, 3.3, 0])
        ge_s = T("using laboratory tools to change an organism's DNA", 28, GREY).move_to([0, 2.65, 0])
        L, Mid, R = build_dna()
        dna_l = T("DNA", 30, GREY).move_to([A + 0.5, 1.35, 0])
        gene_l = T("human insulin gene", 28, YELLOW).move_to([0.275, -2.4, 0])
        self.at("Genetic engineering")
        self.play(FadeIn(ge, shift=DOWN * 0.1), run_time=0.5)
        self.at("laboratory tools")
        self.play(FadeIn(ge_s), run_time=0.5)
        self.play(FadeIn(L), FadeIn(Mid), FadeIn(R), FadeIn(dna_l), FadeIn(gene_l), run_time=0.7)
        same = T("the same kind of molecule in every living thing", 28, GREY).move_to([0, -3.1, 0])
        self.at("the same kind")
        self.play(FadeIn(same, shift=UP * 0.1), run_time=0.5)
        self.at("another species")
        self.play(Indicate(Mid, color=YELLOW, scale_factor=1.04), run_time=0.7)

        # restriction enzyme
        self.at("A restriction enzyme")
        self.play(FadeOut(same), FadeOut(ge_s), run_time=0.4)
        enz = chip("restriction enzyme", PURPLE, 30).move_to([-3.4, 2.4, 0])
        m1 = RoundedRectangle(corner_radius=0.08, width=TL + 0.4, height=1.9, stroke_color=TEAL, stroke_width=4).move_to([C1 + TL / 2, 0.05, 0])
        m2 = m1.copy().move_to([C2 + TL / 2, 0.05, 0])
        s1 = T("short sequence", 26, TEAL).move_to([C1 + TL / 2, -1.35, 0])
        s2 = T("short sequence", 26, TEAL).move_to([C2 + TL / 2, -1.35, 0])
        self.play(FadeIn(enz, shift=DOWN * 0.2), run_time=0.5)
        self.at("cuts DNA at")
        self.play(FadeIn(m1), FadeIn(s1), FadeIn(m2), FadeIn(s2), FadeOut(gene_l), run_time=0.6)
        self.at("one particular")
        self.play(enz.animate.move_to([C1 + TL / 2, 2.05, 0]), run_time=0.5)
        self.play(L.animate.shift(LEFT * 0.7), FadeOut(m1), s1.animate.shift(LEFT * 0.7),
                  Flash(np.array([C1 + TL / 2, 0.05, 0]), color=PURPLE, flash_radius=0.8), run_time=0.5)
        self.play(enz.animate.move_to([C2 + TL / 2, 2.05, 0]), run_time=0.5)
        self.play(R.animate.shift(RIGHT * 0.7), FadeOut(m2), s2.animate.shift(RIGHT * 0.7),
                  Flash(np.array([C2 + TL / 2, 0.05, 0]), color=PURPLE, flash_radius=0.8), run_time=0.5)
        self.play(FadeOut(enz), FadeOut(s1), FadeOut(s2), FadeOut(dna_l), run_time=0.4)

        # sticky ends
        self.at("Many restriction enzymes")
        tgt = Mid.copy().scale(GENE_SCALE).move_to(GENE_POS)
        self.play(FadeOut(L), FadeOut(R), Mid.animate.scale(GENE_SCALE).move_to(GENE_POS), run_time=0.9)
        self.at("stranded tails")
        self.play(Mid[0].animate.set_color(TEAL), Mid[3].animate.set_color(TEAL), run_time=0.5)
        top_t, bot_t = Mid[0], Mid[3]
        tl1 = T("single-stranded tail", 26, TEAL).move_to([top_t.get_center()[0] - 0.4, 1.9, 0])
        tl2 = T("single-stranded tail", 26, TEAL).move_to([bot_t.get_center()[0] + 0.4, -2.2, 0])
        ar1 = arr(tl1.get_bottom() + DOWN * 0.05, top_t.get_top() + UP * 0.03, TEAL)
        ar2 = arr(tl2.get_top() + UP * 0.05, bot_t.get_bottom() + DOWN * 0.03, TEAL)
        self.play(FadeIn(tl1), GrowArrow(ar1), FadeIn(tl2), GrowArrow(ar2), run_time=0.7)
        self.at("called sticky ends")
        se = term("sticky ends", 46).move_to([0, -3.1, 0])
        self.play(FadeIn(se, scale=0.9), run_time=0.6)
        self.finish()


# ---------------------------------------------------------------------------------------------
CTR = np.array([0.0, 0.5, 0.0])
R_ = 1.8


class S03Join(SpokenScene):
    """plasmid (copies itself) -> cut open with the same enzyme -> gene slides in, ends pair -> ligase seals -> recombinant DNA."""

    def construct(self):
        # the gene piece, rebuilt where S02 left it
        _, gene, _ = build_dna()
        gene.scale(GENE_SCALE).move_to(GENE_POS)
        gene[0].set_color(TEAL)
        gene[3].set_color(TEAL)
        self.add(gene)
        gene_l = T("insulin gene,\nwith sticky ends", 26, YELLOW, line_spacing=0.8).move_to([3.6, -2.9, 0])

        ring = Circle(radius=R_, arc_center=CTR, stroke_color=ORANGE, stroke_width=SW).move_to(CTR)
        ring_l = term("plasmid", 38, ORANGE).move_to(CTR + UP * 2.8)
        sub = T("usually circular", 26, GREY).next_to(ring_l, RIGHT, buff=0.3)
        self.at("A plasmid")
        self.play(gene.animate.scale(0.5).move_to([-1.0, -2.9, 0]), Create(ring), FadeIn(ring_l), FadeIn(gene_l), run_time=1.0)
        self.at("usually circular")
        self.play(FadeIn(sub), run_time=0.4)

        # main chromosome and the copy
        chrom = bars(-6.2, -3.4, 0.5, GREY, h=0.3, gap=0.06)
        chrom_l = T("main chromosome", 26, GREY).next_to(chrom, UP, buff=0.25)
        ring2 = ring.copy().scale(0.6).move_to(CTR + RIGHT * 4.4)
        self.at("copies itself")
        self.play(FadeIn(chrom), FadeIn(chrom_l), TransformFromCopy(ring, ring2), run_time=1.0)
        copy_l = T("a copy", 26, ORANGE).next_to(ring2, DOWN, buff=0.2)
        self.play(FadeIn(copy_l), run_time=0.3)

        # cut open with the same enzyme
        self.at("Cut it open")
        enz = chip("restriction enzyme", PURPLE, 28).move_to([-3.4, 3.0, 0])
        self.play(FadeOut(VGroup(chrom, chrom_l, ring2, copy_l, sub, ring_l)), FadeIn(enz, shift=DOWN * 0.2), run_time=0.6)
        self.play(enz.animate.move_to([-1.9, 2.95, 0]), run_time=0.4)
        open_arc = ring_arc(CTR, R_, 125, 290, ORANGE)
        gene_arc = ring_arc(CTR, R_, 55, 70, YELLOW)

        def end_sq(p):
            return Square(0.28, stroke_width=0, fill_color=TEAL, fill_opacity=1).move_to(p)
        e1, e2 = end_sq(open_arc.get_start()), end_sq(open_arc.get_end())
        self.at("same enzyme")
        self.play(ReplacementTransform(ring, open_arc), Flash(CTR + UP * R_, color=PURPLE, flash_radius=0.8), run_time=0.7)
        self.play(FadeIn(e1), FadeIn(e2), FadeOut(enz), run_time=0.5)

        # the gene piece moves into the gap
        g_up = gene_arc.copy().shift(UP * 0.8)
        g1, g2 = end_sq(g_up.get_start()), end_sq(g_up.get_end())
        self.at("the sticky ends match")
        self.play(FadeOut(gene, shift=UP * 0.6), FadeOut(gene_l), FadeIn(g_up), FadeIn(g1), FadeIn(g2), run_time=0.9)
        self.play(g_up.animate.shift(DOWN * 0.8), g1.animate.shift(DOWN * 0.8), g2.animate.shift(DOWN * 0.8), run_time=0.8)
        pair = T("ends pair", 30, TEAL).move_to(CTR)
        self.play(FadeIn(pair), Indicate(VGroup(e1, e2, g1, g2), color=TEAL, scale_factor=1.5), run_time=0.7)

        # ligase seals
        self.at("DNA ligase")
        lig = chip("DNA ligase", GREEN, 32).move_to([3.6, 2.9, 0])
        self.play(FadeIn(lig, shift=DOWN * 0.2), FadeOut(pair), run_time=0.5)
        self.at("joins two DNA ends")
        self.play(lig.animate.move_to([1.9, 2.9, 0]), run_time=0.5)
        self.play(Flash(e1.get_center(), color=GREEN, flash_radius=0.5), Flash(e2.get_center(), color=GREEN, flash_radius=0.5),
                  FadeOut(VGroup(e1, e2, g1, g2)), run_time=0.6)
        join_l = T("one strand", 30, GREEN).move_to(CTR)
        self.play(FadeIn(join_l), run_time=0.4)

        # recombinant DNA
        self.at("recombinant DNA")
        self.play(FadeOut(lig), FadeOut(join_l), run_time=0.4)
        rec = term("recombinant DNA", 48).move_to([0, -2.3, 0])
        self.play(FadeIn(rec, shift=UP * 0.15), run_time=0.6)
        self.at("from more than one source")
        lab_h = T("human gene", 30, YELLOW).move_to(CTR + RIGHT * 4.0 + UP * 1.3)
        lab_p = T("bacterial plasmid", 30, ORANGE).move_to(CTR + LEFT * 4.2 + DOWN * 0.3)
        ah = arr(lab_h.get_left(), CTR + np.array([R_ * np.cos(np.radians(55)), R_ * np.sin(np.radians(55)), 0]) + RIGHT * 0.12, YELLOW)
        ap = arr(lab_p.get_right(), CTR + np.array([-R_, 0, 0]) + LEFT * 0.12, ORANGE)
        self.play(FadeIn(lab_h), GrowArrow(ah), FadeIn(lab_p), GrowArrow(ap), run_time=0.8)
        self.finish()


# ---------------------------------------------------------------------------------------------
class S04Bacteria(SpokenScene):
    """plasmids into some bacteria -> antibiotic leaves those -> they divide, plasmid copied -> insulin chains join."""

    def construct(self):
        xs = [-5.2, -2.6, 0.0, 2.6, 5.2]
        cells = [cell([x, 0.9, 0], w=2.2, h=1.7) for x in xs]
        bl = T("bacteria", 30, GREY).move_to([0, -0.4, 0])
        self.at("Put the plasmids")
        pl_l = T("recombinant plasmids", 30, ORANGE).move_to([0, 3.3, 0])
        pls = [rec_ring([xs[i], 2.3, 0], 0.36) for i in (1, 3)]
        self.play(FadeIn(pl_l), *[FadeIn(p) for p in pls], run_time=0.6)
        self.at("into bacteria")
        self.play(LaggedStart(*[FadeIn(c, scale=0.9) for c in cells], lag_ratio=0.1), FadeIn(bl), run_time=0.9)
        self.at("take one up")
        self.play(*[p.animate.move_to([xs[i], 0.9, 0]) for p, i in zip(pls, (1, 3))], run_time=0.9)
        only = T("only some take one up", 32, GREY).move_to([0, -1.5, 0])
        self.play(FadeOut(pl_l), FadeIn(only), run_time=0.4)

        # antibiotic
        self.at("antibiotic")
        abx = chip("antibiotic", RED, 34).move_to([0, 3.0, 0])
        self.play(FadeOut(only), FadeIn(abx, shift=DOWN * 0.2), run_time=0.5)
        self.at("leaves mostly the ones")
        dead = [cells[0], cells[2], cells[4]]
        keep = T("leaves mostly the ones that took it", 32, GREEN).move_to([0, -1.5, 0])
        nop = VGroup(*[T("no plasmid", 24, RED).move_to([c.get_center()[0], -0.25, 0]) for c in dead])
        self.play(FadeOut(bl), FadeIn(nop), *[c.animate.set_stroke(RED, opacity=0.9).set_fill(RED, 0.15) for c in dead], FadeIn(keep),
                  *[cells[i].animate.set_stroke(GREEN) for i in (1, 3)], run_time=0.8)

        # divide
        self.at("As they divide")
        surv = VGroup(cells[1], pls[0])
        self.play(FadeOut(VGroup(*dead, abx, keep, nop, cells[3], pls[1])), surv.animate.scale(1.1).move_to([-3.4, 0.4, 0]), run_time=0.8)
        daughter = surv.copy()
        self.add(daughter)
        self.play(surv.animate.shift(LEFT * 1.35), daughter.animate.shift(RIGHT * 1.35), run_time=0.8)
        cp_l = T("plasmid copied,\ngene and all", 30, ORANGE, line_spacing=0.8).move_to([-3.4, -1.4, 0])
        self.at("plasmid is copied")
        self.play(FadeIn(cp_l), Indicate(daughter[1], color=ORANGE, scale_factor=1.5), Indicate(surv[1], color=ORANGE, scale_factor=1.5), run_time=0.7)

        # insulin chains
        ch1 = chip("insulin chain", YELLOW, 30).move_to([1.6, 1.6, 0])
        ch2 = chip("insulin chain", YELLOW, 30).move_to([1.6, -0.8, 0])
        a1 = arr(daughter[0].get_right(), ch1.get_left(), YELLOW)
        a2 = arr(daughter[0].get_right(), ch2.get_left(), YELLOW)
        self.at("If the gene is switched on")
        self.play(GrowArrow(a1), GrowArrow(a2), FadeIn(ch1, shift=RIGHT * 0.2), FadeIn(ch2, shift=RIGHT * 0.2), run_time=0.8)
        self.at("cut free")
        ins = chip("insulin", YELLOW, 42).move_to([5.2, 0.4, 0])
        a3 = arr(ch1.get_right(), ins.get_left() + UP * 0.15, YELLOW)
        a4 = arr(ch2.get_right(), ins.get_left() + DOWN * 0.15, YELLOW)
        step = T("cut free and purified", 28, GREY).move_to([4.9, -1.6, 0])
        self.play(FadeIn(step), run_time=0.4)
        self.at("and joined")
        self.play(GrowArrow(a3), GrowArrow(a4), FadeIn(ins, scale=0.9), run_time=0.8)
        note = T("a simplified model, not a factory recipe", 26, GREY).move_to([0, -3.2, 0])
        self.play(FadeIn(note), run_time=0.4)
        self.finish()


# ---------------------------------------------------------------------------------------------
class S05Tools(SpokenScene):
    """PCR doubling plot (ideal) -> gel with short pieces running farther -> CRISPR guide RNA and Cas9 cut."""

    def construct(self):
        # --- PCR ---
        title = term("polymerase chain reaction (PCR)", 36).move_to([0, 3.3, 0])
        ox, oy, W, H = -6.0, -3.0, 7.8, 5.2
        xax = Line([ox, oy, 0], [ox + W + 0.2, oy, 0], color=GREY, stroke_width=3)
        yax = Line([ox, oy, 0], [ox, oy + H + 0.2, 0], color=GREY, stroke_width=3)
        xl = T("cycles (ideal reaction)", 26, GREY).move_to([ox + W / 2, oy - 0.7, 0])
        yl = T("copies of the chosen stretch", 26, GREY).rotate(PI / 2).move_to([ox - 0.6, oy + H / 2, 0])
        ticks = VGroup(*[M(str(n), 22, GREY).move_to([ox + n * W / 10, oy - 0.3, 0]) for n in (0, 2, 4, 6, 8, 10)])
        pts = [np.array([ox + n * W / 10, oy + (2 ** n) / 1024 * H, 0]) for n in range(11)]
        self.at("polymerase chain reaction")
        self.play(FadeIn(title, shift=DOWN * 0.1), Create(xax), Create(yax), FadeIn(xl), FadeIn(yl), FadeIn(ticks), run_time=0.9)
        self.at("many copies")
        d0 = Dot(pts[0], radius=0.12, color=YELLOW)
        one = M("1 copy", 26, YELLOW).next_to(d0, UP, buff=0.3).shift(RIGHT * 0.5)
        self.play(FadeIn(d0, scale=1.5), FadeIn(one), run_time=0.4)
        self.at("doubles each cycle")
        dots = [Dot(p, radius=0.1, color=YELLOW) for p in pts[1:]]
        curve = VMobject(color=YELLOW, stroke_width=6)
        xs_ = np.linspace(0, 10, 80)
        curve.set_points_smoothly([np.array([ox + x * W / 10, oy + (2 ** x) / 1024 * H, 0]) for x in xs_])
        dbl = T("doubles each cycle", 34, TEAL, weight=BOLD).move_to([4.2, 0.8, 0])
        ten = M("1,024 copies", 28, YELLOW).move_to([4.2, -0.3, 0])
        ten2 = T("after 10 ideal cycles", 26, GREY).next_to(ten, DOWN, buff=0.15)
        self.play(Create(curve), LaggedStart(*[FadeIn(d, scale=1.4) for d in dots], lag_ratio=0.08), FadeIn(dbl), run_time=1.4)
        self.play(FadeIn(ten), FadeIn(ten2), run_time=0.3)

        # --- gel ---
        self.at("Gel electrophoresis")
        pcr = VGroup(title, xax, yax, xl, yl, ticks, d0, one, curve, *dots, ten, ten2, dbl)
        gt = term("gel electrophoresis", 36).move_to([0, 3.3, 0])
        gel = Rectangle(width=6.4, height=5.2, stroke_color=GREY, stroke_width=4, fill_color=GREY, fill_opacity=0.12).move_to([-2.8, -0.5, 0])
        top = gel.get_top()[1]
        lane_x = [-4.6, -2.8, -1.0]
        wells = VGroup(*[Rectangle(width=1.0, height=0.28, stroke_color=GREY, stroke_width=3, fill_color=BG, fill_opacity=1).move_to([x, top - 0.25, 0]) for x in lane_x])
        neg = T("- negative end", 26, GREY).move_to([3.3, top - 0.2, 0])
        pos = T("+ positive end", 26, GREY).move_to([3.3, -3.0, 0])
        wy = top - 0.25
        ladder = VGroup(*[seg(lane_x[0] - 0.4, lane_x[0] + 0.4, wy, GREY, 0.16) for _ in range(4)])
        short = seg(lane_x[1] - 0.4, lane_x[1] + 0.4, wy, TEXT, 0.2)
        long_ = seg(lane_x[2] - 0.4, lane_x[2] + 0.4, wy, TEXT, 0.2)
        ll = T("known sizes", 26, GREY).move_to([lane_x[0], top + 0.35, 0])
        sl = T("short", 26, TEXT).move_to([lane_x[1], top + 0.35, 0])
        gl = T("long", 26, TEXT).move_to([lane_x[2], top + 0.35, 0])
        cur = arr([1.1, top - 0.5, 0], [1.1, -2.7, 0], TEAL)
        cur_l = T("electric current", 26, TEAL).move_to([3.2, -0.5, 0])
        self.play(FadeOut(pcr), FadeIn(gt, shift=DOWN * 0.1), FadeIn(gel), FadeIn(wells), FadeIn(neg), FadeIn(pos),
                  FadeIn(ladder), FadeIn(short), FadeIn(long_), FadeIn(ll), FadeIn(sl), FadeIn(gl), run_time=0.9)
        self.at("sorts DNA pieces by size")
        self.play(GrowArrow(cur), FadeIn(cur_l), run_time=0.4)
        self.at("Shorter pieces")
        ladder_y = [wy - 0.9, wy - 1.8, wy - 2.7, wy - 3.6]
        self.play(*[b.animate.move_to([lane_x[0], y, 0]) for b, y in zip(ladder, ladder_y)],
                  short.animate.move_to([lane_x[1], wy - 3.5, 0]), long_.animate.move_to([lane_x[2], wy - 1.2, 0]), run_time=1.2)
        fl = T("farther", 28, TEAL, weight=BOLD).move_to([lane_x[1], wy - 3.5 - 0.5, 0])
        nl = T("near the wells", 26, GREY).move_to([lane_x[2] - 0.6, wy - 1.2 - 0.45, 0])
        fl.shift(RIGHT * 0.0); nl.shift(RIGHT * 0.0)
        self.at("travel farther")
        self.play(FadeIn(fl), FadeIn(nl), run_time=0.5)

        # --- CRISPR ---
        self.at("CRISPR")
        gelg = VGroup(gt, gel, wells, neg, pos, ladder, short, long_, ll, sl, gl, cur, cur_l, fl, nl)
        ct = term("CRISPR", 38).move_to([0, 3.3, 0])
        dnaL = bars(-5.5, 0.0, -1.2, GREY, h=0.4, gap=0.07)
        dnaR = bars(0.0, 5.5, -1.2, GREY, h=0.4, gap=0.07)
        tgt = RoundedRectangle(corner_radius=0.08, width=1.5, height=1.3, stroke_color=TEAL, stroke_width=4).move_to([0, -1.2, 0])
        tgt_l = T("one sequence", 28, TEAL).move_to([0, -2.5, 0])
        guide = chip("guide RNA", BLUE, 36).move_to([-3.6, 1.6, 0])
        cas = chip("Cas9", PURPLE, 36).move_to([0, 2.4, 0])
        self.play(FadeOut(gelg), FadeIn(ct, shift=DOWN * 0.1), FadeIn(dnaL), FadeIn(dnaR), run_time=0.7)
        self.at("a guide")
        self.play(FadeIn(guide, shift=RIGHT * 0.2), run_time=0.5)
        self.at("matches one sequence")
        self.play(FadeIn(tgt), FadeIn(tgt_l), guide.animate.move_to([0, 0.2, 0]), run_time=0.8)
        self.at("a protein called")
        self.play(FadeIn(cas, shift=DOWN * 0.2), cas.animate.move_to([0, 1.3, 0]), run_time=0.6)
        self.at("cuts both strands")
        self.play(Flash(np.array([0, -1.2, 0]), color=PURPLE, flash_radius=0.9),
                  dnaL.animate.shift(LEFT * 0.4), dnaR.animate.shift(RIGHT * 0.4), FadeOut(tgt), run_time=0.7)
        cut_l = T("both strands cut", 32, PURPLE).move_to([0, -2.5, 0])
        self.play(FadeOut(tgt_l), FadeIn(cut_l), run_time=0.4)
        self.finish()


# ---------------------------------------------------------------------------------------------
class S06Answer(SpokenScene):
    """the question returns; the tool chain; crops and blood stem cells; evidence and values."""

    def construct(self):
        q1 = T("Can we design life,", 40, GOLD, font=TITLE_FONT)
        q2 = T("and how should we decide when we should?", 36, TEXT, font=TITLE_FONT)
        q = VGroup(q1, q2).arrange(DOWN, buff=0.2).move_to([0, 2.9, 0])
        self.at("So can we design life")
        self.play(FadeIn(q, shift=DOWN * 0.1), run_time=0.7)

        names = [("enzyme cuts", PURPLE), ("ligase joins", GREEN), ("plasmid copies", ORANGE), ("gene read", YELLOW)]
        xs = [-5.0, -1.7, 1.6, 4.8]
        chips = [chip(n, c, 30).move_to([x, 0.0, 0]) for (n, c), x in zip(names, xs)]
        arrows = [arr(chips[i].get_right(), chips[i + 1].get_left(), GREY, w=4) for i in range(3)]
        self.at("change DNA")
        self.play(FadeIn(chips[0], shift=UP * 0.1), run_time=0.4)
        self.play(GrowArrow(arrows[0]), FadeIn(chips[1], shift=UP * 0.1), run_time=0.5)
        self.at("copy a plasmid")
        self.play(GrowArrow(arrows[1]), FadeIn(chips[2], shift=UP * 0.1), run_time=0.5)
        self.at("read the human gene")
        self.play(GrowArrow(arrows[2]), FadeIn(chips[3], shift=UP * 0.1), run_time=0.5)
        ins = chip("human insulin", YELLOW, 34).move_to([4.5, -1.8, 0])
        ar_i = arr(chips[3].get_bottom(), ins.get_top(), YELLOW)
        self.play(GrowArrow(ar_i), FadeIn(ins, shift=UP * 0.1), run_time=0.5)

        self.at("Related tools")
        self.play(FadeOut(VGroup(ins, ar_i)), run_time=0.3)
        crops = T("crops", 36, TEAL).move_to([-3.4, -1.7, 0])
        stem = T("CRISPR: blood stem cells", 36, TEAL).move_to([1.2, -1.7, 0])
        self.at("change crops")
        self.play(FadeIn(crops, shift=UP * 0.1), run_time=0.4)
        self.at("blood stem cells")
        self.play(FadeIn(stem, shift=UP * 0.1), run_time=0.4)

        self.at("Whether a change")
        self.play(FadeOut(VGroup(*chips, *arrows, crops, stem)), run_time=0.5)
        ev = chip("evidence", TEAL, 44).move_to([-3.2, 0.3, 0])
        va = chip("values", GOLD, 44).move_to([3.2, 0.3, 0])
        plus = T("and", 36, GREY).move_to([0, 0.3, 0])
        self.at("judged use by use")
        self.play(FadeIn(ev, shift=UP * 0.1), FadeIn(plus), FadeIn(va, shift=UP * 0.1), run_time=0.6)
        items = VGroup(T("safety", 34, GOLD), T("fair access", 34, GOLD), T("limits", 34, GOLD)).arrange(DOWN, buff=0.25, aligned_edge=LEFT)
        items.next_to(va, DOWN, buff=0.5)
        self.at("such as safety")
        self.play(FadeIn(items[0], shift=UP * 0.1), run_time=0.4)
        self.at("fair access")
        self.play(FadeIn(items[1], shift=UP * 0.1), run_time=0.4)
        self.at("and limits")
        self.play(FadeIn(items[2], shift=UP * 0.1), run_time=0.4)
        self.finish()


class S07End(EndCard):
    LINE = "Judge each use by its evidence and its values."
