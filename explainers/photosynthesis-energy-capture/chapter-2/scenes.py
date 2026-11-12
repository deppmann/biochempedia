"""The Slowest Worker Sets the Pace: limiting factors (chapter-2 film, Capturing Sunlight).

COLOUR MAP (same as chapter 1): carbon dioxide BLUE, water TEAL, light YELLOW, glucose AMBER, oxygen RED,
the plant GREEN, soil brown, structure GREY. Dark ground, same fonts and helpers as chapter 1.
"""
import random
import numpy as np
from bp_style import *  # noqa: F401,F403

AMBER = "#F2A93B"
SOIL = "#8B6B4A"
ALGAE = "#9ACD32"
COATC = "#B8A98A"
WHITE = "#F4F4F4"

CUP_X, CW, CB, CT = -3.4, 2.8, -3.0, -0.4      # cup centre x, width, bottom, water surface
MX, MY = 5.6, 2.95                                # rate meter pivot
GX0, GY0 = 0.8, -3.1                             # graph origin
BX0, BX1, BT, BB = -1.4, 4.2, 3.0, -3.0          # bay water column: left, right, surface, bed top
PERM = [3, 7, 1, 9, 5, 0, 8, 2, 6, 4]


def P(x, y):
    return np.array([x, y, 0.0])


def gx(L):
    return GX0 + 0.68 * L


def gy(r):
    return GY0 + 0.53 * r


def rate(L, cap):
    return min(L, cap)


def world_start(sc, ambient=True):
    sc.clock = ValueTracker(0)
    sc.clock.add_updater(lambda m, dt: m.increment_value(dt))
    sc.add(sc.clock)
    if not ambient:
        return
    rng = random.Random(type(sc).__name__)
    W, H = config.frame_width, config.frame_height
    motes = VGroup()
    for _ in range(22):
        d = Dot(radius=rng.uniform(0.025, 0.06), color=rng.choice([TEAL, GREY, TEXT])).set_opacity(rng.uniform(0.12, 0.3))
        d.move_to([rng.uniform(-W / 2, W / 2), rng.uniform(-H / 2, H / 2), 0])
        d.v = (rng.uniform(-0.2, 0.2), rng.uniform(0.15, 0.4))

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


# ----------------------------------------------------------------------------- rate meter
class Meter:
    def __init__(self, sc, m=0.0, twitch=0.0):
        self.sc = sc
        self.m = ValueTracker(m)
        self.tw = ValueTracker(twitch)
        c = P(MX, MY)
        self.arc = Arc(radius=0.85, start_angle=0, angle=PI, arc_center=c, stroke_color=GREY, stroke_width=6)
        self.base = Line(P(MX - 0.85, MY), P(MX + 0.85, MY), stroke_color=GREY, stroke_width=4)

        def val():
            return float(np.clip(self.m.get_value() + self.tw.get_value() * 0.03 * np.sin(13 * sc.clock.get_value()), 0.001, 1))

        def fill():
            v = val()
            return Arc(radius=0.85, start_angle=PI - PI * v, angle=PI * v, arc_center=c, stroke_color=RED, stroke_width=9)

        def needle():
            a = PI - PI * val()
            return Line(c, c + 0.78 * P(np.cos(a), np.sin(a)), stroke_color=TEXT, stroke_width=5)
        self.fill = always_redraw(fill)
        self.needle = always_redraw(needle)
        self.pivot = Dot(c, radius=0.09, color=TEXT)
        self.label = T("relative net\noxygen build-up\n(flotation proxy)", 22, TEXT, line_spacing=0.9).move_to(P(MX - 0.1, 1.95))
        self.label.align_to(P(6.72, 0), RIGHT)
        self.mobs = VGroup(self.arc, self.base, self.fill, self.needle, self.pivot, self.label)

    def link(self, lab):
        self.m.clear_updaters()
        self.m.add_updater(lambda t: t.set_value(lab.meter_value()))

    def unlink(self):
        self.m.clear_updaters()


# ----------------------------------------------------------------------------- lamp
def lamp_group(sc, x, Ltr, on_tr, ysurf, spread=1.0):
    def build():
        L, on, t = Ltr.get_value(), on_tr.get_value(), sc.clock.get_value()
        y = 3.1 - 0.33 * L
        g = VGroup()
        g.add(Line(P(x, y + 0.5), P(x, y + 0.9), stroke_color=GREY, stroke_width=4))
        g.add(Polygon(P(x - 0.2, y + 0.5), P(x + 0.2, y + 0.5), P(x + 0.42, y + 0.1), P(x - 0.42, y + 0.1),
                      stroke_color=GREY, stroke_width=3, fill_color=GREY, fill_opacity=0.5))
        g.add(Circle(radius=0.55 + 0.04 * np.sin(3 * t), stroke_width=0, fill_color=YELLOW, fill_opacity=0.22 * on).move_to(P(x, y - 0.05)))
        g.add(Circle(radius=0.27, stroke_color=YELLOW, stroke_width=3, fill_color=YELLOW, fill_opacity=0.15 + 0.8 * on).move_to(P(x, y - 0.05)))
        if on > 0.02:
            op = float(np.clip((0.2 + 0.09 * L) * on, 0, 0.9))
            for i, dx in enumerate(np.linspace(-1, 1, 5)):
                o = op * (0.85 + 0.15 * np.sin(3 * t + i))
                g.add(Line(P(x + dx * 0.3, y - 0.3), P(x + dx * 0.95 * spread, ysurf), stroke_color=YELLOW, stroke_width=4, stroke_opacity=o))
        return g
    return always_redraw(build)


# ----------------------------------------------------------------------------- the cup
def cup_static():
    l, r = CUP_X - CW / 2, CUP_X + CW / 2
    water = Rectangle(width=CW, height=CT - CB, stroke_width=0, fill_color=TEAL, fill_opacity=0.18).move_to(P(CUP_X, (CT + CB) / 2))
    walls = VMobject(stroke_color=TEXT, stroke_width=5)
    walls.set_points_as_corners([P(l, CT + 0.25), P(l, CB), P(r, CB), P(r, CT + 0.25)])
    return VGroup(water, walls)


def cup_pos(i):
    return P(CUP_X - 0.95 + 0.475 * (i % 5) + 0.12 * (i // 5), CB + 0.17 + 0.27 * (i // 5))


def top_pos(i):
    return P(CUP_X - 0.95 + 0.475 * (i % 5) + 0.12 * (i // 5), CT - 0.17 - 0.26 * (i // 5))


def leaf_pos(i):
    return P(1.2 + 0.85 * (i % 5), 0.4 - 0.85 * (i // 5))


class Lab:
    """Cup + disks + dissolved carbon dioxide + lamp. Trackers: L (lamp), on, p (trial progress 0..1),
    co2 (0..1), cap (carbon dioxide cap on the rate), d (1 = disks still on the leaf), nvis, dy."""

    def __init__(self, sc, co2=0.0, L=1.0, on=0.0, p=0.0, cap=4.5, d=0.0, nvis=10.0):
        self.sc = sc
        self.co2, self.L, self.on, self.p = ValueTracker(co2), ValueTracker(L), ValueTracker(on), ValueTracker(p)
        self.cap, self.d, self.nvis, self.dy = ValueTracker(cap), ValueTracker(d), ValueTracker(nvis), ValueTracker(0)
        self.static = cup_static()
        rng = random.Random(7)
        self.dpos = [(rng.uniform(-1.2, 1.2), rng.uniform(0.45, 2.3), rng.uniform(0, 6)) for _ in range(22)]
        self.dots = always_redraw(self.build_dots)
        self.disks = always_redraw(self.build_disks)
        self.lamp = lamp_group(sc, CUP_X, self.L, self.on, CT, spread=1.0)

    def spd(self):
        return 0.6 + 0.4 * rate(self.L.get_value(), self.cap.get_value())

    def tau(self, i):
        return (0.25 + 0.6 * PERM.index(i) / 9) / self.spd()

    def f(self, i):
        x = float(np.clip((self.p.get_value() - self.tau(i)) / 0.12, 0, 1))
        return float(smooth(x))

    def meter_value(self):
        fr = sum(self.f(i) for i in range(10)) / 10
        return 0.95 * rate(self.L.get_value(), self.cap.get_value()) / 7.5 * fr * self.on.get_value() ** 0

    def count(self):
        return int(sum(1 for i in range(10) if self.f(i) > 0.5))

    def build_dots(self):
        t = self.sc.clock.get_value()
        k = self.co2.get_value() * 22
        g = VGroup()
        for i, (ox, oy, ph) in enumerate(self.dpos):
            op = float(np.clip(k - i, 0, 1)) * 0.85
            if op < 0.02:
                continue
            g.add(Dot(P(CUP_X + ox + 0.1 * np.sin(0.8 * t + ph), CB + oy + 0.1 * np.sin(0.6 * t + ph * 1.3)),
                      radius=0.07, color=BLUE).set_opacity(op))
        return g

    def build_disks(self):
        t = self.sc.clock.get_value()
        d, dy, on = self.d.get_value(), self.dy.get_value(), self.on.get_value()
        nv = self.nvis.get_value()
        g = VGroup()
        for i in range(10):
            v = float(np.clip(nv - i, 0, 1))
            if v < 0.02:
                continue
            f = self.f(i)
            a, b = cup_pos(i), top_pos(i)
            pos = a + (b - a) * f
            pos = pos * (1 - d) + leaf_pos(i) * d
            pos = pos + P(0, dy * d + 0.03 * np.sin(1.5 * t + i) * f)
            e = Ellipse(width=0.44, height=0.26, stroke_color=GREEN, stroke_width=2, fill_color=GREEN, fill_opacity=0.85 * v).move_to(pos)
            e.set_stroke(opacity=v)
            g.add(e)
            bub = on * float(np.clip((self.p.get_value() - self.tau(i) + 0.3) / 0.3, 0, 1))
            if bub > 0.02 and d < 0.5:
                g.add(Dot(pos + P(-0.06, 0.02), radius=0.05, color=RED).set_opacity(bub))
                g.add(Dot(pos + P(0.07, -0.02), radius=0.04, color=RED).set_opacity(bub))
        return g

    def add_to(self, sc, lamp=True, disks=True, dots=True):
        sc.add(self.static)
        if dots:
            sc.add(self.dots)
        if disks:
            sc.add(self.disks)
        if lamp:
            sc.add(self.lamp)

    def trial(self, sc, L, run=1.2, move=0.5):
        sc.play(self.L.animate.set_value(L), run_time=move)
        self.p.set_value(0)
        sc.play(self.p.animate.set_value(1.0), run_time=run, rate_func=linear)


def co2_gauge(lab):
    x0, y0, h = -6.1, -3.0, 1.7
    box = Rectangle(width=0.4, height=h, stroke_color=BLUE, stroke_width=3).move_to(P(x0, y0 + h / 2))
    fill = always_redraw(lambda: Rectangle(width=0.4, height=max(0.02, h * float(np.clip(lab.co2.get_value(), 0, 1))), stroke_width=0,
                                           fill_color=BLUE, fill_opacity=0.85).move_to(P(x0, y0 + max(0.02, h * float(np.clip(lab.co2.get_value(), 0, 1))) / 2)))
    lab_t = T("carbon\ndioxide\nsupply", 24, BLUE, line_spacing=0.9).move_to(P(x0, -0.55))
    return VGroup(box, fill, lab_t)


# ----------------------------------------------------------------------------- graph
def x_axis(Lend=4.6):
    return Line(P(GX0, GY0), P(gx(Lend), GY0), stroke_color=GREY, stroke_width=4)


def y_axis():
    return Line(P(GX0, GY0), P(GX0, gy(7.5)), stroke_color=GREY, stroke_width=4)


def x_ext(a=4.6, b=8.0):
    return DashedVMobject(Line(P(gx(a), GY0), P(gx(b), GY0), stroke_color=GREY, stroke_width=4), num_dashes=10)


def x_label():
    t = T("light (lamp closer)", 26, TEXT).move_to(P(3.2, -3.55))
    ar = Arrow(P(5.0, -3.55), P(6.0, -3.55), color=YELLOW, buff=0, stroke_width=5, max_tip_length_to_length_ratio=0.3)
    return VGroup(t, ar)


def graph_tag():
    return T("rate (computed, relative units)", 22, TEXT).move_to(P(0.45, 1.1), aligned_edge=LEFT)


def curve(a, b, cap, color=TEXT, width=6, n=60):
    pts = [P(gx(L), gy(rate(L, cap))) for L in np.linspace(a, b, n)]
    m = VMobject(stroke_color=color, stroke_width=width)
    m.set_points_as_corners(pts)
    return m


def gpoint(L, cap):
    return Dot(P(gx(L), gy(rate(L, cap))), radius=0.14, color=TEXT)


def drop_point(sc, L, cap, rt=0.45):
    d = gpoint(L, cap)
    sc.play(FadeIn(d, shift=DOWN * 0.5, scale=1.6), run_time=rt)
    return d


# ----------------------------------------------------------------------------- the Bay
class Bay:
    def __init__(self, sc, turb=0.0, mud=0.0, alg=0.0, coat=0.0, rays_on=1.0):
        self.sc = sc
        self.turb, self.mud, self.alg, self.coat, self.rays_on = (ValueTracker(v) for v in (turb, mud, alg, coat, rays_on))
        self.static = VGroup(
            Rectangle(width=BX1 - BX0, height=BT - BB, stroke_width=0, fill_color=TEAL, fill_opacity=0.14).move_to(P((BX0 + BX1) / 2, (BT + BB) / 2)),
            Line(P(BX0, BT), P(BX1, BT), stroke_color=TEAL, stroke_width=5),
            Rectangle(width=BX1 - BX0, height=0.3, stroke_width=0, fill_color=SOIL, fill_opacity=0.7).move_to(P((BX0 + BX1) / 2, BB - 0.15)),
        )
        rng = random.Random(11)
        self.bx = [BX0 + 0.35 + (BX1 - BX0 - 0.7) * k / 13 for k in range(14)]
        self.bh = [rng.uniform(1.2, 1.8) for _ in range(14)]
        self.bph = [rng.uniform(0, 6) for _ in range(14)]
        self.mudp = [(rng.uniform(BX0 + 0.2, BX1 - 0.2), rng.uniform(BB + 0.5, BT - 0.3), rng.uniform(0, 6)) for _ in range(16)]
        self.algp = [(rng.uniform(BX0 + 0.2, BX1 - 0.2), rng.uniform(BB + 0.5, BT - 0.3), rng.uniform(0, 6)) for _ in range(14)]
        self.rays = always_redraw(self.build_rays)
        self.blades = always_redraw(self.build_blades)
        self.parts = always_redraw(self.build_parts)

    def frac(self):
        return 0.6 * float(np.exp(-1.6 * self.turb.get_value()))

    def build_rays(self):
        on = self.rays_on.get_value()
        g = VGroup()
        if on < 0.02:
            return g
        fr = self.frac()
        t = self.sc.clock.get_value()
        n = 8
        for k, x in enumerate(np.linspace(BX0 + 0.5, BX1 - 0.5, 6)):
            for s in range(n):
                d0, d1 = s / n, (s + 1) / n
                op = on * 0.85 * (fr / 0.85) ** ((d0 + d1) / 2) * (0.85 + 0.15 * np.sin(2.5 * t + k))
                g.add(Line(P(x, BT - (BT - BB) * d0), P(x, BT - (BT - BB) * d1), stroke_color=YELLOW, stroke_width=5, stroke_opacity=float(op)))
        return g

    def blade_pts(self, i):
        t = self.sc.clock.get_value()
        h = self.bh[i]
        pts = []
        for s in np.linspace(0, 1, 6):
            sw = 0.16 * np.sin(1.2 * t + self.bph[i] + 2 * s) * s ** 1.5
            pts.append(P(self.bx[i] + sw, BB + h * s))
        return pts

    def build_blades(self):
        fr = self.frac()
        op = 0.4 + 0.6 * min(1.0, fr / 0.6)
        g = VGroup()
        for i in range(14):
            m = VMobject(stroke_color=GREEN, stroke_width=6, stroke_opacity=op)
            m.set_points_smoothly(self.blade_pts(i))
            g.add(m)
        return g

    def build_parts(self):
        t = self.sc.clock.get_value()
        g = VGroup()
        mv, av, cv = self.mud.get_value(), self.alg.get_value(), self.coat.get_value()
        if mv > 0.02:
            for (x, y, ph) in self.mudp:
                g.add(Dot(P(x + 0.25 * np.sin(0.5 * t + ph), y + 0.15 * np.sin(0.4 * t + ph)), radius=0.11, color=SOIL).set_opacity(0.9 * mv))
        if av > 0.02:
            for (x, y, ph) in self.algp:
                g.add(Dot(P(x + 0.25 * np.sin(0.45 * t + ph), y + 0.15 * np.sin(0.35 * t + ph * 1.4)), radius=0.09, color=ALGAE).set_opacity(0.9 * av))
        if cv > 0.02:
            for i in range(14):
                pts = self.blade_pts(i)
                for s in (2, 3, 4):
                    g.add(Dot(pts[s] + P(0.06, 0), radius=0.07, color=COATC).set_opacity(0.9 * cv))
        return g

    def add_to(self, sc):
        sc.add(self.static, self.rays, self.blades, self.parts)

    def meter_value(self):
        return 0.75 * self.frac() / 0.6


def light_gauge(bay, x=-2.3):
    y0, h = -3.0, 4.0
    box = Rectangle(width=0.4, height=h, stroke_color=YELLOW, stroke_width=3).move_to(P(x, y0 + h / 2))
    fill = always_redraw(lambda: Rectangle(width=0.4, height=max(0.02, h * bay.frac()), stroke_width=0, fill_color=YELLOW,
                                           fill_opacity=0.85).move_to(P(x, y0 + max(0.02, h * bay.frac()) / 2)))
    return VGroup(box, fill)


def target_line(x=-2.3):
    y = -3.0 + 4.0 * 0.22
    return DashedVMobject(Line(P(-6.3, y), P(x + 0.25, y), stroke_color=TEXT, stroke_width=4), num_dashes=16)


# ----------------------------------------------------------------------------- map of the Bay (schematic)
MAP = [(-4.0, 3.3), (-3.55, 3.15), (-3.5, 2.4), (-3.75, 1.6), (-3.55, 0.8), (-3.7, 0.0), (-3.5, -0.8), (-3.6, -1.6),
       (-3.45, -2.4), (-3.5, -3.2), (-2.6, -3.3), (-2.55, -2.4), (-2.8, -1.6), (-2.75, -0.8), (-2.95, 0.0), (-2.8, 0.9),
       (-3.1, 1.7), (-3.0, 2.5), (-3.2, 3.3)]


def bay_map():
    outline = Polygon(*[P(x, y) for x, y in MAP], stroke_color=TEAL, stroke_width=4, fill_color=TEAL, fill_opacity=0.3)
    lowpts = [(-3.6, -1.0), (-3.55, -1.6), (-3.45, -2.4), (-3.5, -3.2), (-2.6, -3.3), (-2.55, -2.4), (-2.8, -1.6), (-2.8, -1.0)]
    low = Polygon(*[P(x, y) for x, y in lowpts], stroke_width=0, fill_color=TEAL, fill_opacity=0.75)
    sch = T("schematic map", 22, TEXT).move_to(P(-4.6, -3.55))
    return outline, low, sch


# ----------------------------------------------------------------------------- shared
def leaf_mob():
    body = Ellipse(width=5.6, height=3.4, stroke_color=GREEN, stroke_width=5, fill_color=GREEN, fill_opacity=0.3).move_to(P(2.6, -0.4))
    vein = Line(P(-0.1, -0.4), P(5.3, -0.4), stroke_color=GREEN, stroke_width=4).set_opacity(0.6)
    return VGroup(body, vein)


def pulse_ring(sc, mob, color=GOLD, rt=0.8):
    ring = SurroundingRectangle(mob, color=color, buff=0.12, stroke_width=5, corner_radius=0.1)
    sc.play(Create(ring), run_time=rt / 2)
    sc.play(FadeOut(ring), run_time=rt / 2)


# ============================================================================ scenes
class S00Title(TitleCard):
    LESSON = "Capturing Sunlight"
    TITLE = "The Slowest Worker Sets the Pace"


class S01Question(SpokenScene):
    def construct(self):
        world_start(self)
        co2 = chip("carbon dioxide", BLUE, 36)
        wat = chip("water", TEAL, 36)
        plus = T("+", 40, TEXT)
        glu = chip("glucose", AMBER, 36)
        arrow = Arrow(LEFT * 0.5, RIGHT * 0.5, color=YELLOW, buff=0, stroke_width=7)
        ray = Line(P(-0.5, 2.2), P(-0.05, 1.5), stroke_color=YELLOW, stroke_width=6)
        left = VGroup(co2, plus, wat).arrange(RIGHT, buff=0.3)
        strip = VGroup(left, arrow, glu).arrange(RIGHT, buff=0.4).move_to(P(-0.5, 0.4))
        ray.move_to(arrow.get_center() + UP * 1.0)
        self.play(FadeIn(left, shift=RIGHT * 0.3), run_time=0.9)
        self.at("what a plant builds its sugar from")
        self.play(GrowArrow(arrow), Create(ray), run_time=0.7)
        self.play(FadeIn(glu, shift=RIGHT * 0.3), run_time=0.7)
        self.wait(0.4)
        # shrink to an icon
        icon = VGroup(Square(0.3, stroke_width=0, fill_color=BLUE, fill_opacity=1), Square(0.3, stroke_width=0, fill_color=TEAL, fill_opacity=1),
                      Arrow(LEFT * 0.25, RIGHT * 0.25, color=YELLOW, buff=0, stroke_width=4), Square(0.34, stroke_width=0, fill_color=AMBER, fill_opacity=1)
                      ).arrange(RIGHT, buff=0.12).move_to(P(-5.6, 3.35))
        self.play(ReplacementTransform(VGroup(strip, ray), icon), run_time=0.9)
        self.at("this film asks how fast it can build")
        leaf = leaf_mob().scale(0.62).move_to(P(-1.2, -1.9))
        meter = Meter(self, 0.0, twitch=0.0)
        Ltr, on = ValueTracker(1.0), ValueTracker(1.0)
        lp = lamp_group(self, -1.2, Ltr, on, -1.0, spread=1.2)
        self.play(FadeIn(leaf), FadeIn(meter.mobs), run_time=0.8)
        self.add(meter.fill, meter.needle)
        self.add(lp)
        self.play(Ltr.animate.set_value(4.0), meter.m.animate.set_value(0.55), run_time=2.2)
        self.at("why does more light stop")
        meter.tw.set_value(1.0)
        q = T("?", 150, GOLD, weight=BOLD).move_to(P(2.3, 0.3))
        self.play(FadeIn(q, scale=0.5), run_time=0.6)
        q.add_updater(lambda m: m.move_to(P(2.3, 0.3 + 0.1 * np.sin(2 * self.clock.get_value()))))
        self.finish()


class S02Disks(SpokenScene):
    def construct(self):
        world_start(self)
        lab = Lab(self, co2=0.0, L=1.0, on=0.0, d=1.0, nvis=0.0)
        meter = Meter(self, 0.0)
        self.add(lab.disks)
        self.play(Create(lab.static[1]), FadeIn(lab.static[0]), FadeIn(meter.mobs), run_time=1.4)
        self.add(meter.fill, meter.needle)
        leaf = leaf_mob()
        self.play(FadeIn(leaf), run_time=0.8)
        self.at("punch small discs out of a spinach leaf")
        ring = Circle(radius=0.3, stroke_color=TEXT, stroke_width=6)
        straw = Line(P(0, 0), P(0.9, 1.1), stroke_color=TEXT, stroke_width=6)
        punch = VGroup(ring, straw).move_to(leaf_pos(0) + P(0.45, 0.55))
        punch.shift(leaf_pos(0) - ring.get_center())
        holes = VGroup()
        self.add(punch)
        for i in range(10):
            tgt = leaf_pos(i)
            self.play(punch.animate.shift(tgt - ring.get_center()), run_time=0.09)
            self.play(lab.nvis.animate.set_value(i + 1), run_time=0.11)
            h = DashedVMobject(Circle(radius=0.24, stroke_color=TEXT, stroke_width=3).move_to(tgt), num_dashes=8)
            holes.add(h)
            self.add(h)
        self.play(FadeOut(punch), run_time=0.3)
        self.at("pull the air out of them")
        air = ValueTracker(0)

        def bubbles():
            a = air.get_value()
            g = VGroup()
            for i in range(10):
                for j in range(3):
                    g.add(Dot(leaf_pos(i) + P(0.12 * (j - 1) + 0.05 * np.sin(5 * a + i), 0.3 + a * (0.9 + 0.3 * j)), radius=0.05, color=WHITE).set_opacity(max(0, 0.8 * (1 - a))))
            return g
        bub = always_redraw(bubbles)
        self.add(bub)
        at = T("air out", 30, WHITE).move_to(P(2.6, -2.8))
        self.play(air.animate.set_value(1.0), FadeIn(at), run_time=0.9, rate_func=linear)
        self.remove(bub)
        self.at("so they sink")
        self.play(FadeOut(at), lab.dy.animate.set_value(-0.35), run_time=0.5)
        sk = T("they sink", 30, TEXT).move_to(P(2.6, -2.8))
        self.add(sk)
        self.at("drop them into water")
        self.play(FadeOut(sk), FadeOut(VGroup(leaf, holes)), lab.d.animate.set_value(0.0), lab.dy.animate.set_value(0), run_time=1.5, rate_func=smooth)
        self.at("with baking soda")
        spoon = VGroup(RoundedRectangle(corner_radius=0.1, width=0.8, height=0.3, stroke_color=GREY, stroke_width=3, fill_color=GREY, fill_opacity=0.5),
                       Line(P(0.4, 0), P(1.2, 0.5), stroke_color=GREY, stroke_width=5)).move_to(P(-5.2, 0.3)).rotate(-0.4)
        bl = T("baking soda", 30, WHITE).move_to(P(-5.4, 1.2))
        self.add(lab.dots)
        self.play(FadeIn(spoon), FadeIn(bl), run_time=0.5)
        grains = VGroup(*[Dot(P(-4.6 + 0.12 * k, 0.1), radius=0.05, color=WHITE) for k in range(8)])
        self.add(grains)
        self.play(grains.animate.shift(DOWN * 0.9).set_opacity(0), lab.co2.animate.set_value(0.6), run_time=1.6)
        self.finish()


class S03Float(SpokenScene):
    def construct(self):
        world_start(self)
        lab = Lab(self, co2=0.6, L=2.0, on=0.0, p=0.0)
        meter = Meter(self, 0.0)
        lab.add_to(self)
        self.add(meter.mobs, meter.fill, meter.needle)
        meter.link(lab)
        self.add(meter.m)
        self.at("dissolved carbon dioxide")
        tag = T("dissolved carbon dioxide", 30, BLUE).move_to(P(2.5, 0.2))
        arr = Arrow(P(0.5, 0.0), P(-1.9, -1.1), color=BLUE, buff=0, stroke_width=5)
        self.play(FadeIn(tag, shift=LEFT * 0.2), GrowArrow(arr), run_time=0.9)
        self.at("shine a lamp on the cup")
        self.play(lab.on.animate.set_value(1.0), run_time=1.2)
        self.at("as the discs photosynthesize")
        cnt = always_redraw(lambda: T(f"floating: {lab.count()} of 10", 42, TEXT, weight=BOLD).move_to(P(2.6, -1.8)))
        self.play(FadeOut(VGroup(tag, arr)), FadeIn(cnt), run_time=0.6)
        self.at("oxygen gas collects inside them")
        ox = T("oxygen gas inside", 30, RED).move_to(P(2.6, -0.7))
        self.play(FadeIn(ox, shift=UP * 0.15), run_time=0.6)
        self.at("one by one")
        self.play(lab.p.animate.set_value(1.0), run_time=3.6, rate_func=linear)
        self.play(FadeOut(ox), run_time=0.5)
        self.finish()


class S04Curve(SpokenScene):
    def construct(self):
        world_start(self)
        lab = Lab(self, co2=0.6, L=2.0, on=1.0, p=1.0)
        meter = Meter(self, 0.0)
        lab.add_to(self)
        self.add(meter.mobs, meter.fill, meter.needle)
        meter.link(lab)
        self.add(meter.m)
        cnt = T("floating: 10 of 10", 42, TEXT, weight=BOLD).move_to(P(2.6, -1.8))
        self.add(cnt)
        xa, ya, xl, gt = x_axis(4.6), y_axis(), x_label(), graph_tag()
        self.play(FadeOut(cnt), Create(xa), Create(ya), FadeIn(xl), FadeIn(gt), run_time=0.9)
        pts = []
        lab.L.set_value(1.0)
        lab.p.set_value(0)
        self.play(lab.p.animate.set_value(1.0), run_time=1.2, rate_func=linear)
        pts.append(drop_point(self, 1, 4.5, 0.35))
        self.at("move the lamp closer")
        lab.trial(self, 2.0, run=0.7, move=0.4)
        pts.append(drop_point(self, 2, 4.5, 0.35))
        self.at("step by step")
        lab.trial(self, 3.0, run=0.7, move=0.4)
        pts.append(drop_point(self, 3, 4.5, 0.35))
        self.at("each time the discs float sooner")
        lab.trial(self, 4.0, run=0.9, move=0.4)
        pts.append(drop_point(self, 4, 4.5))
        self.at("plot the rate against brightness")
        self.play(Indicate(gt, color=GOLD, scale_factor=1.05), lab.p.animate.set_value(0.0), run_time=0.4)
        self.play(lab.p.animate.set_value(1.0), run_time=1.0, rate_func=linear)
        self.at("and the curve climbs")
        ln = curve(1, 4, 4.5)
        self.play(Create(ln), run_time=1.5)
        tg = T("light is holding the rate back", 28, YELLOW).move_to(P(3.6, 0.0))
        self.play(FadeIn(tg, shift=UP * 0.15), run_time=0.6)
        self.finish()


def graph_base(sc, lab, ext=False, upto=4):
    """Rebuild chapter-2's graph in the same place: axes, label, points 1..upto and the line."""
    xa = x_axis(4.6)
    items = [xa, y_axis(), x_label(), graph_tag()]
    sc.add(*items)
    pts = [gpoint(L, 4.5) for L in range(1, upto + 1)]
    ln = curve(1, upto, 4.5)
    sc.add(*pts, ln)
    return items, pts, ln


class S05Predict(SpokenScene):
    def construct(self):
        world_start(self)
        lab = Lab(self, co2=0.6, L=4.0, on=1.0, p=1.0)
        meter = Meter(self, 0.0)
        lab.add_to(self)
        self.add(meter.mobs, meter.fill, meter.needle)
        meter.link(lab)
        self.add(meter.m)
        graph_base(self, lab)
        self.at("this cup has only a pinch of baking soda")
        spoon = VGroup(RoundedRectangle(corner_radius=0.1, width=0.6, height=0.25, stroke_color=GREY, stroke_width=3, fill_color=GREY, fill_opacity=0.5),
                       Line(P(0.3, 0), P(1.0, 0.45), stroke_color=GREY, stroke_width=5)).move_to(P(-5.6, 0.2)).rotate(-0.4)
        pl = T("a pinch of\nbaking soda", 28, WHITE, line_spacing=0.9).move_to(P(-5.6, 1.1))
        grains = VGroup(*[Dot(P(-4.6 + 0.12 * k, 0.0), radius=0.05, color=WHITE) for k in range(3)])
        self.add(grains)
        self.play(FadeIn(spoon), FadeIn(pl), lab.co2.animate.set_value(0.3), grains.animate.shift(DOWN * 0.8).set_opacity(0), run_time=1.8)
        self.at("keep moving the lamp closer")
        ext = x_ext()
        qm = T("?", 90, GOLD, weight=BOLD).move_to(P(5.2, -1.6))
        self.play(Create(ext), FadeIn(qm, scale=0.6), lab.L.animate.set_value(4.4), run_time=1.6)
        self.play(lab.L.animate.set_value(4.0), run_time=0.8)
        self.at("does the curve keep climbing")
        q = T("Does the curve keep climbing?", 36, TEXT).move_to(P(-1.2, 3.4))
        self.play(FadeIn(q, shift=DOWN * 0.15), lab.L.animate.set_value(4.6), run_time=1.2)
        self.play(lab.L.animate.set_value(4.0), run_time=0.8)
        self.at("make your guess")
        qm.add_updater(lambda m: m.set_opacity(0.6 + 0.4 * np.sin(4 * self.clock.get_value())))
        self.play(lab.L.animate.set_value(4.8), run_time=1.0)
        self.finish()


class S06Pause(NarratedScene):
    def construct(self):
        world_start(self)
        lab = Lab(self, co2=0.3, L=4.0, on=1.0, p=1.0)
        meter = Meter(self, 0.0)
        lab.add_to(self)
        self.add(meter.mobs, meter.fill, meter.needle)
        meter.link(lab)
        self.add(meter.m)
        graph_base(self, lab)
        self.add(x_ext())
        q = T("Does the curve keep climbing?", 36, TEXT).move_to(P(-1.2, 3.4))
        qm = T("?", 90, GOLD, weight=BOLD).move_to(P(5.2, -1.6))
        qm.add_updater(lambda m: m.set_opacity(0.6 + 0.4 * np.sin(4 * self.clock.get_value())))
        self.add(q, qm)
        k = ValueTracker(0)
        c0 = P(-6.0, 3.3)
        back = Circle(radius=0.36, stroke_color=GREY, stroke_width=4).move_to(c0)
        fill = always_redraw(lambda: Sector(radius=0.34, angle=max(0.01, TAU * k.get_value()), start_angle=PI / 2,
                                            fill_color=GOLD, fill_opacity=0.9, stroke_width=0, arc_center=c0))
        self.add(back, fill)
        self.play(k.animate.set_value(1.0), run_time=self.narration_s, rate_func=linear)
        self.finish()


class S07Reveal(SpokenScene):
    def construct(self):
        world_start(self)
        lab = Lab(self, co2=0.3, L=4.0, on=1.0, p=1.0, cap=4.5)
        meter = Meter(self, 0.0)
        lab.add_to(self)
        self.add(meter.mobs, meter.fill, meter.needle)
        meter.link(lab)
        self.add(meter.m)
        items, pts, ln = graph_base(self, lab)
        ext = x_ext()
        qm = T("?", 90, GOLD, weight=BOLD).move_to(P(5.2, -1.6))
        self.add(ext, qm)
        lab.trial(self, 5.0, run=0.5, move=0.3)
        self.play(FadeOut(qm), run_time=0.2)
        p5 = drop_point(self, 5, 4.5, 0.4)
        lab.trial(self, 6.0, run=0.5, move=0.3)
        p6 = drop_point(self, 6, 4.5, 0.4)
        self.at("brighter light now changes almost nothing")
        flat = curve(4, 8, 4.5)
        self.play(Create(curve(4.5, 8, 4.5)), ReplacementTransform(ext, x_axis(8.0).set_opacity(1)), run_time=1.5)
        self.at("the discs are running short of carbon dioxide")
        g = co2_gauge(lab)
        self.add(g)
        self.play(FadeIn(g, shift=UP * 0.2), run_time=0.6)
        self.play(lab.co2.animate.set_value(0.1), run_time=2.4)
        self.at("carbon dioxide has become the slow worker")
        worker = VGroup(Circle(radius=0.22, stroke_color=BLUE, stroke_width=4, fill_color=BLUE, fill_opacity=0.5).move_to(P(5.7, -0.05)),
                        RoundedRectangle(corner_radius=0.1, width=0.5, height=0.75, stroke_color=BLUE, stroke_width=4, fill_color=BLUE, fill_opacity=0.3).move_to(P(5.7, -0.6)))
        wl = chip("carbon dioxide", BLUE, 26).move_to(P(5.1, 0.55))
        pk = VGroup(*[Square(0.26, stroke_width=0, fill_color=YELLOW, fill_opacity=0.95).move_to(P(3.2 + 0.4 * k, -0.3)) for k in range(6)])
        self.play(FadeIn(worker, shift=LEFT * 0.2), FadeIn(wl), run_time=0.8)
        self.play(LaggedStart(*[FadeIn(s, shift=RIGHT * 0.3) for s in pk], lag_ratio=0.2), run_time=1.4)
        for i, s in enumerate(pk):
            s.add_updater(lambda m, dt, i=i: m.set_y(-0.3 + 0.04 * np.sin(3 * self.clock.get_value() + i)))
        self.at("and the whole process waits for it")
        self.wait(1.5)
        self.finish()


def lab_fade_in(sc, lab, meter, **kw):
    lab.add_to(sc, **kw)
    sc.add(meter.mobs, meter.fill, meter.needle)


class S08Term(SpokenScene):
    def construct(self):
        world_start(self)
        meter = Meter(self, 0.57)
        self.add(meter.mobs, meter.fill, meter.needle)
        meter.tw.set_value(0.0)
        xa, ya, xl, gt = x_axis(8.0), y_axis(), x_label(), graph_tag()
        self.add(xa, ya, xl, gt, *[gpoint(L, 4.5) for L in range(1, 7)], curve(1, 8, 4.5))
        defn = T("an input or condition\nthat holds a process\nback", 34, TEXT, line_spacing=1.0)
        title = T("limiting factor", 46, GOLD, weight=BOLD)
        card = VGroup(title, defn).arrange(DOWN, buff=0.4).move_to(P(-3.4, 0.2))
        box = SurroundingRectangle(card, color=GOLD, buff=0.35, stroke_width=4, corner_radius=0.15)
        self.play(Create(box), FadeIn(defn), run_time=1.4)
        self.at("limiting factor")
        self.play(FadeIn(title, shift=DOWN * 0.15), run_time=0.8)
        self.at("on the rising part of this curve")
        rise = curve(0, 4.5, 4.5, YELLOW, 11)
        self.play(Create(rise), run_time=1.2)
        self.at("it was light")
        t1 = T("limit: light", 30, YELLOW, weight=BOLD).move_to(P(2.0, -0.3))
        self.play(FadeIn(t1, shift=UP * 0.15), run_time=0.6)
        self.at("on the flat part")
        fl = curve(4.5, 8, 4.5, BLUE, 11)
        self.play(Create(fl), FadeOut(rise), run_time=1.2)
        self.at("it is carbon dioxide")
        t2 = T("limit: carbon\ndioxide", 30, BLUE, weight=BOLD, line_spacing=0.9).move_to(P(5.1, 0.3))
        self.play(FadeIn(t2, shift=UP * 0.15), run_time=0.6)
        self.finish()


class S09MoreSoda(SpokenScene):
    def construct(self):
        world_start(self)
        lab = Lab(self, co2=0.1, L=6.0, on=1.0, p=1.0, cap=4.5)
        meter = Meter(self, 0.0)
        meter.link(lab)
        self.add(meter.m)
        xa, ya, xl, gt = x_axis(8.0), y_axis(), x_label(), graph_tag()
        self.add(xa, ya, xl, gt, *[gpoint(L, 4.5) for L in range(1, 7)])
        c1 = curve(1, 8, 4.5)
        self.add(c1)
        self.play(FadeIn(VGroup(lab.static)), FadeIn(meter.mobs), run_time=0.8)
        self.add(lab.dots, lab.disks, lab.lamp, meter.fill, meter.needle)
        self.at("add more baking soda")
        spoon = VGroup(RoundedRectangle(corner_radius=0.12, width=1.1, height=0.4, stroke_color=GREY, stroke_width=3, fill_color=GREY, fill_opacity=0.5),
                       Line(P(0.55, 0), P(1.5, 0.6), stroke_color=GREY, stroke_width=6)).move_to(P(-5.5, 0.9)).rotate(-0.4)
        bl = T("more baking soda", 26, WHITE).move_to(P(-6.6, 2.5), aligned_edge=LEFT)
        grains = VGroup(*[Dot(P(-4.9 + 0.1 * k, 0.6), radius=0.06, color=WHITE) for k in range(12)])
        self.add(grains)
        self.play(FadeIn(spoon), FadeIn(bl), run_time=0.5)
        g = co2_gauge(lab)
        self.add(g)
        self.play(grains.animate.shift(DOWN * 1.2).set_opacity(0), lab.co2.animate.set_value(0.9), lab.cap.animate.set_value(6.5), run_time=1.5)
        self.play(FadeOut(VGroup(spoon, bl)), run_time=0.2)
        self.at("now the curve climbs higher")
        self.play(c1.animate.set_stroke(opacity=0.3), lab.L.animate.set_value(7.0), run_time=0.5)
        c2 = curve(4.5, 8, 6.5, TEXT, 7)
        self.play(Create(c2), run_time=2.0)
        c2full = curve(1, 8, 6.5, TEXT, 7)
        self.at("something else such as temperature")
        tg = T("temperature or\nenzyme speed\nsets this new ceiling", 22, TEXT, line_spacing=0.9).move_to(P(3.7, -1.9), aligned_edge=LEFT)
        self.play(FadeIn(tg, shift=DOWN * 0.15), run_time=0.8)
        self.at("now sets a new ceiling")
        self.play(Indicate(tg, color=GOLD, scale_factor=1.05), run_time=1.0)
        self.at("when a curve is flat")
        flatseg = curve(6.5, 8, 6.5, GOLD, 11)
        self.play(Create(flatseg), run_time=0.7)
        self.play(lab.L.animate.set_value(7.9), run_time=1.2)
        self.at("more of that factor barely changes the rate")
        self.play(lab.L.animate.set_value(7.0), run_time=1.0)
        self.play(lab.L.animate.set_value(7.9), run_time=1.0)
        self.finish()


class S10Bay(SpokenScene):
    def construct(self):
        world_start(self)
        meter = Meter(self, 0.7)
        bay = Bay(self)
        meter.link(bay)
        self.add(meter.m)
        self.add(meter.mobs, meter.fill, meter.needle)
        self.at("chesapeake bay")
        outline, low, sch = bay_map()
        name = T("Chesapeake Bay", 28, TEXT).move_to(P(-6.7, 2.4), aligned_edge=LEFT)
        self.play(Create(outline), FadeIn(name), FadeIn(sch), run_time=2.0)
        self.at("underwater grasses grow on the bottom")
        dot = Dot(P(-3.05, -2.0), radius=0.14, color=GOLD)
        self.add(dot)
        self.play(FadeIn(bay.static), run_time=0.8)
        self.add(bay.rays, bay.blades, bay.parts)
        self.play(Indicate(dot, color=GOLD, scale_factor=2.0), run_time=0.8)
        self.at("most eelgrass")
        eg = T("eelgrass", 32, GREEN, weight=BOLD).move_to(P(1.4, 0.8))
        self.play(FadeIn(eg, shift=UP * 0.15), run_time=0.7)
        self.at("lower bay")
        self.play(FadeIn(low), run_time=1.0)
        self.at("saltier")
        sl = T("saltier water", 30, TEAL, weight=BOLD).move_to(P(-6.7, -1.8), aligned_edge=LEFT)
        self.play(FadeIn(sl, shift=RIGHT * 0.2), run_time=0.7)
        self.finish()


class S11Murk(SpokenScene):
    def construct(self):
        world_start(self)
        meter = Meter(self, 0.7)
        bay = Bay(self, rays_on=0.0)
        meter.link(bay)
        self.add(meter.m)
        self.add(meter.mobs, meter.fill, meter.needle)
        bay.add_to(self)
        lt = T("light from\nthe surface", 30, YELLOW, line_spacing=0.9).move_to(P(-4.6, 2.2))
        self.play(FadeIn(lt), bay.rays_on.animate.set_value(1.0), run_time=2.2)
        self.at("mud and floating algae block it")
        ml = T("mud", 30, SOIL, weight=BOLD).move_to(P(-4.6, 0.8))
        self.play(FadeIn(ml), bay.mud.animate.set_value(1.0), bay.turb.animate.set_value(0.4), run_time=1.0)
        self.at("algae")
        al = T("floating algae", 30, ALGAE, weight=BOLD).move_to(P(-4.6, -0.3))
        self.play(FadeIn(al), bay.alg.animate.set_value(1.0), bay.turb.animate.set_value(0.8), run_time=1.0)
        self.at("so does material growing on the leaves")
        cl = T("growth on\nthe leaves", 30, COATC, weight=BOLD, line_spacing=0.9).move_to(P(-4.6, -1.7))
        self.play(FadeIn(cl), bay.coat.animate.set_value(1.0), bay.turb.animate.set_value(1.1), run_time=1.6)
        self.finish()


class S12Target(SpokenScene):
    def construct(self):
        world_start(self)
        meter = Meter(self, 0.75)
        bay = Bay(self)
        meter.link(bay)
        self.add(meter.m)
        self.add(meter.mobs, meter.fill, meter.needle)
        bay.add_to(self)
        self.at("there is a habitat target")
        gg = light_gauge(bay)
        tl = target_line()
        gl = T("light at\nthe grass", 24, YELLOW, line_spacing=0.9).move_to(P(-3.5, 1.5))
        self.play(FadeIn(gg), Create(tl), FadeIn(gl), run_time=1.2)
        self.at("more than 22")
        tt = T("target: more than\n22% of surface light", 28, TEXT, line_spacing=0.9).move_to(P(-6.7, -1.35), aligned_edge=LEFT)
        self.play(FadeIn(tt, shift=UP * 0.15), run_time=0.8)
        self.at("of the light at the surface")
        self.play(Indicate(bay.rays, color=GOLD, scale_factor=1.0), run_time=1.0)
        self.at("reach the grass")
        self.play(Indicate(gg, color=GOLD, scale_factor=1.1), run_time=1.0)
        self.at("when murky water cuts the light")
        self.play(bay.mud.animate.set_value(1.0), bay.alg.animate.set_value(1.0), bay.turb.animate.set_value(1.0), run_time=2.4)
        self.at("light can become the limiting factor")
        lim = T("limit: light", 34, YELLOW, weight=BOLD).move_to(P(-4.6, 0.6))
        self.play(FadeIn(lim, shift=UP * 0.15), run_time=0.6)
        # tiny inset of the rate curve, low rising part lit
        ox, oy = -6.5, 2.0
        ax = VGroup(Line(P(ox, oy), P(ox + 2.6, oy), stroke_color=GREY, stroke_width=3), Line(P(ox, oy), P(ox, oy + 1.6), stroke_color=GREY, stroke_width=3))
        full = VMobject(stroke_color=TEXT, stroke_width=4)
        full.set_points_as_corners([P(ox + 0.35 * L, oy + 0.2 * rate(L, 4.5)) for L in np.linspace(0, 7, 40)])
        low = VMobject(stroke_color=YELLOW, stroke_width=8)
        low.set_points_as_corners([P(ox + 0.35 * L, oy + 0.2 * rate(L, 4.5)) for L in np.linspace(0, 2.2, 14)])
        self.play(FadeIn(ax), Create(full), run_time=0.8)
        self.play(Create(low), run_time=0.6)
        self.finish()


class S13Rule(SpokenScene):
    def construct(self):
        world_start(self)
        lab = Lab(self, co2=0.1, L=6.0, on=1.0, p=1.0, cap=4.5)
        meter = Meter(self, 0.0)
        meter.link(lab)
        self.add(meter.m)
        bay = Bay(self)
        lab.add_to(self)
        g = co2_gauge(lab)
        self.add(g)
        bay.add_to(self)
        self.add(meter.mobs, meter.fill, meter.needle)
        ct = T("cup: other conditions\nheld fixed", 24, TEXT, line_spacing=0.9).move_to(P(-6.7, 3.2), aligned_edge=LEFT)
        bt = T("bay: light can limit", 26, YELLOW).move_to(P(1.4, 3.45))
        cover = Rectangle(width=BX1 - BX0 + 0.1, height=7.4, stroke_width=0, fill_color=BG, fill_opacity=0.72).move_to(P((BX0 + BX1) / 2, 0))
        cover_l = Rectangle(width=5.4, height=7.8, stroke_width=0, fill_color=BG, fill_opacity=0.0).move_to(P(-4.1, 0))
        self.add(cover, cover_l)
        self.play(FadeIn(ct), run_time=0.8)
        self.at("carbon dioxide capped the rate")
        self.play(Indicate(g, color=GOLD, scale_factor=1.05), run_time=1.0)
        self.at("in the bay")
        self.play(FadeOut(cover), cover_l.animate.set_fill(BG, 0.72), run_time=0.5)
        self.at("murky water can make")
        self.play(bay.mud.animate.set_value(1.0), bay.alg.animate.set_value(1.0), bay.turb.animate.set_value(1.0), run_time=1.3)
        self.at("light the limit")
        self.play(FadeIn(bt), run_time=0.6)
        self.at("real plants can face two limits at once")
        self.play(cover_l.animate.set_fill(BG, 0.0), run_time=0.6)
        two = T("two factors can limit at once", 26, TEXT).move_to(P(0.0, -3.65))
        self.play(FadeIn(two, shift=UP * 0.1), run_time=0.6)
        self.at("a flat curve means")
        self.play(lab.L.animate.set_value(7.8), run_time=1.5)
        self.at("no longer helping much")
        self.play(lab.co2.animate.set_value(0.8), lab.cap.animate.set_value(6.5), run_time=2.0)
        self.finish()


class S14End(EndCard):
    LINE = "One or more limiting factors cap how fast photosynthesis runs."
