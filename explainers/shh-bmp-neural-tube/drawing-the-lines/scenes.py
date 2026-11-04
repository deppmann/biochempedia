"""Chapter 5 of 6: Drawing the Lines  (Ventral to Dorsal: Sonic Hedgehog and BMP in the Neural Tube)

Timed to the SPOKEN words: every self.at("...") cue waits for that phrase in audio/words.json.

COLOR MAP (one color per concept, the whole chapter series; same as chapters 1 and 3)
  YELLOW = Sonic hedgehog (Shh) and the slope of signal it makes; a drug that activates Smoothened
  DORSAL = BMP and the dorsal tissues that send it: the second, opposing slope (blue-violet)
  TEAL   = notochord and floor plate (the Shh source tissue)
  BLUE   = class I factors (Pax6, Irx3) and the dorsal side of a border
  ORANGE = class II factors (Nkx2.2), the p3 domain and V3 neurons; also the generic "output" of the
           simple blur model (a ventral gene turned on by high signal)
  GREEN  = Olig2, the pMN domain and motor neurons (and, in the electroporation scene only, the DNA glow)
  RED    = repression (the T-bars) and nothing else
  GREY   = tube wall, neutral cells, axes, landscape;  TEXT (white) = the cell of interest, borders, highlights
  GOLD   = title rule and the "box 4" frame
Map geometry: the transverse tube map is the one from chapter 1 (centred at x=0, dorsal up).
"""
import numpy as np
from bp_style import *  # noqa: F401,F403

ORANGE = "#F29E4C"
PURPLE = "#B58CD9"
DORSAL = "#7D8BFF"
LIGHT_TEAL = "#A6E6EA"
LESSON = "Ventral to Dorsal: Sonic Hedgehog and BMP in the Neural Tube"


# ----------------------------------------------------------------------------- small helpers
def arr(a, b, color=GREY, w=5, tip=0.22):
    return Arrow(a, b, buff=0.0, color=color, stroke_width=w, tip_length=tip,
                 max_tip_length_to_length_ratio=0.5, max_stroke_width_to_length_ratio=14)


def inhib(a, b, color=RED, w=5, bar_w=0.22):
    a, b = np.array(a, float), np.array(b, float)
    d = (b - a) / np.linalg.norm(b - a)
    b = b - d * 0.04
    perp = np.array([-d[1], d[0], 0])
    return VGroup(Line(a, b, color=color, stroke_width=w), Line(b + perp * bar_w, b - perp * bar_w, color=color, stroke_width=w + 1))


def mix(c1, c2, t):
    return interpolate_color(ManimColor(c1), ManimColor(c2), float(np.clip(t, 0, 1)))


def lab(s, x, y, color=TEXT, size=24, anchor="c", **kw):
    t = T(s, size, color, **kw).move_to([x, y, 0])
    if anchor == "l":
        t.shift(RIGHT * (x - t.get_left()[0]))
    elif anchor == "r":
        t.shift(RIGHT * (x - t.get_right()[0]))
    return t


def bar(x, y, w, h, color, o=0.55, sw=3):
    return RoundedRectangle(corner_radius=0.07, width=w, height=h, stroke_color=color, stroke_width=sw,
                            fill_color=color, fill_opacity=o).move_to([x, y, 0])


def cellr(x, y, color=GREY, o=0.18, w=1.0, h=0.4, sw=2):
    return RoundedRectangle(corner_radius=0.07, width=w, height=h, stroke_color=color, stroke_width=sw,
                            fill_color=color, fill_opacity=o).move_to([x, y, 0])



LG = "#C3C9D4"      # light grey for small labels (readable on the dark ground)


def ldr(p, q, color=GREY, w=2.5):
    """A thin leader line from a label to the thing it names."""
    return Line([p[0], p[1], 0], [q[0], q[1], 0], color=color, stroke_width=w)


# ----------------------------------------------------------------------------- the column of cells (blur model)
NC, CH = 28, 0.22          # 28 cells, 0.22 tall; cell 0 is nearest the source
I0 = 13.5                  # the half-maximal position (between cells 13 and 14)


def cy(i):
    return -NC * CH / 2 + CH / 2 + i * CH


def resp(i, n):
    """Output of a cell at position i for an illustrative Hill model: lambda 20 um, cells 5 um -> c = exp(-i/4)."""
    return 1.0 / (1.0 + np.exp(n * (i - I0) / 4.0))


def make_cells(x, w=1.1):
    return VGroup(*[RoundedRectangle(corner_radius=0.04, width=w, height=CH - 0.02, stroke_color=GREY, stroke_width=1.5,
                                     fill_color=GREY, fill_opacity=0.15).move_to([x, cy(i), 0]) for i in range(NC)])


def style_out(cells, n):
    for i, c in enumerate(cells):
        r = resp(i, n)
        c.set_fill(ORANGE, 0.06 + 0.84 * r).set_stroke(mix(GREY, ORANGE, r), 1.5)


def strip_slope(x, w=0.4):
    return VGroup(*[Rectangle(width=w, height=CH, stroke_width=0, fill_color=YELLOW,
                              fill_opacity=0.06 + 0.9 * np.exp(-i / 4.0)).move_to([x, cy(i), 0]) for i in range(NC)])


# column layout shared by scenes 4, 5 and 5b: signal strip | cells | bracket and its label | output curve
STRIPX, COLX, BRX, CX0, CSC = -5.6, -4.5, -3.78, -1.3, 2.7


def curve_pts(n):
    ii = np.linspace(-0.5, NC - 0.5, 90)
    return [np.array([CX0 + CSC * resp(i, n), cy(i), 0]) for i in ii]


def make_curve(n):
    m = VMobject(stroke_color=ORANGE, stroke_width=6, fill_opacity=0)
    m.set_points_smoothly(curve_pts(n))
    return m


def curve_axis():
    return Line([CX0, cy(-0.5), 0], [CX0, cy(NC - 0.5), 0], color=GREY, stroke_width=2)


def out_scale():
    """Horizontal scale of the output curve: 0 to max."""
    y = cy(-0.5) - 0.14
    return VGroup(Line([CX0, y, 0], [CX0 + CSC, y, 0], color=GREY, stroke_width=2),
                  lab("0", CX0, y - 0.3, LG, 26), lab("max", CX0 + CSC, y - 0.3, LG, 26),
                  lab("output", CX0 + CSC / 2, y - 0.3, ORANGE, 26))


def pos_label():
    """Names the vertical axis of the output curve."""
    return lab("position", CX0 + 0.15, 3.5, LG, 26, "l")


def bracket(n, x=None, tick=0.17):
    """Bracket on the cell wall for the 10 to 90% width: 18/n cells, centred on the half-maximal cell."""
    x = BRX if x is None else x
    d = 9.0 / n
    y0, y1 = cy(I0 - d), cy(I0 + d)
    return VGroup(Line([x, y0, 0], [x, y1, 0], color=TEXT, stroke_width=4),
                  Line([x - tick, y0, 0], [x, y0, 0], color=TEXT, stroke_width=4),
                  Line([x - tick, y1, 0], [x, y1, 0], color=TEXT, stroke_width=4))


def bk_label(n, x=None, size=34):
    s = "18" if n < 1.5 else "9" if n < 3 else "4" if n < 6 else "2"
    x = BRX + 0.3 if x is None else x
    return lab(f"about\n{s} cells", x, 0.0, TEXT, size, "l", line_spacing=0.9, weight=BOLD)


# ----------------------------------------------------------------------------- the transverse neural tube map (chapter 1)
ROW_YS = [-1.50 + 0.44 * i for i in range(9)]
FLOOR_Y, ROOF_Y, EPI_Y, NOTO_Y = -1.88, 2.43, 3.15, -3.0
TWD = 2.0                                                  # half width of the tube wall
STRIPE_COL = [(ORANGE, 0.55), (GREEN, 0.55), (BLUE, 0.34), (BLUE, 0.2), (BLUE, 0.34)]


BK, BOFF = 1.25, -0.425          # the enlarged map: y' = BK * y + BOFF (about 72% of the frame height for the tube wall)


def TY(y, big=False):
    return BK * y + BOFF if big else y


def tube_map(x=0.0, stripes=True, big=False):
    K = BK if big else 1.0
    Y = lambda y: TY(y, big)
    sh = RoundedRectangle(corner_radius=0.9 * K, width=2 * TWD * K, height=4.6 * K, stroke_color=GREY, stroke_width=5,
                          fill_color=GREY, fill_opacity=0.06).move_to([0, Y(0.3), 0])
    can = RoundedRectangle(corner_radius=0.12, width=0.3, height=3.9 * K, stroke_color=GREY, stroke_width=1.5,
                           fill_color=BG, fill_opacity=0.9).move_to([0, Y(0.3), 0])
    w = VGroup(*[VGroup(cellr(-0.98 * K, Y(y), w=1.6 * K, h=0.4 * K), cellr(0.98 * K, Y(y), w=1.6 * K, h=0.4 * K)) for y in ROW_YS])
    if stripes:
        for r, (col, o) in enumerate(STRIPE_COL):
            for c in w[r]:
                c.set_stroke(col, 3).set_fill(col, o)
    if big:
        no = Circle(radius=0.3, stroke_color=TEAL, stroke_width=3, fill_color=TEAL, fill_opacity=0.4).move_to([0, -3.42, 0])
        ep = bar(0, 3.32, 5.2, 0.2, DORSAL, 0.55)
    else:
        no = Circle(radius=0.36, stroke_color=TEAL, stroke_width=3, fill_color=TEAL, fill_opacity=0.4).move_to([0, NOTO_Y, 0])
        ep = bar(0, EPI_Y, 4.4, 0.2, DORSAL, 0.55)
    fl = bar(0, Y(FLOOR_Y), 2.0 * K, 0.24, TEAL, 0.6)
    rf = bar(0, Y(ROOF_Y), 2.0 * K, 0.24, DORSAL, 0.6)
    g = VGroup(sh, can, w, no, ep, fl, rf)
    g.shift(RIGHT * x)
    return g


def _tl(txt, y, side, color, tx, target, size=26, weight=NORMAL):
    t = lab(txt, tx, y, color, size, "r" if side == "l" else "l", weight=weight)
    sx = t.get_right()[0] + 0.1 if side == "l" else t.get_left()[0] - 0.1
    return VGroup(t, ldr([sx, y], [target, y], color, 2.5))


def tube_labels(x=0.0, side_epi="r", size=26, with_vz=True, big=False):
    """The six labels of the map, as separate groups so they can arrive one at a time."""
    K = BK if big else 1.0
    Y = lambda y: TY(y, big)
    ey = 3.32 if big else EPI_Y
    ny = -3.42 if big else NOTO_Y
    ew = 2.6 if big else 2.25
    out = [
        _tl("roof plate", Y(ROOF_Y), "l", DORSAL, x - TWD * K - 0.5, x - 1.05 * K, size),
        _tl("epidermis", ey, side_epi, DORSAL, (x + TWD * K + 0.6) if side_epi == "r" else (x - TWD * K - 0.5),
            (x + ew) if side_epi == "r" else (x - ew), size),
        _tl("floor plate", Y(FLOOR_Y), "l", TEAL, x - TWD * K - 0.5, x - 1.05 * K, size),
        _tl("notochord", ny, "l", TEAL, x - TWD * K - 0.5, x - (0.32 if big else 0.42), size),
    ]
    if with_vz:
        out.append(_tl("ventricular zone", Y(1.75), "r", LG, x + TWD * K + 0.5, x + 1.8 * K, size))
    return out


def dv_axis(x=6.0):
    up = arr([x, 0.35, 0], [x, 2.3, 0], LG, 4, 0.2)
    dn = arr([x, 0.15, 0], [x, -1.8, 0], LG, 4, 0.2)
    return VGroup(up, dn, lab("dorsal", x, 2.65, LG, 26), lab("ventral", x, -2.15, LG, 26))


def border_y(r):
    """y of the border between stripe row r and row r+1 on the full map."""
    return (ROW_YS[r] + ROW_YS[r + 1]) / 2


# ----------------------------------------------------------------------------- zoomed ventral half of the tube (scenes 11 to 14)
VXC = -1.6
VY = [-1.8 + 0.9 * k for k in range(5)]
VROW = [(ORANGE, 0.5), (GREEN, 0.5), (BLUE, 0.28), (BLUE, 0.2), (BLUE, 0.28)]
LM_X = VXC - 2.0        # right edge of left-margin labels
RM_X = 0.55             # left edge of right-margin labels
VFL_Y, VNO_Y = -2.64, -3.35


def vcell(x, y, col, o):
    return RoundedRectangle(corner_radius=0.07, width=1.5, height=0.8, stroke_color=col, stroke_width=2.5,
                            fill_color=col, fill_opacity=o).move_to([x, y, 0])


def vzoom():
    cells = [[vcell(VXC - 0.82, VY[k], VROW[k][0], VROW[k][1]), vcell(VXC + 0.82, VY[k], VROW[k][0], VROW[k][1])]
             for k in range(5)]
    can = Rectangle(width=0.1, height=4.6, stroke_width=0, fill_color=GREY, fill_opacity=0.5).move_to([VXC, 0.0, 0])
    shell = RoundedRectangle(corner_radius=0.3, width=3.7, height=4.9, stroke_color=GREY, stroke_width=3,
                             fill_opacity=0).move_to([VXC, 0.05, 0])
    fl = bar(VXC, VFL_Y, 3.5, 0.3, TEAL, 0.6)
    no = Circle(radius=0.38, stroke_color=TEAL, stroke_width=3, fill_color=TEAL, fill_opacity=0.4).move_to([VXC, VNO_Y, 0])
    return cells, VGroup(shell, can, fl, no, *[c for row in cells for c in row]), fl, no


def vlabels():
    fp = VGroup(lab("floor plate", VXC - 2.25, VFL_Y, TEAL, 26, "r"), ldr([VXC - 2.15, VFL_Y], [VXC - 1.78, VFL_Y], TEAL))
    nc = VGroup(lab("notochord", VXC - 2.25, VNO_Y, TEAL, 26, "r"), ldr([VXC - 2.15, VNO_Y], [VXC - 0.42, VNO_Y], TEAL))
    return VGroup(fp, nc)


def pmn_halo(cells):
    h = SurroundingRectangle(cells[1][1], color=ORANGE, buff=0.07, stroke_width=7)
    h.set_fill(ORANGE, 0.18)
    return h


def neuron_c(x, y, flip, color, s=1.2):
    soma = Circle(radius=0.15 * s, stroke_width=0, fill_color=color, fill_opacity=0.95).move_to([x, y, 0])
    ax = Line([x, y, 0], [x + 0.5 * s * flip, y, 0], color=color, stroke_width=4)
    d1 = Line([x, y, 0], [x - 0.28 * s * flip, y + 0.24 * s, 0], color=color, stroke_width=4)
    d2 = Line([x, y, 0], [x - 0.28 * s * flip, y - 0.24 * s, 0], color=color, stroke_width=4)
    return VGroup(ax, d1, d2, soma)


LCELL, RCELL = VXC - 0.82, VXC + 0.82


# ----------------------------------------------------------------------------- the landscape and the A/B circuit (scenes 15 to 18, 21)
LX = 3.7
CHY = 1.95


def land_y(x, k=1.0):
    def V(v):
        return v ** 4 - 2 * k * v ** 2
    vmin = -k * k if k > 0 else 0.0
    edge = V(1.5) - vmin
    return -2.65 + 3.1 * (V(x) - vmin) / edge


def land_pts(k=1.0):
    xs = np.linspace(-1.5, 1.5, 100)
    return [np.array([LX * x, land_y(x, k), 0]) for x in xs]


def land_curve(k=1.0):
    m = VMobject(stroke_color=GREY, stroke_width=7, fill_opacity=0)
    m.set_points_smoothly(land_pts(k))
    return m


def land_fill(k=1.0):
    pts = land_pts(k)
    return Polygon(*(pts + [np.array([LX * 1.5, -3.0, 0]), np.array([-LX * 1.5, -3.0, 0])]),
                   stroke_width=0, fill_color=GREY, fill_opacity=0.10)


def ball_at(x, k=1.0):
    return np.array([LX * x, land_y(x, k) + 0.22, 0])


def make_ball():
    return Circle(radius=0.22, stroke_color=TEXT, stroke_width=3, fill_color=TEXT, fill_opacity=0.9)


def ab_chips():
    ca = chip("factor A", BLUE, 32).move_to([-4.9, CHY, 0])
    cb = chip("factor B", ORANGE, 32).move_to([4.9, CHY, 0])
    return ca, cb


def _carc(p0, p1, color, w, bar_w):
    arc = ArcBetweenPoints(np.array(p0, float), np.array(p1, float), angle=-0.8, color=color, stroke_width=w)
    t = arc.point_from_proportion(1.0) - arc.point_from_proportion(0.97)
    t = t / np.linalg.norm(t)
    end = arc.get_end()
    perp = np.array([-t[1], t[0], 0])
    return VGroup(arc, Line(end + perp * bar_w, end - perp * bar_w, color=color, stroke_width=w + 1))


def ab_arrows(w=8):
    """Two curved blunt arrows, one over and one under, each from one chip to the other."""
    bw = 0.1 + 0.02 * w
    return VGroup(_carc([-3.75, CHY + 0.25, 0], [3.7, CHY + 0.25, 0], RED, w, bw),
                  _carc([3.75, CHY - 0.25, 0], [-3.7, CHY - 0.25, 0], RED, w, bw))


def xmin(k):
    return float(np.sqrt(k)) if k > 0 else 0.0


# ============================================================================================
class S00Title(TitleCard):
    LESSON = LESSON
    TITLE = "Drawing the Lines"


# ============================================================================================
class S01Q(SpokenScene):
    def construct(self):
        N, H = 24, 0.26
        ys = [-N * H / 2 + H / 2 + i * H for i in range(N)]
        SX, WX = -2.2, 0.0
        strip = VGroup(*[Rectangle(width=1.2, height=H, stroke_width=0, fill_color=YELLOW,
                                   fill_opacity=0.08 + 0.85 * np.exp(-i / 6.0)).move_to([SX, ys[i], 0]) for i in range(N)])
        cells = VGroup(*[RoundedRectangle(corner_radius=0.04, width=2.6, height=H - 0.03, stroke_color=GREY, stroke_width=1.5,
                                          fill_color=GREY, fill_opacity=0.12).move_to([WX, ys[i], 0]) for i in range(N)])
        bands = [(0, 3, ORANGE), (4, 7, GREEN), (8, 11, BLUE), (12, 15, PURPLE), (16, 19, DORSAL), (20, 23, GREY)]

        def blur(i):
            t = min(i / 19.0, 1.0)
            return mix(ORANGE, TEXT, t), 0.62 - 0.32 * t

        def crisp(i):
            for a, b, col in bands:
                if a <= i <= b:
                    return col, 0.72
        for i, c in enumerate(cells):
            col, o = blur(i)
            c.set_stroke(col, 1.5).set_fill(col, o)
        l_s = lab("slope of signal", SX - 0.3, 3.5, YELLOW, 30)
        self.at("smooth slope")
        self.play(LaggedStart(*[FadeIn(r) for r in strip], lag_ratio=0.02), run_time=0.6)
        self.at("of signal")
        self.play(FadeIn(l_s), run_time=0.3)
        self.at("should give", lead=0.2)
        self.play(FadeIn(cells, lag_ratio=0.03), run_time=0.6)
        l_b = lab("blur", WX + 1.7, 0.0, TEXT, 48, "l", weight=BOLD)
        self.at("blur", lead=0.2)
        self.play(FadeIn(l_b, shift=RIGHT * 0.15), run_time=0.4)
        self.at("yet the domains")
        anims = []
        for i, c in enumerate(cells):
            col, o = crisp(i)
            anims.append(c.animate.set_stroke(col, 1.5).set_fill(col, o))
        l_d = lab("domains", WX + 0.9, 3.5, TEXT, 30)
        self.play(FadeOut(l_b), *anims, FadeIn(l_d), run_time=0.9)
        self.at("sharp borders")
        lines = VGroup(*[Line([WX - 1.5, (ys[b] + ys[b + 1]) / 2, 0], [WX + 1.5, (ys[b] + ys[b + 1]) / 2, 0], color=TEXT, stroke_width=4)
                         for b in (3, 7, 11, 15, 19)])
        self.play(LaggedStart(*[Create(l) for l in lines], lag_ratio=0.2), run_time=1.0)
        self.at("why")
        q = T("?", 100, TEXT, weight=BOLD).move_to([0.2, 0.0, 0])
        main = VGroup(strip, cells, l_s, l_d, lines)
        bx = RoundedRectangle(corner_radius=0.2, width=5.3, height=3.6, stroke_color=GOLD, stroke_width=5,
                              fill_color=GOLD, fill_opacity=0.12).move_to([4.2, 0, 0])
        num = T("4", 80, GOLD, weight=BOLD).move_to([2.2, 0.0, 0])
        txt = lab("How does a\nslope become\nlines?", 2.85, 0.0, TEXT, 34, "l", line_spacing=0.95)
        self.play(main.animate.shift(LEFT * 2.6), FadeIn(q, scale=0.6), FadeIn(bx), FadeIn(num), FadeIn(txt), run_time=0.8)
        self.finish()


# ============================================================================================
AX_C = [0.0, 0.4]


def resp_axes():
    return Axes(x_range=[-2.2, 2.2, 1], y_range=[0, 1.0, 0.5], x_length=11.0, y_length=5.4, tips=False,
                axis_config={"color": LG, "stroke_width": 3, "include_ticks": False},
                y_axis_config={"stroke_opacity": 0}).move_to([AX_C[0], AX_C[1], 0])


def left_axis(ax):
    return Line(ax.c2p(-2.2, 0), ax.c2p(-2.2, 1.0), color=LG, stroke_width=3)


def hill1(x):
    return 1 / (1 + 10 ** (-x))


def resp_labels(ax):
    xl = lab("log concentration", ax.c2p(2.2, 0)[0] + 0.3, ax.c2p(0, 0)[1] + 0.5, LG, 26, "r")
    yl = lab("output", ax.c2p(-2.2, 1.0)[0] + 0.15, 3.42, ORANGE, 28, "l")
    return xl, yl


class S02Blur(SpokenScene):
    def construct(self):
        ax = resp_axes()
        xl, yl = resp_labels(ax)
        la = left_axis(ax)
        curve = ax.plot(hill1, x_range=[-2.2, 2.2], color=ORANGE, stroke_width=8)
        xa = ax.c2p(-2.2, 0)[0] + 0.15
        l_h = lab("Hill coefficient 1:\ngraded", xa, 2.15, TEXT, 34, "l", line_spacing=0.95, weight=BOLD)
        l_def = lab("Hill coefficient: how steeply\noutput rises with concentration", ax.c2p(0.45, 0)[0], -0.3, LG, 26, "l",
                    line_spacing=0.95)
        self.add(ax, la, xl, yl)
        self.at("output simply rises", lead=0.35)
        self.play(Create(curve), run_time=1.9)
        self.at("the gentle curve")
        self.play(Indicate(curve, color=ORANGE, scale_factor=1.0), run_time=0.8)
        self.at("simple binding", lead=0.35)
        self.play(FadeIn(l_h, shift=RIGHT * 0.15), run_time=0.6)
        self.play(FadeIn(l_def, shift=UP * 0.1), run_time=0.6)
        self.finish()


def hbr(xa, xb, y, color=TEXT, tick=0.14, w=4):
    """A horizontal bracket below an axis, ticks pointing up at the thing measured."""
    return VGroup(Line([xa, y, 0], [xb, y, 0], color=color, stroke_width=w),
                  Line([xa, y, 0], [xa, y + tick, 0], color=color, stroke_width=w),
                  Line([xb, y, 0], [xb, y + tick, 0], color=color, stroke_width=w))


class S03Blur2(SpokenScene):
    def construct(self):
        ax = resp_axes()
        xl, yl = resp_labels(ax)
        curve = ax.plot(hill1, x_range=[-2.2, 2.2], color=ORANGE, stroke_width=8)
        self.add(ax, left_axis(ax), xl, yl, curve)
        x1, x2 = -np.log10(9), np.log10(9)

        def level(r, x, name):
            p_y = ax.c2p(-2.2, r)
            p_c = ax.c2p(x, r)
            p_x = ax.c2p(x, 0)
            h = DashedLine(p_y, p_c, color=TEXT, stroke_width=3)
            v = DashedLine(p_c, p_x, color=TEXT, stroke_width=3)
            d = Dot(p_x, radius=0.11, color=ORANGE)
            t = lab(name, p_y[0] - 0.12, p_y[1], TEXT, 26, "r")
            return h, v, d, t
        h1, v1, d1, t1 = level(0.1, x1, "10%")
        h2, v2, d2, t2 = level(0.9, x2, "90%")
        h5, v5, d5, t5 = level(0.5, 0.0, "50%")
        self.at("from 10")
        self.play(FadeIn(t1), Create(h1), run_time=0.3)
        self.play(Create(v1), FadeIn(d1), run_time=0.3)
        self.at("to 90")
        self.play(FadeIn(t2), Create(h2), run_time=0.4)
        self.play(Create(v2), FadeIn(d2), run_time=0.4)
        self.at("output then")
        self.play(FadeIn(t5), Create(h5), run_time=0.3)
        self.play(Create(v5), FadeIn(d5), run_time=0.3)
        yb = ax.c2p(0, 0)[1] - 0.38
        xs = [ax.c2p(x1, 0)[0], ax.c2p(0, 0)[0], ax.c2p(x2, 0)[0]]
        b9a, b9b = hbr(xs[0], xs[1], yb), hbr(xs[1], xs[2], yb)
        n9a = lab("9×", (xs[0] + xs[1]) / 2, yb - 0.3, TEXT, 28, weight=BOLD)
        n9b = lab("9×", (xs[1] + xs[2]) / 2, yb - 0.3, TEXT, 28, weight=BOLD)
        self.play(Create(b9a), FadeIn(n9a), run_time=0.45)
        self.play(Create(b9b), FadeIn(n9b), run_time=0.45)
        self.at("81 fold")
        yb2 = yb - 0.78
        b81 = hbr(xs[0], xs[2], yb2, GOLD, 0.16, 5)
        n81 = lab("9 × 9 = 81-fold", xs[2] + 0.2, yb2 - 0.02, GOLD, 34, "l", weight=BOLD)
        self.play(Create(b81), FadeIn(n81, shift=LEFT * 0.15), run_time=0.8)
        self.at("in concentration")
        self.play(Indicate(n81, color=GOLD, scale_factor=1.08), run_time=0.7)
        self.finish()


# ============================================================================================
class S04Blur3(SpokenScene):
    def construct(self):
        strip = strip_slope(STRIPX)
        cells = make_cells(COLX)
        l_sig = lab("signal", STRIPX, 3.5, YELLOW, 26)
        l_out = pos_label()
        self.play(LaggedStart(*[FadeIn(r) for r in strip], lag_ratio=0.02), FadeIn(cells), FadeIn(l_sig), run_time=0.45)
        self.at("illustrative slope")
        l_par = lab("illustrative slope:\ndecay length 20 µm,\ncells 5 µm wide", 2.0, -1.9, LG, 26, "l", line_spacing=0.95)
        self.play(FadeIn(l_par, shift=LEFT * 0.15), run_time=0.6)
        self.at("that change", lead=0.7)
        ca, cv, sc = curve_axis(), make_curve(1), out_scale()
        self.play(FadeIn(ca), FadeIn(sc), FadeIn(l_out), run_time=0.4)
        anims = []
        for i, c in enumerate(cells):
            r = resp(i, 1)
            anims.append(c.animate.set_fill(ORANGE, 0.06 + 0.84 * r).set_stroke(mix(GREY, ORANGE, r), 1.5))
        cv.set_stroke(opacity=0)
        self.add(cv)
        full = make_curve(1)

        def draw(m, a):
            m.pointwise_become_partial(full, 0, max(a, 0.002))
            m.set_stroke(color=ORANGE, width=6, opacity=min(1.0, a * 6))
        self.play(UpdateFromAlphaFunc(cv, draw), *anims, run_time=0.9, rate_func=linear)
        self.at("about 18 cells")
        br = bracket(1)
        l18 = bk_label(1)
        self.play(Create(br), FadeIn(l18, shift=LEFT * 0.15), run_time=0.8)
        self.at("18 cells of")
        self.play(Indicate(l18, color=TEXT, scale_factor=1.08), run_time=0.7)
        self.at("in between answers")
        mid = VGroup(*[cells[i] for i in range(5, 22)])
        self.play(Indicate(mid, color=TEXT, scale_factor=1.12), run_time=1.0)
        self.at("is a blur")
        l_bl = lab("a blur", 2.0, 0.6, ORANGE, 52, "l", weight=BOLD)
        self.play(FadeIn(l_bl, shift=UP * 0.15), run_time=0.5)
        self.finish()


class S05Steep(SpokenScene):
    def construct(self):
        nt = ValueTracker(1)
        strip = strip_slope(STRIPX)
        cells = make_cells(COLX)
        for i, c in enumerate(cells):
            c.add_updater(lambda m, i=i: m.set_fill(ORANGE, 0.06 + 0.84 * resp(i, nt.get_value()))
                          .set_stroke(mix(GREY, ORANGE, resp(i, nt.get_value())), 1.5))
        ca = curve_axis()
        cv = make_curve(1)
        cv.add_updater(lambda m: m.set_points_smoothly(curve_pts(nt.get_value())))
        br = bracket(1)
        br.add_updater(lambda m: m.become(bracket(nt.get_value())))
        bl = bk_label(1)
        bl.add_updater(lambda m: m.become(bk_label(nt.get_value())))
        l_sig = lab("signal", STRIPX, 3.5, YELLOW, 26)
        l_out = pos_label()
        self.add(strip, cells, ca, cv, br, bl, l_sig, l_out, out_scale())
        TX, VX = 2.0, 3.55
        title = lab("10 to 90% expression width,\nillustrative Hill model", TX, 2.35, TEXT, 26, "l", line_spacing=0.95)
        rule = Line([TX, 1.65, 0], [6.75, 1.65, 0], color=GREY, stroke_width=2)
        rows = []
        for j, (n, w) in enumerate([(1, "about 18 cells"), (2, "about 9 cells"), (4, "about 4 cells"), (8, "about 2 cells")]):
            y = 1.05 - 0.85 * j
            rows.append(VGroup(lab(f"Hill {n}", TX, y, TEXT, 30, "l", weight=BOLD), lab(w, VX, y, TEXT, 30, "l")))
        self.at("this simple model")
        self.play(FadeIn(title), Create(rule), FadeIn(rows[0], shift=LEFT * 0.15), run_time=0.7)
        self.at("a steeper")
        self.play(FadeIn(rows[1], shift=LEFT * 0.15), nt.animate.set_value(2), run_time=0.8)
        self.at("switch like response")
        self.play(FadeIn(rows[2], shift=LEFT * 0.15), nt.animate.set_value(4), run_time=0.8)
        self.at("narrows the blur")
        self.play(FadeIn(rows[3], shift=LEFT * 0.15), nt.animate.set_value(8), run_time=1.0)
        self.at("one or two cells")
        hl = SurroundingRectangle(rows[3], color=TEXT, buff=0.14, stroke_width=4)
        self.play(Create(hl), run_time=0.5)
        self.finish()


class S05bCells(SpokenScene):
    def construct(self):
        H1X, H8X = -2.0, 3.0
        strip = strip_slope(STRIPX)
        cells8 = make_cells(COLX)
        style_out(cells8, 8)
        ca, cv, br, bl, sc = curve_axis(), make_curve(8), bracket(8), bk_label(8), out_scale()
        self.add(strip, cells8, ca, cv, br, bl, sc)
        cells1 = make_cells(H1X)
        style_out(cells1, 1)
        l1 = lab("Hill 1", H1X, 3.42, TEXT, 28, weight=BOLD)
        l8 = lab("Hill 8", H8X, 3.42, TEXT, 28, weight=BOLD)
        self.play(FadeOut(strip), FadeOut(ca), FadeOut(cv), FadeOut(br), FadeOut(bl), FadeOut(sc),
                  cells8.animate.shift(RIGHT * (H8X - COLX)), FadeIn(cells1), FadeIn(l1), FadeIn(l8), run_time=0.6)
        ax_x = H1X - 1.35
        full = DoubleArrow([ax_x, cy(-0.5), 0], [ax_x, cy(NC - 0.5), 0], color=TEXT, stroke_width=4, tip_length=0.2, buff=0)
        l_all = lab("every cell\nstill here", ax_x - 0.3, 0.0, TEXT, 34, "r", line_spacing=0.95)
        self.at("all still there", lead=0.0)
        self.play(GrowFromCenter(full), FadeIn(l_all, shift=RIGHT * 0.15), run_time=0.8)
        self.at("fewer of them", lead=0.3)
        b1 = bracket(1, x=H1X + 0.8)
        t1 = lab("about 18 cells\nin between", H1X + 1.05, 0.0, TEXT, 28, "l", line_spacing=0.95)
        self.play(Create(b1), FadeIn(t1, shift=LEFT * 0.15), run_time=0.7)
        ring = SurroundingRectangle(VGroup(cells8[13], cells8[14]), color=TEXT, buff=0.05, stroke_width=5)
        t8 = lab("about 2 cells\nin between", H8X + 0.95, 0.0, TEXT, 28, "l", line_spacing=0.95)
        ld8 = ldr([H8X + 0.6, 0.0], [H8X + 0.9, 0.0], TEXT, 3)
        self.play(Create(ring), FadeIn(t8, shift=LEFT * 0.15), Create(ld8), run_time=0.7)
        self.finish()


# ============================================================================================
COLB = -3.4
PX, LEND = 1.6, 4.2


def zone_cells(x, zones):
    """zones: list of (first_cell, last_cell, color, opacity)."""
    cs = make_cells(x)
    for a, b, col, o in zones:
        for i in range(a, b + 1):
            cs[i].set_stroke(col, 1.5).set_fill(col, o)
    return cs


TWO = [(0, 13, ORANGE, 0.6), (14, 27, BLUE, 0.6)]
THREE = [(0, 8, ORANGE, 0.6), (9, 17, GREEN, 0.6), (18, 27, BLUE, 0.6)]


def retint(cells, zones):
    out = []
    for a, b, col, o in zones:
        for i in range(a, b + 1):
            out.append(cells[i].animate.set_stroke(col, 1.5).set_fill(col, o))
    return out


def pair_arrows(yc, up, down, x0=PX, dx=0.5, gap=0.1, w=8):
    """Two blunt arrows between chips `up` (above) and `down` (below): each starts at one chip's edge and ends just short of the other."""
    ytop = up.get_bottom()[1] - gap
    ybot = down.get_top()[1] + gap
    a1 = inhib([x0 - dx, ytop, 0], [x0 - dx, ybot + 0.06, 0], RED, w)
    a2 = inhib([x0 + dx, ybot, 0], [x0 + dx, ytop - 0.06, 0], RED, w)
    return a1, a2


class S06Where(SpokenScene):
    def construct(self):
        H1X, H8X = -2.0, 3.0
        cells = make_cells(H8X)
        style_out(cells, 8)
        cells1 = make_cells(H1X)
        style_out(cells1, 1)
        l1 = lab("Hill 1", H1X, 3.42, TEXT, 28, weight=BOLD)
        l8 = lab("Hill 8", H8X, 3.42, TEXT, 28, weight=BOLD)
        ax_x = H1X - 1.35
        full = DoubleArrow([ax_x, cy(-0.5), 0], [ax_x, cy(NC - 0.5), 0], color=TEXT, stroke_width=4, tip_length=0.2, buff=0)
        l_all = lab("every cell\nstill here", ax_x - 0.3, 0.0, TEXT, 34, "r", line_spacing=0.95)
        b1 = bracket(1, x=H1X + 0.8)
        t1 = lab("about 18 cells\nin between", H1X + 1.05, 0.0, TEXT, 28, "l", line_spacing=0.95)
        ring = SurroundingRectangle(VGroup(cells[13], cells[14]), color=TEXT, buff=0.05, stroke_width=5)
        t8 = lab("about 2 cells\nin between", H8X + 0.95, 0.0, TEXT, 28, "l", line_spacing=0.95)
        ld8 = ldr([H8X + 0.6, 0.0], [H8X + 0.9, 0.0], TEXT, 3)
        self.add(cells, cells1, l1, l8, full, l_all, b1, t1, ring, t8, ld8)
        self.play(FadeOut(VGroup(cells1, l1, l8, full, l_all, b1, t1, ring, t8, ld8)),
                  cells.animate.shift(RIGHT * (COLB - H8X)), run_time=0.5)
        self.play(*retint(cells, TWO), run_time=0.5)
        self.at("their switch")
        line = Line([COLB + 0.65, 0, 0], [0.7, 0, 0], color=TEXT, stroke_width=4)
        l_b = lab("border", -1.0, 0.3, TEXT, 30)
        self.play(Create(line), FadeIn(l_b, shift=UP * 0.1), run_time=0.7)
        self.at("the factors themselves")
        ca = chip("factor A", BLUE, 44).move_to([PX, 1.6, 0])
        cb = chip("factor B", ORANGE, 44).move_to([PX, -1.6, 0])
        self.play(FadeIn(ca, scale=0.8, shift=DOWN * 0.2), FadeIn(cb, scale=0.8, shift=UP * 0.2), run_time=0.8)
        self.at("either side")
        self.play(Indicate(ca, color=BLUE, scale_factor=1.08), Indicate(cb, color=ORANGE, scale_factor=1.08), run_time=0.7)
        self.at("repress each other", lead=0.25)
        a1, a2 = pair_arrows(0, ca, cb)
        self.play(GrowFromPoint(a1, a1.get_top()), GrowFromPoint(a2, a2.get_bottom()), run_time=0.8)
        self.finish()


# ============================================================================================
class S07Electro(SpokenScene):
    def construct(self):
        tm = tube_map(0.0, stripes=False, big=True)
        w = tm[2]
        labs = tube_labels(0.0, big=True)
        dv = dv_axis(6.4)
        Y = lambda y: TY(y, True)
        self.play(FadeIn(tm), run_time=0.2)
        self.play(LaggedStart(*[FadeIn(l) for l in labs], FadeIn(dv), lag_ratio=0.25), run_time=0.8)
        self.at("by electroporation")
        ey = Y(0.3)
        el = VGroup(RoundedRectangle(corner_radius=0.05, width=0.16, height=3.2, stroke_color=TEXT, stroke_width=3,
                                     fill_color=TEXT, fill_opacity=0.5).move_to([-6.2, ey, 0]),
                    RoundedRectangle(corner_radius=0.05, width=0.16, height=3.2, stroke_color=TEXT, stroke_width=3,
                                     fill_color=TEXT, fill_opacity=0.5).move_to([6.2, ey, 0]))
        l_e = VGroup(lab("electroporation", 3.45, -1.95, TEXT, 26, "l"), ldr([3.4, -1.85], [3.0, -1.5], TEXT, 2.5))
        self.play(el[0].animate.move_to([-2.85, ey, 0]), el[1].animate.move_to([2.85, ey, 0]), run_time=1.0)
        self.play(FadeIn(l_e), run_time=0.3)
        self.at("is pushed into cells")
        dots = VGroup(*[Dot([x, Y(y), 0], radius=0.11, color=GREEN) for x, y in
                        ((2.7, 0.95), (2.7, 0.3), (2.7, -0.35), (2.5, 0.65), (2.5, 0.0))])
        l_d = lab("DNA", 3.45, Y(0.35), GREEN, 32, "l", weight=BOLD)
        self.play(FadeOut(l_e), FadeIn(dots), FadeIn(l_d), run_time=0.4)
        self.play(*[d.animate.move_to([1.2 + 0.25 * ((j % 2) - 0.5), d.get_y(), 0]) for j, d in enumerate(dots)], run_time=1.0)
        self.at("on one side of the tube")
        right = [w[i][1] for i in range(9)]
        self.play(FadeOut(dots), *[c.animate.set_stroke(GREEN, 4).set_fill(GREEN, 0.55) for c in right], run_time=1.0)
        l_el = lab("electroporated\nside", 3.45, Y(-0.6), GREEN, 28, "l", line_spacing=0.95)
        self.play(FadeOut(l_d), FadeIn(l_el), run_time=0.5)
        self.at("the other side")
        l_c = lab("control side", -3.4, Y(0.35), TEXT, 30, "r")
        self.play(FadeIn(l_c, shift=RIGHT * 0.15), Indicate(VGroup(*[w[i][0] for i in range(9)]), color=TEXT, scale_factor=1.0),
                  run_time=0.8)
        self.finish()


# ============================================================================================
def pair_scene_chips(yc, top, bot, dy=1.55):
    ct = chip(top[0], top[1], 44).move_to([PX, yc + dy, 0])
    cb = chip(bot[0], bot[1], 44).move_to([PX, yc - dy, 0])
    return ct, cb


class S08Pair1(SpokenScene):
    def construct(self):
        cells = zone_cells(COLB, TWO)
        line = Line([COLB + 0.65, 0, 0], [0.7, 0, 0], color=TEXT, stroke_width=4)
        d1 = lab("Pax6 domain\n(includes pMN)", COLB - 0.7, 1.5, BLUE, 26, "r", line_spacing=0.95)
        d2 = lab("Nkx2.2 domain", COLB - 0.7, -1.5, ORANGE, 26, "r")
        self.add(cells, line, d1, d2)
        l_c = lab("Briscoe and colleagues", 0.0, 3.0, LG, 26, "l")
        self.at("james briscoe")
        self.play(FadeIn(l_c, shift=LEFT * 0.15), run_time=0.6)
        self.at("showed that", lead=-0.6)
        cp, cn = pair_scene_chips(0, ("Pax6", BLUE), ("Nkx2.2", ORANGE))
        self.play(FadeIn(cp, scale=0.8, shift=DOWN * 0.2), run_time=0.5)
        self.at("showed that", lead=-1.9)
        self.play(FadeIn(cn, scale=0.8, shift=UP * 0.2), run_time=0.5)
        self.at("repress each other", lead=0.2)
        a1, a2 = pair_arrows(0, cp, cn)
        self.play(GrowFromPoint(a1, a1.get_top()), GrowFromPoint(a2, a2.get_bottom()), run_time=0.6)
        self.finish()
        self.wait(0.8)


class S09Pair1b(SpokenScene):
    def construct(self):
        tm = tube_map(0.0, stripes=True, big=True)
        labs = tube_labels(0.0, big=True)
        dv = dv_axis(6.4)
        Y = lambda y: TY(y, True)
        self.add(tm)
        self.play(LaggedStart(*[FadeIn(l) for l in labs], FadeIn(dv), lag_ratio=0.2), run_time=0.9)
        yb = Y(border_y(0))
        hl = Line([-2.7, yb, 0], [2.7, yb, 0], color=TEXT, stroke_width=7)
        self.at("border", lead=-0.15)
        self.play(Create(hl), run_time=0.4)
        l_m = _tl("pMN", Y(ROW_YS[1]), "l", GREEN, -3.0, -2.3, 32, BOLD)
        self.at("pmn", lead=0.2)
        self.play(FadeIn(l_m, shift=RIGHT * 0.15), run_time=0.4)
        l_p = _tl("p3", Y(ROW_YS[0]), "r", ORANGE, 3.0, 2.3, 32, BOLD)
        self.at("p3", lead=0.2)
        self.play(FadeIn(l_p, shift=LEFT * 0.15), run_time=0.4)
        # the blue rows above are the Pax6 / Irx3 side of the border
        y0, y1 = Y(ROW_YS[2] - 0.2), Y(ROW_YS[4] + 0.2)
        br = VGroup(Line([2.75, y0, 0], [2.75, y1, 0], color=BLUE, stroke_width=4),
                    Line([2.75, y0, 0], [2.6, y0, 0], color=BLUE, stroke_width=4),
                    Line([2.75, y1, 0], [2.6, y1, 0], color=BLUE, stroke_width=4))
        l_pi = lab("Pax6 and Irx3\ndomains", 2.95, (y0 + y1) / 2, BLUE, 26, "l", line_spacing=0.95)
        self.play(Create(br), FadeIn(l_pi, shift=LEFT * 0.15), run_time=0.6)
        self.finish()


class S10Pair2(SpokenScene):
    def construct(self):
        cells = zone_cells(COLB, THREE)
        yb = (cy(17) + cy(18)) / 2
        line = Line([COLB + 0.65, yb, 0], [0.7, yb, 0], color=TEXT, stroke_width=4)
        d1 = lab("Irx3 domain", COLB - 0.7, yb + 1.5, BLUE, 26, "r")
        d2 = lab("Olig2 domain", COLB - 0.7, yb - 1.5, GREEN, 26, "r")
        self.add(cells, line, d1, d2)
        l_c = lab("Novitch, Chen and Jessell, 2001", 0.0, 3.2, LG, 26, "l")
        self.play(FadeIn(l_c, shift=LEFT * 0.15), run_time=0.6)
        self.at("found the same", lead=-0.2)
        ci, co = pair_scene_chips(yb, ("Irx3", BLUE), ("Olig2", GREEN), 1.2)
        self.play(FadeIn(ci, scale=0.8, shift=DOWN * 0.2), run_time=0.4)
        self.at("and olig2", lead=0.1)
        self.play(FadeIn(co, scale=0.8, shift=UP * 0.2), run_time=0.4)
        a1, a2 = pair_arrows(yb, ci, co)
        self.play(GrowFromPoint(a1, a1.get_top()), GrowFromPoint(a2, a2.get_bottom()), run_time=0.6)
        self.finish()
        self.wait(1.8)


# ============================================================================================
def predict_state():
    cells, zoom, fl, no = vzoom()
    h = pmn_halo(cells)
    lb = vlabels()
    l_ctl = lab("control side", LM_X, VY[4], LG, 26, "r")
    l_el = lab("electroporated side", RM_X, VY[4], TEXT, 26, "l")
    l_f = lab("Nkx2.2 forced on\nin pMN", RM_X, VY[1], ORANGE, 30, "l", weight=BOLD, line_spacing=0.95)
    l_m = lab("motor neuron\ndomain", LM_X, VY[1], GREEN, 26, "r", line_spacing=0.95)
    q = lab("What happens\nto those cells?", RM_X, 0.85, TEXT, 40, "l", font=TITLE_FONT, line_spacing=0.95)
    return dict(cells=cells, zoom=zoom, fl=fl, no=no, halo=h, lb=lb, l_ctl=l_ctl, l_el=l_el, l_f=l_f, l_m=l_m, q=q)


class S11Predict(SpokenScene):
    def construct(self):
        S = predict_state()
        tm = tube_map(0.0, stripes=True, big=True)
        labs = tube_labels(0.0, big=True)
        dv = dv_axis(6.4)
        self.add(tm, *labs, dv)
        self.play(FadeOut(tm), *[FadeOut(l) for l in labs], FadeOut(dv), FadeIn(S["zoom"]), FadeIn(S["lb"]), run_time=0.8)
        self.play(FadeIn(S["l_ctl"]), FadeIn(S["l_el"]), run_time=0.4)
        self.at("force", lead=0.3)
        self.play(FadeIn(S["halo"]), FadeIn(S["l_f"], shift=LEFT * 0.15), run_time=0.7)
        self.at("motor neuron domain")
        self.play(FadeIn(S["l_m"], shift=RIGHT * 0.15), Indicate(S["halo"], color=ORANGE, scale_factor=1.1), run_time=0.7)
        self.at("what happens")
        self.play(Write(S["q"]), run_time=0.8)
        self.at("those cells")
        self.play(Indicate(S["halo"], color=TEXT, scale_factor=1.15), run_time=0.8)
        self.finish()


class S12Pause(NarratedScene):
    def construct(self):
        S = predict_state()
        self.add(S["zoom"], S["lb"], S["halo"], S["l_ctl"], S["l_el"], S["l_f"], S["l_m"], S["q"])
        self.finish()


class S13Reveal(SpokenScene):
    def construct(self):
        S = predict_state()
        cells = S["cells"]
        self.add(S["zoom"], S["lb"], S["halo"], S["l_ctl"], S["l_el"], S["l_m"])
        yp = VY[1]
        nl = neuron_c(LCELL, yp, -1, GREEN)
        nr = neuron_c(RCELL, yp, 1, GREEN)
        l_mn = lab("motor neurons", RM_X, yp, GREEN, 30, "l", weight=BOLD)
        self.at("motor neurons")
        self.play(FadeIn(nl, scale=0.6), FadeIn(nr, scale=0.6), FadeIn(l_mn), run_time=0.8)
        self.at("suppressed")
        l_sp = lab("motor neurons\nsuppressed", RM_X, yp, TEXT, 30, "l", weight=BOLD, line_spacing=0.95)
        self.play(FadeOut(nr, scale=0.3), ReplacementTransform(l_mn, l_sp),
                  cells[1][1].animate.set_fill(GREY, 0.18).set_stroke(GREY, 2.5), run_time=0.9)
        self.at("the cells make", lead=0.1)
        vr = neuron_c(RCELL, yp, 1, ORANGE)
        l_v3 = lab("V3 neurons", RM_X, yp, ORANGE, 30, "l", weight=BOLD)
        self.play(FadeIn(vr, scale=0.6), ReplacementTransform(l_sp, l_v3),
                  cells[1][1].animate.set_fill(ORANGE, 0.5).set_stroke(ORANGE, 2.5), run_time=0.8)
        self.at("the fate of")
        l_p3 = lab("p3 domain", LM_X, VY[0], ORANGE, 26, "r", weight=BOLD)
        self.play(FadeIn(l_p3, shift=RIGHT * 0.15), run_time=0.5)
        self.at("the domain below")
        v0l = neuron_c(LCELL, VY[0], -1, ORANGE)
        v0r = neuron_c(RCELL, VY[0], 1, ORANGE)
        self.play(FadeIn(v0l, scale=0.6), FadeIn(v0r, scale=0.6), run_time=0.7)
        self.finish()


class S14Reveal2(SpokenScene):
    def construct(self):
        S = predict_state()
        cells = S["cells"]
        cells[1][1].set_fill(ORANGE, 0.5).set_stroke(ORANGE, 2.5)
        yp = VY[1]
        nl = neuron_c(LCELL, yp, -1, GREEN)
        vr = neuron_c(RCELL, yp, 1, ORANGE)
        v0l = neuron_c(LCELL, VY[0], -1, ORANGE)
        v0r = neuron_c(RCELL, VY[0], 1, ORANGE)
        l_p3 = lab("p3 domain", LM_X, VY[0], ORANGE, 26, "r", weight=BOLD)
        self.add(S["zoom"], S["lb"], S["l_ctl"], S["l_el"], S["l_m"], l_p3, nl, vr, v0l, v0r)
        yb0 = (VY[0] + VY[1]) / 2
        yb1 = (VY[1] + VY[2]) / 2
        bl = Line([VXC - 1.65, yb0, 0], [VXC - 0.05, yb0, 0], color=TEXT, stroke_width=8)
        br_ = Line([VXC + 0.05, yb0, 0], [VXC + 1.65, yb0, 0], color=TEXT, stroke_width=8)
        self.at("one factor")
        cn = chip("Nkx2.2", ORANGE, 34).move_to([RM_X + 0.95, 0.75, 0])
        self.play(FadeIn(cn, scale=0.8), run_time=0.5)
        self.at("in the wrong place")
        self.play(Create(bl), Create(br_), run_time=0.8)
        self.at("moved the line")
        ghost = DashedLine([VXC + 0.05, yb0, 0], [VXC + 1.65, yb0, 0], color=GREY, stroke_width=4)
        l_mv = lab("line moved\nup one row", RM_X + 0.35, (yb0 + yb1) / 2, TEXT, 28, "l", line_spacing=0.95)
        up = arr([RM_X + 0.12, yb0, 0], [RM_X + 0.12, yb1, 0], TEXT, 5, 0.2)
        self.add(ghost)
        self.play(br_.animate.move_to([VXC + 0.85, yb1, 0]), FadeIn(l_mv), GrowArrow(up), run_time=1.2)
        self.at("nothing was done", lead=0.3)
        eq1 = lab("=", VXC - 1.15, VFL_Y, TEXT, 30, weight=BOLD)
        eq2 = lab("=", VXC + 1.15, VFL_Y, TEXT, 30, weight=BOLD)
        l_s = lab("no imposed change\nto the Shh source", RM_X, -3.0, TEAL, 26, "l", line_spacing=0.95)
        ld1 = ldr([RM_X - 0.08, -2.82], [VXC + 1.8, VFL_Y], TEAL)
        ld2 = ldr([RM_X - 0.08, VNO_Y + 0.05], [VXC + 0.45, VNO_Y], TEAL)
        self.play(Indicate(S["fl"], color=TEAL, scale_factor=1.1), Indicate(S["no"], color=TEAL, scale_factor=1.2),
                  FadeIn(eq1), FadeIn(eq2), FadeIn(l_s, shift=LEFT * 0.15), Create(ld1), Create(ld2), run_time=1.0)
        self.finish()


# ============================================================================================
def top_label(s, color=RED, size=28):
    return lab(s, 0.0, 3.4, color, size)


class S15Switch(SpokenScene):
    def construct(self):
        ca, cb = ab_chips()
        curve, fill = land_curve(1.0), land_fill(1.0)
        self.add(fill, curve)
        self.at("two factors")
        self.play(FadeIn(ca, scale=0.8), FadeIn(cb, scale=0.8), run_time=0.5)
        self.at("repress each other", lead=0.3)
        ar = ab_arrows(8)
        self.play(Create(ar[0]), Create(ar[1]), run_time=0.7)
        l_sw = lab("bistable switch", 0.0, 0.3, GOLD, 40, weight=BOLD)
        self.at("can form a switch", lead=0.0)
        self.play(FadeIn(l_sw, scale=0.9), run_time=0.5)
        self.at("two stable states", lead=0.1)
        rings = VGroup(*[Circle(radius=0.34, stroke_color=TEXT, stroke_width=3).set_stroke(opacity=0.8).move_to(ball_at(x))
                         for x in (-1.0, 1.0)])
        l_ba = lab("A on, B off", -LX, -3.4, BLUE, 28)
        l_bb = lab("B on, A off", LX, -3.4, ORANGE, 28)
        xb = ValueTracker(-1.0)
        ball = make_ball()
        ball.add_updater(lambda m: m.move_to(ball_at(xb.get_value())))
        self.play(FadeIn(rings), FadeIn(l_ba), FadeIn(l_bb), FadeIn(ball, scale=0.6), run_time=0.6)
        self.play(Indicate(l_ba, color=BLUE, scale_factor=1.12), run_time=0.5)
        self.play(xb.animate.set_value(1.0), run_time=1.0, rate_func=smooth)
        self.play(Indicate(l_bb, color=ORANGE, scale_factor=1.12), run_time=0.5)
        self.finish()


class S16Switch2(SpokenScene):
    def construct(self):
        kt = ValueTracker(1.0)
        ca, cb = ab_chips()
        ar = ab_arrows(9)
        curve = land_curve(1.0)
        curve.add_updater(lambda m: m.set_points_smoothly(land_pts(kt.get_value())))
        fill = land_fill(1.0)
        fill.add_updater(lambda m: m.become(land_fill(kt.get_value())))
        ball = make_ball().move_to(ball_at(1.0))
        ball.add_updater(lambda m: m.move_to(ball_at(xmin(kt.get_value()), kt.get_value())))
        l_sw = lab("bistable switch", 0.0, 0.3, GOLD, 40, weight=BOLD)
        self.add(ca, cb, ar, fill, curve, ball, l_sw)
        self.at("only when")
        l_st = top_label("strong, cooperative repression")
        self.play(FadeIn(l_st, shift=DOWN * 0.1), Indicate(ar, color=RED, scale_factor=1.0), run_time=0.8)
        self.at("a weak loop", lead=0.1)
        weak = ab_arrows(2.5)
        l_wk = top_label("weak repression")
        self.play(Transform(ar, weak), ReplacementTransform(l_st, l_wk), FadeOut(l_sw), run_time=0.6)
        self.play(kt.animate.set_value(-0.6), run_time=1.0)
        l_no = lab("weak loop: one state, no switch", 0.0, 0.3, GOLD, 38, weight=BOLD)
        self.play(FadeIn(l_no, scale=0.9), run_time=0.4)
        self.finish()


class S17Switch3(SpokenScene):
    def construct(self):
        ca, cb = ab_chips()
        ar = ab_arrows(9)
        curve, fill = land_curve(1.0), land_fill(1.0)
        xb = ValueTracker(0.0)
        ball = make_ball()
        ball.add_updater(lambda m: m.move_to(ball_at(xb.get_value())))
        l_c = lab("cell near a border", 0.0, 0.3, TEXT, 30)
        l_top = top_label("strong cross-repression")
        self.add(ca, cb, ar, fill, curve, ball, l_c)
        self.play(FadeIn(l_top, shift=DOWN * 0.1), run_time=0.5)
        t_fall = self.t_of("it falls")
        self.at("cannot hold both factors")
        amp, sgn = 0.03, 1
        while self.elapsed() < t_fall - 0.6:
            self.play(xb.animate.set_value(sgn * amp), run_time=0.3, rate_func=smooth)
            sgn *= -1
            amp = min(amp + 0.02, 0.13)
        self.at("it falls")
        self.play(FadeOut(l_c), xb.animate.set_value(1.0), run_time=1.0, rate_func=rush_into)
        self.play(xb.animate.set_value(1.1), run_time=0.25)
        self.play(xb.animate.set_value(1.0), run_time=0.25)
        self.at("and the loop")
        self.play(Indicate(ar, color=RED, scale_factor=1.0), run_time=0.5)
        self.at("helps hold it there")
        ring = Circle(radius=0.38, stroke_color=TEXT, stroke_width=5).move_to(ball_at(1.0))
        l_h = lab("held in place", LX, -3.4, TEXT, 28)
        self.play(Create(ring), FadeIn(l_h), run_time=0.7)
        self.finish()


# ============================================================================================
EMB = "#9CA5B5"


def embryo(cx, cy_, s=1.0, rot=0.0):
    """A cartoon embryo: a curled body that tapers to a tail, a rounded head, and a row of small bumps. Not anatomical."""
    R = 1.0 * s
    n = 60
    ths = np.linspace(np.radians(70), np.radians(330), n)
    wd = (0.55 * (1 - np.linspace(0, 1, n)) ** 0.8 + 0.07) * s
    outer = [np.array([(R + wd[i]) * np.cos(ths[i]), (R + wd[i]) * np.sin(ths[i]), 0]) for i in range(n)]
    inner = [np.array([(R - wd[i]) * np.cos(ths[i]), (R - wd[i]) * np.sin(ths[i]), 0]) for i in range(n)]
    body = Polygon(*(outer + inner[::-1]), stroke_color=EMB, stroke_width=3, fill_color=EMB, fill_opacity=1)
    hp = outer[0] * 0.5 + inner[0] * 0.5
    head = Circle(radius=0.62 * s, stroke_color=EMB, stroke_width=3, fill_color=EMB, fill_opacity=1).move_to(hp + np.array([0.05, 0.05, 0]) * s)
    bumps = VGroup(*[Dot((np.array([R * np.cos(ths[k]), R * np.sin(ths[k]), 0])), radius=0.07 * s, color=BG) for k in range(14, 46, 6)])
    g = VGroup(body, head, bumps)
    g.move_to([0, 0, 0]).rotate(rot).move_to([cx, cy_, 0])
    return g


class S18Memory(SpokenScene):
    def construct(self):
        curve, fill = land_curve(1.0), land_fill(1.0)
        ball = make_ball().move_to(ball_at(1.0))
        ca, cb = ab_chips()
        ar = ab_arrows(9)
        self.add(ca, cb, ar, fill, curve, ball)
        self.at("some memory")
        l_m = lab("memory", 0.0, 0.3, GOLD, 48, weight=BOLD)
        self.play(FadeIn(l_m, scale=0.9), Indicate(ball, color=TEXT, scale_factor=1.4), run_time=0.9)
        self.at("in 2012", lead=0.1)
        dish = Circle(radius=2.75, stroke_color=LG, stroke_width=6, fill_color=GREY, fill_opacity=0.08).move_to([0, -0.15, 0])
        cr = lab("Balaskas, Ribes, Briscoe and colleagues, 2012", 0.0, 3.35, LG, 28)
        self.play(*[FadeOut(m) for m in (ca, cb, ar, fill, curve, ball, l_m)], FadeIn(dish, scale=0.85), FadeIn(cr), run_time=0.8)
        e1, e2 = embryo(-0.7, 0.45, 0.78, 0.3), embryo(0.95, -0.85, 0.62, -2.6)
        l_e = lab("mouse embryos\nin culture", 3.3, 0.2, TEXT, 34, "l", line_spacing=0.95, weight=BOLD)
        ld = ldr([3.2, 0.15], [1.65, -0.55], TEXT, 3)
        self.at("2012", lead=-0.7)
        self.play(FadeIn(e1, scale=0.7), FadeIn(e2, scale=0.7), run_time=0.7)
        self.at("in mouse", lead=0.25)
        self.play(FadeIn(l_e, shift=LEFT * 0.15), Create(ld), run_time=0.6)
        self.finish()


# ============================================================================================
def stripes19(cx, b1, b2, ytop=1.5, ybot=-3.5, w=1.5, o=0.65):
    """Column of three stripes; b1, b2 are the border heights as fractions of the column."""
    H = ytop - ybot
    parts = [(0, b1, ORANGE), (b1, b2, GREEN), (b2, 1, BLUE)]
    g = VGroup()
    for a, b, col in parts:
        h = (b - a) * H
        g.add(Rectangle(width=w, height=h, stroke_width=0, fill_color=col, fill_opacity=o).move_to([cx, ybot + a * H + h / 2, 0]))
    return g


def normal_lines(cx, ytop=1.5, ybot=-3.5, w=1.5):
    H = ytop - ybot
    return VGroup(*[DashedLine([cx - w / 2 - 0.3, ybot + b * H, 0], [cx + w / 2 + 0.3, ybot + b * H, 0], color=TEXT, stroke_width=3.5)
                    for b in (0.3, 0.62)])


class S19Memory2(SpokenScene):
    def construct(self):
        CL, CR = -3.45, 3.45
        YAX = 2.35
        N1, N2 = (0.3, 0.62), (0.5, 0.82)

        def panel(cx, title):
            t = lab(title, cx, 3.4, TEXT, 30, weight=BOLD)
            ax = Arrow([cx - 2.9, YAX, 0], [cx + 2.55, YAX, 0], buff=0, color=LG, stroke_width=3, tip_length=0.2)
            tm = lab("time", cx + 2.55, YAX - 0.38, LG, 26, "r")
            return t, ax, tm
        tL, axL, tmL = panel(CL, "Short pulse")
        colx_l, colx_r = CL - 1.15, CR - 1.15
        colL = stripes19(colx_l, *N1)
        nlL = normal_lines(colx_l)
        self.play(FadeIn(tL), Create(axL), FadeIn(tmL), FadeIn(colL), Create(nlL), run_time=0.4)
        self.at("short pulse")
        spike = Rectangle(width=0.2, height=0.6, stroke_width=0, fill_color=YELLOW, fill_opacity=0.95).move_to([CL - 2.2, YAX + 0.3, 0])
        self.play(GrowFromEdge(spike, DOWN), run_time=0.4)
        self.at("smoothened", lead=0.3)
        l_pa = lab("Smoothened agonist", CL - 2.3, YAX - 0.42, YELLOW, 26, "l")
        self.play(FadeIn(l_pa, shift=DOWN * 0.1), run_time=0.5)
        self.at("left the borders")
        l_na = lab("borders close\nto normal", CL - 0.1, -0.7, TEXT, 30, "l", line_spacing=0.95)
        l_dl = lab("dotted: normal\nborder positions", CL - 0.1, -2.1, LG, 26, "l", line_spacing=0.95)
        self.play(colL.animate.shift(UP * 0.05), run_time=0.2)
        self.play(colL.animate.shift(DOWN * 0.05), FadeIn(l_na, shift=LEFT * 0.15), FadeIn(l_dl), run_time=0.5)
        # right panel arrives after the first sentence and starts to run before the words, so the result can be held on screen
        self.at("close to normal", lead=-0.5)
        tR, axR, tmR = panel(CR, "Continuous")
        colR = stripes19(colx_r, *N1)
        nlR = normal_lines(colx_r)
        self.play(FadeIn(tR), Create(axR), FadeIn(tmR), FadeIn(colR), Create(nlR), run_time=0.5)
        barb = Rectangle(width=4.2, height=0.45, stroke_width=0, fill_color=YELLOW, fill_opacity=0.95).move_to([CR - 2.3 + 2.1, YAX + 0.225, 0])
        l_pb = lab("Smoothened agonist", CR - 2.3, YAX - 0.42, YELLOW, 26, "l")
        self.play(GrowFromEdge(barb, LEFT), FadeIn(l_pb, shift=DOWN * 0.1), run_time=0.8)
        colR2 = stripes19(colx_r, *N2)
        l_nb = lab("borders\nshifted", CR - 0.1, -0.7, TEXT, 30, "l", line_spacing=0.95)
        self.play(Transform(colR, colR2), FadeIn(l_nb, shift=LEFT * 0.15), run_time=0.8)
        self.finish()


# ============================================================================================
class S20Limit(SpokenScene):
    def construct(self):
        card = RoundedRectangle(corner_radius=0.25, width=11.4, height=5.0, stroke_color=GOLD, stroke_width=4,
                                fill_color=GOLD, fill_opacity=0.06).move_to([0, 0, 0])
        self.at("there is a limit")
        l_l = lab("A LIMIT", 0.0, 1.7, GOLD, 40, weight=BOLD)
        self.play(FadeIn(card), FadeIn(l_l, scale=0.9), run_time=0.7)
        self.at("sharp is not")
        c1 = chip("sharp", ORANGE, 60, 0.3)
        ne = T("≠", 90, TEXT, weight=BOLD)
        c2 = chip("accurate", GREEN, 60, 0.3)
        row = VGroup(c1, ne, c2).arrange(RIGHT, buff=0.5).move_to([0, -0.4, 0])
        self.play(FadeIn(c1, scale=0.85), run_time=0.5)
        self.at("the same as")
        self.play(FadeIn(ne, scale=0.6), run_time=0.4)
        self.at("accurate")
        self.play(FadeIn(c2, scale=0.85), run_time=0.5)
        self.finish()


class S21Limit2(SpokenScene):
    def construct(self):
        ca, cb = ab_chips()
        ar = ab_arrows(9)
        curve, fill = land_curve(1.0), land_fill(1.0)
        xb = ValueTracker(-1.0)
        ball = make_ball()
        ball.add_updater(lambda m: m.move_to(ball_at(xb.get_value())))
        l_ok = lab("correct side", -LX, -3.4, TEXT, 36)
        self.add(ca, cb, ar, fill, curve, ball, l_ok)
        l_bl = lab("brief blips:\nthe ball returns", -4.2, 0.3, TEXT, 34, "l", line_spacing=0.95)
        self.add(l_bl)
        # brief blips first: three clear short pushes, the ball comes back each time
        for _ in range(3):
            bl = arr([-6.3, -1.25, 0], [-4.4, -1.25, 0], LG, 11, 0.4)
            self.play(GrowArrow(bl), xb.animate.set_value(-0.5), run_time=0.2, rate_func=rush_from)
            self.play(FadeOut(bl), xb.animate.set_value(-1.0), run_time=0.22)
        self.at("misreading", lead=0.0)
        push = arr([-6.4, -1.25, 0], [-3.4, -1.25, 0], TEXT, 13, 0.42)
        l_pu = lab("large or lasting\nerror", -4.2, 0.3, TEXT, 34, "l", line_spacing=0.95, weight=BOLD)
        self.play(GrowArrow(push), ReplacementTransform(l_bl, l_pu), run_time=0.45)
        self.at("can tip a cell", lead=0.3)
        self.play(xb.animate.set_value(0.0), run_time=1.0, rate_func=smooth)
        self.at("wrong side")
        l_w = lab("wrong side", LX, -3.4, TEXT, 36)
        self.play(xb.animate.set_value(1.0), FadeOut(push), FadeOut(l_pu), FadeIn(l_w), run_time=0.9, rate_func=rush_into)
        self.at("the switch")
        self.play(Indicate(ar, color=RED, scale_factor=1.0), run_time=0.8)
        self.at("hold the error")
        ring = Circle(radius=0.38, stroke_color=TEXT, stroke_width=5).move_to(ball_at(1.0))
        self.play(Create(ring), run_time=0.6)
        self.finish()


class S22Limit3(SpokenScene):
    def construct(self):
        X = -3.4
        cells = zone_cells(X, TWO)
        flips = {9: "B", 11: "B", 12: "B", 15: "O", 16: "O", 18: "O"}
        for i, k in flips.items():
            col = BLUE if k == "B" else ORANGE
            cells[i].set_stroke(col, 1.5).set_fill(col, 0.6)
        s1 = strip_slope(X - 1.25, 0.5)
        l_s1 = lab("signal", X - 1.25, 3.45, YELLOW, 26)
        cx_, cy_ = 3.4, 1.0
        face = Circle(radius=1.45, stroke_color=TEXT, stroke_width=6).move_to([cx_, cy_, 0])
        ticks = VGroup(*[Line([cx_ + 1.2 * np.sin(a), cy_ + 1.2 * np.cos(a), 0], [cx_ + 1.35 * np.sin(a), cy_ + 1.35 * np.cos(a), 0],
                              color=TEXT, stroke_width=4) for a in np.arange(0, 2 * np.pi, np.pi / 2)])
        hand = Line([cx_, cy_, 0], [cx_, cy_ + 1.05, 0], color=TEXT, stroke_width=6)
        clock = VGroup(face, ticks, hand)
        g_clock = clock.copy().set_stroke(opacity=0.2)
        s2 = VGroup(*[Rectangle(width=0.5, height=CH, stroke_width=0, fill_color=DORSAL,
                                fill_opacity=0.06 + 0.9 * np.exp(-(NC - 1 - i) / 4.0)).move_to([X + 1.25, cy(i), 0]) for i in range(NC)])
        g_s2 = s2.copy()
        for r in g_s2:
            r.set_fill(DORSAL, r.get_fill_opacity() * 0.2)
        l_bn = lab("possible benefit\nin a model", cx_, -2.35, GOLD, 36, line_spacing=0.95, weight=BOLD)
        self.add(cells, s1, l_s1, g_clock, g_s2)
        l_rg = VGroup(lab("ragged border", -1.7, 0.0, TEXT, 36, "l", weight=BOLD), ldr([-1.8, 0.0], [X + 0.62, 0.0], TEXT, 3))
        self.play(FadeIn(l_rg, shift=LEFT * 0.15), Indicate(VGroup(*[cells[i] for i in range(8, 20)]), color=TEXT, scale_factor=1.1), run_time=0.9)
        self.at("reading over time", lead=0.3)
        l_clk = lab("reading over time", cx_, cy_ - 2.0, TEXT, 30)
        self.play(FadeOut(l_rg), FadeOut(g_clock), FadeIn(clock), FadeIn(l_clk, shift=UP * 0.1), run_time=0.6)

        def fix(idxs):
            return [cells[i].animate.set_stroke(ORANGE if i <= 13 else BLUE, 1.5).set_fill(ORANGE if i <= 13 else BLUE, 0.6)
                    for i in idxs]
        c0 = np.array([cx_, cy_, 0])
        self.play(Rotate(hand, -2 * PI * 0.35, about_point=c0, rate_func=linear), *fix([9, 18]), run_time=0.9)
        self.at("two opposing slopes", lead=0.25)
        l_s2 = lab("opposing slope", X + 1.25, 3.45, DORSAL, 26)
        self.play(FadeOut(g_s2), FadeIn(s2), FadeIn(l_s2), *fix([11, 16]), Rotate(hand, -2 * PI * 0.25, about_point=c0, rate_func=linear),
                  run_time=0.9)
        self.play(*fix([12, 15]), run_time=0.4)
        self.at("can help", lead=0.4)
        self.play(FadeIn(l_bn, shift=UP * 0.15), run_time=0.6)
        self.finish()
        self.wait(1.5)


# ============================================================================================
class S23Takeaway(SpokenScene):
    def construct(self):
        MX = -2.2
        tm = tube_map(MX, stripes=True)
        labs = tube_labels(MX, side_epi="l", size=26, with_vz=False)
        self.add(tm, *labs)
        CXc, CW = 3.7, 6.2
        card = RoundedRectangle(corner_radius=0.2, width=CW, height=6.4, stroke_color=GOLD, stroke_width=4,
                                fill_color=GOLD, fill_opacity=0.07).move_to([CXc, -0.1, 0])
        L = CXc - CW / 2 + 0.35
        tk = lab("TAKEAWAY", L, 2.75, GOLD, 26, "l", weight=BOLD)
        num = T("4", 44, GOLD, weight=BOLD).move_to([L + 0.2, 1.95, 0])
        hd = lab("How does a slope\nbecome lines?", L + 0.65, 1.95, TEXT, 26, "l", line_spacing=0.95)
        self.at("the takeaway")
        self.play(FadeIn(card), FadeIn(tk), FadeIn(num), FadeIn(hd), run_time=0.8)
        self.at("the slope sets", lead=0.1)
        c1 = chip("the slope", YELLOW, 30)
        c1.move_to([L + c1.width / 2, 0.85, 0])
        self.play(FadeIn(c1, scale=0.85), run_time=0.5)
        t1 = lab("sets roughly where\neach line falls", L, -0.2, TEXT, 32, "l", line_spacing=0.95)
        self.at("where each line falls", lead=0.3)
        ys = [border_y(r) for r in range(4)]
        lines = VGroup(*[Line([MX - TWD + 0.05, y, 0], [MX + TWD - 0.05, y, 0], color=TEXT, stroke_width=4) for y in ys])
        self.play(FadeIn(t1, shift=LEFT * 0.15), LaggedStart(*[Create(l) for l in lines], lag_ratio=0.2), run_time=1.0)
        self.at("pairs of repressors", lead=0.3)
        c2 = chip("pairs of repressors", RED, 30)
        c2.move_to([L + c2.width / 2, -1.4, 0])
        yb = border_y(0)
        px = MX + TWD + 0.5
        pair = VGroup(inhib([px, yb + 1.1, 0], [px, yb + 0.14, 0], RED, 8, 0.2),
                      inhib([px, yb - 1.1, 0], [px, yb - 0.14, 0], RED, 8, 0.2))
        ld_p = ldr([MX + TWD + 0.02, yb], [px - 0.22, yb], TEXT, 4)
        self.play(FadeIn(c2, scale=0.85), GrowFromCenter(pair), Create(ld_p), run_time=0.9)
        t2 = lab("make each line sharp,\nand help hold it", L, -2.45, TEXT, 32, "l", line_spacing=0.95)
        self.at("make each line sharp", lead=0.3)
        self.play(FadeIn(t2, shift=LEFT * 0.15), *[l.animate.set_stroke(TEXT, 8) for l in lines], run_time=0.9)
        self.at("help hold it")
        self.play(Indicate(pair, color=RED, scale_factor=1.25), run_time=0.8)
        self.finish()


class S24End(EndCard):
    LINE = "Pairs of repressors make each line sharp, and help hold it."
