"""Drugs against a part, section film: a bond to the mutation itself (Biochemistrypedia explainer)

Timed to the SPOKEN words: every self.at("...") cue waits for that phrase in audio/words.json.

COLOR MAP (one color per concept, whole video)
  BLUE   = Ras (the protein)
  YELLOW = GTP (the nucleotide the cell holds in vast excess)
  TEAL   = GDP
  PURPLE = the cysteine / glycine at position 12 (the residue and its thiol)
  ORANGE = the small molecule: competitor, fragments, the compound, sotorasib
  GREY   = outlines, Raf, neutral labels
  RED    = blocked / not possible
"""
import numpy as np
from bp_style import *  # noqa: F401,F403

PURPLE = "#B58CD9"
ORANGE = "#F29E4C"


def rr(t, ph=0.0):
    return 1 + 0.05 * np.sin(3 * t + ph) + 0.04 * np.cos(2 * t + 1)


def surf(c, R, ang, k=1.0, ph=0.0):
    t = np.radians(ang)
    r = rr(t, ph) * k
    return np.array([c[0] + R * r * 1.1 * np.cos(t), c[1] + R * r * 0.95 * np.sin(t), 0])


def blob(c, R, ph=0.0):
    f = ParametricFunction(lambda t: surf(c, R, np.degrees(t), 1.0, ph), t_range=[0, TAU], stroke_color=BLUE,
                           stroke_width=4, fill_color=BLUE, fill_opacity=0.16)
    return f


def bchip(text, color=BLUE, size=24, **kw):
    c = chip(text, color, size=size, **kw)
    back = RoundedRectangle(corner_radius=0.14, width=c[0].width, height=c[0].height, stroke_width=0,
                            fill_color=BG, fill_opacity=1).move_to(c[0])
    return VGroup(back, *c)


def sh_badge(pos, up=None):
    dirv = up if up is not None else UP
    stalk = Line(pos, pos + dirv * 0.45, color=PURPLE, stroke_width=5)
    b = Circle(radius=0.3, stroke_color=PURPLE, stroke_width=3, fill_color=BG, fill_opacity=1)
    b.move_to(pos + dirv * 0.75)
    t = T("SH", 22, PURPLE, weight=BOLD).move_to(b)
    return VGroup(stalk, b, t)


def note(text, color=TEXT, pos=(3.3, 2.6), size=26):
    return T(text, size, color, line_spacing=0.9).move_to([pos[0], pos[1], 0])


def schem():
    return T("schematic, not to scale", 22, GREY).move_to([-4.6, -3.55, 0])


class S00Title(TitleCard):
    LESSON = "Drugs Against a Part"
    TITLE = "A Bond to the Mutation Itself"


# --------------------------------------------------------------------------------------------
class S01Tight(SpokenScene):
    def construct(self):
        C, R = np.array([-3.9, -0.2, 0]), 2.2
        ras = blob(C, R)
        lab = T("Ras", 36, BLUE, weight=BOLD).move_to(C + UP * 1.2)
        flag = chip("undruggable target", RED, size=24).move_to([-3.9, 2.95, 0])
        self.add(schem())
        self.at("standard example")
        self.play(FadeIn(ras, scale=0.9), FadeIn(lab), run_time=0.8)
        self.play(FadeIn(flag, shift=DOWN * 0.15), run_time=0.6)

        gtp = bchip("GTP", YELLOW, size=26).move_to([2.2, -2.6, 0])
        site = C + DOWN * 0.1
        grips = VGroup(*[Line(site + np.array([dx, -0.5 * s, 0]), site + np.array([dx, -0.2 * s, 0]),
                              color=YELLOW, stroke_width=4) for dx in (-0.5, 0.5) for s in (1,)])
        self.at("picomolar affinity")
        self.play(gtp.animate.move_to(site), run_time=0.9)
        self.play(FadeIn(grips), run_time=0.3)
        held = T("held: picomolar affinity", 24, YELLOW).move_to([-3.9, -2.9, 0])
        self.play(FadeIn(held, shift=UP * 0.1), run_time=0.4)

        crowd = VGroup(*[bchip("GTP", YELLOW, size=22).move_to([x, y, 0]) for x in (2.7, 4.0, 5.3)
                         for y in (2.0, 1.2, 0.4, -0.4, -1.2)])
        clab = T("the cell: near the millimolar range", 24, YELLOW).move_to([4.0, 2.95, 0])
        self.at("millimolar range")
        self.play(LaggedStart(*[FadeIn(g, scale=0.8) for g in crowd], lag_ratio=0.06), FadeIn(clab), run_time=1.6)

        comp = bchip("competitor", ORANGE, size=22).move_to([-0.2, 0.0, 0])
        self.at("competitor for that site")
        self.play(FadeIn(comp, shift=LEFT * 0.2), run_time=0.5)
        self.play(comp.animate.shift(LEFT * 0.25), run_time=0.4)
        self.play(comp.animate.shift(RIGHT * 0.35), run_time=0.3)
        self.at("vast excess")
        self.play(Indicate(crowd, color=YELLOW, scale_factor=1.05), run_time=1.0)

        nog = T("no deep groove", 26, RED).move_to([4.0, -2.7, 0])
        self.at("no groove")
        self.play(Indicate(ras, color=BLUE, scale_factor=1.03), FadeIn(nog), run_time=1.0)
        self.finish()


# --------------------------------------------------------------------------------------------
class S02Cysteine(SpokenScene):
    def construct(self):
        C, R = np.array([-0.8, -0.2, 0]), 2.7
        ras = blob(C, R)
        lab = T("Ras", 40, BLUE, weight=BOLD).move_to(C + DOWN * 0.2)
        self.add(ras, lab, schem())
        p = surf(C, R, 50)
        site = Dot(p, radius=0.17, color=PURPLE)
        gly_l = bchip("Gly 12", PURPLE, size=26).move_to([4.3, 2.9, 0])
        gline = Line(gly_l.get_left(), p + RIGHT * 0.2, color=PURPLE, stroke_width=2)
        self.at("laboratory went at")
        self.play(FadeIn(site, scale=2), FadeIn(gly_l), Create(gline), run_time=0.7)

        nos = T("no side chain", 26, GREY).move_to([4.3, 2.05, 0])
        self.at("has no")
        self.play(FadeIn(nos, shift=DOWN * 0.1), run_time=0.5)

        cys_l = bchip("Cys 12", PURPLE, size=26).move_to(gly_l)
        mut = T("one cancer mutation", 26, RED).move_to([4.3, 2.05, 0])
        self.at("One cancer mutation")
        self.play(FadeOut(nos), FadeIn(mut, shift=DOWN * 0.1), run_time=0.4)
        self.at("replaces it with cysteine")
        self.play(Transform(gly_l, cys_l), run_time=0.8)
        stalk = sh_badge(p, up=np.array([0.6, 0.8, 0]))
        self.at("That puts a thiol")
        self.play(Create(stalk[0]), FadeIn(stalk[1:], scale=0.5), run_time=0.8)
        thi = T("a thiol:\na reactive\nsulphur-hydrogen group", 24, PURPLE, line_spacing=0.9).move_to([4.4, -0.1, 0])
        thline = Line(stalk[1].get_right() + DOWN * 0.1, thi.get_top() + UP * 0.1, color=PURPLE, stroke_width=2)
        self.at("surface of the protein")
        self.play(Indicate(stalk[1:], color=PURPLE, scale_factor=1.2), run_time=0.8)
        self.at("a reactive")
        self.play(FadeIn(thi, shift=UP * 0.1), run_time=0.8)
        self.finish()


# --------------------------------------------------------------------------------------------
class S03Screen(SpokenScene):
    def construct(self):
        C, R = np.array([-3.6, 0.5, 0]), 1.9
        ras = blob(C, R)
        lab = T("Ras", 34, BLUE, weight=BOLD).move_to(C + UP * 0.5)
        gdp = bchip("GDP", TEAL if False else "#3FB8C0", size=24).move_to(C + DOWN * 0.7)
        p = surf(C, R, 40)
        sh = sh_badge(p, up=np.array([0.6, 0.8, 0]))
        cap = T("purified K-Ras G12C, GDP-bound", 24, TEXT).move_to([-3.6, -1.9, 0])
        self.add(schem())
        self.at("The group held")
        self.play(FadeIn(ras, scale=0.95), FadeIn(lab), FadeIn(gdp), FadeIn(sh), run_time=0.8)
        self.play(FadeIn(cap), run_time=0.4)

        dots = VGroup(*[Dot([2.0 + 0.16 * i, 2.8 - 0.13 * j, 0], radius=0.055, color=ORANGE)
                        for i in range(24) for j in range(20)])
        dots.move_to([3.6, 1.65, 0])
        dl = T("480 sulphur-seeking fragments", 24, ORANGE).move_to([3.6, 0.0, 0])
        self.at("480")
        self.play(FadeIn(dots, lag_ratio=0.002), FadeIn(dl), run_time=1.5)

        self.at("over it")
        self.play(dots.animate.shift(LEFT * 0.25).set_opacity(0.55), run_time=0.8)

        beam = Line(LEFT * 0.9, RIGHT * 0.9, color=GREY, stroke_width=5)
        post = Polygon([-0.25, -0.65, 0], [0.25, -0.65, 0], [0, 0, 0], color=GREY, stroke_width=3, fill_color=GREY, fill_opacity=0.4)
        pans = VGroup(Line(LEFT * 0.9, LEFT * 0.9 + DOWN * 0.4, color=GREY, stroke_width=3),
                      Line(RIGHT * 0.9, RIGHT * 0.9 + DOWN * 0.4, color=GREY, stroke_width=3))
        bal = VGroup(post, beam, pans).move_to([3.6, -1.5, 0])
        wl = T("weigh the protein", 24, GREY).move_to([3.6, -2.8, 0])
        self.at("weighed the protein")
        self.play(FadeIn(bal), FadeIn(wl), run_time=0.6)
        self.play(Rotate(VGroup(beam, pans), angle=-0.15, about_point=beam.get_center()), run_time=0.8)

        two = [dots[137], dots[262]]
        big = VGroup(*[Dot(d.get_center(), radius=0.2, color=ORANGE) for d in two])
        res = T("two fragments:\nattached to most\nof the protein", 24, ORANGE, line_spacing=0.9).move_to([3.6, 0.0, 0])
        self.at("Two fragments attached")
        self.play(FadeOut(dots), FadeOut(dl), FadeOut(bal), FadeOut(wl), run_time=0.5)
        big.move_to([3.6, 2.0, 0]).arrange(RIGHT, buff=0.8).move_to([3.6, 2.0, 0])
        self.play(FadeIn(big, scale=0.4), FadeIn(res), run_time=0.7)
        self.play(big.animate.set_color(ORANGE), run_time=0.2)
        b0 = Line(big[0].get_bottom(), sh[1].get_right() + RIGHT * 0.0, color=ORANGE, stroke_width=0)  # unused anchor
        self.wait(0.3)

        # normal K-Ras: reset the right half, then show the contrast
        NC = np.array([3.4, 0.5, 0])
        nras = blob(NC, R, ph=1.3)
        nlab = T("Ras", 34, BLUE, weight=BOLD).move_to(NC + UP * 0.9)
        cys = VGroup(*[bchip("Cys", PURPLE, size=22).move_to(NC + off) for off in
                       (np.array([-1.0, -0.6, 0]), np.array([0.2, -0.9, 0]), np.array([1.0, 0.1, 0]))])
        ncap = T("normal K-Ras", 24, TEXT).move_to([3.4, -1.9, 0])
        self.at("Normal")
        self.play(FadeOut(big), FadeOut(res), run_time=0.4)
        self.play(FadeIn(nras, scale=0.95), FadeIn(nlab), FadeIn(ncap), run_time=0.6)
        three = T("three cysteines elsewhere", 24, PURPLE).move_to([3.4, 2.95, 0])
        self.at("three cysteines")
        self.play(FadeIn(cys, scale=0.7, lag_ratio=0.3), FadeIn(three), run_time=1.0)
        frag = Dot([0.5, 1.7, 0], radius=0.17, color=ORANGE)
        none = T("no detectable reaction", 26, RED).move_to([3.4, -2.8, 0])
        self.at("no detectable reaction")
        self.play(FadeIn(frag), run_time=0.2)
        self.play(frag.animate.move_to(cys[2].get_center() + UP * 0.9 + RIGHT * 0.9), run_time=0.5)
        self.play(frag.animate.shift(RIGHT * 0.7 + UP * 0.4), FadeIn(none), run_time=0.5)
        self.finish()


# --------------------------------------------------------------------------------------------
class S04Bond(SpokenScene):
    def construct(self):
        C, R = np.array([-3.0, -0.3, 0]), 2.5
        ras = blob(C, R)
        lab = T("K-Ras G12C", 28, BLUE, weight=BOLD).move_to(C + np.array([-1.0, 1.2, 0]))
        cys = bchip("Cys 12", PURPLE, size=22).move_to(C + np.array([1.0, 1.2, 0]))
        gdp = bchip("GDP", "#3FB8C0", size=24).move_to(C + np.array([-0.9, -1.6, 0]))
        self.add(schem())
        self.at("crystal structure")
        self.play(FadeIn(ras, scale=0.95), FadeIn(lab), FadeIn(cys), FadeIn(gdp), run_time=0.8)

        pocket = DashedVMobject(RoundedRectangle(corner_radius=0.3, width=2.7, height=1.1, stroke_color=ORANGE,
                                                 stroke_width=3), num_dashes=30).move_to(C + np.array([1.0, -0.2, 0]))
        comp = bchip("compound", ORANGE, size=22).move_to(pocket)
        bond = Line(cys.get_bottom(), comp.get_top(), color=ORANGE, stroke_width=8)
        loop = ParametricFunction(lambda t: surf(C, R, t * 1.0, 1.0), t_range=[18, 70], stroke_color=BLUE, stroke_width=11)
        loopl = T("switch II loop", 24, BLUE).move_to([-1.6, 2.85, 0])
        self.at("pocket beneath")
        self.play(Create(loop), FadeIn(loopl), run_time=0.7)
        self.play(Create(pocket), FadeIn(comp), run_time=0.8)
        self.play(Create(bond), run_time=0.4)

        n1 = note("a pocket no earlier\nRas structure had shown", ORANGE, pos=(3.9, 0.3))
        self.at("no earlier Ras structure")
        self.play(FadeIn(n1, shift=DOWN * 0.1), run_time=0.6)

        self.at("Once bonded")
        self.play(Indicate(bond, color=ORANGE, scale_factor=1.3), run_time=0.8)
        n2 = note("tilts Ras toward\nholding GDP", "#3FB8C0", pos=(3.9, -1.9))
        self.at("tilts Ras")
        self.play(FadeIn(n2, shift=DOWN * 0.1), Indicate(gdp, color="#3FB8C0", scale_factor=1.15), run_time=0.9)

        raf = bchip("Raf", GREY, size=26).move_to([3.0, 1.7, 0])
        self.at("gets in the way")
        self.play(raf.animate.move_to([0.9, 1.5, 0]), run_time=0.8)
        stop = inhibx = VGroup(Line(UP * 0.3, DOWN * 0.3, color=RED, stroke_width=8)).move_to([0.0, 1.5, 0])
        self.play(FadeIn(stop), run_time=0.3)
        self.wait(0.2)

        # clear stage: keep the protein, bring in the GTP crowd for the bond point
        self.at("bond lasts")
        self.play(FadeOut(n1), FadeOut(n2), FadeOut(raf), FadeOut(stop), run_time=0.4)
        n3 = note("the bond lasts for the life\nof that protein molecule", ORANGE, pos=(3.9, 2.9), size=24)
        self.play(FadeIn(n3), Indicate(bond, color=ORANGE, scale_factor=1.3), run_time=0.8)
        crowd = VGroup(*[bchip("GTP", YELLOW, size=22).move_to([x, y, 0]) for x in (2.8, 4.2, 5.6)
                         for y in (0.9, 0.0, -0.9)])
        self.at("never has to")
        self.play(LaggedStart(*[FadeIn(g, scale=0.8) for g in crowd], lag_ratio=0.05), run_time=1.0)
        self.play(Indicate(crowd, color=YELLOW, scale_factor=1.05), run_time=0.8)

        sot = bchip("sotorasib", ORANGE, size=22).move_to(comp)
        n4 = note("sotorasib: reported in 2019\nby Canon and colleagues,\na drug for patients", ORANGE, pos=(3.9, -2.2), size=24)
        self.at("and colleagues reported")
        self.play(FadeOut(crowd), FadeOut(n3), run_time=0.4)
        self.play(FadeIn(n4), run_time=0.5)
        self.at("a drug for patients")
        self.play(Transform(comp, sot), run_time=0.7)
        self.at("same cysteine")
        self.play(Indicate(VGroup(cys, bond), color=PURPLE, scale_factor=1.15), run_time=1.0)

        rule = T("Bond to a residue only the mutant has.", 38, TEXT, font=TITLE_FONT)
        fit(rule, max_w=11.5)
        self.at("Keep this rule")
        self.play(FadeOut(VGroup(ras, lab, cys, gdp, loop, loopl, pocket, comp, bond, n4)), run_time=0.5)
        self.play(FadeIn(rule, shift=UP * 0.15), run_time=0.8)
        self.finish()


class S05End(EndCard):
    LINE = "Bond to a residue only the mutant has."
