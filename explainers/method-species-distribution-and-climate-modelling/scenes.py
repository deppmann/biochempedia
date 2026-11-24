"""Mapping Climates and Moving Ranges.

RED: warmth. BLUE: rain and equal-temperature contours. GREEN: forest and
species. GOLD: dryness, limits and lag. TEAL: model projections.
GREY: terrain, axes and observations.
"""

from bp_parts import *
from bp_style import EndCard

LESSON_TITLE = "Species Distribution and Climate Modelling"
QUESTION = "How far uphill each decade?"
CARD = {"size": 36, "y": -2.97}
WARMING = 0.3
COOLING_PER_100_M = 0.6
ISOTHERM_SHIFT = 100 * WARMING / COOLING_PER_100_M
MEDIAN_SHIFT = 11.0
UNDERSTORY_OFFSET = -4.1
# Illustrative monthly inputs, explicitly labelled schematic in both scenes.
TEMPERATURE = np.array([12, 13, 16, 19, 23, 27, 29, 28, 24, 20, 16, 13])
RAIN = np.array([70, 62, 54, 46, 33, 23, 15, 18, 34, 54, 68, 76])
RIDGE = np.array([[-6.25, -1.12], [-5.55, -1.0], [-4.9, -0.9],
                  [-4.25, -1.00], [-3.5, -0.58], [-2.8, 0.18],
                  [-1.92, 1.18], [-1.28, 2.02], [-0.96, 1.91], [-0.42, 1.36]])


def p(x, y):
    return np.array([x, y, 0.0])


def poly(points, color, opacity=1.0, stroke=0):
    return Polygon(*(p(x, y) for x, y in points), fill_color=color,
                   fill_opacity=opacity, stroke_color=color, stroke_width=stroke)


def line(points, color, width=4):
    curve = VMobject(stroke_color=color, stroke_width=width)
    curve.set_points_as_corners([p(x, y) for x, y in points])
    return curve


def label(text, x, y, color=TEXT, size=32, width=5.55):
    return fit_text(text, max_w=width, color=color, size=size,
                    min_size=28, max_lines=2).move_to(p(x, y))


def right(text, y=2.72, color=TEXT, size=35):
    return label(text, 3.30, y, color, size)


def terrain_label(text, x, y, color, size=32):
    plate = boxed_label(text, color, size=size, pad=0.16, stroke=0, fill_opacity=0.94)
    plate.box.set_fill(BG)
    return plate.move_to(p(x, y))


def note(text, color=TEXT):
    return caption(text, size=31, color=color, y=-3.00).move_to(p(0, -3.00))


def frames():
    panels = TwoPanel("", "", colors=("#3A5360", "#3A5360"), top=3.19, bottom=-2.42)
    return VGroup(panels.left_frame, panels.right_frame)


def surface(x):
    return np.interp(x, RIDGE[:, 0], RIDGE[:, 1])


def tree(x, y, size, shade):
    stem = Line(p(x, y - 0.04), p(x, y + size * 0.62), color="#6C5949", stroke_width=4)
    crown = poly([(x - size * 0.34, y + size * 0.15),
                  (x - size * 0.46, y + size * 0.49),
                  (x - size * 0.30, y + size * 0.79),
                  (x, y + size), (x + size * 0.33, y + size * 0.78),
                  (x + size * 0.48, y + size * 0.48),
                  (x + size * 0.28, y + size * 0.19)], shade)
    return VGroup(stem, crown)


def cloud(x, y, width, height, color):
    coords = [(-0.53, -0.23), (-0.49, 0.03), (-0.36, 0.16),
              (-0.24, 0.13), (-0.14, 0.43), (0.02, 0.51),
              (0.18, 0.43), (0.28, 0.18), (0.41, 0.17),
              (0.53, -0.02), (0.49, -0.23), (0.30, -0.30), (-0.33, -0.30)]
    return poly([(x + a * width, y + b * height) for a, b in coords], color)


def landscape(moving=True):
    """Single cross-section used at the same coordinates throughout the film."""
    sky = poly([(-6.25, -2.29), (-0.42, -2.29), (-0.42, 3.04), (-6.25, 3.04)], "#1A303D")
    clouds = VGroup(
        cloud(-4.76, 2.06, 1.76, 0.73, "#6A8792"),
        cloud(-3.25, 1.20, 1.42, 0.64, "#577D8C"),
        cloud(-5.10, 0.43, 1.16, 0.48, "#537987"),
        cloud(-2.27, 2.56, 1.00, 0.34, "#577887"),
    )
    if moving:
        for i, item in enumerate(clouds):
            anchor = item.get_center().copy()
            item.clock = i * 0.35
            def drift(mob, dt, origin=anchor):
                mob.clock += dt
                mob.move_to(origin + RIGHT * 0.63 * np.sin(mob.clock * 0.98) + UP * 0.10 * np.sin(mob.clock * 1.26))
            item.add_updater(drift)
    rear = poly([(-6.25, -2.29), (-6.25, -0.06), (-5.62, 0.20),
                 (-4.99, -0.39), (-4.35, 0.10), (-3.64, 1.03),
                 (-3.02, 0.58), (-2.32, 0.69), (-1.58, 1.42),
                 (-0.92, 2.40), (-0.42, 2.05), (-0.42, -2.29)], "#314F59")
    ground = poly([(-6.25, -2.29), *map(tuple, RIDGE), (-0.42, -2.29)], "#766348")
    face = poly([(-6.25, -2.29), (-6.25, -1.75), (-4.52, -1.68), (-3.47, -1.97),
                 (-2.34, -1.34), (-1.28, 2.02), (-0.96, 1.91), (-0.42, 1.36),
                 (-0.42, -2.29)], "#514C49")
    sand = poly([(-4.32, -2.29), (-4.68, -1.78), (-4.25, -1.0), (-3.5, -0.58),
                 (-2.8, 0.18), (-2.86, -0.86), (-3.47, -1.97), (-3.37, -2.29)], "#A3774C")
    forest_floor = poly([(-6.25, -2.29), (-6.25, -1.12), (-5.55, -1.0),
                         (-4.9, -0.9), (-4.25, -1.0), (-4.48, -1.62),
                         (-4.20, -2.29)], "#315C4D")
    grove = VGroup(*[tree(x, y, h, col) for x, y, h, col in [
        (-5.68, -1.17, 1.12, "#48826A"), (-5.31, -1.08, 1.28, "#56916F"),
        (-4.70, -1.02, 0.90, "#46775B"), (-5.68, -1.79, 1.05, "#6C9C64"),
        (-4.98, -1.70, 0.84, "#5D8C5C"), (-6.02, -1.98, 0.52, "#487B57"),
        (-5.34, -2.09, 0.49, "#487B57"),
    ]])
    strata = VGroup(
        line([(-4.12, -1.49), (-3.62, -1.42), (-3.13, -1.20)], "#CE9A66", 2),
        line([(-4.05, -1.78), (-3.57, -1.73), (-3.19, -1.53)], "#C39261", 2),
        line([(-2.30, -0.68), (-1.72, -0.38), (-1.10, 0.83), (-0.65, 1.13)], "#81786A", 2),
        line([(-2.01, -1.40), (-1.45, -0.91), (-0.81, 0.24), (-0.48, 0.46)], "#81786A", 2),
    )
    world = VGroup(sky, rear, clouds, ground, face, sand, forest_floor, strata, grove)
    world.grove = grove
    return world


def outline(x, y, rx, ry, color, width=5, fill=0):
    return Ellipse(width=2 * rx, height=2 * ry, stroke_color=color,
                   stroke_width=width, fill_color=color, fill_opacity=fill).move_to(p(x, y))


def mountain_point(metres):
    # The slope rises linearly across this part of the shared drawing.
    y = 0.01 + metres * 0.020
    x = np.interp(y, RIDGE[4:8, 1], RIDGE[4:8, 0])
    return x, y


def elevation_band(metres, color, width=6):
    x, y = mountain_point(metres)
    return line([(x - 0.33, y + 0.055),
                 (x + 0.08, y),
                 (x + 0.42, y - 0.11),
                 (x + 0.60, y - 0.23)], color, width)


def month_plot():
    return Plot(box=(1.45, 5.96, -1.74, 2.00), xr=(1, 12), yr=(0, 90),
                xticks=[(1, "Jan"), (6, "Jun"), (12, "Dec")],
                size=28, color="#A9B5C3")


def monthly_bars(plot):
    return VGroup(*[
        line([(plot.pt(month, 0)[0], plot.y0 + 0.07),
              (plot.pt(month, 0)[0], plot.pt(month, rain)[1])], BLUE, 9)
        for month, rain in enumerate(RAIN, 1)
    ])


def monthly_trace(plot, values, color):
    return plot.curve(lambda x: np.interp(x, np.arange(1, 13), values), color=color, n=133)


def niche_plot():
    plot = Plot(box=(1.14, 5.91, -1.63, 2.06), xr=(0, 1), yr=(0, 1),
                xlabel="Temperature", ylabel="Rainfall", label_size=29)
    plot.ylabel.shift(LEFT * 0.12 + DOWN * 0.12)
    return plot


NICHE_POINTS = [(0.42, 0.50), (0.48, 0.65), (0.59, 0.61), (0.63, 0.45), (0.55, 0.50)]
MAP_POINTS = [(-5.77, -1.21), (-5.37, -0.99), (-4.98, -1.30), (-4.53, -1.17), (-4.90, -1.63)]


def occupied_map():
    return outline(-5.13, -1.31, 0.91, 0.60, GREEN, fill=0.16)


def occupied_niche(plot):
    return outline(*plot.pt(0.53, 0.54)[:2], 0.89, 0.68, GREEN, fill=0.22)


def ratio_material():
    formula = VGroup(right("Isotherm climb", 2.40, BLUE, 37),
                     right("warming ÷ cooling per 100 m", 1.77, TEXT, 32))
    warming = boxed_label(f"{WARMING:g} °C / decade", RED, size=36).move_to(p(3.30, 0.72))
    cooling = boxed_label(f"{COOLING_PER_100_M:g} °C / 100 m", BLUE, size=36).move_to(p(3.30, -0.62))
    return formula, warming, cooling


def isotherm_label():
    return terrain_label("Isotherm", -2.93, 1.79, BLUE)


def predict_world(moving=True):
    world = VGroup(frames(), landscape(moving))
    world.contour = elevation_band(0, BLUE, 8)
    world.contour_label = isotherm_label()
    world.inputs = ratio_material()
    world.add(world.contour, world.contour_label, *world.inputs, scope_tag("schematic", size=28, color=TEXT))
    return world


class S01Hook(SpokenScene):
    def construct(self):
        world = landscape()
        self.add(frames(), world, scope_tag("schematic", size=28, color=TEXT))
        wet = boxed_label("Rainforest", GREEN, size=32, fill_opacity=0.15).move_to(p(-5.03, 0.86))
        dry = label("Desert", -3.51, -0.85, TEXT, 31)
        self.at("grow rainforest")
        self.play(FadeIn(wet), run_time=0.42)
        self.at("another desert")
        self.play(FadeIn(dry), run_time=0.52)
        self.at("where will warming")
        band = elevation_band(0, BLUE, 8)
        self.play(Create(band), run_time=0.66)
        self.play(Transform(band, elevation_band(35, BLUE, 8)), run_time=1.46)
        self.at("climate models turn")
        warm, rain = ValueTracker(0.20), ValueTracker(0.32)
        wd = dial(warm, p(1.98, 0.24), radius=1, color=RED, fmt="", size=28)
        rd = dial(rain, p(4.57, 0.24), radius=1, color=BLUE, fmt="", size=28)
        gauges = VGroup(wd, rd, label("Warmth", 1.98, -0.34, RED),
                        label("Rainfall", 4.57, -0.34, BLUE),
                        right("30-year averages", 2.72))
        self.play(FadeIn(gauges), run_time=0.34)
        self.at("averages of warmth")
        self.play(warm.animate.set_value(0.69), rain.animate.set_value(0.53), run_time=1.40)
        self.at("into a testable")
        plot = month_plot()
        bars = monthly_bars(plot)
        self.play(FadeOut(gauges), FadeOut(wet), FadeOut(dry), run_time=0.36)
        self.play(FadeIn(plot), LaggedStart(*[Create(bar) for bar in bars], lag_ratio=0.13), run_time=1.22)
        self.play(Create(monthly_trace(plot, 2 * TEMPERATURE, RED)),
                  Transform(band, occupied_map().set_stroke(TEAL, 5)), run_time=1.22)
        self.finish()


class S02Title(TitleCard):
    LESSON = LESSON_TITLE
    TITLE = "Mapping Climates and Moving Ranges"

    def construct(self):
        plot = month_plot()
        self.add(landscape(), frames(), monthly_bars(plot), monthly_trace(plot, 2 * TEMPERATURE, RED))
        shade = poly([(-6.4, -2.5), (6.4, -2.5), (6.4, 3.2), (-6.4, 3.2)], BG, 0.82)
        self.add(shade)
        title = T(self.TITLE, 52, font=TITLE_FONT)
        lesson = T(self.LESSON, 30, TEAL)
        rule = Line(LEFT * 1.10, RIGHT * 1.10, color=GOLD, stroke_width=4)
        group = VGroup(title, rule, lesson).arrange(DOWN, buff=0.35)
        self.play(FadeIn(group), run_time=0.40)
        self.wait(0.99)
        self.play(FadeOut(group), run_time=0.40)


class S03Classify(SpokenScene):
    def construct(self):
        plot = month_plot()
        temp = monthly_trace(plot, 2 * TEMPERATURE, RED)
        rain = monthly_trace(plot, RAIN, BLUE)
        self.add(frames(), landscape(), plot, scope_tag("schematic", size=28, color=TEXT))
        self.at("walter lieth diagram")
        title = right("Walter–Lieth diagram")
        self.play(FadeIn(title), run_time=0.53)
        self.at("plots monthly temperature")
        self.play(Create(temp), run_time=0.99)
        self.at("beside rain")
        self.play(Create(rain), run_time=1.12)
        guide = plot.hline(20, color=GREY)
        unit_pair = VGroup(label("10 °C", 2.55, -1.21, RED, 28),
                           label("20 mm", 4.98, -1.21, BLUE, 28))
        self.at("a month reads dry")
        self.play(Create(guide), FadeIn(unit_pair), run_time=0.77)
        dry = note("Dry: rain < 2 × temperature", GOLD)
        # Interpolate exact crossings before filling the dry interval.
        months = np.arange(1, 13)
        margin = 2 * TEMPERATURE - RAIN
        crosses = [i + 1 + margin[i] / (margin[i] - margin[i + 1])
                   for i in range(11) if margin[i] * margin[i + 1] < 0]
        xs = np.array([crosses[0], 5, 6, 7, 8, 9, crosses[1]])
        top = [tuple(plot.pt(x, np.interp(x, months, 2 * TEMPERATURE))[:2]) for x in xs]
        bottom = [tuple(plot.pt(x, np.interp(x, months, RAIN))[:2]) for x in xs[::-1]]
        fill = poly(top + bottom, GOLD, 0.55)
        self.at("falls below twice")
        self.play(FadeOut(guide), FadeOut(unit_pair), run_time=0.38)
        self.add(fill)
        self.bring_to_front(temp, rain)
        self.play(FadeIn(fill), FadeIn(dry), run_time=1.12)
        cursor = ValueTracker(crosses[0])
        sample = plot.dot(cursor.get_value, lambda: np.interp(cursor.get_value(), months, RAIN),
                          color=BLUE, radius=0.085)
        self.add(sample)
        self.play(cursor.animate.set_value(crosses[1]), rate_func=linear, run_time=3.45)
        self.at("an empirical plant stress")
        stress = note("Empirical plant-stress marker", GOLD)
        self.play(swap(dry, stress),
                  fill.animate.set_fill(opacity=0.32), run_time=1.32)
        self.at("water balance")
        self.play(FadeOut(stress), FadeOut(sample), run_time=0.50)
        self.at("rules sort climates")
        self.play(FadeOut(VGroup(plot, fill, rain, temp, title)), run_time=0.48)
        ladder = Ledger([("Arid?", "1", GOLD), ("Temperature class", "2", RED),
                         ("Subtype rules", "3", TEAL)], top_left=(0.68, 2.54),
                        title="Köppen–Geiger", row_h=1.00, key_w=4.40, width=5.18, size=31)
        self.play(FadeIn(ladder), run_time=0.38)
        for i, (phrase, coords, color) in enumerate([
            ("aridity then", (-3.83, -1.23, 0.58, 0.65), GOLD),
            ("temperature class then", (-2.22, -0.13, 0.48, 0.67), RED),
            ("subtype rules", (-5.25, -1.37, 0.73, 0.66), TEAL),
        ]):
            zone = outline(*coords, color, width=3.5, fill=0.25)
            self.at(phrase)
            self.play(ladder.reveal(i), Create(zone), run_time=0.63)
        self.finish()


class S04Sdm(SpokenScene):
    def construct(self):
        weather = month_plot()
        old = VGroup(weather, monthly_trace(weather, RAIN, BLUE),
                     monthly_trace(weather, 2 * TEMPERATURE, RED))
        plot = niche_plot()
        dots = VGroup(*[Dot(p(*xy), radius=0.078, color=GREEN) for xy in MAP_POINTS])
        self.add(frames(), landscape(), old, scope_tag("schematic", size=28, color=TEXT))
        self.at("species distribution models")
        self.play(LaggedStart(*[GrowFromCenter(d) for d in dots], lag_ratio=0.21), run_time=1.8)
        self.at("following hutchinson")
        self.play(FadeOut(old), run_time=0.44)
        self.play(Create(plot.axes), run_time=1.90)
        self.at("become axes of")
        title = label("Niche space", 3.65, 2.72, TEXT, 35)
        self.play(FadeIn(plot.xlabel), FadeIn(plot.ylabel), FadeIn(title), run_time=0.74)
        self.at("a niche is")
        self.play(LaggedStart(*[
            TransformFromCopy(dot, Dot(plot.pt(*xy), radius=0.09, color=GREEN))
            for dot, xy in zip(dots, NICHE_POINTS)
        ], lag_ratio=0.34), run_time=2.40)
        self.at("replaces itself without")
        rule = note("Population replaces itself without immigrants")
        self.play(FadeIn(rule), run_time=0.68)
        self.at("the models fit")
        envelope = occupied_niche(plot)
        self.play(Create(envelope), FadeOut(rule), run_time=0.84)
        self.at("species was recorded")
        self.play(TransformFromCopy(envelope, occupied_map()), run_time=0.62)
        self.play(FadeIn(terrain_label("Occupied climate", -4.29, -0.30, GREEN, 30)), run_time=0.47)
        self.finish()


def predict_question():
    card = question_card(QUESTION, **CARD)
    text = card.question
    plate = RoundedRectangle(width=text.width + 0.67, height=0.80, corner_radius=0.13,
                             fill_color="#6E552D", fill_opacity=1,
                             stroke_color=GOLD, stroke_width=2.6).move_to(text)
    return plate, card


class S05PredictQ(SpokenScene):
    def construct(self):
        band = elevation_band(0, BLUE, 8)
        formula, warming, cooling = ratio_material()
        name = isotherm_label()
        self.add(frames(), landscape(), scope_tag("schematic", size=28, color=TEXT))
        self.at("as climate warms")
        self.play(Create(band), run_time=1.03)
        self.at("and isotherm")
        self.play(FadeIn(name), run_time=0.62)
        self.at("temperature climbs uphill")
        direction = arrow((-2.58, 0.35), (-2.00, 0.95), BLUE)
        self.play(GrowArrow(direction), run_time=1.46)
        self.at("its speed equals")
        self.play(FadeIn(formula[0]), run_time=0.68)
        self.at("divided by cooling")
        self.play(FadeIn(formula[1]), FadeOut(direction), run_time=1.10)
        self.at("slope warms 0")
        self.play(FadeIn(warming, shift=UP * 0.18), run_time=0.82)
        self.at("and cools 0")
        self.play(FadeIn(cooling, shift=UP * 0.18), run_time=0.82)
        self.at("how far uphill")
        plate, question = predict_question()
        plate.set_fill("#211B0D")
        self.play(GrowFromCenter(plate), run_time=0.51)
        self.play(FadeIn(question, run_time=0.60), plate.animate.set_fill("#6E552D"),
                  run_time=2.05, rate_func=linear)
        self.finish()


class S06PredictPause(PredictPause):
    QUESTION = QUESTION
    CARD = CARD
    SECONDS = 4.5

    def construct(self):
        self.add(predict_world(moving=False), *predict_question())
        self.wait(self.SECONDS)


class S07PredictReveal(SpokenScene):
    def construct(self):
        world = predict_world()
        contour = world.contour
        plate, question = predict_question()
        self.add(*world, plate, question)
        self.at("0 .3 divided")
        self.play(*[FadeOut(item) for item in world.inputs], FadeOut(plate), FadeOut(question), run_time=0.39)
        division = right(f"{WARMING:g} ÷ {COOLING_PER_100_M:g}", 1.95, TEXT, 41)
        answer = right(f"= {WARMING / COOLING_PER_100_M:g}", 1.18, BLUE, 40)
        self.play(FadeIn(division), run_time=0.52)
        self.at("is 0 .5")
        self.play(FadeIn(answer), run_time=0.62)
        self.at("times 100 meters")
        multiply = right(f"{WARMING / COOLING_PER_100_M:g} × 100 m", 0.24, TEXT, 38)
        self.play(FadeIn(multiply), run_time=0.80)
        origin = elevation_band(0, BLUE, 3).set_stroke(opacity=0.48)
        self.add(origin)
        self.at("the isotherm climbs")
        climb = right(f"= {ISOTHERM_SHIFT:g} m / decade", -0.47, BLUE, 39)
        self.play(Transform(contour, elevation_band(ISOTHERM_SHIFT, BLUE, 8), run_time=2.84),
                  FadeIn(climb, run_time=0.50))
        self.at("the measured median")
        species = elevation_band(0, GREEN, 9)
        self.play(Create(species), run_time=0.69)
        self.at("11 meters a decade", lead=0.50)
        species_rate = right(f"Species: {MEDIAN_SHIFT:g} m / decade", -1.46, GREEN, 32)
        self.play(Transform(species, elevation_band(MEDIAN_SHIFT, GREEN, 9), run_time=2.42),
                  FadeIn(species_rate, run_time=0.50))
        self.at("11 over 50")
        sx, sy, _ = species.get_end()
        cx, cy, _ = contour.get_end()
        brace_x = -1.30
        brace = line([(sx + 0.07, sy), (brace_x, sy), (brace_x, cy), (cx + 0.07, cy)], GOLD, 4)
        result = note(f"{MEDIAN_SHIFT:g} / {ISOTHERM_SHIFT:g} = {MEDIAN_SHIFT / ISOTHERM_SHIFT:.0%}", GOLD)
        self.play(Create(brace), FadeIn(result), run_time=2.54)
        self.finish()


def flow_seeds(start, end):
    arrows = VGroup(*[
        Arrow(p(start[0] + dx, start[1]), p(end[0] + dx, end[1]), buff=0,
              color=GOLD, stroke_width=3, tip_length=0.12)
        for dx in (-0.17, 0.17)
    ])
    seeds = VGroup(*[Dot(radius=0.047, color=YELLOW) for _ in range(5)])
    a, b = p(*start), p(*end)
    seeds.clock = 0.0

    def move(mob, dt):
        mob.clock += dt
        for i, seed in enumerate(mob):
            phase = (mob.clock / 1.8 + i / len(mob)) % 1
            seed.move_to(interpolate(a, b, phase))

    seeds.add_updater(move, call_updater=True)
    return arrows, seeds


def transplant_pin(x, color=GREEN):
    y = surface(x)
    return VGroup(Line(p(x, y), p(x, y + 0.40), color=color, stroke_width=5),
                  Dot(p(x, y + 0.42), color=color, radius=0.103))


class S08ControlsNiche(SpokenScene):
    def construct(self):
        plot = niche_plot()
        occupied = occupied_niche(plot)
        occupied_label = label("Occupied climate", 3.73, 2.78, GREEN, 34)
        band = occupied_map()
        self.add(frames(), landscape(), band, plot, occupied, occupied_label,
                 scope_tag("schematic", size=28, color=TEXT))
        factor = note("Tolerable conditions")
        self.at("tolerable conditions")
        self.play(FadeIn(factor), Indicate(occupied, color=GREEN), run_time=0.87)
        self.at("neighbors and places")
        neighbours = note("Neighbours")
        self.play(swap(factor, neighbours), run_time=0.48)
        self.at("places reached")
        reached = note("Places reached")
        self.play(swap(neighbours, reached), run_time=0.55)

        self.at("immigrants can sustain")
        arrows, seeds = flow_seeds((-4.76, -1.05), (-3.58, -0.85))
        self.play(LaggedStart(*[GrowArrow(a) for a in arrows], lag_ratio=0.24),
                  FadeOut(reached), run_time=1.11)
        self.add(seeds)
        patch = outline(-3.56, -0.91, 0.44, 0.32, GOLD, fill=0.30)
        self.at("sink population")
        sink_label = label("Sink", -3.46, 0.05, GOLD, 31)
        self.play(Create(patch), FadeIn(sink_label), run_time=0.64)
        pulse(patch, base=5, amp=2, speed=2.0)
        self.at("deaths beat births")
        deficit = note("Local deaths exceed births", GOLD)
        self.play(FadeIn(deficit), run_time=0.63)
        self.at("unreached suitable places")
        empty = outline(-2.12, 0.73, 0.47, 0.46, GREEN)
        empty_label = terrain_label("Empty suitable", -2.20, 1.63, GREEN, 30)
        self.play(Create(empty), FadeIn(empty_label),
                  FadeOut(deficit), run_time=1.20)

        self.at("models map occupied")
        self.play(occupied.animate.set_fill(opacity=0.40), run_time=0.93)
        larger = outline(*plot.pt(0.53, 0.54)[:2], 1.79, 1.44, GREY, width=4)
        self.at("fundamental niche")
        larger_label = label("Fundamental niche", 3.68, -1.36, TEXT, 29)
        self.play(Create(larger), run_time=1.33)
        self.play(FadeIn(larger_label), run_time=0.56)
        self.at("persist without competitors")
        self.play(larger.animate.set_stroke(opacity=0.58), run_time=1.40)

        self.at("transplants inside")
        # Place all three tests on the same slope, relative to one marked edge.
        edge = -3.88
        border = DashedLine(p(edge, -0.78), p(edge, 1.44), color=GREY, dash_length=0.12)
        # Reset the example before introducing the transplant treatment.
        self.play(FadeOut(VGroup(band, patch, empty, arrows, seeds, sink_label, empty_label)),
                  Create(border), run_time=0.52)
        loc = [-5.34, edge, -2.60]
        pins = [transplant_pin(x) for x in loc]
        tags = [label(s, x, 2.27, TEXT, 30) for s, x in
                zip(("Inside", "Edge", "Beyond"), (-5.35, -3.82, -1.93))]
        self.play(FadeIn(pins[0], shift=DOWN * 0.35), FadeIn(tags[0]), run_time=0.46)
        self.at("at and beyond")
        self.play(FadeIn(pins[1], shift=DOWN * 0.35), FadeIn(tags[1]), run_time=0.47)
        self.play(FadeIn(pins[2], shift=DOWN * 0.35), FadeIn(tags[2]), run_time=0.56)
        self.at("plantings fail")
        self.play(FadeOut(pins[2]), run_time=0.50)
        self.at("conditions there")
        self.play(FadeIn(note("If only beyond fails: conditions", GOLD)), run_time=0.58)
        self.finish()


def thermometer(x, y, height, fraction, color):
    shell = Line(p(x, y), p(x, y + height), color=GREY, stroke_width=10)
    column = Line(p(x, y), p(x, y + height * fraction), color=color, stroke_width=6)
    bulb = Dot(p(x, y), radius=0.12, color=color)
    return VGroup(shell, column, bulb)


def tracks():
    observed = VGroup(label("Observed", 3.3, 1.55, TEXT, 32),
                      Line(p(1.25, 1.15), p(5.42, 1.15), color=GREY, stroke_width=6))
    projected = VGroup(label("Scenario projection", 3.3, -0.45, TEAL, 32),
                       DashedLine(p(1.25, -0.91), p(5.42, -0.91), color=TEAL,
                                  dash_length=0.15, stroke_width=6))
    return observed, projected


# An invented continent for the schematic tiles; no real region is implied.
COAST = [(-5.92, 1.34), (-5.65, 2.28), (-4.53, 2.62), (-4.13, 2.36), (-3.53, 2.68),
         (-2.51, 2.39), (-2.14, 1.92), (-1.06, 1.60), (-1.31, 1.08), (-2.30, 0.80),
         (-2.63, 0.11), (-2.96, -0.07), (-3.16, -1.17), (-3.85, -1.92),
         (-4.28, -1.50), (-4.56, -0.71), (-4.43, -0.19), (-5.07, 0.12), (-5.46, 0.77)]


def coast_contains(x, y):
    intersections = []
    for (ax, ay), (bx, by) in zip(COAST, COAST[1:] + COAST[:1]):
        if (ay > y) != (by > y):
            intersections.append(ax + (y - ay) * (bx - ax) / (by - ay))
    return sum(v > x for v in intersections) % 2


def map_cells(spacing, confidence=False, epoch=0.0):
    cells = VGroup()
    for x in np.arange(-5.98 + spacing / 2, -0.92, spacing):
        for y in np.arange(-2.02 + spacing / 2, 2.74, spacing):
            if not coast_contains(x, y):
                continue
            color = (BLUE if y > 1.55 + epoch + 0.32 * np.sin(x * 1.9) else
                     GOLD if abs(x + 3.25) < 0.85 and y > -0.40 else GREEN)
            opacity = (0.52 + 0.37 * (np.sin(x * 5 + y * 4) + 1) / 2) if confidence else 0.9
            r = spacing * 0.46
            cells.add(poly([(x-r, y-r), (x+r, y-r), (x+r, y+r), (x-r, y+r)], color, opacity))
    return cells


def continent():
    water = poly([(-6.25, -2.29), (-0.42, -2.29), (-0.42, 3.04), (-6.25, 3.04)], "#1A303D")
    land = poly(COAST, "#3D5F5C", 1, 2.5)
    return VGroup(water, land)


class S09ControlsClimate(SpokenScene):
    def construct(self):
        world = landscape()
        self.add(frames(), world, scope_tag("schematic", size=28, color=TEXT))
        open_station = thermometer(-3.60, -0.53, 2.18, 0.81, RED)
        logger = thermometer(-5.53, -1.76, 0.86, 0.60, BLUE)
        self.at("open weather stations")
        self.play(GrowFromEdge(open_station, DOWN), run_time=1.0)
        self.at("miss forest shade")
        self.play(GrowFromEdge(logger, DOWN), run_time=0.76)
        station_label = terrain_label("Open station", -3.50, 2.65, TEXT, 30)
        logger_label = terrain_label("Understory", -5.12, -0.45, BLUE, 31)
        self.play(FadeIn(station_label), FadeIn(logger_label), run_time=0.56)

        self.at("2019 dafran")
        cite = right("De Frenne et al. · 2019")
        self.play(FadeIn(cite), run_time=0.64)
        compare = VGroup(thermometer(2.18, -0.94, 3.04, 0.81, RED),
                         thermometer(4.47, -0.94, 3.04, 0.81, BLUE))
        self.at("found understories")
        self.play(TransformFromCopy(open_station, compare[0]),
                  TransformFromCopy(logger, compare[1]), run_time=1.18)
        cool = thermometer(4.47, -0.94, 3.04, 0.81 + UNDERSTORY_OFFSET / 15, BLUE)
        self.at("averaged about")
        result = right(f"−{abs(UNDERSTORY_OFFSET):g} °C on average", -1.70, BLUE, 36)
        self.play(Transform(compare[1], cool), FadeIn(result), run_time=0.80)
        self.at("maximum temperature")
        maximum = note("Difference in maximum temperature")
        self.play(FadeIn(maximum), run_time=0.50)

        self.at("fire soils and")
        self.play(FadeOut(VGroup(station_label, logger_label, cite, result, maximum)),
                  FadeOut(VGroup(open_station, logger, *compare)), run_time=0.42)
        flame = poly([(-4.12, -0.86), (-4.24, -0.30), (-4.02, -0.51),
                      (-3.89, 0.12), (-3.74, -0.30), (-3.61, -0.52),
                      (-3.63, -0.82), (-3.88, -1.03)], RED)
        soil = line([(-3.52, -1.95), (-2.68, -1.65), (-1.91, -0.90)], GOLD, 5)
        self.play(GrowFromEdge(flame, DOWN), Create(soil), run_time=0.72)
        self.at("forest loss also")
        self.play(FadeOut(world.grove[1]), FadeOut(world.grove[2]),
                  FadeOut(world.grove[4]), run_time=1.25)
        self.at("reshape vegetation")
        habitat = note("Fire, soils and forest loss", GOLD)
        self.play(FadeOut(flame), FadeIn(habitat), run_time=0.73)
        self.at("models report confidence")
        confidence = label("Confidence", 2.50, 2.50, TEXT, 30)
        tiles = VGroup(*[poly([(x, 2.23), (x + 0.54, 2.23), (x + 0.54, 2.76), (x, 2.76)],
                              TEXT, opacity) for x, opacity in [(3.85, 0.34), (4.51, 0.61), (5.17, 0.94)]])
        self.play(FadeIn(confidence), LaggedStart(*[FadeIn(t) for t in tiles], lag_ratio=0.2),
                  FadeOut(habitat), run_time=0.83)
        self.at("keep projections apart")
        observed, projected = tracks()
        self.play(Create(projected[1]), FadeIn(projected[0]), run_time=0.61)
        self.at("from observations")
        self.play(Create(observed[1]), FadeIn(observed[0]), run_time=0.66)
        self.finish()


def class_change_chart():
    return Plot(box=(1.15, 5.95, -1.32, 2.00), xr=(0, 3), yr=(0, 15),
                yticks=[(0, "0"), (5, "5"), (10, "10"), (15, "15%")],
                size=28, color="#A9B5C3")


def vertical_bar(plot, x, percent, color):
    a, b = plot.pt(x - 0.25, 0), plot.pt(x + 0.25, percent)
    return poly([(a[0], a[1]), (b[0], a[1]), (b[0], b[1]), (a[0], b[1])], color, 0.83)


def climate_scan(color=GREY):
    # A reading cursor for the map, separate from the cells whose classes change.
    return poly([(-6.06, -1.08), (-5.28, -1.08), (-5.28, 2.76),
                 (-6.06, 2.76)], color, 0.39)


class S10Unlocked1(SpokenScene):
    def construct(self):
        map_base = continent()
        cells = map_cells(0.58)
        self.add(frames(), map_base, scope_tag("schematic map", size=28, color=TEXT))
        self.at("2018 and 2023")
        cite = right("Beck et al. · 2018, 2023", 2.70)
        self.play(FadeIn(cite), FadeIn(cells), run_time=1.65)
        self.at("colleagues mapped")
        detail = map_cells(0.30)
        self.play(FadeOut(cells), FadeIn(detail), run_time=2.08)
        self.at("about 1 km")
        grid = note("Köppen–Geiger grid · about 1 km")
        self.play(FadeIn(grid), run_time=0.67)
        self.at("with confidence levels")
        shaded = map_cells(0.30, confidence=True)
        self.play(Transform(detail, shaded), run_time=1.28)
        conf = label("Confidence\nshading", -1.84, -1.53, TEXT, 28, width=2.60)
        self.play(FadeIn(conf), run_time=0.40)

        plot = class_change_chart()
        heading = right("Land changing major class", 2.63, TEXT, 32)
        self.play(swap(cite, heading), FadeIn(plot), run_time=0.66)
        observed = vertical_bar(plot, 0.57, 5, GREY)
        obs = label("Observed", 2.05, -1.83, TEXT, 28)
        val = label("~5%", 2.05, 0.19, TEXT, 32)
        self.at("about 5")
        self.play(GrowFromEdge(observed, DOWN), FadeIn(obs), FadeIn(val), run_time=0.70)
        self.at("between 1901")
        start = label("1901–1930", -4.42, -2.96, TEXT, 31)
        first_epoch = map_cells(0.30, confidence=True, epoch=-0.23)
        self.play(swap(grid, start), Transform(detail, first_epoch), run_time=0.82)
        time_span = arrow((-2.98, -2.96), (0.95, -2.96), GREY)
        self.play(GrowArrow(time_span), run_time=1.28, rate_func=linear)
        self.at("and 1991")
        observed_period = label("1991–2020", 2.33, -2.96, TEXT, 31)
        second_epoch = map_cells(0.30, confidence=True)
        sweep = climate_scan()
        self.add(sweep)
        self.play(FadeIn(observed_period), Transform(detail, second_epoch),
                  sweep.animate.shift(RIGHT * 4.66), run_time=3.34, rate_func=linear)
        self.remove(sweep)

        self.at("by 2071")
        projected_period = note("Projection for 2071–2099", TEAL)
        future = map_cells(0.30, confidence=True, epoch=0.25)
        self.play(FadeOut(VGroup(start, time_span, observed_period)), run_time=0.40)
        sweep = climate_scan(TEAL)
        self.add(sweep)
        self.play(FadeIn(projected_period), Transform(detail, future),
                  sweep.animate.shift(RIGHT * 4.66), run_time=2.30, rate_func=linear)
        self.remove(sweep)
        self.at("scenarios project")
        low, high = [vertical_bar(plot, x, value, TEAL) for x, value in [(1.61, 5), (2.57, 13)]]
        options = VGroup(label("Low", 3.72, -1.69, TEAL, 29),
                         label("High", 5.25, -1.69, TEAL, 29),
                         label("Emissions", 4.49, -2.16, TEXT, 28))
        self.play(LaggedStart(GrowFromEdge(low, DOWN), GrowFromEdge(high, DOWN), lag_ratio=0.42),
                  FadeIn(options), run_time=0.82)
        self.at("5 to 13")
        self.play(FadeIn(label("5%", 3.72, 0.19, TEAL, 32)),
                  FadeIn(label("13%", 5.25, 1.95, TEAL, 32)), run_time=0.62)
        self.at("a class change")
        self.play(swap(projected_period, note("Climate class change ≠ biome change", GOLD)),
                  run_time=0.84)
        self.finish()


def arrow(start, end, color):
    return Arrow(p(*start), p(*end), buff=0, tip_length=0.23,
                 max_tip_length_to_length_ratio=0.45, color=color, stroke_width=8)


def transplant_bars():
    plot = Plot(box=(0.72, 5.95, -1.98, 1.86), xr=(0, 50), yr=(0, 3))
    bars = VGroup()
    for y, value, key, color in [(2.50, 46, "Niche limit", GREEN),
                                 (1.54, 26, "Dispersal limit", TEAL),
                                 (0.58, 23, "Sink", GOLD)]:
        start, end = plot.pt(0, y), plot.pt(value, y)
        bar = line([(start[0], start[1]), (end[0], end[1])], color, 13)
        text = label(f"{value}%   {key}", 0, start[1] + 0.36, color, 31)
        text.align_to(p(0.72, 0), LEFT)
        bars.add(VGroup(bar, text))
    return bars


class S11Unlocked2(SpokenScene):
    def construct(self):
        map_base = continent()
        map_detail = map_cells(0.30, confidence=True)
        geography = VGroup(map_base, map_detail)
        self.add(frames(), geography, scope_tag("schematic", size=28, color=TEXT))
        self.at("chen thomas and")
        cite = right("Chen et al. · 2011")
        self.play(FadeIn(cite), run_time=0.63)
        self.at("pooled land range shifts")
        pooled = right("Median range shifts", 1.43, TEXT, 37)
        self.play(FadeIn(pooled), run_time=0.31)
        north = arrow((-4.60, -0.21), (-4.60, 2.44), GREEN)
        north.set_stroke(width=12)
        self.at("land range shifts")
        shade = poly([(-6.24, -2.28), (-0.43, -2.28), (-0.43, 3.03), (-6.24, 3.03)], BG, 0.56)
        self.play(FadeIn(shade), run_time=1.81, rate_func=linear)
        self.at("median shifts were")
        self.play(GrowArrow(north), run_time=1.65, rate_func=linear)
        self.at("kilometers poleward")
        lat = right("16.9 km / decade poleward", 0.35, GREEN, 32)
        self.play(FadeIn(lat), run_time=0.59)

        self.at("11 meters uphill")
        slope = landscape()
        self.play(FadeOut(VGroup(geography, shade, north)), FadeIn(slope), run_time=0.58)
        uphill = arrow((-4.29, -0.72), (-3.22, -0.03), GREEN)
        elev = right(f"{MEDIAN_SHIFT:.1f} m / decade uphill", -0.74, GREEN, 32)
        self.play(GrowArrow(uphill), FadeIn(elev), run_time=0.78)
        self.at("largest where warming")
        bigger = arrow((-4.29, -0.72), (-1.98, 1.26), GREEN)
        heat = elevation_band(50, BLUE, 7)
        self.play(Transform(uphill, bigger), Create(heat), run_time=1.27)

        self.at("in 2014 hargreaves")
        trial_cite = right("Hargreaves et al. · 2014", 2.68, TEXT, 33)
        self.play(FadeOut(VGroup(pooled, lat, elev, uphill, heat)),
                  swap(cite, trial_cite), run_time=0.78)
        self.at("reviewed 111 transplant")
        trials = right("111 transplant tests", 2.02, TEXT, 32)
        pins = VGroup(*[transplant_pin(x) for x in [-5.34, -3.88, -2.60]])
        self.play(FadeIn(trials), LaggedStart(*[FadeIn(pin, shift=DOWN * 0.42) for pin in pins], lag_ratio=.44),
                  run_time=2.30)
        self.at("beyond range edges")
        boundary = DashedLine(p(-3.69, -0.84), p(-3.69, 1.16), color=GREY, dash_length=0.12)
        self.play(Create(boundary), run_time=0.71)

        bars = transplant_bars()
        self.at("only 46 percent")
        self.play(Create(bars[0][0]), FadeIn(bars[0][1]), run_time=1.42)
        self.at("at a niche limit")
        self.play(FadeOut(pins[2]), run_time=0.63)
        self.at("pointed to dispersal")
        self.play(Create(bars[1][0]), FadeIn(bars[1][1]), FadeIn(pins[2]), run_time=0.61)
        self.at("or sinks", lead=0.45)
        self.play(Create(bars[2][0]), FadeIn(bars[2][1]),
                  FadeIn(note("Shares do not add to 100%")), run_time=0.35)
        self.finish()


class S12End(EndCard):
    LINE = "Climate gives a first guess; dispersal, neighbours and land shape ranges."
