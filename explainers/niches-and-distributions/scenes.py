"""Where It Can Live, Where It Is  (Biochemistrypedia explainer, niches and distributions)

COLOUR MAP: niche box TEAL; coast SAND, sea pale blue; found = DARK GREEN dots; sink = GREY dots,
immigrant arrows BLUE; neighbours ORANGE; lambda bars YELLOW. Curves/shading are computed from one
schematic condition profile along the coast (tprof, mprof) and one niche box.
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
class S00Title(TitleCard):
    LESSON = "Niches and distributions"
    TITLE = "Where It Can Live, Where It Is"


class S01Hook(SpokenScene):
    def construct(self):
        m = map_base(V0, label=False)
        self.play(FadeIn(m["base"]), run_time=0.3)
        ambient(self)
        icon = rosette(1.3).move_to([-3.4, 2.2, 0])
        icon_l = T("the dune plant", 34, GREEN, weight=BOLD).move_to([-3.4, 1.15, 0])
        dots = found_dots(V0, pocket=True)
        self.play(FadeIn(icon, scale=0.5), FadeIn(icon_l), LaggedStart(*[FadeIn(d, scale=0.4) for d in dots], lag_ratio=0.02), run_time=0.9)
        self.at("planted")
        patch_pos = [(3.45 + 0.3 * i, 0.9 + 0.3 * j) for j in range(3) for i in range(5)]
        pl = [rosette(0.24).move_to(V0.P(*p)) for p in patch_pos]
        self.play(LaggedStart(*[FadeIn(r, scale=0.3) for r in pl[:4]], lag_ratio=0.15), run_time=0.5)
        self.at("60")
        lab = tag("planted, about 60 km", 24, GREEN, V0.P(4.35, 2.62))
        lab2 = tag("beyond the edge", 24, GREEN, V0.P(4.35, 2.2))
        self.play(FadeIn(lab), FadeIn(lab2), run_time=0.7)
        self.at("northern edge")
        m["edge"].add(*[])
        ln = DashedLine(V0.P(coast_x(EDGE_Y) - 0.05, EDGE_Y), V0.P(MX1, EDGE_Y), color=TEXT, stroke_width=5, dash_length=0.2)
        el = tag("northern range edge", 24, TEXT, V0.P(4.75, EDGE_Y + 0.27))
        self.play(Create(ln), FadeIn(el), run_time=1.0)
        self.at("planted population")
        yrs = M("year 0", 40, TEXT).move_to([-3.4, -0.4, 0])
        self.add(yrs)
        for k in range(1, 5):
            pass
        cnt = ValueTracker(0)
        yrs.add_updater(lambda t: t.become(M(f"year {int(cnt.get_value())}", 40, TEXT).move_to([-3.4, -0.4, 0])))
        self.play(cnt.animate.set_value(12), LaggedStart(*[FadeIn(r, scale=0.3) for r in pl[4:]], lag_ratio=0.06),
                  run_time=1.0, rate_func=linear)
        yrs.clear_updaters()
        fin = M("12 to 14 years", 40, TEXT).move_to([-3.4, -0.4, 0])
        self.play(Transform(yrs, fin), run_time=0.3)
        self.at("more than tripled")
        tr = T("more than tripled", 38, GREEN, weight=BOLD).move_to([-3.4, -1.6, 0])
        self.play(FadeIn(tr, shift=UP * 0.2), Indicate(VGroup(*pl), color=GREEN, scale_factor=1.1), run_time=1.0)
        self.at("can live there")
        self.play(Indicate(VGroup(*pl), color=GREEN, scale_factor=1.15), run_time=1.0)
        self.at("never there")
        q = T("?", 64, TEXT, weight=BOLD).move_to(V0.P(2.7, 0.62))
        self.play(FadeIn(q, scale=0.4), run_time=0.5)
        self.play(Indicate(q, color=YELLOW, scale_factor=1.3), run_time=0.8)
        self.finish()


def carry_map(scene, dots=True, label=True):
    m = map_base(V0, label=label)
    parts = [m["base"], m["edge"]]
    d = found_dots(V0)
    if dots:
        parts.append(d)
    scene.add(*parts)
    ambient(scene)
    return m, d


class S02Two(SpokenScene):
    def construct(self):
        m, d = carry_map(self)
        self.at("keep two things apart")
        dv = divider()
        self.play(Create(dv), run_time=0.8)
        self.play(dv.animate.set_stroke(YELLOW, 7), rate_func=there_and_back, run_time=0.8)
        self.at("set of conditions")
        ax = left_axes()
        self.play(Create(ax[0]), Create(ax[1]), run_time=1.0)
        self.play(FadeIn(ax[2]), FadeIn(ax[3]), run_time=0.6)
        hc = header("conditions", -3.3, TEAL)
        self.play(Write(hc), run_time=0.8)
        self.at("the map of where")
        hm = header("map", 3.7, SAND)
        self.play(Write(hm), run_time=0.6)
        self.play(Indicate(d, color=DKG, scale_factor=1.08), run_time=1.2)
        self.finish()


def carry_split(scene, dots=False, label=True, pts=None):
    m = map_base(V0, label=label)
    scene.add(m["base"], m["edge"], divider(), left_axes(), header("conditions", -3.3, TEAL), header("map", 3.7, SAND))
    d = found_dots(V0)
    if dots:
        scene.add(d)
    ambient(scene)
    return m, d


class S03Axes(SpokenScene):
    def construct(self):
        m, d = carry_split(self, dots=True)
        self.play(FadeOut(d), FadeOut(m["edge"][1]), run_time=0.8)
        ax = left_axes()
        marks = [spot_marker(i) for i in range(len(SPOTS))]
        self.play(LaggedStart(*[FadeIn(k, scale=0.3) for k in marks], lag_ratio=0.25), run_time=2.6)
        self.at("temperature")
        self.play(Indicate(ax[2], color=YELLOW, scale_factor=1.15), run_time=0.9)
        self.at("soil moisture")
        self.play(Indicate(ax[3], color=YELLOW, scale_factor=1.15), run_time=0.9)
        self.at("sampled spot")
        self.play(LaggedStart(*[Indicate(k, color=YELLOW, scale_factor=1.6) for k in marks], lag_ratio=0.1), run_time=1.0)
        self.at("becomes a point")
        dots = []
        anims = []
        for p in POINTS:
            if p["spot"] == 4:
                continue
            dd = Dot(marks[p["spot"]].get_center(), radius=0.1, color=TEXT)
            dots.append(dd)
            anims.append(dd.animate.move_to(pt_pos(p)))
        self.add(*dots)
        self.play(LaggedStart(*anims, lag_ratio=0.08), run_time=1.3)
        nums = tag("21 °C, wet", 24, YELLOW, pt_pos(POINTS[0]) + RIGHT * 0.1 + UP * 0.55)
        self.play(FadeIn(nums), run_time=0.3)
        self.at("one place can give several")
        extra = [p for p in POINTS if p["spot"] == 4]
        ed = [Dot(marks[4].get_center(), radius=0.1, color=YELLOW) for _ in extra]
        self.add(*ed)
        self.play(FadeOut(nums), Indicate(marks[4], color=YELLOW, scale_factor=1.8),
                  LaggedStart(*[e.animate.move_to(pt_pos(p)) for e, p in zip(ed, extra)], lag_ratio=0.3), run_time=1.8)
        sch = T("schematic", 22, GREY).move_to([3.7, -3.55, 0])
        self.play(FadeIn(sch), run_time=0.4)
        self.finish()


def carry_points(scene, marks=True, color_mode=False):
    pts = left_points(color_mode)
    scene.add(pts)
    mk = None
    if marks:
        mk = VGroup(*[spot_marker(i) for i in range(len(SPOTS))])
        scene.add(mk)
    return pts, mk


class S04Lambda(SpokenScene):
    def construct(self):
        m, d = carry_split(self, label=False)
        pts, mk = carry_points(self)
        ring = Circle(radius=0.22, color=YELLOW, stroke_width=5).move_to(pt_pos(POINTS[[p["spot"] for p in POINTS].index(HI)]))
        ring2 = Circle(radius=0.22, color=YELLOW, stroke_width=5).move_to(mk[HI].get_center())
        self.at("ask one question")
        self.play(Create(ring), Create(ring2), run_time=0.8)
        panel = Rectangle(width=5.2, height=6.0, stroke_color=LAMC, stroke_width=4, fill_color=BG, fill_opacity=0.96).move_to([-3.3, 0.0, 0])
        left = [o for o in self.mobjects if (len(o.get_family()) > 1 or o.has_points()) and o.get_x() < -0.4]
        self.play(FadeIn(panel), run_time=0.8)
        self.remove(*left)
        self.add(panel)
        ros = [rosette(0.55).move_to([-5.0 + 0.72 * (i % 6) + 0.3, 1.7 - 1.0 * (i // 6), 0]) for i in range(12)]
        self.at("count a local population")
        self.play(LaggedStart(*[FadeIn(r, scale=0.3) for r in ros[:10]], lag_ratio=0.12), run_time=1.6)
        cnt = M("count: 10", 34, TEXT).move_to([-3.3, -0.35, 0])
        self.play(FadeIn(cnt), run_time=0.4)
        self.at("once a year")
        yr = M("year 1", 34, YELLOW).move_to([-3.3, 3.4, 0]).move_to([-3.3, 2.55, 0])
        self.play(FadeIn(yr), run_time=0.5)
        self.at("no newcomers")
        yr2 = M("year 2", 34, YELLOW).move_to(yr)
        cnt2 = M("count: 12", 34, TEXT).move_to(cnt)
        self.play(Transform(yr, yr2), Transform(cnt, cnt2), LaggedStart(*[FadeIn(r, scale=0.3) for r in ros[10:]], lag_ratio=0.5),
                  run_time=1.4)
        nn = T("no immigrants", 28, SINK).move_to([-3.3, -1.05, 0])
        self.play(FadeIn(nn), run_time=0.5)
        self.at("by what factor")
        q = T("× ?", 44, LAMC, weight=BOLD).move_to([-3.3, -1.9, 0])
        self.play(FadeIn(q, scale=0.5), FadeOut(nn), run_time=0.8)
        self.play(Indicate(cnt, color=LAMC), run_time=1.0)
        self.at("lambda")
        eq = VGroup(T("λ = next count / this count", 26, LAMC), M("12 / 10 = 1.2 (schematic)", 24, LAMC)).arrange(DOWN, buff=0.15).move_to([-3.3, -2.15, 0])
        self.play(FadeOut(q), FadeIn(eq), run_time=0.8)
        self.finish()


class S05Box(SpokenScene):
    def construct(self):
        m, d = carry_split(self, label=False)
        pts, mk = carry_points(self)
        base = -2.4
        unit = 1.8
        lam = [1.25, 0.75, 1.1, 0.9, 1.4, 0.7, 1.05, 1.3, 0.65, 1.2, 0.95, 1.5]
        left = [o for o in self.mobjects if (len(o.get_family()) > 1 or o.has_points()) and o.get_x() < -0.4]
        self.remove(*left)
        self.add(header("λ each year, one point", -3.3, LAMC, 30))
        x0 = -4.9
        bars = [Rectangle(width=0.28, height=l * unit, stroke_width=0, fill_color=LAMC, fill_opacity=0.9).move_to([x0 + 0.36 * i, base + l * unit / 2, 0]) for i, l in enumerate(lam)]
        one = DashedLine([-5.6, base + unit, 0], [-0.55, base + unit, 0], color=TEXT, stroke_width=4)
        onel = T("λ = 1", 26, TEXT).move_to([-6.1, base + unit, 0])
        floor = Line([-5.6, base, 0], [-0.55, base, 0], color=GREY, stroke_width=3)
        self.add(floor)
        self.play(Create(one), FadeIn(onel), run_time=0.8)
        self.play(LaggedStart(*[GrowFromEdge(b, DOWN) for b in bars], lag_ratio=0.28), run_time=3.2)
        self.at("long run")
        br = Brace(VGroup(*bars), UP, color=TEAL).shift(UP * 0.35)
        brl = T("long-run λ", 34, TEAL, weight=BOLD).next_to(br, UP, buff=0.12)
        gm = float(np.exp(np.mean(np.log(lam))))
        gl = DashedLine([-5.6, base + gm * unit, 0], [-0.55, base + gm * unit, 0], color=TEAL, stroke_width=5)
        self.play(GrowFromCenter(br), FadeIn(brl), run_time=1.0)
        self.at("good and bad years")
        self.play(Create(gl), *[Indicate(b, color=WHITE, scale_factor=1.05) for b in bars[::2]], run_time=1.6)
        self.at("one good summer")
        self.play(FadeOut(gl), bars[-1].animate.set_fill(YELLOW, 1), run_time=0.5)
        gl_ = T("one good year", 28, YELLOW).move_to([-2.0, 2.15, 0])
        self.play(FadeIn(gl_), Indicate(bars[-1], color=YELLOW, scale_factor=1.15), run_time=0.9)
        cx = VGroup(Line(UL, DR), Line(UR, DL)).scale(0.3).set_color(RED).set_stroke(width=8).move_to(bars[-1].get_top() + UP * 0.1)
        self.play(Create(cx), run_time=0.6)
        self.finish()


class S06Longrun(SpokenScene):
    def construct(self):
        m, d = carry_split(self, label=False)
        pts, mk = carry_points(self)
        hi = [p for p in POINTS if p["inside"]]
        self.at("long run")
        tg1 = tag("long-run λ ≥ 1", 24, TEAL, np.array([-3.2, 2.55, 0]))
        lo = [p for p in POINTS if not p["inside"]][0]
        tg2 = tag("λ < 1", 24, SINK, pt_pos(lo) + RIGHT * 0.9)
        self.play(FadeIn(tg1), FadeIn(tg2), run_time=0.8)
        self.at("at least one")
        self.play(*[pts[i].animate.set_color(TEAL).scale(1.3) for i, p in enumerate(POINTS) if p["inside"]],
                  *[pts[i].animate.set_color(SINK).set_opacity(0.35) for i, p in enumerate(POINTS) if not p["inside"]], run_time=1.6)
        self.at("the population replaces itself")
        self.play(FadeOut(tg1), FadeOut(tg2), *[Indicate(pts[i], color=TEAL, scale_factor=1.6) for i, p in enumerate(POINTS) if p["inside"]], run_time=1.6)
        self.at("drawn as a teal box")
        box = niche_box()
        self.play(Create(box), run_time=1.4)
        lab = VGroup(T("niche: long-run λ ≥ 1", 26, TEAL, weight=BOLD), T("without immigrants", 26, TEAL)).arrange(DOWN, buff=0.08).move_to([-3.2, 2.55, 0])
        self.play(FadeIn(lab, shift=DOWN * 0.1), run_time=0.8)
        self.play(box.animate.set_fill(TEAL, 0.3), run_time=1.0)
        self.finish()


def carry_niche(scene, dots=False, shading=True, label=True, edge_label=True):
    m, d = carry_split(scene, dots=dots, label=edge_label)
    pts = left_points(True)
    for i, p in enumerate(POINTS):
        if not p["inside"]:
            pts[i].set_opacity(0.35)
    box = niche_box()
    scene.add(pts, box)
    sh = None
    if shading:
        sh = shade(V0)
        scene.add(sh)
        scene.bring_to_back(sh)
        scene.bring_to_back(m["base"])
    return m, d, pts, box, sh


class S07Map(SpokenScene):
    def construct(self):
        m, d = carry_split(self, label=False)
        pts = left_points(True)
        for i, p in enumerate(POINTS):
            if not p["inside"]:
                pts[i].set_opacity(0.35)
        box = niche_box()
        self.add(pts, box)
        curve = ParametricFunction(lambda s: np.array([px(tprof(s)), py(mprof(s)), 0]), t_range=[MY0, MY1], color=GREY, stroke_width=3)
        trk = ValueTracker(MY0)
        mkr = Circle(radius=0.13, stroke_color=YELLOW, stroke_width=4, fill_color=BG, fill_opacity=1)
        mkr.add_updater(lambda o: o.move_to(V0.P(5.9, trk.get_value())))
        cd = Dot(radius=0.13, color=YELLOW)
        cd.add_updater(lambda o: o.move_to([px(tprof(trk.get_value())), py(mprof(trk.get_value())), 0]))
        links = Line(ORIGIN, RIGHT, color=YELLOW, stroke_width=2.5)
        links.add_updater(lambda o: o.put_start_and_end_on(cd.get_center(), mkr.get_center()))
        # shading slices
        slices = VGroup()
        ys = np.arange(MY0, MY1, 0.1)
        for y in ys:
            ok = inbox(tprof(y + 0.05), mprof(y + 0.05))
            p = land_poly(V0, y, y + 0.1, TEAL, 0.6 if ok else 0.0)
            p.ok = ok
            p.y = y
            p.add_updater(lambda o: o.set_fill(TEAL, 0.6 if (o.ok and o.y < trk.get_value()) else 0.0))
            slices.add(p)
        self.add(slices, m["edge"])
        self.at("turn to the map")
        self.play(FadeIn(curve), FadeIn(cd), FadeIn(mkr), FadeIn(links), run_time=0.8)
        self.at("shade every stretch")
        self.play(trk.animate.set_value(MY1), run_time=4.5, rate_func=linear)
        for o in (mkr, cd, links) + tuple(slices):
            o.clear_updaters()
        self.play(FadeOut(mkr), FadeOut(cd), FadeOut(links), run_time=0.4)
        self.at("that teal shading")
        lab = tag("could live here (schematic)", 24, TEAL, V0.P(4.7, 1.45))
        self.play(FadeIn(lab), run_time=0.7)
        self.play(Indicate(slices, color=TEAL, scale_factor=1.03), run_time=1.2)
        self.finish()


class S08Dots(SpokenScene):
    def construct(self):
        m, d, pts, box, sh = carry_niche(self)
        dots = found_dots(V0)
        self.at("places where")
        self.play(LaggedStart(*[FadeIn(x, scale=0.3) for x in dots], lag_ratio=0.04), run_time=3.0)
        self.at("do not match")
        b1 = Rectangle(width=3.9, height=1.5, stroke_color=YELLOW, stroke_width=6).move_to(V0.P(4.4, 0.95))
        b2 = Rectangle(width=2.6, height=0.95, stroke_color=YELLOW, stroke_width=6).move_to(V0.P(4.4, -1.45))
        self.play(Create(b1), Create(b2), run_time=1.2)
        self.play(Indicate(b1, color=YELLOW), Indicate(b2, color=YELLOW), run_time=1.0)
        self.finish()


class S09Empty(SpokenScene):
    def construct(self):
        m, d, pts, box, sh = carry_niche(self, edge_label=False)
        dots = found_dots(V0)
        self.add(dots)
        b1 = Rectangle(width=3.9, height=1.5, stroke_color=YELLOW, stroke_width=6).move_to(V0.P(4.4, 0.95))
        self.add(b1)
        self.at("picture a teal stretch")
        self.play(dots.animate.set_opacity(0.3), Indicate(b1, color=YELLOW, scale_factor=1.05), run_time=1.0)
        self.play(b1.animate.scale(1.08), rate_func=there_and_back, run_time=1.0)
        self.at("its conditions are inside")
        t1 = tag("inside the niche", 30, TEAL, V0.P(4.4, 1.5))
        pp = Dot(pt_pos(POINTS[[p["spot"] for p in POINTS].index(8)]), radius=0.17, color=YELLOW)
        self.play(FadeIn(t1), FadeIn(pp), Indicate(box, color=TEAL, scale_factor=1.05), run_time=1.2)
        self.at("nothing has arrived")
        t2 = tag("N = 0, no immigrants", 28, TEXT, V0.P(4.4, 0.75))
        sc = T("schematic", 22, GREY).move_to([5.6, -3.55, 0])
        ar = DashedLine(V0.P(4.0, -0.8), V0.P(4.0, 0.0), color=DKG, stroke_width=5)
        ar.add_tip(tip_length=0.2)
        self.play(FadeIn(t2), FadeIn(sc), run_time=0.8)
        self.play(Create(ar), run_time=1.2)
        self.play(FadeOut(ar[-1]), run_time=0.4)
        self.finish()


class S10Rule(SpokenScene):
    def construct(self):
        m, d, pts, box, sh = carry_niche(self)
        dots = found_dots(V0)
        dots.set_opacity(0.45)
        self.add(dots)
        t = tag("inside the niche", 28, TEAL, V0.P(4.4, 1.55))
        self.add(t)
        self.at("absence alone")
        ban = VGroup(T("missing ≠", 32, TEXT, weight=BOLD), T("outside the niche", 32, TEXT, weight=BOLD)).arrange(DOWN, buff=0.1)
        ban = VGroup(BackgroundRectangle(ban, color=BG, fill_opacity=0.9, buff=0.18), ban).move_to(V0.P(4.4, 1.6))
        self.play(FadeOut(t), FadeIn(ban), run_time=1.0)
        self.at("edge of a niche")
        self.play(m["edge"][0].animate.set_stroke(YELLOW, 10), run_time=0.8)
        self.at("a species can be missing")
        br = Brace(Line(V0.P(6.45, 0.25), V0.P(6.45, 1.75)), RIGHT, color=TEAL, buff=0.0)
        self.play(m["edge"][0].animate.set_stroke(TEXT, 5), GrowFromCenter(br), run_time=1.0)
        self.at("because it never got there")
        self.play(Indicate(ban, color=YELLOW, scale_factor=1.06), run_time=1.2)
        self.play(Indicate(sh, color=TEAL, scale_factor=1.02), run_time=1.2)
        self.finish()


def zoom_world(scene, grey_pocket=False):
    mz = map_base(VZ)
    sh = shade(VZ)
    scene.add(mz["base"], sh)
    found = found_dots(VZ, pocket=False, r=0.14)
    scene.add(found)
    pocket = VGroup(*[Dot(VZ.P(x, y), radius=0.15, color=SINK if grey_pocket else DKG).set_stroke(TEXT, 1.2, 0.9) for x, y in POCKET])
    scene.add(pocket)
    box = Rectangle(width=4.2, height=1.55, stroke_color=YELLOW, stroke_width=6).move_to(VZ.P(4.45, -1.45))
    scene.add(box)
    clock = ValueTracker(0)
    clock.add_updater(lambda o, dt: o.increment_value(dt))
    scene.add(clock)
    box.add_updater(lambda o: o.set_fill(YELLOW, 0.09 + 0.09 * np.sin(2.2 * clock.get_value())))
    return mz, sh, found, pocket, box


def clipboard():
    board = RoundedRectangle(corner_radius=0.15, width=4.6, height=4.3, stroke_color=TEXT, stroke_width=4, fill_color=BG, fill_opacity=1).move_to([-3.3, 0.9, 0])
    rows = VGroup(*[T(f"survey {i + 1}", 28, TEXT).move_to([-4.5, 2.5 - 0.62 * i, 0]).set_x(-4.5, ) for i in range(6)])
    for r in rows:
        r.align_to([-5.4, 0, 0], LEFT)
    return board, rows


class S11Predict(SpokenScene):
    def construct(self):
        mz, sh, found, pocket, box = zoom_world(self)
        board, rows = clipboard()
        self.at("the other mismatch")
        self.play(Indicate(box, color=YELLOW, scale_factor=1.04), FadeIn(board), run_time=1.0)
        self.add(rows)
        self.at("a plant turns up")
        stamps = []
        for i, r in enumerate(rows):
            s = T("present", 28, GREEN, weight=BOLD).move_to([-2.0, r.get_y(), 0])
            stamps.append(s)
        self.play(LaggedStart(*[FadeIn(r, shift=RIGHT * 0.1) for r in rows], lag_ratio=0.15), run_time=1.0)
        self.at("every survey")
        self.play(LaggedStart(*[FadeIn(s, scale=1.6) for s in stamps[:3]], lag_ratio=0.5), run_time=1.8)
        self.at("year after year")
        self.play(LaggedStart(*[FadeIn(s, scale=1.6) for s in stamps[3:]], lag_ratio=0.5), run_time=1.6)
        self.at("is that site inside")
        q = chip("Inside the niche?", YELLOW, 38)
        q.move_to([-3.3, -2.0, 0])
        self.play(FadeIn(q, scale=0.7), run_time=0.8)
        self.play(Indicate(box, color=YELLOW, scale_factor=1.06), run_time=0.8)
        self.finish()


class S12Pause(NarratedScene):
    def construct(self):
        mz, sh, found, pocket, box = zoom_world(self)
        board, rows = clipboard()
        stamps = [T("present", 28, GREEN, weight=BOLD).move_to([-2.0, r.get_y(), 0]) for r in rows]
        q = chip("Inside the niche?", YELLOW, 38).move_to([-3.3, -2.0, 0])
        self.add(board, rows, *stamps, q)
        trk = ValueTracker(1.0)
        ring = always_redraw(lambda: Arc(radius=0.55, start_angle=PI / 2, angle=-TAU * trk.get_value(), color=YELLOW, stroke_width=8).move_to([-0.8, -2.0, 0]))
        self.add(ring)
        self.play(trk.animate.set_value(0.001), run_time=max(1.0, self.narration_s - 0.2), rate_func=linear)
        self.finish()


class S13Reveal(SpokenScene):
    def construct(self):
        mz, sh, found, pocket, box = zoom_world(self)
        frame = Rectangle(width=4.0, height=4.9, stroke_color=GREY, stroke_width=3).move_to([-3.4, -0.3, 0])
        base = -2.5
        unit = 2.0
        bar = Rectangle(width=1.6, height=unit, stroke_width=0, fill_color=LAMC, fill_opacity=0.9).move_to([-3.4, base + unit / 2, 0])
        one = DashedLine([-5.2, base + unit, 0], [-1.6, base + unit, 0], color=TEXT, stroke_width=4)
        onel = T("λ = 1", 26, TEXT).move_to([-4.6, base + unit + 0.3, 0])
        gl = T("this site's λ", 28, LAMC).move_to([-3.4, 3.4, 0])
        self.play(FadeIn(frame), FadeIn(bar), Create(one), FadeIn(onel), FadeIn(gl), run_time=1.0)
        self.at("not necessarily")
        self.play(Indicate(pocket, color=YELLOW, scale_factor=1.1), run_time=1.2)
        self.at("deaths outnumber")
        dt = T("deaths > births", 30, RED, weight=BOLD).move_to([-3.4, 2.5, 0])
        self.play(FadeIn(dt), pocket.animate.set_color(SINK), run_time=0.9)
        gone = [pocket[1], pocket[4], pocket[8], pocket[10]]
        self.play(*[FadeOut(g, scale=0.3) for g in gone], run_time=1.0)
        self.at("lambda")
        nh = 0.8 * unit
        t1 = T("λ < 1", 34, BG, weight=BOLD).move_to([-3.4, base + nh / 2, 0])
        self.play(bar.animate.stretch_to_fit_height(nh).move_to([-3.4, base + nh / 2, 0]), FadeIn(t1), run_time=1.2)
        self.at("seeds arriving")
        neigh = [d for d in found if VZ.P(5, 0)[1] and d.get_y() > 0.5 and 2.0 < d.get_x() < 6.5]
        neigh = sorted(neigh, key=lambda d: d.get_x())
        sel = [neigh[i] for i in np.linspace(0, len(neigh) - 1, 4).astype(int)]
        targets = [pocket[1].get_center(), pocket[4].get_center(), pocket[8].get_center(), pocket[10].get_center()]
        arrows = [Arrow(s.get_center() + DOWN * 0.15, t + UP * 0.2, buff=0.1, color=BLUE, stroke_width=6) for s, t in zip(sel, targets)]
        self.play(LaggedStart(*[GrowArrow(a) for a in arrows], lag_ratio=0.3), run_time=1.6)
        self.at("replace the dead")
        seeds = [Dot(a.get_start(), radius=0.1, color=BLUE) for a in arrows]
        self.add(*seeds)
        self.play(*[sd.animate.move_to(t) for sd, t in zip(seeds, targets)], run_time=1.4)
        newp = [Dot(t, radius=0.15, color=SINK).set_stroke(TEXT, 1.2, 0.9) for t in targets]
        self.play(*[FadeOut(sd) for sd in seeds], *[FadeIn(n, scale=0.4) for n in newp], run_time=0.8)
        self.play(*[Indicate(a, color=BLUE, scale_factor=1.15) for a in arrows], run_time=1.2)
        self.finish()


class S14Cut(SpokenScene):
    def construct(self):
        mz, sh, found, pocket, box = zoom_world(self, grey_pocket=True)
        frame = Rectangle(width=4.0, height=4.9, stroke_color=GREY, stroke_width=3).move_to([-3.4, -0.3, 0])
        base, unit, nh = -2.5, 2.0, 1.6
        bar = Rectangle(width=1.6, height=nh, stroke_width=0, fill_color=LAMC, fill_opacity=0.9).move_to([-3.4, base + nh / 2, 0])
        one = DashedLine([-5.2, base + unit, 0], [-1.6, base + unit, 0], color=TEXT, stroke_width=4)
        onel = T("λ = 1", 26, TEXT).move_to([-4.6, base + unit + 0.3, 0])
        t1 = T("λ < 1", 34, BG, weight=BOLD).move_to([-3.4, base + nh / 2, 0])
        neigh = sorted([d for d in found if d.get_y() > 0.5], key=lambda d: d.get_x())
        sel = [neigh[i] for i in np.linspace(0, len(neigh) - 1, 4).astype(int)]
        arrows = [Arrow(s.get_center() + DOWN * 0.15, pocket[j].get_center() + UP * 0.2, buff=0.1, color=BLUE, stroke_width=6)
                  for s, j in zip(sel, (1, 4, 8, 10))]
        self.add(frame, bar, one, onel, t1, *arrows)
        sc = VGroup(Line(ORIGIN, UR * 0.6, color=TEXT, stroke_width=7), Line(ORIGIN, DR * 0.6, color=TEXT, stroke_width=7),
                    Circle(radius=0.14, color=TEXT).shift(UL * 0.15), Circle(radius=0.14, color=TEXT).shift(DL * 0.15)).scale(1.4)
        sc.move_to(arrows[0].get_center() + LEFT * 2.5 + UP * 0.6)
        self.at("cut off")
        yrs = M("year 1", 34, YELLOW).move_to([3.6, 2.7, 0])
        self.play(FadeIn(sc), FadeIn(yrs), run_time=0.5)
        self.play(sc.animate.move_to(arrows[1].get_center() + UP * 0.1), run_time=0.7)
        self.play(sc[0].animate.rotate(0.35, about_point=sc.get_center()), sc[1].animate.rotate(-0.35, about_point=sc.get_center()), rate_func=there_and_back, run_time=0.4)
        self.play(*[FadeOut(a, shift=DOWN * 0.1) for a in arrows], FadeOut(sc), run_time=0.7)
        self.at("the plants dwindle")
        cnt = ValueTracker(1)
        yrs.add_updater(lambda t: t.become(M(f"year {int(cnt.get_value())}", 34, YELLOW).move_to([3.6, 2.7, 0])))
        order = list(pocket)
        self.play(cnt.animate.set_value(5), LaggedStart(*[FadeOut(p, scale=0.3) for p in order], lag_ratio=0.2), run_time=2.4, rate_func=linear)
        yrs.clear_updaters()
        self.at("called a sink")
        lab = VGroup(T("sink: λ < 1,", 32, SINK, weight=BOLD), T("kept going by immigrants", 28, SINK)).arrange(DOWN, buff=0.1).move_to([-3.4, 2.7, 0])
        self.play(FadeIn(lab), Indicate(box, color=YELLOW), run_time=1.2)
        self.finish()


def full_world(scene, edge_label=True):
    m, d, pts, box, sh = carry_niche(scene, edge_label=edge_label)
    dots = found_dots(V0, pocket=False)
    pocket = VGroup(*[Dot(V0.P(x, y), radius=0.07, color=SINK).set_stroke(TEXT, 1.2, 0.9) for x, y in POCKET])
    scene.add(dots, pocket)
    return m, d, pts, box, sh, dots, pocket


def imm_arrows(v=V0):
    ar = VGroup()
    for xa, xb in ((3.9, 3.9), (4.5, 4.4), (5.0, 4.9)):
        ar.add(Arrow(v.P(xa, -0.75), v.P(xb, -1.35), buff=0, color=BLUE, stroke_width=5, tip_length=0.15))
    return ar


class S15Presence(SpokenScene):
    def construct(self):
        m, d, pts, box, sh, dots, pocket = full_world(self)
        self.add(header("conditions", -3.3, TEAL), header("map", 3.7, SAND))
        ar = imm_arrows()
        self.at("presence alone")
        t1 = tag("not yet reached", 26, YELLOW, V0.P(4.4, 1.2))
        t2 = tag("held by immigrants", 24, BLUE, V0.P(4.4, -2.0))
        self.play(FadeIn(t1), FadeIn(t2), FadeIn(ar), run_time=1.0)
        self.play(Indicate(pocket, color=SINK, scale_factor=1.2), run_time=1.0)
        self.at("a map shows only")
        hm = T("map alone: found / not found", 26, SAND, weight=BOLD).move_to([3.7, 3.4, 0])
        old = [o for o in self.mobjects if isinstance(o, Text) and abs(o.get_y() - 3.4) < 0.1 and o.get_x() > 0]
        self.play(*[FadeOut(o) for o in old], run_time=0.4)
        self.play(FadeOut(sh), FadeOut(ar), FadeOut(t1), FadeOut(t2),
                  pocket.animate.set_color(DKG), FadeIn(hm), run_time=1.0)
        self.play(Indicate(VGroup(dots, pocket), color=DKG, scale_factor=1.05), run_time=1.5)
        self.at("spotting sinks")
        hn = T("needs counts and movement data", 24, BLUE, weight=BOLD).move_to([3.7, 3.4, 0])
        tg = tag("λ < 1", 26, SINK, V0.P(2.7, -1.45))
        self.play(FadeIn(sh), FadeIn(ar), pocket.animate.set_color(SINK), FadeOut(hm), FadeIn(hn), FadeIn(tg), run_time=1.4)
        self.play(Indicate(ar, color=BLUE, scale_factor=1.15), run_time=1.0)
        self.finish()


class S16Others(SpokenScene):
    def construct(self):
        m, d = carry_split(self, label=False)
        pts = left_points(True)
        for i, p in enumerate(POINTS):
            if not p["inside"]:
                pts[i].set_opacity(0.35)
        box = niche_box()
        self.add(pts, box)
        self.at("other species change")
        self.play(Indicate(box, color=TEAL, scale_factor=1.03), run_time=1.2)
        self.at("a competitor or an enemy")
        tf = tuft(0.7).move_to([-0.8, 1.0, 0])
        tl = T("competitor / enemy", 24, ORANGE).move_to([-2.4, 2.45, 0])
        self.play(FadeIn(tf, shift=LEFT * 0.4), FadeIn(tl), run_time=1.0)
        x0, x1, y0, y1 = px(BOX_T[0]), px(BOX_T[1]), py(BOX_M[0]), py(BOX_M[1])
        shrunk = Rectangle(width=(x1 - x0) - 0.9, height=y1 - y0, stroke_color=TEAL, stroke_width=6, fill_color=TEAL, fill_opacity=0.3).move_to([(x0 + x1) / 2 - 0.45, (y0 + y1) / 2, 0])
        self.at("push it down")
        dn = Arrow([-0.8, 0.4, 0], [-0.8, -0.9, 0], color=ORANGE, buff=0, stroke_width=7)
        dl = T("λ down", 26, ORANGE, weight=BOLD).move_to([-0.9, -1.35, 0])
        self.play(Transform(box, shrunk), GrowArrow(dn), FadeIn(dl), run_time=1.4)
        self.play(FadeOut(tf), FadeOut(tl), FadeOut(dn), FadeOut(dl), run_time=0.5)
        self.at("a helper")
        sb = shrub(0.9).move_to([-0.8, 0.3, 0])
        sl = T("helper", 26, SHRUB).move_to([-0.8, -0.45, 0])
        self.play(FadeIn(sb, shift=RIGHT * 0.3), FadeIn(sl), run_time=0.9)
        grown = Rectangle(width=(x1 - x0) - 0.9, height=(y1 - y0) + 0.9, stroke_color=TEAL, stroke_width=6, fill_color=TEAL, fill_opacity=0.3).move_to([(x0 + x1) / 2 - 0.45, (y0 + y1) / 2 + 0.45, 0])
        self.at("push it up")
        up = Arrow([-0.8, 0.9, 0], [-0.8, 2.0, 0], color=SHRUB, buff=0, stroke_width=7)
        ul = T("λ up", 26, SHRUB, weight=BOLD).move_to([-0.8, 2.4, 0])
        self.play(Transform(box, grown), GrowArrow(up), FadeIn(ul), run_time=1.4)
        sch = T("shapes schematic", 22, GREY).move_to([-3.3, -3.55, 0])
        self.play(FadeIn(sch), run_time=0.4)
        self.finish()


class S17Back(SpokenScene):
    def construct(self):
        m = map_base(V0, label=True)
        dots = found_dots(V0)
        self.add(m["base"], m["edge"], dots)
        ambient(self)
        icon = rosette(1.3).move_to([-3.4, 2.2, 0])
        icon_l = T("the dune plant", 34, GREEN, weight=BOLD).move_to([-3.4, 1.15, 0])
        self.at("back to the dune plant")
        self.play(FadeIn(icon, scale=0.5), FadeIn(icon_l), run_time=0.9)
        self.at("its planted population")
        patch_pos = [(3.45 + 0.3 * i, 0.9 + 0.3 * j) for j in range(3) for i in range(5)]
        pl = [rosette(0.24).move_to(V0.P(*p)) for p in patch_pos]
        self.play(LaggedStart(*[FadeIn(r, scale=0.3) for r in pl[:4]], lag_ratio=0.2), run_time=0.8)
        self.at("grew past the edge")
        self.play(LaggedStart(*[FadeIn(r, scale=0.3) for r in pl[4:]], lag_ratio=0.15), run_time=2.0)
        self.at("so at least at that site")
        lab = VGroup(T("this planted population", 32, GREEN), T("persisted beyond the edge", 32, GREEN)).arrange(DOWN, buff=0.12).move_to([-3.4, -0.5, 0])
        self.play(FadeIn(lab, shift=UP * 0.2), run_time=1.0)
        self.at("the edge is not")
        self.play(m["edge"][0].animate.set_stroke(YELLOW, 9), Indicate(VGroup(*pl), color=GREEN, scale_factor=1.1), run_time=1.4)
        self.play(m["edge"][0].animate.set_stroke(TEXT, 5), run_time=0.6)
        self.finish()


class S18Takehome(SpokenScene):
    def construct(self):
        m, d, pts, box, sh = carry_niche(self)
        dots = found_dots(V0, pocket=False)
        pocket = VGroup(*[Dot(V0.P(x, y), radius=0.07, color=SINK).set_stroke(TEXT, 1.2, 0.9) for x, y in POCKET])
        ar = imm_arrows()
        self.add(dots, pocket, ar, header("conditions", -3.3, TEAL), header("map", 3.7, SAND))
        world = VGroup(*self.mobjects)
        self.play(world.animate.scale(0.8, about_point=[0, 1.0, 0]), run_time=1.2)
        for w in self._rip:
            w.lo, w.hi, w.k = 1.0 + 0.8 * (MY0 - 1.0), 1.0 + 0.8 * (MY1 - 1.0), 0.8
        self.at("a niche is where")
        c1 = VGroup(T("niche: long-run λ ≥ 1", 28, TEAL, weight=BOLD), T("without immigrants", 28, TEAL)).arrange(DOWN, buff=0.08).move_to([-3.0, -3.25, 0])
        self.play(FadeIn(c1, shift=UP * 0.1), Indicate(box, color=TEAL, scale_factor=1.05), run_time=1.2)
        self.at("a map shows only")
        c2 = VGroup(T("map: shows only", 28, SAND, weight=BOLD), T("where it is found", 28, SAND)).arrange(DOWN, buff=0.08).move_to([3.1, -3.25, 0])
        self.play(FadeIn(c2, shift=UP * 0.1), Indicate(dots, color=DKG, scale_factor=1.05), run_time=1.2)
        self.finish()


class S19End(EndCard):
    LINE = "A niche: conditions where long-run λ is at least 1 without immigrants."
