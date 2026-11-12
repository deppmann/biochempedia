"""Downhill for Free (crossing-the-membrane, film 1)  (Biochemistrypedia explainer, high school Biology)

COLOR MAP (one colour per concept, whole film and the lesson's take-homes)
  WATER   = small BLUE dots           SODIUM Na+   = ORANGE dots
  CHLORIDE Cl- = GREEN dots           DYE          = RED dots
  OXYGEN  = small WHITE dots, grey outline
  MEMBRANE = grey heads, pale cream tails      PROTEINS = TEAL blocks      ATP = YELLOW token
THE WORLD: one vertical membrane at x = 0 with the left side and the right side; the tanks, drops and
counters are all built around it. Dye counts come from a real random-walk simulation (dye_sim).
Rates in the tank counters are schematic and say so.
"""
import numpy as np
from bp_style import *  # noqa: F401,F403

NA = "#F29E4C"
CL = GREEN
DYE = RED
WATER = BLUE
O2 = "#FFFFFF"
HEAD = GREY
TAILC = "#EADFC8"
PROT = TEAL
ATP = YELLOW
FPS_SIM = 30


def lab(text, size=28, color=TEXT, **kw):
    t = T(text, size, color, **kw)
    t.set_stroke(BG, 7, background=True)
    t.set_z_index(20)
    return t


def P3(x, y):
    return np.array([x, y, 0.0])


# ------------------------------------------------------------------ swarm of jiggling dots
def circ_in(C, R):
    C = np.array(C, float)

    def f(P):
        v = P - C
        d = np.linalg.norm(v, axis=1)
        m = d > R
        P = P.copy()
        if m.any():
            nd = np.clip(2 * R - d[m], 0, R)
            P[m] = C + v[m] / d[m, None] * nd[:, None]
        return P
    return f


def circ_out(C, R):
    C = np.array(C, float)

    def f(P):
        v = P - C
        d = np.linalg.norm(v, axis=1) + 1e-9
        m = d < R
        P = P.copy()
        if m.any():
            P[m] = C + v[m] / d[m, None] * (2 * R - d[m])[:, None]
        return P
    return f


class Swarm(VGroup):
    """Dots doing a random walk inside a box, reflecting at its walls (and at a water surface, if ymax is given)."""

    def __init__(self, color, n, box, sig=1.4, r=0.09, seed=0, ring=False, constrain=None, ymax=None, accept=None):
        super().__init__()
        self.rng = np.random.RandomState(seed)
        self.box, self.sig, self.constrain, self.ymax = box, sig, constrain, ymax
        x0, x1, y0, y1 = box
        pts = []
        while len(pts) < n:
            p = [self.rng.uniform(x0, x1), self.rng.uniform(y0, y1)]
            if accept is None or accept(p[0], p[1]):
                pts.append(p)
        self.P = np.array(pts, float)
        self._enforce()
        for p in self.P:
            d = Dot(P3(*p), radius=r, color=color)
            if ring:
                d.set_stroke(GREY, 2.5, 1)
            self.add(d)
        self.op = ValueTracker(1.0)
        self._lastop = 1.0
        self.add_updater(self._step)

    def _enforce(self):
        P = self.P
        x0, x1, y0, y1 = self.box
        for ax, (lo, hi) in enumerate(((x0, x1), (y0, y1))):
            m = P[:, ax] < lo
            P[m, ax] = 2 * lo - P[m, ax]
            m = P[:, ax] > hi
            P[m, ax] = 2 * hi - P[m, ax]
        if self.ymax is not None:
            ym = self.ymax(P[:, 0])
            m = P[:, 1] > ym
            P[m, 1] = 2 * ym[m] - P[m, 1]
            P[:, 1] = np.maximum(P[:, 1], y0)
        if self.constrain is not None:
            P = self.constrain(P)
        self.P = P

    def _step(self, _, dt):
        v = self.op.get_value()
        if v != self._lastop:
            self._lastop = v
            for d in self.submobjects:
                d.set_fill(opacity=v)
                d.set_stroke(opacity=v)
        if dt <= 0:
            return
        old = self.P
        self.P = old + self.rng.randn(*old.shape) * self.sig * np.sqrt(dt)
        self._enforce()
        for d, a, b in zip(self.submobjects, old, self.P):
            d.shift([b[0] - a[0], b[1] - a[1], 0])


def fade_swarm(sw, to=1.0, rt=0.6):
    return sw.op.animate.set_value(to).set_run_time(rt)


class Passers(VGroup):
    """Dots that drift along x with a little wobble (used for things that cross the membrane)."""

    def __init__(self, color, ys, x0, v, x_end=6.5, loop=None, r=0.1, ring=False, seed=0):
        super().__init__()
        rng = np.random.RandomState(seed)
        self.v, self.x_end, self.loop, self.t = v, x_end, loop, 0.0
        self.y0 = list(ys)
        self.ph = [rng.uniform(0, 6) for _ in ys]
        self.x = [x0 + (i * 0.9 if loop else 0.0) for i in range(len(ys))]
        for x, y in zip(self.x, ys):
            d = Dot(P3(x, y), radius=r, color=color)
            if ring:
                d.set_stroke(GREY, 2.5, 1)
            self.add(d)
        self.add_updater(self._step)

    def _step(self, _, dt):
        self.t += dt
        for i, d in enumerate(self.submobjects):
            self.x[i] += self.v * dt
            if self.loop:
                if self.x[i] > self.loop[1]:
                    self.x[i] = self.loop[0]
            else:
                self.x[i] = min(self.x[i], self.x_end)
            y = self.y0[i] + 0.16 * np.sin(2.3 * self.t + self.ph[i])
            d.move_to(P3(self.x[i], y))


# ------------------------------------------------------------------ dye simulation (computed)
class DyeSim:
    def __init__(self, seed, n=110, D=1.3, t_rel=7.3, t_cnt=8.8, T=34.0):
        rng = np.random.RandomState(seed)
        K = int(T * FPS_SIM)
        dt = 1.0 / FPS_SIM
        sd = np.sqrt(2 * D * dt)
        blob = (-5.0, -3.4, -1.0, 1.1)
        full = (-5.45, 5.45, -3.25, 1.4)
        P = np.zeros((K, n, 2))
        p = np.stack([rng.uniform(blob[0], blob[1], n), rng.uniform(blob[2], blob[3], n)], 1)
        lr = np.zeros(K)
        rl = np.zeros(K)
        side = np.where(p[:, 0] < 0, -1, 1)   # a crossing counts once the dot is clear of the line (+-0.5)
        for k in range(K):
            t = k * dt
            box = blob if t < t_rel else full
            q = p + rng.randn(n, 2) * sd
            for ax, (lo, hi) in enumerate(((box[0], box[1]), (box[2], box[3]))):
                m = q[:, ax] < lo
                q[m, ax] = 2 * lo - q[m, ax]
                m = q[:, ax] > hi
                q[m, ax] = 2 * hi - q[m, ax]
            if t >= t_cnt:
                go_r = (side == -1) & (q[:, 0] > 0.5)
                go_l = (side == 1) & (q[:, 0] < -0.5)
                lr[k], rl[k] = go_r.sum(), go_l.sum()
                side = np.where(go_r, 1, np.where(go_l, -1, side))
            p = q
            P[k] = p
        self.P, self.lr, self.rl, self.t_cnt, self.K = P, np.cumsum(lr), np.cumsum(rl), t_cnt, K

    def rates(self, t):
        if t < self.t_cnt + 0.3:
            return (0, 0)
        k = min(int(t * FPS_SIM), self.K - 1)
        w = min(3.0, t - self.t_cnt)
        k0 = max(0, k - int(w * FPS_SIM))
        w = max((k - k0) / FPS_SIM, 0.5)
        return (int(round((self.lr[k] - self.lr[k0]) / w)), int(round((self.rl[k] - self.rl[k0]) / w)))


_SIM = {}


def sim():
    if "s" not in _SIM:
        _SIM["s"] = DyeSim(SEED)
    return _SIM["s"]


SEED = 96
CY0 = -0.8   # centre of the dye tank


class DyeDots(VGroup):
    def __init__(self, t0=0.0):
        super().__init__()
        s = sim()
        self.t = t0
        self.sc, self.cy, self.op = ValueTracker(1.0), ValueTracker(CY0), ValueTracker(1.0)
        self._lastop = 1.0
        for p in s.P[int(t0 * FPS_SIM)]:
            self.add(Dot(P3(*p), radius=0.09, color=DYE))
        self.add_updater(self._step)

    def _step(self, _, dt):
        self.t += max(dt, 0)
        s = sim()
        p = s.P[min(int(self.t * FPS_SIM), s.K - 1)]
        sc, cy = self.sc.get_value(), self.cy.get_value()
        v = self.op.get_value()
        for d, q in zip(self.submobjects, p):
            d.move_to(P3(sc * q[0], cy + sc * (q[1] - CY0)))
            if v != self._lastop:
                d.set_fill(opacity=v)
        self._lastop = v


def dye_tank(level=1.5):
    out = VMobject(stroke_color=GREY, stroke_width=6)
    out.set_points_as_corners([P3(-5.7, 1.8), P3(-5.7, -3.4), P3(5.7, -3.4), P3(5.7, 1.8)])
    fill = Rectangle(width=11.4, height=level + 3.4, stroke_width=0, fill_color=WATER, fill_opacity=0.2)
    fill.move_to(P3(0, (level - 3.4) / 2))
    surf = Line(P3(-5.7, level), P3(5.7, level), color=WATER, stroke_width=4)
    return VGroup(fill, surf, out)


def dye_hits(t):
    return sim().rates(t)


class Counter(VGroup):
    def __init__(self, title, fn, size=32):
        self.fn, self.vals, self.cl, self.cr, self.size = fn, None, TEXT, TEXT, size
        box = RoundedRectangle(corner_radius=0.12, width=5.5, height=1.02, stroke_color=GREY, stroke_width=3,
                               fill_color=BG, fill_opacity=0.92)
        ttl = T(title, 22, TEXT).move_to(box.get_top() + DOWN * 0.26)
        super().__init__(box, ttl)
        self.box = box
        self.row = VGroup()
        self.add(self.row)
        self.move_to(P3(3.85, 3.1))
        self._upd(self)
        self.add_updater(self._upd)

    def _upd(self, m):
        v = self.fn()
        key = (v, self.cl, self.cr)
        if key == self.vals:
            return
        self.vals = key
        a = M(f"→ {v[0]:>3}", self.size, self.cl)
        b = M(f"← {v[1]:>3}", self.size, self.cr)
        row = VGroup(a, b).arrange(RIGHT, buff=0.8)
        row.move_to(self.box.get_center() + DOWN * 0.17)
        self.remove(self.row)
        self.row = row
        self.add(row)


def show_counter(scene, cnt, rt=0.5):
    cnt.suspend_updating()
    scene.play(FadeIn(cnt), run_time=rt)
    cnt.resume_updating()


# ------------------------------------------------------------------ membrane
ROWS = [-3.36 + 0.42 * i for i in range(17)]
YA, YB_ = 1.68, -1.68


def make_membrane(prot=False, thin=False):
    hw, rr = 0.55, 0.17
    rows = {}
    mem = VGroup()
    for y in ROWS:
        if prot and (abs(y - YA) < 0.7 or abs(y - YB_) < 0.7):
            continue
        g = VGroup()
        for sgn in (-1, 1):
            hx = sgn * hw
            for dy in (0.09, -0.09):
                g.add(Line(P3(hx, y), P3(sgn * 0.1, y + dy), color=TAILC, stroke_width=4.5))
            g.add(Dot(P3(hx, y), radius=rr, color=HEAD).set_stroke(TEXT, 1.5, 0.6))
        rows[y] = g
        mem.add(g)
    mem.rows = rows
    if prot:
        mem.add(*blocks())
    if thin:
        mem.stretch(0.4, 0).stretch(0.76, 1).move_to(P3(0, -0.8))
    return mem


def blocks():
    out = []
    for y in (YA, YB_):
        r = RoundedRectangle(corner_radius=0.18, width=1.25, height=1.3, stroke_color=PROT, stroke_width=4,
                             fill_color=PROT, fill_opacity=0.6).move_to(P3(0, y))
        out.append(r)
    return out


def thin_blocks():
    return []


# ------------------------------------------------------------------ two tanks
XL0, XL1, XR0, XR1, YBOT, YTOP = -5.7, -0.32, 0.32, 5.7, -3.4, 1.8


def tanks(lL, lR):
    outL = VMobject(stroke_color=GREY, stroke_width=6)
    outL.set_points_as_corners([P3(XL0, YTOP), P3(XL0, YBOT), P3(XL1, YBOT), P3(XL1, YTOP)])
    outR = VMobject(stroke_color=GREY, stroke_width=6)
    outR.set_points_as_corners([P3(XR0, YTOP), P3(XR0, YBOT), P3(XR1, YBOT), P3(XR1, YTOP)])
    outs = VGroup(outL, outR)

    def fills(x0, x1, tr):
        f = Rectangle(width=x1 - x0, height=1, stroke_width=0, fill_color=WATER, fill_opacity=0.2)
        s = Line(P3(x0, 0), P3(x1, 0), color=WATER, stroke_width=4)

        def u(m):
            lv = tr.get_value()
            h = lv - YBOT
            f.become(Rectangle(width=x1 - x0, height=h, stroke_width=0, fill_color=WATER, fill_opacity=0.2)
                     .move_to(P3((x0 + x1) / 2, YBOT + h / 2)))
            s.put_start_and_end_on(P3(x0, lv), P3(x1, lv))
        g = VGroup(f, s)
        g.add_updater(u)
        u(g)
        return g
    wl, wr = fills(XL0, XL1, lL), fills(XR0, XR1, lR)
    g = VGroup(wl, wr, outs)
    g.outs, g.waters = outs, VGroup(wl, wr)
    return g


def water_swarm(lL, lR, n=76, seed=3):
    ymax = lambda x: np.where(x < 0, lL.get_value(), lR.get_value()) - 0.08
    return Swarm(WATER, n, (-5.55, 5.55, -3.25, 0.1), sig=1.5, r=0.075, seed=seed, ymax=ymax)


def salt_swarms(lL, n=11, seed=5, start=None):
    ymax = lambda x: np.zeros_like(x) + lL.get_value() - 0.1
    box = (-5.5, -0.48, -3.2, 0.1)
    a = Swarm(NA, n, box, sig=1.5, r=0.12, seed=seed, ymax=ymax)
    b = Swarm(CL, n, box, sig=1.5, r=0.12, seed=seed + 1, ymax=ymax)
    return a, b


def legend(items, pos):
    g = VGroup()
    for col, txt in items:
        g.add(VGroup(Dot(radius=0.14, color=col), lab(txt, 30, col)).arrange(RIGHT, buff=0.14))
    g.arrange(RIGHT, buff=0.5).move_to(pos)
    return g


def ring_at(pos, color=TEXT, r=0.3):
    return Circle(radius=r, stroke_color=color, stroke_width=5).move_to(pos)


def arr(a, b, color=WATER, w=8):
    return Arrow(a, b, buff=0, color=color, stroke_width=w, tip_length=0.3, max_tip_length_to_length_ratio=0.5,
                 max_stroke_width_to_length_ratio=14)


# =====================================================================================================
class S00Title(TitleCard):
    LESSON = "Crossing the Membrane"
    TITLE = "Downhill for Free"


# -----------------------------------------------------------------------------------------------------
class S01Question(SpokenScene):
    def construct(self):
        C, R = (0.0, -0.3), 2.3
        cell = Circle(radius=R, stroke_color=GREY, stroke_width=10, fill_color=WATER, fill_opacity=0.08).move_to(P3(*C))
        ring = Circle(radius=R - 0.12, stroke_color=TAILC, stroke_width=3).move_to(P3(*C))
        inside = Swarm(WATER, 24, (-2.2, 2.2, -2.5, 1.9), sig=1.6, r=0.1, seed=1, constrain=circ_in(C, R - 0.3),
                       accept=lambda x, y: np.hypot(x - C[0], y - C[1]) < R - 0.3)
        outside = Swarm(WATER, 60, (-6.5, 6.5, -3.7, 3.7), sig=1.6, r=0.1, seed=2, constrain=circ_out(C, R + 0.3),
                        accept=lambda x, y: np.hypot(x - C[0], y - C[1]) > R + 0.3)
        inside.op.set_value(0)
        outside.op.set_value(0)
        self.add(cell, ring, inside, outside)
        self.play(inside.op.animate.set_value(1), outside.op.animate.set_value(1), run_time=0.4)
        self.at("water inside a cell")
        self.play(cell.animate.set_fill(WATER, 0.3), run_time=0.5)
        self.play(cell.animate.set_fill(WATER, 0.08), run_time=0.7)
        self.at("all around it")
        big = Circle(radius=R + 0.2, stroke_color=WATER, stroke_width=8).move_to(P3(*C))
        self.add(big)
        self.play(big.animate.scale(2.3).set_stroke(opacity=0), run_time=1.4)
        self.remove(big)
        self.at("so how does water know")
        q = T("?", 110, GOLD, font=TITLE_FONT, weight=BOLD).move_to(P3(0, 2.95))
        q.set_stroke(BG, 8, background=True)
        self.play(GrowFromCenter(q), run_time=0.5)
        self.play(q.animate.scale(1.12), run_time=0.4)
        self.play(q.animate.scale(1 / 1.12), run_time=0.4)
        self.at("to find out")
        glass = dye_tank()
        world = VGroup(cell, ring, q)
        self.play(world.animate.scale(0.3).set_opacity(0), inside.op.animate.set_value(0),
                  outside.op.animate.set_value(0), FadeIn(glass), run_time=1.6)
        self.at("a drop of dye")
        drop = Dot(P3(-4.1, 3.3), radius=0.22, color=DYE)
        self.add(drop)
        self.play(drop.animate.move_to(P3(-4.1, 1.55)), rate_func=rush_into, run_time=0.8)
        splash = Circle(radius=0.2, stroke_color=DYE, stroke_width=6).move_to(P3(-4.1, 1.5))
        self.remove(drop)
        self.add(splash)
        self.play(splash.animate.scale(4).set_stroke(opacity=0), run_time=0.9)
        self.finish()


# -----------------------------------------------------------------------------------------------------
class S02Dye(SpokenScene):
    def construct(self):
        tank = dye_tank()
        dye = DyeDots(0.0)
        dye.op.set_value(0)
        self.add(tank, dye)
        self.play(dye.op.animate.set_value(1), run_time=0.6)
        self.at("each dye molecule")
        pick = dye.submobjects[9]
        ring = Circle(radius=0.3, stroke_color=TEXT, stroke_width=5)
        ring.add_updater(lambda m: m.move_to(pick.get_center()))
        trace = TracedPath(pick.get_center, stroke_color=TEXT, stroke_width=4, dissipating_time=2.0)
        self.add(trace, ring)
        self.at("now draw a line", lead=0.5)
        ring.clear_updaters()
        trace.clear_updaters()
        self.remove(trace)
        self.play(FadeOut(ring), run_time=0.3)
        self.at("now draw a line")
        mid = DashedLine(P3(0, 1.8), P3(0, -3.4), color=TEXT, stroke_width=5, dash_length=0.25)
        self.play(Create(mid), run_time=0.9)
        self.at("count the crossings")
        cnt = Counter("crossings per second", lambda: dye_hits(dye.t))
        show_counter(self, cnt)
        self.finish()


# -----------------------------------------------------------------------------------------------------
class S03Tally(SpokenScene):
    def construct(self):
        tank = dye_tank()
        mid = DashedLine(P3(0, 1.8), P3(0, -3.4), color=TEXT, stroke_width=5, dash_length=0.25)
        dye = DyeDots(11.5)
        cnt = Counter("crossings per second", lambda: dye_hits(dye.t))
        self.add(tank, mid, dye, cnt)
        self.at("far more cross")
        cnt.cl = YELLOW
        crowded = lab("crowded side", 30, YELLOW).move_to(P3(-3.0, 2.4))
        self.play(FadeIn(crowded), run_time=0.5)
        self.at("simply because")
        self.play(Indicate(crowded, scale_factor=1.1, color=YELLOW), run_time=0.8)
        self.at("later")
        cnt.cl = TEXT
        later = lab("later", 36, GOLD, weight=BOLD).move_to(P3(-3.0, 3.3))
        self.play(FadeOut(crowded), FadeIn(later), run_time=0.5)
        self.at("the dye is even")
        self.wait(1.0)
        self.at("crossings still happen")
        cnt.cl, cnt.cr = GOLD, GOLD
        self.play(FadeOut(later), run_time=0.4)
        self.play(Indicate(cnt.box, color=GOLD, scale_factor=1.05), run_time=0.8)
        self.at("the molecules never stopped moving")
        cnt.cl, cnt.cr = TEXT, TEXT
        dots = [dye.submobjects[i] for i in (3, 20, 35)]
        traces = [TracedPath(d.get_center, stroke_color=TEXT, stroke_width=4, dissipating_time=2.5) for d in dots]
        self.add(*traces)
        self.at("there is just no net movement", lead=0.5)
        for t in traces:
            t.clear_updaters()
            self.remove(t)
        self.at("there is just no net movement")
        cap = lab("still moving, no net movement", 30, GOLD, weight=BOLD).move_to(P3(-3.2, 3.2))
        self.play(FadeIn(cap, shift=UP * 0.15), run_time=0.6)
        self.finish()


# -----------------------------------------------------------------------------------------------------
class S04Gradient(SpokenScene):
    def construct(self):
        tank = dye_tank()
        dye = DyeDots(7.0)
        self.add(tank, dye)
        self.play(tank.animate.scale(0.55).move_to(P3(0, 2.15)), dye.sc.animate.set_value(0.55),
                  dye.cy.animate.set_value(2.15), run_time=1.5)

        def top(x):
            return -0.75 - 2.35 * (x + 5.5) / 11.0
        n = 44
        strips = VGroup()
        for i in range(n):
            x = -5.5 + (i + 0.5) * 11.0 / n
            f = i / (n - 1)
            col = interpolate_color(ManimColor("#9E2A2B"), ManimColor("#F6D5CF"), f)
            h = top(x) + 3.15
            strips.add(Rectangle(width=11.0 / n + 0.01, height=h, stroke_width=0, fill_color=col, fill_opacity=1)
                       .move_to(P3(x, -3.15 + h / 2)))
        self.play(LaggedStart(*[FadeIn(s, shift=UP * 0.2) for s in strips], lag_ratio=0.03), run_time=1.6)
        self.at("concentration gradient")
        gl = lab("concentration gradient", 34, YELLOW, weight=BOLD).move_to(P3(2.6, 0.2))
        self.play(FadeIn(gl, shift=UP * 0.1), run_time=0.6)
        self.at("no energy spent")
        self.wait(0.2)
        self.at("substance moves")
        ball = Dot(P3(-5.2, top(-5.2) + 0.32), radius=0.3, color=GOLD).set_stroke(TEXT, 3)
        path = Line(P3(-5.2, top(-5.2) + 0.32), P3(5.2, top(5.2) + 0.32))
        self.add(ball)
        self.play(MoveAlongPath(ball, path), rate_func=rate_functions.ease_in_sine, run_time=5.4)
        self.at("that spreading is diffusion")
        dl = VGroup(lab("diffusion:", 36, GOLD, weight=BOLD), lab("down the gradient,", 30, TEXT),
                    lab("no energy spent", 30, TEXT)).arrange(DOWN, buff=0.12).move_to(P3(2.7, -0.95))
        self.play(FadeOut(gl), FadeIn(dl, shift=UP * 0.1), run_time=0.7)
        self.finish()


# -----------------------------------------------------------------------------------------------------
def water_sides(seed=3, n=46):
    L = Swarm(WATER, n, (-6.3, -0.85, -3.5, 3.5), sig=1.4, r=0.09, seed=seed)
    R = Swarm(WATER, n, (0.85, 6.3, -3.5, 3.5), sig=1.4, r=0.09, seed=seed + 10)
    return L, R


class S05Membrane(SpokenScene):
    def construct(self):
        L, R = water_sides()
        L.op.set_value(0)
        R.op.set_value(0)
        mem = make_membrane()
        self.add(L, R)
        self.play(L.op.animate.set_value(1), R.op.animate.set_value(1),
                  LaggedStart(*[FadeIn(g, shift=UP * 0.1) for g in mem], lag_ratio=0.05), run_time=2.6)
        self.at("two rows of phospholipids")
        lefts = VGroup(*[g[2] for g in mem])
        rights = VGroup(*[g[5] for g in mem])
        self.play(Indicate(lefts, color=TEXT, scale_factor=1.25), Indicate(rights, color=TEXT, scale_factor=1.25),
                  run_time=0.8)
        self.at("phospholipids")
        top = mem.rows[ROWS[14]]
        pl = lab("phospholipid", 34, YELLOW, weight=BOLD).move_to(P3(-3.4, 2.5))
        pa = arr(P3(-2.2, 2.45), P3(-0.9, 2.95), YELLOW, 5)
        self.play(FadeIn(pl), GrowArrow(pa), run_time=0.6)
        self.at("heads facing the water")
        h = lab("heads", 32, TEXT, weight=BOLD).move_to(P3(-2.9, 0.9))
        ha = arr(P3(-2.2, 0.95), P3(-0.95, 1.1), TEXT, 5)
        self.play(FadeOut(pl), FadeOut(pa), FadeIn(h), GrowArrow(ha), run_time=0.6)
        self.at("oily tails")
        tails = lab("oily tails", 32, TAILC, weight=BOLD).move_to(P3(-2.6, -0.5))
        ta = arr(P3(-1.55, -0.5), P3(-0.2, -0.5), TAILC, 5)
        self.play(FadeIn(tails), GrowArrow(ta), run_time=0.6)
        self.at("small oxygen molecules")
        self.play(FadeOut(h), FadeOut(ha), FadeOut(tails), FadeOut(ta), run_time=0.5)
        ox = Passers(O2, [2.2, 0.35, -1.0, -2.4, 3.0, -0.2], -3.4, 1.9, ring=True, r=0.13, seed=4)
        ox.v = 1.7
        for i, d in enumerate(ox.submobjects):
            ox.x[i] = -3.8 + 0.35 * i
        self.add(ox)
        ol = lab("oxygen", 34, TEXT, weight=BOLD).move_to(P3(-4.6, 3.1))
        self.play(FadeIn(ol), run_time=0.4)
        self.finish()


# -----------------------------------------------------------------------------------------------------
class S06Ions(SpokenScene):
    def construct(self):
        L, R = water_sides()
        mem = make_membrane()
        self.add(L, R, mem)
        na = Swarm(NA, 8, (-6.2, -0.82, -3.4, 3.4), sig=1.7, r=0.13, seed=21)
        cl = Swarm(CL, 8, (-6.2, -0.82, -3.4, 3.4), sig=1.7, r=0.13, seed=22)
        na.op.set_value(0)
        cl.op.set_value(0)
        self.add(na, cl)
        self.play(na.op.animate.set_value(1), cl.op.animate.set_value(1), run_time=0.8)
        self.at("sodium")
        lg = legend([(NA, "Na+"), (CL, "Cl-")], P3(-4.6, 3.35))
        self.play(FadeIn(lg), run_time=0.5)
        self.at("bounce off")
        bo = lab("bounce off", 32, RED, weight=BOLD).move_to(P3(-2.7, 1.0))
        self.play(FadeIn(bo), run_time=0.4)
        self.at("they cross mainly through proteins", lead=0.8)
        self.play(FadeOut(bo), run_time=0.3)
        self.at("they cross mainly through proteins")
        bl = blocks()
        rowsA = [mem.rows[y] for y in ROWS if abs(y - YA) < 0.7]
        rowsB = [mem.rows[y] for y in ROWS if abs(y - YB_) < 0.7]
        self.play(*[FadeOut(g) for g in rowsA + rowsB], *[FadeIn(b) for b in bl], run_time=1.0)
        self.add(*bl)
        ion = Passers(NA, [YB_], -2.6, 1.0, r=0.13, seed=5)
        ion2 = Passers(CL, [YB_ + 0.22], -3.9, 1.0, r=0.13, seed=6)
        self.add(ion, ion2)
        self.at("proteins")
        pl = lab("protein", 34, PROT, weight=BOLD).move_to(P3(2.6, -2.75))
        self.play(FadeIn(pl), run_time=0.5)
        self.at("water crosses")
        wat = Passers(WATER, [YA - 0.3, YA, YA + 0.3, YA - 0.15, YA + 0.15], -3.2, 1.7, loop=(-3.4, 3.4), r=0.09, seed=8)
        self.add(wat)
        self.at("protein water channels")
        wl = lab("water channel", 34, WATER, weight=BOLD).move_to(P3(2.9, 2.75))
        self.play(FadeIn(wl), run_time=0.5)
        self.at("selectively permeable")
        sp = lab("selectively permeable", 36, GOLD, weight=BOLD).move_to(P3(3.85, -0.4))
        self.play(FadeOut(pl), FadeOut(wl), FadeIn(sp, shift=UP * 0.15), run_time=0.8)
        self.finish()


# -----------------------------------------------------------------------------------------------------
def build_world(scene, lL, lR, salt=True, mem_in=True):
    tk = tanks(lL, lR)
    ws = water_swarm(lL, lR)
    objs = [tk, ws]
    mem = make_membrane(prot=True, thin=True)
    objs.append(mem)
    na = cl = None
    if salt:
        na, cl = salt_swarms(lL)
        objs += [na, cl]
    scene.add(*objs)
    return tk, ws, mem, na, cl


def cross_arrows(color=WATER, left=True, right=True, big=None):
    g = VGroup()
    if right:
        g.add(arr(P3(-1.5, -1.0), P3(1.5, -1.0), color, 8))
    if left:
        g.add(arr(P3(1.5, -2.0), P3(-1.5, -2.0), color, 8))
    return g


class S07Tanks(SpokenScene):
    def construct(self):
        mem = make_membrane(prot=True)
        sL, sR = water_sides()
        self.add(sL, sR, mem)
        lL, lR = ValueTracker(0.2), ValueTracker(0.2)
        tk = tanks(lL, lR)
        ws = water_swarm(lL, lR)
        ws.op.set_value(0)
        self.add(ws)
        thin = make_membrane(prot=True, thin=True)
        self.at("now join two tanks")
        self.play(Transform(mem, thin), FadeIn(tk), ws.op.animate.set_value(1), sL.op.animate.set_value(0),
                  sR.op.animate.set_value(0), run_time=2.0)
        self.at("pure water")
        pw = VGroup(lab("pure water", 32, WATER, weight=BOLD).move_to(P3(-3.0, 2.4)),
                    lab("pure water", 32, WATER, weight=BOLD).move_to(P3(3.0, 2.4)))
        self.play(FadeIn(pw), run_time=0.5)
        self.at("same level")
        lv = DashedLine(P3(XL0, 0.2), P3(XR1, 0.2), color=TEXT, stroke_width=4, dash_length=0.2)
        lt = lab("same level", 32, TEXT, weight=BOLD).move_to(P3(-3.0, 3.3))
        self.play(Create(lv), FadeIn(lt), run_time=0.9)
        self.at("water crosses both ways")
        cnt = Counter("water per second (schematic)", lambda: (20, 20))
        a1 = arr(P3(-1.4, -0.9), P3(1.4, -0.9), WATER, 9)
        a2 = arr(P3(1.4, -1.5), P3(-1.4, -1.5), WATER, 9)
        show_counter(self, cnt, 0.01)
        self.play(GrowArrow(a1), GrowArrow(a2), FadeOut(lt), run_time=0.9)
        self.at("stir salt")
        self.play(FadeOut(a1), FadeOut(a2), FadeOut(lv), FadeOut(pw[0]), run_time=0.5)
        spoon = VGroup(Ellipse(width=0.9, height=0.5, color=GREY, fill_opacity=1, fill_color=GREY),
                       Line(P3(0.4, 0.0), P3(2.0, 1.2), color=GREY, stroke_width=10)).move_to(P3(-3.3, 2.0))
        self.play(FadeIn(spoon), run_time=0.4)
        na, cl = salt_swarms(lL)
        na.op.set_value(0)
        cl.op.set_value(0)
        self.add(na, cl)
        self.play(Rotate(spoon, angle=0.5, about_point=P3(-3.3, 2.0)), na.op.animate.set_value(1),
                  cl.op.animate.set_value(1), run_time=1.2)
        lg = legend([(NA, "Na+"), (CL, "Cl-")], P3(-3.0, 3.35))
        self.play(FadeOut(spoon), FadeIn(lg), run_time=0.5)
        self.at("the salt cannot cross")
        cc = lab("cannot cross", 34, RED, weight=BOLD).move_to(P3(-3.0, 2.35))
        self.play(FadeIn(cc, shift=UP * 0.1), run_time=0.5)
        self.finish()


# -----------------------------------------------------------------------------------------------------
class S08Predict(SpokenScene):
    def construct(self):
        lL, lR = ValueTracker(0.2), ValueTracker(0.2)
        tk, ws, mem, na, cl = build_world(self, lL, lR)
        pw = lab("pure water", 32, WATER, weight=BOLD).move_to(P3(3.0, 2.4))
        lg = legend([(NA, "Na+"), (CL, "Cl-")], P3(-3.0, 2.4))
        self.add(pw, lg)
        a1 = arr(P3(-1.4, -0.9), P3(1.4, -0.9), WATER, 9)
        self.at("water can cross")
        self.play(GrowArrow(a1), run_time=0.7)
        self.at("salt cannot")
        x1 = VGroup(Line(P3(-0.9, -1.3), P3(-0.5, -0.9), color=RED, stroke_width=9), Line(P3(-0.9, -0.9), P3(-0.5, -1.3), color=RED, stroke_width=9)).move_to(P3(-1.0, -1.4))
        self.play(FadeOut(a1), FadeIn(x1), run_time=0.5)
        self.at("which tank's")
        self.play(FadeOut(x1), FadeOut(pw), FadeOut(lg), run_time=0.4)
        title = lab("Pause and predict", 40, GOLD, weight=BOLD).move_to(P3(0, 3.4))
        up_l = VGroup(arr(P3(-3.0, 1.9), P3(-3.0, 2.5), TEXT, 8), lab("left rises?", 30, TEXT, weight=BOLD).move_to(P3(-3.0, 2.8)))
        up_r = VGroup(arr(P3(3.0, 1.9), P3(3.0, 2.5), TEXT, 8), lab("right rises?", 30, TEXT, weight=BOLD).move_to(P3(3.0, 2.8)))
        title.move_to(P3(0, 3.4))
        up_l[1].move_to(P3(-3.0, 2.8))
        up_r[1].move_to(P3(3.0, 2.8))
        self.play(FadeIn(title), run_time=0.5)
        self.play(FadeIn(up_l), FadeIn(up_r), run_time=0.6)
        self.at("the salty one")
        self.play(up_l[1].animate.set_color(NA), up_l[0].animate.set_color(NA), run_time=0.4)
        self.at("the pure one")
        self.play(up_l[1].animate.set_color(TEXT), up_l[0].animate.set_color(TEXT),
                  up_r[1].animate.set_color(WATER), up_r[0].animate.set_color(WATER), run_time=0.4)
        self.at("pause the film")
        self.play(Indicate(title, color=GOLD, scale_factor=1.12), run_time=1.0)
        self.finish()


class S09Pause(NarratedScene):
    def construct(self):
        lL, lR = ValueTracker(0.2), ValueTracker(0.2)
        tk, ws, mem, na, cl = build_world(self, lL, lR)
        title = lab("Pause and predict", 40, GOLD, weight=BOLD).move_to(P3(0, 3.4))
        up_l = VGroup(arr(P3(-3.0, 1.9), P3(-3.0, 2.5), TEXT, 8), lab("left rises?", 30, TEXT, weight=BOLD).move_to(P3(-3.0, 2.8)))
        up_r = VGroup(arr(P3(3.0, 1.9), P3(3.0, 2.5), TEXT, 8), lab("right rises?", 30, TEXT, weight=BOLD).move_to(P3(3.0, 2.8)))
        self.add(title, up_l, up_r)
        self.wait(2.2)
        self.play(Indicate(up_l, color=NA, scale_factor=1.1), run_time=1.0)
        self.play(Indicate(up_r, color=WATER, scale_factor=1.1), run_time=1.0)
        self.finish()


# -----------------------------------------------------------------------------------------------------
LEVEL_L, LEVEL_R = 0.75, -0.35


class S10Reveal(SpokenScene):
    def construct(self):
        lL, lR = ValueTracker(0.2), ValueTracker(0.2)
        tk, ws, mem, na, cl = build_world(self, lL, lR)
        title = lab("Pause and predict", 40, GOLD, weight=BOLD).move_to(P3(0, 3.4))
        self.add(title)
        self.play(FadeOut(title), lL.animate.set_value(LEVEL_L), lR.animate.set_value(LEVEL_R), run_time=1.5)
        self.at("the salty side")
        sl = lab("the salty side", 34, NA, weight=BOLD).move_to(P3(-3.0, 2.6))
        self.play(FadeIn(sl), run_time=0.5)
        self.at("look closely")
        cL, cR = P3(-3.05, -0.7), P3(3.05, -0.7)
        cir_l = Circle(radius=1.95, stroke_color=TEXT, stroke_width=6, fill_color=BG, fill_opacity=0.96).move_to(cL).set_z_index(5)
        cir_r = cir_l.copy().move_to(cR)
        mk = lambda col, n, c, r, sd: Swarm(col, n, (c[0] - 1.9, c[0] + 1.9, c[1] - 1.9, c[1] + 1.9), sig=1.0, r=r, seed=sd,
                                            constrain=circ_in(c[:2], 1.65),
                                            accept=lambda x, y: np.hypot(x - c[0], y - c[1]) < 1.65)
        wr, wl, sn, sc = mk(WATER, 24, cR, 0.14, 31), mk(WATER, 16, cL, 0.14, 32), mk(NA, 5, cL, 0.16, 33), mk(CL, 3, cL, 0.16, 34)
        for s_ in (wr, wl, sn, sc):
            s_.set_z_index(6)
            s_.op.set_value(0)
        self.add(wr, wl, sn, sc)
        self.play(FadeOut(sl), ws.op.animate.set_value(0.2), na.op.animate.set_value(0.2), cl.op.animate.set_value(0.2),
                  GrowFromCenter(cir_l), GrowFromCenter(cir_r), run_time=0.9)
        self.play(*[s_.op.animate.set_value(1) for s_ in (wr, wl, sn, sc)], run_time=0.5)
        self.at("one drop from each side")
        tl = lab("left", 30, NA, weight=BOLD).move_to(P3(-3.05, 1.55)).set_z_index(7)
        tr = lab("right", 30, WATER, weight=BOLD).move_to(P3(3.05, 1.55)).set_z_index(7)
        self.play(FadeIn(tl), FadeIn(tr), run_time=0.5)
        self.at("on the left")
        self.play(Indicate(sn, color=NA, scale_factor=1.5), Indicate(sc, color=CL, scale_factor=1.5), run_time=1.0)
        self.at("not water")
        self.play(Indicate(sn, color=NA, scale_factor=1.5), Indicate(sc, color=CL, scale_factor=1.5), run_time=1.0)
        self.at("fewer water molecules")
        nl = lab("16 water molecules", 30, WATER, weight=BOLD).move_to(P3(-3.05, -3.05))
        nr = lab("24 water molecules", 30, WATER, weight=BOLD).move_to(P3(3.05, -3.05))
        sch = lab("schematic", 26, TEXT).move_to(P3(0, 2.35))
        nl.set_z_index(60); nr.set_z_index(60); sch.set_z_index(60)
        self.play(FadeIn(nl, shift=UP * 0.1), FadeIn(nr, shift=UP * 0.1), FadeIn(sch), run_time=0.8)
        self.finish()


# -----------------------------------------------------------------------------------------------------
def world_after(scene, salt=True):
    lL, lR = ValueTracker(LEVEL_L), ValueTracker(LEVEL_R)
    tk, ws, mem, na, cl = build_world(scene, lL, lR, salt)
    return lL, lR, tk, ws, mem, na, cl


class S11Why(SpokenScene):
    def construct(self):
        lL, lR, tk, ws, mem, na, cl = world_after(self)
        self.at("more water molecules reach")
        big = arr(P3(4.6, -1.4), P3(0.5, -1.4), WATER, 16)
        self.play(GrowArrow(big), run_time=1.2)
        self.at("more cross to the left")
        rates = [(17, 20)]
        cnt = Counter("water per second (schematic)", lambda: rates[0])
        small = arr(P3(-1.4, -2.4), P3(-0.5, -2.4), WATER, 5)
        show_counter(self, cnt, 0.01)
        self.play(big.animate.put_start_and_end_on(P3(4.6, -1.4), P3(-2.2, -1.4)), run_time=1.2)
        self.at("water is running down")
        ramp = Polygon(P3(-5.5, 1.9), P3(5.5, 1.9), P3(5.5, 2.2), color=WATER, fill_color=WATER, fill_opacity=0.35, stroke_width=4)
        gl = lab("water's own gradient", 32, WATER, weight=BOLD).move_to(P3(-3.0, 3.3))
        self.play(FadeOut(big), FadeIn(ramp), FadeIn(gl), run_time=0.6)
        ball = Dot(P3(5.1, 2.34), radius=0.15, color=WATER).set_stroke(TEXT, 3)
        self.add(ball)
        self.play(MoveAlongPath(ball, Line(P3(5.1, 2.34), P3(-5.1, 2.07))), rate_func=rate_functions.ease_in_sine, run_time=2.6)
        self.at("that net movement")
        osm = lab("osmosis", 44, GOLD, weight=BOLD).move_to(P3(-3.0, 3.3))
        self.play(FadeOut(gl), FadeIn(osm, shift=UP * 0.1), run_time=0.6)
        self.play(Indicate(osm, color=GOLD, scale_factor=1.15), run_time=0.8)
        self.finish()


# -----------------------------------------------------------------------------------------------------
class S12Stop(SpokenScene):
    def construct(self):
        lL, lR, tk, ws, mem, na, cl = world_after(self)
        push = ValueTracker(0.0)
        cnt = Counter("water per second (schematic)",
                      lambda: (int(round(17 + 3 * push.get_value())), 20))
        self.add(cnt)
        self.at("does the left tank rise forever")
        up = arr(P3(-3.0, 0.95), P3(-3.0, 1.75), TEXT, 9)
        q = lab("forever?", 38, GOLD, weight=BOLD).move_to(P3(-3.0, 2.5))
        self.play(GrowArrow(up), FadeIn(q), run_time=0.8)
        self.play(up.animate.shift(UP * 0.2), run_time=0.8)
        self.at("now")
        no = lab("No", 44, RED, weight=BOLD).move_to(P3(-3.0, 2.5))
        self.play(FadeOut(up), FadeOut(q), FadeIn(no), run_time=0.5)
        self.at("the taller column")
        col = Line(P3(-5.9, LEVEL_L), P3(-5.9, LEVEL_R), color=TEXT, stroke_width=5)
        self.play(FadeOut(no), run_time=0.5)
        self.at("presses back")
        down = arr(P3(-3.0, 2.75), P3(-3.0, 1.0), RED, 3)
        pl = lab("push of the taller column", 30, RED, weight=BOLD).move_to(P3(-3.0, 3.4))
        self.play(FadeIn(pl), GrowArrow(down), run_time=0.6)
        self.play(down.animate.set_stroke(width=16), push.animate.set_value(1.0), run_time=2.2)
        self.at("the rise stops")
        cnt.cl, cnt.cr = GREEN, GREEN
        bal = lab("balanced", 34, GREEN, weight=BOLD).move_to(P3(3.5, 2.2))
        self.play(FadeIn(bal), run_time=0.6)
        self.at("balances the difference")
        self.play(Indicate(cnt.box, color=GREEN, scale_factor=1.05), run_time=0.9)
        self.finish()


# -----------------------------------------------------------------------------------------------------
def token(r=0.32):
    c = Circle(radius=r, stroke_color=ATP, stroke_width=5, fill_color=ATP, fill_opacity=0.35)
    t = lab("ATP", int(r * 70), ATP, weight=BOLD).move_to(c)
    return VGroup(c, t)


def slash(center, s=0.4):
    c = np.array([center[0], center[1], 0.0])
    return Line(c + P3(-s, s), c + P3(s, -s), color=RED, stroke_width=9)


class S13Free(SpokenScene):
    def construct(self):
        self.at("nothing in this film")
        big = token(0.7)
        big.move_to(P3(-1.6, 0.9))
        bs = slash(P3(-1.6, 0.9), 0.85)
        ne = lab("no energy spent", 44, TEXT, weight=BOLD).move_to(P3(2.1, 0.9))
        self.play(FadeIn(big), run_time=0.6)
        self.play(Create(bs), FadeIn(ne, shift=LEFT * 0.2), run_time=0.8)
        self.at("die", lead=1.4)
        # small token and label go to the top row
        sm = token(0.28).move_to(P3(-2.0, 3.35))
        sms = slash(P3(-2.0, 3.35), 0.34)
        sml = lab("no energy spent", 32, TEXT, weight=BOLD).move_to(P3(1.0, 3.35))
        self.play(Transform(big, sm), Transform(bs, sms), Transform(ne, sml), run_time=1.0)
        # three downhill ramps
        specs = [(-4.3, DYE, "dye", False), (0.0, O2, "oxygen", True), (4.3, WATER, "water", False)]
        icons = []
        for x, col, name, ring in specs:
            ln = Line(P3(x - 1.6, 2.5), P3(x + 1.6, 0.9), color=GREY, stroke_width=8)
            ball = Dot(P3(x - 1.6, 2.5 + 0.2), radius=0.2, color=col)
            if ring:
                ball.set_stroke(GREY, 3)
            nm = lab(name, 34, col if name != "oxygen" else TEXT, weight=BOLD).move_to(P3(x, 0.4))
            icons.append((ln, ball, nm, x))
        self.at("die")  # "dye" transcribed as "die"
        self.play(FadeIn(icons[0][0]), FadeIn(icons[0][1]), FadeIn(icons[0][2]), run_time=0.4)
        self.at("oxygen")
        self.play(FadeIn(icons[1][0]), FadeIn(icons[1][1]), FadeIn(icons[1][2]), run_time=0.3)
        self.at("and water")
        self.play(FadeIn(icons[2][0]), FadeIn(icons[2][1]), FadeIn(icons[2][2]), run_time=0.3)
        self.at("ran downhill")
        rolls = []
        for ln, ball, nm, x in icons:
            rolls.append(MoveAlongPath(ball, Line(P3(x - 1.6, 2.7), P3(x + 1.6, 1.1))))
        self.play(*rolls, rate_func=rate_functions.ease_in_sine, run_time=2.4)
        self.at("the salt never crossed")
        mem = make_membrane(thin=True).scale(0.5).move_to(P3(-3.6, -1.55))
        na = Swarm(NA, 4, (-5.9, -3.9, -2.9, -0.35), sig=1.5, r=0.12, seed=41)
        cl = Swarm(CL, 4, (-5.9, -3.9, -2.9, -0.35), sig=1.5, r=0.12, seed=42)
        cc = lab("cannot cross", 34, RED, weight=BOLD).move_to(P3(-3.2, -3.4))
        mem.set_opacity(0)
        self.add(mem, na, cl)
        self.play(mem.animate.set_opacity(1), FadeIn(cc), run_time=0.8)
        self.at("moving anything uphill")
        up = Line(P3(1.4, -3.0), P3(5.4, -1.0), color=GREY, stroke_width=8)
        tk = token(0.3).move_to(P3(1.4, -2.65))
        qq = lab("?", 56, GOLD, weight=BOLD).move_to(P3(5.4, -0.4))
        self.play(FadeIn(up), FadeIn(tk), FadeIn(qq), run_time=0.7)
        self.play(tk.animate.move_to(P3(3.2, -1.55)), run_time=2.0)
        self.at("second film's story")
        ul = lab("uphill costs energy", 34, ATP, weight=BOLD).move_to(P3(3.0, -3.2))
        self.play(FadeIn(ul, shift=UP * 0.1), run_time=0.6)
        self.finish()


# -----------------------------------------------------------------------------------------------------
class S14Rule(SpokenScene):
    def construct(self):
        lL, lR, tk, ws, mem, na, cl = world_after(self)
        self.at("so here is the rule")
        rule = lab("The rule", 34, GOLD, weight=BOLD).move_to(P3(-5.2, 3.45))
        self.play(FadeIn(rule), run_time=0.5)
        self.at("with no energy spent")
        l1 = lab("With no energy spent,", 34, TEXT, weight=BOLD).move_to(P3(0.3, 3.4))
        self.play(Write(l1), run_time=1.4)
        self.at("whatever can cross")
        l2 = lab("whatever can cross runs down its own gradient.", 34, TEXT, weight=BOLD).move_to(P3(0, 2.85))
        d1 = arr(P3(-1.6, -1.0), P3(1.6, -1.0), WATER, 8)
        self.play(Write(l2), run_time=2.2)
        self.at("and water runs toward")
        l3 = lab("Water runs toward the particles that cannot cross.", 34, WATER, weight=BOLD).move_to(P3(0, 2.3))
        d2 = arr(P3(4.0, -1.4), P3(-1.0, -1.4), WATER, 14)
        self.play(Write(l3), GrowArrow(d2), run_time=1.4)
        self.at("the dissolved particles that cannot cross")
        box = RoundedRectangle(corner_radius=0.2, width=5.1, height=3.6, stroke_color=NA, stroke_width=6).move_to(P3(-3.0, -1.35)).set_z_index(8)
        self.play(Create(box), run_time=0.9)
        self.play(Indicate(box, color=NA, scale_factor=1.04), run_time=0.9)
        self.finish()


# -----------------------------------------------------------------------------------------------------
class S15End(EndCard):
    LINE = "Whatever can cross runs downhill for free; water runs toward trapped solute."
