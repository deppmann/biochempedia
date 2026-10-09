# Same destination, faster arrival  (Enzyme action basics)
#
# COLOR MAP (one color per concept, kept for every scene):
#   YELLOW  substrate / reactants / the thing that moves      (also the "car" and the ball)
#   GREEN   product / destination / thermodynamics, DG        (the green light means "favorable")
#   RED     the uncatalyzed barrier / kinetics, DG-double-dagger (and the red light / "stop")
#   BLUE    the enzyme and everything catalyzed
#   PURPLE  the transition state
#   GOLD    binding energy
#   GREY    structure, axes, de-emphasized things
#   AMBER   only the amber lamp of the traffic light (equilibrium)
from bp_style import *
import json
import os
import numpy as np

PURPLE = "#B58CF0"
AMBER = "#F0A93B"


# ---------------------------------------------------------------- helpers
class Base(NarratedScene):
    """NarratedScene plus: until("some phrase") waits until the narration reaches that phrase."""

    def narr(self):
        if not hasattr(self, "_narr"):
            sid = os.environ.get("KX_SCENE_ID")
            sc = [s for s in json.load(open(os.environ["KX_SCRIPT"]))["scenes"] if s["id"] == sid][0]
            self._narr = sc.get("narration", "")
        return self._narr

    def at(self, phrase):
        n = self.narr()
        i = n.find(phrase)
        assert i >= 0, phrase
        return i / len(n)

    # Measured onset times (s) of key phrases, read off pauses in the actual narration audio
    # (ffmpeg silencedetect). They override the character-proportional estimate, which drifts
    # by up to ~1.5 s where the voice speeds up or pauses.
    CUES = {}

    def tm(self, phrase):
        if phrase in self.CUES:
            return self.CUES[phrase]
        return self.at(phrase) * self.narration_s

    def until(self, phrase, lead=0.25):
        rem = self.tm(phrase) - lead - self.elapsed()
        if rem > 0.02:
            self.wait(rem)

    def span(self, a, b=None):
        """Seconds between the narration positions of two phrases (b=None -> end of narration)."""
        tb = self.narration_s if b is None else self.tm(b)
        return tb - self.tm(a)


def smooth(s):
    return s * s * (3 - 2 * s)


def prof(s, h, dg):
    """Free-energy profile along the reaction coordinate: a step of dg plus a barrier of height ~h."""
    return dg * smooth(s) + h * np.exp(-((s - 0.43) / 0.16) ** 2)


class Curve:
    """A free-energy profile mapped into screen space."""

    def __init__(self, x0, x1, y0, h, dg):
        self.x0, self.x1, self.y0, self.h, self.dg = x0, x1, y0, h, dg

    def pt(self, s):
        return np.array([self.x0 + (self.x1 - self.x0) * s, self.y0 + prof(s, self.h, self.dg), 0.0])

    def mob(self, color, w=6):
        return ParametricFunction(lambda t: self.pt(t), t_range=[0, 1, 0.01], color=color, stroke_width=w)

    def peak_s(self):
        ss = np.linspace(0, 1, 2001)
        return ss[np.argmax(prof(ss, self.h, self.dg))]

    def peak(self):
        return self.pt(self.peak_s())


def ball_on(curve, tr, color=YELLOW, r=0.17):
    d = Dot(radius=r, color=color)
    d.add_updater(lambda m: m.move_to(curve.pt(tr.get_value()) + UP * r))
    d.move_to(curve.pt(tr.get_value()) + UP * r)
    return d


def cross(center, size=0.28, color=RED, w=7):
    c = np.array(center, dtype=float)
    a = Line(c + np.array([-size, size, 0]), c + np.array([size, -size, 0]), color=color, stroke_width=w)
    b = Line(c + np.array([-size, -size, 0]), c + np.array([size, size, 0]), color=color, stroke_width=w)
    return VGroup(a, b)


def check(center, size=0.24, color=GREEN, w=7):
    c = np.array(center, dtype=float)
    return VMobject(color=color, stroke_width=w).set_points_as_corners(
        [c + np.array([-size, 0.0, 0]), c + np.array([-size * 0.25, -size * 0.8, 0]), c + np.array([size, size * 0.9, 0])])


def vbrace(x, y_lo, y_hi, color, label=None, label_dx=0.55, size=30, w=4):
    """Vertical double arrow between two heights, with an optional mono label."""
    arr = DoubleArrow([x, y_lo, 0], [x, y_hi, 0], color=color, buff=0, stroke_width=w,
                      tip_length=0.2, max_tip_length_to_length_ratio=0.45)
    g = VGroup(arr)
    if label:
        g.add(M(label, size, color).move_to([x + label_dx, (y_lo + y_hi) / 2, 0]))
    return g


def blob(rfun, scale=1.0, n=160, center=ORIGIN):
    """A closed schematic shape (NOT a molecule: an abstract silhouette used as a shape-fit cartoon)."""
    th = np.linspace(0, TAU, n, endpoint=False)
    pts = [np.array([scale * rfun(t) * np.cos(t), scale * rfun(t) * np.sin(t), 0.0]) + center for t in th]
    return Polygon(*pts, stroke_width=0)


def r_ts(t):
    return 1.0 + 0.26 * np.cos(3 * t) + 0.12 * np.cos(2 * t + 0.8)


def r_sub(t):
    return 0.74 + 0.03 * np.cos(2 * t)


def make_cup(shape, gap, color=BLUE, w=8):
    c = VMobject()
    c.pointwise_become_partial(shape, gap, 1 - gap)
    c.set_stroke(color, w).set_fill(opacity=0)
    return c


def dots_row(active, n=4, y=3.15):
    g = VGroup()
    for i in range(n):
        on = (i == active)
        c = Circle(radius=0.26, stroke_color=TEXT if on else GREY, stroke_width=3,
                   fill_color=TEXT if on else BG, fill_opacity=1 if on else 0)
        t = T(str(i + 1), 24, BG if on else GREY, weight=BOLD).move_to(c)
        g.add(VGroup(c, t))
    return g.arrange(RIGHT, buff=0.45).move_to([0, y, 0])


# ---------------------------------------------------------------- title and end cards
class S00Title(TitleCard):
    LESSON = "Enzyme action basics"
    TITLE = "Same destination, faster arrival"


class S07End(EndCard):
    LINE = "An enzyme changes the speed, never the destination."


# ---------------------------------------------------------------- s01: two GPS questions
class S01Gps(Base):
    CUES = {"First:": 4.43, "That's thermodynamics": 8.20, "Second:": 14.84, "That's kinetics": 17.85,
            "Here's the line": 24.86, "It never changes": 29.61}

    def construct(self):
        cxl, cxr = -3.35, 3.35
        py, ph = 0.2, 4.6          # panel centre y, height
        top = py + ph / 2

        q = T("Does this reaction work?", 40).move_to([0, 3.05, 0])
        self.play(FadeIn(q, shift=DOWN * 0.15), run_time=1.0)

        def panel(cx, col):
            return RoundedRectangle(corner_radius=0.2, width=5.9, height=ph, stroke_color=col, stroke_width=3,
                                    fill_color=col, fill_opacity=0.06).move_to([cx, py, 0])

        # --- first question: will it get there? (thermodynamics)
        self.until("First:")
        lbox = panel(cxl, GREEN)
        lhead = T("Will it get there?", 34, GREEN, weight=BOLD).move_to([cxl, top - 0.5, 0])
        A = np.array([cxl - 2.0, 0.45, 0]); B = np.array([cxl + 2.0, -0.5, 0])
        dA = Dot(A, radius=0.16, color=YELLOW); dB = Dot(B, radius=0.16, color=GREEN)
        lA = T("reactants", 24, YELLOW).next_to(dA, UP, buff=0.15)
        lB = T("products", 24, GREEN).next_to(dB, DOWN, buff=0.15)
        route = Arrow(A, B, color=GREEN, buff=0.22, stroke_width=7)
        self.play(Create(lbox), FadeIn(lhead), run_time=1.0)
        self.play(FadeIn(dA), FadeIn(lA), FadeIn(dB), FadeIn(lB), run_time=0.8)
        self.play(GrowArrow(route), run_time=1.6)
        self.until("That's thermodynamics")
        lfoot = VGroup(T("THERMODYNAMICS", 26, GREEN, weight=BOLD), M("ΔG", 30, GREEN)).arrange(RIGHT, buff=0.3)
        lfoot.move_to([cxl, py - ph / 2 + 0.5, 0])
        self.play(FadeIn(lfoot, shift=UP * 0.1), run_time=0.8)
        self.until("whether the reaction is favorable")
        fav = T("favorable", 28, GREEN).move_to([cxl + 0.35, 1.2, 0])
        ck = check([cxl + 1.65, 1.2, 0])
        self.play(FadeIn(fav), Create(ck), run_time=0.9)

        # --- second question: how congested is the road? (kinetics)
        self.until("Second:")
        rbox = panel(cxr, RED)
        rhead = T("How congested?", 34, RED, weight=BOLD).move_to([cxr, top - 0.5, 0])
        curve = Curve(cxr - 2.0, cxr + 2.0, 0.45, 1.35, -1.0)
        cmob = curve.mob(RED)
        dA2 = Dot(curve.pt(0), radius=0.16, color=YELLOW)
        dB2 = Dot(curve.pt(1), radius=0.16, color=GREEN)
        lA2 = T("reactants", 24, YELLOW).next_to(dA2, UP, buff=0.15)
        lB2 = T("products", 24, GREEN).next_to(dB2, DOWN, buff=0.15)
        self.play(Create(rbox), FadeIn(rhead), run_time=1.0)
        self.play(FadeIn(dA2), FadeIn(lA2), FadeIn(dB2), FadeIn(lB2), run_time=0.6)
        self.play(Create(cmob), run_time=1.6)
        self.until("That's kinetics")
        pk = curve.peak()
        ba = vbrace(pk[0], 0.45, pk[1] - 0.04, RED)
        bl = M("ΔG‡", 30, RED).move_to([pk[0] + 1.05, 1.05, 0])
        rfoot = VGroup(T("KINETICS", 26, RED, weight=BOLD), M("ΔG‡", 30, RED)).arrange(RIGHT, buff=0.3)
        rfoot.move_to([cxr, py - ph / 2 + 0.5, 0])
        tr = ValueTracker(0)
        ball = ball_on(curve, tr)
        self.play(FadeIn(rfoot, shift=UP * 0.1), GrowFromCenter(ba), FadeIn(bl), FadeIn(ball), FadeOut(dA2), run_time=1.0)
        # a slow, labored crossing of the hill while the narration says "how fast you'll get there"
        tt = max(3.0, self.span("That's kinetics", "Here's the line") - 1.8)
        self.play(tr.animate.set_value(0.38), run_time=tt * 0.4, rate_func=rate_functions.ease_out_quad)
        self.play(tr.animate.set_value(0.47), run_time=tt * 0.35, rate_func=linear)
        self.play(tr.animate.set_value(1.0), run_time=tt * 0.25, rate_func=rate_functions.ease_in_quad)
        self.play(FadeOut(ball), run_time=0.3)          # arrived: the product dot stays, the ball goes

        # --- the line to remember: enzyme answers only the second question
        self.until("Here's the line")
        enz = chip("enzyme", BLUE, 30).move_to([0, -3.0, 0])
        a_r = Arrow([0.6, -2.62, 0], [cxr - 0.7, py - ph / 2 - 0.05, 0], color=BLUE, buff=0, stroke_width=6)
        a_l = DashedLine([-0.6, -2.62, 0], [cxl + 0.7, py - ph / 2 - 0.05, 0], color=GREY, stroke_width=5)
        x_l = cross([cxl + 0.05 - 0.9 + 0.0, -2.62, 0], 0.2, RED, 6)
        x_l.move_to((np.array([-0.6, -2.62, 0]) + np.array([cxl + 0.7, py - ph / 2 - 0.05, 0])) / 2)
        self.play(FadeIn(enz, shift=UP * 0.2), run_time=0.8)
        # dim the thermodynamics panel (stroke and contents only; keep its fill faint, not brighter)
        self.play(GrowArrow(a_r), Create(a_l), Create(x_l),
                  lbox.animate.set_stroke(opacity=0.3).set_fill(opacity=0.03),
                  VGroup(lhead, dA, lA, dB, lB, route, lfoot, fav, ck).animate.set_opacity(0.3), run_time=1.2)
        self.until("It never changes")
        # lower the hill: same ends, lower barrier, faster crossing
        new = Curve(cxr - 2.0, cxr + 2.0, 0.45, 0.8, -1.0)
        pk2 = new.peak()
        ba2 = vbrace(pk2[0], 0.45, pk2[1] - 0.04, BLUE)
        bl2 = M("ΔG‡", 30, BLUE).move_to([pk2[0] + 0.85, pk2[1] + 0.35, 0])
        tr2 = ValueTracker(0)
        ball2 = ball_on(new, tr2)                        # rides the LOWERED curve
        self.play(Transform(cmob, new.mob(BLUE)), Transform(ba, ba2), Transform(bl, bl2), FadeIn(ball2), run_time=1.4)
        self.play(tr2.animate.set_value(1.0), run_time=1.1, rate_func=linear)
        self.play(FadeOut(ball2), run_time=0.3)
        self.finish()


# ---------------------------------------------------------------- s02: the traffic light
class S02Light(Base):
    CUES = {"Green": 3.89, "Yellow": 8.63, "Red": 12.09, "It can only speed": 24.46, "Spontaneity belongs": 27.37}

    def construct(self):
        cx = -5.3
        housing = RoundedRectangle(corner_radius=0.3, width=1.5, height=5.3, stroke_color=GREY, stroke_width=3,
                                   fill_color="#171a23", fill_opacity=1).move_to([cx, -0.1, 0])
        ys = [1.55, -0.1, -1.75]
        cols = [GREEN, AMBER, RED]
        lamps = [Circle(radius=0.55, stroke_width=0, fill_color=c, fill_opacity=0.16).move_to([cx, y, 0])
                 for c, y in zip(cols, ys)]
        self.play(FadeIn(housing), *[FadeIn(l) for l in lamps], run_time=1.0)

        def row(dg, words, col, y):
            a = M(dg, 36, col)
            a.move_to([-3.9 + a.width / 2, y, 0])
            b = T(words, 30)
            b.move_to([-1.35 + b.width / 2, y, 0])
            return VGroup(a, b)

        rows = [row("ΔG < 0", "go: spontaneous", GREEN, ys[0]),
                row("ΔG = 0", "equilibrium: no net movement", AMBER, ys[1]),
                row("ΔG > 0", "stop: the cell must spend energy", RED, ys[2])]

        def light_on(i, run=0.6):
            anims = []
            for j, l in enumerate(lamps):
                if j == i:
                    anims.append(l.animate.set_fill(opacity=1).set_stroke(cols[j], width=8, opacity=0.35))
                else:
                    anims.append(l.animate.set_fill(opacity=0.16).set_stroke(width=0))
            self.play(*anims, run_time=run)

        self.until("Green")
        light_on(0)
        self.play(FadeIn(rows[0], shift=RIGHT * 0.2), run_time=0.8)
        self.until("Yellow")
        light_on(1)
        self.play(FadeIn(rows[1], shift=RIGHT * 0.2), run_time=0.8)
        self.until("Red")
        light_on(2)
        self.play(FadeIn(rows[2], shift=RIGHT * 0.2), run_time=0.8)

        # the enzyme cannot change the colour of the light
        self.until("The crucial part")
        light_on(0, 0.8)
        self.play(FadeOut(rows[1]), FadeOut(rows[2]), run_time=0.8)
        self.until("an enzyme cannot")
        self.play(FadeOut(rows[0]), run_time=0.5)
        enz = chip("enzyme", BLUE, 32).move_to([0.6, 1.55, 0])
        push = Arrow([-0.6, 1.55, 0], [-4.35, 1.55, 0], color=BLUE, buff=0, stroke_width=6)
        x = cross([-3.2, 1.55, 0], 0.26, RED, 8)
        cap = T("can't change the color", 30, GREY).move_to([-1.6, 0.8, 0])
        self.play(FadeIn(enz, shift=LEFT * 0.2), GrowArrow(push), run_time=1.0)
        self.play(Create(x), FadeIn(cap), run_time=0.7)
        self.until("It can only speed")
        # ... it can only speed your passage through a green one
        road = Line([-3.4, -1.4, 0], [6.0, -1.4, 0], color=GREY, stroke_width=8)
        mark = Line([-3.4, -1.4, 0], [-3.4, -1.0, 0], color=GREEN, stroke_width=4)
        end = Line([6.0, -1.4, 0], [6.0, -1.0, 0], color=GREEN, stroke_width=4)
        car = Dot(radius=0.2, color=YELLOW).move_to([-3.4, -1.15, 0])
        self.play(FadeOut(push), FadeOut(x), FadeOut(cap), Create(road), FadeIn(car), run_time=0.6)
        slow = T("slow", 30, GREY).move_to([1.2, -2.0, 0])
        self.play(FadeIn(slow), car.animate.move_to([-1.6, -1.15, 0]), run_time=1.6, rate_func=linear)
        fast = T("fast", 30, BLUE).move_to([1.2, -2.0, 0])
        self.play(enz.animate.move_to([2.4, -0.45, 0]), FadeOut(slow), FadeIn(fast),
                  car.animate.move_to([-1.3, -1.15, 0]), run_time=0.6, rate_func=linear)
        self.play(car.animate.move_to([5.9, -1.15, 0]), run_time=0.7, rate_func=linear)
        self.until("Spontaneity belongs")
        sp = T("set by ΔG, not by the catalyst", 30, GREEN).move_to([0.7, 1.55, 0])
        self.play(FadeIn(sp, shift=UP * 0.1), run_time=0.8)
        self.finish()


# ---------------------------------------------------------------- s03: the mountain shortcut
class S03Mountain(Base):
    CUES = {"Without an enzyme": 1.99, "Notice both routes": 10.49, "So how exactly": 18.24,
            "transition-state secret": 21.04}

    def construct(self):
        hi = Curve(-5.0, 5.0, -0.6, 3.4, -1.0)
        lo = Curve(-5.0, 5.0, -0.6, 1.4, -1.0)
        hi_m, lo_m = hi.mob(RED, 6), lo.mob(BLUE, 6)
        pts = [hi.pt(s) for s in np.linspace(0, 1, 160)] + [np.array([5.0, -2.9, 0]), np.array([-5.0, -2.9, 0])]
        rock = Polygon(*pts, stroke_width=0, fill_color=GREY, fill_opacity=0.2)
        tr = ValueTracker(0)
        ball = ball_on(hi, tr)
        lab_r = T("reactants", 28, YELLOW).next_to(ball, UP, buff=0.3)
        end_dot = Dot(hi.pt(1.0), radius=0.17, color=GREEN)
        lab_p = T("products", 28, GREEN).next_to(end_dot, UP, buff=0.3)

        self.play(FadeIn(rock), FadeIn(ball), FadeIn(lab_r), FadeIn(end_dot), FadeIn(lab_p), run_time=1.2)
        self.until("Without an enzyme")
        self.play(Create(hi_m), run_time=1.4)
        pkh = hi.peak()
        lab_hi = T("high mountain", 28, RED).move_to([pkh[0] + 2.2, pkh[1] + 0.05, 0])
        self.play(FadeIn(lab_hi), FadeOut(lab_r), run_time=0.5)
        self.play(tr.animate.set_value(1.0), run_time=2.8, rate_func=smooth)
        self.play(FadeOut(ball), run_time=0.3)
        # the enzyme: a lower pass
        self.until("With an enzyme")
        tr.set_value(0)
        ball = ball_on(lo, tr)
        lab_lo = T("lower pass (enzyme)", 28, BLUE).move_to([3.1, 0.55, 0])
        self.play(hi_m.animate.set_stroke(opacity=0.4), lab_hi.animate.set_opacity(0.4), FadeIn(ball), FadeIn(lab_r),
                  Create(lo_m), FadeIn(lab_lo), run_time=1.4)
        pkl = lo.peak()
        self.play(lab_r.animate.set_opacity(0), tr.animate.set_value(1.0), run_time=1.8, rate_func=smooth)
        self.play(FadeOut(ball), run_time=0.3)
        # both routes end at the same place: send one traveller down each route at once
        self.until("Notice both routes")
        t2 = ValueTracker(0)
        b_hi = ball_on(hi, t2, RED, 0.13)
        b_lo = ball_on(lo, t2, BLUE, 0.13)
        self.play(FadeIn(b_hi), FadeIn(b_lo), run_time=0.3)
        self.play(t2.animate.set_value(1.0), run_time=2.4, rate_func=smooth)
        self.play(FadeOut(b_hi), FadeOut(b_lo), Indicate(end_dot, scale_factor=1.8, color=GREEN),
                  Indicate(lab_p, color=GREEN), run_time=1.2)
        self.until("the enzyme doesn't move")
        same = T("same destination", 28, GREEN).move_to([3.0, -2.3, 0])
        self.play(FadeIn(same, shift=UP * 0.1), Flash(end_dot, color=GREEN, flash_radius=0.45), run_time=0.9)
        # how does it lower the pass?
        self.until("So how exactly")
        q = T("?", 64, PURPLE, weight=BOLD).move_to([pkl[0], pkl[1] - 1.0, 0])
        ring = Circle(radius=0.35, color=PURPLE, stroke_width=4).move_to(pkl + UP * 0.02)
        self.play(FadeOut(same), Create(ring), FadeIn(q, scale=0.5), run_time=0.9)
        self.until("transition-state secret")
        self.play(Indicate(ring, color=PURPLE, scale_factor=1.4), run_time=1.0)
        self.finish()


# ---------------------------------------------------------------- s04: lowers the barrier, not DG
class S04Barrier(Base):
    CUES = {"Both curves": 3.84, "What changes": 15.33, "far lower": 22.0, "Enzymes speed reactions": 24.80,
            "by stabilizing": 26.5, "not by changing": 31.0}

    def construct(self):
        X0, X1, Y0 = -4.4, 4.1, -1.2
        unc = Curve(X0, X1, Y0, 3.3, -1.0)
        cat = Curve(X0, X1, Y0, 1.3, -1.0)
        ax_y = Arrow([-5.0, -2.75, 0], [-5.0, 2.75, 0], color=GREY, buff=0, stroke_width=4, tip_length=0.2)
        ax_x = Arrow([-5.0, -2.75, 0], [5.9, -2.75, 0], color=GREY, buff=0, stroke_width=4, tip_length=0.2)
        ylab = T("Free energy, G", 26, GREY).rotate(PI / 2).move_to([-5.6, 0.0, 0])
        xlab = T("Reaction progress", 26, GREY).move_to([0.4, -3.2, 0])
        self.play(Create(ax_y), Create(ax_x), FadeIn(ylab), FadeIn(xlab), run_time=1.6)

        # both curves: same substrate, same product
        self.until("Both curves")
        c_u, c_c = unc.mob(RED), cat.mob(BLUE)
        sub = Dot(unc.pt(0), radius=0.17, color=YELLOW)
        prod = Dot(unc.pt(1), radius=0.17, color=GREEN)
        l_sub = T("substrate", 26, YELLOW).next_to(sub, DOWN, buff=0.2).shift(RIGHT * 0.45)
        l_prod = T("product", 26, GREEN).next_to(prod, UP, buff=0.2).shift(LEFT * 0.35)
        l_unc = T("without enzyme", 26, RED).move_to([2.9, 0.5, 0])
        l_cat = T("with enzyme", 26, BLUE).move_to([2.9, -0.55, 0])
        self.play(FadeIn(sub), FadeIn(l_sub), run_time=0.6)
        self.play(Create(c_u), FadeIn(l_unc), FadeIn(prod), FadeIn(l_prod), run_time=2.4)
        self.play(Create(c_c), FadeIn(l_cat), run_time=1.6)
        # so DG is identical
        self.until("so ΔG")
        d_sub = DashedLine([X0, Y0, 0], [4.85, Y0, 0], color=YELLOW, stroke_width=2.5).set_opacity(0.55)
        d_prod = DashedLine([X1 - 1.2, unc.pt(1)[1], 0], [4.85, unc.pt(1)[1], 0], color=GREEN, stroke_width=2.5).set_opacity(0.55)
        dg = vbrace(4.85, unc.pt(1)[1], Y0, GREEN, "ΔG", 0.65, 32, 5)
        self.play(Create(d_sub), Create(d_prod), run_time=0.8)
        self.play(GrowFromCenter(dg), run_time=1.0)
        # the hill is what changes
        self.until("What changes")
        self.play(FadeOut(l_unc), FadeOut(l_cat), run_time=0.5)
        pu, pc = unc.peak(), cat.peak()
        d_top = DashedLine([-2.9, pu[1], 0], [pu[0], pu[1], 0], color=RED, stroke_width=2.5).set_opacity(0.6)
        b_u = vbrace(-2.9, Y0, pu[1], RED, "ΔG‡", -0.7, 30, 5)
        self.play(Create(d_top), GrowFromCenter(b_u), run_time=1.2)
        self.until("far lower")
        b_c = vbrace(pc[0], Y0, pc[1], BLUE, None, 0, 30, 5)
        # label sits inside the blue hump, left of its arrow, so the TS arrow above has room later
        t_c = M("ΔG‡", 26, BLUE).move_to([pc[0] - 0.52, (Y0 + pc[1]) / 2 - 0.1, 0])
        self.play(GrowFromCenter(b_c), FadeIn(t_c), run_time=1.2)
        # transition state at the top of the hill
        self.until("Enzymes speed reactions")
        ts_u = Dot(pu, radius=0.16, color=PURPLE)
        ts_c = Dot(pc, radius=0.16, color=PURPLE)
        l_ts = T("transition state", 26, PURPLE).move_to([pu[0] + 2.25, pu[1] - 0.05, 0])
        self.play(FadeIn(ts_u, scale=1.6), FadeIn(l_ts), run_time=0.9)
        self.until("by stabilizing")
        self.play(FadeIn(ts_c, scale=1.6), run_time=0.5)
        st = Arrow(pu + DOWN * 0.3, pc + UP * 0.35, color=PURPLE, buff=0.0, stroke_width=5)
        self.play(GrowArrow(st), run_time=0.9)
        self.until("not by changing")
        self.play(FadeOut(st), Indicate(dg, color=GREEN, scale_factor=1.25), Indicate(prod, color=GREEN, scale_factor=2.0),
                  run_time=1.4)
        self.finish()


# ---------------------------------------------------------------- s05: what is the transition state
class S05Ts(Base):
    CUES = {"The top row": 8.38, "substrate in": 10.02, "transition state, product": 11.10, "product out": 12.27,
            "The bottom row": 13.44, "The key insight": 19.19}

    def construct(self):
        OFF = 1.7                      # the curve starts low on screen and moves to the "top row" later
        cv = Curve(-4.5, 4.5, 0.95, 2.0, -0.5)
        dy = ValueTracker(-OFF)
        cm = cv.mob(RED, 5)
        pk = cv.peak()
        tr = ValueTracker(0)
        ball = Dot(radius=0.17, color=YELLOW)
        ball.add_updater(lambda m: m.move_to(cv.pt(tr.get_value()) + UP * (0.17 + dy.get_value())))
        ball.move_to(cv.pt(0) + UP * (0.17 - OFF))
        l_sub = T("substrate", 26, YELLOW).move_to([cv.pt(0)[0] + 0.1, 0.35, 0])
        l_prod = T("product", 26, GREEN).move_to([cv.pt(1)[0] - 0.1, -0.1, 0])
        top = VGroup(cm, l_sub, l_prod)
        top.shift(DOWN * OFF)
        # "neither substrate nor product": both ends are named from the start
        self.play(Create(cm), FadeIn(ball), FadeIn(l_sub), FadeIn(l_prod), run_time=1.6)

        # fleeting, highest-energy: the ball reaches the top and flashes
        self.until("it's a fleeting")
        self.play(tr.animate.set_value(cv.peak_s()), run_time=2.2, rate_func=smooth)
        ts = Dot(pk + DOWN * OFF, radius=0.2, color=PURPLE)
        l_ts = T("transition state", 28, PURPLE).move_to([pk[0] + 2.1, pk[1] + 0.1 - OFF, 0])
        top.add(ts, l_ts)
        self.play(FadeIn(ts, scale=2.0), Flash(ts, color=PURPLE, flash_radius=0.5), FadeIn(l_ts), run_time=0.9)
        self.until("exists for about")
        fs = M("≈ 10 fs", 30, PURPLE).move_to([pk[0] - 2.0, pk[1] + 0.1 - OFF, 0])
        top.add(fs)
        self.play(FadeIn(fs, shift=RIGHT * 0.15), run_time=0.7)
        # the arc: substrate in, transition state, product out
        self.until("The top row")
        self.play(tr.animate.set_value(1.0), run_time=1.5, rate_func=smooth)
        self.until("substrate in", 0.1)
        self.play(Indicate(l_sub, color=YELLOW), run_time=0.7)
        self.until("transition state, product", 0.1)
        self.play(Indicate(l_ts, color=PURPLE), Indicate(ts, color=PURPLE), run_time=0.7)
        self.until("product out", 0.1)
        self.play(Indicate(l_prod, color=GREEN), run_time=0.7)

        # zoom in on the chemistry: bond fractions (not drawn as atoms)
        self.until("The bottom row")
        tr.set_value(0)
        s_ts = cv.peak_s()
        frac = lambda: 1 / (1 + np.exp(-(tr.get_value() - s_ts) * 14))   # exactly 50/50 at the barrier top
        zoom = T("zooming in on the chemistry", 26, GREY).move_to([0, -0.75, 0])
        BX, BW = -1.6, 6.0

        def bar(y, col, getter):
            return always_redraw(lambda: Rectangle(width=max(0.001, BW * getter()), height=0.5, stroke_width=0,
                                                   fill_color=col, fill_opacity=0.9).align_to([BX, 0, 0], LEFT).set_y(y))

        y1, y2 = -1.55, -2.5
        frame1 = Rectangle(width=BW, height=0.5, stroke_color=GREY, stroke_width=2).move_to([BX + BW / 2, y1, 0])
        frame2 = Rectangle(width=BW, height=0.5, stroke_color=GREY, stroke_width=2).move_to([BX + BW / 2, y2, 0])
        n1 = T("old bond", 28, YELLOW).move_to([BX - 0.35, y1, 0]).align_to([BX - 0.3, 0, 0], RIGHT)
        n2 = T("new bond", 28, GREEN).move_to([BX - 0.35, y2, 0]).align_to([BX - 0.3, 0, 0], RIGHT)
        b1 = bar(y1, YELLOW, lambda: 1 - frac())
        b2 = bar(y2, GREEN, lambda: frac())
        p1 = always_redraw(lambda: M(f"{int(round(100 * (1 - frac())))}%", 26, YELLOW).move_to([BX + BW + 0.75, y1, 0]))
        p2 = always_redraw(lambda: M(f"{int(round(100 * frac()))}%", 26, GREEN).move_to([BX + BW + 0.75, y2, 0]))
        # the curve moves up to become the top row; the ball's offset tracker follows it
        self.play(top.animate.shift(UP * OFF), dy.animate.set_value(0), FadeOut(fs), run_time=1.0)
        self.play(FadeIn(zoom), Create(frame1), Create(frame2), FadeIn(n1), FadeIn(n2),
                  FadeIn(b1), FadeIn(b2), FadeIn(p1), FadeIn(p2), run_time=1.2)
        ts_c = ts.get_center()
        self.play(tr.animate.set_value(cv.peak_s()), run_time=1.6, rate_func=smooth)
        half = T("half-broken, half-formed", 28, PURPLE).move_to([0, -3.2, 0])
        self.play(FadeIn(half, shift=UP * 0.1), Flash(ts, color=PURPLE, flash_radius=0.5), run_time=0.9)
        self.until("The key insight")
        self.play(FadeOut(half), run_time=0.4)          # the 50/50 caption only belongs at the top
        self.play(tr.animate.set_value(1.0), run_time=1.1, rate_func=smooth)
        self.play(FadeOut(ball), FadeOut(VGroup(zoom, frame1, frame2, n1, n2, b1, b2, p1, p2)), run_time=0.6)

        # the key insight: the TS has a specific shape and the enzyme is tuned to it
        BC = np.array([-3.3, -2.0, 0])
        shape = blob(r_ts, 0.8, center=BC)
        shape.set_fill(PURPLE, 0.85).set_stroke(PURPLE, 2)
        outline = blob(r_ts, 0.8 * 1.2, center=BC)
        gap = ValueTracker(0.16)
        cup = always_redraw(lambda: make_cup(outline, gap.get_value(), BLUE, 8))
        line = DashedLine(pk + DOWN * 0.25, BC + UP * 1.2, color=PURPLE, stroke_width=3).set_opacity(0.7)
        l_geo = T("a specific geometry", 30, PURPLE)
        l_geo.move_to([-0.9 + l_geo.width / 2, -1.55, 0])
        l_en = T("the enzyme is tuned to grip it", 30, BLUE)
        l_en.move_to([-0.9 + l_en.width / 2, -2.5, 0])
        self.play(Create(line), FadeIn(shape, scale=0.5), run_time=1.0)
        self.play(FadeIn(l_geo, shift=RIGHT * 0.15), run_time=0.7)
        self.until("tuned the enzyme")
        self.add(cup)
        self.play(FadeIn(cup), FadeIn(l_en, shift=RIGHT * 0.15), run_time=0.8)
        self.play(gap.animate.set_value(0.05), run_time=1.2)
        self.finish()


# ---------------------------------------------------------------- s06: binding energy facilitates catalysis
class S06Binding(Base):
    CUES = {"First,": 2.54, "releasing binding energy": 5.7, "Second,": 8.89,
            "fits the transition state better": 12.4, "than it fits the ground-state": 14.6,
            "Third,": 17.35, "catalyzed ΔG‡": 19.2, "equals the uncatalyzed": 20.4, "minus the binding": 22.6,
            "Fourth,": 25.23, "drugs shaped": 27.55, "exploit that tight fit": 30.2, "binding far harder": 32.0,
            "than substrate mimics": 33.5, "The enzyme's job": 34.75, "bind the transition state": 37.01}

    def construct(self):
        X0, X1, Y0 = -4.4, 4.4, -1.5
        unc = Curve(X0, X1, Y0, 3.0, -0.8)
        cat = Curve(X0, X1, Y0, 1.1, -0.8)

        # ---- 1. energy landscape
        tags = dots_row(0)
        self.play(FadeIn(tags), run_time=0.8)
        c_u, c_c = unc.mob(RED, 6), cat.mob(BLUE, 6)
        pu, pc = unc.peak(), cat.peak()
        sub = Dot(unc.pt(0), radius=0.16, color=YELLOW)
        prod = Dot(unc.pt(1), radius=0.16, color=GREEN)
        l_sub = T("substrate", 26, YELLOW).next_to(sub, UP, buff=0.2).shift(RIGHT * 0.3)
        l_prod = T("product", 26, GREEN).next_to(prod, UP, buff=0.2)
        ax_y = Arrow([-5.0, -2.75, 0], [-5.0, 2.5, 0], color=GREY, buff=0, stroke_width=4, tip_length=0.2)
        ax_x = Arrow([-5.0, -2.75, 0], [5.4, -2.75, 0], color=GREY, buff=0, stroke_width=4, tip_length=0.2)
        l_yax = T("Free energy, G", 26, GREY).rotate(PI / 2).move_to([-5.5, 0.0, 0])
        l_xax = T("Reaction progress", 26, GREY).move_to([0.2, -3.15, 0])
        l_unc = T("without enzyme", 26, RED).move_to([-3.2, 2.25, 0])
        l_cat = T("with enzyme", 26, BLUE).move_to([-3.2, 1.7, 0])
        ts_u = Dot(pu, radius=0.17, color=PURPLE)
        ts_c = Dot(pc, radius=0.17, color=PURPLE)
        self.play(Create(ax_y), Create(ax_x), FadeIn(l_yax), FadeIn(l_xax), run_time=1.0)
        self.until("First,", 0.2)
        self.play(FadeIn(sub), FadeIn(l_sub), FadeIn(prod), FadeIn(l_prod), Create(c_u), FadeIn(l_unc), run_time=1.6)
        self.play(FadeIn(ts_u, scale=1.6), run_time=0.4)
        self.until("releasing binding energy", 0.6)
        self.play(Create(c_c), FadeIn(l_cat), run_time=1.0)
        self.play(FadeIn(ts_c, scale=1.6), run_time=0.4)
        bind = Arrow(pu + DOWN * 0.3, pc + UP * 0.28, color=GOLD, buff=0, stroke_width=8)
        l_bind = T("binding energy released", 28, GOLD).move_to([pu[0] + 3.2, (pu[1] + pc[1]) / 2 + 0.45, 0])
        l_at = T("at the transition state", 26, PURPLE).move_to([pu[0] + 3.2, (pu[1] + pc[1]) / 2 - 0.05, 0])
        self.play(GrowArrow(bind), FadeIn(l_bind), run_time=1.0)
        self.play(FadeIn(l_at), run_time=0.6)

        # ---- 2. shape complementarity
        self.until("Second,", 0.2)
        stage1 = VGroup(c_u, c_c, sub, prod, l_sub, l_prod, ax_y, ax_x, l_yax, l_xax, l_unc, l_cat, ts_u, ts_c,
                        bind, l_bind, l_at)
        self.play(FadeOut(stage1), Transform(tags, dots_row(1)), run_time=0.9)
        C = np.array([0.0, -0.2, 0.0])
        ts_shape = blob(r_ts, 1.25, center=C)
        ts_shape.set_fill(PURPLE, 0.85).set_stroke(PURPLE, 2)
        outline = blob(r_ts, 1.25 * 1.17, center=C)
        cup = make_cup(outline, 0.07, BLUE, 9)
        sub_shape = blob(r_sub, 1.25, center=C).set_fill(YELLOW, 0.9).set_stroke(YELLOW, 2)
        l_site = T("active site", 28, BLUE).move_to([C[0], C[1] - 2.45, 0])
        self.play(Create(cup), FadeIn(l_site), run_time=1.2)
        self.until("fits the transition state better", 0.3)
        l_t = T("transition state", 28, PURPLE).move_to([-3.6, 1.5, 0])
        snug = T("snug fit", 28, GREEN).move_to([3.8, 0.2, 0])
        self.play(FadeIn(ts_shape, scale=0.4), FadeIn(l_t, shift=RIGHT * 0.1), FadeIn(snug), run_time=1.2)
        self.until("than it fits the ground-state", 0.2)
        l_s = T("ground-state substrate", 28, YELLOW).move_to([-3.6, 1.5, 0])
        loose = T("loose fit", 28, GREY).move_to([3.8, 0.2, 0])
        self.play(Transform(ts_shape, sub_shape), FadeOut(l_t), FadeOut(snug), run_time=0.9)
        self.play(FadeIn(l_s, shift=RIGHT * 0.1), FadeIn(loose), run_time=0.6)
        sub_shape = ts_shape

        # ---- 3. the bookkeeping: take the binding energy off the top of the uncatalyzed barrier
        self.until("Third,", 0.2)
        self.play(FadeOut(VGroup(cup, sub_shape, l_s, loose, l_site)), Transform(tags, dots_row(2)), run_time=0.9)
        base_y = -2.3
        BWID = 1.4
        hu, hb = 3.6, 2.3
        hc = hu - hb
        XU, XB = -1.6, 1.6
        eq = VGroup(M("ΔG‡cat", 34, BLUE), M("=", 34, TEXT), M("ΔG‡uncat", 34, RED), M("−", 34, TEXT), M("ΔGbind", 34, GOLD))
        eq.arrange(RIGHT, buff=0.3).move_to([0, 2.25, 0])
        base = Line([-3.6, base_y, 0], [3.6, base_y, 0], color=GREY, stroke_width=3)
        bar_low = Rectangle(width=BWID, height=hc, stroke_width=0, fill_color=RED, fill_opacity=0.9).move_to([XU, base_y + hc / 2, 0])
        bar_top = Rectangle(width=BWID, height=hb, stroke_width=0, fill_color=RED, fill_opacity=0.9).move_to([XU, base_y + hc + hb / 2, 0])
        n_u = T("uncatalyzed ΔG‡", 26, RED).next_to(bar_low, DOWN, buff=0.2)
        self.until("catalyzed ΔG‡", 0.2)
        self.play(FadeIn(eq[0], shift=DOWN * 0.1), run_time=0.6)
        self.until("equals the uncatalyzed", 0.2)
        self.play(FadeIn(eq[1]), FadeIn(eq[2], shift=DOWN * 0.1), Create(base),
                  GrowFromEdge(VGroup(bar_low, bar_top), DOWN), FadeIn(n_u), run_time=1.1)
        self.until("minus the binding", 0.2)
        # the top slab of the barrier is the binding energy: it turns gold, then is carried away
        self.play(FadeIn(eq[3]), FadeIn(eq[4], shift=DOWN * 0.1), bar_top.animate.set_fill(GOLD), run_time=0.8)
        n_b = T("binding energy", 26, GOLD)
        n_b.move_to([XB + BWID / 2 + 0.25 + n_b.width / 2, base_y + hc + hb / 2, 0])
        n_c = T("catalyzed ΔG‡", 26, BLUE).next_to(bar_low, DOWN, buff=0.2)
        self.play(bar_top.animate.move_to([XB, base_y + hc + hb / 2, 0]), FadeIn(n_b),
                  bar_low.animate.set_fill(BLUE), ReplacementTransform(n_u, n_c), run_time=1.3)
        self.play(Indicate(eq[0], color=BLUE, scale_factor=1.06), Indicate(bar_low, color=BLUE, scale_factor=1.08), run_time=0.9)

        # ---- 4. the payoff in medicine
        self.until("Fourth,", 0.2)
        self.play(FadeOut(VGroup(eq, base, bar_low, bar_top, n_b, n_c)), Transform(tags, dots_row(3)), run_time=0.9)
        # two rows: a transition-state analog drug (snug) and a substrate mimic (loose), with binding-strength bars
        rows_y = [1.1, -1.3]
        cups, items, lbls, bars = [], [], [], []
        for k, (yy, col, name, rf, length) in enumerate([
                (rows_y[0], PURPLE, "transition-state analog (drug)", r_ts, 6.2),
                (rows_y[1], YELLOW, "substrate mimic", r_sub, 0.9)]):
            c = np.array([-5.0, yy, 0.0])
            outl = blob(r_ts, 0.6 * 1.17, center=c)
            cups.append(make_cup(outl, 0.07, BLUE, 6))
            sh = blob(rf, 0.6, center=c).set_fill(col, 0.9).set_stroke(col, 2)
            items.append(sh)
            lb = T(name, 28, col)
            lb.move_to([-3.6 + lb.width / 2, yy + 0.65, 0])
            lbls.append(lb)
            bars.append(Rectangle(width=length, height=0.5, stroke_width=0, fill_color=col, fill_opacity=0.9)
                        .move_to([-3.6 + length / 2, yy - 0.15, 0]))
        l_ax = T("how tightly it binds the enzyme", 26, GREY).move_to([0.5, -2.75, 0])
        self.until("drugs shaped", 0.2)
        drug_home = items[0].get_center()
        items[0].shift(UP * 1.5)
        self.play(Create(cups[0]), FadeIn(items[0]), FadeIn(lbls[0]), run_time=1.0)
        self.until("exploit that tight fit", 0.2)
        self.play(items[0].animate.move_to(drug_home), run_time=0.8, rate_func=rate_functions.ease_in_quad)
        self.play(Indicate(cups[0], color=BLUE, scale_factor=1.12), run_time=0.6)
        self.until("binding far harder", 0.2)
        self.play(GrowFromEdge(bars[0], LEFT), FadeIn(l_ax), run_time=1.1)
        self.until("than substrate mimics", 0.3)
        self.play(Create(cups[1]), FadeIn(items[1]), FadeIn(lbls[1]), GrowFromEdge(bars[1], LEFT), run_time=0.8)
        far = T("far tighter", 30, PURPLE).move_to([4.6, rows_y[0] - 0.15, 0])
        self.play(FadeIn(far), run_time=0.4)

        # ---- the enzyme's job, in one line (the comparison stays up through "The enzyme's job, in one line:")
        self.until("bind the transition state", 0.5)
        self.play(FadeOut(VGroup(*cups, *items, *lbls, *bars, l_ax, far)), FadeOut(tags), run_time=0.6)
        line = T("Bind the transition state\ntighter than the substrate.", 46, TEXT, font=TITLE_FONT,
                 t2c={"transition state": PURPLE, "substrate": YELLOW}, line_spacing=0.9)
        fit(line, max_w=11.5)
        self.play(Write(line), run_time=1.6)
        self.finish()
