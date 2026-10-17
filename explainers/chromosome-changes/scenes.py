"""Chromosome changes: one missed separation, one extra chromosome  (Biochemistrypedia explainer)

Timed to the SPOKEN words: every self.at("...") cue waits for that phrase in audio/words.json.

COLOR MAP (one color per concept, whole video)
  BLUE   = homologue "A" of the parent being followed (chromosome 21A; allele 3 in the marker scenes)
  YELLOW = homologue "B" of the same parent (21B; allele 4)
  GREY   = everything else: cells, outlines, the other parent's chromosomes, arrows, labels
  RED    = the error and its abnormal products (failure to part, disomic, nullisomic, three copies,
           the verdict chips)
  GREEN  = a normal product
  TEAL   = the division that is running (meiosis I / meiosis II chip)
  TEXT   = the marker band on a chromosome
"""
import numpy as np
from bp_style import *  # noqa: F401,F403

# stage for the meiosis scenes
X0, X1, X2 = -5.0, -1.2, 2.6
SEC_Y = [1.48, -1.48]
SP_Y = [2.2, 0.75, -0.75, -2.2]
R0, R1, R2 = 1.05, 0.85, 0.58
CAP_H = 0.7


def capsule(color, h=CAP_H, w=0.17, op=0.85):
    return RoundedRectangle(corner_radius=w / 2, width=w, height=h, stroke_color=color, stroke_width=2.5,
                            fill_color=color, fill_opacity=op)


def chromo(color, n=2, h=CAP_H):
    """A chromosome as n side-by-side chromatids (n=2: sisters still joined)."""
    caps = [capsule(color, h) for _ in range(n)]
    g = VGroup(*caps).arrange(RIGHT, buff=0.03)
    g.caps = caps
    return g


def cell(x, y, r, color=GREY):
    return Circle(radius=r, stroke_color=color, stroke_width=3, fill_color=color, fill_opacity=0.07).move_to([x, y, 0])


def arr(a, b, color=GREY, w=4):
    return Arrow(a, b, buff=0.05, color=color, stroke_width=w, tip_length=0.2,
                 max_tip_length_to_length_ratio=0.45, max_stroke_width_to_length_ratio=12)


def div_chip(text, color=GREY, x=0.0):
    c = chip(text, color, size=26)
    return c.move_to([x, 3.2, 0])


def sperm_icon(n, x, y):
    c = Circle(radius=0.36, stroke_color=RED, stroke_width=3, fill_color=RED, fill_opacity=0.1)
    caps = VGroup(*[capsule(BLUE, h=0.4, w=0.11) for _ in range(n)]).arrange(RIGHT, buff=0.04)
    return VGroup(c, caps.move_to(c)).move_to([x, y, 0])


def tall(color, label, h=3.0, w=0.32):
    """A whole chromosome with its marker band at the centromere; the band carries the allele number."""
    body = capsule(color, h=h, w=w, op=0.8)
    band = RoundedRectangle(corner_radius=0.08, width=0.6, height=0.44, fill_color=TEXT, fill_opacity=1,
                            stroke_color=color, stroke_width=3).move_to(body)
    num = M(label, 26, BG, weight=BOLD).move_to(band)
    g = VGroup(body, band, num)
    g.body, g.band, g.num = body, band, num
    g.bn = VGroup(band, num)
    return g


def homologue_pair(x, y=0.3):
    a = tall(BLUE, "3").move_to([x - 0.8, y, 0])
    b = tall(YELLOW, "4").move_to([x + 0.8, y, 0])
    return VGroup(a, b)


def sister_pair(x, y=0.3):
    a = tall(BLUE, "3").move_to([x - 0.38, y, 0])
    b = tall(BLUE, "3").move_to([x + 0.38, y, 0])
    link = Line(a.band.get_right(), b.band.get_left(), color=TEXT, stroke_width=6)
    return VGroup(a, b, link)


class S00Title(TitleCard):
    LESSON = "Chromosome number and structure"
    TITLE = "One missed separation, one extra chromosome"


# ---------------------------------------------------------------------------------------------
class S01Count(SpokenScene):
    """46 small chromosomes in a cell; a 47th appears in red; the question."""

    def construct(self):
        box = RoundedRectangle(corner_radius=0.3, width=11.9, height=4.7, stroke_color=GREY, stroke_width=3,
                               fill_color=GREY, fill_opacity=0.06).move_to([0, -0.45, 0])
        ys = [1.0, -0.45, -1.9]
        slots = [((i - 3.5) * 1.35, ys[0]) for i in range(8)] + [((i - 3.5) * 1.35, ys[1]) for i in range(8)] \
            + [((i - 3.5) * 1.35, ys[2]) for i in range(7)]
        pairs = VGroup(*[chromo(GREY, n=2, h=1.1).move_to([x, y, 0]) for (x, y) in slots])
        count = M("46", 76, TEXT, weight=BOLD).move_to([-0.9, 2.9, 0])
        self.at("In 1959")
        self.play(FadeIn(box), run_time=0.5)
        self.play(LaggedStart(*[FadeIn(p, scale=0.8) for p in pairs], lag_ratio=0.03), FadeIn(count), run_time=2.0)
        self.at("nine children")
        self.play(Indicate(count, color=TEXT, scale_factor=1.12), run_time=0.7)

        extra = chromo(RED, n=1, h=1.1).move_to([(7 - 3.5) * 1.35, ys[2], 0])
        self.at("It found")
        count47 = M("47", 76, RED, weight=BOLD).move_to(count)
        self.play(FadeIn(extra, scale=1.6), ReplacementTransform(count, count47), run_time=0.9)
        self.at("One chromosome too many")
        self.play(Indicate(extra, color=RED, scale_factor=1.4), run_time=0.9)
        q = T("How?", 52, RED, weight=BOLD).move_to([2.4, 2.9, 0])
        self.at("How does")
        self.play(FadeIn(q, shift=UP * 0.2), run_time=0.5)
        self.at("meiosis")
        self.play(FadeOut(VGroup(box, pairs, count47, extra, q)), run_time=0.8)
        self.finish()


# ---------------------------------------------------------------------------------------------
class S02Divisions(SpokenScene):
    """a cell divides twice: homologues part, then sisters part; then nondisjunction."""

    def construct(self):
        x0, x1, x2 = X0 + 1.7, X1 + 1.7, X2 + 1.7
        st = cell(x0, 0, R0)
        a = chromo(BLUE).move_to([x0 - 0.35, 0, 0])
        b = chromo(YELLOW).move_to([x0 + 0.35, 0, 0])
        self.at("A cell makes")
        self.play(FadeIn(st), FadeIn(a), FadeIn(b), run_time=0.6)
        chI = div_chip("meiosis I", GREY, -1.4)
        chII = div_chip("meiosis II", GREY, 2.4)
        self.at("two divisions")
        self.play(FadeIn(chI), FadeIn(chII), run_time=0.6)

        # meiosis I: homologues part
        secs = [cell(x1, y, R1) for y in SEC_Y]
        arrs = [arr([x0 + R0 + 0.05, 0.3 * s, 0], [x1 - R1 - 0.05, y - 0.15 * s, 0]) for s, y in zip((1, -1), SEC_Y)]
        chI_on = div_chip("meiosis I", TEAL, -1.4)
        self.at("At meiosis")
        self.play(ReplacementTransform(chI, chI_on), *[GrowArrow(x) for x in arrs], *[FadeIn(s) for s in secs],
                  run_time=2.4)
        hl = T("homologues", 24, GREY).move_to([x0, -R0 - 0.4, 0])
        self.at("of each pair")
        self.play(FadeIn(hl), a.animate.move_to([x1, SEC_Y[0], 0]), b.animate.move_to([x1, SEC_Y[1], 0]),
                  run_time=1.2)

        # meiosis II: sisters part
        sps = [cell(x2, y, R2) for y in SP_Y]
        arrs2 = [arr([x1 + R1 + 0.05, y, 0], [x2 - R2 - 0.05, sy, 0])
                 for y, sy_pair in zip(SEC_Y, [(SP_Y[0], SP_Y[1]), (SP_Y[2], SP_Y[3])]) for sy in sy_pair]
        chII_on = div_chip("meiosis II", TEAL, 2.4)
        self.at("At meiosis", nth=1)
        self.play(ReplacementTransform(chII, chII_on), FadeOut(hl), *[GrowArrow(x) for x in arrs2],
                  *[FadeIn(s) for s in sps], run_time=0.8)
        sl = T("sister chromatids", 24, GREY).move_to([x1, -SEC_Y[0] - R1 - 0.4 + 0.0, 0])
        sl.move_to([x1, -2.78, 0])
        self.at("sister chromatids")
        self.play(FadeIn(sl), run_time=0.4)
        self.at("of each chromosome")
        self.play(a.caps[0].animate.move_to([x2, SP_Y[0], 0]), a.caps[1].animate.move_to([x2, SP_Y[1], 0]),
                  b.caps[0].animate.move_to([x2, SP_Y[2], 0]), b.caps[1].animate.move_to([x2, SP_Y[3], 0]),
                  run_time=1.2)

        # nondisjunction: the pair that fails to part
        self.at("disjunction")
        everything = VGroup(st, secs[0], secs[1], *arrs, *arrs2, *sps, a, b, chI_on, chII_on, sl)
        self.play(FadeOut(everything), run_time=0.4)
        pa = chromo(BLUE, h=1.9).move_to([-0.45, 0.2, 0])
        pb = chromo(YELLOW, h=1.9).move_to([0.45, 0.2, 0])
        pull = VGroup(arr([-1.3, 0.2, 0], [-4.6, 0.2, 0], GREY, 6), arr([1.3, 0.2, 0], [4.6, 0.2, 0], GREY, 6))
        title = T("nondisjunction", 48, RED, weight=BOLD).move_to([0, 2.55, 0])
        self.play(FadeIn(pa), FadeIn(pb), FadeIn(title, shift=DOWN * 0.15), run_time=0.5)
        self.at("failure of chromosomes")
        self.play(*[GrowArrow(x) for x in pull], run_time=0.6)
        stuck = Line([-1.0, -1.45, 0], [1.0, -1.45, 0], color=RED, stroke_width=6)
        note = T("they stay together", 30, RED).move_to([0, -2.0, 0])
        self.at("part")
        self.play(Create(stuck), FadeIn(note), run_time=0.6)
        c1 = div_chip("at meiosis I", GREY, -2.4).move_to([-2.4, -3.1, 0])
        c2 = div_chip("at meiosis II", GREY, 2.4).move_to([2.4, -3.1, 0])
        self.at("Where it happens")
        self.play(FadeIn(c1), FadeIn(c2), run_time=0.6)
        self.at("changes the result")
        self.play(Indicate(c1, color=TEAL), Indicate(c2, color=TEAL), run_time=0.9)
        self.finish()


# ---------------------------------------------------------------------------------------------
class S03First(SpokenScene):
    """meiosis I error: both homologues to one cell -> two disomic sperm, two nullisomic."""

    def construct(self):
        st = cell(X0, 0, R0)
        a = chromo(BLUE).move_to([X0 - 0.35, 0, 0])
        b = chromo(YELLOW).move_to([X0 + 0.35, 0, 0])
        stl = T("spermatocyte", 24, GREY).move_to([X0, R0 + 0.4, 0])
        self.at("Follow chromosome")
        self.play(FadeIn(st), FadeIn(a), FadeIn(b), FadeIn(stl), run_time=0.5)
        la = T("21A", 26, BLUE, weight=BOLD).move_to([X0 - 0.6, -R0 - 0.4, 0])
        lb = T("21B", 26, YELLOW, weight=BOLD).move_to([X0 + 0.6, -R0 - 0.4, 0])
        chI = div_chip("meiosis I", GREY, -3.1)
        chII = div_chip("meiosis II", GREY, 0.7)
        self.at("call the")
        self.play(FadeIn(la), FadeIn(lb), FadeIn(chI), FadeIn(chII), run_time=0.7)

        # error at meiosis I
        chI_bad = div_chip("meiosis I", RED, -3.1)
        ring = SurroundingRectangle(VGroup(a, b), color=RED, buff=0.08, corner_radius=0.12, stroke_width=4)
        self.at("fail to separate")
        self.play(ReplacementTransform(chI, chI_bad), Create(ring), run_time=0.7)
        secs = [cell(X1, y, R1) for y in SEC_Y]
        arrs = [arr([X0 + R0 + 0.05, 0.3 * s, 0], [X1 - R1 - 0.05, y - 0.15 * s, 0]) for s, y in zip((1, -1), SEC_Y)]
        self.at("same cell")
        self.play(*[GrowArrow(x) for x in arrs], *[FadeIn(s) for s in secs], FadeOut(VGroup(la, lb)), run_time=0.5)
        grp = VGroup(a, b, ring)
        self.play(grp.animate.move_to([X1, SEC_Y[0], 0]), run_time=0.8)
        self.play(FadeOut(ring), run_time=0.2)

        # meiosis II normal
        sps = [cell(X2, y, R2) for y in SP_Y]
        arrs2 = [arr([X1 + R1 + 0.05, y, 0], [X2 - R2 - 0.05, sy, 0])
                 for y, pr in zip(SEC_Y, [(SP_Y[0], SP_Y[1]), (SP_Y[2], SP_Y[3])]) for sy in pr]
        chII_on = div_chip("meiosis II", TEAL, 0.7)
        self.at("Meiosis", nth=1)
        self.play(ReplacementTransform(chII, chII_on), *[GrowArrow(x) for x in arrs2], *[FadeIn(s) for s in sps],
                  run_time=0.8)
        self.at("runs normally")
        self.play(a.caps[0].animate.move_to([X2 - 0.12, SP_Y[0], 0]), b.caps[0].animate.move_to([X2 + 0.12, SP_Y[0], 0]),
                  a.caps[1].animate.move_to([X2 - 0.12, SP_Y[1], 0]), b.caps[1].animate.move_to([X2 + 0.12, SP_Y[1], 0]),
                  run_time=1.3)

        # the products
        top = Line([3.55, SP_Y[0] + 0.45, 0], [3.55, SP_Y[1] - 0.45, 0], color=RED, stroke_width=5)
        t1 = VGroup(T("disomic", 30, RED, weight=BOLD), T("two copies", 24, GREY)).arrange(DOWN, aligned_edge=LEFT, buff=0.1)
        t1.next_to(top, RIGHT, buff=0.25)
        self.at("meaning each")
        self.play(sps[0].animate.set_stroke(RED), sps[1].animate.set_stroke(RED), Create(top), FadeIn(t1), run_time=0.8)
        bot = Line([3.55, SP_Y[2] + 0.45, 0], [3.55, SP_Y[3] - 0.45, 0], color=RED, stroke_width=5)
        t2 = VGroup(T("nullisomic", 30, RED, weight=BOLD), T("none", 24, GREY)).arrange(DOWN, aligned_edge=LEFT, buff=0.1)
        t2.next_to(bot, RIGHT, buff=0.25)
        self.at("The other cell")
        self.play(Indicate(secs[1], color=GREY, scale_factor=1.15), run_time=0.7)
        self.at("its two")
        self.play(sps[2].animate.set_stroke(RED), sps[3].animate.set_stroke(RED), Create(bot), FadeIn(t2), run_time=0.8)
        self.finish()


# ---------------------------------------------------------------------------------------------
class S04Second(SpokenScene):
    """meiosis II error: one disomic, one nullisomic, two normal; tally 2 vs 1; disomic sperm + egg."""

    def construct(self):
        st = cell(X0, 0, R0)
        a = chromo(BLUE).move_to([X0 - 0.35, 0, 0])
        b = chromo(YELLOW).move_to([X0 + 0.35, 0, 0])
        chI = div_chip("meiosis I", GREY, -3.1)
        chII = div_chip("meiosis II", GREY, 0.7)
        self.at("Now fail")
        self.play(FadeIn(st), FadeIn(a), FadeIn(b), FadeIn(chI), FadeIn(chII), run_time=0.7)
        chII_bad = div_chip("meiosis II", RED, 0.7)
        self.at("instead")
        self.play(ReplacementTransform(chII, chII_bad), run_time=0.5)

        secs = [cell(X1, y, R1) for y in SEC_Y]
        arrs = [arr([X0 + R0 + 0.05, 0.3 * s, 0], [X1 - R1 - 0.05, y - 0.15 * s, 0]) for s, y in zip((1, -1), SEC_Y)]
        chI_on = div_chip("meiosis I", TEAL, -3.1)
        self.at("normal")
        self.play(ReplacementTransform(chI, chI_on), *[GrowArrow(x) for x in arrs], *[FadeIn(s) for s in secs],
                  a.animate.move_to([X1, SEC_Y[0], 0]), b.animate.move_to([X1, SEC_Y[1], 0]), run_time=1.3)

        ring = SurroundingRectangle(a, color=RED, buff=0.1, corner_radius=0.12, stroke_width=4)
        self.at("sisters")
        self.play(Create(ring), run_time=0.5)
        sps = [cell(X2, y, R2) for y in SP_Y]
        arrs2 = [arr([X1 + R1 + 0.05, y, 0], [X2 - R2 - 0.05, sy, 0])
                 for y, pr in zip(SEC_Y, [(SP_Y[0], SP_Y[1]), (SP_Y[2], SP_Y[3])]) for sy in pr]
        self.at("giving")
        self.play(*[GrowArrow(x) for x in arrs2], *[FadeIn(s) for s in sps], FadeOut(ring), run_time=0.7)
        self.play(a.caps[0].animate.move_to([X2 - 0.12, SP_Y[0], 0]), a.caps[1].animate.move_to([X2 + 0.12, SP_Y[0], 0]),
                  b.caps[0].animate.move_to([X2, SP_Y[2], 0]), b.caps[1].animate.move_to([X2, SP_Y[3], 0]),
                  run_time=1.2)
        t_dis = T("disomic", 28, RED, weight=BOLD).next_to(sps[0], RIGHT, buff=0.3)
        t_nul = T("none", 28, RED, weight=BOLD).next_to(sps[1], RIGHT, buff=0.3)
        self.play(sps[0].animate.set_stroke(RED), sps[1].animate.set_stroke(RED), FadeIn(t_dis), FadeIn(t_nul),
                  run_time=0.6)
        t_n1 = T("normal", 28, GREEN, weight=BOLD).next_to(sps[2], RIGHT, buff=0.3)
        t_n2 = T("normal", 28, GREEN, weight=BOLD).next_to(sps[3], RIGHT, buff=0.3)
        self.at("The other cell")
        self.play(sps[2].animate.set_stroke(GREEN), sps[3].animate.set_stroke(GREEN), FadeIn(t_n1), FadeIn(t_n2),
                  run_time=0.8)

        # tally: 2 vs 1
        left = VGroup(st, secs[0], secs[1], *arrs, *arrs2, chI_on, chII_bad)
        r1l = T("meiosis I error", 28, TEXT).move_to([-4.2, 1.0, 0])
        r2l = T("meiosis II error", 28, TEXT).move_to([-4.2, -1.0, 0])
        r1l.set_x(-4.2); r2l.set_x(-4.2)
        n1 = M("2", 56, RED, weight=BOLD).move_to([-0.7, 1.0, 0])
        n2 = M("1", 56, RED, weight=BOLD).move_to([-0.7, -1.0, 0])
        i1 = VGroup(sperm_icon(2, -2.4, 1.0), sperm_icon(2, -1.5, 1.0))
        i2 = sperm_icon(2, -2.4, -1.0)
        self.at("So a")
        self.play(FadeOut(left), FadeOut(t_n1), FadeOut(t_n2), FadeOut(sps[2]), FadeOut(sps[3]),
                  FadeOut(VGroup(t_nul, sps[1])), FadeOut(b.caps[0]), FadeOut(b.caps[1]), FadeIn(r1l), run_time=0.7)
        self.at("error gives")
        self.play(FadeIn(i1), FadeIn(n1), run_time=0.6)
        self.at("and a")
        self.play(FadeIn(r2l), run_time=0.4)
        self.at("error gives", nth=1)
        self.play(FadeIn(i2), FadeIn(n2), run_time=0.6)

        # a disomic sperm joins a normal egg
        keep = VGroup(sps[0], a.caps[0], a.caps[1], t_dis)
        self.at("Joined")
        self.play(FadeOut(VGroup(r1l, r2l, i1, i2, n1, n2)), FadeOut(t_dis), run_time=0.5)
        sp_group = VGroup(sps[0], a.caps[0], a.caps[1])
        egg = cell(3.2, 0, 0.9)
        egg_chr = capsule(GREY, h=CAP_H).move_to(egg)
        egg_lbl = T("normal egg", 26, GREY).next_to(egg, DOWN, buff=0.3)
        self.play(sp_group.animate.move_to([-2.4, 0, 0]).scale(1.3), FadeIn(egg), FadeIn(egg_chr), FadeIn(egg_lbl),
                  run_time=1.1)
        zyg = cell(0, 0.3, 1.7, RED)
        self.at("sperm gives")
        self.play(FadeOut(egg_lbl), FadeOut(VGroup(sps[0], egg)), FadeIn(zyg),
                  a.caps[0].animate.scale(2.0 / 1.3).move_to([-0.7, 0.3, 0]),
                  a.caps[1].animate.scale(2.0 / 1.3).move_to([0.0, 0.3, 0]),
                  egg_chr.animate.scale(2.0).move_to([0.7, 0.3, 0]), run_time=1.0)
        three = T("three copies", 40, RED, weight=BOLD).next_to(zyg, DOWN, buff=0.3)
        self.at("zygote")
        self.play(FadeIn(three, shift=UP * 0.15), run_time=0.5)
        self.finish()


# ---------------------------------------------------------------------------------------------
HEAD_Y = 3.2


def column_label(text, x, y=1.95):
    return T(text, 26, GREY).move_to([x, y, 0])


def verdict(text, x=-3.4, y=-2.8):
    return chip(text, RED, size=30).move_to([x, y, 0])


class S05MaternalOne(SpokenScene):
    """homologues differ at the centromere marker, sisters do not; then Child A types 1, 3, 4."""

    def construct(self):
        head = T("DNA marker at the centromere", 32, GREY).move_to([0, HEAD_Y, 0])
        hp = homologue_pair(-3.2)
        sp = sister_pair(3.2)
        hl = T("homologues", 30, TEXT).move_to([-3.2, -2.0, 0])
        sl = T("sisters", 30, TEXT).move_to([3.2, -2.0, 0])
        hd = T("alleles differ", 26, GREY).move_to([-3.2, -2.55, 0])
        sd = T("same allele", 26, GREY).move_to([3.2, -2.55, 0])
        self.play(FadeIn(head), FadeIn(hp, shift=UP * 0.15), FadeIn(hl), run_time=0.7)
        self.at("differ there")
        self.play(FadeIn(hd), Indicate(hp[0].bn, color=TEXT, scale_factor=1.15), Indicate(hp[1].bn, color=TEXT, scale_factor=1.15), run_time=0.6)
        self.at("and sisters")
        self.play(FadeIn(sp, shift=UP * 0.15), FadeIn(sl), run_time=0.7)
        self.at("do not")
        self.play(FadeIn(sd), Indicate(sp[0].bn, color=TEXT, scale_factor=1.15), Indicate(sp[1].bn, color=TEXT, scale_factor=1.15), run_time=0.6)

        # the family
        head2 = T("chromosome 21, marker at the centromere", 30, GREY).move_to([0, HEAD_Y, 0])
        fa = VGroup(tall(GREY, "1", h=3.4).move_to([-5.45, -0.3, 0]), tall(GREY, "2", h=3.4).move_to([-4.55, -0.3, 0]))
        mo = VGroup(tall(BLUE, "3", h=3.4).move_to([-2.25, -0.3, 0]), tall(YELLOW, "4", h=3.4).move_to([-1.35, -0.3, 0]))
        demo_body = capsule(GREY, h=3.4, w=0.32, op=0.8).move_to([-1.0, -0.2, 0])
        demo_band = RoundedRectangle(corner_radius=0.08, width=0.6, height=0.44, fill_color=TEXT, fill_opacity=1,
                                     stroke_color=GREY, stroke_width=3).move_to(demo_body)
        demo_line = Line(demo_band.get_right() + RIGHT * 0.05, demo_band.get_right() + RIGHT * 0.9, color=GREY, stroke_width=3)
        demo_lbl = T("DNA marker at the centromere", 28, TEXT).next_to(demo_line, RIGHT, buff=0.15)
        demo = VGroup(demo_body, demo_band, demo_line, demo_lbl)
        self.at("Take a DNA marker")
        self.play(FadeOut(VGroup(hp, sp, hl, sl, hd, sd)), ReplacementTransform(head, head2), FadeIn(demo), run_time=0.7)
        fl = column_label("father", -5.0)
        ml = column_label("mother", -1.8)
        self.at("The father carries")
        self.play(FadeOut(demo), FadeIn(fa, shift=UP * 0.15), FadeIn(fl), run_time=0.7)
        self.at("the mother carries")
        self.play(FadeIn(mo, shift=UP * 0.15), FadeIn(ml), run_time=0.7)

        ch = VGroup(tall(GREY, "1", h=3.4).move_to([2.1, -0.3, 0]), tall(BLUE, "3", h=3.4).move_to([3.2, -0.3, 0]),
                    tall(YELLOW, "4", h=3.4).move_to([4.3, -0.3, 0]))
        cl = column_label("Child A", 3.2)
        self.at("Child A types")
        self.play(FadeIn(cl), LaggedStart(*[FadeIn(c, shift=UP * 0.15) for c in ch], lag_ratio=0.25), run_time=1.3)
        r1 = SurroundingRectangle(ch[0], color=TEXT, buff=0.12, corner_radius=0.1, stroke_width=3)
        r2 = SurroundingRectangle(VGroup(ch[1], ch[2]), color=TEXT, buff=0.12, corner_radius=0.1, stroke_width=3)
        self.at("paternal allele")
        self.play(Create(r1), run_time=0.5)
        self.at("two different")
        self.play(Create(r2), run_time=0.5)
        link = arr([-0.8, -0.3, 0], [1.9 - 0.0, -0.3, 0], TEXT, 5)
        self.at("is maternal")
        self.play(GrowArrow(link), Indicate(mo, color=TEXT, scale_factor=1.05), run_time=0.8)
        v = verdict("maternal meiosis I")
        self.at("the error was")
        self.play(FadeIn(v, shift=UP * 0.15), run_time=0.6)
        self.finish()


# ---------------------------------------------------------------------------------------------
class S06MaternalTwo(SpokenScene):
    """Child B types 1, 3, 3 -> sisters -> maternal meiosis II; the crossover caveat; the rule."""

    def construct(self):
        head = T("chromosome 21, marker near the centromere", 30, GREY).move_to([0, HEAD_Y, 0])
        fa = VGroup(tall(GREY, "1", h=3.4).move_to([-5.45, -0.3, 0]), tall(GREY, "2", h=3.4).move_to([-4.55, -0.3, 0]))
        mo = VGroup(tall(BLUE, "3", h=3.4).move_to([-2.25, -0.3, 0]), tall(YELLOW, "4", h=3.4).move_to([-1.35, -0.3, 0]))
        fl = column_label("father", -5.0)
        ml = column_label("mother", -1.8)
        self.add(head, fa, mo, fl, ml)
        ch = VGroup(tall(GREY, "1", h=3.4).move_to([2.1, -0.3, 0]), tall(BLUE, "3", h=3.4).move_to([3.2, -0.3, 0]),
                    tall(BLUE, "3", h=3.4).move_to([4.3, -0.3, 0]))
        cl = column_label("Child B", 3.2)
        self.at("Child B types")
        self.play(FadeIn(cl), LaggedStart(*[FadeIn(c, shift=UP * 0.15) for c in ch], lag_ratio=0.25), run_time=1.3)
        r2 = SurroundingRectangle(VGroup(ch[1], ch[2]), color=TEXT, buff=0.12, corner_radius=0.1, stroke_width=3)
        self.at("one maternal allele")
        self.play(Create(r2), run_time=0.5)
        # bracket under the two matching chromosomes
        bx0, bx1, by = 3.2, 4.3, -2.2
        brk = VGroup(Line([bx0, by + 0.15, 0], [bx0, by, 0], color=TEXT, stroke_width=4),
                     Line([bx0, by, 0], [bx1, by, 0], color=TEXT, stroke_width=4),
                     Line([bx1, by, 0], [bx1, by + 0.15, 0], color=TEXT, stroke_width=4))
        bl = T("sisters", 28, TEXT).move_to([3.75, -2.6, 0])
        self.at("The sisters stayed")
        self.play(FadeOut(r2), Create(brk), FadeIn(bl), run_time=0.7)
        v = verdict("maternal meiosis II")
        self.at("consistent with")
        self.play(FadeIn(v, shift=UP * 0.15), run_time=0.6)

        # the caveat: a crossover between marker and centromere
        self.at("One caveat")
        self.play(Indicate(v, color=RED, scale_factor=1.06), run_time=0.7)
        new_num = M("4", 26, BG, weight=BOLD).move_to(ch[2].num)
        v2 = verdict("looks like meiosis I")
        self.at("A crossover")
        cx = ch[2].band.get_center() + UP * 0.45
        xmark = VGroup(Line(cx + [-0.2, 0.15, 0], cx + [0.2, -0.15, 0], color=RED, stroke_width=6),
                       Line(cx + [-0.2, -0.15, 0], cx + [0.2, 0.15, 0], color=RED, stroke_width=6))
        self.play(Create(xmark), run_time=0.4)
        self.play(FadeOut(xmark), Transform(ch[2].num, new_num), ch[2].band.animate.set_stroke(YELLOW, 6), FadeOut(v), run_time=0.8)
        self.at("look like the other")
        self.play(FadeOut(brk), FadeOut(bl), FadeIn(v2, shift=UP * 0.15), run_time=0.8)

        # the rule: two panels
        self.at("Keep the rule")
        self.play(FadeOut(VGroup(head, fa, mo, fl, ml, cl, ch, v2)), run_time=0.7)
        hp = homologue_pair(-3.4, 0.5)
        sp = sister_pair(3.4, 0.5)
        hl = T("two homologues together", 28, TEXT).move_to([-3.4, -1.7, 0])
        sl = T("two sisters together", 28, TEXT).move_to([3.4, -1.7, 0])
        v_h = chip("meiosis I", RED, size=32).move_to([-3.4, -2.55, 0])
        v_s = chip("meiosis II", RED, size=32).move_to([3.4, -2.55, 0])
        self.at("homologues together")
        self.play(FadeIn(hp, shift=UP * 0.15), FadeIn(hl), run_time=0.6)
        self.play(FadeIn(v_h), run_time=0.4)
        self.at("sisters together")
        self.play(FadeIn(sp, shift=UP * 0.15), FadeIn(sl), run_time=0.6)
        self.play(FadeIn(v_s), run_time=0.4)
        self.finish()


class S07End(EndCard):
    LINE = "Two homologues together: meiosis I. Two sisters together: meiosis II."
