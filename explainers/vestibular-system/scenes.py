"""Vestibular system: why your own head turns cancel centrally  (Biochemistrypedia explainer)

Timed to the SPOKEN words: every self.at("...") cue waits for that phrase in audio/words.json.

COLOR MAP (one color per concept, whole video)
  BLUE   = semicircular-canal afferents (the periphery)
  YELLOW = the central vestibular-only neuron and its response
  GREEN  = self-generated (active) turn: the motor command, the expected feedback, cancellation
  ORANGE = passive turn (pushed from outside)
  TEAL   = neck proprioceptive feedback (the actual feedback)
  RED    = mismatch / cancellation failing
  GREY   = outlines, axes, de-emphasised
All numbers are the lesson's made-up illustration (20 deg/s, 40 and 4 spikes/s, 2.0 and 0.2, 90 percent).
"""
import numpy as np
from bp_style import *  # noqa: F401,F403

ORANGE = "#F29E4C"
TEALN = "#3FB8C0"  # neck feedback (same value as TEAL, kept as its own concept)


# ---------------------------------------------------------------------------------------------
# helpers
# ---------------------------------------------------------------------------------------------
def bchip(text, color=BLUE, size=26, **kw):
    c = chip(text, color, size=size, **kw)
    back = RoundedRectangle(corner_radius=0.14, width=c[0].width, height=c[0].height, stroke_width=0,
                            fill_color=BG, fill_opacity=1).move_to(c[0])
    return VGroup(back, *c)


def lines2(a, b, color, size=24):
    """a two-line label chip."""
    label = VGroup(T(a, size, color), T(b, size, color)).arrange(DOWN, buff=0.08)
    box = RoundedRectangle(corner_radius=0.14, width=label.width + 0.44, height=label.height + 0.4,
                           stroke_color=color, stroke_width=2.5, fill_color=color, fill_opacity=0.16)
    back = RoundedRectangle(corner_radius=0.14, width=box.width, height=box.height, stroke_width=0,
                            fill_color=BG, fill_opacity=1)
    g = VGroup(back, box, label)
    label.move_to(box)
    return g


def arr(a, b, color=GREY, w=5, tip=0.22):
    return Arrow(a, b, buff=0.08, color=color, stroke_width=w, tip_length=tip,
                 max_tip_length_to_length_ratio=0.45, max_stroke_width_to_length_ratio=12)


def head_icon(color, scale=1.0):
    """a head seen from above: circle with a nose triangle pointing up (forward)."""
    face = Circle(radius=0.62, stroke_color=color, stroke_width=4, fill_color=color, fill_opacity=0.18)
    nose = Triangle(stroke_width=0, fill_color=color, fill_opacity=0.9).scale(0.17)
    nose.move_to(face.get_top() + UP * 0.1)
    g = VGroup(face, nose)
    return g.scale(scale)


def turn_arrow(center, color, flip=False, r=0.98):
    arc = Arc(radius=r, start_angle=PI * 0.15, angle=PI * 0.7, color=color, stroke_width=5)
    arc.add_tip(tip_length=0.2)
    arc.move_arc_center_to(center)
    if flip:
        arc.flip(UP, about_point=center)
    return arc


def ticks(x0, x1, y, n, color, seed, h=0.32):
    """irregular spike ticks along a baseline."""
    rng = np.random.RandomState(seed)
    xs = np.sort(rng.uniform(x0 + 0.1, x1 - 0.1, n))
    base = Line([x0, y - h / 2, 0], [x1, y - h / 2, 0], color=GREY, stroke_width=2)
    tk = VGroup(*[Line([x, y - h / 2, 0], [x, y + h / 2, 0], color=color, stroke_width=4) for x in xs])
    return base, tk


def bell(t, peak, mid=0.5, wid=0.17):
    return peak * np.exp(-(((t - mid) / wid) ** 2))


def make_axes(w, h, ymax, ytick_vals, xlabel, color=GREY):
    ax = Axes(x_range=[0, 1, 0.5], y_range=[0, ymax, ymax], x_length=w, y_length=h,
              axis_config={"color": color, "stroke_width": 3, "include_ticks": False, "include_tip": False},
              tips=False)
    labels = VGroup()
    for v in ytick_vals:
        p = ax.c2p(0, v)
        tk = Line(p + LEFT * 0.08, p + RIGHT * 0.08, color=color, stroke_width=3)
        lb = M(f"{v:g}", 22, GREY).next_to(tk, LEFT, buff=0.1)
        labels.add(tk, lb)
    xl = T(xlabel, 22, GREY).next_to(ax, DOWN, buff=0.15)
    return ax, labels, xl


class S00Title(TitleCard):
    LESSON = "Balance: vestibular hair cells and self-motion"
    TITLE = "Why Your Own Turns Cancel"


# ---------------------------------------------------------------------------------------------
class S01Turn(SpokenScene):
    """two heads (own turn, pushed) -> the same afferent firing under both -> the question."""

    def construct(self):
        xl, xr = -3.3, 3.3
        hl = head_icon(GREEN, 1.6).move_to([xl, 1.05, 0])
        hr = head_icon(ORANGE, 1.6).move_to([xr, 1.05, 0])
        al = turn_arrow([xl, 1.05, 0], GREEN, r=1.3)
        ar = turn_arrow([xr, 1.05, 0], ORANGE, r=1.3)
        tl = T("a turn you make", 30, GREEN).move_to([xl, 3.0, 0])
        tr = T("a push from outside", 30, ORANGE).move_to([xr, 3.0, 0])
        note = T("heads drawn from above, nose up", 22, GREY).move_to([0, -3.3, 0])

        self.at("You turn your head")
        self.play(FadeIn(hl), FadeIn(tl), Create(al), run_time=0.8)
        self.at("A push from outside")
        self.play(FadeIn(hr), FadeIn(tr), Create(ar), run_time=0.8)
        self.play(FadeIn(note), run_time=0.4)

        # afferents under each head
        cl = bchip("canal afferents", BLUE, 28).move_to([xl, -0.85, 0])
        cr = bchip("canal afferents", BLUE, 28).move_to([xr, -0.85, 0])
        bl, tkl = ticks(xl - 1.6, xl + 1.6, -1.8, 10, BLUE, 3, h=0.4)
        br, tkr = ticks(xr - 1.6, xr + 1.6, -1.8, 10, BLUE, 5, h=0.4)
        self.at("alert monkeys")
        self.play(FadeIn(cl), FadeIn(cr), Create(bl), Create(br), run_time=0.7)
        self.at("respond to head motion")
        self.play(LaggedStart(*[Create(t) for t in tkl], lag_ratio=0.12),
                  LaggedStart(*[Create(t) for t in tkr], lag_ratio=0.12), run_time=1.6)
        self.at("They respond to both")
        both = T("both respond", 30, BLUE).move_to([0, -2.5, 0])
        self.play(FadeIn(both, shift=UP * 0.1), run_time=0.5)
        self.at("where does the difference")
        q = T("Where does the difference arise?", 36, font=TITLE_FONT).move_to([0, -3.1, 0])
        self.play(FadeOut(note), FadeIn(q, shift=UP * 0.1), run_time=0.7)
        self.finish()


# ---------------------------------------------------------------------------------------------
class S02Central(SpokenScene):
    """afferent -> vestibular-only neuron across a periphery/central divider; conditions; afferents keep firing."""

    def construct(self):
        head = T("Roy and Cullen, 2004: four alert macaques, in vivo", 30, GREY).to_edge(UP, buff=0.5)
        self.at("The answer is central")
        self.play(FadeIn(head), run_time=0.6)
        div = DashedLine([0.05, 2.5, 0], [0.05, -3.0, 0], color=GREY, stroke_width=3)
        lp = T("periphery", 28, BLUE).move_to([-3.4, 2.35, 0])
        lc = T("central", 28, YELLOW).move_to([3.4, 2.35, 0])
        self.play(Create(div), FadeIn(lp), FadeIn(lc), run_time=0.7)

        aff = bchip("canal afferents", BLUE, 28).move_to([-3.4, 1.2, 0])
        neu = lines2("vestibular-only", "neuron", YELLOW, 28).move_to([3.4, 1.2, 0])
        link = arr(aff.get_right(), neu.get_left(), GREY)
        self.at("vestibular only neurons")
        self.play(FadeIn(aff), FadeIn(neu, scale=0.9), GrowArrow(link), run_time=0.8)

        desc = VGroup(T("neurons of the vestibular nuclei:", 24, YELLOW),
                      T("respond to head motion,", 24, TEXT),
                      T("not to eye movements", 24, TEXT)).arrange(DOWN, buff=0.1).move_to([3.4, -0.35, 0])
        self.at("These are neurons")
        self.play(FadeIn(desc, shift=UP * 0.1), run_time=0.7)

        c1 = chip("head restraint", GREY, 24)
        c2 = chip("neck torque", GREY, 24)
        c3 = chip("search coils: head and gaze", GREY, 24)
        row = VGroup(c1, c2).arrange(RIGHT, buff=0.3)
        lab = T("conditions varied", 24, GREY)
        blk = VGroup(lab, row).arrange(DOWN, buff=0.15).move_to([-3.0, -0.6, 0])
        self.at("varied conditions")
        self.play(FadeIn(blk, shift=UP * 0.1), run_time=0.7)
        c3.move_to([3.4, -1.7, 0])
        self.at("magnetic search coils")
        self.play(FadeIn(c3), run_time=0.5)

        b, tk = ticks(-4.8, -1.6, -2.1, 9, BLUE, 7, h=0.4)
        self.at("The afferents kept firing")
        self.play(Create(b), LaggedStart(*[Create(t) for t in tk], lag_ratio=0.15), run_time=1.5)
        fl = T("afferents keep firing", 24, BLUE).next_to(b, DOWN, buff=0.15)
        self.play(FadeIn(fl), run_time=0.4)
        self.at("so the cancellation is central")
        self.play(Indicate(VGroup(neu[1], neu[2]), color=YELLOW, scale_factor=1.08), run_time=0.8)
        self.finish()


# ---------------------------------------------------------------------------------------------
class S03Numbers(SpokenScene):
    """head velocity (one shape) -> neuron modulation: passive 40 then active 4 -> sensitivity -> 90 percent."""

    def construct(self):
        tag = T("made-up numbers, in this sketch", 26, GOLD).to_edge(UP, buff=0.5)
        axL, lbL, xlL = make_axes(4.6, 2.8, 45, [0, 20], "time (in this sketch)")
        axR, lbR, xlR = make_axes(4.6, 2.8, 45, [0, 20, 40], "time (in this sketch)")
        # left axis only goes to 20 deg/s: use its own scale
        axL = Axes(x_range=[0, 1, 0.5], y_range=[0, 22.5, 22.5], x_length=4.6, y_length=2.8,
                   axis_config={"color": GREY, "stroke_width": 3, "include_ticks": False, "include_tip": False}, tips=False)
        lbL = VGroup()
        for v in (0, 20):
            p = axL.c2p(0, v)
            tk = Line(p + LEFT * 0.08, p + RIGHT * 0.08, color=GREY, stroke_width=3)
            lbL.add(tk, M(f"{v}", 22, GREY).next_to(tk, LEFT, buff=0.1))
        xlL = T("time (in this sketch)", 22, GREY).next_to(axL, DOWN, buff=0.15)
        gL = VGroup(axL, lbL, xlL).move_to([-3.3, 0.7, 0])
        gR = VGroup(axR, lbR, xlR).move_to([3.3, 0.7, 0])
        tL = T("head velocity (deg/s)", 24, TEXT).next_to(axL, UP, buff=0.25)
        tR = T("neuron modulation (spikes/s)", 24, YELLOW).next_to(axR, UP, buff=0.25)
        # tL/tR positioned after groups moved
        tL.next_to(gL[0], UP, buff=0.25)
        tR.next_to(gR[0], UP, buff=0.25)

        self.at("made up numbers")
        self.play(FadeIn(tag), run_time=0.5)
        self.play(FadeIn(gL), FadeIn(gR), FadeIn(tL), FadeIn(tR), run_time=0.8)

        vel = axL.plot(lambda t: bell(t, 20), x_range=[0, 1, 0.01], color=TEXT, stroke_width=5)
        passive = axR.plot(lambda t: bell(t, 40), x_range=[0, 1, 0.01], color=ORANGE, stroke_width=5)
        active = axR.plot(lambda t: bell(t, 4), x_range=[0, 1, 0.01], color=GREEN, stroke_width=5)

        self.at("A passive turn")
        pl = T("passive turn", 24, ORANGE).move_to(axL.c2p(0.5, 24.0) + UP * 0.0)
        self.play(Create(vel), run_time=1.0)
        self.at("It evokes a modulation")
        self.play(Create(passive), run_time=1.0)
        pk = M("40", 24, ORANGE).next_to(axR.c2p(0.5, 40), RIGHT, buff=0.4)
        self.play(FadeIn(pk), run_time=0.3)

        eq1 = M("passive: 40 / 20 = 2.0 spikes/s per deg/s", 24, ORANGE).move_to([0, -1.95, 0])
        self.at("Divide the modulation")
        self.play(FadeIn(eq1, shift=UP * 0.1), run_time=0.6)

        # active: same head velocity, small response
        self.at("An active turn")
        self.play(Create(active), run_time=0.9)
        pk2 = M("4", 24, GREEN).next_to(axR.c2p(0.5, 4), UP, buff=0.12)
        self.play(FadeIn(pk2), run_time=0.3)
        eq2 = M("active:  4 / 20 = 0.2 spikes/s per deg/s", 24, GREEN).move_to([0, -2.6, 0])
        self.at("Sensitivity is 0 2")
        self.play(FadeIn(eq2, shift=UP * 0.1), run_time=0.6)
        eq3 = M("1 - 0.2 / 2.0 = 90 % cancelled", 28, YELLOW).move_to([0, -3.2, 0])
        self.at("response is 90")
        self.play(FadeIn(eq3, shift=UP * 0.1), run_time=0.6)
        self.play(Indicate(eq3, color=YELLOW, scale_factor=1.06), run_time=0.8)
        self.finish()


# ---------------------------------------------------------------------------------------------
class S04Match(SpokenScene):
    """motor command -> expected feedback; neck proprioception; both meet at a dashed match; cancellation."""

    def construct(self):
        head = T("In the neurons tested", 24, GREY).move_to([0, 3.4, 0])
        q = T("What lets the neuron cancel?", 36, font=TITLE_FONT).move_to([0, 2.85, 0])
        self.at("What lets the neuron cancel")
        self.play(FadeIn(q), run_time=0.6)

        neu = lines2("vestibular-only", "neuron", YELLOW, 24).move_to([4.5, 0.15, 0])
        self.play(FadeIn(neu), run_time=0.5)

        match = bchip("match?", GREY, 26).move_to([1.2, 0.15, 0])
        match[1].set_stroke(GREY)
        dash = DashedVMobject(match[1].copy().set_stroke(GREY, width=3).set_fill(opacity=0), num_dashes=40)
        match_g = VGroup(match[0], match[2], dash)
        out = arr([2.0, 0.15, 0], neu.get_left(), YELLOW)

        tagm = T("schematic; location not known", 22, GREY).move_to([2.6, -0.62, 0])
        neck = lines2("neck", "proprioception", TEALN, 24).move_to([-4.6, -1.7, 0])
        self.at("response to active motion")
        self.play(FadeIn(head), run_time=0.4)
        self.at("neck proprioceptive activation")
        self.play(FadeIn(neck, shift=RIGHT * 0.1), run_time=0.7)
        a_n = arr(neck.get_right(), [0.75, -0.1, 0], TEALN)
        self.at("feedback from the neck")
        self.play(GrowArrow(a_n), FadeIn(match_g), FadeIn(tagm), run_time=0.8)

        mc = bchip("motor command", GREEN, 26).move_to([-4.4, 1.6, 0])
        ex = lines2("expected", "feedback", GREEN, 24).move_to([-0.6, 1.6, 0])
        a_m = arr(mc.get_right(), ex.get_left(), GREEN)
        self.at("feedback expected from the motor command")
        self.play(FadeIn(mc), run_time=0.5)
        self.play(GrowArrow(a_m), FadeIn(ex), run_time=0.7)
        a_e = arr(ex.get_right(), [1.0, 0.5, 0], GREEN)
        self.at("The command sets")
        self.play(GrowArrow(a_e), run_time=0.5)
        self.play(GrowArrow(out), run_time=0.5)
        res = T("active response cancelled", 26, GREEN).move_to([4.2, -1.4, 0])
        self.at("should report")
        self.play(FadeIn(res), run_time=0.5)
        self.finish()


# ---------------------------------------------------------------------------------------------
class S05Mismatch(SpokenScene):
    """sensitivity bars: passive 2.0, active matched 0.2, mismatched: arrow climbing toward 2.0."""

    def construct(self):
        base_y, k = -2.2, 2.1   # 1.0 sensitivity unit = 1.75 scene units
        tag = T("sensitivity (spikes/s per deg/s): made-up numbers", 24, GOLD).to_edge(UP, buff=0.5)
        baseline = Line([-6.0, base_y, 0], [6.0, base_y, 0], color=GREY, stroke_width=3)
        ref = DashedLine([-6.0, base_y + 2.0 * k, 0], [6.0, base_y + 2.0 * k, 0], color=GREY, stroke_width=2.5)
        ref_l = M("2.0", 24, GREY).move_to([-6.0 + 0.35, base_y + 2.0 * k + 0.28, 0])
        xs = [-3.9, 0.0, 3.9]

        def bar(x, val, color):
            r = Rectangle(width=1.6, height=val * k, stroke_color=color, stroke_width=3,
                          fill_color=color, fill_opacity=0.3)
            return r.move_to([x, base_y + val * k / 2, 0])

        b1, b2 = bar(xs[0], 2.0, ORANGE), bar(xs[1], 0.2, GREEN)
        v1 = M("2.0", 28, ORANGE).next_to(b1, UP, buff=0.12)
        v2 = M("0.2", 28, GREEN).next_to(b2, UP, buff=0.12)
        l1 = VGroup(T("passive", 24, ORANGE), T("turn", 24, ORANGE)).arrange(DOWN, buff=0.05).move_to([xs[0], base_y - 0.65, 0])
        l2 = VGroup(T("active, feedback", 24, GREEN), T("matches", 24, GREEN)).arrange(DOWN, buff=0.05).move_to([xs[1], base_y - 0.65, 0])
        l3 = VGroup(T("active, feedback", 24, RED), T("mismatched", 24, RED)).arrange(DOWN, buff=0.05).move_to([xs[2], base_y - 0.65, 0])

        self.play(FadeIn(tag), Create(baseline), Create(ref), FadeIn(ref_l), run_time=0.6)
        self.play(FadeIn(b1), FadeIn(v1), FadeIn(l1), FadeIn(b2), FadeIn(v2), FadeIn(l2), run_time=0.8)

        self.at("Now suppose neck feedback")
        slot = DashedVMobject(Rectangle(width=1.6, height=1.0, stroke_color=RED, stroke_width=3), num_dashes=24)
        slot.move_to([xs[2], base_y + 0.5, 0])
        self.play(FadeIn(l3), FadeIn(slot), run_time=0.7)
        b3 = bar(xs[2], 0.2, RED)
        self.play(FadeOut(slot), FadeIn(b3), run_time=0.4)

        self.at("climb back")
        up = arr([xs[2], base_y + 0.2 * k + 0.1, 0], [xs[2], base_y + 2.0 * k - 0.05, 0], RED, w=7)
        tw = T("expected to climb", 24, RED)
        tw2 = T("back toward 2.0", 24, RED)
        tg = VGroup(tw, tw2).arrange(DOWN, buff=0.05).next_to(up, LEFT, buff=0.3)
        # keep the note inside the frame: sits right of the arrow
        self.play(GrowArrow(up), run_time=1.0)
        self.play(FadeIn(tg), run_time=0.5)

        self.at("the cancellation failed")
        fail = T("cancellation fails", 30, RED, weight=BOLD).move_to([xs[2] - 0.2, 2.6, 0])
        self.play(FadeIn(fail, shift=DOWN * 0.1), run_time=0.6)
        self.finish()


# ---------------------------------------------------------------------------------------------
class S06Rule(SpokenScene):
    """three limits, each lighting its part of a small chain; the rule."""

    def construct(self):
        aff = bchip("canal afferents", BLUE, 26).move_to([2.2, 1.5, 0])
        match = bchip("match?", GREY, 26).move_to([5.3, -0.9, 0])
        neu = lines2("vestibular-only", "neuron", YELLOW, 24).move_to([2.2, -0.9, 0])
        dash = DashedVMobject(match[1].copy().set_stroke(GREY, width=3).set_fill(opacity=0), num_dashes=40)
        match_g = VGroup(match[0], match[2], dash)
        a2 = arr([2.2, 1.0, 0], neu.get_top(), GREY)
        q = T("not located", 22, GREY).next_to(match_g, DOWN, buff=0.15)
        b, tk = ticks(3.9, 4.8, 1.5, 3, BLUE, 11)

        self.at("Three limits matter")
        self.play(FadeIn(aff), FadeIn(match_g), FadeIn(neu), GrowArrow(a2), run_time=0.9)

        def row(n, text, y, color):
            badge = VGroup(Circle(radius=0.26, stroke_color=color, stroke_width=3, fill_color=color, fill_opacity=0.2),
                           M(str(n), 24, color)).move_to([-6.0, y, 0])
            badge[1].move_to(badge[0])
            lines = [T(s, 26, TEXT) for s in text]
            t = VGroup(*lines).arrange(DOWN, aligned_edge=LEFT, buff=0.06)
            t.next_to(badge, RIGHT, buff=0.3)
            return VGroup(badge, t)

        r1 = row(1, ["The comparator circuit", "was not located"], 1.5, GREY)
        r2 = row(2, ["Not every vestibular neuron", "was shown to cancel"], 0.0, YELLOW)
        r3 = row(3, ["Afferents kept firing:", "the periphery did not switch off"], -1.5, BLUE)

        self.at("The comparator circuit")
        self.play(FadeIn(r1, shift=RIGHT * 0.1), Indicate(match_g, color=WHITE, scale_factor=1.1), FadeIn(q), run_time=0.9)
        self.at("Not every vestibular neuron")
        self.play(FadeIn(r2, shift=RIGHT * 0.1), Indicate(VGroup(neu[1], neu[2]), color=YELLOW, scale_factor=1.08), run_time=0.9)
        self.at("since the afferents kept firing")
        self.play(FadeIn(r3, shift=RIGHT * 0.1), Create(tk[0]), run_time=0.5)
        self.play(LaggedStart(*[Create(t) for t in tk[1:]], lag_ratio=0.3), run_time=0.8)

        self.at("Keep this rule")
        chain = VGroup(aff, neu, match_g, q, a2, tk)
        self.play(FadeOut(VGroup(r1, r2, r3)), chain.animate.shift(UP * 1.1 + LEFT * 0.0), run_time=0.8)
        rule = VGroup(T("In the neurons tested, the cancelling is central,", 34, TEXT, font=TITLE_FONT),
                      T("and it held only when neck feedback", 34, TEXT, font=TITLE_FONT),
                      T("matched the expected feedback", 34, YELLOW, font=TITLE_FONT)).arrange(DOWN, buff=0.18)
        rule.move_to([0, -1.9, 0])
        self.at("In the neurons tested")
        self.play(FadeIn(rule, shift=UP * 0.1), run_time=0.9)
        self.finish()


class S07End(EndCard):
    LINE = "Afferents keep firing; in the neurons tested, central cancelling needed matched neck feedback."
