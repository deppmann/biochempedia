"""Asymmetric division: one protein makes sisters different (Biochemistrypedia explainer)

COLOR MAP (one color per concept, whole video)
  YELLOW = Numb (the crescent, and the protein in a daughter)
  TEAL   = Notch (receptor bars) and the signal passing between the sisters
  RED    = block (Numb switching Notch off in a daughter)
  VIOLET = inner fate: neuron and sheath (Notch off)
  ORANGE = outer fate: hair and socket (Notch on)
  GREY   = cells, outlines, "no Numb", unknown
"""
import numpy as np
from bp_style import *  # noqa: F401,F403

ORANGE = "#F29E4C"
VIOLET = "#A98BE0"  # inner fate, kept apart from Notch teal
CY = 0.5          # vertical centre of the cells
DX = 2.4          # daughters sit at +-DX
DR = 2.3         # daughter radius
MR = 2.8          # mother radius
SY = 0.95         # signal arrow offset from CY


def cell(c, r, color=GREY, op=0.14):
    return Circle(radius=r, stroke_color=color, stroke_width=4, fill_color=color, fill_opacity=op).move_to(c)


def crescent(center, r, span, w=14):
    return Arc(radius=r, start_angle=PI - span / 2, angle=span, arc_center=center, color=YELLOW, stroke_width=w)


def arr(a, b, color=TEAL, w=6):
    return Arrow(a, b, buff=0, color=color, stroke_width=w, tip_length=0.24,
                 max_tip_length_to_length_ratio=0.5, max_stroke_width_to_length_ratio=12)


def block(a, b, color=RED, w=6):
    a, b = np.array(a, float), np.array(b, float)
    d = (b - a) / np.linalg.norm(b - a)
    perp = np.array([-d[1], d[0], 0])
    return VGroup(Line(a, b, color=color, stroke_width=w),
                  Line(b + perp * 0.26, b - perp * 0.26, color=color, stroke_width=w + 2))


def bar(x, color=TEAL):
    return RoundedRectangle(corner_radius=0.08, width=0.26, height=1.3, stroke_color=color, stroke_width=3,
                            fill_color=color, fill_opacity=0.55).move_to([x, CY, 0])


def label(text, color, x, y, size=26):
    t = T(text, size, color)
    return t.move_to([x, y, 0])


def fate_chip(kind, x, y=-3.2):
    txt, col = ("neuron + sheath", VIOLET) if kind == "in" else ("hair + socket", ORANGE)
    return chip(txt, col, size=28).move_to([x, y, 0])


def fate(c, color):
    return c.animate.set_stroke(color).set_fill(color, 0.38)


# signal geometry
UP_A = ([-1.8, CY + SY, 0], [1.8, CY + SY, 0])      # left cell speaks, right cell hears
DN_A = ([1.8, CY - SY, 0], [-1.8, CY - SY, 0])      # right cell speaks, left cell hears


class S00Title(TitleCard):
    LESSON = "Asymmetric division: Numb"
    TITLE = "One protein makes sisters different"


def split(scene, mother, extras=(), rt=1.0):
    """stretch the mother, then cross-fade into two daughters. returns (L, R)."""
    L = cell([-DX, CY, 0], DR)
    R = cell([DX, CY, 0], DR)
    g = VGroup(mother, *extras)
    scene.play(g.animate.stretch(1.45, 0), run_time=rt * 0.5)
    scene.play(FadeOut(mother), FadeIn(L), FadeIn(R), run_time=rt * 0.5)
    return L, R


# ---------------------------------------------------------------------------------------------
class S01Question(SpokenScene):
    def construct(self):
        self.at("How does one cell")
        mother = cell([0, CY, 0], MR)
        self.play(FadeIn(mother, scale=0.9), run_time=0.7)
        self.at("sensory organ precursor")
        lab = T("sensory organ precursor, fly", 28, GREY).move_to([0, -3.2, 0])
        self.play(FadeIn(lab, shift=UP * 0.1), run_time=0.5)
        self.at("four cells")
        dots = VGroup(*[Dot(radius=0.13, color=GREY).move_to([0, CY, 0]) for _ in range(4)])
        pos = [[-0.55, CY + 0.35, 0], [0.55, CY + 0.35, 0], [-0.55, CY - 0.35, 0], [0.55, CY - 0.35, 0]]
        self.play(FadeIn(dots), run_time=0.25)
        self.play(*[d.animate.move_to(p) for d, p in zip(dots, pos)], run_time=0.6)
        self.at("It divides")
        self.play(FadeOut(dots), FadeOut(lab), run_time=0.3)
        L, R = split(self, mother, rt=0.9)
        q1 = chip("?", GREY).move_to([-DX, -3.2, 0])
        q2 = chip("?", GREY).move_to([DX, -3.2, 0])
        self.play(FadeIn(q1, shift=UP * 0.1), FadeIn(q2, shift=UP * 0.1), run_time=0.4)
        self.at("make the neuron")
        self.play(FadeOut(q1), run_time=0.15)
        a = fate_chip("in", -DX)
        self.play(FadeIn(a), fate(L, VIOLET), run_time=0.5)
        self.at("make the hair")
        self.play(FadeOut(q2), run_time=0.15)
        b = fate_chip("out", DX)
        self.play(FadeIn(b), fate(R, ORANGE), run_time=0.5)
        self.finish()


# ---------------------------------------------------------------------------------------------
class S02Crescent(SpokenScene):
    def construct(self):
        mother = cell([0, CY, 0], MR)
        self.add(mother)
        self.at("a protein called Numb")
        cres = crescent([0, CY, 0], MR, 1.8)
        nl = label("Numb", YELLOW, -5.0, CY + 1.8, 30)
        self.play(Create(cres), FadeIn(nl, shift=RIGHT * 0.15), run_time=0.8)
        self.at("It forms a crescent")
        self.play(cres.animate.set_stroke(width=22), run_time=0.4)
        self.play(cres.animate.set_stroke(width=14), run_time=0.3)
        self.at("antibody to Numb")
        ab = T("antibody stain", 24, GREY).move_to([0, -3.2, 0])
        self.play(FadeIn(ab), Flash(cres, color=YELLOW, line_length=0.3, flash_radius=2.5, num_lines=10), run_time=0.7)
        self.at("the cell divides")
        self.play(FadeOut(ab), FadeOut(nl), run_time=0.3)
        L, R = cell([-DX, CY, 0], DR), cell([DX, CY, 0], DR)
        g = VGroup(mother, cres)
        self.play(g.animate.stretch(1.45, 0), run_time=0.5)
        cres2 = crescent([-DX, CY, 0], DR, 2.0)
        self.play(FadeOut(mother), FadeIn(L), FadeIn(R), ReplacementTransform(cres, cres2), run_time=0.7)
        self.at("one daughter only")
        t1 = label("Numb", YELLOW, -DX, -2.35, 30)
        self.play(FadeIn(t1), run_time=0.4)
        self.at("gets none")
        t2 = label("no Numb", GREY, DX, -2.35, 30)
        self.play(FadeIn(t2), run_time=0.4)
        self.finish()


# ---------------------------------------------------------------------------------------------
class S03Notch(SpokenScene):
    def construct(self):
        L, R = cell([-DX, CY, 0], DR), cell([DX, CY, 0], DR)
        cres = crescent([-DX, CY, 0], DR, 2.0)
        t1 = label("Numb", YELLOW, -DX, -2.35, 30)
        t2 = label("no Numb", GREY, DX, -2.35, 30)
        self.add(L, R, cres, t1, t2)
        self.at("act on")
        self.play(Indicate(VGroup(cres, t1), color=YELLOW, scale_factor=1.15), run_time=0.8)
        self.at("is a receptor")
        bl, br = bar(-0.32), bar(0.32)
        nl = T("Notch", 28, TEAL).move_to([0, CY + 1.9, 0])
        self.play(FadeIn(bl), FadeIn(br), FadeIn(nl, shift=DOWN * 0.1), run_time=0.7)
        self.at("it is cut")
        self.play(Indicate(VGroup(bl, br), color=TEAL, scale_factor=1.2), run_time=0.7)
        self.at("two sisters touch")
        aU, aD = arr(*UP_A), arr(*DN_A)
        self.play(GrowArrow(aU), GrowArrow(aD), run_time=0.7)
        self.at("each could signal")
        self.play(Indicate(VGroup(aU, aD), color=TEAL, scale_factor=1.08), run_time=0.8)
        self.at("off Notch")
        blk = block(*DN_A)
        self.play(ReplacementTransform(aD, blk), bl.animate.set_stroke(GREY).set_fill(GREY, 0.3), run_time=0.7)
        self.wait(0.1)
        self.finish()


# ---------------------------------------------------------------------------------------------
class S04Fates(SpokenScene):
    def construct(self):
        L, R = cell([-DX, CY, 0], DR), cell([DX, CY, 0], DR)
        cres = crescent([-DX, CY, 0], DR, 2.0)
        t1 = label("Numb", YELLOW, -DX, -2.35, 30)
        t2 = label("no Numb", GREY, DX, -2.35, 30)
        bl = bar(-0.32, GREY)
        bl.set_fill(GREY, 0.3)
        br = bar(0.32)
        aU = arr(*UP_A)
        blk = block(*DN_A)
        self.add(L, R, cres, t1, t2, bl, br, aU, blk)
        self.at("cannot hear")
        self.play(Indicate(blk, color=RED, scale_factor=1.15), run_time=0.7)
        self.at("Its sister can")
        self.play(Indicate(VGroup(aU, br), color=TEAL, scale_factor=1.12), run_time=0.7)
        self.at("takes the Notch on")
        self.play(fate(R, ORANGE), run_time=0.6)
        self.at("makes the hair")
        cb = fate_chip("out", DX)
        self.play(FadeIn(cb, shift=UP * 0.1), run_time=0.5)
        self.at("takes the Notch off")
        self.play(fate(L, VIOLET), run_time=0.6)
        self.at("makes the neuron")
        ca = fate_chip("in", -DX)
        self.play(FadeIn(ca, shift=UP * 0.1), run_time=0.5)
        self.at("private veto")
        v = T("a private veto", 28, RED).move_to([0, 3.3, 0])
        self.play(FadeIn(v, shift=DOWN * 0.1), Indicate(blk, color=RED, scale_factor=1.2), run_time=0.7)
        self.finish()


# ---------------------------------------------------------------------------------------------
class S05Tests(SpokenScene):
    def construct(self):
        L, R = cell([-DX, CY, 0], DR), cell([DX, CY, 0], DR)
        bl, br = bar(-0.32), bar(0.32)
        aU, aD = arr(*UP_A), arr(*DN_A)
        nl = T("Notch", 28, TEAL).move_to([0, CY + 1.9, 0])
        t1 = label("Numb", YELLOW, -DX, -2.35, 30)
        t2 = label("no Numb", GREY, DX, -2.35, 30)
        cres = crescent([-DX, CY, 0], DR, 2.0)
        # start from the end of the last scene, neutral cells
        bl.set_stroke(GREY).set_fill(GREY, 0.3)
        blk = block(*DN_A)
        self.add(L, R, bl, br, aU, blk, nl, cres, t1, t2)
        self.at("Now test the idea")
        # clear the old answer: reset to a neutral rig with no labels on the fates
        # (done with the case-one label in the same animation)
        self.at("Remove Numb")
        case1 = T("Case 1: no Numb", 32, GREY, weight=BOLD).move_to([0, 3.3, 0])
        self.play(FadeOut(cres), FadeOut(t1), FadeOut(t2), FadeOut(blk), FadeIn(case1, shift=DOWN * 0.1), run_time=0.6)
        no1 = label("no Numb", GREY, -DX, -2.35, 30)
        no2 = label("no Numb", GREY, DX, -2.35, 30)
        self.play(FadeIn(no1), FadeIn(no2), run_time=0.3)
        self.at("nothing blocks Notch")
        self.play(GrowArrow(aD), bl.animate.set_stroke(TEAL).set_fill(TEAL, 0.55), run_time=0.7)
        self.at("take the outer fate")
        self.play(fate(L, ORANGE), fate(R, ORANGE), run_time=0.7)
        self.at("outer support cells")
        ca, cb = fate_chip("out", -DX), fate_chip("out", DX)
        self.play(FadeIn(ca, shift=UP * 0.1), FadeIn(cb, shift=UP * 0.1), run_time=0.5)
        self.at("give Numb to both")
        # reset every result in the same animation that brings in case two
        case2 = T("Case 2: Numb in both", 32, YELLOW, weight=BOLD).move_to([0, 3.3, 0])
        cl = crescent([-DX, CY, 0], DR, 2.0)
        cr = Arc(radius=DR, start_angle=-1.0, angle=2.0, arc_center=[DX, CY, 0], color=YELLOW, stroke_width=14)
        n1 = label("Numb", YELLOW, -DX, -2.35, 30)
        n2 = label("Numb", YELLOW, DX, -2.35, 30)
        self.play(FadeOut(case1), FadeIn(case2), FadeOut(ca), FadeOut(cb), FadeOut(no1), FadeOut(no2),
                  L.animate.set_stroke(GREY).set_fill(GREY, 0.14), R.animate.set_stroke(GREY).set_fill(GREY, 0.14),
                  Create(cl), Create(cr), FadeIn(n1), FadeIn(n2), run_time=0.8)
        self.at("Neither can hear")
        bU, bD = block(*UP_A), block(*DN_A)
        self.play(ReplacementTransform(aU, bU), ReplacementTransform(aD, bD),
                  bl.animate.set_stroke(GREY).set_fill(GREY, 0.3), br.animate.set_stroke(GREY).set_fill(GREY, 0.3),
                  run_time=0.7)
        self.at("take the inner fate")
        self.play(fate(L, VIOLET), fate(R, VIOLET), run_time=0.7)
        self.at("make neurons")
        ca, cb = fate_chip("in", -DX), fate_chip("in", DX)
        self.play(FadeIn(ca, shift=UP * 0.1), FadeIn(cb, shift=UP * 0.1), run_time=0.5)
        self.finish()


# ---------------------------------------------------------------------------------------------
class S06Rule(SpokenScene):
    def construct(self):
        mother = cell([0, CY, 0], MR)
        self.add(mother)
        self.at("whole mechanism")
        self.wait(0.2)
        self.at("gathers on one side")
        cres = crescent([0, CY, 0], MR, 1.8)
        self.play(Create(cres), run_time=0.8)
        self.at("hands it to one daughter")
        L, R = cell([-DX, CY, 0], DR), cell([DX, CY, 0], DR)
        self.play(VGroup(mother, cres).animate.stretch(1.45, 0), run_time=0.5)
        cres2 = crescent([-DX, CY, 0], DR, 2.0)
        self.play(FadeOut(mother), FadeIn(L), FadeIn(R), ReplacementTransform(cres, cres2), run_time=0.7)
        self.at("blocks Notch")
        bl, br = bar(-0.32, GREY), bar(0.32)
        bl.set_fill(GREY, 0.3)
        aU = arr(*UP_A)
        blk = block(*DN_A)
        bt = T("Numb blocks", 24, RED).move_to([-2.2, CY - SY - 0.5, 0])
        self.play(FadeIn(bl), FadeIn(br), FadeIn(blk), FadeIn(bt), run_time=0.6)
        self.at("sister still hears")
        self.play(GrowArrow(aU), fate(R, ORANGE), run_time=0.7)
        self.play(fate(L, VIOLET), run_time=0.5)
        self.at("Remember the rule")
        rule = T("Numb to one daughter only: the sisters differ", 30, TEXT).move_to([0, -3.1, 0])
        self.play(FadeIn(rule, shift=UP * 0.1), run_time=0.6)
        self.finish()


class S07End(EndCard):
    LINE = "Numb goes to one daughter only, so the sisters differ."
