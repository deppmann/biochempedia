"""Opening and closing a critical period, chapter 3: Brakes, and Borrowed Cells  (Biochemistrypedia explainer)

COLOR MAP (one color per concept, whole series; taken from the single-film version and extended)
  BLUE   = the closed or deprived eye and the cortex response to it
  ORANGE = the open (good) eye and the cortex response to it
  YELLOW = inhibition: GABA, the inhibition curve, parvalbumin cells
  PURPLE = the GAD enzymes that make GABA (not used in this chapter)
  PINK   = receptors (GABA, nicotinic, Nogo)
  TEAL   = what the experimenter adds: chondroitinase, nicotinic blocker, fluoxetine, diazepam
  GREEN  = the open window (plasticity possible) and the machinery for change
  GOLD   = the transplanted donor cells (hexagons) and the second window they bring
  RED    = brakes, and anything missing or blocked: the net, Nogo, Lynx1, the knockout
  GREY   = structure, frames, labels, the host's own neurons
Schematic note: the inhibition curve is one logistic in age; the window opens where it crosses the
threshold line and ends at a fixed age. Ages are schematic, not measured values.
"""
import numpy as np
from bp_style import *  # noqa: F401,F403

PURPLE = "#B58CD9"
ORANGE = "#F29E4C"
PINK = "#E58FB8"


def pt(x, y):
    return np.array([x, y, 0.0])


# ---------------------------------------------------------------------------------------------
# helpers
# ---------------------------------------------------------------------------------------------
def bchip(text, color=BLUE, size=26, **kw):
    c = chip(text, color, size=size, **kw)
    back = RoundedRectangle(corner_radius=0.14, width=c[0].width, height=c[0].height, stroke_width=0,
                            fill_color=BG, fill_opacity=1).move_to(c[0])
    return VGroup(back, *c)


def arr(a, b, color=GREY, w=5, tip=0.22):
    return Arrow(a, b, buff=0.06, color=color, stroke_width=w, tip_length=tip,
                 max_tip_length_to_length_ratio=0.45, max_stroke_width_to_length_ratio=12)


def inhib(a, b, color=RED, w=5):
    a, b = np.array(a, float), np.array(b, float)
    d = (b - a) / np.linalg.norm(b - a)
    b = b - d * 0.05
    perp = np.array([-d[1], d[0], 0])
    return VGroup(Line(a, b, color=color, stroke_width=w),
                  Line(b + perp * 0.26, b - perp * 0.26, color=color, stroke_width=w + 1))


def eye_open(color):
    return VGroup(Ellipse(width=0.9, height=0.5, stroke_color=color, stroke_width=4, fill_color=color, fill_opacity=0.15),
                  Dot(radius=0.12, color=color))


def eye_shut(color):
    lid = ArcBetweenPoints(LEFT * 0.45, RIGHT * 0.45, angle=-PI / 2.6, stroke_color=color, stroke_width=5)
    lashes = VGroup(*[Line(lid.point_from_proportion(p), lid.point_from_proportion(p) + DOWN * 0.12 + RIGHT * dx,
                           stroke_color=color, stroke_width=3) for p, dx in ((0.2, -0.04), (0.5, 0), (0.8, 0.04))])
    return VGroup(lid, lashes)


def credit(text, pos, left=False):
    return T(text, 24, GREY).move_to(pos, aligned_edge=LEFT if left else RIGHT)


def settle(scene, secs):
    """Hold the finished picture for at least `secs` after the last animation (and to the end of the narration)."""
    scene.wait(max(secs, scene.narration_s + 0.4 - scene.elapsed()))


def cross_over(mob, color=RED, w=6):
    c = mob.get_center()
    hw, hh = mob.width / 2 + 0.1, mob.height / 2 + 0.1
    return VGroup(Line(c + [-hw, hh, 0], c + [hw, -hh, 0], color=color, stroke_width=w),
                  Line(c + [-hw, -hh, 0], c + [hw, hh, 0], color=color, stroke_width=w))


# ---- the age axis and the inhibition curve (one model shared by every stage scene) -----------
def X(a):
    return -5.4 + 0.19 * a


def Lg(a):
    return 1.0 / (1.0 + np.exp(-(a - 20.0) / 14.0))


def Sg(a):
    return (Lg(a) - Lg(0)) / (Lg(60) - Lg(0))


AY = -2.3            # age axis of the stage
BAND_Y = 2.9         # row of the window bands on the stage


def Y(a):
    return AY + 0.2 + 3.8 * Sg(a)


def _solve_open(level=0.35):
    lo, hi = 0.0, 60.0
    for _ in range(60):
        mid = (lo + hi) / 2
        if Sg(mid) < level:
            lo = mid
        else:
            hi = mid
    return lo


A_OPEN = _solve_open()   # age where inhibition crosses the threshold line
A_END = 30.0             # usual closing age
YT = Y(A_OPEN)           # threshold height


def band(a0, a1, y, color=GREEN, op=0.55, h=0.6, sw=3):
    r = RoundedRectangle(corner_radius=0.1, width=X(a1) - X(a0), height=h, stroke_color=color, stroke_width=sw,
                         fill_color=color, fill_opacity=op)
    return r.move_to([(X(a0) + X(a1)) / 2, y, 0])


def closed_band(a0, a1, y, h=0.6):
    return band(a0, a1, y, GREY, 0.0, h, 2).set_stroke(opacity=0.6)


class Strip:
    """An age axis with young / adult labels; bands sit on the row `by` above it."""

    def __init__(self, ay):
        self.ay = ay
        self.by = ay + 0.75
        self.group = VGroup(Line([X(0), ay, 0], [X(62), ay, 0], color=GREY, stroke_width=3),
                            T("young", 26, GREY).move_to([X(8), ay - 0.4, 0]),
                            T("adult", 26, GREY).move_to([X(50), ay - 0.4, 0]))


def make_stage():
    d = {}
    d["axes"] = VGroup(Line([X(0), AY, 0], [X(62), AY, 0], color=GREY, stroke_width=3),
                       Line([X(0), AY, 0], [X(0), 2.0, 0], color=GREY, stroke_width=3))
    d["young"] = T("young", 26, GREY).move_to([X(8), AY - 0.4, 0])
    d["adult"] = T("adult", 26, GREY).move_to([X(50), AY - 0.4, 0])
    d["ylab"] = T("inhibition", 28, YELLOW).move_to([X(0) + 1.1, 2.2, 0])
    d["cA"] = ParametricFunction(lambda t: np.array([X(t), Y(t), 0]), t_range=[0, A_END], color=YELLOW, stroke_width=6)
    d["cB"] = ParametricFunction(lambda t: np.array([X(t), Y(t), 0]), t_range=[A_END, 60], color=YELLOW, stroke_width=6)
    d["cross"] = Dot([X(A_OPEN), YT, 0], radius=0.13, color=TEXT)
    d["tshort"] = DashedLine([X(0), YT, 0], [X(A_OPEN), YT, 0], color=TEXT, stroke_width=3)
    d["band"] = band(A_OPEN, A_END, BAND_Y)
    d["blab"] = T("window", 26, TEXT).move_to(d["band"])
    d["g1"] = DashedLine([X(A_OPEN), YT, 0], [X(A_OPEN), BAND_Y - 0.3, 0], color=GREEN, stroke_width=3)
    return d


# ---- cells ------------------------------------------------------------------------------------
def pv_cell(c, s=1.0):
    c = np.array(c, float)
    soma = Circle(radius=1.0 * s, stroke_color=YELLOW, stroke_width=5, fill_color=YELLOW, fill_opacity=0.35).move_to(c)
    dend = VGroup()
    for k in range(7):
        ang = k * TAU / 7 + 0.3
        d = np.array([np.cos(ang), np.sin(ang), 0])
        perp = np.array([-d[1], d[0], 0])
        p0, p1 = c + d * 1.0 * s, c + d * 1.65 * s
        dend.add(Line(p0, p1, color=YELLOW, stroke_width=4))
        dend.add(Line(p1, p1 + (d + perp * 0.7) * 0.3 * s, color=YELLOW, stroke_width=4))
        dend.add(Line(p1, p1 + (d - perp * 0.7) * 0.3 * s, color=YELLOW, stroke_width=4))
    return VGroup(soma, dend)


def pv_net(c, s=1.0, r1=1.2, r2=1.5, n=14, color=RED, sw=3.5):
    c = np.array(c, float)
    P = [c + np.array([np.cos(k * TAU / n), np.sin(k * TAU / n), 0]) * r1 * s for k in range(n)]
    Q = [c + np.array([np.cos((k + 0.5) * TAU / n), np.sin((k + 0.5) * TAU / n), 0]) * r2 * s for k in range(n)]
    net = VGroup()
    for k in range(n):
        net.add(Line(P[k], P[(k + 1) % n], color=color, stroke_width=sw))
        net.add(Line(Q[k], Q[(k + 1) % n], color=color, stroke_width=sw))
        net.add(Line(P[k], Q[k], color=color, stroke_width=sw))
        net.add(Line(P[(k + 1) % n], Q[k], color=color, stroke_width=sw))
    return net


def hexcell(c, r=0.24):
    return RegularPolygon(6, radius=r, stroke_color=GOLD, stroke_width=3, fill_color=GOLD, fill_opacity=0.55).move_to(c)


def mature_cell(c, r=0.2):
    c = np.array(c, float)
    body = Circle(radius=r, stroke_color=GOLD, stroke_width=3, fill_color=GOLD, fill_opacity=0.55).move_to(c)
    arms = VGroup(*[Line(c + np.array([np.cos(a), np.sin(a), 0]) * r, c + np.array([np.cos(a), np.sin(a), 0]) * (r * 1.1 + r),
                         color=GOLD, stroke_width=3) for a in (0.5, 2.4, 4.3)])
    return VGroup(body, arms)


def rat(s=1.0, c=ORIGIN):
    stk = dict(stroke_color=GREY, stroke_width=4, fill_color=GREY, fill_opacity=0.28)
    body = Ellipse(width=3.0, height=1.7, **stk)
    head = Ellipse(width=1.5, height=1.2, **stk).move_to([1.6, 0.3, 0])
    snout = Polygon([2.2, 0.75, 0], [3.1, 0.3, 0], [2.2, -0.15, 0], **stk)
    ear = Circle(radius=0.32, **stk).move_to([1.35, 1.0, 0])
    eye = Dot([2.0, 0.45, 0], radius=0.08, color=TEXT)
    nose = Dot([3.05, 0.3, 0], radius=0.1, color=PINK)
    tail = ArcBetweenPoints([-1.45, -0.1, 0], [-3.4, -0.95, 0], angle=-PI / 2.4, stroke_color=GREY, stroke_width=5)
    legs = VGroup(*[Line([x, -0.8, 0], [x - 0.1, -1.3, 0], color=GREY, stroke_width=6) for x in (-0.9, -0.4, 0.7, 1.2)])
    wh = VGroup(*[Line([2.8, 0.3, 0], [2.8 + 0.6, 0.3 + dy, 0], color=GREY, stroke_width=2.5) for dy in (0.3, 0.0, -0.3)])
    g = VGroup(tail, legs, body, head, ear, snout, eye, nose, wh)
    return g.scale(s).move_to(c)


# ---- a labelled predict card -------------------------------------------------------------------
def pred_header():
    return VGroup(T("Pause and predict", 44, TEXT, font=TITLE_FONT),
                  Line(LEFT * 1.4, RIGHT * 1.4, color=GOLD, stroke_width=4).shift(DOWN * 0.45)).move_to([0, 3.15, 0])


def tile(cx, cy=0.35, w=3.9, h=3.5):
    return RoundedRectangle(corner_radius=0.2, width=w, height=h, stroke_color=GREY, stroke_width=2.5).move_to([cx, cy, 0])


def card1_parts():
    """Predict card for the net: three tiles and the question. Returns dict of mobject groups."""
    p = {}
    p["head"] = pred_header()
    cx1, cx2, cx3 = -4.2, 0.0, 4.2
    cell = pv_cell(pt(cx1, 0.7), 0.6)
    net = pv_net(pt(cx1, 0.7), 0.6).set_stroke(opacity=0.35)
    xmark = cross_over(VGroup(Circle(radius=0.9).move_to(pt(cx1, 0.7))), RED, 6)
    t1 = T("net digested", 28, TEAL).move_to([cx1, -0.75, 0])
    p["t1"] = VGroup(tile(cx1), cell, net, xmark, t1)
    p["t2"] = VGroup(tile(cx2), rat(0.55, pt(cx2 - 0.15, 0.8)), T("adult rat", 28, TEXT).move_to([cx2, -0.75, 0]))
    shut = eye_shut(BLUE).scale(1.9).move_to(pt(cx3, 0.85))
    p["t3"] = VGroup(tile(cx3), shut, T("one eye closed", 28, BLUE).move_to([cx3, -0.75, 0]))
    p["q"] = T("Does the cortex shift?", 38, TEXT).move_to([0, -2.35, 0])
    c1 = bchip("shifts", GREEN, 30).move_to([-2.3, -3.2, 0])
    c2 = bchip("does not shift", RED, 30).move_to([2.3, -3.2, 0])
    p["chips"] = VGroup(c1, c2)
    return p


# =============================================================================================
class S00Title(TitleCard):
    LESSON = "Opening and closing a critical period"
    TITLE = "Brakes, and Borrowed Cells"


# ---------------------------------------------------------------------------------------------
class S01Q(SpokenScene):
    """The window ends; what closes it? Does the machinery wear out?"""

    def construct(self):
        st = make_stage()
        self.play(FadeIn(st["axes"], run_time=0.2), FadeIn(st["young"], run_time=0.2), FadeIn(st["adult"], run_time=0.2))
        self.at("maturing inhibition")
        self.play(FadeIn(st["ylab"], run_time=0.4),
                  Succession(Create(st["cA"], run_time=0.55), Create(st["cB"], run_time=0.3)))
        self.at("opens the window")
        self.play(Create(st["tshort"], run_time=0.3), FadeIn(st["cross"], run_time=0.3))
        self.play(Create(st["g1"], run_time=0.3), GrowFromEdge(st["band"], LEFT, run_time=0.6))
        self.play(FadeIn(st["blab"], run_time=0.3))
        self.at("what closes it")
        endbar = Line([X(A_END), BAND_Y - 0.42, 0], [X(A_END), BAND_Y + 0.42, 0], color=RED, stroke_width=9)
        q = T("?", 80, YELLOW, weight=BOLD).move_to([X(A_END) + 0.6, BAND_Y, 0])
        self.play(Create(endbar, run_time=0.3), FadeIn(q, scale=0.5, run_time=0.5))
        self.play(Indicate(q, color=YELLOW, scale_factor=1.2, run_time=0.7))
        self.at("Does the machinery")
        m1 = bchip("machinery for change", GREEN, 30).move_to([2.6, -0.3, 0])
        self.play(FadeIn(m1, shift=UP * 0.15, run_time=0.6))
        self.at("wear out")
        m2 = bchip("wears out?", GREY, 30).move_to(m1)
        self.play(ReplacementTransform(m1, m2, run_time=0.6))
        self.finish()


# ---------------------------------------------------------------------------------------------
class S02Decay(SpokenScene):
    """Worn-out machinery versus machinery held by a brake; one molecule is removed from each."""

    def construct(self):
        LX, RX, CY, W, H = -3.4, 3.4, 0.1, 5.5, 4.2
        lbox = RoundedRectangle(corner_radius=0.2, width=W, height=H, stroke_color=GREY, stroke_width=4,
                                fill_color=GREY, fill_opacity=0.1).move_to([LX, CY, 0])
        lbox.set_stroke(opacity=0.8)
        crack = VMobject(color=GREY, stroke_width=5).set_points_as_corners(
            [pt(LX - 0.5, CY + H / 2), pt(LX - 0.1, CY + 0.7), pt(LX - 0.7, CY), pt(LX - 0.1, CY - 0.7), pt(LX - 0.5, CY - H / 2)])
        ltxt = T("machinery", 34, GREY).move_to([LX + 1.1, CY, 0])
        lcap = T("worn out?", 34, GREY).move_to([LX, CY - H / 2 - 0.4, 0])
        left = VGroup(lbox, crack, ltxt, lcap)
        rbox = RoundedRectangle(corner_radius=0.2, width=W, height=H, stroke_color=GREEN, stroke_width=4,
                                fill_color=GREEN, fill_opacity=0.18).move_to([RX, CY, 0])
        rtxt = T("machinery", 34, GREEN).move_to([RX - 0.7, CY, 0])
        brake = inhib([RX + 1.9, CY + H / 2 + 1.0, 0], [RX + 1.9, CY + H / 2 + 0.05, 0], RED, 8)
        rcap = T("held by a brake?", 34, RED).move_to([RX, CY - H / 2 - 0.4, 0])
        right = VGroup(rbox, rtxt, brake, rcap)
        self.play(FadeIn(left, run_time=0.5), FadeIn(right, run_time=0.5))
        self.at("removing one molecule")
        top = CY + H / 2
        cl = bchip("remove one molecule", TEAL, 26).move_to([LX - 0.9, 3.35, 0])
        cr = bchip("remove one molecule", TEAL, 26).move_to([RX - 0.9, 3.35, 0])
        al = arr([LX - 0.9, 2.95, 0], [LX - 0.9, top - 0.1, 0], TEAL, 5, 0.2)
        ar = arr([RX - 0.9, 2.95, 0], [RX - 0.9, top - 0.1, 0], TEAL, 5, 0.2)
        self.play(FadeIn(cl, shift=DOWN * 0.15), FadeIn(cr, shift=DOWN * 0.15), GrowArrow(al), GrowArrow(ar), run_time=0.7)
        qm = T("?", 90, YELLOW, weight=BOLD).move_to([RX + 1.7, CY - 0.1, 0])
        self.play(FadeIn(qm, scale=0.6, run_time=0.4))
        self.at("bring the window back")
        ly = -3.3
        lamp1 = Circle(radius=0.38, stroke_color=GREY, stroke_width=4, fill_color=GREY, fill_opacity=0.3).move_to([LX - 1.7, ly, 0])
        ltx = T("window stays shut", 30, GREY).next_to(lamp1, RIGHT, buff=0.25)
        lamp2 = Circle(radius=0.38, stroke_color=YELLOW, stroke_width=4, fill_opacity=0).move_to([RX - 1.0, ly, 0])
        q2 = T("?", 36, YELLOW, weight=BOLD).move_to(lamp2)
        rtx = T("window?", 30, YELLOW).next_to(lamp2, RIGHT, buff=0.25)
        self.play(FadeIn(VGroup(lamp1, ltx), run_time=0.4), FadeIn(VGroup(lamp2, q2, rtx), run_time=0.4))
        self.finish()


# ---------------------------------------------------------------------------------------------
class S03Net(SpokenScene):
    """A perineuronal net condenses around a parvalbumin cell as the window ends."""

    def construct(self):
        C = pt(0, 0.5)
        S = 1.15
        st = Strip(-3.2)
        top = band(A_OPEN, A_END, st.by)
        toplab = T("window", 26, TEXT).move_to(top)
        cell = pv_cell(C, S)
        self.play(FadeIn(cell, run_time=0.45), FadeIn(st.group, run_time=0.3), FadeIn(top, run_time=0.3), FadeIn(toplab, run_time=0.3))
        self.at("window ends")
        cap = Line([X(A_END), st.by - 0.5, 0], [X(A_END), st.by + 0.5, 0], color=RED, stroke_width=8)
        self.play(Create(cap, run_time=0.4))
        self.at("lattice of matrix")
        net = pv_net(C, S, sw=4.5)
        loose = pv_net(C, S, sw=4.5).scale(1.4, about_point=C).set_stroke(opacity=0.6)
        self.play(FadeIn(loose, run_time=0.6))
        self.at("called a")
        nlab = T("perineuronal net", 30, RED).move_to([4.35, 2.1, 0])
        nptr = Line(C + np.array([1.83, 1.54, 0]), [2.55, 2.08, 0], color=RED, stroke_width=3)
        self.play(FadeIn(nlab, shift=DOWN * 0.1, run_time=0.5), Create(nptr, run_time=0.5))
        self.at("net condenses")
        self.play(Transform(loose, net.copy().set_stroke(opacity=1.0)), run_time=1.5)
        self.at("many parvalbumin cells")
        pl = T("parvalbumin cell", 30, YELLOW).move_to([0, 3.4, 0])
        side = VGroup()
        for sx in (-4.9, 4.9):
            sc = pt(sx, 0.2)
            side.add(pv_cell(sc, 0.62), pv_net(sc, 0.62, sw=3.5))
        self.play(FadeIn(pl, run_time=0.4), FadeIn(side, run_time=0.8))
        self.finish()


# ---------------------------------------------------------------------------------------------
class S04Pred(SpokenScene):
    def construct(self):
        p = card1_parts()
        self.play(FadeIn(p["head"], run_time=0.5))
        self.at("Digest that net")
        self.play(FadeIn(p["t1"], shift=UP * 0.15, run_time=0.6))
        self.at("adult rat")
        self.play(FadeIn(p["t2"], shift=UP * 0.15, run_time=0.6))
        self.at("close one eye")
        self.play(FadeIn(p["t3"], shift=UP * 0.15, run_time=0.6))
        self.at("Does the cortex")
        self.play(FadeIn(p["q"], run_time=0.5))
        self.at("shift")
        self.play(FadeIn(p["chips"], shift=UP * 0.1, run_time=0.5))
        self.finish()


class S05Pause(NarratedScene):
    def construct(self):
        p = card1_parts()
        self.add(*p.values())
        self.finish()


# ---------------------------------------------------------------------------------------------
def bar(x, base, h, color, w=0.75):
    return Rectangle(width=w, height=max(h, 0.02), stroke_width=0, fill_color=color, fill_opacity=0.9).move_to([x, base + max(h, 0.02) / 2, 0])


class S06Reveal(SpokenScene):
    """Chondroitinase dissolves the net; the adult band reopens and the cortex shifts."""

    def construct(self):
        C = pt(-4.2, 0.45)
        cell = pv_cell(C, 1.2)
        cell_lab = T("adult cortex cell", 28, TEXT).move_to([-4.2, -1.95, 0])
        net = pv_net(C, 1.2, sw=4)
        st = Strip(-3.2)
        usual = band(A_OPEN, A_END, st.by)
        ulab = T("window", 26, TEXT).move_to(usual)
        adult_closed = closed_band(46, 58, st.by)
        clo0 = T("closed", 26, GREY).move_to(adult_closed)
        # the bar chart: untreated adult pair first, treated pair arrives on the result
        base, bx0 = -0.8, 1.9
        axes = VGroup(Line([bx0, base, 0], [6.7, base, 0], color=GREY, stroke_width=3),
                      Line([bx0, base, 0], [bx0, 2.5, 0], color=GREY, stroke_width=3))
        ylab = T("cortex response", 24, GREY).rotate(PI / 2).move_to([bx0 - 0.5, 0.85, 0])
        lg1 = VGroup(Square(0.28, stroke_width=0, fill_color=BLUE, fill_opacity=0.9), T("response to closed eye", 24, BLUE))
        lg1[1].next_to(lg1[0], RIGHT, buff=0.15)
        lg2 = VGroup(Square(0.28, stroke_width=0, fill_color=ORANGE, fill_opacity=0.9), T("response to open eye", 24, ORANGE))
        lg2[1].next_to(lg2[0], RIGHT, buff=0.15)
        legend = VGroup(lg1, lg2).arrange(DOWN, aligned_edge=LEFT, buff=0.2).move_to([4.4, 3.2, 0])
        b1c, b1o = bar(3.0, base, 1.9, BLUE), bar(3.85, base, 1.9, ORANGE)
        g1 = T("adult,\nno enzyme", 24, TEXT, line_spacing=0.8).move_to([3.42, base - 0.6, 0])
        chart = VGroup(axes, ylab, legend, b1c, b1o, g1)
        self.play(FadeIn(cell, run_time=0.5), FadeIn(cell_lab, run_time=0.5), FadeIn(net, run_time=0.5), FadeIn(st.group, run_time=0.5),
                  FadeIn(usual, run_time=0.5), FadeIn(ulab, run_time=0.5), FadeIn(adult_closed, run_time=0.5), FadeIn(clo0, run_time=0.5),
                  FadeIn(chart, run_time=0.6))
        self.at("an enzyme", lead=0.5)
        enz = bchip("chondroitinase\nABC", TEAL, 26).move_to([-0.3, 2.35, 0])
        cr = credit("Pizzorusso and colleagues, 2002", pt(-6.7, 3.55), left=True)
        self.play(FadeIn(enz, shift=DOWN * 0.2, run_time=0.5), FadeIn(cr, run_time=0.5))
        self.at("cuts the net's")
        self.play(enz.animate.move_to([-0.3, 0.45, 0]), run_time=0.8)
        self.at("sugar chains")
        outs = []
        for l in net:
            v = l.get_center() - C
            v = v / (np.linalg.norm(v) + 1e-6)
            outs.append(l.animate.shift(v * 0.3).set_opacity(0.0))
        self.play(LaggedStart(*outs, lag_ratio=0.01, run_time=1.1))
        self.at("let deprivation shift")
        adult_open = band(46, 58, st.by)
        alab = T("reopened", 26, TEXT).move_to(adult_open)
        b2c, b2o = bar(5.35, base, 0.45, BLUE), bar(6.2, base, 2.7, ORANGE)
        g2 = T("adult,\nenzyme", 24, TEXT, line_spacing=0.8).move_to([5.78, base - 0.6, 0])
        self.play(Transform(adult_closed, adult_open), FadeOut(clo0), FadeIn(alab), FadeIn(g2),
                  GrowFromEdge(b2c, DOWN), GrowFromEdge(b2o, DOWN), run_time=1.0)
        settle(self, 2.0)
        self.finish()


# ---------------------------------------------------------------------------------------------
class S08Nogo(SpokenScene):
    """Myelin carries Nogo; with the Nogo receptor removed, the band stretches past its usual end."""

    def construct(self):
        myel = RoundedRectangle(corner_radius=0.3, width=10.4, height=0.8, stroke_color=GREY, stroke_width=3,
                                fill_color=GREY, fill_opacity=0.28).move_to([-0.3, 2.65, 0])
        mlab = T("myelin", 30, TEXT).move_to([-4.6, 2.65, 0])
        st = Strip(-3.0)
        usual = band(A_OPEN, A_END, st.by)
        ulab = T("window", 26, TEXT).move_to(usual)
        umark = DashedLine([X(A_END), st.ay, 0], [X(A_END), st.by + 0.9, 0], color=TEXT, stroke_width=3)
        utxt = T("usual closing age", 26, TEXT).move_to([X(A_END) + 0.15, st.by + 1.15, 0], aligned_edge=LEFT)
        cr = credit("McGee and colleagues, 2005", pt(6.6, 3.55))
        self.play(FadeIn(myel, run_time=0.5), FadeIn(mlab, run_time=0.5), FadeIn(st.group, run_time=0.5),
                  FadeIn(usual, run_time=0.5), FadeIn(ulab, run_time=0.5), FadeIn(umark, run_time=0.5),
                  FadeIn(utxt, run_time=0.5), FadeIn(cr, run_time=0.5))
        self.at("proteins")
        sq_kw = dict(width=0.6, height=0.6, stroke_color=RED, stroke_width=3, fill_color=RED, fill_opacity=0.55)
        sqa = Rectangle(**sq_kw).move_to([-3.6, 1.75, 0])
        sqb = Rectangle(**sq_kw).move_to([3.4, 1.75, 0])
        olab = VGroup(T("other myelin\nproteins", 24, RED, line_spacing=0.8).move_to([-3.6, 1.02, 0]),
                      T("other myelin\nproteins", 24, RED, line_spacing=0.8).move_to([3.4, 1.02, 0]))
        self.play(FadeIn(sqa, shift=DOWN * 0.1, run_time=0.4), FadeIn(sqb, shift=DOWN * 0.1, run_time=0.4), FadeIn(olab, run_time=0.4))
        self.at("no go")
        ng = bchip("Nogo", RED, 32).move_to([-0.4, 1.75, 0])
        self.play(FadeIn(ng, shift=DOWN * 0.1, run_time=0.4))
        self.at("Mice lacking")
        mem = Rectangle(width=11.0, height=0.25, stroke_width=0, fill_color=GREY, fill_opacity=0.6).move_to([0, -0.05, 0])
        rec = RoundedRectangle(corner_radius=0.14, width=1.2, height=1.1, stroke_color=PINK, stroke_width=5,
                               fill_color=PINK, fill_opacity=0.7).move_to([-0.4, 0.5, 0])
        a1 = arr([-0.4, 1.38, 0], [-0.4, 1.12, 0], RED, 4, 0.14)
        rlab = T("Nogo receptor", 30, PINK).move_to([-3.6, -0.85, 0])
        lead = Line([-2.2, -0.75, 0], [-0.95, -0.14, 0], color=PINK, stroke_width=3)
        # Establish the labelled receptor before its spoken name, then remove it.
        self.add(rec, rlab, lead)
        self.play(FadeIn(mem, run_time=0.3), FadeIn(a1, run_time=0.3))
        self.at("the no go receptor")
        gone = cross_over(rec, RED, 7)
        self.play(Create(gone, run_time=0.5))
        self.play(rec.animate.set_fill(opacity=0.25), a1.animate.set_opacity(0.2), run_time=0.4)
        self.at("kept plasticity")
        ext = band(A_END, 38, st.by)
        elab = T("plasticity continues", 26, GREEN).move_to([X(38) + 0.15, st.by, 0], aligned_edge=LEFT)
        self.play(GrowFromEdge(ext, LEFT), FadeIn(elab), run_time=1.6)
        self.at("closing age")
        self.play(Indicate(umark, color=TEXT, scale_factor=1.05), Indicate(utxt, color=TEXT, scale_factor=1.05), run_time=0.8)
        settle(self, 1.2)
        self.finish()


# ---------------------------------------------------------------------------------------------
NIC_X = 1.0


def nic_parts(fill=0.65):
    mem = Rectangle(width=11.0, height=0.45, stroke_width=0, fill_color=GREY, fill_opacity=0.6).move_to([0, 0.9, 0])
    rec = RoundedRectangle(corner_radius=0.2, width=2.4, height=3.9, stroke_color=PINK, stroke_width=5,
                           fill_color=PINK, fill_opacity=fill).move_to([NIC_X, 0.9, 0])
    rlab = T("nicotinic receptor", 28, PINK).move_to([NIC_X, -1.4, 0])
    return mem, rec, rlab


def nic_slot(st):
    """The adult slot: label naming the mutant, and the band that is '?' / open / closed."""
    lab = T("adult, no Lynx1", 26, RED).move_to([X(52), st.by + 0.7, 0])
    return lab


class S09Lynx(SpokenScene):
    def construct(self):
        mem, rec, rlab = nic_parts(0.35)
        st = Strip(-3.2)
        lyn = Ellipse(width=1.7, height=1.3, stroke_color=RED, stroke_width=4, fill_color=RED, fill_opacity=0.6).move_to([-3.0, 1.2, 0])
        llab = T("Lynx1", 38, RED).move_to([-3.0, 2.75, 0])
        slot = closed_band(46, 58, st.by)
        qm = T("?", 40, YELLOW, weight=BOLD).move_to(slot)
        cr = credit("Morishita and colleagues, 2010", pt(6.6, 3.55))
        nl = nic_slot(st)
        self.add(mem, rec, nl, slot, qm)
        self.play(FadeIn(lyn, run_time=0.5), FadeIn(llab, run_time=0.5),
                  FadeIn(st.group, run_time=0.4), FadeIn(cr, run_time=0.4))
        self.at("small membrane")
        sm = T("small membrane protein", 26, RED).move_to([-3.0, -0.1, 0])
        self.play(FadeIn(sm, run_time=0.5))
        self.at("damps")
        bar_ = inhib([-2.0, 1.4, 0], [NIC_X - 1.25, 1.4, 0], RED, 7)
        self.play(Create(bar_, run_time=0.45))
        self.at("nicotinic receptors")
        self.play(FadeIn(rlab, run_time=0.4))
        self.at("Adult mice")
        self.play(Indicate(nl, color=RED, scale_factor=1.04, run_time=0.25))
        self.at("without it")
        self.play(FadeOut(VGroup(lyn, llab, sm, bar_), run_time=0.5), rec.animate.set_fill(opacity=0.65), run_time=0.5)
        self.at("kept strong")
        adult_open = band(46, 58, st.by)
        alab = T("open", 26, TEXT).move_to(adult_open)
        self.play(Transform(slot, adult_open), FadeOut(qm), FadeIn(alab), run_time=0.8)
        settle(self, 1.2)
        self.finish()


class S10Nic(SpokenScene):
    def construct(self):
        mem, rec, rlab = nic_parts(0.65)
        st = Strip(-3.2)
        adult_open = band(46, 58, st.by)
        alab = T("open", 26, TEXT).move_to(adult_open)
        nl = nic_slot(st)
        self.add(mem, rec, rlab, st.group, adult_open, alab, nl)
        self.at("Blocking")
        blk = bchip("blocker", TEAL, 32).move_to([NIC_X, 3.4, 0])
        self.play(FadeIn(blk, shift=DOWN * 0.3, run_time=0.5))
        self.play(rec.animate.set_fill(opacity=0.15), Create(inhib([NIC_X, 3.0, 0], [NIC_X, 2.75, 0], TEAL, 7)), run_time=0.4)
        self.at("prevented that")
        shut = closed_band(46, 58, st.by)
        slab_ = T("closed", 26, RED).move_to(adult_open)
        self.play(Transform(adult_open, shut), FadeOut(alab), FadeIn(slab_), run_time=0.6)
        settle(self, 1.5)
        self.finish()


# ---------------------------------------------------------------------------------------------
def stage_full():
    """Stage at the end of s11: red brake part, threshold, band, window label."""
    st = make_stage()
    st["cB"].set_color(RED)
    st["thr"] = DashedLine([X(A_OPEN), YT, 0], [X(62), YT, 0], color=TEXT, stroke_width=3)
    st["thrl"] = T("threshold", 26, TEXT).move_to([X(8), YT + 0.4, 0])
    st["g2"] = DashedLine([X(A_END), Y(A_END), 0], [X(A_END), BAND_Y - 0.3, 0], color=RED, stroke_width=3)
    st["bk"] = T("brake", 28, RED).move_to([X(44), Y(44) + 0.5, 0])
    st["slot"] = closed_band(46, 58, BAND_Y)
    return st


STAGE_KEYS = ("axes", "young", "adult", "ylab", "cA", "cB", "cross", "tshort", "g1", "band", "blab", "thr", "thrl", "g2", "bk")


class S11Inh(SpokenScene):
    def construct(self):
        st = make_stage()
        base = [st[k] for k in ("axes", "young", "adult", "ylab", "cA", "cB", "cross", "tshort", "g1", "band", "blab")]
        self.add(*base)
        self.at("Inhibition itself")
        self.wait(0.1)
        self.at("second job")
        sj = bchip("a second job", YELLOW, 30).move_to([2.8, -0.6, 0])
        self.play(FadeIn(sj, shift=UP * 0.15, run_time=0.5))
        self.at("Past the threshold")
        thr = DashedLine([X(A_OPEN), YT, 0], [X(62), YT, 0], color=TEXT, stroke_width=3)
        thrl = T("threshold", 26, TEXT).move_to([X(8), YT + 0.4, 0])
        self.play(FadeOut(sj, run_time=0.3), Create(thr, run_time=0.5), FadeIn(thrl, run_time=0.4))
        self.at("keeps maturing")
        dot = Dot([X(A_OPEN), YT, 0], radius=0.16, color=TEXT)
        path = ParametricFunction(lambda t: np.array([X(t), Y(t), 0]), t_range=[A_OPEN, 52], stroke_opacity=0)
        self.add(dot)
        self.play(MoveAlongPath(dot, path), run_time=1.1, rate_func=linear)
        self.at("becomes a")
        g2 = DashedLine([X(A_END), Y(A_END), 0], [X(A_END), BAND_Y - 0.3, 0], color=RED, stroke_width=3)
        bk = T("brake", 28, RED).move_to([X(44), Y(44) + 0.5, 0])
        self.play(st["cB"].animate.set_color(RED), Create(g2), FadeIn(bk, shift=DOWN * 0.1), run_time=0.8)
        settle(self, 1.0)
        self.finish()


DOT_S12 = 0.55      # adult dot after "less GABA" (just below the curve's adult height)
DOT_S13 = -0.4      # adult dot after fluoxetine (nearer the threshold line)


class S12Harauzov(SpokenScene):
    def construct(self):
        st = stage_full()
        adot = Dot([X(52), Y(52), 0], radius=0.16, color=TEXT)
        self.add(*[st[k] for k in STAGE_KEYS])
        self.at("In adult rats")
        slot = st["slot"]
        clab0 = T("closed", 26, GREY).move_to([X(46) - 0.2, BAND_Y, 0], aligned_edge=RIGHT)
        alab = T("adult rat", 26, TEXT).move_to([X(52) + 1.0, Y(52) - 0.45, 0])
        self.play(FadeIn(slot, run_time=0.4), FadeIn(clab0, run_time=0.4), FadeIn(adot, scale=0.5, run_time=0.4), FadeIn(alab, run_time=0.4))
        self.at("reducing")
        down = arr([X(52) - 0.5, Y(52) - 0.2, 0], [X(52) - 0.5, DOT_S12 + 0.2, 0], TEAL, 6)
        lab = T("less GABA\ntransmission", 26, TEAL, line_spacing=0.8).move_to([2.0, -0.1, 0])
        self.play(GrowArrow(down, run_time=0.5), FadeIn(lab, run_time=0.5))
        self.play(adot.animate.move_to([X(52), DOT_S12, 0]), alab.animate.move_to([X(52) + 1.0, DOT_S12 - 0.45, 0]), run_time=0.8)
        self.at("partly restored")
        part = band(46, 52, BAND_Y, GREEN, 0.5)
        part.move_to([X(46) + part.width / 2, BAND_Y, 0])
        plab = T("partly", 26, TEXT).move_to([X(46) - 0.2, BAND_Y, 0], aligned_edge=RIGHT)
        cr = credit("Harauzov and colleagues, 2010", pt(6.6, -3.55))
        self.play(GrowFromEdge(part, LEFT), ReplacementTransform(clab0, plab), FadeIn(cr), run_time=0.8)
        settle(self, 1.5)
        self.finish()


class S13Fluox(SpokenScene):
    def construct(self):
        st = stage_full()
        adot = Dot([X(52), Y(52), 0], radius=0.16, color=TEXT)
        alab = T("adult rat", 26, TEXT).move_to([X(52) + 1.0, Y(52) - 0.45, 0])
        cr = credit("Maya Vetencourt and colleagues, 2008", pt(6.6, -3.55))
        clab0 = T("closed", 26, GREY).move_to([X(46) - 0.2, BAND_Y, 0], aligned_edge=RIGHT)
        self.add(*[st[k] for k in STAGE_KEYS], st["slot"], clab0, adot, alab, cr)
        self.at("weeks")
        wk = arr([X(30), -1.7, 0], [X(52) - 0.1, -1.7, 0], TEAL, 5)
        wkl = T("weeks", 26, TEAL).move_to([X(41), -1.3, 0])
        self.play(GrowArrow(wk), FadeIn(wkl), run_time=0.9)
        self.at("fluoxetine")
        fl = bchip("fluoxetine", TEAL, 26).move_to([-1.3, -1.7, 0])
        self.play(FadeIn(fl, shift=UP * 0.1, run_time=0.5))
        self.at("lowered inhibition")
        down = arr([X(52) - 0.5, Y(52) - 0.2, 0], [X(52) - 0.5, DOT_S13 + 0.25, 0], TEAL, 6)
        self.play(GrowArrow(down, run_time=0.3))
        self.play(adot.animate.move_to([X(52), DOT_S13, 0]), alab.animate.move_to([X(52) + 1.0, DOT_S13 + 0.5, 0]), run_time=0.8)
        self.at("restored plasticity")
        rest = band(46, 58, BAND_Y, GREEN, 0.55)
        rest.move_to([X(46) + rest.width / 2, BAND_Y, 0])
        flab = T("restored", 26, TEXT).move_to([X(46) - 0.2, BAND_Y, 0], aligned_edge=RIGHT)
        self.play(Transform(st["slot"], rest), ReplacementTransform(clab0, flab), run_time=0.8)
        self.at("Diazepam")
        dz = bchip("diazepam", TEAL, 26).move_to([2.6, -0.15, 0])
        self.play(FadeIn(dz, shift=UP * 0.1, run_time=0.3))
        up = arr([X(52) - 0.5, DOT_S13 + 0.25, 0], [X(52) - 0.5, Y(52) - 0.2, 0], TEAL, 6)
        self.at("blocked that")
        shut = closed_band(46, 58, BAND_Y)
        clab = T("closed", 26, RED).move_to([X(46) - 0.2, BAND_Y, 0], aligned_edge=RIGHT)
        self.play(FadeOut(down), GrowArrow(up), adot.animate.move_to([X(52), Y(52), 0]),
                  alab.animate.move_to([X(52) + 1.0, Y(52) - 0.45, 0]),
                  Transform(st["slot"], shut), ReplacementTransform(flab, clab), run_time=0.6)
        settle(self, 1.8)
        self.finish()


# ---------------------------------------------------------------------------------------------
GB, GH, GW = -2.9, 4.3, 1.7


def gauge_parts(cx, level):
    outline = Rectangle(width=GW, height=GH, stroke_color=GREY, stroke_width=4).move_to([cx, GB + GH / 2, 0])
    inner = GH - 0.1
    h = max(level * inner, 0.03)
    fill = Rectangle(width=GW - 0.12, height=h, stroke_width=0, fill_color=YELLOW, fill_opacity=0.8).move_to([cx, GB + 0.05 + h / 2, 0])
    yt = GB + 0.05 + 0.45 * inner
    thr = DashedLine([cx - GW / 2 - 0.2, yt, 0], [cx + GW / 2 + 0.2, yt, 0], color=TEXT, stroke_width=4)
    yb = GB + 0.05 + 0.78 * inner
    ytop = GB + GH - 0.05
    zone = Rectangle(width=GW - 0.12, height=ytop - yb, stroke_width=0, fill_color=RED, fill_opacity=0.28).move_to([cx, (yb + ytop) / 2, 0])
    zlab = T("brake", 26, RED).move_to([cx + 1.4, (yb + ytop) / 2, 0])
    return outline, fill, thr, zone, zlab


def lamp_parts(x, state):
    col = GREEN if state else GREY
    lamp = Circle(radius=0.6, stroke_color=col, stroke_width=5, fill_color=col, fill_opacity=0.9 if state else 0.3).move_to([x, 0.5, 0])
    wl = T("window", 28, TEXT).move_to([x, -0.5, 0])
    st = T("open" if state else "closed", 28, GREEN if state else RED).move_to([x, -1.05, 0])
    return lamp, wl, st


class S14Mirror(SpokenScene):
    def construct(self):
        div = Line([0, -3.4, 0], [0, 3.6, 0], color=GREY, stroke_width=2).set_opacity(0.5)
        self.add(div)
        lcx, rcx = -3.7, 3.7
        t1 = T("GAD65 knockout", 32, RED, weight=BOLD).move_to([lcx, 3.3, 0])
        o1, f1, th1, z1, zl1 = gauge_parts(lcx - 0.7, 0.2)
        lamp1, wl1, st1 = lamp_parts(lcx + 2.0, False)
        # right panel: present from the start, dim, until the adult is the subject
        t2 = T("adult, on fluoxetine", 32, TEAL, weight=BOLD).move_to([rcx, 3.3, 0])
        o2, f2, th2, z2, zl2 = gauge_parts(rcx - 0.7, 0.55)
        lamp2, wl2, st2 = lamp_parts(rcx + 2.0, True)
        ghost = VGroup(t2.copy(), o2.copy(), lamp_parts(rcx + 2.0, False)[0], lamp_parts(rcx + 2.0, False)[1]).set_opacity(0.28)
        self.play(FadeIn(VGroup(t1, o1, f1, th1, z1, zl1, lamp1, wl1), run_time=0.5), FadeIn(st1, run_time=0.5),
                  FadeIn(ghost, run_time=0.5))
        self.at("diazepam")
        dz1 = bchip("diazepam", TEAL, 26).move_to([lcx - 0.7, 2.35, 0])
        a1 = arr([lcx - 0.7, 2.0, 0], [lcx - 0.7, 1.55, 0], TEAL, 5, 0.18)
        self.play(FadeIn(dz1, run_time=0.3), GrowArrow(a1, run_time=0.3))
        self.at("opened the window")
        _, f1b, *_ = gauge_parts(lcx - 0.7, 0.62)
        lamp1b, _, st1b = lamp_parts(lcx + 2.0, True)
        self.play(Transform(f1, f1b), Transform(lamp1, lamp1b), ReplacementTransform(st1, st1b), run_time=0.8)
        self.at("In the adults")
        self.play(FadeOut(ghost, run_time=0.3),
                  FadeIn(VGroup(t2, o2, f2, th2, z2, zl2, lamp2, wl2), run_time=0.5), FadeIn(st2, run_time=0.5))
        self.at("put the")
        dz2 = bchip("diazepam", TEAL, 26).move_to([rcx - 0.7, 2.35, 0])
        a2 = arr([rcx - 0.7, 2.0, 0], [rcx - 0.7, 1.55, 0], TEAL, 5, 0.18)
        self.play(FadeIn(dz2, run_time=0.3), GrowArrow(a2, run_time=0.3))
        self.at("break back")
        _, f2b, *_ = gauge_parts(rcx - 0.7, 0.9)
        lamp2b, _, st2b = lamp_parts(rcx + 2.0, False)
        self.play(Transform(f2, f2b), Transform(lamp2, lamp2b), ReplacementTransform(st2, st2b), run_time=0.8)
        settle(self, 2.0)
        self.finish()


# ---------------------------------------------------------------------------------------------
SLAB_W, SLAB_H = 6.8, 4.6
SLAB_FINAL = pt(2.7, 0.7)
HOST_OFF = [pt(-2.4, 1.3), pt(-0.6, -1.3), pt(1.6, 1.5), pt(2.5, -1.3)]
DONOR_OFF = [pt(-1.0, 0.8), pt(-2.3, -0.2), pt(0.2, -0.3), pt(1.2, 0.1), pt(2.4, 0.7)]
MATURE_OFF = [pt(-2.6, -0.5), pt(-1.2, 0.5), pt(0.3, 1.2), pt(1.0, -0.7), pt(2.5, 0.3)]


def slab_parts(center=SLAB_FINAL):
    c = np.array(center, float)
    slab = RoundedRectangle(corner_radius=0.25, width=SLAB_W, height=SLAB_H, stroke_color=GREY, stroke_width=3,
                            fill_color=GREY, fill_opacity=0.08).move_to(c)
    lab = T("young mouse cortex", 28, GREY).move_to(c + np.array([0, SLAB_H / 2 + 0.38, 0]))
    host = VGroup(*[Circle(radius=0.3, stroke_color=GREY, stroke_width=3, fill_color=GREY, fill_opacity=0.35).move_to(c + o)
                    for o in HOST_OFF])
    return slab, lab, host


class S16Tr(SpokenScene):
    def construct(self):
        start = pt(0.1, 0.7)
        slab, lab, host = slab_parts(start)
        sgroup = VGroup(slab, lab, host)
        st = Strip(-3.3)
        band1 = band(A_OPEN, A_END, st.by)
        blab = T("window", 26, TEXT).move_to(band1)
        self.play(FadeIn(sgroup, run_time=0.6))
        self.at("whether the window")
        self.play(FadeIn(st.group, run_time=0.4), FadeIn(band1, run_time=0.4), FadeIn(blab, run_time=0.4))
        self.at("follows the cells")
        q_txt = T("follows the cells?", 30, YELLOW).move_to([0.75, st.by, 0], aligned_edge=LEFT)
        self.play(FadeIn(q_txt, shift=RIGHT * 0.1, run_time=0.6))
        self.at("Transplant", lead=0.5)
        self.play(FadeOut(q_txt, run_time=0.15))
        q_txt.set_opacity(0)
        self.remove(q_txt)
        self.at("Transplant")
        donor_box = RoundedRectangle(corner_radius=0.2, width=2.8, height=2.8, stroke_color=GOLD, stroke_width=4,
                                     fill_color=GOLD, fill_opacity=0.08).move_to([-4.9, 0.7, 0])
        hex0 = [pt(-5.6, 1.5), pt(-4.6, 1.6), pt(-5.2, 0.7), pt(-4.3, 0.7), pt(-5.0, -0.1)]
        donors = VGroup(*[hexcell(p, 0.3) for p in hex0])
        shift = SLAB_FINAL - start
        self.play(sgroup.animate.shift(shift), FadeIn(donor_box, run_time=0.45), FadeIn(donors, run_time=0.45), run_time=0.45)
        self.at("embryonic")
        emb = T("embryonic", 30, GOLD).move_to([-4.9, 2.55, 0])
        self.play(FadeIn(emb, shift=DOWN * 0.1, run_time=0.4))
        self.at("inhibitory")
        self.play(*[Indicate(d, color=GOLD, scale_factor=1.3) for d in donors], run_time=0.8)
        self.at("neuron precursors")
        plab = T("inhibitory neuron\nprecursors", 26, GOLD, line_spacing=0.8).move_to([-4.9, -1.55, 0])
        self.play(FadeIn(plab, shift=UP * 0.1, run_time=0.5))
        self.at("into a young")
        moves = [d.animate.move_to(SLAB_FINAL + o) for d, o in zip(donors, DONOR_OFF)]
        self.play(LaggedStart(*moves, lag_ratio=0.12, run_time=1.4),
                  FadeOut(VGroup(donor_box, plab, emb), run_time=0.8))
        settle(self, 1.0)
        self.finish()


class S17Mature(SpokenScene):
    def construct(self):
        slab, lab, host = slab_parts()
        donors = VGroup(*[hexcell(SLAB_FINAL + o, 0.3) for o in DONOR_OFF])
        st = Strip(-3.3)
        band1 = band(A_OPEN, A_END, st.by)
        blab = T("window", 26, TEXT).move_to(band1)
        self.add(slab, lab, host, donors, st.group, band1, blab)
        self.at("mature")
        mats = VGroup(*[mature_cell(SLAB_FINAL + o, 0.3) for o in MATURE_OFF])
        self.play(*[FadeTransform(d, m) for d, m in zip(donors, mats)], run_time=0.8)
        self.at("interneurons")
        il = T("mature interneurons", 26, GOLD).move_to([4.5, -1.95, 0])
        self.play(FadeIn(il, run_time=0.4))
        self.at("parvalbumin cells")
        pl = T("parvalbumin cells", 26, YELLOW).move_to([0.4, -1.95, 0])
        c0, c3 = SLAB_FINAL + MATURE_OFF[0], SLAB_FINAL + MATURE_OFF[3]
        rings = VGroup(Circle(radius=0.5, stroke_color=YELLOW, stroke_width=3).move_to(c0),
                       Circle(radius=0.5, stroke_color=YELLOW, stroke_width=3).move_to(c3))
        ptrs = VGroup(Line([c0[0], -1.75, 0], [c0[0], c0[1] - 0.5, 0], color=YELLOW, stroke_width=2.5),
                      Line([1.6, -1.75, 0], [c3[0] - 0.1, c3[1] - 0.5, 0], color=YELLOW, stroke_width=2.5))
        self.play(FadeIn(pl, run_time=0.5), Create(rings, run_time=0.5), Create(ptrs, run_time=0.5))
        self.at("host's own window")
        newlab = T("host's window", 24, TEXT).move_to(band1)
        self.play(ReplacementTransform(blab, newlab, run_time=0.4))
        self.at("closes")
        cap = Line([X(A_END), st.by - 0.5, 0], [X(A_END), st.by + 0.5, 0], color=RED, stroke_width=8)
        self.play(Create(cap, run_time=0.3), band1.animate.set_fill(opacity=0.2), run_time=0.8)
        settle(self, 1.4)
        self.finish()


# ---------------------------------------------------------------------------------------------
CAND0, CAND1 = A_OPEN + 26.0, A_END + 26.0     # the second-window slot, aligned with the cells'-age row in s20


def card2_parts():
    p = {}
    p["head"] = pred_header()
    # a reminder of the experiment: host cortex with donor cells
    c = pt(0, 1.5)
    mini = VGroup(RoundedRectangle(corner_radius=0.2, width=5.0, height=1.9, stroke_color=GREY, stroke_width=3,
                                   fill_color=GREY, fill_opacity=0.08).move_to(c))
    for o in [pt(-2.0, 0.45), pt(-0.6, -0.5), pt(0.9, 0.55), pt(2.0, -0.4)]:
        mini.add(Circle(radius=0.17, stroke_color=GREY, stroke_width=2.5, fill_color=GREY, fill_opacity=0.35).move_to(c + o))
    for o in [pt(-1.3, -0.3), pt(-0.2, 0.4), pt(0.4, -0.55), pt(1.5, 0.1), pt(2.1, 0.55)]:
        mini.add(mature_cell(c + o, 0.15))
    p["mini"] = mini
    st = Strip(-1.0)
    host = band(A_OPEN, A_END, st.by, GREEN, 0.2, 0.9)
    hcap = Line([X(A_END), st.by - 0.55, 0], [X(A_END), st.by + 0.55, 0], color=RED, stroke_width=8)
    hlab = T("host's window", 24, TEXT).move_to(host)
    p["strip"] = VGroup(st.group, host, hcap, hlab)
    cand = closed_band(CAND0, CAND1, st.by, 0.9)
    qm = T("?", 56, YELLOW, weight=BOLD).move_to(cand)
    p["cand"] = VGroup(cand, qm)
    p["hc"] = bchip("the host's age", GREEN, 38).move_to([-3.0, -2.75, 0])
    p["cc"] = bchip("the cells' age", GOLD, 38).move_to([3.0, -2.75, 0])
    p["ld"] = VGroup(Line([-2.7, -2.3, 0], [-1.4, st.by - 0.47, 0], color=GREEN, stroke_width=2.5).set_opacity(0.8),
                     Line([2.95, -2.3, 0], [3.45, st.by - 0.47, 0], color=GOLD, stroke_width=2.5).set_opacity(0.8))
    p["st"] = st
    return p


class S18Pred(SpokenScene):
    def construct(self):
        p = card2_parts()
        self.play(FadeIn(p["head"], run_time=0.5), FadeIn(p["mini"], run_time=0.5), FadeIn(p["strip"], run_time=0.6))
        self.at("second window")
        self.play(FadeIn(p["cand"], run_time=0.5))
        self.at("host's age")
        self.play(FadeIn(p["hc"], shift=UP * 0.15, run_time=0.5), FadeIn(p["ld"][0], run_time=0.5))
        self.at("cell's age")
        self.play(FadeIn(p["cc"], shift=UP * 0.15, run_time=0.5), FadeIn(p["ld"][1], run_time=0.5))
        self.finish()


class S19Pause(NarratedScene):
    def construct(self):
        p = card2_parts()
        self.add(p["head"], p["mini"], p["strip"], p["cand"], p["hc"], p["cc"], p["ld"])
        self.finish()


class S20Reveal(SpokenScene):
    def construct(self):
        p = card2_parts()
        st = p["st"]
        self.add(p["head"], p["mini"], p["strip"], p["cand"], p["hc"], p["cc"], p["ld"])
        self.at("the cells age", lead=0.0)
        cr = credit("Southwell and colleagues, 2010", pt(6.6, 3.55))
        self.play(p["hc"].animate.set_opacity(0.25), Indicate(p["cc"], color=GOLD, scale_factor=1.12), FadeIn(cr), run_time=0.9)
        self.at("When they reach")
        UPS = 2.0
        ay2 = -2.4
        gy = -1.5
        axis2 = Line([X(26), ay2, 0], [X(62), ay2, 0], color=GOLD, stroke_width=3)
        lab2 = T("cells' age", 26, GOLD).move_to([X(56), ay2 - 0.5, 0])
        hx = hexcell([X(26), ay2, 0], 0.26)
        tlab = T("transplant", 24, GOLD).move_to([X(26) + 0.1, ay2 - 0.5, 0])
        self.play(FadeOut(p["hc"], run_time=0.4), FadeOut(p["cc"], run_time=0.4), FadeOut(p["head"], run_time=0.4),
                  FadeOut(p["mini"], run_time=0.4), FadeOut(p["ld"], run_time=0.4),
                  p["strip"].animate.shift(UP * UPS), p["cand"].animate.shift(UP * UPS),
                  FadeIn(axis2, run_time=0.5), FadeIn(lab2, run_time=0.5), FadeIn(hx, run_time=0.5), FadeIn(tlab, run_time=0.5),
                  run_time=0.7)
        self.at("native interneurons")
        ghost = band(CAND0, CAND1, gy, GREEN, 0.0, 0.9, 3)
        ghost.set_fill(GREEN, opacity=0.15)
        self.play(FadeIn(ghost, run_time=0.5), hx.animate.move_to([X(CAND0) + 0.35, ay2, 0]), run_time=1.0)
        self.at("in the normal window")
        glab = T("native interneurons,\nnormal window", 24, TEXT, line_spacing=0.8).move_to([X(CAND0) - 2.0, gy, 0])
        self.play(FadeIn(glab, run_time=0.5), hx.animate.move_to([X(CAND0) + 1.0, ay2, 0]), run_time=0.6)
        self.at("the host shifted")
        gold = band(CAND0, CAND1, st.by + UPS, GOLD, 0.55, 0.9)
        glab2 = T("second window", 26, TEXT).move_to(gold)
        gd = VGroup(DashedLine([X(CAND0), gy + 0.47, 0], [X(CAND0), st.by + UPS - 0.5, 0], color=GOLD, stroke_width=3),
                    DashedLine([X(CAND1), gy + 0.47, 0], [X(CAND1), st.by + UPS - 0.5, 0], color=GOLD, stroke_width=3))
        self.play(FadeOut(p["cand"], run_time=0.3), Create(gd, run_time=0.4), GrowFromEdge(gold, LEFT, run_time=0.8))
        self.play(FadeIn(glab2, run_time=0.4))
        settle(self, 1.8)
        self.finish()


# ---------------------------------------------------------------------------------------------
def head_circle(c, r):
    return Circle(radius=r, stroke_color=GREY, stroke_width=4, fill_color=GREY, fill_opacity=0.12).move_to(c)


class S23Amb(SpokenScene):
    def construct(self):
        title = T("Why does this matter?", 40, GREY).move_to([0, 3.35, 0])
        HC = pt(0, -0.2)
        head = head_circle(HC, 2.1)
        ge = eye_open(ORANGE).scale(1.6).move_to(HC + pt(0.9, 0.3))
        pe = eye_open(BLUE).scale(1.6).move_to(HC + pt(-0.9, 0.3))
        kid = T("child", 30, GREY).move_to([0, 2.35, 0])
        child = VGroup(head, ge, pe, kid)
        self.play(FadeIn(title), FadeIn(child), run_time=0.5)
        cx, base = 3.1, -1.45
        box = RoundedRectangle(corner_radius=0.25, width=6.0, height=5.3, stroke_color=GREY, stroke_width=3,
                               fill_color=GREY, fill_opacity=0.08).move_to([cx, -0.05, 0])
        clab = T("visual cortex", 32, TEXT).move_to([cx, 2.25, 0])
        bo = Rectangle(width=1.3, height=3.0, stroke_width=0, fill_color=ORANGE, fill_opacity=0.9).move_to([cx - 1.4, base + 1.5, 0])
        bb = Rectangle(width=1.3, height=0.55, stroke_width=0, fill_color=BLUE, fill_opacity=0.9).move_to([cx + 1.4, base + 0.275, 0])
        bl = VGroup(T("good eye\ninput", 26, ORANGE, line_spacing=0.8).move_to([cx - 1.4, base - 0.55, 0]),
                    T("weak eye\ninput", 26, BLUE, line_spacing=0.8).move_to([cx + 1.4, base - 0.55, 0]))
        self.at("In amblyopia")
        t2 = T("amblyopia", 46, TEXT, font=TITLE_FONT).move_to([0, 3.35, 0])
        self.play(ReplacementTransform(title, t2), child.animate.shift(LEFT * 3.9),
                  FadeIn(VGroup(box, clab, bo, bb, bl)), run_time=0.6)
        self.at("one eye sees poorly")
        blur = VGroup(*[eye_open(BLUE).scale(1.6).shift(RIGHT * dx).set_opacity(0.3) for dx in (-0.2, 0.0, 0.2)]).move_to(pe)
        plab = T("sees poorly", 28, BLUE).move_to([-3.9, -1.1, 0])
        self.play(ReplacementTransform(pe, blur), FadeIn(plab), run_time=0.6)
        self.at("its input to the cortex")
        a_o = arr(ge.get_right() + RIGHT * 0.1, [0.05, 0.1, 0], ORANGE, 12, 0.4)
        path = VMobject(color=BLUE, stroke_width=12, fill_opacity=0).set_points_as_corners(
            [pt(-4.8, -0.4), pt(-4.8, -2.5), pt(-0.3, -2.5), pt(-0.3, -1.1)])
        a_b = VGroup(path, Triangle(color=BLUE, fill_color=BLUE, fill_opacity=1, stroke_width=0).scale(0.22)
                     .rotate(-PI / 2).move_to([-0.05, -1.1, 0]))
        self.play(GrowArrow(a_o), FadeIn(a_b), run_time=0.7)
        self.at("was degraded")
        self.play(a_b[0].animate.set_stroke(opacity=0.3), a_b[1].animate.set_fill(opacity=0.3),
                  Indicate(bb, color=BLUE, scale_factor=1.1), run_time=0.6)
        self.at("in childhood")
        ch = bchip("in childhood", GOLD, 34).move_to([-3.9, -3.3, 0])
        self.play(FadeIn(ch, shift=UP * 0.1, run_time=0.5))
        settle(self, 1.0)
        self.finish()


def face(cx, cy, r, es, ed):
    head = head_circle(pt(cx, cy), r)
    ge = eye_open(ORANGE).scale(es).move_to([cx - ed, cy + 0.1, 0])
    pe = eye_open(BLUE).scale(es).move_to([cx + ed, cy + 0.1, 0])
    pw, ph = 0.9 * es + 0.55, 0.5 * es + 0.5
    patch = VGroup(RoundedRectangle(corner_radius=0.2, width=pw, height=ph, stroke_color=GREY, stroke_width=4,
                                    fill_color="#B9BEC9", fill_opacity=0.4).move_to(ge),
                   Line(ge.get_center() + [-pw / 2, 0.15, 0], [cx - r * 0.97, cy + 0.5, 0], color=GREY, stroke_width=3))
    return head, ge, pe, patch


class S24Patch(SpokenScene):
    def construct(self):
        # child figure, built centred and slid left when the adult arrives
        head, ge, pe, patch = face(0, -0.3, 1.6, 1.4, 0.85)
        kid = T("child", 34, TEXT).move_to([0, -3.0, 0])
        childg = VGroup(head, ge, pe, kid)
        self.play(FadeIn(childg, run_time=0.5))
        self.at("the good eye")
        self.play(FadeIn(patch, shift=RIGHT * 0.3, run_time=0.5))
        childg.add(patch)
        self.at("works best")
        big = arr([0, 1.45, 0], [0, 3.5, 0], GREEN, 16, 0.55)
        bl = T("benefit", 28, GREEN).move_to([1.2, 2.5, 0])
        wl = T("works best", 28, GREEN).move_to([0, -3.55, 0])
        self.play(GrowArrow(big), FadeIn(bl), FadeIn(wl), run_time=0.8)
        childg.add(big, bl, wl)
        self.at("and much")
        ah, age_, ape, apatch = face(3.3, -0.4, 2.1, 1.8, 1.1)
        al = T("adult", 34, TEXT).move_to([3.3, -3.0, 0])
        self.play(childg.animate.shift(LEFT * 3.5), FadeIn(VGroup(ah, age_, ape, apatch, al)), run_time=0.8)
        self.at("much less")
        small = arr([3.3, 1.9, 0], [3.3, 2.85, 0], GREEN, 16, 0.4)
        sbl = T("benefit", 28, GREEN).move_to([4.5, 2.4, 0])
        sl = T("much less reliably", 28, GREEN).move_to([3.3, -3.55, 0])
        self.play(GrowArrow(small), FadeIn(sbl), FadeIn(sl), run_time=0.6)
        settle(self, 1.8)
        self.finish()


class S25Caution(SpokenScene):
    def construct(self):
        r = rat(1.5, pt(-1.6, -1.55))
        self.play(FadeIn(r, run_time=0.7))
        self.at("show mechanism")
        mech = bchip("mechanism", GREEN, 38).move_to([-4.2, 3.2, 0])
        self.play(FadeIn(mech, shift=DOWN * 0.2, run_time=0.5))
        self.at("not treatment")
        tr = bchip("treatment", GREY, 38).move_to([0.3, 3.2, 0])
        nty = T("not yet", 38, RED).move_to([4.5, 3.2, 0])
        strike = Line(tr.get_left() + [-0.1, 0, 0], tr.get_right() + [0.1, 0, 0], color=RED, stroke_width=4)
        self.play(FadeIn(tr, shift=LEFT * 0.2, run_time=0.4))
        self.play(Create(strike, run_time=0.4), FadeIn(nty, run_time=0.4))
        self.at("Reopening plasticity")
        g = bchip("plasticity reopens", GREEN, 32).move_to([-3.6, 1.35, 0])
        self.play(FadeIn(g, shift=RIGHT * 0.2, run_time=0.6))
        self.at("also reopen")
        v = bchip("vulnerability", RED, 32).move_to([4.2, 1.35, 0])
        ar_ = arr([g.get_right()[0] + 0.15, 1.35, 0], [v.get_left()[0] - 0.15, 1.35, 0], GREY, 6, 0.25)
        arl = T("can also reopen", 26, TEXT).move_to([(g.get_right()[0] + v.get_left()[0]) / 2, 1.9, 0])
        self.play(GrowArrow(ar_, run_time=0.6), FadeIn(arl, run_time=0.5))
        self.at("vulnerability")
        self.play(FadeIn(v, shift=LEFT * 0.2, run_time=0.5))
        settle(self, 1.2)
        self.finish()


class S26Take(SpokenScene):
    def construct(self):
        BY, BH, BW, X0 = 0.0, 2.2, 10.0, -5.0
        w = ValueTracker(0.0)
        hdr = T("In rodent visual cortex", 32, GREY).move_to([0, 3.4, 0])
        track = RoundedRectangle(corner_radius=0.15, width=BW, height=BH, stroke_color=GREY, stroke_width=3).move_to([0, BY, 0])
        fill = always_redraw(lambda: Rectangle(width=max(w.get_value(), 0.01), height=BH, stroke_width=0, fill_color=GREEN,
                                               fill_opacity=0.55).move_to([X0 + max(w.get_value(), 0.01) / 2, BY, 0]))
        wlab = T("window", 34, GREY).move_to([0, BY, 0])
        wlab.add_updater(lambda m: m.set_color(TEXT if w.get_value() > BW * 0.5 else GREY))
        self.at("rodent visual")
        self.play(FadeIn(hdr, run_time=0.5))
        self.at("window is set")
        self.add(fill)
        self.play(FadeIn(track, run_time=0.4), FadeIn(wlab, run_time=0.4))
        self.at("state of a circuit")
        cir = T("the state of a circuit", 38, YELLOW).move_to([-2.4, 2.15, 0])
        self.play(FadeIn(cir, shift=DOWN * 0.1, run_time=0.6))
        self.at("not simply")
        ns = T("not simply", 32, GREY).move_to([2.0, 2.15, 0])
        agec = bchip("age", GREY, 34).move_to([3.9, 2.15, 0])
        self.play(FadeIn(ns, run_time=0.3), FadeIn(agec, run_time=0.3))
        strike = Line(agec.get_left() + [0.05, 0, 0], agec.get_right() + [-0.05, 0, 0], color=RED, stroke_width=3.5).set_opacity(0.85)
        self.play(Create(strike, run_time=0.4))
        self.at("Inhibition opens")
        inh = bchip("inhibition", YELLOW, 28).move_to([-4.9, -2.9, 0])
        inha = arr([-4.9, -2.45, 0], [-4.9, BY - BH / 2 - 0.05, 0], YELLOW, 7, 0.3)
        self.play(FadeIn(inh), GrowArrow(inha), w.animate.set_value(BW), run_time=0.4, rate_func=smooth)
        # A readable open state must precede both closing causes.
        self.wait(1.5)
        self.at("added")
        brk = bchip("added brakes", RED, 28).move_to([4.6, -2.9, 0])
        bar1 = inhib([4.6, -2.5, 0], [4.6, BY - BH / 2 - 0.02, 0], RED, 7)
        self.play(FadeIn(brk, run_time=0.3), Create(bar1, run_time=0.4))
        self.play(w.animate.set_value(6.0), run_time=0.5)
        self.at("more mature")
        mat = bchip("more mature inhibition", YELLOW, 28).move_to([0.0, -2.9, 0])
        bar2 = inhib([0.0, -2.5, 0], [0.0, BY - BH / 2 - 0.02, 0], RED, 7)
        self.play(FadeIn(mat, run_time=0.3), Create(bar2, run_time=0.4), w.animate.set_value(0.35), run_time=0.7)
        self.at("close it")
        clo = T("closed", 34, RED).move_to([3.6, BY, 0])
        self.play(FadeIn(clo, run_time=0.4))
        settle(self, 2.0)
        self.finish()


class S27End(EndCard):
    LINE = "In rodent cortex, circuit state sets the window, not simply age."
