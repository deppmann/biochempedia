"""Catching Proteins on the Move (organelles-as-a-system, film 2 = chapter 2).

THE WORLD: the same cell and COLOUR MAP as film 1 (NUCLEUS deep blue, mRNA purple, ROUGH ER teal + dark dots,
GOLGI orange, VESICLES / marked protein gold, MEMBRANE grey, MITOCHONDRIA red, ATP yellow). Added here:
CONDENSING VACUOLES = pale-gold sacs, STORAGE GRANULES = solid gold, a CLOCK, and a BAR CHART.
Cell geometry is film 1's; in the chart scenes the whole cell is scaled to 0.55 and moved left (a transform).
Schematic, not to scale; the cloud of marked dots is schematic, the bars are the quoted values only.
"""
import numpy as np
from bp_style import *  # noqa: F401,F403

PURPLE = "#B58CD9"
NUCB = "#5B7CFA"
ORANGE = "#F29E4C"
PALE = "#EBD79A"
DGOLD = "#E0A020"
RY = -0.1
CELL_C = np.array([-0.5, -0.55, 0])
NUC_C = np.array([-4.5, RY, 0])
NUC_R = 1.4
MEM = np.array([5.13, RY, 0])
STOPS = ["nucleus", "ribosome", "vesicle", "Golgi", "vesicle", "membrane"]

ST = {"S": 1.0, "C": CELL_C.copy()}


def P(x, y):
    return np.array([x, y, 0.0])


def setw(s=1.0, c=None):
    ST["S"] = s
    ST["C"] = np.array(CELL_C if c is None else [c[0], c[1], 0.0], float)


def W(p):
    p = np.array([p[0], p[1], 0.0])
    return ST["S"] * (p - CELL_C) + ST["C"]


def sk():
    return ST["S"]


def sw(w):
    return w * max(ST["S"], 0.55) ** 0.5


# ---------------------------------------------------------------- slots (world coordinates)
ER_SL = ([(x, RY + 0.87) for x in (-1.7, -1.2, -0.7, -0.2, 0.25)]
         + [(x, RY + 0.33) for x in (-1.7, -1.2, -0.7, -0.2, 0.25)]
         + [(x, RY - 0.87) for x in (-1.7, -1.2, -0.7, -0.2)])
GV_SL = [(1.5, 1.0), (2.2, 1.15), (2.9, 1.1), (1.5, -1.2), (2.3, -1.35), (3.0, -1.3), (1.15, 0.45), (1.15, -0.65)]
VAC_C = [(3.95, 0.5), (3.95, -0.75)]
VAC_SL = [(3.95 + dx, y + dy) for (_, y) in VAC_C for dx, dy in ((-0.13, 0.1), (0.13, 0.1), (-0.13, -0.1), (0.13, -0.1))]
GR_SL = [(4.6, 0.45), (4.85, -0.4), (4.75, -1.0), (4.4, -1.6), (3.9, -1.9), (3.3, -2.15), (2.6, -2.2)]
SC_SL = [(-3.1, -1.6), (-2.2, 1.35), (0.2, 1.5), (0.7, -1.9), (-1.2, -2.0), (-5.0, -1.9), (-3.0, 1.3), (1.9, -2.2),
         (-0.4, -1.55), (2.3, 1.7), (-5.3, 1.2), (3.2, -1.65)]
N_DOTS = 12

S0 = dict(ER=10)
S7 = dict(ER=5, GV=5)
S37 = dict(VAC=6)
S117 = dict(GR=7)


# ---------------------------------------------------------------- parts
def cell_m():
    return Ellipse(width=11.4 * sk(), height=5.4 * sk(), stroke_color=GREY, stroke_width=sw(8), fill_color=GREY,
                   fill_opacity=0.10).move_to(W(CELL_C))


def nuc_m():
    return Circle(radius=NUC_R * sk(), stroke_color=NUCB, stroke_width=sw(6), fill_color=NUCB,
                  fill_opacity=0.24).move_to(W(NUC_C))


def nuc_label():
    return T("nucleus", 26, "#A9BBFF").move_to(W(NUC_C + DOWN * 1.2)).set_stroke(BG, 8, background=True)


def er_m(phase=0.0, op=1.0):
    g = VGroup()
    for off in (0.65, 0.0, -0.65):
        g.add(ParametricFunction(
            lambda x, o=off: W(P(x, RY + o + 0.1 * np.sin(2 * np.pi * (x + 0.8) / 0.8 + phase))),
            t_range=[-2.0, 0.4], color=TEAL, stroke_width=sw(11)))
    return g.set_stroke(opacity=op)


def er_live(scene, speed=1.0):
    tr = ValueTracker(0)
    tr.add_updater(lambda t, dt: t.increment_value(dt * speed))
    scene.add(tr)
    er = always_redraw(lambda: er_m(tr.get_value()))
    scene.add(er)
    return er


def dots_m():
    d = VGroup()
    for k in range(5):
        x = -1.8 + 0.5 * k + 0.1
        for y in (RY + 0.85, RY - 0.85):
            d.add(Dot(W(P(x, y)), radius=0.09 * sk() ** 0.5, color=BG).set_stroke(TEXT, sw(2.5)).set_fill(BG, 1))
    return d


def golgi_m():
    g = VGroup()
    for i in range(5):
        x0 = 1.6 + 0.45 * i
        h = 0.95 - 0.1 * abs(i - 2)
        g.add(ParametricFunction(lambda t, x0=x0, h=h: W(P(x0 + 0.2 * (1 - (t / h) ** 2), RY + t)), t_range=[-h, h],
                                 color=ORANGE, stroke_width=sw(14)))
    return g


def gv_m(pos):
    return Circle(radius=0.2 * sk(), stroke_color=GOLD, stroke_width=sw(4), fill_color=GOLD,
                  fill_opacity=0.13).move_to(W(pos))


def vac_m(pos):
    return Circle(radius=0.36 * sk(), stroke_color=PALE, stroke_width=sw(4), fill_color=PALE,
                  fill_opacity=0.28).move_to(W(pos))


def gran_m(pos):
    return Circle(radius=0.17 * sk(), stroke_color=GOLD, stroke_width=sw(2), fill_color=GOLD,
                  fill_opacity=0.95).move_to(W(pos))


def glow_m(pos, r=0.1, op=1.0):
    return VGroup(Circle(r * 2.2, stroke_width=0, fill_color=GOLD, fill_opacity=0.10 * op),
                  Circle(r * 1.5, stroke_width=0, fill_color=GOLD, fill_opacity=0.18 * op),
                  Circle(r, stroke_color=GOLD, stroke_width=2, fill_color=GOLD, fill_opacity=0.9 * op)).move_to(pos)


class World:
    """The cell. .static is one VGroup; .vacs / .grans / .gvs are lists so scenes can animate them."""

    def __init__(self, scene, live=True, granules=True, label=False):
        self.scene = scene
        self.cell, self.nuc = cell_m(), nuc_m()
        self.dots = dots_m()
        self.golgi = golgi_m()
        self.gvs = [gv_m(p) for p in GV_SL[:8]]
        self.vacs = [vac_m(p) for p in VAC_C]
        self.grans = [gran_m(p) for p in GR_SL] if granules else []
        self.er_static = None if live else er_m()
        parts = [self.cell, self.nuc, self.dots, self.golgi, *self.gvs, *self.vacs, *self.grans]
        if self.er_static is not None:
            parts.append(self.er_static)
        self.static = VGroup(*parts)
        if label:
            self.static.add(nuc_label())
        self.live = live

    def add(self, motes_on=True):
        self.scene.add(self.static)
        if self.live:
            self.er = er_live(self.scene)
        if motes_on:
            motes(self.scene)
        return self


def bob(m, amp=0.08, period=2.2, ph=0.0):
    m._bt = ph

    def u(mm, dt):
        a = np.sin(2 * np.pi * mm._bt / period)
        mm._bt += dt
        b = np.sin(2 * np.pi * mm._bt / period)
        mm.shift(UP * amp * (b - a))
    m.add_updater(u)
    return m


def breathe(m, amp=0.06, period=2.6):
    m._bt = 0.0
    m._cur = 1.0

    def u(mm, dt):
        mm._bt += dt
        tgt = 1 + amp * np.sin(2 * np.pi * mm._bt / period)
        mm.scale(tgt / mm._cur)
        mm._cur = tgt
    m.add_updater(u)
    return m


def motes(scene, n=22):
    rng = np.random.RandomState(7)
    g = VGroup()
    cx, cy, S = ST["C"][0], ST["C"][1], sk()
    for i in range(n):
        d = Dot(radius=rng.uniform(0.07, 0.12) * S ** 0.5, color=TEAL if i % 2 else GREY).set_opacity(0.5)
        d.move_to(W(P(rng.uniform(-5, 4), rng.uniform(-2.4, 1.9))))
        d.v = np.array([rng.uniform(-0.7, 0.7), rng.uniform(-0.5, 0.5), 0]) * S

        def u(m, dt, cx=cx, cy=cy, S=S):
            m.shift(m.v * dt)
            p = m.get_center()
            if ((p[0] - cx) / (5.5 * S)) ** 2 + ((p[1] - cy) / (2.5 * S)) ** 2 > 1:
                m.v = -m.v
        d.add_updater(u)
        g.add(d)
    g.set_z_index(-1)
    scene.add(g)
    return g


def ambient(scene, n=26):
    """Faint drifting dots over a whole frame, for scenes that are not the cell."""
    rng = np.random.RandomState(11)
    g = VGroup()
    for i in range(n):
        d = Dot(radius=rng.uniform(0.05, 0.1), color=TEAL if i % 2 else GREY).set_opacity(0.35)
        d.move_to([rng.uniform(-6.5, 6.5), rng.uniform(-3.5, 3.5), 0])
        d.v = np.array([rng.uniform(-0.5, 0.5), rng.uniform(-0.4, 0.4), 0])

        def u(m, dt):
            m.shift(m.v * dt)
            p = m.get_center()
            if abs(p[0]) > 6.6:
                m.v[0] = -m.v[0]
            if abs(p[1]) > 3.6:
                m.v[1] = -m.v[1]
        d.add_updater(u)
        g.add(d)
    g.set_z_index(-5)
    scene.add(g)
    return g


def lab(text, pos, size=28, color=TEXT, **kw):
    return T(text, size, color, **kw).move_to(pos).set_stroke(BG, 8, background=True)


# ---------------------------------------------------------------- route strip (film 1's)
def strip_m(lit=()):
    chips = [chip(s, PURPLE if i == 0 else GOLD, size=24, pad=0.12) for i, s in enumerate(STOPS)]
    items = []
    for i, c in enumerate(chips):
        if i:
            items.append(T("→", 24, GREY))
        items.append(c)
    g = VGroup(*items).arrange(RIGHT, buff=0.14).move_to(P(0, 3.4))
    g.chips = chips
    for i, c in enumerate(chips):
        _style(c, i in lit)
    return g


def _style(c, on):
    col = c[0].get_stroke_color()
    c[0].set_stroke(opacity=1 if on else 0.3, width=4 if on else 2.5).set_fill(col, 0.4 if on else 0.08)
    c[1].set_opacity(1 if on else 0.4)


def light(g, idx):
    out = []
    for i, c in enumerate(g.chips):
        on = i in idx
        col = c[0].get_stroke_color()
        out.append(c[0].animate.set_stroke(opacity=1 if on else 0.3, width=4 if on else 2.5).set_fill(col, 0.4 if on else 0.08))
        out.append(c[1].animate.set_opacity(1 if on else 0.4))
    return out


def route_purple():
    return Line(W(P(-3.1, RY)), W(P(-2.0, RY)), color=PURPLE, stroke_width=sw(9))


def route_gold():
    return Line(W(P(0.4, RY)), W(MEM), color=GOLD, stroke_width=sw(8)).set_z_index(-2)


# ---------------------------------------------------------------- the marked cloud
def targets(ER=0, GV=0, VAC=0, GR=0, n=N_DOTS):
    pts = []
    for k, sl in ((ER, ER_SL), (GV, GV_SL), (VAC, VAC_SL), (GR, GR_SL)):
        pts += [W(P(*s)) for s in sl[:k]]
    i = 0
    while len(pts) < n:
        pts.append(W(P(*SC_SL[i % len(SC_SL)])))
        i += 1
    return pts


class Cloud:
    def __init__(self, scene, state, n=N_DOTS, add=True):
        pts = targets(n=n, **state)
        r = 0.1 * max(sk(), 0.75)
        self.dots = [glow_m(p, r) for p in pts]
        self.g = VGroup(*self.dots)
        for i, d in enumerate(self.dots):
            bob(d, 0.035, 1.8 + 0.13 * i, ph=0.37 * i)
        if add:
            scene.add(self.g)

    def go(self, state):
        pts = targets(n=len(self.dots), **state)
        return [d.animate.move_to(p) for d, p in zip(self.dots, pts)]


# ---------------------------------------------------------------- rain of beads (full-size world)
def rain(scene, kind, xr, n, ystops=(0.8, 0.9), ytop=3.1, speed=1.5, seed=3):
    rng = np.random.RandomState(seed)
    g = VGroup()
    for i in range(n):
        if kind == "gold":
            m = glow_m(P(0, 0), 0.09)
        else:
            m = Dot(radius=0.1, color=GREY).set_opacity(0.95)
        m.ys = rng.uniform(*ystops)
        m.yt = ytop
        m.xr = xr
        m.v = rng.uniform(0.8, 1.2) * speed
        m.move_to(P(rng.uniform(*xr), rng.uniform(m.ys, ytop)))

        def u(mm, dt):
            mm.shift(DOWN * mm.v * dt)
            if mm.get_center()[1] < mm.ys:
                mm.move_to(P(np.random.uniform(*mm.xr), mm.yt))
        m.add_updater(u)
        g.add(m)
    scene.add(g)
    return g


# ---------------------------------------------------------------- clock
class Clk:
    def __init__(self, scene, face_c, text_c, minutes=0.0, text=None, size=28):
        self.m = ValueTracker(minutes)
        self.idle = ValueTracker(0)
        self.idle.add_updater(lambda t, dt: t.increment_value(dt * 0.5))
        self.txt = text
        self.face_c = P(face_c[0], face_c[1])
        self.size = size
        face = Circle(0.45, stroke_color=TEXT, stroke_width=4, fill_color=TEXT, fill_opacity=0.08).move_to(self.face_c)
        cap = Dot(self.face_c, radius=0.05, color=TEXT)
        hand = always_redraw(lambda: Line(self.face_c, self.face_c + 0.36 * np.array(
            [np.sin(0.09 * self.m.get_value() + self.idle.get_value()),
             np.cos(0.09 * self.m.get_value() + self.idle.get_value()), 0]), color=GOLD, stroke_width=5))
        tc = P(text_c[0], text_c[1])

        def mk():
            s = self.txt if self.txt is not None else f"{int(round(self.m.get_value()))} minutes of chase"
            t = T(s, self.size, TEXT)
            return t.move_to(tc + RIGHT * t.width / 2)
        text_m = always_redraw(mk)
        self.static = VGroup(face, cap)
        scene.add(self.idle, self.m, self.static, hand, text_m)
        self.parts = (self.static, hand, text_m)


# ---------------------------------------------------------------- chart
BX = [1.45, 3.0, 4.55, 6.1]
BASE = -2.2
SCY = 3.5 / 100
BW = 0.9
BCOL = [TEAL, GOLD, PALE, DGOLD]
BNAMES = ["rough\nER", "Golgi\nvesicles", "condensing\nvacuoles", "storage\ngranules"]


class Chart:
    def __init__(self, scene):
        self.tr = [ValueTracker(0) for _ in range(4)]
        self.scene = scene
        title = VGroup(T("Where the marked grains are", 24, TEXT), T("(% of counted grains)", 24, TEXT)
                       ).arrange(DOWN, buff=0.08).move_to(P(3.8, 2.55))
        sw_ = DashedVMobject(Rectangle(width=0.36, height=0.26, stroke_color=TEXT, stroke_width=2), num_dashes=12)
        lg = T("other parts (not shown)", 22, TEXT)
        leg = VGroup(sw_, lg).arrange(RIGHT, buff=0.15).move_to(P(3.8, 1.85))
        base = Line(P(0.85, BASE), P(6.75, BASE), color=TEXT, stroke_width=3)
        grid = VGroup(*[DashedLine(P(0.85, BASE + v * SCY), P(6.75, BASE + v * SCY), color=GREY, stroke_width=1.5, dash_length=0.12)
                        for v in (50, 100)])
        ticks = VGroup(*[T(s, 22, TEXT).move_to(P(0.5, BASE + v * SCY)) for s, v in (("0", 0), ("50", 50), ("100", 100))])
        cats = VGroup(*[T(n, 22, c, line_spacing=0.6).move_to(P(x, BASE - 0.5)) for n, c, x in zip(BNAMES, BCOL, BX)])
        self.slots = [DashedVMobject(Rectangle(width=BW, height=1.2, stroke_color=TEXT, stroke_width=2), num_dashes=40
                                     ).move_to(P(x, BASE + 0.6)).set_opacity(0.5) for x in BX]
        self.frame = VGroup(title, leg, base, grid, ticks, cats, *self.slots)
        self.bars, self.vals = [], []
        for i in range(4):
            tr = self.tr[i]

            def bar(i=i, tr=tr):
                v = tr.get_value()
                h = max(v * SCY, 0.001)
                r = Rectangle(width=BW, height=h, stroke_width=0, fill_color=BCOL[i], fill_opacity=0.92 if v > 0.05 else 0)
                return r.move_to(P(BX[i], BASE + h / 2))

            def val(i=i, tr=tr):
                v = tr.get_value()
                if v < 0.5:
                    return VMobject()
                gys = (BASE + 50 * SCY, BASE + 100 * SCY)
                y = None
                for off in (0.32, 0.2):
                    if all(abs(BASE + v * SCY + off - gy) >= 0.2 for gy in gys):
                        y = BASE + v * SCY + off
                        break
                if y is None:
                    gy = min(gys, key=lambda g: abs(BASE + v * SCY + 0.32 - g))
                    y = gy + 0.32
                return T(f"{v:.1f}%", 28, BCOL[i]).move_to(P(BX[i], y)).set_stroke(BG, 6, background=True)
            self.bars.append(always_redraw(bar))
            self.vals.append(always_redraw(val))

        for s, tr in zip(self.slots, self.tr):
            s.add_updater(lambda m, tr=tr: m.set_opacity(0.5 if tr.get_value() < 0.5 else 0))

    def add(self, scene):
        scene.add(self.frame, *self.bars, *self.vals)

    def fade_in(self):
        return FadeIn(self.frame)

    def set(self, *vals):
        return [self.tr[i].animate.set_value(v) for i, v in enumerate(vals) if v is not None]


CH_S = 0.55
CH_C = (-3.5, 0.2)


def chart_world(scene, live=True, granules=True):
    setw(CH_S, CH_C)
    return World(scene, live=live, granules=granules).add()


def chart_clock(scene, minutes=0.0, text=None):
    return Clk(scene, (-6.2, 2.45), (-5.55, 2.45), minutes, text, 28)


def full_clock(scene, minutes=0.0, text=None):
    return Clk(scene, (6.2, 3.15), (3.1, 2.2), minutes, text, 26)


def thumb(cx, vals, cy=0.45):
    """A small copy of the chart for one time point (only the quoted values are drawn)."""
    pw, ph = 2.8, 3.4
    frame = RoundedRectangle(corner_radius=0.12, width=pw, height=ph, stroke_color=GREY, stroke_width=3,
                             fill_color=GREY, fill_opacity=0.06).move_to(P(cx, cy))
    by = cy - ph / 2 + 0.5
    g = VGroup(frame, Line(P(cx - 1.2, by), P(cx + 1.2, by), color=TEXT, stroke_width=2.5))
    bars = []
    for i, v in enumerate(vals):
        x = cx + (-0.93 + 0.62 * i)
        if v:
            h = v * 2.7 / 100
            r = Rectangle(width=0.5, height=h, stroke_width=0, fill_color=BCOL[i], fill_opacity=0.92).move_to(P(x, by + h / 2))
            g.add(r)
            bars.append(r)
        else:
            g.add(DashedVMobject(Rectangle(width=0.5, height=0.5, stroke_color=TEXT, stroke_width=1.5), num_dashes=16
                                 ).move_to(P(x, by + 0.25)).set_opacity(0.4))
    g.bars = bars
    return g


def stamp(text, pos, color=TEXT, size=40, ang=-0.12):
    w = T(text, size, color, font=TITLE_FONT)
    box = RoundedRectangle(corner_radius=0.1, width=w.width + 0.5, height=w.height + 0.4, stroke_color=color, stroke_width=5,
                           fill_color=BG, fill_opacity=0.9)
    g = VGroup(box, w.move_to(box)).rotate(ang).move_to(pos)
    return g


# ================================================================ S00
class S00Title(TitleCard):
    LESSON = "Organelles as a System"
    TITLE = "Catching Proteins on the Move"


# ================================================================ S01
class S01Question(SpokenScene):
    def construct(self):
        setw(1.0)
        w = World(self, live=True)
        self.play(Create(w.cell), FadeIn(w.nuc), run_time=1.2)
        w.add()
        self.add(nuc_label())
        parcel = glow_m(W(P(-0.8, 0.225)), 0.14)
        self.play(FadeIn(parcel, scale=0.6), run_time=0.8)
        breathe(parcel, 0.1, 1.8)
        st = strip_m(())
        self.play(FadeIn(st, shift=DOWN * 0.2), run_time=0.8)
        self.at("the first film drew")
        rp, rg = route_purple(), route_gold()
        self.play(Create(rp), Create(rg), run_time=1.6)
        self.play(*light(st, (0,)), run_time=0.3)
        self.at("rough ER")
        self.play(*light(st, (1,)), run_time=0.4)
        self.at("to the Golgi")
        self.play(*light(st, (3,)), Indicate(w.golgi, color=ORANGE, scale_factor=1.05), run_time=0.8)
        self.at("cell membrane")
        self.play(*light(st, (5,)), run_time=0.5)
        self.at("but a drawing")
        s = stamp("drawing", P(-1.0, -2.0))
        s.scale(2.4)
        s.set_opacity(0)
        self.add(s)
        self.play(s.animate.scale(1 / 2.4).set_opacity(1), run_time=0.45, rate_func=rush_into)
        self.play(s.animate.shift(DOWN * 0.07), rate_func=there_and_back, run_time=0.25)
        self.at("not evidence")
        q = T("?", 120, GOLD, font=TITLE_FONT)
        q.move_to(P(1.4, 1.5))
        self.play(FadeIn(q, scale=0.6), run_time=0.7)
        bob(q, 0.12, 1.6)
        self.finish()


# ================================================================ S02
def guinea_pig(pos):
    body = Ellipse(width=2.3, height=1.35, stroke_color="#C9A27C", stroke_width=4, fill_color="#B08968", fill_opacity=0.9)
    head = Circle(0.55, stroke_color="#C9A27C", stroke_width=4, fill_color="#B08968", fill_opacity=0.95).shift(LEFT * 1.2 + UP * 0.1)
    ear = Circle(0.2, stroke_color="#C9A27C", stroke_width=3, fill_color="#8C6A4C", fill_opacity=0.95).shift(LEFT * 0.95 + UP * 0.58)
    eye = Dot(LEFT * 1.42 + UP * 0.22, radius=0.07, color=BG)
    nose = Dot(LEFT * 1.72 + UP * 0.05, radius=0.07, color="#F4B6B6")
    paws = VGroup(Ellipse(width=0.4, height=0.22, color="#C9A27C", fill_color="#8C6A4C", fill_opacity=1).shift(DOWN * 0.7 + LEFT * 0.6),
                  Ellipse(width=0.4, height=0.22, color="#C9A27C", fill_color="#8C6A4C", fill_opacity=1).shift(DOWN * 0.7 + RIGHT * 0.5))
    return VGroup(paws, body, head, ear, eye, nose).move_to(pos)


class S02Cells(SpokenScene):
    def construct(self):
        ambient(self)
        self.at("in 1967")
        yr = T("1967", 60, GOLD, font=TITLE_FONT).move_to(P(-4.6, 2.75))
        self.play(FadeIn(yr, shift=RIGHT * 0.3), run_time=0.8)
        self.at("James")
        nm = T("Jamieson and Palade", 34, TEXT).move_to(P(-3.1, 1.85))
        self.play(FadeIn(nm, shift=UP * 0.2), run_time=0.9)
        self.at("thin slices")
        dish = Ellipse(width=3.8, height=1.0, stroke_color=GREY, stroke_width=5, fill_color=GREY, fill_opacity=0.12).move_to(P(1.9, -1.2))
        slc = Ellipse(width=2.5, height=0.55, stroke_color="#E3A99B", stroke_width=3, fill_color="#D49A8A", fill_opacity=0.85).move_to(P(1.9, -1.1))
        self.play(FadeIn(dish, shift=UP * 0.2), FadeIn(slc, scale=0.7), run_time=1.0)
        self.at("guinea pig")
        gp = guinea_pig(P(-3.9, -0.9))
        ar = Arrow(P(-2.4, -0.9), P(0.0, -1.1), buff=0.1, color=GOLD, stroke_width=6)
        self.play(FadeIn(gp, shift=RIGHT * 0.3), GrowArrow(ar), run_time=0.7)
        bob(gp, 0.05, 1.8)
        self.at("pancreas")
        pl = lab("pancreas slice", P(1.9, -2.1), 30, TEXT)
        self.play(FadeIn(pl), Indicate(slc, color="#E3A99B", scale_factor=1.1), run_time=0.9)
        self.at("the cells they studied")
        setw(1.0)
        w = World(self, live=False)
        w.static.save_state()
        w.static.scale(0.1, about_point=ORIGIN).move_to(P(1.9, -1.1))
        self.add(w.static)
        self.play(FadeOut(VGroup(yr, nm, gp, ar, pl, dish)), FadeOut(slc),
                  Restore(w.static), run_time=1.5)
        motes(self)
        self.at("make digestive enzymes")
        lb = lab("makes digestive enzymes (not a beta cell)", P(0.4, 2.75), 28, TEXT)
        self.play(FadeIn(lb, shift=DOWN * 0.15), run_time=0.8)
        self.at("not insulin")
        self.play(Indicate(lb, color=GOLD, scale_factor=1.06), run_time=1.0)
        self.at("but they too send")
        parcel = glow_m(W(P(-0.8, 0.225)), 0.13)
        self.play(FadeIn(parcel, scale=0.6), run_time=0.5)
        for p in (P(0.4, RY), P(2.5, RY), MEM):
            self.play(parcel.animate.move_to(W(p)), run_time=0.7, rate_func=linear)
        self.play(parcel.animate.move_to(P(6.3, RY)).scale(1.2), run_time=0.7, rate_func=linear)
        self.play(FadeOut(parcel), run_time=0.4)
        self.finish()


# ================================================================ S03
class S03Problem(SpokenScene):
    def construct(self):
        setw(1.0)
        w = World(self, live=True).add()
        self.at("a cell is always making")
        grey = VGroup(*[Dot(W(P(*s)), radius=0.08, color=GREY).set_opacity(0.95) for s in ER_SL[:10]])
        self.play(LaggedStart(*[FadeIn(d, scale=0.4) for d in grey], lag_ratio=0.18), run_time=2.0)
        for i, d in enumerate(grey):
            bob(d, 0.04, 1.7 + 0.1 * i, ph=0.3 * i)
        self.at("if every protein carries")
        sites = ([W(P(*s)) for s in ER_SL[:9]] + [W(P(*s)) for s in GV_SL[:6]] + [W(P(*s)) for s in VAC_SL[:4]]
                 + [W(P(*s)) for s in GR_SL[:6]])
        glows = VGroup(*[glow_m(p, 0.1) for p in sites])
        self.play(LaggedStart(*[FadeIn(g, scale=0.4) for g in glows], lag_ratio=0.06), run_time=1.6)
        for i, g in enumerate(glows):
            bob(g, 0.035, 1.6 + 0.07 * i, ph=0.2 * i)
        self.at("the mark is everywhere")
        t1 = lab("everything marked: no order visible", P(0.4, 2.65), 30, GOLD)
        self.play(FadeIn(t1, shift=DOWN * 0.15), run_time=0.8)
        self.at("you learn nothing")
        self.play(Indicate(glows, color=GOLD, scale_factor=1.15), run_time=1.4)
        self.at("you need to mark")
        self.play(FadeOut(glows), FadeOut(t1), run_time=0.9)
        rng = np.random.RandomState(5)
        c = P(-1.0, 1.15)
        batch = VGroup(*[glow_m(c + P(*(rng.uniform(-0.3, 0.3, 2))), 0.09) for _ in range(6)])
        ring = Circle(0.62, stroke_color=GOLD, stroke_width=5).move_to(c)
        t2 = lab("mark one batch", P(-1.0, 2.7), 32, GOLD)
        self.play(FadeIn(batch, scale=0.5), Create(ring), FadeIn(t2), run_time=1.2)
        for i, d in enumerate(batch):
            bob(d, 0.03, 1.5 + 0.1 * i, ph=0.3 * i)
        breathe(ring, 0.05, 2.0)
        self.finish()


# ================================================================ S04
class S04Pulse(SpokenScene):
    def construct(self):
        setw(1.0)
        w = World(self, live=True).add()
        self.at("so they gave")
        clk = full_clock(self, 0.0, "pulse: 3 min")
        note = lab("3-minute pulse", P(-3.3, 2.6), 30, GOLD)
        self.play(FadeIn(clk.static), FadeIn(note), run_time=1.0)
        self.at("a short pulse")
        beads = rain(self, "gold", (-1.9, 0.3), 9, ystops=(0.8, 0.95), speed=1.1)
        self.play(clk.m.animate.set_value(3), run_time=3.0, rate_func=linear)
        self.at("only proteins made")
        marks = VGroup(*[glow_m(W(P(*s)), 0.1) for s in ER_SL[:5] + ER_SL[10:12]])
        self.play(LaggedStart(*[FadeIn(g, scale=0.4) for g in marks], lag_ratio=0.2), run_time=1.6)
        for i, g in enumerate(marks):
            bob(g, 0.03, 1.5 + 0.1 * i, ph=0.3 * i)
        self.at("carried the mark")
        self.play(Indicate(marks, color=GOLD, scale_factor=1.2), run_time=1.5)
        self.finish()


# ================================================================ S05
class S05Chase(SpokenScene):
    def construct(self):
        setw(1.0)
        w = World(self, live=True).add()
        clk = full_clock(self, 3.0, "pulse: 3 min")
        batch_pos = ER_SL[:5] + ER_SL[10:12]
        marks = VGroup(*[glow_m(W(P(*s)), 0.1) for s in batch_pos])
        self.add(marks)
        for i, g in enumerate(marks):
            bob(g, 0.03, 1.5 + 0.1 * i, ph=0.3 * i)
        self.at("then came the chase")
        clk.txt = None
        clk.m.set_value(0)
        self.play(Indicate(clk.static, scale_factor=1.2), run_time=1.0)
        grey = rain(self, "grey", (-3.8, 3.4), 16, ystops=(-2.0, 0.9), speed=1.3, seed=9)
        self.at("plenty of the ordinary")
        self.wait(1.0)
        self.at("proteins made after")
        new = VGroup(*[Dot(W(P(*s)), radius=0.08, color=GREY).set_opacity(0.95) for s in ER_SL[5:10] + ER_SL[12:14]])
        self.play(LaggedStart(*[FadeIn(d, scale=0.4) for d in new], lag_ratio=0.2), run_time=1.5)
        for i, d in enumerate(new):
            bob(d, 0.04, 1.7 + 0.1 * i, ph=0.3 * i)
        self.at("carried no mark")
        self.wait(0.8)
        self.at("the marked batch")
        halo = Circle(1.35, stroke_width=0, fill_color=GOLD, fill_opacity=0.14).move_to(W(P(-0.7, 0.55)))
        t = lab("marked batch", P(-0.7, 2.7), 30, GOLD)
        self.play(FadeIn(halo), FadeIn(t), run_time=1.2)
        breathe(halo, 0.08, 2.2)
        self.at("on its own")
        self.play(Indicate(marks, color=GOLD, scale_factor=1.25), run_time=1.4)
        self.finish()


# ================================================================ S06
class S06Methods(SpokenScene):
    def construct(self):
        ambient(self)
        div = Line(P(0, -3.4), P(0, 3.0), color=GREY, stroke_width=3)
        self.play(Create(div), run_time=1.2)
        self.at("in one")
        h1 = T("centrifuge", 34, TEXT).move_to(P(-3.4, 3.0))
        n1 = T("1", 80, GOLD, font=TITLE_FONT).move_to(P(-3.4, 0.3))
        self.play(FadeIn(h1), FadeIn(n1, scale=0.6), run_time=0.8)
        self.at("broken cells")
        c = P(-3.4, 0.3)
        base = Circle(1.5, stroke_color=GREY, stroke_width=4, fill_color=GREY, fill_opacity=0.12).move_to(c)
        bar = RoundedRectangle(corner_radius=0.2, width=2.7, height=0.5, stroke_color=TEXT, stroke_width=4,
                               fill_color=TEXT, fill_opacity=0.12).move_to(c)
        tb = VGroup(*[Rectangle(width=0.5, height=0.7, stroke_color=TEXT, stroke_width=3, fill_color=TEAL, fill_opacity=0.5
                                ).move_to(c + RIGHT * s * 1.35) for s in (-1, 1)])
        rotor = VGroup(bar, tb)
        self.play(FadeOut(n1), FadeIn(base), FadeIn(rotor), run_time=0.8)
        self.at("were spun")
        self.play(Rotate(rotor, angle=5 * TAU, about_point=c, rate_func=smooth), run_time=2.4)
        self.at("settled into layers")
        tube = RoundedRectangle(corner_radius=0.3, width=1.1, height=3.8, stroke_color=TEXT, stroke_width=4).move_to(P(-4.1, -0.1))
        bands = VGroup(Rectangle(width=1.0, height=0.8, stroke_width=0, fill_color=GREY, fill_opacity=0.3),
                       Rectangle(width=1.0, height=0.8, stroke_width=0, fill_color=TEAL, fill_opacity=0.8),
                       Rectangle(width=1.0, height=0.8, stroke_width=0, fill_color=ORANGE, fill_opacity=0.8),
                       Rectangle(width=1.0, height=0.8, stroke_width=0, fill_color=GREY, fill_opacity=0.3)).arrange(DOWN, buff=0.02).move_to(tube)
        self.play(FadeOut(rotor), FadeOut(base), FadeIn(tube), run_time=0.5)
        self.play(LaggedStart(*[FadeIn(b, shift=DOWN * 0.3) for b in bands], lag_ratio=0.2), run_time=1.0)
        l1 = T("ER pieces", 30, TEAL).move_to(P(-1.6, bands[1].get_center()[1]))
        l2 = T("Golgi pieces", 30, ORANGE).move_to(P(-1.55, bands[2].get_center()[1]))
        gl = VGroup(*[glow_m(bands[1].get_center() + P(dx, dy), 0.07) for dx, dy in
                      ((-0.3, 0.15), (0.0, -0.15), (0.3, 0.15), (0.3, -0.2), (-0.3, -0.2))])
        self.play(FadeIn(l1), FadeIn(l2), FadeIn(gl), run_time=0.6)
        for i, g in enumerate(gl):
            bob(g, 0.025, 1.5 + 0.1 * i, ph=0.3 * i)
        self.at("in the other")
        h2 = T("electron microscope", 34, TEXT).move_to(P(3.4, 3.0))
        self.play(FadeIn(h2), run_time=0.7)
        self.at("electron microscope pictures")
        panel = RoundedRectangle(corner_radius=0.2, width=5.8, height=4.5, stroke_color=GREY, stroke_width=4,
                                 fill_color="#C8CCD2", fill_opacity=0.95).move_to(P(3.4, 0.3))
        nuc = Circle(0.9, stroke_color="#8A9099", stroke_width=4, fill_color="#9AA0A8", fill_opacity=0.9).move_to(P(1.7, 1.2))
        ers = VGroup(*[ParametricFunction(lambda x, o=o: P(x, o + 0.1 * np.sin(5 * x)), t_range=[1.5, 5.1], color=TEAL, stroke_width=9)
                       for o in (0.0, -0.65, -1.3)])
        self.play(FadeIn(panel), FadeIn(nuc), Create(ers), run_time=1.6)
        self.at("radioactive grains")
        rng = np.random.RandomState(4)
        gr = VGroup(*[Dot(P(rng.uniform(1.8, 4.9), o + rng.uniform(0.12, 0.25) * (1 if k % 2 else -1)),
                          radius=0.1, color="#05070B") for k, o in enumerate((0.0, -0.65, -1.3, 0.0, -0.65, -1.3, 0.0, -0.65))])
        gl2 = lab("radioactive grains", P(3.4, -2.6), 30, TEXT)
        self.play(LaggedStart(*[FadeIn(d, scale=0.3) for d in gr], lag_ratio=0.12), FadeIn(gl2), run_time=1.6)
        self.play(Indicate(gr, color=GOLD, scale_factor=1.4), run_time=1.2)
        self.finish()


# ================================================================ S07
class S07Predict(SpokenScene):
    def construct(self):
        w = chart_world(self)
        self.at("time for a prediction")
        ch = Chart(self)
        self.play(ch.fade_in(), run_time=1.2)
        ch.add(self)
        self.at("the clock reads")
        clk = chart_clock(self, 0.0)
        self.play(FadeIn(clk.static), run_time=0.8)
        self.at("right after the pulse")
        q = T("?", 120, GOLD, font=TITLE_FONT).move_to(P(3.8, 0.3))
        self.play(FadeIn(q, scale=0.6), run_time=0.8)
        bob(q, 0.12, 1.6)
        self.at("where do you predict")
        self.play(Indicate(q, color=GOLD, scale_factor=1.2), run_time=1.2)
        self.finish()


# ================================================================ S08
class S08Pause(SpokenScene):
    def construct(self):
        w = chart_world(self)
        ch = Chart(self)
        ch.add(self)
        clk = chart_clock(self, 0.0)
        q = T("?", 120, GOLD, font=TITLE_FONT).move_to(P(3.8, 0.3))
        bob(q, 0.12, 1.6)
        self.add(q)
        tr = ValueTracker(0)
        ctr = P(-3.5, -2.6)
        base = Circle(0.5, color=GREY, stroke_width=5).move_to(ctr)
        arc = always_redraw(lambda: Arc(radius=0.5, start_angle=PI / 2, angle=-TAU * max(tr.get_value(), 0.001),
                                        color=GOLD, stroke_width=8, arc_center=ctr))
        self.add(base, arc)
        self.play(tr.animate.set_value(1), run_time=5.0, rate_func=linear)
        self.finish()


# ================================================================ S09
class S09Reveal(SpokenScene):
    def construct(self):
        w = chart_world(self)
        ch = Chart(self)
        ch.add(self)
        clk = chart_clock(self, 0.0)
        st = strip_m(())
        self.add(st)
        self.at("over the rough ER")
        cl = Cloud(self, S0, add=False)
        self.play(FadeIn(cl.g, scale=0.5), *ch.set(86.3, None, None, None), run_time=2.0)
        cl_note = lab("marked grains: schematic", P(-3.5, -1.75), 24, TEXT)
        self.add(cl_note)
        self.at("at the start of the chase")
        self.play(Indicate(clk.static, scale_factor=1.25), run_time=1.0)
        self.at("that is where")
        n = lab("ribosome on rough ER", P(-3.5, -2.55), 28, TEAL)
        self.play(*light(st, (1,)), FadeIn(n), run_time=0.9)
        self.at("ribosomes build")
        self.play(Indicate(w.dots, color=TEXT, scale_factor=1.1), run_time=1.4)
        self.finish()


# ================================================================ S10
class S10Golgi(SpokenScene):
    def construct(self):
        w = chart_world(self)
        ch = Chart(self)
        ch.tr[0].set_value(86.3)
        ch.add(self)
        clk = chart_clock(self, 0.0)
        cl = Cloud(self, S0)
        self.at("minutes later")
        self.play(clk.m.animate.set_value(7), run_time=1.6, rate_func=linear)
        self.at("spread out")
        self.play(*cl.go(S7), run_time=1.6)
        self.at("by seven minutes")
        self.play(*ch.set(43.7, 43.0, None, None), run_time=2.0)
        self.at("almost as many")
        nt = lab("nearly tied", P(2.25, 0.45), 26, TEXT)
        self.play(FadeIn(nt, shift=DOWN * 0.1), run_time=0.7)
        self.at("golgi vesicles are small")
        gl = lab("Golgi vesicles: small vesicles", P(-3.5, -2.0), 26, GOLD)
        gl2 = lab("at the Golgi's edge", P(-3.5, -2.45), 26, GOLD)
        self.play(FadeIn(gl), FadeIn(gl2), *[Indicate(g, color=GOLD, scale_factor=1.4) for g in w.gvs], run_time=1.6)
        self.finish()


# ================================================================ S11
class S11Vacuoles(SpokenScene):
    def construct(self):
        w = chart_world(self)
        ch = Chart(self)
        ch.tr[0].set_value(43.7)
        ch.tr[1].set_value(43.0)
        ch.add(self)
        clk = chart_clock(self, 7.0)
        cl = Cloud(self, S7)
        self.at("later still")
        self.play(clk.m.animate.set_value(37), run_time=1.0, rate_func=linear)
        self.at("the mark moved on")
        self.play(*cl.go(S37), *ch.set(0, 0, None, None), run_time=2.0)
        self.at("the grains gathered")
        lb = lab("condensing vacuoles", P(-3.5, -1.95), 28, PALE)
        lb2 = lab("(forming storage granules)", P(-3.5, -2.45), 26, PALE)
        self.play(*ch.set(None, None, 48.5, None), FadeIn(lb), FadeIn(lb2), run_time=3.0)
        self.at("these are storage granules")
        self.play(*[Indicate(v, color=PALE, scale_factor=1.3) for v in w.vacs], run_time=1.6)
        self.finish()


# ================================================================ S12
class S12Granules(SpokenScene):
    def construct(self):
        w = chart_world(self)
        ch = Chart(self)
        ch.tr[2].set_value(48.5)
        ch.add(self)
        clk = chart_clock(self, 37.0)
        cl = Cloud(self, S37)
        lb = lab("condensing vacuoles", P(-3.5, -1.95), 28, PALE)
        lb2 = lab("(forming storage granules)", P(-3.5, -2.45), 26, PALE)
        self.add(lb, lb2)
        self.at("at the last time point")
        self.play(clk.m.animate.set_value(117), run_time=1.8, rate_func=linear)
        self.at("more than half")
        self.play(*cl.go(S117), *ch.set(None, None, 0, 58.6), FadeOut(lb), FadeOut(lb2),
                  *[v.animate.scale(0.5).set_fill(GOLD, 0.95).set_stroke(GOLD) for v in w.vacs], run_time=1.4)
        self.at("finished storage granules")
        gl = lab("storage (zymogen) granules", P(-3.5, -1.95), 28, GOLD)
        self.play(FadeIn(gl), run_time=0.8)
        self.at("these hold the protein")
        self.play(*[Indicate(g, color=GOLD, scale_factor=1.5) for g in w.grans], run_time=1.4)
        self.at("until the cell releases")
        nt = lab("chart shows 0, 7, 37 and 117", P(-3.5, -2.6), 24, TEXT)
        nt2 = lab("minutes only", P(-3.5, -3.0), 24, TEXT)
        self.play(FadeIn(nt), FadeIn(nt2), run_time=0.8)
        self.finish()


# ================================================================ S13
class S13Order(SpokenScene):
    def construct(self):
        ambient(self)
        names = ["rough ER", "Golgi vesicles", "condensing vacuoles", "storage granules"]
        chips = [chip(n, c, size=24, pad=0.12) for n, c in zip(names, BCOL)]
        items = []
        for i, c in enumerate(chips):
            if i:
                items.append(T("→", 24, GREY))
            items.append(c)
        st = VGroup(*items).arrange(RIGHT, buff=0.14).move_to(P(0, 3.3))
        st.chips = chips
        for c in chips:
            _style(c, False)
        self.add(st)
        xs = [-4.8, -1.6, 1.6, 4.8]
        vals = [[86.3, 0, 0, 0], [43.7, 43.0, 0, 0], [0, 0, 48.5, 0], [0, 0, 0, 58.6]]
        caps = ["0 min", "7 min", "37 min", "117 min"]
        ths = [thumb(x, v) for x, v in zip(xs, vals)]
        cps = [T(c, 28, TEXT).move_to(P(x, -1.65)) for c, x in zip(caps, xs)]
        ars = [Arrow(P(x + 1.45, 0.45), P(x + 1.75, 0.45), buff=0, color=TEXT, stroke_width=4, max_tip_length_to_length_ratio=0.8)
               for x in xs[:-1]]
        self.at("each part's share")
        self.play(LaggedStart(*[AnimationGroup(FadeIn(t, shift=UP * 0.2), FadeIn(c)) for t, c in zip(ths, cps)], lag_ratio=0.5),
                  run_time=2.8)
        self.play(*[GrowArrow(a) for a in ars], run_time=0.8)
        for k, ph in enumerate(("rough ER", "then Golgi vesicles", "then condensing vacuoles", "then storage granules")):
            self.at(ph)
            self.play(*light(st, (2 * k,)), Indicate(ths[k].bars[-1], color=BCOL[k], scale_factor=1.1),
                      ths[k][0].animate.set_stroke(BCOL[k], 5), run_time=1.0)
        self.at("the chart shows only")
        nt = lab("each part's own highest share; times between not shown", P(0, -2.75), 26, TEXT)
        self.play(FadeIn(nt, shift=UP * 0.1), *[ths[i][0].animate.set_stroke(GREY, 3) for i in range(4)],
                  *light(st, ()), run_time=1.0)
        self.play(Indicate(VGroup(*cps), color=GOLD, scale_factor=1.12), run_time=1.5)
        self.finish()


# ================================================================ S14
class S14Meaning(SpokenScene):
    def construct(self):
        setw(1.0)
        w = World(self, live=True).add()
        rp, rg = route_purple(), route_gold()
        self.add(rp, rg)
        st = strip_m((0, 1, 3, 5))
        self.add(st)
        s = stamp("drawing", P(-1.0, -2.0))
        self.add(s)
        self.at("these were digestive")
        cn = lab("digestive-enzyme cells, not beta cells", P(0.2, -3.55), 28, TEXT)
        self.play(FadeIn(cn, shift=UP * 0.15), run_time=0.9)
        self.at("direct evidence")
        self.play(Indicate(rg, color=GOLD, scale_factor=1.05), run_time=1.4)
        self.at("the order of stops")
        parcel = glow_m(W(P(-0.8, 0.225)), 0.14)
        self.play(FadeIn(parcel, scale=0.6), run_time=0.4)
        for p in (P(0.4, RY), P(2.5, RY), MEM):
            self.play(parcel.animate.move_to(W(p)), run_time=0.8, rate_func=linear)
        self.play(FadeOut(parcel), run_time=0.3)
        self.at("a drawing had become")
        self.play(s.animate.shift(UP * 0.5).rotate(0.3).set_opacity(0), run_time=0.9)
        m = stamp("measured", P(-1.0, -2.0), GREEN, 40)
        m.scale(2.4).set_opacity(0)
        self.add(m)
        self.play(m.animate.scale(1 / 2.4).set_opacity(1), run_time=0.5, rate_func=rush_into)
        self.play(m.animate.shift(DOWN * 0.07), rate_func=there_and_back, run_time=0.25)
        self.finish()


# ================================================================ S15
class S15Answer(SpokenScene):
    def construct(self):
        setw(1.0)
        w = World(self, live=True).add()
        clk = full_clock(self, 0.0, "pulse: 3 min")
        self.at("mark one batch")
        gold = rain(self, "gold", (-1.9, 0.3), 8, ystops=(0.8, 0.95), speed=1.4)
        marks = VGroup(*[glow_m(W(P(*s)), 0.1) for s in ER_SL[:10]])
        self.play(LaggedStart(*[FadeIn(g, scale=0.4) for g in marks], lag_ratio=0.15), run_time=1.6)
        self.at("then watch where")
        gold.clear_updaters()
        self.play(FadeOut(gold), run_time=0.4)
        clk.txt = None
        grey = rain(self, "grey", (-3.8, 3.4), 14, ystops=(-2.0, 0.9), speed=1.3, seed=9)
        cl = Cloud(self, S0, add=False)
        self.remove(marks)
        self.add(cl.g)
        self.play(clk.m.animate.set_value(7), *cl.go(S7), run_time=2.0, rate_func=smooth)
        self.at("each stop")
        self.play(clk.m.animate.set_value(37), *cl.go(S37), run_time=1.6, rate_func=smooth)
        self.at("peaks later")
        self.play(clk.m.animate.set_value(117), *cl.go(S117), run_time=2.2, rate_func=smooth)
        self.finish()


# ================================================================ S16
class S16End(EndCard):
    LINE = "Mark one batch, follow it, and the order of stops appears."
