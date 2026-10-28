"""Birth order and layers: the day a neuron is born sets the layer it settles in.

COLOR MAP (one color per concept, whole video)
  ORANGE = earliest-born cohort / deep-layer fate (layer 6)
  YELLOW = second cohort, and the thing that is moved or highlighted
  GREEN  = third cohort
  BLUE   = latest-born cohort / upper-layer fate (layer 2)
  PURPLE = progenitors and the cell cycle
  PINK   = preplate, marginal zone, subplate
  TEAL   = the labeled thymidine pulse and its label
  RED    = the rejected prediction (cells shoving outward)
  GREY   = tissue outlines, axes, de-emphasized
"""
import numpy as np
from bp_style import *  # noqa: F401,F403

ORANGE = "#F29E4C"
PURPLE = "#B58CD9"
PINK = "#E58FB4"
COH = [ORANGE, YELLOW, GREEN, BLUE]

X0, X1 = -6.0, -0.5          # slice edges
Y_BOT, Y_TOP = -3.3, 3.1
Y_VENT = -2.95
ROWS = [-1.4, -0.4, 0.6, 1.6]
LX = -0.2                     # left edge of right-hand labels
R = 0.18


def col_x(k, i):
    return -5.4 + i * 1.75 + k * 0.36


def slice_frame(vent_label=True):
    box = Rectangle(width=X1 - X0, height=Y_TOP - Y_BOT, stroke_color=GREY, stroke_width=2.5,
                    fill_opacity=0).move_to([(X0 + X1) / 2, (Y_TOP + Y_BOT) / 2, 0])
    surf = Line([X0, Y_TOP, 0], [X1, Y_TOP, 0], color=GREY, stroke_width=6)
    vent = Rectangle(width=X1 - X0, height=0.7, stroke_width=0, fill_color=PURPLE, fill_opacity=0.28
                     ).move_to([(X0 + X1) / 2, Y_BOT + 0.35, 0])
    return VGroup(box, vent, surf)


def lab(text, y, color=TEXT, size=22):
    t = T(text, size, color)
    return t.move_to([LX + t.width / 2, y, 0])


def nd(color, x, y, r=R):
    return Circle(radius=r, stroke_color=color, stroke_width=2, fill_color=color, fill_opacity=0.9).move_to([x, y, 0])


def cohort_at_vent(k):
    return VGroup(*[nd(COH[k], col_x(k, i), Y_VENT) for i in range(3)])


def cohort_final(k):
    return VGroup(*[nd(COH[k], col_x(k, i), ROWS[k]) for i in range(3)])


def rise(g, y, rt=1.2, lag=0.12):
    return LaggedStart(*[d.animate.set_y(y) for d in g], lag_ratio=lag, run_time=rt)


def arr(a, b, color=GREY, w=5):
    return Arrow(a, b, buff=0.08, color=color, stroke_width=w, tip_length=0.22,
                 max_tip_length_to_length_ratio=0.45, max_stroke_width_to_length_ratio=12)


class S00Title(TitleCard):
    LESSON = "Birth order and fate"
    TITLE = "The day you are born sets your layer"


# ---------------------------------------------------------------------------------------------
class S01Climb(SpokenScene):
    def construct(self):
        sl = slice_frame()
        vl = lab("ventricle", Y_VENT, PURPLE)
        self.play(FadeIn(sl), FadeIn(vl), run_time=0.7)
        a = nd(ORANGE, -4.4, Y_VENT, 0.3)
        b = nd(BLUE, -2.4, Y_VENT, 0.3)
        self.at("first cortical plate")
        self.play(FadeIn(a, scale=0.5), run_time=0.4)
        self.play(a.animate.set_y(ROWS[0]), FadeIn(lab("first plate neurons: deepest", ROWS[0], ORANGE)), run_time=1.6)
        self.at("days later")
        self.play(FadeIn(b, scale=0.5), run_time=0.4)
        ghost = DashedLine([-2.4, Y_VENT + 0.35, 0], [-2.4, ROWS[3] - 0.35, 0], color=GREY, stroke_width=3)
        self.at("near the ventricle")
        self.play(Indicate(sl[1], color=PURPLE, scale_factor=1.0), run_time=0.8)
        self.at("climb past")
        self.play(Create(ghost), b.animate.set_y(ROWS[3]), FadeIn(lab("born later: near the surface", ROWS[3], BLUE)),
                  run_time=2.0)
        q = T("?", 120, YELLOW, weight=BOLD).move_to([3.3, 0.1, 0])
        self.at("birthday decide")
        self.play(FadeIn(q, scale=0.6), run_time=0.5)
        self.play(Indicate(q, color=YELLOW, scale_factor=1.2), run_time=0.8)
        self.finish()


# ---------------------------------------------------------------------------------------------
class S02Build(SpokenScene):
    def construct(self):
        sl = slice_frame()
        self.add(sl)
        progs = VGroup(*[Circle(radius=0.17, stroke_color=PURPLE, stroke_width=2, fill_color=PURPLE, fill_opacity=0.6
                                ).move_to([-5.3 + i * 0.9, Y_VENT, 0]) for i in range(6)])
        plab = lab("progenitors", Y_VENT, PURPLE)
        self.at("Progenitors line the ventricle")
        self.play(FadeIn(progs), FadeIn(plab), run_time=0.8)
        self.at("travel outward")
        pre_d = VGroup(*[nd(PINK, -5.2 + 0.85 * j, Y_VENT, 0.12) for j in range(6)])
        self.play(FadeIn(pre_d), run_time=0.3)
        self.play(pre_d.animate.set_y(2.55), run_time=1.6)
        self.at("thin sheet")
        band = RoundedRectangle(corner_radius=0.12, width=5.2, height=0.5, stroke_color=PINK, stroke_width=2.5,
                                fill_color=PINK, fill_opacity=0.4).move_to([(X0 + X1) / 2, 2.55, 0])
        pre_l = lab("preplate", 2.55, PINK)
        self.play(FadeIn(band), FadeOut(pre_d), FadeIn(pre_l), FadeOut(plab), run_time=0.8)
        self.at("splits it in two")
        mz = RoundedRectangle(corner_radius=0.1, width=5.2, height=0.3, stroke_color=PINK, stroke_width=2.5,
                              fill_color=PINK, fill_opacity=0.4).move_to([(X0 + X1) / 2, 2.8, 0])
        sp = mz.copy().move_to([(X0 + X1) / 2, -2.2, 0])
        c0 = cohort_at_vent(0)
        self.play(FadeIn(c0), run_time=0.3)
        self.play(Transform(band, mz), TransformFromCopy(band, sp), FadeOut(pre_l), rise(c0, ROWS[0], 1.6), run_time=1.6)
        self.at("marginal zone")
        l_mz = lab("marginal zone (layer 1)", 2.8, PINK)
        self.play(FadeIn(l_mz), run_time=0.4)
        self.at("subplate")
        l_sp = lab("subplate", -2.2, PINK)
        self.play(FadeIn(l_sp), run_time=0.4)
        self.at("Each later wave")
        groups = [cohort_at_vent(k) for k in (1, 2, 3)]
        self.play(*[FadeIn(g) for g in groups], run_time=0.3)
        self.play(LaggedStart(*[rise(g, ROWS[k], 2.2) for g, k in zip(groups, (1, 2, 3))], lag_ratio=0.35), run_time=3.2)
        self.at("made first")
        l6 = lab("layer 6: made first", ROWS[0], ORANGE)
        self.play(FadeIn(l6), run_time=0.4)
        self.at("made last")
        l2 = lab("layer 2: made last", ROWS[3], BLUE)
        self.play(FadeIn(l2), run_time=0.4)
        self.finish()


# ---------------------------------------------------------------------------------------------
def cell(color, r=0.55, op=0.35):
    return Circle(radius=r, stroke_color=color, stroke_width=4, fill_color=color, fill_opacity=op)


class S03Date(SpokenScene):
    def construct(self):
        yA, yB = 1.5, -1.5
        a = cell(PURPLE, 0.7).move_to([-1.0, yA, 0])
        b = cell(PURPLE, 0.7).move_to([-1.0, yB, 0])
        self.at("how do you know")
        self.play(FadeIn(a, scale=0.7), FadeIn(b, scale=0.7), run_time=0.8)
        self.at("last S phase")
        s_lab = T("copying DNA", 24, PURPLE).next_to(a, UP, buff=0.25)
        s_lab2 = T("copying DNA", 24, PURPLE).next_to(b, DOWN, buff=0.25)
        self.play(FadeIn(s_lab), FadeIn(s_lab2), run_time=0.5)
        self.at("one dose of thymidine")
        pulse = chip("labeled thymidine", TEAL, size=26).move_to([-4.3, (yA + yB) / 2, 0])
        self.play(FadeIn(pulse, shift=RIGHT * 0.2), run_time=0.6)
        self.at("next hour or so")
        dotsA = VGroup(*[Dot(pulse.get_right() + [0.1, 0.1 * j, 0], radius=0.09, color=TEAL) for j in range(-1, 2)])
        dotsB = dotsA.copy()
        self.add(dotsA, dotsB)
        self.play(*[d.animate.move_to(a.get_center() + [-0.3 + 0.3 * i, -0.15 + 0.15 * (i % 2), 0]) for i, d in enumerate(dotsA)],
                  *[d.animate.move_to(b.get_center() + [-0.3 + 0.3 * i, -0.15 + 0.15 * (i % 2), 0]) for i, d in enumerate(dotsB)],
                  run_time=1.2)
        self.play(a.animate.set_stroke(TEAL).set_fill(TEAL, 0.9), b.animate.set_stroke(TEAL).set_fill(TEAL, 0.9),
                  FadeOut(dotsA), FadeOut(dotsB), FadeOut(s_lab), FadeOut(s_lab2), run_time=0.6)
        self.at("divides again halves")
        b1 = b.copy(); b2 = b.copy()
        self.remove(b)
        self.add(b1, b2)
        self.play(b1.animate.move_to([2.6, yB + 0.0, 0]).scale(0.75), b2.animate.move_to([4.2, yB, 0]).scale(0.75),
                  run_time=1.2)
        self.play(b1.animate.set_fill(TEAL, 0.45), b2.animate.set_fill(TEAL, 0.45), run_time=0.8)
        lightlab = T("half the label each", 24, TEAL).move_to([3.4, yB - 1.0, 0])
        self.play(FadeIn(lightlab), run_time=0.4)
        self.at("heavily labeled")
        self.play(a.animate.move_to([3.4, yA, 0]), run_time=1.2)
        heavy = T("heavy label: left the cycle", 24, TEAL).move_to([3.4, yA + 1.1, 0])
        self.play(FadeIn(heavy), run_time=0.4)
        self.at("label was there")
        self.play(Indicate(a, color=TEAL, scale_factor=1.12), run_time=0.8)
        self.at("marks that moment")
        stamp = T("a date stamp, not an instruction", 26, TEXT).move_to([1.5, -3.1, 0])
        self.play(FadeIn(stamp, shift=UP * 0.1), run_time=0.6)
        self.finish()


# ---------------------------------------------------------------------------------------------
class S04Order(SpokenScene):
    def construct(self):
        sl = slice_frame()
        self.add(sl)
        cs = [cohort_final(k) for k in range(4)]
        labs = [lab("labeled earliest: deepest", ROWS[0], ORANGE), lab("labeled later: nearer the surface", ROWS[3], BLUE)]
        pul = chip("one pulse per embryonic day", TEAL, size=24).move_to([LX + 2.5, 0.1, 0])
        self.at("pulses on different")
        self.play(FadeIn(pul, shift=LEFT * 0.2), run_time=0.6)
        self.at("Cells labeled earliest")
        self.play(FadeIn(cs[0], scale=0.5), FadeIn(labs[0]), run_time=0.7)
        self.at("later days")
        self.play(LaggedStart(*[FadeIn(cs[k], scale=0.5) for k in (1, 2, 3)], lag_ratio=0.5), FadeIn(labs[1]), run_time=1.8)
        self.at("ruled out")
        self.play(FadeOut(labs[0]), FadeOut(labs[1]), FadeOut(pul), run_time=0.5)
        head = T("if new cells shoved old ones outward", 24, RED).move_to([3.0, 3.0, 0])
        col = VGroup(*[nd(COH[j], 3.0, 1.8 - j * 1.0) for j in range(4)])
        ctop = T("earliest", 22, ORANGE).next_to(col[0], RIGHT, buff=0.3)
        cbot = T("latest", 22, BLUE).next_to(col[3], RIGHT, buff=0.3)
        self.play(FadeIn(head), FadeIn(col), FadeIn(ctop), FadeIn(cbot), run_time=0.8)
        self.at("earliest cells would end up on top")
        self.play(Indicate(col[0], color=ORANGE, scale_factor=1.4), run_time=0.8)
        self.at("on the bottom")
        cross = VGroup(Line([1.45, 0.4, 0], [2.15, -0.3, 0], color=RED, stroke_width=9),
                       Line([1.45, -0.3, 0], [2.15, 0.4, 0], color=RED, stroke_width=9))
        nolab = T("not what is seen", 24, RED).move_to([3.4, -2.2, 0])
        self.play(Create(cross), FadeIn(nolab), Indicate(cs[0], color=ORANGE, scale_factor=1.3), run_time=0.9)
        self.at("Later cells passed them")
        runner = nd(BLUE, -4.55, Y_VENT, 0.2)
        self.play(FadeIn(runner), run_time=0.3)
        self.play(runner.animate.set_y(ROWS[3] + 0.0), run_time=1.8)
        self.finish()


# ---------------------------------------------------------------------------------------------
class S05Move(SpokenScene):
    def construct(self):
        sl = slice_frame(vent_label=False)
        bands = VGroup(*[RoundedRectangle(corner_radius=0.1, width=5.2, height=0.7, stroke_width=0, fill_color=COH[k],
                                          fill_opacity=0.18).move_to([(X0 + X1) / 2, ROWS[k], 0]) for k in range(4)])
        # older host: its deep layers are already made (host neurons, dimmed); young host has none
        host = VGroup(*[nd(COH[k], col_x(k, i), ROWS[k], 0.16).set_opacity(0.5) for k in range(3) for i in (0, 2)])
        self.add(sl, bands, host)
        head = T("older host: makes upper layers", 24, TEXT).move_to([LX + 2.9, 3.05, 0])
        seg1 = Rectangle(width=2.2, height=0.7, stroke_color=PURPLE, stroke_width=3, fill_color=PURPLE, fill_opacity=0.25
                         ).move_to([LX + 1.2, 0.5, 0])
        seg2 = Rectangle(width=3.4, height=0.7, stroke_color=PURPLE, stroke_width=3, fill_color=PURPLE, fill_opacity=0.55
                         ).move_to([LX + 3.9, 0.5, 0])
        t1 = T("S phase", 22, TEXT).move_to(seg1)
        t2 = T("later in the cycle", 22, TEXT).move_to(seg2)
        donor = nd(ORANGE, -3.4, Y_VENT, 0.24)
        dl = T("deep-layer progenitor", 22, ORANGE).move_to([LX + 1.9, Y_VENT, 0])
        self.at("own schedule")
        self.play(FadeIn(head), FadeIn(seg1), FadeIn(seg2), FadeIn(t1), FadeIn(t2), run_time=0.8)
        self.at("McConnell moved ferret")
        self.play(FadeIn(donor, scale=0.5), FadeIn(dl), run_time=0.6)
        mk = Triangle(color=YELLOW, fill_opacity=1, stroke_width=0).scale(0.22).rotate(PI).move_to(seg1.get_top() + UP * 0.35)
        self.at("while copying DNA")
        self.play(FadeIn(mk, shift=DOWN * 0.2), run_time=0.4)
        dau = nd(ORANGE, -3.4, Y_VENT, 0.2)
        self.add(dau)
        self.at("upper layers")
        self.play(dau.animate.set_y(ROWS[3]), run_time=1.6)
        self.play(dau.animate.set_color(BLUE).set_fill(BLUE, 0.9), run_time=0.4)
        res = lab("upper layers, like the host", ROWS[3], BLUE)
        self.play(FadeIn(res), run_time=0.4)
        self.at("moved later in the cycle")
        # reset the old answer in the same beat as the new case
        self.play(FadeOut(dau), FadeOut(res), mk.animate.move_to(seg2.get_top() + UP * 0.35), run_time=0.7)
        dau = nd(ORANGE, -3.4, Y_VENT, 0.2)
        self.add(dau)
        self.at("settled in the deep layers")
        self.play(dau.animate.set_y(ROWS[0]), run_time=1.4)
        res = lab("deep layers, as their birthday said", ROWS[0], ORANGE)
        self.play(FadeIn(res), run_time=0.4)
        self.at("fate was already fixed")
        fixed = T("fate fixed", 24, YELLOW).next_to(seg2, DOWN, buff=0.25)
        self.play(FadeIn(fixed), run_time=0.5)
        self.at("Late progenitors")
        late = nd(BLUE, -3.4, Y_VENT, 0.24)
        late_l = T("late progenitor", 22, BLUE).move_to([LX + 1.9, Y_VENT, 0])
        head2 = T("young host: makes deep layers", 24, TEXT).move_to([LX + 2.9, 3.05, 0])
        self.play(FadeOut(dau), FadeOut(res), FadeOut(fixed), FadeOut(mk), FadeOut(seg1), FadeOut(seg2), FadeOut(t1),
                  FadeOut(t2), FadeOut(donor), FadeOut(dl), FadeOut(host), Transform(head, head2), FadeIn(late), FadeIn(late_l), run_time=0.8)
        dau = nd(BLUE, -3.4, Y_VENT, 0.2)
        self.add(dau)
        self.at("still made")
        self.play(dau.animate.set_y(ROWS[3]), run_time=1.6)
        res = lab("still upper layers", ROWS[3], BLUE)
        self.play(FadeIn(res), run_time=0.4)
        self.finish()


# ---------------------------------------------------------------------------------------------
class S06Rule(SpokenScene):
    def construct(self):
        sl = slice_frame(vent_label=False)
        self.add(sl)
        cs = [cohort_final(k) for k in range(4)]
        self.add(*cs)
        l0 = lab("early: deep", ROWS[0], ORANGE)
        l3 = lab("later: above", ROWS[3], BLUE)
        up = arr([X1 + 0.1, ROWS[0] + 0.3, 0], [X1 + 0.1, ROWS[3] - 0.3, 0], GREY)
        self.at("birthday predicts its layer")
        self.play(FadeIn(l0), FadeIn(l3), run_time=0.6)
        self.at("pass them")
        runner = nd(BLUE, -4.3, Y_VENT, 0.2)
        self.add(runner)
        self.play(runner.animate.set_y(ROWS[3] - 0.0), run_time=1.5)
        self.play(FadeOut(runner), run_time=0.2)
        self.at("choices narrow")
        self.play(FadeOut(l0), FadeOut(l3), run_time=0.4)
        head = T("what a progenitor can still make", 24, TEXT).move_to([LX + 3.0, 3.05, 0])
        rows = []
        specs = [("young", [0, 1, 2, 3], 1.9), ("older", [1, 2, 3], 0.6), ("late", [2, 3], -0.7)]
        note = T("schematic: fewer choices with age", 22, GREY).move_to([LX + 3.0, 2.55, 0])
        self.play(FadeIn(head), FadeIn(note), run_time=0.4)
        for name, ks, y in specs:
            t = T(name + " progenitor", 24, PURPLE).move_to([LX + 1.3, y, 0])
            t.set_x(LX + t.width / 2)
            sw = VGroup(*[nd(COH[k], LX + 4.0 + 0.6 * k, y, 0.2) for k in ks])
            rows.append((t, sw))
        self.play(*[FadeIn(m) for r in rows for m in r], run_time=0.5)
        self.at("do not reverse")
        ar = arr([LX + 3.2, -0.5, 0], [LX + 3.2, 1.5, 0], GREY)
        xx = VGroup(Line([LX + 3.05, 0.35, 0], [LX + 3.35, 0.65, 0], color=RED, stroke_width=8),
                    Line([LX + 3.05, 0.65, 0], [LX + 3.35, 0.35, 0], color=RED, stroke_width=8))
        ar = VGroup(ar, xx)
        self.play(FadeIn(ar), run_time=0.6)
        self.at("Keep the rule")
        self.play(FadeOut(head), FadeOut(note), FadeOut(ar), *[FadeOut(m) for r in rows for m in r], run_time=0.5)
        rule = T("birthday predicts layer", 36, TEXT, font=TITLE_FONT).move_to([LX + 2.9, 0.4, 0])
        self.play(FadeIn(rule, shift=UP * 0.15), run_time=0.7)
        self.finish()


class S07End(EndCard):
    LINE = "When a neuron is born predicts where it settles."
