"""Take the Machinery Away  (Biochemistrypedia explainer, chapter 6 of 6, "The Death Machinery in Neurons").
Timed to the SPOKEN words: every self.at("...") waits for that phrase in audio/words.json.

COLOR MAP (one colour per concept, shared with the other chapters; taken from scenes.old.py)
  BLUE   = the neuron / a living cell / axons
  YELLOW = NGF, the survival signal, and the brakes it applies
  TEAL   = new gene expression (and "no new protein")
  ORANGE = Bax (the pro-death BCL-2 family protein)
  PINK   = cytochrome c
  PURPLE = Apaf-1 / the apoptosome (not used in this chapter)
  RED    = the killers (caspases), death, "deleted / crossed out"
  GREEN  = survives; neurons saved from death by deleting Bax (the "extra" neurons and axons)
  GREY   = outlines, mitochondrion, timelines, plain labels, dead or inactive things, the mouse
  GOLD   = the "eat me" tag (not used in this chapter)
  WHITE  = (as in chapter 4) the gate bar and the brake badges
"""
import numpy as np
from bp_style import *  # noqa: F401,F403

PURPLE = "#B58CD9"
ORANGE = "#F29E4C"
PINK = "#F28CB1"
WHITE = TEXT
MOUSE = "#6B7385"


# ---------------------------------------------------------------------------------------------
# small helpers
# ---------------------------------------------------------------------------------------------
def bchip(text, color=BLUE, size=26, **kw):
    c = chip(text, color, size=size, **kw)
    back = RoundedRectangle(corner_radius=0.14, width=c[0].width, height=c[0].height, stroke_width=0,
                            fill_color=BG, fill_opacity=1).move_to(c[0])
    return VGroup(back, *c)


def dimchip(c, o=0.35):
    return [c[1].animate.set_stroke(opacity=o).set_fill(opacity=0.16 * o), c[2].animate.set_opacity(o)]


def undim(c, color):
    return [c[1].animate.set_stroke(color, opacity=1).set_fill(color, 0.16), c[2].animate.set_color(color).set_opacity(1)]


def litchip(c, color, fill=0.38):
    return [c[1].animate.set_stroke(color, opacity=1).set_fill(color, fill), c[2].animate.set_color(color).set_opacity(1)]


def dimmed(c, o=0.35):
    """a chip already dimmed (for rebuilding a held state)"""
    c[1].set_stroke(opacity=o).set_fill(opacity=0.16 * o)
    c[2].set_opacity(o)
    return c


def arr(a, b, color=GREY, w=5, tip=0.22):
    return Arrow(a, b, buff=0.08, color=color, stroke_width=w, tip_length=tip,
                 max_tip_length_to_length_ratio=0.45, max_stroke_width_to_length_ratio=12)


def inhib(a, b, color=RED, w=5):
    a, b = np.array(a, float), np.array(b, float)
    d = (b - a) / np.linalg.norm(b - a)
    b = b - d * 0.08
    perp = np.array([-d[1], d[0], 0])
    return VGroup(Line(a, b, color=color, stroke_width=w),
                  Line(b + perp * 0.26, b - perp * 0.26, color=color, stroke_width=w + 1))


def xmark(center, s=0.22, color=RED, w=6):
    c = np.array(center, float)
    return VGroup(Line(c + [-s, -s, 0], c + [s, s, 0], color=color, stroke_width=w),
                  Line(c + [-s, s, 0], c + [s, -s, 0], color=color, stroke_width=w))


def kbadge(c, color=RED, r=0.21):
    """a red 'deleted' badge on the upper-right corner of a chip: the words stay readable"""
    p = c.get_corner(UR)
    disc = Circle(radius=r, stroke_color=BG, stroke_width=2, fill_color=color, fill_opacity=1).move_to(p)
    s = r * 0.45
    x = VGroup(Line(p + [-s, -s, 0], p + [s, s, 0], color=WHITE, stroke_width=4),
               Line(p + [-s, s, 0], p + [s, -s, 0], color=WHITE, stroke_width=4))
    return VGroup(disc, x)


def nrn(r=0.3, color=BLUE, fill=0.35):
    """a neuron as a cell body with a nucleus (small, for crowds)"""
    c = Circle(radius=r, stroke_color=color, stroke_width=3, fill_color=color, fill_opacity=fill)
    n = Dot(radius=r * 0.34, color=color)
    g = VGroup(c, n)
    g.c, g.n = c, n
    return g


def pack(cx, cy, w, h, n, r, seed, gap=1.08):
    """n non-overlapping circle centres of radius r inside an ellipse w x h (deterministic)"""
    rs = np.random.RandomState(seed)
    pts, tries = [], 0
    while len(pts) < n and tries < 60000:
        tries += 1
        x = (rs.rand() * 2 - 1) * (w / 2 - r)
        y = (rs.rand() * 2 - 1) * (h / 2 - r)
        if (x / (w / 2 - r)) ** 2 + (y / (h / 2 - r)) ** 2 > 1:
            continue
        if all((x - a) ** 2 + (y - b) ** 2 >= (2 * r * gap) ** 2 for a, b in pts):
            pts.append((x, y))
    assert len(pts) == n, (len(pts), n)
    return [np.array([cx + x, cy + y, 0.0]) for x, y in pts]


def ganglion(cx, cy, w, h, n, r, seed, color=BLUE):
    shell = Ellipse(width=w, height=h, stroke_color=GREY, stroke_width=3.5, fill_color=GREY, fill_opacity=0.08).move_to([cx, cy, 0])
    cells = [nrn(r, color).move_to(p) for p in pack(cx, cy, w, h, n, r, seed)]
    g = VGroup(shell, *cells)
    g.shell, g.cells = shell, cells
    return g


def vbar(x, base_y, w, color, h0):
    tr = ValueTracker(h0)
    bar = always_redraw(lambda: Rectangle(width=w, height=max(tr.get_value(), 0.02), stroke_color=color, stroke_width=2,
                                          fill_color=color, fill_opacity=0.85).move_to([x, base_y, 0], aligned_edge=DOWN))
    return tr, bar


def mouse(scale=1.0, center=(0, 0, 0)):
    """a mouse silhouette in side view, facing right (one body colour, so no seams)"""
    body = Ellipse(width=3.0, height=1.8, stroke_width=0, fill_color=MOUSE, fill_opacity=1)
    head = Ellipse(width=1.5, height=1.2, stroke_width=0, fill_color=MOUSE, fill_opacity=1).move_to([1.6, -0.1, 0])
    ear = Circle(radius=0.38, stroke_width=0, fill_color=MOUSE, fill_opacity=1).move_to([1.3, 0.62, 0])
    ear_in = Circle(radius=0.2, stroke_width=0, fill_color="#868EA3", fill_opacity=1).move_to([1.3, 0.66, 0])
    nose = Dot([2.32, -0.1, 0], radius=0.09, color="#C9CED8")
    eye = Dot([1.95, 0.12, 0], radius=0.07, color=BG)
    tail = ParametricFunction(lambda t: np.array([-1.4 - 1.7 * t, -0.15 + 0.85 * np.sin(t * 2.6), 0]),
                              t_range=[0, 1, 0.02], color=MOUSE, stroke_width=8)
    f1 = Ellipse(width=0.55, height=0.28, stroke_width=0, fill_color=MOUSE, fill_opacity=1).move_to([-0.8, -0.95, 0])
    f2 = Ellipse(width=0.55, height=0.28, stroke_width=0, fill_color=MOUSE, fill_opacity=1).move_to([0.8, -0.95, 0])
    g = VGroup(tail, f1, f2, body, head, ear, ear_in, nose, eye)
    g.scale(scale).move_to(np.array(center, float))
    return g


def chromosome(center, w=5.6):
    c = np.array(center, float)
    bar = RoundedRectangle(corner_radius=0.25, width=w, height=0.5, stroke_color=GREY, stroke_width=3,
                           fill_color=GREY, fill_opacity=0.25).move_to(c)
    g3 = Rectangle(width=0.8, height=0.95, stroke_color=RED, stroke_width=3, fill_color=BG, fill_opacity=1).move_to(c + [-w * 0.2, 0, 0])
    g3f = Rectangle(width=0.8, height=0.95, stroke_color=RED, stroke_width=3, fill_color=RED, fill_opacity=0.25).move_to(g3)
    g9 = Rectangle(width=0.8, height=0.95, stroke_color=RED, stroke_width=3, fill_color=BG, fill_opacity=1).move_to(c + [w * 0.2, 0, 0])
    g9f = Rectangle(width=0.8, height=0.95, stroke_color=RED, stroke_width=3, fill_color=RED, fill_opacity=0.25).move_to(g9)
    l3 = T("caspase-3", 26, RED).move_to(c + [-w * 0.2, -0.85, 0])
    l9 = T("caspase-9", 26, RED).move_to(c + [w * 0.2, -0.85, 0])
    cl = T("chromosome", 26, GREY).move_to(c + [0, -1.55, 0])
    g = VGroup(bar, g3, g3f, g9, g9f, l3, l9, cl)
    g.g3, g.g9 = g3, g9
    return g


PATH = [("NGF loss", YELLOW), ("Bax", ORANGE), ("cytochrome c", PINK), ("caspase-9", RED), ("caspase-3", RED), ("neuron dies", GREY)]
PATH_X = 4.9
PATH_Y = [3.0, 1.85, 0.7, -0.45, -1.6, -2.75]


def pathway():
    chips = [bchip(t, c, 26).move_to([PATH_X, y, 0]) for (t, c), y in zip(PATH, PATH_Y)]
    arrs = [arr(chips[i].get_bottom(), chips[i + 1].get_top(), GREY, 4, 0.18) for i in range(len(chips) - 1)]
    return chips, arrs


def cell_apop(R=2.4, c=(0, 0, 0)):
    """apoptotic neuron: dense (pyknotic) nucleus (same outer size as the other cell: no size claim)"""
    c = np.array(c, float)
    outer = Circle(radius=R, stroke_color=BLUE, stroke_width=4, fill_color=BLUE, fill_opacity=0.18).move_to(c)
    nuc = Circle(radius=R * 0.24, stroke_color=TEXT, stroke_width=2, fill_color=BLUE, fill_opacity=1).move_to(c)
    return VGroup(outer, nuc)


def cell_vac(R=2.4, c=(0, 0, 0)):
    """caspase-null neuron: nucleus not condensed, cytoplasm full of vacuoles"""
    c = np.array(c, float)
    outer = Circle(radius=R, stroke_color=BLUE, stroke_width=4, fill_color=BLUE, fill_opacity=0.18).move_to(c)
    nuc = Circle(radius=R * 0.45, stroke_color=BLUE, stroke_width=2, fill_color=BLUE, fill_opacity=0.3).move_to(c)
    vac = [Circle(radius=R * 0.15, stroke_color=GREY, stroke_width=2.5, fill_color=BG, fill_opacity=1)
           .move_to(c + R * 0.74 * np.array([np.cos(np.radians(a)), np.sin(np.radians(a)), 0])) for a in range(15, 375, 60)]
    g = VGroup(outer, nuc, *vac)
    g.vac = vac
    return g


def tile(x, y, w=3.0, h=4.8, rows=6, cols=4, r=0.25):
    box = RoundedRectangle(corner_radius=0.2, width=w, height=h, stroke_color=GREY, stroke_width=3, fill_color=GREY, fill_opacity=0.08).move_to([x, y, 0])
    cells = []
    for i in range(rows):
        for j in range(cols):
            cells.append(nrn(r, BLUE).move_to([x + (j - (cols - 1) / 2) * 0.66, y + ((rows - 1) / 2 - i) * 0.72, 0]))
    g = VGroup(box, *cells)
    g.box, g.cells = box, cells
    return g


# =============================================================================================
class S00Title(TitleCard):
    LESSON = "The Death Machinery in Neurons"
    TITLE = "Take the Machinery Away"


# ---------------------------------------------------------------------------------------------
MOUSE_BIG = 1.5
MOUSE_BIG_C = [-1.7, 0.1, 0]
DISH_C = [-1.7, 0.4, 0]


def dish(center, R=2.4):
    c = np.array(center, float)
    ring = Circle(radius=R, stroke_color=GREY, stroke_width=4, fill_color=GREY, fill_opacity=0.08).move_to(c)
    cells = [nrn(0.4, BLUE).move_to(c + [x, y, 0]) for x, y in [(-1.0, 0.95), (0.8, 1.15), (-1.2, -0.5), (0.2, 0.05), (1.3, -0.7), (-0.1, -1.4)]]
    lab = T("neurons in culture", 28, GREY).move_to(c + [0, -R - 0.5, 0])
    return VGroup(ring, *cells, lab)


class S01(SpokenScene):
    """culture shows the pathway; now a whole animal"""

    def construct(self):
        chips, arrs = pathway()
        m = mouse(MOUSE_BIG, MOUSE_BIG_C)
        d = dish(DISH_C)
        self.at("culture shows")
        steps = [FadeIn(chips[0], shift=DOWN * 0.15)]
        for i in range(1, len(chips)):
            steps.append(AnimationGroup(GrowArrow(arrs[i - 1]), FadeIn(chips[i], shift=DOWN * 0.15)))
        self.play(FadeIn(d, scale=0.9), LaggedStart(*steps, lag_ratio=0.4), run_time=2.3)
        self.at("whole animal")
        self.play(FadeOut(d), FadeIn(m, shift=RIGHT * 0.3), run_time=0.9)
        self.at("delete its parts")
        self.play(LaggedStart(*[Indicate(c[2], color=TEXT, scale_factor=1.15) for c in chips], lag_ratio=0.3), run_time=1.6)
        self.finish()


# ---------------------------------------------------------------------------------------------
CH_C = [-3.4, -0.5, 0]
MOUSE_S2_C = [-3.4, 2.1, 0]
MOUSE_S2_SCALE = 1.2


def cluster():
    cl = VGroup(*[nrn(0.4, BLUE).move_to([3.5 + dx, y, 0]) for y in (1.9, 0.8) for dx in (-1.05, 0, 1.05)])
    lab = T("spinal and\nperipheral neurons\nthat normally die", 26, TEXT, line_spacing=0.9).move_to([3.5, -1.0, 0])
    q = T("?", 110, TEXT, weight=BOLD).move_to([3.5, -2.9, 0])
    return cl, lab, q


class S02(SpokenScene):
    """a knockout mouse: caspase-3 or caspase-9 crossed out; do the neurons that normally die survive?"""

    def construct(self):
        chips, arrs = pathway()
        m = mouse(MOUSE_BIG, MOUSE_BIG_C)
        self.add(*chips, *arrs, m)
        ch = chromosome(CH_C, w=5.8).scale(1.1, about_point=np.array(CH_C))
        cl, lab, q = cluster()
        self.play(*[FadeOut(o) for o in [*chips, *arrs]],
                  m.animate.scale(MOUSE_S2_SCALE / MOUSE_BIG).move_to(MOUSE_S2_C), FadeIn(ch),
                  LaggedStart(*[FadeIn(n, scale=0.6) for n in cl], lag_ratio=0.1), run_time=0.7)
        x3g = xmark(ch.g3.get_center(), 0.34, RED, 7)
        x9g = xmark(ch.g9.get_center(), 0.34, RED, 7)
        self.at("caspase 3")
        self.play(Create(x3g), run_time=0.5)
        self.at("or caspase 9")
        self.play(FadeOut(x3g), Create(x9g), run_time=0.6)
        self.at("do the spinal")
        self.play(Indicate(cl, color=BLUE, scale_factor=1.08), run_time=0.8)
        self.at("normally die")
        self.play(FadeIn(lab), run_time=0.5)
        self.at("survive")
        self.play(FadeIn(q, scale=0.6), run_time=0.5)
        self.finish()


class S03Pause(NarratedScene):
    """silent pause: the question stays on screen, still"""

    def construct(self):
        m = mouse(MOUSE_S2_SCALE, MOUSE_S2_C)
        ch = chromosome(CH_C, w=5.8).scale(1.1, about_point=np.array(CH_C))
        x9g = xmark(ch.g9.get_center(), 0.34, RED, 7)
        cl, lab, q = cluster()
        self.add(m, ch, x9g, cl, lab, q)
        self.finish()


# ---------------------------------------------------------------------------------------------
def bar_chart_parts():
    base, H = -2.3, 4.6
    axis = Line([-4.6, base, 0], [6.0, base, 0], color=GREY, stroke_width=4)
    yax = Line([-4.6, base, 0], [-4.6, base + H + 0.2, 0], color=GREY, stroke_width=4)
    ylab = T("neurons that died", 30, TEXT).rotate(PI / 2).move_to([-5.45, base + H / 2, 0])
    n1 = T("normal mouse", 28, TEXT).move_to([-1.4, base - 0.5, 0])
    n2 = T("caspase-null mouse", 28, TEXT).move_to([3.4, base - 0.5, 0])
    return base, H, axis, yax, ylab, n1, n2


class S04(SpokenScene):
    """equal bars: the same number died"""

    def construct(self):
        base, H, axis, yax, ylab, n1, n2 = bar_chart_parts()
        no = T("No.", 64, RED, weight=BOLD).move_to([0.7, 3.25, 0])
        t1, b1 = vbar(-1.4, base, 2.3, RED, 0.02)
        t2, b2 = vbar(3.4, base, 2.3, RED, 0.02)
        eq = T("=", 90, TEXT, weight=BOLD).move_to([1.0, base + H * 0.5, 0])
        tag = T("counted by Oppenheim and colleagues", 28, TEXT).move_to([0.7, -3.5, 0])
        self.add(b1, b2)
        self.play(FadeIn(no, scale=0.7), Create(axis), Create(yax), FadeIn(ylab), FadeIn(n1), FadeIn(n2), run_time=0.9)
        self.at("oppenheim's group")
        self.play(FadeIn(tag, shift=UP * 0.1), run_time=0.5)
        self.at("counted them")
        self.play(t1.animate.set_value(H), run_time=0.7)
        self.play(t2.animate.set_value(H), run_time=0.7)
        self.at("the same number")
        self.play(FadeIn(eq, scale=0.6), run_time=0.5)
        self.at("in normal mice")
        self.play(Indicate(n1, color=TEXT, scale_factor=1.1), run_time=0.7)
        self.finish()


# ---------------------------------------------------------------------------------------------
class S05(SpokenScene):
    """timeline: the caspase-null deaths come later, and do not look apoptotic"""

    def construct(self):
        y1, y2 = 2.2, -0.5
        x1, x2 = -1.2, 3.8
        a1 = Arrow([-6.3, y1, 0], [6.5, y1, 0], buff=0, color=GREY, stroke_width=4, tip_length=0.25)
        a2 = Arrow([-6.3, y2, 0], [6.5, y2, 0], buff=0, color=GREY, stroke_width=4, tip_length=0.25)
        l1 = T("normal mouse", 32, TEXT).move_to([-6.3, y1 + 0.65, 0], aligned_edge=LEFT)
        l2 = T("caspase-null mouse", 32, TEXT).move_to([-6.3, y2 + 0.65, 0], aligned_edge=LEFT)
        ag1 = T("age", 26, GREY).move_to([6.1, y1 - 0.45, 0])
        ag2 = T("age", 26, GREY).move_to([6.1, y2 - 0.45, 0])

        def marker(x, y):
            return VGroup(Dot([x, y, 0], radius=0.2, color=RED), T("deaths", 26, RED).move_to([x, y - 0.55, 0]))

        m1, m2 = marker(x1, y1), marker(x1, y2)
        guide = DashedLine([x1, y1 - 0.9, 0], [x1, y2 + 0.4, 0], color=GREY, stroke_width=3)
        self.play(Create(a1), Create(a2), FadeIn(l1), FadeIn(l2), FadeIn(ag1), FadeIn(ag2), FadeIn(m1), FadeIn(m2), run_time=0.6)
        self.at("came later")
        brk = Arrow([x1, y2 + 0.7, 0], [x2, y2 + 0.7, 0], buff=0, color=TEXT, stroke_width=4, tip_length=0.22)
        later = T("later", 38, TEXT, weight=BOLD).move_to([(x1 + x2) / 2, y2 + 1.2, 0])
        self.play(Create(guide), m2.animate.shift(RIGHT * (x2 - x1)), GrowArrow(brk), FadeIn(later), run_time=1.1)
        self.at("did not look")
        tag = bchip("not apoptotic", TEXT, 38).move_to([x2, -2.95, 0])
        lead = Line([x2, y2 - 0.95, 0], tag.get_top(), color=GREY, stroke_width=3)
        self.play(Create(lead), FadeIn(tag, shift=UP * 0.15), run_time=0.7)
        self.finish()


# ---------------------------------------------------------------------------------------------
LX, RX, CY = -3.5, 3.5, 0.25
CR = 2.4


class S06(SpokenScene):
    """side by side: pyknotic apoptotic neuron, and a caspase-null neuron full of vacuoles"""

    def construct(self):
        big = Circle(radius=CR * 0.5, stroke_color=BLUE, stroke_width=2, fill_color=BLUE, fill_opacity=0.3).move_to([LX, CY, 0])
        left = cell_apop(CR, [LX, CY, 0])
        nuc_dense = left[1]
        left.remove(nuc_dense)
        hl = T("apoptotic neuron", 32, TEXT).move_to([LX, 3.35, 0])
        ll = T("chromatin condensed", 26, TEXT).move_to([LX, -2.7, 0])
        right = cell_vac(CR, [RX, CY, 0])
        vac = right.vac
        for v in vac:
            right.remove(v)
        hr = T("caspase-null neuron", 32, TEXT).move_to([RX, 3.35, 0])
        lr = T("condensation absent or reduced", 26, TEXT).move_to([RX, -2.7, 0])
        lv = T("cytoplasm full of vacuoles", 26, TEXT).move_to([RX, -3.3, 0])
        self.play(FadeIn(left), FadeIn(big), FadeIn(hl), run_time=0.8)
        self.play(Transform(big, nuc_dense), FadeIn(ll), run_time=0.8)
        self.at("absent or reduced")
        self.play(FadeIn(right), FadeIn(hr), FadeIn(lr), run_time=0.9)
        self.at("cytoplasm")
        self.play(LaggedStart(*[FadeIn(v, scale=0.4) for v in vac], lag_ratio=0.2), run_time=1.3)
        self.at("vacuoles")
        self.play(FadeIn(lv), run_time=0.5)
        self.finish()


class S07(SpokenScene):
    """so deleting a caspase changes how these neurons die: caspases decide how"""

    def construct(self):
        left = cell_apop(CR, [LX, CY, 0])
        right = cell_vac(CR, [RX, CY, 0])
        hl = T("apoptotic neuron", 32, TEXT).move_to([LX, 3.35, 0])
        hr = T("caspase-null neuron", 32, TEXT).move_to([RX, 3.35, 0])
        ll = T("chromatin condensed", 26, TEXT).move_to([LX, -2.7, 0])
        lr = T("condensation absent or reduced", 26, TEXT).move_to([RX, -2.7, 0])
        lv = T("cytoplasm full of vacuoles", 26, TEXT).move_to([RX, -3.3, 0])
        self.add(left, right, hl, hr, ll, lr, lv)
        S = 0.74
        self.play(FadeOut(VGroup(hl, hr, ll, lr, lv)), left.animate.scale(S).move_to([LX, -0.1, 0]),
                  right.animate.scale(S).move_to([RX, -0.1, 0]), run_time=0.4)
        cl = bchip("caspase", RED, 34).move_to([LX, 2.9, 0])
        cr = bchip("caspase", RED, 34).move_to([RX, 2.9, 0])
        al = arr(cl.get_bottom(), [LX, 1.85, 0], RED)
        ar = arr(cr.get_bottom(), [RX, 1.85, 0], RED).set_opacity(0.45)
        br = kbadge(cr)
        lab = T("caspases decide how", 46, TEXT, weight=BOLD).move_to([0, -2.9, 0])
        self.at("deleting a caspase")
        self.play(FadeIn(cl, shift=DOWN * 0.2), GrowArrow(al), FadeIn(cr, shift=DOWN * 0.2), GrowArrow(ar), run_time=0.5)
        self.at("changes how")
        self.play(FadeIn(br, scale=0.5), *dimchip(cr, 0.4), run_time=0.4)
        self.at("these neurons die")
        self.play(FadeIn(lab, shift=UP * 0.15), run_time=0.5)
        self.finish()


# ---------------------------------------------------------------------------------------------
G8 = dict(cy=0.4, w=5.8, h=4.3, n=22, r=0.32, seed=3)
G8_X = (-3.6, 3.6)
GHOST = [0, 3, 5, 8, 11, 14, 17, 20]


class S08(SpokenScene):
    """delete Bax: normal ganglion loses neurons; the Bax-null ganglion stays crowded; rescued populations"""

    def construct(self):
        gl = ganglion(G8_X[0], color=BLUE, **G8)
        gr = ganglion(G8_X[1], color=BLUE, **G8)
        for i in GHOST:
            gr.cells[i].set_color(GREEN)
        hl = T("normal mouse", 32, TEXT).move_to([G8_X[0], 3.45, 0])
        hr = T("Bax-null mouse", 32, TEXT).move_to([G8_X[1], 3.45, 0])
        sl = T("naturally occurring death", 28, RED).move_to([G8_X[0], 2.95, 0])
        sr = T("largely eliminated", 28, GREEN).move_to([G8_X[1], 2.95, 0])
        b = bchip("Bax", ORANGE, 36).move_to([0, 0.4, 0])
        bb = kbadge(b)
        pt = T("rescued populations include", 26, GREY).move_to([0, -2.25, 0])
        r1 = VGroup(*[T(t, 28, TEXT) for t in ["sympathetic neurons", "sensory neurons"]]).arrange(RIGHT, buff=1.0).move_to([0, -2.8, 0])
        r2 = VGroup(*[T(t, 28, TEXT) for t in ["facial motor neurons", "retinal ganglion cells"]]).arrange(RIGHT, buff=1.0).move_to([0, -3.4, 0])
        row = VGroup(*r1, *r2)
        self.play(FadeIn(hl), FadeIn(gl.shell), LaggedStart(*[FadeIn(c, scale=0.5) for c in gl.cells], lag_ratio=0.01), run_time=0.3)
        self.at("now delete")
        self.play(FadeIn(b, shift=DOWN * 0.2), run_time=0.5)
        self.at("instead")
        self.play(FadeIn(bb, scale=0.5), *dimchip(b, 0.45), run_time=0.4)
        self.play(LaggedStart(*[AnimationGroup(gl.cells[i].animate.set_color(GREY).set_opacity(0.3)) for i in GHOST], lag_ratio=0.1), run_time=0.9)
        self.at("in many neuron")
        self.play(FadeIn(hr), FadeIn(gr.shell), LaggedStart(*[FadeIn(c, scale=0.5) for c in gr.cells], lag_ratio=0.02), run_time=0.8)
        self.at("populations")
        self.play(FadeIn(pt), LaggedStart(*[FadeIn(t, shift=UP * 0.12) for t in row], lag_ratio=0.2), run_time=1.0)
        self.at("naturally occurring death")
        self.play(FadeIn(sl, shift=UP * 0.1), run_time=0.5)
        self.at("largely eliminated")
        self.play(FadeIn(sr, shift=UP * 0.1), run_time=0.5)
        self.finish()


# ---------------------------------------------------------------------------------------------
TILE_X = [-5.025, -1.675, 1.675, 5.025]
TILE_Y = 0.1
POPS = ["sympathetic\nneurons", "sensory\nneurons", "facial motor\nneurons", "some other\npopulations"]


class S09(SpokenScene):
    """caveat: not every population; in Bax-dependent populations deleting Bax stops the death"""

    def construct(self):
        b = bchip("Bax", ORANGE, 30).move_to([-5.7, 3.3, 0])
        bb = kbadge(b)
        dimmed(b, 0.45)
        self.add(b, bb)
        tiles = [tile(xx, TILE_Y) for xx in TILE_X]
        labs = [T(p, 26, TEXT, line_spacing=0.9).move_to([xx, -3.05, 0]) for p, xx in zip(POPS, TILE_X)]
        lab4 = T("not rescued", 28, RED).move_to([TILE_X[3], 3.3, 0])
        leg = VGroup(nrn(0.16, GREY, 0.35), T("= died", 26, TEXT)).arrange(RIGHT, buff=0.15).move_to([2.7, 3.3, 0])
        self.add(lab4, leg)
        self.at("bax deletion")
        self.play(LaggedStart(*[AnimationGroup(FadeIn(t), FadeIn(l)) for t, l in zip(tiles, labs)], lag_ratio=0.2), run_time=1.2)
        self.at("not rescue every")
        t4 = tiles[3]
        self.play(*[t4.cells[i].animate.set_color(GREY) for i in (0, 2, 3, 5, 7, 8, 10, 12, 13, 15, 17, 18, 20, 22, 23)], run_time=0.8)
        self.at("where neurons depend")
        dep = T("in Bax-dependent populations", 28, GREEN).move_to([-4.4, 3.3, 0], aligned_edge=LEFT)
        self.play(FadeIn(dep), *[t.box.animate.set_stroke(GREEN) for t in tiles[:3]], run_time=0.8)
        self.at("deleting it stops")
        self.play(*[c.animate.set_color(GREEN) for t in tiles[:3] for c in t.cells], run_time=0.9)
        self.at("the death")
        self.play(Indicate(VGroup(*tiles[:3]), color=GREEN, scale_factor=1.03), run_time=0.7)
        self.finish()


# ---------------------------------------------------------------------------------------------
class S10(SpokenScene):
    """caspases decide how; Bax decides whether (in Bax-dependent populations)"""

    def construct(self):
        top = T("in Bax-dependent populations", 28, GREEN).move_to([0, 3.4, 0])
        y1, y2 = 1.4, -1.9
        c1 = bchip("caspases", RED, 34).move_to([-4.7, y1, 0])
        i1a = cell_apop(0.95, [-0.7, y1, 0])
        i1b = cell_vac(0.95, [2.0, y1, 0])
        a1 = arr(c1.get_right(), [-1.75, y1, 0], RED)
        w1 = T("how", 58, TEXT, weight=BOLD).move_to([5.2, y1, 0])
        c2 = bchip("Bax", ORANGE, 34).move_to([-4.7, y2, 0])
        i2a = nrn(0.8, GREEN).move_to([-0.7, y2, 0])
        i2b = nrn(0.8, GREY).move_to([2.0, y2, 0])
        x2 = xmark([2.0, y2, 0], 0.62, RED, 7)
        a2 = arr(c2.get_right(), [-1.75, y2, 0], ORANGE)
        w2 = T("whether", 58, TEXT, weight=BOLD).move_to([5.2, y2, 0])
        sep = Line([-6.2, -0.25, 0], [6.2, -0.25, 0], color=GREY, stroke_width=2).set_opacity(0.5)
        self.add(top, c1, a1, i1a, i1b, w1)
        self.at("decide how")
        self.play(Indicate(w1, color=TEXT, scale_factor=1.08), run_time=0.5)
        self.at("decides whether")
        self.play(Create(sep), FadeIn(c2, shift=RIGHT * 0.2), GrowArrow(a2), FadeIn(i2a), FadeIn(i2b), run_time=0.8)
        self.play(Create(x2), FadeIn(w2, scale=0.8), run_time=0.4)
        self.finish()


# ---------------------------------------------------------------------------------------------
class S11(SpokenScene):
    """close-up of the surplus neurons: the saved neurons were not normal"""

    def construct(self):
        g = ganglion(0.0, 0.1, 9.6, 5.0, 16, 0.55, 7)
        saved = [1, 4, 6, 9, 13]
        rings = VGroup(*[DashedVMobject(Circle(radius=0.7, stroke_color=GREEN, stroke_width=4).move_to(g.cells[i]), num_dashes=16)
                         for i in saved])
        hdr = T("Bax-null mouse", 32, TEXT).move_to([-4.2, 3.3, 0])
        lab = VGroup(DashedVMobject(Circle(radius=0.2, stroke_color=GREEN, stroke_width=4), num_dashes=10),
                     T("saved neurons", 32, GREEN)).arrange(RIGHT, buff=0.2).move_to([3.2, 3.3, 0])
        nn = T("not normal", 52, TEXT, weight=BOLD).move_to([0, -3.15, 0])
        self.add(g, hdr)
        self.play(*[FadeIn(c, scale=0.7) for c in g.cells], run_time=0.3)
        self.at("saved neurons")
        self.play(Create(rings), FadeIn(lab), *[g.cells[i].animate.set_color(GREEN) for i in saved], run_time=0.7)
        self.at("not normal")
        self.play(FadeIn(nn, shift=UP * 0.15), run_time=0.5)
        self.finish()


# ---------------------------------------------------------------------------------------------
SEC_X = [-4.6, 0.0, 4.6]
SEC_Y = 0.3
SEC_R = 2.05
SEC_NAMES = ["dorsal root", "ventral root", "facial nerve"]
SEC_EXTRA = [4, 7, 7]


def section(cx, cy, n_extra, seed):
    s = SEC_R / 1.55
    shell = Circle(radius=SEC_R, stroke_color=GREY, stroke_width=4, fill_color=GREY, fill_opacity=0.08).move_to([cx, cy, 0])
    base_pts = [np.array([0.0, 0.0])]
    base_pts += [0.63 * s * np.array([np.cos(np.radians(a)), np.sin(np.radians(a))]) for a in range(0, 360, 60)]
    base_pts += [1.18 * s * np.array([np.cos(np.radians(a)), np.sin(np.radians(a))]) for a in range(30, 390, 60)]
    rb, re_ = 0.27 * s, 0.12 * s
    base = [Circle(radius=rb, stroke_color=BLUE, stroke_width=3, fill_color=BLUE, fill_opacity=0.45).move_to([cx + p[0], cy + p[1], 0])
            for p in base_pts]
    rs = np.random.RandomState(seed)
    ex_pts, tries = [], 0
    while len(ex_pts) < n_extra and tries < 50000:
        tries += 1
        ang, rad = rs.rand() * TAU, np.sqrt(rs.rand()) * (SEC_R - re_ - 0.1)
        p = rad * np.array([np.cos(ang), np.sin(ang)])
        if min(np.linalg.norm(p - q) for q in base_pts) < rb + re_ + 0.05:
            continue
        if any(np.linalg.norm(p - q) < 2 * re_ + 0.08 for q in ex_pts):
            continue
        ex_pts.append(p)
    assert len(ex_pts) == n_extra, (len(ex_pts), n_extra)
    extra = [Circle(radius=re_, stroke_color=GREEN, stroke_width=3, fill_color=GREEN, fill_opacity=0.6).move_to([cx + p[0], cy + p[1], 0]) for p in ex_pts]
    return shell, base, extra


class S12(SpokenScene):
    """three nerve cross-sections: more myelinated axons, many very small"""

    def construct(self):
        secs = [section(x, SEC_Y, n, 11 + i) for i, (x, n) in enumerate(zip(SEC_X, SEC_EXTRA))]
        names = [T(n, 30, TEXT).move_to([x, SEC_Y + SEC_R + 0.5, 0]) for n, x in zip(SEC_NAMES, SEC_X)]
        pct = T("about 30 to 55 percent more", 38, GREEN, weight=BOLD).move_to([0, -2.45, 0])
        leg1 = VGroup(Circle(radius=0.17, stroke_color=BLUE, stroke_width=3, fill_color=BLUE, fill_opacity=0.45),
                      T("normal-mouse axons", 26, TEXT)).arrange(RIGHT, buff=0.2)
        leg2 = VGroup(Circle(radius=0.1, stroke_color=GREEN, stroke_width=3, fill_color=GREEN, fill_opacity=0.6),
                      T("extra axons, many very small", 26, GREEN)).arrange(RIGHT, buff=0.2)
        VGroup(leg1, leg2).arrange(RIGHT, buff=0.9).move_to([0, -3.3, 0])
        self.play(*[FadeIn(secs[i][0], scale=0.8) for i in (0, 1)], run_time=0.5)
        self.at("spinal nerve roots")
        self.play(FadeIn(names[0]), FadeIn(names[1]), run_time=0.4)
        self.at("facial nerve")
        self.play(FadeIn(secs[2][0], scale=0.8), FadeIn(names[2]), run_time=0.6)
        self.at("myelinated axon")
        self.play(*[LaggedStart(*[GrowFromCenter(a) for a in s[1]], lag_ratio=0.06) for s in secs], FadeIn(leg1), run_time=1.3)
        self.at("rose by about")
        self.play(*[LaggedStart(*[GrowFromCenter(a) for a in s[2]], lag_ratio=0.1) for s in secs], FadeIn(leg2), run_time=1.0)
        self.at("30 to 55 percent")
        self.play(FadeIn(pct, shift=UP * 0.15), run_time=0.8)
        self.at("many extra axons")
        self.play(*[Indicate(VGroup(*s[2]), color=GREEN, scale_factor=1.25) for s in secs], run_time=1.0)
        self.at("very small")
        self.play(Indicate(leg2, color=GREEN, scale_factor=1.06), run_time=0.8)
        self.finish()


# ---------------------------------------------------------------------------------------------
MN_Y = [2.5, 1.5, 0.5, -0.5, -1.5, -2.5]
MN_COL = [BLUE, GREEN, BLUE, GREEN, BLUE, GREEN]
MUSCLE_L = 3.5


class S13(SpokenScene):
    """motor axons reach a muscle; then some neurons shrink and their axons pull away"""

    def construct(self):
        hdr = T("Bax-null mouse. Green: extra neurons.", 30, TEXT).move_to([0, 3.5, 0])
        cord = RoundedRectangle(corner_radius=0.3, width=2.0, height=6.3, stroke_color=GREY, stroke_width=3,
                                fill_color=GREY, fill_opacity=0.1).move_to([-5.7, -0.15, 0])
        clab = T("spinal cord", 26, GREY).move_to([-5.7, -3.6, 0])
        mus = RoundedRectangle(corner_radius=0.3, width=3.0, height=6.3, stroke_color=GREY, stroke_width=3,
                               fill_color=GREY, fill_opacity=0.12).move_to([5.0, -0.15, 0])
        fibers = VGroup(*[Line([3.75, y, 0], [6.25, y, 0], color=GREY, stroke_width=2).set_opacity(0.5) for y in MN_Y])
        mlab = T("muscle", 26, GREY).move_to([5.0, -3.6, 0])
        neurons = [nrn(0.38, c, 0.4).move_to([-5.7, y, 0]) for c, y in zip(MN_COL, MN_Y)]
        trs = [ValueTracker(-5.3) for _ in MN_Y]
        axons = [always_redraw(lambda t=t, y=y, c=c: VGroup(
            Line([-5.3, y, 0], [t.get_value(), y, 0], color=c, stroke_width=5),
            Dot([t.get_value(), y, 0], radius=0.1, color=c))) for t, y, c in zip(trs, MN_Y, MN_COL)]
        lost = VGroup(T("lost contact", 28, RED).move_to([1.2, -0.5, 0]), T("lost contact", 28, RED).move_to([1.2, -2.5, 0]))
        self.add(cord, clab, mus, fibers, mlab, *axons)
        self.play(FadeIn(hdr), run_time=0.5)
        self.at("motor neurons")
        self.play(*[FadeIn(n, scale=0.5) for n in neurons], run_time=0.8)
        self.at("innervate their targets")
        self.play(*[t.animate.set_value(MUSCLE_L) for t in trs], run_time=1.6)
        self.at("then a subset")
        self.play(Indicate(VGroup(neurons[3], neurons[5]), color=TEXT, scale_factor=1.2), run_time=0.6)
        self.at("shrank")
        self.play(neurons[3].animate.scale(0.55), neurons[5].animate.scale(0.55), run_time=0.6)
        self.at("lost contact")
        self.play(trs[3].animate.set_value(-1.0), trs[5].animate.set_value(-1.0), run_time=1.0)
        self.play(FadeIn(lost), run_time=0.5)
        self.finish()


# ---------------------------------------------------------------------------------------------
class S14(SpokenScene):
    """alive, but small; limited target support?"""

    def construct(self):
        NC = [-3.1, 0.5, 0]
        ghost = DashedVMobject(Circle(radius=2.3, stroke_color=GREY, stroke_width=3), num_dashes=36).move_to(NC)
        n = nrn(2.3, GREEN, 0.3).move_to(NC)
        l1 = T("saved from death", 34, GREEN).move_to([-3.1, -2.5, 0])
        l2 = T("alive, but small", 34, GREEN).move_to([-3.1, -2.5, 0])
        tgt = RoundedRectangle(corner_radius=0.3, width=3.0, height=4.4, stroke_color=GREY, stroke_width=3,
                               fill_color=GREY, fill_opacity=0.12).move_to([4.5, 0.5, 0])
        tl = T("target", 28, GREY).move_to([4.5, 2.2, 0])
        dots = VGroup(Dot([3.8, 0.9, 0], radius=0.14, color=WHITE), Dot([3.8, -0.1, 0], radius=0.14, color=WHITE))
        dl = T("target support", 26, WHITE).move_to([4.5, -0.85, 0])
        thin = DashedLine([3.0, 0.5, 0], [-0.3, 0.5, 0], color=GREY, stroke_width=3)
        lim = T("too little target support?", 32, TEXT).move_to([2.9, -2.9, 0])
        self.play(FadeIn(ghost), FadeIn(n), FadeIn(tgt), FadeIn(tl), run_time=0.6)
        self.at("saved from death")
        self.play(FadeIn(l1, shift=UP * 0.15), run_time=0.5)
        self.at("smaller cell")
        self.play(n.animate.scale(0.5), FadeOut(l1, run_time=0.4), Succession(Wait(0.5), FadeIn(l2)), run_time=1.0)
        self.at("that fits")
        self.play(Indicate(tgt, color=GREY, scale_factor=1.03), run_time=0.6)
        self.at("too little")
        self.play(Create(thin), FadeIn(dots), FadeIn(dl), FadeIn(lim), run_time=0.8)
        self.finish()


# ---------------------------------------------------------------------------------------------
G15 = dict(cx=1.9, cy=-0.15, w=7.6, h=5.4, n=24, r=0.36, seed=5)
MOUSE_C = [-5.1, 2.4, 0]


def ko_chips():
    ngf = bchip("NGF", YELLOW, 30).move_to([-5.1, -0.5, 0])
    bax = bchip("Bax", ORANGE, 30).move_to([-5.1, -1.9, 0])
    return ngf, bax


class S15(SpokenScene):
    """NGF-null mouse: the sympathetic ganglion empties"""

    def construct(self):
        m = mouse(0.6, MOUSE_C)
        ngf, _ = ko_chips()
        nb = kbadge(ngf)
        g = ganglion(**G15)
        gl = T("sympathetic ganglion", 28, GREY).move_to([1.9, 3.15, 0])
        nolab = T("no sympathetic neurons left", 32, TEXT, weight=BOLD).move_to([1.9, 0.6, 0])
        qchip = bchip("what else does\nNGF do for them?", YELLOW, 34).move_to([1.9, -0.9, 0])
        qb = kbadge(qchip)
        self.play(FadeIn(m), FadeIn(ngf), FadeIn(g.shell), FadeIn(gl), LaggedStart(*[FadeIn(c, scale=0.5) for c in g.cells], lag_ratio=0.03), run_time=0.7)
        self.play(FadeIn(nb, scale=0.5), *dimchip(ngf, 0.45), run_time=0.3)
        self.at("lose their sympathetic")
        self.play(LaggedStart(*[AnimationGroup(c.animate.set_color(GREY).scale(0.6)) for c in g.cells], lag_ratio=0.03), run_time=0.8)
        self.play(*[FadeOut(c) for c in g.cells], FadeIn(nolab, shift=UP * 0.1), run_time=0.5)
        self.at("so you cannot")
        self.play(Indicate(g.shell, color=TEXT, scale_factor=1.02), run_time=0.6)
        self.at("what else")
        self.play(FadeIn(qchip, scale=0.8), run_time=0.6)
        self.at("does for them")
        self.play(FadeIn(qb, scale=0.5), run_time=0.5)
        self.finish()


class S16(SpokenScene):
    """NGF and Bax both deleted: the ganglion stays full"""

    def construct(self):
        m = mouse(0.6, MOUSE_C)
        ngf, bax = ko_chips()
        nb = kbadge(ngf)
        dimmed(ngf, 0.45)
        bb = kbadge(bax)
        g = ganglion(color=GREEN, **G15)
        gl = T("sympathetic ganglion", 28, GREY).move_to([1.9, 3.15, 0])
        self.add(m, ngf, nb, g.shell, gl)
        self.at("mice lacking both")
        self.play(FadeIn(bax, shift=DOWN * 0.15), run_time=0.5)
        self.play(FadeIn(bb, scale=0.5), *dimchip(bax, 0.45), run_time=0.4)
        self.at("the sympathetic neurons")
        self.play(LaggedStart(*[FadeIn(c, scale=0.5) for c in g.cells], lag_ratio=0.05), run_time=1.3)
        self.at("survive")
        sv = T("survive", 42, GREEN, weight=BOLD).move_to([1.9, -3.4, 0])
        self.play(FadeIn(sv, shift=UP * 0.15), run_time=0.5)
        self.finish()


# ---------------------------------------------------------------------------------------------
ORG_NAMES = ["salivary gland", "heart", "stomach", "kidney", "trachea"]
ORG_Y = [2.6, 1.3, 0.0, -1.3, -2.6]
ORG_X = 4.3
ORG_L = ORG_X - 1.7
GAN_C = np.array([-4.5, 0.3, 0.0])
GAN_S = 0.55
GAN_R = GAN_C[0] + G15["w"] * GAN_S / 2 + 0.1
ORG_LEVEL = [(0, 0.0, "none or almost none"), (1, 0.18, "greatly reduced"), (3, 0.35, "somewhat reduced"),
             (3, 0.35, "somewhat reduced"), (5, 0.55, "normal")]
FULL_FILL = 0.55


def org_boxes(fill=0.0):
    out = []
    for name, y in zip(ORG_NAMES, ORG_Y):
        box = RoundedRectangle(corner_radius=0.15, width=3.4, height=1.1, stroke_color=GREY, stroke_width=3,
                               fill_color=BLUE, fill_opacity=fill).move_to([ORG_X, y, 0])
        lab = T(name, 26, TEXT).move_to(box)
        dash = DashedVMobject(RoundedRectangle(corner_radius=0.15, width=3.4, height=1.1, stroke_color=GREY, stroke_width=3).move_to(box), num_dashes=44)
        dash.set_opacity(0)
        out.append(VGroup(box, lab, dash))
    return out


def strands(i, count, color=BLUE, w=3.5):
    y = ORG_Y[i]
    if count == 0:
        return VGroup()
    g = VGroup()
    for k in range(count):
        off = (k - (count - 1) / 2) * 0.17
        g.add(Line([GAN_R, GAN_C[1] + off * 0.5, 0], [ORG_L, y + off, 0], color=color, stroke_width=w))
    return g


def dashed_lines():
    return [DashedLine([GAN_R, GAN_C[1], 0], [ORG_L, y, 0], color=GREY, stroke_width=3) for y in ORG_Y]


def left_group():
    g = ganglion(color=GREEN, **G15).scale(GAN_S).move_to(GAN_C)
    lab = T("NGF and Bax deleted", 26, TEXT).move_to([GAN_C[0], -1.5, 0])
    return g, lab


def s16_state(scene):
    """the held end of s16: the big full ganglion with both crossed-out causes"""
    m = mouse(0.6, MOUSE_C)
    ngf, bax = ko_chips()
    dimmed(ngf, 0.45)
    dimmed(bax, 0.45)
    nb, bb = kbadge(ngf), kbadge(bax)
    g = ganglion(color=GREEN, **G15)
    gl = T("sympathetic ganglion", 28, GREY).move_to([1.9, 3.15, 0])
    sv = T("survive", 42, GREEN, weight=BOLD).move_to([1.9, -3.4, 0])
    scene.add(m, ngf, bax, nb, bb, g, gl, sv)
    return m, ngf, bax, nb, bb, g, gl, sv


class S17(SpokenScene):
    """question over the organ map: what would innervation look like?"""

    def construct(self):
        m, ngf, bax, nb, bb, g, gl, sv = s16_state(self)
        lab = T("NGF and Bax deleted", 26, TEXT).move_to([GAN_C[0], -1.5, 0])
        boxes = org_boxes()
        dl = dashed_lines()
        q = T("?", 120, TEXT, weight=BOLD).move_to([-0.1, 2.2, 0])
        self.at("did nothing")
        self.play(FadeOut(VGroup(m, ngf, bax, nb, bb, gl, sv)),
                  g.animate.scale(GAN_S).move_to(GAN_C), FadeIn(lab),
                  LaggedStart(*[FadeIn(b, shift=LEFT * 0.2) for b in boxes], lag_ratio=0.2), run_time=1.4)
        self.at("keep neurons")
        self.play(Indicate(VGroup(*g.cells), color=GREEN, scale_factor=1.15), run_time=1.0)
        self.at("their innervation")
        self.play(*[Create(d) for d in dl], run_time=0.8)
        self.at("look like")
        self.play(FadeIn(q, scale=0.6), run_time=0.6)
        self.finish()


class S18Pause(NarratedScene):
    """silent pause: the question stays on screen, still"""

    def construct(self):
        g, lab = left_group()
        boxes = org_boxes()
        dl = dashed_lines()
        q = T("?", 120, TEXT, weight=BOLD).move_to([-0.1, 2.2, 0])
        self.add(g, lab, *boxes, *dl, q)
        self.finish()


# ---------------------------------------------------------------------------------------------
class S19(SpokenScene):
    """expected: like Bax-null mice. It did not."""

    def construct(self):
        g, lab = left_group()
        boxes = org_boxes()
        dl = dashed_lines()
        q = T("?", 120, TEXT, weight=BOLD).move_to([-0.1, 2.2, 0])
        self.add(g, lab, *boxes, *dl, q)
        full = [strands(i, 5) for i in range(5)]
        exp = T("expected: as in mice lacking only Bax", 28, TEXT).move_to([-1.0, 3.5, 0])
        bot = T("compared with Bax-null mice,\nembryos and newborns", 26, TEXT, line_spacing=0.9).move_to([GAN_C[0], -2.75, 0])
        self.at("it would look like")
        self.play(FadeOut(q), *[FadeOut(d) for d in dl], FadeIn(exp), FadeIn(bot), run_time=0.5)
        self.play(*[Create(f) for f in full], *[b[0].animate.set_fill(BLUE, FULL_FILL) for b in boxes], run_time=0.9)
        self.at("lacking only")
        self.play(Indicate(exp, color=ORANGE, scale_factor=1.05), run_time=0.7)
        self.at("it did not")
        xm = xmark(exp.get_left() + [-0.35, 0, 0], 0.2, RED, 6)
        self.play(FadeIn(xm, scale=0.5), exp.animate.set_opacity(0.55), *[f.animate.set_opacity(0.25) for f in full],
                  *[b[0].animate.set_fill(BLUE, 0.1) for b in boxes], run_time=0.8)
        self.finish()


def legend_col():
    rows = []
    for fill, txt in [(None, "absent"), (0.18, "greatly reduced"), (0.35, "somewhat reduced"), (FULL_FILL, "normal")]:
        if fill is None:
            sw = DashedVMobject(Square(side_length=0.3, stroke_color=GREY, stroke_width=3), num_dashes=12)
        else:
            sw = Square(side_length=0.3, stroke_color=GREY, stroke_width=3, fill_color=BLUE, fill_opacity=fill)
        rows.append(VGroup(sw, T(txt, 24, TEXT)).arrange(RIGHT, buff=0.18))
    g = VGroup(*rows).arrange(DOWN, aligned_edge=LEFT, buff=0.14).move_to([-6.6, -2.85, 0], aligned_edge=LEFT)
    return g


def set_levels(boxes):
    """organ boxes and strands in their NGF/Bax double-null state; returns the strands"""
    out = []
    for i, (n, f, _t) in enumerate(ORG_LEVEL):
        boxes[i][0].set_fill(BLUE, f)
        out.append(strands(i, n))
    boxes[0][0].set_stroke(opacity=0)
    boxes[0][2].set_opacity(1)
    return out


class S20(SpokenScene):
    """organ map coloured by innervation: it differs by organ"""

    def construct(self):
        g, lab = left_group()
        boxes = org_boxes(0.1)
        full = [strands(i, 5).set_opacity(0.25) for i in range(5)]
        bot = T("compared with Bax-null mice,\nembryos and newborns", 26, TEXT, line_spacing=0.9).move_to([GAN_C[0], -2.75, 0])
        self.add(g, lab, *boxes, *full, bot)
        lv = [strands(i, n) for i, (n, f, _t) in enumerate(ORG_LEVEL)]
        self.at("axons failed")
        self.play(Indicate(g, color=GREEN, scale_factor=1.03), run_time=0.7)
        self.at("fully innervate many targets")
        anims = []
        for i, (n, f, _t) in enumerate(ORG_LEVEL):
            a = [FadeOut(full[i]), FadeIn(lv[i]), boxes[i][0].animate.set_fill(BLUE, f)]
            if i == 0:
                a += [boxes[0][0].animate.set_stroke(opacity=0), boxes[0][2].animate.set_opacity(1)]
            anims.append(AnimationGroup(*a))
        self.play(LaggedStart(*anims, lag_ratio=0.35), run_time=2.0)
        self.at("differed by organ")
        leg = legend_col()
        self.play(FadeOut(bot), FadeIn(leg), run_time=0.7)
        self.finish()


class S21(SpokenScene):
    """salivary glands none, heart greatly reduced, trachea normal"""

    def construct(self):
        g, lab = left_group()
        boxes = org_boxes()
        lv = set_levels(boxes)
        leg = legend_col()
        self.add(g, lab, *boxes, *lv, leg)

        def tag(i):
            b = boxes[i]
            t = T(ORG_LEVEL[i][2], 24, TEXT).move_to([ORG_X, ORG_Y[i] - 0.24, 0])
            return t, [b[1].animate.move_to([ORG_X, ORG_Y[i] + 0.2, 0])]

        self.at("salivary glands")
        self.play(boxes[0][2].animate.set_stroke(TEXT, width=4), run_time=0.4)
        t0, m0 = tag(0)
        self.at("almost none")
        self.play(*m0, FadeIn(t0), run_time=0.5)
        self.at("heart was greatly")
        t1, m1 = tag(1)
        self.play(boxes[0][2].animate.set_stroke(GREY, width=3),
                  boxes[1][0].animate.set_stroke(TEXT, width=4), run_time=0.4)
        self.at("greatly reduced")
        self.play(*m1, FadeIn(t1), run_time=0.5)
        self.at("trachea")
        t4, m4 = tag(4)
        self.play(boxes[1][0].animate.set_stroke(GREY, width=3),
                  boxes[4][0].animate.set_stroke(TEXT, width=4), run_time=0.4)
        self.at("was normal")
        self.play(*m4, FadeIn(t4), run_time=0.5)
        t2, m2 = tag(2)
        t3, m3 = tag(3)
        self.play(boxes[4][0].animate.set_stroke(GREY, width=3), *m2, *m3, FadeIn(t2), FadeIn(t3), run_time=0.7)
        self.finish()


# ---------------------------------------------------------------------------------------------
class S22(SpokenScene):
    """NGF: growing into targets, then survival (in the order spoken)"""

    def construct(self):
        ngf = bchip("NGF", YELLOW, 46).move_to([0.0, 3.0, 0])
        # growth panel (left): spoken first
        gn = nrn(1.0, GREEN, 0.35).move_to([-5.0, -0.7, 0])
        tg = [RoundedRectangle(corner_radius=0.15, width=1.6, height=0.9, stroke_color=GREY, stroke_width=3,
                               fill_color=GREY, fill_opacity=0.12).move_to([-1.0, y, 0]) for y in (0.7, -0.7, -2.1)]
        tl = T("targets", 26, GREY).move_to([-1.0, 1.55, 0])
        ax = VGroup(*[Line([-4.0, -0.7 + 0.12 * k, 0], [-1.85, y, 0], color=BLUE, stroke_width=4) for k, y in zip((-1, 0, 1), (-2.1, -0.7, 0.7))])
        gl = T("axons grow into targets", 32, TEXT).move_to([-3.0, -3.3, 0])
        ga = arr(ngf.get_bottom() + [-0.5, 0, 0], [-4.6, 0.55, 0], YELLOW)
        # survival panel (right): spoken second
        sn = nrn(1.0, GREEN, 0.35).move_to([4.4, -0.5, 0])
        sl = T("survival", 42, GREEN, weight=BOLD).move_to([4.4, -2.7, 0])
        sa = arr(ngf.get_bottom() + [0.5, 0, 0], [4.2, 0.65, 0], YELLOW)
        growth = T("growth", 28, YELLOW).move_to([-3.1, 2.0, 0])
        survival = T("survival", 28, YELLOW).move_to([3.2, 2.0, 0])
        self.at("NGF is needed")
        self.play(FadeIn(ngf, scale=0.8), run_time=0.6)
        self.at("axons to grow")
        self.play(GrowArrow(ga), FadeIn(growth), FadeIn(gn), run_time=0.6)
        self.at("into many targets")
        self.play(FadeIn(VGroup(*tg)), FadeIn(tl), Create(ax), run_time=1.0)
        self.play(FadeIn(gl, shift=UP * 0.1), run_time=0.5)
        self.at("as well as")
        self.play(GrowArrow(sa), FadeIn(survival), FadeIn(sn), run_time=0.6)
        self.at("for survival")
        self.play(FadeIn(sl, shift=UP * 0.1), run_time=0.5)
        self.finish()


# ---------------------------------------------------------------------------------------------
class S23(SpokenScene):
    """the general logic: delete the machinery, then see what is still wrong"""

    def construct(self):
        names = [("Bax", ORANGE), ("cytochrome c", PINK), ("caspase-9", RED), ("caspase-3", RED)]
        chips = [bchip(t, c, 36) for t, c in names]
        row = VGroup(*chips).arrange(RIGHT, buff=0.62).move_to([0, 0.6, 0])
        ars = [arr(chips[i].get_right(), chips[i + 1].get_left(), GREY, 4, 0.18) for i in range(3)]
        bs = [kbadge(c) for c in chips]
        chain = VGroup(*chips, *ars)
        n = nrn(1.8, GREEN, 0.35).move_to([0, -1.0, 0])
        wrong = bchip("what is still\nwrong?", TEXT, 36).move_to([4.9, -1.0, 0])
        dying = bchip("dying", GREY, 34).move_to([-4.9, -1.0, 0])
        db = kbadge(dying)
        a_w = arr(n.get_right() + [0.15, 0, 0], wrong.get_left(), TEXT)
        self.play(FadeIn(chain, shift=DOWN * 0.1), run_time=0.6)
        self.at("delete the death machinery")
        self.play(LaggedStart(*[FadeIn(b, scale=0.4) for b in bs], lag_ratio=0.2),
                  *[a for c in chips for a in dimchip(c, 0.4)], *[a.animate.set_opacity(0.3) for a in ars], run_time=1.0)
        self.at("look at what")
        full = VGroup(chain, *bs)
        self.play(full.animate.scale(0.7).move_to([0, 3.15, 0]), FadeIn(n, scale=0.7), run_time=0.8)
        self.at("still wrong")
        self.play(GrowArrow(a_w), FadeIn(wrong, shift=LEFT * 0.2), run_time=0.5)
        self.at("once dying")
        self.play(FadeIn(dying, shift=RIGHT * 0.2), run_time=0.5)
        self.at("no longer an option")
        self.play(FadeIn(db, scale=0.5), *dimchip(dying, 0.45), run_time=0.5)
        self.finish()


class S24(SpokenScene):
    """caveat: the deleted gene may have other jobs"""

    def construct(self):
        gene = bchip("deleted gene", RED, 38).move_to([-4.0, 0.2, 0])
        gb = kbadge(gene)
        j1 = bchip("cell death", GREY, 32).move_to([2.8, 2.2, 0])
        j2 = bchip("other job?", TEXT, 32).move_to([2.8, 0.2, 0])
        j3 = bchip("other job?", TEXT, 32).move_to([2.8, -1.8, 0])
        a1 = arr(gene.get_right(), j1.get_left(), GREY)
        a2 = arr(gene.get_right(), j2.get_left(), TEXT)
        a3 = arr(gene.get_right(), j3.get_left(), TEXT)
        care = T("read such results with care", 46, TEXT, weight=BOLD).move_to([0, -3.15, 0])
        self.at("deleted gene")
        self.play(FadeIn(gene, shift=RIGHT * 0.2), FadeIn(gb, scale=0.5), run_time=0.7)
        self.at("other jobs")
        self.play(FadeIn(j2), FadeIn(j3), FadeIn(j1), run_time=0.4)
        self.play(GrowArrow(a2), GrowArrow(a3), GrowArrow(a1), run_time=0.6)
        self.at("read such results")
        self.play(FadeIn(care, shift=UP * 0.15), run_time=0.6)
        self.finish()


# ---------------------------------------------------------------------------------------------
# the closing summary: four short lines on the left, the two brakes drawn on the right.
# Both brakes are dashed previews from line 1; the gate and first brake solidify with
# badge 1 on line 2, and the caspase brake solidifies with badge 2 on line 3.
# ---------------------------------------------------------------------------------------------
def sum_lines():
    items = [T("Killers already built.\nNGF keeps brakes on them.", 28, TEXT, line_spacing=0.9),
             T("Brake 1: the gate at the\nmitochondrion, opened by\nnew gene expression.", 28, TEXT, line_spacing=0.9),
             T("Brake 2: on the caspases,\nlifted without new protein.", 28, TEXT, line_spacing=0.9),
             T("Both brakes off:\nthe neuron dies by apoptosis.", 28, TEXT, line_spacing=0.9)]
    VGroup(*items).arrange(DOWN, aligned_edge=LEFT, buff=0.5).move_to([-6.6, 0.0, 0], aligned_edge=LEFT)
    return items


def badge(txt, pos):
    c = Circle(radius=0.3, stroke_color=WHITE, stroke_width=3, fill_color=WHITE, fill_opacity=1).move_to(pos)
    return VGroup(c, T(txt, 28, BG, weight=BOLD).move_to(pos))


def sum_pic():
    d = {}
    d["ngf"] = bchip("NGF", YELLOW, 30).move_to([3.8, 3.1, 0])
    d["casp"] = bchip("caspases", RED, 30).move_to([3.4, -1.0, 0])
    d["apop"] = bchip("apoptosis", GREY, 30).move_to([3.4, -3.0, 0])
    d["a_end"] = arr(d["casp"].get_bottom(), d["apop"].get_top(), GREY)
    body = RoundedRectangle(corner_radius=0.5, width=2.8, height=1.3, stroke_color=GREY, stroke_width=4,
                            fill_color=GREY, fill_opacity=0.15).move_to([2.4, 0.85, 0])
    d["mito"] = VGroup(body, T("mitochondrion", 24, GREY).move_to([2.4, 0.7, 0]))
    d["gL"] = Line([1.7, 1.5, 0], [2.4, 1.5, 0], color=WHITE, stroke_width=11)
    d["gR"] = Line([2.4, 1.5, 0], [3.1, 1.5, 0], color=WHITE, stroke_width=11)
    d["lineA"] = inhib([3.2, 2.7, 0], [2.75, 1.62, 0], YELLOW)       # brake one: NGF holds the gate shut
    d["lineB"] = inhib([4.5, 2.7, 0], [4.3, -0.6, 0], YELLOW)        # brake two: NGF holds the caspases
    d["a_mito"] = arr([2.4, 0.2, 0], [2.4, -0.6, 0], GREY, 4, 0.18)
    d["b1"] = badge("1", [3.7, 2.15, 0])
    d["b2"] = badge("2", [5.1, 1.0, 0])
    d["gene"] = T("new gene\nexpression", 26, TEAL, line_spacing=0.85).move_to([-0.3, 2.45, 0])
    d["gene_a"] = arr([0.65, 2.1, 0], [1.7, 1.6, 0], TEAL, 5, 0.2)
    d["noprot"] = T("no new protein", 24, TEAL).move_to([5.65, 0.1, 0])
    d["ghostA"] = VGroup(*[DashedVMobject(part.copy(), num_dashes=8) for part in d["lineA"]]).set_opacity(0.45)
    d["ghostB"] = VGroup(*[DashedVMobject(part.copy(), num_dashes=14) for part in d["lineB"]]).set_opacity(0.45)
    d["ghostGate"] = VGroup(*[DashedVMobject(d[k].copy(), num_dashes=5) for k in ("gL", "gR")]).set_opacity(0.45)
    return d


def dim_ngf(c, o=0.4):
    return [c[1].animate.set_stroke(opacity=o).set_fill(opacity=0.06), c[2].animate.set_opacity(o)]


def base_diagram(scene, d):
    """the diagram as it stands at the end of s25"""
    scene.add(d["casp"], d["apop"], d["a_end"], d["mito"], d["a_mito"], d["gL"], d["gR"], d["ngf"], d["lineA"], d["lineB"])


class S25(SpokenScene):
    """line 1: the killers are built; a survival signal keeps brakes on them"""

    def construct(self):
        items = sum_lines()
        d = sum_pic()
        self.add(items[0], d["casp"], d["apop"], d["a_end"], d["mito"], d["a_mito"],
                 d["ngf"], d["ghostA"], d["ghostB"], d["ghostGate"])
        self.at("killers are already built")
        self.play(Indicate(d["casp"][2], color=RED, scale_factor=1.12), run_time=0.6)
        self.at("a survival signal")
        self.play(Indicate(d["ngf"], color=YELLOW, scale_factor=1.1), run_time=0.6)
        self.at("keeps brakes")
        self.play(Indicate(VGroup(d["ghostA"], d["ghostB"]), color=YELLOW, scale_factor=1.05), run_time=0.6)
        self.at("on them")
        self.play(Indicate(d["casp"][2], color=RED, scale_factor=1.12), run_time=0.4)
        self.finish()


class S26(SpokenScene):
    """line 2: brake one is the gate at the mitochondrion; NGF loss opens it through new gene expression"""

    def construct(self):
        d = sum_pic()
        its = sum_lines()
        self.add(its[0])
        self.add(d["casp"], d["apop"], d["a_end"], d["mito"], d["a_mito"], d["ngf"],
                 d["ghostA"], d["ghostB"], d["ghostGate"])
        self.at("break 1")
        self.play(FadeIn(its[1], shift=RIGHT * 0.2), FadeIn(d["b1"], scale=0.6),
                  ReplacementTransform(d["ghostA"], d["lineA"]),
                  ReplacementTransform(d["ghostGate"], VGroup(d["gL"], d["gR"])), run_time=0.7)
        self.at("gate at the mitochondrion")
        self.play(Indicate(VGroup(d["gL"], d["gR"]), color=WHITE, scale_factor=1.25), Indicate(d["mito"], color=GREY, scale_factor=1.05), run_time=0.8)
        self.at("loss opens it")
        self.play(d["lineA"].animate.set_opacity(0.25), run_time=0.6)
        self.at("new gene expression")
        self.play(FadeIn(d["gene"]), GrowArrow(d["gene_a"]), run_time=0.6)
        self.play(d["gL"].animate.shift(LEFT * 0.45), d["gR"].animate.shift(RIGHT * 0.45), run_time=0.6)
        self.finish()


def s26_end(scene, d, n_items=2, b2_off=False):
    its = sum_lines()
    scene.add(*its[:n_items])
    base_diagram(scene, d)
    if not b2_off:
        scene.remove(d["lineB"])
        scene.add(d["ghostB"])
    d["gL"].shift(LEFT * 0.45)
    d["gR"].shift(RIGHT * 0.45)
    d["lineA"].set_opacity(0.25)
    scene.add(d["b1"], d["gene"], d["gene_a"])
    if b2_off:
        d["lineB"].set_opacity(0.25)
        dimmed(d["ngf"], 0.4)
        scene.add(d["b2"], d["noprot"])
    return its


class S27(SpokenScene):
    """line 3: brake two is on the caspases; deprivation lifts it without new protein"""

    def construct(self):
        d = sum_pic()
        its = s26_end(self, d)
        self.at("break 2")
        self.play(FadeIn(its[2], shift=RIGHT * 0.2), FadeIn(d["b2"], scale=0.6),
                  ReplacementTransform(d["ghostB"], d["lineB"]), run_time=0.7)
        self.at("on the cast")
        self.play(Indicate(d["lineB"], color=YELLOW, scale_factor=1.15), Indicate(d["casp"][2], color=RED, scale_factor=1.2), run_time=0.8)
        self.at("deprivation lifts it")
        self.play(d["lineB"].animate.set_opacity(0.25), *dim_ngf(d["ngf"]), run_time=0.7)
        self.at("without new protein")
        self.play(FadeIn(d["noprot"]), run_time=0.5)
        self.finish()


class S28(SpokenScene):
    """line 4: apoptosis only when both brakes are off"""

    def construct(self):
        d = sum_pic()
        its = s26_end(self, d, 3, True)
        self.at("the neuron dies")
        self.play(FadeIn(its[3], shift=RIGHT * 0.2), run_time=0.7)
        self.at("dies by apoptosis")
        self.play(*litchip(d["apop"], RED), d["a_end"].animate.set_color(RED), run_time=0.8)
        self.at("only when both")
        self.play(Indicate(d["b1"], color=WHITE, scale_factor=1.4), Indicate(d["b2"], color=WHITE, scale_factor=1.4), run_time=0.8)
        self.at("are off")
        self.play(Indicate(VGroup(d["gL"], d["gR"]), color=WHITE, scale_factor=1.3), run_time=0.6)
        self.finish()


# ---------------------------------------------------------------------------------------------
class S29(SpokenScene):
    """which neurons get enough NGF in the first place: targets, and competition (a question, not an answer)"""

    def construct(self):
        ys = [3.0, 1.8, 0.6, -0.6, -1.8, -3.0]
        NX = -5.7
        ns = [nrn(0.4, BLUE, 0.35).move_to([NX, y, 0]) for y in ys]

        def box(y):
            return RoundedRectangle(corner_radius=0.25, width=3.2, height=3.4, stroke_color=GREY, stroke_width=3,
                                    fill_color=GREY, fill_opacity=0.12).move_to([4.7, y, 0])

        tgA, tgB = box(1.9), box(-1.9)
        tlA = T("target", 26, GREY).move_to([5.45, 3.25, 0])
        tlB = T("target", 26, GREY).move_to([5.45, -3.25, 0])
        dotsA = [Dot([3.8, 2.5, 0], radius=0.15, color=YELLOW), Dot([3.8, 1.5, 0], radius=0.15, color=YELLOW)]
        dotsB = [Dot([3.8, -1.9, 0], radius=0.15, color=YELLOW)]
        nlA = T("NGF", 26, YELLOW, weight=BOLD).move_to([4.8, 2.0, 0])
        nlB = T("NGF", 26, YELLOW, weight=BOLD).move_to([4.8, -1.9, 0])
        ends = [(3.55, 2.5), (3.55, 1.5), (2.5, 0.8), (2.5, -0.8), (3.55, -1.9), (2.5, -3.0)]
        trs = [(ValueTracker(NX + 0.4), ValueTracker(y)) for y in ys]

        def mk(tx, ty, y):
            return always_redraw(lambda: VGroup(Line([NX + 0.4, y, 0], [tx.get_value(), ty.get_value(), 0], color=BLUE, stroke_width=4),
                                                Dot([tx.get_value(), ty.get_value(), 0], radius=0.11, color=BLUE)))

        axs = [mk(tx, ty, y) for (tx, ty), y in zip(trs, ys)]
        q = T("enough NGF for which neurons?", 36, TEXT, weight=BOLD).move_to([-2.0, 3.5, 0])
        self.add(*axs)
        self.at("which neurons")
        self.play(LaggedStart(*[FadeIn(n, scale=0.6) for n in ns], lag_ratio=0.12), run_time=0.8)
        self.at("get enough")
        self.play(FadeIn(tgA), FadeIn(tgB), FadeIn(tlA), FadeIn(tlB),
                  LaggedStart(*[FadeIn(d, scale=0.5) for d in dotsA + dotsB], lag_ratio=0.2), FadeIn(nlA), FadeIn(nlB), run_time=0.8)
        self.at("in the first place")
        self.play(*[tr[0].animate.set_value(e[0]) for tr, e in zip(trs, ends)],
                  *[tr[1].animate.set_value(e[1]) for tr, e in zip(trs, ends)], FadeIn(q), run_time=1.8)
        self.at("targets")
        self.play(Indicate(VGroup(tgA, tgB), color=TEXT, scale_factor=1.05), run_time=0.9)
        self.at("competition")
        # the axons that missed keep searching while the ones at a dot hold: nothing is decided on screen
        self.play(*[trs[i][0].animate.set_value(ends[i][0] + 0.45) for i in (2, 3, 5)],
                  *[trs[i][1].animate.set_value(ends[i][1] + (0.2 if i != 3 else -0.2)) for i in (2, 3, 5)],
                  Indicate(VGroup(*ns), color=TEXT, scale_factor=1.15), run_time=0.8)
        self.play(*[trs[i][0].animate.set_value(ends[i][0] - 0.1) for i in (2, 3, 5)], run_time=0.5)
        self.finish()


class S30End(EndCard):
    LINE = "The killers are already built;\na survival signal keeps brakes on them."
