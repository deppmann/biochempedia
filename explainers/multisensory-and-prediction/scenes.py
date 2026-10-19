"""Senses are weighted by their reliability  (Biochemistrypedia explainer)

Timed to the SPOKEN words: every self.at("...") cue waits for that phrase in audio/words.json.
All numbers are the lesson's worked example (vision 50 mm, touch 54 mm, SD 2 / 4 / 8 mm).
All curves are model curves computed from those numbers: "in this sketch".

COLOR MAP (one color per concept, whole video)
  BLUE   = vision (the visual cue, the visual stimulus)
  ORANGE = touch (the touch cue)
  GREEN  = the combined estimate (the weighted average)
  TEAL   = precision (one over variance)
  PURPLE = sound
  YELLOW = the answer being asked for / the perceived location
  RED    = what is not shown
  GREY   = axes, scope chips, de-emphasized
"""
import numpy as np
from bp_style import *  # noqa: F401,F403

ORANGE = "#F29E4C"
PURPLE = "#B58CD9"

# ---------------------------------------------------------------------------------------------
# the one stage: bar height in mm on a horizontal axis, curves above it
# ---------------------------------------------------------------------------------------------
BASE = -2.2          # y of the axis
SC = 15.0            # curve height per unit of probability density
X0, X1 = 38.0, 66.0  # mm shown
WX = 11.6            # screen width of that range
MV, MH, SH = 50.0, 54.0, 4.0   # vision says 50, touch says 54, touch SD 4 (lesson)
TOP = 1.25           # top of the marker lines (just under the weight bar)


def xp(h):
    return (h - 52.0) * WX / (X1 - X0)


def gauss(h, mu, s):
    return np.exp(-0.5 * ((h - mu) / s) ** 2) / (s * np.sqrt(2 * np.pi))


def comb(sv, sh=SH):
    pv, ph = 1.0 / sv ** 2, 1.0 / sh ** 2
    wv = pv / (pv + ph)
    return wv, wv * MV + (1 - wv) * MH, float(np.sqrt(1.0 / (pv + ph)))


def gcurve(mu, s, color, fo=0.2):
    hs = np.linspace(X0, X1, 141)
    pts = [np.array([xp(h), BASE + SC * gauss(h, mu, s), 0.0]) for h in hs]
    line = VMobject(stroke_color=color, stroke_width=5, fill_opacity=0)
    line.set_points_smoothly(pts)
    fill = VMobject(stroke_width=0, fill_color=color, fill_opacity=fo)
    fill.set_points_as_corners(pts + [np.array([xp(X1), BASE, 0.0]), np.array([xp(X0), BASE, 0.0])])
    return VGroup(fill, line)


def axis():
    g = VGroup(Line([xp(X0), BASE, 0], [xp(X1), BASE, 0], color=GREY, stroke_width=3))
    for h in range(40, 65, 4):
        g.add(Line([xp(h), BASE, 0], [xp(h), BASE - 0.12, 0], color=GREY, stroke_width=3))
        g.add(M(str(h), 22, GREY).move_to([xp(h), BASE - 0.42, 0]))
    g.add(T("bar height (mm)   ·   curves: model, in this sketch", 22, GREY).move_to([0, BASE - 1.0, 0]))
    return g


def vline(h, color, top=TOP, dashed=False):
    cls = DashedLine if dashed else Line
    return cls([xp(h), BASE, 0], [xp(h), top, 0], color=color, stroke_width=5)


def row(name, color, detail, y):
    dot = Circle(radius=0.12, stroke_width=0, fill_color=color, fill_opacity=1)
    nm = T(name, 26, color, weight=BOLD)
    parts = [dot, nm]
    if detail:
        parts.append(T(detail, 22, TEXT))
    g = VGroup(*parts).arrange(RIGHT, buff=0.18)
    return g.move_to([-6.2 + g.width / 2, y, 0])


Y1, Y2, Y3 = 3.2, 2.7, 2.2


def wbar(wv, y=1.55, W=9.4, x0=-5.0):
    h = 0.55
    a = Rectangle(width=W * wv, height=h, stroke_width=0, fill_color=BLUE, fill_opacity=0.55)
    b = Rectangle(width=W * (1 - wv), height=h, stroke_width=0, fill_color=ORANGE, fill_opacity=0.55)
    a.move_to([x0 + W * wv / 2, y, 0])
    b.move_to([x0 + W * wv + W * (1 - wv) / 2, y, 0])
    # numbers only at the lesson's two weightings (0.8 / 0.2); names only while the bar moves
    exact = min(abs(wv - 0.8), abs(wv - 0.2)) < 0.005
    la = T(f"vision {wv:.1f}" if exact else "vision", 22, TEXT).move_to(a)
    lb = T(f"touch {1 - wv:.1f}" if exact else "touch", 22, TEXT).move_to(b)
    return VGroup(a, b, la, lb)


def wtag(y=1.55, x=5.5):
    return T("weights", 22, GREY).move_to([x, y, 0])


def names():
    nv = T("vision", 26, BLUE, weight=BOLD).move_to([xp(50) - 1.15, BASE + 2.9, 0])
    nt = T("touch", 26, ORANGE, weight=BOLD).move_to([xp(58.2), BASE + 1.8, 0])
    return nv, nt


class S00Title(TitleCard):
    LESSON = "Combining senses and predicting them"
    TITLE = "Senses Are Weighted By Their Reliability"


# ---------------------------------------------------------------------------------------------
class S01Question(SpokenScene):
    """Two cues disagree; a yellow question mark slides between them."""

    def construct(self):
        head = T("Judging the height of one bar", 34, font=TITLE_FONT).to_edge(UP, buff=0.5)
        ax = axis()
        self.play(FadeIn(head), FadeIn(ax), run_time=0.8)
        mv, mt = vline(50, BLUE, 1.6), vline(54, ORANGE, 1.6)
        lv = T("vision says 50 mm", 28, BLUE)
        lv.move_to([xp(50) + 0.12 - lv.width / 2, 1.95, 0])
        lt = T("touch says 54 mm", 28, ORANGE)
        lt.move_to([xp(54) - 0.12 + lt.width / 2, 1.95, 0])
        self.at("Your eyes say")
        self.play(Create(mv), FadeIn(lv, shift=DOWN * 0.15), run_time=0.8)
        self.at("Your hand says")
        self.play(Create(mt), FadeIn(lt, shift=DOWN * 0.15), run_time=0.8)
        dash = DashedLine([0, BASE, 0], [0, 1.6, 0], color=YELLOW, stroke_width=5)
        q = T("?", 64, YELLOW, weight=BOLD).move_to([0, 2.45, 0])
        mid = VGroup(dash, q)
        self.at("how much to trust")
        self.play(FadeIn(mid, shift=UP * 0.2), run_time=0.6)
        self.play(mid.animate.shift(LEFT * 0.55), run_time=0.6)
        self.play(mid.animate.shift(RIGHT * 1.1), run_time=0.9)
        self.at("Which one do you")
        self.play(mid.animate.shift(LEFT * 0.55), Indicate(q, color=YELLOW, scale_factor=1.25), run_time=0.9)
        self.finish()


# ---------------------------------------------------------------------------------------------
class S02Rule(SpokenScene):
    """Markers grow into noisy curves; the weighting rule is built line by line."""

    def construct(self):
        ax = axis()
        mv, mt = vline(50, BLUE, 1.6), vline(54, ORANGE, 1.6)
        self.add(ax, mv, mt)
        cv, ct = gcurve(MV, 2.0, BLUE, 0.22), gcurve(MH, SH, ORANGE, 0.22)
        nv, nt = names()
        self.at("Each sense gives")
        self.play(FadeOut(mv), FadeOut(mt), GrowFromEdge(cv, DOWN), GrowFromEdge(ct, DOWN), run_time=1.2)
        self.play(FadeIn(nv), FadeIn(nt), run_time=0.5)
        self.at("independent and Gaussian")
        self.play(Indicate(cv[1], color=BLUE, scale_factor=1.0), Indicate(ct[1], color=ORANGE, scale_factor=1.0), run_time=1.0)
        l1 = T("best combination = weighted average", 32, GREEN, weight=BOLD).move_to([0, 3.15, 0])
        self.at("weighted average")
        self.play(Write(l1), run_time=1.2)
        l2 = T("precision = 1 / variance", 30, TEAL).move_to([0, 2.5, 0])
        self.at("over its variance")
        self.play(FadeIn(l2, shift=UP * 0.15), run_time=0.6)
        l3 = T("weight = precision ÷ sum of precisions", 30, TEXT).move_to([0, 1.85, 0])
        self.at("sum of the precisions")
        self.play(FadeIn(l3, shift=UP * 0.15), run_time=0.7)
        self.finish()


# ---------------------------------------------------------------------------------------------
class S03Numbers(SpokenScene):
    """SD 2 and 4, variances 4 and 16, weights 0.8 and 0.2, combined estimate 50.8."""

    def construct(self):
        ax = axis()
        cv, ct = gcurve(MV, 2.0, BLUE, 0.22), gcurve(MH, SH, ORANGE, 0.22)
        nv, nt = names()
        self.add(ax, cv, ct, nv, nt)
        r1 = row("vision", BLUE, "SD 2 mm", Y1)
        r2 = row("touch", ORANGE, "SD 4 mm", Y2)
        self.at("Take vision")
        self.play(FadeOut(nv), FadeIn(r1), run_time=0.6)
        self.at("and touch")
        self.play(FadeOut(nt), FadeIn(r2), run_time=0.6)
        r1b = row("vision", BLUE, "SD 2 mm   variance 4 mm²", Y1)
        r2b = row("touch", ORANGE, "SD 4 mm   variance 16 mm²", Y2)
        self.at("Their variances")
        self.play(Transform(r1, r1b), Transform(r2, r2b), run_time=0.8)
        bar = wbar(0.8)
        tag = wtag()
        self.at("The weights come")
        self.play(GrowFromEdge(bar[0], LEFT), GrowFromEdge(bar[1], LEFT), FadeIn(bar[2]), FadeIn(bar[3]), FadeIn(tag), run_time=1.0)
        mk = vline(50, GREEN)
        mk.set_stroke(width=6)
        r3 = row("combined", GREEN, "estimate 50.8 mm", Y3)
        self.at("combined estimate")
        self.play(Create(mk), FadeIn(r3), run_time=0.6)
        self.play(mk.animate.shift(RIGHT * (xp(50.8) - xp(50))), run_time=1.0)
        self.at("nearer to vision")
        self.play(Indicate(bar[0], color=BLUE, scale_factor=1.04), run_time=0.9)
        self.finish()


# ---------------------------------------------------------------------------------------------
def state_after_s03(scene):
    ax = axis()
    cv, ct = gcurve(MV, 2.0, BLUE, 0.22), gcurve(MH, SH, ORANGE, 0.22)
    r1 = row("vision", BLUE, "SD 2 mm   variance 4 mm²", Y1)
    r2 = row("touch", ORANGE, "SD 4 mm   variance 16 mm²", Y2)
    bar, tag = wbar(0.8), wtag()
    mk = vline(50.8, GREEN)
    mk.set_stroke(width=6)
    r3 = row("combined", GREEN, "estimate 50.8 mm", Y3)
    scene.add(ax, cv, ct, r1, r2, bar, tag, mk, r3)
    return ax, cv, ct, r1, r2, bar, tag, mk, r3


class S04Narrower(SpokenScene):
    """The combined curve is narrower than either cue."""

    def construct(self):
        ax, cv, ct, r1, r2, bar, tag, mk, r3 = state_after_s03(self)
        cc = gcurve(50.8, 1.789, GREEN, 0.25)
        r3a = row("combined", GREEN, "estimate 50.8 mm   variance 3.2 mm²", Y3)
        self.at("The combined variance")
        self.play(Transform(r3, r3a), GrowFromEdge(cc, DOWN), run_time=1.3)
        r3b = row("combined", GREEN, "50.8 mm   variance 3.2 mm²   SD 1.789 mm", Y3)
        self.at("The standard deviation")
        self.play(Transform(r3, r3b), Indicate(cc[1], color=GREEN, scale_factor=1.0), run_time=1.0)
        cmp_ = M("SD: 1.789 < 2 < 4 mm", 26, GREEN).move_to([3.4, 2.7, 0])
        self.at("lower than either")
        self.play(Write(cmp_), run_time=1.2)
        self.at("weaker cue")
        self.play(Indicate(ct[1], color=ORANGE, scale_factor=1.0), Indicate(bar[3], color=ORANGE, scale_factor=1.15), run_time=1.2)
        self.at("second independent cue")
        self.play(Indicate(cc[1], color=GREEN, scale_factor=1.0), run_time=1.0)
        self.finish()


# ---------------------------------------------------------------------------------------------
class S05Blur(SpokenScene):
    """Blur the picture: vision SD 2 -> 8, the weights swap, the estimate moves to 53.2."""

    def construct(self):
        sv = ValueTracker(2.0)
        ax = axis()
        ct = gcurve(MH, SH, ORANGE, 0.22)
        cv = always_redraw(lambda: gcurve(MV, sv.get_value(), BLUE, 0.22))
        cc = always_redraw(lambda: gcurve(comb(sv.get_value())[1], comb(sv.get_value())[2], GREEN, 0.25))
        bar = always_redraw(lambda: wbar(comb(sv.get_value())[0]))
        mk = always_redraw(lambda: vline(comb(sv.get_value())[1], GREEN).set_stroke(width=6))
        tag = wtag()
        r1 = row("vision", BLUE, "SD 2 mm   variance 4 mm²", Y1)
        r2 = row("touch", ORANGE, "SD 4 mm   variance 16 mm²", Y2)
        r3 = row("combined", GREEN, "50.8 mm   variance 3.2 mm²   SD 1.789 mm", Y3)
        self.add(ax, ct, cv, cc, bar, mk, tag, r1, r2, r3)
        r1n, r3n = row("vision", BLUE, "", Y1), row("combined", GREEN, "", Y3)
        t0 = self.t_of("Now blur the picture")
        t1 = self.t_of("weights swap")
        self.at("Now blur the picture")
        self.play(Transform(r1, r1n), Transform(r3, r3n), run_time=0.5)
        self.play(sv.animate.set_value(8.0), run_time=max(1.5, t1 - t0 - 1.2), rate_func=smooth)
        r1c = row("vision", BLUE, "SD 8 mm   variance 64 mm²", Y1)
        self.play(Transform(r1, r1c), run_time=0.5)
        self.at("weights swap")
        self.play(Indicate(bar[0], color=BLUE, scale_factor=1.04), Indicate(bar[1], color=ORANGE, scale_factor=1.04), run_time=1.0)
        r3c = row("combined", GREEN, "53.2 mm   variance 12.8 mm²   SD 3.58 mm", Y3)
        self.at("The estimate moves")
        self.play(Transform(r3, r3c), run_time=0.7)
        self.at("same arithmetic")
        self.play(Indicate(bar[1], color=ORANGE, scale_factor=1.06), run_time=1.0)
        # --- Alais and Burr card -------------------------------------------------------------
        self.at("and Burr")
        cur = Group(*self.mobjects)
        self.play(FadeOut(cur), run_time=0.6)
        self.clear()
        head = T("Alais and Burr: sound and sight, human localization", 30, font=TITLE_FONT).move_to([0, 3.1, 0])
        yline = -0.5
        axl = Line([-5.8, yline, 0], [5.8, yline, 0], color=GREY, stroke_width=3)
        axt = T("location", 24, GREY).move_to([5.0, yline - 0.45, 0])
        band = VGroup(*[Rectangle(width=w, height=2.4, stroke_width=0, fill_color=BLUE, fill_opacity=o).move_to([-1.6, 0.7, 0])
                        for w, o in [(5.0, 0.10), (3.8, 0.12), (2.6, 0.16)]])
        bl = T("sight, severely blurred", 28, BLUE).move_to([-1.6, 2.3, 0])
        sd = Line([2.8, yline, 0], [2.8, 1.9, 0], color=PURPLE, stroke_width=6)
        sl = T("sound", 28, PURPLE, weight=BOLD).move_to([2.8, 2.3, 0])
        tri = Triangle(color=YELLOW, fill_color=YELLOW, fill_opacity=1, stroke_width=0).scale(0.22)
        tri.rotate(PI).move_to([-1.6, yline + 0.35, 0])
        pl = T("perceived location", 26, YELLOW)
        pl.next_to(tri, DOWN, buff=0.3)
        pl.move_to([pl.get_center()[0], yline - 1.05, 0])
        sch = T("schematic, not data", 24, GREY).move_to([0, -2.9, 0])
        self.play(Write(head), FadeIn(axl), FadeIn(axt), FadeIn(sch), run_time=0.9)
        self.play(FadeIn(band), FadeIn(bl), FadeIn(tri), FadeIn(pl), run_time=0.8)
        self.at("severely")
        self.play(Create(sd), FadeIn(sl), run_time=0.7)
        self.at("sound captured")
        # pulled most of the way toward sound, stopping short of the line: an illustration, not a measured shift
        self.play(tri.animate.move_to([2.1, yline + 0.35, 0]), pl.animate.move_to([2.1, yline - 1.05, 0]), run_time=1.2)
        self.finish()


# ---------------------------------------------------------------------------------------------
class S06Scope(SpokenScene):
    """What the model's test shows and does not show, and the rule."""

    def construct(self):
        obs = VGroup(*[Circle(radius=0.3, stroke_color=GREY, stroke_width=4, fill_color=GREY, fill_opacity=0.3) for _ in range(4)])
        obs.arrange(RIGHT, buff=0.35).move_to([-4.6, 2.2, 0])
        ol = T("4 human observers", 24, GREY).move_to([-4.6, 1.45, 0])
        head = T("Ernst and Banks", 34, font=TITLE_FONT).move_to([0, 3.3, 0])
        self.play(FadeIn(head), run_time=0.5)
        self.at("four human observers")
        self.play(LaggedStart(*[FadeIn(c, scale=0.6) for c in obs], lag_ratio=0.25), FadeIn(ol), run_time=1.4)
        cs = chip("by sight", BLUE, 26).move_to([-0.6, 2.35, 0])
        ct = chip("by touch", ORANGE, 26).move_to([-0.6, 1.3, 0])
        self.at("judged bar height")
        self.play(FadeIn(cs, shift=RIGHT * 0.2), FadeIn(ct, shift=RIGHT * 0.2), run_time=0.9)
        cn = chip("noise added to vision", BLUE, 26).move_to([3.9, 2.35, 0])
        ar = Arrow(cs.get_right(), cn.get_left(), buff=0.1, color=BLUE, stroke_width=5)
        self.at("noise was added")
        self.play(GrowArrow(ar), FadeIn(cn), run_time=0.8)
        cm = chip("maximum-likelihood model", GREEN, 26).move_to([-3.4, -0.2, 0])
        cj = chip("their judgements", GREY, 26).move_to([4.3, -0.2, 0])
        ra = Arrow([-0.6, -0.2, 0], [2.6, -0.2, 0], buff=0.0, color=GREEN, stroke_width=5)
        rs = T("closely resembled", 26, GREEN).move_to([1.0, 0.35, 0])
        self.at("A maximum likelihood")
        self.play(FadeIn(cm), run_time=0.5)
        self.at("closely resembled")
        self.play(GrowArrow(ra), FadeIn(rs), FadeIn(cj), run_time=0.8)
        s1 = chip("one task", GREY, 28)
        s2 = chip("four people", GREY, 28)
        s3 = chip("behavioural fit", GREY, 28)
        sc = VGroup(s1, s2, s3).arrange(RIGHT, buff=0.5).move_to([0, -1.5, 0])
        self.at("one task")
        self.play(FadeIn(s1, shift=UP * 0.15), run_time=0.4)
        self.at("four people")
        self.play(FadeIn(s2, shift=UP * 0.15), run_time=0.4)
        self.at("behavioral fit")
        self.play(FadeIn(s3, shift=UP * 0.15), run_time=0.4)
        br = chip("where in the brain?", RED, 30)
        brd = DashedVMobject(br[0], num_dashes=40).set_color(RED)
        nb = VGroup(br[1], brd).move_to([-1.5, -2.8, 0])
        ns = T("not shown", 28, RED, weight=BOLD).next_to(nb, RIGHT, buff=0.5)
        self.at("in the brain")
        self.play(FadeIn(nb, shift=UP * 0.15), run_time=0.5)
        self.play(FadeIn(ns), run_time=0.4)
        # --- the rule -------------------------------------------------------------------------
        self.at("Keep the rule")
        self.play(FadeOut(Group(*self.mobjects)), run_time=0.4)
        self.clear()
        b1 = wbar(0.8, y=1.2, W=8.0, x0=-4.0)
        b2 = wbar(0.2, y=-1.0, W=8.0, x0=-4.0)
        t1 = T("vision SD 2 mm", 26, BLUE).move_to([-4.0 + 1.4, 1.2 + 0.7, 0])
        t2 = T("vision SD 8 mm", 26, BLUE).move_to([-4.0 + 1.4, -1.0 + 0.7, 0])
        self.play(FadeIn(b1), FadeIn(t1), run_time=0.4)
        self.at("which sense wins")
        self.play(FadeIn(b2), FadeIn(t2), run_time=0.6)
        self.at("follows its reliability")
        self.play(Indicate(b1[0], color=BLUE, scale_factor=1.03), Indicate(b2[1], color=ORANGE, scale_factor=1.03), run_time=1.2)
        self.finish()


class S07End(EndCard):
    LINE = "Which sense wins follows its reliability in the task at hand."
