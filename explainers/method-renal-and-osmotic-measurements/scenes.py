"""Measuring filtration, clearance, and osmolality.

Colour map from the patch-clamp film: blue for instruments, grey for
structure, purple for a selective barrier, yellow for the measured quantity,
green for the inulin reference, red for a limitation, orange for added
solute, teal for filtrate/water, and gold for questions and dates.
"""

from bp_parts import *
from bp_style import EndCard, SpokenScene, TitleCard
from layout_check import Checker

PURPLE = "#B58CD9"
ORANGE = "#F29E4C"
CORTEX = "#664452"
MEDULLA = "#38314B"
LUMEN = "#204B60"
BENCH = "#1B2334"
REF = 30 * 2.0 / 0.50
UNKNOWN = 300
REABSORBED = 1
QUESTION = "300 mL/min vs 120: Reabsorbed or secreted?"
END_LINE = "Tubule samples, clearance, and freezing point measure\nfiltration, transport, and osmolality."


def p(x, y):
    return np.array([x, y, 0.0])


def words(text, x, y, color=TEXT, size=30, width=5.7):
    return fit_text(text, max_w=width, size=size, min_size=28,
                    color=color, max_lines=3).move_to(p(x, y))


def path(points, color, width, fill=None):
    curve = VMobject(stroke_color=color, stroke_width=width)
    curve.set_points_smoothly([p(x, y) for x, y in points])
    if fill:
        curve.set_fill(fill, opacity=1)
    return curve


def arrow(start, end, color=GREY):
    return Arrow(p(*start), p(*end), buff=0, color=color, stroke_width=5,
                 tip_length=0.16, max_tip_length_to_length_ratio=0.28)


def transit(track, color=TEAL, count=22, speed=0.25, radius=0.145):
    """Move filtrate through the open lumen, with no off-path exits."""
    stream = VGroup()
    gleam = interpolate_color(ManimColor(color), ManimColor(TEXT), 0.35)
    # Resample the Beziers by distance so particles don't pile up at the bends.
    sample = np.array([track.point_from_proportion(t) for t in np.linspace(0, 1, 181)])
    distance = np.r_[0, np.cumsum(np.linalg.norm(np.diff(sample, axis=0), axis=1))]
    fractions = distance / distance[-1]
    for i in range(count):
        dot = Dot(radius=radius * (0.76 + 0.35 * (i % 3) / 2), color=gleam)
        dot.phase = (i + 0.18 * (i % 3)) / count
        dot.travel = speed * (0.91 + 0.07 * (i % 3))

        def flow(mob, dt):
            mob.phase = (mob.phase + dt * mob.travel) % 1
            mob.move_to([np.interp(mob.phase, fractions, sample[:, axis]) for axis in range(3)])
            mob.set_opacity(min(1, mob.phase * 25, (1 - mob.phase) * 25))

        dot.add_updater(flow)
        flow(dot, 0)
        stream.add(dot)
    return stream


def tubule_segment(track, landmark, upstream):
    """Keep a copy of the route on one side of a transport site."""
    samples = np.linspace(0, 1, 201)
    split = min(samples, key=lambda t: np.linalg.norm(track.point_from_proportion(t) - landmark))
    start, end = (0, split) if upstream else (split, 1)
    return track.copy().pointwise_become_partial(track, start, end)


def kidney():
    """The same cortex, medulla, glomerulus and tubule in each carried shot."""
    cortex = path(
        [(-2.1, 2.65), (-4.35, 2.77), (-5.92, 1.72), (-6.32, -0.15),
         (-5.57, -1.87), (-3.71, -2.50), (-1.75, -1.98), (-0.79, -0.9),
         (-1.25, 0.09), (-0.82, 1.1), (-1.15, 2.15), (-2.1, 2.65)],
        "#995B67", 3, CORTEX,
    )
    medulla = path(
        [(-2.53, 1.34), (-3.96, 1.56), (-5.32, 0.84), (-5.37, -0.72),
         (-4.28, -1.85), (-2.91, -1.84), (-1.51, -0.88), (-1.30, -0.04),
         (-1.76, 0.74), (-2.53, 1.34)],
        "#795F90", 3, MEDULLA,
    )
    course = [
        (-4.86, 1.40), (-4.28, 1.07), (-3.90, 1.51), (-3.37, 1.46),
        (-3.60, 0.83), (-3.37, -0.58), (-3.17, -1.47), (-2.71, -1.52),
        (-2.47, -0.70), (-2.40, 0.57), (-2.12, 1.01), (-1.78, 0.67),
        (-1.93, 0.13), (-1.70, -0.23), (-1.38, -1.44), (-1.30, -1.81),
    ]
    route = path(course, TEAL, 4)
    wall = route.copy().set_stroke("#97BAC9", width=38)
    lumen = route.copy().set_stroke(LUMEN, width=32)
    cup = Circle(radius=0.53, stroke_color=BLUE, stroke_width=4,
                 fill_color=LUMEN, fill_opacity=1).move_to(p(-4.90, 1.57))
    tuft = path(
        [(-5.17, 1.56), (-5.05, 1.81), (-4.79, 1.72), (-4.79, 1.46),
         (-5.05, 1.42), (-5.08, 1.62), (-4.89, 1.67), (-4.84, 1.52)],
        RED, 7,
    )
    vessel = path([(-6.02, 1.31), (-5.69, 1.50), (-5.43, 1.78), (-5.13, 1.74)], RED, 10)
    return VGroup(cortex, medulla), VGroup(wall, lumen, cup, vessel, tuft), route


def bench():
    return RoundedRectangle(width=6.81, height=5.43, corner_radius=0.25,
                            stroke_width=0, fill_color=BENCH, fill_opacity=1).move_to(p(3.23, 0.04))


def set_world(scene, color=TEAL, flowing=True):
    organ, nephron, route = kidney()
    stream = transit(route, color) if flowing else VGroup()
    scene.add(bench(), organ, nephron, stream, scope_tag(size=28, color=TEXT))
    return stream, route


def pipette(tip, length=1.45):
    x, y = tip
    return Polygon(p(x - 0.035, y), p(x + 0.035, y), p(x + 0.19, y + length),
                   p(x - 0.19, y + length), stroke_color=BLUE, stroke_width=3,
                   fill_color=BLUE, fill_opacity=0.28)


def vial(x, y, color, width=0.73, height=1.13):
    body = RoundedRectangle(width=width, height=height, corner_radius=0.13,
                            stroke_color=BLUE, stroke_width=3, fill_color=LUMEN,
                            fill_opacity=0.72).move_to(p(x, y))
    liquid = RoundedRectangle(width=width - 0.14, height=height * 0.42, corner_radius=0.10,
                              stroke_width=0, fill_color=color, fill_opacity=0.8)
    liquid.move_to(p(x, y - height * 0.21))
    rim = Line(p(x - width * 0.60, y + height / 2), p(x + width * 0.60, y + height / 2),
               color=BLUE, stroke_width=4)
    return VGroup(body, liquid, rim)


def sample_drop(x, y, scale=1):
    return path(
        [(0, 0.68), (-0.30, 0.17), (-0.42, -0.06), (-0.31, -0.33),
         (0, -0.45), (0.31, -0.33), (0.42, -0.06), (0.30, 0.17), (0, 0.68)],
        BLUE, 3, LUMEN,
    ).scale(scale).move_to(p(x, y))


def stage_icon(x, y, scale=1):
    base = RoundedRectangle(width=1.83, height=0.24, corner_radius=0.10, stroke_width=0,
                            fill_color=BLUE, fill_opacity=0.85).move_to(p(x, y - 0.58))
    well = vial(x - 0.26, y, TEAL, 0.83, 0.89)
    probe = Line(p(x + 0.42, y + 0.68), p(x + 0.42, y - 0.34), color=BLUE, stroke_width=6)
    return VGroup(base, well, probe).scale(scale, about_point=p(x, y))


def equation(u="U", v="V", divisor="P"):
    top = M(f"{u} × {v}", 31, YELLOW).move_to(p(2.15, 0.95))
    rule = Line(p(1.54, 0.51), p(3.67, 0.51), stroke_width=3, color=TEXT)
    bottom = M(divisor, 31, ORANGE).move_to(p(2.15, 0.05))
    name = M("C =", 31).move_to(p(0.87, 0.54))
    return name, top, rule, bottom


def gauge(value, color=GREEN, reference=False):
    """One fixed, linear clearance scale for the worked example and comparisons."""
    x, base, height = 5.34, -1.82, 3.68
    track = RoundedRectangle(width=1.05, height=height, corner_radius=0.13,
                             stroke_color=GREY, stroke_width=2, fill_color=BG,
                             fill_opacity=0.70).move_to(p(x, base + height / 2))
    ceiling = 320

    def fill(bar):
        h = height * np.clip(value.get_value(), 0, ceiling) / ceiling
        # A stroke-free rectangle keeps the 1 mL/min case to scale.
        bar.stretch_to_fit_height(max(h, 0.002)).move_to(p(x, base + h / 2))
        bar.set_fill(color, opacity=0.85 if h else 0)

    bar = Rectangle(width=0.87, height=1, stroke_width=0, fill_color=color)
    bar.add_updater(fill)
    fill(bar)
    y = base + height * REF / ceiling
    mark = DashedLine(p(4.5, y), p(6.21, y), dash_length=0.09,
                      color=GREEN, stroke_width=3)
    return VGroup(track, bar, mark) if reference else VGroup(track, bar)


def question():
    return question_card(QUESTION, y=-3.15, size=32, max_w=10.55).question


def choices():
    return arrow((-4.39, -0.26), (-3.60, -0.26), ORANGE), arrow((-3.60, -0.85), (-4.39, -0.85), TEAL)


class S01Hook(SpokenScene, TitleCard):
    TITLE = "Measuring Filtration, Clearance, and Osmolality"
    LESSON = "Renal and Osmotic Measurements"

    def construct(self):
        organ, nephron, route = kidney()
        self.add(organ, bench())
        tiny = nephron.copy().scale(0.46, about_point=p(-4.45, 1.38))
        self.add(tiny)
        q = T("?", 92, GOLD).move_to(p(-4.65, -0.25))
        self.at("how do you measure")
        self.play(FadeIn(q), run_time=0.42)
        self.at("hidden nephron")
        self.play(Transform(tiny, nephron), q.animate.move_to(p(-4.65, -0.16)), run_time=1.85)
        self.add(transit(route))
        bob(q, amp=0.075, speed=3)
        self.at("three measurements")
        q.clear_updaters()
        title = words(self.TITLE.replace(" and ", "\nand "), 3.22, 1.90, size=37, width=5.9)
        self.play(FadeOut(q), FadeIn(title), run_time=0.55)
        tools = [pipette((1.12, -1.64), 1.52).rotate(-0.45),
                 VGroup(vial(2.78, -0.83, RED, width=0.64),
                        vial(3.74, -0.83, YELLOW, width=0.64)),
                 stage_icon(5.40, -0.80)]
        self.add(*[tool.set_opacity(0.28) for tool in tools])
        name = words("Micropuncture", 3.23, -1.98, BLUE, 32)
        self.at("micropuncture")
        self.play(tools[0].animate.set_opacity(1), FadeIn(name), run_time=0.45)
        self.at("clearance")
        clearance = words("Clearance", 3.23, -1.98, YELLOW, 32)
        self.play(tools[1].animate.set_opacity(1), swap(name, clearance, 0.55))
        self.at("freezing point osmometry")
        self.play(tools[2].animate.set_opacity(1),
                  swap(clearance, words("Freezing-point osmometry", 3.23, -1.98, BLUE, 32), 0.55))
        self.add(scope_tag(size=28, color=TEXT))
        self.finish()


class S02Micropuncture(SpokenScene):
    def construct(self):
        set_world(self)
        glass = pipette((1.12, -1.64), 1.52).rotate(-0.45)
        self.add(glass, words("Micropuncture", 3.23, 2.13, BLUE, 35))
        self.at("under a microscope")
        target = pipette((-4.94, 1.95), 1.31)
        self.play(Transform(glass, target, path_arc=-0.33), run_time=1.7)
        self.at("draws a tiny drop")
        drop = Dot(p(-4.93, 1.88), radius=0.135, color=BLUE)
        self.add(drop)
        self.play(drop.animate.move_to(p(-4.94, 2.72)), run_time=0.93)
        self.at("bowman's capsule")
        capsule = words("Bowman’s capsule", -2.82, 3.27, BLUE, 31)
        self.play(FadeIn(capsule), run_time=0.52)
        specimen = sample_drop(1.69, 0.04, 1.48)
        urine = vial(4.78, 0.04, YELLOW, 1.05, 1.60)
        self.at("cup around")
        self.play(ReplacementTransform(drop, specimen), FadeIn(urine),
                  glass.animate.shift(UP * 0.32 + LEFT * 0.15), run_time=1.36)
        self.add(words("Capsular fluid", 1.69, -1.30, BLUE),
                 words("Bladder urine", 4.78, -1.30, YELLOW))
        self.at("a solute there")
        solute = Dot(p(1.69, -0.02), radius=0.14, color=ORANGE)
        vanished = Dot(p(4.78, -0.02), radius=0.14, color=ORANGE, fill_opacity=0.45)
        self.play(GrowFromCenter(solute), FadeIn(vanished), run_time=0.48)
        self.at("missing from bladder")
        self.play(FadeOut(vanished, scale=0.1), run_time=0.86)
        self.finish()


class S03Clearance(SpokenScene):
    def construct(self):
        stream, route = set_world(self)
        glass = pipette((-5.09, 2.27), 1.31)
        self.add(glass)
        self.at("without a pipette")
        self.play(Transform(glass, pipette((1.05, 0.79), 1.31).rotate(-0.7), path_arc=0.46),
                  run_time=1.25)
        self.at("blood and urine")
        plasma = vial(2.95, 1.69, RED, 0.54, 0.76)
        urine = vial(3.93, 1.69, YELLOW, 0.54, 0.76)
        collecting = vial(-1.28, -2.31, YELLOW, 0.57, 0.72)
        drips = transit(Line(p(-1.30, -1.89), p(-1.28, -2.44)), YELLOW, count=2, radius=0.07)
        self.play(FadeOut(glass), FadeIn(plasma), FadeIn(urine), FadeIn(collecting), run_time=0.62)
        self.add(drips)
        self.at("clearance equals")
        heading = words("Clearance", 2.15, 2.25, YELLOW, 35)
        self.play(FadeIn(heading), FadeOut(plasma), FadeOut(urine), run_time=0.48)
        sign, _, rule, divisor = equation()
        u = M("U", 31, YELLOW).move_to(p(1.62, 0.95))
        times = M("× V", 31, YELLOW).move_to(p(2.42, 0.95))
        self.at("urine concentration")
        self.play(FadeIn(sign), FadeIn(u), run_time=0.43)
        meaning = words("Urine concentration", 2.17, -0.82, YELLOW, 28, 3.7)
        self.add(meaning)
        self.at("times urine flow")
        flow_label = words("Urine flow", 2.17, -0.82, YELLOW)
        self.play(FadeIn(times, run_time=0.55), swap(meaning, flow_label, 0.55))
        self.at("divided by plasma")
        meaning = words("Plasma concentration", 2.17, -0.82, ORANGE, 28, 3.7)
        self.play(Create(rule), FadeIn(divisor), swap(flow_label, meaning, 0.65))
        self.at("no plasma is wiped")
        self.play(FadeOut(meaning), run_time=0.36)
        self.at("plasma volume holding")
        equiv = words("Plasma volume equivalent\nto one minute’s excretion", 2.32, -1.30, TEXT, 28, 4.0)
        self.play(FadeIn(equiv, shift=UP * 0.1), run_time=0.75)
        self.at("inulin is freely")
        inulin = transit(route, GREEN)
        self.play(FadeOut(equiv), FadeOut(stream), FadeIn(inulin), run_time=0.8)
        self.at("neither reabsorbed")
        inulin_name = words("Inulin", -4.49, -0.73, GREEN, 33)
        self.play(FadeIn(inulin_name), run_time=0.55)
        self.at("glomerular filtration rate")
        value = ValueTracker(0)
        scale = gauge(value)
        gfr = words("GFR", 5.34, 2.26, GREEN, 33)
        self.play(FadeIn(scale), FadeIn(gfr), run_time=0.66)
        self.at("the plasma filtered")
        definition = words("Plasma filtered\nper minute", 2.18, -1.30, GREEN, 30)
        self.play(FadeIn(definition), run_time=0.65)
        self.finish()


class S04WorkedMath(SpokenScene):
    def construct(self):
        set_world(self, GREEN)
        number = ValueTracker(0)
        scale = gauge(number)
        sign, top, rule, bottom = equation()
        self.add(scale, sign, top, rule, bottom, words("GFR", 5.34, 2.26, GREEN, 33))
        self.at("illustrative adult")
        self.play(FadeIn(words("Illustrative adult\nhuman values", 2.40, 2.25, GOLD, 28, 4.65)), run_time=0.56)
        self.at("30 mg")
        numeric = M("30 × V", 31, YELLOW).move_to(top)
        unit = words("U = 30 mg/mL", 2.15, -0.83, YELLOW, 30)
        self.play(swap(top, numeric, 0.62), FadeIn(unit))
        self.at("2 milliliters")
        product = M("30 × 2.0", 31, YELLOW).move_to(top)
        flow = words("V = 2.0 mL/min", 2.15, -1.62, YELLOW, 30)
        self.play(swap(numeric, product, 0.57), FadeIn(flow, run_time=0.57))
        self.at("0 .5 mg")
        denominator = M("0.50", 31, ORANGE).move_to(bottom)
        concentration = words("P = 0.50 mg/mL", 2.15, -2.19, ORANGE, 28)
        self.play(swap(bottom, denominator, 0.60), FadeIn(concentration, run_time=0.60))
        self.at("30 times 2")
        self.play(FadeOut(unit), FadeOut(flow), FadeOut(concentration), run_time=0.76)
        self.at("is 60")
        result = M("60 mg/min", 31, YELLOW).move_to(product)
        self.play(swap(product, result, 0.62))
        self.at("60 divided by")
        self.play(swap(denominator, M("0.50 mg/mL", 30, ORANGE).move_to(bottom), 0.58))
        self.at("gives 120")
        answer = Readout([("GFR", lambda: REF, "{:.0f} mL/min", GREEN)],
                         at=p(2.19, -1.32), size=29)
        self.play(number.animate.set_value(REF), FadeIn(answer), run_time=0.60)
        self.finish()


def comparison(value, color=YELLOW):
    meter = gauge(value, color, reference=True)
    reference = words("GFR reference\n120 mL/min", 2.13, 0.66, GREEN, 31)
    return VGroup(meter, reference)


def prediction_arrows():
    inward, outward = choices()
    return VGroup(inward, outward, T("?", 32, ORANGE).move_to(p(-4.68, -0.26)),
                  T("?", 32, TEAL).move_to(p(-4.68, -0.85)))


class S05Predict(SpokenScene):
    def construct(self):
        filtrate, route = set_world(self, GREEN)
        amount = ValueTracker(0)
        self.add(comparison(amount))
        self.at("now predict")
        self.play(FadeIn(words("Freely filtered solute", 3.43, 2.19, YELLOW, 32)), run_time=0.6)
        self.at("a clearance of 300")
        solute = transit(route, YELLOW)
        result = words("300 mL/min", 2.13, 1.45, YELLOW, 32)
        self.play(amount.animate.set_value(UNKNOWN), FadeOut(filtrate), FadeIn(solute), FadeIn(result), run_time=0.75)
        self.at("did the tubule")
        self.play(FadeIn(prediction_arrows()), FadeIn(question()), run_time=0.66)
        self.finish()


class S06Pause(Scene):
    def construct(self):
        self.camera.background_color = BG
        _, route = set_world(self, GREEN, flowing=False)
        stream = transit(route, YELLOW)
        stream.clear_updaters(recursive=True)
        self.add(stream, comparison(ValueTracker(UNKNOWN)), prediction_arrows(), question(),
                 words("Freely filtered solute", 3.43, 2.19, YELLOW, 32),
                 words("300 mL/min", 2.13, 1.45, YELLOW, 32))
        checker = Checker(self)
        checker.sample()
        self.wait(4.5)
        checker.sample()
        checker.flush()


def station():
    """Same freezing-point instrument before and after the tonicity comparison."""
    base = RoundedRectangle(width=4.40, height=0.26, corner_radius=0.10, stroke_width=0,
                            fill_color=BLUE, fill_opacity=0.62).move_to(p(3.29, -1.95))
    bath = RoundedRectangle(width=2.08, height=2.71, corner_radius=0.20,
                            stroke_color=BLUE, stroke_width=4, fill_color=LUMEN,
                            fill_opacity=1).move_to(p(1.62, -0.42))
    thermometer = RoundedRectangle(width=0.36, height=2.44, corner_radius=0.16,
                                   color=BLUE, stroke_width=3).move_to(p(3.45, -0.50))
    bulb = Dot(p(3.45, -1.65), radius=0.23, color=BLUE)
    readout = RoundedRectangle(width=0.65, height=2.10, corner_radius=0.14, color=GREY,
                               stroke_width=3).move_to(p(5.19, -0.41))
    return VGroup(base, bath, thermometer, bulb, readout)


def stage_columns(salinity):
    cold = Line(p(3.45, -1.60), p(3.45, 0.52), color=BLUE, stroke_width=8)
    osmol = Rectangle(width=0.43, height=0.42, stroke_width=0, fill_color=YELLOW, fill_opacity=0.9)

    def temperature(m):
        m.put_start_and_end_on(p(3.45, -1.6), p(3.45, 0.50 - 1.35 * salinity.get_value()))

    def dissolved(m):
        h = 0.38 + 1.41 * salinity.get_value()
        m.stretch_to_fit_height(h).move_to(p(5.19, -1.35 + h / 2))

    cold.add_updater(temperature)
    osmol.add_updater(dissolved)
    temperature(cold)
    dissolved(osmol)
    return VGroup(cold, osmol)


class S07Answer(SpokenScene):
    def construct(self):
        stream, route = set_world(self, YELLOW)
        amount = ValueTracker(UNKNOWN)
        chart = comparison(amount)
        heading = words("Freely filtered solute", 3.43, 2.19, YELLOW, 32)
        high = words("300 mL/min", 2.13, 1.45, YELLOW, 32)
        self.add(chart, heading, high)
        inward, outward = choices()
        self.at("the tubule secreted")
        answer = question_card("Net secretion", color=ORANGE, y=-3.15, size=34).question
        self.play(GrowArrow(inward), FadeIn(answer), run_time=0.65)
        self.at("more leaves in urine")
        incoming = transit(Line(p(-4.58, -0.26), p(-3.48, -0.26)), ORANGE, count=4, speed=0.6)
        self.add(incoming)
        self.at("cells added extra")
        downstream = tubule_segment(route, p(-3.43, -0.26), upstream=False)
        more = transit(downstream, ORANGE, count=8, speed=0.33, radius=0.10)
        self.play(FadeIn(more), run_time=0.58)
        self.at("at one milliliter")
        low = words("1 mL/min", 2.13, 1.45, YELLOW, 32)
        self.play(amount.animate.set_value(REABSORBED), swap(high, low, 0.90),
                  FadeOut(incoming), FadeOut(more), FadeOut(inward), FadeOut(answer), run_time=1.15)
        self.at("most was reabsorbed")
        before_site = tubule_segment(route, p(-3.33, -0.85), upstream=True)
        after_site = tubule_segment(route, p(-3.33, -0.85), upstream=False)
        filtered = transit(before_site, YELLOW, count=10, speed=0.54)
        retained = transit(Line(p(-3.32, -0.85), p(-4.68, -0.85)), YELLOW, count=5, speed=0.7)
        urine_trace = transit(after_site, YELLOW, count=1, speed=0.36)
        remaining_solute = VGroup(filtered, retained, urine_trace)
        reabsorb = question_card("Net reabsorption", color=TEAL, y=-3.15, size=34).question
        self.play(FadeOut(stream), FadeIn(remaining_solute), GrowArrow(outward),
                  FadeIn(reabsorb), run_time=0.72)
        self.at("next how do we")
        stage = station()
        fluid = transit(route)
        self.play(FadeOut(chart), FadeOut(heading), FadeOut(low), FadeOut(outward),
                  FadeOut(remaining_solute), FadeOut(reabsorb), FadeIn(fluid), run_time=0.48)
        self.play(FadeIn(stage), FadeIn(stage_columns(ValueTracker(0))), run_time=0.90)
        self.finish()


class S08Osmometry(SpokenScene):
    def construct(self):
        set_world(self)
        amount = ValueTracker(0)
        apparatus = station()
        self.add(apparatus, stage_columns(amount))
        title = words("Osmolality", 3.20, 2.24, YELLOW, 36)
        self.at("osmolality counts")
        self.play(FadeIn(title), run_time=0.42)
        self.at("dissolved particles")
        meaning = words("Dissolved particles per kg of water", 3.23, 1.49, TEXT, 28, 6.4)
        self.play(FadeIn(meaning), run_time=0.59)
        salt = words("Sodium\nchloride", 1.62, 0.21, ORANGE, 28, 1.74)
        pair = VGroup(Dot(p(1.39, -0.52), radius=0.15, color=ORANGE),
                      Dot(p(1.96, -0.25), radius=0.15, color=ORANGE))
        self.at("sodium chloride")
        self.play(FadeIn(salt), run_time=0.4)
        self.at("makes two ions")
        self.play(ReplacementTransform(salt, pair), run_time=0.73)
        self.at("urea stays one")
        urea = words("Urea", 1.58, 0.54, PURPLE, 28)
        self.play(FadeIn(urea), run_time=0.34)
        urea_dot = Dot(p(1.51, -1.07), radius=0.15, color=PURPLE)
        self.play(ReplacementTransform(urea, urea_dot), run_time=0.67)
        self.at("extra particles lower")
        extra = VGroup(*[Dot(p(x, y), radius=0.12, color=ORANGE)
                         for x, y in [(1.0, -0.07), (1.12, -0.86), (2.24, -0.91), (2.07, -1.29)]])
        self.play(FadeIn(extra), amount.animate.set_value(1), run_time=2.42)
        self.at("freezing point osmometry")
        temp = words("Freezing\npoint", 3.48, 1.45, BLUE, 28)
        osm = words("Osmolality", 5.42, 1.45, YELLOW, 28)
        self.play(FadeOut(meaning), run_time=0.42)
        self.play(FadeIn(temp), FadeIn(osm), run_time=0.64)
        self.at("where a sample freezes")
        ice = Polygon(p(0.80, -0.09), p(2.44, -0.09), p(2.44, -1.56), p(0.80, -1.56),
                      stroke_width=0, fill_color=BLUE, fill_opacity=0.23)
        self.play(FadeIn(ice), run_time=0.7)
        self.finish()


class S09Limits(SpokenScene):
    def construct(self):
        set_world(self, GREEN)
        amount = ValueTracker(REF)
        chart = comparison(amount)
        name = words("Creatinine clearance", 3.24, 2.22, YELLOW, 34)
        self.add(chart, name)
        self.at("slightly secreted")
        tiny = arrow((-4.17, -0.25), (-3.60, -0.25), ORANGE)
        self.play(GrowArrow(tiny), run_time=0.68)
        self.at("tends to overestimate")
        bias = words("Tends to overestimate GFR", 2.05, -1.15, RED, 28, 3.72)
        # Qualitative offset only. The script provides no creatinine clearance value.
        self.play(amount.animate.set_value(REF * 1.12), FadeIn(bias), run_time=1.27)
        self.at("osmosis follows")
        self.play(FadeOut(chart), FadeOut(name), FadeOut(tiny), FadeOut(bias), run_time=0.47)
        heading = words("Effective osmolality", 3.27, 2.22, YELLOW, 35)
        well = RoundedRectangle(width=4.46, height=2.45, corner_radius=0.17, stroke_width=0,
                                fill_color=LUMEN, fill_opacity=1).move_to(p(2.83, -0.35))
        wall = Line(p(2.75, -1.57), p(2.75, 0.87), color=PURPLE, stroke_width=6)
        salt = VGroup(*[Dot(p(x, y), radius=0.13, color=ORANGE)
                       for x, y in [(1.17, 0.14), (1.66, -0.30), (1.09, -0.87), (2.17, -0.97)]])
        probe = Line(p(5.56, -1.10), p(5.56, 0.72), color=BLUE, stroke_width=7)
        bulb = Dot(p(5.56, -1.16), radius=0.23, color=BLUE)
        self.play(FadeIn(well), Create(wall), FadeIn(heading), run_time=1.12)
        self.at("cannot cross a membrane")
        salt_label = words("Salt stays outside", 1.76, 1.44, ORANGE, 28, 2.8)
        self.play(FadeIn(salt), FadeIn(salt_label), run_time=0.60)
        self.at("freezing point also counts")
        urea = VGroup(Dot(p(1.30, 0.54), radius=0.14, color=PURPLE),
                      Dot(p(1.65, -0.64), radius=0.14, color=PURPLE),
                      Dot(p(1.48, -1.20), radius=0.14, color=PURPLE))
        self.play(GrowFromCenter(probe), FadeIn(bulb), FadeIn(urea), run_time=0.70)
        self.at("crosses cell membranes")
        self.play(urea.animate.shift(RIGHT * 2.34),
                  FadeIn(words("Urea crosses", 4.01, 1.44, PURPLE, 28)), run_time=2.16)
        self.at("draws little water")
        self.play(FadeIn(words("Freezing point counts both", 3.21, -2.12, BLUE, 30)), run_time=0.75)
        self.finish()


def frog_panel():
    frame = RoundedRectangle(width=6.07, height=2.33, corner_radius=0.15, stroke_width=0,
                             fill_color="#282B41", fill_opacity=1).move_to(p(3.27, 1.31))
    date = words("Wearn & Richards, 1924", 3.26, 2.13, GOLD, 30)
    drop = sample_drop(0.88, 1.22, 0.63)
    urine = vial(5.50, 1.22, YELLOW, 0.52, 0.77)
    return frame, date, drop, urine


def slices():
    return VGroup(*[
        RoundedRectangle(width=2.07 - i * 0.24, height=0.21, corner_radius=0.09,
                         stroke_color=interpolate_color(ManimColor(TEAL), ManimColor(PURPLE), i / 4),
                         stroke_width=2.5,
                         fill_color=interpolate_color(ManimColor("#85C5C9"), ManimColor("#473158"), i / 4),
                         fill_opacity=1).move_to(p(2.60, 0.29 - 0.41 * i))
        for i in range(5)
    ])


class S10UnlockedKidney(SpokenScene):
    def construct(self):
        set_world(self)
        self.at("these methods unlocked")
        self.play(FadeIn(words("What the methods revealed", -3.17, 3.51, size=32)), run_time=0.72)
        frame, date, drop, urine = frog_panel()
        self.at("in 1924")
        self.play(FadeIn(frame), FadeIn(date), run_time=1.12)
        self.at("micropunctured a frog")
        needle = pipette((-4.88, 1.88), 1.17)
        self.play(FadeIn(needle, shift=DOWN * 0.26), FadeIn(drop), run_time=1.0)
        self.at("capsular fluid held")
        self.play(GrowFromCenter(Dot(drop.get_center() + p(-0.02, 0.05), radius=0.08, color=ORANGE)),
                  GrowFromCenter(Dot(drop.get_center() + p(0.09, -0.11), radius=0.08, color=TEAL)),
                  FadeIn(words("Sugar + chloride", 2.75, 1.46, TEXT, 28)), run_time=0.75)
        self.at("no protein found")
        self.play(FadeIn(words("No protein detected", 3.08, 0.98, TEXT, 28)), run_time=0.59)
        self.at("bladder urine held")
        self.play(FadeIn(urine), FadeIn(words("No sugar", 5.37, 0.45, YELLOW, 28)), run_time=0.75)
        self.at("filter followed by reabsorption")
        conclusion = words("Frog: filter, then reabsorb", 3.23, -0.24, GOLD, 31)
        self.play(FadeOut(needle), FadeIn(conclusion), run_time=0.86)
        self.at("in 1951")
        self.play(FadeOut(conclusion), run_time=0.35)
        second = words("Wirz, Hargitay & Kuhn, 1951", 3.28, -0.17, GOLD, 29)
        self.play(FadeIn(second), run_time=0.80)
        self.at("freezing points of rat")
        stack = slices().shift(DOWN * 0.89)
        self.play(LaggedStart(*[FadeIn(layer, shift=DOWN * 0.18) for layer in stack], lag_ratio=0.44),
                  run_time=2.59)
        self.at("osmolality climbed")
        rising = arrow((4.08, -0.70), (4.08, -2.33), YELLOW)
        scale_text = words("Osmolality\nincreases", 5.32, -1.48, YELLOW, 28, 2.02)
        self.play(GrowArrow(rising), FadeIn(scale_text), run_time=1.12)
        self.at("cortex down to")
        self.play(FadeIn(words("Cortex", 0.87, -0.62, TEXT, 28)), run_time=0.45)
        self.at("papilla")
        self.play(FadeIn(words("Papilla", 1.13, -2.25, TEXT, 28)), run_time=0.49)
        self.at("countercurrent multiplier")
        loop = path([(5.06, -0.81), (5.06, -1.86), (5.20, -2.21), (5.58, -2.21),
                     (5.72, -1.86), (5.72, -0.81)], TEAL, 10)
        self.play(FadeOut(scale_text), run_time=0.40)
        self.play(Create(loop), run_time=1.30)
        self.at("opposite flows")
        self.play(GrowArrow(arrow((4.74, -0.93), (4.74, -1.65), GOLD)),
                  GrowArrow(arrow((6.04, -1.65), (6.04, -0.93), GOLD)), run_time=0.91)
        self.finish()


# Figure 2c and 2e, Zimmerman et al. (2016), doi:10.1038/nature18950.
# These are relative schematic levels, with timing anchors from the paper
# and the supplied narration. Interpolation is used only for the continuous
# neural recording. The two blood samples are separate measured time points.
NEURON_TIMES = [-1, 0, 1]
NEURON_LEVELS = [0.83, 0.83, 0.21]


class S11UnlockedThirst(SpokenScene):
    def construct(self):
        set_world(self)
        heading = words("Zimmerman, Knight et al., 2016", 3.18, 2.42, GOLD, 31, 6)
        self.at("in 2016")
        self.play(FadeIn(heading), run_time=1.15)
        self.at("water restricted mice")
        species = words("Water-restricted mice", 3.25, 1.88, TEXT, 28)
        self.play(FadeIn(species), run_time=0.64)
        neurons = Plot(box=(1.02, 6.03, 0.30, 1.21), xr=(-1, 5), yr=(0, 1),
                       color=GREY, stroke=2.6)
        plasma = Plot(box=(1.02, 6.03, -1.96, -0.77), xr=(-1, 5), yr=(0, 1),
                      xticks=[(-1, "−1"), (0, "0"), (1, "1"), (5, "5 min")],
                      size=28, color=GREY, stroke=2.6)
        access_x = neurons.pt(0, 0)[0]
        water = DashedLine(p(access_x, -1.89), p(access_x, 1.24), dash_length=0.075,
                           color=BLUE, stroke_width=3)
        nlabel = words("Thirst-neuron activity", 4.04, 1.43, TEAL, 28)
        self.at("thirst neurons quieted")
        now = ValueTracker(-1)
        curve = neurons.live_curve(lambda t: np.interp(t, NEURON_TIMES, NEURON_LEVELS), now,
                                   color=TEAL, width=7)
        self.add(neurons, curve, water)
        water_label = words("Water access", 3.14, -0.02, BLUE, 28)
        self.play(FadeIn(nlabel), now.animate.set_value(0), run_time=1.05)
        self.play(FadeIn(water_label), run_time=0.45)
        self.at("within one minute")
        self.play(now.animate.set_value(1), run_time=1.25, rate_func=linear)
        self.at("yet plasma osmolality")
        title = words("Plasma osmolality", 4.09, -0.42, YELLOW, 28)
        before = Dot(plasma.pt(-1, 0.64), radius=0.105, color=YELLOW)
        after = Dot(plasma.pt(5, 0.64), radius=0.105, color=YELLOW)
        self.play(FadeIn(plasma), FadeIn(title), GrowFromCenter(before), run_time=1.05)
        self.at("freezing point osmometry")
        method = words("Freezing-point measurement", 3.42, -2.94, BLUE, 28)
        self.play(FadeIn(method), run_time=0.75)
        self.at("stayed raised five")
        self.play(GrowFromCenter(after), run_time=1.11)
        self.at("water going in")
        self.play(FadeOut(method), run_time=0.45)
        self.at("blood was sampled")
        gap = BraceBetweenPoints(p(1.19, -1.38), p(5.88, -1.38), direction=DOWN, color=GOLD, buff=0.08)
        self.play(GrowFromCenter(gap), run_time=0.88)
        self.at("small early change")
        self.play(FadeIn(words("A small early change could be missed", 1.25, -3.16, GOLD, 28, 7.6)),
                  run_time=0.70)
        self.finish()


class S12End(EndCard):
    LINE = END_LINE
