"""Recording many neurons: recorded is not counted  (Biochemistrypedia explainer)

Timed to the SPOKEN words: every self.at("...") cue waits for that phrase in audio/words.json.

COLOR MAP (one color per concept, whole video)
  GREY   = the probe, its recording sites, tree lines, trial dots, de-emphasised things
  BLUE   = a neuron, and "neurons" as a count
  TEAL   = a signal picked up on a site / channels addressed at one time
  YELLOW = a sorted unit (an inference) and its rate
  ORANGE = mouse A
  PINK   = mouse B
  PURPLE = a session
  RED    = the wrong count (crossed out, 24 unit-trials, pooled rate, pseudoreplication)
  GREEN  = the right count (the animal level: n = 2, the animal mean) and the animals level
"""
import numpy as np
from bp_style import *  # noqa: F401,F403

PURPLE = "#B58CD9"
ORANGE = "#F29E4C"
PINK = "#E58FB5"


# ---------------------------------------------------------------------------------------------
# helpers
# ---------------------------------------------------------------------------------------------
def bchip(text, color=BLUE, size=26, **kw):
    """chip with an opaque backing so lines drawn behind it do not show through."""
    c = chip(text, color, size=size, **kw)
    back = RoundedRectangle(corner_radius=0.14, width=c[0].width, height=c[0].height, stroke_width=0,
                            fill_color=BG, fill_opacity=1).move_to(c[0])
    return VGroup(back, *c)


def neuron(color=BLUE, r=0.34, nd=3):
    """a simple neuron: round cell body with a few short dendrite lines."""
    soma = Circle(radius=r, stroke_color=color, stroke_width=4, fill_color=color, fill_opacity=0.35)
    lines = []
    for k in range(nd):
        ang = 2 * PI * k / nd + PI / 6
        d = np.array([np.cos(ang), np.sin(ang), 0])
        lines.append(Line(d * r, d * (r + 0.36), color=color, stroke_width=4))
    g = VGroup(soma, *lines)
    g.soma = soma
    return g


def spike_glyph(w=1.1, h=0.7, color=TEAL):
    """a small spike-shaped waveform (a sketch, not a recording)."""
    xs = np.array([0, .18, .3, .38, .44, .52, .62, .8, 1.0]) * w
    ys = np.array([0, 0, -.12, .15, 1.0, -.55, -.12, 0, 0]) * h
    m = VMobject(color=color, stroke_width=4)
    m.set_points_as_corners([[x - w / 2, y, 0] for x, y in zip(xs, ys)])
    return m


def link(a, b, color=GREY, w=3, op=1.0):
    return Line(a, b, color=color, stroke_width=w, stroke_opacity=op)


def shout(mob, color, s=1.12):
    return Indicate(mob, color=color, scale_factor=s)


class S00Title(TitleCard):
    LESSON = "Recording many neurons"
    TITLE = "Recorded is not counted"


# ---------------------------------------------------------------------------------------------
class S01Probe(SpokenScene):
    """A probe with 960 sites does not record 960 neurons: 384 at a time, more than 700 with two probes."""

    def construct(self):
        cx = -3.0
        shank = Polygon([cx - .38, 3.35, 0], [cx + .38, 3.35, 0], [cx + .38, -2.9, 0], [cx, -3.45, 0], [cx - .38, -2.9, 0],
                        stroke_color=GREY, stroke_width=3, fill_color=GREY, fill_opacity=0.18)
        sites = VGroup()
        ys = np.arange(3.05, -2.8, -0.3)
        for y in ys:
            for dx in (-0.14, 0.14):
                sites.add(Square(0.13, stroke_color=GREY, stroke_width=2, fill_color=GREY, fill_opacity=0.55)
                          .move_to([cx + dx, y, 0]))
        probe = VGroup(shank, sites)
        lbrace = Brace(shank, direction=LEFT, color=GREY, buff=0.12)
        l_lbl = T("960 recording sites", 26, GREY).rotate(PI / 2).next_to(lbrace, LEFT, buff=0.15)

        self.at("recording sites")
        self.play(FadeIn(shank), LaggedStart(*[FadeIn(s) for s in sites], lag_ratio=0.02), run_time=1.4)
        self.play(GrowFromCenter(lbrace), FadeIn(l_lbl), run_time=0.7)

        q = bchip("960 neurons?", BLUE, 44).move_to([2.6, 2.4, 0])
        self.at("neurons")
        self.play(FadeIn(q, shift=LEFT * 0.2), run_time=0.5)
        self.at("No")
        cross = VGroup(Line(q.get_corner(UL), q.get_corner(DR), color=RED, stroke_width=7),
                       Line(q.get_corner(DL), q.get_corner(UR), color=RED, stroke_width=7))
        self.play(Create(cross), q[2].animate.set_opacity(0.85), run_time=0.5)

        # 384 addressed at a time: a band of the shank lights up
        band = Rectangle(width=0.95, height=2.46, stroke_color=TEAL, stroke_width=4, fill_color=TEAL, fill_opacity=0.28)
        band.move_to([cx, 0.2, 0])
        rbrace = Brace(band, direction=RIGHT, color=TEAL, buff=0.12)
        chip384 = bchip("384 at a time", TEAL, 34).next_to(rbrace, RIGHT, buff=0.25)
        self.at("address")
        self.play(FadeIn(band), GrowFromCenter(rbrace), run_time=0.6)
        self.play(FadeIn(chip384, shift=LEFT * 0.2), run_time=0.5)

        # the two-probe result
        p1 = T("2 probes, awake mouse", 28, GREY).move_to([2.6, -0.75, 0])
        self.at("Two probes")
        self.play(FadeIn(p1, shift=UP * 0.1), run_time=0.5)
        big = M("> 700", 56, BLUE)
        lab = T("well-isolated\nneurons at once", 26, BLUE, line_spacing=0.8)
        res = VGroup(big, lab).arrange(RIGHT, buff=0.35).move_to([2.6, -1.85, 0])
        self.at("neurons at once")
        self.play(FadeIn(res, shift=UP * 0.15), run_time=0.6)
        reg = T("from 5 brain structures", 28, GREY).move_to([2.6, -3.0, 0])
        self.at("brain structures")
        self.play(FadeIn(reg, shift=UP * 0.1), run_time=0.5)
        self.finish()


# ---------------------------------------------------------------------------------------------
SX = 0.0                                  # sites column x
SY = [2.0, 1.12, 0.24, -0.64, -1.52, -2.4]  # site rows


def site_column():
    col = VGroup()
    for y in SY:
        col.add(Square(0.34, stroke_color=GREY, stroke_width=3, fill_color=GREY, fill_opacity=0.5).move_to([SX, y, 0]))
    bar = RoundedRectangle(corner_radius=0.1, width=0.6, height=SY[0] - SY[-1] + 1.0, stroke_color=GREY, stroke_width=3,
                           fill_color=GREY, fill_opacity=0.15).move_to([SX, (SY[0] + SY[-1]) / 2, 0])
    return VGroup(bar, *col)


class S02Units(SpokenScene):
    """sites hear neurons; spike sorting makes units: merge two neurons, split one."""

    def construct(self):
        col = site_column()
        n1 = neuron(BLUE).move_to([-3.2, 1.1, 0])
        n2 = neuron(BLUE).move_to([3.4, -1.0, 0])
        n3 = neuron(BLUE).move_to([3.4, -2.6, 0])
        self.play(FadeIn(col), FadeIn(n1), FadeIn(n2), FadeIn(n3), run_time=0.8)

        sorter = bchip("spike sorting", YELLOW, 32)
        glyph = spike_glyph(1.0, 0.6, YELLOW)
        top = VGroup(sorter, glyph).arrange(RIGHT, buff=0.4).move_to([0, 3.05, 0])
        self.at("Spike sorting")
        self.play(FadeIn(top, shift=DOWN * 0.15), run_time=0.6)

        # one neuron on several sites
        sites = col[1:]
        l1 = [link(n1.soma.get_right(), sites[i].get_left(), TEAL, 4) for i in (0, 1, 2)]
        self.at("One neuron shows up")
        self.play(*[Create(l) for l in l1], *[sites[i].animate.set_fill(TEAL, 0.9).set_stroke(TEAL) for i in (0, 1, 2)],
                  run_time=0.7)
        lbl1 = T("one neuron, several sites", 24, TEAL).move_to([-3.2, -0.5, 0])
        self.play(FadeIn(lbl1), run_time=0.4)

        # one site hears two neurons
        l2 = [link(n2.soma.get_left(), sites[4].get_right(), TEAL, 4), link(n3.soma.get_left(), sites[4].get_right(), TEAL, 4)]
        self.at("one site hears")
        self.play(*[Create(l) for l in l2], sites[4].animate.set_fill(TEAL, 0.9).set_stroke(TEAL), run_time=0.7)
        lbl2 = T("one site, two neurons", 24, TEAL).move_to([3.4, 0.4, 0])
        self.play(FadeIn(lbl2), run_time=0.4)

        # merge two neurons into one unit
        box = SurroundingRectangle(VGroup(n2, n3), color=YELLOW, buff=0.25, corner_radius=0.15, stroke_width=5)
        ulab = T("one unit, two neurons", 24, YELLOW).next_to(box, UP, buff=0.12)
        self.at("merge two neurons")
        self.play(FadeOut(lbl2), Create(box), FadeIn(ulab), run_time=0.7)

        # split one neuron into two units
        ua = bchip("unit", YELLOW, 28).move_to([-5.45, 2.2, 0])
        ub = bchip("unit", YELLOW, 28).move_to([-5.45, 0.2, 0])
        a1 = Arrow(n1.get_left() + LEFT * 0.0, ua.get_right(), buff=0.1, color=YELLOW, stroke_width=4, tip_length=0.2)
        a2 = Arrow(n1.get_left(), ub.get_right(), buff=0.1, color=YELLOW, stroke_width=4, tip_length=0.2)
        self.at("or split one")
        lbl3 = T("one neuron, two units", 24, YELLOW).move_to([-4.6, -0.75, 0])
        self.play(FadeOut(lbl1), FadeIn(ua), FadeIn(ub), GrowArrow(a1), GrowArrow(a2), FadeIn(lbl3), run_time=0.8)

        # treat each unit as an inference
        self.at("inference")
        everything = VGroup(col, n1, n2, n3, box, ulab, ua, ub, a1, a2, lbl3, *l1, *l2, top)
        inf = bchip("a unit is an inference", YELLOW, 46)
        qs = bchip("quality scores", GREY, 34)
        grp = VGroup(inf, qs).arrange(DOWN, buff=0.5).move_to(ORIGIN)
        self.play(FadeOut(everything), run_time=0.5)
        self.play(FadeIn(inf, scale=0.9), run_time=0.5)
        self.at("quality scores")
        self.play(FadeIn(qs, shift=UP * 0.1), run_time=0.5)
        self.finish()


# ---------------------------------------------------------------------------------------------
LEAF_X = [-5.0 + 1.5 * i for i in range(6)]
Y_MOUSE, Y_SESS, Y_UNIT, Y_TRIAL = 2.75, 1.35, -0.05, -1.15
RX = 4.9
SESS_X = [(LEAF_X[0] + LEAF_X[1]) / 2, (LEAF_X[2] + LEAF_X[3]) / 2, LEAF_X[4], LEAF_X[5]]
MOUSE_X = [sum(LEAF_X[:4]) / 4, sum(LEAF_X[4:]) / 2]


def build_tree():
    mice = [bchip("mouse A", ORANGE, 26).move_to([MOUSE_X[0], Y_MOUSE, 0]),
            bchip("mouse B", PINK, 26).move_to([MOUSE_X[1], Y_MOUSE, 0])]
    sess = [bchip(f"S{i + 1}", PURPLE, 24, pad=0.16).move_to([SESS_X[i], Y_SESS, 0]) for i in range(4)]
    units = [bchip(f"U{i + 1}", YELLOW, 24, pad=0.16).move_to([LEAF_X[i], Y_UNIT, 0]) for i in range(6)]
    parent = [0, 0, 1, 1, 2, 3]   # unit -> session
    mparent = [0, 0, 1, 1]        # session -> mouse
    lines_ms = [link(mice[mparent[i]].get_bottom(), sess[i].get_top(), GREY, 3) for i in range(4)]
    lines_su = [link(sess[parent[i]].get_bottom(), units[i].get_top(), GREY, 3) for i in range(6)]
    return mice, sess, units, lines_ms, lines_su


def trial_dots(x):
    return VGroup(*[Dot(radius=0.07, color=GREY).move_to([x + dx, Y_TRIAL, 0]) for dx in (-0.33, -0.11, 0.11, 0.33)])


class S03Nest(SpokenScene):
    """a nested tree: 2 mice, 4 sessions, 6 units, 24 unit-trials; units in one mouse are not independent."""

    def construct(self):
        mice, sess, units, lms, lsu = build_tree()
        cnt = lambda txt, col, y: T(txt, 28, col).move_to([RX, y, 0])
        c_m, c_s = cnt("2 mice", TEXT, Y_MOUSE), cnt("4 sessions", PURPLE, Y_SESS)
        c_u, c_t = cnt("6 units", YELLOW, Y_UNIT), cnt("24 unit-trials", RED, Y_TRIAL)

        hold = VGroup(bchip("a unit is an inference", YELLOW, 46), bchip("quality scores", GREY, 34)).arrange(DOWN, buff=0.5).move_to(ORIGIN)
        self.add(hold)
        self.at("in an invented")
        self.play(FadeOut(hold), run_time=0.3)
        self.play(FadeIn(T("invented dataset", 26, GREY).to_corner(DL, buff=0.5)), run_time=0.5)
        self.at("Two mice")
        self.play(FadeIn(mice[0], shift=DOWN * 0.1), FadeIn(mice[1], shift=DOWN * 0.1), FadeIn(c_m), run_time=0.6)
        self.at("two sessions")
        self.play(*[Create(l) for l in lms], *[FadeIn(s) for s in sess], FadeIn(c_s), run_time=0.8)
        self.at("Each unit appears")
        self.play(*[Create(l) for l in lsu[:]], *[FadeIn(u) for u in units], run_time=0.8)
        self.at("Six units")
        self.play(FadeIn(c_u), run_time=0.4)
        dots = [trial_dots(x) for x in LEAF_X]
        self.at("four trials")
        self.play(*[FadeIn(d) for d in dots], run_time=0.6)
        self.at("make")
        self.play(FadeIn(c_t, shift=LEFT * 0.1), run_time=0.5)

        # not independent
        br = Brace(VGroup(*units[:4]), direction=DOWN, color=RED, buff=1.05)
        note = T("share one mouse's conditions", 26, RED).next_to(br, DOWN, buff=0.15)
        self.at("not independent")
        self.play(GrowFromCenter(br), FadeIn(note), run_time=0.7)
        self.finish()


# ---------------------------------------------------------------------------------------------
RATES = [8, 2, 4, 8, 2, 2]


class S04Rates(SpokenScene):
    """six unit rates; pooled 4.33 vs animal mean 3.75."""

    def construct(self):
        mice, sess, units, lms, lsu = build_tree()
        for s in sess:
            s.set_opacity(0.5)
        base = VGroup(*mice, *sess, *units, *lms, *lsu)
        # recolour mouse lines faintly, keep the same positions as in the last scene
        self.add(base)
        yr = Y_TRIAL - 0.1
        rate_lbl = T("spikes/s", 26, GREY).move_to([RX, yr, 0])
        rates = [M(str(r), 40, YELLOW).move_to([LEAF_X[i], yr, 0]) for i, r in enumerate(RATES)]
        self.at("spikes per second")
        self.play(FadeIn(rate_lbl), LaggedStart(*[FadeIn(r, shift=DOWN * 0.1) for r in rates], lag_ratio=0.15), run_time=1.6)

        # pooled
        pooled = VGroup(T("pooled, every unit counts once", 26, RED), M("4.33", 48, RED)).arrange(RIGHT, buff=0.4)
        pooled.move_to([-0.6, -2.75, 0])
        self.at("Pooled")
        self.play(FadeIn(pooled, shift=UP * 0.1), run_time=0.6)
        self.at("twice the units")
        hiA = SurroundingRectangle(VGroup(*rates[:4]), color=ORANGE, buff=0.18, corner_radius=0.12, stroke_width=4)
        hiB = SurroundingRectangle(VGroup(*rates[4:]), color=PINK, buff=0.18, corner_radius=0.12, stroke_width=4)
        t4 = T("4 units", 24, ORANGE).next_to(hiA, DOWN, buff=0.12)
        t2 = T("2 units", 24, PINK).next_to(hiB, DOWN, buff=0.1)
        self.play(Create(hiA), Create(hiB), run_time=0.6)
        self.play(FadeIn(t4), FadeIn(t2), run_time=0.4)

        # equal weight per mouse
        mA = VGroup(T("mouse A", 28, ORANGE), M("5.5", 44, ORANGE)).arrange(RIGHT, buff=0.25)
        mB = VGroup(T("mouse B", 28, PINK), M("2", 44, PINK)).arrange(RIGHT, buff=0.25)
        mAB = VGroup(mA, mB).arrange(RIGHT, buff=0.9).move_to([-0.6, -2.75, 0])
        self.at("equally")
        self.play(FadeOut(pooled), FadeOut(t4), FadeOut(t2), run_time=0.4)
        self.at("mouse A averages")
        self.play(FadeIn(mA, shift=UP * 0.1), hiA.animate.set_stroke(opacity=1), run_time=0.5)
        self.at("mouse B averages")
        self.play(FadeIn(mB, shift=UP * 0.1), run_time=0.5)
        final = VGroup(T("animal mean", 30, GREEN), M("(5.5 + 2) / 2 = 3.75", 40, GREEN)).arrange(RIGHT, buff=0.4)
        final.move_to([-0.6, -3.4, 0])
        self.at("animal mean")
        self.play(FadeIn(final, shift=UP * 0.1), run_time=0.6)
        self.finish()


# ---------------------------------------------------------------------------------------------
class S05N(SpokenScene):
    """24 dots counted as independent, then merged into the two mice."""

    def construct(self):
        def cluster(n_rows, cx, color):
            d = VGroup()
            for r in range(n_rows):
                for c in range(4):
                    d.add(Dot(radius=0.15, color=color).move_to([cx + (c - 1.5) * 0.5, 0.75 + ((n_rows - 1) / 2 - r) * 0.5, 0]))
            return d
        dA = cluster(4, -3.0, ORANGE)
        dB = cluster(2, 3.0, PINK)
        capA = T("mouse A", 28, ORANGE).move_to([-3.0, 2.35, 0])
        capB = T("mouse B", 28, PINK).move_to([3.0, 2.35, 0])
        n24 = VGroup(M("n = 24", 56, RED), T("unit-trials", 28, RED)).arrange(RIGHT, buff=0.3).move_to([0, -1.55, 0])
        self.at("Count every")
        self.play(FadeIn(capA), FadeIn(capB), LaggedStart(*[FadeIn(d, scale=0.5) for d in [*dA, *dB]], lag_ratio=0.03), run_time=1.5)
        self.play(FadeIn(n24, shift=UP * 0.1), run_time=0.5)
        name = bchip("pseudoreplication", RED, 40).move_to([0, -3.0, 0])
        self.at("has a name")
        self.play(FadeIn(name, shift=UP * 0.1), run_time=0.6)

        # merge into two mice
        bigA = Circle(radius=0.95, stroke_color=ORANGE, stroke_width=5, fill_color=ORANGE, fill_opacity=0.4).move_to([-3.0, 0.75, 0])
        bigB = Circle(radius=0.95, stroke_color=PINK, stroke_width=5, fill_color=PINK, fill_opacity=0.4).move_to([3.0, 0.75, 0])
        n2 = VGroup(M("n = 2", 64, GREEN), T("mice", 32, GREEN)).arrange(RIGHT, buff=0.3).move_to([0, -1.55, 0])
        self.at("claim about mice")
        self.play(FadeOut(name), FadeOut(n24), run_time=0.4)
        self.play(ReplacementTransform(dA, bigA), ReplacementTransform(dB, bigB), run_time=1.0)
        self.play(FadeIn(n2, shift=UP * 0.1), run_time=0.5)
        sub = T("the sample size belongs to the level of the question", 30, GREEN).move_to([0, -3.0, 0])
        self.at("sample size belongs")
        self.play(FadeIn(sub, shift=UP * 0.1), run_time=0.6)
        self.finish()


# ---------------------------------------------------------------------------------------------
class S06Rule(SpokenScene):
    """sites != channels != neurons; a unit is an inference; the hierarchy; which level."""

    def construct(self):
        ne = lambda: M("≠", 44, RED)
        c_sites = bchip("sites", GREY, 40)
        c_ch = bchip("channels", TEAL, 40)
        c_neu = bchip("neurons", BLUE, 40)
        row = VGroup(c_sites, ne(), c_ch, ne(), c_neu).arrange(RIGHT, buff=0.5).move_to([0, 1.2, 0])
        self.at("Each number")
        self.play(FadeIn(c_sites), FadeIn(c_ch), FadeIn(c_neu), run_time=0.7)
        self.at("Sites are not channels")
        self.play(FadeIn(row[1]), shout(c_sites, GREY), shout(c_ch, TEAL), run_time=0.6)
        self.at("channels are not neurons")
        self.play(FadeIn(row[3]), shout(c_neu, BLUE), run_time=0.6)
        unit = bchip("a unit is an inference", YELLOW, 44).move_to([0, -1.1, 0])
        self.at("A unit is")
        self.play(FadeIn(unit, shift=UP * 0.1), run_time=0.6)

        # nested hierarchy
        spec = [("animals", GREEN, 11.4, 6.5, 0.0), ("sessions", PURPLE, 10.2, 5.0, 0.2),
                ("units", YELLOW, 9.0, 3.6, 0.4), ("trials", GREY, 7.8, 2.2, 0.6)]
        boxes, labels = [], []
        for name, col, w, h, lift in spec:
            b = RoundedRectangle(corner_radius=0.2, width=w, height=h, stroke_color=col, stroke_width=4,
                                 fill_color=col, fill_opacity=0.07).move_to([0, -3.3 + h / 2 + lift, 0])
            lb = T(name, 30, col, weight=BOLD).move_to([b.get_left()[0] + 1.05, b.get_top()[1] - 0.4, 0])
            boxes.append(b)
            labels.append(lb)
        dots = VGroup(*[Dot(radius=0.11, color=GREY).move_to([-0.65 + 0.43 * k, boxes[3].get_center()[1] - 0.35, 0]) for k in range(4)])
        self.at("animals")
        self.play(FadeOut(row), FadeOut(unit), FadeIn(boxes[0]), FadeIn(labels[0]), run_time=0.5)
        self.at("sessions")
        self.play(FadeIn(boxes[1]), FadeIn(labels[1]), run_time=0.5)
        self.at("units and trials")
        self.play(FadeIn(boxes[2]), FadeIn(labels[2]), run_time=0.5)
        self.play(FadeIn(boxes[3]), FadeIn(labels[3]), LaggedStart(*[FadeIn(d) for d in dots], lag_ratio=0.1), run_time=0.7)

        # which level is the question about
        def ring_for(lb):
            return SurroundingRectangle(lb, color=GOLD, buff=0.12, corner_radius=0.1, stroke_width=5)

        def q_pos(lb):
            return [lb.get_right()[0] + 0.45 + 1.15, lb.get_center()[1], 0]
        q = T("your question", 28, GOLD, weight=BOLD)
        ring = ring_for(labels[3])
        q.move_to(q_pos(labels[3]))
        self.at("which level")
        self.play(Create(ring), FadeIn(q), run_time=0.4)
        for i in (2, 1):
            self.play(Transform(ring, ring_for(labels[i])), q.animate.move_to(q_pos(labels[i])), run_time=0.45)
        self.play(Transform(ring, ring_for(labels[0])), q.animate.move_to(q_pos(labels[0])),
                  boxes[0].animate.set_stroke(width=8).set_fill(GREEN, 0.16), run_time=0.6)
        self.finish()


class S07End(EndCard):
    LINE = "Say which level your question is about."
