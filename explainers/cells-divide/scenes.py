"""Cells divide: copy first, then share  (grade 7 Life Science explainer)

COLOR MAP (one color per concept, whole film)
  BLUE   = chromosomes (single bar = one chromosome; two joined bars = one copied chromosome)
  TEAL   = nucleus outline
  GREY   = cell outline, skin cells, fibers, neutral structure
  YELLOW = vocabulary words and the stage tracker highlight
  GREEN  = the count that matches the parent cell (4)
  RED    = the question marks / the "skip the copying" case
  TEXT   = joined mark between two copies
"""
import numpy as np
from bp_style import *  # noqa: F401,F403

HEIGHTS = [0.62, 0.8, 0.96, 0.7]
BW = 0.17


def chrom(h, copied=False, bw=BW, color=BLUE):
    """one chromosome: a bar, or two joined bars if copied. Anchor at its centre."""
    if not copied:
        b = RoundedRectangle(corner_radius=bw / 2, width=bw, height=h, stroke_width=0,
                             fill_color=color, fill_opacity=1)
        g = VGroup(b)
    else:
        a = RoundedRectangle(corner_radius=bw / 2, width=bw, height=h, stroke_width=0, fill_color=color, fill_opacity=1)
        b = a.copy()
        a.shift(LEFT * (bw / 2 + 0.01))
        b.shift(RIGHT * (bw / 2 + 0.01))
        j = Rectangle(width=2 * bw + 0.02, height=0.07, stroke_width=0, fill_color=TEXT, fill_opacity=1)
        g = VGroup(a, b, j)
    return g


def cell(w, h, x=0, y=0):
    return Ellipse(width=w, height=h, stroke_color=GREY, stroke_width=4, fill_color=GREY, fill_opacity=0.08).move_to([x, y, 0])


def nucleus(r, x=0, y=0):
    return Circle(radius=r, stroke_color=TEAL, stroke_width=4, fill_color=TEAL, fill_opacity=0.10).move_to([x, y, 0])


def count_tag(n, color=GREEN, size=40, wide=False):
    num = M(str(n), size + 12, color, weight=BOLD)
    lab = T("chromosomes" if n != 1 else "chromosome", 26, color)
    return VGroup(num, lab).arrange(RIGHT if wide else DOWN, buff=0.2 if wide else 0.08)


def word(text, size=30):
    return T(text, size, YELLOW, weight=BOLD)


class S00Title(TitleCard):
    LESSON = "How cells divide"
    TITLE = "Copy first, then share"


# ----------------------------------------------------------------------------------------------
class S01Scrape(SpokenScene):
    def construct(self):
        cells = VGroup(*[RoundedRectangle(corner_radius=0.18, width=1.35, height=1.35, stroke_color=GREY, stroke_width=3,
                                          fill_color=GREY, fill_opacity=0.15) for _ in range(8)])
        cells.arrange(RIGHT, buff=0.2).move_to([0, 0.3, 0])
        for c in cells:
            c.add(Circle(radius=0.28, stroke_color=TEAL, stroke_width=3, fill_color=TEAL, fill_opacity=0.12).move_to(c))
        skin = T("skin", 28, GREY).next_to(cells, DOWN, buff=0.35)
        self.at("scrape your knee")
        self.play(FadeIn(cells, lag_ratio=0.1), FadeIn(skin), run_time=1.2)
        gap = VGroup(cells[3], cells[4])
        scr = T("scrape", 34, RED, weight=BOLD).next_to(cells, UP, buff=0.5)
        self.play(FadeOut(gap, shift=UP * 0.4), FadeIn(scr), run_time=0.7)
        q = T("?", 90, RED, weight=BOLD).move_to([(cells[3].get_center()[0] + cells[4].get_center()[0]) / 2, 0.3, 0])
        self.at("new skin often")
        wk = T("new skin in about 1 to 2 weeks", 30, TEXT).to_edge(DOWN, buff=0.9)
        self.play(FadeIn(q, scale=0.6), FadeIn(wk), run_time=0.8)
        self.at("where did those")
        self.play(Indicate(q, color=RED, scale_factor=1.25), run_time=1.0)
        self.at("one cell splits")
        self.play(FadeOut(VGroup(cells[0:3], cells[5:8], skin, scr, wk, q)), run_time=0.7)
        parent = cell(5.6, 4.6, 0, 0.2)
        nuc = nucleus(1.5, 0, 0.2)
        bars = VGroup(*[chrom(h * 1.3, bw=BW * 1.4) for h in HEIGHTS]).arrange(RIGHT, buff=0.3).move_to(nuc)
        lab1 = T("1 cell", 34, TEXT).move_to([0, -2.6, 0])
        self.play(FadeIn(parent), FadeIn(nuc), FadeIn(bars), FadeIn(lab1), run_time=0.8)
        d1 = cell(5.0, 4.0, -3.0, 0.2)
        d2 = cell(5.0, 4.0, 3.0, 0.2)
        lab2 = T("2 cells", 34, TEXT).move_to([0, -2.6, 0])
        self.play(ReplacementTransform(parent, VGroup(d1, d2)), FadeOut(nuc), FadeOut(bars), ReplacementTransform(lab1, lab2),
                  run_time=1.4)
        self.at("full set of instructions")
        qa = T("?", 100, RED, weight=BOLD).move_to(d1)
        qb = T("?", 100, RED, weight=BOLD).move_to(d2)
        full = T("a full set of instructions?", 36, YELLOW).move_to([0, 2.9, 0])
        self.play(FadeIn(qa, scale=0.6), FadeIn(qb, scale=0.6), FadeIn(full), run_time=0.8)
        self.at("get a complete set")
        self.play(Indicate(VGroup(qa, qb), color=RED, scale_factor=1.2), run_time=1.2)
        self.finish()


# ----------------------------------------------------------------------------------------------
class S02Cycle(SpokenScene):
    def construct(self):
        title = word("cell cycle", 40).to_edge(UP, buff=0.5)
        self.at("cell cycle")
        self.play(Write(title), run_time=0.8)
        inter = chip("Interphase", BLUE, size=34).move_to([-4.0, 1.75, 0])
        mito = chip("Mitosis", GREEN, size=34).move_to([4.0, 1.75, 0])
        arr1 = CurvedArrow(inter.get_top() + UP * 0.05, mito.get_top() + UP * 0.05, angle=-TAU / 9, color=GREY, stroke_width=5)
        arr2 = CurvedArrow(mito.get_bottom() + DOWN * 0.05, inter.get_bottom() + DOWN * 0.05, angle=-TAU / 9, color=GREY, stroke_width=5)
        self.at("two main parts")
        self.play(Create(arr1), Create(arr2), run_time=1.0)
        self.at("interphase is when")
        self.play(FadeIn(inter, scale=0.8), run_time=0.6)
        d1 = T("grows and copies\nits chromosomes", 28, TEXT, line_spacing=0.8).move_to([-4.0, 0.35, 0])
        cl = cell(3.4, 2.0, -4.0, -2.1)
        nuc = nucleus(0.75, -4.0, -2.1)
        bars = VGroup(*[chrom(h * 0.9, bw=0.08) for h in HEIGHTS]).arrange(RIGHT, buff=0.2).move_to(nuc)
        self.play(FadeIn(d1), FadeIn(cl), FadeIn(nuc), run_time=0.7)
        self.play(cl.animate.scale(1.12), run_time=0.6)
        self.at("chromosomes")
        self.play(FadeIn(bars), run_time=0.5)
        chlab = word("chromosomes", 28).move_to([-4.0, -3.5, 0])
        nlab = T("nucleus", 26, TEAL).move_to([-1.2, -1.4, 0])
        nar = Arrow(nlab.get_left() + LEFT * 0.05, nuc.get_right() + RIGHT * 0.05, buff=0.05, color=TEAL, stroke_width=3, tip_length=0.18)
        self.at("threads in the nucleus")
        self.play(FadeIn(chlab), FadeIn(nlab), FadeIn(nar), run_time=0.7)
        self.at("busy not resting")
        busy = T("busy, not resting", 30, TEXT).move_to([-4.0, -0.5, 0])
        self.play(FadeIn(busy), bars.animate.scale(1.12), run_time=0.6)
        self.play(bars.animate.scale(1 / 1.12), run_time=0.5)
        self.at("mitosis is when")
        self.play(FadeIn(mito, scale=0.8), run_time=0.6)
        c1 = cell(2.5, 2.0, 2.8, -2.1)
        c2 = cell(2.5, 2.0, 5.3, -2.1)
        mb = T("divides into\ntwo new cells", 28, TEXT, line_spacing=0.8).move_to([4.0, 0.35, 0])
        pc = cell(3.6, 2.0, 4.05, -2.1)
        self.play(FadeIn(pc), FadeIn(mb), run_time=0.6)
        self.play(ReplacementTransform(pc, VGroup(c1, c2)), run_time=1.2)
        self.finish()


# ----------------------------------------------------------------------------------------------
class S03Copy(SpokenScene):
    def construct(self):
        cx = -2.3
        cl = cell(8.4, 6.0, cx, 0)
        nuc = nucleus(2.2, cx, -0.2)
        xs = [cx - 1.5, cx - 0.5, cx + 0.5, cx + 1.5]
        scale = 1.6
        singles = [chrom(h * scale, bw=BW * 1.2).move_to([x, -0.2, 0]) for h, x in zip(HEIGHTS, xs)]
        model = T("model cell", 28, GREY).move_to([cx, 2.55, 0])
        self.at("picture a model")
        self.play(FadeIn(cl), FadeIn(nuc), FadeIn(model), run_time=0.8)
        tag = count_tag(4).move_to([4.5, 1.5, 0])
        self.at("four chromosomes")
        self.play(LaggedStart(*[FadeIn(s, scale=0.7) for s in singles], lag_ratio=0.15), FadeIn(tag), run_time=1.3)
        self.at("in interphase")
        iphase = word("interphase", 32).move_to([4.5, 3.1, 0])
        self.play(FadeIn(iphase), run_time=0.5)
        self.at("each chromosome is copied")
        copies = [chrom(h * scale, copied=True, bw=BW * 1.2).move_to([x, -0.2, 0]) for h, x in zip(HEIGHTS, xs)]
        self.play(LaggedStart(*[ReplacementTransform(s, c) for s, c in zip(singles, copies)], lag_ratio=0.25), run_time=2.4)
        self.at("still one chromosome")
        self.play(Indicate(copies[3], color=YELLOW, scale_factor=1.25), run_time=1.0)
        call = T("1 chromosome", 30, YELLOW).move_to([4.5, -0.4, 0])
        call2 = T("2 identical copies,\njoined together", 26, TEXT).next_to(call, DOWN, buff=0.15)
        ar = Arrow(call.get_left() + LEFT * 0.05, copies[3].get_right() + RIGHT * 0.05, buff=0.08, color=YELLOW, stroke_width=4)
        self.play(FadeIn(call), FadeIn(ar), run_time=0.5)
        self.at("identical copies joined")
        self.play(FadeIn(call2), run_time=0.6)
        self.at("still has four chromosomes")
        self.play(Indicate(tag[0], color=GREEN, scale_factor=1.3), run_time=1.0)
        self.at("now has two copies")
        self.play(*[Indicate(c, color=YELLOW, scale_factor=1.12) for c in copies], run_time=1.2)
        self.finish()


# ----------------------------------------------------------------------------------------------
STAGES = ["Prophase", "Metaphase", "Anaphase", "Telophase"]
MS = 1.15            # chromosome height scale in the mitosis scenes
THICK = BW * 1.9     # thick (coiled) bar width
CY = -0.45           # cell centre y
COL_Y = [CY + (1.5 - i) * 1.2 for i in range(4)]


def tracker():
    chips = VGroup(*[T(s, 28, GREY) for s in STAGES])
    chips.arrange(RIGHT, buff=0.9).to_edge(UP, buff=0.45)
    arrows = VGroup(*[Arrow(chips[i].get_right() + RIGHT * 0.06, chips[i + 1].get_left() + LEFT * 0.06, buff=0, color=GREY,
                            stroke_width=3, tip_length=0.15) for i in range(3)])
    return chips, arrows


def hilite(chips, i):
    return [chips[j].animate.set_color(YELLOW if j == i else GREY) for j in range(4)]


class S04Line(SpokenScene):
    def construct(self):
        cl = cell(9.0, 5.2, 0, CY)
        xs = [-1.5, -0.5, 0.5, 1.5]
        copies = [chrom(h * MS, copied=True, bw=BW).move_to([x, CY, 0]) for h, x in zip(HEIGHTS, xs)]
        nuc = nucleus(2.3, 0, CY)
        self.add(cl, nuc, *copies)
        chips, arrows = tracker()
        self.at("mitosis begins")
        mt = word("mitosis", 34).move_to([0, 2.6, 0])
        self.play(FadeIn(mt), run_time=0.5)
        self.play(FadeOut(mt), run_time=0.4)
        self.at("four stages")
        self.play(FadeIn(chips), FadeIn(arrows), run_time=1.0)
        self.at("same order")
        self.play(Indicate(chips, color=YELLOW, scale_factor=1.05), run_time=1.0)
        self.at("in prophase")
        self.play(*hilite(chips, 0), FadeOut(nuc), run_time=0.5)
        thick = [chrom(h * MS, copied=True, bw=THICK).move_to([x, CY, 0]) for h, x in zip(HEIGHTS, xs)]
        self.at("coil up")
        self.play(*[Transform(c, t) for c, t in zip(copies, thick)], run_time=1.4)
        lab = T("thick enough to see", 28, TEXT).move_to([0, CY - 3.0, 0])
        self.at("thick enough to see")
        self.play(FadeIn(lab), run_time=0.5)
        self.at("in metaphase")
        self.play(*hilite(chips, 1), FadeOut(lab), run_time=0.5)
        mid = DashedLine([0, CY + 2.45, 0], [0, CY - 2.45, 0], color=GREY, stroke_width=3)
        self.at("line up")
        self.play(*[c.animate.move_to([0, y, 0]) for c, y in zip(copies, COL_Y)], Create(mid), run_time=1.2)
        self.finish()


# ----------------------------------------------------------------------------------------------
def hrow(x, scale=MS):
    """four single chromosomes in a row, as they sit in a daughter nucleus."""
    return VGroup(*[chrom(h * scale, bw=THICK) for h in HEIGHTS]).arrange(RIGHT, buff=0.25)


class S05Apart(SpokenScene):
    def construct(self):
        chips, arrows = tracker()
        for c in chips:
            c.set_color(GREY)
        chips[1].set_color(YELLOW)
        cl = cell(9.0, 5.2, 0, CY)
        copies = [chrom(h * MS, copied=True, bw=THICK).move_to([0, y, 0]) for h, y in zip(HEIGHTS, COL_Y)]
        mid = DashedLine([0, CY + 2.45, 0], [0, CY - 2.45, 0], color=GREY, stroke_width=3)
        self.add(cl, chips, arrows, mid, *copies)
        self.at("in anaphase")
        self.play(*hilite(chips, 2), FadeOut(mid), run_time=0.5)
        lefts, rights = [], []
        for h, y in zip(HEIGHTS, COL_Y):
            lefts.append(chrom(h * MS, bw=THICK).move_to([-THICK / 2 - 0.01, y, 0]))
            rights.append(chrom(h * MS, bw=THICK).move_to([THICK / 2 + 0.01, y, 0]))
        self.at("two copies of each")
        self.play(*[FadeOut(c) for c in copies], *[FadeIn(x) for x in lefts + rights], run_time=0.3)
        self.play(*[l.animate.shift(LEFT * 0.35) for l in lefts], *[r.animate.shift(RIGHT * 0.35) for r in rights], run_time=0.8)
        self.at("pulled to")
        rt = max(self.t_of("thin fibers") - self.elapsed() + 0.3, 2.0)
        self.play(*[l.animate.move_to([-3.0, l.get_center()[1], 0]) for l in lefts],
                  *[r.animate.move_to([3.0, r.get_center()[1], 0]) for r in rights], run_time=rt, rate_func=smooth)
        fibers = VGroup()
        for l in lefts:
            fibers.add(Line([-4.45, CY, 0], l.get_left(), color=GREY, stroke_width=3))
        for r in rights:
            fibers.add(Line([4.45, CY, 0], r.get_right(), color=GREY, stroke_width=3))
        self.at("fibers")
        self.play(FadeIn(fibers), run_time=0.6)
        self.at("in telophase")
        self.play(*hilite(chips, 3), FadeOut(fibers), run_time=0.5)
        n1 = nucleus(1.45, -3.0, CY)
        n2 = nucleus(1.45, 3.0, CY)
        r1 = hrow(0).move_to([-3.0, CY, 0])
        r2 = hrow(0).move_to([3.0, CY, 0])
        self.at("two new nuclei")
        self.play(FadeIn(n1), FadeIn(n2), *[l.animate.move_to(t.get_center()) for l, t in zip(lefts, r1)],
                  *[r.animate.move_to(t.get_center()) for r, t in zip(rights, r2)], run_time=1.2)
        d1 = cell(5.2, 3.4, -3.0, CY)
        d2 = cell(5.2, 3.4, 3.0, CY)
        self.at("splits into two")
        self.play(ReplacementTransform(cl, VGroup(d1, d2)), run_time=1.6)
        self.at("daughter cell")
        dl1 = word("daughter cell", 30).move_to([-3.0, -3.0, 0])
        dl2 = word("daughter cell", 30).move_to([3.0, -3.0, 0])
        self.play(FadeIn(dl1), FadeIn(dl2), run_time=0.6)
        self.at("the parent cell")
        ghost = DashedVMobject(Ellipse(width=11.8, height=4.5, color=GREY, stroke_width=3).move_to([0, CY, 0]), num_dashes=70)
        pl = word("parent cell", 30).move_to([0, CY + 2.75, 0])
        self.play(Create(ghost), FadeIn(pl), run_time=1.0)
        self.finish()


# ----------------------------------------------------------------------------------------------
class S06Answer(SpokenScene):
    def construct(self):
        Y = 0.55
        d1 = cell(5.2, 3.4, -3.0, Y)
        d2 = cell(5.2, 3.4, 3.0, Y)
        n1 = nucleus(1.45, -3.0, Y)
        n2 = nucleus(1.45, 3.0, Y)
        b1 = hrow(0).move_to([-3.0, Y, 0])
        b2 = hrow(0).move_to([3.0, Y, 0])
        lab1 = word("daughter cell", 28).move_to([-3.0, Y - 2.1, 0])
        lab2 = word("daughter cell", 28).move_to([3.0, Y - 2.1, 0])
        self.add(d1, d2, n1, n2, b1, b2, lab1, lab2)
        TY = -2.45

        def tags(n, col):
            return count_tag(n, col, wide=True).move_to([-3.0, TY, 0]), count_tag(n, col, wide=True).move_to([3.0, TY, 0])

        q = T("a complete set?", 40, RED, weight=BOLD).to_edge(UP, buff=0.55)
        self.at("get a complete set")
        self.play(FadeIn(q), run_time=0.6)
        self.at("copying comes first")
        step1 = chip("1  Copy every chromosome", BLUE, size=30).to_edge(UP, buff=0.5)
        self.play(FadeOut(q), FadeIn(step1), run_time=0.6)
        self.at("one copy of each chromosome")
        step2 = chip("2  Share: one copy of each to each new cell", GREEN, size=30).to_edge(UP, buff=0.5)
        self.play(FadeOut(step1), FadeIn(step2), run_time=0.6)
        self.at("ends up with four")
        t1, t2 = tags(4, GREEN)
        self.play(FadeIn(t1), FadeIn(t2), run_time=0.7)
        self.at("same as the parent cell")
        par = T("same as the parent cell: 4", 30, GREY).move_to([0, -3.25, 0])
        self.play(FadeIn(par), run_time=0.6)
        self.at("skip the copying")
        skip = chip("Skip the copying", RED, size=30).to_edge(UP, buff=0.5)
        gone = [b1[2], b1[3], b2[0], b2[1]]
        r1, r2 = tags(2, RED)
        self.play(FadeOut(step2), FadeIn(skip), FadeOut(par), *[FadeOut(g) for g in gone],
                  FadeOut(t1), FadeOut(t2), FadeIn(r1), FadeIn(r2), run_time=1.0)
        self.at("only two")
        self.play(Indicate(VGroup(r1, r2), color=RED, scale_factor=1.15), run_time=1.0)
        self.at("copy first then share")
        okb = chip("Copy first, then share", GREEN, size=32).to_edge(UP, buff=0.5)
        f1, f2 = tags(4, GREEN)
        self.play(FadeOut(skip), FadeIn(okb), *[FadeIn(g) for g in gone], FadeOut(r1), FadeOut(r2),
                  FadeIn(f1), FadeIn(f2), run_time=1.0)
        self.finish()


class S07End(EndCard):
    LINE = "Copy first, then share the copies."
