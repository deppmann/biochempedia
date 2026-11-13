"""What Becomes a Tree? — animated explainer.

COLOR MAP
  GOLD  = light energy
  TEAL  = carbon dioxide
  BLUE  = water
  GREEN = sugar / newly fixed plant material
  BROWN = wood

The tree world is rebuilt by ``tree_world`` everywhere it returns, so its soil,
trunk, canopy, roots, and gauge never drift between scenes.
"""
from bp_parts import *


BROWN = "#A9754F"
SOIL = "#72523C"
LEAF = "#6DAA57"
OXYGEN = "#C9D6E5"
TREE_X = 1.35
SOIL_Y = -2.15


def arrow(a, b, color=TEXT, width=5, tip=0.22):
    return Arrow(a, b, buff=0.04, color=color, stroke_width=width,
                 tip_length=tip, max_tip_length_to_length_ratio=0.35)


def shuttle(mob, path, period=4.0, phase=0.0):
    """Move a token back and forth along a visible route indefinitely."""
    mob._shuttle_t = phase * period

    def update(m, dt):
        m._shuttle_t += dt
        alpha = 0.5 - 0.5 * np.cos(TAU * m._shuttle_t / period)
        m.move_to(path.point_from_proportion(alpha))

    return mob.add_updater(update)


def leaf_shape(width=2.6, height=1.25, color=LEAF):
    """A leaf silhouette, not a molecular drawing."""
    body = Ellipse(width=width, height=height, color=color, stroke_width=4,
                   fill_color=color, fill_opacity=0.28).rotate(0.18)
    vein = Line(body.get_left() + RIGHT * 0.15, body.get_right() + LEFT * 0.15,
                color=color, stroke_width=3).rotate(0.18, about_point=body.get_center())
    # Labels and blocks deliberately sit on this low-opacity picture of a leaf.
    body.layout_ok = True
    vein.layout_ok = True
    pulse(body, base=4.0, amp=0.65, speed=1.1)
    return VGroup(body, vein)


def tree_picture(full=True):
    """The single carried tree, always at the same scale and coordinates."""
    h = 4.45 if full else 3.45
    trunk = RoundedRectangle(corner_radius=0.12, width=0.78, height=h,
                             stroke_color=BROWN, stroke_width=4,
                             fill_color=BROWN, fill_opacity=0.70)
    trunk.move_to([TREE_X, SOIL_Y + h / 2, 0])
    roots = VGroup(*[
        Line([TREE_X, SOIL_Y + 0.1, 0], [TREE_X + dx, SOIL_Y - 0.48, 0],
             color=BROWN, stroke_width=5)
        for dx in (-1.25, -0.62, 0.62, 1.25)
    ])
    y = SOIL_Y + h - 0.15
    canopy = VGroup(
        Circle(1.15, color=LEAF, stroke_width=4, fill_color=LEAF, fill_opacity=0.27).move_to([TREE_X - 0.95, y, 0]),
        Circle(1.30, color=LEAF, stroke_width=4, fill_color=LEAF, fill_opacity=0.29).move_to([TREE_X + 0.10, y + 0.40, 0]),
        Circle(1.10, color=LEAF, stroke_width=4, fill_color=LEAF, fill_opacity=0.27).move_to([TREE_X + 1.18, y, 0]),
    )
    # The canopy is a low-opacity background world; foreground labels remain legible on it.
    for crown in canopy:
        crown.layout_ok = True
    pulse(canopy, base=4.0, amp=0.55, speed=1.0)
    return VGroup(roots, trunk, canopy)


def soil_strip():
    return RoundedRectangle(corner_radius=0.12, width=13.0, height=0.78,
                            stroke_color=SOIL, stroke_width=3,
                            fill_color=SOIL, fill_opacity=0.35).move_to([0, SOIL_Y - 0.15, 0])


def soil_gauge(value=0.96):
    """Wide schematic soil-mass gauge; value is deliberately only slightly changed."""
    box = RoundedRectangle(corner_radius=0.16, width=4.1, height=1.0,
                           stroke_color=SOIL, stroke_width=3).move_to([-4.25, -1.15, 0])
    fill = Rectangle(width=3.55 * value, height=0.28, stroke_width=0,
                     fill_color=SOIL, fill_opacity=0.9)
    fill.align_to(box.get_left() + RIGHT * 0.28, LEFT).move_to([box.get_left()[0] + 0.28 + fill.width / 2, -1.32, 0])
    lab = T("soil mass", 28, TEXT).move_to([-4.25, -0.90, 0])
    return VGroup(box, fill, lab)


def seed_picture():
    seed = Ellipse(width=0.55, height=0.32, color=BROWN, stroke_width=4,
                   fill_color=BROWN, fill_opacity=0.85).rotate(-0.25)
    return seed.move_to([-4.4, SOIL_Y + 0.45, 0])


def tree_world(full=True, gauge=True, seed=False):
    """Shared world builder used by every whole-tree scene."""
    g = VGroup(soil_strip(), tree_picture(full=full))
    if gauge:
        g.add(soil_gauge())
    if seed:
        g.add(seed_picture())
    return g


def path_dots():
    """Slow, looping-looking path markers for prediction frames."""
    co2 = Dot([-4.9, 1.15, 0], radius=0.13, color=TEAL)
    water = Dot([-0.2, -2.0, 0], radius=0.13, color=BLUE)
    light = Dot([5.35, 2.55, 0], radius=0.13, color=GOLD)
    routes = (
        Line([-5.0, 1.15, 0], [-0.65, 1.5, 0]),
        Line([-0.3, -1.9, 0], [0.65, -0.35, 0]),
        Line([5.2, 2.55, 0], [3.05, 1.9, 0]),
    )
    for i, (dot, route) in enumerate(zip((co2, water, light), routes)):
        shuttle(dot, route, period=4.2 + i * 0.5, phase=i / 3)
    return VGroup(co2, water, light)


def breathe(mob, lo=0.35, hi=1.0, period=2.4, phase=0.0):
    """Slow whole-object opacity swing so a long hold keeps visible motion."""
    mob._br_t = phase * period

    def update(m, dt):
        m._br_t += dt
        a = lo + (hi - lo) * (0.5 - 0.5 * np.cos(TAU * m._br_t / period))
        m.set_stroke(opacity=a)
        m.set_fill(opacity=a if m.get_fill_opacity() > 0 else 0)

    return mob.add_updater(update)


def prediction_backdrop():
    world = tree_world(full=True, gauge=False)
    co2_path = arrow([-5.2, 1.15, 0], [-0.1, 1.55, 0], TEAL, 6)
    water_path = arrow([-0.4, -2.0, 0], [0.85, -0.15, 0], BLUE, 6)
    light_path = arrow([5.5, 2.65, 0], [2.75, 1.8, 0], GOLD, 6)
    marks = VGroup(*[T("?", 50, c, weight=BOLD).move_to(p) for c, p in (
        (TEAL, [-0.35, 1.85, 0]), (BLUE, [0.35, -0.05, 0]), (GOLD, [3.0, 2.2, 0]))])
    for i, p in enumerate((co2_path, water_path, light_path)):
        breathe(p, 0.3, 1.0, 2.4, phase=i / 3)
    for i, m in enumerate(marks):
        breathe(m, 0.2, 1.0, 1.8, phase=i / 3)
    dots = path_dots()
    for i, d in enumerate(dots):
        breathe(d, 0.15, 1.0, 1.5, phase=i / max(1, len(dots)))
    wash = Rectangle(width=14.2, height=8.2, stroke_width=0, fill_color=GOLD, fill_opacity=0.0)
    wash.layout_ok = True
    wash._w_t = 0.0

    def wash_update(m, dt):
        m._w_t += dt
        m.set_fill(GOLD, opacity=0.09 * (0.5 - 0.5 * np.cos(TAU * m._w_t / 2.8)))

    wash.add_updater(wash_update)
    return VGroup(VGroup(wash, world), co2_path, water_path, light_path, marks, dots)


def prediction_question():
    return question_card("Which paths carry matter — and which carries only energy?",
                         y=2.95, size=28, max_w=5.4, left=-6.2)


def sugar_block(text="SUGAR", size=30):
    return chip(text, GREEN, size)


class S00Hook(SpokenScene):
    def construct(self):
        soil = soil_strip()
        seed = seed_picture()
        gauge = soil_gauge(1.0)
        ghost = tree_picture(full=True).set_opacity(0.13)
        self.add(soil, ghost)
        self.play(GrowFromCenter(seed), FadeIn(gauge), run_time=0.75)

        self.at("What becomes the wood")
        question = T("What becomes the wood?", 38, TEXT, font=TITLE_FONT).move_to([-3.8, 3.25, 0])
        self.play(FadeIn(question, shift=DOWN * 0.12), run_time=0.65)

        self.at("Watch one tiny seed")
        sprout = tree_picture(full=False)
        sprout.scale(0.16, about_point=[TREE_X, SOIL_Y, 0])
        self.play(ReplacementTransform(seed.copy(), sprout), run_time=1.0)

        self.at("tree gains layer after layer")
        tree = tree_picture(full=True)
        self.play(Transform(sprout, tree), FadeOut(ghost), run_time=2.2, rate_func=smooth)
        ring1 = SurroundingRectangle(tree[1], color=BROWN, buff=0.12, stroke_width=4)
        ring2 = SurroundingRectangle(tree[1], color=BROWN, buff=0.24, stroke_width=3).set_opacity(0.65)
        self.play(Create(ring1), Create(ring2), run_time=1.0)
        self.play(FadeOut(ring1), FadeOut(ring2), run_time=0.4)

        self.at("soil gauge barely moves")
        slightly_less = soil_gauge(0.96)
        self.play(Transform(gauge, slightly_less), run_time=1.8)
        tag = scope_tag("size change schematic")
        self.play(FadeIn(tag), run_time=0.4)

        self.at("Something outside the soil")
        outside = VGroup(
            Dot([-4.9, 1.8, 0], radius=0.16, color=TEAL),
            Dot([-3.9, 2.45, 0], radius=0.16, color=GOLD),
            Dot([-2.8, -0.15, 0], radius=0.16, color=BLUE),
        )
        self.play(LaggedStart(*[FadeIn(d, scale=1.6) for d in outside], lag_ratio=0.25), run_time=1.2)
        self.play(outside.animate.shift(RIGHT * 0.45), run_time=1.5, rate_func=there_and_back)
        self.finish()


class S01Title(NarratedScene):
    def construct(self):
        world = tree_world(full=True, gauge=True)
        title = T("What Becomes a Tree?", 44, TEXT, font=TITLE_FONT).move_to([-3.65, 2.75, 0])
        water = VGroup(*[Dot([-0.15 + i * 0.12, -1.8 + i * 0.55, 0], radius=0.09, color=BLUE) for i in range(4)])
        self.add(world)
        self.play(FadeIn(title), water.animate.shift(UP * 0.45),
                  world[1][2].animate.rotate(0.015), run_time=1.25)
        self.play(water.animate.shift(UP * 0.35), world[1][2].animate.rotate(-0.025), run_time=0.55)
        self.finish()


class S02Sort(SpokenScene):
    def construct(self):
        tree = tree_picture(full=False).scale(0.78).move_to([0, -0.35, 0])
        self.add(tree)
        matter_tray = RoundedRectangle(corner_radius=0.2, width=4.3, height=2.05,
                                       stroke_color=TEAL, stroke_width=4).move_to([-4.15, 0.45, 0])
        matter_lab = T("MATTER", 34, TEXT, weight=BOLD).next_to(matter_tray, UP, buff=0.18)
        energy_wire = CubicBezier([1.8, 1.45, 0], [3.0, 2.2, 0], [4.2, 0.4, 0], [5.2, 0.7, 0],
                                  color=GOLD, stroke_width=5)
        machine = VGroup(RoundedRectangle(corner_radius=0.15, width=2.1, height=1.5,
                                          stroke_color=GREY, stroke_width=4),
                         T("BUILDER", 28, TEXT)).move_to([5.1, -0.25, 0])
        machine[1].move_to([5.1, 0.12, 0])
        gear = Circle(radius=0.24, color=GOLD, stroke_width=5).move_to([5.1, -0.62, 0])
        gear.add_updater(lambda m, dt: m.rotate(1.4 * dt))

        self.at("Matter has mass")
        self.play(FadeIn(matter_tray), FadeIn(matter_lab), run_time=0.7)
        co2 = chip("carbon dioxide", TEAL, 28).move_to([-4.65, 0.65, 0])
        water = chip("water", BLUE, 28).move_to([-3.25, 0.05, 0])
        self.play(FadeIn(co2, shift=DOWN * 0.2), FadeIn(water, shift=DOWN * 0.2), run_time=0.8)

        self.at("Energy can move")
        self.play(Create(energy_wire), FadeIn(machine), FadeIn(gear), run_time=0.8)
        pulse_dot = Dot(energy_wire.get_start(), radius=0.15, color=GOLD)
        energy_lab = T("ENERGY", 32, GOLD, weight=BOLD).move_to([3.3, 2.35, 0])
        self.play(FadeIn(energy_lab), MoveAlongPath(pulse_dot, energy_wire), run_time=1.6, rate_func=linear)
        shuttle(pulse_dot, energy_wire, period=3.6)

        self.at("does not become wood")
        product = Rectangle(width=0.62, height=1.55, color=BROWN, stroke_width=4,
                            fill_color=BROWN, fill_opacity=0.65).move_to([5.1, -2.0, 0])
        self.play(Indicate(pulse_dot, color=GOLD, scale_factor=1.4),
                  GrowFromEdge(product, DOWN), run_time=1.0)

        self.at("Sunlight reaches the leaf")
        leaf = leaf_shape(2.0, 0.9).move_to([2.65, 0.9, 0])
        self.play(FadeIn(leaf), MoveAlongPath(pulse_dot, energy_wire.copy()), run_time=1.5, rate_func=linear)
        breathe(leaf, 0.35, 1.0, 2.2)
        breathe(energy_wire, 0.35, 1.0, 2.2, phase=0.5)
        breathe(matter_tray, 0.4, 1.0, 2.6, phase=0.25)

        self.at("electricity runs a factory")
        self.play(product.animate.stretch(1.16, 1), run_time=2.1, rate_func=linear)
        self.play(product.animate.set_fill(BROWN, opacity=0.82), run_time=0.6)
        self.finish()


class S03Inputs(SpokenScene):
    def construct(self):
        leaf = leaf_shape(8.2, 4.0).move_to([0.65, 0.55, 0])
        leaf_lab = T("LEAF", 30, LEAF, weight=BOLD).move_to([-2.15, 2.65, 0])
        self.add(leaf)
        roots = VGroup(*[Line([-4.6, -2.75, 0], [-4.6 + dx, -1.25, 0], color=BROWN, stroke_width=5)
                         for dx in (-0.8, -0.25, 0.3, 0.85)])
        self.add(roots)

        self.at("moves upward")
        drops = VGroup(*[Dot([-4.8 + i * 0.25, -2.45, 0], radius=0.13, color=BLUE) for i in range(3)])
        self.play(drops.animate.shift(UP * 2.0 + RIGHT * 2.0), FadeIn(leaf_lab), run_time=1.6)

        self.at("Carbon dioxide enters")
        opening = Ellipse(width=1.0, height=0.35, color=TEAL, stroke_width=4).move_to([3.2, 0.35, 0])
        co2 = VGroup(*[chip("CO₂", TEAL, 26).move_to([6.0, y, 0]) for y in (1.2, 0.35, -0.5)])
        self.play(Create(opening), co2.animate.shift(LEFT * 1.25), run_time=1.5)

        self.at("Light arrives")
        rays = VGroup(*[Arrow([x, 3.25, 0], [x - 0.25, 2.1, 0], buff=0, color=GOLD,
                              stroke_width=6, tip_length=0.18) for x in (-0.2, 1.1, 2.4)])
        self.play(LaggedStart(*[GrowArrow(r) for r in rays], lag_ratio=0.2), run_time=1.2)

        self.at("build sugar")
        water = chip("WATER", BLUE, 28).move_to([-1.6, 0.0, 0])
        carbon = chip("CARBON DIOXIDE", TEAL, 28).move_to([1.5, 0.0, 0])
        sugar = sugar_block().move_to([0.0, 0.0, 0])
        self.play(FadeOut(drops), FadeOut(co2), FadeIn(water), FadeIn(carbon), run_time=0.65)
        self.play(ReplacementTransform(VGroup(water, carbon), sugar),
                  rays.animate.set_opacity(0.35), run_time=1.3)

        self.at("Oxygen leaves")
        oxygen = chip("OXYGEN", OXYGEN, 28).move_to([5.55, 2.05, 0])
        self.play(FadeIn(oxygen, shift=LEFT * 2.2 + DOWN * 0.7), run_time=1.35)

        self.at("word equation is a summary")
        equation = fit_text("carbon dioxide + water  →  sugar + oxygen", max_w=11.6,
                            size=34, color=TEXT, max_lines=1).move_to([0, -3.2, 0])
        self.play(FadeIn(equation, shift=UP * 0.1), run_time=0.75)
        self.play(sugar.animate.shift(UP * 0.12), run_time=1.3, rate_func=there_and_back)
        self.finish()


class S04Predict(SpokenScene):
    def construct(self):
        backdrop = prediction_backdrop()
        self.add(backdrop)
        self.at("Which paths carry matter")
        q = prediction_question()
        self.play(FadeIn(q.question, shift=DOWN * 0.1), run_time=0.7)
        self.play(Indicate(backdrop[1], color=TEAL), Indicate(backdrop[2], color=BLUE), run_time=1.7)
        self.at("Which path carries only energy")
        self.play(Indicate(backdrop[3], color=GOLD), run_time=1.6)
        self.at("Follow each color")
        self.play(LaggedStart(*[Indicate(m, color=m.get_color(), scale_factor=1.35) for m in backdrop[4]], lag_ratio=0.25),
                  run_time=1.8)
        self.finish()


class S05Pause(PredictPause):
    QUESTION = "Which paths carry matter — and which carries only energy?"
    SECONDS = 4.5
    CARD = {"y": 2.95, "size": 28, "max_w": 5.4, "left": -6.2}

    def backdrop(self):
        return prediction_backdrop()


class S06Reveal(SpokenScene):
    def construct(self):
        world = tree_world(full=True, gauge=False)
        self.add(world)
        co2 = chip("CARBON DIOXIDE", TEAL, 28).move_to([-4.65, 1.15, 0])
        water = chip("WATER", BLUE, 28).move_to([-3.65, -0.65, 0])
        light = chip("LIGHT", GOLD, 28).move_to([5.25, 3.15, 0])

        self.at("paths carry matter")
        self.play(FadeIn(co2), FadeIn(water), run_time=0.55)
        self.play(co2.animate.move_to([-0.25, 1.5, 0]),
                  water.animate.move_to([0.25, 0.35, 0]), run_time=1.5)

        self.at("light path carries energy")
        wire = CubicBezier([4.75, 2.65, 0], [4.0, 2.9, 0], [3.0, 2.5, 0], [2.55, 1.7, 0],
                           color=GOLD, stroke_width=5)
        self.play(FadeIn(light), Create(wire), run_time=0.8)
        gold_dot = Dot(wire.get_start(), radius=0.14, color=GOLD)
        self.play(MoveAlongPath(gold_dot, wire), run_time=1.15, rate_func=linear)

        self.at("powers sugar building")
        sugar = sugar_block().move_to([0.1, 1.0, 0])
        self.play(ReplacementTransform(VGroup(co2, water), sugar), run_time=1.15)
        layer = RoundedRectangle(corner_radius=0.12, width=1.18, height=4.52, color=BROWN,
                                 stroke_width=4, fill_color=BROWN, fill_opacity=0.48).move_to(world[1][1])
        self.play(Transform(sugar, layer), run_time=1.35)
        self.play(gold_dot.animate.move_to(wire.get_start()), run_time=0.65)

        self.at("conditions limit its speed")
        speed = dial(ValueTracker(0.62), center=[-4.55, 0.0, 0], radius=1.2,
                     label="building speed", color=GREEN, fmt="{:.0f}%")
        self.play(FadeIn(speed), run_time=0.7)

        self.at("first half explains")
        rule = fit_text("Light supplies energy; carbon dioxide and water supply matter.",
                        max_w=5.6, size=30, color=TEXT, max_lines=2).move_to([-3.55, 2.75, 0])
        self.play(FadeIn(rule, shift=DOWN * 0.1), run_time=0.8)

        self.at("second half reminds us")
        tab = chip("conditions limit speed", GREY, 24).move_to([-4.6, -1.35, 0])
        self.play(ReplacementTransform(speed, tab), rule.animate.move_to([-3.45, 2.9, 0]), run_time=1.0)
        self.play(gold_dot.animate.move_to(wire.get_end()), run_time=1.5, rate_func=there_and_back)
        self.finish()


class S07Chloroplast(SpokenScene):
    def construct(self):
        leaf = leaf_shape(9.6, 4.8).move_to([-0.8, 0.35, 0])
        self.add(leaf)
        cell = RoundedRectangle(corner_radius=0.35, width=7.6, height=3.6,
                                stroke_color=TEXT, stroke_width=4, fill_color=GREY,
                                fill_opacity=0.08).move_to([-0.8, 0.35, 0])
        self.at("inside chloroplasts")
        self.play(Create(cell), run_time=1.0)
        chloros = VGroup(*[
            chip("CHLOROPLAST", LEAF, 24).move_to([-2.5 + (i % 2) * 3.4, 1.5 - (i // 2) * 2.6, 0])
            for i in range(4)
        ])
        self.play(LaggedStart(*[FadeIn(c, scale=0.8) for c in chloros], lag_ratio=0.16), run_time=1.3)

        self.at("mostly in leaves")
        self.play(chloros.animate.scale(1.02), run_time=1.2, rate_func=there_and_back)

        self.at("Chlorophyll inside them")
        patch = RoundedRectangle(corner_radius=0.1, width=1.35, height=0.38,
                                 color=LEAF, stroke_width=4, fill_color=LEAF, fill_opacity=0.8)
        patch.move_to([0.4, 0.55, 0])
        patch_lab = T("chlorophyll", 26, TEXT).next_to(patch, DOWN, buff=0.14)
        ray = arrow([4.8, 2.8, 0], patch.get_right(), GOLD, 7)
        self.play(FadeIn(patch), FadeIn(patch_lab), GrowArrow(ray), run_time=1.25)
        self.play(ShowPassingFlash(ray.copy().set_stroke(width=12), time_width=0.5), run_time=1.1)

        self.at("Roots which sit in darkness")
        root_cell = RoundedRectangle(corner_radius=0.3, width=4.4, height=2.5,
                                     stroke_color=BROWN, stroke_width=4, fill_color=SOIL,
                                     fill_opacity=0.14).move_to([3.9, -1.45, 0])
        root_lab = T("root cell", 30, BROWN).move_to([3.9, -0.75, 0])
        none = T("no chloroplasts", 28, TEXT).move_to([3.9, -1.65, 0])
        self.play(FadeOut(ray), FadeIn(root_cell), FadeIn(root_lab), FadeIn(none), run_time=1.05)

        self.at("bacteria do the work")
        bacterium = VGroup(RoundedRectangle(corner_radius=0.45, width=2.6, height=1.15,
                                            stroke_color=TEAL, stroke_width=4,
                                            fill_color=TEAL, fill_opacity=0.18),
                           T("bacterium", 26, TEXT)).move_to([4.0, 1.15, 0])
        no_chl = T("no chloroplast", 26, TEAL).next_to(bacterium, DOWN, buff=0.18)
        self.play(FadeOut(root_cell), FadeOut(root_lab), FadeOut(none), FadeIn(bacterium), FadeIn(no_chl), run_time=1.0)
        self.play(bacterium.animate.shift(UP * 0.1), run_time=1.25, rate_func=there_and_back)
        self.finish()


class S08Routes(SpokenScene):
    def construct(self):
        world = tree_world(full=True, gauge=False)
        self.add(world)
        sugar = sugar_block().move_to([-1.45, 1.25, 0])
        self.play(FadeIn(sugar, scale=0.75), run_time=0.65)

        self.at("Some is used now")
        cell = VGroup(Circle(radius=0.72, color=TEXT, stroke_width=4), T("CELL", 26, TEXT)).move_to([-4.7, 1.6, 0])
        p1 = arrow(sugar.get_left(), cell.get_right(), GREEN, 5)
        token1 = Circle(radius=0.18, color=GREEN, stroke_width=4,
                        fill_color=GREEN, fill_opacity=0.85).move_to(sugar)
        self.play(Create(p1), FadeIn(cell), MoveAlongPath(token1, p1), run_time=1.45)
        self.play(cell.animate.set_fill(GOLD, opacity=0.28), run_time=0.8)

        self.at("linked into starch")
        store = VGroup(RoundedRectangle(corner_radius=0.16, width=2.4, height=1.7,
                                        stroke_color=GREEN, stroke_width=4),
                       T("STARCH", 28, GREEN)).move_to([-4.7, -1.05, 0])
        p2 = arrow(sugar.get_left() + DOWN * 0.12, store.get_right(), GREEN, 5)
        stacks = VGroup(*[Rectangle(width=0.42, height=0.24, color=GREEN, fill_color=GREEN,
                                    fill_opacity=0.65).move_to([-5.15 + i * 0.47, -1.48, 0]) for i in range(3)])
        self.play(Create(p2), FadeIn(store), LaggedStart(*[FadeIn(s, shift=UP * 0.2) for s in stacks], lag_ratio=0.2), run_time=1.4)

        self.at("rebuilt into wood")
        p3 = arrow(sugar.get_bottom(), [1.35, -0.2, 0], GREEN, 5)
        ring = SurroundingRectangle(world[1][1], color=BROWN, buff=0.18, stroke_width=5)
        new_leaf = leaf_shape(1.4, 0.65).move_to([3.0, 2.8, 0])
        self.play(Create(p3), Create(ring), FadeIn(new_leaf, shift=DOWN * 0.2), run_time=1.3)

        self.at("Each route starts")
        self.play(Indicate(sugar, color=GREEN, scale_factor=1.25),
                  token1.animate.move_to(sugar.get_left() + LEFT * 0.28), run_time=1.25)
        self.play(sugar.animate.shift(UP * 0.12), run_time=1.2, rate_func=there_and_back)
        self.finish()


def rabbit_picture():
    body = Ellipse(width=1.55, height=1.15, color=TEXT, stroke_width=4, fill_color=TEXT, fill_opacity=0.12)
    head = Circle(radius=0.48, color=TEXT, stroke_width=4, fill_color=TEXT, fill_opacity=0.12).move_to([0.72, 0.42, 0])
    ears = VGroup(Ellipse(width=0.25, height=0.85, color=TEXT, stroke_width=3).move_to([0.55, 1.02, 0]),
                    Ellipse(width=0.25, height=0.85, color=TEXT, stroke_width=3).move_to([0.88, 1.04, 0]))
    return VGroup(body, head, ears)


def fox_picture():
    body = Ellipse(width=1.8, height=1.05, color=BROWN, stroke_width=4, fill_color=BROWN, fill_opacity=0.16)
    head = Polygon([0.55, 0.25, 0], [1.35, 0.75, 0], [1.15, -0.05, 0], color=BROWN,
                   stroke_width=4, fill_color=BROWN, fill_opacity=0.16)
    tail = ArcBetweenPoints([-0.7, 0.15, 0], [-1.4, 0.7, 0], angle=-1.4, color=BROWN, stroke_width=7)
    return VGroup(body, head, tail)


class S09Foodweb(SpokenScene):
    def construct(self):
        sun = Circle(radius=0.48, color=GOLD, stroke_width=5, fill_color=GOLD, fill_opacity=0.4).move_to([-5.6, 2.6, 0])
        clover = VGroup(*[Circle(radius=0.34, color=LEAF, stroke_width=4, fill_color=LEAF,
                                fill_opacity=0.3).move_to([-4.7 + 0.35 * np.cos(i * TAU / 3), -1.25 + 0.35 * np.sin(i * TAU / 3), 0]) for i in range(3)])
        stem = Line([-4.7, -2.0, 0], [-4.7, -1.2, 0], color=LEAF, stroke_width=6)
        rabbit = bob(rabbit_picture().move_to([-0.3, -1.1, 0]), amp=0.06, speed=1.4, seed=1)
        fox = bob(fox_picture().move_to([4.25, -1.1, 0]), amp=0.06, speed=1.2, seed=2)
        origin = arrow(sun.get_bottom(), clover.get_top(), GOLD, 5)
        self.play(FadeIn(sun), Create(origin), FadeIn(clover), FadeIn(stem), run_time=1.0)

        self.at("move through a food web")
        route1 = arrow(clover.get_right(), rabbit.get_left(), GREEN, 5)
        route2 = arrow(rabbit.get_right(), fox.get_left(), GREEN, 5)
        self.play(FadeIn(rabbit), FadeIn(fox), Create(route1), Create(route2), run_time=1.1)

        self.at("rabbit eats clover")
        token = Circle(radius=0.2, color=GREEN, stroke_width=4, fill_color=GREEN, fill_opacity=0.8).move_to(clover)
        self.play(MoveAlongPath(token, route1), rabbit.animate.scale(1.04), run_time=1.3)

        self.at("fox eats the rabbit")
        self.play(MoveAlongPath(token, route2), fox.animate.scale(1.04), run_time=1.3)

        self.at("energy captured by a producer")
        producer = T("PRODUCER", 30, LEAF, weight=BOLD).next_to(clover, DOWN, buff=0.25)
        self.play(FadeIn(producer), ShowPassingFlash(origin.copy().set_stroke(width=11), time_width=0.5), run_time=1.2)

        self.at("Almost every food web")
        self.play(token.animate.move_to(clover), run_time=1.4)

        self.at("chemical energy instead")
        cave = VGroup(Arc(radius=0.8, start_angle=0, angle=PI, color=GREY, stroke_width=5),
                       Line([-0.8, 0, 0], [0.8, 0, 0], color=GREY, stroke_width=5),
                       T("chemical energy", 26, TEAL).move_to([0, -0.45, 0])).move_to([4.7, 2.2, 0])
        self.play(FadeIn(cave), run_time=0.9)
        self.play(token.animate.shift(UP * 0.1), run_time=1.1, rate_func=there_and_back)
        self.finish()


class S10Return(SpokenScene):
    def construct(self):
        soil = soil_strip()
        seed = seed_picture()
        gauge = soil_gauge(0.96)
        tree = tree_picture(full=True)
        self.play(FadeIn(soil), GrowFromCenter(seed), FadeIn(gauge), run_time=0.7)

        self.at("Return to the tree")
        self.play(ReplacementTransform(seed.copy(), tree), run_time=1.6)

        self.at("soil did not need")
        self.play(Indicate(gauge, color=SOIL, scale_factor=1.04), run_time=1.2)

        self.at("Matter arrived mainly")
        co2 = chip("CARBON DIOXIDE", TEAL, 28).move_to([-0.25, 1.5, 0])
        water = chip("WATER", BLUE, 28).move_to([0.2, 0.35, 0])
        self.play(FadeIn(co2, shift=LEFT * 4.6 + DOWN * 0.1), run_time=1.45)

        self.at("water also supplying")
        self.play(FadeIn(water, shift=LEFT * 4.1 + DOWN * 0.6), run_time=1.35)

        self.at("Light supplied the energy")
        wire = CubicBezier([5.3, 2.6, 0], [4.2, 3.0, 0], [3.1, 2.4, 0], [2.55, 1.7, 0],
                           color=GOLD, stroke_width=6)
        light_dot = Dot(wire.get_start(), radius=0.16, color=GOLD)
        self.play(Create(wire), MoveAlongPath(light_dot, wire), run_time=1.5, rate_func=linear)
        sugar = sugar_block().move_to([0.0, 1.0, 0])
        self.play(ReplacementTransform(VGroup(co2, water), sugar), run_time=1.0)

        self.at("Light supplies the energy")
        energy_rule = T("LIGHT → ENERGY", 30, GOLD, weight=BOLD).move_to([-4.55, 2.8, 0])
        self.play(FadeIn(energy_rule), light_dot.animate.move_to(wire.get_start()), run_time=1.2)

        self.at("supply the matter")
        matter_rule = T("CO₂ + WATER → MATTER", 30, TEXT, weight=BOLD).move_to([-3.9, 2.05, 0])
        self.play(FadeIn(matter_rule), run_time=0.75)
        layer = SurroundingRectangle(tree[1], color=BROWN, buff=0.2, stroke_width=5)
        self.play(Transform(sugar, layer), run_time=1.25)

        self.at("make living material")
        new_leaf = leaf_shape(1.5, 0.65).move_to([3.05, 2.75, 0])
        feed = arrow([2.65, 1.25, 0], [5.25, 0.45, 0], GREEN, 5)
        other_life = T("other life", 30, GREEN).move_to([5.25, 0.0, 0])
        self.play(FadeIn(new_leaf, shift=DOWN * 0.2), Create(feed), FadeIn(other_life), run_time=1.3)
        self.play(light_dot.animate.move_to(wire.get_end()), run_time=1.5, rate_func=there_and_back)
        self.finish()


class S11End(EndCard):
    LINE = "Light supplies the energy; carbon dioxide and water supply the matter."
