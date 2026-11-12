"""Two Animals on One Plot  (Biochemistrypedia explainer, tissues-and-homeostasis, film 2 of 2)

Same look and colour map as film 1 (../scenes.py): ORANGE = outside / leak, TEAL = inside / push-back,
dashed light teal = set point, strengths are dials. Plots are SCHEMATIC; every curve is computed from the
lesson's simple model: slope = leak / (leak + push-back), push-back strength P may change along the axis.
"""
import os
import numpy as np
from bp_style import *  # noqa: F401,F403

ORANGE = "#F29E4C"
TEAL_L = "#9FE8EC"
DIAG = "#C8C8C8"
MUSSEL_C = BLUE
CRAB_C = GREEN


def lab(text, size=28, color=TEXT, **kw):
    return T(text, size=size, color=color, **kw)


def new_clock(sc):
    sc.clk = ValueTracker(0)
    sc.clk.add_updater(lambda m, dt: m.increment_value(dt))
    sc.add(sc.clk)
    ambient(sc)


def ambient(sc, n=44):
    """Slow drifting motes behind the content (never a dead frame while the narrator speaks)."""
    import random
    rng = random.Random(os.environ.get("KX_SCENE_ID", "x"))
    W, H = config.frame_width, config.frame_height
    motes = VGroup()
    for _ in range(n):
        d = Dot(radius=rng.uniform(0.04, 0.09), color=rng.choice([TEAL, ORANGE, TEXT])).set_opacity(rng.uniform(0.18, 0.4))
        d.move_to([rng.uniform(-W / 2, W / 2), rng.uniform(-H / 2, H / 2), 0])
        d.v = (rng.uniform(-0.15, 0.15), rng.uniform(0.12, 0.3))
        motes.add(d)

    def drift(g, dt):
        for m in g:
            m.shift([m.v[0] * dt, m.v[1] * dt, 0])
            if m.get_y() > H / 2 + 0.1:
                m.shift(DOWN * (H + 0.2))
            if abs(m.get_x()) > W / 2 + 0.1:
                m.shift(RIGHT * (-np.sign(m.get_x()) * (W + 0.2)))
    motes.add_updater(drift)
    motes.set_z_index(-4)
    sc.add(motes)


def bracket(x0, x1, y, color, tick=0.14):
    return VGroup(Line([x0, y, 0], [x1, y, 0]), Line([x0, y - tick, 0], [x0, y + tick, 0]),
                  Line([x1, y - tick, 0], [x1, y + tick, 0])).set_stroke(color, 4)


def make_dial(center, color, getP, r=0.65, clk=None):
    face = Circle(radius=r, stroke_color=color, stroke_width=5, fill_color=BG, fill_opacity=1).move_to(center)
    ticks = VGroup(*[Line(np.array(center) + r * 0.78 * np.array([np.cos(a), np.sin(a), 0]),
                          np.array(center) + r * 0.95 * np.array([np.cos(a), np.sin(a), 0])).set_stroke(color, 3)
                     for a in np.linspace(0, np.pi, 7)])

    def needle():
        P = max(getP(), 0.0)
        th = np.pi * (1 - P / (P + 1))
        if clk is not None:
            th += 0.025 * np.sin(clk.get_value() * 3.1)
        tip = np.array(center) + r * 0.82 * np.array([np.cos(th), np.sin(th), 0])
        return VGroup(Line(center, tip).set_stroke(color, 6), Dot(center, radius=0.07, color=color))
    return VGroup(face, ticks, always_redraw(needle))


def man_mob(h=3.2):
    skin = "#E8C39E"
    head = Circle(radius=0.42, fill_color=skin, fill_opacity=1, stroke_width=0).move_to([0, 1.15, 0])
    eyes = VGroup(Dot([-0.15, 1.22, 0], radius=0.05, color=BG), Dot([0.15, 1.22, 0], radius=0.05, color=BG))
    smile = ArcBetweenPoints([-0.14, 1.02, 0], [0.14, 1.02, 0], angle=-1.3).set_stroke(BG, 3)
    torso = RoundedRectangle(corner_radius=0.2, width=1.3, height=1.55, fill_color="#7A5C9E", fill_opacity=1,
                             stroke_width=0).move_to([0, 0.05, 0])
    legs = VGroup(*[Rectangle(width=0.5, height=1.1, fill_color="#3B3350", fill_opacity=1, stroke_width=0
                              ).move_to([sx * 0.3, -1.15, 0]) for sx in (-1, 1)])
    arms = VGroup(*[Line([sx * 0.62, 0.6, 0], [sx * 0.9, -0.45, 0]).set_stroke("#7A5C9E", 16) for sx in (-1, 1)])
    return VGroup(legs, arms, torso, head, eyes, smile).set_height(h)


def sway(sc, mob, amp=0.035, f=1.6):
    mob._ang = 0.0
    c = mob.get_bottom()

    def up(m, dt):
        a = amp * np.sin(sc.clk.get_value() * f)
        m.rotate(a - m._ang, about_point=c)
        m._ang = a
    mob.add_updater(up)
    return mob


def mussel_mob(w=2.0):
    shell = Ellipse(width=2.0, height=1.25, fill_color="#33497F", fill_opacity=1, stroke_color="#9DB4E8", stroke_width=4)
    rings = VGroup(*[Arc(radius=0.35 * k, start_angle=0.5, angle=2.2, stroke_color="#9DB4E8", stroke_width=3,
                         arc_center=[-0.8, -0.1, 0]) for k in (1, 2, 3)])
    lip = Line([-1.0, 0.0, 0], [1.0, 0.0, 0]).set_stroke("#1d2a4d", 3)
    return VGroup(shell, rings, lip).set_width(w)


def crab_mob(w=2.0):
    body = Ellipse(width=1.7, height=1.1, fill_color="#4E9E4A", fill_opacity=1, stroke_color="#A5E3A0", stroke_width=4)
    legs = VGroup(*[Line([sx * 0.7, -0.1 - 0.15 * k, 0], [sx * (1.25 + 0.1 * k), -0.55 - 0.18 * k, 0]).set_stroke("#A5E3A0", 5)
                    for sx in (-1, 1) for k in range(3)])
    arms = VGroup(*[Line([sx * 0.6, 0.35, 0], [sx * 1.0, 0.85, 0]).set_stroke("#A5E3A0", 6) for sx in (-1, 1)])
    claws = VGroup(*[Circle(radius=0.26, fill_color="#4E9E4A", fill_opacity=1, stroke_color="#A5E3A0",
                            stroke_width=4).move_to([sx * 1.05, 1.0, 0]) for sx in (-1, 1)])
    eyes = VGroup(*[Dot([sx * 0.25, 0.4, 0], radius=0.09, color=WHITE) for sx in (-1, 1)])
    return VGroup(legs, arms, claws, body, eyes).set_width(w)


def fish_mob(w=1.8):
    body = Ellipse(width=1.6, height=0.8, fill_color="#5B9BD5", fill_opacity=1, stroke_color="#BFE0FF", stroke_width=3)
    tail = Polygon([-0.7, 0, 0], [-1.25, 0.4, 0], [-1.25, -0.4, 0], fill_color="#5B9BD5", fill_opacity=1,
                   stroke_color="#BFE0FF", stroke_width=3)
    eye = Dot([0.45, 0.1, 0], radius=0.07, color=WHITE)
    return VGroup(tail, body, eye).set_width(w)


# ------------------------------------------------------------------------------------ model (computed)
def crab_curve(k=12.0, f0=0.75):
    """Blood osmolality of the crab from the simple model: slope = L / (L + P(f)), P grows as the water
    gets more dilute below f0. Integrated downward from full seawater, where blood = water."""
    fs = np.linspace(1.0, 0.15, 400)
    g = np.empty_like(fs)
    g[0] = 1.0
    for i in range(1, len(fs)):
        fm = 0.5 * (fs[i] + fs[i - 1])
        slope = 1.0 / (1.0 + k * max(0.0, f0 - fm))
        g[i] = g[i - 1] - slope * (fs[i - 1] - fs[i])
    order = np.argsort(fs)
    return lambda f: float(np.interp(f, fs[order], g[order]))


crab_g = crab_curve()
FLAT_G = 0.8
FM = [1.0, 0.9, 0.8, 0.7, 0.6, 0.5, 0.4, 0.35]
FJ = [0.01, -0.015, 0.012, -0.01, 0.015, -0.012, 0.01, -0.01]
FC = [1.0, 0.9, 0.8, 0.7, 0.6, 0.5, 0.4, 0.3, 0.2]
FCJ = [0.0, 0.0, 0.01, -0.012, 0.012, -0.01, 0.01, -0.01, 0.01]


class Plot:
    def __init__(s, sc, ox, oy, w, h, xl, yl, xt, yt, xsize=28, ysize=26):
        s.sc, s.ox, s.oy, s.w, s.h = sc, ox, oy, w, h
        s.fp = ValueTracker(0.6)
        s.fp.auto = None
        s.gf = None
        s.vline = True
        s.show_probe = ValueTracker(0)
        sc.add(s.fp, s.show_probe)

        def drift(m, dt):
            if m.auto:
                lo, hi, per, ph = m.auto
                c, a = (lo + hi) / 2, (hi - lo) / 2
                m.set_value(c + a * np.sin(2 * np.pi * sc.clk.get_value() / per + ph))
        s.fp.add_updater(drift)
        s.xax = Line([ox, oy, 0], [ox + w + 0.15, oy, 0]).set_stroke(TEXT, 5)
        s.yax = Line([ox, oy, 0], [ox, oy + h + 0.15, 0]).set_stroke(TEXT, 5)
        s.xl = lab(xl, xsize, TEXT).move_to([ox + w / 2, oy - 0.82, 0])
        s.yl = lab(yl, ysize, TEXT).rotate(PI / 2).move_to([ox - 0.7, oy + h / 2, 0])
        s.xt = VGroup(lab(xt[0], 24, TEXT).move_to([ox + 0.4, oy - 0.3, 0]),
                      lab(xt[1], 24, TEXT).move_to([ox + w - 0.7, oy - 0.3, 0]))
        s.yt = VGroup(lab(yt[0], 24, TEXT).rotate(PI / 2).move_to([ox - 0.3, oy + 0.45, 0]),
                      lab(yt[1], 24, TEXT).rotate(PI / 2).move_to([ox - 0.3, oy + h - 0.45, 0]))
        panel = Rectangle(width=w + 0.15, height=h + 0.15, fill_color="#26384d", fill_opacity=1, stroke_width=0
                          ).move_to([ox + (w + 0.15) / 2, oy + (h + 0.15) / 2, 0]).set_z_index(-5)
        s.frame = VGroup(panel, s.xax, s.yax)

    def px(s, f):
        return s.ox + s.w * f

    def py(s, g):
        return s.oy + s.h * g

    def pt(s, f, g):
        return np.array([s.px(f), s.py(g), 0.0])

    def line(s, f0, f1, g0, g1, color, width=6, dashed=False):
        a, b = s.pt(f0, g0), s.pt(f1, g1)
        return (DashedLine(a, b, color=color, stroke_width=width, dash_length=0.18) if dashed
                else Line(a, b).set_stroke(color, width))

    def diag(s, color=DIAG, width=5, op=1.0):
        return Line(s.pt(0.02, 0.02), s.pt(0.98, 0.98)).set_stroke(color, width, opacity=op)

    def curve(s, gfun, f0, f1, color, width=7, n=60):
        fs = np.linspace(f0, f1, n)
        return VMobject().set_points_smoothly([s.pt(f, gfun(f)) for f in fs]).set_stroke(color, width)

    def probe(s):
        def f():
            if s.show_probe.get_value() < 0.5:
                return VGroup()
            fv = s.fp.get_value()
            g = VGroup(Dot(s.pt(fv, 0), radius=0.14, color=ORANGE))
            if s.vline:
                g.add(DashedLine(s.pt(fv, 0), s.pt(fv, s.gf(fv) if s.gf else 1.0), color=ORANGE, stroke_width=4,
                                 dash_length=0.14))
            if s.gf:
                g.add(Dot(s.pt(fv, s.gf(fv)), radius=0.15, color=TEAL))
            return g.set_z_index(6)
        return always_redraw(f)

    def dots(s, fs, js, gfun, color, r=0.11):
        return VGroup(*[Dot(s.pt(f, gfun(f) + j), radius=r, color=color) for f, j in zip(fs, js)])


def plot_a(sc):
    return Plot(sc, -5.5, -2.6, 5.6, 5.0, "water osmolality (outside)", "blood osmolality (inside)",
                ("dilute", "full seawater"), ("low", "high"))


def plot_b(sc):
    return Plot(sc, 1.9, -2.6, 4.65, 5.0, "outside temperature", "body (core) temperature",
                ("cold", "hot"), ("low", "high"), xsize=26, ysize=24)


def tag_schematic():
    return lab("schematic", 24, TEXT).move_to([-5.7, 3.45, 0])


def add_axes_plain(sc, p, ticks=True):
    sc.add(p.frame, p.xl, p.yl)
    if ticks:
        sc.add(p.xt, p.yt)


def colour_axes(p):
    return [p.xax.animate.set_stroke(ORANGE), p.xl.animate.set_color(ORANGE), p.xt.animate.set_color(ORANGE),
            p.yax.animate.set_stroke(TEAL), p.yl.animate.set_color(TEAL), p.yt.animate.set_color(TEAL)]


def plot_colored(sc, p):
    add_axes_plain(sc, p)
    p.xax.set_stroke(ORANGE)
    p.xl.set_color(ORANGE)
    p.xt.set_color(ORANGE)
    p.yax.set_stroke(TEAL)
    p.yl.set_color(TEAL)
    p.yt.set_color(TEAL)


# ======================================================================================= scenes
class S00Title(TitleCard):
    LESSON = "Tissues, Organs and Homeostasis"
    TITLE = "Two Animals on One Plot"


class S01Question(SpokenScene):
    def construct(self):
        new_clock(self)
        tank = Rectangle(width=9.0, height=5.2, stroke_color=GREY, stroke_width=5).move_to([-1.5, -0.5, 0])
        sand = Rectangle(width=8.8, height=0.5, fill_color="#8a7350", fill_opacity=1, stroke_width=0).move_to([-1.5, -2.85, 0])
        wop = ValueTracker(0.55)
        self.add(wop)
        water = always_redraw(lambda: Rectangle(width=8.8, height=4.1, fill_color=ORANGE, fill_opacity=wop.get_value(),
                                                stroke_width=0).move_to([-1.5, -1.0, 0]))
        mussel = mussel_mob(1.9).move_to([-3.9, -2.15, 0])
        crab = sway(self, crab_mob(2.0).move_to([0.9, -2.0, 0]), amp=0.05, f=2.2)
        bub = VGroup(*[Circle(radius=0.07, stroke_color=WHITE, stroke_width=2).set_opacity(0.6) for _ in range(5)])
        for i, b in enumerate(bub):
            b.ph = i * 0.37
            b.bx = -5.2 + i * 1.9

        def rise(m, dt):
            for b in m:
                b.ph = (b.ph + dt * 0.12) % 1.0
                b.move_to([b.bx + 0.15 * np.sin(b.ph * 12), -2.4 + 3.4 * b.ph, 0])
        bub.add_updater(rise)
        l_m = lab("mussel", 28, TEXT).move_to([-3.9, -3.45, 0])
        l_c = lab("shore crab", 28, TEXT).move_to([0.9, -3.45, 0])
        self.add(water)
        self.play(FadeIn(tank), FadeIn(sand), run_time=0.8)
        self.add(bub)
        self.play(FadeIn(mussel, shift=DOWN * 0.2), FadeIn(l_m), run_time=1.0)
        self.at("shore crab")
        self.play(FadeIn(crab, shift=DOWN * 0.2), FadeIn(l_c), run_time=1.0)
        self.at("into water")
        jug = VGroup(RoundedRectangle(corner_radius=0.2, width=1.1, height=1.4, fill_color="#8CC7E8", fill_opacity=0.9,
                                      stroke_width=0),
                     Polygon([-0.4, 0.7, 0], [-0.9, 0.9, 0], [-0.9, 0.55, 0], [-0.4, 0.3, 0], fill_color="#8CC7E8",
                             fill_opacity=0.9, stroke_width=0)).rotate(0.55).move_to([0.4, 2.95, 0])
        drops = always_redraw(lambda: VGroup(*[
            Circle(radius=0.09, stroke_width=0, fill_color="#8CC7E8", fill_opacity=0.95).move_to(
                [-0.55 + 0.05 * k, 2.2 - ((self.clk.get_value() * 1.3 + k / 4) % 1.0) * 1.2, 0]) for k in range(4)]))
        l_h = lab("half-strength seawater", 28, ORANGE).move_to([-3.4, 2.75, 0])
        self.play(FadeIn(jug, shift=DOWN * 0.3), run_time=0.5)
        self.add(drops)
        self.at("diluted to half strength")
        self.play(wop.animate.set_value(0.22), FadeIn(l_h), run_time=2.0)
        self.at("Whose blood follows")
        q = lab("?", 96, YELLOW, weight=BOLD).move_to([-1.5, -0.7, 0])
        q.add_updater(lambda m: m.set_opacity(0.6 + 0.4 * np.sin(self.clk.get_value() * 4)))
        self.play(FadeIn(q, scale=0.5), run_time=0.6)
        self.at("The first film built a dial")
        d1 = make_dial([3.9, 1.4, 0], ORANGE, lambda: 1.0, r=0.6, clk=self.clk)
        d2 = make_dial([3.9, -0.7, 0], TEAL, lambda: 1.0, r=0.6, clk=self.clk)
        t1 = lab("leak\nstrength", 28, ORANGE).move_to([5.7, 1.4, 0])
        t2 = lab("push-back\nstrength", 28, TEAL).move_to([5.8, -0.7, 0])
        self.play(FadeIn(d1, shift=LEFT * 0.3), FadeIn(t1), run_time=0.8)
        self.play(FadeIn(d2, shift=LEFT * 0.3), FadeIn(t2), run_time=0.8)
        self.at("Now we read")
        self.play(Indicate(t1, color=ORANGE, scale_factor=1.12), Indicate(t2, color=TEAL, scale_factor=1.12), run_time=1.4)
        self.finish()


def particles(sc, box_c, n, color=ORANGE, w=2.0, h=2.2):
    box = Rectangle(width=w, height=h, stroke_color=GREY, stroke_width=3).move_to(box_c)
    ds = VGroup(*[Dot(radius=0.09, color=color) for _ in range(n)])
    rng = np.random.RandomState(n)
    par = [(rng.uniform(-0.8, 0.8), rng.uniform(-0.9, 0.9), rng.uniform(0.6, 1.4), rng.uniform(0, 6)) for _ in range(n)]

    def mv(m, dt):
        t = sc.clk.get_value()
        for d, (x, y, sp, ph) in zip(m, par):
            d.move_to(np.array(box_c) + [x + 0.15 * np.sin(sp * t + ph), y + 0.15 * np.cos(sp * 1.3 * t + ph), 0])
    ds.add_updater(mv)
    mv(ds, 0)
    return VGroup(box, ds)


class S02Axes(SpokenScene):
    def construct(self):
        new_clock(self)
        p = plot_a(self)
        self.play(Create(p.xax), Create(p.yax), run_time=1.2)
        self.at("Across the bottom")
        self.play(FadeIn(p.xl, shift=UP * 0.1), FadeIn(p.xt), run_time=1.0)
        self.at("the concentration of dissolved particles")
        b1 = particles(self, [2.9, 0.5, 0], 5)
        b2 = particles(self, [5.5, 0.5, 0], 20)
        c1 = lab("dilute", 26, ORANGE).move_to([2.9, -0.85, 0])
        c2 = lab("concentrated", 26, ORANGE).move_to([5.5, -0.85, 0])
        self.play(FadeIn(b1), FadeIn(c1), run_time=0.8)
        self.play(FadeIn(b2), FadeIn(c2), run_time=0.8)
        self.at("Up the side")
        self.play(FadeIn(p.yl, shift=RIGHT * 0.1), FadeIn(p.yt), run_time=1.0)
        self.at("Orange marks the outside")
        self.play(*colour_axes(p), run_time=1.4)
        tag = tag_schematic()
        self.play(FadeIn(tag), run_time=0.5)
        self.play(Indicate(p.xl, color=ORANGE, scale_factor=1.06), run_time=1.0)
        self.play(Indicate(p.yl, color=TEAL, scale_factor=1.06), run_time=1.0)
        self.finish()


def gauge_bars(sc, p):
    """Two bars in the right column tied to the probe: outside (orange) and inside (teal)."""
    bx = (2.7, 4.7)
    bw = 1.1
    tubes = VGroup(*[Rectangle(width=bw, height=p.h, stroke_color=GREY, stroke_width=3).move_to([x, p.oy + p.h / 2, 0])
                     for x in bx])
    bo = always_redraw(lambda: Rectangle(width=bw - 0.1, height=max(0.05, p.h * p.fp.get_value()), stroke_width=0,
                                         fill_color=ORANGE, fill_opacity=0.92).move_to(
        [bx[0], p.oy + max(0.05, p.h * p.fp.get_value()) / 2, 0]))
    bi = always_redraw(lambda: Rectangle(width=bw - 0.1, height=max(0.05, p.h * p.gf(p.fp.get_value())), stroke_width=0,
                                         fill_color=TEAL, fill_opacity=0.92).move_to(
        [bx[1], p.oy + max(0.05, p.h * p.gf(p.fp.get_value())) / 2, 0]))
    lo = lab("water", 26, ORANGE).move_to([bx[0], p.oy - 0.4, 0])
    li = lab("blood", 26, TEAL).move_to([bx[1], p.oy - 0.4, 0])
    return tubes, bo, bi, lo, li


class S03Lines(SpokenScene):
    def construct(self):
        new_clock(self)
        p = plot_a(self)
        plot_colored(self, p)
        tag = tag_schematic()
        self.add(tag)
        p.gf = lambda f: f
        p.fp.set_value(0.6)
        p.fp.auto = (0.25, 0.9, 7.0, 0.0)
        p.show_probe.set_value(1)
        self.add(p.probe())
        dg = p.diag()
        self.play(Create(dg), run_time=1.8)
        self.at("Along it, blood equals water")
        tubes, bo, bi, lo, li = gauge_bars(self, p)
        self.play(FadeIn(tubes), FadeIn(lo), FadeIn(li), run_time=0.8)
        self.add(bo, bi)
        l_d = lab("blood = water", 28, DIAG).move_to([-3.4, 1.35, 0])
        self.play(FadeIn(l_d), run_time=0.7)
        self.at("That is a perfect conformer")
        l_c = lab("ideal conformer", 30, YELLOW, weight=BOLD).move_to([-3.4, 1.9, 0])
        self.play(FadeIn(l_c, scale=1.1), run_time=0.7)
        self.at("Then draw a flat line")
        self.play(dg.animate.set_stroke(opacity=0.4), FadeOut(l_d), FadeOut(l_c), run_time=0.6)
        flat = p.line(0.3, 0.9, FLAT_G, FLAT_G, TEAL, 8)
        p.gf = lambda f: FLAT_G
        self.play(Create(flat), run_time=1.4)
        self.at("the blood stays put")
        l_f = VGroup(lab("ideal regulator:", 28, TEAL, weight=BOLD), lab("blood held", 28, TEAL)).arrange(
            DOWN, aligned_edge=LEFT, buff=0.08).move_to([-3.2, 2.0, 0])
        self.play(FadeIn(l_f, shift=DOWN * 0.1), run_time=0.8)
        self.at("That is a perfect regulator")
        self.play(Indicate(l_f, color=YELLOW, scale_factor=1.1), run_time=1.0)
        self.at("Over the range")
        br = bracket(p.px(0.3), p.px(0.9), p.oy + 0.35, ORANGE)
        l_r = lab("range it survives", 26, ORANGE).move_to([p.px(0.6), p.oy + 0.75, 0])
        l_r.set_z_index(9)
        l_bg = BackgroundRectangle(l_r, color="#253650", fill_opacity=0.95, buff=0.06).set_z_index(8)
        self.play(Create(br), FadeIn(VGroup(l_bg, l_r)), run_time=1.0)
        self.finish()


class S04Slope(SpokenScene):
    def construct(self):
        new_clock(self)
        p = plot_a(self)
        plot_colored(self, p)
        self.add(tag_schematic())
        dg = p.diag(op=0.5)
        flat = p.line(0.3, 0.9, FLAT_G, FLAT_G, TEAL, 6).set_stroke(opacity=0.4)
        self.add(dg, flat)
        Pt = ValueTracker(0.1)
        self.add(Pt)
        d1 = make_dial([2.3, 1.7, 0], ORANGE, lambda: 1.0, r=0.7, clk=self.clk)
        d2 = make_dial([2.3, -0.3, 0], TEAL, lambda: Pt.get_value(), r=0.7, clk=self.clk)
        t1 = lab("leak\nstrength", 28, ORANGE).move_to([4.2, 1.7, 0])
        t2 = lab("push-back\nstrength", 28, TEAL).move_to([4.5, -0.3, 0])
        self.add(d1, d2, t1, t2)
        # triangle on the diagonal
        a, b, c = p.pt(0.35, 0.35), p.pt(0.6, 0.35), p.pt(0.6, 0.6)
        lh = Line(a, b).set_stroke(ORANGE, 8)
        lv = Line(b, c).set_stroke(TEAL, 8)
        self.play(Create(lh), run_time=2.7)
        self.at("outside change")
        l_oc = lab("outside change", 28, ORANGE).move_to([p.px(0.475) + 1.0, p.py(0.35) - 0.45, 0])
        self.play(FadeIn(l_oc), run_time=0.5)
        self.at("gets inside")
        self.play(Create(lv), run_time=1.0)
        l_ic = lab("inside\nchange", 28, TEAL).move_to([p.px(0.6) + 1.0, p.py(0.475), 0])
        self.play(FadeIn(l_ic), run_time=0.6)
        self.at("In the simple model")
        cap = VGroup(lab("slope = leak strength ÷", 26, YELLOW), lab("(leak + push-back strength)", 26, YELLOW)
                     ).arrange(DOWN, buff=0.08).move_to([3.9, -1.9, 0])
        self.play(FadeIn(cap, shift=UP * 0.1), run_time=0.6)
        test = always_redraw(lambda: Line(p.pt(0.25, 0.6 + (0.25 - 0.6) / (1 + Pt.get_value())),
                                          p.pt(0.95, 0.6 + (0.95 - 0.6) / (1 + Pt.get_value()))).set_stroke(YELLOW, 7).set_z_index(4))
        self.play(FadeOut(lh), FadeOut(lv), FadeOut(l_oc), FadeOut(l_ic), FadeIn(test), run_time=0.4)
        self.at("steep means")
        self.play(Indicate(t1, color=ORANGE, scale_factor=1.15), run_time=1.0)
        T1 = max(0.5, self.t_of("Flat means") - 0.2 - self.elapsed())
        self.play(Pt.animate(rate_func=linear).set_value(0.35), run_time=T1)
        self.at("Flat means")
        self.play(Pt.animate(rate_func=smooth).set_value(9.0), Indicate(t2, color=TEAL, scale_factor=1.15), run_time=3.0)
        self.at("A line halfway between")
        self.play(Pt.animate(rate_func=smooth).set_value(1.0), run_time=2.0)
        self.play(Indicate(t1, color=ORANGE, scale_factor=1.12), Indicate(t2, color=TEAL, scale_factor=1.12), run_time=1.2)
        self.finish()


def base_a(sc, with_flat=False, mussel=False, crab_dot=False):
    p = plot_a(sc)
    plot_colored(sc, p)
    sc.add(tag_schematic())
    dg = p.diag()
    sc.add(dg)
    extra = {}
    if with_flat:
        extra["flat"] = p.line(0.3, 0.9, FLAT_G, FLAT_G, TEAL, 6).set_stroke(opacity=0.5)
        sc.add(extra["flat"])
    if mussel:
        extra["md"] = p.dots(FM, FJ, lambda f: f, MUSSEL_C)
        extra["md"].set_opacity(0.5 if crab_dot else 1.0)
        sc.add(extra["md"])
    if crab_dot:
        extra["cd"] = Dot(p.pt(1.0, 1.0), radius=0.19, color=CRAB_C).set_z_index(5)
        sc.add(extra["cd"])
    return p, extra


class S05Mussel(SpokenScene):
    def construct(self):
        new_clock(self)
        p, _ = base_a(self)
        mus = sway(self, mussel_mob(2.6).move_to([3.7, 1.0, 0]), amp=0.04, f=1.9)
        self.at("Now the blue")
        self.play(FadeIn(mus, shift=LEFT * 0.4), run_time=1.0)
        n1 = VGroup(lab("blue mussel", 30, BLUE, weight=BOLD), T("Mytilus edulis", 28, TEXT, slant=ITALIC)
                    ).arrange(DOWN, buff=0.12).move_to([3.7, -0.9, 0])
        self.play(FadeIn(n1), run_time=0.7)
        self.at("dilute its water")
        p.fp.set_value(1.0)
        p.gf = None
        p.show_probe.set_value(1)
        self.add(p.probe())
        dots = VGroup()
        T_each = 0.55
        for f, j in zip(FM, FJ):
            d = Dot(p.pt(f, f + j), radius=0.11, color=MUSSEL_C)
            dots.add(d)
            self.play(p.fp.animate(rate_func=smooth).set_value(f), run_time=0.35)
            self.play(FadeIn(d, scale=2.0), run_time=0.2)
            if self.t_of("over the salinities") - 0.2 - self.elapsed() < 0.4 and f < 0.8:
                break
        self.at("over the salinities")
        p.vline = False
        brk = bracket(p.px(0.33), p.px(1.0), p.oy + 0.4, BLUE)
        l_s = lab("salinities it tolerates", 26, BLUE).move_to([p.px(0.66), p.oy + 0.8, 0])
        self.play(Create(brk), FadeIn(l_s), run_time=0.9)
        done = len(dots)
        for f, j in list(zip(FM, FJ))[done:]:
            d = Dot(p.pt(f, f + j), radius=0.11, color=MUSSEL_C)
            dots.add(d)
            self.play(p.fp.animate(rate_func=smooth).set_value(f), FadeIn(d, scale=2.0), run_time=0.4)
        p.fp.auto = (0.33, 1.0, 5.0, -PI / 2)
        self.at("Its points fall along")
        self.play(Indicate(dots, color=BLUE, scale_factor=1.5), run_time=1.4)
        self.at("the muscle conforms")
        l_c = lab("conformer", 32, YELLOW, weight=BOLD).move_to([-1.2, -1.3, 0])
        self.play(FadeOut(brk), FadeOut(l_s), FadeIn(l_c, scale=1.1), run_time=0.8)
        self.at("That label covers")
        l_v = lab("this one variable", 28, TEXT).move_to([-1.3, -1.85, 0])
        self.play(FadeIn(l_v, shift=UP * 0.1), run_time=0.8)
        self.finish()


class S06Crab(SpokenScene):
    def construct(self):
        new_clock(self)
        p, ex = base_a(self, mussel=True)
        ex["md"].set_opacity(0.5)
        mus = sway(self, mussel_mob(1.2).move_to([5.7, 2.6, 0]), amp=0.04, f=1.9)
        self.add(mus)
        crab = sway(self, crab_mob(2.8).move_to([8.2, 0.9, 0]), amp=0.05, f=2.2)
        self.add(crab)
        self.at("Now the shore crab")
        self.play(crab.animate.move_to([3.7, 0.9, 0]), run_time=1.6)
        nm = VGroup(lab("shore crab", 30, GREEN, weight=BOLD), T("Carcinus maenas", 28, TEXT, slant=ITALIC)
                    ).arrange(DOWN, buff=0.12).move_to([3.7, -0.9, 0])
        self.play(FadeIn(nm), run_time=0.7)
        self.at("In full")
        cd = Dot(p.pt(1.0, 1.0), radius=0.19, color=CRAB_C).set_z_index(5)
        l_cd = lab("crab", 28, GREEN).move_to([p.px(1.0) - 0.7, p.py(1.0) + 0.45, 0])
        self.play(Create(DashedLine(p.pt(1.0, 0), p.pt(1.0, 1.0), color=ORANGE, stroke_width=4, dash_length=0.14)), run_time=0.8)
        self.play(FadeIn(cd, scale=2.5), FadeIn(l_cd), run_time=0.8)
        ring = always_redraw(lambda: Circle(radius=0.3 + 0.12 * np.sin(self.clk.get_value() * 4), stroke_color=GREEN,
                                            stroke_width=4).move_to(cd.get_center()))
        self.add(ring)
        self.at("near the diagonal")
        self.play(Indicate(ex["md"][0], color=YELLOW, scale_factor=1.8), run_time=1.2)
        self.at("So far")
        self.play(mus.animate.scale(1.6).move_to([5.4, 2.1, 0]), run_time=1.0)
        self.finish()


def lit(c, on):
    c[0].set_fill(TEAL, opacity=0.5 if on else 0.1)
    c[0].set_stroke(TEAL, opacity=1.0 if on else 0.5)
    c[1].set_opacity(1.0 if on else 0.55)


def ghost_and_cards(sc, p):
    ys = {"flat": FLAT_G, "between": crab_g(0.5), "diagonal": 0.5}
    cs = {k: chip(k, TEAL, size=30).move_to([4.2, y, 0]) for k, y in zip(("flat", "between", "diagonal"), (1.4, 0.3, -0.8))}
    q = lab("crab's blood sits…", 28, TEAL).move_to([4.2, 2.4, 0])
    rings = VGroup(*[DashedVMobject(Circle(radius=0.22, stroke_color=TEAL, stroke_width=4).move_to(p.pt(0.5, y)))
                     for y in ys.values()])
    return ys, cs, q, rings


class S07Predict(SpokenScene):
    def construct(self):
        new_clock(self)
        p, ex = base_a(self, with_flat=True, mussel=True, crab_dot=True)
        self.at("Now dilute the water")
        p.fp.set_value(1.0)
        p.gf = None
        p.show_probe.set_value(1)
        self.add(p.probe())
        self.play(p.fp.animate(rate_func=smooth).set_value(0.5), run_time=2.0)
        l_h = lab("half strength", 28, ORANGE).move_to([p.px(0.5) + 1.3, p.py(0.0) + 0.55, 0]).set_z_index(7)
        self.play(FadeIn(l_h), run_time=0.5)
        self.at("Will the crab's blood")
        ys, cs, q, rings = ghost_and_cards(self, p)
        ghost = always_redraw(lambda: Dot(p.pt(0.5, 0.65 + 0.15 * np.sin(self.clk.get_value() * 2.0)), radius=0.17,
                                          color=GREEN).set_opacity(0.8).set_z_index(6))
        self.add(ghost)
        self.play(FadeIn(rings), FadeIn(q), FadeIn(cs["flat"], shift=LEFT * 0.2), FadeIn(cs["between"], shift=LEFT * 0.2),
                  FadeIn(cs["diagonal"], shift=LEFT * 0.2), run_time=1.4)
        self.at("or in between")
        self.play(Indicate(cs["between"], color=YELLOW, scale_factor=1.15), run_time=1.0)
        self.finish()


class S08Pause(NarratedScene):
    def construct(self):
        new_clock(self)
        p, ex = base_a(self, with_flat=True, mussel=True, crab_dot=True)
        p.fp.set_value(0.5)
        p.gf = None
        p.show_probe.set_value(1)
        self.add(p.probe())
        l_h = lab("half strength", 28, ORANGE).move_to([p.px(0.5) + 1.3, p.py(0.0) + 0.55, 0]).set_z_index(7)
        self.add(l_h)
        ys, cs, q, rings = ghost_and_cards(self, p)
        names = ("flat", "between", "diagonal")
        pos = ValueTracker(0.0)
        self.add(pos)

        def gy():
            t = pos.get_value()
            i = int(t) % 3
            return ys[names[i]]
        ghost = always_redraw(lambda: Dot(p.pt(0.5, gy() + 0.02 * np.sin(self.clk.get_value() * 6)), radius=0.17,
                                          color=GREEN).set_z_index(6))
        self.add(rings, q, *cs.values(), ghost)
        for k, c in cs.items():
            c.add_updater(lambda m, k=k: lit(m, names[int(pos.get_value()) % 3] == k))
        ring_bg = Circle(radius=0.38, stroke_color=GREY, stroke_width=5).move_to([6.1, 3.15, 0])
        prog = ValueTracker(0.0)
        ring = always_redraw(lambda: Arc(radius=0.38, start_angle=PI / 2, angle=-TAU * max(prog.get_value(), 0.001),
                                         stroke_color=TEAL, stroke_width=7).move_to(ring_bg.get_center()))
        self.add(ring_bg, ring)
        self.play(prog.animate.set_value(1.0), pos.animate.set_value(5.99), run_time=4.8, rate_func=linear)
        self.finish()


def curve_dots(p, upto=None):
    return p.dots(FC, FCJ, crab_g, CRAB_C)


class S09Reveal(SpokenScene):
    def construct(self):
        new_clock(self)
        p, ex = base_a(self, with_flat=True, mussel=True, crab_dot=True)
        p.fp.set_value(0.5)
        p.gf = None
        p.show_probe.set_value(1)
        self.add(p.probe())
        l_h = lab("half strength", 28, ORANGE).move_to([p.px(0.5) + 1.3, p.py(0.0) + 0.55, 0]).set_z_index(7)
        self.add(l_h)
        ys, cs, q, rings = ghost_and_cards(self, p)
        self.add(q, *cs.values())
        for k, c in cs.items():
            lit(c, False)
        self.at("In between")
        lit(cs["between"], True)
        real = Dot(p.pt(0.5, crab_g(0.5)), radius=0.19, color=CRAB_C).set_z_index(6)
        self.play(Indicate(cs["between"], color=YELLOW, scale_factor=1.15), FadeIn(real, scale=2.5), run_time=0.8)
        ring = always_redraw(lambda: Circle(radius=0.3 + 0.1 * np.sin(self.clk.get_value() * 4), stroke_color=GREEN, stroke_width=4).move_to(real.get_center()))
        self.add(ring)
        self.at("the crab holds its blood")
        br = Line(p.pt(0.5, 0.5), p.pt(0.5, crab_g(0.5))).set_stroke(YELLOW, 8)
        l_ab = lab("well above\nthe water", 28, YELLOW).move_to([p.px(0.5) - 1.5, p.py((0.5 + crab_g(0.5)) / 2) - 0.2, 0])
        self.play(Create(br), FadeIn(l_ab), run_time=0.8)
        self.at("Its line bends flatter")
        self.play(FadeOut(q), FadeOut(cs["flat"]), FadeOut(cs["diagonal"]), FadeOut(cs["between"]), FadeOut(l_ab),
                  FadeOut(br), FadeOut(l_h), run_time=0.4)
        crv = p.curve(crab_g, 1.0, 0.15, CRAB_C, 7)
        cdots = VGroup(*[Dot(p.pt(f, crab_g(f) + j), radius=0.11, color=CRAB_C) for f, j in zip(FC, FCJ) if f != 1.0])
        p.vline = False
        self.play(Create(crv), run_time=2.2)
        self.play(FadeIn(cdots, lag_ratio=0.2), run_time=0.8)
        p.gf = crab_g
        p.fp.auto = (0.25, 0.95, 7.0, -PI / 2)
        self.at("conforms at one end")
        l_cf = lab("conforms here", 28, YELLOW).move_to([p.px(0.89), -1.3, 0])
        self.play(FadeIn(l_cf), run_time=0.7)
        self.at("regulates at the other")
        l_rg = lab("regulates here", 28, YELLOW).move_to([p.px(0.375), 1.95, 0])
        arr = Arrow(p.pt(0.3, crab_g(0.3) - 0.16), p.pt(0.3, crab_g(0.3) - 0.02), buff=0, color=TEAL, stroke_width=10, tip_length=0.3)
        l_pb = lab("pull up", 26, TEAL).move_to([p.px(0.3) + 0.1, p.py(crab_g(0.3)) + 0.6, 0])
        self.play(GrowArrow(arr), FadeIn(l_pb), FadeIn(l_rg), run_time=1.0)
        self.finish()


def crab_scene_base(sc, with_probe=True):
    p, ex = base_a(sc, mussel=True)
    crv = p.curve(crab_g, 1.0, 0.15, CRAB_C, 7)
    cd = VGroup(*[Dot(p.pt(f, crab_g(f) + j), radius=0.11, color=CRAB_C) for f, j in zip(FC, FCJ)])
    sc.add(crv, cd)
    p.gf = crab_g
    if with_probe:
        p.fp.auto = (0.25, 0.95, 8.0, 0.0)
        p.show_probe.set_value(1)
        sc.add(p.probe())
    return p, ex, crv, cd


class S10Label(SpokenScene):
    def construct(self):
        new_clock(self)
        p, ex, crv, cd = crab_scene_base(self, with_probe=False)
        l_cf = lab("conforms here", 28, YELLOW).move_to([p.px(0.89), -1.3, 0])
        l_rg = lab("regulates here", 28, YELLOW).move_to([p.px(0.375), 1.95, 0])
        self.add(l_cf, l_rg)
        cr = sway(self, crab_mob(2.6).move_to([3.7, 0.9, 0]), amp=0.05, f=2.2)
        self.add(cr)
        self.at("So, regulator and conformer")
        b_r = bracket(p.px(0.78), p.px(1.0), -0.75, YELLOW)
        b_l = bracket(p.px(0.2), p.px(0.55), 1.4, YELLOW)
        t_r = lab("conformer\n(this range)", 26, YELLOW).move_to([p.px(0.89), -1.3, 0])
        t_l = lab("regulator\n(this range)", 26, YELLOW).move_to([p.px(0.375), 1.95, 0])
        self.play(FadeOut(l_cf), FadeOut(l_rg), run_time=0.5)
        self.play(Create(b_r), Create(b_l), FadeIn(t_r), FadeIn(t_l), run_time=1.0)
        self.play(Indicate(b_l, color=WHITE, scale_factor=1.05), Indicate(b_r, color=WHITE, scale_factor=1.05), run_time=1.5)
        self.at("They never describe")
        cross = lab("not a whole animal", 30, ORANGE, weight=BOLD).move_to([3.7, -0.9, 0])
        self.play(FadeIn(cross), run_time=0.7)
        self.play(Indicate(cr, color=GREEN, scale_factor=1.1), run_time=1.5)
        self.at("Name one variable")
        stamp = VGroup(lab("one variable,", 34, YELLOW, weight=BOLD), lab("one range", 34, YELLOW, weight=BOLD)).arrange(
            DOWN, buff=0.1)
        box = RoundedRectangle(corner_radius=0.15, width=stamp.width + 0.6, height=stamp.height + 0.5, stroke_color=YELLOW,
                               stroke_width=6).move_to(stamp)
        st = VGroup(box, stamp).move_to([3.7, -2.35, 0]).rotate(0.06)
        self.play(FadeIn(st, scale=1.6), run_time=0.6)
        self.play(Indicate(st, color=WHITE, scale_factor=1.08), run_time=1.4)
        self.finish()


def human_line(t):
    return 0.5 + 0.077 * (t - 0.5)     # model: slope = L / (L + P) with P about 12 x L


def fish_line(t):
    return 0.04 + 0.92 * t


def plot_a_final(sc, probe=True):
    p, ex, crv, cd = crab_scene_base(sc, with_probe=probe)
    ttl = lab("blood salt", 30, TEXT, weight=BOLD).move_to([-2.7, 2.95, 0])
    sc.add(ttl)
    return p, ttl


def human_tag(sc, q, label=True):
    man = sway(sc, man_mob(1.3).move_to([q.px(0.1), q.py(0.86), 0]))
    g = [man]
    if label:
        l_h = VGroup(lab("adult human:", 24, TEAL, weight=BOLD), lab("regulates core", 24, TEAL),
                     lab("temperature", 24, TEAL)).arrange(DOWN, aligned_edge=LEFT, buff=0.04).move_to(
            [q.px(0.1) + 1.8, q.py(0.86), 0])
        g.append(l_h)
    return g


def tol_label(q):
    br = bracket(q.px(0.3), q.px(0.7), q.oy + 0.35, ORANGE)
    l_t = lab("tolerable\nrange", 24, ORANGE).move_to([q.px(0.5), q.oy + 0.95, 0])
    return br, l_t


class S11Temp(SpokenScene):
    def construct(self):
        new_clock(self)
        p, ttl = plot_a_final(self)
        q = plot_b(self)
        self.add(tag_schematic())
        self.at("Now a second plot")
        self.play(Create(q.xax), Create(q.yax), FadeIn(q.frame[0]), run_time=1.2)
        t2 = lab("temperature", 30, TEXT, weight=BOLD).move_to([4.2, 2.95, 0])
        self.play(FadeIn(t2), run_time=0.5)
        self.at("Outside temperature goes across")
        self.play(FadeIn(q.xl, shift=UP * 0.1), FadeIn(q.xt), q.xax.animate.set_stroke(ORANGE),
                  q.xl.animate.set_color(ORANGE), q.xt.animate.set_color(ORANGE), run_time=1.0)
        self.at("Body temperature goes up")
        self.play(FadeIn(q.yl, shift=RIGHT * 0.1), FadeIn(q.yt), q.yax.animate.set_stroke(TEAL),
                  q.yl.animate.set_color(TEAL), q.yt.animate.set_color(TEAL), run_time=1.0)
        dgq = q.diag(op=0.5)
        self.play(Create(dgq), run_time=1.0)
        self.at("Over the air temperatures")
        br, l_t = tol_label(q)
        self.play(Create(br), FadeIn(l_t), run_time=1.0)
        self.at("An adult human regulates")
        man, l_h = human_tag(self, q)
        self.play(FadeIn(man, shift=DOWN * 0.2), FadeIn(l_h), run_time=0.9)
        self.at("That gives a nearly flat line")
        hl = q.curve(human_line, 0.3, 0.7, TEAL, 8, n=10)
        self.play(Create(hl), run_time=1.6)
        dot = always_redraw(lambda: Dot(q.pt(0.5 + 0.2 * np.sin(self.clk.get_value() * 0.9),
                                             human_line(0.5 + 0.2 * np.sin(self.clk.get_value() * 0.9))), radius=0.15,
                                        color=TEAL).set_z_index(6))
        self.add(dot)
        self.finish()


def fish_tag_group(q):
    f_ic = fish_mob(1.0).move_to([q.px(0.9), q.py(0.36), 0])
    l_f = VGroup(lab("lake fish:", 22, "#8CC7E8", weight=BOLD), lab("largely follows", 22, "#8CC7E8"),
                 lab("the water", 22, "#8CC7E8")).arrange(DOWN, aligned_edge=LEFT, buff=0.03).move_to(
        [q.px(0.8) + 0.1, q.py(0.2) + 0.15, 0])
    return f_ic, l_f


class S12Fish(SpokenScene):
    def construct(self):
        new_clock(self)
        p, ttl = plot_a_final(self)
        t2 = lab("temperature", 30, TEXT, weight=BOLD).move_to([4.2, 2.95, 0])
        q = plot_b(self)
        plot_colored(self, q)
        self.add(t2, tag_schematic(), q.diag(op=0.5))
        br, l_t = tol_label(q)
        man, l_h = human_tag(self, q)
        hl = q.curve(human_line, 0.3, 0.7, TEAL, 8, n=10)
        self.add(br, l_t, man, l_h, hl)
        dot = always_redraw(lambda: Dot(q.pt(0.5 + 0.2 * np.sin(self.clk.get_value() * 0.9),
                                             human_line(0.5 + 0.2 * np.sin(self.clk.get_value() * 0.9))), radius=0.15,
                                        color=TEAL).set_z_index(6))
        self.add(dot)
        self.at("A typical fish")
        f_ic, l_f = fish_tag_group(q)
        f_ic.move_to([q.px(1.0) + 1.5, q.py(0.36), 0])
        self.add(f_ic)
        self.play(FadeOut(l_h), f_ic.animate.move_to([q.px(0.9), q.py(0.36), 0]), run_time=1.5)
        fl = q.curve(fish_line, 0.05, 0.95, TEAL, 6, n=10)
        self.at("Its body temperature largely")
        self.play(Create(fl), FadeOut(l_t), FadeOut(br), FadeIn(l_f), run_time=2.0)
        fdot = always_redraw(lambda: Dot(q.pt(0.5 + 0.4 * np.sin(self.clk.get_value() * 0.8),
                                              fish_line(0.5 + 0.4 * np.sin(self.clk.get_value() * 0.8))), radius=0.15,
                                         color=TEAL).set_z_index(6))
        self.add(fdot)
        self.finish()


class S13Close(SpokenScene):
    def construct(self):
        new_clock(self)
        p, ttl = plot_a_final(self, probe=False)
        t2 = lab("temperature", 30, TEXT, weight=BOLD).move_to([4.2, 2.95, 0])
        q = plot_b(self)
        plot_colored(self, q)
        hl = q.curve(human_line, 0.3, 0.7, TEAL, 8, n=10)
        fl = q.curve(fish_line, 0.05, 0.95, TEAL, 6, n=10)
        self.add(t2, tag_schematic(), q.diag(op=0.5), fl, hl)
        mus = mussel_mob(0.9).move_to([-1.6, -0.4, 0])
        l_mu = lab("mussel", 24, BLUE).next_to(mus, RIGHT, buff=0.15)
        crb = sway(self, crab_mob(1.0).move_to([-4.5, 1.8, 0]), amp=0.05, f=2.2)
        l_cr = lab("crab", 24, GREEN).next_to(crb, RIGHT, buff=0.2)
        man = sway(self, man_mob(1.2).move_to([q.px(0.1), q.py(0.86), 0]))
        l_hu = lab("human", 24, TEAL).next_to(man, RIGHT, buff=0.15)
        fish = fish_mob(0.9).move_to([q.px(0.9), q.py(0.36), 0])
        l_fi = lab("fish", 24, "#8CC7E8").next_to(fish, DOWN, buff=0.05)
        da = make_dial([-1.6, -1.5, 0], TEAL, lambda: 0.1, r=0.4, clk=self.clk)
        db = make_dial([-2.5, 1.8, 0], TEAL, lambda: 6.0, r=0.4, clk=self.clk)
        dc = make_dial([q.px(0.1) + 2.4, q.py(0.86), 0], TEAL, lambda: 12.0, r=0.4, clk=self.clk)
        dd = make_dial([q.px(0.9) - 1.3, q.py(0.36), 0], TEAL, lambda: 0.1, r=0.4, clk=self.clk)
        self.at("Two plots, one dial")
        self.play(FadeIn(mus), FadeIn(l_mu), FadeIn(crb), FadeIn(l_cr), run_time=1.0)
        self.play(FadeIn(man), FadeIn(l_hu), FadeIn(fish), FadeIn(l_fi), run_time=1.0)
        self.at("Each line slope is the share")
        self.play(Indicate(crv_of(self, p), color=YELLOW), Indicate(hl, color=YELLOW), run_time=1.5)
        self.at("It holds for that variable")
        self.play(Indicate(ttl, color=YELLOW, scale_factor=1.15), Indicate(t2, color=YELLOW, scale_factor=1.15), run_time=1.5)
        self.at("In the simple model")
        self.play(FadeIn(da), FadeIn(db), FadeIn(dc), FadeIn(dd), run_time=1.0)
        self.play(Indicate(da, color=YELLOW, scale_factor=1.2), Indicate(db, color=YELLOW, scale_factor=1.2),
                  Indicate(dc, color=YELLOW, scale_factor=1.2), Indicate(dd, color=YELLOW, scale_factor=1.2), run_time=1.4)
        self.finish()


def crv_of(sc, p):
    return p.curve(crab_g, 1.0, 0.15, GREEN, 9)


class S14End(EndCard):
    LINE = "Regulator or conformer: one variable, one range, never a whole animal."
