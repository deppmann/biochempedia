"""Warmth from excitation and silence: thermosensation (Biochemistrypedia explainer)

Timed to the SPOKEN words: every self.at("...") cue waits for that phrase in audio/words.json.
Spike ticks and temperature traces are drawn in this sketch (the lesson gives only the 0.2 to 6 Hz
range of the cool fibres' ongoing firing, the 27 and 32 degree baselines, and the 1 degree per
second ramp); nothing here is a recording.

COLOR MAP (one color per concept, whole video)
  ORANGE = warm-excited polymodal C fibre and its spikes ("excitation")
  BLUE   = TRPM8 and cool-sensitive C fibres and their spikes ("silence" when they go quiet)
  YELLOW = the thermal stimulus: warming, the Peltier surface step, the temperature trace, "warmth"
  GREEN  = the mouse's report (lick)
  RED    = failure / removal / not identified
  GREY   = skin, axes, labels, de-emphasized
"""
import numpy as np
from bp_style import *  # noqa: F401,F403

ORANGE = "#F29E4C"
WARM, COOL, STIM, REPORT, GONE = ORANGE, BLUE, YELLOW, GREEN, RED

T_RAMP0, T_RAMP1, T_END = 4.0, 6.5, 10.0
RX0, RX1 = -2.6, 6.2          # raster x range


# ---------------------------------------------------------------------------------------------
# sketch data
# ---------------------------------------------------------------------------------------------
def rate_warm(t):
    return 0.7 if t < T_RAMP0 else 0.7 + 5.3 * min(1.0, (t - T_RAMP0) / (T_RAMP1 - T_RAMP0))


def rate_cool(t):
    return 3.5 - 3.2 * min(1.0, max(0.0, (t - T_RAMP0) / (T_RAMP1 - T_RAMP0)))


def temp(t):
    return min(1.0, max(0.0, (t - T_RAMP0) / (T_RAMP1 - T_RAMP0)))


def spike_times(rate, seed):
    t = np.arange(0, T_END, 0.002)
    r = np.array([rate(x) for x in t])
    cum = np.cumsum(r) * 0.002
    rng = np.random.default_rng(seed)
    n = int(cum[-1])
    tg = np.arange(n) + 0.5 + rng.uniform(-0.3, 0.3, n)
    return t[np.searchsorted(cum, tg)]


WARM_T = spike_times(rate_warm, 3)
COOL_T = spike_times(rate_cool, 5)


# ---------------------------------------------------------------------------------------------
# helpers
# ---------------------------------------------------------------------------------------------
def X(t, x0=RX0, x1=RX1):
    return x0 + t / T_END * (x1 - x0)


def ticks(times, y, upto, color, h=1.2, x0=RX0, x1=RX1, w=5):
    g = VGroup()
    for t in times:
        if t <= upto:
            g.add(Line([X(t, x0, x1), y - h / 2, 0], [X(t, x0, x1), y + h / 2, 0], color=color, stroke_width=w))
    return g


def live_ticks(times, y, tracker, color, h=0.9, x0=RX0, x1=RX1):
    return always_redraw(lambda: ticks(times, y, tracker.get_value(), color, h, x0, x1))


def baseline_line(y, h=1.2, x0=RX0, x1=RX1):
    return Line([x0, y - h / 2 - 0.08, 0], [x1, y - h / 2 - 0.08, 0], color=GREY, stroke_width=2, stroke_opacity=0.6)


def arr(a, b, color=GREY, w=5, tip=0.22):
    return Arrow(np.array(a, float), np.array(b, float), buff=0, color=color, stroke_width=w, tip_length=tip,
                 max_tip_length_to_length_ratio=0.5, max_stroke_width_to_length_ratio=14)


def bchip(text, color=BLUE, size=24, **kw):
    c = chip(text, color, size=size, **kw)
    back = RoundedRectangle(corner_radius=0.14, width=c[0].width, height=c[0].height, stroke_width=0,
                            fill_color=BG, fill_opacity=1).move_to(c[0])
    return VGroup(back, *c)


def cross(center, s=0.3, color=GONE, w=7):
    c = np.array(list(center)[:2] + [0.0], float)
    return VGroup(Line(c + [-s, -s, 0], c + [s, s, 0], color=color, stroke_width=w),
                  Line(c + [-s, s, 0], c + [s, -s, 0], color=color, stroke_width=w))


def fibre(y, color, label, skin_label=False):
    """skin piece, ending bulb, axon and name of one afferent fibre."""
    skin = RoundedRectangle(corner_radius=0.1, width=0.3, height=1.3, stroke_color=GREY, stroke_width=3,
                            fill_color=GREY, fill_opacity=0.35).move_to([-6.1, y, 0])
    bulb = Circle(radius=0.17, stroke_color=color, stroke_width=4, fill_color=color, fill_opacity=0.5).move_to([-5.68, y, 0])
    axon = Line([-5.5, y, 0], [RX0 - 0.15, y, 0], color=color, stroke_width=5)
    name = T(label, 22, color).move_to([-4.35, y + 0.5, 0])
    g = VGroup(skin, bulb, axon, name)
    if skin_label:
        sl = T("forepaw skin", 22, GREY)
        sl.move_to([-6.3 + sl.width / 2, y - 0.95, 0])
        g.add(sl)
    return g


def temp_panel(tracker, y0=-3.0, h=1.5):
    """temperature trace in this sketch, drawn up to the tracker."""
    ax = VGroup(Line([RX0, y0, 0], [RX1, y0, 0], color=GREY, stroke_width=3),
                Line([RX0, y0, 0], [RX0, y0 + h + 0.2, 0], color=GREY, stroke_width=3))
    lab = T("temperature", 22, GREY).move_to([RX0 + 0.1 + 0.8, y0 + h + 0.38, 0])

    def curve():
        k = tracker.get_value()
        ts = np.linspace(0, max(k, 0.01), 160)
        m = VMobject(stroke_color=STIM, stroke_width=6)
        m.set_points_as_corners([[X(t), y0 + 0.15 + temp(t) * (h - 0.15), 0] for t in ts])
        return m

    return VGroup(ax, lab), always_redraw(curve)


def playhead(tracker, ytop, ybot):
    return always_redraw(lambda: DashedLine([X(tracker.get_value()), ybot, 0], [X(tracker.get_value()), ytop, 0],
                                            color=GREY, stroke_width=2, dash_length=0.12, stroke_opacity=0.7))


def sketch_note():
    t = T("spikes and traces: in this sketch", 22, GREY)
    return t.move_to([6.3 - t.width / 2, -3.35, 0])


class S00Title(TitleCard):
    LESSON = "Hot, warm, cool and cold"
    TITLE = "Warmth from excitation and silence"


# ---------------------------------------------------------------------------------------------
class S01Puzzle(SpokenScene):
    def construct(self):
        days = VGroup(*[Square(0.5, stroke_color=GREY, stroke_width=3, fill_color=GREY, fill_opacity=0.0) for _ in range(10)])
        days.arrange(RIGHT, buff=0.14).move_to([0, 2.3, 0])
        dlab = T("training days", 26, GREY).next_to(days, UP, buff=0.25)

        warm = bchip("forepaw warming", STIM, 28).move_to([-4.4, 0.0, 0])
        mouse = bchip("TRPM8-null mouse", COOL, 28).move_to([0.0, 0.0, 0])
        rep = bchip("reports it", REPORT, 28).move_to([4.4, 0.0, 0])
        a1 = arr(warm.get_right() + RIGHT * 0.1, mouse.get_left() + LEFT * 0.1, STIM)
        a2 = arr(mouse.get_right() + RIGHT * 0.1, rep.get_left() + LEFT * 0.1, REPORT)

        self.play(FadeIn(dlab), FadeIn(days), run_time=0.5)
        self.at("trained for")
        self.play(LaggedStart(*[d.animate.set_fill(GREY, 0.55) for d in days], lag_ratio=0.25), run_time=1.3)
        self.at("report warming")
        self.play(FadeIn(warm, shift=RIGHT * 0.2), GrowArrow(a1), FadeIn(mouse), run_time=0.6)
        self.play(GrowArrow(a2), FadeIn(rep), run_time=0.5)
        self.at("completely failed")
        x = cross(a2.get_center(), 0.38)
        no = T("no report", 30, GONE, weight=BOLD).next_to(a2, DOWN, buff=0.55)
        self.play(Create(x), rep.animate.set_opacity(0.35), FadeIn(no), run_time=0.5)

        # the puzzle: cold receptor, cold, warmth
        trpm = bchip("TRPM8: cold receptor", COOL, 28).move_to([-3.6, -2.5, 0])
        cold = bchip("cold", COOL, 28).move_to([0.6, -2.5, 0])
        warmth = bchip("warmth", STIM, 28).move_to([5.0, -2.5, 0])
        self.at("A cold receptor should matter for cold")
        self.play(FadeIn(trpm), run_time=0.4)
        self.play(GrowArrow(arr(trpm.get_right() + RIGHT * 0.1, cold.get_left() + LEFT * 0.1, COOL)), FadeIn(cold), run_time=0.6)
        self.at("miss warmth")
        dash = DashedLine(cold.get_right() + RIGHT * 0.15, warmth.get_left() + LEFT * 0.15, color=STIM, stroke_width=5)
        q = T("?", 64, STIM, weight=BOLD).move_to(dash.get_center() + UP * 0.5)
        self.play(Create(dash), FadeIn(warmth), FadeIn(q, scale=1.4), run_time=0.7)
        self.finish()


# ---------------------------------------------------------------------------------------------
class S02Task(SpokenScene):
    def construct(self):
        plate = Rectangle(width=3.8, height=0.5, stroke_color=GREY, stroke_width=4, fill_color=GREY, fill_opacity=0.3).move_to([-3.7, -0.9, 0])
        plate_l = T("Peltier surface, 8 × 8 mm", 24, GREY).next_to(plate, DOWN, buff=0.3)
        paw = RoundedRectangle(corner_radius=0.5, width=2.8, height=1.2, stroke_color=GREY, stroke_width=3,
                               fill_color=GREY, fill_opacity=0.18).move_to([-3.7, 0.0, 0])
        paw_l = T("forepaw", 24, GREY).move_to(paw)
        mouse_l = T("head-fixed mouse", 26, TEXT).move_to([-3.7, 1.9, 0])

        ax = VGroup(Line([0.6, -1.9, 0], [6.2, -1.9, 0], color=GREY, stroke_width=3),
                    Line([0.6, -1.9, 0], [0.6, 2.3, 0], color=GREY, stroke_width=3))
        tl = T("time", 22, GREY).move_to([5.7, -2.3, 0])
        yl = T("temperature", 22, GREY).move_to([0.6 + 0.9, 2.55, 0])
        base = Line([0.8, -0.5, 0], [3.3, -0.5, 0], color=STIM, stroke_width=7)
        step = Line([3.3, -0.5, 0], [3.3, 0.6, 0], color=STIM, stroke_width=7)
        top = Line([3.3, 0.6, 0], [6.0, 0.6, 0], color=STIM, stroke_width=7)
        base_l = M("32 °C", 28, STIM).move_to([2.0, -1.1, 0])
        dbl = DoubleArrow([3.75, -0.5, 0], [3.75, 0.6, 0], color=STIM, buff=0, stroke_width=4, tip_length=0.18)
        step_l = M("+1 °C", 28, STIM).move_to([4.8, 0.05, 0])
        lick = bchip("mouse licks", REPORT, 28).move_to([4.7, 1.6, 0])

        self.at("Here is the task")
        self.play(FadeIn(mouse_l), FadeIn(paw), FadeIn(paw_l), run_time=0.6)
        self.at("Peltier surface")
        self.play(FadeIn(plate), FadeIn(plate_l), FadeIn(ax), FadeIn(tl), FadeIn(yl), run_time=0.7)
        self.at("holds")
        self.play(Create(base), FadeIn(base_l), run_time=0.7)
        self.at("then steps")
        self.play(Create(step), plate.animate.set_stroke(STIM).set_fill(STIM, 0.3), Create(top), run_time=0.6)
        self.at("warming step")
        self.play(GrowFromCenter(dbl), FadeIn(step_l), run_time=0.5)
        self.at("licks to report")
        self.play(FadeIn(lick, shift=UP * 0.2), run_time=0.5)
        self.finish()


# ---------------------------------------------------------------------------------------------
class S03Warm(SpokenScene):
    def construct(self):
        y = 1.5
        trk = ValueTracker(0.0)
        prep = T("ex vivo skin-nerve preparation", 24, GREY).move_to([1.8, 3.0, 0])
        f = fibre(y, WARM, "polymodal C fibre", skin_label=True)
        bl = baseline_line(y, 0.9)
        ticks_m = live_ticks(WARM_T, y, trk, WARM)
        panel, curve = temp_panel(trk)
        ph = playhead(trk, y + 0.6, -3.0)
        ramp_l = T("warming, 1 °C per second", 24, STIM).move_to([X(7.3), -0.6, 0])

        tick_l = T("each tick is one spike", 22, GREY).move_to([X(1.9), y + 0.85, 0])
        self.add(curve, ticks_m, ph)
        self.add(sketch_note())
        self.play(FadeIn(f), Create(bl), FadeIn(panel), run_time=0.9)
        rate = (T_RAMP0 - 0.1) / (self.t_of("increased its firing") - 0.3 - self.elapsed())
        self.add(trk)
        trk.add_updater(lambda m, dt: m.set_value(min(T_RAMP0 - 0.1, m.get_value() + dt * rate)))
        self.at("skin nerve preparation")
        self.play(FadeIn(prep), run_time=0.5)
        self.at("Each tick")
        self.play(FadeIn(tick_l), run_time=0.4)
        self.at("warmed")
        self.play(FadeIn(ramp_l), run_time=0.5)
        self.at("One population")
        self.at("Warming")
        trk.clear_updaters()
        self.play(trk.animate.set_value(T_END), run_time=4.2, rate_func=linear)
        self.play(Indicate(ticks_m, color=WARM, scale_factor=1.04), run_time=0.8)
        self.finish()


# ---------------------------------------------------------------------------------------------
class S04Cool(SpokenScene):
    def construct(self):
        y = 1.5
        trk = ValueTracker(0.0)
        f = fibre(y, COOL, "cool-sensitive C fibre", skin_label=True)
        bl = baseline_line(y, 0.9)
        ticks_m = live_ticks(COOL_T, y, trk, COOL)
        panel, curve = temp_panel(trk)
        ph = playhead(trk, y + 0.6, -3.0)
        share = T("about 19% of thermosensitive fibres recorded", 24, GREY).move_to([1.8, 3.0, 0])
        bath = M("27 °C bath", 26, STIM).move_to([X(1.6), -2.5, 0])
        rng_l = M("0.2 to 6 Hz", 26, COOL).move_to([X(2.0), y + 0.95, 0])
        note1 = T("awake forepaw skin, thermal imaging: 26 to 28 °C", 24, TEXT).move_to([1.6, 0.1, 0])
        note2 = T("usual bath, 32 °C: this population not seen", 24, GONE).move_to([1.6, -0.6, 0])

        self.add(sketch_note())
        self.play(FadeIn(f), Create(bl), FadeIn(panel), run_time=0.8)
        self.add(curve, ticks_m, ph)
        rate = (T_RAMP0 - 0.1) / (self.t_of("Warming reduced") - 0.3 - self.elapsed())
        self.add(trk)
        trk.add_updater(lambda m, dt: m.set_value(min(T_RAMP0 - 0.1, m.get_value() + dt * rate)))
        self.at("group")
        self.play(FadeIn(share), run_time=0.5)
        self.at("skin")
        self.play(FadeIn(bath), run_time=0.4)
        self.at("fired all the time")
        self.play(FadeIn(rng_l), run_time=0.4)
        self.at("Warming reduced")
        trk.clear_updaters()
        self.play(trk.animate.set_value(T_END), run_time=3.5, rate_func=linear)
        self.at("thermal imaging")
        self.play(FadeIn(note1), run_time=0.5)
        self.at("the usual")
        self.play(FadeIn(note2), run_time=0.5)
        self.finish()


# ---------------------------------------------------------------------------------------------
def band(y0, y1):
    y0, y1 = y0 - 0.2, y1 + 0.2
    x0, x1 = X(T_RAMP0), X(T_END)
    return Rectangle(width=x1 - x0, height=y1 - y0, stroke_width=0, fill_color=STIM, fill_opacity=0.12).move_to(
        [(x0 + x1) / 2, (y0 + y1) / 2, 0])


class S05Two(SpokenScene):
    def construct(self):
        yw, yc = 2.2, -0.1
        fw = fibre(yw, WARM, "polymodal C fibre")
        fc = fibre(yc, COOL, "cool-sensitive C fibre", skin_label=True)
        bls = VGroup(baseline_line(yw), baseline_line(yc))
        tw = ticks(WARM_T, yw, T_END, WARM)
        tc = ticks(COOL_T, yc, T_END, COOL)
        bd = band(yc - 0.7, yw + 0.7)
        bd_l = T("warming", 24, STIM).move_to([X(5.3), yc - 1.05, 0])
        up = VGroup(Arrow([0, 0, 0], [0, 0.7, 0], buff=0, color=WARM, stroke_width=7, tip_length=0.22),
                    T("speeds up", 24, WARM)).arrange(RIGHT, buff=0.15).move_to([X(8.3), (yw + yc) / 2, 0])
        dn = VGroup(Arrow([0, 0.7, 0], [0, 0, 0], buff=0, color=COOL, stroke_width=7, tip_length=0.22),
                    T("slows down", 24, COOL)).arrange(RIGHT, buff=0.15).move_to([X(8.3), yc - 1.1, 0])
        sn = sketch_note()

        self.add(sn)
        self.at("one channel at a time")
        self.play(FadeIn(fw), FadeIn(fc), Create(bls), run_time=0.8)
        self.play(FadeIn(tw), FadeIn(tc), FadeIn(bd), FadeIn(bd_l), run_time=0.8)
        self.at("speed up")
        self.play(FadeIn(up), Indicate(tw, color=WARM, scale_factor=1.03), run_time=0.9)
        self.at("slow down")
        self.play(FadeIn(dn), Indicate(tc, color=COOL, scale_factor=1.03), run_time=0.9)

        trpm = bchip("TRPM8 removed", GONE, 26).move_to([X(5.0), yc, 0])
        self.at("Without")
        self.play(FadeOut(tc), FadeIn(trpm), run_time=0.7)
        self.at("one part")
        xx = cross(dn.get_left() + LEFT * 0.35, 0.22)
        self.play(dn.animate.set_opacity(0.35), Create(xx), run_time=0.6)

        red = T("reduced cool input", 36, COOL, weight=BOLD).move_to([-0.2, -1.95, 0])
        self.at("reduced cool input")
        self.play(FadeIn(red, shift=UP * 0.15), run_time=0.6)
        bl_ = T("a central circuit that flips the cool signal", 24, GREY).move_to([-0.2, -2.6, 0])
        box = DashedVMobject(RoundedRectangle(corner_radius=0.14, width=bl_.width + 0.5, height=0.8,
                                              stroke_color=GREY, stroke_width=3), num_dashes=40).move_to(bl_)
        ni = T("not identified here", 24, GONE, weight=BOLD).move_to([-0.2, -3.3, 0])
        self.at("central circuit")
        self.play(FadeIn(box), FadeIn(bl_), run_time=0.6)
        self.at("has been identified")
        self.play(FadeIn(ni), run_time=0.4)
        self.finish()


# ---------------------------------------------------------------------------------------------
class S06Rule(SpokenScene):
    def construct(self):
        yw, yc = 2.2, -0.1
        fw = fibre(yw, WARM, "polymodal C fibre")
        fc = fibre(yc, COOL, "cool-sensitive C fibre", skin_label=True)
        bls = VGroup(baseline_line(yw), baseline_line(yc))
        tw = ticks(WARM_T, yw, T_END, WARM)
        tc = ticks(COOL_T, yc, T_END, COOL)
        bd = band(yc - 0.7, yw + 0.7)

        self.add(sketch_note())
        self.play(FadeIn(fw), FadeIn(fc), Create(bls), FadeIn(tw), FadeIn(tc), FadeIn(bd), run_time=0.9)

        xa, xb = X(0.1), X(T_RAMP0 - 0.1)
        yb = yc - 0.7
        br = VGroup(Line([xa, yb, 0], [xb, yb, 0], color=COOL, stroke_width=5),
                    Line([xa, yb, 0], [xa, yb + 0.18, 0], color=COOL, stroke_width=5),
                    Line([xb, yb, 0], [xb, yb + 0.18, 0], color=COOL, stroke_width=5))
        rest = T("resting condition", 24, COOL).move_to([(xa + xb) / 2, yb - 0.38, 0])
        part = T("part of the stimulus", 24, STIM).move_to([(xa + xb) / 2, yb - 0.38, 0])
        self.at("one baseline")
        self.play(Create(br), FadeIn(rest), run_time=0.7)
        self.at("part of the stimulus")
        self.play(ReplacementTransform(rest, part), run_time=0.6)

        ex = bchip("excitation", WARM, 30).move_to([-3.3, -2.5, 0])
        pl = T("+", 40, TEXT).move_to([-1.0, -2.5, 0])
        si = bchip("silence", COOL, 30).move_to([1.2, -2.5, 0])
        eq = T("=", 40, TEXT).move_to([3.0, -2.5, 0])
        wm = bchip("warmth", STIM, 30).move_to([4.9, -2.5, 0])
        self.at("read from excitation")
        self.play(FadeIn(ex, shift=UP * 0.15), Indicate(tw, color=WARM, scale_factor=1.03), run_time=0.6)
        self.at("silence")
        self.play(FadeIn(pl), FadeIn(si, shift=UP * 0.15), Indicate(tc, color=COOL, scale_factor=1.03), run_time=0.6)
        self.play(FadeIn(eq), FadeIn(wm, scale=0.9), run_time=0.6)
        self.finish()


class S07End(EndCard):
    LINE = "Warmth is read from excitation and from silence."
