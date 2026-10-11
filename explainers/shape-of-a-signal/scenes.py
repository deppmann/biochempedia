"""The shape of a signal: a late part reads signal length  (Biochemistrypedia explainer)

Timed to the SPOKEN words: every self.at("...") cue waits for that phrase in audio/words.json.

COLOR MAP (one color per concept, whole video)
  YELLOW = the growth factor, the signal that arrives from outside (EGF, NGF)
  TEAL   = ERK, its activity trace, and the kinase that ERK activates
  ORANGE = c-Fos, the delayed product (the pill, the pile, the slow route)
  GOLD   = a phosphate (the round "P" badge)
  GREEN  = kept: the ring round protected c-Fos, the checks
  RED    = lost: destroyed c-Fos, the crossed-out stopwatch
  PURPLE = what the cell does (divide, nerve-like, differentiate, later genes)
  GREY   = time axes, gene chips, labels, things not yet known (dashed)
  TEXT   = how long a signal lasts (the white bars), titles, the dashed "now" line

No molecular structures: kinases and genes are labelled chips; c-Fos is a pill with a short tail
that carries two docking sites; a phosphate is a "P" badge; ERK activity is a curve computed
from a smooth step. Time runs left to right in every plot.
"""
import numpy as np
from bp_style import *  # noqa: F401,F403

PURPLE = "#B58CD9"
ORANGE = "#F29E4C"


# ---------------------------------------------------------------------------------------------
# helpers
# ---------------------------------------------------------------------------------------------
def p3(c):
    c = np.array(c, float)
    return np.array([c[0], c[1], 0.0])


def bchip(text, color=BLUE, size=26, pad=0.2, **kw):
    """chip with an opaque backing so lines drawn behind it do not show through."""
    c = chip(text, color, size=size, pad=pad, **kw)
    back = RoundedRectangle(corner_radius=0.14, width=c[0].width, height=c[0].height, stroke_width=0,
                            fill_color=BG, fill_opacity=1).move_to(c[0])
    g = VGroup(back, *c)
    g.set_z_index(3)
    return g


def arr(a, b, color=GREY, w=6, tip=0.24):
    return Arrow(a, b, buff=0.06, color=color, stroke_width=w, tip_length=tip,
                 max_tip_length_to_length_ratio=0.45, max_stroke_width_to_length_ratio=12)


def pbadge(r=0.22):
    c = Circle(radius=r, stroke_color=GOLD, stroke_width=2, fill_color=GOLD, fill_opacity=1)
    g = VGroup(c, T("P", 22, BG, weight=BOLD).move_to(c))
    g.set_z_index(4)
    return g


def qbox(center, w=0.85, h=0.85, color=GREY, size=32):
    """the unknown: a dashed box with a question mark, opaque so nothing shows through."""
    box = RoundedRectangle(corner_radius=0.14, width=w, height=h)
    back = box.copy().set_stroke(width=0).set_fill(BG, 1)
    dash = DashedVMobject(box, num_dashes=max(16, int((w + h) * 9))).set_color(color)
    q = T("?", size, color, weight=BOLD)
    g = VGroup(back, dash, q).move_to(center)
    g.set_z_index(3)
    return g


def _step(x0, x1, y_base, on, off, h, w, n):
    sg = lambda z: 1.0 / (1.0 + np.exp(-z))
    xs = np.linspace(x0, x1, n)
    ys = y_base + h * (sg((xs - on) / w) - sg((xs - off) / w))
    return xs, ys


def trace(x0, x1, y_base, on, off, h=1.0, w=0.09, color=TEAL, n=220):
    """ERK activity against time: a smooth step up at x=on and a smooth step down at x=off."""
    xs, ys = _step(x0, x1, y_base, on, off, h, w, n)
    m = VMobject(stroke_color=color, stroke_width=7)
    m.set_points_smoothly([np.array([x, y, 0.0]) for x, y in zip(xs, ys)])
    return m


def area(x0, x1, y_base, on, off, h=1.0, w=0.09, color=TEAL, n=220):
    """the soft fill under a trace."""
    xs, ys = _step(x0, x1, y_base, on, off, h, w, n)
    pts = [np.array([x, y, 0.0]) for x, y in zip(xs, ys)] + [np.array([x1, y_base, 0.0]), np.array([x0, y_base, 0.0])]
    return Polygon(*pts, stroke_width=0, fill_color=color, fill_opacity=0.18)


def baseline(x0, x1, y):
    return Line([x0, y, 0], [x1, y, 0], color=GREY, stroke_width=2.5, stroke_opacity=0.6)


def span_bar(xa, xb, y, color=TEXT):
    """a bar that marks how long a signal lasted."""
    return RoundedRectangle(corner_radius=0.05, width=xb - xa, height=0.1, stroke_width=0, fill_color=color,
                            fill_opacity=0.95).move_to([(xa + xb) / 2, y, 0])


def check(center, s=0.3, color=GREEN):
    c = p3(center)
    return VGroup(Line(c + [-s, 0.0, 0], c + [-s * 0.3, -s * 0.8, 0], color=color, stroke_width=9),
                  Line(c + [-s * 0.3, -s * 0.8, 0], c + [s, s * 0.9, 0], color=color, stroke_width=9))


def cross(center, s=0.3, color=RED, w=8):
    c = p3(center)
    return VGroup(Line(c + [-s, s, 0], c + [s, -s, 0], color=color, stroke_width=w),
                  Line(c + [-s, -s, 0], c + [s, s, 0], color=color, stroke_width=w))


class Cfos(VGroup):
    """c-Fos: a pill, a short tail with two docking sites, and its name inside.

    parts: back, body, tail, dots, label.   sites: where the two phosphates land.   end: right end of the pill.
    """

    def __init__(self, center, k=1.0, label=True, size=24, color=ORANGE, tail=True):
        super().__init__()
        c = p3(center)
        w, h = 1.6 * k, 0.7 * k
        self.k, self.color = k, color
        self.back = RoundedRectangle(corner_radius=h / 2, width=w, height=h, stroke_width=0, fill_color=BG,
                                     fill_opacity=1).move_to(c)
        self.body = RoundedRectangle(corner_radius=h / 2, width=w, height=h, stroke_color=color, stroke_width=4,
                                     fill_color=color, fill_opacity=0.3).move_to(c)
        self.end = c + np.array([w / 2, 0, 0])
        self.sites = [c + np.array([w / 2 + 0.4 * k, 0, 0]), c + np.array([w / 2 + 0.9 * k, 0, 0])]
        self.tail = Line(self.end, self.sites[1], color=color, stroke_width=5)
        self.dots = VGroup(*[Dot(s, radius=0.07, color=color) for s in self.sites])
        self.label = T("c-Fos", size, color).move_to(c) if label else VGroup()
        parts = [self.back, self.body, self.label]
        if tail:
            parts = [self.back, self.tail, self.dots, self.body, self.label]
        self.add(*parts)
        self.set_z_index(2)

    def recolor(self, color):
        return [self.body.animate.set_stroke(color).set_fill(color, 0.3), self.tail.animate.set_color(color),
                self.dots.animate.set_color(color), self.label.animate.set_color(color)]


def ghost_cfos(center, k=1.0, color=ORANGE):
    """where c-Fos will appear: a dashed outline, no name."""
    c = p3(center)
    w, h = 1.6 * k, 0.7 * k
    box = RoundedRectangle(corner_radius=h / 2, width=w, height=h).move_to(c)
    g = DashedVMobject(box, num_dashes=30).set_color(color)
    g.set_z_index(2)
    return g


def ring(blob, color=GREEN, pad=0.16):
    """a ring round c-Fos and its tail: protected."""
    x0 = blob.body.get_left()[0] - pad
    x1 = blob.sites[1][0] + 0.22 * blob.k + pad
    h = blob.body.height + 2 * pad
    r = RoundedRectangle(corner_radius=h / 2, width=x1 - x0, height=h, stroke_color=color, stroke_width=5)
    r.set_z_index(2)
    return r.move_to([(x0 + x1) / 2, blob.body.get_center()[1], 0])


def stopwatch(center, r=1.0):
    c = p3(center)
    face = Circle(radius=r, stroke_color=GREY, stroke_width=7).move_to(c)
    btn = RoundedRectangle(corner_radius=0.06, width=0.36 * r, height=0.24 * r, stroke_color=GREY, stroke_width=6,
                           fill_color=GREY, fill_opacity=0.5).move_to(c + [0, r + 0.22 * r, 0])
    ticks = VGroup(*[Line(c + (r - 0.2) * v, c + (r - 0.04) * v, color=GREY, stroke_width=6) for v in (UP, RIGHT, DOWN, LEFT)])
    hand = Line(c, c + [0.42 * r, 0.5 * r, 0], color=TEXT, stroke_width=7)
    pin = Dot(c, radius=0.07, color=TEXT)
    return VGroup(face, btn, ticks, hand, pin)


def lengthen(*mobs):
    """pulse the white length bars and their labels (no recolouring)."""
    return [m.animate(rate_func=there_and_back).scale(1.18) for m in mobs]


# ---------------------------------------------------------------------------------------------
# the question picture (scene 1, and the start of scene 2)
# ---------------------------------------------------------------------------------------------
Q_ERK = np.array([-0.4, 0.0, 0.0])
Q_EGF = np.array([-5.0, 1.95, 0.0])
Q_NGF = np.array([-5.0, -1.95, 0.0])
Q_DIV = np.array([4.75, 1.95, 0.0])
Q_NER = np.array([4.75, -1.95, 0.0])


def question_parts():
    """every part of the finished question picture, in its final place."""
    p = {}
    p["head"] = T("PC12 cells, a rat cell line", 28, GREY).move_to([0, 3.2, 0])
    p["erk"] = bchip("ERK", TEAL, 44).move_to(Q_ERK)
    p["egf"] = bchip("EGF", YELLOW, 36).move_to(Q_EGF)
    p["egf_cap"] = T("epidermal\ngrowth factor", 24, GREY, line_spacing=0.8).next_to(p["egf"], DOWN, buff=0.18)
    p["ngf"] = bchip("NGF", YELLOW, 36).move_to(Q_NGF)
    p["ngf_cap"] = T("nerve\ngrowth factor", 24, GREY, line_spacing=0.8).next_to(p["ngf"], UP, buff=0.18)
    p["div"] = bchip("divide", PURPLE, 34).move_to(Q_DIV)
    p["ner"] = bchip("nerve-like", PURPLE, 34).move_to(Q_NER)
    p["a1"] = arr([-3.9, 1.6, 0], [-1.35, 0.4, 0], YELLOW)
    p["a2"] = arr([-3.9, -1.6, 0], [-1.35, -0.4, 0], YELLOW)
    p["o1"] = arr([0.65, 0.4, 0], [3.3, 1.7, 0], TEAL)
    p["o2"] = arr([0.65, -0.4, 0], [3.3, -1.7, 0], TEAL)
    p["q1"] = qbox([-2.62, 1.0, 0])
    p["q2"] = qbox([-2.62, -1.0, 0])
    return p


# ---------------------------------------------------------------------------------------------
class S00Title(TitleCard):
    LESSON = "The shape of a signal"
    TITLE = "A late part reads signal length"


# ---------------------------------------------------------------------------------------------
class S01Question(SpokenScene):
    """one kinase, two orders: the puzzle is drawn, not stated."""

    def construct(self):
        p = question_parts()
        kin = bchip("kinase", TEAL, 44).move_to(Q_ERK)
        self.at("one kinase")
        self.play(FadeIn(kin, scale=0.85), run_time=0.5)
        ph1 = qbox(Q_DIV, w=2.3, h=1.0)
        ph2 = qbox(Q_NER, w=2.3, h=1.0)
        self.at("two different orders")
        self.play(GrowArrow(p["o1"]), GrowArrow(p["o2"]), FadeIn(ph1), FadeIn(ph2), run_time=0.8)
        self.at("rat cell line")
        self.play(FadeIn(p["head"], shift=DOWN * 0.1), run_time=0.5)
        self.at("epidermal")
        self.play(FadeIn(p["egf"], shift=RIGHT * 0.2), FadeIn(p["egf_cap"]), run_time=0.6)
        self.at("says divide")
        self.play(FadeOut(ph1), FadeIn(p["div"]), Indicate(p["egf"][1:], color=YELLOW, scale_factor=1.1), run_time=0.7)
        self.at("Nerve growth factor")
        self.play(FadeIn(p["ngf"], shift=RIGHT * 0.2), FadeIn(p["ngf_cap"]), run_time=0.6)
        self.at("and grow")
        self.play(FadeOut(ph2), FadeIn(p["ner"]), Indicate(p["ngf"][1:], color=YELLOW, scale_factor=1.1), run_time=0.7)
        self.at("Both switch on")
        self.play(GrowArrow(p["a1"]), GrowArrow(p["a2"]), run_time=0.7)
        self.at("same kinase")
        self.play(FadeOut(kin), FadeIn(p["erk"]), run_time=0.5)
        self.play(Indicate(p["erk"][1:], color=TEAL, scale_factor=1.15), run_time=0.6)
        self.at("molecule is the same")
        self.play(Indicate(p["erk"][1:], color=TEAL, scale_factor=1.12), run_time=0.7)
        self.at("something else")
        self.play(FadeIn(p["q1"], scale=0.6), FadeIn(p["q2"], scale=0.6), run_time=0.6)
        self.play(Wiggle(p["q1"][2], scale_value=1.2), Wiggle(p["q2"][2], scale_value=1.2), run_time=0.8)
        self.finish()


# ---------------------------------------------------------------------------------------------
# scene 2: the plot. one row per signal, time to the right
# ---------------------------------------------------------------------------------------------
PX0, PX1 = -4.0, 3.0
ROWS = [2.3, 0.3, -1.8]
ROW_H = 1.25
AXIS_Y = -3.4
ON_X = -3.4
OFFS = [-2.0, 2.2, 0.2]
OUT_X = 4.75


def row_base(i):
    return ROWS[i] - 0.7


class S02Length(SpokenScene):
    """the same kinase, switched on for different lengths: brief, long, longer than EGF alone."""

    def construct(self):
        p = question_parts()
        self.add(p["head"], p["erk"], p["egf"], p["egf_cap"], p["ngf"], p["ngf_cap"], p["div"], p["ner"],
                 p["a1"], p["a2"], p["o1"], p["o2"], p["q1"], p["q2"])
        self.wait(0.1)

        # --- open the picture out into three rows of ERK activity against time ---------------
        bases = [baseline(PX0, PX1, row_base(i)) for i in range(3)]
        axis = Arrow([PX0, AXIS_Y, 0], [PX1 + 0.3, AXIS_Y, 0], buff=0, color=GREY, stroke_width=4, tip_length=0.2)
        time_lbl = T("time", 26, GREY).move_to([PX1 + 1.0, AXIS_Y, 0])
        erk_lbl = T("ERK activity", 28, TEAL).move_to([-0.5, 3.25, 0])
        egf3 = bchip("EGF", YELLOW, 32).move_to([-5.3, ROWS[2] + 0.3, 0])
        cap3 = T("with extra\nreceptors", 24, GREY, line_spacing=0.8).next_to(egf3, DOWN, buff=0.12)
        dif = bchip("differentiate", PURPLE, 24).move_to([OUT_X, ROWS[2], 0])
        # the chips from scene 1 slide to their rows
        self.play(FadeOut(VGroup(p["head"], p["erk"], p["a1"], p["a2"], p["o1"], p["o2"], p["q1"], p["q2"],
                                 p["egf_cap"], p["ngf_cap"])), run_time=0.35)
        self.play(p["egf"].animate.scale(32 / 36).move_to([-5.3, ROWS[0], 0]),
                  p["ngf"].animate.scale(32 / 36).move_to([-5.3, ROWS[1], 0]),
                  p["div"].animate.move_to([OUT_X, ROWS[0], 0]).scale(24 / 34),
                  p["ner"].animate.move_to([OUT_X, ROWS[1], 0]).scale(24 / 34),
                  *[FadeIn(b) for b in bases], FadeIn(axis), FadeIn(time_lbl), FadeIn(erk_lbl), run_time=0.7)

        tr = []
        for i in range(3):
            args = (PX0 + 0.1, PX1 - 0.1, row_base(i), ON_X, OFFS[i])
            tr.append((trace(*args, h=ROW_H), area(*args, h=ROW_H)))
        bars = [span_bar(ON_X, OFFS[i], row_base(i) - 0.14) for i in range(3)]
        lens = [T("brief", 26, TEXT).move_to([(ON_X + OFFS[0]) / 2, row_base(0) - 0.52, 0]),
                T("long", 26, TEXT).move_to([(ON_X + OFFS[1]) / 2, row_base(1) - 0.52, 0]),
                T("longer than EGF alone", 24, TEXT).move_to([(ON_X + OFFS[2]) / 2, row_base(2) - 0.52, 0])]

        # --- row 1: EGF, brief ---------------------------------------------------------------
        self.at("briefly")
        self.play(Create(tr[0][0], rate_func=linear), run_time=0.9)
        self.play(FadeIn(tr[0][1]), GrowFromEdge(bars[0], LEFT), FadeIn(lens[0]), run_time=0.4)
        self.at("divides")
        self.play(Indicate(p["div"][1:], color=PURPLE, scale_factor=1.12), run_time=0.7)

        # --- row 2: NGF, long ----------------------------------------------------------------
        self.at("keeps")
        self.play(Create(tr[1][0], rate_func=linear), run_time=1.8)
        self.play(FadeIn(tr[1][1]), GrowFromEdge(bars[1], LEFT), FadeIn(lens[1]), run_time=0.5)
        self.at("stops dividing")
        self.play(Indicate(p["ner"][1:], color=PURPLE, scale_factor=1.12), run_time=0.7)

        # --- row 3: EGF, in cells with extra receptors ------------------------------------------
        self.at("Engineered cells")
        self.play(FadeIn(egf3, shift=RIGHT * 0.2), FadeIn(cap3), run_time=0.6)
        self.at("extra")
        self.play(Indicate(cap3, color=TEXT, scale_factor=1.12), run_time=0.7)
        self.at("Given")
        self.play(Indicate(egf3[1:], color=YELLOW, scale_factor=1.12), run_time=0.7)
        self.at("keep")
        self.play(Create(tr[2][0], rate_func=linear), run_time=1.8)
        self.play(FadeIn(tr[2][1]), GrowFromEdge(bars[2], LEFT), FadeIn(lens[2]), run_time=0.5)
        self.at("differentiate")
        self.play(FadeIn(dif, shift=LEFT * 0.2), run_time=0.6)

        # --- the length is the message --------------------------------------------------------
        self.at("length of the signal")
        self.play(*lengthen(*bars, *lens), run_time=1.2)
        self.at("what counts")
        self.play(*[tr_[0].animate.set_stroke(width=11) for tr_ in tr], run_time=0.5)
        self.play(*[tr_[0].animate.set_stroke(width=7) for tr_ in tr], run_time=0.5)
        self.finish()


# ---------------------------------------------------------------------------------------------
# scenes 3 and 4: one stage. ERK on top, c-Fos below, time to the right
# ---------------------------------------------------------------------------------------------
XT0 = -3.3          # ERK switches on
XT1 = 0.9           # c-Fos appears
E_BASE, E_TOP = 1.0, 2.5
C_Y = -1.15
AX_Y = -2.95
DLY_Y = -2.45
LX = -5.4           # the row-label column
K3 = 1.3            # c-Fos scale on this stage
GENE_AT = np.array([-1.75, -0.1, 0])


def stage_parts():
    """the stage as scene 3 leaves it, rebuilt for scene 4. Returns a dict of mobjects."""
    p = {}
    p["erk"] = bchip("ERK", TEAL, 30).move_to([LX, 1.75, 0])
    p["cf"] = bchip("c-Fos", ORANGE, 28).move_to([LX, C_Y, 0])
    p["base"] = baseline(-4.0, 5.9, E_BASE)
    p["axis"] = Arrow([-4.0, AX_Y, 0], [5.4, AX_Y, 0], buff=0, color=GREY, stroke_width=4, tip_length=0.2)
    p["time"] = T("time", 26, GREY).move_to([5.85, AX_Y, 0])
    p["tr"] = trace(-4.0, -0.2, E_BASE, XT0, 99.0, h=E_TOP - E_BASE)
    p["dash"] = DashedLine([-0.2, E_TOP, 0], [3.3, E_TOP, 0], color=TEAL, stroke_width=6, dash_length=0.18)
    p["q"] = qbox([3.8, E_TOP, 0], color=TEAL)
    p["gene"] = bchip("c-fos gene", GREY, 28).move_to(GENE_AT)
    p["diag"] = arr([XT0 + 0.05, E_BASE - 0.1, 0], [XT1 - 1.1, C_Y + 0.05, 0], GREY)
    p["diag"].set_z_index(1)
    p["dly"] = DoubleArrow([XT0, DLY_Y, 0], [XT1, DLY_Y, 0], buff=0, color=GREY, stroke_width=4, tip_length=0.18)
    p["dly_t"] = T("delay", 26, GREY).move_to([(XT0 + XT1) / 2, -2.05, 0])
    p["g0"] = DashedLine([XT0, DLY_Y, 0], [XT0, AX_Y, 0], color=GREY, stroke_width=3, dash_length=0.1)
    p["g1"] = DashedLine([XT1, DLY_Y, 0], [XT1, AX_Y, 0], color=GREY, stroke_width=3, dash_length=0.1)
    p["vline"] = DashedLine([XT1, 2.8, 0], [XT1, AX_Y, 0], color=TEXT, stroke_width=3, dash_length=0.12)
    p["still"] = T("still on?", 28, TEXT).move_to([XT1 + 1.25, 3.1, 0])
    p["ghost"] = ghost_cfos([XT1, C_Y], k=K3)
    p["tag"] = T("in fibroblasts", 28, GREY).move_to([-3.6, 3.1, 0])
    return p


class S03Delay(SpokenScene):
    """no stopwatch: the cell compares the signal with a delayed product of itself."""

    def construct(self):
        p = stage_parts()
        sw = stopwatch([0, 0.3, 0], 1.3)
        self.play(FadeIn(sw, scale=0.9), run_time=0.5)
        self.at("no stopwatch")
        x = cross([0, 0.3, 0], 1.5, RED, 12)
        self.play(Create(x[0]), Create(x[1]), run_time=0.5)

        # --- the signal -----------------------------------------------------------------------
        self.at("compare the signal")
        self.play(FadeOut(VGroup(sw, x)), run_time=0.25)
        self.play(FadeIn(p["erk"]), FadeIn(p["base"]), FadeIn(p["axis"]), FadeIn(p["time"]), run_time=0.3)
        self.play(Create(p["tr"], rate_func=linear), Create(p["dash"]), FadeIn(p["q"]), run_time=0.8)

        # --- the delayed product --------------------------------------------------------------
        self.at("delayed product")
        self.play(FadeIn(p["cf"]), FadeIn(p["ghost"]), GrowFromCenter(p["dly"]), FadeIn(p["g0"]), FadeIn(p["g1"]),
                  FadeIn(p["dly_t"]), run_time=0.8)

        self.at("same signal")
        self.play(Indicate(VGroup(p["dly"], p["dly_t"]), color=TEXT, scale_factor=1.1), run_time=0.8)

        # --- ERK switches on the gene, the protein is slow to make -------------------------------
        self.at("fibroblasts")
        self.play(FadeIn(p["tag"], shift=DOWN * 0.1), run_time=0.6)
        self.at("switches on")
        self.play(GrowArrow(p["diag"]), FadeIn(p["gene"], scale=0.8), run_time=0.7)
        self.at("called")
        self.play(Indicate(p["gene"][1:], color=TEXT, scale_factor=1.1), run_time=0.7)
        blob = Cfos([XT1, C_Y], k=K3, size=30)
        dot = Dot(p["diag"].get_start(), radius=0.15, color=ORANGE)
        dot.set_z_index(4)
        self.at("takes time")
        self.add(dot)
        self.play(dot.animate.move_to(p["diag"].get_end()), run_time=1.3, rate_func=linear)
        self.at("make")
        self.remove(dot)
        self.play(FadeOut(p["ghost"]), FadeIn(blob, scale=0.6), run_time=0.4)

        # --- and it is quickly destroyed ----------------------------------------------------------
        self.at("quickly destroyed")
        self.play(*blob.recolor(RED), run_time=0.4)
        self.play(FadeOut(blob, scale=0.2), run_time=0.6)
        ghost2 = ghost_cfos([XT1, C_Y], k=K3)

        # --- the test ------------------------------------------------------------------------------
        self.at("test is simple")
        self.play(Create(p["vline"]), FadeIn(ghost2), run_time=0.9)
        self.at("still on")
        self.play(FadeIn(p["still"], shift=DOWN * 0.1), Indicate(p["q"][2], color=TEXT, scale_factor=1.3), run_time=0.8)
        self.at("new protein")
        self.play(Indicate(ghost2, color=ORANGE, scale_factor=1.12), run_time=0.8)
        self.finish()


class S04Protect(SpokenScene):
    """if ERK is still on when c-Fos appears, phosphates protect it."""

    def construct(self):
        p = stage_parts()
        ghost = ghost_cfos([XT1, C_Y], k=K3)
        self.add(p["erk"], p["cf"], p["base"], p["axis"], p["time"], p["tr"], p["dash"], p["q"], p["gene"],
                 p["diag"], p["dly"], p["dly_t"], p["g0"], p["g1"], p["vline"], p["still"], ghost, p["tag"])

        # --- the clinic: the name is called a while after you sign in -----------------------------
        t_call = T("name called", 26, GREY).move_to([XT1 + 1.45, 0.45, 0])
        t_in = T("sign in", 26, GREY).move_to([-4.45, 0.45, 0])
        self.at("calls your name")
        self.play(FadeIn(t_call), Indicate(p["vline"], color=TEXT, scale_factor=1.0), run_time=0.7)
        self.at("sign in")
        self.play(FadeIn(t_in), run_time=0.5)
        self.at("waiting room")
        self.play(Indicate(p["dash"], color=TEAL, scale_factor=1.0), Indicate(p["tr"], color=TEAL, scale_factor=1.0),
                  run_time=0.8)

        # --- ERK is still active when c-Fos appears -----------------------------------------------
        rest = trace(-0.2, 5.9, E_BASE, XT0, 5.1, h=E_TOP - E_BASE)
        full_area = area(-4.0, 5.9, E_BASE, XT0, 5.1, h=E_TOP - E_BASE)
        on_lbl = T("still on", 28, TEXT).move_to(p["still"])
        self.at("still active")
        self.play(FadeOut(VGroup(t_in, t_call, p["dash"], p["q"])), Create(rest, rate_func=linear),
                  ReplacementTransform(p["still"], on_lbl), run_time=1.0)
        self.play(FadeIn(full_area), run_time=0.3)
        blob = Cfos([XT1, C_Y], k=K3, size=30)
        self.at("appears")
        self.play(FadeOut(ghost), FadeIn(blob, scale=0.7), run_time=0.5)

        # --- phosphates land near one end ---------------------------------------------------------
        sites = blob.sites
        ring_s = [Circle(radius=0.3, stroke_color=GOLD, stroke_width=4).move_to(s) for s in sites]
        self.at("phosphates are added")
        self.play(*[Create(r) for r in ring_s], run_time=0.5)
        self.play(*[FadeOut(r) for r in ring_s], run_time=0.3)
        p1 = pbadge(0.26).move_to([sites[0][0], E_BASE, 0])
        self.at("adds them")
        self.play(FadeIn(p1, scale=0.6), run_time=0.25)
        self.play(p1.animate.move_to(sites[0] + [0, 0.02, 0]), run_time=0.8)
        kin = bchip("kinase", TEAL, 28).move_to([4.35, -0.15, 0])
        a_k = arr([4.35, E_BASE - 0.05, 0], [4.35, 0.25, 0], TEAL)
        self.at("so does a kinase")
        self.play(GrowArrow(a_k), FadeIn(kin, shift=DOWN * 0.1), run_time=0.7)
        p2 = pbadge(0.26).move_to(kin.get_bottom() + [0, -0.32, 0])
        self.play(FadeIn(p2, scale=0.6), run_time=0.25)
        self.play(p2.animate.move_to(sites[1] + [0, 0.02, 0]), run_time=0.8)

        # --- protected -------------------------------------------------------------------------------
        rg = ring(blob)
        prot = T("protected", 28, GREEN).move_to([sites[1][0] + 1.55, C_Y, 0])
        self.at("Those phosphates")
        self.play(Indicate(p1, color=TEXT, scale_factor=1.25), Indicate(p2, color=TEXT, scale_factor=1.25), run_time=0.8)
        self.at("protect")
        self.play(Create(rg), FadeIn(prot), run_time=0.8)
        self.finish()


# ---------------------------------------------------------------------------------------------
# scene 5: two panels, brief and long
# ---------------------------------------------------------------------------------------------
PW = 5.6
LO, RO = -6.1, 0.5          # left edges of the two panels
U0, U1 = 0.4, 1.5           # ERK on, c-Fos appears (panel units)
BRIEF_OFF, LONG_OFF = 1.0, 4.7
E5_BASE, E5_TOP = 1.0, 2.5
C5_Y = -1.1
AX5_Y = -2.8
K5 = 0.95


def blob5(x, y, **kw):
    return Cfos([x, y], k=K5, size=24, **kw)


class S05Compare(SpokenScene):
    """brief: made and lost.  long: builds up, switches on later genes."""

    def panel(self, o):
        """axes for one panel: [baseline, axis, 'time' label]."""
        return [baseline(o, o + PW, E5_BASE),
                Arrow([o, AX5_Y, 0], [o + PW, AX5_Y, 0], buff=0, color=GREY, stroke_width=4, tip_length=0.2),
                T("time", 24, GREY).move_to([o + PW - 0.45, AX5_Y - 0.42, 0])]

    def construct(self):
        h5 = E5_TOP - E5_BASE
        # --- left panel: a brief signal ----------------------------------------------------------
        lt = T("brief signal", 32, TEXT).move_to([LO + PW / 2, 3.3, 0])
        l_axes = self.panel(LO)
        l_erk = T("ERK", 26, TEAL).move_to([LO + 0.5, E5_TOP + 0.38, 0])
        l_tr = trace(LO, LO + PW - 0.1, E5_BASE, LO + U0, LO + BRIEF_OFF, h=h5)
        l_ar = area(LO, LO + PW - 0.1, E5_BASE, LO + U0, LO + BRIEF_OFF, h=h5)
        l_bar = span_bar(LO + U0, LO + BRIEF_OFF, E5_BASE - 0.14)
        l_line = DashedLine([LO + U1, 2.7, 0], [LO + U1, AX5_Y, 0], color=TEXT, stroke_width=3, dash_length=0.12)
        l_blob = blob5(LO + U1, C5_Y)
        self.at("brief signal")
        self.play(FadeIn(lt), *[FadeIn(a) for a in l_axes], FadeIn(l_erk), run_time=0.5)
        self.play(Create(l_tr, rate_func=linear), run_time=0.8)
        self.play(FadeIn(l_ar), GrowFromEdge(l_bar, LEFT), run_time=0.3)
        self.at("already off")
        self.play(*lengthen(l_bar), run_time=0.6)
        self.at("appears")
        self.play(Create(l_line), FadeIn(l_blob, scale=0.7), run_time=0.7)
        self.at("made and lost")
        self.play(*l_blob.recolor(RED), run_time=0.4)
        self.play(FadeOut(l_blob, scale=0.2), run_time=0.6)
        l_x = cross([LO + U1, C5_Y], 0.32, RED, 7)
        self.play(Create(l_x[0]), Create(l_x[1]), run_time=0.4)

        # --- right panel: a long signal ------------------------------------------------------------
        rt = T("long signal", 32, TEXT).move_to([RO + PW / 2, 3.3, 0])
        r_axes = self.panel(RO)
        r_erk = T("ERK", 26, TEAL).move_to([RO + 0.5, E5_TOP + 0.38, 0])
        r_tr = trace(RO, RO + PW - 0.1, E5_BASE, RO + U0, RO + LONG_OFF, h=h5)
        r_ar = area(RO, RO + PW - 0.1, E5_BASE, RO + U0, RO + LONG_OFF, h=h5)
        r_bar = span_bar(RO + U0, RO + LONG_OFF, E5_BASE - 0.14)
        r_line = DashedLine([RO + U1, 2.7, 0], [RO + U1, AX5_Y, 0], color=TEXT, stroke_width=3, dash_length=0.12)
        self.at("long signal")
        self.play(FadeIn(rt), *[FadeIn(a) for a in r_axes], FadeIn(r_erk), run_time=0.4)
        self.play(Create(r_tr, rate_func=linear), run_time=0.8)
        self.play(FadeIn(r_ar), GrowFromEdge(r_bar, LEFT), Create(r_line), run_time=0.3)
        self.at("still on")
        self.play(*lengthen(r_bar), run_time=0.6)

        # the first c-Fos appears, gains a phosphate and stays; then more of it gathers
        ys = [-2.2, -1.45, -0.7, 0.05]
        cells = []
        for y in ys:
            b = blob5(RO + U1, y, tail=False)
            pb = pbadge(0.22).move_to(b.end + [0.04, 0, 0])
            cells.append((b, pb))
        self.at("builds up")
        self.play(FadeIn(cells[0][0], scale=0.7), run_time=0.4)
        self.play(FadeIn(cells[0][1], scale=0.5), run_time=0.3)
        self.play(LaggedStart(*[FadeIn(VGroup(b, pb), shift=UP * 0.2) for b, pb in cells[1:]], lag_ratio=0.35),
                  run_time=1.2)

        # --- it switches on later genes --------------------------------------------------------------
        self.at("transcription factor")
        self.play(*[Indicate(VGroup(b, pb), color=TEXT, scale_factor=1.06) for b, pb in cells], run_time=0.8)
        late = bchip("later genes", PURPLE, 24).move_to([RO + 4.4, -1.075, 0])
        to_late = arr([RO + U1 + 1.2, -1.075, 0], [late.get_left()[0] - 0.02, -1.075, 0], ORANGE)
        self.at("later genes")
        self.play(GrowArrow(to_late), FadeIn(late, shift=LEFT * 0.2), run_time=0.8)

        # --- in fibroblasts, c-Fos lets the cell tell brief from long ----------------------------------
        fib = T("fibroblasts", 28, GREY).move_to([0, 3.3, 0])
        self.at("fibroblasts")
        self.play(FadeIn(fib, shift=DOWN * 0.1), run_time=0.6)
        self.at("tell a brief")
        self.play(*lengthen(l_bar), run_time=0.7)
        self.at("from a long")
        self.play(*lengthen(r_bar), run_time=0.7)
        self.finish()


# ---------------------------------------------------------------------------------------------
# scene 6: two routes, the hedge, and the rule
# ---------------------------------------------------------------------------------------------
S6_ERK = np.array([-5.2, 0.3, 0.0])
S6_CF = np.array([1.9, 0.3, 0.0])
K6 = 1.45


def corner_route(points, color):
    """a right-angled route drawn as one path, with its arrow head as a second piece."""
    path = VMobject(stroke_color=color, stroke_width=7).set_points_as_corners(points)
    d = points[-1] - points[-2]
    ang = np.arctan2(d[1], d[0])
    tip = Triangle(fill_color=color, fill_opacity=1, stroke_width=0).scale(0.17).rotate(ang - PI / 2).move_to(points[-1])
    return path, tip


class S06Rule(SpokenScene):
    """a fast route and a slow route meet at c-Fos; it was shown for c-Fos; not every long signal; the rule."""

    def construct(self):
        erk = bchip("ERK", TEAL, 40).move_to(S6_ERK)
        ghost = ghost_cfos(S6_CF, k=K6)
        target = Cfos(S6_CF, k=K6, size=32)
        sites = target.sites
        gtail = DashedLine(target.end, sites[1], color=ORANGE, stroke_width=4, dash_length=0.12)
        gtail.set_z_index(2)
        fast_pts = [S6_ERK + [0, 0.7, 0], np.array([S6_ERK[0], 2.4, 0]), np.array([sites[0][0], 2.4, 0]),
                    sites[0] + [0, 0.45, 0]]
        slow_pts = [S6_ERK + [0, -0.7, 0], np.array([S6_ERK[0], -2.1, 0]), np.array([S6_CF[0], -2.1, 0]),
                    S6_CF + [0, -0.55, 0]]
        fast, f_tip = corner_route([np.array(q, float) for q in fast_pts], TEAL)
        slow, s_tip = corner_route([np.array(q, float) for q in slow_pts], ORANGE)
        gene = bchip("c-fos gene", GREY, 28).move_to([-1.6, -2.1, 0])
        f_lbl = T("phosphates from ERK", 32, TEAL).move_to([-1.0, 2.9, 0])
        s_lbl = T("the new protein", 32, ORANGE).move_to([-1.6, -2.85, 0])
        pb = pbadge(0.27).move_to(fast_pts[0])
        pb2 = pbadge(0.27).move_to(fast_pts[0])

        self.at("The signal reaches")
        self.play(FadeIn(erk, shift=RIGHT * 0.2), FadeIn(ghost), FadeIn(gtail), run_time=0.7)
        self.at("fast route")
        self.play(Create(fast, rate_func=linear), run_time=0.8)
        self.play(FadeIn(f_tip), run_time=0.1)
        self.at("slow route")
        self.play(FadeIn(gene), run_time=0.25)
        self.play(Create(slow, rate_func=linear), run_time=0.7)
        self.play(FadeIn(s_tip), run_time=0.1)
        self.at("needs both")
        self.play(Indicate(fast, color=TEXT, scale_factor=1.0), Indicate(slow, color=TEXT, scale_factor=1.0),
                  Indicate(ghost, color=ORANGE, scale_factor=1.1), run_time=0.9)

        # --- what c-Fos needs: phosphates from ERK, and the new protein (slow to make) -----------------
        self.at("phosphates")
        self.play(FadeIn(f_lbl, shift=DOWN * 0.1), FadeIn(pb, scale=0.6), FadeIn(pb2, scale=0.6),
                  Indicate(erk[1:], color=TEAL, scale_factor=1.15), run_time=0.7)
        dot = Dot(slow_pts[0], radius=0.17, color=ORANGE)
        dot.set_z_index(1)
        self.at("it needs the new")
        self.add(dot)
        self.play(FadeIn(s_lbl, shift=UP * 0.1), run_time=0.4)
        self.play(MoveAlongPath(dot, slow), run_time=2.3, rate_func=linear)
        self.remove(dot)
        self.at("make")
        self.play(FadeOut(ghost), FadeOut(gtail), FadeIn(target, scale=0.8), run_time=0.3)
        # the phosphates travel only now, to a c-Fos that is already there
        self.play(MoveAlongPath(pb, fast, rate_func=linear),
                  Succession(Wait(0.15), MoveAlongPath(pb2, fast, rate_func=linear, run_time=0.55)), run_time=0.7)
        rg = ring(target)
        self.play(pb.animate.move_to(sites[0] + [0, 0.02, 0]), pb2.animate.move_to(sites[1] + [0, 0.02, 0]),
                  Create(rg), run_time=0.4)

        # --- shown for c-Fos in fibroblasts; later for other early gene products ------------------------
        cf2 = Cfos([-3.3, 0.3], k=1.5, size=32)
        pbs2 = [pbadge(0.28).move_to(s + [0, 0.02, 0]) for s in cf2.sites]
        rg2 = ring(cf2)
        fib = T("in fibroblasts", 32, GREY).move_to([-2.6, -1.0, 0])
        chk = check([-6.0, 0.3, 0], s=0.34)
        self.at("shown for")
        self.play(FadeOut(VGroup(erk, fast, slow, f_tip, s_tip, gene, f_lbl, s_lbl, target, rg, pb, pb2)), run_time=0.3)
        self.play(FadeIn(cf2, scale=0.8), *[FadeIn(b, scale=0.6) for b in pbs2], FadeIn(rg2), run_time=0.5)
        self.at("fibroblasts")
        self.play(FadeIn(fib), Create(chk), run_time=0.6)
        others = [bchip("early gene product", GREY, 30) for _ in range(3)]
        for i, o in enumerate(others):
            o.move_to([3.55, 1.9 - 1.9 * i, 0])
        chks = [check([o.get_left()[0] - 0.5, o.get_center()[1], 0]) for o in others]
        self.at("several other")
        self.play(LaggedStart(*[AnimationGroup(FadeIn(o, shift=LEFT * 0.2), Create(c)) for o, c in zip(others, chks)],
                              lag_ratio=0.4), run_time=1.6)

        # --- not every long signal --------------------------------------------------------------------
        rows_y = [1.55, -0.05, -1.65]
        sigs, qs = [], []
        for y in rows_y:
            sigs.append(trace(-5.4, 1.1, y - 0.5, -4.5, -0.3, h=1.05))
            qs.append(qbox([3.6, y, 0], w=1.2, h=1.2, size=36))
        lbl = T("every long signal", 32, TEXT).move_to([-2.2, 3.05, 0])
        read = T("read this way?", 32, GREY).move_to([3.6, 3.05, 0])
        self.at("Do not assume")
        self.play(FadeOut(VGroup(cf2, *pbs2, rg2, fib, chk, *others, *chks)), run_time=0.25)
        self.play(*[Create(s, rate_func=linear) for s in sigs], run_time=0.5)
        self.at("every long signal")
        self.play(FadeIn(lbl), FadeIn(read), *[FadeIn(q, scale=0.6) for q in qs], run_time=0.6)

        # --- the rule -----------------------------------------------------------------------------------
        self.at("Keep this rule")
        er = bchip("ERK", TEAL, 30).move_to([LX, 1.75, 0])
        er_tr = trace(-4.0, 5.9, E_BASE, XT0, 5.1, h=E_TOP - E_BASE)
        er_base = baseline(-4.0, 5.9, E_BASE)
        er_ar = area(-4.0, 5.9, E_BASE, XT0, 5.1, h=E_TOP - E_BASE)
        late_b = Cfos([XT1, C_Y], k=K3, size=30)
        late_r = ring(late_b)
        late_p = [pbadge(0.26).move_to(s + [0, 0.02, 0]) for s in late_b.sites]
        dly = DoubleArrow([XT0, DLY_Y, 0], [XT1, DLY_Y, 0], buff=0, color=GREY, stroke_width=4, tip_length=0.18)
        dly_t = T("arrives late", 28, ORANGE).move_to([(XT0 + XT1) / 2, -2.0, 0])
        self.play(FadeOut(VGroup(lbl, read, *sigs, *qs)), run_time=0.3)
        self.play(FadeIn(er), FadeIn(er_base), Create(er_tr, rate_func=linear), FadeIn(er_ar), run_time=0.7)
        self.at("arrives late")
        self.play(GrowFromCenter(dly), FadeIn(dly_t), FadeIn(late_b, scale=0.7), run_time=0.8)
        self.at("time a signal")
        self.play(Create(late_r), *[FadeIn(b, scale=0.6) for b in late_p], Indicate(er_tr, color=TEAL, scale_factor=1.0),
                  run_time=0.8)
        self.finish()


class S07End(EndCard):
    LINE = "A part that arrives late can time a signal."
