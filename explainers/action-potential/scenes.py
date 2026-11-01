"""What lets the charge in: the action potential and conduction (Biochemistrypedia explainer)

Timed to the SPOKEN words: every self.at("...") cue waits for that phrase in audio/words.json.
All traces are computed from the Hodgkin-Huxley equations with the lesson's constants and are labelled
"in this sketch"; the numbers on screen are the lesson's own.

COLOR MAP (one color per concept, whole video)
  YELLOW = sodium: sodium current, sodium conductance, sodium's equilibrium line, the active stretch
  BLUE   = potassium: potassium current, potassium conductance, potassium's equilibrium line
  GREEN  = the membrane voltage trace
  RED    = inactivation / refractory / "cannot be excited" / the old theory's stop
  TEAL   = conductance g in the rule (I = g x driving force)
  ORANGE = driving force in the rule
  GREY   = membrane, axes, rest and zero lines, de-emphasized
"""
import numpy as np
from bp_style import *  # noqa: F401,F403

ORANGE = "#F29E4C"
NA, K, VOLT, INACT = YELLOW, BLUE, GREEN, RED


# ---------------------------------------------------------------------------------------------
# Hodgkin-Huxley model (the lesson's constants: gNa 120, gK 36, leak 0.3 mS/cm2, Cm 1 uF/cm2, rest -65 mV,
# ENa +50, EK -77; leak reversal -54.4 is the standard value, used only inside the computed trace)
# ---------------------------------------------------------------------------------------------
def _rates(V):
    am = 1.0 if abs(V + 40) < 1e-6 else 0.1 * (V + 40) / (1 - np.exp(-(V + 40) / 10))
    bm = 4 * np.exp(-(V + 65) / 18)
    ah = 0.07 * np.exp(-(V + 65) / 20)
    bh = 1 / (1 + np.exp(-(V + 35) / 10))
    an = 0.1 if abs(V + 55) < 1e-6 else 0.01 * (V + 55) / (1 - np.exp(-(V + 55) / 10))
    bn = 0.125 * np.exp(-(V + 65) / 80)
    return am, bm, ah, bh, an, bn


def hh_free(T=10.0, dt=0.005, stim=(0.5, 0.5, 15.0)):
    gNa, gK, gL, ENa, EK, EL = 120., 36., 0.3, 50., -77., -54.4
    V = -65.
    am, bm, ah, bh, an, bn = _rates(V)
    m, h, n = am / (am + bm), ah / (ah + bh), an / (an + bn)
    out = []
    for i in range(int(T / dt)):
        t = i * dt
        I = stim[2] if stim[0] <= t < stim[0] + stim[1] else 0.0
        gna, gk = gNa * m ** 3 * h, gK * n ** 4
        out.append((t, V, gna, gk))
        V += dt * (I - gna * (V - ENa) - gk * (V - EK) - gL * (V - EL))
        am, bm, ah, bh, an, bn = _rates(V)
        m += dt * (am * (1 - m) - bm * m); h += dt * (ah * (1 - h) - bh * h); n += dt * (an * (1 - n) - bn * n)
    return np.array(out)


def hh_clamp(Vc=0.0, T=7.5, dt=0.005):
    """gates relax at a held voltage, starting from rest: returns t, gNa(t), gK(t)."""
    V0 = -65.
    am, bm, ah, bh, an, bn = _rates(V0)
    m, h, n = am / (am + bm), ah / (ah + bh), an / (an + bn)
    out = []
    for i in range(int(T / dt)):
        am, bm, ah, bh, an, bn = _rates(Vc)
        out.append((i * dt, 120. * m ** 3 * h, 36. * n ** 4))
        m += dt * (am * (1 - m) - bm * m); h += dt * (ah * (1 - h) - bh * h); n += dt * (an * (1 - n) - bn * n)
    return np.array(out)


FREE = hh_free()
CLAMP = hh_clamp()
GN_MAX = FREE[:, 2].max()
T_PEAK = FREE[FREE[:, 1].argmax(), 0]
T_MIN = FREE[FREE[:, 1].argmin(), 0]


# ---------------------------------------------------------------------------------------------
# helpers
# ---------------------------------------------------------------------------------------------
class Ax:
    """maps (t, y-value) to scene coordinates."""
    def __init__(self, x0, x1, y0, y1, t0, t1, v0, v1):
        self.x0, self.x1, self.y0, self.y1, self.t0, self.t1, self.v0, self.v1 = x0, x1, y0, y1, t0, t1, v0, v1

    def X(self, t):
        return self.x0 + (t - self.t0) / (self.t1 - self.t0) * (self.x1 - self.x0)

    def Y(self, v):
        return self.y0 + (v - self.v0) / (self.v1 - self.v0) * (self.y1 - self.y0)

    def P(self, t, v):
        return np.array([self.X(t), self.Y(v), 0.0])


def curve(ax, t, v, upto=None, color=VOLT, w=5, stride=8):
    if upto is not None:
        k = int(np.searchsorted(t, upto))
        t, v = t[:k], v[:k]
    t, v = t[::stride], v[::stride]
    m = VMobject(stroke_color=color, stroke_width=w)
    if len(t) >= 2:
        m.set_points_as_corners([ax.P(a, b) for a, b in zip(t, v)])
    return m


def live_curve(ax, t, v, tracker, color=VOLT, w=5, start=0.0):
    return always_redraw(lambda: curve(ax, t[t >= start], v[t >= start], upto=tracker.get_value(), color=color, w=w))


def label_left(text, pos, color=GREY, size=22):
    return M(text, size, color).next_to(np.array(pos), LEFT, buff=0.12)


def dashed(p, q, color=GREY, w=2.5, op=0.9):
    return DashedLine(p, q, color=color, stroke_width=w, dash_length=0.12, stroke_opacity=op)


def bchip(text, color=BLUE, size=24, **kw):
    c = chip(text, color, size=size, **kw)
    back = RoundedRectangle(corner_radius=0.14, width=c[0].width, height=c[0].height, stroke_width=0,
                            fill_color=BG, fill_opacity=1).move_to(c[0])
    return VGroup(back, *c)


def arr(a, b, color=GREY, w=6, tip=0.25):
    return Arrow(np.array(a, float), np.array(b, float), buff=0, color=color, stroke_width=w, tip_length=tip,
                 max_tip_length_to_length_ratio=0.5, max_stroke_width_to_length_ratio=14)


def cross(center, s=0.28, color=INACT, w=7):
    c = np.array(list(center)[:2] + [0.0], float)
    return VGroup(Line(c + [-s, -s, 0], c + [s, s, 0], color=color, stroke_width=w),
                  Line(c + [-s, s, 0], c + [s, -s, 0], color=color, stroke_width=w))


def ts(text, size=26, color=TEXT, **kw):
    return T(text, size, color, **kw)


def membrane_bar(x0, x1, y, h=0.32):
    return RoundedRectangle(corner_radius=0.1, width=x1 - x0, height=h, stroke_color=GREY, stroke_width=3,
                            fill_color=GREY, fill_opacity=0.35).move_to([(x0 + x1) / 2, y, 0])


# ---------------------------------------------------------------------------------------------
# two-plot stage for scenes 4 and 5 (voltage on top, conductances below, one time axis)
# ---------------------------------------------------------------------------------------------
TW = 10.0
VAX = Ax(-3.7, 4.5, 0.15, 3.35, 0.0, TW, -100.0, 60.0)
GAX = Ax(-3.7, 4.5, -3.30, -0.60, 0.0, TW, 0.0, 1.05)   # conductances in units of the sodium peak
MX, MY = 5.45, -1.95   # centre of the little membrane at the lower right


def build_stage(scene, animate=True):
    """returns dict of static mobjects; adds them (animated or not)."""
    S = {}
    S["vaxis"] = Line(VAX.P(0, -100), VAX.P(0, 60), color=GREY, stroke_width=3)
    S["gaxis"] = VGroup(Line(GAX.P(0, 0), GAX.P(0, 1.05), color=GREY, stroke_width=3),
                        Line(GAX.P(0, 0), GAX.P(TW, 0), color=GREY, stroke_width=3))
    xe = VAX.X(TW)
    S["lines"] = VGroup(
        dashed(VAX.P(0, 50), [xe, VAX.Y(50), 0], NA),
        dashed(VAX.P(0, 0), [xe, VAX.Y(0), 0], GREY),
        dashed(VAX.P(0, -65), [xe, VAX.Y(-65), 0], GREY),
        dashed(VAX.P(0, -77), [xe, VAX.Y(-77), 0], K))
    S["ylab"] = VGroup(label_left("+50 mV", VAX.P(0, 50) - [0.05, 0, 0], NA),
                       label_left("0 mV", VAX.P(0, 0) - [0.05, 0, 0], GREY),
                       label_left("rest −65 mV", VAX.P(0, -65) - [0.05, 0, 0], GREY))
    S["klab"] = M("−77 mV", 22, K).next_to(np.array([xe + 0.08, VAX.Y(-77), 0]), RIGHT, buff=0.05)
    S["desc"] = VGroup(T("sodium equilibrium", 22, NA).move_to([VAX.X(8.5), VAX.Y(50) - 0.25, 0]),
                       T("potassium equilibrium", 22, K).move_to([VAX.X(8.1), VAX.Y(-77) - 0.27, 0]))
    S["tlab"] = T("time, in this sketch", 22, GREY).move_to([VAX.X(8.0), GAX.Y(0) - 0.27, 0])
    S["glab"] = VGroup(T("conductance", 22, GREY).move_to([-5.15, -1.2, 0]),
                       T("sodium", 22, NA).move_to([-5.15, -1.75, 0]),
                       T("potassium", 22, K).move_to([-5.15, -2.3, 0]))
    S["vlab"] = VGroup()
    S["mem"] = VGroup(membrane_bar(MX - 0.85, MX + 0.85, MY, h=0.42),
                      T("outside", 22, GREY).move_to([MX, MY + 1.5, 0]),
                      T("inside", 22, GREY).move_to([MX, MY - 1.45, 0]))
    S["chNa"] = bchip("Na", NA, 24, pad=0.1).move_to([MX - 0.42, MY, 0])
    S["chK"] = bchip("K", K, 24, pad=0.1).move_to([MX + 0.46, MY, 0])
    S["chNa"].set_z_index(5); S["chK"].set_z_index(5)
    S["nain"] = VGroup(arr([MX - 0.42, MY + 1.15, 0], [MX - 0.42, MY + 0.32, 0], NA, w=8),
                       arr([MX - 0.42, MY - 0.32, 0], [MX - 0.42, MY - 1.1, 0], NA, w=8))
    S["kout"] = VGroup(arr([MX + 0.46, MY - 1.1, 0], [MX + 0.46, MY - 0.32, 0], K, w=8),
                       arr([MX + 0.46, MY + 0.32, 0], [MX + 0.46, MY + 1.15, 0], K, w=8))
    static = [S["vaxis"], S["gaxis"], S["lines"], S["ylab"], S["klab"], S["desc"], S["tlab"], S["glab"], S["vlab"],
              S["mem"], S["chNa"], S["chK"]]
    if animate:
        scene.play(*[FadeIn(m) for m in static], run_time=1.0)
    else:
        scene.add(*static)
    return S


def stage_curves(scene, tr, with_g=True):
    cv = live_curve(VAX, FREE[:, 0], FREE[:, 1], tr, VOLT, 6)
    cg = live_curve(GAX, FREE[:, 0], FREE[:, 2] / GN_MAX, tr, NA, 5)
    ck = live_curve(GAX, FREE[:, 0], FREE[:, 3] / GN_MAX, tr, K, 5)
    dot = always_redraw(lambda: Dot(curve(VAX, FREE[:, 0], FREE[:, 1], upto=max(tr.get_value(), 0.02)).get_end()
                                    if tr.get_value() > 0.05 else VAX.P(0, -65), radius=0.11, color=VOLT))
    scene.add(cv, cg, ck, dot)
    return cv, cg, ck, dot


def chip_in(scene, c):
    """add a bchip's opaque backing at once; return the fade for the visible parts."""
    scene.add(c[0])
    return FadeIn(VGroup(c[1], c[2]))


def run_to(scene, phrase, lead=0.2, nth=0, lo=0.3, hi=6.0):
    """seconds from now until just before the narrator says `phrase` (clamped), to spread a slow move over a gap."""
    return max(lo, min(hi, scene.t_of(phrase, nth) - lead - scene.elapsed()))


class S00Title(TitleCard):
    LESSON = "The Action Potential and Conduction"
    TITLE = "What Lets the Charge In"


# ---------------------------------------------------------------------------------------------
class S01Overshoot(SpokenScene):
    """axon + electrode; the voltage sketch passes zero; the old theory's stop; the overshoot; the question."""

    def construct(self):
        ax = Ax(-3.6, 5.6, -3.4, 1.5, 1.8, 4.8, -90.0, 55.0)
        tube = RoundedRectangle(corner_radius=0.5, width=6.6, height=1.1, stroke_color=GREY, stroke_width=4,
                                fill_color=GREY, fill_opacity=0.18).move_to([-2.7, 2.75, 0])
        elec = Line([-4.3, 3.5, 0], [-3.3, 2.75, 0], color=TEXT, stroke_width=4)
        tip = Dot([-3.3, 2.75, 0], radius=0.08, color=TEXT)
        tube_lbl = T("squid giant axon", 30, TEXT).move_to([2.6, 2.75, 0])
        self.at("Hodgkin and Huxley")
        self.play(FadeIn(tube), run_time=0.6)
        self.at("fine electrode")
        self.play(Create(elec), run_time=run_to(self, "inside", lo=0.5))
        self.play(FadeIn(tip), run_time=0.3)
        self.at("squid giant axon")
        self.play(FadeIn(tube_lbl), run_time=0.6)

        zero = dashed(ax.P(1.8, 0), ax.P(4.8, 0), GREY)
        rest = dashed(ax.P(1.8, -65), ax.P(4.8, -65), GREY)
        axes = Line(ax.P(1.8, -90), ax.P(1.8, 55), color=GREY, stroke_width=3)
        labs = VGroup(label_left("0 mV", ax.P(1.8, 0) - [0.05, 0, 0]), label_left("rest −65 mV", ax.P(1.8, -65) - [0.05, 0, 0]))
        sk = T("in this sketch", 22, GREY).move_to([4.6, ax.Y(-65) + 0.3, 0])
        self.at("At the peak")
        self.play(FadeIn(axes), FadeIn(zero), FadeIn(rest), FadeIn(labs), FadeIn(sk), run_time=0.5)
        tr = ValueTracker(1.8)
        cv = live_curve(ax, FREE[:, 0], FREE[:, 1], tr, VOLT, 6, start=1.8)
        dot = always_redraw(lambda: Dot(ax.P(tr.get_value(), float(np.interp(tr.get_value(), FREE[:, 0], FREE[:, 1]))),
                                        radius=0.11, color=VOLT))
        self.add(cv, dot)
        self.play(tr.animate.set_value(T_PEAK), run_time=run_to(self, "turned positive", lo=1.0), rate_func=smooth)
        k0 = int(np.argmax(FREE[:, 1] > 0))
        kk = int(np.searchsorted(FREE[:, 0], T_PEAK))
        pts = [ax.P(FREE[i, 0], FREE[i, 1]) for i in range(k0, kk, 4)] + [ax.P(T_PEAK, FREE[kk, 1])]
        poly = Polygon(*([ax.P(FREE[k0, 0], 0)] + pts + [ax.P(T_PEAK, 0)]), stroke_width=0, fill_color=VOLT, fill_opacity=0.3)
        pos_lbl = T("inside is positive", 28, VOLT).move_to([ax.X(T_PEAK) - 2.5, ax.Y(44), 0])
        self.at("turned positive")
        self.play(FadeIn(poly), FadeIn(pos_lbl), run_time=0.6)

        xs_ = ax.X(FREE[k0, 0]); xe_ = ax.X(T_PEAK + 0.55)
        old = dashed([xs_, ax.Y(0), 0], [xe_, ax.Y(0), 0], INACT, w=5, op=1)
        old.set_z_index(3)
        stop = Line([xe_, ax.Y(0) - 0.28, 0], [xe_, ax.Y(0) + 0.28, 0], color=INACT, stroke_width=8)
        old_lbl = T("old theory: stops near zero", 26, INACT).move_to([4.05, ax.Y(0) - 0.55, 0])
        self.at("The old theory")
        self.play(Create(old), FadeIn(old_lbl), run_time=run_to(self, "near zero", lo=0.8))
        self.play(FadeIn(stop), run_time=0.4)
        over = T("it overshot", 30, VOLT, weight=BOLD).move_to([ax.X(T_PEAK) + 1.6, ax.Y(30), 0])
        self.at("It overshot")
        self.play(Indicate(poly, color=VOLT, scale_factor=1.08), FadeIn(over), run_time=0.8)

        q = ts("What let charge in faster than it leaks out?", 30, TEXT).move_to([0.9, -3.15, 0])
        self.at("faster than")
        self.play(FadeOut(old_lbl), FadeOut(pos_lbl), FadeOut(over), FadeIn(q, shift=UP * 0.1), run_time=0.7)
        qm = T("?", 120, YELLOW, weight=BOLD).move_to([-0.9, ax.Y(30), 0])
        self.at("What was it")
        self.play(FadeIn(qm, scale=0.6), run_time=0.6)
        self.finish()


# ---------------------------------------------------------------------------------------------
class S02Clamp(SpokenScene):
    """voltage held fixed; early inward and delayed outward currents; choline reverses the early one."""

    def construct(self):
        ax_v = Ax(-3.6, 5.6, 1.45, 3.0, 0.0, 8.0, -80.0, 10.0)
        Y0, SC = -1.35, 0.0011
        Y_I = lambda i: Y0 + SC * i
        T0 = 0.5
        tt = CLAMP[:, 0] + T0
        i_na = CLAMP[:, 1] * (0 - 50.0)          # microA/cm2, outward positive, at 0 mV
        i_k = CLAMP[:, 2] * (0 + 77.0)
        i_na_chol = CLAMP[:, 1] * (0 + 5.4)      # E_Na moved to -5.4 mV, g_Na assumed unchanged
        mx = lambda t, i: np.array([ax_v.X(t), Y_I(i), 0.0])

        v_axis = Line(ax_v.P(0, -80), ax_v.P(0, 10), color=GREY, stroke_width=3)
        v_lab = VGroup(label_left("0 mV", ax_v.P(0, 0) - [0.05, 0, 0]), label_left("−65 mV", ax_v.P(0, -65) - [0.05, 0, 0]))
        i_axis = Line(mx(0, -1650), mx(0, 2050), color=GREY, stroke_width=3)
        i_zero = Line(mx(0, 0), mx(8, 0), color=GREY, stroke_width=3)
        i_lab = VGroup(T("outward ↑", 24, GREY).move_to([-5.15, Y_I(1300), 0]),
                       T("current", 24, GREY).move_to([-5.15, Y_I(0), 0]),
                       T("inward ↓", 24, GREY).move_to([-5.15, Y_I(-1300), 0]))
        sk = T("in this sketch", 22, GREY).move_to([4.7, -3.3, 0])
        step = VMobject(stroke_color=VOLT, stroke_width=6)
        step.set_points_as_corners([ax_v.P(0, -65), ax_v.P(T0, -65), ax_v.P(T0, 0), ax_v.P(8, 0)])
        hdr = T("voltage clamp: the membrane voltage is held fixed", 28, TEXT).move_to([-1.0, 3.5, 0])
        held = T("held fixed", 26, VOLT).move_to([ax_v.X(5.6), ax_v.Y(0) - 0.5, 0])
        sq = T("squid axon", 22, GREY).move_to([5.45, 3.5, 0])

        self.at("held the membrane voltage")
        self.play(FadeIn(v_axis), FadeIn(v_lab), FadeIn(i_axis), FadeIn(i_zero), FadeIn(i_lab), FadeIn(sk), run_time=0.6)
        self.play(Create(step), run_time=run_to(self, "voltage clamp", lo=1.0))
        self.at("voltage clamp")
        self.play(FadeIn(hdr, shift=DOWN * 0.1), FadeIn(held), run_time=0.6)
        self.at("In the squid axon")
        self.play(FadeIn(sq), run_time=0.5)
        self.at("a step gave")
        self.play(Indicate(step, color=VOLT, scale_factor=1.02), run_time=0.8)

        def mk(i, color, tr):
            def f():
                v = tr.get_value()
                k = int(np.searchsorted(CLAMP[:, 0], v))
                m = VMobject(stroke_color=color, stroke_width=7)
                if k >= 3:
                    m.set_points_as_corners([mx(tt[j], i[j]) for j in range(0, k, 6)])
                return m
            return always_redraw(f)

        tr_na, tr_k = ValueTracker(0.0), ValueTracker(0.0)
        na_c, k_c = mk(i_na, NA, tr_na), mk(i_k, K, tr_k)
        self.add(na_c, k_c)
        na_lbl = T("early, inward", 28, NA).move_to([mx(T0 + 3.2, 0)[0], Y_I(-1000), 0])
        self.at("early inward current")
        self.play(tr_na.animate.set_value(7.4), run_time=run_to(self, "delayed outward current", lo=1.2, hi=3.2), rate_func=linear)
        self.play(FadeIn(na_lbl), run_time=0.3)
        k_lbl = T("delayed, outward", 28, K).move_to([mx(T0 + 1.5, 0)[0], Y_I(1650), 0])
        self.at("delayed outward current")
        self.play(tr_k.animate.set_value(7.4), run_time=run_to(self, "replaced most", lo=1.2, hi=3.0) - 0.3, rate_func=linear)
        self.play(FadeIn(k_lbl), run_time=0.3)

        # --- second case: choline. Reset every result in the same beat the new case label comes in. ---
        chol = T("most outside sodium replaced by choline", 28, TEXT).move_to([-1.0, 3.5, 0])
        self.at("replaced most")
        na_c.clear_updaters(); k_c.clear_updaters()
        self.play(FadeOut(na_c), FadeOut(k_c), FadeOut(na_lbl), FadeOut(k_lbl), FadeOut(held), FadeOut(step),
                  ReplacementTransform(hdr, chol), run_time=0.8)
        step2 = step.copy()
        held2 = held.copy()
        self.play(FadeIn(step2), FadeIn(held2), run_time=0.5)
        tr_na2, tr_k2 = ValueTracker(0.0), ValueTracker(0.0)
        na_c2, k_c2 = mk(i_na_chol, NA, tr_na2), mk(i_k, K, tr_k2)
        self.add(na_c2, k_c2)
        ghost = DashedVMobject(VMobject(stroke_color=NA).set_points_as_corners([mx(tt[j], i_na[j]) for j in range(0, len(tt), 6)]),
                               num_dashes=70).set_stroke(NA, width=4, opacity=0.45)
        rev_lbl = T("reversed: now outward", 28, NA).move_to([mx(T0 + 4.2, 0)[0], Y_I(380), 0])
        self.at("The early current reversed")
        self.play(tr_na2.animate.set_value(7.4), run_time=run_to(self, "The delayed current", lo=1.0, hi=2.4) - 0.5, rate_func=linear)
        ghost_lbl = T("normal sea water", 26, NA).set_opacity(0.7).move_to([mx(T0 + 3.0, 0)[0], Y_I(-1150), 0])
        self.play(FadeIn(ghost), FadeIn(ghost_lbl), FadeIn(rev_lbl), run_time=0.5)
        lit = T("little affected", 28, K).move_to([mx(T0 + 1.5, 0)[0], Y_I(1650), 0])
        self.at("The delayed current")
        self.play(tr_k2.animate.set_value(7.4), run_time=run_to(self, "early current is sodium", lo=1.0, hi=3.0) - 0.4, rate_func=linear)
        self.play(FadeIn(lit), run_time=0.4)

        na_chip = bchip("sodium", NA, 28).move_to([mx(T0 + 4.6, 0)[0], Y_I(-700), 0])
        k_chip = bchip("potassium", K, 28).move_to([mx(T0 + 5.5, 0)[0], Y_I(1150), 0])
        self.at("early current is sodium")
        self.play(chip_in(self, na_chip), FadeOut(rev_lbl), run_time=0.6)
        self.at("Potassium")
        self.play(chip_in(self, k_chip), FadeOut(lit), run_time=0.6)
        self.finish()


# ---------------------------------------------------------------------------------------------
class S03Rule(SpokenScene):
    """I = g x (Vm - E), worked for sodium and potassium on a short membrane each."""

    def construct(self):
        eq = VGroup(M("I", 50, TEXT), M("=", 50, TEXT), M("g", 50, TEAL, weight=BOLD), M("×", 50, TEXT),
                    M("(Vm − E)", 50, ORANGE)).arrange(RIGHT, buff=0.3).move_to([0, 3.1, 0])
        g_lbl = T("conductance: how open", 26, TEAL).move_to([-3.1, 2.4, 0])
        d_lbl = T("driving force: which way, how hard", 26, ORANGE).move_to([3.0, 2.4, 0])
        self.at("rule—current")
        self.play(FadeIn(eq[0]), run_time=0.4)
        self.at("equals")
        self.play(*[FadeIn(m) for m in eq[1:]], run_time=0.8)
        self.at("conductance")
        self.play(Indicate(eq[2], color=TEAL, scale_factor=1.3), FadeIn(g_lbl), run_time=0.8)
        self.at("driving force")
        self.play(Indicate(eq[4], color=ORANGE, scale_factor=1.15), FadeIn(d_lbl), run_time=0.8)
        vm_lbl = T("Vm: the membrane voltage", 26, TEXT).move_to([3.1, 1.6, 0])
        e_lbl = T("E: the ion's equilibrium voltage", 26, TEXT).move_to([3.0, 1.05, 0])
        self.at("membrane voltage")
        self.play(FadeIn(vm_lbl), run_time=0.5)
        self.at("equilibrium voltage")
        self.play(FadeIn(e_lbl), run_time=0.5)

        YM = -0.15
        def column(xm, ion_color, ch_name):
            bar = membrane_bar(xm - 0.95, xm + 0.95, YM, h=0.5)
            ch = bchip(ch_name, ion_color, 32, pad=0.14).move_to([xm, YM, 0]); ch.set_z_index(5)
            out_l = T("outside", 24, GREY).move_to([xm, 1.95, 0])
            in_l = T("inside", 24, GREY).move_to([xm, -2.6, 0])
            return VGroup(bar, ch, out_l, in_l)

        xn, xk = -1.7, 5.4
        mem_n, mem_k = column(xn, NA, "Na"), column(xk, K, "K")
        rows_n = VGroup(M("E = +50 mV", 26, NA), M("Vm = 0 mV", 26, TEXT), M("g = 20 mS/cm²", 26, TEAL),
                        M("0 − 50 = −50 mV", 26, ORANGE), M("I = 20 × (−50)", 26, TEXT), M("= −1000 µA/cm²", 30, NA, weight=BOLD))
        rows_k = VGroup(M("E = −77 mV", 24, K), M("Vm = 0 mV", 24, TEXT), M("g = 15 mS/cm²", 24, TEAL),
                        M("0 − (−77) = +77 mV", 24, ORANGE), M("I = 15 × 77", 24, TEXT), M("= +1155 µA/cm²", 28, K, weight=BOLD))
        ys = [1.45, 0.85, 0.25, -0.35, -0.95, -1.65]
        for r, x0 in ((rows_n, -6.4), (rows_k, 0.3)):
            for r_, y in zip(r, ys):
                r_.move_to([0, y, 0]).align_to([x0, 0, 0], LEFT)
        note = T("illustrative round numbers, model squid axon", 24, GREY).move_to([0, -3.2, 0])
        self.at("model squid axon")
        self.play(FadeIn(mem_n), FadeOut(vm_lbl), FadeOut(e_lbl), run_time=0.7)
        self.at("illustrative round numbers")
        self.play(FadeIn(note), run_time=0.5)
        self.at("Sodium's equilibrium voltage")
        self.play(FadeIn(rows_n[0]), run_time=0.5)
        self.at("Step the membrane")
        self.play(FadeIn(rows_n[1]), run_time=0.5)
        self.at("with sodium conductance")
        self.play(FadeIn(rows_n[2]), run_time=0.5)
        self.at("force is minus")
        self.play(FadeIn(rows_n[3]), run_time=0.6)
        na_arr = arr([xn, 1.6, 0], [xn, -2.25, 0], NA, w=16, tip=0.45)
        self.at("so the current is")
        self.play(FadeIn(rows_n[4]), run_time=0.5)
        self.at("microamperes")
        self.play(FadeIn(rows_n[5]), GrowArrow(na_arr), run_time=1.0)
        self.at("centimeter—inward")
        self.play(Indicate(na_arr, color=NA, scale_factor=1.04), run_time=0.7)

        self.at("For potassium")
        self.play(FadeIn(mem_k), run_time=0.6)
        self.at("minus 77")
        self.play(FadeIn(rows_k[0]), FadeIn(rows_k[1]), run_time=0.6)
        self.at("With conductance")
        self.play(FadeIn(rows_k[2]), FadeIn(rows_k[3]), run_time=0.7)
        k_arr = arr([xk, -2.25, 0], [xk, 1.6, 0], K, w=18, tip=0.45)
        self.at("plus 1155—outward")
        self.play(FadeIn(rows_k[4]), run_time=0.5)
        self.at("1155—outward")
        self.play(FadeIn(rows_k[5]), GrowArrow(k_arr), run_time=1.0)
        self.at("outward")
        self.play(Indicate(k_arr, color=K, scale_factor=1.04), run_time=0.7)
        self.finish()


# ---------------------------------------------------------------------------------------------
class S04Rise(SpokenScene):
    """voltage and conductances: the rising phase to the peak."""

    def construct(self):
        self.at("run free")
        S = build_stage(self)
        tr = ValueTracker(0.0)
        cv, cg, ck, dot = stage_curves(self, tr)
        stim = arr([VAX.X(0.5), VAX.Y(-65) - 0.95, 0], [VAX.X(0.5), VAX.Y(-65) - 0.2, 0], TEXT, w=5, tip=0.2)
        stim_l = T("stimulus", 22, TEXT).next_to(stim, RIGHT, buff=0.1).shift(DOWN * 0.15)
        self.at("past threshold")
        self.play(FadeIn(stim), FadeIn(stim_l), tr.animate.set_value(1.4), run_time=run_to(self, "sodium conductance climbs", lo=1.0), rate_func=linear)
        self.play(FadeOut(stim), FadeOut(stim_l), run_time=0.3)
        self.at("sodium conductance climbs")
        self.play(tr.animate.set_value(2.8), run_time=run_to(self, "sodium flows in", lo=1.0), rate_func=linear)
        self.at("sodium flows in")
        self.play(FadeIn(S["nain"]), tr.animate.set_value(3.05), run_time=run_to(self, "voltage rises", lo=0.6), rate_func=linear)
        self.at("voltage rises")
        self.play(Indicate(S["lines"][0], color=NA), tr.animate.set_value(3.4), run_time=run_to(self, "raises sodium conductance", lo=1.0), rate_func=linear)
        rp = T("rising phase", 28, VOLT, weight=BOLD).move_to([VAX.X(T_PEAK) + 1.5, VAX.Y(-30), 0])
        self.at("raises sodium conductance further")
        self.play(Indicate(cg, color=NA, scale_factor=1.0), run_time=0.8)
        self.play(tr.animate.set_value(3.6), run_time=run_to(self, "rising phase", lo=0.5), rate_func=linear)
        self.at("rising phase")
        self.play(FadeIn(rp), run_time=0.5)
        self.at("stays short of")
        self.play(tr.animate.set_value(T_PEAK), run_time=0.7, rate_func=smooth)
        pk = FREE[int(np.searchsorted(FREE[:, 0], T_PEAK)), 1]
        gap = VGroup(Line([VAX.X(T_PEAK), VAX.Y(pk), 0], [VAX.X(T_PEAK), VAX.Y(50), 0], color=NA, stroke_width=5),
                     Line([VAX.X(T_PEAK) - 0.15, VAX.Y(50), 0], [VAX.X(T_PEAK) + 0.15, VAX.Y(50), 0], color=NA, stroke_width=5))
        short = T("short of +50 mV", 22, NA).move_to([VAX.X(T_PEAK) + 1.5, VAX.Y(50) + 0.2, 0])
        self.play(Create(gap), FadeIn(short), run_time=0.7)
        inact = bchip("inactivation", INACT, 26).move_to([GAX.X(T_PEAK) + 2.1, GAX.Y(0.85), 0])
        inact_a = arr([GAX.X(T_PEAK) + 1.0, GAX.Y(0.78), 0], [GAX.X(T_PEAK) + 0.2, GAX.Y(0.6), 0], INACT, w=4, tip=0.2)
        self.at("Inactivation")
        self.play(chip_in(self, inact), GrowArrow(inact_a), run_time=0.7)
        self.at("just starting")
        self.play(FadeIn(S["kout"]), Indicate(ck, color=K, scale_factor=1.0), run_time=0.8)
        self.finish()


class S05Fall(SpokenScene):
    """the falling phase and the undershoot."""

    def construct(self):
        S = build_stage(self, animate=False)
        tr = ValueTracker(T_PEAK)
        cv, cg, ck, dot = stage_curves(self, tr)
        pk = FREE[int(np.searchsorted(FREE[:, 0], T_PEAK)), 1]
        gap = VGroup(Line([VAX.X(T_PEAK), VAX.Y(pk), 0], [VAX.X(T_PEAK), VAX.Y(50), 0], color=NA, stroke_width=5),
                     Line([VAX.X(T_PEAK) - 0.15, VAX.Y(50), 0], [VAX.X(T_PEAK) + 0.15, VAX.Y(50), 0], color=NA, stroke_width=5))
        short = T("short of +50 mV", 22, NA).move_to([VAX.X(T_PEAK) + 1.5, VAX.Y(50) + 0.2, 0])
        rp = T("rising phase", 28, VOLT, weight=BOLD).move_to([VAX.X(T_PEAK) + 1.5, VAX.Y(-30), 0])
        inact = bchip("inactivation", INACT, 26).move_to([GAX.X(T_PEAK) + 2.1, GAX.Y(0.85), 0])
        inact_a = arr([GAX.X(T_PEAK) + 1.0, GAX.Y(0.78), 0], [GAX.X(T_PEAK) + 0.2, GAX.Y(0.6), 0], INACT, w=4, tip=0.2)
        self.add(S["nain"], S["kout"], gap, short, rp, inact, inact_a)
        for m in S["kout"]:
            m.set_opacity(0.6)
        self.at("Inactivation then")
        self.play(FadeOut(S["nain"]), FadeOut(gap), FadeOut(short), FadeOut(rp), Indicate(inact[2], color=INACT), run_time=0.7)
        self.at("shuts off")
        self.play(tr.animate.set_value(4.1), run_time=run_to(self, "Potassium current", lo=1.0), rate_func=linear)
        self.at("Potassium current")
        self.play(FadeOut(inact), FadeOut(inact_a), S["kout"].animate.set_opacity(1.0), tr.animate.set_value(5.3),
                  run_time=run_to(self, "falling phase", lo=1.0), rate_func=linear)
        fp = T("falling phase", 28, VOLT, weight=BOLD).move_to([VAX.X(6.9), VAX.Y(-18), 0])
        self.at("falling phase")
        self.play(FadeIn(fp), tr.animate.set_value(6.7), run_time=run_to(self, "falls slowly", lo=1.0), rate_func=linear)
        hi = T("stays raised", 26, K).move_to([GAX.X(7.6), GAX.Y(0.62), 0])
        self.at("falls slowly")
        self.play(tr.animate.set_value(7.5), run_time=run_to(self, "stays raised", lo=1.0), rate_func=linear)
        self.at("stays raised")
        self.play(FadeIn(hi), Indicate(ck, color=K, scale_factor=1.0), run_time=0.8)
        self.play(tr.animate.set_value(8.2), run_time=run_to(self, "pulls the voltage", lo=0.4), rate_func=linear)
        self.at("pulls the voltage")
        self.play(Indicate(S["lines"][3], color=K), Indicate(S["klab"], color=K), run_time=1.0)
        self.play(tr.animate.set_value(9.3), run_time=run_to(self, "below rest", lo=0.6), rate_func=linear)
        k0 = int(np.searchsorted(FREE[:, 0], 5.3))
        k1 = int(np.searchsorted(FREE[:, 0], 9.6))
        seg = FREE[k0:k1]
        below = seg[seg[:, 1] < -65.0]
        j0 = int(np.argmax(FREE[:, 0] >= below[0, 0]))
        j1 = int(np.argmax(FREE[:, 0] >= below[-1, 0]))
        pts = [VAX.P(FREE[j, 0], FREE[j, 1]) for j in range(j0, j1, 6)]
        poly = Polygon(*([VAX.P(FREE[j0, 0], -65)] + pts + [VAX.P(FREE[j1, 0], -65)]), stroke_width=0,
                       fill_color=VOLT, fill_opacity=0.5)
        us = T("undershoot", 28, VOLT, weight=BOLD).move_to([VAX.X(8.5), VAX.Y(-50), 0])
        self.at("below rest")
        self.play(FadeIn(poly), run_time=0.7)
        self.at("undershoot")
        self.play(FadeIn(us), tr.animate.set_value(TW), run_time=1.2)
        self.finish()


# ---------------------------------------------------------------------------------------------
class S06Travel(SpokenScene):
    """an axon in four stretches: the stretch behind is inactivated, the next one fires; then the rule."""

    def construct(self):
        yc, hw = 0.9, 1.2           # axon centre line, half-gap between the two membrane walls
        xs = [-4.65, -1.55, 1.55, 4.65]
        wall_w, wall_h = 2.9, 0.6

        def wall(x, up):
            return RoundedRectangle(corner_radius=0.1, width=wall_w, height=wall_h, stroke_color=GREY, stroke_width=3,
                                    fill_color=GREY, fill_opacity=0.4).move_to([x, yc + (hw if up else -hw), 0])
        top = [wall(x, True) for x in xs]
        bot = [wall(x, False) for x in xs]
        core = Rectangle(width=12.4, height=2 * hw - wall_h + 0.04, stroke_width=0, fill_color=GREY, fill_opacity=0.08).move_to([0, yc, 0])
        out_l = T("outside", 24, GREY).move_to([-5.7, yc + hw + 0.85, 0])
        in_l = T("inside the axon", 24, GREY).move_to([-4.85, yc, 0])
        self.add(core, *top, *bot, out_l, in_l)
        for m in (top[0], bot[0]):
            m.set_stroke(INACT).set_fill(INACT, 0.65)   # the spike has already passed this stretch

        def color_stretch(i, color, op=0.65):
            return [top[i].animate.set_stroke(color).set_fill(color, op), bot[i].animate.set_stroke(color).set_fill(color, op)]

        def into(i):   # sodium entering a stretch
            return VGroup(arr([xs[i] - 0.6, yc + hw + 1.1, 0], [xs[i] - 0.6, yc + hw + 0.35, 0], NA, w=8, tip=0.24),
                          arr([xs[i] + 0.6, yc + hw + 1.1, 0], [xs[i] + 0.6, yc + hw + 0.35, 0], NA, w=8, tip=0.24))

        self.at("Right after a spike")
        self.play(*color_stretch(1, NA), run_time=0.5)
        self.at("most sodium channels")
        self.play(*color_stretch(1, INACT), run_time=0.8)
        lab2 = T("inactivated", 26, INACT).move_to([xs[1], yc - hw - 0.7, 0])
        self.at("inactivated")
        self.play(FadeIn(lab2), run_time=0.5)
        stim = arr([xs[1], yc + hw + 1.45, 0], [xs[1], yc + hw + 0.4, 0], TEXT, w=12, tip=0.34)
        stim_l = T("strong stimulus", 26, TEXT).move_to([xs[1] + 2.2, yc + hw + 1.1, 0])
        x2 = cross([xs[1], yc], 0.4)
        no2 = T("no second spike", 28, INACT).move_to([xs[1], yc - hw - 1.3, 0])
        self.at("No stimulus")
        self.play(GrowArrow(stim), FadeIn(stim_l), run_time=0.7)
        self.at("triggers a second spike")
        self.play(Create(x2), FadeIn(no2), run_time=0.7)

        self.at("An impulse travels")
        self.play(FadeOut(stim), FadeOut(stim_l), FadeOut(x2), FadeOut(no2), FadeOut(lab2), run_time=0.5)
        self.play(*color_stretch(2, NA), run_time=0.5)
        nin = into(2)
        self.play(FadeIn(nin), run_time=0.4)
        cur = arr([xs[2] + 0.3, yc, 0], [xs[3] - 0.4, yc, 0], NA, w=9, tip=0.3)
        self.at("inward current spreads along the core")
        self.play(GrowArrow(cur), run_time=run_to(self, "It brings", lo=1.0, hi=2.6))
        core_l = T("current spreads along the core", 26, NA).move_to([xs[3] - 1.4, yc - hw - 0.7, 0])
        self.play(FadeIn(core_l), run_time=0.4)
        self.at("next stretch")
        self.play(*color_stretch(3, NA), FadeOut(core_l), run_time=0.7)
        nin2 = into(3)
        self.play(FadeIn(nin2), run_time=0.3)
        thr = T("brought to threshold", 26, NA).move_to([xs[3] - 0.9, yc - hw - 0.7, 0])
        self.at("to threshold")
        self.play(FadeIn(thr), run_time=0.4)
        self.at("just behind")
        self.play(*color_stretch(2, INACT), FadeOut(nin), FadeOut(cur), FadeOut(thr), run_time=0.7)
        x3 = cross([xs[2], yc], 0.4)
        beh = T("cannot be excited again", 26, INACT).move_to([xs[2], yc - hw - 0.7, 0])
        self.at("cannot be excited again")
        self.play(Create(x3), FadeIn(beh), run_time=0.7)
        way = arr([-1.6, yc - hw - 1.75, 0], [2.4, yc - hw - 1.75, 0], TEXT, w=10, tip=0.36)
        way_l = T("one way", 28, TEXT).next_to(way, UP, buff=0.12)
        self.at("travels one way")
        self.play(GrowArrow(way), FadeIn(way_l), run_time=0.8)
        rule1 = Text("In the squid axon, sodium entering makes the spike.", font=FONT, font_size=34, t2c={"sodium entering": NA})
        rule2 = Text("Inactivation and potassium end it.", font=FONT, font_size=34, t2c={"Inactivation": INACT, "potassium": K})
        rules = VGroup(rule1, rule2).arrange(DOWN, buff=0.2).move_to([0, -3.0, 0])
        self.at("Keep this rule")
        self.play(FadeOut(nin2), FadeOut(beh), FadeOut(x3), FadeOut(way), FadeOut(way_l), run_time=0.5)
        self.at("Sodium entering makes")
        self.play(FadeIn(rule1, shift=UP * 0.1), run_time=0.7)
        self.at("Inactivation and potassium")
        self.play(FadeIn(rule2, shift=UP * 0.1), run_time=0.7)
        self.finish()


class S07End(EndCard):
    LINE = "Squid axon: sodium makes the spike; inactivation and potassium end it."
