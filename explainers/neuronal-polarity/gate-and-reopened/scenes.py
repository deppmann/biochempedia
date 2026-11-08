"""Neuronal polarity, chapter 6: The Gate, and the Race Reopened (Biochemistrypedia chaptered film)

Timed to the SPOKEN words: every self.at("...") cue waits for that phrase in audio/words.json.
No curve is plotted in this chapter; the one scale that is drawn (scenes 21-23) is a fixed
conversion, 1 unit on screen = 20 micrometres of axon, so the 35-micrometre ruler and the cut
positions are to scale with each other.

COLOR MAP (one color per concept, whole chapter series; taken from scenes.old.py)
  YELLOW = the axon, axonal proteins (channels), and the neurite that wins and becomes the axon
  BLUE   = dendrites and dendrite proteins (MAP2, receptors, spines)
  GREY   = cell body, outlines, the dish, membranes, neurites that have not been chosen
  GREEN  = PIP3 and positive feedback (not used in this chapter)
  RED    = a block, the cut, a lowered level, "held back"
  ORANGE = actin
  TEAL   = microtubules (the tracks)
  PURPLE = ankyrin G, the axon initial segment, the gate
  MAG    = beta-IV spectrin (new in this chapter; used only for that protein)
  GOLD   = guide text and questions (not a biological concept)
"""
import numpy as np
from types import SimpleNamespace
from bp_style import *  # noqa: F401,F403

PURPLE = "#B58CD9"
ORANGE = "#F29E4C"
MAG = "#E070B0"
SOMA_FILL = "#262b36"
PILL_FILL = "#2f2640"

C0 = np.array([-2.4, -0.1, 0.0])                 # cell body of the whole mature neuron
FULL_D = [(112, 2.1), (155, 2.2), (205, 2.1), (250, 2.0)]
YA = [25, 95, 165, 230, 305]


def u(deg):
    a = np.radians(deg)
    return np.array([np.cos(a), np.sin(a), 0.0])


def P(x, y):
    return np.array([x, y, 0.0])


def pdot(p, col=BLUE, r=.11):
    return Dot(p, radius=r, color=col).set_stroke(BG, width=2.5, opacity=1)


def lab(text, col=TEXT, size=26, pos=(0, 0), **kw):
    return T(text, max(size, 26), col, **kw).move_to([pos[0], pos[1], 0])


def _base(m):
    if not hasattr(m, "_b"):
        m._b = (m.get_fill_opacity(), m.get_stroke_opacity())
    return m._b


def fx(mob, f):
    out = []
    for m in mob.family_members_with_points():
        b = _base(m)
        out.append(m.animate.set_fill(opacity=b[0] * f).set_stroke(opacity=b[1] * f))
    return out


def setf(mob, f):
    for m in mob.family_members_with_points():
        b = _base(m)
        m.set_fill(opacity=b[0] * f).set_stroke(opacity=b[1] * f)
    return mob


# ---------------------------------------------------------------------------------------------
# the whole neuron (same model as chapter 1)
# ---------------------------------------------------------------------------------------------
def tube(pts, ws, color):
    pts = [np.array(p, float) for p in pts]
    n = len(pts)
    left, right = [], []
    for i, p in enumerate(pts):
        d = pts[1] - pts[0] if i == 0 else (pts[-1] - pts[-2] if i == n - 1 else pts[i + 1] - pts[i - 1])
        d = d / (np.linalg.norm(d) + 1e-9)
        nr = np.array([-d[1], d[0], 0.0])
        w = max(ws[i], 0.03)
        left.append(p + nr * w / 2)
        right.append(p - nr * w / 2)
    return Polygon(*(left + right[::-1]), stroke_width=0, fill_color=color, fill_opacity=1)


def arbor(c, ang, trunk, s, R, color):
    d = u(ang)
    p0 = c + d * R * 0.8
    pm = p0 + u(ang + 4) * trunk * s * 0.5
    p1 = pm + u(ang - 5) * trunk * s * 0.5
    trunk_poly = tube([p0, pm, p1], [0.26 * s, 0.17 * s, 0.10 * s], color)
    twigs = VGroup()
    ends = []
    for sg in (-1, 1):
        a = ang + sg * 34
        be = pm + u(a) * trunk * s * 0.42
        twigs.add(tube([pm, be], [0.14 * s, 0.07 * s], color))
        for sg2 in (-1, 1):
            a2 = a + sg2 * 30
            e2 = be + u(a2) * trunk * s * 0.17
            twigs.add(tube([be, e2], [0.07 * s, 0.03 * s], color))
            ends.append((e2, a2))
    ends.append((p1, ang - 5))
    return VGroup(trunk_poly, twigs), ends


class Neu:
    def __init__(self, c=C0, s=1.12, dends=FULL_D, axon_len=8.2, R=0.8, wob=0.1, axw=13, t1=1.0):
        self.c = np.array([c[0], c[1], 0.0])
        self.s = s
        self.R = R * s
        self.L = axon_len
        self.wob = wob * s
        self.axw = axw
        self.soma = Circle(radius=self.R, stroke_color=GREY, stroke_width=max(2.0, 4 * s),
                           fill_color=SOMA_FILL, fill_opacity=1).move_to(self.c)
        self.dends, self.ends = [], []
        for ang, tl in dends:
            g, e = arbor(self.c, ang, tl, s, self.R, BLUE)
            self.dends.append(g)
            self.ends.append(e)
        self.dgroup = VGroup(*self.dends)
        self.axon = self.piece(0, t1)
        self.group = VGroup(self.axon, self.dgroup, self.soma)

    def pt(self, t):
        x = self.c[0] + self.R * 0.9 + t * self.L
        return np.array([x, self.c[1] + self.wob * np.sin(1.1 * (x - self.c[0]) / self.s), 0.0])

    def piece(self, t0, t1, color=YELLOW, w=None):
        return ParametricFunction(self.pt, t_range=[t0, t1, (t1 - t0) / 80], color=color,
                                  stroke_width=w or self.axw)

    def outer(self, i):
        return max(self.ends[i], key=lambda e: np.linalg.norm(e[0] - self.c))


def full_neuron():
    return Neu()


AIS_T = 0.2                                        # the initial segment: first fifth of the drawn axon


def ais_piece(n, t1=AIS_T):
    return n.piece(0, t1, PURPLE, w=28)


def cutmark(p, h=0.5, w=5):
    return DashedLine(p + UP * h, p + DOWN * h, color=RED, stroke_width=w, dash_length=0.12)




def left_text(text, col, size, x_left, y):
    t = lab(text, col, size, (0, y))
    return t.align_to(P(x_left, 0), LEFT)


def leader(a, b, col, w=3):
    a, b = np.array(a, float)[:2], np.array(b, float)[:2]
    return Line(P(*a), P(*b), color=col, stroke_width=w)


def xmark(x, y, r=.24, col=RED, w=7):
    return VGroup(Line(P(x - r, y - r), P(x + r, y + r), color=col, stroke_width=w),
                  Line(P(x - r, y + r), P(x + r, y - r), color=col, stroke_width=w))


# ---------------------------------------------------------------------------------------------
# the zoom stage: soma, dendrite stub and the first stretch of axon, drawn large
# ---------------------------------------------------------------------------------------------
ZY, ZR, ZCX, AXH = -0.45, 2.5, -5.1, 1.4
ZTOP, ZBOT = ZY + AXH, ZY - AXH
ZX0 = ZCX + np.sqrt(ZR ** 2 - AXH ** 2)
ZXE = 6.8
CX0, CX1 = -2.6, 2.4                                # the collar (initial segment) spans these x


def hollow(p0, p1, w0, w1, color, sw=6):
    p0, p1 = np.array(p0, float), np.array(p1, float)
    d = (p1 - p0) / np.linalg.norm(p1 - p0)
    nr = np.array([-d[1], d[0], 0.0])
    L0, R0, L1, R1 = p0 + nr * w0, p0 - nr * w0, p1 + nr * w1, p1 - nr * w1
    lumen = Polygon(L0, L1, R1, R0, stroke_width=0, fill_color=color, fill_opacity=.08)
    walls = VGroup(Line(L0, L1, color=color, stroke_width=sw), Line(R0, R1, color=color, stroke_width=sw))
    return lumen, walls


class Z:
    def __init__(self):
        c = P(ZCX, ZY)
        self.lumen = Rectangle(width=ZXE - ZX0, height=2 * AXH, stroke_width=0, fill_color=YELLOW,
                               fill_opacity=.08).move_to([(ZX0 + ZXE) / 2, ZY, 0])
        dl, dw = hollow(P(-5.1, 1.6), P(-4.3, 3.65), .5, .35, BLUE)
        self.dend = VGroup(dl, dw)
        self.soma_fill = Circle(radius=ZR, stroke_width=0, fill_color=SOMA_FILL, fill_opacity=1).move_to(c)
        a0 = np.arcsin(AXH / ZR)
        self.soma_arc = Arc(radius=ZR, start_angle=a0, angle=2 * PI - 2 * a0, arc_center=c, color=GREY, stroke_width=5)
        self.tp = Line(P(ZX0, ZTOP), P(CX1, ZTOP), color=YELLOW, stroke_width=6)
        self.td = Line(P(CX1, ZTOP), P(ZXE, ZTOP), color=YELLOW, stroke_width=6)
        self.bp = Line(P(ZX0, ZBOT), P(CX1, ZBOT), color=YELLOW, stroke_width=6)
        self.bd = Line(P(CX1, ZBOT), P(ZXE, ZBOT), color=YELLOW, stroke_width=6)
        self.sleeve = RoundedRectangle(corner_radius=.3, width=CX1 - CX0, height=2 * AXH + .5, stroke_color=PURPLE,
                                       stroke_width=6, fill_color=PURPLE, fill_opacity=.2).move_to([(CX0 + CX1) / 2, ZY, 0])
        self.cell = VGroup(self.lumen, self.soma_fill, self.soma_arc, self.tp, self.td, self.bp, self.bd)

    def build(self, scene, dend=False, collar=False):
        if collar:
            scene.add(self.sleeve)
        if dend:
            scene.add(self.dend)
        scene.add(self.cell)
        return self


COLLAR_LABEL = (-0.1, 1.75)


def collar_label():
    return lab("axon initial segment", PURPLE, 28, COLLAR_LABEL)


def zoom_to_stage(scene, group, pt, c_old, r_old, t_scale=.9, t_swap=.3, zmobs=(), also_fade=()):
    """Animate the whole drawing growing about the axon base until its soma matches the zoom stage, then swap
    in the zoom stage (hollow axon) with a short cross-fade."""
    k = ZR / r_old
    tgt = P(ZCX + (pt[0] - c_old[0]) * k, ZY)
    scene.play(group.animate.scale(k, about_point=pt).shift(tgt - pt), *[FadeOut(m) for m in also_fade],
               run_time=t_scale, rate_func=rate_functions.ease_in_out_sine)
    scene.play(FadeOut(group), *[FadeIn(m) for m in zmobs], run_time=t_swap)


# ---------------------------------------------------------------------------------------------
# scene 0: title
# ---------------------------------------------------------------------------------------------
class S00Title(TitleCard):
    LESSON = "One Axon, Many Dendrites: Neuronal Polarity"
    TITLE = "The Gate, and the Race Reopened"


# ---------------------------------------------------------------------------------------------
# s01: the question
# ---------------------------------------------------------------------------------------------
class S01(SpokenScene):
    def construct(self):
        n = full_neuron()
        self.play(FadeIn(n.group), run_time=.4)
        self.at("axon has been")
        self.play(Indicate(n.axon, color=TEXT, scale_factor=1.15), run_time=.8)
        starts = [(155, 1.3), (205, 1.5), (112, 1.4), (250, 1.3), (155, 1.9), (205, 1.9), (112, 1.9), (250, 1.8)]
        dots = VGroup(*[pdot(n.c + u(a) * d) for a, d in starts])
        self.add(dots)
        self.play(FadeIn(dots, scale=1.5), run_time=.4)
        self.at("what keeps")
        # the dendrite proteins drift toward the base of the axon and stop there, crowding the soma side
        ends = [(-1.62 + .42 * (k // 4), -0.1 + (1 if k % 2 else -1) * (.45 + .38 * ((k % 4) // 2))) for k in range(8)]
        self.play(*[d.animate.move_to(P(*e)) for d, e in zip(dots, ends)], run_time=1.8, rate_func=rate_functions.ease_in_out_sine)
        self.at("wandering into")
        q = lab("?", GOLD, 110, (-0.2, 1.4), font=TITLE_FONT)
        self.play(FadeIn(q, scale=.6), *[d.animate.shift(RIGHT * .25) for d in dots[::2]], run_time=.7)
        self.finish()


# ---------------------------------------------------------------------------------------------
# s02: zoom to the proximal axon, a collar appears
# ---------------------------------------------------------------------------------------------
def bracket_mobs():
    br = DoubleArrow(P(CX0, -2.7), P(CX1, -2.7), buff=0, color=GREY, stroke_width=3, tip_length=.18)
    bl = lab("first few tens of micrometres", GREY, 26, (-0.1, -3.25))
    return br, bl


class S02(SpokenScene):
    def construct(self):
        n = full_neuron()
        self.add(n.group)
        z = Z()
        zoom_to_stage(self, n.group, n.pt(.04), n.c, n.R, t_scale=.9, t_swap=.3, zmobs=[z.cell])
        self.at("micrometers")
        br, bl = bracket_mobs()
        self.play(GrowFromCenter(br), FadeIn(bl), run_time=.7)
        self.at("form the")
        self.play(GrowFromEdge(z.sleeve, LEFT), run_time=.8)
        self.at("axon initial segment")
        self.play(FadeIn(collar_label(), shift=UP * .1), run_time=.5)
        self.finish()


# ---------------------------------------------------------------------------------------------
# the cutaway of the membrane (s03, s04, s05)
# ---------------------------------------------------------------------------------------------
MEM_Y0, MEM_Y1 = 1.30, 1.80
COAT_Y0 = -0.90
PILL_X = [-4.8, -2.4, 0.0, 2.4, 4.8]
RING_X = [-6.0, -3.6, -1.2, 1.2, 3.6, 6.0]
PILL_Y = 0.35
ROD_Y = -2.2
ANK_LAB = (1.2, -1.15)


def membrane_bar():
    return Rectangle(width=12.8, height=MEM_Y1 - MEM_Y0, stroke_width=0, fill_color=GREY,
                     fill_opacity=.95).move_to([0, (MEM_Y0 + MEM_Y1) / 2, 0])


def interior():
    return Rectangle(width=12.8, height=3.0, stroke_width=0, fill_color=YELLOW, fill_opacity=.05).move_to([0, COAT_Y0 - 1.5, 0])


def coat_band():
    band = Rectangle(width=12.8, height=MEM_Y0 - COAT_Y0, stroke_width=1.5, stroke_color=PURPLE, stroke_opacity=.5,
                     fill_color=PURPLE, fill_opacity=.22).move_to([0, (MEM_Y0 + COAT_Y0) / 2, 0])
    rng = np.random.RandomState(8)
    dots = VGroup()
    while len(dots) < 110:
        x, y = rng.uniform(-6.2, 6.2), rng.uniform(COAT_Y0 + .1, MEM_Y0 - .1)
        if any(abs(x - px) < .95 and y < PILL_Y + .6 and y > PILL_Y - .6 for px in PILL_X):
            continue
        dots.add(Dot([x, y, 0], radius=.05, color=PURPLE).set_opacity(.6))
    return VGroup(band, dots)


def pill(x):
    box = RoundedRectangle(corner_radius=.28, width=1.6, height=.9, stroke_color=PURPLE, stroke_width=3,
                           fill_color=PILL_FILL, fill_opacity=1)
    return VGroup(box).move_to([x, PILL_Y, 0])


def pills():
    return VGroup(*[pill(x) for x in PILL_X])


def ank_label():
    t = lab("ankyrin G", PURPLE, 28, ANK_LAB)
    l = leader((ANK_LAB[0] - .35, ANK_LAB[1] + .27), (PILL_X[2] + .55, PILL_Y - .46), PURPLE)
    return VGroup(t, l)


def spectrin_links():
    links = VGroup(*[Line(P(x, PILL_Y - .45), P(x, ROD_Y), color=PURPLE, stroke_width=4).set_z_index(3) for x in PILL_X])
    rods = VGroup(*[Line(P(a, ROD_Y), P(b, ROD_Y), color=MAG, stroke_width=11).set_z_index(2)
                    for a, b in zip(RING_X[:-1], RING_X[1:])])
    return links, rods


def rings():
    return VGroup(*[RoundedRectangle(corner_radius=.1, width=.3, height=1.4, stroke_width=0, fill_color=ORANGE,
                                     fill_opacity=1).move_to([x, ROD_Y, 0]).set_z_index(1) for x in RING_X])


def inset():
    """small map of where the cutaway is taken: the axon with its collar, a dashed cut line through it"""
    frame = RoundedRectangle(corner_radius=.12, width=2.3, height=1.15, stroke_color=GREY, stroke_width=2).move_to([5.55, 3.2, 0])
    ax = Rectangle(width=2.0, height=.42, stroke_color=YELLOW, stroke_width=3, fill_color=YELLOW, fill_opacity=.1).move_to([5.55, 3.2, 0])
    sl = Rectangle(width=1.0, height=.58, stroke_color=PURPLE, stroke_width=3, fill_color=PURPLE, fill_opacity=.3).move_to([5.1, 3.2, 0])
    cut = DashedLine(P(5.1, 2.75), P(5.1, 3.65), color=TEXT, stroke_width=3, dash_length=.08)
    return VGroup(frame, ax, sl, cut)


class S03(SpokenScene):
    def construct(self):
        z = Z()
        z.build(self, dend=False, collar=True)
        lbl = collar_label()
        br, bl = bracket_mobs()
        self.add(lbl, br, bl)
        # A taller cutaway fills the stage while retaining the same molecular schematic.
        def cutaway(m):
            return m.stretch(1.4, 1, about_point=P(0, MEM_Y1))
        mem = cutaway(membrane_bar())
        coat = cutaway(coat_band())
        pl = cutaway(pills())
        ml = lab("membrane", GREY, 28, (-4.5, 2.4))
        old = VGroup(z.cell, z.sleeve, lbl, br, bl)
        self.play(FadeOut(old), FadeIn(mem), FadeIn(ml), FadeIn(inset()),
                  FadeIn(cutaway(interior())), run_time=.4)
        self.at("dense coat", lead=.45)
        self.play(FadeIn(coat), run_time=.35)
        cl = lab("dense coat", PURPLE, 28, (-3.6, -2.7))
        cl_line = leader((-3.6, -2.43), (-3.6, -.44), PURPLE)
        self.play(FadeIn(cl), Create(cl_line), run_time=.3)
        self.at("built on")
        self.play(LaggedStart(*[FadeIn(p, scale=.7) for p in pl], lag_ratio=.15), run_time=1.0)
        self.at("ancurin")
        self.play(FadeIn(cutaway(ank_label())), run_time=.5)
        self.finish()


class S04(SpokenScene):
    def construct(self):
        mem, coat, pl = membrane_bar(), coat_band(), pills()
        ml = lab("membrane", GREY, 28, (-4.5, 2.4))
        self.add(interior(), mem, coat, pl, ml, ank_label())
        links, rods = spectrin_links()
        rg = rings()
        self.at("binds")
        self.play(Create(links), run_time=.6)
        self.at("beta")
        self.play(Create(rods), run_time=.7)
        bl = lab("beta-IV spectrin", MAG, 28, (3.4, -3.5))
        bll = leader((3.0, -3.25), (3.0, ROD_Y - .08), MAG)
        self.play(FadeIn(bl), Create(bll), run_time=.5)
        self.at("rings of actin")
        self.play(LaggedStart(*[FadeIn(r, scale=.5) for r in rg], lag_ratio=.1), run_time=.9)
        al = lab("rings of actin", ORANGE, 28, (-3.6, -3.5))
        all_ = leader((-3.6, -3.25), (-3.6, ROD_Y - .72), ORANGE)
        self.play(FadeIn(al), Create(all_), run_time=.4)
        self.finish()


def channel_na(x, y, col=YELLOW):
    return VGroup(*[Rectangle(width=.2, height=.8, stroke_width=0, fill_color=col, fill_opacity=1).move_to([x + s * .17, y, 0])
                    for s in (-1, 1)])


def channel_k(x, y, col=YELLOW):
    return VGroup(RoundedRectangle(corner_radius=.12, width=.55, height=.8, stroke_color=col, stroke_width=4,
                                   fill_color=col, fill_opacity=.35).move_to([x, y, 0]),
                  Line(P(x, y - .3), P(x, y + .3), color=col, stroke_width=4))


def neurofascin(x, y, col=YELLOW):
    return VGroup(Line(P(x, y - .4), P(x, y + .1), color=col, stroke_width=5),
                  Circle(radius=.17, stroke_width=0, fill_color=col, fill_opacity=1).move_to([x, y + .2, 0]))


def dock(x):
    return Line(P(x, PILL_Y + .45), P(x, MEM_Y0), color=PURPLE, stroke_width=5)


class S05(SpokenScene):
    def construct(self):
        mem, coat, pl = membrane_bar(), coat_band(), pills()
        links, rods = spectrin_links()
        rg = rings()
        low = VGroup(links, rods, rg)
        self.add(interior(), mem, coat, low, pl, ank_label())
        ym = (MEM_Y0 + MEM_Y1) / 2
        self.at("through its")
        self.play(FadeOut(low), run_time=.5)
        self.at("repeats")
        bumps = VGroup()
        for x in PILL_X:
            for dx in (-.55, -.3, .3, .55):
                bumps.add(Square(side_length=.15, stroke_width=0, fill_color=TEXT, fill_opacity=1)
                          .move_to([x + dx, PILL_Y - .52, 0]))
        al = lab("ankyrin repeats", TEXT, 28, (-3.1, -1.15))
        all_ = leader((-2.75, -.92), (-2.7, PILL_Y - .62), TEXT)
        self.play(FadeIn(bumps), FadeIn(al), Create(all_), run_time=.7)
        self.at("sodium channels")
        na = VGroup(*[VGroup(dock(x), channel_na(x, ym + .05)) for x in PILL_X[:2]])
        self.play(FadeIn(na, shift=DOWN * .3), FadeIn(lab("sodium channels", YELLOW, 28, (-3.6, 2.5))), run_time=.7)
        self.at("potassium channels")
        kc = VGroup(*[VGroup(dock(x), channel_k(x, ym + .05)) for x in PILL_X[2:4]])
        self.play(FadeIn(kc, shift=DOWN * .3), FadeIn(lab("KCNQ2/3", YELLOW, 28, (1.2, 2.5))), run_time=.7)
        self.at("and", nth=1)
        nf = VGroup(dock(PILL_X[4]), neurofascin(PILL_X[4], ym + .05))
        self.play(FadeIn(nf, shift=DOWN * .3), FadeIn(lab("neurofascin-186", YELLOW, 28, (4.9, 2.5))), run_time=.7)
        self.finish()


# ---------------------------------------------------------------------------------------------
# s06: the two jobs (cards); s09 comes back to them
# ---------------------------------------------------------------------------------------------
def numeral(k, x, y):
    return VGroup(Circle(radius=.5, stroke_width=0, fill_color=GOLD, fill_opacity=1),
                  T(str(k), 44, BG, weight=BOLD)).move_to([x, y, 0])


def bolt(x, y, s=1.0):
    pts = [(0.15, 1.0), (-0.45, 0.0), (-0.05, 0.0), (-0.2, -1.0), (0.5, 0.2), (0.1, 0.2)]
    return Polygon(*[P(x + px * s, y + py * s) for px, py in pts], stroke_width=0, fill_color=YELLOW, fill_opacity=1)


CARD_Y = 0.75


def job_cards():
    c1 = RoundedRectangle(corner_radius=.3, width=6.0, height=5.6, stroke_color=GOLD, stroke_width=3).move_to([-3.4, CARD_Y, 0])
    c2 = c1.copy().move_to([3.4, CARD_Y, 0])
    n1, n2 = numeral(1, -3.4, CARD_Y + 1.85), numeral(2, 3.4, CARD_Y + 1.85)
    t1 = T("Electrical", 46, TEXT, TITLE_FONT).move_to([-3.4, CARD_Y + .55, 0])
    t2 = T("Holding\npolarity", 46, TEXT, TITLE_FONT).move_to([3.4, CARD_Y + .45, 0])
    ic1 = bolt(-3.4, CARD_Y - 1.3, 1.0)
    return SimpleNamespace(c1=c1, c2=c2, n1=n1, n2=n2, t1=t1, t2=t2, ic1=ic1,
                           g1=VGroup(c1, n1, t1, ic1), g2=VGroup(c2, n2))


class S06(SpokenScene):
    def construct(self):
        k = job_cards()
        self.play(Create(k.c1), Create(k.c2), FadeIn(k.n1), FadeIn(k.n2), run_time=.8)
        self.at("first is")
        self.play(Write(k.t1), run_time=.6)
        self.at("electrical")
        self.play(FadeIn(k.ic1, scale=.6), run_time=.5)
        self.finish()


# ---------------------------------------------------------------------------------------------
# s07, s08: sodium channels and the spike (zoom stage)
# ---------------------------------------------------------------------------------------------
def na_pair(x, y):
    return VGroup(*[Rectangle(width=.1, height=.5, stroke_width=0, fill_color=YELLOW, fill_opacity=1)
                    .move_to([x + s * .09, y, 0]) for s in (-1, 1)])


def collar_channels(dense=True):
    g = VGroup()
    for x in np.linspace(CX0 + .35, CX1 - .35, 9):
        for y in (ZTOP, ZBOT):
            g.add(na_pair(x, y))
    return g


def sparse_channels():
    g = VGroup()
    for x, y in ((4.0, ZTOP), (5.6, ZTOP), (4.8, ZBOT)):
        g.add(na_pair(x, y))
    return g


GX = 3.2                    # voltage gauge: x of the bar
G_REST, G_THR_HI, G_THR_LO = 1.8, 3.0, 2.3


class S07(SpokenScene):
    def construct(self):
        z = Z()
        z.build(self, dend=False, collar=True)
        lbl = collar_label()
        self.add(lbl)
        self.at("high density")
        ch, sp = collar_channels(), sparse_channels()
        self.play(LaggedStart(*[FadeIn(c, scale=1.6) for c in ch], lag_ratio=.05), FadeIn(sp), run_time=1.2)
        sl = lab("sodium channels", YELLOW, 28, (-0.1, -2.7))
        self.play(FadeIn(sl), run_time=.4)
        self.at("gives it")
        # Adjacent to the collar: a schematic voltage column and visible depolarization gap.
        gx, bottom, rest_y, high_y, low_y = .8, -1.45, -.8, .55, -.05
        bar = Rectangle(width=.65, height=2.3, stroke_color=GREY, stroke_width=3,
                        fill_color=GREY, fill_opacity=.12).move_to([gx, -.3, 0])
        fill = Rectangle(width=.59, height=rest_y-bottom, stroke_width=0,
                         fill_color=YELLOW, fill_opacity=.6).move_to([gx, (bottom+rest_y)/2, 0])
        bt = lab("membrane voltage", TEXT, 28, (3.75, 1.5))
        rest = Line(P(gx-.45, rest_y), P(gx+.5, rest_y), color=GREY, stroke_width=4)
        rest_l = left_text("resting", GREY, 28, 2.3, rest_y)
        thr = DashedLine(P(gx-.45, high_y), P(gx+.5, high_y), color=GOLD, stroke_width=4, dash_length=.12)
        thr_l = left_text("threshold", GOLD, 28, 2.3, high_y)
        gap = DoubleArrow(P(1.7, rest_y), P(1.7, high_y), buff=0, color=GOLD,
                          stroke_width=4, tip_length=.14)
        self.play(FadeIn(bar), FadeIn(fill), FadeIn(bt), Create(rest), FadeIn(rest_l),
                  Create(thr), FadeIn(thr_l), GrowFromCenter(gap), run_time=.7)
        self.at("low threshold")
        small_gap = DoubleArrow(P(1.7, rest_y), P(1.7, low_y), buff=0, color=GOLD,
                                stroke_width=4, tip_length=.14)
        self.play(thr.animate.shift(DOWN*(high_y-low_y)), thr_l.animate.shift(DOWN*(high_y-low_y)),
                  Transform(gap, small_gap), run_time=.9)
        self.play(FadeIn(lab("small rise to threshold", GOLD, 26, (0.0, -3.3))), run_time=.3)
        self.finish()


class S08(SpokenScene):
    def construct(self):
        z = Z()
        z.build(self, dend=False, collar=True)
        lbl = collar_label()
        ch, sp = collar_channels(), sparse_channels()
        self.add(lbl, ch, sp)
        l1 = lab("in many neurons,", GOLD, 28, (0.0, -2.8))
        l2 = lab("the action potential starts here", TEXT, 28, (0.0, -3.3))
        self.at("many neurons")
        self.play(FadeIn(l1), run_time=.5)
        self.at("this is where")
        px = 1.7
        self.play(Flash(P(px, ZY), color=TEXT, line_length=.5, flash_radius=1.0, num_lines=14), FadeIn(l2), run_time=.7)
        self.at("action potential")
        band = Rectangle(width=.55, height=2 * AXH - .1, stroke_width=0, fill_color=YELLOW, fill_opacity=.55).move_to([px, ZY, 0])
        core = Rectangle(width=.2, height=2 * AXH - .1, stroke_width=0, fill_color=TEXT, fill_opacity=.95).move_to([px, ZY, 0])
        pulse = VGroup(band, core)
        self.add(pulse)
        self.play(pulse.animate.shift(RIGHT * 5.5), run_time=1.6, rate_func=linear)
        self.play(FadeOut(pulse), run_time=.2)
        self.finish()


# ---------------------------------------------------------------------------------------------
# s09 - s12: the bead experiment, on a close-up membrane stage (dendrite, cell body, collar)
# ---------------------------------------------------------------------------------------------
CITE_Y = -2.65
BM_Y = -0.4                   # the membrane line
BY = 0.8                      # bead centre height
BEAD_R = .7
BX0, BX1 = -5.9, 0.9          # glide path of the bead
IS_X0, IS_X1 = 0.4, 5.6


class S09(SpokenScene):
    def construct(self):
        k = job_cards()
        self.add(k.g1, k.g2)
        self.at("1999")
        self.play(*fx(k.g1, .4), FadeIn(k.t2), run_time=.6)
        self.at("bettina")
        names = lab("Winckler, Forscher and Mellman, 1999", TEXT, 28, (0, CITE_Y))
        self.play(FadeIn(names, shift=UP * .1), run_time=.6)
        self.at("membrane itself")
        mem = Line(P(2.0, CARD_Y - 1.3), P(4.8, CARD_Y - 1.3), color=GREY, stroke_width=10)
        bd = VGroup(*[Dot(P(2.35 + .3 * i, CARD_Y - 1.75 + (i % 2) * .65), radius=.09, color=BLUE) for i in range(3)])
        yd = VGroup(*[Dot(P(3.95 + .3 * i, CARD_Y - 1.75 + (i % 2) * .65), radius=.09, color=YELLOW) for i in range(3)])
        self.play(Create(mem), FadeIn(bd), FadeIn(yd), run_time=.6)
        self.at("divided there")
        div = Line(P(3.4, CARD_Y - 2.05), P(3.4, CARD_Y - .55), color=PURPLE, stroke_width=7)
        qq = lab("Is the membrane itself divided there?", GOLD, 28, (0, CITE_Y - .65))
        self.play(FadeIn(qq), Create(div), run_time=.6)
        self.finish()


def bead_stage():
    zones = VGroup()
    h = BM_Y + 3.8
    for x0, x1, col, op in ((-6.8, -3.6, BLUE, .16), (-3.6, IS_X0, GREY, .16), (IS_X0, IS_X1, PURPLE, .24)):
        zones.add(Rectangle(width=x1 - x0, height=h, stroke_width=0, fill_color=col, fill_opacity=op)
                  .move_to([(x0 + x1) / 2, BM_Y - h / 2, 0]))
    memb = Line(P(-6.8, BM_Y), P(6.8, BM_Y), color=GREY, stroke_width=11)
    names = VGroup(lab("dendrite", BLUE, 28, (-5.2, -3.4)), lab("cell body", TEXT, 28, (-1.6, -3.4)),
                   lab("axon initial segment", PURPLE, 28, (3.0, -3.4)))
    return VGroup(zones, memb, names)


def beam_poly(a, f):
    d = (f - a) / np.linalg.norm(f - a)
    nr = np.array([-d[1], d[0], 0.0])
    return [a, f + nr * .3, f - nr * .3, a]


class Rig:
    """a bead on a stalk attached to a membrane protein, held in a laser trap whose focus can run ahead of it"""
    def __init__(self, x0, off=.2):
        self.bx, self.pull, self.off = ValueTracker(x0), ValueTracker(0), off
        self.bead = Circle(radius=BEAD_R, stroke_color=TEXT, stroke_width=3, fill_color=TEXT, fill_opacity=.85)
        self.prot = Dot(radius=.16, color=BLUE).set_stroke(BG, 3)
        self.stalk = Line(P(0, 0), P(0, 1), color=BLUE, stroke_width=5)
        self.beam = Polygon(P(0, 3.8), P(.3, 0), P(-.3, 0), stroke_width=0, fill_color=TEXT, fill_opacity=.22)
        self.ring = Circle(radius=.95, stroke_color=TEXT, stroke_width=3)
        self.tether = DashedLine(P(0, 0), P(1, 0), color=TEXT, stroke_width=4)
        self.bead.add_updater(lambda m: m.move_to(P(self.bx.get_value(), BY)))
        self.prot.add_updater(lambda m: m.move_to(P(self.bx.get_value(), BM_Y)))
        self.stalk.add_updater(lambda m: m.put_start_and_end_on(P(self.bx.get_value(), BM_Y), P(self.bx.get_value(), BY - BEAD_R)))
        self.beam.add_updater(lambda m: m.set_points_as_corners(beam_poly(P(self.f()[0], 3.8), self.f())))
        self.ring.add_updater(lambda m: m.move_to(self.f()))
        self.tether.add_updater(lambda m: m.become(DashedLine(P(self.bx.get_value(), BY), self.f(), color=TEXT, stroke_width=4)))
        for m in (self.bead, self.prot, self.stalk, self.beam, self.ring, self.tether):
            m.update()

    def f(self):
        return P(self.bx.get_value() + self.off + self.pull.get_value() * 2.6, BY + self.pull.get_value() * .45)


class S10(SpokenScene):
    def construct(self):
        st = bead_stage()
        self.add(st)
        rig = Rig(-4.5)
        self.at("small beads")
        self.play(FadeIn(rig.prot), Create(rig.stalk), FadeIn(rig.bead, scale=.5), run_time=.6)
        self.at("membrane proteins")
        pl = lab("membrane protein", BLUE, 28, (-4.4, -1.5))
        pll = leader((-4.5, -1.22), (-4.5, BM_Y - .2), BLUE)
        self.play(FadeIn(pl), Create(pll), run_time=.5)
        self.at("dragged them")
        self.play(FadeIn(rig.beam), FadeIn(rig.ring), run_time=.5)
        self.at("laser trap")
        ll = lab("laser trap", TEXT, 28, (-1.9, 3.1))
        self.play(FadeIn(ll), rig.bx.animate.set_value(-3.9), run_time=.7)
        self.finish()


class S11(SpokenScene):
    def construct(self):
        st = bead_stage()
        self.add(st)
        rig = Rig(BX0)
        self.add(rig.prot, rig.stalk, rig.bead, rig.beam, rig.ring)
        self.play(rig.bx.animate.set_value(-1.4), run_time=2.2, rate_func=linear)
        self.at("moved freely")
        free = lab("moved freely", BLUE, 28, (-3.1, -1.6))
        self.play(FadeIn(free, run_time=.4), rig.bx.animate(run_time=1.7, rate_func=linear).set_value(BX1))
        self.at("initial segment")
        self.add(rig.tether)
        self.play(rig.pull.animate.set_value(1.0), run_time=.7)
        self.at("they were")
        hb = lab("held back", RED, 30, (2.9, -1.75))
        hl = leader((2.0, -1.45), (BX1 + .1, BM_Y - .2), RED)
        self.play(FadeIn(hb), Create(hl), run_time=.4)
        self.finish()


class S12(SpokenScene):
    def construct(self):
        st = bead_stage()
        rig = Rig(BX1)
        rig.pull.set_value(1.0)
        for m in (rig.bead, rig.prot, rig.stalk, rig.beam, rig.ring, rig.tether):
            m.update()
        hb = lab("held back", RED, 30, (2.9, -1.75))
        hl = leader((2.0, -1.45), (BX1 + .1, BM_Y - .2), RED)
        self.add(st, rig.prot, rig.stalk, rig.bead, rig.beam, rig.ring, rig.tether, hb, hl)
        self.at("depended on")
        ac = VGroup(*[Line(P(x, BM_Y - .12), P(x, BM_Y - .95), color=ORANGE, stroke_width=10)
                      for x in np.linspace(IS_X0 + .35, IS_X1 - .35, 8)])
        self.play(FadeOut(VGroup(hb, hl)), FadeIn(ac, scale=1.2), run_time=.7)
        al = lab("depends on actin", ORANGE, 30, (3.0, -2.0))
        all_ = leader((3.0, -1.75), (3.0, BM_Y - 1.0), ORANGE)
        self.play(FadeIn(al), Create(all_), run_time=.5)
        self.at("still argued")
        note = lab("how the barrier works: still argued", GOLD, 28, (-2.7, 3.2))
        self.play(FadeIn(note), run_time=.6)
        self.finish()


# ---------------------------------------------------------------------------------------------
# s13 - s16: the knockdown experiment on the whole neuron (enlarged: soma left, the axon fills the width)
# ---------------------------------------------------------------------------------------------
MID_C, MID_S = (-4.2, 0.1), 1.4
MID_D = [(112, 1.5), (158, 1.3), (202, 1.3), (250, 1.4)]
ANKB = (2.2, 3.0)                  # centre of the ankyrin G level bar
ANKB_W, ANKB_H = 2.8, .3


def mid_neuron():
    return Neu(c=MID_C, s=MID_S, dends=MID_D, axon_len=10.0, axw=30)


def mid_ais(n):
    return n.piece(0, .22, PURPLE, w=64)


def ank_gauge(frac, labels=True):
    title = lab("ankyrin G level", PURPLE, 28, (ANKB[0], ANKB[1] + .6))
    track = Rectangle(width=ANKB_W, height=ANKB_H, stroke_color=PURPLE, stroke_width=3, fill_opacity=0).move_to([ANKB[0], ANKB[1], 0])
    w = max(ANKB_W * frac, .01)
    fillr = Rectangle(width=w, height=ANKB_H, stroke_width=0, fill_color=PURPLE, fill_opacity=.9)
    fillr.move_to(track.get_left() + RIGHT * w / 2)
    ends = VGroup(lab("lowered", RED, 26, (ANKB[0] - ANKB_W / 2 + .65, ANKB[1] - .5)),
                  lab("normal", GREY, 26, (ANKB[0] + ANKB_W / 2 - .6, ANKB[1] - .5)))
    arrow = Arrow(P(ANKB[0] + ANKB_W / 2 + .4, ANKB[1] + .5), P(ANKB[0] + ANKB_W / 2 + .4, ANKB[1] - .25), buff=0,
                  color=RED, stroke_width=8, tip_length=.28)
    return SimpleNamespace(title=title, track=track, fill=fillr, ends=ends, arrow=arrow)


def ank_link(n):
    return DashedLine(P(ANKB[0] - ANKB_W / 2, ANKB[1] - .15), n.pt(.11) + UP * .4, color=PURPLE, stroke_width=3)


def dend_dots(n):
    dots = VGroup()
    for (ang, tl), k in zip(MID_D, range(4)):
        for j in range(4):
            dots.add(pdot(n.c + u(ang + (j % 3 - 1) * 8) * (n.R * .9 + .45 + j * .45), BLUE, .13))
    return dots


class S13(SpokenScene):
    def construct(self):
        n = mid_neuron()
        ais = mid_ais(n)
        self.add(ais, n.group)
        self.at("scaffold")
        g = ank_gauge(1.0)
        link = ank_link(n)
        self.play(FadeIn(g.title), Create(g.track), FadeIn(g.fill), Create(link), run_time=.8)
        self.at("lower")
        newfill = Rectangle(width=.7, height=ANKB_H, stroke_width=0, fill_color=PURPLE, fill_opacity=.9).move_to(g.track.get_left() + RIGHT * .35)
        self.play(Transform(g.fill, newfill), GrowArrow(g.arrow), FadeIn(g.ends), run_time=.9)
        self.at("initial segment has formed")
        isl = lab("initial segment", PURPLE, 28, (-2.2, -1.7))
        isll = leader((-2.2, -1.45), n.pt(.11) + DOWN * .4, PURPLE)
        self.play(FadeIn(isl), Create(isll), Indicate(ais, color=TEXT, scale_factor=1.15), run_time=.8)
        self.at("already chosen")
        al = lab("axon: already chosen", YELLOW, 28, (3.4, -1.3))
        all_ = leader((2.8, -1.05), (2.4, n.pt(.7)[1] - .2), YELLOW)
        self.play(FadeIn(al), Create(all_), Indicate(n.axon, color=TEXT, scale_factor=1.05), run_time=.8)
        self.finish()


Q1 = "What happens to the initial segment?"
Q2 = "Does MAP2 stay out of the axon?"


def s14_objects():
    """end state shared by s14, s15 (pause) and s16"""
    n = mid_neuron()
    ais = mid_ais(n)
    g = ank_gauge(.25)
    link = ank_link(n)
    dots = dend_dots(n)
    mlab = lab("MAP2", BLUE, 28, (-1.6, 2.9))
    mlead = leader((-2.1, 2.72), tuple(n.c + u(112) * (n.R * .9 + .45 + .45 * 2))[:2], BLUE)
    q1 = lab(Q1, GOLD, 30, (2.0, -2.55))
    q2 = lab(Q2, GOLD, 30, (2.0, -3.25))
    return SimpleNamespace(n=n, ais=ais, g=g, link=link, dots=dots, mlab=mlab, mlead=mlead, q1=q1, q2=q2)


def s14_base(scene, o):
    scene.add(o.ais, o.n.group, o.g.title, o.g.track, o.g.fill, o.g.ends, o.g.arrow, o.link)


class S14(SpokenScene):
    def construct(self):
        o = s14_objects()
        s14_base(self, o)
        self.at("what happens")
        self.play(Indicate(o.ais, color=TEXT, scale_factor=1.15), FadeIn(o.q1, shift=UP * .1), run_time=.8)
        self.at("does map2")
        self.play(FadeIn(o.dots, scale=1.4), FadeIn(o.mlab), Create(o.mlead), FadeIn(o.q2, shift=UP * .1), run_time=.8)
        self.at("stay out")
        self.finish()


class S15Pause(NarratedScene):
    def construct(self):
        o = s14_objects()
        s14_base(self, o)
        self.add(o.dots, o.mlab, o.mlead, o.q1, o.q2)
        self.finish()


class S16(SpokenScene):
    def construct(self):
        o = s14_objects()
        s14_base(self, o)
        self.add(o.dots, o.mlab, o.mlead, o.q1, o.q2)
        cite = lab("Hedstrom, Ogawa and Rasband, 2008", TEXT, 30, (2.0, -2.9))
        self.at("in 2008")
        self.play(FadeOut(VGroup(o.q1, o.q2)), FadeIn(cite, shift=DOWN * .1), run_time=.6)
        self.at("did this")
        self.play(Indicate(VGroup(o.g.track, o.g.fill), color=PURPLE, scale_factor=1.12), run_time=.8)
        self.finish()


# ---------------------------------------------------------------------------------------------
# s17 - s20: what happened, on the zoom stage
# ---------------------------------------------------------------------------------------------
def soma_dots():
    rng = np.random.RandomState(12)
    g = VGroup()
    while len(g) < 9:
        a, r = rng.uniform(0, 2 * PI), rng.uniform(0, 1.8)
        p = P(ZCX + r * np.cos(a), ZY + r * np.sin(a))
        if p[0] > -3.6:
            continue
        g.add(pdot(p))
    g.add(*[pdot(P(-5.1 + .8 * t, 1.6 + 2.0 * t), BLUE, .1) for t in (.2, .45, .7, .92)])
    return g


def axon_dots_final():
    pts = [(-2.7, -.1), (-2.3, -1.1), (-1.7, -.2), (-1.2, -1.1), (-.6, -.2), (0.0, -.7), (.7, -1.2), (1.1, -.1), (1.6, -1.1), (2.1, -.3)]
    return [P(x, y) for x, y in pts]


KEY_DOT = 5


def spine(x, y0, s):
    return VGroup(Line(P(x, y0), P(x, y0 + s * .45), color=BLUE, stroke_width=6),
                  Circle(radius=.2, stroke_color=BLUE, stroke_width=4, fill_color=BLUE, fill_opacity=.5).move_to([x, y0 + s * .62, 0]))


def spines():
    g = VGroup()
    for x in (-2.0, -1.0, 1.0, 2.0):
        g.add(spine(x, ZTOP, 1))
    for x in (-1.5, -0.5, 0.5, 1.5):
        g.add(spine(x, ZBOT, -1))
    return g


def map2_label():
    t = lab("MAP2", BLUE, 28, (0.0, 2.2))
    ld = leader((0.0, 1.95), (0.0, -.62), BLUE)
    return VGroup(t, ld)


def zstage_gauge():
    """the ankyrin G level bar, same place and size as on the whole-neuron stage"""
    g = ank_gauge(.25)
    return VGroup(g.title, g.track, g.fill, g.ends, g.arrow)


class S17(SpokenScene):
    def construct(self):
        o = s14_objects()
        s14_base(self, o)
        self.add(o.dots, o.mlab, o.mlead)
        z = Z()
        sd = soma_dots()
        grp = VGroup(o.ais, o.n.group, o.dots)
        self.play(FadeOut(VGroup(o.link, o.mlab, o.mlead)), run_time=.25)
        zoom_to_stage(self, grp, o.n.pt(.08), o.n.c, o.n.R, t_scale=.6, t_swap=.3, zmobs=[z.sleeve, z.dend, z.cell, sd])
        lbl = collar_label()
        self.add(lbl)
        self.at("fell apart")
        rng = np.random.RandomState(3)
        frags = VGroup()
        for k in range(16):
            x = CX0 + .2 + (CX1 - CX0 - .4) * k / 15
            y = ZTOP if k % 2 == 0 else ZBOT
            frags.add(RoundedRectangle(corner_radius=.05, width=.36, height=.16, stroke_width=0, fill_color=PURPLE, fill_opacity=.95).move_to([x, y, 0]))
        self.add(frags)
        self.play(FadeOut(z.sleeve), FadeOut(lbl),
                  *[f.animate.shift(RIGHT * rng.uniform(-.55, .55)).set_fill(opacity=0) for f in frags], run_time=1.3)
        self.at("spread into")
        ml = map2_label()
        finals = axon_dots_final()
        ad = VGroup(*[pdot(P(-3.3, ZY + np.random.RandomState(k).uniform(-.5, .5))) for k in range(len(finals))])
        self.add(ad)
        self.play(FadeIn(ml), *[d.animate.move_to(p) for d, p in zip(ad, finals)], run_time=1.4)
        self.finish()


def stage18(scene, blue_walls=True):
    z = Z()
    sd = soma_dots()
    ad = VGroup(*[pdot(p) for p in axon_dots_final()])
    gg = zstage_gauge()
    scene.add(z.dend, z.cell, sd, ad, gg)
    if blue_walls:
        z.tp.set_color(BLUE)
        z.bp.set_color(BLUE)
    return z, sd, ad, gg


class S18(SpokenScene):
    def construct(self):
        z, sd, ad, gg = stage18(self, blue_walls=False)
        ml = map2_label()
        self.add(ml)
        self.at("near the cell")
        self.play(z.tp.animate.set_color(BLUE), z.bp.animate.set_color(BLUE), run_time=.9)
        self.at("look like a dendrite")
        pl = lab("proximal axon", BLUE, 28, (-0.1, -3.2))
        self.play(FadeIn(pl), run_time=.4)
        self.at("dendritic spines")
        sp = spines()
        self.play(LaggedStart(*[GrowFromEdge(s, DOWN if s[1].get_center()[1] > ZY else UP) for s in sp], lag_ratio=.12), run_time=1.0)
        sl = lab("dendritic spines", BLUE, 28, (4.6, 1.85))
        sll = leader((3.3, 1.7), (2.25, 1.38), BLUE)
        self.play(FadeIn(sl), Create(sll), run_time=.4)
        self.finish()


def yellow_dots():
    rng = np.random.RandomState(9)
    return VGroup(*[Dot(P(3.9 + .36 * k + rng.uniform(-.08, .08), ZY + rng.uniform(-.55, .55)), radius=.11, color=YELLOW) for k in range(8)])


class S19(SpokenScene):
    def construct(self):
        z, sd, ad, gg = stage18(self)
        sp = spines()
        self.add(sp, map2_label())
        self.at("farther out")
        arr = Arrow(P(3.1, 1.45), P(6.5, 1.45), buff=0, color=GREY, stroke_width=4, tip_length=.22)
        fo = lab("farther out", GREY, 28, (4.8, 1.95))
        self.play(GrowArrow(arr), FadeIn(fo), run_time=.6)
        self.at("kept axonal")
        yd = yellow_dots()
        al = lab("axonal proteins", YELLOW, 28, (4.7, -2.55))
        all_ = leader((4.7, -2.25), (4.8, ZY - .75), YELLOW)
        self.play(FadeIn(yd, scale=1.5), FadeIn(al), Create(all_), run_time=.8)
        self.finish()


class S20(SpokenScene):
    def construct(self):
        z, sd, ad, gg = stage18(self)
        sp = spines()
        yd = yellow_dots()
        self.add(sp, yd)
        self.play(FadeOut(gg), *fx(VGroup(sd, z.dend), .4), *fx(sp, .5), *fx(yd, .3), run_time=.4)
        self.at("identity has")
        hd = lab("identity has to be actively held", GOLD, 34, (0, 3.3), font=TITLE_FONT)
        self.play(FadeIn(hd), run_time=.6)
        self.at("near the cell body")
        brp = DoubleArrow(P(CX0, 2.0), P(CX1, 2.0), buff=0, color=BLUE, stroke_width=3, tip_length=.16)
        pl = lab("proximal axon", BLUE, 28, (-0.1, 2.5))
        self.play(GrowFromCenter(brp), FadeIn(pl), run_time=.6)
        self.at("initial segment holds")
        sb = DoubleArrow(P(CX0, -2.85), P(CX1, -2.85), buff=0, color=PURPLE, stroke_width=5, tip_length=.2)
        hl = lab("initial segment holds it", PURPLE, 28, (-0.1, -3.4))
        self.play(GrowFromCenter(sb), FadeIn(hl), run_time=.8)
        self.at("farther out")
        brd = DoubleArrow(P(CX1 + .4, 2.0), P(6.6, 2.0), buff=0, color=YELLOW, stroke_width=3, tip_length=.16)
        dl = lab("distal axon", YELLOW, 28, (4.5, 2.5))
        self.play(GrowFromCenter(brd), FadeIn(dl), run_time=.6)
        self.at("something else")
        sh = lab("held by something else", YELLOW, 28, (4.4, -2.55))
        q = lab("?", GOLD, 90, (4.9, ZY + .05), font=TITLE_FONT)
        ni = lab("(not yet identified)", GOLD, 28, (4.4, -3.15))
        self.play(FadeIn(sh), FadeIn(ni), FadeIn(q, scale=.6), run_time=.5)
        self.at("not yet identified")
        self.finish()


# ---------------------------------------------------------------------------------------------
# s21 - s23: the mature neuron's cut. 1 unit = 20 micrometres
# ---------------------------------------------------------------------------------------------
ROW_Y = [1.4, -0.6, -2.6]
ROW_CUT_UM = [20, 70, 140]
UM = 1 / 20.0
ROW_D = [(50, 1.0), (115, .9), (180, .9)]
CITE_TXT = "Gomis-Rüth, Wierenga and Bradke, 2008"


class Row:
    def __init__(self, y, um):
        self.y = y
        self.um = um
        self.n = Neu(c=(-4.9, y), s=.8, dends=ROW_D, axon_len=11.0, wob=.0, axw=10, t1=1.0)
        self.x0 = self.n.pt(0)[0]
        self.tcut = um * UM / self.n.L
        self.stump = self.n.piece(0, self.tcut)
        self.distal = self.n.piece(self.tcut, 1.0)
        self.cutx = self.n.pt(self.tcut)[0]
        self.cm = cutmark(self.n.pt(self.tcut), .45)
        self.tag = lab(f"{um} µm", GOLD, 26, (self.cutx, y - .75))
        self.n.group.remove(self.n.axon)

    def pre(self):
        return VGroup(self.stump, self.distal, self.n.dgroup, self.n.soma)

    def post(self):
        return VGroup(self.stump, self.n.dgroup, self.n.soma, self.cm, self.tag)


def x35():
    return Row(0, 20).x0 + 35 * UM


def rows():
    return [Row(y, um) for y, um in zip(ROW_Y, ROW_CUT_UM)]


def ruler_mobs(x):
    ln = DashedLine(P(x, -3.3), P(x, 2.9), color=GOLD, stroke_width=4, dash_length=.15)
    x0 = Row(0, 20).x0
    bar = DoubleArrow(P(x0, -3.6), P(x, -3.6), buff=0, color=GOLD, stroke_width=4, tip_length=.15)
    return ln, bar


def cite21():
    return lab(CITE_TXT, TEXT, 28, (0, 3.55))


def mature_lab():
    return lab("mature neurons", TEXT, 26, (0, 3.05))


class S21(SpokenScene):
    def construct(self):
        rs = rows()
        cite = cite21()
        self.play(FadeIn(cite, shift=DOWN * .1), FadeIn(rs[0].pre()), FadeIn(rs[2].pre()), run_time=.7)
        self.at("made the mature")
        self.play(FadeIn(mature_lab()), FadeIn(rs[1].pre()), run_time=.5)
        self.at("neurons cut")
        self.play(*[FadeIn(r.cm) for r in rs], *[FadeIn(r.tag) for r in rs],
                  *[r.distal.animate.set_stroke(opacity=0).shift(RIGHT * .3 + DOWN * .2) for r in rs], run_time=.9)
        self.finish()


def regrown(rs):
    return [r.n.piece(r.tcut, r.tcut + 3.0 / r.n.L, YELLOW) for r in rs[1:]]


def regrow_labels(rs):
    return [lab("stump regrows", YELLOW, 26, (rs[1].cutx + 1.6, rs[1].y + .65)),
            lab("stump regrows", YELLOW, 26, (rs[2].cutx + 1.6, rs[2].y + .65))]


class S22(SpokenScene):
    def construct(self):
        rs = rows()
        self.add(cite21(), mature_lab(), *[r.post() for r in rs])
        X = x35()
        ln, bar = ruler_mobs(X)
        self.at("shorter than")
        self.play(Create(bar), run_time=.6)
        self.at("35")
        self.play(Create(ln), FadeIn(lab("35 µm", GOLD, 28, (X + 1.0, -3.6))), run_time=.6)
        self.play(FadeIn(short_stump_tag(rs[0])), run_time=.3)
        self.at("dendrite became")
        r1 = rs[0]
        d = r1.n.dends[0]
        p1 = r1.n.ends[0][-1][0]
        Ln = 1.5
        tr = ValueTracker(.05)
        line = Line(p1, p1 + RIGHT * .05, color=YELLOW, stroke_width=10)
        line.add_updater(lambda m: m.put_start_and_end_on(p1, p1 + RIGHT * tr.get_value()))
        self.play(Indicate(d, color=TEXT, scale_factor=1.1), run_time=.5)
        self.play(d.animate.set_color(YELLOW), run_time=.5)
        self.add(line)
        dl = lab("a dendrite becomes the axon", YELLOW, 26, (0, 0))
        dl.move_to([p1[0] + Ln + .2 + dl.width / 2, p1[1], 0])
        self.play(tr.animate.set_value(Ln), FadeIn(dl), run_time=.8, rate_func=rate_functions.ease_in_sine)
        self.at("longer stumps")
        regs = regrown(rs)
        self.play(*[Create(g) for g in regs], run_time=1.0)
        self.play(*[FadeIn(l) for l in regrow_labels(rs)], run_time=.4)
        self.finish()


def short_stump_tag(r):
    tag = lab("under\n35 µm", GOLD, 26, (0, 0))
    tag.move_to([(r.x0 + r.cutx)/2, r.y + .55, 0])
    tag.align_to(P(x35() - .12, 0), RIGHT)
    return tag


def s22_end(scene, rs):
    """end state of s22 (used by s23)"""
    X = x35()
    ln, bar = ruler_mobs(X)
    r1 = rs[0]
    d = r1.n.dends[0]
    p1 = r1.n.ends[0][-1][0]
    d.set_color(YELLOW)
    line = Line(p1, p1 + RIGHT * 1.5, color=YELLOW, stroke_width=10)
    regs = regrown(rs)
    dl = lab("a dendrite becomes the axon", YELLOW, 26, (0, 0))
    dl.move_to([p1[0] + 1.7 + dl.width / 2, p1[1], 0])
    rl = lab("35 µm", GOLD, 28, (X + 1.0, -3.6))
    allm = VGroup(cite21(), mature_lab(), *[r.post() for r in rs], ln, bar, rl, short_stump_tag(r1), line, *regs, dl, *regrow_labels(rs))
    scene.add(allm)
    return allm


MT_COL = "#FFF1B8"


class S23(SpokenScene):
    def construct(self):
        rs = rows()
        old = s22_end(self, rs)
        n = Neu(c=(-5.0, -0.45), s=1.25, dends=[(50, 1.0), (115, .9), (250, .9)], axon_len=12.0, wob=0, axw=22, t1=1.0)
        x0 = n.pt(0)[0]
        tcut = 7.0 / n.L
        stump = n.piece(0, tcut).set_stroke(opacity=.4)
        reg = n.piece(tcut, tcut + 3.0 / n.L).set_stroke(opacity=.4)
        cm = cutmark(n.pt(tcut), .5)
        n.group.remove(n.axon)
        big = VGroup(stump, reg, n.dgroup, n.soma, cm)
        self.play(FadeOut(old), FadeIn(big), run_time=.8)
        self.at("stable microtubules")
        xa, xb = x0 + 1.75, n.pt(tcut + 3.0 / n.L)[0]
        y0 = n.pt(0)[1]
        glow = Line(P(xa, y0), P(xb, y0), color=GOLD, stroke_width=26, stroke_opacity=.3)
        mts = VGroup(*[Line(P(xa, y0 + dy), P(xb, y0 + dy), color=MT_COL, stroke_width=3.5) for dy in (-.07, 0, .07)])
        self.play(Create(glow), Create(mts), run_time=.8)
        ml = lab("stable microtubules", MT_COL, 28, (1.2, 1.3))
        mll = leader((1.2, 1.03), (1.2, y0 + .16), MT_COL)
        self.play(FadeIn(ml), Create(mll), run_time=.4)
        self.at("distal axon")
        self.play(Indicate(VGroup(glow, mts), color=TEXT, scale_factor=1.1), run_time=.8)
        self.at("did not test")
        sl = RoundedRectangle(corner_radius=.15, width=1.5, height=.9, stroke_color=PURPLE, stroke_width=5, fill_color=PURPLE,
                              fill_opacity=.25).move_to([x0 + .85, y0, 0])
        nl = lab("initial segment: not tested", PURPLE, 28, (-1.2, -2.4))
        nll = leader((-2.8, -2.15), (x0 + .85, y0 - .48), PURPLE)
        self.play(FadeIn(sl, scale=.8), FadeIn(nl), Create(nll), run_time=.7)
        self.finish()


# ---------------------------------------------------------------------------------------------
# s24, s25: the two cards
# ---------------------------------------------------------------------------------------------
def cmp_cards():
    c1 = RoundedRectangle(corner_radius=.3, width=6.2, height=6.0, stroke_color=GOLD, stroke_width=3).move_to([-3.4, 0, 0])
    c2 = c1.copy().move_to([3.4, 0, 0])
    return c1, c2


YC = (-3.4, -0.2)
YR0 = .42


def y_dir(i):
    return u(YA[i])


def y_line(i, length, col=GREY):
    c = P(*YC)
    d = y_dir(i)
    return Line(c + d * YR0 * .7, c + d * (YR0 + length), color=col, stroke_width=10)


def y_soma():
    return Circle(radius=YR0, stroke_color=GREY, stroke_width=4, fill_color=SOMA_FILL, fill_opacity=1).move_to([YC[0], YC[1], 0])


LEAD_I, WIN_I = 2, 4


def young_final():
    """five equal neurites, one turned gold: where the race restarts"""
    ls = [y_line(i, 1.8, YELLOW if i == WIN_I else GREY) for i in range(5)]
    return VGroup(*ls, y_soma())


def mature_icon(cx, cy):
    n = Neu(c=(cx - 2.3, cy), s=.8, dends=[(35, 1.2), (105, 1.0), (250, 1.0)], axon_len=4.6, wob=0, axw=11)
    t = .15
    stump = n.piece(0, t)
    ghost = n.piece(t, 1.0).set_stroke(opacity=.3)
    cm = cutmark(n.pt(t), .55)
    n.group.remove(n.axon)
    return n, stump, ghost, cm


class S24(SpokenScene):
    def construct(self):
        c1, c2 = cmp_cards()
        c2.set_stroke(opacity=.3)
        self.add(c2, c1)
        self.at("young neuron's")
        t1 = T("A young neuron's cut", 36, TEXT, TITLE_FONT).move_to([-3.4, 2.4, 0])
        ls = [y_line(i, 1.8) for i in range(5)]
        c = P(*YC)
        d = y_dir(LEAD_I)
        tip = Line(c + d * (YR0 + 1.8), c + d * (YR0 + 2.5), color=GREY, stroke_width=10)
        ic = VGroup(*ls, tip, y_soma())
        self.play(FadeIn(t1), FadeIn(ic, scale=.8), run_time=.55)
        self.at("cut")
        cm = cutmark(c + d * (YR0 + 1.8), .4)
        self.play(FadeIn(cm), FadeOut(tip), run_time=.4)
        self.at("reopens")
        res = lab("the race reopens, easily", GOLD, 32, (-3.4, -2.55), font=TITLE_FONT)
        self.play(ls[WIN_I].animate.set_color(YELLOW), FadeIn(res, shift=UP * .1), run_time=.7)
        self.finish()


class S25(SpokenScene):
    def construct(self):
        c1, c2 = cmp_cards()
        t1 = T("A young neuron's cut", 36, TEXT, TITLE_FONT).move_to([-3.4, 2.4, 0])
        res = lab("the race reopens, easily", GOLD, 32, (-3.4, -2.55), font=TITLE_FONT)
        cm = cutmark(P(*YC) + y_dir(LEAD_I) * (YR0 + 1.8), .4)
        left = VGroup(c1, t1, young_final(), cm, res)
        self.add(left, c2)
        c2.set_stroke(opacity=.3)
        self.play(*fx(left, .4), c2.animate.set_stroke(opacity=1), run_time=.35)
        self.at("mature neuron's")
        t2 = T("A mature neuron's cut", 36, TEXT, TITLE_FONT).move_to([3.4, 2.4, 0])
        n, stump, ghost, cm2 = mature_icon(3.4, .45)
        self.play(FadeIn(t2), FadeIn(n.group), FadeIn(stump), FadeIn(ghost), run_time=.8)
        self.at("cut reopens")
        self.play(FadeIn(cm2), run_time=.4)
        self.at("only when")
        r1 = lab("only when almost the whole\naxon is removed", GOLD, 32, (3.4, -1.45), font=TITLE_FONT)
        self.play(FadeIn(r1, shift=UP * .1), run_time=.6)
        self.at("almost the whole")
        r2 = lab("below 35 µm, in these cultures", GREY, 26, (3.4, -2.65))
        self.play(FadeIn(r2), run_time=.5)
        self.finish()


# ---------------------------------------------------------------------------------------------
# s26 - s29: dish and brain
# ---------------------------------------------------------------------------------------------
SLICE_C = (-3.6, 0.0)
RCX = 3.4                      # centre of the right-hand text column
MIG0 = (-3.6, -0.85)
MIG1 = (-3.6, 1.45)
LIGHT = "#C9CEDA"


def dish_mob():
    return Ellipse(width=5.8, height=5.0, stroke_color=GREY, stroke_width=3).move_to([SLICE_C[0], SLICE_C[1], 0])


def slice_mob():
    frame = RoundedRectangle(corner_radius=.25, width=5.4, height=7.2, stroke_color=GREY, stroke_width=3).move_to([SLICE_C[0], SLICE_C[1], 0])
    bands = VGroup()
    ys = np.linspace(-3.6, 3.6, 7)
    for i in range(6):
        bands.add(Rectangle(width=5.4, height=7.2 / 6, stroke_width=0, fill_color=GREY, fill_opacity=.04 + .06 * (i % 2))
                  .move_to([SLICE_C[0], (ys[i] + ys[i + 1]) / 2, 0]))
    rng = np.random.RandomState(21)
    cells = VGroup(*[Dot(P(SLICE_C[0] + rng.uniform(-2.5, 2.5), rng.uniform(-3.4, 3.4)), radius=.04, color=GREY).set_opacity(.22) for _ in range(30)])
    return VGroup(bands, cells, frame)


def mig_arrow():
    return Arrow(P(-5.8, -2.3), P(-5.8, 2.5), buff=0, color=TEXT, stroke_width=7, tip_length=.35).set_opacity(.55)


class Young:
    def __init__(self, c=(0, 0), sc=1.0, lens=(2.3,) * 5, col=GREY):
        self.c = np.array([c[0], c[1], 0.0])
        self.R = 0.75 * sc
        self.dirs = [u(a) for a in YA]
        self.lines = VGroup(*[Line(self.c + d * self.R * .9, self.c + d * (self.R + l * sc), color=col, stroke_width=9 * max(sc, .65))
                              for d, l in zip(self.dirs, lens)])
        self.soma = Circle(radius=self.R, stroke_color=GREY, stroke_width=4, fill_color=SOMA_FILL, fill_opacity=1).move_to(self.c)
        self.group = VGroup(self.lines, self.soma)


def young_in_dish():
    return Young(c=(SLICE_C[0], SLICE_C[1]), sc=.85)


def brain_caution():
    return lab("In the brain,\nthe race may be\ntilted or skipped",
               GOLD, 38, (RCX, -1.25), font=TITLE_FONT)


class S26(SpokenScene):
    def construct(self):
        dish = dish_mob()
        y = young_in_dish()
        self.add(dish, y.group)
        self.at("one caution")
        cau = lab("One caution", GOLD, 44, (RCX, 3.0), font=TITLE_FONT)
        self.play(FadeIn(cau), run_time=.5)
        self.at("in a dish")
        dl = lab("This was all in a dish.", TEXT, 32, (RCX, 1.55))
        self.play(FadeIn(dl), run_time=.5)
        self.at("brain")
        self.play(FadeOut(dish), FadeOut(y.group), run_time=.3)
        sl = slice_mob()
        caution = brain_caution()
        self.play(FadeIn(sl), FadeIn(caution), *fx(dl, .5), run_time=.6)
        self.at("tilted")
        self.at("skipped")
        self.finish()


def migrant(cx, cy, trailing=GREY, lead=GREY):
    c = P(cx, cy)
    trail = Line(c + DOWN * .6, c + DOWN * 1.9, color=trailing, stroke_width=7)
    tip = c + UP * 1.55
    leadp = Line(c + UP * .6, tip, color=lead, stroke_width=12)
    fork = VGroup(*[Line(tip, tip + u(90 + s * 40) * .38, color=lead, stroke_width=7) for s in (-1, 1)])
    soma = Circle(radius=.7, stroke_color=GREY, stroke_width=4, fill_color=SOMA_FILL, fill_opacity=1).move_to(c)
    return VGroup(trail, leadp, fork, soma)


class S27(SpokenScene):
    def construct(self):
        sl = slice_mob()
        hd = lab("developing cortex", TEXT, 36, (RCX, 3.0), font=TITLE_FONT)
        cell = migrant(*MIG0)
        self.add(sl, cell, brain_caution())
        mv, last = ValueTracker(0), [0.0]

        def upd(m):
            v = mv.get_value()
            m.shift(UP * (v - last[0]))
            last[0] = v
        cell.add_updater(upd)

        def tlabel(txt, col):
            t = lab(txt, col, 28, (0, 0))
            t.add_updater(lambda m: m.move_to(cell[0].get_center() + RIGHT * (.5 + m.width / 2)))
            ln = Line(P(0, 0), P(1, 0), color=col, stroke_width=3)
            ln.add_updater(lambda m: m.put_start_and_end_on(cell[0].get_center() + RIGHT * .08, cell[0].get_center() + RIGHT * .42))
            return t, ln

        self.at("developing cortex")
        arr = mig_arrow()
        self.play(FadeIn(hd), FadeIn(arr), mv.animate.set_value(.9), run_time=1.6, rate_func=linear)
        self.at("trailing process")
        t1, l1 = tlabel("trailing\nprocess", GREY)
        self.add(t1, l1)
        self.play(FadeIn(t1), FadeIn(l1), mv.animate.set_value(1.45), run_time=1.0, rate_func=linear)
        self.at("migrating neuron")
        la = Arrow(P(.7, 1.15), P(.7, 2.0), buff=0, color=TEXT, stroke_width=6, tip_length=.25)
        lt = lab("migrating neuron", TEXT, 30, (3.0, 1.6))
        self.play(FadeIn(la), FadeIn(lt), mv.animate.set_value(1.95), run_time=.85, rate_func=linear)
        self.at("becomes its")
        t2, l2 = tlabel("often\nbecomes\nthe axon", YELLOW)
        self.remove(t1, l1)
        self.add(t2, l2)
        self.play(cell[0].animate.set_color(YELLOW), FadeIn(t2), FadeIn(l2), mv.animate.set_value(2.3), run_time=.9, rate_func=linear)
        self.finish()


def pathway():
    lk = chip("LKB1", LIGHT, 30).move_to([1.6, .2, 0])
    sa = chip("SAD-A", LIGHT, 30).move_to([5.3, 1.3, 0])
    sb = chip("SAD-B", LIGHT, 30).move_to([5.3, -.9, 0])
    ar1 = Arrow(lk.get_right(), sa.get_left(), buff=.1, color=TEXT, stroke_width=5)
    ar2 = Arrow(lk.get_right(), sb.get_left(), buff=.1, color=TEXT, stroke_width=5)
    act = lab("activates", TEXT, 26, (3.45, .2))
    return lk, sa, sb, ar1, ar2, act


def slice_scene_base(scene, trailing_gold=True):
    sl = slice_mob()
    cell = migrant(*MIG1, trailing=YELLOW if trailing_gold else GREY)
    scene.add(sl, mig_arrow(), cell)
    return sl, cell


class S28(SpokenScene):
    def construct(self):
        sl, cell = slice_scene_base(self)
        hd = lab("developing cortex", TEXT, 36, (RCX, 3.0), font=TITLE_FONT)
        self.add(hd)
        lk, sa, sb, ar1, ar2, act = pathway()
        self.at("clearly required")
        h2 = lab("clearly required there", GOLD, 36, (RCX, 3.0), font=TITLE_FONT)
        self.play(FadeOut(hd), FadeIn(h2), run_time=.6)
        self.at("kinase")
        self.play(FadeIn(lk, scale=.8), run_time=.5)
        self.at("sad kinase")
        self.play(FadeIn(sa, scale=.8), FadeIn(sb, scale=.8), run_time=.6)
        self.at("it activates")
        self.play(GrowArrow(ar1), GrowArrow(ar2), FadeIn(act), run_time=.7)
        self.finish()


class S29(SpokenScene):
    def construct(self):
        sl = slice_mob()
        cell = migrant(*MIG1, trailing=YELLOW)
        h2 = lab("clearly required there", GOLD, 36, (RCX, 3.0), font=TITLE_FONT)
        lk, sa, sb, ar1, ar2, act = pathway()
        self.add(sl, mig_arrow(), h2, cell, lk, sa, sb, ar1, ar2, act)
        x_lk = xmark(1.6, .85)
        x_sa, x_sb = xmark(5.3, 1.95), xmark(5.3, -.3)
        self.at("lacking")
        ko1 = migrant(*MIG1)
        self.play(FadeOut(cell), FadeIn(ko1), Create(x_lk), run_time=.6)
        self.at("or both")
        ko2 = migrant(*MIG1)
        self.play(FadeOut(x_lk), FadeOut(ko1), run_time=.25)
        self.play(FadeIn(ko2), Create(x_sa), Create(x_sb), run_time=.4)
        self.at("fail to form")
        self.play(FadeIn(lab("fail to form axons", RED, 36, (RCX, -2.5), font=TITLE_FONT), shift=UP * .1), run_time=.6)
        self.finish()


# ---------------------------------------------------------------------------------------------
# s30: closing card
# ---------------------------------------------------------------------------------------------
ROWS30_Y = [2.45, 0.0, -2.45]
LAB30_X = 0.2


def row_frame(y):
    return RoundedRectangle(corner_radius=.25, width=13.2, height=2.3, stroke_color=GOLD, stroke_width=3).move_to([0, y, 0])


D30 = [(20, .8), (105, .55), (180, .65), (255, .55)]


def left_lab(txt, col, y, size=34):
    t = lab(txt, col, size, (0, y))
    return t.align_to(P(LAB30_X, 0), LEFT)


class S30(SpokenScene):
    def construct(self):
        fr = [row_frame(y) for y in ROWS30_Y]
        y0, y1, y2 = ROWS30_Y
        # row 1: a young neuron, five equal neurites
        yg = Young(c=(-5.0, y0), sc=.42, lens=(2.0,) * 5)
        w1 = Line(yg.c + yg.dirs[0] * .28, yg.c + yg.dirs[0] * 1.3, color=YELLOW, stroke_width=9)
        t1 = left_lab("won in a race", YELLOW, y0)
        # row 2: a neuron with its axon; the initial segment is added, loosened, and the proximal axon changes
        n2 = Neu(c=(-5.4, y1), s=.85, dends=D30, axon_len=4.4, wob=0, axw=10)
        n2.group.remove(n2.axon)
        prox = n2.piece(0, .22, YELLOW)
        rest = n2.piece(.22, 1.0, YELLOW)
        ais2 = n2.piece(0, .22, PURPLE, w=30)
        t2 = left_lab("then held", PURPLE, y1 + .38)
        t2b = left_lab("loses features", BLUE, y1 - .38)
        # row 3: a neuron with a long axon, cut almost all the way
        n3 = Neu(c=(-5.4, y2), s=.85, dends=D30, axon_len=4.4, wob=0, axw=10)
        n3.group.remove(n3.axon)
        stump3 = n3.piece(0, .1)
        distal3 = n3.piece(.1, 1.0)
        cm3 = cutmark(n3.pt(.1), .4, w=4)
        t3 = left_lab("race reopens", YELLOW, y2)
        self.play(*[Create(f) for f in fr], FadeIn(yg.group), FadeIn(n2.group), FadeIn(prox), FadeIn(rest),
                  FadeIn(n3.group), FadeIn(stump3), FadeIn(distal3), run_time=.6)
        self.at("won in a")
        self.play(Create(w1), FadeIn(t1), run_time=.6)
        self.at("then held")
        self.play(FadeIn(ais2), FadeIn(t2), run_time=.5)
        self.at("loosen the")
        self.play(FadeOut(ais2), run_time=.8)
        self.at("lose features")
        sp2 = VGroup(*[Line(n2.pt(.02 + .035 * k), n2.pt(.02 + .035 * k) + UP * .24 * (1 if k % 2 else -1), color=BLUE, stroke_width=4) for k in range(1, 6)])
        self.play(prox.animate.set_color(BLUE), FadeIn(sp2), FadeIn(t2b), run_time=.8)
        self.at("cut almost")
        self.play(FadeIn(cm3), distal3.animate.set_stroke(opacity=.3), run_time=.8)
        self.at("race reopens")
        d = n3.dends[0]
        p1 = n3.ends[0][-1][0]
        self.play(d.animate.set_color(YELLOW), run_time=.3)
        newax = Line(p1, p1 + u(20) * 1.5, color=YELLOW, stroke_width=10)
        self.play(Create(newax), FadeIn(t3), run_time=.8)
        self.finish()


class S31End(EndCard):
    LINE = "Won in a race, then held.\nLoosen the hold: features can fade.\nA near-total cut can reopen the race."
