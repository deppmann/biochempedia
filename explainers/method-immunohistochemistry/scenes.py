"""Immunohistochemistry and immunofluorescence: seeing where a protein sits  (Biochemistrypedia methods film)

Timed to the SPOKEN words: every self.at("...") cue waits for that phrase in audio/words.json.

COLOR MAP (one color per concept, whole video)
  PURPLE  = the target protein (the antigen, the epitope)
  BLUE    = the primary antibody (and the microscope apparatus)
  ORANGE  = the labeled secondary antibody
  GREEN   = the label / the signal / the first marker in an image
  MAGENTA = the second marker (second color) in an image
  TAN     = the enzyme and its colored product
  TEAL    = reagents you add (fixative, detergent, blocker, amino acids), step bar
  GREY    = tissue, cells, membranes, structure, de-emphasised text
  YELLOW  = questions, highlights, the epitope tab
  RED     = nonspecific signal, the pitfall
  GOLD    = dates and the closing rule
"""
import numpy as np
from bp_style import *  # noqa: F401,F403

PURPLE = "#B58CD9"
ORANGE = "#F29E4C"
MAGENTA = "#E066C8"
TAN = "#C9955A"


# ---------------------------------------------------------------------------------------------
# helpers
# ---------------------------------------------------------------------------------------------
def lab(text, size=24, color=GREY, **kw):
    return T(text, size, color, **kw)


def lines(*texts, size=24, color=TEXT, buff=0.12, align=ORIGIN, colors=None):
    g = VGroup(*[T(t, size, (colors[i] if colors else color)) for i, t in enumerate(texts)])
    return g.arrange(DOWN, aligned_edge=align, buff=buff)


def arr(a, b, color=GREY, w=5, tip=0.2):
    return Arrow([a[0], a[1], 0], [b[0], b[1], 0], buff=0.0, color=color, stroke_width=w, tip_length=tip,
                 max_tip_length_to_length_ratio=0.45, max_stroke_width_to_length_ratio=12)


def membrane(x0, x1, y, h=0.3, color=GREY):
    return RoundedRectangle(corner_radius=0.08, width=x1 - x0, height=h, stroke_color=color, stroke_width=2.5,
                            fill_color=color, fill_opacity=0.35).move_to([(x0 + x1) / 2, y, 0])


def cellc(cx, cy, r=0.7, color=GREY, fill=0.12, nuc=True):
    """A cell as a circle, with a small nucleus circle."""
    g = VGroup(Circle(radius=r, stroke_color=color, stroke_width=3, fill_color=color, fill_opacity=fill))
    if nuc:
        g.add(Circle(radius=r * 0.36, stroke_color=color, stroke_width=2, fill_color=color, fill_opacity=0.08))
    return g.move_to([cx, cy, 0])


def Yab(x, y, color, s=1.0, down=False, w=7):
    """Antibody as a simple pictogram: three bars. Junction at (x, y). Arm tips (the variable end)
    point up, or down with down=True; the stem end is the constant end."""
    dx, dy, st = 0.38 * s, 0.5 * s, 0.55 * s
    parts = [Line([0, -st, 0], [0, 0, 0]), Line([0, 0, 0], [-dx, dy, 0]), Line([0, 0, 0], [dx, dy, 0])]
    g = VGroup(*parts).set_stroke(color, w * max(s, 0.8))
    if down:
        g.rotate(PI, about_point=ORIGIN)
    g.shift([x, y, 0])
    g.dx, g.dy, g.st = dx, dy, st
    return g


def peg(x, base_y, h=0.8, w=0.36, tab=True):
    """A target protein standing on a membrane: a rounded post with a small yellow epitope tab on top."""
    p = RoundedRectangle(corner_radius=0.1, width=w, height=h, stroke_color=PURPLE, stroke_width=2.5,
                         fill_color=PURPLE, fill_opacity=0.55).move_to([x, base_y + h / 2, 0])
    g = VGroup(p)
    if tab:
        t = Rectangle(width=w * 0.7, height=0.14, stroke_width=0, fill_color=YELLOW, fill_opacity=1.0)
        t.move_to([x, base_y + h - 0.02, 0])
        g.add(t)
    return g


def dot(x, y, r=0.1, color=GREEN, op=1.0):
    return Circle(radius=r, stroke_width=0, fill_color=color, fill_opacity=op).move_to([x, y, 0])


def panel_box(cx, cy, w, h, color=GREY, fill=BG):
    return RoundedRectangle(corner_radius=0.12, width=w, height=h, stroke_color=color, stroke_width=2.5,
                            fill_color=fill, fill_opacity=1.0).move_to([cx, cy, 0])


def tag(text, size=22):
    return T(text, size, GOLD)


# ---------------------------------------------------------------------------------------------
class S00Title(TitleCard):
    LESSON = "Methods library"
    TITLE = "Seeing Where a Protein Sits"


# ---------------------------------------------------------------------------------------------
class S01Problem(SpokenScene):
    """cells shown by shape; which protein? an antibody lights the cells that hold it; three questions."""

    def construct(self):
        rng = np.random.RandomState(4)
        xs = [-5.2, -3.5, -1.8, -0.1]
        ys = [1.55, -0.1, -1.75]
        cells = []
        for j, y in enumerate(ys):
            for i, x in enumerate(xs):
                dx, dy = rng.uniform(-0.12, 0.12, 2)
                cells.append(cellc(x + dx + (0.4 if j == 1 else 0), y + dy, rng.uniform(0.62, 0.78)))
        field = VGroup(*cells).scale(1.1).move_to([-1.5, -0.05, 0])
        flab = lab("cell bodies, cell shapes", 26, GREY).move_to([-1.5, 3.1, 0])
        qs = VGroup(*[T("?", 38, YELLOW, weight=BOLD).move_to(c[0].get_center()) for c in cells])
        which = lab("which protein?", 28, YELLOW).move_to([-1.5, -3.25, 0])

        self.at("and Golgi stains")
        self.play(LaggedStart(*[FadeIn(c) for c in cells], lag_ratio=0.06), FadeIn(flab), run_time=1.6)
        self.at("They do not say")
        self.play(LaggedStart(*[FadeIn(q, scale=0.6) for q in qs], lag_ratio=0.05), FadeIn(which), run_time=1.2)

        # the antibody
        self.at("Immunostaining uses")
        ab = Yab(4.3, 0.5, BLUE, 1.7)
        ab_lbl = lines("antibody against", "one chosen protein", size=26, color=BLUE).move_to([4.3, 2.3, 0])
        hit = [0, 2, 5, 8, 11]
        self.play(FadeOut(qs), FadeOut(which), FadeOut(flab), FadeIn(ab, shift=DOWN * 0.3), FadeIn(ab_lbl), run_time=0.8)
        self.at("so it reports")
        glow = [cells[k][0].animate.set_stroke(GREEN, 4).set_fill(GREEN, 0.45) for k in hit]
        ident = chip("molecular identity", GREEN, 28).move_to([4.3, -1.0, 0])
        self.play(*glow, FadeIn(ident, shift=UP * 0.15), run_time=0.9)

        # three questions
        self.at("It answers three questions")
        self.play(FadeOut(ab), FadeOut(ab_lbl), FadeOut(ident), run_time=0.5)
        q1 = chip("In which cells?", YELLOW, 26).move_to([4.3, 2.0, 0])
        q2 = chip("In which part\nof the cell?", YELLOW, 26).move_to([4.3, 0.3, 0])
        q3 = chip("Overlap with\nanother protein?", YELLOW, 26).move_to([4.3, -1.7, 0])
        self.at("In which cells")
        self.play(FadeIn(q1, shift=LEFT * 0.2), *[Indicate(cells[k][0], color=GREEN, scale_factor=1.15) for k in hit], run_time=1.0)
        self.at("In which part")
        ring = Circle(radius=cells[0][1].width / 2 + 0.07, stroke_color=YELLOW, stroke_width=4).move_to(cells[0][1].get_center())
        self.play(FadeIn(q2, shift=LEFT * 0.2), Create(ring), run_time=0.7)
        self.at("And does it overlap")
        m1 = [dot(cells[k].get_center()[0] + dx, cells[k].get_center()[1] + dy, 0.09, MAGENTA) for k, dx, dy in
              [(2, 0.3, -0.3), (5, -0.3, 0.3), (8, 0.3, 0.25)]]
        self.play(FadeIn(q3, shift=LEFT * 0.2), *[FadeIn(m, scale=0.4) for m in m1], run_time=0.8)
        self.finish()


# ---------------------------------------------------------------------------------------------
class S02Prepare(SpokenScene):
    """fix (bridges lock proteins), section onto a slide, permeabilize, block."""

    def construct(self):
        names = ["1 fix", "2 section", "3 open membranes", "4 block"]
        bar = VGroup(*[chip(n, GREY, 22, pad=0.14) for n in names]).arrange(RIGHT, buff=0.3).move_to([0, 3.1, 0])

        def lit(i):
            return [bar[k].animate.set_color(TEAL if k == i else GREY) for k in range(4)]

        self.add(bar)
        # ---- 1. fix
        self.at("First fix the tissue")
        self.play(*lit(0), run_time=0.3)
        BX, BY, BW, BH = -3.8, 0.0, 4.0, 2.8
        block = RoundedRectangle(corner_radius=0.15, width=BW, height=BH, stroke_color=GREY, stroke_width=3,
                                 fill_color=GREY, fill_opacity=0.3).move_to([BX, BY, 0])
        btxt = lab("tissue", 28, TEXT).move_to(block)
        fixc = chip("formaldehyde", TEAL, 26).move_to([BX, 2.35, 0])
        fa = arr([BX, 1.95, 0], [BX, 1.55, 0], TEAL, w=5, tip=0.18)
        self.play(FadeIn(block), FadeIn(btxt), run_time=0.5)
        self.play(FadeIn(fixc, shift=DOWN * 0.15), GrowArrow(fa), run_time=0.5)
        # close-up
        CX, CY, CR = 3.3, 0.0, 2.3
        lens = Circle(radius=CR, stroke_color=GREY, stroke_width=3).move_to([CX, CY, 0])
        l1 = Line([BX + BW / 2, 0.5, 0], [CX - 2.2, 0.8, 0], color=GREY, stroke_width=2)
        l2 = Line([BX + BW / 2, -0.5, 0], [CX - 2.2, -0.8, 0], color=GREY, stroke_width=2)
        P = [(CX + a, CY + b) for a, b in [(-1.05, 1.0), (1.05, 0.85), (-1.15, -0.85), (0.95, -1.0), (0.0, 0.1)]]
        prot = VGroup(*[Circle(radius=0.3, stroke_color=PURPLE, stroke_width=2.5, fill_color=PURPLE,
                               fill_opacity=0.5).move_to([x, y, 0]) for x, y in P])
        plab = lab("proteins", 24, PURPLE).move_to([CX, CY + CR + 0.3, 0])
        self.play(Create(lens), Create(l1), Create(l2), FadeIn(prot), FadeIn(plab), run_time=0.8)
        self.at("amine groups")
        pairs = [(0, 4), (4, 0), (1, 4), (4, 1), (2, 4), (4, 2), (3, 4), (4, 3)]
        amine = VGroup(*[dot(P[a][0] + (P[b][0] - P[a][0]) * 0.36, P[a][1] + (P[b][1] - P[a][1]) * 0.36, 0.08, TEAL) for a, b in pairs])
        am_lbl = lab("amine groups", 24, TEAL).move_to([CX, -CY - CR - 0.3, 0])
        self.play(FadeIn(amine, scale=0.3), FadeIn(am_lbl), run_time=0.6)
        self.at("methylene bridges")
        br = VGroup(*[Line([P[a][0], P[a][1], 0], [P[4][0], P[4][1], 0], color=TEAL, stroke_width=8) for a in range(4)])
        br_lbl = lab("methylene bridges", 24, TEAL).move_to([CX, -CY - CR - 0.3, 0])
        self.play(FadeOut(amine), Create(br), ReplacementTransform(am_lbl, br_lbl), run_time=0.9)
        self.at("That locks proteins")
        lock = lab("proteins locked in place", 24, TEXT).move_to([CX, -CY - CR - 0.75, 0])
        self.play(FadeIn(lock), *[Indicate(p, color=PURPLE, scale_factor=1.1) for p in prot], run_time=0.8)

        # ---- 2. section
        self.at("Then cut")
        self.play(*lit(1), FadeOut(VGroup(lens, l1, l2, prot, plab, br, br_lbl, lock, fixc, fa)), run_time=0.4)
        top = BY + BH / 2
        knife = Rectangle(width=BW + 0.4, height=0.07, stroke_width=0, fill_color=TEXT, fill_opacity=1).move_to([BX, top + 0.4, 0])
        slab = Rectangle(width=BW, height=0.24, stroke_color=GREY, stroke_width=2, fill_color=GREY, fill_opacity=0.5).move_to([BX, top - 0.14, 0])
        slide = Rectangle(width=5.4, height=0.4, stroke_color=BLUE, stroke_width=3, fill_color=BLUE, fill_opacity=0.18).move_to([3.0, -0.9, 0])
        slide_lbl = lab("glass slide", 24, BLUE).move_to([3.0, -1.5, 0])
        self.play(knife.animate.move_to([BX, top - 0.28, 0]), run_time=0.4)
        self.play(FadeIn(slab), FadeOut(btxt), block.animate.stretch_to_fit_height(BH - 0.3).shift(DOWN * 0.15),
                  knife.animate.shift(UP * 0.4).set_opacity(0), FadeIn(slide), FadeIn(slide_lbl), run_time=0.4)
        self.play(slab.animate.stretch_to_fit_width(4.4).move_to([3.0, -0.6, 0]), run_time=0.8)
        sec_lbl = lab("section", 24, TEXT).move_to([3.0, -0.1, 0])
        self.play(FadeIn(sec_lbl), run_time=0.2)

        # ---- 3. permeabilize
        self.at("Open the membranes")
        self.play(*lit(2), FadeOut(VGroup(block, slab, slide, slide_lbl, sec_lbl, knife)), run_time=0.4)
        CCX = 0.6
        cell = Circle(radius=1.9, stroke_color=GREY, stroke_width=6, fill_color=GREY, fill_opacity=0.12).move_to([CCX, -0.1, 0])
        cnuc = Circle(radius=0.75, stroke_color=GREY, stroke_width=2, fill_color=GREY, fill_opacity=0.08).move_to([CCX, -0.1, 0])
        cname = lab("cell", 24, GREY).move_to([CCX, 2.3, 0])
        ab = Yab(-4.0, -0.1, BLUE, 1.5, down=False)
        ab.rotate(-PI / 2, about_point=ab.get_center())
        ab_lbl = lab("antibody", 26, BLUE).move_to([-4.0, 0.9, 0])
        self.play(FadeIn(cell), FadeIn(cnuc), FadeIn(cname), FadeIn(ab), FadeIn(ab_lbl), run_time=0.5)
        det = chip("detergent", TEAL, 26).move_to([4.6, 1.7, 0])
        da = arr([3.9, 1.35, 0], [2.4, 0.5, 0], TEAL, w=5, tip=0.18)
        open_cell = DashedVMobject(Circle(radius=1.9, stroke_color=GREY, stroke_width=6).move_to([CCX, -0.1, 0]), num_dashes=24)
        self.play(FadeIn(det, shift=LEFT * 0.2), GrowArrow(da), FadeOut(cell), FadeIn(open_cell), run_time=0.7)
        self.at("so antibodies can reach")
        self.play(FadeOut(ab_lbl), ab.animate.move_to([CCX - 0.9, -0.1, 0]), run_time=1.0)
        reach = lab("antibody reaches inside", 24, BLUE).move_to([CCX, -2.65, 0])
        self.play(FadeIn(reach), run_time=0.3)

        # ---- 4. block
        self.at("Then block")
        self.play(*lit(3), FadeOut(VGroup(open_cell, cnuc, cname, ab, det, da, reach)), run_time=0.4)
        WY = -1.2
        wall = Rectangle(width=11.6, height=0.3, stroke_color=GREY, stroke_width=2.5, fill_color=GREY, fill_opacity=0.35).move_to([0, WY, 0])
        wall_lbl = lab("section surface", 24, GREY).move_to([-4.6, WY - 0.6, 0])
        sx = [-5.2, -3.0, -0.8, 1.4]
        sites = VGroup(*[dot(x, WY + 0.18, 0.17, RED) for x in sx])
        tpeg = peg(4.6, WY + 0.15, 1.0)
        tpeg_lbl = lab("target protein", 24, PURPLE).move_to([4.6, WY - 0.6, 0])
        stuck = Yab(sx[2], WY + 0.18 + 0.75, BLUE, 1.5, down=True)
        stuck_lbl = lab("unwanted sticking", 26, RED).move_to([-0.8, 1.3, 0])
        self.play(FadeIn(wall), FadeIn(wall_lbl), FadeIn(sites), FadeIn(tpeg), FadeIn(tpeg_lbl), FadeIn(stuck, shift=DOWN * 0.4),
                  FadeIn(stuck_lbl), run_time=0.8)
        self.at("using a protein")
        bsa = chip("BSA", TEAL, 26).move_to([-3.6, 2.0, 0])
        ser = chip("normal serum", TEAL, 26).move_to([-1.0, 2.0, 0])
        cover = VGroup(*[dot(x, WY + 0.18, 0.24, TEAL, 0.9) for x in sx])
        self.play(FadeIn(bsa, shift=DOWN * 0.1), FadeIn(ser, shift=DOWN * 0.1), run_time=0.5)
        self.play(ReplacementTransform(sites, cover), FadeOut(stuck_lbl), stuck.animate.move_to([4.6, 0.67, 0]), run_time=1.2)
        self.finish()


# ---------------------------------------------------------------------------------------------
class S03Antibodies(SpokenScene):
    """primary binds target by its variable end; labeled secondary binds its constant end; fluorophore or enzyme."""

    def construct(self):
        MY = -2.35
        mem = membrane(-6.3, 6.3, MY)
        base = MY + 0.15
        cxL, cxR = -3.0, 4.2
        s = 1.5

        def complex_(cx):
            p1, p2 = peg(cx - 0.57, base), peg(cx + 0.57, base)
            tip_y = base + 0.8 - 0.02 + 0.07
            jy = tip_y + 0.5 * s
            prim = Yab(cx, jy, BLUE, s, down=True)
            stem_top = jy + 0.55 * s
            sec = Yab(cx, stem_top + 0.5 * s, ORANGE, s, down=True)
            top = stem_top + 0.5 * s + 0.55 * s
            return p1, p2, prim, sec, top, jy, stem_top

        p1, p2, prim, sec, topL, jy, stem_top = complex_(cxL)
        self.add(mem, p1, p2)
        tgt_lbl = lab("target protein", 22, PURPLE).move_to([cxL, base - 0.55, 0])
        self.add(tgt_lbl)

        sch = lab("schematic icons, not to scale", 22, GREY).move_to([-3.6, -3.35, 0])
        self.add(sch)
        self.at("Now apply the primary")
        prim.shift(UP * 2.6)
        self.play(FadeIn(prim), run_time=0.3)
        self.play(prim.animate.shift(DOWN * 2.6), run_time=1.2)
        self.at("It binds its epitope")
        ep = lab("epitope", 22, YELLOW).move_to([cxL - 1.95, base + 0.85, 0])
        ve = lab("variable end", 22, BLUE).move_to([cxL - 1.95, base + 1.3, 0])
        self.play(FadeIn(ep), FadeIn(ve), *[Indicate(p[1], color=YELLOW, scale_factor=1.6) for p in (p1, p2)], run_time=0.9)

        # secondary
        self.at("Next comes a labeled")
        sec.shift(UP * 1.8)
        dotL = dot(cxL, topL + 0.12, 0.15, GREEN)
        dotL.shift(UP * 1.8)
        sec_lbl = lines("labeled", "secondary", size=22, color=ORANGE).move_to([cxL - 1.95, jy + 1.85, 0])
        self.play(FadeIn(sec), FadeIn(dotL), FadeIn(sec_lbl), run_time=0.4)
        self.play(sec.animate.shift(DOWN * 1.8), dotL.animate.shift(DOWN * 1.8), run_time=1.0)
        self.at("It binds the constant")
        cl = lab("constant end", 24, BLUE).move_to([cxL + 1.85, stem_top - 0.5, 0])
        ca = arr([cxL + 0.75, stem_top - 0.5, 0], [cxL + 0.1, stem_top - 0.06, 0], BLUE, w=3, tip=0.12)
        self.play(FadeIn(cl), GrowArrow(ca), run_time=0.6)
        self.at("A rabbit primary")
        rp = lines("rabbit primary", size=22, color=BLUE).move_to([cxL - 1.95, jy + 0.55, 0])
        self.play(FadeIn(rp), run_time=0.4)
        self.at("by an")
        asec = lines("anti-rabbit", "secondary", size=22, color=ORANGE).move_to([cxL - 1.95, jy + 1.45, 0])
        self.play(FadeOut(sec_lbl), FadeIn(asec), run_time=0.4)

        # label
        self.at("The label is a fluorophore")
        halo = Circle(radius=0.34, stroke_width=0, fill_color=GREEN, fill_opacity=0.3).move_to(dotL)
        fl = lab("fluorophore", 24, GREEN).move_to([cxL + 1.5, topL + 0.12, 0])
        self.play(FadeIn(halo, scale=0.5), FadeIn(fl), run_time=0.5)
        self.play(halo.animate.scale(1.5).set_opacity(0.18), run_time=0.5)
        imm = lab("immunofluorescence", 22, GREEN).move_to([cxL + 0.0, topL + 1.0, 0])
        self.play(FadeIn(imm), run_time=0.3)

        self.at("or an enzyme such as")
        q1, q2, prim2, sec2, topR, jy2, st2 = complex_(cxR)
        hexa = RegularPolygon(6, radius=0.2, stroke_color=TAN, stroke_width=3, fill_color=TAN, fill_opacity=0.9).move_to([cxR, topR + 0.14, 0])
        self.play(FadeIn(q1), FadeIn(q2), FadeIn(prim2), FadeIn(sec2), FadeIn(hexa), run_time=0.7)
        en = lab("enzyme", 24, TAN).next_to(hexa, RIGHT, buff=0.18)
        hrp = lab("horseradish peroxidase", 22, TAN).move_to([cxR + 0.0, topR + 1.0, 0])
        self.play(FadeIn(en), FadeIn(hrp), run_time=0.4)
        self.at("The enzyme makes")
        prod = Ellipse(width=3.0, height=4.3, stroke_color=TAN, stroke_width=3, fill_color=TAN, fill_opacity=0.18).move_to([cxR, (base + topR) / 2, 0])
        prod_lbl = lines("colored product", "at the site", size=22, color=TAN).move_to([cxR - 3.0, 0.0, 0])
        self.play(GrowFromCenter(prod), FadeIn(prod_lbl), run_time=1.0)
        self.at("That gives a permanent")
        perm = lines("permanent preparation,", "ordinary microscope", size=22, color=TAN).move_to([cxR, MY - 0.75, 0])
        self.play(FadeIn(perm, shift=UP * 0.1), run_time=0.6)
        self.finish()


# ---------------------------------------------------------------------------------------------
def image_panel(cx, cy, w, h, seed=3, kinds=None, ncols=4, nrows=3, label=True):
    """Idealised microscope image: dark field with faint cell outlines. kinds: list of 'g','m','b','' per cell."""
    rng = np.random.RandomState(seed)
    box = panel_box(cx, cy, w, h)
    cells = VGroup()
    marks = VGroup()
    cw, ch = w / ncols, h / nrows
    n = 0
    for j in range(nrows):
        for i in range(ncols):
            x = cx - w / 2 + cw * (i + 0.5) + rng.uniform(-0.08, 0.08)
            y = cy + h / 2 - ch * (j + 0.5) + rng.uniform(-0.06, 0.06)
            r = min(cw, ch) * 0.38
            cells.add(Circle(radius=r, stroke_color=GREY, stroke_width=2, fill_opacity=0).move_to([x, y, 0]).set_stroke(opacity=0.5))
            k = kinds[n] if kinds and n < len(kinds) else ""
            for col, ch_ in (("g", GREEN), ("m", MAGENTA)):
                if k in (col, "b"):
                    for _ in range(3):
                        a, b = rng.uniform(-r * 0.55, r * 0.55, 2)
                        marks.add(dot(x + a, y + b, 0.08 if w < 6 else 0.1, ch_ if k != "b" else (GREEN if _ < 2 else MAGENTA)))
                    if k == "b":
                        break
            n += 1
    cap = lab("example image, idealised", 22, GREY).move_to([cx, cy - h / 2 - 0.3, 0]) if label else VGroup()
    return VGroup(box, cells, marks, cap), box, cells, marks, cap


class S04Imaging(SpokenScene):
    """slide under a fluorescence microscope -> an image; confocal pinhole + stacked sections; two colors in one cell."""

    def construct(self):
        # ---- A: fluorescence microscope
        slide = Rectangle(width=4.4, height=0.4, stroke_color=BLUE, stroke_width=3, fill_color=BLUE, fill_opacity=0.18).move_to([-3.6, -2.6, 0])
        sec = Rectangle(width=3.4, height=0.18, stroke_color=GREY, stroke_width=2, fill_color=GREY, fill_opacity=0.5).move_to([-3.6, -2.3, 0])
        sd = VGroup(*[dot(-4.7 + 0.55 * i, -2.3, 0.07, GREEN) for i in range(3)] + [dot(-2.5, -2.3, 0.07, GREEN)])
        lens = Polygon([-4.5, 0.6, 0], [-2.7, 0.6, 0], [-3.1, 1.2, 0], [-4.1, 1.2, 0], stroke_color=BLUE, stroke_width=4,
                       fill_color=BLUE, fill_opacity=0.25)
        rays = VGroup(*[arr([x, -2.1, 0], [x * 0.55 - 3.6 * 0.45 + 0.0, 0.5, 0], GREEN, w=3, tip=0.14) for x in (-4.4, -3.6, -2.8)])
        mic_lbl = chip("fluorescence microscope", BLUE, 24).move_to([-3.6, 2.2, 0])
        img, ibox, icells, imarks, icap = image_panel(3.3, 0.1, 5.2, 4.2, seed=3,
                                                       kinds=["", "g", "", "g", "g", "", "", "g", "", "", "g", ""])
        self.at("fluorescent slide")
        self.play(FadeIn(slide), FadeIn(sec), FadeIn(sd), run_time=0.5)
        self.play(FadeIn(lens), FadeIn(mic_lbl), *[GrowArrow(r) for r in rays], run_time=0.8)
        self.play(FadeIn(ibox), FadeIn(icells), FadeIn(imarks, scale=0.5), FadeIn(icap), run_time=0.8)

        # ---- B: confocal
        self.at("Or use a confocal")
        self.play(FadeOut(VGroup(slide, sec, sd, lens, rays, mic_lbl)), run_time=0.5)
        cx = -3.6
        plate = VGroup(Rectangle(width=2.4, height=0.2, stroke_width=0, fill_color=BLUE, fill_opacity=0.9).move_to([cx - 1.45, 1.7, 0]),
                       Rectangle(width=2.4, height=0.2, stroke_width=0, fill_color=BLUE, fill_opacity=0.9).move_to([cx + 1.45, 1.7, 0]))
        lensb = Polygon([cx - 1.0, 0.0, 0], [cx + 1.0, 0.0, 0], [cx + 0.6, 0.55, 0], [cx - 0.6, 0.55, 0], stroke_color=BLUE, stroke_width=4,
                        fill_color=BLUE, fill_opacity=0.25)
        focus_pt = dot(cx, -2.3, 0.14, GREEN)
        far_pt = dot(cx, -1.2, 0.14, RED)
        self.play(FadeIn(plate), FadeIn(lensb), FadeIn(focus_pt), FadeIn(far_pt), run_time=0.6)
        self.at("a pinhole")
        pin_lbl = lab("pinhole", 26, BLUE).move_to([cx, 2.3, 0])
        good = VGroup(Line([cx, -2.2, 0], [cx - 0.7, 0.05, 0], color=GREEN, stroke_width=4), Line([cx, -2.2, 0], [cx + 0.7, 0.05, 0], color=GREEN, stroke_width=4),
                      Line([cx - 0.7, 0.55, 0], [cx, 1.7, 0], color=GREEN, stroke_width=4), Line([cx + 0.7, 0.55, 0], [cx, 1.7, 0], color=GREEN, stroke_width=4))
        bad = VGroup(Line([cx, -1.1, 0], [cx - 0.7, 0.05, 0], color=RED, stroke_width=4), Line([cx, -1.1, 0], [cx + 0.7, 0.05, 0], color=RED, stroke_width=4),
                     Line([cx - 0.7, 0.55, 0], [cx - 1.2, 1.58, 0], color=RED, stroke_width=4), Line([cx + 0.7, 0.55, 0], [cx + 1.2, 1.58, 0], color=RED, stroke_width=4))
        self.play(FadeIn(pin_lbl), Create(good), run_time=0.8)
        self.at("rejects")
        fl = lines("in focus:", "passes", size=24, color=GREEN).move_to([cx + 1.9, -2.3, 0])
        ol = lines("out of focus:", "blocked", size=24, color=RED).move_to([cx + 2.2, -1.1, 0])
        self.play(Create(bad), FadeIn(ol), FadeIn(fl), run_time=0.9)
        self.at("optical sections")
        self.play(FadeOut(VGroup(ibox, icells, imarks, icap)), run_time=0.4)
        sheets = VGroup()
        for k in range(3):
            o = np.array([3.3 - 0.4 * (2 - k) * 0.0, -1.1 + 1.0 * k, 0])
            pg = Polygon([-2.0, -0.7, 0], [1.6, -0.7, 0], [2.3, 0.5, 0], [-1.3, 0.5, 0], stroke_color=GREY, stroke_width=2.5,
                         fill_color=BG, fill_opacity=0.95).shift(o)
            ds = VGroup(*[dot(o[0] + a, o[1] + b, 0.08, GREEN) for a, b in [(-0.8 + 0.2 * k, -0.2), (0.6 - 0.3 * k, 0.1), (0.1 + 0.3 * k, -0.3)]])
            sheets.add(VGroup(pg, ds))
        sh_lbl = lab("optical sections, stacked", 24, TEXT).move_to([3.3, -2.35, 0])
        sheets_ordered = VGroup(*sheets)
        self.play(LaggedStart(*[FadeIn(sh, shift=UP * 0.2) for sh in sheets_ordered], lag_ratio=0.35), FadeIn(sh_lbl), run_time=1.4)

        # ---- C: two colors
        self.at("Use several antibodies")
        self.play(FadeOut(VGroup(plate, lensb, focus_pt, far_pt, pin_lbl, good, bad, fl, ol, sheets, sh_lbl)), run_time=0.5)
        kinds = ["g", "", "m", "g", "m", "b", "", "g", "", "m", "m", ""]
        img2, b2, c2, m2, cap2 = image_panel(0, 0.1, 8.4, 4.6, seed=8, kinds=kinds)
        leg1 = lab("marker 1", 24, GREEN).move_to([-3.2, -2.95, 0])
        leg2 = lab("marker 2", 24, MAGENTA).move_to([-1.2, -2.95, 0])
        self.play(FadeIn(b2), FadeIn(c2), FadeIn(m2, scale=0.5), FadeIn(cap2), run_time=0.7)
        self.play(FadeIn(leg1), FadeIn(leg2), run_time=0.4)
        self.at("coincide in one cell")
        both = c2[5]
        ring = Circle(radius=both.width / 2 + 0.1, stroke_color=YELLOW, stroke_width=5).move_to(both)
        bl = lab("both markers in one cell", 24, YELLOW).move_to([3.0, -2.95, 0])
        self.play(Create(ring), FadeIn(bl), run_time=0.8)
        self.finish()


# ---------------------------------------------------------------------------------------------
class S05Reading(SpokenScene):
    """where it sits (nucleus, crescent, lysosome surface); saturation hides amount; overlap = proximity."""

    def construct(self):
        top = lab("example, idealised", 22, GREY).move_to([0, 3.1, 0])
        xs = [-4.2, 0.0, 4.2]
        cy = 0.7
        cs = [Circle(radius=1.6, stroke_color=GREY, stroke_width=3, fill_color=GREY, fill_opacity=0.12).move_to([x, cy, 0]) for x in xs]
        ns = [Circle(radius=0.65, stroke_color=GREY, stroke_width=2, fill_color=GREY, fill_opacity=0.08).move_to([x, cy, 0]) for x in xs]
        self.at("Read the image")
        self.play(FadeIn(top), *[FadeIn(c) for c in cs], *[FadeIn(n) for n in ns], run_time=1.0)
        self.at("Signal in the nucleus")
        self.play(ns[0].animate.set_stroke(GREEN, 3).set_fill(GREEN, 0.75), run_time=0.7)
        l1 = lines("in the nucleus:", "transcription factor, Fos", size=26, color=TEXT).move_to([xs[0], -1.6, 0])
        self.play(FadeIn(l1), run_time=0.4)
        self.at("A crescent on the membrane")
        cres = Arc(radius=1.6, start_angle=PI - 0.9, angle=1.8, stroke_color=GREEN, stroke_width=14)
        cres.shift(np.array([xs[1], cy, 0]) - cres.get_arc_center())
        l2 = lines("on the membrane:", "a crescent", size=26, color=TEXT).move_to([xs[1], -1.6, 0])
        self.play(Create(cres), FadeIn(l2), run_time=0.8)
        self.at("on a lysosome surface")
        lys = VGroup()
        for dx, dy in [(-0.9, 0.6), (0.9, 0.7), (-0.6, -0.7), (0.8, -0.6)]:
            lys.add(Circle(radius=0.28, stroke_color=GREEN, stroke_width=5, fill_color=GREY, fill_opacity=0.25).move_to([xs[2] + dx, cy + dy, 0]))
        l3 = lines("on a lysosome", "surface", size=26, color=TEXT).move_to([xs[2], -1.6, 0])
        self.play(FadeIn(lys, scale=0.5), FadeIn(l3), run_time=0.8)

        # amount: saturation
        self.at("Counting stained nuclei")
        self.play(FadeOut(VGroup(top, *cs, *ns, cres, lys, l1, l2, l3)), run_time=0.5)
        ox, oy = -5.0, -2.4
        xaxis = Line([ox, oy, 0], [ox + 8.2, oy, 0], color=GREY, stroke_width=3)
        yaxis = Line([ox, oy, 0], [ox, oy + 4.9, 0], color=GREY, stroke_width=3)
        xl = lab("label present", 24, GREY).move_to([ox + 4.1, oy - 0.45, 0])
        yl = lab("pixel value", 24, GREY).rotate(PI / 2).move_to([ox - 0.5, oy + 2.45, 0])
        curve = VMobject().set_points_as_corners([[ox, oy, 0], [ox + 4.0, oy + 3.6, 0], [ox + 8.0, oy + 3.6, 0]]).set_stroke(YELLOW, 6)
        ex = lab("example, idealised", 22, GREY).move_to([ox + 7.0, oy + 5.05, 0])
        thr = DashedLine([ox, oy + 1.2, 0], [ox + 8.2, oy + 1.2, 0], color=TEAL, stroke_width=3)
        thr_l = lab("threshold", 24, TEAL).move_to([ox + 7.2, oy + 1.55, 0])
        self.play(Create(xaxis), Create(yaxis), FadeIn(xl), FadeIn(yl), FadeIn(ex), Create(curve, run_time=1.2, rate_func=linear))
        self.at("a threshold and matched")
        ms = chip("matched settings", TEAL, 26).move_to([ox + 1.9, oy + 4.3, 0])
        self.play(Create(thr), FadeIn(thr_l), FadeIn(ms), run_time=0.8)
        self.at("Saturated pixels")
        p1, p2 = [ox + 5.4, oy + 3.6, 0], [ox + 7.4, oy + 3.6, 0]
        d1, d2 = dot(p1[0], p1[1], 0.14, RED), dot(p2[0], p2[1], 0.14, RED)
        v1 = DashedLine([p1[0], oy, 0], p1, color=GREY, stroke_width=2)
        v2 = DashedLine([p2[0], oy, 0], p2, color=GREY, stroke_width=2)
        sat = lines("saturated: same value,", "different amounts", size=24, color=RED).move_to([ox + 6.9, oy + 4.3, 0])
        self.play(Create(v1), Create(v2), FadeIn(d1), FadeIn(d2), FadeIn(sat), run_time=1.0)

        # overlap
        self.at("Where two colors overlap")
        self.play(FadeOut(VGroup(xaxis, yaxis, xl, yl, curve, ex, thr, thr_l, ms, d1, d2, v1, v2, sat)), run_time=0.5)
        a = Circle(radius=1.9, stroke_color=GREEN, stroke_width=3, fill_color=GREEN, fill_opacity=0.4).move_to([-1.2, 0.9, 0])
        b = Circle(radius=1.9, stroke_color=MAGENTA, stroke_width=3, fill_color=MAGENTA, fill_opacity=0.4).move_to([1.2, 0.9, 0])
        la = lab("marker 1", 28, GREEN).move_to([-4.9, 0.9, 0])
        lb = lab("marker 2", 28, MAGENTA).move_to([4.9, 0.9, 0])
        self.play(FadeIn(a), FadeIn(b), FadeIn(la), FadeIn(lb), run_time=0.8)
        self.at("That is proximity")
        c1 = chip("close together: proximity", YELLOW, 30).move_to([-2.9, -2.0, 0])
        c2 = chip("interaction: not shown", GREY, 30).move_to([3.2, -2.0, 0])
        self.play(FadeIn(c1, shift=UP * 0.15), FadeIn(c2, shift=UP * 0.15), run_time=0.8)
        self.finish()


# ---------------------------------------------------------------------------------------------
class S06Controls(SpokenScene):
    """bright is bound, not present; no-primary control; knockout tissue; peptide competition has limits."""

    def construct(self):
        PW, PH, PY = 3.9, 3.0, 0.95
        xs = [-4.3, 0.0, 4.3]
        cpos = [(-1.15, 0.65), (0.0, 0.65), (1.15, 0.65), (-0.6, -0.65), (0.6, -0.65)]
        boxes, cellsets = [], []
        for x in xs:
            boxes.append(panel_box(x, PY, PW, PH))
            cellsets.append(VGroup(*[Circle(radius=0.5, stroke_color=GREY, stroke_width=2, fill_opacity=0).move_to([x + a, PY + b, 0]).set_stroke(opacity=0.5)
                                     for a, b in cpos]))
        spots = VGroup(*[dot(xs[0] + a + 0.05, PY + b + 0.05, 0.13, GREEN) for a, b in cpos])
        self.at("Bright signal")
        h1 = lab("test section", 26, TEXT).move_to([xs[0], PY + 1.8, 0])
        self.play(FadeIn(boxes[0]), FadeIn(cellsets[0]), FadeIn(h1), run_time=0.5)
        self.play(FadeIn(spots, scale=0.4), run_time=0.5)
        c1 = lines("bright signal:", "antibody is bound", size=26, color=GREEN).move_to([xs[0], PY - 2.1, 0])
        self.play(FadeIn(c1), run_time=0.4)
        self.at("not necessarily that")
        q = lines("protein there?", size=28, color=YELLOW).move_to([xs[0], PY - 3.0, 0])
        self.play(FadeIn(q, scale=0.8), run_time=0.5)

        self.at("So run controls")
        h2 = lab("no primary", 26, TEXT).move_to([xs[1], PY + 1.8, 0])
        h3 = lab("knockout tissue", 26, TEXT).move_to([xs[2], PY + 1.8, 0])
        same = lab("matched tissue, same processing", 24, GREY).move_to([0, 3.3, 0])
        self.play(FadeIn(same), FadeIn(boxes[1]), FadeIn(cellsets[1]), FadeIn(boxes[2]), FadeIn(cellsets[2]), run_time=0.6)
        self.at("Omit the primary")
        c2 = lines("secondary only,", "no primary", size=26, color=ORANGE).move_to([xs[1], PY - 2.1, 0])
        self.play(FadeIn(h2), FadeIn(c2), run_time=0.6)
        self.at("any signal is")
        specks = VGroup(*[dot(xs[1] + a, PY + b, 0.09, RED) for a, b in [(-1.5, 0.15), (0.6, -0.15)]])
        c2b = lines("any signal is", "background", size=26, color=RED).move_to([xs[1], PY - 3.0, 0])
        self.play(FadeIn(specks, scale=0.4), FadeIn(c2b), run_time=0.7)

        self.at("Best of all")
        c3 = lines("protein absent", "(knockout)", size=26, color=TEXT).move_to([xs[2], PY - 2.1, 0])
        self.play(FadeIn(h3), FadeIn(c3), run_time=0.6)
        self.at("The signal should vanish")
        ghosts = VGroup(*[DashedVMobject(Circle(radius=0.13, stroke_color=GREEN, stroke_width=2).move_to([xs[2] + a + 0.05, PY + b + 0.05, 0]), num_dashes=8) for a, b in cpos])
        c3b = lines("signal gone", size=28, color=GREEN).move_to([xs[2], PY - 3.0, 0])
        self.play(FadeIn(ghosts), FadeIn(c3b), run_time=0.8)

        self.at("Peptide competition")
        pep = chip("peptide competition blocks the antibody with its target peptide.\nIt has limits: use other controls too.", YELLOW, 24)
        pep.move_to([0, -3.1, 0])
        self.play(FadeIn(pep, shift=UP * 0.15), run_time=0.7)
        self.finish()


# ---------------------------------------------------------------------------------------------
class S07Discoveries(SpokenScene):
    """left: Coons joins antibody to a fluorescent group, stained section seen in UV; right: Fos staining at three hours."""

    def construct(self):
        div = Line([0, 3.3, 0], [0, -3.4, 0], color=GREY, stroke_width=1.5).set_stroke(opacity=0.5)
        self.add(div)
        lx, rx = -3.2, 3.4
        rng = np.random.RandomState(9)
        # ---- left: Coons
        date1 = lab("early 1940s", 34, GOLD, weight=BOLD).move_to([lx, 3.0, 0])
        ab = Yab(lx - 0.5, 1.6, BLUE, 1.9)
        fg = dot(lx + 0.7, 1.6, 0.26, GREEN)
        join = Line([lx - 0.5 + 0.2, 1.6, 0], [lx + 0.7 - 0.26, 1.6, 0], color=GREEN, stroke_width=6)
        j_lbl = lab("antibody + fluorescent group", 28, GREEN).move_to([lx, 0.05, 0])
        sec = Rectangle(width=5.2, height=1.4, stroke_color=GREY, stroke_width=2.5, fill_color=GREY, fill_opacity=0.3).move_to([lx, -1.15, 0])
        sec_l = lab("tissue section, stained with it", 26, TEXT).move_to([lx, -2.2, 0])
        spots = VGroup(*[dot(lx + rng.uniform(-2.3, 2.3), -1.15 + rng.uniform(-0.5, 0.5), 0.09, GREEN) for _ in range(14)])
        uv = VGroup(*[arr([lx + d, 0.1, 0], [lx + d, -0.4, 0], MAGENTA, w=4, tip=0.14) for d in (-1.8, -0.6, 0.6, 1.8)])
        uv_l = lab("ultraviolet light", 24, MAGENTA).move_to([lx + 3.0, 0.1, 0])
        t1 = tag("Coons and colleagues, early 1940s").move_to([lx, -3.2, 0])

        self.at("In the early 1940s")
        self.play(FadeIn(date1), FadeIn(ab, shift=RIGHT * 0.3), FadeIn(t1), run_time=0.6)
        self.at("joined antibody")
        self.play(FadeIn(fg, shift=LEFT * 0.3), run_time=0.4)
        self.play(Create(join), FadeIn(j_lbl), run_time=0.4)
        self.at("could be seen")
        self.play(FadeOut(j_lbl), FadeIn(sec), FadeIn(sec_l), run_time=0.5)
        self.at("ultraviolet light")
        uv_l.move_to([lx + 1.95, 0.45, 0])
        self.play(FadeIn(uv), FadeIn(uv_l), FadeIn(spots, scale=0.4), run_time=0.9)

        # ---- right: Fos
        date2 = lab("1988", 34, GOLD, weight=BOLD).move_to([rx, 3.0, 0])
        ctx = chip("rat cortex: stimulated", YELLOW, 26).move_to([rx, 2.1, 0])
        clock = lab("three hours later", 28, GOLD).move_to([rx, 1.35, 0])
        names = ["thalamus", "pontine nuclei", "globus pallidus", "cerebellum"]
        boxes, labs, fos = [], [], []
        for k, nme in enumerate(names):
            y = 0.4 - 0.85 * k
            b = RoundedRectangle(corner_radius=0.12, width=5.6, height=0.7, stroke_color=GREY, stroke_width=2.5, fill_color=GREY, fill_opacity=0.12).move_to([rx, y, 0])
            l = lab(nme, 24, TEXT).move_to([rx - 1.9, y, 0]).align_to(b, LEFT).shift(RIGHT * 0.2)
            ns = VGroup(*[VGroup(Circle(radius=0.11, stroke_color=GREEN, stroke_width=2, fill_color=GREEN, fill_opacity=0.9)).move_to(
                [rx + 0.5 + rng.uniform(-0.1, 2.1) * 1.0, y + rng.uniform(-0.2, 0.2), 0]) for _ in range(5)])
            boxes.append(b); labs.append(l); fos.append(ns)
        t2 = tag("Sagar, Sharp and Curran, 1988").move_to([rx, -3.4, 0])
        fos_lbl = lab("scattered nuclei with Fos staining", 24, GREEN).move_to([rx, -3.0, 0])

        self.at("In 1988")
        self.play(FadeIn(date2), run_time=0.4)
        self.at("stimulated rat cortex")
        self.play(FadeIn(ctx, shift=DOWN * 0.15), run_time=0.5)
        self.at("Three hours later")
        self.play(FadeIn(clock), *[FadeIn(b) for b in boxes], *[FadeIn(l) for l in labs], FadeIn(t2), run_time=0.7)
        self.at("nuclear")
        self.play(FadeIn(fos_lbl), run_time=0.3)
        self.at("thalamus")
        for k in range(4):
            self.play(boxes[k].animate.set_stroke(GREEN, 2.5), FadeIn(fos[k], scale=0.3), run_time=0.45)
        self.at("cellular map")
        box = SurroundingRectangle(VGroup(*boxes), color=GREEN, stroke_width=3, buff=0.12, corner_radius=0.15)
        self.play(Create(box), run_time=0.8)
        self.finish()


class S08Rule(SpokenScene):
    """left: Numb crescent passes to one daughter; right: mTORC1 moves to lysosomes; the rule."""

    def construct(self):
        div = Line([0, 3.3, 0], [0, -2.9, 0], color=GREY, stroke_width=1.5).set_stroke(opacity=0.5)
        self.add(div)
        lx, rx = -3.2, 3.4
        # ---- left: Numb
        date1 = lab("1994", 32, GOLD, weight=BOLD).move_to([lx, 3.0, 0])
        cy = 0.5
        cell = Circle(radius=1.5, stroke_color=GREY, stroke_width=3, fill_color=GREY, fill_opacity=0.12).move_to([lx, cy, 0])
        nuc = Circle(radius=0.5, stroke_color=GREY, stroke_width=2, fill_color=GREY, fill_opacity=0.08).move_to([lx, cy, 0])
        cres = Arc(radius=1.5, start_angle=PI - 0.95, angle=1.9, stroke_color=GREEN, stroke_width=14)
        cres.shift(np.array([lx, cy, 0]) - cres.get_arc_center())
        nm = lab("Numb", 30, GREEN, weight=BOLD).move_to([lx - 2.45, cy, 0])
        sop = lines("dividing Drosophila", "sensory organ precursor", size=22, color=GREY, buff=0.04).move_to([lx, 2.3, 0])
        t1 = tag("Rhyu, Jan and Jan, 1994").move_to([lx, -1.6, 0])
        d1 = Circle(radius=1.0, stroke_color=GREEN, stroke_width=4, fill_color=GREEN, fill_opacity=0.4).move_to([lx - 1.1, cy, 0])
        d2 = Circle(radius=1.0, stroke_color=GREY, stroke_width=3, fill_color=GREY, fill_opacity=0.1).move_to([lx + 1.1, cy, 0])
        dl1 = lab("one daughter cell", 24, GREEN).move_to([lx - 1.1, cy - 1.45, 0])
        self.at("In 1994")
        self.play(FadeIn(date1), FadeIn(cell), FadeIn(nuc), FadeIn(sop), FadeIn(t1), run_time=0.7)
        self.at("lay on one half")
        self.play(Create(cres), FadeIn(nm), run_time=0.8)
        self.at("passed to one daughter")
        self.play(FadeOut(VGroup(cell, nuc, cres, nm)), FadeIn(d1), FadeIn(d2), run_time=0.9)
        self.play(FadeIn(dl1), run_time=0.4)

        # ---- right: mTOR (schematic comparison of fixed cells)
        date2 = lab("2010", 34, GOLD, weight=BOLD).move_to([rx, 3.0, 0])
        sch = lab("schematic comparison of fixed cells", 22, GREY).move_to([rx, 2.45, 0])
        cy2 = 0.5
        cxs = [rx - 1.55, rx + 1.55]
        cells2 = [Circle(radius=1.4, stroke_color=GREY, stroke_width=3, fill_color=GREY, fill_opacity=0.12).move_to([x, cy2, 0]) for x in cxs]
        L = [(-0.55, 0.6), (0.6, 0.45), (0.0, -0.7)]
        lys = [VGroup(*[Circle(radius=0.22, stroke_color=MAGENTA, stroke_width=4, fill_color=MAGENTA, fill_opacity=0.25).move_to([x + a, cy2 + b, 0]) for a, b in L]) for x in cxs]
        scat = [(-0.1, 0.05), (0.2, 0.15), (-0.3, -0.1), (0.35, -0.2), (-0.05, 0.3), (0.3, -0.05)]
        gd1 = VGroup(*[dot(cxs[0] + a, cy2 + b, 0.09, GREEN) for a, b in scat])
        gd2 = VGroup()
        for (a, b) in L:
            for sgn in (1, -1):
                gd2.add(dot(cxs[1] + a + sgn * 0.22, cy2 + b, 0.09, GREEN))
        bl = lab("before amino acids", 24, TEAL).move_to([cxs[0], cy2 - 1.8, 0])
        al = lab("after amino acids", 24, TEAL).move_to([cxs[1], cy2 - 1.8, 0])
        t2 = tag("Sancak and colleagues, 2010").move_to([rx, -1.95, 0])
        self.at("In 2010")
        self.play(FadeIn(date2), FadeIn(sch), run_time=0.4)
        l_g = lab("mTOR", 24, GREEN).move_to([rx - 1.3, -2.55, 0])
        l_m = lab("lysosomal protein", 24, MAGENTA).move_to([rx + 1.2, -2.55, 0])
        self.play(FadeIn(cells2[0]), FadeIn(lys[0]), FadeIn(gd1), FadeIn(bl), FadeIn(t2), FadeIn(l_g), FadeIn(l_m), run_time=0.7)
        self.at("amino acids move")
        self.play(FadeIn(cells2[1]), FadeIn(lys[1]), FadeIn(al), run_time=0.6)
        self.at("to lysosomal membranes")
        self.play(FadeIn(gd2, scale=0.4), run_time=1.0)
        # ---- the rule
        self.at("A stain shows")
        rule = lab("A stain shows where antibody bound. Judge it against controls.", 30, GOLD, weight=BOLD)
        fit(rule, max_w=12.0)
        rule.move_to([0, -3.25, 0])
        self.play(FadeIn(rule, shift=UP * 0.15), run_time=0.8)
        self.finish()




class S09End(EndCard):
    LINE = "A stain shows where antibody bound. Judge it against controls."
