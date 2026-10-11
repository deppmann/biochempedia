"""Explainer film: a full response before every receptor is occupied (binding-and-dose-response).

COLOR MAP (one colour per concept, whole film)
  BLUE   receptors
  YELLOW ligand, occupancy (dots, curve, Kd marks)
  GREEN  response (curves, gauge, EC50)
  GREY   empty / spare receptors, ghosts, axes
  RED    receptors removed by the irreversible blocker
  TEXT   neutral labels

Every curve is computed from the lesson's equations:
  occupancy = L / (Kd + L)   (x axis is log10 of L / Kd)
  response  = occupancy / 0.05, capped at 1  (the lesson's example: ceiling at 5% occupancy)
  with a fraction f of the receptors left: response = f * occupancy / 0.05, capped at 1
"""
import numpy as np
from bp_style import *

REC, LIG, RESP, SPARE, GONE = BLUE, YELLOW, GREEN, GREY, RED
CEIL = 0.05

# ---- plot geometry (log10 L/Kd from -3 to 3) -------------------------------------------------
XL, XR, YB, YT = -5.0, 5.0, -1.9, 2.5


def px(x):
    return XL + (x + 3) / 6 * (XR - XL)


def py(y):
    return YB + y * (YT - YB)


def occ(x):
    return 1 / (1 + 10 ** (-x))


def resp(x, f=1.0):
    return min(f * occ(x) / CEIL, 1.0)


def curve(fn, color, width=6, n=241):
    xs = np.linspace(-3, 3, n)
    m = VMobject()
    m.set_points_as_corners([[px(x), py(fn(x)), 0] for x in xs])
    return m.set_stroke(color, width).set_fill(opacity=0)


def base(kd=True, xtitle=True):
    """axes, y labels, faint guides, Kd tick label and x title. Returns a VGroup."""
    g = VGroup()
    g.add(Line([XL, YB, 0], [XR, YB, 0], color=GREY, stroke_width=3))
    g.add(Line([XL, YB, 0], [XL, YT + 0.1, 0], color=GREY, stroke_width=3))
    for v, s in ((0.5, "50%"), (1.0, "100%")):
        g.add(DashedLine([XL, py(v), 0], [XR, py(v), 0], color="#2c3340", stroke_width=2, dash_length=0.15))
        g.add(T(s, 22, GREY).next_to([XL, py(v), 0], LEFT, buff=0.15))
    g.add(T("0", 22, GREY).next_to([XL, YB, 0], LEFT, buff=0.15))
    if kd:
        g.add(Line([px(0), YB, 0], [px(0), YB - 0.12, 0], color=GREY, stroke_width=3))
    if xtitle:
        g.add(T("ligand concentration (log scale)", 22, GREY).move_to([XR - 1.95, YB - 0.42, 0]))
    return g


def kd_label():
    return T("Kd", 26, LIG, weight=BOLD).move_to([px(0), YB - 0.42, 0])


# ---- receptor row -----------------------------------------------------------------------------
RX = [-5.7 + 0.6 * i for i in range(20)]
R_BOT, R_TOP, MEM_Y = 0.45, 2.55, 0.3
GAUGE_Y, GAUGE_W = -1.35, 8.0


def receptor(x):
    return RoundedRectangle(corner_radius=0.12, width=0.42, height=R_TOP - R_BOT, stroke_color=REC, stroke_width=3,
                            fill_color=REC, fill_opacity=0.25).move_to([x, (R_BOT + R_TOP) / 2, 0])


def ligand(x, y=R_TOP - 0.38):
    return Circle(radius=0.18, stroke_width=0, fill_color=LIG, fill_opacity=1).move_to([x, y, 0])


def membrane():
    return RoundedRectangle(corner_radius=0.1, width=12.6, height=0.3, stroke_color=GREY, stroke_width=3,
                            fill_color=GREY, fill_opacity=0.35).move_to([0, MEM_Y, 0])


def gauge_outline():
    return Rectangle(width=GAUGE_W, height=0.55, stroke_color=GREY, stroke_width=3).move_to([0, GAUGE_Y, 0])


def gauge_fill(frac):
    r = Rectangle(width=max(GAUGE_W * frac, 0.02), height=0.55, stroke_width=0, fill_color=RESP, fill_opacity=0.9)
    return r.move_to([-GAUGE_W / 2, GAUGE_Y, 0], aligned_edge=LEFT)


def down_arrow():
    return Arrow([0, 0.1, 0], [0, GAUGE_Y + 0.4, 0], buff=0.05, color=GREY, stroke_width=5, tip_length=0.2)


def bracket(i0, i1, y=2.85):
    a, b = RX[i0] - 0.21, RX[i1] + 0.21
    return VGroup(Line([a, y - 0.15, 0], [a, y, 0], color=SPARE, stroke_width=3),
                  Line([a, y, 0], [b, y, 0], color=SPARE, stroke_width=3),
                  Line([b, y, 0], [b, y - 0.15, 0], color=SPARE, stroke_width=3))


def land(x, run=0.5):
    d = ligand(x)
    return d, AnimationGroup(FadeIn(d, shift=DOWN * 0.8), run_time=run)


# =================================================================================================
class S00Title(TitleCard):
    LESSON = "Binding: Affinity, Occupancy and Dose–Response"
    TITLE = "A Full Response, Mostly Empty Receptors"


# =================================================================================================
class S01Puzzle(SpokenScene):
    def construct(self):
        recs = VGroup(*[receptor(x) for x in RX])
        mem, ga, arrow = membrane(), gauge_outline(), down_arrow()
        glab = T("response", 24, RESP).move_to([0, GAUGE_Y - 0.75, 0])
        self.play(FadeIn(mem), LaggedStart(*[FadeIn(r, shift=UP * 0.15) for r in recs], lag_ratio=0.04),
                  Create(ga), FadeIn(arrow), FadeIn(glab), run_time=1.2)
        self.at("responding at its maximum")
        fill = gauge_fill(1.0)
        self.play(GrowFromEdge(fill, LEFT), run_time=1.0)
        self.at("only about")
        d, a = land(RX[0])
        lab5 = T("5%", 30, LIG, weight=BOLD).move_to([RX[0], 3.3, 0])
        self.play(a, FadeIn(lab5, shift=DOWN * 0.1))
        self.at("other")
        br = bracket(1, 19)
        lab95 = T("95% empty", 28, SPARE).move_to([(RX[1] + RX[19]) / 2, 3.3, 0])
        self.play(Create(br), FadeIn(lab95, shift=DOWN * 0.1), run_time=0.8)
        self.at("How can a tissue")
        q = T("?", 96, TEXT, weight=BOLD).move_to([5.5, GAUGE_Y, 0])
        self.play(FadeIn(q, scale=0.6), run_time=0.5)
        self.play(Indicate(fill, color=TEXT, scale_factor=1.04), run_time=0.8)
        self.finish()


# =================================================================================================
class S02Occupancy(SpokenScene):
    def construct(self):
        b = base(kd=True, xtitle=False)
        xt = T("ligand concentration (log scale)", 22, LIG).move_to([XR - 1.95, YB - 0.42, 0])
        self.play(Create(b), run_time=0.9)
        self.at("start with binding")
        occ_c = curve(occ, LIG, 7)
        occ_lab = T("occupancy", 26, LIG).move_to([px(2.1), py(0.58), 0])
        self.play(Create(occ_c), FadeIn(occ_lab), run_time=1.8)
        self.at("any molecule that binds")
        self.play(FadeIn(xt, shift=UP * 0.1), run_time=0.6)
        self.at("fraction of receptors occupied")
        eq = M("occupancy = [L] / (Kd + [L])", 32, TEXT).move_to([0, 3.3, 0])
        self.play(Write(eq), run_time=1.8)
        self.at("dissociation constant")
        kd = kd_label()
        vl = DashedLine([px(0), YB, 0], [px(0), py(0.5), 0], color=LIG, stroke_width=3)
        hl = DashedLine([XL, py(0.5), 0], [px(0), py(0.5), 0], color=LIG, stroke_width=3)
        dot = Dot([px(0), py(0.5), 0], radius=0.13, color=LIG)
        self.play(FadeIn(kd, shift=UP * 0.1), Create(vl), Create(hl), FadeIn(dot, scale=0.5), run_time=0.9)
        self.at("half of the receptors")
        self.play(Indicate(dot, color=TEXT, scale_factor=1.8), run_time=0.7)
        self.at("occupancy comes at")
        x5 = float(np.log10(0.05 / 0.95))
        dot5 = Dot([px(x5), py(0.05), 0], radius=0.13, color=TEXT)
        lab5 = T("5%", 28, TEXT, weight=BOLD).move_to([px(x5) - 0.55, py(0.05) + 0.55, 0])
        v5 = DashedLine([px(x5), YB, 0], [px(x5), py(0.05), 0], color=TEXT, stroke_width=3)
        self.play(FadeOut(vl), FadeOut(hl), ReplacementTransform(dot, dot5), FadeIn(v5), FadeIn(lab5), run_time=1.1)
        self.at("far below")
        gap = DoubleArrow([px(x5) + 0.08, YB - 0.95, 0], [px(0) - 0.08, YB - 0.95, 0], buff=0, color=TEXT,
                          stroke_width=4, tip_length=0.18)
        self.play(Create(gap), run_time=0.8)
        self.finish()


# =================================================================================================
class S03Assumption(SpokenScene):
    def construct(self):
        b = base(kd=True, xtitle=False)
        xt = T("ligand concentration (log scale)", 22, LIG).move_to([XR - 1.95, YB - 0.42, 0])
        occ_c = curve(occ, LIG, 11)
        occ_lab = T("occupancy", 26, LIG).move_to([px(2.1), py(0.58), 0])
        self.add(b, xt, kd_label(), occ_c, occ_lab)
        self.wait(0.3)
        self.at("proportional to occupancy")
        rc = curve(occ, RESP, 4)
        lab = T("response, if proportional to occupancy", 26, RESP).move_to([-3.0, 3.25, 0])
        self.play(Create(rc), FadeIn(lab, shift=DOWN * 0.1), run_time=1.6)
        self.at("gives half of the maximum")
        hl = DashedLine([XL, py(0.5), 0], [px(0), py(0.5), 0], color=RESP, stroke_width=3)
        vl = DashedLine([px(0), py(0.5), 0], [px(0), YB, 0], color=RESP, stroke_width=3)
        dot = Dot([px(0), py(0.5), 0], radius=0.13, color=RESP)
        self.play(Create(hl), run_time=0.7)
        self.play(Create(vl), FadeIn(dot, scale=0.5), run_time=0.5)
        self.at("would equal")
        ec = T("EC50", 26, RESP, weight=BOLD).move_to([px(0) - 1.05, YB - 0.42, 0])
        eqs = T("=", 26, TEXT).move_to([px(0) - 0.5, YB - 0.42, 0])
        self.play(FadeIn(ec, shift=UP * 0.1), FadeIn(eqs), run_time=0.6)
        self.at("But in")
        # clear the assumption's marks, then the tissue's own response curve replaces the proportional one
        self.play(FadeOut(hl), FadeOut(vl), FadeOut(dot), FadeOut(ec), FadeOut(eqs), run_time=0.5)
        self.at("reach its full response")
        rc2 = curve(resp, RESP, 4)
        lab2 = T("response of the tissue", 26, RESP).move_to([-3.0, 3.25, 0])
        self.play(Transform(rc, rc2), Transform(lab, lab2), run_time=1.8)
        xc = float(np.log10(CEIL / (1 - CEIL)))
        vc = DashedLine([px(xc), YB, 0], [px(xc), py(1.0), 0], color=GREY, stroke_width=3)
        self.at("before all of its receptors")
        yd = Dot([px(xc), py(CEIL), 0], radius=0.13, color=LIG)
        self.play(Create(vc), FadeIn(yd, scale=0.5), run_time=0.7)
        self.finish()


# =================================================================================================
class S04Bottleneck(SpokenScene):
    def construct(self):
        recs = VGroup(*[receptor(x) for x in RX])
        mem, ga, arrow = membrane(), gauge_outline(), down_arrow()
        glab = T("pathway after the receptor", 24, GREY).move_to([0, GAUGE_Y - 0.75, 0])
        self.at("amplification in the pathway")
        self.play(FadeIn(mem), LaggedStart(*[FadeIn(r, shift=UP * 0.15) for r in recs], lag_ratio=0.04),
                  Create(ga), FadeIn(arrow), FadeIn(glab), run_time=1.3)
        self.at("bottleneck")
        glab2 = T("slowest step downstream", 24, TEXT).move_to(glab)
        self.play(Transform(glab, glab2), Indicate(ga, color=TEXT, scale_factor=1.05), run_time=0.9)
        self.at("full speed")
        d1, a1 = land(RX[0])
        fill = gauge_fill(1.0)
        full = T("full speed", 24, RESP).move_to([5.25, GAUGE_Y, 0])
        self.play(a1, run_time=0.5)
        self.play(GrowFromEdge(fill, LEFT), FadeIn(full), run_time=0.8)
        self.at("add nothing")
        ds, anims = [], []
        for i in (1, 2):
            d, a = land(RX[i], 0.5)
            ds.append(d)
            anims.append(a)
        self.play(AnimationGroup(*anims, lag_ratio=0.4))
        self.at("enough receptors")
        self.play(Indicate(fill, color=TEXT, scale_factor=1.03), run_time=0.8)
        self.at("more occupied receptors")
        anims = []
        for i in (3, 4):
            d, a = land(RX[i], 0.5)
            ds.append(d)
            anims.append(a)
        self.play(AnimationGroup(*anims, lag_ratio=0.4))
        nc = T("no change", 24, TEXT).move_to([5.25, GAUGE_Y - 0.55, 0])
        self.play(FadeIn(nc, shift=UP * 0.1), run_time=0.5)
        self.at("not needed")
        br = bracket(1, 19)
        sp = T("not needed for a full response", 30, SPARE).move_to([(RX[1] + RX[19]) / 2, 3.3, 0])
        self.play(Create(br), FadeIn(sp, shift=DOWN * 0.1), run_time=0.9)
        self.at("spare receptors")
        sp1 = T("spare receptors", 30, SPARE).move_to(sp)
        self.play(Transform(sp, sp1), run_time=0.6)
        self.at("Together")
        sp2 = T("the receptor reserve", 30, SPARE).move_to(sp)
        self.play(Transform(sp, sp2), run_time=0.8)
        self.finish()


# =================================================================================================
class S05Gap(SpokenScene):
    def construct(self):
        b = base(kd=True, xtitle=False)
        xt = T("ligand concentration (log scale)", 22, LIG).move_to([XR - 1.95, YB - 0.42, 0])
        occ_c = curve(occ, LIG, 7)
        occ_lab = T("occupancy", 26, LIG).move_to([px(2.1), py(0.58), 0])
        self.add(b, xt, occ_c, occ_lab)
        self.wait(0.2)
        self.at("property of the receptor")
        kd = kd_label()
        vl = DashedLine([px(0), YB, 0], [px(0), py(0.5), 0], color=LIG, stroke_width=3)
        dot = Dot([px(0), py(0.5), 0], radius=0.13, color=LIG)
        self.play(FadeIn(kd, shift=UP * 0.1), Create(vl), FadeIn(dot, scale=0.5), run_time=0.8)
        self.at("whole pathway")
        rc = curve(resp, RESP, 6)
        lab = T("response", 26, RESP).move_to([px(-2.2), py(0.9), 0])
        self.play(Create(rc), FadeIn(lab, shift=DOWN * 0.1), run_time=1.8)
        self.at("ceiling at")
        xc = float(np.log10(CEIL / (1 - CEIL)))
        d5 = Dot([px(xc), py(CEIL), 0], radius=0.13, color=TEXT)
        v5 = DashedLine([px(xc), py(CEIL), 0], [px(xc), py(1.0), 0], color=TEXT, stroke_width=3)
        l5 = T("5% occupied", 24, TEXT).move_to([px(xc) + 1.15, py(0.62), 0])
        self.play(FadeIn(d5, scale=0.5), Create(v5), FadeIn(l5), run_time=1.0)
        self.at("Half of the maximum")
        xh = float(np.log10(0.025 / 0.975))
        h50 = DashedLine([XL, py(0.5), 0], [px(xh), py(0.5), 0], color=RESP, stroke_width=3)
        vh = DashedLine([px(xh), py(0.5), 0], [px(xh), YB, 0], color=RESP, stroke_width=3)
        dh = Dot([px(xh), py(0.5), 0], radius=0.13, color=RESP)
        self.play(Create(h50), run_time=0.6)
        self.play(Create(vh), FadeIn(dh, scale=0.5), run_time=0.5)
        ec = T("EC50", 26, RESP, weight=BOLD).move_to([px(xh), YB - 0.42, 0])
        self.play(FadeIn(ec, shift=UP * 0.1), run_time=0.4)
        self.at("times below")
        gap = DoubleArrow([px(xh) + 0.1, YB - 0.95, 0], [px(0) - 0.1, YB - 0.95, 0], buff=0, color=TEXT,
                          stroke_width=4, tip_length=0.18)
        gl = T("39-fold", 26, TEXT).move_to([(px(xh) + px(0)) / 2, YB - 1.4, 0])
        self.play(Create(gap), FadeIn(gl, shift=UP * 0.1), run_time=0.9)
        self.at("no change in binding")
        self.play(Indicate(occ_c, color=TEXT, scale_factor=1.0), run_time=1.0)
        self.finish()


# =================================================================================================
class S06Proof(SpokenScene):
    CASES = [("all receptors", 1.0, TEXT), ("half removed", 0.5, GONE), ("90% removed", 0.1, GONE),
             ("more than 95% removed", 0.04, GONE)]

    def case_label(self, i):
        t, f, c = self.CASES[i]
        return T(t, 28, c, weight=BOLD).move_to([XL - 0.9, 3.3, 0], aligned_edge=LEFT)

    def construct(self):
        b = base(kd=False, xtitle=False)
        xt = T("ligand concentration (log scale)", 22, GREY).move_to([XR - 1.95, YB - 0.42, 0])
        self.add(b, xt)
        self.wait(0.3)
        self.at("taking receptors away")
        c0 = curve(lambda x: resp(x, 1.0), RESP, 6)
        lab = self.case_label(0)
        self.play(Create(c0), FadeIn(lab, shift=DOWN * 0.1), run_time=1.5)
        ideal = T("idealised", 24, GREY).move_to([px(1.6), py(0.9), 0])
        self.play(FadeIn(ideal), run_time=0.4)
        self.at("irreversible blocker")
        blocker = chip("irreversible blocker", GONE, size=24).move_to([4.3, 3.3, 0])
        self.play(FadeIn(blocker, shift=DOWN * 0.1), run_time=0.6)
        ghost = DashedVMobject(curve(lambda x: resp(x, 1.0), GREY, 4), num_dashes=70).set_color(GREY)
        # case: half removed. The label changes and the old curve clears together.
        self.at("Remove half")
        lab1 = self.case_label(1)
        self.add(ghost)
        self.play(FadeOut(c0, run_time=0.25), Transform(lab, lab1), run_time=0.3)
        self.at("curve moves right")
        c1 = curve(lambda x: resp(x, 0.5), RESP, 6)
        self.play(Create(c1), run_time=1.3)
        # case: 90% removed
        self.at("remove 90")
        lab2 = self.case_label(2)
        self.play(FadeOut(c1, run_time=0.25), Transform(lab, lab2), run_time=0.3)
        self.at("further right")
        c2 = curve(lambda x: resp(x, 0.1), RESP, 6)
        self.play(Create(c2), run_time=1.3)
        # case: more than 95% removed
        self.at("only when more")
        lab3 = self.case_label(3)
        self.play(FadeOut(c2, run_time=0.25), Transform(lab, lab3), run_time=0.3)
        self.at("does the maximum")
        c3 = curve(lambda x: resp(x, 0.04), RESP, 6)
        self.play(Create(c3), run_time=1.3)
        self.at("no sharp threshold")
        self.play(Indicate(ideal, color=TEXT, scale_factor=1.2), run_time=0.9)
        self.at("shift first")
        self.play(Indicate(ghost, color=TEXT, scale_factor=1.0), run_time=0.9)
        self.at("fall later")
        self.play(Indicate(c3, color=TEXT, scale_factor=1.0), run_time=0.9)
        self.at("Keep the rule")
        self.play(Indicate(c3, color=TEXT, scale_factor=1.0), run_time=0.9)
        self.finish()


# =================================================================================================
class S07End(EndCard):
    LINE = "A full response does not mean every receptor is occupied."
