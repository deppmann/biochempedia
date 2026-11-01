"""Cortical areas: the cortex map is drawn twice  (Biochemistrypedia explainer)

The cortex is drawn as a flat bar seen from above, front on the left, back on the right.

COLOR MAP (one color per concept, whole video)
  PURPLE = motor area
  GREEN  = touch (somatosensory) area, and its barrels
  PINK   = visual area
  ORANGE = Emx2
  BLUE   = Pax6
  YELLOW = FGF8, the signal from the front edge
  TEXT   = thalamic axons (the input)
  RED    = a blocker / something removed
  GREY   = the sheet, labels, de-emphasized
"""
import numpy as np
from bp_style import *  # noqa: F401,F403

PURPLE = "#B58CD9"
ORANGE = "#F29E4C"
PINK = "#E58BB5"
W = 10.0
X0 = -4.6
AREA_COL = [PURPLE, GREEN, PINK]
WT = (0.38, 0.70)   # borders in the normal map, as fractions front to back


def xf(f, w=W, x0=X0):
    return x0 + f * w


def make_map(b1, b2, cy=0.0, h=1.5, w=W, x0=X0, labels=("motor", "touch", "vision"), op=0.38, sw=3):
    xs = [x0, x0 + b1 * w, x0 + b2 * w, x0 + w]
    blocks, labs = VGroup(), VGroup()
    for i in range(3):
        r = Rectangle(width=xs[i + 1] - xs[i], height=h, stroke_color=AREA_COL[i], stroke_width=sw,
                      fill_color=AREA_COL[i], fill_opacity=op).move_to([(xs[i] + xs[i + 1]) / 2, cy, 0])
        blocks.add(r)
        if labels[i]:
            t = T(labels[i], 24, TEXT)
            if t.width > r.width - 0.2:
                t.scale((r.width - 0.2) / t.width)
            t.move_to([r.get_center()[0], cy + h / 2 - 0.3, 0])
            labs.add(t)
    return VGroup(blocks, labs)


def sheet(cy, h, w=W, x0=X0, op=0.22):
    return Rectangle(width=w, height=h, stroke_color=GREY, stroke_width=3, fill_color=GREY,
                     fill_opacity=op).move_to([x0 + w / 2, cy, 0])


def strips(fn, color, cy, h, n=22, w=W, x0=X0):
    g = VGroup()
    for i in range(n):
        f = (i + 0.5) / n
        g.add(Rectangle(width=w / n, height=h, stroke_width=0, fill_color=color,
                        fill_opacity=float(fn(f))).move_to([x0 + f * w, cy, 0]))
    return g


def emx(f, k=0.55):
    return 0.05 + k * f


def pax(f, k=0.55):
    return 0.05 + k * (1 - f)


def barrels(cx, cy, cols=4, rows=3, sp=0.34, r=0.1, color=GREEN):
    g = VGroup()
    for i in range(cols):
        for j in range(rows):
            g.add(Circle(radius=r, stroke_color=color, stroke_width=2, fill_color=color, fill_opacity=0.7).move_to(
                [cx + (i - (cols - 1) / 2) * sp, cy + (j - (rows - 1) / 2) * sp, 0]))
    return g


def ends(cy, front="front", back="back", size=24):
    return VGroup(T(front, size, GREY).move_to([X0 + 0.45, cy, 0]), T(back, size, GREY).move_to([X0 + W - 0.4, cy, 0]))


def glow(x, y, r=0.34, dim=1.0):
    g = VGroup()
    for k, o in ((2.6, 0.08), (1.9, 0.14), (1.35, 0.25)):
        g.add(Circle(radius=r * k, stroke_width=0, fill_color=YELLOW, fill_opacity=o * dim))
    g.add(Circle(radius=r, stroke_color=YELLOW, stroke_width=3, stroke_opacity=max(0.3, dim),
                 fill_color=YELLOW, fill_opacity=0.95 * dim))
    return g.move_to([x, y, 0])


class S00Title(TitleCard):
    LESSON = "Mapping the cortex: areas and arealization"
    TITLE = "The cortex map is drawn twice"


# ---------------------------------------------------------------------------------------------
class S01Sheet(SpokenScene):
    """adult map (whiskers, eyes) below a blank embryonic sheet; the question between them."""

    def construct(self):
        adult_cy, emb_cy, h = -1.5, 1.9, 1.9
        outline = Rectangle(width=W, height=h, stroke_color=GREY, stroke_width=3).move_to([X0 + W / 2, adult_cy, 0])
        tag_a = T("adult mouse cortex, from above", 24, GREY).move_to([0.4, -2.95, 0])
        self.at("In an adult mouse")
        self.play(Create(outline), FadeIn(tag_a), run_time=0.8)
        m = make_map(*WT, cy=adult_cy, h=h, labels=("", "whiskers", "eyes"))
        dots = barrels(xf(0.54), adult_cy - 0.2, cols=4, rows=3, sp=0.3, r=0.09)
        self.at("maps the whiskers")
        self.play(FadeIn(m[0][1]), FadeIn(m[1][0]), run_time=0.5)
        self.play(FadeIn(dots, lag_ratio=0.1), run_time=0.7)
        self.at("what the eyes see")
        self.play(FadeIn(m[0][2]), FadeIn(m[1][1]), run_time=0.6)

        emb = sheet(emb_cy, h)
        tag_e = T("embryo cortex, from above", 24, GREY).move_to([0.4, 3.35, 0])
        fb = ends(3.35)
        self.at("In the embryo")
        self.play(FadeIn(emb, shift=DOWN * 0.15), FadeIn(tag_e), FadeIn(fb), run_time=0.8)
        self.at("looks the same")
        self.play(Indicate(emb, color=TEXT, scale_factor=1.02), run_time=1.0)
        self.at("no clear borders")
        self.play(Indicate(emb, color=TEXT, scale_factor=1.02), run_time=0.8)
        arrow = Arrow([0, 0.7, 0], [0, -0.3, 0], buff=0, color=GREY, stroke_width=5, tip_length=0.25)
        q = T("?", 60, TEXT, weight=BOLD).move_to([0.9, 0.2, 0])
        self.at("where do the areas come from")
        self.play(GrowArrow(arrow), FadeIn(q, scale=0.6), run_time=0.8)
        word = T("arealization", 34, TEXT, font=TITLE_FONT).move_to([3.4, 0.2, 0])
        self.at("is called")
        self.play(FadeIn(word, shift=LEFT * 0.2), run_time=0.7)
        self.finish()


# ---------------------------------------------------------------------------------------------
class S02Gradients(SpokenScene):
    """the sheet splits into two bars: Emx2 and Pax6 gradients; a progenitor reads the mix."""

    def construct(self):
        h = 1.4
        sh = sheet(1.9, 1.6).shift(DOWN * 1.0)
        fb = ends(3.0)
        cells = VGroup(*[Circle(radius=0.11, stroke_color=TEXT, stroke_width=2, fill_color=TEXT, fill_opacity=0.5).move_to(
            [xf((i + 0.5) / 12), 0.9 + (0.25 if i % 2 else -0.25), 0]) for i in range(12)])
        self.at("Cells in the sheet")
        self.play(FadeIn(sh), FadeIn(fb), run_time=0.6)
        self.at("Progenitors")
        self.play(LaggedStart(*[FadeIn(c, scale=0.4) for c in cells], lag_ratio=0.08), run_time=1.0)
        self.at("transcription factors")
        self.play(Indicate(sh, color=TEXT, scale_factor=1.02), run_time=0.8)

        a = sheet(1.9, h)
        b = sheet(0.1, h)
        self.at("two of them")
        self.play(ReplacementTransform(sh, a), FadeIn(b), FadeOut(cells), fb.animate.move_to([0, 3.3, 0]).set_opacity(0), run_time=0.9)
        fb2 = ends(3.3)
        self.play(FadeIn(fb2), run_time=0.3)
        ea = strips(emx, ORANGE, 1.9, h)
        pb = strips(pax, BLUE, 0.1, h)
        lab_e = T("Emx2", 30, ORANGE, weight=BOLD).move_to([X0 - 0.9, 1.9, 0])
        lab_p = T("Pax6", 30, BLUE, weight=BOLD).move_to([X0 - 0.9, 0.1, 0])
        self.at("opposing gradients")
        self.play(LaggedStart(FadeIn(ea), FadeIn(pb), lag_ratio=0.7), FadeIn(lab_e), FadeIn(lab_p), run_time=1.6)
        self.at("highest at the back")
        self.play(Indicate(ea[-4:], color=ORANGE, scale_factor=1.1), Indicate(lab_e, color=ORANGE), run_time=0.9)
        self.at("highest at the front")
        self.play(Indicate(pb[:4], color=BLUE, scale_factor=1.1), Indicate(lab_p, color=BLUE), run_time=0.9)

        c = ValueTracker(0.1)
        cursor = always_redraw(lambda: VGroup(
            Line([xf(c.get_value()), 2.6, 0], [xf(c.get_value()), -0.65, 0], stroke_color=TEXT, stroke_width=3),
            Circle(radius=0.15, stroke_color=TEXT, stroke_width=3, fill_color=TEXT, fill_opacity=0.9).move_to(
                [xf(c.get_value()), -0.65, 0])))
        base = Line([-1.3, -3.0, 0], [1.3, -3.0, 0], stroke_color=GREY, stroke_width=2)

        def readout():
            v = c.get_value()
            e = Rectangle(width=0.7, height=2.0 * emx(v, 0.85), stroke_width=0, fill_color=ORANGE, fill_opacity=0.9)
            p = Rectangle(width=0.7, height=2.0 * pax(v, 0.85), stroke_width=0, fill_color=BLUE, fill_opacity=0.9)
            e.move_to([-0.55, -3.0 + e.height / 2, 0])
            p.move_to([0.55, -3.0 + p.height / 2, 0])
            return VGroup(e, p)

        ro = always_redraw(readout)
        cap = T("the mix this cell holds", 24, GREY).move_to([4.1, -2.3, 0])
        self.at("reads its position")
        self.play(FadeIn(cursor), FadeIn(base), FadeIn(ro), FadeIn(cap), run_time=0.6)
        self.play(c.animate.set_value(0.9), run_time=3.0, rate_func=linear)
        self.play(c.animate.set_value(0.5), run_time=1.4)
        self.finish()


# ---------------------------------------------------------------------------------------------
class S03Remove(SpokenScene):
    """remove or raise a factor and watch the borders move; reset before each new case."""

    def construct(self):
        cy, h = 1.35, 2.5
        b1, b2 = ValueTracker(WT[0]), ValueTracker(WT[1])
        m = always_redraw(lambda: make_map(b1.get_value(), b2.get_value(), cy=cy, h=h))
        fb = ends(3.3)
        ea = strips(emx, ORANGE, -0.45, 0.32)
        pb = strips(pax, BLUE, -0.9, 0.32)
        lab_e = T("Emx2", 26, ORANGE, weight=BOLD).move_to([X0 - 0.85, -0.45, 0])
        lab_p = T("Pax6", 26, BLUE, weight=BOLD).move_to([X0 - 0.85, -0.9, 0])
        self.at("Does the mix matter")
        self.play(FadeIn(m), FadeIn(fb), FadeIn(ea), FadeIn(pb), FadeIn(lab_e), FadeIn(lab_p), run_time=1.0)
        hedge = T("areas read from marker genes at birth", 24, GREY).move_to([0, -3.3, 0])
        self.at("marker genes")
        self.play(FadeIn(hedge, shift=UP * 0.1), run_time=0.6)

        chip1 = chip("no Emx2", ORANGE, 30).move_to([0, -2.0, 0])
        self.at("Without")
        self.play(FadeOut(ea), FadeIn(chip1, shift=UP * 0.15), run_time=0.6)
        self.at("expanded toward the back")
        self.play(b1.animate.set_value(0.52), b2.animate.set_value(0.86), run_time=1.6)
        self.at("the visual area shrank")
        self.play(Indicate(m[1][2], color=PINK), run_time=0.9)

        # reset to normal at the same moment the new case appears
        chip2 = chip("no working Pax6", BLUE, 30).move_to([0, -2.0, 0])
        self.at("Without", nth=1)
        self.play(b1.animate.set_value(WT[0]), b2.animate.set_value(WT[1]), FadeOut(chip1), FadeIn(ea), FadeOut(pb),
                  FadeIn(chip2, shift=UP * 0.15), run_time=0.7)
        self.at("the other way")
        self.play(b1.animate.set_value(0.25), b2.animate.set_value(0.55), run_time=1.2)

        ea_hi = strips(lambda f: emx(f, 0.95), ORANGE, -0.45, 0.32)
        chip3 = chip("extra Emx2", ORANGE, 30).move_to([0, -2.0, 0])
        self.at("Raise")
        self.play(b1.animate.set_value(WT[0]), b2.animate.set_value(WT[1]), FadeOut(chip2), FadeIn(pb),
                  ReplacementTransform(ea, ea_hi), FadeIn(chip3, shift=UP * 0.15), run_time=0.7)
        self.at("the opposite way")
        self.play(b1.animate.set_value(0.28), b2.animate.set_value(0.58), run_time=1.6)
        self.at("allocating territory")
        self.play(Indicate(m[0], color=TEXT, scale_factor=1.03), run_time=1.0)
        self.finish()


# ---------------------------------------------------------------------------------------------
class S04Lamp(SpokenScene):
    """FGF8 as a lamp at the front; barrel field moves with a second source and with a blocker."""

    def construct(self):
        bw, bx0, cy, bh = 9.2, -4.6, 0.0, 2.8
        A, B = ValueTracker(1.0), ValueTracker(0.0)
        px = ValueTracker(0.0)      # barrel field centre
        sec = ValueTracker(0.0)     # opacity of the second, partial field

        def level(f):
            return min(0.85, 0.05 + 0.8 * (A.get_value() * np.exp(-3.2 * f) + B.get_value() * np.exp(-3.2 * (1 - f))))

        bar = Rectangle(width=bw, height=bh, stroke_color=GREY, stroke_width=3, fill_color=GREY,
                        fill_opacity=0.22).move_to([bx0 + bw / 2, cy, 0])
        light = always_redraw(lambda: strips(level, YELLOW, cy, bh, n=26, w=bw, x0=bx0))
        fb = VGroup(T("front", 24, GREY).move_to([bx0 + 0.45, cy + 1.75, 0]), T("back", 24, GREY).move_to([bx0 + bw - 0.4, cy + 1.75, 0]))
        fields = always_redraw(lambda: barrels(px.get_value(), cy + 0.3, cols=4, rows=3, sp=0.5, r=0.14))
        fld_lbl = always_redraw(lambda: T("barrel field", 26, GREEN).move_to([px.get_value(), cy - 1.8, 0]))
        part = always_redraw(lambda: barrels(2.9, cy + 0.3, cols=2, rows=3, sp=0.5, r=0.14).set_opacity(sec.get_value()))
        part_lbl = always_redraw(lambda: T("second, partial", 26, GREEN).move_to([3.2, cy - 1.8, 0]).set_opacity(sec.get_value()))
        cells = VGroup(*[Circle(radius=0.1, stroke_color=TEXT, stroke_width=2, fill_color=TEXT, fill_opacity=0.5).move_to(
            [bx0 + (i + 0.5) / 9 * bw, cy - 0.95, 0]) for i in range(9)])

        src = glow(-5.3, cy, 0.4)
        src_lbl = T("FGF8", 28, YELLOW, weight=BOLD).move_to([-5.3, cy + 1.6, 0])
        self.at("The gradients need a source")
        self.play(FadeIn(bar), FadeIn(fb), run_time=0.6)
        self.at("At the front")
        self.play(FadeIn(src, scale=0.5), FadeIn(src_lbl), run_time=0.7)
        self.add(light)
        self.play(Indicate(src, color=YELLOW, scale_factor=1.15), run_time=1.0)
        self.at("lamp at the front")
        self.play(FadeIn(light), run_time=0.8)
        self.at("how bright it is")
        self.play(LaggedStart(*[FadeIn(c, scale=0.4) for c in cells], lag_ratio=0.1), run_time=1.0)
        self.at("how far forward")
        self.play(Indicate(cells[:3], color=YELLOW, scale_factor=1.3), run_time=1.0)
        self.at("barrel field")
        self.add(fields, fld_lbl)
        self.play(FadeIn(fields), FadeIn(fld_lbl), run_time=0.8)

        src2 = glow(5.3, cy, 0.4)
        src2_lbl = T("FGF8", 28, YELLOW, weight=BOLD).move_to([5.3, cy + 1.6, 0])
        self.at("Add a second source")
        self.play(FadeIn(src2, scale=0.5), FadeIn(src2_lbl), B.animate.set_value(1.0), run_time=1.2)
        self.add(part, part_lbl)
        self.at("a partial second")
        self.play(sec.animate.set_value(1.0), run_time=1.0)

        # reset the old answer in the same beat the blocker appears
        blocker = VGroup(Rectangle(width=0.22, height=2.4, stroke_color=RED, stroke_width=3, fill_color=RED, fill_opacity=0.8))
        blocker.move_to([-4.75, cy, 0])
        blk_lbl = T("blocker", 26, RED).move_to([-4.2, cy - 1.8, 0])
        self.at("Block")
        self.play(B.animate.set_value(0.0), sec.animate.set_value(0.0), FadeOut(src2), FadeOut(src2_lbl),
                  FadeIn(blocker, shift=RIGHT * 0.2), FadeIn(blk_lbl),
                  Transform(src, glow(-5.3, cy, 0.26, dim=0.3)), A.animate.set_value(0.3), run_time=1.0)
        self.at("moves toward the front")
        self.play(px.animate.set_value(-2.2), run_time=1.8)
        self.finish()


# ---------------------------------------------------------------------------------------------
class S05Input(SpokenScene):
    """thalamic axons reach the map; a visual graft forms barrels; without axons the borders remain."""

    def construct(self):
        cy, h = 1.8, 1.9
        m = make_map(*WT, cy=cy, h=h, op=0.12)
        outline = VGroup(*[r.copy().set_fill(opacity=0) for r in m[0]])
        fb = ends(3.3)
        self.at("Genes sketch the map")
        self.play(Create(outline), FadeIn(m[0]), FadeIn(m[1]), FadeIn(fb), run_time=1.0)

        thal = chip("thalamus", TEXT, 28).move_to([0, -2.9, 0])
        centers = [xf(WT[0] / 2), xf((WT[0] + WT[1]) / 2), xf((WT[1] + 1) / 2)]
        axons = VGroup(*[CubicBezier([0 + (k - 1) * 0.6, -2.45, 0], [(k - 1) * 0.6, -1.2, 0], [c, -0.4, 0], [c, cy - h / 2, 0],
                                      stroke_color=TEXT, stroke_width=4) for k, c in enumerate(centers)])
        self.at("input shapes much of it")
        self.play(m[0].animate.set_fill(opacity=0.38), FadeIn(thal), run_time=0.7)
        self.at("Thalamic axons")
        self.play(LaggedStart(*[Create(a) for a in axons], lag_ratio=0.25), run_time=1.5)
        self.at("eyes, ears and skin")
        self.play(Indicate(axons, color=TEXT, scale_factor=1.0), run_time=0.9)

        gx = centers[1]
        graft = Rectangle(width=2.0, height=1.3, stroke_color=PINK, stroke_width=4, fill_color=PINK,
                          fill_opacity=0.6).move_to([gx, cy - 0.25, 0])
        g_lbl = T("visual cortex graft", 24, PINK).move_to([gx, 3.3, 0])
        self.at("fetal visual cortex")
        self.play(FadeOut(m[1][1]), FadeIn(g_lbl), FadeIn(graft, shift=DOWN * 0.5), run_time=0.9)
        ext = Line(axons[1].get_end(), [gx, cy - 0.5, 0], stroke_color=TEXT, stroke_width=4)
        self.at("Whisker axons grew")
        self.play(Create(ext), Indicate(axons[1], color=TEXT, scale_factor=1.0), run_time=0.9)
        dots = barrels(gx, cy - 0.25, cols=4, rows=2, sp=0.42, r=0.11)
        self.at("formed barrels")
        self.play(FadeIn(dots, lag_ratio=0.12), run_time=0.9)

        # reset: new case, no axons reach the cortex
        short = VGroup(*[CubicBezier([(k - 1) * 0.6, -2.45, 0], [(k - 1) * 0.6, -1.8, 0], [c, -1.6, 0], [c, -1.3, 0],
                                     stroke_color=TEXT, stroke_width=4) for k, c in enumerate(centers)])
        stops = VGroup(*[T("x", 28, RED, weight=BOLD).move_to([c, -0.95, 0]) for c in centers])
        self.at("Yet in mice")
        self.play(FadeOut(VGroup(graft, g_lbl, dots, ext, axons)), FadeIn(m[1][1]), FadeIn(short), run_time=0.8)
        self.play(FadeIn(stops), run_time=0.4)
        self.at("axons never")
        self.play(Indicate(stops, color=RED, scale_factor=1.3), run_time=0.8)
        self.at("normal borders")
        self.play(Indicate(m[0], color=TEXT, scale_factor=1.03), run_time=1.0)
        self.finish()


# ---------------------------------------------------------------------------------------------
class S06Twice(SpokenScene):
    """sketch from the sheet, refined by input; weaken the signal and the borders move."""

    def construct(self):
        b1, b2 = ValueTracker(WT[0]), ValueTracker(WT[1])
        sk = always_redraw(lambda: make_map(b1.get_value(), b2.get_value(), cy=1.95, h=1.3, labels=("", "", ""), op=0.14, sw=2))
        rf = always_redraw(lambda: make_map(b1.get_value(), b2.get_value(), cy=-1.55, h=1.3, op=0.4))
        t_sk = T("sketch from the sheet", 28, TEXT).move_to([0.4, 3.15, 0])
        t_rf = T("refined by input", 28, TEXT).move_to([0.4, -0.55, 0])
        src = glow(-5.3, 1.95, 0.3)
        e_s = strips(emx, ORANGE, 1.1, 0.22)
        p_s = strips(pax, BLUE, 0.84, 0.22)
        self.at("drawn twice")
        self.play(FadeIn(sk), FadeIn(t_sk), run_time=0.8)
        self.at("a sketch from the sheet")
        self.play(FadeIn(e_s), FadeIn(p_s), run_time=0.8)
        self.at("a signal from the edge")
        self.play(FadeIn(src, scale=0.5), run_time=0.7)
        self.at("set where the borders fall")
        self.play(Indicate(sk[0], color=TEXT, scale_factor=1.02), run_time=1.0)

        arrow = Arrow([0.4, 0.4, 0], [0.4, -0.15, 0], buff=0, color=GREY, stroke_width=5, tip_length=0.22)
        thal = chip("thalamic input", TEXT, 26).move_to([0.4, -3.4, 0])
        ax = VGroup(*[Line([0.4 + (k - 1) * 0.5, -3.05, 0], [xf(c), -2.2, 0], stroke_color=TEXT, stroke_width=4)
                      for k, c in enumerate((WT[0] / 2, (WT[0] + WT[1]) / 2, (WT[1] + 1) / 2))])
        self.at("a refined copy")
        self.play(GrowArrow(arrow), FadeIn(rf), FadeIn(t_rf), run_time=0.9)
        self.at("thalamic input")
        self.play(FadeIn(thal), LaggedStart(*[Create(a) for a in ax], lag_ratio=0.2), run_time=1.0)
        self.at("Move the signal")
        self.play(Transform(src, glow(-5.3, 1.95, 0.17, dim=0.3)), b1.animate.set_value(0.30), b2.animate.set_value(0.60), run_time=1.6)
        self.finish()


class S07End(EndCard):
    LINE = "Position sketches the map. Input then refines it."
