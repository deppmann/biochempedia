"""Gene targeting: deleting one gene in a whole mouse  (Biochemistrypedia methods film)

Timed to the SPOKEN words: every self.at("...") cue waits for that phrase in audio/words.json.

COLOR MAP (one color per concept, whole video)
  TEAL   = the cell's own gene and chromosome DNA
  BLUE   = engineered DNA: the targeting vector, the knocked-out or knocked-in allele
  ORANGE = the neo marker (neomycin resistance)
  PURPLE = the tk marker (thymidine kinase)
  AGOUTI = embryonic stem cells and everything that comes from them (brown, the agouti coat)
  GREY   = host strain, structure, labels (the black host mouse is drawn dark with a white outline)
  YELLOW = neurons, the readout, a highlighted step
  GREEN  = survives, correct result, a control
  RED    = dies, wrong, the pitfall
  GOLD   = dates, source tags and the closing rule
"""
import numpy as np
from bp_style import *  # noqa: F401,F403

PURPLE = "#B58CD9"
ORANGE = "#F29E4C"
AGOUTI = "#C98F45"
HOSTFILL = "#232733"
NEUTRAL = "#3A3F4D"


# ---------------------------------------------------------------------------------------------
# helpers
# ---------------------------------------------------------------------------------------------
def lab(text, size=24, color=GREY, **kw):
    return T(text, size, color, **kw)


def arr(a, b, color=GREY, w=5, tip=0.2):
    return Arrow([a[0], a[1], 0], [b[0], b[1], 0], buff=0.0, color=color, stroke_width=w, tip_length=tip,
                 max_tip_length_to_length_ratio=0.45, max_stroke_width_to_length_ratio=12)


def poly(pts, color=YELLOW, w=5):
    m = VMobject()
    m.set_points_as_corners([np.array([p[0], p[1], 0.0]) for p in pts])
    m.set_stroke(color, w)
    return m


def blk(x0, x1, y, color, h=0.34, op=0.6):
    return Rectangle(width=x1 - x0, height=h, stroke_color=color, stroke_width=2.5, fill_color=color,
                     fill_opacity=op).move_to([(x0 + x1) / 2, y, 0])


def xmark(x, y, size=36, color=RED):
    return T("✕", size, color, weight=BOLD).move_to([x, y, 0])


def tick(x, y, size=36, color=GREEN):
    return T("✓", size, color, weight=BOLD).move_to([x, y, 0])


def tag(text, x, y, size=22):
    return T(text, size, GOLD).move_to([x, y, 0])


def mouse(scale=1.0, fill=HOSTFILL, patches=(), eye=TEXT):
    """Side-on mouse made of ellipses. patches: (cx, cy, w, h) agouti patches on the coat."""
    st = dict(stroke_color=TEXT, stroke_width=2.5, fill_color=fill, fill_opacity=1)
    body = Ellipse(width=2.0, height=1.1, **st)
    head = Ellipse(width=0.95, height=0.8, **st).move_to([1.05, 0.12, 0])
    ear = Circle(radius=0.2, **st).move_to([0.8, 0.6, 0])
    tail = ArcBetweenPoints([-0.95, -0.05, 0], [-1.95, 0.5, 0], angle=1.0, stroke_color=TEXT, stroke_width=3)
    ps = [Ellipse(width=w, height=h, stroke_width=0, fill_color=AGOUTI, fill_opacity=1).move_to([cx, cy, 0])
          for (cx, cy, w, h) in patches]
    e = Dot(radius=0.055, color=eye).move_to([1.28, 0.22, 0])
    nose = Dot(radius=0.06, color=TEXT).move_to([1.5, 0.1, 0])
    return VGroup(tail, body, *ps, head, ear, e, nose).scale(scale)


def coat_mouse(kind, scale=1.0):
    if kind == "agouti":
        return mouse(scale, fill=AGOUTI, eye=BG)
    if kind == "black":
        return mouse(scale, fill=HOSTFILL)
    if kind == "chimera":
        return mouse(scale, fill=HOSTFILL,
                     patches=[(-0.35, 0.18, 0.75, 0.45), (0.45, -0.22, 0.6, 0.4), (-0.55, -0.25, 0.4, 0.3),
                              (0.25, 0.3, 0.35, 0.25)])
    return mouse(scale, fill=NEUTRAL)


def chip2(texts, color=BLUE, size=22, pad=0.16, buff=0.06):
    """A rounded box around two or more stacked lines of text."""
    ls = VGroup(*[T(t, size, color) for t in texts]).arrange(DOWN, buff=buff)
    box = RoundedRectangle(corner_radius=0.14, width=ls.width + 2 * pad, height=ls.height + 2 * pad,
                           stroke_color=color, stroke_width=2.5, fill_color=color, fill_opacity=0.16)
    return VGroup(box, ls.move_to(box))


def cell(x, y, r=0.85, color=AGOUTI, op=0.35):
    return Circle(radius=r, stroke_color=color, stroke_width=3, fill_color=color, fill_opacity=op).move_to([x, y, 0])


# ---------------------------------------------------------------------------------------------
class S00Title(TitleCard):
    LESSON = "Methods library"
    TITLE = "Deleting One Gene in a Whole Mouse"


# ---------------------------------------------------------------------------------------------
class S01Problem(SpokenScene):
    """The question: what does one gene do in a whole animal? A dish cannot show it; DNA added at random cannot choose."""

    def construct(self):
        # --- act 1: the dish cannot show whole-animal functions
        dish = RoundedRectangle(corner_radius=0.3, width=5.2, height=3.0, stroke_color=GREY, stroke_width=3,
                                fill_color=GREY, fill_opacity=0.08).move_to([-3.4, 1.3, 0])
        rng = np.random.RandomState(4)
        cells = VGroup(*[Circle(radius=0.3, stroke_color=GREY, stroke_width=2, fill_color=GREY, fill_opacity=0.3)
                         .move_to([-3.4 + (i % 4 - 1.5) * 1.05 + rng.randn() * 0.06,
                                   1.3 + (i // 4 - 0.5) * 1.05 + rng.randn() * 0.06, 0]) for i in range(8)])
        dish_lbl = lab("cells in a dish", 30, GREY).move_to([-3.4, -0.6, 0])
        m = coat_mouse("neutral", 1.5).move_to([3.4, 1.4, 0])
        m_lbl = lab("a whole mouse", 30, GREY).move_to([3.4, -0.5, 0])
        c1 = chip("blood pressure", YELLOW, 30).move_to([3.4, -1.5, 0])
        c2 = chip("nervous-system wiring", YELLOW, 30).move_to([3.4, -2.6, 0])

        self.at("Cell culture")
        self.play(FadeIn(dish), FadeIn(cells), FadeIn(dish_lbl), run_time=0.6)
        self.at("blood pressure")
        self.play(FadeIn(m), FadeIn(m_lbl), FadeIn(c1, shift=UP * 0.1), run_time=0.5)
        self.at("wiring")
        self.play(FadeIn(c2, shift=UP * 0.1), run_time=0.4)
        big = xmark(-3.4, 1.3, 130, RED)
        self.play(FadeIn(big, scale=1.5), run_time=0.4)

        # --- act 2: before gene targeting, DNA could be added but not aimed
        self.at("Before gene targeting")
        self.play(*[FadeOut(o) for o in (dish, cells, dish_lbl, m, m_lbl, c1, c2, big)], run_time=0.5)
        xs = np.linspace(-5.1, 5.1, 9)
        genes = VGroup(*[blk(x - 0.4, x + 0.4, -0.2, TEAL, h=0.7, op=0.55) for x in xs])
        chrom = Line([-6.1, -0.2, 0], [6.1, -0.2, 0], color=TEAL, stroke_width=4)
        chrom_lbl = lab("genes along a chromosome", 26, TEAL).move_to([0, -2.2, 0])
        self.play(FadeIn(chrom), FadeIn(genes), FadeIn(chrom_lbl), run_time=0.6)
        self.at("add DNA at random")
        drops = VGroup()
        for x in (-4.6, -1.3, 2.0, 4.9):
            d = VGroup(blk(x - 0.3, x + 0.3, 2.0, BLUE, h=0.3, op=0.8), arr([x, 1.7], [x, 0.4], BLUE, 4, 0.18))
            drops.add(d)
        dna_lbl = lab("DNA added anywhere", 30, BLUE).move_to([0, 3.0, 0])
        self.play(FadeIn(dna_lbl), LaggedStart(*[FadeIn(d, shift=DOWN * 0.4) for d in drops], lag_ratio=0.25), run_time=1.2)
        self.at("choose which gene")
        ret = VGroup(Circle(radius=0.62, stroke_color=YELLOW, stroke_width=4),
                     Line([-0.9, 0, 0], [0.9, 0, 0], color=YELLOW, stroke_width=3),
                     Line([0, -0.9, 0], [0, 0.9, 0], color=YELLOW, stroke_width=3)).move_to([xs[4], -0.2, 0])
        self.play(FadeOut(drops), FadeOut(dna_lbl), Create(ret), run_time=0.6)
        ch_lbl = lab("choose this gene?", 30, YELLOW).move_to([0, 1.5, 0])
        self.play(FadeIn(ch_lbl), FadeIn(xmark(xs[4], 0.0, 110, RED)), run_time=0.5)

        # --- act 3: the question
        self.at("So how do you test")
        self.play(*[FadeOut(o) for o in self.mobjects], run_time=0.5)
        g = chip("one gene", TEAL, 36).move_to([-4.2, 0.6, 0])
        q = T("?", 64, YELLOW, weight=BOLD).next_to(g, UP, buff=0.15)
        m2 = coat_mouse("neutral", 1.5).move_to([3.0, 0.6, 0])
        a = arr([-2.4, 0.6], [0.0, 0.6], GREY, 6, 0.28)
        self.play(FadeIn(g), FadeIn(q), run_time=0.4)
        self.play(GrowArrow(a), FadeIn(m2), run_time=0.6)
        self.at("in a whole animal")
        t = lab("what does it do in a whole animal?", 36, TEXT).move_to([0, -1.9, 0])
        self.play(FadeIn(t, shift=UP * 0.15), run_time=0.5)
        self.finish()


# ---------------------------------------------------------------------------------------------
class S02Swap(SpokenScene):
    """ES cells; a targeting vector with two homology arms, neo between and tk outside; electroporation; the swap."""

    def construct(self):
        # --- beat 1: embryo -> ES cells
        emb = Circle(radius=1.45, stroke_color=GREY, stroke_width=3, fill_color=GREY, fill_opacity=0.08).move_to([-4.0, 0.7, 0])
        icm = Ellipse(width=1.3, height=0.9, stroke_color=AGOUTI, stroke_width=2, fill_color=AGOUTI,
                      fill_opacity=0.6).move_to([-4.0, 1.25, 0])
        emb_lbl = lab("early embryo", 28, GREY).move_to([-4.0, -1.4, 0])
        dish = RoundedRectangle(corner_radius=0.3, width=5.2, height=3.0, stroke_color=GREY, stroke_width=3,
                                fill_color=GREY, fill_opacity=0.08).move_to([2.7, 0.7, 0])
        rng = np.random.RandomState(8)
        escs = VGroup(*[Circle(radius=0.3, stroke_color=AGOUTI, stroke_width=2, fill_color=AGOUTI, fill_opacity=0.5)
                        .move_to([2.7 + (i % 4 - 1.5) * 1.05 + rng.randn() * 0.05, 0.7 + (i // 4 - 0.5) * 1.0 + rng.randn() * 0.05, 0])
                        for i in range(8)])
        dish_lbl = lab("ES cells in culture", 28, AGOUTI).move_to([2.7, -1.4, 0])
        a = arr([-2.3, 0.7], [-0.1, 0.7], GREY, 6, 0.28)

        self.at("Embryonic stem cells")
        self.play(FadeIn(dish), LaggedStart(*[GrowFromCenter(e) for e in escs], lag_ratio=0.1), FadeIn(dish_lbl), run_time=0.9)
        self.at("early embryo")
        self.play(FadeIn(emb), FadeIn(icm), FadeIn(emb_lbl), run_time=0.5)
        self.play(GrowArrow(a), run_time=0.6)
        self.at("any tissue")
        tis = lab("can still contribute to any tissue", 32, TEXT).move_to([0, -2.6, 0])
        self.play(FadeIn(tis, shift=UP * 0.15), run_time=0.5)

        # --- beat 2: the gene in the ES cell, and the vector
        self.at("targeting vector")
        self.play(*[FadeOut(o) for o in (emb, icm, emb_lbl, dish, escs, dish_lbl, a, tis)], run_time=0.4)
        CY = -2.2
        cellbox = RoundedRectangle(corner_radius=0.5, width=12.2, height=3.9, stroke_color=AGOUTI, stroke_width=3,
                                   fill_color=AGOUTI, fill_opacity=0.07).move_to([0, -1.35, 0])
        cell_lbl = lab("ES cell", 26, AGOUTI).move_to([-5.3, -2.95, 0])
        old = VGroup(blk(-4.4, -2.4, CY, TEAL, op=0.45), blk(-2.4, -0.4, CY, TEAL, op=0.85), blk(-0.4, 1.6, CY, TEAL, op=0.45))
        rest = VGroup(blk(-5.6, -4.4, CY, TEAL, op=0.45), blk(1.6, 5.6, CY, TEAL, op=0.45))
        gene_lbl = lab("the gene", 24, TEAL).move_to([-1.4, -2.85, 0])
        self.play(FadeIn(cellbox), FadeIn(cell_lbl), FadeIn(old), FadeIn(rest), FadeIn(gene_lbl), run_time=0.7)

        VY = 2.3
        la = blk(-4.4, -2.4, VY, BLUE, op=0.7)
        neo = blk(-2.4, -0.4, VY, ORANGE, op=0.8)
        ra = blk(-0.4, 1.6, VY, BLUE, op=0.7)
        tk = blk(1.9, 3.1, VY, PURPLE, op=0.8)
        lal = lab("homology arm", 22, BLUE).move_to([-3.4, VY + 0.65, 0])
        ral = lab("homology arm", 22, BLUE).move_to([0.6, VY + 0.65, 0])
        neol = lab("neomycin resistance", 22, ORANGE).move_to([-1.4, VY - 0.6, 0])
        tkl = lab("thymidine kinase", 22, PURPLE).move_to([2.5, VY - 0.6, 0])
        conn = VGroup(*[DashedLine([x, VY - 0.25, 0], [x, CY + 0.25, 0], color=GREY, stroke_width=2) for x in (-3.4, 0.6)])
        match = lab("matching DNA", 22, GREY).move_to([-3.4 + 1.0, -0.3, 0]).set_opacity(0.0)

        self.at("matching the gene")
        self.play(FadeIn(la), FadeIn(ra), Create(conn), run_time=0.7)
        self.at("two homology arms")
        self.play(FadeIn(lal), FadeIn(ral), run_time=0.4)
        self.at("neomycin")
        self.play(FadeIn(neo), FadeIn(neol), run_time=0.5)
        self.at("thymidine kinase")
        self.play(FadeIn(tk), FadeIn(tkl), run_time=0.5)

        vec = VGroup(la, neo, ra, tk, lal, ral, neol, tkl)
        self.at("Electroporation")
        bolt = poly([(-5.7, 3.1), (-5.3, 2.3), (-5.9, 2.0), (-5.4, 1.0)], YELLOW, 6)
        self.play(Create(bolt), run_time=0.25)
        rest_all = VGroup(cellbox, cell_lbl, old, rest, gene_lbl)
        self.play(FadeOut(conn), vec.animate.shift(DOWN * 1.0), rest_all.animate.shift(UP * 1.6), run_time=0.8)
        self.play(FadeOut(bolt), run_time=0.2)
        CY = CY + 1.6

        self.at("In rare cells")
        conn2 = VGroup(*[DashedLine([x, CY + 1.55, 0], [x, CY + 0.25, 0], color=GREY, stroke_width=2) for x in (-3.4, 0.6)])
        self.play(Create(conn2), run_time=0.5)
        self.at("swaps")
        xs_ = VGroup(xmark(-3.4, CY + 0.9, 34, YELLOW), xmark(0.6, CY + 0.9, 34, YELLOW))
        self.play(FadeIn(xs_, scale=1.4), run_time=0.3)
        newseg = VGroup(la, neo, ra)
        self.play(FadeOut(old), FadeOut(gene_lbl), FadeOut(conn2), FadeOut(xs_), FadeOut(lal), FadeOut(ral),
                  FadeOut(neol), FadeOut(tkl), newseg.animate.shift(DOWN * 1.9), FadeOut(tk),
                  run_time=0.9)
        done = lab("the vector's version, in the gene's place", 24, GREEN).move_to([-1.4, CY - 0.65, 0])
        self.play(FadeIn(done), run_time=0.4)
        self.finish()


# ---------------------------------------------------------------------------------------------
def genome(cx, y, kind):
    parts = []
    if kind == "none":
        parts = [Rectangle(width=3.2, height=0.34, fill_color=TEAL, fill_opacity=0.5, stroke_color=TEAL, stroke_width=2.5)]
    elif kind == "random":
        parts = [Rectangle(width=1.7, height=0.34, fill_color=TEAL, fill_opacity=0.5, stroke_color=TEAL, stroke_width=2.5),
                 Rectangle(width=0.3, height=0.34, fill_color=BLUE, fill_opacity=0.7, stroke_color=BLUE, stroke_width=2.5),
                 Rectangle(width=0.5, height=0.34, fill_color=ORANGE, fill_opacity=0.8, stroke_color=ORANGE, stroke_width=2.5),
                 Rectangle(width=0.3, height=0.34, fill_color=BLUE, fill_opacity=0.7, stroke_color=BLUE, stroke_width=2.5),
                 Rectangle(width=0.5, height=0.34, fill_color=PURPLE, fill_opacity=0.8, stroke_color=PURPLE, stroke_width=2.5)]
    else:
        parts = [Rectangle(width=0.9, height=0.34, fill_color=TEAL, fill_opacity=0.5, stroke_color=TEAL, stroke_width=2.5),
                 Rectangle(width=0.3, height=0.34, fill_color=BLUE, fill_opacity=0.7, stroke_color=BLUE, stroke_width=2.5),
                 Rectangle(width=0.5, height=0.34, fill_color=ORANGE, fill_opacity=0.8, stroke_color=ORANGE, stroke_width=2.5),
                 Rectangle(width=0.3, height=0.34, fill_color=BLUE, fill_opacity=0.7, stroke_color=BLUE, stroke_width=2.5),
                 Rectangle(width=1.2, height=0.34, fill_color=TEAL, fill_opacity=0.5, stroke_color=TEAL, stroke_width=2.5)]
    g = VGroup(*parts).arrange(RIGHT, buff=0)
    return g.move_to([cx, y, 0])


class S03Select(SpokenScene):
    """Two selections: G418 kills cells with no vector; ganciclovir kills cells that kept tk; the survivor is screened and grown."""

    def construct(self):
        X = [-4.2, 0.0, 4.2]
        cA, cB, cC = [cell(x, 1.7) for x in X]
        gA, gB, gC = genome(X[0], 0.2, "none"), genome(X[1], 0.2, "random"), genome(X[2], 0.2, "swap")
        tA = lab("took up no vector", 26, GREY).move_to([X[0], -0.6, 0])
        tB = lab("random insertion", 26, GREY).move_to([X[1], -0.6, 0])
        tC = lab("correct swap", 26, GREY).move_to([X[2], -0.6, 0])
        enr = lab("enrichment, then screen survivors", 26, GREY).move_to([0, -2.45, 0])
        leg = VGroup(VGroup(Square(side_length=0.28, fill_color=ORANGE, fill_opacity=0.8, stroke_color=ORANGE), lab("neo", 24, ORANGE)).arrange(RIGHT, buff=0.15),
                     VGroup(Square(side_length=0.28, fill_color=PURPLE, fill_opacity=0.8, stroke_color=PURPLE), lab("tk", 24, PURPLE)).arrange(RIGHT, buff=0.15)).arrange(RIGHT, buff=0.7).move_to([0, -3.15, 0])

        self.at("A drug")
        self.play(FadeIn(VGroup(cA, cB, cC)), FadeIn(VGroup(gA, gB, gC)), FadeIn(VGroup(tA, tB, tC)), FadeIn(leg), FadeIn(enr), run_time=0.7)
        g418 = chip("G418", RED, 30).move_to([X[0], 3.0, 0])
        self.play(FadeIn(g418, shift=DOWN * 0.2), run_time=0.4)
        self.at("kills cells")
        xa = xmark(X[0], 1.7, 80, RED)
        self.play(FadeIn(xa, scale=1.4), cA.animate.set_opacity(0.15), run_time=0.4)
        self.play(FadeOut(g418), run_time=0.2)
        self.play(FadeIn(tick(X[1], -1.35, 30)), FadeIn(tick(X[2], -1.35, 30)), run_time=0.3)

        self.at("A correct swap loses")
        ring = Circle(radius=1.05, stroke_color=GREEN, stroke_width=4).move_to([X[2], 1.7, 0])
        notk = lab("no tk", 28, GREEN).move_to([X[2], -1.9, 0])
        self.play(Create(ring), FadeIn(notk), run_time=0.5)
        self.at("A random insertion keeps it")
        keeps = lab("keeps tk", 28, PURPLE).move_to([X[1], -1.9, 0])
        self.play(FadeIn(keeps), run_time=0.4)
        self.at("ganciclovir")
        gc = chip("ganciclovir", RED, 28).move_to([X[1], 3.0, 0])
        self.play(FadeIn(gc, shift=DOWN * 0.2), run_time=0.4)
        self.at("toxic")
        xb = xmark(X[1], 1.7, 80, RED)
        self.play(FadeIn(xb, scale=1.4), cB.animate.set_opacity(0.15), run_time=0.4)
        self.play(FadeOut(gc), run_time=0.2)

        self.at("Survivors are screened")
        gone = [cA, cB, gA, gB, tA, tB, xa, xb, keeps, leg, enr]
        ticks_ = [m for m in self.mobjects if isinstance(m, Text) and m.text in ("✓",)]
        self.play(*[FadeOut(o) for o in gone + ticks_], run_time=0.5)
        grp = VGroup(cC, gC, tC, ring, notk)
        self.play(grp.animate.shift(LEFT * 4.2), run_time=0.6)
        screen = chip("PCR or Southern blot", BLUE, 30).move_to([-0.6, -2.7, 0])
        self.play(FadeIn(screen, shift=UP * 0.15), run_time=0.4)
        self.at("then expanded")
        ok = tick(2.6, -2.7, 70)
        self.play(FadeIn(ok, scale=1.4), run_time=0.3)
        clone = VGroup(*[cell(0 + dx, 1.7 + dy, 0.55, AGOUTI, 0.35) for dx, dy in
                         [(-1.6, 0.5), (1.6, 0.5), (-2.6, -0.2), (2.6, -0.2), (-1.0, 1.25), (1.0, 1.25)]])
        cl_lbl = lab("a clone of correct cells", 28, GREEN).move_to([4.2, 2.9, 0])
        self.play(LaggedStart(*[GrowFromCenter(c) for c in clone], lag_ratio=0.12), FadeIn(cl_lbl), run_time=1.0)
        self.finish()


# ---------------------------------------------------------------------------------------------
class S04Mouse(SpokenScene):
    """Blastocyst injection, chimera coat, breeding to germline transmission, homozygous mutant."""

    def construct(self):
        # --- stage 1: injection and foster mother
        bl = Circle(radius=1.5, stroke_color=TEXT, stroke_width=3, fill_color=HOSTFILL, fill_opacity=1).move_to([0, 0.7, 0])
        cav = Circle(radius=0.8, stroke_color=GREY, stroke_width=2, fill_color=BG, fill_opacity=1).move_to([0, 0.7, 0])
        bl_lbl = lab("C57BL/6 host blastocyst: black", 26, TEXT).move_to([0, -1.2, 0])
        dish = RoundedRectangle(corner_radius=0.3, width=3.0, height=1.8, stroke_color=GREY, stroke_width=3,
                                fill_color=GREY, fill_opacity=0.08).move_to([-4.8, 2.0, 0])
        escs = VGroup(*[Circle(radius=0.26, stroke_color=AGOUTI, stroke_width=2, fill_color=AGOUTI, fill_opacity=0.55)
                        .move_to([-4.8 + dx, 2.0 + dy, 0]) for dx, dy in [(-0.7, 0.3), (0.0, 0.35), (0.7, 0.25), (-0.35, -0.35), (0.35, -0.4)]])
        es_lbl = lab("129 ES cells: agouti", 26, AGOUTI).move_to([-4.8, 0.7, 0])
        ex_l = lab("example strains and coat colours", 24, GREY).move_to([0, 3.3, 0])
        needle = Polygon([2.9, 2.6, 0], [3.1, 2.8, 0], [0.55, 1.15, 0], stroke_color=BLUE, stroke_width=3, fill_color=BLUE, fill_opacity=0.2)
        needle_cells = VGroup(*[Circle(radius=0.14, stroke_width=1.5, stroke_color=AGOUTI, fill_color=AGOUTI, fill_opacity=0.8).move_to([2.0 - 0.3 * i, 2.0 - 0.2 * i, 0]) for i in range(2)])

        self.at("are injected")
        self.play(FadeIn(bl), FadeIn(cav), FadeIn(dish), FadeIn(escs), FadeIn(es_lbl), FadeIn(ex_l), run_time=0.6)
        self.play(FadeIn(needle), FadeIn(needle_cells), run_time=0.4)
        inj = VGroup(*[Circle(radius=0.2, stroke_width=1.5, stroke_color=AGOUTI, fill_color=AGOUTI, fill_opacity=0.85).move_to([0.5 * ((i % 2) - 0.5) + 0.0, 0.55 + 0.3 * (i // 2), 0]) for i in range(4)])
        self.play(needle_cells.animate.move_to([0.4, 0.9, 0]).set_opacity(0.0), FadeIn(inj), run_time=0.7)
        self.play(FadeOut(needle), run_time=0.25)
        self.at("different coat")
        self.play(FadeIn(bl_lbl), run_time=0.4)
        mom = coat_mouse("neutral", 0.9).move_to([4.4, 0.7, 0])
        mom_lbl = lab("foster mother", 26, GREY).move_to([4.4, -0.35, 0])
        a1 = arr([1.8, 0.7], [2.7, 0.7], GREY, 5, 0.22)
        self.at("foster mothers")
        self.play(GrowArrow(a1), FadeIn(mom), FadeIn(mom_lbl), run_time=0.6)

        # --- stage 2: the chimera
        self.at("The pups are chimeras")
        self.play(*[FadeOut(o) for o in self.mobjects], run_time=0.5)
        ch = coat_mouse("chimera", 1.9).move_to([0, 0.5, 0])
        ch_lbl = lab("chimera: host cells and ES cells mixed", 30, TEXT).move_to([0, -1.9, 0])
        self.play(FadeIn(ch, scale=0.9), FadeIn(ch_lbl), run_time=0.7)
        self.at("shows the share")
        la = lab("agouti: from ES cells", 26, AGOUTI).move_to([-3.6, 2.3, 0])
        lb = lab("black: from the host", 26, TEXT).move_to([3.6, 2.3, 0])
        aa = arr([-3.1, 2.0], [-1.6, 1.3], AGOUTI, 4, 0.18)
        ab = arr([3.1, 2.0], [1.2, 0.7], TEXT, 4, 0.18)
        self.play(FadeIn(la), FadeIn(lb), GrowArrow(aa), GrowArrow(ab), run_time=0.6)

        # --- stage 3: mate with a black strain, read the litter
        self.at("A chimera, usually male")
        self.play(*[FadeOut(o) for o in self.mobjects], run_time=0.4)
        ch2 = coat_mouse("chimera", 1.0).move_to([-3.6, 2.2, 0])
        ch2_l = lab("chimera, usually male", 26, TEXT).move_to([-3.6, 1.2, 0])
        times = T("×", 48, TEXT).move_to([-0.8, 2.2, 0])
        bk = coat_mouse("black", 1.0).move_to([2.0, 2.2, 0])
        bk_l = lab("black strain", 26, TEXT).move_to([2.0, 1.2, 0])
        self.play(FadeIn(ch2), FadeIn(ch2_l), FadeIn(times), FadeIn(bk), FadeIn(bk_l), run_time=0.6)
        kinds = ["black", "agouti", "black", "agouti"]
        pups = VGroup(*[coat_mouse(k, 0.72).move_to([-4.5 + 3.0 * i, -0.4, 0]) for i, k in enumerate(kinds)])
        pup_l = lab("example litter", 24, GREY).move_to([-5.0, -1.4, 0])
        arrd = arr([-0.8, 0.8], [-0.8, 0.2], GREY, 4, 0.2)
        self.play(GrowArrow(arrd), LaggedStart(*[FadeIn(p, shift=DOWN * 0.2) for p in pups], lag_ratio=0.12), FadeIn(pup_l), run_time=0.9)
        self.at("Agouti pups come from")
        ag = [pups[i] for i, k in enumerate(kinds) if k == "agouti"]
        rings = VGroup(*[Ellipse(width=2.6, height=1.3, stroke_color=GREEN, stroke_width=3).move_to(p.get_center() + [-0.2, 0, 0]) for p in ag])
        dim = [pups[i].animate.set_opacity(0.3) for i, k in enumerate(kinds) if k == "black"]
        self.play(Create(rings), *dim, run_time=0.6)
        self.at("shows if they carry")
        dna = chip("tail DNA test", BLUE, 28).move_to([-2.4, -2.5, 0])
        res = lab("carries the targeted allele?", 28, GREEN).move_to([2.6, -2.5, 0])
        self.play(FadeIn(dna, shift=UP * 0.1), run_time=0.4)
        self.play(FadeIn(res), run_time=0.4)

        # --- stage 4: heterozygous, then homozygous
        self.at("These are usually heterozygous")
        self.play(*[FadeOut(o) for o in self.mobjects], run_time=0.5)
        p1 = coat_mouse("agouti", 0.85).move_to([-4.5, 1.0, 0])
        p2 = coat_mouse("agouti", 0.85).move_to([-0.7, 1.0, 0])
        g1 = M("+/-", 36, BLUE).move_to([-4.5, -0.1, 0])
        g2 = M("+/-", 36, BLUE).move_to([-0.7, -0.1, 0])
        hl = lab("heterozygous", 28, BLUE).move_to([-2.6, -0.9, 0])
        x2 = T("×", 48, TEXT).move_to([-2.6, 1.0, 0])
        self.play(FadeIn(p1), FadeIn(p2), FadeIn(g1), FadeIn(g2), FadeIn(x2), FadeIn(hl), run_time=0.7)
        self.at("Further breeding gives")
        a3 = arr([1.3, 1.0], [2.5, 1.0], GREY, 6, 0.26)
        p3 = coat_mouse("agouti", 0.85).move_to([4.6, 1.0, 0])
        g3 = M("-/-", 36, BLUE).move_to([4.6, -0.1, 0])
        hom = lab("homozygous mutant", 28, GREEN).move_to([4.6, -0.9, 0])
        self.play(GrowArrow(a3), FadeIn(p3), FadeIn(g3), FadeIn(hom), run_time=0.7)
        self.finish()


# ---------------------------------------------------------------------------------------------
class S05Reading(SpokenScene):
    """Reading: the colony screen (real counts), then a null mouse against wild-type, then the TrkA example."""

    def construct(self):
        # --- the screen: 2 of 234
        n_c, n_r = 26, 9
        pitch = 0.46
        dots = VGroup()
        pos = []
        for r in range(n_r):
            for c in range(n_c):
                if len(pos) < 234:
                    p = [(-(n_c - 1) / 2 + c) * pitch, ((n_r - 1) / 2 - r) * pitch + 0.1]
                    pos.append(p)
                    dots.add(Circle(radius=0.15, stroke_color=AGOUTI, stroke_width=1.5, fill_color=AGOUTI,
                                    fill_opacity=0.45).move_to([p[0], p[1], 0]))
        title = lab("G418-resistant colonies, each screened", 34, TEXT).move_to([0, 2.9, 0])
        tag_ = lab("real data", 24, GREY).move_to([5.0, -3.1, 0])
        self.at("At the cell stage")
        self.play(FadeIn(title), LaggedStart(*[FadeIn(d, scale=0.5) for d in dots], lag_ratio=0.004), FadeIn(tag_), run_time=1.4)
        self.at("two correct colonies")
        hi = [dots[40], dots[150]]
        rr = VGroup(*[Circle(radius=0.32, stroke_color=GREEN, stroke_width=4).move_to(h.get_center()) for h in hi])
        cnt = VGroup(*[T("234 colonies screened", 36, TEXT), T("2 correct", 36, GREEN)]).arrange(RIGHT, buff=0.8).move_to([0, -2.6, 0])
        self.play(*[h.animate.set_fill(GREEN, 1.0).set_stroke(GREEN) for h in hi], Create(rr), run_time=0.5)
        self.play(FadeIn(cnt), run_time=0.5)

        # --- mouse stage
        self.at("In mice")
        self.play(*[FadeOut(o) for o in self.mobjects], run_time=0.5)
        wt = coat_mouse("neutral", 1.1).move_to([-3.9, 1.6, 0])
        nl = coat_mouse("neutral", 1.1).move_to([3.5, 1.6, 0])
        wt_l = VGroup(lab("wild-type", 28, TEXT), M("+/+", 28, GREY)).arrange(DOWN, buff=0.1).move_to([-3.9, 0.2, 0])
        nl_l = VGroup(lab("homozygous null", 28, BLUE), M("-/-", 28, BLUE)).arrange(DOWN, buff=0.1).move_to([3.5, 0.2, 0])
        vs = lab("compare", 30, GREY).move_to([-0.1, 1.6, 0])
        self.play(FadeIn(wt), FadeIn(nl), FadeIn(wt_l), FadeIn(nl_l), FadeIn(vs), run_time=0.7)
        self.at("null mice lose")
        c1 = chip("TrkA-null", BLUE, 28).move_to([3.5, -1.1, 0])
        self.play(FadeIn(c1, shift=UP * 0.1), run_time=0.4)
        self.at("lose sympathetic neurons")
        l1 = chip("sympathetic neurons: lost", YELLOW, 26).move_to([3.5, -2.0, 0])
        l2 = chip("many sensory neurons: lost", YELLOW, 26).move_to([3.5, -2.9, 0])
        self.play(FadeIn(l1, shift=UP * 0.1), run_time=0.4)
        self.play(FadeIn(l2, shift=UP * 0.1), run_time=0.4)

        # --- ganglion + timeline
        self.at("Their superior cervical ganglion")
        self.play(*[FadeOut(o) for o in self.mobjects], run_time=0.5)
        rng = np.random.RandomState(3)

        def ganglion(cx, cy):
            return Ellipse(width=3.0, height=1.7, stroke_color=GREY, stroke_width=3, fill_color=GREY, fill_opacity=0.08).move_to([cx, cy, 0])

        def neurons(cx, cy, n=28):
            out = VGroup()
            for _ in range(n):
                while True:
                    dx, dy = rng.uniform(-1.2, 1.2), rng.uniform(-0.62, 0.62)
                    if (dx / 1.2) ** 2 + (dy / 0.62) ** 2 < 0.9:
                        break
                out.add(Dot(radius=0.07, color=YELLOW).move_to([cx + dx, cy + dy, 0]))
            return out

        gw, gn = ganglion(-4.0, 1.7), ganglion(-4.0, -1.5)
        nw, nn = neurons(-4.0, 1.7), neurons(-4.0, -1.5)
        gw_l = VGroup(lab("wild-type", 24, TEXT)).move_to([-4.0, 0.45, 0])
        gn_l = VGroup(lab("TrkA-null", 24, BLUE)).move_to([-4.0, -2.75, 0])
        top = lab("superior cervical ganglion", 24, GREY).move_to([-4.0, 2.95, 0])
        self.play(FadeIn(gw), FadeIn(gn), FadeIn(nw), FadeIn(nn), FadeIn(gw_l), FadeIn(gn_l), FadeIn(top), run_time=0.7)
        # idealised timeline
        ax = Arrow([-0.8, -2.5, 0], [6.1, -2.5, 0], buff=0, color=GREY, stroke_width=3, tip_length=0.18)
        ay = Arrow([-0.8, -2.5, 0], [-0.8, 2.3, 0], buff=0, color=GREY, stroke_width=3, tip_length=0.18)
        xl = lab("embryonic day", 24, GREY).move_to([3.0, -3.05, 0])
        yl = lab("neurons", 24, GREY).move_to([0.0, 2.65, 0])
        ide = lab("idealised", 24, GREY).move_to([4.6, 3.0, 0])
        e155 = VGroup(DashedLine([3.4, -2.5, 0], [3.4, 2.0, 0], color=GREY, stroke_width=2),
                      DashedLine([2.2, -2.5, 0], [2.2, 2.0, 0], color=GREY, stroke_width=2))
        e_l = VGroup(M("13.5", 24, GOLD).move_to([2.2, -2.85, 0]), M("15.5", 24, GOLD).move_to([3.4, -2.85, 0]))
        xl.move_to([5.2, -3.15, 0])
        wtl = poly([(-0.8, 1.6), (6.0, 1.6)], TEXT, 4)
        nl1 = poly([(-0.8, 1.6), (3.4, 1.6)], BLUE, 6)
        nl2 = poly([(3.4, 1.6), (4.0, 1.0), (4.6, 0.1), (5.2, -0.8), (6.0, -1.5)], BLUE, 6)
        wl_lab = lab("wild-type", 22, TEXT).move_to([5.1, 2.0, 0])
        self.play(Create(ax), Create(ay), FadeIn(xl), FadeIn(yl), FadeIn(ide), run_time=0.6)
        self.at("forms normally")
        self.play(Create(wtl), Create(nl1), FadeIn(wl_lab), run_time=1.0)
        self.at("from embryonic day")
        same_c = lab("same count", 22, GOLD).move_to([2.2, 2.3, 0])
        self.play(Create(e155), FadeIn(e_l), FadeIn(same_c), run_time=0.4)
        self.play(Create(nl2), *[d.animate.set_opacity(0.0) for d in nn[6:]], run_time=1.0)
        self.at("Survival, not birth")
        sv = chip("survival failed, not birth", RED, 26).move_to([4.2, -1.9, 0])
        self.play(FadeIn(sv, shift=UP * 0.1), run_time=0.4)
        self.finish()


# ---------------------------------------------------------------------------------------------
class S06Pitfalls(SpokenScene):
    """Left: background strain (flanking ES DNA, caspase-3 on two strains); right: compensation (MyoD and Myf-5)."""

    def construct(self):
        div = Line([0.0, 3.3, 0], [0.0, -3.3, 0], color=GREY, stroke_width=2).set_opacity(0.5)
        self.add(div)
        # ---------------- left
        LX = -3.1
        t1 = T("genetic background", 30, TEXT, weight=BOLD).move_to([LX, 3.1, 0])
        by = 1.95
        flank = VGroup(blk(-6.0, -4.6, by, AGOUTI, op=0.55), blk(-4.6, -3.1 + 0.0, by, BLUE, op=0.85),
                       blk(-3.1, -1.6, by, AGOUTI, op=0.55))
        f_l = lab("targeted gene", 22, BLUE).move_to([-3.85, by - 0.55, 0])
        f_l2 = lab("flanking DNA from the ES cell", 22, AGOUTI).move_to([LX, by + 0.6, 0])
        mut = VGroup(xmark(-5.3, by, 28, RED), xmark(-2.35, by, 28, RED))
        mut_l = lab("may carry its own mutations", 22, RED).move_to([LX, by - 1.1, 0])
        self.at("First, genetic background")
        self.play(FadeIn(t1), run_time=0.4)
        self.at("flanked by")
        self.play(FadeIn(flank), FadeIn(f_l), FadeIn(f_l2), run_time=0.6)
        self.at("may carry")
        self.play(FadeIn(mut, scale=1.3), FadeIn(mut_l), run_time=0.5)

        cs = lab("same knockout: caspase-3-null mice", 24, BLUE).move_to([LX, -0.15, 0])
        o1 = chip2(["on 129X1/SvJ:", "died perinatally, exencephaly"], RED, 22).move_to([LX, -1.0, 0])
        o2 = chip2(["on C57BL/6J: adults,", "minimal brain pathology"], GREEN, 22).move_to([LX, -2.0, 0])
        self.at("on one strain")
        self.play(FadeIn(cs), FadeIn(o1, shift=UP * 0.1), run_time=0.5)
        self.at("another strain")
        self.play(FadeIn(o2, shift=UP * 0.1), run_time=0.5)
        c1 = chip2(["control: backcross to a defined strain;", "compare wild-type, same background"], GREEN, 22)
        c1.move_to([LX, -3.05, 0])
        self.at("backcross")
        self.play(FadeIn(c1, shift=UP * 0.1), run_time=0.5)

        # ---------------- right
        RX = 3.2
        t2 = T("compensation", 30, TEXT, weight=BOLD).move_to([RX, 3.1, 0])
        myod = chip("MyoD", BLUE, 30).move_to([1.7, 1.5, 0])
        myf = chip("Myf-5", TEAL, 30).move_to([4.7, 1.5, 0])
        musc = chip("muscle", GREY, 28).move_to([RX, -0.3, 0])
        a1 = arr([1.7, 1.05], [2.7, -0.0, 0], GREY, 4, 0.18)
        a2 = arr([4.7, 1.05], [3.7, -0.0, 0], GREY, 4, 0.18)
        self.at("Second, compensation")
        self.play(FadeIn(t2), FadeIn(myod), FadeIn(myf), run_time=0.5)
        self.play(FadeIn(musc), GrowArrow(a1), GrowArrow(a2), run_time=0.5)
        self.at("had normal muscle")
        xm = T("✕", 26, RED, weight=BOLD).move_to(myod.get_corner(UL) + [0.05, 0.05, 0])
        nm = lab("MyoD-null: muscle normal", 24, GREEN).move_to([RX, -1.05, 0])
        self.play(FadeIn(xm, scale=1.4), myod[1].animate.set_opacity(0.35), FadeOut(a1), FadeIn(nm), run_time=0.5)
        up = lab("Myf-5 raised", 24, YELLOW).move_to([4.7, 2.5, 0])
        self.at("raised")
        self.play(myf.animate.scale(1.3), FadeIn(up), run_time=0.4)
        self.at("related genes together")
        c2 = chip2(["control: delete related", "genes together"], GREEN, 22)
        c2.move_to([RX, -2.4, 0])
        xm2 = T("✕", 26, RED, weight=BOLD).move_to(myf.get_corner(UL) + [0.05, 0.05, 0])
        self.play(FadeIn(c2, shift=UP * 0.1), FadeIn(xm2, scale=1.4), myf[1].animate.set_opacity(0.35), run_time=0.5)
        self.finish()


# ---------------------------------------------------------------------------------------------
class S07Bax(SpokenScene):
    """Bax-null: neuron death largely eliminated (idealised dots); Bax-null with NGF-null: test target innervation."""

    def construct(self):
        xs = np.linspace(-3.2, 3.2, 10)
        wt_l = lab("wild-type", 28, TEXT).move_to([-5.2, 1.9, 0])
        bx_l = lab("Bax-null", 28, BLUE).move_to([-5.2, -0.1, 0])
        wt = VGroup(*[Circle(radius=0.26, stroke_color=YELLOW, stroke_width=3, fill_color=YELLOW, fill_opacity=0.6).move_to([x + 0.6, 1.9, 0]) for x in xs])
        bx = VGroup(*[Circle(radius=0.26, stroke_color=YELLOW, stroke_width=3, fill_color=YELLOW, fill_opacity=0.6).move_to([x + 0.6, -0.1, 0]) for x in xs])
        ide = lab("idealised", 24, GREY).move_to([5.4, 3.1, 0])
        self.at("studied in")
        self.play(FadeIn(wt_l), FadeIn(bx_l), FadeIn(wt), FadeIn(bx), FadeIn(ide), run_time=0.7)
        self.at("had naturally occurring")
        dead = [wt[i] for i in (1, 3, 4, 7, 8)]
        marks = VGroup(*[xmark(d.get_center()[0], 1.9, 30, RED) for d in dead])
        self.play(*[d.animate.set_opacity(0.15) for d in dead], FadeIn(marks), run_time=0.7)
        dl = lab("natural neuron death", 24, RED).move_to([0.6, 2.75, 0])
        self.play(FadeIn(dl), run_time=0.3)
        self.at("largely eliminated")
        el = lab("largely eliminated", 24, GREEN).move_to([0.6, 0.75, 0])
        self.play(FadeIn(el), run_time=0.4)
        t1 = tag("Knudson and colleagues, 1995; White and colleagues, 1998", 0.0, -1.2)
        self.play(FadeIn(t1), run_time=0.3)
        self.at("A deletion in every")
        every = chip("gene deleted in every cell of the animal", BLUE, 28).move_to([0.0, -2.4, 0])
        self.play(FadeIn(every, shift=UP * 0.1), run_time=0.5)

        self.at("combined")
        self.play(*[FadeOut(o) for o in self.mobjects], run_time=0.5)
        bxc = chip("Bax-null", BLUE, 30).move_to([-4.2, 2.6, 0])
        ngc = chip("NGF-null", BLUE, 30).move_to([-1.2, 2.6, 0])
        plus = T("+", 40, TEXT).move_to([-2.7, 2.6, 0])
        ys = [1.1, 0.3, -0.5, -1.3]
        nr = VGroup(*[Circle(radius=0.28, stroke_color=YELLOW, stroke_width=3, fill_color=YELLOW, fill_opacity=0.6).move_to([-5.0, y, 0]) for y in ys])
        nr_l = lab("neurons stay alive", 26, GREEN).move_to([-3.4, 1.9, 0])
        tgt = RoundedRectangle(corner_radius=0.2, width=2.4, height=3.5, stroke_color=GREY, stroke_width=3,
                               fill_color=GREY, fill_opacity=0.1).move_to([4.4, -0.1, 0])
        tgt_l = lab("target", 26, GREY).move_to([4.4, 1.9, 0])
        axs = VGroup(*[Line([-4.7, y, 0], [3.2, y, 0], color=YELLOW, stroke_width=2.5) for y in ys])
        self.play(FadeIn(bxc), FadeIn(plus), FadeIn(ngc), run_time=0.5)
        self.play(FadeIn(nr), FadeIn(nr_l), FadeIn(tgt), FadeIn(tgt_l), Create(axs), run_time=0.8)
        self.at("could be tested")
        q = lab("what does NGF do for target innervation?", 32, TEXT).move_to([0.0, -2.4, 0])
        qq = T("?", 64, YELLOW, weight=BOLD).move_to([4.4, -0.1, 0])
        self.play(FadeIn(q, shift=UP * 0.1), FadeIn(qq), run_time=0.5)
        t2 = tag("Glebova and Ginty, 2004", 0.0, -3.1)
        self.play(FadeIn(t2), run_time=0.3)
        self.finish()


# ---------------------------------------------------------------------------------------------
def brain(cx, cy, kind, seed=0, w=2.9, h=2.4):
    """kind 'wt': neurons in neat rows; 'mut': a shared scrambled pattern with panel-specific jitter."""
    out = RoundedRectangle(corner_radius=0.8, width=w, height=h, stroke_color=GREY, stroke_width=3,
                           fill_color=GREY, fill_opacity=0.08).move_to([cx, cy, 0])
    dots = VGroup()
    if kind == "wt":
        for r in range(4):
            for c in range(6):
                dots.add(Dot(radius=0.07, color=YELLOW).move_to([cx + (c - 2.5) * 0.36, cy + (1.5 - r) * 0.42 - 0.05, 0]))
    else:
        base = np.random.RandomState(5)
        jit = np.random.RandomState(seed)
        for _ in range(24):
            x = base.uniform(-1.0, 1.0)
            y = base.uniform(-0.8, 0.8)
            dots.add(Dot(radius=0.07, color=YELLOW).move_to([cx + x + jit.uniform(-0.17, 0.17), cy + y + jit.uniform(-0.17, 0.17), 0]))
    return VGroup(out, dots)


def tag2(l1, l2, x, y):
    return VGroup(T(l1, 22, GOLD), T(l2, 22, GOLD)).arrange(DOWN, buff=0.04).move_to([x, y, 0])


class S08Reelin(SpokenScene):
    """Dab1 knockout copies the reeler brain; the double receptor knockout mimics it; knock-ins; the rule."""

    def construct(self):
        xs = [-4.7, -1.55, 1.55, 4.7]
        by = 1.5
        bw = brain(xs[0], by, "wt")
        br = brain(xs[1], by, "mut", 1)
        bd = brain(xs[2], by, "mut", 2)
        bv = brain(xs[3], by, "mut", 3)
        lw = lab("wild-type", 24, TEXT).move_to([xs[0], 0.0, 0])
        lr = lab("reeler", 24, TEXT).move_to([xs[1], 0.0, 0])
        lr2 = VGroup(lab("spontaneous mutant,", 22, GREY), lab("not a knockout", 22, GREY)).arrange(DOWN, buff=0.04).move_to([xs[1], -0.65, 0])
        ld = lab("Dab1 knockout", 24, BLUE).move_to([xs[2], 0.0, 0])
        lv = VGroup(lab("ApoER2/VLDLR", 24, BLUE), lab("double knockout", 24, BLUE)).arrange(DOWN, buff=0.04).move_to([xs[3], -0.22, 0])
        ex = lab("schematic: reeler-like", 22, GREY).move_to([0, 3.3, 0])
        self.at("Howell and colleagues")
        self.play(FadeIn(bw), FadeIn(lw), FadeIn(ex), run_time=0.4)
        self.play(FadeIn(bd), FadeIn(ld), run_time=0.5)
        self.play(FadeIn(tag2("Howell and", "colleagues, 1997", xs[2], -0.75)), run_time=0.3)
        self.at("copied the")
        self.play(FadeIn(br), FadeIn(lr), run_time=0.5)
        self.at("spontaneous mutant")
        self.play(FadeIn(lr2), run_time=0.4)
        self.at("removed both")
        self.play(FadeIn(bv), FadeIn(lv), run_time=0.5)
        self.play(FadeIn(tag2("Trommsdorff and", "colleagues, 1999", xs[3], -1.05)), run_time=0.3)
        self.at("mimicked reeler")
        br_ = Rectangle(width=9.5, height=2.5, stroke_color=GREEN, stroke_width=3).move_to([1.575, by + 0.02, 0])
        same = lab("reeler-like: misplaced neurons", 30, GREEN).move_to([1.575, -2.4, 0])
        self.play(Create(br_), FadeIn(same), run_time=0.6)

        # --- knock-in
        self.at("change a gene")
        self.play(*[FadeOut(o) for o in self.mobjects], run_time=0.5)
        ko_bar = VGroup(blk(-5.8, -2.6, 2.5, TEAL, h=0.5, op=0.45), blk(-1.2, 1.6, 2.5, TEAL, h=0.5, op=0.45))
        ko_gap = DashedVMobject(Rectangle(width=1.4, height=0.5, stroke_color=RED, stroke_width=2).move_to([-1.9, 2.5, 0]))
        ko_l = lab("knockout: gene deleted", 28, RED).move_to([4.0, 2.5, 0])
        ki_bar = VGroup(blk(-5.8, -2.6, 1.0, TEAL, h=0.5, op=0.45), blk(-2.6, -1.2, 1.0, BLUE, h=0.5, op=0.85), blk(-1.2, 1.6, 1.0, TEAL, h=0.5, op=0.45))
        ki_l = lab("knock-in: gene switched", 28, BLUE).move_to([4.0, 1.0, 0])
        self.play(FadeIn(ko_bar), Create(ko_gap), FadeIn(ko_l), run_time=0.6)
        self.at("instead of deleting")
        self.play(FadeIn(ki_bar), FadeIn(ki_l), run_time=0.5)

        self.at("put in a")
        s1 = chip("alpha1 or alpha2 subunit", TEAL, 30).move_to([-2.2, -0.9, 0])
        s2 = chip("diazepam-insensitive alpha1 or alpha2", BLUE, 30).move_to([-2.2, -0.9, 0])
        t = tag("Fagiolini and colleagues, 2004", -2.2, -1.6)
        self.play(FadeIn(s1), run_time=0.3)
        self.play(Transform(s1, s2), FadeIn(t), run_time=0.7)
        self.at("critical period")
        res = lab("alpha1 circuits drive the critical period", 34, GREEN).move_to([0, -2.5, 0])
        self.play(FadeIn(res, shift=UP * 0.1), run_time=0.5)

        self.at("A knockout shows")
        self.play(*[FadeOut(o) for o in self.mobjects], run_time=0.5)
        rule = T("A knockout shows necessity,", 44, GOLD, font=TITLE_FONT).move_to([0, 0.5, 0])
        rule2 = T("not sufficiency.", 44, GOLD, font=TITLE_FONT).move_to([0, -0.4, 0])
        self.play(FadeIn(rule, shift=UP * 0.15), run_time=0.5)
        self.play(FadeIn(rule2, shift=UP * 0.15), run_time=0.5)
        self.finish()


def lines2(text, color):
    return lab(text, 26, color)


class S09End(EndCard):
    LINE = "A knockout shows necessity, not sufficiency."
