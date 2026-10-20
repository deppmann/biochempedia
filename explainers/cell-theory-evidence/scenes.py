"""The cell theory and its evidence: why seeing cells took better tools  (Biochemistrypedia explainer)

Timed to the SPOKEN words: every self.at("...") cue waits for that phrase in audio/words.json.

COLOR MAP (one color per concept, whole video)
  BLUE   = a cell (outline, cork boxes, cells in tissue)
  ORANGE = DNA (labelled bars, never a molecule)
  PINK   = metabolism (the chemical reactions label)
  TEAL   = a tool's limit (lines, bars: what it can separate)
  PURPLE = stain and the nucleus it reveals
  YELLOW = highlight, the question, the thing being named
  GREEN  = can be seen / separated / supported by evidence
  RED    = too small to separate / the wrong idea
  GREY   = outlines, axis, de-emphasized
"""
import math
import numpy as np
from bp_style import *  # noqa: F401,F403

ORANGE = "#F29E4C"
PURPLE = "#B58CD9"
PINK = "#E58FB0"


def bchip(text, color=BLUE, size=26, **kw):
    c = chip(text, color, size=size, **kw)
    back = RoundedRectangle(corner_radius=0.14, width=c[0].width, height=c[0].height, stroke_width=0,
                            fill_color=BG, fill_opacity=1).move_to(c[0])
    return VGroup(back, *c)


def btext(text, size=24, color=GREY, **kw):
    t = T(text, size, color, **kw)
    back = Rectangle(width=t.width + 0.2, height=t.height + 0.12, stroke_width=0, fill_color=BG, fill_opacity=1).move_to(t)
    return VGroup(back, t)


def arr(a, b, color=GREY, w=5, tip=0.22):
    return Arrow(a, b, buff=0.08, color=color, stroke_width=w, tip_length=tip,
                 max_tip_length_to_length_ratio=0.45, max_stroke_width_to_length_ratio=12)


def cellc(r=0.4, color=BLUE, op=0.15, sw=3.5):
    return Circle(radius=r, stroke_color=color, stroke_width=sw, fill_color=color, fill_opacity=op)


def dna_block(w=1.3):
    """DNA as a plain labelled block (no structure drawn)."""
    box = RoundedRectangle(corner_radius=0.1, width=w, height=0.6, stroke_color=ORANGE, stroke_width=3,
                           fill_color=ORANGE, fill_opacity=0.25)
    lab = T("DNA", 26, ORANGE, weight=BOLD).move_to(box)
    return VGroup(box, lab)


class S00Title(TitleCard):
    LESSON = "The cell theory and its evidence"
    TITLE = "Seeing cells took better tools"


# ---------------------------------------------------------------------------------------------
class S01Cork(SpokenScene):
    """Hooke's cork slice -> boxes -> 'cell' -> only walls -> about 175 years -> plants and animals?"""

    def construct(self):
        cols, rows, bw, bh = 9, 6, 0.92, 0.64
        grid = VGroup(*[Rectangle(width=bw, height=bh, stroke_color=BLUE, stroke_width=3, fill_opacity=0)
                        .move_to([(c - (cols - 1) / 2) * bw, ((rows - 1) / 2 - r) * bh, 0])
                        for r in range(rows) for c in range(cols)])
        grid.move_to([-0.4, 0.1, 0])
        slice_ = RoundedRectangle(corner_radius=0.2, width=grid.width + 0.6, height=grid.height + 0.6,
                                  stroke_color=GREY, stroke_width=4, fill_color=GREY, fill_opacity=0.12).move_to(grid)
        head = T("Robert Hooke, 1665", 36, YELLOW, font=TITLE_FONT).to_edge(UP, buff=0.45)
        cap = T("a thin slice of cork", 28, GREY).next_to(slice_, DOWN, buff=0.3)
        self.at("exceedingly thin slice")
        self.play(FadeIn(head, shift=DOWN * 0.1), FadeIn(slice_), FadeIn(cap), run_time=0.9)
        self.at("rows of tiny")
        self.play(LaggedStart(*[Create(g) for g in grid], lag_ratio=0.03), run_time=2.4)
        self.at("called them cells")
        pick = grid[cols * 2 + 8]
        lab = T("cell", 30, YELLOW, weight=BOLD)
        lab_b = btext("cell", 30, YELLOW, weight=BOLD)
        lab_b.move_to(slice_.get_right() + RIGHT * 0.0).shift(LEFT * 0.0)
        lab_b.move_to([6.0, 0.7, 0])
        ptr = arr([5.6, 0.7, 0], pick.get_right() + RIGHT * 0.05, YELLOW)
        self.play(pick.animate.set_stroke(YELLOW, 6).set_fill(YELLOW, 0.3), FadeIn(lab_b), GrowArrow(ptr), run_time=0.8)
        self.at("walls left by")
        walls = T("walls left by cork cells that had died", 28, GREY).move_to(cap)
        self.play(Transform(cap, walls), run_time=0.6)
        self.at("years passed")
        shrink = VGroup(slice_, grid, cap)
        self.play(FadeOut(lab_b), FadeOut(ptr), FadeOut(head), FadeOut(cap),
                  VGroup(slice_, grid).animate.scale(0.5).move_to([-4.3, 0.4, 0]), run_time=1.2)
        yr = T("1665", 30, YELLOW, font=MONO).next_to(slice_, DOWN, buff=0.25)
        line = arr([-1.9, 0.4, 0], [2.5, 0.4, 0], YELLOW)
        span = T("about 175 years", 30, YELLOW).next_to(line, UP, buff=0.2)
        self.play(FadeIn(yr), GrowArrow(line), FadeIn(span), run_time=1.0)
        self.at("plants and animals alike")
        q = bchip("plants and animals\nalike: cells?", YELLOW, 28).move_to([4.4, 0.4, 0])
        self.play(FadeIn(q, shift=LEFT * 0.2), run_time=0.7)
        self.at("Why did it take")
        why = T("Why did it take so long?", 44, TEXT, font=TITLE_FONT).move_to([0, -2.6, 0])
        self.play(FadeIn(why, shift=UP * 0.15), Indicate(q, color=YELLOW, scale_factor=1.08), run_time=0.9)
        self.finish()


# ---------------------------------------------------------------------------------------------
class S02Six(SpokenScene):
    """Six ideas acted out by one stage: organism of cells, one cell, division, metabolism, DNA copied, same make-up."""

    def construct(self):
        def caption(n, text):
            return T(f"{n}   {text}", 32, TEXT).move_to([0, 3.0, 0])

        dots = VGroup(*[VGroup(Circle(radius=0.22, stroke_color=GREY, stroke_width=3, fill_opacity=0),
                               T(str(i + 1), 22, GREY)) for i in range(6)])
        for d in dots:
            d[1].move_to(d[0])
        dots.arrange(RIGHT, buff=0.5).move_to([0, -3.2, 0])

        def light(i):
            return [dots[i][0].animate.set_stroke(YELLOW).set_fill(YELLOW, 0.9), dots[i][1].animate.set_color(BG)]

        title = T("The cell theory", 36, YELLOW, font=TITLE_FONT).move_to([0, 3.0, 0])
        self.at("The cell theory")
        self.play(FadeIn(title), FadeIn(dots), run_time=0.8)

        # 1 organism made of cells
        box = RoundedRectangle(corner_radius=0.25, width=7.4, height=4.0, stroke_color=GREY, stroke_width=4,
                               fill_color=GREY, fill_opacity=0.1).move_to([0, -0.1, 0])
        boxlab = T("a living organism", 26, GREY).move_to([0, 1.55, 0])
        cells = VGroup(*[cellc(0.4).move_to([(c - 2.5) * 1.05, 0.55 - r * 0.95, 0]) for r in range(3) for c in range(6)])
        cap1 = caption(1, "All living organisms are made of cells")
        self.at("All living organisms")
        self.play(Transform(title, cap1), FadeIn(box), FadeIn(boxlab), *light(0), run_time=0.8)
        self.at("made of cells")
        self.play(LaggedStart(*[GrowFromCenter(c) for c in cells], lag_ratio=0.04), run_time=1.1)

        # 2 one cell
        one = cells[8]
        cap2 = caption(2, "Cells are the basic unit of life")
        self.at("Cells are the basic unit")
        big = cellc(1.6, BLUE, 0.15, 5).move_to([0, -0.1, 0])
        lab_one = T("one cell", 28, BLUE).move_to([0, -2.1, 0])
        others = VGroup(*[c for c in cells if c is not one])
        self.play(Transform(title, cap2), FadeOut(box), FadeOut(boxlab), FadeOut(others), *light(1),
                  Transform(one, big), run_time=1.2)
        self.play(FadeIn(lab_one), run_time=0.4)

        # 3 division
        cap3 = caption(3, "All cells arise from pre-existing cells")
        self.at("All cells arise")
        a = cellc(1.15, BLUE, 0.15, 5).move_to([-1.7, -0.1, 0])
        b = cellc(1.15, BLUE, 0.15, 5).move_to([1.7, -0.1, 0])
        div_lab = T("cell division", 28, BLUE).move_to([0, -2.1, 0])
        self.play(Transform(title, cap3), *light(2), ReplacementTransform(one, VGroup(a, b)),
                  Transform(lab_one, div_lab), run_time=1.4)

        # 4 metabolism
        cap4 = caption(4, "Metabolism happens inside cells")
        self.at("Metabolism")
        cell = cellc(1.6, BLUE, 0.15, 5).move_to([0, -0.1, 0])
        met = chip("chemical\nreactions", PINK, 26).move_to(cell)
        self.play(Transform(title, cap4), *light(3), FadeOut(lab_one), ReplacementTransform(VGroup(a, b), cell), run_time=1.0)
        self.at("all the chemical reactions")
        self.play(FadeIn(met, scale=0.9), run_time=0.6)

        # 5 DNA passed on
        cap5 = caption(5, "Hereditary information, DNA, passes from cell to cell")
        self.at("Hereditary information")
        cellA = cellc(1.45, BLUE, 0.15, 5).move_to([-3.1, -0.1, 0])
        cellB = cellc(1.1, BLUE, 0.15, 5).move_to([3.1, -0.1, 0])
        dnaA = dna_block(1.3).move_to(cellA.get_center() + UP * 0.1)
        self.play(Transform(title, cap5), *light(4), FadeOut(met), ReplacementTransform(cell, cellA),
                  FadeIn(cellB), run_time=1.0)
        self.play(FadeIn(dnaA, scale=0.9), run_time=0.5)
        self.at("passes from cell")
        dnaB = dna_block(1.1).scale(0.9).move_to(cellB.get_center() + UP * 0.1)
        pass_ar = arr([-1.5, -0.1, 0], [1.7, -0.1, 0], ORANGE)
        copy = dnaA.copy()
        self.play(GrowArrow(pass_ar), Transform(copy, dnaB), run_time=1.3)

        # 6 same basic composition
        cap6 = caption(6, "All cells have the same basic composition")
        self.at("same basic composition")
        self.play(Transform(title, cap6), *light(5), FadeOut(pass_ar), run_time=0.6)
        self.play(Indicate(cellA, color=BLUE, scale_factor=1.06), Indicate(cellB, color=BLUE, scale_factor=1.06),
                  Indicate(dnaA, color=ORANGE, scale_factor=1.1), Indicate(copy, color=ORANGE, scale_factor=1.1),
                  run_time=1.0)
        self.finish()


# ---------------------------------------------------------------------------------------------
class S03Resolve(SpokenScene):
    """magnification vs resolution on a blurred pair of points; then a stain reveals a nucleus."""

    def construct(self):
        def pair(sep, halo, dot=0.1):
            hs = VGroup(*[Circle(radius=halo, stroke_width=0, fill_color=BLUE, fill_opacity=0.28).move_to([s * sep / 2, 0, 0]) for s in (-1, 1)])
            ds = VGroup(*[Circle(radius=dot, stroke_width=0, fill_color=TEXT, fill_opacity=1).move_to([s * sep / 2, 0, 0]) for s in (-1, 1)])
            return VGroup(hs, ds)

        blurred = pair(0.5, 0.55).move_to([0, 0.5, 0])
        hd1 = T("Magnification", 36, YELLOW, font=TITLE_FONT).move_to([0, 2.9, 0])
        l1 = T("two points, blurred together", 28, GREY).move_to([0, -1.2, 0])
        note = T("in this sketch", 22, GREY).move_to([0, -3.1, 0])
        self.at("Magnification is how many")
        self.play(FadeIn(hd1), FadeIn(blurred), FadeIn(l1), FadeIn(note), run_time=0.8)
        self.at("times larger")
        big = pair(0.5, 0.55).scale(2.0).move_to([-3.2, 0.5, 0])
        l2 = T("magnified: bigger,\nstill one blob", 28, GREY).move_to([-3.2, -1.7, 0])
        self.play(Transform(blurred, big), Transform(l1, l2), hd1.animate.move_to([-3.2, 2.9, 0]), run_time=1.2)
        self.at("Resolution is the smallest")
        hd2 = T("Resolution", 36, GREEN, font=TITLE_FONT).move_to([3.2, 2.9, 0])
        fine = pair(1.6, 0.2, 0.16).move_to([3.2, 0.5, 0])
        brace = BraceBetweenPoints([2.4, 0.15, 0], [4.0, 0.15, 0], DOWN, color=GREEN)
        l3 = T("smallest distance at which\ntwo points still look separate", 26, GREEN).next_to(brace, DOWN, buff=0.15)
        self.play(FadeIn(hd2), FadeIn(fine), run_time=0.7)
        self.play(GrowFromCenter(brace), FadeIn(l3), run_time=0.8)
        self.at("Resolution decides how much detail")
        self.play(Indicate(fine, color=GREEN, scale_factor=1.08), run_time=0.9)
        self.wait(0.3)

        # stain
        self.at("Many cells are almost clear")
        self.play(*[FadeOut(m) for m in (blurred, hd1, l1, hd2, fine, brace, l3, note)], run_time=0.6)
        cell = cellc(2.3, BLUE, 0.04, 4).set_stroke(opacity=0.5).move_to([0, 0.3, 0])
        nuc = Circle(radius=0.8, stroke_color=PURPLE, stroke_width=3, fill_color=PURPLE, fill_opacity=0.0).set_stroke(opacity=0.15).move_to([0.2, 0.4, 0])
        clear = T("almost clear", 30, GREY).move_to([0, -2.6, 0])
        self.play(FadeIn(cell), FadeIn(nuc), FadeIn(clear), run_time=0.8)
        self.at("A stain is a dye")
        dye = bchip("stain", PURPLE, 30).move_to([-4.8, 2.4, 0])
        self.play(FadeIn(dye, shift=DOWN * 0.1), run_time=0.5)
        self.at("sticks to some cell parts")
        nlab = T("nucleus", 30, PURPLE, weight=BOLD).move_to([3.9, 1.8, 0])
        nptr = arr([3.2, 1.7, 0], [1.05, 0.8, 0], PURPLE)
        self.play(dye.animate.move_to([-3.3, 0.4, 0]), run_time=0.8)
        self.play(nuc.animate.set_stroke(PURPLE, 5, opacity=1).set_fill(PURPLE, 0.55), cell.animate.set_stroke(opacity=0.5),
                  FadeIn(nlab), GrowArrow(nptr), FadeOut(dye), run_time=0.9)
        self.at("It adds contrast")
        con = T("more contrast", 32, PURPLE).move_to([0, -2.6, 0])
        self.play(Transform(clear, con), run_time=0.6)
        self.finish()


# ---------------------------------------------------------------------------------------------
class S04Limits(SpokenScene):
    """log size ladder 1 mm -> 1 nm; each tool's limit line; what it can separate turns green."""

    def construct(self):
        K = 1.1  # units per decade
        y = lambda um: K * math.log10(um)
        AX = -4.6
        axis = Line([AX, y(0.001) - 0.1, 0], [AX, y(1000) + 0.1, 0], color=GREY, stroke_width=3)
        ticks = VGroup()
        for um, lab in [(1000, "1 mm"), (100, "100 µm"), (10, "10 µm"), (1, "1 µm"), (0.1, "100 nm"), (0.01, "10 nm"), (0.001, "1 nm")]:
            tk = Line([AX - 0.1, y(um), 0], [AX + 0.1, y(um), 0], color=GREY, stroke_width=3)
            tl = T(lab, 22, GREY).next_to(tk, LEFT, buff=0.12)
            ticks.add(VGroup(tk, tl))
        
        def zone(um):
            top = y(um)
            r = Rectangle(width=6.2 - AX, height=top - (y(0.001) - 0.1), stroke_width=0, fill_color=RED, fill_opacity=0.10)
            r.move_to([(AX + 6.2) / 2, (top + y(0.001) - 0.1) / 2, 0])
            return r

        def tool_line(um, color=TEAL):
            return Line([AX, y(um), 0], [6.2, y(um), 0], color=color, stroke_width=4)

        def obj(um, label, py=None):
            d = Circle(radius=0.14, stroke_color=GREEN, stroke_width=3, fill_color=GREEN, fill_opacity=0.9).move_to([-3.9, y(um) if py is None else py, 0])
            t = T(label, 22, GREEN).next_to(d, RIGHT, buff=0.2)
            return VGroup(d, t)

        # eye
        self.at("unaided eye")
        L1 = tool_line(100)
        lab1 = btext("unaided eye: about 0.1 mm (100 µm)", 24, TEAL).move_to([3.0, y(100) + 0.28, 0])
        z = zone(100)
        zl = T("cannot be separated", 24, RED).move_to([4.4, y(100) - 0.8, 0])
        self.play(Create(axis), FadeIn(ticks), Create(L1), FadeIn(lab1), FadeIn(z), FadeIn(zl), run_time=1.0)
        self.at("frog egg")
        o1 = obj(1000, "African clawed frog egg, about 1 mm")
        self.play(FadeIn(o1, scale=0.8), run_time=0.6)
        # light
        self.at("light microscope")
        L2 = tool_line(0.2)
        lab2 = btext("light microscope: 0.2 µm", 24, TEAL).move_to([4.1, y(0.2) + 0.28, 0])
        z2 = zone(0.2)
        self.play(Create(L2), FadeIn(lab2), Transform(z, z2), zl.animate.move_to([4.4, y(0.2) - 0.8, 0]), run_time=1.1)
        self.at("cheek cell")
        o2 = obj(55, "cheek cell, about 50 to 60 µm")
        self.play(FadeIn(o2, scale=0.8), run_time=0.5)
        self.at("bacterium")
        o3 = obj(1.5, "bacterium, about 1 to 2 µm")
        self.play(FadeIn(o3, scale=0.8), run_time=0.5)
        # electron
        self.at("electron microscope")
        band = Rectangle(width=6.2 - AX, height=y(0.002) - y(0.001), stroke_width=0, fill_color=TEAL, fill_opacity=0.5)
        band.move_to([(AX + 6.2) / 2, (y(0.002) + y(0.001)) / 2, 0])
        lab3 = btext("electron microscope: about 1 to 2 nm", 24, TEAL).move_to([3.0, y(0.002) + 0.3, 0])
        z3 = zone(0.002)
        self.play(FadeIn(band), FadeIn(lab3), FadeOut(z), FadeOut(zl), run_time=1.0)
        self.at("shorter wavelengths")
        wl = btext("electrons: much shorter\nwavelengths than\nvisible light", 22, TEAL).move_to([4.7, -1.5, 0])
        self.play(FadeIn(wl), run_time=0.6)
        self.at("enough for a ribosome")
        o4 = obj(0.025, "ribosome, about 0.02 to 0.03 µm")
        self.play(FadeIn(o4, scale=0.8), run_time=0.6)
        self.finish()


# ---------------------------------------------------------------------------------------------
class S05Revised(SpokenScene):
    """four stations on a timeline; Schwann's fluid model is crossed out; Remak and Virchow fix it."""

    def construct(self):
        xs = [-4.7, -1.6, 1.6, 4.7]
        tl = Line([-6.2, 0.2, 0], [6.2, 0.2, 0], color=GREY, stroke_width=4)
        years = ["1838", "1839", "1852", "1855"]
        yl = VGroup(*[btext(y_, 28, YELLOW, font=MONO).move_to([x, 0.2, 0]) for y_, x in zip(years, xs)])
        self.at("The theory also changed")
        self.play(Create(tl), run_time=0.8)

        def card(x, name, desc, color=TEXT):
            n = T(name, 26, color, weight=BOLD)
            d = T(desc, 22, TEXT)
            g = VGroup(n, d).arrange(DOWN, buff=0.12)
            g.move_to([x, 2.2, 0])
            tick = Line([x, 0.5, 0], [x, 1.3, 0], color=GREY, stroke_width=3)
            return g, tick

        def tissue(label, x):
            blk = RoundedRectangle(corner_radius=0.15, width=2.8, height=1.7, stroke_color=GREY, stroke_width=3,
                                   fill_color=GREY, fill_opacity=0.1).move_to([x, -1.7, 0])
            cs = VGroup(*[cellc(0.24, BLUE, 0.2, 3).move_to([x + (c - 1.5) * 0.55, -1.45 + (0.28 if r == 0 else -0.28) - 0.1, 0])
                          for r in range(2) for c in range(4)])
            lb = T(label, 22, GREY).move_to([x, -2.9, 0])
            return VGroup(blk, cs), lb

        # Schleiden
        g1, t1 = card(xs[0], "Matthias\nSchleiden", "plant tissues are\nmade of cells")
        tis1, lb1 = tissue("plant tissue", xs[0])
        self.at("described plant tissues")
        self.play(FadeIn(yl[0]), Create(t1), FadeIn(g1, shift=DOWN * 0.1), run_time=0.7)
        self.play(FadeIn(tis1), FadeIn(lb1), run_time=0.6)
        # Schwann
        g2, t2 = card(xs[1], "Theodor\nSchwann", "animal tissues share\nthe cellular plan")
        tis2, lb2 = tissue("animal tissue", xs[1])
        self.at("found the same cellular plan")
        self.play(FadeIn(yl[1]), Create(t2), FadeIn(g2, shift=DOWN * 0.1), run_time=0.7)
        self.play(FadeIn(tis2), FadeIn(lb2), run_time=0.6)
        # the wrong model
        self.at("structureless fluid")
        fl = RoundedRectangle(corner_radius=0.15, width=2.8, height=1.7, stroke_color=RED, stroke_width=3,
                              fill_color=RED, fill_opacity=0.1).move_to([xs[1], -1.7, 0])
        newc = cellc(0.3, BLUE, 0.2, 3).move_to([xs[1], -1.7, 0])
        fl_lab = T("new cells form inside\na structureless fluid", 22, RED).move_to([xs[1], -2.95, 0])
        self.play(FadeOut(tis2), FadeOut(lb2), FadeIn(fl), FadeIn(fl_lab), run_time=0.6)
        self.play(GrowFromCenter(newc), run_time=0.7)
        self.at("That part was wrong")
        x1 = Line([xs[1] - 1.2, -1.0, 0], [xs[1] + 1.2, -2.4, 0], color=RED, stroke_width=8)
        x2 = Line([xs[1] - 1.2, -2.4, 0], [xs[1] + 1.2, -1.0, 0], color=RED, stroke_width=8)
        self.play(Create(x1), Create(x2), run_time=0.6)
        # Remak
        g3, t3 = card(xs[2], "Robert\nRemak", "new cells form when\ncells divide")
        a = cellc(0.45, BLUE, 0.15, 4).move_to([xs[2] - 1.0, -1.7, 0])
        b = cellc(0.32, BLUE, 0.15, 4).move_to([xs[2] + 0.55, -1.7, 0])
        c = cellc(0.32, BLUE, 0.15, 4).move_to([xs[2] + 1.15, -1.7, 0])
        ar = arr([xs[2] - 0.4, -1.7, 0], [xs[2] + 0.1, -1.7, 0], GREEN)
        lb3 = T("cells divide", 22, GREEN).move_to([xs[2], -2.6, 0])
        self.at("published evidence")
        self.play(FadeIn(yl[2]), Create(t3), FadeIn(g3, shift=DOWN * 0.1), run_time=0.7)
        self.play(FadeIn(a), GrowArrow(ar), ReplacementTransform(a.copy(), VGroup(b, c)), FadeIn(lb3), run_time=0.9)
        # Virchow
        g4, t4 = card(xs[3], "Rudolf\nVirchow", "every cell comes\nfrom a cell")
        ch = bchip("every cell comes\nfrom a cell", GREEN, 24).move_to([xs[3], -1.8, 0])
        self.at("spread the idea")
        self.play(FadeIn(yl[3]), Create(t4), FadeIn(g4, shift=DOWN * 0.1), run_time=0.7)
        self.play(FadeIn(ch, scale=0.9), run_time=0.6)
        self.finish()


# ---------------------------------------------------------------------------------------------
class S06Rule(SpokenScene):
    """bars to the same scale from the lesson's numbers: resolution finer than the structure; then the theory, corrected."""

    def construct(self):
        U = 25.0  # units per micrometre, so 0.2 um = 5.0 units
        X0 = -6.0
        def bar(um_lo, um_hi, color, y):
            solid = Rectangle(width=um_lo * U, height=0.4, stroke_width=0, fill_color=color, fill_opacity=0.9)
            solid.move_to([X0 + um_lo * U / 2, y, 0])
            g = VGroup(solid)
            if um_hi > um_lo:
                ext = Rectangle(width=(um_hi - um_lo) * U, height=0.4, stroke_width=0, fill_color=color, fill_opacity=0.4)
                ext.move_to([X0 + um_lo * U + (um_hi - um_lo) * U / 2, y, 0])
                g.add(ext)
            return g

        y1, y2, y3 = 1.6, 0.1, -1.4
        b1 = bar(0.2, 0.2, TEAL, y1)
        l1 = T("light microscope: separates 0.2 µm", 26, TEAL).move_to([X0 + 0.2 * U + 0.3 + 2.9, y1, 0])
        b2 = bar(0.02, 0.03, BLUE, y2)
        l2 = T("ribosome: about 0.02 to 0.03 µm", 26, BLUE).move_to([X0 + 0.03 * U + 0.3 + 2.8, y2, 0])
        b3 = Rectangle(width=0.05, height=0.4, stroke_width=0, fill_color=TEAL, fill_opacity=1).move_to([X0 + 0.025, y3, 0])
        l3 = T("electron microscope: about\n0.001 to 0.002 µm (1 to 2 nm)", 26, TEAL).move_to([X0 + 0.3 + 3.3, y3, 0])
        scale = T("bars drawn to the same scale, from the lesson's numbers", 22, GREY).move_to([0, -3.0, 0])

        self.at("why did it take better tools")
        self.play(GrowFromEdge(b1[0], LEFT), FadeIn(l1), FadeIn(scale), run_time=0.9)
        self.at("A tool can show a structure")
        self.play(GrowFromEdge(b2[0], LEFT), FadeIn(b2[1:]), FadeIn(l2), run_time=0.8)
        no = T("smaller than the limit: not separated", 26, RED).move_to([2.3, y2 - 0.65, 0])
        self.play(FadeIn(no), run_time=0.5)
        self.at("finer than the structure")
        self.play(FadeIn(b3), FadeIn(l3), FadeOut(no), run_time=0.7)
        yes = T("finer than the ribosome: separated", 26, GREEN).move_to([2.3, y3 - 0.85, 0])
        self.play(FadeIn(yes), run_time=0.5)
        self.at("Making the image bigger")
        mag = chip("bigger image: the comparison stays the same", YELLOW, 26).move_to([0, 2.95, 0])
        self.play(FadeIn(mag, shift=DOWN * 0.1), run_time=0.7)

        self.at("The cell theory is a")
        self.play(*[FadeOut(m) for m in (b1, b2, b3, l1, l2, l3, yes, scale, mag)], run_time=0.7)
        theory = chip("the cell theory", BLUE, 44, pad=0.35).move_to([0, 0.9, 0])
        wt = T("a well-tested explanation, not a guess", 36, GREEN).move_to([0, -0.4, 0])
        self.play(FadeIn(theory, scale=0.9), run_time=0.6)
        self.play(FadeIn(wt, shift=UP * 0.1), run_time=0.7)
        self.at("Scientists corrected it")
        ev = bchip("new evidence", YELLOW, 32).move_to([-4.9, 0.9, 0])
        ar = arr([-3.5, 0.9, 0], [-2.2, 0.9, 0], YELLOW)
        cor = T("corrected", 34, YELLOW, weight=BOLD).move_to([0, 2.4, 0])
        self.play(FadeIn(ev, shift=RIGHT * 0.2), GrowArrow(ar), run_time=0.7)
        self.play(Indicate(theory, color=YELLOW, scale_factor=1.08), FadeIn(cor), run_time=0.8)
        self.finish()


class S07End(EndCard):
    LINE = "Every cell comes from a cell."
