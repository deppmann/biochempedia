"""Endocrine axes and how to test them: read the pair, not one number  (Biochemistrypedia explainer)

Timed to the SPOKEN words: every self.at("...") cue waits for that phrase in audio/words.json.

COLOR MAP (one color per concept, whole video)
  PURPLE = releasing signal from the hypothalamus (CRH)
  YELLOW = trophic hormone from the pituitary (ACTH, TSH), and the synthetic ACTH given in the test
  ORANGE = target hormone from the gland (cortisol, free T4)
  BLUE   = long-loop feedback
  TEAL   = a blood sample, a measurement, an assay, a criterion tied to an assay
  RED    = a lesion or failure (the break in the chain)
  GREEN  = intact / the gland can answer
  WHITE  = (TEXT) the hormone curve in the sketch of pulses
  GREY   = block outlines, axes, conditions, de-emphasized
Bars are "not to scale". The pulse curve is a sketch computed from the lesson's 27 min average half-life.
"""
import numpy as np
from bp_style import *  # noqa: F401,F403

PURPLE = "#B58CD9"
ORANGE = "#F29E4C"

Y0 = 1.0                      # y of the row of blocks
XB = (-4.7, 0.0, 4.7)         # x of hypothalamus, pituitary, target gland
BASE = -2.9                   # baseline of the bars
BARH = 2.4                    # full height of a bar frame
PANEL_L = -6.2                # left edge of the left-hand panel


# ---------------------------------------------------------------------------------------------
# helpers
# ---------------------------------------------------------------------------------------------
def arr(a, b, color=GREY, w=5, tip=0.22):
    return Arrow(a, b, buff=0.0, color=color, stroke_width=w, tip_length=tip,
                 max_tip_length_to_length_ratio=0.45, max_stroke_width_to_length_ratio=14)


def inhib(a, b, color=BLUE, w=5):
    a, b = np.array(a, float), np.array(b, float)
    d = (b - a) / np.linalg.norm(b - a)
    perp = np.array([-d[1], d[0], 0])
    return VGroup(Line(a, b, color=color, stroke_width=w), Line(b + perp * 0.24, b - perp * 0.24, color=color, stroke_width=w + 1))


def bchip(text, color=BLUE, size=26, **kw):
    """chip with an opaque backing, so a line behind it does not show through."""
    c = chip(text, color, size=size, **kw)
    back = RoundedRectangle(corner_radius=0.14, width=c[0].width, height=c[0].height, stroke_width=0,
                            fill_color=BG, fill_opacity=1).move_to(c[0])
    return VGroup(back, *c)


def btext(text, size=24, color=GREY):
    t = T(text, size, color)
    back = Rectangle(width=t.width + 0.2, height=t.height + 0.12, stroke_width=0, fill_color=BG, fill_opacity=1).move_to(t)
    return VGroup(back, t)


def block(name, x, y=Y0, color=GREY):
    rect = RoundedRectangle(corner_radius=0.18, width=3.0, height=1.5, stroke_color=color, stroke_width=4,
                            fill_color=GREY, fill_opacity=0.12).move_to([x, y, 0])
    lab = T(name, 26, TEXT, line_spacing=0.8).move_to(rect)
    g = VGroup(rect, lab)
    g.rect, g.lab = rect, lab
    return g


def badge(text, color, x, y=Y0 + 0.75):
    c = Circle(radius=0.27, stroke_color=color, stroke_width=3, fill_color=BG, fill_opacity=1).move_to([x, y, 0])
    return VGroup(c, T(text, 28, color, weight=BOLD).move_to(c))


def cross(blk, color=RED):
    """a red X in a circle on the top-left corner of the block: marks the break without hiding the label."""
    c = blk.rect.get_corner(UL) + [0.4, 0.0, 0]
    ring = Circle(radius=0.3, stroke_color=color, stroke_width=4, fill_color=BG, fill_opacity=1).move_to(c)
    d = 0.13
    return VGroup(ring, Line(c + [-d, d, 0], c + [d, -d, 0], color=color, stroke_width=6),
                  Line(c + [-d, -d, 0], c + [d, d, 0], color=color, stroke_width=6))


class Ax:
    """The three-block axis: hypothalamus, anterior pituitary, target gland, with feedback."""

    def __init__(self, tgt="Adrenal\ncortex", rel="CRH", tro="ACTH", feedback=True, rel_chip=True):
        self.b = [block("Hypothalamus", XB[0]), block("Anterior\npituitary", XB[1]), block(tgt, XB[2])]
        self.a1 = arr([-3.15, Y0, 0], [-1.55, Y0, 0], PURPLE if rel_chip else GREY)
        self.a2 = arr([1.55, Y0, 0], [3.15, Y0, 0], YELLOW)
        self.c1 = bchip(rel, PURPLE, 24).move_to([-2.35, Y0 + 0.62, 0]) if rel_chip else VGroup()
        self.c2 = bchip(tro, YELLOW, 24).move_to([2.35, Y0 + 0.62, 0])
        top = Y0 + 0.75
        self.v1 = Line([XB[2], top, 0], [XB[2], 2.55, 0], color=BLUE, stroke_width=5)
        self.h = Line([XB[2], 2.55, 0], [XB[0], 2.55, 0], color=BLUE, stroke_width=5)
        self.d1 = inhib([XB[1], 2.55, 0], [XB[1], top + 0.06, 0])
        self.d2 = inhib([XB[0], 2.55, 0], [XB[0], top + 0.06, 0])
        self.fbl = btext("long-loop feedback", 24, BLUE).move_to([-2.35, 2.55, 0])
        self.fb = VGroup(self.v1, self.h, self.d1, self.d2, self.fbl) if feedback else VGroup()
        self.strong = VGroup(T("strong", 22, BLUE).move_to([-5.45, 2.15, 0]), T("strong", 22, BLUE).move_to([0.7, 2.15, 0]))

    def all(self, strong=False):
        g = VGroup(*self.b, self.a1, self.a2, self.c1, self.c2, self.fb)
        if strong:
            g.add(self.strong)
        return g


class Gauge:
    def __init__(self, x, color, name, base=BASE, h=BARH):
        self.x, self.color, self.base, self.h = x, color, base, h
        self.frame = Rectangle(width=0.8, height=h, stroke_color=GREY, stroke_width=3).move_to([x, base + h / 2, 0])
        self.fill = Rectangle(width=0.8, height=0.02, stroke_width=0, fill_color=color, fill_opacity=0.9).move_to([x, base + 0.01, 0])
        self.name = T(name, 26, color).move_to([x, base - 0.32, 0])
        self.val = VGroup()

    def group(self):
        return VGroup(self.frame, self.fill, self.name)

    def set(self, level, text=None):
        """state in one go, no animation (level in bar units, 0 to BARH)."""
        self.fill.stretch_to_fit_height(max(level, 0.02)).align_to(self.frame, DOWN)
        if text:
            self.val = self.text(text)
        return self

    def text(self, s):
        return M(s, 22, self.color).move_to([self.x, self.base + self.h + 0.3, 0])

    def anim(self, level, text=None):
        """animations for a change; call self.val bookkeeping afterwards."""
        a = [self.fill.animate.stretch_to_fit_height(max(level, 0.02)).align_to(self.frame, DOWN)]
        new = self.text(text) if text else VGroup()
        old = self.val
        if len(old) and text:
            a.append(ReplacementTransform(old, new))
        elif text:
            a.append(FadeIn(new))
        elif len(old):
            a.append(FadeOut(old))
        self.val = new
        return a


# the hormone-pulse sketch (scene 1 and the closing recap)
HL = 27.0
PULSES = [(40, 1.0), (175, 1.1), (310, 0.9)]


def level(t):
    v = 0.0
    for t0, a in PULSES:
        tau = t - t0
        if tau < 0:
            continue
        v += a * (tau / 8.0 if tau < 8 else 2 ** (-(tau - 8) / HL))
    return v


class Sketch:
    def __init__(self, x0, yb, xs, ys, tmax=418):
        self.x0, self.yb, self.xs, self.ys, self.tmax = x0, yb, xs, ys, tmax

    def P(self, t, v):
        return np.array([self.x0 + t * self.xs, self.yb + v * self.ys, 0])

    def curve(self, t_end=None, w=5):
        te = self.tmax if t_end is None else max(t_end, 0.5)
        return ParametricFunction(lambda t: self.P(t, level(t)), t_range=[0, te, 0.5], color=TEXT, stroke_width=w,
                                  use_smoothing=False)

    def axes(self, top_v=1.3, w=3):
        xa = Arrow(self.P(0, 0), self.P(self.tmax + 12, 0), buff=0, color=GREY, stroke_width=w, tip_length=0.2,
                   max_tip_length_to_length_ratio=0.2)
        ya = Arrow(self.P(0, 0), self.P(0, top_v), buff=0, color=GREY, stroke_width=w, tip_length=0.2,
                   max_tip_length_to_length_ratio=0.2)
        return VGroup(xa, ya)


class S00Title(TitleCard):
    LESSON = "Endocrine axes and how to test them"
    TITLE = "Read the Pair, Not One Number"


# ---------------------------------------------------------------------------------------------
class S01Curve(SpokenScene):
    """one sample, one number? -> a point riding a pulsatile curve -> half-life -> a sample before a pulse vs on the peak."""

    def construct(self):
        sk = Sketch(-5.6, -2.7, 0.0275, 3.5)

        # the question, drawn: one sample -> one number "?"
        samp = bchip("one blood sample", TEAL, 34).move_to([-3.4, 0.3, 0])
        sarr = arr([-1.3, 0.3, 0], [0.9, 0.3, 0], GREY)
        qbox = RoundedRectangle(corner_radius=0.2, width=2.6, height=1.9, stroke_color=GREY, stroke_width=4,
                                fill_color=GREY, fill_opacity=0.12).move_to([3.4, 0.3, 0])
        q = M("?", 72, YELLOW).move_to(qbox)
        qlab = T("one number", 34, TEXT).next_to(qbox, UP, buff=0.3)
        self.play(FadeIn(samp, shift=RIGHT * 0.2), run_time=0.5)
        self.play(GrowArrow(sarr), FadeIn(VGroup(qbox, qlab)), run_time=0.5)
        self.play(FadeIn(q, scale=0.6), run_time=0.4)
        self.at("What can")
        self.play(Indicate(q, color=YELLOW, scale_factor=1.25), run_time=0.9)

        # one point on a moving curve
        self.at("A hormone level")
        self.play(FadeOut(VGroup(samp, sarr, qbox, qlab, q)), run_time=0.5)
        axes = sk.axes()
        ylab = T("hormone level, relative units (in this sketch)", 22, GREY).move_to([-5.7, 2.1, 0], aligned_edge=LEFT)
        xlab = T("time", 24, GREY).move_to(sk.P(sk.tmax + 12, 0) + [-0.1, -0.35, 0])
        self.at("one point")
        self.play(Create(axes), FadeIn(ylab), FadeIn(xlab), run_time=0.9)
        dot = Dot(sk.P(0, 0), color=TEAL, radius=0.15)
        self.at("moving curve")
        self.play(FadeIn(dot, scale=2.0), run_time=0.5)

        # pulses, then cleared: trace the curve with the dot riding its tip
        tt = ValueTracker(0.0)
        curve = always_redraw(lambda: sk.curve(tt.get_value()))
        rider = always_redraw(lambda: Dot(sk.P(tt.get_value(), level(tt.get_value())), color=TEAL, radius=0.15))
        self.remove(dot)
        self.at("Hormones are released")
        self.add(curve, rider)
        self.play(tt.animate.set_value(sk.tmax), run_time=4.4, rate_func=linear)
        full = sk.curve()
        self.remove(curve, rider)
        self.add(full)

        # the half-life of growth hormone: 27 min, an average
        self.at("average")
        p_pk, p_h = sk.P(48, 1.0), sk.P(75, 1.0)
        mark = VGroup(DashedLine(p_pk, p_h, color=GREY, stroke_width=3, dash_length=0.12),
                      DashedLine(p_h, sk.P(75, 0.5), color=GREY, stroke_width=3, dash_length=0.12),
                      Dot(p_pk, color=TEAL, radius=0.1), Dot(sk.P(75, 0.5), color=TEAL, radius=0.1))
        t27 = T("27 min", 24, TEXT).move_to(p_pk + [1.0, 0.3, 0])
        half = T("half", 22, GREY).move_to(sk.P(75, 0.75) + [0.5, 0, 0])
        call = T("growth hormone: average half-life 27 min", 28, TEXT).move_to([0, 3.15, 0])
        self.play(FadeIn(call, shift=DOWN * 0.1), Create(mark), FadeIn(t27), FadeIn(half), run_time=0.9)
        self.at("one small")
        note = T("one small study: 1962, five people, large intravenous dose", 24, GREY).move_to([0, 2.65, 0])
        self.play(FadeIn(note, shift=DOWN * 0.1), run_time=0.6)

        # a sample just before a pulse reads low; one on its peak reads high
        self.at("just before")
        self.play(FadeOut(VGroup(mark, t27, half, call, note)), run_time=0.4)
        da = Dot(sk.P(165, level(165)), color=TEAL, radius=0.17)
        la = T("sample just before a pulse", 24, TEAL).move_to([-2.1, -3.2, 0])
        ca = Line(da.get_center() + [0.0, -0.17, 0], la.get_top() + [0.5, 0.05, 0], color=TEAL, stroke_width=2)
        self.play(FadeIn(da, scale=2.2), FadeIn(la), Create(ca), run_time=0.6)
        self.at("many times lower")
        la2 = T("sample just before a pulse: reads low", 24, TEAL).move_to([-2.1, -3.2, 0])
        self.play(Transform(la, la2), run_time=0.4)
        self.at("on its peak")
        db = Dot(sk.P(183, level(183)), color=TEAL, radius=0.17)
        lb = T("sample on the peak: reads high", 24, TEAL).move_to(sk.P(183, level(183)) + [0.45, 0.1, 0], aligned_edge=LEFT)
        self.play(FadeIn(db, scale=2.2), FadeIn(lb), run_time=0.6)
        self.finish()


# ---------------------------------------------------------------------------------------------
class S02Axis(SpokenScene):
    """two hormones -> the cortisol axis in the lesson's order -> trophic and target -> long-loop feedback."""

    def construct(self):
        ax = Ax()
        gc, gk = Gauge(2.35, YELLOW, "ACTH"), Gauge(4.7, ORANGE, "cortisol")
        # the two readings, side by side, centred; they slide to their places as the axis appears
        g = VGroup(gc.group(), gk.group())
        V = np.array([-2.1, 2.2, 0])
        g.shift(V)
        self.play(FadeIn(g, shift=UP * 0.2), run_time=0.7)
        self.at("Take the cortisol axis")
        self.play(g.animate.shift(-V), *[FadeIn(b) for b in ax.b], run_time=0.9)

        # CRH drives ACTH
        self.at("vasopressin")
        self.play(FadeIn(ax.c1, shift=DOWN * 0.1), ax.b[0].rect.animate.set_stroke(PURPLE), run_time=0.5)
        self.at("drives")
        self.play(GrowArrow(ax.a1), run_time=0.5)
        self.at("from the")
        self.play(FadeIn(ax.c2, shift=DOWN * 0.1), run_time=0.4)
        self.at("pituitary")
        self.play(ax.b[1].rect.animate.set_stroke(YELLOW), run_time=0.4)
        # ACTH drives the adrenal cortex to make cortisol
        self.at("drives the adrenal")
        self.play(GrowArrow(ax.a2), run_time=0.6)
        self.at("to make cortisol")
        self.play(ax.b[2].rect.animate.set_stroke(ORANGE), Indicate(gk.name, color=ORANGE, scale_factor=1.2), run_time=0.8)

        # trophic and target
        self.at("Call")
        tag1 = bchip("trophic hormone: ACTH", YELLOW, 28)
        tag2 = bchip("target hormone: cortisol", ORANGE, 28)
        tags = VGroup(tag1, tag2).arrange(DOWN, buff=0.35, aligned_edge=LEFT).move_to([PANEL_L, -1.6, 0], aligned_edge=LEFT)
        self.play(FadeIn(tag1, shift=RIGHT * 0.2), Indicate(gc.name, color=YELLOW, scale_factor=1.2), run_time=0.7)
        self.at("cortisol the target")
        self.play(FadeIn(tag2, shift=RIGHT * 0.2), Indicate(gk.name, color=ORANGE, scale_factor=1.2), run_time=0.7)

        # long-loop feedback on CRH and ACTH
        self.at("feeds back")
        self.play(Create(ax.v1), run_time=0.2)
        self.play(Create(ax.h), run_time=0.5)
        self.at("on")
        self.play(Create(ax.d2), run_time=0.5)
        self.at("that")
        self.play(Create(ax.d1), run_time=0.5)
        self.at("long loop")
        self.play(FadeIn(ax.fbl), run_time=0.5)
        self.at("strong evidence")
        self.play(FadeIn(ax.strong, shift=DOWN * 0.1), run_time=0.5)
        self.finish()


# ---------------------------------------------------------------------------------------------
def conditions():
    lines = ["made-up example, bars not to scale", "08:00 blood draw", "normal sleep-wake schedule",
             "no glucocorticoid", "normal cortisol-binding globulin"]
    ts = VGroup(*[T(s, 24, GREY).move_to([PANEL_L, -1.25 - 0.47 * i, 0], aligned_edge=LEFT) for i, s in enumerate(lines)])
    return ts


def person(name):
    return T(name, 36, TEXT, weight=BOLD).move_to([PANEL_L, -0.45, 0], aligned_edge=LEFT)


class S03Primary(SpokenScene):
    """break the chain at the gland: person A, low cortisol 3, high ACTH 300 -> primary."""

    def construct(self):
        ax = Ax()
        gc, gk = Gauge(2.35, YELLOW, "ACTH"), Gauge(4.7, ORANGE, "cortisol")
        tag1 = bchip("trophic hormone: ACTH", YELLOW, 28)
        tag2 = bchip("target hormone: cortisol", ORANGE, 28)
        tags = VGroup(tag1, tag2).arrange(DOWN, buff=0.35, aligned_edge=LEFT).move_to([PANEL_L, -1.6, 0], aligned_edge=LEFT)
        ax.b[0].rect.set_stroke(PURPLE); ax.b[1].rect.set_stroke(YELLOW); ax.b[2].rect.set_stroke(ORANGE)
        self.add(ax.all(strong=True), gc.group(), gk.group(), tags)

        self.play(FadeOut(tags), FadeOut(ax.strong), run_time=0.6)
        # the break at the gland
        self.at("gland")
        x = cross(ax.b[2])
        self.play(ax.b[2].rect.animate.set_stroke(RED), Create(x), run_time=0.7)

        # conditions
        self.at("made up")
        cond = conditions()
        self.play(FadeIn(cond[0], shift=RIGHT * 0.15), run_time=0.4)
        self.at("normal sleep")
        self.play(LaggedStart(*[FadeIn(c, shift=RIGHT * 0.15) for c in cond[2:]], lag_ratio=0.35), run_time=1.4)
        self.at("in the morning")
        self.play(FadeIn(cond[1], shift=RIGHT * 0.15), run_time=0.4)
        self.at("Person A")
        pa = person("Person A")
        self.play(FadeIn(pa, shift=RIGHT * 0.15), run_time=0.4)
        self.at("cortisol of")
        self.play(*gk.anim(0.45, "3 µg/dL"), run_time=0.9)
        self.at("picograms")
        self.play(*gc.anim(BARH, "300 pg/mL"), run_time=1.1)

        # low cortisol should make an intact pituitary drive hard
        self.at("Low cortisol")
        self.play(FadeOut(cond), Indicate(gk.fill, color=ORANGE), run_time=0.7)
        self.at("intact pituitary")
        self.play(ax.b[1].rect.animate.set_stroke(GREEN), run_time=0.5)
        self.at("drive hard")
        a2t = arr([1.55, Y0, 0], [3.15, Y0, 0], YELLOW, w=14, tip=0.34)
        self.play(ReplacementTransform(ax.a2, a2t), run_time=0.5)
        self.at("it does")
        self.play(Indicate(gc.fill, color=YELLOW, scale_factor=1.12), run_time=0.7)
        self.at("The adrenal does not answer")
        self.play(Indicate(x, color=RED, scale_factor=1.15), run_time=0.9)
        self.at("the primary")
        verdict = bchip("primary: the gland fails", RED, 30).move_to([PANEL_L, -1.3, 0], aligned_edge=LEFT)
        self.play(FadeIn(verdict, shift=RIGHT * 0.2), run_time=0.6)
        self.at("Reference intervals")
        ref = VGroup(T("reference intervals differ", 24, GREY), T("by laboratory and assay", 24, GREY)).arrange(DOWN, buff=0.12, aligned_edge=LEFT)
        ref.move_to([PANEL_L, -2.5, 0], aligned_edge=UL)
        self.play(FadeIn(ref, shift=RIGHT * 0.15), run_time=0.6)
        self.finish()


# ---------------------------------------------------------------------------------------------
class S04Central(SpokenScene):
    """person B: same low cortisol, low ACTH -> the drive is missing -> secondary or tertiary, the pair cannot say which."""

    def construct(self):
        ax = Ax()
        gc, gk = Gauge(2.35, YELLOW, "ACTH"), Gauge(4.7, ORANGE, "cortisol")
        ax.b[0].rect.set_stroke(PURPLE); ax.b[1].rect.set_stroke(GREEN); ax.b[2].rect.set_stroke(RED)
        a2t = arr([1.55, Y0, 0], [3.15, Y0, 0], YELLOW, w=14, tip=0.34)
        x = cross(ax.b[2])
        gk.set(0.45, "3 µg/dL"); gc.set(BARH, "300 pg/mL")
        pa = person("Person A")
        verdict = bchip("primary: the gland fails", RED, 30).move_to([PANEL_L, -1.3, 0], aligned_edge=LEFT)
        ref = VGroup(T("reference intervals differ", 24, GREY), T("by laboratory and assay", 24, GREY)).arrange(DOWN, buff=0.12, aligned_edge=LEFT)
        ref.move_to([PANEL_L, -2.5, 0], aligned_edge=UL)
        ax_all = ax.all()
        ax_all.remove(ax.a2)
        self.add(ax_all, a2t, gc.group(), gk.group(), gk.val, gc.val, x, pa, verdict, ref)

        # clear person A, bring in person B (same cortisol, ACTH not yet shown)
        pb = person("Person B")
        a2n = arr([1.55, Y0, 0], [3.15, Y0, 0], YELLOW)
        self.play(FadeOut(VGroup(x, verdict, ref)), ReplacementTransform(pa, pb), ReplacementTransform(a2t, a2n),
                  ax.b[2].rect.animate.set_stroke(ORANGE), ax.b[1].rect.animate.set_stroke(YELLOW),
                  *gc.anim(0.02), run_time=0.8)
        self.at("but")
        self.play(*gc.anim(0.45, "5 pg/mL"), run_time=1.0)
        self.at("The drive itself")
        a2d = a2n.copy().set_opacity(0.25)
        self.play(Transform(a2n, a2d), run_time=0.6)
        # the pituitary or the hypothalamus?
        self.at("points to the pituitary")
        bp = badge("?", RED, -0.8)
        bh = badge("?", RED, -5.5)
        self.play(ax.b[1].rect.animate.set_stroke(RED), FadeIn(bp, scale=1.5), run_time=0.5)
        self.at("a secondary")
        c1 = bchip("secondary: pituitary", RED, 28).move_to([PANEL_L, -1.3, 0], aligned_edge=LEFT)
        self.play(FadeIn(c1, shift=RIGHT * 0.2), run_time=0.5)
        self.at("the hypothalamus")
        self.play(ax.b[0].rect.animate.set_stroke(RED), FadeIn(bh, scale=1.5), run_time=0.5)
        self.at("a tertiary")
        c2 = bchip("tertiary: hypothalamus", RED, 28).move_to([PANEL_L, -2.2, 0], aligned_edge=LEFT)
        self.play(FadeIn(c2, shift=RIGHT * 0.2), run_time=0.5)
        self.at("cannot say")
        br = Brace(VGroup(c1, c2), RIGHT, color=RED)
        which = T("which?", 32, RED, weight=BOLD).next_to(br, RIGHT, buff=0.2)
        self.play(GrowFromCenter(br), FadeIn(which), Indicate(VGroup(bp, bh), color=RED, scale_factor=1.25), run_time=0.9)
        self.at("either lesion")
        self.play(Indicate(VGroup(gc.frame, gc.fill, gc.val), color=YELLOW, scale_factor=1.1), run_time=0.9)
        self.at("gland disease")
        l1 = T("gland disease: primary", 28, TEXT)
        l2 = T("central disease: secondary or tertiary", 28, TEXT)
        lines = VGroup(l1, l2).arrange(DOWN, buff=0.35, aligned_edge=LEFT).move_to([PANEL_L, -1.5, 0], aligned_edge=UL)
        self.play(FadeOut(VGroup(c1, c2, br, which)), FadeIn(l1, shift=RIGHT * 0.2), run_time=0.7)
        self.at("central disease")
        self.play(FadeIn(l2, shift=RIGHT * 0.2), run_time=0.7)
        self.finish()


# ---------------------------------------------------------------------------------------------
class S05Stim(SpokenScene):
    """stimulation test: synthetic ACTH, cortisol 16 after 30 min; adequate depends on the assay; a normal answer does not clear the upstream."""

    def construct(self):
        ax = Ax()
        gc, gk = Gauge(2.35, YELLOW, "ACTH"), Gauge(4.7, ORANGE, "cortisol")
        ax.b[0].rect.set_stroke(RED); ax.b[1].rect.set_stroke(RED); ax.b[2].rect.set_stroke(ORANGE)
        a2d = arr([1.55, Y0, 0], [3.15, Y0, 0], YELLOW).set_opacity(0.25)
        gk.set(0.45, "3 µg/dL"); gc.set(0.45, "5 pg/mL")
        pb = person("Person B")
        bp, bh = badge("?", RED, -0.8), badge("?", RED, -5.5)
        l1 = T("gland disease: primary", 28, TEXT)
        l2 = T("central disease: secondary or tertiary", 28, TEXT)
        lines = VGroup(l1, l2).arrange(DOWN, buff=0.35, aligned_edge=LEFT).move_to([PANEL_L, -1.5, 0], aligned_edge=UL)
        ax_all = ax.all()
        ax_all.remove(ax.a2)
        self.add(ax_all, a2d, gc.group(), gk.group(), gk.val, gc.val, bp, bh, pb, lines)

        # reset: the previous answer goes, the test begins
        self.play(FadeOut(VGroup(lines, bp, bh, gc.group(), gc.val)),
                  ax.b[0].rect.animate.set_stroke(PURPLE), ax.b[1].rect.animate.set_stroke(YELLOW), run_time=0.7)
        self.at("B receives")
        syn = bchip("synthetic ACTH", YELLOW, 26).move_to([1.9, -1.5, 0])
        sarr = arr([2.5, -0.95, 0], [3.65, 0.22, 0], YELLOW, w=6)
        self.at("synthetic")
        self.play(FadeIn(syn, shift=UP * 0.2), GrowArrow(sarr), run_time=0.8)
        self.at("minutes later")
        clock = T("30 min later", 26, TEXT).move_to([1.9, -2.5, 0])
        self.play(FadeIn(clock), *gk.anim(BARH, "16 µg/dL"), run_time=1.5)
        self.at("Whether that is adequate")
        q = bchip("adequate? depends on the assay", TEAL, 28).move_to([PANEL_L, -1.35, 0], aligned_edge=LEFT)
        self.play(FadeIn(q, shift=RIGHT * 0.2), run_time=0.6)
        self.at("criteria for newer")
        hist = bchip("historical criterion", GREY, 26).move_to([PANEL_L, -2.2, 0], aligned_edge=LEFT)
        newer = bchip("newer, more specific assays", TEAL, 26).move_to([PANEL_L, -3.05, 0], aligned_edge=LEFT)
        self.play(FadeIn(hist, shift=RIGHT * 0.2), run_time=0.5)
        self.at("sit below")
        self.play(FadeIn(newer, shift=DOWN * 0.2), run_time=0.6)

        self.at("An adequate response")
        self.play(FadeOut(VGroup(q, hist, newer, clock)), run_time=0.5)
        ok = bchip("the adrenal can answer ACTH", GREEN, 28).move_to([PANEL_L, -1.35, 0], aligned_edge=LEFT)
        self.play(FadeIn(ok, shift=RIGHT * 0.2), ax.b[2].rect.animate.set_stroke(GREEN), run_time=0.7)
        self.at("After a recent loss")
        loss = bchip("recent loss of central drive", RED, 28).move_to([PANEL_L, -2.2, 0], aligned_edge=LEFT)
        bp2, bh2 = badge("?", RED, -0.8), badge("?", RED, -5.5)
        self.play(FadeIn(loss, shift=RIGHT * 0.2), FadeIn(bp2, scale=1.5), FadeIn(bh2, scale=1.5),
                  ax.b[0].rect.animate.set_stroke(RED), ax.b[1].rect.animate.set_stroke(RED), run_time=0.7)
        self.at("may not yet")
        atr = bchip("adrenal may not yet be atrophied", GREEN, 28).move_to([PANEL_L, -3.05, 0], aligned_edge=LEFT)
        self.play(FadeIn(atr, shift=RIGHT * 0.2), run_time=0.6)
        self.at("does not exclude")
        self.play(Indicate(VGroup(bp2, bh2), color=RED, scale_factor=1.3), run_time=1.0)
        self.finish()


# ---------------------------------------------------------------------------------------------
class S06Rule(SpokenScene):
    """the thyroid reads the same way -> the rule: a point on a moving curve, a criterion belongs to its assay, read pairs."""

    def construct(self):
        ax = Ax(tgt="Thyroid", rel_chip=False, feedback=False)
        ax.c2 = bchip("TSH", YELLOW, 24).move_to([2.35, Y0 + 0.62, 0])
        ax.b[0].rect.set_stroke(GREY); ax.b[1].rect.set_stroke(YELLOW); ax.b[2].rect.set_stroke(ORANGE)
        gc, gk = Gauge(2.35, YELLOW, "TSH"), Gauge(4.7, ORANGE, "free T4")
        self.play(FadeIn(VGroup(ax.all(), gc.group(), gk.group())), run_time=0.5)

        # primary pattern: high TSH, low free T4
        self.at("High")
        self.play(*gc.anim(BARH, "high"), run_time=0.8)
        self.at("low free")
        self.play(*gk.anim(0.45, "low"), run_time=0.8)
        x = cross(ax.b[2])
        self.at("primary pattern")
        pr = bchip("primary pattern", RED, 30).move_to([PANEL_L, -1.3, 0], aligned_edge=LEFT)
        self.play(ax.b[2].rect.animate.set_stroke(RED), Create(x), FadeIn(pr, shift=RIGHT * 0.2), run_time=0.8)

        # reset, then the central pattern
        self.at("low free", nth=1)
        self.play(FadeOut(VGroup(x, pr)), ax.b[2].rect.animate.set_stroke(ORANGE), *gc.anim(0.02), run_time=0.4)
        self.at("low or")
        self.play(*gc.anim(0.45, "low"), run_time=0.5)
        self.at("inappropriately normal")
        mid = DashedLine([1.0, BASE + 1.15, 0], [2.75, BASE + 1.15, 0], color=YELLOW, stroke_width=4, dash_length=0.1)
        alt = VGroup(T("or inappropriately", 22, YELLOW), T("normal", 22, YELLOW)).arrange(DOWN, buff=0.08, aligned_edge=RIGHT)
        alt.move_to([0.95, BASE + 1.15, 0], aligned_edge=RIGHT)
        self.play(Create(mid), FadeIn(alt), run_time=0.8)
        self.at("central disease")
        self.play(ax.b[0].rect.animate.set_stroke(RED), ax.b[1].rect.animate.set_stroke(RED),
                  FadeIn(bchip("central disease", RED, 30).move_to([PANEL_L, -1.3, 0], aligned_edge=LEFT), shift=RIGHT * 0.2),
                  run_time=0.8)

        # the rule
        self.at("A hormone level")
        old = Group(*[m for m in self.mobjects])
        self.play(FadeOut(old), run_time=0.4)
        sk = Sketch(-6.2, 0.35, 0.0155, 2.5, tmax=418)
        axes = sk.axes(top_v=1.2)
        curve = sk.curve(w=4)
        dot = Dot(sk.P(183, level(183)), color=TEAL, radius=0.15)
        cap = T("a point on a moving curve", 32, TEXT).move_to([-2.9, -0.25, 0])
        self.play(Create(axes), Create(curve), run_time=0.8)
        self.at("point on")
        self.play(FadeIn(dot, scale=2.2), FadeIn(cap), run_time=0.6)
        self.at("criterion")
        c_crit = bchip("criterion", GREY, 34).move_to([4.0, 2.6, 0])
        belongs = T("belongs to", 28, GREY).move_to([4.0, 1.8, 0])
        c_assay = bchip("assay", TEAL, 34).move_to([4.0, 1.0, 0])
        self.play(FadeIn(c_crit, shift=DOWN * 0.1), run_time=0.5)
        self.at("belongs to its")
        self.play(FadeIn(belongs), FadeIn(c_assay, shift=UP * 0.1), run_time=0.6)
        self.at("Read hormones")
        c_tro = bchip("trophic hormone", YELLOW, 26)
        c_tgt = bchip("target hormone", ORANGE, 26)
        pair = VGroup(c_tro, c_tgt).arrange(RIGHT, buff=0.5).move_to([-2.9, -1.75, 0])
        self.play(FadeIn(c_tro, shift=UP * 0.1), FadeIn(c_tgt, shift=UP * 0.1), run_time=0.6)
        self.at("as pairs")
        pl = Line(c_tro.get_right(), c_tgt.get_left(), color=TEXT, stroke_width=4)
        br = Brace(pair, DOWN, color=TEXT)
        pt = T("a pair", 30, TEXT).next_to(br, DOWN, buff=0.12)
        self.play(Create(pl), GrowFromCenter(br), FadeIn(pt), run_time=0.7)
        self.at("know which assay")
        num = bchip("the number", TEXT, 34).move_to([4.0, -1.0, 0])
        na = arr([4.0, 0.6, 0], [4.0, -0.55, 0], TEAL, w=6)
        self.play(GrowArrow(na), FadeIn(num, shift=UP * 0.1), run_time=0.7)
        self.finish()


class S07End(EndCard):
    LINE = "Read hormones as pairs, and know which assay made the number."
