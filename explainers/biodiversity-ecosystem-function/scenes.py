"""Biodiversity and ecosystem function: splitting a mixture's extra yield  (Biochemistrypedia explainer)

Timed to the SPOKEN words: every self.at("...") cue waits for that phrase in audio/words.json.
Every number on screen is the lesson's worked problem (M_A 400, M_B 100, Y_A 300, Y_B 100 g dry
biomass per square metre, sown in equal proportions). Bars are drawn to scale from those numbers.

COLOR MAP (one color per concept, whole video)
  BLUE   = species A
  ORANGE = species B
  GREY   = the expected yield / expected relative yield (the benchmark), axes, generic species
  GOLD   = the net effect (observed minus expected)
  GREEN  = complementarity (and the gain in relative yield, mean of which it uses)
  RED    = selection
  TEXT   = the best monoculture line and plain labels
"""
import numpy as np
from bp_style import *  # noqa: F401,F403

ORANGE = "#F29E4C"
BASE = -2.8          # y of the axis baseline
K = 0.011            # units per g/m2 : 400 -> 4.4
UNIT = "grams dry biomass per m²"
XA, XB, XM, BW = -3.8, -1.4, 1.5, 1.5


def hbar(x, v, color, k=K, w=BW, op=0.45):
    r = Rectangle(width=w, height=v * k, stroke_color=color, stroke_width=3, fill_color=color, fill_opacity=op)
    return r.move_to([x, BASE + v * k / 2, 0])


def side_label(word, val, y, color, x=5.2, vs=30):
    return VGroup(T(word, 26, color), M(val, vs, color)).arrange(DOWN, buff=0.08).move_to([x, y, 0])


def vlabel(text, mob, color=TEXT, size=28):
    return M(text, size, color).next_to(mob, UP, buff=0.12)


def axis(x0=-4.9, x1=2.5):
    return Line([x0, BASE, 0], [x1, BASE, 0], color=GREY, stroke_width=3)


def dashed(y, x0=-4.9, x1=2.5, color=GREY):
    return DashedLine([x0, y, 0], [x1, y, 0], color=color, stroke_width=3, dash_length=0.15)


def yy(v, k=K):
    return BASE + v * k


def chart(full=True):
    """Bars A alone 400, B alone 100, mixture (A 300 + B 100). Returns a dict of the pieces."""
    d = {}
    d["axis"] = axis()
    d["barA"] = hbar(XA, 400, BLUE)
    d["barB"] = hbar(XB, 100, ORANGE)
    d["valA"] = vlabel("400", d["barA"])
    d["valB"] = vlabel("100", d["barB"])
    d["nameA"] = T("A alone", 26, BLUE).move_to([XA, BASE - 0.4, 0])
    d["nameB"] = T("B alone", 26, ORANGE).move_to([XB, BASE - 0.4, 0])
    mA = hbar(XM, 300, BLUE)
    mB = hbar(XM, 100, ORANGE)
    mB.move_to([XM, yy(300) + 100 * K / 2, 0])
    d["mixA"], d["mixB"] = mA, mB
    d["mix"] = VGroup(mA, mB)
    d["tA"] = M("A 300", 22, TEXT).move_to(mA)
    d["tB"] = M("B 100", 22, TEXT).move_to(mB)
    d["valM"] = vlabel("400", mB)
    d["nameM"] = T("A + B together", 26, TEXT).move_to([XM, BASE - 0.4, 0])
    d["unit"] = T(UNIT, 22, GREY).to_corner(UL, buff=0.5).shift(DOWN * 0.55)
    return d


def add_all(scene, d, keys):
    scene.add(*[d[k] for k in keys])


STATIC = ["axis", "barA", "barB", "valA", "valB", "nameA", "nameB", "mixA", "mixB", "tA", "tB", "valM", "nameM", "unit"]


class S00Title(TitleCard):
    LESSON = "Biodiversity and ecosystem function"
    TITLE = "Splitting a mixture's extra yield"


# ---------------------------------------------------------------------------------------------
class S01Mixture(SpokenScene):
    def construct(self):
        d = chart()
        head = T("Made-up example: two species, sown in equal proportions", 28, TEXT).to_edge(UP, buff=0.4)
        self.play(FadeIn(head, shift=DOWN * 0.1), FadeIn(d["unit"]), Create(d["axis"]), run_time=0.8)
        self.at("monocultures")
        self.play(FadeIn(d["nameA"]), FadeIn(d["nameB"]), FadeIn(d["nameM"]), run_time=0.6)
        two = T("one reason, or two?", 46, GOLD).move_to([0, 0.6, 0])
        self.at("one reason")
        self.play(FadeIn(two, scale=0.9), run_time=0.6)
        self.at("Species A alone")
        self.play(FadeOut(two), GrowFromEdge(d["barA"], DOWN), run_time=0.8)
        self.play(FadeIn(d["valA"]), run_time=0.4)
        self.at("Species B alone")
        self.play(GrowFromEdge(d["barB"], DOWN), run_time=0.6)
        self.play(FadeIn(d["valB"]), run_time=0.4)
        self.at("Sown together")
        self.play(GrowFromEdge(d["mixA"], DOWN), run_time=0.7)
        self.play(GrowFromEdge(d["mixB"], DOWN), run_time=0.5)
        self.play(FadeIn(d["tA"]), FadeIn(d["tB"]), FadeIn(d["valM"]), run_time=0.5)
        q = M("?", 70, GOLD).move_to([4.2, yy(300), 0])
        qt = T("a gain?", 30, GOLD).next_to(q, DOWN, buff=0.2)
        self.at("Is that a")
        self.play(FadeIn(q, scale=1.4), FadeIn(qt), run_time=0.5)
        self.at("where does it come from")
        self.play(Indicate(q, color=GOLD, scale_factor=1.3), run_time=0.8)
        self.finish()


# ---------------------------------------------------------------------------------------------
class S02Benchmark(SpokenScene):
    def construct(self):
        d = chart()
        add_all(self, d, STATIC)
        head = T("Made-up example: two species, sown in equal proportions", 28, TEXT).to_edge(UP, buff=0.4)
        self.add(head)
        self.at("set a benchmark")
        self.play(Indicate(VGroup(d["barA"], d["barB"]), color=GREY, scale_factor=1.04), run_time=0.8)
        self.at("expected mixture yield")
        ex = dashed(yy(250))
        exl = side_label("expected", "250", yy(250), GREY)
        self.play(Create(ex), FadeIn(exl), run_time=0.9)
        self.at("over")
        eq = M("(400 + 100) / 2 = 250", 32, GREY).move_to([0.8, 2.6, 0])
        self.play(FadeIn(eq, shift=DOWN * 0.1), run_time=0.6)
        self.at("observed yield")
        self.play(Indicate(d["mix"], color=TEXT, scale_factor=1.05), run_time=0.8)
        self.at("net effect")
        br = Brace(Line([2.55, yy(250), 0], [2.55, yy(400), 0]), direction=RIGHT, color=GOLD, buff=0.1)
        lab = M("+150", 34, GOLD).next_to(br, RIGHT, buff=0.2)
        self.play(GrowFromCenter(br), FadeIn(lab), run_time=0.7)
        self.at("two parts")
        # the +150 splits into two unknown parts
        mid = (yy(250) + yy(400)) / 2
        split = Line([2.95, mid, 0], [3.6, mid, 0], color=GOLD, stroke_width=3)
        q1 = M("?", 40, GOLD).move_to([3.95, (mid + yy(400)) / 2, 0])
        q2 = M("?", 40, GOLD).move_to([3.95, (mid + yy(250)) / 2, 0])
        self.play(FadeOut(lab), Create(split), FadeIn(q1), FadeIn(q2), run_time=0.8)
        self.finish()


# ---------------------------------------------------------------------------------------------
class S03Two(SpokenScene):
    def construct(self):
        ctitle = chip("complementarity", GREEN, 34).move_to([-3.2, 3.0, 0])
        stitle = chip("selection", RED, 34).move_to([3.2, 3.0, 0])
        # left panel: two species each above the level the monoculture predicts
        b0 = -1.5
        exp_h, act_h = 1.7, 2.9
        xs = [-4.3, -2.0]
        cols = [BLUE, ORANGE]
        names = ["A", "B"]
        lbars, lexp, lup, lnames = [], [], [], []
        for x, c, n in zip(xs, cols, names):
            bar = Rectangle(width=1.5, height=act_h, stroke_color=c, stroke_width=3, fill_color=c, fill_opacity=0.45)
            bar.move_to([x, b0 + act_h / 2, 0])
            e = DashedLine([x - 0.95, b0 + exp_h, 0], [x + 0.95, b0 + exp_h, 0], color=GREY, stroke_width=3, dash_length=0.12)
            up = Arrow([x + 1.2, b0 + exp_h, 0], [x + 1.2, b0 + act_h, 0], buff=0, color=GREEN, stroke_width=6,
                       tip_length=0.25, max_tip_length_to_length_ratio=0.5)
            nm = T(n, 30, c).move_to([x, b0 - 0.35, 0])
            lbars.append(bar); lexp.append(e); lup.append(up); lnames.append(nm)
        lcap = VGroup(T("on average, better than", 24, GREEN), T("monocultures predict", 24, GREEN)).arrange(DOWN, buff=0.08).move_to([-3.2, -2.55, 0])
        # right panel: random draw of species, one productive one takes over
        sx = [1.3, 2.6, 3.9, 5.2]
        dots = []
        for i, x in enumerate(sx):
            c = RED if i == 2 else GREY
            dots.append(Circle(radius=0.42, stroke_color=c, stroke_width=3, fill_color=c, fill_opacity=0.5).move_to([x, 0.1, 0]))
        rcap1 = T("a random mix of species", 24, GREY).move_to([3.3, 1.9, 0])
        rcap2 = VGroup(T("one highly productive", 24, RED), T("species dominates", 24, RED)).arrange(DOWN, buff=0.08).move_to([3.3, -2.55, 0])
        netq = VGroup(M("net effect = ", 30, GOLD), M("complementarity", 30, GREEN), M(" + ", 30, GOLD), M("selection", 30, RED))
        netq.arrange(RIGHT, buff=0.2).move_to([0, -3.35, 0])

        self.at("Complementarity is the first part")
        self.play(FadeIn(ctitle, shift=DOWN * 0.1), run_time=0.5)
        self.play(*[FadeIn(x) for x in lbars], *[FadeIn(x) for x in lnames], *[Create(x) for x in lexp], run_time=0.8)
        self.at("better in mixture")
        self.play(*[GrowArrow(x) for x in lup], FadeIn(lcap), run_time=0.8)
        self.at("used resources differently")
        self.play(Indicate(VGroup(*lbars), color=GREEN, scale_factor=1.03), run_time=0.9)
        self.at("Selection is the second part")
        self.play(FadeIn(stitle, shift=DOWN * 0.1), run_time=0.5)
        self.play(*[GrowFromCenter(x) for x in dots], FadeIn(rcap1), run_time=0.7)
        self.at("highly productive species")
        self.play(Indicate(dots[2], color=RED, scale_factor=1.5), run_time=0.8)
        self.at("dominates")
        self.play(dots[2].animate.scale(2.0), *[dots[i].animate.scale(0.7) for i in (0, 1, 3)], FadeIn(rcap2), run_time=0.9)
        self.at("The partition measures both")
        self.play(FadeIn(netq, shift=UP * 0.1), run_time=0.7)
        self.finish()


# ---------------------------------------------------------------------------------------------
RK = 4.4  # units per 1.0 relative yield
RX = [-3.3, 0.6]
RW = 2.2


def rbar(x, v, color):
    r = Rectangle(width=RW, height=v * RK, stroke_color=color, stroke_width=3, fill_color=color, fill_opacity=0.45)
    return r.move_to([x, BASE + v * RK / 2, 0])


def backed(g):
    back = Rectangle(width=g.width + 0.12, height=g.height + 0.1, stroke_width=0, fill_color=BG, fill_opacity=1).move_to(g)
    out = VGroup(back, g)
    out.set_z_index(5)
    return out


def ry(v):
    return BASE + v * RK


class S04Relative(SpokenScene):
    def construct(self):
        ax = axis(-5.2, 2.4)
        unit = T("relative yield = mixture yield ÷ own monoculture yield", 22, GREY).to_corner(UL, buff=0.5).shift(DOWN * 0.1)
        legend = T("dashed: the species alone   solid: in the mixture", 22, GREY).next_to(unit, DOWN, buff=0.12, aligned_edge=LEFT)
        outs = []
        for x, c in zip(RX, [BLUE, ORANGE]):
            r = Rectangle(width=RW, height=RK, stroke_color=c, stroke_width=3).move_to([x, BASE + RK / 2, 0])
            outs.append(DashedVMobject(r, num_dashes=44))
        nm = [T("species A", 28, BLUE).move_to([RX[0], BASE - 0.4, 0]), T("species B", 28, ORANGE).move_to([RX[1], BASE - 0.4, 0])]
        alone = [M("alone 400", 26, BLUE).next_to(outs[0], UP, buff=0.12), M("alone 100", 26, ORANGE).next_to(outs[1], UP, buff=0.12)]
        self.at("measure each species")
        self.play(FadeIn(unit), FadeIn(legend), Create(ax), *[Create(o) for o in outs], *[FadeIn(n) for n in nm], *[FadeIn(a) for a in alone], run_time=1.0)
        self.at("Species A yields")
        fa = rbar(RX[0], 0.75, BLUE)
        la = M("300", 36, TEXT).move_to([RX[0], ry(0.75) - 0.5, 0])
        self.play(GrowFromEdge(fa, DOWN), run_time=0.8)
        self.play(FadeIn(la), run_time=0.3)
        self.at("relative yield is")
        ra = backed(VGroup(M("300/400", 24, BLUE), M("0.75", 40, BLUE)).arrange(DOWN, buff=0.08).move_to([-1.35, ry(0.75) - 0.75, 0]))
        self.play(FadeIn(ra, shift=RIGHT * 0.1), run_time=0.5)
        self.at("Species B yields")
        fb = rbar(RX[1], 1.0, ORANGE)
        lb = M("100", 36, TEXT).move_to([RX[1], ry(1.0) - 0.55, 0])
        self.play(GrowFromEdge(fb, DOWN), run_time=0.8)
        self.play(FadeIn(lb), run_time=0.3)
        self.at("relative yield is", nth=1)
        rb = backed(VGroup(M("100/100", 24, ORANGE), M("1", 40, ORANGE)).arrange(DOWN, buff=0.08).move_to([-1.35, ry(1.0) - 0.6, 0]))
        self.play(FadeIn(rb, shift=RIGHT * 0.1), run_time=0.5)
        self.at("sown at half")
        ex = dashed(ry(0.5), -5.2, 2.4)
        exl = side_label("expected", "0.5", ry(0.5), GREY, x=4.9, vs=36)
        self.play(Create(ex), FadeIn(exl), run_time=0.8)
        self.at("The gains are")
        gxa = RX[0] - RW / 2 - 0.25
        gxb = RX[1] + RW / 2 + 0.25
        ga = Line([gxa, ry(0.5), 0], [gxa, ry(0.75), 0], color=GREEN, stroke_width=8)
        gb = Line([gxb, ry(0.5), 0], [gxb, ry(1.0), 0], color=GREEN, stroke_width=8)
        gal = M("+0.25", 32, GREEN).move_to([gxa - 0.2 - 0.7, (ry(0.5) + ry(0.75)) / 2, 0])
        gbl = M("+0.5", 32, GREEN).move_to([gxb + 0.2 + 0.6, (ry(0.5) + ry(1.0)) / 2, 0])
        self.play(Create(ga), FadeIn(gal), run_time=0.6)
        self.at("and 0")
        self.play(Create(gb), FadeIn(gbl), run_time=0.6)
        self.finish()


# ---------------------------------------------------------------------------------------------
class S05Sum(SpokenScene):
    def construct(self):
        wk = 0.05
        x0 = -6.0
        h = 0.6
        yE1, yG = 2.75, 2.0
        yE2, yR = 0.85, 0.1
        yE3, yN = -0.95, -1.7
        endg = x0 + 187.5 * wk
        eq1 = M("complementarity = 2 × 0.375 × 250 = +187.5", 28, GREEN)
        eq2 = M("selection = −37.5", 28, RED)
        eq3 = M("187.5 − 37.5 = 150", 28, GOLD)
        for e, y in ((eq1, yE1), (eq2, yE2), (eq3, yE3)):
            e.move_to([0, y, 0]).align_to([x0, 0, 0], LEFT)

        def bar(v, color, left, y):
            r = Rectangle(width=v * wk, height=h, stroke_color=color, stroke_width=3, fill_color=color, fill_opacity=0.5)
            return r.move_to([left + v * wk / 2, y, 0])

        gbar = bar(187.5, GREEN, x0, yG)
        rbar_ = bar(37.5, RED, endg - 37.5 * wk, yR)
        nbar = bar(150, GOLD, x0, yN)
        gl = M("+187.5", 28, GREEN).next_to(gbar, RIGHT, buff=0.2)
        rl = M("−37.5", 28, RED).next_to(rbar_, RIGHT, buff=0.2)
        nl = M("150 net effect", 28, GOLD).next_to(nbar, RIGHT, buff=0.2)
        link = DashedLine([endg, yG - h / 2, 0], [endg, yR + h / 2, 0], color=GREY, stroke_width=2, dash_length=0.1)
        xn = endg - 37.5 * wk
        link2 = DashedLine([xn, yR - h / 2, 0], [xn, yN + h / 2, 0], color=GREY, stroke_width=2, dash_length=0.1)
        ca = chip("A: alone 400, gain 0.25", BLUE, 26)
        cb = chip("B: alone 100, gain 0.5", ORANGE, 26)
        cc = VGroup(ca, cb).arrange(RIGHT, buff=0.6).move_to([0, -3.0, 0])

        der1 = M("mean gain = (0.25 + 0.5) / 2", 26, GREEN).move_to([0, 1.3, 0]).align_to([x0, 0, 0], LEFT)
        der2 = M("mean gain = (0.25 + 0.5) / 2 = 0.375", 26, GREEN).move_to([0, 1.3, 0]).align_to([x0, 0, 0], LEFT)
        self.at("Complementarity is richness")
        self.play(FadeIn(eq1, shift=DOWN * 0.1), run_time=0.7)
        self.at("the mean gain")
        self.play(FadeIn(der1, shift=DOWN * 0.1), run_time=0.6)
        self.at("Two times")
        self.play(ReplacementTransform(der1, der2), GrowFromEdge(gbar, LEFT), FadeIn(gl), run_time=1.0)
        self.at("Selection asks")
        self.play(FadeIn(cc, shift=UP * 0.1), run_time=0.7)
        self.at("larger gain went to species")
        self.play(Indicate(cb, color=ORANGE, scale_factor=1.08), run_time=0.8)
        self.at("So selection is negative")
        self.play(FadeIn(eq2, shift=DOWN * 0.1), Create(link), GrowFromEdge(rbar_, RIGHT), FadeIn(rl), run_time=0.9)
        self.at("Add them")
        self.play(FadeIn(eq3, shift=DOWN * 0.1), Create(link2), GrowFromEdge(nbar, LEFT), FadeIn(nl), run_time=0.9)
        self.finish()


# ---------------------------------------------------------------------------------------------
class S06Rule(SpokenScene):
    def construct(self):
        d = chart()
        add_all(self, d, STATIC)
        head = T("Made-up example: two species, sown in equal proportions", 28, TEXT).to_edge(UP, buff=0.4)
        self.add(head)
        ex = dashed(yy(250))
        exl = side_label("expected", "250", yy(250), GREY)
        self.add(ex, exl)
        self.at("best monoculture")
        best = dashed(yy(400), color=TEXT)
        bl = side_label("best monoculture", "400", yy(400), TEXT, x=4.9)
        self.play(Create(best), FadeIn(bl), run_time=0.8)
        self.at("exactly what species")
        self.play(Indicate(VGroup(d["barA"], d["mix"]), color=TEXT, scale_factor=1.04), run_time=0.9)
        self.at("no transgressive overyielding")
        no = T("no transgressive overyielding", 30, TEXT).move_to([0.8, 2.6, 0])
        self.play(FadeIn(no, shift=DOWN * 0.1), run_time=0.7)
        self.at("beats the average monoculture")
        self.play(Indicate(exl, color=TEXT, scale_factor=1.15), run_time=0.9)
        self.at("positive complementarity term")
        self.play(*[FadeOut(m) for m in self.mobjects], run_time=0.6)
        comp = chip("positive complementarity", GREEN, 38).move_to([0, 2.6, 0])
        part = chip("resource partitioning", GREY, 38).move_to([0, -0.2, 0])
        a1 = Line([0, comp.get_bottom()[1] - 0.15, 0], [0, 1.6, 0], color=GREY, stroke_width=5)
        a2 = Line([0, 0.75, 0], [0, part.get_top()[1] + 0.12, 0], color=GREY, stroke_width=5)
        q = M("?", 56, GOLD).move_to([0, 1.18, 0])
        self.play(FadeIn(comp, shift=DOWN * 0.2), run_time=0.5)
        self.play(Create(a1), FadeIn(q), Create(a2), FadeIn(part), run_time=0.8)
        self.at("does not prove")
        self.play(Indicate(q, color=GOLD, scale_factor=1.4), run_time=0.8)
        self.at("Keep this rule")
        rule = T("The partition splits the gain.", 44, TEXT)
        rule2 = T("It names no mechanism.", 44, TEXT)
        VGroup(rule, rule2).arrange(DOWN, buff=0.3).move_to([0, -2.2, 0])
        self.play(FadeIn(rule, shift=UP * 0.1), run_time=0.6)
        self.at("names no mechanism")
        self.play(FadeIn(rule2, shift=UP * 0.1), run_time=0.6)
        self.finish()


class S07End(EndCard):
    LINE = "The partition splits the gain, but names no mechanism."
