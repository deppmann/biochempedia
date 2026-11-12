"""Reading Evolution Across Time: mutualism, parasitism and coevolution (chapter 2).

COLOUR MAP (same as chapter 1)
  GREEN  = plant / host / alga   PURPLE = fungus / parasite / phage / partner
  GOLD   = rhizobia              TEAL   = benefit        RED = cost
  ORANGE = rotifer               GREY   = structure
"""
import numpy as np
from bp_style import *  # noqa: F401,F403

PURPLE = "#B07CE0"
PALEP = "#E7D6FF"
LIGHTG = "#B8C0CE"
ORANGE = "#F29B3C"


# ---------------------------------------------------------------- small helpers
def clip(v, a, b):
    return max(a, min(b, v))


def ambient_clock(sc):
    clk = ValueTracker(0)
    clk.add_updater(lambda m, dt: m.increment_value(dt))
    sc.add(clk)
    return clk


def pulse(m, amp=0.06, per=1.6):
    m._f = 1.0
    m._tt = 0.0

    def up(mm, dt):
        mm._tt += dt
        f = 1 + amp * np.sin(2 * np.pi * mm._tt / per)
        mm.scale(f / mm._f)
        mm._f = f
    m.add_updater(up)
    return m

# ---------------------------------------------------------------- the balance
class Bal:
    def __init__(s, cx, py, L=2.3, h=1.35, tw=0.8, mx=1.0, mn=0.2, col=TEXT):
        s.cx, s.py, s.L, s.h, s.tw, s.mx, s.mn, s.col = cx, py, L, h, tw, mx, mn, col
        s.zb, s.zc, s.wb, s.wc, s.db, s.dc, s.th = [ValueTracker(0) for _ in range(7)]
        s.clock = ValueTracker(0)
        s.clock.add_updater(lambda m, dt: m.increment_value(dt))
        s.beam_m = always_redraw(s.beam)
        s.bk = [always_redraw(lambda i=i: s.block(i)) for i in (0, 1)]
        s.pivot = Dot([cx, py, 0], radius=0.13, color=GOLD)
        s.post = VGroup(Line([cx, py, 0], [cx, py - 3.0, 0], color=GREY, stroke_width=6),
                        Line([cx - 0.7, py - 3.0, 0], [cx + 0.7, py - 3.0, 0], color=GREY, stroke_width=8))
        s.labs = []

    def ang(s):
        base = clip((s.wb.get_value() - s.wc.get_value()) * 0.42, -0.34, 0.34)
        return base + s.th.get_value() + 0.014 * np.sin(1.8 * s.clock.get_value() + s.cx)

    def ends(s):
        a = s.ang()
        c, n = np.cos(a), np.sin(a)
        return (np.array([s.cx - s.L * c, s.py - s.L * n, 0.0]), np.array([s.cx + s.L * c, s.py + s.L * n, 0.0]))

    def tray(s, i):
        return s.ends()[i] + np.array([0, -s.h, 0.0])

    def beam(s):
        l, r = s.ends()
        g = VGroup(Line(l, r, color=s.col, stroke_width=8))
        for e in (l, r):
            t = e + np.array([0, -s.h, 0.0])
            a = t + np.array([-s.tw, 0, 0.0])
            b = t + np.array([s.tw, 0, 0.0])
            g.add(Line(e, a, color=s.col, stroke_width=3), Line(e, b, color=s.col, stroke_width=3),
                  Line(a, b, color=s.col, stroke_width=8))
        return g

    def block(s, i):
        z = (s.zb, s.zc)[i].get_value()
        d = (s.db, s.dc)[i].get_value()
        side = s.mn + z * (s.mx - s.mn)
        col = (TEAL, RED)[i]
        sq = Square(side, stroke_color=col, stroke_width=3, fill_color=col, fill_opacity=0.6)
        sq.move_to(s.tray(i) + np.array([0, side / 2 + 0.05 + d, 0]))
        return sq

    def label(s, i, text, size=30, color=None):
        col = color or (TEAL, RED)[i]
        t = T(text, size, col)
        t.add_updater(lambda m: m.move_to(s.tray(i) + np.array([0, -0.45, 0])))
        t.move_to(s.tray(i) + np.array([0, -0.45, 0]))
        return t

    def static(s):
        return VGroup(s.post, s.pivot)

    def net(s):
        return s.wb.get_value() - s.wc.get_value()

    def load(s, sc, b, c, labels=True, blocks=True):
        for tr, v in ((s.zb, b), (s.wb, b), (s.zc, c), (s.wc, c)):
            tr.set_value(v)
        sc.add(s.clock, s.post, s.pivot, s.beam_m)
        if blocks:
            sc.add(*s.bk)
        if labels:
            s.labs = [s.label(0, "benefit"), s.label(1, "cost")]
            sc.add(*s.labs)

    def drop_anim(s, sc, i, v, fall=0.7):
        z, d, w = (s.zb, s.zc)[i], (s.db, s.dc)[i], (s.wb, s.wc)[i]
        z.set_value(v)
        d.set_value(2.8)
        sc.add(s.bk[i])
        return Succession(d.animate(rate_func=rush_into, run_time=fall).set_value(0),
                          w.animate(rate_func=smooth, run_time=0.9).set_value(v))



def panel(x=2.35, w=8.5, y=0.0, h=7.4):
    r = Rectangle(width=w, height=h, stroke_width=0, fill_color="#171d2a", fill_opacity=1).move_to([x, y, 0])
    r.set_z_index(-5)
    return r


def qmark(x, y):
    c = Circle(radius=0.75, stroke_color=YELLOW, stroke_width=4, fill_color=BG, fill_opacity=0.92)
    return VGroup(c, T("?", 100, YELLOW, weight=BOLD)).move_to([x, y, 0])


def schematic_tag():
    return T("schematic", 24, GREY).move_to([-5.6, 3.45, 0])


# ================================================================ chapter 2 helpers
XS = 0.52                      # x units per week of time gap (and per week on the timeline)
AX_B = -2.0                    # baseline of the infection axis
BXS = (-3.12, 0.0, 3.12)       # weeks 4, 10, 16 (gap -6, 0, +6)


def WX(w):
    return -5.2 + XS * w


def stag(y=-3.45, x=-5.6):
    return T("schematic", 24, GREY).move_to([x, y, 0])


def I_arm(g):
    return 1 / (1 + np.exp(0.25 * g))


_GT = np.linspace(-10, 10, 201)


def _wave_table():
    om, tau = 2 * np.pi / 12, 0.6
    t = np.linspace(0, 120, 1201)
    h0 = 0.5 + 0.46 * np.cos(om * t)
    p = 0.5 + 0.46 * np.cos(om * (t - tau))
    out = []
    for g in _GT:
        hg = 0.5 + 0.46 * np.cos(om * (t + g))
        out.append(np.mean(p * hg + (1 - p) * (1 - hg)))
    return np.array(out)


_WT = _wave_table()


def I_wave(g):
    return float(np.interp(g, _GT, _WT))


def yI(i):
    return AX_B + 4.2 * i


def curve_pts(f, x0, x1, n=120):
    return [np.array([x, f(x), 0.0]) for x in np.linspace(x0, x1, n)]


def curve(f, x0, x1, color, sw=7, n=120):
    return VMobject().set_points_smoothly(curve_pts(f, x0, x1, n)).set_stroke(color, sw)


def f_arm(x):
    return yI(I_arm(x / XS))


def f_wave(x):
    return yI(I_wave(x / XS))


def loop_dot(path, color, per=4.0, r=0.14):
    d = Dot(radius=r, color=color)
    d._t = 0.0

    def up(m, dt):
        m._t += dt
        m.move_to(path.point_from_proportion((m._t / per) % 1.0))
    d.add_updater(up)
    up(d, 0)
    return d


def bob(m, amp=0.06, per=2.4, ph=0.0):
    m._bt = 0.0
    m._bo = 0.0

    def up(mm, dt):
        mm._bt += dt
        o = amp * np.sin(2 * np.pi * mm._bt / per + ph)
        mm.shift(UP * (o - mm._bo))
        mm._bo = o
    m.add_updater(up)
    return m


def axes_xy(y_axis=True):
    xa = Line([-5.4, AX_B, 0], [5.4, AX_B, 0], color=GREY, stroke_width=4)
    g = VGroup(xa)
    ya = None
    if y_axis:
        ya = VGroup(Line([-5.4, AX_B, 0], [-5.4, 2.5, 0], color=GREY, stroke_width=4),
                    T("infection", 28, TEXT).rotate(PI / 2).move_to([-6.2, 0.2, 0]))
    return xa, ya


def row_gap(y=-2.65):
    txt = ["− past hosts", "0  same time", "+ future hosts"]
    return VGroup(*[T(t, 28, TEXT).move_to([x, y, 0]) for t, x in zip(txt, BXS)])


def row_weeks():
    a = VGroup(*[T(t, 28, TEXT).move_to([x, -2.65, 0]) for t, x in zip(["week 4", "week 10", "week 16"], BXS)])
    b = VGroup(*[T(t, 28, TEXT).move_to([x, -3.3, 0]) for t, x in zip(["past hosts", "same time", "future hosts"], BXS)])
    return VGroup(a, b)


def vial(color, x, y, h=0.7, w=0.3):
    body = RoundedRectangle(corner_radius=0.06, width=w, height=h, stroke_color=color, stroke_width=3,
                            fill_color=color, fill_opacity=0.55)
    cap = Rectangle(width=w * 1.15, height=0.1, stroke_width=0, fill_color=TEXT, fill_opacity=0.9)
    cap.move_to(body.get_top() + UP * 0.05)
    return VGroup(body, cap).move_to([x, y, 0])


def rack_box():
    r = Rectangle(width=12.6, height=1.7, stroke_color=GREY, stroke_width=4, fill_color="#1d2433", fill_opacity=0.9)
    return r.move_to([0, -2.2, 0])


RACK_Y = -2.05


def phage_icon(s=1.0, color=PURPLE):
    head = RegularPolygon(6, radius=0.3 * s, color=color, fill_opacity=0.6, stroke_width=3)
    tail = Line([0, -0.3 * s, 0], [0, -0.75 * s, 0], color=color, stroke_width=3)
    legs = VGroup(*[Line([0, -0.75 * s, 0], [dx * s, -1.0 * s, 0], color=color, stroke_width=3) for dx in (-0.3, 0, 0.3)])
    return VGroup(head, tail, legs)


def bacterium_icon(s=1.0):
    return RoundedRectangle(corner_radius=0.22 * s, width=0.9 * s, height=0.45 * s, stroke_color=GREEN,
                            stroke_width=3, fill_color=GREEN, fill_opacity=0.6)


def rotifer_icon(s=1.0):
    body = Ellipse(width=0.8 * s, height=0.45 * s, fill_color=ORANGE, fill_opacity=0.9, stroke_color=ORANGE, stroke_width=3)
    crown = VGroup(*[Line([-0.4 * s, y * s, 0], [-0.58 * s, y * s * 1.6, 0], color=ORANGE, stroke_width=3) for y in (-0.12, 0, 0.12)])
    foot = Line([0.4 * s, 0, 0], [0.64 * s, 0, 0], color=ORANGE, stroke_width=4)
    return VGroup(body, crown, foot)


def alga_icon(s=1.0, spines=False, color=GREEN):
    c = Circle(radius=0.2 * s, stroke_color=color, stroke_width=3, fill_color=color, fill_opacity=0.8)
    g = VGroup(c)
    if spines:
        for k in range(10):
            a = 2 * PI * k / 10
            g.add(Line([0.2 * s * np.cos(a), 0.2 * s * np.sin(a), 0], [0.36 * s * np.cos(a), 0.36 * s * np.sin(a), 0],
                       color=color, stroke_width=3))
    return g


class Bars:
    def __init__(s, trs, color=PURPLE, w=1.5, errs=None):
        s.trs, s.color, s.w, s.errs = trs, color, w, errs
        s.mob = always_redraw(s.mk)
        s.err = always_redraw(s.mke)

    def mk(s):
        g = VGroup()
        for x, t in zip(BXS, s.trs):
            h = max(t.get_value(), 0.001)
            g.add(Rectangle(width=s.w, height=h, stroke_width=3, stroke_color=s.color, fill_color=s.color,
                            fill_opacity=0.55).move_to([x, AX_B + h / 2, 0]))
        return g

    def mke(s):
        g = VGroup()
        if s.errs is None or s.errs.get_value() < 0.01:
            return g
        e = 0.28 * s.errs.get_value()
        for x, t in zip(BXS, s.trs):
            top = AX_B + t.get_value()
            g.add(Line([x, top - e, 0], [x, top + e, 0], color=TEXT, stroke_width=4),
                  Line([x - 0.2, top + e, 0], [x + 0.2, top + e, 0], color=TEXT, stroke_width=4),
                  Line([x - 0.2, top - e, 0], [x + 0.2, top - e, 0], color=TEXT, stroke_width=4))
        return g


def reveal_curve(f, x0, x1, rv, color, sw=7):
    def mk():
        v = clip(rv.get_value(), 0.003, 1.0)
        return curve(f, x0, x0 + (x1 - x0) * v, color, sw, n=max(4, int(140 * v)))
    return always_redraw(mk)


def clock_up(sc):
    rv = ValueTracker(0)
    rv.add_updater(lambda m, dt: m.increment_value(dt))
    sc.add(rv)
    return rv


def stream(path, color, n=4, speed=0.2, r=0.07, rev=False, ph=0.0):
    dots = VGroup(*[Dot(radius=r, color=color) for _ in range(n)])
    for i, d in enumerate(dots):
        d._u = (i / n + ph) % 1.0

    def up(g, dt):
        for d in g:
            d._u = (d._u + (-1 if rev else 1) * speed * dt) % 1.0
            d.move_to(path.point_from_proportion(d._u))
    dots.add_updater(up)
    up(dots, 0)
    return dots


# ---------------------------------------------------------------- swarms
def wander_setup(mobs, spd, seed):
    rng = np.random.RandomState(seed)
    for m in mobs:
        a = rng.uniform(0, 6.28)
        m.v = np.array([np.cos(a), np.sin(a), 0.0]) * spd
        m.rng = np.random.RandomState(rng.randint(10 ** 6))


def wander_step(m, dt, box, spd):
    x0, x1, y0, y1 = box
    m.v = m.v + np.append(m.rng.normal(size=2), 0) * 1.5 * dt
    n = np.linalg.norm(m.v) + 1e-6
    m.v = m.v / n * spd
    p = m.get_center() + m.v * dt
    if p[0] < x0 or p[0] > x1:
        m.v[0] *= -1
    if p[1] < y0 or p[1] > y1:
        m.v[1] *= -1
    m.move_to([clip(p[0], x0, x1), clip(p[1], y0, y1), 0])


class Vessel:
    def __init__(s, cx, cy, w, h, n, colors, seed):
        s.cx, s.cy, s.w, s.h = [ValueTracker(v) for v in (cx, cy, w, h)]
        s.box = always_redraw(lambda: RoundedRectangle(
            corner_radius=0.3, width=s.w.get_value(), height=s.h.get_value(), stroke_color=LIGHTG, stroke_width=5,
            fill_color="#1c2a3a", fill_opacity=0.5).move_to([s.cx.get_value(), s.cy.get_value(), 0]))
        rng = np.random.RandomState(seed)
        s.cells = VGroup(*[Dot(radius=0.13, color=colors[i % len(colors)]) for i in range(n)])
        for d in s.cells:
            d.u, d.v_ = rng.uniform(0.08, 0.92), rng.uniform(0.08, 0.92)
            d.du, d.dv = rng.uniform(-0.12, 0.12), rng.uniform(-0.12, 0.12)
        s.cells.add_updater(s.up)
        s.up(s.cells, 0)

    def up(s, g, dt):
        for d in g:
            d.du += 0.06 * np.random.uniform(-1, 1) * dt * 10 * 0.1
            d.dv += 0.06 * np.random.uniform(-1, 1) * dt * 10 * 0.1
            d.u += d.du * dt
            d.v_ += d.dv * dt
            if d.u < 0.08 or d.u > 0.92:
                d.du *= -1
            if d.v_ < 0.08 or d.v_ > 0.92:
                d.dv *= -1
            d.u, d.v_ = clip(d.u, 0.08, 0.92), clip(d.v_, 0.08, 0.92)
            d.move_to([s.cx.get_value() + (d.u - 0.5) * s.w.get_value(), s.cy.get_value() + (d.v_ - 0.5) * s.h.get_value(), 0])

    def label(s, text, size=28, color=TEXT):
        t = T(text, size, color)
        f = lambda m, dt=0: m.move_to([s.cx.get_value(), s.cy.get_value() + s.h.get_value() / 2 + 0.45, 0])
        t.add_updater(f)
        f(t)
        return t


def add_motes(sc):
    import random
    rng = random.Random(os.environ.get("KX_SCENE_ID", "x"))
    W, H = config.frame_width, config.frame_height
    motes = VGroup()
    for _ in range(40):
        d = Dot(radius=rng.uniform(0.05, 0.1), color=rng.choice([TEAL, LIGHTG, PALEP])).set_opacity(rng.uniform(0.18, 0.4))
        d.move_to([rng.uniform(-W / 2, W / 2), rng.uniform(-H / 2, H / 2), 0])
        d.v = (rng.uniform(-0.15, 0.15), rng.uniform(0.1, 0.3))

        def drift(m, dt, W=W, H=H):
            m.shift([m.v[0] * dt, m.v[1] * dt, 0])
            if m.get_y() > H / 2 + 0.1:
                m.shift(DOWN * (H + 0.2))
            if abs(m.get_x()) > W / 2 + 0.1:
                m.shift(LEFT * (W + 0.2) * (1 if m.get_x() > 0 else -1))
        d.add_updater(drift)
        motes.add(d)
    motes.set_z_index(-10)
    sc.add(motes)


class SS(SpokenScene):
    def setup(self):
        super().setup()
        add_motes(self)


class NS(NarratedScene):
    def setup(self):
        super().setup()
        add_motes(self)


# ================================================================ scenes
class S00Title(TitleCard):
    LESSON = "Mutualism, Parasitism and Coevolution"
    TITLE = "Reading Evolution Across Time"


class S01Link(SS):
    def construct(self):
        kw = dict(L=1.8, h=1.4, tw=0.8, mx=0.9, mn=0.2)
        H = Bal(-3.3, 0.9, col=GREEN, **kw)
        P = Bal(3.3, 0.9, col=PURPLE, **kw)
        self.add(panel(0, 13.2, 0.0, 7.4))
        H.load(self, 0.5, 0.45, labels=False)
        P.load(self, 0.5, 0.45, labels=False)
        rod = always_redraw(lambda: Line(H.ends()[1], P.ends()[0], color=GOLD, stroke_width=9))
        lh = T("host", 44, GREEN).move_to([-3.3, 3.2, 0])
        lp = T("partner", 44, PURPLE).move_to([3.3, 3.2, 0])
        self.add(rod, lh, lp)
        self.at("scored each")
        self.play(H.wb.animate.set_value(0.8), H.zb.animate.set_value(0.8), run_time=1.5)
        self.at("When both partners")
        self.play(P.zb.animate.set_value(0.9), P.wb.animate.set_value(0.9), run_time=1.4)
        self.at("each resets")
        self.play(H.th.animate(rate_func=smooth).set_value(-0.2), run_time=1.3)
        self.play(H.zb.animate.set_value(0.3), H.wb.animate.set_value(0.3), H.th.animate.set_value(0.0), run_time=1.2)
        self.at("How can you")
        ring = Circle(radius=0.6, stroke_color=YELLOW, stroke_width=6).move_to([0, 2.7, 0])
        hand = Line([0, 2.7, 0], [0, 3.15, 0], color=YELLOW, stroke_width=6)
        hand._t = 0.0

        def spin(m, dt):
            m.rotate(-2.2 * dt, about_point=np.array([0, 2.7, 0]))
        hand.add_updater(spin)
        q = T("how do you see it?", 40, YELLOW).move_to([0, -3.3, 0])
        self.play(FadeIn(ring), FadeIn(hand), FadeIn(q, shift=UP * 0.2), run_time=1.0)
        self.finish()


class S02Freeze(SS):
    def construct(self):
        b = bacterium_icon().move_to([-4.8, 3.2, 0])
        bl = T("bacterium", 30, GREEN).next_to(b, RIGHT, buff=0.25)
        ph = phage_icon(0.8).move_to([0.6, 3.2, 0])
        pl = T("phage", 30, PURPLE).next_to(ph, RIGHT, buff=0.25)
        self.play(FadeIn(b), FadeIn(bl), run_time=0.8)
        bob(b, 0.08, 2.0)
        self.at("and a phage")
        self.play(FadeIn(ph), FadeIn(pl), run_time=0.8)
        bob(ph, 0.08, 2.2, 1.0)
        self.at("Freeze samples")
        tl = Line([-5.2, 2.0, 0], [5.2, 2.0, 0], color=GREY, stroke_width=4)
        ticks = VGroup(*[Line([WX(w), 1.9, 0], [WX(w), 2.1, 0], color=GREY, stroke_width=4) for w in range(0, 21, 2)])
        nums = VGroup(*[T(str(w), 28, TEXT).move_to([WX(w), 1.45, 0]) for w in range(0, 21, 4)])
        wk = T("weeks", 28, TEXT).move_to([6.1, 2.0, 0])
        rack = rack_box()
        rl = T("freezer rack", 28, TEXT).move_to([0, -3.45, 0])
        self.play(Create(tl), FadeIn(ticks), FadeIn(nums), FadeIn(wk), FadeIn(rack), FadeIn(rl), run_time=1.0)
        self.at("every two weeks")
        snow = VGroup(*[Dot(radius=0.04, color=PALEP) for _ in range(14)])
        for i, d in enumerate(snow):
            d.move_to([-6 + i * 0.9, -1.5 - (i % 3) * 0.4, 0])
            d._t = i

        def sn(g, dt):
            for d in g:
                d.shift(DOWN * 0.15 * dt)
                if d.get_y() < -2.9:
                    d.shift(UP * 1.5)
        snow.add_updater(sn)
        self.add(snow)
        for w in range(0, 21, 2):
            gv = vial(GREEN, WX(w) - 0.2, 0.7)
            pv = vial(PURPLE, WX(w) + 0.2, 0.7)
            self.add(gv, pv)
            self.play(gv.animate.move_to([WX(w) - 0.2, RACK_Y, 0]), pv.animate.move_to([WX(w) + 0.2, RACK_Y, 0]),
                      run_time=0.22, rate_func=rush_into)
        self.at("revive later")
        self.play(rack.animate(rate_func=there_and_back).scale(1.04), run_time=1.5)
        self.finish()


def rack_with_vials():
    g = VGroup(rack_box())
    for w in range(0, 21, 2):
        g.add(vial(GREEN, WX(w) - 0.2, RACK_Y), vial(PURPLE, WX(w) + 0.2, RACK_Y))
    return g


class S03Assay(SS):
    def construct(self):
        rk = rack_with_vials()
        rl = T("freezer rack", 28, TEXT).move_to([0, -3.45, 0])
        self.add(rk, rl)
        ti = T("time-shift assay", 34, YELLOW).move_to([-3.6, 3.3, 0])
        self.at("time shift")
        self.play(FadeIn(ti), run_time=0.7)
        self.at("Phages from one time")
        idx = {4: 2, 10: 5, 16: 8}  # week -> pair index
        pv = rk[1 + 2 * idx[10] + 1]
        self.play(pv.animate.move_to([0, 2.3, 0]), run_time=1.3)
        pt = T("phage, week 10", 30, PURPLE).next_to(pv, RIGHT, buff=0.3)
        self.play(FadeIn(pt), run_time=0.5)
        gv = {}
        for w, nm, lab in ((4, "the past", "week 4:\npast"), (10, "the same time", "week 10:\nsame time"),
                           (16, "and the future", "week 16:\nfuture")):
            self.at(nm)
            v = rk[1 + 2 * idx[w]]
            self.play(v.animate.move_to([BXS[(4, 10, 16).index(w)], 0.2, 0]), run_time=0.7)
            x = BXS[(4, 10, 16).index(w)]
            ln = Arrow([0, 1.9, 0], [x, 0.65, 0], color=PURPLE, stroke_width=5, buff=0.05)
            lb = T(lab, 28, GREEN).move_to([x, -0.6, 0])
            self.play(GrowArrow(ln), FadeIn(lb), run_time=0.5)
        vs3 = [rk[1 + 2 * idx[w]] for w in (4, 10, 16)] + [pv]
        for v in vs3:
            bob(v, 0.1, 1.6)
        self.wait(2.5)
        self.finish()


def bar_frame(sc, y_axis=False):
    xa, ya = axes_xy(y_axis)
    sc.add(xa)
    if ya is not None:
        sc.add(ya)
    return xa, ya


class S04Null(SS):
    def construct(self):
        xa, ya = axes_xy(True)
        self.add(xa)
        trs = [ValueTracker(0) for _ in range(3)]
        errs = ValueTracker(0)
        B = Bars(trs, errs=errs)
        self.add(B.mob, B.err)
        row = row_gap()
        top = T("no heritable change", 36, TEXT).move_to([0, 2.9, 0])
        tg = stag(3.45)
        self.add(tg)
        self.play(FadeIn(row), FadeIn(top), *[t.animate.set_value(2.0) for t in trs], run_time=1.6)
        self.at("every pairing")
        self.play(*[Indicate(m, color=YELLOW, scale_factor=1.03) for m in B.mob], run_time=1.5)
        self.at("A repeatable difference")
        top2 = T("at least one partner changed", 36, YELLOW).move_to([0, 2.9, 0])
        self.play(trs[0].animate.set_value(1.3), trs[1].animate.set_value(2.6), trs[2].animate.set_value(1.7),
                  errs.animate.set_value(1.0), ReplacementTransform(top, top2), run_time=2.0)
        self.at("The shape")
        yl = T("time gap: host minus phage", 28, TEXT).move_to([0, -3.3, 0])
        self.play(FadeOut(top2), FadeOut(tg), *[t.animate.set_value(0.001) for t in trs], errs.animate.set_value(0),
                  Create(ya), FadeIn(yl), run_time=1.8)
        d = loop_dot(Line([-5.2, AX_B, 0], [5.2, AX_B, 0]), YELLOW, 5.0, 0.1)
        self.add(d)
        self.finish()


class S05Arms(SS):
    def construct(self):
        hx = [-5.2, -3.9, -1.9, 0.1, 2.1, 4.1]
        px = [-5.2, -2.9, -0.9, 1.1, 3.1, 5.1]

        def stairs(xs, y0, color):
            pts = [np.array([xs[0], y0, 0.0])]
            y = y0
            for x in xs[1:]:
                pts.append(np.array([x, y, 0.0]))
                y += 0.75
                pts.append(np.array([x, y, 0.0]))
            pts.append(np.array([xs[-1] + 1.0 if xs[-1] < 5 else 5.5, y, 0.0]))
            m = VMobject().set_points_as_corners(pts).set_stroke(color, 9)
            return m
        H = stairs(hx, -1.6, GREEN)
        P = stairs(px, -1.9, PURPLE)
        tg = stag()
        self.add(tg)
        self.at("arms race")
        tt = T("arms race", 36, YELLOW).move_to([0, 3.3, 0])
        self.play(FadeIn(tt), run_time=0.6)
        self.at("Host resistance")
        hl = T("host resistance", 30, GREEN).move_to([-4.3, 3.3, 0])
        self.play(FadeIn(hl), Create(H, rate_func=linear), run_time=2.0)
        pl = T("phage infectivity", 30, PURPLE).move_to([4.2, 3.3, 0])
        self.at("phage infectivity")
        self.play(FadeIn(pl), Create(P, rate_func=linear), run_time=2.0)
        self.at("repeated rounds")
        rr = T("repeated rounds", 32, YELLOW).move_to([0, -2.8, 0])
        self.play(FadeIn(rr), run_time=0.8)
        d1 = loop_dot(H, YELLOW, 4.0, 0.12)
        d2 = loop_dot(P, YELLOW, 4.0, 0.12)
        self.add(d1, d2)
        self.finish()


def predict_scene(sc, with_q=True):
    xa, _ = axes_xy(True)
    xa2, ya = axes_xy(True)
    sc.add(xa, ya)
    outs = VGroup(*[Rectangle(width=1.5, height=3.2, stroke_color=GREY, stroke_width=4).move_to([x, AX_B + 1.6, 0])
                    for x in BXS])
    qs = VGroup(*[T("?", 80, YELLOW, weight=BOLD).move_to([x, AX_B + 1.6, 0]) for x in BXS])
    return outs, qs


class S06Predict(SS):
    def construct(self):
        outs, qs = predict_scene(self)
        wk = row_weeks()
        tag = VGroup(vial(PURPLE, 0, 0), T("phage from week 10", 32, PURPLE)).arrange(RIGHT, buff=0.25).move_to([-3.4, 3.2, 0])
        self.at("one phage")
        self.play(FadeIn(tag, shift=DOWN * 0.2), run_time=0.9)
        bob(tag, 0.05, 2.0)
        self.at("Test it on")
        self.play(LaggedStart(*[Create(o) for o in outs], lag_ratio=0.4), FadeIn(wk), run_time=2.4)
        self.at("Which does it")
        qt = T("Which does it infect best?", 34, YELLOW).move_to([2.6, 3.2, 0])
        self.play(FadeIn(qt), FadeIn(qs, scale=0.6), run_time=1.0)
        for q in qs:
            pulse(q, 0.06)
        self.finish()


class S07Pause(NS):
    def construct(self):
        outs, qs = predict_scene(self)
        wk = row_weeks()
        tag = VGroup(vial(PURPLE, 0, 0), T("phage from week 10", 32, PURPLE)).arrange(RIGHT, buff=0.25).move_to([-3.4, 3.2, 0])
        qt = T("Which does it infect best?", 34, YELLOW).move_to([2.6, 3.2, 0])
        self.add(outs, wk, tag, qt, qs)
        for q in qs:
            pulse(q, 0.06)
        tr = ValueTracker(0)
        ring = always_redraw(lambda: Arc(radius=0.45, start_angle=PI / 2, angle=-2 * PI * max(tr.get_value(), 0.001),
                                         color=YELLOW, stroke_width=8).move_to([6.2, 3.2, 0]))
        self.add(ring)
        self.play(tr.animate(rate_func=linear).set_value(1), run_time=self.beat(0.92))
        self.finish()


class S08Reveal(SS):
    def construct(self):
        outs, qs = predict_scene(self)
        wk = row_weeks()
        tag = VGroup(vial(PURPLE, 0, 0), T("phage from week 10", 32, PURPLE)).arrange(RIGHT, buff=0.25).move_to([-3.4, 3.2, 0])
        self.add(outs, wk, tag)
        trs = [ValueTracker(0) for _ in range(3)]
        B = Bars(trs)
        self.add(B.mob)
        tg = T("toy model", 24, GREY).move_to([5.7, 3.45, 0])
        self.add(tg)
        self.play(FadeOut(outs), *[t.animate(rate_func=smooth).set_value(4.2 * I_arm(g)) for t, g in zip(trs, (-6, 0, 6))],
                  run_time=2.0)
        self.at("never met")
        nt = T("resistance this phage\nhas not met", 28, TEXT).move_to([3.12, -0.5, 0])
        self.play(FadeIn(nt, shift=DOWN * 0.2), Indicate(B.mob[2], color=YELLOW), run_time=1.5)
        self.at("Infection falls")
        ln = curve(f_arm, -5.2, 5.2, PURPLE, 8)
        self.play(FadeOut(nt), *[t.animate.set_value(t.get_value() * 0.0 + 0.0 + 4.2 * I_arm(g) * 0.35)
                                  for t, g in zip(trs, (-6, 0, 6))], FadeOut(tag),
                  Create(ln, rate_func=linear), run_time=4.0)
        self.at("keeps falling")
        lab = T("arms race: one-way trend", 32, PURPLE).move_to([2.2, 2.9, 0])
        self.play(FadeIn(lab, shift=DOWN * 0.2), run_time=0.8)
        d = loop_dot(ln, YELLOW, 4.0)
        self.add(d)
        self.finish()


class S09Fluct(SS):
    def construct(self):
        cA, cS = ValueTracker(12), ValueTracker(4)
        fav = ValueTracker(-1)
        ZC = (-3.0, 3.0)
        rng = np.random.RandomState(4)
        circ = VGroup(*[Circle(radius=0.2, stroke_color=GREEN, stroke_width=3, fill_color=GREEN, fill_opacity=0.7) for _ in range(12)])
        sqs = VGroup(*[Square(0.38, stroke_color=GREEN, stroke_width=3, fill_color=GREEN, fill_opacity=0.7) for _ in range(12)])
        for g, cx in ((circ, ZC[0]), (sqs, ZC[1])):
            for i, m in enumerate(g):
                m._h = np.array([cx + (i % 4 - 1.5) * 1.0, 0.9 - (i // 4) * 1.1, 0.0])
                m._i = i
                m._p = rng.uniform(0, 6.3)
        t = ValueTracker(0)
        t.add_updater(lambda m, dt: m.increment_value(dt))
        self.add(t)

        def upg(g, tr):
            def up(m, dt):
                for d in m:
                    d.set_opacity(clip(tr.get_value() - d._i, 0, 1))
                    d.set_fill(GREEN, opacity=0.7 * clip(tr.get_value() - d._i, 0, 1))
                    d.move_to(d._h + 0.08 * np.array([np.sin(1.3 * t.get_value() + d._p), np.cos(1.1 * t.get_value() + d._p), 0]))
            g.add_updater(up)
            up(g, 0)
        upg(circ, cA)
        upg(sqs, cS)
        ph = VGroup(*[Dot(radius=0.1, color=PURPLE) for _ in range(14)])
        wander_setup(ph, 0.5, 9)
        for i, d in enumerate(ph):
            d._o = np.array([rng.uniform(-1.6, 1.6), rng.uniform(-1.6, 1.0), 0.0])
            d.move_to([-6, 3.0, 0])

        def upp(m, dt):
            cx = -3.0 + 3.0 * (fav.get_value() + 1)
            for d in m:
                tgt = np.array([cx, 0.0, 0.0]) + d._o + 0.25 * np.array([np.sin(2.3 * t.get_value() + d._o[0] * 3), np.cos(2.1 * t.get_value() + d._o[1] * 3), 0])
                d.move_to(d.get_center() + (tgt - d.get_center()) * min(1, 2.5 * dt))
        ph.add_updater(upp)
        fr = VGroup(*[Rectangle(width=5.6, height=4.2, stroke_color=GREY, stroke_width=3).move_to([x, 0.1, 0]) for x in ZC])
        com = T("common", 30, TEXT)
        rar = T("rare", 30, TEXT)

        def lab(m, dt=0):
            a, s = cA.get_value(), cS.get_value()
            com.move_to([ZC[0] if a >= s else ZC[1], 2.55, 0])
            rar.move_to([ZC[1] if a >= s else ZC[0], 2.55, 0])
        com.add_updater(lab)
        lab(com)
        self.add(fr, circ, sqs)
        for g in (circ, sqs):
            pass
        legend = T("phages", 30, PURPLE).move_to([0, -3.1, 0])
        self.play(FadeIn(legend), run_time=0.5)
        self.add(ph)
        self.at("Whichever host type")
        self.add(com, rar)
        self.wait(0.8)
        self.at("attacked most")
        self.play(cA.animate(rate_func=smooth).set_value(3), cS.animate(rate_func=smooth).set_value(12), run_time=3.2)
        self.at("Rare types")
        self.play(fav.animate(rate_func=smooth).set_value(1), run_time=1.6)
        self.at("keeps shifting")
        self.play(cA.animate(rate_func=smooth).set_value(12), cS.animate(rate_func=smooth).set_value(3), run_time=2.6)
        self.play(fav.animate(rate_func=smooth).set_value(-1), run_time=1.4)
        self.finish()


def plot_axes(sc):
    xa, ya = axes_xy(True)
    sc.add(xa, ya, row_gap())


class S10Wave(SS):
    def construct(self):
        plot_axes(self)
        arm = curve(f_arm, -5.2, 5.2, PURPLE, 8).set_stroke(opacity=0.35)
        self.add(arm)
        self.at("tend to do best")
        wave = curve(f_wave, -5.2, 5.2, PALEP, 8)
        self.play(Create(wave, rate_func=linear), run_time=4.5)
        ring = Circle(radius=0.3, stroke_color=YELLOW, stroke_width=5).move_to([-0.3, f_wave(-0.3), 0])
        self.play(Create(ring), run_time=0.6)
        self.at("rises and falls")
        lab = T("fluctuating selection:\nrises and falls, no trend", 30, PALEP).move_to([0, 3.2, 0])
        d = loop_dot(wave, YELLOW, 4.0)
        self.play(FadeIn(lab, shift=DOWN * 0.2), FadeOut(ring), run_time=0.8)
        self.add(d)
        self.at("long run trend")
        mid = DashedLine([-5.2, yI(0.5), 0], [5.2, yI(0.5), 0], color=TEXT, stroke_width=3)
        self.play(Create(mid), run_time=1.5)
        self.finish()


class S11Contrast(SS):
    def construct(self):
        plot_axes(self)
        arm = curve(f_arm, -5.2, 5.2, PURPLE, 8)
        wave = curve(f_wave, -5.2, 5.2, PALEP, 8)
        self.add(arm, wave)
        da = loop_dot(arm, YELLOW, 4.5)
        dw = loop_dot(wave, YELLOW, 4.5)
        self.add(da, dw)
        self.at("evidence")
        ev = T("evidence, not proof", 40, YELLOW).move_to([0, 3.45, 0])
        self.play(FadeIn(ev, shift=DOWN * 0.2), run_time=0.8)
        self.at("A one way")
        la = T("points to escalation", 30, PURPLE).move_to([-3.2, 2.85, 0])
        self.play(FadeIn(la, shift=DOWN * 0.2), Indicate(arm, color=YELLOW), run_time=1.6)
        self.at("A wave with")
        lw = T("points to tracking", 30, PALEP).move_to([3.6, 2.85, 0])
        self.play(FadeIn(lw, shift=DOWN * 0.2), Indicate(wave, color=YELLOW), run_time=1.6)
        self.finish()


CH_BOX = (-4.3, 3.1, -2.5, 1.7)


class S12Chemostat(SS):
    def construct(self):
        ves = RoundedRectangle(corner_radius=0.3, width=8.0, height=4.8, stroke_color=LIGHTG, stroke_width=5,
                               fill_color="#1c2a3a", fill_opacity=0.5).move_to([-0.6, -0.4, 0])
        self.play(FadeIn(ves), run_time=0.8)
        pin = Arrow([-3.3, 3.7, 0], [-3.3, 2.0, 0], color=LIGHTG, stroke_width=8, buff=0)
        pout = Arrow([3.4, -2.0, 0], [5.0, -2.0, 0], color=LIGHTG, stroke_width=8, buff=0)
        algae = VGroup(*[Dot(radius=0.12, color=GREEN) for _ in range(18)])
        wander_setup(algae, 0.35, 3)
        for i, d in enumerate(algae):
            d.move_to([-4.0 + (i % 6) * 1.3, -2.0 + (i // 6) * 1.3, 0])
        rots = VGroup(*[rotifer_icon(0.7) for _ in range(5)])
        wander_setup(rots, 0.6, 7)
        for i, r in enumerate(rots):
            r.move_to([-3.0 + i * 1.5, 0.8 - (i % 2), 0])
        entry = np.array([-3.3, 1.6, 0.0])

        def upa(g, dt):
            for d in g:
                wander_step(d, dt, CH_BOX, 0.35)

        def upr(g, dt):
            for r in g:
                best = min(algae, key=lambda a: np.linalg.norm(a.get_center() - r.get_center()))
                dv = best.get_center() - r.get_center()
                n = np.linalg.norm(dv)
                if n < 0.3:
                    best.move_to(entry + np.array([np.random.uniform(-0.3, 0.3), 0, 0]))
                    r.v = r.v * 0.2
                else:
                    r.move_to(r.get_center() + dv / n * 0.55 * dt)
        algae.add_updater(upa)
        rots.add_updater(upr)
        self.at("Picture")
        self.add(algae)
        self.play(GrowArrow(pin), run_time=0.8)
        self.at("steady inflow")
        il = T("inflow", 30, TEXT).move_to([-1.9, 3.2, 0])
        self.play(FadeIn(il), run_time=0.5)
        self.add(stream(Line([-3.3, 3.7, 0], [-3.3, 2.0, 0]), LIGHTG, 4, 0.2, 0.06))
        self.at("matching outflow")
        ol = T("outflow", 30, TEXT).move_to([5.3, -1.4, 0])
        self.play(GrowArrow(pout), FadeIn(ol), run_time=0.8)
        self.add(stream(Line([3.4, -2.0, 0], [5.0, -2.0, 0]), LIGHTG, 3, 0.25, 0.06))
        self.at("Rotifer's")
        self.add(rots)
        lg = VGroup(VGroup(alga_icon(0.8), T("algae", 28, GREEN)).arrange(RIGHT, buff=0.2),
                    VGroup(rotifer_icon(0.7), T("rotifers", 28, ORANGE)).arrange(RIGHT, buff=0.2)).arrange(DOWN, buff=0.4, aligned_edge=LEFT)
        lg.move_to([5.2, 1.0, 0])
        self.play(FadeIn(lg), run_time=0.8)
        self.finish()


# trace helpers for the lag scenes
def wave_fn(cx0, cy, A, P, lag):
    return lambda x: cy + A * np.sin(2 * np.pi * ((x - cx0) / P - lag))


class S13Lag(SS):
    def construct(self):
        X0, X1, P, cy, A = -5.0, 5.0, 5.0, 0.0, 1.3
        fg = wave_fn(X0, cy, A, P, 0.0)
        fo = wave_fn(X0, cy, A, P, 0.25)
        base = Line([X0, cy, 0], [X1 + 0.3, cy, 0], color=GREY, stroke_width=3)
        tx = T("time", 28, TEXT).move_to([6.2, cy, 0])
        rv = ValueTracker(0)
        rv.add_updater(lambda m, dt: m.increment_value(dt * 0.09))
        self.add(base, tx, rv)
        g = reveal_curve(fg, X0, X1, rv, GREEN)
        o = always_redraw(lambda: reveal_curve(fo, X0, X1, rv, ORANGE).copy() if False else
                          curve(fo, X0, X0 + (X1 - X0) * clip(rv.get_value() - 0.0, 0.003, 1), ORANGE, 7,
                                n=max(4, int(140 * clip(rv.get_value(), 0.003, 1)))))
        tg = stag(3.45, -5.6)
        self.add(tg)
        self.add(g, o)
        slot = None
        caps = [("prey rise", GREEN, "In classical"), ("predators multiply", ORANGE, "predators multiply"),
                ("prey crash", GREEN, "prey crash"), ("predators starve", ORANGE, "predators starve")]
        for txt, col, cue in caps:
            self.at(cue if cue != "In classical" else "prey rise")
            new = T(txt, 36, col).move_to([0, 3.2, 0])
            if slot is None:
                self.play(FadeIn(new, shift=DOWN * 0.2), run_time=0.5)
            else:
                self.play(ReplacementTransform(slot, new), run_time=0.5)
            slot = new
        self.at("Rotifer peaks")
        self.play(FadeOut(slot), run_time=0.4)
        gpk, opk = X0 + 0.25 * P, X0 + 0.5 * P
        v1 = DashedLine([gpk, cy + A, 0], [gpk, 2.3, 0], color=GREEN, stroke_width=3)
        v2 = DashedLine([opk, cy + A, 0], [opk, 2.3, 0], color=ORANGE, stroke_width=3)
        br = Line([gpk, 2.3, 0], [opk, 2.3, 0], color=YELLOW, stroke_width=6)
        dl = T("delay", 28, YELLOW).move_to([(gpk + opk) / 2, 2.8, 0])
        self.play(Create(v1), Create(v2), Create(br), FadeIn(dl), run_time=1.4)
        self.at("quarter cycle")
        ab = T("about 0.25 in the classical case", 28, TEXT).move_to([3.6, -3.4, 0])
        self.play(FadeIn(ab, shift=UP * 0.2), run_time=0.8)
        self.at("fraction of the period")
        t1, t2 = X0 + 0.75 * P, X0 + 1.75 * P
        v3 = DashedLine([t1, cy - A, 0], [t1, -2.3, 0], color=GREEN, stroke_width=3)
        v4 = DashedLine([t2, cy - A, 0], [t2, -2.3, 0], color=GREEN, stroke_width=3)
        br2 = Line([t1, -2.3, 0], [t2, -2.3, 0], color=YELLOW, stroke_width=6)
        pt = T("period", 28, YELLOW).move_to([(t1 + t2) / 2, -2.75, 0])
        self.play(Create(v3), Create(v4), Create(br2), FadeIn(pt), run_time=1.4)
        self.at("phase lag")
        eq = T("phase lag = delay / period", 34, YELLOW).move_to([-2.6, -3.4, 0])
        self.play(Write(eq), run_time=1.5)
        self.finish()


class S14Clones(SS):
    def construct(self):
        shades = [GREEN, "#2E9B5A", "#B5E35B", "#58C9A3"]
        VL = Vessel(-3.4, -0.5, 5.4, 4.0, 14, [GREEN], 1)
        VR = Vessel(3.4, -0.5, 5.4, 4.0, 14, shades, 2)
        nm = T("Takehito Yoshida and colleagues", 30, TEXT).move_to([0, 3.4, 0])
        self.play(FadeIn(nm), run_time=0.8)
        self.at("started the algae")
        self.add(VL.box, VR.box, VL.cells, VR.cells)
        ll = VL.label("one clone (identical cells)", 28, GREEN)
        lr = VR.label("several clones", 28, GREEN)
        self.play(FadeIn(ll), FadeIn(lr), run_time=0.8)
        self.at("A clone is")
        self.play(Indicate(VL.cells, color=YELLOW, scale_factor=1.05), run_time=1.8)
        self.at("One clone cannot")
        self.play(Indicate(ll, color=RED), run_time=1.6)
        self.at("Several clones can")
        self.play(Indicate(VR.cells, color=YELLOW, scale_factor=1.05), Indicate(lr, color=YELLOW), run_time=1.8)
        self.finish()


class S15Result(SS):
    def construct(self):
        shades = [GREEN, "#2E9B5A", "#B5E35B", "#58C9A3"]
        VL = Vessel(-3.4, -0.5, 5.4, 4.0, 14, [GREEN], 1)
        VR = Vessel(3.4, -0.5, 5.4, 4.0, 14, shades, 2)
        self.add(VL.box, VR.box, VL.cells, VR.cells)
        ll = VL.label("one clone (identical cells)", 28, GREEN)
        lr = VR.label("several clones", 28, GREEN)
        self.add(ll, lr)
        tg = stag(3.7, 6.1)
        self.add(tg)
        W = 5.0
        pls = []
        for cx, P, lag, col in ((-3.4, 1.25, 0.25, 0), (3.4, 3.4, 0.5, 1)):
            x0 = cx - W / 2
            cy = -1.65
            ax = Line([x0, cy, 0], [x0 + W, cy, 0], color=GREY, stroke_width=3)
            self.add(ax)
            rv = ValueTracker(0)
            fg = wave_fn(x0, cy, 0.9, P, 0.0)
            fo = wave_fn(x0, cy, 0.9, P, lag)
            gcur = always_redraw(lambda fg=fg, x0=x0, rv=rv: curve(fg, x0, x0 + W * clip(rv.get_value(), 0.003, 1), GREEN, 6, n=max(4, int(200 * clip(rv.get_value(), 0.003, 1)))))
            ocur = always_redraw(lambda fo=fo, x0=x0, rv=rv: curve(fo, x0, x0 + W * clip(rv.get_value(), 0.003, 1), ORANGE, 6, n=max(4, int(200 * clip(rv.get_value(), 0.003, 1)))))
            self.add(gcur, ocur)
            pls.append(rv)
        self.at("One clone gave")
        c1 = T("short cycles, near quarter lag", 28, TEXT).move_to([-3.4, -3.45, 0])
        self.play(*[tr.animate(rate_func=smooth).set_value(v) for tr, v in
                    ((VL.cy, 1.65), (VR.cy, 1.65), (VL.h, 2.5), (VR.h, 2.5), (VL.w, 5.0), (VR.w, 5.0))], run_time=1.2)
        self.play(pls[0].animate(rate_func=linear).set_value(1), FadeIn(c1), run_time=2.0)
        self.at("Several clones gave")
        c2 = T("long cycles, largely out of step", 28, TEXT).move_to([3.4, -3.45, 0])
        self.play(pls[1].animate(rate_func=linear).set_value(1), FadeIn(c2), run_time=3.6)
        self.finish()


class S16Tradeoff(SS):
    def construct(self):
        bal = Bal(-1.9, 1.3, L=2.3, h=1.35, tw=0.8)
        n = ValueTracker(0.5)
        bal.load(self, 0.575, 0.575, labels=False, blocks=False)

        def drive(m, dt=0):
            v = n.get_value()
            for tr in (bal.zb, bal.wb):
                tr.set_value(0.25 + 0.65 * v)
            for tr in (bal.zc, bal.wc):
                tr.set_value(0.9 - 0.65 * v)
        drv = ValueTracker(0)
        drv.add_updater(drive)
        self.add(drv)
        al = alga_icon(1.8, True).move_to([-3.6, 3.3, 0])
        at = T("defended alga", 30, GREEN).next_to(al, RIGHT, buff=0.3)
        self.add(al, at)
        bob(al, 0.05, 2.0)
        tg = stag()
        self.add(tg)
        self.at("Defence against")
        self.add(*bal.bk)
        lb = bal.label(0, "escape from grazing", 28, TEAL)
        lc = T("poorer nutrient\ncompetition", 28, RED)
        lc.add_updater(lambda m: m.move_to(bal.tray(1) + np.array([0, -0.6, 0])))
        lc.move_to(bal.tray(1) + np.array([0, -0.6, 0]))
        lb.add_updater(lambda m: m.move_to(bal.tray(0) + np.array([0, -0.5, 0])))
        self.play(FadeIn(lb), FadeIn(lc), run_time=1.0)
        fr = Rectangle(width=0.7, height=4.0, stroke_color=ORANGE, stroke_width=3).move_to([5.2, 0.0, 0])
        fill = always_redraw(lambda: Rectangle(width=0.6, height=max(4.0 * n.get_value(), 0.01), stroke_width=0,
                                               fill_color=ORANGE, fill_opacity=0.9).move_to([5.2, -2.0 + 2.0 * n.get_value(), 0]))
        ml = T("rotifers", 30, ORANGE).move_to([5.2, 2.5, 0])
        self.at("Many rotifers")
        self.add(fr, fill)
        self.play(FadeIn(ml), n.animate(rate_func=smooth).set_value(0.95), run_time=2.4)
        self.at("Few rotifers")
        self.play(n.animate(rate_func=smooth).set_value(0.08), run_time=2.8)
        self.play(Indicate(bal.bk[1], color=YELLOW), run_time=1.2)
        self.finish()


class S17Scope(SS):
    def construct(self):
        al = alga_icon(2.4, True).move_to([-4.2, 1.9, 0])
        ro = rotifer_icon(2.0).move_to([4.2, 1.9, 0])
        bob(al, 0.06, 2.0)
        bob(ro, 0.06, 2.3, 1.0)
        self.add(al, ro)
        self.at("prey evolution")
        tk = VGroup(Line([-0.3, 0, 0], [-0.1, -0.25, 0], color=GREEN, stroke_width=9),
                    Line([-0.1, -0.25, 0], [0.35, 0.3, 0], color=GREEN, stroke_width=9))
        ev = VGroup(tk, T("evolved", 32, GREEN)).arrange(RIGHT, buff=0.2).move_to([-1.9, 1.9, 0])
        self.play(FadeIn(ev, shift=RIGHT * 0.2), run_time=0.9)
        self.at("Predator evolution")
        nt = T("not tested", 32, GREY).move_to([1.5, 1.9, 0])
        self.play(FadeIn(nt, shift=LEFT * 0.2), run_time=0.9)
        self.at("So this is")
        top = Arrow([-3.8, -0.6, 0], [4.0, -0.6, 0], color=YELLOW, stroke_width=6, buff=0)
        bot = Arrow([4.0, -2.3, 0], [-3.8, -2.3, 0], color=YELLOW, stroke_width=6, buff=0)
        vr = Line([4.0, -0.6, 0], [4.0, -2.3, 0], color=YELLOW, stroke_width=6)
        vl = Line([-3.8, -2.3, 0], [-3.8, -0.6, 0], color=YELLOW, stroke_width=6)
        a1 = T("evolution changes numbers", 28, TEXT).move_to([0, -0.2, 0])
        a2 = T("numbers change selection", 28, TEXT).move_to([0, -2.75, 0])
        self.play(GrowArrow(top), FadeIn(a1), run_time=0.8)
        self.play(Create(vr), GrowArrow(bot), FadeIn(a2), Create(vl), run_time=1.1)
        path = Rectangle(width=7.8, height=1.7).move_to([0.1, -1.45, 0])
        self.add(stream(path, YELLOW, 4, 0.12, 0.07))
        self.at("ecoevolutionary")
        ee = T("eco-evolutionary feedback", 36, YELLOW).move_to([0, -1.45, 0])
        self.play(Write(ee), run_time=1.6)
        self.finish()


def mini_plot(cx, cy, w, h, f, color):
    xa = Line([cx - w / 2, cy - h / 2, 0], [cx + w / 2, cy - h / 2, 0], color=GREY, stroke_width=3)
    ya = Line([cx - w / 2, cy - h / 2, 0], [cx - w / 2, cy + h / 2, 0], color=GREY, stroke_width=3)
    fn = lambda x: cy - h / 2 + 0.08 + (h - 0.16) * f(((x - cx) / (w / 2)) * 10)
    cv = curve(fn, cx - w / 2 + 0.1, cx + w / 2 - 0.1, color, 7, 80)
    return VGroup(xa, ya, cv), cv


class S18Take(SS):
    def construct(self):
        rk = Rectangle(width=3.6, height=1.5, stroke_color=GREY, stroke_width=4, fill_color="#1d2433", fill_opacity=0.9).move_to([-4.6, 2.2, 0])
        vs = VGroup(*[vial(c, -6.1 + 0.45 * i + (0.0 if c == GREEN else 0.17), 2.2, 0.6, 0.2)
                      for i in range(7) for c in (GREEN, PURPLE)])
        rl = T("freezer", 28, TEXT).move_to([-4.6, 0.8, 0])
        self.at("Pairing partners")
        self.play(FadeIn(rk), FadeIn(vs), FadeIn(rl), run_time=1.0)
        p1, c1 = mini_plot(-0.4, 2.1, 3.8, 2.2, I_arm, PURPLE)
        p2, c2 = mini_plot(4.1, 2.1, 3.8, 2.2, I_wave, PALEP)
        l1 = T("escalation", 28, PURPLE).move_to([-0.4, 0.45, 0])
        l2 = T("tracking", 28, PALEP).move_to([4.1, 0.45, 0])
        self.at("reveals")
        self.play(Create(p1), run_time=1.2)
        self.play(Create(p2), run_time=1.2)
        d1 = loop_dot(c1, YELLOW, 4.0, 0.1)
        d2 = loop_dot(c2, YELLOW, 4.0, 0.1)
        self.add(d1, d2)
        self.at("A trend points")
        self.play(FadeIn(l1), Indicate(p1, color=YELLOW), run_time=1.4)
        self.at("a wave to")
        self.play(FadeIn(l2), Indicate(p2, color=YELLOW), run_time=1.4)
        self.at("Coevolution also")
        h = bacterium_icon(1.2).move_to([-5.0, -1.4, 0])
        ph = phage_icon(1.0).move_to([-1.9, -1.2, 0])
        bob(h, 0.06, 2.0)
        bob(ph, 0.06, 2.2, 1.0)
        ht = T("heritable\nchange?", 28, GREEN).move_to([-5.0, -2.9, 0])
        pt = T("heritable\nchange?", 28, PURPLE).move_to([-1.9, -2.9, 0])
        self.play(FadeIn(h), FadeIn(ph), FadeIn(ht), FadeIn(pt), run_time=1.2)
        self.at("checked with controls")
        ct = T("control:\none side held fixed", 30, YELLOW).move_to([3.4, -1.9, 0])
        self.play(FadeIn(ct, shift=LEFT * 0.2), run_time=0.8)
        self.play(Indicate(ct, color=YELLOW), run_time=0.8)
        self.finish()


class S19End(EndCard):
    LINE = "Across time: a one-way trend points to escalation, a wave to tracking."
