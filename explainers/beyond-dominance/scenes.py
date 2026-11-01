"""Beyond dominant and recessive: when no allele hides the other  (Biochemistrypedia explainer)

COLOR MAP (one color per concept, whole video)
  RED    = the R allele, red phenotype (red flowers, red hairs)
  WHITE  = the W allele, white phenotype
  PINK   = the in-between phenotype (pink snapdragon flowers)
  TEAL   = a vocabulary term label (allele, heterozygous, incomplete dominance, codominance ...)
  YELLOW = ratio / expected share (1 : 2 : 1)
  BLUE   = the A marker on a red blood cell
  GREEN  = the B marker on a red blood cell
  PURPLE = a person who shows the trait (shaded pedigree symbol)
  GOLD   = chromosome 21
  GREY   = outlines, headers, structure
"""
import random
from bp_style import *  # noqa: F401,F403

WHT = "#FFFFFF"
PINK = "#F29BB5"
PURPLE = "#B58CD9"


def tok(letter, color, size=0.8):
    box = RoundedRectangle(corner_radius=0.14, width=size, height=size, stroke_color=color, stroke_width=3,
                           fill_color=color, fill_opacity=0.9)
    lt = T(letter, int(size * 46), BG, weight=BOLD).move_to(box)
    g = VGroup(box, lt)
    g.box, g.lt = box, lt
    return g


def swatch(color, size=1.1):
    return RoundedRectangle(corner_radius=0.16, width=size, height=size, stroke_color=color, stroke_width=3,
                            fill_color=color, fill_opacity=0.9)


def roan(size=1.1):
    """A coat patch: thin red and white hair bars side by side (not a drawn animal)."""
    pat = [RED, WHT, WHT, RED, RED, WHT, RED, WHT, WHT, RED, WHT, RED]
    n = len(pat)
    w = size / n
    bars = VGroup(*[Rectangle(width=w, height=size * 0.94, stroke_width=0, fill_color=c, fill_opacity=0.95)
                    for c in pat]).arrange(RIGHT, buff=0)
    frame = RoundedRectangle(corner_radius=0.16, width=size + 0.06, height=size, stroke_color=GREY, stroke_width=3)
    bars.move_to(frame)
    return VGroup(bars, frame)


def arr(a, b, color=GREY, w=5, tip=0.22):
    return Arrow(a, b, buff=0.06, color=color, stroke_width=w, tip_length=tip,
                 max_tip_length_to_length_ratio=0.45, max_stroke_width_to_length_ratio=12)


def term(text, size=30, color=TEAL):
    return T(text, size, color, weight=BOLD)


def pair(l1, c1, l2, c2, at, size=0.8, gap=1.0):
    a = tok(l1, c1, size).move_to([at[0] - gap / 2, at[1], 0])
    b = tok(l2, c2, size).move_to([at[0] + gap / 2, at[1], 0])
    return a, b


class S00Title(TitleCard):
    LESSON = "Beyond Dominant and Recessive"
    TITLE = "When no allele hides the other"


# ---------------------------------------------------------------------------------------------
class S01Pink(SpokenScene):
    """red x white -> pink; red cow x white bull -> roan; the old rule does not fit; the question."""

    def construct(self):
        y1, y2 = 2.3, -0.35
        # snapdragons
        a = swatch(RED, 1.4).move_to([-3.8, y1, 0])
        b = swatch(WHT, 1.4).move_to([0.1, y1, 0])
        x1 = T("×", 44, GREY).move_to([-1.85, y1, 0])
        la = T("red snapdragon", 24, RED).next_to(a, DOWN, buff=0.15)
        lb = T("white snapdragon", 24, WHT).next_to(b, DOWN, buff=0.15)
        ar1 = arr([1.5, y1, 0], [2.9, y1, 0])
        c = swatch(PINK, 1.4).move_to([4.5, y1, 0])
        lc = T("pink flowers", 24, PINK).next_to(c, DOWN, buff=0.15)
        self.at("Cross a red snapdragon")
        self.play(FadeIn(a, scale=0.9), FadeIn(la), run_time=0.5)
        self.play(FadeIn(x1), FadeIn(b, scale=0.9), FadeIn(lb), run_time=0.5)
        self.at("every offspring")
        self.play(GrowArrow(ar1), FadeIn(c, scale=0.8), FadeIn(lc), run_time=0.7)
        # cattle
        d = swatch(RED, 1.4).move_to([-3.8, y2, 0])
        e = swatch(WHT, 1.4).move_to([0.1, y2, 0])
        x2 = T("×", 44, GREY).move_to([-1.85, y2, 0])
        ld = T("red Shorthorn cow", 24, RED).next_to(d, DOWN, buff=0.15)
        le = T("white Shorthorn bull", 24, WHT).next_to(e, DOWN, buff=0.15)
        ar2 = arr([1.5, y2, 0], [2.9, y2, 0])
        f = roan(1.4).move_to([4.5, y2, 0])
        lf = T("roan calf", 24, TEXT).next_to(f, DOWN, buff=0.15)
        self.at("cow")
        self.play(FadeIn(d, scale=0.9), FadeIn(ld), run_time=0.5)
        self.at("white bull")
        self.play(FadeIn(x2), FadeIn(e, scale=0.9), FadeIn(le), run_time=0.5)
        self.at("The calf")
        self.play(GrowArrow(ar2), FadeIn(f, scale=0.8), FadeIn(lf), run_time=0.7)
        self.at("red hairs")
        self.play(Indicate(f, color=WHT, scale_factor=1.2), run_time=0.9)
        # the old rule
        r1 = chip("dominant allele", TEAL, 24)
        r2 = chip("recessive allele", TEAL, 24)
        rr = VGroup(r1, T("hides", 24, GREY), r2).arrange(RIGHT, buff=0.35).move_to([0, -2.5, 0])
        self.at("old rule")
        self.play(FadeIn(rr, shift=UP * 0.1), run_time=0.6)
        q = T("What is going on?", 42, TEXT, weight=BOLD).move_to([0, -3.3, 0])
        self.at("What is going on")
        self.play(FadeIn(q, shift=UP * 0.15), run_time=0.5)
        self.play(Indicate(c, color=PINK, scale_factor=1.15), Indicate(f, color=WHT, scale_factor=1.15), run_time=0.8)
        self.finish()


# ---------------------------------------------------------------------------------------------
class S02Between(SpokenScene):
    """gene -> alleles -> heterozygous -> genotypes RR, RW, WW and their colours -> in between."""

    def construct(self):
        gene = Rectangle(width=3.0, height=0.9, stroke_color=TEAL, stroke_width=4, fill_color=TEAL, fill_opacity=0.25)
        gene.move_to([0, 2.5, 0])
        gl = T("a gene", 28, TEAL, weight=BOLD).move_to(gene)
        tr = tok("R", RED, 0.9).move_to([-1.3, 0.3, 0])
        tw = tok("W", WHT, 0.9).move_to([1.3, 0.3, 0])
        a1 = arr(gene.get_bottom() + LEFT * 0.7, tr.get_top() + UP * 0.05, TEAL)
        a2 = arr(gene.get_bottom() + RIGHT * 0.7, tw.get_top() + UP * 0.05, TEAL)
        al = term("allele", 30).move_to([0, 0.3, 0])
        self.at("An allele")
        self.play(FadeIn(gene), FadeIn(gl), run_time=0.5)
        self.play(GrowArrow(a1), GrowArrow(a2), FadeIn(tr, scale=0.8), FadeIn(tw, scale=0.8), FadeIn(al), run_time=0.8)
        # heterozygous
        box = RoundedRectangle(corner_radius=0.2, width=4.6, height=1.5, stroke_color=GREY, stroke_width=3).move_to([0, 0.3, 0])
        hl = term("heterozygous", 34).move_to([0, 1.6, 0])
        dl = T("two different alleles", 26, GREY).move_to([0, -1.75, 0])
        self.at("heterozygous plant")
        self.play(FadeOut(VGroup(gene, gl, a1, a2, al)), FadeIn(box), FadeIn(hl), run_time=0.6)
        self.play(FadeIn(dl), run_time=0.4)
        rl = T("red allele", 24, RED).move_to([-1.3, -0.85, 0])
        wl = T("white allele", 24, WHT).move_to([1.3, -0.85, 0])
        self.at("red allele")
        self.play(FadeIn(rl), Indicate(tr, color=RED), run_time=0.5)
        self.at("white allele")
        self.play(FadeIn(wl), Indicate(tw, color=WHT), run_time=0.5)
        # genotypes
        x0, x1, x2 = -4.2, 0.0, 4.2
        yt, ys, yn = 0.0, 1.95, -1.1
        rr = pair("R", RED, "R", RED, [x0, yt])
        ww = pair("W", WHT, "W", WHT, [x2, yt])
        sr, sp, sw_ = swatch(RED, 1.3).move_to([x0, ys, 0]), swatch(PINK, 1.3).move_to([x1, ys, 0]), swatch(WHT, 1.3).move_to([x2, ys, 0])
        nr, npk, nw = T("red", 28, RED).move_to([x0, yn, 0]), T("pink", 28, PINK).move_to([x1, yn, 0]), T("white", 28, WHT).move_to([x2, yn, 0])
        self.at("is red")
        self.play(FadeOut(VGroup(box, hl, dl, rl, wl)), tr.animate.move_to([x1 - 0.5, yt, 0]), tw.animate.move_to([x1 + 0.5, yt, 0]),
                  FadeIn(VGroup(*rr), scale=0.8), run_time=0.7)
        self.play(FadeIn(sr, scale=0.8), FadeIn(nr), run_time=0.5)
        self.at("is white")
        self.play(FadeIn(VGroup(*ww), scale=0.8), run_time=0.5)
        self.play(FadeIn(sw_, scale=0.8), FadeIn(nw), run_time=0.5)
        self.at("is pink")
        self.play(FadeIn(sp, scale=0.8), FadeIn(npk), Indicate(VGroup(tr, tw), color=PINK), run_time=0.7)
        ti = term("incomplete dominance", 38).move_to([0, -2.45, 0])
        self.at("incomplete dominance")
        self.play(FadeIn(ti, shift=UP * 0.1), run_time=0.5)
        bt = T("in between", 28, PINK).move_to([x1, -1.75, 0])
        self.at("in between")
        self.play(FadeIn(bt), Indicate(sp, color=PINK, scale_factor=1.2), run_time=0.7)
        self.finish()


# ---------------------------------------------------------------------------------------------
class S03Return(SpokenScene):
    """paint stays mixed; but a pink plant passes separate R or W; pink x pink Punnett square 1:2:1."""

    def construct(self):
        # paint analogy
        d1 = Circle(radius=1.0, stroke_color=RED, fill_color=RED, fill_opacity=0.9).move_to([-1.6, 0.6, 0])
        d2 = Circle(radius=1.0, stroke_color=WHT, fill_color=WHT, fill_opacity=0.9).move_to([1.6, 0.6, 0])
        pl = T("mixing paint", 32, TEXT).move_to([0, 2.5, 0])
        self.at("mixing paint")
        self.play(FadeIn(d1, scale=0.8), FadeIn(d2, scale=0.8), FadeIn(pl), run_time=0.6)
        m = Circle(radius=1.25, stroke_color=PINK, fill_color=PINK, fill_opacity=0.9).move_to([0, 0.6, 0])
        self.play(d1.animate.move_to([0, 0.6, 0]), d2.animate.move_to([0, 0.6, 0]), run_time=0.7)
        self.play(FadeOut(d1), FadeOut(d2), FadeIn(m), run_time=0.3)
        ml = T("paint stays mixed", 32, TEXT).move_to([0, -1.1, 0])
        self.at("paint stays mixed")
        self.play(FadeIn(ml, shift=UP * 0.1), run_time=0.5)
        self.wait(self.beat(0.05))
        # Punnett square
        cx, cy, cs = 0.2, -0.5, 1.7
        cells = {}
        for i, xs in enumerate([-0.5, 0.5]):
            for j, ys in enumerate([0.5, -0.5]):
                cells[(i, j)] = Square(cs, stroke_color=GREY, stroke_width=3).move_to([cx + xs * cs, cy + ys * cs, 0])
        grid = VGroup(*cells.values())
        top = [tok("R", RED, 0.7).move_to([cx - 0.5 * cs, cy + cs + 0.55, 0]), tok("W", WHT, 0.7).move_to([cx + 0.5 * cs, cy + cs + 0.55, 0])]
        left = [tok("R", RED, 0.7).move_to([cx - cs - 0.55, cy + 0.5 * cs, 0]), tok("W", WHT, 0.7).move_to([cx - cs - 0.55, cy - 0.5 * cs, 0])]
        p1 = VGroup(swatch(PINK, 0.7), T("pink plant", 24, PINK)).arrange(RIGHT, buff=0.2).move_to([cx + 3.9, cy + cs + 0.55, 0])
        p2 = VGroup(swatch(PINK, 0.7), T("pink plant", 24, PINK)).arrange(RIGHT, buff=0.2).move_to([cx - 4.6, cy + cs + 0.55, 0])
        sc = T("sex cells", 26, TEAL, weight=BOLD).move_to([cx, cy + cs + 1.25, 0])
        self.at("A pink plant passes")
        self.play(FadeOut(m), FadeOut(ml), FadeOut(pl), FadeIn(p1), run_time=0.5)
        self.at("separate")
        self.play(FadeIn(top[0], shift=DOWN * 0.2), FadeIn(top[1], shift=DOWN * 0.2), FadeIn(sc), run_time=0.7)
        self.at("Cross two pink plants")
        self.play(FadeIn(p2), FadeIn(left[0], shift=RIGHT * 0.2), FadeIn(left[1], shift=RIGHT * 0.2), run_time=0.7)
        self.at("punnet")
        self.play(Create(grid), run_time=0.7)
        spec = {(0, 0): ("RR", RED), (1, 0): ("RW", PINK), (0, 1): ("RW", PINK), (1, 1): ("WW", WHT)}
        fills = {}
        for k, (g, col) in spec.items():
            f = Square(cs - 0.1, stroke_width=0, fill_color=col, fill_opacity=0.85).move_to(cells[k])
            t = T(g, 34, BG, weight=BOLD).move_to(cells[k])
            fills[k] = VGroup(f, t)
        ratio = T("1 red : 2 pink : 1 white", 30, YELLOW, weight=BOLD).move_to([cx, cy - cs - 0.6, 0])
        self.at("one red")
        self.play(FadeIn(fills[(0, 0)], scale=0.8), run_time=0.4)
        self.at("two pink", nth=1)
        self.play(FadeIn(fills[(1, 0)], scale=0.8), FadeIn(fills[(0, 1)], scale=0.8), run_time=0.5)
        self.at("one white")
        self.play(FadeIn(fills[(1, 1)], scale=0.8), FadeIn(ratio), run_time=0.5)
        note = T("red and white\ncome back", 28, TEXT, line_spacing=0.9).move_to([cx + 4.4, cy - 0.2, 0])
        self.at("come back")
        self.play(FadeIn(note), ScaleInPlace(fills[(0, 0)], 1.12, rate_func=there_and_back), ScaleInPlace(fills[(1, 1)], 1.12, rate_func=there_and_back), run_time=0.9)
        sep = T("alleles stay separate", 28, TEAL, weight=BOLD).move_to([cx + 4.4, cy - 1.4, 0])
        self.at("never blended")
        self.play(FadeIn(sep, shift=UP * 0.1), run_time=0.5)
        self.finish()


# ---------------------------------------------------------------------------------------------
class S04Both(SpokenScene):
    """codominance: roan shows both; 1:2:1; then ABO markers."""

    def construct(self):
        ct = term("codominance", 44).move_to([0, 3.0, 0])
        self.at("Codeminence")
        self.play(FadeIn(ct, shift=DOWN * 0.1), run_time=0.5)
        tx = T("both alleles show fully", 30, TEXT).move_to([0, 2.3, 0])
        self.at("both alleles show fully")
        self.play(FadeIn(tx), run_time=0.5)
        rn = roan(2.4).move_to([-4.6, 0.2, 0])
        rl = T("R W: roan", 28, TEXT).next_to(rn, DOWN, buff=0.2)
        self.at("cattle")
        self.play(FadeIn(rn, scale=0.8), FadeIn(rl), run_time=0.7)
        # hairs
        h1 = Rectangle(width=0.22, height=1.1, stroke_width=0, fill_color=RED, fill_opacity=1).move_to([-1.85, 0.2, 0])
        h2 = Rectangle(width=0.22, height=1.1, stroke_width=0, fill_color=WHT, fill_opacity=1).move_to([-1.55, 0.2, 0])
        hh = VGroup(h1, h2)
        lh1 = T("red hair", 24, RED).move_to([-2.4, -0.9, 0])
        lh2 = T("white hair", 24, WHT).move_to([-0.6, -0.9, 0])
        self.at("Each hair")
        self.play(FadeIn(hh, scale=0.8), run_time=0.4)
        self.at("red or white")
        self.play(FadeIn(lh1), FadeIn(lh2), run_time=0.5)
        sb = T("side by side", 26, GREY).move_to([-1.7, 1.2, 0])
        self.at("side by side")
        self.play(FadeIn(sb), run_time=0.4)
        # roan x roan
        lab = T("roan × roan", 26, GREY).move_to([3.9, 1.4, 0])
        sq = [swatch(RED, 0.95), roan(0.95), roan(0.95), swatch(WHT, 0.95)]
        row = VGroup(*sq).arrange(RIGHT, buff=0.2).move_to([3.9, 0.2, 0])
        # keep row inside the frame
        row.move_to([3.9, 0.2, 0])
        self.at("roan by roan")
        self.play(FadeIn(lab), run_time=0.4)
        self.at("one red")
        self.play(FadeIn(sq[0], scale=0.8), run_time=0.3)
        self.at("two roan")
        self.play(FadeIn(sq[1], scale=0.8), FadeIn(sq[2], scale=0.8), run_time=0.4)
        self.at("one white")
        ratio = T("1 : 2 : 1", 32, YELLOW, weight=BOLD).move_to([3.9, -1.3, 0])
        self.play(FadeIn(sq[3], scale=0.8), FadeIn(ratio), run_time=0.4)
        onavg = T("on average", 24, GREY).next_to(ratio, DOWN, buff=0.15)
        self.at("on average")
        self.play(FadeIn(onavg), run_time=0.3)
        # blood types
        old = VGroup(ct, tx, rn, rl, hh, lh1, lh2, sb, lab, row, ratio, onavg)
        names = ["A", "B", "AB", "O"]
        xs = [-4.5, -1.5, 1.5, 4.5]
        cells = [Circle(radius=1.15, stroke_color=GREY, stroke_width=4, fill_color=RED, fill_opacity=0.12).move_to([x, 0.1, 0]) for x in xs]
        tl = [T("type " + n, 30, TEXT, weight=BOLD).move_to([x, -1.6, 0]) for n, x in zip(names, xs)]
        title = T("ABO blood type", 38, TEXT, weight=BOLD).move_to([0, 2.8, 0])
        self.at("blood type")
        self.play(FadeOut(old), run_time=0.4)
        self.play(FadeIn(title), run_time=0.4)
        self.at("red blood cells")
        self.play(LaggedStart(*[FadeIn(c, scale=0.8) for c in cells], lag_ratio=0.15), run_time=0.8)
        self.play(FadeIn(VGroup(*tl)), run_time=0.4)

        def marker(letter, color, x, dx):
            return tok(letter, color, 0.6).move_to([x + dx, 1.25, 0])
        mA = [marker("A", BLUE, xs[0], 0), marker("A", BLUE, xs[2], -0.35)]
        mB = [marker("B", GREEN, xs[1], 0), marker("B", GREEN, xs[2], 0.35)]
        self.at("marker")
        self.play(*[FadeIn(m, scale=0.7) for m in mA], run_time=0.5)
        self.at("marker", nth=1)
        self.play(*[FadeIn(m, scale=0.7) for m in mB], run_time=0.5)
        self.at("or neither")
        neither = T("no marker", 24, GREY).move_to([xs[3], 1.65, 0])
        self.play(FadeIn(neither), run_time=0.4)
        self.at("carries both")
        self.play(Indicate(cells[2], color=TEXT, scale_factor=1.2), Indicate(VGroup(mA[1], mB[1]), color=TEXT), run_time=0.9)
        self.finish()


# ---------------------------------------------------------------------------------------------
class S05Family(SpokenScene):
    """a pedigree with two unshaded parents and a shaded child; then a karyotype and trisomy 21."""

    def construct(self):
        def sq(cx, cy, shaded=False, s=0.9):
            return Square(s, stroke_color=GREY, stroke_width=4, fill_color=PURPLE, fill_opacity=0.95 if shaded else 0).move_to([cx, cy, 0])

        def ci(cx, cy, shaded=False, s=0.9):
            return Circle(radius=s / 2, stroke_color=GREY, stroke_width=4, fill_color=PURPLE, fill_opacity=0.95 if shaded else 0).move_to([cx, cy, 0])
        fam = T("families", 30, GREY)
        ttl = T("a family chart", 32, TEXT).move_to([0, 3.0, 0])
        dad = sq(-1.0, 1.7)
        mom = ci(1.0, 1.7)
        pl = Line([-0.55, 1.7, 0], [0.55, 1.7, 0], color=GREY, stroke_width=4)
        drop = Line([0, 1.7, 0], [0, 0.6, 0], color=GREY, stroke_width=4)
        bar = Line([-2.4, 0.6, 0], [2.4, 0.6, 0], color=GREY, stroke_width=4)
        kids = [sq(-2.4, -0.4), ci(0, -0.4, shaded=True), sq(2.4, -0.4)]
        ticks = [Line([x, 0.6, 0], [x, 0.05, 0], color=GREY, stroke_width=4) for x in (-2.4, 0, 2.4)]
        gI = T("I", 28, GREY).move_to([-4.4, 1.7, 0])
        gII = T("II", 28, GREY).move_to([-4.4, -0.4, 0])
        self.at("existing families")
        self.play(FadeIn(ttl, shift=DOWN * 0.1), run_time=0.5)
        pedname = term("pedigree", 36).move_to([0, 3.0, 0])
        self.at("pedigree is a chart")
        self.play(FadeOut(ttl), FadeIn(pedname), Create(dad), Create(mom), Create(pl), FadeIn(gI), run_time=0.8)
        self.play(Create(drop), Create(bar), *[Create(t) for t in ticks], FadeIn(gII), run_time=0.6)
        self.play(*[Create(k) for k in kids], run_time=0.6)
        key = VGroup(Square(0.45, stroke_color=GREY, stroke_width=3, fill_color=PURPLE, fill_opacity=0.95), T("shows the trait", 26, PURPLE)).arrange(RIGHT, buff=0.2).move_to([4.3, 1.7, 0])
        self.at("shaded symbol")
        self.play(FadeIn(key), Indicate(kids[1], color=PURPLE, scale_factor=1.2), run_time=0.7)
        un = T("unshaded parents", 26, TEXT).move_to([0, 2.55, 0])
        self.at("unshaded parents")
        self.play(FadeIn(un), Indicate(dad, color=TEXT), Indicate(mom, color=TEXT), run_time=0.8)
        clue = T("a clue for a recessive trait", 30, TEXT).move_to([0, -1.8, 0])
        self.at("clue")
        self.play(FadeIn(clue, shift=UP * 0.1), run_time=0.5)
        np_ = T("not proof", 30, YELLOW, weight=BOLD).move_to([0, -2.5, 0])
        self.at("not proof")
        self.play(FadeIn(np_), run_time=0.4)
        # karyotype
        ped = VGroup(pedname, un, dad, mom, pl, drop, bar, *ticks, *kids, key, gI, gII, clue, np_)
        counts = [8, 8, 7]
        hs = [1.3 - 0.035 * i for i in range(23)]
        homes = []  # center of each pair slot
        idx = 0
        for r, n in enumerate(counts):
            for c in range(n):
                homes.append((-4.5 + c * 1.3 if n == 8 else -3.85 + c * 1.3, 1.75 - r * 1.75))
        bars = []
        for p in range(23):
            for k in range(2):
                bars.append((p, Rectangle(width=0.2, height=hs[p], stroke_width=0, fill_color=GREY, fill_opacity=0.9)))
        rnd = random.Random(7)
        scat = []
        for p, b in bars:
            scat.append((rnd.uniform(-5.2, 5.2), rnd.uniform(-2.2, 2.4)))
        angs = []
        for (p, b), (sx, sy) in zip(bars, scat):
            ang = rnd.uniform(-0.9, 0.9)
            angs.append(ang)
            b.move_to([sx, sy, 0]).rotate(ang)
        kt = term("karyotype", 36).move_to([0, 3.15, 0])
        self.at("karyotype is a picture")
        self.play(FadeOut(ped), FadeIn(kt), FadeIn(VGroup(*[b for _, b in bars]), scale=0.7), run_time=0.9)
        anims = []
        for i, (p, b) in enumerate(bars):
            hx, hy = homes[p]
            anims.append(b.animate.rotate(-angs[i]).move_to([hx + (-0.17 if i % 2 == 0 else 0.17), hy, 0]))
        self.at("sorted into pairs")
        self.play(LaggedStart(*[AnimationGroup(a) for a in anims], lag_ratio=0.02), run_time=1.6)
        cnt = T("46 chromosomes = 23 pairs", 30, TEXT, weight=BOLD).move_to([0, -3.2, 0])
        self.at("human body cell")
        self.play(FadeIn(cnt, shift=UP * 0.1), run_time=0.5)
        # pair 21
        hx, hy = homes[20]
        hl = SurroundingRectangle(VGroup(bars[40][1], bars[41][1]), color=GOLD, buff=0.15, stroke_width=3)
        l21 = T("chromosome 21", 24, GOLD).next_to(hl, DOWN, buff=0.12)
        self.at("Three copies")
        self.play(Create(hl), FadeIn(l21), run_time=0.6)
        third = Rectangle(width=0.2, height=hs[20], stroke_width=0, fill_color=GOLD, fill_opacity=1).move_to([hx + 0.5, hy, 0])
        for _, b in bars[40:42]:
            b.set_fill(GOLD)
        hl2 = SurroundingRectangle(VGroup(bars[40][1], bars[41][1], third), color=GOLD, buff=0.15, stroke_width=3)
        tri = term("trisomy 21", 30, GOLD).move_to([-1.8, -3.2, 0])
        self.at("trisomy")
        self.play(FadeIn(third, shift=DOWN * 0.3), Transform(hl, hl2), FadeOut(cnt), FadeIn(tri), run_time=0.8)
        c47 = T("47 chromosomes", 30, TEXT, weight=BOLD).next_to(tri, RIGHT, buff=0.6)
        self.at("a cell with it")
        self.play(FadeIn(c47), run_time=0.5)
        self.finish()


# ---------------------------------------------------------------------------------------------
class S06Answer(SpokenScene):
    """the question answered: two patterns, alleles stay separate, and the tools."""

    def construct(self):
        q = T("What if neither allele is fully dominant?", 38, TEXT, weight=BOLD).move_to([0, 3.05, 0])
        self.at("neither allele")
        self.play(FadeIn(q, shift=DOWN * 0.1), run_time=0.6)
        xl, xr = -3.3, 3.3
        t1 = term("incomplete dominance", 34).move_to([xl, 2.1, 0])
        t2 = term("codominance", 34).move_to([xr, 2.1, 0])
        a1 = pair("R", RED, "W", WHT, [xl, 1.2])
        a2 = pair("R", RED, "W", WHT, [xr, 1.2])
        s1 = swatch(PINK, 1.8).move_to([xl, -0.8, 0])
        s2 = roan(1.8).move_to([xr, -0.8, 0])
        l1 = T("in between", 28, PINK).move_to([xl, -2.0, 0])
        l2 = T("shows both alleles", 28, TEXT).move_to([xr, -2.0, 0])
        d1 = arr([xl, 0.75, 0], [xl, 0.2, 0])
        d2 = arr([xr, 0.75, 0], [xr, 0.2, 0])
        self.at("incomplete dominance")
        self.play(FadeIn(t1), FadeIn(VGroup(*a1), scale=0.8), run_time=0.6)
        self.at("in between")
        self.play(GrowArrow(d1), FadeIn(s1, scale=0.8), FadeIn(l1), run_time=0.7)
        self.at("codaminants")
        self.play(FadeIn(t2), FadeIn(VGroup(*a2), scale=0.8), run_time=0.6)
        self.at("shows both alleles")
        self.play(GrowArrow(d2), FadeIn(s2, scale=0.8), FadeIn(l2), run_time=0.7)
        sep = T("the alleles stay separate", 32, TEAL, weight=BOLD).move_to([0, -2.85, 0])
        self.at("stay separate")
        self.play(FadeIn(sep, shift=UP * 0.1), Indicate(VGroup(*a1), color=TEXT), Indicate(VGroup(*a2), color=TEXT), run_time=0.8)
        ret = T("red and white offspring return", 28, TEXT).move_to([0, -3.3, 0])
        self.at("red and white offspring")
        self.play(FadeIn(ret), run_time=0.5)
        # the tools
        c1 = chip("pedigree: traits in families", TEAL, 26)
        c2 = chip("karyotype: whole chromosomes", TEAL, 26)
        tools = VGroup(c1, c2).arrange(RIGHT, buff=0.5).move_to([0, -3.0, 0])
        self.at("Pedigrees and karyotypes")
        self.play(FadeOut(sep), FadeOut(ret), FadeIn(tools, shift=UP * 0.1), run_time=0.7)
        self.finish()


class S07End(EndCard):
    LINE = "The alleles stay separate, even when neither is fully dominant."
