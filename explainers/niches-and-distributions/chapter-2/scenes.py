"""Planting Past the Edge  (Biochemistrypedia explainer, niches and distributions, chapter 2)

Same COLOUR MAP and map world as chapter 1: niche TEAL; coast SAND, sea pale blue; found = DARK GREEN;
sink GREY; immigrant arrows BLUE; neighbours ORANGE; cleared plots bare TAN; lambda bars YELLOW.
All bar heights are schematic and say so.
"""
import numpy as np
from bp_style import *  # noqa: F401,F403

ORANGE = "#F29E4C"
SAND = "#C9B27C"
SEA = "#4F86B8"
DKG = "#2FB04F"
SINK = "#9AA0A6"
SHRUB = "#7BC96F"
LAMC = "#E8C95A"

MX0, MX1, MY0, MY1 = 0.9, 6.5, -3.3, 2.9
EDGE_Y = 0.2
OX, OY = -5.6, -2.8
BOX_T, BOX_M = (0.25, 0.88), (0.45, 0.85)


def coast_x(y):
    return 1.95 + 0.14 * np.sin(2.2 * y)


def tprof(y):
    return 0.92 - 0.82 * (y + 3.3) / 6.2


def mprof(y):
    return 0.62 + 0.22 * np.sin(1.5 * y + 0.6)


def inbox(t, m):
    return BOX_T[0] <= t <= BOX_T[1] and BOX_M[0] <= m <= BOX_M[1]


def teal_runs():
    ys = np.arange(MY0, MY1 + 1e-6, 0.02)
    runs, a = [], None
    for y in ys:
        ok = inbox(tprof(y), mprof(y))
        if ok and a is None:
            a = y
        if not ok and a is not None:
            runs.append((a, y))
            a = None
    if a is not None:
        runs.append((a, MY1))
    return runs


RUNS = teal_runs()


def px(t):
    return OX + 4.5 * t


def py(m):
    return OY + 5.4 * m


class View:
    def __init__(s, sc=1.0, cm=(3.7, -0.2), cs=(3.7, -0.2), win=(MX0, MX1, MY0, MY1)):
        s.sc, s.cm, s.cs, s.win = sc, cm, cs, win

    def P(s, x, y):
        return np.array([s.cs[0] + s.sc * (x - s.cm[0]), s.cs[1] + s.sc * (y - s.cm[1]), 0.0])

    def inwin(s, x, y):
        return s.win[0] <= x <= s.win[1] and s.win[2] <= y <= s.win[3]


V0 = View()
VZ = View(sc=1.7, cm=(4.3, -1.2), cs=(3.6, -0.3), win=(2.55, 6.1, -3.0, 0.2))


def land_poly(v, ya, yb, color, op, stroke=0):
    ya, yb = max(ya, v.win[2]), min(yb, v.win[3])
    if yb <= ya:
        return None
    ys = np.linspace(ya, yb, max(2, int((yb - ya) / 0.05)))
    a = [v.P(max(coast_x(y), v.win[0]), y) for y in ys]
    b = [v.P(v.win[1], y) for y in ys[::-1]]
    return Polygon(*(a + b), stroke_width=stroke, stroke_color=SAND, fill_color=color, fill_opacity=op)


def sea_poly(v):
    if v.win[0] >= 2.1:
        return None
    ys = np.linspace(v.win[2], v.win[3], 60)
    a = [v.P(v.win[0], y) for y in ys]
    b = [v.P(max(coast_x(y), v.win[0]), y) for y in ys[::-1]]
    return Polygon(*(a + b), stroke_width=0, fill_color=SEA, fill_opacity=0.45)


def tag(text, size=26, color=TEXT, pos=ORIGIN, bg=True):
    t = T(text, size, color)
    t.move_to(pos)
    if not bg:
        return VGroup(t)
    r = BackgroundRectangle(t, color=BG, fill_opacity=0.85, buff=0.1)
    return VGroup(r, t)


def rosette(size=0.5, color=GREEN):
    g = VGroup()
    for k in range(6):
        e = Ellipse(width=size * 0.3, height=size * 0.62, stroke_width=0, fill_color=color, fill_opacity=0.95)
        e.shift(UP * size * 0.28).rotate(k * PI / 3, about_point=ORIGIN)
        g.add(e)
    g.add(Dot(radius=size * 0.08, color="#E8F5C8"))
    return g


def tuft(size=0.6, color=ORANGE):
    g = VGroup()
    for a in (-0.7, -0.35, 0, 0.35, 0.7):
        g.add(Line(ORIGIN, UP * size * (1 - abs(a) * 0.3), color=color, stroke_width=5).rotate(a, about_point=ORIGIN))
    return g.move_to(ORIGIN)


def shrub(size=0.7, color=SHRUB):
    g = VGroup(Line(DOWN * size * 0.5, DOWN * size * 0.1, color="#8A6B3F", stroke_width=6))
    for dx, dy, r in ((-0.22, 0.1, 0.24), (0.22, 0.1, 0.24), (0, 0.3, 0.28)):
        g.add(Circle(radius=r * size, stroke_width=0, fill_color=color, fill_opacity=0.95).shift(RIGHT * dx * size + UP * dy * size))
    return g


def dkdot(p, r=0.09, color=DKG):
    return Dot(p, radius=r, color=color).set_stroke("#0B3D1A", 2.5, 1.0)


# ---- dots (map coordinates) --------------------------------------------------------------------
def make_found():
    rng = np.random.RandomState(7)
    out = []
    for kind, y0, y1 in (("south", -2.9, -2.1), ("neigh", -0.85, 0.05)):
        for y in np.arange(y0, y1 + 1e-6, 0.36):
            for x in np.arange(2.6, 6.2, 0.62):
                if rng.rand() < 0.25:
                    continue
                out.append((x + rng.uniform(-0.12, 0.12), y + rng.uniform(-0.08, 0.08), kind))
    return out


FOUND = make_found()
POCKET = [(3.6 + 0.34 * i, -1.7 + 0.42 * j) for j in range(2) for i in range(6)]


def map_base(v=V0, edge=True, label=True):
    d = {}
    d["sea"] = sea_poly(v)
    d["land"] = land_poly(v, MY0, MY1, SAND, 0.38, 3)
    parts = [d["sea"], d["land"]]
    d["edge"] = VGroup()
    if edge and v.win[2] < EDGE_Y < v.win[3]:
        ln = DashedLine(v.P(coast_x(EDGE_Y) - 0.05, EDGE_Y), v.P(MX1, EDGE_Y), color=TEXT, stroke_width=5, dash_length=0.2)
        d["edge"].add(ln)
        if label:
            d["edge"].add(tag("northern range edge", 24, TEXT, v.P(4.75, EDGE_Y + 0.27)))
    d["base"] = VGroup(*[p for p in parts if p is not None])
    return d


def shade(v=V0, op=0.6):
    g = VGroup()
    for ya, yb in RUNS:
        p = land_poly(v, ya, yb, TEAL, op)
        if p is not None:
            g.add(p)
    return g


def found_dots(v=V0, kinds=("south", "neigh"), pocket=True, r=0.09):
    g = VGroup()
    for x, y, k in FOUND:
        if k in kinds and v.inwin(x, y):
            g.add(dkdot(v.P(x, y), r))
    if pocket:
        for x, y in POCKET:
            if v.inwin(x, y):
                g.add(dkdot(v.P(x, y), r))
    return g


def ambient(scene):
    """Waves drifting up through the sea strip, so a held map is never a dead frame."""
    rip = VGroup()
    for k in range(9):
        w = ParametricFunction(lambda t: np.array([t, 0.07 * np.sin(11 * t), 0]), t_range=[-0.4, 0.4], color=WHITE, stroke_width=5).set_opacity(0.8)
        w.move_to([1.4, MY0 + 0.75 * k, 0])
        w.lo, w.hi, w.k = MY0, MY1, 1.0
        w.add_updater(lambda o, dt: o.shift(UP * 0.6 * dt * o.k) if o.get_y() < o.hi else o.shift(DOWN * (o.hi - o.lo)))
        rip.add(w)
    scene.add(rip)
    scene._rip = rip
    return rip


def header(text, x, color=TEXT, size=32):
    return T(text, size, color, weight=BOLD).move_to([x, 3.4, 0])


# ---- left panel -----------------------------------------------------------------------------
def left_axes():
    xax = Arrow([OX, OY, 0], [OX + 4.8, OY, 0], buff=0, color=GREY, stroke_width=4, tip_length=0.2)
    yax = Arrow([OX, OY, 0], [OX, OY + 5.7, 0], buff=0, color=GREY, stroke_width=4, tip_length=0.2)
    xl = T("temperature", 28, TEXT).move_to([OX + 2.4, OY - 0.45, 0])
    yl = T("soil moisture", 28, TEXT).rotate(PI / 2).move_to([OX - 0.55, OY + 2.7, 0])
    return VGroup(xax, yax, xl, yl)


SPOTS = [(-2.8, 1), (-2.5, 3), (-1.6, 1), (-1.3, 1), (-0.6, 3), (-0.1, 1), (0.4, 1), (0.9, 1), (1.3, 1), (1.9, 1), (2.4, 1), (2.8, 1)]
SPOT_X = [4.2, 3.4, 5.2, 4.0, 4.8, 4.0, 5.0, 3.6, 4.4, 5.0, 3.8, 4.6]


def make_points():
    rng = np.random.RandomState(11)
    pts = []
    for i, (y, n) in enumerate(SPOTS):
        for k in range(n):
            j = 0.015 if n == 1 else 0.05
            t = tprof(y) + (rng.uniform(-j, j) if k else 0)
            m = mprof(y) + (rng.uniform(-j, j) if k else 0)
            pts.append(dict(spot=i, y=y, t=t, m=m, inside=inbox(t, m)))
    return pts


POINTS = make_points()
HI = 5  # the spot used for the lambda close-up (y = -0.1)


def pt_pos(p):
    return np.array([px(p["t"]), py(p["m"]), 0])


def spot_marker(i):
    y = SPOTS[i][0]
    return Circle(radius=0.11, stroke_color=TEXT, stroke_width=3, fill_color=BG, fill_opacity=1).move_to(V0.P(SPOT_X[i], y))


def left_points(color_mode=False, r=0.1):
    g = VGroup()
    for p in POINTS:
        c = TEXT
        if color_mode:
            c = TEAL if p["inside"] else SINK
        g.add(Dot(pt_pos(p), radius=r, color=c))
    return g


def niche_box(c=TEAL):
    x0, x1, y0, y1 = px(BOX_T[0]), px(BOX_T[1]), py(BOX_M[0]), py(BOX_M[1])
    return Rectangle(width=x1 - x0, height=y1 - y0, stroke_color=c, stroke_width=6, fill_color=c, fill_opacity=0.18).move_to([(x0 + x1) / 2, (y0 + y1) / 2, 0])


def divider():
    return DashedLine([-0.1, -3.4, 0], [-0.1, 3.0, 0], color=GREY, stroke_width=3)




# ================================================================================================
# CHAPTER 2 helpers
# ================================================================================================
TAN = "#B89868"
PX, PW, PH = 5.2, 1.1, 0.75
SITE_Y = [-2.6, -1.7, -0.8, 0.2, 1.2, 2.2]      # three inside, one at the edge, two beyond
CB, CU, CMAX = -1.9, 1.8, 3.2                    # chart baseline, height of lambda = 1, tube height
GX = [-5.2 + 0.95 * i for i in range(6)]
BW = 0.38


def pc(i):
    return V0.P(PX, SITE_Y[i])


def sway(m, ph=0.0, amp=0.28):
    m.t = ph

    def up(o, dt):
        o.t += dt
        o.rotate(amp * dt * np.cos(2.2 * o.t), about_point=o.get_bottom())
    m.add_updater(up)
    return m


def ch2_dots(hide=False, op=1.0):
    rng = np.random.RandomState(7)
    g = VGroup()
    for y in np.arange(-2.9, 0.06, 0.36):
        for x in np.arange(2.6, 6.2, 0.62):
            if rng.rand() < 0.25:
                continue
            xx, yy = x + rng.uniform(-0.12, 0.12), y + rng.uniform(-0.08, 0.08)
            if hide and 4.4 < xx < 6.0:
                continue
            g.add(dkdot(V0.P(xx, yy)))
    g.set_opacity(op)
    g.set_z_index(2)
    return g


def edge_line():
    ln = DashedLine(V0.P(coast_x(EDGE_Y) - 0.05, EDGE_Y), V0.P(MX1, EDGE_Y), color=TEXT, stroke_width=5, dash_length=0.2)
    ln.set_z_index(3)
    return ln


def edge_label():
    lab = tag("northern range edge", 26, TEXT, ORIGIN)
    lab.move_to([3.0, EDGE_Y + 0.33, 0])
    lab.shift(RIGHT * (4.45 - lab.get_right()[0]))
    lab.set_z_index(30)
    return lab


def world(scene, dots=True, hide=False, op=1.0, label=True, edge=True):
    m = map_base(V0, label=False)
    m["base"].set_z_index(0)
    scene.add(m["base"])
    d = ch2_dots(hide, op)
    if dots:
        scene.add(d)
    ln = edge_line()
    lab = edge_label()
    if edge:
        scene.add(ln)
    if label and edge:
        scene.add(lab)
    ambient(scene)
    return dict(m=m, dots=d, line=ln, label=lab)


# ---- the six plots on the map --------------------------------------------------------------
def plot_parts(i):
    c = pc(i)
    P = {}
    P["bg"] = Rectangle(width=PW, height=PH, stroke_width=0, fill_color=BG, fill_opacity=0.95).move_to(c)
    P["tan"] = Rectangle(width=PW / 2, height=PH, stroke_width=0, fill_color=TAN, fill_opacity=0.92).move_to(c + RIGHT * PW / 4)
    P["out"] = Rectangle(width=PW, height=PH, stroke_color=TEXT, stroke_width=3, fill_opacity=0).move_to(c)
    P["div"] = Line(c + UP * PH / 2, c + DOWN * PH / 2, color=TEXT, stroke_width=3)
    P["tl"] = sway(tuft(0.3).move_to(c + LEFT * PW / 4 + DOWN * 0.15), ph=i)
    P["tr"] = sway(tuft(0.3).move_to(c + RIGHT * PW / 4 + DOWN * 0.15), ph=i + 1.5)
    P["rl"] = rosette(0.22).move_to(c + LEFT * PW / 4 + UP * 0.13)
    P["rr"] = rosette(0.22).move_to(c + RIGHT * PW / 4 + UP * 0.13)
    z = dict(bg=10, tan=11, tl=12, tr=12, rl=13, rr=13, div=14, out=15)
    for k, v in P.items():
        v.set_z_index(z[k])
    return P


def plot_group(P, keys):
    return VGroup(*[P[k] for k in keys])


STATES = dict(empty=("bg", "out"), whole=("bg", "rl", "rr", "out"), split=("bg", "tan", "tl", "rl", "rr", "div", "out"))


def all_plots(scene, state="split", add=True):
    parts = [plot_parts(i) for i in range(6)]
    groups = [plot_group(P, STATES[state]) for P in parts]
    if add:
        scene.add(*groups)
    return parts, groups


def pulse_plots(scene, groups, idx, color=YELLOW, rt=1.0, sf=1.12):
    return Indicate(VGroup(*[groups[i] for i in idx]), color=color, scale_factor=sf, run_time=rt)


# ---- the lambda chart (left panel) ---------------------------------------------------------
class Chart:
    def __init__(self, vals=None, keys=True):
        self.tr = [[ValueTracker(0.0) for _ in range(2)] for _ in range(6)]
        if vals:
            for i in range(6):
                for j in range(2):
                    self.tr[i][j].set_value(vals[i][j])
        self.base = Line([-5.75, CB, 0], [0.0, CB, 0], color=GREY, stroke_width=3)
        self.dash = DashedLine([-5.75, CB + CU, 0], [0.0, CB + CU, 0], color=TEXT, stroke_width=4, dash_length=0.15)
        self.lam = T("λ = 1", 26, TEXT).move_to([-6.2, CB + CU + 0.3, 0])
        self.tubes = VGroup()
        self.fills = VGroup()
        self.keys = VGroup()
        for i in range(6):
            for j in range(2):
                x = GX[i] + (-0.22 if j == 0 else 0.22)
                self.tubes.add(Rectangle(width=BW, height=CMAX, stroke_color=GREY, stroke_width=2.5, fill_opacity=0).move_to([x, CB + CMAX / 2, 0]))
                f = Rectangle(width=BW, height=0.002, stroke_width=0, fill_color=LAMC, fill_opacity=0.92)
                f.move_to([x, CB + 0.001, 0])

                def up(o, tr=self.tr[i][j], x=x):
                    h = max(tr.get_value() * CU, 0.002)
                    o.stretch_to_fit_height(h)
                    o.move_to([x, CB + h / 2, 0])
                f.add_updater(up)
                self.fills.add(f)
                ic = tuft(0.28).move_to([x, CB - 0.32, 0]) if j == 0 else Square(0.26, stroke_width=0, fill_color=TAN, fill_opacity=0.95).move_to([x, CB - 0.32, 0])
                self.keys.add(ic)
        for a, b, name in ((0, 2, "inside"), (3, 3, "edge"), (4, 5, "beyond")):
            x0, x1 = GX[a] - 0.45, GX[b] + 0.45
            self.keys.add(Line([x0, CB - 0.62, 0], [x1, CB - 0.62, 0], color=GREY, stroke_width=3))
            self.keys.add(T(name, 28, TEXT).move_to([(x0 + x1) / 2, CB - 1.05, 0]))
        self.all = VGroup(self.base, self.dash, self.lam, self.tubes, self.fills, self.keys)
        self.all.set_z_index(5)

    def bar(self, i, j):
        return self.tubes[2 * i + j]

    def to(self, vals):
        """vals: dict {(i, j): value} -> list of animations"""
        return [self.tr[i][j].animate.set_value(v) for (i, j), v in vals.items()]

    def groupvals(self, vv, sites=range(6)):
        return {(i, j): vv[i][j] for i in sites for j in range(2)}

    def tubes_of(self, sites, js=(0, 1)):
        return VGroup(*[self.bar(i, j) for i in sites for j in js])


R1 = [[1.3, 1.4], [1.4, 1.3], [1.3, 1.4], [1.2, 1.3], [1.5, 1.4], [1.6, 1.5]]
R2 = [[1.3, 1.4], [1.4, 1.3], [1.3, 1.4], [0.9, 1.3], [0.55, 1.4], [0.5, 1.5]]
R3 = [[1.3, 1.4], [1.4, 1.3], [1.3, 1.4], [0.8, 0.85], [0.55, 0.6], [0.5, 0.55]]
RF = [[0.6, 0.7], [0.5, 0.6], [0.7, 0.5], [0.5, 0.6], [0.4, 0.5], [0.5, 0.4]]


def ttl(text, y=3.45, color=TEXT, size=34, x=-3.4):
    return T(text, size, color, weight=BOLD).move_to([x, y, 0])


def schem(y=-3.55):
    return T("bar heights schematic", 24, TEXT).move_to([-3.4, y, 0])


# ---- icons -------------------------------------------------------------------------------
def thermo(k=1.0):
    bulb = Circle(radius=0.2 * k, stroke_width=0, fill_color=RED, fill_opacity=1).move_to([0, -0.4 * k, 0])
    stem = RoundedRectangle(corner_radius=0.08 * k, width=0.16 * k, height=0.9 * k, stroke_width=0, fill_color=RED, fill_opacity=1).move_to([0, 0.0, 0])
    ring = RoundedRectangle(corner_radius=0.12 * k, width=0.3 * k, height=1.15 * k, stroke_color=TEXT, stroke_width=3, fill_opacity=0).move_to([0, 0.05 * k, 0])
    return VGroup(ring, stem, bulb)


def seed_stop(k=1.0):
    seed = Ellipse(width=0.3 * k, height=0.46 * k, stroke_color="#8A6B3F", stroke_width=2, fill_color="#E3C58B", fill_opacity=1).move_to([-0.3 * k, -0.05 * k, 0])
    stop = RegularPolygon(8, color=RED, stroke_width=0, fill_opacity=1).scale(0.3 * k).move_to([0.25 * k, 0.05 * k, 0])
    bar = Line([0.12 * k, 0.05 * k, 0], [0.38 * k, 0.05 * k, 0], color=WHITE, stroke_width=6 * k)
    return VGroup(seed, stop, bar)


def seed_icon(k=1.0):
    return Ellipse(width=0.4 * k, height=0.62 * k, stroke_color="#8A6B3F", stroke_width=3, fill_color="#E3C58B", fill_opacity=1)


def glove(s=1.0, col="#D8C9A8"):
    g = VGroup()
    g.add(RoundedRectangle(corner_radius=0.12 * s, width=0.7 * s, height=0.6 * s).move_to([0, 0, 0]))
    for dx, h in ((-0.25, 0.45), (-0.083, 0.55), (0.083, 0.5), (0.25, 0.4)):
        g.add(RoundedRectangle(corner_radius=0.07 * s, width=0.15 * s, height=h * s).move_to([dx * s, (0.27 + h / 2) * s, 0]))
    g.add(RoundedRectangle(corner_radius=0.07 * s, width=0.15 * s, height=0.4 * s).rotate(-0.8).move_to([0.45 * s, 0.05 * s, 0]))
    g.set_fill(col, 1).set_stroke("#8A7E65", 2.5)
    cuff = Rectangle(width=0.8 * s, height=0.22 * s, stroke_color="#8A7E65", stroke_width=2.5, fill_color=GREY, fill_opacity=1).move_to([0, -0.4 * s, 0])
    g.add(cuff)
    return g


def die(s=0.8):
    sq = RoundedRectangle(corner_radius=0.12 * s, width=s, height=s, stroke_color=TEXT, stroke_width=4, fill_color=BG, fill_opacity=1)
    pips = VGroup(*[Dot([dx * s * 0.27, dy * s * 0.27, 0], radius=0.07 * s, color=TEXT) for dx, dy in ((-1, 1), (1, 1), (0, 0), (-1, -1), (1, -1))])
    return VGroup(sq, pips)


def cloud(k=1.0):
    g = VGroup()
    for dx, dy, r in ((-0.35, 0, 0.3), (0.0, 0.18, 0.38), (0.38, 0, 0.3)):
        g.add(Circle(radius=r * k, stroke_width=0, fill_color=GREY, fill_opacity=1).move_to([dx * k, dy * k, 0]))
    g.add(Rectangle(width=1.0 * k, height=0.3 * k, stroke_width=0, fill_color=GREY, fill_opacity=1).move_to([0.02 * k, -0.1 * k, 0]))
    for dx in (-0.3, 0.0, 0.3):
        g.add(Line([dx * k, -0.35 * k, 0], [(dx - 0.08) * k, -0.62 * k, 0], color="#6FA8DC", stroke_width=5))
    return g


def bolt(k=1.0):
    pts = [(0.05, 0.6), (-0.3, -0.05), (-0.02, -0.05), (-0.12, -0.6), (0.3, 0.1), (0.03, 0.1)]
    return Polygon(*[[x * k, y * k, 0] for x, y in pts], stroke_width=0, fill_color=YELLOW, fill_opacity=1)


def grazer(k=1.0):
    c = "#C49A6C"
    g = VGroup(Ellipse(width=0.7 * k, height=0.38 * k, stroke_width=0, fill_color=c, fill_opacity=1),
               Circle(radius=0.14 * k, stroke_width=0, fill_color=c, fill_opacity=1).move_to([0.42 * k, 0.2 * k, 0]))
    for dx in (-0.22, -0.1, 0.12, 0.24):
        g.add(Line([dx * k, -0.12 * k, 0], [dx * k, -0.4 * k, 0], color=c, stroke_width=5))
    return g


def fungus(k=1.0):
    leaf = Ellipse(width=0.9 * k, height=0.55 * k, stroke_width=0, fill_color=GREEN, fill_opacity=1)
    spots = VGroup(*[Dot([dx * k, dy * k, 0], radius=0.07 * k, color="#7A3B1E") for dx, dy in ((-0.2, 0.05), (0.05, -0.1), (0.22, 0.08))])
    return VGroup(leaf, spots)


def soilp(k=1.0):
    g = VGroup(Line([-0.45 * k, 0.15 * k, 0], [0.45 * k, 0.15 * k, 0], color="#8A6B3F", stroke_width=6))
    for dx in (-0.25, 0.0, 0.25):
        g.add(Line([dx * k, 0.15 * k, 0], [(dx * 1.4) * k, -0.3 * k, 0], color="#C49A6C", stroke_width=4))
        g.add(Dot([(dx * 1.4) * k, -0.3 * k, 0], radius=0.07 * k, color=ORANGE))
    return g


def card_text(text, color, size=30):
    t = T(text, size, color, weight=BOLD)
    if t.width > 3.1:
        t.scale_to_fit_width(3.1)
    return t


def card(icon, text, color, y, w=4.8, h=1.4, x=-3.4):
    r = RoundedRectangle(corner_radius=0.18, width=w, height=h, stroke_color=color, stroke_width=4, fill_color=color, fill_opacity=0.14).move_to([x, y, 0])
    icon.move_to([x - w / 2 + 0.85, y, 0])
    t = card_text(text, color).move_to([x + 0.65, y, 0])
    return VGroup(r, icon, t)


CARD_Y = [1.0, -0.65, -2.3]


def three_cards(labels=("conditions", "neighbours", "never arrived")):
    return [card(thermo(0.8), labels[0], TEAL, CARD_Y[0]),
            card(tuft(0.6).scale(1.0), labels[1], ORANGE, CARD_Y[1]),
            card(seed_stop(1.0), labels[2], BLUE, CARD_Y[2])]


def dune_id(scene=None, y=3.0):
    ic = rosette(0.95).move_to([-3.4, y, 0])
    lb = T("the dune plant", 30, GREEN, weight=BOLD).move_to([-3.4, y - 0.8, 0])
    return ic, lb


def ticker(pos, rate, start=1, cap=99, color=TEXT, size=44, prefix="year "):
    m = M(f"{prefix}{start}", size, color).move_to(pos)
    m.t = 0.0

    def up(o, dt):
        o.t += dt
        n = min(cap, start + int(o.t * rate))
        o.become(M(f"{prefix}{n}", size, color).move_to(pos))
    m.add_updater(up)
    return m


# ================================================================================================
class S00Title(TitleCard):
    LESSON = "Niches and distributions"
    TITLE = "Planting Past the Edge"

    def construct(self):
        m = map_base(V0, label=False)
        m["base"].set_opacity(0.4)
        self.add(m["base"], edge_line())
        super().construct()


class S01Hook(SpokenScene):
    def construct(self):
        w = world(self, dots=False, label=False, edge=False)
        ic, lb = dune_id()
        dots = ch2_dots()
        order = sorted(list(dots), key=lambda d: d.get_y())
        self.play(FadeIn(ic, scale=0.5), FadeIn(lb), LaggedStart(*[FadeIn(d, scale=0.4) for d in order], lag_ratio=0.03), run_time=1.4)
        self.at("headland")
        el = edge_label()
        self.play(Create(w["line"]), FadeIn(el), run_time=0.9)
        self.at("why does it stop there")
        q = T("?", 72, TEXT, weight=BOLD).move_to(V0.P(2.7, 1.0))
        self.play(w["line"].animate.set_stroke(YELLOW, 8), FadeIn(q, scale=0.4), run_time=0.6)
        self.play(Indicate(q, color=YELLOW, scale_factor=1.3), run_time=0.8)
        cards = three_cards()
        self.at("is it the cold")
        self.play(FadeIn(cards[0], shift=RIGHT * 0.5), run_time=0.7)
        self.at("the neighbors")
        self.play(FadeIn(cards[1], shift=RIGHT * 0.5), run_time=0.7)
        self.at("seeds never getting there")
        self.play(FadeIn(cards[2], shift=RIGHT * 0.5), w["line"].animate.set_stroke(TEXT, 5), run_time=0.7)
        self.play(cards[2].animate(rate_func=there_and_back).scale(1.04), Indicate(q, color=YELLOW), run_time=1.0)
        self.finish()


class S02Link(SpokenScene):
    def construct(self):
        w = world(self, dots=False, label=False, edge=True)
        self.add(ch2_dots(), edge_label())
        ic, lb = dune_id()
        cards = three_cards()
        self.add(ic, lb, *cards)
        self.play(FadeOut(VGroup(ic, lb, *cards)), run_time=0.5)
        ax = left_axes()
        self.play(Create(ax), run_time=1.2)
        self.at("conditions where")
        nb = niche_box()
        self.play(FadeIn(nb, scale=0.9), run_time=1.0)
        self.at("lambda stays")
        lab = T("λ ≥ 1 without immigrants", 30, TEAL, weight=BOLD).move_to([-2.5, 2.5, 0])
        self.play(FadeIn(lab, shift=UP * 0.15), run_time=0.9)
        self.play(Indicate(nb, color=TEAL, scale_factor=1.05), run_time=1.2)
        self.at("now we test an edge directly")
        inset = VGroup(ax, nb, lab)
        self.play(inset.animate.scale(0.25).move_to([-6.0, 3.1, 0]).set_opacity(0.0), w["line"].animate.set_stroke(YELLOW, 8), run_time=1.3)
        self.play(Indicate(w["line"], color=YELLOW, scale_factor=1.0), run_time=1.0)
        self.play(w["line"].animate.set_stroke(TEXT, 5), run_time=0.5)
        self.finish()


class S03Three(SpokenScene):
    def construct(self):
        w = world(self, dots=False, label=False)
        self.add(ch2_dots(), edge_label())
        ic, lb = dune_id()
        cards = three_cards()
        self.add(ic, lb, *cards)
        self.play(LaggedStart(*[c.animate(rate_func=there_and_back).scale(1.05) for c in cards], lag_ratio=0.35), run_time=1.8)
        names = ["abiotic limit", "biotic limit", "dispersal limit"]
        cols = [TEAL, ORANGE, BLUE]
        keys = ["conditions make an abiotic limit", "other species make a biotic limit", "never arriving makes a dispersal limit"]
        for k in range(3):
            self.at(keys[k], lead=0.0)
            nt = card_text(names[k], cols[k]).move_to(cards[k][2].get_center())
            old = cards[k][2]
            cards[k].remove(old)
            cards[k].add(nt)
            self.play(FadeOut(old), FadeIn(nt), run_time=0.6)
            self.play(*[an for j in range(3) for an in lit(cards[j], j == k, cols[j])], run_time=0.4)
            self.play(cards[k].animate(rate_func=there_and_back).scale(1.05), run_time=0.8)
        self.play(*[an for j in range(3) for an in lit(cards[j], True, cols[j])], run_time=0.6)
        self.finish()


def bump(m, k=1.05):
    return m.animate(rate_func=there_and_back).scale(k)


def lit(m, on, color):
    """Dim or light a card/chip without turning its tinted box solid."""
    r = m[0]
    out = [r.animate.set_fill(color, 0.45 if on else 0.06).set_stroke(opacity=1.0 if on else 0.35)]
    out += [o.animate.set_opacity(1.0 if on else 0.35) for o in list(m)[1:]]
    return out


def sow(scene, i, rt=0.3):
    c = pc(i)
    ros = [rosette(0.22).move_to(c + np.array([dx, 0.13, 0])) for dx in (-PW / 4, PW / 4)]
    for r in ros:
        r.set_z_index(13)
    scene.play(*[FadeIn(r, scale=0.3) for r in ros], run_time=rt)
    return ros


class S04Plant(SpokenScene):
    def construct(self):
        w = world(self, hide=True, op=0.5)
        parts = [plot_parts(i) for i in range(6)]
        frames = [plot_group(P, STATES["empty"]) for P in parts]
        hand = glove(1.5).move_to([-3.4, 0.9, 0])
        hl = T("same planting", 34, TEXT, weight=BOLD).move_to([-3.4, -1.3, 0])
        self.play(FadeIn(hand), FadeIn(hl), LaggedStart(*[FadeIn(f, scale=0.8) for f in frames], lag_ratio=0.2), run_time=1.4)
        self.play(hand.animate.shift(UP * 0.2), run_time=0.2)
        self.at("plant the species beyond the edge")
        hand_at = lambda i: pc(i) + LEFT * 1.05 + DOWN * 0.1
        self.play(hand.animate.scale(0.3).move_to(hand_at(5)), FadeOut(hl), run_time=0.5)
        sown = {}
        sown[5] = sow(self, 5)
        self.play(hand.animate.move_to(hand_at(4)), run_time=0.3)
        sown[4] = sow(self, 4)
        self.play(hand.animate.move_to(hand_at(3)), run_time=0.3)
        sown[3] = sow(self, 3)
        self.at("follow it for years")
        yr = ticker([-3.4, 0.8, 0], 0.8, start=1, cap=9)
        self.add(yr)
        self.at("plant the same way inside")
        for i in (2, 1, 0):
            self.play(hand.animate.move_to(hand_at(i)), run_time=0.3)
            sown[i] = sow(self, i)
        br = Line(V0.P(4.42, -3.0), V0.P(4.42, -0.4), color=TEXT, stroke_width=3)
        cl = T("controls", 28, TEXT, weight=BOLD).move_to(V0.P(3.55, -1.7))
        cl = VGroup(BackgroundRectangle(cl, color=BG, fill_opacity=0.85, buff=0.08), cl)
        br2 = Line(V0.P(4.42, 0.9), V0.P(4.42, 2.6), color=TEXT, stroke_width=3)
        bl = T("beyond", 28, TEXT, weight=BOLD).move_to(V0.P(3.65, 1.75))
        bl = VGroup(BackgroundRectangle(bl, color=BG, fill_opacity=0.85, buff=0.08), bl)
        for o in (br, cl, br2, bl):
            o.set_z_index(30)
        self.play(FadeIn(br), FadeIn(cl), FadeIn(br2), FadeIn(bl), FadeOut(hand), run_time=0.7)
        self.at("transplanting itself")
        yr.clear_updaters()
        bz = bolt(1.6).move_to([-3.4, 1.7, 0])
        bt = T("transplant shock", 34, YELLOW, weight=BOLD).move_to([-3.4, 0.5, 0])
        self.play(FadeOut(yr), FadeIn(bz, scale=0.5), FadeIn(bt), run_time=0.7)
        self.play(Indicate(VGroup(*[sown[i][k] for i in range(6) for k in range(2)]), color=YELLOW, scale_factor=1.2), run_time=1.0)
        self.at("a bad year")
        cd = cloud(1.6).move_to([-3.4, -1.1, 0])
        ct = T("a bad year", 34, GREY, weight=BOLD).move_to([-3.4, -2.6, 0])
        self.play(FadeIn(cd, shift=DOWN * 0.3), FadeIn(ct), run_time=0.8)
        self.at("kill plants anywhere")
        self.play(LaggedStart(*[Indicate(frames[i], color=RED, scale_factor=1.15) for i in range(6)], lag_ratio=0.12), run_time=1.4)
        self.finish()


def big_plot():
    """The enlarged example site in the left panel (neighbours = ORANGE tufts, the dune plant = rosettes)."""
    cx, cy, W, H = -3.4, 0.9, 4.4, 2.4
    bg = Rectangle(width=W, height=H, stroke_color=TEXT, stroke_width=4, fill_color=BG, fill_opacity=0.95).move_to([cx, cy, 0])
    tan = Rectangle(width=W / 2, height=H, stroke_width=0, fill_color=TAN, fill_opacity=0.92).move_to([cx + W / 4, cy, 0])
    dv = Line([cx, cy + H / 2, 0], [cx, cy - H / 2, 0], color=TEXT, stroke_width=4)
    lt = VGroup(*[sway(tuft(0.7).move_to([x, y, 0]), ph=x) for x, y in ((-5.1, 0.4), (-4.3, 1.2), (-3.75, 0.45))])
    rt = VGroup(*[sway(tuft(0.7).move_to([x, y, 0]), ph=x + 1) for x, y in ((-3.05, 0.4), (-2.3, 1.2), (-1.75, 0.45))])
    rl = VGroup(*[rosette(0.42).move_to([x, y, 0]) for x, y in ((-4.85, 1.55), (-4.2, 0.35))])
    rr = VGroup(*[rosette(0.42).move_to([x, y, 0]) for x, y in ((-2.85, 1.55), (-2.2, 0.35))])
    return dict(bg=bg, tan=tan, dv=dv, lt=lt, rt=rt, rl=rl, rr=rr)


class S05Neighbours(SpokenScene):
    def construct(self):
        w = world(self, hide=True, op=0.5)
        parts, groups = all_plots(self, "whole")
        B = big_plot()
        self.add(B["bg"], B["lt"], B["rt"], B["rl"], B["rr"])
        for P in parts:
            P["tl"].set_opacity(0)
            P["tr"].set_opacity(0)
        self.add(*[P["tl"] for P in parts], *[P["tr"] for P in parts])
        self.play(*[P["tl"].animate.set_opacity(1) for P in parts], *[P["tr"].animate.set_opacity(1) for P in parts], run_time=0.5)
        self.at("split every site in two")
        self.play(Create(B["dv"]), LaggedStart(*[Create(P["div"]) for P in parts], lag_ratio=0.1), run_time=1.0)
        self.at("randomly chosen")
        d = die(0.9).move_to([-5.6, 2.95, 0])
        dl = T("random", 32, TEXT, weight=BOLD).move_to([-4.2, 2.95, 0])
        self.play(FadeIn(d, scale=0.5), FadeIn(dl), run_time=0.5)
        self.play(Rotate(d, angle=TAU, run_time=1.0))
        self.at("clear away")
        B["tan"].set_opacity(0)
        self.add(B["tan"])
        for P in parts:
            P["tan"].set_opacity(0)
            self.add(P["tan"])
        self.play(FadeOut(B["rt"], shift=RIGHT * 0.5), *[FadeOut(P["tr"], shift=RIGHT * 0.2) for P in parts],
                  B["tan"].animate.set_opacity(0.92), *[P["tan"].animate.set_opacity(0.92) for P in parts], run_time=1.0)
        self.bring_to_front(*B["rr"])
        ct = VGroup(T("neighbours", 30, TEXT, weight=BOLD), T("cleared", 30, TAN, weight=BOLD)).arrange(DOWN, buff=0.05).move_to([-2.1, -0.75, 0])
        self.play(FadeIn(ct, shift=UP * 0.1), run_time=0.7)
        self.at("on the others")
        lt = VGroup(T("neighbours", 30, TEXT, weight=BOLD), T("left", 30, ORANGE, weight=BOLD)).arrange(DOWN, buff=0.05).move_to([-4.7, -0.75, 0])
        self.play(FadeIn(lt, shift=UP * 0.1), Indicate(B["lt"], color=ORANGE, scale_factor=1.15), run_time=1.0)
        self.play(Indicate(VGroup(*[P["tl"] for P in parts]), color=ORANGE, scale_factor=1.3), run_time=1.0)
        self.finish()


def icon_row():
    surv = VGroup(rosette(0.6), T("survival", 26, GREEN, weight=BOLD)).arrange(DOWN, buff=0.12)
    grow = VGroup(Arrow([0, -0.3, 0], [0, 0.35, 0], buff=0, color=GREEN, stroke_width=8, tip_length=0.25), T("growth", 26, GREEN, weight=BOLD)).arrange(DOWN, buff=0.12)
    sd = VGroup(*[seed_icon(0.5).move_to([dx, dy, 0]) for dx, dy in ((-0.25, 0), (0.0, 0.1), (0.25, 0))])
    seeds = VGroup(sd, T("seed production", 26, GREEN, weight=BOLD)).arrange(DOWN, buff=0.12)
    for g, x in ((surv, -5.5), (grow, -3.8), (seeds, -1.6)):
        g.move_to([x, 2.7, 0])
    return [surv, grow, seeds]


class S06Lambda(SpokenScene):
    def construct(self):
        w = world(self, hide=True, op=0.5)
        parts, groups = all_plots(self, "split")
        ch = Chart()
        self.play(FadeIn(ch.all), run_time=0.8)
        ic = icon_row()
        self.at("survival")
        self.play(FadeIn(ic[0], shift=DOWN * 0.2), run_time=0.6)
        self.at("growth")
        self.play(FadeIn(ic[1], shift=DOWN * 0.2), run_time=0.6)
        self.at("seed production")
        self.play(FadeIn(ic[2], shift=DOWN * 0.2), run_time=0.6)
        self.at("from those")
        ars = VGroup(*[Arrow([g.get_center()[0], 1.95, 0], [g.get_center()[0], 1.4, 0], buff=0, color=YELLOW, stroke_width=6, tip_length=0.2) for g in ic])
        self.play(LaggedStart(*[GrowArrow(a) for a in ars], lag_ratio=0.25), run_time=1.0)
        self.at("estimate lambda")
        self.play(LaggedStart(*[Indicate(t, color=LAMC, scale_factor=1.0) for t in ch.tubes], lag_ratio=0.06), run_time=1.6)
        self.at("every plot")
        self.play(LaggedStart(*[Indicate(g, color=YELLOW, scale_factor=1.15) for g in groups], lag_ratio=0.1), run_time=1.3)
        self.at("one season's survival")
        sv = VGroup(rosette(0.6), T("first-year survival", 30, TEXT, weight=BOLD)).arrange(RIGHT, buff=0.25).move_to([-3.4, 2.7, 0])
        x1 = Line(sv.get_corner(UL), sv.get_corner(DR), color=RED, stroke_width=5)
        x2 = Line(sv.get_corner(UR), sv.get_corner(DL), color=RED, stroke_width=5)
        self.play(FadeOut(VGroup(*ic, ars)), run_time=0.4)
        self.play(FadeIn(sv), run_time=0.5)
        self.play(Create(x1), Create(x2), run_time=0.6)
        self.play(Indicate(VGroup(sv, x1, x2), color=RED, scale_factor=1.05), run_time=0.9)
        self.finish()


def state_world(scene, state="split", chart_vals=None):
    w = world(scene, hide=True, op=0.5)
    parts, groups = all_plots(scene, state)
    ch = Chart(chart_vals)
    scene.add(ch.all)
    return w, parts, groups, ch


class S07Dispersal(SpokenScene):
    def construct(self):
        w, parts, groups, ch = state_world(self)
        t = ttl("result 1")
        sc = schem()
        self.play(FadeIn(t), FadeIn(sc), run_time=0.5)
        self.play(*ch.to(ch.groupvals(R1, range(4))), run_time=1.6)
        self.at("lambda beyond the edge")
        self.play(*ch.to(ch.groupvals(R1, (4, 5))), pulse_plots(self, groups, (4, 5), YELLOW, 1.3), run_time=1.3)
        self.at("with or without neighbors")
        self.play(Indicate(ch.tubes_of((4, 5)), color=LAMC, scale_factor=1.0), run_time=1.2)
        self.at("the species can live there")
        cl = T("the species can live there", 30, GREEN, weight=BOLD).move_to([-3.4, 2.3, 0])
        self.play(FadeIn(cl, shift=UP * 0.1), *[g[-1].animate.set_stroke(GREEN, 6) for g in groups[4:]], run_time=0.8)
        self.play(Indicate(ch.tubes_of((4, 5)), color=GREEN, scale_factor=1.0), run_time=1.0)
        self.at("seeds have not arrived")
        t2 = VGroup(T("result 1:", 34, TEXT, weight=BOLD), T("dispersal limit (likely)", 34, TEXT, weight=BOLD)).arrange(DOWN, buff=0.08).move_to([-3.4, 3.2, 0])
        ars = VGroup(*[Arrow(V0.P(x, -0.6), V0.P(x, 0.0), buff=0, color=BLUE, stroke_width=7, tip_length=0.2) for x in (2.9, 3.6)])
        bars = VGroup(*[Line(V0.P(x - 0.3, 0.12), V0.P(x + 0.3, 0.12), color=BLUE, stroke_width=8) for x in (2.9, 3.6)])
        for o in (ars, bars):
            o.set_z_index(20)
        self.play(FadeOut(cl), Transform(t, t2), FadeIn(ars), FadeIn(bars), run_time=1.0)
        self.play(Indicate(ars, color=BLUE, scale_factor=1.1), run_time=1.0)
        self.at("recolonized empty patches")
        ps = VGroup(*[DashedVMobject(Circle(radius=0.22, color=BLUE, stroke_width=4)).move_to(V0.P(x, y)) for x, y in ((2.7, 1.1), (3.4, 1.6), (3.9, 1.0))])
        ps.set_z_index(20)
        self.play(LaggedStart(*[FadeIn(p, scale=0.5) for p in ps], lag_ratio=0.3), run_time=1.0)
        self.play(Indicate(ps, color=BLUE, scale_factor=1.15), run_time=1.0)
        self.finish()


class S08Dune(SpokenScene):
    def construct(self):
        w = world(self, hide=False, op=1.0)
        parts, groups, ch = None, None, None
        cap = T("Cross and Eckert", 32, GOLD, weight=BOLD).move_to([-3.4, 3.4, 0])
        ic = rosette(1.3).move_to([-3.4, 2.1, 0])
        lb = T("the dune plant", 34, GREEN, weight=BOLD).move_to([-3.4, 1.05, 0])
        self.play(FadeIn(cap), FadeIn(ic, scale=0.5), FadeIn(lb), run_time=0.8)
        self.at("though its neighbors were never cleared")
        note = chip("neighbours not tested", ORANGE, 30)
        note.move_to([-3.4, 0.0, 0])
        self.play(FadeIn(note, shift=UP * 0.1), run_time=0.8)
        self.play(Indicate(note, color=ORANGE, scale_factor=1.05), run_time=0.8)
        self.at("planted beyond its northern edge")
        pos = [(3.45 + 0.3 * i, 0.9 + 0.3 * j) for j in range(3) for i in range(5)]
        pl = [rosette(0.24).move_to(V0.P(*p)) for p in pos]
        for p in pl:
            p.set_z_index(20)
        lab = tag("planted beyond the edge", 26, GREEN, V0.P(4.35, 2.5))
        lab.set_z_index(30)
        self.play(LaggedStart(*[FadeIn(r, scale=0.3) for r in pl[:4]], lag_ratio=0.15), FadeIn(lab), run_time=0.9)
        self.at("the population")
        yrs = ticker([-3.4, -1.0, 0], 12 / 2.4, start=0, cap=12, size=44)
        yrs.t = 0.0
        self.add(yrs)
        tr = T("more than tripled", 40, GREEN, weight=BOLD).move_to([-3.4, -2.2, 0])
        self.play(LaggedStart(*[FadeIn(r, scale=0.3) for r in pl[4:]], lag_ratio=0.2),
                  Succession(Wait(0.9), FadeIn(tr, shift=UP * 0.2)), run_time=2.4, rate_func=linear)
        yrs.clear_updaters()
        fin = M("12 to 14 years", 40, TEXT).move_to([-3.4, -1.0, 0])
        self.play(Transform(yrs, fin), run_time=0.4)
        self.play(Indicate(VGroup(*pl), color=GREEN, scale_factor=1.1), run_time=1.0)
        self.finish()


class S09Biotic(SpokenScene):
    def construct(self):
        w, parts, groups, ch = state_world(self)
        t = ttl("result 2")
        sc = schem()
        self.play(FadeIn(t), FadeIn(sc), run_time=0.4)
        self.play(*ch.to(ch.groupvals(R2, range(4))), run_time=1.4)
        self.at("beyond the edge")
        self.play(pulse_plots(self, groups, (4, 5), YELLOW, 1.0), run_time=1.0)
        self.at("lambda falls below one")
        self.play(*ch.to({(4, 0): R2[4][0], (5, 0): R2[5][0]}), run_time=1.3)
        self.at("neighbors remain")
        self.play(Indicate(VGroup(parts[4]["tl"], parts[5]["tl"]), color=ORANGE, scale_factor=1.5),
                  Indicate(ch.tubes_of((4, 5), (0,)), color=ORANGE, scale_factor=1.0), run_time=1.2)
        self.at("cleared plots do fine")
        self.play(*ch.to({(4, 1): R2[4][1], (5, 1): R2[5][1]}), Indicate(VGroup(parts[4]["tan"], parts[5]["tan"]), color=TAN, scale_factor=1.15), run_time=1.3)
        self.at("other species are setting")
        t2 = VGroup(T("result 2:", 34, TEXT, weight=BOLD), T("biotic limit", 34, ORANGE, weight=BOLD)).arrange(DOWN, buff=0.08).move_to([-3.4, 3.2, 0])
        self.play(Transform(t, t2), Indicate(VGroup(parts[4]["tl"], parts[5]["tl"]), color=ORANGE, scale_factor=1.5), run_time=1.2)
        self.play(Indicate(ch.tubes_of((4, 5), (0,)), color=ORANGE, scale_factor=1.0), run_time=1.0)
        self.finish()


class S10Predict(SpokenScene):
    def construct(self):
        w, parts, groups, ch = state_world(self, chart_vals=R2)
        t = ttl("result 3")
        sc = schem()
        self.play(*[tr.animate.set_value(0.0) for row in ch.tr for tr in row], FadeIn(sc), run_time=0.7)
        self.play(FadeIn(t), run_time=0.4)
        self.at("the plots inside the range")
        self.play(*ch.to(ch.groupvals(R3, range(3))), pulse_plots(self, groups, (0, 1, 2), YELLOW, 1.4), run_time=1.4)
        self.at("beyond the edge")
        self.play(*ch.to(ch.groupvals(R3, (3, 4, 5))), run_time=1.5)
        self.at("whether or not")
        self.play(Indicate(ch.tubes_of((4, 5)), color=LAMC, scale_factor=1.0), pulse_plots(self, groups, (4, 5), YELLOW, 1.2), run_time=1.2)
        self.at("what does that implicate")
        q = chip("What is implicated?", YELLOW, 34).move_to([-3.4, 2.55, 0])
        self.play(FadeIn(q, scale=0.7), run_time=0.7)
        self.play(Indicate(q, color=YELLOW, scale_factor=1.06), run_time=0.8)
        self.finish()


class S11Pause(NarratedScene):
    def construct(self):
        w, parts, groups, ch = state_world(self, chart_vals=R3)
        self.add(ttl("result 3"), schem(), chip("What is implicated?", YELLOW, 34).move_to([-3.4, 2.55, 0]))
        trk = ValueTracker(1.0)
        ring = always_redraw(lambda: Arc(radius=0.5, start_angle=PI / 2, angle=-TAU * trk.get_value(), color=YELLOW, stroke_width=8).move_to([-0.7, 2.55, 0]))
        self.add(ring)
        self.play(trk.animate.set_value(0.001), run_time=max(1.0, self.narration_s - 0.2), rate_func=linear)
        self.finish()


class S12Reveal(SpokenScene):
    def construct(self):
        w = world(self, hide=True, op=0.5)
        parts, groups = all_plots(self, "split")
        glow = Rectangle(width=1.5, height=2.1, stroke_color=YELLOW, stroke_width=6, fill_opacity=0).move_to(V0.P(PX, 1.7))
        glow.set_z_index(25)
        clk = ValueTracker(0)
        clk.add_updater(lambda o, dt: o.increment_value(dt))
        self.add(clk)
        glow.add_updater(lambda o: o.set_stroke(opacity=0.45 + 0.45 * np.sin(3 * clk.get_value())))
        t = VGroup(T("result 3:", 34, TEXT, weight=BOLD), T("conditions beyond the edge", 34, TEAL, weight=BOLD)).arrange(DOWN, buff=0.08).move_to([-3.4, 3.2, 0])
        self.add(t, glow)
        self.at("conditions beyond the edge", lead=0.0)
        th = card(thermo(0.8), "conditions", TEAL, 1.7, h=1.3)
        self.play(FadeIn(th, scale=0.9), run_time=0.7)
        self.at("climate is a strong candidate")
        tg = T("candidate, not proved", 32, YELLOW, weight=BOLD).move_to([-3.4, 0.75, 0])
        self.play(th[0].animate.set_fill(TEAL, 0.45), FadeIn(tg), run_time=1.0)
        icons = [(grazer(1.0), "herbivores", -5.4), (fungus(1.0), "pathogens", -3.5), (soilp(1.0), "soil partners", -1.4)]
        objs = []
        for (ic, name, x), key in zip(icons, ("herbivores", "pathogens", "missing soil partners")):
            self.at(key)
            ic.move_to([x, -0.45, 0])
            lb = T(name, 24, TEXT).move_to([x, -1.3, 0])
            self.play(FadeIn(ic, shift=UP * 0.2), FadeIn(lb), run_time=0.6)
            objs += [ic, lb]
        self.at("need their own tests first")
        tt = T("test these too", 34, TEXT, weight=BOLD).move_to([-3.4, -2.4, 0])
        self.play(FadeIn(tt, shift=UP * 0.1), LaggedStart(*[Indicate(o, color=YELLOW, scale_factor=1.15) for o in objs[::2]], lag_ratio=0.3), run_time=1.3)
        self.finish()


class S13Fail(SpokenScene):
    def construct(self):
        w, parts, groups, ch = state_world(self)
        self.play(FadeIn(schem()), run_time=0.4)
        self.at("every plot fails")
        self.play(*ch.to(ch.groupvals(RF)), run_time=1.4)
        self.at("inside the range as well as beyond it")
        self.play(Indicate(ch.tubes_of((0, 1, 2)), color=LAMC, scale_factor=1.0), run_time=0.9)
        self.play(Indicate(ch.tubes_of((4, 5)), color=LAMC, scale_factor=1.0), pulse_plots(self, groups, (0, 1, 2, 4, 5), RED, 1.0), run_time=1.0)
        self.at("then the test cannot")
        bn = T("the edge cannot be singled out", 30, RED, weight=BOLD)
        bn.scale_to_fit_width(min(bn.width, 6.0))
        bn.move_to([-3.4, 3.4, 0])
        self.play(FadeIn(bn, shift=DOWN * 0.15), run_time=0.8)
        self.at("handling")
        its = []
        gl = glove(0.8).move_to([-5.4, 2.6, 0]); gt = T("handling?", 24, TEXT).move_to([-5.4, 1.8, 0])
        self.play(FadeIn(gl, scale=0.6), FadeIn(gt), run_time=0.5)
        self.at("the seed")
        sd = seed_icon(1.0).move_to([-3.4, 2.6, 0]); st = T("the seed?", 24, TEXT).move_to([-3.4, 1.8, 0])
        self.play(FadeIn(sd, scale=0.6), FadeIn(st), run_time=0.5)
        self.at("bad year")
        cd = cloud(0.9).move_to([-1.4, 2.6, 0]); ct = T("bad year?", 24, TEXT).move_to([-1.4, 1.8, 0])
        self.play(FadeIn(cd, scale=0.6), FadeIn(ct), run_time=0.5)
        grp = VGroup(gl, gt, sd, st, cd, ct)
        self.at("check them")
        self.play(LaggedStart(*[Indicate(o, color=YELLOW, scale_factor=1.2) for o in (gl, sd, cd)], lag_ratio=0.25), run_time=1.0)
        self.at("repeat the study")
        arr = Arc(radius=0.42, start_angle=0, angle=1.5 * PI, color=TEXT, stroke_width=8).add_tip(tip_length=0.24).move_to([-4.2, 2.25, 0])
        rl = T("repeat", 34, TEXT, weight=BOLD).move_to([-2.7, 2.25, 0])
        arr.add_updater(lambda o, dt: o.rotate(2.0 * dt))
        self.play(FadeOut(grp), run_time=0.3)
        self.play(FadeIn(arr), FadeIn(rl), run_time=0.4)
        self.finish()


# ---- the two-by-two table ----------------------------------------------------------------
TCX = [-3.6, -1.6]          # column centres (inside, beyond)
TRY = [1.55, -0.15]         # row centres (neighbours left, cleared)
CW, CH = 2.0, 1.7


def table():
    g = VGroup()
    x0, x1, x2 = TCX[0] - CW / 2, TCX[0] + CW / 2, TCX[1] + CW / 2
    yt, ym, yb = TRY[0] + CH / 2, (TRY[0] + TRY[1]) / 2, TRY[1] - CH / 2
    for y in (yt, ym, yb):
        g.add(Line([x0 - 1.9, y, 0], [x2, y, 0], color=GREY, stroke_width=3))
    for x in (x0, x1, x2):
        g.add(Line([x, yt, 0], [x, yb, 0], color=GREY, stroke_width=3))
    heads = VGroup(T("inside", 32, TEXT, weight=BOLD).move_to([TCX[0], yt + 0.4, 0]), T("beyond", 32, TEXT, weight=BOLD).move_to([TCX[1], yt + 0.4, 0]))
    rows = VGroup(*[VGroup(T("neighbours", 24, TEXT, weight=BOLD), T(w2, 24, c, weight=BOLD)).arrange(DOWN, buff=0.05).move_to([x0 - 1.15, TRY[r], 0])
                    for r, (w2, c) in enumerate((("left", ORANGE), ("cleared", TAN)))])
    return g, heads, rows


class Cells:
    def __init__(self, vals=None):
        self.tr = [[ValueTracker(0.0) for _ in range(2)] for _ in range(2)]   # [row][col]
        if vals:
            for r in range(2):
                for c in range(2):
                    self.tr[r][c].set_value(vals[r][c])
        self.tubes, self.fills, self.dash = VGroup(), VGroup(), VGroup()
        for r in range(2):
            for c in range(2):
                x, yb = TCX[c], TRY[r] - CH / 2 + 0.15
                self.tubes.add(Rectangle(width=0.6, height=1.4, stroke_color=GREY, stroke_width=2.5, fill_opacity=0).move_to([x, yb + 0.7, 0]))
                f = Rectangle(width=0.6, height=0.002, stroke_width=0, fill_color=LAMC, fill_opacity=0.92)

                def up(o, tr=self.tr[r][c], x=x, yb=yb):
                    h = max(tr.get_value() * 0.8, 0.002)
                    o.stretch_to_fit_height(h)
                    o.move_to([x, yb + h / 2, 0])
                f.add_updater(up)
                self.fills.add(f)
                self.dash.add(DashedLine([x - 0.55, yb + 0.8, 0], [x + 0.55, yb + 0.8, 0], color=TEXT, stroke_width=3, dash_length=0.1))
        self.all = VGroup(self.tubes, self.fills, self.dash)

    def to(self, vals):
        return [self.tr[r][c].animate.set_value(vals[r][c]) for r in range(2) for c in range(2)]


class S14Rule(SpokenScene):
    def construct(self):
        w = world(self, hide=True, op=0.5)
        parts, groups = all_plots(self, "split")
        g, heads, rows = table()
        cells = Cells()
        self.play(Create(g), run_time=1.0)
        self.play(FadeIn(heads), FadeIn(rows), FadeIn(cells.all), run_time=0.8)
        self.at("compare lambda beyond the edge")
        hb = Rectangle(width=CW, height=2 * CH, stroke_color=YELLOW, stroke_width=6).move_to([TCX[1], (TRY[0] + TRY[1]) / 2, 0])
        hi = Rectangle(width=CW, height=2 * CH, stroke_color=BLUE, stroke_width=6).move_to([TCX[0], (TRY[0] + TRY[1]) / 2, 0])
        self.play(Create(hb), pulse_plots(self, groups, (4, 5), YELLOW, 1.2), run_time=1.2)
        self.at("with lambda inside the range")
        self.play(Create(hi), FadeOut(hb), pulse_plots(self, groups, (0, 1, 2), BLUE, 1.2), run_time=1.2)
        self.at("on plots with and without")
        hr1 = Rectangle(width=CW * 2 + 1.9, height=CH, stroke_color=ORANGE, stroke_width=6).move_to([-3.55, TRY[0], 0])
        hr2 = Rectangle(width=CW * 2 + 1.9, height=CH, stroke_color=TAN, stroke_width=6).move_to([-3.55, TRY[1], 0])
        self.play(FadeOut(hi), Create(hr1), Indicate(VGroup(*[P["tl"] for P in parts]), color=ORANGE, scale_factor=1.3), run_time=1.1)
        self.play(FadeOut(hr1), Create(hr2), Indicate(VGroup(*[P["tan"] for P in parts]), color=TAN, scale_factor=1.15), run_time=1.1)
        self.play(FadeOut(hr2), run_time=0.4)
        self.finish()


class S15Why(SpokenScene):
    def construct(self):
        w = world(self, hide=True, op=0.5)
        parts, groups = all_plots(self, "split")
        g, heads, rows = table()
        cells = Cells()
        self.add(g, heads, rows, cells.all)
        chips = [chip("access", BLUE, 24, pad=0.12), chip("neighbours", ORANGE, 24, pad=0.12), chip("conditions", TEAL, 24, pad=0.12)]
        for c, x in zip(chips, (-5.6, -3.5, -1.2)):
            c.move_to([x, -1.7, 0])
            c[0].set_fill(c[0].get_stroke_color(), 0.06).set_stroke(opacity=0.35)
            c[1].set_opacity(0.35)
        self.play(FadeIn(VGroup(*chips)), run_time=0.5)
        pats = dict(
            a=[[1.3, 1.4], [1.3, 1.4]],
            n=[[1.3, 0.5], [1.3, 1.4]],
            c=[[1.3, 0.5], [1.3, 0.5]])
        outl = [Rectangle(width=CW, height=2 * CH, stroke_color=BLUE, stroke_width=6).move_to([TCX[1], (TRY[0] + TRY[1]) / 2, 0]),
                Rectangle(width=CW, height=CH, stroke_color=ORANGE, stroke_width=6).move_to([TCX[1], TRY[0], 0]),
                Rectangle(width=CW, height=2 * CH, stroke_color=TEAL, stroke_width=6).move_to([TCX[1], (TRY[0] + TRY[1]) / 2, 0])]
        ccol = [BLUE, ORANGE, TEAL]
        cur = None
        for k, (key, ph) in enumerate((("access", "a"), ("neighbors", "n"), ("conditions beyond", "c"))):
            self.at(key)
            anims = [an for j, c in enumerate(chips) for an in lit(c, j == k, ccol[j])]
            if cur is not None:
                anims.append(FadeOut(cur))
            self.play(*anims, *cells.to(pats[ph]), Create(outl[k]), run_time=1.0)
            cur = outl[k]
        self.at("edge")
        ics = [(grazer(0.7), "herbivores", -5.2), (fungus(0.7), "pathogens", -3.4), (soilp(0.7), "soil partners", -1.5)]
        objs = []
        for ic, nm, x in ics:
            ic.move_to([x, -2.45, 0])
            objs += [ic, T(nm, 22, TEXT).move_to([x, -2.95, 0])]
        cap = T("need their own tests", 26, YELLOW, weight=BOLD).move_to([-3.4, -3.45, 0])
        self.play(FadeOut(cur), *[an for j, c in enumerate(chips) for an in lit(c, False, ccol[j])], FadeIn(VGroup(*objs)), FadeIn(cap), run_time=0.8)
        self.at("a map of where")
        occ = ch2_dots(hide=False, op=1.0)
        occ.set_z_index(26)
        ml = T("map alone: cannot tell", 30, SAND, weight=BOLD).move_to([3.7, 3.4, 0])
        self.play(*[g2.animate.set_opacity(0.0) for g2 in groups], w["m"]["base"].animate.set_opacity(0.3), FadeIn(occ), FadeIn(ml), run_time=1.2)
        self.at("cannot do it")
        self.play(Indicate(ml, color=YELLOW, scale_factor=1.08), Indicate(occ, color=DKG, scale_factor=1.04), run_time=1.4)
        self.finish()


class S16Takehome(SpokenScene):
    def construct(self):
        w = world(self, hide=True, op=0.5)
        parts, groups = all_plots(self, "empty")
        ch = Chart()
        self.play(FadeIn(ch.all), run_time=0.6)
        self.at("plant beyond the edge", lead=0.0)
        bl = tag("beyond", 26, TEXT, V0.P(3.65, 1.75)); bl.set_z_index(30)
        ros = {}
        def sow2(idx):
            out = []
            for i in idx:
                c = pc(i)
                for dx in (-PW / 4, PW / 4):
                    r = rosette(0.22).move_to(c + np.array([dx, 0.13, 0])); r.set_z_index(13); out.append(r)
            return out
        self.play(*[FadeIn(r, scale=0.3) for r in sow2((4, 5))], FadeIn(bl), run_time=0.8)
        self.at("with the same planting inside")
        cl = tag("controls", 26, TEXT, V0.P(3.5, -1.7)); cl.set_z_index(30)
        self.play(*[FadeIn(r, scale=0.3) for r in sow2((0, 1, 2, 3))], FadeIn(cl), run_time=0.9)
        self.at("and measure lambda")
        self.play(*ch.to(ch.groupvals(R1)), run_time=1.6)
        self.play(Indicate(ch.tubes, color=LAMC, scale_factor=1.0), run_time=1.0)
        self.at("where it replaces itself")
        lt = T("λ ≥ 1 beyond the edge", 32, YELLOW, weight=BOLD).move_to([-3.4, 2.7, 0])
        self.play(FadeIn(lt, shift=UP * 0.1), Indicate(ch.tubes_of((4, 5)), color=YELLOW, scale_factor=1.0), pulse_plots(self, groups, (4, 5), YELLOW, 1.2), run_time=1.3)
        self.at("the range stops short")
        sh = VGroup()
        for ya, yb in RUNS:
            if yb > EDGE_Y:
                p = land_poly(V0, max(ya, EDGE_Y), yb, TEAL, 0.4)
                if p is not None:
                    sh.add(p)
        sh.set_z_index(1)
        nl = VGroup(T("niche continues", 24, TEAL, weight=BOLD), T("past the edge", 24, TEAL, weight=BOLD)).arrange(DOWN, buff=0.05).move_to(V0.P(3.3, 1.75))
        nl = VGroup(BackgroundRectangle(nl, color=BG, fill_opacity=0.8, buff=0.08), nl); nl.set_z_index(30)
        self.play(FadeOut(bl), FadeIn(sh), FadeIn(nl), run_time=1.2)
        self.play(Indicate(sh, color=TEAL, scale_factor=1.02), run_time=1.2)
        self.finish()


class S17End(EndCard):
    LINE = "Transplants with inside controls tell conditions, neighbours and access apart."
