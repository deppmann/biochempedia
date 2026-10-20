"""Capturing Sunlight: where a plant's mass comes from  (Biochemistrypedia explainer)

COLOR MAP (one color per concept, whole video)
  BLUE   = carbon dioxide
  TEAL   = water
  YELLOW = light / sunlight
  GREEN  = the plant, the chloroplast and chlorophyll
  ORANGE = glucose (sugar)
  PINK   = oxygen
  PURPLE = minerals from the soil
  GOLD   = chemical energy
  GREY   = soil, pot, cell outline, structure, de-emphasized
  RED    = the open question
"""
import numpy as np
from bp_style import *  # noqa: F401,F403

PURPLE = "#B58CD9"
ORANGE = "#F29E4C"
PINK = "#E58AB8"
LIGHTC = "#B8BECC"


def bchip(text, color=BLUE, size=26, **kw):
    c = chip(text, color, size=size, **kw)
    back = RoundedRectangle(corner_radius=0.14, width=c[0].width, height=c[0].height, stroke_width=0,
                            fill_color=BG, fill_opacity=1).move_to(c[0])
    return VGroup(back, *c)


def arr(a, b, color=GREY, w=5, tip=0.22):
    return Arrow(a, b, buff=0.08, color=color, stroke_width=w, tip_length=tip,
                 max_tip_length_to_length_ratio=0.45, max_stroke_width_to_length_ratio=12)


def pulse(c, color, s=1.12, **kw):
    return Indicate(VGroup(*c[1:]), color=color, scale_factor=s, **kw)


def pot(cx, cy, w=2.6, h=1.2):
    return Rectangle(width=w, height=h, stroke_color=GREY, stroke_width=3, fill_color=GREY,
                     fill_opacity=0.3).move_to([cx, cy, 0])


def trunk(cx, y0, y1, w=0.3):
    return Rectangle(width=w, height=y1 - y0, stroke_color=GREEN, stroke_width=3, fill_color=GREEN,
                     fill_opacity=0.5).move_to([cx, (y0 + y1) / 2, 0])


def canopy(cx, cy, w=2.2, h=1.1, label=None):
    r = RoundedRectangle(corner_radius=0.35, width=w, height=h, stroke_color=GREEN, stroke_width=3,
                         fill_color=GREEN, fill_opacity=0.3).move_to([cx, cy, 0])
    if label:
        return VGroup(r, T(label, 26, GREEN).move_to(r))
    return VGroup(r)


class S00Title(TitleCard):
    LESSON = "Capturing Sunlight"
    TITLE = "Where a Plant's Mass Comes From"


# ---------------------------------------------------------------------------------------------
class S01Willow(SpokenScene):
    def construct(self):
        LX, RX = -3.9, 3.9
        py = -1.5
        # start: pot, soil, stem
        hl = T("Start", 30, GREY).move_to([LX, 3.15, 0])
        lpot = pot(LX, py)
        lstem = trunk(LX, py + 0.6, py + 1.4, 0.14)
        self.play(FadeIn(hl), FadeIn(lpot), run_time=0.8)
        self.at("planted a willow stem")
        self.play(GrowFromEdge(lstem, DOWN), run_time=0.8)
        lab_stem = T("willow stem: 5 lb", 26, GREEN).move_to([LX, -2.65, 0])
        lab_soil = T("dried soil: 200 lb", 26, LIGHTC).move_to([LX, -3.15, 0])
        self.at("The stem weighed")
        self.play(FadeIn(lab_stem, shift=UP * 0.1), run_time=0.5)
        self.at("The soil weighed")
        self.play(FadeIn(lab_soil, shift=UP * 0.1), run_time=0.5)

        # five years later
        self.at("Five years later")
        ar = arr([-1.5, 0.2, 0], [1.5, 0.2, 0], GREY)
        ar_l = T("5 years", 28, GREY).next_to(ar, UP, buff=0.15)
        rpot = pot(RX, py)
        rtrunk = trunk(RX, py + 0.6, py + 3.0)
        rcan = canopy(RX, py + 3.55, 2.4, 1.1)
        hr = T("Five years later", 30, GREY).move_to([RX, 3.35, 0])
        self.play(GrowArrow(ar), FadeIn(ar_l), FadeIn(hr), FadeIn(rpot), run_time=0.5)
        self.play(GrowFromEdge(rtrunk, DOWN), run_time=0.6)
        self.play(FadeIn(rcan, scale=0.8), run_time=0.3)
        lab_tree = T("tree: about 169 lb", 26, GREEN).move_to([RX, -2.65, 0])
        self.at("he reported a tree")
        self.play(FadeIn(lab_tree, shift=UP * 0.1), run_time=0.5)
        lab_soil2 = T("soil: about 2 oz lighter", 26, LIGHTC).move_to([RX, -3.15, 0])
        self.at("ounces lighter")
        self.play(FadeIn(lab_soil2, shift=UP * 0.1), run_time=0.5)

        # the question
        self.at("So where does a plant's mass")
        gone = VGroup(hl, lpot, lstem, lab_stem, lab_soil, ar, ar_l, hr)
        q1 = T("Where does a\nplant's mass\ncome from?", 44, TEXT, font=TITLE_FONT, line_spacing=0.9).move_to([-3.6, 0.2, 0])
        self.play(FadeOut(gone), run_time=0.4)
        self.play(FadeIn(q1, shift=UP * 0.15), run_time=0.5)
        self.at("And how does sunlight")
        sun_c = Circle(radius=0.38, stroke_color=YELLOW, stroke_width=4, fill_color=YELLOW, fill_opacity=0.9)
        rays = VGroup(*[Line(UP * 0.55, UP * 0.85, color=YELLOW, stroke_width=5).rotate(a * PI / 4, about_point=ORIGIN)
                        for a in range(8)])
        sun = VGroup(sun_c, rays).move_to([-3.6, 2.4, 0])
        q2 = T("How does\nsunlight end up\nstored in sugar?", 44, TEXT, font=TITLE_FONT, line_spacing=0.9).move_to([-3.6, -0.1, 0])
        self.play(FadeOut(q1), run_time=0.3)
        self.play(FadeIn(sun, scale=0.7), FadeIn(q2, shift=UP * 0.15), run_time=0.6)
        self.finish()


# ---------------------------------------------------------------------------------------------
class S02Equation(SpokenScene):
    def construct(self):
        # words first, formulas after "With formulas"
        yi, yo = 1.5, -1.7
        pw = T("photosynthesis", 54, GREEN, font=TITLE_FONT).move_to([0, 0, 0])
        self.wait(0.3)
        self.play(Write(pw), run_time=1.0)

        light = bchip("light energy", YELLOW, 32)
        co2 = bchip("carbon dioxide", BLUE, 32)
        h2o = bchip("water", TEAL, 32)
        plus1 = T("+", 40, GREY)
        plus2 = T("+", 40, GREY)
        row = VGroup(co2, plus1, h2o, plus2, light).arrange(RIGHT, buff=0.35).move_to([0, yi, 0])
        sugar = bchip("sugar", ORANGE, 32)
        oxy = bchip("oxygen", PINK, 32)
        plus3 = T("+", 40, GREY)
        out = VGroup(sugar, plus3, oxy).arrange(RIGHT, buff=0.35).move_to([0, yo, 0])
        down = arr([0, 0.8, 0], [0, -0.9, 0], GREY, 6)

        self.at("use light energy")
        self.play(pw.animate.scale(0.52).move_to([1.75, -0.05, 0]), FadeIn(light, shift=DOWN * 0.15), run_time=0.7)
        self.at("carbon dioxide and water")
        self.play(FadeIn(co2, shift=DOWN * 0.15), FadeIn(plus1), FadeIn(h2o, shift=DOWN * 0.15), FadeIn(plus2), run_time=0.8)
        self.at("into sugar")
        self.play(GrowArrow(down), run_time=0.4)
        self.play(FadeIn(sugar, shift=DOWN * 0.15), run_time=0.5)
        self.at("release oxygen")
        self.play(FadeIn(plus3), FadeIn(oxy, shift=DOWN * 0.15), run_time=0.6)

        self.at("The sugar is glucose")
        gl = bchip("glucose", ORANGE, 32).move_to(sugar)
        note = T("a small sugar molecule with 6 carbon atoms", 26, ORANGE).move_to([0, -3.0, 0])
        self.play(FadeOut(sugar), FadeIn(gl), run_time=0.5)
        sugar = gl
        self.play(FadeIn(note, shift=UP * 0.1), run_time=0.5)

        self.at("With formulas")
        f_co2 = bchip("6 CO₂", BLUE, 34)
        f_h2o = bchip("6 H₂O", TEAL, 34)
        f_light = bchip("light energy", YELLOW, 34)
        row2 = VGroup(f_co2, T("+", 40, GREY), f_h2o, T("+", 40, GREY), f_light).arrange(RIGHT, buff=0.35).move_to([0, yi, 0])
        f_glu = bchip("C₆H₁₂O₆", ORANGE, 34)
        f_oxy = bchip("6 O₂", PINK, 34)
        out2 = VGroup(f_glu, T("+", 40, GREY), f_oxy).arrange(RIGHT, buff=0.35).move_to([0, yo, 0])
        self.play(FadeOut(note), FadeOut(VGroup(co2, h2o, light, sugar, oxy, plus1, plus2, plus3)), run_time=0.4)
        self.play(FadeIn(VGroup(f_co2, f_h2o, f_light, f_glu, f_oxy, row2[1], row2[3], out2[1])), run_time=0.5)
        co2, h2o, sugar, oxy = f_co2, f_h2o, f_glu, f_oxy
        self.at("six carbon dioxide")
        self.play(pulse(co2, BLUE, 1.12), run_time=0.7)
        self.at("plus six water")
        self.play(pulse(h2o, TEAL, 1.12), run_time=0.7)
        self.at("makes one glucose")
        self.play(pulse(sugar, ORANGE, 1.12), run_time=0.7)
        self.at("six oxygen molecules")
        self.play(pulse(oxy, PINK, 1.12), run_time=0.7)
        self.finish()


# ---------------------------------------------------------------------------------------------
class S03Count(SpokenScene):
    def construct(self):
        U = 0.24
        X0 = 1.25
        rows = [("carbon", 6, 1.15), ("hydrogen", 12, -0.15), ("oxygen", 18, -1.45)]
        BAR = LIGHTC
        head_l = T("left side", 28, GREY).move_to([-3.5, 3.0, 0])
        head_r = T("right side", 28, GREY).move_to([3.5, 3.0, 0])
        form_l = T("6CO₂ + 6H₂O", 28, TEXT).move_to([-3.5, 2.45, 0])
        form_r = T("C₆H₁₂O₆ + 6O₂", 28, TEXT).move_to([3.5, 2.45, 0])
        self.at("Count the atoms")
        self.play(FadeIn(head_l), FadeIn(form_l), FadeIn(head_r), FadeIn(form_r), run_time=0.7)
        labels = [T(n, 28, TEXT).move_to([0, y, 0]) for n, _, y in rows]
        self.play(*[FadeIn(l) for l in labels], run_time=0.5)

        def bar(n, y, side):
            w = n * U
            r = Rectangle(width=w, height=0.62, stroke_color=BAR, stroke_width=2, fill_color=BAR, fill_opacity=0.35)
            r.move_to([side * (X0 + w / 2), y, 0])
            num = M(str(n), 28, TEXT).move_to([side * (X0 + w + 0.42), y, 0])
            return VGroup(r, num)

        lbars = [bar(n, y, -1) for _, n, y in rows]
        rbars = [bar(n, y, 1) for _, n, y in rows]
        for b, cue in zip(lbars, ["carbon", "hydrogen", "oxygen"]):
            self.at(cue)
            self.play(GrowFromEdge(b[0], RIGHT), FadeIn(b[1]), run_time=0.45)
        self.at("On the right")
        for b in rbars:
            self.play(GrowFromEdge(b[0], LEFT), FadeIn(b[1]), run_time=0.45)
        self.at("exactly the same")
        self.play(*[b[0].animate.set_stroke(TEXT).set_fill(TEXT, 0.55) for b in lbars + rbars], run_time=0.6)
        cm = T("conservation of matter", 36, GOLD, font=TITLE_FONT).move_to([0, -2.6, 0])
        self.at("conservation of matter")
        self.play(FadeIn(cm, shift=UP * 0.1), run_time=0.5)
        sub = T("atoms are rearranged, never created or destroyed", 26, TEXT).move_to([0, -3.25, 0])
        self.at("rearranged")
        self.play(FadeIn(sub, shift=UP * 0.1), run_time=0.5)
        self.finish()


# ---------------------------------------------------------------------------------------------
class S04Source(SpokenScene):
    def construct(self):
        cx = 0.5
        pw, ph, py = 8.4, 1.3, -2.3
        p = pot(cx, py, pw, ph)
        tk = trunk(cx, py + ph / 2, 0.7)
        cn = canopy(cx, 1.5, 3.4, 1.4, "willow")
        soil_lbl = T("dried soil", 26, LIGHTC).move_to([cx, -3.3, 0])
        self.at("Now the willow")
        self.play(FadeIn(p), FadeIn(soil_lbl), GrowFromEdge(tk, DOWN), run_time=0.8)
        self.play(FadeIn(cn, scale=0.8), run_time=0.5)

        co2 = bchip("carbon dioxide", BLUE, 28).move_to([-4.7, 1.5, 0])
        air = T("in the air", 24, GREY).next_to(co2, UP, buff=0.15)
        a_co2 = arr(co2.get_right(), [cx - 1.7, 1.5, 0], BLUE, 5)
        self.at("The carbon and much")
        self.play(FadeIn(co2, shift=RIGHT * 0.2), FadeIn(air), run_time=0.5)
        self.at("came from carbon dioxide in")
        self.play(GrowArrow(a_co2), run_time=0.6)

        wat = bchip("water", TEAL, 26).move_to([cx - 2.6, py + 0.1, 0])
        a_w = arr([cx - 2.6, py + 0.45, 0], [cx - 0.15, py + ph / 2 + 0.25, 0], TEAL, 5)
        self.at("The hydrogen came from water")
        self.play(FadeIn(wat), run_time=0.4)
        self.play(GrowArrow(a_w), run_time=0.5)

        mn = bchip("small amount of minerals", PURPLE, 22).move_to([cx + 2.0, py + 0.1, 0])
        a_m = arr([cx + 0.9, py + 0.45, 0], [cx + 0.15, py + ph / 2 + 0.25, 0], PURPLE, 3, 0.16)
        self.at("small amount of minerals")
        self.play(FadeIn(mn), run_time=0.4)
        self.play(GrowArrow(a_m), run_time=0.5)

        self.at("barely changed")
        soil2 = T("dried soil: barely changed", 26, LIGHTC).move_to([cx, -3.3, 0])
        self.play(Transform(soil_lbl, soil2), run_time=0.5)

        self.at("Most of a plant's dry mass")
        note = T("most of the dry mass:\ncarbon from\ncarbon dioxide", 26, BLUE, line_spacing=0.9).move_to([cx + 4.2, 1.5, 0])
        a_big = arr(co2.get_right(), [cx - 1.7, 1.5, 0], BLUE, 12, 0.3)
        self.play(Transform(a_co2, a_big), pulse(co2, BLUE, 1.1), run_time=0.7)
        self.play(FadeIn(note, shift=LEFT * 0.1), run_time=0.5)
        self.finish()


# ---------------------------------------------------------------------------------------------
class S05Chloroplast(SpokenScene):
    def construct(self):
        cell = RoundedRectangle(corner_radius=0.4, width=7.4, height=5.4, stroke_color=GREY, stroke_width=3,
                                fill_color=GREY, fill_opacity=0.08).move_to([-0.1, -0.1, 0])
        cell_l = T("leaf cell", 24, GREY).move_to([-2.9, 2.2, 0])
        el = Ellipse(width=5.4, height=3.3, stroke_color=GREEN, stroke_width=4, fill_color=GREEN,
                     fill_opacity=0.1).move_to([-0.6, -0.1, 0])
        cl_l = T("chloroplast", 28, GREEN).move_to([0.3, 2.2, 0])
        self.wait(0.3)
        self.play(FadeIn(cell), FadeIn(cell_l), run_time=0.6)
        self.at("happens in the chloroplast")
        self.play(Create(el), FadeIn(cl_l), run_time=0.7)

        stacks = VGroup()
        for sx in (-2.6, -1.5, -0.4):
            st = VGroup(*[Rectangle(width=0.9, height=0.13, stroke_color=GREEN, stroke_width=2, fill_color=GREEN,
                                    fill_opacity=0.35).move_to([sx, -0.9 + k * 0.22, 0]) for k in range(5)])
            stacks.add(st)
        self.at("stacks of membranes")
        self.play(*[FadeIn(s, shift=UP * 0.1) for s in stacks], run_time=0.8)
        chl = bchip("chlorophyll", GREEN, 26).move_to([-1.5, -2.3, 0])
        ln = Line(chl.get_top() + UP * 0.02, [-1.5, -0.35, 0], color=GREEN, stroke_width=3)
        self.at("hold chlorophyll")
        self.play(FadeIn(chl), Create(ln), run_time=0.5)
        self.play(*[s.animate.set_fill(GREEN, 0.8) for s in [r for st in stacks for r in st]], run_time=0.5)
        pig = T("green pigment", 24, GREEN).next_to(chl, RIGHT, buff=0.2)
        self.at("green pigment")
        self.play(FadeIn(pig), run_time=0.4)

        # light
        lights = VGroup(*[arr([-5.7, y, 0], [-3.15, y * 0.35 + 0.0, 0], YELLOW, 5) for y in (1.2, 0.0, -1.2)])
        l_lbl = T("light", 30, YELLOW).move_to([-5.1, 2.0, 0])
        self.at("absorbs light")
        self.play(FadeIn(l_lbl), *[GrowArrow(a) for a in lights], run_time=0.8)
        rb = T("mostly red\nand blue", 24, YELLOW, line_spacing=0.9).move_to([-5.1, -2.1, 0])
        self.at("mostly red and blue")
        self.play(FadeIn(rb, shift=UP * 0.1), run_time=0.5)

        self.at("captured energy")
        self.play(*[Indicate(r, color=YELLOW, scale_factor=1.05) for st in stacks for r in st], run_time=0.8)
        # split water, build glucose, oxygen
        wat = bchip("water", TEAL, 22).move_to([0.95, 0.45, 0])
        self.at("split water")
        self.play(FadeIn(wat, scale=0.8), run_time=0.5)
        glu = bchip("glucose", ORANGE, 20).move_to([0.85, -0.45, 0])
        co2 = bchip("carbon dioxide", BLUE, 24).move_to([5.0, -1.3, 0])
        a_c = arr(co2.get_left(), [1.5, -1.3, 0], BLUE, 5)
        self.at("build glucose")
        self.play(FadeIn(co2), GrowArrow(a_c), run_time=0.6)
        self.play(FadeIn(glu, scale=0.8), run_time=0.5)
        oxy = bchip("oxygen", PINK, 26).move_to([5.0, 0.9, 0])
        a_o = arr(wat.get_right(), oxy.get_left(), PINK, 5)
        self.at("The oxygen released")
        self.play(GrowArrow(a_o), FadeIn(oxy), run_time=0.7)
        self.at("split water", nth=1)
        self.play(pulse(wat, TEAL, 1.15), run_time=0.6)
        self.finish()


# ---------------------------------------------------------------------------------------------
class S06Energy(SpokenScene):
    def construct(self):
        self.at("Energy is conserved too")
        le = bchip("light energy", YELLOW, 34).move_to([-4.0, 0.0, 0])
        ce = bchip("chemical energy", GOLD, 34).move_to([4.0, 0.0, 0])
        self.play(FadeIn(le, shift=RIGHT * 0.2), run_time=0.7)
        keep = T("not used up, not made", 28, YELLOW).move_to([-4.0, -1.0, 0])
        self.at("not used up or made")
        self.play(FadeIn(keep, shift=UP * 0.1), run_time=0.5)
        ar = arr([-1.9, 0.0, 0], [1.9, 0.0, 0], GOLD, 7)
        tl = T("transformed", 28, GOLD).next_to(ar, UP, buff=0.15)
        self.at("transformed into chemical energy")
        self.play(GrowArrow(ar), FadeIn(tl), run_time=0.6)
        self.play(FadeIn(ce, shift=LEFT * 0.2), run_time=0.5)
        held = T("held in the arrangement\nof atoms in molecules", 28, GOLD, line_spacing=0.9).move_to([4.0, -1.3, 0])
        self.at("held in the arrangement")
        self.play(FadeIn(held, shift=UP * 0.1), run_time=0.5)

        # levels sketch
        low_y, high_y = -1.8, 1.0
        head = T("Chemical energy, in this sketch", 28, GREY).move_to([0, 3.15, 0])
        low = Line([-5.8, low_y, 0], [-0.4, low_y, 0], color=GREY, stroke_width=6)
        high = Line([1.0, high_y, 0], [5.9, high_y, 0], color=GREY, stroke_width=6)
        lowc = bchip("carbon dioxide + water", BLUE, 28).move_to([-3.1, low_y + 0.7, 0])
        highc = bchip("glucose + oxygen", ORANGE, 28).move_to([3.45, high_y + 0.7, 0])
        self.at("Glucose and oxygen together")
        self.play(FadeOut(VGroup(le, ce, keep, ar, tl, held)), run_time=0.4)
        self.play(FadeIn(head), Create(high), FadeIn(highc), run_time=0.6)
        self.at("carbon dioxide and water they")
        self.play(Create(low), FadeIn(lowc), run_time=0.6)
        g1 = DashedLine([-0.4, low_y, 0], [0.3, low_y, 0], color=GOLD, stroke_width=3)
        g2 = DashedLine([0.3, high_y, 0], [1.0, high_y, 0], color=GOLD, stroke_width=3)
        up = arr([0.3, low_y, 0], [0.3, high_y, 0], GOLD, 5)
        more = T("more chemical energy", 28, GOLD).move_to([3.45, high_y - 0.55, 0])
        self.play(Create(g1), Create(g2), GrowArrow(up), FadeIn(more), run_time=0.7)

        # closing answer
        self.at("dry mass comes mostly")
        gone = VGroup(head, low, high, lowc, highc, up, more, g1, g2)
        self.play(FadeOut(gone), run_time=0.6)
        r1a = bchip("carbon dioxide in the air", BLUE, 32)
        r1b = bchip("most of a plant's dry mass", GREEN, 32)
        r1 = VGroup(r1a, arr(LEFT * 0.7, RIGHT * 0.7, GREY, 6), r1b).arrange(RIGHT, buff=0.3).move_to([0, 1.3, 0])
        r2a = bchip("sunlight", YELLOW, 32)
        r2b = bchip("chemical energy in sugar", GOLD, 32)
        r2 = VGroup(r2a, arr(LEFT * 0.7, RIGHT * 0.7, GREY, 6), r2b).arrange(RIGHT, buff=0.3).move_to([0, -1.3, 0])
        self.play(FadeIn(r1a, shift=RIGHT * 0.15), GrowArrow(r1[1]), FadeIn(r1b), run_time=0.9)
        self.at("sunlight is stored")
        self.play(FadeIn(r2a, shift=RIGHT * 0.15), GrowArrow(r2[1]), FadeIn(r2b), run_time=0.9)
        self.finish()


class S07End(EndCard):
    LINE = "Plant dry mass comes mostly from carbon dioxide; sunlight is stored in sugar."
