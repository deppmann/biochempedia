"""Meiosis and Variation: Meiosis halves and shuffles chromosomes  (Biochemistrypedia explainer)

COLOR MAP (one color per concept, whole video)
  BLUE   = a chromosome that came from the mother (in the model cell)
  ORANGE = a chromosome that came from the father (in the model cell)
  GREY   = a body (diploid) cell outline, labels, de-emphasized
  GREEN  = a haploid cell / sex cell (gamete) outline
  TEAL   = a vocabulary term label, shown the moment it is spoken
  PINK   = chromosomes in an egg, PURPLE = chromosomes in a sperm (last scene only)
  YELLOW = the count of combinations, and what is highlighted
Chromosomes are drawn only as labelled bars. No molecules, no helix.
Model cell: 3 pairs (the real human number is 23).
"""
import numpy as np
from bp_style import *  # noqa: F401,F403

DAD = "#F29E4C"
MOM = BLUE
EGGC = ["#F4A3C8", "#D0457F"]   # the egg's chromosomes (pink family; two shades keep pairs apart)
SPC = ["#C6B3F5", "#7B4FD6"]    # the sperm's chromosomes (purple family)
PH = [1.5, 1.1, 0.8]      # bar height of pair 1, 2, 3 (so the pairs can be told apart)
XP = [-1.2, 0.0, 1.2]     # x of each pair inside the big cell


def rbar(color, h, w=0.26, fo=0.55):
    return RoundedRectangle(corner_radius=min(0.08, w / 2.5), width=w, height=h, stroke_color=color,
                            stroke_width=2.5, fill_color=color, fill_opacity=fo)


def dbl(color, h):
    """a copied chromosome: two identical copies (sister chromatids) joined side by side."""
    return VGroup(rbar(color, h, 0.13), rbar(color, h, 0.13)).arrange(RIGHT, buff=0.02)


def cellc(center, r, color=GREY):
    return Circle(radius=r, stroke_color=color, stroke_width=4, fill_color=color, fill_opacity=0.08).move_to(center)


def term(text, size=26):
    return chip(text, TEAL, size=size)


def banner(text, size=28, y=-3.05):
    return T(text, size, TEXT).move_to([0, y, 0])


def arr(a, b, color=GREY, w=5):
    return Arrow(a, b, buff=0.05, color=color, stroke_width=w, tip_length=0.2,
                 max_tip_length_to_length_ratio=0.45, max_stroke_width_to_length_ratio=12)


def P(x, y):
    return np.array([x, y, 0.0])


class S00Title(TitleCard):
    LESSON = "Meiosis and Variation"
    TITLE = "Meiosis halves and shuffles chromosomes"


# ---------------------------------------------------------------------------------------------
class S01Question(SpokenScene):
    """The puzzle: same two parents, children who are not the same."""

    def construct(self):
        mother = chip("mother", MOM, 30).move_to(P(-2.6, 2.6))
        father = chip("father", DAD, 30).move_to(P(2.6, 2.6))
        self.at("Why don't siblings")
        self.play(FadeIn(mother, shift=DOWN * 0.2), FadeIn(father, shift=DOWN * 0.2), run_time=0.7)
        kids, ars = [], []
        for k, x in enumerate([-4.2, 0.0, 4.2]):
            box = RoundedRectangle(corner_radius=0.2, width=3.4, height=2.4, stroke_color=GREY, stroke_width=3,
                                   fill_color=GREY, fill_opacity=0.08).move_to(P(x, -0.6))
            half1 = Rectangle(width=1.2, height=0.9, stroke_width=0, fill_color=MOM, fill_opacity=0.6)
            half2 = Rectangle(width=1.2, height=0.9, stroke_width=0, fill_color=DAD, fill_opacity=0.6)
            bar_ = VGroup(half1, half2).arrange(RIGHT, buff=0).move_to(box.get_center() + UP * 0.4)
            lab = T(f"child {k + 1}", 26, TEXT).move_to(box.get_center() + DOWN * 0.55)
            kids.append(VGroup(box, bar_, lab))
        self.at("exactly alike")
        self.play(*[FadeIn(k, shift=UP * 0.2) for k in kids], run_time=0.9)
        for k, x in zip(kids, [-4.2, 0.0, 4.2]):
            if x < 0:
                ars.append(arr(P(-3.0, 2.15), k[0].get_top() + UP * 0.05, MOM))
            elif x > 0:
                ars.append(arr(P(3.0, 2.15), k[0].get_top() + UP * 0.05, DAD))
            else:
                ars.append(arr(P(-2.4, 2.15), k[0].get_top() + P(-0.3, 0.05), MOM))
                ars.append(arr(P(2.4, 2.15), k[0].get_top() + P(0.3, 0.05), DAD))
        self.at("same two parents")
        self.play(*[GrowArrow(a) for a in ars], run_time=0.8)
        self.at("half of their chromosomes")
        half_t = T("half from each parent", 30, YELLOW).move_to(P(0, -2.6))
        self.play(FadeIn(half_t, shift=UP * 0.15), run_time=0.6)
        self.at("almost never")
        qs = [T("?", 64, YELLOW, weight=BOLD).move_to(k[0].get_corner(UR) + P(-0.3, -0.15)) for k in kids]
        diff = T("not the same mix", 30, RED).move_to(P(0, -2.6))
        self.play(FadeOut(half_t), FadeIn(diff), *[FadeIn(q, scale=1.4) for q in qs], run_time=0.8)
        self.at("how eggs and sperm")
        egg = chip("egg", GREEN, 28).move_to(P(-2.6, 1.55))
        sperm = chip("sperm", GREEN, 28).move_to(P(2.6, 1.55))
        self.play(FadeOut(diff), FadeOut(VGroup(*ars)),
                  FadeIn(egg, shift=DOWN * 0.3), FadeIn(sperm, shift=DOWN * 0.3), run_time=0.9)
        hint = T("how are they made?", 36, YELLOW).move_to(P(0, -2.6))
        self.play(FadeIn(hint, shift=UP * 0.15), run_time=0.6)
        self.finish()


# ---------------------------------------------------------------------------------------------
class S02Sets(SpokenScene):
    """A model diploid cell (3 pairs), then a haploid gamete."""

    def construct(self):
        CY = 0.4
        cell = cellc(P(0, CY), 2.3)
        bars = []
        for i in range(3):
            b = rbar(MOM, PH[i]).move_to(P(XP[i] - 0.2, CY))
            o = rbar(DAD, PH[i]).move_to(P(XP[i] + 0.2, CY))
            bars += [b, o]
        self.at("Most human body cells")
        self.play(FadeIn(cell), *[FadeIn(b, scale=0.8) for b in bars], run_time=0.8)
        lab46 = T("46 chromosomes in 23 pairs", 28, TEXT).move_to(P(0, 3.2))
        note = T("model cell: 3 pairs shown, not 23", 22, GREY).move_to(P(0, -3.3))
        self.at("46 chromosomes")
        self.play(FadeIn(lab46, shift=DOWN * 0.1), FadeIn(note), run_time=0.6)
        self.at("from your mother")
        leg_m = chip("from mother", MOM, 22).move_to(P(-1.5, -2.55))
        self.play(FadeIn(leg_m), *[Indicate(bars[k], color=MOM, scale_factor=1.12) for k in (0, 2, 4)], run_time=0.8)
        self.at("from your father")
        leg_f = chip("from father", DAD, 22).move_to(P(1.5, -2.55))
        self.play(FadeIn(leg_f), *[Indicate(bars[k], color=DAD, scale_factor=1.12) for k in (1, 3, 5)], run_time=0.8)
        self.at("diploid")
        dip = term("diploid: two sets", 26).move_to(P(0, -2.55))
        self.play(FadeOut(VGroup(leg_m, leg_f)), FadeIn(dip, shift=UP * 0.1), run_time=0.5)
        gcell = cellc(P(4.0, CY), 1.5, GREEN)
        gbars = []
        for k, (col, i) in enumerate([(MOM, 0), (DAD, 1), (MOM, 2)]):
            gbars.append(rbar(col, PH[i] * 0.8).move_to(P(4.0 + [-0.6, 0.0, 0.6][k], CY)))
        self.at("haploid")
        hap = term("haploid: one set", 26).move_to(P(4.0, -1.75))
        leg_m2 = chip("from mother", MOM, 22).move_to(P(2.6, 3.2))
        leg_f2 = chip("from father", DAD, 22).move_to(P(5.0, 3.2))
        self.play(VGroup(cell, *bars, lab46, dip).animate.shift(LEFT * 3.2), run_time=0.7)
        self.play(FadeIn(gcell, scale=0.8), *[FadeIn(b, scale=0.8) for b in gbars], FadeIn(hap, shift=UP * 0.1),
                  FadeIn(leg_m2), FadeIn(leg_f2), run_time=0.9)
        self.at("a gamete")
        gam = term("gamete: egg or sperm", 26).move_to(P(4.0, 2.35))
        self.play(FadeIn(gam, shift=DOWN * 0.1), run_time=0.6)
        self.at("23 chromosomes")
        n23 = T("23 chromosomes", 28, YELLOW).move_to(P(4.0, -2.55))
        self.play(FadeIn(n23, shift=UP * 0.1), run_time=0.6)
        self.finish()


# ---------------------------------------------------------------------------------------------
class S03Divide(SpokenScene):
    """Copy once, divide twice: pairs apart, then copies apart -> four cells."""

    def construct(self):
        CY = 0.4
        # carried over from the last scene
        cell = cellc(P(-3.2, CY), 2.3)
        ob, oo = [], []
        for i in range(3):
            ob.append(rbar(MOM, PH[i]).move_to(P(-3.2 + XP[i] - 0.2, CY)))
            oo.append(rbar(DAD, PH[i]).move_to(P(-3.2 + XP[i] + 0.2, CY)))
        gcell = cellc(P(4.0, CY), 1.5, GREEN)
        gb = [rbar(c, PH[i] * 0.8).move_to(P(4.0 + [-0.6, 0.0, 0.6][k], CY))
              for k, (c, i) in enumerate([(MOM, 0), (DAD, 1), (MOM, 2)])]
        self.add(cell, *ob, *oo, gcell, *gb)
        main = VGroup(cell, *ob, *oo)
        self.at("Meiosis")
        title = T("Meiosis", 40, TEXT, font=TITLE_FONT).move_to(P(0, 3.15))
        self.play(FadeOut(VGroup(gcell, *gb)), main.animate.shift(RIGHT * 3.2), FadeIn(title), run_time=0.9)
        self.at("diploid cell")
        dip = term("diploid", 26).move_to(P(0, -2.55))
        self.play(FadeIn(dip, shift=UP * 0.1), run_time=0.5)
        # --- copy -----------------------------------------------------------------------
        self.at("copies its")
        b1 = banner("1 · The DNA is copied once")
        dB = [dbl(MOM, PH[i]).move_to(ob[i]) for i in range(3)]
        dO = [dbl(DAD, PH[i]).move_to(oo[i]) for i in range(3)]
        self.play(FadeOut(dip), FadeIn(b1, shift=UP * 0.1),
                  *[ReplacementTransform(ob[i], dB[i]) for i in range(3)],
                  *[ReplacementTransform(oo[i], dO[i]) for i in range(3)], run_time=1.0)
        self.at("sister chromatids")
        sc = term("sister chromatids", 26).move_to(P(4.3, 1.7))
        pt = arr(P(sc.get_left()[0], 1.6), dO[2].get_right() + P(0.05, 0.25), TEAL)
        self.play(FadeIn(sc, shift=LEFT * 0.2), GrowArrow(pt), Indicate(dO[2], color=TEAL, scale_factor=1.25),
                  run_time=0.9)
        # --- divides twice ------------------------------------------------------------------
        self.at("divides twice")
        b2 = banner("2 · The cell divides twice")
        self.play(FadeOut(VGroup(sc, pt)), ReplacementTransform(b1, b2), run_time=0.6)
        # --- first division -------------------------------------------------------------------
        self.at("the first division")
        b3 = banner("First division: the pairs are pulled apart")
        self.play(ReplacementTransform(b2, b3), run_time=0.5)
        left_set = [(dB[0], 0), (dO[1], 1), (dB[2], 2)]
        right_set = [(dO[0], 0), (dB[1], 1), (dO[2], 2)]
        cr = cell.copy()
        self.add(cr)
        self.at("pulled apart")
        k = 0.674
        L, R = P(-3.1, CY), P(3.1, CY)
        anims = [cell.animate.scale(k).move_to(L), cr.animate.scale(k).move_to(R)]
        for j, (d, i) in enumerate(left_set):
            anims.append(d.animate.scale(0.8).move_to(P(L[0] + [-0.6, 0.0, 0.6][j], CY)))
        for j, (d, i) in enumerate(right_set):
            anims.append(d.animate.scale(0.8).move_to(P(R[0] + [-0.6, 0.0, 0.6][j], CY)))
        self.play(*anims, run_time=1.3)
        # --- second division ------------------------------------------------------------------
        self.at("In the second")
        b4 = banner("Second division: the copies are pulled apart")
        self.play(ReplacementTransform(b3, b4), run_time=0.5)
        cl2, cr2 = cell.copy(), cr.copy()
        self.add(cl2, cr2)
        self.at("sister chromatids", nth=1)
        k2 = 1.2 / 1.55
        cents = [(-4.5, cell, left_set, -3.1), (-1.5, cl2, left_set, -3.1), (1.5, cr, right_set, 3.1), (4.5, cr2, right_set, 3.1)]
        anims = [cell.animate.scale(k2).move_to(P(-4.5, CY)), cl2.animate.scale(k2).move_to(P(-1.5, CY)),
                 cr.animate.scale(k2).move_to(P(1.5, CY)), cr2.animate.scale(k2).move_to(P(4.5, CY))]
        for (sset, c1, c2) in [(left_set, -4.5, -1.5), (right_set, 1.5, 4.5)]:
            for j, (d, i) in enumerate(sset):
                col = MOM if d in dB else DAD
                s1 = rbar(col, PH[i] * 0.7, 0.2).move_to(P(c1 + [-0.5, 0.0, 0.5][j], CY))
                s2 = rbar(col, PH[i] * 0.7, 0.2).move_to(P(c2 + [-0.5, 0.0, 0.5][j], CY))
                anims += [Transform(d[0], s1), Transform(d[1], s2)]
        self.play(*anims, run_time=1.8)
        self.at("four cells form")
        for c in (cell, cl2, cr, cr2):
            pass
        res = term("4 haploid cells", 28).move_to(P(0, -1.75))
        n3 = T("3 chromosomes each (model cell)", 24, GREY).move_to(P(0, -2.4))
        self.play(FadeOut(b4),
                  *[c.animate.set_stroke(GREEN) for c in (cell, cl2, cr, cr2)],
                  FadeIn(res, shift=UP * 0.1), FadeIn(n3), run_time=1.0)
        self.finish()


# ---------------------------------------------------------------------------------------------
class S04Cross(SpokenScene):
    """Way one: crossing over swaps matching pieces between the two chromosomes of a pair."""

    def construct(self):
        W, HP = 0.7, 2.2
        TOPY, BOTY = 1.3, -0.9

        def piece(color, y, letter, x):
            r = Rectangle(width=W, height=HP, stroke_color=color, stroke_width=3, fill_color=color, fill_opacity=0.5)
            band = Rectangle(width=W, height=0.34, stroke_width=0, fill_color=TEXT, fill_opacity=0.9)
            ltr = T(letter, 24, BG, weight=BOLD)
            g = VGroup(r, band, ltr)
            band.move_to(r), ltr.move_to(band)
            g.move_to(P(x, y))
            return g

        XB, XO = 1.0, 5.2
        bt, bb = piece(MOM, TOPY, "A", XB), piece(MOM, BOTY, "B", XB)
        ot, ob_ = piece(DAD, TOPY, "a", XO), piece(DAD, BOTY, "b", XO)
        self.at("Meiosis mixes")
        self.play(*[FadeIn(m, scale=0.9) for m in (bt, bb, ot, ob_)], run_time=0.8)
        leg1 = chip("blue: from your mother", MOM, 22).move_to(P(-3.4, -2.0))
        leg2 = chip("orange: from your father", DAD, 22).move_to(P(-3.4, -2.8))
        self.play(FadeIn(leg1), FadeIn(leg2), run_time=0.5)
        self.at("allele is")
        al = T("A and a: two versions", 28, TEXT).move_to(P(-3.4, 1.65))
        al2 = T("(alleles) of one gene", 28, TEXT).move_to(P(-3.4, 1.15))
        self.play(FadeIn(al), FadeIn(al2), Indicate(bt[1], color=YELLOW, scale_factor=1.3),
                  Indicate(ot[1], color=YELLOW, scale_factor=1.3), run_time=1.0)
        self.at("crossing over")
        chip1 = term("crossing over", 30).move_to(P(-3.4, 2.85))
        self.play(FadeIn(chip1, shift=DOWN * 0.1), run_time=0.5)
        self.at("side by side")
        self.play(VGroup(bt, bb).animate.shift(RIGHT * 2.0), VGroup(ot, ob_).animate.shift(LEFT * 1.2), run_time=1.0)
        self.at("swap matching pieces")
        self.play(CyclicReplace(bb, ob_, path_arc=PI * 0.6), run_time=1.4)
        self.at("alleles from both")
        txt = T("one chromosome now has", 26, TEXT).move_to(P(-3.4, -0.35))
        txt2 = T("pieces from both parents", 26, YELLOW).move_to(P(-3.4, -0.8))
        a = arr(P(-1.05, -0.55), P(2.5, -0.55), YELLOW)
        self.play(FadeIn(txt), FadeIn(txt2), GrowArrow(a), run_time=0.9)
        self.finish()


# ---------------------------------------------------------------------------------------------
class S05Shuffle(SpokenScene):
    """Way two: independent assortment. Each pair doubles the combinations: 2 x 2 x 2 = 8; 23 pairs = 2^23."""

    def construct(self):
        H5 = [1.25, 0.9, 0.6]
        PX = [-3.5, 0.0, 3.5]
        pairs = VGroup()
        pb, po, plabs = [], [], []
        for i in range(3):
            b = rbar(MOM, H5[i] + 0.2).move_to(P(PX[i] - 0.25, 1.9))
            o = rbar(DAD, H5[i] + 0.2).move_to(P(PX[i] + 0.25, 1.9))
            lab = T(f"pair {i + 1}", 24, GREY).move_to(P(PX[i], 0.95))
            pb.append(b), po.append(o), plabs.append(lab)
            pairs.add(b, o, lab)
        self.at("The second way")
        self.play(FadeIn(pairs, shift=DOWN * 0.15), run_time=0.8)
        self.at("independent assortment")
        head = term("independent assortment", 30).move_to(P(0, 3.15))
        self.play(FadeIn(head, shift=DOWN * 0.1), run_time=0.5)

        def gam(choices, x, y=-0.65):
            box = RoundedRectangle(corner_radius=0.15, width=1.4, height=1.8, stroke_color=GREEN, stroke_width=3,
                                   fill_color=GREEN, fill_opacity=0.08).move_to(P(x, y))
            g = VGroup(box)
            for j, c in enumerate(choices):
                col = MOM if c == 0 else DAD
                g.add(rbar(col, H5[j], 0.22).move_to(P(x + [-0.4, 0.0, 0.4][j], y)))
            return g

        self.at("lines up and separates")
        self.play(*[Indicate(m, scale_factor=1.15) for m in (pb[0], po[1], pb[2])], run_time=0.8)
        self.at("one chromosome from each pair")
        sample = gam([0, 1, 0], 0.0)
        cap = T("a sex cell: one from each pair", 26, GREEN).move_to(P(0, -2.45))
        self.play(FadeIn(sample, shift=UP * 0.3), FadeIn(cap), run_time=0.9)
        self.at("either chromosome")
        self.play(*[Indicate(m, color=YELLOW, scale_factor=1.15) for m in (pb[0], po[0])], run_time=0.8)
        # --- doubling ----------------------------------------------------------------------
        self.at("every pair")
        self.play(FadeOut(sample), FadeOut(cap), run_time=0.4)

        def stage(k):
            n = 2 ** k
            out = []
            for idx in range(n):
                bits = [(idx >> (k - 1 - j)) & 1 for j in range(k)]
                out.append(gam(bits, (idx - (n - 1) / 2) * 1.6))
            return out

        s1 = stage(1)
        c1 = T("1 pair: 2 choices", 30, YELLOW).move_to(P(0, -2.45))
        self.play(*[FadeIn(g, shift=UP * 0.2) for g in s1], FadeIn(c1), run_time=0.8)
        self.at("combinations")
        s2 = stage(2)
        c2 = T("2 pairs: 2 × 2 = 4", 30, YELLOW).move_to(P(0, -2.45))
        self.play(*[TransformFromCopy(s1[j], s2[2 * j + c]) for j in range(2) for c in range(2)],
                  FadeOut(VGroup(*s1)), ReplacementTransform(c1, c2), run_time=1.1)
        self.at("Three pairs give")
        s3 = stage(3)
        c3 = T("3 pairs: 2 × 2 × 2 = 8", 30, YELLOW).move_to(P(0, -2.45))
        self.play(*[TransformFromCopy(s2[j], s3[2 * j + c]) for j in range(4) for c in range(2)],
                  FadeOut(VGroup(*s2)), ReplacementTransform(c2, c3), run_time=1.3)
        self.at("which is")
        note = T("calculated; crossing over not counted", 22, GREY).move_to(P(0, -3.15))
        self.play(Indicate(c3, color=YELLOW, scale_factor=1.12), FadeIn(note), run_time=0.8)
        # --- 23 pairs -------------------------------------------------------------------------
        self.at("Humans have 23 pairs")
        self.play(FadeOut(VGroup(*s3)), FadeOut(c3), FadeOut(pairs), FadeOut(note), FadeOut(head), run_time=0.7)
        h23 = T("Humans: 23 pairs", 40, TEXT).move_to(P(0, 2.4))
        self.play(FadeIn(h23, shift=DOWN * 0.1), run_time=0.5)
        self.at("to the power")
        big = T("2²³", 110, YELLOW, weight=BOLD).move_to(P(0, 0.6))
        self.play(FadeIn(big, scale=0.8), run_time=0.7)
        self.at("about")
        num = M("= 8,388,608", 44, TEXT).move_to(P(0, -1.0))
        txt = T("about 8.4 million chromosome combinations", 34, YELLOW).move_to(P(0, -1.9))
        nt = T("from one parent · calculated · crossing over not counted", 22, GREY).move_to(P(0, -2.7))
        self.play(FadeIn(num, shift=UP * 0.1), FadeIn(txt, shift=UP * 0.1), FadeIn(nt), run_time=0.9)
        self.finish()


# ---------------------------------------------------------------------------------------------
class S06Answer(SpokenScene):
    """Egg + sperm -> diploid cell; each child from a different egg and sperm; the answer."""

    def construct(self):
        H6 = [1.0, 0.75, 0.55]

        def gcell(center, choices, kind, r=1.1, hs=1.0, w=0.22, color=GREEN):
            c = cellc(center, r, color)
            g = VGroup(c)
            for j, ch in enumerate(choices):
                g.add(rbar(EGGC[ch] if kind == 'e' else SPC[ch], H6[j] * hs, w).move_to(center + P([-0.4, 0.0, 0.4][j] * hs, 0)))
            return g

        egg = gcell(P(-3.2, 0.6), [0, 1, 0], 'e')
        sperm = gcell(P(3.2, 0.6), [1, 1, 0], 'p')
        self.at("Fertilization")
        el = T("egg: 23", 28, EGGC[0]).move_to(P(-3.2, -1.0))
        sl = T("sperm: 23", 28, SPC[0]).move_to(P(3.2, -1.0))
        fert = term("fertilization", 30).move_to(P(0, 2.9))
        self.play(FadeIn(egg), FadeIn(sperm), FadeIn(el), FadeIn(sl), FadeIn(fert, shift=DOWN * 0.1), run_time=0.9)
        self.at("join")
        # merged diploid cell: the egg's bar and the sperm's bar of each pair side by side
        zc = cellc(P(0, 0.6), 1.7, GREY)
        zb = VGroup(zc)
        for j, (ce, cs) in enumerate([(0, 1), (1, 1), (0, 0)]):
            zb.add(rbar(EGGC[ce], H6[j] * 1.2, 0.26).move_to(P([-0.8, 0.0, 0.8][j] - 0.2, 0.6)))
            zb.add(rbar(SPC[cs], H6[j] * 1.2, 0.26).move_to(P([-0.8, 0.0, 0.8][j] + 0.2, 0.6)))
        self.play(ReplacementTransform(VGroup(egg, sperm), zb), FadeOut(VGroup(el, sl)), run_time=1.4)
        self.at("diploid cell")
        dl = term("diploid: 46", 28).move_to(P(0, -1.6))
        nt = T("model: 3 + 3 = 6 chromosomes", 22, GREY).move_to(P(0, -2.3))
        self.play(FadeIn(dl, shift=UP * 0.1), FadeIn(nt), run_time=0.6)
        # --- three children ----------------------------------------------------------------
        self.at("Each sibling")
        self.play(FadeOut(VGroup(zb, dl, nt, fert)), run_time=0.5)
        combos = [([0, 1, 0], [1, 1, 0]), ([1, 0, 0], [0, 1, 1]), ([0, 0, 1], [1, 0, 1])]
        kids = []
        for k, x in enumerate([-4.2, 0.0, 4.2]):
            box = RoundedRectangle(corner_radius=0.2, width=3.3, height=2.5, stroke_color=GREY, stroke_width=3,
                                   fill_color=GREY, fill_opacity=0.08).move_to(P(x, 0.4))
            g = VGroup(box)
            e, s = combos[k]
            for j in range(3):
                g.add(rbar(EGGC[e[j]], H6[j] * 1.1, 0.26).move_to(P(x + [-0.95, 0.0, 0.95][j] - 0.2, 0.4)))
                g.add(rbar(SPC[s[j]], H6[j] * 1.1, 0.26).move_to(P(x + [-0.95, 0.0, 0.95][j] + 0.2, 0.4)))
            g.add(T(f"child {k + 1}", 26, TEXT).move_to(P(x, -1.2)))
            kids.append(g)
        self.play(*[FadeIn(k, shift=UP * 0.2) for k in kids], run_time=0.9)
        self.at("different egg")
        d1 = T("a different egg", 30, GREEN).move_to(P(-2.2, 2.6))
        self.play(FadeIn(d1, shift=DOWN * 0.1), run_time=0.5)
        self.at("different sperm")
        d2 = T("and a different sperm", 30, GREEN).move_to(P(2.6, 2.6))
        self.play(FadeIn(d2, shift=DOWN * 0.1), run_time=0.5)
        key1 = T("pink: from the egg (mother)", 22, EGGC[0]).move_to(P(-3.0, -3.2))
        key2 = T("purple: from the sperm (father)", 22, SPC[0]).move_to(P(3.0, -3.2))
        self.play(FadeIn(key1), FadeIn(key2), run_time=0.4)
        self.at("a new mix")
        mix = T("each sex cell is a new mix", 34, YELLOW).move_to(P(0, -2.3))
        self.play(FadeIn(mix, shift=UP * 0.15), run_time=0.6)
        self.at("halves the chromosomes")
        self.play(FadeOut(VGroup(*kids, d1, d2, mix, key1, key2)), run_time=0.5)
        h = chip("halves the chromosomes", GREEN, 40).move_to(P(0, 1.2))
        self.play(FadeIn(h, shift=UP * 0.15), run_time=0.7)
        self.at("shuffles them")
        s = chip("shuffles them", YELLOW, 40).move_to(P(0, -0.4))
        self.play(FadeIn(s, shift=UP * 0.15), run_time=0.7)
        self.at("siblings differ")
        end = T("so siblings differ", 48, TEXT, font=TITLE_FONT).move_to(P(0, -2.45))
        self.play(FadeIn(end, shift=UP * 0.15), run_time=0.7)
        self.finish()


class S07End(EndCard):
    LINE = "Meiosis halves the chromosomes and shuffles them, so siblings differ."
