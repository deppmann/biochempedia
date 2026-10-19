"""Proprioception: position is an estimate  (Biochemistrypedia explainer)

COLOR MAP (one color per concept, whole video)
  YELLOW = the stimulus: vibration, stretch
  BLUE   = primary (Ia) spindle endings
  PURPLE = secondary (II) spindle endings
  GREEN  = Piezo2 and its current
  ORANGE = the felt / computed limb-position estimate
  RED    = wrong claim, deletion, deficit
  GREY   = structure, outlines, de-emphasized
"""
import numpy as np
from bp_style import *  # noqa: F401,F403

PURPLE = "#B58CD9"
ORANGE = "#F29E4C"


def arr(a, b, color=GREY, w=5, tip=0.22):
    return Arrow(a, b, buff=0.08, color=color, stroke_width=w, tip_length=tip,
                 max_tip_length_to_length_ratio=0.45, max_stroke_width_to_length_ratio=12)


def darr(a, b, color=GREY, w=4):
    """modulatory / uncertain: dashed arrow."""
    a, b = np.array(a, float), np.array(b, float)
    d = (b - a) / np.linalg.norm(b - a)
    ln = DashedLine(a, b - d * 0.2, color=color, stroke_width=w, dash_length=0.18)
    tip = Triangle(fill_color=color, fill_opacity=1, stroke_width=0).scale(0.12)
    tip.rotate(np.arctan2(d[1], d[0]) - PI / 2).move_to(b - d * 0.1)
    return VGroup(ln, tip)


def pol(center, ang_deg, length):
    a = np.radians(ang_deg)
    return np.array(center) + length * np.array([np.cos(a), np.sin(a), 0])


def bone(a, b, color, w=16, dashed=False):
    if dashed:
        return DashedLine(a, b, color=color, stroke_width=w, dash_length=0.3)
    return Line(a, b, color=color, stroke_width=w)


class S00Title(TitleCard):
    LESSON = "Proprioception"
    TITLE = "Position Is an Estimate"


# ---------------------------------------------------------------------------------------------
class S01Illusion(SpokenScene):
    def construct(self):
        S_ = np.array([-5.8, -1.9, 0]); E = np.array([-1.6, -1.9, 0])
        TRUE, FELT, L = 70, 30, 4.4
        tip_t, tip_f = pol(E, TRUE, L), pol(E, FELT, L)
        upper = bone(S_, E, GREY)
        fore = bone(E, tip_t, GREY)
        hand = Circle(radius=0.28, stroke_color=GREY, stroke_width=4, fill_color=GREY, fill_opacity=0.35).move_to(tip_t)
        joint = Circle(radius=0.2, stroke_color=TEXT, stroke_width=3, fill_color=BG, fill_opacity=1).move_to(E)
        arm = VGroup(upper, fore, hand, joint)
        tl = T("true forearm position", 26, GREY).next_to(tip_t, UP, buff=0.3).shift(RIGHT * 0.3)
        eyes = chip("eyes closed", GREY, size=26).move_to([-4.6, 1.6, 0])
        self.at("close your eyes")
        self.play(FadeIn(arm), FadeIn(eyes), run_time=0.8)
        self.play(FadeIn(tl), run_time=0.4)

        # vibrator on biceps tendon (upper arm, near the elbow, on the flexor side)
        vib = RoundedRectangle(corner_radius=0.1, width=1.0, height=0.5, stroke_color=YELLOW, stroke_width=3,
                               fill_color=YELLOW, fill_opacity=0.35).move_to([-3.1, -1.62, 0])
        waves = VGroup(*[Arc(radius=0.35 + 0.28 * i, start_angle=PI / 4, angle=PI / 2, arc_center=[-3.1, -1.37, 0],
                             color=YELLOW, stroke_width=3) for i in range(3)])
        vlab = T("vibrator on biceps\ntendon, 100 Hz", 26, YELLOW).move_to([-3.6, 0.1, 0])
        vln = Line(vlab.get_bottom() + DOWN * 0.05, vib.get_top() + UP * 0.9, color=YELLOW, stroke_width=2)
        self.at("vibrator on your biceps")
        self.play(FadeIn(vib), FadeIn(vlab), run_time=0.5)
        self.play(LaggedStart(*[Create(w) for w in waves], lag_ratio=0.3), run_time=0.9)
        self.play(Indicate(waves, color=YELLOW, scale_factor=1.15), run_time=0.8)

        # the felt position
        felt_fore = bone(E, tip_f, ORANGE, dashed=True)
        felt_hand = Circle(radius=0.28, stroke_color=ORANGE, stroke_width=4, fill_color=ORANGE, fill_opacity=0.25).move_to(tip_f)
        fl = T("felt position", 26, ORANGE).next_to(tip_f, RIGHT, buff=0.55)
        self.at("misjudge where your elbow")
        ghost = VGroup(bone(E, tip_t, ORANGE, dashed=True), Circle(radius=0.28, stroke_color=ORANGE, stroke_width=4,
                       fill_color=ORANGE, fill_opacity=0.25).move_to(tip_t))
        self.add(ghost)
        self.play(Transform(ghost, VGroup(felt_fore, felt_hand)), run_time=1.6)
        self.play(FadeIn(fl), run_time=0.4)
        self.at("has not moved")
        self.play(Indicate(VGroup(fore, hand, tl), color=TEXT, scale_factor=1.05), run_time=0.9)

        # the angle
        arc = Arc(radius=2.6, start_angle=np.radians(FELT), angle=np.radians(TRUE - FELT), arc_center=E, color=ORANGE, stroke_width=5)
        al = M("up to 40°", 26, ORANGE).move_to(pol(E, 50, 3.55))
        sub = T("in one experiment, while the muscle contracted", 24, GREY).to_edge(DOWN, buff=0.55)
        self.at("error reached")
        self.play(Create(arc), FadeIn(al), run_time=0.9)
        self.play(FadeIn(sub), run_time=0.4)

        ban = T("limb position: a computed estimate", 34, ORANGE, font=TITLE_FONT).to_edge(UP, buff=0.45)
        self.at("computed estimate")
        self.play(Write(ban), run_time=1.0)
        self.finish()


# ---------------------------------------------------------------------------------------------
class S02Spindle(SpokenScene):
    def construct(self):
        # many afferents -> one estimate
        ys = np.linspace(-2.2, 2.2, 6)
        cells = VGroup(*[Circle(radius=0.26, stroke_color=GREY, stroke_width=3, fill_color=GREY, fill_opacity=0.3).move_to([-5, y, 0]) for y in ys])
        est = chip("limb position\nestimate", ORANGE, size=30).move_to([2.6, 0, 0])
        links = VGroup(*[arr([-4.6, y, 0], est.get_left() + LEFT * 0.0 + UP * (y * 0.12), GREY, w=3, tip=0.16) for y in ys])
        many = T("many afferents", 28, GREY).next_to(cells, DOWN, buff=0.3).shift(RIGHT * 0.2)
        self.at("populations of afferents")
        self.play(LaggedStart(*[FadeIn(c, scale=0.7) for c in cells], lag_ratio=0.12), run_time=1.2)
        self.play(FadeIn(est), LaggedStart(*[GrowArrow(l) for l in links], lag_ratio=0.1), FadeIn(many), run_time=1.4)
        self.at("muscle spindle")
        self.play(FadeOut(VGroup(cells, links, est, many)), run_time=0.6)

        # spindle
        cap = RoundedRectangle(corner_radius=0.7, width=8.4, height=1.7, stroke_color=GREY, stroke_width=4,
                               fill_color=GREY, fill_opacity=0.12).move_to([-1.2, 2.1, 0])
        fib = VGroup(Line([-5.0, 2.35, 0], [2.6, 2.35, 0], color=GREY, stroke_width=3),
                     Line([-5.0, 1.85, 0], [2.6, 1.85, 0], color=GREY, stroke_width=3))
        e1 = Ellipse(width=1.1, height=1.55, stroke_color=BLUE, stroke_width=5, fill_color=BLUE, fill_opacity=0.3).move_to([-2.6, 2.1, 0])
        e2 = Ellipse(width=1.1, height=1.55, stroke_color=PURPLE, stroke_width=5, fill_color=PURPLE, fill_opacity=0.3).move_to([0.5, 2.1, 0])
        ax1 = VMobject(color=BLUE, stroke_width=4).set_points_as_corners([[-2.6, 2.9, 0], [-2.6, 3.35, 0], [4.8, 3.35, 0]])
        ax2 = VMobject(color=PURPLE, stroke_width=4).set_points_as_corners([[0.5, 1.3, 0], [0.5, 0.85, 0], [4.8, 0.85, 0]])
        n1 = chip("Ia", BLUE, size=28).move_to([5.7, 3.35, 0])
        n2 = chip("II", PURPLE, size=28).move_to([5.7, 0.85, 0])
        slab = T("muscle spindle", 26, GREY).move_to([-1.2, 0.95, 0])
        slab.shift(LEFT * 3.0 + DOWN * 0.1)
        self.play(FadeIn(cap), Create(fib), run_time=0.8)
        self.play(FadeIn(slab), run_time=0.3)
        self.at("two sensory endings")
        self.play(FadeIn(e1, scale=0.8), Create(ax1), FadeIn(n1), run_time=0.9)
        self.play(FadeIn(e2, scale=0.8), Create(ax2), FadeIn(n2), run_time=0.9)

        # rows
        rowA = VGroup(chip("Ia", BLUE, size=26), chip("static length", BLUE, size=26), chip("rate of change: more", BLUE, size=26)).arrange(RIGHT, buff=0.4)
        rowB = VGroup(chip("II", PURPLE, size=26), chip("static length", PURPLE, size=26), chip("rate of change: less", PURPLE, size=26)).arrange(RIGHT, buff=0.4)
        rows = VGroup(rowA, rowB).arrange(DOWN, buff=0.4, aligned_edge=LEFT).move_to([0, -0.9, 0])
        rows.shift(LEFT * 0.0)
        self.at("static muscle length")
        self.play(FadeIn(rowA[0]), FadeIn(rowB[0]), FadeIn(rowA[1], shift=RIGHT * 0.2), FadeIn(rowB[1], shift=RIGHT * 0.2), run_time=0.9)
        self.at("rate of change")
        self.play(FadeIn(rowA[2], shift=RIGHT * 0.2), run_time=0.6)
        self.play(FadeIn(rowB[2], shift=RIGHT * 0.2), run_time=0.6)
        myth = chip("Ia = velocity, II = position", GREY, size=28).move_to([0, -3.0, 0])
        self.at("old rule")
        self.play(FadeIn(myth, shift=UP * 0.2), run_time=0.6)
        cross = Line(myth.get_left() + LEFT * 0.15, myth.get_right() + RIGHT * 0.15, color=RED, stroke_width=7)
        self.at("is wrong")
        self.play(Create(cross), myth.animate.set_opacity(0.6), run_time=0.6)
        self.finish()


# ---------------------------------------------------------------------------------------------
class S03Vibration(SpokenScene):
    def construct(self):
        title = T("human recordings, in the leg of healthy people", 28, GREY).to_edge(UP, buff=0.5)
        self.at("human recordings")
        self.play(FadeIn(title), run_time=0.5)
        # 15 blue + 5 purple endings
        def grid(n, cols, color, origin):
            ds = VGroup(*[Circle(radius=0.3, stroke_color=color, stroke_width=3, fill_color=color, fill_opacity=0.5) for _ in range(n)])
            ds.arrange_in_grid(rows=int(np.ceil(n / cols)), cols=cols, buff=0.25)
            return ds.move_to(origin)
        g1 = grid(15, 5, BLUE, [-3.6, 0.6, 0])
        g2 = grid(5, 5, PURPLE, [3.6, 0.6, 0])
        l1 = T("15 primary endings", 30, BLUE).next_to(g1, DOWN, buff=0.4)
        l2 = T("5 secondary endings", 30, PURPLE).next_to(g2, DOWN, buff=0.4)
        self.at("in the leg")
        self.play(LaggedStart(*[FadeIn(d, scale=0.5) for d in g1], lag_ratio=0.05), LaggedStart(*[FadeIn(d, scale=0.5) for d in g2], lag_ratio=0.08), run_time=1.2)
        self.at("15 primary")
        self.play(FadeIn(l1), run_time=0.4)
        self.at("5 secondary")
        self.play(FadeIn(l2), run_time=0.4)
        note = T("less sensitive to low-amplitude\ntendon vibration", 26, PURPLE).move_to([3.6, -2.35, 0])
        self.at("less sensitive")
        self.play(g2.animate.set_opacity(0.35), FadeIn(note), run_time=0.8)
        self.at("likely carriers")
        self.play(FadeOut(VGroup(title, g1, g2, l1, l2, note)), run_time=0.6)

        # circuit
        b1 = chip("tendon\nvibration", YELLOW, size=28).move_to([-4.6, 0.3, 0])
        b2 = chip("primary\nendings", BLUE, size=28).move_to([-0.3, 0.3, 0])
        b3 = chip("limb position\npercept: biased", ORANGE, size=28).move_to([4.2, 0.3, 0])
        a1 = arr(b1.get_right(), b2.get_left(), GREY)
        a2 = arr(b2.get_right(), b3.get_left(), GREY)
        lik = T("likely carriers", 26, BLUE).next_to(b2, UP, buff=0.35)
        self.play(FadeIn(b1), run_time=0.4)
        self.play(GrowArrow(a1), FadeIn(b2), run_time=0.6)
        self.play(FadeIn(lik), GrowArrow(a2), FadeIn(b3), run_time=0.7)
        other = chip("other afferents?", GREY, size=26).move_to([-0.3, -2.4, 0])
        da = darr(other.get_right() + RIGHT * 0.05, b3.get_bottom() + DOWN * 0.05, GREY)
        no = T("not excluded", 24, GREY).next_to(other, DOWN, buff=0.25)
        self.at("do not show that only")
        self.play(FadeIn(other), FadeIn(no), run_time=0.6)
        self.play(FadeIn(da), run_time=0.6)
        self.finish()


# ---------------------------------------------------------------------------------------------
class S04Channel(SpokenScene):
    def construct(self):
        cell = RoundedRectangle(corner_radius=0.5, width=5.8, height=3.4, stroke_color=GREY, stroke_width=4,
                                fill_color=GREY, fill_opacity=0.1).move_to([-3.3, 1.6, 0])
        clab = T("sensory ending (mouse)", 26, GREY).move_to([-3.3, 2.9, 0])
        mem = RoundedRectangle(corner_radius=0.1, width=5.8, height=0.42, stroke_color=GREY, stroke_width=3,
                               fill_color=GREY, fill_opacity=0.4).move_to([-3.3, -0.1, 0])
        sL = arr([-6.3, -1.2, 0], [-6.3, -1.2, 0] + LEFT * 0.0, YELLOW)  # placeholder removed below
        sL = arr([-5.6, -1.0, 0], [-6.5, -1.0, 0], YELLOW)
        sR = arr([-1.0, -1.0, 0], [-0.1, -1.0, 0], YELLOW)
        slab = T("stretch", 28, YELLOW).move_to([-3.3, -1.0, 0])
        q = chip("?", GREY, size=36).move_to([-3.3, -0.1, 0])
        self.play(FadeIn(cell), FadeIn(clab), FadeIn(mem), run_time=0.6)
        self.play(GrowArrow(sL), GrowArrow(sR), FadeIn(slab), FadeIn(q), run_time=0.8)
        qlab = T("what turns stretch into current?", 26, TEXT).move_to([-3.3, 1.5, 0])
        self.play(FadeIn(qlab), run_time=0.5)
        ch = chip("Piezo2", GREEN, size=28).move_to([-3.3, -0.1, 0])
        self.at("channel called")
        self.play(FadeOut(qlab), Transform(q, ch), run_time=0.8)

        # evidence cards
        c1 = chip("1  Where it is\nreporter: spindle and tendon\norgan endings", GREEN, size=24)
        c2 = chip("2  What current it carries\nrapidly adapting, dissociated\nsensory neurons", GREEN, size=24)
        c3 = chip("3  Whether it is needed\ndeletion: stretch-evoked\nfiring sharply reduced", GREEN, size=24)
        cards = VGroup(c1, c2, c3).arrange(DOWN, buff=0.35)
        for c in cards:
            c.set_width(min(c.width, 5.6)) if False else None
        cards.move_to([3.6, 0.1, 0])
        # ticks
        flab = T("stretch-evoked firing, in this sketch", 24, GREY).move_to([-3.3, -2.2, 0])
        ticks = VGroup(*[Line([x, -2.75, 0], [x, -3.35, 0], color=YELLOW, stroke_width=5) for x in np.linspace(-5.4, -1.2, 8)])
        self.at("three kinds of evidence")
        self.play(FadeIn(flab), Create(ticks), run_time=0.8)
        self.at("where it is")
        self.play(FadeIn(c1, shift=LEFT * 0.2), Indicate(q, color=GREEN, scale_factor=1.15), run_time=0.9)
        cur = arr([-3.3, 0.45, 0], [-3.3, 1.7, 0], GREEN, w=7)
        curl = T("current in", 26, GREEN).move_to([-1.5, 1.1, 0])
        self.at("what current it carries")
        self.play(FadeIn(c2, shift=LEFT * 0.2), GrowArrow(cur), FadeIn(curl), run_time=0.9)
        xmark = VGroup(Line([-3.95, 0.35, 0], [-2.65, -0.55, 0], color=RED, stroke_width=8),
                       Line([-3.95, -0.55, 0], [-2.65, 0.35, 0], color=RED, stroke_width=8))
        self.at("whether the ending needs")
        self.play(FadeIn(c3, shift=LEFT * 0.2), run_time=0.7)
        self.at("deleting it")
        self.play(Create(xmark), FadeOut(cur), FadeOut(curl), q.animate.set_opacity(0.4), run_time=0.7)
        self.play(*[t.animate.set_opacity(0.0) for t in ticks[1:3]] + [t.animate.set_opacity(0.0) for t in ticks[4:6]] +
                  [ticks[7].animate.set_opacity(0.0)], run_time=0.8)
        self.finish()


# ---------------------------------------------------------------------------------------------
class S05Decay(SpokenScene):
    def construct(self):
        # 25 labelled neurons
        dots = VGroup(*[Circle(radius=0.2, stroke_color=GREEN if i < 23 else GREY, stroke_width=3,
                               fill_color=GREEN if i < 23 else GREY, fill_opacity=0.55 if i < 23 else 0.0) for i in range(25)])
        dots.arrange_in_grid(rows=5, cols=5, buff=0.22).move_to([-4.6, 0.5, 0])
        dl = T("25 labelled neurons,\nmouse cell bodies in culture", 24, TEXT).next_to(dots, UP, buff=0.35)
        dn = T("23 with a rapidly\nadapting current", 24, GREEN).next_to(dots, DOWN, buff=0.35)
        self.at("cell bodies and culture")
        self.play(FadeIn(dl), LaggedStart(*[FadeIn(d, scale=0.5) for d in dots], lag_ratio=0.04), run_time=1.2)
        self.at("rapidly adapting currents")
        self.play(FadeIn(dn), run_time=0.5)
        oth = T("label also marks\nother neurons", 24, GREY).move_to(dn.get_center() + DOWN * 0.9)
        self.at("some other neurons")
        self.play(FadeIn(oth), run_time=0.6)

        # plot
        ax = Axes(x_range=[0, 25, 5], y_range=[0, 1.0, 0.25], x_length=6.2, y_length=3.6,
                  axis_config={"color": GREY, "stroke_width": 3, "include_ticks": True, "include_numbers": False, "tip_length": 0.15},
                  tips=False).move_to([2.8, -0.3, 0])
        xl = T("time (ms)", 24, GREY).next_to(ax.x_axis, DOWN, buff=0.55)
        yl = T("fraction of peak current", 24, GREY).next_to(ax, UP, buff=0.55).align_to(ax, LEFT)
        ticklabs = VGroup(*[M(str(t), 22, GREY).next_to(ax.c2p(t, 0), DOWN, buff=0.12) for t in (0, 10, 20)])
        ylabs = VGroup(M("1", 22, GREY).next_to(ax.c2p(0, 1.0), LEFT, buff=0.12), M("0", 22, GREY).next_to(ax.c2p(0, 0), LEFT, buff=0.12))
        tag = T("in this sketch: one exponential, tau = 5.6 ms (assumed)", 22, ORANGE).next_to(ax, DOWN, buff=1.05)
        self.at("time constant")
        self.play(Create(ax), FadeIn(xl), FadeIn(yl), FadeIn(ticklabs), FadeIn(ylabs), run_time=1.0)
        tau_lab = M("tau = 5.6 ms", 26, GREEN).move_to(ax.c2p(17, 0.82))
        self.play(FadeIn(tau_lab), run_time=0.4)
        curve = ax.plot(lambda t: np.exp(-t / 5.6), x_range=[0, 25], color=GREEN, stroke_width=6)
        self.at("one exponential")
        self.play(Create(curve), run_time=1.6)
        self.play(FadeIn(tag), run_time=0.4)
        d10 = Dot(ax.c2p(10, np.exp(-10 / 5.6)), color=YELLOW, radius=0.09)
        d20 = Dot(ax.c2p(20, np.exp(-20 / 5.6)), color=YELLOW, radius=0.09)
        v10 = DashedLine(ax.c2p(10, 0), d10.get_center(), color=YELLOW, stroke_width=3)
        v20 = DashedLine(ax.c2p(20, 0), d20.get_center(), color=YELLOW, stroke_width=3)
        p10 = M("17%", 26, YELLOW).next_to(d10, UP, buff=0.2).shift(RIGHT * 0.3)
        p20 = M("3%", 26, YELLOW).next_to(d20, UP, buff=0.25)
        self.at("is left at")
        self.play(Create(v10), FadeIn(d10), FadeIn(p10), run_time=0.8)
        self.at("and about")
        self.play(Create(v20), FadeIn(d20), FadeIn(p20), run_time=0.8)
        self.finish()


# ---------------------------------------------------------------------------------------------
class S06Rule(SpokenScene):
    def construct(self):
        # mouse panel
        mt = T("In mouse: Piezo2 deleted", 32, GREEN).move_to([-3.4, 3.0, 0])
        sq = VGroup(*[Square(side_length=0.8, stroke_color=GREY, stroke_width=3, fill_color=GREY, fill_opacity=0.25) for _ in range(8)])
        sq.arrange_in_grid(rows=2, cols=4, buff=0.25).move_to([-3.4, 1.4, 0])
        ml = T("8 muscles per mouse line", 26, GREY).next_to(sq, DOWN, buff=0.35)
        self.play(FadeIn(mt), FadeIn(sq), FadeIn(ml), run_time=0.4)
        self.at("small stretch response remained")
        self.play(sq[5].animate.set_stroke(GREEN).set_fill(GREEN, 0.7), run_time=0.7)
        mr = T("still responded to stretch:\n1 of 8 muscles, per line", 24, GREEN).next_to(ml, DOWN, buff=0.25)
        self.play(FadeIn(mr), run_time=0.5)
        ch = chip("principal transducer,\nnot the transducer", GREEN, size=30).move_to([-3.4, -2.4, 0])
        self.at("principal transducer")
        self.play(FadeIn(ch, shift=UP * 0.2), run_time=0.7)

        # human panel
        ht = T("In humans", 32, RED).move_to([3.4, 3.0, 0])
        ppl = VGroup(*[VGroup(Circle(radius=0.38, stroke_color=TEXT, stroke_width=3, fill_color=TEXT, fill_opacity=0.2),
                              Arc(radius=0.7, start_angle=0, angle=PI, color=TEXT, stroke_width=3).shift(DOWN * 1.0))
                       for _ in range(2)]).arrange(RIGHT, buff=1.2).move_to([3.4, 1.7, 0])
        pl = T("two people with inactivating\nPIEZO2 variants", 26, GREY).next_to(ppl, DOWN, buff=0.55)
        self.at("in humans")
        self.play(FadeIn(ht), FadeIn(ppl), FadeIn(pl), run_time=0.9)
        worse = chip("reaching and joint-angle tasks:\nmarkedly worse without visual cues", RED, size=26).move_to([3.4, -1.0, 0])
        self.at("markedly worse")
        self.play(FadeIn(worse, shift=UP * 0.2), run_time=0.7)
        series = T("two people: a clinical series", 26, GREY).move_to([3.4, -2.3, 0])
        self.at("clinical series")
        self.play(FadeIn(series), run_time=0.5)

        # rule
        self.at("keep this rule")
        everything = VGroup(mt, sq, ml, mr, ch, ht, ppl, pl, worse, series)
        self.play(FadeOut(everything), run_time=0.7)
        r1 = T("Limb position is an estimate\nfrom many signals.", 40, ORANGE, font=TITLE_FONT).move_to([0, 0.2, 0])
        self.at("estimate from many")
        self.play(Write(r1), run_time=1.5)
        self.finish()


class S07End(EndCard):
    LINE = "Limb position is an estimate from many signals."
