"""Proneural genes and lateral inhibition, chapter 2: The Casting Call  (Biochemistrypedia chaptered film)

COLOR MAP (one color per concept, whole chapter series; first six are the map from scenes.old.py)
  GREEN   = proneural activity / the neural fate; here the achaete-scute family (genes, proteins, bristles)
  LIME    = the extra bristles that form when achaete-scute is switched on in extra places (same concept, lighter tone)
  YELLOW  = Delta (not used in this chapter)
  BLUE    = Notch
  RED     = E(spl) repressor and inhibition arrows; also the cross that marks "removed" (a no / stop mark)
  GREY    = cells, bodies, DNA, things held back (labels are plain TEXT colour, never grey)
  GOLD    = the question mark, regulatory switches (enhancers) and the puzzle card
  TEAL    = the atonal family (gene, chordotonal organs, R8)
  PARTNER = the bHLH partner protein (Daughterless / E proteins), a soft violet
  TEXT    = labels, DNA binding site (E-box) and plain text
"""
import numpy as np
from bp_style import *  # noqa: F401,F403

PRO, ATO, NOT, PART = GREEN, TEAL, BLUE, "#B48EDD"
EXTRA_C = "#D8F56B"


# ------------------------------------------------------------------------------------------------
# shared drawing helpers
# ------------------------------------------------------------------------------------------------
def P3(x, y):
    return np.array([x, y, 0.0])


def arr(a, b, color=GREY, w=5):
    return Arrow(P3(*a) if len(a) == 2 else a, P3(*b) if len(b) == 2 else b, buff=0.06, color=color,
                 stroke_width=w, tip_length=0.22, max_tip_length_to_length_ratio=0.3)


def check_mark(center, s=0.6, color=GREEN, w=12):
    c = np.array([center[0], center[1], 0.0])
    m = VMobject(stroke_color=color, stroke_width=w, fill_opacity=0)
    m.set_points_as_corners([c + P3(-0.55 * s, 0.0), c + P3(-0.15 * s, -0.45 * s), c + P3(0.6 * s, 0.55 * s)])
    return m


def cross_mark(center, s=0.35, color=RED, w=8):
    c = np.array([center[0], center[1], 0.0])
    return VGroup(Line(c + P3(-s, -s), c + P3(s, s), color=color, stroke_width=w),
                  Line(c + P3(-s, s), c + P3(s, -s), color=color, stroke_width=w))


def strike(mob, color=RED, w=7, pad=0.06):
    return Line(mob.get_corner(DL) + P3(-pad, -pad), mob.get_corner(UR) + P3(pad, pad), color=color, stroke_width=w)


def leader(text, pos, target, size=28, color=TEXT, lc=GREY):
    """A label with a thin leader line to the thing it names."""
    t = T(text, size, color).move_to(P3(*pos))
    side = RIGHT if target[0] > pos[0] else LEFT
    ln = Line(t.get_edge_center(side) + side * 0.1, P3(*target), color=lc, stroke_width=2.5).set_opacity(0.85)
    return VGroup(t, ln)


# ---- cells --------------------------------------------------------------------------------------
CLP = {"A": (-0.95, 0.0), "B": (0.95, 0.0), "C": (0, 1.6), "D": (-1.95, -1.5), "E": (1.95, -1.5)}


def cluster_cells(sc=1.1, center=(-2.7, -0.5), rim=GREY, sw=4):
    return {k: Circle(radius=0.85 * sc, stroke_color=rim, stroke_width=sw, fill_color=GREY, fill_opacity=0.08)
            .move_to(P3(center[0] + x * sc, center[1] + y * sc)) for k, (x, y) in CLP.items()}


# ---- the fly (top view), drawn at unit size then scaled ---------------------------------------
PARTS = [(0, 0.45, 0.75, 0.85), (0, -1.45, 0.625, 1.0), (0, 1.6, 0.4, 0.4)]   # thorax, abdomen, head


class FlyIcon:
    def __init__(self, scale=1.0, center=(0, 0), col=GREY):
        self.sc, self.c = scale, np.array([center[0], center[1], 0.0])
        wings = VGroup(*[Ellipse(width=0.85, height=2.3, stroke_color=col, stroke_width=2, fill_color=col, fill_opacity=0.06)
                         .rotate(s * 0.5).move_to(P3(s * 1.0, -0.2)) for s in (-1, 1)])
        self.abd = Ellipse(width=1.25, height=2.0, stroke_color=col, stroke_width=3, fill_color=col, fill_opacity=0.1).move_to(P3(0, -1.45))
        stripes = VGroup(*[Line(P3(-0.625 * np.sqrt(1 - ((y + 1.45) / 1.0) ** 2), y), P3(0.625 * np.sqrt(1 - ((y + 1.45) / 1.0) ** 2), y),
                                color=col, stroke_width=2).set_opacity(0.5) for y in (-1.0, -1.45, -1.9)])
        self.thorax = Ellipse(width=1.5, height=1.7, stroke_color=col, stroke_width=3, fill_color=col, fill_opacity=0.14).move_to(P3(0, 0.45))
        self.head = Circle(radius=0.4, stroke_color=col, stroke_width=3, fill_color=col, fill_opacity=0.14).move_to(P3(0, 1.6))
        self.group = VGroup(wings, self.abd, stripes, self.thorax, self.head)
        self.group.scale(scale, about_point=ORIGIN).shift(self.c)

    def pt(self, x, y):
        return self.c + self.sc * P3(x, y)


def _inside(x, y, part, k=1.1):
    cx, cy, a, b = part
    return ((x - cx) / a) ** 2 + ((y - cy) / b) ** 2 < k * k


def _in_wing(x, y):
    """True if (x, y) in FlyIcon unit space lies inside (or just beside) either wing ellipse."""
    for sgn in (-1, 1):
        a = sgn * 0.5
        dx, dy = x - sgn * 1.0, y + 0.2
        u = dx * np.cos(a) + dy * np.sin(a)
        v = -dx * np.sin(a) + dy * np.cos(a)
        if (u / 0.62) ** 2 + (v / 1.4) ** 2 < 1:
            return True
    return False


def fly_bristles(f, color=GREEN, sw=4, ln=0.19, gap=0.07):
    """External bristles around the outline of a FlyIcon: short, spaced, and only where the outline is free."""
    out = []
    for i, (cx, cy, a, b) in enumerate(PARTS):
        others = [p for j, p in enumerate(PARTS) if j != i]
        step = 28 if i < 2 else 45
        for d in range(8, 368, step):
            t = np.radians(d)
            p = P3(cx + a * np.cos(t), cy + b * np.sin(t))
            n = P3(np.cos(t) / a, np.sin(t) / b)
            n = n / np.linalg.norm(n)
            p0 = p + gap * n
            q = p0 + ln * n
            if any(_inside(p[0], p[1], o, 1.3) or _inside(q[0], q[1], o, 1.3) for o in others):
                continue
            if any(_in_wing(v[0], v[1]) for v in (p0, q, (p0 + q) / 2)):
                continue
            out.append(Line(f.pt(*p0[:2]), f.pt(*q[:2]), color=color, stroke_width=sw))
    # the fly's back (notum) carries rows of bristles, drawn well inside the thorax outline
    for u in (-0.27, 0.27):
        for v in (0.95, 0.65, 0.35, 0.05):
            out.append(bristle(f.pt(u, v), 0.2 * f.sc, color, sw, 0.045))
    return VGroup(*out)


CHORDO_SPOTS = [(-0.3, 0.78, 0.5), (0.3, 0.8, -0.4), (-0.33, 0.28, 0.2), (0.33, 0.22, -0.4), (0.0, 0.52, 1.4),
                (-0.17, -1.0, 0.3), (0.17, -1.0, -0.3), (0.0, -1.27, 1.5), (-0.17, -1.6, 0.3), (0.17, -1.6, -0.3),
                (0.0, -1.9, 1.4), (0.0, 1.6, 0.4)]


def fly_chordos(f, color=ATO):
    return VGroup(*[Ellipse(width=0.4 * f.sc, height=0.15 * f.sc, stroke_color=color, stroke_width=2, fill_color=color, fill_opacity=0.9)
                    .rotate(a).move_to(f.pt(x, y)) for x, y, a in CHORDO_SPOTS])


def fly_inner(f, color=ATO):
    """A dashed inner outline: the cut-away that says 'inside the body'."""
    parts = []
    for (cx, cy, a, b) in PARTS:
        e = Ellipse(width=2 * a * 0.78 * f.sc, height=2 * b * 0.78 * f.sc, stroke_color=color, stroke_width=3).move_to(f.pt(cx, cy))
        parts.append(DashedVMobject(e, num_dashes=22).set_opacity(0.8))
    return VGroup(*parts)


# ---- the notum (the fly's back) and its bristles ------------------------------------------------
NRAT = 0.9     # one notum shape for the whole film: a = 0.9 b
DC = [(0.32 * s, v) for s in (-1, 1) for v in (0.55, 0.3, 0.05, -0.2)]
SCU = [(0.2, -0.7), (-0.2, -0.7), (0.5, -0.56), (-0.5, -0.56)]
LAT = [(0.78 * s, 0.4) for s in (-1, 1)] + [(0.8 * s, 0.1) for s in (-1, 1)] + [(0.74 * s, -0.25) for s in (-1, 1)] + [(0.56 * s, -0.45) for s in (-1, 1)]
EXTRA = [(0.0, 0.78), (-0.58, 0.68), (0.58, 0.68), (0.0, 0.36), (-0.58, 0.22), (0.58, 0.22),
         (0.0, 0.08), (-0.58, -0.06), (0.58, -0.06), (0.0, -0.3), (-0.32, -0.44), (0.32, -0.44),
         (-0.3, 0.82), (0.3, 0.82), (0.0, -0.58)]


def notum_geom(center, b):
    a = NRAT * b
    out = Ellipse(width=2 * a, height=2 * b, stroke_color=GREY, stroke_width=4, fill_color=GREY, fill_opacity=0.08).move_to(P3(*center))
    pos = lambda lst: [P3(center[0] + u * a, center[1] + v * b) for u, v in lst]
    return out, {"dc": pos(DC), "sc": pos(SCU), "lat": pos(LAT), "extra": pos(EXTRA)}


def bristle(p, ln, color=GREEN, sw=5, r=0.075):
    tilt = 0.25 * np.sign(p[0]) if abs(p[0]) > 0.01 else 0.0
    tip = P3(p[0] + tilt * ln, p[1] - ln)
    return VGroup(Line(P3(p[0], p[1]), tip, color=color, stroke_width=sw), Dot(P3(p[0], p[1]), radius=r, color=color))


def bristles(points, ln, color=GREEN, sw=5, r=0.075):
    return VGroup(*[bristle(p, ln, color, sw, r) for p in points])


def ghosts(points, r=0.13):
    return VGroup(*[DashedVMobject(Circle(radius=r, stroke_color=TEXT, stroke_width=3).move_to(p), num_dashes=8).set_opacity(0.7) for p in points])


def band_poly(center, a, b, u0, u1, color=GREEN, op=0.3):
    us = np.linspace(u0, u1, 6)
    top = [P3(center[0] + u * a, center[1] + 0.93 * b * np.sqrt(max(0, 1 - u * u))) for u in us]
    bot = [P3(center[0] + u * a, center[1] - 0.93 * b * np.sqrt(max(0, 1 - u * u))) for u in us[::-1]]
    return Polygon(*top, *bot, stroke_width=0, fill_color=color, fill_opacity=op)


# ---- body wall and chordotonal organ -----------------------------------------------------------
def organ_static(xl, xr, ybot, ys, wsp, hsp, color=ATO):
    """Two anchors on the wall's inner face, two fibres, and the spindle-shaped organ between them."""
    spindle = Ellipse(width=wsp, height=hsp, stroke_color=color, stroke_width=3, fill_color=color, fill_opacity=0.55).move_to(P3((xl + xr) / 2, ys))
    l1 = Line(P3(xl, ybot), P3((xl + xr) / 2 - wsp / 2, ys), color=color, stroke_width=4)
    l2 = Line(P3(xr, ybot), P3((xl + xr) / 2 + wsp / 2, ys), color=color, stroke_width=4)
    d1, d2 = Dot(P3(xl, ybot), radius=0.1, color=color), Dot(P3(xr, ybot), radius=0.1, color=color)
    return VGroup(l1, l2, d1, d2, spindle)


class Organ:
    """A strip of body wall with a chordotonal organ hung inside it. k bends the wall; lift moves everything up."""
    HW, SAG = 5.6, 0.8

    def __init__(self):
        self.k, self.lift = ValueTracker(0), ValueTracker(0)
        self.wall = always_redraw(self._wall)
        self.org = always_redraw(self._org)

    def edge(self, x, off):
        k = self.k.get_value()
        y0 = 0.6 + self.lift.get_value()
        return y0 + off - self.SAG * k * (1 - (x / self.HW) ** 2)

    def _wall(self):
        xs = np.linspace(-self.HW, self.HW, 36)
        top = [P3(x, self.edge(x, 0.5)) for x in xs]
        bot = [P3(x, self.edge(x, -0.5)) for x in xs[::-1]]
        return Polygon(*top, *bot, stroke_color=GREY, stroke_width=3, fill_color=GREY, fill_opacity=0.2)

    def _org(self):
        k = self.k.get_value()
        xa = 1.9 + 1.5 * k
        ys = self.edge(0, -0.5) - 2.1
        return organ_static(-xa, xa, self.edge(xa, -0.5), ys, 2.0 + 1.6 * k, 1.35 - 0.7 * k)


def body_wall_label():
    t = T("body wall", 28, TEXT, weight=BOLD).move_to(P3(-4.3, 1.85))
    ln = Line(P3(-4.3, 1.62), P3(-4.3, 1.14), color=GREY, stroke_width=2.5)
    return VGroup(t, ln)


# ---- bHLH protein cartoon ------------------------------------------------------------------------
def protein(center, sc=1.0, mirror=False, color=GREEN):
    m = -1 if mirror else 1
    pt = lambda x, y: P3(center[0] + m * x * sc, center[1] + y * sc)
    kw = dict(stroke_color=color, stroke_width=3, fill_color=color)
    h1 = RoundedRectangle(width=0.8 * sc, height=1.7 * sc, corner_radius=0.35 * sc, fill_opacity=0.28, **kw).move_to(pt(-0.55, 0.55))
    h2 = RoundedRectangle(width=0.8 * sc, height=1.7 * sc, corner_radius=0.35 * sc, fill_opacity=0.28, **kw).move_to(pt(0.55, 0.55))
    loop = ArcBetweenPoints(pt(-0.55, 1.4), pt(0.55, 1.4), angle=-PI * m, stroke_color=color, stroke_width=7)
    basic = RoundedRectangle(width=0.6 * sc, height=0.9 * sc, corner_radius=0.18 * sc, fill_opacity=0.6, **kw).move_to(pt(-0.55, -0.75))
    g = VGroup(basic, h1, loop, h2)
    g.basic, g.h1, g.loop, g.h2 = basic, h1, loop, h2
    return g


def dna_bar(y, w=12.8, h=0.4):
    return Rectangle(width=w, height=h, stroke_color=GREY, stroke_width=2, fill_color=GREY, fill_opacity=0.4).move_to(P3(0, y))


# pair geometry shared by S14 to S16
PSC, PCY = 1.7, 0.0            # protein scale, y of the proteins when they grip the DNA
PDX = 0.94 * PSC               # centre-to-centre: the two inner helices touch
LIFT = 0.4                     # the proteins hover this far above the DNA until the basic parts lower onto it
DNA_Y = PCY - 1.2 * PSC - 0.2
EBY = DNA_Y
EBW = 2 * (PDX + 0.55 * PSC) + 0.6 * PSC + 0.5


def pair_group(together=True, colB=PART, dy=0.0):
    dx = PDX if together else 2.7
    A = protein((-dx, PCY + dy), PSC, False, GREEN)
    B = protein((dx, PCY + dy), PSC, True, colB)
    return A, B


def pair_box(dy=0.0):
    """The 'pairing' highlight: an outline round the two touching inner helices, with its label below."""
    box = RoundedRectangle(width=1.95 * PSC, height=1.95 * PSC, corner_radius=0.3, stroke_color=TEXT, stroke_width=4,
                           fill_opacity=0).move_to(P3(0, PCY + 0.55 * PSC + dy))
    lab = T("pairing", 30, TEXT, weight=BOLD).move_to(P3(0, PCY - 0.95 * PSC + dy))
    ln = Line(lab.get_top() + UP * 0.05, box.get_bottom(), color=TEXT, stroke_width=2.5)
    return VGroup(box, lab, ln)


def ebox_rect():
    return Rectangle(width=EBW, height=0.5, stroke_color=TEXT, stroke_width=3, fill_color=TEXT, fill_opacity=0.5).move_to(P3(0, EBY))


def right_group(lines, x_left, y):
    """Stack of text lines, left-aligned at x_left, vertically centred on y."""
    g = VGroup(*[T(t, s, c, weight=w) for t, s, c, w in lines]).arrange(DOWN, buff=0.1, aligned_edge=LEFT)
    g.move_to(P3(0, y))
    g.shift(RIGHT * (x_left - g.get_left()[0]))
    return g


# ------------------------------------------------------------------------------------------------
class S00Title(TitleCard):
    LESSON = "Proneural genes and lateral inhibition"
    TITLE = "The Casting Call"


# ------------------------------------------------------------------------------------------------
class S01Question(SpokenScene):
    def construct(self):
        cells = cluster_cells(1.1, (-2.7, -0.5))
        grp = VGroup(*cells.values())
        lamp = Polygon(P3(-3.1, 3.55), P3(-2.3, 3.55), P3(-2.0, 3.1), P3(-3.4, 3.1), stroke_color=GREY, stroke_width=3, fill_color=GREY, fill_opacity=0.5)
        cone = Polygon(P3(-3.0, 3.1), P3(-2.4, 3.1), P3(0.7, -3.3), P3(-5.9, -3.3), stroke_width=0, fill_color=TEXT, fill_opacity=0.1)
        q1 = T("What gives them", 44, TEXT, font=TITLE_FONT)
        q2 = T("that ability?", 44, GOLD, font=TITLE_FONT)
        q = VGroup(q1, q2).arrange(DOWN, buff=0.25, aligned_edge=LEFT).move_to(P3(3.9, 0.0))
        self.play(LaggedStart(*[GrowFromCenter(c) for c in grp], lag_ratio=0.15), run_time=1.0)
        self.at("audition")
        self.play(FadeIn(cone), FadeIn(lamp), grp.animate.set_stroke(TEXT, 5).set_fill(TEXT, 0.12), run_time=0.7)
        self.at("what")
        self.play(FadeIn(q1, shift=LEFT * 0.25), run_time=0.5)
        self.at("ability")
        self.play(FadeIn(q2, shift=LEFT * 0.25), run_time=0.45)
        self.finish()


# ------------------------------------------------------------------------------------------------
class S02Found(SpokenScene):
    def construct(self):
        CY_ = -0.6
        f = FlyIcon(0.55, (-5.9, 2.0))
        flab = T("fly", 38, TEXT, weight=BOLD).move_to(P3(-4.55, 2.0))
        chrom = RoundedRectangle(width=13.0, height=1.1, corner_radius=0.5, stroke_color=GREY, stroke_width=3,
                                 fill_color=GREY, fill_opacity=0.2).move_to(P3(0, CY_))
        bands = VGroup(*[Line(P3(x, CY_ - 0.38), P3(x, CY_ + 0.38), color=GREY, stroke_width=3).set_opacity(0.6)
                         for x in (-6.0, -5.2, -4.4, -3.6, 3.6, 4.4, 5.2, 6.0)])
        g1 = Rectangle(width=2.8, height=4.4, stroke_color=PRO, stroke_width=4, fill_color=PRO, fill_opacity=0.3).move_to(P3(-1.5, CY_))
        g2 = Rectangle(width=2.8, height=4.4, stroke_color=PRO, stroke_width=4, fill_color=PRO, fill_opacity=0.3).move_to(P3(1.5, CY_))
        n1 = T("achaete", 38, PRO, weight=BOLD).move_to(g1)
        n2 = T("scute", 38, PRO, weight=BOLD).move_to(g2)
        br = Brace(VGroup(g1, g2), UP, buff=0.15, color=PRO)
        cx = T("achaete-scute complex", 42, PRO).next_to(br, UP, buff=0.15)
        clab = T("chromosome", 34, TEXT).move_to(P3(-4.9, -1.85))
        self.add(chrom, bands)
        self.at("fly")
        self.play(FadeIn(f.group, shift=RIGHT * 0.2), FadeIn(flab), run_time=0.6)
        self.at("them")
        self.play(GrowFromCenter(g1), run_time=0.5)
        self.at("and", lead=0.2)
        self.play(FadeIn(n1, scale=0.8), run_time=0.25)
        self.at("and", lead=-0.0)
        self.play(GrowFromCenter(g2), run_time=0.25)
        self.at("and", lead=-0.3)
        self.play(FadeIn(n2, scale=0.8), run_time=0.3)
        self.at("sit", lead=0.1)
        self.play(GrowFromCenter(br), FadeIn(cx, shift=UP * 0.15), run_time=0.7)
        self.at("chromosome")
        self.play(FadeIn(clab, shift=UP * 0.1), run_time=0.5)
        self.finish()


# ------------------------------------------------------------------------------------------------
class S03Bristles(SpokenScene):
    def construct(self):
        out, pts = notum_geom((-1.2, 0.0), 3.0)
        allp = pts["dc"] + pts["sc"] + pts["lat"]
        br = bristles(allp, 0.15 * 3.0, GREEN, 6)
        lab = leader("the fly's back\n(notum)", (4.6, 0.0), (out.get_right()[0] + 0.1, 0.0), 32, TEXT)
        self.play(FadeIn(out), run_time=0.5)
        self.at("bristles")
        self.play(LaggedStart(*[GrowFromPoint(b, b[1].get_center()) for b in br], lag_ratio=0.05), run_time=1.1)
        self.at("back")
        self.play(FadeIn(lab, shift=UP * 0.1), run_time=0.4)
        self.finish()


# ---- the prediction frame is rebuilt by S04, S05 and S06 ------------------------------------------
LX, RX, NY, NB = -3.7, 3.7, -0.35, 2.35


def predict_frame():
    lo, lp = notum_geom((LX, NY), NB)
    ro, rp = notum_geom((RX, NY), NB)
    lt = VGroup(T("Remove", 30, TEXT), T("achaete-scute", 30, PRO)).arrange(RIGHT, buff=0.18).move_to(P3(LX, 3.0))
    rt = T("Switch it on in extra places", 30, TEXT).move_to(P3(RX, 3.0))
    lq = T("?", 110, GOLD, font=TITLE_FONT).move_to(P3(LX, NY))
    rq = T("?", 110, GOLD, font=TITLE_FONT).move_to(P3(RX, NY))
    pr = T("Predict", 44, GOLD, font=TITLE_FONT).move_to(P3(0, 0.55))
    return lo, lp, ro, rp, lt, rt, lq, rq, pr


class S04Predict(SpokenScene):
    def construct(self):
        out0, pts0 = notum_geom((-1.2, 0.0), 3.0)
        br0 = bristles(pts0["dc"] + pts0["sc"] + pts0["lat"], 0.15 * 3.0, GREEN, 6)
        lo, lp, ro, rp, lt, rt, lq, rq, pr = predict_frame()
        self.add(out0, br0)
        self.at("predict", lead=0.0)
        self.play(ReplacementTransform(out0, lo), FadeOut(br0), FadeIn(ro, shift=RIGHT * 0.5), FadeIn(pr, scale=0.8), run_time=1.1)
        self.at("remove these")
        self.play(FadeIn(lt, shift=DOWN * 0.15), run_time=0.5)
        self.at("what happens")
        self.play(FadeIn(lq, scale=0.7), run_time=0.5)
        self.at("then switch")
        self.play(FadeIn(rt, shift=DOWN * 0.15), run_time=0.5)
        self.at("extra places")
        self.play(FadeIn(rq, scale=0.7), run_time=0.5)
        self.finish()


class S05Pause(NarratedScene):
    def construct(self):
        lo, lp, ro, rp, lt, rt, lq, rq, pr = predict_frame()
        self.add(lo, ro, lt, rt, lq, rq, pr)
        tt = ValueTracker(0)
        c = P3(0, -1.2)
        face = Circle(radius=0.85, stroke_color=GREY, stroke_width=5, fill_opacity=0).move_to(c)
        knob = Line(c + P3(0, 0.85), c + P3(0, 1.1), color=TEXT, stroke_width=7)
        ring = always_redraw(lambda: Arc(radius=0.85, start_angle=PI / 2, angle=-2 * PI * min(tt.get_value(), 4.999) / 5, color=GOLD, stroke_width=9).move_arc_center_to(c))
        num = always_redraw(lambda: M(str(max(1, 5 - int(tt.get_value()))), 60, GOLD).move_to(c))
        self.add(face, knob, ring, num)
        self.play(tt.animate.set_value(5.0), run_time=max(1.0, self.narration_s - 0.05), rate_func=linear)
        self.finish()


def reveal_parts():
    """Every piece of the reveal frame, so S06 can build it and S07 can fold it away."""
    lo, lp, ro, rp, lt, rt, lq, rq, pr = predict_frame()
    ln = 0.15 * NB
    allp = lambda p: p["dc"] + p["sc"] + p["lat"]
    mc, mb = (0, NY - 0.1), 1.25
    mo, mp = notum_geom(mc, mb)
    return dict(lo=lo, ro=ro, lt=lt, rt=rt, lq=lq, rq=rq, pr=pr, mo=mo,
                m_br=bristles(allp(mp), 0.15 * mb, GREEN, 3.5, 0.045),
                m_lab=T("normal", 28, TEXT).move_to(P3(0, mc[1] - mb - 0.38)),
                l_old=bristles(allp(lp), ln, GREEN, 5), l_ghost=ghosts(allp(lp)),
                r_norm=bristles(allp(rp), ln, GREEN, 5), r_extra=bristles(rp["extra"], ln, EXTRA_C, 5),
                l_lab=T("bristles missing", 32, TEXT).move_to(P3(LX, NY - NB - 0.5)),
                r_lab=T("extra bristles", 32, EXTRA_C).move_to(P3(RX, NY - NB - 0.5)))


class S06Reveal(SpokenScene):
    def construct(self):
        P = reveal_parts()
        self.add(P["lo"], P["ro"], P["lt"], P["rt"], P["lq"], P["rq"], P["pr"])
        self.at("remove them", lead=0.0)
        self.play(FadeOut(P["lq"]), FadeOut(P["pr"]), FadeIn(P["mo"]), FadeIn(P["m_br"]), FadeIn(P["m_lab"]), FadeIn(P["l_old"]), run_time=0.6)
        self.at("missing")
        self.play(FadeOut(P["l_old"]), FadeIn(P["l_ghost"]), FadeIn(P["l_lab"], shift=UP * 0.1), run_time=0.7)
        self.play(Indicate(P["l_ghost"], color=TEXT, scale_factor=1.08), run_time=0.5)
        self.at("switch them")
        self.play(FadeOut(P["rq"]), run_time=0.3)
        self.play(LaggedStart(*[GrowFromPoint(b, b[1].get_center()) for b in P["r_norm"]], lag_ratio=0.04), run_time=0.8)
        self.at("extra bristles")
        self.play(LaggedStart(*[GrowFromPoint(b, b[1].get_center()) for b in P["r_extra"]], lag_ratio=0.06), FadeIn(P["r_lab"], shift=UP * 0.1), run_time=0.9)
        self.finish()


# ------------------------------------------------------------------------------------------------
def name_card(sc=1.0, y=2.55):
    box = RoundedRectangle(width=5.6 * sc, height=1.9 * sc, corner_radius=0.2 * sc, stroke_color=ATO, stroke_width=4, fill_color=ATO, fill_opacity=0.1).move_to(P3(0, y))
    nm = T("atonal", 62 * sc, ATO, font=TITLE_FONT).move_to(P3(-0.9 * sc, y))
    yr = M("1993", 46 * sc, TEXT).move_to(P3(1.7 * sc, y))
    return box, nm, yr


class S07Atonal(SpokenScene):
    def construct(self):
        P = reveal_parts()
        keys = ("lo", "ro", "lt", "rt", "mo", "m_br", "m_lab", "l_ghost", "r_norm", "r_extra", "l_lab", "r_lab")
        old = VGroup(*[P[k] for k in keys])
        box, nm, yr = name_card(0.8, 3.0)
        org = Organ()
        bw = body_wall_label()
        lab = T("chordotonal organ", 36, ATO).move_to(P3(0, -3.4))
        self.add(old)
        self.play(old.animate.scale(0.12).move_to(box.get_center()).set_opacity(0), FadeIn(box), FadeIn(nm), FadeIn(org.wall), FadeIn(org.org),
                  FadeIn(bw), run_time=0.3)
        self.remove(old)
        self.at("1993")
        self.play(FadeIn(yr, shift=LEFT * 0.2), run_time=0.5)
        self.at("for")
        self.play(FadeIn(lab, shift=UP * 0.1), run_time=0.5)
        self.finish()


class S08Chordo(SpokenScene):
    def construct(self):
        box, nm, yr = name_card(0.8, 3.0)
        org = Organ()
        bw = body_wall_label()
        lab = T("chordotonal organ", 36, ATO).move_to(P3(0, -3.4))
        self.add(box, nm, yr, org.wall, org.org, bw, lab)
        sr = T("internal stretch receptor", 40, ATO).move_to(P3(0, -3.2))
        self.play(FadeOut(box), FadeOut(nm), FadeOut(yr), org.lift.animate.set_value(0.9), bw.animate.shift(UP * 0.9),
                  ReplacementTransform(lab, sr), run_time=0.5)
        self.at("internal")
        self.play(org.k.animate.set_value(1.0), run_time=0.8, rate_func=smooth)
        self.play(org.k.animate.set_value(0.0), run_time=0.55, rate_func=smooth)
        self.play(org.k.animate.set_value(1.0), run_time=0.55, rate_func=smooth)
        self.finish()


# ------------------------------------------------------------------------------------------------
class S09Kinds(SpokenScene):
    def construct(self):
        WY = 0.15
        BPRO = interpolate_color(ManimColor(PRO), WHITE, 0.4)
        BATO = interpolate_color(ManimColor(ATO), WHITE, 0.4)
        wall = Rectangle(width=13.0, height=0.9, stroke_color=GREY, stroke_width=3, fill_color=GREY, fill_opacity=0.22).move_to(P3(0, WY))
        chip_a = chip("achaete-scute", PRO, size=32).move_to(P3(-5.0, 3.4))
        chip_t = chip("atonal", ATO, size=32).move_to(P3(5.0, 3.4))
        bx = -3.4
        brs = VGroup(Line(P3(bx, WY + 0.45), P3(bx + 0.35, 2.45), color=PRO, stroke_width=15), Dot(P3(bx, WY + 0.45), radius=0.33, color=PRO))
        orgn = organ_static(1.8, 5.1, WY - 0.45, -2.45, 3.5, 1.75)
        a1 = arr((-4.4, 2.95), (-3.2, 2.5), BPRO, 9)
        a2 = arr((4.6, 2.95), (3.8, WY + 0.55), BATO, 9)
        l1 = T("external bristle", 36, PRO).move_to(P3(-0.2, 1.75))
        l1.shift(RIGHT * (-2.3 - l1.get_left()[0]))
        l2 = T("internal\nchordotonal organ", 34, ATO).move_to(P3(0, -2.0))
        l2.shift(RIGHT * (1.4 - l2.get_right()[0]))
        self.play(GrowFromEdge(wall, LEFT), run_time=0.4)
        self.at("different")
        self.play(FadeIn(chip_a, shift=DOWN * 0.15), FadeIn(chip_t, shift=DOWN * 0.15), run_time=0.6)
        self.at("start")
        self.play(GrowArrow(a1), FadeIn(brs, shift=UP * 0.2), FadeIn(l1, shift=RIGHT * 0.1), run_time=0.7)
        self.at("different", nth=1)
        self.play(GrowArrow(a2), FadeIn(orgn, shift=DOWN * 0.2), FadeIn(l2, shift=LEFT * 0.1), run_time=0.8)
        self.finish()


class S10Kinds2(SpokenScene):
    def construct(self):
        FC = -0.2
        fl = FlyIcon(1.15, (-3.6, FC))
        fr = FlyIcon(1.15, (3.6, FC))
        bro = fly_bristles(fl, PRO, 4)
        chs = fly_chordos(fr, ATO)
        inner = fly_inner(fr, ATO)
        ca = chip("achaete-scute ON", PRO, size=28).move_to(P3(-3.6, 3.35))
        ct = chip("atonal ON", ATO, size=28).move_to(P3(3.6, 3.35))
        la = T("only external sense organs", 28, PRO).move_to(P3(-3.6, -3.6))
        lt = T("mostly chordotonal organs", 28, ATO).move_to(P3(3.6, -3.6))
        self.add(fl.group, fr.group)
        self.at("force")
        self.play(FadeIn(ca, shift=DOWN * 0.15), run_time=0.5)
        self.at("only external")
        self.play(LaggedStart(*[Create(b) for b in bro], lag_ratio=0.02), run_time=0.9)
        self.at("organs form")
        self.play(FadeIn(la, shift=UP * 0.1), run_time=0.5)
        self.at("force", nth=1)
        self.play(FadeIn(ct, shift=DOWN * 0.15), run_time=0.5)
        self.at("mostly")
        self.play(FadeIn(inner), LaggedStart(*[GrowFromCenter(c) for c in chs], lag_ratio=0.06), run_time=1.2)
        self.at("organs form", nth=1)
        self.play(FadeIn(lt, shift=UP * 0.1), run_time=0.5)
        self.finish()


# ------------------------------------------------------------------------------------------------
EYE_C, UNIT_C = P3(-3.6, -0.1), P3(3.5, 0.0)
EYE_R, UNIT_R = 2.7, 2.7
R8_R, SEV_R, RING_R = 0.65, 0.42, 1.6


def eye_dome():
    dome = Circle(radius=EYE_R, stroke_color=GREY, stroke_width=4, fill_color=GREY, fill_opacity=0.08).move_to(EYE_C)
    dots = []
    for r in range(-6, 7):
        for c in range(-6, 7):
            x, y = (c + 0.5 * (r % 2)) * 0.5, r * 0.433
            if np.hypot(x, y) < EYE_R - 0.3:
                dots.append(Circle(radius=0.19, stroke_color=GREY, stroke_width=2, fill_color=GREY, fill_opacity=0.18).move_to(EYE_C + P3(x, y)))
    lattice = VGroup(*dots)
    target = min(dots, key=lambda d: np.linalg.norm(d.get_center() - (EYE_C + P3(1.0, 0.4))))
    return dome, lattice, target


def eye_label():
    return T("compound eye", 32, TEXT).move_to(EYE_C + P3(0, -EYE_R - 0.6))


def unit_parts():
    unit = Circle(radius=UNIT_R, stroke_color=GREY, stroke_width=4, fill_color=GREY, fill_opacity=0.08).move_to(UNIT_C)
    r8 = Circle(radius=R8_R, stroke_color=ATO, stroke_width=4, fill_color=ATO, fill_opacity=0.6).move_to(UNIT_C)
    r8t = T("R8", 38, TEXT, weight=BOLD).move_to(UNIT_C)
    dirs = [P3(np.cos(a), np.sin(a)) for a in np.linspace(PI / 2, PI / 2 + 2 * PI, 8)[:-1]]
    seven = VGroup(*[Circle(radius=SEV_R, stroke_color=TEXT, stroke_width=3, fill_color=GREY, fill_opacity=0.4).move_to(UNIT_C + RING_R * d) for d in dirs])
    arrows = VGroup(*[Arrow(UNIT_C + 0.78 * d, UNIT_C + (RING_R - SEV_R - 0.06) * d, buff=0, color=ATO, stroke_width=4, tip_length=0.16,
                            max_tip_length_to_length_ratio=0.5) for d in dirs])
    return unit, r8, r8t, seven, arrows, dirs


def zoom_lines(target):
    t = target.get_center()
    pa = UNIT_C + UNIT_R * P3(np.cos(np.radians(104)), np.sin(np.radians(104)))
    pb = UNIT_C + UNIT_R * P3(np.cos(np.radians(256)), np.sin(np.radians(256)))
    return VGroup(Line(t + P3(0.1, 0.15), pa, color=GREY, stroke_width=2.5).set_opacity(0.7),
                  Line(t + P3(0.1, -0.15), pb, color=GREY, stroke_width=2.5).set_opacity(0.7))


class S11R8(SpokenScene):
    def construct(self):
        dome, lattice, target = eye_dome()
        elab = eye_label()
        ch = chip("atonal", ATO, size=30).move_to(EYE_C + P3(0, EYE_R + 0.55))
        unit, r8, r8t, seven, arrows, dirs = unit_parts()
        zl = zoom_lines(target)
        fnd = T("founding photoreceptor", 32, ATO).move_to(UNIT_C + P3(0, -UNIT_R - 0.6))
        self.play(FadeIn(dome), LaggedStart(*[FadeIn(d, scale=0.5) for d in lattice], lag_ratio=0.008), FadeIn(elab), run_time=1.2)
        self.at("atonal")
        self.play(FadeIn(ch, shift=DOWN * 0.15), run_time=0.5)
        self.at("needed")
        self.play(target.animate.set_stroke(ATO, 4).set_fill(ATO, 0.6), Create(zl), FadeIn(unit, scale=0.5), run_time=0.45)
        self.at("r8")
        self.play(GrowFromCenter(r8), FadeIn(r8t, scale=0.6), run_time=0.5)
        self.at("founding")
        self.play(Indicate(r8, color=ATO, scale_factor=1.2), FadeIn(fnd, shift=UP * 0.1), run_time=0.9)
        self.at("each")
        ripple = Circle(radius=R8_R, stroke_color=ATO, stroke_width=6, fill_opacity=0).move_to(UNIT_C)
        self.play(ripple.animate.scale(3.4).set_stroke(opacity=0), LaggedStart(*[GrowArrow(a) for a in arrows], lag_ratio=0.05),
                  LaggedStart(*[FadeIn(s, scale=0.4) for s in seven], lag_ratio=0.08), run_time=1.0)
        self.finish()


class S12R8b(SpokenScene):
    def construct(self):
        dome, lattice, target = eye_dome()
        target.set_stroke(ATO, 4).set_fill(ATO, 0.6)
        elab = eye_label()
        ch = chip("atonal", ATO, size=30).move_to(EYE_C + P3(0, EYE_R + 0.55))
        unit, r8, r8t, seven, arrows, dirs = unit_parts()
        zl = zoom_lines(target)
        fnd = T("founding photoreceptor", 32, ATO).move_to(UNIT_C + P3(0, -UNIT_R - 0.6))
        self.add(dome, lattice, elab, ch, zl, unit, r8, r8t, seven, arrows, fnd)
        xx = strike(ch)
        r8ghost = DashedVMobject(Circle(radius=R8_R, stroke_color=ATO, stroke_width=4).move_to(UNIT_C), num_dashes=14).set_opacity(0.8)
        tghost = DashedVMobject(Circle(radius=0.25, stroke_color=ATO, stroke_width=3).move_to(target.get_center()), num_dashes=10).set_opacity(0.9)
        sghost = VGroup(*[DashedVMobject(Circle(radius=SEV_R, stroke_color=TEXT, stroke_width=3).move_to(s.get_center()), num_dashes=12).set_opacity(0.8) for s in seven])
        rec = VGroup(*[Arrow(a.get_start(), a.get_end(), buff=0, color=ATO, stroke_width=3, tip_length=0.16, max_tip_length_to_length_ratio=0.5).set_opacity(0.5) for a in arrows])
        none = T("none form", 36, TEXT, weight=BOLD).move_to(UNIT_C + P3(0, -UNIT_R - 0.6))
        self.at("without")
        self.play(Create(xx), run_time=0.4)
        self.at("no r8")
        self.play(FadeOut(r8), FadeOut(r8t), FadeOut(arrows), FadeIn(r8ghost), FadeOut(fnd),
                  target.animate.set_stroke(GREY, 2).set_fill(GREY, 0.18), FadeIn(tghost), run_time=0.8)
        self.at("seven")
        self.play(FadeOut(seven), FadeIn(sghost), run_time=0.9)
        self.at("recruits")
        self.play(FadeIn(rec), run_time=0.5)
        self.at("do not form")
        self.play(FadeOut(rec), FadeIn(none, shift=UP * 0.1), run_time=0.6)
        self.finish()


# ------------------------------------------------------------------------------------------------
S13_SC, S13_CY = 1.85, 0.05


class S13Bhlh(SpokenScene):
    def construct(self):
        sc, cp = S13_SC, (0, S13_CY)
        ca = chip("achaete-scute", PRO, size=40).move_to(P3(-3.6, 0.2))
        ct = chip("atonal", ATO, size=40).move_to(P3(3.6, 0.2))
        pr = protein(cp, sc)
        tf = T("bHLH transcription factor", 38, PRO, weight=BOLD).move_to(P3(0, -3.35))
        l_basic = leader("basic", (-4.1, -1.5), (-0.55 * sc - 0.45, cp[1] - 0.75 * sc), 34, PRO)
        l_h1 = leader("helix", (-4.1, 0.9), (-0.55 * sc - 0.45, cp[1] + 0.55 * sc), 34, PRO)
        l_loop = leader("loop", (4.1, 2.9), (0.4 * sc, cp[1] + 1.75 * sc), 34, PRO)
        l_h2 = leader("helix", (4.1, 0.6), (0.55 * sc + 0.45, cp[1] + 0.55 * sc), 34, PRO)
        self.add(ca, ct, tf)
        self.at("same")
        self.play(ca.animate.move_to(P3(0, 1.0)), ct.animate.move_to(P3(0, -0.6)), run_time=0.7)
        self.at("protein", lead=0.5)
        self.play(FadeOut(ca[1]), FadeOut(ct[1]), run_time=0.25)
        self.at("protein", lead=0.0)
        self.play(ReplacementTransform(ca[0], pr), FadeOut(ct[0], target_position=pr.get_center()), run_time=0.8)
        self.at("basic")
        self.play(FadeIn(l_basic), Indicate(pr.basic, color=PRO, scale_factor=1.15), run_time=0.4)
        self.at("helix")
        self.play(FadeIn(l_h1), Indicate(pr.h1, color=PRO, scale_factor=1.1), run_time=0.4)
        self.at("transcription", lead=0.5)
        self.play(FadeIn(l_loop), Indicate(pr.loop, color=PRO, scale_factor=1.15), run_time=0.3)
        self.at("transcription", lead=0.2)
        self.play(FadeIn(l_h2), Indicate(pr.h2, color=PRO, scale_factor=1.1), run_time=0.4)
        self.finish()


class S14Bhlh2(SpokenScene):
    def construct(self):
        solo = protein((0, S13_CY), S13_SC)
        A, B = pair_group(together=False, dy=LIFT)
        Ap, Bp = pair_group(together=True, dy=LIFT)
        pbox = pair_box(LIFT)
        dna = dna_bar(DNA_Y)
        ebox = ebox_rect()
        lab = T("E-box", 40, TEXT, weight=BOLD).move_to(P3(0, DNA_Y - 0.8))
        tf = T("bHLH transcription factor", 38, PRO, weight=BOLD).move_to(P3(0, -3.35))
        self.add(solo, tf)
        self.play(ReplacementTransform(solo, A), FadeIn(B, shift=LEFT * 0.4), FadeOut(tf), run_time=0.9)
        self.at("part")
        self.play(Indicate(VGroup(A.h1, A.h2, A.loop), color=TEXT, scale_factor=1.06), Indicate(VGroup(B.h1, B.h2, B.loop), color=TEXT, scale_factor=1.06), run_time=0.7)
        self.at("pair")
        self.play(ReplacementTransform(A, Ap), ReplacementTransform(B, Bp), run_time=0.9)
        self.play(FadeIn(pbox), run_time=0.4)
        self.at("basic part")
        self.play(FadeIn(dna, shift=UP * 0.3), Indicate(Ap.basic, color=TEXT, scale_factor=1.2), Indicate(Bp.basic, color=TEXT, scale_factor=1.2), run_time=0.6)
        self.at("grips")
        self.play(VGroup(Ap, Bp, pbox).animate.shift(DOWN * LIFT), FadeOut(pbox), run_time=0.7)
        self.at("short sequence")
        self.play(FadeIn(ebox, scale=0.7), run_time=0.5)
        self.at("e box")
        self.play(FadeIn(lab, shift=UP * 0.1), run_time=0.5)
        self.finish()


def carried_pair():
    Ap, Bp = pair_group(together=True, colB=PART)
    return Ap, Bp, dna_bar(DNA_Y), ebox_rect(), T("E-box", 40, TEXT, weight=BOLD).move_to(P3(0, DNA_Y - 0.8))


LABX = 3.75


class S15Partner(SpokenScene):
    def construct(self):
        Ap, Bp, dna, ebox, lab = carried_pair()
        self.add(Ap, Bp, dna, ebox, lab)
        l_pro = leader("proneural\nprotein", (-5.3, 1.5), (-3.45, 1.2), 32, PRO)
        part = right_group([("partner", 34, PART, NORMAL)], LABX, 1.7)
        fly_dl = right_group([("fly:", 30, TEXT, NORMAL), ("Daughterless", 34, PART, NORMAL)], LABX, 1.7)
        lead = Line(P3(LABX - 0.1, 1.4), P3(3.25, 1.2), color=GREY, stroke_width=2.5).set_opacity(0.85)
        self.at("protein", lead=0.4)
        self.play(FadeIn(l_pro), Indicate(Ap, color=PRO, scale_factor=1.04), run_time=0.8)
        self.at("partner")
        self.play(Indicate(Bp, color=PART, scale_factor=1.05), FadeIn(part), FadeIn(lead), run_time=0.8)
        self.at("daughterless", lead=0.3)
        self.play(ReplacementTransform(part, fly_dl), run_time=0.6)
        self.finish()


class S16Partner2(SpokenScene):
    def construct(self):
        Ap, Bp, dna, ebox, lab = carried_pair()
        l_pro = leader("proneural\nprotein", (-5.3, 1.5), (-3.45, 1.2), 32, PRO)
        fly_dl = right_group([("fly:", 30, TEXT, NORMAL), ("Daughterless", 34, PART, NORMAL)], LABX, 1.7)
        lead1 = Line(P3(LABX - 0.1, 1.4), P3(3.25, 1.2), color=GREY, stroke_width=2.5).set_opacity(0.85)
        self.add(Ap, Bp, dna, ebox, lab, l_pro, fly_dl, lead1)
        vt = right_group([("vertebrates:", 38, TEXT, NORMAL), ("E proteins", 46, PART, BOLD)], LABX - 0.3, -0.45)
        lead2 = Line(P3(LABX - 0.4, -0.2), P3(3.2, 0.2), color=GREY, stroke_width=2.5).set_opacity(0.85)
        self.play(FadeIn(vt, shift=UP * 0.1), FadeIn(lead2), run_time=0.5)
        self.at("partners")
        self.play(Indicate(Bp, color=PART, scale_factor=1.04), Indicate(vt[1], color=PART, scale_factor=1.06), run_time=0.7)
        self.finish()


# ------------------------------------------------------------------------------------------------
FX, VX = -4.15, 4.3
TY_A, TY_N, TY_T, TY_H = 1.85, -0.35, -1.45, -2.55


def tree_parts():
    hf = T("fly", 40, TEXT, weight=BOLD).move_to(P3(FX, 3.4))
    hv = T("vertebrates", 40, TEXT, weight=BOLD).move_to(P3(VX, 3.4))
    c_a = chip("achaete-scute", PRO, size=42).move_to(P3(FX, TY_A))
    c_t = chip("atonal", ATO, size=42).move_to(P3(FX, TY_T))
    c_asc = chip("Ascl1 (Mash1)", PRO, size=42).move_to(P3(VX, TY_A))
    c_ng = chip("Neurogenins", ATO, size=42).move_to(P3(VX, TY_N))
    c_at = chip("Atoh1", ATO, size=42).move_to(P3(VX, TY_H))
    link_a = Line(P3(c_a.get_right()[0] + 0.1, TY_A), P3(c_asc.get_left()[0] - 0.1, TY_A), color=PRO, stroke_width=6)
    lab_a = T("related to", 30, TEXT).move_to(P3((c_a.get_right()[0] + c_asc.get_left()[0]) / 2, TY_A + 0.45))
    JX = 0.3
    trunk = Line(P3(c_t.get_right()[0] + 0.1, TY_T), P3(JX, TY_T), color=ATO, stroke_width=6)
    spine1 = Line(P3(JX, TY_T), P3(JX, TY_N), color=ATO, stroke_width=6)
    spine2 = Line(P3(JX, TY_T), P3(JX, TY_H), color=ATO, stroke_width=6)
    br_n = Line(P3(JX, TY_N), P3(c_ng.get_left()[0] - 0.1, TY_N), color=ATO, stroke_width=6)
    br_h = Line(P3(JX, TY_H), P3(c_at.get_left()[0] - 0.1, TY_H), color=ATO, stroke_width=6)
    lab_t = T("related to", 30, TEXT).move_to(P3((c_t.get_right()[0] + JX) / 2, TY_T + 0.45))
    ghost = lambda c: DashedVMobject(c[0].copy().set_fill(opacity=0).set_stroke(GREY, 3), num_dashes=36).set_opacity(0.8)
    return dict(hf=hf, hv=hv, c_a=c_a, c_t=c_t, c_asc=c_asc, c_ng=c_ng, c_at=c_at, link_a=link_a, lab_a=lab_a,
                trunk=trunk, spine1=spine1, spine2=spine2, br_n=br_n, br_h=br_h, lab_t=lab_t,
                g_asc=ghost(c_asc), g_ng=ghost(c_ng), g_at=ghost(c_at))


class S17Vert(SpokenScene):
    def construct(self):
        t = tree_parts()
        self.add(t["hf"], t["hv"], t["c_a"], t["c_t"])
        self.at("relatives")
        self.play(FadeIn(t["g_asc"]), FadeIn(t["g_ng"]), FadeIn(t["g_at"]), run_time=0.6)
        self.at("both")
        self.play(Indicate(t["c_a"], color=PRO, scale_factor=1.1), Indicate(t["c_t"], color=ATO, scale_factor=1.1), run_time=0.7)
        self.at("is related", lead=0.8)
        self.play(FadeOut(t["g_asc"]), FadeIn(t["c_asc"], scale=0.9), run_time=0.5)
        self.at("related to")
        self.play(Create(t["link_a"]), FadeIn(t["lab_a"], shift=UP * 0.1), run_time=0.7)
        self.at("related to", lead=-0.55)
        self.play(Indicate(t["c_a"], color=PRO, scale_factor=1.12), Indicate(t["c_asc"], color=PRO, scale_factor=1.1), run_time=0.7)
        self.finish()


class S18Vert2(SpokenScene):
    def construct(self):
        t = tree_parts()
        self.add(*[t[k] for k in ("hf", "hv", "c_a", "c_t", "c_asc", "link_a", "lab_a", "g_ng", "g_at")])
        self.at("neurogenins")
        self.play(FadeOut(t["g_ng"]), FadeIn(t["c_ng"], scale=0.9), Create(t["trunk"]), run_time=0.45)
        self.play(Create(t["spine1"]), Create(t["br_n"]), run_time=0.45)
        self.at("called", lead=-0.1)
        self.play(FadeOut(t["g_at"]), FadeIn(t["c_at"], scale=0.9), Create(t["spine2"]), Create(t["br_h"]), run_time=0.6)
        self.at("related to")
        self.play(FadeIn(t["lab_t"], shift=UP * 0.1), Indicate(t["c_t"], color=ATO, scale_factor=1.12),
                  VGroup(t["c_a"], t["c_asc"], t["link_a"], t["lab_a"]).animate.set_opacity(0.4), run_time=0.8)
        self.finish()


# ------------------------------------------------------------------------------------------------
CELLS_R = 0.43
FCY = -0.25
CL_CENTERS = [(-4.4, 1.2), (-0.5, 1.6), (3.8, 1.2), (-2.4, -1.3), (1.6, -1.2), (5.0, -1.5)]


def field():
    cells = {}
    rows, cols = 6, 12
    for r in range(rows):
        for c in range(cols):
            x = (c - (cols - 1) / 2 + 0.5 * (r % 2) - 0.25) * 1.0
            y = ((rows - 1) / 2 - r) * 0.866 + FCY
            cells[(r, c)] = Circle(radius=CELLS_R, stroke_color=GREY, stroke_width=2.5, fill_color=GREY, fill_opacity=0.08).move_to(P3(x, y))
    return cells


def pick_clusters(cells):
    used, out = set(), []
    for (cx, cy) in CL_CENTERS:
        c0 = P3(cx, cy + FCY)
        order = sorted((k for k in cells if k not in used), key=lambda k: np.linalg.norm(cells[k].get_center() - c0))
        pick = order[:5]
        used.update(pick)
        out.append(pick)
    return out


class S19Where(SpokenScene):
    def construct(self):
        cells = field()
        fgroup = VGroup(*cells.values())
        keys = list(cells.keys())
        clusters = pick_clusters(cells)
        clus = [VGroup(*[cells[k] for k in cl]) for cl in clusters]
        q = T("?", 170, GOLD, font=TITLE_FONT).move_to(P3(0, FCY))
        emb = T("embryo", 32, TEXT).move_to(P3(0, 3.4))
        notch = chip("Notch", NOT, size=34).move_to(P3(5.5, 3.3))
        xx = strike(notch, pad=0.1)
        # phase B: the embryo shrinks to the top third; the gene strip fills the lower 40%
        SS, SCY = 0.45, 2.55
        small = VGroup(*[c.copy() for c in fgroup]).scale(SS).move_to(P3(0, SCY))
        for c in small:
            c.set_stroke(width=2)
        small_cells = {k: small[i] for i, k in enumerate(keys)}
        for cl in clusters:
            for k in cl:
                small_cells[k].set_stroke(PRO, 3).set_fill(PRO, 0.3)
        ccen, cbot = [], []
        for cl in clusters:
            g = VGroup(*[small_cells[k] for k in cl])
            ccen.append(g.get_center())
            cbot.append(P3(g.get_center()[0], g.get_bottom()[1] - 0.02))
        order = sorted(range(6), key=lambda i: ccen[i][0])
        BY = -2.0
        dna = dna_bar(BY, 13.0, 0.55)
        g1 = Rectangle(width=1.9, height=1.6, stroke_color=PRO, stroke_width=3, fill_color=PRO, fill_opacity=0.4).move_to(P3(-1.05, BY))
        g2 = Rectangle(width=1.9, height=1.6, stroke_color=PRO, stroke_width=3, fill_color=PRO, fill_opacity=0.4).move_to(P3(1.05, BY))
        gn1 = T("achaete", 30, PRO, weight=BOLD).move_to(g1)
        gn2 = T("scute", 30, PRO, weight=BOLD).move_to(g2)
        sx = [-5.5, -4.4, -3.3, 3.3, 4.4, 5.5]
        sw = VGroup(*[Rectangle(width=0.62, height=0.62, stroke_color=GOLD, stroke_width=3, fill_color=GOLD, fill_opacity=0.35).move_to(P3(x, BY)) for x in sx])
        lines = [Line(P3(sx[j], BY + 0.31), cbot[order[j]], color=GOLD, stroke_width=3.5).set_opacity(0.9) for j in range(6)]
        for ln in lines:
            ln.set_z_index(-1)
        brl = Brace(sw[:3], DOWN, buff=0.15, color=GOLD)
        brr = Brace(sw[3:], DOWN, buff=0.15, color=GOLD)
        brg = Brace(VGroup(g1, g2), DOWN, buff=0.15, color=PRO)
        rl = T("regulatory DNA", 28, GOLD).next_to(brl, DOWN, buff=0.1)
        rr = T("regulatory DNA", 28, GOLD).next_to(brr, DOWN, buff=0.1)
        glab = T("achaete-scute genes", 28, PRO).next_to(brg, DOWN, buff=0.1)
        emb2 = T("embryo", 30, TEXT).move_to(P3(-5.1, SCY))
        self.play(FadeIn(fgroup), run_time=0.3)
        self.at("decides")
        self.play(FadeIn(q, scale=0.6), run_time=0.5)
        self.at("embryo")
        self.play(FadeOut(q), FadeIn(emb, shift=DOWN * 0.1), run_time=0.5)
        self.at("clusters still")
        self.play(LaggedStart(*[cl.animate.set_stroke(PRO, 5).set_fill(PRO, 0.3) for cl in clus], lag_ratio=0.12), run_time=1.0)
        self.at("right places")
        self.play(*[Indicate(cl, color=PRO, scale_factor=1.06) for cl in clus], run_time=0.5)
        self.at("without notch", lead=0.15)
        self.play(FadeIn(notch, shift=DOWN * 0.15), run_time=0.35)
        self.play(Create(xx), run_time=0.35)
        self.at("regulatory")
        self.play(Transform(fgroup, small), ReplacementTransform(emb, emb2), FadeIn(dna, shift=UP * 0.3), FadeIn(g1), FadeIn(g2), FadeIn(gn1), FadeIn(gn2), run_time=0.7)
        self.at("around the")
        self.play(LaggedStart(*[GrowFromCenter(s_) for s_ in sw], lag_ratio=0.1), GrowFromCenter(brl), GrowFromCenter(brr), FadeIn(rl), FadeIn(rr), run_time=0.8)
        self.at("genes", lead=0.3)
        self.play(GrowFromCenter(brg), FadeIn(glab, shift=UP * 0.1), run_time=0.4)
        self.at("sets the map", lead=0.1)
        for j in range(6):
            i = order[j]
            self.play(Create(lines[j]), sw[j].animate.set_fill(GOLD, 1.0),
                      *[cells[k].animate.set_stroke(GOLD, 4) for k in clusters[i]], run_time=0.25)
        self.finish()


# ------------------------------------------------------------------------------------------------
class S20Where2(SpokenScene):
    def construct(self):
        nc, nb = (-4.0, 0.25), 2.5
        na = NRAT * nb
        out, pts = notum_geom(nc, nb)
        marks = VGroup(*[Circle(radius=0.17, stroke_color=PRO, stroke_width=4, fill_color=PRO, fill_opacity=0.35).move_to(p)
                         for p in pts["dc"] + pts["sc"] + pts["lat"]])
        # wing: a leaf outline, with cluster marks placed inside it
        t = np.linspace(0, 2 * PI, 80)
        L, W, x0, yc = 5.2, 1.95, 1.3, 0.1
        half = lambda f: W * np.sqrt(max(0, 1 - (2 * f - 1) ** 2)) * (1.0 - 0.3 * (2 * f - 1))
        wp = [P3(x0 + L * (0.5 + 0.5 * np.cos(a)), yc + W * np.sin(a) * (1.0 - 0.3 * np.cos(a))) for a in t]
        wing = VMobject(stroke_color=GREY, stroke_width=4, fill_color=GREY, fill_opacity=0.08)
        wing.set_points_smoothly(wp + [wp[0]])
        wm = []
        for f in (0.25, 0.42, 0.6, 0.78):
            for s in (-0.62, 0.62):
                wm.append(P3(x0 + L * f, yc + s * half(f)))
        for f in (0.35, 0.55, 0.72):
            wm.append(P3(x0 + L * f, yc))
        wmarks = VGroup(*[Circle(radius=0.17, stroke_color=PRO, stroke_width=4, fill_color=PRO, fill_opacity=0.35).move_to(p) for p in wm])
        nlab = T("notum", 32, TEXT, weight=BOLD).move_to(P3(-5.95, nc[1] - nb - 0.55))
        wlab = T("wing", 32, TEXT, weight=BOLD).move_to(P3(x0 + L / 2, yc - W - 0.55))
        b1 = band_poly(nc, na, nb, -0.5, -0.14)
        b2 = band_poly(nc, na, nb, 0.14, 0.5)
        sl = T("proneural stripes", 32, PRO, weight=BOLD).move_to(P3(nc[0], 3.45))
        sl_a = Line(sl.get_bottom() + LEFT * 0.9 + DOWN * 0.05, P3(nc[0] - 0.32 * na, nc[1] + 1.9), color=PRO, stroke_width=2.5)
        sl_b = Line(sl.get_bottom() + RIGHT * 0.9 + DOWN * 0.05, P3(nc[0] + 0.32 * na, nc[1] + 1.9), color=PRO, stroke_width=2.5)
        nch = chip("Notch", NOT, size=38).move_to(P3(nc[0] + 0.7, nc[1] - nb - 0.7))
        nb_y = nc[1] - nb * 0.93 * np.sqrt(1 - 0.32 ** 2) + 0.5
        na1 = arr((nc[0] + 0.5, nch.get_top()[1] + 0.02), (nc[0] - 0.32 * na - 0.0, nb_y), NOT, 6)
        na2 = arr((nc[0] + 0.9, nch.get_top()[1] + 0.02), (nc[0] + 0.32 * na, nb_y), NOT, 6)
        self.add(out, marks)
        self.at("map")
        self.wait(0.6)
        self.at("notum")
        self.play(FadeIn(nlab, shift=UP * 0.1), run_time=0.4)
        self.at("wing")
        self.play(FadeIn(wing), run_time=0.5)
        self.play(FadeIn(wmarks, lag_ratio=0.05), FadeIn(wlab), run_time=0.7)
        self.at("there", lead=0.3)
        self.play(FadeIn(b1), FadeIn(b2), FadeIn(sl), Create(sl_a), Create(sl_b), run_time=0.6)
        self.at("notch", lead=0.0)
        self.play(FadeIn(nch, shift=UP * 0.15), run_time=0.4)
        self.play(GrowArrow(na1), GrowArrow(na2), run_time=0.5)
        self.at("stripes")
        self.play(Indicate(VGroup(b1, b2), color=PRO, scale_factor=1.03), run_time=0.7)
        self.finish()


# ------------------------------------------------------------------------------------------------
class S21Answer(SpokenScene):
    def construct(self):
        card = RoundedRectangle(width=9.0, height=1.3, corner_radius=0.2, stroke_color=GOLD, stroke_width=4, fill_color=GOLD, fill_opacity=0.1).move_to(P3(-0.6, 3.15))
        n1 = T("Puzzle 1", 30, GOLD).move_to(P3(-3.7, 3.15))
        wm = T("Who may?", 60, TEXT, font=TITLE_FONT).move_to(P3(-0.3, 3.15))
        ck = check_mark((3.0, 3.15), 1.0, GREEN, 14)
        cp = chip("Proneural factors", PRO, size=38).move_to(P3(-4.3, -1.2))
        cr = chip("Regulatory DNA", GOLD, size=38).move_to(P3(0, -3.35))
        tissue = VGroup(*[Circle(radius=0.88, stroke_color=GREY, stroke_width=4, fill_color=GREY, fill_opacity=0.08).move_to(P3(x, 1.0)) for x in np.linspace(-5.5, 5.5, 7)])
        mid = VGroup(*tissue[2:5])
        BRY = -0.28
        brk = VGroup(Line(P3(-2.75, BRY), P3(2.75, BRY), color=PRO, stroke_width=7),
                     Line(P3(-2.75, BRY), P3(-2.75, BRY + 0.3), color=PRO, stroke_width=7),
                     Line(P3(2.75, BRY), P3(2.75, BRY + 0.3), color=PRO, stroke_width=7))
        dna = dna_bar(-2.45, 12.8, 0.45)
        sq = Rectangle(width=0.62, height=0.62, stroke_color=GOLD, stroke_width=3, fill_color=GOLD, fill_opacity=1).move_to(P3(0, -2.45))
        ap = arr((-2.95, -1.0), (-1.45, BRY - 0.06), PRO, 7)
        stem = Line(P3(0, -2.1), P3(0, BRY - 0.04), color=GOLD, stroke_width=5)
        self.add(card, n1, wm, tissue, dna)
        self.at("factors", lead=0.5)
        self.play(FadeIn(cp, shift=DOWN * 0.15), run_time=0.5)
        self.at("able")
        self.play(Create(brk), GrowArrow(ap), mid.animate.set_stroke(PRO, 6).set_fill(PRO, 0.3), run_time=0.9)
        self.at("regulatory")
        self.play(FadeIn(cr, shift=UP * 0.15), run_time=0.5)
        self.at("places it", lead=0.3)
        self.play(FadeIn(sq, shift=DOWN * 0.5), Create(stem), mid.animate.set_stroke(GOLD, 6), brk.animate.set_color(GOLD), run_time=0.7)
        self.at("places it", lead=-0.5)
        self.play(Create(ck), run_time=0.6)
        self.finish()


class S22Takeaway(SpokenScene):
    def construct(self):
        l1 = VGroup(T("Proneural factors say", 56, PRO, font=TITLE_FONT), T("who may.", 56, TEXT, font=TITLE_FONT)).arrange(RIGHT, buff=0.25).move_to(P3(0, 3.2))
        l2 = VGroup(T("Notch", 56, NOT, font=TITLE_FONT), T("will say", 56, TEXT, font=TITLE_FONT), T("who does.", 56, TEXT, font=TITLE_FONT)).arrange(RIGHT, buff=0.25).move_to(P3(0, 2.3))
        cells = cluster_cells(0.9, (0, -0.65), GREY, 5)
        grp = VGroup(*cells.values())
        qm = T("?", 64, GOLD, font=TITLE_FONT).move_to(cells["C"])
        self.add(grp)
        self.at("factors", lead=0.5)
        self.play(FadeIn(l1, shift=UP * 0.15), grp.animate.set_stroke(PRO, 6).set_fill(PRO, 0.15), run_time=0.8)
        self.at("notch")
        self.play(FadeIn(l2, shift=UP * 0.15), cells["C"].animate.set_stroke(GOLD, 9).set_fill(GOLD, 0.12), FadeIn(qm, scale=0.6), run_time=0.6)
        self.at("who does")
        self.play(Indicate(qm, color=GOLD, scale_factor=1.25), run_time=0.5)
        self.finish()


class S23End(EndCard):
    LINE = "Proneural factors say who may. Notch will say who does."

    def construct(self):
        l1 = VGroup(T("Proneural factors say", 48, PRO, font=TITLE_FONT), T("who may.", 48, TEXT, font=TITLE_FONT)).arrange(RIGHT, buff=0.25)
        l2 = VGroup(T("Notch", 48, NOT, font=TITLE_FONT), T("will say who does.", 48, TEXT, font=TITLE_FONT)).arrange(RIGHT, buff=0.25)
        line = VGroup(l1, l2).arrange(DOWN, buff=0.4)
        sub = T("biochemistrypedia.com", 24, TEAL)
        g = VGroup(line, sub).arrange(DOWN, buff=0.6)
        self.add(line)
        self.wait(0.3)
        self.play(FadeIn(sub), run_time=self.beat(0.15))
        self.finish()
