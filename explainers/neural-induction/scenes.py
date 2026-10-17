"""Neural induction: neural is the default fate  (Biochemistrypedia explainer)

COLOR MAP (one color per concept, whole video)
  GREY   = ectoderm cell with no fate shown yet; outlines; labels
  ORANGE = epidermis (skin) fate
  BLUE   = neural fate
  YELLOW = BMP / BMP4, the signal that makes skin
  GREEN  = the organizer's BMP antagonists (Noggin, Chordin, Follistatin)
  PURPLE = organizer and dorsal mesoderm
  PINK   = BMP receptor on a cell surface
  RED    = a jammed receptor
"""
import numpy as np
from bp_style import *  # noqa: F401,F403

ORANGE = "#F29E4C"
PURPLE = "#B58CD9"
PINK = "#E58AC0"


# ------------------------------------------------------------------ helpers
def cell(p, r=0.42, color=GREY):
    c = Circle(radius=r, stroke_color=color, stroke_width=3, fill_color=color, fill_opacity=0.28)
    return c.move_to([p[0], p[1], 0])


def paint(c, color):
    return c.animate.set_stroke(color).set_fill(color, 0.32)


def grid_pos(rows, cols, pitch, center=(0, 0)):
    return [np.array([center[0] + (j - (cols - 1) / 2) * pitch, center[1] + ((rows - 1) / 2 - i) * pitch, 0])
            for i in range(rows) for j in range(cols)]


def gap_pts(rows, cols, pitch, center=(0, 0)):
    P = grid_pos(rows, cols, pitch, center)
    out = []
    for i in range(rows):
        for j in range(cols):
            k = i * cols + j
            if j < cols - 1:
                out.append((P[k] + P[k + 1]) / 2)
            if i < rows - 1:
                out.append((P[k] + P[k + cols]) / 2)
    return out


def dot(p, r=0.09, color=YELLOW):
    return Circle(radius=r, stroke_width=0, fill_color=color, fill_opacity=1).move_to([p[0], p[1], 0])


def clasp(p, r=0.24, color=GREEN):
    """An antagonist drawn as an open ring that closes on a BMP dot."""
    return Arc(radius=r, start_angle=PI * 0.3, angle=PI * 1.4, stroke_color=color, stroke_width=6).move_to([p[0], p[1], 0])


def tick(p, w=0.5, color=PINK):
    return RoundedRectangle(corner_radius=0.05, width=w, height=0.16, stroke_width=0, fill_color=color,
                            fill_opacity=1).move_to([p[0], p[1], 0])


def inhibit(a, b, color=YELLOW, w=6):
    a, b = np.array(a, float), np.array(b, float)
    d = (b - a) / np.linalg.norm(b - a)
    perp = np.array([-d[1], d[0], 0])
    return VGroup(Line(a, b, color=color, stroke_width=w),
                  Line(b + perp * 0.3, b - perp * 0.3, color=color, stroke_width=w + 1))


def clock():
    face = Circle(radius=0.32, stroke_color=GREY, stroke_width=3)
    hand = Line(ORIGIN, UP * 0.24, color=GREY, stroke_width=3)
    g = VGroup(face, hand)
    g.hand = hand
    return g


class S00Title(TitleCard):
    LESSON = "Neural induction"
    TITLE = "Neural is the default fate"


# ------------------------------------------------------------------ 1
class S01Cap(SpokenScene):
    def construct(self):
        C = np.array([-3.7, 0.1, 0])
        n = 22
        ring = VGroup(*[cell(C + 2.4 * np.array([np.cos(a), np.sin(a), 0]), r=0.3)
                        for a in [PI / 2 + 2 * PI * k / n for k in range(n)]])
        blast_lbl = T("blastula", 28, GREY).move_to(C)
        self.play(LaggedStart(*[FadeIn(c, scale=0.6) for c in ring], lag_ratio=0.02), FadeIn(blast_lbl), run_time=0.8)
        cap = VGroup(*[ring[k] for k in (20, 21, 0, 1, 2)])
        self.at("small square")
        self.play(*[paint(c, TEXT) for c in cap], run_time=0.5)

        self.at("hollow ball")
        self.play(Indicate(ring, color=TEXT, scale_factor=1.04), run_time=1.2)
        self.at("Culture it")
        P = grid_pos(3, 6, 0.9, (3.2, 0.3))
        grid = VGroup(*[cell(p, 0.38) for p in P])
        dish = RoundedRectangle(corner_radius=0.2, width=5.5, height=3.3, stroke_color=GREY, stroke_width=3,
                                stroke_opacity=0.7).move_to([3.2, 0.3, 0])
        salt = T("salt water", 24, GREY).move_to([3.2, -1.95, 0])
        cap_copy = VGroup(*[c.copy() for c in cap])
        self.play(ReplacementTransform(cap_copy, grid), FadeIn(dish), FadeIn(salt), ring.animate.set_opacity(0.3),
                  blast_lbl.animate.set_opacity(0.3), run_time=1.3)
        self.at("becomes skin")
        skin = chip("skin", ORANGE, size=28).move_to([3.2, 2.6, 0])
        self.play(*[paint(c, ORANGE) for c in grid], FadeIn(skin, shift=UP * 0.1), run_time=0.7)

        self.at("pull the same square")
        mid = VGroup(grid, dish, salt, skin)
        self.play(FadeOut(VGroup(ring, blast_lbl)), mid.animate.shift(LEFT * 3.2), run_time=0.9)
        self.at("into single cells")
        T2 = grid_pos(3, 6, 1.7, (0, 0.3))
        self.play(FadeOut(dish), FadeOut(salt), FadeOut(skin),
                  *[g.animate.move_to(p) for g, p in zip(grid, T2)], run_time=1.2)

        self.at("a few hours")
        clk = clock().move_to([-1.4, -2.7, 0])
        hrs = T("a few hours", 28, GREY).move_to([0.3, -2.7, 0])
        self.play(FadeIn(clk), FadeIn(hrs), Rotate(clk.hand, angle=-2 * PI, about_point=clk[0].get_center()),
                  run_time=1.2)
        self.at("neural tissue")
        neural = chip("neural", BLUE, size=28).move_to([0, 2.95, 0])
        self.play(*[paint(c, BLUE) for c in grid], FadeIn(neural, shift=UP * 0.1), run_time=0.7)
        self.at("Why")
        q = T("?", 90, TEXT, font=TITLE_FONT).move_to([0, -2.7, 0])
        self.play(FadeOut(VGroup(clk, hrs)), FadeIn(q, scale=0.5), run_time=0.5)
        self.finish()


# ------------------------------------------------------------------ 2
class S02Signal(SpokenScene):
    def construct(self):
        pitch = 1.0
        P = grid_pos(3, 6, pitch, (0, 0.3))
        grid = VGroup(*[cell(p, 0.38) for p in P])
        self.play(FadeIn(grid, lag_ratio=0.04), run_time=0.8)
        self.at("ectoderm")
        lbl = T("ectoderm", 28, GREY).move_to([0, -1.9, 0])
        self.play(FadeIn(lbl), run_time=0.4)

        self.at("outer layer")
        self.play(Indicate(grid, color=TEXT, scale_factor=1.04), run_time=1.2)
        self.at("pass a signal")
        gp = gap_pts(3, 6, pitch, (0, 0.3))
        dots = VGroup(*[dot(p) for p in gp])
        self.play(LaggedStart(*[FadeIn(d, scale=0.3) for d in dots], lag_ratio=0.05),
                  *[paint(c, ORANGE) for c in grid], run_time=1.3)
        self.at("bone morphogenetic protein")
        bmp = chip("BMP4", YELLOW, size=28).move_to([0, 2.95, 0])
        self.play(FadeIn(bmp, shift=DOWN * 0.1), Indicate(dots, color=YELLOW, scale_factor=1.6), run_time=0.9)

        self.at("Spread the cells")
        P2 = grid_pos(3, 6, 1.7, (0, 0.3))
        far = gap_pts(3, 6, 1.7, (0, 0.3))
        self.play(FadeOut(lbl), *[g.animate.move_to(p) for g, p in zip(grid, P2)],
                  *[d.animate.move_to(f).set_opacity(0.6) for d, f in zip(dots, far)], run_time=1.6)
        self.at("diluted away")
        self.play(*[d.animate.set_opacity(0.0) for d in dots], run_time=1.0)
        self.at("become neural")
        neural = chip("neural", BLUE, size=28).move_to([0, -2.9, 0])
        self.play(*[paint(c, BLUE) for c in grid], FadeIn(neural, shift=UP * 0.1), run_time=0.7)
        self.finish()


# ------------------------------------------------------------------ 3
class S03Three(SpokenScene):
    def construct(self):
        py = 1.2
        P = grid_pos(2, 3, 1.3, (0, py))
        sep = VGroup(*[cell(p, 0.4, BLUE) for p in P])
        for c in sep:
            c.set_fill(BLUE, 0.32)
        self.play(FadeIn(sep), run_time=0.5)

        self.at("give the separated cells")
        gp = gap_pts(2, 3, 1.3, (0, py))
        dots = VGroup(*[dot(p) for p in gp])
        bmp = chip("BMP4", YELLOW, size=26).move_to([0, 3.0, 0])
        self.play(FadeIn(bmp, shift=DOWN * 0.1), LaggedStart(*[FadeIn(d, scale=0.3) for d in dots], lag_ratio=0.08),
                  run_time=1.0)
        self.at("become skin again")
        skinC = chip("skin", ORANGE, size=26).move_to([0, -1.25, 0])
        self.play(*[paint(c, ORANGE) for c in sep], FadeIn(skinC, shift=UP * 0.1), run_time=0.7)

        self.at("side by side")
        lblC = chip("separated + BMP4", YELLOW, size=24).move_to([0, -0.35, 0])
        grpC = VGroup(sep, dots, bmp, skinC, lblC)
        self.play(FadeIn(lblC), grpC.animate.shift(RIGHT * 4.3), run_time=0.9)
        # panel A: intact; panel B: separated; both neutral until scored
        A = VGroup(*[cell(p, 0.4) for p in grid_pos(2, 3, 0.82, (-4.3, py))])
        B = VGroup(*[cell(p, 0.4) for p in grid_pos(2, 3, 1.3, (0, py))])
        lblA = chip("intact", GREY, size=24).move_to([-4.3, -0.35, 0])
        lblB = chip("separated", GREY, size=24).move_to([0, -0.35, 0])
        self.play(FadeIn(A), FadeIn(B), FadeIn(lblA), FadeIn(lblB), run_time=0.8)
        self.at("intact square is skin")
        skinA = chip("skin", ORANGE, size=26).move_to([-4.3, -1.25, 0])
        self.play(*[paint(c, ORANGE) for c in A], FadeIn(skinA, shift=UP * 0.1), run_time=0.6)
        self.at("cells are neural")
        neuB = chip("neural", BLUE, size=26).move_to([0, -1.25, 0])
        self.play(*[paint(c, BLUE) for c in B], FadeIn(neuB, shift=UP * 0.1), run_time=0.6)
        self.at("default fate")
        src = chip("signals between cells", YELLOW, size=26).move_to([-2.6, -2.85, 0])
        tgt = chip("neural", BLUE, size=26).move_to([3.4, -2.85, 0])
        dflt = T("the default", 24, BLUE).next_to(tgt, UP, buff=0.12)
        self.play(FadeIn(tgt), FadeIn(dflt), run_time=0.5)
        self.at("actively suppress")
        self.play(FadeIn(src), Create(inhibit(src.get_right() + RIGHT * 0.1, tgt.get_left() + LEFT * 0.1)), run_time=0.7)
        self.finish()


# ------------------------------------------------------------------ 4
class S04Organizer(SpokenScene):
    def construct(self):
        xs = [-5.4 + 1.2 * i for i in range(10)]
        ecto = VGroup(*[cell((x, 1.8), 0.5, ORANGE) for x in xs])
        dots = VGroup(*[dot(((xs[i] + xs[i + 1]) / 2, 1.8), 0.1) for i in range(9)])
        lbl = T("ectoderm", 26, GREY).move_to([0, 3.1, 0])
        self.play(FadeIn(ecto, lag_ratio=0.05), FadeIn(dots), FadeIn(lbl), run_time=1.0)

        self.at("should make")
        org = chip("organizer", PURPLE, size=28).move_to([5.0, -0.5, 0])
        self.play(FadeIn(org, shift=LEFT * 0.2), run_time=0.5)
        self.at("blocks it")
        qbox = VGroup(RoundedRectangle(corner_radius=0.12, width=1.0, height=1.0, stroke_color=GREEN, stroke_width=3,
                                       fill_color=GREEN, fill_opacity=0.12), T("?", 48, GREEN))
        qlab = T("blocks BMP", 24, GREEN).next_to(qbox, RIGHT, buff=0.25)
        q = VGroup(qbox, qlab).move_to([0, -2.7, 0])
        self.play(FadeIn(q, scale=0.8), run_time=0.6)

        self.at("three such")
        boxes = VGroup(*[VGroup(RoundedRectangle(corner_radius=0.12, width=1.0, height=1.0, stroke_color=GREEN,
                                                 stroke_width=3, fill_color=GREEN, fill_opacity=0.12),
                                T("?", 48, GREEN)) for _ in range(3)]).arrange(RIGHT, buff=0.5)
        boxes.next_to(qlab, LEFT, buff=0.4)
        q3 = VGroup(boxes, qlab.copy()).move_to([0, -2.7, 0])
        self.play(ReplacementTransform(q, q3), run_time=0.7)
        q = q3
        self.at("proteins")
        self.play(LaggedStart(*[Indicate(b, color=GREEN, scale_factor=1.15) for b in boxes], lag_ratio=0.35),
                  Indicate(org, color=PURPLE, scale_factor=1.1), run_time=1.2)
        self.at("is the set")
        fin = [(3.2 - 0.95 * k, -0.5) for k in range(7)]
        mes = VGroup(*[cell((4.2, -0.5), 0.4, PURPLE) for k in range(7)])
        mes.set_opacity(0)
        self.add(mes)
        self.play(LaggedStart(*[mes[k].animate.set_opacity(1).move_to([fin[k][0], fin[k][1], 0]) for k in range(7)],
                              lag_ratio=0.3), run_time=8.0)
        self.at("beneath the ectoderm")
        mlab = T("dorsal mesoderm", 26, PURPLE).move_to([0.5, -1.4, 0])
        self.play(FadeIn(mlab), run_time=0.4)

        self.at("involution")
        self.play(Indicate(mes, color=PURPLE, scale_factor=1.1), run_time=1.0)
        self.at("secretes")
        names = ["Noggin", "Chordin", "Follistatin"]
        chips = VGroup(*[chip(n, GREEN, size=26) for n in names]).arrange(RIGHT, buff=0.35).move_to([0, -2.7, 0])
        self.play(FadeOut(q[1]), run_time=0.3)
        self.play(LaggedStart(*[ReplacementTransform(b, c) for b, c in zip(q[0], chips)], lag_ratio=0.45),
                  run_time=2.2)
        gd = VGroup(*[dot((3.2 - 0.95 * k, -0.5), 0.12, GREEN) for k in range(1, 7)])
        self.add(gd)
        self.play(*[d.animate.move_to([d.get_center()[0], 0.5, 0]) for d in gd], run_time=1.6)
        self.finish()


# ------------------------------------------------------------------ 5
class S05Catch(SpokenScene):
    def construct(self):
        xs = [-4.4, -2.2, 0.0, 2.2, 4.4]
        mid = (-2.2, 0.0, 2.2)
        ecto = VGroup(*[cell((x, 1.7), 0.8, ORANGE) for x in xs])
        ticks = VGroup(*[tick((x, 0.9)) for x in xs])
        # BMP already at the receptors of the two flanking cells; free BMP in the fluid below the middle three
        bound = VGroup(*[dot((x, 0.68), 0.14) for x in (xs[0], xs[4])])
        free = VGroup(*[dot((x, -0.7), 0.14) for x in mid])
        mx = [-2.6, -1.3, 0.0, 1.3, 2.6]
        mes = VGroup(*[cell((x, -2.0), 0.42, PURPLE) for x in mx])
        elab = T("ectoderm", 26, GREY).move_to([0, 3.2, 0])
        mlab = T("dorsal mesoderm", 24, PURPLE).move_to([0, -3.1, 0])
        self.play(FadeIn(ecto), FadeIn(ticks), FadeIn(bound), FadeIn(free), FadeIn(mes), FadeIn(elab), FadeIn(mlab),
                  run_time=1.0)

        self.at("enter a cell")
        gd = VGroup(*[dot((x + 0.35, -1.5), 0.13, GREEN) for x in mid])
        self.add(gd)
        self.play(*[d.animate.shift(UP * 0.4) for d in gd], run_time=1.4)
        self.at("in the fluid")
        # free BMP drifts up toward the empty receptors; the antagonists follow it through the fluid
        self.play(*[f.animate.shift(UP * 0.6) for f in free], *[d.animate.shift(UP * 0.7) for d in gd],
                  run_time=9.0, rate_func=linear)

        self.at("bind")
        clasps = VGroup(*[clasp(f.get_center()) for f in free])
        self.play(*[ReplacementTransform(d, c) for d, c in zip(gd, clasps)], run_time=0.6)
        self.at("keep it off")
        self.play(*[VGroup(f, c).animate.shift(DOWN * 0.7) for f, c in zip(free, clasps)], run_time=1.0)
        self.at("directly above")
        self.play(Indicate(VGroup(ecto[1], ecto[2], ecto[3]), color=TEXT, scale_factor=1.05), run_time=0.8)
        self.at("cut off")
        self.play(*[paint(ecto[i], BLUE) for i in (1, 2, 3)], run_time=0.7)
        self.at("neural plate")
        npl = chip("neural plate", BLUE, size=26).move_to([0, 3.2, 0])
        self.play(ReplacementTransform(elab, npl), run_time=0.6)
        self.finish()


# ------------------------------------------------------------------ 6
def case_row(spread, state, jam=False):
    """one row of six cells; the receptors turn red when jammed."""
    pitch = 2.1 if spread else 1.65
    xs = [(j - 2.5) * pitch for j in range(6)]
    cells = VGroup(*[cell((x, 0.7), 0.72, state) for x in xs])
    tk = VGroup(*[tick((x, -0.04), 0.7, RED if jam else PINK) for x in xs])
    return VGroup(cells, tk), xs


class S06Rule(SpokenScene):
    def construct(self):
        # case 1 baseline: intact square, skin, BMP at the receptors
        lab1 = chip("intact square + Noggin", GREEN, size=26).move_to([0, 2.9, 0])
        row1, xs = case_row(False, ORANGE)
        d1 = VGroup(*[dot((x, -0.3), 0.16) for x in xs])
        self.at("Give an intact square")
        self.play(FadeIn(lab1), FadeIn(row1), FadeIn(d1), run_time=0.8)
        self.at("catches")
        cls = VGroup(*[clasp((x, -0.3), 0.3) for x in xs])
        self.play(FadeIn(cls), run_time=0.4)
        self.play(*[VGroup(d, c).animate.shift(DOWN * 1.0) for d, c in zip(d1, cls)], run_time=0.7)
        self.at("becomes neural")
        res1 = chip("neural", BLUE, size=26).move_to([0, -2.5, 0])
        self.play(*[paint(c, BLUE) for c in row1[0]], FadeIn(res1, shift=UP * 0.1), run_time=0.6)

        # case 2: reset to the intact baseline in the same move as the new label
        self.at("Jam the")
        lab2 = chip("jammed BMP receptor", RED, size=26).move_to([0, 2.9, 0])
        row2, _ = case_row(False, ORANGE, jam=True)
        d2 = VGroup(*[dot((x, -0.3), 0.16) for x in xs])
        self.play(FadeOut(VGroup(lab1, row1, d1, cls, res1)), FadeIn(lab2), FadeIn(row2), FadeIn(d2), run_time=0.7)
        self.at("result is the same")
        res2 = chip("neural", BLUE, size=26).move_to([0, -2.5, 0])
        self.play(*[paint(c, BLUE) for c in row2[0]], FadeIn(res2, shift=UP * 0.1), run_time=0.6)

        # case 3: separated cells are neural; BMP4 brings skin back
        self.at("Add")
        lab3 = chip("separated cells + BMP4", YELLOW, size=26).move_to([0, 2.9, 0])
        row3, xs3 = case_row(True, BLUE)
        res3 = chip("neural", BLUE, size=26).move_to([0, -2.5, 0])
        self.play(FadeOut(VGroup(lab2, row2, d2, res2)), FadeIn(lab3), FadeIn(row3), FadeIn(res3), run_time=0.7)
        d3 = VGroup(*[dot((x, -0.3), 0.16) for x in xs3])
        self.at("to separated cells")
        self.play(FadeIn(d3, lag_ratio=0.1), run_time=0.8)
        self.at("return to skin")
        res3b = chip("skin", ORANGE, size=26).move_to([0, -2.5, 0])
        self.play(*[paint(c, ORANGE) for c in row3[0]], ReplacementTransform(res3, res3b), run_time=0.7)

        # the rule
        self.at("Keep one rule")
        self.play(FadeOut(VGroup(lab3, row3, d3, res3b)), run_time=0.5)
        ec = chip("ectoderm", GREY, size=36).move_to([-3.6, -0.6, 0])
        ne = chip("neural", BLUE, size=36).move_to([3.6, -0.6, 0])
        ar = Arrow(ec.get_right() + RIGHT * 0.1, ne.get_left() + LEFT * 0.1, buff=0, color=BLUE, stroke_width=6)
        self.at("ectoderm becomes neural")
        self.play(FadeIn(ec), FadeIn(ne), GrowArrow(ar), run_time=0.8)
        self.at("unless")
        by = chip("BMP signaling", YELLOW, size=36).move_to([0, 1.8, 0])
        self.play(FadeIn(by, shift=DOWN * 0.1), Create(inhibit([0, 1.3, 0], [0, -0.5, 0])), run_time=0.8)
        self.finish()


class S07End(EndCard):
    LINE = "Ectoderm becomes neural unless BMP signaling tells it otherwise."
