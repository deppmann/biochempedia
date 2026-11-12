"""The Price of a Breath (organism-problems, film 1)

COLOUR MAP: CO2 = TEALC arrows; water vapour = BLUE; oxygen = RED (warm); guard cells / stomata = PURPLE;
the price = GOLD balance scale; wax, cells, labels = GREY.  Leaf world is one cross-section, same place every scene.
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


def bee():
    body = Ellipse(width=1.3, height=0.65, color=GREY, fill_opacity=0.2)
    wings = VGroup(*[Ellipse(width=0.7, height=0.42, color=GREY).rotate(a).move_to([x, 0.45, 0]) for x, a in [(-0.25, -0.6), (0.25, 0.6)]])
    head = Circle(radius=0.24, color=GREY).move_to([0.8, 0.1, 0])
    stripes = VGroup(*[Line([x, -0.25, 0], [x, 0.25, 0], color=GREY) for x in [-0.25, 0, 0.25]])
    return VGroup(body, wings, head, stripes)


def human():
    return VGroup(Circle(radius=0.25, color=GREY).move_to([0, 0.9, 0]), Line([0, 0.65, 0], [0, -0.3, 0], color=GREY, stroke_width=5),
                  Line([-0.6, 0, 0], [0, 0.4, 0], color=GREY, stroke_width=5), Line([0, 0.4, 0], [0.6, 0, 0], color=GREY, stroke_width=5),
                  Line([-0.45, -1.1, 0], [0, -0.3, 0], color=GREY, stroke_width=5), Line([0, -0.3, 0], [0.45, -1.1, 0], color=GREY, stroke_width=5))


ROWS = ["energy and materials", "exchange and transport", "a stable inside", "defense", "reproduction"]
RY = [1.6, 0.5, -0.6, -1.7, -2.8]
COLX = [2.7, 4.2, 5.7]


def icons():
    g = VGroup()
    for f, x in zip((plant, bee, human), COLX):
        ic = f()
        ic.set_height(1.0).move_to([x, 2.85, 0])
        ic.ph = random.random() * 6

        def bob(m, dt):
            m.ph += dt * 2.2
            m.shift(UP * 0.06 * (math.sin(m.ph) - math.sin(m.ph - dt * 2.2)))
        ic.add_updater(bob)
        g.add(ic)
    return g


def checklist():
    sq, txt, tk = VGroup(), VGroup(), VGroup()
    for r, y in zip(ROWS, RY):
        s = Square(0.36, color=GREY, stroke_width=3).move_to([-6.3, y, 0])
        t = T(r, 30, TEXT)
        t.next_to(s, RIGHT, buff=0.25)
        sq.add(s)
        txt.add(t)
        tk.add(tick(-6.3, y + 0.02))
    return sq, txt, tk


def price_tag(y):
    b = Polygon([-0.45, 0.25, 0], [0.3, 0.25, 0], [0.55, 0, 0], [0.3, -0.25, 0], [-0.45, -0.25, 0], color=GOLD, stroke_width=3,
                fill_color=GOLD, fill_opacity=0.12)
    q = T("?", 28, GOLD, weight=BOLD).move_to(b.get_center())
    return VGroup(b, q).move_to([0.9, y, 0])


class Chest:
    def __init__(self, cx=-2.9, h=7.0):
        self.cx = cx
        self.torso = RoundedRectangle(corner_radius=1.4, width=4.8, height=h, stroke_color=GREY, stroke_width=3).move_to([cx, 0, 0])
        self.trach = VGroup(Line([cx - 0.35, 3.5, 0], [cx - 0.35, 1.7, 0]), Line([cx + 0.35, 3.5, 0], [cx + 0.35, 1.7, 0]),
                            Line([cx - 0.35, 1.7, 0], [cx - 1.1, 1.0, 0]), Line([cx + 0.35, 1.7, 0], [cx + 1.1, 1.0, 0])).set_stroke(GREY, 4)
        self.lungs = VGroup()
        for s in (-1, 1):
            self.lungs.add(Ellipse(width=2.0, height=3.4).set_stroke(GREY, 3).set_fill(GREY, 0.12).move_to([cx + s * 1.1, -0.7, 0]))
            rng = random.Random(3 + s)
            for i in range(9):
                a, r = rng.uniform(0, 2 * math.pi), rng.uniform(0.0, 0.6)
                self.lungs.add(Circle(radius=0.2, stroke_color=BLUE, stroke_width=3, fill_color=BLUE, fill_opacity=0.15)
                               .move_to([cx + s * 1.1 + r * math.cos(a) * 0.9, -0.7 + r * math.sin(a) * 1.9, 0]))
        self.lungs.ph = 0.0
        self.lungs.sprev = 1.0

        def breathe(m, dt):
            m.ph += dt * 2 * math.pi / 3.6
            s = 1 + 0.07 * math.sin(m.ph)
            m.scale(s / m.sprev, about_point=np.array([cx, -0.7, 0]))
            m.sprev = s
        self.lungs.add_updater(breathe)
        self.body = VGroup(self.torso, self.trach)

    def streams(self, red=True, blue=True):
        cx = self.cx
        g = VGroup()
        if red:
            g.add(PathStream([[cx - 0.15, 3.4], [cx - 0.15, 1.8], [cx - 1.0, 0.4]], O2C, 3, 0.15, 0.55, 6, (), 0.0),
                  PathStream([[cx - 0.1, 3.4], [cx - 0.1, 1.8], [cx + 1.2, 0.4]], O2C, 3, 0.15, 0.55, 6, (), 0.4))
        if blue:
            g.add(PathStream([[cx - 1.1, 0.5], [cx + 0.15, 1.9], [cx + 0.15, 3.4]], BLUE, 3, 0.15, 0.5, 5, (), 0.2),
                  PathStream([[cx + 1.2, 0.5], [cx + 0.2, 1.9], [cx + 0.2, 3.4]], BLUE, 3, 0.15, 0.5, 5, (), 0.7))
        return g


def question_card():
    return VGroup(T("More water per", 40, GOLD), T("molecule of gas,", 40, GOLD), T("or less?", 40, GOLD)).arrange(DOWN, buff=0.15).move_to([3.4, 1.0, 0])


class S00Title(TitleCard):
    LESSON = "What an Organism Has to Do"
    TITLE = "The Price of a Breath"


class S01Question(SpokenScene):
    def construct(self):
        leaf = Ellipse(width=10, height=2.6).set_stroke(GREEN, 4).set_fill(GREEN, 0.22).move_to([0, -1.1, 0])
        rib = Line([-5, -1.1, 0], [5, -1.1, 0], color=GREEN, stroke_width=3)
        blade = VGroup(leaf, rib)
        blade.t, blade.prev = 0.0, 0.0

        def sway(m, dt):
            m.t += dt
            a = 0.05 * math.sin(m.t * 1.3)
            m.rotate(a - m.prev, about_point=np.array([-5, -1.1, 0]))
            m.prev = a
        blade.add_updater(sway)
        self.play(FadeIn(blade), run_time=0.8)
        card = VGroup(T("Why can't a leaf take carbon dioxide", 36), T("without losing water?", 36)).arrange(DOWN, buff=0.15).move_to([0, 3.0, 0])
        self.play(FadeIn(card), run_time=0.7)
        up_t = VGroup(*[PathStream([[x, 1.9], [x, 0.2]], TEALC, 2, 0.18, 0.55, 7, (), i * 0.2) for i, x in enumerate((-4, -1.4, 1.4, 4))])
        up_b = VGroup(*[PathStream([[x, 0.2], [x, 1.9]], BLUE, 2, 0.18, 0.55, 7, (), i * 0.3) for i, x in enumerate((-2.7, 0, 2.7, 5.2))])
        under_t = VGroup(*[PathStream([[x, -3.6], [x, -2.5]], TEALC, 1, 0.2, 0.5, 6, (), i * 0.3) for i, x in enumerate((-3, 0, 3))])
        self.add(up_t)
        self.wait(2.0)
        self.add(up_b)
        self.at("taking something in")
        self.add(under_t)
        self.at("carries a cost")
        tag = price_tag(0.0).scale(1.4).move_to([5.9, -1.1, 0])
        self.play(FadeIn(tag, shift=DOWN * 0.2), run_time=0.5)
        self.at("easy to see")
        self.play(Indicate(tag, color=GOLD, scale_factor=1.15), run_time=0.9)
        self.finish()


class S02Checklist(SpokenScene):
    def construct(self):
        sq, txt, tk = checklist()
        ic = icons()
        head = T("five problems", 30, GOLD).move_to([-3.6, 2.85, 0])
        self.at("every multicellular organism")
        self.play(FadeIn(ic), FadeIn(sq), FadeIn(head), run_time=1.0)
        cues = ["get energy and materials", "exchange and move them", "keep its inside", "resist damage and invasion", "leave descendants"]
        for i, c in enumerate(cues):
            self.at(c)
            self.play(FadeIn(txt[i], shift=RIGHT * 0.3), run_time=0.5)
            self.play(Create(tk[i]), run_time=0.4)
        self.finish()


class S03Price(SpokenScene):
    def construct(self):
        sq, txt, tk = checklist()
        ic = icons()
        self.add(sq, txt, tk, ic)
        ticks = VGroup(*[tick(x, y) for y in RY for x in COLX])
        self.at("each body solves all five")
        self.play(LaggedStart(*[Create(t) for t in ticks], lag_ratio=0.12), run_time=3.2)
        tags = VGroup(*[price_tag(y) for y in RY])
        self.at("many solutions carry a cost")
        self.play(LaggedStart(*[FadeIn(t, shift=LEFT * 0.4) for t in tags], lag_ratio=0.2), run_time=2.0)
        self.at("the exchange problem")
        glow = SurroundingRectangle(VGroup(txt[1], tags[1]), color=GOLD, buff=0.1, stroke_width=4)
        self.play(Create(glow), tags[1][0].animate.set_fill(GOLD, 0.7), run_time=0.8)
        self.at("most clearly")
        dim = [m for i in (0, 2, 3, 4) for m in (txt[i], tags[i], sq[i], tk[i])] + [ticks[j] for j in range(15) if j // 3 != 1]
        self.play(*[m.animate.set_opacity(0.2) for m in dim], run_time=1.0)
        self.finish()


class S04Pore(SpokenScene):
    def construct(self):
        L = Leaf(g=0.45)
        self.play(FadeIn(L.cells), run_time=1.2)
        self.at("a waxy layer covers")
        self.play(FadeIn(L.wax), run_time=0.7)
        wl = label("waxy layer", -4.3, 2.35, GREY)
        self.play(FadeIn(wl), run_time=0.4)
        self.at("and water crosses it poorly")
        beads = VGroup()
        rng = random.Random(5)
        for i in range(9):
            d = Dot(radius=0.11, color=BLUE)
            d.x0, d.ph, d.sp = rng.choice([-1, 1]) * rng.uniform(1.9, 6.3), rng.uniform(0, 6), rng.uniform(1.8, 3.0)

            def bounce(m, dt):
                m.ph += dt * m.sp
                m.move_to([m.x0 + 0.3 * math.sin(m.ph * 0.5), 0.55 + 0.4 * abs(math.sin(m.ph)), 0])
            d.add_updater(bounce)
            d.update(0)
            beads.add(d)
        self.play(FadeIn(beads), run_time=0.6)
        self.at("so gas moves mainly through")
        pl = label("stoma (pore)", 0, 2.45, TEXT)
        pa = Arrow(pl.get_bottom(), [0, 1.0, 0], buff=0.1, color=TEXT, stroke_width=4)
        self.play(FadeIn(pl), Create(pa), FadeOut(wl), run_time=0.7)
        self.at("two guard cells flank")
        self.play(FadeIn(L.guards, shift=DOWN * 0.2), run_time=0.8)
        gl = label("guard cells", 4.4, 2.45, PURPLE)
        ga = Arrow(gl.get_left(), [1.15, 1.5, 0], buff=0.15, color=PURPLE, stroke_width=4)
        self.play(FadeIn(gl), Create(ga), run_time=0.7)
        self.at("and open or close the gap")
        self.play(L.g.animate.set_value(0.8), run_time=1.5)
        self.play(L.g.animate.set_value(0.15), run_time=1.5)
        self.play(L.g.animate.set_value(0.45), run_time=1.2)
        self.finish()


class S05Inside(SpokenScene):
    def construct(self):
        L = Leaf(g=0.45)
        self.add(L.cells, L.wax, L.guards)
        self.at("inside the leaf")
        glow = Ellipse(width=5.2, height=2.6, stroke_color=TEXT, stroke_width=3).move_to([0, -0.7, 0])
        glow.set_stroke(opacity=0.5)
        self.play(Create(glow), run_time=1.2)
        self.at("cell walls line")
        self.play(FadeOut(glow), run_time=0.4)
        self.play(Create(L.film), run_time=1.4)
        self.at("those walls are wet")
        wl = label("wet cell walls", -3.6, 0.6, BLUE)
        wa = Arrow(wl.get_bottom(), [-3.5, 0.2, 0], buff=0.05, color=BLUE, stroke_width=4)
        self.play(FadeIn(wl), Create(wa), run_time=0.7)
        self.at("carbon dioxide must dissolve")
        self.add(teal_streams(L))
        self.at("but a wet surface")
        self.add(blue_streams(L))
        self.finish()


class S06Same(SpokenScene):
    def construct(self):
        L = Leaf(g=0.45)
        tm, bm = ValueTracker(1.0), ValueTracker(1.0)
        self.add(L.cells, L.wax, L.guards, L.film)
        self.add(teal_streams(L, (tm,)), blue_streams(L, (bm,)))
        self.at("so water vapor leaves")
        self.add(blue_streams(L, (bm,), extra=True)[2:])
        self.play(tm.animate.set_value(0.65), bm.animate.set_value(1.5), run_time=1.5)
        self.at("both gases take one path")
        self.play(Indicate(L.guards, color=PURPLE, scale_factor=1.05), run_time=1.2)
        self.at("what then sets the price")
        sc = Scale([5.0, 1.85], 0.8, 0, 0)
        lab = T("price = water lost / carbon gained", 28, GOLD).move_to([3.2, 3.5, 0])
        self.play(FadeIn(sc), FadeIn(lab), run_time=1.0)
        self.finish()


class S07Co2gap(SpokenScene):
    def construct(self):
        base = -2.6
        o = Gauge(-4.6, base, 1.3, 4.8, TEALC, 0.0, seed=1)
        i = Gauge(-2.8, base, 1.3, 4.8, TEALC, 0.0, seed=2)
        title = T("carbon dioxide in air", 30, TEALC).move_to([-3.7, 3.3, 0])
        self.at("look at two gaps")
        self.add(o, i)
        self.play(FadeIn(title), run_time=1.0)
        self.add(label("outside", -4.6, -3.15), label("inside", -2.8, -3.15))
        self.at("first the carbon dioxide gap")
        self.play(o.h.animate.set_value(4.6), i.h.animate.set_value(4.6), run_time=2.0)
        self.at("carbon dioxide is a tiny share")
        t1 = VGroup(T("CO₂ ≈ 0.04%", 36, TEALC), T("of air", 36, TEALC)).arrange(DOWN, buff=0.1).move_to([4.2, 1.2, 0])
        t2 = label("schematic", 4.2, -0.3, GREY, 24)
        self.play(FadeIn(t1), FadeIn(t2), run_time=0.8)
        self.at("draws it down only part")
        self.play(i.h.animate.set_value(3.3), run_time=1.6)
        br = VGroup(Line([-1.9, base + 3.3, 0], [-1.6, base + 3.3, 0]), Line([-1.6, base + 3.3, 0], [-1.6, base + 4.6, 0]),
                    Line([-1.9, base + 4.6, 0], [-1.6, base + 4.6, 0])).set_stroke(YELLOW, 5)
        gl = label("CO₂ gap", -0.3, base + 3.95, YELLOW, 32)
        self.play(Create(br), FadeIn(gl), run_time=0.9)
        self.finish()


class S08Watergap(SpokenScene):
    def construct(self):
        base = -2.6
        o = Gauge(-4.6, base, 1.3, 4.8, TEALC, 4.6, seed=1)
        i = Gauge(-2.8, base, 1.3, 4.8, TEALC, 3.3, seed=2)
        title = T("carbon dioxide in air", 30, TEALC).move_to([-3.7, 3.3, 0])
        lo, li = label("outside", -4.6, -3.15), label("inside", -2.8, -3.15)
        self.add(title, o, i, lo, li)
        self.at("now the water gap")
        gapbar = Gauge(-3.9, base, 1.0, 3.2, TEALC, 1.3, seed=3, outline=False, dots=False)
        self.remove(o, i)
        self.play(FadeOut(lo), FadeOut(li), FadeOut(title), run_time=1.0)
        self.add(gapbar)
        self.add(label("CO₂ gap", -3.9, -3.15, TEALC, 30))
        wcol = Rectangle(width=1.4, height=1.6, stroke_color=BLUE, stroke_width=3, fill_color=BLUE, fill_opacity=0.12).move_to([-1.3, base + 0.8, 0])
        self.at("air inside a leaf is saturated")
        wgap = Gauge(-1.3, base + 1.6, 1.4, 3.0, BLUE, 0.0, seed=4, outline=False)
        self.add(wcol, wgap)
        self.play(wgap.h.animate.set_value(3.0), gapbar.h.animate.set_value(0.03), run_time=2.2)
        self.play(FadeIn(label("inside: saturated", 1.7, base + 4.6, BLUE, 28)), run_time=0.5)
        self.at("while outside air is drier")
        self.play(FadeIn(label("outside: drier", 1.5, base + 1.6, BLUE, 28)), run_time=0.5)
        self.at("that gap is far bigger")
        t = T("water gap ≈ 100 × CO₂ gap", 30, YELLOW).move_to([-0.2, 3.45, 0])
        self.play(FadeIn(label("water gap", -1.3, -3.15, BLUE, 30)), FadeIn(t), run_time=0.8)
        self.at("so the leaf pays")
        sc = Scale([4.3, -0.9], 1.0, 1, 14, tilt=0.0)
        self.play(FadeIn(sc), run_time=0.5)
        self.play(sc.t.animate.set_value(0.45), run_time=1.6)
        tx = VGroup(T("hundreds of H₂O per CO₂", 24), T("(depends on the air)", 24, GREY)).arrange(DOWN, buff=0.08).move_to([4.6, -3.2, 0])
        self.play(FadeIn(tx), run_time=0.6)
        self.finish()


class S09Speed(SpokenScene):
    def construct(self):
        L = Leaf(g=0.45)
        shr = ValueTracker(1.0)
        self.add(L.cells, L.wax, L.guards, L.film)
        self.add(teal_streams(L, (shr,), thin=True), blue_streams(L, (shr,), thick=True, extra=True), Scale([5.0, 1.85], 0.8, 1, 8, tilt=0.45))
        t0 = label("gaps held fixed for now", -4.0, 3.4, YELLOW, 30)
        self.add(t0)
        self.play(L.g.animate.set_value(0.12), shr.animate.set_value(0.35), run_time=3.5)
        self.at("both streams shrink together")
        self.wait(0.5)
        self.at("the pores set how fast")
        self.play(FadeOut(t0), run_time=0.3)
        self.play(FadeIn(label("pores → how fast", -4.1, 3.4, PURPLE, 30)), run_time=0.5)
        self.at("the two gaps set the price")
        self.play(FadeIn(label("gaps → the price", -4.1, 2.7, GOLD, 30)), run_time=0.5)
        self.play(L.g.animate.set_value(0.2), shr.animate.set_value(0.5), run_time=2.0)
        self.finish()


class S10Predict(SpokenScene):
    def construct(self):
        ch = Chest()
        self.at("your lung also moves")
        self.add(ch.lungs)
        self.play(FadeIn(ch.body), run_time=1.5)
        self.at("a wet surface")
        wl = label("wet surface", 3.4, -0.7, BLUE, 30)
        self.play(FadeIn(wl), Indicate(ch.lungs, color=BLUE, scale_factor=1.03), run_time=1.2)
        self.at("it takes in oxygen")
        self.add(ch.streams(True, False))
        ol = label("oxygen in", 3.4, 2.6, O2C, 32)
        self.play(FadeIn(ol), run_time=0.5)
        self.at("will it pay more water")
        self.add(ch.streams(False, True))
        self.play(FadeOut(wl), FadeOut(ol), run_time=0.3)
        self.play(FadeIn(question_card()), run_time=0.8)
        self.finish()


class S11Pause(NarratedScene):
    def construct(self):
        ch = Chest()
        self.add(ch.body, ch.lungs, ch.streams(True, True), question_card())
        ring_bg = Circle(radius=0.5, stroke_color=GREY, stroke_width=4).move_to([3.4, -2.2, 0])
        p = ValueTracker(0.01)
        ring = always_redraw(lambda: Arc(radius=0.5, start_angle=PI / 2, angle=-TAU * p.get_value(), stroke_color=GOLD, stroke_width=7).move_to([3.4, -2.2, 0]))
        self.add(ring_bg, ring)
        self.play(p.animate.set_value(1.0), run_time=self.beat(0.9), rate_func=linear)
        self.finish()


class S12Lung(SpokenScene):
    def construct(self):
        ch = Chest()
        qc = question_card()
        self.add(ch.body, ch.lungs, ch.streams(True, True), qc)
        base, k = -2.7, 0.2
        self.at("far less")
        self.play(FadeOut(qc), run_time=0.6)
        hr, hw = label("oxygen", 2.45, 3.4, O2C, 30), label("water vapor", 5.25, 3.4, BLUE, 30)
        self.play(FadeIn(hr), FadeIn(hw), run_time=0.6)
        self.at("oxygen is plentiful in air")
        ri = Gauge(1.7, base, 1.1, 4.4, O2C, 0.0, seed=1, outline=False)
        li = label("in", 1.7, -3.2, TEXT, 26)
        self.add(ri, li)
        v1 = VGroup(T("about", 24), T("21%", 24)).arrange(DOWN, buff=0.05).move_to([1.7, base + 21 * k + 0.55, 0])
        self.play(ri.h.animate.set_value(21 * k), run_time=1.6)
        self.play(FadeIn(v1), run_time=0.4)
        self.at("so each breath can hand over")
        ro = Gauge(3.2, base, 1.1, 4.4, O2C, 21 * k, seed=2, outline=False)
        lo = label("out", 3.2, -3.2, TEXT, 26)
        self.add(ro, lo)
        self.play(ro.h.animate.set_value(16 * k), run_time=1.6)
        v2 = VGroup(T("about", 24), T("16%", 24)).arrange(DOWN, buff=0.05).move_to([3.2, base + 16 * k + 0.55, 0])
        self.play(FadeIn(v2), run_time=0.4)
        self.at("the breath out carries away")
        wi = Gauge(4.6, base, 1.0, 2.0, BLUE, 0.0, seed=3, outline=False)
        wo = Gauge(5.9, base, 1.0, 2.0, BLUE, 0.0, seed=4, outline=False)
        i3, o3 = label("in", 4.6, -3.2, TEXT, 26), label("out", 5.9, -3.2, TEXT, 26)
        self.add(wi, wo, i3, o3)
        self.play(wi.h.animate.set_value(1 * k), wo.h.animate.set_value(5.5 * k), run_time=1.6)
        vi = VGroup(T("about", 24, BLUE), T("1%", 24, BLUE)).arrange(DOWN, buff=0.05).move_to([4.6, base + 1 * k + 0.7, 0])
        vo = VGroup(T("about", 24, BLUE), T("5 to 6%", 24, BLUE)).arrange(DOWN, buff=0.05).move_to([5.9, base + 5.5 * k + 0.75, 0])
        self.play(FadeIn(vi), FadeIn(vo), run_time=0.5)
        self.at("so the lung pays")
        self.play(FadeOut(VGroup(ri, ro, wi, wo, hr, hw, li, lo, i3, o3, v1, v2, vi, vo)), run_time=0.8)
        sc = Scale([3.7, -1.5], 1.4, 1, 1, tilt=0.05, cl=O2C, cr=BLUE)
        t1 = T("about 1 H₂O per O₂", 36, GOLD).move_to([3.7, 2.7, 0])
        t2 = VGroup(T("varies with breathing,", 24, GREY), T("temperature and humidity", 24, GREY)).arrange(DOWN, buff=0.08).move_to([3.7, 1.5, 0])
        self.play(FadeIn(sc), FadeIn(t1), run_time=0.8)
        self.play(FadeIn(t2), FadeIn(label("schematic", 6.0, -3.2, GREY, 24)), run_time=0.6)
        self.finish()


class S13Close(SpokenScene):
    def construct(self):
        L = Leaf(g=0.06, half=3.2, sides=False, bottom_xs=(-2.2, 0, 2.2), dx=-3.3, dy=0.7)
        self.add(L.cells, L.wax, L.guards)
        self.at("but the lung cannot close")
        ch = Chest(cx=3.4, h=6.0)
        self.play(FadeIn(ch.body), FadeIn(ch.lungs), FadeIn(L.film), run_time=1.2)
        self.play(FadeIn(label("nearly closed", -3.3, 3.45, PURPLE, 28)), run_time=0.5)
        self.at("it sits sheltered deep")
        self.add(ch.streams(True, True))
        self.at("in ordinary unsaturated air")
        self.play(FadeIn(label("unsaturated air", 0.0, 3.45, YELLOW, 28)), run_time=0.5)
        shr = ValueTracker(0.4)
        self.add(PathStream([L.P(-0.3, 2.4), L.P(0.0, 1.0), L.P(-0.5, -1.6)], TEALC, 1, 0.12, 0.4, 4, (shr,)),
                 PathStream([L.P(0.5, -1.6), L.P(0.05, 0.9), L.P(0.3, 2.4)], BLUE, 1, 0.12, 0.4, 4, (shr,), 0.5),
                 PathStream([L.P(2.0, 0.4), L.P(2.4, 2.4)], BLUE, 1, 0.1, 0.35, 3, (), 0.2))
        self.at("narrowing or sheltering")
        sc1 = Scale([-5.4, -3.8], 0.45, 1, 2, tilt=0.15)
        sc2 = Scale([5.6, -3.8], 0.45, 1, 1, tilt=0.05, cl=O2C)
        self.play(FadeIn(sc1), FadeIn(sc2), run_time=0.6)
        self.at("but while gas keeps flowing in")
        self.play(FadeIn(label("only the leaf can close", 0, -3.5, TEXT, 28)), run_time=0.6)
        self.finish()


class S14Checklist(SpokenScene):
    def construct(self):
        sq, txt, tk = checklist()
        ic = icons()
        tags = VGroup(*[price_tag(y) for y in RY])
        ticks = VGroup(*[tick(x, y) for y in RY for x in COLX])
        self.add(sq, txt, tk, ic, ticks, tags)
        self.at("back to the checklist")
        self.play(Indicate(txt, color=GOLD, scale_factor=1.03), run_time=1.4)
        self.at("for every row")
        self.play(LaggedStart(*[Indicate(t, color=GOLD, scale_factor=1.25) for t in tags], lag_ratio=0.25), run_time=2.2)
        self.at("and where that cost is paid")
        tags[1][0].set_fill(GOLD, 0.7)
        sc_a = Scale([-3.0, -3.0], 0.0001, 0, 0)
        self.play(Indicate(tags[1], color=GOLD, scale_factor=1.4), run_time=1.0)
        self.at("then ask how you would test it")
        self.play(FadeIn(label("how would you test it?", 0, -3.5, YELLOW, 32)), run_time=0.6)
        self.finish()


class S15End(EndCard):
    LINE = "A leaf pays water for carbon; the two gaps set the price."
