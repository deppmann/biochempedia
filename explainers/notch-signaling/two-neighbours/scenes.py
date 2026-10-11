"""Two equal neighbours, two fates (section film, Notch lesson)

COLOR MAP
  ORANGE = the anchor cell fate
  BLUE   = the ventral uterine precursor fate
  TEAL   = lin-12 (gene / receptor)
  RED    = the laser, crossed-out lin-12, "not anchor"
  GOLD   = the three scientists' names
  GREY   = cells before they choose, outlines, captions
"""
from bp_style import *  # noqa: F401,F403

ORANGE = "#F29E4C"
CX = 3.3
CY = 0.45
R = 2.0
TAGY = -2.05


def hdr(text):
    return T(text, 24, GREY).move_to([0, 3.35, 0])


def cell(side, name, color=GREY, op=0.14):
    c = Circle(radius=R, stroke_color=color, stroke_width=4, fill_color=color, fill_opacity=op)
    c.move_to([side * CX, CY, 0])
    lab = T(name, 30, TEXT, weight=BOLD).move_to(c)
    return VGroup(c, lab)


def recolor(c, color, op=0.3):
    return c[0].animate.set_fill(color, op).set_stroke(color)


def tag(side, text, color, size=24):
    t = chip(text, color, size=size)
    return t.move_to([side * CX, TAGY, 0])


def cross(c):
    return Cross(Circle(radius=0.3), stroke_color=RED, stroke_width=4).scale(0.8).set_opacity(0.6).move_to(c)


def gene_chip(side, crossed=False, text="lin-12", color=TEAL):
    g = chip(text, color, size=28).move_to([side * CX, CY - 0.9, 0])
    return g


class S00Title(TitleCard):
    LESSON = "Notch signaling"
    TITLE = "Two Equal Cells, Two Fates"


class S01Pair(SpokenScene):
    def construct(self):
        h = hdr("Gonad of a worm larva (schematic, not to scale)")
        L, Rr = cell(-1, "Z1.ppp"), cell(1, "Z4.aaa")
        self.at("two cells")
        self.play(FadeIn(h), GrowFromCenter(L[0]), GrowFromCenter(Rr[0]), run_time=self.beat(0.08))
        self.at("named")
        self.play(FadeIn(L[1]), FadeIn(Rr[1]), run_time=self.beat(0.05))
        wl = T("one worm", 26, GREY).move_to([0, 2.95, 0])
        self.at("anchor cell")
        a1 = tag(-1, "anchor cell", ORANGE)
        self.play(FadeIn(wl), recolor(L, ORANGE), FadeIn(a1, shift=UP * 0.1), run_time=self.beat(0.06))
        self.at("other becomes")
        v1 = tag(1, "ventral uterine precursor", BLUE)
        self.play(recolor(Rr, BLUE), FadeIn(v1, shift=UP * 0.1), run_time=self.beat(0.06))
        self.at("which is which")
        wl2 = T("another worm", 26, GREY).move_to(wl)
        a2 = tag(1, "anchor cell", ORANGE)
        v2 = tag(-1, "ventral uterine precursor", BLUE)
        self.play(Transform(wl, wl2), recolor(L, BLUE), recolor(Rr, ORANGE),
                  FadeOut(a1), FadeOut(v1), FadeIn(a2), FadeIn(v2), run_time=self.beat(0.08))
        self.at("about half")
        note = T("Each cell is the anchor cell in about half of animals", 26, TEXT).move_to([0, -3.15, 0])
        fit(note, max_w=11.5)
        self.play(FadeIn(note, shift=UP * 0.1), run_time=self.beat(0.06))
        self.finish()


class S02Laser(SpokenScene):
    def construct(self):
        h = hdr("Laser ablation (schematic)")
        L, Rr = cell(-1, "Z1.ppp"), cell(1, "Z4.aaa")
        self.add(h, L, Rr)
        self.at("with a laser")
        beam = Line([-CX, 3.0, 0], L.get_center() + UP * 0.2, color=RED, stroke_width=8)
        self.play(Create(beam), run_time=self.beat(0.04))
        self.play(FadeOut(L), FadeOut(beam), run_time=self.beat(0.05))
        self.at("anchor cell")
        t1 = tag(1, "anchor cell", ORANGE)
        self.play(recolor(Rr, ORANGE), FadeIn(t1, shift=UP * 0.1), run_time=self.beat(0.05))
        self.at("instead")
        L2, R2 = cell(-1, "Z1.ppp"), cell(1, "Z4.aaa")
        beam2 = Line([CX, 3.0, 0], R2.get_center() + UP * 0.2, color=RED, stroke_width=8)
        self.play(FadeOut(Rr), FadeOut(t1), FadeIn(L2), run_time=self.beat(0.04))
        self.play(FadeIn(R2), run_time=0.01)
        self.play(Create(beam2), run_time=self.beat(0.04))
        self.play(FadeOut(R2), FadeOut(beam2), run_time=self.beat(0.05))
        self.at("does")
        t2 = tag(-1, "anchor cell", ORANGE)
        self.play(recolor(L2, ORANGE), FadeIn(t2, shift=UP * 0.1), run_time=self.beat(0.05))
        self.at("whichever one")
        note = T("Whichever is killed, the survivor is always the anchor cell", 26, TEXT).move_to([0, -3.15, 0])
        fit(note, max_w=11.5)
        self.play(FadeIn(note, shift=UP * 0.1), run_time=self.beat(0.05))
        self.at("other fate")
        q = chip("the other fate needs a neighbour", BLUE, size=24).move_to([CX, CY, 0])
        self.play(FadeIn(q, shift=DOWN * 0.1), run_time=self.beat(0.07))
        self.finish()


class S03Lin12(SpokenScene):
    def construct(self):
        h = hdr("Greenwald's thesis work (schematic)")
        L, Rr = cell(-1, "Z1.ppp"), cell(1, "Z4.aaa")
        self.add(h, L, Rr)
        names = T("Greenwald  ·  Paul Sternberg  ·  Robert Horvitz", 26, GOLD).move_to([0, 2.95, 0])
        self.at("thesis work")
        self.play(FadeIn(names, shift=DOWN * 0.1), run_time=self.beat(0.07))
        self.at("gene called")
        gl, gr = gene_chip(-1), gene_chip(1)
        self.play(FadeIn(gl), FadeIn(gr), run_time=self.beat(0.05))
        self.at("with no")
        cap = T("no lin-12", 28, RED, weight=BOLD).move_to([0, -3.15, 0])
        xl, xr = cross(gl.get_center()), cross(gr.get_center())
        ta, tb = tag(-1, "anchor cell", ORANGE), tag(1, "anchor cell", ORANGE)
        self.play(FadeIn(cap), Create(xl), Create(xr), run_time=self.beat(0.05))
        self.play(recolor(L, ORANGE), recolor(Rr, ORANGE), FadeIn(ta), FadeIn(tb), run_time=self.beat(0.06))
        self.at("with overactive")
        cap2 = T("overactive lin-12", 28, TEAL, weight=BOLD).move_to(cap)
        og1 = chip("lin-12 (overactive)", TEAL, size=22).move_to(gl)
        og2 = chip("lin-12 (overactive)", TEAL, size=22).move_to(gr)
        na = T("not anchor", 24, RED, weight=BOLD).move_to([-CX, TAGY, 0])
        nb = T("not anchor", 24, RED, weight=BOLD).move_to([CX, TAGY, 0])
        self.play(FadeOut(cap), FadeOut(xl), FadeOut(xr), FadeOut(gl), FadeOut(gr), FadeOut(ta), FadeOut(tb),
                  recolor(L, GREY, 0.14), recolor(Rr, GREY, 0.14), run_time=self.beat(0.04))
        self.play(FadeIn(cap2), FadeIn(og1), FadeIn(og2), run_time=self.beat(0.04))
        self.at("neither")
        self.play(FadeIn(na), FadeIn(nb), run_time=self.beat(0.05))
        self.finish()


class S04Mosaic(SpokenScene):
    def construct(self):
        h = hdr("Mosaic worm (schematic)")
        L, Rr = cell(-1, "cell"), cell(1, "cell")
        self.add(h, L, Rr)
        self.at("mosaic worms")
        gr = gene_chip(1)
        gl = gene_chip(-1)
        self.play(FadeIn(gr), FadeIn(gl), run_time=self.beat(0.05))
        self.at("only one")
        xl = cross(gl.get_center())
        cap = T("one cell lacks lin-12", 26, RED, weight=BOLD).move_to([-CX, -3.15, 0])
        self.play(Create(xl), FadeIn(cap), run_time=self.beat(0.06))
        self.at("always becomes")
        ta = tag(-1, "anchor cell", ORANGE)
        self.play(recolor(L, ORANGE), FadeIn(ta), run_time=self.beat(0.06))
        self.at("what circuit")
        q = T("What circuit could produce this?", 34, TEXT, font=TITLE_FONT).move_to([0, -3.15, 0])
        self.play(FadeOut(cap), run_time=0.3)
        self.play(FadeIn(q, shift=UP * 0.1), run_time=self.beat(0.06))
        self.finish()


class S05End(EndCard):
    LINE = "A cell's fate can depend on its neighbour."
