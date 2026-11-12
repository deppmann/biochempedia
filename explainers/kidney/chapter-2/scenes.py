"""Making urine more concentrated than blood: film 2 of the kidney lesson (chapter 2).

COLOUR MAP (same as film 1): blood RED; filtrate and urine YELLOW (a deeper yellow = more concentrated);
salt ORANGE dots; urea small GREY dots; water BLUE drops; tissue a light-to-dark ORANGE wash (darker = more
concentrated); antidiuretic hormone (ADH) is always the GOLD KEY. Everything is a schematic cartoon.
One world: a vertical slice of kidney (cortex, outer medulla, inner medulla, papilla) with the loop of Henle
on the right of centre and the collecting duct on the left. Every scene that continues it rebuilds it in place.
"""
import random
import importlib.util
import numpy as np
from bp_style import *  # noqa: F401,F403

ORANGE = "#F08A3C"
PROT = "#A7AEBB"

# ------------------------------------------------------------------ geometry of the slice
TOP, Y_COR, Y_OUT, Y_BOT = 2.9, 2.0, 0.4, -3.4
HW_TOP, Y_TAPER = 3.0, -0.8
DESC_X, ASC_X, DUCT_X = 0.7, 1.6, -2.0
BEND_Y = -1.5
BEND_C = ((DESC_X + ASC_X) / 2, BEND_Y)
BEND_R = (ASC_X - DESC_X) / 2


def hw(y):
    return HW_TOP if y >= Y_TAPER else 0.5 + 2.5 * ((y - Y_BOT) / (Y_TAPER - Y_BOT))


def conc(y, go, gi):
    """Tissue concentration 0..1 (schematic): ramps through the outer medulla, then deeper still."""
    return go * 0.5 * float(np.clip((Y_COR - y) / (Y_COR - Y_OUT), 0, 1)) + gi * 0.5 * float(np.clip((Y_OUT - y) / (Y_OUT - Y_BOT), 0, 1))


def densify(pts, step=0.22):
    out = [np.array([*pts[0], 0.0])]
    for a, b in zip(pts[:-1], pts[1:]):
        a, b = np.array(a, float), np.array(b, float)
        n = max(1, int(np.ceil(np.linalg.norm(b - a) / step)))
        for k in range(1, n + 1):
            p = a + (b - a) * k / n
            out.append(np.array([p[0], p[1], 0.0]))
    return out


def arc_pts(c, r, a0, a1, n=16):
    return [(c[0] + r * np.cos(a), c[1] + r * np.sin(a)) for a in np.linspace(a0, a1, n)]


BEND = arc_pts(BEND_C, BEND_R, PI, 2 * PI)
LOOP_LOW = [(DESC_X, TOP), (DESC_X, BEND_Y)] + BEND + [(ASC_X, BEND_Y), (ASC_X, Y_OUT)]   # down, around, up to the outer medulla
ASC_UP = [(ASC_X, Y_OUT), (ASC_X, TOP)]
DUCT = [(DUCT_X, TOP), (DUCT_X, Y_TAPER), (0.0, -3.3)]
DUCT_LEN = 3.7 + float(np.hypot(2.0, 2.5))


# ------------------------------------------------------------------ moving particles
class Route:
    def __init__(self, pts):
        self.p = [np.array([x, y, 0.0]) for x, y in pts]
        d = [np.linalg.norm(self.p[i + 1] - self.p[i]) for i in range(len(self.p) - 1)]
        self.cum = np.concatenate([[0.0], np.cumsum(d)])
        self.L = float(self.cum[-1])

    def at(self, s):
        s = min(max(s, 0.0), self.L)
        i = min(int(np.searchsorted(self.cum, s, side="right") - 1), len(self.p) - 2)
        seg = self.cum[i + 1] - self.cum[i]
        t = 0.0 if seg < 1e-9 else (s - self.cum[i]) / seg
        return self.p[i] * (1 - t) + self.p[i + 1] * t


def dot(kind, r=None):
    if kind == "water":
        return Dot(radius=r or 0.085, color=BLUE)
    if kind == "salt":
        return Dot(radius=r or 0.085, color=ORANGE)
    if kind == "urea":
        return Dot(radius=r or 0.065, color=PROT)
    if kind == "flow":
        return Dot(radius=r or 0.06, color=YELLOW)
    raise ValueError(kind)


def particle(kind, route, period, phase, gate, bounce=False, fin=0.12, fout=0.22, r=None, vis=None):
    m = dot(kind, r)
    m.t = phase * period
    m.set_opacity(0)

    def up(mm, dt):
        mm.t += dt
        f = (mm.t / period) % 1.0
        if bounce:
            s = 1 - abs(2 * f - 1)
            op = 1.0
        else:
            s = f
            op = min(1.0, f / fin, (1 - f) / fout)
        mm.move_to(route.at(s * route.L))
        mm.set_opacity(max(op, 0) * gate.get_value() * (1 if vis is None else vis.get_value()))

    m.add_updater(up)
    return m


def jiggler(kind, box, seed, speed=0.5, r=None, gate=None):
    """A dot that wanders inside box=(x0, x1, y0, y1), bouncing off its edges."""
    rng = random.Random(seed)
    m = dot(kind, r)
    x0, x1, y0, y1 = box
    m.move_to([rng.uniform(x0, x1), rng.uniform(y0, y1), 0])
    ang = rng.uniform(0, TAU)
    m.v = np.array([np.cos(ang), np.sin(ang), 0.0]) * speed * rng.uniform(0.6, 1.3)
    m.clk = rng.uniform(0, 5)

    def up(mm, dt):
        mm.clk += dt
        if int(mm.clk * 2.0) != int((mm.clk - dt) * 2.0):
            a = rng.uniform(-1.1, 1.1)
            c, s = np.cos(a), np.sin(a)
            mm.v = np.array([mm.v[0] * c - mm.v[1] * s, mm.v[0] * s + mm.v[1] * c, 0.0])
        p = mm.get_center() + mm.v * dt
        if p[0] < x0 or p[0] > x1:
            mm.v[0] *= -1
            p[0] = min(max(p[0], x0), x1)
        if p[1] < y0 or p[1] > y1:
            mm.v[1] *= -1
            p[1] = min(max(p[1], y0), y1)
        mm.move_to(p)
        if gate is not None:
            mm.set_opacity(gate.get_value())

    m.add_updater(up)
    return m


def plate(t, pad=0.1, op=0.82):
    r = Rectangle(width=t.width + 2 * pad, height=t.height + 2 * pad, stroke_width=0, fill_color=BG, fill_opacity=op).move_to(t)
    return VGroup(r, t)


def lab(text, size=28, color=TEXT, **kw):
    return T(text, size, color, **kw)


def leader(a, b, op=0.7):
    return Line(a, b, color=TEXT, stroke_width=2.5).set_opacity(op)


def key_icon(h=0.62):
    """The GOLD KEY: antidiuretic hormone, in every film of this lesson."""
    bow = Circle(radius=0.17, stroke_color=GOLD, stroke_width=5, fill_color=GOLD, fill_opacity=0.35).move_to([-0.3, 0, 0])
    shaft = Line([-0.13, 0, 0], [0.42, 0, 0], color=GOLD, stroke_width=6)
    t1 = Line([0.30, 0, 0], [0.30, -0.15, 0], color=GOLD, stroke_width=6)
    t2 = Line([0.42, 0, 0], [0.42, -0.2, 0], color=GOLD, stroke_width=6)
    g = VGroup(bow, shaft, t1, t2)
    g.rotate(-PI / 2)
    g.set_height(h)
    return g


def ledger_bar(lit=False, water=False):
    words = ["excreted", "=", "filtered", "-", "reabsorbed" + (" (water)" if water else ""), "+", "secreted"]
    ts = VGroup(*[T(w, 30, TEXT if lit else GREY) for w in words]).arrange(RIGHT, buff=0.3)
    box = RoundedRectangle(corner_radius=0.15, width=ts.width + 0.7, height=0.62, stroke_color=GOLD, stroke_width=3)
    g = VGroup(box, ts).move_to([0, 3.5, 0])
    return g, ts


# ------------------------------------------------------------------ the world of this film: the slice of kidney
class Slice(SpokenScene):
    """Builds the slice of kidney in the same place every time, with trackers for what changes:
    go / gi    tissue shading of the outer / inner medulla (0 none .. 1 full)
    thk        how thick the upper ascending limb is (0 thin .. 1 thick)
    dsh        how concentrated the downward arm's fluid is
    ash        how pale the thick ascending limb's fluid has become
    lvis, dvis visibility of the loop and of the collecting duct
    dcon       how concentrated the collecting duct's urine is"""

    def slice(self, go=0.0, gi=0.0, thk=1.0, dsh=0.0, ash=0.0, lvis=1.0, dvis=0.3, dcon=0.0, dividers=True, loop=True, duct=True):
        V = ValueTracker
        self.go, self.gi, self.thk, self.dsh, self.ash = V(go), V(gi), V(thk), V(dsh), V(ash)
        self.lvis, self.dvis, self.dcon = V(lvis), V(dvis), V(dcon)
        # tissue wash: thin horizontal strips, each darker with its concentration
        ys = np.linspace(TOP, Y_BOT, 25)
        strips = VGroup()
        for y0, y1 in zip(ys[:-1], ys[1:]):
            s = Polygon([-hw(y0), y0, 0], [hw(y0), y0, 0], [hw(y1), y1, 0], [-hw(y1), y1, 0], stroke_width=0,
                        fill_color=ORANGE, fill_opacity=0.04)
            s.ym = (y0 + y1) / 2
            strips.add(s)

        def tissue(m):
            for s in m:
                s.set_fill(ORANGE, opacity=0.04 + 0.52 * conc(s.ym, self.go.get_value(), self.gi.get_value()))
        strips.add_updater(tissue)
        self.strips = strips
        self.outline = Polygon([-3, TOP, 0], [3, TOP, 0], [3, Y_TAPER, 0], [0.5, Y_BOT, 0], [-0.5, Y_BOT, 0], [-3, Y_TAPER, 0],
                               stroke_color=GREY, stroke_width=5, fill_opacity=0)
        self.divs = VGroup(*[DashedLine([-hw(y), y, 0], [hw(y), y, 0], color=GREY, stroke_width=2.5).set_opacity(0.7) for y in (Y_COR, Y_OUT)])
        self.add(strips, self.outline)
        if dividers:
            self.add(self.divs)
        self.drip = None
        # collecting duct
        if duct:
            self.duct = self.tube(DUCT, 30, 22, self.dvis, lambda y, x: 0.2 + 0.72 * self.dcon.get_value() * float(np.clip((TOP - y) / 6.2, 0, 1)))
            self.add(self.duct)
        if loop:
            self.loop_low = self.tube(LOOP_LOW, 26, 18, self.lvis, self.f_loop, thin=True)
            self.loop_up = self.tube(ASC_UP, 26, 18, self.lvis, self.f_up, thick=True)
            self.add(self.loop_low, self.loop_up)

    def f_loop(self, y, x):
        c = conc(y, self.go.get_value(), self.gi.get_value())
        if x < BEND_C[0] - 0.01 or y < BEND_Y - 0.001 and x < BEND_C[0]:      # the downward arm
            return 0.2 + 0.75 * self.dsh.get_value() * min(1.0, c * 1.05)
        return 0.3 + 0.5 * self.dsh.get_value()                                # bend and the thin upward arm

    def f_up(self, y, x):
        base = 0.3 + 0.5 * self.dsh.get_value()
        return base * (1 - 0.8 * self.ash.get_value() * float(np.clip((y - Y_OUT) / (Y_COR - Y_OUT), 0, 1)))

    def tube(self, pts, ow, iw, vis, fluid, thin=False, thick=False):
        """A tube: grey wall, dark lumen, and short yellow pieces whose opacity is the fluid's concentration."""
        outer = VMobject().set_points_as_corners([np.array([*p, 0.0]) for p in pts]).set_stroke(GREY, ow, 1)
        under = VMobject().set_points_as_corners([np.array([*p, 0.0]) for p in pts]).set_stroke(BG, iw, 1)
        dp = densify(pts)
        pieces = VGroup(*[Line(a, b).set_stroke(YELLOW, iw, 0.3) for a, b in zip(dp[:-1], dp[1:])])
        for ln in pieces:
            ln.set_cap_style(CapStyleType.BUTT)
        for m in (outer, under):
            m.set_cap_style(CapStyleType.ROUND)
            m.joint_type = LineJointType.ROUND
        g = VGroup(outer, under, pieces)
        g.outer, g.pieces = outer, pieces

        def up(m):
            v = vis.get_value()
            if thick:
                k = self.thk.get_value()
                ow2, iw2 = 24 + 22 * k, 17 + 15 * k
            else:
                ow2, iw2 = ow, iw
            outer.set_stroke(GREY, ow2, v)
            under.set_stroke(BG, iw2, v)
            for ln in pieces:
                mid = ln.get_center()
                ln.set_stroke(YELLOW, iw2, v * (0.15 + 0.8 * min(1.0, max(0.0, fluid(mid[1], mid[0])))))
        g.add_updater(up)
        return g

    def zone_labels(self):
        z = VGroup(lab("cortex", 30).move_to([3.3, 2.45, 0], aligned_edge=LEFT),
                   lab("outer medulla", 30).move_to([3.3, 1.2, 0], aligned_edge=LEFT),
                   lab("inner medulla", 30).move_to([3.3, -0.6, 0], aligned_edge=LEFT),
                   lab("papilla", 30).move_to([3.3, -3.3, 0], aligned_edge=LEFT))
        ld = leader([3.2, -3.3, 0], [0.75, -3.3, 0])
        return z, ld

    def add_drip(self):
        d = Dot(radius=0.09, color=YELLOW)
        d.t = 0.0

        def up(m, dt):
            m.t += dt
            f = (m.t / 0.9) % 1.0
            m.move_to([0, -3.42 - 0.34 * f, 0])
            m.set_opacity(min(1, f * 6, (1 - f) * 3))
        d.add_updater(up)
        self.add(d)
        self.drip = d
        return d

    def flow_dots(self, gate, n=9, speed=0.9):
        """Fluid moving down the downward arm and up the upward arm."""
        rt = Route([(DESC_X, TOP)] + [(DESC_X, BEND_Y)] + BEND[1:] + [(ASC_X, BEND_Y), (ASC_X, TOP)])
        per = rt.L / speed
        g = VGroup(*[particle("flow", rt, per, i / n, gate, fin=0.03, fout=0.03, r=0.055) for i in range(n)])
        self.add(g)
        return g

    def salt_out(self, gate, n=7, follow=None):
        """Salt stepping out through the thick upward arm into the outer medulla (to the right)."""
        g = VGroup()
        for i in range(n):
            y = Y_OUT + 0.25 + (Y_COR - Y_OUT - 0.5) * ((i * 0.618) % 1.0)
            rt = Route([(ASC_X, y), (ASC_X + 0.35, y), (ASC_X + 1.15, y + 0.05)])
            g.add(particle("salt", rt, 2.4, i / n, gate, fin=0.1, fout=0.3))
            if follow is not None:
                rt2 = Route([(ASC_X, y), (ASC_X + 0.35, y), (ASC_X + 1.15, y + 0.05)])
                w = particle("water", Route([(ASC_X, y - 0.08), (ASC_X + 0.3, y - 0.1), (ASC_X + 1.0, y - 0.04)]), 2.4, i / n + 0.14, follow, fin=0.1, fout=0.3)
                g.add(w)
        self.add(g)
        return g

    def thick_bounce(self, gate, n=5):
        g = VGroup()
        for i in range(n):
            y = Y_OUT + 0.3 + (Y_COR - Y_OUT - 0.6) * ((i * 0.618 + 0.2) % 1.0)
            rt = Route([(ASC_X - 0.05, y), (ASC_X + 0.1, y + 0.06), (ASC_X - 0.05, y)])
            g.add(particle("water", Route([(ASC_X - 0.03, y), (ASC_X + 0.11, y + 0.04)]), 1.3, i / n, gate, bounce=True, r=0.075))
        self.add(g)
        return g

    def pores(self, side=-1, y0=-1.2, y1=2.5, n=9, x=None, col=BLUE):
        x = DESC_X if x is None else x
        g = VGroup(*[Circle(radius=0.055, stroke_color=col, stroke_width=3, fill_color=BG, fill_opacity=1).move_to([x + side * 0.12, y, 0])
                     for y in np.linspace(y0, y1, n)])
        return g

    def desc_out(self, gate, n=8):
        """Water leaving the thin downward arm through its open pores (to the left)."""
        g = VGroup()
        for i in range(n):
            y = -1.1 + 3.5 * ((i * 0.618 + 0.1) % 1.0)
            rt = Route([(DESC_X - 0.05, y), (DESC_X - 0.35, y), (DESC_X - 1.05, y - 0.04)])
            g.add(particle("water", rt, 2.2, i / n, gate, fin=0.1, fout=0.3))
        self.add(g)
        return g

    def desc_salt_stay(self, gate, n=5):
        g = VGroup()
        for i in range(n):
            y = -1.0 + 3.2 * ((i * 0.618 + 0.3) % 1.0)
            g.add(particle("salt", Route([(DESC_X - 0.03, y), (DESC_X + 0.04, y + 0.08)]), 1.2, i / n, gate, bounce=True, r=0.07))
        self.add(g)
        return g

    def rising_band(self):
        pass


# ================================================================ scenes
class S00Title(TitleCard):
    LESSON = "The Kidney, part 2"
    TITLE = "Making Urine More Concentrated Than Blood"


# ---- film 1's picture, shrunk: the nephron left to right, with the ledger bar
def film1_parts():
    spec = importlib.util.spec_from_file_location("kidney_film1", str(Path(__file__).resolve().parent.parent / "scenes.py"))
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    w = mod.world_parts()
    return w


class S01Link(SpokenScene):
    def construct(self):
        w = film1_parts()
        parts = VGroup(*[w[k] for k in ("cap", "patch", "tfill", "tl", "knot", "cfill", "cl", "aff", "eff")])
        bar, terms = ledger_bar(lit=True)
        world = VGroup(parts, bar)
        gc = world.get_center()
        gate = ValueTracker(1.0)
        # water drops: along the tube, most hop up into the blood vessel
        tube_rt = lambda f: Route([f(-3.9, -0.6), f(-2.6, -0.6), f(-1.4, -0.6), f(-0.9, 2.15), f(6.0, 2.15)])
        ident = lambda x, y: (x, y)
        big = VGroup(*[particle("water", tube_rt(ident), 7.0, i / 9, gate, r=0.1) for i in range(9)])
        big2 = VGroup(*[particle("water", Route([(-3.9, -0.6), (6.2, -0.6)]), 8.0, i / 3 + 0.05, gate, r=0.1) for i in range(3)])
        self.at("first film")
        self.play(FadeIn(parts), FadeIn(bar, shift=DOWN * 0.2), run_time=1.0)
        self.add(big, big2)
        self.at("taking back")
        self.play(Indicate(terms[2], color=GOLD, scale_factor=1.15), run_time=1.0)
        s, tgt = 0.52, np.array([-3.0, 1.55, 0.0])
        mp = lambda x, y: tuple((tgt + s * (np.array([x, y, 0.0]) - gc))[:2])
        self.at("filtered water")
        gate.set_value(0)
        self.remove(big, big2)
        self.play(world.animate.scale(s).move_to(tgt), run_time=1.3)
        small = VGroup(*[particle("water", tube_rt(mp), 5.0, i / 9, ValueTracker(1.0), r=0.06) for i in range(9)],
                       *[particle("water", Route([mp(-3.9, -0.6), mp(6.2, -0.6)]), 6.0, i / 3 + 0.05, ValueTracker(1.0), r=0.06) for i in range(3)])
        self.add(small)
        ex, ey = mp(6.3, -0.6)
        ring = Circle(radius=0.38, stroke_color=GOLD, stroke_width=6).move_to([ex - 0.1, ey, 0])
        lbl = lab("the last litres", 52, YELLOW).move_to([2.0, -1.5, 0])
        arr = Arrow(lbl.get_top() + UP * 0.05, [ex - 0.1, ey - 0.4, 0], color=GOLD, buff=0.05, stroke_width=6)
        self.at("the last liters")
        self.play(Create(ring), FadeIn(lbl, shift=UP * 0.2), GrowArrow(arr), run_time=1.0)
        self.play(Indicate(ring, color=GOLD, scale_factor=1.25), run_time=1.2)
        self.finish()


class S02Question(SpokenScene):
    def construct(self):
        def beaker(cx):
            return VGroup(Line([cx - 1.6, 1.1, 0], [cx - 1.45, -2.9, 0], color=GREY, stroke_width=5),
                          Line([cx - 1.45, -2.9, 0], [cx + 1.45, -2.9, 0], color=GREY, stroke_width=5),
                          Line([cx + 1.45, -2.9, 0], [cx + 1.6, 1.1, 0], color=GREY, stroke_width=5))

        def fill(cx, col, op):
            return Polygon([cx - 1.58, 0.7, 0], [cx + 1.58, 0.7, 0], [cx + 1.44, -2.88, 0], [cx - 1.44, -2.88, 0],
                           stroke_width=0, fill_color=col, fill_opacity=op)
        bl, br = beaker(-3.7), beaker(3.7)
        fl, fr = fill(-3.7, RED, 0.22), fill(3.7, YELLOW, 0.3)
        self.play(Create(bl), Create(br), run_time=1.5)
        gate = ValueTracker(1.0)
        ud = VGroup(*[jiggler("salt", (2.35, 5.05, -2.7, 0.5), 10 + i, 0.55) for i in range(24)])
        pd = VGroup(*[jiggler("salt", (-5.05, -2.35, -2.7, 0.5), 50 + i, 0.55) for i in range(6)])
        ul = VGroup(lab("most concentrated", 30, YELLOW), lab("human urine, near 1,200", 30, YELLOW)).arrange(DOWN, buff=0.1).move_to([3.7, 2.35, 0])
        pl = VGroup(lab("plasma", 34, RED), lab("about 290 mOsm per kg", 30, TEXT)).arrange(DOWN, buff=0.1).move_to([-3.7, 2.35, 0])
        self.at("urine")
        self.play(FadeIn(fr), FadeIn(ud), run_time=0.6)
        self.at("about four times")
        self.play(FadeIn(ul, shift=DOWN * 0.1), run_time=0.8)
        self.at("as plasma")
        self.play(FadeIn(fl), FadeIn(pd), FadeIn(pl, shift=DOWN * 0.1), run_time=1.0)
        # a water pump, drawn and crossed out
        body = RoundedRectangle(corner_radius=0.15, width=1.7, height=1.0, stroke_color=GREY, stroke_width=5, fill_color=GREY, fill_opacity=0.15)
        wheel = VGroup(Circle(radius=0.3, stroke_color=BLUE, stroke_width=5), Line([-0.3, 0, 0], [0.3, 0, 0], color=BLUE, stroke_width=5),
                       Line([0, -0.3, 0], [0, 0.3, 0], color=BLUE, stroke_width=5))
        pipe = VGroup(Line([-1.45, 0, 0], [-0.85, 0, 0], color=BLUE, stroke_width=9), Line([0.85, 0, 0], [1.45, 0, 0], color=BLUE, stroke_width=9))
        pump = VGroup(pipe, body, wheel).move_to([0, -0.2, 0])
        wheel.add_updater(lambda m, dt: m.rotate(dt * 2.0))
        pl2 = lab("water pump", 32, TEXT).move_to([0, -1.25, 0])
        cross = VGroup(Line([-1.0, 0.45, 0], [1.0, -0.85, 0], color=RED, stroke_width=11), Line([-1.0, -0.85, 0], [1.0, 0.45, 0], color=RED, stroke_width=11))
        self.at("pump")
        self.play(FadeIn(pump, scale=0.8), FadeIn(pl2), run_time=0.8)
        self.at("moves water")
        self.play(Create(cross), run_time=0.6)
        q = lab("?", 150, GOLD, weight=BOLD).move_to([0, 1.7, 0])
        q.t = 0.0
        self.at("so how")
        self.play(FadeIn(q, scale=0.5), run_time=0.6)
        q.add_updater(lambda m, dt: (setattr(m, "t", m.t + dt), m.set_height(1.5 * (1 + 0.1 * np.sin(m.t * 4)))))
        self.finish()


class S03Osmolality(SpokenScene):
    def construct(self):
        cy, bx = -0.5, 4.8
        word = lab("osmolality", 64, TEXT).move_to([0, 0.2, 0])
        self.at("osmolality")
        self.play(FadeIn(word, scale=0.9), run_time=0.8)
        top = lab("osmolality = dissolved particles per kg of water", 34, TEXT).move_to([0, 3.3, 0])
        box = Rectangle(width=2 * bx, height=5.8, stroke_color=GREY, stroke_width=5).move_to([0, cy, 0])
        mem = DashedLine([0, cy - 2.9, 0], [0, cy + 2.9, 0], color=GREY, stroke_width=5)
        left_d = VGroup(*[jiggler("salt", (-bx + 0.25, -0.3, cy - 2.65, cy + 2.65), 100 + i, 0.5) for i in range(5)])
        right_d = VGroup(*[jiggler("salt", (0.3, bx - 0.25, cy - 2.65, cy + 2.65), 200 + i, 0.5) for i in range(20)])
        self.at("dissolved particles")
        self.play(ReplacementTransform(word, top), Create(box), Create(mem), run_time=1.2)
        self.play(FadeIn(left_d), FadeIn(right_d), run_time=1.0)
        self.at("kilogram of water")
        self.play(Indicate(top, color=BLUE, scale_factor=1.04), run_time=1.2)
        # water crosses to the crowded side
        gate = ValueTracker(0.0)
        drops = VGroup()
        for i in range(10):
            y = cy - 2.3 + 4.6 * ((i * 0.618) % 1.0)
            drops.add(particle("water", Route([(-3.6, y), (-0.3, y), (0.4, y + 0.1), (3.2, y + 0.3)]), 4.2, i / 10, gate, r=0.1, fin=0.08, fout=0.18))
        self.add(drops)
        self.at("water moves by osmosis")
        gate.set_value(1.0)
        cl = plate(chip("less concentrated", TEXT, 28), op=0.97).move_to([-2.4, cy + 2.2, 0]).set_z_index(20)
        cr = plate(chip("more concentrated", TEXT, 28), op=0.97).move_to([2.4, cy + 2.2, 0]).set_z_index(20)
        self.play(Indicate(mem, color=BLUE), run_time=1.0)
        self.at("the more concentrated side")
        self.play(FadeIn(cl, shift=DOWN * 0.1), FadeIn(cr, shift=DOWN * 0.1), run_time=0.8)
        # the box becomes a tube in tissue
        self.at("so the tissue outside")
        tissue_op = ValueTracker(0.22)
        tissue = Rectangle(width=12.6, height=5.8, stroke_color=GREY, stroke_width=3, fill_color=ORANGE, fill_opacity=0.22).move_to([0, cy, 0])
        tissue.add_updater(lambda m: m.set_fill(ORANGE, opacity=tissue_op.get_value()))
        tube = VGroup(Rectangle(width=12.6, height=1.3, stroke_width=0, fill_color=BG, fill_opacity=1),
                      Rectangle(width=12.6, height=1.3, stroke_width=0, fill_color=YELLOW, fill_opacity=0.22),
                      Line([-6.3, 0.65, 0], [6.3, 0.65, 0], color=GREY, stroke_width=7), Line([-6.3, -0.65, 0], [6.3, -0.65, 0], color=GREY, stroke_width=7)).move_to([0, cy, 0])
        self.play(FadeOut(VGroup(box, mem, left_d, right_d, drops, cl, cr)), FadeIn(tissue), run_time=0.9)
        self.remove(drops)
        gate.set_value(0.0)
        self.add(tube)
        tl = lab("tissue", 34, TEXT).move_to([-5.2, cy + 2.2, 0])
        ul = lab("urine", 34, YELLOW).move_to([-5.4, cy, 0])
        self.play(FadeIn(plate(tl).set_z_index(20)), FadeIn(plate(ul).set_z_index(20)), run_time=0.8)
        self.at("a little more concentrated")
        # the shading outside deepens a little, then water leaves the tube
        out = VGroup()
        wg = ValueTracker(0.0)
        for i in range(14):
            x = -5.0 + 10.0 * ((i * 0.618) % 1.0)
            sgn = 1 if i % 2 == 0 else -1
            out.add(particle("water", Route([(x, cy + sgn * 0.3), (x, cy + sgn * 1.7)]), 2.6, i / 14, wg, r=0.1))
        self.add(out)
        self.play(tissue_op.animate.set_value(0.5), run_time=1.5)
        wg.set_value(1.0)
        self.at("than the urine")
        self.play(Indicate(tl, color=ORANGE), run_time=1.0)
        # salt and urea in the tissue
        sg = ValueTracker(0.0)
        zg = ValueTracker(0.0)
        salts = VGroup(*[jiggler("salt", (-6.0, 6.0, cy + 0.95, cy + 2.65) if i % 2 == 0 else (-6.0, 6.0, cy - 2.65, cy - 0.95), 300 + i, 0.4, gate=sg, r=0.1) for i in range(26)])
        ureas = VGroup(*[jiggler("urea", (-6.0, 6.0, cy - 2.65, cy - 0.95), 400 + i, 0.4, gate=zg, r=0.085) for i in range(10)])
        self.add(salts, ureas)
        sl = VGroup(dot("salt", 0.12), lab("salt", 34, ORANGE)).arrange(RIGHT, buff=0.15).move_to([4.8, cy + 2.2, 0])
        zl = VGroup(dot("urea", 0.1), lab("urea (deep medulla)", 32, TEXT)).arrange(RIGHT, buff=0.15).move_to([3.7, cy - 2.2, 0])
        self.at("salt supplies most")
        sg.set_value(1.0)
        self.play(FadeIn(plate(sl).set_z_index(20)), run_time=0.8)
        self.at("deep down")
        zg.set_value(1.0)
        self.play(FadeIn(plate(zl).set_z_index(20)), run_time=0.8)
        self.finish()


class S04Slab(Slice):
    def construct(self):
        self.slice(go=0, gi=0, thk=0, dividers=False, loop=False, duct=False)
        self.remove(self.strips, self.outline)
        self.at("picture a slice")
        self.play(Create(self.outline), FadeIn(self.strips), run_time=2.0)
        self.add_drip()
        self.drip.set_opacity(0)
        z, ld = self.zone_labels()
        self.at("outer layer is the cortex")
        cor = Rectangle(width=6, height=Y_COR - TOP, stroke_width=0, fill_color=TEXT, fill_opacity=0.12).move_to([0, (TOP + Y_COR) / 2, 0])
        self.play(FadeIn(cor), FadeIn(z[0], shift=LEFT * 0.1), run_time=0.8)
        self.at("beneath lies the medulla")
        self.play(FadeOut(cor), Create(self.divs[0]), run_time=0.8)
        med = Polygon([-3, Y_COR, 0], [3, Y_COR, 0], [3, Y_TAPER, 0], [0.5, Y_BOT, 0], [-0.5, Y_BOT, 0], [-3, Y_TAPER, 0],
                      stroke_width=0, fill_color=TEXT, fill_opacity=0.08)
        self.play(FadeIn(med), run_time=0.8)
        self.at("outer zone")
        self.play(Create(self.divs[1]), FadeIn(z[1], shift=LEFT * 0.1), run_time=0.8)
        self.at("inner zone")
        self.play(FadeIn(z[2], shift=LEFT * 0.1), run_time=0.8)
        self.at("papilla")
        tip = Polygon([-0.5, Y_BOT, 0], [0.5, Y_BOT, 0], [0.65, -2.7, 0], [-0.65, -2.7, 0], stroke_width=0, fill_color=GOLD, fill_opacity=0.35)
        self.play(FadeOut(med), FadeIn(tip), FadeIn(z[3], shift=LEFT * 0.1), Create(ld), run_time=0.9)
        self.at("urine drains")
        self.play(FadeOut(tip), run_time=0.5)
        gate_d = ValueTracker(1.0)
        self.drip.set_opacity(1)
        # the duct, faint, then the loop
        self.dvis, self.dcon = ValueTracker(0.0), ValueTracker(0.0)
        self.duct = self.tube(DUCT, 30, 22, self.dvis, lambda y, x: 0.25)
        self.add(self.duct)
        dl = lab("collecting duct", 28, TEXT).move_to([-6.8, 1.3, 0], aligned_edge=LEFT)
        dll = leader([-6.8 + dl.width + 0.1, 1.3, 0], [DUCT_X - 0.2, 1.3, 0])
        self.play(self.dvis.animate.set_value(0.3), FadeIn(dl), Create(dll), run_time=0.8)
        self.at("a hairpin tube")
        self.play(FadeOut(z), FadeOut(ld), FadeOut(dl), FadeOut(dll), run_time=0.4)
        self.lvis, self.thk, self.dsh, self.ash = ValueTracker(1.0), ValueTracker(0.0), ValueTracker(0.0), ValueTracker(0.0)
        self.go, self.gi = ValueTracker(0), ValueTracker(0)
        # draw the loop by revealing it
        self.loop_low = self.tube(LOOP_LOW, 26, 18, self.lvis, self.f_loop, thin=True)
        self.loop_up = self.tube(ASC_UP, 26, 18, self.lvis, self.f_up, thick=True)
        loop = VGroup(self.loop_low, self.loop_up)
        self.play(Create(self.loop_low[0]), Create(self.loop_up[0]), run_time=1.1)
        self.add(loop)
        ll = lab("loop of Henle", 32, TEXT).move_to([3.3, -1.7, 0], aligned_edge=LEFT)
        lll = leader([3.25, -1.7, 0], [ASC_X + 0.25, -1.7, 0])
        self.at("the loop")
        self.play(FadeIn(ll, shift=LEFT * 0.1), Create(lll), run_time=0.5)
        self.at("dips into it")
        gate = ValueTracker(0.0)
        fd = self.flow_dots(gate)
        gate.set_value(1.0)
        self.play(Indicate(loop, color=GOLD, scale_factor=1.02), run_time=1.2)
        self.finish()


class S05Ascending(Slice):
    def construct(self):
        self.slice(go=0, gi=0, thk=0, dsh=0, ash=0, dvis=0.3)
        self.add_drip()
        flow = ValueTracker(1.0)
        self.flow_dots(flow)
        thin_l = VGroup(lab("thin ascending", 30, TEXT), lab("limb", 30, TEXT)).arrange(DOWN, aligned_edge=LEFT, buff=0.05).move_to([3.3, -0.55, 0], aligned_edge=LEFT)
        thin_ld = leader([3.25, -0.55, 0], [ASC_X + 0.25, -0.55, 0])
        thick_l = VGroup(lab("thick ascending", 30, TEXT), lab("limb", 30, TEXT)).arrange(DOWN, aligned_edge=LEFT, buff=0.05).move_to([3.3, 1.2, 0], aligned_edge=LEFT)
        thick_ld = leader([3.25, 1.2, 0], [ASC_X + 0.45, 1.2, 0])
        hl = VMobject().set_points_as_corners([np.array([ASC_X, BEND_Y, 0]), np.array([ASC_X, TOP, 0])]).set_stroke(GOLD, 30, 0.0)
        self.add(hl)
        self.at("upward arm")
        self.play(hl.animate.set_stroke(GOLD, 30, 0.35), run_time=0.7)
        self.play(hl.animate.set_stroke(GOLD, 30, 0.0), run_time=0.7)
        self.at("in the outer medulla")
        self.play(self.thk.animate.set_value(1.0), run_time=0.9)
        self.at("it is thick")
        self.play(FadeIn(thin_l, shift=LEFT * 0.1), Create(thin_ld), run_time=0.7)
        self.at("the thick ascending limb")
        self.play(FadeIn(thick_l, shift=LEFT * 0.1), Create(thick_ld), run_time=0.8)
        sg, wg = ValueTracker(0.0), ValueTracker(0.0)
        self.salt_out(sg, 8)
        self.thick_bounce(wg, 6)
        self.at("moves salt out")
        sg.set_value(1.0)
        self.add(self.ash, self.go)
        self.ash.add_updater(lambda m, dt: m.set_value(min(1.0, m.get_value() + dt / 6.0)))
        self.go.add_updater(lambda m, dt: m.set_value(min(0.7, m.get_value() + dt * 0.7 / 7.0)))
        self.play(Indicate(self.loop_up[0], color=ORANGE, scale_factor=1.05), run_time=1.0)
        self.at("almost no water through")
        wg.set_value(1.0)
        self.play(Indicate(self.loop_up[0], color=BLUE, scale_factor=1.06), run_time=1.0)
        self.at("salt leaves")
        self.play(Indicate(self.loop_up[0], color=ORANGE, scale_factor=1.05), run_time=1.0)
        self.at("tissue gets saltier")
        self.play(Indicate(self.strips, color=ORANGE, scale_factor=1.0), run_time=1.0)
        self.finish()


class S06Descending(Slice):
    def construct(self):
        self.slice(go=0.7, gi=0, thk=1, dsh=0, ash=1, dvis=0.3)
        self.add_drip()
        flow = ValueTracker(1.0)
        self.flow_dots(flow)
        sg = ValueTracker(1.0)
        self.salt_out(sg, 8)
        dl = lab("thin descending limb (rabbit)", 28, TEXT)
        dl = VGroup(lab("thin descending", 30, TEXT), lab("limb (rabbit)", 30, TEXT)).arrange(DOWN, aligned_edge=RIGHT, buff=0.05).move_to([-3.2, -0.4, 0], aligned_edge=RIGHT)
        dld = leader([-3.15, -0.4, 0], [DESC_X - 0.2, -0.4, 0])
        hl = VMobject().set_points_as_corners([np.array([DESC_X, TOP, 0]), np.array([DESC_X, BEND_Y, 0])]).set_stroke(GOLD, 30, 0.0)
        self.add(hl)
        self.at("the thin descending limb")
        self.play(hl.animate.set_stroke(GOLD, 30, 0.35), run_time=0.7)
        self.play(hl.animate.set_stroke(GOLD, 30, 0.0), run_time=0.7)
        self.at("downward arm")
        self.play(FadeIn(dl, shift=RIGHT * 0.1), Create(dld), run_time=0.8)
        pores = self.pores(-1, -1.2, 2.6, 10)
        wg, zg = ValueTracker(0.0), ValueTracker(0.0)
        self.desc_out(wg, 9)
        self.desc_salt_stay(zg, 6)
        self.at("in rabbit tubules")
        self.play(FadeIn(pores, lag_ratio=0.1), run_time=1.0)
        self.at("lets water through")
        wg.set_value(1.0)
        self.play(Indicate(pores, color=BLUE, scale_factor=1.3), run_time=1.0)
        self.at("holds its salt")
        zg.set_value(1.0)
        self.play(Indicate(self.loop_low[0], color=ORANGE, scale_factor=1.04), run_time=1.0)
        self.at("passing salty tissue")
        self.play(Indicate(self.strips, color=ORANGE, scale_factor=1.0), run_time=1.2)
        self.at("loses water by osmosis")
        self.play(self.dsh.animate.set_value(1.0), run_time=3.2)
        self.at("concentrates on the way down")
        self.play(Indicate(self.loop_low[0], color=YELLOW, scale_factor=1.04), run_time=1.2)
        self.finish()


class S07Multiply(Slice):
    def construct(self):
        self.slice(go=0.7, gi=0, thk=1, dsh=1, ash=1, dvis=0.3)
        self.add_drip()
        flow = ValueTracker(1.0)
        self.flow_dots(flow)
        sg = ValueTracker(1.0)
        self.salt_out(sg, 8)
        wg, zg = ValueTracker(1.0), ValueTracker(1.0)
        self.desc_out(wg, 6)
        # arrows: down in the left arm, up in the right arm
        dn = VGroup(*[Arrow([DESC_X - 0.55, y + 0.35, 0], [DESC_X - 0.55, y - 0.35, 0], color=TEXT, buff=0, stroke_width=7, max_tip_length_to_length_ratio=0.5) for y in (2.2, 0.6, -0.9)])
        upa = VGroup(*[Arrow([ASC_X + 0.5, y - 0.35, 0], [ASC_X + 0.5, y + 0.35, 0], color=TEXT, buff=0, stroke_width=7, max_tip_length_to_length_ratio=0.5) for y in (2.2, 0.6, -0.9)])
        cf = lab("countercurrent flow", 26, TEXT).move_to([3.2, 2.45, 0], aligned_edge=LEFT)
        self.at("opposite directions")
        self.play(FadeIn(dn, lag_ratio=0.2), FadeIn(upa, lag_ratio=0.2), FadeIn(cf, shift=LEFT * 0.1), run_time=1.6)
        self.at("concentrated fluid rounds the bend")
        ring = Circle(radius=0.55, stroke_color=YELLOW, stroke_width=6).move_to([BEND_C[0], BEND_Y - 0.05, 0])
        self.play(Create(ring), run_time=0.8)
        self.play(Indicate(ring, color=YELLOW, scale_factor=1.3), run_time=1.0)
        self.at("saltier start")
        self.play(FadeOut(ring), Indicate(self.loop_up[0], color=ORANGE, scale_factor=1.05), run_time=1.0)
        self.at("level by level")
        mult = VGroup(lab("countercurrent", 30, GOLD), lab("multiplier", 30, GOLD)).arrange(DOWN, aligned_edge=LEFT, buff=0.05).move_to([3.2, 1.2, 0], aligned_edge=LEFT)
        for v in (0.8, 0.88, 0.95, 1.0):
            self.play(self.go.animate.set_value(v), run_time=0.85)
        self.at("this is the countercurrent")
        self.play(FadeOut(cf), FadeIn(mult, shift=LEFT * 0.1), run_time=0.7)
        self.play(Indicate(mult, color=GOLD), run_time=1.0)
        self.at("deeper down")
        q = lab("?", 110, GOLD, weight=BOLD).move_to([-0.8, -2.15, 0])
        ql = VGroup(lab("inner medulla:", 30, TEXT), lab("mechanism", 30, TEXT), lab("debated", 30, TEXT)).arrange(DOWN, aligned_edge=LEFT, buff=0.05).move_to([3.3, -0.6, 0], aligned_edge=LEFT)
        self.play(self.gi.animate.set_value(1.0), FadeIn(q, scale=0.5), FadeIn(ql, shift=LEFT * 0.1), run_time=2.0)
        q.t = 0.0
        q.add_updater(lambda m, dt: (setattr(m, "t", m.t + dt), m.set_height(1.0 * (1 + 0.1 * np.sin(m.t * 4)))))
        self.finish()


def full_state(scene, **kw):
    """The slice as it stands once the multiplier has worked."""
    scene.slice(go=1, gi=1, thk=1, dsh=1, ash=1, dvis=0.3, **kw)
    scene.add_drip()


class S08Predict(Slice):
    def construct(self):
        full_state(self)
        flow = ValueTracker(1.0)
        fd = self.flow_dots(flow)
        sg = ValueTracker(1.0)
        so = self.salt_out(sg, 8)
        wg = ValueTracker(0.0)
        self.at("thick ascending limb")
        self.play(Indicate(self.loop_up[0], color=GOLD, scale_factor=1.06), run_time=1.2)
        pores = self.pores(1, Y_OUT + 0.15, TOP - 0.15, 10, x=ASC_X + 0.1)
        self.at("let water through")
        for _ in range(2):
            self.play(FadeIn(pores), self.loop_up[0].animate.set_stroke(GREY, 40, 0.5), run_time=0.45)
            self.play(FadeOut(pores), self.loop_up[0].animate.set_stroke(GREY, 40, 1.0), run_time=0.45)
        self.play(FadeIn(pores), run_time=0.5)
        self.at("would the multiplier")
        band = Rectangle(width=6.0, height=Y_COR - Y_OUT, stroke_color=GOLD, stroke_width=5, fill_opacity=0).move_to([0, (Y_COR + Y_OUT) / 2, 0])
        self.play(Create(band), run_time=0.8)
        for g in (flow, sg):
            g.set_value(0.0)
        self.at("still work well")
        c1 = chip("still works\nwell", TEXT, 30).move_to([5.0, 0.9, 0])
        c2 = chip("badly\nweakened", TEXT, 30).move_to([5.0, -0.7, 0])
        pd = lab("Pause and decide", 32, GOLD).move_to([5.0, 3.35, 0])
        self.play(FadeIn(c1, shift=LEFT * 0.1), FadeIn(c2, shift=LEFT * 0.1), run_time=0.8)
        self.at("pause and decide")
        self.play(FadeIn(pd), Indicate(c1, color=GOLD), Indicate(c2, color=GOLD), run_time=1.2)
        self.finish()


class S09Pause(Slice):
    def construct(self):
        full_state(self)
        self.add(self.pores(1, Y_OUT + 0.15, TOP - 0.15, 10, x=ASC_X + 0.1))
        self.add(Rectangle(width=6.0, height=Y_COR - Y_OUT, stroke_color=GOLD, stroke_width=5, fill_opacity=0).move_to([0, (Y_COR + Y_OUT) / 2, 0]))
        self.add(chip("still works\nwell", TEXT, 30).move_to([5.0, 0.9, 0]), chip("badly\nweakened", TEXT, 30).move_to([5.0, -0.7, 0]))
        q = lab("Pause and decide", 32, GOLD).move_to([5.0, 3.35, 0])
        track = Circle(radius=0.5, stroke_color=GREY, stroke_width=6).move_to([5.9, -2.9, 0])
        tv = ValueTracker(0)
        ring = always_redraw(lambda: Arc(radius=0.5, start_angle=PI / 2, angle=-TAU * max(1 - tv.get_value(), 0.001),
                                         arc_center=[5.9, -2.9, 0], stroke_color=GOLD, stroke_width=8))
        self.add(q, track, ring)
        self.play(tv.animate.set_value(1.0), run_time=self.narration_s - 0.1, rate_func=linear)
        self.finish()


class S10Reveal(Slice):
    def construct(self):
        full_state(self)
        flow = ValueTracker(0.0)
        fd = self.flow_dots(flow)
        sg, wg = ValueTracker(1.0), ValueTracker(0.0)
        self.salt_out(sg, 8, follow=wg)
        pores = self.pores(1, Y_OUT + 0.15, TOP - 0.15, 10, x=ASC_X + 0.1)
        band = Rectangle(width=6.0, height=Y_COR - Y_OUT, stroke_color=GOLD, stroke_width=5, fill_opacity=0).move_to([0, (Y_COR + Y_OUT) / 2, 0])
        c1 = chip("still works\nwell", TEXT, 30).move_to([5.0, 0.9, 0])
        c2 = chip("badly\nweakened", TEXT, 30).move_to([5.0, -0.7, 0])
        self.add(pores, band, c1, c2)
        self.at("badly weakened")
        self.play(c2[0].animate.set_stroke(GOLD, 7).set_fill(GOLD, 0.3), Indicate(c2, color=GOLD, scale_factor=1.12), run_time=1.4)
        self.at("water would follow")
        wg.set_value(1.0)
        self.play(Indicate(pores, color=BLUE, scale_factor=1.25), run_time=1.2)
        self.at("most of the difference")
        self.play(self.go.animate.set_value(0.2), self.gi.animate.set_value(0.2), self.ash.animate.set_value(0.0), FadeOut(band), run_time=3.2)
        cap = lab("salt without\nwater", 38, TEXT).move_to([5.0, 2.0, 0])
        cap = VGroup(lab("salt without", 38, TEXT), lab("water", 38, TEXT)).arrange(DOWN, buff=0.05).move_to([5.0, 2.0, 0])
        self.at("salt moving without water")
        wg.set_value(0.0)
        self.play(FadeOut(pores), FadeOut(VGroup(c1, c2)), self.go.animate.set_value(1.0), self.gi.animate.set_value(1.0), self.ash.animate.set_value(1.0),
                  FadeIn(cap, shift=LEFT * 0.1), run_time=2.0)
        self.play(Indicate(cap, color=GOLD, scale_factor=1.08), run_time=1.2)
        self.finish()


class S11Evidence(Slice):
    def construct(self):
        self.slice(go=1, gi=1, thk=1, dsh=1, ash=1, lvis=0.25, dvis=0.25)
        self.add_drip()
        # thermometer (right panel)
        TX = 5.0
        glass = RoundedRectangle(corner_radius=0.17, width=0.34, height=3.4, stroke_color=TEXT, stroke_width=5).move_to([TX, 0.2, 0])
        bulb = Circle(radius=0.34, stroke_color=TEXT, stroke_width=5, fill_color=BLUE, fill_opacity=0.9).move_to([TX, -1.85, 0])
        lvl = ValueTracker(0.8)
        merc = always_redraw(lambda: Rectangle(width=0.16, height=max(0.05, 3.0 * lvl.get_value()), stroke_width=0, fill_color=BLUE, fill_opacity=0.95)
                             .move_to([TX, -1.5 + max(0.05, 3.0 * lvl.get_value()) / 2, 0]))
        ft = lab("freezing point", 30, TEXT).move_to([TX, 2.55, 0])
        rat = lab("rat, 1951", 32, GOLD).move_to([TX, 3.35, 0])
        self.add(glass, merc, bulb)
        # the measured profile, beside the slice (left panel)
        px = lambda c: -6.1 + 2.6 * c
        ys = [2.55, 1.35, -0.3, -1.4, -2.7]
        cs = [conc(y, 1, 1) for y in ys]
        pts = VGroup()
        self.at("is real tissue graded")
        self.play(FadeIn(rat, shift=DOWN * 0.1), FadeIn(ft), run_time=0.9)
        self.at("measured the freezing")
        for i, y in enumerate(ys):
            h = 0.5
            strip = Rectangle(width=2 * hw(y), height=h, stroke_color=TEXT, stroke_width=4, fill_color=TEXT, fill_opacity=0.25).move_to([0, y, 0])
            self.play(FadeIn(strip), run_time=0.15)
            sl = strip.copy().set_fill(ORANGE, opacity=0.35 + 0.5 * cs[i])
            self.play(sl.animate.scale(0.28).move_to([TX, -1.85, 0]), run_time=0.45)
            self.play(FadeOut(sl), lvl.animate.set_value(0.8 - 0.62 * cs[i]), FadeOut(strip), run_time=0.3)
            p = Dot(radius=0.13, color=ORANGE).move_to([px(cs[i]), y, 0])
            pts.add(p)
            self.add(p)
        self.at("more particles")
        note = VGroup(lab("more particles:", 28, TEXT), lab("lower freezing point", 28, TEXT)).arrange(DOWN, buff=0.05).move_to([TX, -3.05, 0])
        self.play(FadeIn(note, shift=UP * 0.1), run_time=0.6)
        for _ in range(2):
            self.play(lvl.animate.set_value(0.8), run_time=0.7)
            self.play(lvl.animate.set_value(0.18), run_time=0.7)
        self.at("osmolality rose")
        curve = VMobject().set_points_smoothly([np.array([px(c), y, 0]) for c, y in zip(cs, ys)]).set_stroke(ORANGE, 6)
        ax = Line([-6.1, 2.9, 0], [-6.1, -3.4, 0], color=GREY, stroke_width=3)
        ol = VGroup(lab("osmolality,", 28, ORANGE), lab("schematic", 28, ORANGE)).arrange(DOWN, buff=0.05).move_to([-5.0, 3.3, 0])
        self.play(Create(curve), Create(ax), FadeIn(ol), run_time=2.0)
        self.play(Indicate(curve, color=ORANGE, scale_factor=1.0), run_time=1.0)
        self.finish()


class S12Duct(Slice):
    def construct(self):
        full_state(self)
        self.dvis.set_value(0.3)
        self.lvis.set_value(1.0)
        flow = ValueTracker(1.0)
        self.flow_dots(flow, n=7)
        sg = ValueTracker(1.0)
        self.salt_out(sg, 6)
        # urine flowing down the duct
        drt = Route([(DUCT_X, TOP), (DUCT_X, Y_TAPER), (0.0, -3.3)])
        dg = ValueTracker(0.0)
        dflow = VGroup(*[particle("flow", drt, drt.L / 0.8, i / 7, dg, fin=0.03, fout=0.03, r=0.055) for i in range(7)])
        self.add(dflow)
        self.at("the collecting duct")
        dg.set_value(1.0)
        self.play(self.dvis.animate.set_value(1.0), self.lvis.animate.set_value(0.35), run_time=1.6)
        self.at("from cortex to papilla")
        sweep = Dot(radius=0.2, color=GOLD).move_to([DUCT_X, TOP, 0]).set_opacity(0.0)
        self.play(sweep.animate.set_opacity(0.9), run_time=0.2)
        self.play(MoveAlongPath(sweep, VMobject().set_points_as_corners([np.array([*p, 0.0]) for p in DUCT])), run_time=2.4)
        self.play(FadeOut(sweep), run_time=0.2)
        self.at("antidiuretic hormone")
        # inset: a duct cell (left panel)
        fx0, fx1, fy0, fy1 = -6.75, -3.3, -0.9, 2.85
        frame = RoundedRectangle(corner_radius=0.12, width=fx1 - fx0, height=fy1 - fy0, stroke_color=GREY, stroke_width=4, fill_color=BG, fill_opacity=1).move_to([(fx0 + fx1) / 2, (fy0 + fy1) / 2, 0])
        tis = Rectangle(width=0.8, height=fy1 - fy0 - 0.1, stroke_width=0, fill_color=ORANGE, fill_opacity=0.5).move_to([fx0 + 0.45, (fy0 + fy1) / 2, 0])
        cell = Rectangle(width=1.7, height=fy1 - fy0 - 0.1, stroke_width=0, fill_color=GREY, fill_opacity=0.22).move_to([fx0 + 1.3 + 0.85, (fy0 + fy1) / 2, 0])
        mx = fx0 + 0.9 + 1.7 + 0.0
        lumen = Rectangle(width=fx1 - mx - 0.05, height=fy1 - fy0 - 0.1, stroke_width=0, fill_color=YELLOW, fill_opacity=0.25).move_to([(mx + fx1) / 2 - 0.02, (fy0 + fy1) / 2, 0])
        mem = Line([mx, fy1 - 0.05, 0], [mx, fy0 + 0.05, 0], color=GREY, stroke_width=6)
        zl1 = leader([DUCT_X - 0.2, 1.2, 0], [fx1 + 0.05, 1.2, 0], 0.5)
        cap = lab("duct cell (schematic)", 26, TEXT).move_to([(fx0 + fx1) / 2, fy0 - 0.85, 0])
        self.play(FadeIn(frame), FadeIn(tis), FadeIn(cell), FadeIn(lumen), Create(mem), Create(zl1), FadeIn(cap), run_time=1.0)
        key = key_icon(1.0).move_to([fx0 + 0.45, 3.6, 0])
        kl = lab("ADH", 28, GOLD)
        self.at("acts on its cells")
        self.play(key.animate.move_to([fx0 + 0.45, 1.9, 0]), run_time=1.3)
        kl.next_to(key, DOWN, buff=0.12)
        self.play(FadeIn(kl), Indicate(key, color=GOLD, scale_factor=1.2), run_time=0.8)
        # vesicles with channels slide to the wall facing the urine
        ves = VGroup(*[Circle(radius=0.28, stroke_color=TEXT, stroke_width=3, fill_color=BG, fill_opacity=1).move_to([fx0 + 1.9, y, 0]) for y in (2.15, 0.8, -0.35)])
        doors = VGroup(*[VGroup(Rectangle(width=0.16, height=0.34, stroke_color=TEAL, stroke_width=4, fill_color=BG, fill_opacity=1),
                                 Line([-0.08, 0, 0], [0.08, 0, 0], color=TEAL, stroke_width=4)).move_to(v.get_center()) for v in ves])
        self.add(ves, doors)
        al = lab("aquaporin-2", 28, TEAL).move_to([-5.0, fy0 - 0.35, 0])
        self.at("they insert")
        self.play(FadeIn(ves), FadeIn(doors), run_time=0.8)
        self.at("stored water channels")
        self.play(FadeIn(plate(al)), run_time=0.7)
        self.at("facing the urine")
        self.play(AnimationGroup(*[d.animate.move_to([mx - 0.0, y, 0]) for d, y in zip(doors, (2.15, 0.8, -0.35))], lag_ratio=0.25),
                  FadeOut(ves), run_time=2.4)
        self.finish()


class S13Concentrate(Slice):
    def construct(self):
        full_state(self)
        self.dvis.set_value(1.0)
        self.lvis.set_value(0.35)
        flow = ValueTracker(1.0)
        self.flow_dots(flow, n=7)
        sg = ValueTracker(1.0)
        self.salt_out(sg, 6)
        drt = Route([(DUCT_X, TOP), (DUCT_X, Y_TAPER), (0.0, -3.3)])
        dg = ValueTracker(1.0)
        self.add(VGroup(*[particle("flow", drt, drt.L / 0.8, i / 7, dg, fin=0.03, fout=0.03, r=0.055) for i in range(7)]))
        # the duct-cell inset exactly as left by the last scene
        fx0, fx1, fy0, fy1 = -6.75, -3.3, -0.9, 2.85
        mx = fx0 + 0.9 + 1.7
        frame = RoundedRectangle(corner_radius=0.12, width=fx1 - fx0, height=fy1 - fy0, stroke_color=GREY, stroke_width=4, fill_color=BG, fill_opacity=1).move_to([(fx0 + fx1) / 2, (fy0 + fy1) / 2, 0])
        tis = Rectangle(width=0.8, height=fy1 - fy0 - 0.1, stroke_width=0, fill_color=ORANGE, fill_opacity=0.5).move_to([fx0 + 0.45, (fy0 + fy1) / 2, 0])
        cell = Rectangle(width=1.7, height=fy1 - fy0 - 0.1, stroke_width=0, fill_color=GREY, fill_opacity=0.22).move_to([fx0 + 1.3 + 0.85, (fy0 + fy1) / 2, 0])
        lumen = Rectangle(width=fx1 - mx - 0.05, height=fy1 - fy0 - 0.1, stroke_width=0, fill_color=YELLOW, fill_opacity=0.25).move_to([(mx + fx1) / 2 - 0.02, (fy0 + fy1) / 2, 0])
        mem = Line([mx, fy1 - 0.05, 0], [mx, fy0 + 0.05, 0], color=GREY, stroke_width=6)
        zl1 = leader([DUCT_X - 0.2, 1.2, 0], [fx1 + 0.05, 1.2, 0], 0.5)
        cap = lab("duct cell (schematic)", 26, TEXT).move_to([(fx0 + fx1) / 2, fy0 - 0.85, 0])
        key = key_icon(1.0).move_to([fx0 + 0.45, 1.9, 0])
        kl = lab("ADH", 28, GOLD).next_to(key, DOWN, buff=0.12)
        ys = (2.15, 0.8, -0.35)
        doors = VGroup(*[VGroup(Rectangle(width=0.16, height=0.34, stroke_color=TEAL, stroke_width=4, fill_color=BG, fill_opacity=1),
                                 Line([-0.08, 0, 0], [0.08, 0, 0], color=TEAL, stroke_width=4)).move_to([mx, y, 0]) for y in ys])
        al = lab("aquaporin-2", 28, TEAL).move_to([-5.0, fy0 - 0.35, 0])
        self.add(frame, tis, cell, lumen, mem, zl1, cap, key, kl, doors, plate(al))
        # water crossing at the doors (inset) and leaving the duct at every depth (slice)
        wg = ValueTracker(0.0)
        ins = VGroup(*[particle("water", Route([(mx + 0.55, y + dy), (mx, y), (mx - 0.9, y - 0.05), (fx0 + 0.4, y - 0.05)]), 2.6, k / 6, wg, r=0.09, fin=0.08, fout=0.18)
                       for k, (y, dy) in enumerate([(2.15, 0.0), (0.8, 0.0), (-0.35, 0.0), (2.15, 0.0), (0.8, 0.0), (-0.35, 0.0)])])
        outs = VGroup()
        for i, yy in enumerate([2.4, 1.6, 0.8, 0.0, -0.8, -1.5]):
            xx = DUCT_X if yy > Y_TAPER else -2.0 * ((yy + 3.3) / 2.5)
            sgn = 1 if i % 2 == 0 else -1
            outs.add(particle("water", Route([(xx, yy), (xx + sgn * 0.45, yy), (xx + sgn * 0.9, yy)]), 2.4, i / 6, wg, r=0.09))
        self.add(ins, outs)
        self.at("water leaves the urine")
        wg.set_value(1.0)
        self.play(Indicate(doors, color=BLUE, scale_factor=1.3), run_time=1.4)
        self.at("into the concentrated medulla")
        self.play(Indicate(self.strips, color=ORANGE, scale_factor=1.0), run_time=1.0)
        self.at("the urine comes out concentrated")
        cl = lab("concentrated", 34, YELLOW).move_to([2.0, -3.3, 0], aligned_edge=LEFT)
        self.play(self.dcon.animate.set_value(1.0), FadeIn(cl, shift=LEFT * 0.1), run_time=2.0)
        self.at("take")
        self.play(key.animate.shift(UP * 1.4).set_opacity(0), kl.animate.set_opacity(0), run_time=1.3)
        self.at("the channels withdraw")
        wg.set_value(0.0)
        self.play(AnimationGroup(*[d.animate.move_to([fx0 + 1.9, y, 0]) for d, y in zip(doors, ys)], lag_ratio=0.2), run_time=1.6)
        dl = lab("dilute", 34, YELLOW).move_to([2.0, -3.3, 0], aligned_edge=LEFT)
        self.at("dilute urine flows out")
        self.play(self.dcon.animate.set_value(0.0), FadeOut(cl), FadeIn(dl, shift=LEFT * 0.1), run_time=1.6)
        self.finish()


class S14Close(Slice):
    def construct(self):
        full_state(self)
        self.dvis.set_value(1.0)
        self.dcon.set_value(0.8)
        self.lvis.set_value(0.7)
        flow = ValueTracker(1.0)
        self.flow_dots(flow, n=7)
        sg = ValueTracker(1.0)
        self.salt_out(sg, 8)
        drt = Route([(DUCT_X, TOP), (DUCT_X, Y_TAPER), (0.0, -3.3)])
        dg = ValueTracker(1.0)
        self.add(VGroup(*[particle("flow", drt, drt.L / 0.8, i / 7, dg, fin=0.03, fout=0.03, r=0.055) for i in range(7)]))
        key = key_icon(0.8).move_to([-3.45 - 0.0, 0.2, 0]).set_opacity(0)
        # water leaving the duct, the gold key in place
        wg = ValueTracker(0.0)
        outs = VGroup()
        for i, yy in enumerate([2.4, 1.6, 0.8, 0.0, -0.8, -1.5]):
            xx = DUCT_X if yy > Y_TAPER else -2.0 * ((yy + 3.3) / 2.5)
            sgn = 1 if i % 2 == 0 else -1
            outs.add(particle("water", Route([(xx, yy), (xx + sgn * 0.45, yy), (xx + sgn * 0.9, yy)]), 2.4, i / 6, wg, r=0.09))
        self.add(outs)
        ug = ValueTracker(0.0)
        ureas = VGroup(*[jiggler("urea", (-1.3, 0.2, -2.35, -0.5), 600 + i, 0.35, gate=ug, r=0.085) for i in range(9)])
        self.add(ureas)
        kk = key_icon(0.8).move_to([-3.9, 1.0, 0])
        kkl = lab("ADH", 34, GOLD).next_to(kk, DOWN, buff=0.1)
        self.at("never pumps water")
        self.play(Indicate(self.strips, color=ORANGE, scale_factor=1.0), run_time=1.5)
        self.at("moves solute first")
        sl = lab("salt", 32, ORANGE).move_to([3.3, 1.2, 0], aligned_edge=LEFT)
        sll = leader([3.25, 1.2, 0], [ASC_X + 0.9, 1.2, 0])
        self.play(FadeIn(plate(sl)), Create(sll), Indicate(self.loop_up[0], color=ORANGE, scale_factor=1.05), run_time=1.2)
        ug.set_value(1.0)
        zl = VGroup(dot("urea", 0.1), lab("urea", 32, TEXT)).arrange(RIGHT, buff=0.15).move_to([3.5, -1.2, 0], aligned_edge=LEFT)
        self.play(FadeIn(plate(zl)), run_time=0.8)
        self.at("a medulla more concentrated")
        self.play(self.go.animate.set_value(0.7), self.gi.animate.set_value(0.7), run_time=0.8)
        self.play(self.go.animate.set_value(1.0), self.gi.animate.set_value(1.0), run_time=1.0)
        self.play(Indicate(self.strips, color=ORANGE, scale_factor=1.0), run_time=1.0)
        self.at("water follows")
        wg.set_value(1.0)
        self.play(FadeIn(kk), FadeIn(kkl), FadeOut(sl), FadeOut(sll), FadeOut(zl), run_time=1.0)
        bar, terms = ledger_bar(lit=True)
        self.at("opens the way")
        self.play(FadeIn(bar, shift=DOWN * 0.2), run_time=0.8)
        bar2, terms2 = ledger_bar(lit=True, water=True)
        self.play(Transform(bar, bar2), run_time=0.6)
        self.play(Indicate(bar[1][4], color=GOLD, scale_factor=1.15), run_time=1.0)
        self.finish()


class S15End(EndCard):
    LINE = "No pump moves water: move solute first, and water follows."
