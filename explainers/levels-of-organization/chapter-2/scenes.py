"""One Job, Five Levels  (Biochemistrypedia Life Science film, levels-of-organization, chapter 2)

Same look and colour map as chapter 1 (dark ground, flat cartoon).
  CYAN = oxygen   RED = red blood cell   PALE BLUE = water   (as in chapter 1)
  level colours:  cell PURPLE, tissue BLUE (royal), organ GREEN, organ system ORANGE, organism GOLD
  LEVEL STRIP on the left: five boxes bottom to top, filled as each level is named.
"""
import math
import random
import numpy as np
from bp_style import *  # noqa: F401,F403

AMBER = "#F5A623"
CYAN = "#5CE1FF"
WATER = "#9CC9FF"
BROWN = "#C98B52"
JOB = [YELLOW, AMBER, CYAN, BROWN, RED, GREEN]
PURPLE = "#A57BFF"
TBLUE = "#4F7CFF"
ORANGE = "#FF9A3C"
VESSEL = "#E58A9A"
RIM = "#FFB8AE"
LEVELS = [("cell", PURPLE), ("tissue", TBLUE), ("organ", GREEN), ("organ\nsystem", ORANGE), ("organism", GOLD)]
STAGE_X = 1.5          # centre of the stage (chapter 1's cluster sat here)

CLK = {"t": 0.0}


class ClockMob(Mobject):
    def __init__(self):
        super().__init__()
        CLK["t"] = 0.0
        self.add_updater(lambda m, dt: CLK.__setitem__("t", CLK["t"] + dt))


def pulse(t=None, per=2.0):
    """A beat: contract for 60% of the period, rest for 40%."""
    t = CLK["t"] if t is None else t
    ph = (t % per) / per
    return math.sin(math.pi * ph / 0.6) ** 2 if ph < 0.6 else 0.0


def smooth(x):
    x = min(1.0, max(0.0, x))
    return x * x * (3 - 2 * x)


def tw(m, rt, rf=smooth, **kw):
    """Tween entries of m.s (a state dict) over rt seconds."""
    st = {}

    def f(mm, al):
        if not st:
            st.update({k: mm.s[k] for k in kw})
        for k, v in kw.items():
            mm.s[k] = st[k] + (v - st[k]) * al
    return UpdateFromAlphaFunc(m, f, run_time=rt, rate_func=rf)


def lab(text, color=TEXT, size=30, bold=True):
    return T(text, size, color, weight=BOLD if bold else NORMAL)


def tag(text, color, size=28):
    return VGroup(Dot(radius=0.11, color=color), T(text, size, TEXT)).arrange(RIGHT, buff=0.18)


def chaikin(pts, n=2):
    for _ in range(n):
        out = []
        for i in range(len(pts)):
            a, b = pts[i], pts[(i + 1) % len(pts)]
            out += [0.75 * a + 0.25 * b, 0.25 * a + 0.75 * b]
        pts = out
    return pts


def freeze(m):
    m.update(0)
    for sm in m.get_family():
        sm.clear_updaters()
    return m


# ------------------------------------------------------------------ level strip
class Strip(VGroup):
    X = -5.9

    def __init__(self, done=0):
        super().__init__()
        self.boxes, self.labs = [], []
        for i, (name, col) in enumerate(LEVELS):
            y = -2.7 + 1.35 * i
            b = RoundedRectangle(corner_radius=0.12, width=1.8, height=1.2, stroke_color=col, stroke_width=5,
                                 fill_color=col, fill_opacity=0).move_to([self.X, y, 0])
            l = T(name, 24, TEXT, weight=BOLD, line_spacing=0.7).move_to(b)
            l.set_opacity(0)
            self.boxes.append(b)
            self.labs.append(l)
            self.add(b, l)
        for i in range(done):
            self.boxes[i].set_fill(LEVELS[i][1], 0.5)
            self.labs[i].set_opacity(1)

    def fill(self, i):
        return [self.boxes[i].animate.set_fill(LEVELS[i][1], 0.5), self.labs[i].animate.set_opacity(1)]

    def flash(self, i, rt=0.55):
        col = LEVELS[i][1]
        return self.boxes[i].animate(rate_func=there_and_back, run_time=rt).set_stroke(TEXT, 10).set_fill(col, 0.95)


# ------------------------------------------------------------------ red blood cell (biconcave disc, real profile)
C0, C2, C4 = 0.207, 2.003, -1.123


def zprof(r):
    r = min(abs(r), 1.0)
    return 0.5 * math.sqrt(max(0.0, 1 - r * r)) * (C0 + C2 * r * r + C4 * r ** 4)


DOTS = [(-0.45, 0.35), (0.1, 0.55), (0.5, 0.2), (-0.1, -0.1), (-0.5, -0.4), (0.35, -0.45), (0.0, 0.0)]


class RBC(VGroup):
    def __init__(self, pos=(0, 0), D=2.2, tau=0.0, dots=0.0, tube=None, ang=0.0, alpha=1.0, wob=0.0):
        super().__init__()
        self.s = dict(x=pos[0], y=pos[1], D=D, L=1.0, h=1.0, tau=tau, bias=0.0, ang=ang, dots=dots, fly=1.0,
                      alpha=alpha, wob=wob, dim=1.0)
        self.tube, self.t, self.first = tube, 0.0, True
        self.body = VMobject(stroke_color=RIM, stroke_width=4, fill_color=RED, fill_opacity=0.95)
        self.dimple = VMobject(stroke_width=0, fill_color="#B8352E", fill_opacity=0.8)
        self.dotm = VGroup(*[Dot(radius=0.1, color=CYAN) for _ in DOTS])
        self.add(self.body, self.dimple, self.dotm)
        self.add_updater(lambda m, dt: m._upd(dt))
        self._upd(0)

    def _upd(self, dt):
        s = self.s
        self.t += dt
        if self.tube is not None:
            ht = min(1.0, 2 * self.tube.hw(s["x"] + 0.9) * 0.9 / s["D"])
            if self.first or dt == 0:
                s["h"] = ht
            else:
                s["h"] += (ht - s["h"]) * min(1.0, dt * 5.0)
            s["L"] = (1.0 / s["h"]) ** 0.7
            s["bias"] = 1.0 - s["h"]
        self.first = False
        tau = min(1.0, max(0.0, s["tau"] + s["wob"] * (0.5 - 0.5 * math.cos(self.t * 2.0))))
        R = s["D"] / 2
        ca, sa = math.cos(s["ang"]), math.sin(s["ang"])
        Rm = np.array([[ca, -sa, 0], [sa, ca, 0], [0, 0, 1]])
        c = np.array([s["x"], s["y"], 0.0])
        pts = []
        for th in np.linspace(0, 2 * math.pi, 90, endpoint=False):
            cx, sy = math.cos(th), math.sin(th)
            side = zprof(cx) * (1 if sy >= 0 else -1)
            yu = (1 - tau) * sy + tau * side
            f = (1 - 0.28 * s["bias"] * cx) / (1 + 0.28 * s["bias"])
            pts.append(c + Rm @ np.array([cx * R * s["L"], yu * R * s["h"] * f, 0]))
        a = s["alpha"]
        self.body.set_points_as_corners(pts + [pts[0]])
        self.body.set_fill(RED, 0.95 * a).set_stroke(RIM, 4, opacity=a)
        dp = []
        for th in np.linspace(0, 2 * math.pi, 40, endpoint=False):
            dp.append(c + Rm @ np.array([0.5 * R * s["L"] * math.cos(th), 0.5 * R * s["h"] * math.sin(th) * (1 - tau), 0]))
        self.dimple.set_points_as_corners(dp + [dp[0]])
        self.dimple.set_fill("#B8352E", 0.8 * a * (1 - tau) * s["dim"])
        for d, (u, v) in zip(self.dotm, DOTS):
            home = c + Rm @ np.array([u * R * s["L"] * 0.8, v * R * s["h"] * 0.8 * (1 - 0.7 * tau), 0])
            away = home + np.array([u, v, 0]) / (math.hypot(u, v) + 0.2) * 3.5
            d.move_to(home + (away - home) * (1 - s["fly"]))
            d.set_opacity(min(1.0, s["dots"]) * a)


def smoothstep(x):
    return smooth(x)


class Tube(VGroup):
    X0, X1 = -4.6, 6.6

    def hw(self, x):
        if x <= -0.6:
            return 1.7
        if x < 0.5:
            return 1.7 - 1.2 * smooth((x + 0.6) / 1.1)
        if x < 3.3:
            return 0.5
        if x < 4.4:
            return 0.5 + 1.2 * smooth((x - 3.3) / 1.1)
        return 1.7

    def __init__(self):
        super().__init__()
        xs = np.linspace(self.X0, self.X1, 140)
        top = [[x, self.hw(x), 0] for x in xs]
        bot = [[x, -self.hw(x), 0] for x in xs]
        self.inner = VMobject(stroke_width=0, fill_color="#3B1D2B", fill_opacity=0.6)
        self.inner.set_points_as_corners(top + bot[::-1] + [top[0]])
        self.wt = VMobject().set_points_as_corners(top).set_stroke(VESSEL, 10)
        self.wb = VMobject().set_points_as_corners(bot).set_stroke(VESSEL, 10)
        self.add(self.inner, self.wt, self.wb)


# ------------------------------------------------------------------ heart muscle cell (short, branching, striped)
class HCell(VGroup):
    def __init__(self, pos=(0, 0), b=1.0, A=2.4, own=False, amp=1.0):
        super().__init__()
        self.s = dict(x=pos[0], y=pos[1], b=b, A=A, f=0.0, amp=amp, op=1.0)
        self.own = own
        self.body = VMobject(stroke_color=PURPLE, stroke_width=4, fill_color="#3A2866", fill_opacity=0.95)
        self.stripes = VGroup(*[Line(ORIGIN, UP) for _ in range(7)]).set_stroke("#B79CFF", 3, opacity=0.8)
        self.add(self.body, self.stripes)
        self.add_updater(lambda m, dt: m._upd())
        self._upd()

    def _upd(self):
        s = self.s
        if self.own:
            s["f"] = s["amp"] * pulse()
        b = s["b"] * (1 + 0.12 * s["f"])
        A = s["A"] * (1 - 0.22 * s["f"]) * s["b"] / b
        o = np.array([s["x"], s["y"], 0.0])
        P = [(-A, 0.85), (A, 0.85), (A + 0.9, 1.6), (A + 1.25, 1.3), (A + 0.55, 0.18), (A + 0.55, -0.18), (A + 1.25, -1.3),
             (A + 0.9, -1.6), (A, -0.85), (-A, -0.85), (-A - 0.6, -0.3), (-A - 0.6, 0.3)]
        pts = chaikin([o + np.array([x * b, y * b, 0]) for x, y in P], 2)
        self.body.set_points_as_corners(pts + [pts[0]])
        for i, ln in enumerate(self.stripes):
            x = (-0.78 + 1.56 * i / 6) * A
            ln.put_start_and_end_on(o + np.array([x * b, -0.62 * b, 0]), o + np.array([x * b, 0.62 * b, 0]))
        op = s["op"]
        self.stripes.set_stroke("#B79CFF", max(1.5, 3 * min(1.0, s["b"] / 0.6)), opacity=0.8 * op)
        self.body.set_stroke(PURPLE, max(2.0, 4 * min(1.0, s["b"] / 0.6)), opacity=op)
        self.body.set_fill("#3A2866", 0.95 * op)


SLOTS = [(-1.3, 1.3), (1.25, 1.3), (-2.575, 0), (-0.025, 0), (2.525, 0), (-1.3, -1.3), (1.25, -1.3)]
LAGS = [0.25, 0.3, 0.0, 0.05, 0.1, 0.45, 0.5]
STARTS = [(STAGE_X - 1.3, 5.5), (STAGE_X + 1.25, 5.5), (STAGE_X - 2.575, -5.5), (1.2, -0.7), (9.5, 0.0),
          (STAGE_X - 1.3, -5.5), (STAGE_X + 1.25, -5.5)]


class Network(VGroup):
    """Seven heart muscle cells. go=0: the middle one stands where the single cell stood, the others wait off screen;
    go=1: linked end to end in a brick pattern (the tissue)."""
    B0, A0 = 0.42, 2.7

    def __init__(self, pos=(STAGE_X, 0), sc=1.0, amp=1.0, hull=0.0, go=1.0):
        super().__init__()
        self.s = dict(x=pos[0], y=pos[1], sc=sc, amp=amp, hull=hull, go=go, op=1.0)
        self.cells = [HCell((0, 0), self.B0, self.A0) for _ in SLOTS]
        self.hullm = RoundedRectangle(corner_radius=0.5, width=8.7, height=4.7, stroke_color=TBLUE, stroke_width=6,
                                      fill_color=TBLUE, fill_opacity=0)
        self.add(self.hullm, *self.cells)
        self.add_updater(lambda m, dt: m._upd())
        self._upd()

    def _upd(self):
        s = self.s
        f = s["amp"] * pulse()
        sc = s["sc"]
        for i, (c, (rx, ry)) in enumerate(zip(self.cells, SLOTS)):
            al = smooth((s["go"] - LAGS[i]) / 0.5)
            tx, ty = s["x"] + sc * rx * (1 - 0.12 * f), s["y"] + sc * ry
            sx, sy = STARTS[i]
            c.s.update(x=sx + (tx - sx) * al, y=sy + (ty - sy) * al, f=f, op=s["op"])
            if i == 3:
                c.s.update(b=1.0 + (self.B0 * sc - 1.0) * al, A=2.4 + (self.A0 - 2.4) * al)
            else:
                c.s.update(b=self.B0 * sc, A=self.A0)
        hp = min(1.0, s["hull"] * 2) * s["op"]
        self.hullm.stretch_to_fit_width(8.7 * sc * (1 - 0.12 * f))
        self.hullm.stretch_to_fit_height(4.7 * sc)
        self.hullm.move_to([s["x"] - 0.03 * sc, s["y"], 0])
        self.hullm.set_stroke(TBLUE, max(2, 6 * min(1, sc)), opacity=hp)
        self.hullm.set_fill(TBLUE, 0.1 * hp)


# ------------------------------------------------------------------ heart (organ)
def heart_pts(cx, cy, h, n=90):
    sc = h / 29.0
    out = []
    for t in np.linspace(0, 2 * math.pi, n, endpoint=False):
        x = 16 * math.sin(t) ** 3
        y = 13 * math.cos(t) - 5 * math.cos(2 * t) - 2 * math.cos(3 * t) - math.cos(4 * t)
        out.append(np.array([cx + x * sc, cy + (y + 2.5) * sc, 0.0]))
    return out


def set_heart(m, cx, cy, h):
    p = heart_pts(cx, cy, h)
    m.set_points_as_corners(p + [p[0]])


class HeartOrgan(VGroup):
    """detail=True: tan coat, pink lining and the blue muscle network inside, green outline.
    mix 0 -> 1 shrinks the network from its tissue size into the heart's middle."""

    def __init__(self, pos=(STAGE_X, 0), h=4.8, detail=True, beat=1.0, mix=1.0, cp=1.0, olp=1.0, fillp=1.0, dop=1.0):
        super().__init__()
        self.s = dict(x=pos[0], y=pos[1], h=h, beat=beat, olp=olp, fillp=fillp, cp=cp, mix=mix, dop=dop)
        self.detail = detail
        self.coat = VMobject(stroke_color="#C9B28A", stroke_width=14, fill_color="#5B2330", fill_opacity=0.7)
        self.lin = VMobject(stroke_color="#F4A6B7", stroke_width=8, fill_opacity=0)
        self.out = VMobject(stroke_color=GREEN, stroke_width=6, fill_opacity=0)
        self.net = None
        parts = [self.coat]
        if detail:
            self.net = Network((pos[0], pos[1]), 1.0, amp=1.0, hull=1.0)
            parts += [self.lin, self.net]
        parts.append(self.out)
        self.add(*parts)
        self.add_updater(lambda m, dt: m._upd())
        self._upd()

    def _upd(self):
        s = self.s
        h = s["h"] * (1 + 0.045 * s["beat"] * pulse())
        k = max(0.3, min(1.0, s["h"] / 4.8))
        set_heart(self.coat, s["x"], s["y"], h)
        set_heart(self.out, s["x"], s["y"], h * 1.08)
        self.out.set_stroke(GREEN, max(2.5, 6 * min(1.0, s["h"] / 3)), opacity=s["olp"])
        self.coat.set_stroke("#C9B28A", 14 * k, opacity=s["cp"])
        self.coat.set_fill("#5B2330", 0.7 * s["fillp"])
        if self.detail:
            set_heart(self.lin, s["x"], s["y"], h * 0.9)
            self.lin.set_stroke("#F4A6B7", 8 * k, opacity=s["cp"] * s["dop"])
            mx = s["mix"]
            self.net.s.update(x=s["x"], y=s["y"] + 0.04 * s["h"] * mx, sc=1.0 + (0.0937 * s["h"] - 1.0) * mx, op=s["dop"])


# ------------------------------------------------------------------ the body (carried from scene to scene)
K, BC = 0.95, (STAGE_X, -0.1)
PERSON = [(-0.6, 2.3), (-2.0, 2.2), (-2.7, 1.5), (-2.8, -0.5), (-2.1, -0.5), (-1.9, 0.6), (-1.8, -0.9), (-1.7, -3.7), (-0.1, -3.7), (0, -1.2),
          (0.1, -3.7), (1.7, -3.7), (1.8, -0.9), (1.9, 0.6), (2.1, -0.5), (2.8, -0.5), (2.7, 1.5), (2.0, 2.2), (0.6, 2.3)]


def Pt(x, y, k=K, c=BC):
    return np.array([c[0] + x * k, c[1] + y * k, 0.0])


def person(k=K, c=BC):
    body = Polygon(*[Pt(x, y, k, c) for x, y in PERSON]).round_corners(0.3 * k)
    head = Circle(radius=0.65 * k).move_to(Pt(0, 3.05, k, c))
    return VGroup(body, head).set_stroke(GREY, 4).set_fill(GREY, 0)


def in_person(x, y):
    if x * x + (y - 3.05) ** 2 < 0.62 ** 2:
        return True
    inside = False
    n = len(PERSON)
    for i in range(n):
        x1, y1 = PERSON[i]
        x2, y2 = PERSON[(i + 1) % n]
        if (y1 > y) != (y2 > y) and x < (x2 - x1) * (y - y1) / (y2 - y1) + x1:
            inside = not inside
    return inside


def mesh(k=K, c=BC, colorfn=None, step=0.27, r=0.055, lo=0.6, hi=1.0):
    rng = random.Random(5)
    g = VGroup()
    for j, y in enumerate(np.arange(-3.6, 3.75, step * 0.9)):
        for x in np.arange(-2.8, 2.85, step):
            xx = x + (step / 2 if j % 2 else 0)
            if in_person(xx, y):
                col = colorfn(xx, y) if colorfn else "#C7D2E8"
                d = Dot(radius=r * k * 1.5, color=col)
                d.move_to([c[0] + xx * k, c[1] + y * k, 0])
                d.ph = rng.uniform(0, 6.28)
                g.add(d)
    g.t = 0.0

    def sh(m, dt):
        m.t += dt
        for d in m:
            d.set_opacity(lo + (hi - lo) * (0.5 + 0.5 * math.sin(1.6 * m.t + d.ph)))
    g.add_updater(sh)
    return g


def lattice(c, R=3.15, sp=1.12):
    pts = []
    rows = int(R / (sp * 0.866)) + 1
    for j in range(-rows, rows + 1):
        y = j * sp * 0.866
        for i in range(-6, 7):
            x = (i + (j % 2) * 0.5) * sp
            if math.hypot(x, y) <= R:
                pts.append(np.array([c[0] + x, c[1] + y, 0.0]))
    return pts


class Cluster(VGroup):
    def __init__(self, c=(1.5, 0)):
        super().__init__()
        self.c = np.array([c[0], c[1], 0.0])
        self.pts = lattice(c)
        self.edges = [(i, j) for i in range(len(self.pts)) for j in range(i + 1, len(self.pts)) if np.linalg.norm(self.pts[i] - self.pts[j]) < 1.18]
        self.nbr = {i: [] for i in range(len(self.pts))}
        for i, j in self.edges:
            self.nbr[i].append(j)
            self.nbr[j].append(i)
        self.chan = VGroup(*[Line(self.pts[i], self.pts[j]) for i, j in self.edges]).set_stroke(WATER, 6, opacity=0.8)
        self.cells = VGroup(*[Circle(radius=0.44, stroke_color=TEXT, stroke_width=3, fill_color="#E8EAF0", fill_opacity=0.85).move_to(p) for p in self.pts])
        self.add(self.chan, self.cells)


class Walkers(VGroup):
    def __init__(self, cl, n=18, seed=4):
        super().__init__()
        rng = random.Random(seed)
        self.cl, self.rng, self.on = cl, rng, 0.0
        self.recs = []
        for k in range(n):
            self.add(Dot(radius=0.1, color=AMBER if k % 2 else CYAN).set_opacity(0))
            i = rng.randrange(len(cl.pts))
            self.recs.append([i, rng.choice(cl.nbr[i]), rng.random()])
        self.add_updater(lambda m, dt: m._u(dt))

    def _u(self, dt):
        cl = self.cl
        for d, r in zip(self.submobjects, self.recs):
            r[2] += dt * 0.5
            if r[2] >= 1:
                r[2] -= 1
                prev = r[0]
                r[0] = r[1]
                opts = [x for x in cl.nbr[r[0]] if x != prev] or cl.nbr[r[0]]
                r[1] = self.rng.choice(opts)
            d.move_to(cl.pts[r[0]] * (1 - r[2]) + cl.pts[r[1]] * r[2])
            d.set_opacity(self.on)


def groups_of(cl):
    phis = [60, 0, -60, -120, 180, 120]
    used, out = set(), []
    for ph in phis:
        tgt = cl.c + 2.0 * np.array([math.cos(math.radians(ph)), math.sin(math.radians(ph)), 0])
        order = sorted((i for i in range(len(cl.pts)) if i not in used), key=lambda i: np.linalg.norm(cl.pts[i] - tgt))[:3]
        used.update(order)
        out.append(order)
    return out


def tinted_cluster():
    cl = Cluster((STAGE_X, 0))
    grp = groups_of(cl)
    for k, gr in enumerate(grp):
        for i in gr:
            cl.cells[i].set_fill(JOB[k], 0.9).set_stroke(JOB[k])
    return cl, grp


# vessel tree in body coordinates
TREE = {
    "trunk": [(0.25, 0.55), (0.1, -0.3), (0.0, -1.2)],
    "legL": [(0.0, -1.2), (-0.9, -1.5), (-0.95, -2.5), (-0.95, -3.35)],
    "legR": [(0.0, -1.2), (0.9, -1.5), (0.95, -2.5), (0.95, -3.35)],
    "armL": [(0.2, 0.7), (-1.0, 1.65), (-2.3, 1.2), (-2.45, 0.2), (-2.45, -0.3)],
    "armR": [(0.3, 0.7), (1.0, 1.65), (2.3, 1.2), (2.45, 0.2), (2.45, -0.3)],
    "head": [(0.25, 0.7), (0.1, 1.6), (0.0, 2.3), (0.0, 3.0)],
}


def path_pts(key):
    return [Pt(x, y) for x, y in TREE[key]]


def vessel_group(width_scale=1.0, color=VESSEL):
    g = VGroup()
    for key in TREE:
        w = (9 if key == "trunk" else 6) * width_scale
        g.add(VMobject().set_points_as_corners(path_pts(key)).set_stroke(color, w))
    return g


class PathFlow(VGroup):
    """Small red discs that run along polylines (blood cells in vessels)."""

    def __init__(self, paths, per=3, color=RED, speed=0.16, r=0.12, seed=2, vfun=None):
        super().__init__()
        rng = random.Random(seed)
        self.paths = paths
        self.lens = []
        for p in paths:
            seg = [np.linalg.norm(p[i + 1] - p[i]) for i in range(len(p) - 1)]
            self.lens.append(seg)
        self.recs = []
        for pi in range(len(paths)):
            for k in range(per):
                self.add(Dot(radius=r, color=color).set_opacity(0))
                self.recs.append([pi, (k + rng.random() * 0.4) / per, rng.uniform(0.85, 1.15)])
        self.on, self.speed, self.vfun = 0.0, speed, vfun
        self.add_updater(lambda m, dt: m._u(dt))

    def at(self, pi, u):
        seg = self.lens[pi]
        tgt = u * sum(seg)
        for i, L in enumerate(seg):
            if tgt <= L or i == len(seg) - 1:
                a = min(1.0, tgt / L) if L else 0
                return self.paths[pi][i] * (1 - a) + self.paths[pi][i + 1] * a
            tgt -= L

    def _u(self, dt):
        v = self.speed * (self.vfun() if self.vfun else 1.0)
        for d, r in zip(self.submobjects, self.recs):
            r[1] = (r[1] + dt * v * r[2]) % 1.0
            d.move_to(self.at(r[0], r[1]))
            d.set_opacity(min(1.0, 5 * r[1], 5 * (1 - r[1])) * self.on)


def lungs():
    L = Ellipse(width=1.0 * K, height=1.5 * K).move_to(Pt(-0.75, 1.1))
    R = Ellipse(width=1.0 * K, height=1.5 * K).move_to(Pt(1.3, 1.1))
    return VGroup(L, R).set_stroke("#9FB4C9", 4).set_fill("#9FB4C9", 0.2)


def toe_cells():
    g = VGroup()
    for sgn in (-1, 1):
        for dx, dy in [(-0.2, 0.1), (0.2, 0.1), (0.0, -0.17), (-0.4, -0.2), (0.4, -0.2)]:
            c = Pt(sgn * 0.95, -3.3) + np.array([dx, dy, 0]) * 0.8
            g.add(Circle(radius=0.15, stroke_color=PURPLE, stroke_width=3, fill_color=PURPLE, fill_opacity=0.25).move_to(c))
    return g


def nerve_cell(sc=1.0, c=(0, 0), vertical=True, pulse_on=True):
    """Cell body with short branches and one long branch (schematic)."""
    c = np.array([c[0], c[1], 0.0])
    g = VGroup()
    soma = Circle(radius=0.42 * sc, stroke_color=PURPLE, stroke_width=4, fill_color="#3A2866", fill_opacity=0.95).move_to(c)
    for a in [100, 150, 200, 250, 60, 20]:
        d = np.array([math.cos(math.radians(a)), math.sin(math.radians(a)), 0])
        g.add(Line(c + d * 0.4 * sc, c + d * 0.95 * sc).set_stroke(PURPLE, 4))
    axon_pts = [c + np.array([0.0, -0.4 * sc, 0]), c + np.array([0.1 * sc, -1.2 * sc, 0]), c + np.array([-0.1 * sc, -2.0 * sc, 0]),
                c + np.array([0.0, -2.8 * sc, 0])]
    ax = VMobject().set_points_smoothly(axon_pts).set_stroke(PURPLE, 5)
    g.add(ax, soma)
    return g


# ================================================================== scenes
class S00Title(TitleCard):
    LESSON = "From Cells to Organisms"
    TITLE = "One Job, Five Levels"


class S01Question(SpokenScene):
    def construct(self):
        self.add(ClockMob())
        cl, grp = tinted_cluster()
        wk = Walkers(cl)
        wk.on = 1
        strip = Strip(0)
        self.add(cl, wk)
        self.play(FadeIn(strip, shift=RIGHT * 0.3), run_time=0.8)
        self.at("many small cells")
        flashes = [cl.cells[i].animate(rate_func=there_and_back).scale(1.3) for gr in grp for i in gr]
        self.play(LaggedStart(*flashes, lag_ratio=0.03, run_time=2.0))
        self.at("who gets oxygen")
        outl = person()
        ms = mesh()
        self.play(FadeOut(cl, scale=0.4), FadeOut(wk), Create(outl),
                  LaggedStart(*[FadeIn(d) for d in ms], lag_ratio=0.004, run_time=1.7), run_time=1.7)
        self.at("toes,")
        rings = VGroup(*[Circle(radius=0.45, stroke_color=YELLOW, stroke_width=6).move_to(Pt(s_ * 0.95, -3.45)) for s_ in (-1, 1)])
        rings.t = 0.0

        def pul(m, dt):
            m.t += dt
            for r_ in m:
                r_.set_stroke(YELLOW, 6, opacity=0.55 + 0.45 * math.sin(4 * m.t))
        rings.add_updater(pul)
        tl = lab("toes", YELLOW).move_to([5.0, -3.3, 0])
        ta = Arrow(tl.get_left() + LEFT * 0.05, Pt(1.0 + 0.0, -3.45) + RIGHT * 0.55, buff=0.05, color=YELLOW, stroke_width=4, tip_length=0.18)
        self.play(FadeIn(rings), FadeIn(tl), GrowArrow(ta), run_time=0.7)
        self.at("far from your")
        lg = lungs()
        o2 = VGroup(*[Dot(radius=0.11, color=CYAN).move_to(Pt(1.3, 1.1) + np.array([dx, dy, 0])) for dx, dy in [(0, 0.2), (-0.15, -0.1), (0.15, -0.1)]])
        ll = lab("lungs", TEXT).move_to([5.3, 1.3, 0])
        la = Arrow(ll.get_left() + LEFT * 0.05, Pt(1.3, 1.1) + RIGHT * 0.5, buff=0.05, color=TEXT, stroke_width=4, tip_length=0.18)
        self.play(Create(lg), FadeIn(o2, scale=1.5), FadeIn(ll), GrowArrow(la), run_time=1.0)
        o2.t = 0.0
        o2.add_updater(lambda m, dt: (setattr(m, "t", m.t + dt), m.set_opacity(0.7 + 0.3 * math.sin(5 * m.t))))
        self.at("lungs?")
        d1 = DashedVMobject(VMobject().set_points_as_corners([Pt(1.3, 0.3), Pt(0.2, -0.9), Pt(-0.9, -1.5), Pt(-0.95, -3.0)]), num_dashes=22).set_stroke(YELLOW, 5)
        d2 = DashedVMobject(VMobject().set_points_as_corners([Pt(1.3, 0.3), Pt(0.9, -1.5), Pt(0.95, -3.0)]), num_dashes=16).set_stroke(YELLOW, 5)
        q = T("?", 120, GOLD, weight=BOLD).move_to(Pt(0.05, -0.2))
        self.play(Create(d1), Create(d2), FadeIn(q, scale=0.4), run_time=1.3)
        self.at("Those toe cells")
        self.play(q.animate.scale(1.2), run_time=0.8, rate_func=there_and_back)
        self.finish()


class S02Rbc(SpokenScene):
    def construct(self):
        self.add(ClockMob())
        strip = Strip(0)
        outl = person()
        ms = mesh()
        rings = VGroup(*[Circle(radius=0.45, stroke_color=YELLOW, stroke_width=6, stroke_opacity=0.8).move_to(Pt(s_ * 0.95, -3.45)) for s_ in (-1, 1)])
        lg = lungs()
        self.add(strip, outl, ms, lg, rings)
        cell = RBC((STAGE_X, 0.0), D=0.3, tau=0.0, dots=0.0)
        cell.s["fly"] = 0.0
        self.add(cell)
        ms.clear_updaters()
        self.play(FadeOut(VGroup(outl, ms, lg, rings), scale=3.0), tw(cell, 2.0, D=4.2), run_time=2.0)
        self.at("one kind of")
        self.play(*strip.fill(0), run_time=0.6)
        self.at("A red blood cell")
        rl = lab("red blood cell", RED, 36).move_to([STAGE_X, 3.2, 0])
        self.play(FadeIn(rl, shift=DOWN * 0.1), run_time=0.5)
        self.at("flexible")
        self.play(tw(cell, 1.0, tau=0.3), run_time=1.0)
        self.play(tw(cell, 0.7, tau=0.0), run_time=0.7)
        self.at("dented on both")
        self.play(tw(cell, 1.5, tau=1.0), run_time=1.5)
        a1 = Arrow([STAGE_X, 1.9, 0], [STAGE_X, 0.35, 0], buff=0, color=TEXT, stroke_width=5, tip_length=0.2)
        a2 = Arrow([STAGE_X, -1.9, 0], [STAGE_X, -0.35, 0], buff=0, color=TEXT, stroke_width=5, tip_length=0.2)
        dl = lab("dent", TEXT, 32).move_to([STAGE_X + 1.0, 1.5, 0])
        dl2 = lab("dent", TEXT, 32).move_to([STAGE_X + 1.0, -1.5, 0])
        self.play(GrowArrow(a1), GrowArrow(a2), FadeIn(dl), FadeIn(dl2), run_time=0.6)
        self.at("It carries")
        self.play(FadeOut(VGroup(a1, a2, dl, dl2)), tw(cell, 1.0, tau=0.0), run_time=1.0)
        cell.s["dots"] = 1.0
        self.play(tw(cell, 1.3, fly=1.0), run_time=1.3)
        self.finish()


class S03Specialized(SpokenScene):
    def construct(self):
        self.add(ClockMob())
        strip = Strip(1)
        cell = RBC((STAGE_X, 0.2), D=3.4, dots=1.0, wob=0.3)
        self.add(strip, cell)
        self.at("shape")
        self.play(ShowPassingFlash(cell.body.copy().set_stroke(YELLOW, 12), time_width=0.6), run_time=1.4)
        self.at("one kind of job")
        self.play(ShowPassingFlash(cell.dimple.copy().set_fill(opacity=0).set_stroke(YELLOW, 8), time_width=0.7), run_time=1.0)
        self.at("specialized cell")
        sl = lab("specialized cell", PURPLE, 38).move_to([STAGE_X, 2.95, 0])
        sa = Arrow(sl.get_bottom() + DOWN * 0.05, [STAGE_X, 1.95, 0], buff=0, color=PURPLE, stroke_width=5, tip_length=0.2)
        self.play(FadeIn(sl, shift=DOWN * 0.1), GrowArrow(sa), run_time=0.7)
        self.at("a mature")
        ghost = Circle(radius=0.62, stroke_color=GREY, stroke_width=5, fill_color=PURPLE, fill_opacity=0.35).move_to([STAGE_X, 0.2, 0])
        ghost_d = DashedVMobject(ghost.copy().set_fill(opacity=0), num_dashes=24).set_stroke(TEXT, 5)
        self.play(FadeIn(ghost), FadeIn(ghost_d), run_time=0.6)
        self.at("no nucleus")
        nl = lab("no nucleus when mature", TEXT, 34).move_to([STAGE_X, -2.55, 0])
        self.play(FadeOut(ghost, scale=1.6), FadeOut(ghost_d, scale=1.6), FadeIn(nl, shift=UP * 0.1), run_time=1.2)
        self.finish()


def squeeze_stage(cell_x=-1.7, with_cell=True, strip_done=1):
    tube = Tube()
    cell = RBC((cell_x, 0.0), D=2.2, dots=1.0, tube=tube)
    return tube, cell


class S04Predict(SpokenScene):
    def construct(self):
        self.add(ClockMob())
        strip = Strip(1)
        tube = Tube()
        cell = RBC((STAGE_X, 0.2), D=3.4, dots=1.0, tube=None)
        self.add(strip, cell)
        self.play(tw(cell, 1.1, x=-1.7, y=0.0, D=2.2), FadeIn(tube.inner), run_time=1.1)
        cell.tube = tube
        self.at("blood vessel narrower")
        self.play(Create(tube.wt), Create(tube.wb), run_time=1.0)
        self.at("narrower than")
        up = DashedLine([-1.7, 1.1, 0], [3.2, 1.1, 0], dash_length=0.15).set_stroke(YELLOW, 4)
        dn = DashedLine([-1.7, -1.1, 0], [3.2, -1.1, 0], dash_length=0.15).set_stroke(YELLOW, 4)
        self.play(Create(up), Create(dn), run_time=0.6)
        self.at("What would let")
        for _ in range(2):
            self.play(tw(cell, 0.7, x=-1.45), run_time=0.7)
            self.play(tw(cell, 0.7, x=-1.7), run_time=0.7)
        self.at("Pause")
        pp = lab("Pause and predict", GOLD, 42).move_to([STAGE_X, 3.1, 0])
        self.play(FadeIn(pp, shift=DOWN * 0.15), run_time=0.7)
        self.finish()


class S05Pause(NarratedScene):
    def construct(self):
        self.add(ClockMob())
        strip = Strip(1)
        tube = Tube()
        cell = RBC((-1.7, 0.0), D=2.2, dots=1.0, tube=tube)
        up = DashedLine([-1.7, 1.1, 0], [3.2, 1.1, 0], dash_length=0.15).set_stroke(YELLOW, 4)
        dn = DashedLine([-1.7, -1.1, 0], [3.2, -1.1, 0], dash_length=0.15).set_stroke(YELLOW, 4)
        pp = lab("Pause and predict", GOLD, 42).move_to([STAGE_X, 3.1, 0])
        bar = Rectangle(width=12.0, height=0.12, stroke_width=0, fill_color=GOLD, fill_opacity=0.9).move_to([0, -3.72, 0])
        self.add(strip, tube, cell, up, dn, pp, bar)
        cell.add_updater(lambda m, dt: m.s.__setitem__("x", -1.7 + 0.12 * math.sin(CLK["t"] * 2.2)))

        def f(m, al):
            m.stretch_to_fit_width(12.0 * (1 - al))
            m.move_to([-6.0 + m.width / 2, -3.72, 0])
        self.play(UpdateFromAlphaFunc(bar, f, run_time=4.6, rate_func=linear))
        self.finish()


class S06Reveal(SpokenScene):
    def construct(self):
        self.add(ClockMob())
        strip = Strip(1)
        tube = Tube()
        cell = RBC((-1.7, 0.0), D=2.2, dots=1.0, tube=tube)
        pp = lab("Pause and predict", GOLD, 42).move_to([STAGE_X, 3.1, 0])
        self.add(strip, tube, cell, pp)
        sl = lab("its shape", TEXT, 42).move_to([STAGE_X, 3.1, 0])
        self.play(FadeOut(pp), FadeIn(sl), run_time=0.5)
        self.at("flexible disc")
        sl2 = lab("flexible disc", TEXT, 42).move_to([STAGE_X, 3.1, 0])
        self.play(ReplacementTransform(sl, sl2), run_time=0.4)
        t0 = self.elapsed()

        def runner(m, dt):
            tt = self.elapsed() - t0
            m.s["x"] = -1.7 + 1.15 * min(max(tt, 0.0), 6.1)
        cell.add_updater(runner)
        self.at("bends and folds")
        l3 = lab("bends and folds", TEXT, 42).move_to([STAGE_X, 3.1, 0])
        self.play(ReplacementTransform(sl2, l3), run_time=0.4)
        self.at("springs back")
        l4 = lab("springs back", TEXT, 42).move_to([STAGE_X, 3.1, 0])
        self.play(ReplacementTransform(l3, l4), run_time=0.4)
        self.finish()


def vessel_top(y=2.45, hw=0.75):
    inner = Rectangle(width=11.2, height=2 * hw, stroke_width=0, fill_color="#3B1D2B", fill_opacity=0.6).move_to([1.0, y, 0])
    wt = Line([-4.6, y + hw, 0], [6.6, y + hw, 0]).set_stroke(VESSEL, 10)
    wb = Line([-4.6, y - hw, 0], [6.6, y - hw, 0]).set_stroke(VESSEL, 10)
    return VGroup(inner, wt, wb)


def top_flow(alpha0=1.0):
    discs = [RBC((x, 2.45), D=0.95, dots=1.0, alpha=alpha0) for x in (-3.4, -0.4, 2.6, 5.6)]
    dg = VGroup(*discs)

    def flow(m, dt):
        v = 0.55 + 2.2 * pulse()
        for d in discs:
            d.s["x"] += v * dt
            if d.s["x"] > 6.3:
                d.s["x"] -= 10.8
            x = d.s["x"]
            d.s["alpha"] = min(1.0, max(0.0, min(x + 4.4, 6.2 - x) / 0.6))
    dg.add_updater(flow)
    return dg


class S07Pump(SpokenScene):
    def construct(self):
        self.add(ClockMob())
        strip = Strip(1)
        tube0 = Tube()
        cell0 = RBC((5.3, 0.0), D=2.2, dots=1.0, tube=tube0)
        self.add(strip, tube0, cell0)
        self.at("blood has to")
        tube1 = vessel_top()
        dg = top_flow(0.0)
        self.play(FadeOut(tube0), FadeOut(cell0), FadeIn(tube1), run_time=0.7)
        self.add(dg)
        self.at("heart muscle cells")
        hc = HCell((1.2, -0.7), 1.0, 2.4, own=True)
        self.play(GrowFromCenter(hc), run_time=1.0)
        hl = lab("heart muscle cell", PURPLE, 34).move_to([STAGE_X, -3.0, 0])
        self.play(FadeIn(hl, shift=UP * 0.1), run_time=0.5)
        self.at("striped")
        self.play(hc.stripes.animate(rate_func=there_and_back).set_stroke(TEXT, 6, opacity=1), run_time=1.0)
        self.at("shortens")
        hl2 = lab("heart muscle cell: shortens", PURPLE, 34).move_to([STAGE_X, -3.0, 0])
        self.play(ReplacementTransform(hl, hl2), run_time=0.5)
        self.finish()


class S08Tissue(SpokenScene):
    def construct(self):
        self.add(ClockMob())
        strip = Strip(1)
        tube1 = vessel_top()
        dg = top_flow()
        hl2 = lab("heart muscle cell: shortens", PURPLE, 34).move_to([STAGE_X, -3.0, 0])
        net = Network((STAGE_X, 0), 1.0, amp=1.0, hull=0.0, go=0.0)
        self.add(strip, tube1, dg, net, hl2)
        self.play(FadeOut(tube1), FadeOut(dg), FadeOut(hl2), run_time=0.6)
        self.play(tw(net, 3.6, go=1.0, rf=linear), run_time=3.6)
        self.at("Similar cells")
        tl = lab("tissue: similar cells, one job", TBLUE, 34).move_to([STAGE_X, 3.3, 0])
        self.at("form a tissue")
        self.play(tw(net, 1.0, hull=1.0), FadeIn(tl, shift=DOWN * 0.1), *strip.fill(1), run_time=1.0)
        self.at("This one is")
        tl2 = lab("heart muscle tissue", TBLUE, 34).move_to([STAGE_X, -3.3, 0])
        self.play(FadeIn(tl2, shift=UP * 0.1), run_time=0.6)
        self.at("its cells shorten")
        self.play(Indicate(tl2, color=TBLUE, scale_factor=1.08), run_time=1.0)
        self.finish()


class S09Organ(SpokenScene):
    def construct(self):
        self.add(ClockMob())
        strip = Strip(2)
        heart = HeartOrgan((STAGE_X, 0), 4.8, detail=True, mix=0.0, cp=0.0, olp=0.0, fillp=0.0)
        tl = lab("tissue: similar cells, one job", TBLUE, 34).move_to([STAGE_X, 3.3, 0])
        tl2 = lab("heart muscle tissue", TBLUE, 34).move_to([STAGE_X, -3.3, 0])
        self.add(strip, heart, tl, tl2)
        self.play(FadeOut(tl), FadeOut(tl2), tw(heart, 2.0, mix=1.0), run_time=2.0)
        self.at("other kinds")
        ol = lab("other tissues", "#C9B28A", 28).move_to([5.5, 2.75, 0])
        oa = Arrow(ol.get_left() + LEFT * 0.05, [STAGE_X + 2.3, 1.3, 0], buff=0.05, color="#C9B28A", stroke_width=4, tip_length=0.18)
        self.play(FadeIn(ol), GrowArrow(oa), tw(heart, 1.6, cp=1.0), run_time=1.6)
        self.at("Different tissues")
        gl = lab("organ: different tissues", GREEN, 34).move_to([STAGE_X, 3.3, 0])
        self.play(FadeOut(ol), FadeOut(oa), FadeIn(gl, shift=DOWN * 0.1), *strip.fill(2),
                  tw(heart, 1.0, olp=1.0, fillp=1.0), run_time=1.0)
        self.at("the heart")
        hl = lab("heart", GREEN, 34).move_to([STAGE_X, -3.3, 0])
        self.play(FadeIn(hl, shift=UP * 0.1), run_time=0.6)
        self.finish()


def body_state():
    outl = person().set_stroke(GREY, 3, opacity=0.6)
    return outl


class S10System(SpokenScene):
    def construct(self):
        self.add(ClockMob())
        strip = Strip(3)
        for i in (3,):
            strip.boxes[i].set_fill(ORANGE, 0)
            strip.labs[i].set_opacity(0)
        heart = HeartOrgan((STAGE_X, 0), 4.8)
        gl = lab("organ: different tissues", GREEN, 34).move_to([STAGE_X, 3.3, 0])
        hl = lab("heart", GREEN, 34).move_to([STAGE_X, -3.3, 0])
        self.add(strip, heart, gl, hl)
        outl = body_state()
        hp = Pt(0.25, 0.95)
        self.play(FadeOut(gl), FadeOut(hl), Create(outl),
                  tw(heart, 1.6, x=hp[0], y=hp[1], h=1.15, dop=0.0), run_time=1.6)
        self.at("fresh from")
        lg = lungs()
        paths = [[Pt(-0.75, 1.1), hp + LEFT * 0.2], [Pt(1.3, 1.1), hp + RIGHT * 0.2]]
        fl = PathFlow(paths, per=3, color=CYAN, speed=0.45, r=0.1)
        fl.on = 1
        self.play(Create(lg), run_time=0.8)
        self.add(fl)
        self.at("branching set")
        vg = vessel_group()
        flow = PathFlow([path_pts(k) for k in TREE], per=3, speed=0.14, vfun=lambda: 0.5 + 1.5 * pulse())
        self.play(LaggedStart(*[Create(v) for v in vg], lag_ratio=0.3, run_time=2.6))
        self.add(flow)
        flow.on = 1
        self.at("Organs working")
        fx = VGroup(*[v.copy().set_stroke(ORANGE, 14) for v in vg])
        self.play(ShowPassingFlash(fx, time_width=0.6), run_time=1.8)
        self.at("organ system")
        sl = lab("organ system:\nheart and\nblood vessels", ORANGE, 28).move_to([5.45, 2.2, 0])
        self.play(*strip.fill(3), FadeIn(sl, shift=LEFT * 0.1), run_time=0.8)
        self.at("are one")
        self.play(vg.animate.set_stroke(ORANGE, 9), strip.flash(3), run_time=1.0)
        self.finish()


class S11Organism(SpokenScene):
    def construct(self):
        self.add(ClockMob())
        strip = Strip(4)
        outl = body_state()
        hp = Pt(0.25, 0.95)
        ms = mesh(lo=0.2, hi=0.5)
        vg = vessel_group().set_stroke(ORANGE)
        heart = HeartOrgan((hp[0], hp[1]), 1.15, dop=0.0)
        heart.s["dop"] = 0.0
        lg = lungs()
        sl = lab("organ system:\nheart and\nblood vessels", ORANGE, 28).move_to([5.45, 2.2, 0])
        flow = PathFlow([path_pts(k) for k in TREE], per=3, speed=0.14, vfun=lambda: 0.5 + 1.5 * pulse())
        flow.on = 1
        self.add(strip, outl, lg, vg, heart, flow, sl)
        self.at("All the systems")
        self.play(outl.animate.set_stroke(GOLD, 6, opacity=1).set_fill(GOLD, 0.08), FadeIn(ms), FadeOut(sl), run_time=1.6)
        self.at("organism")
        you = lab("you", GOLD, 46).move_to([5.45, 2.2, 0])
        self.play(*strip.fill(4), FadeIn(you, scale=0.7), run_time=0.7)
        self.at("Now the oxygen")
        tc = toe_cells()
        self.play(FadeIn(tc), run_time=0.8)
        self.at("oxygen reaches")
        o2 = PathFlow([[Pt(-0.95, -3.0), Pt(-0.95, -3.3)], [Pt(0.95, -3.0), Pt(0.95, -3.3)]], per=4, color=CYAN, speed=0.5, r=0.1)
        o2.on = 1
        self.add(o2)
        self.play(tc.animate.set_fill(CYAN, 0.6).set_stroke(CYAN), run_time=1.6)
        ol = tag("oxygen", CYAN, 30).move_to([5.3, -3.2, 0])
        self.play(FadeIn(ol), run_time=0.5)
        self.at("That one job")
        for i in range(5):
            self.play(strip.flash(i, 0.45), run_time=0.45)
        self.at("from one cell")
        self.play(strip.flash(0, 0.6), run_time=0.6)
        self.play(Indicate(outl, color=GOLD, scale_factor=1.03), strip.flash(4, 0.8), run_time=0.8)
        self.finish()


class S12Nerve(SpokenScene):
    def construct(self):
        self.add(ClockMob())
        strip = Strip(5)
        r0 = RBC((-1.4, 1.2), D=1.8, dots=1.0, wob=0.4)
        h0 = HCell((3.2, 1.2), 0.45, 2.4, own=True)
        self.add(strip, r0, h0)
        self.at("A nerve cell")
        self.play(FadeOut(r0), FadeOut(h0), run_time=0.6)
        soma_c = (-3.7, 2.7)
        soma = nerve_cell(1.0, soma_c)
        self.play(FadeIn(soma), run_time=0.8)
        self.at("long branches")
        ap = [np.array(p + (0,)) for p in [(-3.7, 2.3), (-3.0, 1.2), (-1.6, 0.1), (0.4, -0.7), (2.6, -1.5), (4.4, -2.3), (5.3, -2.7)]]
        ax = VMobject().set_points_smoothly(ap).set_stroke(PURPLE, 6)
        sp = lab("spine", GREY, 28).move_to([-1.9, 3.0, 0])
        self.play(Create(ax), FadeIn(sp), run_time=1.6)
        ft = lab("foot", GREY, 28).move_to([5.7, -3.4, 0])
        tips = VGroup(*[Line(ap[-1], ap[-1] + np.array(d + (0,))).set_stroke(PURPLE, 4) for d in [(0.5, 0.2), (0.5, -0.2), (0.3, -0.5)]])
        self.play(FadeIn(tips), FadeIn(ft), run_time=0.3)
        self.at("It carries signals")
        dot = Dot(radius=0.16, color=YELLOW)
        glow = Circle(radius=0.3, stroke_width=0, fill_color=YELLOW, fill_opacity=0.35)
        pg = VGroup(glow, dot)
        lens = [np.linalg.norm(ap[i + 1] - ap[i]) for i in range(len(ap) - 1)]
        tot = sum(lens)
        axp = ax.copy()
        pg.t = 0.0

        def mv(m, dt):
            m.t += dt
            u = (m.t * 0.3) % 1.0
            m.move_to(axp.point_from_proportion(u))
        pg.add_updater(mv)
        self.add(pg)
        self.at("in some cases")
        ml = lab("in some cases about 1 meter", TEXT, 32).move_to([-1.0, -2.8, 0])
        self.play(FadeIn(ml, shift=UP * 0.1), run_time=0.7)
        self.finish()


class S13Shapes(SpokenScene):
    def construct(self):
        self.add(ClockMob())
        strip = Strip(5)
        S, E = np.array([-4.3, 0.1, 0]), np.array([0.0, -0.4, 0])
        A = np.array([-3.4, 0.9, 0])
        up = Line(S, E).set_stroke("#D8D2C4", 22)
        fore = Line(E, E + 4.0 * np.array([0.8, -0.57, 0])).set_stroke("#D8D2C4", 22)
        joint = Dot(radius=0.2, color="#8B8576").move_to(E)
        mus = VMobject(stroke_color=PURPLE, stroke_width=4, fill_color="#3A2866", fill_opacity=0.95)
        stripes = VGroup(*[Line(ORIGIN, UP) for _ in range(9)]).set_stroke("#B79CFF", 3, opacity=0.8)
        arm = VGroup(up, fore, joint, mus, stripes)

        def upd(m, dt):
            f = pulse(per=2.4)
            th = math.radians(-35 + 65 * f)
            d = np.array([math.cos(th), math.sin(th), 0])
            nrm = np.array([-d[1], d[0], 0])
            fore.put_start_and_end_on(E, E + 4.0 * d)
            F = E + 1.2 * d + 0.45 * nrm
            v = F - A
            n = np.array([-v[1], v[0], 0]) / np.linalg.norm(v)
            us = np.linspace(0, 1, 24)
            w = 0.28 * (1 + 0.25 * f)
            top = [A + v * u + n * w * math.sin(math.pi * u) ** 0.5 for u in us]
            bot = [A + v * u - n * w * math.sin(math.pi * u) ** 0.5 for u in us]
            mus.set_points_as_corners(top + bot[::-1] + [top[0]])
            for i, ln in enumerate(stripes):
                u = 0.1 + 0.8 * i / 8
                c = A + v * u
                ww = w * math.sin(math.pi * u) ** 0.5 * 0.8
                ln.put_start_and_end_on(c - n * ww, c + n * ww)
        arm.add_updater(upd)
        upd(arm, 0)
        self.add(strip)
        self.play(FadeIn(arm), run_time=1.0)
        ml = lab("arm muscle cell", PURPLE, 34).move_to([-2.0, 2.4, 0])
        self.play(FadeIn(ml, shift=DOWN * 0.1), run_time=0.5)
        self.at("It shortens")
        bl = lab("bone", "#D8D2C4", 32).move_to([4.6, -2.5, 0])
        self.play(FadeIn(bl), run_time=0.5)
        self.at("Three cells")
        self.play(FadeOut(arm), FadeOut(ml), FadeOut(bl), run_time=0.7)
        rb = RBC((-2.8, 0.7), D=2.0, dots=1.0, wob=0.4)
        nv = nerve_cell(1.0, (1.3, 2.0))
        mus2 = VMobject(stroke_color=PURPLE, stroke_width=4, fill_color="#3A2866", fill_opacity=0.95)
        st2 = VGroup(*[Line(ORIGIN, UP) for _ in range(9)]).set_stroke("#B79CFF", 3, opacity=0.8)
        mg = VGroup(mus2, st2)

        def u2(m, dt):
            f = pulse(per=2.4)
            L = 3.0 * (1 - 0.18 * f)
            w = 0.3 * (1 + 0.25 * f)
            c = np.array([5.0, 0.7, 0])
            us = np.linspace(0, 1, 24)
            top = [c + np.array([(u - 0.5) * L, w * math.sin(math.pi * u) ** 0.5, 0]) for u in us]
            bot = [c + np.array([(u - 0.5) * L, -w * math.sin(math.pi * u) ** 0.5, 0]) for u in us]
            mus2.set_points_as_corners(top + bot[::-1] + [top[0]])
            for i, ln in enumerate(st2):
                u = 0.1 + 0.8 * i / 8
                x = c[0] + (u - 0.5) * L
                ww = w * math.sin(math.pi * u) ** 0.5 * 0.8
                ln.put_start_and_end_on([x, c[1] - ww, 0], [x, c[1] + ww, 0])
        mg.add_updater(u2)
        u2(mg, 0)
        axl = nv[-2].copy()
        pg = Dot(radius=0.13, color=YELLOW)
        pg.t = 0.0
        pg.add_updater(lambda m, dt: (setattr(m, "t", m.t + dt), m.move_to(axl.point_from_proportion((m.t * 0.35) % 1.0))))
        self.play(FadeIn(rb), FadeIn(nv), FadeIn(mg), run_time=0.8)
        self.add(pg)
        t1 = lab("carries\noxygen", CYAN, 30).move_to([-2.8, -2.1, 0])
        t2 = lab("carries\nsignals", YELLOW, 30).move_to([1.3, -2.1, 0])
        t3 = lab("shortens\nto pull", PURPLE, 30).move_to([5.0, -2.1, 0])
        self.at("each fitting")
        self.play(FadeIn(t1), run_time=0.4)
        self.play(FadeIn(t2), run_time=0.4)
        self.play(FadeIn(t3), run_time=0.4)
        ns = T("not to scale", 24, GREY).move_to([5.3, -3.4, 0])
        self.play(FadeIn(ns), run_time=0.4)
        self.finish()


def rings_group():
    specs = [(4.4, 2.4, TBLUE), (6.4, 4.0, GREEN), (8.4, 5.6, ORANGE), (10.4, 7.2, GOLD)]
    return [RoundedRectangle(corner_radius=0.5, width=w, height=h, stroke_color=c, stroke_width=6, fill_color=c, fill_opacity=0.06).move_to([STAGE_X, 0, 0])
            for w, h, c in specs]


class S14Zoom(SpokenScene):
    def construct(self):
        self.add(ClockMob())
        strip = Strip(5)
        hp = Pt(0.25, 0.95)
        outl = person().set_stroke(GOLD, 6).set_fill(GOLD, 0.08)
        vg = vessel_group().set_stroke(ORANGE)
        sh = freeze(HeartOrgan((hp[0], hp[1]), 1.15, dop=0.0))
        A = VGroup(outl, vg, sh)
        B = freeze(HeartOrgan((STAGE_X, 0), 4.8))
        C = freeze(Network((STAGE_X, 0), 1.0, amp=0.0, hull=1.0))
        D = HCell((1.2, -0.0), 1.0, 2.4, own=True)
        strip.set_z_index(50)
        self.add(A, strip)
        self.play(strip.flash(4, 0.5), run_time=0.5)
        delta = np.array([STAGE_X, 0, 0]) - hp
        self.play(A.animate.scale(3.2, about_point=hp).shift(delta), strip.flash(3, 0.8), run_time=0.8)
        self.play(FadeOut(A, scale=1.4), FadeIn(B, scale=0.6), strip.flash(2, 0.6), run_time=0.6)
        self.play(FadeOut(B, scale=2.0), FadeIn(C, scale=0.5), strip.flash(1, 0.6), run_time=0.6)
        self.play(FadeOut(C, scale=2.0), FadeIn(D, scale=0.5), strip.flash(0, 0.6), run_time=0.6)
        self.at("still a cell")
        cl = lab("cell", PURPLE, 40).move_to([STAGE_X, 2.7, 0])
        self.play(FadeIn(cl, shift=DOWN * 0.1), run_time=0.6)
        self.at("sits inside")
        D.own = True
        self.play(FadeOut(cl), tw(D, 0.8, b=0.4, x=STAGE_X - 0.35, y=0.0), run_time=0.8)
        cl2 = lab("cell", PURPLE, 30).move_to([STAGE_X, -0.95, 0])
        rg = rings_group()
        self.add(cl2)
        self.play(LaggedStart(*[GrowFromCenter(r) for r in rg], lag_ratio=0.5, run_time=2.0))
        names = [("tissue", TBLUE, 0.8, "a tissue"), ("heart", GREEN, 1.6, "the heart"),
                 ("circulatory system", ORANGE, 2.4, "the circulatory system"), ("you", GOLD, 3.2, "and you")]
        for i, (nm, col, y, ph) in enumerate(names):
            self.at(ph)
            t = lab(nm, col, 30).move_to([STAGE_X, y, 0])
            self.play(FadeIn(t), Indicate(rg[i], color=col, scale_factor=1.03), strip.flash(i + 1, 0.6), run_time=0.6)
        self.finish()


class S15Labor(SpokenScene):
    def construct(self):
        self.add(ClockMob())
        strip = Strip(5)
        stair = []
        for i, (nm, col) in enumerate(LEVELS):
            x, y = -3.5 + 1.9 * i, -2.8 + 1.4 * i
            r = RoundedRectangle(corner_radius=0.12, width=2.9, height=0.9, stroke_color=col, stroke_width=5, fill_color=col, fill_opacity=0.5).move_to([x, y, 0])
            t = T(nm.replace("\n", " "), 30, TEXT, weight=BOLD).move_to(r)
            stair.append(VGroup(r, t))
        self.add(strip)
        self.play(*[ReplacementTransform(VGroup(strip.boxes[i], strip.labs[i]), stair[i]) for i in range(5)], run_time=1.4)
        up = [Arrow([-3.5 + 1.9 * i + 0.95, -2.8 + 1.4 * i + 0.45, 0], [-3.5 + 1.9 * i + 0.95, -2.8 + 1.4 * (i + 1) - 0.45, 0], buff=0,
                    color=TEXT, stroke_width=6, tip_length=0.2) for i in range(4)]
        self.play(LaggedStart(*[GrowArrow(a) for a in up], lag_ratio=0.2), run_time=0.8)
        self.at("division of labor")
        ban = lab("division\nof labor", GOLD, 54).move_to([4.5, -1.8, 0])
        self.play(FadeIn(ban, shift=DOWN * 0.15), *[s_[0].animate(rate_func=there_and_back).set_fill(LEVELS[i][1], 0.95) for i, s_ in enumerate(stair)], run_time=1.5)
        self.at("Each level")
        self.play(LaggedStart(*[Indicate(a, color=YELLOW, scale_factor=1.3) for a in up], lag_ratio=0.25), run_time=2.0)
        self.at("depend on")
        dn = [Arrow([-3.5 + 1.9 * i + 0.55, -2.8 + 1.4 * (i + 1) - 0.45, 0], [-3.5 + 1.9 * i + 0.55, -2.8 + 1.4 * i + 0.45, 0], buff=0,
                    color=GREY, stroke_width=6, tip_length=0.2) for i in range(4)]
        self.play(LaggedStart(*[GrowArrow(a) for a in dn], lag_ratio=0.15), run_time=1.0)
        self.play(*[s_[0].animate(rate_func=there_and_back).set_fill(LEVELS[i][1], 0.95) for i, s_ in enumerate(stair)], run_time=1.5)
        self.finish()


class S16End(EndCard):
    LINE = "Cells shaped for their jobs build tissues, organs, systems and you."
