"""Reproduction and meiosis: meiosis makes each mix different  (grade 7 Life Science explainer)

COLOR MAP (one color per concept, whole film)
  BLUE   = chromosomes (a bar = one chromosome; two joined bars = one copied chromosome)
  GREEN  = the strawberry plant and asexual copying (same as the parent)
  GOLD   = sex cells (egg, sperm) and the fertilized egg outline
  YELLOW = vocabulary words and allele letters
  RED    = the question marks and "different" signal
  GREY   = cell and body outlines, neutral structure, soil
  TEXT   = numbers and plain labels
"""
import numpy as np
from bp_style import *  # noqa: F401,F403

BW = 0.2
TALL = 1.1
SHORT = 0.75


def chrom(h, copied=False, bw=BW, color=BLUE):
    if not copied:
        return VGroup(RoundedRectangle(corner_radius=bw / 2, width=bw, height=h, stroke_width=0, fill_color=color, fill_opacity=1))
    a = RoundedRectangle(corner_radius=bw / 2, width=bw, height=h, stroke_width=0, fill_color=color, fill_opacity=1)
    b = a.copy()
    a.shift(LEFT * (bw / 2 + 0.01))
    b.shift(RIGHT * (bw / 2 + 0.01))
    j = Rectangle(width=2 * bw + 0.02, height=0.07, stroke_width=0, fill_color=TEXT, fill_opacity=1)
    return VGroup(a, b, j)


def cell(w, h, x=0, y=0, color=GREY):
    return Ellipse(width=w, height=h, stroke_color=color, stroke_width=4, fill_color=color, fill_opacity=0.08).move_to([x, y, 0])


def put(h, x, y, copied=False, letter=None, bw=BW):
    """a chromosome at (x, y); returns (bar, letter-or-None)."""
    bar = chrom(h, copied, bw).move_to([x, y, 0])
    lab = T(letter, 28, YELLOW, weight=BOLD).next_to(bar, UP, buff=0.1) if letter else None
    return bar, lab


def word(text, size=30):
    return T(text, size, YELLOW, weight=BOLD)


def block(label, w, h, x, y, color, size=26):
    r = RoundedRectangle(corner_radius=0.2, width=w, height=h, stroke_color=color, stroke_width=4, fill_color=color, fill_opacity=0.18).move_to([x, y, 0])
    t = T(label, size, TEXT, line_spacing=0.8).move_to(r)
    return VGroup(r, t)


def arrow(a, b, color=GREY, w=5):
    return Arrow(a, b, buff=0.08, color=color, stroke_width=w, tip_length=0.22)


class S00Title(TitleCard):
    LESSON = "Reproduction and meiosis"
    TITLE = "Meiosis makes each mix different"


# ----------------------------------------------------------------------------------------------
class S01Question(SpokenScene):
    def construct(self):
        sy = -2.05
        soil = Line([-6.3, sy, 0], [6.3, sy, 0], color=GREY, stroke_width=4)
        soil_l = T("soil", 24, GREY).move_to([-5.6, sy - 0.4, 0])
        par = block("parent\nplant", 2.4, 2.6, -4.2, -0.5, GREEN, 28)
        self.at("strawberry plant")
        self.play(Create(soil), FadeIn(soil_l), FadeIn(par, scale=0.9), run_time=1.0)
        stem = Line([-3.0, -1.7, 0], [3.0, -1.7, 0], color=GREEN, stroke_width=7)
        stem_l = T("thin stem", 26, GREEN).move_to([0, -1.25, 0])
        self.at("thin stem")
        self.play(Create(stem), FadeIn(stem_l), run_time=1.3)
        newp = block("new\nplant", 2.4, 2.6, 4.2, -0.5, GREEN, 28)
        roots = VGroup(*[Line([4.2 + dx, -1.85, 0], [4.2 + dx * 1.5, -2.85, 0], color=GREEN, stroke_width=4) for dx in (-0.5, 0, 0.5)])
        roots_l = T("roots", 24, GREEN).move_to([5.7, -2.6, 0])
        self.at("grow roots")
        self.play(FadeIn(roots, lag_ratio=0.3), FadeIn(roots_l), run_time=0.9)
        self.play(FadeIn(newp, scale=0.8), run_time=0.7)
        same = T("same genetic information", 36, GREEN, weight=BOLD).move_to([0, 2.5, 0])
        self.at("same genetic information")
        self.play(FadeIn(same, shift=DOWN * 0.15), run_time=0.7)
        self.play(Indicate(VGroup(par, newp), color=GREEN, scale_factor=1.05), run_time=0.9)
        self.at("brothers and sisters")
        self.play(FadeOut(VGroup(soil, soil_l, par, stem, stem_l, newp, roots, roots_l, same)), run_time=0.7)
        mom = block("mother", 2.4, 1.1, -2.4, 2.45, GREY, 30)
        dad = block("father", 2.4, 1.1, 2.4, 2.45, GREY, 30)
        sis = block("sister", 2.6, 1.3, -4.3, 0.2, GREY, 30)
        bro = block("brother", 2.6, 1.3, 4.3, 0.2, GREY, 30)
        a1 = arrow([-2.8, 1.9, 0], [-4.0, 0.9, 0])
        a2 = arrow([-1.9, 1.9, 0], [3.6, 0.9, 0])
        a3 = arrow([1.9, 1.9, 0], [-3.6, 0.9, 0])
        a4 = arrow([2.8, 1.9, 0], [4.0, 0.9, 0])
        self.play(FadeIn(mom), FadeIn(dad), run_time=0.5)
        self.play(GrowArrow(a3), GrowArrow(a4), GrowArrow(a1), GrowArrow(a2), FadeIn(sis), FadeIn(bro), run_time=0.9)
        self.at("look different")
        ne = T("not exact copies", 34, RED, weight=BOLD).move_to([0, 0.2, 0])
        self.play(FadeIn(ne, scale=0.8), run_time=0.7)
        q = T("Why don't you look exactly like\nyour parents or your brothers and sisters?", 36, YELLOW, line_spacing=0.9).move_to([0, -2.4, 0])
        self.at("why don't you look")
        self.play(FadeIn(q, shift=UP * 0.15), run_time=1.0)
        self.finish()


# ----------------------------------------------------------------------------------------------
class S02TwoWays(SpokenScene):
    def construct(self):
        div = Line([0, 3.2, 0], [0, -3.4, 0], color=GREY, stroke_width=2)
        h1 = word("asexual reproduction", 32).move_to([-3.3, 3.0, 0])
        self.at("a runner is")
        self.play(Create(div), FadeIn(h1), run_time=0.8)
        p = block("1 parent", 2.6, 1.3, -3.3, 1.2, GREEN, 30)
        self.at("one parent")
        self.play(FadeIn(p, scale=0.9), run_time=0.6)
        o = block("offspring", 2.6, 1.3, -3.3, -1.4, GREEN, 30)
        a = arrow([-3.3, 0.5, 0], [-3.3, -0.7, 0], GREEN)
        self.at("the offspring")
        self.play(GrowArrow(a), FadeIn(o), run_time=0.8)
        same = T("genetically the same", 30, GREEN).move_to([-3.3, -2.5, 0])
        self.at("genetically the same")
        self.play(FadeIn(same), Indicate(VGroup(p, o), color=GREEN, scale_factor=1.05), run_time=0.9)
        h2 = word("sexual reproduction", 32).move_to([3.3, 3.0, 0])
        self.at("sexual reproduction is")
        self.play(FadeIn(h2, shift=DOWN * 0.1), run_time=0.7)
        s1 = cell(2.2, 1.7, 1.9, 1.2, GOLD)
        s2 = cell(2.2, 1.7, 4.7, 1.2, GOLD)
        l1 = T("sex cell", 28, GOLD).move_to(s1)
        l2 = T("sex cell", 28, GOLD).move_to(s2)
        self.at("two sex cells")
        self.play(FadeIn(VGroup(s1, l1), scale=0.8), FadeIn(VGroup(s2, l2), scale=0.8), run_time=0.8)
        off = cell(2.8, 1.7, 3.3, -1.4, GOLD)
        offl = T("offspring", 28, TEXT).move_to(off)
        a1 = arrow([2.1, 0.3, 0], [2.9, -0.55, 0], GOLD)
        a2 = arrow([4.5, 0.3, 0], [3.7, -0.55, 0], GOLD)
        self.at("join")
        self.play(GrowArrow(a1), GrowArrow(a2), run_time=0.5)
        self.play(FadeIn(VGroup(off, offl), scale=0.8), run_time=0.7)
        self.at("one from each")
        self.play(Indicate(VGroup(s1, l1), color=GOLD, scale_factor=1.1), Indicate(VGroup(s2, l2), color=GOLD, scale_factor=1.1), run_time=1.0)
        nc = T("resemble parents,\nnot copies", 28, RED, line_spacing=0.85).move_to([3.3, -2.8, 0])
        self.at("not copies")
        self.play(FadeIn(nc), run_time=0.7)
        self.finish()


# ----------------------------------------------------------------------------------------------
class S03Pairs(SpokenScene):
    def construct(self):
        cx, cy = -2.3, -0.2
        cl = cell(8.0, 5.4, cx, cy)
        title = T("model body cell", 30, GREY).move_to([cx, 3.0, 0])
        self.at("in a body cell")
        self.play(FadeIn(cl), FadeIn(title), run_time=0.8)
        xs = [cx - 1.7, cx - 0.3, cx + 1.3, cx + 2.3]
        hs = [TALL * 1.7, TALL * 1.7, SHORT * 1.7, SHORT * 1.7]
        by = cy + 0.35
        bars = [chrom(h, bw=0.34).move_to([x, by, 0]) for x, h in zip(xs, hs)]
        self.at("chromosomes come in pairs")
        self.play(LaggedStart(*[FadeIn(b, scale=0.6) for b in bars], lag_ratio=0.2), run_time=1.2)
        br = Brace(VGroup(bars[0], bars[1]), direction=DOWN, color=YELLOW, buff=0.15)
        brl = word("chromosome pair", 26).next_to(br, DOWN, buff=0.12)
        self.at("a chromosome pair")
        self.play(GrowFromCenter(br), FadeIn(brl), run_time=0.8)
        top = by + TALL * 1.7 / 2
        mt = T("from\nmother", 24, GREY, line_spacing=0.8).move_to([xs[0], top + 0.6, 0])
        ft = T("from\nfather", 24, GREY, line_spacing=0.8).move_to([xs[1], top + 0.6, 0])
        am = arrow([xs[0], top + 0.3, 0], [xs[0], top + 0.05, 0], GREY, 3)
        af = arrow([xs[1], top + 0.3, 0], [xs[1], top + 0.05, 0], GREY, 3)
        self.at("from your mother")
        self.play(FadeIn(mt), GrowArrow(am), run_time=0.6)
        self.at("your father")
        self.play(FadeIn(ft), GrowArrow(af), run_time=0.6)
        self.at("typical human body cell")
        hum = VGroup(T("human body cell", 28, GREY), M("46", 64, TEXT, weight=BOLD), T("chromosomes", 28, TEXT), T("in 23 pairs", 28, TEXT)).arrange(DOWN, buff=0.12).move_to([4.7, 1.8, 0])
        self.play(FadeIn(hum, shift=LEFT * 0.2), run_time=0.9)
        self.at("each chromosome is copied")
        copies = [chrom(h, copied=True, bw=0.34).move_to([x, by, 0]) for x, h in zip(xs, hs)]
        mod = VGroup(T("model cell", 28, GREY), M("4", 64, TEXT, weight=BOLD), T("chromosomes", 28, TEXT)).arrange(DOWN, buff=0.12).move_to([4.7, -0.7, 0])
        self.play(*[ReplacementTransform(b, c) for b, c in zip(bars, copies)], FadeOut(VGroup(br, brl, mt, ft, am, af)), FadeIn(mod), run_time=1.8)
        self.at("still one chromosome")
        one = T("1 chromosome:\n2 joined copies", 26, YELLOW, line_spacing=0.85).move_to([4.7, -2.9, 0])
        self.play(Indicate(copies[0], color=YELLOW, scale_factor=1.15), FadeIn(one), run_time=1.2)
        self.finish()


# ----------------------------------------------------------------------------------------------
class S04Half(SpokenScene):
    def construct(self):
        px, sx, y = -3.3, 3.7, 0.5
        pc = cell(5.6, 4.2, px, y)
        bars = []
        for x, h in zip([px - 1.5, px - 0.6, px + 0.7, px + 1.5], [TALL, TALL, SHORT, SHORT]):
            bars.append(chrom(h * 1.7, copied=True, bw=0.26).move_to([x, y, 0]))
        pl = T("parent cell", 28, GREY).move_to([px, y + 2.45, 0])
        c4 = VGroup(M("4", 48, TEXT, weight=BOLD), T("chromosomes", 28, TEXT)).arrange(RIGHT, buff=0.2).move_to([px, y - 2.65, 0])
        self.at("meiosis is the cell")
        self.play(FadeIn(pc), *[FadeIn(b) for b in bars], FadeIn(pl), FadeIn(c4), run_time=0.9)
        m = word("meiosis", 36).move_to([0.75, y + 0.65, 0])
        ar = arrow([-0.2, y, 0], [1.7, y, 0], YELLOW)
        sc = cell(3.4, 3.1, sx, y, GOLD)
        scl = T("sex cell", 28, GOLD).move_to([sx, y + 2.0, 0])
        self.play(FadeIn(m, shift=DOWN * 0.1), GrowArrow(ar), run_time=0.8)
        self.at("makes sex cells")
        self.play(FadeIn(sc), FadeIn(scl), run_time=0.7)
        self.at("one chromosome from each pair")
        s1 = chrom(TALL * 1.7, copied=True, bw=0.26).move_to([sx - 0.6, y, 0])
        s2 = chrom(SHORT * 1.7, copied=True, bw=0.26).move_to([sx + 0.6, y, 0])
        self.play(FadeIn(s1, scale=0.8), FadeIn(s2, scale=0.8), Indicate(bars[0], color=YELLOW, scale_factor=1.2),
                  Indicate(bars[3], color=YELLOW, scale_factor=1.2), run_time=1.2)
        self.at("half of the parent's")
        c2 = VGroup(M("2", 48, TEXT, weight=BOLD), T("chromosomes: half", 28, TEXT)).arrange(RIGHT, buff=0.2).move_to([sx, y - 2.65, 0])
        self.play(FadeIn(c2, shift=UP * 0.1), Indicate(c2, color=YELLOW, scale_factor=1.08), run_time=1.0)
        self.at("a human egg or sperm")
        hum = VGroup(T("human egg or sperm, normally:", 30, TEXT), M("23", 48, GOLD, weight=BOLD), T("chromosomes", 28, TEXT)).arrange(RIGHT, buff=0.25).move_to([0, -3.45, 0])
        self.play(FadeIn(hum, shift=UP * 0.1), run_time=0.9)
        self.finish()


# ----------------------------------------------------------------------------------------------
class S05Sorting(SpokenScene):
    def construct(self):
        px = -3.6
        pc = cell(5.4, 4.0, px, 0.9)
        pl = T("parent cell", 28, GREY).move_to([px, 3.1, 0])
        xs = [px - 1.5, px - 0.8, px + 0.8, px + 1.5]
        hs = [TALL * 1.5, TALL * 1.5, SHORT * 1.5, SHORT * 1.5]
        pbars = [chrom(h, copied=True, bw=0.2).move_to([x, 0.8, 0]) for x, h in zip(xs, hs)]
        self.at("each pair splits up")
        self.play(FadeIn(pc), FadeIn(pl), *[FadeIn(b) for b in pbars], run_time=0.8)
        self.play(*[Indicate(pbars[i], color=YELLOW, scale_factor=1.15) for i in (0, 1)], run_time=0.8)
        self.play(*[Indicate(pbars[i], color=YELLOW, scale_factor=1.15) for i in (2, 3)], run_time=0.8)
        sA = cell(3.2, 3.0, 2.2, 1.65, GOLD)
        sB = cell(3.2, 3.0, 2.2, -1.65, GOLD)
        self.at("a mix chosen by chance")
        a1 = arrow([-0.8, 1.2, 0], [0.5, 1.7, 0], GOLD)
        a2 = arrow([-0.8, 0.4, 0], [0.5, -1.3, 0], GOLD)
        self.play(GrowArrow(a1), GrowArrow(a2), FadeIn(sA), FadeIn(sB), run_time=0.9)
        a_t = chrom(TALL * 1.5, copied=True, bw=0.2).move_to([1.75, 1.55, 0])
        a_s = chrom(SHORT * 1.5, copied=True, bw=0.2).move_to([2.65, 1.55, 0])
        b_t = chrom(TALL * 1.5, copied=True, bw=0.2).move_to([1.75, -1.75, 0])
        b_s = chrom(SHORT * 1.5, copied=True, bw=0.2).move_to([2.65, -1.75, 0])
        self.play(*[FadeIn(m, scale=0.7) for m in (a_t, a_s, b_t, b_s)], run_time=0.7)
        defn = T("allele = one version\nof a gene", 30, YELLOW, line_spacing=0.85).move_to([px, -2.1, 0])
        self.at("an allele is one version")
        self.play(FadeIn(defn), run_time=0.7)
        self.at("big b and little b")
        LB = T("B", 30, YELLOW, weight=BOLD).next_to(pbars[0], UP, buff=0.1)
        Lb = T("b", 30, YELLOW, weight=BOLD).next_to(pbars[1], UP, buff=0.1)
        sLB = T("B", 30, YELLOW, weight=BOLD).next_to(a_t, UP, buff=0.1)
        sLb = T("b", 30, YELLOW, weight=BOLD).next_to(b_t, UP, buff=0.1)
        self.play(FadeIn(LB, scale=1.4), FadeIn(Lb, scale=1.4), run_time=0.7)
        self.at("chance of carrying")
        p1 = VGroup(M("50%", 44, TEXT, weight=BOLD), T("chance of B", 26, TEXT)).arrange(DOWN, buff=0.08).move_to([5.5, 1.65, 0])
        self.play(FadeIn(sLB, scale=1.4), FadeIn(p1, shift=LEFT * 0.2), run_time=0.9)
        self.at("same chance")
        p2 = VGroup(M("50%", 44, TEXT, weight=BOLD), T("chance of b", 26, TEXT)).arrange(DOWN, buff=0.08).move_to([5.5, -1.65, 0])
        self.play(FadeIn(sLb, scale=1.4), FadeIn(p2, shift=LEFT * 0.2), run_time=0.9)
        self.finish()


# ----------------------------------------------------------------------------------------------
def mini(x, y, letters, w=3.2, h=2.9, color=GREY):
    """a cell with two pairs; letters are the two labels over the tall pair."""
    c = cell(w, h, x, y, color)
    g = VGroup(c)
    for dx, hh, lt in [(-0.95, TALL * 1.2, letters[0]), (-0.4, TALL * 1.2, letters[1]), (0.4, SHORT * 1.2, None), (0.95, SHORT * 1.2, None)]:
        b, l = put(hh, x + dx, y - 0.2, False, lt)
        g.add(b)
        if l is not None:
            g.add(l)
    return g


class S06Answer(SpokenScene):
    def construct(self):
        self.at("fertilization joins")
        egg = cell(2.8, 2.3, -4.3, 2.0, GOLD)
        spm = cell(2.8, 2.3, 4.3, 2.0, GOLD)
        el = T("egg", 28, GOLD).move_to([-4.3, 3.45, 0])
        sl = T("sperm", 28, GOLD).move_to([4.3, 3.45, 0])
        e1 = chrom(TALL, bw=0.22).move_to([-4.65, 1.95, 0])
        e2 = chrom(SHORT, bw=0.22).move_to([-3.95, 1.95, 0])
        s1 = chrom(TALL, bw=0.22).move_to([3.95, 1.95, 0])
        s2 = chrom(SHORT, bw=0.22).move_to([4.65, 1.95, 0])
        self.play(FadeIn(VGroup(egg, el, e1, e2)), FadeIn(VGroup(spm, sl, s1, s2)), run_time=0.9)
        fe = cell(4.6, 3.2, 0, -1.2, GOLD)
        fl = T("fertilized egg", 28, GOLD).move_to([0, -3.2, 0])
        f1 = chrom(TALL * 1.3, bw=0.24).move_to([-1.3, -1.2, 0])
        f2 = chrom(TALL * 1.3, bw=0.24).move_to([-0.7, -1.2, 0])
        f3 = chrom(SHORT * 1.3, bw=0.24).move_to([0.7, -1.2, 0])
        f4 = chrom(SHORT * 1.3, bw=0.24).move_to([1.3, -1.2, 0])
        a1 = arrow([-4.0, 0.7, 0], [-1.9, -0.5, 0], GOLD)
        a2 = arrow([4.0, 0.7, 0], [1.9, -0.5, 0], GOLD)
        self.play(GrowArrow(a1), GrowArrow(a2), run_time=0.5)
        self.play(FadeIn(fe), FadeIn(fl), TransformFromCopy(e1, f1), TransformFromCopy(s1, f2),
                  TransformFromCopy(e2, f3), TransformFromCopy(s2, f4), run_time=1.6)
        self.at("in humans")
        eq = M("23 + 23 = 46", 40, TEXT, weight=BOLD).move_to([0, 2.3, 0])
        hl = T("human chromosomes", 26, GREY).next_to(eq, DOWN, buff=0.15)
        self.play(FadeIn(VGroup(eq, hl), scale=0.9), run_time=0.9)
        self.at("full pairs again")
        self.play(Indicate(VGroup(f1, f2), color=YELLOW, scale_factor=1.2), run_time=0.9)
        self.play(Indicate(VGroup(f3, f4), color=YELLOW, scale_factor=1.2), run_time=0.8)
        self.at("each child grows")
        self.play(FadeOut(VGroup(egg, spm, el, sl, e1, e2, s1, s2, fe, fl, f1, f2, f3, f4, a1, a2, eq, hl)), run_time=0.7)
        lab1 = T("two parents:\neach child", 28, GOLD, line_spacing=0.85).move_to([-4.9, 1.3, 0])
        k1 = mini(-1.5, 1.3, ("B", "B"), color=GOLD)
        k2 = mini(2.1, 1.3, ("B", "b"), color=GOLD)
        ex = T("for example (an illustration)", 26, GREY).move_to([0, 3.35, 0])
        self.play(FadeIn(ex), run_time=0.5)
        self.play(FadeIn(lab1), FadeIn(k1, scale=0.85), FadeIn(k2, scale=0.85), run_time=1.4)
        self.at("brothers and sisters usually differ")
        dif = T("usually\ndiffer", 32, RED, weight=BOLD, line_spacing=0.85).move_to([5.2, 1.3, 0])
        self.play(FadeIn(dif, scale=0.8), run_time=0.7)
        lab2 = T("runner:\nparent and\nnew plant", 28, GREEN, line_spacing=0.85).move_to([-4.9, -2.0, 0])
        self.at("a runner has one parent")
        r1 = mini(-1.5, -2.0, ("B", "b"), color=GREEN)
        r2 = mini(2.1, -2.0, ("B", "b"), color=GREEN)
        self.play(FadeIn(lab2), FadeIn(r1, scale=0.85), FadeIn(r2, scale=0.85), run_time=1.0)
        self.at("genetically the same")
        same = T("same", 32, GREEN, weight=BOLD).move_to([5.2, -2.0, 0])
        self.play(FadeIn(same), run_time=0.6)
        self.finish()


class S07End(EndCard):
    LINE = "Each sex cell is a different mix, so offspring vary."
