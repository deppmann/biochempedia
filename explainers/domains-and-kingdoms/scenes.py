"""Domains and kingdoms: sort life by asking the right questions  (Biochemistrypedia explainer)

COLOR MAP (one color per concept, whole film)
  BLUE   = Bacteria (domain, and bacterial evidence)
  PURPLE = Archaea (domain, and archaeal evidence)
  GREEN  = Eukarya and its kingdoms, eukaryote cells
  YELLOW = the question being asked / the nucleus
  TEAL   = ribosomal RNA sequence evidence
  ORANGE = cell wall
  PINK   = how it gets food (autotroph, decomposer, ingester)
  RED    = a limit (a key only sorts what is built into it)
  GREY   = outlines, neutral things, the prokaryote cell outline
"""
import numpy as np
from bp_style import *  # noqa: F401,F403

PURPLE = "#B58CD9"
ORANGE = "#F29E4C"
PINK = "#E88FB4"


def bchip(text, color=BLUE, size=26, **kw):
    c = chip(text, color, size=size, **kw)
    back = RoundedRectangle(corner_radius=0.14, width=c[0].width, height=c[0].height, stroke_width=0,
                            fill_color=BG, fill_opacity=1).move_to(c[0])
    return VGroup(back, *c)


def arr(a, b, color=GREY, w=5, tip=0.22):
    return Arrow(a, b, buff=0.08, color=color, stroke_width=w, tip_length=tip,
                 max_tip_length_to_length_ratio=0.45, max_stroke_width_to_length_ratio=12)


def dna_bar(w=1.2):
    bar = RoundedRectangle(corner_radius=0.06, width=w, height=0.16, stroke_color=TEXT, stroke_width=2,
                           fill_color=TEXT, fill_opacity=0.85)
    t = T("DNA", 22, TEXT).next_to(bar, DOWN, buff=0.1)
    return VGroup(bar, t)


def cell(r, color, pos, wall=False):
    c = Circle(radius=r, stroke_color=color, stroke_width=4, fill_color=color, fill_opacity=0.10).move_to(pos)
    if wall:
        w = Circle(radius=r * 1.3, stroke_color=ORANGE, stroke_width=4).move_to(pos)
        return VGroup(w, c)
    return VGroup(c)


class S00Title(TitleCard):
    LESSON = "Domains and kingdoms"
    TITLE = "Sort Life by Asking the Right Questions"


# ---------------------------------------------------------------------------------------------
class S01Pond(SpokenScene):
    def construct(self):
        title = T("A drop of pond water", 36, font=TITLE_FONT).move_to([0, 3.1, 0])
        drop = Circle(radius=2.85, stroke_color=GREY, stroke_width=4, fill_color=GREY, fill_opacity=0.08).move_to([0, -0.35, 0])
        self.at("pond water")
        self.play(Write(title), Create(drop), run_time=1.2)

        dom = [bchip("Bacteria", BLUE, 30).move_to([5.0, 1.4, 0]),
               bchip("Archaea", PURPLE, 30).move_to([5.0, -0.4, 0]),
               bchip("Eukarya", GREEN, 30).move_to([5.0, -2.2, 0])]
        dlab = T("domains", 26, GREY).move_to([5.0, 2.5, 0])
        self.at("all three domains")
        self.play(FadeIn(dlab), run_time=0.3)
        for d in dom:
            self.play(FadeIn(d, shift=LEFT * 0.2), run_time=0.35)
        self.at("largest group")
        self.play(*[Indicate(d, color=YELLOW, scale_factor=1.12) for d in dom], run_time=0.9)

        alg = Ellipse(width=1.3, height=0.8, stroke_color=GREEN, stroke_width=3, fill_color=GREEN, fill_opacity=0.25).move_to([-1.0, 0.7, 0])
        alg_l = T("algae", 24, TEXT).next_to(alg, DOWN, buff=0.1)
        amo = Ellipse(width=1.2, height=0.9, stroke_color=GREEN, stroke_width=3, fill_color=GREEN, fill_opacity=0.25).rotate(0.5).move_to([1.1, 0.5, 0])
        amo_l = T("amoeba", 24, TEXT).next_to(amo, DOWN, buff=0.1)
        ani = RoundedRectangle(corner_radius=0.2, width=1.3, height=0.6, stroke_color=GREEN, stroke_width=3, fill_color=GREEN, fill_opacity=0.25).move_to([-0.9, -1.4, 0])
        ani_l = T("tiny animals", 24, TEXT).next_to(ani, DOWN, buff=0.1)
        self.at("You may see")
        for s, l in ((alg, alg_l), (amo, amo_l), (ani, ani_l)):
            self.play(FadeIn(s, scale=0.8), FadeIn(l), run_time=0.5)
        pts = [[1.0, -1.1], [1.6, -1.7], [0.3, -2.0], [1.9, -0.6], [-0.2, -0.3], [2.0, -1.2], [0.9, -2.1]]
        dots = VGroup(*[Dot([x, y, 0], radius=0.07, color=TEXT) for x, y in pts])
        sp = T("specks", 24, TEXT).move_to([1.2, -2.5, 0])
        self.at("specks")
        self.play(FadeIn(dots, lag_ratio=0.15), FadeIn(sp), run_time=0.8)

        q = VGroup(T("Which", 34, YELLOW), T("questions?", 34, YELLOW), T("In what", 34, YELLOW), T("order?", 34, YELLOW)).arrange(DOWN, buff=0.18, aligned_edge=LEFT)
        q.move_to([-5.0, -0.3, 0])
        self.at("sort living things")
        self.play(FadeIn(q, shift=RIGHT * 0.2), run_time=0.6)
        self.finish()


# ---------------------------------------------------------------------------------------------
class S02Nucleus(SpokenScene):
    def construct(self):
        head = T("Does it have a nucleus?", 40, YELLOW, weight=BOLD).move_to([0, 3.1, 0])
        self.at("first question")
        self.play(Write(head), run_time=1.0)

        # eukaryote cell (left)
        L, R = np.array([-3.3, 0.35, 0]), np.array([3.3, 0.35, 0])
        ec = cell(1.9, GREEN, L)
        nuc = RoundedRectangle(corner_radius=0.2, width=2.3, height=1.5, stroke_color=YELLOW, stroke_width=4,
                               fill_color=YELLOW, fill_opacity=0.12).move_to(L)
        nuc_l = T("nucleus", 26, YELLOW).move_to(L + UP * 0.38)
        edna = dna_bar(1.2).move_to(L + DOWN * 0.15)
        self.at("wrapped in membrane")
        self.play(Create(ec), run_time=0.6)
        self.play(Create(nuc), FadeIn(nuc_l), run_time=0.7)
        self.play(FadeIn(edna), run_time=0.4)

        pc = cell(1.9, GREY, R)
        pdna = dna_bar(1.2).move_to(R)
        elab = T("eukaryote", 30, GREEN, weight=BOLD).move_to(L + DOWN * 2.35)
        plab = T("prokaryote", 30, TEXT, weight=BOLD).move_to(R + DOWN * 2.35)
        nolab = T("no nucleus", 26, RED).move_to(R + UP * 0.9)
        self.at("with a nucleus")
        self.play(FadeIn(elab), run_time=0.4)
        self.at("have no nucleus")
        self.play(Create(pc), FadeIn(pdna), run_time=0.7)
        self.play(FadeIn(plab), FadeIn(nolab), run_time=0.5)

        b = bchip("Bacteria", BLUE, 28).move_to([1.6, -3.1, 0])
        a = bchip("Archaea", PURPLE, 28).move_to([4.7, -3.1, 0])
        e = bchip("Eukarya", GREEN, 28).move_to([-3.3, -3.1, 0])
        self.at("Bacteria and")
        self.play(FadeIn(b, shift=UP * 0.2), FadeIn(a, shift=UP * 0.2), run_time=0.6)
        self.at("are prokaryotes")
        self.play(Indicate(plab, color=YELLOW), run_time=0.7)
        self.at("Eukarya are")
        self.play(FadeIn(e, shift=UP * 0.2), run_time=0.6)
        self.finish()


# ---------------------------------------------------------------------------------------------
class S03Evidence(SpokenScene):
    def construct(self):
        xl, xb, xa = -4.8, -0.4, 4.6
        b = cell(1.15, BLUE, [xb, 1.9, 0])
        a = cell(1.15, PURPLE, [xa, 1.9, 0])
        bl = T("Bacteria", 26, BLUE).move_to([xb, 1.9, 0])
        al = T("Archaea", 26, PURPLE).move_to([xa, 1.9, 0])
        micro = VGroup(T("under a light", 26, GREY), T("microscope", 26, GREY)).arrange(DOWN, buff=0.1).move_to([xl, 1.9, 0])
        alike = T("look alike", 28, YELLOW, weight=BOLD).move_to([(xb + xa) / 2, 1.9, 0])
        self.at("look alike")
        self.play(Create(b), Create(a), FadeIn(bl), FadeIn(al), run_time=0.8)
        self.play(FadeIn(micro), FadeIn(alike), run_time=0.5)

        # row 1: RNA
        y1, y2 = -0.2, -1.5
        r1 = T("rRNA sequence", 28, TEAL, weight=BOLD).move_to([xl, y1, 0])
        r1b = bchip("bacterial pattern", BLUE, 24).move_to([xb, y1, 0])
        r1a = bchip("archaeal pattern", PURPLE, 24).move_to([xa, y1, 0])
        self.at("ribosomal")
        self.play(FadeIn(r1, shift=RIGHT * 0.2), run_time=0.5)
        self.at("Its sequence differs")
        self.play(FadeIn(r1b, shift=UP * 0.15), run_time=0.5)
        self.play(FadeIn(r1a, shift=UP * 0.15), run_time=0.5)

        r2 = T("cell wall", 28, ORANGE, weight=BOLD).move_to([xl, y2, 0])
        self.at("Another is the cell wall")
        self.play(FadeIn(r2, shift=RIGHT * 0.2), run_time=0.5)
        wall_b = Circle(radius=1.15 * 1.28, stroke_color=ORANGE, stroke_width=4).move_to([xb, 1.9, 0])
        wall_a = Circle(radius=1.15 * 1.28, stroke_color=ORANGE, stroke_width=4).move_to([xa, 1.9, 0])
        r2b = bchip("peptidoglycan (most)", ORANGE, 24).move_to([xb, y2, 0])
        r2a = bchip("no peptidoglycan", ORANGE, 24).move_to([xa, y2, 0])
        self.at("Most bacteria")
        self.play(FadeIn(r2b, shift=UP * 0.15), Create(wall_b), run_time=0.6)
        self.at("Archaea walls")
        self.play(FadeIn(r2a, shift=UP * 0.15), Create(wall_a), run_time=0.6)

        end = T("Only sequence or chemical evidence tells them apart", 30, YELLOW, weight=BOLD)
        fit(end, max_w=12)
        end.move_to([0, -3.0, 0])
        self.at("Only sequence")
        self.play(FadeIn(end, shift=UP * 0.15), run_time=0.7)
        self.finish()


# ---------------------------------------------------------------------------------------------
class S04Kingdoms(SpokenScene):
    def construct(self):
        top = bchip("Eukarya: has a nucleus", GREEN, 28).move_to([0, 2.9, 0])
        self.at("cell with a nucleus")
        self.play(FadeIn(top, shift=DOWN * 0.15), run_time=0.7)

        xs = [-4.8, -1.6, 1.6, 4.8]
        names = ["Plants", "Fungi", "Animals", "Protists"]
        chips = [bchip(n, GREEN, 30).move_to([x, 1.4, 0]) for x, n in zip(xs, names)]
        for ch in chips:
            ch.shift(UP * (1.4 + 0.37 - ch[1].get_top()[1]))
        lines = [Line(top.get_bottom(), c.get_top(), color=GREEN, stroke_width=3) for c in chips]
        klab = T("four kingdoms", 26, GREY).move_to([4.3, 2.9, 0])
        self.at("four kingdoms")
        self.play(*[Create(l) for l in lines], run_time=0.5)
        self.play(*[FadeIn(c, shift=DOWN * 0.15) for c in chips], FadeIn(klab), run_time=0.6)
        self.at("rank just below domain")
        self.play(Indicate(klab, color=YELLOW, scale_factor=1.15), run_time=0.8)

        def icons(x, n, wall):
            g = VGroup()
            for i in range(n):
                g.add(cell(0.28, GREEN, [x + (i - (n - 1) / 2) * 0.95, 0.15, 0], wall=wall))
            return g

        def lab(text, x, y, color=TEXT, size=24):
            return T(text, size, color).move_to([x, y, 0])

        # plants
        pi = icons(xs[0], 3, True)
        p1, p2, p3 = lab("many cells", xs[0], -0.55), lab("cellulose wall", xs[0], -1.1, ORANGE), lab("autotroph (most)", xs[0], -1.65, PINK)
        self.at("Plants have")
        self.play(Create(pi), FadeIn(p1), run_time=0.6)
        self.at("cellulose walls")
        self.play(FadeIn(p2), run_time=0.4)
        self.at("autotrophs")
        self.play(FadeIn(p3), run_time=0.4)
        d1 = lab("makes its own food", xs[0], -2.2, PINK, 22)
        self.at("make their own food")
        self.play(FadeIn(d1), run_time=0.4)

        # fungi
        fi = icons(xs[1], 3, True)
        f1, f2, f3 = lab("chitin wall", xs[1], -0.55, ORANGE), lab("many decomposers", xs[1], -1.65, PINK), lab("absorbs food", xs[1], -1.1, PINK)
        self.at("Fungi have")
        self.play(Create(fi), FadeIn(f1), run_time=0.6)
        self.at("absorb their food")
        self.play(FadeIn(f3), run_time=0.4)
        self.at("many are decomposers")
        self.play(FadeIn(f2), run_time=0.4)

        # animals
        ai = icons(xs[2], 3, False)
        a1, a2, a3 = lab("many cells", xs[2], -0.55), lab("no wall", xs[2], -1.1), lab("ingester", xs[2], -1.65, PINK)
        self.at("Animals have")
        self.play(Create(ai), FadeIn(a1), run_time=0.6)
        self.at("no walls")
        self.play(FadeIn(a2), run_time=0.4)
        self.at("which take food")
        self.play(FadeIn(a3), run_time=0.4)
        a4 = lab("takes food inside", xs[2], -2.2, PINK, 22)
        self.at("inside the body")
        self.play(FadeIn(a4), run_time=0.4)

        # protists
        qi = icons(xs[3], 1, False)
        q1, q2 = lab("any other eukaryote", xs[3], -0.55), lab("single cell or alga", xs[3], -1.1)
        self.at("Any other eukaryote")
        self.play(Create(qi), FadeIn(q1), run_time=0.6)
        self.at("such as kelp")
        self.play(FadeIn(q2), run_time=0.4)
        qw = Circle(radius=0.28 * 1.3, stroke_color=ORANGE, stroke_width=4).move_to([xs[3], 0.15, 0])
        qw = DashedVMobject(qw, num_dashes=12)
        q3 = lab("some have walls,", xs[3], -1.65, ORANGE, 22)
        q4 = lab("some do not", xs[3], -2.1, ORANGE, 22)
        self.at("is a protist")
        self.play(Create(qw), FadeIn(q3), FadeIn(q4), run_time=0.5)
        self.play(Indicate(chips[3], color=YELLOW, scale_factor=1.15), run_time=0.7)
        self.finish()


# ---------------------------------------------------------------------------------------------
class S05Key(SpokenScene):
    def construct(self):
        head = T("dichotomous key", 34, YELLOW, weight=BOLD).move_to([0, 3.2, 0])
        self.at("dichotomous key")
        self.play(Write(head), run_time=0.6)

        qx, ox = -4.3, -0.3
        ys = [2.3, 0.7, -0.9, -2.4]
        q1 = bchip("Nucleus?", YELLOW, 26).move_to([qx, ys[0], 0])
        q2 = bchip("Plant traits?", YELLOW, 26).move_to([qx, ys[1], 0])
        q3 = bchip("Fungus traits?", YELLOW, 26).move_to([qx, ys[2], 0])
        q4 = bchip("Animal traits?", YELLOW, 26).move_to([qx, ys[3], 0])
        self.play(FadeIn(q1), run_time=0.3)

        # no nucleus branch
        o1 = bchip("sequence or wall chemistry", TEAL, 24).move_to([ox + 0.4, ys[0], 0])
        a1 = arr(q1.get_right(), o1.get_left(), GREY)
        n1 = T("no", 24, GREY).next_to(a1, UP, buff=0.05)
        # yes goes down
        d1 = arr(q1.get_bottom(), q2.get_top(), GREY)
        y1 = T("yes", 24, GREY).next_to(d1, RIGHT, buff=0.1)
        self.play(GrowArrow(a1), FadeIn(n1), FadeIn(o1), run_time=0.3)
        self.play(GrowArrow(d1), FadeIn(y1), FadeIn(q2), run_time=0.3)
        pr = [bchip("archaebacteria", PURPLE, 24).move_to([4.2, ys[0] + 0.45, 0]),
              bchip("eubacteria", BLUE, 24).move_to([4.2, ys[0] - 0.45, 0])]
        pa = [arr(o1.get_right(), p.get_left(), GREY, w=3, tip=0.16) for p in pr]
        self.play(*[GrowArrow(x) for x in pa], *[FadeIn(p, shift=RIGHT * 0.15) for p in pr], run_time=0.3)
        stop = bchip("stop: looks cannot decide", RED, 22).move_to([4.2, 0.95, 0])
        sa = arr(o1.get_bottom() + RIGHT * 1.2, stop.get_left(), RED, w=3, tip=0.16)
        self.play(GrowArrow(sa), FadeIn(stop, shift=RIGHT * 0.15), run_time=0.3)

        res = []
        def step(q, qprev_arrow_target, y, name):
            o = bchip(name, GREEN, 26).move_to([ox, y, 0])
            a = arr(q.get_right(), o.get_left(), GREY)
            t = T("yes", 24, GREY).next_to(a, UP, buff=0.05)
            return o, a, t
        o2, a2, t2 = step(q2, None, ys[1], "plants")
        o3, a3, t3 = step(q3, None, ys[2], "fungi")
        o4, a4, t4 = step(q4, None, ys[3], "animals")
        self.play(GrowArrow(a2), FadeIn(t2), FadeIn(o2), run_time=0.3)
        d2 = arr(q2.get_bottom(), q3.get_top(), GREY); n2 = T("no", 24, GREY).next_to(d2, RIGHT, buff=0.1)
        self.play(GrowArrow(d2), FadeIn(n2), FadeIn(q3), run_time=0.3)
        self.play(GrowArrow(a3), FadeIn(t3), FadeIn(o3), run_time=0.3)
        d3 = arr(q3.get_bottom(), q4.get_top(), GREY); n3 = T("no", 24, GREY).next_to(d3, RIGHT, buff=0.1)
        self.play(GrowArrow(d3), FadeIn(n3), FadeIn(q4), run_time=0.3)
        self.play(GrowArrow(a4), FadeIn(t4), FadeIn(o4), run_time=0.3)
        # protists: elbow below animals row
        p = bchip("protists", GREEN, 26).move_to([3.6, ys[3], 0])
        elbow = VGroup(Line(q4.get_bottom(), [qx, -3.3, 0], color=GREY, stroke_width=5),
                       Line([qx, -3.3, 0], [3.6, -3.3, 0], color=GREY, stroke_width=5),
                       arr([3.6, -3.3, 0], p.get_bottom(), GREY))
        n4 = T("no: any other", 22, GREY).move_to([1.6, -3.05, 0])
        self.play(Create(elbow), FadeIn(n4), FadeIn(p), run_time=0.3)

        lim = T("A key only sorts what was built into it", 26, RED, weight=BOLD)
        lim = VGroup(lim).move_to([3.4, -0.3, 0])
        lim_t = T("A key only sorts", 26, RED, weight=BOLD)
        lim_u = T("what was built into it", 26, RED, weight=BOLD)
        limg = VGroup(lim_t, lim_u).arrange(DOWN, buff=0.12).move_to([3.5, -0.5, 0])
        self.at("A key works only")
        self.play(FadeIn(limg, shift=LEFT * 0.2), run_time=0.7)
        self.at("two part name")
        allm = Group(*self.mobjects)
        self.play(FadeOut(allm), run_time=0.6)

        g = T("Callinectes", 64, TEXT, font=TITLE_FONT, slant=ITALIC)
        s = T("sapidus", 64, TEXT, font=TITLE_FONT, slant=ITALIC)
        nm = VGroup(g, s).arrange(RIGHT, buff=0.5).move_to([0, 0.7, 0])
        crab = T("the blue crab", 28, GREY).move_to([0, 2.3, 0])
        self.play(FadeIn(crab), run_time=0.3)
        gl = T("genus: capital letter", 28, YELLOW, weight=BOLD).next_to(g, DOWN, buff=0.7)
        sl = T("epithet: lower case", 28, GREEN, weight=BOLD).next_to(s, DOWN, buff=0.7)
        gl.set_x(g.get_center()[0]); sl.set_x(s.get_center()[0])
        gb = Line(g.get_bottom() + DOWN * 0.15, gl.get_top() + UP * 0.1, color=YELLOW, stroke_width=3)
        sb = Line(s.get_bottom() + DOWN * 0.15, sl.get_top() + UP * 0.1, color=GREEN, stroke_width=3)
        self.at("genus comes first")
        self.play(Write(g), run_time=0.9)
        self.play(Create(gb), FadeIn(gl), run_time=0.5)
        self.at("epithet comes second")
        self.play(Write(s), run_time=0.8)
        self.play(Create(sb), FadeIn(sl), run_time=0.5)
        self.at("blue crab")
        self.play(Indicate(crab, color=YELLOW), run_time=0.7)
        self.finish()


# ---------------------------------------------------------------------------------------------
class S06Answer(SpokenScene):
    def construct(self):
        q = VGroup(T("How can we classify an organism", 34, YELLOW, weight=BOLD),
                   T("we have never seen before?", 34, YELLOW, weight=BOLD)).arrange(DOWN, buff=0.12).move_to([0, 3.0, 0])
        self.at("classify an organism")
        self.play(FadeIn(q, shift=DOWN * 0.15), run_time=0.8)

        s1 = VGroup(T("1", 34, YELLOW, weight=BOLD), T("Ask the trait questions in order", 32)).arrange(RIGHT, buff=0.3)
        s2 = VGroup(T("2", 34, YELLOW, weight=BOLD), T("If looks are not enough, check", 32), ).arrange(RIGHT, buff=0.3)
        s2b = T("sequence or chemical evidence", 32, TEAL, weight=BOLD)
        s1.move_to([0, 1.5, 0])
        s2.move_to([0, 0.7, 0]); s2.set_x(s1.get_left()[0] + s2.width / 2)
        s2b.next_to(s2, DOWN, buff=0.15, aligned_edge=LEFT).shift(RIGHT * 0.55)
        s1.set_x(s2.get_center()[0] - s2.width / 2 + s1.width / 2)
        self.at("Ask the trait questions")
        self.play(FadeIn(s1, shift=RIGHT * 0.2), run_time=0.7)
        self.at("looks are not enough")
        self.play(FadeIn(s2, shift=RIGHT * 0.2), run_time=0.6)
        self.play(FadeIn(s2b), run_time=0.5)

        root = np.array([0, -2.55, 0])
        xs = [-3.8, 0, 3.8]
        ends = [np.array([x, -1.15, 0]) for x in xs]
        chips = [bchip("Bacteria", BLUE, 28).move_to(ends[0]), bchip("Archaea", PURPLE, 28).move_to(ends[1]),
                 bchip("Eukarya", GREEN, 28).move_to(ends[2])]
        br = [Line(root, c.get_bottom() + DOWN * 0.05, color=GREY, stroke_width=5) for c in chips]
        note = T("one tree: branches show relatedness, not rank", 28, TEXT)
        fit(note, max_w=12)
        note.move_to([0, -3.15, 0])
        self.at("three domains")
        self.play(*[Create(b) for b in br], run_time=0.8)
        self.play(*[FadeIn(c, shift=UP * 0.15) for c in chips], run_time=0.6)
        self.at("Branches show")
        self.play(FadeIn(note), run_time=0.6)
        self.finish()


class S07End(EndCard):
    LINE = "Ask the trait questions in order, then check sequence or chemical evidence."
