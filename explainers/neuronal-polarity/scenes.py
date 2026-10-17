"""Neuronal polarity: an axon is a state, not a stamp  (Biochemistrypedia explainer)

COLOR MAP (one color per concept, whole video)
  YELLOW = the axon (and the leading neurite that becomes it)
  BLUE   = dendrites and the dendrite protein MAP2
  GREY   = cell body, neurites that have not been chosen, outlines, bar baseline
  GREEN  = PIP3 and positive feedback
  RED    = negative feedback, a blocked step, the cut, loss of ankyrin G
  ORANGE = actin
  TEAL   = microtubules
  PURPLE = ankyrin G and the axon initial segment
"""
import numpy as np
from bp_style import *  # noqa: F401,F403

PURPLE = "#B58CD9"
ORANGE = "#F29E4C"
SOMA_FILL = "#262b36"

C0 = np.array([-4.3, 0.45, 0.0])     # cell body centre, same in every scene that shows the whole cell
SOMA_R = 0.72
BASE_Y = -3.3                      # baseline of the length chart
BAR_X0 = 2.3


def u(deg):
    a = np.radians(deg)
    return np.array([np.cos(a), np.sin(a), 0.0])


class Neuron:
    """Cell body plus neurites whose lengths are ValueTrackers. Lines redraw from the trackers."""

    def __init__(self, specs, center=C0, soma_r=SOMA_R):
        self.c = np.array(center, float)
        self.lines, self.tips, self.tr = [], [], []
        self.dirs = []
        grp = VGroup()
        for deg, L, col, w in specs:
            d = u(deg)
            tr = ValueTracker(L)
            ln = Line(self.c, self.c + d * L, color=col, stroke_width=w)
            ln.add_updater(lambda m, d=d, tr=tr: m.put_start_and_end_on(
                self.c + d * 0.02, self.c + d * max(tr.get_value(), 0.05)))
            tip = Dot(self.c + d * L, radius=0.075 + 0.012 * w, color=col)
            tip.add_updater(lambda m, d=d, tr=tr: m.move_to(self.c + d * max(tr.get_value(), 0.05)))
            self.lines.append(ln); self.tips.append(tip); self.tr.append(tr); self.dirs.append(d)
            grp.add(ln, tip)
        self.soma = Circle(radius=soma_r, stroke_color=GREY, stroke_width=4,
                           fill_color=SOMA_FILL, fill_opacity=1).move_to(self.c)
        self.group = VGroup(grp, self.soma)

    def recolor(self, i, col):
        return [self.lines[i].animate.set_color(col), self.tips[i].animate.set_color(col)]

    def point(self, i, L):
        return self.c + self.dirs[i] * L


DEND = [20, 110, 200, 290]
DLEN = (2.4, 2.1, 2.3, 2.2)


def mature(ax_len=10.3, dend_len=DLEN):
    specs = [(0, ax_len, YELLOW, 11)]
    for deg, L in zip(DEND, dend_len):
        specs.append((deg, L, BLUE, 8))
    return Neuron(specs)


def young(lengths=(2.3, 2.3, 2.3, 2.3, 2.3)):
    specs = [(0, lengths[0], GREY, 10)]
    for deg, L in zip(DEND, lengths[1:]):
        specs.append((deg, L, GREY, 10))
    return Neuron(specs)


class Chart:
    """Bars for neurite length, driven by the same trackers as the neuron."""

    def __init__(self, neuron, cols, s=0.55, order=None, x0=BAR_X0, dx=0.9):
        self.s = s
        self.bars = VGroup()
        self.n = neuron
        order = order or list(range(len(neuron.tr)))
        for k, i in enumerate(order):
            x = x0 + k * dx
            tr = neuron.tr[i]
            bar = Line([x, BASE_Y, 0], [x, BASE_Y + 0.1, 0], color=cols[i], stroke_width=26)
            bar.add_updater(lambda m, x=x, tr=tr: m.put_start_and_end_on(
                [x, BASE_Y, 0], [x, BASE_Y + max(tr.get_value() * s, 0.06), 0]))
            self.bars.add(bar)
        self.base = Line([x0 - 0.45, BASE_Y - 0.12, 0], [x0 + (len(order) - 1) * dx + 0.45, BASE_Y - 0.12, 0],
                         color=GREY, stroke_width=3)
        self.title = T("neurite length", 24, GREY).next_to(self.base, DOWN, buff=0.12)
        self.group = VGroup(self.bars, self.base, self.title)


def cutmark(p, color=RED, h=0.55):
    return DashedLine(p + UP * h, p + DOWN * h, color=color, stroke_width=5, dash_length=0.12)


def hdr(text, color=TEXT, size=30):
    return T(text, size, color, font=TITLE_FONT).to_edge(UP, buff=0.35)


class S00Title(TitleCard):
    LESSON = "Neuronal polarity"
    TITLE = "An axon is a state, not a stamp"


# ---------------------------------------------------------------------------------------------
class S01Cut(SpokenScene):
    """polarized neuron: cut near the body -> a dendrite becomes the axon; rebuild; cut far -> old axon regrows."""

    def construct(self):
        nA = mature()
        lblA = hdr("Cut close to the cell body", RED)
        axl = T("axon", 26, YELLOW).move_to(nA.point(0, 3.2) + UP * 0.6)
        dl = T("dendrites", 26, BLUE).move_to(C0 + LEFT * 0.1 + DOWN * 2.75)
        self.play(FadeIn(nA.group), FadeIn(axl), FadeIn(dl), run_time=0.5)
        self.at("close to the cell body")
        cut = cutmark(nA.point(0, 1.5))
        self.play(Create(cut), FadeIn(lblA), run_time=0.5)
        distal = Line(nA.point(0, 1.5), nA.point(0, 10.3), color=YELLOW, stroke_width=11)
        dtip = Dot(nA.point(0, 10.3), radius=0.2, color=YELLOW)
        self.add(distal, dtip)
        nA.tr[0].set_value(1.5)
        self.play(FadeOut(distal), FadeOut(dtip), FadeOut(axl), run_time=0.7)
        self.at("can grow out")
        self.play(nA.tr[1].animate.set_value(6.3), nA.recolor(1, YELLOW)[0], nA.recolor(1, YELLOW)[1], *nA.recolor(0, BLUE),
                  FadeOut(cut), run_time=2.2)
        new = T("new axon", 26, YELLOW).move_to(nA.point(1, 6.3) + RIGHT * 1.15)
        self.play(FadeIn(new), run_time=0.4)
        # ---- case B: rebuild and reset in one animation ----
        nB = mature()
        lblB = hdr("Cut farther away", RED)
        self.at("farther away")
        self.play(FadeOut(nA.group), FadeOut(new), FadeOut(dl), FadeOut(lblA), FadeIn(nB.group), FadeIn(lblB), run_time=0.6)
        cutB = cutmark(nB.point(0, 6.0))
        distalB = Line(nB.point(0, 6.0), nB.point(0, 10.3), color=YELLOW, stroke_width=11)
        dtipB = Dot(nB.point(0, 10.3), radius=0.2, color=YELLOW)
        self.play(Create(cutB), run_time=0.4)
        self.add(distalB, dtipB)
        nB.tr[0].set_value(6.0)
        self.play(FadeOut(distalB), FadeOut(dtipB), run_time=0.5)
        self.at("the old axon simply regrows")
        self.play(nB.tr[0].animate.set_value(10.3), FadeOut(cutB), run_time=1.8)
        q = T("What decides which process is the axon?", 34, TEXT, font=TITLE_FONT).move_to([0.6, -2.5, 0])
        self.at("What decides")
        self.play(FadeOut(lblB), FadeIn(q, shift=UP * 0.15), run_time=0.7)
        self.finish()


class S02Race(SpokenScene):
    """five equal neurites; bar chart; one pulls ahead and becomes the axon."""

    def construct(self):
        n = young()
        cols = [GREY] * 5
        ch = Chart(n, cols)
        head = hdr("Cultured rat hippocampal neuron", GREY, 28)
        self.at("Start in a dish")
        self.play(FadeIn(head), FadeIn(n.group), run_time=0.8)
        self.at("grows several short neurites")
        self.play(FadeIn(ch.group), run_time=0.8)
        alike = T("all alike", 30, GREY).move_to([3.8, 0.9, 0])
        self.at("all look alike")
        self.play(FadeIn(alike), run_time=0.4)
        self.at("one neurite starts to grow")
        self.play(FadeOut(alike), n.tr[0].animate.set_value(5.0), run_time=3.4, rate_func=rate_functions.ease_in_sine)
        self.at("becomes the axon")
        self.play(*n.recolor(0, YELLOW), ch.bars[0].animate.set_color(YELLOW), run_time=0.6)
        lab = T("axon", 28, YELLOW).move_to(n.point(0, 5.0) + UP * 0.6 + LEFT * 0.2)
        self.play(FadeIn(lab), run_time=0.3)
        # the ten-micrometre gap
        self.at("tends to win once")
        y2 = BASE_Y + 2.3 * ch.s
        y1 = BASE_Y + 5.0 * ch.s
        x = BAR_X0 + 0.55
        ref = DashedLine([BAR_X0 - 0.2, y2, 0], [BAR_X0 + 0.65, y2, 0], color=GREY, stroke_width=3)
        gap = DoubleArrow([BAR_X0 + 0.5, y2, 0], [BAR_X0 + 0.5, y1, 0], color=TEXT, stroke_width=4, buff=0,
                          tip_length=0.18)
        gl = T("about 10 µm longer", 28, TEXT).next_to(gap, RIGHT, buff=0.2).shift(UP * 0.35)
        self.play(Create(ref), GrowFromCenter(gap), FadeIn(gl), run_time=0.8)
        race = T("a race", 48, GOLD, font=TITLE_FONT).move_to([4.0, 1.5, 0])
        self.at("behaves like a race")
        self.play(FadeIn(race, scale=0.9), run_time=0.5)
        self.finish()


class S03Feedback(SpokenScene):
    """leader with positive feedback + PIP3; PI3-kinase blocked -> no axon; negative feedback with a question mark."""

    def construct(self):
        n = young((5.0, 2.3, 2.3, 2.3, 2.3))
        self.add(n.group)
        n.lines[0].set_color(YELLOW); n.tips[0].set_color(YELLOW)
        head = hdr("Two kinds of feedback", TEXT, 30)
        self.play(FadeIn(head), run_time=0.5)
        # positive feedback loop on the right
        grows = chip("grows", YELLOW, size=28).move_to([2.3, 2.3, 0])
        faster = chip("grows faster", YELLOW, size=28).move_to([5.0, 2.3, 0])
        top = CurvedArrow(grows.get_top() + UP * 0.05, faster.get_top() + UP * 0.05, angle=-TAU / 4,
                          color=GREEN, stroke_width=5)
        bot = CurvedArrow(faster.get_bottom() + DOWN * 0.05, grows.get_bottom() + DOWN * 0.05, angle=-TAU / 4,
                          color=GREEN, stroke_width=5)
        pos = T("positive feedback", 30, GREEN).move_to([3.65, 0.95, 0])
        self.at("Positive feedback in the leader")
        self.play(FadeIn(grows), FadeIn(faster), Create(top), Create(bot), FadeIn(pos), run_time=1.2)
        # PIP3 at tip
        tipp = n.point(0, 5.0)
        dots = VGroup(*[Dot(tipp + np.array([0.12 + 0.2 * (k % 3) * 0, 0, 0]) + RIGHT * 0.0, radius=0.07, color=GREEN)
                        for k in range(1)])
        dots = VGroup(*[Dot(tipp + np.array(p), radius=0.08, color=GREEN) for p in
                        [(-0.45, 0.28, 0), (-0.2, -0.3, 0), (0.15, 0.32, 0), (0.38, -0.2, 0), (-0.05, 0.0, 0.0),
                         (-0.6, -0.22, 0)]])
        pl = T("PIP3", 28, GREEN).next_to(dots, DOWN, buff=0.45).shift(RIGHT * 0.1)
        self.at("builds up at its tip")
        self.play(LaggedStart(*[FadeIn(d, scale=0.3) for d in dots], lag_ratio=0.15), FadeIn(pl), run_time=1.2)
        # PI3-kinase blocked
        self.at("Blocking")
        k = chip("PI 3-kinase", GREEN, size=28).move_to([3.7, -1.0, 0])
        cross = VGroup(Line(k.get_corner(UL), k.get_corner(DR), color=RED, stroke_width=4),
                       Line(k.get_corner(DL), k.get_corner(UR), color=RED, stroke_width=4))
        self.play(FadeIn(k), run_time=0.4)
        self.play(Create(cross), run_time=0.4)
        self.at("stop any neurite from becoming an axon")
        noax = T("no neurite becomes an axon", 28, RED).move_to([3.7, -2.1, 0])
        self.play(FadeIn(noax), FadeOut(dots), FadeOut(pl), *n.recolor(0, GREY), run_time=0.6)
        # negative feedback: red bars on the other neurites, with a question mark
        self.at("Negative feedback holds the others back")
        self.play(FadeOut(k), FadeOut(cross), FadeOut(noax), *n.recolor(0, YELLOW), run_time=0.4)
        bars = VGroup()
        for i in range(1, 5):
            p = n.point(i, 1.0)
            d = n.dirs[i]
            perp = np.array([-d[1], d[0], 0])
            bars.add(Line(p + perp * 0.32, p - perp * 0.32, color=RED, stroke_width=8))
        neg = T("negative feedback", 30, RED).move_to([3.7, -1.0, 0])
        self.play(LaggedStart(*[Create(b) for b in bars], lag_ratio=0.2), FadeIn(neg), run_time=1.2)
        self.at("less settled")
        qm = T("how?", 36, GOLD, weight=BOLD).move_to([3.7, -2.0, 0])
        self.play(FadeIn(qm, scale=1.3), run_time=0.5)
        self.finish()


def cone(cx, cy, col, n_actin, mt_end, seed, sc=1.32):
    """schematic growth cone: shaft, fan, actin lines (orange), microtubules (teal)."""
    rng = np.random.RandomState(seed)
    W, H = 3.4 * sc, 2.6 * sc
    fan = Ellipse(width=W, height=H, stroke_color=col, stroke_width=5, fill_color=col, fill_opacity=0.08
                  ).move_to([cx, cy, 0])
    x_neck = cx - W / 2 + 0.05
    shaft_x0 = x_neck - 1.35
    shaft = VGroup(Line([shaft_x0, cy + 0.3, 0], [x_neck, cy + 0.42, 0], color=col, stroke_width=5),
                   Line([shaft_x0, cy - 0.3, 0], [x_neck, cy - 0.42, 0], color=col, stroke_width=5))
    actin = VGroup()
    for _ in range(n_actin):
        while True:
            x, y = rng.uniform(-W / 2, W / 2), rng.uniform(-H / 2, H / 2)
            if (x / (W / 2 * 0.93)) ** 2 + (y / (H / 2 * 0.9)) ** 2 < 0.85 and x > -W / 2 + 0.45:
                break
        a = rng.uniform(0, PI)
        c = np.array([cx + x, cy + y, 0]); dv = np.array([np.cos(a), np.sin(a), 0]) * 0.2 * sc
        actin.add(Line(c - dv, c + dv, color=ORANGE, stroke_width=4))
    mts = VGroup()
    for k, yo in enumerate((-0.2, 0.0, 0.2)):
        mts.add(Line([shaft_x0, cy + yo, 0], [mt_end - 0.2 * k, cy + yo, 0], color=TEAL, stroke_width=7))
    return dict(fan=fan, shaft=shaft, actin=actin, mts=mts, x_neck=x_neck, shaft_x0=shaft_x0, cx=cx, cy=cy)


class S04Tip(SpokenScene):
    """two growth cones: dense actin + short microtubules (sibling) vs loose actin + deep microtubules (leader)."""

    def construct(self):
        CY = 0.25
        LX, SX = -2.55, 3.95
        Lc = cone(LX, CY, YELLOW, 18, LX + 0.5, 3)
        Sc = cone(SX, CY, GREY, 60, 0, 5)
        # sibling microtubules stop at the neck
        for k, m in enumerate(Sc["mts"]):
            m.put_start_and_end_on(m.get_start(), [Sc["x_neck"] + 0.2 - 0.15 * k, m.get_start()[1], 0])
        lt = T("leader", 32, YELLOW).move_to([LX, 2.45, 0])
        st = T("sibling", 32, GREY).move_to([SX, 2.45, 0])
        self.at("Look at the growth cone")
        self.play(FadeIn(VGroup(Lc["fan"], Lc["shaft"])), FadeIn(VGroup(Sc["fan"], Sc["shaft"])),
                  FadeIn(lt), FadeIn(st), run_time=1.0)
        a_lab = chip("actin", ORANGE, size=28).move_to([LX - 1.6, -2.85, 0])
        m_lab = chip("microtubules", TEAL, size=28).move_to([LX + 1.5, -2.85, 0])
        self.at("Its actin network is looser")
        self.play(FadeIn(Sc["actin"]), FadeIn(Lc["actin"]), FadeIn(a_lab), run_time=1.2)
        loose = T("loose", 30, ORANGE).move_to([LX, -2.0, 0])
        dense = T("dense", 30, ORANGE).move_to([SX, -2.0, 0])
        self.play(FadeIn(loose), FadeIn(dense), run_time=0.4)
        self.at("push in")
        self.play(FadeIn(Lc["mts"]), FadeIn(Sc["mts"]), FadeIn(m_lab), run_time=1.0)
        self.at("more stable")
        self.play(Indicate(Lc["mts"], color=TEAL, scale_factor=1.0), run_time=0.8)
        # chosen sibling: loosen actin, microtubules push in
        self.at("Loosen the actin in a chosen neurite")
        drop = VGroup(*[m for i, m in enumerate(Sc["actin"]) if i % 3 != 0])
        newmts = VGroup(*[Line(m.get_start(), [SX + 0.5 - 0.2 * k, m.get_start()[1], 0], color=TEAL, stroke_width=7)
                          for k, m in enumerate(Sc["mts"])])
        self.play(FadeOut(drop), Transform(dense, T("loosened", 30, ORANGE).move_to([SX, -2.0, 0])), run_time=1.0)
        self.at("stabilize its microtubules")
        self.play(Transform(Sc["mts"], newmts), run_time=0.9)
        self.at("can become the axon")
        newt = T("chosen", 32, YELLOW).move_to([SX, 2.45, 0])
        self.play(ReplacementTransform(st, newt), Sc["fan"].animate.set_stroke(YELLOW),
                  Sc["shaft"].animate.set_color(YELLOW), run_time=0.8)
        self.finish()


class S05Hold(SpokenScene):
    """mature neuron: AIS on ankyrin G; MAP2 kept out of axon; lower ankyrin G -> segment dissolves, MAP2 enters, axon looks like a dendrite."""

    def construct(self):
        n = mature()
        self.play(FadeIn(n.group), run_time=0.8)
        # MAP2 dots in dendrites and soma
        rng = np.random.RandomState(2)
        dots = VGroup()
        for i in range(1, 5):
            for _ in range(5):
                dots.add(Dot(n.point(i, rng.uniform(0.7, n.tr[i].get_value() - 0.1)) + np.array([0, rng.uniform(-.18, .18), 0]),
                             radius=0.07, color=TEXT))
        for dd in dots:
            dd.set_color(BLUE).set_stroke(TEXT, 1.5)
        # AIS band
        ais = Line(n.point(0, 0.95), n.point(0, 2.95), color=PURPLE, stroke_width=26).set_opacity(0.85)
        ais_lbl = T("axon initial segment", 28, PURPLE).move_to(n.point(0, 3.6) + DOWN * 0.85)
        self.at("scaffold called")
        ank = chip("ankyrin G", PURPLE, size=30).move_to([-0.9, -2.35, 0])
        self.play(FadeIn(ank), run_time=0.5)
        self.at("builds the axon initial segment")
        self.play(Create(ais), FadeIn(ais_lbl), run_time=0.9)
        map2 = chip("MAP2", BLUE, size=28).move_to([-5.6, -2.35, 0])
        self.at("It works as a gate")
        self.play(LaggedStart(*[FadeIn(d, scale=0.3) for d in dots], lag_ratio=0.05), FadeIn(map2), run_time=1.2)
        self.play(Indicate(ais, color=PURPLE, scale_factor=1.15), run_time=0.8)
        # lower ankyrin G
        self.at("in a mature neuron")
        cross = VGroup(Line(ank.get_corner(UL), ank.get_corner(DR), color=RED, stroke_width=4),
                       Line(ank.get_corner(DL), ank.get_corner(UR), color=RED, stroke_width=4))
        self.play(Create(cross), run_time=0.4)
        self.at("falls apart")
        self.play(ais.animate.set_color(RED).set_opacity(0.5), run_time=0.4)
        self.play(FadeOut(ais), FadeOut(ais_lbl), run_time=0.5)
        # MAP2 enters axon
        self.at("spreads into the axon")
        newd = VGroup(*[Dot(n.point(0, 0.9 + 0.62 * k) + np.array([0, (-1) ** k * 0.14, 0]), radius=0.07,
                            color=BLUE).set_stroke(TEXT, 1.5) for k in range(14)])
        self.play(LaggedStart(*[FadeIn(d, scale=0.3) for d in newd], lag_ratio=0.1), run_time=2.0)
        self.at("begins to look like a dendrite")
        spines = VGroup()
        for k in range(1, 12):
            p = n.point(0, 0.8 + 0.8 * k)
            s = 1 if k % 2 else -1
            spines.add(Line(p, p + UP * 0.32 * s, color=BLUE, stroke_width=4))
        self.play(*n.recolor(0, BLUE), FadeIn(spines), run_time=1.2)
        lab = T("looks like a dendrite", 30, BLUE).move_to([3.2, -2.35, 0])
        self.play(FadeIn(lab), run_time=0.4)
        self.finish()


class S06Rule(SpokenScene):
    """short stump: level bars, a dendrite wins. long stump: stump bar already tallest, regrows."""

    def construct(self):
        # case A: short stump (1.0 long), four dendrites alike
        nA = mature()
        cols = [YELLOW, BLUE, BLUE, BLUE, BLUE]
        chA = Chart(nA, cols, s=0.3)
        lblA = hdr("Short stump: under 35 µm", RED)
        self.add(nA.group)
        self.at("Now return to the cut")
        cutp = nA.point(0, 1.2)
        cut = cutmark(cutp)
        self.play(Create(cut), FadeIn(lblA), run_time=0.6)
        distal = Line(cutp, nA.point(0, 10.3), color=YELLOW, stroke_width=11)
        dtip = Dot(nA.point(0, 10.3), radius=0.2, color=YELLOW)
        self.add(distal, dtip)
        nA.tr[0].set_value(1.2)
        self.at("stump shorter than")
        self.play(FadeOut(distal), FadeOut(dtip), FadeIn(chA.group), run_time=0.8)
        nobody = T("no process clearly ahead", 30, GREY).move_to([3.9, 1.0, 0])
        self.at("no process is clearly ahead")
        self.play(FadeIn(nobody), run_time=0.5)
        self.at("like the first race again")
        self.play(FadeOut(cut), FadeOut(nobody), run_time=0.4)
        self.at("a dendrite can win it")
        self.play(nA.tr[1].animate.set_value(6.3), *nA.recolor(1, YELLOW), *nA.recolor(0, BLUE), chA.bars[0].animate.set_color(BLUE), chA.bars[1].animate.set_color(YELLOW),
                  run_time=1.9)
        # case B: reset everything in one animation
        nB = mature()
        chB = Chart(nB, cols, s=0.3)
        lblB = hdr("Long stump: over 35 µm", RED)
        self.at("Leave a longer stump")
        self.play(FadeOut(nA.group), FadeOut(chA.group), FadeOut(lblA), FadeIn(nB.group), FadeIn(lblB),
                  FadeIn(chB.group), run_time=0.6)
        cutp = nB.point(0, 5.2)
        cutB = cutmark(cutp)
        distalB = Line(cutp, nB.point(0, 10.3), color=YELLOW, stroke_width=11)
        dtipB = Dot(nB.point(0, 10.3), radius=0.2, color=YELLOW)
        self.play(Create(cutB), run_time=0.3)
        self.add(distalB, dtipB)
        nB.tr[0].set_value(5.2)
        self.play(FadeOut(distalB), FadeOut(dtipB), run_time=0.4)
        self.at("the old axon regrows")
        self.play(nB.tr[0].animate.set_value(10.3), FadeOut(cutB), run_time=1.6)
        self.at("Keep this rule")
        rule = T("An axon is a state the cell holds", 38, GOLD, font=TITLE_FONT).move_to([1.9, -1.2, 0])
        self.play(FadeOut(lblB), FadeOut(chB.group), FadeIn(rule, shift=UP * 0.15), run_time=0.8)
        self.at("that state can pass to another process")
        sub = T("lose enough of the axon, and the state can pass on", 28, TEXT).next_to(rule, DOWN, buff=0.35)
        self.play(FadeIn(sub), run_time=0.6)
        self.finish()


class S07End(EndCard):
    LINE = "An axon is a state the cell holds, not a stamp."
