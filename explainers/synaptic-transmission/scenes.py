"""Release comes in countable packets: synaptic transmission and quantal release (Biochemistrypedia explainer)

Timed to the SPOKEN words: every self.at("...") cue waits for that phrase in audio/words.json.
Every plot is a sketch ("in this sketch"); the numbers on screen are the lesson's own (the made-up frog
junction: 0.40 mV, 200 stimuli, 74 failures, 0.37, 0.99; normal calcium: 60 quanta, 24 mV, fires at 12 mV,
safety factor 2.0; myasthenia: 0.24 mV, 14.4 mV, 45 quanta, 10.8 mV).

COLOR MAP (one color per concept, whole video)
  BLUE   = presynaptic side: axon, nerve terminal
  YELLOW = transmitter: acetylcholine, a packet (quantum), vesicle filling
  GREEN  = the muscle's voltage response: miniature, evoked response, the bar of quanta, "fires"
  TEAL   = calcium
  PURPLE = magnesium
  PINK   = receptors
  ORANGE = the level at which the fibre fires (dashed line), the safety factor
  RED    = failure / no response / "the fibre fails"
  GOLD   = where the fault lies (highlight of the muscle side or the terminal side in the last scene)
  GREY   = muscle fibre, membranes, axes, labels, de-emphasized
"""
import numpy as np
from bp_style import *  # noqa: F401,F403

ORANGE = "#F29E4C"
PURPLE = "#B58CD9"
PINK = "#E88FC0"

BASE_Y = -1.4      # resting level on the trace panel
Q_VIS = 0.7        # height of one miniature on the trace panel (sketch)


def arr(a, b, color=GREY, w=4, tip=0.2):
    return Arrow(a, b, buff=0.06, color=color, stroke_width=w, tip_length=tip,
                 max_tip_length_to_length_ratio=0.45, max_stroke_width_to_length_ratio=12)


def packet(r=0.24, dot=0.065, color=YELLOW, rings=1):
    """a quantum: a cluster of transmitter dots (hex packing), not a molecule."""
    pts = [np.array([0.0, 0.0, 0.0])]
    for k in range(1, rings + 1):
        for j in range(6 * k):
            ang = 2 * np.pi * j / (6 * k)
            pts.append(np.array([np.cos(ang), np.sin(ang), 0.0]) * r * k)
    g = VGroup(*[Dot(p, radius=dot, color=color) for p in pts])
    return g


_F = lambda s: np.exp(-s / 0.22) - np.exp(-s / 0.04)
_PEAK = max(_F(s) for s in np.linspace(0.001, 1.0, 400))


def blip_y(x, x0, h):
    t = x - x0
    if t < 0:
        return 0.0
    return h * _F(t) / _PEAK


def trace_from(blips, x0=1.0, x1=6.2, base=BASE_Y, dx=0.01):
    xs = np.arange(x0, x1 + 1e-9, dx)
    ys = np.array([base + sum(blip_y(x, bx, h) for bx, h in blips) for x in xs])
    m = VMobject(stroke_color=GREEN, stroke_width=4)
    m.set_points_as_corners([[x, y, 0] for x, y in zip(xs, ys)])
    return m


BLIPS = [(1.4, 1.0 * Q_VIS), (2.25, 0.95 * Q_VIS), (2.65, 1.05 * Q_VIS), (3.75, 1.0 * Q_VIS),
         (4.7, 0.94 * Q_VIS), (5.45, 1.02 * Q_VIS)]


class Stage:
    """nerve terminal over a muscle fibre with an intracellular electrode (cells as simple shapes)."""

    def __init__(self):
        self.axon = RoundedRectangle(corner_radius=0.2, width=1.45, height=0.55, stroke_color=BLUE, stroke_width=3,
                                     fill_color=BLUE, fill_opacity=0.18).move_to([-5.55, 2.2, 0])
        self.term = RoundedRectangle(corner_radius=0.55, width=3.4, height=1.7, stroke_color=BLUE, stroke_width=3,
                                     fill_color=BLUE, fill_opacity=0.18).move_to([-3.3, 2.2, 0])
        self.muscle = RoundedRectangle(corner_radius=0.15, width=5.7, height=2.8, stroke_color=GREY, stroke_width=3,
                                       fill_color=GREY, fill_opacity=0.14).move_to([-3.3, -0.45, 0])
        self.term_lbl = T("nerve terminal", 22, BLUE).move_to([-3.3, 2.7, 0])
        self.mus_lbl = T("muscle fibre", 22, GREY).move_to([-1.9, -1.45, 0])
        self.end_lbl = T("endplate", 22, GREY).move_to([-3.3, -0.1, 0])
        self.el_line = Line([-6.0, -3.3, 0], [-4.7, -0.5, 0], color=TEXT, stroke_width=3)
        self.tip = Dot([-4.7, -0.5, 0], radius=0.08, color=TEXT)
        self.el_lbl = T("electrode", 22, TEXT).move_to([-4.55, -2.95, 0])
        self.nostim = T("nerve not stimulated", 22, GREY).move_to([-4.7, 3.3, 0])
        self.body = VGroup(self.axon, self.term, self.muscle, self.term_lbl, self.mus_lbl, self.end_lbl,
                           self.el_line, self.tip, self.el_lbl)


def panel_axes():
    yax = Line([1.0, -2.4, 0], [1.0, 2.9, 0], color=GREY, stroke_width=3)
    xax = Line([1.0, -2.4, 0], [6.2, -2.4, 0], color=GREY, stroke_width=3)
    ylab = T("voltage, mV", 22, GREY).rotate(PI / 2).move_to([0.55, 0.25, 0])
    xlab = T("time", 22, GREY).move_to([5.7, -2.8, 0])
    note = T("in this sketch", 22, GREY).move_to([3.0, -3.25, 0])
    return VGroup(yax, xax, ylab, xlab, note)


def solution_chips():
    c1 = chip("less calcium", TEAL, 22)
    c2 = chip("more magnesium", PURPLE, 22)
    return VGroup(c1, c2).arrange(RIGHT, buff=0.25).move_to([3.5, 3.1, 0])


def thr_line():
    ln = DashedLine([1.0, 2.4, 0], [6.2, 2.4, 0], color=ORANGE, stroke_width=3)
    lb = T("fires the fibre", 22, ORANGE).move_to([4.95, 2.68, 0])
    return VGroup(ln, lb)


# ---- trial grid (twelve impulses at low release; heights are multiples of one miniature) ----
PATTERN = [0, 1, 0, 2, 0, 1, 3, 0, 1, 2, 0, 1]
BW, BH, GAP = 1.2, 1.3, 0.1
UNIT = 0.26


def trial_box(n, cx, cy):
    box = Rectangle(width=BW, height=BH, stroke_color=GREY, stroke_width=2).move_to([cx, cy, 0])
    by = cy - BH / 2 + 0.3
    xs = np.arange(0, BW - 0.2, 0.01)
    pts = []
    for x in xs:
        y = by + (blip_y(x, 0.2, n * UNIT) if n else 0.0)
        pts.append([cx - BW / 2 + 0.1 + x, y, 0])
    tr = VMobject(stroke_color=(GREEN if n else GREY), stroke_width=3.5)
    tr.set_points_as_corners(pts)
    return VGroup(box, tr)


def trial_grid(cx0=1.6, cy0=1.85):
    boxes = []
    for i, n in enumerate(PATTERN):
        r, c = divmod(i, 4)
        boxes.append(trial_box(n, cx0 + c * (BW + GAP), cy0 - r * (BH + GAP)))
    return boxes


# ---- bar of quanta (response in mV) ----
MV = 0.24
BASE_B = -3.0
BAR_X = -2.6


def stripes(n, q, color=GREEN):
    rs = []
    for i in range(n):
        h = q * MV
        r = Rectangle(width=2.0, height=h, stroke_width=0, fill_color=color, fill_opacity=0.9 if i % 2 == 0 else 0.55)
        r.move_to([BAR_X, BASE_B + h * i + h / 2, 0])
        rs.append(r)
    return VGroup(*rs)


def bar_axes():
    ax = Line([-4.3, BASE_B, 0], [-4.3, 3.1, 0], color=GREY, stroke_width=3)
    base = Line([-4.3, BASE_B, 0], [-0.9, BASE_B, 0], color=GREY, stroke_width=3)
    ticks = VGroup()
    for v in (0, 12, 24):
        y = BASE_B + v * MV
        ticks.add(Line([-4.4, y, 0], [-4.3, y, 0], color=GREY, stroke_width=3))
        ticks.add(M(str(v), 22, GREY).move_to([-4.75, y, 0]))
    ylab = T("response, mV", 22, GREY).rotate(PI / 2).move_to([-5.6, 0.2, 0])
    return VGroup(ax, base, ticks, ylab)


def thr_bar():
    y = BASE_B + 12 * MV
    ln = DashedLine([-4.3, y, 0], [6.0, y, 0], color=ORANGE, stroke_width=3)
    lb = T("fires at 12 mV (illustration)", 24, ORANGE).move_to([2.9, y + 0.33, 0])
    return VGroup(ln, lb)


class S00Title(TitleCard):
    LESSON = "Synaptic transmission and quantal release"
    TITLE = "Release comes in countable packets"


# ---------------------------------------------------------------------------------------------
class S01Blips(SpokenScene):
    """electrode in a resting frog fibre at the endplate; the nerve is not stimulated; small equal blips arrive at random."""

    def construct(self):
        st = Stage()
        self.at("Put an electrode")
        self.play(FadeIn(st.muscle), FadeIn(st.term), FadeIn(st.axon), FadeIn(st.mus_lbl), FadeIn(st.term_lbl), run_time=0.8)
        self.at("inside a resting")
        self.play(Create(st.el_line), FadeIn(st.tip), FadeIn(st.el_lbl), run_time=0.9)
        self.at("where the nerve ends")
        self.play(FadeIn(st.end_lbl), run_time=0.4)
        self.at("Stimulate nothing")
        self.play(FadeIn(st.nostim), run_time=0.5)

        ax = panel_axes()
        tr = trace_from(BLIPS)
        self.at("Small depolarizations")
        self.play(FadeIn(ax), run_time=0.5)
        t_end = self.t_of("far too small") - 0.5
        self.play(Create(tr, rate_func=linear), run_time=max(1.0, t_end - self.elapsed()))
        self.at("far too small")
        thr = thr_line()
        self.play(Create(thr[0]), FadeIn(thr[1]), run_time=0.7)
        self.at("What are they")
        q = T("?", 96, TEXT, weight=BOLD).move_to([3.6, 0.7, 0])
        self.play(FadeIn(q, scale=0.6), Indicate(tr, color=GREEN, scale_factor=1.0), run_time=0.9)
        self.finish()


# ---------------------------------------------------------------------------------------------
class S02Packet(SpokenScene):
    """a packet leaves as a blip appears; an impulse; less calcium, more magnesium; a grid of trials with failures."""

    def construct(self):
        st = Stage()
        ax = panel_axes()
        tr = trace_from(BLIPS)
        thr = thr_line()
        self.add(st.body, st.nostim, ax, tr, thr)

        self.at("These are miniature")
        lab = T("miniature endplate potential", 24, GREEN).move_to([3.4, 0.55, 0])
        pt = arr([3.75, 0.2, 0], [3.75, BASE_Y + Q_VIS + 0.12, 0], GREEN)
        self.play(FadeIn(lab), GrowArrow(pt), run_time=0.7)

        self.at("spontaneous release")
        pk = [packet().move_to([x, 1.95, 0]) for x in (-4.3, -3.3, -2.3)]
        ach = T("acetylcholine", 22, YELLOW).move_to([-3.3, 2.7, 0])
        self.play(FadeOut(lab), FadeOut(pt), FadeOut(st.nostim), ReplacementTransform(st.term_lbl, ach),
                  *[FadeIn(p, scale=0.6) for p in pk], run_time=0.8)
        out = pk[2].copy()
        ring = Circle(radius=0.15, color=GREEN, stroke_width=4).move_to([-2.3, 1.15, 0])
        self.play(out.animate.move_to([-2.3, 1.15, 0]), run_time=0.7)
        nb1 = trace_from([(3.2, Q_VIS)], x0=3.2, x1=4.1)
        nb1.set_stroke(YELLOW, 6)
        self.play(FadeOut(out), ring.animate.scale(4).set_stroke(opacity=0), Create(nb1, rate_func=linear), run_time=0.8)
        self.play(nb1.animate.set_stroke(GREEN, 4), run_time=0.3)

        self.at("from the nerve terminal")
        out2 = pk[0].copy()
        ring2 = Circle(radius=0.15, color=GREEN, stroke_width=4).move_to([-4.3, 1.15, 0])
        self.play(out2.animate.move_to([-4.3, 1.15, 0]), run_time=0.7)
        nb2 = trace_from([(4.15, Q_VIS)], x0=4.15, x1=4.65)
        nb2.set_stroke(YELLOW, 6)
        self.play(FadeOut(out2), ring2.animate.scale(4).set_stroke(opacity=0), Create(nb2, rate_func=linear), run_time=0.8)
        self.play(nb2.animate.set_stroke(GREEN, 4), run_time=0.3)

        self.at("nerve impulse")
        boxes = trial_grid()
        leg = T("each box: one nerve impulse, in this sketch", 22, GREY).move_to([3.55, -3.2, 0])
        self.play(FadeOut(ax), FadeOut(tr), FadeOut(thr), FadeOut(nb1), FadeOut(nb2), run_time=0.6)
        imp_lbl = T("nerve impulse", 22, TEXT).move_to([-5.3, 3.3, 0])
        pulse = Dot([-6.1, 2.2, 0], radius=0.17, color=TEXT)
        self.play(FadeIn(imp_lbl), FadeIn(pulse), LaggedStart(*[FadeIn(b[0]) for b in boxes], lag_ratio=0.05), FadeIn(leg), run_time=0.9)
        self.play(pulse.animate.move_to([-4.6, 2.2, 0]), run_time=0.6)
        self.play(FadeOut(pulse), run_time=0.2)

        self.at("They bathed")
        chips = solution_chips()
        self.play(FadeIn(chips, shift=DOWN * 0.15), run_time=0.7)
        self.at("a trickle")
        self.play(FadeOut(pk[0]), FadeOut(pk[2]), run_time=0.8)

        self.at("Now an impulse")
        self.play(LaggedStart(*[Create(b[1]) for b in boxes], lag_ratio=0.15), run_time=1.8)
        self.at("a failure")
        empties = [b for b, n in zip(boxes, PATTERN) if n == 0]
        fl = T("no response: a failure", 26, RED, weight=BOLD).move_to([3.55, -2.45, 0])
        self.play(*[b[0].animate.set_stroke(RED, 4) for b in empties], *[b[1].animate.set_color(RED) for b in empties], FadeIn(fl), run_time=0.7)
        self.finish()


# ---------------------------------------------------------------------------------------------
def s2_end_state(scene):
    """what S02 leaves on screen (rebuilt in the same place)."""
    st = Stage()
    ach = T("acetylcholine", 22, YELLOW).move_to([-3.3, 2.7, 0])
    body = VGroup(st.axon, st.term, st.muscle, st.mus_lbl, st.end_lbl, st.el_line, st.tip, st.el_lbl, ach)
    pk = packet().move_to([-3.3, 1.95, 0])
    imp = T("nerve impulse", 22, TEXT).move_to([-5.3, 3.3, 0])
    chips = solution_chips()
    boxes = trial_grid()
    for b, n in zip(boxes, PATTERN):
        if n == 0:
            b[0].set_stroke(RED, 4)
            b[1].set_color(RED)
    leg = T("each box: one nerve impulse, in this sketch", 22, GREY).move_to([3.55, -3.2, 0])
    fl = T("no response: a failure", 26, RED, weight=BOLD).move_to([3.55, -2.45, 0])
    side = VGroup(body, pk, imp, chips, leg, fl)
    scene.add(side, *boxes)
    return side, boxes


COLX = [1.8, 3.1, 4.4, 5.7]
BASE_H = -2.0


class S03Steps(SpokenScene):
    """the twelve trials sort into columns at 0, 1, 2, 3 miniatures; then one quantum: a packet, one vesicle, not one molecule."""

    def construct(self):
        side, boxes = s2_end_state(self)
        grid = VGroup(*boxes)

        self.at("When a response did come")
        fails = [b for b, n in zip(boxes, PATTERN) if n == 0]

        self.at("its size was not random")
        self.play(FadeOut(side), grid.animate.scale(0.9).move_to([-3.3, 0.3, 0]), run_time=1.0)
        base = Line([1.0, BASE_H, 0], [6.2, BASE_H, 0], color=GREY, stroke_width=3)
        labs = [M(s, 26, c).move_to([x, -2.45, 0]) for s, c, x in zip(["0", "1x", "2x", "3x"], [RED, GREEN, GREEN, GREEN], COLX)]
        axt = T("size of response, in miniatures", 22, GREY).move_to([3.6, -3.0, 0])
        skn = T("in this sketch", 22, GREY).move_to([3.6, -3.4, 0])
        self.play(Create(base), FadeIn(VGroup(*labs)), FadeIn(axt), FadeIn(skn), run_time=0.8)

        self.at("The amplitudes clustered")
        dots, tgt = [], []
        count = [0, 0, 0, 0]
        for b, n in zip(boxes, PATTERN):
            d = Dot(b.get_center(), radius=0.27, color=RED if n == 0 else GREEN)
            dots.append(d)
            tgt.append([COLX[n], BASE_H + 0.36 + 0.62 * count[n], 0])
            count[n] += 1
        self.play(*[FadeIn(d, scale=0.5) for d in dots], run_time=0.5)
        self.play(LaggedStart(*[d.animate.move_to(t) for d, t in zip(dots, tgt)], lag_ratio=0.1), run_time=2.2)

        cols = {1: [dots[i] for i, n in enumerate(PATTERN) if n == 1], 2: [dots[i] for i, n in enumerate(PATTERN) if n == 2],
                3: [dots[i] for i, n in enumerate(PATTERN) if n == 3]}

        def box_col(k):
            return SurroundingRectangle(VGroup(labs[k], *cols[k]), color=GREEN, buff=0.15, stroke_width=4)
        self.at("one miniature")
        hb = box_col(1)
        self.play(Create(hb), run_time=0.5)
        self.at("twice that")
        hb2 = box_col(2)
        self.play(FadeOut(hb), Create(hb2), run_time=0.5)
        self.at("three times")
        hb3 = box_col(3)
        self.play(FadeOut(hb2), Create(hb3), run_time=0.5)
        self.play(FadeOut(hb3), run_time=0.4)

        self.at("Each packet is a quantum")
        self.play(FadeOut(grid), run_time=0.5)
        pk = packet(r=0.33, dot=0.13, rings=2).move_to([-3.3, 0.3, 0])
        ql = T("one quantum", 34, YELLOW, weight=BOLD).move_to([-3.3, 2.75, 0])
        self.play(LaggedStart(*[FadeIn(d, scale=0.3) for d in pk], lag_ratio=0.04), FadeIn(ql), run_time=1.0)

        self.at("later identified")
        ves = Circle(radius=1.35, color=GREY, stroke_width=5).move_to([-3.3, 0.3, 0])
        vl = T("one vesicle", 26, GREY).move_to([-3.3, 1.95, 0])
        self.play(Create(ves), FadeIn(vl), run_time=0.9)

        self.at("not one molecule")
        one = pk[-1]
        ring = Circle(radius=0.19, color=RED, stroke_width=5).move_to(one.get_center())
        rl = T("not one molecule", 28, RED, weight=BOLD).move_to([-3.3, -1.5, 0])
        self.play(Create(ring), FadeIn(rl, shift=UP * 0.1), run_time=0.8)
        self.finish()


# ---------------------------------------------------------------------------------------------
def s4_left():
    hdr = T("ratio of means", 24, GREY).move_to([-3.3, 1.4, 0])
    h = 0.40 * 4.0
    b1 = Rectangle(width=1.3, height=h, stroke_color=GREEN, stroke_width=3, fill_color=GREEN, fill_opacity=0.5).move_to([-4.6, -0.9 + h / 2, 0])
    b2 = Rectangle(width=1.3, height=h, stroke_color=GREEN, stroke_width=3, fill_color=GREEN, fill_opacity=0.5).move_to([-2.0, -0.9 + h / 2, 0])
    l1 = T("mean miniature\n0.40 mV", 22, GREEN, line_spacing=0.8).move_to([-4.6, -1.55, 0])
    l2 = T("mean response\nfailures included\n0.40 mV", 22, GREEN, line_spacing=0.8).move_to([-2.0, -1.75, 0])
    eq = M("m = 0.40 / 0.40 = 1.00", 26, TEXT).move_to([-3.3, -2.9, 0])
    return hdr, b1, b2, l1, l2, eq


def s4_right():
    hdr = T("failures", 24, GREY).move_to([3.6, 1.4, 0])
    cells = VGroup()
    for i in range(200):
        r, c = divmod(i, 20)
        cells.add(Square(side_length=0.2, stroke_width=0, fill_color=GREY, fill_opacity=0.45).move_to([1.4 + c * 0.22, 1.05 - r * 0.22, 0]))
    l1 = T("200 stimuli, 74 gave no response", 22, RED).move_to([3.6, -1.3, 0])
    eq = M("74 / 200 = 0.37", 26, TEXT).move_to([3.6, -2.2, 0])
    return hdr, cells, l1, eq


def fill_failures(cells):
    return [cells[i].animate.set_fill(RED, 0.9) for i in range(74)]


class S04Count(SpokenScene):
    """two bars of equal height give m = 1.00; a grid of 200 stimuli with 74 failures gives 0.37."""

    def construct(self):
        self.at("The mean quantal content")
        defn = T("mean quantal content, m = average number of quanta per impulse", 28, TEXT).move_to([0, 3.05, 0])
        self.play(FadeIn(defn, shift=DOWN * 0.1), run_time=0.8)

        self.at("the average number")
        rowb = VGroup()
        for cx, k in zip([-4.0, -2.4, -0.8, 0.8, 2.4, 4.0], [1, 0, 2, 1, 3, 0]):
            bx = Rectangle(width=1.4, height=1.5, stroke_color=GREY, stroke_width=2).move_to([cx, 0.6, 0])
            rowb.add(bx)
            for j in range(k):
                rowb.add(packet(r=0.13, dot=0.05).move_to([cx + (j - (k - 1) / 2) * 0.42, 0.6, 0]))
        cap = T("quanta released by each nerve impulse", 24, GREY).move_to([0, -0.5, 0])
        avg = T("their average is the mean quantal content", 28, TEXT).move_to([0, -1.4, 0])
        self.play(LaggedStart(*[FadeIn(m) for m in rowb], lag_ratio=0.04), FadeIn(cap), run_time=1.4)
        self.at("one impulse releases")
        self.play(FadeIn(avg, shift=UP * 0.1), run_time=0.6)
        self.at("Take a made")
        self.play(FadeOut(VGroup(rowb, cap, avg)), run_time=0.5)
        self.at("frog junction in low")
        c0 = chip("made-up frog junction", GREY, 22)
        c1 = chip("low calcium", TEAL, 22)
        c2 = chip("high magnesium", PURPLE, 22)
        row = VGroup(c0, c1, c2).arrange(RIGHT, buff=0.3).move_to([0, 2.3, 0])
        self.play(LaggedStart(*[FadeIn(c, shift=DOWN * 0.1) for c in (c0, c1, c2)], lag_ratio=0.3), run_time=1.2)

        hdr, b1, b2, l1, l2, eq = s4_left()
        self.at("The mean miniature")
        self.play(FadeIn(hdr), GrowFromEdge(b1, DOWN), FadeIn(l1), run_time=0.8)
        self.at("and the mean response")
        self.play(GrowFromEdge(b2, DOWN), FadeIn(l2), run_time=0.8)
        self.at("So the ratio")
        brace = DashedLine(b1.get_corner(UR) + [0.05, 0, 0], b2.get_corner(UL) + [-0.05, 0, 0], color=TEXT, stroke_width=3)
        self.play(Create(brace), run_time=0.4)
        self.play(FadeIn(eq, shift=UP * 0.1), run_time=0.6)

        rh, cells, rl, req = s4_right()
        self.at("Failures give a second")
        self.play(FadeIn(rh), FadeIn(cells), run_time=0.8)
        self.at("stimuli gave")
        self.play(LaggedStart(*fill_failures(cells), lag_ratio=0.015), run_time=1.3)
        self.at("no response")
        self.play(FadeIn(rl), run_time=0.4)
        self.play(FadeIn(req, shift=UP * 0.1), run_time=0.6)
        self.finish()


class S05Safety(SpokenScene):
    """the failure estimate agrees; then normal calcium: a bar of sixty quanta against the level that fires, safety factor 2."""

    def construct(self):
        defn = T("mean quantal content, m = average number of quanta per impulse", 28, TEXT).move_to([0, 3.05, 0])
        c0 = chip("made-up frog junction", GREY, 22)
        c1 = chip("low calcium", TEAL, 22)
        c2 = chip("high magnesium", PURPLE, 22)
        row = VGroup(c0, c1, c2).arrange(RIGHT, buff=0.3).move_to([0, 2.3, 0])
        hdr, b1, b2, l1, l2, eq = s4_left()
        brace = DashedLine(b1.get_corner(UR) + [0.05, 0, 0], b2.get_corner(UL) + [-0.05, 0, 0], color=TEXT, stroke_width=3)
        rh, cells, rl, req = s4_right()
        for i in range(74):
            cells[i].set_fill(RED, 0.9)
        self.add(defn, row, hdr, b1, b2, l1, l2, brace, eq, rh, cells, rl, req)

        self.at("Under a Poisson model")
        req2 = M("m = -ln(0.37) = 0.99", 26, TEXT).move_to([3.6, -2.9, 0])
        self.play(FadeIn(req2, shift=UP * 0.1), run_time=0.8)
        self.at("The two estimates agree")
        r1 = SurroundingRectangle(eq, color=GREEN, buff=0.12, stroke_width=3)
        r2 = SurroundingRectangle(req2, color=GREEN, buff=0.12, stroke_width=3)
        ag = T("agree", 30, GREEN, weight=BOLD).move_to([0.15, -2.9, 0])
        self.play(Create(r1), Create(r2), FadeIn(ag), run_time=0.8)

        self.at("Now restore normal calcium")
        self.play(FadeOut(VGroup(defn, row, hdr, b1, b2, l1, l2, brace, eq, rh, cells, rl, req, req2, r1, r2, ag)), run_time=0.7)
        axes = bar_axes()
        self.play(FadeIn(axes), run_time=0.5)
        self.at("and suppose")
        bar = stripes(60, 0.40)
        t1 = M("60 quanta x 0.40 mV", 28, GREEN).move_to([2.9, 2.5, 0])
        self.play(LaggedStart(*[FadeIn(r, shift=UP * 0.08) for r in bar], lag_ratio=0.02), FadeIn(t1), run_time=1.6)
        self.at("If they add linearly")
        t3 = T("if quanta add linearly", 22, GREY).move_to([2.9, 1.15, 0])
        self.play(FadeIn(t3), run_time=0.4)
        self.at("the response is")
        t2 = M("= 24 mV", 28, GREEN).move_to([2.9, 1.8, 0])
        self.play(FadeIn(t2, shift=UP * 0.1), run_time=0.5)
        self.at("fires at")
        thr = thr_bar()
        self.play(Create(thr[0]), FadeIn(thr[1]), run_time=0.8)
        self.at("The safety factor")
        y0, y1 = BASE_B + 12 * MV, BASE_B + 24 * MV
        dbl = DoubleArrow([-0.95, y0, 0], [-0.95, y1, 0], color=ORANGE, buff=0, stroke_width=4, tip_length=0.2)
        sf1 = T("safety factor", 28, ORANGE).move_to([2.9, -0.85, 0])
        sf2 = M("24 / 12 = 2.0", 28, ORANGE).move_to([2.9, -1.5, 0])
        self.play(GrowFromCenter(dbl), FadeIn(sf1), run_time=0.7)
        self.at("the ratio of the two")
        self.play(FadeIn(sf2, shift=UP * 0.1), run_time=0.6)
        self.finish()


class S06Where(SpokenScene):
    """smaller quanta still fire; fewer quanta fail; size depends on filling and receptors; rule: size points after, number before."""

    def construct(self):
        axes = bar_axes()
        bar = stripes(60, 0.40)
        thr = thr_bar()
        t1 = M("60 quanta x 0.40 mV", 28, GREEN).move_to([2.9, 2.5, 0])
        t2 = M("= 24 mV", 28, GREEN).move_to([2.9, 1.8, 0])
        t3 = T("if quanta add linearly", 22, GREY).move_to([2.9, 1.15, 0])
        y0, y1 = BASE_B + 12 * MV, BASE_B + 24 * MV
        dbl = DoubleArrow([-0.95, y0, 0], [-0.95, y1, 0], color=ORANGE, buff=0, stroke_width=4, tip_length=0.2)
        sf1 = T("safety factor", 28, ORANGE).move_to([2.9, -0.85, 0])
        sf2 = M("24 / 12 = 2.0", 28, ORANGE).move_to([2.9, -1.5, 0])
        self.add(axes, bar, thr, t1, t2, t3, dbl, sf1, sf2)

        self.at("fewer receptors")
        chm = chip("myasthenia gravis", GREY, 24).move_to([2.9, 3.0, 0])
        self.play(FadeOut(VGroup(t1, t2, t3, dbl, sf1, sf2)), run_time=0.6)
        rec = T("fewer receptors", 30, PINK, weight=BOLD).move_to([2.9, 2.3, 0])
        self.play(FadeIn(chm, shift=DOWN * 0.1), FadeIn(rec), run_time=0.6)
        self.at("smaller quantal size")
        small = stripes(60, 0.24)
        qs = M("quantal size 0.24 mV", 26, PINK).move_to([2.9, 1.7, 0])
        self.play(Transform(bar, small), FadeIn(qs), run_time=1.2)
        self.at("of them still")
        r1 = M("60 x 0.24 = 14.4 mV", 26, GREEN).move_to([2.9, 1.1, 0])
        r2 = T("still fires", 30, GREEN, weight=BOLD).move_to([2.9, -0.8, 0])
        self.play(FadeIn(r1, shift=UP * 0.1), run_time=0.5)
        self.play(FadeIn(r2), run_time=0.4)
        self.at("But suppose")
        hedge = T("suppose release runs down:\n25 percent fewer quanta, 60 to 45", 24, RED, line_spacing=0.8).move_to([2.9, -1.85, 0])
        self.play(FadeIn(hedge, shift=UP * 0.1), run_time=0.6)
        self.at("The response is then")
        fewer = stripes(45, 0.24, RED)
        f1 = M("45 x 0.24 = 10.8 mV", 26, RED).move_to([2.9, 1.1, 0])
        f2 = T("the fibre fails", 30, RED, weight=BOLD).move_to([2.9, -0.8, 0])
        self.play(Transform(bar, fewer), ReplacementTransform(r1, f1), ReplacementTransform(r2, f2), run_time=1.2)

        self.at("vesicle filling")
        self.play(FadeOut(VGroup(chm, rec, qs, f1, f2, thr, hedge)), run_time=0.6)
        va = chip("vesicle filling", YELLOW, 26).move_to([0.9, 2.3, 0])
        vb = chip("receptors", PINK, 26).move_to([4.7, 2.3, 0])
        vm = chip("miniature size", GREEN, 28).move_to([2.8, 0.7, 0])
        a1 = arr(va.get_bottom(), vm.get_top() + [-0.5, 0, 0], YELLOW)
        a2 = arr(vb.get_bottom(), vm.get_top() + [0.5, 0, 0], PINK)
        self.play(FadeIn(va, shift=DOWN * 0.1), FadeIn(vb, shift=DOWN * 0.1), run_time=0.6)
        self.play(GrowArrow(a1), GrowArrow(a2), FadeIn(vm), run_time=0.7)
        self.at("receptor count")
        chk = T("pair it with a receptor count", 24, GREY).move_to([2.8, -0.35, 0])
        self.play(FadeIn(chk, shift=UP * 0.1), run_time=0.5)

        self.at("Even so")
        self.play(FadeOut(VGroup(axes, bar, va, vb, vm, a1, a2, chk)), run_time=0.7)

        def card(cx, header, hcolor, n_pk, scale_pk):
            hd = T(header, 34, hcolor, weight=BOLD).move_to([cx, 3.0, 0])
            term = RoundedRectangle(corner_radius=0.5, width=4.0, height=1.5, stroke_color=BLUE, stroke_width=3,
                                    fill_color=BLUE, fill_opacity=0.18).move_to([cx, 1.65, 0])
            tl = T("nerve terminal", 22, BLUE).move_to([cx, 2.1, 0])
            mus = RoundedRectangle(corner_radius=0.15, width=5.4, height=2.0, stroke_color=GREY, stroke_width=3,
                                   fill_color=GREY, fill_opacity=0.14).move_to([cx, -0.55, 0])
            ml = T("muscle fibre", 22, GREY).move_to([cx, -1.15, 0])
            pks = VGroup(*[packet().scale(scale_pk).move_to([cx + dx, 1.3, 0]) for dx in ([-1.0, 0, 1.0] if n_pk == 3 else [0])])
            return hd, term, tl, mus, ml, pks

        h1, t_1, tl1, m1, ml1, p1 = card(-3.2, "smaller packets", YELLOW, 3, 0.4)
        self.at("smaller packets")
        self.play(FadeIn(VGroup(h1, t_1, tl1, m1, ml1, p1)), run_time=0.8)
        self.at("after the synapse")
        lb1 = T("points after the synapse", 30, GOLD, weight=BOLD).move_to([-3.2, -2.3, 0])
        self.play(m1.animate.set_stroke(GOLD, 7), FadeIn(lb1, shift=UP * 0.1), run_time=0.8)
        h2, t_2, tl2, m2, ml2, p2 = card(3.2, "fewer packets", YELLOW, 1, 1.0)
        self.at("fewer packets")
        self.play(FadeIn(VGroup(h2, t_2, tl2, m2, ml2, p2)), run_time=0.8)
        self.at("before it")
        lb2 = T("points before it", 30, GOLD, weight=BOLD).move_to([3.2, -2.3, 0])
        self.play(t_2.animate.set_stroke(GOLD, 7), FadeIn(lb2, shift=UP * 0.1), run_time=0.8)
        self.finish()


class S07End(EndCard):
    LINE = "Smaller packets point after the synapse; fewer packets point before it."
