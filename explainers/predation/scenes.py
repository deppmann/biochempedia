"""Two Ledgers, One Kill: the Lotka-Volterra predator-prey loop (Biochemistrypedia explainer).

Timed to the SPOKEN words: every self.at / self.until cue uses audio/words.json.

COLOUR MAP (one colour per concept, whole film; the lesson's TEAL / ORANGE lifted for the dark ground)
  TEAL   = prey (N): ledger, curve, threshold P*
  ORANGE = predators (P): ledger, curve, threshold N*
  TEXT   = the dot, its orbit trail and labels      GOLD = the equilibrium diamond
  GREY   = frames and neutral arrows                RED  = 'no built-in delay'
Every curve and orbit is computed from dN/dt = N(r - aP), dP/dt = P(eaN - m) with the
lesson's numbers r = 1, a = 0.01, e = 0.1, m = 0.5 (so P* = 100, N* = 500).
"""
import numpy as np
from bp_style import *  # noqa: F401,F403

ORANGE = "#F29E4C"
R_, A_, E_, M_ = 1.0, 0.01, 0.1, 0.5
NS, PS = M_ / (E_ * A_), R_ / A_          # N* = 500, P* = 100
NMAX, PMAX = 1400.0, 220.0

# ---------------------------------------------------------------- the phase plane (one layout per scene)
LAY = dict(x0=-5.6, y0=-2.95, w=6.0, h=6.0)


def set_layout(x0, y0, w, h):
    LAY.update(x0=x0, y0=y0, w=w, h=h)


def px(N):
    return LAY["x0"] + LAY["w"] * np.asarray(N) / NMAX


def py(P):
    return LAY["y0"] + LAY["h"] * np.asarray(P) / PMAX


def pxy(N, P):
    return np.array([float(px(N)), float(py(P)), 0.0])


# ---------------------------------------------------------------- computed orbits
def _f(s):
    return np.array([s[0] * (R_ - A_ * s[1]), s[1] * (E_ * A_ * s[0] - M_)])


class Loop:
    """One closed Lotka-Volterra orbit, computed (RK4) from a start (N0, P0)."""

    def __init__(self, N0, P0, dt=0.01):
        s = np.array([N0, P0], float)
        pts, t = [s.copy()], 0.0
        while t < 40:
            k1 = _f(s); k2 = _f(s + dt / 2 * k1); k3 = _f(s + dt / 2 * k2); k4 = _f(s + dt * k3)
            sn = s + dt / 6 * (k1 + 2 * k2 + 2 * k3 + k4)
            t += dt
            if t > 1.0 and s[0] < N0 <= sn[0]:
                fr = (N0 - s[0]) / (sn[0] - s[0])
                pts.append(s + fr * (sn - s))
                t = t - dt + fr * dt
                break
            pts.append(sn.copy()); s = sn
        pts[-1] = pts[0].copy()
        self.arr = np.array(pts)
        self.T = t
        self.n = len(pts)
        self.i_prey = int(self.arr[:, 0].argmax())      # prey peak (P crosses P* going up)
        self.i_pred = int(self.arr[:, 1].argmax())      # predator peak (N crosses N* going down)
        self.u_prey = self.i_prey / (self.n - 1)
        self.u_pred = self.i_pred / (self.n - 1)

    def val(self, u):
        """(N, P) at fraction u of one period; u wraps."""
        f = (u % 1.0) * (self.n - 1)
        i = int(f); i2 = min(i + 1, self.n - 1); fr = f - i
        return self.arr[i] * (1 - fr) + self.arr[i2] * fr

    def scr(self, u):
        N, P = self.val(u)
        return pxy(N, P)

    def screen_pts(self, u, step=4):
        u = min(max(u, 0.0), 1.0)
        k = int(u * (self.n - 1))
        idx = list(range(0, k + 1, step))
        N = self.arr[idx, 0]; P = self.arr[idx, 1]
        pts = [np.array([float(px(a)), float(py(b)), 0.0]) for a, b in zip(N, P)]
        pts.append(self.scr(u))
        return pts


MAIN = Loop(900, 60)
SMALL = Loop(600, 85)
BIG = Loop(1100, 55)


def corner_line(pts, color, w, op=1.0):
    if len(pts) < 2:
        return VMobject()
    m = VMobject().set_points_as_corners(pts)
    m.set_stroke(color, w, opacity=op)
    m.set_fill(opacity=0)
    return m


def trail(loop, tr, color=TEXT, w=7, op=0.95):
    return always_redraw(lambda: corner_line(loop.screen_pts(tr.get_value()), color, w, op))


def dot_at(loop, tr, color=TEXT, r=0.22):
    return always_redraw(lambda: Dot(loop.scr(tr.get_value()), radius=r, color=color).set_z_index(6))


# ---------------------------------------------------------------- plane pieces
def plane_axes(xlabel=True, ylabel=True, size=30):
    x0, y0, w, h = LAY["x0"], LAY["y0"], LAY["w"], LAY["h"]
    xa = Arrow([x0, y0, 0], [x0 + w + 0.25, y0, 0], buff=0, color=GREY, stroke_width=6, tip_length=0.25)
    ya = Arrow([x0, y0, 0], [x0, y0 + h + 0.25, 0], buff=0, color=GREY, stroke_width=6, tip_length=0.25)
    g = VGroup(xa, ya)
    if xlabel:
        g.add(T("prey, N", size, TEAL).move_to([x0 + w - 0.55, y0 - 0.4, 0]))
    if ylabel:
        g.add(T("predators, P", size, ORANGE).move_to([x0 + 1.15, y0 + h + 0.42, 0]))
    return g


def pstar_line():
    return DashedLine(pxy(0, PS), pxy(NMAX, PS), color=TEAL, stroke_width=7, dash_length=0.2)


def nstar_line():
    return DashedLine(pxy(NS, 0), pxy(NS, PMAX), color=ORANGE, stroke_width=7, dash_length=0.2)


def diamond():
    return Square(side_length=0.3, stroke_color=GOLD, stroke_width=3, fill_color=GOLD, fill_opacity=0.9).rotate(PI / 4).move_to(pxy(NS, PS)).set_z_index(5)


ZONES = {   # name: (N range, P range, sx, sy): prey direction sx, predator direction sy
    "br": ((NS, NMAX), (0, PS), +1, +1),
    "tr": ((NS, NMAX), (PS, PMAX), -1, +1),
    "tl": ((0, NS), (PS, PMAX), -1, -1),
    "bl": ((0, NS), (0, PS), +1, -1),
}


def zone_rect(z):
    (n0, n1), (p0, p1), _, _ = ZONES[z]
    a, b = pxy(n0, p0), pxy(n1, p1)
    return Rectangle(width=b[0] - a[0], height=b[1] - a[1], stroke_width=0, fill_color=GREY, fill_opacity=0.22).move_to((a + b) / 2)


def zone_arrow(z):
    (n0, n1), (p0, p1), sx, sy = ZONES[z]
    c = pxy((n0 + n1) / 2, (p0 + p1) / 2) + np.array([0.0, -0.0, 0.0])
    # keep arrows out of the orbit's busiest parts: nudge toward the corner away from the diamond
    c = c + np.array([0.45 * sx, 0.5 * sy, 0.0]) * 0.0
    return Arrow(c - np.array([0.62 * sx, 0.55 * sy, 0.0]), c + np.array([0.62 * sx, 0.55 * sy, 0.0]), buff=0,
                 color=TEXT, stroke_width=7, tip_length=0.26).set_opacity(0.9)


def direction_card(z, origin=np.array([3.9, -0.9, 0.0])):
    """Right-panel composition of the two directions in zone z (prey across, predators up)."""
    _, _, sx, sy = ZONES[z]
    a = Arrow(origin, origin + [2.3 * sx, 0, 0], buff=0, color=TEAL, stroke_width=9, tip_length=0.34)
    b = Arrow(origin, origin + [0, 1.9 * sy, 0], buff=0, color=ORANGE, stroke_width=9, tip_length=0.34)
    c = Arrow(origin, origin + [2.3 * sx, 1.9 * sy, 0], buff=0, color=TEXT, stroke_width=11, tip_length=0.38)
    return VGroup(a, b, c)


def direction_words(z):
    _, _, sx, sy = ZONES[z]
    t1 = T("prey increase" if sx > 0 else "prey decrease", 38, TEAL).move_to([3.9, 3.15, 0])
    t2 = T("predators increase" if sy > 0 else "predators decrease", 38, ORANGE).move_to([3.9, 2.45, 0])
    return VGroup(t1, t2)


# ---------------------------------------------------------------- time-series strip (right panel)
SX0, SY0, SW, SH = 1.45, -0.7, 5.1, 3.5


def sxx(i, n):
    return SX0 + SW * i / (n - 1)


def sN(N):
    return SY0 + SH * N / 1250.0


def sP(P):
    return SY0 + SH * P / 210.0


def strip_axes():
    xa = Arrow([SX0, SY0, 0], [SX0 + SW + 0.25, SY0, 0], buff=0, color=GREY, stroke_width=4, tip_length=0.2)
    ya = Arrow([SX0, SY0, 0], [SX0, SY0 + SH + 0.25, 0], buff=0, color=GREY, stroke_width=4, tip_length=0.2)
    tl = T("time", 28, TEXT).move_to([SX0 + SW - 0.4, SY0 - 0.4, 0])
    nl = T("numbers", 28, TEXT).rotate(PI / 2).move_to([SX0 - 0.42, SY0 + SH / 2, 0])
    return VGroup(xa, ya, tl, nl)


def legend():
    return VGroup(T("prey", 28, TEAL).move_to([2.0, -1.3, 0]), T("predators", 28, ORANGE).move_to([3.7, -1.3, 0]))


def strip_curve(loop, tr, key, color, w=7):
    def mk():
        u = min(max(tr.get_value(), 0.0), 1.0)
        k = int(u * (loop.n - 1))
        idx = list(range(0, k + 1, 3)) + [k]
        if key == "N":
            pts = [np.array([sxx(i, loop.n), sN(loop.arr[i, 0]), 0.0]) for i in idx]
        else:
            pts = [np.array([sxx(i, loop.n), sP(loop.arr[i, 1]), 0.0]) for i in idx]
        return corner_line(pts, color, w)
    return always_redraw(mk)


def now_line(loop, tr):
    return always_redraw(lambda: DashedLine([sxx(min(tr.get_value(), 1.0) * (loop.n - 1), loop.n), SY0, 0],
                                            [sxx(min(tr.get_value(), 1.0) * (loop.n - 1), loop.n), SY0 + SH, 0],
                                            color=TEXT, stroke_width=3, dash_length=0.12).set_opacity(0.7))


# ---------------------------------------------------------------- animals (cartoons)
def hare(k=1.0, color=TEAL):
    body = Ellipse(width=1.15, height=0.72, stroke_color=color, stroke_width=3, fill_color=color, fill_opacity=0.9)
    head = Circle(radius=0.28, stroke_color=color, stroke_width=3, fill_color=color, fill_opacity=0.9).move_to([0.62, 0.22, 0])
    ears = VGroup(*[Ellipse(width=0.16, height=0.62, stroke_color=color, stroke_width=3, fill_color=color, fill_opacity=0.9)
                    .rotate(a).move_to([0.5 + dx, 0.78, 0]) for a, dx in [(0.15, 0.0), (-0.1, 0.2)]])
    tail = Circle(radius=0.12, stroke_color=TEXT, stroke_width=2, fill_color=TEXT, fill_opacity=0.9).move_to([-0.6, 0.12, 0])
    eye = Dot([0.7, 0.28, 0], radius=0.04, color=BG)
    return VGroup(ears, body, head, tail, eye).scale(k)


def fox(k=1.0, color=ORANGE):
    body = Ellipse(width=1.6, height=0.8, stroke_color=color, stroke_width=3, fill_color=color, fill_opacity=0.9)
    head = Circle(radius=0.38, stroke_color=color, stroke_width=3, fill_color=color, fill_opacity=0.9).move_to([-0.9, 0.28, 0])
    snout = Triangle(stroke_color=color, stroke_width=3, fill_color=color, fill_opacity=0.9).scale(0.2).rotate(PI / 2).move_to([-1.35, 0.2, 0])
    ears = VGroup(*[Triangle(stroke_color=color, stroke_width=3, fill_color=color, fill_opacity=0.9).scale(0.16).move_to([-0.95 + dx, 0.7, 0])
                    for dx in (0.0, 0.25)])
    tail = Ellipse(width=0.95, height=0.36, stroke_color=color, stroke_width=3, fill_color=color, fill_opacity=0.9).rotate(0.5).move_to([1.2, 0.35, 0])
    tip = Circle(radius=0.12, stroke_color=TEXT, stroke_width=2, fill_color=TEXT, fill_opacity=0.9).move_to([1.55, 0.5, 0])
    eye = Dot([-1.02, 0.34, 0], radius=0.045, color=BG)
    return VGroup(tail, tip, ears, body, head, snout, eye).scale(k)


# ---------------------------------------------------------------- ledgers
class Ledger:
    def __init__(self, color, name, cx, cy=0.3, w=4.0, h=4.6, side=-1, bar=True, bar_v=0.5, rows=6):
        self.color, self.cx, self.cy, self.w, self.h, self.rows = color, cx, cy, w, h, rows
        top = cy + h / 2
        self.top = top
        box = RoundedRectangle(corner_radius=0.15, width=w, height=h, stroke_color=color, stroke_width=4,
                               fill_color=color, fill_opacity=0.22).move_to([cx, cy, 0])
        div = Line([cx, top - 0.75, 0], [cx, cy - h / 2 + 0.2, 0], color=color, stroke_width=2).set_opacity(0.6)
        rule = Line([cx - w / 2 + 0.15, top - 0.72, 0], [cx + w / 2 - 0.15, top - 0.72, 0], color=color, stroke_width=2).set_opacity(0.6)
        self.title = T(name, 32, color, weight=BOLD).move_to([cx, top - 0.38, 0])
        self.h_b = T("births", 28, TEXT).move_to([cx - w / 4, top - 1.05, 0])
        self.h_d = T("deaths", 28, TEXT).move_to([cx + w / 4, top - 1.05, 0])
        self.base = VGroup(box, div, rule, self.title, self.h_b, self.h_d)
        self.births, self.deaths = [], []
        self.bar_tr = ValueTracker(bar_v)
        self.bar = None
        if bar:
            bx = cx + side * (w / 2 + 0.38)
            by0 = cy - 1.8
            outline = Rectangle(width=0.3, height=3.6, stroke_color=color, stroke_width=3).move_to([bx, by0 + 1.8, 0])
            fill = always_redraw(lambda: Rectangle(width=0.3, height=max(0.02, self.bar_tr.get_value() * 3.6), stroke_width=0,
                                                   fill_color=color, fill_opacity=0.85).move_to([bx, by0 + max(0.02, self.bar_tr.get_value() * 3.6) / 2, 0]))
            self.base.add(outline)
            self.bar = fill
        self.pop = None

    def slot(self, kind, i):
        x = self.cx - self.w / 4 if kind == "b" else self.cx + self.w / 4
        return np.array([x, self.top - 1.7 - 0.5 * i, 0.0])

    def entry(self, kind, i):
        sign = "+" if kind == "b" else "−"
        return T(sign, 48, self.color, weight=BOLD).move_to(self.slot(kind, i))

    def fill_static(self, nb, nd):
        for i in range(nb):
            self.births.append(self.entry("b", i))
        for i in range(nd):
            self.deaths.append(self.entry("d", i))
        return VGroup(*self.births, *self.deaths)

    def mobs(self):
        g = VGroup(self.base, *self.births, *self.deaths)
        return g


def chain(x1, x2, y, c1=TEAL, c2=ORANGE, n=9):
    links = VGroup()
    for i in range(n):
        f = i / (n - 1)
        col = interpolate_color(ManimColor(c1), ManimColor(c2), f)
        x = x1 + (x2 - x1) * f
        if i % 2 == 0:
            m = Ellipse(width=0.56, height=0.3, stroke_color=col, stroke_width=5)
        else:
            m = Ellipse(width=0.3, height=0.3, stroke_color=col, stroke_width=5)
        links.add(m.move_to([x, y, 0]))
    return links


class Base(SpokenScene):
    def until(self, phrase, lead=0.2, nth=0, lo=0.3):
        """Seconds from now to just before the narrator says `phrase` (run_time that keeps the picture moving)."""
        return max(lo, self.t_of(phrase, nth) - lead - self.elapsed())

    def to(self, phrase, *anims, lead=0.2, nth=0, lo=0.3, **kw):
        self.play(*anims, run_time=self.until(phrase, lead, nth, lo), **kw)


LX, RX, LY = -3.9, 3.9, 0.3


def two_ledgers(pb=(3, 2), pr=(2, 2), vp=0.62, vr=0.42):
    L = Ledger(TEAL, "prey ledger", LX, LY, side=-1, bar_v=vp)
    Rr = Ledger(ORANGE, "predator ledger", RX, LY, side=+1, bar_v=vr)
    L.fill_static(*pb)
    Rr.fill_static(*pr)
    return L, Rr


def panel(x, y, w, h, op=0.2):
    return RoundedRectangle(corner_radius=0.2, width=w, height=h, stroke_width=0, fill_color=GREY, fill_opacity=op).move_to([x, y, 0]).set_z_index(-5)


def plane_panel():
    return panel(-2.75, 0.0, 7.1, 7.5)


def bob(m, amp=0.18, speed=3.2, phase=0.0):
    """Make an animal hop: a continuous idle motion (time-based updater)."""
    st = [0.0]

    def upd(mm, dt):
        old = amp * abs(np.sin(speed * st[0] + phase))
        st[0] += dt
        mm.shift(UP * (amp * abs(np.sin(speed * st[0] + phase)) - old))
    m.add_updater(upd)
    return m


class Flow(VGroup):
    """A few dots drifting through one zone of the plane in that zone's direction (a picture of the arrow)."""

    def __init__(self, z, n=5):
        super().__init__()
        (n0, n1), (p0, p1), self.sx, self.sy = ZONES[z]
        self.a, self.b = pxy(n0, p0), pxy(n1, p1)
        self.t = 0.0
        for i in range(n):
            self.add(Dot(radius=0.09, color=TEXT).set_opacity(0.9))
        self._place()
        self.add_updater(lambda m, dt: m._step(dt))

    def _place(self):
        for i, d in enumerate(self.submobjects):
            bx, by = (0.13 + 0.37 * i) % 1.0, (0.21 + 0.61 * i) % 1.0
            fx = (bx + self.sx * 0.11 * self.t) % 1.0
            fy = (by + self.sy * 0.14 * self.t) % 1.0
            d.move_to([self.a[0] + 0.1 + (self.b[0] - self.a[0] - 0.2) * fx, self.a[1] + 0.1 + (self.b[1] - self.a[1] - 0.2) * fy, 0])

    def _step(self, dt):
        self.t += dt
        self._place()


def spin_on(scene, tracker, rate):
    """Keep a tracker running forever (a continuous clock for idle motion)."""
    tracker.add_updater(lambda m, dt: m.increment_value(dt * rate))
    scene.add(tracker)


def u_at_N(loop, target):
    """Orbit fraction where the prey number first falls to `target` after the prey peak."""
    for i in range(loop.i_prey, loop.i_pred + 1):
        if loop.arr[i, 0] <= target:
            return i / (loop.n - 1)
    return loop.u_pred


# ============================================================================================= scenes
class S00Title(TitleCard):
    LESSON = "Predation and Community Effects"
    TITLE = "Two Ledgers, One Kill"


class S01Question(Base):
    def construct(self):
        loop = MAIN
        W0, W1 = 0.8, 1.8        # a window of the computed cycle: u from 0.8 to 1.8
        x0, x1, y0, y1 = -5.9, 6.0, -2.7, 2.9
        self.add(panel(0.0, 0.1, 13.2, 7.0, 0.16))
        xa = Arrow([x0, y0, 0], [x1 + 0.3, y0, 0], buff=0, color=GREY, stroke_width=6, tip_length=0.25)
        ya = Arrow([x0, y0, 0], [x0, y1 + 0.3, 0], buff=0, color=GREY, stroke_width=6, tip_length=0.25)
        tl = T("time", 30, TEXT).move_to([x1 - 0.4, y0 - 0.4, 0])
        nl = T("numbers", 30, TEXT).rotate(PI / 2).move_to([x0 - 0.45, 0.1, 0])
        cmp_ = T("computed", 26, TEXT).move_to([-4.7, y0 - 0.4, 0])
        tr = ValueTracker(0.0)

        def xy(key, q):
            N, P = loop.val(W0 + q * (W1 - W0))
            return np.array([x0 + (x1 - x0) * q, y0 + (y1 - y0) * (N / 1250.0 if key == "N" else P / 210.0), 0.0])

        def curve(key, color):
            def mk():
                a = tr.get_value()
                if a < 0.01:
                    return VMobject()
                pts = [xy(key, q) for q in np.linspace(0, a, int(220 * a) + 2)]
                return corner_line(pts, color, 8)
            return always_redraw(mk)

        cN, cP = curve("N", TEAL), curve("P", ORANGE)
        sc = ValueTracker(0.0)
        spin_on(self, sc, 0.2)

        def head(key, color):
            def mk():
                a = tr.get_value()
                q = a if a < 0.999 else (sc.get_value() % 1.0)
                return Dot(xy(key, max(q, 0.0)), radius=0.17, color=color).set_z_index(6)
            return always_redraw(mk)

        hN, hP = head("N", TEAL), head("P", ORANGE)
        qN = (loop.u_prey + 1 - W0) / (W1 - W0)
        qP = (loop.u_pred + 1 - W0) / (W1 - W0)
        pN, pP = xy("N", qN), xy("P", qP)
        self.add(xa, ya, tl, nl, cmp_)
        self.wait(0.3)
        self.add(cN, cP, hN, hP)
        self.play(tr.animate.set_value(qP + 0.08), run_time=self.until("why", lead=0.0) + 1.2, rate_func=linear)
        lab_n = T("prey", 34, TEAL).move_to([pN[0] - 1.0, pN[1] + 0.1, 0])
        lab_p = T("predators", 34, ORANGE).move_to([pP[0] + 1.6, pP[1] + 0.1, 0])
        self.play(FadeIn(lab_n), FadeIn(lab_p), run_time=0.5)
        gap = Line([pN[0], pP[1] + 0.6, 0], [pP[0], pP[1] + 0.6, 0], color=TEXT, stroke_width=5)
        ticks = VGroup(Line([pN[0], pP[1] + 0.42, 0], [pN[0], pP[1] + 0.78, 0], color=TEXT, stroke_width=5),
                       Line([pP[0], pP[1] + 0.42, 0], [pP[0], pP[1] + 0.78, 0], color=TEXT, stroke_width=5))
        qm = T("?", 80, GOLD, weight=BOLD).move_to([(pN[0] + pP[0]) / 2, pP[1] + 1.35, 0])
        self.to("after the prey", tr.animate.set_value(qP + 0.2), rate_func=linear)
        self.play(Create(gap), FadeIn(ticks), FadeIn(qm, scale=0.6), run_time=0.7)
        self.to("The answer is", tr.animate.set_value(1.0), rate_func=linear)
        self.play(qm.animate.scale(1.25), run_time=0.5)
        self.play(qm.animate.scale(0.8), run_time=0.5)
        self.finish()


class S02Ledgers(Base):
    def construct(self):
        L = Ledger(TEAL, "ledger", LX, LY, side=-1, bar_v=0.5)
        Rr = Ledger(ORANGE, "predator ledger", RX, LY, side=+1, bar_v=0.4)
        hr = bob(hare(0.72).move_to([LX, 3.12, 0]), 0.08, 7.0, 0.0)
        fx_ = bob(fox(0.8).move_to([RX, 2.95, 0]), 0.14, 6.0, 1.0)
        self.play(FadeIn(L.base, shift=UP * 0.2), FadeIn(hr), run_time=0.8)
        self.add(L.bar)
        self.wait(0.3)
        self.at("births and deaths")
        self.play(Indicate(L.h_b, color=TEAL, scale_factor=1.2), run_time=0.6)
        self.play(Indicate(L.h_d, color=TEAL, scale_factor=1.2), run_time=0.6)
        self.at("Births push")
        for i in range(3):
            e = L.entry("b", i)
            L.births.append(e)
            self.play(FadeIn(e, scale=1.6), L.bar_tr.animate.increment_value(0.075), run_time=0.45)
            self.wait(0.1)
        self.at("deaths pull")
        for i in range(2):
            e = L.entry("d", i)
            L.deaths.append(e)
            self.play(FadeIn(e, scale=1.6), L.bar_tr.animate.increment_value(-0.06), run_time=0.45)
            self.wait(0.1)
        self.at("Here are")
        self.play(FadeIn(Rr.base, shift=UP * 0.2), FadeIn(fx_), run_time=0.8)
        self.add(Rr.bar)
        self.play(Transform(L.title, T("prey ledger", 32, TEAL, weight=BOLD).move_to(L.title)), run_time=0.4)
        self.at("one for prey")
        e = Rr.entry("b", 0)
        Rr.births.append(e)
        self.play(Indicate(L.title, color=TEAL, scale_factor=1.2), FadeIn(e, scale=1.6), Rr.bar_tr.animate.increment_value(0.04), run_time=0.7)
        e = Rr.entry("b", 1)
        Rr.births.append(e)
        self.play(FadeIn(e, scale=1.6), Rr.bar_tr.animate.increment_value(0.04), run_time=0.45)
        self.at("one for predators")
        e = Rr.entry("d", 0)
        Rr.deaths.append(e)
        self.play(Indicate(Rr.title, color=ORANGE, scale_factor=1.2), FadeIn(e, scale=1.6), Rr.bar_tr.animate.increment_value(-0.04), run_time=0.7)
        e = Rr.entry("d", 1)
        Rr.deaths.append(e)
        self.play(FadeIn(e, scale=1.6), Rr.bar_tr.animate.increment_value(-0.04), run_time=0.45)
        self.finish()


class S03Kill(Base):
    def construct(self):
        L, Rr = two_ledgers((3, 2), (2, 2))
        self.add(L.mobs(), Rr.mobs(), L.bar, Rr.bar)
        tray = Polygon([-0.95, -0.55, 0], [0.95, -0.55, 0], [0.7, -1.05, 0], [-0.7, -1.05, 0], stroke_color=GOLD, stroke_width=5,
                       fill_color=GOLD, fill_opacity=0.3)
        tlab = T("food", 32, GOLD).next_to(tray, DOWN, buff=0.15)
        f = bob(fox(0.9).move_to([0.45, 1.5, 0]), 0.06, 2.4)
        self.play(FadeIn(f, shift=LEFT * 0.3), FadeIn(tray), FadeIn(tlab), run_time=0.8)
        tokens = []
        mouth = lambda: f[4].get_center() + LEFT * 0.45

        def kill(slot, n_tok):
            h = hare(1.0).move_to([-1.25, 0.3, 0])
            self.add(h)
            self.play(h.animate.move_to([-1.0, 1.55, 0]), run_time=0.6, rate_func=smooth)
            self.play(h.animate.scale(0.2).move_to(mouth()), FadeOut(h), run_time=0.3)
            mark = T("−", 48, TEAL, weight=BOLD).move_to(mouth())
            self.add(mark)
            self.play(mark.animate.move_to(L.slot("d", slot)), L.bar_tr.animate.increment_value(-0.05), run_time=0.6, path_arc=0.5)
            L.deaths.append(mark)
            tok = Circle(radius=0.19, stroke_color=TEAL, stroke_width=3, fill_color=TEAL, fill_opacity=0.9).move_to(mouth())
            self.play(tok.animate.move_to([-0.5 + 0.5 * n_tok, -0.78, 0]), run_time=0.45, rate_func=rush_into)
            tokens.append(tok)

        kill(2, 0)
        self.at("Each is a death")
        kill(3, 1)
        self.at("Each is also food")
        kill(4, 2)
        self.at("predators turn that food")
        plus = T("+", 48, ORANGE, weight=BOLD).move_to([0.0, -0.78, 0])
        self.add(plus)
        self.play(plus.animate.move_to(Rr.slot("b", 2)), Rr.bar_tr.animate.increment_value(0.06), run_time=1.0, path_arc=-0.5)
        Rr.births.append(plus)
        tag = T("e: average new predators\nper prey eaten (a rate,\nnot one kill per birth)", 26, ORANGE).move_to([RX, -2.9, 0])
        self.play(FadeIn(tag), run_time=0.7)
        self.at("So every kill")
        stamp = T("entered twice", 44, GOLD, weight=BOLD)
        box = SurroundingRectangle(stamp, color=GOLD, buff=0.2, corner_radius=0.1, stroke_width=6)
        st = VGroup(box, stamp).rotate(-0.06).move_to([0, 3.3, 0])
        self.play(FadeIn(st, scale=1.5), run_time=0.6)
        a1 = Arrow([-2.5, 3.15, 0], [-3.3, 2.78, 0], buff=0.05, color=GOLD, stroke_width=6)
        a2 = Arrow([2.5, 3.15, 0], [3.3, 2.78, 0], buff=0.05, color=GOLD, stroke_width=6)
        self.play(GrowArrow(a1), GrowArrow(a2), run_time=0.7)
        self.play(Indicate(L.deaths[-1], color=GOLD), Indicate(Rr.births[-1], color=GOLD), run_time=1.0)
        self.finish()


class S04Coupled(Base):
    def construct(self):
        L, Rr = two_ledgers((3, 0), (0, 2), vp=0.5, vr=0.35)
        pv, nv = ValueTracker(0.0), ValueTracker(0.0)
        d_slots = [L.entry("d", i) for i in range(6)]
        b_slots = [Rr.entry("b", i) for i in range(6)]
        for i, s in enumerate(d_slots):
            s.add_updater(lambda m, dt, i=i: m.set_opacity(float(np.clip(1.0 + 5.0 * pv.get_value() - i, 0, 1))))
        for i, s in enumerate(b_slots):
            s.add_updater(lambda m, dt, i=i: m.set_opacity(float(np.clip(1.0 + 5.0 * nv.get_value() - i, 0, 1))))
        hr = bob(hare(0.72).move_to([LX, 3.12, 0]), 0.08, 7.0, 0.0)
        fx_ = bob(fox(0.8).move_to([RX, 2.95, 0]), 0.14, 6.0, 1.0)
        self.add(L.mobs(), Rr.mobs(), L.bar, Rr.bar, *d_slots, *b_slots, hr, fx_)
        ch = chain(-1.95, 1.95, -1.2)
        self.at("That double entry")
        self.play(LaggedStart(*[FadeIn(c, scale=0.5) for c in ch], lag_ratio=0.15), run_time=1.8)
        trk = ValueTracker(0.0)
        spin_on(self, trk, 0.35)
        tk = always_redraw(lambda: Dot([-1.95 + 3.9 * (trk.get_value() % 1.0), -1.2, 0], radius=0.14, color=TEXT).set_z_index(5))
        self.add(tk)

        def slider(x, color, name):
            track = Line([x, -0.4, 0], [x, 2.2, 0], color=GREY, stroke_width=8)
            lab = T(name, 42, color, weight=BOLD).move_to([x, 2.7, 0])
            return track, lab
        trP, lbP = slider(-0.75, ORANGE, "P")
        trN, lbN = slider(0.75, TEAL, "N")
        knobP = always_redraw(lambda: Dot([-0.75, -0.4 + 2.6 * pv.get_value(), 0], radius=0.24, color=ORANGE).set_z_index(5))
        knobN = always_redraw(lambda: Dot([0.75, -0.4 + 2.6 * nv.get_value(), 0], radius=0.24, color=TEAL).set_z_index(5))
        self.at("The more predators")
        self.play(FadeIn(trP), FadeIn(lbP), FadeIn(knobP), run_time=0.6)
        fP = T("per prey: r − aP", 32, TEAL).move_to([LX, -2.75, 0])
        self.to("faster each prey", pv.animate.set_value(0.95), rate_func=smooth, lo=1.0)
        self.play(L.bar_tr.animate.set_value(0.28), FadeIn(fP), run_time=1.2)
        self.at("The more prey")
        self.play(FadeIn(trN), FadeIn(lbN), FadeIn(knobN), run_time=0.6)
        fN = T("per predator:\neaN − m", 32, ORANGE).move_to([RX, -2.75, 0])
        self.to("faster predators", nv.animate.set_value(0.95), rate_func=smooth, lo=1.0)
        self.play(Rr.bar_tr.animate.set_value(0.7), FadeIn(fN), run_time=1.2)
        self.play(pv.animate.set_value(0.4), nv.animate.set_value(0.4), run_time=1.0)
        self.finish()


def balance(tr, hb, cx=3.9, cy=1.0):
    """The scale of s05, a function of the predator number P (tracker `tr`) and the birth weight (`hb`, 0..1)."""
    HB = 0.9   # block height that equals the fixed birth rate; the risk block is HB * P / P*

    def mk():
        p = tr.get_value()
        hl = max(0.0, HB * hb.get_value())
        hd = max(0.0, HB * p / PS)
        th = float(np.clip((hd - hl) / HB * 0.28, -0.4, 0.4))
        Lh = 1.9
        rl = np.array([cx + Lh * np.cos(th), cy - Lh * np.sin(th), 0.0])
        ll = np.array([cx - Lh * np.cos(th), cy + Lh * np.sin(th), 0.0])
        beam = Line(ll, rl, color=TEXT, stroke_width=10)
        post = Line([cx, cy, 0], [cx, cy - 3.3, 0], color=GREY, stroke_width=10)
        base = Line([cx - 0.9, cy - 3.3, 0], [cx + 0.9, cy - 3.3, 0], color=GREY, stroke_width=12)
        piv = Dot([cx, cy, 0], radius=0.17, color=TEXT)
        parts = [post, base, beam, piv]
        for end, col, hh in ((ll, TEAL, hl), (rl, ORANGE, hd)):
            pan_c = end + np.array([0, -1.5, 0])
            pan = Line(pan_c + [-0.9, 0, 0], pan_c + [0.9, 0, 0], color=TEXT, stroke_width=10)
            s1 = Line(end, pan_c + [-0.9, 0, 0], color=TEXT, stroke_width=3)
            s2 = Line(end, pan_c + [0.9, 0, 0], color=TEXT, stroke_width=3)
            parts += [s1, s2, pan]
            if hh > 0.03:
                blk = Rectangle(width=1.2, height=hh, stroke_color=col, stroke_width=3, fill_color=col, fill_opacity=0.9)
                blk.move_to(pan_c + [0, 0.05 + hh / 2, 0])
                parts.append(blk)
        parts.append(T("births", 34, TEAL).move_to(ll + [0, -2.15, 0]))
        parts.append(T("death risk", 34, ORANGE).move_to(rl + [-0.3, -2.15, 0]))
        return VGroup(*parts)
    return always_redraw(mk)


class S05PreyLine(Base):
    def construct(self):
        set_layout(-5.6, -2.95, 6.0, 6.0)
        self.add(plane_panel())
        ax = plane_axes()
        self.add(ax)
        p, hb = ValueTracker(0.0), ValueTracker(0.0)
        scale = balance(p, hb)
        marker = always_redraw(lambda: VGroup(
            Dot(pxy(0, p.get_value()), radius=0.2, color=ORANGE).set_z_index(6),
            Line(pxy(0, p.get_value()), pxy(NMAX * 0.07, p.get_value()), color=ORANGE, stroke_width=6)))
        self.play(FadeIn(scale), FadeIn(marker), run_time=0.9)
        self.wait(0.3)
        self.at("Each prey's birth rate")
        self.play(hb.animate.set_value(1.0), run_time=1.0, rate_func=smooth)
        self.at("stays fixed")
        hl = Rectangle(width=1.5, height=1.2, stroke_color=GOLD, stroke_width=6).move_to([3.9 - 1.9 * np.cos(0.28 * 1.0) + 0.0, 1.0 + 1.9 * np.sin(0.28) - 1.5 + 0.55, 0])
        self.play(Create(hl), run_time=0.6)
        self.play(FadeOut(hl), run_time=0.5)
        self.at("risk of death")
        self.to("At one predator number", p.animate.set_value(PS), rate_func=smooth, lo=1.5)
        self.wait(0.2)
        line = pstar_line()
        lab1 = T("P* = r/a", 38, TEAL, weight=BOLD)
        lab2 = T("prey stop changing", 30, TEAL)
        lab = VGroup(lab1, lab2).arrange(DOWN, aligned_edge=RIGHT, buff=0.1).move_to([-1.75, py(PS) + 0.9, 0])
        self.play(Create(line), run_time=1.0)
        self.at("the two balance")
        self.play(FadeIn(lab), run_time=0.6)
        up = Arrow(pxy(300, 40), pxy(850, 40), buff=0, color=TEAL, stroke_width=8, tip_length=0.3)
        upl = T("prey increase", 30, TEAL).next_to(up, DOWN, buff=0.15)
        dn = Arrow(pxy(850, 190), pxy(300, 190), buff=0, color=TEAL, stroke_width=8, tip_length=0.3)
        dnl = T("prey decrease", 30, TEAL).next_to(dn, UP, buff=0.15)
        self.play(GrowArrow(up), FadeIn(upl), GrowArrow(dn), FadeIn(dnl), run_time=1.0)
        self.finish()


class S06PredLine(Base):
    def construct(self):
        set_layout(-5.6, -2.95, 6.0, 6.0)
        self.add(plane_panel())
        ax = plane_axes()
        self.add(ax)
        n = ValueTracker(0.0)
        marker = always_redraw(lambda: VGroup(
            Dot(pxy(n.get_value(), 0), radius=0.2, color=TEAL).set_z_index(6),
            Line(pxy(n.get_value(), 0), pxy(n.get_value(), PMAX * 0.07), color=TEAL, stroke_width=6)))
        f = bob(fox(1.25).move_to([3.9, 2.55, 0]), 0.07, 2.6)
        gx0, gw, gy, gh = 1.5, 4.8, 0.55, 1.2
        frame = Rectangle(width=gw, height=gh, stroke_color=ORANGE, stroke_width=6).move_to([gx0 + gw / 2, gy, 0])
        fill = always_redraw(lambda: Rectangle(width=max(0.02, (gw - 0.2) * 0.5 * n.get_value() / NS), height=gh - 0.2, stroke_width=0,
                                               fill_color=ORANGE, fill_opacity=0.9).move_to([gx0 + 0.1 + max(0.02, (gw - 0.2) * 0.5 * n.get_value() / NS) / 2, gy, 0]))
        tick = Line([gx0 + gw / 2, gy - 0.85, 0], [gx0 + gw / 2, gy + 0.85, 0], color=TEXT, stroke_width=7)
        gl = T("stomach", 32, TEXT).move_to([gx0 + 0.95, gy + 1.0, 0])
        ro = always_redraw(lambda: T("N = %d" % (int(round(n.get_value() / 10.0)) * 10), 44, TEAL, weight=BOLD).move_to([3.9, -2.6, 0]))
        self.play(FadeIn(f), FadeIn(frame), FadeIn(gl), FadeIn(marker), FadeIn(ro), run_time=0.9)
        self.add(fill)
        self.wait(0.3)
        self.at("Each predator must eat")
        self.to("replace itself", n.animate.set_value(NS * 0.55), rate_func=smooth, lo=1.0)
        rl = T("replaces itself", 32, TEXT).move_to([gx0 + gw / 2 + 0.2, gy - 1.2, 0])
        self.play(n.animate.set_value(NS), run_time=1.0, rate_func=smooth)
        self.play(Create(tick), FadeIn(rl, shift=UP * 0.1), run_time=0.6)
        self.at("That happens")
        line = nstar_line()
        self.play(Create(line), run_time=1.2)
        lab1 = T("N* = m/(ea)", 38, ORANGE, weight=BOLD).move_to([-1.3, 2.65, 0])
        lab2 = T("predators stop changing", 24, ORANGE).move_to([-1.3, 2.15, 0])
        self.play(FadeIn(lab1), FadeIn(lab2), run_time=0.7)
        self.at("With more prey")
        self.play(n.animate.set_value(NS * 1.6), run_time=1.2, rate_func=smooth)
        up = Arrow([px(900), py(20), 0], [px(900), py(95), 0], buff=0, color=ORANGE, stroke_width=8, tip_length=0.3)
        upl = T("predators\nincrease", 30, ORANGE).move_to([px(900), py(135), 0])
        self.play(GrowArrow(up), FadeIn(upl), run_time=0.9)
        self.at("With fewer")
        self.play(n.animate.set_value(NS * 0.4), run_time=1.2, rate_func=smooth)
        dn = Arrow([px(250), py(130), 0], [px(250), py(55), 0], buff=0, color=ORANGE, stroke_width=8, tip_length=0.3)
        dnl = T("predators\ndecrease", 26, ORANGE).move_to([px(250), py(170), 0])
        self.play(GrowArrow(dn), FadeIn(dnl), run_time=0.9)
        self.play(n.animate.set_value(NS * 0.8), run_time=1.5, rate_func=smooth)
        self.finish()


def plane_world(lines=True, arrows=False, panel_on=True):
    g = VGroup()
    if panel_on:
        g.add(plane_panel())
    g.add(plane_axes())
    if lines:
        g.add(pstar_line(), nstar_line(), diamond(),
              T("P*", 34, TEAL, weight=BOLD).move_to([LAY["x0"] - 0.42, float(py(PS)), 0]),
              T("N*", 34, ORANGE, weight=BOLD).move_to([float(px(NS)), LAY["y0"] - 0.4, 0]))
    if arrows:
        for z in ZONES:
            g.add(zone_arrow(z))
    return g


class S07Plane(Base):
    def construct(self):
        set_layout(-5.6, -2.95, 6.0, 6.0)
        self.add(plane_panel())
        ax = plane_axes()
        self.add(ax)
        c1 = VGroup(T("P* = r/a", 40, TEAL, weight=BOLD), T("prey stop changing", 30, TEAL)).arrange(DOWN, buff=0.1).move_to([3.9, 2.0, 0])
        c2 = VGroup(T("N* = m/(ea)", 40, ORANGE, weight=BOLD), T("predators stop changing", 30, ORANGE)).arrange(DOWN, buff=0.1).move_to([3.9, 0.0, 0])
        pl, nl = pstar_line(), nstar_line()
        self.play(FadeIn(c1, shift=UP * 0.15), FadeIn(c2, shift=UP * 0.15), Create(pl), Create(nl), run_time=2.2)
        self.at("prey across")
        self.play(Indicate(ax[2], color=TEAL, scale_factor=1.25), run_time=0.8)
        self.at("predators up")
        self.play(Indicate(ax[3], color=ORANGE, scale_factor=1.25), run_time=0.8)
        pt = T("P*", 34, TEAL, weight=BOLD).move_to([LAY["x0"] - 0.42, float(py(PS)), 0])
        nt = T("N*", 34, ORANGE, weight=BOLD).move_to([float(px(NS)), LAY["y0"] - 0.4, 0])
        self.at("The two lines cut")
        dm = diamond()
        el = T("equilibrium (N*, P*)", 28, GOLD).move_to([px(1000), py(PS) + 0.5, 0]).set_z_index(30)
        el.set_stroke("#262b33", width=10, background=True)
        self.play(FadeIn(dm, scale=2.0), FadeIn(pt), FadeIn(nt), FadeOut(c1), FadeOut(c2), run_time=0.9)
        self.play(FadeIn(el), run_time=0.6)
        self.at("four zones")
        order = ["br", "tr", "tl", "bl"]
        t_end = self.narration_s - 0.2
        slot = (t_end - self.elapsed()) / 4.0
        card = words = prev_rec = None
        for z in order:
            rec = zone_rect(z)
            za = zone_arrow(z)
            fl = Flow(z)
            dc = direction_card(z)
            dw = direction_words(z)
            if card is None:
                self.play(FadeIn(rec), GrowArrow(za), FadeIn(fl), FadeIn(dc), FadeIn(dw), run_time=0.6)
                card, words = dc, dw
            else:
                self.play(FadeOut(prev_rec), FadeIn(rec), GrowArrow(za), FadeIn(fl), Transform(card, dc), Transform(words, dw), run_time=0.7)
            prev_rec = rec
            self.wait(max(0.2, slot - 0.7))
        self.finish()


def strip_all(tr, loop=MAIN):
    return strip_axes(), legend(), strip_curve(loop, tr, "N", TEAL), strip_curve(loop, tr, "P", ORANGE), now_line(loop, tr)


def build_world(tr, loop=MAIN, arrows=False):
    set_layout(-5.6, -2.95, 6.0, 6.0)
    pw = plane_world(arrows=arrows)
    sa, lg, cN, cP, nl = strip_all(tr, loop)
    cmp_ = T("computed", 26, TEXT).move_to([2.35, -1.95, 0])
    tl = trail(loop, tr)
    dt = dot_at(loop, tr, r=0.19)
    return pw, sa, lg, cN, cP, nl, cmp_, tl, dt


class S08Loop(Base):
    def construct(self):
        tr = ValueTracker(0.0)
        pw, sa, lg, cN, cP, nl, cmp_, tl, dt = build_world(tr, arrows=True)
        self.add(pw)
        self.wait(0.2)
        self.at("Start a dot")
        self.play(FadeIn(dt, scale=2.5), run_time=0.5)
        ring = Circle(radius=0.4, color=TEXT, stroke_width=4).move_to(MAIN.scr(0))
        self.play(Create(ring), run_time=0.4)
        self.play(FadeOut(ring), FadeIn(sa), FadeIn(lg), FadeIn(cmp_), run_time=0.4)
        self.add(tl, cN, cP, nl)
        self.play(tr.animate.set_value(1.0), run_time=self.narration_s - 0.3 - self.elapsed(), rate_func=linear)
        self.finish()


def hold_frame(scene, tags=True):
    up = MAIN.u_prey
    tr = ValueTracker(up)
    pw, sa, lg, cN, cP, nl, cmp_, tl, dt = build_world(tr)
    pos = MAIN.scr(up)
    ph = ValueTracker(0.0)
    spin_on(scene, ph, 1.0)
    ring = always_redraw(lambda: Circle(radius=0.38 + 0.14 * np.sin(ph.get_value() * 3.5), color=GOLD, stroke_width=6).move_to(pos))
    pk = T("prey peak", 32, TEAL).move_to([pos[0] - 0.1, pos[1] + 0.75, 0])
    q1 = T("rising?", 40, ORANGE, weight=BOLD).move_to([2.8, -2.75, 0])
    q2 = T("falling?", 40, ORANGE, weight=BOLD).move_to([5.1, -2.75, 0])
    q1.add_updater(lambda m, dt: m.set_opacity(0.45 + 0.55 * max(0.0, np.sin(ph.get_value() * 3.0))))
    q2.add_updater(lambda m, dt: m.set_opacity(0.45 + 0.55 * max(0.0, -np.sin(ph.get_value() * 3.0))))
    cut = T("?", 64, GOLD, weight=BOLD).move_to([SX0 + SW * up + 0.8, sP(MAIN.val(up)[1]) + 0.6, 0])
    return tr, (pw, sa, lg, cmp_, tl, cN, cP, nl, dt), ring, pk, q1, q2, cut


class S09Predict(Base):
    def construct(self):
        tr = ValueTracker(0.0)
        pw, sa, lg, cN, cP, nl, cmp_, tl, dt = build_world(tr)
        self.add(pw, sa, lg, cmp_, tl, cN, cP, nl, dt)
        self.play(tr.animate.set_value(MAIN.u_prey), run_time=self.until("where the prey curve", lead=0.0, lo=1.5) + 1.0, rate_func=smooth)
        ph = ValueTracker(0.0)
        spin_on(self, ph, 1.0)
        pos = MAIN.scr(MAIN.u_prey)
        ring = always_redraw(lambda: Circle(radius=0.38 + 0.14 * np.sin(ph.get_value() * 3.5), color=GOLD, stroke_width=6).move_to(pos))
        self.add(ring)
        pk = T("prey peak", 32, TEAL).move_to([pos[0] - 0.1, pos[1] + 0.75, 0])
        self.play(FadeIn(pk), run_time=0.5)
        self.at("Are the predators")
        q1 = T("rising?", 40, ORANGE, weight=BOLD).move_to([2.8, -2.75, 0])
        q2 = T("falling?", 40, ORANGE, weight=BOLD).move_to([5.1, -2.75, 0])
        q1.add_updater(lambda m, dt: m.set_opacity(0.45 + 0.55 * max(0.0, np.sin(ph.get_value() * 3.0))))
        q2.add_updater(lambda m, dt: m.set_opacity(0.45 + 0.55 * max(0.0, -np.sin(ph.get_value() * 3.0))))
        cut = T("?", 64, GOLD, weight=BOLD).move_to([SX0 + SW * MAIN.u_prey + 0.8, sP(MAIN.val(MAIN.u_prey)[1]) + 0.6, 0])
        self.play(FadeIn(q1), FadeIn(q2), FadeIn(cut), run_time=0.6)
        self.finish()


class S10Pause(Base):
    def construct(self):
        tr, objs, ring, pk, q1, q2, cut = hold_frame(self)
        self.add(*objs, ring, pk, q1, q2, cut)
        bar_bg = Rectangle(width=4.8, height=0.26, stroke_color=GOLD, stroke_width=4).move_to([4.0, -3.4, 0])
        cnt = ValueTracker(1.0)
        bar = always_redraw(lambda: Rectangle(width=max(0.01, 4.8 * cnt.get_value()), height=0.26, stroke_width=0, fill_color=GOLD,
                                              fill_opacity=0.9).move_to([1.6 + max(0.01, 4.8 * cnt.get_value()) / 2, -3.4, 0]))
        self.add(bar_bg, bar)
        self.play(cnt.animate.set_value(0.0), run_time=4.6, rate_func=linear)
        self.finish()


class S11Reveal(Base):
    def construct(self):
        up = MAIN.u_prey
        u1 = u_at_N(MAIN, 800)
        tr = ValueTracker(up)
        pw, sa, lg, cN, cP, nl, cmp_, tl, dt = build_world(tr)
        self.add(pw, sa, lg, cmp_, tl, cN, cP, nl, dt)
        q1 = T("rising!", 44, ORANGE, weight=BOLD).move_to([3.9, -2.75, 0])
        self.play(FadeIn(q1, scale=1.4), run_time=0.6)
        sx_ = lambda: float(px(NS)) + 0.05
        br = always_redraw(lambda: VGroup(
            Line([sx_(), MAIN.scr(tr.get_value())[1] - 0.5, 0], [MAIN.scr(tr.get_value())[0], MAIN.scr(tr.get_value())[1] - 0.5, 0], color=TEXT, stroke_width=6),
            Line([sx_(), MAIN.scr(tr.get_value())[1] - 0.65, 0], [sx_(), MAIN.scr(tr.get_value())[1] - 0.35, 0], color=TEXT, stroke_width=6),
            Line([MAIN.scr(tr.get_value())[0], MAIN.scr(tr.get_value())[1] - 0.65, 0], [MAIN.scr(tr.get_value())[0], MAIN.scr(tr.get_value())[1] - 0.35, 0], color=TEXT, stroke_width=6)))
        bl = always_redraw(lambda: T("prey still above N*", 28, TEXT).move_to([-1.5, 2.75, 0]))
        # the dot drifts on at orbit pace for the whole scene
        t_total = self.narration_s - 0.4
        self.play(tr.animate.set_value(up + (u1 - up) * 0.3), run_time=self.until("there are still more", lead=0.0, lo=1.0), rate_func=linear)
        self.play(FadeIn(br), FadeIn(bl), run_time=0.6)
        self.play(tr.animate.set_value(u1), run_time=max(1.0, t_total - self.elapsed()), rate_func=linear)
        self.finish()


class S12Lag(Base):
    def construct(self):
        up, upp = MAIN.u_prey, MAIN.u_pred
        u0 = u_at_N(MAIN, 800)
        tr = ValueTracker(u0)
        pw, sa, lg, cN, cP, nl, cmp_, tl, dt = build_world(tr)
        self.add(pw, sa, lg, cmp_, tl, cN, cP, nl, dt)
        self.to("star", tr.animate.set_value(upp), rate_func=smooth, lead=0.0, lo=1.0)
        ring = Circle(radius=0.38, color=ORANGE, stroke_width=6).move_to(MAIN.scr(upp))
        self.play(Create(ring), tr.animate.set_value(upp + 0.02), run_time=0.7, rate_func=linear)
        x1, x2 = SX0 + SW * up, SX0 + SW * upp
        y = 3.0
        brk = VGroup(Line([x1, y, 0], [x2, y, 0], color=TEXT, stroke_width=6),
                     Line([x1, y - 0.18, 0], [x1, y + 0.18, 0], color=TEXT, stroke_width=6),
                     Line([x2, y - 0.18, 0], [x2, y + 0.18, 0], color=TEXT, stroke_width=6))
        pkN = DashedLine([x1, sN(MAIN.val(up)[0]) + 0.05, 0], [x1, y, 0], color=TEAL, stroke_width=4)
        pkP = DashedLine([x2, sP(MAIN.val(upp)[1]) + 0.05, 0], [x2, y, 0], color=ORANGE, stroke_width=4)
        lag = T("lag", 38, TEXT, weight=BOLD).move_to([(x1 + x2) / 2 + 1.1, y + 0.35, 0])
        self.at("So the predator peak")
        self.play(Create(pkN), Create(pkP), tr.animate.set_value(upp + 0.08), run_time=1.0, rate_func=linear)
        self.play(Create(brk), FadeIn(lag), tr.animate.set_value(upp + 0.16), run_time=0.9, rate_func=linear)
        self.at("Nothing in the model")
        clock = VGroup(Circle(radius=0.55, color=TEXT, stroke_width=6), Line(ORIGIN, UP * 0.36, color=TEXT, stroke_width=6),
                       Line(ORIGIN, RIGHT * 0.27, color=TEXT, stroke_width=6), Line([-0.62, -0.62, 0], [0.62, 0.62, 0], color=RED, stroke_width=9)).move_to([2.1, -3.05, 0])
        cl = T("no built-in delay", 34, RED, weight=BOLD).move_to([4.75, -3.05, 0])
        self.play(FadeIn(clock, scale=1.3), FadeIn(cl, shift=LEFT * 0.2), tr.animate.set_value(upp + 0.26), run_time=1.0, rate_func=linear)
        self.play(tr.animate.set_value(upp + 0.42), run_time=self.until("The lag comes", lo=1.0), rate_func=linear)
        self.at("The lag comes")
        self.play(Indicate(lag, color=GOLD, scale_factor=1.3), tr.animate.set_value(upp + 0.5), run_time=1.0, rate_func=linear)
        self.play(tr.animate.set_value(upp + 0.65), run_time=max(0.5, self.narration_s - 0.4 - self.elapsed()), rate_func=linear)
        self.finish()


class S13Loops(Base):
    def construct(self):
        set_layout(-5.6, -2.95, 6.0, 6.0)
        pw = plane_world()
        one = ValueTracker(1.0)
        trm = trail(MAIN, one, TEXT, 7, 0.9)
        ph = ValueTracker(0.0)
        spin_on(self, ph, 0.2)
        dm = always_redraw(lambda: Dot(MAIN.scr(ph.get_value() % 1.0), radius=0.17, color=TEXT).set_z_index(6))
        self.add(pw, trm, dm)
        GOLDL, VIOL = GOLD, "#B58CD9"
        uA, uB = ValueTracker(0.0), ValueTracker(0.0)
        trA = trail(SMALL, uA, GOLDL, 7, 0.95)
        trB = trail(BIG, uB, VIOL, 7, 0.95)
        dA = always_redraw(lambda: Dot(SMALL.scr(uA.get_value() % 1.0), radius=0.17, color=GOLDL).set_z_index(6))
        dB = always_redraw(lambda: Dot(BIG.scr(uB.get_value() % 1.0), radius=0.17, color=VIOL).set_z_index(6))
        self.wait(0.3)
        self.at("Start the dot")
        stA = Circle(radius=0.34, color=GOLDL, stroke_width=5).move_to(SMALL.scr(0))
        self.play(FadeIn(dA, scale=2.5), Create(stA), run_time=0.8)
        self.add(trA)
        self.play(FadeOut(stA), uA.animate.set_value(1.0), run_time=self.until("In this classical") + 0.4, rate_func=linear)
        uA.add_updater(lambda m, dt: m.increment_value(dt * 0.2))
        self.add(uA)
        lines = ["classical Lotka-Volterra model", "each start with both", "populations present, away", "from the equilibrium, keeps", "its own loop (computed)"]
        note = VGroup(*[T(s, 28 if i == 0 else 28, GOLD if i == 0 else TEXT, weight=BOLD if i == 0 else NORMAL) for i, s in enumerate(lines)]).arrange(DOWN, aligned_edge=LEFT, buff=0.25).move_to([3.75, 1.4, 0])
        self.at("In this classical")
        self.play(FadeIn(note[0], shift=UP * 0.1), run_time=0.6)
        self.at("each start")
        self.play(FadeIn(note[1], shift=UP * 0.1), run_time=0.5)
        self.at("populations present")
        self.play(FadeIn(note[2], shift=UP * 0.1), run_time=0.5)
        self.at("away from")
        self.play(FadeIn(note[3], shift=UP * 0.1), run_time=0.5)
        self.at("keeps its own")
        self.play(FadeIn(note[4], shift=UP * 0.1), run_time=0.5)
        self.at("Where it starts")
        stB = Circle(radius=0.34, color=VIOL, stroke_width=5).move_to(BIG.scr(0))
        self.play(FadeIn(dB, scale=2.5), Create(stB), run_time=0.8)
        self.add(trB)
        self.play(FadeOut(stB), uB.animate.set_value(1.0), run_time=self.until("size of the cycle", lo=2.0), rate_func=linear)
        uB.add_updater(lambda m, dt: m.increment_value(dt * 0.2))
        self.add(uB)
        sz = T("start sets the size", 34, VIOL, weight=BOLD).move_to([3.85, -1.5, 0])
        self.play(FadeIn(sz), run_time=0.6)
        self.finish()


class S14Rule(Base):
    def construct(self):
        set_layout(-2.35, -2.75, 4.7, 5.5)
        pw = plane_world(panel_on=False)
        pnl = panel(0.0, 0.2, 5.6, 6.6)
        one = ValueTracker(1.0)
        tl = trail(MAIN, one, TEXT, 5, 0.7)
        L = Ledger(TEAL, "prey ledger", -5.1, 0.35, w=3.2, h=3.9, bar=False)
        Rr = Ledger(ORANGE, "predator ledger", 5.1, 0.35, w=3.2, h=3.9, bar=False)
        L.title.scale(0.8); Rr.title.scale(0.8)
        L.fill_static(2, 2)
        Rr.fill_static(2, 2)
        ph = ValueTracker(0.0)
        spin_on(self, ph, 0.1)
        dm = always_redraw(lambda: Dot(MAIN.scr(ph.get_value() % 1.0), radius=0.15, color=TEXT).set_z_index(6))
        self.add(pnl, pw, tl, dm)
        self.play(FadeIn(L.mobs(), shift=RIGHT * 0.3), FadeIn(Rr.mobs(), shift=LEFT * 0.3), run_time=1.0)
        dmd = pxy(NS, PS)
        xa, xb = -3.5, float(dmd[0]) - 0.28
        xc, xd = 3.5, float(dmd[0]) + 0.28
        c1 = chain(xa, xb, 0.35, TEAL, GOLD, n=5)
        c2 = chain(xc, xd, 0.35, ORANGE, GOLD, n=5)
        self.at("So, every kill")
        self.play(LaggedStart(*[FadeIn(c, scale=0.5) for c in c1], lag_ratio=0.2), LaggedStart(*[FadeIn(c, scale=0.5) for c in c2], lag_ratio=0.2), run_time=2.0)
        trk = ValueTracker(0.0)
        spin_on(self, trk, 0.4)
        t1 = always_redraw(lambda: Dot([xa + (xb - xa) * (trk.get_value() % 1.0), 0.35, 0], radius=0.12, color=TEXT).set_z_index(7))
        t2 = always_redraw(lambda: Dot([xc + (xd - xc) * (trk.get_value() % 1.0), 0.35, 0], radius=0.12, color=TEXT).set_z_index(7))
        self.add(t1, t2)
        self.at("In this simple model")
        head = T("per capita\ngrowth rate", 32, TEXT, weight=BOLD, line_spacing=1.4).move_to([5.2, 3.0, 0])
        self.play(FadeIn(head, shift=DOWN * 0.15), run_time=0.8)
        fP = T("per prey:\nr − aP", 34, TEAL).move_to([-5.1, -2.5, 0])
        fN = T("per predator:\neaN − m", 34, ORANGE).move_to([5.1, -2.5, 0])
        self.at("each population's")
        self.play(FadeIn(fP, shift=UP * 0.15), FadeIn(fN, shift=UP * 0.15), run_time=0.9)
        self.at("set by the")
        self.play(Indicate(fP, color=TEAL, scale_factor=1.15), Indicate(fN, color=ORANGE, scale_factor=1.15), run_time=1.0)
        self.finish()


class S15End(EndCard):
    LINE = "Each population's per capita growth rate is set by the other's numbers."
