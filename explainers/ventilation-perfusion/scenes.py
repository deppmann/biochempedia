"""Ventilation, perfusion and gas exchange: a spread of ratios lowers arterial oxygen  (Biochemistrypedia explainer)

Timed to the SPOKEN words: every self.at("...") cue waits for that phrase in audio/words.json.

COLOR MAP (one color per concept, whole video)
  BLUE   = air, ventilation, alveolar gas
  RED    = blood, perfusion, blood flow, arterial blood
  YELLOW = the oxygen the blood leaves with (oxygen content, PO2, the A-a difference, the question)
  GREEN  = the middle of the range (the measured band, the textbook value 0.8)
  GREY   = lung outline, axes, labels, de-emphasized
Only labelled blocks, arrows, bars and plots. Every number on screen is the lesson's own
(roughly 6 L/min air and 5 L/min blood in a resting adult; 95.5 percent between ratios 0.3 and 2.1 in four
young semirecumbent normal subjects by the inert-gas method; reference mean of the blood-flow distribution
0.80 to 1.00; textbook 0.8). The curve in scene 5 and the bars in scene 4 and 6 are schematic and say so.
"""
import numpy as np
from bp_style import *  # noqa: F401,F403

AIR, BLOOD, VALUE, MID = BLUE, RED, YELLOW, GREEN


# ---------------------------------------------------------------------------------------------
# helpers
# ---------------------------------------------------------------------------------------------
def arr(a, b, color=GREY, w=5, tip=0.2):
    return Arrow(a, b, buff=0.0, color=color, stroke_width=w, tip_length=tip,
                 max_tip_length_to_length_ratio=0.45, max_stroke_width_to_length_ratio=12)


def bchip(text, color=BLUE, size=26, **kw):
    """chip with an opaque backing so lines drawn behind it do not show through."""
    c = chip(text, color, size=size, **kw)
    back = RoundedRectangle(corner_radius=0.14, width=c[0].width, height=c[0].height, stroke_width=0,
                            fill_color=BG, fill_opacity=1).move_to(c[0])
    return VGroup(back, *c)


def unit(x, y, air=True, blood=True, s=1.0, arrow=0.85):
    """A lung unit as a labelled block: alveolus box, air arrow above, blood arrow below.
    When a flow is absent a dashed grey stub stands in for its arrow."""
    box = RoundedRectangle(corner_radius=0.2, width=1.5 * s, height=1.1 * s, stroke_color=AIR, stroke_width=3,
                           fill_color=AIR, fill_opacity=0.12).move_to([x, y, 0])
    L = arrow * s
    top = [x, y + 0.55 * s + L, 0]
    bot = [x, y - 0.55 * s - L, 0]
    if air:
        a = arr(top, [x, y + 0.55 * s + 0.04, 0], AIR, w=7, tip=0.24)
    else:
        a = DashedLine(top, [x, y + 0.55 * s + 0.04, 0], color=GREY, stroke_width=3, dash_length=0.12)
    if blood:
        b = arr(bot, [x, y - 0.55 * s - 0.04, 0], BLOOD, w=7, tip=0.24)
    else:
        b = DashedLine(bot, [x, y - 0.55 * s - 0.04, 0], color=GREY, stroke_width=3, dash_length=0.12)
    g = VGroup(a, box, b)
    g.box, g.a, g.b = box, a, b
    return g


def label_block(lines, x, y, sizes=None, colors=None, buff=0.14):
    sizes = sizes or [30] + [24] * (len(lines) - 1)
    colors = colors or [TEXT] + [GREY] * (len(lines) - 1)
    return VGroup(*[T(t, s, c) for t, s, c in zip(lines, sizes, colors)]).arrange(DOWN, buff=buff).move_to([x, y, 0])


class S00Title(TitleCard):
    LESSON = "Ventilation, perfusion and gas exchange"
    TITLE = "A spread of ratios lowers arterial oxygen"


# ---------------------------------------------------------------------------------------------
class S01Question(SpokenScene):
    """6 L/min air and 5 L/min blood go through the lungs; neither number says what the blood leaves with;
    what settles it is air and blood at the same places in the same proportion."""

    def construct(self):
        who = T("resting adult, every minute", 24, GREY).move_to([0, 3.15, 0])
        air = bchip("air  about 6 L/min", AIR, 28).move_to([-3.4, 2.35, 0])
        blood = bchip("blood  about 5 L/min", BLOOD, 28).move_to([3.4, 2.35, 0])
        lung = RoundedRectangle(corner_radius=0.35, width=9.0, height=3.7, stroke_color=GREY, stroke_width=3,
                                fill_color=GREY, fill_opacity=0.07).move_to([0, -0.55, 0])
        lung_lbl = T("lungs", 26, GREY).move_to(lung.get_corner(UL) + [0.7, -0.3, 0])
        a1 = arr([-3.4, 1.8, 0], [-3.4, 1.3, 0], AIR, w=7)
        a2 = arr([3.4, 1.8, 0], [3.4, 1.3, 0], BLOOD, w=7)

        self.at("A resting adult")
        self.play(FadeIn(who), run_time=0.5)
        self.at("liters of air")
        self.play(FadeIn(air, shift=DOWN * 0.2), run_time=0.6)
        self.at("liters of blood")
        self.play(FadeIn(blood, shift=DOWN * 0.2), run_time=0.6)
        xs = [-3.15, -1.05, 1.05, 3.15]
        units = [unit(x, -0.55, True, True, s=0.78) for x in xs]
        self.at("through the lungs")
        self.play(FadeIn(lung), FadeIn(lung_lbl), GrowArrow(a1), GrowArrow(a2), run_time=0.9)
        self.play(LaggedStart(*[FadeIn(u.box, scale=0.9) for u in units], lag_ratio=0.15), run_time=0.8)

        q = T("What does the blood leave with?", 34, VALUE, weight=BOLD).move_to([0, -3.1, 0])
        self.at("Do those two numbers")
        self.play(FadeIn(q, shift=UP * 0.15), run_time=0.6)
        self.at("They do not")
        self.play(air.animate.set_opacity(0.35), blood.animate.set_opacity(0.35), a1.animate.set_opacity(0.35),
                  a2.animate.set_opacity(0.35), Indicate(q, color=VALUE, scale_factor=1.06), run_time=0.9)

        # same places, same proportion: four places, each with the same air-to-blood pairing
        self.at("same places")
        self.play(FadeOut(q), FadeOut(lung_lbl), *[Indicate(u.box, color=TEXT, scale_factor=1.12) for u in units],
                  run_time=0.9)
        q2 = T("air and blood together, in the same proportion", 30, TEXT).move_to([0, -3.1, 0])
        self.at("same proportion")
        self.play(*[GrowArrow(u.a) for u in units], *[GrowArrow(u.b) for u in units], FadeIn(q2), run_time=0.9)
        self.finish()


# ---------------------------------------------------------------------------------------------
class S02Ratio(SpokenScene):
    """one quantity: ventilation / perfusion; zero = shunt; infinite = dead space."""

    def construct(self):
        cond = T("for a given inspired gas and mixed venous blood", 24, GREY).move_to([0, 3.2, 0])
        self.at("For a given")
        self.play(FadeIn(cond), run_time=0.6)

        eq = VGroup(T("ventilation", 40, AIR), T("÷", 40, TEXT), T("perfusion", 40, BLOOD),
                    T("=  ratio", 40, TEXT, weight=BOLD)).arrange(RIGHT, buff=0.3).move_to([0, 2.35, 0])
        self.at("one quantity")
        self.play(FadeIn(eq[3], shift=UP * 0.1), run_time=0.5)
        self.at("ventilation divided by")
        self.play(FadeIn(eq[0]), run_time=0.4)
        self.play(FadeIn(eq[1]), FadeIn(eq[2]), run_time=0.5)

        # number line, not to scale
        y0 = 0.95
        line = Line([-5.2, y0, 0], [5.2, y0, 0], color=GREY, stroke_width=4)
        t0 = T("0", 30, TEXT, weight=BOLD).move_to([-5.2, y0 + 0.75, 0])
        tinf = T("∞", 40, TEXT, weight=BOLD).move_to([5.2, y0 + 0.75, 0])
        tick0 = Line([-5.2, y0 - 0.15, 0], [-5.2, y0 + 0.15, 0], color=GREY, stroke_width=4)
        tickinf = Line([5.2, y0 - 0.15, 0], [5.2, y0 + 0.15, 0], color=GREY, stroke_width=4)
        note = T("ratio, not to scale", 22, GREY).move_to([0, y0 - 0.45, 0])
        mark = Triangle(color=VALUE, fill_color=VALUE, fill_opacity=1).scale(0.2).rotate(PI).move_to([-5.2, y0 + 0.2, 0])
        self.at("At a ratio of zero")
        self.play(Create(line), FadeIn(tick0), FadeIn(tickinf), FadeIn(t0), FadeIn(tinf), FadeIn(note), FadeIn(mark),
                  run_time=0.8)

        shunt = unit(-4.6, -1.8, air=False, blood=True, s=1.4, arrow=0.5)
        s_lbl = VGroup(T("shunt", 34, BLOOD, weight=BOLD), T("perfused,", 26, GREY), T("not ventilated", 26, GREY)
                       ).arrange(DOWN, buff=0.08, aligned_edge=LEFT).move_to([-1.0, -0.85, 0])
        s_lbl.align_to([-3.2, 0, 0], LEFT).set_y(-1.0)
        self.at("makes it a shunt")
        self.play(FadeIn(shunt), FadeIn(s_lbl), run_time=0.8)
        s_out = VGroup(T("blood leaves with the", 24, VALUE), T("oxygen content it", 24, VALUE),
                       T("arrived with", 24, VALUE)).arrange(DOWN, buff=0.12, aligned_edge=LEFT)
        s_out.next_to(s_lbl, DOWN, buff=0.35, aligned_edge=LEFT)
        self.at("Its blood leaves")
        self.play(FadeIn(s_out), run_time=0.7)
        self.at("infinite ratio")
        self.play(mark.animate.move_to([5.2, y0 + 0.2, 0]), run_time=1.2)
        dead = unit(4.6, -1.8, air=True, blood=False, s=1.4, arrow=0.5)
        d_lbl = VGroup(T("dead space", 34, AIR, weight=BOLD), T("ventilated,", 26, GREY), T("not perfused", 26, GREY)
                       ).arrange(DOWN, buff=0.08, aligned_edge=RIGHT).move_to([1.0, -0.85, 0])
        d_lbl.align_to([3.2, 0, 0], RIGHT).set_y(-1.0)
        self.at("dead space")
        self.play(FadeIn(dead), FadeIn(d_lbl), run_time=0.8)
        self.finish()


# ---------------------------------------------------------------------------------------------
class S03Spread(SpokenScene):
    """a spread of ratios (log axis): 95.5 percent of flow and ventilation between 0.3 and 2.1; 0.8 is the middle of a range."""

    def construct(self):
        X = lambda r: 5.9 * np.log10(r)      # log axis: 0.1 -> -5.9, 10 -> +5.9
        ay = -1.35
        axis = Line([-5.9, ay, 0], [5.9, ay, 0], color=GREY, stroke_width=4)
        ax_lbl = T("ventilation-perfusion ratio (log scale)", 24, GREY).move_to([0, -3.35, 0])
        low = T("low", 24, GREY).move_to([-5.6, ay - 0.45, 0])
        high = T("high", 24, GREY).move_to([5.6, ay - 0.45, 0])
        ticks = VGroup()
        for r in (0.3, 2.1):
            ticks.add(Line([X(r), ay - 0.14, 0], [X(r), ay + 0.14, 0], color=GREY, stroke_width=4))
            ticks.add(T(f"{r}", 26, TEXT, weight=BOLD).move_to([X(r), ay - 0.5, 0]))
        self.at("Real lungs hold")
        self.play(Create(axis), FadeIn(ax_lbl), FadeIn(low), FadeIn(high), run_time=0.9)
        spread = DoubleArrow([X(0.12), ay + 0.5, 0], [X(8.5), ay + 0.5, 0], color=GREY, stroke_width=4, buff=0,
                             tip_length=0.2)
        sp_lbl = T("a spread of ratios", 28, TEXT).move_to([0, ay + 1.0, 0])
        self.at("spread of ratios")
        self.play(GrowFromCenter(spread), FadeIn(sp_lbl), run_time=0.8)

        meth = bchip("inert-gas method", GREY, 26).move_to([-3.2, 3.1, 0])
        self.at("inert gas method")
        self.play(FadeIn(meth, shift=DOWN * 0.15), run_time=0.5)
        subj = T("four young semirecumbent normal subjects", 26, GREY).move_to([2.6, 3.1, 0])
        self.at("four young")
        self.play(FadeIn(subj), FadeOut(spread), FadeOut(sp_lbl), run_time=0.6)

        # bars between 0.3 and 2.1
        w = X(2.1) - X(0.3)
        cx = (X(2.1) + X(0.3)) / 2
        fbar = Rectangle(width=w, height=0.62, stroke_color=BLOOD, stroke_width=3, fill_color=BLOOD, fill_opacity=0.35
                         ).move_to([cx, 0.15, 0])
        vbar = Rectangle(width=w, height=0.62, stroke_color=AIR, stroke_width=3, fill_color=AIR, fill_opacity=0.35
                         ).move_to([cx, 1.0, 0])
        ft = VGroup(T("blood flow", 26, TEXT, weight=BOLD).align_to(fbar, LEFT).shift(RIGHT * 0.2),
                    T("95.5%", 26, TEXT, weight=BOLD).align_to(fbar, RIGHT).shift(LEFT * 0.2))
        vt = VGroup(T("ventilation", 26, TEXT, weight=BOLD).align_to(vbar, LEFT).shift(RIGHT * 0.2),
                    T("95.5%", 26, TEXT, weight=BOLD).align_to(vbar, RIGHT).shift(LEFT * 0.2))
        for g, b in ((ft, fbar), (vt, vbar)):
            for t in g:
                t.set_y(b.get_y())
        guides = VGroup(*[DashedLine([X(r), ay, 0], [X(r), 1.4, 0], color=GREY, stroke_width=2, dash_length=0.1)
                          for r in (0.3, 2.1)])
        rngnote = VGroup(T("range only, not the", 22, GREY), T("distribution's shape", 22, GREY)
                         ).arrange(DOWN, buff=0.05, aligned_edge=LEFT).move_to([4.1, 0.58, 0])
        rngnote.align_to([2.4, 0, 0], LEFT)
        self.at("both blood flow")
        self.play(FadeIn(ticks), Create(guides), run_time=0.5)
        self.play(GrowFromEdge(fbar, LEFT), GrowFromEdge(vbar, LEFT), run_time=0.8)
        self.play(FadeIn(ft), FadeIn(vt), FadeIn(rngnote), run_time=0.4)

        noshunt = T("no shunt on air", 26, TEXT).move_to([-4.9, 0.58, 0])
        self.at("no shunt on air")
        self.play(FadeIn(noshunt, shift=RIGHT * 0.2), run_time=0.6)

        # healthy reference mean of the blood-flow distribution 0.80 to 1.00
        ref = Line([X(0.8), ay, 0], [X(1.0), ay, 0], color=VALUE, stroke_width=12)
        ref_lbl = VGroup(T("healthy reference: mean of the blood-flow", 24, VALUE),
                         T("distribution, 0.80 to 1.00", 24, VALUE)).arrange(DOWN, buff=0.06).move_to([0, -2.45, 0])
        ref_ln = Line([X(0.9), ay - 0.08, 0], [X(0.9), -2.1, 0], color=VALUE, stroke_width=2)
        self.at("Reference values")
        self.play(FadeOut(noshunt), FadeOut(subj), Create(ref), Create(ref_ln), FadeIn(ref_lbl), run_time=0.7)
        self.at("Textbooks quote")
        self.play(FadeOut(ref), FadeOut(ref_lbl), FadeOut(ref_ln), run_time=0.4)
        line08 = DashedLine([X(0.8), ay, 0], [X(0.8), 1.5, 0], color=MID, stroke_width=4, dash_length=0.12)
        tb = T("0.8", 28, MID, weight=BOLD).move_to([X(0.8), ay - 0.5, 0])
        tb_lbl = T("textbook: a single ratio of 0.8", 26, MID).move_to([0, 2.05, 0])
        self.play(Create(line08), FadeIn(tb), FadeIn(tb_lbl), run_time=0.6)
        rng = T("the middle of a range", 28, TEXT, weight=BOLD).move_to([0, 2.05, 0])
        band = SurroundingRectangle(VGroup(fbar, vbar), color=MID, stroke_width=4, buff=0.12)
        self.at("middle of a range")
        self.play(ReplacementTransform(tb_lbl, rng), Create(band), run_time=0.7)
        self.finish()


# ---------------------------------------------------------------------------------------------
class S04Averages(SpokenScene):
    """expired gas is averaged by ventilation, arterial blood by blood flow; a spread lowers arterial PO2 by itself."""

    def construct(self):
        h1 = T("A spread lowers arterial PO2 by itself", 34, VALUE, weight=BOLD).move_to([0, 3.15, 0])
        h2 = T("even if every unit equilibrates with its own alveolar gas", 26, GREY).move_to([0, 2.55, 0])
        self.at("A spread lowers")
        self.play(FadeIn(h1, shift=UP * 0.1), run_time=0.6)
        self.at("That holds even")
        self.play(FadeIn(h2), run_time=0.6)

        names = ["high ratio", "mid ratio", "low ratio"]
        vent = [3.2, 1.8, 0.8]       # schematic bar lengths
        flow = [0.8, 1.8, 3.2]
        ys = [1.2, 0.05, -1.1]
        lblx = 0.0
        rows, vb, fb = [], [], []
        for n, v, f, y in zip(names, vent, flow, ys):
            c = bchip(n, GREY, 26).move_to([lblx, y, 0])
            b1 = Rectangle(width=v, height=0.7, stroke_color=AIR, stroke_width=3, fill_color=AIR, fill_opacity=0.45)
            b1.move_to([-1.55 - v / 2, y, 0])
            b2 = Rectangle(width=f, height=0.7, stroke_color=BLOOD, stroke_width=3, fill_color=BLOOD, fill_opacity=0.45)
            b2.move_to([1.55 + f / 2, y, 0])
            rows.append(c); vb.append(b1); fb.append(b2)
        hv = T("ventilation", 26, AIR).move_to([-3.2, 1.9, 0])
        hf = T("blood flow", 26, BLOOD).move_to([3.2, 1.9, 0])
        self.at("The two averages")
        self.play(FadeIn(VGroup(*rows)), FadeIn(hv), FadeIn(hf), run_time=0.6)
        self.play(*[GrowFromEdge(b, RIGHT) for b in vb], *[GrowFromEdge(b, LEFT) for b in fb], run_time=1.0)

        coll_l = VGroup(T("expired alveolar gas", 28, AIR), T("weighted by ventilation", 24, GREY)).arrange(DOWN, buff=0.08
                                                                                                         ).move_to([-3.4, -2.55, 0])
        coll_r = VGroup(T("arterial blood", 28, BLOOD), T("weighted by blood flow", 24, GREY)).arrange(DOWN, buff=0.08
                                                                                                    ).move_to([3.4, -2.55, 0])
        self.at("weighted by ventilation")
        self.play(FadeIn(coll_l), run_time=0.5)
        self.at("well ventilated")
        self.play(vb[0].animate.set_fill(AIR, 0.9).set_stroke(AIR, opacity=1), vb[1].animate.set_opacity(0.45), vb[2].animate.set_opacity(0.3),
                  fb[0].animate.set_opacity(0.3), fb[1].animate.set_opacity(0.3), fb[2].animate.set_opacity(0.3), run_time=0.9)
        self.at("Arterial blood is weighted")
        self.play(FadeIn(coll_r),
                  vb[0].animate.set_opacity(0.3), fb[0].animate.set_opacity(0.3), run_time=0.5)
        self.at("poorly ventilated")
        self.play(fb[2].animate.set_fill(BLOOD, 0.9).set_stroke(BLOOD, opacity=1), vb[2].animate.set_opacity(0.45), run_time=0.9)
        tag = T("schematic bars, no scale", 22, GREY).move_to([0, -3.4, 0])
        self.play(FadeIn(tag), run_time=0.4)
        self.finish()


# ---------------------------------------------------------------------------------------------
class S05Content(SpokenScene):
    """mixing is by content; the dissociation curve is flat at the top; high-ratio unit adds little, low-ratio unit subtracts a lot."""

    def construct(self):
        head = T("blood from different units mixes by content, not by partial pressure", 28, TEXT
                 ).move_to([0, 3.2, 0])
        fit(head, max_w=12.2)
        self.at("mixes by oxygen content")
        self.play(FadeIn(head, shift=UP * 0.1), run_time=0.7)

        ox, oy, W, H = -5.4, -2.55, 6.2, 4.6
        xax = Line([ox, oy, 0], [ox + W, oy, 0], color=GREY, stroke_width=4)
        yax = Line([ox, oy, 0], [ox, oy + H, 0], color=GREY, stroke_width=4)
        ylbl = T("oxygen content", 26, VALUE).rotate(PI / 2).move_to([ox - 0.45, oy + H / 2 - 0.2, 0])
        xlbl = T("partial pressure of oxygen", 26, GREY).move_to([ox + W / 2, oy - 0.5, 0])
        f = lambda x: x ** 3.2 / (x ** 3.2 + 0.32 ** 3.2)
        P = lambda x: [ox + W * x, oy + H * 0.92 * f(x) / 1.0, 0]
        self.at("Content is how much")
        self.play(Create(xax), Create(yax), FadeIn(ylbl), run_time=0.8)
        self.at("plots content against")
        self.play(FadeIn(xlbl), run_time=0.5)
        curve = ParametricFunction(lambda t: np.array(P(t)), t_range=[0.0, 1.0, 0.01], color=VALUE, stroke_width=6)
        top = ParametricFunction(lambda t: np.array(P(t)), t_range=[0.72, 1.0, 0.01], color=VALUE, stroke_width=11)
        sch = T("schematic shape, no scale", 22, GREY).move_to([ox + W + 2.2, oy + 0.3, 0])
        self.at("flat at the top")
        self.play(Create(curve), run_time=1.3)
        self.play(Create(top), FadeIn(sch), run_time=0.6)

        # units as dots on the curve
        xm, xh, xl = 0.6, 0.9, 0.3
        dm = Dot(P(xm), radius=0.14, color=TEXT)
        dm_lbl = T("mid-ratio unit", 24, TEXT).move_to([P(xm)[0] + 1.1, P(xm)[1] - 0.65, 0])
        dh = Dot(P(xh), radius=0.14, color=AIR)
        dl = Dot(P(xl), radius=0.14, color=BLOOD)
        gain = Line(P(xm), [P(xm)[0], P(xh)[1], 0], color=VALUE, stroke_width=0)
        # right-hand notes
        n_hi = VGroup(T("high-ratio unit", 28, AIR, weight=BOLD), T("adds almost nothing per dL", 26, VALUE)
                      ).arrange(DOWN, buff=0.08, aligned_edge=LEFT).move_to([3.65, 1.6, 0]).align_to([1.5, 0, 0], LEFT)
        n_lo = VGroup(T("low-ratio unit", 28, BLOOD, weight=BOLD), T("subtracts a great deal", 26, VALUE)
                      ).arrange(DOWN, buff=0.08, aligned_edge=LEFT).move_to([3.65, -0.7, 0]).align_to([1.5, 0, 0], LEFT)
        self.at("high ratio unit")
        self.play(FadeIn(dm), FadeIn(dm_lbl), run_time=0.4)
        self.play(FadeIn(dh, scale=1.4), FadeIn(n_hi), run_time=0.7)
        hi_drop = DashedLine(P(xh), [P(xh)[0], oy, 0], color=GREY, stroke_width=2, dash_length=0.1)
        hi_lvl = DashedLine(P(xh), [ox, P(xh)[1], 0], color=GREY, stroke_width=2, dash_length=0.1)
        mid_lvl = DashedLine(P(xm), [ox, P(xm)[1], 0], color=GREY, stroke_width=2, dash_length=0.1)
        self.play(Create(mid_lvl), Create(hi_lvl), run_time=0.5)
        self.at("low ratio unit")
        self.play(FadeOut(hi_lvl), FadeOut(mid_lvl), FadeIn(dl, scale=1.4), FadeIn(n_lo), run_time=0.7)
        lo_lvl = DashedLine(P(xl), [ox, P(xl)[1], 0], color=GREY, stroke_width=2, dash_length=0.1)
        mid_lvl2 = DashedLine(P(xm), [ox, P(xm)[1], 0], color=GREY, stroke_width=2, dash_length=0.1)
        self.play(Create(lo_lvl), Create(mid_lvl2), run_time=0.5)
        self.finish()


# ---------------------------------------------------------------------------------------------
class S06Difference(SpokenScene):
    """alveolar PO2 is calculated; arterial PO2 sits below it; the gap is the A-a difference; the rule."""

    def construct(self):
        base = -2.5
        Hh = 3.8
        bx1, bx2 = -4.6, -1.5
        a_bar = Rectangle(width=1.7, height=Hh, stroke_color=AIR, stroke_width=3, fill_color=AIR, fill_opacity=0.4
                          ).move_to([bx1, base + Hh / 2, 0])
        a_lbl = VGroup(T("alveolar PO2", 28, AIR), T("calculated", 24, GREY)).arrange(DOWN, buff=0.06
                                                                                      ).move_to([bx1, base - 0.6, 0])
        floor = Line([-5.9, base, 0], [-0.1, base, 0], color=GREY, stroke_width=3)
        self.at("is calculated")
        self.play(Create(floor), GrowFromEdge(a_bar, DOWN), FadeIn(a_lbl), run_time=1.0)

        drop = 1.1
        r_bar = Rectangle(width=1.7, height=Hh, stroke_color=BLOOD, stroke_width=3, fill_color=BLOOD, fill_opacity=0.4
                          ).move_to([bx2, base + Hh / 2, 0])
        r_lbl = T("arterial PO2", 28, BLOOD).move_to([bx2, a_lbl[0].get_y(), 0])
        self.at("The result is")
        self.play(GrowFromEdge(r_bar, DOWN), FadeIn(r_lbl), run_time=0.8)
        r_new = Rectangle(width=1.7, height=Hh - drop, stroke_color=BLOOD, stroke_width=3, fill_color=BLOOD,
                          fill_opacity=0.4).move_to([bx2, base + (Hh - drop) / 2, 0])
        ref = DashedLine([bx1 + 0.85, base + Hh, 0], [bx2 + 1.55, base + Hh, 0], color=GREY, stroke_width=3, dash_length=0.12)
        brace = Line([bx2 + 1.2, base + Hh, 0], [bx2 + 1.2, base + Hh - drop, 0], color=VALUE, stroke_width=0)
        gap = DoubleArrow([bx2 + 1.2, base + Hh - 0.02, 0], [bx2 + 1.2, base + Hh - drop + 0.02, 0], color=VALUE,
                          stroke_width=6, buff=0, tip_length=0.18)
        gap_lbl = VGroup(T("alveolar-arterial", 28, VALUE, weight=BOLD), T("oxygen difference", 28, VALUE, weight=BOLD)
                         ).arrange(DOWN, buff=0.06, aligned_edge=LEFT).move_to([1.9, base + Hh - drop / 2 - 0.1, 0])
        self.at("alveolar arterial oxygen")
        self.play(Transform(r_bar, r_new), Create(ref), run_time=0.8)
        self.play(GrowArrow(gap), FadeIn(gap_lbl), run_time=0.6)

        nb = bchip("even when every unit equilibrates\nwith its own alveolar gas", GREY, 26).move_to([3.2, -0.7, 0])
        self.at("even when every")
        self.play(FadeIn(nb, shift=LEFT * 0.2), run_time=0.6)
        nd = T("a difference, not a diffusion gradient", 26, TEXT).move_to([3.2, -1.9, 0])
        fit(nd, max_w=6.0)
        self.at("not a diffusion gradient")
        self.play(FadeIn(nd, shift=LEFT * 0.2), run_time=0.6)

        # each unit's ratio sets its gas -> a spread -> wider difference
        self.at("Each unit's")
        self.play(FadeOut(VGroup(a_bar, a_lbl, r_bar, r_lbl, ref, gap, gap_lbl, nb, nd, floor)), run_time=0.7)
        c1 = bchip("each unit's ratio mainly sets its gas", AIR, 34).move_to([0, 2.3, 0])
        c1n = T("for a given inspired gas and mixed venous blood", 24, GREY).move_to([0, 1.65, 0])
        c2 = bchip("a spread of ratios", GREY, 34).move_to([0, 0.5, 0])
        c3 = bchip("a wider alveolar-arterial difference", VALUE, 34).move_to([0, -1.3, 0])
        a12 = arr([0, 1.3, 0], [0, 0.95, 0], GREY, w=5)
        a23 = arr([0, 0.0, 0], [0, -0.7, 0], GREY, w=5)
        self.play(FadeIn(c1, shift=UP * 0.1), FadeIn(c1n), run_time=0.6)
        self.at("A spread of ratios alone")
        self.play(GrowArrow(a12), FadeIn(c2), run_time=0.6)
        self.play(GrowArrow(a23), FadeIn(c3), run_time=0.7)
        self.finish()


class S07End(EndCard):
    LINE = "A spread of ratios alone can widen the alveolar-arterial difference."
