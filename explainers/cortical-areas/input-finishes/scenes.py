"""Mapping the Cortex: Areas and Arealization, chapter 5: Input Finishes the Drawing  (Biochemistrypedia chaptered film)

The recurring picture is ONE mouse cortical hemisphere seen from above: front on the LEFT, back on the RIGHT,
the medial edge (midline) along the TOP, the lateral (outer) edge along the BOTTOM.
Visual grammar: DASHED borders = the sketch (the marker readout at birth, drawn in violet);
SOLID, filled areas = the ink (what input finishes), used only in the closing scene.

COLOR MAP (one color per concept, whole chapter series; same map as chapters 1 to 4)
  PURPLE = motor area
  GREEN  = somatosensory (touch) area, and its barrels
  PINK   = visual area (and visual activity, and the grafted visual tissue)
  SAND   = auditory area
  ORANGE = Emx2 (not drawn in this chapter)
  BLUE   = Pax6 (not drawn in this chapter)
  YELLOW = signalling centres / FGF8 (not drawn here); also the question marks
  TEAL   = neurons, and activity (spontaneous / sensory)
  TEXT   = thalamus and thalamic axons (the input), also retinal axons
  VIOLET = the marker stain and the sketch it reveals (the readout at birth)
  GOLD   = credits (years)
  LIGHT  = a flash of light (pale cream, kept apart from the FGF8 yellow)
  RED    = something removed / blocked / the mutation
  GREY   = the sheet, labels, de-emphasised things
  edge angle = its own hue ramp, used only in the orientation maps (hue follows the preferred edge angle)
"""
import colorsys
import numpy as np
from bp_style import *  # noqa: F401,F403

PURPLE = "#B58CD9"
ORANGE = "#F29E4C"
PINK = "#E58BB5"
SAND = "#D9B77E"
VIOLET = "#A970F5"
LIGHT = "#FFF3C4"
NEURON = TEAL
AXON = TEXT
NAMES = ("motor", "touch", "auditory", "visual")


# ---------------------------------------------------------------------------------------------
# geometry helpers (same hemisphere as chapter 1)
def catmull(pts, n=14):
    P = np.array(pts, float)
    m = len(P)
    out = []
    for i in range(m):
        p0, p1, p2, p3 = P[(i - 1) % m], P[i], P[(i + 1) % m], P[(i + 2) % m]
        for t in np.linspace(0, 1, n, endpoint=False):
            out.append(0.5 * ((2 * p1) + (-p0 + p2) * t + (2 * p0 - 5 * p1 + 4 * p2 - p3) * t ** 2
                              + (-p0 + 3 * p1 - 3 * p2 + p3) * t ** 3))
    return np.array(out)


def shape(D, s=1.0, c=(0, 0), color=GREY, fill=GREY, fo=0.0, sw=3, closed=True):
    pts = [[c[0] + s * x, c[1] + s * y, 0.0] for x, y in D]
    if closed:
        pts.append(pts[0])
    m = VMobject(stroke_color=color, stroke_width=sw, fill_color=fill, fill_opacity=fo)
    m.set_points_as_corners(pts)
    return m


def blobpts(cx, cy, rx, ry, ph=0.0, n=90):
    th = np.linspace(0, 2 * np.pi, n, endpoint=False)
    r = 1 + 0.06 * np.sin(3 * th + ph) + 0.035 * np.sin(5 * th + 2 * ph)
    return np.stack([cx + rx * r * np.cos(th), cy + ry * r * np.sin(th)], 1)


HB = [(0.0, -2.55), (1.6, -2.5), (2.9, -2.25), (3.9, -1.8), (4.55, -1.0), (4.8, 0.0), (4.7, 1.0), (4.2, 1.9),
      (3.3, 2.35), (2.5, 2.4), (1.0, 2.4), (-0.5, 2.4), (-2.0, 2.4), (-3.4, 2.3), (-4.2, 1.95), (-4.65, 1.2),
      (-4.75, 0.3), (-4.4, -0.5), (-3.7, -1.1), (-2.6, -1.75), (-1.3, -2.3)]
DH = catmull(HB, 12)

PATCH = {  # name: (cx, cy, rx, ry, color, phase)
    "motor": (-3.15, 1.1, 1.2, 0.95, PURPLE, 0.3),
    "touch": (-0.3, 0.35, 1.7, 1.3, GREEN, 1.1),
    "auditory": (1.95, -1.55, 1.15, 0.65, SAND, 2.0),
    "visual": (3.55, 0.45, 0.95, 1.3, PINK, 0.6),
}


class CMap:
    """The mouse hemisphere, scaled s and centred c; P() converts map units to scene coordinates."""

    def __init__(self, s=1.0, c=(0.0, -0.15)):
        self.s, self.c = s, c

    def P(self, x, y):
        return np.array([self.c[0] + self.s * x, self.c[1] + self.s * y, 0.0])

    def outline(self, color=GREY, fill=GREY, fo=0.16, sw=3):
        return shape(DH, self.s, self.c, color, fill, fo, sw)

    def patch(self, name, fo=0.42, sw=2.5):
        cx, cy, rx, ry, col, ph = PATCH[name]
        return shape(blobpts(cx, cy, rx, ry, ph), self.s, self.c, col, col, fo, sw)

    def patches(self, fo=0.42, sw=2.5):
        return VGroup(*[self.patch(n, fo, sw) for n in NAMES])

    def sketch(self, color=None, fo=0.09, sw=3.5, names=NAMES):
        """faint fills plus dashed outlines: the pencil sketch (one colour for all areas if color is given)."""
        fills, dashes = VGroup(), VGroup()
        for n in names:
            cx, cy, rx, ry, col, ph = PATCH[n]
            c = color or col
            pts = blobpts(cx, cy, rx, ry, ph)
            fills.add(shape(pts, self.s, self.c, c, c, fo, 0))
            dashes.add(DashedVMobject(shape(pts, self.s, self.c, c, c, 0.0, sw), num_dashes=36))
        return VGroup(fills, dashes)


A = CMap(0.88, (0.0, 0.95))    # the standard map: question or credit above, thalamus below
B = CMap(1.0, (1.6, 0.1))      # graft story: fetal donor at the left, host at the right
THAL_Y = -3.4
AX_X = (-0.7, -0.25, 0.25, 0.7)


def glow(x, y, r=0.34, dim=1.0, color=LIGHT):
    g = VGroup()
    for k, o in ((2.6, 0.08), (1.9, 0.14), (1.35, 0.25)):
        g.add(Circle(radius=r * k, stroke_width=0, fill_color=color, fill_opacity=o * dim))
    g.add(Circle(radius=r, stroke_color=color, stroke_width=3, stroke_opacity=max(0.3, dim), fill_color=color,
                 fill_opacity=0.95 * dim))
    return g.move_to([x, y, 0])


def mouse_head(s=1.0, c=(0, 0), color=GREY, whisk=True):
    cx, cy = c
    g = VGroup()
    for sx in (-1, 1):
        g.add(Circle(radius=0.34 * s, stroke_color=color, stroke_width=3, fill_color=color, fill_opacity=0.15)
              .move_to([cx + sx * 0.62 * s, cy + 0.55 * s, 0]))
    g.add(Ellipse(width=1.5 * s, height=1.2 * s, stroke_color=color, stroke_width=3, fill_color=BG, fill_opacity=1)
          .move_to([cx, cy, 0]))
    for sx in (-1, 1):
        g.add(Dot([cx + sx * 0.3 * s, cy + 0.15 * s, 0], radius=0.06 * s, color=TEXT))
    g.add(Dot([cx, cy - 0.22 * s, 0], radius=0.1 * s, color=PINK))
    if whisk:
        for sx in (-1, 1):
            for dy in (0.14, -0.02, -0.18):
                g.add(Line([cx + sx * 0.3 * s, cy - 0.28 * s, 0], [cx + sx * 1.15 * s, cy - 0.28 * s + dy * s * 1.4, 0],
                           stroke_color=color, stroke_width=2.5))
    return g


def ferret(s=1.0, c=(0, 0), right=True, color=GREY):
    """a long-bodied ferret in side view: bushy tail, four short dark legs, slender body, small head with a dark mask."""
    g = VGroup()

    def E(w, h, x, y, fill=BG, fo=1.0, sw=3, col=color):
        return Ellipse(width=w * s, height=h * s, stroke_color=col, stroke_width=sw, fill_color=fill, fill_opacity=fo).move_to(
            [x * s, y * s, 0])

    tail = VMobject(stroke_color=color, stroke_width=3, fill_color=color, fill_opacity=0.3)
    tail.set_points_smoothly([np.array([-2.2 * s, 0.3 * s, 0]), np.array([-3.0 * s, 0.4 * s, 0]), np.array([-3.9 * s, 0.55 * s, 0]),
                              np.array([-3.0 * s, 0.02 * s, 0]), np.array([-2.2 * s, -0.22 * s, 0])])
    tail.close_path()
    g.add(tail)
    for x in (-1.7, -1.1, 1.0, 1.6):
        g.add(RoundedRectangle(corner_radius=0.1 * s, width=0.36 * s, height=0.75 * s, stroke_color=color, stroke_width=3,
                               fill_color=color, fill_opacity=0.4).move_to([x * s, -0.62 * s, 0]))
    g.add(E(4.7, 1.1, 0.0, 0.0))                        # body
    g.add(E(1.7, 1.15, 2.05, 0.12))                     # head
    sn = VMobject(stroke_color=color, stroke_width=3, fill_color=BG, fill_opacity=1.0)
    sn.set_points_smoothly([np.array([2.35 * s, 0.5 * s, 0]), np.array([3.1 * s, 0.22 * s, 0]), np.array([3.65 * s, -0.02 * s, 0]),
                            np.array([3.1 * s, -0.3 * s, 0]), np.array([2.35 * s, -0.45 * s, 0])])
    sn.close_path()
    g.add(sn)                                           # a tapered snout
    g.add(E(1.1, 0.42, 2.45, 0.27, fill=color, fo=0.5, sw=0))    # the dark mask across the eyes
    g.add(Ellipse(width=0.42 * s, height=0.5 * s, stroke_color=color, stroke_width=3, fill_color=color, fill_opacity=0.5)
          .move_to([1.7 * s, 0.78 * s, 0]))             # rounded ear
    g.add(Dot([2.55 * s, 0.3 * s, 0], radius=0.1 * s, color=TEXT))
    g.add(Dot([3.62 * s, -0.02 * s, 0], radius=0.12 * s, color=TEXT))
    for dy in (0.22, -0.22):
        g.add(Line([3.3 * s, -0.05 * s, 0], [3.95 * s, (-0.05 + dy) * s, 0], stroke_color=color, stroke_width=2.5))
    if not right:
        g.flip(UP)
    return g.shift([c[0], c[1], 0])


def eye_icon(s=1.0, c=(0, 0), color=TEXT):
    cx, cy = c
    a = ArcBetweenPoints([cx - 0.6 * s, cy, 0], [cx + 0.6 * s, cy, 0], angle=-1.4, stroke_color=color, stroke_width=3.5)
    b = ArcBetweenPoints([cx - 0.6 * s, cy, 0], [cx + 0.6 * s, cy, 0], angle=1.4, stroke_color=color, stroke_width=3.5)
    return VGroup(a, b, Circle(radius=0.19 * s, stroke_color=color, stroke_width=3, fill_color=color, fill_opacity=0.9)
                  .move_to([cx, cy, 0]))


def route(pts, color=AXON, sw=4):
    """an axon drawn through waypoints, with its growth-cone dot at the end."""
    P = [np.array([x, y, 0.0]) for x, y in pts]
    line = VMobject(stroke_color=color, stroke_width=sw)
    line.set_points_smoothly(P)
    return VGroup(line, Dot(P[-1], radius=0.09, color=color))


def axon(p0, p1, color=AXON, sw=4, bend=0.0):
    p0 = np.array([p0[0], p0[1], 0.0])
    p1 = np.array([p1[0], p1[1], 0.0])
    dy = p1[1] - p0[1]
    c1 = p0 + np.array([bend, dy * 0.5, 0])
    c2 = p1 - np.array([0, dy * 0.4, 0])
    line = CubicBezier(p0, c1, c2, p1, stroke_color=color, stroke_width=sw)
    return VGroup(line, Dot(p1, radius=0.09, color=color))


def grow(scene, axs, run_time=1.2, lag=0.12):
    """grow axons from their start: the line is drawn and the growth cone rides its tip."""
    axs = list(axs)
    for a in axs:
        a[1].move_to(a[0].get_start())
    scene.add(*[a[1] for a in axs])
    return LaggedStart(*[AnimationGroup(Create(a[0]), UpdateFromFunc(a[1], lambda d, l=a[0]: d.move_to(l.get_end())))
                         for a in axs], lag_ratio=lag, run_time=run_time)


def qtext(s, size=34, y=3.42, x=0.0, color=TEXT):
    t = T(s, size, color, font=TITLE_FONT)
    fit(t, max_w=12.2)
    return t.move_to([x, y, 0])


def tagged(text, color=TEXT, size=26, weight=NORMAL, **kw):
    """a label with a dark backing so it stays readable over a coloured area."""
    t = T(text, size, color, weight=weight, **kw)
    bg = RoundedRectangle(corner_radius=0.1, width=t.width + 0.3, height=t.height + 0.2, stroke_width=0, fill_color=BG,
                          fill_opacity=0.88).move_to(t)
    return VGroup(bg, t)


def lab(text, x, y, size=26, color=TEXT, **kw):
    return T(text, size, color, **kw).move_to([x, y, 0])


def leader(p0, p1, color=GREY, sw=3):
    return Line([p0[0], p0[1], 0], [p1[0], p1[1], 0], stroke_color=color, stroke_width=sw)


# ---- thalamic axon routes in map A (each ends just inside the bottom of its own area, never crossing another) ----
ROUTES = {
    "motor": [(-0.7, -3.05), (-2.0, -1.7), (-2.9, -0.1), (-2.9, 1.25)],
    "touch": [(-0.25, -3.05), (-0.25, -1.2), (-0.25, 0.3)],
    "auditory": [(0.25, -3.05), (0.9, -1.7), (1.5, -0.85)],
    "visual": [(0.7, -3.05), (2.7, -2.0), (3.5, -0.55), (3.3, 0.35)],
}


def full_axons(sw=4):
    return VGroup(*[route(ROUTES[n], sw=sw) for n in NAMES])


def thal_chip(label="thalamus", x=0.0, size=28):
    return chip(label, AXON, size).move_to([x, THAL_Y, 0])


# ---- the mutant state (layout A) ---------------------------------------------------------------
MAIN_TAG_POS = (-5.4, 1.2)
STOP_Y = -2.45
POISED_Y = -2.88
SHEET_BOT = -1.4


def mutant_tag():
    t = T("Gbx2\nmutant", 32, RED, weight=BOLD, line_spacing=0.9)
    return t.move_to([MAIN_TAG_POS[0], MAIN_TAG_POS[1], 0])


def poised_axons():
    return VGroup(*[route([(x, -3.05), (x, (-3.05 + POISED_Y) / 2), (x, POISED_Y)]) for x in AX_X])


def stopped_axons():
    return VGroup(*[route([(x, -3.05), (x, (-3.05 + STOP_Y) / 2), (x, STOP_Y)]) for x in AX_X])


def caps():
    return VGroup(*[Line([x - 0.2, STOP_Y + 0.0, 0], [x + 0.2, STOP_Y + 0.0, 0], stroke_color=RED, stroke_width=7) for x in AX_X])


def gaps():
    return VGroup(*[DashedLine([x, STOP_Y + 0.12, 0], [x, SHEET_BOT, 0], dash_length=0.12, stroke_color=GREY, stroke_width=3)
                    for x in AX_X])


def mutant_state(stain=False, sketch=False):
    d = dict(tag=mutant_tag(), out=A.outline(fo=0.18), chip=thal_chip(), ax=stopped_axons(), caps=caps(), gaps=gaps())
    d["static"] = VGroup(d["tag"], d["out"], d["chip"], d["ax"], d["caps"], d["gaps"])
    if stain:
        d["stain"] = stain_group()
    if sketch:
        d["sk"] = A.sketch(VIOLET, 0.07)
    return d


STAIN_POS = (4.7, -2.45)


def stain_group():
    ch = chip("marker stain", VIOLET, 26).move_to([STAIN_POS[0], STAIN_POS[1], 0])
    ar = Arrow([STAIN_POS[0] - 0.2, STAIN_POS[1] + 0.35, 0], [3.5, -0.3, 0], buff=0.05, color=VIOLET, stroke_width=5,
               tip_length=0.22)
    return VGroup(ch, ar)


def question_marks(cm=A):
    return VGroup(*[T("?", 52, YELLOW, weight=BOLD).move_to(cm.P(PATCH[n][0], PATCH[n][1])) for n in NAMES])


# =============================================================================================
class S00Title(TitleCard):
    LESSON = "Mapping the Cortex: Areas and Arealization"
    TITLE = "Input Finishes the Drawing"


# ---------------------------------------------------------------------------------------------
class S01(SpokenScene):
    """the sheet draws a sketch; the thalamus waits below with axons poised; the question."""

    def construct(self):
        out = A.outline(fo=0.18)
        sk = A.sketch(fo=0.12)
        chip_t = thal_chip()
        stubs = poised_axons()
        sk_lab = lab("faint sketch", -5.4, 0.3, 28, GREY)
        sk_ld = leader([-4.4, 0.4], [-3.55, 1.3])
        ax_lab = lab("thalamic axons", 3.6, -2.45, 28, TEXT)
        ax_ld = leader([2.2, -2.5], [0.95, -2.85])
        q = qtext("Does the sketch need those axons at all?", 38)
        self.play(FadeIn(out, shift=DOWN * 0.1), run_time=0.5)
        self.at("a sketch")
        self.play(FadeIn(sk[0]), Create(sk[1], lag_ratio=0.0), FadeIn(sk_lab), Create(sk_ld), run_time=0.8)
        self.at("thalamic axons")
        self.play(FadeIn(chip_t, shift=UP * 0.1), Create(stubs, lag_ratio=0.15), FadeIn(ax_lab), Create(ax_ld), run_time=0.9)
        self.at("Does the sketch need")
        self.play(FadeIn(q, shift=DOWN * 0.1), run_time=0.6)
        self.at("those axons")
        self.play(Indicate(stubs, color=AXON, scale_factor=1.0), Indicate(ax_lab, color=YELLOW, scale_factor=1.1), run_time=1.0)
        self.finish()


# ---------------------------------------------------------------------------------------------
class S02(SpokenScene):
    """a mouse that lacks the transcription factor Gbx2."""

    def construct(self):
        mouse = mouse_head(3.0, (-2.9, -0.1))
        cap_m = T("mouse", 32, GREY).move_to([-2.9, -2.65, 0])
        gene = chip("Gbx2", TEXT, 64).move_to([3.4, 0.6, 0])
        cap_g = T("transcription factor", 32, TEXT).move_to([3.4, -0.7, 0])
        x1 = Line(gene.get_corner(UL) + [0.15, -0.1, 0], gene.get_corner(DR) + [-0.15, 0.1, 0], stroke_color=RED, stroke_width=10)
        x2 = Line(gene.get_corner(UR) + [-0.15, -0.1, 0], gene.get_corner(DL) + [0.15, 0.1, 0], stroke_color=RED, stroke_width=10)
        tag = T("Gbx2 mutant", 44, RED, weight=BOLD).move_to([-2.9, 3.3, 0])
        self.play(FadeIn(mouse, shift=UP * 0.1), FadeIn(cap_m), FadeIn(tag, shift=DOWN * 0.1), run_time=0.7)
        self.at("lacks")
        self.play(FadeIn(gene, scale=0.8), Create(x1), Create(x2), run_time=0.5)
        self.at("transcription factor")
        self.play(FadeIn(cap_g, shift=UP * 0.1), run_time=0.7)
        self.play(Indicate(gene, color=RED, scale_factor=1.08), run_time=0.9)
        self.finish()


# ---------------------------------------------------------------------------------------------
class S03(SpokenScene):
    """the mutant's thalamic axons grow up and stop far below the cortex."""

    def construct(self):
        tag = mutant_tag()
        out = A.outline(fo=0.18)
        chip_t = thal_chip()
        cortex = lab("cortex", 0.0, 0.95, 40, GREY)
        gp = gaps()
        gl = lab("never arrive", 3.4, -2.2, 30, RED)
        gld = leader([2.15, -2.2], [0.82, -2.0], RED)
        self.add(tag, out, chip_t, cortex)
        self.play(Create(gp), FadeIn(gl), Create(gld), run_time=0.6)
        full = VGroup(*[route([(x, -3.05), (x, (-3.05 + STOP_Y) / 2), (x, STOP_Y)], sw=6) for x in AX_X])
        self.at("thalamic axons")
        self.play(grow(self, [a for a in full], 1.6, 0.1), run_time=1.6)
        self.at("never reach")
        cp = caps()
        self.play(Create(cp), Indicate(full, color=RED, scale_factor=1.0), run_time=0.8)
        self.finish()


class S04(SpokenScene):
    """the newborn mutant cortex waits for its marker stain."""

    def construct(self):
        d = mutant_state()
        self.add(d["static"])
        q = qtext("What should the marker borders look like at birth?")
        qm = question_marks()
        st = stain_group()
        self.play(FadeIn(qm, scale=0.6, lag_ratio=0.15), run_time=0.7)
        self.at("only from thalamic input")
        self.play(Indicate(d["ax"], color=AXON, scale_factor=1.0), run_time=0.9)
        self.at("what should")
        self.play(FadeIn(q, shift=DOWN * 0.1), run_time=0.5)
        self.at("marker borders")
        self.play(FadeIn(st[0], shift=LEFT * 0.2), GrowArrow(st[1]), run_time=0.6)
        self.finish()


class S05Pause(NarratedScene):
    """silent beat: the question stays on screen, still."""

    def construct(self):
        d = mutant_state(True)
        self.add(d["static"], d["stain"], qtext("What should the marker borders look like at birth?"), question_marks())
        self.finish()


# ---------------------------------------------------------------------------------------------
class S06(SpokenScene):
    """prediction: missing or misplaced. Reality: the stain shows borders in their normal places."""

    def construct(self):
        d = mutant_state(True)
        q = qtext("What should the marker borders look like at birth?")
        qm = question_marks()
        self.add(d["static"], d["stain"], q, qm)
        pred = qtext("missing or misplaced", 42).set_color(RED)
        self.play(FadeOut(q), FadeOut(qm), run_time=0.3)
        self.at("missing or misplaced")
        self.play(FadeIn(pred, shift=DOWN * 0.1), run_time=0.5)
        strike = Line(pred.get_left() + [-0.1, 0, 0], pred.get_right() + [0.1, 0, 0], stroke_color=TEXT, stroke_width=6)
        sk = A.sketch(VIOLET, 0.07)
        self.at("they were not")
        self.play(pred.animate.set_color(GREY), Create(strike), FadeIn(sk[0]),
                  LaggedStart(*[Create(m) for m in sk[1]], lag_ratio=0.25), Indicate(d["stain"][0], color=VIOLET, scale_factor=1.1),
                  run_time=1.2)
        self.finish()


# ---------------------------------------------------------------------------------------------
class S07(SpokenScene):
    """Miyashita-Lin, Rubenstein and colleagues, 1999: normal borders at birth in the mutant."""

    def construct(self):
        d = mutant_state(True, True)
        self.add(d["static"], d["stain"], d["sk"])
        cx = -5.15
        year = M("1999", 44, GOLD, weight=BOLD).move_to([cx, -0.55, 0])
        n1 = T("Miyashita-Lin", 28, TEXT).move_to([cx, -1.3, 0])
        n2 = T("Rubenstein", 28, TEXT).move_to([cx, -1.85, 0])
        n3 = T("and colleagues", 28, TEXT).move_to([cx, -2.4, 0])
        for t in (n1, n2, n3):
            fit(t, max_w=2.9)
        self.play(FadeIn(year, shift=RIGHT * 0.1), run_time=0.5)
        self.at("Emily")
        self.play(FadeIn(n1, shift=RIGHT * 0.1), run_time=0.5)
        self.at("John Rubenstein")
        self.play(FadeIn(n2, shift=RIGHT * 0.1), run_time=0.5)
        self.at("and colleagues")
        self.play(FadeIn(n3, shift=RIGHT * 0.1), run_time=0.5)
        self.at("found normal borders")
        self.play(Indicate(d["sk"][1], color=VIOLET, scale_factor=1.03), run_time=1.1)
        self.at("several area markers")
        self.play(Indicate(d["stain"][0], color=VIOLET, scale_factor=1.12), run_time=1.0)
        self.finish()


# ---------------------------------------------------------------------------------------------
class S08(SpokenScene):
    """the sketch forms without thalamic input: the violet sketch stays; the axons go."""

    def construct(self):
        d = mutant_state(True, True)
        self.add(d["static"], d["stain"], d["sk"])
        cx = -5.15
        cred = VGroup(M("1999", 44, GOLD, weight=BOLD).move_to([cx, -0.55, 0]), T("Miyashita-Lin", 28, TEXT).move_to([cx, -1.3, 0]),
                      T("Rubenstein", 28, TEXT).move_to([cx, -1.85, 0]), T("and colleagues", 28, TEXT).move_to([cx, -2.4, 0]))
        self.add(cred)
        self.play(FadeOut(cred), FadeOut(d["stain"]), run_time=0.4)
        self.at("marker sketch")
        self.play(Indicate(d["sk"][1], color=VIOLET, scale_factor=1.0), run_time=0.9)
        self.at("without thalamic input")
        self.play(FadeOut(VGroup(d["ax"], d["caps"], d["gaps"], d["chip"])), run_time=0.9)
        self.finish()


# ---------------------------------------------------------------------------------------------
def adult_outline(cm=A):
    g = VGroup()
    for n in NAMES:
        cx, cy, rx, ry, col, ph = PATCH[n]
        g.add(DashedVMobject(shape(blobpts(cx + 0.12, cy - 0.1, rx * 1.2, ry * 1.17, ph + 1.2), cm.s, cm.c, GREY, GREY, 0, 3),
                             num_dashes=40))
    return g


class S09(SpokenScene):
    """the limit is the readout: markers at birth are a sketch; adult borders could still need input."""

    def construct(self):
        out = A.outline(fo=0.18)
        sk = A.sketch(VIOLET, 0.07)
        tag = mutant_tag()
        self.add(out, sk, tag)
        self.play(FadeOut(tag), run_time=0.4)
        self.at("readout")
        self.play(Indicate(sk[1], color=TEXT, scale_factor=1.0), run_time=0.9)
        l1 = lab("markers at birth", -5.1, 0.15, 28, VIOLET, weight=BOLD)
        a1 = Arrow([-4.4, 0.5, 0], [-3.55, 1.3, 0], buff=0.05, color=VIOLET, stroke_width=4, tip_length=0.2)
        self.at("markers at birth")
        self.play(FadeIn(l1, shift=UP * 0.1), GrowArrow(a1), run_time=0.7)
        adult = adult_outline()
        qm = T("?", 56, YELLOW, weight=BOLD).move_to(A.P(1.1, -0.45))
        l2 = T("adult borders:\ninput may still\nbe needed", 28, GREY, line_spacing=0.9).move_to([5.25, -1.75, 0])
        ld2 = leader([4.45, -1.2], [3.55, 0.0])
        self.at("adult borders")
        self.play(LaggedStart(*[Create(m) for m in adult], lag_ratio=0.2), FadeIn(qm, scale=0.5), FadeIn(l2, shift=UP * 0.1),
                  Create(ld2), run_time=0.9)
        ch = chip("thalamic input?", AXON, 28).move_to([0, THAL_Y, 0])
        dash = DashedLine([0, -3.08, 0], [0, SHEET_BOT, 0], dash_length=0.14, stroke_color=AXON, stroke_width=4)
        self.at("could still need input")
        self.play(FadeIn(ch, shift=UP * 0.1), Create(dash), run_time=0.8)
        self.finish()


# ---------------------------------------------------------------------------------------------
class S10(SpokenScene):
    """the other question: what does input add? Axons rise from the thalamus into the sketched map."""

    def construct(self):
        out = A.outline(fo=0.18)
        sk = A.sketch(VIOLET, 0.07)
        l1 = lab("markers at birth", -5.1, 0.15, 28, VIOLET, weight=BOLD)
        a1 = Arrow([-4.4, 0.5, 0], [-3.55, 1.3, 0], buff=0.05, color=VIOLET, stroke_width=4, tip_length=0.2)
        adult = adult_outline()
        qm = T("?", 56, YELLOW, weight=BOLD).move_to(A.P(1.1, -0.45))
        l2 = T("adult borders:\ninput may still\nbe needed", 28, GREY, line_spacing=0.9).move_to([5.25, -1.75, 0])
        ld2 = leader([4.45, -1.2], [3.55, 0.0])
        ch = chip("thalamic input?", AXON, 28).move_to([0, THAL_Y, 0])
        dash = DashedLine([0, -3.08, 0], [0, SHEET_BOT, 0], dash_length=0.14, stroke_color=AXON, stroke_width=4)
        self.add(out, sk, l1, a1, adult, qm, l2, ld2, ch, dash)
        self.play(FadeOut(VGroup(l1, a1, adult, qm, l2, ld2, dash)), Transform(ch, thal_chip()), run_time=0.6)
        axs = full_axons()
        q = qtext("What does input add?", 40)
        self.at("other question")
        self.play(Indicate(ch, color=AXON, scale_factor=1.12), run_time=0.8)
        self.at("what does input")
        self.play(FadeIn(q, shift=DOWN * 0.1), grow(self, axs, 1.6, 0.15), run_time=1.6)
        self.finish()


# ---------------------------------------------------------------------------------------------
# the graft story (layout B: fetal donor map at the left, newborn host at the right)
MINI = CMap(0.3, (-5.2, 0.95))
GR_C = tuple(float(v) for v in B.P(PATCH["touch"][0], PATCH["touch"][1])[:2])      # centre of the host touch area
GR_W, GR_H = 2.5, 1.7
BLUE_AX = (-0.5, -0.17, 0.17, 0.5)
B_THAL = (GR_C[0], THAL_Y)


def graft_rect(c=GR_C, op=0.6, w=GR_W, h=GR_H):
    return Rectangle(width=w, height=h, stroke_color=PINK, stroke_width=4, fill_color=PINK, fill_opacity=op).move_to([c[0], c[1], 0])


def host_map():
    out = B.outline(fo=0.16)
    pats = B.patches(fo=0.42, sw=2.5)
    return out, pats


def host_lab():
    return T("newborn rat", 32, TEXT).move_to([5.3, 3.0, 0])


def whisker_axons():
    g = VGroup()
    for i in range(4):
        x0 = GR_C[0] + BLUE_AX[i]
        x1 = GR_C[0] + BLUE_AX[i] * 1.8
        g.add(route([(x0, -3.05), ((x0 + x1) / 2, -1.5), (x1, GR_C[1] - GR_H / 2 + 0.1)]))
    return g


def whisker_source():
    head = mouse_head(0.8, (-4.9, -2.5))
    lb = T("whiskers", 26, GREY).move_to([-4.9, -3.5, 0])
    arr = Arrow([-3.7, -3.0, 0], [GR_C[0] - 1.1, -3.35, 0], buff=0.05, color=GREY, stroke_width=4, tip_length=0.2)
    return VGroup(head, lb, arr)


def fly(m, path, w0, h0, w1, h1):
    def f(mob, a):
        k = a ** 2.2
        mob.become(Rectangle(width=w0 + (w1 - w0) * k, height=h0 + (h1 - h0) * k, stroke_color=PINK, stroke_width=4, fill_color=PINK,
                             fill_opacity=0.6).move_to(path.point_from_proportion(a)))
    return UpdateFromAlphaFunc(m, f)


class S11(SpokenScene):
    """Schlaggar and O'Leary, 1991: a piece of fetal visual cortex moves into somatosensory cortex of a newborn rat."""

    def construct(self):
        year = M("1991", 40, GOLD, weight=BOLD).move_to([-4.9, -1.6, 0])
        names = T("Schlaggar and O'Leary", 28, TEXT).move_to([-4.9, -2.3, 0])
        fit(names, max_w=3.5)
        mini_out = MINI.outline(fo=0.16, sw=2.5)
        mini_pats = VGroup(*[MINI.patch(n, 0.55 if n == "visual" else 0.2, 2) for n in NAMES])
        fetal = T("fetal rat", 32, TEXT).move_to([-5.2, -0.3, 0])
        vis_c = MINI.P(*PATCH["visual"][:2])
        out, pats = host_map()
        hl = host_lab()
        piece = Rectangle(width=0.5, height=0.34, stroke_color=PINK, stroke_width=3, fill_color=PINK, fill_opacity=0.9).move_to(vis_c)
        vlab = tagged("visual cortex", PINK, 26).move_to([-5.2, 2.5, 0])
        vld = leader([-4.7, 2.2], [vis_c[0], vis_c[1] + 0.3], PINK)
        self.add(mini_out, mini_pats, fetal, out, pats, hl)
        self.play(FadeIn(year, shift=DOWN * 0.1), run_time=0.4)
        self.at("Bradley")
        self.play(FadeIn(names, shift=DOWN * 0.1), run_time=0.5)
        self.at("grafted")
        self.play(FadeIn(piece, scale=0.4), run_time=0.5)
        self.at("visual cortex")
        self.play(FadeIn(vlab), Create(vld), Indicate(mini_pats[3], color=PINK, scale_factor=1.15), run_time=0.8)
        self.at("fetal rats")
        self.play(Indicate(fetal, color=TEXT, scale_factor=1.15), run_time=0.7)
        path = ArcBetweenPoints(vis_c, np.array([GR_C[0], GR_C[1], 0]), angle=-2.2)
        self.at("into newborn")
        self.play(FadeOut(vlab), FadeOut(vld), fly(piece, path, 0.5, 0.34, GR_W, GR_H), run_time=1.3)
        self.at("somatosensory")
        self.play(Indicate(pats[1], color=GREEN, scale_factor=1.03), run_time=0.8)
        self.finish()


def graft_state():
    out, pats = host_map()
    graft = graft_rect()
    return out, pats, graft, host_lab()


class S12(SpokenScene):
    """whisker axons grow into the graft. What should the graft build?"""

    def construct(self):
        out, pats, graft, hl = graft_state()
        chip_t = thal_chip(x=B_THAL[0])
        self.add(out, pats, graft, hl)
        src = whisker_source()
        axs = whisker_axons()
        q = qtext("What should the graft build?", 40)
        self.play(FadeIn(chip_t, shift=UP * 0.1), run_time=0.4)
        self.at("axons")
        self.play(Indicate(chip_t, color=AXON, scale_factor=1.12), run_time=0.8)
        self.at("whisker")
        self.play(FadeIn(src, shift=RIGHT * 0.2), run_time=0.7)
        self.at("grew")
        self.play(grow(self, axs, 1.5, 0.12), run_time=1.5)
        self.at("what should the graft")
        self.play(FadeIn(q, shift=DOWN * 0.1), run_time=0.6)
        self.finish()


ZG = CMap(2.2, (0.66, -0.87))     # the host's touch area zoomed so the graft fills the frame
ZC = (0.0, -0.1)


def zoom_graft():
    return graft_rect(ZC, 0.6, GR_W * 2.2, GR_H * 2.2)


def zoom_axons():
    g = VGroup()
    for x0, x1 in zip((-1.2, -0.4, 0.4, 1.2), (-1.9, -0.65, 0.65, 1.9)):
        g.add(route([(x0, -3.5), ((x0 + x1) / 2, -2.7), (x1, ZC[1] - GR_H * 1.1 + 0.1)]))
    return g


class S13Pause(NarratedScene):
    """silent beat: the question stays on screen while the camera moves in on the graft."""

    def construct(self):
        out, pats, graft, hl = graft_state()
        chip_t = thal_chip(x=B_THAL[0])
        src = whisker_source()
        axs = whisker_axons()
        q = qtext("What should the graft build?", 40)
        self.add(out, pats, graft, hl, chip_t, src, axs, q)
        others = VGroup(out, pats[0], pats[2], pats[3], hl, chip_t, src, axs)
        self.wait(0.5)
        self.play(FadeOut(others), run_time=0.8)
        gc = np.array([GR_C[0], GR_C[1], 0])
        zoom = VGroup(pats[1], graft)
        self.play(zoom.animate.scale(2.2, about_point=gc).shift(np.array([-gc[0], ZC[1] - gc[1], 0])), run_time=2.4)
        za = zoom_axons()
        self.play(Create(za, lag_ratio=0.15), run_time=0.9)
        self.finish()


# ---------------------------------------------------------------------------------------------
def barrel_cluster(x, y, r):
    return VGroup(Circle(radius=r, stroke_color=GREEN, stroke_width=3, fill_color=GREEN, fill_opacity=0.5).move_to([x, y, 0]),
                  Circle(radius=r * 0.5, stroke_width=0, fill_color=GREEN, fill_opacity=0.95).move_to([x, y, 0]))


class S14(SpokenScene):
    """rows of barrels form in the graft."""

    def construct(self):
        patch = ZG.patch("touch", 0.42, 2.5)
        graft = zoom_graft()
        za = zoom_axons()
        q = qtext("What should the graft build?", 40)
        self.add(patch, graft, za, q)
        rows = []
        for j in range(4):
            row = VGroup()
            for i in range(5):
                x = (i - 2) * 1.0 + (0.1 if j % 2 else -0.1) + 0.04 * (j - 1.5) * (i - 2)
                y = ZC[1] + (1.5 - j) * 0.8 + 0.05 * (i - 2) ** 2 - 0.1
                row.add(barrel_cluster(x, y, 0.3 + 0.05 * np.sin(1.7 * i + 2.3 * j)))
            rows.append(row)
        self.play(FadeOut(q), run_time=0.4)
        self.at("barrels")
        self.play(LaggedStart(*[FadeIn(r, scale=0.5, lag_ratio=0.15) for r in rows], lag_ratio=0.35), run_time=1.8)
        gl = tagged("grafted visual cortex", PINK, 28).move_to([0, 2.28, 0])
        self.at("visual cortex")
        self.play(FadeIn(gl, shift=DOWN * 0.1), run_time=0.6)
        ta = lab("touch area", -5.3, 0.6, 28, GREEN)
        tld = leader([-4.35, 0.5], [-3.5, 0.2], GREEN)
        self.at("feature of the area")
        self.play(FadeIn(ta, shift=RIGHT * 0.1), Create(tld), Indicate(VGroup(*rows), color=GREEN, scale_factor=1.04), run_time=1.1)
        wa = lab("whisker axons", 4.9, -2.9, 28, TEXT)
        wld = leader([3.5, -2.9], [1.45, -2.75])
        self.at("whose input")
        self.play(FadeIn(wa, shift=LEFT * 0.1), Create(wld), Indicate(za, color=AXON, scale_factor=1.0), run_time=1.2)
        self.finish()


# ---------------------------------------------------------------------------------------------
# the ferret rewiring diagram
X_SRC, X_REL, X_CTX = -4.9, -1.2, 3.9
Y_TOP, Y_BOT = 1.9, -1.6


def blockn(w, h, x, y, color=GREY, fo=0.15, sw=3):
    return Rectangle(width=w, height=h, stroke_color=color, stroke_width=sw, fill_color=color, fill_opacity=fo).move_to([x, y, 0])


def path_nodes():
    d = {}
    d["retina"] = VGroup(eye_icon(1.2, (X_SRC, Y_TOP)), lab("retina", X_SRC, Y_TOP + 0.75))
    d["targets_blk"] = blockn(2.0, 1.1, X_REL, Y_TOP, GREY)
    d["targets_lab"] = lab("usual targets", X_REL, Y_TOP - 0.95)
    d["vctx"] = VGroup(blockn(3.0, 1.5, X_CTX, Y_TOP, PINK, 0.35), lab("visual cortex", X_CTX, Y_TOP, 28))
    d["in_blk"] = blockn(1.3, 0.9, X_SRC, Y_BOT, GREY)
    d["in_lab"] = lab("normal inputs", X_SRC, Y_BOT - 0.85)
    d["ath_blk"] = blockn(2.0, 1.1, X_REL, Y_BOT, GREY)
    d["ath_lab"] = lab("auditory thalamus", X_REL, Y_BOT - 0.95)
    d["actx"] = VGroup(blockn(3.0, 1.5, X_CTX, Y_BOT, SAND, 0.35), lab("auditory cortex", X_CTX, Y_BOT, 28))
    return d


def thin_top_arrows():
    kw = dict(dash_length=0.12, stroke_color=AXON, stroke_width=2.5)
    return VGroup(DashedLine([X_SRC + 0.75, Y_TOP, 0], [X_CTX - 1.5, Y_TOP, 0], **kw))


def solid_arrow(x0, x1, y, color=AXON, sw=6):
    return Arrow([x0, y, 0], [x1, y, 0], buff=0, color=color, stroke_width=sw, tip_length=0.25)


FER_S = 1.25
FER_C = (X_SRC + 2.5 * FER_S, -1.95)       # facing left, so its eye sits at x = X_SRC


def ferret_group():
    f = ferret(FER_S, FER_C, right=False)
    cap = lab("ferret", FER_C[0] + 0.5, -3.55, 30, GREY)
    link = DashedLine([X_SRC, FER_C[1] + 0.3 * FER_S, 0], [X_SRC, Y_TOP - 0.4, 0], dash_length=0.1, stroke_color=GREY, stroke_width=2.5)
    return VGroup(f, cap, link)


class S15(SpokenScene):
    """Sur laboratory, ferrets: born with an immature visual pathway (thin and incomplete)."""

    def construct(self):
        n = path_nodes()
        sur = T("Sur laboratory", 34, TEXT, font=TITLE_FONT).move_to([0, 3.5, 0])
        fg = ferret_group()
        arrows = thin_top_arrows()
        thin = lab("thin, incomplete pathway", -0.6, 2.85, 26, TEXT)
        self.play(FadeIn(sur, shift=DOWN * 0.1), FadeIn(fg, shift=UP * 0.1), FadeIn(n["retina"]), FadeIn(n["targets_blk"]),
                  FadeIn(n["targets_lab"]), FadeIn(n["vctx"]), run_time=0.9)
        self.at("in ferrets")
        self.play(Create(arrows, lag_ratio=0.3), run_time=1.0)
        self.at("immature visual")
        self.play(FadeIn(thin, shift=DOWN * 0.1), Indicate(arrows, color=AXON, scale_factor=1.0), run_time=1.0)
        self.finish()


def top_state(reduced=False):
    n = path_nodes()
    top = VGroup(n["retina"], n["targets_lab"], n["vctx"])
    blk = n["targets_blk"]
    if reduced:
        blk = blockn(0.8, 0.4, X_REL, Y_TOP, RED, 0.35)
        n["targets_lab"].shift(UP * 0.3)
    return n, VGroup(top, blk, thin_top_arrows())


def bottom_row():
    n = path_nodes()
    g = VGroup(n["in_blk"], n["in_lab"], n["ath_blk"], n["ath_lab"], n["actx"])
    arr_in = solid_arrow(X_SRC + 0.75, X_REL - 1.1, Y_BOT)
    arr_out = solid_arrow(X_REL + 1.1, X_CTX - 1.6, Y_BOT)
    return n, g, arr_in, arr_out


def cut_mark():
    cx = X_SRC
    return VGroup(Line([cx - 0.4, Y_BOT + 0.3, 0], [cx + 0.4, Y_BOT - 0.3, 0], stroke_color=RED, stroke_width=7),
                  Line([cx + 0.4, Y_BOT + 0.3, 0], [cx - 0.4, Y_BOT - 0.3, 0], stroke_color=RED, stroke_width=7))


class S16(SpokenScene):
    """the retina's usual targets shrink; the normal inputs to the auditory thalamus are removed."""

    def construct(self):
        n, top = top_state()
        sur = T("Sur laboratory", 34, TEXT, font=TITLE_FONT).move_to([0, 3.5, 0])
        fg = ferret_group()
        thin = lab("thin, incomplete pathway", -0.6, 2.85, 26, TEXT)
        self.add(sur, fg, top, thin)
        self.play(FadeOut(sur), FadeOut(thin), run_time=0.4)
        self.at("retina's normal targets")
        self.play(Indicate(VGroup(n["targets_blk"], n["targets_lab"]), color=TEXT, scale_factor=1.06), run_time=0.9)
        small = blockn(0.8, 0.4, X_REL, Y_TOP, RED, 0.35)
        self.at("were reduced")
        self.play(Transform(n["targets_blk"], small), n["targets_lab"].animate.shift(UP * 0.3), run_time=0.9)
        bn, brow, arr_in, arr_out = bottom_row()
        self.at("normal inputs")
        self.play(FadeOut(fg), run_time=0.4)
        self.play(FadeIn(brow), GrowArrow(arr_in), GrowArrow(arr_out), run_time=0.7)
        self.at("auditory thalamus")
        self.play(Indicate(VGroup(bn["ath_blk"], bn["ath_lab"]), color=TEXT, scale_factor=1.06), run_time=0.8)
        self.at("were removed")
        self.play(bn["in_blk"].animate.set_color(RED), FadeOut(arr_in), Create(cut_mark()), run_time=0.8)
        self.finish()


def rewire_state():
    """the end of S16: top targets shrunk, inputs removed, the thalamus-to-cortex arrow still there."""
    n, top = top_state(reduced=True)
    bn, brow, arr_in, arr_out = bottom_row()
    brow[0].set_color(RED)
    return VGroup(top, brow, arr_out, cut_mark()), bn, arr_out


def retinal_axon():
    return axon((X_SRC + 0.55, Y_TOP - 0.45), (X_REL - 0.8, Y_BOT + 0.62), bend=0.0).set_z_index(3)


class S17(SpokenScene):
    """retinal axons grow into the auditory thalamus; auditory cortex receives visual activity."""

    def construct(self):
        st, bn, arr_out = rewire_state()
        self.add(st)
        ra = retinal_axon()
        self.play(Indicate(st[0][0][0], color=TEXT, scale_factor=1.15), run_time=0.9)
        self.at("grew")
        self.play(grow(self, [ra], 1.2), run_time=1.2)
        self.at("thalamus")
        self.play(Indicate(VGroup(bn["ath_blk"], bn["ath_lab"]), color=TEXT, scale_factor=1.06), run_time=0.7)
        pulses = [Dot(radius=0.12, color=PINK).set_z_index(5) for _ in range(3)]
        anims = []
        for p in pulses:
            p.move_to(ra[0].get_start())
            anims.append(Succession(FadeIn(p, run_time=0.01),
                                    MoveAlongPath(p, ra[0], run_time=0.6, rate_func=linear),
                                    MoveAlongPath(p, Line(arr_out.get_start(), arr_out.get_end() + [0.05, 0, 0]), run_time=0.6, rate_func=linear)))
        self.play(LaggedStart(*anims, lag_ratio=0.35), run_time=1.9)
        box = bn["actx"][0]
        self.at("received")
        self.play(box.animate.set_stroke(PINK, 6), run_time=0.5)
        sparks = VGroup(*[Dot([X_CTX + dx, Y_BOT + dy - 0.62, 0], radius=0.09, color=PINK) for dx, dy in
                          ((-0.9, 0.0), (-0.3, 0.08), (0.4, -0.06), (0.9, 0.05), (0.1, -0.08))])
        self.at("visual activity")
        self.play(FadeIn(sparks, scale=0.4, lag_ratio=0.2), run_time=0.7)
        self.finish()


# ---------------------------------------------------------------------------------------------
# orientation maps: hue follows the preferred edge angle (0 to 180 degrees), so the ramp wraps round
def hue_hex(f):
    r, g, b = colorsys.hsv_to_rgb(f % 1.0, 0.55, 0.9)
    return "#%02x%02x%02x" % (int(r * 255), int(g * 255), int(b * 255))


NC, NR, CELL = 20, 15, 0.38          # a panel is 7.6 x 5.7 at full size
PANEL_C = (-0.9, 0.0)


def hue_at(u, v, regular, rng):
    """visual cortex: smooth iso-orientation stripes. rewired: the same stripes, warped, jittered and with gaps."""
    if regular:
        return 2.6 * u + 0.9 * v + 0.10 * np.sin(2 * np.pi * (1.2 * v + 0.3))
    uu = u + 0.06 * np.sin(2 * np.pi * (2.3 * v + 0.2)) + 0.03 * np.sin(2 * np.pi * (3.1 * u + 1.1 * v))
    vv = v + 0.07 * np.sin(2 * np.pi * (1.7 * u))
    return 2.6 * uu + 0.9 * vv + 0.12 * np.sin(2 * np.pi * (1.2 * vv + 0.3))


def orient_panel(cx, cy, regular, seed=3, s=1.0, grey=True):
    """returns the panel frame, the cells (grey if grey else coloured), the final colours and the tick bars."""
    rng = np.random.RandomState(seed)
    w, h = NC * CELL * s, NR * CELL * s
    frame = Rectangle(width=w, height=h, stroke_color=SAND if grey else PINK, stroke_width=3, fill_opacity=0).move_to([cx, cy, 0])
    cells, cols, hues, gaps = VGroup(), [], [], []
    for j in range(NR):
        for i in range(NC):
            u, v = (i + 0.5) / NC, (j + 0.5) / NR
            hh = hue_at(u, v, regular, rng) % 1.0
            gap = False
            x, y = cx + (i + 0.5 - NC / 2) * CELL * s, cy + (j + 0.5 - NR / 2) * CELL * s
            col = hue_hex(hh)
            cols.append(GREY if gap else col)
            hues.append(hh)
            gaps.append(gap)
            cells.add(Square(CELL * s, stroke_color=GREY, stroke_width=0.6, stroke_opacity=0.35,
                             fill_color=GREY if (grey or gap) else col,
                             fill_opacity=0.22 if (grey or gap) else 0.75).move_to([x, y, 0]))
    ticks = VGroup()
    for j in range(1, NR, 3):
        for i in range(1, NC, 3):
            k = j * NC + i
            if gaps[k]:
                continue
            x, y = cx + (i + 0.5 - NC / 2) * CELL * s, cy + (j + 0.5 - NR / 2) * CELL * s
            th = hues[k] * np.pi
            d = 0.15 * s * 1.4
            ticks.add(Line([x - d * np.cos(th), y - d * np.sin(th), 0], [x + d * np.cos(th), y + d * np.sin(th), 0],
                           stroke_color=BG, stroke_width=4))
    return frame, cells, cols, ticks


def final_fills(cells, cols):
    """a coloured twin of the grey cells, for Transform."""
    tw = cells.copy()
    for t, c in zip(tw, cols):
        t.set_fill(c, 0.22 if c == GREY else 0.75)
    return tw


def hue_legend(vertical=True, title="edge angle"):
    """a full hue ramp bar, 0 to 180 degrees, same structure whichever way it lies (so one can transform into the other)."""
    n = 60
    bar = VGroup()
    if vertical:
        x0, y0, L, W = 5.0, 2.0, 4.0, 0.36
        for k in range(n):
            bar.add(Rectangle(width=W, height=L / n + 0.01, stroke_width=0, fill_color=hue_hex(k / n), fill_opacity=0.85)
                    .move_to([x0, y0 - (k + 0.5) * L / n, 0]))
        t = T(title, 26, GREY).move_to([5.45, 2.55, 0])
        tk = [T("0°", 26, GREY).move_to([5.75, 2.0, 0]), T("90°", 26, GREY).move_to([5.8, 0.0, 0]),
              T("180°", 26, GREY).move_to([5.95, -2.0, 0])]
    else:
        x0, y0, L, W = -3.0, -2.72, 6.0, 0.26
        for k in range(n):
            bar.add(Rectangle(width=L / n + 0.01, height=W, stroke_width=0, fill_color=hue_hex(k / n), fill_opacity=0.85)
                    .move_to([x0 + (k + 0.5) * L / n, y0, 0]))
        t = T(title, 26, GREY).move_to([-4.6, y0, 0])
        tk = [T("0°", 26, GREY).move_to([-3.0, -3.25, 0]), T("90°", 26, GREY).move_to([0.0, -3.25, 0]),
              T("180°", 26, GREY).move_to([3.0, -3.25, 0])]
    return VGroup(bar, t, *tk)


Q_REWIRED = "What did the rewired cortex build?"
PAN_S = 0.7


class S18(SpokenScene):
    """adult auditory cortex has no map of edge orientation. What did the rewired cortex build?"""

    def construct(self):
        frame, cells, cols, ticks = orient_panel(PANEL_C[0], PANEL_C[1], False, seed=3)
        head = lab("auditory cortex (normal)", PANEL_C[0], 3.42, 34, SAND, weight=BOLD)
        leg = hue_legend(True)
        q = qtext(Q_REWIRED, 36, y=-3.42)
        self.play(FadeIn(head, shift=DOWN * 0.1), FadeIn(frame), run_time=0.6)
        self.at("cortex")
        self.play(FadeIn(cells, lag_ratio=0.004), run_time=1.0)
        self.at("no map")
        self.play(Indicate(frame, color=SAND, scale_factor=1.01), run_time=0.9)
        self.at("edge orientation")
        self.play(FadeIn(leg, shift=LEFT * 0.15), run_time=0.9)
        self.at("what did the rewired cortex")
        self.play(FadeIn(q, shift=DOWN * 0.1), run_time=0.7)
        self.finish()


class S19Pause(NarratedScene):
    """silent beat: the question stays on screen; a slow pulse shows the pause is a pause."""

    def construct(self):
        frame, cells, cols, ticks = orient_panel(PANEL_C[0], PANEL_C[1], False, seed=3)
        head = lab("auditory cortex (normal)", PANEL_C[0], 3.42, 34, SAND, weight=BOLD)
        q = qtext(Q_REWIRED, 36, y=-3.42)
        qm = T("?", 200, YELLOW, weight=BOLD).move_to([PANEL_C[0], PANEL_C[1], 0]).set_opacity(0.1)
        self.add(frame, cells, head, hue_legend(True), q, qm)
        self.play(qm.animate.set_opacity(0.38), run_time=2.3, rate_func=smooth)
        self.play(qm.animate.set_opacity(0.1), run_time=2.3, rate_func=smooth)
        self.finish()


class S20(SpokenScene):
    """neurons tuned to edge orientation, arranged in a map like visual cortex, but less regular."""

    def construct(self):
        frame, cells, cols, ticks_unused = orient_panel(PANEL_C[0], PANEL_C[1], False, seed=3)
        head = lab("auditory cortex (normal)", PANEL_C[0], 3.42, 34, SAND, weight=BOLD)
        leg_v = hue_legend(True)
        q = qtext(Q_REWIRED, 36, y=-3.42)
        self.add(frame, cells, head, leg_v, q)
        # the answer: the same panel slides right, shrinks, and the cells take their preferred-angle hues
        RX, VX, CY = 3.3, -3.3, 0.2
        fr2, cells2, cols2, ticks2 = orient_panel(RX, CY, False, seed=3, s=PAN_S)
        fin2 = final_fills(cells2, cols2)
        credit_t = T("Sharma, Angelucci and Sur, 2000", 30, TEXT).move_to([0, 3.5, 0])
        head2 = lab("rewired auditory cortex: less regular", RX, 2.95, 26, SAND, weight=BOLD)
        leg_h = hue_legend(False)
        vf, vcells, vcols, vticks = orient_panel(VX, CY, True, seed=1, s=PAN_S, grey=False)
        head1 = lab("visual cortex (reference)", VX, 2.95, 26, PINK, weight=BOLD)
        self.play(FadeOut(q), FadeOut(head), FadeIn(credit_t, shift=DOWN * 0.1), ReplacementTransform(frame, fr2),
                  ReplacementTransform(cells, cells2), FadeOut(leg_v), FadeIn(leg_h), FadeIn(vf), FadeIn(vcells, lag_ratio=0.003),
                  FadeIn(head1), run_time=1.0)
        self.play(Transform(cells2, fin2, lag_ratio=0.004), FadeIn(head2), run_time=1.6)
        self.play(FadeIn(ticks2), FadeIn(vticks), run_time=0.6)
        self.at("like visual cortex")
        self.play(Indicate(head1, color=PINK, scale_factor=1.06), Indicate(vf, color=PINK, scale_factor=1.01), run_time=0.9)
        self.at("less regular")
        self.play(Indicate(head2, color=TEXT, scale_factor=1.06), Indicate(fr2, color=TEXT, scale_factor=1.01), run_time=1.0)
        self.finish()


class S21(SpokenScene):
    """a companion paper: the animals responded to light through the rewired pathway as to a visual stimulus."""

    def construct(self):
        tag = T("companion paper:  von Melchner, Pallas and Sur", 30, TEXT).move_to([0, 3.45, 0])
        fer = ferret(0.95, (1.3, 1.15), right=True)
        flash = glow(-5.0, 1.15, 0.4)
        rays = VGroup(*[Line(np.array([-5.0, 1.15, 0]) + 0.75 * np.array([np.cos(a), np.sin(a), 0]),
                             np.array([-5.0, 1.15, 0]) + 1.15 * np.array([np.cos(a), np.sin(a), 0]), stroke_color=LIGHT, stroke_width=4)
                        for a in np.linspace(0, 2 * np.pi, 9)[:-1]])
        YR = -2.3
        eye = eye_icon(1.4, (-5.4, YR))
        eye_l = lab("retina", -5.4, YR - 1.1, 26, GREY)
        ath = VGroup(blockn(3.3, 1.5, -1.5, YR, GREY), lab("auditory thalamus", -1.5, YR - 1.1, 26))
        act = VGroup(blockn(3.5, 1.5, 3.7, YR, SAND, 0.35), lab("auditory cortex", 3.7, YR - 1.1, 26))
        a1 = solid_arrow(-4.55, -3.2, YR, sw=6)
        a2 = solid_arrow(0.3, 1.85, YR, sw=6)
        diagram = VGroup(eye, eye_l, ath, act, a1, a2)
        self.add(tag, fer)
        self.play(Indicate(fer, color=GREY, scale_factor=1.0), run_time=0.8)
        self.at("reported")
        self.play(FadeIn(diagram), run_time=0.8)
        self.at("to light")
        self.play(FadeIn(flash, scale=0.4), Create(rays), run_time=0.5)
        p1 = Dot(radius=0.14, color=LIGHT).move_to([-4.6, YR, 0]).set_z_index(5)
        p2 = Dot(radius=0.14, color=PINK).move_to([-4.6, YR, 0]).set_z_index(5)
        self.play(Succession(FadeIn(p1, run_time=0.05), MoveAlongPath(p1, Line([-4.6, YR, 0], [-3.2, YR, 0]), run_time=0.35, rate_func=linear),
                             FadeOut(p1, run_time=0.05),
                             FadeIn(p2, run_time=0.05), MoveAlongPath(p2, Line([-3.2, YR, 0], [3.0, YR, 0]), run_time=1.1, rate_func=linear)),
                  Indicate(ath[0], color=PINK, scale_factor=1.04), run_time=1.6)
        self.play(act[0].animate.set_stroke(PINK, 6).set_fill(PINK, 0.55), FadeOut(p2), run_time=0.4)
        resp = lab("turns toward the light", 1.3, -0.55, 30, TEXT)
        self.at("a visual")
        self.play(fer.animate.flip(UP), FadeIn(resp, shift=UP * 0.1), run_time=0.9)
        self.finish()


# ---------------------------------------------------------------------------------------------
# Chou and colleagues: the visual area drawn as primary core plus higher-order ring, then zoomed
def vis_ring(cm, fo=0.2):
    return shape(blobpts(3.5, 0.45, 1.1, 1.5, 0.6), cm.s, cm.c, PINK, PINK, fo, 2.5)


def vis_core(cm, fo=0.6):
    return shape(blobpts(3.55, 0.45, 0.6, 0.92, 0.6), cm.s, cm.c, PINK, PINK, fo, 3.5)


ZS = 1.75
ZV = CMap(ZS * 1.0, (-ZS * 3.5, 0.6 - ZS * 0.45))     # visual area centred at (0, 0.6)
ZV_C = (0.0, 0.6)


def vis_axons_z():
    g = VGroup()
    for x0, x1 in zip((-0.5, 0.0, 0.5), (-0.55, 0.0, 0.55)):
        g.add(route([(x0, -3.05), ((x0 + x1) / 2, -2.0), (x1, 0.6 - 1.61 + 0.2)]))
    return g


def vis_chip():
    return chip("visual thalamus", AXON, 28).move_to([0, THAL_Y, 0])


def zone_labels():
    l1 = T("primary visual\ncortex", 28, PINK, weight=BOLD, line_spacing=0.9).move_to([-4.9, 0.6, 0])
    ld1 = leader([-3.65, 0.6], [-0.6, 0.6], PINK)
    l2 = T("higher-order\nareas", 28, PINK, line_spacing=0.9).move_to([4.8, 1.4, 0])
    ld2 = leader([3.55, 1.4], [1.4, 1.4], PINK)
    return l1, ld1, l2, ld2


def credit_chou():
    year = M("2013", 44, GOLD, weight=BOLD).move_to([-5.0, 3.1, 0])
    nm = T("Chou and\ncolleagues", 28, TEXT, line_spacing=0.9).move_to([-5.0, 2.2, 0])
    return year, nm


class S22(SpokenScene):
    """back on the mouse map: visual cortex at the back with higher-order visual areas around it; zoom in on it."""

    def construct(self):
        out = A.outline(fo=0.18)
        sk = A.sketch(names=("motor", "touch", "auditory"))
        ring, core = vis_ring(A), vis_core(A)
        chip_t = thal_chip("visual thalamus", x=1.8)
        self.add(out, sk, ring, core, chip_t)
        l1, ld1, l2, ld2 = zone_labels()
        self.wait(0.2)
        self.play(FadeOut(out), FadeOut(sk), FadeOut(chip_t), Transform(ring, vis_ring(ZV)), Transform(core, vis_core(ZV)),
                  run_time=1.0)
        self.play(FadeIn(l1, shift=RIGHT * 0.1), Create(ld1), FadeIn(l2, shift=LEFT * 0.1), Create(ld2), FadeIn(vis_chip()),
                  Create(vis_axons_z()), run_time=0.7)
        self.finish()


def chou_state():
    ring, core = vis_ring(ZV), vis_core(ZV)
    l1, ld1, l2, ld2 = zone_labels()
    return ring, core, VGroup(l1, ld1, l2, ld2), vis_chip(), vis_axons_z()


class S23(SpokenScene):
    """Chou and colleagues, 2013: the axons from the visual thalamus are removed."""

    def construct(self):
        ring, core, labels, chip_t, ax = chou_state()
        self.add(ring, core, labels, chip_t, ax)
        year, nm = credit_chou()
        self.play(FadeIn(year, shift=RIGHT * 0.1), run_time=0.5)
        self.at("Shenju")
        self.play(FadeIn(nm, shift=RIGHT * 0.1), run_time=0.6)
        cuts = VGroup(*[Line([a[0].point_from_proportion(0.45)[0] - 0.25, a[0].point_from_proportion(0.45)[1] - 0.12, 0],
                             [a[0].point_from_proportion(0.45)[0] + 0.25, a[0].point_from_proportion(0.45)[1] + 0.12, 0],
                             stroke_color=RED, stroke_width=7) for a in ax])
        self.at("removed")
        self.play(Create(cuts, lag_ratio=0.2), ax.animate.set_color(RED), run_time=0.8)
        self.at("axons")
        self.play(FadeOut(ax), FadeOut(cuts), run_time=0.9)
        self.at("visual thalamus")
        self.play(Indicate(chip_t, color=TEXT, scale_factor=1.08), run_time=0.9)
        self.finish()


class S24(SpokenScene):
    """primary visual cortex and the higher-order areas around it blur into one shade."""

    def construct(self):
        ring, core, labels, chip_t, ax = chou_state()
        year, nm = credit_chou()
        self.add(ring, core, labels, chip_t, year, nm)
        self.play(FadeOut(year), FadeOut(nm), run_time=0.4)
        self.at("primary visual cortex")
        self.play(Indicate(labels[0], color=PINK, scale_factor=1.1), Indicate(core, color=PINK, scale_factor=1.03), run_time=1.0)
        self.at("higher order")
        self.play(Indicate(labels[2], color=PINK, scale_factor=1.1), Indicate(ring, color=PINK, scale_factor=1.02), run_time=1.0)
        self.at("failed to develop")
        ghost = DashedVMobject(vis_core(ZV, 0.0).set_stroke(GREY, 2.5, 0.7), num_dashes=30)
        self.play(core.animate.set_fill(PINK, 0.0).set_stroke(opacity=0), ring.animate.set_fill(PINK, 0.38).set_stroke(opacity=0.5),
                  labels.animate.set_opacity(0.25), FadeIn(ghost), run_time=1.3)
        res = T("one shade:\nno primary /\nhigher-order\nsplit", 28, RED, line_spacing=0.9).move_to([4.8, -0.7, 0])
        self.play(FadeOut(labels), FadeOut(ghost), FadeIn(res, shift=UP * 0.1), run_time=0.6)
        self.finish()


# ---------------------------------------------------------------------------------------------
ZT = CMap(2.0, (0.6, -0.7))          # the touch area zoomed to fill the frame (centre at 0, 0)


def lattice(stage, cx, cy, nx=6, ny=4, seed=5):
    """a map of dots inside an area: stage 0 coarse (wide, jittered, uneven), 1 tightening, 2 tight and nearly regular."""
    rng = np.random.RandomState(seed)
    sp, jit, rv = ((0.82, 0.22, 0.05), (0.62, 0.10, 0.03), (0.46, 0.03, 0.02))[stage]
    g = VGroup()
    for j in range(ny):
        for i in range(nx):
            jx, jy, jr = rng.uniform(-1, 1, 3)
            r = 0.15 - 0.05 * stage + rv * jr
            g.add(Dot([cx + (i - (nx - 1) / 2) * sp + jx * jit, cy + (j - (ny - 1) / 2) * sp * 0.9 + jy * jit, 0], radius=r,
                      color=TEXT).set_opacity(0.85 + 0.1 * stage))
    return g


ZK = 1.5
Z_TOUCH = CMap(ZK, (-3.7 + 0.3 * ZK, 0.6 - 0.35 * ZK))
Z_VIS = CMap(ZK, (3.7 - 3.55 * ZK, 0.6 - 0.45 * ZK))


class S25(SpokenScene):
    """normal development (not the mutant): activity refines the map inside each area, here two areas tightening."""

    def construct(self):
        p1 = Z_TOUCH.patch("touch", 0.42, 3)
        p2 = Z_VIS.patch("visual", 0.42, 3)
        tag = lab("normal development: inside each area", 0, 3.45, 30, GREY)
        c1 = chip("spontaneous\nactivity", NEURON, 26).move_to([-3.7, -2.85, 0])
        c2 = chip("sensory\nactivity", NEURON, 26).move_to([3.7, -2.85, 0])
        ar1 = Arrow([-3.7, -2.3, 0], [-3.7, -1.5, 0], buff=0.05, color=NEURON, stroke_width=5, tip_length=0.22)
        ar2 = Arrow([3.7, -2.3, 0], [3.7, -1.7, 0], buff=0.05, color=NEURON, stroke_width=5, tip_length=0.22)
        tc, vc = (-3.7, 0.6), (3.7, 0.6)
        a0, a1, a2 = lattice(0, *tc, 6, 4, 5), lattice(1, *tc, 6, 4, 5), lattice(2, *tc, 6, 4, 5)
        b0, b1, b2 = lattice(0, *vc, 3, 4, 8), lattice(1, *vc, 3, 4, 8), lattice(2, *vc, 3, 4, 8)
        self.add(p1, p2, tag)
        self.play(FadeIn(c1, shift=UP * 0.1), GrowArrow(ar1), run_time=0.6)
        self.at("sensory activity")
        self.play(FadeIn(c2, shift=UP * 0.1), GrowArrow(ar2), run_time=0.6)
        cl = lab("coarse maps", 0.0, -1.7, 28, GREY)
        self.play(FadeIn(a0, lag_ratio=0.02), FadeIn(b0, lag_ratio=0.02), FadeIn(cl), run_time=0.8)
        self.at("refine")
        self.play(Transform(a0, a1), Transform(b0, b1), run_time=1.0)
        self.play(Transform(a0, a2), Transform(b0, b2), run_time=1.0)
        rl = lab("tighter maps", 0.0, -1.7, 28, TEXT)
        self.play(Transform(cl, rl), run_time=0.4)
        note = T("Later lessons take that up.", 32, GREY).move_to([0, -2.85, 0])
        self.at("Later lessons")
        self.play(FadeOut(c1), FadeOut(c2), FadeOut(ar1), FadeOut(ar2), run_time=0.3)
        self.play(FadeIn(note, shift=DOWN * 0.1), run_time=0.6)
        self.finish()


def inner_dots(cm, name, n_x, n_y, sp, r=0.1):
    cx, cy = PATCH[name][:2]
    g = VGroup()
    for i in range(n_x):
        for j in range(n_y):
            g.add(Dot(cm.P(cx + (i - (n_x - 1) / 2) * sp, cy + (j - (n_y - 1) / 2) * sp), radius=r, color=TEXT).set_opacity(1.0))
    return g


def barrel_grid(cm):
    g = VGroup()
    cx, cy = PATCH["touch"][:2]
    for i in range(5):
        for j in range(3):
            g.add(Circle(radius=0.1 * cm.s, stroke_color=TEXT, stroke_width=2, fill_color=TEXT, fill_opacity=1.0)
                  .move_to(cm.P(cx + (i - 2) * 0.4, cy + (j - 1) * 0.4)))
    return g


def vis_ticks(cm):
    cx, cy = PATCH["visual"][:2]
    pts = [(-0.4, 0.7, 0.3), (0.0, 0.7, 0.9), (0.4, 0.7, 1.5), (-0.4, 0.0, 2.1), (0.0, 0.0, 2.7), (0.4, 0.0, 0.1),
           (-0.4, -0.7, 0.7), (0.0, -0.7, 1.3), (0.4, -0.7, 1.9)]
    g = VGroup()
    for dx, dy, th in pts:
        x, y = cm.P(cx + dx, cy + dy)[:2]
        d = 0.2
        g.add(Line([x - d * np.cos(th), y - d * np.sin(th), 0], [x + d * np.cos(th), y + d * np.sin(th), 0], stroke_color=TEXT, stroke_width=6))
    return g


class S26(SpokenScene):
    """pencil sketch, then inked borders and inner maps drawn over it as axons arrive."""

    def construct(self):
        out = A.outline(fo=0.16)
        sk = A.sketch(VIOLET, 0.07)
        ink = A.patches(fo=0.45, sw=3.5)
        chip_t = thal_chip()
        axs = full_axons()
        lab1 = lab("sketch, before input", 0, 3.45, 34, VIOLET, weight=BOLD)
        lab2 = lab("input arrives", 0, 3.45, 34, TEXT, weight=BOLD)
        inner = VGroup(inner_dots(A, "motor", 3, 2, 0.4), barrel_grid(A), inner_dots(A, "auditory", 4, 2, 0.4), vis_ticks(A))
        self.add(out, sk, lab1)
        self.at("marker sketch")
        self.play(Indicate(sk[1], color=VIOLET, scale_factor=1.0), run_time=1.0)
        self.at("Input then")
        self.play(FadeIn(chip_t, shift=UP * 0.1), Transform(lab1, lab2), grow(self, axs, 0.6, 0.08), run_time=0.6)
        self.at("sharpens it")
        self.play(FadeIn(ink, scale=0.97), FadeOut(sk), run_time=0.8)
        self.at("shapes what")
        self.play(LaggedStart(*[FadeIn(g, lag_ratio=0.05) for g in inner], lag_ratio=0.25), run_time=1.6)
        self.wait(1.0)
        self.finish()


class S27End(EndCard):
    LINE = "The marker sketch forms without input; input then sharpens it."
