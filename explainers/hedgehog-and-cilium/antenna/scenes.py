"""A position becomes a place  (section film, lesson: Hedgehog and the primary cilium)

COLOR MAP (one color per concept, whole video)
  BLUE   = Patched
  PURPLE = Smoothened (tagged Smoothened has a white tag dot)
  TEAL   = intraflagellar transport proteins (the shuttle)
  YELLOW = the short stretch of Smoothened that sends it to the cilium
  GREEN  = pathway ON
  RED    = defects / altered / cannot pass the signal on
  GREY   = cell, cilium, target genes, labels, de-emphasised things
Everything is schematic and idealised, not to scale.
"""
import numpy as np
from bp_style import *  # noqa: F401,F403

PURPLE = "#B58CD9"
YT, CW = -1.1, 1.2          # cell top edge y, cilium half width


def bchip(text, color=BLUE, size=26, **kw):
    c = chip(text, color, size=size, **kw)
    back = RoundedRectangle(corner_radius=0.14, width=c[0].width, height=c[0].height, stroke_width=0,
                            fill_color=BG, fill_opacity=1).move_to(c[0])
    return VGroup(back, *c)


def ghost_chip(text, color=GREY, size=26):
    c = chip(text, color, size=size)
    box = DashedVMobject(RoundedRectangle(corner_radius=0.14, width=c[0].width, height=c[0].height), num_dashes=34).set_color(color)
    return VGroup(box, c[1])


def arr(a, b, color=GREY, w=5):
    return Arrow(a, b, buff=0.08, color=color, stroke_width=w, tip_length=0.22,
                 max_tip_length_to_length_ratio=0.45, max_stroke_width_to_length_ratio=12)


def cross(at, s=0.22, color=RED):
    at = np.array(at, float)
    return VGroup(Line(at + [-s, -s, 0], at + [s, s, 0], color=color, stroke_width=7),
                  Line(at + [-s, s, 0], at + [s, -s, 0], color=color, stroke_width=7))


def smo(tagged=True, altered=False, size=24):
    """a Smoothened chip: purple body, white tag dot, a short stretch tab on its right edge."""
    c = bchip("Smoothened", PURPLE, size=size)
    tab = RoundedRectangle(corner_radius=0.06, width=0.3, height=0.3, stroke_width=3,
                           stroke_color=RED if altered else YELLOW, fill_color=RED if altered else YELLOW,
                           fill_opacity=0.7).next_to(c, RIGHT, buff=0.0)
    parts = [c, tab]
    if tagged:
        parts.append(Dot(c.get_corner(UL) + [0.05, 0.0, 0], radius=0.11, color=TEXT))
    return VGroup(*parts)


def cell_with_cilium():
    body = RoundedRectangle(corner_radius=0.5, width=12.4, height=2.4, stroke_color=GREY, stroke_width=4).move_to([0, YT - 1.2, 0])
    patch = Rectangle(width=2 * CW - 0.06, height=0.2, stroke_width=0, fill_color=BG, fill_opacity=1).move_to([0, YT, 0])
    wl = Line([-CW, YT, 0], [-CW, 1.4, 0], color=GREY, stroke_width=4)
    wr = Line([CW, YT, 0], [CW, 1.4, 0], color=GREY, stroke_width=4)
    tip = ArcBetweenPoints([-CW, 1.4, 0], [CW, 1.4, 0], angle=-PI, color=GREY, stroke_width=4)
    return body, patch, VGroup(wl, wr, tip)


class S00Title(TitleCard):
    LESSON = "Hedgehog and the Primary Cilium"
    TITLE = "A position becomes a place"


# ---------------------------------------------------------------------------------------------
class S01Screen(SpokenScene):
    def construct(self):
        q = T("Where in the cell?", 44, font=TITLE_FONT).move_to([0, 0.4, 0])
        qm = chip("Hedgehog signalling", YELLOW, 30).move_to([0, 1.7, 0])
        self.at("Where in the cell")
        self.play(FadeIn(qm, shift=DOWN * 0.1), Write(q), run_time=1.0)

        self.at("The first clue")
        self.play(FadeOut(q), FadeOut(qm), run_time=0.4)
        lab = T("Kathryn Anderson's laboratory, 2003", 30, GREY).move_to([0, 3.0, 0])
        scr = chip("chemical mutagenesis screen", TEXT, 28).move_to([0, 2.0, 0])
        self.at("In 2003")
        self.play(FadeIn(lab), FadeIn(scr, shift=DOWN * 0.1), run_time=0.7)

        self.at("mouse mutants")
        ma = bchip("mouse mutant", GREY, 28).move_to([-3.0, 0.4, 0])
        mb = bchip("mouse mutant", GREY, 28).move_to([3.0, 0.4, 0])
        la = arr(scr.get_bottom(), ma.get_top() + UP * 0.05)
        lb = arr(scr.get_bottom(), mb.get_top() + UP * 0.05)
        self.play(GrowArrow(la), GrowArrow(lb), FadeIn(ma, shift=DOWN * 0.1), FadeIn(mb, shift=DOWN * 0.1), run_time=0.9)

        self.at("Two had defects")
        br = Brace(VGroup(ma, mb), DOWN, color=RED, buff=0.25)
        defect = T("defects in the neural tube and limbs", 30, RED).next_to(br, DOWN, buff=0.15)
        self.play(GrowFromCenter(br), FadeIn(defect, shift=UP * 0.1), run_time=0.9)

        self.at("Those defects pointed")
        res = chip("pointed to: broken Sonic hedgehog signalling", YELLOW, 28).move_to([0, -2.9, 0])
        self.play(FadeIn(res, shift=UP * 0.15), run_time=0.7)
        self.finish()


# ---------------------------------------------------------------------------------------------
class S02Shuttle(SpokenScene):
    def construct(self):
        # damaged genes -> intraflagellar transport proteins
        dg = bchip("damaged genes", RED, 28).move_to([-3.3, 2.8, 0])
        ift = bchip("intraflagellar transport proteins", TEAL, 28).move_to([2.2, 2.8, 0])
        a1 = arr(dg.get_right(), ift.get_left())
        self.at("The damaged genes encoded")
        self.play(FadeIn(dg, shift=RIGHT * 0.1), run_time=0.5)
        self.play(GrowArrow(a1), FadeIn(ift, shift=LEFT * 0.1), run_time=0.8)

        # the shuttle in a cilium
        body, patch, cil = cell_with_cilium()
        cil_l = T("primary cilium", 28, GREY).move_to([-4.0, 0.6, 0])
        self.at("That is the shuttle")
        self.play(FadeOut(dg), FadeOut(a1), ift.animate.scale(0.8).move_to([-3.2, 3.2, 0]), run_time=0.6)
        self.add(body, patch)
        self.play(Create(body), Create(cil), FadeIn(cil_l), run_time=1.0)
        shut = bchip("motor shuttle", TEAL, 24).move_to([0, YT + 0.45, 0])
        part = Square(0.34, stroke_color=GREY, stroke_width=3, fill_color=GREY, fill_opacity=0.6).next_to(shut, UP, buff=0.08)
        pl = T("part", 24, GREY).next_to(part, RIGHT, buff=0.15)
        grp = VGroup(shut, part)
        self.at("carrying parts")
        self.play(FadeIn(grp, shift=UP * 0.1), FadeIn(pl), run_time=0.5)
        self.play(grp.animate.shift(UP * 1.6), pl.animate.shift(UP * 1.6), run_time=0.8)
        self.play(grp.animate.shift(DOWN * 1.6), pl.animate.shift(DOWN * 1.6), run_time=0.8)

        # a position in a sequence
        self.at("Crosses placed")
        self.play(FadeOut(VGroup(body, cil, cil_l, grp, pl, ift)), run_time=0.5)
        hh = bchip("Patched", BLUE, 30).move_to([-4.5, 1.2, 0])
        gap = ghost_chip("intraflagellar transport", TEAL, 26).move_to([0.2, 1.2, 0])
        tg = bchip("target genes", GREY, 30).move_to([4.6, 1.2, 0])
        l1 = arr(hh.get_right(), gap.get_left(), GREY)
        l2 = arr(gap.get_right(), tg.get_left(), GREY)
        note = T("idealised: other steps not shown", 22, GREY).move_to([0, 2.5, 0])
        self.play(FadeIn(hh), FadeIn(tg), FadeIn(note), run_time=0.5)
        self.at("after Patched")
        self.play(FadeIn(gap), GrowArrow(l1), GrowArrow(l2), run_time=0.8)
        self.at("before the target genes")
        self.play(Circumscribe(tg, color=TEXT, buff=0.08), run_time=0.7)
        pos = T("a position in a sequence", 32, TEAL).move_to([0.2, 0.2, 0])
        self.at("a position in a sequence")
        self.play(FadeIn(pos, shift=DOWN * 0.1), run_time=0.6)

        cell = DashedVMobject(RoundedRectangle(corner_radius=0.5, width=8.0, height=2.0), num_dashes=60).set_color(GREY).move_to([0, -2.2, 0])
        qm = T("?", 80, GREY, weight=BOLD).move_to(cell)
        cl = T("a place in the cell", 32, GREY).move_to([0, -3.55, 0])
        self.at("not a place")
        self.play(Create(cell), FadeIn(qm), FadeIn(cl), run_time=0.9)
        self.finish()


# ---------------------------------------------------------------------------------------------
class S03Follow(SpokenScene):
    def construct(self):
        body, patch, cil = cell_with_cilium()
        cil_l = T("primary cilium", 28, GREY).move_to([-4.0, 1.8, 0])
        self.add(patch)
        self.at("The place came")
        lab = T("Kevin Corbit, Jeremy Reiter's laboratory, 2005", 30, GREY).move_to([0, 3.2, 0])
        self.play(Create(body), Create(cil), FadeIn(cil_l), FadeIn(lab), run_time=1.2)

        self.at("Kevin")
        self.play(Indicate(lab, color=TEXT, scale_factor=1.05), run_time=0.8)
        pos = [(-4.4, -1.9), (-3.0, -2.9), (3.0, -1.9), (4.3, -2.9)]
        sm = [smo().move_to([x, y, 0]) for x, y in pos]
        note = T("idealised: white dot = tag; positions for example", 22, GREY).move_to([3.0, 3.2, 0])
        self.at("followed a")
        self.play(*[FadeIn(s, scale=0.8) for s in sm], run_time=0.8)
        self.play(FadeOut(lab), FadeIn(note), run_time=0.4)

        self.at("The tag let them")
        self.play(*[Flash(s[2], color=TEXT, line_length=0.12, num_lines=8, flash_radius=0.3) for s in sm], run_time=0.8)

        lamp = chip("pathway ON", GREEN, 30).move_to([4.2, 1.0, 0])
        self.at("pathway was switched on")
        self.play(FadeIn(lamp, scale=0.8), run_time=0.5)
        self.at("collected in")
        dest = [(-0.12, -0.6), (-0.12, 0.0), (-0.12, 0.6), (-0.12, 1.2)]
        self.play(LaggedStart(*[s.animate.scale(0.68).move_to([x, y, 0]) for s, (x, y) in zip(sm, dest)],
                              lag_ratio=0.2), run_time=1.8)
        self.finish()


# ---------------------------------------------------------------------------------------------
class S04Stretch(SpokenScene):
    def construct(self):
        body, patch, cil = cell_with_cilium()
        cil_l = T("primary cilium", 28, GREY).move_to([-4.0, 1.8, 0])
        self.add(body, patch, cil, cil_l)
        # carried over from the last scene: the four tagged chips in the cilium
        dest = [(-0.12, -0.6), (-0.12, 0.0), (-0.12, 0.6), (-0.12, 1.2)]
        old = [smo().scale(0.68).move_to([x, y, 0]) for x, y in dest]
        self.add(*old)

        # one sample chip, shown large, to point at its short stretch
        sample = smo().move_to([-4.2, 0.5, 0])
        stretch_l = T("short stretch that\nsends it to the cilium", 24, YELLOW).move_to([-4.2, -0.35, 0])
        self.at("Then the group changed")
        self.play(*[FadeOut(o) for o in old], FadeIn(sample, scale=0.8), run_time=0.6)
        self.play(FadeIn(stretch_l), Circumscribe(sample[1], color=YELLOW, buff=0.1), run_time=0.8)

        al = T("changed stretch", 24, RED).move_to([-4.2, -0.35, 0])
        self.at("that sends it there")
        self.play(FadeOut(stretch_l), sample[1].animate.set_color(RED).set_fill(RED, 0.7), FadeIn(al), run_time=0.8)

        # four changed chips, tab already replaced, stay in the body (same count as before)
        pos = [(-4.4, -1.9), (-4.4, -2.9), (4.3, -1.9), (4.3, -2.9)]
        ch = [smo(altered=True).move_to([x, y, 0]) for x, y in pos]
        stay = T("stays in the body of the cell", 24, RED).move_to([0.2, -1.7, 0])
        self.at("stayed in the body")
        self.play(FadeOut(sample), FadeOut(al), *[FadeIn(c, scale=0.8) for c in ch], FadeIn(stay), run_time=0.8)

        sig = chip("signal passed on", GREEN, 28).move_to([0.2, -2.9, 0])
        ar = arr(ch[1].get_right() + [0.45, 0.0, 0], sig.get_left(), GREY)
        self.at("could no longer pass")
        self.play(FadeIn(sig), GrowArrow(ar), run_time=0.6)
        x = cross(ar.get_center(), color=RED)
        self.play(Create(x), sig.animate.set_opacity(0.35), run_time=0.6)

        self.at("lost its place")
        self.play(Indicate(stay, color=RED, scale_factor=1.1), *[Circumscribe(c, color=RED, buff=0.08) for c in ch], run_time=1.0)
        ring = Ellipse(width=3.2, height=4.0, stroke_color=TEXT, stroke_width=4).move_to([0, 0.75, 0])
        self.at("in vertebrates")
        self.play(Create(ring), run_time=0.6)
        place = T("in vertebrates:\nthe primary cilium", 30, TEXT, weight=BOLD).move_to([4.0, 2.4, 0])
        self.at("primary cilium")
        self.play(FadeIn(place, shift=DOWN * 0.1), run_time=0.6)
        self.finish()


class S05End(EndCard):
    LINE = "In vertebrates, the signal is read in the primary cilium."
