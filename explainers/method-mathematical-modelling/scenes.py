"""Mathematical and computational models: a model as an experiment on paper  (Biochemistrypedia methods film)

Timed to the SPOKEN words: every self.at("...") cue waits for that phrase in audio/words.json.
Every curve is computed in this file from the equation it is labelled with (numpy only).

COLOR MAP (one color per concept, whole video)
  BLUE   = the model: assumptions, equations, the "model" tag
  YELLOW = what the model computes: populations, prey, aurelia, the action potential, the model's prediction
  PURPLE = predators
  PINK   = the second species and the losing neurons
  GREEN  = measurement (data) and controls
  RED    = the gap, the failure, the pitfall
  ORANGE = an assumption that was changed
  TEAL   = the fixed NGF supply
  GREY   = structure, axes, de-emphasised text
  GOLD   = dates and the closing rule
"""
import numpy as np
from bp_style import *  # noqa: F401,F403

PURPLE = "#B58CD9"
ORANGE = "#F29E4C"
PINK = "#E57AA8"


# ---------------------------------------------------------------------------------------------
# the mathematics (all curves on screen come from here)
# ---------------------------------------------------------------------------------------------
def rk4(f, y0, t1, n):
    ts = np.linspace(0, t1, n + 1)
    h = t1 / n
    ys = np.zeros((n + 1, len(y0)))
    ys[0] = y0
    for i in range(n):
        y, t = ys[i], ts[i]
        k1 = f(t, y); k2 = f(t + h / 2, y + h / 2 * k1); k3 = f(t + h / 2, y + h / 2 * k2); k4 = f(t + h, y + h * k3)
        ys[i + 1] = y + h / 6 * (k1 + 2 * k2 + 2 * k3 + k4)
    return ts, ys


def predprey(K=None, t1=32.0, N0=30.0, P0=30.0, r=0.8, a=0.02, e=0.5, m=0.6):
    """Lotka-Volterra: dN/dt = rN - aNP ; dP/dt = eaNP - mP. With K: logistic prey, rN(1-N/K) - aNP."""
    def f(t, y):
        N, P = y
        g = r * N * (1 - N / K) if K else r * N
        return np.array([g - a * N * P, e * a * N * P - m * P])
    return rk4(f, [N0, P0], t1, 6000)


def logistic(t, K=100.0, r=0.6, N0=5.0):
    return K / (1 + (K - N0) / N0 * np.exp(-r * t))


def hodgkin_huxley(t1=22.0, dt=0.005):
    """Conductance model of the squid axon: I = g(V - E) for each ion, g_Na = gNa_max m^3 h, g_K = gK_max n^4.
    Modern sign convention, standard 6.3 C parameters; a 1 ms current pulse starts the spike."""
    gNa, gK, gL, ENa, EK, EL = 120.0, 36.0, 0.3, 50.0, -77.0, -54.387

    def xo(v, c):
        return np.where(np.abs(v) < 1e-7, c, v / (1 - np.exp(-v / c)))
    an = lambda V: 0.01 * xo(V + 55, 10); bn = lambda V: 0.125 * np.exp(-(V + 65) / 80)
    am = lambda V: 0.1 * xo(V + 40, 10); bm = lambda V: 4 * np.exp(-(V + 65) / 18)
    ah = lambda V: 0.07 * np.exp(-(V + 65) / 20); bh = lambda V: 1 / (1 + np.exp(-(V + 35) / 10))
    V = -65.0
    n = an(V) / (an(V) + bn(V)); m = am(V) / (am(V) + bm(V)); h = ah(V) / (ah(V) + bh(V))
    N = int(t1 / dt); ts = np.arange(N) * dt; out = np.zeros(N)
    for i, t in enumerate(ts):
        I = 15.0 if 3.0 <= t < 4.0 else 0.0
        dV = I - gNa * m ** 3 * h * (V - ENa) - gK * n ** 4 * (V - EK) - gL * (V - EL)
        m += dt * (am(V) * (1 - m) - bm(V) * m); h += dt * (ah(V) * (1 - h) - bh(V) * h)
        n += dt * (an(V) * (1 - n) - bn(V) * n); V += dt * dV
        out[i] = V
    return ts, out


def competition(alone, t1=40.0, K1=100.0, K2=60.0, a12=0.5, a21=1.5, r=0.4):
    """Lotka-Volterra competition: r_i N_i [1 - (N_i + a_ij N_j)/K_i]; alone = a_ij set to zero."""
    def f(t, y):
        N1, N2 = y
        x12, x21 = (0.0, 0.0) if alone else (a12, a21)
        return np.array([r * N1 * (1 - (N1 + x12 * N2) / K1), r * N2 * (1 - (N2 + x21 * N1) / K2)])
    return rk4(f, [2.0, 2.0], t1, 4000)


def hill(x, n):
    return x ** n / (1 + x ** n)


# ---------------------------------------------------------------------------------------------
# helpers
# ---------------------------------------------------------------------------------------------
def lab(text, size=24, color=GREY, **kw):
    return T(text, size, color, **kw)


def lines(*texts, size=24, color=TEXT, buff=0.12, align=LEFT, colors=None, **kw):
    g = VGroup(*[T(t, size, (colors[i] if colors else color), **kw) for i, t in enumerate(texts)])
    return g.arrange(DOWN, aligned_edge=align, buff=buff)


def arr(a, b, color=GREY, w=5, tip=0.2):
    return Arrow(np.array([a[0], a[1], 0.0]), np.array([b[0], b[1], 0.0]), buff=0.0, color=color, stroke_width=w,
                 tip_length=tip, max_tip_length_to_length_ratio=0.45, max_stroke_width_to_length_ratio=12)


def poly(pts, color=YELLOW, w=5):
    m = VMobject()
    m.set_points_as_corners([np.array([p[0], p[1], 0.0]) for p in pts])
    m.set_stroke(color, w)
    return m


def dashed(a, b, color=GREY, w=2):
    return DashedLine(np.array([a[0], a[1], 0.0]), np.array([b[0], b[1], 0.0]), color=color, stroke_width=w)


def sup(base, power, size=28, color=TEXT):
    """base with a raised power, built from two pieces."""
    a = T(base, size, color)
    b = T(power, int(size * 0.65), color).next_to(a, UR, buff=0.02).shift(DOWN * 0.1)
    return VGroup(a, b)


def model_tag(pos, text="model"):
    c = chip(text, BLUE, 22, pad=0.14)
    return c.move_to([pos[0], pos[1], 0])


class Pl:
    """A little plot: data box (l,r,b,t in frame units) mapped from x0..x1, y0..y1."""

    def __init__(self, l, r, b, t, x0, x1, y0, y1):
        self.l, self.r, self.b, self.t = l, r, b, t
        self.x0, self.x1, self.y0, self.y1 = x0, x1, y0, y1

    def P(self, x, y):
        return [self.l + (x - self.x0) / (self.x1 - self.x0) * (self.r - self.l),
                self.b + (y - self.y0) / (self.y1 - self.y0) * (self.t - self.b)]

    def axes(self, color=GREY):
        return VGroup(poly([self.P(self.x0, self.y1), self.P(self.x0, self.y0), self.P(self.x1, self.y0)], color, 3))

    def curve(self, xs, ys, color=YELLOW, w=5):
        pts = []
        for x, y in zip(xs, ys):
            if y > self.y1 or y < self.y0:
                break
            pts.append(self.P(x, y))
        return poly(pts, color, w)

    def dots(self, xs, ys, color=GREEN, r=0.09):
        return VGroup(*[Dot(self.P(x, y) + [0.0], radius=r, color=color) for x, y in zip(xs, ys)])


# ---------------------------------------------------------------------------------------------
class S00Title(TitleCard):
    LESSON = "Methods library"
    TITLE = "Models Turn Assumptions Into Predictions"


# ---------------------------------------------------------------------------------------------
class S01Problem(SpokenScene):
    """a tangle nobody can reason through; a curve that cannot say why; a model that makes a number to test."""

    def construct(self):
        rng = np.random.RandomState(4)
        A = chip("A", GREY, 28).move_to([-5.2, 1.7, 0]); B = chip("B", GREY, 28).move_to([-2.4, 2.4, 0])
        C = chip("C", GREY, 28).move_to([-4.6, -1.0, 0]); D = chip("D", GREY, 28).move_to([-1.6, -0.2, 0])
        ab = CurvedArrow(A.get_top() + [0.25, 0.05, 0], B.get_left() + [-0.05, 0.1, 0], angle=-0.7, color=GREY, stroke_width=4)
        ba = CurvedArrow(B.get_left() + [-0.05, -0.15, 0], A.get_right() + [0.05, 0.0, 0], angle=-0.7, color=GREY, stroke_width=4)
        cd = CurvedArrow(C.get_right() + [0.05, 0.1, 0], D.get_left() + [-0.05, 0.0, 0], angle=-0.7, color=GREY, stroke_width=4)
        dc = CurvedArrow(D.get_bottom() + [-0.2, -0.05, 0], C.get_bottom() + [0.2, -0.05, 0], angle=-0.7, color=GREY, stroke_width=4)
        bd = arr(B.get_bottom() + [0.1, -0.05, 0], D.get_top() + [0, 0.05, 0], GREY, 4, 0.16)
        ac = arr(A.get_bottom() + [0, -0.05, 0], C.get_top() + [0, 0.05, 0], GREY, 4, 0.16)
        net = VGroup(A, B, C, D, ab, ba, cd, dc, bd, ac)
        # delay: a clock beside the B-to-D arrow
        clock = VGroup(Circle(radius=0.32, stroke_color=TEXT, stroke_width=3, fill_color=BG, fill_opacity=1),
                       Line(ORIGIN, UP * 0.2, color=TEXT, stroke_width=3), Line(ORIGIN, RIGHT * 0.14, color=TEXT, stroke_width=3))
        clock.move_to([-2.0, 1.1, 0])
        dl = lab("delay", 26, TEXT).next_to(clock, RIGHT, buff=0.12)
        # a crowd of competing cells
        cells = VGroup()
        pts = []
        tries = 0
        while len(pts) < 24 and tries < 5000:
            tries += 1
            p = rng.uniform(-1, 1, 2) * [2.3, 1.9]
            if (p[0] / 2.3) ** 2 + (p[1] / 1.9) ** 2 < 1 and all(np.hypot(p[0] - q[0], p[1] - q[1]) > 0.62 for q in pts):
                pts.append(p)
        for p in pts:
            cells.add(Circle(radius=0.27, stroke_color=GREY, stroke_width=3, fill_color=GREY, fill_opacity=0.18).move_to([4.0 + p[0], 0.3 + p[1], 0]))
        crowd_l = lab("a crowd of competing cells", 26, GREY).move_to([4.0, -2.55, 0])
        q = T("?", 110, YELLOW, weight=BOLD).move_to([0.1, -1.7, 0])
        qchip = lab("what will it do?", 28, TEXT).move_to([-2.9, -2.9, 0])

        self.at("Some systems")
        self.play(FadeIn(net, lag_ratio=0.1), run_time=1.2)
        self.at("Two feedback loops")
        self.play(*[m.animate.set_color(BLUE) for m in (ab, ba, A[0], B[0])], run_time=0.5)
        self.play(*[m.animate.set_color(BLUE) for m in (cd, dc, C[0], D[0])], run_time=0.5)
        self.at("a delay")
        self.play(FadeIn(clock), FadeIn(dl), run_time=0.5)
        self.at("a crowd of competing cells")
        self.play(FadeIn(cells, lag_ratio=0.05), FadeIn(crowd_l), run_time=1.2)
        self.at("intuition does not predict")
        self.play(FadeIn(q, scale=1.2), FadeIn(qchip), run_time=0.5)

        # --- a measured curve
        self.at("a measured curve")
        self.play(FadeOut(VGroup(net, clock, dl, cells, crowd_l, q, qchip)), run_time=0.4)
        pl = Pl(-6.0, 0.8, -2.6, 2.4, 0, 20, 0, 110)
        ax = pl.axes()
        xs = np.linspace(1, 19, 13)
        ys = logistic(xs, 100, 0.55, 5) + rng.randn(13) * 3.0
        data = pl.dots(xs, ys, GREEN, 0.1)
        ex = lab("example data", 24, GREY).move_to([-1.6, -3.1, 0])
        tl = lab("time", 24, GREY).move_to([-2.6, -3.1, 0]).shift(LEFT * 2.0)
        self.play(FadeIn(ax), LaggedStart(*[FadeIn(d, scale=1.5) for d in data], lag_ratio=0.08), FadeIn(ex), run_time=1.1)
        self.at("why it has its shape")
        why = lab("why this shape?", 32, TEXT, weight=BOLD).move_to([-2.4, 3.1, 0])
        qq = T("?", 80, YELLOW, weight=BOLD).move_to([-5.2, 1.4, 0])
        self.play(FadeIn(why), FadeIn(qq, scale=1.2), run_time=0.5)

        self.at("A model proposes a cause")
        mc = fit(chip("model: a proposed cause", BLUE, 26), max_w=4.8).move_to([4.0, 1.6, 0])
        self.play(FadeOut(qq), FadeIn(mc, shift=LEFT * 0.2), run_time=0.5)
        tt = np.linspace(0, 20, 200)
        mod = pl.curve(tt, logistic(tt, 100, 0.55, 5), YELLOW, 5)
        self.play(Create(mod, run_time=1.2, rate_func=linear))
        self.at("a number")
        px = pl.P(10, logistic(10, 100, 0.55, 5))
        pd = Dot([px[0], px[1], 0], radius=0.15, color=YELLOW)
        ring = Circle(radius=0.3, stroke_color=YELLOW, stroke_width=3).move_to(pd)
        nl = lines("a number the cause", "must produce", size=26, color=YELLOW, buff=0.08, align=ORIGIN).move_to([4.0, -0.7, 0])
        ln = poly([[px[0] + 0.3, px[1] - 0.1], [3.0, -0.2]], YELLOW, 3)
        self.play(FadeIn(pd, scale=2.0), Create(ring), Create(ln), FadeIn(nl), run_time=0.8)
        self.finish()


# ---------------------------------------------------------------------------------------------
class S02Assumptions(SpokenScene):
    """step 1: an assumptions box fills while the predator-prey sketch builds."""

    def construct(self):
        box = RoundedRectangle(corner_radius=0.2, width=6.9, height=5.6, stroke_color=BLUE, stroke_width=4,
                               fill_color=BLUE, fill_opacity=0.08).move_to([-3.1, -0.1, 0])
        title = lab("assumptions", 34, BLUE, weight=BOLD).move_to([-3.1, 2.2, 0])
        sub = lab("and what is left out", 24, GREY).move_to([-3.1, 1.65, 0])
        it1 = lab("prey grow exponentially", 28, TEXT).move_to([-3.1, 0.7, 0])
        it2 = lab("consumption ∝ prey × predators", 28, TEXT).move_to([-3.1, -0.2, 0])
        it3 = lab("no handling time", 28, TEXT).move_to([-3.1, -1.1, 0])
        it4 = lab("each predator dies at a constant rate", 28, TEXT)
        it4 = fit(it4, max_w=6.2).move_to([-3.1, -2.0, 0])
        # sketch
        prey = chip("prey", YELLOW, 30).move_to([2.6, 2.1, 0])
        pred = chip("predators", PURPLE, 30).move_to([2.6, -2.2, 0])
        g_in = arr([5.9, 2.1], [prey.get_right()[0] + 0.1, 2.1], GREY, 5, 0.2)
        g_l = lab("growth", 24, GREY).move_to([5.0, 2.55, 0])
        c_arr = arr([2.6, 1.5], [2.6, -1.55], GREY, 5, 0.2)
        c_l = lab("consumption", 24, GREY).move_to([4.2, 0.9, 0])
        h_chip = chip("handling time", GREY, 24, fill_opacity=0.05)
        h_chip.move_to([4.6, -0.1, 0])
        h_x = VGroup(Line(h_chip.get_corner(UL), h_chip.get_corner(DR), color=RED, stroke_width=5),
                     Line(h_chip.get_corner(DL), h_chip.get_corner(UR), color=RED, stroke_width=5))
        d_out = arr([pred.get_right()[0] + 0.1, -2.2], [5.9, -2.2], GREY, 5, 0.2)
        d_l = lab("death", 24, GREY).move_to([5.1, -1.75, 0])

        self.at("state the assumptions")
        self.play(FadeIn(box), FadeIn(title), run_time=0.6)
        self.at("what is left out")
        self.play(FadeIn(sub), run_time=0.4)
        self.at("prey grow exponentially")
        self.play(FadeIn(it1, shift=RIGHT * 0.2), FadeIn(prey), GrowArrow(g_in), FadeIn(g_l), run_time=0.7)
        self.at("proportional to prey times predators")
        self.play(FadeIn(it2, shift=RIGHT * 0.2), FadeIn(pred), GrowArrow(c_arr), FadeIn(c_l), run_time=0.7)
        self.at("no handling time")
        self.play(FadeIn(it3, shift=RIGHT * 0.2), FadeIn(h_chip), Create(h_x), run_time=0.7)
        self.at("constant rate")
        self.play(FadeIn(it4, shift=RIGHT * 0.2), GrowArrow(d_out), FadeIn(d_l), run_time=0.7)
        self.finish()


# ---------------------------------------------------------------------------------------------
class S03Rules(SpokenScene):
    """step 2: the rules as equations; curves computed from them; per-individual and total growth; K."""

    def construct(self):
        K, r = 100.0, 0.6
        e1 = M("dN/dt = rN", 38, BLUE).move_to([-4.0, 1.3, 0])
        e1n = lab("exponential growth", 26, GREY).next_to(e1, DOWN, buff=0.15, aligned_edge=LEFT)
        e2 = M("dN/dt = rN(1 − N/K)", 38, BLUE).move_to([-3.2, -1.0, 0])
        e2n = lab("logistic growth", 26, GREY).next_to(e2, DOWN, buff=0.15, aligned_edge=LEFT)
        pl = Pl(1.6, 6.3, -2.6, 2.7, 0, 14, 0, 130)
        ax = pl.axes()
        xl = lab("time", 24, GREY).move_to([4.0, -3.1, 0]); yl = lab("N", 24, GREY).move_to([1.0, 2.7, 0])
        tt = np.linspace(0, 14, 300)
        ex_c = pl.curve(tt, 5 * np.exp(r * tt), GREY, 5)
        lg_c = pl.curve(tt, logistic(tt, K, r, 5), YELLOW, 6)
        kline = dashed(pl.P(0, K), pl.P(14, K), GREY, 2)
        kl = lab("K", 26, TEXT).move_to([pl.l - 0.35, pl.P(0, K)[1], 0])
        tag = model_tag([-5.4, 3.2])

        self.at("write the rules")
        self.play(FadeIn(tag), FadeIn(ax), FadeIn(xl), FadeIn(yl), run_time=0.6)
        self.at("Exponential growth")
        self.play(FadeIn(e1, shift=RIGHT * 0.2), FadeIn(e1n), Create(ex_c, run_time=1.4, rate_func=linear))
        self.at("Logistic growth", lead=0.0)
        leg = lines("N: population size", "r: growth rate", "K: carrying capacity", size=22, color=GREY, buff=0.06).move_to([-4.6, -2.7, 0]).align_to([-5.9, 0, 0], LEFT)
        self.play(FadeIn(e2, shift=RIGHT * 0.2), FadeIn(e2n), FadeIn(kline), FadeIn(kl), FadeIn(leg), run_time=0.5)
        self.play(Create(lg_c, run_time=1.8, rate_func=linear))

        # --- per-individual and total growth
        self.at("per individual")
        keep = e2
        self.play(FadeOut(VGroup(e1, e1n, e2n, leg, ax, xl, yl, ex_c, lg_c, kline, kl, tag)), e2.animate.move_to([0.0, 3.2, 0]).scale(0.8), run_time=0.5)
        pa = Pl(-5.9, -0.9, -2.2, 1.7, 0, 1.3, -0.35, 1.05)   # per capita r(1-N/K), r=1, K=1
        pb = Pl(0.9, 5.9, -2.2, 1.7, 0, 1.3, -0.45, 0.32)     # total N(1-N/K)
        axa, axb = pa.axes(), pb.axes()
        za = dashed(pa.P(0, 0), pa.P(1.3, 0), GREY, 2); zb = dashed(pb.P(0, 0), pb.P(1.3, 0), GREY, 2)
        ta = lab("growth per individual", 26, TEXT, weight=BOLD).move_to([-3.4, 2.45, 0])
        tb = lab("total growth", 26, TEXT, weight=BOLD).move_to([3.4, 2.45, 0])
        xa = lab("N", 24, GREY).move_to([-3.4, -2.65, 0]); xb = lab("N", 24, GREY).move_to([3.4, -2.65, 0])
        nn = np.linspace(0, 1.3, 200)
        ca = pa.curve(nn, 1 - nn, YELLOW, 6)
        cb = pb.curve(nn, nn * (1 - nn), YELLOW, 6)
        tag1 = model_tag([-6.0, 3.2]); 
        self.play(FadeIn(axa), FadeIn(za), FadeIn(ta), FadeIn(xa), FadeIn(tag1), run_time=0.5)
        self.at("falls in a straight line")
        self.play(Create(ca, run_time=1.2, rate_func=linear))
        self.play(FadeIn(axb), FadeIn(zb), FadeIn(tb), FadeIn(xb), run_time=0.4)
        self.at("Total growth peaks")
        self.play(Create(cb, run_time=1.3, rate_func=linear))
        pk = Dot(pb.P(0.5, 0.25) + [0.0], radius=0.13, color=GOLD)
        pk_l = lab("K/2", 26, GOLD, weight=BOLD).move_to([pb.P(0.5, 0.25)[0], pb.P(0.5, 0.25)[1] + 0.4, 0])
        pk_d = dashed(pb.P(0.5, 0.25), pb.P(0.5, 0.0), GOLD, 2)
        self.play(FadeIn(pk, scale=1.6), FadeIn(pk_l), Create(pk_d), run_time=0.5)
        self.at("equilibrium")
        kd = Dot(pb.P(1.0, 0.0) + [0.0], radius=0.13, color=TEXT)
        kdl = lab("K: growth is zero", 24, TEXT).move_to([pb.P(0.45, -0.1)[0], pb.P(0.45, -0.1)[1], 0])
        kld = poly([[kdl.get_right()[0] + 0.08, kdl.get_right()[1]], [pb.P(1.0, 0.0)[0] - 0.12, pb.P(1.0, 0.0)[1] - 0.04]], TEXT, 2)
        self.play(FadeIn(kd, scale=1.6), FadeIn(kdl), Create(kld), run_time=0.5)
        self.at("not a ceiling")
        below = lab("above K: shrinks", 24, TEXT).move_to([pb.P(0.45, -0.31)[0], pb.P(0.45, -0.31)[1], 0])
        bld = poly([[below.get_right()[0] + 0.08, below.get_right()[1]], [pb.P(1.14, -0.16)[0] - 0.1, pb.P(1.14, -0.16)[1] - 0.05]], TEXT, 2)
        self.play(FadeIn(below), Create(bld), run_time=0.5)
        self.finish()


# ---------------------------------------------------------------------------------------------
class S04Run(SpokenScene):
    """step 3: run it; neutral cycles with a lag; change one assumption (logistic prey) and run again."""

    def construct(self):
        ts, ys = predprey()
        N, P = ys[:, 0], ys[:, 1]
        ymax = 1.08 * max(N.max(), P.max())
        big = Pl(-5.8, 5.4, -2.5, 2.5, 0, ts[-1], 0, ymax)
        ax = big.axes()
        cN = big.curve(ts, N, YELLOW, 5); cP = big.curve(ts, P, PURPLE, 5)
        lN = lab("prey", 28, YELLOW, weight=BOLD).move_to([-5.0, 3.1, 0]); lP = lab("predators", 28, PURPLE, weight=BOLD).move_to([-3.2, 3.1, 0])
        tag = model_tag([5.4, 3.1])
        tl = lab("time", 24, GREY).move_to([-0.2, -3.0, 0])
        # lag marks: first prey peak, next predator peak
        def peaks(y):
            return [i for i in range(1, len(y) - 1) if y[i] > y[i - 1] and y[i] >= y[i + 1]]
        ip = peaks(N)[0]; iq = [i for i in peaks(P) if i > ip][0]
        xp, xq = ts[ip], ts[iq]
        v1 = dashed(big.P(xp, 0), big.P(xp, ymax), YELLOW, 2); v2 = dashed(big.P(xq, 0), big.P(xq, ymax), PURPLE, 2)
        lag = poly([big.P(xp, ymax * 0.995), big.P(xq, ymax * 0.995)], TEXT, 5)
        lag_l = lab("predator peak lags", 24, TEXT).move_to([big.P(xq, 0)[0] + 0.15 + 1.1, big.P(xp, ymax * 0.995)[1], 0])
        neutral = lab("cycles neither grow nor shrink", 26, TEXT).move_to([3.0, -3.0, 0])
        # rerun with logistic prey
        ts2, ys2 = predprey(K=120.0)
        cN2 = None

        self.at("run it")
        self.play(FadeIn(ax), FadeIn(tag), FadeIn(tl), FadeIn(lN), FadeIn(lP), run_time=0.5)
        self.play(Create(cN, run_time=2.0, rate_func=linear), Create(cP, run_time=2.0, rate_func=linear))
        self.at("repeating cycles")
        self.play(FadeIn(neutral), run_time=0.4)
        self.at("predator peaks lagging")
        self.play(Create(v1), Create(v2), run_time=0.4)
        self.play(Create(lag), FadeIn(lag_l), run_time=0.5)

        # --- shrink to the top slot, rerun below
        self.at("change one assumption")
        top = Pl(-5.8, 5.4, 0.55, 3.0, 0, ts[-1], 0, ymax)
        bot = Pl(-5.8, 5.4, -3.2, -0.65, 0, ts[-1], 0, ymax)
        ax_t = top.axes(); cN_t = top.curve(ts, N, YELLOW, 4); cP_t = top.curve(ts, P, PURPLE, 4)
        ax_b = bot.axes()
        ymax2 = ymax
        cN_b = bot.curve(ts2, ys2[:, 0], YELLOW, 4); cP_b = bot.curve(ts2, ys2[:, 1], PURPLE, 4)
        old = VGroup(ax, cN, cP, v1, v2, lag, lag_l, neutral, lN, lP, tl, tag)
        t_tag = lab("exponential prey", 24, GREY).move_to([-4.6, 3.35, 0])
        self.play(FadeOut(old), run_time=0.4)
        self.play(FadeIn(ax_t), FadeIn(cN_t), FadeIn(cP_t), FadeIn(t_tag), FadeIn(model_tag([5.4, 3.35])), run_time=0.5)
        self.at("prey growth logistic")
        b_tag = lab("logistic prey, example parameters", 26, ORANGE, weight=BOLD).move_to([-2.4, -0.2, 0])
        leg_n = lab("prey", 22, YELLOW).move_to([4.0, -0.95, 0]); leg_p = lab("predators", 22, PURPLE).move_to([5.3, -0.95, 0])
        self.play(FadeIn(ax_b), FadeIn(b_tag), FadeIn(leg_n), FadeIn(leg_p), run_time=0.5)
        self.play(Create(cN_b, run_time=1.3, rate_func=linear), Create(cP_b, run_time=1.3, rate_func=linear))
        self.at("the cycles change")
        self.play(Indicate(VGroup(cN_b, cP_b), color=ORANGE, scale_factor=1.0), run_time=0.8)
        self.at("which conclusions survive")
        chk = chip("which conclusions survive?", ORANGE, 24).move_to([3.7, -0.2, 0])
        self.play(FadeIn(chk, shift=UP * 0.15), run_time=0.5)
        self.finish()


# ---------------------------------------------------------------------------------------------
class S05Reading(SpokenScene):
    """compare with data the fit did not use: predicted 18.8 m/s vs measured 21.2 m/s; the gap is the lesson."""

    def construct(self):
        c1 = chip("separate current measurements", GREEN, 26).move_to([-3.6, 3.0, 0])
        c2 = chip("fitted equations", BLUE, 26).move_to([2.2, 3.0, 0])
        a12 = arr(c1.get_right() + [0.1, 0, 0], c2.get_left() + [-0.1, 0, 0], GREY, 5, 0.2)
        fibre_y1, fibre_y2 = 0.9, -1.0
        x0, x1 = -4.2, 5.2
        D = x1 - x0
        f1 = Line([x0, fibre_y1, 0], [x1, fibre_y1, 0], color=GREY, stroke_width=10).set_opacity(0.4)
        f2 = Line([x0, fibre_y2, 0], [x1, fibre_y2, 0], color=GREY, stroke_width=10).set_opacity(0.4)
        l1 = lines("model", "predicted", size=26, color=YELLOW, buff=0.06, align=RIGHT).move_to([-5.6, fibre_y1, 0])
        l2 = lines("measured", "", size=26, color=GREEN, buff=0.06, align=RIGHT)
        l2 = lab("measured", 26, GREEN).move_to([-5.4, fibre_y2, 0])
        v1 = M("18.8 m/s", 32, YELLOW).move_to([5.6 - 0.2, fibre_y1 + 0.6, 0])
        v2 = M("21.2 m/s", 32, GREEN).move_to([5.6 - 0.2, fibre_y2 + 0.6, 0])
        v1.set_x(1.6); v2.set_x(1.8)
        d1 = Dot([x0, fibre_y1, 0], radius=0.2, color=YELLOW); d2 = Dot([x0, fibre_y2, 0], radius=0.2, color=GREEN)
        cond = lab("one fibre, 18.5 °C", 26, TEXT).move_to([0.2, 2.05, 0])
        self.at("not fitted")
        self.play(FadeIn(f1), FadeIn(f2), FadeIn(d1), FadeIn(d2), FadeIn(l1[0]), FadeIn(l2), run_time=0.8)
        self.at("squid axon model")
        self.play(FadeIn(c2, shift=DOWN * 0.15), run_time=0.5)
        self.at("separate current measurements")
        self.play(FadeIn(c1, shift=RIGHT * 0.2), GrowArrow(a12), run_time=0.6)
        self.play(Indicate(c1, color=GREEN, scale_factor=1.1), run_time=0.6)
        self.at("degrees Celsius")
        self.play(FadeIn(cond), run_time=0.4)
        self.at("predicted conduction")
        self.play(FadeIn(l1[1]), run_time=0.2)
        T1 = 2.3
        self.play(d1.animate.move_to([x0 + D * 18.8 / 21.2, fibre_y1, 0]), run_time=T1, rate_func=linear)
        self.play(FadeIn(v1, scale=1.1), run_time=0.3)
        self.at("The measurement was")
        self.play(d2.animate.move_to([x1, fibre_y2, 0]), run_time=T1, rate_func=linear)
        self.play(FadeIn(v2, scale=1.1), run_time=0.3)
        self.at("that gap")
        xm = x0 + D * 18.8 / 21.2
        gl = dashed([xm, fibre_y1 + 0.3], [xm, fibre_y2 - 0.3], YELLOW, 2)
        br = DoubleArrow([xm, fibre_y2 - 0.55, 0], [x1, fibre_y2 - 0.55, 0], buff=0, color=RED, stroke_width=5, tip_length=0.16)
        gap_l = lab("the gap: 2.4 m/s", 28, RED, weight=BOLD).move_to([(xm + x1) / 2, fibre_y2 - 1.05, 0])
        self.play(Create(gl), GrowFromCenter(br), FadeIn(gap_l), run_time=0.8)
        self.at("what to test next")
        qs = VGroup(*[chip(t, ORANGE, 24) for t in ("test the assumptions", "test the parameters", "test the measurements")]).arrange(RIGHT, buff=0.3).move_to([0.0, -3.1, 0])
        self.play(LaggedStart(*[FadeIn(c, shift=UP * 0.15) for c in qs], lag_ratio=0.3), run_time=1.0)
        self.finish()


# ---------------------------------------------------------------------------------------------
class S06Pitfalls(SpokenScene):
    """a fit is not a mechanism (two curves, same points); exclusion holds only under stated conditions."""

    def construct(self):
        rng = np.random.RandomState(3)
        pl = Pl(-5.9, -0.9, -0.7, 2.4, 0, 20, 0, 110)
        ax = pl.axes()
        xs = np.linspace(1, 19, 12)
        ys = logistic(xs, 100, 0.55, 5) + rng.randn(12) * 2.5
        data = pl.dots(xs, ys, GREEN, 0.1)
        tt = np.linspace(0, 20, 200)
        # curve A: logistic. curve B: Gompertz y = K exp(-b exp(-c t)), grid-fitted to the same points
        best = None
        for K in np.linspace(90, 115, 26):
            for b in np.linspace(1.0, 6.0, 51):
                for c in np.linspace(0.15, 0.7, 56):
                    err = np.sum((K * np.exp(-b * np.exp(-c * xs)) - ys) ** 2)
                    if best is None or err < best[0]:
                        best = (err, K, b, c)
        _, K, b, c = best
        ca = pl.curve(tt, logistic(tt, 100, 0.55, 5), YELLOW, 5)
        cb = pl.curve(tt, K * np.exp(-b * np.exp(-c * tt)), ORANGE, 5)
        h1 = lab("Pitfall: a fit is not a mechanism", 26, RED, weight=BOLD)
        h1 = fit(h1, max_w=6.0).move_to([-3.4, 3.3, 0])
        ex = lab("example data", 22, GREY).move_to([-3.4, -1.15, 0])
        la = lab("assumption A", 22, YELLOW).move_to([-4.7, 0.2, 0]).shift(UP * 0.0)
        lb = lab("assumption B", 22, ORANGE).move_to([-4.7, -0.3, 0])
        la.move_to([-2.5, 0.35, 0]); lb.move_to([-2.5, -0.1, 0])
        n4 = VGroup(sup("n", "4", 28, TEXT), lab(": a fit to data,", 26, TEXT), lab("not a count of channel parts", 26, TEXT))
        n4 = VGroup(VGroup(n4[0], n4[1]).arrange(RIGHT, buff=0.05), n4[2]).arrange(DOWN, aligned_edge=LEFT, buff=0.08)
        n4.move_to([-3.4, -2.15, 0])
        n4.shift(RIGHT * (-3.4 - n4.get_center()[0]))
        ctl1 = chip("test predictions and assumptions", GREEN, 24)
        ctl1 = fit(ctl1, max_w=5.6).move_to([-3.4, -3.2, 0])

        sep = Line([0.0, 3.4, 0], [0.0, -3.4, 0], color=GREY, stroke_width=1.5)
        h2 = lab("Pitfall: unstated assumptions", 26, RED, weight=BOLD)
        h2 = fit(h2, max_w=6.0).move_to([3.4, 3.3, 0])
        st = lab("competitive exclusion is predicted with:", 26, TEXT)
        st = fit(st, max_w=5.7).move_to([3.4, 2.4, 0])
        k1 = chip("one limiting resource", BLUE, 28).move_to([3.4, 1.5, 0])
        k2 = chip("a constant environment", BLUE, 28).move_to([3.4, 0.5, 0])
        k3 = chip("no other check on the winner", BLUE, 28)
        k3 = fit(k3, max_w=5.8).move_to([3.4, -0.5, 0])
        ctl2 = chip("list the conditions with the conclusion", GREEN, 24)
        ctl2 = fit(ctl2, max_w=5.8).move_to([3.4, -2.3, 0])

        self.at("A fit is not")
        self.play(FadeIn(h1), FadeIn(ax), FadeIn(data), FadeIn(ex), run_time=0.7)
        self.at("Several curves")
        self.play(Create(ca, run_time=1.0, rate_func=linear), FadeIn(la), run_time=1.0)
        self.play(Create(cb, run_time=1.0, rate_func=linear), FadeIn(lb), run_time=1.0)
        self.at("n to the fourth")
        self.play(FadeIn(n4, shift=UP * 0.1), run_time=0.5)
        self.at("test predictions")
        self.play(FadeIn(ctl1, shift=UP * 0.15), run_time=0.5)
        self.at("competitive exclusion")
        self.play(FadeIn(sep), FadeIn(h2), FadeIn(st), run_time=0.5)
        self.at("one limiting resource")
        self.play(FadeIn(k1, shift=RIGHT * 0.2), run_time=0.4)
        self.at("constant environment")
        self.play(FadeIn(k2, shift=RIGHT * 0.2), run_time=0.4)
        self.at("no other check")
        self.play(FadeIn(k3, shift=RIGHT * 0.2), run_time=0.4)
        self.at("List the conditions")
        self.play(FadeIn(ctl2, shift=UP * 0.15), run_time=0.5)
        self.finish()


# ---------------------------------------------------------------------------------------------
class S07Unlocked(SpokenScene):
    """Hodgkin and Huxley 1952 (lead with: described, did not prove) and Gause 1930s (in his cultures)."""

    def construct(self):
        # left: Hodgkin and Huxley
        sep = Line([0.0, 3.5, 0], [0.0, -3.5, 0], color=GREY, stroke_width=1.5)
        y1 = lab("1952", 40, GOLD, weight=BOLD).move_to([-3.4, 3.15, 0])
        s1 = lab("Hodgkin & Huxley", 26, GREY).move_to([-3.4, 2.5, 0])
        pl = Pl(-5.9, -0.9, -0.55, 1.95, 0, 22, -80, 50)
        ax = pl.axes()
        ts, V = hodgkin_huxley()
        sel = np.arange(0, len(ts), 8)
        spike = pl.curve(ts[sel], V[sel], YELLOW, 5)
        xl1 = lab("time", 22, GREY).move_to([-3.4, -0.95, 0]); yl1 = lab("voltage", 22, GREY).move_to([-5.0, 2.0, 0])
        tag1 = model_tag([-1.3, 3.15])
        ch1 = chip("equations described the currents", GREEN, 24)
        ch1 = fit(ch1, max_w=5.8).move_to([-3.4, -1.65, 0])
        ch2 = chip("not a proof of a gating mechanism", RED, 24)
        ch2 = fit(ch2, max_w=5.8).move_to([-3.4, -2.45, 0])
        cr = lines("a historical review credits it with", "predicting features of channel gating", size=22, color=GREY, buff=0.04, align=ORIGIN).move_to([-3.4, -3.25, 0])
        # right: Gause
        y2 = lab("1930s", 40, GOLD, weight=BOLD).move_to([3.4, 3.15, 0])
        s2 = lab("Gause", 26, GREY).move_to([3.4, 2.5, 0])
        pr = Pl(0.9, 5.9, -0.55, 1.95, 0, 40, 0, 110)
        ax2 = pr.axes()
        la = lab("P. aurelia", 22, YELLOW).move_to([2.2, 2.0, 0]); lc = lab("P. caudatum", 22, PINK).move_to([4.4, 2.0, 0])
        ta, ya = competition(True); tm, ym = competition(False)
        a1 = pr.curve(ta, ya[:, 0], YELLOW, 5); a2 = pr.curve(ta, ya[:, 1], PINK, 5)
        m1 = pr.curve(tm, ym[:, 0], YELLOW, 5); m2 = pr.curve(tm, ym[:, 1], PINK, 5)
        xl2 = lab("time", 22, GREY).move_to([3.4, -0.95, 0])
        tag2 = model_tag([5.3, 3.15], "schematic")
        alone = lab("alone", 26, TEXT, weight=BOLD).move_to([1.8, 1.45, 0])
        mixed = lab("mixed", 26, TEXT, weight=BOLD).move_to([1.8, 1.45, 0])
        ch3 = chip("aurelia persisted, caudatum declined", PINK, 24)
        ch3 = fit(ch3, max_w=5.8).move_to([3.4, -1.65, 0])
        ch3b = lab("in his cultures", 24, TEXT).move_to([3.4, -2.25, 0])
        ch4 = chip("a test of Lotka-Volterra competition", BLUE, 24)
        ch4 = fit(ch4, max_w=5.8).move_to([3.4, -3.0, 0])

        self.add(sep)
        self.at("described the currents")
        self.play(FadeIn(y1), FadeIn(s1), FadeIn(ch1, shift=UP * 0.15), run_time=0.6)
        self.at("did not prove")
        self.play(FadeIn(ch2, shift=UP * 0.15), run_time=0.5)
        self.at("computed the action potential")
        self.play(FadeIn(ax), FadeIn(xl1), FadeIn(yl1), FadeIn(tag1), run_time=0.4)
        self.play(Create(spike, run_time=1.8, rate_func=linear))
        self.at("conduction speed")
        self.play(Indicate(spike, color=YELLOW, scale_factor=1.0), run_time=0.6)
        self.at("historical review")
        self.play(FadeIn(cr), run_time=0.5)

        self.at("grew two")
        self.play(FadeIn(y2), FadeIn(s2), FadeIn(ax2), FadeIn(xl2), FadeIn(tag2), run_time=0.6)
        self.at("Alone")
        self.play(FadeIn(la), FadeIn(lc), FadeIn(alone), run_time=0.3)
        self.play(Create(a1, run_time=1.6, rate_func=linear), Create(a2, run_time=1.6, rate_func=linear))
        self.at("Mixed")
        self.play(FadeOut(VGroup(a1, a2, alone)), run_time=0.3)
        self.play(FadeIn(mixed), Create(m1, run_time=1.8, rate_func=linear), Create(m2, run_time=1.8, rate_func=linear))
        self.at("in his cultures")
        self.play(FadeIn(ch3, shift=UP * 0.15), FadeIn(ch3b), run_time=0.5)
        self.at("laboratory test")
        self.play(FadeIn(ch4, shift=UP * 0.15), run_time=0.5)
        self.finish()


# ---------------------------------------------------------------------------------------------
class S08Rule(SpokenScene):
    """Huang and Ferrell 1996, Deppmann and colleagues 2008, then the rule."""

    def construct(self):
        sep = Line([0.0, 3.5, 0], [0.0, -3.5, 0], color=GREY, stroke_width=1.5)
        y1 = lab("1996", 40, GOLD, weight=BOLD).move_to([-3.4, 3.15, 0])
        s1 = lab("Huang & Ferrell", 26, GREY).move_to([-3.4, 2.5, 0])
        pl = Pl(-5.9, -0.9, -1.2, 1.9, 0, 3.0, 0, 1.0)
        ax = pl.axes()
        xx = np.linspace(0, 3.0, 200)
        c4 = pl.curve(xx, hill(xx, 4), YELLOW, 5); c5 = pl.curve(xx, hill(xx, 5), YELLOW, 5)
        c1 = pl.curve(xx, hill(xx, 1), GREY, 4)
        xl = lab("stimulus", 22, GREY).move_to([-3.4, -1.55, 0]); yl = lab("response", 22, GREY).move_to([-5.1, 2.0, 0])
        tg = model_tag([-1.3, 3.15])
        n_l = lines("Hill coefficient", "n = 4 to 5", size=22, color=YELLOW, buff=0.12).move_to([-5.0, 1.5, 0]).align_to([-5.8, 0, 0], LEFT)
        one_l = fit(lab("n = 1 (no cooperativity)", 22, GREY), max_w=3.8).move_to([-2.8, -0.75, 0])
        ok1 = chip("oocyte extracts matched", GREEN, 24)
        ok1 = fit(ok1, max_w=5.8).move_to([-3.4, -2.3, 0])
        # right: neurons share a fixed supply
        y2 = lab("2008", 40, GOLD, weight=BOLD).move_to([3.4, 3.15, 0])
        s2 = lab("Deppmann & colleagues", 26, GREY)
        s2 = fit(s2, max_w=5.8).move_to([3.4, 2.5, 0])
        sup_bar = RoundedRectangle(corner_radius=0.12, width=4.8, height=0.5, stroke_color=TEAL, stroke_width=3,
                                   fill_color=TEAL, fill_opacity=0.25).move_to([3.4, 1.7, 0])
        sup_l = lab("NGF made at a constant rate", 24, TEAL).move_to(sup_bar)
        xs = np.linspace(1.35, 5.45, 6)
        neurons = VGroup(*[Circle(radius=0.3, stroke_color=YELLOW, stroke_width=3, fill_color=YELLOW, fill_opacity=0.25).move_to([x, 0.55, 0]) for x in xs])
        feeds = [arr([x, 1.42], [x, 0.9], TEAL, 3, 0.12) for x in xs]
        f1 = chip("feedback on TrkA level", BLUE, 24).move_to([3.4, -0.7, 0])
        f2 = chip("feedback on signal duration", BLUE, 24)
        f2 = fit(f2, max_w=5.8).move_to([3.4, -1.5, 0])
        ok2 = chip("predictions tested in mouse ganglia", GREEN, 24)
        ok2 = fit(ok2, max_w=5.8).move_to([3.4, -2.45, 0])
        sc = lab("schematic", 22, GREY).move_to([5.7, 3.15, 0])
        rule = T("A good fit does not show that the equation's mechanism is the one at work.", 40, TEXT, font=TITLE_FONT)
        rule = VGroup(*[T(s, 42, TEXT, font=TITLE_FONT) for s in ("A good fit does not show", "that the equation's mechanism", "is the one at work.")]).arrange(DOWN, buff=0.3)
        rb = RoundedRectangle(corner_radius=0.2, width=rule.width + 0.9, height=rule.height + 0.9, stroke_color=GOLD, stroke_width=4).move_to(rule)
        rule_g = VGroup(rb, rule)

        self.add(sep)
        self.at("solved the")
        self.play(FadeIn(y1), FadeIn(s1), FadeIn(ax), FadeIn(xl), FadeIn(yl), FadeIn(tg), run_time=0.6)
        self.at("rate equations")
        self.play(Create(c1, run_time=1.0, rate_func=linear), FadeIn(one_l), run_time=1.0)
        self.at("coefficient of")
        self.play(Create(c4, run_time=1.2, rate_func=linear), Create(c5, run_time=1.2, rate_func=linear), FadeIn(n_l))
        self.at("no cooperative enzyme")
        self.play(Indicate(c1, color=GREY, scale_factor=1.0), run_time=0.6)
        self.at("Oocyte extracts matched")
        self.play(FadeIn(ok1, shift=UP * 0.15), run_time=0.5)

        self.at("In 2008")
        self.play(FadeIn(y2), FadeIn(s2), FadeIn(sc), run_time=0.5)
        self.at("for NGF")
        self.play(FadeIn(sup_bar), FadeIn(sup_l), run_time=0.6)
        self.at("constant rate")
        self.play(FadeIn(neurons, lag_ratio=0.1), *[GrowArrow(a) for a in feeds], run_time=1.0)
        nofb = lab("no feedback: no winners", 22, GREY).move_to([3.4, -0.1, 0])
        self.play(FadeIn(nofb), run_time=0.4)
        self.at("TrkA level")
        self.play(FadeOut(nofb), FadeIn(f1, shift=RIGHT * 0.2), run_time=0.5)
        self.at("signal duration")
        self.play(FadeIn(f2, shift=RIGHT * 0.2), run_time=0.5)
        rs = np.random.RandomState(7)
        winners = sorted(rs.choice(6, 3, replace=False).tolist())
        anims = []
        for i, n in enumerate(neurons):
            if i in winners:
                anims.append(n.animate.scale(1.5))
            else:
                anims.append(n.animate.scale(0.55).set_color(PINK))
        self.play(*anims, run_time=1.2)
        self.at("tested in mouse ganglia")
        self.play(FadeIn(ok2, shift=UP * 0.15), run_time=0.5)

        self.at("Keep this rule")
        keepall = Group(*[m for m in self.mobjects])
        self.play(FadeOut(keepall), run_time=0.6)
        self.at("A good fit")
        self.play(FadeIn(rule_g, scale=0.95), run_time=0.9)
        self.finish()


# ---------------------------------------------------------------------------------------------
class S09End(EndCard):
    LINE = "A good fit does not show the model's mechanism is at work."
