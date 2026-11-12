"""Cells or Serum? (innate immunity, chapter 2: Metchnikoff, Bordet and complement).

Same colour map as chapter 1 (../scenes.py): bacteria GOLD; removal dial and k TEAL; barrier BROWN;
macrophages and monocytes PURPLE; neutrophils BLUE; receptor glow HI; complement C3b tags GREEN;
water flea GREY (transparent). Chapter 1's wound box, slider and corner factor are reused from
../scenes.py in the hook and again in the dial scene. Two columns, 'cells' (PURPLE) and 'serum'
(pale yellow SER), carry the argument across the film.
"""
import os
import importlib.util
import numpy as np
from types import SimpleNamespace
from bp_style import *  # noqa: F401,F403

_here = os.path.dirname(os.path.abspath(__file__))
_spec = importlib.util.spec_from_file_location("film1_scenes", os.path.join(_here, "..", "scenes.py"))
f1 = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(f1)

PURPLE = f1.PURPLE
NEUT = f1.NEUT
HI = f1.HI
BAC = GOLD
SER = "#E8D98A"        # pale yellow serum
SPORE = "#D5D9DF"      # needle spores
YEAST = "#C9B27C"      # budding yeast
CLOT = "#8E2B2B"
FOOD = "#A08C6A"


# ---------------- helpers ----------------
def lab(text, size=28, color=TEXT, **kw):
    return T(text, size, color, **kw).set_stroke(BG, 8, background=True)


def roam(m, x0, x1, y0, y1, speed=0.4, seed=0, spin=0.0):
    rng = np.random.RandomState(seed)
    v = rng.normal(0, 1, 2)
    v *= speed / max(np.linalg.norm(v), 1e-6)
    st = {"v": v}

    def upd(mob, dt):
        v = st["v"]
        v += rng.normal(0, speed * 3, 2) * dt
        n = np.linalg.norm(v)
        if n > speed:
            v *= speed / n
        c = mob.get_center()
        p = c[:2] + v * dt
        if p[0] < x0:
            p[0], v[0] = x0, abs(v[0])
        if p[0] > x1:
            p[0], v[0] = x1, -abs(v[0])
        if p[1] < y0:
            p[1], v[1] = y0, abs(v[1])
        if p[1] > y1:
            p[1], v[1] = y1, -abs(v[1])
        mob.move_to([p[0], p[1], 0])
        if spin:
            mob.rotate(spin * dt)
    m.add_updater(upd)
    return m


def wobble(m, amp=0.08, speed=1.3, phase=0.0):
    base = m.get_center().copy()
    st = {"t": phase}

    def upd(mob, dt):
        st["t"] += dt
        mob.move_to(base + np.array([amp * np.sin(speed * st["t"]), amp * 0.8 * np.cos(speed * 1.3 * st["t"]), 0]))
    m.add_updater(upd)
    return m


def breathe(m, amp=0.025, speed=1.6):
    st = {"t": 0.0, "s": 1.0}

    def upd(mob, dt):
        st["t"] += dt
        ns = 1 + amp * np.sin(speed * st["t"])
        mob.scale(ns / st["s"])
        st["s"] = ns
    m.add_updater(upd)
    return m


def motes(sc, n=16, seed=3):
    rng = np.random.RandomState(seed)
    g = VGroup()
    for _ in range(n):
        d = Dot(radius=rng.uniform(0.04, 0.08), color=rng.choice([TEAL, TEXT, GREY])).set_opacity(rng.uniform(0.22, 0.4))
        d.move_to([rng.uniform(-6.7, 6.7), rng.uniform(-3.7, 3.7), 0])
        vx, vy = rng.uniform(-0.12, 0.12), rng.uniform(0.08, 0.25)

        def drift(m, dt, vx=vx, vy=vy):
            m.shift([vx * dt, vy * dt, 0])
            if m.get_y() > 3.75:
                m.shift(DOWN * 7.5)
        d.add_updater(drift)
        g.add(d)
    g.set_z_index(-5)
    sc.add(g)
    return g


def heads(active=None, xs=(-3.5, 3.5), y=3.3, size=40):
    a = T("cells", size, PURPLE, weight=BOLD).move_to([xs[0], y, 0])
    b = T("serum", size, SER, weight=BOLD).move_to([xs[1], y, 0])
    if active == "cells":
        b.set_opacity(0.4)
    if active == "serum":
        a.set_opacity(0.4)
    return VGroup(a, b)


def tickmark(color=GREEN, s=0.4):
    return VMobject().set_points_as_corners([[-0.5 * s, 0, 0], [-0.15 * s, -0.45 * s, 0], [0.55 * s, 0.55 * s, 0]]).set_stroke(color, 9)


def crossmark(color=RED, s=0.32):
    return VGroup(Line([-s, -s, 0], [s, s, 0]), Line([-s, s, 0], [s, -s, 0])).set_stroke(color, 9)


def result_tag(text, good, x, y=2.35, size=30):
    mark = tickmark() if good else crossmark()
    t = T(text, size, GREEN if good else RED, weight=BOLD)
    g = VGroup(mark, t).arrange(RIGHT, buff=0.25).move_to([x, y, 0])
    return g


def flame(x, y, s=1.0):
    outer = Polygon([0, 0.55, 0], [0.3, 0.05, 0], [0.22, -0.3, 0], [0, -0.38, 0], [-0.22, -0.3, 0], [-0.3, 0.05, 0],
                    stroke_width=0, fill_color=RED, fill_opacity=0.95)
    inner = Polygon([0, 0.2, 0], [0.13, -0.1, 0], [0, -0.3, 0], [-0.13, -0.1, 0], stroke_width=0, fill_color=YELLOW, fill_opacity=0.95)
    g = VGroup(outer, inner).scale(s).move_to([x, y, 0])
    st = {"t": 0.0, "s": 1.0}

    def fl(m, dt):
        st["t"] += dt
        ns = 1 + 0.14 * np.sin(st["t"] * 11)
        m.stretch(ns / st["s"], 1)
        st["s"] = ns
    g.add_updater(fl)
    return g


# ---------------- flea ----------------
def make_flea(scale=1.0, center=(0.0, -0.4)):
    c = np.array([center[0], center[1], 0.0])
    P = lambda x, y: c + scale * np.array([x, y, 0.0])
    sw = max(3.0, 6 * scale)
    body = Ellipse(width=9.0 * scale, height=4.6 * scale, stroke_color=GREY, stroke_width=sw, fill_color=GREY, fill_opacity=0.22).move_to(P(0, 0))
    head = Circle(radius=0.95 * scale, stroke_color=GREY, stroke_width=sw, fill_color=GREY, fill_opacity=0.22).move_to(P(-4.5, 0.1))
    eye = Dot(P(-4.8, 0.3), radius=0.17 * scale, color=TEXT)
    ant = VGroup(Line(P(-5.2, 0.8), P(-6.1, 1.7)), Line(P(-5.6, 1.25), P(-5.5, 1.95))).set_stroke(GREY, sw)
    tail = Line(P(4.4, -0.5), P(6.2, -1.1)).set_stroke(GREY, sw)
    gut = Rectangle(width=7.4 * scale, height=0.62 * scale, stroke_color=GREY, stroke_width=sw, fill_color=GREY, fill_opacity=0.3).move_to(P(0, 0.9))
    parts = VGroup(body, head, eye, ant, tail, gut)
    return SimpleNamespace(g=parts, P=P, scale=scale, body=body, gut=gut, head=head, eye=eye, ant=ant, tail=tail)


def needle(pos, ang, scale=1.0):
    L, W = 0.9 * scale, 0.09 * scale
    s = Polygon([-L / 2, 0, 0], [0, W, 0], [L / 2, 0, 0], [0, -W, 0], stroke_width=0, fill_color=SPORE, fill_opacity=1)
    s.rotate(ang).move_to([pos[0], pos[1], 0])
    s.set_z_index(4)
    return s


CAV_X = [1.3, 0.3, -0.7, -1.7, -2.7]


def cavity_spores(fl, ang=-PI / 2):
    return VGroup(*[needle(fl.P(x, -0.9)[:2] if False else fl.P(x, -0.9), ang, fl.scale) for x in CAV_X])


def make_cell(pos, r=0.27, color=GREY, fill=0.15):
    ring = Circle(radius=r, stroke_color=color, stroke_width=4, fill_color=color, fill_opacity=fill)
    nuc = Circle(radius=r * 0.38, stroke_width=0, fill_color=color, fill_opacity=0.5)
    nuc.shift([r * 0.15, r * 0.1, 0])
    return VGroup(ring, nuc).move_to([pos[0], pos[1], 0])


def cavity_cells(fl, n=7, seed=5, color="#C3C9D4", fill=0.28, r=0.38, move=True):
    rng = np.random.RandomState(seed)
    bx0, bx1 = fl.P(-3.0, 0)[0], fl.P(3.2, 0)[0]
    by0, by1 = fl.P(0, -1.75)[1], fl.P(0, -0.35)[1]
    cells = VGroup()
    for i in range(n):
        c = make_cell([rng.uniform(bx0, bx1), rng.uniform(by0, by1)], r * fl.scale, color, fill)
        if move:
            roam(c, bx0, bx1, by0, by1, speed=0.45 * max(fl.scale, 0.6), seed=seed * 10 + i)
        cells.add(c)
    return cells, (bx0, bx1, by0, by1)


def pause_ring(sc, prog, x=6.0, y=-3.2):
    bg = Circle(radius=0.42, stroke_color=TEXT, stroke_width=3, stroke_opacity=0.4).move_to([x, y, 0])
    ring = always_redraw(lambda: Arc(radius=0.42, start_angle=PI / 2, angle=-2 * PI * max(prog.get_value(), 1e-3), color=TEAL, stroke_width=7).move_to([x, y, 0]))
    return bg, ring


def card(text, size=32, color=TEXT, fill=BG, w=None, h=None, border=None, pad=0.45):
    t = T(text, size, color, weight=BOLD, line_spacing=0.85)
    ww = (w or t.width + 2 * pad)
    hh = (h or t.height + 2 * pad)
    box = RoundedRectangle(corner_radius=0.22, width=ww, height=hh, stroke_color=border or color, stroke_width=4, fill_color=fill, fill_opacity=1)
    return VGroup(box, t)


# ---------------- tubes ----------------
class Tube:
    def __init__(self, x, y=0.3, w=1.9, h=3.0, level=0.7, color=SER, opacity=0.55):
        self.x, self.y, self.w, self.h, self.color, self.op = x, y, w, h, color, opacity
        self.outline = VMobject().set_points_as_corners([[x - w / 2, y + h / 2, 0], [x - w / 2, y - h / 2, 0], [x + w / 2, y - h / 2, 0], [x + w / 2, y + h / 2, 0]])
        self.outline.set_stroke(TEXT, 5)
        self.rim = Line([x - w / 2 - 0.14, y + h / 2, 0], [x + w / 2 + 0.14, y + h / 2, 0]).set_stroke(TEXT, 5)
        hh = max((h - 0.12) * level, 0.02)
        self.liq = Rectangle(width=w - 0.14, height=hh, stroke_width=0, fill_color=color, fill_opacity=opacity if level > 0 else 0)
        self.liq.move_to([x, y - h / 2 + 0.06 + hh / 2, 0])
        self.top = y + h / 2
        self.bot = y - h / 2

    @property
    def g(self):
        return VGroup(self.liq, self.outline, self.rim)

    def level_anim(self, level, opacity=None):
        hh = max((self.h - 0.12) * level, 0.02)
        a = self.liq.animate.stretch_to_fit_height(hh).move_to([self.x, self.y - self.h / 2 + 0.06 + hh / 2, 0])
        if opacity is not None:
            a = a.set_fill(self.color, opacity)
        return a

    def rods(self, n=8, seed=0, level=0.7):
        g = VGroup()
        rng = np.random.RandomState(seed)
        x0, x1 = self.x - self.w / 2 + 0.3, self.x + self.w / 2 - 0.3
        y0, y1 = self.bot + 0.3, self.bot + 0.06 + (self.h - 0.12) * level - 0.25
        for i in range(n):
            r = Arc(radius=0.26, angle=2.3, stroke_width=9, color=BAC)
            r.rotate(rng.uniform(0, 6.28)).move_to([rng.uniform(x0, x1), rng.uniform(y0, y1), 0])
            roam(r, x0, x1, y0, y1, speed=0.7, seed=seed * 7 + i, spin=rng.uniform(-2.0, 2.0))
            g.add(r)
        return g

    def label(self, text, y_top=-1.55, size=28, color=TEXT):
        t = T(text, size, color, line_spacing=0.9)
        t.move_to([self.x, 0, 0])
        t.align_to([0, y_top, 0], UP)
        return t


TX = [-5.2, -1.75, 1.75, 5.2]


# ================= SCENES =================
class S00Title(TitleCard):
    LESSON = "Innate Immunity: Recognize and Respond"
    TITLE = "Cells or Serum?"

    def construct(self):
        fl = make_flea(0.3, (-2.7, -2.75)).g
        tb = Tube(2.9, -2.75, 0.7, 1.4, level=0.7)
        deco = VGroup(fl, tb.g)
        self.play(FadeIn(deco), run_time=0.5)
        super().construct()


class S01Hook(SpokenScene):
    def construct(self):
        w = f1.make_world(self, plot=False, clock=False, slide=True, factor=True, counter=False, k0=0.0, show_val=False, N0=100)
        self.at("defenses")
        self.play(w.K.animate.set_value(0.6), run_time=0.9)
        self.at("remove more than half")
        big = M("k > 0.5", 80, TEAL).move_to([3.8, 0.7, 0])
        self.play(FadeIn(big, scale=0.8), w.N.animate.set_value(40), run_time=1.2)
        self.at("every doubling time")
        each = T("every doubling time", 38, TEAL, weight=BOLD).move_to([3.8, -0.5, 0])
        self.play(FadeIn(each), w.N.animate.set_value(80), run_time=0.9)
        self.at("time")
        self.play(w.N.animate.set_value(64), run_time=0.8)
        self.at("But who does")
        q = T("?", 200, TEXT, weight=BOLD).move_to([3.8, 0.1, 0])
        self.play(FadeOut(VGroup(big, each)), FadeIn(q, scale=0.4), run_time=0.8)
        self.at("Cells or")
        cell = make_cell([2.6, 0.2], 1.15, PURPLE, 0.3)
        cell.set_z_index(3)
        wobble(cell, 0.06, 1.4)
        tb = Tube(5.3, 0.2, 1.5, 2.8, level=0.7)
        self.play(FadeOut(q, scale=0.3), FadeIn(cell, shift=LEFT * 0.6), FadeIn(tb.g, shift=RIGHT * 0.6), run_time=1.0)
        cl = T("cells", 40, PURPLE, weight=BOLD).move_to([2.6, -1.75, 0])
        self.play(FadeIn(cl), run_time=0.5)
        self.at("dissolved")
        sl = T("serum", 40, SER, weight=BOLD).move_to([5.3, -1.75, 0])
        self.play(FadeIn(sl), run_time=0.5)
        self.finish()


class S02Argument(SpokenScene):
    def construct(self):
        motes(self)
        hd = heads()
        self.add(hd)
        cell = make_cell([-3.5, 0.6], 1.5, PURPLE, 0.3).set_z_index(3)
        wobble(cell, 0.07, 1.4)
        tb = Tube(3.5, 0.6, 1.9, 3.2, level=0.7)
        bub = VGroup(*[Dot(radius=0.07, color=SER).set_opacity(0.8).move_to([3.5 + (i - 1) * 0.35, -0.3 + 0.5 * i, 0]) for i in range(3)])
        for i, b in enumerate(bub):
            def up(m, dt, i=i):
                m.shift(UP * 0.5 * dt)
                if m.get_y() > 1.3:
                    m.shift(DOWN * 1.8)
            b.add_updater(up)
        self.play(FadeIn(cell, scale=0.7), FadeIn(tb.g), FadeIn(bub), run_time=1.0)
        era = T("1880s and 1890s", 44, TEXT, weight=BOLD).move_to([0, -2.6, 0])
        self.at("1880s")
        self.play(FadeIn(era, shift=UP * 0.2), run_time=0.8)
        self.at("argued")
        arr = VGroup(Arrow([-0.9, 0.5, 0], [-2.0, 0.5, 0], buff=0, stroke_width=8, color=TEXT),
                     Arrow([0.9, 0.5, 0], [2.0, 0.5, 0], buff=0, stroke_width=8, color=TEXT))
        arr = VGroup(DoubleArrow([-1.2, 0.5, 0], [1.2, 0.5, 0], buff=0, stroke_width=8, color=TEXT))
        self.play(GrowFromCenter(arr), run_time=0.9)
        self.at("Mechnikoff")
        nm = card("Elie Metchnikoff", 32, TEXT, border=PURPLE, fill=BG)
        nm.move_to([-3.5, -1.5, 0])
        nm.shift(LEFT * 3)
        self.play(nm.animate.move_to([-3.5, -1.5, 0]), run_time=1.0)
        self.at("a zoologist")
        self.play(Indicate(cell, color=PURPLE, scale_factor=1.12), run_time=1.0)
        self.at("championed")
        self.play(Indicate(hd[0], color=PURPLE, scale_factor=1.25), run_time=1.0)
        self.at("He chose")
        fl = make_flea(0.62, (0.0, 0.2))
        self.play(FadeOut(VGroup(cell, tb.g, bub, arr, era)), FadeOut(nm), run_time=0.7)
        self.play(FadeIn(fl.g), run_time=0.8)
        mg = VGroup(Circle(radius=0.95, stroke_color=TEXT, stroke_width=7, fill_color=BG, fill_opacity=0.15),
                    Line([0.67, -0.67, 0], [1.5, -1.5, 0]).set_stroke(TEXT, 10)).move_to([-3.4, 0.2, 0])
        self.add(mg.set_z_index(6))
        self.at("see through")
        self.play(mg.animate.move_to([3.2, 0.2, 0]), run_time=2.6, rate_func=smooth)
        self.finish()


class S03Flea(SpokenScene):
    def construct(self):
        fl = make_flea()
        food = VGroup()
        rng = np.random.RandomState(2)
        for i in range(9):
            d = Dot(radius=0.07, color=FOOD).set_opacity(0.8).move_to(fl.P(-3.4 + i * 0.8, 0.9 + rng.uniform(-0.1, 0.1)))

            def fm(m, dt):
                m.shift(RIGHT * 0.55 * dt)
                if m.get_x() > fl.P(3.5, 0)[0]:
                    m.shift(LEFT * 7.0)
            d.add_updater(fm)
            food.add(d)
        self.play(Create(fl.body), Create(fl.head), run_time=0.8)
        self.play(FadeIn(VGroup(fl.eye, fl.ant, fl.tail)), Create(fl.gut), FadeIn(food), run_time=0.6)
        self.at("daphnia")
        name = T("water flea (Daphnia)", 36, TEXT, weight=BOLD).move_to([0, 2.8, 0])
        self.play(FadeIn(name, shift=DOWN * 0.15), run_time=0.7)
        self.at("transparent")
        self.play(Indicate(fl.body, color=GREY, scale_factor=1.03), run_time=1.0)
        # spores swallowed
        prog = ValueTracker(0.0)
        self.add(prog)
        y0 = fl.P(0, 0.9)[1]
        sp = VGroup(*[needle([-9, y0], 0, 1.0) for _ in range(5)])

        def ms(m):
            for i, s in enumerate(m):
                x = -5.4 + 6.8 * prog.get_value() - 1.0 * i
                s.move_to([x, y0, 0])
                s.set_opacity(0 if x < -4.9 else 1)
        sp.add_updater(ms)
        self.add(sp)
        self.at("Some fleas swallow")
        self.play(prog.animate.set_value(0.55), run_time=self.t_of("spores of") - 0.2 - self.elapsed(), rate_func=linear)
        sl = lab("yeast spores", 34, TEXT, weight=BOLD).move_to([0.0, 1.28, 0])
        self.add(sl)
        self.play(prog.animate.set_value(1.0), run_time=self.t_of("The spores pierce") - 0.5 - self.elapsed(), rate_func=linear)
        sp.clear_updaters()
        self.at("pierce")
        tg = [fl.P(x, -0.9) for x in CAV_X]
        self.play(*[sp[i].animate.rotate(-PI / 2).move_to(tg[i]) for i in range(5)], FadeOut(sl), run_time=2.0, lag_ratio=0.2)
        for i, s_ in enumerate(sp):
            wobble(s_, 0.22, 1.5, i)
        self.at("body cavity")
        bc = lab("body cavity", 34, TEXT, weight=BOLD).move_to([0.0, -2.15, 0])
        self.play(FadeIn(bc), run_time=0.6)
        self.finish()


def flea_with_spores(sc, cells=True, n=7, color=GREY, fill=0.15):
    fl = make_flea()
    sp = cavity_spores(fl)
    sc.add(fl.g, sp)
    cs = None
    if cells:
        cs, bd = cavity_cells(fl, n=n, color=color, fill=fill)
        sc.add(cs)
    return fl, sp, cs


class S04Predict(SpokenScene):
    def construct(self):
        fl = make_flea()
        sp = cavity_spores(fl)
        self.add(fl.g, sp)
        cs, bd = cavity_cells(fl)
        self.at("blood cells")
        self.play(FadeIn(cs, lag_ratio=0.15), run_time=1.3)
        self.at("passive")
        pl = lab("passive?", 34, TEXT, weight=BOLD).move_to([0.0, 1.28, 0])
        self.play(FadeIn(pl), run_time=0.6)
        self.at("carried")
        self.play(Indicate(sp, color=YELLOW, scale_factor=1.3), run_time=1.2)
        self.at("What would you")
        self.play(FadeOut(pl), run_time=0.3)
        q = card("passive cells: what happens to the spores?", 30, TEXT, pad=0.3).move_to([0, 3.0, 0])
        self.play(FadeIn(q, scale=0.9), run_time=0.8)
        self.at("with the spores")
        self.play(Indicate(sp, color=YELLOW, scale_factor=1.3), run_time=1.0)
        self.finish()


class S05Pause(NarratedScene):
    def construct(self):
        fl = make_flea()
        sp = cavity_spores(fl)
        self.add(fl.g, sp)
        cs, bd = cavity_cells(fl)
        self.add(cs)
        q = card("passive cells: what happens to the spores?", 30, TEXT, pad=0.3).move_to([0, 3.0, 0])
        self.add(q)
        prog = ValueTracker(0)
        self.add(prog)
        bg, ring = pause_ring(self, prog)
        self.add(bg, ring)
        self.play(prog.animate.set_value(1.0), run_time=self.narration_s - 0.1, rate_func=linear)
        self.finish()


class S06Reveal(SpokenScene):
    def construct(self):
        fl = make_flea()
        sp = cavity_spores(fl)
        self.add(fl.g, sp)
        cs, bd = cavity_cells(fl)
        self.add(cs)
        self.at("Instead")
        self.play(*[c[0].animate.set_stroke(PURPLE).set_fill(PURPLE, 0.3) for c in cs],
                  *[c[1].animate.set_fill(PURPLE, 0.55) for c in cs], run_time=1.0)
        self.at("mobile cells")
        for c in cs:
            c.clear_updaters()
        order = list(range(7))
        anims = []
        for i in range(5):
            anims.append(cs[i].animate.move_to(sp[i].get_center()))
        self.play(*anims, run_time=2.0, rate_func=smooth)
        for i in (5, 6):
            roam(cs[i], bd[0], bd[1], bd[2], bd[3], speed=0.45, seed=70 + i)
        self.at("surround")
        self.play(*[cs[i].animate.scale(2.1) for i in range(5)], run_time=1.0)
        for i in range(5):
            cs[i].set_z_index(1)
        self.at("engulf")
        big = make_cell([5.2, 2.5], 1.1, PURPLE, 0.3)
        spo = needle([5.2, 2.5], 0.6, 0.9)
        ring = Circle(radius=0.15, stroke_color=TEXT, stroke_width=4).move_to([5.2, 2.5, 0])
        self.play(FadeIn(big), FadeIn(spo), run_time=0.5)
        self.play(ring.animate.scale(4.0), run_time=0.8)
        self.finish()


class S07Outcomes(SpokenScene):
    def construct(self):
        cL, cR = (-3.4, -0.3), (3.4, -0.3)
        L = make_flea(0.5, cL)
        R = make_flea(0.5, cR)
        div = DashedLine([0, -2.9, 0], [0, 2.8, 0], color=GREY, stroke_width=3).set_opacity(0.6)
        spL = cavity_spores(L)
        spR = cavity_spores(R)
        csL = VGroup(*[make_cell(spL[i].get_center(), 0.3, PURPLE, 0.3) for i in range(5)])
        for c in csL:
            c.set_z_index(1)
        csR, bdR = cavity_cells(R, n=2, color=PURPLE, fill=0.3, r=0.4)
        self.play(FadeIn(div), FadeIn(L.g), FadeIn(R.g), run_time=0.8)
        self.add(spL, spR, csL, csR)
        grpL = VGroup(L.g, spL, csL)
        st = {"t": 0.0}

        def bob(m, dt):
            st["t"] += dt
            m.shift(UP * 0.3 * 1.6 * np.cos(1.6 * st["t"]) * dt)
        grpL.add_updater(bob)
        grpR = VGroup(R.g, spR, csR, yeast_holder := VGroup())
        st2 = {"t": 0.0}

        def bob2(m, dt):
            st2["t"] += dt
            m.shift(UP * 0.12 * 1.3 * np.cos(1.3 * st2["t"]) * dt)
        self.at("destroyed")
        self.play(*[spL[i].animate.scale(0.15).set_opacity(0) for i in range(5)], run_time=1.6)
        self.at("infection stopped")
        wl = lab("cells win: lives", 34, PURPLE, weight=BOLD).move_to([cL[0], -2.3, 0])
        self.play(FadeIn(wl, shift=UP * 0.15), run_time=0.7)
        self.at("Where spores")
        yeast = VGroup()
        rng = np.random.RandomState(8)
        bx0, bx1, by0, by1 = bdR
        for i in range(22):
            y = Circle(radius=0.07 + 0.04 * rng.rand(), stroke_width=0, fill_color=YEAST, fill_opacity=0.95)
            y.move_to([rng.uniform(bx0, bx1), rng.uniform(by0, by1), 0])
            yeast.add(y)
        self.play(*[FadeOut(s, scale=0.4) for s in spR], FadeIn(yeast, scale=0.2, lag_ratio=0.06), run_time=2.6)
        self.at("the flea died")
        wr = lab("spores win: dies", 34, SPORE, weight=BOLD).move_to([cR[0], -2.3, 0])
        self.play(FadeIn(wr, shift=UP * 0.15), R.g.animate.set_opacity(0.5), run_time=0.8)
        self.finish()


class S08Limit(SpokenScene):
    def construct(self):
        motes(self, 12, 5)
        hd = heads(active="cells")
        self.add(hd)
        ic = make_cell([-4.2, 0.1], 1.7, PURPLE, 0.3).set_z_index(3)
        wobble(ic, 0.06, 1.4)
        sp = needle([-1.9, 0.1], 0.0, 1.2)
        st = {"t": 0.0}

        def loop(m, dt):
            st["t"] += dt
            ph = (st["t"] % 3.2) / 3.2
            x = -1.9 + (-4.2 + 1.9 + 0.2) * min(ph / 0.8, 1.0)
            m.move_to([x, 0.1 + 0.1 * np.sin(st["t"] * 3), 0])
            m.set_opacity(1.0 if ph < 0.75 else max(0.0, 1 - (ph - 0.75) / 0.2))
        sp.add_updater(loop)
        c1 = card("1884: phagocytes are\nan active defense", 38, TEXT, border=PURPLE, w=7.6, h=2.2).move_to([2.2, 1.3, 0])
        c2 = card("not shown: that\ncells work alone", 38, TEXT, border=GREY, w=7.6, h=2.2)
        c2 = VGroup(DashedVMobject(RoundedRectangle(corner_radius=0.22, width=7.6, height=2.2, stroke_color=GREY, stroke_width=4), num_dashes=44), c2[1]).move_to([2.2, -1.4, 0])
        self.at("1884")
        self.play(FadeIn(c1, shift=LEFT * 0.4), run_time=0.9)
        self.at("eating cell")
        self.play(FadeIn(ic, scale=0.6), FadeIn(sp), run_time=1.0)
        self.at("phagocyte")
        pl = lab("phagocyte", 38, PURPLE, weight=BOLD).move_to([-4.2, -2.3, 0])
        self.play(FadeIn(pl), run_time=0.6)
        self.at("But it did not")
        self.play(FadeIn(c2, shift=LEFT * 0.4), run_time=0.9)
        self.at("work alone")
        self.play(Indicate(c2[1], color=TEXT, scale_factor=1.06), run_time=1.0)
        self.finish()


def blood_tube(x=0.0):
    return Tube(x, 0.3, 1.9, 3.0, level=0.8, color=RED, opacity=0.6)


class S09Bordet(SpokenScene):
    def construct(self):
        motes(self, 12, 9)
        hd = heads(active="serum")
        self.add(hd)
        paris = T("Paris, 1890s", 48, TEXT, weight=BOLD).move_to([-3.0, 0.4, 0])
        self.play(FadeIn(paris, shift=UP * 0.2), run_time=0.8)
        self.at("Jules")
        nm = card("Jules Bordet\nPasteur Institute", 30, TEXT, border=SER, w=4.8, h=1.4).move_to([3.5 + 4, 2.15, 0])
        self.play(nm.animate.move_to([3.5, 2.15, 0]), run_time=1.0)
        self.at("serum")
        self.play(Indicate(hd[1], color=SER, scale_factor=1.25), run_time=0.9)
        self.at("the fluid")
        self.play(FadeOut(paris), run_time=0.4)
        bt = blood_tube(0.0)
        self.play(FadeIn(bt.g), run_time=0.9)
        bl = lab("blood", 30, RED, weight=BOLD).move_to([-1.9, 0.5, 0])
        self.play(FadeIn(bl), run_time=0.5)
        self.at("once blood clots")
        clot_h = (bt.h - 0.12) * 0.38
        serum = Rectangle(width=bt.w - 0.14, height=0.02, stroke_width=0, fill_color=SER, fill_opacity=0.55).move_to([0, bt.bot + 0.06 + clot_h, 0])
        serum.align_to([0, bt.bot + 0.06 + clot_h, 0], DOWN)
        self.add(serum)
        self.play(bt.liq.animate.set_fill(CLOT, 0.85).stretch_to_fit_height(clot_h).move_to([0, bt.bot + 0.06 + clot_h / 2, 0]),
                  serum.animate.stretch_to_fit_height((bt.h - 0.12) * 0.42).align_to([0, bt.bot + 0.06 + clot_h, 0], DOWN),
                  FadeOut(bl), run_time=1.6)
        sl = lab("serum", 36, SER, weight=BOLD).move_to([2.2, 0.9, 0])
        ln = Line([1.5, 0.9, 0], [0.5, 0.75, 0]).set_stroke(SER, 4)
        self.play(FadeIn(sl), Create(ln), run_time=0.7)
        self.at("Serum from an animal")
        t1 = Tube(TX[0])
        l1 = t1.label("immune\nserum")
        self.play(FadeOut(VGroup(bt.g, serum, sl, ln, nm)), FadeIn(t1.g), run_time=1.0)
        self.at("immunized")
        self.play(FadeIn(l1), run_time=0.6)
        self.at("cholera")
        rods = t1.rods(9, seed=1)
        self.play(FadeIn(rods), run_time=0.8)
        self.at("bacterium")
        vl = lab("Vibrio", 30, BAC, weight=BOLD).move_to([TX[0] + 2.35, 0.4, 0])
        vl2 = Line([TX[0] + 1.6, 0.4, 0], [TX[0] + 0.95, 0.4, 0]).set_stroke(BAC, 4)
        self.play(FadeIn(vl), Create(vl2), run_time=0.7)
        self.at("killed")
        tg = result_tag("kills", True, TX[0])
        self.play(FadeOut(rods), FadeOut(vl), FadeOut(vl2), FadeIn(tg), run_time=1.2)
        self.finish()


def row(sc, upto=3, tags=True, flame_on=True):
    """Rebuild tubes 1..3 exactly as film s09/s10 leave them."""
    o = SimpleNamespace()
    o.t1, o.t2, o.t3 = Tube(TX[0]), Tube(TX[1]), Tube(TX[2])
    return o


class S10Heat(SpokenScene):
    def construct(self):
        motes(self, 10, 10)
        hd = heads(active="serum")
        self.add(hd)
        t1, t2, t3 = Tube(TX[0]), Tube(TX[1]), Tube(TX[2])
        l1, l2, l3 = t1.label("immune\nserum"), t2.label("immune serum,\nheated to about\n55 °C", y_top=-2.25), t3.label("fresh\nnormal serum")
        self.add(t1.g, l1, result_tag("kills", True, TX[0]))
        self.at("Heated")
        self.play(FadeIn(t2.g), FadeIn(l2), run_time=0.8)
        r2 = t2.rods(9, seed=2)
        self.add(r2)
        fl = flame(TX[1], -1.7, 0.8)
        self.play(FadeIn(r2), FadeIn(fl), run_time=0.8)
        self.at("lost its power")
        tg2 = result_tag("no kill", False, TX[1])
        self.play(FadeIn(tg2), run_time=0.7)
        self.at("Fresh serum")
        self.play(FadeIn(t3.g), FadeIn(l3), run_time=0.8)
        r3 = t3.rods(9, seed=3)
        self.play(FadeIn(r3), run_time=0.8)
        self.at("could not kill")
        tg3 = result_tag("no kill", False, TX[2])
        self.play(FadeIn(tg3), run_time=0.7)
        self.finish()


class S11Mix(SpokenScene):
    def construct(self):
        hd = heads(active="serum")
        self.add(hd)
        t1, t2, t3, t4 = Tube(TX[0]), Tube(TX[1]), Tube(TX[2]), Tube(TX[3], level=0.0)
        l2, l3 = t2.label("heated immune\nserum"), t3.label("fresh\nnormal serum")
        l4 = t4.label("heated immune\n+ fresh normal")
        r2, r3 = t2.rods(7, seed=2), t3.rods(7, seed=3)
        self.add(t2.g, t3.g, t4.g, l2, l3, r2, r3)
        self.at("mixed")
        s2 = ArcBetweenPoints([TX[1], 2.15, 0], [TX[3] - 0.3, 2.15, 0], angle=-0.5).set_stroke(SER, 7)
        self.play(FadeIn(l4), Create(s2), run_time=0.5)
        r4 = t4.rods(8, seed=4, level=0.7)
        self.play(t2.level_anim(0.3), t4.level_anim(0.4, 0.55), FadeIn(r4), FadeOut(s2), run_time=1.3)
        self.at("with the fresh")
        s3 = ArcBetweenPoints([TX[2], 2.15, 0], [TX[3] + 0.3, 2.15, 0], angle=-0.5).set_stroke(SER, 7)
        self.play(Create(s3), run_time=0.5)
        self.play(t3.level_anim(0.3), t4.level_anim(0.7), FadeOut(s3), run_time=1.3)
        self.at("killed again")
        tg = result_tag("kills", True, TX[3])
        self.play(FadeOut(r4), FadeIn(tg), run_time=1.2)
        self.at("So the killing")
        self.play(FadeOut(VGroup(t2.g, t3.g, t4.g, l2, l3, l4, tg, r2, r3)), run_time=0.9)
        b1, b2 = block(-3.4, PURPLE), block(3.5, GREEN)
        t1_ = T("part 1", 54, TEXT, weight=BOLD).move_to([-3.4, 0.1, 0])
        t2_ = T("part 2", 54, TEXT, weight=BOLD).move_to([3.5, 0.1, 0])
        self.at("two separate")
        self.play(FadeIn(b1, scale=0.8), FadeIn(t1_), run_time=0.8)
        self.play(FadeIn(b2, scale=0.8), FadeIn(t2_), run_time=0.8)
        self.finish()


def block(x, color):
    return RoundedRectangle(corner_radius=0.25, width=6.2, height=4.2, stroke_color=color, stroke_width=4, fill_color=color, fill_opacity=0.08).move_to([x, 0.1, 0])


class S12Parts(SpokenScene):
    def construct(self):
        motes(self, 12, 12)
        hd = heads(active="serum")
        self.add(hd)
        b1, b2 = block(-3.4, TEXT), block(3.5, GREEN)
        p1 = T("part 1", 54, TEXT, weight=BOLD).move_to([-3.4, 0.1, 0])
        p2 = T("part 2", 54, TEXT, weight=BOLD).move_to([3.5, 0.1, 0])
        self.add(b1, b2, p1, p2)
        breathe(b1)
        breathe(b2)
        self.at("survives heat")
        fl1 = flame(-5.0, -0.8, 0.9)
        h1 = T("survives heat", 34, TEXT).move_to([-3.0, -0.8, 0])
        self.play(p1.animate.move_to([-3.4, 1.3, 0]), FadeIn(fl1), FadeIn(h1), run_time=1.0)
        self.at("raised by")
        i1 = T("raised by immunization", 32, TEXT).move_to([-3.4, -1.6, 0])
        self.play(FadeIn(i1, shift=UP * 0.15), run_time=0.8)
        self.at("antibody")
        ab = T("antibody", 56, TEXT, weight=BOLD).move_to([-3.4, 1.3, 0])
        self.play(ReplacementTransform(p1, ab), b1.animate.set_stroke(PURPLE), run_time=1.0)
        self.at("destroyed by heat")
        fl2 = flame(1.2, -0.8, 0.9)
        h2 = T("destroyed by heat", 34, TEXT).move_to([3.9, -0.8, 0])
        self.play(p2.animate.move_to([3.5, 1.3, 0]), FadeIn(fl2), FadeIn(h2), run_time=1.0)
        self.at("present in all")
        i2 = T("in all fresh serum", 32, TEXT).move_to([3.5, -1.6, 0])
        self.play(FadeIn(i2, shift=UP * 0.15), run_time=0.8)
        self.at("We call it complement")
        cp = T("complement", 56, GREEN, weight=BOLD).move_to([3.5, 1.3, 0])
        self.play(ReplacementTransform(p2, cp), run_time=1.0)
        self.finish()


class S13Rejoin(SpokenScene):
    def construct(self):
        motes(self, 10, 13)
        hd = heads(xs=(-3.5, 3.5))
        self.add(hd)
        self.play(Indicate(hd[0], color=PURPLE, scale_factor=1.2), Indicate(hd[1], color=SER, scale_factor=1.2), run_time=1.2)
        bx, by = -0.4, -0.2
        bact = Circle(radius=0.95, stroke_color=BAC, stroke_width=5, fill_color=BAC, fill_opacity=0.85).move_to([bx, by, 0])
        wobble(bact, 0.05, 1.2)
        bact.set_z_index(2)
        un = Circle(radius=0.95, stroke_color=BAC, stroke_width=5, fill_color=BAC, fill_opacity=0.85).move_to([-4.6, by, 0])
        wobble(un, 0.05, 1.0, 1.0)
        self.at("Watch a bacterium")
        self.play(FadeIn(bact, scale=0.5), FadeIn(un, scale=0.5), run_time=0.9)
        ul = lab("untagged", 30, BAC, weight=BOLD).move_to([-4.6, -1.65, 0])
        self.add(ul)
        self.at("meet complement")
        rng = np.random.RandomState(4)
        tags = VGroup()
        floaters = VGroup()
        for i in range(14):
            a = 2 * PI * i / 14
            tgt = np.array([bx + 0.98 * np.cos(a), by + 0.98 * np.sin(a), 0])
            tag = Dot(radius=0.13, color=GREEN).set_z_index(3).move_to([rng.uniform(1.8, 5.8), rng.uniform(-2.2, 2.0), 0])
            tag.tgt = tgt
            tags.add(tag)
        for tg in tags:
            roam(tg, 1.6, 6.2, -2.6, 2.4, speed=0.5, seed=int(tg.get_x() * 100) % 1000)
        self.play(FadeIn(tags, lag_ratio=0.1), run_time=1.2)
        self.at("Small green tags")
        for tg in tags:
            tg.clear_updaters()
        self.play(*[tg.animate.move_to(tg.tgt) for tg in tags[:7]], run_time=1.6, lag_ratio=0.1)
        self.at("C3b")
        cl = lab("C3b", 44, GREEN, weight=BOLD).move_to([bx + 1.2, by + 1.9, 0])
        ln = Line([bx + 0.85, by + 1.55, 0], [tags[2].tgt[0], tags[2].tgt[1] + 0.15, 0]).set_stroke(GREEN, 4)
        self.play(FadeIn(cl), Create(ln), run_time=0.7)
        self.at("coat")
        self.play(*[tg.animate.move_to(tg.tgt) for tg in tags[7:]], run_time=1.5, lag_ratio=0.1)
        self.at("A neutrophil")
        nt = Circle(radius=1.25, stroke_color=NEUT, stroke_width=5, fill_color=NEUT, fill_opacity=0.35).move_to([5.1, by, 0]).set_z_index(1)
        nucl = VGroup(*[Circle(radius=0.2, stroke_width=0, fill_color=NEUT, fill_opacity=0.8).move_to([5.1 + dx, by + dy, 0]) for dx, dy in [(-0.3, 0.3), (0.1, 0.45), (0.35, -0.1)]]).set_z_index(1)
        nl = lab("neutrophil", 34, NEUT, weight=BOLD).move_to([5.1, by - 1.75, 0])
        self.play(FadeIn(nt, shift=LEFT * 0.6), FadeIn(nucl, shift=LEFT * 0.6), FadeIn(nl), run_time=0.9)
        self.at("grabs")
        coated = VGroup(bact, tags, cl, ln)
        for m in (bact,):
            m.clear_updaters()
        self.play(VGroup(nt, nucl).animate.move_to([nt.get_x() - 3.7, by, 0]), nl.animate.shift(LEFT * 3.7), run_time=1.0)
        self.play(FadeOut(cl), FadeOut(ln), run_time=0.2)
        self.play(VGroup(bact, tags).animate.scale(0.45).move_to([nt.get_x() - 0.2, by, 0]), run_time=1.2)
        self.finish()


class S14K(SpokenScene):
    def construct(self):
        motes(self, 8, 14)
        hd = heads()
        self.add(hd)
        nt = Circle(radius=1.3, stroke_color=NEUT, stroke_width=5, fill_color=NEUT, fill_opacity=0.35).move_to([-3.4, 0.9, 0]).set_z_index(1)
        wobble(nt, 0.05, 1.1)
        self.add(nt)
        speed = {"v": 0.9}
        bs = VGroup()
        for i in range(4):
            b = VGroup(Circle(radius=0.38, stroke_color=BAC, stroke_width=4, fill_color=BAC, fill_opacity=0.85),
                       *[Dot(radius=0.07, color=GREEN).move_to([0.42 * np.cos(2 * PI * j / 6), 0.42 * np.sin(2 * PI * j / 6), 0]) for j in range(6)])
            b.move_to([-1.2 + i * 2.0, 0.9, 0])
            b.set_z_index(2)

            def mv(m, dt):
                m.shift(LEFT * speed["v"] * dt)
                if m.get_x() < -2.5:
                    m.shift(RIGHT * 8.0)
                x = m.get_x()
                m.set_opacity(1.0 if x > -2.2 else max(0.0, (x + 2.5) / 0.3))
            b.add_updater(mv)
            bs.add(b)
        self.add(bs)
        self.at("Coated microbes")
        nl = lab("coated microbes eaten far more readily", 28, TEXT).move_to([1.4, 2.2, 0])
        self.play(FadeIn(nl), run_time=0.6)
        self.at("In the first film's")
        K = ValueTracker(0.3)
        self.add(K)
        x0, x1, y = -2.6, 4.6, -1.35
        track = Rectangle(width=x1 - x0, height=0.6, stroke_color=TEAL, stroke_width=4, fill_opacity=0).move_to([(x0 + x1) / 2, y, 0])
        fill = always_redraw(lambda: Rectangle(width=max(1e-3, (x1 - x0) * K.get_value()), height=0.6, stroke_width=0, fill_color=TEAL, fill_opacity=0.85).move_to([x0 + (x1 - x0) * K.get_value() / 2, y, 0]))
        mark = Line([(x0 + x1) / 2, y - 0.55, 0], [(x0 + x1) / 2, y + 0.55, 0], color=TEXT, stroke_width=4)
        kk = T("k", 64, TEAL, weight=BOLD).move_to([x0 - 0.7, y, 0])
        self.play(FadeOut(nl), FadeIn(track), FadeIn(mark), FadeIn(kk), run_time=0.9)
        self.add(fill)
        self.at("raises k")
        rl = lab("complement coating raises k", 34, TEAL, weight=BOLD).move_to([1.0, -2.45, 0])
        self.play(K.animate.set_value(0.7), FadeIn(rl), run_time=1.8)
        self.at("The cells eat")
        self.play(Indicate(nt, color=NEUT, scale_factor=1.1), run_time=1.0)
        self.at("the proteins make")
        speed["v"] = 1.8
        self.play(K.animate.set_value(0.85), hd[0].animate.move_to([-1.6, 3.3, 0]), hd[1].animate.move_to([1.6, 3.3, 0]), run_time=1.8)
        self.finish()


class S15Nobel(SpokenScene):
    def construct(self):
        hd = heads(xs=(-1.6, 1.6))
        self.add(hd)
        self.at("1908")
        ban = card("1908 Nobel Prize, shared", 40, TEXT, border=TEXT, w=9.4, h=1.4).move_to([0, 1.7, 0])
        self.play(FadeIn(ban, shift=DOWN * 0.3), run_time=0.9)
        self.at("Metchnikoff")
        n1 = card("Metchnikoff", 36, PURPLE, border=PURPLE, w=4.6, h=1.3).move_to([-8.5, -0.4, 0])
        self.play(n1.animate.move_to([-3.1, -0.4, 0]), run_time=1.0)
        self.at("Paul")
        n2 = card("Paul Ehrlich", 36, SER, border=SER, w=4.6, h=1.3).move_to([8.5, -0.4, 0])
        self.play(n2.animate.move_to([3.1, -0.4, 0]), run_time=1.0)
        self.at("serum")
        self.play(Indicate(n2, color=SER, scale_factor=1.08), run_time=1.0)
        self.at("Each side")
        self.play(n1.animate.move_to([-2.4, -0.4, 0]), n2.animate.move_to([2.4, -0.4, 0]), run_time=1.2)
        self.at("one system")
        one = card("one system", 54, TEXT, border=TEXT, w=7.0, h=1.8).move_to([0, -0.4, 0])
        self.play(FadeOut(VGroup(n1, n2, ban, hd)), FadeIn(one, scale=0.8), run_time=1.2)
        self.finish()


class S16End(EndCard):
    LINE = "Cells and serum proteins are one system: complement speeds phagocytes."
