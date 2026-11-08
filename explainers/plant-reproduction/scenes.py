"""Plant reproduction: one tube, two sperm, two fusions  (Biochemistrypedia explainer)

Timed to the SPOKEN words: every self.at("...") cue waits for that phrase in audio/words.json.

COLOR MAP (one color per concept, whole video)
  BLUE   = paternal: pollen, pollen tube, sperm, the paternal set of chromosomes, the Y allele
  ORANGE = maternal: egg, polar nuclei, central cell, integuments and seed coat, maternal sets, the y allele
  GREEN  = zygote and embryo
  YELLOW = endosperm (and the yellow kernel it colours)
  GREY   = structure and de-emphasized things: stigma, style, ovary, ovule outline, synergids, signals
  TEXT   = plain labels and sums
"""
import numpy as np
from bp_style import *  # noqa: F401,F403

ORANGE = "#F29E4C"
PAT, MAT, EMB, END = BLUE, ORANGE, GREEN, YELLOW


# ---------------------------------------------------------------------------------------------
# helpers
# ---------------------------------------------------------------------------------------------
def P3(x, y):
    return np.array([x, y, 0.0])


def tube_line(pts, w=14, color=PAT, op=0.55):
    m = VMobject(stroke_color=color, stroke_width=w, stroke_opacity=op)
    m.set_points_as_corners([P3(*p) for p in pts])
    return m


def sperm(pos, r=0.32, label=None):
    c = Circle(radius=r, stroke_color=PAT, stroke_width=3, fill_color=PAT, fill_opacity=0.55).move_to(pos)
    if label:
        return VGroup(c, M(label, 24, TEXT).move_to(c))
    return VGroup(c)


def lab(text, color=TEXT, size=24, **kw):
    return T(text, size, color, **kw)


def eqrow(parts, size=40):
    """parts: list of (text, color); returns a horizontal group."""
    g = VGroup(*[M(t, size, c) for t, c in parts]).arrange(RIGHT, buff=0.22)
    return g


class Ovule:
    """The enlarged ovule, drawn as boxes and discs. Built once, relative to centre C."""
    HW, HH, GAP = 2.4, 3.3, 0.55
    SYN_L, SYN_R = (-1.1, 1.65), (1.1, 1.65)
    EGG, CC = (0, 1.5), (0, -1.0)
    NUC = [(-0.75, -1.0), (0.75, -1.0)]
    SP1, SP2 = (-1.3, 0.85), (-0.75, 0.45)

    def __init__(self, C):
        self.C = np.array(C, float)
        c = self.C
        hw, hh, g = self.HW, self.HH, self.GAP
        self.integ = VMobject(stroke_color=GREY, stroke_width=5)
        self.integ.set_points_as_corners([c + P3(*p) for p in
                                          [(-g, hh), (-hw, hh), (-hw, -hh), (hw, -hh), (hw, hh), (g, hh)]])
        self.sac = RoundedRectangle(corner_radius=0.4, width=3.6, height=5.2, stroke_color=GREY,
                                    stroke_width=2, fill_opacity=0).move_to(c + P3(0, -0.1))
        self.egg = Circle(radius=0.55, stroke_color=MAT, stroke_width=3, fill_color=MAT, fill_opacity=0.3).move_to(c + P3(*self.EGG))
        self.synL = Ellipse(width=0.7, height=1.0, stroke_color=GREY, stroke_width=3, fill_color=GREY, fill_opacity=0.25).move_to(c + P3(*self.SYN_L))
        self.synR = Ellipse(width=0.7, height=1.0, stroke_color=GREY, stroke_width=3, fill_color=GREY, fill_opacity=0.25).move_to(c + P3(*self.SYN_R))
        self.cc = Ellipse(width=3.2, height=2.4, stroke_color=MAT, stroke_width=3, fill_color=MAT, fill_opacity=0.10).move_to(c + P3(*self.CC))
        self.nuc = [Circle(radius=0.32, stroke_color=MAT, stroke_width=3, fill_color=MAT, fill_opacity=0.45).move_to(c + P3(*p)) for p in self.NUC]
        self.tube_pts = [(c[0] + 0.0, c[1] + 3.45), (c[0] + 0.0, c[1] + 2.9), (c[0] - 1.1, c[1] + 2.25)]
        self.base = VGroup(self.integ, self.sac, self.egg, self.synL, self.synR, self.cc, *self.nuc)

    def at(self, rel):
        return self.C + P3(*rel)

    def group(self):
        return VGroup(self.base)


class S00Title(TitleCard):
    LESSON = "Flowers, seeds and fruit"
    TITLE = "One tube, two sperm, two fusions"


# ---------------------------------------------------------------------------------------------
class S01Haze(SpokenScene):
    """tassel -> pollen drifts to a silk -> one grain: tube cell + two sperm -> tube grows -> two '?' boxes."""

    def construct(self):
        tassel = VGroup(RoundedRectangle(corner_radius=0.15, width=3.4, height=0.9, stroke_color=PAT, stroke_width=3,
                                         fill_color=PAT, fill_opacity=0.12),
                        lab("tassel: male flowers", PAT)).move_to(P3(-3.8, 2.8))
        tassel[1].move_to(tassel[0])
        ear_b = RoundedRectangle(corner_radius=0.2, width=1.6, height=2.0, stroke_color=MAT, stroke_width=3,
                                 fill_color=MAT, fill_opacity=0.12).move_to(P3(3.8, -1.5))
        ear_l = lab("ear: female flowers", MAT).move_to(P3(3.8, -3.0))
        silk = Line(P3(3.8, -0.5), P3(3.8, 1.9), color=MAT, stroke_width=7)
        silk_l = lab("silk", MAT).next_to(silk, RIGHT, buff=0.2)
        self.play(FadeIn(tassel), run_time=0.4)
        self.at("ripe maize tassel")
        self.play(FadeIn(ear_b), FadeIn(ear_l), Create(silk), FadeIn(silk_l), run_time=1.0)
        # pollen haze drifting from the tassel to the silk tip
        rng = np.random.default_rng(3)
        dots = VGroup(*[Circle(radius=0.11, stroke_width=0, fill_color=PAT, fill_opacity=0.9).move_to(
            P3(-3.8 + rng.uniform(-1.4, 1.4), 2.3 + rng.uniform(-0.2, 0.2))) for _ in range(16)])
        self.at("yellow haze")
        self.play(FadeIn(dots), run_time=0.4)
        anims = []
        for i, d in enumerate(dots):
            tgt = P3(3.8 + rng.uniform(-0.45, 0.45), 1.9 + rng.uniform(0.0, 0.5))
            anims.append(d.animate.move_to(tgt))
        self.play(LaggedStart(*anims, lag_ratio=0.08), run_time=self.beat(0.16))
        # one grain, enlarged
        grain = Circle(radius=1.55, stroke_color=PAT, stroke_width=5, fill_color=PAT, fill_opacity=0.10).move_to(P3(-3.0, 0.5))
        s1 = sperm(P3(-3.6, 0.5), 0.34)
        s2 = sperm(P3(-2.4, 0.5), 0.34)
        g_lab = lab("pollen grain: three cells", TEXT, 26).move_to(P3(-3.0, 2.55))
        self.at("tiny plant")
        self.play(FadeOut(VGroup(tassel, ear_b, ear_l, silk, silk_l, dots)), FadeIn(grain, scale=0.6), run_time=0.8)
        tc = lab("tube cell", PAT, 24).move_to(P3(-3.0, -0.55))
        sp_l = lab("sperm", PAT, 24).move_to(P3(-3.0, 1.35))
        self.play(FadeIn(s1), FadeIn(s2), FadeIn(g_lab), FadeIn(tc), FadeIn(sp_l), run_time=0.8)
        # tube grows
        tube = tube_line([(-1.45, 0.5), (1.9, 0.5)], w=26)
        self.at("grows a tube")
        self.play(Create(tube), run_time=1.0)
        t_l = lab("pollen tube", PAT, 26).move_to(P3(0.2, 1.2))
        self.play(FadeIn(t_l), run_time=0.4)
        self.at("two sperm")
        self.play(s1.animate.move_to(P3(0.6, 0.5)), s2.animate.move_to(P3(1.5, 0.5)), FadeOut(sp_l), run_time=1.0)
        # puzzle: two arrows, two question boxes
        q1 = chip("?", GREY, 40).move_to(P3(4.8, 2.0))
        q2 = chip("?", GREY, 40).move_to(P3(4.8, -1.0))
        a1 = Arrow(s2[0].get_right() + RIGHT * 0.35, q1.get_left(), buff=0.1, color=PAT, stroke_width=5)
        a2 = Arrow(s2[0].get_right() + RIGHT * 0.35, q2.get_left(), buff=0.1, color=PAT, stroke_width=5)
        self.at("Both sperm")
        self.play(GrowArrow(a1), GrowArrow(a2), FadeIn(q1), FadeIn(q2), run_time=0.8)
        why = T("Why two?", 52, TEXT, font=TITLE_FONT).move_to(P3(0.6, -2.4))
        self.at("Why two")
        self.play(Write(why), run_time=0.8)
        self.finish()


# ---------------------------------------------------------------------------------------------
class S02Route(SpokenScene):
    """stigma -> style -> ovary with a tube; the ovule enlarges; the tube bursts into a synergid."""

    def construct(self):
        X = -0.8
        stigma = Rectangle(width=1.6, height=0.45, stroke_color=GREY, stroke_width=3, fill_color=GREY, fill_opacity=0.3).move_to(P3(X, 2.75))
        style = Rectangle(width=0.6, height=3.5, stroke_color=GREY, stroke_width=3, fill_color=GREY, fill_opacity=0.12).move_to(P3(X, 0.75))
        ovary = RoundedRectangle(corner_radius=0.2, width=3.6, height=2.4, stroke_color=GREY, stroke_width=3,
                                 fill_color=GREY, fill_opacity=0.12).move_to(P3(X, -2.2))
        ovule_s = RoundedRectangle(corner_radius=0.2, width=1.0, height=1.2, stroke_color=GREY, stroke_width=4,
                                   fill_color=GREY, fill_opacity=0.3).move_to(P3(X, -1.9))
        l_stigma = lab("stigma", GREY).next_to(stigma, LEFT, buff=0.25)
        l_style = lab("style", GREY).next_to(style, LEFT, buff=0.25)
        l_ovary = lab("ovary", GREY).move_to(P3(X, -3.05))
        l_ovule = lab("ovule", GREY).move_to(P3(X + 1.0, -2.25))
        col = VGroup(stigma, style, ovary, l_stigma, l_style, l_ovary, l_ovule)
        self.play(FadeIn(col), FadeIn(ovule_s), run_time=0.8)

        grain = Circle(radius=0.22, stroke_color=PAT, stroke_width=3, fill_color=PAT, fill_opacity=0.9).move_to(P3(X, 4.2))
        self.at("transfer of pollen")
        self.play(grain.animate.move_to(P3(X, 3.2)), run_time=0.8)
        c_poll = chip("pollination", TEXT, 26).move_to(P3(3.6, 3.0))
        a_poll = Arrow(c_poll.get_left(), P3(X + 0.9, 3.0), buff=0.1, color=TEXT, stroke_width=4)
        self.play(FadeIn(c_poll), GrowArrow(a_poll), run_time=0.6)
        self.at("Fertilization")
        c_fert = chip("fertilization", TEXT, 26).move_to(P3(3.6, -1.5))
        a_fert = Arrow(c_fert.get_left(), P3(X + 0.55, -1.5), buff=0.1, color=TEXT, stroke_width=4)
        self.play(FadeIn(c_fert), GrowArrow(a_fert), run_time=0.6)
        self.at("separate events")
        self.play(Indicate(c_poll, color=TEXT, scale_factor=1.08), Indicate(c_fert, color=TEXT, scale_factor=1.08), run_time=0.8)

        # tube down the style
        tube = tube_line([(X, 3.1), (X, -1.3)], w=14)
        self.at("pollen tube down")
        self.play(FadeOut(VGroup(c_poll, a_poll, c_fert, a_fert)), Create(tube), run_time=1.6)
        sp1 = sperm(P3(X, 2.6), 0.13)
        sp2 = sperm(P3(X, 2.2), 0.13)
        self.at("no flagella")
        self.play(FadeIn(sp1), FadeIn(sp2), run_time=0.4)
        self.at("ride inside")
        self.play(sp1.animate.move_to(P3(X, -0.6)), sp2.animate.move_to(P3(X, -0.2)), run_time=1.6)

        # enlarge the ovule
        ov = Ovule(P3(0.0, -0.1))
        self.at("Near the ovule")
        self.play(FadeOut(VGroup(col, grain, tube, sp1, sp2)), ReplacementTransform(ovule_s, ov.integ),
                  FadeIn(ov.sac), FadeIn(ov.egg), FadeIn(ov.synL), FadeIn(ov.synR), FadeIn(ov.cc),
                  *[FadeIn(n) for n in ov.nuc], run_time=1.4)
        l_syn = lab("synergids", GREY).move_to(ov.at((3.8, 1.65)))
        ln_syn = Line(l_syn.get_left() + LEFT * 0.05, ov.synR.get_right() + RIGHT * 0.05, color=GREY, stroke_width=2)
        def leader(txt, pos, tgt, lines=None):
            t = lab(txt, GREY, 22).move_to(ov.at(pos))
            edge = t.get_right() + RIGHT * 0.05 if pos[0] < 0 else t.get_left() + LEFT * 0.05
            return VGroup(t, Line(edge, ov.at(tgt), color=GREY, stroke_width=2))
        extra = VGroup(
            leader("micropyle", (-3.3, 3.2), (-0.5, 3.2)),
            leader("integuments", (-3.5, 0.4), (-2.4, 0.4)),
            leader("egg", (3.2, 0.75), (0.42, 1.1)))
        cc_t = VGroup(lab("central cell", GREY, 22), lab("(two polar nuclei)", GREY, 22)).arrange(DOWN, buff=0.08).move_to(ov.at((4.1, -1.0)))
        cc_ln = Line(cc_t.get_left() + LEFT * 0.05, ov.at((1.6, -1.0)), color=GREY, stroke_width=2)
        self.play(FadeIn(l_syn), Create(ln_syn), FadeIn(extra), FadeIn(cc_t), Create(cc_ln), run_time=0.8)
        # chemical signals
        sx, sy = ov.SYN_L[0], 2.2
        sig = VGroup(*[Arrow(ov.at((sx + ddx, sy)), ov.at((sx + ddx + dx, sy + dy)), buff=0, color=GREY,
                             stroke_width=3, tip_length=0.14) for ddx, dx, dy in [(-0.2, -0.25, 0.4), (0.0, 0.05, 0.45), (0.2, 0.3, 0.4)]])
        l_sig = lab("chemical signals", GREY).move_to(ov.at((3.9, 2.7)))
        ln_sig = Line(l_sig.get_left() + LEFT * 0.05, ov.at((sx + 0.6, 2.65)), color=GREY, stroke_width=2)
        self.at("chemical signals")
        self.play(FadeIn(sig), FadeIn(l_sig), Create(ln_sig), run_time=0.5)
        tube2 = tube_line(ov.tube_pts, w=16)
        self.play(Create(tube2), run_time=1.2)
        self.at("bursts into")
        tip = Circle(radius=0.3, stroke_color=PAT, stroke_width=4, fill_opacity=0).move_to(P3(*ov.tube_pts[-1]))
        self.play(FadeOut(sig), FadeOut(l_sig), FadeOut(ln_sig), Flash(tip, color=PAT, line_length=0.3, flash_radius=0.35), run_time=0.6)
        s1 = sperm(ov.at((-1.15, 2.0)), 0.18)
        s2 = sperm(ov.at((-0.95, 2.0)), 0.18)
        self.at("releases both sperm")
        self.play(s1.animate.move_to(ov.at(ov.SP1)).scale(0.32 / 0.18), s2.animate.move_to(ov.at(ov.SP2)).scale(0.32 / 0.18),
                  FadeOut(tube2), run_time=1.4)
        self.finish()


# ---------------------------------------------------------------------------------------------
def ovule_state(C, sperm_pos=True, tens=True, cc20=True):
    """rebuild the ovule at C with the sperm in place. returns (ov, sperms list, labels dict)."""
    ov = Ovule(C)
    sp1 = sperm(ov.at(ov.SP1), 0.32)
    sp2 = sperm(ov.at(ov.SP2), 0.32)
    return ov, sp1, sp2


class S03Count(SpokenScene):
    def construct(self):
        ov = Ovule(P3(0.0, -0.1))
        sp1 = sperm(ov.at(ov.SP1), 0.32)
        sp2 = sperm(ov.at(ov.SP2), 0.32)
        # same picture as the end of the last scene, then slid left to make room
        grp = VGroup(ov.base, sp1, sp2)
        self.add(grp)
        self.wait(0.8)
        self.play(grp.animate.shift(LEFT * 2.0), run_time=1.0)
        ov.C = ov.C + LEFT * 2.0
        top = chip("maize body cells: 2n = 20", TEXT, 28).move_to(P3(3.2, 3.0))
        self.at("body cells")
        self.play(FadeIn(top), run_time=0.6)
        n_egg = M("10", 26, MAT).move_to(ov.egg)
        r_egg = lab("egg: 10", MAT, 30).move_to(P3(3.2, 1.55))
        self.at("egg carries")
        self.play(FadeIn(n_egg), FadeIn(r_egg), Indicate(ov.egg, color=MAT, scale_factor=1.25), run_time=0.8)
        n_s1 = M("10", 24, TEXT).move_to(sp1)
        n_s2 = M("10", 24, TEXT).move_to(sp2)
        r_sp = lab("each sperm: 10", PAT, 30).move_to(P3(3.2, 0.45))
        self.at("each sperm")
        self.play(FadeIn(n_s1), FadeIn(n_s2), FadeIn(r_sp), Indicate(sp1, color=PAT), Indicate(sp2, color=PAT), run_time=0.8)
        cc_l = lab("central cell", MAT, 24).move_to(ov.at((0, -0.15)))
        self.at("central cell")
        self.play(Indicate(ov.cc, color=MAT, scale_factor=1.05), FadeIn(cc_l), run_time=0.7)
        n_n = [M("10", 24, TEXT).move_to(n) for n in ov.nuc]
        r_cc = lab("central cell: 10 + 10 = 20", MAT, 28).move_to(P3(3.2, -1.1))
        self.at("two polar nuclei")
        self.play(*[FadeIn(x) for x in n_n], FadeIn(r_cc), *[Indicate(n, color=MAT) for n in ov.nuc], run_time=0.9)
        n_cc = M("20", 28, MAT).move_to(ov.at((0, -1.8)))
        self.at("makes")
        self.play(FadeIn(n_cc), Indicate(r_cc, color=MAT), run_time=0.7)
        self.finish()


# ---------------------------------------------------------------------------------------------
class S04Two(SpokenScene):
    def construct(self):
        ov = Ovule(P3(-2.0, -0.1))
        sp1 = sperm(ov.at(ov.SP1), 0.32, "10")
        sp2 = sperm(ov.at(ov.SP2), 0.32, "10")
        n_egg = M("10", 26, MAT).move_to(ov.egg)
        n_n = [M("10", 24, TEXT).move_to(n) for n in ov.nuc]
        cc_l = lab("central cell", MAT, 24).move_to(ov.at((0, -0.15)))
        n_cc = M("20", 28, MAT).move_to(ov.at((0, -1.8)))
        self.add(ov.base, sp1, sp2, n_egg, cc_l, n_cc, *n_n)
        # sperm 1 -> egg
        self.at("One sperm fuses")
        self.play(sp1.animate.move_to(ov.at((-0.15, 1.5))), FadeOut(n_egg), run_time=1.0)
        e1 = eqrow([("10", MAT), ("+", TEXT), ("10", PAT), ("=", TEXT), ("20", EMB)], 42).move_to(P3(3.2, 1.9))
        self.at("makes twenty")
        zyg = Circle(radius=0.6, stroke_color=EMB, stroke_width=4, fill_color=EMB, fill_opacity=0.4).move_to(ov.egg)
        z_n = M("20", 26, TEXT).move_to(ov.egg)
        self.play(FadeIn(e1), ReplacementTransform(VGroup(ov.egg, sp1), VGroup(zyg, z_n)), run_time=0.9)
        z_l = lab("zygote, then embryo", EMB, 28).move_to(P3(3.2, 1.0))
        self.at("zygote grows")
        self.play(FadeIn(z_l), Indicate(zyg, color=EMB), run_time=0.7)
        # sperm 2 -> central cell
        self.at("other sperm")
        self.play(sp2.animate.move_to(ov.at((0, -1.0))), run_time=1.1)
        e2 = eqrow([("20", MAT), ("+", TEXT), ("10", PAT), ("=", TEXT), ("30", END)], 42).move_to(P3(3.2, -0.8))
        self.at("plus ten makes", nth=1)
        new_cc = Ellipse(width=3.2, height=2.4, stroke_color=END, stroke_width=4, fill_color=END, fill_opacity=0.22).move_to(ov.cc)
        n30 = M("30", 28, END).move_to(ov.at((0, -1.8)))
        self.play(FadeIn(e2), Transform(ov.cc, new_cc), ReplacementTransform(n_cc, n30), run_time=0.9)
        e_l = lab("first cell of the endosperm", END, 28).move_to(P3(3.2, -1.7))
        e_l2 = lab("a tissue that stores food", END, 26).move_to(P3(3.2, -2.3))
        self.at("first cell")
        self.play(FadeIn(e_l), run_time=0.6)
        self.at("stores food")
        self.play(FadeIn(e_l2), run_time=0.5)
        self.finish()


# ---------------------------------------------------------------------------------------------
def setblock(color, w=0.98, h=0.85):
    r = RoundedRectangle(corner_radius=0.12, width=w, height=h, stroke_color=color, stroke_width=3,
                         fill_color=color, fill_opacity=0.35)
    return VGroup(r, M("10", 28, TEXT).move_to(r))


class S05Sets(SpokenScene):
    def construct(self):
        ov = Ovule(P3(-2.0, -0.1))
        sp2 = sperm(ov.at((0, -1.0)), 0.32, "10")
        zyg = Circle(radius=0.6, stroke_color=EMB, stroke_width=4, fill_color=EMB, fill_opacity=0.4).move_to(ov.egg)
        z_n = M("20", 26, TEXT).move_to(ov.egg)
        ov.cc.become(Ellipse(width=3.2, height=2.4, stroke_color=END, stroke_width=4, fill_color=END, fill_opacity=0.22).move_to(ov.cc))
        n_n = [M("10", 24, TEXT).move_to(n) for n in ov.nuc]
        n30 = M("30", 28, END).move_to(ov.at((0, -1.8)))
        base = VGroup(ov.integ, ov.sac, ov.synL, ov.synR, ov.cc, *ov.nuc)
        self.add(base, zyg, z_n, sp2, *n_n, n30)

        # legend
        lg1 = VGroup(Square(0.3, stroke_width=0, fill_color=MAT, fill_opacity=0.7), lab("maternal set", MAT, 24)).arrange(RIGHT, buff=0.15)
        lg2 = VGroup(Square(0.3, stroke_width=0, fill_color=PAT, fill_opacity=0.7), lab("paternal set", PAT, 24)).arrange(RIGHT, buff=0.15)
        legend = VGroup(lg1, lg2).arrange(RIGHT, buff=0.6).move_to(P3(3.4, 3.1))

        X0 = 2.85

        def row(y, name, color, blocks):
            nm = lab(name, color, 26)
            nm.move_to(P3(0.6, y), aligned_edge=LEFT)
            bs = VGroup(*[setblock(c) for c in blocks]).arrange(RIGHT, buff=0.1)
            cont = RoundedRectangle(corner_radius=0.15, width=bs.width + 0.3, height=bs.height + 0.3, stroke_color=color,
                                    stroke_width=3, fill_opacity=0).move_to(bs)
            g = VGroup(cont, bs)
            g.move_to(P3(X0, y), aligned_edge=LEFT)
            return nm, bs, cont

        nm_e, bs_e, ct_e = row(1.75, "embryo", EMB, [MAT, PAT])
        nm_n, bs_n, ct_n = row(0.1, "endosperm", END, [MAT, MAT, PAT])
        self.at("count the sets")
        self.play(FadeIn(legend), run_time=0.6)
        self.at("The embryo has")
        self.play(FadeIn(nm_e), Create(ct_e), Indicate(zyg, color=EMB), run_time=0.6)
        self.at("one maternal set")
        self.play(FadeIn(bs_e[0], shift=DOWN * 0.15), run_time=0.5)
        self.at("one paternal set")
        self.play(FadeIn(bs_e[1], shift=DOWN * 0.15), run_time=0.5)
        self.at("The endosperm has")
        self.play(FadeIn(nm_n), Create(ct_n), Indicate(ov.cc, color=END, scale_factor=1.05), run_time=0.6)
        self.at("two maternal sets")
        self.play(FadeIn(bs_n[0], shift=DOWN * 0.15), FadeIn(bs_n[1], shift=DOWN * 0.15), run_time=0.7)
        self.at("one paternal set", nth=1)
        self.play(FadeIn(bs_n[2], shift=DOWN * 0.15), run_time=0.5)
        # seed coat
        nm_c = lab("seed coat", MAT, 26).move_to(P3(0.6, -1.6), aligned_edge=LEFT)
        ch_c = chip("maternal tissue: 20", MAT, 24).move_to(P3(X0, -1.6), aligned_edge=LEFT)
        l_int = lab("integuments", MAT, 22).move_to(P3(-5.6, -2.9))
        self.at("seed coat grows")
        self.play(FadeIn(nm_c), run_time=0.4)
        self.at("integuments")
        self.play(ov.integ.animate.set_color(MAT), FadeIn(l_int), run_time=0.7)
        self.at("own tissue")
        self.play(FadeIn(ch_c), run_time=0.6)
        self.finish()


# ---------------------------------------------------------------------------------------------
def allele(sym, color, w=1.2, h=0.95):
    r = RoundedRectangle(corner_radius=0.12, width=w, height=h, stroke_color=color, stroke_width=3,
                         fill_color=color, fill_opacity=0.35)
    return VGroup(r, M(sym, 40, TEXT, weight=BOLD).move_to(r))


class S06Xenia(SpokenScene):
    def construct(self):
        p_m = chip("seed parent: white, y y", MAT, 28).move_to(P3(-3.2, 3.0))
        p_p = chip("pollen parent: yellow, Y Y", PAT, 28).move_to(P3(3.2, 3.0))
        cross = M("x", 36, TEXT).move_to(P3(0, 3.0))
        self.at("Cross a maize plant")
        self.play(FadeIn(p_m, shift=RIGHT * 0.2), FadeIn(cross), FadeIn(p_p, shift=LEFT * 0.2), run_time=1.0)

        def mkrow(y, name, color, syms):
            nm = lab(name, color, 30).move_to(P3(-5.7, y), aligned_edge=LEFT)
            bs = VGroup(*[allele(s, c) for s, c in syms]).arrange(RIGHT, buff=0.12)
            cont = RoundedRectangle(corner_radius=0.15, width=bs.width + 0.3, height=bs.height + 0.3, stroke_color=color,
                                    stroke_width=3, fill_opacity=0).move_to(bs)
            VGroup(cont, bs).move_to(P3(-3.0, y), aligned_edge=LEFT)
            return nm, bs, cont

        nm_e, bs_e, ct_e = mkrow(1.2, "embryo", EMB, [("y", MAT), ("Y", PAT)])
        nm_n, bs_n, ct_n = mkrow(-0.5, "endosperm", END, [("y", MAT), ("y", MAT), ("Y", PAT)])
        self.at("The embryo has")
        self.play(FadeIn(nm_e), Create(ct_e), run_time=0.5)
        self.at("one white allele")
        self.play(FadeIn(bs_e[0], shift=DOWN * 0.15), run_time=0.5)
        self.at("and one yellow")
        self.play(FadeIn(bs_e[1], shift=DOWN * 0.15), run_time=0.5)
        self.at("the endosperm has")
        self.play(FadeIn(nm_n), Create(ct_n), run_time=0.5)
        self.at("two white alleles", nth=1)
        self.play(FadeIn(bs_n[0], shift=DOWN * 0.15), FadeIn(bs_n[1], shift=DOWN * 0.15), run_time=0.7)
        self.at("and one yellow", nth=1)
        self.play(FadeIn(bs_n[2], shift=DOWN * 0.15), run_time=0.5)
        # kernel
        arrow = Arrow(P3(1.2, -0.5), P3(2.6, -0.5), buff=0.05, color=END, stroke_width=5)
        kern = RoundedRectangle(corner_radius=0.3, width=1.5, height=1.5, stroke_color=END, stroke_width=4,
                                fill_color=END, fill_opacity=0.75).move_to(P3(3.6, -0.5))
        k_l = lab("yellow kernel", END, 28).next_to(kern, DOWN, buff=0.25)
        self.at("fully dominant")
        self.play(GrowArrow(arrow), FadeIn(kern, scale=0.8), FadeIn(k_l), run_time=0.9)
        note = VGroup(lab("simplified: one gene, Y fully dominant;", GREY, 22),
                      lab("real maize deepens with each Y copy", GREY, 22)).arrange(DOWN, buff=0.06).move_to(P3(-1.6, -1.7))
        self.at("dominant")
        self.play(FadeIn(note), run_time=0.5)
        x_l = chip("xenia", TEXT, 30).move_to(P3(3.6, 1.5))
        self.at("called xenia")
        self.play(FadeIn(x_l, shift=DOWN * 0.15), run_time=0.6)
        # rule
        r1 = VGroup(lab("endosperm =", END, 28), lab("2 maternal", MAT, 28), lab("+", TEXT, 28), lab("1 paternal", PAT, 28)).arrange(RIGHT, buff=0.2)
        r2 = VGroup(lab("embryo =", EMB, 28), lab("1 maternal", MAT, 28), lab("+", TEXT, 28), lab("1 paternal", PAT, 28)).arrange(RIGHT, buff=0.2)
        rule = VGroup(r1, r2).arrange(DOWN, buff=0.2, aligned_edge=LEFT).move_to(P3(0, -2.85))
        box = SurroundingRectangle(rule, color=GOLD, buff=0.2, stroke_width=3, corner_radius=0.15)
        self.at("Keep the rule")
        self.play(FadeIn(rule, shift=UP * 0.15), Create(box), run_time=0.9)
        self.finish()


class S07End(EndCard):
    LINE = "Endosperm: two maternal sets plus one paternal set."
