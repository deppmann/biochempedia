"""Choosing a partner: one match, two opposite outcomes  (Biochemistrypedia explainer)

COLOR MAP (one color per concept, whole video)
  YELLOW = Sidekick-1 label (its layer, its cells, its knobs)
  BLUE   = Sidekick-2 label (its layer, its cells, its knobs)
  PURPLE = the Dscam1 neuron (its identity, its branches and knobs)
  ORANGE = a neighbouring neuron with a different Dscam1 subset
  TEAL   = a gradient (continuous order)
  GREEN  = pulled together
  RED    = pushed apart / Dscam1 missing
  GREY   = neutral cells, layers with no label named, structure
"""
import numpy as np
from bp_style import *  # noqa: F401,F403

PURPLE = "#B58CD9"
ORANGE = "#F29E4C"

BY = [0.9, -0.4, -1.7]      # centres of the three sublaminae
BX0, BX1 = -4.0, 6.0        # layer stack spans these x values
LABX = -5.2                 # left column for layer names


def arr(a, b, color=GREY, w=5, tip=0.2):
    return Arrow(a, b, buff=0.0, color=color, stroke_width=w, tip_length=tip,
                 max_tip_length_to_length_ratio=0.5, max_stroke_width_to_length_ratio=12)


def bchip(text, color=BLUE, size=26, **kw):
    c = chip(text, color, size=size, **kw)
    back = RoundedRectangle(corner_radius=0.14, width=c[0].width, height=c[0].height, stroke_width=0,
                            fill_color=BG, fill_opacity=1).move_to(c[0])
    return VGroup(back, *c)


def band(i, color=GREY, op=0.12):
    return Rectangle(width=BX1 - BX0, height=1.2, stroke_color=color, stroke_width=2.5,
                     fill_color=color, fill_opacity=op).move_to([(BX0 + BX1) / 2, BY[i], 0])


def band_knobs(i, color, op=0.9):
    return VGroup(*[Circle(0.09, stroke_width=0, fill_color=color, fill_opacity=op).move_to([x, BY[i] - 0.3, 0])
                    for x in np.arange(-3.8, 5.81, 0.4)])


def cell(x, color=GREY):
    return Circle(0.36, stroke_color=color, stroke_width=4, fill_color=color, fill_opacity=0.35).move_to([x, 3.0, 0])


def proc(x, i, color=GREY, kop=1.0, w=0.7, y=None):
    y = BY[i] + 0.3 if y is None else y
    stem = Line([x, 2.64, 0], [x, y, 0], color=color, stroke_width=5)
    arbor = Line([x - w, y, 0], [x + w, y, 0], color=color, stroke_width=5)
    kn = VGroup(*[Circle(0.09, stroke_width=0, fill_color=color, fill_opacity=kop).move_to([x + dx, y - 0.17, 0])
                  for dx in (-0.6, -0.2, 0.2, 0.6)])
    return VGroup(stem, arbor, kn)


def bonds(x, i, color):
    return VGroup(*[Line([x + dx, BY[i] + 0.13 - 0.1, 0], [x + dx, BY[i] - 0.3 + 0.1, 0], color=color, stroke_width=3)
                    for dx in (-0.6, -0.2, 0.2, 0.6)])


def paint(p, color):
    """animations that recolour a proc (stem, arbor, knobs)."""
    return [p[0].animate.set_color(color), p[1].animate.set_color(color), p[2].animate.set_fill(color, 1)]


def tint(b, color, op=0.14):
    return b.animate.set_stroke(color).set_fill(color, op)


def lab(text, color, i):
    return T(text, 26, color).move_to([LABX, BY[i], 0])


def path(pts, color, w=6):
    m = VMobject(stroke_color=color, stroke_width=w, fill_opacity=0)
    m.set_points_smoothly([np.array([x, y, 0.0]) for x, y in pts])
    return m


def tip(pts, color, w=6):
    return VGroup(path(pts, color, w), Circle(0.14, stroke_width=0, fill_color=color, fill_opacity=1).move_to([*pts[-1], 0]))


def note(text, color=GREY, size=24, y=-3.15):
    return T(text, size, color).move_to([1.0, y, 0])


class S00Title(TitleCard):
    LESSON = "Choosing a partner"
    TITLE = "One match, two opposite outcomes"


# ---------------------------------------------------------------------------------------------
class S01Gradient(SpokenScene):
    def construct(self):
        strips = VGroup(*[Rectangle(width=10 / 12, height=3.8, stroke_width=0, fill_color=TEAL,
                                    fill_opacity=0.04 + 0.4 * k / 11).move_to([BX0 + 10 / 24 + 10 / 12 * k, -0.4, 0])
                          for k in range(12)])
        tag = T("a gradient", 28, TEAL).move_to([1.0, -2.85, 0])
        cA, pA = cell(-1.2), proc(-1.2, 0, kop=0)
        self.at("bring an axon")
        self.play(FadeIn(strips), FadeIn(tag), FadeIn(cA), run_time=0.8)
        self.play(Create(pA[0]), run_time=1.6)
        self.at("thin layer")
        bands = VGroup(*[band(i) for i in range(3)])
        self.play(FadeOut(strips), FadeOut(tag), FadeIn(bands), run_time=0.9)
        self.play(Create(pA[1]), run_time=0.5)
        cB, pB = cell(2.4), proc(2.4, 1, kop=0)
        self.at("each cell type")
        self.play(FadeIn(cB), Create(pB[0]), run_time=1.0)
        self.play(Create(pB[1]), run_time=0.5)
        qs = VGroup(T("?", 44, YELLOW if False else GREY).move_to([-1.2 + 1.35, BY[0] + 0.3, 0]),
                    T("?", 44, GREY).move_to([2.4 + 1.35, BY[1] + 0.3, 0]),
                    T("?", 44, GREY).move_to([-1.2 - 1.35, BY[0] + 0.3, 0]),
                    T("?", 44, GREY).move_to([2.4 - 1.35, BY[1] + 0.3, 0]))
        self.at("does a process choose")
        self.play(FadeIn(qs, lag_ratio=0.2), run_time=0.8)
        self.play(*[Indicate(q, color=TEXT, scale_factor=1.3) for q in qs], run_time=1.0)
        self.at("discrete labels")
        k1, k2 = band_knobs(0, YELLOW), band_knobs(1, BLUE)
        self.play(FadeOut(qs), tint(bands[0], YELLOW), tint(bands[1], BLUE), FadeIn(k1), FadeIn(k2), run_time=1.0)
        self.finish()


class S02Like(SpokenScene):
    def construct(self):
        b = VGroup(band(0, YELLOW), band(1, BLUE), band(2))
        k1, k2 = band_knobs(0, YELLOW), band_knobs(1, BLUE)
        cA, pA = cell(-1.2), proc(-1.2, 0, kop=0)
        cB, pB = cell(2.4), proc(2.4, 1, kop=0)
        self.add(b, k1, k2, cA, pA, cB, pB)
        self.at("two proteins")
        where = note("chick retina")
        self.play(FadeIn(where), run_time=0.5)
        self.at("sidekick 1")
        l1 = lab("Sidekick-1", YELLOW, 0)
        self.play(FadeIn(l1, shift=RIGHT * 0.2), cA.animate.set_stroke(YELLOW).set_fill(YELLOW, 0.35),
                  *paint(pA, YELLOW), run_time=0.8)
        self.at("sidekick 2")
        l2 = lab("Sidekick-2", BLUE, 1)
        self.play(FadeIn(l2, shift=RIGHT * 0.2), cB.animate.set_stroke(BLUE).set_fill(BLUE, 0.35),
                  *paint(pB, BLUE), run_time=0.8)
        self.at("end in different")
        self.play(Indicate(pA[1:], color=TEXT, scale_factor=1.15), Indicate(pB[1:], color=TEXT, scale_factor=1.15),
                  run_time=1.2)
        self.at("binds its own kind")
        bA, bB = bonds(-1.2, 0, YELLOW), bonds(2.4, 1, BLUE)
        self.play(Create(bA), Create(bB), run_time=0.9)
        hom = T("homophilic binding: like binds like", 26, TEXT).move_to([1.0, -3.15, 0])
        self.at("homophilic binding")
        self.play(ReplacementTransform(where, hom), run_time=0.7)
        self.at("stick to other cells")
        self.play(Indicate(bA, color=TEXT), Indicate(bB, color=TEXT), run_time=1.2)
        self.finish()


class S03Shift(SpokenScene):
    def construct(self):
        b = VGroup(band(0, YELLOW), band(1, BLUE))
        k1, k2 = band_knobs(0, YELLOW), band_knobs(1, BLUE)
        cA, pA, bA = cell(-1.2, YELLOW), proc(-1.2, 0, YELLOW), bonds(-1.2, 0, YELLOW)
        cB, pB, bB = cell(2.4, BLUE), proc(2.4, 1, BLUE), bonds(2.4, 1, BLUE)
        cC, pC = cell(5.2), proc(5.2, 2, GREY, kop=0, y=0.25)
        l1, l2 = lab("Sidekick-1", YELLOW, 0), lab("Sidekick-2", BLUE, 1)
        self.add(b, k1, k2, l1, l2, cA, pA, bA, cB, pB, bB)
        self.at("key test")
        self.play(FadeIn(cC), FadeIn(pC), run_time=0.8)
        mis = note("misexpression: a protein made where it is normally absent")
        self.at("expression")
        self.play(FadeIn(mis), Indicate(cC, color=TEXT, scale_factor=1.3), run_time=1.2)
        self.at("produce a sidekick")
        plus = T("+ Sidekick-1", 22, YELLOW).move_to([4.15, 2.3, 0])
        self.play(cC.animate.set_stroke(YELLOW).set_fill(YELLOW, 0.35), *paint(pC, YELLOW), FadeIn(plus), run_time=0.9)
        self.at("shifted toward")
        tgt = proc(5.2, 0, YELLOW, y=0.75)
        self.play(Transform(pC, tgt), run_time=2.0)
        self.at("label biases")
        self.play(Indicate(pC[2], color=TEXT, scale_factor=1.4), run_time=0.8)
        self.at("one part of how")
        one = note("one part of how layers form")
        self.play(ReplacementTransform(mis, one), FadeOut(plus), run_time=0.8)
        self.finish()


class S04Apart(SpokenScene):
    def construct(self):
        soma = Circle(0.5, stroke_color=PURPLE, stroke_width=4, fill_color=PURPLE, fill_opacity=0.35).move_to([-5.3, 0, 0])
        main = [(-4.8, 0.3), (-3.4, 1.3), (-1.8, 1.6), (0.2, 1.2)]
        mir = lambda pts: [(x, -y) for x, y in pts]
        up0 = main + [(1.0, 1.1), (1.8, 0.7), (2.3, 0.15)]
        up_apart = main + [(1.0, 1.3), (2.0, 1.9), (3.2, 2.4)]
        up_cross = main + [(1.2, 0.9), (2.6, -0.3), (4.0, -1.7)]
        up_bun = main + [(1.5, 0.5), (2.8, 0.15), (4.4, 0.1)]
        def pair(pts):
            return tip(pts, PURPLE), tip(mir(pts), PURPLE)
        u0, d0 = pair(main)
        u0[1].set_opacity(0)
        d0[1].set_opacity(0)
        U, D = pair(up0)
        # the first stretch of each branch, drawn alone; the tip is added by Transform later
        head = T("self-avoidance", 34, PURPLE, font=TITLE_FONT).move_to([-2.4, 3.0, 0])
        key = bchip("same Dscam1 forms", PURPLE, 26).move_to([3.6, 3.0, 0])
        no = bchip("no Dscam1", RED, 26).move_to([3.6, 3.0, 0])
        self.at("keep its own branches")
        self.play(FadeIn(soma), Create(u0[0]), Create(d0[0]), run_time=1.4)
        self.add(u0[1], d0[1])
        self.at("avoidance")
        self.play(FadeIn(head, shift=DOWN * 0.1), run_time=0.6)
        self.at("protein dscam1")
        self.play(FadeIn(key), run_time=0.5)
        self.at("identical forms")
        self.play(Transform(u0, U), Transform(d0, D), run_time=1.5)
        self.at("outcome is repulsion")
        r1, r2 = arr([2.6, 0.55, 0], [2.6, 1.15, 0], RED), arr([2.6, -0.55, 0], [2.6, -1.15, 0], RED)
        self.play(Indicate(VGroup(u0[1], d0[1]), color=RED, scale_factor=1.5), GrowArrow(r1), GrowArrow(r2), run_time=0.8)
        self.at("pull apart")
        ua, da = pair(up_apart)
        self.play(Transform(u0, ua), Transform(d0, da), FadeOut(r1), FadeOut(r2), run_time=1.5)
        self.at("without")
        self.play(ReplacementTransform(key, no), Transform(u0, U), Transform(d0, D), run_time=0.8)
        self.at("cross")
        uc, dc = pair(up_cross)
        self.play(Transform(u0, uc), Transform(d0, dc), run_time=0.9)
        self.at("bundle")
        ub, db = pair(up_bun)
        self.play(Transform(u0, ub), Transform(d0, db), run_time=1.2)
        self.finish()


class S05Identity(SpokenScene):
    def construct(self):
        # two neurons; A (purple) from the left, B (orange) from the right, branches overlap in the middle
        sA = Circle(0.45, stroke_color=PURPLE, stroke_width=4, fill_color=PURPLE, fill_opacity=0.35).move_to([-5.4, -0.9, 0])
        sB = Circle(0.45, stroke_color=ORANGE, stroke_width=4, fill_color=ORANGE, fill_opacity=0.35).move_to([5.4, -0.9, 0])
        A1 = path([(-5.0, -0.6), (-3.0, 0.2), (0.0, 0.7), (2.8, 0.6)], PURPLE)
        A2 = path([(-5.0, -0.9), (-2.0, -0.7), (1.0, -0.65), (3.4, -0.7)], PURPLE)
        A3 = path([(-5.0, -1.2), (-3.0, -2.0), (0.0, -2.4), (2.8, -2.2)], PURPLE)
        B1 = path([(5.0, -0.6), (3.0, 0.3), (0.0, 0.0), (-2.8, 0.2)], ORANGE)
        B2 = path([(5.0, -0.9), (2.0, 0.3), (-1.0, -0.65), (-2.6, -2.2)], ORANGE)
        B3 = path([(5.0, -1.2), (3.0, -1.8), (0.5, -1.6), (-3.0, -1.4)], ORANGE)
        neuA, neuB = VGroup(sA, A1, A2, A3), VGroup(sB, B1, B2, B3)
        self.at("tell itself")
        self.play(FadeIn(sA), FadeIn(sB), Create(A1), Create(A2), Create(A3), Create(B1), Create(B2), Create(B3),
                  run_time=1.8)
        # menu of forms
        dots = VGroup(*[Circle(0.07, stroke_width=0, fill_color=GREY, fill_opacity=0.8).move_to([-2.55 + 0.34 * c, 3.3 - 0.3 * r, 0])
                        for r in range(4) for c in range(16)])
        mlab = VGroup(T("Dscam1", 24, TEXT), T("38,016 forms", 24, GREY)).arrange(DOWN, buff=0.08).move_to([-4.8, 2.85, 0])
        self.at("can be spliced")
        self.play(FadeIn(dots, lag_ratio=0.02), FadeIn(mlab), run_time=1.6)
        a_idx, b_idx = [3, 41, 61], [17, 38, 14]
        tagA = VGroup(*[Circle(0.1, stroke_width=0, fill_color=PURPLE, fill_opacity=1) for _ in range(3)]).arrange(RIGHT, buff=0.2).move_to([-5.4, -1.8, 0])
        tagB = VGroup(*[Circle(0.1, stroke_width=0, fill_color=ORANGE, fill_opacity=1) for _ in range(3)]).arrange(RIGHT, buff=0.2).move_to([5.4, -1.8, 0])
        self.at("express a small")
        self.play(*[dots[i].animate.set_fill(PURPLE, 1).scale(1.8) for i in a_idx], run_time=0.3)
        self.play(*[ReplacementTransform(dots[i].copy(), tagA[k]) for k, i in enumerate(a_idx)], run_time=0.5)
        self.at("partly random")
        self.play(*[dots[i].animate.set_fill(ORANGE, 1).scale(1.8) for i in b_idx], run_time=0.5)
        self.play(*[ReplacementTransform(dots[i].copy(), tagB[k]) for k, i in enumerate(b_idx)], run_time=0.9)
        self.at("large menu")
        self.play(Indicate(dots, color=TEXT, scale_factor=1.05), run_time=1.0)
        self.at("own branches match")
        r1 = arr([2.9, 0.85, 0], [2.9, 1.45, 0], RED)
        r2 = arr([3.5, -0.95, 0], [3.5, -1.35, 0], RED)
        self.play(Indicate(tagA, color=TEXT, scale_factor=1.4), GrowArrow(r1), GrowArrow(r2), run_time=1.0)
        self.at("other neurons")
        ring = Circle(0.4, stroke_color=TEXT, stroke_width=3).move_to([-1.0, -0.65, 0])
        ov = T("overlap", 26, TEXT)
        ov = VGroup(Rectangle(width=ov.width + 0.2, height=ov.height + 0.12, stroke_width=0, fill_color=BG, fill_opacity=1), ov)
        ov.next_to(ring, DOWN, buff=0.1)
        self.play(FadeOut(r1), FadeOut(r2), Indicate(tagB, color=TEXT, scale_factor=1.4), Create(ring), FadeIn(ov), run_time=1.0)
        self.finish()


def disc(x, y, color, r=0.4):
    return Circle(r, stroke_color=color, stroke_width=4, fill_color=color, fill_opacity=0.5).move_to([x, y, 0])


class S06Rule(SpokenScene):
    def construct(self):
        ramp = VGroup(*[Rectangle(width=0.4, height=1.6, stroke_width=0, fill_color=TEAL,
                                  fill_opacity=0.08 + 0.8 * k / 11).move_to([-5.4 + 0.2 + 0.4 * k, 0.9, 0]) for k in range(12)])
        steps = VGroup(*[Rectangle(width=1.4, height=1.6, stroke_color=c, stroke_width=3, fill_color=c, fill_opacity=0.35)
                         .move_to([1.5 + 1.55 * k + 0.7, 0.9, 0]) for k, c in enumerate([YELLOW, BLUE, PURPLE])])
        t1 = T("gradient:\ncontinuous order", 28, TEAL, line_spacing=0.8).move_to([-3.0, -0.8, 0])
        t2 = T("labels:\ndiscrete membership", 28, TEXT, line_spacing=0.8).move_to([3.9, -0.8, 0])
        self.at("continuous order")
        self.play(FadeIn(ramp, lag_ratio=0.08), FadeIn(t1), run_time=1.2)
        self.at("discrete membership")
        self.play(FadeIn(steps, lag_ratio=0.3), FadeIn(t2), run_time=1.2)
        # --- the bond ---
        d1, d2 = disc(-0.55, 2.4, GREY, 0.55), disc(0.55, 2.4, GREY, 0.55)
        link = Line([-0.1, 2.4, 0], [0.1, 2.4, 0], color=TEXT, stroke_width=10)
        bondlab = T("like binds like", 30, TEXT).move_to([0, 1.55, 0])
        self.at("same chemistry")
        self.play(FadeOut(VGroup(ramp, steps, t1, t2)), FadeIn(d1), FadeIn(d2), FadeIn(link), FadeIn(bondlab), run_time=0.9)
        yl = T("Sidekick", 30, YELLOW).move_to([-3.6, 0.5, 0])
        pr = T("Dscam1", 30, PURPLE).move_to([3.6, 0.5, 0])
        L1, L2 = disc(-5.1, -0.9, YELLOW, 0.5), disc(-2.1, -0.9, YELLOW, 0.5)
        R1, R2 = disc(3.1, -0.9, PURPLE, 0.5), disc(4.1, -0.9, PURPLE, 0.5)
        self.at("opposite ends")
        self.play(FadeIn(yl), FadeIn(pr), FadeIn(L1), FadeIn(L2), FadeIn(R1), FadeIn(R2), run_time=0.9)
        self.at("draws processes together")
        ga = arr([-5.1, -1.9, 0], [-4.2, -1.9, 0], GREEN)
        gb = arr([-2.1, -1.9, 0], [-3.0, -1.9, 0], GREEN)
        gt = T("together", 28, GREEN).move_to([-3.6, -2.6, 0])
        self.play(L1.animate.move_to([-4.1, -0.9, 0]), L2.animate.move_to([-3.1, -0.9, 0]), GrowArrow(ga), GrowArrow(gb),
                  FadeIn(gt), run_time=1.2)
        self.at("drives branches apart")
        ra = arr([2.95, -1.9, 0], [2.0, -1.9, 0], RED)
        rb = arr([4.25, -1.9, 0], [5.2, -1.9, 0], RED)
        rt = T("apart", 28, RED).move_to([3.6, -2.6, 0])
        self.play(R1.animate.move_to([2.3, -0.9, 0]), R2.animate.move_to([4.9, -0.9, 0]), GrowArrow(ra), GrowArrow(rb),
                  FadeIn(rt), run_time=1.2)
        self.at("decides which")
        self.play(Indicate(VGroup(d1, d2, link), color=TEXT, scale_factor=1.25), run_time=1.0)
        self.finish()


class S07End(EndCard):
    LINE = "What the cell does after the bond forms decides which."
