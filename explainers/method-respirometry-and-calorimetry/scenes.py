"""Measuring Metabolism From the Outside.

Color map follows the patch-clamp film: blue apparatus, grey structure,
yellow recorded oxygen signal, green controls, red heat loss, orange
additions, teal exchanged gas (CO₂), purple cellular machinery, gold rule.
"""
from bp_parts import *
from bp_style import EndCard

PURPLE = "#B58CD9"
ORANGE = "#F29E4C"
HEAT = RED
OXYGEN = YELLOW
CARBON = TEAL
LEFT_X = -3.4
RIGHT_X = 3.35
SAMPLE_SCALE = 0.73
INHALED, EXHALED = 21, 16
UPTAKE = (INHALED - EXHALED) / 100
QUESTION = "Does this raise the body's CO₂/O₂ ratio?"
QUESTION_STYLE = dict(y=3.45, size=36, max_w=12.2)


def p(x, y):
    return np.array([x, y, 0.0])


def label(text, x, y, color=TEXT, size=32):
    return T(text, size, color).move_to(p(x, y))


def number(text, x, y, color=TEXT, size=36):
    return M(text, size, color).move_to(p(x, y))


def heading(text, color=TEXT):
    return label(text, LEFT_X, 3.25, color, 34)


def arrow(a, b, color=TEXT, width=5, tip=0.19):
    return Arrow(a, b, color=color, stroke_width=width, buff=0, tip_length=tip)


def vessel():
    glass = RoundedRectangle(width=6.0, height=5.48, corner_radius=0.40,
                             stroke_color=BLUE, stroke_width=4,
                             fill_color=BLUE, fill_opacity=0.32)
    rail = Line(p(-2.54, -2.28), p(2.54, -2.28), color=BLUE, stroke_width=3)
    return VGroup(glass, rail).shift(RIGHT * LEFT_X)


def mammal():
    """A resting mouse silhouette, without anatomical or molecular detail."""
    body = Ellipse(width=2.95, height=2.05, color=GREY, fill_color=GREY,
                   fill_opacity=1, stroke_width=2).move_to(p(-0.24, -0.48))
    haunch = Ellipse(width=1.71, height=1.47, stroke_width=0, fill_color="#A6ABB6",
                    fill_opacity=1).move_to(p(-0.83, -0.72))
    head = Ellipse(width=1.44, height=1.16, stroke_width=0, fill_color=GREY,
                   fill_opacity=1).rotate(-0.24).move_to(p(1.05, -0.57))
    ear = Circle(radius=0.34, color="#B4B9C4", fill_color=GREY,
                 fill_opacity=1, stroke_width=3).move_to(p(0.83, -0.02))
    foot = Ellipse(width=0.86, height=0.26, stroke_width=0, fill_color="#A6ABB6",
                   fill_opacity=1).move_to(p(0.72, -1.42))
    tail = CubicBezier(p(-1.45, -0.89), p(-2.7, -1.0), p(-2.45, -2.02), p(-0.97, -1.72))
    tail.set_stroke(GREY, 7)
    eye = Dot(p(1.42, -0.42), radius=0.064, color=BG)
    nose = Dot(p(1.74, -0.77), radius=0.073, color=BG)
    return VGroup(tail, foot, body, haunch, head, ear, eye, nose).shift(RIGHT * LEFT_X)


def lungs():
    parts = VGroup()
    for side in (-1, 1):
        part = Ellipse(width=0.52, height=0.90, stroke_width=2, stroke_color=TEXT,
                       fill_color=PURPLE, fill_opacity=0.97)
        parts.add(part.rotate(-side * 0.18).move_to(p(LEFT_X + side * 0.29, -0.37)))
    stem = Line(p(LEFT_X, 0.43), p(LEFT_X, -0.1), stroke_width=8, color=PURPLE)
    return VGroup(stem, parts)


def gas_path(incoming):
    if incoming:
        return CubicBezier(p(-6.67, 1.33), p(-5.05, 1.33), p(-3.50, 1.25), p(LEFT_X, 0.37))
    return CubicBezier(p(LEFT_X + 0.24, 0.31), p(-2.48, 0.93), p(-1.6, 1.57), p(-0.18, 1.59))


def flow(path, color, count=6, period=3.2, radius=0.115, strength=1.0):
    """Move a continuous stream of schematic markers along a physical flow path."""
    particles = VGroup(*[Dot(radius=radius, color=color) for _ in range(count)])
    elapsed = 0.0

    def advance(group, dt):
        nonlocal elapsed
        elapsed += dt
        for index, marker in enumerate(group):
            phase = (elapsed / period + index / count) % 1
            marker.move_to(path.point_from_proportion(phase))
            marker.set_opacity(strength * min(1.0, phase * 10, (1 - phase) * 10))

    advance(particles, 0.0)
    return particles.add_updater(advance)


def gas(incoming, color, strength=1.0):
    path = gas_path(incoming)
    path.set_stroke(color, width=16, opacity=0.34 * strength)
    return VGroup(path, flow(path, color, strength=strength))


def heat_ripples():
    """Arcs travel from the animal's back to the wall."""
    arcs = VGroup()
    for index in range(3):
        arc = Arc(radius=1, start_angle=PI / 4, angle=PI / 2, stroke_color=HEAT, stroke_width=7)
        elapsed = [index * 1.02]

        def spread(mob, dt, time=elapsed):
            time[0] += dt
            q = (time[0] % 3.06) / 3.06
            mob.become(Arc(radius=1.04 + 1.38 * q, start_angle=PI / 4, angle=PI / 2,
                           arc_center=p(LEFT_X - 0.22, -0.21), stroke_color=HEAT,
                           stroke_width=7, stroke_opacity=0.92 * np.sin(PI * q)))

        spread(arc, 0)
        arcs.add(arc.add_updater(spread))
    return arcs


def oxygen_amount(t):
    # Constant schematic ventilation, in arbitrary volume units per model time.
    return UPTAKE * t


def oxygen_monitor(tracker):
    box = (0.83, 6.16, 0.77, 2.34)
    plot = Plot(box, (0, 10), (0, 0.53), label_size=28)
    title = label("Oxygen used", RIGHT_X, box[3] + 0.44, OXYGEN, 33)
    return VGroup(plot, title, plot.live_curve(oxygen_amount, tracker, OXYGEN, width=8),
                  plot.dot(tracker.get_value, lambda: oxygen_amount(tracker.get_value()),
                           color=OXYGEN, ring=OXYGEN, radius=0.105))


def heat_monitor(tracker, center=p(RIGHT_X, -1.14), radius=1.08, title="Heat loss"):
    return dial(tracker, center=center, radius=radius, label=title, color=HEAT, fmt=" ", size=28)


def percentage_bar(text, percent, y):
    track = RoundedRectangle(width=4.65, height=0.60, corner_radius=0.18,
                             stroke_color=GREY, stroke_width=2, fill_color=BLUE,
                             fill_opacity=0.14).move_to(p(RIGHT_X, y))
    length = (track.width - 0.18) * percent / 100
    fill = RoundedRectangle(width=length, height=0.42, corner_radius=0.11,
                            stroke_width=0, fill_color=OXYGEN, fill_opacity=1)
    fill.align_to(track, LEFT).shift(RIGHT * 0.09)
    fill.set_y(y)
    title = label(text, RIGHT_X, y + 0.66, TEXT, 29).align_to(track, LEFT)
    value = number(f"{percent}% O₂", RIGHT_X, y + 0.66, OXYGEN, 31).align_to(track, RIGHT)
    return VGroup(track, title), fill, value


def thermometer(x, y, tracker, color, height=1.45):
    stem = RoundedRectangle(width=0.35, height=height, corner_radius=0.17,
                            stroke_color=TEXT, stroke_width=2.5).move_to(p(x, y))
    bulb = Circle(radius=0.22, stroke_color=TEXT, stroke_width=2.5, fill_color=color,
                  fill_opacity=1).move_to(stem.get_bottom())
    base = stem.get_bottom() + UP * 0.08

    def level():
        length = (height - 0.23) * tracker.get_value()
        return RoundedRectangle(width=0.19, height=length, corner_radius=0.085,
                                stroke_width=0, fill_color=color, fill_opacity=1).move_to(base + UP * length / 2)

    return VGroup(stem, always_redraw(level), bulb)


def balance(gain="G"):
    """The steady-state balance, with each symbol aligned to its meaning."""
    made = VGroup(number("M", 1.38, 0.71, HEAT),
                  label("Heat made", 1.38, 0.13, size=28))
    gained = VGroup(number(gain, 4.99, 0.71, BLUE),
                    label("Heat gained", 4.99, 0.13, size=28))
    dry = VGroup(number("C × (Tb − Ta)", 2.36, -1.04, HEAT, 32),
                 label("Dry leak", 2.36, -1.63, size=28))
    evap = VGroup(number("E", 5.48, -1.04, TEAL),
                  label("Evaporation", 5.48, -1.63, size=28))
    return made, number("+", 3.24, 0.71), gained, number("=", 0.39, -1.04), dry, number("+", 4.48, -1.04), evap


def heat_routes():
    return (
        (arrow(p(-4.66, 0.19), p(-5.44, 1.28), HEAT), label("Radiation", -5.17, 2.25, HEAT, 28)),
        (arrow(p(-3.22, -1.25), p(-3.22, -2.18), HEAT), label("Contact", -2.19, -1.92, HEAT, 28)),
        (arrow(p(-2.19, 0.11), p(-1.37, 1.12), HEAT), label("Moving air", -1.97, 2.25, HEAT, 28)),
    )


def ratio_meter(tracker):
    return dial(tracker, p(RIGHT_X, -0.92), radius=1.46, label="CO₂/O₂ ratio", color=CARBON,
                fmt=" ", size=28)


def pathway():
    branch = CubicBezier(p(-4.72, -0.64), p(-3.72, -0.67), p(-3.49, -0.40), p(-3.22, 0.12))
    branch.set_stroke(PURPLE, width=12)
    junction = Dot(p(-3.22, 0.12), radius=0.17, color=PURPLE)
    title = label("Pentose phosphate\npathway", LEFT_X, 1.87, PURPLE, 30)
    return VGroup(branch, junction, title)


def co2_bubble():
    return chip("CO₂", CARBON, 29, fill_opacity=0.23).move_to(p(-2.18, 1.05))


def prediction_parts(dimmed=True):
    glass = vessel()
    if dimmed:
        glass[0].set_fill(opacity=0.21)
    return (glass, mammal(), pathway(), co2_bubble(),
            label("Step uses 0 O₂", LEFT_X + 0.66, -2.00, OXYGEN, 28))


def prediction_meter(ratio):
    return (oxygen_monitor(ValueTracker(8)), ratio_meter(ratio),
            label("?", RIGHT_X + 1.83, 0.01, GOLD, 39), scope_tag(size=26))


def sample_vessel():
    return vessel().scale(SAMPLE_SCALE).move_to(p(LEFT_X, -0.32))


def sample_dish():
    rim = Ellipse(width=3.39, height=1.47, stroke_color=BLUE, stroke_width=4,
                  fill_color=BLUE, fill_opacity=0.18).move_to(p(LEFT_X, -0.63))
    base = Ellipse(width=3.39, height=1.47, stroke_color=BLUE, stroke_width=3)
    base.move_to(rim).shift(DOWN * 0.18)
    return VGroup(base, rim)


def sample_muscle():
    grains = VGroup()
    for x, y, angle in [(-1.04, -0.13, 23), (-0.51, 0.19, -12), (-0.46, -0.31, 35),
                         (0.03, -0.09, -42), (0.36, 0.23, 19), (0.57, -0.29, 25),
                         (1.05, -0.08, -17)]:
        grain = RoundedRectangle(width=0.52, height=0.24, corner_radius=0.10,
                                 stroke_color=TEXT, stroke_width=1.8,
                                 fill_color=PURPLE, fill_opacity=1)
        grains.add(grain.rotate(angle * DEGREES).move_to(p(LEFT_X + x, -0.62 + y)))
    return grains


def mito_sample():
    organelles = VGroup()
    for x, y, angle in [(-1.04, -0.05, 25), (-0.34, 0.17, -22),
                         (-0.43, -0.37, 17), (0.34, -0.10, -24), (0.99, -0.02, 22)]:
        blob = Ellipse(width=0.68, height=0.35, stroke_color=PURPLE, stroke_width=3,
                       fill_color=PURPLE, fill_opacity=0.5)
        inner = Ellipse(width=0.47, height=0.19, stroke_color=TEXT, stroke_width=2)
        organelles.add(VGroup(blob, inner).rotate(angle * DEGREES).move_to(p(LEFT_X + x, -0.59 + y)))
    return organelles


def probe():
    stem = RoundedRectangle(width=0.28, height=1.56, corner_radius=0.11,
                            color=BLUE, stroke_width=3, fill_color=BLUE, fill_opacity=0.57)
    stem.move_to(p(LEFT_X, 0.39))
    tip = Dot(stem.get_bottom(), color=OXYGEN, radius=0.105)
    cable = VMobject(stroke_color=BLUE, stroke_width=4)
    cable.set_points_as_corners([stem.get_top(), p(LEFT_X, 2.02), p(0.46, 2.02)])
    return VGroup(stem, tip, cable)


def manometer():
    tube = VMobject(stroke_color=BLUE, stroke_width=6)
    tube.set_points_as_corners([p(-1.30, 0.52), p(-0.89, 0.52), p(-0.89, -0.55),
                               p(-0.25, -0.55), p(-0.25, 1.80), p(0.46, 1.80)])
    liquid = VMobject(stroke_color=OXYGEN, stroke_width=5)
    liquid.set_points_as_corners([p(-0.89, -0.05), p(-0.89, -0.55),
                                  p(-0.25, -0.55), p(-0.25, -0.05)])
    return VGroup(tube, liquid)


def sample_plot():
    return Plot((0.79, 6.23, -2.02, 2.12), (0, 10), (0, 1), xlabel="Time",
                ylabel="Oxygen remaining", label_size=32, color=TEXT)


def cycle_oxygen(t):
    # Normalized oxygen balance: baseline consumption + extra consumption after the pinch.
    return 0.9 - 0.031 * t - 0.079 * max(0, t - 3.2)


def fuel_only_oxygen(t):
    # The orange reference isolates the small oxygen demand of the added acid as fuel.
    return 0.9 - 0.031 * t - 0.014 * max(0, t - 3.2)


def mito_oxygen(t):
    # Integrate a shallow basal rate, a faster ADP-stimulated rate, then basal again.
    stimulated = np.clip(t - 2.8, 0, 3.8)
    return 0.9 - 0.023 * t - 0.124 * stimulated


def sample_trace(plot, fn, tracker):
    def shaded_trace():
        t = tracker.get_value()
        top = [plot.pt(x, fn(x)) for x in np.linspace(0, t, 50)]
        return Polygon(plot.pt(0, 0), *top, plot.pt(t, 0), stroke_width=0,
                       fill_color=OXYGEN, fill_opacity=0.34)

    return VGroup(always_redraw(shaded_trace), plot.live_curve(fn, tracker, color=OXYGEN, width=9),
                  plot.dot(tracker.get_value, lambda: fn(tracker.get_value()), color=OXYGEN,
                           ring=OXYGEN, radius=0.11))


def machinery():
    return (boxed_label("Respiratory\nchain", OXYGEN, size=29, box=(2.49, 1.13),
                        fill_opacity=0.25).move_to(p(-4.89, 0.12)),
            boxed_label("ATP\nsynthase", PURPLE, size=29, box=(2.21, 1.13),
                        fill_opacity=0.08).move_to(p(-2.02, 0.12)))


class S01Hook(SpokenScene):
    def construct(self):
        animal, glass = mammal(), vessel()
        unknown = label("?", LEFT_X - 0.15, -0.46, GOLD, 72)
        self.add(glass, animal, unknown)
        bob(animal, amp=0.11, speed=2.2)
        bob(unknown, amp=0.11, speed=2.2)
        self.at("every living system", lead=0.45)
        inlet = gas(True, OXYGEN)
        self.play(FadeIn(inlet), run_time=0.65)
        self.at("trades oxygen")
        self.play(FadeIn(label("O₂", -5.82, 1.87, OXYGEN, 31)), run_time=0.37)
        self.at("carbon dioxide", lead=0.5)
        self.play(FadeIn(gas(False, CARBON)), run_time=0.48)
        self.play(FadeIn(label("CO₂", -1.51, 2.09, CARBON, 31)), run_time=0.32)
        self.at("and heat", lead=0.14)
        self.add(heat_ripples())
        self.at("seal it in")
        self.play(Indicate(glass[0], color=BLUE, scale_factor=1), run_time=0.82)
        self.at("those flows expose", lead=0.35)
        oxygen, heat = ValueTracker(0.1), ValueTracker(0.32)
        self.add(oxygen_monitor(oxygen), heat_monitor(heat, title="Heat flow"), scope_tag(size=26))
        self.play(oxygen.animate.set_value(7.6), heat.animate.set_value(0.65), run_time=2.35, rate_func=linear)
        self.finish()


class S02Title(TitleCard):
    TITLE = "Measuring Metabolism From the Outside"
    LESSON = "Respirometry and Calorimetry"

    def construct(self):
        glass, animal = vessel(), mammal()
        self.add(glass, animal)
        self.play(glass.animate.set_opacity(0.15), animal.animate.set_opacity(0.10), run_time=0.36)
        self.add(gas(True, OXYGEN, strength=0.19), gas(False, CARBON, strength=0.19))
        title = fit_text(self.TITLE, max_w=12.2, size=51, min_size=39, font=TITLE_FONT)
        self.play(FadeIn(title), run_time=0.40)
        self.wait(1.20)


class S03Respirometry(SpokenScene):
    def construct(self):
        animal = mammal()
        self.add(vessel(), animal, lungs(), gas(True, OXYGEN), scope_tag(size=26))
        bob(animal, amp=0.09, speed=2.1)
        self.at("a method called", lead=0.18)
        self.play(FadeIn(heading("Respirometry", OXYGEN)), run_time=0.55)
        self.at("compare air entering", lead=0.5)
        self.play(FadeIn(gas(False, OXYGEN)), run_time=0.66)
        incoming = percentage_bar("Air in", INHALED, 1.26)
        outgoing = percentage_bar("Air out", EXHALED, -0.24)
        self.play(FadeIn(incoming[0]), FadeIn(outgoing[0]), run_time=0.74)
        self.at("21 % oxygen")
        self.play(GrowFromEdge(incoming[1], LEFT), FadeIn(incoming[2]), run_time=0.58)
        self.at("16%")
        self.play(GrowFromEdge(outgoing[1], LEFT), FadeIn(outgoing[2]), run_time=0.58)
        terms = [number(content, x, -1.48, OXYGEN, 34) for content, x in
                 [(f"{INHALED}%", 1.51), ("−", 2.35), (f"{EXHALED}%", 3.26),
                  ("=", 4.15), (f"{INHALED - EXHALED}%", 5.07)]]
        for cue, term in zip(("21 minus", "minus 16", "16 leaves", "leaves about", "5 % of"), terms):
            self.at(cue, lead=0.15)
            self.play(FadeIn(term), run_time=0.26)
        self.at("multiply that drop", lead=0.42)
        self.play(FadeOut(VGroup(*incoming, *outgoing, *terms)), run_time=0.37)
        factor = label(f"{INHALED - EXHALED}% × air breathed", RIGHT_X, -1.70, OXYGEN, 35)
        self.add(factor)
        tracker = ValueTracker(0.14)
        # Use the same monitor convention as the hook, leaving the arithmetic below.
        self.add(oxygen_monitor(tracker))
        self.play(tracker.animate.set_value(9.5), run_time=3.95, rate_func=linear)
        self.finish()


class S04Calorimetry(SpokenScene):
    def construct(self):
        animal = mammal()
        heat = ValueTracker(0.28)
        monitor = heat_monitor(heat, center=p(RIGHT_X, 2.15), radius=0.73, title="")
        heat_title = label("Heat flow", RIGHT_X, 1.72, HEAT, 30)
        self.add(vessel(), animal, heat_ripples(), monitor, scope_tag(size=26))
        bob(animal, amp=0.09, speed=2.1)
        self.at("follow heat", lead=0.25)
        self.play(FadeIn(heading("Calorimetry", HEAT)), FadeIn(heat_title),
                  heat.animate.set_value(0.67), run_time=1.45)
        self.at("metabolic rate is")
        units = caption("Metabolic rate = energy used / time", size=32)
        self.play(FadeIn(units), run_time=0.6)
        self.at("in watts")
        watts = caption("Metabolic rate = energy used / time  (W)", size=32)
        self.play(swap(units, watts, 0.66))
        self.at("at steady state", lead=0.43)
        temp = thermometer(-5.42, 0.55, ValueTracker(0.69), GREEN)
        self.play(FadeIn(temp), run_time=0.63)
        self.at("body temperature holds")
        temp_text = label("Body temperature", -3.63, 2.35, GREEN, 28)
        self.play(FadeIn(temp_text), run_time=0.49)
        self.at("no heat is stored")
        steady = caption("Steady state: no heat stored", size=31, color=GREEN)
        self.play(swap(watts, steady, 0.65))
        equation = balance()
        for cue, group in [
            ("heat made plus", (equation[0],)), ("plus heat gained", equation[1:3]),
            ("equals dry leak", equation[3:5]), ("plus evaporation", equation[5:]),
        ]:
            self.at(cue, lead=0.16)
            self.play(*(FadeIn(part) for part in group), run_time=0.41)
        self.at("dry leak means", lead=0.34)
        self.play(FadeOut(temp_text), FadeOut(temp), run_time=0.4)
        for cue, (route, name) in zip(("means radiation", "contact and", "and moving air"), heat_routes()):
            self.at(cue, lead=0.20)
            self.add(route)
            self.play(FadeIn(name), run_time=0.36)
        self.finish()


class S04bRate(SpokenScene):
    def construct(self):
        animal = mammal()
        heat = ValueTracker(0.67)
        parts = balance()
        monitor = heat_monitor(heat, center=p(RIGHT_X, 2.15), radius=0.73, title="")
        heat_title = label("Heat flow", RIGHT_X, 1.72, HEAT, 30)
        routes = VGroup(*(m for pair in heat_routes() for m in pair))
        steady = caption("Steady state: no heat stored", size=31, color=GREEN)
        calorimetry = heading("Calorimetry", HEAT)
        self.add(vessel(), animal, heat_ripples(), calorimetry, monitor, heat_title,
                 routes, steady, *parts, scope_tag(size=26))
        bob(animal, amp=0.09, speed=2.1)
        self.at("with nothing heating", lead=0)
        zero = balance("0")[2]
        self.play(swap(parts[2], zero, 0.87), FadeOut(routes), run_time=0.87)
        self.at("heat made equals", lead=0.17)
        equality = label("M = heat lost", RIGHT_X, -0.28, HEAT, 39)
        self.play(*(FadeOut(item) for item in (*parts[:2], *parts[3:], zero)), run_time=0.51)
        self.play(FadeIn(equality), run_time=0.53)
        self.at("burning fuel also", lead=0.54)
        self.play(FadeOut(calorimetry), FadeOut(monitor), FadeOut(heat_title), FadeOut(steady), run_time=0.54)
        oxygen = ValueTracker(0.1)
        self.add(oxygen_monitor(oxygen), gas(True, OXYGEN))
        self.play(oxygen.animate.set_value(6.8), run_time=4.75, rate_func=linear)
        self.at("so at steady", lead=0.25)
        self.play(FadeOut(equality), run_time=0.34)
        self.add(heat_monitor(heat))
        self.play(oxygen.animate.set_value(9.9), heat.animate.set_value(0.72), run_time=2.72, rate_func=linear)
        self.at("reveal metabolic rate", lead=0.32)
        bracket = VGroup(Line(p(0.1, 2.19), p(0.1, -1.78), color=GOLD, stroke_width=4),
                         Line(p(0.1, 2.19), p(0.44, 2.19), color=GOLD, stroke_width=4),
                         Line(p(0.1, -1.78), p(0.44, -1.78), color=GOLD, stroke_width=4))
        rule = label("Metabolic rate", RIGHT_X, -2.80, GOLD, 38)
        self.play(Create(bracket), FadeIn(rule), run_time=0.56)
        self.finish()


class S05Predict(SpokenScene):
    def construct(self):
        glass, animal, branch, bubble, zero = prediction_parts(dimmed=False)
        ratio = ValueTracker(0.36)
        oxygen, meter, unknown, tag = prediction_meter(ratio)
        self.add(glass, animal, oxygen, tag)
        bob(animal, amp=0.10, speed=2.15)
        self.at("carbon dioxide adds", lead=0)
        self.play(FadeIn(meter), ratio.animate.set_value(0.5), run_time=1.7)
        self.at("one pathway tests", lead=0.2)
        self.play(Create(branch[0]), FadeIn(branch[1]), run_time=1.24)
        self.at("pentose phosphate pathway", lead=0.25)
        self.play(FadeIn(branch[2]), run_time=0.56)
        self.at("one step releases", lead=0.12)
        self.play(FadeIn(bubble, shift=RIGHT * 0.38 + DOWN * 0.10), run_time=1.1)
        self.at("without using any", lead=0.12)
        self.play(FadeIn(zero), run_time=0.62)
        self.at("predict does running", lead=0.33)
        self.play(FadeIn(question_card(QUESTION, **QUESTION_STYLE)), FadeIn(unknown), run_time=0.72)
        animal.clear_updaters()
        self.play(animal.animate.move_to(mammal()), glass[0].animate.set_fill(opacity=0.21),
                  run_time=5.04, rate_func=linear)
        self.finish()


class S06Pause(PredictPause):
    QUESTION = QUESTION
    CARD = QUESTION_STYLE
    SECONDS = 4.5

    def construct(self):
        ratio = ValueTracker(0.5)
        glass, *body = prediction_parts()
        self.add(glass, *body, *prediction_meter(ratio), question_card(self.QUESTION, **self.CARD))
        self.play(ratio.animate.set_value(0.53), glass[0].animate.set_fill(opacity=0.245),
                  rate_func=there_and_back, run_time=self.SECONDS)


class S07RevealLimit(SpokenScene):
    def construct(self):
        glass, animal, branch, bubble, zero = prediction_parts()
        ratio = ValueTracker(0.5)
        oxygen, meter, unknown, tag = prediction_meter(ratio)
        question = question_card(QUESTION, **QUESTION_STYLE)
        self.add(glass, animal, branch, bubble, zero, oxygen, meter, unknown, tag, question)
        bob(animal, amp=0.09, speed=2.1)
        self.at("surprisingly no", lead=0)
        self.play(FadeOut(question), FadeOut(unknown), glass[0].animate.set_fill(opacity=0.32),
                  run_time=1.0)
        self.at("that step also", lead=0.18)
        self.play(FadeOut(zero), FadeOut(bubble), run_time=0.46)
        nadph = chip("NADPH", PURPLE, 31, fill_opacity=0.15).move_to(p(-2.20, 1.06))
        self.at("also makes nadph")
        self.play(FadeIn(nadph, shift=RIGHT * 0.4), run_time=0.7)
        self.at("an electron carrier")
        carrier = caption("NADPH carries electrons", size=32, color=PURPLE)
        self.play(FadeIn(carrier), run_time=0.58)
        self.at("cells later spend", lead=0.22)
        self.play(FadeOut(oxygen), FadeOut(carrier), run_time=0.48)
        junction = p(0.81, 1.06)
        connector = Line(nadph.get_right() + RIGHT * 0.16, junction, color=PURPLE, stroke_width=6)
        self.play(Create(connector), run_time=0.43)
        self.add(flow(connector, PURPLE, count=4, period=2.2))
        destinations = [(junction, p(3.69, 2.33), "O₂-using reactions"),
                        (junction, p(3.69, 1.34), "Making fat")]
        for cue, (start, end, words) in zip(("oxygen using reactions", "or on making fat"), destinations):
            self.at(cue, lead=0.32)
            target = chip(words, PURPLE, 29).move_to(end + RIGHT * 0.61)
            shaft = arrow(start, target.get_left() + LEFT * 0.17, PURPLE, 6)
            self.play(GrowArrow(shaft), FadeIn(target), run_time=0.78)
            self.add(flow(shaft, PURPLE, count=2, period=2.12, radius=0.105))
        self.at("so the pathway alone", lead=0.28)
        baseline = Plot((1.48, 5.48, -2.67, -2.13), (0, 1), (0, 1), stroke=0)
        steady = label("Ratio holds steady", RIGHT_X - 0.25, -2.95, GREEN, 31)
        self.at("does not raise", lead=0.25)
        self.play(FadeIn(steady), run_time=0.48)
        self.at("carbon dioxide to", lead=0.24)
        self.play(Create(baseline.curve(lambda _: 0.5, color=GREEN, width=9)), run_time=2.9,
                  rate_func=linear)
        self.at("to measure that pathway", lead=0.28)
        right_objects = [m for m in self.mobjects if m not in (glass, animal, branch, tag)]
        self.play(*(FadeOut(item) for item in right_objects), run_time=0.50)
        glucose = Circle(radius=1.11, fill_color=PURPLE, fill_opacity=0.38,
                         stroke_color=PURPLE, stroke_width=5).move_to(p(RIGHT_X, -0.15))
        self.play(GrowFromCenter(glucose), run_time=1.05)
        sugar_name = label("Glucose", RIGHT_X, -1.83, PURPLE, 34)
        self.play(FadeIn(sugar_name), run_time=0.50)
        self.at("use tracers that", lead=0.20)
        marker = Dot(p(2.62, 0.67), radius=0.2, color=GOLD)
        tracer = label("C1 tracer", 2.57, 1.48, GOLD, 32)
        self.play(GrowFromCenter(marker), FadeIn(tracer), run_time=0.58)
        self.at("first carbon")
        released = chip("CO₂", CARBON, 29).move_to(p(5.94, 0.67))
        exit_path = arrow(p(4.27, 0.67), released.get_left() + LEFT * 0.14, GOLD)
        self.play(GrowArrow(exit_path), marker.animate.move_to(p(4.70, 1.08)),
                  tracer.animate.move_to(p(4.70, 1.68)), run_time=0.65)
        self.play(FadeIn(released), run_time=0.35)
        self.finish()


class S08Controls(SpokenScene):
    def construct(self):
        animal = mammal()
        glass = vessel()
        self.add(glass, animal, heat_ripples(), scope_tag(size=26))
        bob(animal, amp=0.10, speed=2)
        self.at("chambers need controls", lead=0)
        self.play(FadeIn(heading("Chamber controls", GREEN)), run_time=0.63)
        temp_plot = Plot((0.79, 6.2, -1.74, 2.27), (0, 8), (0, 1), xlabel="Time",
                         ylabel="Body temperature", color=TEXT, label_size=30)
        clock = ValueTracker(0.07)

        def temperature(t):
            return 0.62 + 0.3 * max(0, 1 - t / 3.6) ** 2

        self.at("wait for steady", lead=0.42)
        curve = temp_plot.live_curve(temperature, clock, color=GREEN, width=8)
        dot = temp_plot.dot(clock.get_value, lambda: temperature(clock.get_value()), color=GREEN, ring=GREEN)
        self.add(temp_plot, curve, dot)
        self.play(clock.animate.set_value(4.65), run_time=3.17, rate_func=linear)
        self.at("hold constant", lead=0.17)
        steady = caption("Steady state", size=35, color=GREEN)
        self.play(FadeIn(steady), clock.animate.set_value(8), run_time=2.54, rate_func=linear)
        self.at("second hold air", lead=0.45)
        self.play(FadeOut(VGroup(temp_plot, curve, dot, steady)), run_time=0.44)
        wall, air = ValueTracker(0.88), ValueTracker(0.52)
        temps = VGroup(thermometer(2.18, 0.59, wall, HEAT, height=2.36),
                       thermometer(4.55, 0.59, air, BLUE, height=2.36))
        names = VGroup(label("Wall", 2.18, -1.04, HEAT), label("Air", 4.55, -1.04, BLUE))
        self.add(temps)
        self.play(FadeIn(names), wall.animate.set_value(0.52), run_time=2.16)
        self.at("so dry heat leaks", lead=0.25)
        same = label("Same Ta", RIGHT_X, -1.90, GREEN, 36)
        dry = arrow(p(-3.65, 0.40), p(-0.70, 1.68), HEAT, 7)
        self.play(GrowArrow(dry), FadeIn(same), run_time=1.0)
        self.add(flow(dry, HEAT, count=4, period=2.15))
        self.finish()


class S09UnlockedCycle(SpokenScene):
    def construct(self):
        large = vessel()
        animal = mammal()
        self.add(large, animal)
        self.at("oxygen records unlocked", lead=0)
        self.play(Transform(large, sample_vessel()), FadeOut(animal), run_time=1.2)
        small = sample_vessel()
        self.remove(large)
        self.add(small)
        dish, muscle, gauge = sample_dish(), sample_muscle(), manometer()
        plot = sample_plot()
        t = ValueTracker(0.1)
        self.play(FadeIn(dish), FadeIn(muscle), Create(gauge), FadeIn(plot), run_time=1.66)
        self.add(sample_trace(plot, cycle_oxygen, t), scope_tag(size=26))
        self.at("then krebs measured", lead=1.5)
        names = heading("Szent-Györgyi & Krebs", GOLD)
        self.play(FadeIn(names), t.animate.set_value(1.04), run_time=1.15, rate_func=linear)
        self.at("oxygen use in", lead=0.16)
        muscle_name = label("Minced pigeon muscle", LEFT_X, -2.75, TEXT, 28)
        self.play(FadeIn(muscle_name), t.animate.set_value(3.2), run_time=3.35, rate_func=linear)
        self.at("a pinch of", lead=0.22)
        pinch = Dot(p(LEFT_X - 0.98, 1.04), color=ORANGE, radius=0.16)
        acid = label("Four-carbon acid", LEFT_X, 2.55, ORANGE, 30)
        self.add(pinch)
        self.play(FadeIn(acid), pinch.animate.move_to(p(LEFT_X - 0.98, -0.51)), run_time=1.25)
        self.at("made the muscle", lead=0.12)
        self.play(t.animate.set_value(6.8), run_time=2.65, rate_func=linear)
        self.at("than oxidizing it", lead=0.22)
        reference = DashedVMobject(plot.curve(fuel_only_oxygen, x0=3.2, color=ORANGE, width=5),
                                   num_dashes=16)
        ref_label = label("Added acid as fuel", 4.42, 1.64, ORANGE, 29)
        self.play(Create(reference), t.animate.set_value(8.15), run_time=1.05, rate_func=linear)
        self.play(FadeIn(ref_label), t.animate.set_value(9.08), run_time=1.3, rate_func=linear)
        self.at("the acid was", lead=0.20)
        self.play(FadeOut(acid), t.animate.set_value(10), run_time=1.98, rate_func=linear)
        self.at("it was reused", lead=0.22)
        loop = CurvedArrow(p(-3.77, 0.21), p(-4.57, -0.13), angle=-PI * 1.56,
                           color=ORANGE, stroke_width=8)
        self.play(Create(loop), FadeOut(pinch), run_time=0.9)
        self.add(flow(loop, ORANGE, count=4, period=1.8, radius=0.13))
        self.at("revealing the citric", lead=0.18)
        self.play(swap(muscle_name, label("Citric acid cycle", LEFT_X, -2.75, GOLD, 32), 0.8))
        self.finish()


class S10UnlockedMito(SpokenScene):
    def construct(self):
        dish, sample = sample_dish(), mito_sample()
        electrode = probe()
        electrode_start = electrode.copy().shift(UP * 0.26)
        plot = sample_plot()
        t = ValueTracker(0.09)
        glass = sample_vessel()
        self.add(glass, dish, sample, plot, electrode_start,
                 sample_trace(plot, mito_oxygen, t), scope_tag(size=26))
        self.at("an oxygen electrode", lead=0)
        self.play(Transform(electrode_start, electrode), t.animate.set_value(0.77), run_time=1.42)
        self.at("tracks the oxygen")
        x_label = label("Isolated mitochondria", LEFT_X, -2.75, TEXT, 29)
        self.play(t.animate.set_value(1.44), run_time=1.75, rate_func=linear)
        self.at("around isolated", lead=0.22)
        self.play(FadeIn(x_label), t.animate.set_value(2.8), run_time=3.35, rate_func=linear)
        self.at("adding a dp", lead=0.18)
        added = chip("ADP", ORANGE, 30).move_to(p(-4.78, 0.83))
        self.play(FadeIn(added, shift=DOWN * 0.39), run_time=0.63)
        self.at("steepen the slow", lead=0.22)
        self.play(t.animate.set_value(5.2), run_time=2.33, rate_func=linear)
        self.at("state 3", lead=0.18)
        state3 = label("State 3", 4.07, 0.86, OXYGEN, 31)
        self.play(FadeIn(state3), t.animate.set_value(5.84), run_time=1.38, rate_func=linear)
        self.at("once the adp", lead=0.15)
        atp = chip("ATP", GREEN, 30).move_to(added)
        self.play(swap(added, atp, 1.70), t.animate.set_value(6.6), run_time=1.70, rate_func=linear)
        self.at("it flattened state", lead=0.18)
        self.play(t.animate.set_value(8.13), run_time=0.9, rate_func=linear)
        self.at("state 4", lead=0.22)
        state4 = label("State 4", 5.39, -0.46, OXYGEN, 31)
        self.play(FadeIn(state4), t.animate.set_value(9.3), run_time=1.4, rate_func=linear)
        self.at("the respiratory chain", lead=0.59)
        chain, synthase = machinery()
        self.play(FadeOut(VGroup(dish, sample, x_label, electrode_start, atp)),
                  Transform(glass, vessel()), run_time=0.52)
        chain_feed = arrow(p(-4.89, 1.55), p(-4.89, 0.86), OXYGEN)
        self.play(FadeIn(chain), GrowArrow(chain_feed), t.animate.set_value(10), run_time=1.16)
        self.add(flow(chain_feed, OXYGEN, count=3, period=1.25, radius=0.093))
        self.play(FadeIn(label("O₂", -4.89, 1.84, OXYGEN, 31)),
                  glass[0].animate.set_fill(opacity=0.25), run_time=0.88)
        self.at("but never touches", lead=0.16)
        self.play(glass[0].animate.set_fill(opacity=0.15), run_time=1.26, rate_func=linear)
        self.at("tp synthase does", lead=0.82)
        adp_feed = arrow(p(-2.02, 1.55), p(-2.02, 0.86), ORANGE)
        self.play(FadeIn(synthase), GrowArrow(adp_feed),
                  glass[0].animate.set_fill(opacity=0.24), run_time=0.84)
        self.add(flow(adp_feed, ORANGE, count=3, period=1.25, radius=0.093))
        self.play(FadeIn(label("ADP", -2.02, 1.84, ORANGE, 31)),
                  glass[0].animate.set_fill(opacity=0.32), run_time=1.04)
        self.finish()


class S11Return(SpokenScene):
    def construct(self):
        chain, synthase = machinery()
        plot = sample_plot()
        leftover = VGroup(plot, sample_trace(plot, mito_oxygen, ValueTracker(10)),
                          label("State 3", 4.07, 0.86, OXYGEN, 31),
                          label("State 4", 5.39, -0.46, OXYGEN, 31),
                          label("O₂", -4.89, 1.84, OXYGEN, 31), label("ADP", -2.02, 1.84, ORANGE, 31),
                          arrow(p(-4.89, 1.55), p(-4.89, 0.86), OXYGEN),
                          arrow(p(-2.02, 1.55), p(-2.02, 0.86), ORANGE))
        closeup = vessel()
        self.add(closeup, chain, synthase, leftover, scope_tag(size=26))
        self.at("in 1961", lead=0)
        self.play(FadeOut(leftover), run_time=0.98)
        # Short rails end outside the blocks; the proteins span the membrane.
        membrane = VGroup(*(Line(p(a, y), p(b, y), color=GREY, stroke_width=5)
                            for a, b in [(-6.28, -6.15), (-3.59, -3.17), (-0.86, -0.52)]
                            for y in (-0.14, 0.38)))
        self.play(Create(membrane), run_time=0.68)
        self.at("mitchell proposed that", lead=0.29)
        proposed = label("Mitchell 1961 (proposed)", RIGHT_X, 1.08, GOLD, 33)
        self.play(FadeIn(proposed), run_time=0.67)
        self.at("a proton gradient", lead=0.24)
        proton_path = CubicBezier(p(-4.89, 0.83), p(-4.7, 1.51), p(-3.1, 1.54), p(-2.02, 0.82))
        proton_path.set_stroke(TEAL, width=7)
        up = arrow(p(-4.89, -1.35), p(-4.89, -0.58), TEAL)
        down = arrow(p(-2.02, 0.92), p(-2.02, 0.83), TEAL, tip=0.10)
        out = arrow(p(-2.02, -0.57), p(-2.02, -1.35), TEAL)
        proton_text = label("H⁺ gradient", LEFT_X, 1.79, TEAL, 30)
        self.play(Create(proton_path), GrowArrow(up), GrowArrow(out), FadeIn(down), run_time=0.75)
        self.play(FadeIn(proton_text), run_time=0.39)
        proton_flow = flow(proton_path, TEAL, count=5, period=1.75)
        self.add(proton_flow)
        self.at("from whole mammals", lead=0.62)
        self.play(FadeOut(VGroup(membrane, chain, synthase, up, down, out, proton_text, proton_path,
                                 proton_flow, proposed)), run_time=0.33)
        animal = mammal()
        self.play(FadeIn(animal), run_time=0.33)
        self.at("to isolated mitochondria", lead=0)
        sample = VGroup(sample_dish(), mito_sample())
        self.play(FadeOut(animal), run_time=0.13)
        self.play(Transform(closeup, sample_vessel()), FadeIn(sample), run_time=0.40)
        self.at("measure what crosses", lead=0.20)
        unknown = label("?", LEFT_X - 0.15, -0.46, GOLD, 72)
        self.play(FadeOut(sample), run_time=0.13)
        self.play(Transform(closeup, vessel()), FadeIn(animal), FadeIn(unknown), run_time=0.40)
        bob(animal, amp=0.11, speed=2.15)
        self.add(gas(True, OXYGEN), heat_ripples())
        oxygen, heat = ValueTracker(0.8), ValueTracker(0.35)
        self.add(oxygen_monitor(oxygen), heat_monitor(heat, title="Heat balance"))
        self.play(oxygen.animate.set_value(6.3), heat.animate.set_value(0.62), run_time=2.27, rate_func=linear)
        self.at("hidden metabolism comes", lead=0.25)
        revealed = label("Metabolic rate", RIGHT_X, -2.82, GOLD, 33)
        core = Circle(radius=0.37, stroke_color=GOLD, stroke_width=4,
                      fill_color=BG, fill_opacity=0.96).move_to(unknown)
        pointer = Line(core.get_center(), core.get_center() + p(0.17, 0.17), color=GOLD, stroke_width=5)
        self.play(swap(unknown, VGroup(core, pointer), 0.78), FadeIn(revealed),
                  oxygen.animate.set_value(8.9), heat.animate.set_value(0.71), run_time=1.93, rate_func=linear)
        self.finish()


class S12End(EndCard):
    LINE = "At steady state, oxygen used and heat lost reveal metabolic rate."
