"""Who Opens the Touch Gate? One dorsal-horn circuit carried through the film (schematic, mouse).

COLOR MAP (one colour per concept, whole film)
  BLUE   = touch input        ORANGE = excitatory relay (somatostatin)   PURPLE = inhibitory neuron / signal
  RED    = projection output / behaviour gauge     TEAL = highlight rings     YELLOW = open question
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
            m.become(Circle(radius=r * (1 + 2.2 * a), stroke_color=color, stroke_width=6).move_to(np.array(pos, float)).set_stroke(opacity=1 - a))
            m.age = a * t
        ring.add_updater(grow)
        self.add(ring)


class Base(Glow, SpokenScene):
    pass


class Plain(Glow, NarratedScene):
    pass


# ------------------------------------------------------------------ scenes
class S00Hook(Base):
    def construct(self):
        w = world()
        self.add(*circuit_items(w))
        for o in (w.O, w.P, w.R):
            o.put(0.2)
        self.play(*Lv([w.panel, w.tag, w.skin, w.fiber, w.pulse, w.pulse2]), run_time=0.8)
        self.ripple(SKIN, BLUE, 0.5, 1.2)
        self.wait(1.2)
        self.ripple(SKIN, BLUE, 0.5, 1.2)
        self.at("skin")
        self.ripple(SKIN, BLUE, 0.5, 1.2)
        self.at("watch")
        self.play(w.fiber2.lvl.animate.set_value(1), run_time=0.8)
        self.at("dorsal horn")
        self.play(*Lv(w.dh), run_time=0.8)
        self.at("it meets")
        self.play(*Lv(w.dh, 0), run_time=0.5)
        self.at("orange relay")
        self.play(*Lv([w.O, w.OR]), run_time=0.7)
        self.ripple(OP, ORANGE, 0.5, 0.8)
        self.at("relay")
        self.play(*Lv(w.Olab), run_time=0.4)
        self.at("purple")
        self.play(*Lv(w.P), w.fiber2.lvl.animate.set_value(0), run_time=0.5)
        self.at("inhibitory")
        self.play(*Lv(w.Plab), run_time=0.4)
        self.at("break")
        self.play(*Lv(w.brake), run_time=0.5)
        self.at("red output")
        self.play(*Lv([w.R, w.route, w.Rlab]), run_time=0.8)
        self.finish()


class S01Title(Plain):
    def construct(self):
        w = world()
        hook_end(w)
        self.add(*circuit_items(w))
        title = Obj(T("Who Opens the Touch Gate?", size=46, font=TITLE_FONT).move_to([0, 3.3, 0]), lvl=0)
        self.add(title)
        self.play(*Lv(w.tag, 0), *Lv(title), run_time=0.7)
        self.wait(0.7)
        self.play(*Lv(title, 0), *Lv(w.tag), run_time=0.5)
        self.finish()


class S02Relay(Base):
    def construct(self):
        w = world()
        hook_end(w)
        w.gauge.put(0)
        w.glab.put(0)
        self.add(*circuit_items(w))
        self.play(*Lv([w.gauge, w.glab]), run_time=1.2)
        self.at("removing")
        w.card.shift(RIGHT * 2.5)
        self.play(*Lv(w.Olab, 0), run_time=0.3)
        self.play(mv(w.O, [-1.4, 2.1, 0], t=1.6), *Lv(w.O, 0.45), *Lv([w.OR], 0), *Lv(w.card),
                  mv(w.card, [1.0, -2.8, 0], t=1.6), run_time=1.6)
        self.at("somatostatin")
        self.play(*Lv(w.sst), run_time=0.8)
        self.at("weakens")
        self.play(gv(w.gauge, 0.25), *Lv([w.R, w.route], 0.5), run_time=3.0)
        self.at("the result")
        self.play(*Lv(w.ghost), run_time=1.0)
        self.at("every route")
        self.play(*Lv([w.bypass, w.q]), run_time=1.2)
        self.finish()


class S03Brake(Base):
    def construct(self):
        w = world()
        s02_end(w)
        self.add(*circuit_items(w))
        self.at("restore")
        self.play(mv(w.O, OP, t=1.4), *Lv(w.O, 1), *Lv([w.OR, w.R, w.route]), *Lv([w.ghost, w.card, w.bypass, w.q, w.sst, w.gauge, w.glab], 0), run_time=1.4)
        self.play(*Lv(w.Olab), run_time=0.3)
        self.at("break")
        self.play(*Lv(w.brake, 0.35), run_time=0.35)
        self.play(*Lv(w.brake, 1), run_time=0.35)
        self.at("dinorphin")
        self.play(*Lv(w.Plab, 0), run_time=0.3)
        self.play(*Lv(w.Plab2), run_time=0.5)
        self.at("superficial")
        self.play(*Lv(w.E, 0.25), *Lv(w.EL, 0.25), *Lv([w.sup, w.deep]), run_time=1.0)
        self.at("myelinated")
        self.play(*Lv([w.fiber2, w.afflab]), run_time=0.9)
        self.at("blue input")
        self.play(*Lv(w.same), run_time=0.8)
        self.at("removing purple")
        self.play(*Lv([w.P, w.brake, w.Plab2, w.fB], 0), run_time=1.3)
        self.at("recruit")
        for i in range(5):
            self.play(*Lv([w.E[i], w.EL[i]]), run_time=0.4)
        self.finish()


class S04Predict(Base):
    def construct(self):
        w = world()
        s03_end(w)
        ch = SimpleNamespace(fewer=chipo("fewer", [5.15, 2.2, 0], TEAL, 32), same=chipo("the same", [5.15, 0.95, 0], TEAL, 32),
                             more=chipo("more", [5.15, -0.4, 0], TEAL, 32))
        self.add(*circuit_items(w), ch.fewer, ch.same, ch.more)
        self.play(*Lv(w.E, 0.25), *Lv(w.EL, 0.25), *Lv([w.R, w.route], 0.3), *Lv([w.Rlab, w.Olab], 0), run_time=1.2)
        self.at("slice")
        self.play(*Lv(w.tag, 0), *Lv(w.tagslice), run_time=0.7)
        self.at("inhibitory population")
        self.play(*Lv(w.pghost), run_time=0.9)
        self.at("abeta")
        self.play(*Lv(w.afflab, 0), *Lv(w.afflab2), run_time=0.7)
        self.at("fewer")
        self.play(*Lv(ch.fewer), run_time=0.6)
        self.at("the same")
        self.play(*Lv(ch.same), run_time=0.6)
        self.at("more")
        self.play(*Lv(ch.more), run_time=0.6)
        self.at("keep")
        self.play(*Lv(w.fiber2, 0.35), run_time=0.5)
        self.play(*Lv(w.fiber2, 1), run_time=0.5)
        self.play(*Lv(w.fiber2, 0.35), run_time=0.5)
        self.finish()


class S05Pause(Plain):
    def construct(self):
        w = world()
        ch = s04_end(w)
        timer = Rectangle(width=12.0, height=0.1, stroke_width=0, fill_color=TEAL, fill_opacity=0.9).move_to([-6.0, -3.68, 0], aligned_edge=LEFT)
        self.add(*circuit_items(w), ch.fewer, ch.same, ch.more, timer)

        def drain(m, a):
            m.stretch_to_fit_width(max(12.0 * (1 - a), 0.02))
            m.move_to([-6.0, -3.68, 0], aligned_edge=LEFT)
        self.play(UpdateFromAlphaFunc(timer, drain, run_time=4.5, rate_func=linear))
        self.finish()


class S06Reveal(Base):
    def construct(self):
        w = world()
        ch = s04_end(w)
        # dashed lamina border and the grid
        lam = Obj(DashedLine([-6.4, 0.45, 0], [1.2, 0.45, 0], color=YELLOW, stroke_width=4), lvl=0)
        lamlab = txt("lamina II–III border", [-6.3, 0.85, 0], YELLOW, 28, left=True)
        gx, gy = 4.0, 0.45
        base, lit = [], []
        for r in range(4):
            for c in range(5):
                p = [gx + (c - 2) * 0.8, gy + (1.5 - r) * 0.8, 0]
                base.append(Obj(Circle(radius=0.28, stroke_color=TEXT, stroke_width=3).move_to(p), lvl=0))
                lit.append(Obj(Circle(radius=0.28, stroke_width=3, stroke_color=ORANGE, fill_color=ORANGE, fill_opacity=0.9).move_to(p), lvl=0))
        gl = txt("% of recorded neurons\n(schematic)", [gx, -1.75, 0], TEXT, 28)
        more = chipo("More", [3.0, 2.55, 0], ORANGE, 40, 1)
        more.move_to([2.9, 2.55, 0])
        hdr5 = txt("5%", [5.3, 2.55, 0], ORANGE, 44)
        hdr40 = txt("40%", [5.3, 2.55, 0], ORANGE, 44)
        s1 = txt("2 of 38", [2.9, -2.75, 0], TEXT, 28)
        s2 = txt("12 of 30", [5.0, -2.75, 0], TEXT, 28)
        gate = txt("gated connection", [-2.3, -3.05, 0], YELLOW, 28)
        qm = txt("where?", [-0.5, -2.4, 0], YELLOW, 44)
        self.add(*circuit_items(w), ch.fewer, ch.same, ch.more, lam, lamlab, *base, *lit, gl, hdr5, hdr40, s1, s2, gate, qm, more)
        more.put(0)
        self.at("more")
        # the chosen answer moves into the header slot, the others leave; circuit quietens
        self.play(*Lv([ch.fewer, ch.same], 0), mv(ch.more, [2.9, 2.55, 0], scale=1.15, t=1.4),
                  *Lv([w.P, w.pghost, w.sup, w.deep, w.same, w.afflab2, w.R, w.route, w.Olab], 0),
                  *Lv([w.skin, w.fiber, w.O], 0.45), run_time=1.4)
        self.at("lamina")
        self.play(*Lv([lam, lamlab]), run_time=1.0)
        self.at("beta")
        self.play(*[Lv(o, 0.3)[0] for o in base], run_time=1.0)
        self.at("5")
        self.play(*Lv(lit[0]), *Lv(hdr5), *Lv(s1), *Lv(w.E[0], 1), *Lv(w.EL[0], 1), run_time=0.8)
        self.at("40")
        self.play(*Lv(hdr5, 0), *Lv(hdr40), run_time=0.5)
        for k in range(1, 8):
            extra = []
            if k in (1, 2, 4, 6):
                j = {1: 1, 2: 2, 4: 3, 6: 4}[k]
                extra = [*Lv(w.E[j]), *Lv(w.EL[j])]
            self.play(*Lv(lit[k]), *extra, run_time=0.25)
            if k == 3:
                self.play(*Lv(gl), *Lv(s2), run_time=0.3)
        self.at("measurement")
        self.play(*Lv([w.fiber, w.fiber2, w.skin, w.O], 1), *Lv(gate), run_time=0.8)
        self.ripple([-3.3, -1.4, 0], YELLOW, 0.4, 0.9)
        self.at("behavior")
        self.play(*[Lv(o, 0.25)[0] for o in lit + base], *Lv([hdr40, s1, s2, gl], 0.3), *Lv(gate, 0), run_time=0.8)
        self.play(*Lv(qm), run_time=0.6)
        self.play(mv(qm, [1.0, -2.9, 0], t=1.0))
        self.play(mv(qm, [-1.2, -2.9, 0], t=1.0))
        self.at("failed")
        self.play(mv(qm, [-0.5, -2.4, 0], t=1.2))
        self.ripple([-3.3, -1.4, 0], YELLOW, 0.4, 0.9)
        self.finish()


# --- tools layout (s07, s08)
STX = [-4.4, 0.0, 4.4]


def tools_world():
    t = SimpleNamespace()
    t.track = Obj(Line([-5.4, 2.45, 0], [5.4, 2.45, 0], color=GREY, stroke_width=4), lvl=0)
    t.dots = [Obj(Dot([x, 2.45, 0], radius=0.16, color=TEXT), lvl=0) for x in STX]
    t.labs = [txt(s, [x, 3.15, 0], TEXT, 32) for s, x in zip(["ablation", "silencing", "activation"], STX)]
    t.P = cell([STX[0], 0.7, 0], PURPLE, 0.45, lvl=0, phase=0.7)
    t.P.cur = 1.0
    t.O = cell([-2.0, -2.1, 0], ORANGE, 0.7, lvl=0)
    t.R = cell([2.2, -2.1, 0], RED, 0.85, lvl=0, phase=2)
    t.Olab, t.Rlab = txt("relay", [-2.0, -3.55, 0], ORANGE), txt("output", [2.2, -3.55, 0], RED)
    t.link = Obj(Line([-1.4, -2.1, 0], [1.5, -2.1, 0], color=ORANGE, stroke_width=6), lvl=0)
    t.fl = Flow(Line([-1.4, -2.1, 0], [1.5, -2.1, 0]), ORANGE, t.link, n=3, speed=0.3)
    t.inh = Inh(lambda: t.P.get_bottom() + DOWN * 0.02, [-2.0, -1.5, 0])
    t.fi = Flow(t.inh.line, PURPLE, t.inh, n=3, speed=0.4)
    t.fi.gain = 1.0
    t.out = Obj(Arrow([2.9, -2.1, 0], [4.6, -2.1, 0], buff=0, color=RED, stroke_width=7, tip_length=0.28), lvl=0)
    t.fo = Flow(Line([2.9, -2.1, 0], [4.6, -2.1, 0]), RED, t.out, n=2, speed=0.3)
    t.cross = Obj(Line([-1.5, -0.45, 0], [-0.9, 0.15, 0], color=RED, stroke_width=8), Line([-1.5, 0.15, 0], [-0.9, -0.45, 0], color=RED, stroke_width=8), lvl=0)
    t.ghost = Obj(DashedVMobject(Circle(radius=0.9, color=PURPLE, stroke_width=4).move_to([STX[0], 0.7, 0]), num_dashes=18), lvl=0)
    t.mark = txt("marked earlier", [STX[0], -0.65, 0], PURPLE, 28)
    t.beh = txt("behaviour", [2.2, -3.55, 0], RED)
    return t


def tools_items(t):
    return [t.track, *t.dots, t.link, t.inh, t.out, t.cross, t.ghost, t.O, t.R, t.P, t.fl, t.fi, t.fo, *t.labs, t.Olab, t.Rlab, t.mark, t.beh]


class S07Tools(Base):
    def construct(self):
        t = tools_world()
        self.add(*tools_items(t))
        self.play(*Lv([t.track, t.dots[0], t.dots[1], t.dots[2]]), *Lv([t.P, t.O, t.R, t.link, t.inh, t.out, t.Olab, t.Rlab]), run_time=1.8)
        self.at("oblation")
        self.play(*Lv(t.labs[0]), t.dots[0].lvl.animate.set_value(1), run_time=0.8)
        self.ripple([STX[0], 2.45, 0], TEAL, 0.2, 0.7)
        self.at("removes")
        self.play(mv(t.P, scale=0.1, t=1.2), *Lv(t.P, 0), *Lv(t.inh, 0), run_time=1.2)
        self.play(mv(t.O, scale=1.25, t=0.8), mv(t.R, scale=1.2, t=0.8), run_time=0.8)
        self.at("marked")
        self.play(*Lv(t.ghost), *Lv(t.mark), run_time=1.0)
        self.at("tetanus")
        self.play(*Lv([t.ghost, t.mark], 0), *Lv(t.labs[1]), run_time=0.8)
        t.P.move_to([STX[1], 0.7, 0])
        self.play(mv(t.P, scale=2.0, t=0.1), run_time=0.1)
        self.play(*Lv(t.P), *Lv(t.inh), mv(t.O, scale=1.0, t=1.0), mv(t.R, scale=1.0, t=1.0), run_time=1.0)
        self.at("alive")
        self.ripple([STX[1], 0.7, 0], PURPLE, 0.9, 0.9)
        self.at("blocking")
        self.play(*Lv(t.cross), t.fi.lvl.animate.set_value(0), run_time=0.5)
        t.fi.gain = 0.0
        self.at("activation")
        t.fi.gain = 1.0
        self.play(*Lv(t.cross, 0), *Lv(t.labs[2]), t.dots[2].lvl.animate.set_value(1), mv(t.P, [STX[2], 0.7, 0], t=1.6), run_time=1.6)
        self.at("added")
        t.fi.speed = 1.2
        self.play(*Lv(t.O, 0.5), *Lv(t.link, 0.35), mv(t.R, scale=0.8, t=1.4), *Lv(t.R, 0.55), run_time=1.4)
        self.at("measured")
        self.play(*Lv(t.Rlab, 0), run_time=0.4)
        self.play(*Lv(t.beh), run_time=0.6)
        self.finish()


class S08Opposites(Base):
    def construct(self):
        t = tools_world()
        # start from the end of s07
        t.track.put(1)
        for d in t.dots:
            d.put(1)
        for l in t.labs:
            l.put(1)
        t.P.move_to([STX[2], 0.7, 0])
        t.P.scale(2.0)
        t.P.cur = 2.0
        t.P.put(1)
        t.inh.put(1)
        t.fi.speed = 1.2
        t.O.put(0.5)
        t.R.put(0.55)
        t.R.scale(0.8)
        t.R.cur = 0.8
        t.link.put(0.35)
        t.out.put(1)
        t.beh.put(1)
        t.Olab.put(1)
        t.out.put(1)
        gs = [Gauge(-1.2, 0.3, lvl=0, color=RED), Gauge(2.0, 0.65, lvl=0, color=RED, ph=1.0), Gauge(5.2, 0.65, lvl=0, color=RED, ph=2.0)]
        gl = [txt("nocifensive\nbehaviour", [-1.2, 2.4, 0], RED), txt("mechanical\nsensitivity", [2.0, 2.4, 0], RED), txt("thermal\nsensitivity", [5.2, 2.4, 0], RED)]
        act = chipo("activate", [-4.6, 2.35, 0], YELLOW, 34)
        inh = chipo("inhibit", [-4.6, -1.8, 0], YELLOW, 34)
        act.put(0)
        inh.put(0)
        # slice inset
        box = Obj(Rectangle(width=8.8, height=5.0, stroke_color=GREY, stroke_width=3).move_to([2.2, -0.1, 0]), lvl=0)
        tagm = txt("mouse slice", [-6.6, 3.35, 0], TEXT, 26, lvl=0, left=True)
        llab, slab = txt("light", [-1.3, 1.2, 0], BLUE, 30), txt("spikes", [-1.3, -0.9, 0], ORANGE, 30)
        schem = txt("schematic", [4.9, -2.2, 0], TEXT, 28)
        pl, sp = [], []
        for k in range(6):
            x = 0.0 + k * 1.0
            pl.append(Obj(Line([x, 1.0, 0], [x, 1.7, 0], color=BLUE, stroke_width=8), Line([x - 0.2, 1.0, 0], [x + 0.2, 1.0, 0], color=BLUE, stroke_width=4), lvl=0))
            sp.append(Obj(Line([x + 0.25, -1.1, 0], [x + 0.25, -0.1, 0], color=ORANGE, stroke_width=6), lvl=0))
        self.add(*tools_items(t), *gs, *gl, act, inh, box, tagm, llab, slab, schem, *pl, *sp)
        O = t.O
        self.add(O)
        # the relay is carried left; everything else of the tool layout leaves
        rest = [t.track, *t.dots, *t.labs, t.P, t.R, t.link, t.inh, t.out, t.Olab, t.beh, t.fl, t.fi, t.fo, t.mark, t.cross, t.ghost]
        self.play(*Lv(rest, 0), mv(O, [-4.6, 0.3, 0], scale=1.8, t=1.4), *Lv(O, 1), run_time=1.4)
        self.at("sharpen")
        self.play(*Lv([act, inh], 0.45), run_time=0.7)
        self.at("relay claim")
        self.play(*Lv([gs[0], gl[0]]), run_time=0.8)
        self.at("somatostatin")
        self.play(*Lv(act, 1), run_time=0.4)
        self.play(*Lv(inh, 0.35), mv(O, scale=2.1, t=0.8), run_time=0.8)
        self.at("activation")
        self.play(gv(gs[0], 0.92), run_time=2.4)
        self.at("inhibition")
        self.play(*Lv(act, 0.35), *Lv(inh, 1), *Lv(O, 0.35), mv(O, scale=1.6, t=0.9), gv(gs[0], 0.25), run_time=1.0)
        self.at("mechanical")
        self.play(*Lv([gs[1], gl[1]]), run_time=0.8)
        self.at("thresholds")
        self.play(gv(gs[1], 0.2), run_time=2.0)
        self.at("thermal")
        self.play(*Lv([gs[2], gl[2]]), run_time=0.8)
        self.at("latency")
        self.play(gv(gs[2], 0.2), run_time=1.6)
        self.at("slice")
        self.play(*Lv(gs + gl, 0), *Lv([act, inh], 0), *Lv([box, tagm, llab, slab, schem]), mv(O, scale=1.4, t=1.0), run_time=1.0)
        self.at("driven")
        for k in range(6):
            self.play(*Lv(pl[k]), run_time=0.3)
            self.play(*Lv(sp[k]), run_time=0.25)
        self.finish()


# --- parvalbumin (s09, s10)
class S09Survival(Base):
    def construct(self):
        tag = txt("mouse, schematic", [-6.6, 3.35, 0], TEXT, 26, lvl=0, left=True)
        chipi = chipo("spared nerve injury", [1.0, 3.15, 0], YELLOW, 30)
        axis = Obj(Line([-5.4, -2.2, 0], [5.4, -2.2, 0], color=GREY, stroke_width=4), lvl=0)
        tlab = [txt(f"{n} weeks", [x, -2.8, 0], TEXT, 28, lvl=0) for n, x in zip([3, 5, 8], STX)]
        tick = [Obj(Line([x, -2.05, 0], [x, -2.35, 0], color=TEXT, stroke_width=4), lvl=0) for x in STX]
        groups = []
        for x in STX:
            cs = [cell([x + (c - 1) * 1.15, 0.8 - r * 1.15, 0], PURPLE, 0.46, lvl=0, phase=c + r) for r in range(2) for c in range(3)]
            groups.append(cs)
        pvlab = txt("parvalbumin neurons", [0, 1.9, 0], PURPLE, 32)
        nosig = txt("no significant fall", [0, -1.5, 0], TEAL, 32)
        # phase 2
        pv = cell([-4.2, 0.3, 0], PURPLE, 0.9, lvl=0, phase=1)
        axon = Obj(Line([-3.3, 0.3, 0], [0.4, 0.3, 0], color=PURPLE, stroke_width=10), lvl=0)
        syn = cell([0.4, 0.3, 0], PURPLE, 0.4, lvl=0, breathe=0.1)
        fl = Flow(Line([-3.3, 0.3, 0], [0.4, 0.3, 0]), PURPLE, axon, n=3, speed=0.2)
        gauge = Gauge(5.0, 0.9, lvl=0)
        glab = txt("injury\nhypersensitivity", [5.0, 2.4, 0], RED, 28)
        synlab = txt("synapse", [0.4, -0.45, 0], PURPLE, 30)
        qm = txt("?", [-3.0, 1.2, 0], YELLOW, 60)
        allg = [c for g in groups for c in g]
        self.add(tag, chipi, axis, *tlab, *tick, *allg, pvlab, nosig, pv, axon, syn, fl, gauge, glab, synlab, qm)
        pv.cur = 1.0
        for o in [tag, axis, *tick]:
            o.put(1)
        for o in tlab:
            o.put(0.4)
        self.wait(0.3)
        self.at("spared")
        self.play(*Lv(chipi), run_time=0.8)
        self.at("counts")
        for g in groups:
            self.play(*Lv(g), run_time=0.3)
        self.at("parvalbumin")
        self.play(*Lv(pvlab), run_time=0.8)
        self.at("significantly")
        self.play(*Lv(nosig), run_time=0.8)
        self.at("3")
        self.play(*Lv(tlab[0]), run_time=0.4)
        self.at("5")
        self.play(*Lv(tlab[1]), run_time=0.4)
        self.at("8")
        self.play(*Lv(tlab[2]), run_time=0.4)
        self.at("yet")
        self.play(*Lv([axis, *tick, *tlab, *allg, pvlab, nosig, chipi], 0), *Lv([pv, axon, syn]), *Lv([gauge, glab]), run_time=0.9)
        self.at("activating")
        fl.speed = 0.5
        self.play(mv(pv, scale=1.0, t=0.4), run_time=0.4)
        self.at("relieved")
        self.play(gv(gauge, 0.28), run_time=2.6)
        self.at("remained")
        self.ripple([-4.2, 0.3, 0], PURPLE, 0.6, 0.9)
        self.at("next question")
        self.play(*Lv(qm), run_time=0.5)
        self.play(mv(qm, [0.4, 1.3, 0], t=2.0))
        self.at("signal")
        self.play(*Lv(synlab), run_time=0.8)
        self.finish()


class S10Populations(Base):
    def construct(self):
        tag = txt("mouse assays", [-6.6, 3.35, 0], TEXT, 26, lvl=1, left=True)
        # carried from s09
        pv0 = cell([-4.2, 0.3, 0], PURPLE, 0.9, lvl=1, phase=1)
        g0 = Gauge(5.0, 0.28, lvl=1)
        glab0 = txt("injury\nhypersensitivity", [5.0, 2.4, 0], RED, 28, 1)
        # the split
        gx = [-1.4, 1.9, 5.2]
        lanes = [Gauge(x, 0.8, lvl=0, ph=i) for i, x in enumerate(gx)]
        llab = [txt(s, [x, 2.4, 0], RED, 28) for s, x in zip(["mechanical\nsensitivity", "heat\nsensitivity", "cold\nsensitivity"], gx)]
        pvc = cell([-4.7, 1.0, 0], PURPLE, 0.75, lvl=0, phase=1)
        pvl = txt("parvalbumin", [-4.7, -0.1, 0], PURPLE, 30)
        gl_el = Ellipse(width=3.2, height=1.7, stroke_color=PURPLE, stroke_width=5, fill_color=PURPLE, fill_opacity=0.3).move_to([-4.7, -1.8, 0])
        glc = Obj(gl_el, Dot(radius=0.3, color=PURPLE).move_to([-4.7, -1.8, 0]), lvl=0, breathe=0.07)
        gll = txt("glycinergic", [-4.7, -2.95, 0], PURPLE, 30)
        rings = [Obj(Rectangle(width=1.1, height=3.9, stroke_color=TEAL, stroke_width=5).move_to([x, -0.2, 0]), lvl=0) for x in gx]
        self.add(tag, g0, glab0, pv0, *lanes, *llab, pvc, pvl, glc, gll, *rings)
        pv0.cur = 1.0
        self.play(mv(pv0, [-4.7, 1.0, 0], scale=0.83, t=1.2), *Lv([g0, glab0], 0), *Lv(lanes + llab), *Lv([pvl, glc, gll], 0.5), run_time=1.4)
        self.play(*Lv(pvc, 0.5), run_time=0.1)
        self.remove(pv0)
        pvc.put(0.5)
        pvc.move_to([-4.7, 1.0, 0])
        self.add(pvc)
        self.at("parval")
        self.play(*Lv([pvc, pvl], 1), run_time=0.5)
        self.at("changed")
        self.play(gv(lanes[0], 0.25), run_time=2.6)
        self.at("thermal")
        self.play(*Lv(rings[1]), run_time=0.5)
        self.play(*Lv(rings[1], 0), run_time=0.8)
        self.at("broader")
        self.play(*Lv([pvc, pvl], 0.4), *Lv([glc, gll], 1), gv(lanes[0], 0.8), run_time=1.2)
        self.at("mechanical", nth=1)
        self.play(gv(lanes[0], 0.25), run_time=1.6)
        self.at("heat")
        self.play(gv(lanes[1], 0.25), run_time=1.4)
        self.at("cold")
        self.play(gv(lanes[2], 0.25), run_time=1.4)
        self.at("one gate")
        self.play(*Lv([glc, gll], 0.4), *Lv([pvc, pvl], 1), gv(lanes[1], 0.8), gv(lanes[2], 0.8), run_time=1.2)
        self.play(*Lv(rings[0]), run_time=0.6)
        self.finish()


class S11Rule(Base):
    def construct(self):
        w = world()
        hook_end(w)
        w.gauge.put(1)
        w.glab.put(1)
        for o in [w.Olab, w.Plab, w.Rlab]:
            o.put(0)
        w.panel.put(0)
        w.tag.put(1)
        oc = np.array([-0.8, 0.1, 0])
        q1 = Orbiter("which cells?", ORANGE, 1.4, oc, 3.8, 3.25)
        q2 = Orbiter("which tool?", PURPLE, 2.7, oc, 3.8, 3.25)
        q3 = Orbiter("which connection?", BLUE, 4.6, oc, 3.8, 3.25)
        for _q, _t in ((q1, [-1.4, 0.95, 0]), (q2, [-4.2, 1.75, 0]), (q3, [0.2, -2.5, 0])):
            _q.target = np.array(_t, float)
            _q.move_to(_q.target)
        self.add(*circuit_items(w), q1, q2, q3)
        w.gauge.val.set_value(0.85)
        # reassemble: pieces drift in
        offs = {w.O: [0, 2.0, 0], w.P: [-1.5, 1.5, 0], w.R: [1.5, 2.0, 0]}
        for o, d in offs.items():
            o.shift(np.array(d))
        for o in (w.O, w.P, w.R):
            o.put(0.0)
        self.play(*Lv([w.O, w.P, w.R, w.skin, w.fiber, w.OR, w.brake, w.route, w.gauge, w.glab, w.pulse], 1),
                  mv(w.O, OP, t=1.6), mv(w.P, PP, t=1.6), mv(w.R, RP, t=1.6), run_time=1.6)
        self.at("behavior")
        self.ripple([GX, 0.0, 0], RED, 0.5, 0.9)
        self.at("which")
        self.play(*Lv(q1), run_time=0.5)
        self.at("captured")
        q1.target = np.array([-1.4, 0.95, 0])
        self.play(*Lv(q2), run_time=0.5)
        self.at("tool")
        q2.target = np.array([-4.2, 1.75, 0])
        self.at("changed")
        self.play(*Lv(q3), run_time=0.5)
        self.at("measured")
        q3.target = np.array([0.2, -2.5, 0])
        self.at("identifies")
        self.ripple([GX, 0.0, 0], RED, 0.5, 0.9)
        self.at("circuit measurements")
        self.ripple([-3.3, -1.4, 0], BLUE, 0.4, 0.9)
        self.at("locate")
        self.ripple([-3.3, -1.4, 0], YELLOW, 0.4, 0.9)
        self.finish()


class S12End(EndCard):
    LINE = "Match behaviour to the tool and the circuit."
