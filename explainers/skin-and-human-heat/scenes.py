"""Skin and human heat: sweat cools only when it evaporates  (Biochemistrypedia explainer)

Timed to the SPOKEN words: every self.at("...") cue waits for that phrase in audio/words.json.

COLOR MAP (one color per concept, whole video)
  ORANGE = heat made by the body (metabolic rate, heat after external work) and the heat that must be removed
  PURPLE = dry exchange (radiant, convective, conductive): the 50 W dry heat gain
  BLUE   = evaporation: sweat that evaporates, evaporative loss E
  GREY   = sweat that drips (no cooling), skin, structure, notes
  YELLOW = the humid-air cap on evaporation, and emphasis
  RED    = stored heat S and the rise in body temperature
  GREEN  = balance: storage zero, body temperature steady
  TEAL   = body mass (water lost without drinking)
Every number is the lesson's worked problem (illustrative: 70 kg adult cycling in hot, sunny air) or its
latent heat and specific heat. The plot in the last scene is a sketch of the lesson's statement, not data.
"""
import numpy as np
from bp_style import *  # noqa: F401,F403

ORANGE = "#F29E4C"
PURPLE = "#B58CD9"

X0 = -4.6          # left end of the watt bars
SC = 0.0083        # scene units per watt
Y_IN, Y_OUT = 1.0, -1.2


def arr(a, b, color=GREY, w=5, tip=0.2):
    return Arrow(a, b, buff=0.06, color=color, stroke_width=w, tip_length=tip,
                 max_tip_length_to_length_ratio=0.45, max_stroke_width_to_length_ratio=12)


def seg(w0, w1, y, color, h=1.0, x0=X0, sc=SC, fill=0.4):
    """A horizontal bar covering w0..w1 watts."""
    r = Rectangle(width=(w1 - w0) * sc, height=h, stroke_color=color, stroke_width=3, fill_color=color, fill_opacity=fill)
    return r.move_to([x0 + (w0 + w1) / 2 * sc, y, 0])


def drop(x, y, r=0.5, color=BLUE):
    c = Circle(radius=r, stroke_width=0, fill_color=color, fill_opacity=1)
    t = Polygon([0, 1.95 * r, 0], [-0.86 * r, 0.5 * r, 0], [0.86 * r, 0.5 * r, 0], stroke_width=0,
                fill_color=color, fill_opacity=1)
    return VGroup(c, t).move_to([x, y, 0])


def wiggle(x, y0, y1, color=BLUE, amp=0.13, waves=3, w=5):
    f = lambda t: np.array([x + amp * np.sin(t * waves * TAU), y0 + (y1 - y0) * t, 0])
    return ParametricFunction(f, t_range=[0, 1, 0.01], color=color, stroke_width=w)


def skin_block(x, y=-2.2, w=4.4):
    r = Rectangle(width=w, height=0.6, stroke_color=GREY, stroke_width=3, fill_color=GREY, fill_opacity=0.3).move_to([x, y, 0])
    return VGroup(r, T("skin", 24, GREY).move_to(r))


class S00Title(TitleCard):
    LESSON = "Skin, sweat and human thermoregulation"
    TITLE = "Sweat cools only when it evaporates"


# ---------------------------------------------------------------------------------------------
class S01Drip(SpokenScene):
    """Two drops: one evaporates and takes heat, one drips. Then vapour uptake lags muscle heat."""

    def construct(self):
        sL, sR = skin_block(-3.4), skin_block(3.4)
        dL = drop(-3.4, -1.45)
        dR = drop(3.0, -1.45)
        self.at("A gram of sweat")
        self.play(FadeIn(sL), FadeIn(sR), FadeIn(dL, shift=DOWN * 0.2), FadeIn(dR, shift=DOWN * 0.2), run_time=0.8)

        hL = T("evaporates", 38, BLUE, weight=BOLD).move_to([-3.4, 3.05, 0])
        self.at("that evaporates")
        vap = VGroup(*[wiggle(x, -1.3, 1.4, amp=0.15) for x in (-4.4, -3.4, -2.4)])
        self.play(FadeIn(hL), ReplacementTransform(dL, vap), run_time=1.1)
        heat = VGroup(*[arr([x, -1.1, 0], [x, 1.4, 0], ORANGE, 8, 0.3) for x in (-3.9, -2.9)])
        tL = T("carries off about 2.4 kJ\nof heat per gram", 28, ORANGE, line_spacing=0.8).move_to([-3.4, 2.2, 0])
        self.at("carries off about")
        self.play(GrowArrow(heat[0]), GrowArrow(heat[1]), FadeIn(tL, shift=DOWN * 0.1), run_time=0.9)

        hR = T("drips", 38, GREY, weight=BOLD).move_to([3.4, 3.05, 0])
        self.at("that drips off")
        self.play(FadeIn(hR), dR.animate.move_to([5.75, -1.45, 0]), run_time=0.35)
        self.play(dR.animate.move_to([5.75, -3.15, 0]), run_time=0.35)
        tR = T("carries away\nalmost none", 28, GREY, line_spacing=0.8).move_to([3.4, 2.2, 0])
        self.at("carries away")
        self.play(FadeIn(tR, shift=DOWN * 0.1), run_time=0.6)

        self.at("So the cooling comes")
        self.play(Indicate(VGroup(hL, vap), color=BLUE, scale_factor=1.06), run_time=1.0)

        # phase 2: vapour uptake lags muscle heat
        self.at("Sweat cools you")
        self.play(*[FadeOut(m) for m in (sL, sR, hL, tL, hR, tR, vap, heat, dR)], run_time=0.6)
        xl = -4.4
        lab1 = T("air takes up water vapour", 32, BLUE).move_to([xl + 2.5, 2.3, 0])
        lab2 = T("heat your muscles make", 32, ORANGE).move_to([xl + 2.5, -0.35, 0])
        b1 = Rectangle(width=4.0, height=1.1, stroke_color=BLUE, stroke_width=3, fill_color=BLUE, fill_opacity=0.4)
        b1.move_to([xl + 2.0, 1.2, 0])
        b2 = Rectangle(width=8.8, height=1.1, stroke_color=ORANGE, stroke_width=3, fill_color=ORANGE, fill_opacity=0.4)
        b2.move_to([xl + 4.4, -1.3, 0])
        self.at("takes up")
        self.play(FadeIn(lab1), GrowFromEdge(b1, LEFT), run_time=0.9)
        day = chip("on a humid day", YELLOW, size=30).move_to([3.0, 2.3, 0])
        self.at("On a humid day")
        self.play(FadeIn(day, shift=DOWN * 0.1), run_time=0.5)
        self.play(FadeIn(lab2), GrowFromEdge(b2, LEFT), run_time=1.0)
        brace = DoubleArrow([xl + 4.05, 0.2, 0], [xl + 8.75, 0.2, 0], color=RED, buff=0, stroke_width=5, tip_length=0.18)
        lag = T("lags behind", 30, RED).move_to([xl + 6.4, 0.65, 0])
        self.at("lag behind")
        self.play(GrowFromCenter(brace), FadeIn(lag), run_time=0.7)
        nts = T("not to scale", 22, GREY).move_to([4.5, -2.75, 0])
        self.play(FadeIn(nts), run_time=0.3)
        self.finish()


# ---------------------------------------------------------------------------------------------
class S02Sum(SpokenScene):
    """The heat-balance sum, term by term; storage zero means steady temperature."""

    def construct(self):
        S = M("S", 52, RED, weight=BOLD)
        eq = M("=", 52)
        mw = M("(M - W)", 52, ORANGE)
        rck = M("± R ± C ± K", 52, PURPLE)
        e = M("- E", 52, BLUE)
        row = VGroup(S, eq, mw, rck, e).arrange(RIGHT, buff=0.42).move_to([0, 2.5, 0])
        row.shift(LEFT * (row.get_center()[0]))
        fit(row, max_w=12.2)

        def lab(text, piece, color, dy=0.95):
            return T(text, 26, color, line_spacing=0.8).move_to(piece.get_center() + DOWN * dy)

        lS = lab("heat\nstorage", S, RED, 1.0)
        lMW = lab("metabolic rate\nminus external work", mw, ORANGE, 1.0)
        lRCK = lab("dry exchange: radiant,\nconvective, conductive", rck, PURPLE, 1.0)
        lE = lab("evaporative\nloss", e, BLUE, 1.0)

        self.at("heat balance is a sum")
        self.play(FadeIn(S, scale=0.9), FadeIn(eq), run_time=0.6)
        self.at("Heat storage")
        self.play(FadeIn(lS), run_time=0.4)
        self.at("metabolic rate")
        self.play(FadeIn(mw, shift=LEFT * 0.2), FadeIn(lMW), run_time=0.7)
        self.at("dry exchange")
        self.play(FadeIn(rck, shift=LEFT * 0.2), run_time=0.6)
        self.at("minus evaporative loss")
        self.play(FadeIn(e, shift=LEFT * 0.2), FadeIn(lE), run_time=0.7)
        self.at("radiant")
        self.play(FadeIn(lRCK), run_time=0.6)
        watts = T("every term is in watts (W)", 28, GREY).move_to([0, 0.35, 0])
        self.at("in watts")
        self.play(FadeIn(watts), run_time=0.5)

        # balance bars
        yi, yo = -0.85, -2.45
        rl1 = T("heat in", 24, GREY).move_to([-5.45, yi, 0])
        rl2 = T("heat out", 24, GREY).move_to([-5.4, yo, 0])
        in1 = seg(0, 800, yi, ORANGE)
        in2 = seg(800, 850, yi, PURPLE)
        out = seg(0, 850, yo, BLUE)
        self.at("When storage is zero")
        self.play(FadeOut(watts), FadeIn(rl1), FadeIn(rl2), GrowFromEdge(in1, LEFT), GrowFromEdge(in2, LEFT),
                  GrowFromEdge(out, LEFT), run_time=1.2)
        z = M("S = 0", 44, GREEN, weight=BOLD).move_to([4.6, -0.85, 0])
        self.play(FadeIn(z, scale=0.9), run_time=0.5)
        steady = T("body temperature\nsteady", 30, GREEN).move_to([4.6, -2.2, 0])
        self.at("body temperature is steady")
        self.play(FadeIn(steady, shift=DOWN * 0.1), run_time=0.6)
        self.finish()


# ---------------------------------------------------------------------------------------------
class S03Heat(SpokenScene):
    """The worked problem: 1000 W metabolic, 200 W external work, 50 W dry gain, so 850 W to remove."""

    def construct(self):
        note = T("illustrative numbers: healthy 70 kg adult cycling steadily in hot, sunny air", 26, GREY).move_to([0, 3.1, 0])
        fit(note, max_w=12.2)
        rl1 = T("heat in", 26, GREY).move_to([-5.6, Y_IN, 0])
        rl2 = T("heat out", 26, GREY).move_to([-5.55, Y_OUT, 0])
        self.at("Take illustrative numbers")
        self.play(FadeIn(note), FadeIn(rl1), FadeIn(rl2), run_time=0.7)

        main = seg(0, 800, Y_IN, ORANGE)
        slice_ = seg(800, 1000, Y_IN, ORANGE)
        lM = T("metabolic rate: 1,000 W", 32, ORANGE).move_to([X0 + 500 * SC, Y_IN + 0.95, 0])
        self.at("Metabolic rate is")
        self.play(GrowFromEdge(VGroup(main, slice_), LEFT), FadeIn(lM), run_time=1.0)

        lW = T("external work: 200 W", 28, GREY).move_to([X0 + 900 * SC, Y_IN - 0.95, 0])
        self.at("becomes external work")
        self.play(slice_.animate.set_stroke(GREY).set_fill(GREY, 0.4), FadeIn(lW), run_time=0.7)

        lH = T("heat made: 800 W", 32, ORANGE).move_to([X0 + 400 * SC, Y_IN + 0.95, 0])
        self.at("That leaves")
        self.play(FadeOut(slice_), FadeOut(lW), ReplacementTransform(lM, lH), run_time=0.8)

        dry = seg(800, 850, Y_IN, PURPLE)
        lD = T("dry heat gain: 50 W", 28, PURPLE)
        lD.move_to([X0 + 850 * SC - 0.25 - lD.width / 2, Y_IN - 0.95, 0])
        self.at("Dry heat gain")
        self.play(GrowFromEdge(dry, LEFT), FadeIn(lD, shift=UP * 0.1), run_time=0.8)

        resp = T("respiratory heat loss ignored", 26, GREY).move_to([0, -3.2, 0])
        self.at("respiratory heat loss")
        self.play(FadeIn(resp), run_time=0.5)

        out = seg(0, 850, Y_OUT, BLUE)
        lE = T("evaporation must remove 850 W", 32, BLUE).move_to([X0 + 425 * SC, Y_OUT - 0.95, 0])
        guide = DashedLine([X0 + 850 * SC, Y_IN + 0.55, 0], [X0 + 850 * SC, Y_OUT - 0.55, 0], color=GREEN, stroke_width=3)
        z = M("S = 0", 46, GREEN, weight=BOLD).move_to([4.7, Y_OUT, 0])
        self.at("To keep storage")
        self.play(GrowFromEdge(out, LEFT), FadeIn(lE), run_time=1.2)
        self.play(Create(guide), FadeIn(z, scale=0.9), run_time=0.6)
        self.finish()


# ---------------------------------------------------------------------------------------------
class S04Sweat(SpokenScene):
    """850 W needs 1.26 L/h if all evaporates; 1.80 L/h if 70 percent evaporates and the rest drips."""

    def construct(self):
        latent = chip("evaporating sweat takes up about 2.43 kJ per g", BLUE, size=30).move_to([0, 2.95, 0])
        fit(latent, max_w=12.2)
        self.at("Evaporating sweat takes up")
        self.play(FadeIn(latent, shift=DOWN * 0.15), run_time=0.8)

        XL, SCL, yb = -6.0, 4.0, 0.7          # sweat bar: 4.0 units per L per hour
        axisl = T("sweat rate", 26, GREY).move_to([XL + 0.8, yb + 1.15, 0])
        b1 = Rectangle(width=1.26 * SCL, height=1.5, stroke_color=BLUE, stroke_width=3, fill_color=BLUE, fill_opacity=0.4)
        b1.move_to([XL + 0.63 * SCL, yb, 0])
        l1 = T("850 W needs 1.26 L per hour, if every gram evaporates", 30, BLUE).move_to([0, yb - 1.2, 0])
        self.at("needs about")
        self.play(FadeIn(axisl), GrowFromEdge(b1, LEFT), run_time=1.3)
        self.play(FadeIn(l1, shift=UP * 0.1), run_time=0.5)

        seven = T("70 percent evaporates", 30, BLUE).move_to([XL + 0.63 * SCL, yb + 0.0, 0])
        self.at("Suppose only")
        self.play(FadeIn(seven), FadeOut(l1), run_time=0.6)

        b2 = Rectangle(width=0.54 * SCL, height=1.5, stroke_color=GREY, stroke_width=3, fill_color=GREY, fill_opacity=0.4)
        b2.move_to([XL + 1.26 * SCL + 0.27 * SCL, yb, 0])
        rest = T("the rest drips", 28, GREY).move_to([XL + 1.26 * SCL + 0.27 * SCL, yb + 1.15, 0])
        self.at("the rest drips")
        self.play(GrowFromEdge(b2, LEFT), FadeIn(rest), run_time=0.8)

        l2 = T("1.80 L per hour", 44, TEXT, weight=BOLD).move_to([XL + 0.9 * SCL + 0.8, yb - 1.4, 0])
        up = arr([XL + 1.8 * SCL + 0.6, yb - 0.5, 0], [XL + 1.8 * SCL + 0.6, yb + 0.6, 0], TEXT, 7)
        self.at("The sweat rate then rises")
        self.play(FadeIn(l2, shift=UP * 0.1), GrowArrow(up), run_time=0.8)

        mass = T("without drinking: body mass falls about 2.6 percent in that hour", 34, TEAL)
        fit(mass, max_w=12.2)
        mass.move_to([0, -2.9, 0])
        self.at("Without drinking")
        self.play(FadeIn(mass, shift=UP * 0.1), run_time=0.8)
        self.finish()


# ---------------------------------------------------------------------------------------------
class S05Cap(SpokenScene):
    """Humid air caps evaporation at 700 W; the 150 W gap is stored: 540 kJ per h, 2.6 degrees C per h."""

    def construct(self):
        yi, yo = 2.15, 0.55
        rl1 = T("heat in", 26, GREY).move_to([-5.6, yi, 0])
        rl2 = T("heat out", 26, GREY).move_to([-5.55, yo, 0])
        in1, in2 = seg(0, 800, yi, ORANGE, h=0.9), seg(800, 850, yi, PURPLE, h=0.9)
        need = T("body needs 850 W", 30, ORANGE).move_to([X0 + 425 * SC, yi + 0.8, 0])
        self.add(rl1, rl2, in1, in2)

        out = seg(0, 700, yo, BLUE, h=0.9)
        cap = DashedLine([X0 + 700 * SC, yo + 0.6, 0], [X0 + 700 * SC, yo - 0.6, 0], color=YELLOW, stroke_width=6)
        capl = T("humid-air cap: 700 W", 28, YELLOW)
        capl.move_to([X0 + 700 * SC - 0.15 - capl.width / 2, yo - 0.85, 0])
        self.at("Now let humid air")
        self.play(GrowFromEdge(out, LEFT), run_time=0.7)
        self.at("cap evaporation")
        self.play(Create(cap), FadeIn(capl, shift=DOWN * 0.1), run_time=0.7)
        self.at("when the body needs")
        self.play(FadeIn(need, shift=DOWN * 0.1), run_time=0.6)

        gap = seg(700, 850, yo, RED, h=0.9, fill=0.55)
        gl = T("stored: 150 W", 30, RED)
        gl.move_to([X0 + 700 * SC + 0.4 + gl.width / 2, yo - 0.85, 0])
        self.at("The gap of")
        self.play(GrowFromEdge(gap, LEFT), FadeIn(gl), run_time=0.8)

        c1 = T("150 W × 3,600 s = 540 kJ per hour", 34, RED).move_to([0, -1.0, 0])
        self.at("in an hour")
        self.play(FadeIn(c1, shift=UP * 0.1), run_time=0.7)
        c2 = T("70 kg × 2.98 kJ per kg per °C ≈ 209 kJ per °C", 34, TEXT).move_to([0, -1.95, 0])
        self.at("Take")
        self.play(FadeIn(c2, shift=UP * 0.1), run_time=0.8)
        c3 = T("540 ÷ 209 ≈ 2.6 °C per hour", 46, RED, weight=BOLD).move_to([-0.6, -3.0, 0])
        up = arr([c3.get_right()[0] + 0.55, -3.4, 0], [c3.get_right()[0] + 0.55, -2.4, 0], RED, 9, 0.3)
        self.at("it rises about")
        self.play(FadeIn(c3, shift=UP * 0.1), GrowArrow(up), run_time=0.9)
        self.finish()


# ---------------------------------------------------------------------------------------------
class S06Rule(SpokenScene):
    """A sketch: evaporative cooling flattens at the cap; three ways to meet the need; the rule."""

    def construct(self):
        OX, OY = -5.3, -2.9
        XS, YS = 0.66, 0.0058            # units per relative unit, per watt (in this sketch)
        P = lambda x, w: np.array([OX + x * XS, OY + w * YS, 0])
        xax = Line(P(0, 0), P(10.3, 0), color=GREY, stroke_width=3)
        yax = Line(P(0, 0), P(0, 1000), color=GREY, stroke_width=3)
        xt = T("sweat secreted (relative units)", 26, GREY).move_to([OX + 5 * XS, OY - 0.5, 0])
        yt = T("evaporative cooling (W)", 26, GREY).rotate(PI / 2).move_to([OX - 0.55, OY + 500 * YS, 0])
        sk = T("in this sketch", 26, GREY).move_to([OX + 1.6, OY + 1000 * YS + 0.2, 0])
        cap_t, req_t = ValueTracker(700.0), ValueTracker(850.0)

        req = always_redraw(lambda: DashedLine(P(0, req_t.get_value()), P(10, req_t.get_value()), color=ORANGE, stroke_width=6))
        capl = always_redraw(lambda: DashedLine(P(0, cap_t.get_value()), P(10, cap_t.get_value()), color=YELLOW, stroke_width=6))

        def curve():
            c = cap_t.get_value()
            xk = 5.0 * c / 700.0
            m = VMobject(color=BLUE, stroke_width=8)
            m.set_points_as_corners([P(0, 0), P(xk, c), P(10, c)])
            return m
        cv = always_redraw(curve)

        def gapband():
            c, r = cap_t.get_value(), req_t.get_value()
            if r - c < 5:
                return VMobject()
            return Rectangle(width=0.45, height=(r - c) * YS, stroke_color=RED, stroke_width=2, fill_color=RED,
                             fill_opacity=0.55).move_to(P(9.7, (r + c) / 2))
        gb = always_redraw(gapband)

        rl = T("needed: 850 W", 28, ORANGE)
        rl.move_to([OX + 10.45 * XS + 0.1 + rl.width / 2, OY + 850 * YS, 0])
        cl = T("humid-air cap: 700 W", 28, YELLOW)
        cl.move_to([OX + 10.45 * XS + 0.1 + cl.width / 2, OY + 700 * YS, 0])

        self.at("Once evaporation")
        self.play(Create(xax), Create(yax), FadeIn(xt), FadeIn(yt), FadeIn(sk), run_time=0.9)
        self.add(req)
        self.play(FadeIn(rl), run_time=0.5)
        self.at("reaches the most")
        self.add(capl, cv)
        self.play(FadeIn(cl), run_time=0.5)
        self.add(gb)
        drips = VGroup(*[drop(P(x, 700)[0], P(x, 700)[1] - 0.45, r=0.2, color=GREY) for x in (6.4, 7.7, 9.0)])
        extra = T("extra sweat drips: no extra cooling", 28, GREY).move_to(P(8.4, 700) + DOWN * 1.55)
        self.at("sweating harder")
        self.play(FadeIn(drips, shift=DOWN * 0.1), FadeIn(extra), run_time=0.8)

        # three ways
        head = T("balance returns when\nthe two lines meet", 28, TEXT, line_spacing=0.9).move_to([4.5, 2.6, 0])
        self.at("three ways")
        self.play(FadeOut(drips), FadeOut(extra), FadeOut(rl), FadeOut(cl), FadeIn(head), run_time=0.7)
        def stat(txt, col):
            return T(txt, 32, col, weight=BOLD).move_to([4.5, -2.0, 0])

        def swap(old, new):
            return Succession(FadeOut(old, run_time=0.2), FadeIn(new, run_time=0.25))

        cur = stat("S > 0: heat stored", RED)
        self.play(FadeIn(cur), run_time=0.3)

        a1 = chip("make less heat:\nslow down", ORANGE, size=28).move_to([4.5, 0.9, 0])
        self.at("Make less heat")
        self.play(FadeIn(a1, shift=DOWN * 0.1), run_time=0.4)
        nxt = stat("S = 0", GREEN)
        self.play(req_t.animate.set_value(700.0), swap(cur, nxt), run_time=1.0)
        cur = nxt

        a2 = chip("less dry gain:\nshade or cooler air", PURPLE, size=28).move_to([4.5, 0.9, 0])
        self.at("less dry heat")
        nxt = stat("S > 0: heat stored", RED)
        self.play(FadeOut(a1), FadeIn(a2), req_t.animate.set_value(850.0), swap(cur, nxt), run_time=0.5)
        cur = nxt
        nxt = stat("S = 0", GREEN)
        self.play(req_t.animate.set_value(700.0), swap(cur, nxt), run_time=1.0)
        cur = nxt

        a3 = chip("drier air:\nhigher cap", YELLOW, size=28).move_to([4.5, 0.9, 0])
        self.at("Or have drier air")
        nxt = stat("S > 0: heat stored", RED)
        self.play(FadeOut(a2), FadeIn(a3), req_t.animate.set_value(850.0), swap(cur, nxt), run_time=0.5)
        cur = nxt
        nxt = stat("S = 0", GREEN)
        self.play(cap_t.animate.set_value(850.0), swap(cur, nxt), run_time=1.0)
        cur = nxt

        note = T("made-up numbers:\npredicts no real person", 28, GREY, line_spacing=0.9).move_to([4.5, -0.45, 0])
        self.at("made up for practice")
        self.play(FadeIn(note, shift=UP * 0.1), run_time=0.6)

        # the rule
        self.at("Keep this rule")
        everything = Group(*self.mobjects)
        self.play(FadeOut(everything), run_time=0.7)
        r1 = T("Sweat cools only when it evaporates", 44, TEXT, font=TITLE_FONT)
        fit(r1, max_w=12.0)
        r1.move_to([0, 0.7, 0])
        r2 = T("and the air sets how much can", 38, YELLOW, font=TITLE_FONT).move_to([0, -0.6, 0])
        self.play(FadeIn(r1, shift=UP * 0.15), run_time=0.8)
        self.at("the air sets")
        self.play(FadeIn(r2, shift=UP * 0.15), run_time=0.8)
        self.finish()


# ---------------------------------------------------------------------------------------------
class S07End(EndCard):
    LINE = "Sweat cools only when it evaporates, and the air sets how much."
