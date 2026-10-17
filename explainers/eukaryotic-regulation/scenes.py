"""Delete Pieces, Find the Committee (Biochemistrypedia explainer, Genetics: eukaryotic regulation)

COLOR MAP (one colour per concept, whole film)
  ORANGE = liver cells and their results
  PINK   = kidney cells and their results
  PURPLE = enhancer element A
  BLUE   = enhancer element B
  YELLOW = enhancer element C
  TEAL   = proteins that bind and bridge (transcription factors, Mediator)
  GREEN  = activity of the reporter / a gene being read
  RED    = a repressor
  GREY   = DNA, promoter, genes, labels, the "if added / if multiplied" guesses
  TEXT   = the enhancer as a whole, totals, neutral text
"""
import numpy as np
from bp_style import *  # noqa: F401,F403

PURPLE = "#B58CD9"
ORANGE = "#F29E4C"
PINK = "#E58BB0"
TEAL_P = "#3FB8C0"
ELC = {"A": PURPLE, "B": BLUE, "C": YELLOW}
BX = -1.9          # left edge of every bar
K = 0.06           # bar width per unit of activity


def arr(a, b, color=GREY, w=5, tip=0.22):
    return Arrow(a, b, buff=0.08, color=color, stroke_width=w, tip_length=tip,
                 max_tip_length_to_length_ratio=0.45, max_stroke_width_to_length_ratio=12)


def solid(m):
    """put an opaque BG-coloured backing behind a mobject so a DNA line does not show through it."""
    back = Rectangle(width=m.width, height=m.height, stroke_width=0, fill_color=BG, fill_opacity=1).move_to(m)
    return VGroup(back, m)


def bchip(text, color=BLUE, size=28, **kw):
    c = chip(text, color, size=size, **kw)
    back = RoundedRectangle(corner_radius=0.14, width=c[0].width, height=c[0].height, stroke_width=0,
                            fill_color=BG, fill_opacity=1).move_to(c[0])
    return VGroup(back, *c)


def gbox(label="", w=0.62, h=0.8, color=GREY, lit=False):
    c = GREEN if lit else color
    r = RoundedRectangle(corner_radius=0.08, width=w, height=h, stroke_color=c, stroke_width=2.5,
                         fill_color=c, fill_opacity=0.6 if lit else 0.15)
    return r


def gene_strip(cx, cy, n=6, w=0.62, gap=0.1):
    return VGroup(*[gbox(w=w) for _ in range(n)]).arrange(RIGHT, buff=gap).move_to([cx, cy, 0])


def light(box, on):
    c = GREEN if on else GREY
    return box.animate.set_stroke(c).set_fill(c, 0.6 if on else 0.15)


def element(letter, present=True, w=0.95, h=0.62, size=28, reverse=False, arrow=True, back=False):
    col = ELC[letter]
    if present:
        box = RoundedRectangle(corner_radius=0.08, width=w, height=h, stroke_color=col, stroke_width=3,
                               fill_color=col, fill_opacity=0.3)
        lab = T(letter, size, col, weight=BOLD).move_to(box)
        g = VGroup(box, lab)
        if back:
            g = VGroup(Rectangle(width=w, height=h, stroke_width=0, fill_color=BG, fill_opacity=1), g)
        if arrow:
            d = LEFT if reverse else RIGHT
            a = Arrow(box.get_bottom() + DOWN * 0.2 - d * 0.28, box.get_bottom() + DOWN * 0.2 + d * 0.28, buff=0,
                      color=col, stroke_width=3, tip_length=0.14)
            g.add(a)
        return g
    box = DashedVMobject(RoundedRectangle(corner_radius=0.08, width=w, height=h, stroke_color=GREY, stroke_width=2.5))
    lab = T(letter, size, GREY).set_opacity(0.4).move_to(box)
    if back:
        return VGroup(Rectangle(width=w, height=h, stroke_width=0, fill_color=BG, fill_opacity=1), box, lab)
    return VGroup(box, lab)


def crow(y, present="ABC", x0=-6.0, reverse=False, order="ABC", w=0.95, gap=0.1):
    g = VGroup()
    for i, L in enumerate(order):
        e = element(L, present=(L in present), w=w, reverse=reverse)
        e.move_to([x0 + w / 2 + i * (w + gap), y, 0])
        g.add(e)
    return g


def bar(value, y, color=GREEN, h=0.5):
    wd = max(value * K, 0.06)
    r = Rectangle(width=wd, height=h, stroke_width=0, fill_color=color, fill_opacity=0.85)
    return r.move_to([BX + wd / 2, y, 0])


def vlabel(value_text, b, color=TEXT, size=28):
    return M(value_text, size, color).next_to(b, RIGHT, buff=0.2)


def baseline(y0, y1):
    return Line([BX, y0, 0], [BX, y1, 0], color=GREY, stroke_width=2.5)


def grow(b):
    return GrowFromEdge(b, LEFT)


class S00Title(TitleCard):
    LESSON = "Eukaryotic Gene Regulation and Epigenetics"
    TITLE = "Delete Pieces, Find the Committee"


# ---------------------------------------------------------------------------------------------
class S01Same(SpokenScene):
    def construct(self):
        cells, strips, names = [], [], []
        for x, nm, col in ((-3.3, "liver cell", ORANGE), (3.3, "kidney cell", PINK)):
            c = RoundedRectangle(corner_radius=0.5, width=5.2, height=2.6, stroke_color=col, stroke_width=4,
                                 fill_color=col, fill_opacity=0.08).move_to([x, 0.6, 0])
            st = gene_strip(x, 0.6)
            n = T(nm, 30, col).move_to([x, 2.4, 0])
            cells.append(c); strips.append(st); names.append(n)
        eq = T("=", 60, TEXT).move_to([0, 0.6, 0])
        head = T("the same genome", 32, TEXT).move_to([0, 3.15, 0])
        self.play(FadeIn(VGroup(*cells)), FadeIn(VGroup(*names)), FadeIn(VGroup(*strips)), run_time=1.0)
        self.at("same genome")
        self.play(FadeIn(eq), FadeIn(head, shift=DOWN * 0.1), run_time=0.6)

        pat = {0: [0, 2, 3], 1: [1, 4, 5]}
        self.at("different set")
        self.play(*[light(strips[k][i], True) for k in (0, 1) for i in pat[k]], run_time=0.7)

        # daughters keep the same set
        dx = {0: [-4.7, -1.9], 1: [1.9, 4.7]}
        d_cells, d_strips, d_arrows = VGroup(), VGroup(), VGroup()
        for k, col in ((0, ORANGE), (1, PINK)):
            for x in dx[k]:
                c = RoundedRectangle(corner_radius=0.3, width=2.6, height=1.1, stroke_color=col, stroke_width=3,
                                     fill_color=col, fill_opacity=0.08).move_to([x, -2.35, 0])
                s = gene_strip(x, -2.35).scale(0.5)
                for i in pat[k]:
                    s[i].set_stroke(GREEN).set_fill(GREEN, 0.6)
                d_cells.add(c); d_strips.add(s)
                d_arrows.add(arr([-3.3 if k == 0 else 3.3, -0.8, 0], [x, -1.75, 0], col, w=3, tip=0.16))
        dlab = T("daughters", 26, GREY).move_to([0, -3.3, 0])
        self.at("its daughters")
        self.play(LaggedStart(*[GrowArrow(a) for a in d_arrows], lag_ratio=0.1), run_time=0.6)
        self.play(FadeIn(d_cells), FadeIn(d_strips), FadeIn(dlab), run_time=0.7)

        # chromatin: packed DNA is hard to read
        chipc = chip("chromatin: packed DNA", GREY, size=28).move_to([0, -2.35, 0])
        self.at("packed into")
        self.play(FadeOut(d_cells), FadeOut(d_strips), FadeOut(d_arrows), FadeOut(dlab),
                  *[light(strips[k][i], False) for k in (0, 1) for i in pat[k]], run_time=0.6)
        self.play(FadeIn(chipc, shift=UP * 0.1), run_time=0.5)
        qs = VGroup(*[T("?", 30, TEXT).move_to(b) for st in strips for b in st])
        self.at("How does a cell choose")
        self.play(LaggedStart(*[FadeIn(q, scale=0.6) for q in qs], lag_ratio=0.05), run_time=0.9)

        # the enhancer
        line = Line([-5.2, -2.35, 0], [5.2, -2.35, 0], color=GREY, stroke_width=4)
        enh = solid(RoundedRectangle(corner_radius=0.08, width=2.2, height=0.7, stroke_color=TEXT, stroke_width=3,
                               fill_color=TEXT, fill_opacity=0.15).move_to([-3.6, -2.35, 0]))
        enh_l = T("enhancer", 28, TEXT).move_to(enh)
        gn = solid(gbox(w=1.6, h=0.7).move_to([3.6, -2.35, 0]))
        gl = T("gene", 26, GREY).move_to(gn)
        self.at("called an enhancer")
        self.play(FadeOut(chipc), FadeOut(qs), FadeIn(line), run_time=0.5)
        self.play(FadeIn(enh), FadeIn(enh_l), FadeIn(gn), FadeIn(gl), run_time=0.7)
        self.play(Indicate(VGroup(enh, enh_l), color=TEXT, scale_factor=1.12), run_time=0.7)
        self.finish()


# ---------------------------------------------------------------------------------------------
class S02Region(SpokenScene):
    def construct(self):
        Y = -0.8
        line = Line([-6, Y, 0], [6, Y, 0], color=GREY, stroke_width=4)
        enh = solid(RoundedRectangle(corner_radius=0.08, width=2.8, height=0.95, stroke_color=TEXT, stroke_width=3,
                                     fill_color=TEXT, fill_opacity=0.15).move_to([-3.8, Y, 0]))
        enh_l = T("enhancer", 32, TEXT).move_to(enh)
        orient = Arrow([-4.5, Y - 0.75, 0], [-3.1, Y - 0.75, 0], buff=0, color=TEXT, stroke_width=4, tip_length=0.2)
        prom = bchip("promoter", GREY, size=30).move_to([2.0, Y, 0])
        gene = solid(RoundedRectangle(corner_radius=0.08, width=1.9, height=0.95, stroke_color=GREY, stroke_width=2.5,
                                      fill_color=GREY, fill_opacity=0.15).move_to([4.6, Y, 0]))
        gene_l = T("gene", 30, GREY).move_to(gene)
        self.add(line, enh, enh_l, prom, gene, gene_l)
        self.play(FadeIn(orient), run_time=0.3)

        tx = T("transcription", 30, GREEN).move_to([4.6, Y + 1.1, 0])
        self.at("raises transcription")
        self.play(gene[1].animate.set_stroke(GREEN).set_fill(GREEN, 0.6), FadeIn(tx, shift=UP * 0.1), run_time=0.6)

        dist = DoubleArrow([-2.2, Y + 1.1, 0], [1.2, Y + 1.1, 0], buff=0, color=TEXT, stroke_width=4, tip_length=0.2)
        dist_l = T("at a distance", 28, TEXT).next_to(dist, UP, buff=0.12)
        self.at("at a distance")
        self.play(GrowFromCenter(dist), FadeIn(dist_l), run_time=0.6)
        orient2 = Arrow([-3.1, Y - 0.75, 0], [-4.5, Y - 0.75, 0], buff=0, color=TEXT, stroke_width=4, tip_length=0.2)
        self.at("either orientation")
        self.play(ReplacementTransform(orient, orient2), run_time=0.7)
        self.wait(0.3)
        self.play(FadeOut(dist), FadeOut(dist_l), FadeOut(tx), FadeOut(orient2),
                  gene[1].animate.set_stroke(GREY).set_fill(GREY, 0.15), run_time=0.5)

        # factors, Mediator, loop
        f1 = bchip("factor", TEAL_P, size=26).move_to([-4.5, Y + 1.15, 0])
        f2 = bchip("factor", TEAL_P, size=26).move_to([-3.0, Y + 1.15, 0])
        self.at("Transcription factors")
        self.play(FadeIn(f1, shift=DOWN * 0.2), FadeIn(f2, shift=DOWN * 0.2), run_time=0.6)
        med = bchip("Mediator", TEAL_P, size=30).move_to([-0.6, Y + 2.7, 0])
        pol = bchip("RNA pol II", GREY, size=26).move_to([2.0, Y + 1.15, 0])
        l1 = Line(f2.get_top(), med.get_left(), color=TEAL_P, stroke_width=4)
        l2 = Line(med.get_right(), pol.get_top(), color=TEAL_P, stroke_width=4)
        self.at("Mediator bridges")
        self.play(FadeIn(med, shift=DOWN * 0.2), Create(l1), run_time=0.6)
        self.play(FadeIn(pol), Create(l2), run_time=0.5)
        left = Line([-6, Y, 0], [-2.4, Y, 0], color=GREY, stroke_width=4)
        right = Line([1.1, Y, 0], [6, Y, 0], color=GREY, stroke_width=4)
        mid = Line([-2.4, Y, 0], [1.1, Y, 0], color=GREY, stroke_width=4)
        loop = CubicBezier(np.array([-2.4, Y, 0]), np.array([-2.4, Y - 2.6, 0]), np.array([1.1, Y - 2.6, 0]),
                           np.array([1.1, Y, 0]), color=GREY, stroke_width=4)
        self.remove(line)
        self.add(left, right, mid)
        self.bring_to_front(enh, enh_l, prom, gene, gene_l)
        self.at("loops out")
        self.play(ReplacementTransform(mid, loop), run_time=0.9)

        # clone a region beside a reporter
        self.at("To map one")
        self.play(FadeOut(VGroup(left, right, loop, enh, enh_l, prom, gene, gene_l, f1, f2, med, pol, l1, l2)), run_time=0.6)
        Y2 = 0.2
        dna = Line([-6.1, Y2, 0], [6.1, Y2, 0], color=GREY, stroke_width=4)
        region = solid(Rectangle(width=5.4, height=1.0, stroke_color=TEXT, stroke_width=3, fill_color=TEXT,
                                 fill_opacity=0.15).move_to([-3.3, Y2, 0]))
        self.at("clone a region")
        self.play(Create(dna), FadeIn(region, scale=0.9), run_time=0.7)
        prom2 = bchip("promoter", GREY, size=30).move_to([0.9, Y2, 0])
        luc = bchip("luciferase", GREEN, size=30).move_to([3.9, Y2, 0])
        self.at("drives luciferase")
        self.play(FadeIn(prom2, shift=LEFT * 0.2), run_time=0.5)
        self.play(FadeIn(luc, shift=LEFT * 0.2), Create(arr(prom2.get_right(), luc.get_left(), GREEN)), run_time=0.6)
        rep = T("a reporter", 30, GREEN).next_to(luc, DOWN, buff=0.4)
        self.at("a reporter")
        self.play(FadeIn(rep, shift=UP * 0.1), run_time=0.5)
        bk = VGroup(Line([-6.0, Y2 + 0.8, 0], [-6.0, Y2 + 1.1, 0], color=TEXT, stroke_width=3),
                    Line([-6.0, Y2 + 1.1, 0], [-0.6, Y2 + 1.1, 0], color=TEXT, stroke_width=3),
                    Line([-0.6, Y2 + 1.1, 0], [-0.6, Y2 + 0.8, 0], color=TEXT, stroke_width=3))
        bl = T("600 base pairs", 32, TEXT).next_to(bk, UP, buff=0.15)
        self.at("base pairs")
        self.play(Create(bk), FadeIn(bl), run_time=0.6)
        els = VGroup(*[element(L, w=1.74, h=1.0, size=36, arrow=False, back=True).move_to([-5.13 + i * 1.8, Y2, 0])
                       for i, L in enumerate("ABC")])
        self.at("three elements")
        self.play(ReplacementTransform(region, els), run_time=0.9)
        self.finish()


# ---------------------------------------------------------------------------------------------
class S03Delete(SpokenScene):
    def construct(self):
        ys = [2.0, 0.6, -0.8, -2.2]
        head = T("liver cells", 32, ORANGE).move_to([-4.4, 3.2, 0])
        rows = [crow(ys[0], "ABC"), crow(ys[1], "BC"), crow(ys[2], "AC"), crow(ys[3], "AB")]
        base = baseline(2.75, -2.75)
        self.play(FadeIn(head), FadeIn(rows[0]), run_time=0.3)
        self.at("delete each element")
        self.play(LaggedStart(*[FadeIn(r) for r in rows[1:]], lag_ratio=0.2), Create(base), run_time=1.0)
        note = T("promoter alone = 1", 24, GREY).move_to([BX + 1.5, -3.15, 0])
        tick = Line([BX + K, -2.75, 0], [BX + K, -3.0, 0], color=GREY, stroke_width=2.5)
        self.at("promoter alone")
        self.play(FadeIn(note), FadeIn(tick), run_time=0.5)
        b0 = bar(100, ys[0]); v0 = vlabel("100", b0)
        self.at("full region")
        self.play(grow(b0), run_time=0.8)
        self.play(FadeIn(v0), run_time=0.2)
        b1 = bar(95, ys[1]); v1 = vlabel("95", b1)
        self.at("Delete A")
        self.play(grow(b1), run_time=0.7)
        self.play(FadeIn(v1), run_time=0.2)
        tg = T("A is dispensable", 24, GREY).move_to([BX + 1.55, ys[1] - 0.52, 0])
        self.at("dispensable")
        self.play(FadeIn(tg, shift=RIGHT * 0.1), run_time=0.4)
        b2 = bar(4, ys[2]); v2 = vlabel("4", b2)
        self.at("Delete B")
        self.play(grow(b2), run_time=0.4)
        self.play(FadeIn(v2), run_time=0.2)
        tb = T("B is needed", 24, BLUE).move_to([BX + 1.1, ys[2] - 0.52, 0])
        self.play(FadeIn(tb), run_time=0.3)
        b3 = bar(30, ys[3]); v3 = vlabel("30", b3)
        self.at("delete C")
        self.play(grow(b3), run_time=0.6)
        self.play(FadeIn(v3), run_time=0.2)
        self.finish()


# ---------------------------------------------------------------------------------------------
class S04Together(SpokenScene):
    def construct(self):
        ys = [2.0, 0.7, -0.6, -1.85, -2.9]
        head = T("liver cells", 32, ORANGE).move_to([-4.4, 3.2, 0])
        r1, r2, r3 = crow(ys[0], "B"), crow(ys[1], "C"), crow(ys[2], "BC")
        base = baseline(2.75, -3.3)
        self.play(FadeIn(head), Create(base), run_time=0.5)
        self.at("pieces alone")
        self.play(FadeIn(r1), FadeIn(r2), run_time=0.6)
        b1 = bar(5, ys[0]); v1 = vlabel("5", b1)
        self.at("B alone")
        self.play(grow(b1), FadeIn(v1), run_time=0.5)
        tg = T("B is not sufficient", 24, BLUE).move_to([BX + 1.6, ys[0] - 0.52, 0])
        self.at("not sufficient")
        self.play(FadeIn(tg), run_time=0.4)
        b2 = bar(2, ys[1]); v2 = vlabel("2", b2)
        self.at("C alone")
        self.play(grow(b2), FadeIn(v2), run_time=0.5)
        b3 = bar(90, ys[2]); v3 = vlabel("90", b3)
        self.at("C together")
        self.play(FadeIn(r3), run_time=0.3)
        self.play(grow(b3), run_time=0.9)
        self.play(FadeIn(v3), run_time=0.2)
        la = T("if added", 26, GREY).move_to([-4.6, ys[3], 0])
        ba = bar(6, ys[3], GREY); va = T("about 6", 24, GREY).next_to(ba, RIGHT, buff=0.2)
        self.at("effects added")
        self.play(FadeIn(la), grow(ba), FadeIn(va), run_time=0.6)
        lm = T("if multiplied", 26, GREY).move_to([-4.6, ys[4], 0])
        bm = bar(10, ys[4], GREY); vm = T("about 10", 24, GREY).next_to(bm, RIGHT, buff=0.2)
        self.at("they multiplied")
        self.play(FadeIn(lm), grow(bm), FadeIn(vm), run_time=0.6)
        nine = T("90 is about 9 times this", 26, TEXT).next_to(vm, RIGHT, buff=0.6)
        self.at("times the multiplied")
        self.play(FadeIn(nine, shift=LEFT * 0.1), Indicate(b3, color=GREEN, scale_factor=1.04), run_time=0.8)
        self.at("work together")
        self.play(Indicate(VGroup(r3, b3, v3), color=GREEN, scale_factor=1.05), run_time=0.8)
        self.finish()


# ---------------------------------------------------------------------------------------------
class S05Kidney(SpokenScene):
    def construct(self):
        head = T("liver cells", 32, ORANGE).move_to([-4.4, 3.2, 0])
        base = baseline(2.4, -1.3)
        ya, yb = 1.6, -0.2
        ra, rb = crow(ya, "BC"), crow(yb, "BC", order="CB", reverse=True)
        ba = bar(90, ya); va = vlabel("90", ba)
        self.add(head, base, ra, ba, va)
        bb = bar(88, yb); vb = vlabel("88", bb)
        self.at("Reverse B and C")
        self.play(FadeIn(rb), run_time=0.5)
        self.play(grow(bb), FadeIn(vb), run_time=0.8)
        ta = T("orientation does not matter here", 28, TEXT).move_to([BX + 3.0, yb - 0.95, 0])
        self.at("orientation does not")
        self.play(FadeIn(ta), run_time=0.5)

        # kidney
        yk = [2.1, 0.9, -0.3, -1.5]
        headk = T("kidney cells", 32, PINK).move_to([-4.4, 3.2, 0])
        rk = [crow(yk[0], "ABC"), crow(yk[1], "BC"), crow(yk[2], "AC"), crow(yk[3], "AB")]
        basek = baseline(2.75, -2.1)
        bk = [bar(v, y, PINK) for v, y in zip((2, 2, 1, 2), yk)]
        vk = [vlabel(t, b) for t, b in zip(("2", "2", "1", "2"), bk)]
        self.at("try kidney")
        self.play(FadeOut(VGroup(head, base, ra, ba, va, rb, bb, vb, ta)), run_time=0.5)
        self.play(FadeIn(headk), Create(basek), FadeIn(VGroup(*rk)), run_time=0.7)
        self.at("nothing scores")
        self.play(LaggedStart(*[AnimationGroup(grow(b), FadeIn(v)) for b, v in zip(bk, vk)], lag_ratio=0.2), run_time=1.0)
        c1 = chip("a needed factor is missing", TEAL_P, size=26).move_to([-2.4, -2.85, 0])
        c2 = chip("or a repressor", RED, size=26).move_to([3.9, -2.85, 0])
        self.at("simplest reading")
        self.play(FadeIn(c1, shift=UP * 0.15), run_time=0.6)
        self.at("kidney repressor")
        self.play(FadeIn(c2, shift=UP * 0.15), run_time=0.6)
        self.finish()


# ---------------------------------------------------------------------------------------------
class S06Rule(SpokenScene):
    def construct(self):
        Y = 1.0
        tag = T("reporter test", 28, GREY).move_to([-4.6, 3.2, 0])
        dna = Line([-6.1, Y, 0], [6.1, Y, 0], color=GREY, stroke_width=4)
        eA = element("A", present=False, w=1.5, h=0.85, size=34, back=True).move_to([-4.2, Y, 0])
        eB = element("B", w=1.5, h=0.85, size=34, arrow=False, back=True).move_to([-2.4, Y, 0])
        eC = element("C", w=1.5, h=0.85, size=34, arrow=False, back=True).move_to([-0.6, Y, 0])
        prom = bchip("promoter", GREY, size=28).move_to([1.8, Y, 0])
        rep = bchip("reporter", GREY, size=28).move_to([4.4, Y, 0])
        self.play(FadeIn(tag), Create(dna), FadeIn(eA), FadeIn(eB), FadeIn(eC), FadeIn(prom), FadeIn(rep), run_time=0.4)
        ring = SurroundingRectangle(VGroup(eB, eC), color=TEXT, buff=0.15, stroke_width=3)
        self.at("minimal liver enhancer")
        self.play(Create(ring), run_time=0.7)
        fb = chip("factor", TEAL_P, size=24).move_to([-2.4, Y + 1.4, 0])
        fc = chip("factor", TEAL_P, size=24).move_to([-0.6, Y + 1.4, 0])
        self.at("factors on both")
        lab1 = T("one factor: reporter off", 26, GREY).move_to([3.4, Y - 0.95, 0])
        self.play(FadeIn(fb, shift=DOWN * 0.3), FadeIn(lab1), run_time=0.5)
        self.wait(0.6)
        self.play(FadeIn(fc, shift=DOWN * 0.3), run_time=0.5)
        self.at("present at once")
        lab2 = T("both factors: on. Fits the data", 26, GREEN).move_to([3.4, Y - 0.95, 0])
        self.play(ReplacementTransform(lab1, lab2), rep[1].animate.set_stroke(GREEN).set_fill(GREEN, 0.5), rep[2].animate.set_color(GREEN), run_time=0.6)
        self.at("committee")
        self.play(Indicate(VGroup(fb, fc), color=TEAL_P, scale_factor=1.15), run_time=0.8)
        comb = T("combinatorial control", 32, TEXT).move_to([3.4, Y + 1.4, 0])
        self.at("combinatorial control")
        self.play(FadeIn(comb, shift=DOWN * 0.1), run_time=0.5)
        self.at("reporter test")
        self.play(Indicate(tag, color=GREY, scale_factor=1.15), run_time=0.6)

        # native gene
        Yn = -2.4
        nat_l = T("native gene", 28, GREY).move_to([-4.6, Yn + 1.0, 0])
        ndna = Line([-6.1, Yn, 0], [6.1, Yn, 0], color=GREY, stroke_width=4)
        nA = element("A", w=1.2, h=0.7, size=30, arrow=False, back=True).move_to([-4.4, Yn, 0])
        nB = element("B", w=1.2, h=0.7, size=30, arrow=False, back=True).move_to([-3.0, Yn, 0])
        nC = element("C", w=1.2, h=0.7, size=30, arrow=False, back=True).move_to([-1.6, Yn, 0])
        ng = solid(RoundedRectangle(corner_radius=0.08, width=2.2, height=0.8, stroke_color=GREY, stroke_width=2.5,
                              fill_color=GREY, fill_opacity=0.15).move_to([2.8, Yn, 0]))
        ngl = T("gene", 28, GREY).move_to(ng)
        self.at("native gene")
        self.play(FadeIn(nat_l), Create(ndna), FadeIn(nA), FadeIn(nB), FadeIn(nC), FadeIn(ng), FadeIn(ngl), run_time=0.9)
        nBd = element("B", present=False, w=1.2, h=0.7, size=30, back=True).move_to([-3.0, Yn, 0])
        q = T("?", 44, TEXT).move_to(ng.get_top() + UP * 0.45)
        self.at("deleting B")
        self.play(ReplacementTransform(nB, nBd), run_time=0.7)
        self.play(FadeIn(q, scale=0.6), run_time=0.4)
        self.finish()


class S07End(EndCard):
    LINE = "B and C work together. The native gene needs a test."
