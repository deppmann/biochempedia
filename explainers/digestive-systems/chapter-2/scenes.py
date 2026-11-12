"""How Does the Stomach Know Food Is Coming? (digestive systems, film 2 = chapter 2)

COLOR MAP (same as film 1, plus two additions)
  GREY (light)  = food
  BLUE          = water, bile, pancreatic juice (bicarbonate, enzymes)
  GREEN         = microbes (not used here)
  GOLD          = acid, gastric juice, the stomach
  RED           = blood
  PALE YELLOW   = lacteal (not used here)
  ORANGE        = fat
  TAN           = duodenal / small-intestine wall
  WHITE         = nerves (new)
  PURPLE        = hormones, small dots carried in RED blood (new)
Two worlds, each carried: the film-1 tube (gutg) and a cartoon dog with a cutaway of its gut; a close-up of
the duodenal wall with its capillary, pancreas, and gallbladder.
"""
import importlib.util
from pathlib import Path
import numpy as np
from bp_style import *  # noqa: F401,F403

_spec = importlib.util.spec_from_file_location("film1_scenes", str(Path(__file__).resolve().parent.parent / "scenes.py"))
_f1 = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(_f1)
FOOD, PALE, ORANGE, TAN = _f1.FOOD, _f1.PALE, _f1.ORANGE, _f1.TAN
XM0, XM1, XS1, XI1, XA1 = _f1.XM0, _f1.XM1, _f1.XS1, _f1.XI1, _f1.XA1
L, runner, food_block, setsz, food_size, dot, brk, gutg, ripple = (
    _f1.L, _f1.runner, _f1.food_block, _f1.setsz, _f1.food_size, _f1.dot, _f1.brk, _f1.gutg, _f1.ripple)

PURPLE = "#B07CE8"
DOGFILL = "#262A36"


# ------------------------------------------------------------------ generic helpers
def flow(m, pts, speed, phase=0.0, gate=None, fade=0.3, loop=True):
    """Move m along a polyline forever, fading in and out at the ends; gate (ValueTracker) scales opacity."""
    pts = [np.array(p, float) for p in pts]
    seg = [float(np.linalg.norm(pts[i + 1] - pts[i])) for i in range(len(pts) - 1)]
    tot = sum(seg)
    m._t = phase

    def upd(mm, dt):
        mm._t += dt
        s = (mm._t * speed) % tot if loop else max(0.0, min(mm._t * speed, tot - 1e-6))
        k = 0
        while k < len(seg) - 1 and s > seg[k]:
            s -= seg[k]
            k += 1
        f = s / seg[k] if seg[k] > 0 else 0
        mm.move_to(pts[k] + (pts[k + 1] - pts[k]) * f)
        done = sum(seg[:k]) + s
        op = min(1.0, done / (fade * speed), (tot - done) / (fade * speed)) if loop else 1.0
        g = gate.get_value() if gate is not None else 1.0
        mm.set_opacity(max(0.0, min(1.0, op * g)))
    m.add_updater(upd)
    upd(m, 0)
    return m


def clock(center, r=0.6, rate=1.3, color=TEXT):
    face = Circle(radius=r, stroke_color=color, stroke_width=5, fill_color=BG, fill_opacity=1).move_to(center)
    ticks = VGroup(*[Line(np.array(center) + r * 0.8 * np.array([np.sin(a), np.cos(a), 0]),
                          np.array(center) + r * 0.95 * np.array([np.sin(a), np.cos(a), 0])).set_stroke(color, 3)
                     for a in np.arange(0, TAU, TAU / 4)])
    hand = Line(center, np.array(center) + np.array([0, r * 0.75, 0]), color=GOLD, stroke_width=6)
    hand._a = 0.0
    hand._rate = rate
    hand._c = np.array(center, float)

    def upd(m, dt):
        da = -m._rate * dt
        m.rotate(da, about_point=m._c)
    hand.add_updater(upd)
    return VGroup(face, ticks, hand), hand


def pulse_stroke(m, color, n=2, t=0.5):
    return [m.animate.set_stroke(color, 8) for _ in range(1)]


# ------------------------------------------------------------------ the dog (cartoon cutaway)
class Dog:
    """A cartoon dog, side view, facing left, with its gut drawn inside. Design coordinates (unscaled):
    mouth at left (-4.4, 0.45), stomach ellipse at (0.4, -0.5), bowl at (-4.9, -2.0), neck dish at (-2.9, -2.0)."""

    def __init__(self, sc=1.0, ox=0.0, oy=0.0):
        self.sc, self.ox, self.oy = sc, ox, oy
        p, S = self.p, self.S
        sw = lambda w: max(2.0, w * max(sc, 0.55))
        self.sw = sw
        legs = VGroup(*[RoundedRectangle(corner_radius=0.15 * sc, width=S(0.45), height=S(1.5), stroke_color=TEXT, stroke_width=sw(3),
                                         fill_color=DOGFILL, fill_opacity=1).move_to(p(x, -1.9)) for x in (-1.2, -0.4, 2.2, 3.0)])
        tail = Line(p(3.3, 0.15), p(4.1, 1.15), color=TEXT, stroke_width=sw(9))
        tail._a = 0.0
        tail._tt = 0.0
        base = p(3.3, 0.15)

        def wag(m, dt):
            m._tt += dt
            a = 0.35 * np.sin(5.0 * m._tt)
            m.rotate(a - m._a, about_point=base)
            m._a = a
        tail.add_updater(wag)
        body = Ellipse(width=S(5.2), height=S(2.4), stroke_color=TEXT, stroke_width=sw(3), fill_color=DOGFILL, fill_opacity=1).move_to(p(0.8, -0.2))
        neck = Polygon(p(-2.5, 1.35), p(-1.0, 0.66), p(-1.2, -0.97), p(-2.4, -0.45), stroke_width=0, fill_color=DOGFILL, fill_opacity=1)
        nl = VGroup(Line(p(-2.5, 1.35), p(-1.0, 0.66)), Line(p(-2.4, -0.45), p(-1.2, -0.97))).set_stroke(TEXT, sw(3))
        head = Circle(radius=S(0.85), stroke_color=TEXT, stroke_width=sw(3), fill_color=DOGFILL, fill_opacity=1).move_to(p(-3.0, 0.7))
        snout = Ellipse(width=S(1.3), height=S(0.7), stroke_color=TEXT, stroke_width=sw(3), fill_color=DOGFILL, fill_opacity=1).move_to(p(-3.8, 0.45))
        ear = Ellipse(width=S(0.45), height=S(0.95), stroke_color=TEXT, stroke_width=sw(3), fill_color="#343947", fill_opacity=1).rotate(0.3).move_to(p(-2.3, 0.65))
        nose = Dot(p(-4.4, 0.5), radius=0.09 * sc, color=TEXT)
        eye = Dot(p(-3.3, 0.95), radius=0.08 * sc, color=TEXT)
        self.body = body
        self.shell = VGroup(legs, tail, body, neck, nl, head, snout, ear, nose, eye)
        # the gut inside
        self.stomach = Ellipse(width=S(2.2), height=S(1.5), stroke_color=GOLD, stroke_width=sw(5), fill_color=GOLD, fill_opacity=0.16).move_to(p(0.4, -0.5))
        pl = lambda *pts: VMobject().set_points_as_corners([p(*q) for q in pts]).set_stroke(GREY, sw(11))
        self.upper = pl((-4.3, 0.45), (-3.1, 0.15), (-2.45, -0.3))
        self.lower = pl((-2.05, -0.25), (-1.25, -0.3), (-0.72, -0.42))
        self.bridge = Line(p(-2.45, -0.3), p(-2.05, -0.25), color=GREY, stroke_width=sw(11))
        bowl = Arc(radius=S(0.62), start_angle=PI, angle=PI, stroke_color=TEXT, stroke_width=sw(5), fill_color=TEXT, fill_opacity=0.18).move_to(p(-4.9, -2.31))
        meat = VGroup(*[self.block(0.3).move_to(p(-4.9 + dx, -2.12)) for dx in (-0.25, 0.0, 0.25)])
        for m in meat:
            m.set_opacity(1)
        self.bowl = VGroup(bowl, meat)
        dish = Arc(radius=S(0.62), start_angle=PI, angle=PI, stroke_color=TEXT, stroke_width=sw(5), fill_color=TEXT, fill_opacity=0.18).move_to(p(-2.9, -2.31))
        self.dish = dish
        self.pile = VGroup(*[self.block(0.26).move_to(p(-2.9 + dx, -2.1 + dy)) for dx, dy in ((-0.3, 0), (0.0, 0.02), (0.3, 0), (-0.14, 0.24), (0.16, 0.24))])
        for m in self.pile:
            m.set_opacity(1)
        # nerves, brainstem
        self.brain = Ellipse(width=S(0.5), height=S(0.4), stroke_color=TEXT, stroke_width=sw(4), fill_color=TEXT, fill_opacity=0.25).move_to(p(-2.8, 1.0))
        self.nA = (p(-2.65, 0.92), p(-0.2, 0.15))
        self.nB = (p(-2.6, 0.82), p(0.7, 0.24))

    # coordinate mapping
    def p(self, x, y):
        return np.array([x * self.sc + self.ox, y * self.sc + self.oy, 0.0])

    def S(self, v):
        return v * self.sc

    def block(self, w=0.3):
        b = RoundedRectangle(corner_radius=0.06 * self.sc, width=w * self.sc, height=w * 0.8 * self.sc, stroke_color=TEXT,
                             stroke_width=max(1.5, 2 * self.sc), fill_color=FOOD, fill_opacity=0.9)
        return b

    def world(self, cut=False, bowl=True, dish=False, pile=False):
        g = VGroup(self.shell, self.stomach, self.upper, self.lower)
        if not cut:
            g.add(self.bridge)
        if bowl:
            g.add(self.bowl)
        if dish:
            g.add(self.dish)
        if pile:
            g.add(self.pile)
        return g

    # paths for the eaten food
    def path_full(self):
        return [self.p(-4.9, -2.0), self.p(-4.3, 0.45), self.p(-3.1, 0.15), self.p(-2.45, -0.3), self.p(-2.05, -0.25), self.p(-1.25, -0.3), self.p(-0.72, -0.42)]

    def path_cut(self):
        return [self.p(-4.9, -2.0), self.p(-4.3, 0.45), self.p(-3.1, 0.15), self.p(-2.45, -0.3), self.p(-2.62, -0.9), self.p(-2.9, -1.85)]

    def food_flow(self, cut, n=4, speed=1.5, gate=None):
        pts = self.path_cut() if cut else self.path_full()
        tot = sum(float(np.linalg.norm(pts[i + 1] - pts[i])) for i in range(len(pts) - 1))
        sp = speed * self.sc
        out = VGroup()
        for i in range(n):
            b = self.block(0.32)
            flow(b, pts, sp, phase=i * tot / sp / n, gate=gate, fade=0.25)
            out.add(b)
        return out

    # fistula + flask
    def fistula(self, level=None):
        p, S = self.p, self.S
        tube = Line(p(0.4, -1.25), p(0.4, -2.3), color=GREY, stroke_width=self.sw(9))
        neck = Rectangle(width=S(0.36), height=S(0.3), stroke_color=TEXT, stroke_width=self.sw(4), fill_color=BG, fill_opacity=1).move_to(p(0.4, -2.4))
        body = RoundedRectangle(corner_radius=0.12 * self.sc, width=S(0.9), height=S(0.95), stroke_color=TEXT, stroke_width=self.sw(5),
                                fill_color=BG, fill_opacity=1).move_to(p(0.4, -3.025))
        parts = [tube, neck, body]
        if level is not None:
            bottom = p(0.4, -3.5)[1] + 0.04 * self.sc
            lev = Rectangle(width=S(0.8), height=0.01, stroke_width=0, fill_color=GOLD, fill_opacity=0.85)

            def up(m):
                h = max(0.01, level.get_value() * S(0.8))
                m.stretch_to_fit_height(h)
                m.move_to([self.p(0.4, 0)[0], bottom + h / 2, 0])
            lev.add_updater(up)
            up(lev)
            parts.append(lev)
        g = VGroup(*parts)
        g.flask = body
        g.tube = tube
        return g

    def drips(self, gate, n=4, speed=1.1):
        out = VGroup()
        pts = [self.p(0.4, -1.15), self.p(0.4, -2.85)]
        sp = speed * self.sc
        tot = float(np.linalg.norm(pts[1] - pts[0]))
        for i in range(n):
            d = dot(GOLD, 0.1 * self.sc)
            flow(d, pts, sp, phase=i * tot / sp / n, gate=gate, fade=0.2)
            out.add(d)
        return out

    def nerves(self, cut=False):
        a, b = self.nA, self.nB
        g = VGroup()
        for s, e in (a, b):
            if cut:
                m = (s + e) / 2
                d = (e - s) / np.linalg.norm(e - s)
                g.add(Line(s, m - d * 0.35 * self.sc, color=TEXT, stroke_width=self.sw(5)))
                g.add(Line(m + d * 0.35 * self.sc, e, color=TEXT, stroke_width=self.sw(5)))
            else:
                g.add(Line(s, e, color=TEXT, stroke_width=self.sw(5)))
        return g


def pile_in(scene, dog, k):
    """fade in the first k blocks of the neck dish pile (static)"""
    return dog.pile[:k]


def scissors(center, scale=1.0):
    c = np.array(center, float)
    b1 = Line(c + np.array([-0.05, 0.0, 0]) * scale, c + np.array([0.55, 0.14, 0]) * scale, color=TEXT, stroke_width=7)
    b2 = Line(c + np.array([-0.05, 0.0, 0]) * scale, c + np.array([0.55, -0.14, 0]) * scale, color=TEXT, stroke_width=7)
    h1 = Circle(radius=0.14 * scale, stroke_color=GOLD, stroke_width=5).move_to(c + np.array([-0.3, 0.2, 0]) * scale)
    h2 = Circle(radius=0.14 * scale, stroke_color=GOLD, stroke_width=5).move_to(c + np.array([-0.3, -0.2, 0]) * scale)
    g = VGroup(b1, b2, h1, h2)
    g.b1, g.b2, g.c = b1, b2, c
    return g


# ------------------------------------------------------------------ the duodenal close-up
class Close:
    """Close-up of the duodenal wall: lumen strip on top, wall cells, a RED capillary, and the pancreas.
    Design coordinates: lumen y 1.6..2.9, cells y 0.65, capillary y -1.0 (x -6.4..1.3), pancreas (2.3, -1.0),
    pancreatic duct x 2.3, gallbladder (5.1, -1.0) with its duct x 5.1."""

    def __init__(self, sc=1.0, ox=0.0, oy=0.0):
        self.sc, self.ox, self.oy = sc, ox, oy
        p, S = self.p, self.S
        sw = lambda w: max(2.0, w * max(sc, 0.55))
        self.sw = sw
        self.lumen = Rectangle(width=S(12.8), height=S(1.5), stroke_color=GREY, stroke_width=sw(3), fill_color=GOLD, fill_opacity=0.0).move_to(p(0, 2.3))
        self.cells = VGroup(*[RoundedRectangle(corner_radius=0.2 * sc, width=S(1.9), height=S(1.3), stroke_color=TAN, stroke_width=sw(4),
                                               fill_color=TAN, fill_opacity=0.3).move_to(p(x, 0.45)) for x in (-4.9, -2.7, -0.5)])
        self.cap = RoundedRectangle(corner_radius=0.35 * sc, width=S(7.7), height=S(1.1), stroke_color=RED, stroke_width=sw(6), fill_color=RED,
                                    fill_opacity=0.10).move_to(p(-2.55, -1.3))
        self.gland = Ellipse(width=S(2.2), height=S(2.0), stroke_color=TEXT, stroke_width=sw(5), fill_color=TEXT, fill_opacity=0.08).move_to(p(2.3, -1.3))
        self.duct = Line(p(2.3, -0.3), p(2.3, 1.55), color=GREY, stroke_width=sw(7))
        self.gb = Ellipse(width=S(1.2), height=S(1.9), stroke_color=BLUE, stroke_width=sw(5), fill_color=BLUE, fill_opacity=0.18).move_to(p(5.1, -1.3))
        self.bduct = Line(p(5.1, -0.35), p(5.1, 1.55), color=GREY, stroke_width=sw(7))
        self.ext = VMobject().set_points_as_corners([p(0.9, -1.3), p(0.9, -2.5), p(5.1, -2.5), p(5.1, -2.25)]).set_stroke(RED, sw(6))

    def p(self, x, y):
        return np.array([x * self.sc + self.ox, y * self.sc + self.oy, 0.0])

    def S(self, v):
        return v * self.sc

    def base(self):
        return VGroup(self.lumen, self.cells, self.cap, self.gland, self.duct)

    def cap_path(self):
        return [self.p(-6.2, -1.3), self.p(1.2, -1.3)]

    def hormone_path(self, cx):
        return [self.p(cx, -0.05), self.p(cx, -1.3), self.p(1.2, -1.3)]

    def ext_path(self, cx):
        return [self.p(cx, -0.05), self.p(cx, -1.3), self.p(0.9, -1.3), self.p(0.9, -2.5), self.p(5.1, -2.5), self.p(5.1, -2.2)]

    def reds(self, n=5, speed=0.9):
        g = VGroup()
        pts = self.cap_path()
        tot = float(np.linalg.norm(pts[1] - pts[0]))
        sp = speed * self.sc
        for i in range(n):
            d = dot(RED, 0.12 * self.sc)
            flow(d, pts, sp, phase=i * tot / sp / n, fade=0.4)
            g.add(d)
        return g

    def hormones(self, color, cxs, gate, speed=1.2, ext=False, per=1, r=0.17):
        g = VGroup()
        for j, cx in enumerate(cxs):
            pts = self.ext_path(cx) if ext else self.hormone_path(cx)
            tot = sum(float(np.linalg.norm(pts[i + 1] - pts[i])) for i in range(len(pts) - 1))
            sp = speed * self.sc
            for k in range(per):
                d = dot(color, r * self.sc)
                flow(d, pts, sp, phase=(j * 0.9 + k * tot / sp / per), gate=gate, fade=0.25)
                g.add(d)
        return g

    def juice(self, x, gate, color=BLUE, n=4, speed=1.4, y0=-0.25, y1=1.5):
        g = VGroup()
        pts = [self.p(x, y0), self.p(x, y1)]
        tot = float(np.linalg.norm(pts[1] - pts[0]))
        sp = speed * self.sc
        for i in range(n):
            d = dot(color, 0.14 * self.sc)
            flow(d, pts, sp, phase=i * tot / sp / n, gate=gate, fade=0.2)
            g.add(d)
        return g


def lbl(text, x, y, color=TEXT, size=30, max_w=6.0):
    return L(text, x, y, color, size, max_w)


def qcard2(text="What will the flask collect?"):
    t = T(text, 38, GOLD)
    card = RoundedRectangle(corner_radius=0.2, width=t.width + 0.8, height=t.height + 0.6, stroke_color=GOLD, stroke_width=4, fill_color=BG, fill_opacity=0.95)
    t.move_to(card)
    return VGroup(card, t).move_to([2.7, 2.7, 0])


def qmark(pos, size=56):
    q = T("?", size, GOLD, weight=BOLD).move_to(pos)
    q._t = 0.0

    def up(m, dt):
        m._t += dt
        m.set_opacity(0.7 + 0.3 * np.sin(3.5 * m._t))
    q.add_updater(up)
    return q


def juice_gate(sc, tr):
    return tr


# =========================================================== scenes
class S00Title(TitleCard):
    LESSON = "Digestive Systems and Nutrition"
    TITLE = "How Does the Stomach Know Food Is Coming?"


class S01Hook(SpokenScene):
    def construct(self):
        d, g = gutg()
        self.add(g)
        rp = ripple(XM0 + 0.3, XA1 - 0.3, 1.8)
        self.add(rp)
        self.play(d["stom"].animate.set_fill(GOLD, 0.30), run_time=1.0)
        self.at("meal")
        bowl = Arc(radius=0.75, start_angle=PI, angle=PI, stroke_color=TEXT, stroke_width=6, fill_color=TEXT, fill_opacity=0.18).move_to([-5.7, 2.75, 0])
        meat = VGroup(*[food_block() for _ in range(3)])
        for i, m in enumerate(meat):
            setsz(m, 0.5)
            m.move_to([-6.0 + 0.3 * i, 2.85 + 0.12 * (i % 2), 0])
        ab = Arrow([-5.7, 2.0, 0], [-5.7, 0.85, 0], buff=0, color=TEXT, stroke_width=7, tip_length=0.3)
        self.play(FadeIn(bowl, shift=DOWN * 0.3), FadeIn(meat, shift=DOWN * 0.3), run_time=0.9)
        self.play(GrowArrow(ab), run_time=0.7)
        self.at("Can it start")
        c, hand = clock([-3.9, 3.0, 0], 0.6, 1.4)
        lb = lbl("ready yet?", -1.5, 3.0, GOLD, 40, 3.2)
        self.play(FadeIn(c, scale=0.6), run_time=0.6)
        self.play(FadeIn(lb, shift=RIGHT * 0.3), run_time=0.5)
        self.at("before any food")
        self.play(d["stom"].animate.set_fill(GOLD, 0.40), run_time=1.0)
        self.finish()


class S02Link(SpokenScene):
    def construct(self):
        d, g = gutg()
        self.add(g)
        rp = ripple(XM0 + 0.3, XA1 - 0.3, 1.8)
        self.add(rp)
        self.at("one way")
        arrow = Arrow([-5.4, 2.9, 0], [5.4, 2.9, 0], buff=0, color=TEXT, stroke_width=8, tip_length=0.4)
        lw = lbl("one way", 0, 3.5, TEXT, 34, 3)
        self.play(GrowArrow(arrow), FadeIn(lw), run_time=1.2)
        self.at("several stretches")
        foods = [_f1.food_runner(ph, 0.95) for ph in (0.0, 2.4, 4.8)]
        for b in foods:
            self.add(b)
        lm = lbl("mouth", -5.7, -1.2, TEXT, 30, 2)
        ls = lbl("stomach", -4.15, -2.5, GOLD, 30, 2)
        ld = brk(XS1, -1.2, -1.75, TAN, "duodenum", -2.3, 30, tx=-1.7)
        lsi = brk(XS1, XI1, -3.0, TAN, "small intestine", -3.45, 30)
        self.play(FadeIn(lm), run_time=0.4)
        self.play(FadeIn(ls), run_time=0.4)
        self.play(Create(ld[0]), FadeIn(ld[1]), run_time=0.5)
        self.play(Create(lsi[0]), FadeIn(lsi[1]), run_time=0.5)
        self.at("Some signals")
        self.play(*[FadeOut(b) for b in foods], FadeOut(arrow), FadeOut(lw), run_time=0.6)
        self.at("ready a stretch")
        self.play(d["stom"].animate.set_fill(GOLD, 0.5), run_time=0.6)
        self.at("before")
        lb = lbl("before", -4.15, 2.6, GOLD, 34, 2.4)
        self.play(FadeIn(lb, shift=DOWN * 0.2), run_time=0.5)
        self.at("food arrives")
        b = food_block()
        setsz(b, 0.85)
        runner(b, [[XM0 + 0.2, 0, 0], [XA1 + 0.2, 0, 0]], 1.5, 0, fn=lambda m, p: setsz(m, food_size(p[0])), loop=False)
        self.add(b)
        self.at("Others")
        self.play(FadeOut(lb), d["stom"].animate.set_fill(GOLD, 0.16), d["si"].animate.set_fill(TAN, 0.55), run_time=0.6)
        self.at("once it is there")
        la = lbl("on arrival", -1.7, 1.95, TEXT, 34, 3)
        self.play(FadeIn(la, shift=DOWN * 0.2), run_time=0.5)
        self.finish()


def dog_scene_base(scene, cut=False, bowl=True, dish=False, pile=False, flow_n=4, sc=1.0, gate=None):
    dog = Dog(sc, 0.35, 0.0)
    w = dog.world(cut=cut, bowl=bowl, dish=dish, pile=pile)
    scene.add(w)
    return dog, w


class S03Pavlov(SpokenScene):
    def construct(self):
        dog = Dog(1.0, 0.35, 0.0)
        cap = T("Ivan Pavlov's laboratory, St Petersburg", 36, TEXT)
        fit(cap, max_w=12.2)
        cap.move_to([0, 3.35, 0])
        self.play(FadeIn(cap, shift=DOWN * 0.2), run_time=0.8)
        self.play(FadeIn(dog.world(), shift=UP * 0.2), run_time=1.2)
        self.add(dog.shell)
        self.add(dog.food_flow(False, 4, 1.4))
        self.at("The dogs")
        self.wait(0.3)
        self.at("awake")
        self.play(dog.body.animate.set_stroke(GOLD, 6), run_time=0.5)
        self.play(dog.body.animate.set_stroke(TEXT, 3), run_time=0.5)
        self.at("one gland")
        lb = lbl("one gland at a time", 2.9, 2.2, GOLD, 34, 5)
        ar = Arrow([2.0, 1.85, 0], dog.p(0.6, -0.1), buff=0.1, color=GOLD, stroke_width=6, tip_length=0.28)
        self.play(FadeIn(lb), GrowArrow(ar), dog.stomach.animate.set_fill(GOLD, 0.45), run_time=0.8)
        self.at("whole")
        self.play(dog.body.animate.set_stroke(GOLD, 6), run_time=0.5)
        self.play(dog.body.animate.set_stroke(TEXT, 3), run_time=0.5)
        self.finish()


class S04Neck(SpokenScene):
    def construct(self):
        dog = Dog(1.0, 0.35, 0.0)
        gA = ValueTracker(1.0)
        gB = ValueTracker(0.0)
        self.add(dog.world(cut=False))
        fa = dog.food_flow(False, 4, 1.4, gate=gA)
        fb = dog.food_flow(True, 4, 1.4, gate=gB)
        self.add(fa, fb)
        self.at("opened at")
        cutmark = Line(dog.p(-2.25, 0.1), dog.p(-2.25, -0.6), color=GOLD, stroke_width=6)
        lb = lbl("neck opening", -2.2, 1.9, GOLD, 34, 4)
        la = Arrow([-2.2, 1.55, 0], dog.p(-2.25, -0.1), buff=0.05, color=GOLD, stroke_width=5, tip_length=0.25)
        self.play(FadeOut(dog.bridge), run_time=0.4)
        self.play(FadeIn(lb), GrowArrow(la), Create(cutmark), gA.animate.set_value(0.0), gB.animate.set_value(1.0), run_time=0.8)
        self.at("Food the dog")
        self.play(FadeIn(dog.dish, shift=DOWN * 0.2), run_time=0.7)
        self.at("fell out")
        self.wait(0.9)
        self.play(FadeIn(dog.pile[0]), FadeIn(dog.pile[1]), run_time=0.5)
        self.wait(0.7)
        self.play(FadeIn(dog.pile[2]), run_time=0.4)
        self.at("It never")
        self.play(FadeOut(lb), FadeOut(la), FadeOut(cutmark), dog.stomach.animate.set_fill(GOLD, 0.16), run_time=0.5)
        ls = lbl("stomach stays empty", 1.9, 1.9, GOLD, 34, 5.5)
        ar = Arrow([1.3, 1.55, 0], dog.p(0.5, 0.1), buff=0.1, color=GOLD, stroke_width=6, tip_length=0.28)
        self.play(FadeIn(ls), GrowArrow(ar), run_time=0.6)
        self.finish()


def neckdog(scene, level=None, with_flask=False, flow_n=4):
    dog = Dog(1.0, 0.35, 0.0)
    scene.add(dog.world(cut=True, dish=True, pile=False))
    pile = VGroup(*dog.pile[:3])
    scene.add(pile)
    scene.add(dog.food_flow(True, flow_n, 1.4))
    return dog


class S05Fistula(SpokenScene):
    def construct(self):
        dog = neckdog(self)
        lvl = ValueTracker(0.0)
        fis = dog.fistula(lvl)
        self.at("fistula")
        self.play(Create(fis.tube), run_time=0.8)
        self.play(FadeIn(VGroup(*fis[1:]), shift=DOWN * 0.2), run_time=0.8)
        lb = lbl("gastric fistula", -1.6, -3.3, TEXT, 30, 3.2)
        self.play(FadeIn(lb), run_time=0.5)
        self.at("juice")
        self.play(dog.stomach.animate.set_fill(GOLD, 0.35), run_time=0.6)
        self.at("flask")
        self.play(fis.flask.animate.set_stroke(GOLD, 8), run_time=0.5)
        self.play(fis.flask.animate.set_stroke(TEXT, 5), run_time=0.4)
        self.finish()


class S06Predict(SpokenScene):
    def construct(self):
        dog = neckdog(self)
        lvl = ValueTracker(0.0)
        fis = dog.fistula(lvl)
        self.add(fis)
        self.add(dog.pile[3], dog.pile[4])
        lb = lbl("gastric fistula", -1.6, -3.3, TEXT, 30, 3.2)
        self.add(lb)
        self.at("Suppose")
        self.play(dog.stomach.animate.set_fill(GOLD, 0.16), run_time=0.5)
        self.at("touches the stomach")
        # food keeps falling into the dish; the flask waits
        self.wait(0.2)
        self.at("What should")
        q = qcard2()
        qm = qmark(dog.p(0.4, -3.0), 56)
        self.play(FadeIn(q, shift=DOWN * 0.2), FadeIn(qm), run_time=0.8)
        self.finish()


class S07Pause(NarratedScene):
    def construct(self):
        dog = neckdog(self)
        self.add(dog.pile[3], dog.pile[4])
        lvl = ValueTracker(0.0)
        fis = dog.fistula(lvl)
        self.add(fis)
        self.add(lbl("gastric fistula", -1.6, -3.3, TEXT, 30, 3.2))
        self.add(qcard2())
        self.add(qmark(dog.p(0.4, -3.0), 56))
        tr = ValueTracker(0)
        ring = Circle(radius=0.4, color=GREY, stroke_width=5).move_to([-1.7, 2.7, 0])
        arc = always_redraw(lambda: Arc(radius=0.4, start_angle=PI / 2, angle=-TAU * max(tr.get_value(), 0.001), color=GOLD, stroke_width=8).move_to(ring))
        self.add(ring, arc)
        self.play(tr.animate.set_value(1.0), run_time=4.8, rate_func=linear)
        self.finish()


class S08Reveal(SpokenScene):
    def construct(self):
        dog = neckdog(self)
        self.add(dog.pile[3], dog.pile[4])
        lvl = ValueTracker(0.0)
        gate = ValueTracker(0.0)
        fis = dog.fistula(lvl)
        self.add(fis)
        self.add(lbl("gastric fistula", -1.6, -3.3, TEXT, 30, 3.2))
        self.add(dog.drips(gate, 4, 1.1))
        c, hand = clock([5.5, -1.3, 0], 0.65, 4.0)
        lm = lbl("some minutes", 5.4, -2.5, TEXT, 30, 3.2)
        self.at("After")
        self.play(FadeIn(c, scale=0.6), FadeIn(lm), run_time=0.7)
        self.wait(self.t_of("acid juice") - 0.3 - self.elapsed())
        hand._rate = 0.4
        self.play(gate.animate.set_value(1.0), dog.stomach.animate.set_fill(GOLD, 0.40), run_time=0.5)
        lvl.add_updater(lambda m, dt: m.set_value(min(0.8, m.get_value() + dt * 0.09)))
        self.add(lvl)
        self.at("It came")
        fis.tube.set_stroke(GOLD, 11)
        self.at("fistula")
        self.play(FadeOut(c), FadeOut(lm), run_time=0.5)
        self.at("The dog was eating")
        ln = lbl("no food in the stomach", 1.7, 1.9, GOLD, 34, 5.5)
        ar = Arrow([1.0, 1.55, 0], dog.p(0.5, 0.1), buff=0.1, color=GOLD, stroke_width=6, tip_length=0.28)
        self.play(FadeIn(ln), GrowArrow(ar), run_time=0.6)
        self.finish()


class S09Vagus(SpokenScene):
    def construct(self):
        dog = neckdog(self)
        self.add(dog.pile[3], dog.pile[4])
        lvl = ValueTracker(0.0)
        fis = dog.fistula(lvl)
        self.add(fis)
        nv = dog.nerves(cut=False)
        full = VGroup(*[Line(s, e, color=TEXT, stroke_width=5) for s, e in (dog.nA, dog.nB)])
        self.at("Then both")
        self.play(FadeIn(dog.brain), Create(full), run_time=1.0)
        lv = lbl("vagus nerves", -0.9, 1.65, TEXT, 34, 4)
        self.play(FadeIn(lv), run_time=0.4)
        sc = scissors(dog.p(-1.8, 0.9), 1.6)
        self.at("were cut")
        # scissors travel to line A, snip, then to B, snip
        mA = (dog.nA[0] + dog.nA[1]) / 2
        mB = (dog.nB[0] + dog.nB[1]) / 2
        self.add(sc)
        self.play(sc.animate.move_to(mA + RIGHT * 0.3), run_time=0.5)
        cutA = nv[:2]
        self.remove(full)
        self.add(nv)
        self.play(sc.b1.animate.rotate(0.35, about_point=sc.c + (mA + RIGHT * 0.3 - sc.c)), run_time=0.25)
        self.play(sc.animate.move_to(mB + RIGHT * 0.3), run_time=0.5)
        self.wait(0.4)
        self.at("These nerves")
        self.play(FadeOut(sc), run_time=0.4)
        lb = lbl("brainstem", -4.9, 2.3, TEXT, 34, 3)
        la = Arrow([-4.2, 2.1, 0], dog.p(-3.0, 1.0), buff=0.08, color=TEXT, stroke_width=5, tip_length=0.25)
        self.at("brainstem")
        self.play(FadeIn(lb), GrowArrow(la), dog.brain.animate.set_fill(TEXT, 0.7), run_time=0.7)
        self.at("to the stomach")
        self.play(dog.stomach.animate.set_fill(GOLD, 0.4), run_time=0.6)
        self.at("Now the dog")
        self.play(FadeOut(lb), FadeOut(la), dog.stomach.animate.set_fill(GOLD, 0.16), run_time=0.4)
        self.add(dog.food_flow(True, 4, 1.4))
        self.at("stayed empty")
        le = lbl("stays empty", 2.7, -3.3, TEXT, 34, 3)
        self.play(FadeIn(le), run_time=0.5)
        self.finish()


class S10Cephalic(SpokenScene):
    def construct(self):
        dog = neckdog(self)
        self.add(dog.pile[3], dog.pile[4])
        lvl = ValueTracker(0.0)
        gate = ValueTracker(0.0)
        fis = dog.fistula(lvl)
        self.add(fis)
        self.add(dog.brain)
        nerves = dog.nerves(cut=False)
        self.add(nerves)
        # pulses ride the nerves from brainstem to stomach
        pg = ValueTracker(0.0)
        pulses = VGroup()
        for k, (s, e) in enumerate((dog.nA, dog.nB)):
            for j in range(3):
                d = dot(TEXT, 0.1)
                flow(d, [s, e], 1.1, phase=j * 1.0 + k * 0.5, gate=pg, fade=0.15)
                pulses.add(d)
        self.add(pulses)
        self.add(dog.drips(gate, 4, 1.1))
        self.at("So when the dog")
        self.play(pg.animate.set_value(1.0), nerves.animate.set_stroke(GOLD, 8), run_time=0.8)
        self.at("start the stomach")
        self.play(gate.animate.set_value(1.0), dog.stomach.animate.set_fill(GOLD, 0.40), run_time=0.6)
        lvl.add_updater(lambda m, dt: m.set_value(min(0.8, m.get_value() + dt * 0.1)))
        self.add(lvl)
        self.at("This is the cephalic")
        t1 = T("cephalic phase", 42, GOLD, weight=BOLD)
        t2 = T("(in the dog: needs the vagus)", 28, TEXT)
        fit(t2, max_w=5.8)
        lab = VGroup(t1, t2).arrange(DOWN, buff=0.15).move_to([3.7, 2.35, 0])
        self.play(FadeIn(lab, shift=DOWN * 0.2), run_time=0.7)
        chips = []
        names = [("sight", -5.7), ("smell", -3.9), ("taste", -2.2), ("chewing", -0.4)]
        for name, x in names:
            self.at(name)
            c = chip(name, TEXT, 30, 0.2, 0.12).move_to([x, 3.3, 0])
            ar = Arrow(c.get_bottom(), dog.p(-3.2, 0.8) if name != "chewing" else dog.p(-3.9, 0.45), buff=0.12, color=TEXT, stroke_width=3, tip_length=0.18)
            self.play(FadeIn(c, shift=DOWN * 0.2), Create(ar), run_time=0.5)
            chips.append((c, ar))
        self.finish()


class S11Limit(SpokenScene):
    def construct(self):
        d, g = gutg()
        self.add(g)
        rp = ripple(XM0 + 0.3, XA1 - 0.3, 1.8)
        self.add(rp)
        self.at("This rules in")
        tk = T("✓", 50, GOLD, weight=BOLD)
        ta = VGroup(T("ruled in:", 32, GOLD, weight=BOLD), T("nerves start the stomach", 32, TEXT)).arrange(DOWN, buff=0.1)
        A = VGroup(tk, ta).arrange(RIGHT, buff=0.3).move_to([-3.0, 3.0, 0])
        self.play(FadeIn(A, shift=DOWN * 0.2), d["stom"].animate.set_fill(GOLD, 0.45), run_time=0.8)
        self.at("It does not")
        box = Square(0.45, stroke_color=TEXT, stroke_width=5)
        tb = VGroup(T("not ruled out:", 32, TEXT, weight=BOLD), T("later steps", 32, TEXT)).arrange(DOWN, buff=0.1)
        B = VGroup(box, tb).arrange(RIGHT, buff=0.3).move_to([3.4, 3.0, 0])
        self.play(FadeIn(B, shift=DOWN * 0.2), run_time=0.8)
        self.at("once food is")
        foods = [_f1.food_runner(ph, 1.1) for ph in (0.0, 3.0)]
        for b in foods:
            self.add(b)
        self.play(d["si"].animate.set_fill(TAN, 0.5), run_time=0.8)
        self.finish()


class S12Duodenum(SpokenScene):
    def construct(self):
        d, g = gutg()
        self.add(g)
        d["stom"].set_fill(GOLD, 0.40)
        self.add(ripple(XM0 + 0.3, XA1 - 0.3, 1.8))
        # chyme: gold and grey grains swirling in the stomach
        cen = np.array([-4.15, 0.0, 0])
        tr = ValueTracker(0.0)   # 0 = in the stomach, 1 = in the duodenum
        mass = VGroup()
        rs = np.random.RandomState(7)
        offs = [np.array([rs.uniform(-0.45, 0.45), rs.uniform(-0.6, 0.6), 0]) for _ in range(10)]
        for i, off in enumerate(offs):
            m = dot(GOLD if i % 2 == 0 else FOOD, 0.12)
            m._tt = i * 0.7

            def upd(mm, dt, off=off):
                mm._tt += dt
                k = tr.get_value()
                c = np.array([-4.15 + k * 2.2, 0.0, 0])
                sq = 1.0 - 0.45 * np.sin(np.pi * min(max(k, 0), 1))  # squeeze through the exit
                mm.move_to(c + np.array([off[0] * (1 - 0.5 * k) + 0.18 * np.sin(1.7 * mm._tt), off[1] * sq + 0.15 * np.cos(2.1 * mm._tt), 0]))
            m.add_updater(upd)
            upd(m, 0)
            mass.add(m)
        for i in range(3):
            pass
        self.at("two later steps")
        self.add(mass)
        self.at("Chyme")
        lc = lbl("chyme", -4.15, 2.6, GOLD, 36, 2.6)
        lc.add_updater(lambda m: m.move_to([-4.15 + tr.get_value() * 2.2, 2.6, 0]))
        self.play(FadeIn(lc, shift=DOWN * 0.2), run_time=0.6)
        self.at("of food")
        self.play(tr.animate.set_value(1.0), d["stom"].animate.set_fill(GOLD, 0.16), run_time=1.9, rate_func=smooth)
        self.at("duodenum")
        ld = brk(XS1, -1.2, -1.75, TAN, "duodenum", -2.3, 32, tx=-1.7)
        self.play(Create(ld[0]), FadeIn(ld[1]), d["si"].animate.set_fill(TAN, 0.5), run_time=0.7)
        self.at("small intestine")
        lsi = brk(XS1, XI1, -3.0, TAN, "small intestine", -3.45, 30)
        self.play(Create(lsi[0]), FadeIn(lsi[1]), run_time=0.7)
        self.finish()


def close_setup(scene, sc=1.0, ox=0.0, oy=0.0, lumen=True):
    cl = Close(sc, ox, oy)
    scene.add(cl.base())
    return cl


class S13Hormone(SpokenScene):
    def construct(self):
        cl = Close()
        self.play(FadeIn(cl.lumen), Create(cl.cells), run_time=0.8)
        self.play(Create(cl.cap), Create(cl.gland), Create(cl.duct), run_time=1.2)
        self.add(cl.reds(5, 0.9))
        self.at("A hormone is")
        lb = lbl("hormone: released into blood, acts at a distance", 0, -3.4, PURPLE, 32, 12.2)
        self.play(FadeIn(lb, shift=UP * 0.2), run_time=0.7)
        pd = dot(PURPLE, 0.22).move_to(cl.p(-2.7, -0.05))
        self.add(pd)
        self.play(pd.animate.scale(1.5), run_time=0.4)
        self.play(pd.animate.scale(1 / 1.5), run_time=0.3)
        self.at("released")
        self.play(pd.animate.move_to(cl.p(-2.7, -1.3)), run_time=1.0)
        self.remove(pd)
        run = dot(PURPLE, 0.22)
        runner(run, [cl.p(-2.7, -1.3), cl.p(1.15, -1.3)], 1.4, 0, loop=False)
        self.add(run)
        self.at("acts on distant")
        self.wait(2.6)
        self.play(cl.gland.animate.set_fill(PURPLE, 0.35), cl.gland.animate.set_stroke(PURPLE, 7), run_time=0.6)
        self.remove(run)
        self.at("The blood carries")
        gate = ValueTracker(1.0)
        self.add(cl.hormones(PURPLE, [-4.9, -2.7, -0.5], gate, speed=1.3, per=1))
        self.at("next gland")
        lg = lbl("gland", 2.3, -2.8, TEXT, 34, 2)
        self.play(FadeIn(lg), run_time=0.5)
        self.finish()


class S14Secretin(SpokenScene):
    def construct(self):
        cl = Close()
        self.add(cl.base())
        self.add(cl.reds(5, 0.9))
        self.at("Acid")
        lg = ValueTracker(0.0)
        acid = VGroup()
        for i in range(7):
            a = dot(GOLD, 0.15)
            flow(a, [[-6.2, 2.25 + 0.4 * np.sin(i * 1.9), 0], [3.4, 2.25 + 0.4 * np.sin(i * 1.9), 0]], 1.1, phase=i * 1.2, gate=lg, fade=0.3)
            acid.add(a)
        self.add(acid)
        lac = lbl("acid", -5.0, 3.42, GOLD, 34, 2)
        self.play(FadeIn(lac), cl.lumen.animate.set_fill(GOLD, 0.2), lg.animate.set_value(1.0), run_time=1.2)
        self.at("duodenal")
        self.play(cl.cells.animate.set_stroke(TEXT, 6), run_time=0.5)
        self.at("release a hormone")
        gate = ValueTracker(0.0)
        hs = cl.hormones(PURPLE, [-4.9, -2.7, -0.5], gate, speed=1.2)
        self.add(hs)
        self.play(gate.animate.set_value(1.0), run_time=0.5)
        self.at("secretin")
        ls = lbl("secretin", -3.0, -2.5, PURPLE, 34, 3)
        self.play(FadeIn(ls), run_time=0.5)
        self.at("pancreas")
        lp = lbl("pancreas", 1.2, -3.0, TEXT, 30, 2.4)
        self.play(FadeIn(lp), cl.gland.animate.set_fill(PURPLE, 0.30), cl.gland.animate.set_stroke(PURPLE, 7), run_time=0.6)
        self.at("fluid")
        jg = ValueTracker(0.0)
        jf = cl.juice(2.3, jg, BLUE, 5, 1.4)
        self.add(jf)
        self.play(jg.animate.set_value(1.0), run_time=0.5)
        self.at("bicarbonate")
        lb = lbl("bicarbonate", 4.0, 0.6, BLUE, 30, 3.0)
        self.play(FadeIn(lb), run_time=0.5)
        self.at("neutralizes")
        self.play(cl.lumen.animate.set_fill(GOLD, 0.0), lg.animate.set_value(0.0), FadeOut(lac), run_time=1.5)
        self.finish()


class S15Cck(SpokenScene):
    def construct(self):
        cl = Close()
        self.add(cl.base())
        self.add(cl.reds(5, 0.9))
        self.add(lbl("pancreas", 1.2, -3.0, TEXT, 30, 2.4))
        self.at("Fat")
        gg = ValueTracker(0.0)
        grains = VGroup()
        for i in range(4):
            f = dot(ORANGE, 0.17)
            flow(f, [[-6.2, 2.0 + 0.35 * (i % 2), 0], [3.4, 2.0 + 0.35 * (i % 2), 0]], 1.0, phase=i * 2.4, gate=gg, fade=0.3)
            grains.add(f)
        for i in range(4):
            f = dot(FOOD, 0.17)
            flow(f, [[-6.2, 2.7 - 0.35 * (i % 2), 0], [3.4, 2.7 - 0.35 * (i % 2), 0]], 1.0, phase=i * 2.4 + 1.2, gate=gg, fade=0.3)
            grains.add(f)
        self.add(grains)
        lf = lbl("fat", -5.2, 3.42, ORANGE, 34, 1.5)
        self.play(FadeIn(lf), gg.animate.set_value(1.0), run_time=0.8)
        self.at("protein")
        lpr = lbl("protein", -3.5, 3.42, TEXT, 34, 2.2)
        self.play(FadeIn(lpr), run_time=0.5)
        self.at("release")
        self.play(cl.cells.animate.set_stroke(TEXT, 6), run_time=0.4)
        gate = ValueTracker(0.0)
        hs = cl.hormones(PURPLE, [-4.9, -2.7, -0.5], gate, speed=1.2)
        self.add(hs)
        self.play(gate.animate.set_value(1.0), run_time=0.5)
        self.at("CCK")
        lc = lbl("CCK", -3.0, -2.5, PURPLE, 36, 2)
        self.play(FadeIn(lc), run_time=0.5)
        self.at("pancreas sends")
        jg = ValueTracker(0.0)
        self.add(cl.juice(2.3, jg, BLUE, 5, 1.4))
        self.play(cl.gland.animate.set_fill(PURPLE, 0.30), cl.gland.animate.set_stroke(PURPLE, 7), jg.animate.set_value(1.0), run_time=0.6)
        self.at("enzymes")
        le = lbl("enzymes", 3.8, 0.6, BLUE, 30, 2.2)
        self.play(FadeIn(le), run_time=0.5)
        self.at("and the gallbladder")
        self.play(Create(cl.ext), FadeIn(cl.gb), Create(cl.bduct), run_time=1.0)
        lgb = lbl("gallbladder", 4.6, -3.0, TEXT, 30, 3.0)
        self.play(FadeIn(lgb), run_time=0.4)
        cck = VGroup()
        eg = ValueTracker(1.0)
        cck = cl.hormones(PURPLE, [-0.5], eg, speed=2.2, ext=True, per=2)
        self.add(cck)
        self.at("squeezes")
        bg = ValueTracker(0.0)
        self.add(cl.juice(5.1, bg, BLUE, 4, 1.4, -0.35, 1.5))
        self.play(cl.gb.animate.stretch(0.6, 1), cl.gb.animate.set_fill(BLUE, 0.5), bg.animate.set_value(1.0), run_time=0.6)
        self.at("bile")
        lbi = lbl("bile", 6.0, 0.6, BLUE, 30, 1.2)
        self.play(FadeIn(lbi), run_time=0.4)
        self.finish()


class S16Idea(SpokenScene):
    def construct(self):
        dog = Dog(1.0, 0.35, 0.0)
        part1 = VGroup(dog.world(cut=True, dish=True), dog.pile[:3], dog.brain)
        lvl = ValueTracker(0.0)
        fis = dog.fistula(lvl)
        nerves = dog.nerves(cut=False)
        pg = ValueTracker(1.0)
        pulses = VGroup()
        for k, (s_, e_) in enumerate((dog.nA, dog.nB)):
            for j in range(3):
                d = dot(TEXT, 0.1)
                flow(d, [s_, e_], 1.1, phase=j * 1.0 + k * 0.5, gate=pg, fade=0.15)
                pulses.add(d)
        gate = ValueTracker(0.0)
        drips = dog.drips(gate, 4, 1.1)
        part1.add(fis, nerves, pulses, drips)
        self.add(part1)
        self.at("So nerves")
        h1 = lbl("nerves start the stomach early", 2.9, 2.5, TEXT, 36, 6.4)
        self.play(FadeIn(h1), nerves.animate.set_stroke(GOLD, 8), run_time=0.8)
        self.at("start the stomach")
        lvl.add_updater(lambda m, dt: m.set_value(min(0.8, m.get_value() + dt * 0.25)))
        self.add(lvl)
        self.play(gate.animate.set_value(1.0), dog.stomach.animate.set_fill(GOLD, 0.4), run_time=0.6)
        self.at("And a stretch")
        self.play(FadeOut(part1), FadeOut(h1), run_time=0.8)
        self.remove(part1)
        cl = Close()
        self.add(cl.base(), cl.gb, cl.bduct, cl.ext)
        self.add(cl.reds(5, 0.9))
        h_g = ValueTracker(0.0)
        hs = cl.hormones(PURPLE, [-4.9, -2.7, -0.5], h_g, speed=1.2, per=1)
        hx = cl.hormones(PURPLE, [-2.7], h_g, speed=1.8, ext=True, per=2)
        self.add(hs, hx)
        self.play(FadeIn(VGroup(cl.base())), run_time=0.5)
        h2 = lbl("food reaches a stretch", 0, 3.42, TEXT, 34, 7)
        self.play(FadeIn(h2), run_time=0.5)
        self.at("signals the glands")
        self.play(h_g.animate.set_value(1.0), cl.gland.animate.set_fill(PURPLE, 0.3), cl.gb.animate.set_fill(BLUE, 0.4), run_time=0.8)
        self.at("acid")
        self.play(FadeOut(h2), run_time=0.3)
        ta = lbl("acid", -5.2, 3.42, GOLD, 34, 1.6)
        self.play(FadeIn(ta), cl.lumen.animate.set_fill(GOLD, 0.2), run_time=0.5)
        self.at("fat")
        tf = lbl("fat", -3.6, 3.42, ORANGE, 34, 1.4)
        self.play(FadeIn(tf), run_time=0.4)
        self.at("protein")
        tp = lbl("protein", -2.0, 3.42, TEXT, 34, 2.0)
        self.play(FadeIn(tp), run_time=0.4)
        self.at("the right glands")
        jg = ValueTracker(0.0)
        self.add(cl.juice(2.3, jg, BLUE, 4, 1.4), cl.juice(5.1, jg, BLUE, 4, 1.4, -0.35, 1.5))
        self.play(cl.gland.animate.set_stroke(PURPLE, 7), cl.gb.animate.set_stroke(PURPLE, 7), jg.animate.set_value(1.0), run_time=0.8)
        self.finish()


class S17End(EndCard):
    LINE = "Nerves ready the stomach early; hormones answer food as it arrives."
