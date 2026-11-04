"""Chapter 2: A Glial Cell That Stops Respiring  (Biochemistrypedia chaptered film)

COLOR MAP (one color per concept, shared by every chapter of this lesson)
  BLUE   = the neuron / axon
  TEAL   = myelinating glia (oligodendrocyte, Schwann cell: the glial cell that wraps axons)
  PURPLE = astrocyte (not used in this chapter)
  ORANGE = lactate and pyruvate (the portable fuel)
  YELLOW = ATP, mitochondria, "pause and predict" and question marks
  GREY   = myelin, membranes, transporter gates, outlines, neutral labels
  GREEN  = evidence for / axon intact / survived
  RED    = blocked, lost, failure
  PINK   = anaesthesia (this chapter only)
"""
import numpy as np
from bp_style import *  # noqa: F401,F403

PURPLE = "#B58CD9"
ORANGE = "#F29E4C"
PINK = "#E58FB0"


# ----------------------------------------------------------------------------------------------
# small builders
def arr(a, b, color=GREY, w=5, tip=0.22):
    return Arrow(a, b, buff=0.06, color=color, stroke_width=w, tip_length=tip,
                 max_tip_length_to_length_ratio=0.45, max_stroke_width_to_length_ratio=12)


def rrect(w, h, color, fo=0.15, sw=3, r=0.2):
    return RoundedRectangle(corner_radius=min(r, w / 2, h / 2), width=w, height=h, stroke_color=color,
                            stroke_width=sw, fill_color=color, fill_opacity=fo)


def dotc(color=ORANGE, r=0.2):
    return Circle(radius=r, stroke_width=0, fill_color=color, fill_opacity=1)


def cross(c, color=RED, s=0.3, w=7):
    c = np.array(list(c) + [0.0] * (3 - len(c)), dtype=float)
    return VGroup(Line(c + np.array([-s, s, 0]), c + np.array([s, -s, 0]), color=color, stroke_width=w),
                  Line(c + np.array([-s, -s, 0]), c + np.array([s, s, 0]), color=color, stroke_width=w))


def tick(c, color=GREEN, s=0.28, w=9):
    c = np.array(list(c) + [0.0] * (3 - len(c)), dtype=float)
    return VMobject(stroke_color=color, stroke_width=w, fill_opacity=0).set_points_as_corners(
        [c + np.array([-s, 0.0, 0]), c + np.array([-s * 0.3, -s * 0.8, 0]), c + np.array([s, s * 0.9, 0])])


def mito_small(x, y, on=True, w=1.0, h=0.55):
    c = YELLOW if on else GREY
    so = 1.0 if on else 0.45
    o = Ellipse(width=w, height=h, stroke_color=c, stroke_width=3, stroke_opacity=so, fill_color=c,
                fill_opacity=0.18 if on else 0.05)
    pts = [[-w * .30, 0, 0], [-w * .18, h * .22, 0], [-w * .06, -h * .22, 0], [w * .06, h * .22, 0],
           [w * .18, -h * .22, 0], [w * .30, 0, 0]]
    ins = VMobject(stroke_color=c, stroke_width=3, stroke_opacity=so, fill_opacity=0).set_points_as_corners(pts)
    return VGroup(o, ins).move_to([x, y, 0])


def mito_big(cx, cy, w=5.0, h=2.5, on=True, label="mitochondrion", cyc="citric acid cycle"):
    """body, ring (the citric acid cycle: a loop with three arrowheads), labels."""
    c = YELLOW if on else GREY
    so = 1.0 if on else 0.45
    body = Ellipse(width=w, height=h, stroke_color=c, stroke_width=4, stroke_opacity=so, fill_color=c,
                   fill_opacity=0.12 if on else 0.04).move_to([cx, cy, 0])
    circ = Circle(radius=0.5, stroke_color=c, stroke_width=4, stroke_opacity=so, fill_opacity=0)
    tris = []
    for k in range(3):
        a = k * TAU / 3
        t = Triangle(fill_color=c, fill_opacity=so, stroke_width=0).scale(0.14).rotate(a)
        t.move_to([0.5 * np.cos(a), 0.5 * np.sin(a), 0])
        tris.append(t)
    ring = VGroup(circ, *tris).move_to([cx, cy - 0.02, 0])
    lab = T(label, 26, c).move_to([cx, cy + 0.9, 0])
    cyl = T(cyc, 26, c).move_to([cx, cy - 0.85, 0])
    if not on:
        lab.set_opacity(0.6)
        cyl.set_opacity(0.6)
    return VGroup(body, ring, lab, cyl)


def spin(mob, scene, turns=1.0, run_time=1.0):
    scene.play(Rotate(mob, angle=-TAU * turns, about_point=mob.get_center(), rate_func=linear), run_time=run_time)


def pulse(scene, mob, color=YELLOW, k=1.25, rt=0.8):
    scene.play(Indicate(mob, color=color, scale_factor=k), run_time=rt)


# geometry shared by the two-cell scenes: glial cell left, partner right, narrow gap with one transporter
CY, CH = -0.1, 6.9
LCX, LW = -3.4, 6.6   # left cell spans x -6.7 .. -0.1
RCX, RW = 3.8, 5.8    # right cell spans x  0.9 ..  6.7
GATE_X = 0.4


def cell_left(label="glial cell", color=TEAL, cy=CY, ch=CH):
    box = rrect(LW, ch, color, 0.08, 4, 0.5).move_to([LCX, cy, 0])
    lab = T(label, 26, color)
    lab.move_to([LCX - LW / 2 + 0.35 + lab.width / 2, cy + ch / 2 - 0.4, 0])
    return VGroup(box, lab)


def cell_right(label, color, cy=CY, ch=CH, fo=0.08):
    box = rrect(RW, ch, color, fo, 4, 0.5).move_to([RCX, cy, 0])
    lab = T(label, 26, color)
    lab.move_to([RCX - RW / 2 + 0.35 + lab.width / 2, cy + ch / 2 - 0.4, 0])
    return VGroup(box, lab)


def gate_one(x, y, label=True):
    """a single transporter square sitting in the gap, labelled once"""
    g = VGroup(rrect(0.62, 1.0, GREY, 0.55, 3, 0.1).move_to([x, y, 0]))
    if label:
        g.add(T("MCT", 26, GREY).move_to([x, y + 0.85, 0]))
    return g


def myelin_axon(x0, x1, y, n=3, tube_h=0.9, band_h=0.55, tube_op=0.85, band_op=0.5):
    """an axon with myelin wrapped AROUND it: a band above and a band below each segment, nothing over the axon."""
    tube = Rectangle(width=x1 - x0, height=tube_h, stroke_width=0, fill_color=BLUE, fill_opacity=tube_op).move_to([(x0 + x1) / 2, y, 0])
    seg = (x1 - x0) / n
    bands = VGroup()
    off = tube_h / 2 + band_h / 2 + 0.02
    for i in range(n):
        cx = x0 + seg * (i + 0.5)
        for s in (1, -1):
            bands.add(rrect(seg - 0.14, band_h, GREY, band_op, 3, 0.25).move_to([cx, y + s * off, 0]))
    return tube, bands


# glycolysis picture inside the left cell (scenes 4, 5, 12)
GLU_P = np.array([-5.3, 2.1, 0])
P1 = np.array([-1.45, 2.5, 0])
P2 = np.array([-1.45, 1.7, 0])
MCY = -1.5   # mitochondrion centre height in the tall cells


def glyc_arrow(dx=0.0):
    a = arr([-4.4 + dx, 2.1, 0], [-3.5 + dx, 2.1, 0], GREY, 5, 0.2)
    l = T("glycolysis", 26, GREY).move_to([-3.55 + dx, 1.62, 0])
    return VGroup(a, l)


# ----------------------------------------------------------------------------------------------
# myelin cross-sections (scenes 2 and 3)
def ring(cx, cy, r_ax=0.9, r_out=2.2, ax_color=BLUE, n=8, state="normal"):
    my = Annulus(inner_radius=r_ax, outer_radius=r_out, stroke_width=0, fill_color=GREY, fill_opacity=0.42)
    lines = [Circle(radius=r, stroke_color=GREY, stroke_width=2.5, stroke_opacity=0.9)
             for r in np.linspace(r_ax + 0.18, r_out - 0.03, n)]
    if state == "broken":
        ax = DashedVMobject(Circle(radius=r_ax, stroke_color=RED, stroke_width=6, fill_opacity=0), num_dashes=9)
        core = Circle(radius=r_ax * 0.8, stroke_width=0, fill_color=RED, fill_opacity=0.18)
        ax = VGroup(core, ax)
    else:
        ax = Circle(radius=r_ax, stroke_color=ax_color, stroke_width=4, fill_color=ax_color, fill_opacity=0.35)
    return VGroup(my, *lines, ax).move_to([cx, cy, 0])


# ----------------------------------------------------------------------------------------------
# MR spectrum (scenes 15, 16, 18): computed from Lorentzian lines at the standard shifts
def lor(p, p0, w):
    return 1.0 / (1.0 + ((p - p0) / w) ** 2)


def other_signal(p):
    return (1.0 * lor(p, 2.02, 0.035) + 0.72 * lor(p, 3.03, 0.04) + 0.55 * lor(p, 3.22, 0.035)
            + 0.18 * lor(p, 2.35, 0.09) + 0.30 * lor(p, 3.56, 0.04))


def lac_signal(p):
    return 0.85 * (lor(p, 1.31, 0.02) + lor(p, 1.35, 0.02))


class Spectrum:
    """x0..x1 is the plot's width, yb its baseline, H the height of a signal of 1.0; ppm runs right to left."""

    def __init__(self, x0, x1, yb, H, lo=0.7, hi=4.0):
        self.x0, self.x1, self.yb, self.H, self.lo, self.hi = x0, x1, yb, H, lo, hi

    def x_of(self, p):
        return self.x0 + (self.hi - p) / (self.hi - self.lo) * (self.x1 - self.x0)

    def grey(self, n=900):
        ps = np.linspace(self.hi, self.lo, n)
        pts = [[self.x_of(p), self.yb + self.H * other_signal(p), 0] for p in ps]
        return VMobject(stroke_color=GREY, stroke_width=4, fill_opacity=0).set_points_as_corners(pts)

    def lac(self, amp, n=300):
        """the lactate doublet drawn ON TOP of the baseline signal, so the orange joins the grey line"""
        ps = np.linspace(1.75, 0.95, n)
        pts = [[self.x_of(p), self.yb + self.H * (other_signal(p) + amp * lac_signal(p)), 0] for p in ps]
        m = VMobject(stroke_color=ORANGE, stroke_width=5, fill_opacity=0).set_points_as_corners(pts)
        if amp < 0.03:
            m.set_stroke(opacity=0)
        return m

    def ticks(self, vals=(4, 3, 2, 1), size=26):
        g = VGroup()
        for v in vals:
            g.add(M(str(v), size, GREY).move_to([self.x_of(v), self.yb - 0.4, 0]))
        g.add(M("ppm", size, GREY).move_to([self.x_of(0.82) + 0.2, self.yb - 0.4, 0]))
        return g


def clock(c, r=0.95):
    c = np.array(list(c) + [0.0] * (3 - len(c)), dtype=float)
    face = Circle(radius=r, stroke_color=TEXT, stroke_width=4, fill_color=TEXT, fill_opacity=0.06).move_to(c)
    hand = Line(c, c + np.array([0, r * 0.8, 0]), color=YELLOW, stroke_width=6)
    top = Line(c + np.array([0, r * 0.82, 0]), c + np.array([0, r, 0]), color=TEXT, stroke_width=4)
    return face, hand, top


# ----------------------------------------------------------------------------------------------
# the "oligodendrocyte, myelin, axon" stage (scenes 8-11), same picture in all four
def stage(y0=1.2):
    cell = Ellipse(width=4.6, height=3.0, stroke_color=TEAL, stroke_width=4, fill_color=TEAL, fill_opacity=0.12).move_to([-4.2, y0, 0])
    m = mito_small(-4.2, y0 + 0.5, on=False, w=1.9, h=1.0)
    gly = chip("glycolysis only", ORANGE, 26).move_to([-4.2, y0 - 0.65, 0])
    lab = T("oligodendrocyte", 26, TEAL).move_to([-4.2, y0 - 1.85, 0])
    iv = T("complex IV lost", 26, RED).move_to([-4.2, y0 - 2.35, 0])
    return VGroup(cell, m, gly, lab, iv)


def stage_axon(y0=1.2, ghost=False):
    tube, bands = myelin_axon(0.2, 6.6, y0, 3)
    stalk = CubicBezier(np.array([-1.95, y0 + 0.4, 0]), np.array([-0.9, y0 + 2.0, 0]), np.array([0.3, y0 + 2.0, 0]),
                        np.array([1.3, y0 + 1.0, 0]), stroke_color=TEAL, stroke_width=8)
    myl = T("myelin", 26, GREY).move_to([4.5, y0 + 1.55, 0])
    axl = T("axon", 26, BLUE).move_to([4.5, y0 - 1.35, 0])
    return tube, bands, stalk, myl, axl


def predict_frame():
    """final frame of scene 8, rebuilt for the pause scene."""
    y0 = 1.2
    head = T("Pause and predict", 34, YELLOW).move_to([0, 3.45, 0])
    st = stage(y0)
    tube, bands, stalk, myl, axl = stage_axon(y0)
    c1, c2 = choice_cards()
    tl, q = months_arrow()
    return VGroup(head, st, tube, bands, stalk, myl, axl, c1, c2, tl, q)


def choice_cards():
    c1 = VGroup(rrect(6.3, 1.25, YELLOW, 0.08, 3, 0.2), T("respiration is needed:", 28, TEXT), T("myelin and axon fail", 28, RED))
    c1[1].move_to([-3.3, -1.95 + 0.27, 0]); c1[2].move_to([-3.3, -1.95 - 0.27, 0]); c1[0].move_to([-3.3, -1.95, 0])
    c2 = VGroup(rrect(6.3, 1.25, YELLOW, 0.08, 3, 0.2), T("respiration is not needed", 28, TEXT))
    c2[0].move_to([3.3, -1.95, 0]); c2[1].move_to([3.3, -1.95, 0])
    return c1, c2


def months_arrow():
    a = Arrow([-1.6, -3.4, 0], [5.3, -3.4, 0], buff=0, color=GREY, stroke_width=5, tip_length=0.25)
    l = T("adult brain, over the following months", 26, GREY).move_to([-3.2, -3.4, 0])
    l.set_x(-6.6 + l.width / 2)
    a2 = Arrow([-6.6 + l.width + 0.2, -3.4, 0], [5.3, -3.4, 0], buff=0, color=GREY, stroke_width=5, tip_length=0.25)
    q = T("?", 64, YELLOW, weight=BOLD).move_to([6.1, -3.35, 0])
    return VGroup(a2, l), q


# ==============================================================================================
class S00Title(TitleCard):
    LESSON = "Feeding the Axon: Glia as Metabolic Partners"
    TITLE = "A Glial Cell That Stops Respiring"


# ----------------------------------------------------------------------------------------------
class S01Q(SpokenScene):
    def construct(self):
        AY = -1.4
        tube = Rectangle(width=13.2, height=0.9, stroke_width=0, fill_color=BLUE, fill_opacity=0.85).move_to([0, AY, 0])
        _t, bands = myelin_axon(-5.4, 5.4, AY, 3)
        wraps = VGroup(*[rrect(3.45, 2.55, TEAL, 0.0, 3, 0.7).move_to([x, AY, 0]).set_stroke(opacity=0.8) for x in (-3.6, 0, 3.6)])
        cell = Ellipse(width=9.0, height=3.0, stroke_color=TEAL, stroke_width=4, fill_color=TEAL, fill_opacity=0.14).move_to([0, 1.75, 0])
        stalk = Line([0, 0.25, 0], [0, -0.55, 0], color=TEAL, stroke_width=12)
        cl = T("glial cell", 28, TEAL).move_to([-5.5, 3.05, 0])
        ml = T("myelin", 26, GREY).move_to([0, -3.15, 0])
        al = T("axon", 26, BLUE).move_to([-6.0, -0.55, 0])
        mx = (-2.8, 0, 2.8)
        on = [mito_small(x, 2.0, True, 1.7, 0.95) for x in mx]
        off = [mito_small(x, 2.0, False, 1.7, 0.95) for x in mx]
        mlab = T("mitochondria", 26, YELLOW).move_to([0, 1.05, 0])
        self.play(FadeIn(tube), FadeIn(bands), FadeIn(wraps), FadeIn(cell), FadeIn(stalk), FadeIn(cl), *[FadeIn(m) for m in on],
                  FadeIn(ml), FadeIn(al), FadeIn(mlab), run_time=0.7)
        self.at("stopped burning")
        self.play(*[Transform(a, b) for a, b in zip(on, off)], mlab.animate.set_color(GREY), run_time=1.3)
        self.at("would the axon")
        glow = tube.copy()
        self.play(tube.animate.set_fill(BLUE, 0.25), run_time=1.0)
        self.at("starve")
        q = T("?", 90, YELLOW, weight=BOLD).move_to([6.0, 0.05, 0])
        self.play(FadeIn(q, scale=0.5), Flash(tube, color=YELLOW, flash_radius=0.7, line_length=0.3), run_time=0.6)
        self.finish()


# ----------------------------------------------------------------------------------------------
RX = 3.9
RY = 0.1


def ring_pair_labels():
    l1 = T("no PLP", 34, TEXT).move_to([-RX, 2.8, 0])
    l2 = T("no CNP", 34, TEXT).move_to([RX, 2.8, 0])
    return l1, l2


def credits():
    c1 = VGroup(T("Griffiths and", 26, GREY), T("colleagues, 1998", 26, GREY)).arrange(DOWN, buff=0.05).move_to([-RX, -2.65, 0])
    c2 = VGroup(T("Lappe-Siefke and", 26, GREY), T("colleagues, 2003", 26, GREY)).arrange(DOWN, buff=0.05).move_to([RX, -2.65, 0])
    return c1, c2


class S02Plp(SpokenScene):
    def construct(self):
        head = T("A puzzle", 38, YELLOW, font=TITLE_FONT).move_to([0, 3.5, 0])
        rn = ring(0, RY, 0.7, 1.7, n=6)
        nl = T("normal", 26, GREY).move_to([0, RY - 2.1, 0])
        self.play(FadeIn(head), FadeIn(rn), FadeIn(nl), run_time=0.9)
        self.at("myelin protein PLP")
        r1 = ring(-RX, RY, 0.7, 1.7, n=6)
        l1, l2 = ring_pair_labels()
        c1, c2 = credits()
        self.play(FadeIn(r1, scale=0.7), FadeIn(l1), FadeIn(c1), run_time=0.9)
        self.at("the enzyme CNP")
        r2 = ring(RX, RY, 0.7, 1.7, n=6)
        self.play(FadeIn(r2, scale=0.7), FadeIn(l2), FadeIn(c2), run_time=0.9)
        self.at("close to normal myelin")
        ok = T("close to normal myelin", 32, GREEN).move_to([0, -3.55, 0])
        self.play(FadeIn(ok, shift=UP * 0.15), run_time=0.7)
        self.finish()


# ----------------------------------------------------------------------------------------------
class S03Aged(SpokenScene):
    def construct(self):
        head = T("A puzzle", 38, YELLOW, font=TITLE_FONT).move_to([0, 3.5, 0])
        rn = ring(0, RY, 0.7, 1.7, n=6)
        nl = T("normal", 26, GREY).move_to([0, RY - 2.1, 0])
        r1, r2 = ring(-RX, RY, 0.7, 1.7, n=6), ring(RX, RY, 0.7, 1.7, n=6)
        l1, l2 = ring_pair_labels()
        c1, c2 = credits()
        ok = T("close to normal myelin", 32, GREEN).move_to([0, -3.55, 0])
        self.add(head, rn, nl, r1, r2, l1, l2, c1, c2, ok)
        age = T("with age", 38, YELLOW).move_to([0, 3.5, 0])
        self.play(FadeOut(ok), FadeOut(c1), FadeOut(c2), Transform(head, age), run_time=0.6)
        self.at("their axons swelled")
        s1, s2 = ring(-RX, RY, 1.05, 1.7, n=6), ring(RX, RY, 1.05, 1.7, n=6)
        sw = T("axon swells", 30, YELLOW).move_to([0, -3.0, 0])
        self.play(Transform(r1, s1), Transform(r2, s2), FadeIn(sw), run_time=1.5)
        self.at("degenerated")
        d1, d2 = ring(-RX, RY, 0.9, 1.7, n=6, state="broken"), ring(RX, RY, 0.9, 1.7, n=6, state="broken")
        dg = T("axon breaks down", 30, RED).move_to([0, -3.0, 0])
        self.play(FadeOut(r1), FadeOut(r2), FadeIn(d1), FadeIn(d2), Transform(sw, dg), run_time=1.3)
        self.at("give the axon more")
        card = T("something besides insulation", 38, YELLOW).move_to([0, -3.45, 0])
        self.play(FadeOut(sw), FadeIn(card, shift=UP * 0.15), run_time=0.8)
        self.finish()


# ----------------------------------------------------------------------------------------------
# chart for scene 4: ATP per glucose, 0.17 units per ATP
BASE_Y, K = -3.0, 0.17
AXX = 1.8


def atp_axis():
    ax = Line([AXX, BASE_Y, 0], [AXX, BASE_Y + 31 * K + 0.3, 0], color=GREY, stroke_width=3)
    base = Line([AXX, BASE_Y, 0], [6.7, BASE_Y, 0], color=GREY, stroke_width=3)
    ts = VGroup(*[M(str(v), 26, GREY).move_to([AXX - 0.4, BASE_Y + v * K, 0]) for v in (0, 10, 20, 30)])
    yl = T("ATP per glucose", 26, YELLOW).rotate(PI / 2).move_to([0.5, -0.2, 0])
    return VGroup(ax, base, ts, yl)


class S04Route1(SpokenScene):
    def construct(self):
        cl = cell_left("glial cell")
        glu = chip("glucose", TEXT, 26).move_to(GLU_P)
        cand = T("a candidate: fuel", 44, TEXT, font=TITLE_FONT).move_to([3.7, 0.2, 0])
        self.play(FadeIn(cl), FadeIn(glu), FadeIn(cand), run_time=0.7)
        self.at("glycolysis turns glucose")
        ga = glyc_arrow()
        chart = atp_axis()
        self.play(GrowArrow(ga[0]), FadeIn(ga[1]), FadeOut(cand), FadeIn(chart), run_time=0.8)
        self.at("into pyruvate")
        p1 = chip("pyruvate", ORANGE, 26).move_to(GLU_P)
        p2 = chip("pyruvate", ORANGE, 26).move_to(GLU_P)
        a1, a2 = chip("ATP", YELLOW, 26).move_to([-4.6, 0.7, 0]), chip("ATP", YELLOW, 26).move_to([-3.2, 0.7, 0])
        self.play(p1.animate.move_to(P1), p2.animate.move_to(P2), glu.animate.set_opacity(0.3), FadeIn(a1), FadeIn(a2), run_time=1.0)
        b1 = Rectangle(width=1.1, height=2 * K, stroke_width=0, fill_color=YELLOW, fill_opacity=0.9).move_to([3.0, BASE_Y + K, 0])
        v1 = T("2 ATP", 26, YELLOW).move_to([3.0, BASE_Y + 2 * K + 0.4, 0])
        bl1 = T("glycolysis", 26, GREY).move_to([3.0, -3.45, 0])
        self.play(a1.animate.move_to([2.1, BASE_Y + 0.6, 0]), a2.animate.move_to([2.5, BASE_Y + 0.6, 0]), run_time=0.8)
        self.play(FadeOut(a1), FadeOut(a2), GrowFromEdge(b1, DOWN), FadeIn(v1), FadeIn(bl1), run_time=0.4)
        self.at("pyruvate can enter")
        pulse(self, VGroup(p1, p2), ORANGE, 1.2, 0.8)
        self.at("the mitochondrion")
        mt = mito_big(LCX, MCY, on=True)
        self.play(FadeIn(mt), run_time=0.4)
        self.play(p1.animate.move_to([LCX + 0.9, MCY + 1.45, 0]), p2.animate.move_to([LCX - 0.9, MCY + 1.45, 0]), run_time=0.7)
        self.play(FadeOut(p1, scale=0.3), FadeOut(p2, scale=0.3), run_time=0.2)
        self.at("far more ATP")
        b2 = Rectangle(width=1.4, height=31 * K, stroke_width=0, fill_color=YELLOW, fill_opacity=0.9).move_to([5.4, BASE_Y + 31 * K / 2, 0])
        bl2 = T("mitochondrion", 26, GREY).move_to([5.4, -3.45, 0])
        v2 = T("far more ATP", 34, YELLOW, weight=BOLD).move_to([5.0, BASE_Y + 31 * K + 0.55, 0])
        chips = [chip("ATP", YELLOW, 26).move_to([LCX + 2.7, MCY + 0.75 * k, 0]) for k in range(-1, 2)]
        ring_ = mt[1]
        self.play(FadeIn(bl2), LaggedStart(*[FadeIn(c) for c in chips], lag_ratio=0.3),
                  Rotate(ring_, angle=-TAU, about_point=ring_.get_center(), rate_func=linear), run_time=1.2)
        self.play(LaggedStart(*[c.animate.move_to([4.0, -2.0 + 1.1 * k, 0]) for k, c in enumerate(chips)], lag_ratio=0.15),
                  GrowFromEdge(b2, DOWN), run_time=1.6)
        self.play(*[FadeOut(c) for c in chips], FadeIn(v2), run_time=0.4)
        self.finish()


# ----------------------------------------------------------------------------------------------
class S05Route2(SpokenScene):
    def construct(self):
        # A single connected route; no duplicate pyruvate/lactate chips.
        cl = cell_left("glial cell")
        glu = chip("glucose", TEXT, 26).move_to([-5.1, 2.1, 0])
        pyr = chip("pyruvate", ORANGE, 26).move_to([-5.1, 0.4, 0])
        ga = arr([-5.1, 1.65, 0], [-5.1, 0.9, 0])
        gl = T("glycolysis", 24, GREY).move_to([-3.15, 1.25, 0])
        mt = mito_big(LCX, -2.0, w=4.8, h=1.5)
        self.add(cl, glu, pyr, ga, gl, mt)
        self.at("become lactate")
        ra = arr([-4.0, 0.4, 0], [-3.1, 0.4, 0], ORANGE, 6)
        lac = chip("lactate", ORANGE, 26).move_to([-2.1, 0.4, 0])
        self.play(GrowArrow(ra), FadeIn(lac), run_time=0.7)
        self.at("turns NADH")
        nadh = chip("NADH", TEXT, 26).move_to([-3.55, -0.45, 0])
        self.play(FadeIn(nadh), run_time=0.4)
        self.at("back into")
        self.play(Transform(nadh, chip("NAD+", TEXT, 26).move_to(nadh)), run_time=0.7)
        self.at("so glycolysis keeps running")
        self.play(Indicate(ga, color=ORANGE, scale_factor=1.15), run_time=0.8)
        self.at("without mitochondria")
        self.play(Transform(mt, mito_big(LCX, -2.0, w=4.8, h=1.5, on=False)), run_time=0.7)
        self.at("another cell can")
        rc = cell_right("another cell", TEXT)
        gate = gate_one(GATE_X, 0.4)
        rmt = mito_big(RCX, MCY, w=4.8, on=True)
        rmt[2].move_to([RCX, -2.95, 0])
        export = arr([-1.15, 0.4, 0], [3.0, 0.4, 0], ORANGE, 5)
        # Gate sits above the route, so its MCT label remains readable.
        self.play(FadeIn(rc), FadeIn(gate), FadeIn(rmt), GrowArrow(export), run_time=0.4)
        carried = lac.copy()
        self.add(carried)
        self.play(carried.animate.move_to([GATE_X, 0.4, 0]), run_time=0.35)
        self.at("turn lactate back")
        self.play(carried.animate.move_to([RCX, 0.4, 0]), run_time=0.35)
        self.play(Transform(carried, chip("pyruvate", ORANGE, 26).move_to([RCX, 0.4, 0])), run_time=0.3)
        burn = arr([RCX, -0.1, 0], [RCX, MCY + 0.6, 0], ORANGE, 5)
        self.at("burn it")
        self.play(GrowArrow(burn), carried.animate.move_to([RCX, MCY + 0.4, 0]), run_time=0.4)
        self.play(FadeOut(carried, scale=0.3), Rotate(rmt[1], angle=-TAU,
                  about_point=rmt[1].get_center(), rate_func=linear), run_time=0.4)
        self.wait(0.6)
        self.finish()


# ----------------------------------------------------------------------------------------------
class S06Tally(SpokenScene):
    def construct(self):
        BX, BY, UNIT = 0.3, -3.3, 0.2
        kept, carried = 2, 29
        seg1 = Rectangle(width=2.2, height=kept * UNIT, stroke_color=GREY, stroke_width=3, fill_color=GREY, fill_opacity=0.2)
        seg1.move_to([BX, BY + kept * UNIT / 2, 0])
        seg2 = Rectangle(width=2.2, height=carried * UNIT, stroke_color=GREY, stroke_width=3, fill_color=GREY, fill_opacity=0.2)
        seg2.move_to([BX, BY + kept * UNIT + carried * UNIT / 2, 0])
        sep = Line([BX - 1.1, BY + kept * UNIT, 0], [BX + 1.1, BY + kept * UNIT, 0], color=TEXT, stroke_width=4)
        top = BY + (kept + carried) * UNIT
        brace = DoubleArrow([-1.2, BY, 0], [-1.2, top, 0], color=GREY, buff=0, stroke_width=4, tip_length=0.2)
        bl = VGroup(T("glucose burned fully:", 30, TEXT), T("about 30 to 32 ATP", 32, YELLOW, weight=BOLD)).arrange(DOWN, buff=0.15).move_to([-4.0, 0.0, 0])
        self.at("a cell that")
        self.play(GrowFromEdge(seg1, DOWN), GrowFromEdge(seg2, DOWN), GrowArrow(brace), FadeIn(bl), FadeIn(sep), run_time=1.2)

        def left(m, y, x=1.8):
            return m.move_to([x + m.width / 2, y, 0])

        self.at("keeps only two")
        k1 = left(T("2 ATP: kept", 30, YELLOW), -2.8)
        k2 = left(T("by the glial cell", 26, GREY), -3.28)
        self.play(seg1.animate.set_fill(YELLOW, 0.9).set_stroke(YELLOW), FadeIn(k1), FadeIn(k2), run_time=0.7)
        self.at("its lactates carry")
        o1 = left(T("about 28 to 30 ATP", 30, ORANGE), 0.4)
        o2 = left(T("in the two lactates", 28, ORANGE), -0.1)
        self.play(seg2.animate.set_fill(ORANGE, 0.85).set_stroke(ORANGE), FadeIn(o1), FadeIn(o2), run_time=0.8)
        self.at("more than nine")
        nt = left(T("more than nine-tenths", 30, TEXT, weight=BOLD), 1.5)
        self.play(FadeIn(nt, shift=UP * 0.1), Indicate(seg2, color=ORANGE, scale_factor=1.04), run_time=1.0)
        self.at("could yield")
        pf = left(T("portable fuel", 42, ORANGE, font=TITLE_FONT), 2.7)
        self.play(FadeIn(pf, shift=UP * 0.1), run_time=0.7)
        self.finish()


# ----------------------------------------------------------------------------------------------
class S07Test(SpokenScene):
    def construct(self):
        CYY, HH = 0.4, 6.4     # boxes span y -2.8 .. 3.6
        cl = cell_left("myelinating cell", cy=CYY, ch=HH)
        rc = cell_right("axon", BLUE, cy=CYY, ch=HH)
        tube, bands = myelin_axon(1.3, 6.4, 0.9, 2, tube_h=1.3, band_h=0.85)
        axlab = T("myelin around the axon", 26, GREY).move_to([RCX + 0.4, 2.75, 0])
        nuc = Ellipse(width=5.0, height=1.3, stroke_color=GREY, stroke_width=3, fill_color=GREY, fill_opacity=0.1).move_to([LCX, 1.9, 0])
        nl = T("nucleus", 26, GREY).move_to([LCX, 2.85, 0])
        g1 = rrect(0.95, 0.6, GREY, 0.45, 3, 0.1).move_to([LCX - 1.55, 1.9, 0])
        g2 = rrect(1.75, 0.6, GREY, 0.45, 3, 0.1).move_to([LCX, 1.9, 0])
        g3 = rrect(0.95, 0.6, GREY, 0.45, 3, 0.1).move_to([LCX + 1.55, 1.9, 0])
        gl = T("Cox10", 26, TEXT).move_to(g2)
        gene = VGroup(g1, g2, g3, gl)
        mb = mito_big(LCX, -1.0, on=True, label="respiratory chain", cyc=" ")
        mb[1].set_opacity(0)
        xs = [LCX - 1.65, LCX - 0.55, LCX + 0.55, LCX + 1.65]
        blocks = VGroup(*[VGroup(rrect(0.9, 0.7, YELLOW, 0.3, 3, 0.1).move_to([x, -1.0, 0]),
                                 T(n, 26, YELLOW).move_to([x, -1.0, 0])) for x, n in zip(xs, ["I", "II", "III", "IV"])])
        self.play(FadeIn(cl), FadeIn(rc), FadeIn(tube), FadeIn(bands), FadeIn(axlab), FadeIn(nuc), FadeIn(nl), FadeIn(gene),
                  FadeIn(mb), FadeIn(blocks), run_time=0.9)
        self.at("one laboratory")
        credit = VGroup(T("Fünfschilling, Nave", 28, GREY), T("and colleagues, 2012", 28, GREY)).arrange(DOWN, buff=0.1).move_to([RCX, -1.4, 0])
        self.play(FadeIn(credit), run_time=0.6)
        self.at("deleted the gene")
        self.play(g2.animate.set_stroke(RED).set_fill(RED, 0.2), gl.animate.set_color(RED), run_time=0.5)
        cx = cross([LCX, 1.9, 0], RED, 0.55, 8)
        self.play(Create(cx), run_time=0.3)
        self.play(g2.animate.shift(UP * 0.0).set_opacity(0), gl.animate.set_opacity(0), FadeOut(cx, scale=1.4), run_time=0.5)
        self.at("in myelinating cells")
        self.play(Indicate(cl[1], color=TEAL, scale_factor=1.25), run_time=0.8)
        self.at("without it")
        tl = Arrow([-5.9, -3.1, 0], [5.9, -3.1, 0], buff=0, color=GREY, stroke_width=5, tip_length=0.25)
        tt = T("weeks to months: the old complex IV wears out", 26, GREY).move_to([0, -3.5, 0])
        self.play(GrowArrow(tl), FadeIn(tt), run_time=1.0, rate_func=linear)
        lost = T("complex IV lost", 26, RED).move_to([LCX, -2.55, 0])
        self.play(blocks[3][0].animate.set_stroke(GREY, opacity=0.35).set_fill(GREY, 0.03), blocks[3][1].animate.set_color(GREY).set_opacity(0.4),
                  FadeIn(lost), run_time=0.5)
        self.at("only by glycolysis")
        gly = chip("glycolysis only", ORANGE, 28).move_to([LCX, 0.8, 0])
        self.play(FadeIn(gly, scale=0.8), blocks[0:3].animate.set_opacity(0.35), mb[0].animate.set_stroke(opacity=0.4), run_time=0.9)
        self.finish()


# ----------------------------------------------------------------------------------------------
class S08Q(SpokenScene):
    def construct(self):
        y0 = 1.2
        head = T("Pause and predict", 34, YELLOW).move_to([0, 3.45, 0])
        st = stage(y0)
        tube, bands, stalk, myl, axl = stage_axon(y0)
        c1, c2 = choice_cards()
        tl, q = months_arrow()
        self.play(FadeIn(head), FadeIn(st), run_time=0.8)
        self.at("must respire")
        self.play(Indicate(st[1], color=YELLOW, scale_factor=1.35), run_time=0.9)
        self.at("keep axons healthy")
        self.play(GrowFromEdge(tube, LEFT), FadeIn(bands), Create(stalk), FadeIn(myl), FadeIn(axl), run_time=1.3)
        self.at("what should happen")
        self.play(FadeIn(c1, shift=UP * 0.15), FadeIn(c2, shift=UP * 0.15), FadeIn(q, scale=0.5), run_time=0.8)
        self.at("following months")
        self.play(GrowArrow(tl[0]), FadeIn(tl[1]), run_time=1.0)
        self.finish()


class S09Pause(NarratedScene):
    def construct(self):
        self.add(predict_frame())
        self.wait(self.narration_s)
        self.finish()


# ----------------------------------------------------------------------------------------------
def result_ticks(y0=1.2):
    return tick([-2.1, y0 - 1.85, 0]), tick([5.7, y0 + 1.55, 0]), tick([5.45, y0 - 1.35, 0])


class S10Reveal(SpokenScene):
    def construct(self):
        y0 = 1.2
        head = T("adult CNS, the months followed", 30, GREY).move_to([0, 3.45, 0])
        st = stage(y0)
        tube, bands, stalk, myl, axl = stage_axon(y0)
        self.play(FadeIn(head), FadeIn(st), Create(stalk), run_time=0.6)
        self.at("myelin and axons should fail")
        # the faint "expected" picture, in the same place as the real one: thin myelin, swollen axon
        gtube = Rectangle(width=6.4, height=0.5, stroke_width=0, fill_color=BLUE, fill_opacity=0.3).move_to([3.4, y0, 0])
        gsw = VGroup(*[Ellipse(width=1.5, height=1.5, stroke_color=RED, stroke_width=3, fill_color=BLUE, fill_opacity=0.3).move_to([x, y0, 0]).set_stroke(opacity=0.5)
                       for x in (1.7, 3.5, 5.3)])
        gsh = VGroup(*[rrect(1.2, 0.12, GREY, 0.3, 2, 0.05).move_to([x, y0 + s * 0.95, 0]).set_stroke(opacity=0.4)
                       for x in (0.9, 2.6, 4.4, 6.0) for s in (1, -1)])
        gl = T("expected: failure", 30, RED).move_to([4.5, y0 - 1.55, 0]).set_opacity(0.55)
        gh = VGroup(gtube, gsh, gsw, gl)
        gh.set_opacity(0.55)
        self.play(FadeIn(gh), run_time=1.0)
        self.at("instead")
        self.play(FadeOut(gh), run_time=0.6)
        self.at("oligodendrocyte survived")
        t1, t2, t3 = result_ticks(y0)
        self.play(GrowFromEdge(tube, LEFT), FadeIn(bands), run_time=0.9)
        self.play(Create(t1), run_time=0.5)
        self.at("myelin and axons were largely")
        self.play(FadeIn(myl), FadeIn(axl), run_time=0.5)
        self.play(Create(t2), run_time=0.4)
        self.play(Create(t3), run_time=0.4)
        res = T("myelin and axon: largely preserved", 36, GREEN, weight=BOLD).move_to([0.9, -2.9, 0])
        self.at("preserved for months")
        self.play(FadeIn(res, shift=UP * 0.1), Indicate(VGroup(t1, t2, t3), color=GREEN, scale_factor=1.15), run_time=1.0)
        self.finish()


class S11Beat(NarratedScene):
    def construct(self):
        y0 = 1.2
        head = T("adult CNS, the months followed", 30, GREY).move_to([0, 3.45, 0])
        st = stage(y0)
        tube, bands, stalk, myl, axl = stage_axon(y0)
        t1, t2, t3 = result_ticks(y0)
        res = T("myelin and axon: largely preserved", 36, GREEN, weight=BOLD).move_to([0.9, -2.9, 0])
        self.add(head, st, tube, bands, stalk, myl, axl, t1, t2, t3, res)
        self.wait(self.narration_s)
        self.finish()


# ----------------------------------------------------------------------------------------------
class S12Mean(SpokenScene):
    def construct(self):
        CYY, HH = 0.4, 6.4
        cl = cell_left("oligodendrocyte", cy=CYY, ch=HH)
        rc = cell_right("axon", BLUE, cy=CYY, ch=HH)
        AYY = 1.0
        tube, bands = myelin_axon(2.0, 6.4, AYY, 3, tube_h=0.9, band_h=0.55)
        axl = T("myelin around the axon", 26, GREY).move_to([4.2, 2.35, 0])
        mt = mito_big(LCX, -1.7, h=2.0, on=False)
        self.play(FadeIn(cl), FadeIn(rc), FadeIn(tube), FadeIn(bands), FadeIn(axl), FadeIn(mt), run_time=0.7)
        self.at("made their myelin")
        done = T("myelin already made", 26, TEAL).move_to([-4.65, 2.7, 0])
        self.play(FadeIn(done), run_time=0.5)
        self.at("on glycolysis alone")
        GL = np.array([-5.3, 2.0, 0])
        glu = chip("glucose", TEXT, 26).move_to(GL)
        ga = arr([-4.4, 2.0, 0], [-3.5, 2.0, 0], GREY, 5, 0.2)
        gal = T("glycolysis", 26, GREY).move_to([-3.45, 1.5, 0])
        atp = chip("2 ATP", YELLOW, 26).move_to([-1.25, 2.05, 0])
        self.play(FadeIn(glu), GrowArrow(ga), FadeIn(gal), run_time=0.7)
        self.play(FadeIn(atp, shift=DOWN * 0.15), run_time=0.5)
        self.at("pyruvate and lactate")
        pyr = chip("pyruvate", ORANGE, 26).move_to([-5.1, 0.1, 0])
        lac = chip("lactate", ORANGE, 26).move_to([-2.0, 0.4, 0])
        self.play(TransformFromCopy(glu, pyr), TransformFromCopy(glu, lac), run_time=0.9)
        self.at("cannot burn")
        x = cross([LCX, -1.7], RED, 0.55, 8)
        self.play(pyr.animate.move_to([-5.1, 0.1, 0]), lac.animate.move_to([-2.2, 0.4, 0]), FadeIn(x), run_time=0.8)
        self.at("must leave")
        gate = gate_one(GATE_X, 0.4)
        q = T("?", 64, YELLOW, weight=BOLD).move_to([GATE_X, 1.9, 0])
        la = arr([-1.1, 0.4, 0], [GATE_X - 0.35, 0.4, 0], ORANGE, 5, 0.2)
        ll = T("leave", 26, ORANGE).move_to([-0.9, -0.1, 0])
        self.play(FadeIn(gate), FadeIn(q, scale=0.5), GrowArrow(la), FadeIn(ll), lac.animate.move_to([-2.0, 0.4, 0]), run_time=1.0)
        self.at("left over")
        lo = T("or be left over", 26, ORANGE).move_to([-5.1, -0.5, 0])
        self.play(Indicate(pyr, color=ORANGE, scale_factor=1.2), FadeIn(lo), run_time=0.9)
        self.at("leaving would fit")
        dash = DashedLine([GATE_X + 0.4, 0.5, 0], [4.5, AYY, 0], color=ORANGE, stroke_width=6, dash_length=0.2)
        dash.add_tip(tip_length=0.25)
        fl = T("fits, not shown", 30, YELLOW).move_to([3.6, -0.45, 0])
        self.play(FadeOut(q), Create(dash), FadeIn(fl), run_time=0.8)
        self.at("but this does not", lead=0.5)
        card = VGroup(T("glia can live on glycolysis", 28, TEXT),
                      T("axons do not need glial respiration", 28, TEXT)).arrange(DOWN, buff=0.12).move_to([0, -3.35, 0])
        self.play(FadeIn(card), Indicate(fl, color=YELLOW, scale_factor=1.08), run_time=0.3)
        self.finish()


# ----------------------------------------------------------------------------------------------
class S13Pns(SpokenScene):
    def construct(self):
        C = np.array([2.5, 0.0, 0])
        bundle = Circle(radius=3.65, stroke_color=GREY, stroke_width=4, fill_color=GREY, fill_opacity=0.06).move_to(C)
        pos = [C] + [C + 2.2 * np.array([np.cos(a), np.sin(a), 0]) for a in np.arange(6) * TAU / 6 + 0.35]
        axons = VGroup(*[Circle(radius=0.6, stroke_color=BLUE, stroke_width=3, fill_color=BLUE, fill_opacity=0.45).move_to(p) for p in pos])
        title = T("peripheral nerve", 34, TEXT).move_to([-4.0, 3.0, 0])
        self.play(FadeIn(bundle), LaggedStart(*[GrowFromCenter(a) for a in axons], lag_ratio=0.1), FadeIn(title), run_time=1.6)
        self.at("schwann cells")
        sch = VGroup(*[Circle(radius=1.0, stroke_color=TEAL, stroke_width=4, fill_color=TEAL, fill_opacity=0.12).move_to(p) for p in pos])
        sl = VGroup(T("Schwann cells", 32, TEAL), T("without Cox10", 30, TEAL)).arrange(DOWN, buff=0.1).move_to([-4.0, 1.8, 0])
        self.play(LaggedStart(*[FadeIn(s) for s in sch], lag_ratio=0.1), FadeIn(sl), run_time=1.2)
        self.add(axons)
        self.at("survived")
        sv = T("survived", 34, GREEN).move_to([-4.0, 0.6, 0])
        self.play(FadeIn(sv, shift=UP * 0.1), run_time=0.5)
        self.at("failed to myelinate")
        thin = VGroup()
        for i, p in enumerate(pos):
            if i in (0, 2, 5):
                continue
            thin.add(Arc(radius=0.78, start_angle=0.5 + i, angle=2.2, arc_center=p, stroke_color=TEXT, stroke_width=9))
        tl = VGroup(T("thin or missing", 30, GREY), T("myelin", 30, GREY)).arrange(DOWN, buff=0.08).move_to([-4.0, -0.7, 0])
        self.play(Create(thin), FadeIn(tl), run_time=1.2)
        self.at("severe neuropathy")
        ringr = Circle(radius=3.85, stroke_color=RED, stroke_width=10).move_to(C)
        sn = VGroup(T("severe", 42, RED, weight=BOLD), T("neuropathy", 42, RED, weight=BOLD)).arrange(DOWN, buff=0.05).move_to([-4.2, -2.3, 0])
        self.play(Create(ringr), FadeIn(sn, shift=UP * 0.1), run_time=0.6)
        self.wait(1.0)
        self.finish()


# ----------------------------------------------------------------------------------------------
class S14Stage(SpokenScene):
    def construct(self):
        C = np.array([-2.6, 0.1, 0])
        cell = Ellipse(width=7.6, height=6.3, stroke_color=TEAL, stroke_width=4, fill_color=TEAL, fill_opacity=0.12).move_to([-2.6, -0.2, 0])
        cl = T("Schwann cell", 28, TEAL).move_to([-2.6, 3.5, 0])
        ax = Circle(radius=1.1, stroke_color=BLUE, stroke_width=4, fill_color=BLUE, fill_opacity=0.4).move_to(C)
        axl = T("axon", 26, BLUE).move_to(C)
        u = ValueTracker(0.02)
        sp = always_redraw(lambda: ParametricFunction(
            lambda t: C + (1.2 + 0.07 * t) * np.array([np.cos(t), np.sin(t), 0]),
            t_range=[0, max(u.get_value(), 0.03)], stroke_color=GREY, stroke_width=8))
        self.add(sp)
        self.play(FadeIn(cell), FadeIn(cl), FadeIn(ax), FadeIn(axl), run_time=0.8)
        self.at("building myelin")
        ml = T("still myelinating", 26, GREY).move_to([-2.6, 2.3, 0])
        self.play(u.animate.set_value(2.5 * PI), FadeIn(ml), run_time=1.4, rate_func=linear)
        self.at("costly stage")
        fr = rrect(0.9, 4.2, YELLOW, 0.0, 4, 0.15).move_to([4.4, -0.1, 0])
        el = VGroup(T("energy", 26, YELLOW), T("demand", 26, YELLOW)).arrange(DOWN, buff=0.05).move_to([4.4, -2.85, 0])
        fill2 = Rectangle(width=0.7, height=3.7, stroke_width=0, fill_color=YELLOW, fill_opacity=0.9).move_to([4.4, -0.1 - 2.1 + 1.85, 0])
        hi = T("high", 26, YELLOW).move_to([4.4, 2.35, 0])
        self.play(FadeIn(fr), FadeIn(el), GrowFromEdge(fill2, DOWN), FadeIn(hi), run_time=1.2)
        self.at("they survived")
        sv = T("cell survives", 28, GREEN).move_to([-2.6, -3.65, 0])
        self.play(FadeIn(sv), run_time=0.6)
        self.at("needed respiration")
        mt = mito_small(-2.6, -2.0, False, 1.8, 0.95)
        mx = cross([-2.6, -2.0], RED, 0.4, 7)
        ml2 = T("no respiration", 26, RED).move_to([-2.6, -2.85, 0])
        fr2 = rrect(0.9, 4.2, YELLOW, 0.0, 4, 0.15).move_to([5.9, -0.1, 0])
        el2 = VGroup(T("energy", 26, YELLOW), T("made", 26, YELLOW)).arrange(DOWN, buff=0.05).move_to([5.9, -2.85, 0])
        fill3 = Rectangle(width=0.7, height=0.55, stroke_width=0, fill_color=YELLOW, fill_opacity=0.9).move_to([5.9, -2.2 + 0.275, 0])
        self.play(FadeIn(mt), FadeIn(mx), FadeIn(ml2), FadeIn(fr2), FadeIn(el2), GrowFromEdge(fill3, DOWN), run_time=0.9)
        stall = T("wrap stalls", 26, RED).move_to([-2.6, 2.3, 0])
        self.play(Transform(ml, stall), run_time=0.5)
        self.at("stage may explain")
        why = VGroup(T("the stage may be", 26, TEXT), T("part of the reason", 26, TEXT)).arrange(DOWN, buff=0.08).move_to([5.15, 3.3, 0])
        self.play(FadeIn(why, shift=UP * 0.1), run_time=0.7)
        self.finish()


# ----------------------------------------------------------------------------------------------
class S15Clue(SpokenScene):
    def construct(self):
        YB = -1.9
        sp = Spectrum(-5.6, 6.4, YB, 4.6)
        grey = sp.grey()
        ticks = sp.ticks()
        mu = T("mutant mice", 34, TEXT, weight=BOLD).move_to([-4.2, 2.25, 0])
        sig = T("signal", 26, GREY).rotate(PI / 2).move_to([-6.4, 0.3, 0])
        amp = ValueTracker(0.0)
        lac = always_redraw(lambda: sp.lac(amp.get_value()))
        self.add(lac)
        self.play(Create(grey, rate_func=linear), FadeIn(ticks), FadeIn(mu), FadeIn(sig), run_time=1.6)
        self.at("a scan that measures")
        sl = T("a scan of brain chemicals", 26, GREY).move_to([-3.4, 3.4, 0])
        self.play(FadeIn(sl), run_time=0.5)
        oc = T("other brain chemicals", 26, GREY).move_to([-0.9, 3.45, 0])
        ol = Line([0.55, 3.35, 0], [sp.x_of(2.02) - 0.05, YB + 4.6 + 0.15, 0], color=GREY, stroke_width=3)
        self.play(FadeIn(oc), Create(ol), FadeOut(sl), run_time=0.6)
        self.at("extra lactate")
        ll = T("lactate", 32, ORANGE, weight=BOLD).move_to([sp.x_of(1.33) - 1.3, 0.9, 0])
        self.play(amp.animate.set_value(0.85), FadeIn(ll), run_time=0.9, rate_func=smooth)
        self.at("only under anesthesia")
        an = chip("anaesthesia", PINK, 30).move_to([5.1, 3.25, 0])
        self.play(FadeIn(an, shift=DOWN * 0.2), run_time=0.6)
        self.play(Indicate(ll, color=ORANGE, scale_factor=1.15), run_time=0.8)
        self.at("within an hour")
        face, hand, top = clock([5.9, -3.15], 0.55)
        hl = T("within an hour", 26, TEXT).move_to([3.7, -3.15, 0])
        self.play(FadeIn(face), FadeIn(hand), FadeIn(top), FadeIn(hl), run_time=0.5)
        self.at("the anesthetic ended")
        self.play(FadeOut(an, shift=UP * 0.2), Rotate(hand, angle=-TAU, about_point=hand.get_start(), rate_func=linear), run_time=1.4)
        self.at("fell below detection")
        self.play(amp.animate.set_value(0.0), FadeOut(ll), run_time=0.7)
        flat = T("below detection", 26, GREY).move_to([sp.x_of(1.33), YB + 0.5, 0])
        self.play(FadeIn(flat), run_time=0.25)
        self.wait(1.0)
        self.finish()


def two_panels():
    """final picture of the question scene (also used by the pause)."""
    head = T("Pause and predict", 30, YELLOW).move_to([-5.0, 3.55, 0])
    mu = T("mutant mice", 32, TEXT, weight=BOLD).move_to([1.3, 3.55, 0])
    YB, H = -2.0, 4.1
    spA = Spectrum(-6.5, -0.5, YB, H)
    spB = Spectrum(0.5, 6.5, YB, H)
    ga, gb = spA.grey(), spB.grey()
    la = spA.lac(0.85)
    lb = spB.lac(0.0)
    ta, tb = spA.ticks(), spB.ticks()
    ca = chip("under anaesthesia", PINK, 28).move_to([-3.5, 2.85, 0])
    cb = chip("not under anaesthesia", GREY, 28).move_to([3.5, 2.85, 0])
    q = T("Why would it show up only under anaesthesia?", 36, YELLOW)
    fit(q, 12.4)
    q.move_to([0, -3.4, 0])
    return head, mu, ga, gb, la, lb, ta, tb, ca, cb, q


class S16Q2(SpokenScene):
    def construct(self):
        head, mu, ga, gb, la, lb, ta, tb, ca, cb, q = two_panels()
        self.play(FadeIn(head), FadeIn(mu), FadeIn(ga), FadeIn(gb), FadeIn(ta), FadeIn(tb), run_time=0.6)
        self.at("show up only")
        self.play(FadeIn(la), FadeIn(ca), FadeIn(cb), run_time=0.5)
        self.at("under anesthesia")
        self.play(FadeIn(q, shift=UP * 0.1), run_time=0.6)
        self.finish()


class S17Pause(NarratedScene):
    def construct(self):
        self.add(*two_panels())
        self.wait(self.narration_s)
        self.finish()


# ----------------------------------------------------------------------------------------------
# scenes 18-20: glial cell left, long gap with one transporter, partner box right
BY, BH = -0.2, 6.4        # boxes span y -3.4 .. 3.0
LBX, LBW = -4.3, 4.8      # glial cell box x -6.7 .. -1.9
PBX, PBW = 4.55, 4.3      # partner box x 2.4 .. 6.7
FLY = 0.9                 # height of the lactate stream
MCTX = -1.2


def flow_scene_parts(partner_label, partner_color, label_size=32):
    lbox = rrect(LBW, BH, TEAL, 0.08, 4, 0.5).move_to([LBX, BY, 0])
    llab = T("glial cell", 26, TEAL).move_to([LBX, BY + BH / 2 - 0.4, 0])
    gly = chip("glycolysis", ORANGE, 28).move_to([LBX, FLY, 0])
    mt = mito_small(LBX, -1.5, False, 2.2, 1.2)
    mx = cross([LBX, -1.5, 0], RED, 0.5, 6)
    gate = gate_one(MCTX, FLY)
    pbox = rrect(PBW, BH, partner_color, 0.08, 4, 0.5).move_to([PBX, BY, 0])
    plab = T(partner_label, label_size, TEXT if partner_color == GREY else partner_color, weight=BOLD).move_to([PBX, BY + BH / 2 - 0.5, 0])
    return VGroup(lbox, llab, gly, mt, mx), gate, VGroup(pbox, plab)


PILE = [[-0.6 + 0.5 * (k % 4), 1.6 + 0.5 * (k // 4), 0] for k in range(8)]


def stream_dot(delay_rt=1.0):
    d = dotc(ORANGE, 0.17).move_to([MCTX + 0.4, FLY, 0])
    return d, Succession(FadeIn(d, run_time=0.1), d.animate.move_to([2.3, FLY, 0]).set_rate_func(linear), FadeOut(d, run_time=0.1))


class S18R1(SpokenScene):
    def construct(self):
        left, gate, right = flow_scene_parts("something", GREY)
        one = T("one reading", 30, GREY).move_to([0.2, 3.35, 0])
        q = T("?", 80, YELLOW, weight=BOLD).move_to([PBX, -0.9, 0])
        self.play(FadeIn(left), FadeIn(gate), FadeIn(right), FadeIn(q), FadeIn(one), run_time=0.8)
        self.at("make more lactate")
        stream = arr([MCTX + 0.45, FLY, 0], [2.3, FLY, 0], ORANGE, 9, 0.3)
        ll = T("lactate", 28, ORANGE).move_to([0.55, FLY + 0.75, 0])
        self.play(GrowArrow(stream), FadeIn(ll), run_time=0.6)
        dots = [stream_dot() for _ in range(5)]
        rt1 = max(0.8, self.t_of("awake") - 0.2 - self.elapsed() - 0.05)
        self.play(LaggedStart(*[a for _, a in dots], lag_ratio=0.2), run_time=rt1)
        self.at("awake")
        aw = chip("awake", GREEN, 30).move_to([0.2, 2.45, 0])
        self.play(FadeIn(aw), run_time=0.4)
        self.at("something uses it")
        dots3 = [stream_dot() for _ in range(6)]
        rt3 = max(0.8, self.t_of("under anesthesia") - 0.2 - self.elapsed() - 0.05)
        self.play(Indicate(right[0], color=ORANGE, scale_factor=1.03, run_time=0.8),
                  LaggedStart(*[a for _, a in dots3], lag_ratio=0.2), run_time=rt3)
        self.at("under anesthesia")
        an = chip("anaesthesia", PINK, 30).move_to([0.2, 2.45, 0])
        trickle = DashedLine([MCTX + 0.45, FLY, 0], [2.3, FLY, 0], color=ORANGE, stroke_width=2, dash_length=0.2)
        slow = [dotc(ORANGE, 0.17).move_to([MCTX - 0.05, FLY, 0]) for _ in range(4)]
        self.play(Transform(aw, an), Transform(stream, trickle), right[0].animate.set_stroke(opacity=0.35), right[1].animate.set_opacity(0.45),
                  q.animate.set_opacity(0.3), FadeOut(ll),
                  LaggedStart(*[s.animate.move_to(PILE[i]) for i, s in enumerate(slow)], lag_ratio=0.2), run_time=1.0)
        self.at("that use slows")
        pl = T("lactate piles up", 30, ORANGE).move_to([0.3, -0.5, 0])
        self.play(FadeIn(pl, shift=UP * 0.1), run_time=0.6)
        self.finish()


class S19R2(SpokenScene):
    def construct(self):
        left, gate, right = flow_scene_parts("something", GREY)
        right[0].set_stroke(opacity=0.35)
        right[1].set_opacity(0.45)
        one = T("one reading", 30, GREY).move_to([0.2, 3.35, 0])
        q = T("?", 80, YELLOW, weight=BOLD).move_to([PBX, -0.9, 0]).set_opacity(0.3)
        piled = VGroup(*[dotc(ORANGE, 0.17).move_to(PILE[i]) for i in range(4)])
        self.add(left, gate, right, q, one, piled)
        self.wait(0.1)
        self.at("the axons are")
        nbox = rrect(PBW, BH, BLUE, 0.1, 4, 0.5).move_to([PBX, BY, 0])
        nlab = T("axon", 32, BLUE, weight=BOLD).move_to([PBX, BY + BH / 2 - 0.5, 0])
        tube, bands = myelin_axon(2.7, 6.4, FLY, 2, tube_h=0.9, band_h=0.55)
        self.play(FadeOut(right), FadeIn(nbox), FadeIn(nlab), FadeIn(tube), FadeIn(bands), FadeOut(one), FadeOut(piled), q.animate.set_opacity(1.0), run_time=0.9)
        self.at("obvious candidate user")
        self.play(Indicate(q, color=YELLOW, scale_factor=1.3), run_time=0.9)
        self.at("never traced")
        dash = DashedLine([MCTX + 0.45, FLY, 0], [2.65, FLY, 0], color=ORANGE, stroke_width=6, dash_length=0.2)
        dash.add_tip(tip_length=0.25)
        nt = T("not traced", 34, YELLOW).move_to([0.55, FLY - 0.95, 0])
        self.play(Create(dash), FadeIn(nt, shift=UP * 0.1), run_time=1.0)
        self.at("where the lactate went")
        pulse(self, nt, YELLOW, 1.2, 0.8)
        self.finish()


# ----------------------------------------------------------------------------------------------
class S20Take(SpokenScene):
    def construct(self):
        CY2, H2 = 0.6, 5.8
        lbox = rrect(LW, H2, TEAL, 0.08, 4, 0.5).move_to([LCX, CY2, 0])
        llab = T("oligodendrocyte", 32, TEAL, weight=BOLD).move_to([LCX, 3.1, 0])
        scope = T("adult brain • the months studied", 30, TEXT).move_to([0, 3.75, 0])
        rbox = rrect(RW, H2, BLUE, 0.08, 4, 0.5).move_to([RCX, CY2, 0])
        rlab = T("axon", 28, BLUE).move_to([RCX, 3.1, 0])
        mt_on = mito_big(LCX, 0.5, on=True, cyc=" ")
        tube, bands = myelin_axon(1.4, 6.2, 1.1, 2, tube_h=1.0, band_h=0.7)
        self.play(FadeIn(lbox), FadeIn(llab), FadeIn(rbox), FadeIn(rlab), FadeIn(mt_on), FadeIn(tube), FadeIn(bands), FadeIn(scope), run_time=0.4)
        self.at("switch off the glial")
        mt_off = mito_big(LCX, 0.5, on=False, cyc=" ")
        x = cross([LCX, 0.5], RED, 0.6, 8)
        off_l = T("respiration off", 34, RED).move_to([LCX, -1.6, 0])
        self.play(Transform(mt_on, mt_off), FadeIn(x), FadeIn(off_l), run_time=1.2)
        self.at("the axon in the brain")
        t = tick([RCX + 0.95, 3.1, 0], GREEN, 0.3, 10)
        sp = T("largely preserved", 42, GREEN, weight=BOLD).move_to([RCX, -1.0, 0])
        self.play(Create(t), FadeIn(sp, shift=UP * 0.1), run_time=1.0)
        self.at("over the")
        tl = Arrow([-5.6, -3.35, 0], [5.8, -3.35, 0], buff=0, color=GREY, stroke_width=5, tip_length=0.25)
        tt = T("the months studied", 28, GREY).move_to([0.1, -2.85, 0])
        self.play(GrowArrow(tl), FadeIn(tt), run_time=1.0)
        self.finish()


class S21End(EndCard):
    LINE = "Without oligodendrocyte respiration, brain axons were largely preserved for months."

    def construct(self):
        line = T("Without oligodendrocyte respiration,\nbrain axons were largely preserved for months.",
                 size=40, font=TITLE_FONT, line_spacing=1.25)
        fit(line, max_w=12.5)
        sub = T("biochemistrypedia.com", size=22, color=TEAL)
        VGroup(line, sub).arrange(DOWN, buff=0.6)
        self.play(FadeIn(line, shift=UP * 0.15), run_time=self.beat(0.3))
        self.play(FadeIn(sub), run_time=self.beat(0.15))
        self.finish()
