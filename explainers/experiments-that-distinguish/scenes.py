"""Experiments that distinguish mechanisms: read the whole distribution  (Biochemistrypedia explainer)

COLOR MAP (one color per concept, whole video)
  ORANGE = cytochrome oxidase / the mitochondrial marker
  BLUE   = acid phosphatase / the lysosome marker
  PURPLE = the unknown enzyme X
  GREY   = protein, tubes, membranes, outlines, the starting mixture
  YELLOW = the thing we are asking about / fraction L / the question mark
  GREEN  = enriched, measured activity (the gauge)
  RED    = not pure
  GOLD   = substrate (the little dots)
  PINK   = detergent
"""
import numpy as np
from bp_style import *  # noqa: F401,F403

PURPLE = "#B58CD9"
ORANGE = "#F29E4C"
PINK = "#E58FC0"

FR = ["N", "M", "L", "P", "S"]
PROT = [15, 20, 5, 20, 40]
CYT = [10, 70, 15, 5, 0]
ACP = [8, 25, 45, 12, 10]
XX = [9, 24, 44, 13, 10]


def rsa(a):
    return [x / p for x, p in zip(a, PROT)]


def bar(x, base, h, w, color, op=0.9):
    r = Rectangle(width=w, height=max(h, 0.03), stroke_width=0, fill_color=color, fill_opacity=op)
    return r.move_to([x, base + max(h, 0.03) / 2, 0])


def tube(x, y, w=1.0, h=1.9, pellet=True):
    t = RoundedRectangle(corner_radius=0.35, width=w, height=h, stroke_color=GREY, stroke_width=4,
                         fill_color=GREY, fill_opacity=0.10).move_to([x, y, 0])
    g = VGroup(t)
    if pellet:
        p = Ellipse(width=w * 0.72, height=0.34, stroke_width=0, fill_color=GREY, fill_opacity=0.85)
        p.move_to([x, y - h / 2 + 0.3, 0])
        g.add(p)
    return g


def rsa_plot(scale=0.5, base=-2.95, xs=(-4.8, -2.4, 0.0, 2.4, 4.8), w=0.6, gap=0.75):
    """Grouped bars of relative specific activity, computed from the lesson's table."""
    out = {"cyt": [], "acp": [], "x": [], "letters": [], "xs": xs, "base": base, "scale": scale}
    for name, arr, col, off in (("cyt", CYT, ORANGE, -gap), ("acp", ACP, BLUE, 0), ("x", XX, PURPLE, gap)):
        for i, v in enumerate(rsa(arr)):
            out[name].append(bar(xs[i] + off, base, v * scale, w, col))
    for i, f in enumerate(FR):
        out["letters"].append(T(f, 30).move_to([xs[i], base - 0.33, 0]))
    out["line"] = Line([xs[0] - 1.2, base, 0], [xs[-1] + 1.2, base, 0], color=GREY, stroke_width=3)
    return out


def val(text, bar_mob, color, size=22):
    return M(text, size, color).next_to(bar_mob, UP, buff=0.1)


def gauge(x, y_base, h, frac, title=None):
    frame = Rectangle(width=0.7, height=h, stroke_color=GREY, stroke_width=4).move_to([x, y_base + h / 2, 0])
    fill = bar(x, y_base, h * frac, 0.7, GREEN, 0.85)
    return frame, fill


# ---------------------------------------------------------------------------------------------
class S00Title(TitleCard):
    LESSON = "Experiments That Distinguish Mechanisms"
    TITLE = "Read the Whole Distribution"


# ---------------------------------------------------------------------------------------------
class S01Pellet(SpokenScene):
    def construct(self):
        circ = Circle(radius=1.5, stroke_color=GREY, stroke_width=5, fill_color=GREY, fill_opacity=0.14)
        circ.move_to(UP * 0.5)
        q = T("?", 110, YELLOW, weight=BOLD).move_to(circ)
        lab = T("pellet named \"mitochondria\"", 34).next_to(circ, DOWN, buff=0.45)
        self.play(FadeIn(circ), FadeIn(lab), run_time=0.7)
        self.play(Write(q), run_time=0.6)
        self.at("really in it")
        self.play(Indicate(q, color=YELLOW, scale_factor=1.3), run_time=1.0)

        self.at("broke rat liver")
        liver = chip("rat liver", GREY, size=34).move_to(UP * 0.5)
        self.play(FadeOut(q), FadeOut(lab), ReplacementTransform(circ, liver), run_time=0.8)

        self.at("five fractions")
        xs = [-4.8, -2.4, 0.0, 2.4, 4.8]
        tubes = VGroup(*[tube(x, 1.5, pellet=(i < 4)) for i, x in enumerate(xs)])
        letters = VGroup(*[T(f, 30).move_to([x, 0.2, 0]) for f, x in zip(FR, xs)])
        self.play(ReplacementTransform(liver, tubes), run_time=0.9)
        self.play(FadeIn(letters, shift=UP * 0.1), run_time=0.5)

        self.at("measured enzymes")
        base = -3.05
        sc = 0.038
        L1 = chip("mitochondrial marker", ORANGE, size=22).move_to([-3.0, 3.1, 0])
        axis = Line([-6.0, base, 0], [6.0, base, 0], color=GREY, stroke_width=3)
        cap = T("percent of each enzyme in each fraction (made-up data)", 22, GREY).move_to([0, -3.38, 0])
        cb = [bar(x - 0.28, base, v * sc, 0.5, ORANGE) for x, v in zip(xs, CYT)]
        self.play(FadeIn(L1), Create(axis), FadeIn(cap), run_time=0.5)
        self.play(LaggedStart(*[GrowFromEdge(b, DOWN) for b in cb], lag_ratio=0.15), run_time=1.4)

        self.at("peaked in one place")
        self.play(Indicate(cb[1], color=ORANGE, scale_factor=1.15), run_time=1.0)

        self.at("acid phosphatase")
        L2 = chip("acid phosphatase", BLUE, size=22).move_to([3.0, 3.1, 0])
        ab = [bar(x + 0.28, base, v * sc, 0.5, BLUE) for x, v in zip(xs, ACP)]
        self.play(FadeIn(L2), run_time=0.4)
        self.play(LaggedStart(*[GrowFromEdge(b, DOWN) for b in ab], lag_ratio=0.15), run_time=1.4)

        self.at("travel with")
        self.play(Indicate(ab[2], color=BLUE, scale_factor=1.12), run_time=1.0)
        self.finish()


# ---------------------------------------------------------------------------------------------
class S02Ratio(SpokenScene):
    def construct(self):
        hdr = T("made-up data for rat liver", 28, GREY).move_to([0, 3.1, 0])
        self.play(FadeIn(hdr), run_time=0.5)

        top = chip("% of the enzyme", BLUE, size=30)
        line = Line(LEFT * 1.9, RIGHT * 1.9, color=TEXT, stroke_width=4)
        bot = chip("% of the protein", GREY, size=30)
        frac = VGroup(top, line, bot).arrange(DOWN, buff=0.2)
        eq = T("=", 44)
        rl = T("relative specific activity", 34, YELLOW)
        formula = VGroup(frac, eq, rl).arrange(RIGHT, buff=0.4).move_to([0, 0.6, 0])
        # lay out all, then show piece by piece
        self.at("percent of an enzyme")
        self.play(FadeIn(top, shift=DOWN * 0.15), run_time=0.5)
        self.at("divide by")
        self.play(Create(line), run_time=0.4)
        self.at("percent of the protein")
        self.play(FadeIn(bot, shift=UP * 0.15), run_time=0.5)
        self.at("relative specific activity")
        self.play(FadeIn(eq), FadeIn(rl, shift=LEFT * 0.2), run_time=0.6)

        self.at("holds")
        base = -2.8
        flab = T("Fraction L", 30, YELLOW).move_to([-3.8, 0.95, 0])
        self.play(formula.animate.scale(0.62).move_to([-3.4, 2.45, 0]), FadeIn(flab), run_time=0.9)
        ax1 = Line([-6.2, base, 0], [-1.2, base, 0], color=GREY, stroke_width=3)
        self.play(Create(ax1), run_time=0.3)

        self.at("acid phosphatase")
        bb = bar(-3.0, base, 45 * 0.05, 0.9, BLUE)
        bl = M("45%", 28, BLUE).next_to(bb, UP, buff=0.12)
        bn = T("acid phosphatase", 22, BLUE).move_to([-3.0, base - 0.35, 0])
        self.play(GrowFromEdge(bb, DOWN), run_time=0.9)
        self.play(FadeIn(bl), FadeIn(bn), run_time=0.4)

        self.at("percent of the protein", nth=1)
        gb = bar(-5.2, base, 5 * 0.05, 0.9, GREY)
        gl = M("5%", 28, GREY).next_to(gb, UP, buff=0.12)
        gn = T("protein", 22, GREY).move_to([-5.2, base - 0.35, 0])
        self.play(GrowFromEdge(gb, DOWN), run_time=0.5)
        self.play(FadeIn(gl), FadeIn(gn), run_time=0.4)

        self.at("over")
        eqn = M("45 ÷ 5", 40).move_to([0.9, 0.9, 0])
        self.play(FadeIn(eqn, shift=RIGHT * 0.2), run_time=0.5)

        self.at("enriched")
        bx = 4.6
        ax2 = Line([3.1, base, 0], [6.1, base, 0], color=GREY, stroke_width=3)
        rb = bar(bx, base, 9.0 * 0.27, 1.2, GREEN)
        ref = DashedLine([3.1, base + 0.27, 0], [6.1, base + 0.27, 0], color=GREY, stroke_width=3)
        one = M("1", 24, GREY).move_to([2.8, base + 0.27, 0])
        note = T("1 = starting mixture", 22, GREY).move_to([bx, base - 0.4, 0])
        eqr = M("= 9.0", 40, GREEN).next_to(eqn, RIGHT, buff=0.2)
        self.play(Create(ax2), Create(ref), FadeIn(one), FadeIn(note), run_time=0.4)
        self.play(GrowFromEdge(rb, DOWN), FadeIn(eqr), run_time=0.9)
        tag = chip("enriched", GREEN, size=28).move_to([bx, 1.7, 0])
        vl = M("9.0", 30, GREEN).next_to(rb, UP, buff=0.1)
        self.play(FadeIn(vl), FadeIn(tag), run_time=0.5)
        self.finish()


# ---------------------------------------------------------------------------------------------
def legend3():
    a = chip("cytochrome oxidase", ORANGE, size=22).move_to([-4.0, 3.1, 0])
    b = chip("acid phosphatase", BLUE, size=22).move_to([0.0, 3.1, 0])
    c = chip("unknown enzyme X", PURPLE, size=22).move_to([4.0, 3.1, 0])
    return a, b, c


class S03Profile(SpokenScene):
    def construct(self):
        P_ = rsa_plot()
        base = P_["base"]
        sc = P_["scale"]
        La, Lb, Lc = legend3()
        axt = T("relative specific activity", 22, GREY).move_to([-4.6, 2.2, 0])
        self.play(Create(P_["line"]), FadeIn(VGroup(*P_["letters"])), FadeIn(axt), run_time=0.8)
        self.at("every fraction")
        self.play(*[Indicate(l, color=YELLOW, scale_factor=1.25) for l in P_["letters"]], run_time=0.8)

        self.at("cytochrome oxidase")
        self.play(FadeIn(La), run_time=0.4)
        self.play(LaggedStart(*[GrowFromEdge(b, DOWN) for b in P_["cyt"]], lag_ratio=0.15), run_time=1.3)
        self.at("peaks in")
        v_m = val("3.5", P_["cyt"][1], ORANGE)
        self.play(FadeIn(v_m), Indicate(P_["cyt"][1], color=ORANGE, scale_factor=1.12), run_time=0.8)

        self.at("acid phosphatase")
        self.play(FadeIn(Lb), run_time=0.4)
        self.play(LaggedStart(*[GrowFromEdge(b, DOWN) for b in P_["acp"]], lag_ratio=0.15), run_time=1.3)
        self.at("peaks in", nth=1)
        v_l = val("9.0", P_["acp"][2], BLUE)
        self.play(FadeIn(v_l), Indicate(P_["acp"][2], color=BLUE, scale_factor=1.08), run_time=0.8)

        self.at("unknown enzyme")
        self.play(FadeIn(Lc), run_time=0.4)
        self.play(LaggedStart(*[GrowFromEdge(b, DOWN) for b in P_["x"]], lag_ratio=0.15), run_time=1.3)
        v_x = val("8.8", P_["x"][2], PURPLE)
        self.play(FadeIn(v_x), run_time=0.4)

        self.at("follows acid phosphatase")
        xl = P_["xs"][2]
        ring = SurroundingRectangle(VGroup(P_["acp"][2], P_["x"][2], v_x, v_l), color=YELLOW, buff=0.12, stroke_width=4)
        self.play(Create(ring), run_time=0.7)

        self.at("does not follow")
        self.play(*[b.animate.set_opacity(0.3) for b in P_["cyt"]], FadeOut(v_m), run_time=0.8)
        self.finish()


# ---------------------------------------------------------------------------------------------
class S04Purity(SpokenScene):
    def construct(self):
        P_ = rsa_plot()
        base = P_["base"]
        La, Lb, Lc = legend3()
        axt = T("relative specific activity", 22, GREY).move_to([-4.6, 2.2, 0])
        v_l = val("9.0", P_["acp"][2], BLUE)
        v_x = val("8.8", P_["x"][2], PURPLE)
        for b in P_["cyt"]:
            b.set_opacity(0.3)
        ring = SurroundingRectangle(VGroup(P_["acp"][2], P_["x"][2], v_x, v_l), color=YELLOW, buff=0.12, stroke_width=4)
        self.add(ring)
        allm = VGroup(P_["line"], *P_["letters"], *P_["cyt"], *P_["acp"], *P_["x"], La, Lb, Lc, axt, v_l, v_x)
        self.add(allm)

        self.at("also carries")
        keep = VGroup(P_["cyt"][2], P_["acp"][2], P_["x"][2], P_["letters"][2], v_l, v_x)
        gone = VGroup(*[m for m in allm if m not in keep.submobjects])
        newline = Line([-3.4, base, 0], [-0.2, base, 0], color=GREY, stroke_width=3)
        pivot = np.array([0.0, base, 0.0])
        P_["cyt"][2].set_opacity(0.9)
        self.play(FadeOut(gone), FadeOut(ring),
                  keep.animate.scale(1.2, about_point=pivot).shift(LEFT * 1.8), run_time=1.0)
        self.add(newline)
        cyt = P_["cyt"][2]
        cl = T("15% of the cell's\ncytochrome oxidase", 22, ORANGE).move_to([-4.9, -1.7, 0])
        ar = Arrow(cl.get_right() + RIGHT * 0.02, [cyt.get_left()[0] - 0.05, -1.7, 0], buff=0.05, color=ORANGE,
                   stroke_width=4, tip_length=0.18)
        self.play(FadeIn(cl), GrowArrow(ar), Indicate(cyt, color=ORANGE, scale_factor=1.1), run_time=0.9)

        self.at("relative specific activity")
        v_c = val("3.0", cyt, ORANGE)
        self.play(FadeIn(v_c), run_time=0.5)

        self.at("acid phosphatase")
        y0 = 1.2
        st = T("all the acid phosphatase", 26, BLUE).move_to([3.6, 2.2, 0])
        r1 = Rectangle(width=2.25, height=0.7, stroke_color=BLUE, stroke_width=3, fill_color=BLUE, fill_opacity=0.7)
        r2 = Rectangle(width=2.75, height=0.7, stroke_color=GREY, stroke_width=3, fill_color=GREY, fill_opacity=0.35)
        r1.move_to([1.0 + 1.125, y0, 0])
        r2.move_to([1.0 + 2.25 + 1.375, y0, 0])
        t1 = T("in L", 24, BLUE).next_to(r1, DOWN, buff=0.15)
        t2 = T("elsewhere", 24, GREY).next_to(r2, DOWN, buff=0.15)
        self.play(FadeIn(st), run_time=0.4)
        self.play(GrowFromEdge(r1, LEFT), GrowFromEdge(r2, LEFT), run_time=0.9)
        self.play(FadeIn(t1), FadeIn(t2), run_time=0.4)

        self.at("enriched in lysosomes")
        tag1 = chip("enriched", GREEN, size=28).move_to([2.2, -1.1, 0])
        self.play(FadeIn(tag1, shift=UP * 0.1), run_time=0.5)
        self.at("not pure")
        tag2 = chip("not pure", RED, size=28).move_to([4.9, -1.1, 0])
        self.play(FadeIn(tag2, shift=UP * 0.1), run_time=0.5)

        self.at("several markers")
        self.play(*[Indicate(m, scale_factor=1.1) for m in (P_["cyt"][2], P_["acp"][2], P_["x"][2])], run_time=1.1)
        self.finish()


# ---------------------------------------------------------------------------------------------
def particle(cx, cy, r=1.25, closed=True):
    if closed:
        return Circle(radius=r, stroke_color=GREY, stroke_width=7).move_to([cx, cy, 0])
    arcs = VGroup()
    for k in range(4):
        a = Arc(radius=r, start_angle=k * PI / 2 + 0.3, angle=PI / 2 - 0.6, arc_center=[cx, cy, 0],
                stroke_color=GREY, stroke_width=7)
        arcs.add(a)
    return arcs


def ghost(text, x, y, color=PURPLE, op=0.45):
    c = chip(text, color, size=26)
    c.set_opacity(op)
    return c.move_to([x, y, 0])


class S05Latency(SpokenScene):
    def construct(self):
        cyL, cyR, cyy = -5.0, 0.7, 0.3
        gL, gR = -2.9, 3.0
        gbase, gh = -2.3, 3.4

        mem = particle(cyL, cyy)
        capL = T("intact particles", 24, GREY).move_to([cyL, -1.75, 0])
        gin = ghost("X?", cyL, cyy)
        self.play(Create(mem), FadeIn(capL), run_time=0.8)

        self.at("inside a particle")
        self.play(FadeIn(gin), run_time=0.4)

        self.at("latency")
        lat = chip("latency", YELLOW, size=30).move_to([-1.5, 3.1, 0])
        self.play(FadeIn(lat, shift=DOWN * 0.1), run_time=0.5)

        self.at("cannot be measured")
        rng = np.random.default_rng(3)
        dots = []
        for ang in (0.5, 1.4, 2.4, 3.5, 4.4, 5.5):
            d = Circle(radius=0.1, stroke_width=0, fill_color=GOLD, fill_opacity=1)
            d.move_to([cyL + 1.75 * np.cos(ang), cyy + 1.55 * np.sin(ang), 0])
            dots.append(d)
        sub = chip("substrate", GOLD, size=22).move_to([-1.5, 1.9, 0])
        self.play(LaggedStart(*[FadeIn(d) for d in dots], lag_ratio=0.1), FadeIn(sub), run_time=0.7)
        self.at("until a membrane")
        self.play(Indicate(mem, color=YELLOW, scale_factor=1.06), run_time=0.9)

        self.at("suppose")
        gfL, fillL = gauge(gL, gbase, gh, 0.10)
        vL = M("10", 30, GREEN).next_to(fillL, UP, buff=0.12)
        act = T("activity measured", 22, GREY).move_to([-0.1, -2.9, 0])
        self.play(Create(gfL), GrowFromEdge(fillL, DOWN), FadeIn(vL), FadeIn(act), run_time=0.8)

        self.at("detergent")
        memR = particle(cyR, cyy)
        capR = T("plus detergent", 24, PINK).move_to([cyR, -1.75, 0])
        xR = chip("X", PURPLE, size=26).move_to([cyR, cyy, 0])
        det = chip("detergent", PINK, size=26).move_to([cyR, 2.4, 0])
        self.play(Create(memR), FadeIn(capR), FadeIn(xR), FadeIn(det, shift=DOWN * 0.2), run_time=0.5)
        broken = particle(cyR, cyy, closed=False)
        dotsR = []
        for ang in (0.5, 1.4, 2.4, 3.5, 4.4, 5.5):
            d = Circle(radius=0.1, stroke_width=0, fill_color=GOLD, fill_opacity=1)
            d.move_to([cyR + 1.75 * np.cos(ang), cyy + 1.55 * np.sin(ang), 0])
            dotsR.append(d)
        self.play(*[FadeIn(d) for d in dotsR], run_time=0.2)
        self.play(FadeOut(memR), FadeIn(broken), run_time=0.3)

        self.at("rises")
        gfR, fillR = gauge(gR, gbase, gh, 1.0)
        fillR0 = bar(gR, gbase, gh * 0.10, 0.7, GREEN, 0.85)
        vR = M("100", 30, GREEN).next_to(fillR, UP, buff=0.12)
        self.play(Create(gfR), FadeIn(fillR0), run_time=0.4)
        ins = [[cyR - 0.7, cyy + 0.5], [cyR + 0.7, cyy + 0.55], [cyR - 0.55, cyy - 0.65], [cyR + 0.6, cyy - 0.6],
               [cyR + 0.05, cyy + 0.8], [cyR + 0.05, cyy - 0.85]]
        self.play(*[d.animate.move_to([p[0], p[1], 0]) for d, p in zip(dotsR, ins)],
                  Transform(fillR0, fillR), FadeIn(vR), run_time=1.2)

        self.at("sealed")
        self.play(*[d.animate(rate_func=there_and_back).shift((mem.get_center() - d.get_center()) * 0.18) for d in dots],
                  Indicate(mem, color=GREY, scale_factor=1.05), run_time=1.2)

        self.at("latent")
        tag = chip("90% latent", YELLOW, size=30).move_to([4.95, 0.3, 0])
        self.play(FadeIn(tag, shift=LEFT * 0.2), run_time=0.5)
        self.at("sits inside")
        self.play(gin.animate.set_opacity(1).become(chip("X", PURPLE, size=26).move_to([cyL, cyy, 0])),
                  run_time=0.6)
        self.finish()


# ---------------------------------------------------------------------------------------------
class S06Rule(SpokenScene):
    def construct(self):
        xc = chip("X", PURPLE, size=34).move_to([-5.0, 3.0, 0])
        ar = Arrow([-4.4, 3.0, 0], [-3.2, 3.0, 0], buff=0.05, color=GREY, stroke_width=5, tip_length=0.22)
        lys = chip("lysosomal", BLUE, size=34).move_to([-1.9, 3.0, 0])
        prov = T("provisional", 26, YELLOW).next_to(lys, DOWN, buff=0.15)
        self.at("provisionally")
        self.play(FadeIn(xc), run_time=0.3)
        self.play(GrowArrow(ar), FadeIn(lys), FadeIn(prov), run_time=0.8)

        self.at("second lysosomal marker")
        b1 = Square(0.34, stroke_color=GREY, stroke_width=3).move_to([-5.9, 1.4, 0])
        t1 = T("a second lysosomal marker tracks X", 24).next_to(b1, RIGHT, buff=0.25)
        t1b = T("on a density gradient", 22, GREY).next_to(t1, DOWN, buff=0.1, aligned_edge=LEFT)
        self.play(FadeIn(b1), FadeIn(t1), FadeIn(t1b), run_time=0.7)
        self.at("images of the protein")
        b2 = Square(0.34, stroke_color=GREY, stroke_width=3).move_to([-5.9, 0.4, 0])
        t2 = T("images of X in intact cells", 24).next_to(b2, RIGHT, buff=0.25)
        self.play(FadeIn(b2), FadeIn(t2), run_time=0.7)

        self.at("shared peak")
        tb = RoundedRectangle(corner_radius=0.5, width=1.8, height=5.3, stroke_color=GREY, stroke_width=4,
                              fill_color=GREY, fill_opacity=0.08).move_to([2.4, -0.4, 0])
        o1 = VGroup(Circle(0.36, stroke_color=TEXT, stroke_width=4, fill_color=TEXT, fill_opacity=0.2),
                    T("1", 26, TEXT)).move_to([1.9, 1.5, 0])
        o2 = VGroup(Square(0.7, stroke_color=TEXT, stroke_width=4, fill_color=TEXT, fill_opacity=0.2),
                    T("2", 26, TEXT)).move_to([2.9, 1.5, 0])
        self.play(Create(tb), FadeIn(o1), FadeIn(o2), run_time=0.7)
        self.at("two organelles")
        self.play(Indicate(o1, color=TEXT), Indicate(o2, color=TEXT), run_time=0.8)
        self.at("sediment together")
        band = Line([1.5, -1.5, 0], [3.3, -1.5, 0], color=YELLOW, stroke_width=6)
        self.play(o1.animate.move_to([1.9, -1.1, 0]), o2.animate.move_to([2.9, -1.1, 0]), run_time=1.0)
        pk = T("one shared peak", 24, YELLOW).move_to([4.85, -1.3, 0])
        self.play(Create(band), FadeIn(pk), run_time=0.5)

        self.at("whole distribution")
        base = -3.1
        xs = [-5.2, -4.2, -3.2, -2.2, -1.2]
        vals = rsa(XX)
        bars = [bar(x, base, v * 0.17, 0.6, PURPLE) for x, v in zip(xs, vals)]
        lets = [T(f, 24, GREY).move_to([x, base - 0.28, 0]) for f, x in zip(FR, xs)]
        ln = Line([-5.8, base, 0], [-0.6, base, 0], color=GREY, stroke_width=3)
        cap = T("X in every fraction", 24, PURPLE).move_to([-3.2, -1.05, 0])
        self.play(Create(ln), FadeIn(cap), *[FadeIn(l) for l in lets], run_time=0.5)
        self.play(LaggedStart(*[GrowFromEdge(b, DOWN) for b in bars], lag_ratio=0.12), run_time=1.0)

        self.at("pellet's name")
        nm = T("a name is not the contents", 26, YELLOW).move_to([-3.2, -0.45, 0])
        self.play(FadeIn(nm), run_time=0.5)
        self.finish()


class S07End(EndCard):
    LINE = "Read the whole distribution; a pellet's name is not its contents."
