"""Cre-lox and binary expression systems: deleting a gene only where Cre acts  (methods film)

Timed to the SPOKEN words: every self.at("...") cue waits for that phrase in audio/words.json.

COLOR MAP (one color per concept, whole video)
  BLUE   = Cre (and Flp): the recombinase enzyme
  YELLOW = loxP sites (and FRT sites), questions marks
  GREEN  = a gene that works / is read; a glowing reporter cell; the intact floxed allele
  RED    = deleted gene, loss, the pitfall
  ORANGE = the transcriptional stop
  TEAL   = tamoxifen
  PURPLE = the modified estrogen receptor (ER)
  PINK   = GAL4 (the yeast activator)
  GREY   = cells, tissues, structure, de-emphasised text
  GOLD   = names and dates, the controls, the closing rule
"""
import numpy as np
from bp_style import *  # noqa: F401,F403

PURPLE = "#B58CD9"
ORANGE = "#F29E4C"
PINK = "#E87FB0"


# ---------------------------------------------------------------------------------------------
# helpers
# ---------------------------------------------------------------------------------------------
def lab(text, size=24, color=GREY, **kw):
    return T(text, size, color, **kw)


def lines(*texts, size=24, color=TEXT, buff=0.14, align=LEFT, colors=None):
    g = VGroup(*[T(t, size, (colors[i] if colors else color)) for i, t in enumerate(texts)])
    return g.arrange(DOWN, aligned_edge=align, buff=buff)


def arr(a, b, color=GREY, w=5, tip=0.2):
    return Arrow(a, b, buff=0.0, color=color, stroke_width=w, tip_length=tip,
                 max_tip_length_to_length_ratio=0.45, max_stroke_width_to_length_ratio=12)


def at(x, y):
    return np.array([x, y, 0.0])


def cell(x, y, r=0.3, color=GREEN, op=0.35, sw=3):
    return Circle(radius=r, stroke_color=color, stroke_width=sw, fill_color=color, fill_opacity=op).move_to(at(x, y))


def red(m):
    return m.animate.set_stroke(RED).set_fill(RED, 0.45)


def green(m):
    return m.animate.set_stroke(GREEN).set_fill(GREEN, 0.35)


def ring(c, r, color=GREEN):
    """A faint halo around a glowing cell (outline only)."""
    return Circle(radius=r, stroke_color=color, stroke_width=3, fill_opacity=0).move_to(c).set_stroke(opacity=0.45)


def tissue(label, x, y, w=3.5, h=2.4, color=GREEN, cr=0.3):
    """A grey panel of six cells (two rows of three). .cells and .lbl are kept for animation."""
    panel = RoundedRectangle(corner_radius=0.2, width=w, height=h, stroke_color=GREY, stroke_width=2.5,
                             fill_color=GREY, fill_opacity=0.08).move_to(at(x, y))
    cells = []
    for r in range(2):
        for c in range(3):
            cells.append(cell(x + (c - 1) * (w / 3.4), y + (0.5 - r) * (h / 2.6), cr, color))
    lbl = T(label, 24, GREY).next_to(panel, DOWN, buff=0.15)
    g = VGroup(panel, *cells, lbl)
    g.panel, g.cells, g.lbl = panel, cells, lbl
    return g


def tri(x, y, color=YELLOW, s=0.36):
    t = Triangle(stroke_color=color, stroke_width=2.5, fill_color=color, fill_opacity=0.9).scale(s / 2)
    t.rotate(-PI / 2).move_to(at(x, y))
    return t


def block(x, y, w, h, color, text="", size=24, op=0.30):
    r = RoundedRectangle(corner_radius=0.1, width=w, height=h, stroke_color=color, stroke_width=3,
                         fill_color=color, fill_opacity=op).move_to(at(x, y))
    back = RoundedRectangle(corner_radius=0.1, width=w, height=h, stroke_width=0, fill_color=BG,
                            fill_opacity=1).move_to(at(x, y)).set_z_index(-1)
    g = VGroup(r, back)
    if text:
        g.add(T(text, size, color).move_to(r))
    return g


def dna(x0, x1, y, color=GREY):
    return Line(at(x0, y), at(x1, y), color=color, stroke_width=5).set_z_index(-3)


def cre_chip(x, y, size=30):
    return chip("Cre", BLUE, size).move_to(at(x, y))


def cross_out(m, color=RED):
    return VGroup(Line(m.get_corner(UL), m.get_corner(DR), color=color, stroke_width=6),
                  Line(m.get_corner(DL), m.get_corner(UR), color=color, stroke_width=6))


def bar(cx, y, w, k, n, w_h=0.55, hi=RED, lo=GREEN):
    """Stacked bar of n offspring: k in colour hi (left part), the rest lo."""
    wk = w * k / n
    parts = VGroup()
    if k > 0:
        parts.add(Rectangle(width=wk, height=w_h, stroke_width=0, fill_color=hi, fill_opacity=0.75)
                  .move_to(at(cx - w / 2 + wk / 2, y)))
    if n - k > 0:
        parts.add(Rectangle(width=w - wk, height=w_h, stroke_width=0, fill_color=lo, fill_opacity=0.75)
                  .move_to(at(cx + w / 2 - (w - wk) / 2, y)))
    frame = Rectangle(width=w, height=w_h, stroke_color=GREY, stroke_width=2.5).move_to(at(cx, y))
    return VGroup(parts, frame)


# ---------------------------------------------------------------------------------------------
class S00Title(TitleCard):
    LESSON = "Methods library"
    TITLE = "Deleting a Gene Only Where Cre Acts"


# ---------------------------------------------------------------------------------------------
class S01Problem(SpokenScene):
    """whole-body knockout; which tissue? chosen cells and time; Gu 1994 T-cell deletion viable."""

    def construct(self):
        kw = dict(w=4.0, h=3.0, cr=0.36)
        P = [tissue("tissue A", -4.4, 0.3, **kw), tissue("tissue B", 0.0, 0.3, **kw), tissue("tissue C", 4.4, 0.3, **kw)]
        allc = [c for p in P for c in p.cells]

        self.at("knockout can kill")
        self.play(*[FadeIn(p) for p in P], run_time=0.7)
        top = lab("gene gone in every cell", 32, RED).move_to(at(0, 2.8))
        self.play(*[red(c) for c in allc], FadeIn(top), run_time=0.8)

        self.at("the embryo")
        die = chip("embryo dies", RED, 34).move_to(at(0, -2.6))
        self.play(FadeIn(die, shift=UP * 0.15), run_time=0.5)

        self.at("which tissue needed the gene")
        qs = VGroup(*[T("?", 60, YELLOW, weight=BOLD).move_to(at(x, 2.5)) for x in (-4.4, 0.0, 4.4)])
        self.play(FadeOut(die), FadeOut(top), FadeIn(qs, shift=DOWN * 0.1), run_time=0.6)

        self.at("chosen cells")
        top2 = lab("gene gone only in chosen cells", 32, TEXT).move_to(at(0, 2.8))
        self.play(FadeOut(qs), *[green(c) for c in allc], FadeIn(top2), run_time=0.6)
        self.play(*[red(c) for c in P[1].cells], run_time=0.6)

        self.at("chosen time")
        tl = arr(at(-4.5, -2.5), at(4.5, -2.5), GREY, 4)
        tl_l = lab("time", 28, GREY).move_to(at(5.1, -2.5))
        mk = Line(at(0, -2.2), at(0, -2.8), color=RED, stroke_width=6)
        mk_l = lab("deleted from here", 28, RED).move_to(at(0, -3.2))
        self.play(GrowArrow(tl), FadeIn(tl_l), FadeIn(mk), FadeIn(mk_l), run_time=0.7)

        self.at("In 1994")
        gu = lab("Gu and colleagues, 1994", 32, GOLD).move_to(at(0, 2.8))
        newl = T("T cells", 24, GREY).move_to(P[2].lbl)
        self.play(FadeOut(tl), FadeOut(tl_l), FadeOut(mk), FadeOut(mk_l), FadeOut(top2),
                  *[green(c) for c in allc], Transform(P[2].lbl, newl), FadeIn(gu), run_time=0.7)

        self.at("in T cells only")
        self.play(*[red(c) for c in P[2].cells], run_time=0.6)

        self.at("The mice were viable")
        ok = chip("mice viable", GREEN, 30).move_to(at(-4.0, -2.7))
        self.play(FadeIn(ok, shift=UP * 0.15), run_time=0.5)

        self.at("germline mutation")
        bad = chip("same mutation in the germline: lethal", RED, 28).move_to(at(2.4, -2.7))
        self.play(FadeIn(bad, shift=UP * 0.15), run_time=0.5)
        self.finish()


# ---------------------------------------------------------------------------------------------
class S02Cre(SpokenScene):
    """Cre cuts at loxP; a floxed gene is intact until Cre acts; same-direction sites: excision."""

    def construct(self):
        cre = cre_chip(-4.6, 2.9, 36)
        self.at("is an enzyme")
        self.play(FadeIn(cre, shift=DOWN * 0.15), run_time=0.5)
        self.at("bacterial virus")
        virus = lab("from a bacterial virus", 28, GREY).next_to(cre, RIGHT, buff=0.3)
        self.play(FadeIn(virus), run_time=0.5)

        self.at("base pair site")
        t0 = tri(1.8, 2.9, YELLOW, 0.5)
        t0l = lab("loxP site: 34 base pairs", 28, YELLOW).next_to(t0, RIGHT, buff=0.25)
        self.play(FadeIn(t0, scale=0.6), FadeIn(t0l), run_time=0.6)

        self.at("A floxed gene")
        line = dna(-6.2, 6.2, 0.3)
        left = block(-4.1, 0.3, 3.4, 1.1, GREEN, "gene", 28)
        piece = block(0.0, 0.3, 3.8, 1.1, GREEN, "piece of the gene", 28)
        right = block(4.1, 0.3, 3.4, 1.1, GREEN, "gene", 28)
        t1, t2 = tri(-2.15, 0.3, YELLOW, 0.42), tri(2.15, 0.3, YELLOW, 0.42)
        l1, l2 = lab("loxP", 26, YELLOW).move_to(at(-2.15, -0.55)), lab("loxP", 26, YELLOW).move_to(at(2.15, -0.55))
        flab = lab("floxed gene", 34, TEXT).move_to(at(0, 1.55))
        self.play(Create(line), FadeIn(left), FadeIn(piece), FadeIn(right), run_time=0.8)
        self.play(FadeIn(t1), FadeIn(t2), FadeIn(l1), FadeIn(l2), FadeIn(flab), run_time=0.7)

        self.at("works normally")
        ok = chip("gene works normally", GREEN, 30).move_to(at(0, -2.4))
        okA = arr(at(0, -0.4), at(0, -1.85), GREEN, 4, 0.18)
        self.play(GrowArrow(okA), FadeIn(ok), run_time=0.6)

        self.at("point the same way")
        same = lab("both point the same way", 28, YELLOW).move_to(at(0, -1.35))
        self.play(FadeOut(ok), FadeOut(okA), Indicate(t1, color=YELLOW, scale_factor=1.4),
                  Indicate(t2, color=YELLOW, scale_factor=1.4), FadeIn(same), run_time=0.9)

        self.at("cuts out the")
        cre2 = cre_chip(0, 2.7, 34)
        self.play(FadeOut(t0), FadeOut(t0l), FadeOut(virus), FadeOut(flab), ReplacementTransform(cre, cre2), run_time=0.6)
        gone = lab("deleted", 30, RED).move_to(at(3.4, 2.7))
        self.play(FadeOut(same), FadeOut(l1), FadeOut(l2), FadeOut(t1), FadeOut(t2),
                  piece.animate.shift(UP * 2.0).set_opacity(0.45),
                  FadeOut(cre2), FadeIn(gone), run_time=1.0)
        self.play(left.animate.shift(RIGHT * 2.3), right.animate.shift(LEFT * 2.3), run_time=0.7)
        self.play(red(left[0]), red(right[0]), FadeOut(left[2]), FadeOut(right[2]), run_time=0.5)
        ko = lab("the gene is knocked out", 32, RED).move_to(at(0, -1.5))
        self.play(FadeIn(ko, shift=UP * 0.1), run_time=0.5)
        self.finish()


# ---------------------------------------------------------------------------------------------
class S03Cross(SpokenScene):
    """conditional knockout by crossing; lox-stop-lox reporter; glow marks Cre action."""

    def construct(self):
        # --- A: the cross ---
        self.at("Cross a floxed mouse")
        fm = chip("floxed mouse", GREEN, 32).move_to(at(-3.6, 3.0))
        cm = chip("Cre mouse", BLUE, 32).move_to(at(3.6, 3.0))
        times = T("×", 48, TEXT).move_to(at(0, 3.0))
        self.play(FadeIn(fm, shift=RIGHT * 0.2), FadeIn(times), FadeIn(cm, shift=LEFT * 0.2), run_time=0.7)
        self.at("from a promoter")
        pr = lines("Cre made from a promoter", "active in one cell type", size=26, color=BLUE, align=ORIGIN).move_to(at(3.6, 2.0))
        self.play(FadeIn(pr), run_time=0.5)
        kw = dict(w=3.9, h=2.8, cr=0.34)
        P = [tissue("tissue A", -4.4, -0.55, **kw), tissue("tissue B", 0.0, -0.55, **kw),
             tissue("tissue C", 4.4, -0.55, **kw)]
        down = arr(at(0, 2.5), at(0, 1.0), GREY, 4)
        self.play(GrowArrow(down), *[FadeIn(p) for p in P], run_time=0.8)

        self.at("Only those cells")
        dots = VGroup(*[Dot(c.get_center(), radius=0.12, color=BLUE) for c in P[1].cells])
        dl = lab("blue dot: Cre-making cell", 24, BLUE).move_to(at(0, -2.62))
        self.play(FadeIn(dots, scale=0.5), FadeIn(dl), run_time=0.5)
        self.at("lose the gene")
        self.play(*[red(c) for c in P[1].cells], run_time=0.7)
        self.at("conditional knockout")
        cko = chip("conditional knockout", TEXT, 32).move_to(at(0, -3.2))
        self.play(FadeIn(cko, shift=UP * 0.15), run_time=0.5)

        # --- B: lox-stop-lox reporter ---
        self.at("A second design")
        cleanup = VGroup(fm, cm, times, pr, down, *P, dots, cko, dl)
        self.play(FadeOut(cleanup), run_time=0.5)
        y = 2.0
        line = dna(-5.6, 5.4, y)
        a1, a2 = tri(-4.5, y, YELLOW, 0.46), tri(-1.6, y, YELLOW, 0.46)
        stop = block(-3.05, y, 2.1, 0.95, ORANGE, "stop", 30)
        rep = block(1.8, y, 4.4, 1.05, GREY, "reporter gene", 30, op=0.12)
        l1, l2 = lab("loxP", 26, YELLOW).move_to(at(-4.5, y - 0.75)), lab("loxP", 26, YELLOW).move_to(at(-1.6, y - 0.75))
        self.play(Create(line), FadeIn(a1), FadeIn(a2), FadeIn(l1), FadeIn(l2), FadeIn(stop), run_time=0.7)
        self.at("in front of a reporter gene")
        self.play(FadeIn(rep), run_time=0.5)
        ccell = cell(0, -0.4, 0.95, GREY, 0.12)
        self.play(FadeIn(ccell), run_time=0.4)

        self.at("cuts the stop out")
        cre = cre_chip(-3.05, 3.5, 34)
        self.play(FadeIn(cre, shift=DOWN * 0.1), run_time=0.4)
        self.play(cre.animate.move_to(at(-3.05, 3.1)), run_time=0.4)
        self.play(stop.animate.set_opacity(0.0), run_time=0.3)
        self.play(rep[0].animate.set_stroke(GREEN).set_fill(GREEN, 0.35), rep[2].animate.set_color(GREEN),
                  ccell.animate.set_stroke(GREEN, 4).set_fill(GREEN, 0.5), run_time=0.7)
        self.play(FadeOut(cre), run_time=0.3)

        self.at("all its descendants")
        xs = [-4.5, -1.5, 1.5, 4.5]
        kids = [cell(x, -2.7, 0.6, GREEN, 0.5, 4) for x in xs]
        ls = [Line(ccell.get_bottom(), k.get_top(), color=GREY, stroke_width=3) for k in kids]
        self.play(*[Create(l) for l in ls], run_time=0.5)
        self.play(*[FadeIn(k, scale=0.5) for k in kids], run_time=0.6)

        self.at("A glowing cell")
        gl = lab("glow: Cre acted here", 30, GREEN).move_to(at(4.0, -0.4))
        self.play(FadeIn(gl, shift=LEFT * 0.15), run_time=0.5)
        self.finish()


# ---------------------------------------------------------------------------------------------
class S04Timing(SpokenScene):
    """CreER held out of the nucleus until tamoxifen; then Flp-FRT and GAL4 in one line each."""

    def construct(self):
        body = Ellipse(width=10.6, height=4.8, stroke_color=GREY, stroke_width=3, fill_color=GREY,
                       fill_opacity=0.08).move_to(at(0, 0.5))
        nuc = Circle(radius=1.75, stroke_color=GREY, stroke_width=3, fill_color=GREY,
                     fill_opacity=0.14).move_to(at(2.9, 0.5))
        nlab = lab("nucleus", 26, GREY).move_to(at(2.9, -0.85))
        fl = block(2.9, -0.1, 2.0, 0.55, GREEN, "")
        ft1, ft2 = tri(1.7, -0.1, YELLOW, 0.32), tri(4.1, -0.1, YELLOW, 0.32)

        self.at("For timing")
        self.play(FadeIn(body), FadeIn(nuc), FadeIn(nlab), FadeIn(fl), FadeIn(ft1), FadeIn(ft2), run_time=0.8)

        self.at("to a modified")
        cre = chip("Cre", BLUE, 30).move_to(at(-3.3, 1.2))
        er = chip("ER", PURPLE, 30)
        self.play(FadeIn(cre, shift=RIGHT * 0.2), run_time=0.4)
        er.move_to(cre.get_right() + RIGHT * 1.0)
        self.play(FadeIn(er), er.animate.next_to(cre, RIGHT, buff=0.0), run_time=0.6)
        erl = lab("modified estrogen receptor", 26, PURPLE).move_to(at(-2.3, 0.5))
        self.play(FadeIn(erl), run_time=0.4)
        creer = VGroup(cre, er)

        self.at("stays out of the nucleus")
        blk = DashedLine(at(-1.4, 1.2), at(0.7, 1.2), color=GREY, stroke_width=4)
        x = cross_out(Square(0.45).move_to(at(0.95, 1.2)))
        self.play(Create(blk), FadeIn(x), run_time=0.6)

        self.at("until tamoxifen is given")
        tam = chip("tamoxifen", TEAL, 30).move_to(at(-4.8, -1.1))
        self.play(FadeOut(erl), FadeOut(blk), FadeOut(x), FadeIn(tam, shift=RIGHT * 0.2), run_time=0.3)
        self.play(tam.animate.move_to(at(-2.8, 0.0)), run_time=0.4)
        grp = VGroup(creer, tam)
        self.play(grp.animate.scale(0.8).move_to(at(2.9, 1.1)), run_time=0.5)
        self.play(fl[0].animate.set_stroke(RED).set_fill(RED, 0.3),
                  FadeOut(ft1), FadeOut(ft2), run_time=0.3)

        # --- other systems ---
        self.at("Flip, from yeast", lead=0.9)
        old = VGroup(body, nuc, nlab, fl, grp)
        self.play(FadeOut(old), run_time=0.5)
        # row 1: Flp
        y1 = 1.7
        flp = chip("Flp", BLUE, 32).move_to(at(-3.4, 3.0))
        flpl = lab("from yeast", 26, GREY).next_to(flp, LEFT, buff=0.3)
        ldna = dna(-6.0, -0.8, y1)
        sq = lambda x: Square(0.4, stroke_color=YELLOW, stroke_width=2.5, fill_color=YELLOW, fill_opacity=0.9).move_to(at(x, y1))
        fr1, fr2 = sq(-5.2), sq(-1.6)
        fb = block(-3.4, y1, 2.2, 0.6, GREEN, "")
        frl = lab("its own FRT sites", 26, YELLOW).move_to(at(-3.4, y1 - 0.8))
        self.play(FadeIn(flp), FadeIn(flpl), run_time=0.4)
        self.play(Create(ldna), FadeIn(fb), FadeIn(fr1), FadeIn(fr2), FadeIn(frl), run_time=0.4)
        self.play(flp.animate.move_to(at(-3.4, y1 + 0.95)), fb.animate.shift(UP * 0.5).set_opacity(0.0), run_time=0.5)
        self.at("does not recognize")
        l_dna = dna(0.8, 6.0, y1)
        lt1, lt2 = tri(1.6, y1, YELLOW, 0.46), tri(5.2, y1, YELLOW, 0.46)
        lb = block(3.4, y1, 2.2, 0.6, GREEN, "")
        ll = lab("loxP sites", 26, YELLOW).move_to(at(3.4, y1 - 0.8))
        flp2 = chip("Flp", BLUE, 32).move_to(at(3.4, y1 + 0.95))
        xx = cross_out(flp2)
        self.play(Create(l_dna), FadeIn(lb), FadeIn(lt1), FadeIn(lt2), FadeIn(ll), FadeIn(flp2), FadeIn(xx), run_time=0.5)

        # row 2: GAL4
        y2 = -1.5
        self.at("In flies")
        enh = chip("enhancer", GREY, 26).move_to(at(-5.0, y2))
        g4 = chip("GAL4", PINK, 32).move_to(at(-2.4, y2))
        a1 = arr(enh.get_right(), g4.get_left(), GREY, 4, 0.18)
        self.play(FadeIn(enh), GrowArrow(a1), FadeIn(g4), run_time=0.7)
        self.at("a yeast activator")
        yl = lab("a yeast activator", 26, PINK).move_to(at(-2.4, y2 - 0.9))
        self.play(FadeIn(yl), run_time=0.5)
        self.at("switches on")
        sqp = lambda x: Square(0.36, stroke_color=PINK, stroke_width=2.5, fill_color=PINK, fill_opacity=0.8).move_to(at(x, y2))
        s1, s2 = sqp(1.0), sqp(1.5)
        tg = block(3.9, y2, 3.0, 0.75, GREEN, "target gene", 28)
        tl2 = dna(0.6, 5.7, y2)
        a2 = arr(g4.get_right() + RIGHT * 0.1, at(0.5, y2), PINK, 4, 0.18)
        sl = lab("GAL4 binding sites in the promoter", 26, PINK).move_to(at(2.6, y2 + 0.75))
        tg[0].set_fill(GREEN, 0.08)
        self.play(Create(tl2), FadeIn(s1), FadeIn(s2), FadeIn(sl), FadeIn(tg), run_time=0.6)
        self.play(GrowArrow(a2), tg[0].animate.set_fill(GREEN, 0.6), run_time=0.6)
        self.finish()


# ---------------------------------------------------------------------------------------------
class S05Reading(SpokenScene):
    """real data: Luo et al. 2020, Clstn3 f/f x Dlx5/6-Cre, parental sex of the Cre carrier."""

    def construct(self):
        W = 5.4
        LX, RX = -3.3, 3.3

        self.at("A real result")
        gold = lab("Luo and colleagues, 2020", 32, GOLD).move_to(at(0, 3.1))
        cx = chip("Clstn3 f/f  ×  Dlx5/6-Cre", TEXT, 34).move_to(at(0, 2.0))
        self.play(FadeIn(gold), run_time=0.5)
        self.at("Floxed")
        self.play(FadeIn(cx, shift=UP * 0.1), cx.animate.scale(1.4).move_to(at(0, 1.7)), run_time=0.8)
        self.at("crossed with")
        pre = bar(0, 0.2, 7.0, 0, 10, 1.0)
        pre[0].set_opacity(0)
        prel = lab("offspring", 32, GREY).move_to(at(0, -0.6))
        self.play(FadeIn(pre), FadeIn(prel), run_time=0.6)

        self.at("should inherit only")
        exp = bar(0, 0.2, 7.0, 0, 10, 1.0)
        expl = lab("expected: only the floxed allele (f/f)", 32, GREEN).move_to(at(0, -0.6))
        self.play(FadeOut(pre), FadeOut(prel), FadeIn(exp), FadeIn(expl), run_time=0.7)

        self.at("When the mother carried")
        hl = chip("mother carries Cre", BLUE, 30).move_to(at(LX, 1.0))
        self.play(FadeOut(exp), FadeOut(expl), FadeOut(cx), FadeIn(hl), run_time=0.5)
        b1 = bar(LX, -0.3, W, 0, 10, 1.0)
        self.play(FadeIn(b1), run_time=0.3)
        self.at("offspring had a knockout")
        b1n = bar(LX, -0.3, W, 73, 83, 1.0)
        l1 = lab("73 of 83 have a knockout allele", 28, RED).move_to(at(LX, -1.2))
        self.play(ReplacementTransform(b1, b1n), FadeIn(l1), run_time=0.8)

        self.at("When the father carried")
        hr = chip("father carries Cre", BLUE, 30).move_to(at(RX, 1.0))
        b2 = bar(RX, -0.3, W, 0, 114, 1.0)
        self.play(FadeIn(hr), FadeIn(b2), run_time=0.6)
        self.at("none of")
        l2 = lab("0 of 114 have one", 28, GREEN).move_to(at(RX, -1.2))
        self.play(FadeIn(l2), run_time=0.5)

        leg1 = VGroup(Square(0.3, stroke_width=0, fill_color=RED, fill_opacity=0.75), lab("knockout allele", 26, TEXT))
        leg1.arrange(RIGHT, buff=0.15)
        leg2 = VGroup(Square(0.3, stroke_width=0, fill_color=GREEN, fill_opacity=0.75), lab("floxed only", 26, TEXT))
        leg2.arrange(RIGHT, buff=0.15)
        legend = VGroup(leg1, leg2).arrange(RIGHT, buff=0.8).move_to(at(0, -2.0))
        self.play(FadeIn(legend), run_time=0.4)

        self.at("Look only at offspring")
        sub = lab("only offspring that carry no Cre", 32, GOLD).move_to(at(0, 2.0))
        self.play(FadeOut(b1n), FadeOut(l1), FadeOut(b2), FadeOut(l2), FadeOut(hr), FadeOut(legend), FadeIn(sub),
                  ReplacementTransform(hl, chip("offspring of Cre mothers", BLUE, 30).move_to(at(0, 1.0))), run_time=0.6)
        self.at("29 of 34")
        b3 = bar(0, -0.3, 7.0, 29, 34, 1.0)
        l3 = lab("29 of 34 have one floxed and one deleted copy", 30, RED).move_to(at(0, -1.2))
        self.play(FadeIn(b3), FadeIn(l3), run_time=0.7)

        self.at("A deleted allele in an animal")
        c1 = chip("deleted allele, no Cre in this animal", RED, 28).move_to(at(-3.0, -2.5))
        self.play(FadeIn(c1, shift=UP * 0.1), run_time=0.5)
        self.at("cannot be")
        nc = lab("not Cre acting in it", 28, BLUE).move_to(at(-3.0, -3.2))
        self.play(FadeIn(nc), run_time=0.4)
        self.at("points to the")
        c2 = chip("points to the germline", GOLD, 28).move_to(at(3.7, -2.5))
        aa = arr(c1.get_right() + RIGHT * 0.1, c2.get_left() + LEFT * 0.1, GOLD, 4, 0.18)
        self.play(GrowArrow(aa), FadeIn(c2), run_time=0.6)
        self.finish()


# ---------------------------------------------------------------------------------------------
class S06Pitfalls(SpokenScene):
    """left: reporter is not deletion (control: measure target); right: germline recombination."""

    def construct(self):
        LX, RX = -3.4, 3.4
        div = Line(at(0, 3.3), at(0, -3.3), color=GREY, stroke_width=2).set_opacity(0.5)
        self.add(div)

        self.at("First, a reporter")
        h1 = chip("1  A reporter is not a deletion", RED, 26).move_to(at(LX, 3.1))
        c = cell(LX, 0.45, 1.3, GREEN, 0.45, 4)
        glow = ring(c.get_center(), 1.55)
        rl = lab("reporter glows", 26, GREEN).move_to(at(LX, 2.3))
        self.play(FadeIn(h1), FadeIn(c), FadeIn(glow), FadeIn(rl), run_time=0.8)

        self.at("A glowing cell may")
        g1 = block(LX, 0.7, 1.7, 0.5, GREEN, "", op=0.4)
        t1, t2 = tri(LX - 1.05, 0.7, YELLOW, 0.3), tri(LX + 1.05, 0.7, YELLOW, 0.3)
        gl = lab("floxed gene", 24, GREEN).move_to(at(LX, 0.05))
        self.play(FadeIn(g1), FadeIn(t1), FadeIn(t2), FadeIn(gl), run_time=0.6)
        self.at("still carry the gene")
        still = lab("may still carry the gene", 28, RED).move_to(at(LX, -1.4))
        self.play(FadeIn(still, shift=UP * 0.1), run_time=0.5)

        self.at("measure the target protein")
        ctl = lines("control: measure the target", "protein or DNA in reporter-positive", "cells in the same animals",
                    size=26, color=GOLD, align=ORIGIN).move_to(at(LX, -2.6))
        self.play(FadeIn(ctl, shift=UP * 0.1), run_time=0.7)

        self.at("Second, germline recombination")
        h2 = chip("2  Germline recombination", RED, 26).move_to(at(RX, 3.1))
        self.play(FadeIn(h2), run_time=0.5)
        self.at("over half of 64")
        st = lines("over half of 64 commonly", "used nervous-system Cre lines", size=28, color=RED,
                   align=ORIGIN).move_to(at(RX, 1.9))
        self.play(FadeIn(st, shift=UP * 0.1), run_time=0.7)
        pa = chip("Cre parent", BLUE, 26).move_to(at(RX, 0.6))
        pu = chip("pup: no Cre, deleted allele", RED, 26).move_to(at(RX, -0.6))
        aar = arr(at(RX, 0.25), at(RX, -0.2), GREY, 4, 0.15)
        self.play(FadeIn(pa), GrowArrow(aar), FadeIn(pu), run_time=0.7)

        self.at("Genotype every animal")
        k1 = lab("genotype every animal", 28, GOLD).move_to(at(RX, -1.8))
        self.play(FadeIn(k1, shift=UP * 0.1), run_time=0.4)
        self.at("check animals without")
        k2 = lab("check animals without Cre", 28, GOLD).move_to(at(RX, -2.6))
        self.play(FadeIn(k2, shift=UP * 0.1), run_time=0.4)
        self.finish()


# ---------------------------------------------------------------------------------------------
class S07Unlocked(SpokenScene):
    """Guy 2007 (Mecp2 reversal); Fuenfschilling 2012 (Cox10 in oligodendrocytes and Schwann cells)."""

    def construct(self):
        self.at("In 2007")
        tag2 = lab("Guy, Bird and colleagues, 2007", 32, GOLD).move_to(at(0, 3.1))
        y = 1.4
        line = dna(-5.8, 5.8, y)
        a1, a2 = tri(-4.8, y, YELLOW, 0.5), tri(-1.6, y, YELLOW, 0.5)
        stop = block(-3.2, y, 2.2, 1.0, ORANGE, "stop", 30)
        gene = block(2.8, y, 4.6, 1.1, GREY, "Mecp2 gene", 30, op=0.12)
        self.play(FadeIn(tag2), Create(line), FadeIn(a1), FadeIn(a2), FadeIn(stop), FadeIn(gene), run_time=0.7)
        self.at("silenced the gene")
        sil = lab("gene silenced", 30, RED).move_to(at(2.8, 2.5))
        self.play(FadeIn(sil), run_time=0.4)
        self.at("removable")
        lbl = lab("lox-stop cassette", 28, ORANGE).move_to(at(-3.2, 2.5))
        self.play(FadeIn(lbl), run_time=0.4)
        self.at("restored it with")
        cre = chip("Cre", BLUE, 30).move_to(at(-2.4, 2.45))
        tam = chip("tamoxifen", TEAL, 30).move_to(at(-5.6, 2.45))
        self.play(FadeOut(lbl), FadeIn(cre, shift=DOWN * 0.1), FadeIn(tam, shift=RIGHT * 0.2), run_time=0.5)
        self.play(tam.animate.move_to(at(-4.0, 2.45)), run_time=0.5)
        self.play(stop.animate.set_opacity(0.0), FadeOut(sil), run_time=0.5)
        self.play(FadeOut(cre), FadeOut(tam), run_time=0.3)
        rest = lab("gene restored", 30, GREEN).move_to(at(2.8, 2.5))
        self.play(gene[0].animate.set_stroke(GREEN).set_fill(GREEN, 0.4), gene[2].animate.set_color(GREEN),
                  FadeIn(rest), run_time=0.7)
        self.at("Advanced symptoms reversed")
        sy1 = chip("advanced symptoms", RED, 30).move_to(at(-3.0, -0.6))
        sy2 = chip("reversed", GREEN, 30).move_to(at(3.0, -0.6))
        sa = arr(sy1.get_right() + RIGHT * 0.1, sy2.get_left() + LEFT * 0.1, GREEN, 5)
        who = lab("in young and mature adult mice", 30, TEXT).move_to(at(0, -1.8))
        self.play(FadeIn(sy1, shift=UP * 0.1), run_time=0.4)
        self.play(GrowArrow(sa), FadeIn(sy2), FadeIn(who), run_time=0.7)

        self.at("In 2012")
        self.play(*[FadeOut(m) for m in (tag2, line, a1, a2, stop, gene, rest, sy1, sy2, sa, who)], run_time=0.5)
        tag = lab("Fünfschilling, Nave and colleagues, 2012", 32, GOLD).move_to(at(0, 3.1))
        og = cell(-3.6, 0.6, 1.1, GREY, 0.18)
        ol = lab("oligodendrocyte", 28, GREY).move_to(at(-3.6, -0.9))
        sc = cell(3.6, 0.6, 1.1, GREY, 0.18)
        sl = lab("Schwann cell", 28, GREY).move_to(at(3.6, -0.9))
        self.play(FadeIn(tag), FadeIn(og), FadeIn(ol), FadeIn(sc), FadeIn(sl), run_time=0.7)
        self.at("deleted")
        cx = chip("Cox10 deleted", RED, 32).move_to(at(0, 0.6))
        self.play(FadeIn(cx), red(og), red(sc), run_time=1.8)
        self.at("Conditional deletion was needed")
        need = lab("respiration removed only in glial cells", 32, TEXT).move_to(at(0, -2.4))
        self.play(FadeIn(need, shift=UP * 0.1), run_time=0.6)
        self.finish()


# ---------------------------------------------------------------------------------------------
class S08Rule(SpokenScene):
    """Orefice 2016: deletion and rescue in peripheral touch neurons; then the rule."""

    def construct(self):
        self.at("In 2016")
        tag = lab("Orefice, Ginty and colleagues, 2016", 32, GOLD).move_to(at(0, 3.2))
        X = -3.5
        skin = RoundedRectangle(corner_radius=0.1, width=5.0, height=0.55, stroke_color=GREY, stroke_width=2.5,
                                fill_color=GREY, fill_opacity=0.2).move_to(at(X, -2.6))
        skl = lab("skin", 26, GREY).move_to(at(X, -2.6))
        nrn = cell(X, -0.4, 0.6, GREEN, 0.35)
        fib = Line(at(X, -2.3), at(X, -1.0), color=GREEN, stroke_width=5)
        brain = Ellipse(width=2.8, height=1.7, stroke_color=GREY, stroke_width=3, fill_color=GREY,
                        fill_opacity=0.12).move_to(at(X, 1.8))
        brl = lab("brain", 26, GREY).move_to(brain)
        cord = Line(at(X, 0.2), at(X, 0.95), color=GREEN, stroke_width=5)
        nl = lab("somatosensory neuron", 26, GREEN).next_to(nrn, RIGHT, buff=0.3)
        self.play(FadeIn(tag), FadeIn(skin), FadeIn(skl), Create(fib), FadeIn(nrn), Create(cord), FadeIn(brain),
                  FadeIn(brl), run_time=0.9)
        self.at("deleted")
        self.play(red(nrn), run_time=0.5)
        self.at("peripheral somatosensory neurons")
        self.play(FadeIn(nl), run_time=0.4)
        self.at("tactile dysfunction")
        td = chip("tactile dysfunction", RED, 30).move_to(at(3.2, 1.8))
        self.play(FadeIn(td, shift=LEFT * 0.15), run_time=0.5)
        self.at("Restoring")
        self.play(green(nrn), FadeOut(td), FadeOut(nl), run_time=0.6)
        rs = lab("gene restored only in these neurons", 28, GREEN).move_to(at(2.7, 2.5))
        self.play(FadeIn(rs), run_time=0.4)
        self.at("rescued tactile sensitivity")
        r1 = chip("tactile sensitivity: rescued", GREEN, 30).move_to(at(3.2, 0.9))
        self.play(FadeIn(r1, shift=LEFT * 0.15), run_time=0.5)
        self.at("but not lethality")
        r2 = chip("lethality: not rescued", RED, 30).move_to(at(3.2, -0.3))
        self.play(FadeIn(r2, shift=LEFT * 0.15), run_time=0.5)

        self.at("Keep this rule")
        self.play(*[FadeOut(m) for m in (tag, skin, skl, nrn, fib, brain, brl, cord, rs, r1, r2)], run_time=0.6)
        self.at("A reporter shows")
        c = cell(-3.3, 0.5, 1.4, GREEN, 0.5, 4)
        glow = ring(c.get_center(), 1.7)
        gl = lab("reporter glows: Cre acted", 30, GREEN).move_to(at(-3.3, 2.7))
        g1 = block(3.3, 0.5, 2.6, 0.8, GREEN, "floxed gene", 28, op=0.4)
        ta, tb = tri(1.8, 0.5, YELLOW, 0.34), tri(4.8, 0.5, YELLOW, 0.34)
        il = lab("gene still intact?", 30, GOLD).move_to(at(3.3, 1.7))
        self.play(FadeIn(c), FadeIn(glow), FadeIn(gl), run_time=0.6)
        self.play(FadeIn(g1), FadeIn(ta), FadeIn(tb), FadeIn(il), run_time=0.6)
        self.at("not that your gene")
        gone = chip("a glow does not show the gene is gone", RED, 30).move_to(at(0, -1.9))
        self.play(FadeIn(gone, shift=UP * 0.1), run_time=0.6)
        self.finish()


# ---------------------------------------------------------------------------------------------
class S09End(EndCard):
    LINE = "A reporter shows where Cre acted, not that your gene is gone."
