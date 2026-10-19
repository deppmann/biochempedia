"""The brain acts before the blood changes: homeostatic loops, threshold and gain, and feedforward thirst
(Biochemistrypedia explainer)

Timed to the SPOKEN words: every self.at("...") cue waits for that phrase in audio/words.json.
Every number on screen is the lesson's own: threshold 284 mOsm/kg and gain 0.43 pmol/L per mOsm/kg are
ILLUSTRATIVE AVERAGES (healthy adults, one summary) and say so on screen; the worked values 4.30, 2.58 and
-1.72 pmol/L are the lesson's. The mouse traces carry no data: only the timings the lesson gives (a fall
within one minute, blood still raised at five minutes) are drawn, and they are labelled "in this sketch".

COLOR MAP (one color per concept, whole video)
  BLUE   = blood (plasma osmolality, the regulated variable)
  YELLOW = thirst neurons (the sensor, the SFO Nos1 population activity) and thirst
  ORANGE = vasopressin (AVP), the hormone output
  GREEN  = excitatory arrow / activation (typed arrow: solid head)
  RED    = inhibitory arrow / "opposes" (typed arrow: bar end)
  TEAL   = feedback (negative feedback, a response to a measured error)
  GOLD   = feedforward (a response to an expected disturbance)
  GREY   = structure, axes, threshold line, comparator, flow arrows, ruled-out cases
"""
import numpy as np
from bp_style import *  # noqa: F401,F403

ORANGE = "#F29E4C"
BLOOD, NEUR, AVP, EXC, INH, FB, FF = BLUE, YELLOW, ORANGE, GREEN, RED, TEAL, GOLD

THR, GAIN = 284.0, 0.43


def avp(p):
    return GAIN * max(p - THR, 0.0)


# ---------------------------------------------------------------------------------------------
# helpers
# ---------------------------------------------------------------------------------------------
class Ax:
    def __init__(self, x0, x1, y0, y1, t0, t1, v0, v1):
        self.x0, self.x1, self.y0, self.y1, self.t0, self.t1, self.v0, self.v1 = x0, x1, y0, y1, t0, t1, v0, v1

    def X(self, t):
        return self.x0 + (t - self.t0) / (self.t1 - self.t0) * (self.x1 - self.x0)

    def Y(self, v):
        return self.y0 + (v - self.v0) / (self.v1 - self.v0) * (self.y1 - self.y0)

    def P(self, t, v):
        return np.array([self.X(t), self.Y(v), 0.0])


def poly(ax, pts, color, w=6):
    m = VMobject(stroke_color=color, stroke_width=w)
    m.set_points_as_corners([ax.P(a, b) for a, b in pts])
    return m


def dashed(p, q, color=GREY, w=2.5, op=0.9):
    return DashedLine(np.array(p, float), np.array(q, float), color=color, stroke_width=w, dash_length=0.12,
                      stroke_opacity=op)


def arr(a, b, color=GREY, w=6, tip=0.25):
    return Arrow(np.array(a, float), np.array(b, float), buff=0, color=color, stroke_width=w, tip_length=tip,
                 max_tip_length_to_length_ratio=0.5, max_stroke_width_to_length_ratio=14)


def inhib(a, b, color=INH, w=6, bar=0.26):
    """inhibitory arrow: a shaft ending in a bar across it."""
    a, b = np.array(a, float), np.array(b, float)
    d = (b - a) / np.linalg.norm(b - a)
    n = np.array([-d[1], d[0], 0.0])
    return VGroup(Line(a, b, color=color, stroke_width=w), Line(b + n * bar, b - n * bar, color=color, stroke_width=w + 2))


def bchip(text, color=BLUE, size=24, **kw):
    c = chip(text, color, size=size, **kw)
    back = RoundedRectangle(corner_radius=0.14, width=c[0].width, height=c[0].height, stroke_width=0,
                            fill_color=BG, fill_opacity=1).move_to(c[0])
    return VGroup(back, *c)


def backed(text, color, size, pad=0.12):
    t = T(text, size, color, weight=BOLD)
    r = Rectangle(width=t.width + 2 * pad, height=t.height + 2 * pad, stroke_width=0, fill_color=BG, fill_opacity=1).move_to(t)
    return VGroup(r, t)


def box(title, body, color, w, h, tsize=26, bsize=22):
    r = RoundedRectangle(corner_radius=0.16, width=w, height=h, stroke_color=color, stroke_width=3,
                         fill_color=color, fill_opacity=0.14)
    t = T(title, tsize, color, weight=BOLD)
    b = T(body, bsize, TEXT, line_spacing=0.8)
    g = VGroup(t, b).arrange(DOWN, buff=0.14).move_to(r)
    return VGroup(r, g)


def noisy(t, seed, amp):
    return amp * (np.sin(7.1 * t + seed) * 0.5 + np.sin(13.3 * t + 2 * seed) * 0.3 + np.sin(23.9 * t + 3 * seed) * 0.2)


def sigm(t, t0, t1):
    """smooth step 0 -> 1 between t0 and t1."""
    u = np.clip((t - t0) / (t1 - t0), 0, 1)
    return u * u * (3 - 2 * u)


def trace(ax, f, t0, t1, color, w=5, n=140):
    ts_ = np.linspace(t0, t1, n)
    return poly(ax, [(t, f(t)) for t in ts_], color, w)


def sketch_tag(pos=(5.6, -3.55)):
    return T("in this sketch", 22, GREY).move_to([pos[0], pos[1], 0])


# ---------------------------------------------------------------------------------------------
# the plot of the lesson's line (shared by s03 and s04)
# ---------------------------------------------------------------------------------------------
LAX = Ax(-5.0, 2.6, -2.55, 2.0, 276.0, 298.0, 0.0, 7.0)


def line_axes(ax=LAX):
    x_axis = Line(ax.P(276, 0), ax.P(298, 0), color=GREY, stroke_width=3)
    y_axis = Line(ax.P(276, 0), ax.P(276, 7), color=GREY, stroke_width=3)
    ticks = VGroup()
    for p in (276, 280, 284, 288, 292, 296):
        ticks.add(Line(ax.P(p, 0), ax.P(p, 0) + DOWN * 0.1, color=GREY, stroke_width=3))
        ticks.add(M(str(p), 22, GREY).next_to(ax.P(p, 0) + DOWN * 0.1, DOWN, buff=0.08))
    for v in (2, 4, 6):
        ticks.add(Line(ax.P(276, v), ax.P(276, v) + LEFT * 0.1, color=GREY, stroke_width=3))
        ticks.add(M(str(v), 22, GREY).next_to(ax.P(276, v) + LEFT * 0.1, LEFT, buff=0.08))
    xl = T("plasma osmolality (mOsm/kg)", 22, BLOOD).next_to(ax.P(287, 0), DOWN, buff=0.62)
    yl = T("AVP (pmol/L)", 22, AVP).next_to(ax.P(276, 7), UP, buff=0.12).align_to(ax.P(276, 7), LEFT).shift(LEFT * 0.4)
    return VGroup(x_axis, y_axis, ticks, xl, yl)


def the_line(ax=LAX, flat=True):
    rise = poly(ax, [(THR, 0), (298, avp(298))], AVP, 7)
    flat_ = poly(ax, [(276, 0), (THR, 0)], AVP, 7)
    return rise, flat_


def equation():
    return M("AVP = 0.43 × (Posm − 284)", 30, AVP), T("for Posm above 284 mOsm/kg", 22, GREY)


# =============================================================================================
class S00Title(TitleCard):
    LESSON = "Autonomic Control and the Hypothalamus"
    TITLE = "The Brain Acts Before the Blood Changes"


# =============================================================================================
class S01Puzzle(SpokenScene):
    def construct(self):
        ax1 = Ax(-3.4, 5.3, 0.55, 3.0, -1.0, 5.2, 0.0, 1.0)     # neurons
        ax2 = Ax(-3.4, 5.3, -3.0, -0.6, -1.0, 5.2, 0.0, 1.0)    # blood
        XT = lambda t: ax1.X(t)
        base1 = Line(ax1.P(-1, 0), ax1.P(5.2, 0), color=GREY, stroke_width=3)
        base2 = Line(ax2.P(-1, 0), ax2.P(5.2, 0), color=GREY, stroke_width=3)
        lab1 = T("Thirst neurons", 26, NEUR, weight=BOLD)
        lab1b = T("population activity", 22, TEXT)
        L1 = VGroup(lab1, lab1b).arrange(DOWN, buff=0.1).move_to([-5.45, 1.8, 0])
        lab2 = T("Blood", 26, BLOOD, weight=BOLD)
        lab2b = T("osmolality", 22, TEXT)
        L2 = VGroup(lab2, lab2b).arrange(DOWN, buff=0.1).move_to([-5.45, -1.8, 0])
        tag = sketch_tag((5.55, 3.55))
        ticks = VGroup()
        for t, s in ((0, "drinking starts"), (1, "1 min"), (5, "5 min")):
            ticks.add(Line([XT(t), -3.2, 0], [XT(t), -3.05, 0], color=GREY, stroke_width=3))
        tl0 = T("drinking starts", 22, TEXT).move_to([XT(0) - 0.15, -3.5, 0])
        tl1 = T("1 min", 22, TEXT).move_to([XT(1) + 0.85, -3.5, 0])
        tl5 = T("5 min after water access", 22, TEXT).move_to([XT(5) - 0.9, -3.5, 0])
        self.play(FadeIn(base1), FadeIn(base2), FadeIn(L1), FadeIn(L2), FadeIn(tag), run_time=0.4)
        hi = 0.82
        f_n = lambda t: hi * (1 - sigm(t, 0.0, 1.0)) + 0.14 * sigm(t, 0.0, 1.0) + noisy(t, 1.3, 0.025) * (1 - sigm(t, 0.0, 1.0)) + noisy(t, 0.4, 0.015)
        pre = trace(ax1, f_n, -1.0, 0.0, NEUR)
        self.play(Create(pre), run_time=0.5)
        self.at("starts to drink")
        dl0 = dashed(ax1.P(0, 1.05), ax2.P(0, -0.1), TEXT)
        self.play(Create(dl0), FadeIn(tl0), run_time=self.beat(0.06))
        self.at("within a minute")
        dl1 = dashed(ax1.P(1, 1.05), ax2.P(1, -0.1), GREY)
        fall = trace(ax1, f_n, 0.0, 1.0, NEUR)
        self.play(Create(dl1), FadeIn(tl1), run_time=self.beat(0.04))
        self.play(Create(fall), run_time=self.beat(0.08))
        low = trace(ax1, f_n, 1.0, 5.0, NEUR)
        self.play(Create(low), run_time=self.beat(0.07))
        self.at("salt in its blood")
        f_b = lambda t: 0.78 + noisy(t, 2.1, 0.02)
        blood = trace(ax2, f_b, -1.0, 5.0, BLOOD, w=6)
        dl5 = dashed(ax1.P(5, 1.05), ax2.P(5, -0.1), GREY)
        self.play(Create(blood), run_time=self.beat(0.16))
        self.play(Create(dl5), FadeIn(tl5), run_time=self.beat(0.05))
        still = backed("still raised", BLOOD, 26).move_to([XT(3.0), -1.8, 0])
        self.play(FadeIn(still), run_time=self.beat(0.05))
        self.at("could not happen")
        gap = Line(ax1.P(5, 0.1), ax2.P(5, 0.78), color=INH, stroke_width=0)
        ask = backed("What turned the neurons down?", NEUR, 28).move_to([XT(2.5), 0.0, 0])
        self.play(FadeIn(ask, shift=UP * 0.1), run_time=self.beat(0.08))
        self.finish()


# =============================================================================================
class S02Loop(SpokenScene):
    def construct(self):
        W, H = 5.6, 1.9
        xl, xr, yt, yb = -3.4, 3.4, 1.75, -1.6
        b_var = box("Regulated variable", "plasma osmolality", BLOOD, W, H).move_to([xl, yt, 0])
        b_sen = box("Sensor", "osmosensitive neurons\nin the lamina terminalis", NEUR, W, H).move_to([xr, yt, 0])
        b_cmp = box("Comparator", "how far it is from\nwhere it should be", GREY, W, H).move_to([xr, yb, 0])
        b_eff = box("Effector", "", FB, W, 2.5).move_to([xl, yb - 0.3, 0])
        e_t = b_eff[1][0]
        e_t.set_color(TEXT)
        e1 = chip("vasopressin (AVP)\nsaves water at the kidney", AVP, size=22, pad=0.15)
        e2 = chip("thirst: takes water in", NEUR, size=22, pad=0.15)
        e1.move_to(b_eff.get_center() + UP * 0.12)
        e2.move_to(b_eff.get_center() + DOWN * 0.85)
        b_eff[0].set_stroke(GREY)
        b_eff[0].set_fill(GREY, 0.14)
        e_t.move_to(b_eff.get_center() + UP * 1.0)
        head = T("A homeostatic loop", 30, TEXT, weight=BOLD).move_to([0, 3.5, 0])
        self.play(FadeIn(head), run_time=0.4)
        ghosts = VGroup(*[RoundedRectangle(corner_radius=0.16, width=W, height=hh, stroke_color=GREY, stroke_width=2, stroke_opacity=0.5).move_to(p)
                          for p, hh in (([xl, yt, 0], H), ([xr, yt, 0], H), ([xr, yb, 0], H), ([xl, yb - 0.3, 0], 2.5))])
        self.at("four parts")
        self.play(LaggedStart(*[FadeIn(g) for g in ghosts], lag_ratio=0.25), run_time=1.6)
        self.at("regulated variable")
        self.play(FadeIn(b_var, shift=UP * 0.15), FadeOut(ghosts[0]), run_time=self.beat(0.04))
        self.at("A sensor measures it")
        a1 = arr([xl + W / 2 + 0.05, yt, 0], [xr - W / 2 - 0.05, yt, 0])
        self.play(GrowArrow(a1), FadeIn(b_sen, shift=UP * 0.15), FadeOut(ghosts[1]), run_time=self.beat(0.05))
        self.at("A comparator")
        a2 = arr([xr, yt - H / 2 - 0.05, 0], [xr, yb + H / 2 + 0.05, 0])
        self.play(GrowArrow(a2), FadeIn(b_cmp, shift=UP * 0.15), FadeOut(ghosts[2]), run_time=self.beat(0.05))
        self.at("An effector pushes back")
        a3 = arr([xr - W / 2 - 0.05, yb, 0], [xl + W / 2 + 0.05, yb, 0])
        self.play(GrowArrow(a3), FadeIn(VGroup(b_eff[0], e_t)), FadeOut(ghosts[3]), run_time=self.beat(0.05))
        self.at("saves water")
        self.play(FadeIn(e1, shift=UP * 0.1), run_time=self.beat(0.05))
        self.at("Thirst takes water in")
        self.play(FadeIn(e2, shift=UP * 0.1), run_time=self.beat(0.05))
        self.at("opposes the error")
        a4 = inhib([xl, yb - 0.3 + 1.25 + 0.05, 0], [xl, yt - H / 2 - 0.08, 0])
        opp = T("opposes\nthe error", 24, INH, line_spacing=0.8).move_to([xl + 0.2 - 3.0 + 3.0, 0.0, 0])
        opp.next_to(a4, LEFT, buff=0.2)
        self.play(Create(a4), FadeIn(opp), run_time=self.beat(0.07))
        self.at("negative feedback")
        nf = T("negative feedback", 34, FB, weight=BOLD).move_to([0.0, 0.1, 0])
        self.play(Write(nf), run_time=self.beat(0.08))
        self.finish()


# =============================================================================================
class S03Line(SpokenScene):
    def construct(self):
        ax = LAX
        axes = line_axes()
        rise, flat = the_line()
        eq, eq2 = equation()
        eqg = VGroup(eq, eq2).arrange(DOWN, buff=0.1).move_to([0, 3.35, 0])
        self.play(FadeIn(axes), run_time=0.5)
        self.at("a threshold")
        thr = dashed(ax.P(THR, 0), ax.P(THR, 6.6), TEXT)
        thr_l = T("threshold: where the response starts", 22, TEXT).next_to(ax.P(THR, 6.6), RIGHT, buff=0.15)
        self.play(Create(thr), FadeIn(thr_l), run_time=self.beat(0.07))
        self.at("a gain")
        self.play(Create(rise), run_time=self.beat(0.10))
        gain_l = T("gain: growth per unit of error", 22, AVP)
        dv = ax.P(298, avp(298)) - ax.P(THR, 0)
        ang = np.arctan2(dv[1], dv[0])
        gain_l.rotate(ang).move_to(ax.P(291, avp(291)) + np.array([-np.sin(ang), np.cos(ang), 0]) * 0.32)
        self.play(FadeIn(gain_l), run_time=self.beat(0.05))
        self.at("one summary gives")
        self.play(FadeIn(eqg, shift=DOWN * 0.1), run_time=self.beat(0.06))
        # right panel: the two numbers
        n1 = VGroup(T("threshold", 24, TEXT, weight=BOLD), M("284 mOsm/kg", 26, BLOOD)).arrange(DOWN, buff=0.1, aligned_edge=LEFT)
        n2 = VGroup(T("gain", 24, AVP, weight=BOLD), M("0.43 pmol/L", 26, AVP), M("per mOsm/kg", 24, BLOOD)).arrange(DOWN, buff=0.08, aligned_edge=LEFT)
        panel = VGroup(n1, n2).arrange(DOWN, buff=0.45, aligned_edge=LEFT).move_to([4.7, 0.9, 0])
        self.at("The gain")
        self.play(FadeIn(n1), FadeIn(n2), FadeOut(gain_l), run_time=self.beat(0.08))
        self.at("illustrative averages")
        hedge = chip("illustrative\naverages", GOLD, size=26, pad=0.2)
        hedge.move_to([4.7, -1.6, 0])
        self.play(FadeIn(hedge, shift=UP * 0.1), run_time=self.beat(0.06))
        self.at("no release")
        self.play(Create(flat), run_time=self.beat(0.06))
        nr = T("no release", 24, AVP).move_to(ax.P(280, 0.8))
        self.play(FadeIn(nr), run_time=self.beat(0.04))
        self.finish()


# =============================================================================================
class S04Drink(SpokenScene):
    def construct(self):
        ax = LAX
        axes = line_axes()
        rise, flat = the_line()
        eq, eq2 = equation()
        eqg = VGroup(eq, eq2).arrange(DOWN, buff=0.1).move_to([0, 3.35, 0])
        thr = dashed(ax.P(THR, 0), ax.P(THR, 6.6), TEXT)
        thr_l = T("threshold", 22, TEXT).next_to(ax.P(THR, 6.6), RIGHT, buff=0.15)
        self.add(axes, rise, flat, eqg, thr, thr_l)
        who = chip("a hypothetical adult", GREY, size=22, pad=0.14).move_to([4.7, 2.3, 0])
        self.play(FadeIn(who), run_time=0.5)
        self.at("Osmolality is")
        p1 = ax.P(294, 0)
        d1 = Dot(ax.P(294, avp(294)), color=AVP, radius=0.11)
        dv1 = dashed(ax.P(294, 0), ax.P(294, avp(294)), BLOOD)
        dh1 = dashed(ax.P(276, avp(294)), ax.P(294, avp(294)), AVP)
        o1 = M("294", 26, BLOOD).next_to(ax.P(294, 1.0), RIGHT, buff=0.12)
        v1 = M("4.30", 28, AVP).next_to(ax.P(276, avp(294)), LEFT, buff=0.55).shift(UP * 0.0)
        brk = BraceBetweenPoints(ax.P(294, 0) + DOWN * 0.05, ax.P(THR, 0) + DOWN * 0.05, color=GREY)
        self.play(Create(dv1), FadeIn(o1), run_time=0.7)
        self.at("above threshold")
        thr_b = Line(ax.P(THR, 0.45), ax.P(294, 0.45), color=GREY, stroke_width=4)
        thr_t = T("10 mOsm/kg above\nthreshold", 24, GREY, line_spacing=0.8).move_to([4.7, 0.6, 0])
        self.play(Create(thr_b), FadeIn(thr_t), run_time=0.7)
        self.at("Vasopressin is")
        self.play(Create(dh1), FadeIn(d1), FadeIn(v1), run_time=0.7)
        self.at("After drinking")
        dv2 = dashed(ax.P(290, 0), ax.P(290, avp(290)), BLOOD)
        dh2 = dashed(ax.P(276, avp(290)), ax.P(290, avp(290)), AVP)
        d2 = Dot(ax.P(290, avp(290)), color=AVP, radius=0.11)
        o2 = M("290", 26, BLOOD).next_to(ax.P(290, 1.0), LEFT, buff=0.12)
        mv = Arrow(ax.P(294, 0) + UP * 0.35, ax.P(290, 0) + UP * 0.35, buff=0, color=BLOOD, stroke_width=6, tip_length=0.2)
        self.play(FadeOut(thr_b), FadeOut(thr_t), GrowArrow(mv), Create(dv2), FadeIn(d2), FadeIn(o2), run_time=0.9)
        self.play(Create(dh2), run_time=0.5)
        v2 = M("2.58", 28, AVP).next_to(ax.P(276, avp(290)), LEFT, buff=0.55)
        self.add(v2)
        self.at("It fell by")
        yb = Line(ax.P(276, avp(294)) + RIGHT * 0.5, ax.P(276, avp(290)) + RIGHT * 0.5, color=INH, stroke_width=0)
        fall = VGroup(
            Line(ax.P(294, avp(294)), ax.P(294, avp(290)), color=INH, stroke_width=6),
            Line(ax.P(290, avp(290)), ax.P(294, avp(290)), color=INH, stroke_width=0),
        )
        fl = M("−1.72", 30, INH).next_to(ax.P(294, (avp(294) + avp(290)) / 2), RIGHT, buff=0.15)
        self.play(Create(fall), FadeIn(fl), run_time=0.7)
        self.at("Less error")
        less = T("less error,\nless hormone", 30, TEXT, weight=BOLD, line_spacing=0.8).move_to([4.7, 0.6, 0])
        self.play(FadeIn(less, shift=UP * 0.1), run_time=0.7)
        self.at("A pure feedback loop")
        fb = chip("feedback reacts\nto an error it\nhas measured", FB, size=24, pad=0.2).move_to([4.7, -1.5, 0])
        self.play(FadeIn(fb, shift=UP * 0.1), run_time=0.8)
        self.finish()


# =============================================================================================
class S05Ahead(SpokenScene):
    def construct(self):
        rows_y = [2.55, 0.55, -1.45]
        names = ["drinks", "sees water,\ncannot drink", "licks an empty bottle\n(salt-challenged mice)"]
        axs, labs, bases = [], [], []
        for y, nm in zip(rows_y, names):
            a = Ax(-1.7, 6.0, y - 0.7, y + 0.7, -0.5, 5.0, 0.0, 1.0)
            axs.append(a)
            labs.append(chip(nm, GREY, size=22, pad=0.16).move_to([-4.6, y, 0]))
            bases.append(Line(a.P(-0.5, 0), a.P(5.0, 0), color=GREY, stroke_width=3))
        head = T("thirst neurons, population activity", 24, NEUR, weight=BOLD).move_to([2.1, 3.62, 0])
        tag = sketch_tag((5.5, -3.55))
        tl = VGroup(T("0 = water available", 22, GREY), T("1 min", 22, GREY))
        hi = 0.78
        f_hi = lambda t: hi + noisy(t, 1.7, 0.03)
        f_dr = lambda t: hi * (1 - sigm(t, 0.0, 1.0)) + 0.14 * sigm(t, 0.0, 1.0) + noisy(t, 1.7, 0.03) * (1 - 0.8 * sigm(t, 0.0, 1.0))
        a0 = axs[0]
        zero = dashed(a0.P(0, -0.1), a0.P(0, 1.1), TEXT)
        one = dashed(a0.P(1, -0.1), a0.P(1, 1.1), GREY)
        z_l = T("water available", 22, TEXT).next_to(a0.P(0, -0.1), DOWN, buff=0.08).shift(RIGHT * 0.1)
        o_l = T("1 min", 22, GREY).next_to(a0.P(1, -0.1), DOWN, buff=0.08).shift(RIGHT * 0.45)
        self.play(FadeIn(head), FadeIn(tag), *[FadeIn(b) for b in bases], run_time=0.3)
        self.at("In water restricted mice")
        self.play(FadeIn(labs[0]), Create(trace(a0, f_hi, -0.5, 0.0, NEUR)), Create(zero), FadeIn(z_l), run_time=self.beat(0.07))
        self.at("within a minute")
        self.play(Create(one), FadeIn(o_l), run_time=self.beat(0.03))
        self.play(Create(trace(a0, f_dr, 0.0, 5.0, NEUR)), run_time=1.6)
        self.at("Seeing water")
        self.play(FadeIn(labs[1]), run_time=self.beat(0.04))
        a1 = axs[1]
        self.at("does not lower")
        self.play(Create(trace(a1, f_hi, -0.5, 5.0, NEUR)), run_time=self.beat(0.08))
        xm = Line(a1.P(4.3, 0.1), a1.P(4.7, 0.5), color=GREY, stroke_width=0)
        self.at("licking an empty bottle")
        self.play(FadeIn(labs[2]), run_time=self.beat(0.04))
        a2 = axs[2]
        self.at("does not either")
        self.play(Create(trace(a2, f_hi, -0.5, 5.0, NEUR)), run_time=self.beat(0.08))
        self.at("ahead of any change")
        bl = chip("blood: still raised at 5 min", BLOOD, size=24, pad=0.14).move_to([-2.4, -3.0, 0])
        self.play(FadeIn(bl, shift=UP * 0.1), run_time=self.beat(0.05))
        self.at("a response to a disturbance")
        ff = chip("feedforward: a response to an expected disturbance", FF, size=26, pad=0.16)
        self.play(FadeOut(bl), run_time=self.beat(0.03))
        ff.move_to([-0.6, -3.0, 0])
        self.play(FadeIn(ff, shift=UP * 0.1), run_time=self.beat(0.08))
        self.finish()


# =============================================================================================
class S06Rule(SpokenScene):
    def construct(self):
        # stage A: the gut route
        neur = chip("thirst neurons", NEUR, size=34, pad=0.26).move_to([3.9, 1.4, 0])
        nsub = T("SFO Nos1 population", 24, TEXT).next_to(neur, DOWN, buff=0.14)
        water = chip("water in the stomach", INH, size=32, pad=0.24).move_to([-4.0, 1.4, 0])
        blood = chip("blood osmolality", BLOOD, size=32, pad=0.24).move_to([-3.0, -2.0, 0])
        self.play(FadeIn(neur), FadeIn(nsub), run_time=self.beat(0.05))
        self.at("straight into the stomach")
        self.play(FadeIn(water, shift=RIGHT * 0.2), run_time=self.beat(0.05))
        self.at("inhibited the neurons")
        ai = inhib([-1.7, 1.4, 0], [2.0, 1.4, 0])
        li = T("inhibits, after about\n105 s in hydrated mice", 24, INH, line_spacing=0.8).move_to([0.15, 2.4, 0])
        self.play(Create(ai), FadeIn(li), run_time=self.beat(0.08))
        self.at("before any detectable change")
        self.play(FadeIn(blood, shift=UP * 0.2), run_time=self.beat(0.05))
        nb = T("no detectable change yet", 26, BLOOD).next_to(blood, RIGHT, buff=0.35)
        self.play(FadeIn(nb), run_time=self.beat(0.05))
        # stage B: limits
        self.at("Keep the limits")
        stage_a = VGroup(neur, nsub, water, blood, ai, li, nb)
        self.play(FadeOut(stage_a), run_time=self.beat(0.04))
        l1 = chip("in mice", GOLD, size=40, pad=0.3)
        l2 = chip("a population calcium signal", GOLD, size=40, pad=0.3)
        l3 = chip("not the feeling of thirst", GOLD, size=40, pad=0.3)
        lim = VGroup(l1, l2, l3).arrange(DOWN, buff=0.55).move_to([0, 0.2, 0])
        self.play(FadeIn(l1, shift=UP * 0.1), run_time=self.beat(0.03))
        self.at("population calcium signal")
        self.play(FadeIn(l2, shift=UP * 0.1), run_time=self.beat(0.03))
        self.at("not the feeling")
        self.play(FadeIn(l3, shift=UP * 0.1), run_time=self.beat(0.03))
        # stage C: the rule
        self.at("Feedback reacts")
        self.play(lim.animate.set_opacity(0.0), run_time=self.beat(0.03))
        fb = box("Feedback", "reacts to a measured error", FB, 6.0, 2.6, tsize=42, bsize=30).move_to([-3.3, -0.3, 0])
        ff = box("Feedforward", "acts on an expected one", FF, 6.0, 2.6, tsize=42, bsize=30).move_to([3.3, -0.3, 0])
        self.remove(*lim)
        self.play(FadeIn(fb, shift=UP * 0.15), run_time=self.beat(0.04))
        self.at("forward acts on")
        self.play(FadeIn(ff, shift=UP * 0.15), run_time=self.beat(0.04))
        self.at("Thirst uses both")
        both = T("thirst uses both", 40, TEXT, weight=BOLD).move_to([0, 2.5, 0])
        self.play(FadeIn(both, shift=UP * 0.1), run_time=self.beat(0.05))
        self.finish()


# =============================================================================================
class S07End(EndCard):
    LINE = "Feedback reacts to a measured error. Feedforward acts on an expected one."
