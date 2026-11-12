"""Pushed From the Source: pressure flow in phloem.

COLOR MAP (identical to chapter 1)
  BLUE   = xylem water, water droplets
  AMBER  = phloem / positive pressure / a push
  GOLD   = sucrose
  RED    = tension, negative pressure, objection zone
  GREY   = air, vapour, structure
  GREEN  = leaf cells (structure only)
  YELLOW = questions and crosses
"""
import os
import random
import numpy as np
from bp_style import *  # noqa: F401,F403

AMBER = "#F5A623"
LEAF = "#3B8A57"
BARK = "#6B5B4B"
PSI = "Ψ"


class LiveScene(SpokenScene):
    """The same restrained drifting field used in chapter 1."""
    def setup(self):
        super().setup()
        rng = random.Random(os.environ.get("KX_SCENE_ID", "x"))
        motes = VGroup(*[
            Circle(radius=rng.uniform(0.23, 0.40), stroke_width=0,
                   fill_color=TEXT, fill_opacity=0.13).move_to(
                [rng.uniform(-6.6, 6.6), rng.uniform(-3.7, 3.7), 0])
            for _ in range(28)
        ])
        phase = [rng.uniform(0, 7) for _ in motes]
        speed = [rng.uniform(0.22, 0.45) for _ in motes]
        base = [m.get_center().copy() for m in motes]
        motes.tm = 0.0

        def drift(group, dt):
            group.tm += dt
            for i, dot in enumerate(group):
                y = ((base[i][1] + 3.8 + speed[i] * group.tm) % 7.6) - 3.8
                dot.move_to([base[i][0] + 0.25 * np.sin(group.tm * 0.7 + phase[i]), y, 0])
        motes.add_updater(drift)
        motes.set_z_index(-20)
        self.add(motes)


def flow(points, n=8, color=AMBER, radius=0.1, speed=0.12, opacity=0.95):
    """Looping particles along a polyline."""
    points = [np.array(p, float) for p in points]
    lengths = [float(np.linalg.norm(points[i + 1] - points[i])) for i in range(len(points) - 1)]
    total = sum(lengths)

    def point_at(u):
        d = u * total
        for i, length in enumerate(lengths):
            if d <= length:
                return points[i] + (points[i + 1] - points[i]) * (d / length if length else 0)
            d -= length
        return points[-1]

    dots = VGroup(*[Dot(points[0], radius=radius, color=color) for _ in range(n)])
    dots.tm = 0.0

    def move(group, dt):
        group.tm += dt
        for i, dot in enumerate(group):
            u = (group.tm * speed + i / n) % 1
            dot.move_to(point_at(u))
            dot.set_opacity(opacity * min(1, u * 7, (1 - u) * 7))
    dots.add_updater(move)
    move(dots, 0)
    return dots


def sugar(center, scale=1.0):
    """A filled hexagonal badge, the chapter-1 sucrose symbol."""
    return RegularPolygon(6, radius=0.16 * scale).set_stroke(GOLD, 2).set_fill(GOLD, 0.92).move_to(center)


def heart():
    return ParametricFunction(
        lambda t: np.array([16 * np.sin(t) ** 3,
                            13 * np.cos(t) - 5 * np.cos(2 * t) - 2 * np.cos(3 * t) - np.cos(4 * t), 0]) * 0.055,
        t_range=[0, TAU]).set_fill(GREY, 0.45).set_stroke(GREY, 4)


def cross(center, size=0.65, color=YELLOW, width=8):
    c = np.array(center, float)
    return VGroup(Line(c + [-size, -size, 0], c + [size, size, 0]),
                  Line(c + [-size, size, 0], c + [size, -size, 0])).set_stroke(color, width)


def pressure_gauge(x, bottom, top, zero, tracker, color=AMBER, width=0.7):
    """Chapter-1 gauge geometry, with fill tied to tracker."""
    frame = Rectangle(width=width, height=top - bottom, stroke_color=GREY, stroke_width=3).move_to([x, (top + bottom) / 2, 0])
    zero_line = Line([x - 0.55, zero, 0], [x + 0.55, zero, 0], color=TEXT, stroke_width=3)
    zero_label = T("0", 28, TEXT).next_to(zero_line, RIGHT, buff=0.08)

    def fill_shape():
        y = tracker.get_value()
        h = max(abs(y - zero), 0.002)
        col = RED if y < zero else color
        return Rectangle(width=width, height=h, stroke_width=0, fill_color=col, fill_opacity=0.88).move_to([x, (y + zero) / 2, 0])
    return VGroup(frame, zero_line, zero_label), always_redraw(fill_shape)


def leaf(center, angle=0, width=2.0, height=1.05):
    body = Ellipse(width=width, height=height).rotate(angle).set_stroke(GREEN, 4).set_fill(LEAF, 0.62).move_to(center)
    vein = Line(body.get_left() + RIGHT * 0.2, body.get_right() + LEFT * 0.2, color=GREEN, stroke_width=3).rotate(angle, about_point=body.get_center())
    return VGroup(body, vein)


def droplet(center, scale=1.0):
    d = VGroup(Circle(radius=0.11 * scale, stroke_width=0, fill_color=BLUE, fill_opacity=1),
               Triangle().scale(0.12 * scale).set_stroke(BLUE, 0).set_fill(BLUE, 1).shift(UP * 0.11 * scale))
    return d.move_to(center)


def bulb_world():
    """The fixed A/B apparatus used unchanged in scenes 3–5."""
    bath = RoundedRectangle(corner_radius=0.16, width=11.5, height=4.9, stroke_color=BLUE, stroke_width=4,
                            fill_color=BLUE, fill_opacity=0.12).move_to([0, -0.55, 0])
    surface = Line([-5.7, 1.9, 0], [5.7, 1.9, 0], color=BLUE, stroke_width=5)
    tube = RoundedRectangle(corner_radius=0.22, width=5.3, height=0.72, stroke_color=AMBER, stroke_width=5,
                            fill_color=AMBER, fill_opacity=0.14).move_to([0, -0.25, 0])
    left = DashedVMobject(Circle(radius=1.45, color=TEXT, stroke_width=5).move_to([-3.7, -0.25, 0]), num_dashes=34)
    right = DashedVMobject(Circle(radius=1.45, color=TEXT, stroke_width=5).move_to([3.7, -0.25, 0]), num_dashes=34)
    labels = VGroup(T("A", 36, TEXT).move_to([-3.7, -2.35, 0]), T("B", 36, TEXT).move_to([3.7, -2.35, 0]))
    return bath, surface, tube, left, right, labels


def source_sink_plant():
    """Fixed plant landmarks, shared by scenes 6–8 and 17."""
    x = -1.1
    soil = Rectangle(width=11.7, height=0.75, stroke_color=BARK, fill_color=BARK, fill_opacity=0.42).move_to([0, -3.05, 0])
    stem = Line([x, -2.7, 0], [x, 2.8, 0], color=GREEN, stroke_width=11)
    xylem = Line([x - 0.14, -2.7, 0], [x - 0.14, 2.8, 0], color=BLUE, stroke_width=5)
    phloem = Line([x + 0.14, -2.7, 0], [x + 0.14, 2.8, 0], color=AMBER, stroke_width=5)
    source = leaf([-2.25, 0.65, 0], angle=0.3, width=2.25, height=1.15)
    branch = Line([x, 0.55, 0], [-1.65, 0.65, 0], color=GREEN, stroke_width=7)
    top = VGroup(*[leaf([x + dx, 2.9 + dy, 0], angle=a, width=1.35, height=0.72)
                   for dx, dy, a in [(-0.55, -0.05, 0.45), (0.4, 0.15, -0.4)]])
    roots = VGroup(*[Line([x, -2.7, 0], [x + dx, -3.55, 0], color=GREY, stroke_width=4) for dx in (-1.15, -0.5, 0.35, 1.0)])
    return VGroup(soil, stem, branch, top, roots, xylem, phloem, source), source, xylem, phloem


def low_gauge(x, y, high=False):
    track = ValueTracker(y + (1.45 if high else 0.55))
    frame, fill = pressure_gauge(x, y, y + 1.8, y + 0.25, track, AMBER, 0.55)
    return track, frame, fill


def opaque_chip(text, color, size, pad=0.3):
    """Readable chip over a busy diagram: dark backing, coloured rim and text."""
    front = chip(text, color, size, pad=pad, fill_opacity=0.16)
    back = RoundedRectangle(corner_radius=0.14, width=front.width, height=front.height,
                            stroke_width=0, fill_color=BG, fill_opacity=0.94)
    return VGroup(back, front)


def vine_world(long=False):
    """Morning-glory stage with a fixed root and a path that can lengthen."""
    root = VGroup(*[Line([-4.8, -2.55, 0], [-4.8 + dx, -3.45, 0], color=GREY, stroke_width=4) for dx in (-0.8, -0.25, 0.4, 0.9)])
    ground = Line([-6.2, -2.55, 0], [6.1, -2.55, 0], color=BARK, stroke_width=5)
    end_x = 4.8 if long else 1.5
    path = VMobject().set_points_smoothly([[-4.8, -2.5, 0], [-3.8, -1.3, 0], [-2.8, 0.0, 0], [-1.4, 1.4, 0], [0.2, 2.45, 0], [end_x, 2.55, 0]]).set_stroke(AMBER, 8)
    support = Line([-5.1, -2.45, 0], [5.3, 3.0, 0], color=GREY, stroke_width=3)
    leaves = VGroup(leaf([-2.7, -0.1, 0], 0.35, 1.25, 0.65), leaf([-1.2, 1.35, 0], -0.35, 1.35, 0.68), leaf([0.4, 2.45, 0], 0.25, 1.45, 0.72))
    if long:
        leaves.add(leaf([3.8, 2.55, 0], -0.25, 1.5, 0.75))
    flower = VGroup(Arc(radius=0.52, start_angle=0.1, angle=PI - 0.2, color=TEAL, stroke_width=5),
                    Line([-0.35, 0, 0], [0.35, 0, 0], color=TEAL, stroke_width=4)).rotate(-0.2).move_to([end_x, 2.78, 0])
    return VGroup(ground, support, root, path, leaves, flower), path, leaves


def dial(center=(4.7, 0.0), needle_angle=-2.4):
    c = np.array([center[0], center[1], 0.0])
    arc = Arc(radius=1.25, start_angle=PI, angle=-PI, color=GREY, stroke_width=7, arc_center=c)
    red = Arc(radius=1.25, start_angle=-0.55, angle=0.55, color=RED, stroke_width=9, arc_center=c)
    needle = Line(c, c + 1.05 * np.array([np.cos(needle_angle), np.sin(needle_angle), 0])).set_stroke(AMBER, 7)
    hub = Dot(c, radius=0.12, color=TEXT)
    return VGroup(arc, red, needle, hub), needle, c


class S00Title(TitleCard):
    LESSON = "Moving Water and Sugar in Plants"
    TITLE = "Pushed From the Source"

    def construct(self):
        brand = T("BIOCHEMISTRYPEDIA", 20, TEAL, weight=BOLD).move_to([0, 3.35, 0])
        lesson = T(self.LESSON.upper(), 22, GREY).move_to([0, 2.85, 0])
        title = T(self.TITLE, 50, TEXT, font=TITLE_FONT).move_to([0, 2.15, 0])
        stem = Line([0, -2.8, 0], [0, 1.2, 0], color=GREEN, stroke_width=9)
        xl = Line([-0.12, -2.8, 0], [-0.12, 1.2, 0], color=BLUE, stroke_width=6)
        ph = Line([0.12, -2.8, 0], [0.12, 1.2, 0], color=AMBER, stroke_width=6)
        lf = VGroup(leaf([-1.0, 0.45, 0], 0.35, 1.8, 0.9), leaf([0.95, -0.55, 0], -0.35, 1.8, 0.9))
        roots = VGroup(*[Line([0, -2.7, 0], [dx, -3.35, 0], color=GREY, stroke_width=3) for dx in (-1.0, -0.35, 0.45, 1.0)])
        symbols = VGroup(T(PSI, 34), VGroup(T(PSI, 34), T("s", 22).shift([0.25, -0.18, 0])),
                         VGroup(T(PSI, 34), T("p", 22).shift([0.25, -0.18, 0]))).arrange(RIGHT, buff=0.7).move_to([3.7, -2.3, 0])
        self.play(FadeIn(brand), FadeIn(lesson), Write(title), run_time=0.8)
        self.play(GrowFromEdge(stem, DOWN), Create(xl), Create(ph), FadeIn(lf), FadeIn(roots), run_time=1.0)
        self.play(FadeIn(symbols), run_time=0.4)
        self.wait(0.35)
        self.play(FadeOut(VGroup(brand, lesson, title, stem, xl, ph, lf, roots, symbols)), run_time=0.4)
        self.finish()


class S01Hook(LiveScene):
    def construct(self):
        plant, src, _, ph = source_sink_plant()
        plant.shift(LEFT * 1.2)
        self.play(FadeIn(plant), run_time=0.8)
        glow = src.copy().set_fill(GOLD, 0.3).set_stroke(GOLD, 7)
        self.at("Sugar made")
        self.play(FadeIn(glow, scale=0.9), run_time=0.6)
        down = flow([[-2.3, 0.7, 0], [-2.15, 0.7, 0], [-2.15, -2.7, 0], [-3.0, -3.35, 0]], 7, GOLD, 0.13, 0.14)
        up = flow([[-2.3, 0.7, 0], [-2.15, 0.7, 0], [-2.15, 2.7, 0], [-1.4, 3.0, 0]], 6, GOLD, 0.13, 0.14)
        self.add(down)
        self.at("shoot tip above")
        self.add(up)
        h = heart().move_to([3.7, 1.7, 0])
        hx = cross(h.get_center(), 0.8)
        level = ValueTracker(-1.3)
        gf, fill = pressure_gauge(3.7, -2.5, 0.9, 0.2, level, RED)
        gx = cross([3.7, -0.8, 0], 0.9)
        self.at("What moves")
        self.play(FadeIn(h), Create(hx), FadeIn(gf), FadeIn(fill), Create(gx), run_time=0.8)
        self.at("nothing pulling")
        q = T("?", 150, YELLOW, weight=BOLD).move_to([5.6, 1.7, 0])
        self.play(FadeIn(q, scale=0.5), run_time=0.5)
        self.play(Indicate(q, color=YELLOW, scale_factor=1.18), run_time=0.8)
        self.finish()


class S02Link(LiveScene):
    def construct(self):
        # Left: the chapter-1 xylem column and its negative gauge.
        xyl = RoundedRectangle(corner_radius=0.18, width=1.35, height=5.5, stroke_color=BLUE, stroke_width=5,
                               fill_color=BLUE, fill_opacity=0.12).move_to([-4.6, -0.25, 0])
        drops = flow([[-4.6, -2.75, 0], [-4.6, 2.25, 0]], 7, BLUE, 0.13, 0.12)
        neg = ValueTracker(-1.8)
        ng, nf = pressure_gauge(-2.9, -2.7, 2.45, 1.0, neg, RED)
        self.play(FadeIn(xyl), run_time=0.5)
        self.add(drops, ng, nf)
        self.at("pulled toward dry air")
        vap = flow([[-4.6, 2.2, 0], [-3.8, 3.2, 0]], 5, GREY, 0.12, 0.13, 0.7)
        self.add(vap)
        pulled = T("pulled", 36, RED).move_to([-3.7, 3.25, 0])
        self.play(FadeIn(pulled), run_time=0.5)
        # Right: a living tube, visibly cellular.
        cells = VGroup(*[RoundedRectangle(corner_radius=0.18, width=1.7, height=1.45, stroke_color=AMBER, stroke_width=4,
                                          fill_color=AMBER, fill_opacity=0.12).move_to([0.6 + 1.7 * i, 0.35, 0]) for i in range(3)])
        cyto = VGroup(*[Circle(radius=0.32, stroke_color=GREEN, stroke_width=3, fill_color=GREEN, fill_opacity=0.18).move_to([0.6 + 1.7 * i, 0.35, 0]) for i in range(3)])
        self.at("Sugar rides")
        self.play(FadeIn(cells), FadeIn(cyto), run_time=0.8)
        sf = flow([[0.0, 0.35, 0], [4.6, 0.35, 0]], 8, GOLD, 0.11, 0.13)
        self.add(sf)
        self.at("living sieve tubes")
        label = T("living sieve tube", 32, AMBER).move_to([2.3, 1.65, 0])
        self.play(FadeIn(label), run_time=0.5)
        roots = VGroup(*[Line([4.8, -0.35, 0], [4.8 + d, -2.4, 0], color=GREY, stroke_width=4) for d in (-0.9, -0.35, 0.4, 0.95)])
        self.at("nothing evaporates")
        no_vap = cross([5.3, 2.3, 0], 0.75)
        self.play(FadeIn(roots), Create(no_vap), run_time=0.7)
        self.finish()


class S03Munch(LiveScene):
    def construct(self):
        credit = T("Ernst Münch, 1930", 32, TEXT).move_to([0, 3.35, 0])
        self.play(FadeIn(credit), run_time=0.5)
        bath, surface, tube, left, right, labels = bulb_world()
        self.at("two bulbs")
        self.play(FadeIn(left), FadeIn(right), run_time=0.7)
        self.at("joined by a tube")
        self.play(Create(tube), FadeIn(labels), run_time=0.7)
        self.at("wrapped in a membrane")
        mem = T("membrane", 28, TEXT).move_to([0, -3.3, 0])
        rule = T("water passes  •  sugar does not", 26, TEXT).move_to([0, -3.68, 0])
        self.play(Indicate(VGroup(left, right), color=TEXT, scale_factor=1.04), FadeIn(mem), run_time=0.7)
        self.at("lets water through")
        self.play(FadeIn(rule), run_time=0.5)
        self.at("Both sit in water")
        self.play(FadeIn(bath), Create(surface), run_time=0.8)
        schematic = T("schematic", 24, GREY).move_to([5.25, 3.35, 0])
        self.play(FadeIn(schematic), run_time=0.3)
        self.finish()


class S04Osmosis(LiveScene):
    def construct(self):
        bath, surface, tube, left, right, labels = bulb_world()
        self.add(bath, surface, tube, left, right, labels)
        sugars = VGroup(*[sugar([-4.25 + 0.38 * (i % 4), -0.9 + 0.48 * (i // 4), 0]) for i in range(12)])
        self.at("strong sugar solution")
        self.play(LaggedStart(*[FadeIn(s, scale=0.5) for s in sugars], lag_ratio=0.06), run_time=1.0)
        wp = VGroup(T(PSI, 42, TEXT), T("s", 24, TEXT).shift([0.29, -0.22, 0]), T("down", 30, GOLD).shift([0.9, 0, 0])).move_to([-3.7, 2.8, 0])
        self.at("lowers its water potential")
        self.play(FadeIn(wp), run_time=0.6)
        waters = VGroup(*[droplet(p, 1.15) for p in [(-5.4, -0.8, 0), (-5.0, 0.8, 0), (-3.7, -2.0, 0), (-2.4, -0.8, 0), (-2.5, 0.8, 0)]])
        self.at("water rushes in")
        self.play(*[w.animate.move_to([-3.7 + 0.35 * np.cos(i), -0.2 + 0.35 * np.sin(i), 0]) for i, w in enumerate(waters)], run_time=1.2)
        level = ValueTracker(-0.35)
        gf, fill = pressure_gauge(-0.6, -2.0, 2.0, -0.9, level, AMBER)
        self.add(gf, fill)
        self.at("pressure inside rises")
        pl = VGroup(T(PSI, 38), T("p", 22).shift([0.26, -0.2, 0]), T("up", 30, AMBER).shift([0.85, 0, 0])).move_to([0, 2.55, 0])
        self.play(level.animate.set_value(1.55), FadeIn(pl), run_time=1.3)
        self.finish()


class S05Flow(LiveScene):
    def construct(self):
        bath, surface, tube, left, right, labels = bulb_world()
        self.add(bath, surface, tube, left, right, labels)
        sugars = VGroup(*[sugar([-4.2 + 0.4 * (i % 4), -0.9 + 0.5 * (i // 4), 0]) for i in range(12)])
        self.add(sugars)
        hi, lo = ValueTracker(1.6), ValueTracker(0.0)
        hg, hf = pressure_gauge(-5.6, -2.0, 2.0, -0.9, hi, AMBER, 0.55)
        lg, lf = pressure_gauge(5.6, -2.0, 2.0, -0.9, lo, AMBER, 0.55)
        hg[2].next_to(hg[1], LEFT, buff=0.08)
        self.add(hg, hf, lg, lf)
        self.at("pressure pushes")
        moving = flow([[-3.2, -0.25, 0], [3.2, -0.25, 0]], 11, GOLD, 0.13, 0.16)
        self.add(moving)
        self.play(hi.animate.set_value(1.25), lo.animate.set_value(0.35), run_time=1.5)
        self.at("toward the other bulb")
        arrow = Arrow([-2.5, -2.75, 0], [2.5, -2.75, 0], buff=0, color=AMBER, stroke_width=8)
        self.play(GrowArrow(arrow), run_time=0.8)
        self.at("flows in bulk")
        label = T("bulk flow", 38, AMBER).move_to([0, 0.75, 0])
        self.play(FadeIn(label), run_time=0.5)
        self.at("higher pressure to lower")
        rule = T("higher pressure  →  lower pressure", 32, TEXT).move_to([0, -3.35, 0])
        self.play(Transform(VGroup(arrow, label), rule), run_time=0.8)
        self.finish()


class S06Plant(LiveScene):
    def construct(self):
        # Begin with the apparatus, then transform the same endpoints into plant organs.
        _, _, tube, left, right, labels = bulb_world()
        apparatus = VGroup(tube, left, right, labels)
        self.add(apparatus)
        plant, source, _, phloem = source_sink_plant()
        source_copy = source.copy().move_to(left.get_center())
        self.at("leaf making sugar")
        self.play(Transform(left, source_copy), FadeOut(labels[0]), run_time=1.0)
        src_label = chip("source", AMBER, 32).move_to([-3.7, -2.35, 0])
        self.at("the source")
        self.play(FadeIn(src_label), run_time=0.5)
        root_icon = VGroup(*[Line([3.7, 0.4, 0], [3.7 + d, -0.9, 0], color=GREY, stroke_width=4) for d in (-0.7, -0.2, 0.35, 0.75)])
        fruit = Circle(radius=0.48, color=GREEN, stroke_width=4, fill_color=GREEN, fill_opacity=0.3).move_to([3.7, 0.8, 0])
        tip = VGroup(leaf([3.35, 1.45, 0], 0.35, 0.9, 0.5), leaf([4.05, 1.45, 0], -0.35, 0.9, 0.5))
        sinks = VGroup(root_icon, fruit, tip)
        self.at("root")
        self.play(Transform(right, sinks), FadeOut(labels[1]), run_time=0.8)
        self.at("fruit")
        self.play(Indicate(fruit, color=GREEN), run_time=0.5)
        self.at("shoot tip")
        self.play(Indicate(tip, color=GREEN), run_time=0.5)
        sink_label = chip("sinks", AMBER, 32).move_to([3.7, -2.35, 0])
        self.at("a sink")
        self.play(FadeIn(sink_label), tube.animate.set_stroke(AMBER, 8), run_time=0.6)
        ph_label = T("phloem", 30, AMBER).move_to([0, 0.55, 0])
        self.play(FadeIn(ph_label), run_time=0.4)
        self.finish()


class S07Sink(LiveScene):
    def construct(self):
        plant, source, xylem, phloem = source_sink_plant()
        self.add(plant)
        sap = flow([[-1.0, 0.5, 0], [-1.0, -2.65, 0]], 7, GOLD, 0.11, 0.13)
        self.add(sap)
        track, gf, fill = low_gauge(2.8, -2.3, high=True)
        self.add(gf, fill)
        root_sugars = VGroup(*[sugar([-0.95, -2.35 + 0.28 * i, 0], 0.8) for i in range(4)])
        self.add(root_sugars)
        self.at("sugar is removed")
        self.play(*[s.animate.shift([1.4 + 0.25 * i, -0.45, 0]) for i, s in enumerate(root_sugars)], run_time=1.0)
        waters = VGroup(*[droplet([-1.0, -2.15 + 0.3 * i, 0], 0.9) for i in range(3)])
        self.add(waters)
        self.at("water leaves")
        self.play(*[w.animate.shift([0.9 + 0.25 * i, -0.4, 0]) for i, w in enumerate(waters)], run_time=0.8)
        self.at("pressure falls")
        self.play(track.animate.set_value(-1.25), run_time=1.0)
        source_water = flow([[-1.25, -1.0, 0], [-1.25, 0.55, 0], [-1.0, 0.55, 0]], 5, BLUE, 0.11, 0.15)
        self.at("xylem alongside")
        self.add(source_water)
        self.play(Indicate(xylem, color=BLUE, scale_factor=1.6), run_time=0.8)
        self.at("water at the source")
        tag = T("water in", 32, BLUE).move_to([-3.2, 1.55, 0])
        self.play(FadeIn(tag), Indicate(source, color=BLUE), run_time=0.7)
        self.finish()


class S08Bothways(LiveScene):
    def construct(self):
        plant, source, _, _ = source_sink_plant()
        self.add(plant)
        high, hg, hf = low_gauge(-4.7, -0.25, high=True)
        low1, g1, f1 = low_gauge(1.2, -3.3, high=False)
        low2, g2, f2 = low_gauge(1.2, 1.55, high=False)
        self.add(hg, hf, g1, f1, g2, f2)
        self.at("source to sink")
        down = flow([[-1.0, 0.6, 0], [-1.0, -2.65, 0]], 7, AMBER, 0.13, 0.14)
        self.add(down)
        self.at("wherever the sink sits")
        up = flow([[-1.0, 0.6, 0], [-1.0, 2.7, 0]], 6, AMBER, 0.13, 0.14)
        self.add(up)
        self.at("down to the roots")
        da = Arrow([-2.0, -0.3, 0], [-2.0, -2.55, 0], buff=0, color=AMBER, stroke_width=8)
        self.play(GrowArrow(da), run_time=0.7)
        self.at("up to a growing")
        ua = Arrow([-0.1, 1.0, 0], [-0.1, 2.65, 0], buff=0, color=AMBER, stroke_width=8)
        self.play(GrowArrow(ua), run_time=0.7)
        self.finish()


class S09Objection(LiveScene):
    def construct(self):
        title = T("the objection", 38, TEXT).move_to([-4.6, 3.2, 0])
        self.play(FadeIn(title), run_time=0.5)
        cells = VGroup(*[RoundedRectangle(corner_radius=0.16, width=1.75, height=3.9, stroke_color=AMBER, stroke_width=5,
                                          fill_color=AMBER, fill_opacity=0.11).move_to([-4.6 + 1.7 * i, 0.0, 0]) for i in range(4)])
        self.at("tubes are narrow")
        self.play(LaggedStart(*[FadeIn(c) for c in cells], lag_ratio=0.12), run_time=1.0)
        plates = VGroup()
        for x in (-3.75, -2.05, -0.35):
            wall = Line([x, -1.85, 0], [x, 1.85, 0], color=TEXT, stroke_width=8)
            holes = VGroup(*[Dot([x, y, 0], radius=0.10, color=BG) for y in (-1.2, -0.6, 0, 0.6, 1.2)])
            plates.add(VGroup(wall, holes))
        self.at("blocked at intervals")
        self.play(FadeIn(plates), run_time=0.8)
        self.at("sieve plates")
        lab = T("sieve plate", 30, TEXT).move_to([-2.05, 2.45, 0])
        pointer = Arrow([-2.05, 2.15, 0], [-2.05, 1.5, 0], buff=0, color=TEXT, stroke_width=4)
        self.play(FadeIn(lab), GrowArrow(pointer), run_time=0.5)
        dg, needle, center = dial((4.65, -0.2), -2.65)
        needed = T("needed", 30, TEXT).move_to([4.65, 1.65, 0])
        impossible = T("impossible?", 30, RED).move_to([4.65, -1.9, 0])
        self.at("Pushing sap")
        self.play(FadeIn(dg), FadeIn(needed), run_time=0.6)
        self.at("impossible pressures")
        self.play(Rotate(needle, 2.25, about_point=center), FadeIn(impossible), run_time=1.3)
        self.finish()


class S10Test(LiveScene):
    def construct(self):
        credit = VGroup(T("Knoblauch, Holbrook and colleagues, 2016", 28, TEXT),
                        T("morning glory (Ipomoea nil)", 26, TEAL)).arrange(DOWN, buff=0.06).move_to([0.4, 3.4, 0])
        self.play(FadeIn(credit), run_time=0.6)
        vine, path, _ = vine_world(False)
        self.at("morning glory")
        self.play(FadeIn(vine), run_time=1.0)
        self.at("measured the pressure")
        probe = VGroup(Line([5.7, -0.5, 0], [0.15, 1.9, 0], color=TEXT, stroke_width=5),
                       Dot([0.15, 1.9, 0], radius=0.11, color=TEXT))
        self.play(Create(probe), run_time=1.0)
        self.at("working sieve tubes")
        self.play(Indicate(path, color=AMBER, scale_factor=1.03), run_time=0.7)
        self.at("tiny probes")
        reading = chip("about 1.08 MPa", AMBER, 34).move_to([4.35, -1.15, 0])
        note = T("moderate-sized plants", 26, TEXT).move_to([4.35, -1.85, 0])
        self.play(FadeIn(reading), FadeIn(note), run_time=0.7)
        self.finish()


class S11Longer(LiveScene):
    def construct(self):
        short, short_path, short_leaves = vine_world(False)
        self.add(short)
        long, long_path, long_leaves = vine_world(True)
        self.at("path longer")
        self.play(Transform(short_path, long_path), run_time=1.8)
        self.at("removing leaves")
        self.play(FadeOut(short_leaves[0]), FadeOut(short_leaves[1]), run_time=0.8)
        far_leaf = long_leaves[-1].copy()
        self.play(FadeIn(far_leaf), run_time=0.5)
        bar = DoubleArrow([-4.8, -1.95, 0], [4.8, -1.95, 0], buff=0, color=TEXT, stroke_width=5, tip_length=0.22)
        self.at("much farther")
        self.play(GrowFromCenter(bar), run_time=1.1)
        label = T("source-to-root path", 30, TEXT).move_to([0, -1.45, 0])
        self.play(FadeIn(label), run_time=0.5)
        travellers = flow([[4.7, 2.55, 0], [0.2, 2.45, 0], [-2.8, 0, 0], [-4.8, -2.5, 0]], 9, GOLD, 0.11, 0.1)
        self.add(travellers)
        self.finish()


class S12Predict(LiveScene):
    def construct(self):
        vine, _, _ = vine_world(True)
        self.add(vine)
        dg, needle, center = dial((4.8, -0.65), -2.7)
        self.add(dg)
        self.at("pressure needed would soar")
        self.play(Rotate(needle, 2.25, about_point=center), run_time=1.5)
        self.at("path much longer")
        bar = DoubleArrow([-4.8, -1.85, 0], [4.75, -1.85, 0], buff=0, color=TEXT, stroke_width=5, tip_length=0.22)
        self.play(GrowFromCenter(bar), run_time=0.8)
        self.at("what must change")
        card = opaque_chip("Longer path. What must change?", YELLOW, 30).move_to([0.5, -3.3, 0])
        self.play(FadeIn(card, scale=0.85), run_time=0.6)
        self.play(Indicate(card, color=YELLOW, scale_factor=1.04), run_time=0.7)
        self.finish()


class S13Pause(Scene):
    def construct(self):
        vine, _, _ = vine_world(True)
        dg, needle, center = dial((4.8, -0.65), -0.45)
        bar = DoubleArrow([-4.8, -1.85, 0], [4.75, -1.85, 0], buff=0, color=TEXT, stroke_width=5, tip_length=0.22)
        card = opaque_chip("Longer path. What must change?", YELLOW, 30).move_to([0.5, -3.3, 0])
        self.add(vine, dg, bar, card)
        timer = ValueTracker(0.001)
        base = Circle(radius=0.48, color=GREY, stroke_width=6).move_to([5.8, -3.05, 0])
        ring = always_redraw(lambda: Arc(radius=0.48, start_angle=PI / 2, angle=-TAU * timer.get_value(),
                                         color=YELLOW, stroke_width=8, arc_center=[5.8, -3.05, 0]))
        self.add(base, ring)
        self.play(timer.animate.set_value(1.0), run_time=4.8, rate_func=linear)


class S14Reveal(LiveScene):
    def construct(self):
        vine, _, _ = vine_world(True)
        self.add(vine)
        one = chip("1  pressure", AMBER, 34).move_to([3.9, 1.25, 0])
        two = chip("2  conductivity", BLUE, 34).move_to([3.9, 0.25, 0])
        self.at("Two things changed")
        self.play(FadeIn(one), FadeIn(two), run_time=0.8)
        self.at("First")
        self.play(two.animate.set_opacity(0.25), Indicate(one, color=AMBER), run_time=0.6)
        level = ValueTracker(-1.55)
        gf, fill = pressure_gauge(-5.75, -2.0, 2.4, -1.8, level, AMBER, 0.7)
        self.add(gf, fill)
        young = opaque_chip("young: about 0.75 MPa", AMBER, 30).move_to([2.2, -1.25, 0])
        self.at("rose with path length")
        self.play(level.animate.set_value(-0.4), FadeIn(young), run_time=1.1)
        longest = opaque_chip("longest: more than 2.2 MPa", AMBER, 30).move_to([2.2, -1.25, 0])
        self.at("passed 2")
        self.play(level.animate.set_value(2.0), Transform(young, longest), run_time=1.5)
        self.finish()


class S15Pores(LiveScene):
    def construct(self):
        # A single sieve plate fills the left half of the frame.
        plate = RoundedRectangle(corner_radius=0.18, width=4.1, height=5.7, stroke_color=AMBER, stroke_width=6,
                                 fill_color=AMBER, fill_opacity=0.12).move_to([-3.75, 0, 0])
        small = VGroup(*[Circle(radius=0.13, color=TEXT, stroke_width=4).move_to([-4.65 + 0.6 * (i % 4), -1.5 + 0.75 * (i // 4), 0]) for i in range(20)])
        self.add(plate, small)
        cond_bg = RoundedRectangle(corner_radius=0.15, width=5.0, height=0.75, stroke_color=GREY, stroke_width=3).move_to([3.0, 1.65, 0])
        cond = Rectangle(width=0.65, height=0.7, stroke_width=0, fill_color=BLUE, fill_opacity=0.85).align_to(cond_bg, LEFT).shift(RIGHT * 0.03)
        cond_label = T("sieve-tube conductivity", 30, TEXT).move_to([3.0, 2.35, 0])
        self.at("conducted five to six")
        self.play(FadeIn(cond_bg), FadeIn(cond_label), cond.animate.stretch_to_fit_width(4.85).align_to(cond_bg, LEFT).shift(RIGHT * 0.03), run_time=1.4)
        mult = T("5 to 6×", 40, BLUE, weight=BOLD).move_to([3.0, 0.85, 0])
        self.play(FadeIn(mult), run_time=0.4)
        wide = VGroup(*[Circle(radius=0.25, color=TEXT, stroke_width=4).move_to(c.get_center()) for c in small])
        self.at("pores were wider")
        self.play(Transform(small, wide), run_time=1.2)
        self.at("With both changes")
        self.play(FadeOut(VGroup(plate, small, cond_bg, cond, cond_label, mult)), run_time=0.6)
        vine, _, _ = vine_world(True)
        self.play(FadeIn(vine), run_time=0.7)
        reach = Line([-4.8, -2.2, 0], [4.8, 2.55, 0], color=AMBER, stroke_width=12)
        self.at("estimated reach")
        self.play(Create(reach), run_time=1.2)
        eq = T("estimated reach = vine length", 32, TEXT).move_to([0, -3.25, 0])
        self.at("matched the length")
        self.play(FadeIn(eq), run_time=0.6)
        self.finish()


class S16Scope(LiveScene):
    def construct(self):
        card = RoundedRectangle(corner_radius=0.25, width=11.0, height=6.6, stroke_color=TEAL, stroke_width=4,
                                fill_color=BG, fill_opacity=0.4)
        vine, _, _ = vine_world(False)
        vine.scale(0.60).move_to([-2.25, -0.05, 0])
        self.play(FadeIn(card), FadeIn(vine), run_time=0.8)
        self.at("one species")
        species = VGroup(T("one species", 38, TEXT), T("Ipomoea nil", 34, TEAL)).arrange(DOWN, buff=0.18).move_to([3.0, 1.75, 0])
        self.play(FadeIn(species), run_time=0.6)
        care = T("measured with care", 32, TEXT).move_to([3.0, 0.35, 0])
        self.at("measured with care")
        self.play(FadeIn(care), run_time=0.5)
        check = T("✓", 80, GREEN, weight=BOLD).move_to([-0.45, -2.1, 0])
        support = VGroup(T("strong support", 38, AMBER), T("pressure flow in this plant", 26, TEXT)).arrange(DOWN, buff=0.12).move_to([2.85, -2.1, 0])
        self.at("strong support")
        self.play(FadeIn(check, scale=0.7), FadeIn(support), run_time=0.8)
        self.finish()


class S17Close(LiveScene):
    def construct(self):
        plant, source, xylem, phloem = source_sink_plant()
        self.add(plant)
        sugars = VGroup(*[sugar([-3.35 + 0.32 * i, 1.55, 0], 0.9) for i in range(4)])
        self.at("sugar goes in")
        self.play(*[s.animate.move_to([-2.3 + 0.2 * i, 0.75, 0]) for i, s in enumerate(sugars)], run_time=0.9)
        waters = VGroup(*[droplet([-3.25 + 0.4 * i, -0.25, 0], 0.95) for i in range(4)])
        self.at("water follows")
        self.play(*[w.animate.move_to([-1.3, 0.2 + 0.25 * i, 0]) for i, w in enumerate(waters)], run_time=0.9)
        high, hg, hf = low_gauge(-4.7, -0.25, high=False)
        self.add(hg, hf)
        self.at("pressure rises")
        self.play(high.animate.set_value(1.3), run_time=0.9)
        down = flow([[-1.0, 0.6, 0], [-1.0, -2.65, 0]], 7, AMBER, 0.12, 0.14)
        up = flow([[-1.0, 0.6, 0], [-1.0, 2.7, 0]], 6, AMBER, 0.12, 0.14)
        self.at("Sap is pushed")
        self.add(down, up)
        pushed = T("pushed", 48, AMBER, weight=BOLD).move_to([2.55, 0.8, 0])
        pulled = T("pulled", 38, RED).move_to([2.55, -0.65, 0])
        blue = Line([1.55, -1.15, 0], [3.55, -1.15, 0], color=BLUE, stroke_width=6)
        self.play(FadeIn(pushed), FadeIn(pulled), Create(blue), run_time=0.7)
        self.at("sugar is taken out")
        sinks = VGroup(chip("root sink", AMBER, 28).move_to([4.8, -2.15, 0]),
                       chip("shoot sink", AMBER, 28).move_to([4.8, 2.35, 0]))
        self.play(FadeIn(sinks), run_time=0.6)
        self.finish()


class S18End(EndCard):
    LINE = "Sugar in, water follows, pressure rises: sap is pushed to sinks."
