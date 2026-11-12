"""Keeping the Gas Fresh (gas exchange, film 2).

COLOUR MAP (same as film 1)
  air = BLUE         blood = RED         oxygen = GOLD         carbon dioxide = PURPLE
  barrier / airway outline = GREY       dead-space air = PALE GREY       fresh air reaching the sac = bright BLUE
The sac, tube and capillary ring are film 1's alveolus (sac centre 0,-0.6; radius 2.2), carried through the film.
Breath animation is a one-dimensional column of gas pushed down the tube; sizes are schematic.
"""
import math
import random
import numpy as np
from bp_style import *  # noqa: F401,F403

PALE = "#C9CED6"
MIXED = "#A5B4C6"
CX, CY, R = 0.0, -0.6, 2.2
TT = 3.55          # top of the tube (mouth)
VD = 6             # dead-space volume in dots
SP = 0.27          # tube length per dot
DEEP_VT, DEEP_PERIOD = 24, 5.0
SHAL_VT, SHAL_PERIOD = 9, 1.875


def clock(scene):
    tr = ValueTracker(0)
    tr.add_updater(lambda m, dt: m.increment_value(dt))
    scene.add(tr)
    return tr


def lab(text, x, y, size=28, color=TEXT, **kw):
    return T(text, size, color, **kw).move_to([x, y, 0])


def ml(lines, x, y, size=28, color=TEXT, gap=0.5):
    """Several centred label lines stacked downward from y."""
    return VGroup(*[lab(t, x, y - i * gap, size, color) for i, t in enumerate(lines)])


def march(p0, p1, color=BLUE, n=5, speed=0.8, r=0.07, op=1.0):
    p0 = np.array(p0, float)
    p1 = np.array(p1, float)
    L = max(np.linalg.norm(p1 - p0), 1e-3)
    g = VGroup(*[Dot(radius=r, color=color) for _ in range(n)])
    for i, d in enumerate(g):
        d.s = i / n

    def upd(m, dt):
        for d in m:
            d.s = (d.s + dt * speed / L) % 1
            d.move_to(p0 + (p1 - p0) * d.s)
            d.set_opacity(op * min(1, d.s * 6, (1 - d.s) * 6))
    g.add_updater(upd)
    upd(g, 0)
    return g


def gauge(x, y0, h, color, src, w=0.42):
    box = Rectangle(width=w, height=h, stroke_color=GREY, stroke_width=3).move_to([x, y0 + h / 2, 0])
    fill = Rectangle(width=w - 0.08, height=0.01, stroke_width=0, fill_color=color, fill_opacity=0.9)

    def upd(m):
        v = max(0.004, min(1.0, src()))
        m.become(Rectangle(width=w - 0.08, height=v * h, stroke_width=0, fill_color=color, fill_opacity=0.9).move_to([x, y0 + v * h / 2, 0]))
    fill.add_updater(upd)
    upd(fill)
    g = VGroup(box, fill)
    g.x, g.y0, g.h = x, y0, h
    return g


def hbar(x, y, w, color, src, label, size=28, h=0.38):
    """Horizontal counter: label above, track below it, fill tied to src (0..1)."""
    lb = lab(label, x, y + 0.5, size, color)
    track = Rectangle(width=w, height=h, stroke_color=GREY, stroke_width=3).move_to([x, y, 0])
    fill = Rectangle(width=0.01, height=h - 0.08, stroke_width=0, fill_color=color, fill_opacity=0.85)

    def upd(m):
        v = max(0.004, min(1.0, src()))
        m.become(Rectangle(width=(w - 0.08) * v, height=h - 0.08, stroke_width=0, fill_color=color, fill_opacity=0.85).move_to([x - w / 2 + 0.04 + (w - 0.08) * v / 2, y, 0]))
    fill.add_updater(upd)
    upd(fill)
    return VGroup(lb, track, fill)


def smooth01(u):
    u = max(0.0, min(1.0, u))
    return u * u * (3 - 2 * u)


# ------------------------------------------------------------------ the carried world: sac, tube, gas column
def sac(cx=CX, cy=CY, R_=R):
    gap = math.asin(0.4 / R_)
    ring = Arc(radius=R_, start_angle=PI / 2 + gap, angle=TAU - 2 * gap, arc_center=[cx, cy, 0], color=GREY, stroke_width=14)
    tube = VGroup(Line([cx - 0.4, cy + R_ * math.cos(gap), 0], [cx - 0.4, TT, 0], color=GREY, stroke_width=14),
                  Line([cx + 0.4, cy + R_ * math.cos(gap), 0], [cx + 0.4, TT, 0], color=GREY, stroke_width=14))
    pool = Circle(radius=R_ - 0.17, stroke_width=0, fill_color=BLUE, fill_opacity=0.13).move_to([cx, cy, 0])
    return ring, tube, pool


class Airway(VGroup):
    """A column of gas dots pushed down the tube by tracker z (units of dots).
    auto=True: z follows a breathing rhythm (amplitude vt, period seconds); else the scene drives z."""

    def __init__(self, ck, auto=False, vt=DEEP_VT, period=DEEP_PERIOD):
        super().__init__()
        self.ck = ck
        self.z = ValueTracker(0.0)
        self.vt = ValueTracker(vt)
        self.period = ValueTracker(period)
        self.auto = auto
        self.phase = 0.0
        self.vt_eff = float(vt)
        rng = random.Random(11)
        dots = []
        for k in range(VD):
            d = Dot(radius=0.095, color=PALE)
            d.s0, d.base = float(k), ManimColor(PALE)
            dots.append(d)
        for k in range(1, 25):
            d = Dot(radius=0.095, color=BLUE)
            d.s0, d.base = -float(k), ManimColor(BLUE)
            dots.append(d)
        for i, d in enumerate(dots):
            d.lane = -0.14 if i % 2 == 0 else 0.14
            r = 1.65 * math.sqrt(rng.random())
            a = rng.random() * TAU
            d.anc = np.array([CX + r * math.cos(a), CY + r * math.sin(a), 0.0])
            d.ph = rng.random() * TAU
            d.maxs = d.s0
        self.add(*dots)
        self.add_updater(lambda m, dt: m._step(dt))
        self._step(0)

    def vent_frac(self):
        return max(0.0, 1.0 - VD / max(self.vt_eff, VD + 0.01))

    def _step(self, dt):
        if self.auto:
            tgt = self.vt.get_value()
            self.vt_eff += (tgt - self.vt_eff) * min(1.0, dt * 2.5)
            self.phase += dt / self.period.get_value()
            self.z.set_value(self.vt_eff * (0.5 - 0.5 * math.cos(TAU * self.phase)))
        z = self.z.get_value()
        t = self.ck.get_value()
        reset = z < 0.2
        for d in self.submobjects:
            if reset:
                d.maxs = d.s0
            s = d.s0 + z
            d.maxs = max(d.maxs, s)
            f = 0.0 if d.maxs <= VD + 0.5 else max(0.0, min(1.0, (d.maxs - s) / 2.0))
            col = interpolate_color(d.base, ManimColor(MIXED), f)
            if s < 0:
                pos = np.array([CX + d.lane, TT - 0.15 - s * SP, 0.0])
                op = max(0.0, min(1.0, s + 1.0))
            elif s <= VD:
                pos = np.array([CX + d.lane, TT - 0.15 - s * SP, 0.0])
                op = 1.0
            else:
                u = smooth01((s - VD) / 2.0)
                a = np.array([CX + d.lane, TT - 0.15 - VD * SP, 0.0])
                b = d.anc + 0.09 * np.array([math.sin(0.9 * t + d.ph), math.cos(1.1 * t + d.ph), 0.0])
                pos = a + (b - a) * u
                op = 1.0
            d.move_to(pos)
            d.set_fill(col, opacity=op)


def co2_dots(ck, pco, n=44, seed=5):
    """Purple dots in the sac: density follows the PCO2 tracker."""
    rng = random.Random(seed)
    g = VGroup(*[Dot(radius=0.075, color=PURPLE) for _ in range(n)])
    for d in g:
        r = 1.75 * math.sqrt(rng.random())
        a = rng.random() * TAU
        d.anc = np.array([CX + r * math.cos(a), CY + r * math.sin(a), 0.0])
        d.thr = rng.random()
        d.ph = (rng.random() * TAU, rng.random() * TAU)
        d.w = (0.7 + rng.random(), 0.7 + rng.random())

    def upd(m):
        t = ck.get_value()
        for d in m:
            d.move_to(d.anc + 0.12 * np.array([math.sin(d.w[0] * t + d.ph[0]), math.cos(d.w[1] * t + d.ph[1]), 0]))
            d.set_fill(PURPLE, opacity=1.0 if d.thr < pco.get_value() else 0.0)
    g.add_updater(upd)
    upd(g)
    return g


RR = R + 0.42


def ring_pt(a):
    gap = 0.42
    th = PI / 2 + gap + a * (TAU - 2 * gap)
    return np.array([CX + RR * math.cos(th), CY + RR * math.sin(th), 0.0])


def cap_ring(ck, color=RED, speed=0.1, n=22, thr=None, op=0.4):
    """Capillary round the sac; dots circulate. thr=pco tracker makes it a CO2 carrier (purple dots, density follows thr)."""
    gap = 0.42
    arc = Arc(radius=RR, start_angle=PI / 2 + gap, angle=TAU - 2 * gap, arc_center=[CX, CY, 0], color=RED, stroke_width=16).set_fill(opacity=0).set_stroke(opacity=op)
    dots = VGroup(*[Dot(radius=0.09, color=(PURPLE if thr is not None else RED)) for _ in range(n)])
    for i, d in enumerate(dots):
        d.a = i / n
        d.thr = (i * 0.618) % 1.0

    def upd(m, dt):
        for d in m:
            d.a = (d.a + dt * speed) % 1.0
            d.move_to(ring_pt(d.a))
            vis = 1.0 if (thr is None or d.thr < thr.get_value()) else 0.0
            d.set_fill(PURPLE if thr is not None else RED, opacity=vis * min(1, d.a * 8, (1 - d.a) * 8))
    dots.add_updater(upd)
    upd(dots, 0)
    return VGroup(arc, dots)


def pour(ck, n=7, speed=0.35, seed=2):
    """Purple dots leaving the capillary ring into the sac, at a constant rate."""
    rng = random.Random(seed)
    g = VGroup(*[Dot(radius=0.09, color=PURPLE) for _ in range(n)])
    for i, d in enumerate(g):
        d.s = i / n
        d.ang = PI * 0.15 + rng.random() * TAU * 0.8 + 0.2
        d.ang = (d.ang if d.ang < PI / 2 - 0.5 or d.ang > PI / 2 + 0.5 else d.ang + 1.1)
        d.rr = 0.3 + 0.8 * rng.random()

    def upd(m, dt):
        for d in m:
            d.s = (d.s + dt * speed) % 1.0
            a, b = np.array([CX + RR * math.cos(d.ang), CY + RR * math.sin(d.ang), 0.0]), np.array([CX + d.rr * math.cos(d.ang), CY + d.rr * math.sin(d.ang), 0.0])
            d.move_to(a + (b - a) * d.s)
            d.set_fill(PURPLE, opacity=min(1, d.s * 6, (1 - d.s) * 4))
    g.add_updater(upd)
    upd(g, 0)
    return g


def world(scene, ck, auto=True, vt=DEEP_VT, period=DEEP_PERIOD):
    ring, tube, pool = sac()
    A = Airway(ck, auto=auto, vt=vt, period=period)
    scene.add(pool, ring, tube, A)
    return A, ring, tube, pool


def person(cx, cy=0.0, k=1.0, pulse=None, color=TEXT):
    head = Circle(radius=0.55 * k, stroke_color=color, stroke_width=4, fill_color=GREY, fill_opacity=0.25).move_to([cx, cy + 1.95 * k, 0])
    body = RoundedRectangle(corner_radius=0.45 * k, width=1.7 * k, height=2.9 * k, stroke_color=color, stroke_width=4, fill_color=GREY, fill_opacity=0.2).move_to([cx, cy - 0.15 * k, 0])
    g = VGroup(body, head)
    if pulse is not None:
        base = body.get_center().copy()
        sy = body.height

        def upd(m):
            m.become(RoundedRectangle(corner_radius=0.45 * k, width=1.7 * k * (1 + 0.06 * (0.5 + 0.5 * math.sin(pulse.get_value() * 2.4))), height=sy, stroke_color=color, stroke_width=4, fill_color=GREY, fill_opacity=0.2).move_to(base))
        body.add_updater(upd)
    return g


# =================================================================== scenes
class S00Title(TitleCard):
    LESSON = "Gas Exchange and Breathing"
    TITLE = "Keeping the Gas Fresh"


class S01Question(SpokenScene):
    def construct(self):
        ck = clock(self)
        pL, pR = -3.9, 2.5
        P1 = person(pL, -0.2, 1.0, ck)
        P2 = person(pR, -0.2, 1.0, ck)
        self.play(FadeIn(P1), FadeIn(P2), run_time=1.0)
        c1 = lab("air moved: 6 L per minute", pL + 0.9, 3.3, 28, BLUE)
        c2 = lab("air moved: 6 L per minute", pR + 0.9, 3.3, 28, BLUE)
        a1 = march([pL, 1.3, 0], [pL, 0.1, 0], BLUE, n=3, speed=0.5)
        a2 = march([pR, 1.3, 0], [pR, 0.1, 0], BLUE, n=3, speed=0.5)
        self.at("same total air")
        self.play(FadeIn(c1), FadeIn(c2), run_time=0.9)
        self.add(a1, a2)
        self.at("So why is one")
        q = chip("Same air moved. Why more carbon dioxide?", GOLD, size=36)
        q = fit(q, max_w=12.4).move_to([0, -3.2, 0])
        self.play(FadeIn(q, shift=UP * 0.2), run_time=0.8)
        t1, t2 = ValueTracker(0.0), ValueTracker(0.0)
        g1 = gauge(pL + 1.9, -2.0, 3.6, PURPLE, lambda: 0.2 + 0.03 * math.sin(2 * ck.get_value()) * 0.0 + 0.0 * t1.get_value())
        g2 = gauge(pR + 1.9, -2.0, 3.6, PURPLE, lambda: 0.2 + 0.7 * t2.get_value())
        gl = VGroup(lab("PCO2", pL + 1.9, 1.9, 30, PURPLE), lab("PCO2", pR + 1.9, 1.9, 30, PURPLE))
        self.play(FadeIn(g1), FadeIn(g2), FadeIn(gl), run_time=0.8)
        self.at("building up")
        self.play(t2.animate.set_value(1.0), run_time=1.5, rate_func=linear)
        self.at("while the other")
        self.play(Indicate(g1, color=PURPLE, scale_factor=1.12), run_time=1.2)
        self.finish()


class S02Link(SpokenScene):
    def construct(self):
        ck = clock(self)
        ring, tube, pool = sac()
        stale = VGroup(*[Dot(radius=0.07, color=BLUE) for _ in range(20)])
        rng = random.Random(3)
        for d in stale:
            r = 1.6 * math.sqrt(rng.random())
            a = rng.random() * TAU
            d.anc = np.array([CX + r * math.cos(a), CY + r * math.sin(a), 0.0])
            d.ph = rng.random() * TAU
        gasv = ValueTracker(1.0)

        def su(m):
            t = ck.get_value()
            for d in m:
                d.move_to(d.anc + 0.14 * np.array([math.sin(0.9 * t + d.ph), math.cos(1.1 * t + d.ph), 0]))
                d.set_fill(BLUE, opacity=0.55 * gasv.get_value())
        stale.add_updater(su)
        su(stale)
        self.play(FadeIn(pool), Create(ring), Create(tube), run_time=1.6)
        self.add(stale)
        self.at("alveolus")
        al = lab("alveolus", -4.1, CY, 34)
        self.play(FadeIn(al), run_time=0.8)
        self.at("Blood can at best")
        cap = cap_ring(ck, speed=0.07)
        lvl = ValueTracker(0.0)
        ga = gauge(3.9, -2.6, 3.8, GOLD, lambda: 0.62 * gasv.get_value())
        gb = gauge(5.7, -2.6, 3.8, RED, lambda: 0.62 * lvl.get_value())
        gl = VGroup(lab("sac gas", 3.9, -2.95, 28), lab("blood out", 5.7, -2.95, 28))
        line = DashedLine([3.5, -2.6 + 3.8 * 0.62, 0], [6.2, -2.6 + 3.8 * 0.62, 0], color=TEXT, stroke_width=3)
        self.play(FadeIn(cap), FadeIn(ga), FadeIn(gb), FadeIn(gl), FadeIn(line), run_time=1.0)
        self.play(lvl.animate.set_value(1.0), run_time=2.0)
        self.at("keeps bringing new blood")
        bl = ml(["blood flow renews", "the blood"], -4.6, 2.2, 28, RED)
        self.play(FadeIn(bl), run_time=0.8)
        self.at("But the gas must be renewed")
        gl2 = ml(["the gas must be", "renewed too"], -4.5, -1.6, 28, BLUE)
        self.play(FadeIn(gl2), gasv.animate.set_value(0.35), run_time=2.0)
        self.at("through the airways")
        a_in = march([CX - 0.2, TT, 0], [CX - 0.2, CY + R - 0.3, 0], BLUE, n=4, speed=0.9, r=0.08)
        self.add(a_in)
        self.play(Indicate(tube, color=BLUE, scale_factor=1.05), run_time=1.2)
        self.at("So what keeps")
        self.play(FadeOut(VGroup(ga, gb, gl, line, bl, gl2)), run_time=0.6)
        qq = ml(["blood matches", "the gas it last", "touches: what", "keeps that gas", "fresh?"], 4.75, 1.9, 30, GOLD, gap=0.58)
        self.play(FadeIn(qq), gasv.animate.set_value(0.9), run_time=1.0)
        self.finish()


def chest_parts(cx=-1.2):
    """Torso (width driven by tracker w), lung and diaphragm (driven by tracker d)."""
    d, w = ValueTracker(0.0), ValueTracker(0.0)
    torso = RoundedRectangle(corner_radius=0.5, width=4.4, height=5.4, stroke_color=TEXT, stroke_width=4, fill_color=GREY, fill_opacity=0.2).move_to([cx, -0.7, 0])

    def tw(m):
        m.become(RoundedRectangle(corner_radius=0.5, width=4.4 * (1 + 0.12 * w.get_value()), height=5.4, stroke_color=TEXT, stroke_width=4, fill_color=GREY, fill_opacity=0.2).move_to([cx, -0.7, 0]))
    torso.add_updater(tw)

    def dome_y(x):
        u = (x - cx) / 2.2
        dd = d.get_value()
        return (-1.8 - 0.55 * dd) + (0.9 - 0.75 * dd) * (1 - u * u)

    lung = VMobject(stroke_color=BLUE, stroke_width=5, fill_color=BLUE, fill_opacity=0.22)

    def lu(m):
        hw = 1.65 * (1 + 0.1 * w.get_value())
        pts = []
        for t in np.linspace(0, PI, 30):
            pts.append([cx + hw * math.cos(t), 0.15 + 1.75 * math.sin(t), 0])
        # left side down, bottom along the diaphragm from left to right, right side up
        pts.append([cx - hw, dome_y(cx - hw), 0])
        for x in np.linspace(cx - hw, cx + hw, 24):
            pts.append([x, dome_y(x), 0])
        pts.append([cx + hw, 0.15, 0])
        m.set_points_as_corners(pts)
    lung.add_updater(lu)

    dome = VMobject(stroke_color=TEXT, stroke_width=10)

    def du(m):
        hw = 2.2 * (1 + 0.12 * w.get_value())
        m.set_points_as_corners([[x, dome_y(x), 0] for x in np.linspace(cx - hw, cx + hw, 40)])
    dome.add_updater(du)
    for m_ in (torso, lung, dome):
        m_.update()
    return d, w, torso, lung, dome


class S03Aspiration(SpokenScene):
    def construct(self):
        ck = clock(self)
        cx = -1.2
        d, w, torso, lung, dome = chest_parts(cx)
        trach = Line([cx, 3.7, 0], [cx, 1.8, 0], color=GREY, stroke_width=18)
        self.play(FadeIn(torso), FadeIn(lung), FadeIn(trach), run_time=1.2)
        self.add(dome)
        idle = VGroup(*[Dot(radius=0.06, color=BLUE) for _ in range(14)])
        rng = random.Random(8)
        for dd in idle:
            dd.anc = np.array([cx + rng.uniform(-1.1, 1.1), rng.uniform(-0.4, 1.3), 0.0])
            dd.ph = rng.random() * TAU
        idle.add_updater(lambda m: [x.move_to(x.anc + 0.12 * np.array([math.sin(0.9 * ck.get_value() + x.ph), math.cos(1.1 * ck.get_value() + x.ph), 0])).set_fill(BLUE, opacity=0.4) for x in m] and None)
        self.add(idle)
        self.at("The diaphragm")
        dl = lab("diaphragm", -5.7, -1.6, 28)
        ld = Line([-4.5, -1.6, 0], [-3.4, -1.5, 0], color=TEXT, stroke_width=3)
        self.play(FadeIn(dl), Create(ld), run_time=0.8)
        self.at("contracts and flattens")
        self.play(d.animate.set_value(1.0), run_time=2.4)
        self.at("The chest enlarges")
        arr = VGroup(Arrow([-3.6, 0.2, 0], [-4.3, 0.2, 0], buff=0, color=TEXT, stroke_width=6, tip_length=0.22),
                     Arrow([1.3, 0.2, 0], [2.0, 0.2, 0], buff=0, color=TEXT, stroke_width=6, tip_length=0.22))
        pg_t = ValueTracker(0.0)
        gp = gauge(3.4, -1.5, 3.4, BLUE, lambda: 0.62 - 0.22 * pg_t.get_value(), w=0.8)
        ref = DashedLine([2.6, -1.5 + 3.4 * 0.62, 0], [4.2, -1.5 + 3.4 * 0.62, 0], color=TEXT, stroke_width=4)
        self.play(w.animate.set_value(1.0), FadeIn(arr), run_time=1.6)
        self.at("pressure in the lungs falls")
        refl = ml(["outside air", "pressure"], 5.5, 0.75, 28)
        gl = lab("lung pressure", 3.4, -1.95, 28)
        self.play(FadeIn(gp), FadeIn(ref), FadeIn(refl), FadeIn(gl), pg_t.animate.set_value(1.0), run_time=1.2)
        self.at("and air flows in")
        a_in = march([cx, 3.65, 0], [cx, 1.7, 0], BLUE, n=5, speed=0.9, r=0.09)
        self.add(a_in)
        self.play(FadeOut(arr), run_time=0.6)
        self.at("aspiration")
        asp = lab("aspiration", 4.7, 3.0, 40, GOLD)
        self.play(FadeIn(asp, shift=UP * 0.15), run_time=0.8)
        self.finish()


class S04Deadspace(SpokenScene):
    def construct(self):
        ck = clock(self)
        A, ring, tube, pool = None, None, None, None
        ring, tube, pool = sac()
        A = Airway(ck, auto=False)
        self.play(FadeIn(pool), Create(ring), Create(tube), run_time=1.3)
        self.add(A)
        self.at("sack")
        al = lab("alveoli", 4.0, CY, 34)
        self.play(FadeIn(al), run_time=0.8)
        self.at("The airways")
        self.play(tube.animate.set_color(TEXT), run_time=0.8)
        self.at("from nose and mouth")
        nm = lab("nose and mouth", 2.7, 3.35, 28)
        self.play(FadeIn(nm), run_time=0.8)
        self.at("smallest bronchioles")
        sb = ml(["smallest", "bronchioles"], -2.6, 2.1, 28)
        self.play(FadeIn(sb), run_time=0.8)
        self.at("exchange nothing")
        ne = lab("no exchange", 3.0, 2.3, 30, TEXT)
        self.play(FadeIn(ne), Indicate(A, color=PALE, scale_factor=1.15), run_time=1.2)
        self.at("dead space")
        ds = lab("dead space", 3.0, 1.55, 40, GOLD)
        self.play(FadeIn(ds, shift=UP * 0.1), run_time=0.8)
        self.finish()


class S05Stale(SpokenScene):
    def construct(self):
        ck = clock(self)
        ring, tube, pool = sac()
        A = Airway(ck, auto=False)
        al = lab("alveoli", 4.0, CY, 34)
        ds = lab("dead space", 3.0, 1.55, 40, GOLD)
        self.add(pool, ring, tube, A, al, ds)
        self.wait(0.3)
        self.at("first air into the sac")
        self.play(FadeOut(ds), A.z.animate.set_value(11), run_time=2.4, rate_func=linear)
        self.at("stale air left")
        st = ml(["stale air", "arrives first"], -4.5, 0.3, 30, TEXT)
        self.play(FadeIn(st), A.z.animate.set_value(24), run_time=2.6, rate_func=linear)
        self.at("And fresh air")
        fr = ml(["fresh air still", "in the tube"], -3.0, 2.8, 28, BLUE)
        self.play(FadeIn(fr), FadeOut(st), run_time=0.8)
        self.at("stop breathing in")
        self.play(A.z.animate.set_value(18), run_time=1.0, rate_func=linear)
        self.at("breathed out")
        bo = ml(["breathed out", "unused"], 3.0, 3.1, 30, GOLD)
        self.play(FadeIn(bo), FadeOut(fr), A.z.animate.set_value(0), run_time=1.8, rate_func=linear)
        self.finish()


def counters(scene, A, ck, alv=True, minute_tr=None, alv_tr=None, y0=3.0):
    mf = (lambda: 1.0)
    af = (lambda: A.vent_frac()) if alv_tr is None else (lambda: alv_tr.get_value())
    m = hbar(4.8, y0 - 0.45, 3.4, BLUE, mf, "minute ventilation")
    out = [m]
    if alv:
        a = hbar(4.8, y0 - 1.95, 3.4, BLUE, af, "alveolar ventilation")
        out.append(a)
    return out


class S06Deep(SpokenScene):
    def construct(self):
        ck = clock(self)
        A, ring, tube, pool = world(self, ck, auto=True, vt=DEEP_VT, period=DEEP_PERIOD)
        self.at("Each breath clears")
        l1 = ml(["dead space", "cleared"], -3.4, 2.5, 30, TEXT)
        self.play(FadeIn(l1), run_time=0.8)
        self.at("sends a large")
        l2 = ml(["large fresh", "portion"], -4.3, -0.2, 30, BLUE)
        self.play(FadeIn(l2), FadeOut(l1), run_time=0.8)
        self.at("The total air moved")
        cm = hbar(4.8, 2.55, 3.4, BLUE, lambda: 1.0, "minute ventilation")
        self.play(FadeIn(cm), FadeOut(l2), run_time=0.8)
        self.at("minute ventilation")
        self.play(Indicate(cm, color=BLUE, scale_factor=1.06), run_time=1.0)
        self.at("The fresh part reaching")
        ca = hbar(4.8, 1.05, 3.4, BLUE, lambda: A.vent_frac(), "alveolar ventilation")
        self.play(FadeIn(ca), run_time=0.8)
        self.at("alveolar ventilation")
        self.play(Indicate(ca, color=BLUE, scale_factor=1.06), run_time=1.0)
        self.finish()


def pco_gauge(pco, x=-6.0, show_label=True):
    g = gauge(x, -2.6, 3.4, PURPLE, lambda: pco.get_value())
    lb = lab("PCO2", x, 1.15, 30, PURPLE)
    return VGroup(g, lb), g


class S07Predict(SpokenScene):
    def construct(self):
        ck = clock(self)
        pco = ValueTracker(0.35)
        A, ring, tube, pool = world(self, ck, auto=True, vt=DEEP_VT, period=DEEP_PERIOD)
        co2 = co2_dots(ck, pco)
        cm = hbar(4.8, 2.55, 3.4, BLUE, lambda: 1.0, "minute ventilation")
        self.add(co2, cm)
        pg, g = pco_gauge(pco)
        self.add(pg)
        self.wait(0.6)
        self.at("but take smaller")
        A.vt.set_value(SHAL_VT)
        A.period.set_value(SHAL_PERIOD)
        self.play(Indicate(cm, color=BLUE, scale_factor=1.06), run_time=1.2)
        self.at("Does carbon dioxide")
        cover = Rectangle(width=0.42, height=3.4, stroke_width=0, fill_color=BG, fill_opacity=1.0).move_to([-6.0, -0.9, 0])
        qm = lab("?", -6.0, -0.9, 80, GOLD)
        q = chip("Same total air,\nsmaller breaths:\nalveolar carbon dioxide?", GOLD, size=30)
        q = fit(q, max_w=5.0).move_to([-3.6, 2.6, 0])
        self.play(FadeIn(cover), FadeIn(qm), FadeIn(q, shift=UP * 0.15), run_time=0.9)
        self.finish()


class S08Pause(NarratedScene):
    def construct(self):
        ck = clock(self)
        pco = ValueTracker(0.35)
        A, ring, tube, pool = world(self, ck, auto=True, vt=SHAL_VT, period=SHAL_PERIOD)
        co2 = co2_dots(ck, pco)
        cm = hbar(4.8, 2.55, 3.4, BLUE, lambda: 1.0, "minute ventilation")
        pg, g = pco_gauge(pco)
        cover = Rectangle(width=0.42, height=3.4, stroke_width=0, fill_color=BG, fill_opacity=1.0).move_to([-6.0, -0.9, 0])
        qm = lab("?", -6.0, -0.9, 80, GOLD)
        q = chip("Same total air,\nsmaller breaths:\nalveolar carbon dioxide?", GOLD, size=30)
        q = fit(q, max_w=5.0).move_to([-3.6, 2.6, 0])
        self.add(co2, cm, pg, cover, qm, q)
        ring_ = Circle(radius=0.35, color=GREY, stroke_width=6).move_to([4.8, -2.4, 0])
        tr = ValueTracker(0)
        arc = Arc(radius=0.35, start_angle=PI / 2, angle=0.01, color=GOLD, stroke_width=8, arc_center=[4.8, -2.4, 0])
        arc.add_updater(lambda m: m.become(Arc(radius=0.35, start_angle=PI / 2, angle=-TAU * max(tr.get_value(), 0.01), color=GOLD, stroke_width=8, arc_center=[4.8, -2.4, 0])))
        self.add(ring_, arc)
        self.play(tr.animate.set_value(1), run_time=self.narration_s - 0.2, rate_func=linear)
        self.finish()


class S09Reveal(SpokenScene):
    def construct(self):
        ck = clock(self)
        pco = ValueTracker(0.35)
        A, ring, tube, pool = world(self, ck, auto=True, vt=SHAL_VT, period=SHAL_PERIOD)
        co2 = co2_dots(ck, pco)
        cm = hbar(4.8, 2.55, 3.4, BLUE, lambda: 1.0, "minute ventilation")
        pg, g = pco_gauge(pco)
        cover = Rectangle(width=0.42, height=3.4, stroke_width=0, fill_color=BG, fill_opacity=1.0).move_to([-6.0, -0.9, 0])
        qm = lab("?", -6.0, -0.9, 80, GOLD)
        self.add(co2, cm, pg, cover, qm)
        self.wait(0.2)
        self.play(FadeOut(cover), FadeOut(qm), run_time=0.5)
        # the rise runs alongside the beats below
        pco.add_updater(lambda m, dt: m.set_value(min(0.62, m.get_value() + dt * 0.027)))
        self.at("Each small breath")
        l1 = ml(["mostly stale air,", "a thin fresh sliver"], -3.9, 2.6, 28, TEXT)
        self.play(FadeIn(l1), run_time=0.8)
        self.at("Less fresh air")
        ta = ValueTracker(0.75)
        ca = hbar(4.8, 1.05, 3.4, BLUE, lambda: ta.get_value(), "alveolar ventilation")
        self.play(FadeIn(ca), FadeOut(l1), run_time=0.5)
        self.play(ta.animate.set_value(A.vent_frac()), run_time=1.6)
        self.at("while the body")
        cap = cap_ring(ck, speed=0.07)
        pr = pour(ck)
        pl = ml(["carbon dioxide", "production", "unchanged", "(schematic)"], 4.9, -0.5, 28, PURPLE)
        self.play(FadeIn(cap), FadeIn(pl), run_time=0.8)
        self.add(pr)
        self.finish()


class S10Rule(SpokenScene):
    def construct(self):
        ck = clock(self)
        pco = ValueTracker(0.62)
        A, ring, tube, pool = world(self, ck, auto=True, vt=SHAL_VT, period=SHAL_PERIOD)
        co2 = co2_dots(ck, pco)
        cap = cap_ring(ck, speed=0.07)
        pr = pour(ck)
        self.add(co2, cap, pr)
        self.at("first film's rule")
        r1 = ml(["the first film's", "rule, in reverse"], 4.8, 2.9, 30, GOLD)
        self.play(FadeIn(r1), run_time=0.8)
        self.at("Blood giving up")
        self.play(FadeOut(cap), run_time=0.5)
        cap2 = cap_ring(ck, speed=0.07, thr=pco)
        self.add(cap2)
        self.play(FadeIn(cap2[0]), run_time=0.6)
        self.at("leaves with no lower")
        gs = gauge(-6.0, -2.6, 3.4, PURPLE, lambda: pco.get_value())
        gb = gauge(-4.2, -2.6, 3.4, PURPLE, lambda: pco.get_value() + 0.04)
        gl = VGroup(lab("PCO2", -5.1, 1.15, 30, PURPLE), lab("sac gas", -6.0, -3.0, 28), lab("blood out", -4.2, -3.0, 28, RED))
        self.play(FadeIn(gs), FadeIn(gb), FadeIn(gl), run_time=0.8)
        self.at("than the gas it last touched")
        link = DashedLine([-5.8, 0, 0], [-4.4, 0, 0], color=TEXT, stroke_width=4)
        link.add_updater(lambda m: m.put_start_and_end_on([-5.82, -2.6 + 3.4 * pco.get_value(), 0], [-4.38, -2.6 + 3.4 * (pco.get_value() + 0.04), 0]))
        self.play(FadeIn(link), run_time=0.8)
        self.at("So the blood's")
        t = ml(["blood leaving tracks", "alveolar PCO2"], 4.8, -0.9, 28, TEXT)
        self.play(FadeIn(t), FadeOut(r1), run_time=0.6)
        self.play(pco.animate.set_value(0.8), run_time=3.2, rate_func=linear)
        self.finish()


class S11Sensor(SpokenScene):
    def construct(self):
        ck = clock(self)
        bs = RoundedRectangle(corner_radius=0.6, width=2.2, height=4.8, stroke_color=TEXT, stroke_width=4, fill_color=GREY, fill_opacity=0.35).move_to([-0.4, -0.2, 0])
        bl = lab("brainstem", -0.25, -0.2, 24)
        self.at("brainstem")
        self.play(FadeIn(bs), FadeIn(bl), run_time=1.0)
        self.at("that result")
        vess = Rectangle(width=1.6, height=5.6, stroke_width=0, fill_color=RED, fill_opacity=0.3).move_to([-5.7, -0.2, 0])
        pt = ValueTracker(0.8)
        vd = VGroup(*[Dot(radius=0.1, color=PURPLE) for _ in range(12)])
        for i, d in enumerate(vd):
            d.s = i / 12
            d.x = -6.2 + 0.2 + (i % 3) * 0.45
        vd.add_updater(lambda m, dt: [setattr(x, "s", (x.s + dt * 0.12) % 1) or x.move_to([x.x, -3.0 + 5.6 * x.s, 0]) for x in m] and None)
        self.play(FadeIn(vess), run_time=0.8)
        self.add(vd)
        self.at("Carbon dioxide")
        wall = Rectangle(width=0.3, height=5.6, stroke_width=0, fill_color=GREY, fill_opacity=0.9).move_to([-4.65, -0.2, 0])
        wl = ml(["blood-brain", "barrier"], -4.9, 3.4, 28, TEXT)
        fluid = Rectangle(width=2.8, height=5.6, stroke_width=0, fill_color=TEAL, fill_opacity=0.12).move_to([-3.05, -0.2, 0])
        self.play(FadeIn(wall), FadeIn(wl), FadeIn(fluid), run_time=0.9)
        self.at("crosses into")
        cross = VGroup(*[Dot(radius=0.09, color=PURPLE) for _ in range(14)])
        rr = random.Random(4)
        for i, d in enumerate(cross):
            d.s = i / 14
            d.yy = rr.uniform(-2.5, 2.3)
        cross.add_updater(lambda m, dt: [setattr(x, "s", (x.s + dt * 0.3) % 1) or x.move_to([-5.0 + 2.3 * x.s, x.yy, 0]) or x.set_fill(PURPLE, opacity=min(1, x.s * 6, (1 - x.s) * 3)) for x in m] and None)
        self.add(cross)
        fl = lab("brain's fluid", -3.05, -3.4, 28, TEAL)
        self.play(FadeIn(fl), run_time=0.8)
        self.at("lowers its pH")
        phv = ValueTracker(0.0)
        gp = gauge(-2.5, -2.2, 3.0, TEAL, lambda: 0.85 - 0.45 * phv.get_value())
        gl = lab("pH", -2.5, 1.1, 30, TEAL)
        self.play(FadeIn(gp), FadeIn(gl), run_time=0.6)
        self.play(phv.animate.set_value(1.0), run_time=2.4)
        self.at("Sensors near")
        sens = VGroup(*[Rectangle(width=0.35, height=0.6, stroke_color=GOLD, stroke_width=3, fill_color=GOLD, fill_opacity=0.1).move_to([-1.5, y, 0]) for y in (1.5, 0.3, -0.9, -2.1)])
        cl = ml(["central", "chemoreceptors"], -0.4, 3.35, 28, GOLD)
        self.play(FadeIn(sens), FadeIn(cl), run_time=0.9)
        self.at("detect the fall")
        self.play(*[s.animate.set_fill(GOLD, opacity=0.9) for s in sens], run_time=0.8)
        self.at("the drive to breathe")
        dia = Arc(radius=1.7, start_angle=PI * 0.15, angle=PI * 0.7, color=TEXT, stroke_width=10, arc_center=[4.4, -3.5, 0])
        dl = lab("diaphragm", 4.4, -3.55, 28)
        arrw = Arrow([0.8, -0.3, 0], [3.5, -1.6, 0], buff=0, color=GOLD, stroke_width=4, tip_length=0.3)
        dr = ml(["drive to", "breathe"], 3.0, 0.9, 30, GOLD)
        self.play(FadeIn(dia), FadeIn(dl), FadeIn(arrw), FadeIn(dr), run_time=0.8)
        self.play(arrw.animate.set_stroke(width=18), run_time=1.6)
        self.finish()


class S12Haldane(SpokenScene):
    def construct(self):
        ck = clock(self)
        sub = person(-5.2, -0.4, 1.0, ck)
        tube = Line([-4.3, 1.6, 0], [1.9, 1.6, 0], color=GREY, stroke_width=18)
        bag = Ellipse(width=2.6, height=2.0, stroke_color=TEXT, stroke_width=4, fill_color=GREY, fill_opacity=0.2).move_to([3.2, 1.6, 0])
        cr = lab("J. S. Haldane and J. G. Priestley, 1905", 0.0, -3.3, 30)
        self.play(FadeIn(sub), FadeIn(cr), run_time=1.0)
        self.play(Create(tube), FadeIn(bag), run_time=0.9)
        out = march([-4.3, 1.6, 0], [1.9, 1.6, 0], BLUE, n=7, speed=1.4, r=0.09)
        self.add(out)
        self.at("last of a forced")
        fillb = Ellipse(width=0.3, height=0.2, stroke_width=0, fill_color=MIXED, fill_opacity=0.8).move_to([3.2, 1.6, 0])
        bt = ValueTracker(0.0)
        fillb.add_updater(lambda m: m.become(Ellipse(width=0.3 + 2.1 * bt.get_value(), height=0.2 + 1.5 * bt.get_value(), stroke_width=0, fill_color=MIXED, fill_opacity=0.8).move_to([3.2, 1.6, 0])))
        self.add(fillb)
        bl = ml(["end of forced breath =", "alveolar sample"], 3.2, 3.2, 28)
        self.play(bt.animate.set_value(1.0), FadeIn(bl), run_time=2.4)
        self.at("In resting subjects")
        self.play(FadeOut(VGroup(sub, tube, bag, out, fillb, bl, cr)), run_time=0.7)
        # two schematic panels
        ca, co = -3.4, 3.6
        c_t, o_t = ValueTracker(0.0), ValueTracker(0.0)
        vA = lambda: 0.12 + 0.75 * smooth01(c_t.get_value() * 1.0)
        vB = lambda: 0.12 + 0.03 * o_t.get_value() + 0.6 * smooth01((o_t.get_value() - 0.9) / 0.1)
        gA = gauge(ca - 1.7, -2.3, 3.4, PURPLE, lambda: 0.40 + 0.12 * min(1, c_t.get_value() * 3), w=0.5)
        oA = gauge(ca + 1.1, -2.3, 3.4, BLUE, vA, w=0.8)
        gB = gauge(co - 1.7, -2.3, 3.4, GOLD, lambda: 0.85 - 0.75 * o_t.get_value(), w=0.5)
        oB = gauge(co + 1.1, -2.3, 3.4, BLUE, vB, w=0.8)
        arA = Arrow([ca - 1.0, -0.6, 0], [ca + 0.2, -0.6, 0], buff=0, color=TEXT, stroke_width=5, tip_length=0.25)
        arB = Arrow([co - 1.0, -0.6, 0], [co + 0.2, -0.6, 0], buff=0, color=TEXT, stroke_width=5, tip_length=0.25)
        tA = ml(["small rise in", "alveolar CO2"], ca - 0.2, 3.1, 28, PURPLE)
        tB = lab("oxygen lowered", co - 0.2, 3.1, 28, GOLD)
        vl = VGroup(lab("ventilation", ca + 1.1, -2.7, 28), lab("ventilation", co + 1.1, -2.7, 28))
        sch = lab("schematic", 0.0, -3.4, 28)
        self.at("a small rise")
        self.play(FadeIn(gA), FadeIn(oA), FadeIn(arA), FadeIn(tA), FadeIn(vl[0]), FadeIn(sch), run_time=1.0)
        self.at("greatly increased")
        self.play(c_t.animate.set_value(1.0), run_time=2.4)
        self.at("Lowering oxygen")
        self.play(FadeIn(gB), FadeIn(oB), FadeIn(arB), FadeIn(tB), FadeIn(vl[1]), run_time=0.6)
        far = DashedLine([co - 2.1, -1.95, 0], [co - 1.2, -1.95, 0], color=TEXT, stroke_width=4)
        fl = lab("falls far", co - 3.0, -1.95, 28)
        self.play(o_t.animate.set_value(0.8), FadeIn(far), FadeIn(fl), run_time=1.3, rate_func=linear)
        self.at("until it fell far")
        self.play(o_t.animate.set_value(1.0), run_time=1.0, rate_func=linear)
        self.finish()


def box(text_lines, x, y, color, w=3.0, h=None, size=28):
    n = len(text_lines)
    h = h or (0.45 + 0.5 * n)
    r = RoundedRectangle(corner_radius=0.14, width=w, height=h, stroke_color=color, stroke_width=3, fill_color=color, fill_opacity=0.14).move_to([x, y, 0])
    t = ml(text_lines, x, y + (n - 1) * 0.25, size, TEXT)
    g = VGroup(r, t)
    g.box = r
    return g


class S13Recap(SpokenScene):
    def construct(self):
        ck = clock(self)
        A = box(["alveolar", "ventilation"], -4.7, 2.3, BLUE)
        B = box(["carbon dioxide", "production", "by the body"], -4.7, 0.3, PURPLE, h=1.7)
        C = box(["alveolar", "PCO2"], -0.2, 1.4, PURPLE, w=2.6)
        D = box(["blood", "PCO2"], 3.9, 1.4, RED, w=2.6)
        E = box(["brainstem", "sensors"], 3.9, -1.0, TEAL, w=2.6)
        F = box(["breathing"], -0.2, -1.0, BLUE, w=2.6, h=0.95)

        def arr(p0, p1, col=TEXT):
            return Arrow(p0, p1, buff=0.05, color=col, stroke_width=5, tip_length=0.25)
        aAC = arr([-3.2, 2.3, 0], [-1.5, 1.7, 0])
        aBC = arr([-3.2, 0.3, 0], [-1.5, 1.1, 0])
        aCD = arr([1.1, 1.4, 0], [2.6, 1.4, 0])
        aDE = arr([3.9, 0.7, 0], [3.9, -0.3, 0])
        aEF = arr([2.6, -1.0, 0], [1.1, -1.0, 0])
        aFA = VGroup(Line([-1.5, -1.0, 0], [-6.55, -1.0, 0], color=TEXT, stroke_width=5), Line([-6.55, -1.0, 0], [-6.55, 2.3, 0], color=TEXT, stroke_width=5),
                     Arrow([-6.55, 2.3, 0], [-6.2, 2.3, 0], buff=0, color=TEXT, stroke_width=5, tip_length=0.25))
        self.at("So breathing keeps")
        self.play(FadeIn(A), run_time=0.8)
        self.at("the gas the blood")
        self.play(FadeIn(C), FadeIn(aAC), run_time=0.9)
        fl1 = march([-3.2, 2.3, 0], [-1.5, 1.7, 0], BLUE, n=3, speed=0.5)
        self.add(fl1)
        self.at("a mammals controller")
        self.play(FadeIn(D), FadeIn(aCD), FadeIn(E), FadeIn(aDE), run_time=1.0)
        self.at("mostly reads")
        self.play(Indicate(E[0], color=TEAL, scale_factor=1.08), run_time=1.0)
        fl2 = VGroup(march([1.1, 1.4, 0], [2.6, 1.4, 0], PURPLE, n=3, speed=0.5), march([3.9, 0.7, 0], [3.9, -0.3, 0], PURPLE, n=3, speed=0.5))
        self.add(fl2)
        self.at("That level is the result")
        self.play(FadeIn(F), run_time=0.8)
        self.play(FadeIn(aFA), run_time=1.2)
        self.at("set against")
        self.play(FadeIn(B), FadeIn(aBC), run_time=1.0)
        self.add(march([-3.2, 0.3, 0], [-1.5, 1.1, 0], PURPLE, n=3, speed=0.5))
        self.at("Too little fresh air")
        self.play(Indicate(A[0], color=BLUE, scale_factor=1.1), run_time=1.0)
        self.at("carbon dioxide climbs")
        self.play(Indicate(C[0], color=PURPLE, scale_factor=1.12), Indicate(D[0], color=RED, scale_factor=1.12), run_time=1.4)
        self.at("The sensors then push")
        self.play(FadeIn(aEF), run_time=0.8)
        self.add(march([2.6, -1.0, 0], [1.1, -1.0, 0], TEAL, n=3, speed=0.5))
        self.play(Indicate(F[0], color=BLUE, scale_factor=1.12), run_time=1.2)
        s1 = lab("resting mammal", 0.0, -2.7, 30, GOLD)
        s2 = lab("steady state, breathing ordinary air", 0.0, -3.3, 28)
        self.play(FadeIn(s1), FadeIn(s2), run_time=0.8)
        self.finish()


class S14End(EndCard):
    LINE = "At fixed CO2 output, alveolar ventilation, not total air, sets alveolar PCO2."
