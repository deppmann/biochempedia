"""When Inhibition Changes Sign (chapter 2). Chapter 1 look and colour map kept; helpers copied from ../scenes.py.
Then one inhibitory synapse (purple ending, red target) carried through the film (schematic, adult male rat).

COLOR MAP (one colour per concept, whole film)
  BLUE   = touch input        ORANGE = excitatory relay (somatostatin)   PURPLE = inhibitory neuron / signal
  RED    = projection output / behaviour gauge     TEAL = KCC2 / chloride control / reversal marker   GOLD = microglia and BDNF   (TEAL = highlight rings in ch.1)     YELLOW = open question
Every gauge, grid and spike train is schematic; nothing here is a recording.
"""
import numpy as np
from types import SimpleNamespace
from bp_style import *  # noqa: F401,F403

PURPLE = "#B58CD9"
ORANGE = "#F29E4C"


# ------------------------------------------------------------------ building blocks
class Obj(VGroup):
    """A group whose visibility is a tracker (lvl 0..1) so things fade without Transform copies."""

    def __init__(self, *mobs, lvl=1.0, breathe=0.0, phase=0.0):
        super().__init__(*mobs)
        self.lvl = ValueTracker(lvl)
        self.breathe, self.phase, self.tt, self.cur, self._last = breathe, phase, 0.0, 1.0, None
        self.base = [(m, m.get_fill_opacity(), m.get_stroke_opacity()) for m in self.family_members_with_points()]
        self.add_updater(self._upd)
        self._upd(self, 0)

    def _upd(self, m, dt):
        self.tt += dt
        o = float(np.clip(self.lvl.get_value(), 0, 1))
        k = 1.0 + self.breathe * np.sin(2.3 * self.tt + self.phase) if self.breathe else 1.0
        key = round(o * k, 3)
        if key == self._last:
            return
        self._last = key
        for mob, f, s in self.base:
            if f > 0:
                mob.set_fill(opacity=min(1.0, f * o * k))
            if s > 0:
                mob.set_stroke(opacity=min(1.0, s * o))

    def put(self, v):
        self.lvl.set_value(v)
        self._last = None
        self._upd(self, 0)
        return self


class Pulse(Obj):
    def __init__(self, path, color=BLUE, period=2.0, ph=0.0, r=0.24, lvl=0.0):
        core, halo = Dot(radius=r, color=color), Dot(radius=r * 2.3, color=color).set_fill(opacity=0.3)
        super().__init__(halo, core, lvl=lvl)
        self.path, self.period, self.ph = path, period, ph
        self.add_updater(self._move)

    def _move(self, m, dt):
        self.ph += dt / self.period
        self.move_to(self.path.point_from_proportion(self.ph % 1.0))


class Flow(Obj):
    """Little dots running along a path, speed and visibility following a source Obj."""

    def __init__(self, path, color, src, n=3, speed=0.3, r=0.09):
        super().__init__(*[Dot(radius=r, color=color) for _ in range(n)], lvl=0)
        self.path, self.src, self.n, self.speed, self.fp, self.gain = path, src, n, speed, 0.0, 1.0
        self.add_updater(self._run)

    def _upd(self, m, dt):
        if hasattr(self, 'gain'):
            self.lvl.set_value(self.src.lvl.get_value() * self.gain)
        super()._upd(m, dt)

    def _run(self, m, dt):
        self.fp += dt * self.speed * max(self.src.lvl.get_value(), 0.0)
        for i, d in enumerate(self.submobjects):
            d.move_to(self.path.point_from_proportion((self.fp + i / self.n) % 1.0))


class Gauge(Obj):
    def __init__(self, x, level=0.85, y0=-2.3, h=4.2, w=1.0, color=RED, lvl=0.0, tremble=0.035, ph=0.0):
        frame = Rectangle(width=w, height=h, stroke_color=TEXT, stroke_width=3).move_to([x, y0 + h / 2, 0])
        fbar = Rectangle(width=w - 0.16, height=h - 0.16, stroke_width=0, fill_color=color, fill_opacity=0.9)
        super().__init__(frame, fbar, lvl=lvl)
        self.val, self.gx, self.gy0, self.gh, self.tr, self.ph, self.gt, self.fbar = ValueTracker(level), x, y0, h, tremble, ph, 0.0, fbar
        self.add_updater(self._fill)
        self._fill(self, 0)

    def _fill(self, m, dt):
        self.gt += dt
        v = float(np.clip(self.val.get_value() + self.tr * np.sin(self.gt * 8 + self.ph), 0.02, 1))
        hh = (self.gh - 0.16) * v
        self.fbar.stretch_to_fit_height(hh)
        self.fbar.move_to([self.gx, self.gy0 + 0.08 + hh / 2, 0])


class Inh(Obj):
    """Inhibitory line with a T-bar from a moving source point to a fixed target."""

    def __init__(self, getp, dst, color=PURPLE, w=6):
        line, bar = Line(LEFT, RIGHT, color=color, stroke_width=w), Line(LEFT, RIGHT, color=color, stroke_width=w + 3)
        super().__init__(line, bar, lvl=0)
        self.getp, self.dst, self.line, self.bar = getp, np.array(dst, float), line, bar
        self.add_updater(self._geo)
        self._geo(self, 0)

    def _geo(self, m, dt):
        a = np.array(self.getp(), float)
        d = self.dst - a
        d = d / max(np.linalg.norm(d), 1e-6)
        perp = np.array([-d[1], d[0], 0])
        self.line.put_start_and_end_on(a, self.dst - d * 0.05)
        self.bar.put_start_and_end_on(self.dst + perp * 0.36, self.dst - perp * 0.36)


class Orbiter(Obj):
    def __init__(self, text, color, theta, center, rx, ry, size=30):
        t = T(text, size=size, color=color)
        super().__init__(t, lvl=0)
        self.theta, self.center, self.rx, self.ry, self.target = theta, np.array(center, float), rx, ry, None
        self.move_to(self.center + np.array([rx * np.cos(theta), ry * np.sin(theta), 0]))
        self.add_updater(self._orb)

    def _orb(self, m, dt):
        if self.target is None:
            self.theta += dt * 0.42
            goal = self.center + np.array([self.rx * np.cos(self.theta), self.ry * np.sin(self.theta), 0])
            self.move_to(goal)
        else:
            self.move_to(self.get_center() + (self.target - self.get_center()) * min(1.0, dt * 3.5))


def cell(pos, color, r, lvl=1.0, breathe=0.07, phase=0.0):
    c = Circle(radius=r, stroke_color=color, stroke_width=5, fill_color=color, fill_opacity=0.42).move_to(pos)
    n = Dot(radius=r * 0.3, color=color).move_to(pos).set_fill(opacity=0.85)
    return Obj(c, n, lvl=lvl, breathe=breathe, phase=phase)


def txt(s, pos, color=TEXT, size=28, lvl=0.0, left=False):
    t = T(s, size=size, color=color)
    if left:
        t.move_to(np.array(pos, float), aligned_edge=LEFT)
    else:
        t.move_to(np.array(pos, float))
    return Obj(t, lvl=lvl)


def chipo(s, pos, color, size=30, lvl=0.0):
    c = chip(s, color, size=size)
    c.move_to(np.array(pos, float))
    return Obj(c, lvl=lvl)


def Lv(objs, v=1.0):
    objs = objs if isinstance(objs, (list, tuple)) else [objs]
    return [o.lvl.animate.set_value(v) for o in objs]


def mv(obj, to=None, scale=None, t=1.0):
    start, s0 = obj.get_center().copy(), obj.cur
    to = start if to is None else np.array(to, float)
    sc = s0 if scale is None else scale

    def f(m, a):
        k = s0 + (sc - s0) * a
        m.scale(k / m.cur)
        m.cur = k
        m.move_to(start + (to - start) * a)
    return UpdateFromAlphaFunc(obj, f, run_time=t)


def gv(g, v):
    return g.val.animate.set_value(v)


# ------------------------------------------------------------------ the one world
SKIN = np.array([-5.45, -2.45, 0])
F0, F1 = np.array([-4.75, -2.2, 0]), np.array([-1.85, -0.55, 0])
OP, PP, RP = np.array([-1.4, -0.3, 0]), np.array([-4.2, 0.9, 0]), np.array([2.6, 0.2, 0])
EX = [(-0.9, -1.95), (0.55, -0.95), (0.65, 0.85), (-0.5, 1.95), (1.45, 1.75)]
GX = 5.3


def unit(v):
    v = np.array(v, float)
    return v / np.linalg.norm(v)


def world():
    w = SimpleNamespace()
    w.panel = Obj(RoundedRectangle(corner_radius=0.25, width=13.2, height=6.55, stroke_color=GREY, stroke_width=3).move_to([0, -0.275, 0]), lvl=0)
    w.tag = txt("mouse circuit, schematic", [-6.6, 3.35, 0], TEXT, 26, lvl=0, left=True)
    w.tagslice = txt("mouse slice", [-6.6, 3.35, 0], TEXT, 26, lvl=0, left=True)
    w.skin = Obj(RoundedRectangle(corner_radius=0.15, width=1.5, height=0.62, stroke_color=BLUE, stroke_width=4, fill_color=BLUE, fill_opacity=0.2).move_to(SKIN),
                 T("skin", 28, BLUE).move_to(SKIN), lvl=0)
    w.fiber2 = Obj(Line(F0, F1, color=BLUE, stroke_width=16).set_stroke(opacity=0.35), lvl=0)
    w.fiber = Obj(Line(F0, F1, color=BLUE, stroke_width=10), lvl=0)
    w.pulse = Pulse(Line(F0, F1))
    w.pulse2 = Pulse(Line(F0, F1), ph=0.5)
    w.O = cell(OP, ORANGE, 0.65, lvl=0)
    w.Olab = txt("relay", [-1.95, 0.85, 0], ORANGE)
    w.P = cell(PP, PURPLE, 0.58, lvl=0, phase=1.3)
    w.Plab = txt("inhibitory", [-4.2, 1.85, 0], PURPLE)
    w.Plab2 = txt("dynorphin\nlineage", [-4.2, 2.0, 0], PURPLE)
    bp = np.array([-3.6, -1.1, 0])
    w.brake = Obj(Line([-4.15, 0.43, 0], bp, color=PURPLE, stroke_width=6),
                  Line(bp + [-0.42, 0, 0], bp + [0.42, 0, 0], color=PURPLE, stroke_width=12), lvl=0)
    w.R = cell(RP, RED, 0.78, lvl=0, phase=2.0)
    w.Rlab = txt("output", [2.6, 1.4, 0], RED)
    w.OR = Obj(Line(OP + [0.7, 0, 0], RP + [-0.85, 0.05, 0], color=ORANGE, stroke_width=9), lvl=0)
    w.E, w.EL = [], []
    for i, e in enumerate(EX):
        e = np.array([e[0], e[1], 0])
        w.E.append(cell(e, ORANGE, 0.44, lvl=0, phase=i))
        d = unit(RP - e)
        w.EL.append(Obj(Line(e + d * 0.46, RP - d * 0.82, color=ORANGE, stroke_width=5), lvl=0))
    w.route = Obj(Arrow(RP + [0.85, 0, 0], [GX - 0.55, 0.2, 0], buff=0, color=RED, stroke_width=10, tip_length=0.28), lvl=0)
    w.gauge = Gauge(GX, 0.85)
    w.glab = txt("nocifensive\nbehaviour", [GX, 2.4, 0], RED, 28)
    # flows (transmitter dots) that follow their source line
    w.fOR = Flow(Line(OP + [0.7, 0, 0], RP + [-0.85, 0.05, 0]), ORANGE, w.OR)
    w.fE = [Flow(Line(np.array([e[0], e[1], 0]), RP), ORANGE, w.EL[i], n=2, speed=0.25) for i, e in enumerate(EX)]
    w.fR = Flow(Line(RP + [0.85, 0, 0], [GX - 0.55, 0.2, 0]), RED, w.route, n=2, speed=0.3)
    w.fB = Flow(Line([-4.15, 0.43, 0], bp), PURPLE, w.brake, n=2, speed=0.3)
    # per-scene extras
    w.sst = txt("somatostatin", [-1.4, 1.3, 0], ORANGE)
    w.ghost = Obj(DashedVMobject(Circle(radius=0.5, color=ORANGE, stroke_width=4).move_to(OP), num_dashes=16), lvl=0)
    w.card = chipo("ablation: population removed", [1.0, -2.8, 0], YELLOW, 28)
    w.bypass = Obj(DashedVMobject(ArcBetweenPoints(np.array([-3.4, -1.9, 0]), np.array([2.2, -0.75, 0]), angle=0.55).set_stroke(YELLOW, 5), num_dashes=22), lvl=0)
    w.q = txt("?", [2.9, -1.5, 0], YELLOW, 54)
    w.sup = txt("superficial", [1.2, 2.65, 0], TEXT)
    w.deep = txt("deep", [0.9, -2.9, 0], TEXT)
    w.afflab = txt("large afferents", [-2.5, -2.75, 0], BLUE)
    w.afflab2 = txt("Aβ input", [-2.5, -2.75, 0], BLUE)
    w.same = chipo("same input", [-5.2, -0.8, 0], BLUE, 28)
    w.pghost = Obj(DashedVMobject(Circle(radius=0.45, color=PURPLE, stroke_width=4).move_to(PP), num_dashes=14),
                   Line(PP + [-0.3, -0.3, 0], PP + [0.3, 0.3, 0], color=RED, stroke_width=7),
                   Line(PP + [-0.3, 0.3, 0], PP + [0.3, -0.3, 0], color=RED, stroke_width=7), lvl=0)
    w.dh = txt("dorsal horn", [-3.0, 2.55, 0], TEXT)
    return w


def circuit_items(w):
    return [w.panel, w.tag, w.tagslice, w.fiber2, w.fiber, w.brake, w.OR, *w.EL, w.route, w.bypass, w.ghost, w.pghost,
            w.skin, w.O, w.P, *w.E, w.R, w.gauge, *w.fE, w.fOR, w.fR, w.fB, w.pulse, w.pulse2,
            w.Olab, w.Plab, w.Plab2, w.Rlab, w.glab, w.sst, w.card, w.q, w.sup, w.deep, w.afflab, w.afflab2, w.same, w.dh]


def hook_end(w):
    for o in [w.panel, w.tag, w.skin, w.fiber, w.pulse, w.pulse2, w.O, w.OR, w.Olab, w.P, w.Plab, w.brake, w.R, w.Rlab, w.route]:
        o.put(1)


def s02_end(w):
    hook_end(w)
    w.O.move_to([-1.4, 2.1, 0])
    w.O.put(0.45)
    w.OR.put(0)
    w.Olab.put(0)
    w.sst.put(1)
    w.ghost.put(1)
    w.card.put(1)
    w.bypass.put(1)
    w.q.put(1)
    w.gauge.put(1)
    w.gauge.val.set_value(0.25)
    w.glab.put(1)
    w.R.put(0.5)
    w.route.put(0.5)


def s03_end(w):
    hook_end(w)
    for o in [w.P, w.brake, w.Plab, w.fB]:
        o.put(0)
    w.Plab2.put(0)
    for o in w.E + w.EL:
        o.put(1)
    for o in [w.sup, w.deep, w.afflab, w.fiber2, w.same]:
        o.put(1)


def s04_end(w):
    s03_end(w)
    for o in w.E + w.EL:
        o.put(0.25)
    w.R.put(0.3)
    w.route.put(0.3)
    w.Rlab.put(0)
    w.Olab.put(0)
    w.tag.put(0)
    w.tagslice.put(1)
    w.afflab.put(0)
    w.afflab2.put(1)
    w.pghost.put(1)
    ch = SimpleNamespace(fewer=chipo("fewer", [5.15, 2.2, 0], TEAL, 32, 1), same=chipo("the same", [5.15, 0.95, 0], TEAL, 32, 1),
                         more=chipo("more", [5.15, -0.4, 0], TEAL, 32, 1))
    return ch


class Glow:
    def setup(self):
        super().setup()
        g = Rectangle(width=15, height=8.5, stroke_width=0, fill_color=TEAL, fill_opacity=0.05)
        g.tt = 0.0

        def br(m, dt):
            m.tt += dt
            m.set_fill(opacity=0.045 + 0.03 * np.sin(m.tt * 2.4))
        g.add_updater(br)
        g.set_z_index(-20)
        self.add(g)

    def ripple(self, pos, color, r=0.4, t=0.8):
        ring = Circle(radius=r, stroke_color=color, stroke_width=6).move_to(np.array(pos, float))
        ring.age = 0.0

        def grow(m, dt):
            m.age += dt
            a = m.age / t
            if a >= 1:
                m.set_stroke(opacity=0)
                return
            m.become(Circle(radius=r * (1 + 1.1 * a), stroke_color=color, stroke_width=5).move_to(np.array(pos, float)).set_stroke(opacity=0.7 * (1 - a)))
            m.set_z_index(-0.5)
            m.age = a * t
        ring.add_updater(grow)
        ring.set_z_index(-0.5)
        self.add(ring)


class Base(Glow, SpokenScene):
    pass


class Plain(Glow, NarratedScene):
    pass




# ================================================================== chapter 2: the one synapse world
GOLD_C = GOLD   # microglia and BDNF
CL, CR, CT, CB = -5.9, 2.4, 0.8, -3.6     # red target neuron
RX, CHX = 4.7, -2.0                        # voltage ruler x, anion channel x
KX = [-4.6, -3.4, 0.9, 1.8]                # KCC2 blocks on the membrane
VM0 = -65.0
CUR_Y0, CUR_K = -1.0, 0.08


def Yv(v):
    """Voltage (mV) to screen y: the ruler runs -90 (y -3.3) to -30 (y +3.3)."""
    return (float(v) + 60.0) * 0.11


def smin(v):
    n = int(round(v))
    return ("−" if n < 0 else "+") + str(abs(n))


def put(objs, v=1.0):
    for o in (objs if isinstance(objs, (list, tuple)) else [objs]):
        if hasattr(o, "put"):
            o.put(v)
        else:
            o.lvl.set_value(v)
    return objs


def mtx(s, pos, color=TEXT, size=36, lvl=0.0):
    t = M(s, size=size, color=color)
    t.move_to(np.array(pos, float), aligned_edge=LEFT)
    return Obj(t, lvl=lvl)


class Stream(VGroup):
    """Small dots (or squares) running along a polyline; opacity from own lvl or from a source Obj."""

    def __init__(self, pts, color, n=4, speed=0.3, r=0.09, src=None, gain=1.0, lvl=0.0, square=False):
        mk = (lambda: Square(side_length=r * 2.6, stroke_color=color, stroke_width=3, fill_color=color, fill_opacity=0.8)) if square else (lambda: Dot(radius=r, color=color))
        super().__init__(*[mk() for _ in range(n)])
        self.path = VMobject().set_points_as_corners([np.append(np.array(p, float), 0.0) if len(p) == 2 else np.array(p, float) for p in pts])
        self.n, self.speed, self.src, self.gain, self.fp, self.sq = n, speed, src, gain, 0.0, square
        self.lvl = ValueTracker(lvl)
        self.add_updater(self._run)
        self._run(self, 0)

    def _run(self, m, dt):
        self.fp += dt * self.speed
        l = (self.src.lvl.get_value() * self.gain) if self.src is not None else self.lvl.get_value()
        l = float(np.clip(l, 0, 1))
        for i, d in enumerate(self.submobjects):
            p = (self.fp + i / self.n) % 1.0
            d.move_to(self.path.point_from_proportion(p))
            o = l * min(1.0, 5 * p, 5 * (1 - p))
            d.set_fill(opacity=o * (0.8 if self.sq else 1.0))
            if self.sq:
                d.set_stroke(opacity=o)


# label zones the wandering chloride dots keep out of: current, KCC2 note, shunt, schematic tags
AVOID = [(-2.05, 0.3, CUR_Y0 - 0.45, CUR_Y0 + 0.45), (-5.7, -0.9, -0.65, 0.35), (-4.6, -2.3, -0.95, 0.05),
         (-5.2, -2.6, -2.45, -1.55), (-0.2, 2.6, 0.0, 0.9)]


class ClDots(VGroup):
    """Chloride dots wandering inside a region. The first `base` are always shown; `acc` (0..1) adds the rest."""

    def __init__(self, region, n=18, base=6, seed=3, r=0.13, amp=0.35, lvl=0.0, acc=0.0, color=TEAL):
        super().__init__(*[Dot(radius=r, color=color) for _ in range(n)])
        rng = np.random.RandomState(seed)
        self.reg, self.n, self.base, self.amp = region, n, base, amp
        x0, x1, y0, y1 = region
        self.home = np.stack([rng.uniform(x0, x1, n), rng.uniform(y0, y1, n)], 1)
        self.ph, self.sp = rng.uniform(0, 6.28, (n, 2)), rng.uniform(0.6, 1.4, (n, 2))
        self.lvl, self.acc, self.t = ValueTracker(lvl), ValueTracker(acc), 0.0
        self.add_updater(self._run)
        self._run(self, 0)

    def _run(self, m, dt):
        self.t += dt
        l, a = float(np.clip(self.lvl.get_value(), 0, 1)), float(np.clip(self.acc.get_value(), 0, 1))
        x0, x1, y0, y1 = self.reg
        for i, d in enumerate(self.submobjects):
            x = self.home[i, 0] + self.amp * np.sin(0.9 * self.t * self.sp[i, 0] + self.ph[i, 0])
            y = self.home[i, 1] + 0.85 * self.amp * np.cos(0.8 * self.t * self.sp[i, 1] + self.ph[i, 1])
            x, y = min(max(x, x0), x1), min(max(y, y0), y1)
            for ax0, ax1, ay0, ay1 in AVOID:
                if ax0 < x < ax1 and ay0 < y < ay1:
                    dd = [x - ax0, ax1 - x, y - ay0, ay1 - y]
                    k = dd.index(min(dd))
                    if k == 0: x = ax0
                    elif k == 1: x = ax1
                    elif k == 2: y = ay0
                    else: y = ay1
            d.move_to([x, y, 0])
            vis = 1.0 if i < self.base else float(np.clip(a * (self.n - self.base + 1) - (i - self.base), 0, 1))
            d.set_fill(opacity=l * vis * 0.9)


class Mark(VGroup):
    """A marker on the voltage ruler: a short line at the tracker's voltage plus a label."""

    def __init__(self, v, color, side, text, size=28, numeric=None, lvl=0.0):
        super().__init__()
        self.v, self.lvl, self.num = ValueTracker(v), ValueTracker(lvl), ValueTracker(0)
        self.color, self.side, self.text0, self.size, self.numeric, self.key = color, side, text, size, numeric, None
        self.line = Line(LEFT * 0.5, RIGHT * 0.5, color=color, stroke_width=9)
        self.lab = T(text, size, color)
        self.add(self.line, self.lab)
        self.add_updater(self._u)
        self._u(self, 0)

    def _u(self, m, dt):
        v, l = self.v.get_value(), float(np.clip(self.lvl.get_value(), 0, 1))
        y = Yv(v)
        txt_ = f"{self.numeric} {smin(v)}" if (self.numeric and self.num.get_value() > 0.5) else self.text0
        if txt_ != self.key:
            self.key = txt_
            self.lab.become(T(txt_, self.size, self.color))
        self.line.move_to([RX, y, 0]).set_stroke(opacity=l)
        w = self.lab.width
        self.lab.move_to([RX - 0.65 - w / 2 if self.side == "L" else RX + 0.65 + w / 2, y, 0]).set_opacity(l)


class CurArrow(Arrow):
    """The anion current through the channel: direction and length follow Vm minus E on the ruler."""

    def __init__(self, E, x=CHX, lvl=0.0):
        super().__init__([x, CUR_Y0, 0], [x, CUR_Y0 + 0.5, 0], buff=0, color=YELLOW, stroke_width=10)
        self.E, self.x, self.lvl = E, x, ValueTracker(lvl)
        self.add_updater(self._u)
        self._u(self, 0)

    def _u(self, m, dt):
        d = (VM0 - self.E.v.get_value()) * CUR_K
        if abs(d) < 0.14:
            d = 0.14 * (1 if d >= 0 else -1)
        new = Arrow([self.x, CUR_Y0, 0], [self.x, CUR_Y0 + d, 0], buff=0, color=YELLOW, stroke_width=10,
                    tip_length=min(0.3, 0.55 * abs(d)), max_tip_length_to_length_ratio=1.0)
        new.set_opacity(float(np.clip(self.lvl.get_value(), 0, 1)))
        self.become(new)


def syn():
    w = SimpleNamespace()
    cc = [(CL + CR) / 2, (CT + CB) / 2, 0]
    w.cell = Obj(RoundedRectangle(corner_radius=0.3, width=CR - CL, height=CT - CB, stroke_color=RED, stroke_width=5,
                                  fill_color=RED, fill_opacity=0.22).move_to(cc), lvl=0)
    w.cell.set_z_index(-2)
    w.celllab = txt("target neuron", [-4.1, -3.2, 0], RED, 28)
    w.term = Obj(RoundedRectangle(corner_radius=0.25, width=4.4, height=1.4, stroke_color=PURPLE, stroke_width=5,
                                  fill_color=PURPLE, fill_opacity=0.32).move_to([-2.0, 2.5, 0]), lvl=0)
    w.termlab = txt("inhibitory ending", [-2.0, 2.5, 0], PURPLE, 28)
    w.chan = Obj(Rectangle(width=0.7, height=0.7, stroke_color=PURPLE, stroke_width=5, fill_color=PURPLE, fill_opacity=0.55).move_to([CHX, 0.8, 0]), lvl=0)
    w.chanlab = txt("anion channel", [-0.4, 1.35, 0], PURPLE, 28)
    w.kc = [Obj(Rectangle(width=0.55, height=0.62, stroke_color=TEAL, stroke_width=4, fill_color=TEAL, fill_opacity=0.5).move_to([x, 0.8, 0]), lvl=0) for x in KX]
    w.kclab = txt("KCC2", [-4.0, 1.42, 0], TEAL, 28)
    w.kclab2 = txt("KCC2: not measured here", [-3.3, -0.15, 0], TEAL, 28)
    w.kcf = [Stream([(x, 0.15), (x, 1.15)], TEAL, n=3, speed=0.22, r=0.08, src=w.kc[i], gain=0.9) for i, x in enumerate(KX)]
    w.inf = Stream([(CHX, 1.78), (CHX, 0.05)], TEAL, n=4, speed=0.28)
    w.cl = ClDots((-5.6, 2.0, -2.7, 0.2))
    w.cl.set_z_index(-1)
    w.cllab = txt("chloride: low", [0.5, -3.2, 0], TEAL, 28)
    w.cllab2 = txt("chloride: high", [0.5, -3.2, 0], TEAL, 28)
    w.ruler = Obj(Line([RX, Yv(-90), 0], [RX, Yv(-30), 0], color=TEXT, stroke_width=4),
                  *[Line([RX - 0.18, Yv(v), 0], [RX + 0.18, Yv(v), 0], color=TEXT, stroke_width=3) for v in range(-90, -29, 10)],
                  T("mV", 24, TEXT).move_to([RX, 3.62, 0]), lvl=0)
    w.Vm = Mark(VM0, RED, "R", "Vm", 28)
    w.Em = Mark(-75, TEAL, "L", "E anion", 28, numeric="E")
    w.arr = CurArrow(w.Em)
    w.arrlab = txt("current", [-1.6, CUR_Y0, 0], YELLOW, 28, left=True)
    return w


def syn_items(w):
    return [w.cell, w.celllab, w.term, w.termlab, w.chan, w.chanlab, *w.kc, *w.kcf, w.kclab, w.kclab2, w.inf, w.cl,
            w.cllab, w.cllab2, w.ruler, w.Vm, w.Em, w.arr, w.arrlab]


def state_full(w, E=-75.0, high=False):
    """Everything of the s02 picture shown; E at `E`; chloride low or high."""
    put([w.cell, w.celllab, w.term, w.termlab, w.chan, w.chanlab, *w.kc, w.kclab, w.inf, w.cl, w.ruler, w.Vm, w.Em, w.arr, w.arrlab])
    w.Em.v.set_value(E)
    if high:
        put(w.cllab2)
        w.cl.acc.set_value(1.0)
        for k in w.kc[1:]:
            k.put(0.25)
    else:
        put(w.cllab)


def hide(objs):
    return Lv(objs, 0)


# ------------------------------------------------------------------ icons and cards (s06-s08, s12)
class CountIcon(Obj):
    def __init__(self, cx, cy, s=1.0, lvl=0.0):
        cols = [ORANGE, PURPLE, RED]
        dots = [Dot(radius=0.2 * s, color=cols[c]).move_to([cx + (c - 1) * 0.65 * s, cy + (0.5 - r) * 0.65 * s, 0]) for r in range(2) for c in range(3)]
        super().__init__(*dots, lvl=lvl, breathe=0.12)


class TraceIcon(Obj):
    """A schematic evoked inhibitory event: difference of two exponentials, computed."""

    def __init__(self, cx, cy, s=1.0, lvl=0.0):
        t = np.linspace(0, 1, 60)
        f = np.exp(-t / 0.3) - np.exp(-t / 0.05)
        f = f / f.max()
        pts = [[cx + (ti - 0.5) * 2.6 * s, cy - 0.4 * s + fi * 0.95 * s, 0] for ti, fi in zip(t, f)]
        self.curve = VMobject(color=PURPLE, stroke_width=5).set_points_as_corners(pts)
        base = Line([cx - 1.3 * s, cy - 0.4 * s, 0], [cx + 1.3 * s, cy - 0.4 * s, 0], color=TEXT, stroke_width=3)
        self.dot = Dot(radius=0.11 * s, color=TEXT)
        super().__init__(base, self.curve, self.dot, lvl=lvl)
        self.add_updater(lambda m, dt: self.dot.move_to(self.curve.point_from_proportion((self.tt * 0.35) % 1.0)))


class PatchIcon(Obj):
    """A perforated-patch electrode on a cell, beside a voltage ruler with a teal marker."""

    def __init__(self, cx, cy, s=1.0, lvl=0.0):
        c0 = np.array([cx - 0.75 * s, cy - 0.3 * s, 0])
        cellc = Circle(radius=0.42 * s, stroke_color=RED, stroke_width=4, fill_color=RED, fill_opacity=0.25).move_to(c0)
        a, b = np.array([cx - 1.5 * s, cy + 0.8 * s, 0]), np.array([cx - 1.05 * s, cy + 0.0 * s, 0])
        d = (b - a) / np.linalg.norm(b - a)
        n = np.array([-d[1], d[0], 0])
        pip = Polygon(a + n * 0.17 * s, a - n * 0.17 * s, b - n * 0.04 * s, b + n * 0.04 * s, stroke_color=TEXT, stroke_width=3, fill_color=TEXT, fill_opacity=0.12)
        rx = cx + 1.05 * s
        ruler = [Line([rx, cy - 0.85 * s, 0], [rx, cy + 0.85 * s, 0], color=TEXT, stroke_width=3)] + \
                [Line([rx - 0.1 * s, cy + k * 0.34 * s, 0], [rx + 0.1 * s, cy + k * 0.34 * s, 0], color=TEXT, stroke_width=2) for k in range(-2, 3)]
        self.mk = Line([rx - 0.24 * s, cy, 0], [rx + 0.24 * s, cy, 0], color=TEAL, stroke_width=7)
        self.rx, self.cy0, self.s = rx, cy, s
        super().__init__(cellc, pip, *ruler, self.mk, lvl=lvl)
        self.add_updater(lambda m, dt: self.mk.move_to([self.rx, self.cy0 + 0.4 * self.s * np.sin(0.9 * self.tt), 0]))


CARDX, CARDY = [-4.5, 0.0, 4.5], -1.85


def make_cards():
    names = ["more counting", "evoked output\nrecording", "anion reversal"]
    cards, icons = [], []
    for i, (cx, nm) in enumerate(zip(CARDX, names)):
        box = RoundedRectangle(corner_radius=0.2, width=4.1, height=3.0, stroke_color=TEXT, stroke_width=3, fill_color=TEXT, fill_opacity=0.05).move_to([cx, CARDY, 0])
        cap = T(nm, 28, TEXT, line_spacing=0.8).move_to([cx, CARDY - 0.95, 0])
        cards.append(Obj(box, cap, lvl=0))
        icons.append([CountIcon, TraceIcon, PatchIcon][i](cx, CARDY + 0.5, 1.0))
    return cards, icons


def fm(p):
    p = np.array(p, float)
    return np.array([p[0] * 0.9 - 0.3, p[1] * 0.55 + 1.3, 0])


def mini():
    m = SimpleNamespace()
    F0m, F1m = fm(F0), fm(F1)
    m.fiber = Obj(Line(F0m, F1m, color=BLUE, stroke_width=9), lvl=0)
    m.pulse, m.pulse2 = Pulse(Line(F0m, F1m), r=0.16), Pulse(Line(F0m, F1m), ph=0.5, r=0.16)
    m.O, m.P, m.R = cell(fm(OP), ORANGE, 0.42, lvl=0), cell(fm(PP), PURPLE, 0.4, lvl=0, phase=1.3), cell(fm(RP), RED, 0.5, lvl=0, phase=2.0)
    bpm, pt = fm([-3.6, -1.1, 0]), fm([-4.15, 0.43, 0])
    m.brake = Obj(Line(pt, bpm, color=PURPLE, stroke_width=4), Line(bpm + [-0.22, 0, 0], bpm + [0.22, 0, 0], color=PURPLE, stroke_width=8), lvl=0)
    m.OR = Obj(Line(fm(OP + [0.7, 0, 0]), fm(RP + [-0.85, 0.05, 0]), color=ORANGE, stroke_width=5), lvl=0)
    m.route = Obj(Arrow(fm(RP + [0.85, 0, 0]), fm([4.3, 0.2, 0]), buff=0, color=RED, stroke_width=8, tip_length=0.25), lvl=0)
    m.items = [m.fiber, m.pulse, m.pulse2, m.O, m.P, m.R, m.brake, m.OR, m.route]
    return m


def check(pos, lvl=0.0):
    a = np.array(pos, float)
    return Obj(Line(a, a + [0.2, -0.22, 0], color=TEXT, stroke_width=8), Line(a + [0.2, -0.22, 0], a + [0.62, 0.34, 0], color=TEXT, stroke_width=8), lvl=lvl)


def mini_checks(lvl=0.0):
    return [check([-3.55, 2.1, 0], lvl), check([-3.15, 0.05, 0], lvl), check([1.6, 2.2, 0], lvl)]


def pipette_poly(a, b, w0=0.28, w1=0.06):
    a, b = np.array(a, float), np.array(b, float)
    d = (b - a) / np.linalg.norm(b - a)
    n = np.array([-d[1], d[0], 0])
    return Polygon(a + n * w0, a - n * w0, b - n * w1, b + n * w1, stroke_color=TEXT, stroke_width=4, fill_color=TEXT, fill_opacity=0.12)


# ------------------------------------------------------------------ s00 .. s13
class S00Hook(Base):
    def construct(self):
        w = world()
        tag = txt("mechanism schematic", [-6.6, 3.35, 0], TEXT, 26, left=True)
        ck = [check([-3.3, 1.55, 0]), check([-3.05, -0.95, 0]), check([3.45, 0.95, 0])]
        self.add(*circuit_items(w), tag, *ck)
        base = [w.panel, w.skin, w.fiber, w.pulse, w.pulse2, w.O, w.OR, w.Olab, w.P, w.Plab, w.brake, w.R, w.Rlab, w.route]
        self.play(*Lv([*base, tag]), run_time=1.2)
        self.ripple(SKIN, BLUE, 0.5, 1.2)
        self.at("gatekeeper")
        self.ripple([-3.6, -1.1, 0], PURPLE, 0.4, 1.0)
        self.at("purple inhibitory")
        self.ripple(PP, PURPLE, 0.6, 1.0)
        self.play(*Lv(ck[0]), run_time=0.5)
        self.at("its ending")
        self.ripple([-3.6, -1.1, 0], PURPLE, 0.4, 1.0)
        self.play(*Lv(ck[1]), run_time=0.5)
        self.at("red target")
        self.ripple(RP, RED, 0.7, 1.0)
        self.play(*Lv(ck[2]), run_time=0.5)
        self.at("this time")
        self.play(*Lv([*ck, w.panel, w.skin, w.fiber, w.O, w.OR, w.Olab, w.P, w.Plab, w.brake, w.Rlab, w.route], 0.0), run_time=1.0)
        self.at("inside the target")
        self.play(mv(w.R, [1.2, 0.0, 0], 2.1, t=1.8), run_time=1.8)
        self.ripple([1.2, 0.0, 0], RED, 1.2, 1.4)
        self.finish()


class S01Title(TitleCard):
    LESSON = "Spinal Circuits That Gate Pain"
    TITLE = "When Inhibition Changes Sign"


class S02Normal(Base):
    def construct(self):
        w = syn()
        self.add(*syn_items(w))
        self.play(*Lv([w.cell, w.celllab]), run_time=0.8)
        self.play(*Lv([w.term, w.termlab]), run_time=0.8)
        self.at("channels")
        self.play(*Lv([w.chan, w.chanlab]), run_time=0.7)
        self.at("chloride")
        self.play(*Lv(w.inf), run_time=0.8)
        self.at("its current")
        self.play(*Lv(w.ruler), run_time=0.8)
        self.at("membrane potential")
        self.play(*Lv(w.Vm), run_time=0.7)
        self.ripple([RX, Yv(VM0), 0], RED, 0.35, 0.9)
        self.at("anion reversal")
        self.play(*Lv(w.Em), run_time=0.7)
        self.ripple([RX, Yv(-75), 0], TEAL, 0.35, 0.9)
        self.at("reversal potential")
        self.play(*Lv([w.arr, w.arrlab]), run_time=0.9)
        self.at("tlkcc2", lead=1.2)
        self.play(*Lv(w.kc), run_time=0.8)
        self.at("tlkcc2")
        self.play(*Lv(w.kclab), run_time=0.5)
        self.at("intracellular")
        self.play(*Lv(w.cl), run_time=0.9)
        self.at("low")
        self.play(*Lv(w.cllab), run_time=0.6)
        self.finish()


class S03Shift(Base):
    def construct(self):
        w = syn()
        tag = txt("adult male rat, lamina I slices", [-6.6, 3.55, 0], TEXT, 24, left=True)
        state_full(w)
        self.add(*syn_items(w), tag)
        self.play(*Lv(tag), run_time=0.6)
        self.at("nerve injury")
        self.play(*[k.lvl.animate.set_value(0.25) for k in w.kc[1:]], run_time=2.6)
        self.at("anion reversal")
        self.play(*Lv(w.cllab, 0), run_time=0.3)
        self.play(w.cl.acc.animate.set_value(1.0), *Lv(w.cllab2), w.Em.v.animate.set_value(-50), run_time=3.0, rate_func=smooth)
        self.at("same synaptic conductance")
        self.ripple([CHX, 0.8, 0], PURPLE, 0.45, 1.2)
        self.at("different sign")
        self.ripple([CHX, -1.0, 0], YELLOW, 0.5, 1.2)
        self.finish()


class S04Numbers(Base):
    def construct(self):
        w = syn()
        state_full(w, E=-50, high=True)
        self.add(*syn_items(w))
        rows = [mtx("Vm = −65 mV", [-5.8, 3.3, 0], RED), mtx("E = −75 mV", [-5.8, 2.55, 0], TEAL),
                mtx("−65 − (−75) = +10 mV", [-5.8, 1.8, 0], YELLOW), mtx("E = −50 mV", [-5.8, 2.55, 0], TEAL),
                mtx("−65 − (−50) = −15 mV", [-5.8, 1.8, 0], YELLOW)]
        force = txt("driving force", [0.5, 1.8, 0], TEXT, 28, left=True)
        keep = txt("conductance\nfixed", [0.3, -1.6, 0], PURPLE, 30)
        up = Obj(Arrow([-4.4, CUR_Y0, 0], [-4.4, CUR_Y0 + 0.8, 0], buff=0, color=YELLOW, stroke_width=10, tip_length=0.3), lvl=0)
        uplab = txt("+10 mV", [-4.4, -2.9, 0], YELLOW, 30)
        dnlab = txt("−15 mV", [-2.0, -2.9, 0], YELLOW, 30)
        self.add(*rows, force, keep, up, uplab, dnlab)
        self.play(*Lv([w.celllab, w.term, w.termlab, w.chanlab, *w.kc, w.kclab, w.cllab2, w.inf, w.arrlab], 0), w.cl.lvl.animate.set_value(0.3), run_time=1.0)
        w.Em.num.set_value(1)
        self.at("minus 65")
        self.play(*Lv(rows[0]), run_time=0.6)
        self.ripple([RX, Yv(VM0), 0], RED, 0.35, 0.9)
        self.at("reversal at minus 75")
        self.play(*Lv(rows[1]), w.Em.v.animate.set_value(-75), run_time=1.8, rate_func=smooth)
        self.at("gives plus 10")
        self.play(*Lv(rows[2]), run_time=0.7)
        self.at("driving force")
        self.play(*Lv(force), run_time=0.5)
        self.at("move reversal")
        self.play(*Lv(up), *Lv(uplab), *Lv([rows[1], rows[2], force], 0), run_time=0.6)
        self.at("minus 50")
        self.play(*Lv(rows[3]), w.Em.v.animate.set_value(-50), run_time=1.9, rate_func=smooth)
        self.at("becomes minus 15")
        self.play(*Lv([rows[4], force, dnlab]), run_time=0.7)
        self.at("conductance stayed")
        self.play(*Lv(keep), run_time=0.7)
        self.ripple([CHX, 0.8, 0], PURPLE, 0.45, 1.2)
        self.at("current direction")
        self.ripple([-4.4, -0.6, 0], YELLOW, 0.5, 1.0)
        self.ripple([CHX, -1.5, 0], YELLOW, 0.5, 1.0)
        self.finish()


class S05Refine(Base):
    def construct(self):
        w = syn()
        state_full(w, E=-50, high=True)
        put([w.celllab, w.term, w.termlab, w.chanlab, *w.kc, w.kclab, w.inf, w.arrlab, w.cllab2], 0)
        put(w.cl, 0.3)
        w.Em.num.set_value(1)
        w.Em.v.set_value(-50)
        put([w.term, w.termlab], 0)
        self.add(*syn_items(w))
        # leftovers of s04, rebuilt for the cross-fade
        old = [mtx("E = −50 mV", [-5.8, 2.55, 0], TEAL, lvl=1), mtx("−65 − (−50) = −15 mV", [-5.8, 1.8, 0], YELLOW, lvl=1),
               txt("driving force", [0.5, 1.8, 0], TEXT, 28, lvl=1, left=True), txt("conductance\nfixed", [0.3, -1.6, 0], PURPLE, 30, lvl=1),
               Obj(Arrow([-4.4, CUR_Y0, 0], [-4.4, CUR_Y0 + 0.8, 0], buff=0, color=YELLOW, stroke_width=10, tip_length=0.3), lvl=1),
               txt("+10 mV", [-4.4, -2.9, 0], YELLOW, 30, lvl=1), txt("−15 mV", [-2.0, -2.9, 0], YELLOW, 30, lvl=1),
               mtx("Vm = −65 mV", [-5.8, 3.3, 0], RED, lvl=1)]
        inp = txt("excitatory\ninput", [-5.5, 3.0, 0], ORANGE, 28)
        A = Stream([(-5.5, 2.25), (-5.5, -1.4)], ORANGE, n=7, speed=0.28, r=0.13)
        B = Stream([(-5.5, -0.9), (-2.0, -0.9), (-2.0, 1.45)], ORANGE, n=6, speed=0.22, r=0.1)
        shunt = txt("shunt", [-3.7, -0.45, 0], ORANGE, 28)
        tagA = txt("schematic", [-4.0, -2.0, 0], TEXT, 24)
        tagB = txt("schematic", [1.2, 0.45, 0], TEXT, 24)
        g = Gauge(1.2, 0.2, y0=-2.8, h=2.9, w=0.7, color=RED, lvl=0, tremble=0.02)
        glab = txt("firing", [1.2, -3.3, 0], RED, 28)
        self.add(*old, inp, A, B, shunt, tagA, tagB, g, glab)
        self.play(*Lv(old, 0), *Lv(w.term), *Lv(w.termlab), *Lv(w.celllab), run_time=1.2)
        self.at("open anion conductance")
        self.play(*Lv(w.arr, 0), *Lv([inp, tagA]), run_time=0.8)
        A.lvl.set_value(1)
        self.ripple([CHX, 0.8, 0], PURPLE, 0.45, 1.0)
        self.at("shunt")
        self.play(*Lv([shunt]), run_time=0.5)
        B.lvl.set_value(0.8)
        self.at("depolarizing response")
        self.play(w.Em.v.animate.set_value(-40), run_time=1.6, rate_func=smooth)
        self.at("excitatory")
        self.play(*Lv([g, glab, tagB]), run_time=0.9)
        self.at("raises firing")
        self.play(gv(g, 0.85), run_time=2.3)
        self.at("rat experiments")
        self.ripple([1.2, -1.4, 0], RED, 0.6, 1.2)
        self.finish()


class S06Predict(Base):
    def construct(self):
        w = syn()
        state_full(w, E=-40, high=True)
        put([w.celllab, w.arr, w.arrlab, w.kclab, w.cllab2], 0)
        put(w.cl, 0.3)
        w.Em.num.set_value(1)
        put([w.term, w.termlab, w.chan, *w.kc, w.inf], 1)
        g = Gauge(1.2, 0.85, y0=-2.8, h=2.9, w=0.7, color=RED, lvl=1, tremble=0.02)
        glab = txt("firing", [1.2, -3.3, 0], RED, 28)
        m = mini()
        pred = txt("Predict", [0, 3.2, 0], YELLOW, 48)
        qtx = Obj(T("Which added measurement can reveal\na changed postsynaptic effect?", 30, YELLOW, line_spacing=0.8).move_to([0, 3.15, 0]), lvl=0)
        stable = txt("cell counts\nstable", [5.4, 1.4, 0], YELLOW, 30)
        ck = mini_checks()
        cards, icons = make_cards()
        sch = txt("schematic icons", [5.3, -3.65, 0], TEXT, 22)
        self.add(*syn_items(w), g, glab, *m.items, pred, qtx, stable, *ck, *cards, *icons, sch)
        self.play(*hide([w.cell, w.term, w.termlab, w.chan, w.chanlab, *w.kc, w.inf, w.cl, w.ruler, w.Vm, w.Em, g, glab]), *Lv(m.items), *Lv(pred), run_time=1.2)
        self.at("cell counts")
        self.play(*Lv([stable, *ck]), run_time=0.8)
        self.at("which added measurement")
        self.play(*Lv(pred, 0), *Lv(qtx), run_time=0.8)
        self.at("more counting")
        self.play(*Lv([cards[0], icons[0]]), run_time=0.7)
        self.at("evoked output")
        self.play(*Lv([cards[1], icons[1]]), run_time=0.7)
        self.at("anion reversal")
        self.play(*Lv([cards[2], icons[2], sch]), run_time=0.7)
        self.finish()


def pred_stage(m, cards, icons, ck, stable, qtx):
    put(m.items)
    put([*cards, *icons, *ck, stable, qtx])


class S07Pause(Base):
    def construct(self):
        m = mini()
        qtx = Obj(T("Which added measurement can reveal\na changed postsynaptic effect?", 30, YELLOW, line_spacing=0.8).move_to([0, 3.15, 0]), lvl=1)
        stable = txt("cell counts\nstable", [5.4, 1.4, 0], YELLOW, 28, lvl=1)
        ck = mini_checks(1)
        cards, icons = make_cards()
        sch = txt("schematic icons", [5.3, -3.65, 0], TEXT, 22, lvl=1)
        put([*cards, *icons])
        put(m.items)
        drift = ClDots((1.8, 2.3, 1.2, 1.6), n=6, base=6, r=0.05, amp=0.15, lvl=1)
        ts = ValueTracker(1.0)
        bar = Rectangle(width=9, height=0.1, stroke_width=0, fill_color=YELLOW, fill_opacity=0.9).move_to([0, -3.65, 0])
        bar.add_updater(lambda b: b.stretch_to_fit_width(max(0.02, 9 * ts.get_value())).move_to([-6.3 + max(0.02, 9 * ts.get_value()) / 2, -3.65, 0]))
        self.add(*m.items, qtx, stable, *ck, *cards, *icons, sch, drift, bar)
        self.play(ts.animate.set_value(0.0), run_time=self.beat(0.9), rate_func=linear)
        self.finish()


class S08Reveal(Base):
    def construct(self):
        m = mini()
        qtx = Obj(T("Which added measurement can reveal\na changed postsynaptic effect?", 30, YELLOW, line_spacing=0.8).move_to([0, 3.15, 0]), lvl=1)
        stable = txt("cell counts\nstable", [5.4, 1.4, 0], YELLOW, 28, lvl=1)
        ck = mini_checks(1)
        cards, icons = make_cards()
        sch = txt("schematic icons", [5.3, -3.65, 0], TEXT, 22, lvl=1)
        put([*cards, *icons])
        put(m.items)
        # the big patch picture
        cc = np.array([-1.3, -0.5, 0])
        bp = cc + 2.1 * np.array([np.cos(0.35), np.sin(0.35), 0])
        pcell = Obj(Circle(radius=2.1, stroke_color=RED, stroke_width=6, fill_color=RED, fill_opacity=0.22).move_to(cc), lvl=0)
        pcell.set_z_index(-2)
        ppip = Obj(pipette_poly([4.4, 2.7, 0], bp + [0.08, 0.05, 0], 0.34, 0.08), lvl=0)
        pore = Obj(DashedVMobject(Circle(radius=0.2, stroke_color=TEXT, stroke_width=4).move_to(bp), num_dashes=10), lvl=0)
        pcl = ClDots((-2.6, -0.1, -1.7, 0.6), n=14, base=14, r=0.13, amp=0.3, lvl=0, seed=5)
        pcl.set_z_index(-1)
        elec = Stream([(4.2, 2.55), tuple(bp)], YELLOW, n=6, speed=0.35, r=0.12)
        plab = txt("gramicidin perforated patch", [3.0, 3.45, 0], TEXT, 30)
        elab = txt("electrical access", [4.9, 0.7, 0], YELLOW, 30)
        clab = txt("chloride stays inside", [-1.3, -3.2, 0], TEAL, 30)
        rows = [(CountIcon(-4.7, 2.1, 1.35), txt("survival", [-1.3, 2.1, 0], TEXT, 56, left=True)),
                (TraceIcon(-4.7, 0.0, 1.3), txt("output", [-1.3, 0.0, 0], PURPLE, 56, left=True)),
                (PatchIcon(-4.7, -2.1, 1.3), txt("postsynaptic effect", [-1.3, -2.1, 0], RED, 56, left=True))]
        arrows = [Obj(Arrow([-2.9, y, 0], [-1.7, y, 0], buff=0, color=TEXT, stroke_width=8, tip_length=0.26), lvl=0) for y in (2.1, 0.0, -2.1)]
        self.add(pcell, pcl, ppip, pore, elec, plab, elab, clab, *m.items, qtx, stable, *ck, *cards, *icons, sch)
        for ic, wd in rows:
            self.add(ic, wd)
        self.add(*arrows)
        self.play(*hide([*m.items, qtx, stable, *ck, sch, cards[0], cards[1], icons[0], icons[1]]), run_time=1.0)
        self.ripple([CARDX[2], CARDY, 0], YELLOW, 1.3, 1.2)
        self.at("gramicidin")
        self.play(*hide([cards[2], icons[2]]), *Lv([pcell, pcl, ppip, plab]), run_time=1.0)
        self.at("gives electrical")
        self.play(*Lv([pore, elab]), run_time=0.7)
        elec.lvl.set_value(1.0)
        self.at("preserving")
        self.play(*Lv(clab), run_time=0.6)
        self.ripple(cc, TEAL, 1.0, 1.4)
        self.at("stable counts")
        self.play(*hide([pcell, pcl, ppip, pore, plab, elab, clab]), run_time=0.5)
        elec.lvl.set_value(0.0)
        self.play(*Lv([rows[0][0], arrows[0]]), run_time=0.5)
        self.at("survival")
        self.play(*Lv(rows[0][1]), run_time=0.5)
        self.at("evoked inhibitory events")
        self.play(*Lv([rows[1][0], arrows[1]]), run_time=0.7)
        self.at("output")
        self.play(*Lv(rows[1][1]), run_time=0.5)
        self.at("reversal tests")
        self.play(*Lv([rows[2][0], arrows[2]]), run_time=0.7)
        self.at("target's response")
        self.play(*Lv(rows[2][1]), run_time=0.5)
        self.finish()


class Microglia(Obj):
    def __init__(self, c, lvl=0.0):
        c = np.array(c, float)
        body = Circle(radius=0.48, stroke_color=GOLD, stroke_width=4, fill_color=GOLD, fill_opacity=0.28).move_to(c)
        nuc = Dot(radius=0.14, color=GOLD).move_to(c)
        arms = [Line(c + 0.46 * np.array([np.cos(a), np.sin(a), 0]), c + 0.78 * np.array([np.cos(a + 0.18), np.sin(a + 0.18), 0]), color=GOLD, stroke_width=5)
                for a in np.linspace(0.3, 6.0, 7)]
        super().__init__(body, nuc, *arms, lvl=lvl, breathe=0.08)


MGC = (2.6, 2.65, 0)
TRKX = 0.0


def world_source(w, with_bdnf=False):
    """s09/s10 extras: microglia, BDNF stream, TrkB block, labels."""
    mg = Microglia(MGC)
    mglab = txt("microglia", [2.6, 3.6, 0], GOLD, 28)
    atp = txt("ATP", [3.95, 2.65, 0], TEXT, 28)
    bd = Stream([(2.3, 2.15), (TRKX + 0.15, 1.2)], GOLD, n=3, speed=0.22, r=0.1, square=True)
    bdlab = txt("BDNF", [3.7, 1.95, 0], GOLD, 28)
    trk = Obj(Rectangle(width=0.5, height=0.6, stroke_color=RED, stroke_width=4, fill_color=RED, fill_opacity=0.55).move_to([TRKX, 0.8, 0]), lvl=0)
    trklab = txt("TrkB", [TRKX, 0.15, 0], TEXT, 28)
    return mg, mglab, atp, bd, bdlab, trk, trklab


class S09Source(Base):
    def construct(self):
        w = syn()
        state_full(w, E=-75)
        put([w.arr, w.arrlab, w.chanlab, w.kclab], 0)
        put(w.kclab)
        self.add(*syn_items(w))
        tag = txt("adult male rat studies", [-6.6, 3.55, 0], TEXT, 24, left=True)
        mg, mglab, atp, bd, bdlab, trk, trklab = world_source(w)
        self.add(tag, mg, mglab, atp, bd, bdlab, trk, trklab)
        self.at("rat studies", lead=0.0)
        self.play(*Lv(tag), run_time=0.6)
        self.at("upstream", lead=-0.6)
        self.play(*Lv([mg, mglab]), run_time=0.8)
        self.at("stimulated")
        self.play(*Lv(atp), run_time=0.5)
        self.ripple(MGC, GOLD, 0.5, 1.0)
        self.at("released")
        bd.lvl.set_value(1.0)
        self.play(*Lv(bdlab), run_time=0.6)
        self.at("gold")
        self.play(*Lv(trk), run_time=0.6)
        self.at("reached")
        self.play(*Lv(trklab), run_time=0.5)
        self.at("on the red target")
        self.ripple([TRKX, 0.8, 0], RED, 0.5, 1.0)
        self.finish()


class S10Target(Base):
    def construct(self):
        w = syn()
        state_full(w, E=-75)
        put([w.arr, w.arrlab, w.chanlab], 0)
        self.add(*syn_items(w))
        tag = txt("adult male rat studies", [-6.6, 3.55, 0], TEXT, 24, left=True, lvl=1)
        mg, mglab, atp, bd, bdlab, trk, trklab = world_source(w)
        put([mg, mglab, atp, bdlab, trk, trklab])
        bd.lvl.set_value(1.0)
        self.add(tag, mg, mglab, atp, bd, bdlab, trk, trklab)
        self.at("moved the reversal marker")
        self.play(w.Em.v.animate.set_value(-50), run_time=2.6, rate_func=smooth)
        self.at("did not measure")
        self.play(*Lv(w.kclab, 0.0), *Lv(w.kclab2), run_time=0.6)
        self.ripple([-4.0, 1.05, 0], TEAL, 0.4, 1.2)
        self.at("purple synapse")
        self.ripple([-2.0, 2.5, 0], PURPLE, 1.0, 1.4)
        self.ripple([CHX, 0.8, 0], PURPLE, 0.45, 1.2)
        self.finish()


class Ind(Obj):
    """One table cell for s11: label plus a small indicator whose tracker p (0..1) is what changes."""

    def __init__(self, kind, cx, cy, lvl=0.0):
        self.kind, self.p, self.cx, self.cy = kind, ValueTracker(0.0), cx, cy
        box = RoundedRectangle(corner_radius=0.15, width=3.9, height=1.5, stroke_color=TEXT, stroke_width=3, stroke_opacity=0.5).move_to([cx, cy, 0])
        name = {"cells": "cells", "events": "events", "rev": "reversal"}[kind]
        lab = T(name, 28, TEXT).move_to([cx - 1.85, cy, 0], aligned_edge=LEFT)
        self.parts = []
        if kind == "cells":
            self.parts = [Dot(radius=0.16, color=[ORANGE, PURPLE, RED, ORANGE, PURPLE][i]).move_to([cx + 0.15 + 0.36 * i, cy, 0]) for i in range(5)]
        elif kind == "events":
            self.parts = [Rectangle(width=0.2, height=0.9, stroke_width=0, fill_color=PURPLE, fill_opacity=0.95).move_to([cx + 0.15 + 0.36 * i, cy, 0]) for i in range(5)]
        else:
            self.parts = [Line([cx + 0.1, cy - 0.25, 0], [cx + 1.8, cy - 0.25, 0], color=TEXT, stroke_width=3),
                          Line([cx + 0.7, cy - 0.25 - 0.25, 0], [cx + 0.7, cy - 0.25 + 0.25, 0], color=TEAL, stroke_width=8)]
        super().__init__(box, lab, *self.parts, lvl=lvl, breathe=0.0)
        self.add_updater(self._ind)

    def _ind(self, m, dt):
        p, t = float(self.p.get_value()), self.tt
        if self.kind == "cells":
            for i, d in enumerate(self.parts):
                s = 1.0 if i < 2 else max(0.02, 1.0 - p)
                d.set_width(0.32 * s)
                d.move_to([self.cx + 0.15 + 0.36 * i, self.cy + 0.05 * np.sin(1.3 * t + i), 0])
        elif self.kind == "events":
            hs = [0.9, 1.0, 0.8, 1.0, 0.9]
            for i, b in enumerate(self.parts):
                h = max(0.08, hs[i] * (1.0 - 0.72 * p) * (1 + 0.07 * np.sin(1.5 * t + i)))
                b.stretch_to_fit_height(h)
                b.move_to([self.cx + 0.15 + 0.36 * i, self.cy - 0.55 + h / 2, 0])
        else:
            self.parts[1].move_to([self.cx + 0.7 + 1.0 * p + 0.04 * np.sin(1.4 * t), self.cy - 0.25, 0])


class S11Patterns(Base):
    def construct(self):
        w = syn()
        state_full(w, E=-50)
        put([w.arr, w.arrlab, w.chanlab], 0)
        mg, mglab, atp, bd, bdlab, trk, trklab = world_source(w)
        put([mg, mglab, atp, trk, trklab])
        bd.lvl.set_value(1.0)
        put(bdlab)
        w.kclab2.put(1)
        w.kclab.put(0)
        X = [-4.5, 0.0, 4.5]
        Y = [1.45, -0.35, -2.15]
        heads = [txt("Cell death", [X[0], 3.2, 0], TEXT, 34), txt("Lost output", [X[1], 3.2, 0], PURPLE, 34),
                 Obj(T("Postsynaptic\nchange", 34, TEAL, line_spacing=0.8).move_to([X[2], 3.15, 0]), lvl=0)]
        co = txt("can coexist", [0, 3.2, 0], YELLOW, 40)
        cols = [[Ind(k, X[c], Y[r]) for r, k in enumerate(["cells", "events", "rev"])] for c in range(3)]
        self.add(*syn_items(w), mg, mglab, atp, bd, bdlab, trk, trklab, *heads, co, *[i for c in cols for i in c])
        self.play(*hide([*syn_items(w), mg, mglab, atp, bdlab, trk, trklab]), *Lv(heads), *Lv([i for c in cols for i in c]), run_time=1.6)
        bd.lvl.set_value(0.0)
        self.at("cell death")
        self.play(cols[0][0].p.animate.set_value(1.0), cols[0][1].p.animate.set_value(1.0), run_time=2.0)
        self.at("lost output")
        self.play(cols[1][1].p.animate.set_value(1.0), run_time=2.0)
        self.at("effect leaves")
        self.ripple([X[2], Y[0], 0], TEAL, 0.8, 1.0)
        self.at("events present")
        self.ripple([X[2], Y[1], 0], TEAL, 0.8, 1.0)
        self.at("reversal moves")
        self.play(cols[2][2].p.animate.set_value(1.0), run_time=1.8)
        self.at("real mechanisms")
        self.play(*Lv([cols[0][0], cols[0][1], cols[0][2], cols[2][0], cols[2][1], cols[2][2], heads[0], heads[2]], 0.0),
                  *Lv(heads[1], 0), run_time=1.0)
        self.play(*Lv(co), cols[1][0].p.animate.set_value(1.0), cols[1][2].p.animate.set_value(1.0), run_time=2.0)
        self.finish()


class CardMech(Obj):
    """The mechanism shrunk into a bordered card: purple ending, red target, channel, ruler with a moving reversal marker."""

    def __init__(self, lvl=0.0):
        cx = -4.15
        box = RoundedRectangle(corner_radius=0.25, width=4.9, height=6.3, stroke_color=TEXT, stroke_width=4).move_to([cx, -0.15, 0])
        title = T("adult male rat\nlamina I", 28, TEXT, line_spacing=0.8).move_to([cx, 2.35, 0])
        term = RoundedRectangle(corner_radius=0.15, width=2.6, height=0.8, stroke_color=PURPLE, stroke_width=4, fill_color=PURPLE, fill_opacity=0.28).move_to([-4.6, 1.0, 0])
        tl = T("ending", 24, PURPLE).move_to([-4.6, 1.0, 0])
        cell_ = RoundedRectangle(corner_radius=0.2, width=3.2, height=1.9, stroke_color=RED, stroke_width=4, fill_color=RED, fill_opacity=0.14).move_to([-4.6, -1.5, 0])
        chan = Rectangle(width=0.4, height=0.4, stroke_color=PURPLE, stroke_width=4, fill_color=PURPLE, fill_opacity=0.55).move_to([-4.6, -0.55, 0])
        self.rx = -2.45
        self.rul = Line([self.rx, -2.5, 0], [self.rx, 1.2, 0], color=TEXT, stroke_width=3)
        ticks = [Line([self.rx - 0.12, -2.5 + 0.617 * k, 0], [self.rx + 0.12, -2.5 + 0.617 * k, 0], color=TEXT, stroke_width=2) for k in range(7)]
        self.mk = Line([self.rx - 0.3, 0, 0], [self.rx + 0.3, 0, 0], color=TEAL, stroke_width=8)
        rl = T("reversal", 24, TEAL).move_to([self.rx - 0.1, -2.85, 0])
        super().__init__(box, title, term, tl, cell_, chan, self.rul, *ticks, self.mk, rl, lvl=lvl)
        self.add_updater(lambda m, dt: self.mk.move_to([self.rx, -2.5 + 0.0617 * (-62.5 + 12.5 * np.sin(0.9 * self.tt) + 90.0), 0]))


class S12Scope(Base):
    def construct(self):
        w = syn()
        state_full(w, E=-50)
        put([w.arr, w.arrlab, w.chanlab], 0)
        mg, mglab, atp, bd, bdlab, trk, trklab = world_source(w)
        put([mg, mglab, atp, trk, trklab, bdlab])
        bd.lvl.set_value(1.0)
        w.kclab2.put(1)
        w.kclab.put(0)
        tag = txt("adult male rat studies", [-6.6, 3.55, 0], TEXT, 24, left=True, lvl=1)
        card = CardMech()
        cdots = ClDots((-5.9, -3.3, -2.3, -0.8), n=10, base=10, r=0.07, amp=0.15, lvl=0, seed=9)
        names = [("Count cells", TEXT), ("Test output", PURPLE), ("Measure reversal", TEAL)]
        RY = [2.1, 0.0, -2.1]
        boxes = [Obj(RoundedRectangle(corner_radius=0.2, width=7.9, height=1.7, stroke_color=TEXT, stroke_width=3).move_to([2.65, y, 0]), lvl=0) for y in RY]
        icons = [CountIcon(0.55, RY[0], 0.8), TraceIcon(0.55, RY[1], 0.7), PatchIcon(0.55, RY[2], 0.8)]
        words = [txt(n, [2.1, y, 0], c, 40, left=True) for (n, c), y in zip(names, RY)]
        self.add(*syn_items(w), mg, mglab, atp, bd, bdlab, trk, trklab, tag, card, cdots, *boxes, *icons, *words)
        self.at("established", lead=0.3)
        self.play(*hide([*syn_items(w), mg, mglab, atp, bdlab, trk, trklab, tag]), *Lv([card, cdots]), *[b.lvl.animate.set_value(0.4) for b in boxes],
                  *[i.lvl.animate.set_value(0.4) for i in icons], run_time=1.6)
        bd.lvl.set_value(0.0)
        self.at("adult male rats")
        self.ripple([-4.15, 2.35, 0], TEXT, 0.9, 1.2)
        self.at("keep the experimental", lead=0.4)
        self.play(*[b.lvl.animate.set_value(0.7) for b in boxes], *[i.lvl.animate.set_value(0.7) for i in icons], run_time=1.2)
        self.at("count cells")
        self.play(boxes[0].lvl.animate.set_value(1.0), icons[0].lvl.animate.set_value(1.0), *Lv(words[0]), run_time=0.7)
        self.at("test output")
        self.play(boxes[1].lvl.animate.set_value(1.0), icons[1].lvl.animate.set_value(1.0), *Lv(words[1]), run_time=0.7)
        self.at("measure reversal")
        self.play(boxes[2].lvl.animate.set_value(1.0), icons[2].lvl.animate.set_value(1.0), *Lv(words[2]), run_time=0.7)
        self.at("target neuron")
        self.ripple([-2.45, -1.0, 0], TEAL, 0.5, 1.2)
        self.finish()


class S13End(EndCard):
    LINE = "Separate survival, output, and postsynaptic effect."
