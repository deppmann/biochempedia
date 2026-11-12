"""Wings Faster Than Nerves (Biochemistrypedia organismal biology film, chapter 2 of Muscle, Bone and Movement)

COLOUR MAP (same as chapter 1): actin BLUE, myosin ORANGE, calcium YELLOW, tropomyosin DARK GREY, troponin PURPLE,
ATP GREEN, Z disc BLACK bar, calcium store PALE TEAL. New here: nerve impulses RED, wingbeat ticks GREY,
thorax a CREAM springy box, the two power-muscle sets ORANGE-striped bands 'set A' and 'set B'.
Everything is a cartoon; the traces are schematic. Every swing and slide is driven by a tracker.
"""
import math
import numpy as np
from bp_style import *  # noqa: F401,F403

ORANGE = "#F29E4C"
PURPLE = "#B58CD9"
DGREY = "#7A8497"
TEALP = "#3FB8C0"
ZOUT = "#C9CED8"
PINK = "#E58FB3"
CREAM = "#F2E6C9"
SLATE = "#6B7690"
NERVE = "#9AA3B5"
PAPER = "#EDE6D3"
INK = "#1a1d27"

D0 = 5.2
THIN_LEN = 3.8
TY = 1.0
Y_COVER, Y_OFF = 0.86, 1.2
THICK_HALF = 2.5


def clamp(x, a=0.0, b=1.0):
    return max(a, min(b, x))


def bar(x1, x2, y, h, color, op=0.6):
    return RoundedRectangle(corner_radius=min(0.08, h / 2.2), width=abs(x2 - x1), height=h, stroke_color=color,
                            stroke_width=2, fill_color=color, fill_opacity=op).move_to([(x1 + x2) / 2, y, 0])


def rect(x1, x2, y, h, color, op=1.0):
    return Rectangle(width=abs(x2 - x1), height=h, stroke_width=0, fill_color=color, fill_opacity=op).move_to([(x1 + x2) / 2, y, 0])


def zdisc(x, h=4.4, w=0.2):
    return Rectangle(width=w, height=h, stroke_color=ZOUT, stroke_width=3, fill_color="#000000", fill_opacity=1).move_to([x, 0, 0])


def tmr():
    t = ValueTracker(0.0)
    t.add_updater(lambda m, dt: m.increment_value(dt))
    return t


def schedule(scene, tm, times, fn):
    st = {"i": 0}
    d = Mobject()

    def u(m, dt):
        while st["i"] < len(times) and tm.get_value() >= times[st["i"]]:
            fn(times[st["i"]], st["i"])
            st["i"] += 1
    d.add_updater(u)
    scene.add(d)
    return d


class Pulser(VGroup):
    """Red nerve impulses that travel along a path (p0fn -> p1fn); fire() sends one."""

    def __init__(self, p0fn, p1fn, dur=0.6, color=RED, r=0.2):
        super().__init__()
        self.p0, self.p1, self.dur, self.color, self.r = p0fn, p1fn, dur, color, r
        self.add_updater(self._u)

    def fire(self):
        d = VGroup(Dot(radius=self.r * 1.9, color=self.color).set_opacity(0.25), Dot(radius=self.r, color=self.color))
        d.s = 0.0
        self.add(d)
        d.move_to(np.array(self.p0(), dtype=float))

    def _u(self, m, dt):
        for d in list(self.submobjects):
            d.s += dt / self.dur
            if d.s >= 1:
                self.remove(d)
            else:
                a, b = np.array(self.p0(), dtype=float), np.array(self.p1(), dtype=float)
                d.move_to(a + (b - a) * d.s)


class Scroller(VGroup):
    """A trace that scrolls left; spawn() puts a mark at the right edge."""

    def __init__(self, XL, XR, speed):
        super().__init__()
        self.XL, self.XR, self.v = XL, XR, speed
        self.add_updater(self._u)

    def spawn(self, mob, op=1.0):
        mob._op = op
        self.add(mob)

    def _u(self, m, dt):
        for it in list(self.submobjects):
            it.shift(LEFT * self.v * dt)
            x = it.get_center()[0]
            if x < self.XL - 0.05:
                self.remove(it)
                continue
            it.set_stroke(opacity=clamp((x - self.XL) / 0.7) * it._op)


def tickmark(x, y0, y1, color=NERVE, w=6):
    l = Line([x, y0, 0], [x, y1, 0], color=color, stroke_width=w)
    l.set_cap_style(CapStyleType.ROUND)
    return l


def spike(x, base, h, color=RED, w=8):
    return tickmark(x, base, base + h, color, w)


def toggle_mobs(x, y, on):
    box = RoundedRectangle(corner_radius=0.3, width=1.4, height=0.64, stroke_color=YELLOW, stroke_width=5,
                           fill_color=YELLOW, fill_opacity=0.08 + 0.5 * on)
    knob = Circle(0.24, stroke_width=0, fill_color=YELLOW, fill_opacity=1).move_to([x - 0.38 + 0.76 * on, y, 0])
    return VGroup(box.move_to([x, y, 0]), knob)


def spring_pts(p0, p1, n=16, amp=0.1):
    p0, p1 = np.array(p0, dtype=float), np.array(p1, dtype=float)
    d = p1 - p0
    L = np.linalg.norm(d)
    if L < 1e-6:
        return [p0, p1]
    u = d / L
    nrm = np.array([-u[1], u[0], 0.0])
    pts = [p0]
    for k in range(1, n):
        pts.append(p0 + d * (k / n) + nrm * amp * (1 if k % 2 else -1))
    pts.append(p1)
    return pts


def spring(p0, p1, n=16, amp=0.1, color=CREAM, w=5):
    m = VMobject(stroke_color=color, stroke_width=w, fill_opacity=0)
    m.set_points_as_corners(spring_pts(p0, p1, n, amp))
    return m


def lab(text, size=30, color=TEXT, pos=(0, 0)):
    return T(text, size, color).move_to([pos[0], pos[1], 0])


# ---------------------------------------------------------------------------------------------
class Fly(VGroup):
    """An insect cartoon whose wings flap from the phase function ph() (cycles)."""

    def __init__(self, cx, cy, s=1.0, ph=None, kind="fly", amp=16, mid=28):
        super().__init__()
        P = lambda dx, dy: np.array([cx + dx * s, cy + dy * s, 0.0])
        self.root = P(0.15, 0.7)
        self.ph, self.amp, self.mid = ph, amp, mid
        self.wings = []
        wl, wh = (2.6, 0.55) if kind in ("locust", "wasp") else (2.4, 0.62)
        for k in range(2):
            w = Ellipse(width=wl * s, height=wh * s, stroke_color=TEXT, stroke_width=2, fill_color=WHITE, fill_opacity=0.32 - 0.1 * k)
            w.move_to(self.root + np.array([wl * s / 2, 0, 0]))
            w._k = k
            w._a = 0.0
            self.wings.append(w)
            w.add_updater(self._wu)
            self.add(w)
            self._wu(w, 0)
        body = VGroup()
        fo = dict(stroke_color=CREAM, stroke_width=2, fill_opacity=0.95)
        if kind == "beetle":
            body.add(Ellipse(width=3.0 * s, height=1.7 * s, fill_color="#46506a", **fo).move_to(P(0.9, 0.0)))
            body.add(Line(P(-0.6, 0.0), P(2.4, 0.0), color=CREAM, stroke_width=2))
            body.add(Circle(0.45 * s, fill_color=SLATE, **fo).move_to(P(-1.0, 0)))
            body.add(Dot(radius=0.09 * s, color=WHITE).move_to(P(-1.15, 0.1)))
        else:
            if kind == "bee":
                ab = Ellipse(width=2.5 * s, height=1.5 * s, fill_color=CREAM, **fo).move_to(P(1.5, -0.15))
                body.add(ab)
                for x in (1.0, 1.5, 2.0):
                    body.add(Line(P(x, -0.62), P(x, 0.32), color=SLATE, stroke_width=9 * s))
            elif kind == "wasp":
                body.add(Ellipse(width=2.9 * s, height=0.8 * s, fill_color=CREAM, **fo).move_to(P(1.9, -0.3)))
                for x in (1.5, 2.1, 2.7):
                    body.add(Line(P(x, -0.6), P(x, 0.0), color=SLATE, stroke_width=8 * s))
            elif kind == "locust":
                body.add(Ellipse(width=3.2 * s, height=0.85 * s, fill_color=SLATE, **fo).move_to(P(1.9, -0.15)))
            else:
                body.add(Ellipse(width=2.3 * s, height=1.25 * s, fill_color=SLATE, **fo).move_to(P(1.45, -0.2)))
            body.add(Circle(0.85 * s * (0.9 if kind == "wasp" else 1), fill_color=CREAM, **fo).move_to(P(0, 0)))
            body.add(Circle(0.5 * s, fill_color=SLATE, **fo).move_to(P(-1.2, -0.1)))
            body.add(Dot(radius=0.1 * s, color=WHITE).move_to(P(-1.35, 0.05)))
        self.add(body)

    def _wu(self, w, dt=0):
        if self.ph is None:
            a = math.radians(self.mid)
        else:
            a = math.radians(self.mid + self.amp * math.sin(2 * math.pi * (self.ph() + 0.1 * w._k)) + 12 * w._k)
        w.rotate(a - w._a, about_point=self.root)
        w._a = a


# ---------------------------------------------------------------------------------------------
class Sarc:
    """Chapter 1's sarcomere (same colour map and geometry), driven by trackers."""

    def __init__(self, sl=0.0, cover=False, A=0.0, ca=False):
        self.sl, self.A, self.tm = ValueTracker(sl), ValueTracker(A), ValueTracker(0.0)
        self.tm.add_updater(lambda m, dt: m.increment_value(dt))
        self.zl, self.zr = zdisc(-D0), zdisc(D0)
        self.rods, self.notches, self.strands, self.trns, self.dots, self.meta = [], [], [], [], [], []
        sides = {-1: [self.zl], 1: [self.zr]}
        for side in (-1, 1):
            for vert in (1, -1):
                rod = bar(side * D0, side * (D0 - THIN_LEN), vert * TY, 0.26, BLUE, 0.75)
                xs = [(-2.7 + 0.4 * k) for k in range(-5, 4)]
                nt = VGroup(*[Square(0.13, stroke_width=0, fill_color=WHITE, fill_opacity=0.95).move_to([(x if side < 0 else -x), vert * 0.87, 0]) for x in xs])
                yc = vert * Y_COVER
                st = Line([side * (D0 - 0.3), yc, 0], [side * (D0 - THIN_LEN + 0.1), yc, 0], color=DGREY, stroke_width=11)
                st.set_cap_style(CapStyleType.ROUND)
                bx = [side * (D0 - 1.1), side * (D0 - 2.5)]
                trn = VGroup(*[Square(0.32, stroke_width=2, stroke_color=PURPLE, fill_color=PURPLE, fill_opacity=0.95).move_to([x, yc, 0]) for x in bx])
                if not cover:
                    st.shift(UP * vert * (Y_OFF - Y_COVER))
                    trn.shift(UP * vert * (Y_OFF - Y_COVER))
                parts = [rod, nt, st, trn]
                if ca:
                    ds = VGroup(*[Circle(0.13, stroke_width=0, fill_color=YELLOW, fill_opacity=1).move_to([x, vert * (Y_OFF + 0.3), 0]) for x in bx])
                    self.dots.append(ds)
                    parts.append(ds)
                    for dd in ds:
                        dd._y0 = dd.get_center()[1]
                        dd._xx = dd.get_center()[0]
                        dd.add_updater(lambda m: m.set_y(m._y0 + 0.16 * math.sin(self.tm.get_value() * 2.2 + 3 * m._xx)))
                self.rods.append(rod); self.notches.append(nt); self.strands.append(st); self.trns.append(trn)
                self.meta.append((side, vert))
                sides[side].extend(parts)
        for side, ms in sides.items():
            for m in ms:
                self._slide(m, side)
        self.thick = bar(-THICK_HALF, THICK_HALF, 0, 0.64, ORANGE, 0.6)
        self.heads = VGroup()
        j0 = 0
        for side in (-1, 1):
            for vert in (1, -1):
                for j in range(5):
                    h = Line(ORIGIN, RIGHT, color=ORANGE, stroke_width=9)
                    h.set_cap_style(CapStyleType.ROUND)
                    phi = 0.4 * ((j * 0.37 + (0.21 if vert > 0 else 0) + (0.13 if side > 0 else 0)) % 1.0)
                    h.add_updater(self._head_upd(side, vert, -2.4 + 0.4 * j, phi, j0))
                    h.put_start_and_end_on([0, 0, 0], [0.2, 0, 0])
                    self.heads.add(h)
                    j0 += 1
        self.z = VGroup(self.zl, self.zr)

    def _slide(self, m, side):
        m._x0 = m.get_center()[0]
        m.add_updater(lambda mm: mm.shift(RIGHT * ((mm._x0 - side * self.sl.get_value()) - mm.get_center()[0])))

    def _head_upd(self, side, vert, x0, phi, j):
        sg = 1 if side < 0 else -1

        def upd(m):
            sl, A, t = self.sl.get_value(), self.A.get_value(), self.tm.get_value()
            p = ((sl + phi) % 0.4) / 0.4
            xs = x0 - 0.3 - phi
            if p < 0.8:
                xb, yb = xs + 0.4 * p, 0.88
            else:
                q = (p - 0.8) / 0.2
                xb, yb = xs + 0.32 * (1 - q), 0.88 - 0.24 * math.sin(math.pi * q)
            tipx = -D0 + THIN_LEN + sl
            a = A if xb < tipx - 0.05 else 0.0
            xf = x0 - 0.3 + 0.05 * math.cos(t * 2 + j)
            yf = 0.64 + 0.04 * math.sin(t * 2.3 + j)
            x, y = xf + (xb - xf) * a, yf + (yb - yf) * a
            m.put_start_and_end_on([sg * x0, vert * 0.32, 0], [sg * x, vert * y, 0])
        return upd

    def start(self, scene):
        scene.add(self.sl, self.A, self.tm)

    def everything(self):
        return VGroup(self.z, *self.rods, *self.notches, *self.strands, *self.trns, self.thick, self.heads, *self.dots)


def chain_mobs(cx, cy, w, zh, c, shr=0.17):
    """One sarcomere (chapter 1's compact drawing); c in 0..1 is how far it has shortened."""
    f = 1 - shr * c
    half = w / 2
    zs = [cx + (-half) * f, cx + half * f]
    zw = max(0.07, 0.06 * zh)
    th, hn, off = 0.17 * zh, 0.09 * zh, 0.25 * zh
    g = VGroup()
    mid = (zs[0] + zs[1]) / 2
    g.add(rect(mid - 0.295 * w, mid + 0.295 * w, cy, th, ORANGE, 0.85))
    for y in (cy + off, cy - off):
        g.add(rect(zs[0], zs[0] + 0.42 * w, y, hn, BLUE, 0.9))
        g.add(rect(zs[1] - 0.42 * w, zs[1], y, hn, BLUE, 0.9))
    for z in zs:
        g.add(Rectangle(width=zw, height=zh, stroke_color=ZOUT, stroke_width=2, fill_color="#000000", fill_opacity=1).move_to([z, cy, 0]))
    return g


# ---------------------------------------------------------------------------------------------
class Thorax:
    """The one world of the second half: a springy CREAM box, set A (front to back) and set B
    (top to bottom), hinged wings, calcium dots. The tracker u in -1..1 is set A shortened (+1) or set B shortened (-1)."""
    CX = 0.0

    def __init__(self, cy=-0.9, u0=0.0, fa=0.45, fb=0.45, ca=0.0, jit=0.04):
        self.cy = cy
        self.u, self.fa, self.fb, self.ca = ValueTracker(u0), ValueTracker(fa), ValueTracker(fb), ValueTracker(ca)
        self.dr, self.amp, self.ck = ValueTracker(0.0), ValueTracker(1.0), ValueTracker(0.0)
        self.tm = tmr()
        self.jit = jit
        self.runner = None
        self.ckpos = ValueTracker(0.0)    # 0 = clock on set B, 1 = clock on set A
        self.ckon = ValueTracker(0.0)
        self.v = {k: ValueTracker(1.0) for k in ('box', 'A', 'B', 'wing')}
        self.box = always_redraw(self._box)
        self.A = always_redraw(self._bandA)
        self.B = always_redraw(self._bandB)
        self.wl = always_redraw(lambda: self._wing(-1))
        self.wr = always_redraw(lambda: self._wing(1))
        self.dots = always_redraw(self._dots)
        self.clock = always_redraw(self._clock)

    def ue(self):
        return self.u.get_value() + self.jit * math.sin(self.tm.get_value() * 2.6)

    def W(self): return 7.4 - 1.0 * self.ue()
    def H(self): return 3.6 + 0.5 * self.ue()
    def L(self): return self.CX - self.W() / 2
    def R(self): return self.CX + self.W() / 2
    def roof(self): return self.cy + self.H() / 2
    def floor(self): return self.cy - self.H() / 2

    def _box(self):
        L, R, rf, fl = self.L(), self.R(), self.roof(), self.floor()
        g = VGroup(spring([L, rf, 0], [R, rf, 0], 22), spring([L, fl, 0], [R, fl, 0], 22),
                   spring([L, fl, 0], [L, rf, 0], 14), spring([R, fl, 0], [R, rf, 0], 14))
        g.set_stroke(opacity=self.v['box'].get_value())
        return g

    def _band_style(self, f, v):
        return dict(stroke_color=ORANGE, stroke_width=3, fill_color=ORANGE, fill_opacity=clamp(f, 0.15, 1.0) * v, stroke_opacity=v)

    def _bandA(self):
        x0, x1, y = self.L() + 0.15, self.R() - 0.15, self.cy + 0.3
        g = VGroup(RoundedRectangle(corner_radius=0.17, width=x1 - x0, height=0.58, **self._band_style(self.fa.get_value(), self.v['A'].get_value())).move_to([(x0 + x1) / 2, y, 0]))
        n = int((x1 - x0) / 0.32)
        for k in range(1, n):
            x = x0 + (x1 - x0) * k / n
            g.add(Line([x, y - 0.2, 0], [x, y + 0.2, 0], color="#5a3510", stroke_width=3).set_opacity(0.55 * self.v['A'].get_value()))
        return g

    def _bandB(self):
        y0, y1, x = self.floor() + 0.15, self.roof() - 0.15, self.CX
        g = VGroup(RoundedRectangle(corner_radius=0.17, width=0.58, height=y1 - y0, **self._band_style(self.fb.get_value(), self.v['B'].get_value())).move_to([x, (y0 + y1) / 2, 0]))
        n = int((y1 - y0) / 0.32)
        for k in range(1, n):
            y = y0 + (y1 - y0) * k / n
            g.add(Line([x - 0.2, y, 0], [x + 0.2, y, 0], color="#5a3510", stroke_width=3).set_opacity(0.55 * self.v['B'].get_value()))
        return g

    def _wing(self, side):
        th = math.radians(8 + 34 * (clamp(self.ue(), -1.2, 1.2) + 1) / 2)
        root = np.array([self.L() if side < 0 else self.R(), self.roof(), 0.0])
        wv = self.v['wing'].get_value()
        e = Ellipse(width=2.3, height=0.62, stroke_color=TEXT, stroke_width=2, fill_color=WHITE, fill_opacity=0.3 * wv, stroke_opacity=wv)
        e.move_to(root + np.array([1.15 * side * math.cos(th), 1.15 * math.sin(th), 0]))
        e.rotate(side * th)
        return VGroup(e, Dot(root, radius=0.1, color=CREAM).set_opacity(wv))

    def _dots(self):
        a = self.ca.get_value()
        dr = self.dr.get_value()
        t = self.tm.get_value()
        g = VGroup()
        if a * (1 - dr) < 0.02:
            return g
        x0, x1, ya = self.L() + 0.5, self.R() - 0.5, self.cy + 0.3
        yb0, yb1 = self.floor() + 0.5, self.roof() - 0.5
        for k in range(8):
            s = 0.04 + 0.92 * k / 7
            x = x0 + (x1 - x0) * s + 0.08 * math.sin(1.7 * t + k)
            y = ya + 0.1 * math.sin(2.1 * t + 2 * k) - dr * (1.0 + 0.3 * k)
            g.add(Dot([x, y, 0], radius=0.12, color=YELLOW))
        for k in range(6):
            s = 0.05 + 0.9 * k / 5
            y = yb0 + (yb1 - yb0) * s + 0.08 * math.sin(1.9 * t + 3 * k)
            x = self.CX + 0.1 * math.sin(2.3 * t + k) - dr * (0.2 * (k % 3 - 1))
            g.add(Dot([x, y - dr * (1.2 + 0.25 * k), 0], radius=0.12, color=YELLOW))
        g.set_opacity(a * (1 - dr))
        return g

    def _clock(self):
        on = self.ckon.get_value()
        if on < 0.02:
            return VGroup()
        if self.ckpos.get_value() < 0.5:
            c = np.array([self.CX + 0.95, self.cy - 0.55, 0.0])
        else:
            c = np.array([self.CX - 1.0, self.cy - 0.45, 0.0])
        a = -2 * math.pi * self.ck.get_value()
        ring = Circle(0.34, stroke_color=TEXT, stroke_width=4, fill_color="#0f1117", fill_opacity=1).move_to(c)
        hand = Line(c, c + 0.26 * np.array([math.sin(a), math.cos(a), 0]), color=TEXT, stroke_width=4)
        g = VGroup(ring, hand, Dot(c, radius=0.04, color=TEXT))
        g.set_opacity(on)
        return g

    def trackers(self):
        return [self.u, self.fa, self.fb, self.ca, self.dr, self.amp, self.ck, self.ckpos, self.ckon, self.tm] + list(self.v.values())

    def start(self, scene, show=True):
        scene.add(*self.trackers())
        if show:
            scene.add(self.box, self.A, self.B, self.wl, self.wr, self.dots, self.clock)

    def run(self, scene, period=1.7):
        t0 = self.tm.get_value()
        d = Mobject()

        def u(m, dt):
            ph = 2 * math.pi * (self.tm.get_value() - t0) / period
            a = self.amp.get_value()
            self.u.set_value(a * math.cos(ph))
            self.fa.set_value(0.45 + a * 0.45 * (0.5 + 0.5 * math.cos(ph - 0.7)))
            self.fb.set_value(0.45 + a * 0.45 * (0.5 + 0.5 * math.cos(ph - 0.7 + math.pi)))
        d.add_updater(u)
        scene.add(d)
        self.runner = d

    def labels_ab(self):
        la = T("set A", 30, ORANGE).move_to([self.CX - 2.0, self.cy + 0.95, 0])
        lb = T("set B", 30, ORANGE).move_to([self.CX + 1.15, self.cy + 1.2, 0])
        return la, lb


def nerve_cable(world, cut, vis=None):
    """The nerve running into the left wall of the thorax; `cut` in 0..1 opens a gap."""
    def mk():
        y = world.cy
        c = cut.get_value()
        o = 1.0 if vis is None else vis.get_value()
        if c < 0.01:
            return Line([-6.5, y, 0], [world.L(), y, 0], color=NERVE, stroke_width=14, stroke_opacity=o)
        g = VGroup(Line([-6.5, y, 0], [-5.3 - 0.3 * c, y, 0], color=NERVE, stroke_width=14),
                   Line([-5.0 + 0.3 * c, y, 0], [world.L(), y, 0], color=NERVE, stroke_width=14))
        return g
    return always_redraw(mk)


# ---------------------------------------------------------------------------------------------
# the compact trace window (s03, s04) and the big one (s05-s07)
CXL, CXR = -4.5, 6.3


def compact_window():
    win = Rectangle(width=11.0, height=2.2, stroke_color=GREY, stroke_width=2, fill_color="#151821", fill_opacity=1).move_to([0.9, -2.4, 0])
    base = Line([CXL, -3.2, 0], [CXR, -3.2, 0], color=GREY, stroke_width=2).set_opacity(0.5)
    return win, base


BX0, BX1 = -6.2, 6.2
TICK_X = [-5.7 + 0.6 * k for k in range(20)]
TALL_X = [-4.2, -1.2, 2.4, 4.8]
TALL_H = [1.75, 1.95, 1.65, 1.85]
B_BASE = -2.3


def big_window():
    win = Rectangle(width=12.4, height=4.5, stroke_color=GREY, stroke_width=2, fill_color="#151821", fill_opacity=1).move_to([0, -0.65, 0])
    base = Line([BX0 + 0.1, B_BASE, 0], [BX1 - 0.1, B_BASE, 0], color=GREY, stroke_width=2).set_opacity(0.5)
    return win, base


def big_ticks():
    return VGroup(*[tickmark(x, 1.0, 1.5, NERVE, 7) for x in TICK_X])


def big_dashes():
    g = VGroup()
    for x in TICK_X:
        r = Rectangle(width=0.34, height=1.9, stroke_color=RED, stroke_width=3).move_to([x, B_BASE + 0.95, 0])
        g.add(DashedVMobject(r, num_dashes=18))
    return g


def shimmer(g, base=0.8, amp=0.2, sp=3.0):
    t = [0.0]

    def u(m, dt):
        t[0] += dt
        m.set_stroke(opacity=base + amp * math.sin(t[0] * sp))
    g.add_updater(u)


# ---------------------------------------------------------------------------------------------
class S00Title(TitleCard):
    LESSON = "Muscle, Bone and Movement"
    TITLE = "Wings Faster Than Nerves"


class S01Hook(SpokenScene):
    def construct(self):
        tm, ph = tmr(), ValueTracker(0.0)
        st = {"last": 0, "n": 0, "sparse": False}
        fly = Fly(1.4, 0.35, 1.3, ph=lambda: ph.get_value(), amp=17, mid=30)
        cable = Line([-6.4, -1.8, 0], [1.1, -0.7, 0], color=NERVE, stroke_width=14)
        nl = lab("nerve", 30, NERVE, (-5.0, -1.2))
        pul = Pulser(lambda: (-6.4, -1.8, 0), lambda: (1.1, -0.7, 0), dur=0.55)
        drv = Mobject()

        def u(m, dt):
            t = tm.get_value()
            f = 1.1 if t < 3.8 else 1.1 + 1.6 * clamp((t - 3.8) / 1.8)
            ph.increment_value(dt * f)
            k = int(math.floor(ph.get_value()))
            if k > st["last"]:
                st["last"] = k
                st["n"] += 1
                if (not st["sparse"]) or st["n"] % 3 == 0:
                    pul.fire()
        drv.add_updater(u)
        self.add(tm, ph, drv, pul)
        self.play(FadeIn(fly), FadeIn(cable), FadeIn(nl), run_time=0.8)
        self.at("so fast", lead=0.0)
        st["sparse"] = True
        self.at("seemed in doubt", lead=0.3)
        card = chip("One impulse per beat?", TEXT, 36).move_to([0.5, -3.2, 0])
        self.play(FadeIn(card, shift=UP * 0.1), run_time=0.7)
        self.finish()


class S02Link(SpokenScene):
    def construct(self):
        s = Sarc(sl=0.0, cover=True, ca=True)
        s.start(self)
        for ds in s.dots:
            ds.set_opacity(0)
        ev = s.everything()
        self.play(FadeIn(ev), run_time=1.0)
        self.at("calcium switches", lead=0.3)
        lc = lab("calcium", 34, YELLOW, (0, 2.95))
        self.play(*[ds.animate.set_opacity(1) for ds in s.dots], FadeIn(lc, shift=DOWN * 0.1), run_time=0.8)
        d = Y_OFF - Y_COVER
        self.play(*[m.animate.shift(UP * vert * d) for (side, vert), m in zip(s.meta, s.strands)],
                  *[m.animate.shift(UP * vert * d) for (side, vert), m in zip(s.meta, s.trns)], run_time=1.0)
        self.at("myosin heads pull", lead=0.4)
        lh = lab("heads pull actin", 32, ORANGE, (0, -3.05))
        self.play(s.A.animate.set_value(1.0), FadeIn(lh, shift=UP * 0.1), run_time=0.8)
        self.play(s.sl.animate.set_value(1.0), run_time=1.6, rate_func=linear)
        self.at("now the question", lead=0.3)
        tg = toggle_mobs(0, 0.0, 1.0).scale(1.6)
        self.play(FadeOut(lc), FadeOut(lh), GrowFromCenter(tg), run_time=0.9)
        self.at("fly's", lead=0.3)
        tm = tmr()
        fly = Fly(2.4, 0.2, 1.1, ph=lambda: tm.get_value() * 2.2, amp=16, mid=30)
        self.add(tm)
        self.play(FadeOut(ev), tg.animate.scale(1 / 1.6).move_to([-3.2, 0.2, 0]), FadeIn(fly), run_time=1.4)
        self.at("throws that switch", lead=0.1)
        q = lab("?", 54, YELLOW, (-3.2, 1.3))
        self.play(FadeIn(q, shift=DOWN * 0.1), run_time=0.6)
        self.finish()


class S03Rule(SpokenScene):
    def construct(self):
        P = 1.4
        tm = tmr()
        ph = lambda: (tm.get_value() - 0.35) / P + 0.25
        win, base = compact_window()
        scr = Scroller(CXL, CXR, 1.3)
        l1 = lab("wingbeat", 26, NERVE, (-5.65, -1.8))
        l2 = lab("impulse", 26, RED, (-5.65, -2.9))

        def mk(t, i):
            x = CXR - 0.05
            scr.spawn(tickmark(x, -1.55, -1.95, NERVE, 6))
            scr.spawn(tickmark(x, -2.0, -2.45, GREY, 2), 0.7)
            scr.spawn(spike(x, -3.2, 0.75))
        times = [0.35 + P * k for k in range(12)]
        schedule(self, tm, times, mk)
        musc = always_redraw(lambda: Ellipse(width=6 * (1 - 0.22 * (0.5 + 0.5 * math.sin(2 * math.pi * ph()))), height=1.1, stroke_color=RED,
                                             stroke_width=2, fill_color=RED, fill_opacity=0.65).move_to([0.4, 1.1, 0]))
        lm = lab("skeletal muscle", 30, RED, (0.4, -0.7))
        self.add(tm, win, base, scr)
        self.play(FadeIn(win), FadeIn(base), FadeIn(l1), FadeIn(l2), FadeIn(musc), run_time=0.8)
        self.at("vertebrate skeletal", lead=0.0)
        self.play(FadeIn(lm, shift=UP * 0.1), run_time=0.5)
        self.at("so does the flight", lead=0.3)
        self.remove(musc)
        locust = Fly(0.0, 0.45, 1.0, ph=ph, kind="locust", amp=15, mid=30)
        ll = lab("locust", 30, TEXT, (0.4, -0.7))
        self.play(FadeOut(musc), FadeOut(lm), FadeIn(locust), FadeIn(ll), run_time=0.8)
        self.at("this is called", lead=0.3)
        top = lab("synchronous: one impulse, one contraction", 32, YELLOW, (0, 3.55))
        self.play(FadeIn(top, shift=DOWN * 0.1), run_time=0.7)
        self.finish()


class S04Pringle(SpokenScene):
    def construct(self):
        tm = tmr()
        ph = lambda: tm.get_value() * 2.0
        cap = lab("J. W. S. Pringle, 1949", 30, TEXT, (-3.9, 3.35))
        self.add(tm)
        self.play(FadeIn(cap, shift=DOWN * 0.1), run_time=0.7)
        self.at("blue bottle flies", lead=0.3)
        fly = Fly(-1.0, 0.5, 1.0, ph=ph, amp=17, mid=30)
        self.play(FadeIn(fly), run_time=0.9)
        self.at("tethered", lead=0.1)
        rod = Line([-1.23, 1.35, 0], [-1.23, 3.2, 0], color=DGREY, stroke_width=14)
        rl = lab("rod glued to its back", 24, DGREY, (-3.2, 2.0))
        self.play(Create(rod), FadeIn(rl), run_time=1.2)
        self.at("then he put", lead=0.2)
        win, base = compact_window()
        scr = Scroller(CXL, CXR, 1.6)
        t_open = self.t_of("then he put")
        schedule(self, tm, [t_open + 0.8 + 0.5 * k for k in range(10)], lambda t, i: scr.spawn(tickmark(CXR - 0.05, -1.55, -1.95, NERVE, 6)))
        self.add(scr)
        win.set_z_index(-1); base.set_z_index(-1)
        self.play(FadeOut(rl), FadeIn(win), FadeIn(base), run_time=0.8)
        self.at("electrode", lead=0.6)
        needle = Line([3.2, -1.0, 0], [-0.7, -0.05, 0], color=ZOUT, stroke_width=5)
        self.play(Create(needle), run_time=1.0)
        self.at("into its flight", lead=0.0)
        box = RoundedRectangle(corner_radius=0.15, width=2.4, height=1.2, stroke_color=GREY, stroke_width=3, fill_color="#151821", fill_opacity=1).move_to([5.3, 0.1, 0])
        bl = lab("recorder", 28, TEXT, (5.3, 0.1))
        wire = CubicBezier([3.2, -1.0, 0], [3.9, -1.3, 0], [3.9, 0.1, 0], [4.1, 0.1, 0], color=ZOUT, stroke_width=4)
        self.play(Create(wire), FadeIn(box), FadeIn(bl), run_time=0.9)
        self.finish()


class S05Predict(SpokenScene):
    def construct(self):
        tm = tmr()
        win, base = big_window()
        ticks = big_ticks()
        self.add(tm, win, base)
        self.play(LaggedStart(*[FadeIn(t) for t in ticks], lag_ratio=0.1), run_time=2.4)
        self.at("the trace should show", lead=0.3)
        dashes = big_dashes()
        shimmer(dashes)
        self.play(LaggedStart(*[FadeIn(d) for d in dashes], lag_ratio=0.08), run_time=1.5)
        self.at("one large spike", lead=0.6)
        pl = lab("predicted: one large spike per beat", 32, RED, (0, 3.25))
        self.play(FadeIn(pl, shift=DOWN * 0.1), run_time=0.7)
        self.at("what do you think", lead=0.2)
        card = chip("What did he see?", TEXT, 34).move_to([0, -3.4, 0])
        self.play(FadeIn(card, shift=UP * 0.1), run_time=0.7)
        self.finish()


class S06Pause(NarratedScene):
    def construct(self):
        win, base = big_window()
        ticks = big_ticks()
        dashes = big_dashes()
        shimmer(dashes)
        pl = lab("predicted: one large spike per beat", 32, RED, (0, 3.25))
        card = chip("What did he see?", TEXT, 34).move_to([0, -3.4, 0])
        cc = np.array([6.0, -3.35, 0.0])
        t = ValueTracker(0.0)
        t.add_updater(lambda m, dt: m.increment_value(dt))
        ring = always_redraw(lambda: VGroup(
            Circle(0.32, stroke_color=GREY, stroke_width=4).move_to(cc),
            Arc(radius=0.32, start_angle=PI / 2, angle=-2 * PI * clamp(t.get_value() / 5.0), stroke_color=TEXT, stroke_width=6, arc_center=cc)))
        self.add(t, win, base, ticks, dashes, pl, card, ring)
        self.finish()


class S07Reveal(SpokenScene):
    def construct(self):
        win, base = big_window()
        ticks = big_ticks()
        dashes = big_dashes()
        shimmer(dashes)
        pl = lab("predicted: one large spike per beat", 32, RED, (0, 3.25))
        card = chip("What did he see?", TEXT, 34).move_to([0, -3.4, 0])
        blips = VGroup(*[tickmark(x + 0.04 * ((k * 7) % 5 - 2), B_BASE, B_BASE + 0.28, PINK, 5) for k, x in enumerate(TICK_X)])
        talls = VGroup(*[spike(x, B_BASE, h) for x, h in zip(TALL_X, TALL_H)])
        for m in list(blips) + list(talls):
            m.set_stroke(opacity=0)
        self.add(win, base, ticks, dashes, pl, card, blips, talls)
        self.wait(0.2)
        self.play(FadeOut(dashes), FadeOut(pl), FadeOut(card), run_time=1.0)
        cur = Line([BX0, B_BASE - 0.2, 0], [BX0, 1.7, 0], color=WHITE, stroke_width=3)
        cur.set_z_index(5)
        allm = [(m, m.get_center()[0]) for m in list(blips) + list(talls)]

        def cu(m, dt):
            x = m.get_center()[0]
            for mm, xx in allm:
                if xx <= x:
                    mm.set_stroke(opacity=1.0)
        cur.add_updater(cu)
        self.add(cur)
        t_sw = self.t_of("far less often") + 1.6
        sch = lab("schematic trace: far fewer large spikes than wingbeats", 28, TEXT, (0, 3.25))
        self.play(cur.animate.shift(RIGHT * (BX1 - 0.3 - BX0)), run_time=max(3.0, t_sw - self.elapsed()), rate_func=linear)
        self.play(FadeOut(cur), run_time=0.3)
        self.add(sch)
        sch.set_opacity(0)
        self.play(sch.animate.set_opacity(1), run_time=0.5)
        self.at("not timed", lead=0.2)
        drops = VGroup()
        for x in TALL_X:
            d = DashedVMobject(Line([x, B_BASE + 2.0, 0], [x, 0.95, 0], color=NERVE, stroke_width=3), num_dashes=8)
            drops.add(d)
        self.play(Create(drops), run_time=1.2)
        talls_pulse = [0.0]

        def tp(m, dt):
            talls_pulse[0] += dt
            m.set_stroke(opacity=0.75 + 0.25 * math.sin(talls_pulse[0] * 4))
        talls.add_updater(tp)
        self.at("one to one rule", lead=0.2)
        fin = lab("the one-to-one rule failed", 40, RED, (0, 3.25))
        self.play(FadeOut(sch), FadeIn(fin, shift=DOWN * 0.1), run_time=0.8)
        self.finish()


# ---------------------------------------------------------------------------------------------
class S08Thorax(SpokenScene):
    def construct(self):
        w = Thorax(u0=0.0, jit=0.12)
        for k in ('box', 'A', 'B', 'wing'):
            w.v[k].set_value(0.0)
        w.start(self)
        self.at("picture", lead=0.4)
        self.play(w.v['box'].animate.set_value(1.0), w.v['wing'].animate.set_value(1.0), run_time=1.2)
        la, lb = w.labels_ab()
        self.at("springy box", lead=0.0)
        tl = lab("thorax: a springy box", 34, CREAM, (0, 3.3))
        self.play(FadeIn(tl, shift=DOWN * 0.1), run_time=0.7)
        self.at("two sets", lead=0.3)
        self.play(w.v['A'].animate.set_value(1.0), run_time=0.8)
        self.play(FadeIn(la), run_time=0.4)
        self.at("pull on it in different", lead=0.6)
        self.play(w.v['B'].animate.set_value(1.0), run_time=0.8)
        self.play(FadeIn(lb), run_time=0.4)
        self.finish()


class S09Stretch(SpokenScene):
    def construct(self):
        w = Thorax(u0=0.0, jit=0.05)
        w.start(self)
        la, lb = w.labels_ab()
        self.add(la, lb)
        self.at("shortens", lead=0.6)
        self.play(w.u.animate.set_value(1.0), w.fa.animate.set_value(0.85), run_time=1.7)
        self.at("is stretched", lead=0.4)
        ls = lab("stretched", 30, TEXT, (w.CX + 1.6, w.cy - 1.3))
        self.play(FadeIn(ls), run_time=0.5)
        self.at("these muscles", lead=0.2)
        sw = lab("already switched on", 34, YELLOW, (0, 3.35))
        self.play(w.ca.animate.set_value(1.0), FadeIn(sw, shift=DOWN * 0.1), run_time=1.2)
        self.at("stretch raises force", lead=0.5)
        dl = lab("stretch, then delay, then more force", 32, TEXT, (0, -3.45))
        w.ckpos.set_value(0.0)
        self.play(FadeOut(sw), FadeIn(dl, shift=UP * 0.1), w.ckon.animate.set_value(1.0), run_time=0.7)
        self.at("after a short delay", lead=0.0)
        self.play(w.ck.animate.set_value(1.0), run_time=1.7, rate_func=linear)
        self.play(w.fb.animate.set_value(0.9), run_time=0.6)
        self.finish()


class S10Cycle(SpokenScene):
    def construct(self):
        w = Thorax(u0=1.0, fa=0.85, fb=0.9, ca=1.0, jit=0.04)
        w.ckon.set_value(1.0); w.ck.set_value(1.0)
        w.start(self)
        la, lb = w.labels_ab()
        self.add(la, lb)
        self.at("shortens", lead=0.5)
        lsB = lab("stretched", 30, TEXT, (w.CX + 1.6, w.cy - 1.3))
        self.add(lsB)
        self.play(FadeOut(lsB), run_time=0.25)
        self.play(w.u.animate.set_value(-1.0), w.fb.animate.set_value(0.95), w.fa.animate.set_value(0.45), w.ckon.animate.set_value(0.0), run_time=1.35)
        self.at("stretches the first set", lead=0.4)
        lsA = lab("stretched", 30, TEXT, (w.CX - 2.6, w.cy - 0.45))
        w.ckpos.set_value(1.0)
        w.ck.set_value(0.0)
        self.play(FadeIn(lsA), w.ckon.animate.set_value(1.0), run_time=0.6)
        self.play(w.ck.animate.set_value(1.0), run_time=1.3, rate_func=linear)
        self.play(w.fa.animate.set_value(0.95), w.fb.animate.set_value(0.45), w.u.animate.set_value(1.0), FadeOut(lsA), w.ckon.animate.set_value(0.0), run_time=1.3)
        self.at("the muscles and the springy", lead=0.1)
        w.run(self, 1.7)
        lp = lab("muscle + thorax set the beat", 32, TEXT, (0.6, -3.45))
        arr = Arc(radius=0.34, angle=4.6, stroke_color=TEXT, stroke_width=6).add_tip(tip_length=0.2).move_to([-3.2, -3.45, 0])
        self.play(FadeIn(lp, shift=UP * 0.1), FadeIn(arr), run_time=0.7)
        self.play(Rotate(arr, angle=-2 * PI, run_time=4.0, rate_func=linear))
        self.finish()


class S11Name(SpokenScene):
    def construct(self):
        tm = tmr()
        self.add(tm)
        kinds = [("fly", "flies", -5.0), ("bee", "bees", -1.7), ("wasp", "wasps", 1.7), ("beetle", "beetles", 5.0)]
        top = lab("asynchronous muscle", 46, YELLOW, (0, 3.0))
        self.at("asynchronous", lead=0.1)
        self.play(FadeIn(top, shift=DOWN * 0.1), run_time=0.8)
        ins = []
        for i, (k, name, x) in enumerate(kinds):
            f = Fly(x - 0.6, 0.3, 0.65, ph=(lambda i=i: tm.get_value() * (2.2 + 0.4 * i)), kind=k, amp=16, mid=30)
            ins.append(f)
        labs = [lab(n, 32, TEXT, (x, -1.0)) for k, n, x in kinds]
        self.at("flies", lead=0.4)
        self.play(FadeIn(ins[0]), FadeIn(labs[0]), run_time=0.7)
        self.at("bees", lead=0.4)
        self.play(FadeIn(ins[1]), FadeIn(labs[1]), run_time=0.7)
        self.at("wasps", lead=0.4)
        self.play(FadeIn(ins[2]), FadeIn(labs[2]), run_time=0.7)
        self.at("beetles", lead=0.4)
        self.play(FadeIn(ins[3]), FadeIn(labs[3]), run_time=0.7)
        self.at("1959", lead=0.3)
        c1 = lab("Machin and Pringle, 1959", 32, TEXT, (0, -2.1))
        c2 = lab("isolated beetle flight muscle is activated by stretch", 28, TEXT, (0, -2.8))
        self.play(FadeIn(c1, shift=UP * 0.1), run_time=0.7)
        self.at("beetle flight", lead=1.0)
        ring = SurroundingRectangle(VGroup(ins[3], labs[3]), color=ORANGE, buff=0.2, stroke_width=4)
        self.play(FadeIn(c2, shift=UP * 0.1), Create(ring), run_time=0.9)
        self.finish()


class S12Nerve(SpokenScene):
    def construct(self):
        w = Thorax(u0=1.0, fa=0.85, fb=0.45, ca=1.0, jit=0.04)
        w.start(self)
        la, lb = w.labels_ab()
        self.add(la, lb)
        w.run(self, 1.7)
        cut, cv = ValueTracker(0.0), ValueTracker(0.0)
        self.add(cut, cv)
        cab = nerve_cable(w, cut, cv)
        self.add(cab)
        nl = lab("nerve", 30, NERVE, (-5.3, w.cy - 0.5))
        pul = Pulser(lambda: (-6.5, w.cy, 0), lambda: (w.L(), w.cy, 0), dur=0.9)
        tm = w.tm
        stop = {"cut": False}
        schedule(self, tm, [3.4, 5.6, 8.0], lambda t, i: None if stop["cut"] else pul.fire())
        self.add(pul)
        self.at("that make the nerve", lead=0.2)
        self.play(cv.animate.set_value(1.0), FadeIn(nl), run_time=0.8)
        self.at("calcium raised", lead=0.6)
        cl = lab("calcium kept up", 34, YELLOW, (0, 3.35))
        self.play(FadeIn(cl, shift=DOWN * 0.1), run_time=0.7)
        self.at("without them", lead=0.5)
        sc1 = Line([-0.5, 0.0, 0], [0.5, 0.0, 0], color=ZOUT, stroke_width=6)
        sc2 = Line([-0.5, 0.0, 0], [0.5, 0.0, 0], color=ZOUT, stroke_width=6)
        sc = VGroup(sc1, sc2)
        sc1.rotate(0.45); sc2.rotate(-0.45)
        sc.move_to([-5.15, w.cy + 2.4, 0])
        self.play(FadeIn(sc), run_time=0.3)
        self.play(sc.animate.move_to([-5.15, w.cy + 0.45, 0]), run_time=0.6)
        stop["cut"] = True
        self.play(Rotate(sc1, angle=-0.45, about_point=sc.get_center()), Rotate(sc2, angle=0.45, about_point=sc.get_center()), cut.animate.set_value(1.0), run_time=0.4)
        self.play(FadeOut(sc), FadeOut(cl), w.dr.animate.set_value(1.0), w.amp.animate.set_value(0.0), run_time=1.5)
        self.finish()


class S13Same(SpokenScene):
    def construct(self):
        tm = tmr()
        self.add(tm)
        CYL = -0.25
        cL, cR = ValueTracker(0.0), ValueTracker(0.0)
        onL, onR = ValueTracker(0.0), ValueTracker(0.0)
        st = {"mode": 0, "t1": 0.0}
        self.add(cL, cR, onL, onR)
        TX = -3.4
        TX2 = 3.4
        sarL = always_redraw(lambda: chain_mobs(TX, CYL, 5.4, 3.0, cL.get_value(), 0.32))
        sarR = always_redraw(lambda: chain_mobs(TX2, CYL, 5.4, 3.0, cR.get_value(), 0.32))
        tgL = always_redraw(lambda: toggle_mobs(TX, 2.0, onL.get_value()))
        tgR = always_redraw(lambda: toggle_mobs(TX2, 2.0, onR.get_value()))
        pL = Pulser(lambda: (TX - 2.6, 2.0, 0), lambda: (TX - 0.9, 2.0, 0), dur=0.45)
        pR = Pulser(lambda: (TX2 - 2.6, 2.0, 0), lambda: (TX2 - 0.9, 2.0, 0), dur=0.45)
        PER = 2.4
        spring_m = always_redraw(lambda: spring([TX2 - 2.7 * (1 - 0.17 * cR.get_value()), -2.35, 0], [TX2 + 2.7 * (1 - 0.17 * cR.get_value()), -2.35, 0], 14, 0.17, TEXT, 4))
        drv = Mobject()
        pt = {"last": -1}

        def u(m, dt):
            t = tm.get_value()
            k = int(math.floor((t - 1.0) / PER))
            if k > pt["last"] and k >= 0:
                pt["last"] = k
                pL.fire()
                if st["mode"] == 0:
                    pR.fire()
                elif k % 2 == 0:
                    pR.fire()
            ph = (t - 1.0 - 0.5) % PER if t > 1.5 else 99
            tgt = 1.0 if 0 <= ph < 0.9 else 0.0
            onL.set_value(onL.get_value() + (tgt - onL.get_value()) * min(1, dt * 10))
            cL.set_value(cL.get_value() + (onL.get_value() - cL.get_value()) * min(1, dt * 3.5))
            if st["mode"] == 0:
                onR.set_value(onL.get_value())
                cR.set_value(cL.get_value())
            else:
                onR.set_value(onR.get_value() + (1.0 - onR.get_value()) * min(1, dt * 6))
                tg = 0.5 + 0.42 * math.sin(2 * math.pi * (t - st["t1"]) / 1.3)
                cR.set_value(cR.get_value() + (tg - cR.get_value()) * min(1, dt * 6))
        drv.add_updater(u)
        self.add(drv, pL, pR)
        self.add(sarL, sarR)
        self.wait(0.4)
        self.at("what changed", lead=0.2)
        ll = lab("synchronous", 36, TEXT, (TX, 3.4))
        lr = lab("asynchronous", 36, TEXT, (TX2, 3.4))
        self.add(tgL, tgR)
        self.play(FadeIn(ll), FadeIn(lr), run_time=0.8)
        self.at("the nerve holds it on", lead=0.2)
        st["mode"] = 1
        st["t1"] = tm.get_value()
        self.at("stretch times", lead=0.1)
        sl = lab("stretch adds force", 30, TEXT, (TX2, -3.2))
        self.add(spring_m)
        self.play(FadeIn(sl, shift=UP * 0.1), run_time=0.7)
        self.finish()


class S14Open(SpokenScene):
    def construct(self):
        paper = RoundedRectangle(corner_radius=0.15, width=10.8, height=6.6, stroke_color="#cdbf9f", stroke_width=3, fill_color=PAPER, fill_opacity=1)
        holes = VGroup(*[Circle(0.13, stroke_width=0, fill_color="#0f1117", fill_opacity=1).move_to([-4.95, y, 0]) for y in (2.4, 1.2, 0.0, -1.2, -2.4)])
        q1 = Text("1.  Were the large spikes\n      full action potentials?", font=FONT, font_size=40, color=INK, line_spacing=1.1).move_to([0.3, 1.3, 0])
        q2 = Text("2.  How does stretch raise force?", font=FONT, font_size=38, color=INK).move_to([0.3, -0.7, 0])
        stamp = VGroup(RoundedRectangle(corner_radius=0.1, width=5.6, height=0.85, stroke_color="#B03A2E", stroke_width=5),
                       T("still being worked out", 30, "#B03A2E")).move_to([1.6, -2.1, 0]).rotate(0.12)
        self.play(FadeIn(paper), FadeIn(holes), run_time=0.7)
        self.at("pringle's recordings", lead=0.0)
        self.play(Write(q1), run_time=2.6)
        self.at("and how stretch", lead=0.1)
        self.play(Write(q2), run_time=3.2)
        self.at("still being worked", lead=0.5)
        stamp.scale(1.6).set_opacity(0)
        self.add(stamp)
        self.play(stamp.animate.scale(1 / 1.6).set_opacity(1), run_time=0.45, rate_func=rush_into)
        self.play(stamp.animate.shift(RIGHT * 0.05), run_time=0.1)
        self.finish()


class S15Rule(SpokenScene):
    def construct(self):
        w = Thorax(cy=-0.4, u0=1.0, fa=0.85, fb=0.45, ca=1.0, jit=0.04)
        w.start(self)
        la, lb = w.labels_ab()
        self.add(la, lb)
        w.run(self, 1.7)
        cut = ValueTracker(0.0)
        self.add(cut)
        cab = nerve_cable(w, cut)
        nl = lab("nerve", 30, NERVE, (-5.3, w.cy + 0.5))
        pul = Pulser(lambda: (-6.5, w.cy, 0), lambda: (w.L(), w.cy, 0), dur=0.9)
        schedule(self, w.tm, [1.0, 3.8, 6.4], lambda t, i: pul.fire())
        self.add(pul, cab, nl)
        self.at("rule for these insects", lead=1.0)
        l1 = T("In asynchronous muscle, stretch times each beat;", 34, TEXT).move_to([0, -3.0, 0])
        l2 = T("the nerve keeps it on.", 34, TEXT).move_to([0, -3.55, 0])
        self.add(l1, l2)
        self.play(AddTextLetterByLetter(l1, time_per_char=0.075), run_time=3.6)
        self.play(AddTextLetterByLetter(l2, time_per_char=0.075), run_time=1.6)
        self.finish()


class S16End(EndCard):
    LINE = "In asynchronous muscle, stretch times each beat; the nerve keeps it on."
