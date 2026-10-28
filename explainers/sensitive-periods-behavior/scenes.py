"""Sensitive periods in behavior: windows are tides, not doors  (Biochemistrypedia explainer)

Timed to the SPOKEN words: every self.at("...") cue waits for that phrase in audio/words.json.

COLOR MAP (one color per concept, whole video)
  TEAL   = the window: how open the young nervous system is to experience (curves, gauges, scores)
  YELLOW = experience that arrives: song heard, patterned light, a tutor
  PURPLE = the memory of the tutor song
  BLUE   = the young bird and its own practice singing
  GREEN  = a normal or good outcome (wild song, native-like scores, a check mark)
  RED    = an abnormal or impaired outcome, or something crossed out
  GREY   = structure, axes, the door, de-emphasized things
"""
import numpy as np
from bp_style import *  # noqa: F401,F403

PURPLE = "#B58CD9"


# ---------------------------------------------------------------------------------------------
# helpers
# ---------------------------------------------------------------------------------------------
def bird(scale=1.0, color=BLUE):
    """A sparrow from simple shapes, facing right."""
    body = Ellipse(width=1.5, height=0.95, stroke_color=color, stroke_width=4, fill_color=color, fill_opacity=0.28)
    head = Circle(radius=0.34, stroke_color=color, stroke_width=4, fill_color=color, fill_opacity=0.28).move_to([0.62, 0.42, 0])
    beak = Polygon([0.93, 0.5, 0], [1.28, 0.4, 0], [0.93, 0.32, 0], stroke_color=YELLOW, stroke_width=3,
                   fill_color=YELLOW, fill_opacity=0.9)
    tail = Polygon([-0.65, 0.1, 0], [-1.4, 0.35, 0], [-1.3, -0.05, 0], stroke_color=color, stroke_width=4,
                   fill_color=color, fill_opacity=0.28)
    eye = Dot([0.72, 0.48, 0], radius=0.05, color=TEXT)
    legs = VGroup(Line([-0.1, -0.45, 0], [-0.1, -0.8, 0], color=color, stroke_width=4),
                  Line([0.2, -0.45, 0], [0.2, -0.8, 0], color=color, stroke_width=4))
    return VGroup(tail, body, head, beak, eye, legs).scale(scale)


def wave(x0, y, L, fn, color, amp=0.4, w=4):
    return ParametricFunction(lambda t: np.array([x0 + t, y + amp * fn(t), 0]), t_range=[0, L, 0.03],
                              color=color, stroke_width=w)


def rich(t):
    return (0.55 + 0.45 * np.sin(2.1 * t)) * np.sin(9.0 * t) + 0.25 * np.sin(23 * t + 1)


def simple(t):
    return 0.55 * np.sin(7.0 * t)


def rambling(t):
    return 0.8 * np.sin(5.0 * t + 0.8) * np.cos(17 * t) + 0.35 * np.sin(31 * t + 2) + 0.2 * np.sin(2.3 * t)


def check(at, color=GREEN, s=0.2):
    c = VMobject(stroke_color=color, stroke_width=7)
    c.set_points_as_corners([[-s, 0, 0], [-s * 0.3, -s * 0.75, 0], [s * 1.1, s * 0.9, 0]])
    return c.move_to(at)


def cross(at, color=RED, s=0.2, w=7):
    return VGroup(Line([-s, -s, 0], [s, s, 0], color=color, stroke_width=w),
                  Line([-s, s, 0], [s, -s, 0], color=color, stroke_width=w)).move_to(at)


def axes(x0, y0, w, h):
    return VGroup(Line([x0, y0, 0], [x0 + w, y0, 0], color=GREY, stroke_width=3),
                  Line([x0, y0, 0], [x0, y0 + h, 0], color=GREY, stroke_width=3))


def bell(t, c=0.45, s=0.17):
    return float(np.exp(-((t - c) / s) ** 2))


def door_f(t):
    return 1.0 if 0.3 < t < 0.62 else 0.04


def curve_mob(x0, y0, w, h, f, color=TEAL, sw=6, n=140, dashed=False):
    pts = [[x0 + (i / n) * w, y0 + 0.08 + f(i / n) * (h - 0.2), 0] for i in range(n + 1)]
    m = VMobject(stroke_color=color, stroke_width=sw).set_points_as_corners(pts)
    return DashedVMobject(m, num_dashes=40) if dashed else m


class S00Title(TitleCard):
    LESSON = "Sensitive periods in behavior"
    TITLE = "Windows need not be doors"


# ---------------------------------------------------------------------------------------------
class S01Sparrow(SpokenScene):
    """sparrow raised without song: simple abnormal song, hearing and syrinx fine, late song does little."""

    def construct(self):
        chamber = RoundedRectangle(corner_radius=0.25, width=4.4, height=3.1, stroke_color=GREY, stroke_width=3
                                   ).move_to([-3.8, -0.15, 0])
        ch_lbl = T("raised without adult song", 24, GREY).next_to(chamber, DOWN, buff=0.2)
        b = bird(1.0).move_to(chamber.get_center() + DOWN * 0.1)
        adult = wave(-5.9, 2.75, 2.4, rich, YELLOW, 0.3, 4)
        adult_lbl = T("adult song", 24, YELLOW).next_to(adult, RIGHT, buff=0.3)
        ar = DashedVMobject(Line([-4.7, 2.3, 0], [-4.7, 1.5, 0], color=YELLOW, stroke_width=5), num_dashes=5)
        bar = Line([-5.15, 1.42, 0], [-4.25, 1.42, 0], color=YELLOW, stroke_width=8)

        self.at("young sparrow")
        self.play(Create(chamber), FadeIn(b), FadeIn(ch_lbl), run_time=1.0)
        self.at("never hears")
        self.play(Create(adult), FadeIn(adult_lbl), Create(ar), Create(bar), run_time=0.9)

        X0 = 1.0
        wild = wave(X0, 2.1, 4.9, rich, GREEN, 0.4, 5)
        wild_lbl = T("wild song", 26, GREEN)
        wild_lbl.move_to([X0 + wild_lbl.width / 2, 2.85, 0])
        mine = wave(X0, 0.65, 4.9, simple, RED, 0.4, 5)
        mine_lbl = T("this bird's song: simple, abnormal", 24, RED)
        mine_lbl.move_to([X0 + mine_lbl.width / 2, 1.3, 0])
        self.at("sings anyway")
        self.play(Create(mine), FadeIn(mine_lbl), b.animate.shift(UP * 0.06), run_time=1.0)
        self.at("lacks the detail")
        self.play(Create(wild), FadeIn(wild_lbl), run_time=1.0)

        ck1 = check([1.2, -0.45, 0])
        c1 = chip("hears normally", GREEN, 26)
        c1.move_to([1.55 + c1.width / 2, -0.45, 0])
        ck2 = check([1.2, -1.3, 0])
        c2 = chip("vocal organ works", GREEN, 26)
        c2.move_to([1.55 + c2.width / 2, -1.3, 0])
        self.at("not deaf")
        self.play(FadeIn(c1), Create(ck1), run_time=0.5)
        self.at("vocal organ works")
        self.play(FadeIn(c2), Create(ck2), run_time=0.5)

        self.at("Play it the right song")
        self.play(FadeOut(adult_lbl), FadeOut(bar), FadeOut(ar), adult.animate.move_to([-4.7, 2.75, 0]), run_time=0.5)
        late = T("the right song, later", 24, YELLOW)
        late.next_to(adult, RIGHT, buff=0.25)
        ar2 = Arrow([-4.7, 2.3, 0], [-4.7, 1.2, 0], color=YELLOW, buff=0, stroke_width=6, tip_length=0.22)
        self.play(FadeIn(late), GrowArrow(ar2), run_time=0.7)
        little = T("little change", 26, GREY).move_to([5.2, -0.55, 0])
        self.at("does little")
        self.play(FadeIn(little), Indicate(mine, color=RED, scale_factor=1.0), run_time=0.8)

        q = T("What did it miss?", 38, font=TITLE_FONT).move_to([3.4, -2.6, 0])
        self.at("What did it miss")
        self.play(FadeOut(little), FadeIn(q, shift=UP * 0.15), run_time=0.7)
        self.finish()


# ---------------------------------------------------------------------------------------------
class S02Window(SpokenScene):
    """one window with an experience arrow, then door-shaped vs tide-shaped windows."""

    def until(self, phrase, margin=0.5, cap=3.0):
        return max(0.4, min(cap, self.t_of(phrase) - self.elapsed() - margin))

    def construct(self):
        # beat 1: one window, experience arriving at the right age
        ax = axes(-3.5, -1.4, 7.0, 3.3)
        yl = T("susceptibility", 24, GREY).move_to([-3.5 + 1.0, 2.15, 0])
        xl = T("age", 24, GREY).move_to([3.7, -1.7, 0])
        win = curve_mob(-3.5, -1.4, 7.0, 3.3, lambda t: bell(t, 0.45, 0.2))
        pk = [-3.5 + 0.45 * 7.0, -1.4 + 0.08 + 3.1, 0]
        exp = chip("experience", YELLOW, 28).move_to([pk[0], 3.1, 0])
        arrow = Arrow(exp.get_bottom(), [pk[0], pk[1] + 0.12, 0], color=YELLOW, buff=0.05, stroke_width=6, tip_length=0.22)
        self.at("missed an experience")
        self.play(Create(ax), FadeIn(yl), FadeIn(xl), Create(win), run_time=1.3)
        self.play(FadeIn(exp, shift=DOWN * 0.2), GrowArrow(arrow), run_time=0.7)
        self.at("window of development")
        self.play(Indicate(win, color=TEAL, scale_factor=1.03), run_time=0.8)

        # beat 2: two shapes
        self.at("How sharp is that window")
        self.play(FadeOut(VGroup(ax, yl, xl, win, exp, arrow)), run_time=0.6)
        lx, rx = -3.4, 3.4
        pw, ph, y0 = 5.0, 3.0, -0.7
        axl = axes(lx - pw / 2, y0, pw, ph)
        axr = axes(rx - pw / 2, y0, pw, ph)
        age_l = T("age", 22, GREY).move_to([lx + pw / 2 - 0.1, y0 - 0.3, 0])
        age_r = T("age", 22, GREY).move_to([rx + pw / 2 - 0.1, y0 - 0.3, 0])
        sus_l = T("susceptibility", 22, GREY).move_to([lx - pw / 2 + 0.95, y0 + ph + 0.25, 0])
        sus_r = T("susceptibility", 22, GREY).move_to([rx - pw / 2 + 0.95, y0 + ph + 0.25, 0])
        self.play(Create(axl), Create(axr), FadeIn(age_l), FadeIn(age_r), FadeIn(sus_l), FadeIn(sus_r), run_time=0.9)

        crit = T("critical period", 32, TEAL, weight=BOLD).move_to([lx, 3.15, 0])
        sens = T("sensitive period", 32, TEAL, weight=BOLD).move_to([rx, 3.15, 0])
        pts = [[lx - pw / 2, y0 + 0.08, 0], [lx - pw / 2 + 0.3 * pw, y0 + 0.08, 0], [lx - pw / 2 + 0.3 * pw, y0 + ph - 0.12, 0],
               [lx - pw / 2 + 0.62 * pw, y0 + ph - 0.12, 0], [lx - pw / 2 + 0.62 * pw, y0 + 0.08, 0], [lx + pw / 2, y0 + 0.08, 0]]
        cl = VMobject(stroke_color=TEAL, stroke_width=6).set_points_as_corners(pts)
        self.at("A critical period")
        self.play(FadeIn(crit, shift=DOWN * 0.1), Create(cl), run_time=1.0)

        tr1 = ValueTracker(0.0)
        dx, dy = lx - 1.2, -2.4
        frame = Rectangle(width=0.95, height=1.5, stroke_color=GREY, stroke_width=3).move_to([dx, dy, 0])
        panel = always_redraw(lambda: Rectangle(
            width=max(0.06, 0.85 * (1 - door_f(tr1.get_value()))), height=1.4, stroke_width=0,
            fill_color=GREY, fill_opacity=0.7).move_to([dx - 0.425 + max(0.06, 0.85 * (1 - door_f(tr1.get_value()))) / 2, dy, 0]))
        d_lbl = T("door", 28, GREY).move_to([dx + 1.3, dy, 0])
        dot1 = always_redraw(lambda: Dot([lx - pw / 2 + tr1.get_value() * pw,
                                          y0 + 0.08 + door_f(tr1.get_value()) * (ph - 0.2), 0], radius=0.11, color=TEXT))
        self.at("like a door")
        self.play(FadeIn(frame), FadeIn(panel), FadeIn(d_lbl), FadeIn(dot1), run_time=0.4)
        self.play(tr1.animate.set_value(1.0), run_time=self.until("A sensitive period", 0.6, 3.5), rate_func=linear)
        self.play(FadeOut(dot1), run_time=0.2)

        sl = curve_mob(rx - pw / 2, y0, pw, ph, lambda t: bell(t, 0.46, 0.2))
        self.at("A sensitive period")
        self.play(FadeIn(sens, shift=DOWN * 0.1), Create(sl), run_time=1.0)
        tr2 = ValueTracker(0.0)
        tx, ty = rx - 1.2, -2.4
        tank = Rectangle(width=1.5, height=1.5, stroke_color=GREY, stroke_width=3).move_to([tx, ty, 0])
        water = always_redraw(lambda: Rectangle(width=1.44, height=0.06 + 1.38 * bell(tr2.get_value(), 0.46, 0.2),
                                                stroke_width=0, fill_color=TEAL, fill_opacity=0.6
                                                ).move_to([tx, ty - 0.75 + 0.03 + (0.06 + 1.38 * bell(tr2.get_value(), 0.46, 0.2)) / 2, 0]))
        t_lbl = T("tide", 28, TEAL).move_to([tx + 1.45, ty, 0])
        dot2 = always_redraw(lambda: Dot([rx - pw / 2 + tr2.get_value() * pw,
                                          y0 + 0.08 + bell(tr2.get_value(), 0.46, 0.2) * (ph - 0.2), 0], radius=0.11, color=TEXT))
        self.at("like a tide")
        self.play(FadeIn(tank), FadeIn(water), FadeIn(t_lbl), FadeIn(dot2), run_time=0.4)
        self.play(tr2.animate.set_value(1.0), run_time=self.until("Most of the windows", 0.6, 3.5), rate_func=linear)
        self.play(FadeOut(dot2), run_time=0.2)

        box = SurroundingRectangle(VGroup(sens, sl, axr, age_r), color=TEAL, buff=0.25, corner_radius=0.2, stroke_width=3)
        self.at("Most of the windows")
        self.play(Create(box), run_time=0.8)
        self.finish()


# ---------------------------------------------------------------------------------------------
class S03Song(SpokenScene):
    """listening phase, practice phase, months apart, deafened in between."""

    def construct(self):
        ty = 2.15
        base = Arrow([-6.0, ty - 0.45, 0], [6.1, ty - 0.45, 0], color=GREY, buff=0, stroke_width=3, tip_length=0.2)
        age = T("age", 22, GREY).move_to([5.85, ty - 0.8, 0])
        lb = Rectangle(width=3.6, height=0.55, stroke_color=YELLOW, stroke_width=3, fill_color=YELLOW, fill_opacity=0.2
                       ).move_to([-4.0, ty, 0])
        pb = Rectangle(width=3.6, height=0.55, stroke_color=BLUE, stroke_width=3, fill_color=BLUE, fill_opacity=0.2
                       ).move_to([3.7, ty, 0])
        lb_l = T("listening phase", 28, YELLOW, weight=BOLD).next_to(lb, UP, buff=0.12)
        pb_l = T("practice phase", 28, BLUE, weight=BOLD).next_to(pb, UP, buff=0.12)

        self.at("two phases")
        self.play(Create(base), FadeIn(age), run_time=0.7)
        b = bird(1.15).move_to([2.7, 0.45, 0])
        tutor = wave(-5.9, 0.45, 3.6, rich, YELLOW, 0.4, 5)
        tutor_l = T("tutor song", 24, YELLOW).move_to([-4.1, 1.15, 0])
        self.at("listening phase")
        self.play(FadeIn(lb), FadeIn(lb_l), FadeIn(b), run_time=0.6)
        self.play(Create(tutor), FadeIn(tutor_l), run_time=0.9)
        mem = chip("memory", PURPLE, 26).move_to([-4.7, -0.9, 0])
        mem_w = wave(-2.5, -0.9, 3.4, rich, PURPLE, 0.3, 5)
        self.at("memorizes")
        self.play(FadeIn(mem, shift=UP * 0.1), Create(mem_w), FadeOut(tutor), FadeOut(tutor_l), run_time=1.0)

        own = chip("its own singing", BLUE, 24).move_to([-4.3, -2.4, 0])
        practice = wave(-2.5, -2.4, 3.4, rambling, BLUE, 0.3, 5)
        self.at("practice phase")
        self.play(FadeIn(pb), FadeIn(pb_l), FadeIn(own), Create(practice), run_time=0.9)
        match = wave(-2.5, -2.4, 3.4, rich, BLUE, 0.3, 5)
        self.at("until they match")
        self.play(Transform(practice, match), run_time=1.6)

        gap = DoubleArrow([-2.0, ty, 0], [1.9, ty, 0], color=GREY, buff=0, stroke_width=3, tip_length=0.18)
        months = T("months", 26, GREY).move_to([-0.05, ty + 0.4, 0])
        self.at("months apart")
        self.play(GrowFromCenter(gap), FadeIn(months), run_time=0.7)

        deaf = chip("deafened", RED, 26).move_to([-0.55, 1.2, 0])
        xx = cross([-0.05, ty, 0], RED, 0.22, 8)
        poor = wave(-2.5, -2.4, 3.4, lambda t: 0.5 * np.sin(4.0 * t) + 0.25 * np.sin(13 * t + 2.0), RED, 0.3, 5)
        poor_l = T("very poor song", 26, RED).move_to([2.9, -2.4, 0])
        self.at("deafened between")
        self.play(FadeIn(deaf, shift=DOWN * 0.1), Create(xx), run_time=0.6)
        self.play(Transform(practice, poor), FadeIn(poor_l), run_time=1.0)

        fb = CurvedArrow([1.2, -2.0, 0], [2.3, -0.6, 0], angle=-TAU / 6, color=BLUE, stroke_width=5, tip_length=0.2)
        hear = T("hears itself", 26, BLUE).move_to([4.6, -1.3, 0])
        self.at("hear itself")
        self.play(Create(fb), FadeIn(hear), run_time=0.8)
        self.finish()


# ---------------------------------------------------------------------------------------------
class S04Language(SpokenScene):
    """46 adult learners: grammar score against age of arrival."""

    def construct(self):
        x0, y0, w, h = -5.6, -2.0, 11.2, 3.0
        ax = axes(x0, y0, w, h)
        yl = T("grammar score", 24, GREY).move_to([x0 + 1.1, y0 + h + 0.25, 0])
        xl = T("age of arrival", 24, GREY).move_to([x0 + w / 2, y0 - 0.6, 0])
        t3 = T("3", 22, GREY).move_to([x0 + 0.1, y0 - 0.3, 0])
        t39 = T("39", 22, GREY).move_to([x0 + w - 0.1, y0 - 0.3, 0])
        note = T("illustration, not the real data", 22, GREY).move_to([x0 + w - 2.4, y0 + h + 0.25, 0])

        rng = np.random.RandomState(7)
        ages = np.linspace(3, 39, 46) + rng.uniform(-0.3, 0.3, 46)
        ages = np.clip(ages, 3, 39)
        puberty = 14.0

        def score(a):
            if a <= 8:
                return 0.93 + rng.uniform(-0.025, 0.025)
            base = 0.93 - 0.40 * (1 - np.exp(-(a - 8) / 10.0))
            spread = 0.03 + 0.14 * min(1.0, (a - 8) / 20.0)
            return float(np.clip(base + rng.uniform(-spread, spread), 0.2, 0.95))

        sc = [score(a) for a in ages]
        px = lambda a: x0 + 0.25 + (a - 3) / 36 * (w - 0.5)
        py = lambda s: y0 + 0.1 + s * (h - 0.35)
        grid = VGroup(*[Dot(radius=0.09, color=GREY) for _ in range(46)]).arrange_in_grid(rows=2, cols=23, buff=0.16
                                                                                         ).move_to([-0.6, 2.75, 0])
        n_lbl = T("46 adults", 26, GREY).move_to([5.2, 2.75, 0])
        young = [i for i, a in enumerate(ages) if a <= 8]
        mid = [i for i, a in enumerate(ages) if 8 < a <= puberty]
        late = [i for i, a in enumerate(ages) if a > puberty]

        def fly(idx):
            return [grid[i].animate.move_to([px(ages[i]), py(sc[i]), 0]).set_color(TEAL).scale(1.1) for i in idx]

        self.at("human test")
        self.play(Create(ax), FadeIn(yl), FadeIn(xl), FadeIn(t3), FadeIn(t39), FadeIn(note), run_time=1.2)
        who = T("Johnson and Newport", 40, font=TITLE_FONT).move_to([0, 0.2, 0])
        self.at("Johnson and Newport")
        self.play(FadeIn(who, shift=UP * 0.15), run_time=0.7)
        self.at("adults who moved")
        self.play(FadeOut(who), LaggedStart(*[FadeIn(d, scale=0.3) for d in grid], lag_ratio=0.02), FadeIn(n_lbl), run_time=1.3)
        self.at("between ages")
        self.play(Indicate(t3, color=TEXT, scale_factor=1.5), Indicate(t39, color=TEXT, scale_factor=1.5), run_time=0.9)
        sent = T("each judges: is this English sentence grammatical?", 26, TEXT).move_to([0, 1.95, 0])
        self.at("judged whether")
        self.play(FadeIn(sent, shift=UP * 0.1), run_time=0.6)

        native_y = py(0.93)
        nat = DashedVMobject(Line([x0, native_y, 0], [x0 + w, native_y, 0], color=GREEN, stroke_width=3), num_dashes=40)
        nat_l = T("native speakers", 24, GREEN).move_to([x0 + w - 1.4, native_y + 0.3, 0])
        self.at("scored like native speakers")
        self.play(FadeOut(sent), LaggedStart(*fly(young), lag_ratio=0.1), Create(nat), FadeIn(nat_l), run_time=1.8)

        pub = DashedVMobject(Line([px(puberty), y0, 0], [px(puberty), y0 + h, 0], color=GREY, stroke_width=3), num_dashes=22)
        pub_l = T("about puberty (approximate)", 24, GREY).move_to([px(puberty) + 1.9, y0 + 0.3, 0])
        self.at("fell steadily")
        self.play(LaggedStart(*fly(mid), lag_ratio=0.12), run_time=1.6)
        trend = Line([px(8), py(0.93), 0], [px(puberty), py(0.75), 0], color=TEAL, stroke_width=5)
        self.play(Create(trend), Create(pub), FadeIn(pub_l), run_time=0.7)
        self.at("After that")
        self.play(LaggedStart(*fly(late), lag_ratio=0.08), FadeOut(n_lbl), run_time=1.8)

        step = VMobject(stroke_color=RED, stroke_width=6).set_points_as_corners(
            [[px(3), py(0.93) + 0.12, 0], [px(puberty), py(0.93) + 0.12, 0], [px(puberty), py(0.3), 0], [px(39), py(0.3), 0]])
        step = DashedVMobject(step, num_dashes=44)
        self.at("That does")
        self.play(Indicate(trend, color=TEAL, scale_factor=1.0), run_time=0.8)
        self.at("door shutting")
        self.play(Create(step), run_time=0.8)
        xx = cross([px(puberty), py(0.6), 0], RED, 0.3, 9)
        self.play(Create(xx), run_time=0.3)

        self.at("still debated")
        self.play(FadeOut(step), FadeOut(xx), run_time=0.4)
        cs = [chip("change in plasticity", TEAL, 24), chip("entrenched first language", TEAL, 24),
              chip("differences in input", YELLOW, 24)]
        row = VGroup(*cs).arrange(RIGHT, buff=0.3).move_to([0.5, 2.75, 0])
        q = T("?", 44, TEXT, weight=BOLD).next_to(row, LEFT, buff=0.3)
        self.play(LaggedStart(*[FadeIn(c, shift=UP * 0.1) for c in cs], lag_ratio=0.3), FadeIn(q), run_time=1.4)
        self.finish()


# ---------------------------------------------------------------------------------------------
class S05Sight(SpokenScene):
    """preferential looking, cataract eye, 28 infants, acuity after treatment."""

    def construct(self):
        # beat 1: where do babies look
        sq_l = Rectangle(width=3.2, height=3.2, stroke_color=GREY, stroke_width=3).move_to([-1.75, 0.9, 0])
        stripes = VGroup(*[Rectangle(width=0.22, height=3.0, stroke_width=0, fill_color=YELLOW, fill_opacity=0.9
                                     ).move_to([-1.75 - 1.26 + 0.21 * 1.0 + i * 0.42, 0.9, 0]) for i in range(7)])
        sq_r = Rectangle(width=3.2, height=3.2, stroke_color=GREY, stroke_width=3, fill_color=GREY, fill_opacity=0.3
                         ).move_to([1.75, 0.9, 0])
        eyeb = Dot([0.0, -2.2, 0], radius=0.2, color=BLUE)
        gaze = Arrow([-0.1, -1.95, 0], [-1.3, -0.85, 0], color=BLUE, buff=0, stroke_width=5, tip_length=0.24)
        gaze_l = T("where the baby looks", 28, BLUE).move_to([3.4, -2.2, 0])
        self.at("Babies cannot tell us")
        self.play(Create(sq_l), Create(sq_r), run_time=0.7)
        self.play(FadeIn(stripes), FadeIn(eyeb), run_time=0.6)
        self.at("watch where they look")
        self.play(GrowArrow(gaze), FadeIn(gaze_l), run_time=0.8)

        # beat 2: the eye with a cataract
        ec = np.array([-2.7, 1.2, 0])
        R = 1.7
        grat = VGroup(*[Rectangle(width=0.14, height=1.5, stroke_width=0, fill_color=YELLOW, fill_opacity=0.95
                                  ).move_to([-6.1 + i * 0.28, ec[1], 0]) for i in range(5)])
        eye = Circle(radius=R, stroke_color=GREY, stroke_width=4).move_to(ec)
        retina = Arc(radius=R, start_angle=-PI / 3, angle=2 * PI / 3, color=GREY, stroke_width=10).move_arc_center_to(ec)
        lens = Ellipse(width=0.45, height=1.8, stroke_color=GREY, stroke_width=4, fill_color=GREY, fill_opacity=0.85
                       ).move_to(ec + LEFT * 0.95)
        lens_l = T("lens", 24, GREY).move_to(ec + LEFT * 0.95 + UP * (R + 0.4))
        rays = VGroup(*[Arrow([-4.95, ec[1] + dy, 0], lens.get_left() + [-0.05, dy * 0.55, 0], color=YELLOW,
                              buff=0, stroke_width=3, tip_length=0.14) for dy in (-0.6, 0, 0.6)])
        self.at("dense cataracts")
        self.play(FadeOut(VGroup(sq_l, sq_r, eyeb, gaze, gaze_l, stripes)), run_time=0.6)
        self.play(FadeIn(grat), Create(eye), Create(retina), FadeIn(lens), FadeIn(lens_l), run_time=0.9)
        self.play(GrowFromCenter(rays), run_time=0.5)
        glow = Ellipse(width=1.2, height=2.4, stroke_width=0, fill_color=YELLOW, fill_opacity=0.28).move_to(ec + RIGHT * 0.95)
        no_pat = T("no pattern", 26, YELLOW).move_to(ec + DOWN * (R + 0.4))
        self.at("no pattern does")
        self.play(FadeIn(glow), FadeIn(no_pat), run_time=0.8)
        clear = Ellipse(width=0.45, height=1.8, stroke_color=GREY, stroke_width=4, fill_opacity=0).move_to(lens)
        bars = VGroup(*[Rectangle(width=0.12, height=1.6, stroke_width=0, fill_color=YELLOW, fill_opacity=0.95
                                  ).move_to(ec + [0.95 + i * 0.26, 0, 0]) for i in range(-1, 2)])
        self.at("until the lens is removed")
        self.play(Transform(lens, clear), FadeOut(glow), FadeOut(no_pat), FadeIn(bars), run_time=1.0)

        # beat 3: 28 infants, acuity after treatment
        dots = VGroup(*[Dot(radius=0.09, color=BLUE) for _ in range(28)]).arrange_in_grid(rows=2, cols=14, buff=0.16
                                                                                         ).move_to([-3.1, -1.6, 0])
        d_lbl = T("28 infants", 28, BLUE).move_to([-3.1, -2.6, 0])
        self.at("followed")
        self.play(LaggedStart(*[FadeIn(d, scale=0.3) for d in dots], lag_ratio=0.03), FadeIn(d_lbl), run_time=1.3)

        px0, py0, pw, ph = 1.0, -0.7, 5.2, 3.4
        pax = axes(px0, py0, pw, ph)
        y_l = T("acuity", 24, GREY).move_to([px0 + 0.6, py0 + ph + 0.25, 0])
        t_l = T("time after treatment", 22, GREY).move_to([px0 + pw / 2, py0 - 0.7, 0])
        nb_y = py0 + 0.6
        nb = DashedVMobject(Line([px0, nb_y, 0], [px0 + pw, nb_y, 0], color=GREY, stroke_width=3), num_dashes=24)
        nb_l = T("newborn", 24, GREY).move_to([px0 + pw - 0.9, nb_y - 0.3, 0])
        start = Dot([px0, nb_y, 0], radius=0.11, color=TEAL)
        self.at("Right after treatment")
        self.play(Create(pax), FadeIn(y_l), FadeIn(t_l), Create(nb), FadeIn(nb_l), FadeIn(start), run_time=1.2)

        amp = ph - 1.4
        pts = lambda a, b: [[px0 + t * pw, nb_y + amp * (0.5 * (1 - np.exp(-5.5 * t)) + 0.5 * (1 - np.exp(-2.2 * t))) * 0.9, 0]
                            for t in np.linspace(a, b, 40)]
        c1 = VMobject(stroke_color=TEAL, stroke_width=6).set_points_as_corners(pts(0.0, 0.1))
        tick_h = T("an hour", 22, GREY).move_to([px0 + 0.1 * pw + 0.2, py0 - 0.3, 0])
        self.at("as little as an hour")
        self.play(Create(c1), FadeIn(tick_h), run_time=0.8)
        c2 = VMobject(stroke_color=TEAL, stroke_width=6).set_points_as_corners(pts(0.1, 1.0))
        pat = chip("patterned input", YELLOW, 24).move_to([px0 + 1.75, py0 + ph - 0.45, 0])
        self.at("patterned input")
        self.play(Create(c2), FadeIn(pat), run_time=1.4)

        self.at("Yet some functions")
        self.play(FadeOut(pat), run_time=0.3)
        red_l = T("lasting deficits in some functions", 24, RED).move_to([px0 + pw / 2, py0 - 1.4, 0])
        f1 = chip("fine acuity", RED, 22, pad=0.16)
        f2 = chip("spacing of facial features", RED, 22, pad=0.16)
        row = VGroup(f1, f2).arrange(RIGHT, buff=0.2).move_to([3.25, py0 - 2.15, 0])
        self.play(FadeIn(red_l), run_time=0.4)
        self.at("fine acuity")
        self.play(FadeIn(f1, shift=UP * 0.1), run_time=0.4)
        self.at("spacing of facial features")
        self.play(FadeIn(f2, shift=UP * 0.1), run_time=0.4)
        self.finish()


# ---------------------------------------------------------------------------------------------
class S06Rule(SpokenScene):
    """experience helps close the window; genes and experience; door crossed out, tide kept."""

    def construct(self):
        x0, y0, w, h = -5.6, -1.2, 11.2, 3.7
        ax = axes(x0, y0, w, h)
        xl = T("age", 24, GREY).move_to([x0 + w - 0.3, y0 - 0.35, 0])
        yl = T("able to learn from a tutor", 24, GREY)
        yl.move_to([x0 + w - yl.width / 2 - 0.1, y0 + h + 0.25, 0])
        a = curve_mob(x0, y0, w, h, lambda t: bell(t, 0.3, 0.14), TEAL)
        nt = lambda t: bell(t, 0.3, 0.14) if t <= 0.3 else (1.0 if t < 0.5 else float(np.exp(-((t - 0.5) / 0.16) ** 2)))
        pts_b = [[x0 + t * w, y0 + 0.08 + nt(t) * (h - 0.2), 0] for t in np.linspace(0.3, 1.0, 90)]
        b = DashedVMobject(VMobject(stroke_color=TEAL, stroke_width=6).set_points_as_corners(pts_b), num_dashes=40)
        tag = T("zebra finch, illustration", 22, GREY).move_to([4.2, 0.85, 0])
        # legend (right of both curves)
        lg1 = Line([1.9, 2.0, 0], [2.5, 2.0, 0], color=TEAL, stroke_width=6)
        lg1_l = T("raised with a tutor", 24, TEAL)
        lg1_l.move_to([2.7 + lg1_l.width / 2, 2.0, 0])
        lg2 = DashedVMobject(Line([1.9, 1.4, 0], [2.5, 1.4, 0], color=TEAL, stroke_width=6), num_dashes=4)
        lg2_l = T("raised without a tutor", 24, TEAL)
        lg2_l.move_to([2.7 + lg2_l.width / 2, 1.4, 0])

        self.at("Experience does more")
        self.play(Create(ax), FadeIn(xl), FadeIn(yl), Create(a), FadeIn(lg1), FadeIn(lg1_l), run_time=1.4)
        tut = chip("tutor heard", YELLOW, 24).move_to([x0 + 1.4, y0 + h - 0.4, 0])
        cx = x0 + 0.2 * w
        cy = y0 + 0.08 + bell(0.2, 0.3, 0.14) * (h - 0.2)
        tut_ar = Arrow(tut.get_bottom(), [cx, cy + 0.1, 0], color=YELLOW, buff=0.05, stroke_width=5, tip_length=0.2)
        self.at("zebra finches")
        self.play(FadeIn(tut), GrowArrow(tut_ar), run_time=0.8)
        self.at("delayed in birds raised without")
        self.play(Create(b), FadeIn(lg2), FadeIn(lg2_l), FadeIn(tag), a.animate.set_stroke(opacity=0.45), run_time=1.6)
        self.at("suggests")
        self.play(Indicate(tut, color=YELLOW, scale_factor=1.1), run_time=0.8)

        g = chip("genes: build the circuit", GREY, 24).move_to([-3.0, -2.7, 0])
        e = chip("experience: what and when", YELLOW, 24).move_to([3.2, -2.7, 0])
        self.at("Genes build the circuit")
        self.play(FadeIn(g, shift=UP * 0.1), run_time=0.6)
        self.at("and experience")
        self.play(FadeIn(e, shift=UP * 0.1), run_time=0.6)

        self.at("Keep this rule")
        self.play(FadeOut(VGroup(ax, xl, yl, a, b, tag, lg1, lg1_l, lg2, lg2_l, tut, tut_ar, g, e)), run_time=0.7)
        door = VGroup(Rectangle(width=2.0, height=3.2, stroke_color=GREY, stroke_width=4),
                      Rectangle(width=1.9, height=3.1, stroke_width=0, fill_color=GREY, fill_opacity=0.5)).move_to([-3.4, 0.4, 0])
        door_l = T("door", 36, GREY).move_to([-3.4, -1.8, 0])
        tank = Rectangle(width=3.2, height=3.2, stroke_color=GREY, stroke_width=4).move_to([3.4, 0.4, 0])
        tide_l = T("tide", 36, TEAL).move_to([3.4, -1.8, 0])
        tr = ValueTracker(0.0)
        wlev = lambda v: 0.5 + 1.7 * (0.5 - 0.5 * np.cos(v * TAU * 0.75))
        water = always_redraw(lambda: Rectangle(width=3.1, height=wlev(tr.get_value()), stroke_width=0, fill_color=TEAL,
                                                fill_opacity=0.6).move_to([3.4, -1.2 + wlev(tr.get_value()) / 2, 0]))
        self.play(FadeIn(door), FadeIn(door_l), FadeIn(tank), FadeIn(water), FadeIn(tide_l), run_time=0.6)
        self.at("tides")
        self.play(tr.animate.set_value(1.0), run_time=self.until("not doors", 0.2, 3.0), rate_func=linear)
        xx = cross(door.get_center(), RED, 1.0, 10)
        self.at("not doors")
        self.play(Create(xx), run_time=0.6)
        self.finish()

    def until(self, phrase, margin=0.5, cap=3.0):
        return max(0.4, min(cap, self.t_of(phrase) - self.elapsed() - margin))


class S07End(EndCard):
    LINE = "Most windows here are tides, not doors."
