"""Where the Marsh Grass Goes: chapter 2 of Energy Flow and Productivity (Biochemistrypedia explainer).

Same world and colour map as chapter 1 (../scenes.py): producers bottom-left, herbivores above them,
the detritus box lower right, the BROWN door between producer and detritus boxes.
COLOUR MAP: GREEN producers / production; PURPLE production passed up; BROWN door and detritus;
GREY (HEAT) respiration leaving as heat; YELLOW sunlight and highlights.
Boxes, pipes and cartoons are schematic.
"""
import numpy as np
from bp_style import *  # noqa: F401,F403

_T, _M = T, M


def T(text, size=30, *a, **k):
    return _T(text, round(size * 1.25), *a, **k)


def M(text, size=30, *a, **k):
    return _M(text, round(size * 1.25), *a, **k)


PURPLE = "#B58CD9"
BROWN = "#B9825A"
HEAT = "#B4BBC8"
PALE = "#DDE3EA"
MUD = "#7A6A5A"

PROD_C = np.array([-4.1, -2.6, 0.0])
HERB_C = np.array([-4.1, 0.3, 0.0])
PRED_C = np.array([-4.1, 2.9, 0.0])
SOIL_C = np.array([3.4, -2.95, 0.0])
BW = 4.8
V = lambda x, y, z=0.0: np.array([x, y, 0.0])


def rbox(w, h, color, pos, op=0.15, sw=3.5):
    return RoundedRectangle(corner_radius=0.16, width=w, height=h, stroke_color=color, stroke_width=sw,
                            fill_color=color, fill_opacity=op).move_to(pos)


def grass(c, s=1.0, color=GREEN):
    g = VGroup(*[Line(ORIGIN, [dx * 0.18 * s, 0.5 * s, 0]).set_stroke(color, 4) for dx in (-2, -1, 0, 1, 2)])
    return g.move_to(c)


def hopper(c, s=1.0):
    body = Ellipse(width=0.9 * s, height=0.42 * s, color=PALE, stroke_width=3).move_to(c)
    head = Circle(radius=0.15 * s, color=PALE, stroke_width=3).move_to(c + np.array([0.52 * s, 0.1 * s, 0]))
    legs = VGroup(*[Line(c + np.array([x * s, -0.1 * s, 0]), c + np.array([(x - 0.15) * s, -0.4 * s, 0]), color=PALE, stroke_width=3)
                    for x in (-0.25, 0.0, 0.25)])
    return VGroup(body, head, legs)


def spider(c, s=1.0):
    b = Circle(radius=0.2 * s, color=PALE, stroke_width=3).move_to(c)
    h = Circle(radius=0.11 * s, color=PALE, stroke_width=3).move_to(c + np.array([0.28 * s, 0, 0]))
    legs = VGroup()
    for sg in (-1, 1):
        for j in range(4):
            y = (j - 1.5) * 0.12 * s
            legs.add(Line(c + np.array([0, y, 0]), c + np.array([sg * 0.45 * s, y + (j - 1.5) * 0.12 * s, 0]), color=PALE, stroke_width=2.5))
    return VGroup(b, h, legs)


def crab(c, s=1.0):
    body = Ellipse(width=0.7 * s, height=0.4 * s, color=PALE, stroke_width=3).move_to(c)
    cl = VGroup(Circle(radius=0.12 * s, color=PALE, stroke_width=3).move_to(c + V(-0.5 * s, 0.3 * s)),
                Circle(radius=0.12 * s, color=PALE, stroke_width=3).move_to(c + V(0.5 * s, 0.3 * s)))
    legs = VGroup(*[Line(c + V(sg * 0.3 * s, -0.1 * s), c + V(sg * (0.5 + 0.05 * k) * s, (-0.3 - 0.04 * k) * s), color=PALE, stroke_width=2.5)
                    for sg in (-1, 1) for k in range(3)])
    return VGroup(body, cl, legs)


def snail(c, s=1.0):
    shell = Circle(radius=0.24 * s, color=PALE, stroke_width=3).move_to(c + V(-0.1 * s, 0.15 * s))
    spiral = Arc(radius=0.12 * s, start_angle=0, angle=PI * 1.5, color=PALE, stroke_width=2.5).move_to(shell)
    foot = Line(c + V(-0.45 * s, -0.12 * s), c + V(0.4 * s, -0.12 * s), color=PALE, stroke_width=4)
    head = Line(c + V(0.4 * s, -0.12 * s), c + V(0.5 * s, 0.1 * s), color=PALE, stroke_width=3)
    return VGroup(shell, spiral, foot, head)


def bacterium(c, s=1.0, ang=0.0):
    return RoundedRectangle(corner_radius=0.1 * s, width=0.4 * s, height=0.2 * s, color=TEAL, stroke_width=3).rotate(ang).move_to(c)


def co2(size=30, color=TEXT):
    a = T("CO", size, color)
    b = T("2", int(size * 0.65), color).next_to(a, RIGHT, buff=0.02).shift(DOWN * 0.08)
    return VGroup(a, b)


def door(pos, color, w=0.46, h=1.05):
    r = Rectangle(width=w, height=h, stroke_color=color, stroke_width=4, fill_color=color, fill_opacity=0.45).move_to(pos)
    k = Dot(radius=0.05, color=TEXT).move_to(pos + np.array([w * 0.2, 0, 0]))
    return VGroup(r, k)


def stream(a, b, color, n=7, speed=0.3, r=0.09, wave=0.0):
    """A looping stream of dots from a to b (a rate, drawn as motion)."""
    a = np.array(a, float)
    b = np.array(b, float)
    g = VGroup(*[Dot(radius=r, color=color) for _ in range(n)])
    g.t = 0.0
    d = b - a
    perp = np.array([-d[1], d[0], 0.0])
    perp = perp / (np.linalg.norm(perp) + 1e-9)

    def upd(m, dt):
        m.t += dt
        for i, dot in enumerate(m):
            ph = (i / n + m.t * speed) % 1
            dot.move_to(a + d * ph + perp * wave * np.sin(ph * 9 + i))
            dot.set_opacity(float(min(1, ph * 6, (1 - ph) * 6)))
    g.add_updater(upd)
    upd(g, 0)
    return g


def pstream(pts, color, n=6, speed=0.25, r=0.09):
    """A looping stream of dots along a polyline."""
    pts = [np.array(p, float) for p in pts]
    seg = [float(np.linalg.norm(pts[i + 1] - pts[i])) for i in range(len(pts) - 1)]
    tot = sum(seg)
    g = VGroup(*[Dot(radius=r, color=color) for _ in range(n)])
    g.t = 0.0

    def pos(s):
        for i, l in enumerate(seg):
            if s <= l:
                return pts[i] + (pts[i + 1] - pts[i]) * (s / l if l else 0)
            s -= l
        return pts[-1]

    def upd(m, dt):
        m.t += dt
        for i, dot in enumerate(m):
            ph = (i / n + m.t * speed) % 1
            dot.move_to(pos(ph * tot))
            dot.set_opacity(float(min(1, ph * 6, (1 - ph) * 6)))
    g.add_updater(upd)
    upd(g, 0)
    return g


def gauge(center, w, h, tr, color, op=0.5, maxh=None):
    mh = maxh or h

    def mk():
        hh = max(tr.get_value() * mh, 0.01)
        return Rectangle(width=w, height=hh, stroke_width=0, fill_color=color, fill_opacity=op).move_to(
            center + np.array([0, -h / 2 + hh / 2, 0]))
    return always_redraw(mk)


def wiggle(mob, amp=0.06, speed=2.0):
    mob.base = mob.get_center().copy()
    mob.tt = 0.0

    def u(m, dt):
        m.tt += dt
        m.move_to(m.base + np.array([0, amp * np.sin(m.tt * speed), 0]))
    mob.add_updater(u)


def pulse(mob, base=0.4, amp=0.2, speed=2.5):
    mob.tt = 0.0

    def u(m, dt):
        m.tt += dt
        m.set_fill(opacity=base + amp * np.sin(m.tt * speed))
    mob.add_updater(u)


def hstream(x, y0=-2.0, y1=0.0, n=4, speed=0.3):
    return stream([x, y0, 0], [x + 0.3, y1, 0], HEAT, n=n, speed=speed, r=0.09, wave=0.15)


class World:
    """Builds the carried objects in fixed places (same as chapter 1)."""

    def __init__(self, prod=True, herb=True, pred=True, soil=False, pf=1.0, hf=0.0):
        self.pf = ValueTracker(pf)
        self.hf = ValueTracker(hf)
        self.prod_box = rbox(BW, 1.6, GREEN, PROD_C)
        self.prod_fill = gauge(PROD_C, BW - 0.1, 1.5, self.pf, GREEN, 0.5, maxh=1.5)
        self.prod_lab = VGroup(T("Smooth", 26), T("cordgrass", 26)).arrange(DOWN, buff=0.03).move_to(PROD_C + np.array([-0.8, 0, 0]))
        self.prod_art = grass(PROD_C + np.array([1.7, -0.3, 0]), 1.3)
        self.prod = VGroup(self.prod_fill, self.prod_box, self.prod_lab, self.prod_art)
        self.herb_box = rbox(BW, 1.7, PALE, HERB_C, op=0.08)
        self.herb_fill = gauge(HERB_C, BW - 0.1, 1.6, self.hf, GREEN, 0.4, maxh=1.6)
        self.herb_lab = T("Herbivores", 30, TEXT).move_to(HERB_C + np.array([-0.8, 0, 0]))
        self.herb_art = hopper(HERB_C + np.array([1.6, 0, 0]), 1.3)
        self.herb = VGroup(self.herb_fill, self.herb_box, self.herb_lab, self.herb_art)
        self.pred_box = rbox(BW, 1.3, PALE, PRED_C, op=0.08)
        self.pred_lab = T("Predators", 30, TEXT).move_to(PRED_C + np.array([-0.8, 0, 0]))
        self.pred_art = spider(PRED_C + np.array([1.6, 0, 0]), 1.3)
        self.pred = VGroup(self.pred_box, self.pred_lab, self.pred_art)
        self.soil_box = rbox(6.2, 1.4, BROWN, SOIL_C, op=0.22)
        self.soil_lab = T("Detritus", 30, BROWN).move_to(SOIL_C + np.array([-1.35, 0, 0]))
        self.soil = VGroup(self.soil_box, self.soil_lab)
        self.parts = []
        if prod:
            self.parts.append(self.prod)
        if herb:
            self.parts.append(self.herb)
        if pred:
            self.parts.append(self.pred)
        if soil:
            self.parts.append(self.soil)

    def add_to(self, scene):
        scene.add(*self.parts)


def brown_door():
    return door([-1.55, -2.6, 0], BROWN)


def pipe(width=0.34, y=-1.17, h=1.35, op=0.6):
    return Rectangle(width=width, height=h, stroke_color=PURPLE, stroke_width=3, fill_color=PURPLE, fill_opacity=op).move_to([-4.1, y, 0])


def critters3():
    """bacteria cluster, snail, crab inside the detritus box (same places in every scene)."""
    bac = VGroup(bacterium(V(0, 0.12), 1.5), bacterium(V(0.1, -0.12), 1.5, 0.5), bacterium(V(-0.25, -0.08), 1.5, -0.4)).move_to(SOIL_C + V(0.6, 0.05))
    sn = snail(SOIL_C + V(1.55, 0.0), 0.95)
    cr = crab(SOIL_C + V(2.4, 0.0), 1.0)
    return bac, sn, cr


def blades_row(color=GREEN, s=1.5, y=-1.9):
    return VGroup(*[grass(V(x, y + 0.375 * s / 1.5 * 1.0), s, color) for x in (1.1, 1.95, 2.8, 3.65, 4.5, 5.35, 6.2)])


def predict_group():
    t1 = T("most of it", 34, TEXT)
    b1 = RoundedRectangle(corner_radius=0.15, width=t1.width + 0.5, height=0.8, stroke_color=GREEN, stroke_width=3, fill_color=GREEN, fill_opacity=0.12)
    o1 = VGroup(b1, t1.move_to(b1)).move_to([3.4, 1.2, 0])
    t2 = T("a small part", 34, TEXT)
    b2 = RoundedRectangle(corner_radius=0.15, width=t2.width + 0.5, height=0.8, stroke_color=GREEN, stroke_width=3, fill_color=GREEN, fill_opacity=0.12)
    o2 = VGroup(b2, t2.move_to(b2)).move_to([3.4, 0.2, 0])
    return o1, o2


def map_group():
    sea = Rectangle(width=14.4, height=8.2, stroke_width=0, fill_color=TEAL, fill_opacity=0.12)
    land_pts = [(-6.8, 3.8), (-1.8, 3.8), (-1.2, 2.9), (-0.2, 2.3), (0.1, 1.6), (-0.4, 0.9), (0.0, 0.4), (0.5, -0.1), (0.9, -0.7),
                (0.95, -1.5), (1.2, -2.4), (1.6, -3.2), (1.9, -3.8), (-6.8, -3.8)]
    land = Polygon(*[V(x, y) for x, y in land_pts], stroke_color=TEXT, stroke_width=4, fill_color="#6F7F5A", fill_opacity=0.4)
    geo = V(0.55, -0.15)
    mark = Dot(geo, radius=0.14, color=YELLOW)
    return VGroup(sea, land, mark), geo


def marsh_group():
    base = Rectangle(width=13.2, height=7.0, stroke_width=0, fill_color=GREEN, fill_opacity=0.22)
    creeks = VGroup()
    paths = []
    for a, k, ph, c0 in ((1.6, 0.55, 0.0, 0.0), (-0.4, 0.5, 1.7, 0.4), (-2.2, 0.45, 3.1, 0.0)):
        f = (lambda a, k, ph: (lambda t: np.array([t, a + k * np.sin(0.75 * t + ph), 0])))(a, k, ph)
        creeks.add(ParametricFunction(f, t_range=[-6.6, 6.6], color=TEAL, stroke_width=16, stroke_opacity=0.55))
        paths.append([f(t) for t in np.linspace(-6.6, 6.6, 14)])
    return base, creeks, paths


# =============================================================================================
class S00Title(TitleCard):
    LESSON = "Energy Flow and Productivity"
    TITLE = "Where the Marsh Grass Goes"


# ---------------------------------------------------------------------------------------------
class S01Link(SpokenScene):
    def construct(self):
        w = World(soil=True, pf=0.5, hf=0.15)
        brown = brown_door()
        pp = pipe(0.12)
        tag = chip("made-up budget", YELLOW, 28).move_to([4.7, 1.4, 0])
        self.play(FadeIn(w.prod), FadeIn(w.herb), FadeIn(w.pred), FadeIn(w.soil), FadeIn(pp), FadeIn(tag), run_time=self.beat(0.15))
        self.at("decomposers")
        pulse(w.soil_box, 0.22, 0.12, 2.0)
        tall = stream([2.2, -2.2, 0], [2.7, 3.5, 0], HEAT, n=9, speed=0.2, r=0.1, wave=0.2)
        self.play(Indicate(w.soil, color=BROWN), FadeIn(tall), run_time=self.beat(0.1))
        self.at("far more than")
        h1 = stream([-1.9, 0.8, 0], [-1.6, 1.8, 0], HEAT, n=3, speed=0.3, r=0.08, wave=0.1)
        h2 = stream([-1.9, 3.1, 0], [-1.6, 3.7, 0], HEAT, n=2, speed=0.3, r=0.08, wave=0.1)
        self.play(FadeIn(h1), FadeIn(h2), run_time=self.beat(0.06))
        self.at("Most plant production")
        wide = stream([-1.4, -2.6, 0], [0.5, -2.9, 0], BROWN, n=18, speed=0.5, r=0.15)
        up = stream([-4.1, -1.8, 0], [-4.1, -0.55, 0], PURPLE, n=2, speed=0.3, r=0.06)
        self.play(FadeIn(brown), FadeIn(wide), FadeIn(up), run_time=self.beat(0.08))
        self.at("never eaten")
        self.play(Indicate(pp, color=PURPLE, scale_factor=1.0), Wiggle(brown, scale_value=1.15), run_time=self.beat(0.1))
        self.finish()


class S02Question(SpokenScene):
    def construct(self):
        w = World(soil=True, pf=0.5, hf=0.15)
        w.add_to(self)
        brown = brown_door()
        pp = pipe(0.12)
        tag = chip("made-up budget", YELLOW, 28).move_to([4.7, 1.4, 0])
        pulse(w.soil_box, 0.22, 0.12, 2.0)
        tall = stream([2.2, -2.2, 0], [2.7, 3.5, 0], HEAT, n=9, speed=0.2, r=0.1, wave=0.2)
        h1 = stream([-1.9, 0.8, 0], [-1.6, 1.8, 0], HEAT, n=3, speed=0.3, r=0.08, wave=0.1)
        h2 = stream([-1.9, 3.1, 0], [-1.6, 3.7, 0], HEAT, n=2, speed=0.3, r=0.08, wave=0.1)
        wide = stream([-1.4, -2.6, 0], [0.5, -2.9, 0], BROWN, n=18, speed=0.5, r=0.15)
        up = stream([-4.1, -1.8, 0], [-4.1, -0.55, 0], PURPLE, n=2, speed=0.3, r=0.06)
        self.add(brown, pp, tag, tall, h1, h2, wide, up)
        self.play(FadeOut(tag, shift=UP * 0.6), run_time=self.beat(0.08))
        self.at("quirk of invented")
        self.play(*[m.animate.set_fill(opacity=0) for m in (w.prod_box, w.herb_box, w.pred_box, w.soil_box)],
                  w.pf.animate.set_value(0.0), w.hf.animate.set_value(0.0), run_time=self.beat(0.1))
        w.soil_box.clear_updaters()
        q = T("?", 110, YELLOW, weight=BOLD).move_to([-0.3, -1.45, 0])
        self.play(FadeIn(q, scale=1.4), run_time=self.beat(0.06))
        self.play(Indicate(q, scale_factor=1.25, color=YELLOW), run_time=self.beat(0.08))
        self.at("In a real ecosystem")
        mp, geo = map_group()
        self.play(FadeOut(VGroup(*w.parts, brown, pp, tall, h1, h2, wide, up)), FadeOut(q),
                  FadeIn(mp), run_time=self.beat(0.2))
        lab = T("Georgia coast", 30, TEXT).move_to([-2.6, -0.25, 0])
        self.play(FadeIn(lab), run_time=self.beat(0.05))
        ring = Circle(radius=0.2, color=YELLOW, stroke_width=4).move_to(geo)
        ring.add_updater(lambda m, dt: m.scale(1 + 0.8 * dt).set_stroke(opacity=max(0.0, m.get_stroke_opacity() - 0.5 * dt)))
        self.add(ring)
        self.finish()


class S03Teal(SpokenScene):
    def construct(self):
        mp, geo = map_group()
        lab = T("Georgia coast", 30, TEXT).move_to([-2.6, -0.25, 0])
        self.add(mp, lab)
        ring = Circle(radius=0.2, color=YELLOW, stroke_width=4).move_to(geo)
        ring.add_updater(lambda m, dt: m.scale(1 + 0.8 * dt).set_stroke(opacity=max(0.0, m.get_stroke_opacity() - 0.5 * dt)))
        self.add(ring)
        self.at("John Teal")
        card = chip("John Teal, Ecology, 1962", GOLD, 34).move_to([-2.4, 3.1, 0])
        card[0].set_fill(BG, 1.0)
        card.set_z_index(20)
        self.play(FadeIn(card, shift=DOWN * 0.2), run_time=self.beat(0.06))
        self.at("coast of Georgia")
        ring.clear_updaters()
        self.play(FadeOut(ring), FadeOut(lab), mp.animate.scale(3.2, about_point=geo).shift(-geo), run_time=self.beat(0.2))
        base, creeks, paths = marsh_group()
        self.at("He built an energy budget")
        tide = [pstream(p, TEAL, n=6, speed=0.12, r=0.1) for p in paths]
        self.play(FadeIn(base), FadeIn(creeks), FadeOut(mp), run_time=self.beat(0.12))
        self.add(*tide)
        self.at("published it in")
        self.play(Indicate(card, color=YELLOW, scale_factor=1.1), run_time=self.beat(0.1))
        self.finish()


class S04Grass(SpokenScene):
    def construct(self):
        base, creeks, paths = marsh_group()
        self.add(base, creeks)
        mud = Rectangle(width=14.4, height=1.4, stroke_width=0, fill_color=MUD, fill_opacity=0.55).move_to([0, -3.4, 0])
        gr = ValueTracker(0.0)
        blades = VGroup()
        rng = np.random.RandomState(3)
        for i in range(36):
            x = -6.5 + 13.0 * i / 35
            h0 = 2.4 + rng.rand() * 2.0
            ph = rng.rand() * 6.28
            ln = Line(V(x, -2.7, 0), V(x, -2.7 + h0, 0)).set_stroke(GREEN, 8)
            ln.h0, ln.ph, ln.x0, ln.tt = h0, ph, x, 0.0

            def u(m, dt):
                m.tt += dt
                h = m.h0 * (0.1 + 0.9 * gr.get_value())
                m.put_start_and_end_on(V(m.x0, -2.7, 0), V(m.x0 + 0.15 * np.sin(m.tt * 1.5 + m.ph) * h / 2, -2.7 + h, 0))
            ln.add_updater(u)
            blades.add(ln)
        water = Rectangle(width=14.4, height=0.8, stroke_width=0, fill_color=TEAL, fill_opacity=0.3)
        water.tt = 0.0

        def wu(m, dt):
            m.tt += dt
            m.stretch_to_fit_height(0.3 + 0.35 * (1 + np.sin(m.tt * 0.9)))
            m.move_to(V(0, -2.7 + m.height / 2, 0))
        water.add_updater(wu)
        self.add(mud, blades, water)
        self.play(gr.animate.set_value(0.6), FadeOut(creeks), run_time=self.beat(0.25))
        self.at("smooth cordgrass")
        lab = VGroup(T("Smooth cordgrass", 40, GREEN), T("Spartina alterniflora", 24, GREY)).arrange(DOWN, buff=0.08).move_to([0, 2.7, 0])
        self.play(FadeIn(lab, shift=UP * 0.2), run_time=self.beat(0.08))
        self.at("tidal mud")
        self.play(Indicate(mud, color=BROWN, scale_factor=1.0), run_time=self.beat(0.08))
        self.at("great deal of plant matter")
        self.play(gr.animate.set_value(1.0), run_time=self.beat(0.15))
        self.at("each year")
        w = World(herb=False, pred=False, pf=0.0)
        for b in blades:
            b.clear_updaters()
        water.clear_updaters()
        self.play(ReplacementTransform(blades, w.prod_box), FadeOut(mud), FadeOut(water), FadeOut(base), FadeOut(lab),
                  FadeIn(w.prod_lab), FadeIn(w.prod_art), run_time=self.beat(0.1))
        self.add(w.prod_fill)
        self.play(w.pf.animate.set_value(1.0), run_time=self.beat(0.1))
        self.finish()


class S05Chain(SpokenScene):
    def construct(self):
        w = World(pf=1.0, hf=0.0)
        self.add(w.prod)
        tag = VGroup(T("grazing-chain prediction", 30, TEXT), T("(schematic)", 26, GREY)).arrange(DOWN, buff=0.08).move_to([3.4, 0.9, 0])
        self.at("grazing chain")
        self.play(FadeIn(tag), run_time=self.beat(0.06))
        self.at("Grass feeds")
        p1 = pipe(0.7, -1.17, 1.25, 0.55)
        up1 = stream([-4.1, -1.7, 0], [-4.1, -0.65, 0], PURPLE, n=4, speed=0.3, r=0.1)
        wiggle(w.herb_art, 0.06, 3.0)
        self.play(FadeIn(w.herb), FadeIn(p1), FadeIn(up1), run_time=self.beat(0.12))
        w.hf.set_value(0.0)
        self.play(w.hf.animate.set_value(0.6), run_time=self.beat(0.08))
        self.at("herbivores feed the predators")
        p2 = pipe(0.7, 1.7, 1.1, 0.55)
        up2 = stream([-4.1, 1.25, 0], [-4.1, 2.2, 0], PURPLE, n=3, speed=0.3, r=0.1)
        self.play(FadeIn(w.pred), FadeIn(p2), FadeIn(up2), run_time=self.beat(0.12))
        self.play(Indicate(w.pred_box, color=PURPLE, scale_factor=1.03), run_time=self.beat(0.1))
        wiggle(w.pred_art, 0.06, 3.0)
        self.play(w.hf.animate.set_value(0.95), run_time=self.beat(0.2))
        self.finish()


def icon_quadrat():
    sq = Square(side_length=2.2, stroke_color=TEXT, stroke_width=5, fill_color=GREEN, fill_opacity=0.18)
    bl = VGroup(*[grass(V(x, y, 0), 1.0) for x in (-0.55, 0.55) for y in (-0.55, 0.4)])
    cap = T("clipped grass", 26, TEXT).next_to(sq, DOWN, buff=0.15)
    return VGroup(sq, bl, cap)


def icon_algae():
    mud = Rectangle(width=2.8, height=1.5, stroke_color=TEXT, stroke_width=4, fill_color=MUD, fill_opacity=0.55)
    pts = [(-0.9, 0.2), (-0.2, -0.3), (0.6, 0.25), (0.9, -0.2), (0.1, 0.45)]
    al = VGroup(*[Ellipse(width=0.6, height=0.3, stroke_width=0, fill_color=GREEN, fill_opacity=0.8).move_to(V(x, y, 0)) for x, y in pts])
    cap = T("algae on the mud", 26, TEXT).next_to(mud, DOWN, buff=0.15)
    return VGroup(mud, al, cap)


def icon_animals():
    a = VGroup(crab(V(-1.0, 0.0), 1.2), snail(V(0.2, 0.0), 1.2), hopper(V(1.3, 0.0), 1.0))
    cap = T("crabs, snails, insects", 26, TEXT).next_to(a, DOWN, buff=0.3)
    return VGroup(a, cap)


def icon_bacteria():
    c = Circle(radius=1.1, stroke_color=TEXT, stroke_width=5, fill_color=TEAL, fill_opacity=0.08)
    rods = VGroup(*[bacterium(V(x, y, 0), 1.6, a) for x, y, a in ((-0.4, 0.4, 0.3), (0.3, 0.5, -0.6), (0.5, -0.3, 0.9), (-0.5, -0.4, -0.2), (0.0, 0.0, 1.3))])
    cap = T("bacteria", 26, TEXT).next_to(c, DOWN, buff=0.15)
    return VGroup(c, rods, cap)


class S06Measure(SpokenScene):
    def construct(self):
        w = World(pred=False, soil=True, pf=1.0, hf=0.0)
        w.add_to(self)
        wiggle(w.herb_art, 0.05, 3.0)
        stage = V(3.4, 0.9)
        pulse(w.soil_box, 0.2, 0.12, 2.0)
        pulse(w.prod_box, 0.2, 0.1, 2.3)

        def drop(ic, target, then=None):
            anims = [ic.animate.scale(0.25).move_to(target).set_opacity(0)]
            if then is not None:
                anims.append(then)
            self.play(*anims, run_time=self.beat(0.07))
            self.remove(ic)

        self.at("measurements of the grass")
        q = icon_quadrat().scale(1.4).move_to(stage)
        self.play(FadeIn(q, scale=0.6), run_time=self.beat(0.06))
        self.wait(self.beat(0.05))
        self.at("algae")
        drop(q, PROD_C)
        al = icon_algae().scale(1.4).move_to(stage)
        self.play(FadeIn(al, scale=0.6), run_time=self.beat(0.06))
        self.wait(self.beat(0.04))
        self.at("measurements of the animals")
        drop(al, PROD_C)
        an = icon_animals().scale(1.4).move_to(stage)
        self.play(FadeIn(an, scale=0.6), run_time=self.beat(0.06))
        self.wait(self.beat(0.04))
        self.at("bacteria living")
        drop(an, HERB_C, w.hf.animate.set_value(0.4))
        bc = icon_bacteria().scale(1.4).move_to(stage)
        self.play(FadeIn(bc, scale=0.6), run_time=self.beat(0.06))
        self.wait(self.beat(0.05))
        drop(bc, SOIL_C)
        self.finish()


class S07Predict(SpokenScene):
    def construct(self):
        w = World(pred=False, pf=1.0, hf=0.0)
        w.add_to(self)
        pp = pipe(0.34)
        up = stream([-4.1, -1.7, 0], [-4.1, -0.65, 0], PURPLE, n=3, speed=0.3, r=0.09)
        wiggle(w.herb_art, 0.06, 3.0)
        self.add(pp, up)
        pp.tt = 0.0

        def flick(m, dt):
            m.tt += dt
            m.stretch_to_fit_width(0.12 + 0.5 * (0.5 + 0.5 * np.sin(m.tt * 3.0)))
            m.move_to(V(-4.1, -1.17, 0))
        pp.add_updater(flick)
        bl = blades_row(GREEN, 2.0)
        self.play(FadeIn(bl, shift=UP * 0.2), run_time=self.beat(0.1))
        hops = VGroup(*[hopper(V(x, -0.7), 1.0) for x in (2.0, 3.7, 5.4)])
        for h in hops:
            wiggle(h, 0.06, 4.0)
        self.at("graze on the living grass")
        self.play(FadeIn(hops, shift=DOWN * 0.2), run_time=self.beat(0.1))
        o1, o2 = predict_group()
        self.at("most of its production")
        self.play(FadeIn(o1, shift=LEFT * 0.3), run_time=self.beat(0.08))
        self.at("only a small part")
        self.play(FadeIn(o2, shift=LEFT * 0.3), run_time=self.beat(0.08))
        self.play(Indicate(o1, color=YELLOW), Indicate(o2, color=YELLOW), run_time=self.beat(0.15))
        self.finish()


class S08Pause(NarratedScene):
    def construct(self):
        w = World(pred=False, pf=1.0, hf=0.0)
        w.add_to(self)
        pp = pipe(0.34)
        up = stream([-4.1, -1.7, 0], [-4.1, -0.65, 0], PURPLE, n=3, speed=0.3, r=0.09)
        wiggle(w.herb_art, 0.06, 3.0)
        pp.tt = 0.0

        def flick(m, dt):
            m.tt += dt
            m.stretch_to_fit_width(0.12 + 0.5 * (0.5 + 0.5 * np.sin(m.tt * 3.0)))
            m.move_to(V(-4.1, -1.17, 0))
        pp.add_updater(flick)
        bl = blades_row(GREEN, 2.0)
        hops = VGroup(*[hopper(V(x, -0.7), 1.0) for x in (2.0, 3.7, 5.4)])
        for h in hops:
            wiggle(h, 0.06, 4.0)
        o1, o2 = predict_group()
        q = VGroup(T("Predict: how much of the grass", 26, YELLOW), T("do grazers take?", 26, YELLOW)).arrange(DOWN, buff=0.1).move_to([2.0, 2.7, 0])
        self.add(pp, up, bl, hops, o1, o2, q)
        tr = ValueTracker(5.0)
        tr.add_updater(lambda m, dt: m.increment_value(-dt))
        self.add(tr)
        cd = always_redraw(lambda: M(str(max(1, int(np.ceil(tr.get_value())))), 60, TEXT).move_to([6.3, 2.7, 0]))
        self.add(cd)
        self.wait(5.0)


class S09Reveal(SpokenScene):
    def construct(self):
        w = World(pred=False, pf=1.0, hf=0.0)
        w.add_to(self)
        pp = pipe(0.34)
        up = stream([-4.1, -1.7, 0], [-4.1, -0.65, 0], PURPLE, n=3, speed=0.3, r=0.09)
        wiggle(w.herb_art, 0.06, 3.0)
        pp.tt = 0.0
        pp.mode = 0.0

        def flick(m, dt):
            m.tt += dt
            wd = 0.12 + 0.5 * (0.5 + 0.5 * np.sin(m.tt * 3.0)) * (1 - m.mode) + 0.0 * m.mode
            m.stretch_to_fit_width(max(wd, 0.12))
            m.move_to(V(-4.1, -1.17, 0))
        pp.add_updater(flick)
        bl = blades_row(GREEN, 2.0)
        hops = VGroup(*[hopper(V(x, -0.7), 1.0) for x in (2.0, 3.7, 5.4)])
        for h in hops:
            wiggle(h, 0.06, 4.0)
        o1, o2 = predict_group()
        self.add(pp, up, bl, hops, o1, o2)
        self.at("Only a small part")
        self.play(FadeOut(o1), o2[0].animate.set_fill(GREEN, 0.5).set_stroke(YELLOW, 5), Indicate(o2, color=YELLOW), run_time=self.beat(0.1))
        self.at("the purple pipe")
        self.play(Indicate(pp, color=PURPLE, scale_factor=1.0), run_time=self.beat(0.08))
        self.at("was thin")
        thin_up = stream([-4.1, -1.7, 0], [-4.1, -0.65, 0], PURPLE, n=2, speed=0.3, r=0.06)
        pp.mode = 1.0
        lab = VGroup(T("grazers: a small part", 24, PURPLE), T("of production", 24, PURPLE)).arrange(DOWN, buff=0.04, aligned_edge=LEFT).move_to([-3.85, -1.17, 0], aligned_edge=LEFT)
        self.play(FadeOut(up), FadeIn(thin_up), FadeIn(lab), run_time=self.beat(0.1))
        self.at("side channel")
        self.play(Wiggle(pp, scale_value=1.5), run_time=self.beat(0.1))
        self.finish()


def fragments(n=22, seed=5):
    rng = np.random.RandomState(seed)
    fr = VGroup()
    for i in range(n):
        x = 0.8 + 5.4 * rng.rand()
        y = -1.9 + 0.8 * rng.rand()
        ang = rng.rand() * PI
        ln = Line(V(-0.09, 0, 0), V(0.09, 0, 0)).rotate(ang).set_stroke("#C9A94A", 5).move_to(V(x, y, 0))
        fr.add(ln)
    return fr


class S10Detritus(SpokenScene):
    def construct(self):
        w = World(pred=False, soil=True, pf=1.0, hf=0.0)
        w.add_to(self)
        brown = brown_door()
        pp = pipe(0.12)
        thin_up = stream([-4.1, -1.7, 0], [-4.1, -0.65, 0], PURPLE, n=2, speed=0.3, r=0.06)
        wiggle(w.herb_art, 0.06, 3.0)
        bl = blades_row(GREEN, 2.0)
        self.add(brown, pp, thin_up, bl)
        self.at("Much of the grass died")
        yel = blades_row("#C9A94A", 2.0)
        self.play(Transform(bl, yel), run_time=self.beat(0.15))
        self.at("broke into fragments")
        fr = fragments()
        self.play(FadeOut(bl), FadeIn(fr), run_time=self.beat(0.06))
        rng = np.random.RandomState(8)
        moves = [f.animate.move_to(V(0.6 + 2.7 * rng.rand(), -3.5 + 0.2 * rng.rand(), 0)).set_opacity(0.9) for f in fr]
        pulse(w.soil_box, 0.22, 0.12, 2.0)
        wide = stream([-1.4, -2.6, 0], [0.5, -2.9, 0], BROWN, n=18, speed=0.5, r=0.15)
        self.play(LaggedStart(*moves, lag_ratio=0.05), FadeIn(wide), run_time=self.beat(0.2))
        self.at("Bacteria used")
        bac, sn, cr = critters3()
        for m in (bac, sn, cr):
            m.shift(UP * 0.5)
        self.play(FadeIn(bac, shift=DOWN * 0.5), run_time=self.beat(0.07))
        self.at("animals that feed")
        self.play(FadeIn(sn, shift=DOWN * 0.5), FadeIn(cr, shift=DOWN * 0.5), run_time=self.beat(0.07))
        for m in (bac, sn, cr):
            m.base0 = m.get_center().copy()
        self.play(bac.animate.shift(DOWN * 0.5), sn.animate.shift(DOWN * 0.5), cr.animate.shift(DOWN * 0.5), run_time=self.beat(0.07))
        wiggle(bac, 0.04, 3.0)
        wiggle(sn, 0.03, 2.0)
        wiggle(cr, 0.04, 2.5)
        self.finish()


def soil_scene_base(scene, with_critters=True):
    """Marsh diagram of s10 end state, rebuilt in the same places. Returns the objects."""
    w = World(pred=False, soil=True, pf=1.0, hf=0.0)
    w.add_to(scene)
    brown = brown_door()
    pp = pipe(0.12)
    thin_up = stream([-4.1, -1.7, 0], [-4.1, -0.65, 0], PURPLE, n=2, speed=0.3, r=0.06)
    wide = stream([-1.4, -2.6, 0], [0.5, -2.9, 0], BROWN, n=18, speed=0.5, r=0.15)
    pulse(w.soil_box, 0.22, 0.12, 2.0)
    wiggle(w.herb_art, 0.06, 3.0)
    scene.add(brown, pp, thin_up, wide)
    rng = np.random.RandomState(8)
    pile = VGroup(*[Line(V(-0.09, 0, 0), V(0.09, 0, 0)).rotate(rng.rand() * PI).set_stroke("#C9A94A", 5).move_to(V(0.6 + 2.7 * rng.rand(), -3.5 + 0.2 * rng.rand(), 0)) for _ in range(22)])
    scene.add(pile)
    w.thin_up = thin_up
    objs = [w, brown, pp, thin_up, wide, pile]
    crit = None
    if with_critters:
        bac, sn, cr = critters3()
        wiggle(bac, 0.04, 3.0)
        wiggle(sn, 0.03, 2.0)
        wiggle(cr, 0.04, 2.5)
        scene.add(bac, sn, cr)
        crit = (bac, sn, cr)
    return w, brown, pp, pile, crit


class S11Eaten(SpokenScene):
    def construct(self):
        w, brown, pp, pile, (bac, sn, cr) = soil_scene_base(self)
        self.at("Those detritus feeders")
        pred = spider(V(2.0, 0.6), 1.6)
        wiggle(pred, 0.06, 2.5)
        lab = T("schematic consumer", 26, TEXT).move_to([2.0, 1.7, 0])
        self.play(FadeIn(pred, shift=DOWN * 0.3), FadeIn(lab), run_time=self.beat(0.1))
        sn2 = sn.copy()
        cr2 = cr.copy()
        sn2.clear_updaters()
        cr2.clear_updaters()
        self.play(Indicate(sn, color=YELLOW), Indicate(cr, color=YELLOW), run_time=self.beat(0.08))
        self.at("themselves eaten")
        pipe_up = Rectangle(width=0.5, height=2.0, stroke_color=PURPLE, stroke_width=3, fill_color=PURPLE, fill_opacity=0.55).move_to(V(2.0, -1.25, 0))
        pst = stream([2.0, -2.2, 0], [2.0, -0.35, 0], PURPLE, n=4, speed=0.3, r=0.09)
        self.add(sn2, cr2)
        self.play(FadeIn(pipe_up), FadeIn(pst), run_time=self.beat(0.08))
        self.play(sn2.animate.move_to(V(2.0, -1.4, 0)).scale(0.7), run_time=self.beat(0.1))
        self.play(sn2.animate.move_to(V(2.0, 0.1, 0)).set_opacity(0), run_time=self.beat(0.08))
        self.at("not a dead end")
        pl = VGroup(T("detrital route", 30, PURPLE), T("(schematic)", 26, GREY)).arrange(DOWN, buff=0.06, aligned_edge=RIGHT).move_to([0.95, -1.2, 0], aligned_edge=RIGHT)
        self.play(FadeIn(pl), cr2.animate.move_to(V(2.0, -1.4, 0)).scale(0.7), run_time=self.beat(0.1))
        self.at("second route")
        self.play(cr2.animate.move_to(V(2.0, 0.1, 0)).set_opacity(0), Indicate(pipe_up, color=PURPLE, scale_factor=1.0), run_time=self.beat(0.1))
        self.finish()


def consumer_chain(scene):
    pred = spider(V(2.0, 0.6), 1.6)
    wiggle(pred, 0.06, 2.5)
    lab = T("schematic consumer", 26, TEXT).move_to([2.0, 1.7, 0])
    pipe_up = Rectangle(width=0.5, height=2.0, stroke_color=PURPLE, stroke_width=3, fill_color=PURPLE, fill_opacity=0.55).move_to(V(2.0, -1.25, 0))
    pst = stream([2.0, -2.2, 0], [2.0, -0.35, 0], PURPLE, n=4, speed=0.3, r=0.09)
    pl = VGroup(T("detrital route", 30, PURPLE), T("(schematic)", 26, GREY)).arrange(DOWN, buff=0.06, aligned_edge=RIGHT).move_to([0.95, -1.2, 0], aligned_edge=RIGHT)
    scene.add(pipe_up, pst, pred, lab, pl)
    return pred, lab, pipe_up, pst, pl


class S12Heat(SpokenScene):
    def construct(self):
        w, brown, pp, pile, (bac, sn, cr) = soil_scene_base(self)
        pred, lab, pipe_up, pst, pl = consumer_chain(self)
        self.at("Every organism")
        self.play(Indicate(bac, color=HEAT), Indicate(sn, color=HEAT), Indicate(cr, color=HEAT), Indicate(pred, color=HEAT), run_time=self.beat(0.1))
        self.at("releases heat")
        hs = [hstream(3.7, -2.0, 0.4, n=3, speed=0.22), hstream(4.7, -2.0, 0.6, n=4, speed=0.31), hstream(5.7, -2.0, 0.2, n=5, speed=0.38), hstream(4.2, 0.6, 2.8, n=3, speed=0.27)]
        self.play(*[FadeIn(h) for h in hs], run_time=self.beat(0.08))
        ht = T("heat", 32, HEAT).move_to([5.3, 0.9, 0])
        self.play(FadeIn(ht), run_time=self.beat(0.05))
        self.at("never returns")
        arr = DashedLine(V(0.2, -3.3, 0), V(-1.7, -3.3, 0), color=BROWN, stroke_width=6, dash_length=0.18)
        arr.add_tip(tip_length=0.25)
        x = VGroup(Line(V(-0.95, -3.1, 0), V(-0.55, -3.5, 0)), Line(V(-0.95, -3.5, 0), V(-0.55, -3.1, 0))).set_stroke(RED, 7)
        nr = VGroup(T("energy:", 26, RED), T("no return", 26, RED)).arrange(DOWN, buff=0.05).move_to([-5.5, -1.2, 0])
        self.play(Create(arr), run_time=self.beat(0.08))
        self.play(FadeIn(x, scale=1.5), FadeIn(nr), run_time=self.beat(0.08))
        self.play(Indicate(nr, color=RED, scale_factor=1.1), run_time=self.beat(0.1))
        self.finish()


class S13Matter(SpokenScene):
    def construct(self):
        w, brown, pp, pile, (bac, sn, cr) = soil_scene_base(self)
        hs = [hstream(3.7, -2.0, 0.4), hstream(4.7, -2.0, 0.4, n=4), hstream(5.7, -2.0, 0.4, n=4)]
        self.add(*hs)
        pred, lab, pipe_up, pst, pl = consumer_chain(self)
        # the energy picture of the last scene gives way to matter cycling
        self.play(FadeOut(VGroup(pred, lab, pipe_up, pst, pl, *hs, w.herb, pp, w.thin_up)), run_time=self.beat(0.06))
        self.at("Only matter cycles")
        cyc = T("matter cycles", 36, YELLOW).move_to([3.4, 0.6, 0])
        self.play(FadeIn(cyc), run_time=self.beat(0.05))
        self.at("Nutrients return")
        nl = T("nutrients", 28, TEAL).move_to([-0.5, -1.75, 0])
        nut = pstream([V(0.2, -3.45, 0), V(-3.4, -3.45, 0), V(-3.4, -3.25, 0)], TEAL, n=6, speed=0.15, r=0.09)
        roots = VGroup(*[Line(V(x, -3.4, 0), V(x + dx, -3.75, 0)).set_stroke(GREEN, 3) for x, dx in ((-3.4, -0.15), (-3.1, 0.05), (-3.7, -0.1))])
        self.play(FadeIn(nl), FadeIn(nut), FadeIn(roots), FadeOut(cyc), run_time=self.beat(0.08))
        self.at("Carbon returns")
        cl = T("carbon", 28, YELLOW).move_to([5.2, 0.2, 0])
        path = [V(3.7, -2.0, 0), V(3.7, 1.5, 0), V(-2.4, 1.5, 0), V(-2.4, -1.75, 0)]
        cd = pstream(path, YELLOW, n=9, speed=0.1, r=0.09)
        self.play(FadeIn(cl), FadeIn(cd), run_time=self.beat(0.08))
        self.at("carbon dioxide")
        c2 = co2(34, TEXT).move_to([0.6, 2.2, 0])
        self.play(FadeIn(c2, shift=UP * 0.2), run_time=self.beat(0.05))
        self.at("which the leaves")
        self.play(Indicate(w.prod_art, color=GREEN, scale_factor=1.5), run_time=self.beat(0.08))
        self.at("The energy comes")
        sun = Circle(radius=0.32, stroke_color=YELLOW, stroke_width=3, fill_color=YELLOW, fill_opacity=0.9).move_to([-4.6, 3.1, 0])
        ss = stream([-4.6, 2.7, 0], [-4.6, -1.7, 0], YELLOW, n=7, speed=0.25, r=0.1)
        el = T("energy in", 30, YELLOW).move_to([-4.3, 2.5, 0], aligned_edge=LEFT)
        self.play(FadeIn(sun), FadeIn(ss), FadeIn(el), run_time=self.beat(0.1))
        self.finish()


def bar_parts():
    L, R, y, h = -5.5, 5.5, 0.7, 2.2
    split = L + (R - L) * 0.55
    grey = Rectangle(width=split - L, height=h, stroke_color=HEAT, stroke_width=3, fill_color=GREEN, fill_opacity=0.5).move_to(V((L + split) / 2, y, 0))
    rem = Rectangle(width=R - split, height=h, stroke_color=GREEN, stroke_width=3, fill_color=GREEN, fill_opacity=0.5).move_to(V((split + R) / 2, y, 0))
    return grey, rem, V((split + R) / 2, y, 0)


class S14Remainder(SpokenScene):
    def construct(self):
        grey, rem, rc = bar_parts()
        top = T("net production", 36, GREEN).move_to([0, 2.5, 0])
        self.play(FadeIn(grey), FadeIn(rem), FadeIn(top, shift=DOWN * 0.2), run_time=self.beat(0.12))
        self.at("remainder")
        self.play(Indicate(rem, color=YELLOW, scale_factor=1.0), run_time=self.beat(0.06))
        self.at("After the respiration")
        gl = T("respiration of bacteria and animals", 28, HEAT).move_to([-2.3, -3.45, 0])
        self.play(grey.animate.set_fill(HEAT, 0.55).set_stroke(HEAT, 3), run_time=self.beat(0.08))
        self.play(grey.animate.shift(DOWN * 3.0).scale(0.5, about_point=V(-3.2, -2.3, 0)), FadeIn(gl), run_time=self.beat(0.12))
        self.at("about 45 percent")
        dash = DashedVMobject(Rectangle(width=rem.width, height=rem.height, stroke_color=YELLOW, stroke_width=6).move_to(rem), num_dashes=40)
        pct = M("45%", 60, YELLOW).move_to(rc)
        self.play(rem.animate.set_fill(GREEN, 0.12).set_stroke(GREEN, 0), FadeIn(dash), FadeIn(pct), run_time=self.beat(0.1))
        tag = VGroup(T("remainder: about 45%", 30, YELLOW), T("of net production", 30, YELLOW)).arrange(DOWN, buff=0.06).move_to([3.4, -1.2, 0])
        self.play(FadeIn(tag, shift=UP * 0.2), FadeOut(top), run_time=self.beat(0.08))
        self.play(Indicate(pct, color=YELLOW, scale_factor=1.15), run_time=self.beat(0.1))
        self.finish()


def creek_f(t):
    return np.array([t, 0.5 + 0.95 * np.sin(0.8 * t), 0.0])


class S15Hedge(SpokenScene):
    def construct(self):
        grey, rem, rc = bar_parts()
        dash = DashedVMobject(Rectangle(width=rem.width, height=rem.height, stroke_color=YELLOW, stroke_width=6).move_to(rem), num_dashes=40)
        rem.set_fill(GREEN, 0.12).set_stroke(GREEN, 0)
        pct = M("45%", 60, YELLOW).move_to(rc)
        remg = VGroup(rem, dash, pct)
        self.add(remg)
        creek = ParametricFunction(creek_f, t_range=[-5.8, 3.4], color=TEAL, stroke_width=26, stroke_opacity=0.5)
        sea = VGroup(*[ParametricFunction(lambda t, y=y: np.array([4.9 + 0.3 * t, y + 0.12 * np.sin(5 * t), 0]), t_range=[0, 6.0 if False else 6], color=TEAL, stroke_width=4)
                       for y in (-2.6, -1.8, -1.0, -0.2, 0.6, 1.4, 2.2)])
        seal = T("open water", 28, TEAL).move_to([5.5, 2.7, 0])
        self.at("He took it")
        pk = VGroup(Rectangle(width=2.0, height=1.1, stroke_color=YELLOW, stroke_width=5, fill_color=GREEN, fill_opacity=0.15), M("45%", 36, YELLOW))
        pk.move_to(creek_f(-5.8) + UP * 0.0)
        self.play(FadeIn(creek), FadeIn(sea), FadeIn(seal), ReplacementTransform(remg, pk), run_time=self.beat(0.15))
        self.at("available to leave")
        q = T("available to leave with the tides?", 34, YELLOW).move_to([-1.0, 2.7, 0])
        arr = DashedVMobject(ParametricFunction(creek_f, t_range=[-5.2, 3.2]).set_stroke(YELLOW, 5), num_dashes=40)
        self.play(FadeIn(q), Create(arr), MoveAlongPath(pk, ParametricFunction(creek_f, t_range=[-5.8, 3.4])), run_time=self.beat(0.3), rate_func=linear)
        self.at("not a measured export")
        stamp = VGroup(RoundedRectangle(corner_radius=0.12, width=9.2, height=1.0, stroke_color=RED, stroke_width=6, fill_color=BG, fill_opacity=0.9),
                       T("remainder, not a measured export", 34, RED)).move_to([-1.3, -1.6, 0]).rotate(0.08)
        stamp[1].move_to(stamp[0])
        self.play(FadeIn(stamp, scale=1.25), run_time=self.beat(0.06), rate_func=rush_from)
        self.play(Wiggle(stamp, scale_value=1.05, rotation_angle=0.02 * TAU), run_time=self.beat(0.08))
        self.finish()


class S16Shift(SpokenScene):
    def construct(self):
        page = RoundedRectangle(corner_radius=0.12, width=6.2, height=6.8, stroke_color=PALE, stroke_width=4, fill_color=PALE, fill_opacity=0.1).move_to([0, 0, 0])
        bars = VGroup(*[Line(V(-2.5, 2.2 - 0.5 * i, 0), V(-2.5 + (4.9 if i % 3 else 3.6), 2.2 - 0.5 * i, 0)).set_stroke(GREY, 8) for i in range(9)])
        title = T("Coastal ecology", 30, TEXT).move_to([0, 2.8, 0])
        rule = Line(V(-2.7, -2.5, 0), V(-0.7, -2.5, 0)).set_stroke(GREY, 3)
        foot = T("* detritus", 22, BROWN).move_to([-1.2, -2.85, 0])
        self.play(FadeIn(page), FadeIn(title), LaggedStart(*[Create(b) for b in bars], lag_ratio=0.12), FadeIn(rule), run_time=self.beat(0.18))
        self.play(FadeIn(foot), run_time=self.beat(0.04))
        self.at("changed the picture")
        self.play(Indicate(foot, color=BROWN, scale_factor=1.3), run_time=self.beat(0.1))
        self.at("moved detritus")
        # coastal budget diagram, detritus at the centre
        gbox = rbox(3.6, 1.3, GREEN, V(-3.7, 2.6, 0))
        glab = T("Producers", 28, TEXT).move_to(gbox)
        hbox = rbox(3.6, 1.3, PALE, V(3.7, 2.6, 0), op=0.08)
        hlab = T("Consumers", 28, TEXT).move_to(hbox)
        bbox = rbox(8.6, 1.9, BROWN, V(0, -0.5, 0), op=0.35)
        blab = T("Detritus", 40, BROWN).move_to(bbox)
        thin = Rectangle(width=0.12, height=1.0, stroke_color=PURPLE, stroke_width=3, fill_color=PURPLE, fill_opacity=0.6)
        link = Line(V(-1.9, 2.6, 0), V(1.9, 2.6, 0)).set_stroke(PURPLE, 4)
        wide = Rectangle(width=1.2, height=1.1, stroke_color=BROWN, stroke_width=3, fill_color=BROWN, fill_opacity=0.5).move_to(V(-3.7, 1.0, 0))
        self.play(FadeOut(VGroup(page, bars, title, rule)), foot.animate.move_to(V(0, -0.5, 0)).scale(1.0), run_time=self.beat(0.07))
        self.play(FadeIn(gbox), FadeIn(glab), FadeIn(hbox), FadeIn(hlab), FadeIn(link), run_time=self.beat(0.08))
        self.at("center of coastal")
        self.play(ReplacementTransform(foot, VGroup(bbox, blab)), run_time=self.beat(0.18))
        hs = [hstream(-4.5, 3.4, 3.8, n=2), hstream(0.0, 0.5, 2.0, n=4), hstream(4.5, 1.9, 3.7, n=2)]
        self.play(*[FadeIn(h) for h in hs], run_time=self.beat(0.06))
        self.play(Indicate(bbox, color=BROWN, scale_factor=1.03), run_time=self.beat(0.1))
        self.finish()


class S17Rule(SpokenScene):
    def construct(self):
        w = World(pred=False, soil=True, pf=1.0, hf=0.0)
        w.add_to(self)
        brown = brown_door()
        pp = pipe(0.12)
        up = stream([-4.1, -1.7, 0], [-4.1, -0.65, 0], PURPLE, n=2, speed=0.3, r=0.06)
        wiggle(w.herb_art, 0.06, 3.0)
        wide = stream([-1.4, -2.6, 0], [0.5, -2.9, 0], BROWN, n=18, speed=0.5, r=0.15)
        pulse(w.soil_box, 0.22, 0.12, 2.0)
        self.add(up)
        self.play(FadeIn(w.prod), FadeIn(w.herb), FadeIn(w.soil), FadeIn(pp), run_time=self.beat(0.1))
        self.at("keep the brown door")
        self.play(FadeIn(brown), FadeIn(wide), run_time=self.beat(0.06))
        ring = SurroundingRectangle(brown, color=YELLOW, buff=0.12, stroke_width=6)
        lab = T("keep it in the budget", 30, YELLOW).move_to([-0.8, -1.45, 0], aligned_edge=LEFT)
        self.play(Create(ring), FadeIn(lab), run_time=self.beat(0.1))
        self.at("most grass production")
        self.play(Indicate(w.soil_box, color=BROWN, scale_factor=1.03), run_time=self.beat(0.1))
        self.at("rather than to grazers")
        self.play(Indicate(pp, color=PURPLE, scale_factor=1.0), run_time=self.beat(0.08))
        self.at("respiration released")
        hs = [stream([-1.5, -1.7, 0], [-0.9, 0.6, 0], HEAT, n=4, speed=0.27, r=0.09, wave=0.15),
              stream([-1.4, 0.9, 0], [-0.9, 2.4, 0], HEAT, n=3, speed=0.33, r=0.09, wave=0.15),
              stream([5.4, -2.2, 0], [5.9, 3.2, 0], HEAT, n=9, speed=0.2, r=0.1, wave=0.2)]
        self.play(*[FadeIn(h) for h in hs], run_time=self.beat(0.1))
        ht = T("heat", 32, HEAT).move_to([4.6, 1.2, 0])
        self.play(FadeIn(ht), run_time=self.beat(0.06))
        self.finish()


class S18End(EndCard):
    LINE = "Detritus belongs in every energy budget; its energy also leaves as heat."
