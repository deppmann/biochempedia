"""Adaptive immunity, chapter 2: Why Is the Second Time Faster?

Same look as chapter 1 (../scenes.py). COLOUR MAP (shared by both films): V BLUE, D GREEN, J ORANGE; ordinary
lymphocytes GREY; the selected clone GOLD; memory cells GOLD with a dark outline; antibody PURPLE; antigen a
small RED spiky shape. New here: a dashed pale line (drawn pale because the ground is dark) marks 'enough cells'.
One world for the middle of the film: a log-scale graph (days along the bottom, fitting cells up the side),
rebuilt at the same place in every scene that continues it.
"""
import math
import random
from bp_style import *  # noqa: F401,F403

ORANGE = "#F29E4C"
PURPLE = "#B58CD9"
LIGHT = "#C9CED8"
DARK = "#2A1D05"
PALE = "#E8ECF4"
LG2 = math.log10(2)

# receptor tip shapes: (sides, start angle); 0 sides = circle  (as in chapter 1)
TIPS = [(3, math.pi / 2), (4, math.pi / 4), (5, math.pi / 2), (6, 0), (0, 0), (3, -math.pi / 2), (4, 0)]
MATCH = 2


def bob(m, amp=0.05, speed=1.3, phase=None):
    m._bt = 0.0
    m._bo = np.zeros(3)
    ph = random.random() * 6.28 if phase is None else phase

    def up(mm, dt):
        mm._bt += dt
        o = np.array([amp * 0.6 * math.sin(mm._bt * speed * 0.8 + ph), amp * math.sin(mm._bt * speed + ph * 1.7), 0])
        mm.shift(o - mm._bo)
        mm._bo = o
    m.add_updater(up)
    return m


def tip_mob(k, size, color=LIGHT, fill=0.45):
    n, a = TIPS[k % len(TIPS)]
    m = Circle(radius=size * 0.85) if n == 0 else RegularPolygon(n=n, radius=size, start_angle=a)
    return m.set_stroke(color, 4).set_fill(color, fill)


class Cell(VGroup):
    def __init__(self, x, y, k, r=0.65, color=GREY):
        super().__init__()
        self.r, self.k = r, k
        self.body = Circle(radius=r).set_stroke(color, 4).set_fill(color, 0.28).move_to([x, y, 0])
        top = self.body.get_center() + UP * r
        self.stalk = Line(top, top + UP * r * 0.45).set_stroke(color, 4)
        self.tip = tip_mob(k, r * 0.5, LIGHT if color == GREY else color).move_to(top + UP * (r * 0.45 + r * 0.42))
        self.add(self.body, self.stalk, self.tip)

    def gold(self):
        return AnimationGroup(self.body.animate.set_stroke(GOLD, 5).set_fill(GOLD, 0.55),
                              self.stalk.animate.set_stroke(GOLD, 5), self.tip.animate.set_stroke(GOLD, 5).set_fill(GOLD, 0.8))


class Antigen(VGroup):
    def __init__(self, R=0.5, tab=0.3, k=MATCH):
        super().__init__()
        self.star = Star(n=7, outer_radius=R, inner_radius=R * 0.62, color=RED).set_fill(RED, 0.75).set_stroke(RED, 3)
        self.tab = tip_mob(k, tab, RED, 0.9).move_to(self.star.get_center() + DOWN * (R + tab * 0.2))
        self.add(self.tab, self.star)
        self.set_z_index(3)


def goto_tip(ant, tip, gap=0.0):
    return tip.get_center() + UP * gap - ant.tab.get_center()


K = 1.3


def lab(text, size=30, color=TEXT, **kw):
    return T(text, size=size * K, color=color, **kw)


def bk(m, pad=0.07, op=0.92):
    """Put m on a ground-coloured pad so a grid line never runs through its letters."""
    return VGroup(BackgroundRectangle(m, color=BG, fill_opacity=op, buff=pad, stroke_width=0), m)


def chp(text, color=BLUE, size=26):
    return chip(text, color, size * K)


def sup(base, exp, size=40, color=TEXT):
    b = T(base, size=size, color=color)
    e = T(exp, size=size * 0.62, color=color)
    e.next_to(b, RIGHT, buff=0.04).shift(UP * b.height * 0.5)
    return VGroup(b, e)


def mem_cell(p, r=0.15):
    return VGroup(Circle(radius=r).set_stroke(DARK, 4).set_fill(GOLD, 0.95),
                  Circle(radius=r * 0.5).set_stroke(DARK, 3).set_fill(DARK, 0.0)).move_to(p)


# ---------------------------------------------------------------- cell clusters (scenes 1-4)
C0 = np.array([-3.0, -0.2, 0.0])


def n_pos(N, C=C0):
    if N == 1:
        return [C.copy()]
    c = min(0.6, 2.8 / math.sqrt(N))
    out = []
    for i in range(N):
        rad = c * math.sqrt(i + 0.5)
        ang = i * 2.39996
        out.append(C + np.array([rad * math.cos(ang), rad * math.sin(ang), 0]))
    return out


def n_rad(N):
    if N == 1:
        return 0.65
    return 0.72 * min(0.6, 2.8 / math.sqrt(N))


def gold_disc(p, r):
    return Circle(radius=r).set_stroke(GOLD, 3).set_fill(GOLD, 0.55).move_to(p)


def make_cluster(N, C=C0):
    ps, r = n_pos(N, C), n_rad(N)
    return [gold_disc(p, r) for p in ps]


def double_round(scene, cells, C=C0, run=1.1):
    """Every cell divides in two: returns the new list of 2N cells."""
    N2 = len(cells) * 2
    ps, r = n_pos(N2, C), n_rad(N2)
    anims, new = [], []
    for i, c in enumerate(cells):
        d = c.copy()
        scene.add(d)
        anims.append(Transform(c, gold_disc(ps[2 * i], r)))
        anims.append(Transform(d, gold_disc(ps[2 * i + 1], r)))
        new += [c, d]
    scene.play(*anims, run_time=run)
    return new


def counter(N, x=3.4, y=1.2):
    big = M(f"{N}", 76, GOLD, weight=BOLD)
    small = lab("cells", 30)
    small.next_to(big, DOWN, buff=0.15)
    return VGroup(big, small).move_to([x, y, 0])


# ---------------------------------------------------------------- the log graph (scenes 5-12)
X0, DX = -4.6, 0.32       # screen x of day 0, per day
Y10, DY = -2.7, 0.9       # screen y of the "10 cells" gridline, per factor of ten
LAG, DT = 1.0, 0.5        # days of lag, days per doubling (illustrative)
L_START, L_ENOUGH, L_MEM = 2.0, 7.0, 5.0
T_CROSS = LAG + DT * (L_ENOUGH - L_START) / LG2
T_PK = T_CROSS + 0.6
L_PK = L_START + (T_PK - LAG) / DT * LG2
T2S = 20.0
T_SEC_X = T2S + LAG + DT * (L_ENOUGH - L_MEM) / LG2
T_GH_X = T2S + LAG + DT * (L_ENOUGH - L_START) / LG2


def Pt(t, L):
    return np.array([X0 + DX * t, Y10 + DY * (L - 1), 0.0])


def L_primary(t):
    if t < LAG:
        return L_START
    if t <= T_PK:
        return L_START + (t - LAG) / DT * LG2
    n = 1e5 + (10 ** L_PK - 1e5) * math.exp(-(t - T_PK) / 0.9)
    return math.log10(n)


def L_sec(t):
    return L_MEM if t < T2S + LAG else L_MEM + (t - T2S - LAG) / DT * LG2


def L_ghost(t):
    return L_START if t < T2S + LAG else L_START + (t - T2S - LAG) / DT * LG2


def curve(f, t0, t1, color=GOLD, w=9):
    n = max(8, int(45 * (t1 - t0)))
    pts = [Pt(t, f(t)) for t in np.linspace(t0, t1, n)]
    return VMobject().set_points_as_corners(pts).set_stroke(color, w)


def axes_parts():
    xax = Line(Pt(0, 0.55), Pt(35, 0.55)).set_stroke(LIGHT, 3)
    yax = Line(Pt(0, 0.55), Pt(0, 7.55)).set_stroke(LIGHT, 3)
    grid = VGroup(*[Line(Pt(0, L), Pt(35, L)).set_stroke(LIGHT, 3, opacity=0.45) for L in range(1, 8)])
    names = ["10", "100", "1,000", "10,000", "100,000", "1,000,000", "10,000,000"]
    ylab = VGroup(*[M(nm, 22, LIGHT) for nm in names])
    for lb, L in zip(ylab, range(1, 8)):
        lb.move_to(Pt(0, L) + LEFT * (0.12 + lb.width / 2))
    xlab = VGroup(*[M(str(d), 22, LIGHT).move_to(Pt(d, 0.55) + DOWN * 0.3) for d in range(0, 36, 7)])
    xt = lab("days", 24, TEXT).move_to([-5.7, -3.5, 0])
    yt = lab("fitting cells (schematic)", 26, TEXT).move_to([-2.4, 3.55, 0])
    return xax, yax, grid, ylab, xlab, xt, yt


def enough_parts():
    ln = DashedLine(Pt(0, L_ENOUGH), Pt(35, L_ENOUGH), dash_length=0.22).set_stroke(PALE, 4)
    tx = lab("enough cells", 24, PALE).move_to([-3.15, 2.97, 0])
    return ln, tx


def graph_base(scene):
    xax, yax, grid, ylab, xlab, xt, yt = axes_parts()
    ln, tx = enough_parts()
    scene.add(grid, xax, yax, ylab, xlab, xt, yt, ln, tx)


def mem_dots(ts=(16.0, 16.8, 17.6, 18.4, 19.2, 20.0)):
    return VGroup(*[mem_cell(Pt(t, L_MEM), 0.15) for t in ts])


def tracer(path, period=4.0, color=PALE, r=0.09):
    d = Dot(radius=r, color=color).set_z_index(5)
    d._t = random.random() * period
    d.move_to(path.point_from_proportion(0))

    def up(m, dt):
        m._t += dt
        m.move_to(path.point_from_proportion((m._t / period) % 1.0))
    d.add_updater(up)
    return d


def comet(path, period=3.0, color=YELLOW, frac=0.22, w=26, op=0.85):
    """A soft glowing stretch that slides along a curve: slow ambient motion for a held graph."""
    g = VMobject().set_stroke(color, w, opacity=op).set_z_index(4)
    g._t = random.random() * period

    def up(m, dt):
        m._t += dt
        a = (m._t / period) % 1.0
        m.pointwise_become_partial(path, max(0.0, a - frac), a)
        m.set_stroke(color, w, opacity=op)
    g.add_updater(up)
    return g


def primary_climb_label(text="primary response", pos=(-1.55, 0.2)):
    if text == "primary response":
        a = lab("primary", 24, GOLD)
        b = lab("response", 24, GOLD)
        return bk(VGroup(a, b).arrange(DOWN, buff=0.05).move_to([pos[0], pos[1], 0]), 0.05, 0.95)
    return bk(lab(text, 24, GOLD).move_to([-1.55, 0.3, 0]), 0.05, 0.95)


# ---------------------------------------------------------------- mice (scenes 13-16)
MX = {"L": -3.55, "R": 3.55}
MY = -0.1
MBODY = "#2b303d"


class Mouse(VGroup):
    def __init__(self, side):
        super().__init__()
        cx, cy = MX[side], MY
        d = -1 if side == "L" else 1
        self.body = Ellipse(width=5.9, height=3.9).set_stroke(LIGHT, 4).set_fill(MBODY, 1).move_to([cx, cy, 0])
        ears = VGroup(*[Circle(radius=0.55).set_stroke(LIGHT, 4).set_fill(MBODY, 1).move_to([cx + dx, cy + 1.7, 0]) for dx in (d * 1.6, d * 0.5)])
        nose = Circle(radius=0.15).set_stroke(RED, 3).set_fill(RED, 0.5).move_to([cx + d * 2.95, cy + 0.1, 0])
        eye = Dot(radius=0.1, color=TEXT).move_to([cx + d * 2.45, cy + 0.5, 0])
        tail = ArcBetweenPoints(np.array([cx - d * 2.85, cy - 0.4, 0]), np.array([cx - d * 3.35, cy + 0.2, 0]), angle=1.2).set_stroke(LIGHT, 4)
        self.add(ears, self.body, nose, eye, tail)


def two_lines(a, b, side, size=24, color=TEXT, y=3.3):
    g = VGroup(lab(a, size, color), lab(b, size, color)).arrange(DOWN, buff=0.06)
    return g.move_to([MX[side], y, 0])


def left_label():
    return two_lines("gets viral protein", "(vaccine)", "L")


def right_label():
    return two_lines("gets antibody from", "an immunized mouse", "R")


def mem_group(side, k=4, bobbing=True):
    cx = MX[side]
    ps = [(-0.8, 0.35), (0.6, 0.6), (0.0, -0.55), (1.1, -0.35), (-0.9, -0.6)][:k]
    g = VGroup(*[mem_cell([cx + dx, MY + dy, 0], 0.3) for dx, dy in ps])
    if bobbing:
        for m in g:
            bob(m, 0.08, 1.8)
    return g


ABW, ABH = 3.4, 0.6


def ab_box(side="R"):
    return Rectangle(width=ABW, height=ABH).set_stroke(PURPLE, 4).move_to([MX[side], MY + 0.1, 0])


def ab_fill(box, tr):
    def f():
        w = max(0.02, ABW * tr.get_value())
        return Rectangle(width=w, height=ABH - 0.08).set_stroke(PURPLE, 0).set_fill(PURPLE, 0.9).move_to(box.get_left() + RIGHT * w / 2)
    return always_redraw(f)


def mini_graph(side):
    """Mini log graph inside a mouse: returns (axes group, point function)."""
    cx, cy = MX[side], MY
    ox, oy = cx - 2.05, cy - 1.25
    sx, sy = 0.386, 0.347

    def pt(t, L):
        return np.array([ox + sx * t, oy + sy * (L - 0.5), 0.0])
    xa = Line(pt(0, 0.5), pt(11, 0.5)).set_stroke(LIGHT, 3)
    ya = Line(pt(0, 0.5), pt(0, 7.7)).set_stroke(LIGHT, 3)
    en = DashedLine(pt(0, 7.0), pt(11, 7.0), dash_length=0.16).set_stroke(PALE, 3)
    et = T("enough", size=24, color=PALE).move_to(pt(8.6, 7.0) + UP * 0.3)
    return VGroup(xa, ya, en, et), pt


def mini_curve(pt, L0, color=GOLD):
    tx = LAG + DT * (7.0 - L0) / LG2

    def f(t):
        return L0 if t < LAG else L0 + (t - LAG) / DT * LG2
    return VMobject().set_points_as_corners([pt(t, f(t)) for t in np.linspace(0, tx, 40)]).set_stroke(color, 8), tx


# ================================================================ scenes
class S00Title(TitleCard):
    TITLE = "Why Is the Second Time Faster?"
    LESSON = "Adaptive Immunity"


class S01Hook(SpokenScene):
    def construct(self):
        random.seed(3)
        left = VGroup(*[gold_disc(p, 0.5) for p in [(-5.1, 0.5, 0), (-4.0, 0.85, 0), (-4.6, -0.4, 0)]])
        for c in left:
            bob(c, 0.04)
        lb = lab("before", 30).move_to([-4.6, -1.6, 0])
        ps = []
        for i in range(44):
            rad = 0.4 * math.sqrt(i + 0.5)
            ang = i * 2.39996
            ps.append(np.array([0.3 + rad * math.cos(ang), 0.3 + rad * math.sin(ang), 0]))
        big = VGroup(*[bob(gold_disc(p, 0.36), 0.05) for p in ps])
        self.play(FadeIn(left, scale=0.8), FadeIn(lb), run_time=1.3)
        self.at("a thousand times more")
        self.play(LaggedStart(*[GrowFromCenter(c) for c in big], lag_ratio=0.04), run_time=2.2)
        self.at("cells that fit")
        la = lab("after: x 1,000 (illustrative)", 26, GOLD).move_to([0.3, -2.95, 0])
        self.play(FadeIn(la, shift=UP * 0.15), run_time=0.7)
        self.at("is your second response")
        sw = Circle(radius=0.95).set_stroke(TEXT, 5).set_fill(BG, 1).move_to([5.0, 0.6, 0])
        btn = Rectangle(width=0.3, height=0.22).set_stroke(TEXT, 4).set_fill(TEXT, 0.6).move_to([5.0, 1.72, 0])
        q = lab("?", 70, YELLOW, weight=BOLD).move_to(sw)
        orb = Dot(radius=0.1, color=YELLOW).move_to(sw.get_center() + UP * 0.78)
        orb._a = 0.0

        def orbit(m, dt):
            m._a += dt * 1.6
            m.move_to(sw.get_center() + 0.78 * np.array([math.sin(m._a), math.cos(m._a), 0]))
        orb.add_updater(orbit)
        self.play(FadeIn(sw), FadeIn(btn), FadeIn(q, scale=1.3), FadeIn(orb), run_time=0.9)
        self.at("thousand times faster")
        lf = lab("1,000 x faster?", 28, YELLOW).move_to([4.95, -0.9, 0])
        self.play(FadeIn(lf, shift=UP * 0.15), Indicate(q, color=YELLOW, scale_factor=1.25), run_time=1.0)
        self.play(Indicate(la, color=YELLOW, scale_factor=1.05), run_time=1.0)
        self.finish()


class S02Link(SpokenScene):
    def construct(self):
        xs = [-5.4, -3.6, -1.8, 0, 1.8, 3.6, 5.4]
        ks = [0, 1, 3, 4, 2, 5, 6]
        row = VGroup(*[bob(Cell(x, -2.2, k, 0.62), 0.04) for x, k in zip(xs, ks)])
        v = Antigen(0.6, 0.3).move_to([-4.0, 1.2, 0])
        bob(v, 0.05)
        self.play(LaggedStart(*[GrowFromCenter(c) for c in row], lag_ratio=0.1), run_time=1.5)
        self.at("antigen")
        self.play(FadeIn(v, scale=1.3), run_time=0.7)
        v.clear_updaters()
        target = row[4]
        target.clear_updaters()
        self.at("choosing the few")
        self.play(v.animate.shift(goto_tip(v, target.tip, 0.9)), run_time=1.3)
        self.play(v.animate.shift(goto_tip(v, target.tip, 0.0) - goto_tip(v, target.tip, 0.9)), run_time=0.6)
        self.play(target.gold(), run_time=0.7)
        self.at("But a few cells")
        others = VGroup(*[c for i, c in enumerate(row) if i != 4])
        for c in others:
            c.clear_updaters()
        dest = np.array([C0[0], C0[1], 0]) - target.body.get_center()
        self.play(FadeOut(others), FadeOut(v), target.animate.shift(dest), run_time=1.5)
        rng = random.Random(7)
        sw = VGroup()
        tries = 0
        pts = []
        while len(pts) < 34 and tries < 5000:
            tries += 1
            x, y = rng.uniform(0.3, 6.4), rng.uniform(-3.3, 2.5)
            if all((x - a) ** 2 + (y - b) ** 2 > 0.6 ** 2 for a, b in pts):
                pts.append((x, y))
        for x, y in pts:
            s = Star(n=7, outer_radius=0.26, inner_radius=0.16, color=RED).set_fill(RED, 0.75).set_stroke(RED, 2).move_to([x, y, 0])
            sw.add(bob(s, 0.07))
        self.play(LaggedStart(*[GrowFromCenter(s) for s in sw], lag_ratio=0.05), run_time=2.0)
        ne = lab("not enough", 34, RED).move_to([-3.0, 2.3, 0])
        self.play(FadeIn(ne, shift=DOWN * 0.15), run_time=0.7)
        self.at("How do a few")
        q = lab("?", 100, YELLOW, weight=BOLD).move_to([-3.0, -2.2, 0])
        self.play(FadeIn(q, scale=1.4), Indicate(target.body, color=YELLOW, scale_factor=1.2), run_time=1.0)
        self.play(Indicate(q, color=YELLOW, scale_factor=1.2), run_time=1.0)
        self.finish()


def gold_cell_at_c0():
    c = Cell(C0[0], C0[1], MATCH, 0.65, GREY)
    c.body.set_stroke(GOLD, 5).set_fill(GOLD, 0.55)
    c.stalk.set_stroke(GOLD, 5)
    c.tip.set_stroke(GOLD, 5).set_fill(GOLD, 0.8)
    return c


def rounds_label(n, x=3.4, y=-0.55):
    return lab(f"after {n} round" + ("" if n == 1 else "s"), 28).move_to([x, y, 0])


class S03Double(SpokenScene):
    def construct(self):
        c0 = gold_cell_at_c0()
        self.add(c0)
        cnt = counter(1)
        rl = rounds_label(0)
        self.play(FadeIn(cnt), FadeIn(rl), run_time=0.8)
        self.play(FadeOut(c0.stalk), FadeOut(c0.tip), run_time=0.6)
        body = c0.body
        cells = [body]
        self.at("divides into two")
        self.play(Transform(cnt, counter(2)), Transform(rl, rounds_label(1)), run_time=0.3)
        cells = double_round(self, cells, run=1.2)
        self.at("divides again")
        self.play(Transform(cnt, counter(4)), Transform(rl, rounds_label(2)), run_time=0.3)
        cells = double_round(self, cells, run=1.2)
        self.at("every round of division")
        for n in (3, 4, 5):
            self.play(Transform(cnt, counter(2 ** n)), Transform(rl, rounds_label(n)), run_time=0.2)
            cells = double_round(self, cells, run=0.75)
        self.at("the clone doubles")
        self.play(Indicate(VGroup(*cells), color=YELLOW, scale_factor=1.04), Indicate(cnt, color=YELLOW, scale_factor=1.15), run_time=1.2)
        for c in cells:
            bob(c, 0.04)
        self.finish()


class S04Rule(SpokenScene):
    def construct(self):
        cells = make_cluster(32)
        self.add(*cells)
        cnt = counter(32)
        rl = rounds_label(5)
        self.add(cnt, rl)
        self.play(Transform(cnt, counter(32, x=4.7, y=-1.0)), Transform(rl, rounds_label(5, 4.7, -2.2)), run_time=0.8)
        for c in cells:
            bob(c, 0.03)
        a = lab("cells =", 36, TEXT).move_to([2.4, 2.7, 0])
        b = lab("starting cells x 2", 36, GOLD)
        e = lab("n", 26, YELLOW, weight=BOLD)
        e.next_to(b, RIGHT, buff=0.04).shift(UP * 0.2)
        bg = VGroup(b, e).move_to([3.1, 1.85, 0])
        nn = lab("n = number of doublings", 30, YELLOW).move_to([3.3, 0.9, 0])
        self.at("the number of cells")
        self.play(FadeIn(a, shift=RIGHT * 0.2), run_time=0.8)
        self.at("starting number")
        self.play(FadeIn(b, shift=RIGHT * 0.2), run_time=0.9)
        self.at("doubled once")
        self.play(FadeIn(e, scale=1.4), run_time=0.7)
        self.play(FadeIn(nn, shift=UP * 0.15), run_time=0.8)
        for c in cells:
            c.clear_updaters()
        self.at("Enough rounds")
        cells2 = cells
        for n in (6, 7):
            self.play(Transform(cnt, counter(2 ** n, x=4.7, y=-1.0)), Transform(rl, rounds_label(n, 4.7, -2.2)), run_time=0.2)
            cells2 = double_round(self, cells2, run=0.8)
        self.at("millions")
        mil = lab("a few  ->  millions", 32, GOLD).move_to([-3.0, -3.4, 0])
        self.play(FadeIn(mil, shift=UP * 0.15), run_time=0.8)
        for c in cells2:
            bob(c, 0.03)
        self.finish()


class S05Graph(SpokenScene):
    def construct(self):
        xax, yax, grid, ylab, xlab, xt, yt = axes_parts()
        ln, tx = enough_parts()
        cells = make_cluster(128)
        cnt = counter(128, x=4.7, y=-1.0)
        rl = rounds_label(7, 4.7, -2.2)
        mil = lab("a few  ->  millions", 32, GOLD).move_to([-3.0, -3.4, 0])
        allm = VGroup(*cells, cnt, rl, mil)
        self.add(allm)
        self.play(FadeOut(allm), run_time=0.8)
        self.at("Now draw it as a graph")
        self.play(Create(xax), Create(yax), run_time=1.2)
        self.at("Days run along")
        self.play(FadeIn(xt), LaggedStart(*[FadeIn(l) for l in xlab], lag_ratio=0.15), Indicate(xax, color=YELLOW), run_time=2.0)
        self.at("Cell number runs up")
        self.play(FadeIn(yt), Indicate(yax, color=YELLOW), run_time=1.5)
        self.at("Each grid line is 10 times")
        self.play(LaggedStart(*[AnimationGroup(Create(g), FadeIn(l)) for g, l in zip(grid, ylab)], lag_ratio=0.35), run_time=3.6)
        self.play(Create(ln), FadeIn(tx), run_time=1.2)
        self.finish()


class S06Primary(SpokenScene):
    def construct(self):
        graph_base(self)
        cv = curve(L_primary, 0, T_CROSS)
        self.at("steady doubling")
        self.play(Create(cv), run_time=2.6, rate_func=linear)
        st = Dot(Pt(0.5, L_START), radius=0.12, color=GOLD)
        self.add(st)
        self.at("starts from")
        sc = lab("100 cells (illustrative)", 24, GOLD).move_to([-1.8, -2.28, 0])
        self.play(FadeIn(sc, shift=UP * 0.15), Indicate(st, color=YELLOW, scale_factor=2), run_time=1.0)
        self.at("needs many")
        dots = VGroup(*[Dot(Pt(LAG + DT * k, L_START + k * LG2), radius=0.1, color=PALE).set_z_index(4) for k in range(18)])
        self.play(LaggedStart(*[FadeIn(d, scale=1.6) for d in dots], lag_ratio=0.18), run_time=3.0)
        br = Brace(Line(Pt(LAG, L_START), Pt(T_CROSS, L_ENOUGH)), direction=np.array([1, -1, 0]), color=PALE)
        bl = lab("about 17 doublings", 24, PALE)
        bl2 = lab("(computed, illustrative)", 22, PALE)
        bgrp = bk(VGroup(bl, bl2).arrange(DOWN, buff=0.08).move_to([0.25, -0.35, 0]))
        self.play(GrowFromCenter(br), FadeIn(bgrp), run_time=1.0)
        self.at("takes days")
        ov = Line(Pt(LAG, 0.55), Pt(T_CROSS, 0.55)).set_stroke(YELLOW, 8)
        dl = lab("days to build", 26, YELLOW).move_to([-1.3, -2.35, 0])
        cap = primary_climb_label(pos=(-0.45, 2.25))
        self.play(Create(ov), FadeOut(sc), FadeIn(dl), FadeIn(cap), run_time=1.2)
        self.add(comet(cv, 3.0))
        self.finish()


class S07Contract(SpokenScene):
    def construct(self):
        graph_base(self)
        cv = curve(L_primary, 0, T_CROSS)
        self.add(cv, primary_climb_label())
        rest = curve(L_primary, T_CROSS, T2S)
        self.at("most of the expanded")
        self.play(Create(rest), run_time=2.6, rate_func=linear)
        die = lab("most cells die", 28, RED).move_to([2.5, 2.3, 0])
        self.play(FadeIn(die, shift=LEFT * 0.2), run_time=0.8)
        self.at("But memory B")
        dots = mem_dots()
        self.play(LaggedStart(*[GrowFromCenter(d) for d in dots], lag_ratio=0.2), run_time=1.6)
        mem = lab("memory", 30, GOLD).move_to([1.05, 1.55, 0])
        self.play(FadeIn(mem, shift=UP * 0.15), run_time=0.7)
        for d in dots:
            bob(d, 0.03)
        self.at("There are many more")
        arr = DoubleArrow(Pt(0, L_START), Pt(0, L_MEM), buff=0.0, color=YELLOW, stroke_width=6)
        arr.move_to([1.0, (Pt(0, L_START)[1] + Pt(0, L_MEM)[1]) / 2, 0])
        self.play(Create(arr), Indicate(dots, color=YELLOW, scale_factor=1.4), run_time=1.5)
        self.add(comet(curve(L_primary, 0, T2S), 4.0))
        self.finish()


def s08_world(scene):
    graph_base(scene)
    full = curve(L_primary, 0, T2S)
    cap = primary_climb_label()
    dots = mem_dots()
    mem = lab("memory", 30, GOLD).move_to([1.05, 1.55, 0])
    arr = DoubleArrow(Pt(0, L_START), Pt(0, L_MEM), buff=0.0, color=YELLOW, stroke_width=6)
    arr.move_to([1.0, (Pt(0, L_START)[1] + Pt(0, L_MEM)[1]) / 2, 0])
    scene.add(full, cap, dots, mem, arr)
    for d in dots:
        bob(d, 0.03)
    return full, cap, dots, mem, arr


def q_chip():
    t = VGroup(lab("how many fewer", 24, YELLOW), lab("doublings?", 24, YELLOW)).arrange(DOWN, buff=0.06)
    bx = RoundedRectangle(corner_radius=0.14, width=t.width + 0.5, height=t.height + 0.4).set_stroke(YELLOW, 3).set_fill(YELLOW, 0.14)
    return VGroup(BackgroundRectangle(bx, color=BG, fill_opacity=1, buff=0, stroke_width=0), bx, t.move_to(bx)).move_to([4.9, 1.5, 0])


class S08Predict(SpokenScene):
    def construct(self):
        full, cap, dots, mem, arr = s08_world(self)
        self.add(comet(full, 4.0))
        self.at("a thousand times bigger")
        xl = lab("x 1,000 (illustrative)", 28, YELLOW).move_to([3.9, -0.45, 0])
        self.play(FadeIn(xl, shift=LEFT * 0.2), Indicate(arr, color=YELLOW), run_time=1.2)
        self.at("How many fewer")
        qc = q_chip()
        self.play(FadeIn(qc, shift=DOWN * 0.2), run_time=0.9)
        self.finish()


class S09Pause(NarratedScene):
    def construct(self):
        full, cap, dots, mem, arr = s08_world(self)
        xl = lab("x 1,000 (illustrative)", 28, YELLOW).move_to([3.9, -0.45, 0])
        qc = q_chip()
        self.add(xl, qc)
        tr = ValueTracker(0)
        ring = always_redraw(lambda: Arc(radius=0.34, start_angle=PI / 2, angle=-TAU * (1 - tr.get_value()), color=YELLOW, stroke_width=7).move_to([6.35, -2.15, 0]))
        self.add(ring, comet(full, 4.0))
        self.play(tr.animate.set_value(0.999), run_time=self.narration_s - 0.5, rate_func=linear)
        self.finish()


class S10Reveal(SpokenScene):
    def construct(self):
        full, cap, dots, mem, arr = s08_world(self)
        self.add(comet(full, 4.0))
        pts = [Pt(LAG, L_START)]
        for k in range(17):
            pts.append(Pt(LAG + DT * (k + 1), L_START + k * LG2))
            pts.append(Pt(LAG + DT * (k + 1), L_START + (k + 1) * LG2))
        stair = VMobject().set_points_as_corners(pts).set_stroke(PALE, 3)
        self.at("About ten fewer")
        self.play(Create(stair), run_time=2.2, rate_func=linear)
        self.at("a thousand fold")
        p1 = sup("2", "10", 31, TEXT)
        e1 = lab("= 1,024", 24, TEXT)
        e1.next_to(p1, RIGHT, buff=0.15)
        l1 = VGroup(p1, e1)
        l2 = lab("about 1,000", 24, TEXT)
        l3 = lab("so x 1,000 =", 24, YELLOW)
        l4 = lab("about 10 doublings", 24, YELLOW)
        pan = VGroup(l1, l2, l3, l4).arrange(DOWN, buff=0.22, aligned_edge=LEFT).move_to([4.55, 0.7, 0])
        box = SurroundingRectangle(pan, buff=0.25, color=PALE, stroke_width=3)
        self.play(FadeIn(l1, shift=LEFT * 0.2), Create(box), run_time=1.0)
        self.play(FadeIn(l2, shift=LEFT * 0.2), run_time=0.8)
        self.at("covers only about ten")
        poly_pts = [Pt(LAG, L_START)]
        for k in range(10):
            poly_pts.append(Pt(LAG + DT * k, L_START + k * LG2))
            poly_pts.append(Pt(LAG + DT * (k + 1), L_START + k * LG2))
        poly_pts.append(Pt(LAG + DT * 10, L_START))
        shade = Polygon(*poly_pts).set_stroke(TEAL, 0).set_fill(TEAL, 0.45)
        sk = lab("skipped", 32, TEAL).move_to([-0.9, -0.7, 0])
        guide = DashedLine(Pt(LAG + DT * 10, L_START + 10 * LG2), Pt(16, L_MEM), dash_length=0.18).set_stroke(GOLD, 4)
        self.play(FadeIn(shade), FadeIn(sk), run_time=1.0)
        self.play(FadeIn(l3, shift=LEFT * 0.2), Create(guide), run_time=1.0)
        self.at("saves those rounds")
        self.play(FadeIn(l4, shift=LEFT * 0.2), Indicate(shade, color=YELLOW, scale_factor=1.03), run_time=1.0)
        self.at("not a thousand fold")
        nope = lab("not 1,000 x faster", 26, RED).move_to([4.4, -1.4, 0])
        self.play(FadeIn(nope, shift=UP * 0.15), run_time=0.8)
        self.finish()


class S11Secondary(SpokenScene):
    def construct(self):
        graph_base(self)
        full = curve(L_primary, 0, T2S)
        dots = mem_dots()
        cap = primary_climb_label("primary")
        self.add(full, dots, cap)
        for d in dots:
            bob(d, 0.03)
        sec = curve(L_sec, T2S, T_SEC_X)
        ghost = curve(L_ghost, T2S, T_GH_X, color=GOLD, w=5)
        ghost.set_stroke(GOLD, 5, opacity=0.45)
        sd = Dot(Pt(T2S, L_MEM), radius=0.14, color=YELLOW)
        self.at("starts high")
        self.play(FadeIn(sd, scale=2.0), Indicate(dots[-1], color=YELLOW, scale_factor=1.8), run_time=1.0)
        self.at("reaches the line sooner")
        self.play(Create(sec), run_time=1.8, rate_func=linear)
        sl = lab("secondary", 30, GOLD).move_to([1.15, 2.05, 0])
        self.play(FadeIn(sl, shift=RIGHT * 0.2), run_time=0.7)
        self.at("needs fewer rounds")
        self.play(Create(ghost), run_time=2.0, rate_func=linear)
        gl = bk(lab("primary, replayed", 24, GOLD).set_opacity(0.85).move_to([0.1, -0.45, 0]))
        self.play(FadeIn(gl), run_time=0.6)
        a, b = Pt(T_SEC_X, L_ENOUGH), Pt(T_GH_X, L_ENOUGH)
        br = Brace(Line(a, b), direction=UP, color=YELLOW)
        bl = lab("fewer doublings", 28, YELLOW).next_to(br, UP, buff=0.08)
        self.play(GrowFromCenter(br), FadeIn(bl), run_time=1.0)
        self.add(comet(sec, 2.0, YELLOW, 0.5, 26, 0.85), comet(ghost, 3.5, PALE, 0.2, 22, 0.5), comet(full, 5.0))
        self.at("Real secondary responses")
        note1 = VGroup(lab("real peaks are", 20, TEXT), lab("usually larger", 20, TEXT)).arrange(DOWN, buff=0.06).move_to([5.1, -0.9, 0])
        note1 = bk(note1)
        note2 = bk(lab("(not in this model)", 20, TEXT).move_to([5.0, -1.55, 0]))
        self.play(FadeIn(note1, shift=UP * 0.15), run_time=0.8)
        self.at("this simple model")
        self.play(FadeIn(note2, shift=UP * 0.15), run_time=0.8)
        self.finish()


class S12Scope(SpokenScene):
    def construct(self):
        graph_base(self)
        full = curve(L_primary, 0, T2S)
        dots = mem_dots()
        sec = curve(L_sec, T2S, T_SEC_X)
        cap = primary_climb_label("primary")
        sl = lab("secondary", 30, GOLD).move_to([1.15, 2.05, 0])
        self.add(full, dots, sec, cap, sl)
        for d in dots:
            bob(d, 0.03)
        self.add(comet(full, 5.0), comet(sec, 2.0, YELLOW, 0.5, 26, 0.85))
        self.at("simplified model")
        tag = chp("simplified model", YELLOW, 26).move_to([4.6, 3.35, 0])
        self.play(FadeIn(tag, shift=DOWN * 0.3), run_time=0.9)
        self.play(Indicate(tag, color=YELLOW, scale_factor=1.08), run_time=0.8)
        self.at("leaves out cell death")
        n1 = VGroup(lab("leaves out:", 20, TEXT), lab("cells dying during expansion", 20, TEXT)).arrange(DOWN, aligned_edge=LEFT, buff=0.08)
        c1 = RoundedRectangle(corner_radius=0.14, width=n1.width + 0.5, height=n1.height + 0.4).set_stroke(RED, 3).set_fill(RED, 0.12)
        g1 = VGroup(BackgroundRectangle(c1, color=BG, fill_opacity=1, buff=0, stroke_width=0), c1, n1.move_to(c1)).move_to([4.2, 0.1, 0])
        self.play(FadeIn(g1, shift=LEFT * 0.4), run_time=1.0)
        self.at("And many memory cells")
        ls = ["leaves out: many memory", "cells respond faster than", "naive cells (varies by", "memory subset)"]
        n2 = VGroup(*[lab(s, 20, TEXT) for s in ls]).arrange(DOWN, aligned_edge=LEFT, buff=0.08)
        c2 = RoundedRectangle(corner_radius=0.14, width=n2.width + 0.5, height=n2.height + 0.4).set_stroke(TEAL, 3).set_fill(TEAL, 0.12)
        g2 = VGroup(BackgroundRectangle(c2, color=BG, fill_opacity=1, buff=0, stroke_width=0), c2, n2.move_to(c2)).move_to([4.2, -1.75, 0])
        self.play(FadeIn(g2, shift=LEFT * 0.4), run_time=1.0)
        self.finish()


# ---------------------------------------------------------------- mice
def left_mouse_final(scene):
    m = Mouse("L")
    mg = mem_group("L", 4, True)
    lb = left_label()
    scene.add(m, mg, lb)
    return m, mg, lb


class S13Vaccine(SpokenScene):
    def construct(self):
        ml, mr = Mouse("L"), Mouse("R")
        qm = lab("?", 110, YELLOW, weight=BOLD).move_to([0, 0.2, 0])
        self.play(FadeIn(ml, shift=RIGHT * 0.3), FadeIn(mr, shift=LEFT * 0.3), FadeIn(qm, scale=1.4), run_time=1.4)
        self.play(Indicate(qm, color=YELLOW, scale_factor=1.25), run_time=1.0)
        self.at("Compare two mice")
        self.play(FadeOut(qm), Indicate(ml.body, color=YELLOW, scale_factor=1.03), Indicate(mr.body, color=YELLOW, scale_factor=1.03), run_time=1.3)
        self.at("One gets")
        lb = left_label()
        self.play(FadeIn(lb, shift=DOWN * 0.15), run_time=0.7)
        v = Antigen(0.45, 0.22).move_to([MX["L"] - 1.4, 2.5, 0])
        self.at("harmless viral protein")
        self.play(FadeIn(v, scale=1.4), run_time=0.6)
        self.play(v.animate.move_to([MX["L"] - 0.9, MY + 0.4, 0]), run_time=1.2)
        self.at("Its own fitting cells")
        cx = MX["L"]
        c1 = gold_disc([cx + 0.5, MY - 0.2, 0], 0.34)
        self.play(FadeOut(v), FadeIn(c1, scale=0.5), run_time=0.7)
        cells = [c1]
        C = np.array([cx, MY - 0.1, 0.0])

        def pos(N):
            cc = 0.46 if N <= 8 else 0.4
            return [C + np.array([cc * math.sqrt(i + 0.5) * math.cos(i * 2.39996), cc * math.sqrt(i + 0.5) * math.sin(i * 2.39996), 0]) for i in range(N)]
        for N in (2, 4, 8):
            ps = pos(N)
            anims, new = [], []
            for i, c in enumerate(cells):
                d = c.copy()
                self.add(d)
                anims += [Transform(c, gold_disc(ps[2 * i], 0.32)), Transform(d, gold_disc(ps[2 * i + 1], 0.32))]
                new += [c, d]
            self.play(*anims, run_time=0.9)
            cells = new
        for c in cells:
            bob(c, 0.06, 1.8)
        self.at("memory cells stay")
        keep = cells[:4]
        go = cells[4:]
        for c in keep:
            c.clear_updaters()
        ps4 = [(-0.8, 0.35), (0.6, 0.6), (0.0, -0.55), (1.1, -0.35)]
        mems = [mem_cell([cx + dx, MY + dy, 0], 0.3) for dx, dy in ps4]
        self.play(*[FadeOut(c) for c in go], *[Transform(c, m) for c, m in zip(keep, mems)], run_time=1.4)
        for c in keep:
            bob(c, 0.08, 1.8)
        self.play(Indicate(VGroup(*keep), color=YELLOW, scale_factor=1.15), run_time=1.0)
        self.finish()


class S14Passive(SpokenScene):
    def construct(self):
        ml, mg, lb = left_mouse_final(self)
        mr = Mouse("R")
        self.add(mr)
        self.at("The other mouse")
        rb = right_label()
        self.play(FadeIn(rb, shift=DOWN * 0.15), Indicate(mr.body, color=YELLOW, scale_factor=1.03), run_time=1.0)
        box = ab_box("R")
        tr = ValueTracker(0.0)
        fill = ab_fill(box, tr)
        al = lab("antibody", 26, PURPLE).move_to([MX["R"], MY + 0.85, 0])
        self.at("protected at once")
        self.add(box, fill, al)
        self.play(tr.animate.set_value(1.0), FadeIn(box), FadeIn(al), run_time=0.9)
        tl = Arrow([MX["R"] - 2.5, -2.6, 0], [MX["R"] + 1.2, -2.6, 0], buff=0, color=LIGHT, stroke_width=4)
        wk = lab("weeks", 28, LIGHT).next_to(tl, RIGHT, buff=0.15)
        mk = Dot(radius=0.14, color=YELLOW)
        mk.add_updater(lambda m: m.move_to([MX["R"] - 2.5 + 3.4 * (1 - tr.get_value()) / 0.88, -2.6, 0]))
        self.play(Create(tl), FadeIn(wk), FadeIn(mk), run_time=0.8)
        self.at("But the antibody")
        self.play(tr.animate.set_value(0.12), run_time=3.2, rate_func=linear)
        self.at("no memory cells")
        nm = lab("no memory cells", 28, TEXT).move_to([MX["R"], MY - 0.95, 0])
        self.play(FadeIn(nm, shift=UP * 0.15), run_time=0.8)
        self.finish()


def right_mouse_final(scene):
    mr = Mouse("R")
    box = ab_box("R")
    tr = ValueTracker(0.12)
    fill = ab_fill(box, tr)
    al = lab("antibody", 26, PURPLE).move_to([MX["R"], MY + 0.85, 0])
    nm = lab("no memory cells", 28, TEXT).move_to([MX["R"], MY - 0.95, 0])
    rb = right_label()
    scene.add(mr, box, fill, al, nm, rb)
    return mr, box, fill, al, nm, rb


def term_labels(side, title, color, a, b):
    t = lab(title, 34, color, weight=BOLD).move_to([MX[side], -2.5, 0])
    s = VGroup(lab(a, 22, TEXT), lab(b, 22, TEXT)).arrange(DOWN, buff=0.05).move_to([MX[side], -3.3, 0])
    return t, s


class S15Terms(SpokenScene):
    def construct(self):
        ml, mg, lb = left_mouse_final(self)
        right_mouse_final(self)
        self.at("active immunity")
        a1, a2 = term_labels("L", "active immunity", GOLD, "your own cells,", "leaves memory")
        self.play(FadeIn(a1, shift=DOWN * 0.3), Indicate(mg, color=YELLOW, scale_factor=1.15), run_time=1.0)
        self.play(FadeIn(a2, shift=DOWN * 0.15), run_time=0.8)
        self.at("passive immunity")
        p1, p2 = term_labels("R", "passive immunity", PURPLE, "borrowed antibody,", "no memory")
        self.play(FadeIn(p1, shift=DOWN * 0.3), run_time=1.0)
        self.play(FadeIn(p2, shift=DOWN * 0.15), run_time=0.8)
        self.finish()


class S16Later(SpokenScene):
    def construct(self):
        ml, mg, lb = left_mouse_final(self)
        mr, box, fill, al, nm, rb = right_mouse_final(self)
        a1, a2 = term_labels("L", "active immunity", GOLD, "your own cells,", "leaves memory")
        p1, p2 = term_labels("R", "passive immunity", PURPLE, "borrowed antibody,", "no memory")
        self.add(a1, a2, p1, p2)
        cap = lab("six months later", 36, YELLOW, weight=BOLD).move_to([0, 3.5, 0])
        gl, ptl = mini_graph("L")
        gr, ptr = mini_graph("R")
        l1 = lab("vaccinated mouse", 26, GOLD).move_to([MX["L"], 2.75, 0])
        l2 = lab("antibody-only mouse", 26, PURPLE).move_to([MX["R"], 2.75, 0])
        self.play(FadeOut(VGroup(a1, a2, p1, p2, mg, box, fill, al, nm, lb, rb)), FadeIn(cap), run_time=1.0)
        self.play(FadeIn(gl), FadeIn(gr), FadeIn(l1), FadeIn(l2), run_time=0.9)
        self.at("both meet the virus")
        va = Antigen(0.25, 0.12).move_to([MX["L"] - 2.2, 2.2, 0])
        vb = Antigen(0.25, 0.12).move_to([MX["R"] + 2.2, 2.2, 0])
        self.play(FadeIn(va, scale=1.5), FadeIn(vb, scale=1.5), run_time=0.6)
        self.play(va.animate.move_to(ptl(0, L_START)), vb.animate.move_to(ptr(0, L_START)), run_time=0.9)
        self.play(FadeOut(va), FadeOut(vb), run_time=0.3)
        cl, txl = mini_curve(ptl, L_MEM)
        cr, txr = mini_curve(ptr, L_START)
        self.at("The vaccinated mouse starts")
        dl = Dot(ptl(0, L_MEM), radius=0.12, color=YELLOW)
        self.play(FadeIn(dl, scale=2.0), run_time=0.6)
        self.play(Create(cl), run_time=1.6, rate_func=linear)
        sl = lab("high start", 24, GOLD).move_to(ptl(3.6, 3.9))
        self.play(FadeIn(sl), run_time=0.5)
        self.at("The other starts")
        dr = Dot(ptr(0, L_START), radius=0.12, color=YELLOW)
        self.play(FadeIn(dr, scale=2.0), run_time=0.6)
        self.play(Create(cr), run_time=3.6, rate_func=linear)
        self.at("never met it")
        sr = lab("naive level", 24, PURPLE).move_to(ptr(6.6, 2.0))
        self.play(FadeIn(sr), run_time=0.6)
        self.add(comet(cl, 2.0, YELLOW, 0.5, 22), comet(cr, 3.5, YELLOW, 0.3, 22))
        self.finish()


class S17End(EndCard):
    LINE = "Memory is a head start: fewer doublings to enough cells."
