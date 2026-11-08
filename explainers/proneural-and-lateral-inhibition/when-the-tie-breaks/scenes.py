"""Proneural genes and lateral inhibition, chapter 4: When Does the Tie Break?  (Biochemistrypedia chaptered film)

COLOR MAP (one color per concept, whole film; same map as the lesson's earlier film and chapters 1-3)
  GREEN  = proneural activity and the neural-precursor fate (winning cells, "neural" labels)
  YELLOW = Delta (chip, meter, the arrows that carry it between cells, the Delta curves)
  BLUE   = Notch activity (chip, meter)
  RED    = inhibition (the Notch-to-Delta arrows inside each cell)
  GREY   = cells, tracks, labels, cells that are held back
  GOLD   = the question, the steepness dials and the round-trip factor

Every number and curve comes from Collier and colleagues' 1996 model as the lesson writes it:
  Notch activity n moves toward f(neighbour Delta), f(x) = x^k / (a + x^k);
  Delta d moves toward g(n), g(x) = 1 / (1 + b x^h);  a = 0.01, b = 100;
  steep example k = h = 2, shallow example k = h = 1, near-threshold example k = h = 2 with b = 12.
The pair, the 37-cell hexagonal sheet and the noisy traces are integrated here; the grid in the last
scenes copies the lesson grid's own update rule (its own scale, not the model's).
"""
import numpy as np
from bp_style import *  # noqa: F401,F403

# ---------------------------------------------------------------- the model
A_CONST = 0.01


def _fg(k, h, b):
    return (lambda x: x ** k / (A_CONST + x ** k)), (lambda x: 1.0 / (1.0 + b * x ** h))


def _fixed(k, h, b):
    f, g = _fg(k, h, b)
    lo, hi = 1e-9, 1.0
    for _ in range(200):
        mid = (lo + hi) / 2
        if g(f(mid)) - mid > 0:
            lo = mid
        else:
            hi = mid
    d = (lo + hi) / 2
    return d, f(d)


STEEP = (2, 2, 100)
SHALLOW = (1, 1, 100)
NEAR = (2, 2, 12)
D_ST, N_ST = _fixed(*STEEP)
D_SH, N_SH = _fixed(*SHALLOW)


def pair_sim(par, dA0, dB0, tmax, dt=0.01, every=5):
    """Integrate the two-cell pair; returns rows (t, dA, dB, nA, nB)."""
    f, g = _fg(*par)
    _, n0 = _fixed(*par)
    dA, dB, nA, nB = dA0, dB0, n0, n0
    out = [(0.0, dA, dB, nA, nB)]
    for i in range(int(round(tmax / dt))):
        ndA = dA + dt * (g(nA) - dA)
        ndB = dB + dt * (g(nB) - dB)
        nnA = nA + dt * (f(dB) - nA)
        nnB = nB + dt * (f(dA) - nB)
        dA, dB, nA, nB = ndA, ndB, nnA, nnB
        if (i + 1) % every == 0:
            out.append(((i + 1) * dt, dA, dB, nA, nB))
    return np.array(out)


SIM_STEEP = pair_sim(STEEP, D_ST * 1.01, D_ST, 22)
SIM_STEEP_01 = pair_sim(STEEP, D_ST * 1.001, D_ST, 22)


def noisy_share(par, sig, tmax, seed, dt=0.02, every=10):
    """Pair with multiplicative noise; returns (t, A's share of the Delta)."""
    f, g = _fg(*par)
    d0, n0 = _fixed(*par)
    rng = np.random.default_rng(seed)
    dA = dB = d0
    nA = nB = n0
    out = []
    for i in range(int(tmax / dt)):
        w = rng.standard_normal(4) * sig * np.sqrt(dt)
        ndA = dA + dt * (g(nA) - dA) + w[0] * d0
        ndB = dB + dt * (g(nB) - dB) + w[1] * d0
        nA, nB = nA + dt * (f(dB) - nA) + w[2] * n0, nB + dt * (f(dA) - nB) + w[3] * n0
        dA, dB = max(ndA, 1e-6), max(ndB, 1e-6)
        if i % every == 0:
            out.append((i * dt, dA / (dA + dB)))
    return np.array(out)


def landscape(par, ulim, N=1201):
    """Height of the 'hill and valleys' picture, from the model's own return map.
    x = A's Delta; one trip round the loop sends x to H(H(x)) with H = g after f.
    u = x - H(x) is the difference between the cells; the flow along u gives a potential.
    By the A <-> B symmetry the picture is mirrored: height(u) = height(|u|)."""
    f, g = _fg(*par)
    H = lambda x: g(f(np.maximum(x, 1e-12)))
    xs = np.linspace(1e-4, 1.5, 6001)
    u = xs - H(xs)
    V = H(H(xs)) - xs
    F = np.gradient(u, xs) * V
    P = -np.concatenate([[0], np.cumsum(0.5 * (F[1:] + F[:-1]) * np.diff(u))])
    ug = np.linspace(-ulim, ulim, N)
    Ps = np.interp(np.abs(ug), u, P)
    Ps = Ps - Ps.min()
    return ug, Ps / Ps.max()


# ---------------------------------------------------------------- layout of the pair
XA, XB = -3.35, 3.35
ROW_T, ROW_B = 0.95, -1.85
CY = -0.35
MXA, MXB = -5.55, 5.55
MH = 0.8
TAG_T, TAG_B = ROW_T + 0.8, ROW_B - 0.8
TOP1, TOP2 = 3.35, 2.8

NODE = {k: np.array([x, y, 0.0]) for k, (x, y) in {"dA": (MXA, TAG_T), "nB": (MXB, TAG_T), "dB": (MXB, TAG_B), "nA": (MXA, TAG_B)}.items()}
# the four dials: on the arrows (top, B inside, bottom, A inside), then on a strip under the loop, then merged in the middle
DIAL_ARROW = [(-0.6, 1.5), (2.43, -0.6), (-0.6, -2.8), (-2.43, -0.6)]
DIAL_VTXT = [(0.82, 1.75), (2.43, -1.05), (0.82, -2.5), (-2.43, -1.05)]
STRIP_X = [-4.9, -2.15, 0.6, 3.35]
STRIP_Y, STRIP_TY = -3.45, -3.3
STEEP_F = [1.3, 1.84, 1.3, 1.84]          # per-step factors read off the 1 -> 1.3 -> 2.4 -> 3.1 -> 5.7 chain


def inhib(a, b, color=RED, w=5):
    a, b = np.array(a, float), np.array(b, float)
    d = (b - a) / np.linalg.norm(b - a)
    b = b - d * 0.04
    perp = np.array([-d[1], d[0], 0])
    return VGroup(Line(a, b, color=color, stroke_width=w), Line(b + perp * 0.26, b - perp * 0.26, color=color, stroke_width=w + 1))


def lerp(p, q, m):
    return np.array([p[0] * (1 - m) + q[0] * m, p[1] * (1 - m) + q[1] * m, 0])


class Ring:
    """Cells A and B, the four nodes of the loop, the four arrows, meters, dials."""

    def __init__(self, d=D_ST, n=N_ST):
        self.v = {k: ValueTracker(x) for k, x in dict(dA=d, nA=n, dB=d, nB=n).items()}
        self.mvis = ValueTracker(1)
        self.bump, self.capvis = ValueTracker(0), ValueTracker(1)
        self.dlevel, self.dvis, self.dmove = ValueTracker(0.5), ValueTracker(0), ValueTracker(0)
        self.tvis, self.fmode = ValueTracker(1), ValueTracker(0)
        self.fv = [ValueTracker(x) for x in STEEP_F]
        self.biglevel, self.bigvis = ValueTracker(0.5), ValueTracker(0)
        self.cellA = RoundedRectangle(corner_radius=0.3, width=5.15, height=5.1, stroke_color=GREY, stroke_width=4,
                                      fill_color=GREY, fill_opacity=0.08).move_to([-4.075, CY, 0])
        self.cellB = self.cellA.copy().move_to([4.075, CY, 0])
        self.labA = T("cell A", 26, GREY).move_to([XA, 1.8, 0])
        self.labB = T("cell B", 26, GREY).move_to([XB, 1.8, 0])
        self.g_cells = VGroup(self.cellA, self.cellB, self.labA, self.labB)
        self.c_dA = chip("Delta", YELLOW, 26, pad=0.16).move_to([XA, ROW_T, 0])
        self.c_nA = chip("Notch activity", BLUE, 24, pad=0.16).move_to([XA, ROW_B, 0])
        self.c_nB = chip("Notch activity", BLUE, 24, pad=0.16).move_to([XB, ROW_T, 0])
        self.c_dB = chip("Delta", YELLOW, 26, pad=0.16).move_to([XB, ROW_B, 0])
        self.g_chips = VGroup(self.c_dA, self.c_nA, self.c_nB, self.c_dB)
        hh = self.c_dA.height / 2
        self.s_top = Arrow([self.c_dA.get_right()[0] + 0.05, ROW_T, 0], [self.c_nB.get_left()[0] - 0.05, ROW_T, 0], buff=0, color=YELLOW,
                           stroke_width=5, tip_length=0.24)
        self.s_bot = Arrow([self.c_dB.get_left()[0] - 0.05, ROW_B, 0], [self.c_nA.get_right()[0] + 0.05, ROW_B, 0], buff=0, color=YELLOW,
                           stroke_width=5, tip_length=0.24)
        self.s_inB = inhib([XB, ROW_T - hh - 0.05, 0], [XB, ROW_B + hh + 0.05, 0])
        self.s_inA = inhib([XA, ROW_B + hh + 0.05, 0], [XA, ROW_T - hh - 0.05, 0])
        self.g_yel = VGroup(self.s_top, self.s_bot)
        self.g_inh = VGroup(self.s_inA, self.s_inB)
        self.g_arrows = VGroup(self.s_top, self.s_inB, self.s_bot, self.s_inA)   # path order
        self.seg = [(np.array([self.c_dA.get_right()[0] + 0.1, ROW_T, 0]), np.array([self.c_nB.get_left()[0] - 0.1, ROW_T, 0])),
                    (np.array([XB, ROW_T - hh - 0.1, 0]), np.array([XB, ROW_B + hh + 0.1, 0])),
                    (np.array([self.c_dB.get_left()[0] - 0.1, ROW_B, 0]), np.array([self.c_nA.get_right()[0] + 0.1, ROW_B, 0])),
                    (np.array([XA, ROW_B + hh + 0.1, 0]), np.array([XA, ROW_T - hh - 0.1, 0]))]
        self.meters = [self._meter(MXA, ROW_T, "dA", YELLOW), self._meter(MXB, ROW_T, "nB", BLUE),
                       self._meter(MXB, ROW_B, "dB", YELLOW), self._meter(MXA, ROW_B, "nA", BLUE)]
        self.cap = always_redraw(self._cap)
        self.dials = [always_redraw(lambda i=i: self._dial(i)) for i in range(4)]
        self.dtexts = [always_redraw(lambda i=i: self._dtext(i)) for i in range(4)]
        self.big = always_redraw(self._big)
        self.dyn = self.meters + [self.cap] + self.dials + self.dtexts + [self.big]

    # ---- meters, cap, dials
    def _meter(self, x, y, key, color):
        def mk():
            vis = self.mvis.get_value()
            h = max(1e-3, np.sqrt(max(self.v[key].get_value(), 0.0)) * MH)
            track = Rectangle(width=0.3, height=MH, stroke_color=GREY, stroke_width=2, fill_opacity=0).move_to([x, y, 0]).set_stroke(opacity=0.6 * vis)
            fill = Rectangle(width=0.3, height=h, stroke_width=0, fill_color=color, fill_opacity=0.92 * vis).move_to([x, y - MH / 2 + h / 2, 0])
            return VGroup(track, fill)
        return always_redraw(mk)

    def _cap(self):
        top = ROW_T - MH / 2 + max(1e-3, np.sqrt(max(self.v["dA"].get_value(), 0.0)) * MH)
        h = max(1e-3, self.bump.get_value())
        vis = self.capvis.get_value()
        return Rectangle(width=0.3, height=h, stroke_width=0, fill_color="#FFF3B0", fill_opacity=0.95 * vis).move_to([MXA, top + h / 2, 0])

    def _dial_pos(self, i):
        m = self.dmove.get_value()
        a, s, c = np.array([*DIAL_ARROW[i], 0.0]), np.array([STRIP_X[i], STRIP_Y, 0.0]), np.array([0.0, -0.3, 0.0])
        return lerp(a, s, m) if m <= 1 else lerp(s, c, m - 1)

    def _dial_r(self):
        m = self.dmove.get_value()
        return 0.55 - 0.18 * min(m, 1) - 0.12 * max(m - 1, 0)

    def _gauge(self, pos, r, level, vis, sw=3.5):
        ang = np.radians(12 + 66 * level)
        arc = Arc(radius=r, start_angle=0, angle=PI, arc_center=pos, color=GREY, stroke_width=sw, stroke_opacity=vis)
        base = Line(pos + LEFT * r, pos + RIGHT * r, color=GREY, stroke_width=sw, stroke_opacity=vis)
        needle = Line(pos, pos + 0.88 * r * np.array([np.cos(ang), np.sin(ang), 0]), color=GOLD, stroke_width=sw + 1.5, stroke_opacity=vis)
        hub = Dot(pos, radius=0.07 * (r / 0.5) ** 0.5, color=GOLD, fill_opacity=vis)
        return VGroup(arc, base, needle, hub)

    def _dial(self, i):
        return self._gauge(self._dial_pos(i), self._dial_r(), self.dlevel.get_value(), self.dvis.get_value(), sw=5)

    def _dtext(self, i):
        m = min(self.dmove.get_value(), 1)
        p = lerp(DIAL_VTXT[i], (STRIP_X[i] + 1.15, STRIP_TY), m)
        if self.fmode.get_value() > 0.5:
            s = "small"
        else:
            s = "×" + ("%.2f" % self.fv[i].get_value()).rstrip("0").rstrip(".")
        t = M(s, 26, GOLD).move_to([p[0], p[1], 0])
        return t.set_opacity(self.dvis.get_value() * self.tvis.get_value())

    def _big(self):
        return self._gauge(np.array([0.0, -0.3, 0.0]), 0.85, self.biglevel.get_value(), self.bigvis.get_value(), sw=6)

    # ---- state helpers
    def set_even(self, shallow=False):
        d, n = (D_SH, N_SH) if shallow else (D_ST, N_ST)
        for k, val in dict(dA=d, nA=n, dB=d, nB=n).items():
            self.v[k].set_value(val)

    def to(self, **kw):
        return [self.v[k].animate.set_value(x) for k, x in kw.items()]

    def toq(self, rt, **kw):
        return [self.v[k].animate(run_time=rt).set_value(x) for k, x in kw.items()]

    def mount(self, scene, cells=True, chips=True, yel=True, inh=True, meters=True):
        if cells:
            scene.add(self.g_cells)
        if chips:
            scene.add(self.g_chips)
        if yel:
            scene.add(self.g_yel)
        if inh:
            scene.add(self.g_inh)
        if meters:
            scene.add(*self.dyn)

    def dot(self):
        return Dot(radius=0.15, color=TEXT).move_to(self.seg[0][0])

    def tag(self, key, text, color=None, size=26):
        col = color or (YELLOW if key in ("dA", "dB") else BLUE)
        return M(text, size, col).move_to(NODE[key])

    def win(self, which):
        c, l = (self.cellA, self.labA) if which == "A" else (self.cellB, self.labB)
        return [c.animate.set_stroke(GREEN, 6).set_fill(GREEN, 0.2), l.animate.set_color(GREEN)]

    def lose(self, which):
        c, l = (self.cellA, self.labA) if which == "A" else (self.cellB, self.labB)
        return [c.animate.set_stroke(GREY, 4, opacity=0.5).set_fill(GREY, 0.04), l.animate.set_color(GREY).set_opacity(0.6)]

    def neutral(self):
        return [self.cellA.animate.set_stroke(GREY, 4, opacity=1).set_fill(GREY, 0.08), self.cellB.animate.set_stroke(GREY, 4, opacity=1).set_fill(GREY, 0.08),
                self.labA.animate.set_color(GREY).set_opacity(1), self.labB.animate.set_color(GREY).set_opacity(1)]


def play_pair(scene, R, arr, run_time, i0=0, i1=None, rate_func=linear):
    """Drive the four meters with the integrated pair, rows i0..i1 of arr."""
    i1 = len(arr) - 1 if i1 is None else i1
    s = ValueTracker(0)
    holder = Mobject()

    def upd(_):
        i = int(round(i0 + s.get_value() * (i1 - i0)))
        R.v["dA"].set_value(arr[i][1])
        R.v["dB"].set_value(arr[i][2])
        R.v["nA"].set_value(arr[i][3])
        R.v["nB"].set_value(arr[i][4])
    holder.add_updater(upd)
    scene.add(holder)
    scene.play(s.animate.set_value(1), run_time=run_time, rate_func=rate_func)
    holder.remove_updater(upd)
    scene.remove(holder)


def until(scene, t):
    r = t - scene.elapsed()
    if r > 0.02:
        scene.wait(r)


def travel_anim(R, dot, segs, each=0.25):
    return Succession(*[dot.animate(run_time=each, rate_func=linear).move_to(R.seg[i][1]) for i in segs])


def travel(scene, R, dot, segs, each=0.25):
    for i in segs:
        a, b = R.seg[i]
        scene.play(dot.animate.move_to(b), run_time=each, rate_func=linear)


def prompt_lines():
    p1 = T("Predict.", 34, GOLD, weight=BOLD)
    p2 = T("A has 1% more Delta than B.", 28, TEXT, t2c={"Delta": YELLOW})
    pg = VGroup(p1, p2).arrange(RIGHT, buff=0.3, aligned_edge=DOWN).move_to([0, TOP1, 0])
    p3 = T("Does the difference grow?", 32, GOLD).move_to([0, TOP2, 0])
    return p1, p2, p3


def bump_tag():
    return M("+1%", 26, YELLOW).move_to([MXA, TAG_T, 0])


def clock(pos, r=0.42):
    face = Circle(radius=r, stroke_color=GOLD, stroke_width=4, fill_opacity=0).move_to(pos)
    hand = Line(pos, pos + UP * r * 0.8, color=GOLD, stroke_width=5)
    knob = Line(pos + UP * (r + 0.02), pos + UP * (r + 0.16), color=GOLD, stroke_width=5)
    return VGroup(face, knob), hand


def hdr(sub_text="worked example: steep responses"):
    name = T("Collier and colleagues, 1996 model", 30, TEXT).move_to([0, TOP1, 0])
    sub = T(sub_text, 26, TEXT).move_to([0, TOP2, 0])
    return name, sub


def foot(text, color=GOLD, y=-3.3):
    return T(text, 34, color).move_to([0, y, 0])


TALLY_Y = [0.6, 0.1, -0.4, -0.9, -1.42]
TALLY = [("1%", YELLOW, 38), ("1.3%", BLUE, 38), ("2.4%", YELLOW, 38), ("3.1%", BLUE, 38), ("5.7%", YELLOW, 44)]


def tally_vals():
    return [M(t, s, c).move_to([0, y, 0]) for (t, c, s), y in zip(TALLY, TALLY_Y)]


def tally_holes():
    return [T("?", 40, GREY).move_to([0, y, 0]) for y in TALLY_Y]


def cmp_col(cx, label, lcol, thick, level, txt, tcol, tip=0.2):
    """One column of the shallow-versus-steep comparison that sits in the middle gap."""
    lab = T(label, 28, lcol).move_to([cx, 0.52, 0])
    arr = Arrow([cx - 0.66, 0.12, 0], [cx + 0.66, 0.12, 0], buff=0, color=TEXT, stroke_width=thick, tip_length=tip, max_tip_length_to_length_ratio=0.5)
    gau = Ring._gauge(None, np.array([cx, -0.6, 0.0]), 0.58, level, 1, sw=4)
    t = T(txt, 24, tcol, line_spacing=0.7).move_to([cx, -1.3, 0])
    return VGroup(lab, arr, gau, t)


def drive(R, arr, i0, i1):
    """Updater holder + tracker: play  s.animate(run_time=..).set_value(1)  to run the integrated pair from row i0 to i1."""
    s = ValueTracker(0)
    holder = Mobject()

    def upd(_):
        i = int(round(i0 + s.get_value() * (i1 - i0)))
        R.v["dA"].set_value(arr[i][1])
        R.v["dB"].set_value(arr[i][2])
        R.v["nA"].set_value(arr[i][3])
        R.v["nB"].set_value(arr[i][4])
    holder.add_updater(upd)
    return s, holder


def row_at(arr, t):
    return int(np.argmin(abs(arr[:, 0] - t)))


# ---------------------------------------------------------------- plots
class Plot:
    def __init__(self, left, right, bottom, top, xmax, ymax):
        self.l, self.r, self.b, self.t, self.xm, self.ym = left, right, bottom, top, xmax, ymax

    def P(self, x, y):
        return np.array([self.l + (self.r - self.l) * x / self.xm, self.b + (self.t - self.b) * y / self.ym, 0])

    def axes(self, color=GREY):
        return VGroup(Line(self.P(0, 0), self.P(self.xm, 0), color=color, stroke_width=3),
                      Line(self.P(0, 0), self.P(0, self.ym), color=color, stroke_width=3))

    def curve(self, xs, ys, color, dashed=False, width=5):
        pts = [self.P(x, y) for x, y in zip(xs, ys)]
        m = VMobject(stroke_color=color, stroke_width=width).set_points_as_corners(pts)
        if dashed:
            return DashedVMobject(m, num_dashes=90, dashed_ratio=0.55)
        return m


# ---------------------------------------------------------------- hexagonal sheet
RL = 0.56   # lattice radius
RD = 0.52   # drawn radius


def hex_cells(rad=3):
    cells = [(q, r) for q in range(-rad, rad + 1) for r in range(-rad, rad + 1) if abs(q + r) <= rad]
    idx = {c: i for i, c in enumerate(cells)}
    dirs = [(1, 0), (1, -1), (0, -1), (-1, 0), (-1, 1), (0, 1)]
    nb = [[idx[(q + dq, r + dr)] for dq, dr in dirs if (q + dq, r + dr) in idx] for q, r in cells]
    return cells, nb


CELLS, NBRS = hex_cells(3)


def hpos(q, r, R, cx, cy):
    return np.array([cx + R * np.sqrt(3) * (q + r / 2), cy - 1.5 * R * r, 0])


def make_hex(q, r, R, rd, cx, cy):
    return RegularPolygon(6, radius=rd, start_angle=PI / 6, stroke_color=GREY, stroke_width=2.5, fill_color=GREY,
                          fill_opacity=0.08).move_to(hpos(q, r, R, cx, cy))


def sheet_sim(seed=0, T_end=60.0, dt=0.05, amp=0.05, every=10):
    f, g = _fg(*STEEP)
    rng = np.random.default_rng(seed)
    d = D_ST * (1 + amp * rng.standard_normal(len(CELLS)))
    n = np.full(len(CELLS), N_ST)
    out = [d.copy()]
    for i in range(int(T_end / dt)):
        mean = np.array([d[j].mean() for j in NBRS])
        n = n + dt * (f(mean) - n)
        d = d + dt * (g(n) - d)
        if (i + 1) % every == 0:
            out.append(d.copy())
    return np.array(out)


SHEET = sheet_sim()
SHEET_WIN = SHEET[-1] > 0.5
SX, SY = -2.9, -0.2


def build_sheet(cx=SX, cy=SY):
    return {c: make_hex(c[0], c[1], RL, RD, cx, cy) for c in CELLS}


def set_cell(h, d):
    d = float(min(1, max(0, d)))
    win = d > 0.5
    h.set_fill(GREEN, 0.1 + 0.8 * d)
    h.set_stroke(GREEN if win else GREY, 4 if win else 2.5, opacity=1 if win else 0.7)


# ================================================================= scenes
class S00Title(TitleCard):
    LESSON = "Proneural genes and lateral inhibition"
    TITLE = "When Does the Tie Break?"


# ---------------------------------------------------------------------------------------------
class S01Question(SpokenScene):
    def construct(self):
        R = Ring()
        R.mount(self)
        lb1 = T("Delta level", 22, YELLOW).move_to([-5.55, 1.62, 0])
        lb2 = T("Notch activity", 22, BLUE).move_to([-5.3, -2.58, 0])
        self.play(FadeIn(lb1), FadeIn(lb2), run_time=0.25)
        self.at("inhibitions")
        self.play(LaggedStart(*[Indicate(a, color=TEXT, scale_factor=1.2) for a in R.g_inh], lag_ratio=0.5), run_time=0.9)
        self.at("positive feedback")
        trace = VGroup(*[Line(a, b, color=GREEN, stroke_width=11, stroke_opacity=0.85) for a, b in R.seg])
        lt = T("positive\nfeedback", 26, GREEN, line_spacing=0.7).move_to([0, CY + 0.1, 0])
        self.play(Succession(*[Create(l, rate_func=linear, run_time=0.32) for l in trace]), FadeIn(lt, run_time=0.8))
        self.at("but is positive")
        q = T("Is positive feedback always enough\nto split two equal cells?", 28, TEXT, line_spacing=0.8).move_to([0, 3.05, 0])
        self.play(FadeOut(trace), FadeOut(lt), FadeOut(lb1), FadeOut(lb2), Write(q), run_time=1.5)
        self.at("split two equal cells")
        self.play(Indicate(R.cellA, color=TEXT, scale_factor=1.03), Indicate(R.cellB, color=TEXT, scale_factor=1.03), run_time=0.9)
        self.finish()


class S02Predict(SpokenScene):
    def construct(self):
        R = Ring()
        R.mount(self)
        q = T("Is positive feedback always enough\nto split two equal cells?", 28, TEXT, line_spacing=0.8).move_to([0, 3.05, 0])
        self.add(q)
        p1, p2, p3 = prompt_lines()
        self.play(ReplacementTransform(q, p1), run_time=0.7)
        self.at("give cell")
        self.play(FadeIn(p2, shift=LEFT * 0.2), run_time=0.6)
        self.at("more delta")
        tag = bump_tag()
        self.play(R.bump.animate.set_value(0.11), FadeIn(tag, shift=DOWN * 0.1), run_time=0.7)
        self.play(Indicate(R.c_dA, color=YELLOW, scale_factor=1.08), run_time=0.7)
        self.at("does the difference")
        self.play(FadeIn(p3, shift=UP * 0.15), run_time=0.7)
        self.finish()


class S03Pause(NarratedScene):
    def construct(self):
        R = Ring()
        R.bump.set_value(0.11)
        R.mount(self)
        p1, p2, p3 = prompt_lines()
        tag = bump_tag()
        cpos = np.array([0.0, CY, 0.0])
        face, hand = clock(cpos, r=0.85)
        self.add(p1, p2, p3, tag, face, hand)
        self.play(Rotate(hand, angle=-2 * PI, about_point=cpos, rate_func=linear), run_time=4.6)
        self.finish()


class S04No(SpokenScene):
    def construct(self):
        R = Ring()
        R.bump.set_value(0.11)
        R.mount(self)
        p1, p2, p3 = prompt_lines()
        tag = bump_tag()
        self.add(p1, p2, p3, tag)
        s0 = T("No.", 30, GOLD, weight=BOLD)
        s1 = T("The difference must come back", 28, TEXT)
        s2 = T("round the loop", 28, GOLD)
        l1 = VGroup(s0, s1, s2).arrange(RIGHT, buff=0.22).move_to([0, TOP1, 0])
        l2 = T("larger than it left.", 28, TEXT).move_to([0, TOP2, 0])
        self.play(FadeOut(p1), FadeOut(p2), FadeOut(p3), FadeIn(s0, scale=0.8), run_time=0.5)
        self.at("the difference must")
        self.play(FadeIn(s1, shift=UP * 0.1), run_time=0.7)
        self.at("round the loop")
        dot = R.dot()
        self.add(dot)
        self.play(FadeIn(s2, shift=UP * 0.1), travel_anim(R, dot, [0, 1, 2, 3], each=0.2))
        self.at("larger than it left")
        self.play(FadeIn(l2, shift=UP * 0.1), R.bump.animate.set_value(0.4), FadeOut(dot), run_time=0.8)
        self.finish()


def step_marker(x, y, up, color):
    m = Triangle(fill_color=color, fill_opacity=1, stroke_color=TEXT, stroke_width=2).scale(0.3)
    if not up:
        m.rotate(PI)
    return m.move_to([x, y, 0])


class S05Round(SpokenScene):
    def construct(self):
        R = Ring()
        R.bump.set_value(0.11)
        R.mount(self)
        tag = bump_tag()
        self.add(tag)

        def cap(txt):
            return T(txt, 38, TEXT, t2c={"Notch activity": BLUE, "Delta": YELLOW}).move_to([0, 3.2, 0])
        c0 = cap("Follow the 1% round the loop")
        self.add(c0)
        self.at("follow it round")
        dot = R.dot()
        self.play(FadeIn(dot, scale=0.5), Indicate(R.c_dA, color=YELLOW, scale_factor=1.08), run_time=0.8)
        self.at("b's notch")
        c1 = cap("B's Notch activity rises")
        up = step_marker(5.0, ROW_T, True, BLUE)
        self.play(dot.animate(run_time=0.45, rate_func=linear).move_to(R.seg[0][1]), ReplacementTransform(c0, c1, run_time=0.45))
        self.play(*R.toq(0.6, nB=0.55), FadeIn(up, scale=1.6, run_time=0.5))
        self.at("b's delta")
        c2 = cap("B's Delta falls")
        dn = step_marker(5.0, ROW_B, False, YELLOW)
        self.play(dot.animate(run_time=0.4, rate_func=linear).move_to(R.seg[1][1]), ReplacementTransform(c1, c2, run_time=0.4))
        self.play(*R.toq(0.6, dB=0.02), FadeIn(dn, scale=1.6, run_time=0.5))
        self.at("then a's notch")
        c3 = cap("A's Notch activity falls")
        dn2 = step_marker(-5.0, ROW_B, False, BLUE)
        self.play(dot.animate(run_time=0.45, rate_func=linear).move_to(R.seg[2][1]), ReplacementTransform(c2, c3, run_time=0.45))
        self.play(*R.toq(0.6, nA=0.22), FadeIn(dn2, scale=1.6, run_time=0.5))
        self.at("a's delta")
        c4 = cap("A's Delta rises")
        up2 = step_marker(-5.0, ROW_T, True, YELLOW)
        self.play(dot.animate(run_time=0.4, rate_func=linear).move_to(R.seg[3][1]), ReplacementTransform(c3, c4, run_time=0.4))
        self.play(*R.toq(0.6, dA=0.2), R.bump.animate(run_time=0.6).set_value(0.3), FadeIn(up2, scale=1.6, run_time=0.5), FadeOut(dot, run_time=0.4))
        self.play(Indicate(up2, color=TEXT, scale_factor=1.3), run_time=0.6)
        self.finish()


HEAD6 = "each dial: how steep the step is  →  its factor"


class S06Factor(SpokenScene):
    def construct(self):
        R = Ring()
        R.dlevel.set_value(0.9)
        R.mount(self)
        self.at("each step")
        self.play(LaggedStart(*[Indicate(a, color=TEXT, scale_factor=1.05) for a in R.g_arrows], lag_ratio=0.35), run_time=1.6)
        self.at("multiplied by a factor")
        head = T(HEAD6, 28, TEXT).move_to([0, 3.25, 0])
        self.play(R.dvis.animate.set_value(1), FadeIn(head, shift=DOWN * 0.1), run_time=0.8)
        self.at("the steeper")
        shallow = cmp_col(-0.76, "shallow", GREY, 2.5, 0.1, "small\nfactor", GREY, tip=0.16)
        steep = cmp_col(0.76, "steep", TEXT, 11, 0.55, "bigger\nfactor", GOLD, tip=0.3)
        self.play(FadeIn(shallow, shift=UP * 0.1), FadeIn(steep, shift=UP * 0.1), run_time=0.9)
        self.at("the bigger")
        steep2 = cmp_col(0.76, "steep", TEXT, 20, 0.95, "big\nfactor", GOLD, tip=0.34)
        self.play(Transform(steep, steep2), R.g_arrows.animate.set_stroke(width=12), run_time=0.9)
        self.finish()


class S07Factor2(SpokenScene):
    def construct(self):
        R = Ring()
        R.dvis.set_value(1)
        R.dlevel.set_value(0.9)
        R.mount(self)
        R.g_arrows.set_stroke(width=12)
        head = T(HEAD6, 28, TEXT).move_to([0, 3.25, 0])
        shallow = cmp_col(-0.76, "shallow", GREY, 2.5, 0.1, "small\nfactor", GREY, tip=0.16)
        steep = cmp_col(0.76, "steep", TEXT, 20, 0.95, "big\nfactor", GOLD, tip=0.34)
        self.add(head, shallow, steep)
        self.at("multiply the factors")
        self.play(FadeOut(head), FadeOut(shallow), FadeOut(steep), R.tvis.animate.set_value(0), R.g_arrows.animate.set_stroke(width=5), run_time=0.3)
        self.play(R.dmove.animate.set_value(1), run_time=0.65)
        self.play(R.tvis.animate.set_value(1), run_time=0.2)
        self.at("all the way round")
        dot = R.dot()
        self.play(FadeIn(dot, scale=0.5), run_time=0.2)
        travel(self, R, dot, [0, 1, 2, 3], each=0.25)
        self.play(FadeOut(dot), run_time=0.15)
        self.at("that product")
        self.play(R.tvis.animate(run_time=0.3).set_value(0), R.dmove.animate(run_time=0.9).set_value(2), R.dvis.animate(run_time=0.9, rate_func=rush_into).set_value(0),
                  R.bigvis.animate(run_time=0.9).set_value(1), R.biglevel.animate(run_time=0.9).set_value(0.93))
        prod = M("×5.7", 40, GOLD).move_to([0, -0.78, 0])
        self.play(FadeIn(prod, shift=UP * 0.1), run_time=0.4)
        self.at("round trip factor")
        bl = T("round-trip factor", 24, GOLD).move_to([0, -1.32, 0])
        self.play(FadeIn(bl, shift=UP * 0.1), run_time=0.6)
        self.finish()


class S08Collier(SpokenScene):
    def construct(self):
        R = Ring()
        R.mount(self)
        self.at("collier")
        name = T("Collier and colleagues, 1996 model", 30, TEXT).move_to([0, TOP1, 0])
        self.play(Write(name), run_time=1.5)
        ph = tally_holes()
        vals = tally_vals()
        self.play(LaggedStart(*[FadeIn(p, scale=0.7) for p in ph], lag_ratio=0.3), run_time=1.2)
        self.at("with steep responses")
        sub = T("worked example: steep responses", 26, TEXT).move_to([0, TOP2, 0])
        R.dlevel.set_value(0.9)
        self.play(FadeIn(sub, shift=UP * 0.1), R.dvis.animate.set_value(1), run_time=0.9)
        self.at("the 1")
        t1 = R.tag("dA", "+1%")
        self.play(FadeIn(t1, scale=1.3), ReplacementTransform(ph[0], vals[0]), R.bump.animate.set_value(0.11), run_time=0.4)
        self.at("comes back")
        dot = R.dot()
        self.add(dot)
        steps = [("nB", "+1.3%", dict(nB=0.5)), ("dB", "-2.4%", dict(dB=0.03)), ("nA", "-3.1%", dict(nA=0.25))]
        for i, (key, txt, mv) in enumerate(steps):
            self.play(dot.animate(run_time=0.17, rate_func=linear).move_to(R.seg[i][1]))
            self.play(FadeIn(R.tag(key, txt), scale=1.3, run_time=0.15), ReplacementTransform(ph[i + 1], vals[i + 1], run_time=0.15), *R.toq(0.15, **mv))
        self.play(dot.animate(run_time=0.17, rate_func=linear).move_to(R.seg[3][1]))
        t5 = R.tag("dA", "+5.7%")
        self.play(ReplacementTransform(t1, t5, run_time=0.25), ReplacementTransform(ph[4], vals[4], run_time=0.25), FadeOut(dot, run_time=0.2),
                  R.bump.animate(run_time=0.4).set_value(0.5), *R.toq(0.4, dA=0.12))
        f1 = foot("round-trip factor about 5.7")
        self.play(FadeIn(f1, shift=UP * 0.1), run_time=0.5)
        self.finish()


class S09Steep(SpokenScene):
    def construct(self):
        R = Ring()
        R.dvis.set_value(1)
        R.dlevel.set_value(0.9)
        R.bump.set_value(0.11)
        R.mount(self)
        name, sub = hdr("worked example: steep responses")
        tag = bump_tag()
        self.add(name, sub, tag)
        dot = R.dot()
        self.add(dot)
        arr = SIM_STEEP
        lab = M("pass 1", 32, GOLD).move_to([0, -0.2, 0])
        self.play(FadeIn(lab, run_time=0.3), travel_anim(R, dot, [0, 1, 2, 3], each=0.1), *R.toq(0.4, nB=0.40, dB=0.062, nA=0.31), R.bump.animate(run_time=0.4).set_value(0.26))
        lab2 = M("pass 2", 32, GOLD).move_to([0, -0.2, 0])
        self.play(ReplacementTransform(lab, lab2, run_time=0.2), travel_anim(R, dot, [0, 1, 2, 3], each=0.1), *R.toq(0.4, nB=0.5, dB=0.04, nA=0.22), R.bump.animate(run_time=0.4).set_value(0.4))
        lab3 = M("pass 3", 32, GOLD).move_to([0, -0.2, 0])
        s, holder = drive(R, arr, row_at(arr, 13.0), row_at(arr, 15.5))
        self.add(holder)
        self.play(ReplacementTransform(lab2, lab3, run_time=0.2), travel_anim(R, dot, [0, 1, 2, 3], each=0.1), s.animate(run_time=0.4, rate_func=linear).set_value(1),
                  R.bump.animate(run_time=0.4).set_value(0.0))
        holder.clear_updaters()
        self.remove(holder)
        self.at("the pair splits")
        s2, holder2 = drive(R, arr, row_at(arr, 15.5), row_at(arr, 20.0))
        self.add(holder2)
        self.play(s2.animate(run_time=0.7, rate_func=linear).set_value(1), *R.win("A"), *R.lose("B"), FadeOut(lab3), FadeOut(dot), FadeOut(tag))
        holder2.clear_updaters()
        self.remove(holder2)
        self.finish()


class S10Shallow(SpokenScene):
    def construct(self):
        R = Ring()
        R.v["dA"].set_value(0.9)
        R.v["dB"].set_value(0.02)
        R.v["nA"].set_value(0.02)
        R.v["nB"].set_value(0.9)
        R.dlevel.set_value(0.9)
        R.dvis.set_value(1)
        R.mount(self)
        R.cellA.set_stroke(GREEN, 6).set_fill(GREEN, 0.2)
        R.labA.set_color(GREEN)
        R.cellB.set_stroke(GREY, 4, opacity=0.5).set_fill(GREY, 0.04)
        R.labB.set_color(GREY).set_opacity(0.6)
        name, sub = hdr("worked example: steep responses")
        self.add(name, sub)
        self.at("with shallow responses")
        sub2 = T("worked example: shallow responses", 26, TEXT).move_to([0, TOP2, 0])
        # the swap is one quick beat (0.12 s): the steep result never sits beside the shallow dials
        self.play(*R.neutral(), *R.toq(0.12, dA=D_SH, dB=D_SH, nA=N_SH, nB=N_SH), R.dlevel.animate(run_time=0.12).set_value(0.2), R.fmode.animate(run_time=0.12).set_value(1),
                  ReplacementTransform(sub, sub2, run_time=0.12), run_time=0.12)
        self.at("the same 1")
        t1 = R.tag("dA", "+1%")
        r1 = M("1%", 32, YELLOW).move_to([0, 0.45, 0])
        self.play(FadeIn(t1, scale=1.3), FadeIn(r1), R.bump.animate.set_value(0.11), run_time=0.5)
        self.at("comes back")
        dot = R.dot()
        self.add(dot)
        travel(self, R, dot, [0, 1, 2, 3], each=0.25)
        self.at("about a seventh")
        t2 = R.tag("dA", "+0.14%")
        r2 = M("0.14%", 32, YELLOW).move_to([0, -0.7, 0])
        dn = Arrow([0, 0.1, 0], [0, -0.3, 0], buff=0, color=GREY, stroke_width=4, tip_length=0.18)
        self.play(ReplacementTransform(t1, t2), R.bump.animate.set_value(0.008), FadeOut(dot), FadeIn(dn), FadeIn(r2, shift=DOWN * 0.1), run_time=0.5)
        f1 = foot("round-trip factor below 1: about 0.14")
        self.play(FadeIn(f1, shift=UP * 0.1), run_time=0.5)
        self.finish()


class S11Shallow2(SpokenScene):
    def construct(self):
        R = Ring(D_SH, N_SH)
        R.dlevel.set_value(0.2)
        R.dvis.set_value(1)
        R.fmode.set_value(1)
        R.bump.set_value(0.008)
        R.mount(self)
        name, sub = hdr("worked example: shallow responses")
        t2 = R.tag("dA", "+0.14%")
        f1 = foot("round-trip factor below 1: about 0.14")
        r1 = M("1%", 32, YELLOW).move_to([0, 0.45, 0])
        dn = Arrow([0, 0.1, 0], [0, -0.3, 0], buff=0, color=GREY, stroke_width=4, tip_length=0.18)
        r2 = M("0.14%", 32, YELLOW).move_to([0, -0.7, 0])
        self.add(name, sub, t2, f1, r1, dn, r2)
        # A and B side by side in the middle gap; the push is drawn larger than 1% so that it can be seen
        sim = pair_sim(SHALLOW, D_SH * 1.8, D_SH, 6.0, every=2)
        R.v["dA"].set_value(sim[0][1])
        R.v["dB"].set_value(sim[0][2])
        scl = 1.5 / np.sqrt(D_SH * 1.8)
        BASE = -1.1

        def bars():
            g = VGroup()
            for key, x in (("dA", -0.7), ("dB", 0.7)):
                h = max(1e-3, np.sqrt(R.v[key].get_value()) * scl)
                g.add(Rectangle(width=0.55, height=h, stroke_width=0, fill_color=YELLOW, fill_opacity=0.92).move_to([x, BASE + h / 2, 0]))
            return g
        bar = always_redraw(bars)
        la = T("A", 28, YELLOW).move_to([-0.7, BASE - 0.28, 0])
        lb = T("B", 28, YELLOW).move_to([0.7, BASE - 0.28, 0])
        note = T("push drawn larger than 1% so it can be seen", 32, GREY).move_to([0, -3.3, 0])
        self.at("the difference fades")
        self.play(FadeOut(t2), FadeOut(f1), FadeOut(r1), FadeOut(r2), FadeOut(dn), R.bump.animate.set_value(0.0), FadeIn(la), FadeIn(lb), FadeIn(bar), run_time=0.5)
        s, holder = drive(R, sim, 0, row_at(sim, 4.0))
        self.add(holder)
        self.play(s.animate(run_time=1.2, rate_func=linear).set_value(1), FadeIn(note, run_time=0.5))
        holder.clear_updaters()
        self.remove(holder)
        self.at("the two cells stay alike")
        eq = T("=", 60, TEXT, weight=BOLD).move_to([0, BASE + 0.6, 0])
        self.play(FadeIn(eq, scale=0.7), run_time=0.5)
        self.at("however long you wait")
        cpos = np.array([5.9, 2.95, 0.0])
        face, hand = clock(cpos, r=0.45)
        self.play(FadeIn(face), FadeIn(hand), run_time=0.3)
        self.play(Rotate(hand, angle=-2 * PI, about_point=cpos, rate_func=linear), run_time=1.5)
        self.finish()


class S12Model(SpokenScene):
    def construct(self):
        R = Ring(D_SH, N_SH)
        R.dlevel.set_value(0.2)
        R.mount(self)
        eq = T("=", 70, TEXT, weight=BOLD).move_to([0, CY, 0])
        self.add(eq)

        def card(x, title, num, col):
            box = RoundedRectangle(corner_radius=0.25, width=5.8, height=3.2, stroke_color=col, stroke_width=3, fill_color=col, fill_opacity=0.1)
            t = T(title, 34, GREY).move_to(box.get_center() + UP * 0.9)
            n = T(num, 46, GOLD).move_to(box.get_center() + DOWN * 0.3)
            return VGroup(box, t, n).move_to([x, 0.7, 0])
        c1 = card(-3.4, "steep loop", "1% → 5.7%", GREEN)
        c2 = card(3.4, "shallow loop", "1% → 0.14%", GREY)
        self.play(FadeOut(R.g_cells), FadeOut(R.g_chips), FadeOut(R.g_yel), FadeOut(R.g_inh), FadeOut(eq), R.mvis.animate.set_value(0),
                  R.capvis.animate.set_value(0), FadeIn(c1, shift=UP * 0.2), FadeIn(c2, shift=UP * 0.2), run_time=1.0)
        self.at("from a model")
        mdl = T("model,", 34, TEXT)
        illu = T("illustrative", 34, GOLD)
        nm = T("not measured", 34, TEXT)
        lab = VGroup(illu, mdl, nm).arrange(RIGHT, buff=0.2).move_to([0, -2.2, 0])
        self.play(FadeIn(mdl, shift=UP * 0.1), run_time=0.5)
        self.at("illustrative")
        self.play(FadeIn(illu, shift=UP * 0.1), run_time=0.5)
        self.at("not measurements")
        self.play(FadeIn(nm, shift=UP * 0.1), run_time=0.5)
        self.finish()


# ---------------------------------------------------------------------------------------------
TIPX, TIPY = 0.0, -3.1
TIP = np.array([TIPX, TIPY, 0])


def pencil():
    body = Polygon([-0.3, 0.75, 0], [-0.3, 4.7, 0], [0.3, 4.7, 0], [0.3, 0.75, 0], stroke_color=TEXT, stroke_width=3, fill_color="#6B7385", fill_opacity=0.9)
    cone = Polygon([0, 0, 0], [-0.3, 0.75, 0], [0.3, 0.75, 0], stroke_color=TEXT, stroke_width=3, fill_color="#D8C3A5", fill_opacity=0.95)
    lead = Polygon([0, 0, 0], [-0.08, 0.2, 0], [0.08, 0.2, 0], stroke_width=0, fill_color="#2A2F3A", fill_opacity=1)
    band = Rectangle(width=0.6, height=0.4, stroke_color=TEXT, stroke_width=3, fill_color=GREY, fill_opacity=0.9).move_to([0, 4.9, 0])
    g = VGroup(body, cone, lead, band)
    g.shift(TIP)
    return g


def ground():
    return VGroup(Line([-6.2, TIPY - 0.02, 0], [6.2, TIPY - 0.02, 0], color=GREY, stroke_width=4))


def pair_icon(cx, cy, winner=None, r=0.6, gap=0.25):
    """Two small cells A and B; the winner (if any) is green."""
    out = VGroup()
    for name, dx in (("A", -(r + gap / 2)), ("B", r + gap / 2)):
        win = winner == name
        c = Circle(radius=r, stroke_color=GREEN if win else GREY, stroke_width=5 if win else 4, fill_color=GREEN if win else GREY,
                   fill_opacity=0.35 if win else 0.08).move_to([cx + dx, cy, 0])
        out.add(c, T(name, 30, GREEN if win else GREY).move_to(c))
    return out


class S13Pencil(SpokenScene):
    def construct(self):
        gr = ground()
        self.add(gr)
        pen = pencil()
        self.play(GrowFromPoint(pen, TIP), run_time=0.3)
        self.at("steep loop")
        dl = Ring._gauge(None, np.array([4.4, -0.2, 0.0]), 1.15, 0.93, 1, sw=8)
        sl = T("steep loop", 44, GOLD).move_to([4.4, 1.5, 0])
        self.play(FadeIn(dl), FadeIn(sl, shift=UP * 0.1), run_time=0.6)
        self.at("even pair")
        pi = pair_icon(-4.4, 0.4, None, r=0.7, gap=0.5)
        eqs = T("=", 44, TEXT).move_to([-4.4, 0.4, 0])
        ep = T("even pair", 36, TEXT).move_to([-4.4, -1.0, 0])
        self.play(FadeIn(pi), FadeIn(ep), FadeIn(eqs), run_time=0.6)
        self.at("pencil")
        arr = Arrow([-2.55, 0.4, 0], [-0.75, 0.4, 0], buff=0, color=GOLD, stroke_width=6, tip_length=0.26)
        self.play(GrowArrow(arr), Indicate(pen, color=GOLD, scale_factor=1.04), run_time=0.3)
        self.at("balanced on its point")
        tdot = Dot(TIP + UP * 0.02, radius=0.1, color=GOLD)
        self.add(tdot)
        self.play(Rotate(pen, angle=0.045, about_point=TIP, rate_func=there_and_back), Indicate(tdot, color=GOLD, scale_factor=3), run_time=0.7)
        self.play(Rotate(pen, angle=-0.045, about_point=TIP, rate_func=there_and_back), run_time=0.7)
        self.finish()


class S14Pencil2(SpokenScene):
    def construct(self):
        gr = ground()
        pen = pencil()
        self.add(gr, pen)
        FALL = 1.3
        head = lambda s: TIP + 5.0 * np.array([-s * np.sin(FALL), np.cos(FALL), 0.0])
        self.at("slightest tip")
        self.play(Rotate(pen, angle=0.07, about_point=TIP), run_time=0.5)
        self.at("grows")
        self.play(Rotate(pen, angle=FALL - 0.07, about_point=TIP, rate_func=rush_into), run_time=0.9)
        self.at("two stable outcomes")
        ghost = pencil()
        ghost.set_opacity(0.55)
        ttl = T("two stable outcomes", 44, GOLD).move_to([0, 2.6, 0])
        self.play(FadeIn(ghost, run_time=0.2), FadeIn(ttl, shift=UP * 0.1, run_time=0.6))
        self.play(Rotate(ghost, angle=-FALL, about_point=TIP, rate_func=rush_into), run_time=0.8)
        self.at("a neural")
        hl = head(1)
        ia = pair_icon(hl[0], hl[1] + 1.0, "A", r=0.6, gap=0.25)
        la = T("A neural", 38, GREEN).move_to([hl[0], hl[1] + 2.1, 0])
        self.play(FadeIn(ia), FadeIn(la, shift=UP * 0.1), run_time=0.5)
        self.at("b neural")
        hr = head(-1)
        ib = pair_icon(hr[0], hr[1] + 1.0, "B", r=0.6, gap=0.25)
        lb = T("B neural", 38, GREEN).move_to([hr[0], hr[1] + 2.1, 0])
        self.play(FadeIn(ib), FadeIn(lb, shift=UP * 0.1), run_time=0.5)
        self.finish()


# ---------------------------------------------------------------------------------------------
def land_curve(par, ulim, y0=-2.4, y1=0.9, xscale=5.0, color=TEXT):
    ug, P = landscape(par, ulim)
    ug = ug[::6]
    P = P[::6]
    pts = [np.array([-u / ulim * xscale, y0 + p * (y1 - y0), 0]) for u, p in zip(ug, P)]       # A neural (u > 0) on the left
    return VMobject(stroke_color=color, stroke_width=6).set_points_as_corners(pts), pts


class S15Bistable(SpokenScene):
    def construct(self):
        curve, pts = land_curve(STEEP, 1.2, y0=-2.0, y1=1.5)
        self.play(Create(curve), run_time=1.5)
        self.at("bistable")
        t = T("bistable", 56, GOLD, font=TITLE_FONT).move_to([-4.5, 3.0, 0])
        self.play(FadeIn(t, shift=UP * 0.1), run_time=0.7)
        self.at("two stable outcomes")
        n = len(pts)
        i_r = int(np.argmin([p[1] for p in pts[: n // 2]]))
        i_l = n // 2 + int(np.argmin([p[1] for p in pts[n // 2:]]))
        dl, dr = Dot(pts[i_l] + UP * 0.2, radius=0.24, color=GREEN), Dot(pts[i_r] + UP * 0.2, radius=0.24, color=GREEN)
        ll = VGroup(T("A neural", 34, GREEN), T("stable", 34, TEXT)).arrange(DOWN, buff=0.1).move_to(pts[i_l] + DOWN * 0.95 + RIGHT * 0.2)
        lr = VGroup(T("B neural", 34, GREEN), T("stable", 34, TEXT)).arrange(DOWN, buff=0.1).move_to(pts[i_r] + DOWN * 0.95 + LEFT * 0.2)
        self.play(FadeIn(dl, scale=0.5), FadeIn(dr, scale=0.5), FadeIn(ll), FadeIn(lr), run_time=0.9)
        self.at("the even state")
        top = pts[n // 2]
        dt = Dot(top + UP * 0.2, radius=0.24, color=TEXT, fill_opacity=0.15, stroke_width=4)
        lt = T("even state", 34, TEXT).move_to(top + UP * 0.85)
        self.play(FadeIn(dt, scale=0.5), FadeIn(lt, shift=UP * 0.1), run_time=0.7)
        self.at("unstable")
        a1 = Arrow(top + UP * 0.1 + LEFT * 0.35, top + LEFT * 1.6 + DOWN * 0.45, buff=0.05, color=RED, stroke_width=7, tip_length=0.26)
        a2 = Arrow(top + UP * 0.1 + RIGHT * 0.35, top + RIGHT * 1.6 + DOWN * 0.45, buff=0.05, color=RED, stroke_width=7, tip_length=0.26)
        un = T("unstable", 44, RED, weight=BOLD).move_to(top + UP * 1.6)
        self.play(FadeIn(un, shift=UP * 0.1), GrowArrow(a1), GrowArrow(a2), run_time=0.7)
        self.finish()


class S16Marble(SpokenScene):
    def construct(self):
        ulim = 0.5
        curve, pts = land_curve(SHALLOW, ulim, y0=-2.4, y1=1.6)
        hd = T("shallow loop", 56, GOLD, font=TITLE_FONT).move_to([0, 3.2, 0])
        self.play(Create(curve), FadeIn(hd, shift=UP * 0.1), run_time=1.0)
        self.at("marble in a bowl")
        xs = np.array([p[0] for p in pts])[::-1]
        ys = np.array([p[1] for p in pts])[::-1]
        Y = lambda x: float(np.interp(x, xs, ys))
        r = 0.32
        marble = Dot(radius=r, color=GREEN).move_to([0, Y(0) + r + 0.03, 0])
        lab = T("the pair", 30, GREEN).move_to([0, Y(0) - 0.6, 0])
        self.play(FadeIn(marble, shift=DOWN * 0.8), FadeIn(lab), run_time=0.6)
        self.at("push it")
        sim = pair_sim(SHALLOW, 0.40, D_SH, 6.0, every=3)
        us = sim[:, 1] - sim[:, 2]
        sc = 5.0 / ulim
        xstart = -us[0] * sc
        push = Arrow([-1.9, Y(0) + 0.6, 0], [-0.6, Y(0) + 0.6, 0], buff=0, color=GOLD, stroke_width=6, tip_length=0.25)
        self.play(GrowArrow(push), FadeOut(lab), marble.animate.move_to([xstart, Y(xstart) + r + 0.03, 0]), run_time=0.7)
        self.play(FadeOut(push), run_time=0.2)
        self.at("rolls back")
        s = ValueTracker(0)

        def place(m):
            i = int(round(s.get_value() * (len(us) - 1)))
            x = -us[i] * sc
            m.move_to([x, Y(x) + r + 0.03, 0])
        marble.add_updater(place)
        self.play(s.animate.set_value(1), run_time=1.5, rate_func=lambda t: 1 - (1 - t) ** 2)
        marble.remove_updater(place)
        self.finish()


# ---------------------------------------------------------------------------------------------
class S17Size(SpokenScene):
    def construct(self):
        pl = Plot(-4.3, 6.2, -2.5, 2.3, 22.0, 1.0)
        q = T("Does the size of the first difference matter much?", 30, TEXT).move_to([0, 3.4, 0])
        ax = pl.axes()
        ticks = VGroup()
        for tt in (0, 5, 10, 15, 20):
            ticks.add(T(str(tt), 26, GREY).move_to(pl.P(tt, 0) + DOWN * 0.36))
        yt = VGroup(*[T(s, 26, GREY).move_to(pl.P(0, v) + LEFT * 0.5) for s, v in (("0", 0.0), ("0.5", 0.5), ("1", 1.0))])
        xl = T("time (arbitrary units)", 26, GREY).move_to([pl.P(11, 0)[0], -3.3, 0])
        yl = T("difference between the cells", 24, GREY).rotate(PI / 2).move_to([-5.65, -0.1, 0])
        self.play(FadeIn(q), FadeIn(ax), FadeIn(ticks), FadeIn(yt), FadeIn(xl), FadeIn(yl), run_time=0.9)
        self.at("first difference")
        d1 = SIM_STEEP[:, 1] - SIM_STEEP[:, 2]
        d2 = SIM_STEEP_01[:, 1] - SIM_STEEP_01[:, 2]
        c1 = pl.curve(SIM_STEEP[:, 0], d1, YELLOW)
        leg1 = VGroup(Line([-4.0, 1.85, 0], [-3.3, 1.85, 0], color=YELLOW, stroke_width=5), T("1% start", 26, YELLOW).move_to([-2.35, 1.85, 0]))
        self.play(Create(c1, rate_func=linear), FadeIn(leg1), run_time=2.0)
        self.at("in this example")
        we = T("worked example", 34, TEXT).move_to([-3.4, 3.4, 0])
        self.play(FadeOut(q), FadeIn(we), run_time=0.5)
        self.at("a start ten")
        c2 = pl.curve(SIM_STEEP_01[:, 0], d2, YELLOW, dashed=True)
        leg2 = T("0.1% start", 26, YELLOW).move_to([-2.25, 1.3, 0])
        dsh = DashedLine([-4.0, 1.3, 0], [-3.3, 1.3, 0], color=YELLOW, stroke_width=5, dashed_ratio=0.5)
        self.play(Create(c2, rate_func=linear), FadeIn(leg2), FadeIn(dsh), run_time=1.6)
        self.at("delays the split")
        x13, x17 = pl.P(13.0, 0)[0], pl.P(17.2, 0)[0]
        v1 = DashedLine([x13, pl.b, 0], [x13, 2.95, 0], color="#F2C14E", stroke_width=4)
        v2 = DashedLine([x17, pl.b, 0], [x17, 2.95, 0], color="#F2C14E", stroke_width=4)
        GB = "#F2C14E"
        t13 = T("about 13", 32, GB, weight=BOLD).move_to([x13 - 1.15, 2.7, 0])
        t17 = T("about 17", 32, GB, weight=BOLD).move_to([x17 + 1.15, 2.7, 0])
        self.play(Create(v1), Create(v2), FadeIn(t13), FadeIn(t17), run_time=0.7)
        self.at("by about a third")
        br = DoubleArrow([x13, 2.7, 0], [x17, 2.7, 0], color=GB, stroke_width=5, buff=0, tip_length=0.18)
        bl = T("about a third later", 32, GB, weight=BOLD).move_to([(x13 + x17) / 2 + 0.6, 3.3, 0])
        self.play(GrowFromCenter(br), FadeIn(bl, shift=UP * 0.1), run_time=0.6)
        self.finish()


class S18Noise(SpokenScene):
    def construct(self):
        L = Plot(-5.6, -1.2, -2.5, 2.2, 30.0, 1.0)
        Rr = Plot(1.9, 6.3, -2.5, 2.2, 30.0, 1.0)
        mid = lambda p: DashedLine(p.P(0, 0.5), p.P(30, 0.5), color=GREY, stroke_width=2, dashed_ratio=0.5).set_stroke(opacity=0.7)

        def frame(p):
            g = VGroup(p.axes(), mid(p))
            for s, v in (("0%", 0.0), ("50%", 0.5), ("100%", 1.0)):
                g.add(T(s, 24, GREY).move_to(p.P(0, v) + LEFT * 0.55))
            g.add(T("0", 24, GREY).move_to(p.P(0, 0) + DOWN * 0.35), T("30", 24, GREY).move_to(p.P(30, 0) + DOWN * 0.35),
                  T("time", 24, GREY).move_to(p.P(15, 0) + DOWN * 0.35))
            return g
        axl, axr = frame(L), frame(Rr)
        axr.set_opacity(0.3)
        cap = T("share of the Delta: cell A solid, cell B dashed", 24, GREY).move_to([0, 3.45, 0])
        self.play(FadeIn(axl), FadeIn(axr), FadeIn(cap), run_time=0.3)
        s = noisy_share(STEEP, 0.08, 30, seed=1)
        cA = L.curve(s[:, 0], s[:, 1], YELLOW)
        cB = L.curve(s[:, 0], 1 - s[:, 1], YELLOW, dashed=True)
        tl = T("steep loop", 34, GOLD).move_to([-3.4, 2.85, 0])
        self.play(Create(cA, rate_func=linear), Create(cB, rate_func=linear), Succession(Wait(run_time=0.2), FadeIn(tl, shift=UP * 0.1, run_time=0.4)), run_time=3.3)
        ea = T("A", 26, YELLOW).move_to(L.P(30, s[-1, 1]) + RIGHT * 0.3)
        eb = T("B", 26, YELLOW).move_to(L.P(30, 1 - s[-1, 1]) + RIGHT * 0.3)
        self.play(FadeIn(ea), FadeIn(eb), run_time=0.2)
        self.at("near the threshold")
        tr = T("just past threshold", 34, GOLD).move_to([4.1, 2.85, 0])
        self.play(axr.animate.set_opacity(1), FadeIn(tr, shift=UP * 0.1), run_time=0.4)
        s2 = noisy_share(NEAR, 0.08, 30, seed=6)
        rA = Rr.curve(s2[:, 0], s2[:, 1], YELLOW)
        rB = Rr.curve(s2[:, 0], 1 - s2[:, 1], YELLOW, dashed=True)
        wl = T("still waiting:\nthe split comes much later", 26, GOLD, line_spacing=0.8).move_to(Rr.P(15, 0.5) + UP * 1.55)
        self.play(Create(rA, rate_func=linear), Create(rB, rate_func=linear), Succession(Wait(run_time=1.2), FadeIn(wl, shift=UP * 0.1, run_time=0.5)), run_time=2.3)
        self.finish()


# ---------------------------------------------------------------------------------------------
class S19Sheet(SpokenScene):
    def construct(self):
        hexes = build_sheet()
        rings = {}
        for c in CELLS:
            rings.setdefault(max(abs(c[0]), abs(c[1]), abs(c[0] + c[1])), []).append(hexes[c])
        centre = hexes[(0, 0)]
        self.at("put the cell")
        self.play(FadeIn(centre, scale=0.6), run_time=0.5)
        self.at("a sheet")
        self.play(LaggedStart(*[AnimationGroup(*[FadeIn(h, scale=0.7) for h in rings[k]]) for k in (1, 2, 3)], lag_ratio=0.5), run_time=1.3)
        self.at("hears the average")
        nbs = [hexes[(dq, dr)] for dq, dr in [(1, 0), (1, -1), (0, -1), (-1, 0), (-1, 1), (0, 1)]]
        nb1 = ValueTracker(0.4)
        vis = ValueTracker(0)
        bx = [2.1 + 0.55 * i for i in range(6)]

        def panel():
            v = vis.get_value()
            g = VGroup()
            for i, x in enumerate(bx):
                val = nb1.get_value() if i == 0 else 0.4
                g.add(Rectangle(width=0.34, height=1.5, stroke_color=GREY, stroke_width=2, fill_opacity=0).move_to([x, 1.15, 0]).set_stroke(opacity=0.6 * v))
                h = val * 1.5
                g.add(Rectangle(width=0.34, height=h, stroke_width=0, fill_color=YELLOW, fill_opacity=0.92 * v).move_to([x, 0.4 + h / 2, 0]))
            avg = (nb1.get_value() + 5 * 0.4) / 6
            g.add(Rectangle(width=0.7, height=1.5, stroke_color=GREY, stroke_width=2, fill_opacity=0).move_to([3.55, -1.9, 0]).set_stroke(opacity=0.6 * v))
            h = avg * 1.5
            g.add(Rectangle(width=0.7, height=h, stroke_width=0, fill_color=YELLOW, fill_opacity=0.92 * v).move_to([3.55, -2.65 + h / 2, 0]))
            return g
        pan = always_redraw(panel)
        self.add(pan)
        lab_n = T("six neighbours' Delta", 24, YELLOW).move_to([3.7, 2.3, 0])
        arrd = Arrow([3.55, 0.25, 0], [3.55, -1.0, 0], buff=0, color=GREY, stroke_width=5, tip_length=0.22)
        lab_a = T("average", 24, TEXT).move_to([5.4, -2.0, 0])
        self.play(*[h.animate.set_fill(YELLOW, 0.35).set_stroke(YELLOW, 4, opacity=1) for h in nbs],
                  centre.animate.set_stroke(TEXT, 5).set_fill(TEXT, 0.15), vis.animate.set_value(1), FadeIn(lab_n), run_time=1.0)
        self.play(GrowArrow(arrd), FadeIn(lab_a), run_time=0.6)
        self.at("one neighbor's change")
        self.play(nb1.animate.set_value(0.95), nbs[0].animate.set_fill(YELLOW, 0.85), Indicate(nbs[0], color=TEXT, scale_factor=1.12), run_time=0.9)
        self.at("diluted")
        dil = T("diluted", 30, GOLD).move_to([5.4, -1.35, 0])
        self.play(FadeIn(dil, shift=UP * 0.1), run_time=0.5)
        self.finish()


class S20Sheet2(SpokenScene):
    def construct(self):
        AX_Y = -2.0
        X = lambda v: -6.0 + 2.0 * v
        axis = Line([X(0), AX_Y, 0], [X(6), AX_Y, 0], color=GREY, stroke_width=4)
        tick = VGroup(*[Line([X(i), AX_Y, 0], [X(i), AX_Y - 0.12, 0], color=GREY, stroke_width=3) for i in range(7)])
        nums = VGroup(*[T(str(i), 38 if i in (1, 4) else 26, GOLD if i in (1, 4) else GREY, weight=BOLD if i in (1, 4) else NORMAL).move_to([X(i), AX_Y - 0.5, 0]) for i in range(7)])
        al = T("round-trip factor", 30, GOLD).move_to([0, -3.35, 0])
        self.play(Create(axis), FadeIn(tick), FadeIn(nums), FadeIn(al), run_time=0.8)
        self.at("a pair splits")
        ca = Circle(radius=0.3, stroke_color=GREY, stroke_width=3, fill_color=GREY, fill_opacity=0.1).move_to([-5.45, 1.6, 0])
        cb = ca.copy().move_to([-4.75, 1.6, 0])
        pt = T("pair splits", 34, TEXT).move_to([1.0, 1.6, 0])
        self.play(FadeIn(ca), FadeIn(cb), FadeIn(pt, shift=RIGHT * 0.2), run_time=0.7)
        self.at("round trip factor")
        self.play(Indicate(al, color=GOLD, scale_factor=1.12), run_time=0.7)
        self.at("above 1")
        drop1 = DashedLine([X(1), 1.2, 0], [X(1), AX_Y, 0], color=GOLD, stroke_width=4)
        bar1 = Rectangle(width=0.01, height=0.8, stroke_width=0, fill_color=GREEN, fill_opacity=0.3).move_to([X(1) + 0.005, 1.6, 0])
        self.play(Create(drop1), run_time=0.4)
        full1 = Rectangle(width=X(6) - X(1), height=0.8, stroke_width=0, fill_color=GREEN, fill_opacity=0.3).move_to([(X(1) + X(6)) / 2, 1.6, 0])
        self.play(Transform(bar1, full1), run_time=0.9)
        self.at("ideal hexagonal sheet")
        hexes = VGroup()
        for q, r in [(0, 0), (1, 0), (1, -1), (0, -1), (-1, 0), (-1, 1), (0, 1)]:
            hexes.add(make_hex(q, r, 0.17, 0.155, 0, 0))
        hexes.move_to([-5.45, -0.1, 0])
        ht = T("ideal hexagonal sheet splits", 26, TEXT).move_to([0, -0.1, 0])
        ht.align_to(np.array([X(4) - 0.3, 0, 0]), RIGHT)
        self.play(FadeIn(hexes), FadeIn(ht, shift=RIGHT * 0.2), run_time=0.8)
        self.at("above 4")
        drop4 = DashedLine([X(4), -0.1 - 0.4, 0], [X(4), AX_Y, 0], color=GOLD, stroke_width=4)
        bar4 = Rectangle(width=0.01, height=0.8, stroke_width=0, fill_color=GREEN, fill_opacity=0.3).move_to([X(4) + 0.005, -0.1, 0])
        full4 = Rectangle(width=X(6) - X(4), height=0.8, stroke_width=0, fill_color=GREEN, fill_opacity=0.3).move_to([(X(4) + X(6)) / 2, -0.1, 0])
        self.play(Create(drop4), run_time=0.3)
        self.play(Transform(bar4, full4), run_time=0.8)
        self.finish()


def live_cells(hexes, fn):
    """Give each hex an updater (so the renderer treats it as moving) that calls fn(hex, k)."""
    for k, c in enumerate(CELLS):
        hexes[c].add_updater(lambda m, k=k: fn(m, k))


def stop_live(hexes):
    for c in CELLS:
        hexes[c].clear_updaters()


class S21Sheet3(SpokenScene):
    def construct(self):
        hexes = build_sheet()
        i0, i1 = int(27 / 0.5), int(46 / 0.5)
        s = ValueTracker(0)
        idx = lambda: int(round(i0 + s.get_value() * (i1 - i0)))
        for k, c in enumerate(CELLS):
            set_cell(hexes[c], SHEET[i0][k])
            self.add(hexes[c])
        live_cells(hexes, lambda m, k: set_cell(m, SHEET[idx()][k]))
        self.at("splits")
        self.play(s.animate.set_value(1), run_time=2.0, rate_func=linear)
        stop_live(hexes)
        self.at("one cell in three")
        big = T("about 1 in 3", 58, GOLD, font=TITLE_FONT).move_to([4.1, 1.4, 0])
        cnt = T(f"{int(SHEET_WIN.sum())} of {len(CELLS)} cells win", 30, TEXT).move_to([4.1, 0.4, 0])
        self.play(FadeIn(big, shift=UP * 0.15), run_time=0.6)
        self.play(FadeIn(cnt), run_time=0.4)
        self.at("typically wins")
        note = T("one example:\nedges and settings\nchange the count", 26, GREY, line_spacing=0.8).move_to([4.1, -1.4, 0])
        self.play(FadeIn(note), run_time=0.5)
        self.finish()


PATCH_DIRS = [(0, 0), (1, 0), (1, -1), (0, -1), (-1, 0), (-1, 1), (0, 1)]


def pick_patch():
    """A seven-cell cluster in the interior of the example sheet that does not hold exactly one winner."""
    idx = {c: i for i, c in enumerate(CELLS)}
    best = None
    for c in CELLS:
        cells = [(c[0] + dq, c[1] + dr) for dq, dr in PATCH_DIRS]
        if not all(x in idx for x in cells):
            continue
        n = sum(int(SHEET_WIN[idx[x]]) for x in cells)
        if n != 1 and (best is None or abs(c[0]) + abs(c[1]) < abs(best[0][0]) + abs(best[0][1])):
            best = (c, cells, n)
    return best


def pick_two():
    """Two disjoint seven-cell clusters in the example sheet: one with exactly one winner, one with several."""
    idx = {c: i for i, c in enumerate(CELLS)}
    pats = []
    for c in CELLS:
        cells = [(c[0] + dq, c[1] + dr) for dq, dr in PATCH_DIRS]
        if all(x in idx for x in cells):
            pats.append((c, cells, sum(int(SHEET_WIN[idx[x]]) for x in cells)))
    best = None
    for a in pats:
        for b in pats:
            if a[2] == 1 and b[2] >= 2 and not set(a[1]) & set(b[1]):
                da = hpos(a[0][0], a[0][1], RL, SX, SY)
                db = hpos(b[0][0], b[0][1], RL, SX, SY)
                dist = float(np.linalg.norm(da - db))
                if best is None or dist > best[0]:
                    best = (dist, a, b)
    return best[1], best[2]


class S22Cluster(SpokenScene):
    def construct(self):
        hexes = build_sheet()
        for k, c in enumerate(CELLS):
            set_cell(hexes[c], SHEET[-1][k])
            self.add(hexes[c])
        pa, pb = pick_two()
        patchA = VGroup(*[hexes[c] for c in pa[1]])
        big = T("about 1 in 3", 58, GOLD, font=TITLE_FONT).move_to([4.1, 1.4, 0])
        cnt = T(f"{int(SHEET_WIN.sum())} of {len(CELLS)} cells win", 30, TEXT).move_to([4.1, 0.4, 0])
        self.add(big, cnt)
        self.at("spaced pattern")
        self.play(FadeOut(big), FadeOut(cnt), run_time=0.5)
        self.at("not a guaranteed winner")
        ringA = Circle(radius=1.5, stroke_color=GOLD, stroke_width=6).move_to(hpos(pa[0][0], pa[0][1], RL, SX, SY))
        ringB = Circle(radius=1.5, stroke_color=TEXT, stroke_width=6).move_to(hpos(pb[0][0], pb[0][1], RL, SX, SY))
        wordB = {2: "two", 3: "three"}.get(pb[2], str(pb[2]))
        keyA = VGroup(Circle(radius=0.24, stroke_color=GOLD, stroke_width=6), T("one winner", 32, GOLD)).arrange(RIGHT, buff=0.25)
        keyB = VGroup(Circle(radius=0.24, stroke_color=TEXT, stroke_width=6), T(f"{wordB} winners", 32, TEXT)).arrange(RIGHT, buff=0.25)
        keys = VGroup(keyA, keyB).arrange(DOWN, buff=0.35, aligned_edge=LEFT).move_to([4.5, 2.0, 0])
        stmt = T("a cluster can hold\none or several\nwinners", 38, GOLD, line_spacing=0.8).move_to([4.5, -0.9, 0])
        self.play(Create(ringA), Create(ringB), FadeIn(keys), run_time=0.9)
        self.play(FadeIn(stmt, shift=UP * 0.1), run_time=0.6)
        until(self, 3.4)
        others = VGroup(*[hexes[c] for c in CELLS if c not in pa[1]])
        self.play(FadeOut(others), FadeOut(ringA), FadeOut(ringB), FadeOut(keys), FadeOut(stmt),
                  patchA.animate.move_to([-0.7, 0.1, 0]).scale(1.9), run_time=0.8)
        self.play(*[h.animate.set_fill(GREY, 0.08).set_stroke(GREY, 3, opacity=1) for h in patchA], run_time=0.3)
        self.at("add help")
        helpl = T("help, not requirements", 38, GOLD).move_to([0, -3.3, 0])
        self.play(FadeIn(helpl, shift=UP * 0.1), run_time=0.5)
        self.at("a head start")
        hs_cell = patchA[2]
        c1 = chip("head start", GREEN, size=34).move_to([4.5, 2.75, 0])
        l1 = Line(c1.get_left() + LEFT * 0.05, hs_cell.get_center() + np.array([0.55, 0.5, 0]), color=GREEN, stroke_width=4)
        self.play(FadeIn(c1, shift=LEFT * 0.2), Create(l1), hs_cell.animate.set_fill(GREEN, 0.6).set_stroke(GREEN, 5), run_time=0.7)
        self.at("a longer reach")
        c2 = chip("longer reach", BLUE, size=34).move_to([4.6, 0.95, 0])
        l2 = DashedLine(hs_cell.get_right() + RIGHT * 0.05, c2.get_left() + LEFT * 0.05, color=BLUE, stroke_width=6).add_tip(tip_length=0.28)
        self.play(FadeIn(c2, shift=LEFT * 0.2), Create(l2), run_time=0.7)
        self.at("or timing")
        c3 = chip("timing", GOLD, size=34).move_to([-4.6, -0.55, 0])
        cpos = np.array([-4.6, 0.5, 0.0])
        face, hand = clock(cpos, r=0.55)
        self.play(FadeIn(c3, shift=RIGHT * 0.2), FadeIn(face), FadeIn(hand), run_time=0.5)
        self.play(Rotate(hand, angle=-PI * 1.5, about_point=cpos, rate_func=linear), run_time=0.9)
        self.wait(0.8)
        self.finish()


class S23Notum(SpokenScene):
    def construct(self):
        oval = Ellipse(width=12.3, height=5.7, stroke_color=GREY, stroke_width=4, fill_color=GREY, fill_opacity=0.06).move_to([0, 0.05, 0])
        lab = T("notum", 36, GREY).move_to([-3.4, 3.3, 0])
        pcells = [(0, 0), (1, 0), (1, -1), (0, -1), (-1, 0), (-1, 1), (0, 1)]
        centres = [-4.2, 0.0, 4.2]
        clusters = [VGroup(*[make_hex(q, r, 0.62, 0.58, cx, 0.1) for q, r in pcells]) for cx in centres]
        self.add(oval)
        self.play(FadeIn(lab, shift=DOWN * 0.1), LaggedStart(*[FadeIn(c, scale=0.8) for c in clusters], lag_ratio=0.25), run_time=0.8)
        self.at("a head start")
        hs = chip("head start", GREEN, size=32).move_to([4.7, 3.05, 0])
        self.play(FadeIn(hs, shift=DOWN * 0.1), run_time=0.5)
        self.at("levels are already uneven")
        pat = [0.38, 0.22, 0.95, 0.15, 0.3, 0.52, 0.2]       # centre + six neighbours, the same in every cluster
        # legend: brighter green = more proneural factor
        grad = VGroup(*[Rectangle(width=0.2, height=0.34, stroke_width=0, fill_color=GREEN, fill_opacity=0.05 + 0.75 * (i / 9)) for i in range(10)]).arrange(RIGHT, buff=0)
        lg = VGroup(T("proneural level:", 30, GREEN), T("low", 26, GREY), grad, T("high", 26, GREEN)).arrange(RIGHT, buff=0.25).move_to([0, -3.3, 0])
        anims = []
        for c in clusters:
            for h, v in zip(c, pat):
                anims.append(h.animate.set_fill(GREEN, 0.05 + 0.75 * v).set_stroke(GREEN, 2.5, opacity=0.6))
        self.play(*anims, FadeIn(lg), run_time=1.3)
        self.at("precursors arise")
        anims = []
        for c in clusters:
            for k, h in enumerate(c):
                if k == 2:
                    anims.append(h.animate.set_fill(GREEN, 0.95).set_stroke(TEXT, 6, opacity=1))
                else:
                    anims.append(h.animate.set_fill(GREEN, 0.04).set_stroke(GREY, 2.5, opacity=0.5))
        pr = T("precursor", 28, TEXT).move_to(clusters[1][2].get_center() + UP * 1.05)
        self.play(*anims, FadeIn(pr, shift=DOWN * 0.1), run_time=1.0)
        self.at("reproducible spots")
        rs = T("the same spots, again and again", 32, GOLD).move_to([0, -3.3, 0])
        self.play(ReplacementTransform(lg, rs), run_time=0.6)
        self.finish()


# ---------------------------------------------------------------------------------------------
GCOLS, GROWS = 9, 7
GDX, GDY, GR = 0.95, 0.84, 0.39
GX0, GY0 = -6.1, 2.75


def grid_nbrs():
    out = []
    for r in range(GROWS):
        for c in range(GCOLS):
            odd = r % 2 == 1
            cand = [(r, c - 1), (r, c + 1), (r - 1, c if odd else c - 1), (r - 1, c + 1 if odd else c),
                    (r + 1, c if odd else c - 1), (r + 1, c + 1 if odd else c)]
            out.append([rr * GCOLS + cc for rr, cc in cand if 0 <= rr < GROWS and 0 <= cc < GCOLS])
    return out


GNB = grid_nbrs()


def grid_sim(h, seed, steps):
    rng = np.random.default_rng(seed)
    d = 0.5 + (rng.random(GCOLS * GROWS) - 0.5) * 0.04
    out = [d.copy()]
    for _ in range(steps):
        notch = np.array([d[j].mean() for j in GNB])
        d = d + (1 / (1 + (notch / 0.5) ** h) - d) * 0.5
        out.append(d.copy())
    return np.array(out)


GRID = grid_sim(4.5, 0, 100)
GEND = 96                      # by step 96 every cell has settled; the pattern is final
GPICK = int((GRID[GEND] > 0.62).sum())
DARK = ManimColor("#2A3040")
BRIGHT = ManimColor(YELLOW)


def paint_cell(cl, v):
    v = float(min(1, max(0, v)))
    cl.set_fill(interpolate_color(DARK, BRIGHT, v), 1.0)
    win = v > 0.62
    cl.set_stroke(GREEN if win else GREY, 5 if win else 1.5, opacity=1 if win else 0.5)


class S24Grid(SpokenScene):
    def construct(self):
        cells = []
        for r in range(GROWS):
            for c in range(GCOLS):
                x = GX0 + c * GDX + (GDX / 2 if r % 2 else 0)
                y = GY0 - r * GDY
                cells.append(Circle(radius=GR, stroke_color=GREY, stroke_width=2, fill_color=GREY, fill_opacity=1.0).move_to([x, y, 0]))
        for k, cl in enumerate(cells):
            paint_cell(cl, GRID[0][k])
        self.at("the grid")
        self.play(LaggedStart(*[FadeIn(c, scale=0.6) for c in cells], lag_ratio=0.02), run_time=1.0)
        self.at("feedback scale")
        PX = 4.75
        hv = ValueTracker(1.0)
        tx0, tx1, ty = PX - 1.7, PX + 1.7, 2.0
        title = T("feedback strength", 30, TEXT).move_to([PX, 2.9, 0])
        track = Line([tx0, ty, 0], [tx1, ty, 0], color=GREY, stroke_width=6)
        kx = lambda: tx0 + (tx1 - tx0) * (hv.get_value() - 0.5) / 7.5
        knob = always_redraw(lambda: Dot([kx(), ty, 0], radius=0.2, color=GOLD))
        val = always_redraw(lambda: M(f"{hv.get_value():.1f}", 44, GOLD).move_to([PX, 1.3, 0]))
        self.play(FadeIn(title), Create(track), FadeIn(knob), FadeIn(val), run_time=0.9)
        self.at("not the model's")
        own = T("the grid's own scale,\nnot the model's", 24, GREY, line_spacing=0.8).move_to([PX, -2.35, 0])
        self.play(FadeIn(own), run_time=0.6)
        self.at("turn the strength")
        self.play(hv.animate.set_value(4.5), run_time=1.2)
        btn = chip("Step time ▸", TEAL, size=28, pad=0.2).move_to([PX, 0.4, 0])
        steps = ValueTracker(0)
        timel = always_redraw(lambda: T(f"time: {int(round(steps.get_value()))} steps", 26, GREY).move_to([PX, -0.3, 0]))
        self.add(timel)
        self.play(FadeIn(btn, shift=UP * 0.1), run_time=0.3)
        self.at("step time forward")
        for k, cl in enumerate(cells):
            cl.add_updater(lambda m, k=k: paint_cell(m, GRID[int(round(steps.get_value()))][k]))
        # legend (the lesson grid's own key)
        MIDC = interpolate_color(DARK, BRIGHT, 0.5)
        lg1 = VGroup(Circle(radius=0.2, stroke_color=GREY, stroke_width=2, fill_color=DARK, fill_opacity=1), T("low Delta: held back", 26, TEXT)).arrange(RIGHT, buff=0.2)
        lg2 = VGroup(Circle(radius=0.2, stroke_color=GREY, stroke_width=2, fill_color=MIDC, fill_opacity=1), T("in between", 26, TEXT)).arrange(RIGHT, buff=0.2)
        lg3 = VGroup(Circle(radius=0.2, stroke_color=GREEN, stroke_width=5, fill_color=BRIGHT, fill_opacity=1), T("N = high Delta, picked", 26, TEXT)).arrange(RIGHT, buff=0.2)
        lg = VGroup(lg1, lg2, lg3).arrange(RIGHT, buff=0.55).move_to([0, -3.4, 0])
        self.play(Indicate(btn, color=TEXT, scale_factor=1.1, run_time=0.8), steps.animate(run_time=2.3, rate_func=linear).set_value(GEND),
                  Succession(Wait(run_time=1.3), FadeIn(lg, run_time=0.6)))
        for cl in cells:
            cl.clear_updaters()
        Ns = VGroup(*[T("N", 24, DARK, weight=BOLD).move_to(cells[k].get_center()) for k in range(len(cells)) if GRID[GEND][k] > 0.62])
        res = VGroup(T(f"{GPICK} of {len(cells)} cells picked", 28, TEXT), T("about a third", 36, GOLD)).arrange(DOWN, buff=0.15).move_to([PX, -1.2, 0])
        self.play(FadeIn(Ns), FadeIn(res, shift=UP * 0.1), run_time=0.5)
        self.finish()


# ---------------------------------------------------------------------------------------------
class S25Takeaway(SpokenScene):
    def construct(self):
        l1 = T("Between two equal cells,", 42, TEXT)
        s1 = T("the tie breaks only on a", 42, TEXT)
        s2 = T("steep loop.", 42, GOLD, weight=BOLD)
        l2 = VGroup(s1, s2).arrange(RIGHT, buff=0.22)
        l1.move_to([0, 3.25, 0])                 # both lines centred over the picture
        l2.move_to([0, 2.55, 0])
        head = VGroup(l1, l2)
        h_center = head.get_center()
        head.scale(1.3).move_to([0, 0.6, 0])      # the headline fills the middle until the picture arrives
        m1 = T("A small difference", 34, TEXT)
        m2 = T("must come back", 34, TEXT)
        m3 = T("larger than it left.", 34, TEXT)
        bottom = VGroup(m1, m2, m3).arrange(RIGHT, buff=0.32, aligned_edge=UP).move_to([0, -3.45, 0])
        base = -2.3
        BW, TARGET = 2.2, 3.8
        XL, XR = -3.2, 3.2
        self.at("between two equal cells")
        self.play(FadeIn(l1, shift=UP * 0.1), run_time=0.6)
        self.at("the tie breaks")
        self.play(FadeIn(s1, shift=UP * 0.1), run_time=0.7)
        self.at("steep loop")
        self.play(FadeIn(s2, scale=1.2), run_time=0.5)
        self.at("a small difference")
        b1 = Rectangle(width=BW, height=0.9, stroke_width=0, fill_color=YELLOW, fill_opacity=0.95).move_to([XL, base + 0.45, 0])
        t1 = T("leaves", 32, GREY).move_to([XL, base - 0.4, 0])
        self.play(head.animate.scale(1 / 1.3).move_to(h_center), FadeIn(b1, shift=UP * 0.1), FadeIn(t1), FadeIn(m1, shift=UP * 0.1), run_time=0.6)
        self.at("must come back")
        ghost = DashedVMobject(Rectangle(width=BW, height=TARGET, stroke_color=GOLD, stroke_width=4, fill_opacity=0).move_to([XR, base + TARGET / 2, 0]),
                               num_dashes=50, dashed_ratio=0.55)
        arc = ArcBetweenPoints([XL + 1.3, base + 0.9, 0], [XR - 1.3, base + TARGET - 0.15, 0], angle=-0.9, color=GOLD, stroke_width=7).add_tip(tip_length=0.3)
        self.play(FadeIn(ghost, run_time=0.4), Create(arc, run_time=0.9), FadeIn(m2, shift=LEFT * 0.1, run_time=0.5))
        self.at("larger than it left")
        b2 = Rectangle(width=BW, height=0.9, stroke_width=0, fill_color=YELLOW, fill_opacity=0.95).move_to([XR, base + 0.45, 0])
        t2 = T("comes back", 32, GREY).move_to([XR, base - 0.4, 0])
        self.play(FadeIn(b2), FadeIn(t2), FadeIn(m3, shift=UP * 0.1), run_time=0.3)
        self.play(b2.animate(run_time=0.9).stretch_to_fit_height(TARGET, about_edge=DOWN))
        self.finish()


class S26End(EndCard):
    LINE = "Between two equal cells, the tie breaks only on a steep loop."
