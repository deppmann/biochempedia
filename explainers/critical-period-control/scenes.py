"""A Window That Follows the Cells: chapter 1 of "Opening and Closing a Critical Period"  (Biochemistrypedia explainer)

COLOR MAP (one color per concept, shared by every chapter; taken from the lesson's earlier film)
  BLUE   = the closed eye (contralateral, the opposite eye) and the cortex response to it
  ORANGE = the open eye (ipsilateral, the same-side eye) and the cortex response to it
  YELLOW = inhibition (inhibitory cells, parvalbumin basket cell, the inhibition curve)
  PURPLE = the GAD enzymes that make GABA (not used in this chapter)
  PINK   = the GABA receptor (not used in this chapter)
  TEAL   = diazepam, and the "predict" card cue (not used for drugs in this chapter)
  GREEN  = the open window in the earlier film; in this chapter the window band is SAND (the lesson's colour for it)
  SAND   = the critical-period window (the band on the age timeline)
  RED    = missing or blocked: the brakes that close the window
  TEXT   = the ocular dominance index and the size of the shift (white)
  GOLD   = the binocular zone of visual cortex
  GREY   = structure, frames, labels, neutral ideas (age, calendar)
"""
import numpy as np
from bp_style import *  # noqa: F401,F403

PURPLE = "#B58CD9"
ORANGE = "#F29E4C"
PINK = "#E58FB8"
SAND = "#D8BD8A"




# ---------------------------------------------------------------------------------------------
# small shapes
# ---------------------------------------------------------------------------------------------
def eye_open(color):
    return VGroup(Ellipse(width=0.9, height=0.5, stroke_color=color, stroke_width=4, fill_color=color, fill_opacity=0.15),
                  Dot(radius=0.12, color=color))


def eye_shut(color):
    lid = ArcBetweenPoints(LEFT * 0.45, RIGHT * 0.45, angle=-PI / 2.6, stroke_color=color, stroke_width=5)
    lashes = VGroup(*[Line(lid.point_from_proportion(p), lid.point_from_proportion(p) + DOWN * 0.12 + RIGHT * dx,
                           stroke_color=color, stroke_width=3) for p, dx in ((0.2, -0.04), (0.5, 0), (0.8, 0.04))])
    return VGroup(lid, lashes)


def mouse_face(closed_color=None, open_color=None, shut=False):
    """Front view of a mouse. The viewer's left eye is the one that closes."""
    c = GREY
    head = Ellipse(width=2.6, height=2.3, stroke_color=c, stroke_width=4, fill_color=c, fill_opacity=0.12)
    ears = VGroup(*[Circle(radius=0.5, stroke_color=c, stroke_width=4, fill_color=c, fill_opacity=0.12).move_to([sx * 1.0, 0.95, 0]) for sx in (-1, 1)])
    snout = Ellipse(width=0.95, height=0.6, stroke_color=c, stroke_width=3, fill_color=c, fill_opacity=0.12).move_to([0, -0.55, 0])
    nose = Dot(radius=0.09, color=c).move_to([0, -0.42, 0])
    whisk = VGroup(*[Line([sx * 0.5, -0.55 + dy * 0.0, 0], [sx * 1.5, -0.55 + dy, 0], color=c, stroke_width=2.5) for sx in (-1, 1) for dy in (0.18, -0.05, -0.28)])
    if shut:
        eyeL = eye_shut(closed_color or GREY).scale(0.8).move_to([-0.6, 0.2, 0])
        eyeR = eye_open(open_color or GREY).scale(0.8).move_to([0.6, 0.2, 0])
    else:
        eyeL = eye_open(GREY).scale(0.8).move_to([-0.6, 0.2, 0])
        eyeR = eye_open(GREY).scale(0.8).move_to([0.6, 0.2, 0])
    return VGroup(ears, head, snout, nose, whisk, eyeL, eyeR)


def mouse_top():
    """Top view of a mouse head, nose up: two eyes, two hemispheres, the binocular zones. Returns (group, zones)."""
    c = GREY
    ears = VGroup(*[Circle(radius=0.55, stroke_color=c, stroke_width=4, fill_color=c, fill_opacity=0.12).move_to([sx * 1.55, 0.2, 0]) for sx in (-1, 1)])
    head = Ellipse(width=3.2, height=3.6, stroke_color=c, stroke_width=4, fill_color=c, fill_opacity=0.10)
    snout = Polygon([-0.7, 1.4, 0], [0.7, 1.4, 0], [0, 2.7, 0], stroke_color=c, stroke_width=4, fill_color=c, fill_opacity=0.10).round_corners(0.3)
    nose = Dot(radius=0.1, color=c).move_to([0, 2.3, 0])
    eyes = VGroup(*[eye_open(c).scale(0.7).move_to([sx * 1.1, 1.0, 0]) for sx in (-1, 1)])
    hemis = VGroup(*[Ellipse(width=1.25, height=2.1, stroke_color=c, stroke_width=3, fill_color=c, fill_opacity=0.14).move_to([sx * 0.68, -0.55, 0]) for sx in (-1, 1)])
    zones = VGroup(*[Ellipse(width=0.6, height=0.55, stroke_width=0, fill_color=GOLD, fill_opacity=0.0).move_to([sx * 0.95, -1.3, 0]) for sx in (-1, 1)])
    g = VGroup(ears, head, snout, nose, eyes, hemis, zones).scale(1.35).move_to([-3.9, 0.0, 0])
    return g, zones


def basket_icon(k=1.0, origin=(0.0, 0.0), scale=1.0):
    """A parvalbumin basket cell (yellow soma, branching axon) wrapping its terminals around a pyramidal cell body (grey).
    k in [0, 1] sets how bold the basket cell is. Returns (group, soma, target)."""
    ox, oy = origin
    sw = 2.0 + 5.0 * k
    op = 0.12 + 0.75 * k
    s = scale
    soma_c = np.array([ox, oy, 0.0])
    tgt_c = np.array([ox + 2.7 * s, oy, 0.0])
    soma = Circle(radius=0.42 * s, stroke_color=YELLOW, stroke_width=sw, fill_color=YELLOW, fill_opacity=op).move_to(soma_c)
    target = Circle(radius=0.6 * s, stroke_color=GREY, stroke_width=4, fill_color=GREY, fill_opacity=0.22).move_to(tgt_c)
    tip = soma_c + RIGHT * 0.42 * s
    hub = soma_c + RIGHT * 1.0 * s
    trunk = Line(tip, hub, color=YELLOW, stroke_width=sw)
    parts = VGroup(trunk)
    basket = VGroup()
    r_b = 0.92 * s
    for deg in (150, 180, 210):
        a = np.radians(deg)
        tp = tgt_c + r_b * np.array([np.cos(a), np.sin(a), 0.0])
        parts.add(Line(hub, tp, color=YELLOW, stroke_width=max(2.0, sw * 0.75)))
    for deg in (128, 142, 155, 168, 180, 192, 205, 218, 232):
        a = np.radians(deg)
        tp = tgt_c + r_b * np.array([np.cos(a), np.sin(a), 0.0])
        basket.add(Dot(tp, radius=(0.06 + 0.045 * k) * s, color=YELLOW))
    arc = Arc(radius=r_b, start_angle=np.radians(124), angle=np.radians(112), arc_center=tgt_c, color=YELLOW, stroke_width=max(2.0, sw * 0.6))
    # Make maturation visible in the entire inhibitory arbor, not just the soma.
    for part in (arc, parts, basket):
        part.set_opacity(0.18 + 0.82 * k)
    g = VGroup(target, arc, parts, basket, soma)
    g.scale(0.82 + 0.18 * k, about_point=soma_c)
    return g, soma, target


def brake_net(center, r_in=0.62, r_out=0.85):
    c = np.array(center, float)
    net = VGroup(Circle(radius=r_in, stroke_color=RED, stroke_width=5).move_to(c), Circle(radius=r_out, stroke_color=RED, stroke_width=5).move_to(c))
    for k in range(12):
        a = k * TAU / 12
        d = np.array([np.cos(a), np.sin(a), 0])
        net.add(Line(c + d * r_in, c + d * r_out, color=RED, stroke_width=4))
    return net


def calendar_icon(color=GREY):
    box = RoundedRectangle(corner_radius=0.12, width=2.0, height=1.8, stroke_color=color, stroke_width=4, fill_color=color, fill_opacity=0.10)
    head = Rectangle(width=2.0, height=0.45, stroke_width=0, fill_color=color, fill_opacity=0.5).move_to(box.get_top() + DOWN * 0.225)
    cells = VGroup(*[Square(0.22, stroke_width=0, fill_color=color, fill_opacity=0.6).move_to([-0.55 + 0.55 * i, -0.05 - 0.4 * j, 0])
                     for j in range(3) for i in range(3)])
    return VGroup(box, head, cells)


def circuit_icon():
    pts = [np.array(p) for p in ([-1.0, 0.0, 0], [0.0, 0.55, 0], [0.0, -0.55, 0], [1.0, 0.0, 0])]
    links = VGroup(*[Line(pts[a], pts[b], color=GREY, stroke_width=4) for a, b in ((0, 1), (0, 2), (1, 3), (2, 3), (1, 2))])
    nodes = VGroup()
    for k, p in enumerate(pts):
        nodes.add(Circle(radius=0.26, stroke_width=0, fill_color=BG, fill_opacity=1).move_to(p))
        nodes.add(Circle(radius=0.26, stroke_color=(YELLOW if k == 1 else GREY), stroke_width=4,
                         fill_color=(YELLOW if k == 1 else GREY), fill_opacity=(0.7 if k == 1 else 0.25)).move_to(p))
    return VGroup(links, nodes)


# ---------------------------------------------------------------------------------------------
# the cortical cell and its two inputs (used from chapter scene 2 to the predict card)
# ---------------------------------------------------------------------------------------------
def width_of(rate):
    return 0.45 * rate


class Diag:
    """Two eyes, two input lines, one cortical cell. The line width shows the response."""

    def __init__(self, dx=0.0, dy=0.0, colored=True, c=30, i=10, shut=False, equal=None):
        self.ec = np.array([-5.2 + dx, 1.65 + dy, 0.0])
        self.ei = np.array([-5.2 + dx, -1.65 + dy, 0.0])
        self.cc = np.array([-0.4 + dx, dy, 0.0])
        self.colored = colored
        self.col_c = BLUE if colored else GREY
        self.col_i = ORANGE if colored else GREY
        self.equal = equal
        wc, wi = (equal, equal) if equal else (width_of(c), width_of(i))
        self.line_c = self.line("c", wc)
        self.line_i = self.line("i", wi)
        self.eye_c = (eye_shut(self.col_c) if shut else eye_open(self.col_c)).scale(1.5).move_to(self.ec)
        self.eye_i = eye_open(self.col_i).scale(1.5).move_to(self.ei)
        self.cell = VGroup(Circle(radius=1.15, stroke_color=GREY, stroke_width=4, fill_color=GREY, fill_opacity=0.22),
                           T("cortical\ncell", 26, GREY, line_spacing=0.8)).move_to(self.cc)
        self.lab_c = T("contralateral\n(opposite side)", 26, BLUE, line_spacing=0.8).move_to(self.ec + UP * 1.0)
        self.lab_i = T("ipsilateral\n(same side)", 26, ORANGE, line_spacing=0.8).move_to(self.ei + DOWN * 1.0)

    def ends(self, which):
        e = self.ec if which == "c" else self.ei
        p0 = e + RIGHT * 0.9
        d = self.cc - p0
        d = d / np.linalg.norm(d)
        return p0, self.cc - d * 1.15

    def line(self, which, w, color=None):
        p0, p1 = self.ends(which)
        col = color or (self.col_c if which == "c" else self.col_i)
        return Line(p0, p1, color=col, stroke_width=w)

    def mid(self, which):
        p0, p1 = self.ends(which)
        return (p0 + p1) / 2

    def base(self):
        return VGroup(self.line_c, self.line_i, self.eye_c, self.eye_i, self.cell)

    def labels(self):
        return VGroup(self.lab_c, self.lab_i)


class Scale:
    """The ocular dominance index scale, -1 to +1, with a marker."""

    def __init__(self, cx=4.2, y=-0.2, w=4.0):
        self.cx, self.y, self.w = cx, y, w
        self.axis = Line([self.x(-1), y, 0], [self.x(1), y, 0], color=GREY, stroke_width=5)
        self.ticks = VGroup()
        for v, s in ((-1, "−1"), (0, "0"), (1, "+1")):
            self.ticks.add(Line([self.x(v), y - 0.12, 0], [self.x(v), y + 0.12, 0], color=GREY, stroke_width=4))
            self.ticks.add(M(s, 26, GREY).move_to([self.x(v), y - 0.5, 0]))
        ln = T("ipsilateral\nonly", 26, ORANGE, line_spacing=0.8).move_to([self.x(-1) + 0.1, y - 1.4, 0])
        rn = T("contralateral\nonly", 26, BLUE, line_spacing=0.8)
        rn.move_to([min(self.x(1) + 0.1, 6.8 - rn.width / 2), y - 1.4, 0])
        self.ends_l = VGroup(ln, rn)
        self.title = T("ocular dominance index", 28, GREY).move_to([cx, y + 1.75, 0])
        self.frame = VGroup(self.axis, self.ticks, self.ends_l, self.title)

    def x(self, v):
        return self.cx + v * self.w / 2

    def marker(self, v, text, color=TEXT):
        tri = Triangle(stroke_width=0, fill_color=color, fill_opacity=1).scale(0.17).rotate(PI).move_to([self.x(v), self.y + 0.3, 0])
        lab = M(text, 40, color, weight=BOLD).move_to([self.x(v), self.y + 0.85, 0])
        return VGroup(tri, lab)


# ---------------------------------------------------------------------------------------------
# age timelines (shift size, inhibition)
# ---------------------------------------------------------------------------------------------
def X(p):
    return -5.5 + 0.19 * p


Y0 = -2.6
SH = 4.6       # height of the shift curve
CREDIT_COL = "#BFC6D2"


def shift_s(p):
    sig = 4.0 if p < 28 else 2.0
    return 0.07 + 0.93 * np.exp(-((p - 28) / sig) ** 2 / 2)


def Ys(p):
    return Y0 + SH * shift_s(p)


def shift_curve():
    return ParametricFunction(lambda t: np.array([X(t), Ys(t), 0]), t_range=[0, 60], color=TEXT, stroke_width=6)


def inhib_f(p):
    return 1 / (1 + np.exp(-(p - 17.2) / 4.5))


IH = 4.2
YT = Y0 + IH * 0.6                      # threshold line
PC = 17.2 + 4.5 * np.log(1.5)           # age at which the normal curve crosses it (about 19)
BTOP = 1.95                             # top of the window band on the inhibition plots


def Yi(p):
    return Y0 + IH * inhib_f(p)


def curve_fn(fn, t0=0.0, t1=60.0, color=YELLOW, sw=6):
    return ParametricFunction(lambda t: np.array([X(t), fn(t), 0]), t_range=[t0, t1], color=color, stroke_width=sw)


def inhib_curve(t0=0, t1=60):
    return curve_fn(Yi, t0, t1)


def axes_plot(ylabel, ycol, ticks=(0, 28, 60), tick_cols=None):
    xa = Arrow([X(0), Y0, 0], [6.5, Y0, 0], buff=0, color=GREY, stroke_width=3, tip_length=0.2)
    ya = Arrow([X(0), Y0, 0], [X(0), 3.15, 0], buff=0, color=GREY, stroke_width=3, tip_length=0.2)
    tk = VGroup()
    for p in ticks:
        tk.add(Line([X(p), Y0 - 0.1, 0], [X(p), Y0 + 0.1, 0], color=GREY, stroke_width=3))
        tk.add(T(f"P{p}", 26, GREY).move_to([X(p), Y0 - 0.5, 0]))
    xl = T("age (postnatal day)", 26, GREY).move_to([0.4, -3.65, 0])
    yl = T(ylabel, 26, ycol).move_to([X(0) - 0.1, 3.5, 0], aligned_edge=LEFT)
    g = VGroup(xa, ya, tk, xl, yl)
    g.yl = yl
    return g


def strips(p0, p1, top, opfun, n=40, color=SAND):
    """A band as one rectangle with a horizontal opacity gradient (soft edges, an open faded end)."""
    ps = np.linspace(p0, p1, n)
    r = Rectangle(width=X(p1) - X(p0), height=top - Y0, stroke_width=0)
    r.move_to([(X(p0) + X(p1)) / 2, (top + Y0) / 2, 0])
    r.set_fill(color=[color] * n, opacity=[float(opfun(p)) for p in ps])
    r.set_sheen_direction(RIGHT)
    r.set_z_index(-1)
    return r


def sig(x):
    return 1 / (1 + np.exp(-x))


def soft_band(top=2.7):
    return strips(15.0, 36.0, top, lambda p: 0.42 * sig((p - 19) / 0.7) * sig((32 - p) / 0.7), n=42)


def open_band(p0=PC, top=BTOP):
    # An unknown closing time: dissolve completely before the adult end.
    return strips(p0, 44, top,
                  lambda p: 0.42 * (1 - np.clip((p - 27) / 17, 0, 1)) ** 2,
                  n=64)


def closed_band(p0=PC, p1=32, top=BTOP):
    return strips(p0, p1, top, lambda p: 0.42, n=40)


def shift_plot(with_peak=True, with_band=False):
    ax = axes_plot("size of the shift", TEXT)
    cur = shift_curve()
    small = T("small", 26, GREY).move_to([X(0) - 0.12, Y0 + 0.5, 0], aligned_edge=RIGHT)
    large = T("large", 26, GREY).move_to([X(0) - 0.12, Y0 + SH, 0], aligned_edge=RIGHT)
    sch = T("schematic", 26, GREY).move_to([4.6, -1.5, 0])
    d = {"ax": ax, "cur": cur, "small": small, "large": large, "sch": sch}
    if with_peak:
        d["pk"] = Dot([X(28), Ys(28), 0], radius=0.13, color=TEXT)
        d["pl"] = T("P28", 26, TEXT, weight=BOLD).move_to([X(28), Ys(28) + 0.5, 0])
    if with_band:
        d["l19"] = DashedLine([X(19), Y0, 0], [X(19), 2.7, 0], color=SAND, stroke_width=3)
        d["l32"] = DashedLine([X(32), Y0, 0], [X(32), 2.7, 0], color=SAND, stroke_width=3)
        d["band"] = soft_band()
        d["t19"] = T("~P19", 26, SAND, weight=BOLD).move_to([X(19) - 0.1, Y0 - 0.5, 0])
        d["t32"] = T("~P32", 26, SAND, weight=BOLD).move_to([X(32) + 0.32, Y0 - 0.5, 0])
        d["cr"] = T("Gordon and Stryker, 1996", 28, CREDIT_COL).move_to([4.1, 2.45, 0])
    return d


# ---------------------------------------------------------------------------------------------
# the predict card (shared by s09, s10 and s11)
# ---------------------------------------------------------------------------------------------
def build_predict(shut=True):
    d = Diag(shut=shut)
    sc = Scale()
    return dict(
        head=T("Pause and predict", 40, TEAL, weight=BOLD).move_to([-1.2, 3.45, 0]),
        diag=d, sc=sc,
        mk=sc.marker(0.5, "0.50"),
        age=chip("two months old (P60)", GREY, size=30).move_to([4.3, 3.4, 0]),
        note=T("same four days, one eye closed", 28, GREY).move_to([-0.4, -3.4, 0]),
        q=T("Shift or not?", 40, TEAL, weight=BOLD).move_to([4.9, -2.55, 0]),
    )


class S00Title(TitleCard):
    LESSON = "Opening and Closing a Critical Period"
    TITLE = "A Window That Follows the Cells"

    def construct(self):
        brand = T("BIOCHEMISTRYPEDIA", size=22, color=TEAL, weight=BOLD)
        lesson = T(self.LESSON.upper(), size=24, color=GREY)
        title = T(self.TITLE, size=54, font=TITLE_FONT)
        fit(title, max_w=11.5)
        rule = Line(LEFT * 1.4, RIGHT * 1.4, color=GOLD, stroke_width=4)
        g = VGroup(brand, lesson, title, rule).arrange(DOWN, buff=0.34).move_to(ORIGIN)
        self.play(FadeIn(g), run_time=0.9)
        self.wait(1.5)
        self.play(FadeOut(g), run_time=0.4)
        self.finish()


# ---------------------------------------------------------------------------------------------
class S01Q(SpokenScene):
    """Young and adult mouse, each closes one eye; the question is posed in the picture."""

    def construct(self):
        S = 2.0
        cy = 0.05

        def panel(cx, name):
            face = mouse_face(BLUE, ORANGE, shut=True).scale(S).move_to([cx, cy, 0])
            nm = T(name, 38, TEXT, weight=BOLD).move_to([cx, 3.3, 0])
            return face, nm

        yf, yn = panel(-3.45, "young (P28)")
        af, an = panel(3.45, "adult (P60)")
        self.add(yf, yn, af, an)
        self.at("one eye closed")
        self.play(Indicate(yf[-2], color=BLUE, scale_factor=1.08),
                  Indicate(af[-2], color=BLUE, scale_factor=1.08), run_time=0.6)
        yc = T("closed eye: big change in cortex", 28, TEXT).move_to([-3.45, -3.3, 0])
        ac = T("closed eye: much less change", 28, GREY).move_to([3.45, -3.3, 0])
        self.at("reshape")
        self.play(FadeIn(yc, shift=UP * 0.1), run_time=0.5)
        self.at("but change")
        self.play(FadeIn(ac, shift=UP * 0.1), run_time=0.5)
        self.at("much less")
        self.play(Indicate(ac, color=TEXT, scale_factor=1.08), run_time=0.8)
        self.finish()


# ---------------------------------------------------------------------------------------------
def s02_panel():
    """The zoomed-in view of the cortical cell (right of the head in s02)."""
    box = RoundedRectangle(corner_radius=0.25, width=7.3, height=7.1, stroke_color=GOLD, stroke_width=3, fill_color=GOLD, fill_opacity=0.04).move_to([3.15, 0, 0])
    g = VGroup()
    # row A: a cell fed by both eyes
    eA1 = eye_open(GREY).scale(1.2).move_to([0.75, 2.45, 0])
    eA2 = eye_open(GREY).scale(1.2).move_to([0.75, 0.85, 0])
    cA = Circle(radius=0.9, stroke_color=GREY, stroke_width=4, fill_color=GREY, fill_opacity=0.22).move_to([5.0, 1.65, 0])
    lA = []
    for e in (eA1, eA2):
        p0 = e.get_center() + RIGHT * 0.8
        d = cA.get_center() - p0
        d = d / np.linalg.norm(d)
        lA.append(Line(p0, cA.get_center() - d * 0.9, color=GREY, stroke_width=7))
    tA1 = T("one eye", 26, GREY).move_to([0.75, 3.05, 0])
    tA2 = T("other eye", 26, GREY).move_to([0.75, 0.2, 0])
    labA = T("most: both eyes", 28, TEXT).move_to([5.0, 0.35, 0])
    # row B: a cell fed by one eye
    eB = eye_open(GREY).scale(1.2).move_to([0.75, -2.0, 0])
    cB = Circle(radius=0.7, stroke_color=GREY, stroke_width=4, fill_color=GREY, fill_opacity=0.22).move_to([5.0, -2.0, 0])
    lB = Line([1.55, -2.0, 0], [4.3, -2.0, 0], color=GREY, stroke_width=7)
    tB = T("one eye", 26, GREY).move_to([0.75, -1.35, 0])
    labB = T("some: one eye only", 28, TEXT).move_to([4.3, -3.2, 0])
    sep = Line([-0.2, -0.45, 0], [6.5, -0.45, 0], color=GREY, stroke_width=2).set_opacity(0.5)
    rowA = VGroup(eA1, eA2, tA1, tA2, cA, *lA)
    rowB = VGroup(eB, tB, cB, lB)
    return box, sep, rowA, labA, rowB, labB, lA


class S02Zone(SpokenScene):
    def construct(self):
        head, zones = mouse_top()
        zl = T("binocular zone", 28, GOLD).move_to([-3.9, -3.5, 0])
        zone = zones[1]
        zline = Line(zl.get_top() + UP * 0.05, zone.get_bottom() + DOWN * 0.05, color=GOLD, stroke_width=3)
        grp = VGroup(head, zl, zline)
        box, sep, rowA, labA, rowB, labB, lA = s02_panel()
        self.play(FadeIn(head), run_time=0.4)
        self.at("binocular zone")
        self.play(*[z.animate.set_fill(opacity=0.95) for z in zones], FadeIn(zl), Create(zline), run_time=0.9)
        self.at("most neurons")
        zc = zone.get_center()
        # The two rays visibly tie the highlighted zone to the enlarged inset.
        zoom = VGroup(
            DashedLine(zc + UR * 0.20, box.get_corner(UL), color=GOLD, stroke_width=4),
            DashedLine(zc + DR * 0.20, box.get_corner(DL), color=GOLD, stroke_width=4))
        self.play(Create(zoom), FadeIn(box), FadeIn(rowA), run_time=0.6)
        self.at("both eyes")
        self.play(FadeIn(labA), Indicate(VGroup(*lA), color=TEXT, scale_factor=1.0), run_time=0.7)
        self.at("some answer only one")
        self.play(FadeIn(rowB), FadeIn(sep), FadeIn(labB), run_time=0.5)
        self.finish()


# ---------------------------------------------------------------------------------------------
class S03Bias(SpokenScene):
    def construct(self):
        d0 = Diag(colored=False, equal=7)
        final = Diag()
        sc = Scale()
        sc.frame.set_opacity(0.3)
        self.add(d0.line_c, d0.line_i, d0.eye_c, d0.eye_i, d0.cell, sc.frame)
        self.at("most cells")
        self.play(Indicate(d0.cell, color=TEXT, scale_factor=1.06), run_time=0.7)
        self.at("opposite side")
        self.play(Transform(d0.line_c, final.line("c", width_of(30))), d0.eye_c.animate.set_color(BLUE), FadeIn(final.lab_c),
                  Transform(d0.line_i, final.line("i", width_of(10))), d0.eye_i.animate.set_color(ORANGE), run_time=0.8)
        self.at("of the head")
        self.play(FadeIn(final.lab_i), run_time=0.6)
        self.play(Indicate(d0.line_c, color=BLUE, scale_factor=1.0), run_time=0.6)
        self.finish()


# ---------------------------------------------------------------------------------------------
class S04Index(SpokenScene):
    def construct(self):
        d = Diag()
        sc = Scale()
        sc.frame.set_opacity(0.3)
        self.add(*d.base(), *d.labels(), sc.frame)
        formula = M("index = (C − I) / (C + I)", 32, TEXT).move_to([3.7, 3.4, 0])
        units = T("C and I are spikes per second", 26, GREY).move_to([3.7, 2.75, 0])
        cl = M("C = 30", 30, BLUE).move_to(d.mid("c") + UP * 0.8 + RIGHT * 0.25)
        il = M("I = 10", 30, ORANGE).move_to(d.mid("i") + DOWN * 0.8 + RIGHT * 0.25)
        sub = M("(30 − 10) / (30 + 10) = 0.50", 30, TEXT).move_to([1.6, -3.45, 0])
        mk0 = sc.marker(0.0, "0.00")
        mk1 = sc.marker(0.5, "0.50")
        self.at("ocular dominance index")
        self.play(Write(formula), run_time=1.2)
        self.at("puts a number")
        self.play(sc.frame.animate.set_opacity(1), run_time=0.6)
        self.at("preference")
        self.play(Indicate(d.line_c, color=BLUE, scale_factor=1.0), Indicate(d.line_i, color=ORANGE, scale_factor=1.0), run_time=0.8)
        self.at("example cell")
        self.play(FadeIn(cl), FadeIn(il), FadeIn(units), run_time=0.6)
        self.at("scores")
        self.play(Write(sub), run_time=0.8)
        self.play(FadeIn(mk0), run_time=0.15)
        self.play(Transform(mk0, mk1), run_time=0.7)
        self.wait(1.0)
        self.finish()


# ---------------------------------------------------------------------------------------------
def clock_parts():
    cc = np.array([3.0, 3.0, 0])
    face = Circle(radius=0.72, stroke_color=GREY, stroke_width=4, fill_color=GREY, fill_opacity=0.12).move_to(cc)
    tks = VGroup(*[Line(cc + 0.72 * np.array([np.sin(a), np.cos(a), 0]) * 0.8, cc + 0.72 * np.array([np.sin(a), np.cos(a), 0]), color=GREY, stroke_width=3)
                   for a in (0, PI / 2, PI, 3 * PI / 2)])
    hand = Line(cc, cc + UP * 0.56, color=TEXT, stroke_width=6)
    return cc, face, tks, hand


def carry_state(scene, d, sc, marker_v, marker_text):
    d.line_c.become(d.line("c", width_of(30)))
    d.line_i.become(d.line("i", width_of(10)))
    mk = sc.marker(marker_v, marker_text)
    scene.add(*d.base(), *d.labels(), sc.frame, mk)
    return mk


class S05Close(SpokenScene):
    def construct(self):
        d = Diag()
        sc = Scale()
        mk = carry_state(self, d, sc, 0.5, "0.50")
        self.at("close the opposite")
        shut = eye_shut(BLUE).scale(1.5).move_to(d.ec)
        self.play(ReplacementTransform(d.eye_c, shut), run_time=0.7)
        cc, face, tks, hand = clock_parts()
        days = T("day 0", 38, TEXT, weight=BOLD).move_to([5.4, 3.0, 0])
        self.at("for about four days")
        self.play(FadeIn(face), FadeIn(tks), FadeIn(hand), FadeIn(days), run_time=0.3)
        for n in range(1, 5):
            new = T(f"day {n}" if n < 4 else "4 days", 38, TEXT, weight=BOLD).move_to([5.4, 3.0, 0])
            self.play(Rotate(hand, angle=-TAU, about_point=cc, rate_func=linear), Transform(days, new), run_time=0.32)
        age = chip("postnatal day 28", GREY, size=32).move_to([4.2, -2.75, 0])
        self.at("postnatal day")
        self.play(FadeIn(age, shift=UP * 0.1), run_time=0.4)
        self.wait(0.5)
        self.finish()


# ---------------------------------------------------------------------------------------------
class S06Reveal(SpokenScene):
    def construct(self):
        d = Diag(shut=True)
        sc = Scale()
        age = chip("postnatal day 28", GREY, size=32).move_to([4.2, -2.75, 0])
        mk = carry_state(self, d, sc, 0.5, "0.50")
        cc, face, tks, hand = clock_parts()
        days = T("4 days", 38, TEXT, weight=BOLD).move_to([5.4, 3.0, 0])
        self.add(age, face, tks, hand, days)
        self.at("responses shift")
        self.play(Transform(d.line_c, d.line("c", width_of(12))), Transform(d.line_i, d.line("i", width_of(18))), run_time=0.9)
        self.at("toward the open eye")
        mk2 = sc.marker(-0.2, "−0.20")
        self.play(Transform(mk, mk2), run_time=1.3)
        cl = M("C = 12", 30, BLUE).move_to(d.mid("c") + UP * 0.8 + RIGHT * 0.25)
        il = M("I = 18", 30, ORANGE).move_to(d.mid("i") + DOWN * 0.8 + RIGHT * 0.25)
        ill = T("illustrative cell", 26, GREY).move_to([-0.4, -1.65, 0])
        sub = M("(12 − 18) / (12 + 18) = −0.20", 30, TEXT).move_to([1.6, -3.45, 0])
        self.at("example")
        self.play(FadeIn(cl), FadeIn(il), FadeIn(ill), FadeOut(VGroup(face, tks, hand, days)), run_time=0.6)
        self.play(FadeIn(sub), run_time=0.4)
        self.at("below zero")
        zero = Line([sc.x(0), sc.y - 0.3, 0], [sc.x(0), sc.y + 0.25, 0], color=TEXT, stroke_width=3)
        self.play(Create(zero), Indicate(mk, color=TEXT, scale_factor=1.15), run_time=0.8)
        self.wait(1.0)
        self.finish()


# ---------------------------------------------------------------------------------------------
class S08Young(SpokenScene):
    def construct(self):
        d = Diag()
        self.add(*d.base(), *d.labels())
        young = chip("young mice", TEXT, size=34).move_to([1.2, 3.4, 0])
        self.at("in young mice")
        self.play(FadeIn(young), run_time=0.5)
        X0 = 4.3
        # closed-eye readout (blue), open-eye readout (orange)
        lc = T("closed eye", 32, BLUE, weight=BOLD).move_to([X0, 2.75, 0])
        nc = M("30", 64, BLUE, weight=BOLD).move_to([X0, 1.75, 0])
        lo = T("open eye", 32, ORANGE, weight=BOLD).move_to([X0, -0.45, 0])
        no = M("10", 64, ORANGE, weight=BOLD).move_to([X0, -1.45, 0])
        self.at("most of that")
        self.play(FadeIn(lc), FadeIn(nc), FadeIn(lo), FadeIn(no), run_time=0.6)
        self.at("the closed")
        shut = eye_shut(BLUE).scale(1.5).move_to(d.ec)
        self.play(ReplacementTransform(d.eye_c, shut), run_time=0.5)
        nc2 = M("30 → 12", 64, BLUE, weight=BOLD).move_to([X0, 1.75, 0])
        no2 = M("10 → 18", 64, ORANGE, weight=BOLD).move_to([X0, -1.45, 0])
        dc = VGroup(M("−18", 48, BLUE, weight=BOLD), T("big drop", 32, BLUE)).arrange(RIGHT, buff=0.3).move_to([X0, 0.7, 0])
        do = VGroup(M("+8", 48, ORANGE, weight=BOLD), T("small rise", 32, ORANGE)).arrange(RIGHT, buff=0.3).move_to([X0, -2.5, 0])
        self.at("responses")
        self.play(Transform(d.line_c, d.line("c", width_of(12))), Transform(d.line_i, d.line("i", width_of(18))),
                  ReplacementTransform(nc, nc2), ReplacementTransform(no, no2), FadeIn(dc), FadeIn(do), run_time=0.7)
        self.at("weakening")
        self.play(Indicate(dc, color=BLUE, scale_factor=1.12), run_time=0.7)
        self.wait(1.2)
        self.finish()


# ---------------------------------------------------------------------------------------------
class S09Pred(SpokenScene):
    def construct(self):
        p = build_predict(shut=False)
        d, sc = p["diag"], p["sc"]
        self.add(*d.base(), *d.labels(), sc.frame, p["mk"])
        self.play(FadeIn(p["head"], shift=DOWN * 0.1), run_time=0.5)
        self.at("do the same thing")
        shut = eye_shut(BLUE).scale(1.5).move_to(d.ec)
        self.play(ReplacementTransform(d.eye_c, shut), FadeIn(p["note"]), run_time=0.7)
        self.at("two month")
        self.play(FadeIn(p["age"], shift=LEFT * 0.1), run_time=0.5)
        self.at("what happens to the score")
        self.play(FadeIn(p["q"], scale=0.7), Indicate(p["mk"], color=TEAL, scale_factor=1.2), run_time=0.8)
        self.finish()


class S10Pause(NarratedScene):
    """The question held still for five seconds, with a countdown."""

    def construct(self):
        p = build_predict(shut=True)
        d, sc = p["diag"], p["sc"]
        self.add(*d.base(), *d.labels(), sc.frame, p["mk"], p["head"], p["age"], p["note"], p["q"])
        tr = ValueTracker(1.0)
        cc = np.array([2.2, -2.55, 0])
        ring_bg = Circle(radius=0.55, stroke_color=GREY, stroke_width=5, fill_opacity=0).move_to(cc).set_stroke(opacity=0.5)
        ring = always_redraw(lambda: Arc(radius=0.55, start_angle=PI / 2, angle=max(0.001, tr.get_value()) * TAU, arc_center=cc, color=TEAL, stroke_width=8))
        num = always_redraw(lambda: M(str(max(1, int(np.ceil(tr.get_value() * 5 - 1e-6)))), 36, TEAL, weight=BOLD).move_to(cc))
        cue = T("pause the video", 30, TEAL).move_to([4.9, -3.35, 0])
        self.add(ring_bg, ring, num)
        self.play(FadeIn(cue), run_time=0.4)
        self.play(tr.animate.set_value(0.0), run_time=4.6, rate_func=linear)


# ---------------------------------------------------------------------------------------------
class S11Reveal(SpokenScene):
    def construct(self):
        p = build_predict(shut=True)
        d, sc = p["diag"], p["sc"]
        mk = p["mk"]
        self.add(*d.base(), *d.labels(), sc.frame, mk, p["head"], p["age"], p["note"], p["q"])
        self.at("much less")
        ghost = sc.marker(-0.2, "young", color=GREY)
        ghost[1].become(T("young", 26, GREY).move_to(ghost[1]))
        ghost[0].set_fill(opacity=0.0).set_stroke(color=GREY, width=3, opacity=1)
        arr_young = DashedLine([sc.x(0.5), sc.y + 0.3, 0], [sc.x(-0.2), sc.y + 0.3, 0], color=GREY, stroke_width=3)
        arr_adult = Arrow([sc.x(0.5), sc.y + 0.85, 0], [sc.x(0.5) - 0.7, sc.y + 0.85, 0], buff=0, color=TEXT, stroke_width=6, tip_length=0.22)
        ml = T("much smaller shift", 34, TEXT, weight=BOLD).move_to([4.3, -2.55, 0])
        ml2 = T("arrow size is illustrative", 26, GREY).move_to([4.3, -3.35, 0])
        self.play(ReplacementTransform(p["q"], ml), FadeOut(p["note"]), FadeIn(ghost), Create(arr_young), run_time=0.6)
        self.play(GrowArrow(arr_adult), mk[0].animate.shift(LEFT * 0.7), FadeOut(mk[1]), FadeIn(ml2), run_time=0.6)
        self.at("in mice", lead=0.0)
        allm = VGroup(*d.base(), *d.labels(), sc.frame, mk, p["head"], p["age"], ml, ml2, ghost, arr_young, arr_adult)
        self.play(FadeOut(allm), run_time=0.3)
        sp = shift_plot()
        self.play(FadeIn(sp["ax"]), FadeIn(sp["small"]), FadeIn(sp["large"]), FadeIn(sp["sch"]), run_time=0.3)
        self.at("the shift is")
        self.play(Create(sp["cur"]), run_time=1.1, rate_func=linear)
        self.at("postnatal day")
        self.play(FadeIn(sp["pk"], scale=0.6), FadeIn(sp["pl"]), run_time=0.5)
        self.wait(1.0)
        self.finish()


# ---------------------------------------------------------------------------------------------
class S12Edges(SpokenScene):
    def construct(self):
        sp = shift_plot(with_band=True)
        self.add(sp["ax"], sp["cur"], sp["pk"], sp["pl"], sp["small"], sp["large"], sp["sch"])
        ms1 = T("much smaller", 30, TEXT).move_to([X(8.5), 0.4, 0])
        ms2 = T("much smaller", 30, TEXT).move_to([X(46), 0.4, 0])
        a1 = Arrow(ms1.get_bottom() + DOWN * 0.05, [X(8.5), Ys(8.5) + 0.35, 0], buff=0, color=TEXT, stroke_width=4, tip_length=0.2)
        a2 = Arrow(ms2.get_bottom() + DOWN * 0.05, [X(46), Ys(46) + 0.35, 0], buff=0, color=TEXT, stroke_width=4, tip_length=0.2)
        self.at("before about")
        self.play(FadeIn(ms1), GrowArrow(a1), Create(sp["l19"]), FadeIn(sp["t19"]), FadeIn(sp["cr"]), run_time=0.7)
        self.at("or after")
        self.play(FadeIn(ms2), GrowArrow(a2), Create(sp["l32"]), FadeIn(sp["t32"]), run_time=0.7)
        self.at("day 32")
        self.play(FadeIn(sp["band"]), run_time=0.9)
        self.wait(1.0)
        self.finish()


# ---------------------------------------------------------------------------------------------
class S13Q2(SpokenScene):
    def construct(self):
        sp = shift_plot(with_band=True)
        self.add(sp["ax"], sp["cur"], sp["pk"], sp["pl"], sp["small"], sp["large"], sp["sch"], sp["band"], sp["l19"], sp["l32"], sp["t19"], sp["t32"], sp["cr"])
        self.at("the window lies")
        wl = T("window", 32, SAND, weight=BOLD).move_to([X(25.5), -1.75, 0])
        by = 2.35
        x0, x1 = X(19), X(32)
        br = VGroup(Line([x0, by, 0], [x1, by, 0], color=SAND, stroke_width=4), Line([x0, by, 0], [x0, by - 0.15, 0], color=SAND, stroke_width=4),
                    Line([x1, by, 0], [x1, by - 0.15, 0], color=SAND, stroke_width=4))
        self.play(FadeIn(wl), FadeOut(sp["pl"]), Create(br), run_time=0.8)
        self.at("is that age itself")
        c1 = chip("age itself?", GREY, size=30).move_to([-2.1, 3.05, 0])
        self.play(FadeOut(sp["ax"].yl), FadeIn(c1, shift=DOWN * 0.1), run_time=0.45)
        self.at("or something")
        c2 = chip("something age brings?", GREY, size=30).move_to([1.85, 3.05, 0])
        self.play(FadeIn(c2, shift=DOWN * 0.1), run_time=0.45)
        self.wait(1.0)
        self.finish()


# ---------------------------------------------------------------------------------------------
class S14Idea(SpokenScene):
    def construct(self):
        head = T("The idea to carry through", 30, TEAL, weight=BOLD).move_to([0, 3.5, 0])
        l1 = T("The window follows", 46, TEXT, font=TITLE_FONT).move_to([0, 2.65, 0])
        l2 = T("the inhibitory cells,", 46, YELLOW, font=TITLE_FONT).move_to([0, 1.8, 0])
        l3 = T("not the calendar.", 46, GREY, font=TITLE_FONT).move_to([0, 0.95, 0])
        # the object the sentence is about: the window band
        wb = RoundedRectangle(corner_radius=0.2, width=3.3, height=2.1, stroke_color=SAND, stroke_width=4, fill_color=SAND, fill_opacity=0.32)
        wt = T("the window", 34, SAND, weight=BOLD).move_to(wb)
        win = VGroup(wb, wt)
        win.scale(1.4).move_to([0, 0.0, 0])
        cell, soma, tgt = basket_icon(1.0, origin=(0, 0), scale=1.2)
        cell.move_to([-4.5, -1.75, 0])
        cl = T("inhibitory cells", 30, YELLOW).move_to([-4.5, -3.45, 0])
        cal = calendar_icon().scale(1.25).move_to([5.3, -1.75, 0])
        cll = T("the calendar", 30, GREY).move_to([5.3, -3.45, 0])
        self.play(FadeIn(head, shift=DOWN * 0.1), FadeIn(win), run_time=0.6)
        self.at("the window follows")
        self.play(FadeIn(l1, shift=UP * 0.1), win.animate.scale(1 / 1.4).move_to([0.3, -1.75, 0]), run_time=0.7)
        self.at("inhibitory cells")
        ar1 = Arrow(cell.get_right() + RIGHT * 0.1, win.get_left() + LEFT * 0.08, buff=0.0, color=YELLOW, stroke_width=7, tip_length=0.3)
        self.play(FadeIn(l2, shift=UP * 0.1), FadeIn(cell), FadeIn(cl), run_time=0.6)
        self.play(GrowArrow(ar1), run_time=0.5)
        self.at("not the calendar")
        ar2 = DashedLine(cal.get_left() + LEFT * 0.15, win.get_right() + RIGHT * 0.1, color=GREY, stroke_width=6)
        mid = ar2.get_center()
        xx = VGroup(Line(mid + UL * 0.4, mid + DR * 0.4, color=RED, stroke_width=8), Line(mid + UR * 0.4, mid + DL * 0.4, color=RED, stroke_width=8))
        self.play(FadeIn(l3, shift=UP * 0.1), FadeIn(cal), FadeIn(cll), run_time=0.6)
        self.play(Create(ar2), run_time=0.4)
        self.play(Create(xx), run_time=0.4)
        self.wait(1.0)
        self.finish()


# ---------------------------------------------------------------------------------------------
def inhib_axes():
    return axes_plot("inhibition", YELLOW, ticks=(0, 60))


def thr_parts():
    thr = DashedLine([X(0), YT, 0], [6.4, YT, 0], color=TEXT, stroke_width=3)
    thl = T("threshold", 26, TEXT).move_to([5.4, YT + 0.4, 0])
    return thr, thl


ICON_ORIGIN = (3.25, -0.95)
ICON_SCALE = 0.70


class S15Open(SpokenScene):
    def construct(self):
        ax = inhib_axes()
        thr, thl = thr_parts()
        wm = chip("working model", GREY, size=28).move_to([4.5, 3.35, 0])
        cur = inhib_curve()
        icon0, _, _ = basket_icon(0.0, ICON_ORIGIN, ICON_SCALE)
        pv = T("parvalbumin basket cell\non a pyramidal cell", 26, YELLOW, line_spacing=0.8).move_to([ICON_ORIGIN[0] + 1.2, -2.0, 0])
        self.play(FadeIn(wm), FadeIn(ax), FadeIn(icon0), run_time=0.5)
        holder = VGroup(icon0)

        def grow(m, a):
            g, _, _ = basket_icon(inhib_f(60 * a), ICON_ORIGIN, ICON_SCALE)
            m.become(g)

        self.play(Create(cur), UpdateFromAlphaFunc(icon0, grow), run_time=3.2, rate_func=linear)
        self.at("parvalbumin basket")
        self.play(FadeIn(pv), run_time=0.4)
        self.at("opens the window")
        self.play(Create(thr), FadeIn(thl), run_time=0.6)
        self.at("passes a threshold")
        dot = Dot([X(PC), YT, 0], radius=0.15, color=TEXT)
        edge = DashedLine([X(PC), Y0, 0], [X(PC), BTOP, 0], color=SAND, stroke_width=4)
        t19 = T("~P19", 26, SAND, weight=BOLD).move_to([X(PC), Y0 - 0.5, 0])
        b = open_band()
        wl = T("window", 32, SAND, weight=BOLD).move_to([X(25.5), -1.65, 0])
        self.play(FadeIn(dot, scale=0.5), Create(edge), FadeIn(t19), run_time=0.4)
        self.play(GrowFromEdge(b, LEFT), FadeIn(wl), run_time=1.0)
        self.wait(0.8)
        self.finish()


class S16Close(SpokenScene):
    def construct(self):
        ax = inhib_axes()
        thr, thl = thr_parts()
        wm = chip("working model", GREY, size=28).move_to([4.5, 3.35, 0])
        cur = inhib_curve()
        cell, soma, tgt = basket_icon(1.0, ICON_ORIGIN, ICON_SCALE)
        pv = T("parvalbumin basket cell\non a pyramidal cell", 26, YELLOW, line_spacing=0.8).move_to([ICON_ORIGIN[0] + 1.2, -2.0, 0])
        edge = DashedLine([X(PC), Y0, 0], [X(PC), BTOP, 0], color=SAND, stroke_width=4)
        t19 = T("~P19", 26, SAND, weight=BOLD).move_to([X(PC), Y0 - 0.5, 0])
        b = open_band()
        wl = T("window", 32, SAND, weight=BOLD).move_to([X(25.5), -1.65, 0])
        self.add(ax, cur, thr, thl, wm, cell, pv, edge, t19, b, wl)
        ride = Dot([X(PC), Yi(PC), 0], radius=0.14, color=TEXT)
        self.add(ride)
        self.at("keeps maturing")
        self.play(MoveAlongPath(ride, inhib_curve(PC, 44), rate_func=linear), run_time=1.3)
        self.play(FadeOut(ride), run_time=0.2)
        self.at("build up around")
        net = brake_net(soma.get_center(), 0.5, 0.7)
        bl = T("brakes", 30, RED, weight=BOLD).move_to([soma.get_center()[0], -2.0, 0])
        nb = closed_band()
        e32 = DashedLine([X(32), Y0, 0], [X(32), BTOP, 0], color=RED, stroke_width=4)
        wl2 = T("window\ncloses", 28, SAND, weight=BOLD, line_spacing=0.8).move_to([X(25.5), -1.55, 0])
        close_link = Arrow(net.get_left(), [X(32), -0.95, 0], buff=0.12,
                           color=RED, stroke_width=4, tip_length=0.2)
        close_day = T("~P32", 26, RED, weight=BOLD).move_to([X(32), Y0 - 0.5, 0])
        self.play(Create(net), FadeIn(bl), FadeOut(pv), run_time=1.0)
        self.play(Transform(b, nb), run_time=0.9)
        self.at("it closes")
        self.play(Create(e32), GrowArrow(close_link), FadeIn(close_day),
                  FadeOut(wl), FadeIn(wl2), run_time=0.5)
        self.wait(2.2)
        self.finish()


# ---------------------------------------------------------------------------------------------
class S17Trigger(SpokenScene):
    def construct(self):
        ax = inhib_axes()
        thr, thl = thr_parts()
        young = chip("young cortex", GREY, size=30).move_to([-0.6, 3.35, 0])
        A, SD, PB = 0.95, 1.8, 11.0

        def g(p):
            f = inhib_f(p)
            return f + A * (1 - f) * np.exp(-((p - PB) / SD) ** 2 / 2)

        def Yg(p):
            return Y0 + IH * g(p)

        # crossing of the threshold on the way up
        pcs = np.linspace(2, PB, 4000)
        pcross = float(pcs[np.argmax(np.array([g(p) for p in pcs]) > 0.6)])
        seg1 = curve_fn(Yg, 0, pcross - 0.5)
        seg2 = curve_fn(Yg, pcross - 0.5, pcross + 0.5)
        seg3 = curve_fn(Yg, pcross + 0.5, 17.0)
        seg4 = curve_fn(Yg, 17.0, 60)
        xc = X(pcross)
        # the switch, right next to the crossing
        swc = [xc - 0.95, YT + 0.55, 0]
        sw_body = RoundedRectangle(corner_radius=0.25, width=1.1, height=0.5, stroke_color=GREY, stroke_width=4, fill_color=GREY, fill_opacity=0.2)
        knob = Circle(radius=0.19, stroke_width=0, fill_color=GREY, fill_opacity=1).move_to(sw_body.get_center() + LEFT * 0.28)
        sw = VGroup(sw_body, knob).move_to(swc)
        sw_lab = T("off", 28, GREY).move_to([swc[0], swc[1] + 0.6, 0])
        bl = T("brief boost", 30, YELLOW, weight=BOLD).move_to([X(1.0), 2.5, 0], aligned_edge=LEFT)
        ba = Arrow(bl.get_right() + RIGHT * 0.05, [X(PB), Yg(PB), 0], buff=0.05, color=YELLOW, stroke_width=4, tip_length=0.2)
        self.play(FadeIn(young), FadeIn(ax), Create(thr), FadeIn(thl), FadeIn(sw), FadeIn(sw_lab), Create(seg1), run_time=1.5, rate_func=linear)
        self.at("a brief boost")
        self.play(FadeIn(bl), GrowArrow(ba), run_time=0.7)
        self.at("enough to start")
        dot = Dot([xc, YT, 0], radius=0.15, color=TEXT)
        self.play(Create(seg2), run_time=0.5, rate_func=linear)
        on = RoundedRectangle(corner_radius=0.25, width=1.1, height=0.5, stroke_color=SAND, stroke_width=4, fill_color=SAND, fill_opacity=0.5).move_to(sw_body)
        kn2 = Circle(radius=0.19, stroke_width=0, fill_color=SAND, fill_opacity=1).move_to(sw_body.get_center() + RIGHT * 0.28)
        band_ = open_band(pcross, top=BTOP)
        edge = DashedLine([xc, Y0, 0], [xc, BTOP, 0], color=SAND, stroke_width=4)
        wl = T("window", 32, SAND, weight=BOLD).move_to([X(pcross + 9), -1.85, 0])
        on_lab = T("on", 28, SAND, weight=BOLD).move_to(sw_lab)
        self.play(FadeIn(dot, scale=0.5), Transform(sw_body, on), Transform(knob, kn2), Transform(sw_lab, on_lab), Create(edge), GrowFromEdge(band_, LEFT), FadeIn(wl), run_time=0.9)
        unknown = T("not tested: must it stay high?", 28, TEXT).move_to([0.7, 2.6, 0])
        self.play(Create(seg3), FadeIn(unknown), run_time=0.7, rate_func=linear)
        self.at("the boost did not")
        lab = T("closed later by further\nmaturation and brakes", 28, SAND, line_spacing=0.8).move_to([3.5, -1.3, 0])
        fade_arrow = Arrow(lab.get_top() + UP * 0.08, [X(36), -0.45, 0], buff=0.05, color=SAND, stroke_width=4, tip_length=0.2)
        self.play(Create(seg4), run_time=1.3, rate_func=linear)
        self.play(FadeIn(lab), GrowArrow(fade_arrow), run_time=0.6)
        self.wait(1.5)
        self.finish()


# ---------------------------------------------------------------------------------------------
class S18Scope(SpokenScene):
    def construct(self):
        def row(y, tag, color):
            card = RoundedRectangle(corner_radius=0.2, width=12.4, height=2.0, stroke_color=color, stroke_width=3, fill_color=color, fill_opacity=0.07).move_to([0, y, 0])
            t = T(tag, 34, color, weight=BOLD)
            t.move_to([card.get_left()[0] + 0.45 + t.width / 2, y, 0])
            return card, t

        c1, t1 = row(2.35, "The rule covers", GREEN)
        c2, t2 = row(0.0, "Adults", YELLOW)
        c3, t3 = row(-2.35, "It does not cover", GREY)
        for c_, t_ in ((c2, t2), (c3, t3)):
            c_.set_stroke(opacity=0.35)
            c_.set_fill(opacity=0.03)
            t_.set_opacity(0.35)
        self.play(FadeIn(c1), FadeIn(t1), FadeIn(c2), FadeIn(t2), FadeIn(c3), FadeIn(t3), run_time=0.6)
        x1 = c1.get_left()[0] + 0.45 + t1.width + 0.5
        mouse = chip("mouse", BLUE, size=32).move_to([0, 2.35, 0])
        rat = chip("rat", BLUE, size=32).move_to([0, 2.35, 0])
        mouse.move_to([x1 + mouse.width / 2, 2.35, 0])
        rat.move_to([x1 + mouse.width + 0.25 + rat.width / 2, 2.35, 0])
        vc = T("visual cortex,\nthe young shift", 30, TEXT, line_spacing=0.8)
        vc.move_to([x1 + mouse.width + 0.25 + rat.width + 0.5 + vc.width / 2, 2.35, 0])
        self.at("mouse and rat")
        self.play(FadeIn(mouse), FadeIn(rat), run_time=0.5)
        self.at("visual cortex")
        self.play(FadeIn(vc), run_time=0.5)
        self.at("adults keep")
        self.play(c2.animate.set_stroke(opacity=1).set_fill(opacity=0.07), t2.animate.set_opacity(1), run_time=0.5)
        ad = T("keep a weaker, different form", 34, TEXT)
        ad.move_to([c2.get_left()[0] + 0.45 + t2.width + 0.5 + ad.width / 2, 0.0, 0])
        self.at("weaker")
        self.play(FadeIn(ad), run_time=0.5)
        self.at("does not cover")
        x0 = c3.get_left()[0] + 0.45 + t3.width + 0.5
        ppl = chip("people", GREY, size=34)
        sl = chip("song and language", GREY, size=34)
        ppl.move_to([x0 + ppl.width / 2, -2.35, 0])
        sl.move_to([x0 + ppl.width + 0.3 + sl.width / 2, -2.35, 0])
        self.play(c3.animate.set_stroke(opacity=1).set_fill(opacity=0.07),
                  t3.animate.set_opacity(1), FadeIn(ppl), FadeIn(sl), run_time=0.4)
        self.wait(2.2)
        self.finish()


# ---------------------------------------------------------------------------------------------
class S20Take(SpokenScene):
    def construct(self):
        head = T("Takeaway", 32, GOLD, weight=BOLD).move_to([0, 3.45, 0])
        l1 = T("The window is set by", 48, TEXT, font=TITLE_FONT).move_to([0, 2.5, 0])
        l2 = T("the state of a circuit,", 48, YELLOW, font=TITLE_FONT).move_to([0, 1.6, 0])
        l3 = T("not simply by age.", 48, GREY, font=TITLE_FONT).move_to([0, 0.7, 0])
        circ = circuit_icon().scale(1.6).move_to([-3.2, -1.7, 0])
        cl = T("state of a circuit", 28, YELLOW).move_to([-3.2, -3.4, 0])
        yl = T("inhibitory cell", 26, YELLOW).move_to([-3.2, -0.15, 0])
        cal = calendar_icon().scale(1.3).move_to([3.2, -1.7, 0])
        cll = T("age", 28, GREY).move_to([3.2, -3.4, 0])
        circ_f = circ.copy().set_opacity(0.35)
        cal_f = cal.copy().set_opacity(0.35)
        self.add(circ_f, cal_f)
        self.play(FadeIn(head, shift=DOWN * 0.1), run_time=0.4)
        self.at("the window is set")
        self.play(FadeIn(l1, shift=UP * 0.1), run_time=0.5)
        self.at("state of a circuit")
        self.play(FadeIn(l2, shift=UP * 0.1), FadeOut(circ_f), FadeIn(circ), FadeIn(cl), FadeIn(yl), run_time=0.6)
        self.at("not simply")
        self.play(FadeIn(l3, shift=UP * 0.1), FadeOut(cal_f), FadeIn(cal), FadeIn(cll), run_time=0.6)
        self.wait(1.0)
        self.finish()


class S21End(EndCard):
    LINE = "The window is set by circuit state, not simply by age."
