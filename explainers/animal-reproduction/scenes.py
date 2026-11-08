"""Animal reproduction: the pattern matters, not the amount  (Biochemistrypedia explainer)

One idea: in Knobil's lesioned rhesus monkeys the pituitary read the PATTERN of GnRH, not its total.

COLOR MAP (one color per concept, whole video)
  YELLOW = GnRH (the infusion, the drip, the bursts)
  BLUE   = hypothalamus
  PURPLE = anterior pituitary
  TEAL   = LH and FSH (the gonadotropins)
  ORANGE = gonads
  GREEN  = restored / works
  RED    = lesion / fails / not sustained / turned down
  GREY   = links, time lines, notes
"""
import numpy as np
from bp_style import *  # noqa: F401,F403

PURPLE = "#B58CD9"
ORANGE = "#F29E4C"


def bchip(text, color=BLUE, size=26, **kw):
    c = chip(text, color, size=size, **kw)
    back = RoundedRectangle(corner_radius=0.14, width=c[0].width, height=c[0].height, stroke_width=0,
                            fill_color=BG, fill_opacity=1).move_to(c[0])
    return VGroup(back, *c)


def arr(a, b, color=GREY, w=5, tip=0.22):
    return Arrow(a, b, buff=0.08, color=color, stroke_width=w, tip_length=tip,
                 max_tip_length_to_length_ratio=0.45, max_stroke_width_to_length_ratio=12)


def state_txt(text, color, x=4.6, y=0.8, size=24):
    return T(text, size, color, weight=BOLD).move_to([x, y, 0])


def cross(center, color=RED, r=0.22, w=6):
    c = np.array(center, float)
    return VGroup(Line(c + [-r, -r, 0], c + [r, r, 0], color=color, stroke_width=w),
                  Line(c + [-r, r, 0], c + [r, -r, 0], color=color, stroke_width=w))


def tick(center, r=0.2, w=6):
    c = np.array(center, float)
    return VGroup(Line(c + [-r, 0, 0], c + [-r * 0.3, -r * 0.8, 0], color=GREEN, stroke_width=w),
                  Line(c + [-r * 0.3, -r * 0.8, 0], c + [r, r * 0.9, 0], color=GREEN, stroke_width=w))


def stream(x, y_top, y_bot, w=12):
    return Line([x, y_top, 0], [x, y_bot, 0], color=YELLOW, stroke_width=w)


def bursts(x, y_top, y_bot, n=3):
    span = (y_top - y_bot) / n
    return VGroup(*[Line([x, y_top - i * span, 0], [x, y_top - i * span - span * 0.4, 0], color=YELLOW, stroke_width=12)
                    for i in range(n)])


LANE_X0, LANE_X1 = -3.9, 5.7
BAR_X = [-3.0, -1.2, 0.6, 2.4, 4.2]


class Rig:
    """The monkey rig: hypothalamus, pituitary, LH and FSH output, GnRH infusion, and two schedule lanes."""

    def __init__(self, dy=0.0):
        self.dy = dy
        d = dy
        self.hypo = bchip("hypothalamus", BLUE, 28).move_to([-5.0, 1.5 + d, 0])
        self.pit = bchip("pituitary", PURPLE, 28).move_to([-0.6, 1.5 + d, 0])
        self.out = bchip("LH, FSH", TEAL, 28).move_to([4.6, 1.5 + d, 0])
        self.link = DashedLine(self.hypo.get_right() + RIGHT * 0.1, self.pit.get_left() + LEFT * 0.1, color=GREY,
                               stroke_width=4, dash_length=0.14)
        self.cut = cross([(self.hypo.get_right()[0] + self.pit.get_left()[0]) / 2, 1.5 + d, 0])
        self.oarrow = arr(self.pit.get_right(), self.out.get_left(), TEAL)
        self.drip = bchip("GnRH infusion", YELLOW, 26).move_to([-0.6, 3.0 + d, 0])
        self.darrow = arr(self.drip.get_bottom(), self.pit.get_top(), YELLOW, w=4)
        self.lesion = T("lesion", 24, RED, weight=BOLD).move_to([-5.0, 0.8 + d, 0])
        self.intact = T("intact", 24, TEXT, weight=BOLD).move_to([-0.6, 0.8 + d, 0])
        self.ya = -0.5 + d   # lane A baseline
        self.yb = -2.6 + d   # lane B baseline
        self.lab_a = T("continuous", 24, GREY).move_to([-5.2, self.ya + 0.3, 0])
        self.lab_b = T("once an hour", 24, GREY).move_to([-5.0, self.yb + 0.45, 0])
        self.base_a = Arrow([LANE_X0, self.ya, 0], [LANE_X1 + 0.3, self.ya, 0], buff=0, color=GREY, stroke_width=3,
                            tip_length=0.18)
        self.base_b = Arrow([LANE_X0, self.yb, 0], [LANE_X1 + 0.3, self.yb, 0], buff=0, color=GREY, stroke_width=3,
                            tip_length=0.18)
        self.time = T("time", 22, GREY).move_to([5.9, self.yb - 0.3, 0])
        self.band = Rectangle(width=LANE_X1 - LANE_X0 - 0.2, height=0.6, stroke_width=0, fill_color=YELLOW,
                              fill_opacity=0.9).move_to([(LANE_X0 + LANE_X1) / 2 + 0.0, self.ya + 0.3 + 0.01, 0])
        self.band.align_to([LANE_X0 + 0.1, 0, 0], LEFT)
        self.bars = [Rectangle(width=0.2, height=0.95, stroke_width=0, fill_color=YELLOW, fill_opacity=0.95)
                     .move_to([x, self.yb + 0.475 + 0.01, 0]) for x in BAR_X]

    def base(self):
        """hypothalamus, link, pituitary, output arrow, output chip (the healthy-looking axis)."""
        return VGroup(self.hypo, self.pit, self.out, self.oarrow)

    def all_static(self):
        return [self.hypo, self.pit, self.out, self.oarrow, self.link, self.cut, self.drip, self.darrow,
                self.lesion, self.intact, self.lab_a, self.lab_b, self.base_a, self.base_b]


class S00Title(TitleCard):
    LESSON = "Animal reproduction"
    TITLE = "The pattern matters, not just the amount"


# ---------------------------------------------------------------------------------------------
class S01Puzzle(SpokenScene):
    """Two drips into the same pituitary: steady fails, hourly bursts work. Why?"""

    def construct(self):
        head = T("female rhesus monkey, hypothalamic drive lost", 28, GREY).move_to([0, 3.2, 0])
        xs = [-3.4, 3.4]
        pits = [bchip("pituitary", PURPLE, 34).move_to([x, 0.3, 0]) for x in xs]
        srcs = [bchip("GnRH", YELLOW, 34).move_to([x, 2.4, 0]) for x in xs]
        divider = DashedLine([0, 2.7, 0], [0, -0.9, 0], color=GREY, stroke_width=2, dash_length=0.12)
        self.at("female rhesus monkey")
        self.play(FadeIn(head), FadeIn(pits[0]), FadeIn(pits[1]), FadeIn(divider), run_time=0.7)
        self.at("missing hormone")
        self.play(FadeIn(srcs[0], shift=DOWN * 0.2), FadeIn(srcs[1], shift=DOWN * 0.2), run_time=0.6)
        self.at("Given steadily")
        st = stream(xs[0], 1.9, 0.85)
        self.play(Create(st), run_time=0.9)
        self.at("it fails")
        res_l = VGroup(bchip("fails", RED, 34), ).move_to([xs[0], -1.0, 0])
        x_l = cross([xs[0] + 1.6, -1.0, 0])
        self.play(FadeIn(res_l, shift=UP * 0.15), Create(x_l), pits[0][1].animate.set_stroke(RED), run_time=0.5)
        self.at("short burst")
        bs = bursts(xs[1], 1.9, 0.85)
        self.play(LaggedStart(*[Create(b) for b in bs], lag_ratio=0.45), run_time=1.1)
        self.at("it works")
        res_r = bchip("works", GREEN, 34).move_to([xs[1], -1.0, 0])
        t_r = tick([xs[1] + 1.6, -1.0, 0])
        self.play(FadeIn(res_r, shift=UP * 0.15), Create(t_r), pits[1][1].animate.set_stroke(GREEN), run_time=0.5)
        self.at("timing matter")
        a = bchip("timing", YELLOW, 36)
        q = T("?", 56, GOLD, weight=BOLD)
        b = bchip("amount", YELLOW, 36)
        row = VGroup(a, q, b).arrange(RIGHT, buff=0.7).move_to([0, -2.7, 0])
        self.play(FadeIn(a, shift=RIGHT * 0.2), FadeIn(b, shift=LEFT * 0.2), Write(q), run_time=0.9)
        self.finish()


# ---------------------------------------------------------------------------------------------
class S02Axis(SpokenScene):
    """hypothalamus -> (portal vessels, GnRH) -> anterior pituitary -> (LH, FSH) -> gonads."""

    def construct(self):
        y = 0.5
        hypo = bchip("hypothalamus", BLUE, 32).move_to([-6.25, y, 0]).align_to([-6.25, 0, 0], LEFT)
        pit = bchip("anterior pituitary", PURPLE, 32).move_to([0.5, y, 0])
        gon = bchip("gonads", ORANGE, 32).move_to([0, y, 0]).align_to([6.25, 0, 0], RIGHT)
        a1 = arr(hypo.get_right(), pit.get_left(), YELLOW, w=6)
        a2 = arr(pit.get_right(), gon.get_left(), TEAL, w=6)
        mam = T("in mammals", 26, GREY).move_to([0, 3.0, 0])
        lab_g = T("GnRH", 32, YELLOW, weight=BOLD).next_to(a1, UP, buff=0.12)
        lab_p = T("portal vessels", 24, GREY).move_to([a1.get_center()[0], y - 0.95, 0])
        lab_l = T("LH, FSH", 30, TEAL, weight=BOLD).next_to(a2, UP, buff=0.12)
        lab_gt = T("gonadotropins", 24, GREY).move_to([a2.get_center()[0], y - 0.95, 0])
        self.at("neurons in the hypothalamus")
        self.play(FadeIn(mam), FadeIn(hypo, shift=RIGHT * 0.2), run_time=0.7)
        self.at("into portal vessels")
        self.play(GrowArrow(a1), FadeIn(lab_g), FadeIn(lab_p), run_time=0.8)
        self.at("anterior pituitary")
        self.play(FadeIn(pit, shift=RIGHT * 0.2), run_time=0.6)
        self.at("two hormones")
        self.play(GrowArrow(a2), FadeIn(lab_l), run_time=0.7)
        self.at("act on the gonads")
        self.play(FadeIn(gon, shift=RIGHT * 0.2), FadeIn(lab_gt), run_time=0.7)
        self.at("released in pulses")
        start, end = a1.get_start() + RIGHT * 0.1, a1.get_end() - RIGHT * 0.1
        for _ in range(3):
            d = Dot(start, radius=0.13, color=YELLOW)
            self.play(FadeIn(d, run_time=0.1), run_time=0.1)
            self.play(d.animate.move_to(end), run_time=0.5, rate_func=linear)
            self.play(FadeOut(d), run_time=0.1)
            self.wait(0.35)
        self.at("hypothalamic pituitary gonadal axis")
        br = Brace(VGroup(hypo, pit, gon), DOWN, buff=1.05, color=GOLD)
        axl = T("hypothalamic-pituitary-gonadal axis", 30, GOLD).next_to(br, DOWN, buff=0.15)
        self.play(GrowFromCenter(br), FadeIn(axl), run_time=0.9)
        self.finish()


# ---------------------------------------------------------------------------------------------
class S03Setup(SpokenScene):
    """Knobil's rig: lesioned hypothalamus, intact pituitary, GnRH replaced by infusion."""

    def construct(self):
        r = Rig(dy=-0.5)
        head = T("Belchetz, Plant, Nakai, Keogh and Knobil, 1978", 28, GREY).move_to([0, 3.35, 0])
        self.at("1978")
        self.play(FadeIn(head), FadeIn(r.hypo), FadeIn(r.pit), FadeIn(r.out), FadeIn(r.oarrow), run_time=0.8)
        solid = arr(r.hypo.get_right(), r.pit.get_left(), GREY)
        self.play(GrowArrow(solid), run_time=0.4)
        monk = T("female rhesus monkeys", 26, GREY).move_to([-4.4, 2.5, 0])
        self.at("rhesus monkeys")
        self.play(FadeIn(monk), run_time=0.5)
        self.at("Lesions of the hypothalamus")
        self.play(FadeOut(solid), Create(r.link), Create(r.cut), FadeIn(r.lesion), r.hypo[1].animate.set_stroke(RED),
                  run_time=0.8)
        self.at("abolished")
        ab = state_txt("abolished", RED, y=0.8 - 0.5)
        self.play(r.oarrow.animate.set_color(RED).set_opacity(0.5), FadeIn(ab, shift=UP * 0.1), run_time=0.6)
        self.at("pituitary was intact")
        self.play(FadeIn(r.intact), Indicate(r.pit[2], color=PURPLE, scale_factor=1.2), run_time=0.7)
        self.at("intravenous infusion")
        self.play(FadeIn(r.drip, shift=DOWN * 0.2), GrowArrow(r.darrow), run_time=0.7)
        self.at("continuously")
        self.play(FadeIn(r.lab_a), Create(r.base_a), run_time=0.6)
        self.at("once an hour")
        self.play(FadeIn(r.lab_b), Create(r.base_b), run_time=0.6)
        self.at("blood samples")
        tag = T("measured in blood", 22, GREY).move_to([4.6, 0.3 - 0.5, 0])
        self.play(FadeIn(tag), Indicate(r.out[2], color=TEAL, scale_factor=1.2), run_time=0.7)
        self.finish()


# ---------------------------------------------------------------------------------------------
def rebuild_s03(scene, r):
    """The end state of s03, rebuilt at its place (dy=-0.5)."""
    ab = state_txt("abolished", RED, y=0.8 + r.dy)
    r.oarrow.set_color(RED).set_opacity(0.5)
    r.hypo[1].set_stroke(RED)
    scene.add(r.hypo, r.pit, r.out, r.oarrow, r.link, r.cut, r.lesion, r.intact, r.drip, r.darrow,
              r.lab_a, r.lab_b, r.base_a, r.base_b, ab)
    return ab


class S04Steady(SpokenScene):
    """continuous infusion: the band grows, LH and FSH are not sustained."""

    def construct(self):
        r = Rig(dy=-0.5)
        ab = rebuild_s03(self, r)
        # slide up to make room for the lanes
        grp = Group(r.hypo, r.pit, r.out, r.oarrow, r.link, r.cut, r.lesion, r.intact, r.drip, r.darrow,
                    r.lab_a, r.lab_b, r.base_a, r.base_b, ab)
        r2 = Rig(dy=0.0)
        self.at("First")
        q = state_txt("?", GREY, y=0.8, size=34)
        self.play(grp.animate.shift(UP * 0.5), run_time=0.4)
        self.play(ReplacementTransform(ab, q),
                  r.oarrow.animate.set_color(TEAL).set_opacity(1.0), FadeIn(r2.time), run_time=0.4)
        self.at("continuous infusion")
        self.play(Indicate(r.lab_a, color=YELLOW, scale_factor=1.15), run_time=0.6)
        self.at("has the hormone all the time")
        thick = Line(r.darrow.get_start(), r.darrow.get_end() + UP * 0.15, color=YELLOW, stroke_width=12)
        self.play(GrowFromEdge(r2.band, LEFT), FadeIn(thick), run_time=3.0, rate_func=linear)
        self.at("total amount")
        self.play(Indicate(r2.band, color=YELLOW, scale_factor=1.04), run_time=0.7)
        self.at("It did not")
        no = state_txt("not sustained", RED, y=0.8)
        self.play(ReplacementTransform(q, no), r.oarrow.animate.set_color(RED), Indicate(r.out[2], color=RED, scale_factor=1.2),
                  run_time=0.6)
        self.finish()


class S05Pulses(SpokenScene):
    """hourly bursts: LH and FSH restored; return to pulses restores them again."""

    def construct(self):
        r = Rig(dy=0.0)
        # end state of s04 (rebuilt in place)
        no = state_txt("not sustained", RED, y=0.8)
        r.oarrow.set_color(RED)
        r.hypo[1].set_stroke(RED)
        thick = Line(r.darrow.get_start(), r.darrow.get_end() + UP * 0.15, color=YELLOW, stroke_width=12)
        self.add(r.hypo, r.pit, r.out, r.oarrow, r.link, r.cut, r.lesion, r.intact, r.drip, r.darrow,
                 r.lab_a, r.lab_b, r.base_a, r.base_b, r.band, no, thick, r.time)
        self.at("Next")
        q = state_txt("?", GREY, y=0.8, size=34)
        self.play(r.band.animate.set_opacity(0.3), FadeOut(thick), ReplacementTransform(no, q),
                  r.oarrow.animate.set_color(TEAL), run_time=0.6)
        self.at("brief infusions")
        self.play(Indicate(r.lab_b, color=YELLOW, scale_factor=1.15), run_time=0.5)
        self.at("once an hour")
        for i, bar in enumerate(r.bars):
            d = Dot(r.drip.get_bottom() + DOWN * 0.1, radius=0.12, color=YELLOW)
            self.play(GrowFromEdge(bar, DOWN), FadeIn(d), run_time=0.1)
            self.play(d.animate.move_to(r.pit.get_top() + UP * 0.1), run_time=0.18, rate_func=linear)
            self.play(FadeOut(d), run_time=0.05)
        br = DoubleArrow([BAR_X[0], r.yb + 1.2, 0], [BAR_X[1], r.yb + 1.2, 0], buff=0, color=GREY, stroke_width=3,
                         tip_length=0.15)
        h = T("1 hour", 22, GREY).move_to([(BAR_X[0] + BAR_X[1]) / 2, r.yb + 1.55, 0])
        self.play(GrowFromCenter(br), FadeIn(h), run_time=0.4)
        self.at("restored")
        ok = state_txt("restored", GREEN, y=0.8)
        self.play(ReplacementTransform(q, ok), Indicate(r.out[2], color=GREEN, scale_factor=1.2), run_time=0.6)
        self.at("returning to the hourly schedule")
        back = CurvedArrow([LANE_X1 + 0.05, r.ya + 0.25, 0], [LANE_X1 + 0.05, r.yb + 0.9, 0], angle=-PI / 2.2,
                           color=GREY, stroke_width=4, tip_length=0.2)
        bl = T("back to pulses", 22, GREY).move_to([4.0, r.yb + 1.55, 0])
        self.play(Create(back), FadeIn(bl), run_time=0.8)
        self.at("secretion back")
        self.play(Indicate(ok, color=GREEN, scale_factor=1.2), Indicate(r.out[2], color=GREEN, scale_factor=1.2), run_time=0.8)
        self.finish()


# ---------------------------------------------------------------------------------------------
class S06Rule(SpokenScene):
    """Same pituitary, two patterns: steady turns it down, hourly bursts restore LH and FSH."""

    def construct(self):
        xs = [-3.6, 3.4]
        srcs = [bchip("GnRH", YELLOW, 28).move_to([x, 3.0, 0]) for x in xs]
        pits = [bchip("pituitary", PURPLE, 28).move_to([x, 1.0, 0]) for x in xs]
        st = stream(xs[0], 2.55, 1.5)
        bs = bursts(xs[1], 2.55, 1.5)
        sub_l = T("steady", 26, GREY).move_to([xs[0] - 1.9, 2.0, 0])
        sub_r = T("hourly", 26, GREY).move_to([xs[1] - 1.9, 2.0, 0])
        divider = DashedLine([0, 3.2, 0], [0, -0.35, 0], color=GREY, stroke_width=2, dash_length=0.12)
        self.at("pattern of")
        self.play(*[FadeIn(m) for m in srcs + pits], FadeIn(divider), Create(st), FadeIn(sub_l), FadeIn(sub_r),
                  LaggedStart(*[Create(b) for b in bs], lag_ratio=0.4), run_time=1.4)
        heading = T("pattern, not total amount", 40, font=TITLE_FONT).move_to([0, -1.05, 0])
        res_l = bchip("LH, FSH not sustained", RED, 26).move_to([xs[0], -0.0 + 0.0, 0]).shift(DOWN * 0.0)
        res_r = bchip("LH, FSH restored", GREEN, 26).move_to([xs[1], 0.0, 0])
        self.at("not its total amount")
        self.play(Write(heading), run_time=1.0)
        self.at("controls the pituitary")
        self.play(FadeIn(res_l, shift=UP * 0.1), FadeIn(res_r, shift=UP * 0.1), pits[0][1].animate.set_stroke(RED),
                  pits[1][1].animate.set_stroke(GREEN), run_time=0.7)
        n1 = T("Shown: pattern reading in this primate.", 24, GREY).move_to([0, -2.0, 0])
        n2 = T("Not shown: where the pulses come from, or the normal interval in humans.", 24, GREY).move_to([0, -2.55, 0])
        self.at("shows pattern reading")
        self.play(FadeIn(n1), run_time=0.6)
        self.at("does not show")
        self.play(FadeIn(n2), run_time=0.6)
        n3 = T("In mice: kisspeptin neurons evoked LH pulses. Primates: a separate question.", 24, GREY).move_to([0, -3.1, 0])
        self.at("In mice")
        self.play(FadeIn(n3), run_time=0.6)
        self.at("turns the pituitary down")
        dn = Arrow([xs[0] + 1.4, 1.45, 0], [xs[0] + 1.4, 0.6, 0], buff=0, color=RED, stroke_width=8, tip_length=0.25)
        dl = T("turned down", 22, RED, weight=BOLD).move_to([xs[0] + 2.6, 1.0, 0])
        self.play(GrowArrow(dn), FadeIn(dl), run_time=0.7)
        self.finish()


class S07End(EndCard):
    LINE = "In these monkeys, the pattern of GnRH controls the pituitary."
