"""Bohr's Dog Blood: Shifting the Curve (oxygen transport, film 2 of 2).

COLOUR MAP (same as film 1): BLUE = oxygen / lung band; RED = hemoglobin, adult curve, capacity tank outline;
TEAL = one-site carriers; GREY = venous-blood band / CO2; GOLD = release bracket.
New here: ORANGE = the right-shifted curve; YELLOW = temperature; PURP = BPG.
All curves are computed: Severinghaus (P50 26.8 mmHg); the shifted curve is sev(P / K) with K = 1.193
(P50 about 32 mmHg; 96.2% at 100 mmHg, 64.6% at 40 mmHg), a model illustration.
"""
import random
import numpy as np
from bp_style import *  # noqa: F401,F403

ORANGE = "#F28C28"
PURP = "#B07CE8"
SOFT = "#C9CED8"
PANEL = "#222A3A"
K = 1.1932

# plot geometry: identical to film 1 (one world)
PX0, PY0, PW, PH = -3.7, -2.7, 9.6, 4.9
XMAX = 120.0
SX = PW / XMAX
XB = 3.0
P_LUNG, P_REST = 100.0, 40.0
PTS = [10, 20, 30, 40, 60, 80, 100]


def px(p):
    return PX0 + p * SX


def py(s):
    return PY0 + s * PH


def sev(p):
    p = np.asarray(p, float)
    return 1.0 / (23400.0 / (p ** 3 + 150.0 * p + 1e-12) + 1.0)


def sev_o(p):
    return sev(np.asarray(p, float) / K)


S_LUNG, S_REST = float(sev(P_LUNG)), float(sev(P_REST))
O_LUNG, O_REST = float(sev_o(P_LUNG)), float(sev_o(P_REST))


def curve_mob(fn, color, w=8, p_lo=0.0, p_hi=120.0):
    p_hi = max(p_hi, p_lo + 1.0)
    ps = np.linspace(p_lo, p_hi, 120)
    pts = [[px(p), py(float(fn(p))), 0] for p in ps]
    m = VMobject(stroke_color=color, stroke_width=w)
    m.set_points_smoothly(pts)
    m.set_fill(opacity=0)
    return m


def sev_curve(w=8, p_hi=120.0):
    return curve_mob(sev, RED, w, 0.0, p_hi)


def ora_curve(w=8, k=K, p_hi=120.0):
    return curve_mob(lambda p: sev(np.asarray(p, float) / k), ORANGE, w, 0.0, p_hi)


def axes_y():
    g = VGroup(Line([PX0, PY0, 0], [PX0, PY0 + PH + 0.25, 0], color=GREY, stroke_width=3))
    for s in (0, 50, 100):
        g.add(Line([PX0, py(s / 100), 0], [PX0 - 0.1, py(s / 100), 0], color=GREY, stroke_width=3))
        g.add(M(str(s), 22, GREY).move_to([PX0 - 0.48, py(s / 100), 0]))
    g.add(T("saturation (%)", 28, TEXT).rotate(PI / 2).move_to([PX0 - 1.2, py(0.5), 0]))
    return g


def axes_x():
    g = VGroup(Line([PX0, PY0, 0], [px(XMAX) + 0.1, PY0, 0], color=GREY, stroke_width=3))
    for p in range(0, 121, 20):
        g.add(Line([px(p), PY0, 0], [px(p), PY0 - 0.1, 0], color=GREY, stroke_width=3))
        g.add(M(str(p), 22, GREY).move_to([px(p), PY0 - 0.38, 0]))
    g.add(T("PO2 (mmHg)", 28, TEXT).move_to([px(60), PY0 - 0.85, 0]))
    g.add(breathing(RoundedRectangle(corner_radius=0.25, width=13.5, height=6.4, stroke_width=0, fill_color=PANEL, fill_opacity=1.0).move_to([0, -0.62, 0]).set_z_index(-5)))
    return g


def breathing(m, period=6.0):
    """The panel's ground brightens and dims very slightly, so a held frame is never a dead frame."""
    m.tb = 0.0

    def f(mm, dt):
        mm.tb += dt
        k = 0.5 + 0.5 * np.sin(2 * PI * mm.tb / period)
        mm.set_fill(interpolate_color(ManimColor(PANEL), ManimColor("#2D384D"), k), opacity=1.0)
    m.add_updater(f)
    return m


def band(p, color, op=0.22, wp=8.0):
    return Rectangle(width=wp * SX, height=PH, stroke_width=0, fill_color=color,
                     fill_opacity=op).move_to([px(p), PY0 + PH / 2, 0])


def lung_label(txt="lungs: ~100 mmHg"):
    return T(txt, 28, BLUE).move_to([px(P_LUNG), 2.75, 0])


def tis_label(txt="resting tissue: ~40 mmHg", p=P_REST):
    return T(txt, 28, TEXT).move_to([px(p), 2.75, 0])


def pdot(p, s, color, r=0.15):
    return Dot([px(p), py(s), 0], radius=r, color=color).set_z_index(5)


def red_dots(r=0.13):
    return VGroup(*[pdot(p, float(sev(p)), RED, r) for p in PTS])


def ora_dots(r=0.13):
    return VGroup(*[pdot(p, float(sev_o(p)), ORANGE, r).set_z_index(6) for p in PTS])


def legend():
    y = -3.55
    l1 = Line([-6.7, y, 0], [-6.2, y, 0], color=RED, stroke_width=8)
    t1 = T("usual blood", 28, RED).next_to(l1, RIGHT, buff=0.15)
    l2 = Line([t1.get_right()[0] + 0.4, y, 0], [t1.get_right()[0] + 0.9, y, 0], color=ORANGE, stroke_width=8)
    t2 = T("shifted right", 28, ORANGE).next_to(l2, RIGHT, buff=0.15)
    return VGroup(l1, t1, l2, t2)


def rel_bar(xb, s_hi, s_lo, p_dot=P_REST, w=7):
    """Gold release bar at xb between two saturations, with a guide from the tissue point."""
    yh, yl = py(s_hi), py(s_lo)
    return VGroup(DashedLine([px(p_dot), yl, 0], [xb, yl, 0], color=GOLD, stroke_width=3, dash_length=0.12),
                  Line([xb - 0.3, yh, 0], [xb, yh, 0], color=GOLD, stroke_width=4),
                  Line([xb, yl, 0], [xb, yh, 0], color=GOLD, stroke_width=w))


def motes(scene, n=16, seed=1):
    rng = random.Random(seed)
    g = VGroup()
    for _ in range(max(n, 26)):
        d = Dot(radius=rng.uniform(0.05, 0.1), color=rng.choice([TEAL, GREY, TEXT])).set_opacity(rng.uniform(0.28, 0.5))
        d.move_to([rng.uniform(-6.5, 6.5), rng.uniform(-3.6, 3.6), 0])
        d.v = (rng.uniform(-0.25, 0.25), rng.uniform(0.15, 0.4))

        def drift(m, dt):
            m.shift([m.v[0] * dt, m.v[1] * dt, 0])
            if m.get_y() > 3.7:
                m.shift(DOWN * 7.4)
            if abs(m.get_x()) > 6.6:
                m.shift(LEFT * 13.2 * (1 if m.get_x() > 0 else -1))
        d.add_updater(drift)
        g.add(d)
    g.set_z_index(-4)
    scene.add(g)
    return g


def hb_block(w=2.4, h=2.0, color=GREY, rounded=True, fill=0.28, slot_r=0.2):
    body = RoundedRectangle(corner_radius=0.4, width=w, height=h) if rounded else Rectangle(width=w, height=h)
    body.set_stroke(color, 4).set_fill(color, fill)
    slots = VGroup(*[Circle(radius=slot_r, stroke_color=TEXT, stroke_width=3).move_to([sx * w * 0.22, sy * h * 0.22, 0])
                     for sy in (1, -1) for sx in (-1, 1)])
    g = VGroup(body, slots)
    g.body, g.slots = body, slots
    return g


def bob(m, amp=0.08, speed=1.6, seed=0.0):
    m.base_y = m.get_y()
    m.t0 = seed

    def f(mm, dt):
        mm.t0 += dt
        mm.move_to([mm.get_x(), mm.base_y + amp * np.sin(speed * mm.t0), 0])
    m.add_updater(f)


def pulse(m, amp=0.3, speed=4.0):
    m.w0 = m.width
    m.tt = 0.0

    def f(mm, dt):
        mm.tt += dt
        mm.set_width(mm.w0 * (1 + amp * np.sin(speed * mm.tt)))
    m.add_updater(f)


def flow(path, color, n=5, speed=0.9, r=0.07):
    """Small dots travelling along a polyline."""
    pts = [np.array(p, float) for p in path]
    segs = list(zip(pts[:-1], pts[1:]))
    lens = [np.linalg.norm(b - a) for a, b in segs]
    L = sum(lens)

    def pos(s):
        s %= L
        for (a, b), l in zip(segs, lens):
            if s <= l:
                return a + (b - a) * s / l
            s -= l
        return segs[-1][1]
    g = VGroup()
    for i in range(n):
        d = Dot(radius=r, color=color).set_z_index(4)
        d.s = i * L / n
        d.move_to(pos(d.s))

        def f(m, dt):
            m.s += speed * dt
            m.move_to(pos(m.s))
        d.add_updater(f)
        g.add(d)
    return g


def polyline(path, color, w=4):
    g = VGroup()
    for a, b in zip(path[:-1], path[1:]):
        g.add(Line(a, b, color=color, stroke_width=w))
    return g


def flask(w=1.5, h=2.0, liquid=RED, op=0.55):
    pts = [(-0.18 * w, h / 2), (0.18 * w, h / 2), (0.18 * w, 0.15 * h), (0.5 * w, -h / 2), (-0.5 * w, -h / 2), (-0.18 * w, 0.15 * h)]
    outline = Polygon(*[[x, y, 0] for x, y in pts], stroke_color=TEXT, stroke_width=4, fill_opacity=0)
    yl = -0.2 * h
    hw = lambda y: 0.18 * w + 0.32 * w * (0.15 * h - y) / (0.65 * h)
    liq = Polygon([-0.5 * w, -h / 2, 0], [0.5 * w, -h / 2, 0], [hw(yl), yl, 0], [-hw(yl), yl, 0],
                  stroke_width=0, fill_color=liquid, fill_opacity=op)
    g = VGroup(liq, outline)
    return g


def rock(m, amp=0.07, speed=1.6):
    m.tt = 0.0
    m.prev = 0.0
    m.c0 = m.get_center()

    def f(mm, dt):
        mm.tt += dt
        a = amp * np.sin(speed * mm.tt)
        mm.rotate(a - mm.prev, about_point=mm.c0)
        mm.prev = a
    m.add_updater(f)


def gauge(cx, cy, tr, vmax, color, label, r=0.55, label_dy=-0.85):
    ring = Circle(radius=r, stroke_color=color, stroke_width=5, fill_color=color, fill_opacity=0.14).move_to([cx, cy, 0])
    ang = lambda: PI * 0.9 - 1.8 * PI * tr.get_value() / vmax
    ptr = always_redraw(lambda: Line([cx, cy, 0], [cx + 0.45 * np.cos(ang()), cy + 0.45 * np.sin(ang()), 0],
                                     color=color, stroke_width=7))
    lab = T(label, 28, color).move_to([cx, cy + label_dy, 0])
    return ring, ptr, lab


# muscle + vessel (s01 and s13 share these)
MX, MY, MW, MH = -3.9, 1.8, 5.4, 3.0
VY, VH = -1.9, 1.3


def muscle():
    body = RoundedRectangle(corner_radius=0.5, width=MW, height=MH, stroke_color="#E8967A", stroke_width=5,
                            fill_color="#C0604A", fill_opacity=0.2).move_to([MX, MY, 0])
    fibres = VGroup(*[RoundedRectangle(corner_radius=0.16, width=MW - 0.7, height=0.3, stroke_width=0,
                                       fill_color="#E8967A", fill_opacity=0.35).move_to([MX, MY - 1.2 + 0.6 * i, 0])
                      for i in range(5)])
    return VGroup(body, fibres)


def vessel(scene):
    v = Rectangle(width=13.2, height=VH, stroke_color=RED, stroke_width=5, fill_color=RED, fill_opacity=0.3).move_to([0, VY, 0])
    scene_cells = VGroup()
    rng = random.Random(3)
    for i in range(11):
        c = Ellipse(width=0.6, height=0.36, color="#FFB3AA", stroke_width=0, fill_opacity=0.6)
        c.move_to([-6.2 + i * 1.2, VY + rng.uniform(-0.3, 0.3), 0])

        def f(m, dt):
            m.shift(RIGHT * 1.0 * dt)
            if m.get_x() > 6.4:
                m.shift(LEFT * 12.8)
        c.add_updater(f)
        scene_cells.add(c)
    return v, scene_cells


def co2_bubble():
    b = VGroup(Circle(radius=0.3, stroke_color=GREY, stroke_width=3, fill_color=GREY, fill_opacity=0.3), T("CO2", 22, TEXT))
    return b


def falling_bubbles(n, seed):
    rng = random.Random(seed)
    g = VGroup()
    ytop, ybot = 0.9, VY - 0.1
    for i in range(n):
        b = co2_bubble().move_to([rng.uniform(-5.7, -2.1), ytop - (ytop - ybot) * i / n, 0])
        b.v = rng.uniform(0.5, 0.7)

        def f(m, dt):
            m.shift(DOWN * m.v * dt)
            if m.get_y() < ybot:
                m.move_to([rng.uniform(-5.7, -2.1), ytop, 0])
        b.add_updater(f)
        g.add(b)
    return g


def jitter_bubbles(n, seed):
    rng = random.Random(seed)
    g = VGroup()
    for i in range(n):
        b = co2_bubble().scale(0.75).move_to([rng.uniform(-6.0, -1.8), rng.uniform(0.7, 2.9), 0])
        b.v = [rng.uniform(-0.35, 0.35), rng.uniform(-0.35, 0.35)]

        def f(m, dt):
            m.shift([m.v[0] * dt, m.v[1] * dt, 0])
            if m.get_x() < -6.1 or m.get_x() > -1.7:
                m.v[0] = -m.v[0]
            if m.get_y() < 0.6 or m.get_y() > 3.0:
                m.v[1] = -m.v[1]
        b.add_updater(f)
        g.add(b)
    return g


def o2_stream(n, seed):
    rng = random.Random(seed)
    g = VGroup()
    for i in range(n):
        d = Dot(radius=0.12, color=BLUE).set_z_index(6)
        d.move_to([rng.uniform(-5.8, -2.0), -1.4 + 4.3 * i / n, 0])
        d.xv = rng.uniform(-0.1, 0.1)

        def f(m, dt):
            m.shift([m.xv * dt, 0.8 * dt, 0])
            if m.get_y() > 2.9:
                m.move_to([rng.uniform(-5.8, -2.0), -1.4, 0])
        d.add_updater(f)
        g.add(d)
    return g


# inset plot (s13, s14)
IX0, IW, IY0, IH = 1.5, 4.6, -0.2, 3.2


def ipx(p):
    return IX0 + p / 120.0 * IW


def ipy(s):
    return IY0 + s * IH


def inset():
    ax = VGroup(Line([IX0, IY0, 0], [IX0, IY0 + IH + 0.15, 0], color=GREY, stroke_width=3),
                Line([IX0, IY0, 0], [IX0 + IW + 0.1, IY0, 0], color=GREY, stroke_width=3),
                T("saturation", 22, TEXT).rotate(PI / 2).move_to([IX0 - 0.35, IY0 + IH / 2, 0]),
                T("PO2", 22, TEXT).move_to([IX0 + IW / 2, IY0 - 0.32, 0]))
    bw = 8.0 * IW / 120.0
    bands = VGroup(Rectangle(width=bw, height=IH, stroke_width=0, fill_color=BLUE, fill_opacity=0.22).move_to([ipx(100), IY0 + IH / 2, 0]),
                   Rectangle(width=bw, height=IH, stroke_width=0, fill_color=GREY, fill_opacity=0.4).move_to([ipx(20), IY0 + IH / 2, 0]))
    ps = np.linspace(0, 120, 100)
    cr = VMobject(stroke_color=RED, stroke_width=4).set_fill(opacity=0)
    cr.set_points_smoothly([[ipx(p), ipy(float(sev(p))), 0] for p in ps]).set_stroke(opacity=0.6)
    co = VMobject(stroke_color=ORANGE, stroke_width=7).set_fill(opacity=0)
    co.set_points_smoothly([[ipx(p), ipy(float(sev_o(p))), 0] for p in ps])
    sh, sl = float(sev_o(100)), float(sev_o(20))
    xb = 3.2
    br = VGroup(DashedLine([ipx(100), ipy(sh), 0], [xb, ipy(sh), 0], color=GOLD, stroke_width=3, dash_length=0.1),
                DashedLine([ipx(20), ipy(sl), 0], [xb, ipy(sl), 0], color=GOLD, stroke_width=3, dash_length=0.1),
                Line([xb, ipy(sl), 0], [xb, ipy(sh), 0], color=GOLD, stroke_width=7))
    lab = T("bigger release", 26, GOLD).move_to([4.85, 0.85, 0])
    ax.add(breathing(Rectangle(width=6.3, height=4.4, stroke_width=0, fill_color=PANEL, fill_opacity=1.0).move_to([3.65, 1.3, 0]).set_z_index(-5)))
    return ax, bands, cr, co, br, lab


# ---------------------------------------------------------------------------------------------
class S00Title(TitleCard):
    LESSON = "Carrying Oxygen and Carbon Dioxide"
    TITLE = "Bohr's Dog Blood: Shifting the Curve"


# ---------------------------------------------------------------------------------------------
class S01Hook(SpokenScene):
    def construct(self):
        motes(self, 12, 31)
        mus = muscle()
        ml = T("working muscle", 30, TEXT).move_to([MX, 3.62, 0])
        v, cells = vessel(self)
        vl = T("blood vessel", 28, RED).move_to([-4.6, -3.2, 0])
        self.play(FadeIn(mus), FadeIn(ml), Create(v), FadeIn(cells), FadeIn(vl), run_time=1.2)
        self.at("pours out")
        bub = falling_bubbles(7, 5)
        self.play(FadeIn(bub), run_time=0.8)
        self.at("does that change")
        a1 = Arrow([-1.05, 2.4, 0], [0.45, 2.75, 0], color=ORANGE, stroke_width=5, buff=0)
        l1 = T("changes oxygen binding?", 30, ORANGE).move_to([3.5, 2.75, 0])
        self.play(Create(a1), FadeIn(l1, shift=RIGHT * 0.2), run_time=1.0)
        self.play(Indicate(l1, color=ORANGE, scale_factor=1.08), run_time=1.0)
        self.at("or does carbon dioxide")
        a2 = Arrow([-1.05, 1.2, 0], [0.45, 0.85, 0], color=SOFT, stroke_width=5, buff=0)
        l2 = T("just rides along?", 30, SOFT).move_to([2.6, 0.85, 0])
        self.play(Create(a2), FadeIn(l2, shift=RIGHT * 0.2), run_time=1.0)
        self.play(Indicate(l2, color=SOFT, scale_factor=1.08), run_time=1.0)
        self.finish()


# ---------------------------------------------------------------------------------------------
class S02Link(SpokenScene):
    def construct(self):
        motes(self, 12, 32)
        ay, ax = axes_y(), axes_x()
        self.play(Create(ay[0]), Create(ax[0]), FadeIn(VGroup(*ay[1:])), FadeIn(VGroup(*ax[1:])), run_time=0.8)
        rc = sev_curve()
        self.play(Create(rc), run_time=1.3)
        self.at("delivering its drop")
        lb, rb = band(P_LUNG, BLUE, 0.22), band(P_REST, GREY, 0.35)
        ll, rl = lung_label(), tis_label()
        ld, td = pdot(P_LUNG, S_LUNG, BLUE), pdot(P_REST, S_REST, SOFT)
        self.play(GrowFromEdge(lb, DOWN), GrowFromEdge(rb, DOWN), FadeIn(ll), FadeIn(rl), run_time=1.2)
        self.play(FadeIn(ld, scale=2), FadeIn(td, scale=2), run_time=0.8)
        self.at("from lung to tissue")
        br = VGroup(DashedLine([px(P_LUNG), py(S_LUNG), 0], [XB, py(S_LUNG), 0], color=GOLD, stroke_width=3, dash_length=0.12),
                    DashedLine([px(P_REST), py(S_REST), 0], [XB, py(S_REST), 0], color=GOLD, stroke_width=3, dash_length=0.12),
                    Line([XB, py(S_REST), 0], [XB, py(S_LUNG), 0], color=GOLD, stroke_width=7))
        self.play(Create(br), run_time=1.5)
        self.at("now ask")
        q = T("?", 64, GOLD, weight=BOLD).move_to([3.55, 1.45, 0])
        self.play(FadeIn(q, scale=0.4), run_time=0.7)
        bob(q, 0.1, 2.0)
        self.at("where tissue is working")
        self.play(Indicate(br[2], color=GOLD, scale_factor=1.08), run_time=1.2)
        self.finish()


# ---------------------------------------------------------------------------------------------
class S03Setup(SpokenScene):
    def construct(self):
        motes(self, 12, 33)
        self.at("in copenhagen")
        cap = T("Copenhagen, 1903", 44, TEXT, font=TITLE_FONT).move_to([0, 3.15, 0])
        self.play(FadeIn(cap, shift=DOWN * 0.15), run_time=0.9)
        names = ["Christian Bohr", "Karl Hasselbalch", "August Krogh"]
        xs = [-4.4, 0.0, 4.4]
        cards = []
        for nm, x in zip(names, xs):
            c = chip(nm, GOLD, 32, pad=0.3, fill_opacity=0.14).move_to([x, 1.6, 0])
            cards.append(c)
        self.at("christian")
        self.play(FadeIn(cards[0], shift=UP * 0.2), run_time=0.7)
        self.at("hasselbalch")
        self.play(FadeIn(cards[1], shift=UP * 0.2), run_time=0.7)
        self.at("august")
        self.play(FadeIn(cards[2], shift=UP * 0.2), run_time=0.7)
        self.at("they took")
        fl = flask(3.2, 3.8, RED, 0.6).move_to([-1.5, -1.5, 0])
        fl_l = T("fresh dog blood", 40, RED).move_to([3.3, -1.5, 0])
        self.play(FadeIn(fl, shift=UP * 0.3), run_time=0.9)
        rock(fl, 0.05, 1.3)
        self.play(FadeIn(fl_l, shift=LEFT * 0.2), run_time=0.7)
        self.finish()


# ---------------------------------------------------------------------------------------------
FL = [-2.6, 1.2, 0]


def apparatus(po, with_co2=False, co=None):
    fl = flask(1.5, 2.0, RED, 0.55).move_to(FL)
    g1 = gauge(-5.6, 3.0, po, 120.0, BLUE, "PO2 set")
    path1 = [[-5.05, 3.0, 0], [-2.75, 3.0, 0], [-2.75, 2.2, 0]]
    ln1 = polyline(path1, BLUE)
    fd1 = flow(path1, BLUE, 6, 0.9)
    parts = [fl, g1[0], g1[1], g1[2], ln1, fd1]
    extra = []
    if with_co2:
        g2 = gauge(0.6, 3.0, co, 1.0, SOFT, "CO2")
        path2 = [[0.05, 3.0, 0], [-2.45, 3.0, 0], [-2.45, 2.2, 0]]
        ln2 = polyline(path2, SOFT)
        fd2 = flow(path2, SOFT, 6, 0.9)
        extra = [g2[0], g2[1], g2[2], ln2, fd2]
    return fl, parts, extra


class S04Method(SpokenScene):
    def construct(self):
        motes(self, 12, 34)
        po = ValueTracker(10.0)
        fl, parts, _ = apparatus(po)
        self.play(*[FadeIn(p) for p in parts], run_time=1.0)
        rock(fl)
        ay, ax = axes_y(), axes_x()
        self.play(Create(ay[0]), Create(ax[0]), FadeIn(VGroup(*ay[1:])), FadeIn(VGroup(*ax[1:])), run_time=1.0)
        self.at("measured")
        d0 = Dot(FL, radius=0.13, color=RED).set_z_index(6)
        self.add(d0)
        self.play(d0.animate.move_to([px(10), py(float(sev(10))), 0]), run_time=1.0)
        self.at("repeating")
        ds = []
        for p in PTS[1:]:
            ds.append(Dot(FL, radius=0.13, color=RED).set_z_index(6))
        self.add(*ds)
        anims = [d.animate.move_to([px(p), py(float(sev(p))), 0]) for d, p in zip(ds, PTS[1:])]
        self.play(LaggedStart(*anims, lag_ratio=0.35), po.animate.set_value(100.0), run_time=2.0, rate_func=linear)
        self.at("traces the curve")
        rc = sev_curve()
        self.play(Create(rc), run_time=1.2)
        self.finish()


class S05Logic(SpokenScene):
    def construct(self):
        motes(self, 12, 35)
        po = ValueTracker(100.0)
        co = ValueTracker(0.08)
        fl, parts, extra = apparatus(po, True, co)
        self.add(axes_y(), axes_x(), sev_curve())
        dots = red_dots()
        self.add(dots, *parts)
        rock(fl)
        self.at("raised the carbon")
        self.play(*[FadeIn(e) for e in extra], run_time=0.9)
        self.play(co.animate.set_value(0.92), run_time=2.4)
        self.at("same oxygen pressures")
        rings = VGroup(*[DashedVMobject(Circle(radius=0.24, stroke_color=TEXT, stroke_width=3).move_to(d.get_center()), num_dashes=12)
                         for d in dots])
        self.play(LaggedStart(*[Create(r) for r in rings], lag_ratio=0.2, run_time=1.6))
        self.at("simply rode along")
        lab = T("rides along: no change", 30, SOFT).move_to([1.9, -1.3, 0])
        self.play(FadeIn(lab, shift=UP * 0.1), run_time=0.7)
        self.at("nothing should change")
        self.play(Indicate(rings, color=TEXT, scale_factor=1.15), run_time=1.2)
        self.at("only carbon dioxide")
        lab2 = T("only CO2 changed", 30, SOFT).move_to([1.9, -1.3, 0])
        self.play(ReplacementTransform(lab, lab2), Indicate(extra[0], color=SOFT, scale_factor=1.25), run_time=1.2)
        self.at("any difference")
        lab3 = T("difference: CO2 or its acid", 30, ORANGE).move_to([1.9, -1.3, 0])
        self.play(ReplacementTransform(lab2, lab3), run_time=0.8)
        self.play(Indicate(lab3, color=ORANGE, scale_factor=1.06), run_time=1.2)
        self.finish()


# ---------------------------------------------------------------------------------------------
def spots_scene(self, animate):
    motes(self, 12, 36 if animate else 37)
    self.add(axes_y(), axes_x(), sev_curve(), red_dots())
    q = T("Where will it show most?", 36, GOLD).move_to([0, 3.3, 0])
    r1 = Circle(radius=0.36, stroke_color=GOLD, stroke_width=6).move_to([px(20), py(float(sev(20))), 0]).set_z_index(7)
    r2 = Circle(radius=0.36, stroke_color=GOLD, stroke_width=6).move_to([px(100), py(float(sev(100))), 0]).set_z_index(7)
    t1 = T("low PO2", 30, GOLD).move_to([-0.1, -1.55, 0])
    t2 = T("near full", 30, GOLD).move_to([4.3, 1.3, 0])
    return q, r1, r2, t1, t2


class S06Predict(SpokenScene):
    def construct(self):
        motes(self, 12, 36)
        po = ValueTracker(100.0)
        co = ValueTracker(0.92)
        fl, parts, extra = apparatus(po, True, co)
        self.add(axes_y(), axes_x(), sev_curve(), red_dots(), *parts, *extra)
        app = VGroup(*parts, *extra)
        q = T("Where will it show most?", 36, GOLD).move_to([0, 3.3, 0])
        r1 = Circle(radius=0.36, stroke_color=GOLD, stroke_width=6).move_to([px(20), py(float(sev(20))), 0]).set_z_index(7)
        r2 = Circle(radius=0.36, stroke_color=GOLD, stroke_width=6).move_to([px(100), py(float(sev(100))), 0]).set_z_index(7)
        t1 = T("low PO2", 30, GOLD).move_to([-0.1, -1.55, 0])
        t2 = T("near full", 30, GOLD).move_to([4.3, 1.3, 0])
        self.play(FadeOut(app), FadeIn(q, shift=DOWN * 0.1), run_time=0.9)
        self.remove(app)
        self.at("where will it show")
        self.play(Indicate(q, color=GOLD, scale_factor=1.2), run_time=1.0)
        rc2 = sev_curve().set_color(GOLD)
        self.play(ShowPassingFlash(rc2, time_width=0.45, run_time=1.6))
        self.at("at a low")
        self.play(FadeIn(r1, scale=2), FadeIn(t1), run_time=0.7)
        pulse(r1)
        self.at("near full")
        self.play(FadeIn(r2, scale=2), FadeIn(t2), run_time=0.7)
        pulse(r2)
        self.finish()


class S07Pause(NarratedScene):
    def construct(self):
        self.add(axes_y(), axes_x(), sev_curve(), red_dots())
        q = T("Where will it show most?", 36, GOLD).move_to([0, 3.3, 0])
        r1 = Circle(radius=0.36, stroke_color=GOLD, stroke_width=6).move_to([px(20), py(float(sev(20))), 0]).set_z_index(7)
        r2 = Circle(radius=0.36, stroke_color=GOLD, stroke_width=6).move_to([px(100), py(float(sev(100))), 0]).set_z_index(7)
        t1 = T("low PO2", 30, GOLD).move_to([-0.1, -1.55, 0])
        t2 = T("near full", 30, GOLD).move_to([4.3, 1.3, 0])
        self.add(q, r1, r2, t1, t2)
        pulse(r1)
        pulse(r2)
        tr = ValueTracker(1.0)
        track = Rectangle(width=8.0, height=0.2, stroke_color=GREY, stroke_width=3).move_to([0, 2.8, 0])
        bar = always_redraw(lambda: Rectangle(width=max(8.0 * tr.get_value(), 0.01), height=0.2, stroke_width=0, fill_color=GOLD,
                                              fill_opacity=0.9).move_to([-4.0 + 4.0 * tr.get_value(), 2.8, 0]))
        self.add(track, bar)
        self.play(tr.animate.set_value(0.0), run_time=4.6, rate_func=linear)
        self.finish()


# ---------------------------------------------------------------------------------------------
class S08Reveal(SpokenScene):
    def construct(self):
        motes(self, 12, 38)
        self.add(axes_y(), axes_x(), sev_curve(), red_dots())
        self.at("more carbon dioxide")
        od = ora_dots()
        for d, p in zip(od, PTS):
            d.move_to([px(p), py(float(sev(p))), 0])
        self.play(FadeIn(od, scale=2), run_time=0.6)
        self.play(LaggedStart(*[d.animate.move_to([px(p), py(float(sev_o(p))), 0]) for d, p in zip(od, PTS)],
                              lag_ratio=0.12, run_time=1.8))
        gaps = [Line([px(p), py(float(sev(p))), 0], [px(p), py(float(sev_o(p))), 0], color=TEXT, stroke_width=7).set_z_index(4)
                for p in PTS]
        self.at("the effect was large")
        ga = VGroup(*gaps[:4])
        la = T("large gap", 32, TEXT).move_to([-0.2, -1.25, 0])
        self.play(Create(ga), FadeIn(la), run_time=1.2)
        self.play(Indicate(ga, color=TEXT, scale_factor=1.2), run_time=0.9)
        self.at("small near full")
        gb = VGroup(*gaps[4:])
        lb = T("small gap", 32, TEXT).move_to([4.3, 1.3, 0])
        self.play(Create(gb), FadeIn(lb), run_time=1.0)
        self.play(Indicate(gb, color=TEXT, scale_factor=1.6), run_time=0.9)
        self.at("the curve had moved")
        oc = ora_curve()
        lg = legend()
        self.play(FadeOut(la), FadeOut(lb), Create(oc), FadeIn(lg), run_time=2.0)
        self.finish()


# ---------------------------------------------------------------------------------------------
def two_curves(self, legend_on=True):
    self.add(axes_y(), axes_x(), sev_curve(), ora_curve())
    if legend_on:
        self.add(legend())


class S09Name(SpokenScene):
    def construct(self):
        motes(self, 12, 39)
        two_curves(self)
        self.at("called the")
        ti = T("Bohr effect", 50, ORANGE, font=TITLE_FONT).move_to([0, 3.3, 0])
        self.play(FadeIn(ti, shift=DOWN * 0.15), run_time=0.8)
        self.at("a fall in oxygen")
        su = T("lower oxygen affinity", 32, TEXT).move_to([0, 2.7, 0])
        self.play(FadeIn(su, shift=UP * 0.1), run_time=0.7)
        gy = -1.7
        ph, cc = ValueTracker(0.8), ValueTracker(0.2)
        xs = (1.6, 4.0)

        def bar(x, tr, color):
            return always_redraw(lambda: Rectangle(width=0.5, height=max(tr.get_value(), 0.02) * 1.7, stroke_width=0, fill_color=color,
                                                   fill_opacity=0.85).move_to([x, gy + max(tr.get_value(), 0.02) * 0.85, 0]))
        tr1 = Rectangle(width=0.5, height=1.7, stroke_color=SOFT, stroke_width=3).move_to([xs[0], gy + 0.85, 0])
        tr2 = Rectangle(width=0.5, height=1.7, stroke_color=SOFT, stroke_width=3).move_to([xs[1], gy + 0.85, 0])
        self.at("when ph falls")
        l1 = T("pH falls", 30, YELLOW).move_to([xs[0], -2.2, 0])
        a1 = Arrow([xs[0], 0.15, 0], [xs[0], 1.15, 0], color=ORANGE, stroke_width=6, buff=0)
        self.play(FadeIn(tr1), FadeIn(bar(xs[0], ph, YELLOW)), FadeIn(l1), Create(a1), ph.animate.set_value(0.2), run_time=1.0)
        self.at("or carbon dioxide rises")
        l2 = T("CO2 rises", 30, SOFT).move_to([xs[1], -2.2, 0])
        a2 = Arrow([xs[1], 0.15, 0], [xs[1], 1.65, 0], color=ORANGE, stroke_width=6, buff=0)
        self.play(FadeIn(tr2), FadeIn(bar(xs[1], cc, SOFT)), FadeIn(l2), Create(a2), cc.animate.set_value(0.9), run_time=1.2)
        self.finish()


class S10P50(SpokenScene):
    def construct(self):
        motes(self, 12, 40)
        two_curves(self)
        y5 = py(0.5)
        lvl = ValueTracker(0.03)
        hl = always_redraw(lambda: DashedLine([PX0, py(lvl.get_value()), 0], [px(32.0), py(lvl.get_value()), 0],
                                              color=TEXT, stroke_width=3, dash_length=0.14))
        self.at("the shift raises")
        self.add(hl)
        self.play(lvl.animate.set_value(0.5), run_time=1.6)
        self.at("the oxygen pressure")
        rd = pdot(26.8, 0.5, RED)
        rline = DashedLine([px(26.8), y5, 0], [px(26.8), PY0, 0], color=RED, stroke_width=3, dash_length=0.12)
        rl = M("26.8", 24, RED).move_to([px(26.8) - 0.52, -2.35, 0])
        self.play(FadeIn(rd, scale=2), Create(rline), FadeIn(rl), run_time=1.0)
        self.at("hemoglobin is half")
        blk = hb_block(1.6, 1.2, RED, fill=0.3, slot_r=0.15).move_to([-2.6, 1.7, 0])
        hf = T("half full", 28, TEXT).move_to([-2.6, 0.85, 0])
        self.play(FadeIn(blk, scale=0.8), FadeIn(hf), run_time=0.7)
        dts = VGroup(*[Dot(blk.slots[i].get_center(), radius=0.15, color=BLUE).set_z_index(6) for i in (0, 3)])
        self.play(LaggedStart(*[GrowFromCenter(d) for d in dts], lag_ratio=0.5), run_time=1.0)
        self.play(Indicate(rd, color=RED, scale_factor=2.0), run_time=1.0)
        self.at("a higher")
        od = pdot(32.0, 0.5, ORANGE).set_z_index(6)
        oline = DashedLine([px(32.0), y5, 0], [px(32.0), -2.45, 0], color=ORANGE, stroke_width=3, dash_length=0.12)
        ol = M("32", 24, ORANGE).move_to([px(32.0) + 0.4, -2.35, 0])
        self.play(FadeOut(VGroup(blk, hf, dts)), FadeIn(od, scale=2), Create(oline), FadeIn(ol), run_time=1.0)
        self.at("looser grip")
        lg = T("P50 rises: looser grip", 32, ORANGE).move_to([2.7, -0.9, 0])
        self.play(FadeIn(lg, shift=UP * 0.1), run_time=0.8)
        self.play(Indicate(lg, color=ORANGE, scale_factor=1.06), run_time=1.0)
        self.finish()


# ---------------------------------------------------------------------------------------------
class S11Lungs(SpokenScene):
    def construct(self):
        motes(self, 12, 41)
        two_curves(self)
        self.at("bring back")
        lb, rb = band(P_LUNG, BLUE, 0.22), band(P_REST, GREY, 0.35)
        ll, rl = lung_label(), tis_label()
        self.play(GrowFromEdge(lb, DOWN), GrowFromEdge(rb, DOWN), FadeIn(ll), FadeIn(rl), run_time=1.5)
        self.at("in the lungs")
        rd, od = pdot(P_LUNG, S_LUNG, RED, 0.12), pdot(P_LUNG, O_LUNG, ORANGE, 0.12).set_z_index(6)
        la = M("97.7%", 28, RED).move_to([3.2, 1.45, 0])
        lo = M("96.2%", 28, ORANGE).move_to([5.3, 1.45, 0])
        self.play(FadeIn(rd, scale=2), FadeIn(od, scale=2), run_time=0.8)
        self.play(FadeIn(la), FadeIn(lo), run_time=0.8)
        self.at("still nearly full")
        self.play(Indicate(od, color=ORANGE, scale_factor=2.2), run_time=1.0)
        self.at("loading barely")
        sm = T("whole curve shifted, model illustration", 24, TEXT).move_to([1.5, -2.3, 0])
        self.play(FadeIn(sm), run_time=0.7)
        self.play(Indicate(VGroup(rd, od), color=BLUE, scale_factor=1.8), run_time=1.0)
        self.finish()


class S12Tissue(SpokenScene):
    def construct(self):
        motes(self, 12, 42)
        two_curves(self)
        self.add(band(P_LUNG, BLUE, 0.22), band(P_REST, GREY, 0.35), lung_label(), tis_label(),
                 pdot(P_LUNG, S_LUNG, RED, 0.12), pdot(P_LUNG, O_LUNG, ORANGE, 0.12).set_z_index(6))
        sm = T("whole curve shifted, model illustration", 24, TEXT).move_to([1.5, -2.3, 0])
        self.add(sm)
        self.at("at tissue")
        rd, od = pdot(P_REST, S_REST, RED, 0.14), pdot(P_REST, O_REST, ORANGE, 0.14).set_z_index(6)
        la = M("74.9%", 28, RED).move_to([-1.9, 1.3, 0])
        lo = M("64.6%", 28, ORANGE).move_to([0.2, -0.2, 0])
        self.play(FadeIn(rd, scale=2), FadeIn(la), run_time=0.8)
        self.play(FadeIn(od, scale=2), FadeIn(lo), run_time=0.8)
        self.at("sits lower")
        gap = Line(rd.get_center(), od.get_center(), color=TEXT, stroke_width=7).set_z_index(4)
        self.play(Create(gap), Indicate(od, color=ORANGE, scale_factor=2.0), run_time=1.2)
        self.at("so the release bracket")
        b1 = rel_bar(2.4, S_LUNG, S_REST)
        b2 = rel_bar(3.4, O_LUNG, O_REST)
        self.play(Create(b1), run_time=1.0)
        self.play(Create(b2), run_time=1.0)
        self.at("by about two")
        r1 = M("4.6 mL per dL", 28, RED).move_to([2.2, -0.95, 0])
        r2 = M("6.4 mL per dL", 28, ORANGE).move_to([2.2, -1.6, 0])
        self.play(FadeOut(sm), FadeIn(r1, shift=UP * 0.1), run_time=0.6)
        self.play(FadeIn(r2, shift=UP * 0.1), run_time=0.6)
        self.at("at rest in this")
        nt = T("released from hemoglobin, model illustration", 24, TEXT).move_to([1.5, -2.3, 0])
        self.play(FadeIn(nt), Indicate(b2[2], color=GOLD, scale_factor=1.15), run_time=1.0)
        self.finish()


# ---------------------------------------------------------------------------------------------
class S13Where(SpokenScene):
    def construct(self):
        motes(self, 12, 43)
        mus = muscle()
        ml = T("working muscle", 30, TEXT).move_to([MX, 3.62, 0])
        v, cells = vessel(self)
        self.at("and that happens")
        self.play(FadeIn(mus), FadeIn(ml), Create(v), FadeIn(cells), run_time=1.3)
        self.at("working tissue is")
        bub = jitter_bubbles(12, 7)
        self.play(FadeIn(bub, lag_ratio=0.1), run_time=1.6)
        self.at("low in oxygen")
        lab = T("high CO2, low PO2", 30, SOFT).move_to([MX, 3.62, 0])
        self.play(Transform(ml, lab), run_time=0.8)
        self.at("so blood gives")
        ax, bands, cr, co, br, bl = inset()
        self.play(FadeIn(ax), FadeIn(bands), Create(cr), run_time=0.8)
        st = o2_stream(8, 9)
        self.add(st)
        self.play(Create(co), run_time=1.0)
        self.play(Create(br), FadeIn(bl), run_time=0.9)
        self.finish()


class S14Paper(SpokenScene):
    def construct(self):
        motes(self, 12, 44)
        mus = muscle()
        v, cells = vessel(self)
        ax, bands, cr, co, br, bl = inset()
        self.add(mus, v, cells, ax, bands, cr, co, br, bl, jitter_bubbles(12, 7), o2_stream(8, 9))
        card = RoundedRectangle(corner_radius=0.2, width=5.6, height=3.8, stroke_color=GOLD, stroke_width=4,
                                fill_color="#EDE6D3", fill_opacity=1.0).move_to([-3.9, 1.65, 0]).set_z_index(20)
        yr = T("1904", 56, BG, font=TITLE_FONT, weight=BOLD).move_to([-3.9, 3.0, 0]).set_z_index(21)
        sub = T("the published paper", 26, "#5B5648").move_to([-3.9, 2.35, 0]).set_z_index(21)
        grp = VGroup(card, yr, sub)
        grp.shift(LEFT * 8)
        self.add(grp)
        self.at("published in")
        self.play(grp.animate.shift(RIGHT * 8), run_time=1.3)
        self.at("a reason")
        ph1 = T("gives up oxygen more", 32, BG, font=TITLE_FONT).move_to([-3.9, 1.45, 0]).set_z_index(22)
        ph2 = T("readily in active tissue", 32, BG, font=TITLE_FONT).move_to([-3.9, 0.9, 0]).set_z_index(22)
        self.play(FadeIn(VGroup(ph1, ph2), shift=UP * 0.1), run_time=0.9)
        self.at("more readily")
        hi = Rectangle(width=4.9, height=1.2, stroke_width=0, fill_color=GOLD, fill_opacity=0.5).move_to([-3.9, 1.17, 0]).set_z_index(21)
        self.play(FadeIn(hi), run_time=0.8)
        self.play(Indicate(VGroup(ph1, ph2), color=BG, scale_factor=1.04), run_time=1.0)
        self.finish()


# ---------------------------------------------------------------------------------------------
def thermometer(x, y, tr, h=1.9):
    tube = RoundedRectangle(corner_radius=0.18, width=0.36, height=h, stroke_color=YELLOW, stroke_width=4).move_to([x, y, 0])
    bulb = Circle(radius=0.3, stroke_color=YELLOW, stroke_width=4, fill_color=YELLOW, fill_opacity=0.9).move_to([x, y - h / 2 - 0.1, 0])
    mer = always_redraw(lambda: Rectangle(width=0.18, height=max(tr.get_value(), 0.05) * (h - 0.3), stroke_width=0,
                                          fill_color=YELLOW, fill_opacity=0.95).move_to(
        [x, y - h / 2 + 0.15 + max(tr.get_value(), 0.05) * (h - 0.3) / 2, 0]))
    return VGroup(tube, bulb), mer


class S15Others(SpokenScene):
    def construct(self):
        motes(self, 12, 45)
        kt = ValueTracker(K)
        self.add(axes_y(), axes_x(), sev_curve())
        oc = always_redraw(lambda: ora_curve(8, kt.get_value()))
        arrow = always_redraw(lambda: Arrow([-3.3, 1.7, 0], [-3.3 + 6.0 * (kt.get_value() - 1.0), 1.7, 0], color=ORANGE,
                                            stroke_width=8, buff=0, max_tip_length_to_length_ratio=0.4))
        lg = legend()
        self.add(oc, lg)
        self.at("also shift")
        sl = T("shift right", 30, ORANGE).move_to([-2.2, 2.35, 0])
        self.play(FadeIn(arrow), FadeIn(sl), run_time=1.0)
        self.play(Indicate(oc, color=ORANGE, scale_factor=1.02), run_time=1.0)
        self.at("warmer tissue")
        c1 = RoundedRectangle(corner_radius=0.2, width=5.8, height=3.0, stroke_color=YELLOW, stroke_width=4,
                              fill_color=YELLOW, fill_opacity=0.08).move_to([3.7, -1.0, 0])
        tt = ValueTracker(0.25)
        th, mer = thermometer(1.9, -0.85, tt)
        tl = T("higher temperature", 28, YELLOW).move_to([4.5, -1.0, 0])
        card1 = VGroup(c1, th, tl)
        card1.shift(RIGHT * 7)
        mer.shift(RIGHT * 0)
        self.add(card1)
        self.play(card1.animate.shift(LEFT * 7), run_time=1.0)
        self.add(mer)
        self.play(tt.animate.set_value(0.6), kt.animate.set_value(1.29), run_time=2.0)
        self.at("working muscle is warmer")
        self.play(tt.animate.set_value(0.9), run_time=1.8)
        self.at("so does more")
        c2 = RoundedRectangle(corner_radius=0.2, width=5.8, height=3.0, stroke_color=PURP, stroke_width=4,
                              fill_color=PURP, fill_opacity=0.08).move_to([3.7, -1.0, 0])
        cell = Ellipse(width=5.0, height=1.9, color=RED, stroke_width=5, fill_opacity=0.14).move_to([3.7, -0.5, 0])
        h1 = hb_block(1.4, 1.1, GREY, fill=0.3, slot_r=0.13).move_to([2.75, -0.5, 0])
        h2 = hb_block(1.4, 1.1, GREY, fill=0.3, slot_r=0.13).move_to([4.65, -0.5, 0])
        cl = T("more BPG inside red cells", 28, PURP).move_to([3.7, -2.05, 0])
        self.play(FadeOut(card1), FadeOut(mer), run_time=0.5)
        self.add(c2)
        self.play(FadeIn(c2), FadeIn(cell), FadeIn(h1), FadeIn(h2), FadeIn(cl), run_time=1.0)
        self.at("a small molecule")
        chips = VGroup(*[chip("BPG", PURP, 22, pad=0.1, fill_opacity=0.3) for _ in range(2)])
        chips[0].move_to([2.3, 0.15, 0])
        chips[1].move_to([5.1, 0.15, 0])
        self.play(FadeIn(chips), run_time=0.6)
        self.play(chips[0].animate.move_to([3.7, -0.15, 0]), chips[1].animate.move_to([3.7, -0.85, 0]),
                  kt.animate.set_value(1.42), run_time=1.8)
        self.finish()


# ---------------------------------------------------------------------------------------------
class S16Separate(SpokenScene):
    def construct(self):
        motes(self, 12, 46)
        xs = [-4.5, 0.0, 4.5]
        specs = [("Bohr effect", "pH and CO2", ORANGE), ("temperature", "", YELLOW), ("BPG", "", PURP)]
        boxes = []
        for (t1, t2, col), x in zip(specs, xs):
            bx = RoundedRectangle(corner_radius=0.25, width=4.1, height=4.6, stroke_color=col, stroke_width=5,
                                  fill_color=col, fill_opacity=0.1).move_to([x, -0.2, 0])
            tx = T(t1, 42, col).move_to([x, 1.45, 0])
            fit(tx, max_w=3.7)
            g = VGroup(bx, tx)
            if t2:
                g.add(T(t2, 34, TEXT).move_to([x, 0.6, 0]))
            boxes.append(g)
        ic1 = co2_bubble().scale(1.6).move_to([xs[0], -1.15, 0])
        tt = ValueTracker(0.8)
        th, mer = thermometer(xs[1], -0.55, tt, h=2.2)
        cell = Ellipse(width=2.8, height=1.5, color=RED, stroke_width=5, fill_opacity=0.16).move_to([xs[2], -0.4, 0])
        ic3 = chip("BPG", PURP, 28, pad=0.15, fill_opacity=0.3).move_to([xs[2], -0.4, 0])
        self.at("they are separate")
        self.play(FadeIn(boxes[0], shift=UP * 0.2), FadeIn(ic1), run_time=0.5)
        self.play(FadeIn(boxes[1], shift=UP * 0.2), FadeIn(th), FadeIn(mer), run_time=0.5)
        self.play(FadeIn(boxes[2], shift=UP * 0.2), FadeIn(cell), FadeIn(ic3), run_time=0.5)
        self.at("each with its own")
        self.play(Indicate(boxes[0][0], color=ORANGE, scale_factor=1.04), Indicate(boxes[1][0], color=YELLOW, scale_factor=1.04),
                  Indicate(boxes[2][0], color=PURP, scale_factor=1.04), run_time=1.4)
        self.at("the name")
        top = Line([xs[0], 2.6, 0], [xs[2], 2.6, 0], color=ORANGE, stroke_width=6)
        dr = VGroup(Line([xs[0], 2.6, 0], [xs[0], 2.1, 0], color=ORANGE, stroke_width=6),
                    Line([xs[1], 2.6, 0], [xs[1], 2.1, 0], color=ORANGE, stroke_width=6),
                    Line([xs[2], 2.6, 0], [xs[2], 2.1, 0], color=ORANGE, stroke_width=6))
        ql = T("all one Bohr effect?", 34, ORANGE).move_to([0, 3.2, 0])
        self.play(Create(top), Create(dr), FadeIn(ql), run_time=1.3)
        self.at("kept for")
        self.play(FadeOut(VGroup(top, dr, ql)), run_time=0.9)
        self.play(Indicate(boxes[0], color=ORANGE, scale_factor=1.06), run_time=1.2)
        self.finish()


# ---------------------------------------------------------------------------------------------
class S17Close(SpokenScene):
    def construct(self):
        motes(self, 12, 47)
        self.add(axes_y(), axes_x(), sev_curve(), band(P_LUNG, BLUE, 0.22), band(P_REST, GREY, 0.35),
                 lung_label(), tis_label(), legend())
        self.add(pdot(P_LUNG, S_LUNG, RED, 0.12), pdot(P_REST, S_REST, RED, 0.14))
        oc = ora_curve()
        self.play(Create(oc), run_time=1.0)
        od1, od2 = pdot(P_LUNG, O_LUNG, ORANGE, 0.12).set_z_index(6), pdot(P_REST, O_REST, ORANGE, 0.14).set_z_index(6)
        self.play(FadeIn(od1, scale=2), FadeIn(od2, scale=2), run_time=0.5)
        self.at("costs little")
        cl = T("costs little", 32, BLUE).move_to([5.0, 0.9, 0])
        self.play(FadeIn(cl, shift=UP * 0.1), Indicate(od1, color=ORANGE, scale_factor=2.2), run_time=1.0)
        self.at("it pays out")
        b1 = rel_bar(2.4, S_LUNG, S_REST)
        b2 = rel_bar(3.4, O_LUNG, O_REST)
        self.play(Create(b1), run_time=0.8)
        self.play(Create(b2), run_time=0.8)
        pl = T("pays out", 32, GOLD).move_to([-0.2, -0.75, 0])
        self.play(FadeIn(pl, shift=UP * 0.1), run_time=0.7)
        self.at("where blood unloads")
        self.play(Indicate(b2[2], color=GOLD, scale_factor=1.15), Indicate(od2, color=ORANGE, scale_factor=2.0), run_time=1.2)
        self.finish()


# ---------------------------------------------------------------------------------------------
class S18End(EndCard):
    LINE = "A modest right shift barely costs loading but raises release in tissue."
