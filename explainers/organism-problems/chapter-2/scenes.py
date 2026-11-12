"""Fewer Pores (organism-problems, film 2 of 2)

Same look and colour map as film 1 (../scenes.py): carbon dioxide = TEALC; water vapour = BLUE; oxygen = warm red;
guard cells and stomata = PURPLE; the price = GOLD balance scale; wax, cells, labels = GREY.
Leaf A = solid outline, leaf B = dashed outline. Bars and gauges not computed are labelled "schematic".
"""
import math
import random
import numpy as np
from bp_style import *  # noqa: F401,F403

PURPLE = "#B58CD9"
TEALC = "#34D6A0"
O2C = "#F0705A"


def arrow_at(pos, ang, size, width, color):
    d = np.array([math.cos(ang), math.sin(ang), 0])
    return Arrow(pos - d * size / 2, pos + d * size / 2, buff=0, color=color, stroke_width=width,
                 tip_length=size * 0.38, max_tip_length_to_length_ratio=0.6,
                 max_stroke_width_to_length_ratio=40)


class PathStream(VGroup):
    """Small arrows that loop along a polyline. mults: trackers multiplying size and width."""

    def __init__(self, pts, color, n=3, speed=0.16, size=0.55, width=6, mults=(), phase=0.0, vis=None):
        super().__init__()
        self.pts = [np.array([p[0], p[1], 0.0]) for p in pts]
        self.cum = [0.0]
        for a, b in zip(self.pts[:-1], self.pts[1:]):
            self.cum.append(self.cum[-1] + float(np.linalg.norm(b - a)))
        self.total = self.cum[-1]
        self.mults = list(mults)
        self.vis = vis
        for i in range(n):
            a = arrow_at(self.pts[0], 0, size, width, color)
            a.ph = (i / n + phase) % 1
            a.base = (size, width, color)
            a.add_updater(self._upd(speed))
            self.add(a)
            a.update(0)

    def _upd(self, speed):
        def f(a, dt):
            a.ph = (a.ph + speed * dt) % 1
            s = a.ph * self.total
            k = max(i for i in range(len(self.cum) - 1) if self.cum[i] <= s + 1e-9)
            seg = self.pts[k + 1] - self.pts[k]
            L = float(np.linalg.norm(seg)) or 1
            pos = self.pts[k] + seg / L * (s - self.cum[k])
            ang = math.atan2(seg[1], seg[0])
            f_ = 1.0
            for m in self.mults:
                f_ *= m.get_value()
            size, width, color = a.base
            a.become(arrow_at(pos, ang, max(size * f_, 0.05), max(width * f_, 0.8), color))
            op = min(1.0, 5 * min(a.ph, 1 - a.ph))
            if self.vis is not None:
                op *= self.vis.get_value()
            a.set_opacity(op)
        return f


def tick(x, y, s=0.17, color=GREEN):
    return VGroup(Line([x - s, y, 0], [x - s * 0.3, y - s * 0.8, 0]),
                  Line([x - s * 0.3, y - s * 0.8, 0], [x + s, y + s * 0.9, 0])).set_stroke(color, 5)


def make_scale(angle, c, sz, nl, nr, cl=TEALC, cr=BLUE):
    base = Triangle(color=GOLD, fill_opacity=0.5, stroke_width=3).scale(0.3 * sz).move_to(c + UP * 0.2 * sz)
    pivot = c + UP * 1.2 * sz
    post = Line(c + UP * 0.35 * sz, pivot, color=GOLD, stroke_width=5)
    L = 1.3 * sz
    el = pivot + np.array([-math.cos(angle), math.sin(angle), 0]) * L
    er = pivot + np.array([math.cos(angle), -math.sin(angle), 0]) * L
    beam = Line(el, er, color=GOLD, stroke_width=6)
    g = VGroup(base, post, beam)
    for end, n, col in ((el, nl, cl), (er, nr, cr)):
        pan_c = end + DOWN * 0.85 * sz
        g.add(Line(end, pan_c + LEFT * 0.5 * sz, color=GOLD, stroke_width=2.5), Line(end, pan_c + RIGHT * 0.5 * sz, color=GOLD, stroke_width=2.5),
              Line(pan_c + LEFT * 0.55 * sz, pan_c + RIGHT * 0.55 * sz, color=GOLD, stroke_width=6))
        for i in range(n):
            r, ci = divmod(i, 5)
            g.add(Dot(pan_c + np.array([(ci - 2) * 0.2 * sz, 0.14 * sz + r * 0.2 * sz, 0]), radius=0.085 * sz, color=col))
    return g


class Scale(VGroup):
    def __init__(self, c, sz=1.0, nl=1, nr=1, tilt=0.0, **kw):
        super().__init__()
        self.t = ValueTracker(tilt)
        self.c, self.sz, self.nl, self.nr, self.kw = np.array([c[0], c[1], 0.0]), sz, nl, nr, kw
        self.add(*make_scale(tilt, self.c, sz, nl, nr, **kw).submobjects)
        self.add_updater(lambda m: m.become_parts())

    def become_parts(self):
        new = make_scale(self.t.get_value(), self.c, self.sz, self.nl, self.nr, **self.kw)
        self.submobjects = list(new.submobjects)


class Gauge(VGroup):
    def __init__(self, x, base, w, hmax, color, h0=0.0, n=9, seed=0, outline=True, dots=True):
        super().__init__()
        self.h = ValueTracker(h0)
        if outline:
            self.add(Rectangle(width=w, height=hmax, stroke_color=color, stroke_width=3, fill_opacity=0).move_to([x, base + hmax / 2, 0]))
        self.fill = Rectangle(width=w, height=0.02, stroke_width=0, fill_color=color, fill_opacity=0.6)

        def fu(m):
            h = max(self.h.get_value(), 0.02)
            m.become(Rectangle(width=w, height=h, stroke_width=0, fill_color=color, fill_opacity=0.6).move_to([x, base + h / 2, 0]))
        self.fill.add_updater(fu)
        self.fill.update(0)
        self.add(self.fill)
        rng = random.Random(seed)
        if dots:
            for _ in range(n):
                d = Dot(radius=0.06, color=TEXT)
                d.u, d.v = rng.random(), rng.random()
                d.du, d.dv = rng.uniform(-0.25, 0.25), rng.uniform(-0.25, 0.25)

                def f(m, dt):
                    m.u += m.du * dt
                    m.v += m.dv * dt
                    if not 0.05 < m.u < 0.95:
                        m.du *= -1
                        m.u = min(max(m.u, 0.05), 0.95)
                    if not 0.05 < m.v < 0.95:
                        m.dv *= -1
                        m.v = min(max(m.v, 0.05), 0.95)
                    h = self.h.get_value()
                    m.move_to([x - w / 2 + m.u * w, base + m.v * h, 0])
                    m.set_opacity(0.75 if h > 0.35 else 0)
                d.add_updater(f)
                d.update(0)
                self.add(d)


class Leaf:
    """One cross-section of a leaf surface, same place in every scene (pore at x = dx)."""

    def __init__(self, g=0.45, half=6.9, sides=True, bottom_xs=(-4.4, -2.2, 0, 2.2, 4.4), dx=0.0, dy=0.0):
        self.g = ValueTracker(g)
        P = lambda x, y: np.array([x + dx, y + dy, 0.0])
        self.P = P
        self.cells = VGroup()
        for x in bottom_xs:
            self.cells.add(Ellipse(width=2.2, height=1.8).move_to(P(x, -2.7)))
        film_cells = [self.cells[i] for i in range(len(bottom_xs)) if abs(bottom_xs[i]) <= 2.3]
        if sides:
            for x in (-3.5, 3.5):
                c = Ellipse(width=1.8, height=1.9).move_to(P(x, -0.8))
                self.cells.add(c)
                film_cells.append(c)
            for x in (-5.7, 5.7):
                self.cells.add(Ellipse(width=2.0, height=1.9).move_to(P(x, -0.8)))
        self.cells.set_stroke(GREY, 4).set_fill(GREY, 0.3)
        self.film = VGroup(*[c.copy().set_fill(opacity=0).set_stroke(BLUE, 6) for c in film_cells])
        self.film.ph = 0.0
        def shimmer(m, dt):
            m.ph += dt * 3.0
            m.set_stroke(width=6 + 2.5 * math.sin(m.ph), opacity=0.75 + 0.25 * math.sin(m.ph * 0.7))
        self.film.add_updater(shimmer)
        self.wl = Rectangle(width=half, height=0.4, stroke_width=2, stroke_color=GREY, fill_color=GREY, fill_opacity=0.5)
        self.wr = self.wl.copy()
        self.gl = Ellipse(width=0.9, height=1.4, stroke_color=PURPLE, stroke_width=3, fill_color=PURPLE, fill_opacity=0.5)
        self.gr = self.gl.copy()

        def place(m=None):
            gg = self.g.get_value()
            self.wl.move_to(P(-(gg + half / 2), 1.2))
            self.wr.move_to(P(gg + half / 2, 1.2))
            self.gl.move_to(P(-(gg + 0.45), 0.85))
            self.gr.move_to(P(gg + 0.45, 0.85))
        place()
        self.wl.add_updater(place)
        self.wax = VGroup(self.wl, self.wr)
        self.guards = VGroup(self.gl, self.gr)


def label(text, x, y, color=TEXT, size=28):
    return T(text, size, color).move_to([x, y, 0])


def teal_streams(leaf, mults=(), thin=False, n=3):
    P = leaf.P
    sz, w = (0.4, 4) if thin else (0.55, 6)
    return VGroup(PathStream([P(-0.9, 3.0), P(-0.25, 1.2), P(-1.9, -1.6)], TEALC, n, 0.14, sz, w, mults, 0.0),
                  PathStream([P(-0.3, 3.0), P(-0.25, 1.2), P(-0.4, -1.6)], TEALC, n, 0.14, sz, w, mults, 0.3))


def blue_streams(leaf, mults=(), n=3, extra=False, thick=False):
    P = leaf.P
    sz, w = (0.7, 10) if thick else (0.55, 6)
    s = [PathStream([P(1.9, -1.6), P(0.2, 0.8), P(0.8, 3.0)], BLUE, n, 0.14, sz, w, mults, 0.15),
         PathStream([P(0.5, -1.6), P(0.15, 0.8), P(0.3, 3.0)], BLUE, n, 0.14, sz, w, mults, 0.55)]
    if extra:
        s.append(PathStream([P(-0.3, -1.6), P(0.05, 0.8), P(0.0, 3.0)], BLUE, n, 0.14, sz, w, mults, 0.35))
        s.append(PathStream([P(3.0, -1.2), P(0.3, 0.7), P(1.2, 3.0)], BLUE, n, 0.14, sz, w, mults, 0.8))
    return VGroup(*s)



def plant():
    stem = Line([0, -0.7, 0], [0, 0.95, 0], color=GREY, stroke_width=4)
    leaves = VGroup(*[Ellipse(width=0.65, height=0.22, color=GREY, fill_opacity=0.2).rotate(a).move_to([x, y, 0])
                      for x, y, a in [(-0.27, 0.1, -0.5), (0.27, 0.45, 0.5)]])
    grain = VGroup(*[Ellipse(width=0.23, height=0.35, color=GREY, fill_opacity=0.2).move_to([x, y, 0]) for x, y in [(-0.12, 0.85), (0.12, 1.1), (0, 1.35)]])
    return VGroup(stem, leaves, grain)




# ---------------------------------------------------------------- film 2 helpers
def motes(scene, n=10, seed=0, color=GREY):
    rng = random.Random(seed)
    for _ in range(n):
        d = Dot(radius=0.05, color=color).set_opacity(0.35)
        d.vx, d.vy = rng.uniform(-0.25, 0.25), rng.uniform(-0.2, 0.2)
        d.move_to([rng.uniform(-6.6, 6.6), rng.uniform(-3.6, 3.6), 0])

        def f(m, dt):
            m.shift([m.vx * dt, m.vy * dt, 0])
            p = m.get_center()
            if abs(p[0]) > 6.7:
                m.move_to([-p[0] * 0.98, p[1], 0])
            if abs(p[1]) > 3.7:
                m.move_to([p[0], -p[1] * 0.98, 0])
        d.add_updater(f)
        scene.add(d)


def pore():
    return Ellipse(width=0.5, height=0.3, stroke_color=PURPLE, stroke_width=3, fill_color=PURPLE, fill_opacity=0.8)


def sway(m, amp=0.05, speed=1.3, about=None, ph=0.0):
    m.t, m.prev = ph, 0.0
    pt = about if about is not None else m.get_bottom()

    def f(mm, dt):
        mm.t += dt
        a = amp * math.sin(mm.t * speed)
        mm.rotate(a - mm.prev, about_point=pt)
        mm.prev = a
    m.add_updater(f)
    return m


def barley_head(cx, y0, n=8, fill=0.25):
    stem = Line([cx, y0 - 2.4, 0], [cx, y0 + 0.2, 0], color=GREEN, stroke_width=5)
    grains = VGroup()
    for i in range(n):
        for s in (-1, 1):
            grains.add(Ellipse(width=0.3, height=0.55, stroke_color=GREEN, stroke_width=3, fill_color=GREEN,
                               fill_opacity=fill).rotate(-s * 0.45).move_to([cx + s * 0.24, y0 + 0.45 * i + (0.2 if s > 0 else 0), 0]))
    return stem, grains


def yield_chart():
    xs = [-4.6, -3.3, -2.0, 2.0, 3.3, 4.6]
    H = [3.6, 3.5, 3.4, 2.5, 2.4, 2.4]
    base = -1.9
    bars, errs, names = VGroup(), VGroup(), VGroup()
    for i, (x, h) in enumerate(zip(xs, H)):
        if i % 3 == 0:
            b = Rectangle(width=1.15, height=h, stroke_color=GREY, stroke_width=3, fill_color=GREY, fill_opacity=0.65)
        else:
            b = Rectangle(width=1.15, height=h, stroke_width=0, fill_color=GREEN, fill_opacity=0.7)
        b.move_to([x, base + h / 2, 0])
        if i % 3:
            b = VGroup(b, DashedVMobject(Rectangle(width=1.15, height=h, stroke_color=GREEN, stroke_width=3).move_to([x, base + h / 2, 0]), num_dashes=24))
        bars.add(b)
        top = base + h
        errs.add(VGroup(Line([x, top - 0.7, 0], [x, top + 0.7, 0]), Line([x - 0.2, top + 0.7, 0], [x + 0.2, top + 0.7, 0]),
                        Line([x - 0.2, top - 0.7, 0], [x + 0.2, top - 0.7, 0])).set_stroke(TEXT, 3))
    for i, x in enumerate(xs):
        names.add(label(["control", "line 1", "line 2"][i % 3], x, -2.4, TEXT, 24))
    groups = VGroup(label("well watered", -3.2, -3.5, BLUE, 30), label("water restricted", 3.2, -3.5, BLUE, 30))
    return bars, errs, names, groups, xs, H, base


def jiggle(group, amp=0.1):
    for i, g in enumerate(group):
        g.ph, g.b0 = i * 1.1, g.get_center()
        g.add_updater(lambda m, dt: (setattr(m, "ph", m.ph + dt * 2.2), m.move_to(m.b0 + np.array([0, amp * math.sin(m.ph), 0]))))
    return group


def tree(cx, y0, w, h, depth=3, color=GREY, sw=3):
    levels = [[np.array([cx, y0, 0.0])]]
    edges = []
    for k in range(1, depth + 1):
        n = 2 ** k
        pts = [np.array([cx - w / 2 + (i + 0.5) / n * w, y0 + k * h / depth, 0.0]) for i in range(n)]
        e = VGroup(*[Line(levels[-1][i // 2], p, color=color, stroke_width=sw) for i, p in enumerate(pts)])
        edges.append(e)
        levels.append(pts)
    nodes = VGroup(*[Circle(radius=0.11 * (sw / 3), stroke_color=color, stroke_width=sw, fill_opacity=0).move_to(p) for lv in levels for p in lv])
    return edges, nodes


def field(cx, w, y0, hmax, n=16, seed=2, color=GREEN, sw=4):
    rng = random.Random(seed)
    g = VGroup()
    for i in range(n):
        x = cx - w / 2 + (i + 0.5) / n * w
        h = hmax * rng.uniform(0.6, 1.0)
        b = Line([x, y0, 0], [x + rng.uniform(-0.2, 0.2), y0 + h, 0], color=color, stroke_width=sw)
        sway(b, 0.12, rng.uniform(1.0, 2.0), np.array([x, y0, 0]), rng.uniform(0, 6))
        g.add(b)
    return g


def dim_card(txt, size=34, y=3.35, color=GOLD):
    return T(txt, size, color).move_to([0, y, 0])


# ---------------------------------------------------------------- scenes
class S00Title(TitleCard):
    LESSON = "What an Organism Has to Do"
    TITLE = "Fewer Pores"


class S01Question(SpokenScene):
    def construct(self):
        motes(self, 8, 1)
        c = np.array([-2.0, -0.4, 0])
        leaf = Ellipse(width=9.6, height=6.0).set_stroke(GREEN, 5).set_fill(GREEN, 0.35).move_to(c)
        rib = Line([-6.8, -0.4, 0], [2.8, -0.4, 0], color=GREEN, stroke_width=3)
        rng = random.Random(4)
        pores = VGroup()
        while len(pores) < 34:
            x, y = rng.uniform(-6.6, 2.6), rng.uniform(-3.2, 2.4)
            if ((x - c[0]) / 4.4) ** 2 + ((y - c[1]) / 2.7) ** 2 < 1 and abs(y - c[1]) > 0.3:
                p = pore().move_to([x, y, 0])
                p.ph = rng.uniform(0, 6)
                p.base = p.get_center()
                p.add_updater(lambda m, dt: (setattr(m, "ph", m.ph + dt), m.move_to(m.base + np.array([0.06 * math.sin(m.ph), 0.05 * math.cos(m.ph * 1.3), 0]))))
                pores.add(p)
        blade = VGroup(leaf, rib, pores)
        self.play(FadeIn(blade), run_time=0.5)
        self.at("remove most")
        self.play(FadeOut(VGroup(*pores[5:])), run_time=1.4)
        self.at("does the plant")
        stem, grains = barley_head(5.6, -1.0, 8, 0.2)
        self.play(FadeIn(stem), FadeIn(grains), run_time=0.8)
        self.at("go hungry")
        q = T("?", 96, YELLOW, weight=BOLD).move_to([5.6, 3.0, 0])
        self.play(FadeIn(q, scale=1.3), run_time=0.6)
        self.at("or can it save")
        card = dim_card("Fewer pores: a hungry plant?").move_to([-1.0, 3.45, 0])
        self.play(FadeIn(card), FadeOut(q), run_time=0.6)
        self.at("water")
        drops = VGroup()
        for i in range(5):
            d = Dot(radius=0.12, color=BLUE).move_to([-4 + i * 1.2, -0.4, 0])
            d.ph = i * 1.3
            d.add_updater(lambda m, dt: (setattr(m, "ph", m.ph + dt), m.shift([0, 0.01 * math.sin(m.ph * 2), 0])))
            drops.add(d)
        self.play(FadeIn(drops), run_time=0.5)
        self.at("fill its grain")
        self.play(grains.animate.set_fill(GREEN, 0.85), run_time=1.5)
        self.finish()


class S02Link(SpokenScene):
    def construct(self):
        motes(self, 8, 2)

        def leaf_top(x, dashed):
            e = Ellipse(width=4.8, height=3.6).move_to([x, 0.5, 0])
            fill = e.copy().set_stroke(width=0).set_fill(GREEN, 0.35)
            outline = DashedVMobject(e.copy().set_stroke(GREEN, 4), num_dashes=40) if dashed else e.copy().set_stroke(GREEN, 4).set_fill(opacity=0)
            return VGroup(fill, outline)
        la, lb = leaf_top(-4.0, False), leaf_top(0.9, True)
        rng = random.Random(8)
        pa, pb = VGroup(), VGroup()
        for G, x in ((pa, -4.0), (pb, 0.9)):
            while len(G) < 14:
                px, py = x + rng.uniform(-2.1, 2.1), 0.5 + rng.uniform(-1.6, 1.6)
                if (((px - x) / 2.2) ** 2 + ((py - 0.5) / 1.6) ** 2) < 1:
                    G.add(pore().move_to([px, py, 0]))
        self.play(FadeIn(la), FadeIn(lb), FadeIn(pa), FadeIn(pb), run_time=1.0)
        ta = label("leaf A", -4.0, -1.8, TEXT, 30)
        self.add(ta)
        self.at("leaf with fewer pores")
        sc = Scale([5.3, -1.1], 0.8, 3, 8, tilt=0.45)
        self.play(FadeOut(VGroup(*pb[4:])), FadeIn(sc), FadeIn(label("leaf B was made up", 0.9, -1.8, TEXT, 28)), run_time=1.2)
        self.at("pay less water")
        self.play(sc.t.animate.set_value(0.15), run_time=1.6)
        self.at("a real experiment")
        self.play(FadeOut(VGroup(la, lb, pa, pb, sc, ta, *[m for m in self.mobjects if isinstance(m, Text)])), run_time=0.8)
        bench = Line([-6.4, -1.8, 0], [6.4, -1.8, 0], color=GREY, stroke_width=8)
        self.play(Create(bench), run_time=0.6)
        plants = VGroup()
        for i, x in enumerate([-5.0, -3.0, -1.0, 1.0, 3.0, 5.0]):
            p = plant().set_height(3.6).move_to([x, 0.1, 0])
            sway(p, 0.04, 1.2, p.get_bottom(), i)
            plants.add(p)
        self.play(LaggedStart(*[FadeIn(p, shift=UP * 0.2) for p in plants], lag_ratio=0.2), run_time=1.6)
        self.finish()


class S03Gene(SpokenScene):
    def construct(self):
        motes(self, 6, 3)
        pl = plant().set_height(5.0).move_to([0, 0.2, 0])
        sway(pl, 0.04, 1.2, pl.get_bottom())
        barley = label("barley", 0, -2.8, TEXT, 30)
        credit = T("Hughes, Gray and colleagues, Plant Physiology, 2017", 24, TEXT).move_to([0, -3.4, 0])
        self.play(FadeIn(pl), FadeIn(credit), run_time=0.8)
        self.at("worked in barley")
        self.play(FadeIn(barley), run_time=0.5)
        self.at("overexpress")
        cell = Ellipse(width=8.8, height=5.6).set_stroke(GREY, 5).set_fill(GREY, 0.22).move_to([1.0, 0.3, 0])
        self.play(pl.animate.set_height(3.0).move_to([-5.8, 0.3, 0]), barley.animate.move_to([-5.8, -2.5, 0]), FadeIn(cell), run_time=1.4)
        self.at("hvepf1")
        gene = VGroup(RoundedRectangle(corner_radius=0.15, width=3.0, height=0.8, stroke_color=YELLOW, stroke_width=3, fill_color="#3a3410", fill_opacity=1),
                      T("HvEPF1 gene", 28, YELLOW)).move_to([-8.5, 1.2, 0])
        self.add(gene)
        self.play(gene.animate.move_to([-0.8, 1.2, 0]), run_time=1.4)
        self.at("making extra")
        prods = VGroup()
        for i in range(12):
            b = RoundedRectangle(corner_radius=0.06, width=0.7, height=0.42, stroke_color=YELLOW, stroke_width=3, fill_color=YELLOW, fill_opacity=0.7)
            b.ph = i / 12
            b.dy = random.Random(i).uniform(-1.3, 0.9)
            b.sy = random.Random(i + 9).uniform(-0.2, 0.2)

            def f(m, dt):
                m.ph = (m.ph + 0.12 * dt) % 1
                x = 1.7 + m.ph * 4.1
                m.move_to([x, 1.2 + m.dy * min(1, m.ph * 3) * 0.9 + 0.1 * math.sin(m.ph * 20), 0])
                m.set_opacity(min(1, 4 * m.ph, 4 * (1 - m.ph)))
            b.add_updater(f)
            b.update(0)
            prods.add(b)
        self.add(prods)
        self.at("gene's product")
        lab = label("HvEPF1 product", 2.2, -1.6, YELLOW, 30)
        self.play(FadeIn(lab), run_time=0.6)
        self.finish()


class S04Job(SpokenScene):
    def construct(self):
        motes(self, 6, 4)
        xs = [-5.0, -3.6, -2.2, -0.8, 0.6, 2.0]
        cells = VGroup(*[Circle(radius=0.55, stroke_color=GREY, stroke_width=5, fill_color=GREY, fill_opacity=0.5).move_to([x, -1.2, 0]) for x in xs])
        self.play(FadeIn(cells), FadeIn(label("young leaf cells", -1.5, -2.3, TEXT, 28)), run_time=1.0)
        self.at("limits leaf cells")
        arrs = VGroup(*[Arrow([x, -0.55, 0], [x, 1.1, 0], buff=0, color=TEXT, stroke_width=9) for x in xs])
        self.play(LaggedStart(*[GrowArrow(a) for a in arrs], lag_ratio=0.15), run_time=1.6)
        slots = VGroup(*[DashedVMobject(Ellipse(width=0.9, height=0.55, stroke_color=PURPLE, stroke_width=3), num_dashes=16).move_to([x, 1.7, 0]) for x in xs])
        self.at("stomatal development")
        self.play(FadeIn(slots), run_time=0.8)
        self.at("moving through")
        blocked = [0, 1, 3, 4]
        blocks = VGroup(*[RoundedRectangle(corner_radius=0.06, width=1.2, height=0.4, stroke_color=YELLOW, stroke_width=3, fill_color=YELLOW, fill_opacity=0.8).move_to([xs[i], 2.8, 0]) for i in blocked])
        self.add(blocks, label("HvEPF1 product", -2.2, 3.5, YELLOW, 28))
        self.play(*[b.animate.move_to([xs[i], 0.3, 0]) for b, i in zip(blocks, blocked)], run_time=1.4)
        self.at("fewer stomata")
        keep = [2, 5]
        self.play(*[FadeOut(arrs[i]) for i in blocked], *[slots[i].animate.set_opacity(0.2) for i in blocked],
                  *[Transform(slots[i], pore().scale(2.0).move_to([xs[i], 1.7, 0])) for i in keep], run_time=1.4)
        self.at("empty vector")
        pl = plant().set_height(3.6).move_to([5.2, 1.0, 0])
        sway(pl, 0.04, 1.2, pl.get_bottom())
        ctrl = VGroup(T("empty-vector", 26, TEXT), T("control:", 26, TEXT), T("same procedure,", 24, TEXT), T("no added gene", 24, TEXT)).arrange(DOWN, buff=0.12).move_to([5.2, -2.3, 0])
        self.play(FadeIn(pl), FadeIn(ctrl), run_time=1.0)
        self.finish()


class S05Density(SpokenScene):
    def construct(self):
        motes(self, 5, 5)
        strip = RoundedRectangle(corner_radius=0.2, width=7.0, height=0.8, stroke_color=GREEN, stroke_width=4, fill_color=GREEN, fill_opacity=0.45).move_to([-2, -0.8, 0])
        resin = Rectangle(width=7.0, height=0.9, stroke_color=BLUE, stroke_width=4, fill_color=BLUE, fill_opacity=0.4).move_to([-2, 1.9, 0])
        rl = label("resin", 3.2, 0.0, TEXT, 30)
        self.play(FadeIn(strip), FadeIn(resin), run_time=0.5)
        self.play(resin.animate.move_to([-2, -0.15, 0]), FadeIn(rl), run_time=0.9)
        self.play(resin.animate.move_to([-2, 1.4, 0]), run_time=0.7)
        vl = label("varnish copy", 3.2, 0.0, TEXT, 30)
        slide = Rectangle(width=2.2, height=0.5, stroke_color=TEXT, stroke_width=3, fill_opacity=0).move_to([-2, 1.4, 0])
        self.play(FadeOut(rl), FadeIn(vl), FadeIn(slide), run_time=0.5)
        mic = VGroup(Rectangle(width=1.2, height=0.4, color=GREY), Rectangle(width=0.4, height=1.6, color=GREY).shift(UP * 0.8),
                     Circle(radius=0.3, color=GREY).shift(UP * 1.8)).move_to([4.8, -0.9, 0])
        self.play(FadeIn(mic), slide.animate.move_to([4.8, -0.6, 0]), run_time=0.8)
        self.at("two engineered lines")
        self.play(FadeOut(VGroup(strip, resin, vl, slide, mic)), run_time=0.4)
        rng = random.Random(6)
        fields = VGroup()
        xs, counts = [-4.5, 0, 4.5], [32, 8, 4]
        for x, n in zip(xs, counts):
            circ = Circle(radius=2.0, stroke_color=TEXT, stroke_width=5, fill_color=GREY, fill_opacity=0.22).move_to([x, 0.9, 0])
            g = VGroup(circ)
            k = 0
            while k < n:
                px, py = rng.uniform(-1.8, 1.8), rng.uniform(-1.8, 1.8)
                if px * px + py * py < 1.75 ** 2:
                    p = pore()
                    p.base = np.array([x + px, 0.9 + py, 0]); p.ph = rng.uniform(0, 6)
                    p.move_to(p.base)
                    p.add_updater(lambda m, dt: (setattr(m, "ph", m.ph + dt), m.move_to(m.base + np.array([0.05 * math.sin(m.ph), 0.04 * math.cos(m.ph * 1.2), 0]))))
                    g.add(p); k += 1
            fields.add(g)
        self.play(FadeIn(fields), FadeIn(label("mature sixth leaf", 0, 3.4, TEXT, 30)), run_time=1.0)
        for x, t in zip(xs, ["control", "line 1", "line 2"]):
            self.add(label(t, x, -1.5, TEXT, 30))
        self.at("about a quarter")
        self.play(FadeIn(VGroup(label("about 24%", 0, -2.3, YELLOW, 34), label("of control", 0, -2.85, TEXT, 24))), run_time=0.6)
        self.at("an eighth")
        self.play(FadeIn(VGroup(label("about 12%", 4.4, -2.3, YELLOW, 34), label("of control", 4.4, -2.85, TEXT, 24))), run_time=0.6)
        self.finish()


class S06Controls(SpokenScene):
    def construct(self):
        motes(self, 5, 6)
        xs = [-4.4, 0, 4.4]
        pls = VGroup()
        for i, x in enumerate(xs):
            p = plant().set_height(3.8).move_to([x, 1.2, 0])
            sway(p, 0.04, 1.2, p.get_bottom(), i)
            pls.add(p)
        names = VGroup(*[label(t, x, -1.0, TEXT, 28) for t, x in zip(["empty-vector control", "line 1", "line 2"], xs)])
        self.at("why the controls")
        self.play(FadeIn(pls), FadeIn(names), run_time=1.2)
        self.at("procedure itself")
        vec = VGroup(RoundedRectangle(corner_radius=0.15, width=3.0, height=0.6, stroke_color=GREY, stroke_width=3, fill_color=GREY, fill_opacity=0.3),
                     T("vector with DNA", 24, TEXT)).move_to([-7.5, 3.5, 0])
        self.add(vec)
        self.play(vec.animate.move_to([7.5, 3.5, 0]), run_time=3.0, rate_func=linear)
        self.remove(vec)
        self.at("inserted gene lands")
        chr1 = RoundedRectangle(corner_radius=0.25, width=0.5, height=2.2, stroke_color=GREY, stroke_width=3).move_to([0, -2.3, 0])
        g1 = Rectangle(width=0.62, height=0.22, stroke_color=YELLOW, stroke_width=3, fill_color=YELLOW, fill_opacity=0.7).move_to([0, -1.7, 0])
        self.play(FadeIn(chr1), FadeIn(g1, shift=DOWN * 0.3), run_time=1.0)
        self.at("somewhere in the genome")
        chr2 = chr1.copy().move_to([4.4, -2.3, 0])
        g2 = g1.copy().move_to([4.4, -2.9, 0])
        self.play(FadeIn(chr2), FadeIn(g2, shift=DOWN * 0.3), run_time=1.0)
        self.add(VGroup(T("insertion site", 26, YELLOW), T("differs", 26, YELLOW)).arrange(DOWN, buff=0.1).move_to([2.2, -2.3, 0]))
        self.at("two independent lines")
        self.play(Indicate(pls[1], scale_factor=1.12), Indicate(pls[2], scale_factor=1.12), run_time=1.2)
        self.at("landing spot effect")
        self.play(Indicate(g1, color=GOLD), Indicate(g2, color=GOLD), run_time=1.5)
        self.finish()


def chamber(cx, dashed, m=None):
    e = Ellipse(width=3.9, height=1.9).move_to([cx, 0.3, 0])
    fill = e.copy().set_stroke(width=0).set_fill(GREEN, 0.4)
    out = DashedVMobject(e.copy().set_stroke(GREEN, 4), num_dashes=36) if dashed else e.copy().set_stroke(GREEN, 4).set_fill(opacity=0)
    top = RoundedRectangle(corner_radius=0.1, width=4.6, height=0.5, stroke_color=GREY, stroke_width=3, fill_color=GREY, fill_opacity=0.7).move_to([cx, 1.45, 0])
    bot = top.copy().move_to([cx, -0.85, 0])
    tubes = VGroup(Rectangle(width=0.55, height=1.4, stroke_color=GREY, stroke_width=3).move_to([cx - 0.8, 2.3, 0]),
                   Rectangle(width=0.55, height=1.4, stroke_color=GREY, stroke_width=3).move_to([cx + 0.8, 2.3, 0]))
    return VGroup(fill, out), top, bot, tubes


class S07Chamber(SpokenScene):
    def construct(self):
        motes(self, 5, 7)
        m = ValueTracker(1.0)
        cxs = [-4.4, 4.4]
        L = [chamber(cxs[0], False), chamber(cxs[1], True)]
        for lf, top, bot, tubes in L:
            top.shift(UP * 0.9); bot.shift(DOWN * 0.9)
        self.play(*[FadeIn(lf) for lf, *_ in L], FadeIn(VGroup(*[l[1] for l in L])), FadeIn(VGroup(*[l[2] for l in L])), run_time=0.8)
        self.at("clamped")
        self.play(*[l[1].animate.shift(DOWN * 0.9) for l in L], *[l[2].animate.shift(UP * 0.9) for l in L], run_time=1.0)
        self.add(label("control", cxs[0], -1.7, TEXT, 28), label("engineered", cxs[1], -1.7, TEXT, 28))
        self.at("small chamber")
        self.play(FadeIn(L[0][3]), FadeIn(L[1][3]), run_time=0.8)
        self.at("measures gas")
        for i, cx in enumerate(cxs):
            mults = (m,) if i else ()
            self.add(PathStream([[cx - 0.8, 3.0], [cx - 0.8, 0.8]], TEALC, 2, 0.18, 0.5, 5, mults, 0.0),
                     PathStream([[cx + 0.8, 0.8], [cx + 0.8, 3.0]], BLUE, 2, 0.18, 0.5, 5, mults, 0.3))
        self.at("in well")
        gc = Gauge(-0.6, -3.0, 0.9, 5.2, GREY, 4.6, seed=1)
        ge = Gauge(0.6, -3.0, 0.9, 5.2, GREY, 4.6, seed=2)
        self.play(FadeIn(gc), FadeIn(ge), FadeIn(label("gas exchange (stomatal conductance)", 0, 3.5, TEXT, 28)), run_time=0.8)
        self.at("leaves with fewer")
        self.play(m.animate.set_value(0.3), ge.h.animate.set_value(1.6), run_time=3.2)
        self.add(T("schematic consequence of lower conductance, not a reported transpiration comparison", 24, TEXT).move_to([0, -3.55, 0]))
        self.finish()


def gas_gauges():
    return Gauge(-4.8, -3.0, 0.9, 5.2, GREY, 1.6, seed=3)


def slots():
    s1 = Rectangle(width=1.9, height=4.2, stroke_color=TEALC, stroke_width=4, fill_color=TEALC, fill_opacity=0.15).move_to([-0.6, -0.9, 0])
    s2 = Rectangle(width=1.9, height=4.2, stroke_color=GREEN, stroke_width=4, fill_color=GREEN, fill_opacity=0.15).move_to([3.6, -0.9, 0])
    return s1, s2


class S08Predict(SpokenScene):
    def construct(self):
        motes(self, 6, 8)
        g = gas_gauges()
        gl = label("gas exchange", -4.8, -3.4, TEXT, 28)
        self.add(g, gl)
        self.play(Indicate(g, color=YELLOW, scale_factor=1.06), run_time=1.5)
        self.at("carbon taken in")
        s1, s2 = slots()
        q1 = T("?", 96, TEALC, weight=BOLD).move_to(s1)
        self.play(FadeIn(s1), FadeIn(q1), FadeIn(label("carbon gained", -0.6, -3.4, TEALC, 28)), run_time=0.8)
        self.at("grain")
        q2 = T("?", 96, GREEN, weight=BOLD).move_to(s2)
        self.play(FadeIn(s2), FadeIn(q2), FadeIn(label("grain yield", 3.6, -3.4, GREEN, 28)), run_time=0.8)
        self.at("did they fall")
        self.play(FadeIn(dim_card("Did carbon and grain fall as steeply?")), run_time=0.7)
        for q in (q1, q2):
            q.ph = 0
            q.add_updater(lambda mm, dt: (setattr(mm, "ph", mm.ph + dt), mm.set_opacity(0.7 + 0.3 * math.sin(mm.ph * 4))))
        self.finish()


class S09Pause(NarratedScene):
    def construct(self):
        g = gas_gauges()
        s1, s2 = slots()
        self.add(g, label("gas exchange", -4.8, -3.4, TEXT, 28), s1, s2,
                 T("?", 96, TEALC, weight=BOLD).move_to(s1), T("?", 96, GREEN, weight=BOLD).move_to(s2),
                 label("carbon gained", -0.6, -3.4, TEALC, 28), label("grain yield", 3.6, -3.4, GREEN, 28),
                 dim_card("Did carbon and grain fall as steeply?"))
        p = ValueTracker(0.01)
        self.add(Circle(radius=0.4, stroke_color=GREY, stroke_width=4).move_to([6.0, 3.0, 0]),
                 always_redraw(lambda: Arc(radius=0.4, start_angle=PI / 2, angle=-TAU * p.get_value(), stroke_color=GOLD, stroke_width=7).move_to([6.0, 3.0, 0])))
        self.play(p.animate.set_value(1.0), run_time=self.beat(0.9), rate_func=linear)
        self.finish()


class S10Carbon(SpokenScene):
    def construct(self):
        L = Leaf(g=0.45)
        tm, bm = ValueTracker(1.0), ValueTracker(1.0)
        base, hmax = 1.55, 1.7
        go = Gauge(-6.0, base, 0.8, hmax, TEALC, 1.7, seed=1)
        gi = Gauge(-4.6, base, 0.8, hmax, TEALC, 1.35, seed=2)
        sc = Scale([5.4, 1.55], 0.8, 1, 8, tilt=0.45)
        world = VGroup(L.cells, L.wax, L.guards, L.film)
        self.play(FadeIn(world), run_time=1.0)
        tst, bst = teal_streams(L, (tm,), thin=True), blue_streams(L, (bm,), thick=True, extra=True)
        self.add(tst, bst, sc)
        self.add(go, gi, label("outside", -6.0, 3.55, TEALC, 24), label("inside", -4.6, 3.55, TEALC, 24))
        gen = T("general physiology, schematic, not measured in this study", 24, TEXT).move_to([1.2, 3.6, 0])
        self.play(FadeIn(gen), run_time=0.5)
        br = always_redraw(lambda: VGroup(Line([-3.95, base + gi.h.get_value(), 0], [-3.7, base + gi.h.get_value(), 0]),
                                          Line([-3.7, base + gi.h.get_value(), 0], [-3.7, base + go.h.get_value(), 0]),
                                          Line([-3.95, base + go.h.get_value(), 0], [-3.7, base + go.h.get_value(), 0])).set_stroke(YELLOW, 5))
        self.add(br)
        self.at("slow gas flow")
        self.play(L.g.animate.set_value(0.15), tm.animate.set_value(0.7), bm.animate.set_value(0.5), run_time=1.8)
        self.at("carbon dioxide inside")
        self.play(gi.h.animate.set_value(0.8), run_time=2.0)
        self.at("its gap")
        self.add(label("CO₂ gap", -2.8, 2.35, YELLOW, 30))
        self.play(Indicate(br, color=YELLOW, scale_factor=1.3), run_time=1.5)
        self.at("props up carbon gain")
        self.play(tm.animate.set_value(0.85), run_time=1.6)
        self.at("save more water")
        self.play(bm.animate.set_value(0.25), sc.t.animate.set_value(0.12), run_time=2.0)
        self.at("in this study")
        everything = Group(*[m for m in self.mobjects])
        self.play(FadeOut(everything), run_time=0.8)
        self.add(dim_card("In this study", 34, 3.3, TEXT))
        motes(self, 8, 10)
        self.at("one efficiency measure")
        self.play(FadeIn(T("water-use efficiency", 44, TEXT).move_to([0, 2.0, 0])), FadeIn(T("(from leaf carbon isotopes)", 28, TEXT).move_to([0, 1.3, 0])), run_time=0.8)
        self.at("rose in both lines")
        xs = [-3.6, 0, 3.6]
        ar = VGroup()
        for x in xs[1:]:
            a = Arrow([x, -1.4, 0], [x, 0.0, 0], buff=0, color=GREEN, stroke_width=10)
            a.ph = 0
            a.add_updater(lambda mm, dt: (setattr(mm, "ph", mm.ph + dt), mm.shift([0, 0.004 * math.sin(mm.ph * 3), 0])))
            ar.add(a)
        flat = Line([-4.2, -0.5, 0], [-3.0, -0.5, 0], color=GREY, stroke_width=8)
        self.play(FadeIn(flat), *[GrowArrow(a) for a in ar], *[FadeIn(label(t, x, -2.1, TEXT, 30)) for t, x in zip(["control", "line 1", "line 2"], xs)], run_time=1.2)
        self.at("under water")
        self.play(FadeIn(label("water restricted", 0, 0.6, YELLOW, 32)), run_time=0.6)
        self.at("measures did not")
        self.play(FadeIn(label("measures did not all agree", 0, -3.2, TEXT, 32)), run_time=0.8)
        self.finish()


def ychart_scene(scene, with_names=True):
    bars, errs, names, groups, xs, H, base = yield_chart()
    return bars, errs, names, groups, xs, H, base


class S11Grain(SpokenScene):
    def construct(self):
        motes(self, 6, 11)
        bars, errs, names, groups, xs, H, base = yield_chart()
        ax = Line([-6.2, base, 0], [6.2, base, 0], color=GREY, stroke_width=4)
        self.play(Create(ax), FadeIn(label("schematic", -5.6, 3.3, TEXT, 24)), FadeIn(names), FadeIn(groups), run_time=0.8)
        self.at("greenhouse trial")
        self.play(Indicate(groups, color=YELLOW, scale_factor=1.1), run_time=1.0)
        self.at("neither line")
        self.play(LaggedStart(*[GrowFromEdge(b, DOWN) for b in bars], lag_ratio=0.1), run_time=1.5)
        self.at("statistically significant")
        self.play(LaggedStart(*[Create(e) for e in errs], lag_ratio=0.1), run_time=1.2)
        jiggle(errs)
        self.at("well watered")
        self.play(Indicate(groups[0], color=YELLOW), run_time=1.0)
        self.at("water restricted")
        self.play(Indicate(groups[1], color=YELLOW), run_time=1.0)
        self.at("no drop")
        self.play(FadeIn(dim_card("no significant drop detected", 36, 3.3, YELLOW)), run_time=0.8)
        self.finish()


class S12Hedge(SpokenScene):
    def construct(self):
        motes(self, 6, 12)
        bars, errs, names, groups, xs, H, base = yield_chart()
        ax = Line([-6.2, base, 0], [6.2, base, 0], color=GREY, stroke_width=4)
        jiggle(errs)
        self.add(ax, bars, errs, names, groups, label("schematic", -5.6, 3.3, TEXT, 24))
        self.at("only five plants")
        icons = VGroup()
        for x in xs:
            for k in range(5):
                p = plant().set_height(0.42).move_to([x + (k - 2) * 0.21, -2.9, 0])
                sway(p, 0.15, 2.0 + k * 0.3, p.get_bottom(), k)
                icons.add(p)
        self.play(LaggedStart(*[FadeIn(i, shift=UP * 0.1) for i in icons], lag_ratio=0.03), run_time=2.0)
        self.at("a small loss")
        top = base + H[0]
        loss = label("a small loss could hide here", -1.4, 3.3, YELLOW, 28)
        band = DashedVMobject(Rectangle(width=3.8, height=0.8, stroke_color=YELLOW, stroke_width=4).move_to([-3.2, top - 0.4, 0]), num_dashes=30)
        self.play(Create(band), FadeIn(loss), run_time=1.5)
        self.play(Indicate(band, color=YELLOW, scale_factor=1.05), run_time=1.4)
        self.at("not proof")
        stamp = VGroup(RoundedRectangle(corner_radius=0.15, width=7.6, height=0.9, stroke_color=O2C, stroke_width=5),
                       T("not proof of equal yield", 36, O2C, weight=BOLD)).move_to([2.0, 3.2, 0])
        self.play(FadeOut(loss), FadeIn(stamp, scale=1.4), run_time=0.6)
        self.finish()


def split_world(cx_t=3.4):
    edges, nodes = tree(cx_t, -1.0, 4.4, 3.4)
    fld = field(cx_t, 5.0, -3.2, 1.4)
    return edges, nodes, fld


class S13How(SpokenScene):
    def construct(self):
        motes(self, 4, 13)
        div = Line([0, -3.7, 0], [0, 3.7, 0], color=GREY, stroke_width=3)
        hh = T("HOW", 44, YELLOW, weight=BOLD).move_to([-3.4, 3.3, 0])
        wh = T("WHY", 44, YELLOW, weight=BOLD).move_to([3.4, 3.3, 0])
        self.at("what kind of answer")
        self.play(Create(div), FadeIn(hh), FadeIn(wh), run_time=1.0)
        self.at("shows how one")
        c = Circle(radius=0.35, stroke_color=GREY, stroke_width=4, fill_color=GREY, fill_opacity=0.3).move_to([-5.6, 2.1, 0])
        st = pore().scale(1.8).move_to([-1.6, 2.1, 0])
        ar = Arrow([-5.1, 2.1, 0], [-2.2, 2.1, 0], buff=0, color=GREY, stroke_width=5)
        blk = RoundedRectangle(corner_radius=0.06, width=1.4, height=0.4, stroke_color=YELLOW, stroke_width=3, fill_color=YELLOW, fill_opacity=0.6).move_to([-3.6, 2.1, 0])
        self.play(FadeIn(c), FadeIn(ar), FadeIn(st), run_time=0.6)
        self.play(FadeIn(blk, shift=DOWN * 0.4), FadeIn(label("one gene limits stomata", -3.4, 1.1, TEXT, 28)), run_time=0.6)
        self.at("what fewer stomata")
        gg = Gauge(-5.6, -1.7, 0.7, 1.4, GREY, 0.5, seed=5)
        drop = Dot(radius=0.3, color=BLUE).move_to([-3.4, -1.0, 0])
        mb = VGroup(*[Rectangle(width=0.4, height=h, stroke_width=0, fill_color=GREEN, fill_opacity=0.6).move_to([-1.6 + (i - 1) * 0.5, -1.7 + h / 2, 0]) for i, h in enumerate([1.2, 1.1, 1.15])])
        self.play(FadeIn(gg), run_time=0.5)
        self.add(label("gas", -5.6, -2.3, TEXT, 28))
        self.at("water")
        self.play(FadeIn(drop), FadeIn(label("water", -3.4, -2.3, BLUE, 28)), run_time=0.5)
        self.at("and grain")
        self.play(FadeIn(mb), FadeIn(label("grain", -1.6, -2.3, GREEN, 28)), run_time=0.8)
        self.at("says nothing")
        edges, nodes, fld = split_world()
        self.play(FadeIn(fld), *[Create(e) for e in edges], FadeIn(nodes), run_time=1.0)
        q = T("?", 80, YELLOW, weight=BOLD).move_to([3.4, 0.9, 0]).add_background_rectangle(color=BG, opacity=0.8)
        self.at("about why wild")
        self.play(FadeIn(q, scale=1.3), run_time=0.5)
        self.at("wild barley")
        self.play(Indicate(fld, color=GREEN, scale_factor=1.05), run_time=0.7)
        self.at("evolved")
        self.play(Indicate(nodes, color=YELLOW, scale_factor=1.3), run_time=1.2)
        self.finish()


class S14Next(SpokenScene):
    def construct(self):
        motes(self, 4, 14)
        div = Line([0, -3.7, 0], [0, 3.7, 0], color=GREY, stroke_width=3)
        hh = T("HOW", 44, YELLOW, weight=BOLD).move_to([-3.4, 3.3, 0]).set_opacity(0.4)
        wh = T("WHY", 44, YELLOW, weight=BOLD).move_to([3.4, 3.3, 0])
        edges, nodes, fld = split_world()
        q = T("?", 80, GREY, weight=BOLD).move_to([3.4, 0.9, 0]).add_background_rectangle(color=BG, opacity=0.8)
        self.add(div, hh, wh, fld, *edges, nodes, q)
        self.at("lineages")
        self.play(Indicate(nodes, color=YELLOW, scale_factor=1.3), run_time=1.5)
        self.at("not one plant")
        self.play(Indicate(wh, color=YELLOW, scale_factor=1.2), run_time=1.2)
        self.at("answering it")
        bedges, bnodes = tree(0, -2.5, 11.0, 5.4, 3, GREY, 4)
        self.play(FadeOut(div), FadeOut(hh), FadeOut(fld), FadeOut(q), *[Transform(e, be) for e, be in zip(edges, bedges)],
                  Transform(nodes, bnodes), wh.animate.move_to([0, 3.4, 0]), run_time=2.0)
        rq = T("?", 56, GREY, weight=BOLD).move_to([0, -3.1, 0])
        self.add(rq)
        self.at("where the lesson")
        self.play(LaggedStart(*[LaggedStart(*[e.animate.set_color(GREEN).set_stroke(width=7) for e in lvl], lag_ratio=0.1) for lvl in edges], lag_ratio=0.5), run_time=2.4)
        self.finish()


class S15End(EndCard):
    LINE = "An experiment shows how a trait works, not why it evolved."
