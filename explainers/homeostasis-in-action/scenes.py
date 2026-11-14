"""When the Body Pushes Back — homeostasis-in-action teaching film.

COLOR MAP
  GOLD   stable range
  RED    disturbance / heat
  BLUE   sensor signals
  YELLOW control-centre signals
  TEAL   response / cooling
  WHITE  current value

The human, gauge, and skin inset are rebuilt by the same builders in every scene
that carries them.  The only plotted curve is computed from an exponential
return model; no curve is hand-sketched.
"""
import numpy as np
from bp_parts import *  # noqa: F401,F403


SKIN = "#C9866B"


def stage_panel():
    """Shared landscape-style field behind the carried diagram world."""
    return RoundedRectangle(corner_radius=0.28, width=13.15, height=6.75,
                            stroke_width=0, fill_color="#2A3445",
                            fill_opacity=0.72).set_z_index(-20)


def breathe_fill(mob, low=0.12, high=0.28, speed=1.15):
    """Slow meaningful field motion for a range, skin, or heat region."""
    mob._breathe_t = 0.0

    def update(m, dt):
        m._breathe_t += dt
        a = low + (high - low) * (0.5 + 0.5 * np.sin(speed * m._breathe_t))
        m.set_fill(opacity=a)
    return mob.add_updater(update)


class FilmSpoken(SpokenScene):
    def setup(self):
        super().setup()
        self.add(stage_panel())


class FilmPredictPause(PredictPause):
    def setup(self):
        super().setup()
        self.add(stage_panel())


def arrow(a, b, color=TEXT, width=5, tip=0.22, buff=0.05):
    return Arrow(a, b, buff=buff, color=color, stroke_width=width,
                 tip_length=tip, max_tip_length_to_length_ratio=0.35,
                 max_stroke_width_to_length_ratio=10)


def edge_point(mob, toward, pad=0.1):
    c = mob.get_center()
    d = np.array(toward) - c
    u = d / max(np.linalg.norm(d), 1e-6)
    tx = (mob.width / 2 + pad) / max(abs(u[0]), 1e-6)
    ty = (mob.height / 2 + pad) / max(abs(u[1]), 1e-6)
    return c + u * min(tx, ty)


def build_person(center=(-3.55, -0.1, 0), scale=1.0, heart_fast=True):
    """The film's carried, full-height schematic human."""
    c = np.array(center, dtype=float)
    head = Circle(radius=0.52, color=TEXT, stroke_width=5,
                  fill_color=SKIN, fill_opacity=0.18).move_to(c + UP * 2.35)
    torso = Line(c + UP * 1.78, c + DOWN * 0.25, color=TEXT, stroke_width=8)
    arms = VGroup(
        Line(c + UP * 1.3, c + LEFT * 0.9 + UP * 0.35, color=TEXT, stroke_width=7),
        Line(c + UP * 1.3, c + RIGHT * 0.9 + UP * 0.5, color=TEXT, stroke_width=7),
    )
    legs = VGroup(
        Line(c + DOWN * 0.25, c + LEFT * 0.75 + DOWN * 1.75, color=TEXT, stroke_width=8),
        Line(c + DOWN * 0.25, c + RIGHT * 0.8 + DOWN * 1.55, color=TEXT, stroke_width=8),
    )
    heart = Circle(radius=0.22, color=RED, stroke_width=5,
                   fill_color=RED, fill_opacity=0.35).move_to(c + LEFT * 0.18 + UP * 0.95)
    if heart_fast:
        pulse(heart, base=5.0, amp=2.4, speed=7.0)
    body = VGroup(head, torso, arms, legs, heart).scale(scale)
    body.head, body.heart = head, heart
    return body


def build_stairs():
    blocks = VGroup()
    for i, (w, h) in enumerate(((1.2, 0.55), (1.2, 1.1), (1.2, 1.65))):
        r = Rectangle(width=w, height=h, color=GREY, stroke_width=3,
                      fill_color=GREY, fill_opacity=0.12)
        r.move_to([-5.75 + 1.15 * i, -3.38 + h / 2, 0])
        blocks.add(r)
    return blocks


def build_gauge(value=2.05, x=3.75, label=None, marker_bob=False):
    """Carried vertical gauge. `value` is its scene y coordinate."""
    outline = RoundedRectangle(corner_radius=0.2, width=2.45, height=5.75,
                               color=GREY, stroke_width=4,
                               fill_color=GREY, fill_opacity=0.24).move_to([x, 0.05, 0])
    breathe_fill(outline, low=0.18, high=0.34, speed=0.72)
    band = Rectangle(width=1.9, height=1.25, stroke_width=0,
                     fill_color=GOLD, fill_opacity=0.28).move_to([x, -0.35, 0])
    band_edge = Rectangle(width=1.9, height=1.25, color=GOLD, stroke_width=3,
                          fill_opacity=0).move_to(band)
    marker = VGroup(
        Line([x - 0.82, value, 0], [x + 0.82, value, 0], color=TEXT, stroke_width=9),
        Triangle(color=TEXT, fill_color=TEXT, fill_opacity=1, stroke_width=0)
        .scale(0.12).rotate(-PI / 2).move_to([x + 1.03, value, 0]),
    )
    if marker_bob:
        bob(marker, amp=0.055, speed=1.7)
    parts = VGroup(outline, band, band_edge, marker)
    if label:
        lab = T(label, 28, GOLD, weight=BOLD).next_to(outline, DOWN, buff=0.16)
        parts.add(lab)
        parts.range_label = lab
    parts.outline, parts.band, parts.band_edge, parts.marker = outline, band, band_edge, marker
    return parts


def build_world(value=2.05, range_label=False, marker_bob=False, stairs=True):
    person = build_person()
    gauge = build_gauge(value=value, label="stable range" if range_label else None,
                        marker_bob=marker_bob)
    steps = build_stairs()
    g = VGroup(person, gauge)
    if stairs:
        g.add(steps)
    g.person, g.gauge, g.stairs = person, gauge, steps
    return g


def build_skin_inset(center=(-0.1, -0.55, 0), scale=1.0, wet=True):
    """Cartoon skin cross-section and sweat gland; no molecular detail."""
    c = np.array(center, dtype=float)
    skin = RoundedRectangle(corner_radius=0.16, width=3.25, height=2.35,
                            color=SKIN, stroke_width=4, fill_color=SKIN,
                            fill_opacity=0.13).move_to(c)
    surface = Line(c + LEFT * 1.45 + UP * 0.65, c + RIGHT * 1.45 + UP * 0.65,
                   color=SKIN, stroke_width=7)
    gland = Arc(radius=0.43, start_angle=0.15, angle=1.75 * PI,
                color=TEAL, stroke_width=8, arc_center=c + DOWN * 0.35)
    duct = Line(c + UP * 0.65, c + UP * 0.02, color=TEAL, stroke_width=6)
    drops = VGroup(*[
        Circle(radius=0.13, color=TEAL, stroke_width=3,
               fill_color=TEAL, fill_opacity=0.5).move_to(c + [dx, 0.98 + dy, 0])
        for dx, dy in ((-0.42, 0), (0.0, 0.16), (0.43, -0.04))
    ])
    if not wet:
        drops.set_opacity(0)
    g = VGroup(skin, surface, gland, duct, drops).scale(scale)
    g.skin, g.surface, g.gland, g.duct, g.drops = skin, surface, gland, duct, drops
    return g


def build_predict_backdrop():
    """Exact carried frame for the spoken prediction and its silent pause."""
    world = build_world(value=1.75, range_label=True, marker_bob=True, stairs=False)
    world.scale(0.72).move_to([-2.7, 0.1, 0])
    world.gauge.range_label.scale(1.45)
    skin = build_skin_inset(center=(2.9, 0.0, 0), scale=1.05, wet=True)
    heat = VGroup(*[
        arrow([2.2 + 0.65 * i, 0.9, 0], [2.2 + 0.65 * i, 1.75, 0], RED, 5, 0.18)
        for i in range(3)
    ])
    for a in heat:
        bob(a, amp=0.04, speed=1.3, seed=2)
    # Both paths are computed functions of horizontal progress.
    def path(fn, color, opacity=0.32):
        pts = [[-0.58 + 3.0 * t, 1.45 + fn(t), 0] for t in np.linspace(0, 1, 70)]
        return VMobject(color=color, stroke_width=5, stroke_opacity=opacity).set_points_as_corners(pts)
    fast = path(lambda t: -1.45 * (1 - np.exp(-3.0 * t)) / (1 - np.exp(-3.0)), TEXT)
    high = path(lambda t: -0.32 * (1 - np.exp(-2.0 * t)) / (1 - np.exp(-2.0)), TEXT)
    g = VGroup(world, skin, heat, fast, high)
    g.world, g.skin, g.heat, g.fast, g.high = world, skin, heat, fast, high
    return g


def loop_nodes(compact=False):
    labels = ["change", "sensor", "control center", "effector", "opposing response"]
    colors = [RED, BLUE, YELLOW, TEAL, TEAL]
    nodes = VGroup(*[chip(l, c, size=25, pad=0.16) for l, c in zip(labels, colors)])
    if compact:
        nodes.arrange(RIGHT, buff=0.12).move_to([0, 0.3, 0])
        fit(nodes, max_w=12.2)
    else:
        positions = ([-4.15, 1.35, 0], [0, 2.2, 0], [4.1, 1.35, 0],
                     [3.0, -1.55, 0], [-3.0, -1.55, 0])
        for n, p in zip(nodes, positions):
            n.move_to(p)
    links = VGroup(*[arrow(edge_point(nodes[i], nodes[(i + 1) % 5].get_center()),
                           edge_point(nodes[(i + 1) % 5], nodes[i].get_center()),
                           colors[(i + 1) % 5], width=4, tip=0.16, buff=0.02)
                     for i in range(5)])
    if compact:
        links.submobjects[-1] = CurvedArrow(nodes[4].get_bottom() + DOWN * 0.12,
                                            nodes[0].get_bottom() + DOWN * 0.12,
                                            angle=-0.55, color=RED,
                                            stroke_width=4, tip_length=0.16)
    return nodes, links


class S00Hook(FilmSpoken):
    def construct(self):
        world = build_world(value=2.05, marker_bob=True)
        self.play(FadeIn(world.person, shift=UP * 0.12), FadeIn(world.stairs),
                  FadeIn(world.gauge.outline), run_time=0.8)
        self.at("At the top")
        self.play(world.stairs.animate.shift(DOWN * 0.45),
                  FadeIn(world.gauge.band), FadeIn(world.gauge.band_edge), run_time=1.0)
        self.at("heartbeat stays fast")
        self.play(Indicate(world.person.heart, color=RED, scale_factor=1.25), run_time=0.8)
        self.at("A marker sits above")
        self.play(FadeIn(world.gauge.marker, shift=UP * 0.15), run_time=0.7)
        self.at("Something must move it back")
        ret = CurvedArrow([4.8, 1.6, 0], [4.75, 0.25, 0], angle=-0.8,
                          color=TEAL, stroke_width=6, tip_length=0.25)
        self.play(Create(ret), run_time=1.1)
        self.add(scope_tag("schematic"))
        self.finish()


class S01Title(TitleCard):
    LESSON = "Homeostasis in Action"
    TITLE = "When the Body Pushes Back"

    def construct(self):
        panel = stage_panel()
        world = build_world(value=2.05, marker_bob=True)
        world.set_opacity(0.32)
        world.layout_ok = True  # intentionally dimmed behind the title
        title = fit_text(self.TITLE, max_w=11.5, size=52, font=TITLE_FONT,
                         color=TEXT).move_to([0, 0.45, 0])
        lesson = T(self.LESSON.upper(), 24, GOLD).next_to(title, UP, buff=0.35)
        rule = Line(LEFT * 1.5, RIGHT * 1.5, color=GOLD, stroke_width=4).next_to(title, DOWN, buff=0.32)
        self.add(panel, world)
        self.play(FadeIn(lesson), Write(title), GrowFromCenter(rule), run_time=0.9)
        self.wait(0.55)
        self.play(FadeOut(VGroup(lesson, title, rule)), run_time=0.45)
        self.finish()


class S02Range(FilmSpoken):
    def construct(self):
        gauge = build_gauge(value=1.55, x=0.0, marker_bob=True)
        gauge.scale(1.12).shift(DOWN * 0.05)
        breathe_fill(gauge.band, low=0.20, high=0.38)
        self.add(gauge.outline)
        self.at("That shaded band")
        self.play(FadeIn(gauge.band), FadeIn(gauge.band_edge), run_time=0.8)
        self.at("range not a single target")
        lab = T("stable range", 36, GOLD, weight=BOLD).next_to(gauge.band, RIGHT, buff=0.35)
        self.play(FadeIn(lab), FadeIn(gauge.marker), run_time=0.7)
        self.at("Inside it")
        self.play(gauge.marker.animate.shift(DOWN * 1.55), run_time=1.2)
        self.play(gauge.marker.animate.shift(UP * 0.65), run_time=0.8)
        self.at("Homeostasis means keeping")
        warm = VGroup(Circle(radius=0.34, color=RED, fill_color=RED, fill_opacity=0.25),
                      *[Line(ORIGIN, RIGHT * 0.28, color=RED, stroke_width=4).rotate(k * PI / 4).shift(RIGHT * 0.58)
                        for k in range(8)]).move_to([-4.6, 0.6, 0])
        cool = VGroup(*[Line(LEFT * 0.35, RIGHT * 0.35, color=BLUE, stroke_width=4).rotate(k * PI / 3)
                        for k in range(3)]).move_to([4.6, 0.6, 0])
        self.play(FadeIn(warm, shift=RIGHT * 0.3), FadeIn(cool, shift=LEFT * 0.3), run_time=0.8)
        self.at("while the outside changes")
        self.play(warm.animate.shift(UP * 0.5), cool.animate.shift(DOWN * 0.45),
                  gauge.marker.animate.shift(UP * 0.35), run_time=1.2)
        self.at("motion matters")
        bull = VGroup(Circle(radius=0.42, color=TEXT), Circle(radius=0.2, color=TEXT),
                      Line(UL * 0.38, DR * 0.38, color=RED, stroke_width=7),
                      Line(UR * 0.38, DL * 0.38, color=RED, stroke_width=7)).move_to(gauge.band)
        self.play(FadeOut(lab), FadeIn(bull), gauge.marker.animate.shift(DOWN * 0.55), run_time=0.7)
        self.play(FadeOut(bull), run_time=0.5)
        self.finish()


class S03Disturbance(FilmSpoken):
    def construct(self):
        world = build_world(value=-0.35, range_label=True, stairs=False)
        self.add(world)
        self.at("Now warm the body")
        heat = Rectangle(width=2.8, height=5.7, stroke_width=0, fill_color=RED,
                         fill_opacity=0.16).move_to([-5.55, 0.1, 0])
        breathe_fill(heat, low=0.10, high=0.25, speed=1.0)
        heat_arrows = VGroup(*[arrow([-6.25, y, 0], [-4.8, y, 0], RED, 6, 0.2)
                               for y in (-1.4, 0.0, 1.4)])
        self.play(FadeIn(heat), LaggedStart(*[GrowArrow(a) for a in heat_arrows], lag_ratio=0.2), run_time=1.0)
        self.at("pushes the temperature marker")
        self.play(world.gauge.marker.animate.shift(UP * 2.35), run_time=1.2)
        self.at("Sensors in the skin and brain")
        sensors = VGroup(*[Dot(p, radius=0.12, color=BLUE) for p in
                           ([-4.4, 0.6, 0], [-3.55, 2.25, 0], [-2.75, 0.55, 0])])
        self.play(LaggedStart(*[FadeIn(d, scale=1.8) for d in sensors], lag_ratio=0.25), run_time=0.9)
        self.at("send blue signals")
        control = chip("control center", YELLOW, size=24, pad=0.11).move_to([-3.55, 3.06, 0])
        blue_paths = VGroup(*[arrow(d.get_center(), control.get_bottom(), BLUE, 4, 0.14) for d in sensors])
        self.play(LaggedStart(*[Create(p) for p in blue_paths], lag_ratio=0.2),
                  FadeIn(control), run_time=1.2)
        self.at("control center sends")
        skin = build_skin_inset(center=(-0.65, -0.65, 0), scale=0.75, wet=False)
        cmd = arrow(control.get_right(), skin.gland.get_center(), YELLOW, 6, 0.2)
        self.play(FadeIn(skin), GrowArrow(cmd), run_time=1.2)
        self.finish()


class S04Cooling(FilmSpoken):
    def construct(self):
        skin = build_skin_inset(center=(-2.65, -0.15, 0), scale=1.35, wet=False)
        gauge = build_gauge(value=1.95, x=3.75, label="stable range")
        breathe_fill(skin.skin, low=0.14, high=0.30, speed=1.25)
        breathe_fill(gauge.band, low=0.20, high=0.38, speed=0.95)
        self.add(skin, gauge)
        self.at("Sweat appears")
        self.play(LaggedStart(*[FadeIn(d, shift=UP * 0.15) for d in skin.drops], lag_ratio=0.2), run_time=0.9)
        self.at("As it evaporates")
        vapor = VGroup(*[Arc(radius=0.35, start_angle=PI, angle=-PI,
                             color=TEAL, stroke_width=4).move_to([-3.2 + i * 0.55, 2.15, 0])
                         for i in range(3)])
        heat = VGroup(*[arrow([-3.2 + i * 0.55, 1.15, 0], [-3.2 + i * 0.55, 2.65, 0], RED, 5, 0.18)
                        for i in range(3)])
        self.play(skin.drops.animate.scale(0.25).set_opacity(0.15),
                  LaggedStart(*[FadeIn(v, shift=UP * 0.2) for v in vapor], lag_ratio=0.2), run_time=1.1)
        self.at("heat leaves the skin")
        self.play(LaggedStart(*[GrowArrow(a) for a in heat], lag_ratio=0.18),
                  gauge.marker.animate.shift(DOWN * 1.75), run_time=1.4)
        self.at("response acts against")
        loop = CurvedArrow([4.85, 1.6, 0], [4.85, -0.25, 0], angle=-0.8,
                           color=TEAL, stroke_width=7, tip_length=0.25)
        label = T("response", 32, TEAL).move_to([0.2, -2.6, 0])
        self.play(Create(loop), FadeIn(label), run_time=0.8)
        self.at("negative feedback")
        new = T("negative feedback", 36, TEAL, weight=BOLD).move_to(label)
        self.play(swap(label, new), Indicate(loop, color=TEAL), run_time=0.9)
        self.finish()


class S05GuidingRule(FilmSpoken):
    def construct(self):
        gauge = build_gauge(value=1.8, x=0.0, label="stable range")
        gauge.scale(1.08)
        breathe_fill(gauge.band, low=0.20, high=0.38, speed=1.0)
        self.add(gauge)
        self.at("opposing responses")
        disturb = arrow([-3.0, 1.8, 0], [-1.2, 1.8, 0], RED, 8, 0.28)
        oppose = arrow([3.0, 1.8, 0], [1.2, 1.8, 0], TEAL, 8, 0.28)
        self.play(GrowArrow(disturb), GrowArrow(oppose), run_time=1.0)
        self.at("move them toward their range")
        self.play(gauge.marker.animate.shift(DOWN * 1.85), run_time=1.3)
        self.at("still vary inside")
        self.play(gauge.marker.animate.shift(UP * 0.45), run_time=0.7)
        self.play(gauge.marker.animate.shift(DOWN * 0.7), run_time=0.7)
        self.at("Negative does not mean harmful")
        bad = T("harmful?", 36, RED).move_to([-3.9, -1.65, 0])
        cross = VGroup(Line(bad.get_corner(UL), bad.get_corner(DR), color=TEXT, stroke_width=7),
                       Line(bad.get_corner(UR), bad.get_corner(DL), color=TEXT, stroke_width=7))
        cross.layout_ok = True  # deliberate cross-out
        self.play(FadeIn(bad), Create(cross), run_time=0.8)
        self.at("pushes against the starting change")
        rule = caption("response opposes change", size=40, color=TEAL, y=-2.9)
        change = Succession(FadeOut(VGroup(bad, cross, gauge, disturb), run_time=0.42),
                            FadeIn(rule, shift=UP * 0.15, run_time=0.58))
        self.play(change, Indicate(oppose, color=TEAL), run_time=1.0)
        self.finish()


class S06Predict(FilmSpoken):
    def construct(self):
        back = build_predict_backdrop()
        breathe_fill(back.skin.skin, low=0.10, high=0.62, speed=1.8)
        self.play(FadeIn(back.world), FadeIn(back.skin), run_time=0.8)
        self.at("cannot evaporate")
        self.play(FadeIn(back.heat), run_time=0.8)
        self.at("return as quickly")
        self.play(Create(back.fast), Create(back.high), run_time=1.0)
        self.at("stay higher")
        self.play(Indicate(back.high, color=TEXT), run_time=0.7)
        self.at("Keep the body")
        q = question_card("No evaporation: fast return or higher?", y=-3.1, size=32)
        self.play(FadeIn(q.question, shift=UP * 0.12), run_time=0.7)
        self.finish()


class S07Pause(FilmPredictPause):
    QUESTION = "No evaporation: fast return or higher?"
    SECONDS = 4.5
    CARD = {"y": -3.1, "size": 32}

    def backdrop(self):
        return build_predict_backdrop()


class S08Reveal(FilmSpoken):
    def construct(self):
        back = build_predict_backdrop()
        breathe_fill(back.skin.skin, low=0.10, high=0.62, speed=1.8)
        self.add(back.world, back.skin, back.heat, back.fast, back.high)
        self.at("Without evaporation")
        self.play(FadeOut(back.fast), back.high.animate.set_stroke(opacity=1.0, width=7), run_time=0.9)
        self.at("removes less heat")
        weak = arrow([2.9, 0.9, 0], [2.9, 1.55, 0], RED, 3, 0.14)
        self.play(Transform(back.heat[1], weak), run_time=0.8)
        self.at("marker stays higher")
        dot = Dot(back.high.get_end(), radius=0.14, color=TEXT, stroke_color=TEAL, stroke_width=3)
        self.play(MoveAlongPath(dot, back.high), run_time=1.5, rate_func=linear)
        ghost_path = back.fast.copy().set_stroke(TEAL, width=4, opacity=0.32)
        ghost_dot = Dot(ghost_path.get_end(), radius=0.12, color=TEAL).set_opacity(0.45)
        vapor = VGroup(*[Arc(radius=0.22, start_angle=PI, angle=-PI, color=TEAL,
                             stroke_width=3).move_to([2.45 + 0.45 * i, 1.65, 0])
                         for i in range(3)]).set_opacity(0.45)
        self.play(Create(ghost_path), FadeIn(ghost_dot), FadeIn(vapor, shift=UP * 0.12), run_time=0.8)
        self.at("response exists")
        eff = place_label(T("effector", 30, TEAL), back.skin.gland,
                          avoid=[back.skin], dirs=(DOWN, RIGHT, LEFT))
        # Keep the label below the inset, with its own short pointer.
        eff.move_to([2.9, -1.85, 0])
        ptr = arrow(eff.get_top(), back.skin.gland.get_bottom(), TEAL, 4, 0.13)
        response = arrow([0.7, -0.55, 0], back.skin.gland.get_left(), TEAL, 7, 0.2)
        self.play(GrowArrow(response), FadeIn(eff), GrowArrow(ptr), run_time=0.9)
        self.at("effect depends")
        thin = arrow(response.get_start(), response.get_end(), TEAL, 3, 0.16)
        self.play(Transform(response, thin), run_time=0.8)
        self.finish()


class S09Map(FilmSpoken):
    def construct(self):
        nodes, links = loop_nodes()
        heading = T("negative-feedback map", 36, TEXT, weight=BOLD).move_to([0, 2.65, 0])
        self.play(FadeIn(heading), run_time=0.5)
        phrases = ["change", "sensor", "control center", "effector", "opposing response"]
        for i, phrase in enumerate(phrases):
            self.at(phrase)
            anims = [FadeIn(nodes[i], scale=0.9)]
            if i:
                anims.insert(0, GrowArrow(links[i - 1]))
            if i == 4:
                anims.append(GrowArrow(links[4]))
            self.play(*anims, run_time=0.65)
        self.at("Sweat glands are the effectors")
        gland = build_skin_inset(center=(0, -1.55, 0), scale=0.55, wet=True)
        self.play(FadeIn(gland), Indicate(nodes[3], color=TEAL), run_time=0.9)
        self.at("combine parts")
        compact, compact_links = loop_nodes(compact=True)
        compact.shift(DOWN * 0.15)
        compact_links.shift(DOWN * 0.15)
        self.play(FadeOut(gland), Transform(nodes, compact), Transform(links, compact_links), run_time=1.1)
        self.at("map is useful")
        note = caption("useful map — not anatomy for every case", size=30, color=GREY, y=-2.95)
        self.play(FadeIn(note), run_time=0.7)
        self.finish()


def thermostat_cartoon():
    box = RoundedRectangle(corner_radius=0.22, width=4.1, height=4.5,
                           color=GREY, stroke_width=4, fill_color=GREY,
                           fill_opacity=0.08).move_to([-3.6, 0.0, 0])
    breathe_fill(box, low=0.12, high=0.42, speed=1.35)
    state = ValueTracker(0.0)
    gauge = dial(state, center=[-3.6, 0.65, 0], radius=1.25,
                 label="off / on", color=YELLOW, fmt="{:.0f}", scale=1, size=34)
    labels = VGroup(*[chip(t, c, size=25, pad=0.14) for t, c in
                      (("sense", BLUE), ("compare", YELLOW), ("act", TEAL))])
    labels.arrange(RIGHT, buff=0.18).move_to([-3.6, -1.55, 0])
    g = VGroup(box, gauge, labels)
    g.box, g.gauge, g.labels, g.state = box, gauge, labels, state
    return g


class S10Thermostat(FilmSpoken):
    def construct(self):
        therm = thermostat_cartoon()
        body = build_person(center=(3.5, -0.15, 0), scale=1.03, heart_fast=False)
        self.at("house thermostat")
        self.play(FadeIn(therm.box), FadeIn(therm[1]), run_time=0.8)
        self.at("sense compare act")
        self.play(LaggedStart(*[FadeIn(x, shift=UP * 0.1) for x in therm[2]], lag_ratio=0.25),
                  therm.state.animate.set_value(1.0), run_time=1.1)
        self.play(therm.state.animate.set_value(0.0), run_time=0.55)
        self.at("A body is richer")
        self.play(FadeIn(body, shift=LEFT * 0.2), therm.animate.set_opacity(0.35), run_time=0.8)
        self.at("Many sensors and effectors")
        sensors = VGroup(*[Dot(p, radius=0.13, color=BLUE) for p in
                           ([3.5, 2.15, 0], [2.65, 0.55, 0], [4.3, 0.45, 0])])
        responses = VGroup(
            arrow([3.5, 0.8, 0], [2.2, -0.2, 0], TEAL, 3, 0.15),
            arrow([3.5, 0.55, 0], [4.9, -0.35, 0], TEAL, 6, 0.2),
            arrow([3.5, 0.2, 0], [3.55, -1.65, 0], TEAL, 9, 0.24),
        )
        self.play(LaggedStart(*[FadeIn(x, scale=1.5) for x in sensors], lag_ratio=0.2),
                  LaggedStart(*[GrowArrow(a) for a in responses], lag_ratio=0.2), run_time=1.2)
        self.at("responses are graded")
        self.play(*[Indicate(a, color=TEAL, scale_factor=1.05) for a in responses], run_time=0.9)
        self.at("No one sets a dial")
        self.play(FadeOut(therm), body.animate.shift(LEFT * 3.5),
                  VGroup(sensors, responses).animate.shift(LEFT * 3.5), run_time=1.0)
        self.finish()


class S11GradualReturn(FilmSpoken):
    def construct(self):
        # Exponential recovery: y(t) = rest + excess * exp(-t/tau).
        rest, excess, tau = 0.8, 3.0, 2.3
        recovery = lambda t: rest + excess * np.exp(-t / tau)
        plot = Plot(box=(-5.65, 5.4, -2.2, 2.65), xr=(0, 8), yr=(0, 4.2),
                    xticks=[0, 2, 4, 6, 8], yticks=[], xlabel="time after climbing",
                    ylabel="heart rate", color=GREY, size=24, label_size=28)
        band = Rectangle(width=11.05, height=0.72, stroke_width=0,
                         fill_color=GOLD, fill_opacity=0.25).move_to([-.125, plot.pt(0, rest)[1], 0])
        breathe_fill(band, low=0.18, high=0.34, speed=0.9)
        band_lab = T("resting range", 28, GOLD).move_to([3.9, plot.pt(0, rest)[1], 0])
        band_lab.layout_ok = True
        t = ValueTracker(0.0)
        curve = plot.live_curve(recovery, t, color=TEXT, width=7)
        dot = plot.dot(lambda: t.get_value(), lambda: recovery(t.get_value()), color=TEXT, ring=TEAL, radius=0.14)
        self.at("correction also takes time")
        self.play(Create(plot), FadeIn(band), FadeIn(band_lab), run_time=0.9)
        self.at("does not snap to rest")
        self.add(curve, dot)
        self.play(t.animate.set_value(1.1), run_time=1.25, rate_func=linear)
        self.at("falls fastest at first")
        self.play(t.animate.set_value(3.8), run_time=1.45, rate_func=linear)
        self.at("approaches its resting range")
        self.play(t.animate.set_value(8.0), run_time=2.0, rate_func=linear)
        self.add(scope_tag("schematic"))
        self.finish()


class S12Handoff(FilmSpoken):
    def construct(self):
        names = ["change", "sensor", "control center", "effector", "response"]
        colors = [RED, BLUE, YELLOW, TEAL, TEAL]
        stones = VGroup(*[RoundedRectangle(corner_radius=0.22, width=2.25, height=1.25,
                                           color=c, stroke_width=4, fill_color=c, fill_opacity=0.12)
                          for c in colors])
        stones.arrange(RIGHT, buff=0.25).move_to([0, 0.4, 0])
        labels = VGroup(*[fit_text(n, max_w=1.95, size=27, color=c, max_lines=2).move_to(s)
                          for n, c, s in zip(names, colors, stones)])
        for label in labels:
            label.layout_ok = True  # deliberate stepping-stone labels
        marker = Dot(stones[0].get_center() + UP * 0.8, radius=0.16, color=TEXT,
                     stroke_color=GOLD, stroke_width=3)
        self.at("simulation to test this map")
        self.play(LaggedStart(*[FadeIn(VGroup(s, l), shift=UP * 0.15)
                                for s, l in zip(stones, labels)], lag_ratio=0.12), run_time=1.1)
        self.add(marker)
        self.at("one step at a time")
        self.play(Succession(*[marker.animate(run_time=0.48).move_to(s.get_center() + UP * 0.8)
                               for s in stones[1:]]))
        self.at("second film compares")
        tiles = VGroup(*[RoundedRectangle(corner_radius=0.14, width=1.25, height=0.72,
                                          color=GREY, stroke_width=3, fill_color=GREY,
                                          fill_opacity=0.08) for _ in range(4)])
        tiles.arrange(RIGHT, buff=0.3).move_to([0, -2.2, 0])
        icons = VGroup(
            Circle(radius=0.17, color=RED, fill_opacity=0.3),
            Ellipse(width=0.55, height=0.28, color=GREEN, fill_opacity=0.2).rotate(0.5),
            VGroup(Line(DOWN * 0.22, UP * 0.22, color=GOLD), Line(ORIGIN, DL * 0.25, color=GOLD), Line(ORIGIN, DR * 0.25, color=GOLD)),
            Circle(radius=0.22, color=BLUE, fill_opacity=0.15),
        )
        for icon, tile in zip(icons, tiles):
            icon.move_to(tile)
        tag = T("compare next", 24, GREY).next_to(tiles, DOWN, buff=0.18)
        self.play(LaggedStart(*[FadeIn(VGroup(tl, ic), shift=UP * 0.18)
                                for tl, ic in zip(tiles, icons)], lag_ratio=0.2), FadeIn(tag), run_time=1.0)
        self.finish()


class S13End(EndCard):
    LINE = "When internal conditions drift, opposing responses move them toward their range."
