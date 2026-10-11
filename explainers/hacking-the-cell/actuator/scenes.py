"""Hacking the cell, section film: an actuator, light in, current out  (Biochemistrypedia)

COLOR MAP (one color per concept, whole film)
  BLUE   = channelrhodopsin-2 and the blue light that opens it
  PURPLE = rhodopsin and its G protein relay
  GOLD   = retinal
  WHITE  = cations (plain dots)
  TEAL   = dates and the timeline
  GREEN  = the neuron fires (action potentials)
  RED    = crossed out (the relay that is skipped)
  GREY   = membrane, labels
No molecular structures: the proteins are labelled blocks in a membrane bar.
"""
import numpy as np
from bp_style import *  # noqa: F401,F403

PURPLE = "#B58CD9"


def arr(a, b, color=GREY, w=5, tip=0.2):
    return Arrow(a, b, buff=0.06, color=color, stroke_width=w, tip_length=tip,
                 max_tip_length_to_length_ratio=0.45, max_stroke_width_to_length_ratio=12)


def membrane(x0, x1, y=0.0, h=0.3):
    return Rectangle(width=x1 - x0, height=h, stroke_color=GREY, stroke_width=2,
                     fill_color=GREY, fill_opacity=0.35).move_to([(x0 + x1) / 2, y, 0])


def prot(label, color, x, y, w=2.8, h=2.0, size=26, lshift=0.0):
    box = RoundedRectangle(corner_radius=0.16, width=w, height=h, stroke_color=color, stroke_width=3,
                           fill_color=color, fill_opacity=0.18).move_to([x, y, 0])
    back = RoundedRectangle(corner_radius=0.16, width=w, height=h, stroke_width=0, fill_color=BG,
                            fill_opacity=1).move_to(box)
    lbl = T(label, size, color).move_to(box.get_top() + DOWN * 0.38 + RIGHT * lshift)
    g = VGroup(back, box, lbl)
    g.box, g.lbl = box, lbl
    return g


def retinal(x, y):
    return chip("retinal", GOLD, size=22, pad=0.14).move_to([x, y, 0])


def strike(m, color=RED):
    return Line(m.get_corner(DL) + [-0.08, -0.04, 0], m.get_corner(UR) + [0.08, 0.04, 0], color=color, stroke_width=7)


def timeline(with_2005=False, y=-3.1):
    xs = {2002: -4.6, 2003: -3.1, 2005: 0.0}
    line = Line([-5.8, y, 0], [5.8 if with_2005 else -1.2, y, 0], color=GREY, stroke_width=4)
    g = VGroup(line)
    for yr in ([2002, 2003] + ([2005] if with_2005 else [])):
        tk = Line([xs[yr], y - 0.12, 0], [xs[yr], y + 0.12, 0], color=TEAL, stroke_width=4)
        lb = T(str(yr), 24, TEAL).next_to(tk, DOWN, buff=0.08)
        g.add(tk, lb)
    return g, xs


class S00Title(TitleCard):
    LESSON = "Hacking the Cell"
    TITLE = "Light in, current out"


class S01Skip(SpokenScene):
    def construct(self):
        LX, RX = -3.4, 3.4
        mem = membrane(-6.2, 6.2, -0.2)
        self.play(FadeIn(mem), run_time=0.4)
        self.at("you met rhodopsin")
        rh = prot("rhodopsin", PURPLE, LX, -0.2, h=2.2)
        self.play(FadeIn(rh), run_time=0.5)
        self.at("seven helices")
        hel = T("seven helices", 24, GREY).next_to(rh, UP, buff=0.12)
        ret = retinal(LX, -0.55)
        self.play(FadeIn(hel), FadeIn(ret), run_time=0.5)
        self.at("absorbs a photon")
        ph = arr([LX, 3.3, 0], [LX, 1.2, 0], BLUE, 6)
        phl = T("photon", 24, BLUE).next_to(ph, RIGHT, buff=0.15)
        self.play(GrowArrow(ph), FadeIn(phl), hel.animate.set_opacity(0), run_time=0.5)
        self.play(Indicate(ret, color=YELLOW, scale_factor=1.25), run_time=0.5)
        self.at("sets off")
        gp = chip("G protein", PURPLE, size=26).move_to([LX, -2.4, 0])
        a1 = arr([LX, -1.5, 0], gp.get_top() + UP * 0.05, PURPLE, 5)
        self.play(GrowArrow(a1), FadeIn(gp), run_time=0.5)
        self.at("skip the relay")
        ghost = chip("G protein", GREY, size=26).move_to([RX, -2.4, 0])
        ghost.set_opacity(0.45)
        nr = T("no relay", 24, RED).next_to(ghost, DOWN, buff=0.1)
        self.play(FadeIn(ghost), FadeOut(ph), FadeOut(phl), run_time=0.3)
        self.play(Create(strike(ghost)), FadeIn(nr), run_time=0.4)
        self.at("from a green alga")
        ch = prot("channelrhodopsin-2", BLUE, RX, -0.2, w=4.0, h=2.2, size=24, lshift=-0.35)
        alga = T("from a green alga", 24, GREY).next_to(ch, UP, buff=0.12)
        self.play(FadeIn(ch), FadeIn(alga), run_time=0.5)
        self.at("itself an ion channel")
        r2 = retinal(RX - 0.8, -0.55)
        pore = Rectangle(width=0.3, height=2.2, stroke_width=0, fill_color=BG, fill_opacity=1).move_to([RX + 1.6, -0.2, 0])
        pl = T("pore", 22, BLUE).next_to(pore, DOWN, buff=0.1).shift(UP * 0.0)
        tag = chip("itself an ion channel", BLUE, size=24).move_to([RX, 2.25, 0])
        self.play(FadeOut(alga), FadeIn(r2), FadeIn(pore), run_time=0.4)
        self.play(FadeIn(tag), run_time=0.4)
        self.finish()


class S02Open(SpokenScene):
    def construct(self):
        CX = -3.2
        mem = VGroup(membrane(-6.3, CX - 1.8, 0), membrane(CX + 1.8, -0.1, 0))
        ch = prot("channelrhodopsin-2", BLUE, CX, 0, w=3.6, h=2.4, size=22, lshift=-0.3)
        ret = retinal(CX - 0.7, -0.5)
        pore = Rectangle(width=0.12, height=2.4, stroke_width=0, fill_color=BG, fill_opacity=1).move_to([CX + 1.4, 0, 0])
        poreline = Line([CX + 1.4, -1.2, 0], [CX + 1.4, 1.2, 0], color=BLUE, stroke_width=2)
        out = T("outside", 22, GREY).move_to([-5.7, 0.6, 0])
        ins = T("inside the neuron", 22, GREY).move_to([-5.0, -2.0, 0])
        self.add(mem)
        self.play(FadeIn(ch), FadeIn(ret), FadeIn(pore), FadeIn(poreline), FadeIn(out), FadeIn(ins), run_time=0.2)
        self.at("shine blue light")
        bl = arr([CX, 3.4, 0], [CX, 1.4, 0], BLUE, 7)
        bll = T("blue light", 24, BLUE).next_to(bl, LEFT, buff=0.15)
        self.play(GrowArrow(bl), FadeIn(bll), run_time=0.5)
        self.at("changes its retinal")
        self.play(Indicate(ret, color=YELLOW, scale_factor=1.3), run_time=0.6)
        self.at("pore opens")
        ms = T("within milliseconds", 22, BLUE).move_to([CX - 0.6, -2.7, 0])
        pore2 = Rectangle(width=0.5, height=2.4, stroke_width=0, fill_color=BG, fill_opacity=1).move_to([CX + 1.4, 0, 0])
        self.play(FadeOut(poreline), Transform(pore, pore2), FadeIn(ms), run_time=0.5)
        self.at("cations flow")
        dots = VGroup(*[Dot(radius=0.09, color=WHITE).move_to([CX + 1.4, 2.2 + 0.0 * i, 0]) for i in range(3)])
        cl = T("cations", 22, WHITE).move_to([CX + 2.2, 1.9, 0])
        self.add(dots)
        self.play(FadeIn(cl), *[d.animate.move_to([CX + 1.4 + (i - 1) * 0.3, -1.6 - 0.4 * i, 0]) for i, d in enumerate(dots)],
                  run_time=0.9, lag_ratio=0.3)
        more = VGroup(*[Dot(radius=0.09, color=WHITE).move_to([CX + 1.4 + dx, 2.0, 0]) for dx in (-0.12, 0.12, 0.0)])
        self.play(*[d.animate.move_to([CX + 1.4 + dx * 2.5, -1.8 - 0.4 * k, 0]) for d, dx, k in zip(more, (-0.12, 0.12, 0.0), range(3))],
                  run_time=0.8, lag_ratio=0.3)
        self.at("depolarizes")
        base, thr = -1.2, 0.5
        lab = T("membrane voltage", 22, GREY).move_to([3.4, 2.6, 0])
        axis = Line([0.9, base, 0], [6.1, base, 0], color=GREY, stroke_width=3)
        dash = DashedLine([0.9, thr, 0], [6.1, thr, 0], color=GREY, stroke_width=3)
        rise = VMobject(color=YELLOW, stroke_width=5).set_points_smoothly(
            [[0.9, base, 0], [1.9, base, 0], [2.6, base + 0.5, 0], [3.3, base + 1.1, 0], [3.8, thr + 0.05, 0]])
        self.play(FadeIn(lab), Create(axis), run_time=0.4)
        self.play(Create(rise), run_time=1.0)
        self.at("At threshold")
        tl = T("threshold", 22, GREY).next_to(dash, UP, buff=0.05).align_to(dash, RIGHT)
        self.play(Create(dash), FadeIn(tl), run_time=0.4)
        self.at("neuron fires")
        spike = VMobject(color=GREEN, stroke_width=6).set_points_as_corners(
            [[3.8, thr + 0.05, 0], [4.15, 2.0, 0], [4.55, base - 0.3, 0], [5.1, base, 0], [6.0, base, 0]])
        fires = chip("fires", GREEN, size=26).move_to([5.3, 1.5, 0])
        idl = T("idealised sketch", 22, GREY).move_to([3.5, -2.4, 0])
        self.play(Create(spike), run_time=0.7)
        self.play(FadeIn(fires), FadeIn(idl), run_time=0.4)
        self.finish()


class S03Shown(SpokenScene):
    def construct(self):
        tl, xs = timeline(False)
        self.add(tl[0])
        self.at("Georg Nagel")
        names = VGroup(T("Georg Nagel, Peter Hegemann, Ernst Bamberg", 30, TEXT),
                       T("and colleagues", 28, GREY)).arrange(DOWN, buff=0.12).move_to([0, 2.7, 0])
        self.play(FadeIn(names, shift=UP * 0.1), run_time=0.5)
        self.at("2002 and 2003")
        band = Rectangle(width=xs[2003] - xs[2002], height=0.34, stroke_width=0, fill_color=TEAL,
                         fill_opacity=0.5).move_to([(xs[2002] + xs[2003]) / 2, -3.1, 0])
        self.play(FadeIn(tl[1:]), FadeIn(band), run_time=0.5)
        self.at("gated channels")
        c1 = chip("Chlamydomonas channelrhodopsins: light-gated channels", BLUE, size=26).move_to([0, 1.0, 0])
        self.play(FadeIn(c1, shift=UP * 0.1), run_time=0.5)
        self.at("passes cations")
        c2 = chip("channelrhodopsin-2 passes cations", BLUE, size=26).move_to([0, -0.2, 0])
        self.play(FadeIn(c2, shift=UP * 0.1), run_time=0.5)
        self.at("works in mammalian cells")
        c3 = chip("channelrhodopsin-2 works in mammalian cells", BLUE, size=26).move_to([0, -1.4, 0])
        self.play(FadeIn(c3, shift=UP * 0.1), run_time=0.5)
        self.finish()


class S04Fired(SpokenScene):
    def construct(self):
        tl, xs = timeline(True)
        band = Rectangle(width=xs[2003] - xs[2002], height=0.34, stroke_width=0, fill_color=TEAL,
                         fill_opacity=0.25).move_to([(xs[2002] + xs[2003]) / 2, -3.1, 0])
        self.add(tl, band)
        self.at("In 2005")
        band2 = Rectangle(width=0.5, height=0.34, stroke_width=0, fill_color=TEAL, fill_opacity=0.6).move_to([xs[2005], -3.1, 0])
        self.play(FadeIn(band2), Indicate(tl[-1], color=TEAL), run_time=0.5)
        self.at("Edward Boyden")
        names = VGroup(T("Edward Boyden, Feng Zhang, Ernst Bamberg,", 28, TEXT),
                       T("Georg Nagel, Karl Deisseroth", 28, TEXT)).arrange(DOWN, buff=0.1).move_to([0, 3.05, 0])
        self.play(FadeIn(names, shift=UP * 0.1), run_time=0.5)
        self.at("hippocampal neurons in culture")
        nx = -4.4
        neuron = Circle(radius=0.95, stroke_color=GREY, stroke_width=3, fill_color=GREY, fill_opacity=0.15).move_to([nx, 0.15, 0])
        nl = T("hippocampal neuron", 22, GREY).next_to(neuron, DOWN, buff=0.1)
        nl2 = T("in culture", 22, GREY).next_to(nl, DOWN, buff=0.04)
        self.play(FadeIn(neuron), FadeIn(nl), FadeIn(nl2), run_time=0.5)
        self.at("the gene for")
        gene = chip("channelrhodopsin-2 gene", BLUE, size=22).move_to([nx, 1.95, 0])
        ga = arr([nx, 1.62, 0], [nx, 1.22, 0], BLUE, 5)
        self.play(FadeIn(gene), run_time=0.3)
        self.play(GrowArrow(ga), run_time=0.4)
        self.play(neuron.animate.set_stroke(BLUE).set_fill(BLUE, 0.2), run_time=0.3)
        self.at("fired action potentials")
        lx0, lx1 = -1.6, 6.0
        by = -0.4
        xsf = [-0.2, 1.3, 2.8, 4.3, 5.6]
        flashes = VGroup(*[Rectangle(width=0.22, height=0.5, stroke_width=0, fill_color=BLUE, fill_opacity=1).move_to([x, 1.45, 0])
                           for x in xsf])
        fl = T("blue light flashes", 22, BLUE).move_to([2.7, 2.05, 0])
        base = Line([lx0, by, 0], [lx1, by, 0], color=GREY, stroke_width=3)
        spikes = VGroup(*[VMobject(color=GREEN, stroke_width=6).set_points_as_corners(
            [[x - 0.2, by, 0], [x, by + 1.1, 0], [x + 0.2, by - 0.25, 0], [x + 0.4, by, 0]]) for x in xsf])
        apl = T("action potentials", 22, GREEN).move_to([2.7, -1.05, 0])
        self.play(FadeIn(fl), Create(base), FadeIn(apl), run_time=0.4)
        for f, s in zip(flashes, spikes):
            self.play(FadeIn(f, run_time=0.15), run_time=0.15)
            self.play(Create(s), run_time=0.3)
        idl = T("idealised", 22, GREY).move_to([5.4, -1.05, 0])
        self.play(FadeIn(idl), run_time=0.3)
        self.at("Other laboratories")
        oth = chip("other laboratories: similar results", GREY, size=24).move_to([2.7, -2.0, 0])
        self.play(FadeIn(oth, shift=UP * 0.1), run_time=0.5)
        self.finish()


class S05End(EndCard):
    LINE = "Channelrhodopsin-2 is itself an ion channel."
