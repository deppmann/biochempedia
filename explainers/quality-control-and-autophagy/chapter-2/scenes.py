"""When the ER Falls Behind: chapter 2 of the quality-control film pair.

COLOR MAP (kept from chapter 1)
  BLUE   arrival carriers, autophagosomes     ORANGE lysosomes and clearance
  GOLD   proteasome                           RED    ubiquitin tags, ERAD route
  TEAL   ER folding helpers                   GREY   cell material, ER, structure
  YELLOW the unfolded-load gauge / exposed stretches
  GREEN  exit 1 (folded)   AMBER the unfolded protein response (UPR)
One world: the ER lumen, translocon slot, gauge and dots are rebuilt in the same place
by World() in every scene.  All diagrams are schematic; proteins are cartoons or blocks.
"""
import math
import random
import numpy as np
from bp_style import *  # noqa: F401,F403

PURPLE = "#B58CD9"
ORANGE = "#F29E4C"
AMBER = "#FFB020"
GOLGI = "#9E8FD0"
LIGHT = "#C3C9D4"
ARROW_GREY = "#7C8596"

LUM_C = np.array([-1.7, -0.85, 0.0])
LUM_W, LUM_H = 8.8, 5.5            # x -6.1..2.7, y -3.6..1.9
SLOT = np.array([-6.1, 0.5, 0.0])
GX, GY0, GY1 = 6.1, -3.0, 1.4      # gauge column and ends
GH = GY1 - GY0
DASH = 0.62                        # dashed line, fraction of the gauge
LOAD0 = 0.45


def p(x, y):
    return np.array([x, y, 0.0])


def label(text, size=30, color=TEXT, **kw):
    return T(text, size=size, color=color, **kw)


def backed(m):
    m.set_stroke(BG, width=7, background=True)
    return m


def cell_outline(width=12.0, height=6.3, center=ORIGIN, opacity=0.18):
    return RoundedRectangle(width=width, height=height, corner_radius=0.7,
                            stroke_color=GREY, stroke_width=4, fill_color=GREY,
                            fill_opacity=opacity).move_to(center)


def carrier(center=ORIGIN, radius=0.43):
    outer = Circle(radius=radius, color=BLUE, stroke_width=5, fill_color=BLUE, fill_opacity=0.07).move_to(center)
    inner = Circle(radius=radius * 0.72, color=BLUE, stroke_width=3).move_to(center)
    return VGroup(outer, inner)


def lysosome(center=p(4.35, -0.1), radius=1.35, with_label=True):
    body = Circle(radius=radius, color=ORANGE, stroke_width=5, fill_color=ORANGE, fill_opacity=0.13).move_to(center)
    shine = Arc(radius=radius * 0.72, start_angle=0.2, angle=1.1, color=ORANGE, stroke_width=3).move_to(center).set_opacity(0.65)
    g = VGroup(body, shine)
    if with_label:
        g.add(label("lysosome", 30, ORANGE).next_to(body, DOWN, buff=0.28))
    return g


def proteasome(center=p(4.5, 2.15), scale=1.0, with_label=True, label_dir=UP):
    body = RoundedRectangle(width=1.5, height=1.0, corner_radius=0.2, stroke_color=GOLD, stroke_width=4,
                            fill_color=GOLD, fill_opacity=0.12).move_to(center)
    caps = VGroup(Line(body.get_left() + UP * 0.38, body.get_left() + DOWN * 0.38, color=GOLD, stroke_width=8),
                  Line(body.get_right() + UP * 0.38, body.get_right() + DOWN * 0.38, color=GOLD, stroke_width=8))
    bore = DashedLine(body.get_left() + RIGHT * 0.12, body.get_right() + LEFT * 0.12, dash_length=0.12, color=GOLD, stroke_width=2)
    g = VGroup(body, caps, bore)
    if with_label:
        g.add(label("proteasome", 28, GOLD).next_to(body, label_dir, buff=0.2))
    return g.scale(scale)


def schem(pos=p(5.9, -3.45)):
    return label("schematic", 28, LIGHT).move_to(pos)


def squig(x0, y0, L=2.0, amp=0.22, waves=3, color=LIGHT, sw=7):
    n = waves * 4
    pts = [p(x0 + L * i / n, y0 + amp * math.sin(i * math.pi / 2)) for i in range(n + 1)]
    return VMobject(color=color, stroke_width=sw).set_points_smoothly(pts)


def tangle(cx, cy, w=0.8, h=0.5, color=LIGHT, sw=7):
    pts = [p(cx + w * math.sin(3 * t + 0.4), cy + h * math.sin(2 * t + 0.9))
           for t in np.linspace(0, 2 * math.pi * 1.25, 36)]
    return VMobject(color=color, stroke_width=sw).set_points_smoothly(pts)


def bob(m, amp=0.06, speed=1.3, phase=0.0, axis=UP):
    st = {"t": phase, "o": 0.0}

    def f(mm, dt):
        st["t"] += dt
        n = amp * math.sin(st["t"] * speed)
        mm.shift(axis * (n - st["o"]))
        st["o"] = n
    m.add_updater(f)
    return m


def flow_arrow(a, b, color, w):
    return Arrow(a, b, buff=0, color=color, stroke_width=w, tip_length=0.16 + 0.018 * w,
                 max_tip_length_to_length_ratio=0.4, max_stroke_width_to_length_ratio=30)


class World:
    """The ER lumen with its translocon slot, drifting unfolded dots, arriving chains and gauge."""

    def __init__(self, load=LOAD0, rate=1.0, stream=False, gauge=True):
        self.load = ValueTracker(load)
        self.rate = ValueTracker(rate)
        self.lumen = RoundedRectangle(width=LUM_W, height=LUM_H, corner_radius=0.5, stroke_color=GREY,
                                      stroke_width=5, fill_color=GREY, fill_opacity=0.18).move_to(LUM_C)
        self.slot = Rectangle(width=0.34, height=1.0, stroke_color=GREY, stroke_width=3,
                              fill_color=BG, fill_opacity=1).move_to(SLOT)
        rng = random.Random(11)
        N = 16
        self.dots = VGroup()
        box = (-5.6, 2.1, -3.1, -0.9)
        for i in range(N):
            d = Dot(radius=0.12, color=LIGHT)
            d.move_to(p(rng.uniform(box[0], box[1]), rng.uniform(box[2], box[3])))
            vel = [rng.choice([-1, 1]) * rng.uniform(0.25, 0.55), rng.choice([-1, 1]) * rng.uniform(0.2, 0.45)]
            d.add_updater(self._drift(vel, i, N, box))
            self.dots.add(d)
        self.stream = VGroup()
        if stream:
            for k in range(3):
                s = squig(-5.7, 0.5, L=0.9, amp=0.13, waves=2)
                s.shift(RIGHT * 0.95 * k)
                s.add_updater(self._flow())
                s.set_z_index(3)
                self.stream.add(s)
        self.gauge = VGroup()
        if gauge:
            box_g = Rectangle(width=0.5, height=GH, stroke_color=TEXT, stroke_width=3).move_to(p(GX, (GY0 + GY1) / 2))
            fill = Rectangle(width=0.5, height=0.05, stroke_width=0, fill_color=YELLOW, fill_opacity=0.9)
            fill.add_updater(self._fill())
            yl = GY0 + DASH * GH
            dash = DashedLine(p(GX - 0.55, yl), p(GX + 0.45, yl), color=RED, stroke_width=4, dash_length=0.1)
            lab = label("unfolded\nload", 28, TEXT).move_to(p(5.8, 2.3))
            self.gauge = VGroup(fill, box_g, dash, lab)
            self.tag = schem()
            self.gauge.add(self.tag)

    def _drift(self, vel, i, N, box):
        load = self.load

        def f(m, dt):
            c = m.get_center()
            c[0] += vel[0] * dt
            c[1] += vel[1] * dt
            if c[0] < box[0] or c[0] > box[1]:
                vel[0] *= -1
            if c[1] < box[2] or c[1] > box[3]:
                vel[1] *= -1
            m.move_to(c)
            m.set_opacity(float(np.clip(load.get_value() * N - i, 0, 1)) * 0.9)
        return f

    def _flow(self):
        rate = self.rate

        def f(m, dt):
            x = m.get_center()[0] + 0.9 * rate.get_value() * dt
            if x > -2.9:
                x -= 2.9
            m.move_to(p(x, 0.5))
            a = float(np.clip((x + 5.9) / 0.6, 0, 1) * np.clip((-2.9 - x) / 0.8, 0, 1))
            m.set_stroke(opacity=a)
        return f

    def _fill(self):
        load = self.load

        def f(m):
            h = max(0.03, load.get_value() * GH)
            m.become(Rectangle(width=0.5, height=h, stroke_width=0, fill_color=YELLOW,
                               fill_opacity=0.9).move_to(p(GX, GY0 + h / 2)))
        return f

    def base(self):
        return [self.lumen, self.slot, self.dots, self.stream]


def make_bell(load, center=p(-5.5, 2.2), size=0.9):
    dome = AnnularSector(inner_radius=0, outer_radius=0.34, angle=PI, start_angle=0,
                         fill_color=AMBER, fill_opacity=0.95, stroke_width=0)
    base = RoundedRectangle(width=0.8, height=0.12, corner_radius=0.05, stroke_width=0,
                            fill_color=AMBER, fill_opacity=1).next_to(dome, DOWN, buff=0)
    clap = Dot(radius=0.07, color=AMBER).next_to(base, DOWN, buff=0.03)
    bell = VGroup(dome, base, clap).scale(size).move_to(center)
    rings = VGroup()
    for k in range(2):
        r = Circle(radius=0.3, color=AMBER, stroke_width=4)
        st = {"t": k * 0.7}

        def f(m, dt, st=st):
            st["t"] += dt
            ph = (st["t"] % 1.4) / 1.4
            on = load.get_value() > DASH
            m.become(Circle(radius=0.3 + 0.35 * ph, color=AMBER, stroke_width=4).move_to(center))
            m.set_stroke(opacity=(1 - ph) * 0.9 if on else 0)
        r.add_updater(f)
        rings.add(r)
    pulse = {"t": 0.0, "s": 1.0}

    def g(m, dt):
        pulse["t"] += dt
        on = load.get_value() > DASH
        s = 1 + (0.13 * math.sin(pulse["t"] * 6.0) if on else 0.0)
        m.scale(s / pulse["s"], about_point=center)
        pulse["s"] = s
    bell.add_updater(g)
    return VGroup(rings, bell)


def flows(thick=1, upr=False):
    """The three arrows of the load equation, drawn inside the lumen."""
    arrival = flow_arrow(p(-6.0, 0.5), p(-3.6, 0.5), ARROW_GREY, {0: 3, 1: 8, 2: 15}[thick])
    a_lab = label("arrival", 28, TEXT).move_to(p(-4.2, 1.05))
    e1 = flow_arrow(p(0.4, 1.2), p(2.6, 1.2), GREEN, 8)
    e1_lab = label("exit 1: folded", 28, GREEN).move_to(p(1.1, 1.55))
    e2 = flow_arrow(p(0.4, 0.3), p(2.5, 0.3), RED, 8)
    e2_lab = label("exit 2: ERAD", 28, RED).move_to(p(1.1, -0.12))
    for lab in (a_lab, e1_lab, e2_lab):
        backed(lab)
    return dict(arrival=arrival, a_lab=a_lab, e1=e1, e1_lab=e1_lab, e2=e2, e2_lab=e2_lab)


def equation_pieces(y=3.5, size=28):
    parts = [label("load change =", size, TEXT), label("entry", size, TEXT),
             label("− (fold-and-export", size, GREEN), label("+ ERAD)", size, RED)]
    g = VGroup(*parts).arrange(RIGHT, buff=0.2).move_to(p(0, y))
    return g


def golgi(center=p(4.1, 1.2), with_label=True):
    rects = VGroup(*[RoundedRectangle(width=1.5 - 0.1 * abs(i - 1), height=0.26, corner_radius=0.13,
                                      stroke_color=GOLGI, stroke_width=3, fill_color=GOLGI,
                                      fill_opacity=0.35).move_to(center + UP * 0.34 * (1 - i)) for i in range(3)])
    g = VGroup(rects)
    if with_label:
        g.add(label("Golgi", 28, GOLGI).next_to(rects, UP, buff=0.18))
    return g


def chapter_map():
    cell = cell_outline(width=12.4, height=6.4, center=p(0, 0.2), opacity=0.12)
    er = RoundedRectangle(width=3.3, height=2.7, corner_radius=0.45, stroke_color=GREY, stroke_width=5,
                          fill_color=GREY, fill_opacity=0.18).move_to(p(-3.9, 0.4))
    er_lab = label("ER", 34, TEXT).move_to(er)
    prot = proteasome(p(4.5, 2.1), 0.9)
    lys = lysosome(p(4.3, 0.1), 1.1, with_label=True)
    arr = Arrow(p(-5.8, -2.0), p(-2.5, -2.0), buff=0, color=BLUE, stroke_width=7)
    clr = Arrow(p(2.5, -2.0), p(5.8, -2.0), buff=0, color=ORANGE, stroke_width=7)
    arr_l = label("arrival", 30, BLUE).move_to(p(-4.15, -2.5))
    clr_l = label("clearance", 30, ORANGE).move_to(p(4.15, -2.5))
    cars = VGroup()
    for k in range(3):
        c = carrier(p(-1.6 + 1.6 * k, 0.1), 0.3)
        st = {"x": -1.6 + 1.6 * k}

        def f(m, dt, st=st):
            nx = st["x"] + 1.5 * dt
            if nx > 3.1:
                nx = -1.9
            m.shift(RIGHT * (nx - st["x"]))
            st["x"] = nx
            m.set_opacity(float(np.clip((nx + 1.9) / 0.5, 0, 1) * np.clip((3.2 - nx) / 0.4, 0, 1)))
        c.add_updater(f)
        cars.add(c)
    return dict(cell=cell, er=er, er_lab=er_lab, prot=prot, lys=lys, arr=arr, clr=clr,
                arr_l=arr_l, clr_l=clr_l, cars=cars)


# ---------------------------------------------------------------- scenes

class S01Link(SpokenScene):
    def construct(self):
        m = chapter_map()
        self.play(Create(m["cell"]), FadeIn(m["er"]), FadeIn(m["er_lab"]), FadeIn(m["prot"]),
                  FadeIn(m["lys"]), FadeIn(m["cars"]), run_time=1.3)
        self.at("how fast does it arrive")
        self.play(GrowArrow(m["arr"]), FadeIn(m["arr_l"]), run_time=0.7)
        self.play(Indicate(m["arr"], color=BLUE, scale_factor=1.06), run_time=0.9)
        self.at("and how fast does it leave")
        self.play(GrowArrow(m["clr"]), FadeIn(m["clr_l"]), run_time=0.7)
        self.play(Indicate(m["clr"], color=ORANGE, scale_factor=1.06), run_time=0.9)
        self.at("Now ask that inside the ER")
        w = World(load=0.15, rate=1.0, stream=True)
        others = VGroup(m["cell"], m["er_lab"], m["prot"], m["lys"], m["cars"], m["arr"], m["clr"], m["arr_l"], m["clr_l"])
        for c in m["cars"]:
            c.clear_updaters()
        self.play(Transform(m["er"], w.lumen), FadeOut(others, run_time=0.6), run_time=1.5)
        self.remove(m["er"])
        self.add(w.lumen)
        self.add(w.slot, w.dots, w.stream)
        self.play(FadeIn(w.slot), run_time=0.6)
        self.at("What happens when unfinished")
        self.play(FadeIn(w.gauge), run_time=0.7)
        self.play(w.load.animate.set_value(LOAD0), run_time=5.2, rate_func=linear)
        self.finish()


class S02Title(TitleCard):
    LESSON = "Quality control and autophagy"
    TITLE = "When the ER Falls Behind"


class S03Arrival(SpokenScene):
    def construct(self):
        w = World(load=LOAD0, stream=False)
        self.add(*w.base())
        self.add(w.gauge)
        y = 0.5
        left = squig(-5.3, y, L=0.5, amp=0.15, waves=1)
        zpts = [p(-4.8 + 0.14 * i, y + a) for i, a in enumerate([0, 0.28, -0.28, 0.28, -0.28, 0.28, 0])]
        zig = VMobject(color=LIGHT, stroke_width=7).set_points_as_corners(zpts)
        right = squig(-3.96, y, L=0.7, amp=0.15, waves=1)
        chain = VGroup(left, zig, right).shift(LEFT * 1.9)
        self.add(chain)
        self.at("Many secreted")
        self.play(chain.animate.shift(RIGHT * 1.9), run_time=3.6, rate_func=smooth)
        self.at("called the")
        trans = backed(label("translocon", 28, TEXT).move_to(p(-4.6, -0.35)))
        self.wait(0.5)
        self.play(FadeIn(trans), run_time=0.6)
        self.at("Chaperones then help")
        bob(chain, 0.07, 1.6)
        self.wait(1.2)
        self.at("grips exposed", lead=1.0)
        self.play(zig.animate.set_color(YELLOW), run_time=0.7)
        bip = chip("BiP", TEAL, 28).move_to(p(-4.38, 1.5))
        self.at("grips exposed")
        self.play(FadeIn(bip), FadeOut(trans), run_time=0.6)
        self.wait(1.0)
        bob(bip, 0.05, 2.0, 1.0)
        # second client with a sugar flag
        client2 = squig(-1.6, -0.3, L=1.8, amp=0.2, waves=3)
        pole = Line(p(0.25, -0.3), p(0.25, 0.2), color=GREEN, stroke_width=4)
        tri = Polygon(p(0.25, 0.2), p(0.25, -0.1), p(0.62, 0.05), color=GREEN, fill_opacity=1, stroke_width=0)
        flag = VGroup(pole, tri)
        lect = chip("lectin chaperone", TEAL, 28).move_to(p(-0.7, 1.25))
        self.at("Lectin chaperones")
        self.play(FadeIn(client2), run_time=0.7)
        self.at("sugar tags")
        self.play(FadeIn(flag, scale=0.5), run_time=0.6)
        self.play(FadeIn(lect), run_time=0.6)
        grab = p(-0.2, 0.6)
        free = p(-0.7, 1.25)
        self.play(lect.animate.move_to(grab), run_time=0.8)
        self.at("supporting repeated folding")
        ring = Circle(radius=1.15, color=TEAL, stroke_width=3).set_stroke(opacity=0.55).move_to(p(-0.7, -0.3))
        orb = Dot(radius=0.12, color=TEAL)
        st = {"a": 0.0}

        def orbit(m, dt):
            st["a"] += 2.4 * dt
            m.move_to(p(-0.7, -0.3) + 1.15 * np.array([math.cos(st["a"]), math.sin(st["a"]), 0]))
        orb.add_updater(orbit)
        self.play(lect.animate.move_to(free), Create(ring), FadeIn(orb), run_time=0.8)
        self.play(lect.animate.move_to(grab), run_time=0.7)
        self.play(lect.animate.move_to(free), run_time=0.7)
        self.play(lect.animate.move_to(grab), run_time=0.7)
        self.at("Folded clients can leave")
        gol = golgi()
        blob = Circle(radius=0.34, color=GREEN, stroke_width=5, fill_color=LIGHT, fill_opacity=0.5).move_to(client2)
        orb.clear_updaters()
        self.play(FadeIn(gol), FadeOut(lect), FadeOut(ring), FadeOut(orb), FadeOut(flag), run_time=0.7)
        self.play(Transform(client2, blob), run_time=0.7)
        self.at("leave for the")
        e1 = flow_arrow(p(0.4, 1.2), p(2.6, 1.2), GREEN, 8)
        self.play(client2.animate.move_to(p(1.2, 1.2)), GrowArrow(e1), run_time=0.8)
        self.play(client2.animate.move_to(p(4.1, 1.2)), run_time=0.9)
        lab = backed(label("exit 1: folded", 28, GREEN).move_to(p(1.1, 1.55)))
        self.play(FadeIn(lab), run_time=0.4)
        self.finish()


class S04Remove(SpokenScene):
    def construct(self):
        w = World(load=LOAD0, stream=False)
        self.add(*w.base())
        self.add(w.gauge)
        cx, cy = -1.5, -0.1
        tang = tangle(cx, cy)
        loop_ring = Circle(radius=1.1, color=TEAL, stroke_width=3).set_stroke(opacity=0.5).move_to(p(cx, cy))
        orb = Dot(radius=0.12, color=TEAL).move_to(p(cx + 1.1, cy))
        st = {"a": 0.0}
        center = {"c": p(cx, cy)}

        def orbit(m, dt):
            st["a"] += 2.4 * dt
            c = center["c"]
            m.move_to(c + 1.1 * np.array([math.cos(st["a"]), math.sin(st["a"]), 0]))
        orb.add_updater(orbit)
        self.add(tang, loop_ring, orb)
        self.at("Some persistently misfolded")
        self.play(FadeIn(tang), FadeIn(loop_ring), run_time=0.8)
        mis = backed(label("misfolded", 28, RED).move_to(p(cx, cy - 1.55)))
        bob(tang, 0.05, 1.5)
        self.at("persistently misfolded clients")
        self.play(FadeIn(mis), run_time=0.5)
        self.at("associated degradation")
        group = VGroup(tang, loop_ring)
        self.play(group.animate.shift(RIGHT * 1.5 + UP * 0.45), mis.animate.shift(RIGHT * 1.5 + UP * 0.45),
                  run_time=1.5, rate_func=smooth)
        center["c"] = center["c"] + RIGHT * 1.5 + UP * 0.45
        self.at("or ERAD")
        tag = backed(label("ERAD", 28, RED).move_to(p(1.5, 1.25)))
        self.play(FadeIn(tag), FadeOut(mis), run_time=0.6)
        # passage
        pas = DashedLine(p(1.7, 0.3), p(4.3, 0.3), color=RED, stroke_width=4, dash_length=0.14)
        hrd = RoundedRectangle(width=0.4, height=1.3, corner_radius=0.12, stroke_color=RED, stroke_width=4,
                               fill_color=RED, fill_opacity=0.35).move_to(p(2.7, 0.3))
        q = label("?", 34, TEXT).move_to(p(3.6, 0.78))
        self.at("During return toward")
        self.play(FadeIn(hrd), Create(pas), FadeOut(tag), run_time=0.9)
        cyt = label("cytosol", 28, LIGHT).move_to(p(3.8, 2.1))
        self.at("the cytosol")
        self.play(FadeIn(cyt), FadeIn(q), run_time=0.6)
        orb.clear_updaters()
        straight = Line(p(-0.4, 0.3), p(2.6, 0.3), color=LIGHT, stroke_width=7)
        self.play(FadeOut(loop_ring), FadeOut(orb), Transform(tang, straight), run_time=1.0)
        self.at("yeast HRD1")
        hlab = backed(label("Hrd1 (yeast)", 28, RED).move_to(p(4.2, 1.45)))
        self.play(FadeIn(hlab), run_time=0.5)
        out = Line(p(0.6, 0.3), p(4.3, 0.3), color=LIGHT, stroke_width=7)
        self.play(Transform(tang, out), run_time=1.3)
        self.at("adds a ubiquitin chain")
        ulab = backed(label("ubiquitin", 28, RED).move_to(p(3.9, -0.35)))
        tags = VGroup(*[Square(side_length=0.26, stroke_width=0, fill_color=RED, fill_opacity=1)
                        .move_to(p(3.1 + 0.34 * i, 0.3)) for i in range(4)])
        self.play(FadeIn(ulab), LaggedStart(*[GrowFromCenter(t) for t in tags], lag_ratio=0.45), run_time=1.8)
        self.wait(0.3)
        self.play(FadeOut(hlab), FadeOut(q), FadeOut(ulab), run_time=0.5)
        self.at("CDC 48")
        cdc = chip("Cdc48", GOLD, 28).move_to(p(4.05, 0.95))
        self.play(FadeIn(cdc, shift=UP * 0.2), run_time=0.7)
        self.at("extracts the tagged")
        out2 = Line(p(3.1, 0.3), p(5.0, 0.3), color=LIGHT, stroke_width=7)
        tags2 = VGroup(*[Square(side_length=0.26, stroke_width=0, fill_color=RED, fill_opacity=1)
                         .move_to(p(3.35 + 0.34 * i, 0.3)) for i in range(4)])
        self.play(Transform(tang, out2), Transform(tags, tags2), cdc.animate.move_to(p(4.05, 0.95)), run_time=1.2)
        prot = proteasome(p(4.3, -1.75), 1.0, with_label=False)
        plab = label("proteasome", 26, GOLD).move_to(p(3.8, -3.3))
        self.play(FadeIn(prot), run_time=0.6)
        self.at("tagged client for destruction")
        carry = VGroup(tang, tags, cdc)
        self.play(carry.animate.move_to(p(4.3, -0.9)), run_time=1.0)
        self.at("by the proteasome")
        self.play(FadeIn(plab), FadeOut(cdc), VGroup(tang, tags).animate.move_to(p(4.3, -1.75)).scale(0.6), run_time=0.8)
        pieces = VGroup(*[Line(p(3.6 + 0.4 * i, -2.65), p(3.82 + 0.4 * i, -2.65), color=LIGHT, stroke_width=7) for i in range(4)])
        self.play(FadeOut(tags), Transform(tang, pieces), run_time=0.6)
        ex2 = flow_arrow(p(0.4, 0.3), p(1.6, 0.3), RED, 8)
        ex2l = backed(label("exit 2: ERAD", 28, RED).move_to(p(1.0, -0.12)))
        self.play(GrowArrow(ex2), FadeIn(ex2l), run_time=0.5)
        self.finish()


def stage(scene, w, thick=1, eq=0):
    fl = flows(thick)
    return fl


class S05Load(SpokenScene):
    def construct(self):
        w = World(load=LOAD0, rate=1.0, stream=True)
        self.add(*w.base())
        self.add(w.gauge)
        bell = make_bell(w.load)
        fl = flows(1)
        eq = equation_pieces()
        self.at("count the flows")
        self.play(FadeIn(eq[0]), run_time=0.8)
        self.at("Arrival is ER")
        self.play(GrowArrow(fl["arrival"]), FadeIn(fl["a_lab"]), FadeIn(eq[1]), run_time=0.9)
        self.at("Clearance is folding and export")
        self.play(GrowArrow(fl["e1"]), FadeIn(fl["e1_lab"]), FadeIn(eq[2]), run_time=0.9)
        self.at("plus removal by ERAD")
        self.play(GrowArrow(fl["e2"]), FadeIn(fl["e2_lab"]), FadeIn(eq[3]), run_time=0.9)
        self.at("When chains arrive faster")
        thick = flow_arrow(p(-6.0, 0.5), p(-3.6, 0.5), ARROW_GREY, 15)
        self.play(Transform(fl["arrival"], thick), w.rate.animate.set_value(2.2), run_time=1.2)
        self.at("than both exits")
        self.play(Indicate(fl["e1"], color=GREEN), Indicate(fl["e2"], color=RED), run_time=1.0)
        self.at("unfolded proteins build up")
        self.add(bell)
        self.play(w.load.animate.set_value(0.88), run_time=4.0, rate_func=linear)
        self.at("The ER senses that stress")
        self.play(Indicate(bell[1], color=AMBER, scale_factor=1.3), run_time=1.2)
        self.finish()


class S06Predict(SpokenScene):
    def construct(self):
        w = World(load=0.88, rate=2.2, stream=True)
        fl = flows(2)
        eq = equation_pieces()
        bell = make_bell(w.load)
        self.add(*w.base(), w.gauge)
        self.add(*[fl[k] for k in ("arrival", "a_lab", "e1", "e1_lab", "e2", "e2_lab")], eq, bell)
        self.at("This alarm is the unfolded")
        upr = label("unfolded protein response (UPR)", 28, AMBER)
        upr.move_to(p(-4.85 + upr.width / 2, 2.38))
        self.play(FadeIn(upr), Indicate(bell[1], color=AMBER, scale_factor=1.3), run_time=1.0)
        self.at("Look at the equation")
        self.play(Indicate(eq, color=YELLOW, scale_factor=1.05), run_time=1.6)
        qn = label("Which flows could it change?", 30, TEXT, weight=BOLD).move_to(p(0, 2.95))
        self.at("Which flows could")
        self.play(FadeIn(qn, shift=DOWN * 0.1), run_time=0.7)

        def ring(target, buff=0.18):
            r = SurroundingRectangle(target, color=TEXT, buff=buff, corner_radius=0.2, stroke_width=3)
            return r
        self.at("could the response change")
        r1 = ring(VGroup(fl["arrival"], fl["a_lab"]))
        self.play(Create(r1), run_time=0.6)
        self.play(FadeOut(r1), run_time=0.3)
        r2 = ring(VGroup(fl["e1"], fl["e1_lab"]))
        self.play(Create(r2), run_time=0.6)
        self.play(FadeOut(r2), run_time=0.3)
        r3 = ring(VGroup(fl["e2"], fl["e2_lab"]))
        self.play(Create(r3), run_time=0.6)
        self.play(FadeOut(r3), run_time=0.3)
        self.finish()


class S07Pause(NarratedScene):
    def construct(self):
        w = World(load=0.88, rate=2.2, stream=True)
        fl = flows(2)
        eq = equation_pieces()
        bell = make_bell(w.load)
        upr = label("unfolded protein response (UPR)", 28, AMBER)
        upr.move_to(p(-4.85 + upr.width / 2, 2.38))
        qn = label("Which flows could it change?", 30, TEXT, weight=BOLD).move_to(p(0, 2.95))
        self.add(*w.base(), w.gauge)
        self.add(*[fl[k] for k in ("arrival", "a_lab", "e1", "e1_lab", "e2", "e2_lab")], eq, bell, upr, qn)
        self.wait(4.5)


class S08Reveal(SpokenScene):
    def construct(self):
        w = World(load=0.88, rate=2.2, stream=True)
        fl = flows(2)
        eq = equation_pieces()
        bell = make_bell(w.load)
        upr = label("unfolded protein response (UPR)", 28, AMBER)
        upr.move_to(p(-4.85 + upr.width / 2, 2.38))
        self.add(*w.base(), w.gauge)
        self.add(*[fl[k] for k in ("arrival", "a_lab", "e1", "e1_lab", "e2", "e2_lab")], eq, bell, upr)
        self.at("It can change both sides")
        self.play(Indicate(bell[1], color=AMBER, scale_factor=1.3), run_time=1.0)
        self.at("In mammals")
        line = Line(p(-5.5, 1.85), p(-5.5, 0.65), color=AMBER, stroke_width=5)
        self.play(Create(line), run_time=0.8)
        self.at("slows the making")
        thin = flow_arrow(p(-6.0, 0.5), p(-3.6, 0.5), ARROW_GREY, 3)
        perk = backed(label("PERK: slower synthesis", 28, AMBER).move_to(p(-3.0, -0.18)))
        self.play(Transform(fl["arrival"], thin), w.rate.animate.set_value(0.45), FadeIn(perk), run_time=1.4)
        self.at("so less arrives")
        self.play(Indicate(fl["a_lab"], color=TEXT), run_time=1.0)
        self.at("The response also increases folding helpers")
        helpers = VGroup(*[chip("", TEAL, 22, pad=0.1) if False else
                           RoundedRectangle(width=0.7, height=0.4, corner_radius=0.1, stroke_color=TEAL, stroke_width=3,
                                            fill_color=TEAL, fill_opacity=0.5).move_to(pos)
                           for pos in (p(-1.6, -1.3), p(-0.3, -1.9), p(-3.2, -1.9), p(-2.2, -2.6))])
        self.play(LaggedStart(*[GrowFromCenter(h) for h in helpers], lag_ratio=0.3), run_time=1.6)
        for h in helpers:
            bob(h, 0.07, 1.7, random.random() * 3)
        e1_thick = flow_arrow(p(0.4, 1.2), p(2.6, 1.2), GREEN, 15)
        more_h = backed(label("more helpers", 28, TEAL).move_to(p(1.1, 1.55)))
        self.play(Transform(fl["e1"], e1_thick), Transform(fl["e1_lab"], more_h), run_time=1.0)
        self.at("removal machinery")
        e2_thick = flow_arrow(p(0.4, 0.3), p(2.5, 0.3), RED, 15)
        more_r = backed(label("more removal", 28, RED).move_to(p(1.1, -0.12)))
        self.play(Transform(fl["e2"], e2_thick), Transform(fl["e2_lab"], more_r), run_time=1.0)
        self.at("Less in and more out")
        self.play(Indicate(fl["arrival"], color=TEXT, scale_factor=1.03), run_time=0.8)
        self.at("let the load fall")
        self.play(w.load.animate.set_value(0.38), run_time=1.9, rate_func=smooth)
        self.finish()


class S09Branches(SpokenScene):
    def construct(self):
        w = World(load=0.38, rate=0.45, stream=True)
        self.add(*w.base(), w.gauge)
        arrival = flow_arrow(p(-6.0, 0.5), p(-3.6, 0.5), ARROW_GREY, 8)
        a_lab = backed(label("arrival", 28, TEXT).move_to(p(-4.2, 1.05)))
        e1 = flow_arrow(p(0.4, 1.2), p(2.6, 1.2), GREEN, 8)
        e2 = flow_arrow(p(0.4, 0.3), p(2.5, 0.3), RED, 8)
        bell = make_bell(w.load)
        self.add(arrival, a_lab, e1, e2, bell)
        self.at("Mammals have three branches")
        mk = lambda t: chip(t, AMBER, 28)
        ire, perk, atf = mk("IRE1"), mk("PERK"), mk("ATF6")
        ire.move_to(p(-4.7, 2.45)); perk.move_to(p(-2.7, 2.45)); atf.move_to(p(-0.7, 2.45))
        self.play(FadeOut(bell), FadeIn(ire), FadeIn(perk), FadeIn(atf), run_time=1.0)
        self.play(Indicate(ire, color=AMBER), run_time=0.5)
        self.play(Indicate(perk, color=AMBER), run_time=0.5)
        self.play(Indicate(atf, color=AMBER), run_time=0.5)
        # IRE1 / XBP1
        halfL = Rectangle(width=1.5, height=0.26, stroke_width=0, fill_color=LIGHT, fill_opacity=0.9).move_to(p(-5.35, 3.0))
        mid = Rectangle(width=0.5, height=0.26, stroke_width=0, fill_color=YELLOW, fill_opacity=1).move_to(p(-4.35, 3.0))
        halfR = Rectangle(width=1.5, height=0.26, stroke_width=0, fill_color=LIGHT, fill_opacity=0.9).move_to(p(-3.35, 3.0))
        rib = VGroup(halfL, mid, halfR)
        xl = backed(label("XBP1 mRNA", 28, TEXT).move_to(p(-0.6, 3.3)))
        self.at("IRE1 splices")
        self.play(FadeIn(rib), run_time=0.7)
        self.at("XBP1 message")
        self.play(FadeIn(xl), run_time=0.5)
        self.play(mid.animate.shift(UP * 0.5).set_opacity(0), run_time=0.7)
        self.play(halfL.animate.shift(RIGHT * 0.25), halfR.animate.shift(LEFT * 0.25), run_time=0.7)
        self.at("slows translation")
        self.play(Indicate(perk, color=AMBER, scale_factor=1.15), FadeOut(rib), FadeOut(xl), run_time=0.6)
        thin = flow_arrow(p(-6.0, 0.5), p(-3.6, 0.5), ARROW_GREY, 3)
        self.play(Transform(arrival, thin), run_time=1.2)
        self.at("A TF6 travels")
        gol = golgi()
        nuc = Circle(radius=0.6, color=GREY, stroke_width=4).move_to(p(3.3, 3.1))
        ves = Circle(radius=0.2, color=AMBER, stroke_width=4, fill_color=AMBER, fill_opacity=0.5).move_to(p(0.3, 2.45))
        self.play(FadeIn(gol), FadeIn(ves), run_time=0.8)
        self.play(ves.animate.move_to(p(2.9, 2.3)), run_time=1.4)
        self.at("where proteases release")
        self.play(ves.animate.move_to(p(4.1, 1.2)), run_time=0.7)
        x1 = Line(p(3.8, 1.5), p(4.4, 1.0), color=TEXT, stroke_width=5)
        x2 = Line(p(3.8, 1.0), p(4.4, 1.5), color=TEXT, stroke_width=5)
        sc = VGroup(x1, x2)
        self.play(Create(sc), run_time=0.7)
        self.wait(0.3)
        self.at("transcription factor domain")
        frag = Square(side_length=0.22, stroke_width=0, fill_color=AMBER, fill_opacity=1).move_to(p(4.1, 1.2))
        self.play(FadeOut(sc), FadeOut(ves), FadeIn(nuc), FadeIn(frag), run_time=0.6)
        nlab = backed(label("nucleus", 28, LIGHT).move_to(p(3.3, 3.1)))
        self.play(frag.animate.move_to(nuc.get_center() + DOWN * 0.1), run_time=1.2)
        self.play(FadeIn(nlab), run_time=0.4)
        self.at("Yeast relies on one")
        yeast = Ellipse(width=2.0, height=1.5, color=GREY, stroke_width=4, fill_color=GREY, fill_opacity=0.18).move_to(p(4.2, -1.6))
        bud = Circle(radius=0.3, color=GREY, stroke_width=4, fill_color=GREY, fill_opacity=0.18).move_to(p(5.05, -1.05))
        ir = chip("Ire1", AMBER, 28).move_to(p(4.2, -1.6))
        ylab = label("yeast", 28, LIGHT).move_to(p(4.2, -2.75))
        self.play(FadeOut(VGroup(gol, nuc, frag, nlab)), FadeIn(yeast), FadeIn(bud), FadeIn(ylab), run_time=0.9)
        self.play(FadeIn(ir, scale=0.6), run_time=0.8)
        self.play(Indicate(ir, color=AMBER, scale_factor=1.2), run_time=0.8)
        self.finish()


class S10Return(SpokenScene):
    def construct(self):
        w = World(load=0.38, rate=0.9, stream=True)
        self.add(*w.base(), w.gauge)
        arrival = flow_arrow(p(-6.0, 0.5), p(-3.6, 0.5), ARROW_GREY, 5)
        e2 = flow_arrow(p(0.4, 0.3), p(2.5, 0.3), RED, 8)
        loop = Arc(radius=0.9, start_angle=0.4, angle=TAU * 0.8, color=TEAL, stroke_width=4).move_to(p(-1.6, -1.55))
        loop.add_tip(tip_length=0.22)
        sens = VGroup(*[chip(t, AMBER, 24, pad=0.14) for t in ("IRE1", "PERK", "ATF6")]).arrange(RIGHT, buff=0.3).move_to(p(-3.2, 2.45))
        self.add(arrival, e2, loop, sens)
        self.at("The response buys time")
        self.play(Indicate(sens, color=AMBER, scale_factor=1.08), run_time=1.2)
        self.at("has limits")
        dim = {"o": 0.18}
        self.play(w.load.animate.set_value(0.97), w.lumen.animate.set_stroke(opacity=0.45).set_fill(opacity=0.08),
                  w.rate.animate.set_value(2.0), run_time=2.4)
        self.at("Persistent stress can also")
        cd = backed(label("cell death", 34, LIGHT, weight=BOLD).move_to(p(4.3, -0.55)))
        cd2 = backed(label("if stress persists", 24, LIGHT).move_to(p(4.3, -1.1)))
        self.at("cell death")
        self.play(FadeIn(cd), FadeIn(cd2), run_time=0.8)
        self.wait(0.6)
        self.at("The ER can retry")
        self.play(FadeOut(cd), FadeOut(cd2), w.load.animate.set_value(0.38), w.rate.animate.set_value(0.9),
                  w.lumen.animate.set_stroke(opacity=1).set_fill(opacity=0.18), run_time=1.0)
        l1 = backed(label("retry", 30, TEAL).move_to(p(-1.6, 0.1)))
        self.play(FadeIn(l1), Indicate(loop, color=TEAL), run_time=0.8)
        self.at("remove them")
        l2 = backed(label("remove", 30, RED).move_to(p(1.4, -0.2)))
        self.play(FadeOut(l1), FadeIn(l2), Indicate(e2, color=RED), run_time=0.8)
        self.at("slow arrival")
        l3 = backed(label("slow arrival", 30, TEXT).move_to(p(-4.6, 1.05)))
        self.play(FadeOut(l2), FadeIn(l3), Indicate(arrival, color=TEXT), run_time=0.8)
        self.at("raise capacity")
        l4 = backed(label("raise capacity", 30, AMBER).move_to(p(-3.2, 3.2)))
        self.play(FadeOut(l3), FadeIn(l4), Indicate(sens, color=AMBER), run_time=0.8)
        self.at("These moves rebalance")
        m = chapter_map()
        others = VGroup(m["cell"], m["er_lab"], m["prot"], m["lys"], m["arr"], m["clr"], m["arr_l"], m["clr_l"])
        er_target = m["er"]
        clutter = VGroup(w.slot, w.dots, w.stream, w.gauge, loop, sens, arrival, e2, l4)
        for d in w.dots:
            d.clear_updaters()
        for s in w.stream:
            s.clear_updaters()
        self.play(Transform(w.lumen, er_target), FadeOut(clutter, run_time=0.6),
                  FadeIn(others), FadeIn(m["cars"]), run_time=1.6)
        self.at("arrival and clearance")
        self.play(Indicate(m["arr"], color=BLUE, scale_factor=1.06), Indicate(m["clr"], color=ORANGE, scale_factor=1.06),
                  run_time=1.1)
        self.at("When folding falls behind")
        self.play(Indicate(m["arr"], color=BLUE, scale_factor=1.06), run_time=0.9)
        self.at("reduce arrival")
        thin = Arrow(p(-5.8, -2.0), p(-2.5, -2.0), buff=0, color=BLUE, stroke_width=3)
        self.play(Transform(m["arr"], thin), run_time=1.0)
        self.at("expand capacity")
        thick = Arrow(p(2.5, -2.0), p(5.8, -2.0), buff=0, color=ORANGE, stroke_width=14)
        self.play(Transform(m["clr"], thick), run_time=1.0)
        self.finish()


class S11End(EndCard):
    LINE = "When folding falls behind, reduce arrival and expand capacity."
