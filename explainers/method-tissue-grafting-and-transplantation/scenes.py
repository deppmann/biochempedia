"""Tissue grafting and transplantation: move it, mark it, read the result (Biochemistrypedia methods film)

Timed to the SPOKEN words: every self.at("...") cue waits for that phrase in audio/words.json.

COLOR MAP (one color per concept, whole video)
  TEAL   = donor tissue / quail cells (the grafted cells)
  ORANGE = host tissue / pigmented host cells / chick cells that are the host
  GREY   = embryo outlines, structure, de-emphasised text
  YELLOW = the question, signals, motor neurons, results to read
  PURPLE = an injected lineage label (dye, dextran)
  RED    = the wound, the pitfall
  GREEN  = a control
  BLUE   = needles and the operating tools
  GOLD   = dates, tags and the closing rule
"""
import numpy as np
from bp_style import *  # noqa: F401,F403

PURPLE = "#B58CD9"
ORANGE = "#F29E4C"
DONOR = TEAL
HOST = ORANGE


def P(x, y):
    return np.array([x, y, 0.0])


def lab(text, size=24, color=GREY, **kw):
    return T(text, size, color, **kw)


def arr(a, b, color=GREY, w=5, tip=0.2):
    return Arrow(P(*a), P(*b), buff=0.0, color=color, stroke_width=w, tip_length=tip,
                 max_tip_length_to_length_ratio=0.45, max_stroke_width_to_length_ratio=12)


def emb(cx, cy, w, h, color=GREY, fo=0.08, sw=3):
    return Ellipse(width=w, height=h, stroke_color=color, stroke_width=sw, fill_color=color,
                   fill_opacity=fo).move_to(P(cx, cy))


def cell(x, y, r, color, fo=0.6, sw=2):
    return Circle(radius=r, stroke_color=color, stroke_width=sw, fill_color=color, fill_opacity=fo).move_to(P(x, y))


def tag(text, x, y, size=24):
    return T(text, size, GOLD).move_to(P(x, y))


def slab(cx, cy, w, h, color=GREY):
    return RoundedRectangle(corner_radius=0.12, width=w, height=h, stroke_color=color, stroke_width=2.5,
                            fill_color=color, fill_opacity=0.07).move_to(P(cx, cy))


def grid_cells(cx, cy, cols, rows, dx, dy, r, colors, seed=0):
    """cells on a grid; colors is a list (len cols*rows) of colour strings."""
    g = VGroup()
    k = 0
    for j in range(rows):
        for i in range(cols):
            x = cx + (i - (cols - 1) / 2) * dx
            y = cy + ((rows - 1) / 2 - j) * dy
            g.add(cell(x, y, r, colors[k], 0.6))
            k += 1
    return g


def nucleus(x, y, r, block=False, scale=1.0):
    n = Circle(radius=r, stroke_color=GREY, stroke_width=2.5, fill_color=GREY, fill_opacity=0.25).move_to(P(x, y))
    g = VGroup(n)
    if block:
        b = Square(side_length=r * 0.62, stroke_width=0, fill_color=TEXT, fill_opacity=0.95).move_to(P(x + r * 0.35, y - r * 0.2))
        g.add(b)
    return g


# -----------------------------------------------------------------------------------------------
class S00Title(TitleCard):
    LESSON = "Methods library"
    TITLE = "Move It, Mark It, Read the Result"


# -----------------------------------------------------------------------------------------------
class S01Problem(SpokenScene):
    """a normal embryo cannot say if a tissue is fixed or instructed; move the tissue and read what it does."""

    def construct(self):
        A = emb(-3.4, -0.4, 6.0, 4.4)
        patch = DashedVMobject(Circle(radius=0.75, stroke_color=DONOR, stroke_width=4).move_to(P(-4.2, 0.2)))
        patch_fill = cell(-4.2, 0.2, 0.75, DONOR, 0.35, 0)
        nb = VGroup(*[cell(-4.2 + 1.5 * np.cos(a), 0.2 + 1.35 * np.sin(a), 0.32, HOST, 0.55)
                      for a in np.linspace(0.4, 2 * np.pi - 0.2, 7)])

        self.at("Look at a normal embryo")
        self.play(FadeIn(A), run_time=0.7)
        self.at("fate")
        self.play(FadeIn(patch), FadeIn(patch_fill), run_time=0.5)
        q1 = chip("fixed?", YELLOW, 28).move_to(P(-5.4, 3.05))
        self.at("fixed")
        self.play(FadeIn(q1, shift=DOWN * 0.1), run_time=0.4)
        q2 = chip("instructed by neighbours?", YELLOW, 26).move_to(P(-1.7, 3.05))
        self.at("instructed by its")
        self.play(FadeIn(q2, shift=DOWN * 0.1), FadeIn(nb), run_time=0.6)

        out = VGroup(*[arr((-3.5 + 0.1 * k, 0.2 + 0.5 * (k - 1)), (-1.4, 0.2 + 1.1 * (k - 1)), YELLOW, 4, 0.16)
                       for k in range(3)])
        lo = lab("what it sends", 26, YELLOW).move_to(P(-5.0, -3.1))
        self.at("what a region sends")
        self.play(*[GrowArrow(a) for a in out], FadeIn(lo), run_time=0.6)
        inn = VGroup(*[arr((-6.2, 0.2 + 1.0 * (k - 1)), (-5.1, 0.2 + 0.6 * (k - 1)), YELLOW, 4, 0.16) for k in range(3)])
        li = lab("what it can receive", 26, YELLOW).move_to(P(-1.7, -3.1))
        self.at("can receive")
        self.play(*[GrowArrow(a) for a in inn], FadeIn(li), run_time=0.6)

        B = emb(3.4, -0.4, 6.0, 4.4)
        moved = patch_fill.copy()
        self.at("So move the tissue")
        self.play(FadeOut(VGroup(out, inn, lo, li, q1, q2)), FadeIn(B), run_time=0.6)
        self.play(moved.animate(path_arc=-1.0).move_to(P(4.6, -1.0)), patch_fill.animate.set_fill(DONOR, 0.0),
                  run_time=1.0)
        lnew = lab("new place", 30, TEXT).move_to(P(3.4, -3.1))
        self.at("new place")
        self.play(FadeIn(lnew), run_time=0.4)
        lnew2 = lab("new time", 30, TEXT).move_to(P(3.4, -3.1))
        self.at("new time")
        self.play(ReplacementTransform(lnew, lnew2), B.animate.scale(1.07), run_time=0.5)
        lnew3 = lab("new host", 30, TEXT).move_to(P(3.4, -3.1))
        self.at("new host")
        self.play(ReplacementTransform(lnew2, lnew3), B.animate.scale(1 / 1.07), run_time=0.5)
        qq = T("?", 72, YELLOW, weight=BOLD).move_to(P(4.6, 0.55))
        qt = chip("what does it do?", YELLOW, 30).move_to(P(3.4, 3.05))
        self.at("read what it does")
        self.play(FadeIn(qq), FadeIn(qt, shift=DOWN * 0.1), run_time=0.6)
        self.finish()


# -----------------------------------------------------------------------------------------------
class S02Pick(SpokenScene):
    """donor and host, same stage or different ages, own place or new place; then the needles and wax plate."""

    def construct(self):
        D = emb(-3.5, -0.2, 5.4, 4.2)
        dl = lab("donor", 30, TEXT).move_to(P(-3.5, 2.6))
        patch = DashedVMobject(Circle(radius=0.7, stroke_color=DONOR, stroke_width=4).move_to(P(-4.4, 0.4)))
        pf = cell(-4.4, 0.4, 0.7, DONOR, 0.45, 0)
        H = emb(3.5, -0.2, 5.4, 4.2)
        hl = lab("host", 30, TEXT).move_to(P(3.5, 2.6))

        self.at("Pick a donor region")
        self.play(FadeIn(D), FadeIn(dl), FadeIn(patch), FadeIn(pf), run_time=0.8)
        self.at("host embryo")
        self.play(FadeIn(H), FadeIn(hl), run_time=0.6)
        cs = chip("same stage", GREEN, 30).move_to(P(0, -3.1))
        self.at("same stage")
        self.play(FadeIn(cs, shift=UP * 0.1), run_time=0.4)
        cd = chip("different ages", YELLOW, 30).move_to(P(0, -3.1))
        self.at("different ages")
        dg = VGroup(D, dl, patch, pf)
        self.play(ReplacementTransform(cs, cd), dg.animate.scale(0.8, about_point=P(-3.5, -0.2)), run_time=0.7)
        p2 = pf.copy().set_fill(DONOR, 0.7)
        pc = pf.get_center()
        self.at("its own place")
        self.play(FadeOut(cd), FadeIn(p2), run_time=0.2)
        self.play(p2.animate.move_to(pc + UP * 1.3), run_time=0.5)
        self.play(p2.animate.move_to(pc), run_time=0.5)
        self.at("new one")
        self.play(p2.animate(path_arc=-1.0).move_to(P(4.5, -0.9)), run_time=1.0)

        self.at("glass needles")
        self.play(FadeOut(VGroup(dg, H, hl, p2)), run_time=0.5)
        plate = Rectangle(width=12.0, height=1.0, stroke_color=GREY, stroke_width=3, fill_color=GREY, fill_opacity=0.3).move_to(P(0, -2.95))
        well = Rectangle(width=4.6, height=0.7, stroke_width=0, fill_color=BG, fill_opacity=1).move_to(P(0, -2.7))
        egg = Circle(radius=1.9, stroke_color=TEXT, stroke_width=3, fill_color=GREY, fill_opacity=0.25).move_to(P(0, -0.15))
        needle = Line(P(6.2, 2.4), P(1.2, 0.2), color=BLUE, stroke_width=6)
        nl = lab("thin glass needle, often heated", 28, BLUE).move_to(P(3.3, 3.1))
        self.play(FadeIn(plate), FadeIn(well), FadeIn(egg), Create(needle), FadeIn(nl), run_time=1.0)
        wl = lab("wax plate with tiny wells", 28, GREY).move_to(P(-4.0, -2.0))
        hold = lab("holds the egg still", 28, TEXT).move_to(P(-4.3, 0.2))
        self.at("wax plates")
        self.play(FadeIn(wl, shift=UP * 0.1), run_time=0.5)
        self.play(FadeIn(hold), run_time=0.4)
        self.finish()


# -----------------------------------------------------------------------------------------------
class S03Mark(SpokenScene):
    """cells of donor and host look alike; pigment marks newts; quail nuclei carry a dense block that persists."""

    def construct(self):
        PL = RoundedRectangle(corner_radius=0.2, width=6.3, height=6.2, stroke_color=GREY, stroke_width=2,
                              fill_color=GREY, fill_opacity=0.05).move_to(P(-3.5, -0.1))
        PR = PL.copy().move_to(P(3.5, -0.1))
        tl = lab("newt: pigment", 28, TEXT, weight=BOLD).move_to(P(-3.5, 2.55))
        tr = lab("quail and chick: nuclei", 28, TEXT, weight=BOLD).move_to(P(3.5, 2.55))
        donor_idx = {(1, 1), (2, 1), (1, 2), (2, 2)}
        n_c, n_r = 6, 4
        grey_cols, mark_cols = [], []
        for j in range(n_r):
            for i in range(n_c):
                d = (i, j) in donor_idx
                grey_cols.append(GREY)
                mark_cols.append(DONOR if d else HOST)
        cells = grid_cells(-3.5, 0.45, n_c, n_r, 0.84, 0.84, 0.34, grey_cols)
        self.at("told apart")
        self.play(FadeIn(PL), FadeIn(tl), FadeIn(cells), run_time=0.7)
        q1 = lab("which cells are donor, which host?", 24, YELLOW).move_to(P(-3.5, -2.3))
        self.play(FadeIn(q1), run_time=0.4)
        q2 = lab("second axis: from the graft alone?", 24, YELLOW).move_to(P(-3.5, -2.8))
        self.at("second axis")
        self.play(FadeIn(q2), run_time=0.4)
        self.at("newt species")
        anims = [c.animate.set_fill(m, 0.6).set_stroke(m) for c, m in zip(cells, mark_cols)]
        l1 = lab("pale donor", 26, DONOR).move_to(P(-5.0, -2.35))
        l2 = lab("pigmented host", 26, HOST).move_to(P(-1.9, -2.35))
        self.play(*anims, FadeOut(q1), FadeOut(q2), run_time=0.8)
        self.play(FadeIn(l1), FadeIn(l2), run_time=0.4)

        self.at("For birds")
        self.play(FadeIn(PR), FadeIn(tr), run_time=0.5)
        cx_ch, cx_q = 1.85, 4.4
        chick = VGroup(cell(cx_ch, 1.0, 0.95, HOST, 0.25), nucleus(cx_ch, 1.0, 0.46))
        quail = VGroup(cell(cx_q, 1.0, 0.95, DONOR, 0.25), nucleus(cx_q, 1.0, 0.46, block=True))
        cl = lab("chick", 26, HOST).move_to(P(cx_ch, -0.2))
        ql = lab("quail", 26, DONOR).move_to(P(cx_q, -0.2))
        self.play(FadeIn(chick), FadeIn(quail), FadeIn(cl), FadeIn(ql), run_time=0.7)
        self.at("large block")
        bl = lab("dense block", 24, TEXT).move_to(P(5.3, -0.75))
        ba = arr((5.2, -0.55), (cx_q + 0.4, 0.85), TEXT, 3, 0.14)
        self.play(FadeIn(bl), GrowArrow(ba), run_time=0.5)
        self.at("does not fade")
        two = VGroup(*[VGroup(cell(x, -1.35, 0.6, DONOR, 0.25), nucleus(x, -1.35, 0.29, block=True)) for x in (3.25, 5.55)])
        self.play(FadeOut(bl), FadeOut(ba), FadeIn(two, shift=DOWN * 0.2), run_time=0.7)
        four = VGroup(*[VGroup(cell(x, -2.6, 0.42, DONOR, 0.25), nucleus(x, -2.6, 0.2, block=True))
                        for x in (2.65, 3.85, 4.95, 6.1)])
        self.play(FadeIn(four, shift=DOWN * 0.2), run_time=0.7)
        self.finish()


# -----------------------------------------------------------------------------------------------
class S04Develop(SpokenScene):
    """develop, fix, section: pale vs pigmented cells; quail piece grafted at the same level, cells emigrate."""

    def construct(self):
        r1, r2 = 1.6, -1.75
        eh = 2.6
        # row 1: newt
        eA = emb(-4.9, r1, 2.7, eh)
        gA = cell(-4.3, r1 - 0.3, 0.38, DONOR, 0.7)
        nlabel = lab("pale graft in host", 22, GREY).move_to(P(-4.9, r1 - 1.55))
        self.at("Let the host develop")
        self.play(FadeIn(eA), FadeIn(gA), FadeIn(nlabel), run_time=0.6)
        a1 = arr((-3.4, r1), (-2.3, r1), GREY, 4, 0.16)
        dl = lab("develop", 22, GREY).move_to(P(-2.85, r1 + 0.45))
        eB = emb(-0.6, r1, 2.7, eh)
        pri = Line(P(-1.05, r1 - 0.8), P(-1.05, r1 + 0.8), color=GREY, stroke_width=7)
        sec = Line(P(-0.15, r1 - 0.7), P(-0.15, r1 + 0.7), color=HOST, stroke_width=7)
        self.play(GrowArrow(a1), FadeIn(dl), FadeIn(eB), FadeIn(pri), FadeIn(sec), run_time=0.8)
        a2 = arr((0.9, r1), (1.95, r1), GREY, 4, 0.16)
        sl = lab("section", 22, GREY).move_to(P(1.4, r1 + 0.45))
        S1 = slab(4.2, r1, 4.2, 2.5)
        cols = [HOST] * 28
        for k in (3, 11, 20):
            cols[k] = DONOR
        cs = grid_cells(4.2, r1, 7, 4, 0.55, 0.56, 0.22, cols)
        self.at("fix and section it")
        self.play(GrowArrow(a2), FadeIn(sl), FadeIn(S1), FadeIn(cs), run_time=0.8)
        l_h = lab("host, induced", 22, HOST).move_to(P(3.0, r1 - 1.6))
        hosts = [c for k, c in enumerate(cs) if cols[k] == HOST][:10]
        self.at("Pigmented cells")
        self.play(FadeIn(l_h), *[c.animate(rate_func=there_and_back).scale(1.3) for c in hosts], run_time=0.8)
        l_d = lab("donor", 22, DONOR).move_to(P(5.5, r1 - 1.6))
        dons = [c for k, c in enumerate(cs) if cols[k] == DONOR]
        self.at("Pale cells")
        self.play(FadeIn(l_d), *[c.animate(rate_func=there_and_back).scale(1.7) for c in dons], run_time=0.8)

        # row 2: bird
        self.at("For birds")
        eC = RoundedRectangle(corner_radius=0.7, width=3.3, height=1.5, stroke_color=GREY, stroke_width=3,
                              fill_color=GREY, fill_opacity=0.08).move_to(P(-4.7, r2))
        tube = Line(P(-6.2, r2), P(-3.2, r2), color=GREY, stroke_width=5)
        self.play(FadeIn(eC), FadeIn(tube), run_time=0.5)
        self.at("quail neural tube")
        qp = Line(P(-5.15, r2), P(-4.25, r2), color=DONOR, stroke_width=13)
        ql = lab("quail piece", 22, DONOR).move_to(P(-4.7, r2 - 1.2))
        self.play(FadeIn(qp, scale=1.3), FadeIn(ql), run_time=0.6)
        self.at("same axial level")
        self.play(Indicate(qp, color=DONOR, scale_factor=1.15), run_time=0.7)
        a3 = arr((-2.9, r2), (-1.85, r2), GREY, 4, 0.16)
        eD = RoundedRectangle(corner_radius=0.7, width=3.3, height=1.5, stroke_color=GREY, stroke_width=3,
                              fill_color=GREY, fill_opacity=0.08).move_to(P(-0.4, r2))
        tube2 = Line(P(-1.9, r2), P(1.1, r2), color=GREY, stroke_width=5)
        qp2 = Line(P(-0.85, r2), P(0.05, r2), color=DONOR, stroke_width=13)
        self.play(GrowArrow(a3), FadeIn(eD), FadeIn(tube2), FadeIn(qp2), run_time=0.6)
        dots = VGroup(*[cell(x, r2 + dy, 0.11, DONOR, 0.9, 0) for x, dy in
                        [(-0.6, 0.35), (-0.15, 0.45), (-0.45, -0.38), (0.0, -0.35), (-0.8, 0.22), (-0.05, 0.22)]])
        self.at("emigrate")
        self.play(FadeIn(dots, shift=UP * 0.1), run_time=0.7)
        a4 = arr((1.25, r2), (2.1, r2), GREY, 4, 0.16)
        S2 = slab(4.3, r2, 4.0, 2.5)
        cols2 = [HOST] * 28
        for k in (5, 6, 13, 22):
            cols2[k] = DONOR
        cs2 = grid_cells(4.3, r2, 7, 4, 0.52, 0.56, 0.21, cols2)
        l2 = lab("quail cells found later in sections", 22, DONOR).move_to(P(4.3, r2 - 1.55))
        self.at("sections long afterwards")
        self.play(GrowArrow(a4), FadeIn(S2), FadeIn(cs2), FadeIn(l2), run_time=0.8)
        self.finish()


# -----------------------------------------------------------------------------------------------
class S05Reading(SpokenScene):
    """host cells = instruction, donor cells = self-differentiation; idealised counts."""

    def construct(self):
        n = 10
        sq = 0.42
        cy = -0.5
        cxL, cxR = -3.4, 3.4
        rng = np.random.RandomState(4)

        def sq_grid(cx, n_donor, n_host=None):
            idx = np.arange(n * n)
            don = set(rng.permutation(idx)[:n_donor].tolist())
            g = VGroup()
            for k in range(n * n):
                i, j = k % n, k // n
                x = cx + (i - (n - 1) / 2) * sq
                y = cy + ((n - 1) / 2 - j) * sq
                col = DONOR if k in don else HOST
                g.add(Square(side_length=sq * 0.86, stroke_width=1.5, stroke_color=col, fill_color=col,
                             fill_opacity=0.6).move_to(P(x, y)))
            return g

        tL = lab("second neural tube", 28, TEXT, weight=BOLD).move_to(P(cxL, 2.95))
        tR = lab("notochord", 28, TEXT, weight=BOLD).move_to(P(cxR, 2.95))
        gL = sq_grid(cxL, 0)
        gR = sq_grid(cxR, 100)
        vL = chip("host cells: instruction", HOST, 26).move_to(P(cxL, 2.3))
        vR = chip("donor cells: self-differentiation", DONOR, 26).move_to(P(cxR, 2.3))
        self.at("A structure made of host cells")
        self.play(FadeIn(tL), FadeIn(gL), run_time=0.5)
        self.at("shows instruction")
        self.play(FadeIn(vL, shift=DOWN * 0.1), run_time=0.4)
        self.at("A structure made of donor cells")
        self.play(FadeIn(tR), FadeIn(gR), run_time=0.5)
        self.wait(0.9)
        self.play(FadeIn(vR, shift=DOWN * 0.1), run_time=0.4)
        pat_L = rng.permutation(100)[:10].tolist()
        pat_R = rng.permutation(100)[:3].tolist()   # host squares in the notochord grid
        animsL = [gL[k].animate.set_fill(DONOR, 0.6).set_stroke(DONOR) for k in pat_L]
        animsR = [gR[k].animate.set_fill(HOST, 0.6).set_stroke(HOST) for k in pat_R]
        ex = lab("idealised example, not real data; each square = 1% of the cells", 22, GOLD).move_to(P(0, 3.45))
        self.at("The marker decides which")
        self.play(Indicate(gL, color=YELLOW, scale_factor=1.04), Indicate(gR, color=YELLOW, scale_factor=1.04), run_time=0.8)
        self.at("idealized example")
        self.play(FadeIn(ex), *animsL, *animsR, run_time=1.0)
        a1 = lab("120 of 1,200 cells unpigmented", 22, TEXT).move_to(P(cxL, -3.0))
        a2 = lab("about 10% donor, so about 90% host", 22, HOST).move_to(P(cxL, -3.4))
        self.at("neural tube cells")
        self.play(FadeIn(a1), run_time=0.4)
        self.at("that is about 10")
        self.play(FadeIn(a2), run_time=0.5)
        b1 = lab("300 of 310 cells unpigmented", 22, TEXT).move_to(P(cxR, -3.0))
        b2 = lab("about 97% donor", 22, DONOR).move_to(P(cxR, -3.4))
        self.at("310 notochord")
        self.play(FadeIn(b1), run_time=0.4)
        self.at("About 97")
        self.play(FadeIn(b2), run_time=0.5)
        self.finish()


# -----------------------------------------------------------------------------------------------
class S06Pitfalls(SpokenScene):
    """three columns: the wound; pigment fades unevenly vs injected dye; grafting artefacts vs dextran injection."""

    def construct(self):
        cx = [-4.6, 0.0, 4.6]
        hy = 3.05
        # --- column 1: the wound
        h1 = chip("the wound", RED, 28).move_to(P(cx[0], hy))
        e1 = emb(cx[0], 0.2, 3.9, 3.4)
        wound = VGroup(Line(P(cx[0] + 0.6, 0.0), P(cx[0] + 1.0, 0.45), color=RED, stroke_width=6),
                       Line(P(cx[0] + 1.0, 0.45), P(cx[0] + 1.3, 0.05), color=RED, stroke_width=6),
                       Line(P(cx[0] + 1.3, 0.05), P(cx[0] + 1.6, 0.5), color=RED, stroke_width=6))
        wp = cell(cx[0] - 0.3, 0.3, 0.55, DONOR, 0.5)
        l1 = lab("a graft is also a wound", 24, RED).move_to(P(cx[0], -2.1))
        c1 = chip("control for the wound", GREEN, 24).move_to(P(cx[0], -2.9))
        self.at("graft is also a wound")
        self.play(FadeIn(h1), FadeIn(e1), FadeIn(wp), run_time=0.5)
        self.play(Create(wound), FadeIn(l1), run_time=0.7)
        self.at("wound effects need a control")
        self.play(FadeIn(c1, shift=UP * 0.1), run_time=0.5)

        # --- column 2: pigment
        h2 = chip("the marker", PURPLE, 28).move_to(P(cx[1], hy))
        self.at("natural pigment")
        pts = [(0.0, 1.8, "#E8A24F"), (-0.55, 1.0, "#E8A24F"), (0.55, 1.0, "#3B3328"), (-0.95, 0.2, "#E8A24F"), (-0.15, 0.2, "#3B3328")]
        rr = 0.36

        def edge(p, q):
            import math
            dx, dy = q[0] - p[0], q[1] - p[1]
            L = math.hypot(dx, dy)
            ux, uy = dx / L, dy / L
            return Line(P(cx[1] + p[0] + ux * rr, p[1] + uy * rr), P(cx[1] + q[0] - ux * rr, q[1] - uy * rr), color=GREY, stroke_width=3)
        links = VGroup(*[edge(p, q) for p, q in [(pts[0], pts[1]), (pts[0], pts[2]), (pts[1], pts[3]), (pts[1], pts[4])]])
        chain = VGroup(*[Circle(radius=rr, stroke_color=HOST, stroke_width=2, fill_color=col, fill_opacity=1).move_to(P(cx[1] + x, y))
                         for x, y, col in pts])
        l2 = lab("pigment not shared evenly", 24, HOST).move_to(P(cx[1], -2.1))
        self.play(FadeIn(h2), FadeIn(links), FadeIn(chain, lag_ratio=0.2), FadeIn(l2), run_time=1.0)
        ys = [1.8, 1.0, 0.2, -0.6, -1.4]
        ops = [0.8, 0.69, 0.58, 0.46, 0.35]
        dye = VGroup(*[cell(cx[1], y, 0.36, PURPLE, o) for y, o in zip(ys, ops)])
        dlinks = VGroup(*[Line(P(cx[1], ys[k] - 0.38), P(cx[1], ys[k + 1] + 0.38), color=GREY, stroke_width=3) for k in range(4)])
        c2 = chip("or an injected dye", PURPLE, 24).move_to(P(cx[1], -2.9))
        self.at("injected dye")
        self.play(FadeOut(chain), FadeOut(links), FadeOut(l2), FadeIn(dye), FadeIn(dlinks), FadeIn(c2, shift=UP * 0.1), run_time=0.9)

        # --- column 3: grafting artefacts
        h3 = chip("grafting artefacts?", RED, 28).move_to(P(cx[2], hy))
        e3 = emb(cx[2], 1.0, 3.7, 2.6)
        g3 = cell(cx[2] - 0.7, 1.1, 0.45, DONOR, 0.6)
        lg = lab("graft", 24, DONOR).move_to(P(cx[2] + 0.5, 1.0))
        self.at("Grafting itself may")
        self.play(FadeIn(h3), FadeIn(e3), FadeIn(g3), FadeIn(lg), run_time=0.7)
        l3 = lab("same pathways, three methods", 24, TEXT).move_to(P(cx[2], 2.15))
        bl = VGroup(*[cell(cx[2] + dx, dy, 0.5, GREY, 0.2) for dx, dy in [(-0.9, 0.2), (0.35, 0.8), (-0.35, -0.8), (0.95, -0.35)]])
        needle = Line(P(cx[2] + 2.0, 1.7), P(cx[2] + 0.8, 1.15), color=BLUE, stroke_width=5)
        self.at("three methods")
        self.play(FadeOut(VGroup(e3, g3, lg)), FadeIn(bl), run_time=0.7)
        self.wait(1.0)
        self.play(FadeIn(l3), run_time=0.4)
        self.at("a fluorescent")
        self.play(Create(needle), run_time=0.5)
        self.at("single blastomere")
        self.play(bl[1].animate.set_fill(PURPLE, 0.8).set_stroke(PURPLE), run_time=0.5)
        c3 = chip("label crest, no graft", PURPLE, 24).move_to(P(cx[2], -2.5))
        self.at("label crest")
        self.play(FadeIn(c3, shift=UP * 0.1), run_time=0.5)
        self.finish()


# -----------------------------------------------------------------------------------------------
class S07Unlocked(SpokenScene):
    """organizer graft (1924); quail-chick chimeras and the neural crest (early 1970s)."""

    def construct(self):
        # left: organizer
        tl = lab("Organizer graft", 30, TEXT, weight=BOLD).move_to(P(-3.4, 3.2))
        don = emb(-5.35, 1.9, 1.9, 1.3, DONOR, 0.15)
        lip = cell(-5.7, 2.1, 0.2, DONOR, 0.9, 0)
        dl = lab("pale donor", 22, DONOR).move_to(P(-5.35, 1.05))
        dar = arr((-4.6, 1.5), (-3.9, 0.7), DONOR, 4, 0.16)
        hostE = emb(-2.5, -0.4, 4.9, 3.8, HOST, 0.12)
        hl = lab("pigmented host", 22, HOST).move_to(P(-2.5, 1.8))
        t1 = lab("Spemann and Mangold, published 1924", 22, GOLD).move_to(P(-3.4, -3.5))
        self.at("In 1924")
        self.play(FadeIn(tl), FadeIn(don), FadeIn(t1), run_time=0.5)
        self.at("dorsal lip")
        self.play(FadeIn(lip), FadeIn(dl), Indicate(lip, color=DONOR, scale_factor=1.8), run_time=0.7)
        self.at("pigmented one")
        graft = lip.copy()
        self.play(FadeIn(hostE), FadeIn(hl), GrowArrow(dar), graft.animate(path_arc=-0.9).move_to(P(-1.6, -0.6)), run_time=1.0)
        prim = Line(P(-3.6, -1.9), P(-3.6, 1.1), color=GREY, stroke_width=8)
        pl = lab("first axis", 22, GREY).move_to(P(-2.85, 0.3))
        sec_nt = Line(P(-1.5, -1.7), P(-1.5, 0.8), color=HOST, stroke_width=12)
        self.at("second body axis")
        self.play(FadeOut(graft), Create(prim), Create(sec_nt), FadeIn(pl), run_time=1.0)
        lh = lab("second neural tube: mostly host cells", 22, HOST).move_to(P(-3.4, -2.75))
        self.at("host tissue")
        self.play(FadeIn(lh), run_time=0.5)

        # right: quail-chick
        tr = lab("Quail-chick chimeras", 30, TEXT, weight=BOLD).move_to(P(3.7, 3.2))
        segs = VGroup(*[Rectangle(width=1.06, height=0.8, stroke_color=GREY, stroke_width=2.5, fill_color=GREY,
                                  fill_opacity=0.12).move_to(P(1.2 + 1.06 * k, 2.1)) for k in range(5)])
        graft_seg = segs[2]
        lt = lab("different levels, different derivatives", 22, GREY).move_to(P(3.85, 1.4))
        t2 = lab("Le Douarin and colleagues, early 1970s", 22, GOLD).move_to(P(3.7, -3.5))
        self.at("early 1970s")
        self.play(FadeIn(tr), FadeIn(segs), FadeIn(lt), FadeIn(t2), run_time=0.6)
        self.at("quail chick chimeras")
        self.play(graft_seg.animate.set_fill(DONOR, 0.7).set_stroke(DONOR), run_time=0.6)
        chips = VGroup(*[chip(t, GREY, 26) for t in ("face skeleton", "ganglia", "adrenal medulla", "gut neurons")])
        chips.arrange(DOWN, buff=0.28).move_to(P(4.7, -1.25))
        dots = VGroup(*[cell(3.9 + 0.2 * (k % 3 - 1), 1.0 - 0.14 * k, 0.09, DONOR, 0.9, 0) for k in range(5)])
        self.at("nuclear mark")
        self.play(FadeIn(dots), run_time=0.4)
        self.at("left the graft")
        route = arr((3.4, 1.2), (2.3, -0.1), DONOR, 5, 0.22)
        self.play(GrowArrow(route), dots.animate.shift(DOWN * 0.95 + LEFT * 1.3), run_time=0.8)
        self.at("which level")
        self.play(FadeIn(chips[0]), run_time=0.3)
        self.at("face skeleton")
        self.play(Indicate(chips[0], color=DONOR), run_time=0.4)
        self.play(*[FadeIn(c) for c in chips[1:]], run_time=0.9)
        self.finish()


# -----------------------------------------------------------------------------------------------
class S08Limb(SpokenScene):
    """extra leg graft: more motor neurons survive; the rule."""

    def construct(self):
        cx = -3.4
        tt = lab("Extra leg graft on a chick embryo", 28, TEXT, weight=BOLD).move_to(P(-3.0, 3.25))
        body = RoundedRectangle(corner_radius=0.8, width=3.0, height=4.4, stroke_color=GREY, stroke_width=3,
                                fill_color=GREY, fill_opacity=0.08).move_to(P(cx, 0.7))
        cord = Line(P(cx, -1.3), P(cx, 2.7), color=GREY, stroke_width=6)
        legL = RoundedRectangle(corner_radius=0.15, width=1.0, height=0.8, stroke_color=GREY, stroke_width=3,
                                fill_color=GREY, fill_opacity=0.3).move_to(P(cx - 2.0, -0.4))
        legR = legL.copy().move_to(P(cx + 2.0, 0.0))
        extra = RoundedRectangle(corner_radius=0.15, width=1.0, height=0.8, stroke_color=DONOR, stroke_width=3,
                                 fill_color=DONOR, fill_opacity=0.5).move_to(P(cx + 2.0, -0.95))
        self.at("In 1976")
        self.play(FadeIn(tt), FadeIn(body), FadeIn(cord), FadeIn(legL), FadeIn(legR), run_time=0.7)
        self.at("extra leg")
        self.play(FadeIn(extra, shift=RIGHT * 0.3), run_time=0.6)
        le = lab("grafted side", 22, DONOR).move_to(P(cx + 1.7, -1.75))
        lu = lab("unoperated side", 22, GREY).move_to(P(cx - 1.7, -1.75))
        self.play(FadeIn(le), FadeIn(lu), run_time=0.4)
        ysn = np.linspace(2.3, -0.7, 8)
        left_n = VGroup(*[cell(cx - 0.8, y, 0.18, YELLOW, 0.9, 0) for y in ysn])
        right_n = VGroup(*[cell(cx + 0.8, y, 0.18, YELLOW, 0.9, 0) for y in ysn])
        ill = lab("dots: illustration, not counts", 26, TEXT).move_to(P(3.8, 2.75))
        self.at("More motor neurons")
        self.play(FadeIn(left_n), FadeIn(right_n), FadeIn(ill), run_time=0.6)
        ax_y = 0.7
        ax = Line(P(1.4, ax_y), P(6.2, ax_y), color=GREY, stroke_width=3)
        ticks = VGroup(); tl = VGroup()
        for v in (0, 10, 20, 30):
            x = 1.4 + 4.8 * v / 30
            ticks.add(Line(P(x, ax_y - 0.1), P(x, ax_y + 0.1), color=GREY, stroke_width=3))
            tl.add(M(str(v), 22, GREY).move_to(P(x, ax_y - 0.4)))
        cap = lab("% more neurons than the unoperated side", 22, GREY).move_to(P(3.8, ax_y - 1.5))
        title2 = lab("motor neurons surviving", 28, TEXT, weight=BOLD).move_to(P(3.8, 3.25))
        zero = Dot(P(1.4, ax_y), radius=0.14, color=YELLOW)
        zl = VGroup(VGroup(lab("day 6, before the loss:", 22, YELLOW), lab("no difference", 22, YELLOW)).arrange(DOWN, aligned_edge=LEFT, buff=0.05).move_to(P(3.0, 2.15)),
                    Line(P(1.4, ax_y + 0.2), P(1.4, 1.85), color=YELLOW, stroke_width=2))
        self.at("counts")
        self.play(FadeIn(title2), Create(ax), FadeIn(ticks), FadeIn(tl), FadeIn(cap), FadeIn(zero), FadeIn(zl), run_time=0.8)
        self.at("before the normal")
        self.play(*[left_n[k].animate.set_fill(YELLOW, 0.12) for k in (1, 3, 5, 6)],
                  *[right_n[k].animate.set_fill(YELLOW, 0.12) for k in (1, 4, 6)], run_time=0.9)
        band = Rectangle(width=4.8 * (27.5 - 11.0) / 30, height=0.5, stroke_width=0, fill_color=YELLOW, fill_opacity=0.85)
        band.move_to(P(1.4 + 4.8 * (11.0 + 27.5) / 2 / 30, ax_y))
        bl = VGroup(lab("cases selected for", 22, YELLOW), lab("vigorous motility", 22, YELLOW)).arrange(DOWN, buff=0.05).move_to(P(5.0, ax_y + 0.6))
        bn = VGroup(M("11.0", 22, YELLOW).move_to(P(1.4 + 4.8 * 11.0 / 30, ax_y - 0.85)), M("27.5", 22, YELLOW).move_to(P(1.4 + 4.8 * 27.5 / 30, ax_y - 0.85)),
                    *[Line(P(1.4 + 4.8 * v / 30, ax_y - 0.55), P(1.4 + 4.8 * v / 30, ax_y - 0.7), color=YELLOW, stroke_width=3) for v in (11.0, 27.5)])
        self.at("vigorous motility")
        self.play(FadeIn(bl), run_time=0.4)
        self.at("the gain was")
        self.play(FadeIn(band, scale=0.5), FadeIn(bn), run_time=0.8)
        self.at("target size")
        self.play(Indicate(extra, color=DONOR, scale_factor=1.3), run_time=0.8)
        t3 = lab("Hollyday and Hamburger, 1976", 22, GOLD).move_to(P(3.8, -1.4))
        self.play(FadeIn(t3), run_time=0.3)
        self.at("touching the cord")
        self.play(Indicate(cord, color=YELLOW), run_time=0.6)
        l1 = T("A graft shows what a tissue does in a new place;", 30, GOLD)
        l2 = T("the marker says whose cells did it.", 30, GOLD)
        txt = VGroup(l1, l2).arrange(DOWN, buff=0.15)
        rbox = RoundedRectangle(corner_radius=0.16, width=txt.width + 0.7, height=txt.height + 0.4, stroke_color=GOLD,
                                stroke_width=2.5, fill_color=GOLD, fill_opacity=0.12)
        box = VGroup(rbox, txt.move_to(rbox)).move_to(P(0, -3.15))
        self.at("A graft shows")
        self.play(FadeIn(box, shift=UP * 0.15), run_time=0.7)
        self.finish()


# -----------------------------------------------------------------------------------------------
class S09End(EndCard):
    LINE = "A graft shows what tissue does; the marker says whose cells."
