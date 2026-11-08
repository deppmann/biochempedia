"""A Middle Gene Reveals Double Crossovers (Biochemistrypedia explainer, Genetics: three-point mapping)

COLOR MAP (one colour per concept, whole film)
  BLUE   = the chromosome (and alleles) carrying the three recessive mutations p q r
  GREEN  = the chromosome (and alleles) carrying the normal + alleles
  YELLOW = a crossover; single-crossover classes and counts
  RED    = double crossovers and their counts
  TEAL   = the middle gene (the one that switches in a double)
  GREY   = tester, parental classes, labels, axes
  TEXT   = totals and neutral text
"""
from bp_style import *  # noqa: F401,F403

L = 9.0
GX = {"q": -3.4, "p": 0.0, "r": 3.4}


def pieces(cx, cy, cuts, cols, L=L, h=0.7, op=0.5):
    xs = [cx - L / 2] + [cx + c for c in cuts] + [cx + L / 2]
    g = VGroup()
    for a, b, c in zip(xs[:-1], xs[1:], cols):
        r = Rectangle(width=b - a, height=h, stroke_color=c, stroke_width=3, fill_color=c, fill_opacity=op)
        r.move_to([(a + b) / 2, cy, 0])
        g.add(r)
    return g


def lab(txt, x, y, size=32):
    return M(txt, size, TEXT).move_to([x, y, 0])


def xmark(x, y_top, y_bot, w=0.28):
    return VGroup(Line([x - w, y_top, 0], [x + w, y_bot, 0], color=YELLOW, stroke_width=7),
                  Line([x + w, y_top, 0], [x - w, y_bot, 0], color=YELLOW, stroke_width=7))


Y_TOP, Y_BOT, Y_G = 2.5, 1.1, -1.2


def homologs(genes):
    """Blue (mutant) and green (normal) chromosomes with alleles written inside."""
    b = pieces(0, Y_TOP, [], [BLUE])
    g = pieces(0, Y_BOT, [], [GREEN])
    labs = VGroup()
    for k in genes:
        labs.add(lab(k if k != "p" else "p", GX[k], Y_TOP), lab("+", GX[k], Y_BOT))
    return b, g, labs


class S00Title(TitleCard):
    LESSON = "Three-Point Crosses: Gene Order and Double Crossovers"
    TITLE = "A Middle Gene Reveals Double Crossovers"


# ---------------------------------------------------------------------------------------------
class S01Cancel(SpokenScene):
    def construct(self):
        b, g, labs = homologs(["q", "r"])
        slot = DashedVMobject(Rectangle(width=L, height=0.9, stroke_color=GREY, stroke_width=3)).move_to([0, Y_G, 0])
        qm = T("?", 44, TEXT).move_to([0, Y_G, 0])
        self.play(FadeIn(b), FadeIn(g), FadeIn(labs), run_time=0.8)
        self.at("How do you count")
        self.play(FadeIn(slot), FadeIn(qm), run_time=0.6)
        x1 = xmark(-1.7, Y_TOP - 0.4, Y_BOT + 0.4)
        gam1 = pieces(0, Y_G, [-1.7], [BLUE, GREEN])
        gl1 = VGroup(lab("q", GX["q"], Y_G), lab("+", GX["r"], Y_G))
        tag1 = T("recombined", 28, YELLOW).move_to([0, Y_G - 1.0, 0])
        self.at("One crossover")
        self.play(Create(x1), run_time=0.6)
        self.play(FadeOut(slot), FadeOut(qm), FadeIn(gam1), FadeIn(gl1), FadeIn(tag1), run_time=0.8)
        x2 = xmark(1.7, Y_TOP - 0.4, Y_BOT + 0.4)
        gam2 = pieces(0, Y_G, [-1.7, 1.7], [BLUE, GREEN, BLUE])
        gl2 = VGroup(lab("q", GX["q"], Y_G), lab("r", GX["r"], Y_G))
        tag2 = T("rearranged twice", 28, YELLOW).move_to([0, Y_G - 1.0, 0])
        self.at("A second crossover")
        self.play(Create(x2), run_time=0.6)
        self.play(ReplacementTransform(gam1, gam2), ReplacementTransform(gl1, gl2),
                  ReplacementTransform(tag1, tag2), run_time=0.9)
        tag3 = T("q r  looks parental", 28, BLUE).move_to([0, Y_G - 1.0, 0])
        self.at("looks parental")
        self.play(ReplacementTransform(tag2, tag3), run_time=0.6)
        self.finish()


# ---------------------------------------------------------------------------------------------
class S02Middle(SpokenScene):
    def construct(self):
        b, g, labs = homologs(["q", "r"])
        x1, x2 = xmark(-1.7, Y_TOP - 0.4, Y_BOT + 0.4), xmark(1.7, Y_TOP - 0.4, Y_BOT + 0.4)
        gam = pieces(0, Y_G, [-1.7, 1.7], [BLUE, GREEN, BLUE])
        gl = VGroup(lab("q", GX["q"], Y_G), lab("r", GX["r"], Y_G))
        self.add(b, g, labs, x1, x2, gam, gl)
        pb, pg = lab("p", 0, Y_TOP), lab("+", 0, Y_BOT)
        ring1 = Circle(radius=0.36, stroke_color=TEAL, stroke_width=5).move_to(pb)
        ring2 = Circle(radius=0.36, stroke_color=TEAL, stroke_width=5).move_to(pg)
        self.at("third gene")
        self.play(FadeIn(pb), FadeIn(pg), Create(ring1), Create(ring2), run_time=0.8)
        mid = lab("+", 0, Y_G)
        ring3 = Circle(radius=0.36, stroke_color=TEAL, stroke_width=5).move_to(mid)
        self.at("middle marker")
        self.play(Indicate(ring1, color=TEAL), Indicate(ring2, color=TEAL), run_time=0.9)
        self.at("double crossover swaps")
        self.play(FadeIn(mid), Create(ring3), run_time=0.8)
        self.at("outer genes")
        self.play(Indicate(gl[0], color=BLUE, scale_factor=1.4), Indicate(gl[1], color=BLUE, scale_factor=1.4), run_time=1.0)
        dbl = T("double crossover", 30, RED).move_to([0, Y_G - 1.05, 0])
        self.at("has switched")
        self.play(Indicate(ring3, color=TEAL, scale_factor=1.5), run_time=0.9)
        self.at("hidden event")
        self.play(FadeIn(dbl, shift=UP * 0.1), run_time=0.6)
        self.finish()


# ---------------------------------------------------------------------------------------------
CLS = [("p q r", 350, GREY), ("+ + +", 342, GREY), ("p q +", 96, YELLOW), ("+ + r", 92, YELLOW),
       ("p + r", 55, YELLOW), ("+ q +", 53, YELLOW), ("+ q r", 7, RED), ("p + +", 5, RED)]
# alphabetical listing as in the lesson: the singles are p q + / + + r (p-r side) etc.; shown as the lesson writes them.
CLS = [("p q r", 350, GREY), ("+ + +", 342, GREY), ("p q +", 96, YELLOW), ("+ + r", 92, YELLOW),
       ("p + r", 55, YELLOW), ("+ q +", 53, YELLOW), ("+ q r", 7, RED), ("p + +", 5, RED)]


class S03Classes(SpokenScene):
    def construct(self):
        mom_b = pieces(-4.3, 2.95, [], [BLUE], L=3.0, h=0.36)
        mom_g = pieces(-4.3, 2.5, [], [GREEN], L=3.0, h=0.36)
        mom_t = VGroup(M("p q r", 22, TEXT).move_to(mom_b), M("+ + +", 22, TEXT).move_to(mom_g))
        tes_a = pieces(1.6, 2.95, [], [GREY], L=3.0, h=0.36)
        tes_b = pieces(1.6, 2.5, [], [GREY], L=3.0, h=0.36)
        tes_t = VGroup(M("p q r", 22, TEXT).move_to(tes_a), M("p q r", 22, TEXT).move_to(tes_b))
        ml = T("female", 24, BLUE).move_to([-4.3, 3.5, 0])
        tl = T("tester", 24, GREY).move_to([1.6, 3.5, 0])
        times = T("x", 36, TEXT).move_to([-1.35, 2.72, 0])
        self.at("A female carries")
        self.play(FadeIn(mom_b), FadeIn(mom_g), FadeIn(mom_t), FadeIn(ml), run_time=0.8)
        self.at("crossed to a tester")
        self.play(FadeIn(times), FadeIn(tes_a), FadeIn(tes_b), FadeIn(tes_t), FadeIn(tl), run_time=0.8)
        base, sc = -1.9, 0.0095
        xs = [-5.25 + 1.5 * i for i in range(8)]
        bars = VGroup(); nums = VGroup(); names = VGroup()
        for (n, v, c), x in zip(CLS, xs):
            r = Rectangle(width=1.1, height=max(v * sc, 0.05), stroke_color=GREY, stroke_width=3,
                          fill_color=GREY, fill_opacity=0.25)
            r.move_to([x, base + max(v * sc, 0.05) / 2, 0])
            bars.add(r)
            nums.add(M(str(v), 26, TEXT).move_to([x, base + max(v * sc, 0.05) + 0.3, 0]))
            names.add(M(n, 24, GREY).move_to([x, base - 0.35, 0]))
        axis = Line([-6.0, base, 0], [6.0, base, 0], color=GREY, stroke_width=3)
        self.at("Sort")
        self.play(Create(axis), *[GrowFromEdge(r, DOWN) for r in bars], FadeIn(nums), FadeIn(names), run_time=1.6)

        def grp(i, j, text, color, y=-2.85):
            a, b = xs[i] - 0.55, xs[j] + 0.55
            ln = Line([a, y + 0.25, 0], [b, y + 0.25, 0], color=color, stroke_width=5)
            t = T(text, 24, color).move_to([(a + b) / 2, y - 0.1, 0])
            return VGroup(ln, t)
        g1, g2, g3 = grp(0, 1, "no crossover", GREY), grp(2, 5, "single crossovers", YELLOW), grp(6, 7, "double crossovers", RED)
        self.at("two biggest")
        self.play(*[b.animate.set_fill(GREY, 0.6) for b in bars[0:2]], FadeIn(g1), run_time=0.8)
        self.at("four in the middle")
        self.play(*[b.animate.set_stroke(YELLOW).set_fill(YELLOW, 0.5) for b in bars[2:6]], FadeIn(g2), run_time=0.8)
        self.at("two smallest")
        self.play(*[b.animate.set_stroke(RED).set_fill(RED, 0.7) for b in bars[6:8]], FadeIn(g3),
                  *[Indicate(nums[k], color=RED, scale_factor=1.4) for k in (6, 7)], run_time=1.0)
        self.finish()


# ---------------------------------------------------------------------------------------------
def gchip(sym, col):
    r = Rectangle(width=1.14, height=1.05, stroke_color=col, stroke_width=3, fill_color=col, fill_opacity=0.45)
    return VGroup(r, M(sym, 46, TEXT).move_to(r))


def row(cx, y, syms):
    """syms: three (symbol, colour) in alphabetical slots p q r. Returns list of chips."""
    chips = []
    for k, (s, c) in enumerate(syms):
        ch = gchip(s, c).move_to([cx + (k - 1) * 1.18, y, 0])
        chips.append(ch)
    return chips


class S04Order(SpokenScene):
    def construct(self):
        B, G_ = BLUE, GREEN
        # left pair: parental p q r vs double + q r ; right pair: parental + + + vs double p + +
        colL = [(("p", B), ("q", B), ("r", B)), (("+", G_), ("q", B), ("r", B))]
        colR = [(("+", G_), ("+", G_), ("+", G_)), (("p", B), ("+", G_), ("+", G_))]
        rows, tags = [], []
        top = T("written in alphabetical order", 28, GREY).move_to([0, 3.0, 0])
        for cx, col, names in ((-3.6, colL, ("parental, 350", "double crossover, 7")),
                               (3.6, colR, ("parental, 342", "double crossover, 5"))):
            for k, (y, syms) in enumerate(zip((1.0, -1.5), col)):
                chips = row(cx, y, syms)
                rows.append(chips)
                tags.append(T(names[k], 24, GREY if k == 0 else RED).move_to([cx, y + 0.9, 0]))
        allchips = VGroup(*[c for r in rows for c in r])
        self.at("Match each rare")
        self.play(FadeIn(top), FadeIn(VGroup(*tags)), FadeIn(allchips), run_time=1.0)
        rings = []
        for r in rows:
            ring = SurroundingRectangle(r[0], color=TEAL, buff=0.08, stroke_width=6, corner_radius=0.05)
            rings.append(ring)
        self.at("differs at")
        self.play(*[Create(x) for x in rings], run_time=0.8)
        self.at("swaps only")
        self.play(Indicate(VGroup(*[r[0] for r in rows[1::2]]), color=TEAL), run_time=0.9)
        # reorder: p and q swap slots in every row; the ring that marks p moves with it
        anims = []
        for r, ring in zip(rows, rings):
            # r = [chip_p, chip_q, chip_r] in alphabetical slots; p goes to the middle slot, q to the left
            anims += [Transform(VGroup(r[0], ring), VGroup(r[0], ring).copy().shift(RIGHT * 1.18), path_arc=-PI),
                      Transform(r[1], r[1].copy().shift(LEFT * 1.18), path_arc=-PI)]
        mapl = T("in map order", 28, TEAL).move_to([0, 3.0, 0])
        self.at("So P is")
        self.play(*anims, run_time=1.4)
        self.at("order is")
        self.play(ReplacementTransform(top, mapl), run_time=0.6)
        self.finish()


# ---------------------------------------------------------------------------------------------
SC = 0.28


def sumrow(parts, size=30):
    g = VGroup(*[M(t, size, c) for t, c in parts]).arrange(RIGHT, buff=0.14)
    return g


def gene_dot(sym, x, y, col=TEXT):
    c = Circle(radius=0.3, stroke_color=col, stroke_width=4, fill_color=BG, fill_opacity=1).move_to([x, y, 0])
    return VGroup(c, M(sym, 28, col).move_to(c))


class S05Distance(SpokenScene):
    def construct(self):
        ly = 1.0
        qx, px, rx = -4.48, -4.48 + 12 * SC, -4.48 + 32 * SC
        line = Line([qx, ly, 0], [rx, ly, 0], color=GREY, stroke_width=5)
        dq, dp, dr = gene_dot("q", qx, ly), gene_dot("p", px, ly, TEAL), gene_dot("r", rx, ly)
        m1, m2 = (qx + px) / 2, (px + rx) / 2
        chp = chip("12 doubles", RED, 32).move_to([(m1 + m2) / 2, 3.0, 0])
        a1 = Arrow(chp.get_bottom() + DOWN * 0.05, [m1, ly + 0.45, 0], color=RED, buff=0.05, stroke_width=5)
        a2 = Arrow(chp.get_bottom() + DOWN * 0.05, [m2, ly + 0.45, 0], color=RED, buff=0.05, stroke_width=5)
        self.play(Create(line), FadeIn(dq), FadeIn(dp), FadeIn(dr), FadeIn(chp, shift=DOWN * 0.1), run_time=0.8)
        self.at("counts in both")
        self.play(GrowArrow(a1), GrowArrow(a2), run_time=0.9)

        def block(mid, a, b, parts, total, tot_text, colr):
            br = BraceBetweenPoints([a, ly - 0.45, 0], [b, ly - 0.45, 0], direction=DOWN, color=GREY)
            br.set_stroke(width=2)
            r1 = sumrow(parts).move_to([mid, -0.2, 0])
            r2 = M(total, 28, TEXT).move_to([mid, -0.95, 0])
            r3 = M(tot_text, 44, colr).move_to([mid, -1.85, 0])
            return br, r1, r2, r3
        b1 = block(m1, qx, px, [("53", YELLOW), ("+", TEXT), ("55", YELLOW), ("+", TEXT), ("12", RED)],
                   "= 120 / 1,000", "12.0 cM", TEXT)
        b2 = block(m2, px, rx, [("96", YELLOW), ("+", TEXT), ("92", YELLOW), ("+", TEXT), ("12", RED)],
                   "= 200 / 1,000", "20.0 cM", TEXT)
        self.at("From Q to P")
        self.play(Create(b1[0]), FadeIn(b1[1]), run_time=0.8)
        self.at("make 120")
        self.play(FadeIn(b1[2]), run_time=0.5)
        self.at("That is")
        self.play(FadeIn(b1[3], shift=UP * 0.1), run_time=0.5)
        self.at("From P to R")
        self.play(Create(b2[0]), FadeIn(b2[1]), run_time=0.8)
        self.at("make 200")
        self.play(FadeIn(b2[2]), run_time=0.5)
        self.at("or 20")
        self.play(FadeIn(b2[3], shift=UP * 0.1), run_time=0.5)
        tot = M("q to r:  12.0 + 20.0 = 32.0 cM", 36, TEXT).move_to([0, -3.0, 0])
        self.at("Together")
        self.play(FadeOut(chp), FadeOut(a1), FadeOut(a2), FadeIn(tot, shift=UP * 0.1), run_time=0.9)
        self.finish()


# ---------------------------------------------------------------------------------------------
class S06Twopoint(SpokenScene):
    def construct(self):
        x0 = -4.6
        wy, wd = 29.6 * SC, 2.4 * SC
        ya, yb = 1.4, -1.0
        la = T("map distance with the middle gene", 26, TEXT).move_to([x0, ya + 0.9, 0], aligned_edge=LEFT)
        la.align_to([x0, 0, 0], LEFT)
        A_y = Rectangle(width=wy, height=0.9, stroke_color=YELLOW, stroke_width=3, fill_color=YELLOW, fill_opacity=0.5)
        A_y.move_to([x0 + wy / 2, ya, 0])
        A_r = Rectangle(width=wd, height=0.9, stroke_color=RED, stroke_width=3, fill_color=RED, fill_opacity=0.7)
        A_r.move_to([x0 + wy + wd / 2, ya, 0])
        na = M("32.0 cM", 30, TEXT).move_to([x0 + wy + wd + 1.0, ya, 0])
        self.play(FadeIn(la), GrowFromEdge(A_y, LEFT), GrowFromEdge(A_r, LEFT), FadeIn(na), run_time=1.0)
        lb = T("q and r alone", 26, TEXT).move_to([x0, yb + 0.9, 0])
        lb.align_to([x0, 0, 0], LEFT)
        ghost = DashedVMobject(Rectangle(width=wd, height=0.9, stroke_color=RED, stroke_width=4)).move_to([x0 + wy + wd / 2, yb, 0])
        self.at("only Q and R")
        self.play(FadeIn(lb), run_time=0.6)
        self.at("parental combinations")
        self.play(Indicate(A_r, color=RED, scale_factor=1.3), run_time=0.8)
        self.at("drop out")
        self.play(FadeIn(ghost), Create(Cross(ghost, stroke_color=RED, stroke_width=6, scale_factor=0.6)), run_time=0.8)
        B_y = Rectangle(width=wy, height=0.9, stroke_color=YELLOW, stroke_width=3, fill_color=YELLOW, fill_opacity=0.5)
        B_y.move_to([x0 + wy / 2, yb, 0])
        nb = M("296 / 1,000 = 29.6%", 30, TEXT).move_to([x0 + wy / 2, yb - 1.0, 0])
        self.at("Only the")
        self.play(GrowFromEdge(B_y, LEFT), run_time=1.0)
        self.at("which gives")
        self.play(FadeIn(nb, shift=UP * 0.1), run_time=0.6)
        gap = BraceBetweenPoints([x0 + wy, yb + 0.55, 0], [x0 + wy + wd, yb + 0.55, 0], direction=UP, color=RED)
        gl = M("2.4", 30, RED).next_to(gap, UP, buff=0.1)
        self.at("short")
        self.play(Create(gap), FadeIn(gl), run_time=0.8)
        self.at("counted once")
        self.play(Indicate(A_r, color=RED, scale_factor=1.4), Indicate(ghost, color=RED), run_time=1.0)
        self.finish()


class S07End(EndCard):
    LINE = "Count every double crossover in both intervals."
