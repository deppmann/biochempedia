"""Schematic cutaways for Why Do Sprouting Peas Get Warm?

Colour map from the lesson's earlier film: glucose and stored energy GOLD,
oxygen BLUE, carbon dioxide GREY, water CYAN, cell work GREEN, thermal
energy ORANGE, mitochondria PURPLE, cells CREAM.
"""
from bp_parts import *
from bp_style import EndCard

GLUCOSE, OXYGEN, CO2 = GOLD, BLUE, GREY
WATER, WORK, HEAT = "#4FC3C9", GREEN, "#F29E4C"
MITO, CELL = "#B58CD9", "#F3E7C9"
RULE = "Respiration releases stored food energy for cell work and as thermal energy."


def point(x, y):
    return np.array([x, y, 0.0])


def label(text, x, y, color=TEXT, size=30):
    return T(text, size=size, color=color, weight=MEDIUM).move_to(point(x, y))


def arrow(start, end, color=TEXT, width=5):
    return Arrow(start, end, buff=0, color=color, stroke_width=width, tip_length=0.18)


def flow_arrow(start, end, color=GLUCOSE):
    direction = normalize(end - start)
    side = rotate_vector(direction, PI / 2)
    shoulder = end - 0.45 * direction
    return Polygon(start + 0.14 * side, shoulder + 0.14 * side, shoulder + 0.29 * side,
                   end, shoulder - 0.29 * side, shoulder - 0.14 * side, start - 0.14 * side,
                   color=color, stroke_width=2.2, fill_color=color, fill_opacity=0.90)


def plant_cell():
    return RoundedRectangle(
        width=12.25, height=5.55, corner_radius=0.64, stroke_color=CELL,
        stroke_width=4, fill_color=CELL, fill_opacity=0.24,
    ).move_to(point(0, 0.03))


def rounded_block(at, color=GLUCOSE, width=0.48, height=0.33):
    return RoundedRectangle(
        width=width, height=height, corner_radius=0.08, stroke_color=color,
        stroke_width=2.4, fill_color=color, fill_opacity=0.82,
    ).move_to(at)


def drop(at):
    return VMobject(color=WATER, stroke_width=2.4, fill_color=WATER, fill_opacity=0.78).set_points_smoothly([
        at + point(0, 0.26), at + point(0.18, -0.03), at + point(0, -0.20),
        at + point(-0.18, -0.03), at + point(0, 0.26),
    ])


def gas(at, color=OXYGEN):
    return VGroup(*[
        Dot(at + point(dx, dy), color=color, radius=0.16)
        for dx, dy in ((-0.36, 0.06), (-0.13, -0.28), (0.03, 0.20), (0.29, -0.09), (0.47, 0.23))
    ])


def thermometer(x, level):
    bottom = -0.83
    tube = RoundedRectangle(
        width=0.71, height=3.12, corner_radius=0.23, color=TEXT, stroke_width=2.8,
        fill_color=BG, fill_opacity=0.88,
    ).move_to(point(x, 0.59))
    ticks = VGroup(*[
        Line(point(x + 0.42, y), point(x + 0.59, y), color=TEXT, stroke_width=2)
        for y in (-0.38, 0.02, 0.42, 0.82, 1.22, 1.62)
    ])

    def column():
        top = level.get_value()
        return Rectangle(width=0.38, height=top - bottom, stroke_width=0,
                         fill_color=HEAT, fill_opacity=1).move_to(point(x, (top + bottom) / 2))

    bulb = Dot(point(x, bottom), radius=0.30, color=HEAT, stroke_color=TEXT, stroke_width=2.5)
    return VGroup(tube, ticks, always_redraw(column), bulb)


ROOM, WARM = -0.38, 0.97
LEFT_FLASK, RIGHT_FLASK = -3.42, 3.42


def pea(at, living=True, radius=0.32):
    color = CELL if living else GREY
    body = Circle(radius=radius, color=color, fill_color=color, fill_opacity=0.77, stroke_width=2).move_to(at)
    hilite = Arc(radius=0.63 * radius, start_angle=0.88, angle=1.20, color=TEXT,
                 stroke_width=2).move_arc_center_to(at)
    return VGroup(body, hilite)


def thermos(x, level, living=True):
    shell = RoundedRectangle(width=5.25, height=5.08, corner_radius=0.56, color=GREY,
                             stroke_width=4, fill_color=GREY, fill_opacity=0.34).move_to(point(x, -0.10))
    glass = RoundedRectangle(width=4.65, height=4.58, corner_radius=0.42, color=TEXT,
                             stroke_width=2.8, fill_color=BG, fill_opacity=0.71).move_to(point(x, -0.10))
    if living:
        def warmth_tint(mob):
            fraction = np.clip((level.get_value() - ROOM) / (1.62 - ROOM), 0, 1)
            mob.set_fill(interpolate_color(ManimColor(BG), ManimColor("#AF5D34"), fraction), opacity=0.71)

        glass.add_updater(warmth_tint, call_updater=True)
    cap = RoundedRectangle(width=2.88, height=0.40, corner_radius=0.12, color=GREY,
                           stroke_width=3, fill_color=GREY, fill_opacity=0.75).move_to(point(x, 2.49))
    ribs = VGroup(*[
        Line(point(x + dx, 2.40), point(x + dx, 2.57), color=BG, stroke_width=2)
        for dx in (-0.95, -0.63, -0.31, 0, 0.31, 0.63, 0.95)
    ])
    peas = VGroup(*[
        pea(point(x + dx, y), living)
        for dx, y in ((-1.58, -1.95), (-0.84, -1.95), (-0.10, -1.95), (0.64, -1.95), (1.38, -1.95),
                      (-1.24, -1.30), (-0.51, -1.30), (0.23, -1.30), (0.97, -1.30))
    ])
    sprouts = VGroup(*[
        ArcBetweenPoints(point(x + dx, -1.00), point(x + dx + 0.20, -0.58), angle=-1,
                         color=WORK, stroke_width=4)
        for dx in (-1.24, -0.51, 0.23)
    ]) if living else VGroup()
    title = label("Sprouting peas" if living else "Boiled, cooled peas", x, 3.10, CELL if living else TEXT, 36)
    return VGroup(shell, glass, cap, ribs, peas, sprouts, thermometer(x + 1.40, level)), title, peas


def thermos_pair(left, right):
    return thermos(LEFT_FLASK, left), thermos(RIGHT_FLASK, right, False)


def room_marker():
    dashes = VGroup(*[
        DashedLine(point(x + 0.46, ROOM), point(x + 0.91, ROOM),
                   dash_length=0.08, color=TEXT, stroke_width=3)
        for x in (LEFT_FLASK, RIGHT_FLASK)
    ])
    return VGroup(dashes, label("Room temperature", 0, -3.15))


def leaf(at, width=1.48, height=0.73):
    a, b = at - RIGHT * width / 2, at + RIGHT * width / 2
    outline = ArcBetweenPoints(a, b, angle=-1.32, color=WORK, fill_color=WORK, fill_opacity=0.70)
    outline.append_vectorized_mobject(ArcBetweenPoints(b, a, angle=-1.32))
    outline.stretch_to_fit_height(height).move_to(at)
    vein = Line(a + RIGHT * 0.15, b - RIGHT * 0.22, color=BG, stroke_width=3)
    return VGroup(outline, vein)


def sun(at):
    disk = Dot(at, radius=0.29, color=YELLOW)
    rays = VGroup(*[
        Line(at + 0.39 * rotate_vector(RIGHT, theta), at + 0.56 * rotate_vector(RIGHT, theta),
             color=YELLOW, stroke_width=3)
        for theta in np.linspace(0, TAU, 8, endpoint=False)
    ])
    return VGroup(disk, rays)


PATH_Y = 0.28


def reaction_steps(y=PATH_Y):
    return VGroup(*[
        Circle(radius=0.29, color=CELL, stroke_width=2.5, fill_color=BG, fill_opacity=0.96).move_to(point(x, y))
        for x in (-2.68, -2.01, -1.34, -0.67, 0, 0.67, 1.34, 2.01, 2.68)
    ])


def pathway():
    track = RoundedRectangle(width=6.40, height=1.28, corner_radius=0.52, stroke_color=CELL, stroke_width=3,
                             fill_color=BG, fill_opacity=0.90).move_to(point(0, PATH_Y))
    line = arrow(point(-2.84, PATH_Y), point(2.95, PATH_Y), CELL, 3)
    return VGroup(track, line, reaction_steps())


def equation():
    parts = VGroup(
        boxed_label("Glucose", GLUCOSE, size=28), label("+", 0, 0),
        boxed_label("Oxygen", OXYGEN, size=28), label("→", 0, 0),
        boxed_label("Carbon dioxide", CO2, size=28), label("+", 0, 0),
        boxed_label("Water", WATER, size=28), label("+", 0, 0),
        boxed_label("Energy", GLUCOSE, size=28),
    )
    return parts.arrange(RIGHT, buff=0.24).move_to(point(0, 3.34))


def travel(token, *points, run_time=1.25, remove=True):
    token.move_to(points[0])
    path = VMobject().set_points_as_corners(points)
    return Succession(
        FadeIn(token, run_time=0.15),
        MoveAlongPath(token, path, run_time=run_time, rate_func=linear),
        *([FadeOut(token, run_time=0.15)] if remove else []),
    )


def trace_steps(steps, color=GLUCOSE, run_time=2.0):
    marks = [Dot(step.get_center(), radius=step.width * 0.40, color=color) for step in steps]
    return LaggedStart(*[Succession(GrowFromCenter(mark), FadeOut(mark)) for mark in marks],
                       lag_ratio=0.37, run_time=run_time)


def organelle(at, color=MITO, width=5.30, height=2.22):
    outer = Ellipse(width=width, height=height, color=color, stroke_width=3.5,
                    fill_color=color, fill_opacity=0.33).move_to(at)
    xs = np.linspace(-0.32, 0.32, 7)
    folds = VGroup(*[
        ArcBetweenPoints(at + point(x * width, 0.24 * height), at + point(x * width + 0.09 * width, -0.23 * height),
                         angle=(-1) ** i * 1.65, color=color, stroke_width=4)
        for i, x in enumerate(xs)
    ])
    return VGroup(outer, folds)


MITO_AT, CHLORO_AT = point(2.98, 0.66), point(-3.06, 0.66)


def chloroplast():
    outline = Ellipse(width=4.67, height=2.20, color=WORK, stroke_width=3.5,
                      fill_color=WORK, fill_opacity=0.33).move_to(CHLORO_AT)
    stacks = VGroup(*[
        rounded_block(CHLORO_AT + point(x, y), WORK, 0.59, 0.15)
        for x in (-1.23, -0.42, 0.40, 1.22) for y in (-0.42, -0.21, 0, 0.21, 0.42)
    ])
    return VGroup(outline, stacks)


def cell_example(kind, at, scale=1.0):
    if kind == "Plant":
        shell = RoundedRectangle(width=1.83, height=1.18, corner_radius=0.23, color=CELL,
                                 fill_color=CELL, fill_opacity=0.34, stroke_width=3).move_to(at)
    else:
        shell = Ellipse(width=1.8, height=1.17, color=CELL, fill_color=CELL,
                        fill_opacity=0.34, stroke_width=3).move_to(at)
    items = VGroup(shell)
    if kind == "Yeast":
        items.add(Circle(radius=0.30, color=CELL, fill_color=CELL, fill_opacity=0.34,
                         stroke_width=3).move_to(at + point(0.70, 0.42)))
    items.add(organelle(at + point(-0.39, 0.10), width=0.66, height=0.36),
              organelle(at + point(0.34, -0.12), width=0.66, height=0.36))
    return items.scale(scale, about_point=at)


FORK = point(-1.06, 0.22)
WORK_AT, HEAT_AT = point(2.22, 1.13), point(2.55, -1.05)


def gear(at=WORK_AT):
    ring = Annulus(inner_radius=0.32, outer_radius=0.65, color=WORK, stroke_width=0,
                   fill_color=WORK, fill_opacity=0.87).move_to(at)
    teeth = VGroup(*[
        Rectangle(width=0.26, height=0.25, stroke_width=0, fill_color=WORK, fill_opacity=1)
        .move_to(at + 0.67 * rotate_vector(RIGHT, a)).rotate(a)
        for a in np.linspace(0, TAU, 8, endpoint=False)
    ])
    return VGroup(ring, teeth).scale(1.26, about_point=at)


HEAT_OFFSETS = ((-0.78, -0.34), (-0.62, 0.69), (0.23, -0.36), (0.69, 0.67),
                (1.18, -0.19), (1.22, 0.72), (1.62, -0.31))


def heat_particles(at=HEAT_AT, spread=False):
    initial = ((-0.86, -0.24), (-0.57, 0.36), (-0.11, -0.46), (0.02, 0.19),
               (0.44, -0.18), (0.64, 0.43), (0.88, -0.41))
    return VGroup(*[
        Dot(at + point(x, y) + (point(dx, dy) if spread else ORIGIN), radius=0.18, color=HEAT)
        for (x, y), (dx, dy) in zip(initial, HEAT_OFFSETS)
    ])


def thermal_motion(particles, duration=2.8):
    """Particles travel away from their initial cluster as thermal energy spreads."""
    return AnimationGroup(*[
        MoveAlongPath(dot, VMobject().set_points_as_corners([
            dot.get_center(), dot.get_center() + point(dx * 0.38, dy * -0.18),
            dot.get_center() + point(dx, dy),
        ]), rate_func=linear)
        for dot, (dx, dy) in zip(particles, HEAT_OFFSETS)
    ], run_time=duration, rate_func=rate_functions.ease_in_quad)


def thermal_stream():
    packet = VGroup(Dot(point(-0.48, -0.13), radius=0.30, color=HEAT),
                    Dot(point(0, 0.14), radius=0.39, color=HEAT),
                    Dot(point(0.54, -0.12), radius=0.31, color=HEAT))
    return travel(packet, FORK, HEAT_AT + point(-0.48, 0.06), point(5.03, -1.20), run_time=2.0)


def fork():
    source = rounded_block(point(-4.42, 0.22), width=1.55, height=0.80)
    stem = flow_arrow(point(-3.48, 0.22), FORK + LEFT * 0.25)
    joint = Dot(FORK, radius=0.24, color=GLUCOSE)
    upper = flow_arrow(FORK + point(0.25, 0.19), WORK_AT + LEFT * 1.09, WORK)
    lower = flow_arrow(FORK + point(0.25, -0.19), HEAT_AT + LEFT * 1.13, HEAT)
    return source, stem, joint, upper, lower


QUESTION = "Where will the released energy go?"
CARD_OPTIONS = dict(y=-3.10, size=34)


def choices():
    row = VGroup(boxed_label("Cell work", WORK, size=30),
                 boxed_label("Warmth", HEAT, size=30),
                 boxed_label("Both", TEXT, size=30, fill_opacity=0.29))
    return row.arrange(RIGHT, buff=0.42).move_to(point(0, -2.15))


def predict_world():
    source, stem, joint, upper, lower = fork()
    return VGroup(plant_cell(), source, stem, joint, upper, lower, gear(), heat_particles(), choices(),
                  scope_tag())


class S00Hook(SpokenScene, TitleCard):
    TITLE = "Why Do Sprouting Peas Get Warm?"
    LESSON = "Releasing Energy from Food"

    def construct(self):
        left_level, right_level = ValueTracker(ROOM), ValueTracker(ROOM)
        (left, left_head, peas), (right, right_head, boiled) = thermos_pair(left_level, right_level)
        self.add(left, right, scope_tag())
        self.at("sprouting peas warm", lead=0.30)
        self.play(FadeIn(left_head), run_time=0.62)
        self.at("while boiled peas", lead=0.32)
        self.play(FadeIn(right_head), run_time=0.60)
        self.at("Peas have no muscles")
        title = VGroup(label(self.TITLE, 0, -2.99, CELL, 33),
                       label(self.LESSON, 0, -3.49, TEXT, 28))
        self.play(FadeIn(title), run_time=0.38)
        self.wait(0.80)
        self.play(FadeOut(title), run_time=0.38)
        self.at("Both thermoses begin")
        room = room_marker()
        self.play(Create(room[0]), run_time=0.85)
        self.play(FadeIn(room[1]), run_time=0.45)
        self.at("Only one contains")
        self.play(*[p[0].animate.set_fill(opacity=1) for p in peas],
                  *[p[0].animate.set_fill(opacity=0.32) for p in boiled], run_time=0.80)
        ring = Circle(radius=0.40, color=CELL, stroke_width=4).move_to(peas[5])
        self.play(Create(ring), run_time=0.60)
        self.play(*[p[0].animate.set_fill(opacity=0.77) for p in (*peas, *boiled)], run_time=0.60)
        self.at("Watch the warmth rise")
        self.play(left_level.animate.set_value(WARM), run_time=3.8, rate_func=linear)
        self.finish()


class S01Stored(SpokenScene):
    def construct(self):
        flask, title, peas = thermos(LEFT_FLASK, ValueTracker(WARM))
        cell = plant_cell().stretch_to_fit_width(9.52).move_to(point(1.41, 0.03))
        self.add(flask, title, scope_tag())
        self.at("Inside the sprouting")
        flask.clear_updaters(recursive=True)
        mini = flask.copy().scale(0.40).move_to(point(-4.94, -0.52))
        seed = peas[5].copy().set_z_index(2)
        self.add(seed)
        self.play(FadeOut(title), Transform(flask, mini), seed.animate.move_to(point(0, 0.03)), run_time=0.84)
        self.play(ReplacementTransform(seed, cell), run_time=0.82)
        self.at("food molecules store", lead=0.05)
        store = VGroup(*[rounded_block(point(-1.56 + 0.45 * i, 0.78), width=0.35, height=0.42)
                         for i in range(5)])
        store_label = label("Food molecules", -0.66, 1.62, CELL)
        self.play(LaggedStart(*[GrowFromCenter(part) for part in store], lag_ratio=0.17), run_time=0.75)
        self.play(FadeIn(store_label), run_time=0.40)
        self.at("The fuel we will")
        blocks = VGroup(*[rounded_block(point(1.65 + 0.90 * i, PATH_Y), width=0.66, height=0.50)
                          for i in range(3)])
        self.play(LaggedStart(*[TransformFromCopy(store[i + 1], block) for i, block in enumerate(blocks)],
                              lag_ratio=0.25), FadeOut(store_label), run_time=1.40)
        name = label("Glucose", 2.60, 1.16, GLUCOSE, 34)
        self.play(FadeIn(name), run_time=0.52)
        self.at("Glucose is a sugar")
        new_blocks = blocks.copy().scale(1.38).move_to(point(2.60, PATH_Y))
        self.play(Transform(blocks, new_blocks), run_time=1.16)
        highlight = SurroundingRectangle(blocks, buff=0.12, color=GLUCOSE, stroke_width=3,
                                         corner_radius=0.10, fill_color=GLUCOSE, fill_opacity=0.20)
        self.play(FadeIn(highlight), run_time=0.58)
        self.bring_to_front(blocks)
        stored_name = label("Glucose stores energy", 2.80, 1.35, GLUCOSE)
        self.play(swap(name, stored_name, run_time=0.75))
        self.at("Plants make glucose")
        sunlight, foliage, sugar = sun(point(-2.68, -1.43)), leaf(point(-0.10, -1.43)), rounded_block(point(2.40, -1.43))
        a = arrow(point(-1.99, -1.43), point(-1.03, -1.43), YELLOW)
        b = arrow(point(0.80, -1.43), point(1.83, -1.43), GLUCOSE)
        self.play(FadeIn(sunlight), run_time=0.38)
        self.play(Create(a), GrowFromCenter(foliage), run_time=0.70)
        self.play(Create(b), GrowFromCenter(sugar), run_time=0.65)
        photo = label("Photosynthesis", -0.10, -2.23, WORK)
        self.play(FadeIn(photo), run_time=0.43)
        self.at("Cells must release")
        self.play(FadeOut(VGroup(flask, store, stored_name, highlight, sunlight, foliage, a, b, photo)),
                  run_time=0.64)
        carried_fuel = VGroup(*[rounded_block(point(-5.41 + 0.73 * i, PATH_Y)) for i in range(3)])
        self.play(sugar.animate.move_to(carried_fuel[1]), Transform(cell, plant_cell()),
                  Transform(blocks, carried_fuel), run_time=1.65)
        self.remove(sugar)
        self.finish()


class S02Pathway(SpokenScene):
    def construct(self):
        rail = pathway()
        fuel = VGroup(*[rounded_block(point(-5.41 + 0.73 * i, PATH_Y)) for i in range(3)])
        self.add(plant_cell(), fuel, scope_tag())
        self.at("Cellular respiration")
        self.play(GrowFromCenter(rail[0]), run_time=0.83)
        self.play(Create(rail[1]), LaggedStart(*[GrowFromCenter(p) for p in rail[2]], lag_ratio=0.13), run_time=1.45)
        name = label("Cellular respiration", 0, 1.66, CELL, 38)
        self.play(FadeIn(name), run_time=0.63)
        eq = equation()
        self.at("Glucose and oxygen")
        self.play(FadeIn(eq[0]), run_time=0.42)
        self.at("oxygen enter the", lead=0.13)
        self.play(FadeIn(VGroup(eq[1], eq[2])), run_time=0.48)
        self.play(fuel.animate.shift(RIGHT * 1.94), travel(gas(point(-5.14, -0.63)),
                   point(-5.14, -0.63), point(-3.14, -0.63), point(-2.64, PATH_Y), run_time=1.04),
                  run_time=1.30)
        self.play(FadeOut(fuel), trace_steps(rail[2], run_time=1.12), run_time=1.12)
        self.at("Carbon dioxide and", lead=0.13)
        carbon = rounded_block(point(2.64, PATH_Y), CO2, 0.72, 0.50)
        water = drop(point(2.64, PATH_Y)).scale(1.30)
        carbon_out = AnimationGroup(travel(carbon, point(2.64, PATH_Y), point(3.69, 0.95),
                                           point(5.30, 0.95), run_time=1.22, remove=False),
                                    FadeIn(VGroup(eq[3], eq[4])), lag_ratio=0.20)
        water_out = AnimationGroup(travel(water, point(2.64, PATH_Y), point(3.70, -0.18),
                                         point(5.30, -0.18), run_time=1.19, remove=False),
                                   FadeIn(VGroup(eq[5], eq[6])), lag_ratio=0.21)
        self.play(AnimationGroup(carbon_out, water_out, lag_ratio=0.40), run_time=2.04)
        self.at("with released energy", lead=0.0)
        energy = Dot(point(2.64, PATH_Y), radius=0.33, color=GLUCOSE)
        self.play(FadeIn(VGroup(eq[7], eq[8])), travel(energy, point(2.64, PATH_Y),
                   point(3.68, -1.36), point(5.35, -1.36), run_time=1.10, remove=False), run_time=1.43)
        self.at("Oxygen is a gas")
        self.play(LaggedStart(*[
            travel(gas(point(-5.26, PATH_Y)), point(-5.26, PATH_Y + dy),
                   point(-3.02, PATH_Y + dy * 0.6), point(-1.72, PATH_Y), run_time=1.80)
            for dy in (-0.68, 0, 0.68)
        ], lag_ratio=0.31), run_time=2.68)
        self.at("Carbon dioxide is a gas")
        carbon_stream = VGroup(*[rounded_block(point(-0.43 + 0.51 * i, 0.21 - 0.25 * i),
                                               CO2, 0.54, 0.41) for i in range(3)])
        self.play(travel(carbon_stream, point(2.42, PATH_Y), point(3.62, 1.36),
                         point(5.07, 1.57), run_time=2.01))
        self.play(FadeOut(VGroup(carbon, water, energy, eq, name)), run_time=0.52)
        self.finish()


class S03Where(SpokenScene):
    def construct(self):
        cell, rail = plant_cell(), pathway()
        self.add(cell, rail, scope_tag())
        self.at("Respiration happens in")
        stones = reaction_steps(0.66)
        stones.shift(LEFT * 1.88)
        stones.scale(1.20, about_point=stones.get_right())
        self.play(FadeOut(VGroup(rail[0], rail[1])), Transform(rail[2], stones), run_time=1.10)
        self.play(LaggedStart(*[step.animate.set_fill(GLUCOSE, opacity=0.96) for step in rail[2]],
                              lag_ratio=0.42), run_time=3.28)
        self.at("The first steps")
        first = rail[2][:4]
        last = rail[2][4:]
        self.play(last.animate.set_fill(BG, opacity=0.96), run_time=0.73)
        cyto = label("Cytoplasm", -3.55, 1.60, CELL, 34)
        self.play(FadeIn(cyto), run_time=0.50)
        self.play(trace_steps(first, CELL, run_time=1.50))
        self.at("Most of the work")
        mito = organelle(MITO_AT)
        self.play(GrowFromCenter(mito), last.animate.move_to(MITO_AT), run_time=1.40)
        self.play(LaggedStart(*[step.animate.set_fill(GLUCOSE, opacity=0.96) for step in last],
                              lag_ratio=0.50), run_time=1.63)
        mito_name = label("Mitochondrion", 2.98, 2.22, MITO, 34)
        self.play(FadeIn(mito_name), run_time=0.48)
        self.at("Plant and animal")
        self.play(FadeOut(cell), FadeOut(VGroup(first, last, cyto)), run_time=0.42)
        examples = VGroup()
        for kind, x in (("Plant", -3.7), ("Animal", -0.25)):
            icon = cell_example(kind, point(x, -1.36))
            name = label(f"{kind} cell", x, -2.30, CELL)
            self.play(FadeIn(icon, shift=UP * 0.37), run_time=0.74)
            self.play(FadeIn(name), run_time=0.36)
            examples.add(icon, name)
        self.at("Fungus cells usually")
        yeast = cell_example("Yeast", point(3.42, -1.36))
        self.play(FadeIn(yeast, shift=UP * 0.37), run_time=0.81)
        self.play(FadeIn(label("Yeast cell", 3.42, -2.30, CELL)), run_time=0.47)
        self.finish()


class S03bPlantParts(SpokenScene):
    def construct(self):
        mito, chloro = organelle(MITO_AT), chloroplast()
        self.add(plant_cell(), mito, scope_tag())
        self.at("Do not confuse")
        self.play(GrowFromCenter(chloro), run_time=1.35)
        chloro_name = label("Chloroplast", -3.06, 2.22, WORK, 34)
        mito_name = label("Mitochondrion", 2.98, 2.22, MITO, 34)
        self.play(FadeIn(mito_name), run_time=0.43)
        self.play(FadeIn(chloro_name), run_time=0.50)
        self.at("Chloroplasts let a plant")
        sugar = rounded_block(point(-0.15, PATH_Y), width=1.02, height=0.66)
        self.play(chloro[0].animate.set_fill(WORK, opacity=0.58), run_time=0.68)
        self.play(travel(sugar, point(-2.16, PATH_Y), point(-0.15, PATH_Y), run_time=1.70, remove=False))
        self.play(FadeIn(label("Make food", -3.06, -1.10, WORK, 34)), run_time=0.64)
        self.at("Mitochondria let plant")
        self.play(MoveAlongPath(sugar, Line(point(-0.15, PATH_Y), point(2.65, PATH_Y)),
                               rate_func=linear), chloro[0].animate.set_fill(WORK, opacity=0.33), run_time=1.68)
        energy = Dot(point(2.65, PATH_Y), radius=0.39, color=GLUCOSE)
        self.play(ReplacementTransform(sugar, energy), mito[0].animate.set_fill(MITO, opacity=0.58), run_time=0.83)
        self.play(FadeIn(label("Release stored energy", 2.98, -1.10, MITO, 34)), run_time=0.62)
        self.at("A plant cell can")
        bracket = VMobject(color=CELL, stroke_width=4).set_points_as_corners([
            point(-4.78, -1.52), point(-4.78, -1.92), point(4.78, -1.92), point(4.78, -1.52),
        ])
        self.play(Create(bracket), run_time=1.43)
        self.play(FadeIn(label("One plant cell", 0, -2.37, CELL)), run_time=0.53)
        self.finish()


class S04Predict(SpokenScene):
    def construct(self):
        source, stem, joint, upper, lower = fork()
        work, heat, options = gear(), heat_particles(), choices()
        self.add(plant_cell(), source, scope_tag())
        self.at("The pathway has released")
        self.play(DrawBorderThenFill(stem), travel(Dot(radius=0.38, color=GLUCOSE),
                  point(-3.51, 0.22), FORK, run_time=1.65), FadeIn(joint), run_time=2.0)
        self.at("Where will that energy")
        q = question_card(QUESTION, **CARD_OPTIONS)
        self.play(DrawBorderThenFill(upper), DrawBorderThenFill(lower), run_time=1.21)
        self.play(FadeIn(q.question), run_time=0.63)
        self.at("Will it power cell", lead=0.32)
        self.play(GrowFromCenter(work), run_time=0.68)
        self.play(FadeIn(options[0]), run_time=0.40)
        self.at("leave as warmth", lead=0.14)
        self.play(FadeIn(heat), run_time=0.52)
        self.play(FadeIn(options[1]), run_time=0.38)
        self.at("or do both", lead=0.04)
        self.play(FadeIn(options[2]), run_time=0.56)
        self.at("Make your prediction")
        self.play(q.question.animate.set_color(TEXT), run_time=0.63)
        self.finish()


class S05Pause(PredictPause):
    QUESTION = QUESTION
    CARD = {**CARD_OPTIONS, "color": TEXT}
    SECONDS = 4.5
    RING_AT = (-4.61, -1.43, 0)

    def backdrop(self):
        return predict_world()

    def construct(self):
        self.add(self.backdrop(), question_card(self.QUESTION, **self.CARD))
        ring, drain = countdown(self.SECONDS, center=self.RING_AT, radius=0.65)
        remaining = drain.mobject
        sector = always_redraw(lambda: Sector(
            radius=0.52, angle=TAU * max(0.001, remaining.get_value()), start_angle=PI / 2,
            fill_color=GLUCOSE, fill_opacity=0.77, stroke_width=0,
        ).shift(self.RING_AT))
        self.add(sector, ring)
        self.play(drain)


def assembled_part():
    return VGroup(*[rounded_block(point(x, y), WORK, 0.42, 0.37)
                    for x, y in ((4.02, 0.84), (4.50, 0.84), (4.98, 0.84),
                                 (4.25, 1.28), (4.73, 1.28), (4.50, 1.72))])


class S06Reveal(SpokenScene):
    def construct(self):
        cell, source, stem, joint, upper, lower, work, hot, options, tag = predict_world()
        q = question_card(QUESTION, color=TEXT, **CARD_OPTIONS)
        self.add(cell, source, stem, joint, upper, lower, work, hot, options, tag, q)
        self.at("It does both")
        self.play(FadeOut(VGroup(q, options)), run_time=0.52)
        self.play(ShowPassingFlash(upper.copy().set_stroke(width=12)),
                  ShowPassingFlash(lower.copy().set_stroke(width=12)), run_time=1.30)
        self.at("One branch powers")
        work_name = label("Cell work", 2.22, 2.50, WORK, 34)
        self.play(travel(Dot(radius=0.34, color=WORK), FORK, WORK_AT, run_time=1.20),
                  Rotate(work, -PI / 2, about_point=WORK_AT), run_time=1.37)
        self.play(FadeIn(work_name), run_time=0.50)
        self.at("building new cell parts", lead=0.24)
        part = assembled_part()
        start = part.copy().arrange(RIGHT, buff=0.12).move_to(point(4.12, -0.02))
        self.play(FadeIn(start, shift=RIGHT * 0.35), run_time=0.60)
        self.play(Transform(start, part), Rotate(work, -PI / 2, about_point=WORK_AT), run_time=1.45)
        self.at("Another becomes thermal")
        self.play(travel(Dot(radius=0.35, color=HEAT), FORK, HEAT_AT + LEFT * 0.82, run_time=1.44))
        heat_name = label("Thermal energy", 2.86, -2.40, HEAT, 34)
        self.play(FadeIn(heat_name), run_time=0.45)
        self.at("the motion of particles")
        self.play(thermal_motion(hot, 2.72))
        self.at("Some released energy")
        self.play(travel(Dot(radius=0.35, color=GLUCOSE), point(-3.48, 0.22), FORK, run_time=1.02))
        self.play(thermal_stream(), run_time=2.28)
        self.finish()


def compact_pathway(at, scale=0.74):
    """The same respiration track used for the comparison and the rate preview."""
    shell = plant_cell().scale(0.60).move_to(ORIGIN)
    rail = pathway()
    mini = VGroup(shell, rail).scale(scale).move_to(at)
    return mini, rail[2]


class S07Energy(SpokenScene):
    def construct(self):
        source, stem, joint, upper, lower = fork()
        cell, work, hot = plant_cell(), gear(), heat_particles(spread=True)
        part = assembled_part()
        self.add(cell, source, stem, joint, upper, lower, work, hot, part, scope_tag())
        self.at("The cell did not")
        new_energy = boxed_label("New energy", TEXT, size=34, fill_opacity=0.22).move_to(point(-3.40, -1.44))
        cross = Cross(Square(side_length=0.47), stroke_color=RED, stroke_width=8)
        cross.next_to(new_energy, LEFT, buff=0.25)
        self.play(FadeIn(new_energy), run_time=0.63)
        self.play(Create(cross), run_time=0.81)
        self.at("It changed energy")
        self.play(FadeOut(VGroup(new_energy, cross)), run_time=0.30)
        gl = label("Energy stored in glucose", 0, 3.34, GLUCOSE, 32)
        self.play(FadeIn(gl), travel(Dot(radius=0.38, color=GLUCOSE),
                  point(-3.48, 0.22), FORK, run_time=1.0), run_time=1.30)
        self.play(travel(Dot(radius=0.31, color=WORK), FORK, WORK_AT, run_time=1.21),
                  travel(Dot(radius=0.31, color=HEAT), FORK, HEAT_AT, run_time=1.21),
                  Rotate(work, -PI / 2, about_point=WORK_AT), run_time=1.51)
        self.at("The thermos slows")
        level = ValueTracker(ROOM)
        flask, head, peas = thermos(LEFT_FLASK, level)
        enlarged_pea = peas[5].set_z_index(1)
        peas.remove(enlarged_pea)
        self.play(FadeOut(VGroup(gl, source, stem, joint, upper, lower, work, hot, part)), run_time=0.38)
        self.play(FadeIn(flask), ReplacementTransform(cell, enlarged_pea), run_time=1.10)
        self.play(FadeIn(head), run_time=0.44)
        self.bring_to_front(enlarged_pea)
        wall_note = label("Insulated wall", 3.31, 1.19, TEXT, 36)
        wall_arrow = arrow(point(1.26, 1.19), point(-0.67, 1.19))
        self.play(FadeIn(wall_note), Create(wall_arrow), run_time=0.70)
        particles = [
            (point(-4.67, -0.81), point(-5.62, 0.42), point(-4.89, 1.17), point(-5.40, 1.77)),
            (point(-4.34, -0.71), point(-3.82, 0.25), point(-3.12, 1.89), point(-2.72, 1.23)),
            (point(-4.72, -0.88), point(-5.63, -0.46), point(-5.04, 0.40), point(-4.53, 0.82)),
        ]
        self.play(LaggedStart(*[travel(Dot(radius=0.22, color=HEAT), *p, run_time=1.76)
                               for p in particles], lag_ratio=0.25), run_time=2.16)
        self.at("living pea cells keep", lead=0.09)
        self.play(level.animate.set_value(WARM), run_time=3.35, rate_func=linear)
        self.finish()


def lungs():
    color = "#E59092"
    left = Ellipse(width=1.42, height=2.14, color=color, fill_color=color,
                   fill_opacity=0.82, stroke_width=3.5).rotate(-0.18).move_to(point(-4.05, -0.03))
    right = left.copy().flip().move_to(point(-2.55, -0.03))
    trachea = VMobject(color=CELL, stroke_width=8).set_points_as_corners([
        point(-3.30, 1.52), point(-3.30, 0.76), point(-3.95, 0.26),
    ])
    branch = Line(point(-3.30, 0.76), point(-2.65, 0.26), stroke_width=8, color=CELL)
    torso = RoundedRectangle(width=4.45, height=3.49, corner_radius=0.75, color=CELL,
                             stroke_width=3, fill_color=CELL, fill_opacity=0.23).move_to(point(-3.30, -0.01))
    return torso, VGroup(left, right), VGroup(trachea, branch)


class S08Breathing(SpokenScene):
    def construct(self):
        panels = TwoPanel("Breathing in lungs", "Respiration in cells", colors=(TEXT, CELL),
                          top=2.95, bottom=-2.72, size=32)
        torso, air_sacs, airway = lungs()
        cell, steps = compact_pathway(point(3.30, 0.18))
        self.add(panels[0], panels[2], cell, scope_tag())
        self.at("Breathing is different")
        self.play(FadeIn(torso), GrowFromCenter(air_sacs), Create(airway), FadeIn(panels[1]), run_time=1.29)
        self.at("cellular respiration", lead=0.03)
        self.play(FadeIn(panels[3]), run_time=0.59)
        self.at("Breathing moves air")
        self.play(air_sacs.animate.scale(1.37, about_point=point(-3.3, 0.0)), run_time=1.42)
        self.play(air_sacs.animate.scale(1 / 1.37, about_point=point(-3.3, 0.0)), run_time=1.30)
        self.at("It brings oxygen")
        in_note = label("Oxygen in", -3.30, -2.20, OXYGEN, 30)
        self.play(FadeIn(in_note), travel(gas(point(-3.3, 1.55)), point(-3.3, 1.55),
                  point(-3.3, 0.77), point(-3.9, 0.21), run_time=1.28),
                  air_sacs.animate.scale(1.34, about_point=point(-3.3, 0.0)), run_time=1.55)
        self.at("carries carbon dioxide")
        out_note = label("Carbon dioxide out", -3.30, -2.20, CO2, 30)
        self.play(swap(in_note, out_note), travel(rounded_block(point(-2.65, 0.20), CO2, 0.73, 0.52),
                  point(-2.65, 0.20), point(-3.30, 0.78), point(-3.30, 1.55), run_time=1.50),
                  air_sacs.animate.scale(1 / 1.34, about_point=point(-3.3, 0.0)), run_time=1.80)
        self.at("Respiration happens inside")
        self.play(FadeOut(out_note, run_time=0.40),
                  LaggedStart(*[step.animate.set_fill(GLUCOSE, opacity=0.97) for step in steps],
                              lag_ratio=0.37, run_time=1.82))
        self.at("including cells in organisms")
        self.play(cell.animate.shift(UP * 0.76), run_time=0.59)
        seed = pea(point(2.24, -1.30), radius=0.36)
        yeast = cell_example("Yeast", point(4.41, -1.30), 0.58)
        self.play(FadeIn(seed, shift=UP * 0.28), FadeIn(yeast, shift=UP * 0.28), run_time=0.79)
        self.play(FadeIn(label("No lungs", 3.30, -0.66, TEXT, 28)), run_time=0.38)
        self.play(FadeIn(label("Seed and yeast", 3.30, -2.23, CELL)), run_time=0.55)
        self.finish()


def mini_steps(at, color=GLUCOSE):
    return VGroup(*[Dot(at + point(x, y), color=color, radius=0.064)
                    for x, y in ((-0.17, -0.07), (0, 0.07), (0.17, -0.02))])


class S09Control(SpokenScene):
    def construct(self):
        left_level, right_level = ValueTracker(WARM), ValueTracker(ROOM)
        (left, left_head, living), (right, right_head, dead) = thermos_pair(left_level, right_level)
        self.add(left, right, scope_tag())
        self.at("Now compare the")
        self.play(FadeIn(left_head), FadeIn(right_head), run_time=0.85)
        left_note = label("Living cells", LEFT_FLASK, -3.13, CELL, 32)
        right_note = label("Cells killed by boiling", 2.91, -3.03, TEXT, 30)
        self.at("Sprouting peas contain")
        active = VGroup(*[mini_steps(p.get_center()) for p in living])
        self.play(LaggedStart(*[AnimationGroup(FadeIn(dots), p[0].animate.set_fill(GLUCOSE, opacity=0.67))
                                for p, dots in zip(living, active)], lag_ratio=0.23), run_time=1.78)
        self.play(FadeIn(left_note), run_time=0.48)
        self.at("keep releasing thermal energy")
        rises = VGroup(*[Dot(p.get_center(), radius=0.19, color=HEAT) for p in living[5:]])
        self.play(LaggedStart(*[
            travel(dot, dot.get_center(), point(LEFT_FLASK - 1.45 + 0.56 * i, 0.8 + 0.20 * (i % 2)),
                   run_time=2.00, remove=False)
            for i, dot in enumerate(rises)
        ], lag_ratio=0.16), left_level.animate.set_value(1.57), run_time=3.00)
        self.at("Boiling killed the cells")
        idle = VGroup(*[mini_steps(p.get_center(), BG) for p in dead])
        barred = VGroup(*[Line(p.get_center() + point(-0.18, -0.18), p.get_center() + point(0.18, 0.18),
                               color=RED, stroke_width=3.5) for p in dead])
        self.play(FadeIn(idle), LaggedStart(*[
            AnimationGroup(Create(bar), p[0].animate.set_fill(GREY, opacity=0.32))
            for p, bar in zip(dead, barred)
        ], lag_ratio=0.20), run_time=1.57)
        self.play(FadeIn(right_note), run_time=0.50)
        self.at("After those peas cool")
        room = room_marker()
        self.play(FadeOut(VGroup(right_note, left_note)), run_time=0.40)
        self.play(Create(room[0][0]), FadeIn(room[1]), run_time=1.08)
        self.at("thermometer stays near", lead=0.48)
        reference = flow_arrow(point(RIGHT_FLASK - 1.31, ROOM), point(RIGHT_FLASK + 0.93, ROOM), TEXT)
        self.play(DrawBorderThenFill(reference), run_time=1.65)
        self.finish()


class S10Rule(SpokenScene):
    def construct(self):
        (left, left_head, _), (right, right_head, _) = thermos_pair(ValueTracker(1.57), ValueTracker(ROOM))
        cell = plant_cell()
        source, stem, joint, upper, lower = fork()
        work, hot = gear(), heat_particles()
        self.add(left, right, left_head, right_head, scope_tag())
        left.clear_updaters(recursive=True)
        right.clear_updaters(recursive=True)
        self.at("Respiration releases stored")
        self.play(FadeOut(VGroup(left_head, right_head)), run_time=0.31)
        self.play(ReplacementTransform(left, cell), FadeOut(right), run_time=1.00)
        self.play(FadeIn(VGroup(source, stem, joint)), run_time=0.63)
        self.at("for cell work", lead=0.30)
        self.play(DrawBorderThenFill(upper), GrowFromCenter(work), run_time=0.85)
        self.at("as thermal energy", lead=0.35)
        self.play(DrawBorderThenFill(lower), FadeIn(hot), run_time=0.71)
        rule = VGroup(label("Respiration releases stored food energy", 0, 3.51, size=28),
                      label("for cell work and as thermal energy.", 0, 3.08, size=28))
        self.play(Write(rule), run_time=1.28)
        self.at("explains the warmth", lead=0.37)
        self.play(thermal_motion(hot, 2.75), thermal_stream(), run_time=2.75)
        self.at("Next temperature", lead=0.16)
        rail = pathway()
        self.play(ReplacementTransform(VGroup(source, stem, joint), rail),
                  FadeOut(VGroup(upper, lower, work, hot)), run_time=0.81)
        temp = VGroup(Line(point(-4.04, -0.91), point(-4.04, -1.53), stroke_width=9, color=HEAT),
                     Dot(point(-4.04, -1.57), radius=0.17, color=HEAT))
        valve = VGroup(Line(point(-0.53, -1.29), point(0.53, -1.29), stroke_width=7, color=OXYGEN),
                       Circle(radius=0.23, color=OXYGEN, stroke_width=5).move_to(point(0, -1.29)),
                       Line(point(0, -1.07), point(0, -0.93), color=OXYGEN, stroke_width=4))
        supply = VGroup(*[rounded_block(point(3.66 + i * 0.43, -1.29), width=0.33) for i in range(3)])
        self.play(FadeIn(temp), run_time=0.40)
        self.play(FadeIn(valve), run_time=0.42)
        self.play(FadeIn(supply), run_time=0.41)
        controls = VGroup(label("Temperature", -4.04, -2.14, HEAT),
                          label("Oxygen", 0, -2.14, OXYGEN), label("Sugar", 4.09, -2.14, GLUCOSE))
        self.play(LaggedStart(*[FadeIn(control) for control in controls], lag_ratio=0.52), run_time=1.35)
        self.play(trace_steps(rail[2], run_time=1.58))
        self.finish()


class S11End(EndCard):
    LINE = RULE
