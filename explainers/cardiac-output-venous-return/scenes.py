"""Cardiac output and venous return: output is where the curves cross  (Biochemistrypedia explainer)

Timed to the SPOKEN words: every self.at("...") cue waits for that phrase in audio/words.json.
Every number on screen is the lesson's own (illustrative model: Qc = 3 + Pra, Qvr = (7 - Pra)/1;
worked problem B and the table of moves). Plots are computed from those equations; nothing is data.

COLOR MAP (one color per concept, whole video)
  BLUE   = the heart and its curve (cardiac function curve)
  GREEN  = the veins, venous return and mean systemic filling pressure (Pms)
  YELLOW = the output: flow Q, the operating point where the curves cross
  TEAL   = oxygen (uptake and oxygen content)
  RED    = vein collapse (the dogs' collapse zone) and nothing else
  GREY   = structure, axes, ghosts of where a line used to be, hedges
  TEXT   = labels and equations
"""
import numpy as np
from bp_style import *  # noqa: F401,F403


# ---------------------------------------------------------------------------------------------
# helpers
# ---------------------------------------------------------------------------------------------
def bchip(text, color=BLUE, size=26, **kw):
    """chip with an opaque backing so lines drawn behind it do not show through."""
    c = chip(text, color, size=size, **kw)
    back = RoundedRectangle(corner_radius=0.14, width=c[0].width, height=c[0].height, stroke_width=0,
                            fill_color=BG, fill_opacity=1).move_to(c[0])
    return VGroup(back, *c)


def arr(a, b, color=GREY, w=5, tip=0.22):
    return Arrow(a, b, buff=0.08, color=color, stroke_width=w, tip_length=tip,
                 max_tip_length_to_length_ratio=0.45, max_stroke_width_to_length_ratio=12)


def btext(text, size=24, color=GREY, **kw):
    t = T(text, size, color, **kw)
    back = Rectangle(width=t.width + 0.2, height=t.height + 0.14, stroke_width=0, fill_color=BG, fill_opacity=1).move_to(t)
    return VGroup(back, t)


class S00Title(TitleCard):
    LESSON = "Cardiac output and venous return"
    TITLE = "Output is where the curves cross"


# ---------------------------------------------------------------------------------------------
# the plot, shared by scenes 4 to 6 (same place every time)
#   x: right atrial pressure Pra, -4 to 10 mmHg     y: flow, 0 to 10 L/min
# ---------------------------------------------------------------------------------------------
X0, SX = -5.2, 0.55
Y0, SY = -2.4, 0.5


def P(p, q):
    return np.array([X0 + (p + 4) * SX, Y0 + q * SY, 0.0])


def plot_axes():
    g = VGroup()
    g.add(Line(P(-4, 0), P(10.4, 0), color=GREY, stroke_width=3))
    g.add(Line(P(-4, 0), P(-4, 10.4), color=GREY, stroke_width=3))
    for p in range(-4, 11, 2):
        g.add(Line(P(p, 0), P(p, 0) + DOWN * 0.1, color=GREY, stroke_width=2))
        g.add(M(str(p), 22, GREY).move_to(P(p, 0) + DOWN * 0.38))
    for q in range(0, 11, 2):
        g.add(Line(P(-4, q), P(-4, q) + LEFT * 0.1, color=GREY, stroke_width=2))
        g.add(M(str(q), 22, GREY).move_to(P(-4, q) + LEFT * 0.38))
    g.add(T("right atrial pressure, Pra (mmHg)", 24, GREY).move_to([P(3, 0)[0], -3.3, 0]))
    g.add(T("flow (L/min)", 24, GREY).rotate(PI / 2).move_to([-6.05, P(0, 5)[1], 0]))
    return g


def vline(pms, color=GREEN, w=6, dashed=False):
    a, b = P(0, pms), P(pms, 0)
    if dashed:
        return DashedLine(a, b, color=color, stroke_width=3, dash_length=0.15).set_opacity(0.55)
    return Line(a, b, color=color, stroke_width=w)


def hline(b, color=BLUE, w=6, dashed=False):
    a, c = P(0, b), P(9 - b, 9)
    if dashed:
        return DashedLine(a, c, color=color, stroke_width=3, dash_length=0.15).set_opacity(0.55)
    return Line(a, c, color=color, stroke_width=w)


def guide_h(q, p):
    return DashedLine(P(-4, q), P(p, q), color=YELLOW, stroke_width=3, dash_length=0.12)


def guide_v(p, q):
    return DashedLine(P(p, 0), P(p, q), color=YELLOW, stroke_width=3, dash_length=0.12)


def guides(p, q):
    return VGroup(guide_h(q, p), guide_v(p, q))


def op_dot(p, q):
    return Dot(P(p, q), radius=0.15, color=YELLOW)


def collapse_band():
    r = Rectangle(width=2 * SX, height=10 * SY, stroke_width=0, fill_color=RED, fill_opacity=0.2)
    r.move_to((P(-4, 0) + P(-2, 10)) / 2)
    return r


def legend(rows, y0=-2.35):
    g = VGroup()
    for i, (txt, col) in enumerate(rows):
        y = y0 - 0.5 * i
        g.add(Line([3.1, y, 0], [3.6, y, 0], color=col, stroke_width=6))
        g.add(T(txt, 22, col).move_to([3.75, y, 0], aligned_edge=LEFT))
    return g


def vr_equation(x=3.0, y=0.5, color=GREEN):
    lhs = M("Qvr =", 25, color)
    num = M("Pms - Pra", 25, color)
    den = M("Rvr", 25, color)
    bar = Line(LEFT, RIGHT, color=color, stroke_width=3).set_width(num.width + 0.2)
    frac = VGroup(num, bar, den).arrange(DOWN, buff=0.08)
    g = VGroup(lhs, frac).arrange(RIGHT, buff=0.2)
    return g.move_to([x + g.width / 2, y, 0])


# ---------------------------------------------------------------------------------------------
class S01Puzzle(SpokenScene):
    """a heart block and a veins block: out is capped by in, and a question over each."""

    def construct(self):
        veins = bchip("veins", GREEN, 46, pad=0.3).move_to([-4.9, -0.4, 0])
        heart = bchip("heart", BLUE, 46, pad=0.3).move_to([-0.1, -0.4, 0])
        out = arr(heart.get_right() + RIGHT * 0.05, [3.0, -0.4, 0], YELLOW, w=9, tip=0.28)
        pumped = T("pumped out", 26, YELLOW).next_to(out, UP, buff=0.14)
        five = T("about 5 L/min", 34, YELLOW).move_to([4.85, -0.15, 0])
        rest = T("adult at rest", 26, GREY).move_to([4.85, -0.7, 0])
        inn = arr(veins.get_right() + RIGHT * 0.05, heart.get_left() + LEFT * 0.05, GREEN, w=9, tip=0.28)
        back = T("flows back in", 28, GREEN).next_to(inn, UP, buff=0.14)

        self.play(FadeIn(heart, scale=0.9), run_time=0.5)
        self.at("blood a minute")
        self.play(GrowArrow(out), FadeIn(pumped), run_time=0.5)
        self.play(FadeIn(five, shift=RIGHT * 0.1), FadeIn(rest), run_time=0.5)
        self.at("cannot pump out")
        self.play(Indicate(VGroup(out, pumped), color=YELLOW, scale_factor=1.08), run_time=0.7)
        self.at("flows back in")
        self.play(FadeIn(veins, shift=RIGHT * 0.2), GrowArrow(inn), FadeIn(back), run_time=0.7)
        cap = T("over any few minutes, out cannot exceed back in", 30, TEXT).move_to([0, -2.3, 0])
        self.play(FadeIn(cap, shift=UP * 0.1), run_time=0.5)
        self.at("what sets cardiac output")
        head = T("What sets cardiac output?", 48, font=TITLE_FONT).move_to([0, 2.95, 0])
        qh = T("?", 84, TEXT, weight=BOLD).move_to([heart.get_center()[0], 1.2, 0])
        qv = T("?", 84, TEXT, weight=BOLD).move_to([veins.get_center()[0], 1.2, 0])
        self.play(Write(head), FadeIn(qh, scale=0.6), FadeIn(qv, scale=0.6), run_time=1.0)
        self.at("the heart")
        self.play(Indicate(heart, color=BLUE, scale_factor=1.15), run_time=0.7)
        self.at("or the veins")
        self.play(Indicate(veins, color=GREEN, scale_factor=1.15), run_time=0.7)
        self.finish()


# ---------------------------------------------------------------------------------------------
class S02Fick(SpokenScene):
    """oxygen bookkeeping: what the lungs take up leaves in the blood; 195 - 143 = 52; 260 / 52 = 5.0 L/min."""

    def construct(self):
        lungs = RoundedRectangle(corner_radius=0.2, width=3.4, height=1.8, stroke_color=GREY, stroke_width=4,
                                 fill_color=GREY, fill_opacity=0.15).move_to([0, 2.2, 0])
        lung_l = T("lungs", 36, TEXT).move_to(lungs)
        self.play(FadeIn(lungs), FadeIn(lung_l), run_time=0.6)

        # --- uptake in, leaves in the blood -----------------------------------------------------
        up_arrow = arr([0, 0.55, 0], [0, 1.25, 0], TEAL, w=8)
        dots = VGroup(*[Dot([0, 0.2, 0], radius=0.11, color=TEAL) for i in range(3)])
        self.at("the lungs take up")
        self.play(GrowArrow(up_arrow), FadeIn(dots), run_time=0.3)
        self.play(LaggedStart(*[d.animate.move_to([0, 1.4, 0]) for d in dots], lag_ratio=0.25), run_time=0.9)
        in_arrow = arr([-6.1, 2.1, 0], [-1.85, 2.1, 0], YELLOW, w=8)
        out_arrow = arr([1.85, 2.1, 0], [6.1, 2.1, 0], YELLOW, w=8)
        out_dots = VGroup(*[Dot([1.9, 2.1, 0], radius=0.11, color=TEAL) for _ in range(3)])
        self.at("leaves in the blood")
        self.play(FadeOut(dots), GrowArrow(out_arrow), GrowArrow(in_arrow),
                  LaggedStart(*[AnimationGroup(FadeIn(d), d.animate.move_to([5.7, 2.1, 0])) for d in out_dots], lag_ratio=0.2),
                  run_time=1.0)

        eq = T("Fick: flow = uptake / (arterial - mixed-venous)", 32, TEXT).move_to([0, -0.55, 0])
        self.at("flowing through them")
        self.play(FadeOut(out_dots), FadeIn(eq, shift=UP * 0.1), run_time=0.6)
        tag = T("made-up numbers: adult at rest, supine, no shunt", 24, GREY).move_to([0, -3.3, 0])
        self.at("made up numbers")
        self.play(FadeIn(tag), run_time=0.4)

        # --- the three numbers -------------------------------------------------------------------
        up_lbl = T("oxygen uptake: 260 mL O2/min", 28, TEAL).move_to([0.45, 0.75, 0], aligned_edge=LEFT)
        self.at("uptake is")
        self.play(FadeIn(up_lbl, shift=UP * 0.1), Indicate(up_arrow, color=TEAL), run_time=0.7)
        art_lbl = T("arterial blood", 26, GREY).move_to([3.95, 2.65, 0])
        art_n = T("195 mL O2/L", 34, TEAL).move_to([3.95, 1.5, 0])
        self.at("arterial blood holds")
        self.play(FadeIn(art_lbl), FadeIn(art_n, shift=UP * 0.1), run_time=0.6)
        mv_lbl = VGroup(T("mixed-venous blood", 26, GREY), T("from the pulmonary artery", 24, GREY)).arrange(DOWN, buff=0.05)
        mv_lbl.move_to([-3.95, 2.95, 0])
        mv_n = T("143 mL O2/L", 34, TEAL).move_to([-3.95, 1.5, 0])
        self.at("pulmonary artery")
        self.play(FadeIn(mv_lbl), run_time=0.5)
        self.at("holds", nth=1)
        self.play(FadeIn(mv_n, shift=UP * 0.1), run_time=0.5)

        diff = T("195 - 143 = 52 mL O2/L", 38, TEAL).move_to([0, -1.5, 0])
        self.at("the difference is")
        self.play(FadeIn(diff, shift=UP * 0.1), run_time=0.6)
        res = T("260 / 52 = 5.0 L/min", 46, YELLOW, weight=BOLD).move_to([0, -2.5, 0])
        self.at("divided by")
        self.play(FadeIn(res, shift=UP * 0.1), run_time=0.6)
        self.play(Indicate(in_arrow, color=YELLOW), Indicate(out_arrow, color=YELLOW), run_time=0.8)
        self.finish()


# ---------------------------------------------------------------------------------------------
class S03Tank(SpokenScene):
    """the veins as a tank: unstressed below the outlet rim, stressed above; adding blood raises the pressure."""

    def construct(self):
        x0, x1, ybot, ytop = -3.9, -0.9, -2.9, 2.6
        rim, level = -0.9, 1.1
        w = x1 - x0

        heart = bchip("heart stopped: no flow", BLUE, 24).move_to([3.2, 2.9, 0])
        self.at("stop the heart")
        self.play(FadeIn(heart, shift=DOWN * 0.1), run_time=0.6)

        wall = VMobject(color=GREY, stroke_width=7).set_points_as_corners(
            [[x0, ytop, 0], [x0, ybot, 0], [x1, ybot, 0], [x1, ytop, 0]])
        unst = Rectangle(width=w - 0.1, height=rim - ybot, stroke_width=0, fill_color=GREEN, fill_opacity=0.22)
        unst.move_to([(x0 + x1) / 2, (rim + ybot) / 2 + 0.03, 0])
        st = Rectangle(width=w - 0.1, height=level - rim, stroke_width=0, fill_color=GREEN, fill_opacity=0.6)
        st.move_to([(x0 + x1) / 2, (level + rim) / 2, 0])
        lvl = Line([x0, level, 0], [x1, level, 0], color=GREEN, stroke_width=5)
        res_lbl = T("systemic circulation as one reservoir", 22, GREY).move_to([(x0 + x1) / 2, -3.3, 0])
        self.at("one pressure")
        self.play(Create(wall), run_time=0.5)
        self.play(FadeIn(unst), FadeIn(st), Create(lvl), FadeIn(res_lbl), run_time=0.8)

        pms = VGroup(T("Pms", 48, GREEN, weight=BOLD), T("mean systemic filling pressure", 24, GREY)).arrange(DOWN, buff=0.05)
        pms.move_to([3.3, level, 0])
        pms_arrow = arr([pms.get_left()[0] - 0.05, level, 0], [x1 + 0.05, level, 0], GREEN)
        self.at("mean systemic")
        self.play(FadeIn(pms, shift=LEFT * 0.1), GrowArrow(pms_arrow), run_time=0.7)

        rimline = DashedLine([x0, rim, 0], [x1 + 0.6, rim, 0], color=GREY, stroke_width=4, dash_length=0.15)
        rim_lbl = T("outlet rim", 26, GREY).move_to([x1 + 0.75, rim, 0], aligned_edge=LEFT)
        self.at("outlet rim")
        self.play(Create(rimline), FadeIn(rim_lbl), run_time=0.6)

        un_lbl = T("unstressed volume", 30, GREEN).move_to([0.7, -1.9, 0], aligned_edge=LEFT)
        un_ar = arr(un_lbl.get_left() + LEFT * 0.0, [x1 - 0.2, -1.9, 0], GREEN, w=4)
        self.at("unstressed volume")
        self.play(FadeIn(un_lbl), GrowArrow(un_ar), unst.animate.set_fill(opacity=0.4), run_time=0.6)
        no_st = T("fills without stretching the walls", 22, GREY).move_to([0.7, -2.35, 0], aligned_edge=LEFT)
        self.at("stretching the walls")
        self.play(FadeIn(no_st), run_time=0.4)

        st_lbl = T("stressed volume", 30, GREEN).move_to([0.7, 0.05, 0], aligned_edge=LEFT)
        st_ar = arr(st_lbl.get_left(), [x1 - 0.2, 0.05, 0], GREEN, w=4)
        self.at("stressed volume")
        self.play(FadeOut(no_st), unst.animate.set_fill(opacity=0.22), FadeIn(st_lbl), GrowArrow(st_ar),
                  st.animate.set_fill(opacity=0.8), run_time=0.6)
        out_l = arr([x0 + 0.5, 0.05, 0], [x0 - 0.55, 0.05, 0], GREEN, w=5)
        out_r = arr([x1 - 0.5, -0.45, 0], [x1 + 0.2, -0.45, 0], GREEN, w=5)
        self.at("stretches them")
        self.play(GrowArrow(out_l), run_time=0.5)
        in_l = arr([x0 - 0.55, 0.05, 0], [x0 + 0.5, 0.05, 0], GREEN, w=5)
        self.at("pushes back")
        self.play(ReplacementTransform(out_l, in_l), st.animate.set_fill(opacity=0.6), run_time=0.7)

        # --- adding blood ------------------------------------------------------------------------
        add = T("add blood", 26, GREEN).move_to([(x0 + x1) / 2, 3.15, 0])
        drops = VGroup(*[Dot([x0 + 0.5 + i * 0.7, 2.9, 0], radius=0.1, color=GREEN) for i in range(4)])
        new_level = 1.6
        st2 = Rectangle(width=w - 0.1, height=new_level - rim, stroke_width=0, fill_color=GREEN, fill_opacity=0.6)
        st2.move_to([(x0 + x1) / 2, (new_level + rim) / 2, 0])
        lvl2 = Line([x0, new_level, 0], [x1, new_level, 0], color=GREEN, stroke_width=5)
        self.at("adding blood")
        self.play(FadeIn(add), FadeIn(drops), run_time=0.4)
        self.play(*[d.animate.move_to([d.get_center()[0], new_level + 0.05, 0]) for d in drops],
                  Transform(st, st2), Transform(lvl, lvl2),
                  pms.animate.shift(UP * (new_level - level)),
                  Transform(pms_arrow, arr([pms.get_left()[0] - 0.05, new_level, 0], [x1 + 0.05, new_level, 0], GREEN)),
                  run_time=1.0)
        self.play(FadeOut(drops), run_time=0.3)
        note1 = T("6 to 7 mmHg in anaesthetized dogs", 26, GREEN).move_to([3.5, -2.7, 0])
        note2 = T("a dog value, not a normal human one", 24, GREY).move_to([3.5, -3.15, 0])
        self.at("measured about")
        self.play(FadeIn(note1, shift=UP * 0.1), run_time=0.6)
        self.at("a dog value")
        self.play(FadeIn(note2, shift=UP * 0.1), run_time=0.5)
        self.finish()


# ---------------------------------------------------------------------------------------------
class S04Veins(SpokenScene):
    """the bypass preparation, then the venous return line from the equation, the collapse zone, Qvr."""

    def construct(self):
        tag = T("anaesthetized, open-chest dogs", 28, GREY).move_to([0, 2.7, 0])
        rh = bchip("right heart", BLUE, 34).move_to([0.3, 0.2, 0])
        self.at("replaced the right heart")
        self.play(FadeIn(rh, shift=DOWN * 0.1), FadeIn(tag), run_time=0.6)
        pump = bchip("external pump", GREY, 30).move_to([0.3, 0.2, 0])
        atrium = bchip("right atrium", BLUE, 30).move_to([-3.6, 0.2, 0])
        pa = bchip("pulmonary artery", GREY, 30).move_to([4.5, 0.2, 0])
        a_in = arr([-6.2, 0.2, 0], atrium.get_left() + LEFT * 0.0, GREEN, w=6)
        a_ap = arr(atrium.get_right(), pump.get_left(), GREY, w=6)
        a_pp = arr(pump.get_right(), pa.get_left(), GREY, w=6)
        ret_l = T("return from\nthe body", 24, GREEN, line_spacing=0.8).move_to([-5.3, 1.2, 0])
        self.at("external pump")
        self.play(ReplacementTransform(rh, pump), run_time=0.6)
        self.play(FadeIn(atrium), FadeIn(pa), GrowArrow(a_ap), GrowArrow(a_pp), GrowArrow(a_in), FadeIn(ret_l), run_time=0.8)
        set_l = T("pressure set by the experimenters", 24, TEXT).move_to([-3.2, -0.75, 0])
        self.at("set right atrial pressure")
        self.play(Indicate(atrium, color=BLUE, scale_factor=1.12), FadeIn(set_l, shift=UP * 0.1), run_time=0.7)
        meas = T("flow measured", 24, GREEN).move_to([-5.3, -0.35, 0])
        self.at("measured the return")
        self.play(FadeIn(meas), Indicate(a_in, color=GREEN), run_time=0.6)

        # --- the plot ----------------------------------------------------------------------------
        axes = plot_axes()
        strip = VGroup(tag, pump, atrium, pa, a_in, a_ap, a_pp, ret_l, set_l, meas)
        self.at("as they lowered")
        self.play(FadeOut(strip), FadeIn(axes), run_time=0.8)
        note = VGroup(T("illustrative model:", 22, GREY), T("Pms = 7 mmHg", 24, GREEN),
                      T("Rvr = 1 mmHg min/L", 24, GREEN)).arrange(DOWN, aligned_edge=LEFT, buff=0.1)
        note.move_to([3.0 + note.width / 2, 2.2, 0])
        line = vline(7)
        dot = Dot(P(7, 0), radius=0.14, color=GREEN)
        self.add(dot)
        self.at("roughly straight line")
        trace = Line(P(7, 0), P(0, 7), color=GREEN, stroke_width=6)
        self.play(Create(trace), dot.animate.move_to(P(0, 7)), run_time=1.6, rate_func=linear)
        # beyond Pra = 0 the same equation, dashed, to the collapse zone (model extrapolation, no data drawn)
        ext = DashedLine(P(0, 7), P(-2, 9), color=GREEN, stroke_width=4, dash_length=0.15)
        band = collapse_band()
        band_l = T("veins collapse:", 24, RED).move_to([-6.0, 3.15, 0], aligned_edge=LEFT)
        band_l2 = T("return stops rising", 24, RED).next_to(band_l, RIGHT, buff=0.15)
        ext_l = T("sketch extension, not measured", 22, GREY).move_to(P(-0.3, 9.1), aligned_edge=LEFT)
        self.at("stopped rising")
        self.play(Create(ext), FadeIn(band), FadeIn(ext_l), run_time=0.9)
        self.at("veins collapse")
        self.play(FadeIn(band_l), FadeIn(band_l2), run_time=0.6)
        # back up the line to zero flow
        pms_pt = Dot(P(7, 0), radius=0.1, color=GREEN)
        pms_lbl = T("Pra = Pms:\nno return", 24, GREEN, line_spacing=0.8).move_to(P(8.4, 1.5))
        self.at("reached zero")
        self.play(FadeOut(ext), FadeOut(ext_l), dot.animate.move_to(P(7, 0)), run_time=1.3)
        self.play(FadeIn(pms_lbl, shift=UP * 0.1), run_time=0.5)
        eq = vr_equation(3.0, 0.3)
        self.at("that line is")
        self.play(FadeIn(eq, shift=LEFT * 0.1), FadeIn(note), run_time=0.8)
        rv = T("Rvr: resistance to\nvenous return", 22, GREEN, line_spacing=0.8).move_to([3.0, -1.0, 0], aligned_edge=LEFT)
        rv.move_to([3.0 + rv.width / 2, -0.95, 0])
        self.at("resistance to")
        self.play(FadeIn(rv, shift=UP * 0.1), run_time=0.5)
        self.finish()


# ---------------------------------------------------------------------------------------------
class S05Cross(SpokenScene):
    """add the heart's line; where they cross is the operating point (illustrative model)."""

    def construct(self):
        axes = plot_axes()
        band = collapse_band()
        vein = vline(7)
        note = VGroup(T("illustrative model:", 22, GREY), T("Pms = 7 mmHg", 24, GREEN),
                      T("Rvr = 1 mmHg min/L", 24, GREEN)).arrange(DOWN, aligned_edge=LEFT, buff=0.1)
        note.move_to([3.0 + note.width / 2, 2.2, 0])
        eq = vr_equation(3.0, 0.3)
        self.add(axes, band, vein, note, eq)
        heart = hline(3)
        h_note = T("heart line valid for\npositive Pra only", 22, GREY, line_spacing=0.8).move_to([4.65, -1.7, 0])
        lg = legend([("heart: 3 + Pra", BLUE), ("veins: 7 - Pra", GREEN)])
        self.at("has a curve")
        self.play(Create(heart), FadeOut(band), FadeOut(eq), run_time=1.0)
        self.play(FadeIn(lg), FadeIn(h_note), run_time=0.3)
        more = T("more filling,\nmore output", 24, BLUE, line_spacing=0.8).move_to(P(5.6, 5.9))
        self.at("higher atrial pressure")
        self.play(FadeIn(more, shift=UP * 0.1), Indicate(heart, color=BLUE, scale_factor=1.0), run_time=0.8)
        self.at("averaged over time")
        eqo = T("output =\nvenous return", 28, YELLOW, line_spacing=0.8).move_to([4.65, 0.55, 0])
        self.play(FadeOut(more), FadeOut(h_note), FadeIn(eqo, shift=UP * 0.1), run_time=0.6)
        dot = op_dot(2, 5)
        ring = Circle(radius=0.3, color=YELLOW, stroke_width=4).move_to(P(2, 5))
        self.at("settles where")
        self.play(FadeIn(dot, scale=0.4), Create(ring), run_time=0.7)
        self.play(FadeOut(ring), run_time=0.3)
        self.at("illustrative model")
        self.play(Indicate(note, color=GREY, scale_factor=1.05), run_time=0.7)
        solve = T("3 + Pra = 7 - Pra", 30, TEXT).move_to([4.65, -0.1, 0])
        self.at("plus atrial pressure")
        self.play(FadeOut(eqo), FadeIn(solve, shift=UP * 0.1), run_time=0.6)
        g = guides(2, 5)
        r1 = T("Pra = 2 mmHg", 28, YELLOW, weight=BOLD).move_to([4.65, -0.7, 0])
        r2 = T("output = 5 L/min", 28, YELLOW, weight=BOLD).move_to([4.65, -1.2, 0])
        self.at("that gives")
        self.play(Create(g), FadeIn(r1, shift=UP * 0.1), run_time=0.8)
        self.play(FadeIn(r2, shift=UP * 0.1), run_time=0.6)
        self.finish()


# ---------------------------------------------------------------------------------------------
class S06Move(SpokenScene):
    """move one line at a time: stronger heart, weaker heart, then the veins' line after days; the rule."""

    def construct(self):
        axes = plot_axes()
        heart = hline(3)
        vein = vline(7)
        dot = op_dot(2, 5)
        gh, gv = guide_h(5, 2), guide_v(2, 5)
        lg = legend([("heart's line", BLUE), ("veins' line", GREEN)])
        tag = T("illustrative model", 22, GREY).move_to([4.65, 3.1, 0])
        self.add(axes, vein, heart, gh, gv, dot, lg, tag)

        def case(txt, col):
            return bchip(txt, col, 26).move_to([4.65, 2.35, 0])

        lab_pra = T("Pra", 28, GREY).move_to([3.1, 0.95, 0], aligned_edge=LEFT)
        lab_q = T("Output", 28, GREY).move_to([3.1, 0.4, 0], aligned_edge=LEFT)

        def val(txt, y):
            known = txt != "?"
            return T(txt, 30, YELLOW if known else GREY).move_to([4.6, y, 0], aligned_edge=LEFT)

        cur = {"p": val("2 mmHg", 0.95), "q": val("5 L/min", 0.4)}

        def setv(pra=None, q=None):
            """animations that replace the value cells (only the ones given); a '?' resets a cell."""
            anims = []
            if pra is not None:
                new = val(pra, 0.95)
                anims.append(ReplacementTransform(cur["p"], new)); cur["p"] = new
            if q is not None:
                new = val(q, 0.4)
                anims.append(ReplacementTransform(cur["q"], new)); cur["q"] = new
            return anims

        chip_now = case("baseline", GREY)
        self.play(FadeIn(chip_now), FadeIn(lab_pra), FadeIn(lab_q), FadeIn(cur["p"]), FadeIn(cur["q"]), run_time=0.5)

        # --- 1. stronger heart -------------------------------------------------------------------
        self.at("move one line")
        self.play(Indicate(heart, color=BLUE, scale_factor=1.0), Indicate(vein, color=GREEN, scale_factor=1.0), run_time=0.8)
        ghost_h = hline(3, GREY, dashed=True)
        c1 = case("stronger heart", BLUE)
        self.at("stronger heart")
        self.add(ghost_h)
        self.play(ReplacementTransform(chip_now, c1), FadeOut(gh), FadeOut(gv), *setv("?", "?"), run_time=0.5)
        self.at("lifts its line")
        self.play(Transform(heart, hline(5)), dot.animate.move_to(P(1, 6)), run_time=1.0)
        self.at("output rises")
        gh = guide_h(6, 1)
        self.play(Create(gh), *setv(None, "6 L/min"), run_time=0.4)
        self.at("atrial pressure falls")
        gv = guide_v(1, 6)
        self.play(Create(gv), *setv("1 mmHg"), run_time=0.4)

        # --- 2. weaker heart: clear the old answer first -----------------------------------------
        c2 = case("weaker heart", BLUE)
        self.at("weaker heart")
        self.play(ReplacementTransform(c1, c2), FadeOut(ghost_h),
                  Transform(heart, hline(3)), dot.animate.move_to(P(2, 5)), FadeOut(gh), FadeOut(gv),
                  *setv("?", "?"), run_time=0.8)
        ghost_h2 = hline(3, GREY, dashed=True)
        self.add(ghost_h2)
        self.at("drops it")
        self.play(Transform(heart, hline(1)), dot.animate.move_to(P(3, 4)), run_time=1.0)
        self.at("output falls")
        gh = guide_h(4, 3)
        self.play(Create(gh), *setv(None, "4 L/min"), run_time=0.4)
        self.at("pressure rises")
        gv = guide_v(3, 4)
        self.play(Create(gv), *setv("3 mmHg"), run_time=0.4)

        # --- 3. over days: the veins' line moves --------------------------------------------------
        c3 = case("hours to days", GREEN)
        base_ring = Circle(radius=0.22, color=GREY, stroke_width=3).move_to(P(2, 5))
        ghost_v = vline(7, GREY, dashed=True)
        self.at("over hours")
        self.add(ghost_v)
        self.play(ReplacementTransform(c2, c3), FadeOut(ghost_h2), FadeIn(base_ring), FadeOut(gh), FadeOut(gv), *setv("?", "?"), run_time=0.6)
        self.at("salt and water")
        self.play(Transform(vein, vline(9)), dot.animate.move_to(P(4, 5)), run_time=1.2)
        self.at("back to")
        gh = guide_h(5, 4)
        self.play(Create(gh), *setv(None, "5 L/min"), run_time=0.4)
        self.at("atrial pressure at")
        gv = guide_v(4, 5)
        self.play(Create(gv), *setv("4 mmHg"), run_time=0.4)

        # --- the rule ----------------------------------------------------------------------------
        rule = T("output sits\nwhere the two\nlines cross", 32, YELLOW, font=TITLE_FONT, line_spacing=0.9).move_to([4.65, 1.0, 0])
        self.at("the rule to keep")
        self.play(FadeOut(c3), FadeOut(lab_pra), FadeOut(lab_q), FadeOut(cur["p"]), FadeOut(cur["q"]), FadeOut(ghost_v), FadeOut(base_ring), run_time=0.5)
        self.play(FadeIn(rule, shift=UP * 0.1), Indicate(dot, color=YELLOW, scale_factor=1.8), run_time=0.9)
        self.finish()


class S07End(EndCard):
    LINE = "Output sits where the heart's line crosses the veins' line."
