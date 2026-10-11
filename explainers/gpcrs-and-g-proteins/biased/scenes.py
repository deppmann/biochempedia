"""Section film: Drugs at GPCRs (Biochemistrypedia explainer)

Timed to the SPOKEN words: every self.at("...") cue waits for that phrase in audio/words.json.

COLOR MAP (one color per concept, whole video)
  BLUE   = receptor in the inactive shape
  GREEN  = receptor in the active shape, and the signal meter fill
  YELLOW = agonist (and any other ligand)
  PURPLE = neutral antagonist
  RED    = inverse agonist
  GREY   = membrane, meter frame, basal line, labels, notes
"""
import numpy as np
from bp_style import *  # noqa: F401,F403

PURPLE = "#B58CD9"

XS = [-5.2, -3.1, -1.0, 1.1]      # receptor centres
TOP_Y = 1.3                         # top of the two bars
BAR_W, BAR_H, OFFS, ANG = 0.30, 2.6, 0.24, 0.20
POCKET_Y = TOP_Y + 0.16
FREE_Y = 2.55
MX, MB, MH, MW = 3.9, -2.3, 4.4, 0.8   # meter
BASAL, HIGH, LOW = 0.20, 0.76, 0.04


def rec(x, active):
    """A receptor: two bars crossing the membrane; the lower ends splay apart when active."""
    col = GREEN if active else BLUE
    bars = []
    for sgn in (-1, 1):
        b = RoundedRectangle(corner_radius=0.14, width=BAR_W, height=BAR_H, stroke_color=col, stroke_width=4,
                             fill_color=col, fill_opacity=0.35)
        b.move_to([x + sgn * OFFS, TOP_Y - BAR_H / 2, 0])
        if active:
            b.rotate(sgn * ANG, about_point=np.array([x + sgn * OFFS, TOP_Y, 0]))
        bars.append(b)
    return VGroup(*bars)


def lig(x, color, y=POCKET_Y):
    return Circle(radius=0.24, stroke_color=color, stroke_width=3, fill_color=color, fill_opacity=0.9).move_to([x, y, 0])


def meter_y(level):
    return MB + MH * level


class Stage(SpokenScene):
    """Shared stage: membrane, four receptors, signal meter, legend, note."""

    def stage(self, active=(), level=BASAL, basal=True, legend=True, hint=False):
        self.mem = RoundedRectangle(corner_radius=0.1, width=8.6, height=0.6, stroke_color=GREY, stroke_width=3,
                                    fill_color=GREY, fill_opacity=0.3).move_to([-2.0, 0.0, 0])
        self.R = [rec(x, i in active) for i, x in enumerate(XS)]
        self.act = [i in active for i in range(4)]
        self.tr = ValueTracker(level)
        frame = Rectangle(width=MW, height=MH, stroke_color=GREY, stroke_width=3).move_to([MX, MB + MH / 2, 0])
        tr = self.tr

        def mk():
            h = max(0.03, tr.get_value() * MH)
            return Rectangle(width=MW - 0.1, height=h, stroke_width=0, fill_color=GREEN, fill_opacity=0.85).move_to(
                [MX, MB + h / 2, 0])
        self.fill = always_redraw(mk)
        title = T("signal", 26).move_to([MX, MB + MH + 0.4, 0])
        self.meter_static = VGroup(frame, title)
        self.basal_line = VGroup(
            DashedLine([MX - 0.65, meter_y(BASAL), 0], [MX + 0.65, meter_y(BASAL), 0], color=TEXT, stroke_width=3),
            T("basal", 24, GREY).move_to([MX - 1.35, meter_y(BASAL), 0]))
        self.legend = VGroup(chip("inactive shape", BLUE, size=24), chip("active shape", GREEN, size=24))
        self.legend[0].move_to([-4.7, -2.8, 0])
        self.legend[1].move_to([-1.6, -2.8, 0])
        self.note = T("idealised, not to scale", 22, GREY).move_to([-2.0, -3.4, 0])
        self.status = None
        parts = [self.mem, *self.R, self.meter_static, self.fill, self.note]
        if basal:
            parts.append(self.basal_line)
        if legend:
            parts.append(self.legend)
        return parts

    def build(self, **kw):
        parts = self.stage(**kw)
        self.add(*parts)
        self.play(*[FadeIn(p) for p in parts if p is not self.fill], run_time=0.5)

    def flip(self, i, on, rt=0.3):
        self.act[i] = on
        return Transform(self.R[i], rec(XS[i], on))

    def set_status(self, text, color=TEXT):
        new = T(text, 24, color).move_to([MX, MB - 0.45, 0])
        if self.status is None:
            self.play(FadeIn(new), run_time=0.3)
        else:
            self.play(ReplacementTransform(self.status, new), run_time=0.3)
        self.status = new

    def header(self, text, color):
        h = T(text, 34, color, weight=BOLD).move_to([-2.0, 3.15, 0])
        self.play(FadeIn(h, shift=DOWN * 0.15), run_time=0.4)
        return h


class S00Title(TitleCard):
    LESSON = "GPCRs and Trimeric G Proteins"
    TITLE = "Three Ways a Drug Moves a Receptor"


# ---------------------------------------------------------------------------------------------
class S01Basal(Stage):
    """Empty pockets, flickering shapes, basal signal, three ways to act."""

    def construct(self):
        parts = self.stage(active=(), level=0.0, basal=False, legend=False)
        q = T("?", 80, GREY).move_to([MX, MB + MH / 2, 0])
        self.add(self.mem, self.fill)
        self.play(FadeIn(self.mem), *[FadeIn(r) for r in self.R], FadeIn(self.meter_static), FadeIn(q),
                  FadeIn(self.note), run_time=0.7)
        self.at("empty pocket")
        x = XS[1]
        lab = T("empty pocket", 26, TEXT).move_to([x, 2.75, 0])
        arrow = Arrow([x, 2.4, 0], [x, 1.62, 0], buff=0.05, color=TEXT, stroke_width=4, tip_length=0.2)
        self.play(FadeIn(lab), GrowArrow(arrow), run_time=0.6)
        self.at("flickers")
        self.play(FadeOut(lab), FadeOut(arrow), FadeIn(self.legend), run_time=0.5)
        seq = [1, 2, 0, 1, 3, 2]
        end_t = self.t_of("small fraction") - 0.9
        k = 0
        while self.elapsed() + 1.0 < end_t and k < 12:
            i = seq[k % len(seq)]
            self.play(self.flip(i, True), run_time=0.3)
            self.wait(0.25)
            self.play(self.flip(i, False), run_time=0.3)
            self.wait(0.1)
            k += 1
        self.at("small fraction")
        hint = T("for many receptors: a small fraction active", 24, GREY).move_to([-2.0, -1.9, 0])
        self.play(self.flip(1, True), FadeIn(hint), run_time=0.4)
        self.at("signals a little")
        self.play(FadeOut(q), self.tr.animate.set_value(BASAL), run_time=0.8)
        self.at("basal activity")
        self.play(FadeIn(self.basal_line), run_time=0.5)
        self.at("three ways")
        h = T("three ways for a drug to act", 34, TEXT, weight=BOLD).move_to([-2.0, 3.15, 0])
        self.play(FadeIn(h, shift=DOWN * 0.15), FadeOut(hint), run_time=0.5)
        self.finish()


# ---------------------------------------------------------------------------------------------
class S02Agonist(Stage):
    def construct(self):
        self.build(active=(1,), level=BASAL)
        self.at("agonist")
        hd = self.header("Way 1: agonist", YELLOW)
        d1 = lig(XS[1], YELLOW, y=FREE_Y)
        self.play(FadeIn(d1, shift=DOWN * 0.2), run_time=0.4)
        self.at("active shape")
        self.play(d1.animate.move_to([XS[1], POCKET_Y, 0]), run_time=0.6)
        self.at("more tightly")
        self.play(Indicate(d1, color=YELLOW, scale_factor=1.3), run_time=0.6)
        self.at("holds receptors")
        d0 = lig(XS[0], YELLOW, y=FREE_Y)
        d2 = lig(XS[2], YELLOW, y=FREE_Y)
        self.play(FadeIn(d0, shift=DOWN * 0.2), FadeIn(d2, shift=DOWN * 0.2), run_time=0.4)
        self.play(self.flip(0, True), self.flip(2, True), d0.animate.move_to([XS[0], POCKET_Y, 0]),
                  d2.animate.move_to([XS[2], POCKET_Y, 0]), run_time=0.7)
        self.at("rises above")
        self.play(self.tr.animate.set_value(HIGH), run_time=1.0)
        self.set_status("above basal", GREEN)
        self.finish()


# ---------------------------------------------------------------------------------------------
class S03Antagonist(Stage):
    def construct(self):
        self.build(active=(1,), level=BASAL)
        self.at("neutral antagonist")
        hd = self.header("Way 2: neutral antagonist", PURPLE)
        a0 = lig(XS[0], PURPLE, y=FREE_Y)
        a1 = lig(XS[1], PURPLE, y=FREE_Y)
        self.play(FadeIn(a0, shift=DOWN * 0.2), FadeIn(a1, shift=DOWN * 0.2), run_time=0.4)
        self.at("both shapes")
        self.play(a0.animate.move_to([XS[0], POCKET_Y, 0]), a1.animate.move_to([XS[1], POCKET_Y, 0]), run_time=0.7)
        self.at("equally well")
        self.play(Indicate(a0, color=PURPLE, scale_factor=1.3), Indicate(a1, color=PURPLE, scale_factor=1.3),
                  run_time=0.7)
        self.at("changes nothing")
        self.set_status("unchanged", TEXT)
        self.play(Indicate(self.fill, color=GREEN, scale_factor=1.0), run_time=0.5)
        self.at("occupies the pocket")
        a2 = lig(XS[2], PURPLE, y=FREE_Y)
        a3 = lig(XS[3], PURPLE, y=FREE_Y)
        self.play(FadeIn(a2, shift=DOWN * 0.2), FadeIn(a3, shift=DOWN * 0.2), run_time=0.3)
        self.play(a2.animate.move_to([XS[2], POCKET_Y, 0]), a3.animate.move_to([XS[3], POCKET_Y, 0]), run_time=0.5)
        self.at("keeps other ligands out")
        y = lig(XS[2] + 1.3, YELLOW, y=2.5)
        self.play(FadeIn(y), run_time=0.3)
        self.play(y.animate.move_to([XS[2] + 0.2, 2.0, 0]), run_time=0.5)
        self.play(y.animate.move_to([XS[2] + 1.3, 2.5, 0]), run_time=0.5)
        kept = T("kept out", 24, GREY).move_to([XS[2] + 2.0, 2.0, 0])
        self.play(FadeIn(kept), FadeOut(y), run_time=0.4)
        self.finish()


# ---------------------------------------------------------------------------------------------
class S04Inverse(Stage):
    def construct(self):
        self.build(active=(1,), level=BASAL)
        self.at("inverse agonist")
        hd = self.header("Way 3: inverse agonist", RED)
        r0 = lig(XS[0], RED, y=FREE_Y)
        r2 = lig(XS[2], RED, y=FREE_Y)
        self.play(FadeIn(r0, shift=DOWN * 0.2), FadeIn(r2, shift=DOWN * 0.2), run_time=0.4)
        self.at("inactive shape")
        self.play(r0.animate.move_to([XS[0], POCKET_Y, 0]), r2.animate.move_to([XS[2], POCKET_Y, 0]), run_time=0.6)
        self.at("more tightly")
        self.play(Indicate(r0, color=RED, scale_factor=1.3), Indicate(r2, color=RED, scale_factor=1.3), run_time=0.6)
        self.at("pulls receptors")
        r1 = lig(XS[1], RED, y=FREE_Y)
        self.play(FadeIn(r1, shift=DOWN * 0.2), run_time=0.3)
        self.play(r1.animate.move_to([XS[1], POCKET_Y, 0]), self.flip(1, False), run_time=0.6)
        self.at("below basal")
        self.play(self.tr.animate.set_value(LOW), run_time=0.9)
        self.set_status("below basal", RED)

        # --- a cell with no basal activity: reset everything, then show the two look the same --------
        self.at("no basal activity")
        nb = T("a cell with no basal activity", 34, TEXT, weight=BOLD).move_to([-2.0, 3.15, 0])
        self.play(FadeOut(r0), FadeOut(r1), FadeOut(r2), FadeOut(self.basal_line), FadeOut(self.status),
                  ReplacementTransform(hd, nb), self.tr.animate.set_value(0.0), run_time=0.8)
        self.status = None
        self.at("an antagonist")
        p0 = lig(XS[0], PURPLE, y=FREE_Y)
        p1 = lig(XS[1], PURPLE, y=FREE_Y)
        plab = T("antagonist", 26, PURPLE).move_to([(XS[0] + XS[1]) / 2, 2.35, 0])
        self.play(FadeIn(p0, shift=DOWN * 0.2), FadeIn(p1, shift=DOWN * 0.2), FadeIn(plab), run_time=0.4)
        self.play(p0.animate.move_to([XS[0], POCKET_Y, 0]), p1.animate.move_to([XS[1], POCKET_Y, 0]), run_time=0.5)
        self.at("and an inverse agonist")
        q2 = lig(XS[2], RED, y=FREE_Y)
        q3 = lig(XS[3], RED, y=FREE_Y)
        qlab = T("inverse agonist", 26, RED).move_to([(XS[2] + XS[3]) / 2, 2.35, 0])
        self.play(FadeIn(q2, shift=DOWN * 0.2), FadeIn(q3, shift=DOWN * 0.2), FadeIn(qlab), run_time=0.4)
        self.play(q2.animate.move_to([XS[2], POCKET_Y, 0]), q3.animate.move_to([XS[3], POCKET_Y, 0]), run_time=0.5)
        self.at("look the same")
        self.set_status("same: no signal", TEXT)

        # --- measurable basal activity: the two separate -----------------------------------------
        self.at("measurable basal activity")
        wb = T("a system with basal activity", 34, TEXT, weight=BOLD).move_to([-2.0, 3.15, 0])
        self.play(FadeOut(VGroup(p0, p1, q2, q3, plab, qlab)), FadeOut(self.status), ReplacementTransform(nb, wb),
                  self.flip(1, True), self.tr.animate.set_value(BASAL), FadeIn(self.basal_line), run_time=0.8)
        self.at("tell them apart")
        ta = VGroup(T("antagonist", 22, PURPLE), T("inverse\nagonist", 22, RED, line_spacing=0.6))
        ta[0].move_to([MX + 1.7, meter_y(BASAL) + 0.25, 0])
        tick_p = Line([MX + 0.45, meter_y(BASAL), 0], [MX + 0.85, meter_y(BASAL), 0], color=PURPLE, stroke_width=5)
        tick_r = Line([MX + 0.45, meter_y(LOW), 0], [MX + 0.85, meter_y(LOW), 0], color=RED, stroke_width=5)
        ta[1].move_to([MX + 1.5, meter_y(LOW) - 0.3, 0])
        self.play(FadeIn(ta), Create(tick_p), Create(tick_r), run_time=0.7)

        # --- many drugs long called antagonists ------------------------------------------------
        self.at("long called antagonists")
        c1 = chip("many drugs, long called antagonists", PURPLE, size=24).move_to([-2.0, -1.9, 0])
        self.play(FadeIn(c1, shift=UP * 0.15), run_time=0.5)
        self.at("inverse agonists when")
        c2 = chip("inverse agonists when tested that way", RED, size=24).move_to([-2.0, -1.9, 0])
        self.play(ReplacementTransform(c1, c2), run_time=0.7)
        self.finish()


class S05End(EndCard):
    LINE = "Basal activity gives a drug three ways to act."
