"""Injury and regeneration, chapter 2: The Stump That Kills Itself  (Biochemistrypedia explainer)

COLOR MAP (one color per concept, shared with the other chapters; taken from scenes.old.py)
  BLUE   = the neuron: cell body, axon, stump
  TEAL   = NMNAT2 (the short-lived supply) and the Wlds fusion protein that stands in for it
  ORANGE = NMN
  GREEN  = NAD+ and ATP (the axon's energy)
  RED    = SARM1 (ring, ARM domains) and the cut / destruction
  TIRC   = a lighter red for SARM1's TIR domains (same family as SARM1)
  YELLOW = calcium
  PURPLE = calpain
  GOLD   = the program (the 'program' column, growth cones in other chapters)
  SAGE   = repair glia (not used in this chapter)
  GREY   = labels, outlines, the starving hypothesis, de-emphasized
"""
import numpy as np
from bp_style import *  # noqa: F401,F403

PURPLE = "#B58CD9"
ORANGE = "#F29E4C"
SAGE = "#9BB99B"
TIRC = "#FF9C94"
DARK = "#2b303b"


# ---------------------------------------------------------------------------------------------
# helpers
# ---------------------------------------------------------------------------------------------
def bchip(text, color=BLUE, size=26, **kw):
    c = chip(text, color, size=size, **kw)
    back = RoundedRectangle(corner_radius=0.14, width=c[0].width, height=c[0].height, stroke_width=0,
                            fill_color=BG, fill_opacity=1).move_to(c[0])
    return VGroup(back, *c)


def arr(a, b, color=GREY, w=5, tip=0.22):
    return Arrow(a, b, buff=0.08, color=color, stroke_width=w, tip_length=tip,
                 max_tip_length_to_length_ratio=0.45, max_stroke_width_to_length_ratio=12)


def tube(x0, x1, y, h=0.4, color=BLUE, op=0.3, sw=3.5):
    return RoundedRectangle(corner_radius=h / 2, width=x1 - x0, height=h, stroke_color=color, stroke_width=sw,
                            fill_color=color, fill_opacity=op).move_to([(x0 + x1) / 2, y, 0])


def beads(x0, x1, y, h=0.4, n=7, color=BLUE, op=0.3):
    pitch = (x1 - x0) / n
    g = VGroup()
    for i in range(n):
        w = pitch * 0.62
        g.add(RoundedRectangle(corner_radius=min(h, w) / 2, width=w, height=h * 0.9, stroke_color=color, stroke_width=3.5,
                               fill_color=color, fill_opacity=op).move_to([x0 + pitch * (i + 0.5), y + (0.05 if i % 2 else -0.05), 0]))
    return g


def neuron(y, xs=-5.4, xe=6.0, xc=-0.8, h=0.4, r=0.65):
    prox = tube(xs, xc, y, h)
    dist = tube(xc, xe, y, h)
    soma = Circle(radius=r, stroke_color=BLUE, stroke_width=4, fill_color=BG, fill_opacity=1).move_to([xs, y, 0])
    soma_f = Circle(radius=r, stroke_width=0, fill_color=BLUE, fill_opacity=0.3).move_to([xs, y, 0])
    nuc = Circle(radius=r * 0.36, stroke_color=GREY, stroke_width=2.5, fill_color=GREY, fill_opacity=0.35).move_to([xs, y, 0])
    n = VGroup(prox, dist, soma, soma_f, nuc)
    n.prox, n.dist, n.soma, n.nuc, n.y, n.xc, n.xe = prox, dist, VGroup(soma, soma_f), nuc, y, xc, xe
    return n


def cutmark(x, y, h=0.9):
    return VGroup(*[Line([x + dx - 0.12, y - h / 2, 0], [x + dx + 0.12, y + h / 2, 0], color=TEXT, stroke_width=5)
                    for dx in (-0.2, 0.2)])


def do_cut(n, gap=0.18):
    return [n.prox.animate.shift(LEFT * gap), n.dist.animate.shift(RIGHT * gap)]


def strike(m, color=RED, w=6):
    return Line(m.get_left() + LEFT * 0.12 + DOWN * 0.14, m.get_right() + RIGHT * 0.12 + UP * 0.14, color=color, stroke_width=w)


def parcel(x, y, color=TEAL):
    return RoundedRectangle(corner_radius=0.06, width=0.3, height=0.3, stroke_color=color, stroke_width=2,
                            fill_color=color, fill_opacity=0.85).move_to([x, y, 0])


def run_parcels(ps, x_end, y, t=2.4, lag=0.3):
    return LaggedStart(*[Succession(FadeIn(p, run_time=0.15),
                                    p.animate(run_time=t, rate_func=linear).move_to([x_end, y, 0])) for p in ps],
                       lag_ratio=lag)


def mouse(scale=1.0):
    tail = CubicBezier([1.7, -0.4, 0], [2.9, -0.9, 0], [3.0, 0.6, 0], [3.9, 0.7, 0]).set_stroke(GREY, 7)
    body = Ellipse(width=3.6, height=2.1).set_fill(DARK, 1).set_stroke(GREY, 4)
    feet = VGroup(*[Ellipse(width=0.8, height=0.35).set_fill(DARK, 1).set_stroke(GREY, 3).move_to([x, -1.0, 0]) for x in (-0.7, 1.0)])
    head = Ellipse(width=1.7, height=1.4).set_fill(DARK, 1).set_stroke(GREY, 4).move_to([-2.0, 0.05, 0])
    ears = VGroup(*[Circle(radius=0.4).set_fill(DARK, 1).set_stroke(GREY, 4).move_to(p) for p in ([-1.7, 0.95, 0], [-2.35, 0.9, 0])])
    snout = Polygon([-3.4, -0.1, 0], [-2.55, 0.42, 0], [-2.55, -0.55, 0]).set_fill(DARK, 1).set_stroke(GREY, 4)
    eye = Dot([-2.15, 0.32, 0], radius=0.08, color=TEXT)
    nose = Dot([-3.38, -0.1, 0], radius=0.09, color=GREY)
    g = VGroup(tail, feet, body, ears, head, snout, eye, nose)
    g.scale(scale)
    g.move_to(ORIGIN)
    return g


def qmark(size=90, color=GOLD):
    return T("?", size, color, weight=BOLD)


def fusion_bar(s=1.0, with_label=True):
    """Ube4b start joined to NMNAT1 (labelled blocks)."""
    a = RoundedRectangle(corner_radius=0.1, width=2.3 * s, height=0.85 * s, stroke_color=GREY, stroke_width=3,
                         fill_color=GREY, fill_opacity=0.2)
    b = RoundedRectangle(corner_radius=0.1, width=2.4 * s, height=0.85 * s, stroke_color=TEAL, stroke_width=3,
                         fill_color=TEAL, fill_opacity=0.3)
    b.next_to(a, RIGHT, buff=0)
    ta = T("Ube4b start", 22 * s, GREY).move_to(a)
    tb = T("NMNAT1", 26 * s, TEAL).move_to(b)
    g = VGroup(a, b, ta, tb)
    g.a, g.b, g.ta, g.tb = a, b, ta, tb
    return g



def frags(x0, x1, y, h=0.4, seed=1, n=7, color=BLUE, op=0.3):
    """Uneven fragments of a broken axon (different lengths, small gaps, slight stagger)."""
    rng = np.random.default_rng(seed)
    w = rng.uniform(0.5, 1.5, n)
    gaps = rng.uniform(0.14, 0.38, n - 1)
    sc = (x1 - x0) / (w.sum() + gaps.sum())
    x = x0
    g = VGroup()
    for i in range(n):
        wi = w[i] * sc
        hi = h * rng.uniform(0.72, 1.0)
        g.add(RoundedRectangle(corner_radius=min(hi, wi) / 2.2, width=wi, height=hi, stroke_color=color, stroke_width=3.5,
                               fill_color=color, fill_opacity=op).move_to([x + wi / 2, y + rng.uniform(-0.08, 0.08), 0]))
        x += wi + (gaps[i] if i < n - 1 else 0)
    return g


def scissors(s=1.0):
    l1 = Line([0.75, 0.2, 0], [-0.3, -0.22, 0], color=TEXT, stroke_width=5)
    l2 = Line([0.75, -0.2, 0], [-0.3, 0.22, 0], color=TEXT, stroke_width=5)
    h1 = Circle(radius=0.17, stroke_color=PURPLE, stroke_width=5).move_to([-0.46, -0.27, 0])
    h2 = Circle(radius=0.17, stroke_color=PURPLE, stroke_width=5).move_to([-0.46, 0.27, 0])
    g = VGroup(l1, l2, h1, h2)
    g.scale(s)
    return g


def frog(s=1.0):
    body = Ellipse(width=1.0, height=0.55).set_fill(DARK, 1).set_stroke(GREY, 3)
    head = Ellipse(width=0.55, height=0.42).set_fill(DARK, 1).set_stroke(GREY, 3).move_to([-0.55, 0.1, 0])
    e1 = Circle(radius=0.09).set_fill(DARK, 1).set_stroke(GREY, 3).move_to([-0.6, 0.34, 0])
    e2 = Circle(radius=0.09).set_fill(DARK, 1).set_stroke(GREY, 3).move_to([-0.42, 0.34, 0])
    leg = VMobject(stroke_color=GREY, stroke_width=4).set_points_as_corners([[0.2, -0.15, 0], [0.55, -0.3, 0], [0.3, -0.42, 0], [0.0, -0.42, 0]])
    g = VGroup(leg, body, head, e1, e2)
    g.scale(s)
    return g


def pause_tag(x=5.3, y=3.4, dur=4.5):
    """'Pause: predict' label with a slow timer ring, so a deliberate stillness reads as one."""
    lab = T("Pause: predict", 28, GOLD)
    ring_bg = Circle(radius=0.24, stroke_color=GOLD, stroke_width=3, stroke_opacity=0.25)
    ring = Circle(radius=0.24, stroke_color=GOLD, stroke_width=5).rotate(PI / 2)
    grp = VGroup(ring_bg, lab).arrange(RIGHT, buff=0.2).move_to([x, y, 0])
    ring.move_to(ring_bg)
    return lab, ring_bg, ring


def run_timer(scene, ring, dur):
    scene.play(Create(ring, run_time=dur, rate_func=linear))


# ---------- the schematic survival plot (chapter 2) ----------
PX0, PX1 = -5.5, 1.9   # x of day 0 and day 21
PY0, PY1 = -2.4, 2.3   # y of "none intact" and "all intact"


def px(t):
    return PX0 + (PX1 - PX0) * t / 21.0


def py(f):
    return PY0 + (PY1 - PY0) * f


def sig(t, mid, k):
    return 1.0 / (1.0 + np.exp(k * (t - mid)))


def curve(mid, k, color, w=5):
    ts = np.linspace(0, 21, 170)
    m = VMobject(stroke_color=color, stroke_width=w)
    m.set_points_as_corners([[px(t), py(sig(t, mid, k)), 0] for t in ts])
    return m


def plot_axes(tag=True):
    xa = Arrow([PX0 - 0.1, PY0, 0], [PX1 + 0.45, PY0, 0], buff=0, color=GREY, stroke_width=3, tip_length=0.2)
    ya = Arrow([PX0, PY0 - 0.1, 0], [PX0, PY1 + 0.4, 0], buff=0, color=GREY, stroke_width=3, tip_length=0.2)
    ticks = VGroup()
    for d, s in ((0, "0"), (7, "7"), (14, "14"), (21, "21+")):
        ticks.add(Line([px(d), PY0 - 0.08, 0], [px(d), PY0 + 0.08, 0], color=GREY, stroke_width=3))
        ticks.add(M(s, 26, GREY).move_to([px(d), PY0 - 0.43, 0]))
    xl = T("days after the cut", 26, GREY).move_to([(PX0 + PX1) / 2, PY0 - 0.98, 0])
    yl = T("axons intact", 26, GREY).move_to([PX0 - 0.1, PY1 + 0.7, 0], aligned_edge=LEFT)
    g = VGroup(xa, ya, ticks, xl, yl)
    if tag:
        tg = T("schematic time course, not measured percentages", 22, GREY)
        tg.move_to([-6.5, 3.5, 0], aligned_edge=LEFT)
        g.add(tg)
    return g


WT_MID, WT_K = 1.75, 5.0
# Wlds and Sarm1-null are drawn as one curve: the lesson says only "two weeks or more" and "a long time".
LONG_MID, LONG_K = 22.0, 0.5


def wt_line():
    return curve(WT_MID, WT_K, GREY, 5)


def wlds_line(w=8):
    return curve(LONG_MID, LONG_K, TEAL, w)


def sarm_line():
    return curve(LONG_MID, LONG_K, RED, 3.5)


def run_off():
    y = py(sig(21, LONG_MID, LONG_K))
    return Arrow([px(21) + 0.02, y, 0], [px(21) + 0.5, y - 0.04, 0], buff=0, color=GREY, stroke_width=5, tip_length=0.22)


# ---------- the starving / program columns ----------
def chain(xs, y, dim=False, bw=0.95):
    blocks = VGroup(*[RoundedRectangle(corner_radius=0.1, width=bw, height=bw * 0.95, stroke_color=GOLD, stroke_width=3,
                                       fill_color=GOLD, fill_opacity=0.22).move_to([x, y, 0]) for x in xs])
    arrows = VGroup(*[arr([a + bw / 2 + 0.05, y, 0], [b - bw / 2 - 0.05, y, 0], GOLD, 4, 0.18) for a, b in zip(xs[:-1], xs[1:])])
    g = VGroup(blocks, arrows)
    g.blocks, g.arrows = blocks, arrows
    return g


CH_X = [1.4, 2.9, 4.4, 5.9]


# ---------- meters (NMNAT2, NMN, NAD+) ----------
class Meter:
    def __init__(self, x, color, level, label, h=3.3, w=0.9, ybot=-1.55):
        self.x, self.color, self.h, self.w, self.ybot = x, color, h, w, ybot
        self.frame = RoundedRectangle(corner_radius=0.1, width=w, height=h, stroke_color=GREY, stroke_width=3).move_to([x, ybot + h / 2, 0])
        self.fill = self._fill(level)
        self.ptr = Triangle(color=TEXT, fill_opacity=1, stroke_width=0).scale(0.2).rotate(PI / 2 * 3 - PI)  # points left
        self.ptr.move_to(self._ptr_pos(level))
        self.lab = T(label, 28, color).move_to([x, ybot - 0.4, 0])

    def _fill(self, level):
        hh = max(level * (self.h - 0.16), 0.02)
        return Rectangle(width=self.w - 0.16, height=hh, stroke_width=0, fill_color=self.color,
                         fill_opacity=0.8).move_to([self.x, self.ybot + 0.08 + hh / 2, 0])

    def _ptr_pos(self, level):
        return [self.x + self.w / 2 + 0.3, self.ybot + 0.08 + level * (self.h - 0.16), 0]

    def group(self):
        return VGroup(self.frame, self.fill, self.ptr, self.lab)

    def to(self, level):
        return [Transform(self.fill, self._fill(level)), self.ptr.animate.move_to(self._ptr_pos(level))]


MX = {"nmnat2": -4.6, "nmn": -0.4, "nad": 3.9}
LV0 = {"nmnat2": 0.85, "nmn": 0.3, "nad": 0.72}
NAD_FALLEN = 0.42   # where the NAD+ bar ends in s14 and starts again in s17


# ---------- the SARM1 ring (large, centred) ----------
RC = np.array([0.0, 0.0, 0.0])
SC = 1.2


def pol(R, a, sc=None):
    sc = SC if sc is None else sc
    return RC + R * sc * np.array([np.cos(a), np.sin(a), 0.0])


ANG = [i * TAU / 8 + TAU / 16 for i in range(8)]


def sarm(shifted=False, cargo="nad", tir="dim", sc=None):
    s = SC if sc is None else sc
    ring = Circle(radius=1.15 * s, stroke_color=RED, stroke_width=6).move_to(RC)
    nodes = VGroup(*[Dot(pol(1.15, a, s), radius=0.1 * s, color=RED) for a in ANG])
    arm_R = 2.28 if shifted else 2.1
    rot = 0.28 if shifted else 0.0
    spokes = VGroup(*[Line(pol(1.15, a, s), pol(arm_R - 0.4, a + rot, s), color=RED, stroke_width=3) for a in ANG])
    arms = VGroup(*[Circle(radius=0.45 * s, stroke_color=RED, stroke_width=3.5, fill_color=RED, fill_opacity=0.3).move_to(pol(arm_R, a + rot, s)) for a in ANG])
    ccol = GREEN if cargo == "nad" else ORANGE
    cg = VGroup(*[Dot(pol(arm_R + 0.18, a + rot, s), radius=0.17 * s, color=ccol) for a in ANG])
    if tir == "dim":
        op, col, fo = 0.75, GREY, 0.25
    else:
        op, col, fo = 1.0, TIRC, 0.5
    tirs = VGroup(*[Square(side_length=0.36 * s, stroke_color=col, stroke_width=3, fill_color=col, fill_opacity=fo)
                    .set_stroke(opacity=op).move_to(pol(0.68, a, s)).rotate(a) for a in ANG])
    g = VGroup(ring, nodes, spokes, arms, cg, tirs)
    g.ring, g.nodes, g.spokes, g.arms, g.cargo, g.tirs = ring, nodes, spokes, arms, cg, tirs
    return g


def leader(a, b, color=GREY):
    return Line(a, b, color=color, stroke_width=2.5, stroke_opacity=0.9)


def edge_pt(center, toward, r):
    d = np.array(toward) - np.array(center)
    return np.array(center) + r * d / np.linalg.norm(d)


# ---------- table (chapter 2, genetics) ----------
TC = (-4.0, 1.0, 4.9)
R1Y, R2Y = 1.3, -0.95


def table_frame():
    title = T("Development", 44, TEXT).move_to([0, 3.4, 0])
    hs = [T("mice", 32, GREY), T("survival", 32, GREY), T("axons", 32, GREY)]
    for h, x in zip(hs, TC):
        h.move_to([x, 2.75, 0])
        h.align_to([0, 2.62, 0], DOWN)      # common baseline (none of these words has a descender)
    heads = VGroup(*hs)
    r1 = RoundedRectangle(corner_radius=0.15, width=13.2, height=1.8, stroke_color=GREY, stroke_width=2).move_to([0, R1Y, 0])
    r2 = RoundedRectangle(corner_radius=0.15, width=13.2, height=2.2, stroke_color=GREY, stroke_width=2).move_to([0, R2Y, 0])
    return title, heads, r1, r2


def row1_cells():
    return (T("NMNAT2-deficient", 36, TEAL).move_to([TC[0], R1Y, 0]),
            T("die around birth", 36, TEXT).move_to([TC[1], R1Y, 0]),
            T("growth stalls", 36, TEXT).move_to([TC[2], R1Y, 0]))


def row2_label():
    a = T("NMNAT2-deficient", 36, TEAL)
    b = T("and Sarm1-null", 36, RED)
    return VGroup(a, b).arrange(DOWN, buff=0.14).move_to([TC[0], R2Y, 0])


def table_caption():
    return T("no cut: these are developing axons", 30, GREY).move_to([0, -3.15, 0])


def stump_shape(y=-1.0):
    """The same stump in s23 and s24: a long distal piece with three cytoskeleton lines."""
    st = tube(-3.4, 6.2, y, 2.8)
    lines = VGroup(*[Line([-3.2, y + d, 0], [6.0, y + d, 0], color=GREY, stroke_width=3) for d in (-0.7, 0.0, 0.7)])
    return st, lines


# =============================================================================================
# scenes
# =============================================================================================
class S00Title(TitleCard):
    LESSON = "Injury and Regeneration: Why the Brain Does Not Regrow"
    TITLE = "The Stump That Kills Itself"

    def construct(self):
        brand = T("BIOCHEMISTRYPEDIA", size=22, color=TEAL, weight=BOLD)
        lesson = T(self.LESSON.upper(), size=24, color=TEXT)
        fit(lesson, max_w=12.2)
        title = T(self.TITLE, size=58, font=TITLE_FONT)
        fit(title, max_w=11.5)
        rule = Line(LEFT * 1.2, RIGHT * 1.2, color=GOLD, stroke_width=4)
        g = VGroup(brand, lesson, title, rule).arrange(DOWN, buff=0.36)
        self.play(FadeIn(brand, shift=UP * 0.1), FadeIn(lesson, shift=UP * 0.1), run_time=self.beat(0.18))
        self.play(Write(title), GrowFromCenter(rule), run_time=self.beat(0.3))
        self.wait(self.beat(0.4))
        self.play(FadeOut(g), run_time=self.beat(0.12))
        self.finish()


class S01Q(SpokenScene):
    def construct(self):
        n = neuron(0.7, xs=-5.2, xe=6.3, xc=0.3, h=1.3, r=1.4)
        self.play(FadeIn(n), run_time=0.5)
        self.at("cut off axon")
        cm = cutmark(0.3, 0.7, 2.0)
        self.play(*do_cut(n, 0.3), FadeIn(cm), run_time=0.5)
        self.at("fall apart")
        q = qmark(110, GREY).move_to([3.4, 2.6, 0])
        self.play(n.dist.animate.set_stroke(GREY).set_fill(GREY, 0.12), FadeIn(q), run_time=0.7)
        self.at("starving")
        c1 = bchip("starving?", GREY, 42).move_to([-3.1, -2.0, 0])
        self.play(FadeIn(c1, shift=UP * 0.2), run_time=0.5)
        self.at("following orders")
        c2 = bchip("following orders?", GOLD, 42).move_to([2.9, -2.0, 0])
        self.play(FadeIn(c2, shift=UP * 0.2), run_time=0.5)
        self.finish()


class S02Waller(SpokenScene):
    def construct(self):
        ys = [2.0, 1.0, 0.0, -1.0, -2.0]
        prox = VGroup(*[tube(-6.2, 0.0, y, 0.5) for y in ys])
        dist = VGroup(*[tube(0.0, 6.2, y, 0.5) for y in ys])
        cm = cutmark(0.0, 0.0, 5.0)
        year = T("1850", 40, GOLD, font=TITLE_FONT)
        name = T("Augustus Waller", 40, TEXT, font=TITLE_FONT)
        cred = VGroup(year, name).arrange(RIGHT, buff=0.5).move_to([0, 3.4, 0])
        fl = T("frog tongue nerves (schematic)", 30, GREY).move_to([0, 2.65, 0])
        self.play(FadeIn(prox), FadeIn(dist), FadeIn(fl), run_time=0.3)
        self.at("1850")
        self.play(FadeIn(year, shift=DOWN * 0.1), run_time=0.4)
        self.at("Augustus Waller")
        self.play(FadeIn(name, shift=DOWN * 0.1), run_time=0.4)
        self.at("cut frog nerve")
        self.play(prox.animate.shift(LEFT * 0.2), dist.animate.shift(RIGHT * 0.2), FadeIn(cm), run_time=0.5)
        self.at("break up")
        dl = T("days later", 30, GREY).move_to([3.4, -2.8, 0])
        frag = VGroup(*[frags(0.4, 6.2, y, 0.5, seed=10 + k, n=6 + (k % 3)) for k, y in enumerate(ys)])
        self.play(FadeIn(dl), *[FadeOut(dist[i]) for i in range(5)], *[FadeIn(frag[i]) for i in range(5)], run_time=1.2)
        self.at("nutrition")
        nut = T("nutrition?", 48, GREY).move_to([3.3, -3.15, 0])
        self.play(FadeOut(dl), FadeIn(nut, shift=UP * 0.15), run_time=0.5)
        self.finish()


class S03Logic(SpokenScene):
    def construct(self):
        div = Line([0, -2.3, 0], [0, 3.7, 0], color=GREY, stroke_opacity=0.35)
        hs = T("Starving", 50, GREY).move_to([-3.4, 3.15, 0])
        hp = T("Program", 50, GOLD).move_to([3.4, 3.15, 0])
        stump = tube(-6.3, -0.5, 1.5, 1.5, GREY, 0.12)
        ch = chain(CH_X, 1.5, bw=1.1)
        out = frags(0.9, 6.2, -0.4, 1.1, seed=4, n=6, color=GREY, op=0.15)
        down = arr([5.9, 0.85, 0], [5.9, 0.2, 0], GOLD, 4, 0.18)
        self.play(FadeIn(div), FadeIn(hs), FadeIn(hp), FadeIn(stump), FadeIn(ch), FadeIn(out), FadeIn(down), run_time=0.6)
        self.at("starving")
        self.play(Indicate(hs, color=GREY, scale_factor=1.1), run_time=0.5)
        frame = RoundedRectangle(corner_radius=0.1, width=5.4, height=0.9, stroke_color=TEAL, stroke_width=3).move_to([-3.4, -0.4, 0])
        fill = Rectangle(width=1.1, height=0.74, stroke_width=0, fill_color=TEAL, fill_opacity=0.8).move_to([-6.0 + 0.55 + 0.0, -0.4, 0])
        fill.align_to(frame, LEFT).shift(RIGHT * 0.08)
        sl = T("supply", 36, TEAL).move_to([-3.4, -1.35, 0])
        self.at("replacing")
        self.play(FadeIn(frame), FadeIn(fill), FadeIn(sl), run_time=0.5)
        self.at("save it")
        full = Rectangle(width=5.24, height=0.74, stroke_width=0, fill_color=TEAL, fill_opacity=0.8).align_to(frame, LEFT).shift(RIGHT * 0.08)
        full.match_y(frame)
        saved = T("delayed", 50, BLUE).move_to([-3.4, -2.7, 0])
        self.play(Transform(fill, full), stump.animate.set_stroke(BLUE).set_fill(BLUE, 0.3), FadeIn(saved), run_time=0.8)
        self.at("If it is a program")
        self.play(Indicate(hp, color=GOLD, scale_factor=1.1), run_time=0.5)
        self.at("deleting one part")
        cross = Cross(ch.blocks[2], stroke_color=RED, stroke_width=7)
        self.play(Create(cross), ch.blocks[2].animate.set_opacity(0.3), run_time=0.6)
        self.at("should stop it")
        whole = tube(0.9, 6.2, -0.4, 1.0, BLUE, 0.3)
        stopped = T("stops", 50, BLUE).move_to([3.4, -2.7, 0])
        self.play(FadeOut(out), FadeIn(whole), FadeOut(down), FadeIn(stopped), run_time=0.8)
        self.finish()


class S04Ask(SpokenScene):
    def construct(self):
        m = mouse(1.4).move_to([0, 0.2, 0])
        self.play(FadeIn(m), run_time=0.5)
        q = qmark(120).move_to([-0.6, 3.0, 0])
        t = T("What mouse would decide it?", 42, TEXT).move_to([0, -2.9, 0])
        self.at("decide it")
        self.play(FadeIn(q, shift=DOWN * 0.15), FadeIn(t), run_time=0.4)
        self.finish()


class S05Pause(NarratedScene):
    def construct(self):
        m = mouse(1.4).move_to([0, 0.2, 0])
        q = qmark(120).move_to([-0.6, 3.0, 0])
        t = T("What mouse would decide it?", 42, TEXT).move_to([0, -2.9, 0])
        lab, bg, ring = pause_tag(5.2, 3.4)
        self.add(m, q, t, lab, bg)
        self.play(Create(ring, run_time=4.5, rate_func=linear))
        self.finish()


class S06Rev(SpokenScene):
    def construct(self):
        m = mouse(1.25).move_to([0, 1.55, 0])
        self.play(FadeIn(m), run_time=0.4)
        self.at("missing a part")
        gene = bchip("gene", GOLD, 40).move_to(m.get_center() + DOWN * 0.1)
        cap = T("missing a part of the program", 36, GOLD).move_to([0, -0.2, 0])
        self.play(FadeIn(gene), FadeIn(cap), run_time=0.4)
        cross = strike(gene)
        self.play(Create(cross), run_time=0.4)
        self.at("cut axons stay")
        a = tube(-4.6, -0.4, -1.45, 0.9)
        b = tube(0.4, 4.6, -1.45, 0.9)
        cm = cutmark(0, -1.45, 1.6)
        w = T("cut axons stay whole", 42, BLUE).move_to([0, -3.0, 0])
        self.play(FadeIn(a), FadeIn(b), FadeIn(cm), FadeIn(w), run_time=0.6)
        self.at("But the first clue")
        ax = plot_axes()
        self.play(*[FadeOut(x) for x in (m, gene, cross, cap, a, b, cm, w)], run_time=0.45)
        self.play(FadeIn(ax), run_time=0.45)
        self.finish()


class S06bWlds(SpokenScene):
    def construct(self):
        ax = plot_axes()
        self.add(ax)
        wt = wt_line()
        wl = wlds_line()
        ro = run_off()
        wtl = T("normal mouse", 28, GREY).move_to([px(2.8), py(0.5), 0], aligned_edge=LEFT)
        wll = T("slow mouse (Wlds)", 28, TEAL).move_to([px(3.2), py(0.84), 0], aligned_edge=LEFT)
        self.play(Create(wt), FadeIn(wtl), run_time=1.0)
        self.at("cut axons last")
        self.play(Create(wl), FadeIn(wll), run_time=1.0)
        self.add(ro)
        self.at("two weeks")
        d14 = DashedLine([px(14), PY0, 0], [px(14), PY1, 0], color=GREY, stroke_width=3)
        big = T("two weeks\nor more", 44, TEAL).move_to([4.6, 0.3, 0])
        self.play(Create(d14), FadeIn(big), run_time=0.6)
        self.finish()


class S07Wlds2(SpokenScene):
    def construct(self):
        fb = fusion_bar(1.9).move_to([0, 0.6, 0])
        pa = VGroup(fb.a.copy(), fb.ta.copy()).shift(LEFT * 1.5)
        pb = VGroup(fb.b.copy(), fb.tb.copy()).shift(RIGHT * 1.5)
        mut = T("the slow mouse's mutation", 34, GREY).move_to([0, 2.9, 0])
        self.at("mutation")
        self.play(FadeIn(mut), FadeIn(pa), FadeIn(pb), run_time=0.6)
        self.at("odd fusion")
        self.play(pa.animate.shift(RIGHT * 1.5), pb.animate.shift(LEFT * 1.5), run_time=0.7)
        self.remove(pa, pb)
        self.add(fb)
        self.at("an enzyme")
        self.play(Indicate(VGroup(fb.b, fb.tb), color=TEAL, scale_factor=1.04), run_time=0.6)
        self.at("makes NAD")
        bx = fb.b.get_center()[0]
        mk = T("makes NAD+", 46, GREEN).move_to([bx, -1.9, 0])
        ar = arr([bx, -0.35, 0], [bx, -1.3, 0], GREEN, 6, 0.24)
        self.play(FadeIn(ar), FadeIn(mk), run_time=0.5)
        self.at("Remember")
        glow = SurroundingRectangle(fb.b, color=TEAL, buff=0.12, stroke_width=5)
        self.play(Create(glow), run_time=0.5)
        self.finish()


class S07bLimit(SpokenScene):
    def construct(self):
        fb = fusion_bar(1.9).move_to([0, 0.6, 0])
        bx = fb.b.get_center()[0]
        mk = T("makes NAD+", 46, GREEN).move_to([bx, -1.9, 0])
        ar = arr([bx, -0.35, 0], [bx, -1.3, 0], GREEN, 6, 0.24)
        glow = SurroundingRectangle(fb.b, color=TEAL, buff=0.12, stroke_width=5)
        self.add(fb, mk, ar, glow)
        self.wait(0.3)
        self.at("might replace")
        div = Line([0, -2.2, 0], [0, 3.7, 0], color=GREY, stroke_opacity=0.35)
        hs = T("Starving", 44, GREY).move_to([-3.4, 3.2, 0])
        hp = T("Program", 44, GOLD).move_to([3.4, 3.2, 0])
        stump = tube(-6.3, -0.5, 1.9, 1.0, GREY, 0.12)
        ch = chain(CH_X, 1.9, bw=1.0).set_opacity(0.4)
        self.play(FadeOut(mk), FadeOut(ar), FadeOut(glow), FadeIn(div), FadeIn(hs), FadeIn(hp), FadeIn(stump), FadeIn(ch), run_time=0.7)
        self.play(fb.animate.scale(1.3 / 1.9).move_to([-3.4, -0.3, 0]), run_time=0.8)
        up = arr([-3.4, 0.45, 0], [-3.4, 1.35, 0], TEAL, 9, 0.32)
        self.play(GrowArrow(up), stump.animate.set_stroke(BLUE).set_fill(BLUE, 0.3), run_time=0.6)
        self.at("That alone")
        lab = T("not yet proof of a program", 44, GOLD).move_to([0, -2.95, 0])
        q = qmark(110).move_to([3.4, -0.3, 0])
        self.play(FadeIn(lab), FadeIn(q, scale=0.7), run_time=0.6)
        self.finish()


def plot_state():
    ax = plot_axes()
    parts = [ax, wt_line(), T("normal mouse", 28, GREY).move_to([px(2.8), py(0.5), 0], aligned_edge=LEFT),
             wlds_line(), T("slow mouse (Wlds)", 28, TEAL).move_to([px(3.2), py(0.84), 0], aligned_edge=LEFT), run_off()]
    return parts


def s08_panel():
    bp = RoundedRectangle(corner_radius=0.15, width=3.9, height=1.9, stroke_color=GOLD, stroke_width=3).move_to([4.65, 1.6, 0])
    bs = RoundedRectangle(corner_radius=0.15, width=3.9, height=1.9, stroke_color=GREY, stroke_width=3).move_to([4.65, -0.55, 0])
    hp = T("Program", 32, GOLD).move_to([4.65, 2.2, 0])
    hs = T("Starving", 32, GREY).move_to([4.65, 0.05, 0])
    wc = bchip("Wlds", TEAL, 30).move_to([4.65, -2.25, 0])
    wn = T("delays the program,\nexplained later", 24, TEAL).move_to([4.65, -3.15, 0])
    cred = T("Freeman laboratory and\ncollaborators, 2012", 24, GREY).move_to([-0.1, -1.6, 0])
    return bs, bp, hs, hp, wc, wn, cred


def sarm_label():
    lab = T("Sarm1-null", 28, RED).move_to([px(12.0), py(0.6), 0], aligned_edge=LEFT)
    ld = leader([px(15.5), py(0.6) + 0.22, 0], [px(15.9), py(sig(15.9, LONG_MID, LONG_K)) - 0.06, 0], RED)
    return lab, ld


class S08Sarm(SpokenScene):
    def construct(self):
        parts = plot_state()
        self.add(*parts)
        bs, bp, hs, hp, wc, wn, cred = s08_panel()
        self.add(bs, bp, hs, hp, wc, wn)
        self.at("deciding mouse")
        self.wait(0.2)
        self.at("ordinary gene")
        gene = bchip("Sarm1", RED, 32).move_to([4.65, 3.2, 0])
        self.play(FadeIn(gene, shift=DOWN * 0.2), run_time=0.5)
        cross = strike(gene)
        self.play(Create(cross), FadeIn(cred), run_time=0.4)
        self.at("kept cut axons")
        sl = sarm_line()
        sll, sld = sarm_label()
        self.play(Create(sl), run_time=1.6)
        self.play(FadeIn(sll), FadeIn(sld), run_time=0.4)
        self.at("The stump carries")
        self.play(FadeOut(cross), gene.animate.move_to([4.65, 1.45, 0]), run_time=0.9)
        self.play(bp.animate.set_fill(GOLD, 0.18), run_time=0.5)
        self.finish()
        self.wait(0.6)


class S09Beat(NarratedScene):
    def construct(self):
        parts = plot_state()
        sl = sarm_line()
        sll, sld = sarm_label()
        bs, bp, hs, hp, wc, wn, cred = s08_panel()
        bp.set_fill(GOLD, 0.18)
        gene = bchip("Sarm1", RED, 32).move_to([4.65, 1.45, 0])
        self.add(*parts, sl, sll, sld, bs, bp, hs, hp, wc, wn, gene, cred)
        self.wait(1.9)
        self.finish()


def axon_scale_parts():
    soma = VGroup(Circle(radius=1.5, stroke_color=BLUE, stroke_width=4, fill_color=BG, fill_opacity=1),
                  Circle(radius=1.5, stroke_width=0, fill_color=BLUE, fill_opacity=0.3),
                  Circle(radius=0.55, stroke_color=GREY, stroke_width=2.5, fill_color=GREY, fill_opacity=0.35)).move_to([-4.7, 0.6, 0])
    ax = tube(-3.2, 6.6, 0.6, 0.8)
    brk = VGroup(*[Line([x - 0.12, 0.2, 0], [x + 0.12, 1.0, 0], color=TEXT, stroke_width=4) for x in (2.3, 2.6)])
    return soma, ax, brk


def brace(x0, x1, y, up=False, color=BLUE):
    d = 0.14 if up else -0.14
    return VGroup(Line([x0, y, 0], [x1, y, 0], color=color, stroke_width=3),
                  Line([x0, y, 0], [x0, y - d, 0], color=color, stroke_width=3),
                  Line([x1, y, 0], [x1, y - d, 0], color=color, stroke_width=3))


class S10Scale(SpokenScene):
    def construct(self):
        soma, ax, brk = axon_scale_parts()
        self.play(FadeIn(soma), GrowFromEdge(ax, LEFT), run_time=1.2)
        self.at("meter long axon")
        br = brace(-3.0, 6.4, 1.45, up=True)
        l1 = T("axon: 1 m long", 34, BLUE).move_to([1.7, 1.95, 0])
        self.play(Create(br), FadeIn(l1), FadeIn(brk), run_time=0.9)
        self.at("micrometers wide")
        ld = leader([5.4, 0.35, 0], [5.0, -0.45, 0], TEXT)
        l2 = T("10 µm wide", 30, TEXT).move_to([5.0, -0.8, 0])
        self.play(FadeIn(ld), FadeIn(l2), run_time=0.5)
        self.at("thousand times")
        vb = brace(-3.0, 6.4, -1.55)
        big = T("about 1,000 times the volume", 38, TEXT).move_to([1.7, -2.15, 0])
        self.play(Create(vb), FadeIn(big, shift=DOWN * 0.15), run_time=0.7)
        self.at("cell body")
        sb = brace(-6.2, -3.2, -1.55)
        l3 = T("cell body", 32, BLUE).move_to([-4.7, -2.15, 0])
        self.play(Create(sb), Indicate(soma, color=BLUE, scale_factor=1.05), FadeIn(l3), run_time=0.7)
        self.at("50 micrometers")
        l4 = T("50 µm across", 30, TEXT).move_to([-4.7, -2.75, 0])
        ap = T("approximate shapes, not to scale", 24, GREY).move_to([1.7, -3.2, 0])
        self.play(FadeIn(l4), FadeIn(ap), run_time=0.5)
        self.at("depends on")
        ps = [parcel(-3.55, 0.6) for _ in range(4)]
        dl = T("deliveries", 32, TEAL).move_to([-0.4, -0.55, 0])
        self.play(FadeIn(dl), run_time=0.3)
        self.play(run_parcels(ps, 6.2, 0.6, t=1.3, lag=0.3), run_time=2.5)
        self.finish()


def top_neuron():
    """The cell body and axon, small, along the top (the same strip used in s11b to s14)."""
    n = neuron(0.7, xs=-5.2, xe=6.3, xc=-1.5, h=1.2, r=1.3)
    # A single outline has no rounded segment seam before the cut.
    n.remove(n.prox, n.dist)
    n.add_to_back(tube(-5.2, 6.3, 0.7, 1.2))
    return n


def small_neuron():
    n = top_neuron()
    n.scale(0.55).move_to([0, 3.0, 0])
    return n


RY = -0.65   # y of the reaction row (NMN, arrow, NAD+)


def reaction_row(y=RY):
    nmn = bchip("NMN", ORANGE, 64).move_to([-4.7, y, 0])
    nad = bchip("NAD+", GREEN, 64).move_to([4.8, y, 0])
    ar = arr([-3.1, y, 0], [3.1, y, 0], GREY, 10, 0.36)
    return nmn, ar, nad


class S11Nmnat2(SpokenScene):
    def construct(self):
        n = top_neuron()
        self.add(n)
        self.at("key delivery")
        c = bchip("NMNAT2", TEAL, 30).move_to([-3.6, 0.7, 0])
        self.play(FadeIn(c), run_time=0.3)
        self.play(c.animate.move_to([3.0, 0.7, 0]), run_time=1.5, rate_func=linear)
        self.at("least stable")
        ls = T("least stable", 38, TEAL).move_to([3.0, -0.55, 0])
        self.play(FadeIn(ls), c[1].animate.set_stroke(TEAL, width=2.5, opacity=0.6), run_time=0.5)
        nmn, ar, nad = reaction_row()
        self.at("turns")
        self.play(n.animate.scale(0.55).move_to([0, 3.0, 0]), c.animate.scale(1.6).move_to([0, 0.5, 0]),
                  ls.animate.move_to([3.9, 0.5, 0]), FadeIn(nmn), run_time=0.9)
        self.at("nicotinamide mononucleotide")
        nl = T("nicotinamide\nmononucleotide", 30, ORANGE).move_to([-4.7, -2.1, 0])
        self.play(FadeIn(nl), run_time=0.5)
        self.at("into")
        self.play(GrowArrow(ar), run_time=0.5)
        self.play(FadeIn(nad), run_time=0.4)
        self.finish()
        self.wait(0.6)


class S11bWlds(SpokenScene):
    def construct(self):
        n = small_neuron()
        c = bchip("NMNAT2", TEAL, 30).scale(1.6).move_to([0, 0.5, 0])
        c[1].set_stroke(TEAL, width=2.5, opacity=0.6)
        ls = T("least stable", 38, TEAL).move_to([3.9, 0.5, 0])
        nmn, ar, nad = reaction_row()
        nl = T("nicotinamide\nmononucleotide", 30, ORANGE).move_to([-4.7, -2.1, 0])
        self.add(n, c, ls, nmn, ar, nad, nl)
        self.at("fusion protein")
        fb = fusion_bar(1.0).move_to([0, 0.5, 0])
        self.play(FadeOut(c), FadeOut(ls), FadeIn(fb), run_time=0.6)
        self.at("longer lived")
        ll = T("longer-lived NMNAT activity", 30, TEAL).move_to([0, 1.6, 0])
        self.play(FadeIn(ll), run_time=0.5)
        self.at("keeps that job")
        d = Dot([-3.0, RY, 0], radius=0.19, color=ORANGE)
        self.add(d)
        self.play(d.animate.move_to([3.0, RY, 0]).set_color(GREEN), run_time=0.9, rate_func=linear)
        self.play(Indicate(nad, color=GREEN), FadeOut(d), run_time=0.3)
        self.at("after a cut")
        keep = T("keeps making NAD+", 38, GREEN).move_to([1.1, -2.8, 0])
        self.play(FadeIn(keep), run_time=0.5)
        d2 = Dot([-3.0, RY, 0], radius=0.19, color=ORANGE)
        self.add(d2)
        self.play(d2.animate.move_to([3.0, RY, 0]).set_color(GREEN), run_time=0.9, rate_func=linear)
        self.play(Indicate(nad, color=GREEN), FadeOut(d2), run_time=0.4)
        self.finish()
        self.wait(0.4)


def meters(levels=None):
    lv = dict(LV0)
    if levels:
        lv.update(levels)
    return {k: Meter(MX[k], c, lv[k], lab) for k, c, lab in
            (("nmnat2", TEAL, "NMNAT2"), ("nmn", ORANGE, "NMN"), ("nad", GREEN, "NAD+"))}


def meter_tag():
    return T("schematic, relative levels", 22, GREY).move_to([-2.4, 2.25, 0])


def strip(cut=False):
    n = neuron(3.05, xs=-6.0, xe=6.4, xc=-1.5, h=0.7, r=0.6)
    if not cut:
        n.prox.set_opacity(0)
        n.dist.set_opacity(0)
        n.whole = tube(-6.0, 6.4, 3.05, 0.7)
        n.add_to_back(n.whole)
    if cut:
        n.prox.shift(LEFT * 0.25)
        n.dist.shift(RIGHT * 0.25)
    return n


class S12Q2(SpokenScene):
    def construct(self):
        n = strip()
        mt = meters()
        ps = VGroup(*[parcel(x, 3.05) for x in (-4.4, -3.2, -2.1, 0.8, 2.3, 3.8)])
        tag = meter_tag()
        self.add(n, ps, tag, *[m.group() for m in mt.values()])
        self.at("cut")
        cm = cutmark(-1.5, 3.05, 1.2)
        n.remove(n.whole)
        n.prox.set_opacity(1).set_fill(BLUE, 0.3)
        n.dist.set_opacity(1).set_fill(BLUE, 0.3)
        self.play(*do_cut(n, 0.25), FadeIn(cm), run_time=0.5)
        self.at("stops arriving")
        self.play(*mt["nmnat2"].to(0.06), FadeOut(ps[3:]), run_time=1.2)
        self.at("What happens")
        t = T("What happens to NMN, and to NAD+?", 34, TEXT).move_to([0, -3.3, 0])
        lab, bg, ring = pause_tag(4.5, 2.25)
        self.play(FadeIn(t), FadeIn(lab), FadeIn(bg), run_time=0.4)
        self.at("NMN")
        q1 = qmark(60).move_to([MX["nmn"] + 1.55, 0.2, 0])
        self.play(FadeIn(q1, scale=0.6), Indicate(mt["nmn"].frame, color=ORANGE), run_time=0.5)
        self.at("and to")
        q2 = qmark(60).move_to([MX["nad"] + 1.55, 0.2, 0])
        self.play(FadeIn(q2, scale=0.6), Indicate(mt["nad"].frame, color=GREEN), run_time=0.5)
        self.finish()


class S13Pause(NarratedScene):
    def construct(self):
        n = strip(cut=True)
        mt = meters({"nmnat2": 0.06})
        t = T("What happens to NMN, and to NAD+?", 34, TEXT).move_to([0, -3.3, 0])
        q1 = qmark(60).move_to([MX["nmn"] + 1.55, 0.2, 0])
        q2 = qmark(60).move_to([MX["nad"] + 1.55, 0.2, 0])
        lab, bg, ring = pause_tag(4.5, 2.25)
        self.add(n, cutmark(-1.5, 3.05, 1.2), t, q1, q2, meter_tag(), lab, bg, *[m.group() for m in mt.values()])
        self.play(Create(ring, run_time=4.5, rate_func=linear))
        self.finish()


class S14Rev2(SpokenScene):
    def construct(self):
        n = strip(cut=True)
        mt = meters({"nmnat2": 0.06})
        self.add(n, cutmark(-1.5, 3.05, 1.2), meter_tag(), *[m.group() for m in mt.values()])
        self.wait(0.3)
        self.at("piles up")
        self.play(*mt["nmn"].to(0.92), run_time=1.0)
        self.at("falls")
        self.play(*mt["nad"].to(NAD_FALLEN), run_time=1.0)
        self.at("ratio")
        r1 = T("NMN to NAD+ ratio: rising", 36, TEXT).move_to([-0.4, -3.0, 0])
        up = Arrow([r1.get_right()[0] + 0.45, -3.3, 0], [r1.get_right()[0] + 0.45, -2.65, 0], buff=0, color=ORANGE, stroke_width=9, tip_length=0.3)
        self.play(FadeIn(r1), GrowArrow(up), run_time=0.7)
        self.at("enzyme fails")
        note = T("(NMN supply and NAD+ use also move it)", 24, GREY).move_to([-0.4, -3.55, 0])
        self.play(FadeIn(note), Indicate(mt["nmnat2"].frame, color=TEAL), run_time=0.7)
        self.finish()
        self.wait(0.4)


def sarm_title():
    return T("SARM1: a ring of eight", 36, RED).move_to([-6.6, 3.35, 0], aligned_edge=LEFT)


def s15_labels():
    """Labels with leader lines for the ring (right side: ARM and TIR; left: the ring)."""
    tp = pol(0.68, -TAU / 16)
    tl = T("TIR domains\nkept apart", 30, TIRC).move_to([5.3, tp[1], 0])
    ll = leader([3.75, tp[1], 0], tp + RIGHT * 0.18)
    ac = pol(2.1, TAU / 16)
    ae = edge_pt(ac, [3.9, 1.8, 0], 0.45 * SC)
    al = T("ARM domains\nhold NAD+", 30, RED).move_to([5.3, 1.9, 0])
    al2 = leader([3.8, 1.8, 0], ae)
    cl = T("central\nring", 30, RED).move_to([-5.2, 0.0, 0])
    cl2 = leader([-4.1, 0.0, 0], pol(1.15, PI) + LEFT * 0.04)
    return tl, ll, al, al2, cl, cl2


class S15Gauge(SpokenScene):
    def construct(self):
        s = sarm()
        title = sarm_title()
        tl, ll, al, al2, cl, cl2 = s15_labels()
        self.at("SARM 1")
        self.play(Create(s.ring), FadeIn(s.nodes), FadeIn(title), run_time=0.8)
        ratio = T("senses the ratio", 30, GREY).move_to([6.6, 3.35, 0], aligned_edge=RIGHT)
        self.play(FadeIn(ratio), run_time=0.4)
        self.at("ring of eight")
        self.play(FadeIn(s.spokes), FadeIn(s.arms), FadeIn(cl), Create(cl2), run_time=0.8)
        self.at("held off")
        self.play(FadeIn(s.tirs), FadeIn(tl), Create(ll), run_time=0.5)
        self.at("while NAD")
        self.play(FadeIn(s.cargo), FadeIn(al), Create(al2), run_time=0.7)
        self.finish()


class S16Open(SpokenScene):
    def construct(self):
        s = sarm()
        title = sarm_title()
        tl, ll, al, al2, cl, cl2 = s15_labels()
        self.add(s, title, tl, ll, al, al2, cl, cl2)
        self.at("leading model")
        lm = T("leading model", 32, GOLD).move_to([6.6, 3.35, 0], aligned_edge=RIGHT)
        self.play(FadeIn(lm), run_time=0.4)
        self.at("NMN competes")
        nmn_new = sarm(cargo="nmn").cargo
        start = VGroup(*[Dot(pol(3.15, a), radius=0.17 * SC, color=ORANGE) for a in ANG])
        nl = T("NMN competes\nfor the site", 30, ORANGE).move_to([5.3, 1.9, 0])
        self.play(FadeIn(start), run_time=0.4)
        self.play(Transform(start, nmn_new), s.cargo.animate.set_opacity(0), FadeOut(al), FadeIn(nl), al2.animate.set_color(ORANGE), run_time=1.1)
        self.at("binding shifts")
        s2 = sarm(shifted=True, cargo="nmn")
        ac2 = pol(2.28, TAU / 16 + 0.28)
        al2b = leader([3.8, 1.8, 0], edge_pt(ac2, [3.9, 1.8, 0], 0.45 * SC), ORANGE)
        self.play(Transform(s.arms, s2.arms), Transform(s.spokes, s2.spokes), Transform(start, s2.cargo),
                  Transform(al2, al2b), run_time=1.0)
        self.at("frees")
        s3 = sarm(shifted=True, cargo="nmn", tir="bright")
        tl2 = T("TIR domains\nfreed", 30, TIRC).move_to(tl.get_center())
        self.play(Transform(s.tirs, s3.tirs), FadeOut(tl), FadeIn(tl2), run_time=0.8)
        self.play(*[Indicate(t, color=TIRC, scale_factor=1.4) for t in s.tirs], run_time=0.7)
        self.finish()


def hub_target(sc=0.9):
    return Circle(radius=0.55 * sc, stroke_color=TIRC, stroke_width=4, fill_color=TIRC, fill_opacity=0.55).move_to(RC)


NB = dict(x=-5.0, ybot=-1.9, h=3.4, w=0.8)


def nad_bar(level):
    x, ybot, h, w = NB["x"], NB["ybot"], NB["h"], NB["w"]
    frame = RoundedRectangle(corner_radius=0.1, width=w, height=h, stroke_color=GREY, stroke_width=3).move_to([x, ybot + h / 2, 0])
    hh = max(level * (h - 0.16), 0.02)
    fill = Rectangle(width=w - 0.16, height=hh, stroke_width=0, fill_color=GREEN, fill_opacity=0.8).move_to([x, ybot + 0.08 + hh / 2, 0])
    lab = T("NAD+", 28, GREEN).move_to([x, ybot - 0.4, 0])
    return frame, fill, lab


def nad_level_y(level):
    return NB["ybot"] + 0.08 + level * (NB["h"] - 0.16)


S17SC = 0.9


def s17_loop():
    lbl = T("proposed feedback", 30, GOLD).move_to([4.9, 3.3, 0])
    c1 = bchip("less NAD+", GREEN, 30).move_to([5.0, 2.2, 0])
    c2 = bchip("higher ratio", ORANGE, 30).move_to([5.0, 0.3, 0])
    a1 = arr([5.0, 1.75, 0], [5.0, 0.8, 0], GREY, 5, 0.2)
    c3 = bchip("more SARM1\nactivity", RED, 30).move_to([5.0, -1.9, 0])
    a2 = arr([5.0, -0.25, 0], [5.0, -1.2, 0], GREY, 5, 0.2)
    back = CurvedArrow([3.6, -1.9, 0], [3.6, 2.2, 0], angle=-TAU / 5, color=GREY, stroke_width=5, tip_length=0.22)
    return lbl, c1, c2, a1, c3, a2, back


def s17_cut_arrow(level):
    return arr([-0.5, -0.3, 0], [NB["x"] + 0.5, nad_level_y(level) + 0.0, 0], TIRC, 6, 0.24)


class S17Tir(SpokenScene):
    def construct(self):
        s = sarm(shifted=True, cargo="nmn", tir="bright")
        title = sarm_title()
        self.add(s, title)
        self.play(s.animate.scale(S17SC / SC, about_point=ORIGIN), run_time=0.8)
        self.at("freed")
        self.play(*[Indicate(t, color=TIRC, scale_factor=1.3) for t in s.tirs], run_time=0.8)
        self.at("come together")
        hub = hub_target()
        self.play(*[t.animate.move_to(RC).scale(0.4).set_opacity(0) for t in s.tirs], FadeIn(hub), run_time=1.1)
        s.remove(s.tirs)
        self.at("enzyme")
        el = T("TIR enzyme", 32, TIRC).move_to([0, -3.3, 0])
        self.play(FadeIn(el), run_time=0.4)
        self.at("that cleaves")
        frame, fill, lab = nad_bar(NAD_FALLEN)
        self.play(FadeIn(frame), FadeIn(fill), FadeIn(lab), run_time=0.5)
        cut = s17_cut_arrow(NAD_FALLEN)
        self.play(GrowArrow(cut), Transform(fill, nad_bar(0.3)[1]), run_time=0.9)
        lbl, c1, c2, a1, c3, a2, back = s17_loop()
        self.at("each loss")
        self.play(FadeIn(lbl), FadeIn(c1), run_time=0.4)
        self.at("ratio higher")
        self.play(GrowArrow(a1), FadeIn(c2), run_time=0.5)
        self.at("slow drift")
        self.play(GrowArrow(a2), FadeIn(c3), Create(back), run_time=0.8)
        self.at("a crash")
        self.play(Transform(fill, nad_bar(0.03)[1].set_fill(RED, 0.9)), run_time=0.6)
        self.finish()


class S17bBeat(NarratedScene):
    def construct(self):
        s = sarm(shifted=True, cargo="nmn", tir="bright", sc=S17SC)
        s.remove(s.tirs)
        hub = hub_target()
        title = sarm_title()
        el = T("TIR enzyme", 32, TIRC).move_to([0, -3.3, 0])
        frame, fill, lab = nad_bar(NAD_FALLEN)
        fill = nad_bar(0.03)[1].set_fill(RED, 0.9)
        cut = s17_cut_arrow(NAD_FALLEN)
        lbl, c1, c2, a1, c3, a2, back = s17_loop()
        self.add(s.ring, s.nodes, s.spokes, s.arms, s.cargo, hub, title, el, frame, fill, lab, cut, lbl, c1, c2, a1, c3, a2, back)
        self.wait(1.9)
        self.finish()


CY = -0.3   # y of the axon in s18


def hbar(x0, y, w, level, color, h=0.45):
    frame = RoundedRectangle(corner_radius=0.1, width=w, height=h, stroke_color=GREY, stroke_width=3).move_to([x0 + w / 2, y, 0])
    ww = max(level * (w - 0.14), 0.02)
    fill = Rectangle(width=ww, height=h - 0.14, stroke_width=0, fill_color=color, fill_opacity=0.85).move_to([x0 + 0.07 + ww / 2, y, 0])
    return frame, fill


class S18Crash(SpokenScene):
    def construct(self):
        ax = tube(-6.2, 6.2, CY, 2.0)
        ys = (0.2, -0.3, -0.8)
        cut_x = (-2.0, 0.4, 2.8)
        lefts = VGroup(*[Line([-6.0, CY + d, 0], [cx, CY + d, 0], color=GREY, stroke_width=3.5) for d, cx in zip(ys, cut_x)])
        rights = VGroup(*[Line([cx, CY + d, 0], [6.0, CY + d, 0], color=GREY, stroke_width=3.5) for d, cx in zip(ys, cut_x)])
        f, fl = hbar(-5.0, 3.15, 6.0, 1.0, GREEN, 0.6)
        al = T("ATP", 36, GREEN).move_to([-5.95, 3.15, 0])
        cyl = T("cytoskeleton", 30, GREY).move_to([-0.9, -2.05, 0])
        cyl2 = leader([-0.9, -1.75, 0], [-0.9, CY - 0.8 - 0.05, 0], GREY)
        self.play(FadeIn(ax), FadeIn(lefts), FadeIn(rights), FadeIn(f), FadeIn(fl), FadeIn(al), FadeIn(cyl), FadeIn(cyl2), run_time=0.4)
        self.at("Energy", lead=0)
        self.play(Transform(fl, hbar(-5.0, 3.15, 6.0, 0.08, GREEN, 0.6)[1]), run_time=0.85)
        self.at("calcium rises")
        rng = np.random.default_rng(3)
        xs = np.linspace(-5.2, 3.1, 12)
        dots = VGroup(*[Dot([x, 1.0, 0], radius=0.14, color=YELLOW) for x in xs])
        cal = bchip("calcium", YELLOW, 30).move_to([4.9, 1.4, 0])
        tgt = [[x, rng.uniform(-0.55, 0.45), 0] for x in xs]
        self.play(FadeIn(cal), FadeIn(dots), run_time=0.2)
        self.play(*[d.animate.move_to(p) for d, p in zip(dots, tgt)], cal.animate.move_to([4.9, 0.15, 0]), run_time=0.8)
        self.at("calpings")
        cp = bchip("calpain", PURPLE, 38).move_to([4.6, -2.2, 0])
        self.play(FadeIn(cp, shift=UP * 0.2), run_time=0.4)
        self.at("proteases")
        pt = T("a protease", 30, PURPLE).move_to([4.6, -2.85, 0])
        self.play(FadeIn(pt), run_time=0.4)
        self.at("switched on")
        self.play(Flash(cp, color=YELLOW, line_length=0.3), run_time=0.5)
        sc = scissors(1.3).move_to([-2.75, CY, 0])
        self.play(cp.animate.move_to([-4.65, CY, 0]), FadeOut(pt), FadeIn(sc), run_time=0.9)
        self.at("cut the")
        for i, (d, cx) in enumerate(zip(ys, cut_x)):
            self.play(sc.animate.move_to([cx - 0.5, CY + d, 0]), run_time=0.3)
            self.play(lefts[i].animate.shift(LEFT * 0.12), rights[i].animate.shift(RIGHT * 0.12), Flash(Dot([cx, CY + d, 0]), color=PURPLE, line_length=0.25, flash_radius=0.3), run_time=0.25)
        fr = frags(-6.2, 6.2, CY, 1.9, seed=21, n=9)
        self.play(FadeOut(ax), FadeIn(fr), FadeOut(lefts), FadeOut(rights), FadeOut(cp), FadeOut(sc), FadeOut(cyl), FadeOut(cyl2), run_time=0.8)
        self.finish()
        self.wait(0.6)


class S19Beat(NarratedScene):
    def construct(self):
        fr = frags(-6.2, 6.2, CY, 1.9, seed=21, n=9)
        f, fl = hbar(-5.0, 3.15, 6.0, 0.08, GREEN, 0.6)
        al = T("ATP", 36, GREEN).move_to([-5.95, 3.15, 0])
        cal = bchip("calcium", YELLOW, 30).move_to([4.9, 0.15, 0])
        rng = np.random.default_rng(3)
        xs = np.linspace(-5.2, 3.1, 12)
        dots = VGroup(*[Dot([x, rng.uniform(-0.55, 0.45), 0], radius=0.14, color=YELLOW) for x in xs])
        self.add(fr, f, fl, al, cal, dots)
        self.wait(1.9)
        self.finish()


class S20Geneq(SpokenScene):
    def construct(self):
        title, heads, r1, r2 = table_frame()
        cells = row1_cells()
        cap = table_caption()
        self.play(FadeIn(title), FadeIn(heads), FadeIn(r1), FadeIn(cap), run_time=0.6)
        self.play(FadeIn(cells[0]), run_time=0.4)
        self.at("die around")
        self.play(FadeIn(cells[1], shift=UP * 0.1), run_time=0.4)
        self.at("growing")
        self.play(FadeIn(cells[2], shift=UP * 0.1), run_time=0.5)
        self.at("Remove")
        lab = row2_label()
        self.play(FadeIn(r2), FadeIn(lab), run_time=0.6)
        self.at("What happens")
        q1 = qmark(84).move_to([TC[1], R2Y, 0])
        q2 = qmark(84).move_to([TC[2], R2Y, 0])
        pl, pbg, ring = pause_tag(4.8, 3.4)
        self.play(FadeIn(q1, scale=0.6), FadeIn(q2, scale=0.6), FadeIn(pl), FadeIn(pbg), run_time=0.5)
        self.finish()


class S21Pause(NarratedScene):
    def construct(self):
        title, heads, r1, r2 = table_frame()
        cells = row1_cells()
        lab = row2_label()
        q1 = qmark(84).move_to([TC[1], R2Y, 0])
        q2 = qmark(84).move_to([TC[2], R2Y, 0])
        pl, pbg, ring = pause_tag(4.8, 3.4)
        self.add(title, heads, r1, r2, *cells, lab, q1, q2, table_caption(), pl, pbg)
        self.play(Create(ring, run_time=4.5, rate_func=linear))
        self.finish()


class S22Generev(SpokenScene):
    def construct(self):
        title, heads, r1, r2 = table_frame()
        cells = row1_cells()
        lab = row2_label()
        q1 = qmark(84).move_to([TC[1], R2Y, 0])
        q2 = qmark(84).move_to([TC[2], R2Y, 0])
        cap = table_caption()
        self.add(title, heads, r1, r2, *cells, lab, q1, q2, cap)
        self.at("axons grow")
        g = T("axons grow", 36, GREEN).move_to([TC[2], R2Y, 0])
        self.play(FadeOut(q2, run_time=0.2))
        self.play(FadeIn(g, shift=UP * 0.1), run_time=0.4)
        self.at("mice survive")
        s = T("mice survive", 36, GREEN).move_to([TC[1], R2Y, 0])
        self.play(FadeOut(q1, run_time=0.2))
        self.play(FadeIn(s, shift=UP * 0.1), run_time=0.4)
        self.at("Losing")
        ca = bchip("NMNAT2 lost", TEAL, 36).move_to([-4.2, -3.2, 0])
        self.play(FadeOut(cap), FadeIn(ca), run_time=0.5)
        self.at("works by")
        cs = bchip("SARM1", RED, 36).move_to([4.2, -3.2, 0])
        ar = arr([-2.2, -3.2, 0], [3.1, -3.2, 0], GREY, 7, 0.28)
        aw = T("acts through SARM1", 28, TEXT).move_to([0.45, -2.65, 0])
        self.play(GrowArrow(ar), FadeIn(aw), run_time=0.6)
        self.at("tripping")
        self.play(FadeIn(cs, scale=0.8), run_time=0.5)
        self.finish()
        self.wait(1.4)


class S23Apop(SpokenScene):
    def construct(self):
        lab = T("Not apoptosis", 56, TEXT, font=TITLE_FONT).move_to([0, 3.2, 0])
        st, lines = stump_shape(-0.9)
        cm = cutmark(-3.65, -0.9, 3.2)
        sl = T("the stump", 30, BLUE).move_to([1.4, -2.7, 0])
        self.play(FadeIn(lab, shift=DOWN * 0.15), FadeIn(st), FadeIn(lines), FadeIn(cm), FadeIn(sl), run_time=0.6)
        self.at("caspases")
        cs = VGroup(*[bchip("caspase", RED, 32).move_to([x, 1.7, 0]) for x in (-4.4, -1.5, 1.4, 4.3)])
        self.play(FadeIn(cs, shift=DOWN * 0.15), run_time=0.6)
        self.at("are blocked")
        xs = VGroup(*[Cross(c, stroke_color=RED, stroke_width=7).scale(1.0) for c in cs])
        self.play(Create(xs), run_time=0.5)
        self.play(FadeOut(st), FadeOut(lines), FadeIn(frags(-3.4, 6.2, -0.9, 2.6, seed=31, n=8)), run_time=0.9)
        self.finish()
        self.wait(1.2)


def switch(on):
    col = RED if on else GREY
    pill = RoundedRectangle(corner_radius=0.55, width=2.4, height=1.1, stroke_color=col, stroke_width=6, fill_color=col, fill_opacity=0.3)
    knob = Circle(radius=0.42, stroke_color=TEXT, stroke_width=3, fill_color=TEXT, fill_opacity=0.9)
    knob.move_to(pill.get_right() + LEFT * 0.55 if on else pill.get_left() + RIGHT * 0.55)
    return VGroup(pill, knob)


class S24Take(SpokenScene):
    def construct(self):
        y = -0.7
        soma = VGroup(Circle(radius=0.7, stroke_color=BLUE, stroke_width=4, fill_color=BG, fill_opacity=1),
                      Circle(radius=0.7, stroke_width=0, fill_color=BLUE, fill_opacity=0.3),
                      Circle(radius=0.25, stroke_color=GREY, stroke_width=2.5, fill_color=GREY, fill_opacity=0.35)).move_to([-6.0, y, 0])
        prox = tube(-6.0, -3.9, y, 0.8)
        st, lines = stump_shape(y)
        self.play(FadeIn(prox), FadeIn(st), FadeIn(lines), FadeIn(soma), run_time=0.5)
        stv = bchip("starving", GREY, 46).move_to([0, 2.0, 0])
        self.at("cut off piece")
        cm = cutmark(-3.65, y, 3.0)
        self.play(prox.animate.shift(LEFT * 0.1), st.animate.shift(RIGHT * 0.1), lines.animate.shift(RIGHT * 0.1), FadeIn(cm), FadeIn(stv), run_time=0.5)
        self.at("not simply", lead=0)
        xx = strike(stv)
        self.play(Create(xx), run_time=0.5)
        self.at("switch")
        sw = switch(False).move_to([1.7, y, 0])
        self.play(FadeIn(sw, scale=0.7), run_time=0.45)
        self.at("waits")
        lbl = T("waits", 42, TEXT).move_to([1.7, 1.1, 0])
        self.play(FadeIn(lbl), run_time=0.3)
        self.at("deliveries")
        ps = VGroup(*[parcel(x, yy).scale(1.3) for x, yy in ((-2.6, y + 0.3), (-2.6, y - 0.3), (-1.2, y), (4.4, y + 0.3), (4.4, y - 0.3))])
        self.play(FadeIn(ps), run_time=0.3)
        self.at("stop")
        self.play(FadeOut(ps), Transform(sw, switch(True).move_to([1.7, y, 0])), FadeOut(lbl), run_time=0.5)
        self.finish()


class S25End(EndCard):
    LINE = "The cut-off piece carries a switch\nthat waits for deliveries to stop."

    def construct(self):
        l1 = T("The cut-off piece carries a switch", 42, font=TITLE_FONT)
        l2 = T("that waits for deliveries to stop.", 42, font=TITLE_FONT)
        line = VGroup(l1, l2).arrange(DOWN, buff=0.5, center=True)
        fit(line, max_w=11.8)
        sub = T("biochemistrypedia.com", size=24, color=TEAL)
        g = VGroup(line, sub).arrange(DOWN, buff=0.6).move_to(ORIGIN)
        self.play(FadeIn(line, shift=UP * 0.15), run_time=self.beat(0.3))
        self.play(FadeIn(sub), run_time=self.beat(0.15))
        self.finish()
