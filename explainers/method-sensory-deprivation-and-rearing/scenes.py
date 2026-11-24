"""An eyes-to-cortex schematic for the sensory deprivation film.

Color map: yellow = opposite-side eye, teal = same-side eye, blue = recording
apparatus, grey = anatomy and scales, green = controls, gold = age and dates.
"""
from bp_parts import *
from bp_style import EndCard

C_EYE, I_EYE = YELLOW, TEAL
CORTEX = "#39475D"
EYES = ((-4.97, 1.92), (-4.97, -1.74))
NEURON = np.array([-1.02, 0.09, 0])
PANEL_X = 3.64


def p(x, y):
    return np.array([x, y, 0.0])


def label(text, x, y, size=32, color=TEXT):
    return T(text, size, color).move_to(p(x, y))


def box(width, height, center, color, opacity=0.24, radius=0.2, stroke=2):
    return RoundedRectangle(width=width, height=height, corner_radius=radius,
                            fill_color=color, fill_opacity=opacity, stroke_color=color,
                            stroke_width=stroke).move_to(center)


def lid_parts(center, color, closure, sutures):
    """Frontal eye icon whose aperture narrows around its horizontal midline."""
    aperture = 1 - 0.93 * closure
    rim = Ellipse(width=2.85, height=1.56, color=GREY, stroke_width=3,
                  fill_color=CORTEX, fill_opacity=1).move_to(center)
    opening = Ellipse(width=2.65, height=1.39 * aperture, color=color, stroke_width=2.8,
                      fill_color=color, fill_opacity=0.25).move_to(center)
    iris = Ellipse(width=0.93, height=1.04 * aperture, color=color, stroke_width=0,
                   fill_color=color, fill_opacity=0.92).move_to(center)
    pupil = Ellipse(width=0.38, height=0.62 * aperture, stroke_width=0,
                    fill_color=BG, fill_opacity=1).move_to(center)
    tie = VGroup()
    if sutures and closure > 0.75:
        for x in (-0.55, 0, 0.55):
            a = center + p(x - 0.07, 0.13)
            b = center + p(x + 0.07, -0.13)
            tie.add(Line(a, b, color=TEXT, stroke_width=2.6))
            tie.add(Dot(a, radius=0.029, color=TEXT))
    return VGroup(rim, opening, iris, pupil, tie)


def signal_path(start, end, color, clock, strength, phase):
    """Move signal packets down the same tract at a rate set by its input."""
    path = CubicBezier(start, start + RIGHT * 0.72, end + LEFT * 0.78, end)
    path.set_stroke(color, 16, opacity=0.24)
    pulse = Ellipse(width=0.63, height=0.30, fill_color=color,
                    stroke_width=0, fill_opacity=1)
    def move(m):
        s = strength()
        fraction = (clock.get_value() * 0.78 + phase) % 1
        a = path.point_from_proportion(max(0, fraction - 0.02))
        b = path.point_from_proportion(min(1, fraction + 0.02))
        direction = b - a
        angle = np.arctan2(direction[1], direction[0])
        m.rotate(angle - m.heading)
        m.heading = angle
        m.move_to(path.point_from_proportion(fraction))
        envelope = np.sin(np.pi * fraction) ** 0.42
        m.set_opacity((0.08 + 0.92 * s) * envelope)
    pulse.heading = 0
    pulse.add_updater(move, call_updater=True)
    return VGroup(path, pulse)


def recording_probe():
    tip = NEURON + p(0.13, 0.21)
    stem = Line(tip, tip + p(0.67, 1.08), color=BLUE, stroke_width=5)
    handle = Line(tip + p(0.43, 0.70), tip + p(0.67, 1.08), color=BLUE, stroke_width=12)
    return VGroup(stem, handle)


def world(closed=(0, 0), rates=(1.0, 0.58), probe=True, moving=True, sutures=True):
    """Build the same eyes, retina–LGN relays, and cortical sheet at fixed landmarks."""
    clock = ValueTracker(0)
    lids = [ValueTracker(c) for c in closed]
    outputs = [ValueTracker(r) for r in rates]
    sheet = box(2.57, 4.79, p(-1.05, 0.09), CORTEX, opacity=1, radius=0.55, stroke=0)
    tissue = VGroup(sheet)
    for x in (-1.88, -1.33, -0.77, -0.22):
        fold = CubicBezier(p(x, -1.93), p(x - 0.32, -0.55), p(x + 0.36, 0.73), p(x, 2.11))
        tissue.add(fold.set_stroke(GREY, 2.4, opacity=0.35))
    for row, y in enumerate(np.linspace(-1.70, 1.88, 9)):
        for col, x in enumerate(np.linspace(-1.94, -0.18, 5)):
            if abs(y - NEURON[1]) < 0.27 and abs(x - NEURON[0]) < 0.29:
                continue
            tissue.add(Dot(p(x + 0.07 * np.sin(row + col), y), radius=0.043,
                           color=TEXT, fill_opacity=0.46, stroke_width=0))

    tracks, icons, relays = VGroup(), VGroup(), VGroup()
    for i, (xy, color) in enumerate(zip(EYES, (C_EYE, I_EYE))):
        eye = p(*xy)
        relay = p(-2.98, 0.97 if i == 0 else -0.87)
        eye_strength = lambda i=i: ([1.0, 0.58][i] * (1 - 0.82 * lids[i].get_value()))
        cortex_strength = lambda i=i: outputs[i].get_value()
        tracks.add(signal_path(eye + RIGHT * 1.28, relay, color, clock, eye_strength, i * 0.12))
        tracks.add(signal_path(relay, NEURON + LEFT * 0.15, color, clock, cortex_strength, i * 0.12 + 0.45))
        relays.add(Circle(radius=0.17, color=color, stroke_width=2.6,
                          fill_color=BG, fill_opacity=1).move_to(relay))
        icons.add(always_redraw(lambda eye=eye, color=color, i=i:
                                lid_parts(eye, color, lids[i].get_value(), sutures)))

    active = Dot(NEURON, radius=0.144, color=TEXT)
    response_glow = Ellipse(width=1.98, height=3.65, color=BLUE, stroke_width=0,
                            fill_color=BLUE, fill_opacity=0.10).move_to(NEURON)
    halo = Circle(radius=0.31, color=BLUE, stroke_width=3).move_to(NEURON)
    if moving:
        def response(m):
            # The cortical response follows the incoming pulses; the tissue stays fixed.
            t = clock.get_value()
            responses = [output.get_value() * (0.5 + 0.5 * np.sin(TAU * (0.78 * t + offset))) ** 2
                         for output, offset in zip(outputs, (0.20, 0.32))]
            strength = max(responses)
            m.set(width=1.12 + 0.90 * strength)
            m.set_fill(opacity=0.04 + 0.94 * strength)
        response_glow.add_updater(response, call_updater=True)
    pipette = recording_probe()
    picture = VGroup(tissue, response_glow, tracks, relays, icons, halo, active)
    if moving:
        picture.add_updater(lambda m, dt: clock.increment_value(dt))
    if probe:
        picture.add(pipette)
    picture.lids, picture.outputs, picture.probe = lids, outputs, pipette
    return picture


def cortex_label():
    return label("Visual cortex", -1.04, -2.67, 30)


def side_labels():
    return VGroup(label("Contralateral", -4.98, 3.03, 31, C_EYE),
                  label("Ipsilateral", -4.98, -2.91, 31, I_EYE))


def index_of(c, i):
    return (c - i) / (c + i) if c + i else 0


def dominance_gauge(value):
    """Horizontal index with a marker positioned from the same value as the readout."""
    rail = Plot(box=(1.38, 5.91, -1.44, -1.44), xr=(-1, 1), yr=(0, 1),
                xticks=[(-1, "−1"), (0, "0"), (1, "+1")], size=30)
    marker = Triangle(color=BLUE, fill_color=BLUE, fill_opacity=1,
                      stroke_width=0).scale(0.15).rotate(PI)
    def move(m):
        m.move_to(rail.pt(value(), 0) + UP * 0.28)
    marker.add_updater(move, call_updater=True)
    return VGroup(rail, marker)


def rate_bars(c, i, numbers=True):
    """The illustrative spike rates and the heights of their bars share trackers."""
    bars = VGroup()
    for tracker, color, x, key in [(c, C_EYE, 2.84, "C"), (i, I_EYE, 4.42, "I")]:
        base = 0.02
        height = 1.24
        track = box(0.64, height, p(x, base + height / 2), color, opacity=0.17, radius=0.07)
        def fill(tracker=tracker, color=color, x=x):
            h = max(0.003, (height - 0.09) * tracker.get_value() / 30)
            return Rectangle(width=0.49, height=h, fill_color=color, fill_opacity=1,
                             stroke_width=0).move_to(p(x, base + 0.045 + h / 2))
        bars.add(track, always_redraw(fill))
        bars.add(label(key, x, -0.23, 28, color))
        if numbers:
            bars.add(counter("{:.0f}", tracker, p(x, 1.61), size=30, color=color))
    return bars


def age_axis(age, xlabel="Postnatal day", with_outcome=False, xticks=None):
    """Shared ruler for the age of the test, with room above it for an outcome curve."""
    if xticks is None:
        xticks = [(19, "P19"), (28, "P28"), (32, "P32")]
    axis = Plot(box=(1.14, 6.17, -2.42, 1.3 if with_outcome else -2.42),
                xr=(15, 36), yr=(0, 1), xticks=xticks,
                xlabel=xlabel, size=28, label_size=28)
    axis.xlabel.shift(LEFT * 0.45)
    cursor = Triangle(stroke_width=0, fill_color=GOLD, fill_opacity=1).scale(0.13).rotate(PI)
    cursor.add_updater(lambda m: m.move_to(axis.pt(age.get_value(), 0) + UP * 0.27),
                       call_updater=True)
    return axis, cursor


QUESTION = "Both eyes shut: Disuse vs. Competition?"
OPTIONS = ("Disuse: ?", "Competition: ?")
CARD = {"y": -3.2, "size": 32, "chip_size": 29, "chips_at": p(PANEL_X, -0.95)}


def prediction_card():
    return question_card(QUESTION, OPTIONS, **CARD)


def activity_badge(number, top, eye=None):
    text = str(number) if eye is None else f"{eye}  {number}"
    return chip(text, C_EYE if top else I_EYE, 33).move_to(
        p(-4.97, 3.25 if top else -3.10))


def model_label():
    return label("Illustrative model, not measured", PANEL_X, 2.73, 28, GOLD)


def percent_line(numerator, denominator):
    exact = 100 * numerator / denominator
    comparison = "=" if exact.is_integer() else "≈"
    return f"{numerator} ÷ {denominator} {comparison} {exact:.0f}%"


class S01Hook(SpokenScene, TitleCard):
    LESSON = "Sensory Deprivation and Controlled Rearing"
    TITLE = "Closing One Eye to Map a Critical Period"

    def construct(self):
        picture = world(probe=False, sutures=False)
        self.add(picture)
        q = question_card("When does experience wire the brain?", y=3.31, size=35)
        self.at("How do you")
        self.play(FadeIn(q), run_time=0.65)
        self.at("Close one eye", lead=0.45)
        self.play(FadeOut(q), picture.lids[0].animate.set_value(1),
                  picture.outputs[0].animate.set_value(0.25), run_time=1.15)
        self.at("listen to cortex", lead=0.25)
        self.play(FadeIn(picture.probe, shift=UP * 0.55), run_time=0.70)
        self.at("Sensory deprivation")
        self.play(FadeIn(cortex_label()), run_time=0.6)
        self.finish()


class S02Title(TitleCard):
    LESSON = "Sensory Deprivation and Controlled Rearing"
    TITLE = "Closing One Eye to Map a Critical Period"

    def construct(self):
        self.add(world(closed=(1, 0), rates=(0.25, 0.58), sutures=False), cortex_label())
        title = VGroup(T("Closing One Eye", 46, TEXT, font=TITLE_FONT),
                       T("to Map a Critical Period", 35, TEXT, font=TITLE_FONT))
        title.arrange(DOWN, buff=0.28).move_to(p(PANEL_X, 0.96))
        self.play(FadeIn(title), run_time=0.27)
        self.wait(1.20)
        self.play(FadeOut(title), run_time=0.33)


class S03Baseline(SpokenScene):
    def construct(self):
        picture = world(closed=(1, 0), rates=(0.25, 0.58), sutures=False)
        self.add(picture, cortex_label())
        self.at("Start in primary", lead=0)
        self.play(picture.lids[0].animate.set_value(0), picture.outputs[0].animate.set_value(0.58),
                  run_time=1.2)
        self.at("In its binocular zone", lead=0.95)
        zone = RoundedRectangle(width=1.77, height=1.53, corner_radius=0.33,
                                color=BLUE, stroke_width=4).move_to(NEURON)
        self.play(Create(zone), run_time=0.67)
        self.play(FadeIn(label("Binocular zone", 2.45, 0.08, 32, BLUE)), run_time=0.48)
        c_label, i_label = side_labels()
        c_side = label("Opposite side", 3.05, 1.92, 33, C_EYE)
        i_side = label("Same side", 3.05, -1.66, 33, I_EYE)
        self.at("Contralateral means")
        self.play(FadeIn(c_label), FadeIn(c_side), run_time=0.64)
        self.at("ipsilateral means")
        self.play(FadeIn(i_label), FadeIn(i_side), run_time=0.64)
        self.at("Most mouse cells")
        self.play(picture.outputs[0].animate.set_value(1), run_time=2.3)
        self.finish()


class S04Index(SpokenScene):
    def construct(self):
        picture = world()
        self.add(picture, side_labels(), cortex_label())
        c, i = ValueTracker(0), ValueTracker(0)
        read_value = lambda: index_of(c.get_value(), i.get_value())
        gauge = dominance_gauge(read_value)
        marker = gauge[1]
        heading = label("Ocular dominance index", PANEL_X, 2.72, 33)
        formula = M("(C − I) ÷ (C + I)", 33).move_to(p(PANEL_X, 2.16))
        self.at("Score preference")
        self.play(FadeIn(gauge[0]), FadeIn(heading), run_time=0.63)
        self.at("contralateral minus")
        self.play(FadeIn(formula), run_time=0.67)
        self.at("An illustrative cell")
        self.play(FadeIn(scope_tag("Illustrative example", size=28, color=GOLD)),
                  FadeIn(label("Spikes per second", PANEL_X, -0.66, 29)), run_time=0.58)
        bars = rate_bars(c, i)
        self.add(bars)
        self.at("30 spikes", lead=1.02)
        self.play(c.animate.set_value(30), run_time=0.80)
        self.at("10 to ipsilateral", lead=0.95)
        self.play(i.animate.set_value(10), run_time=0.75)
        values = M("(30 − 10) ÷ (30 + 10)", 31).move_to(formula)
        numerator = M("20 ÷ (30 + 10)", 33).move_to(formula)
        fraction = M("20 ÷ 40", 33).move_to(formula)
        result = M("20 ÷ 40 = 0.50", 33, BLUE).move_to(formula)
        self.play(swap(formula, values, 0.61))
        self.at("is 20")
        self.play(swap(values, numerator, 0.66))
        self.at("is 40")
        self.play(swap(numerator, fraction, 0.66))
        self.at("is 0 .50", lead=0.28)
        self.play(swap(fraction, result, 0.72), FadeIn(marker, shift=LEFT * 0.75), run_time=0.82)
        self.at("Plus 1 is")
        self.play(FadeIn(label("C only", 5.91, -2.48, 28, C_EYE)), run_time=0.57)
        self.at("minus 1 ipsilateral")
        self.play(FadeIn(label("I only", 1.38, -2.48, 28, I_EYE)), run_time=0.57)
        self.finish()


class S05Deprive(SpokenScene):
    def construct(self):
        picture = world()
        c, i = ValueTracker(30), ValueTracker(10)
        index = lambda: index_of(c.get_value(), i.get_value())
        gauge = dominance_gauge(index)
        self.add(picture, side_labels(), cortex_label(), gauge, rate_bars(c, i, numbers=False),
                 label("Ocular dominance index", PANEL_X, 2.72, 33),
                 scope_tag("Schematic", size=28, color=GOLD))
        self.at("Now suture", lead=0)
        self.play(picture.lids[0].animate.set_value(1), run_time=1.75)
        self.at("diffuse light")
        self.play(picture.outputs[0].animate.set_value(0.70), run_time=1.25)
        heading = label("Monocular deprivation", PANEL_X, 1.97, 31)
        self.at("This is monocular")
        self.play(FadeIn(heading), run_time=0.64)
        day = ValueTracker(28)
        axis, cursor = age_axis(day, xticks=[(28, "P28"), (32, "P32")])
        self.at("At postnatal day")
        self.play(FadeIn(axis), FadeIn(cursor), run_time=0.63)
        self.at("about four days")
        self.play(day.animate.set_value(32), c.animate.set_value(12),
                  picture.outputs[0].animate.set_value(0.35), run_time=3.45)
        self.at("The index drops")
        self.play(c.animate.set_value(6), picture.outputs[0].animate.set_value(0.14), run_time=2.2)
        self.at("favoring the open eye")
        self.play(FadeIn(label("Favors open eye", PANEL_X, 1.65, 30, I_EYE)),
                  FadeOut(heading), run_time=0.63)
        self.at("Change input")
        self.finish()


class S06PredictQ(SpokenScene):
    def construct(self):
        picture = world(closed=(1, 0), rates=(0.14, 0.58))
        self.add(picture, cortex_label())
        q = prediction_card()
        self.at("simple disuse")
        self.play(FadeIn(q.chips[0]), run_time=0.60)
        self.at("competition between eyes")
        self.play(FadeIn(q.chips[1]), run_time=0.60)
        self.at("In an illustrative model")
        self.play(FadeIn(model_label()), run_time=0.58)
        open_eye, closed_eye = activity_badge(10, False), activity_badge(1, True)
        self.at("an open eye ten")
        self.play(FadeIn(open_eye), run_time=0.55)
        self.at("a sutured eye one")
        self.play(FadeIn(closed_eye), run_time=0.55)
        self.at("close both eyes", lead=0.42)
        self.play(picture.lids[1].animate.set_value(1), picture.outputs[1].animate.set_value(0.14),
                  swap(open_eye, activity_badge(1, False), 0.93), run_time=0.97)
        self.at("what does each")
        self.play(FadeIn(q.question), run_time=0.58)
        self.finish()


class S07PredictPause(Scene):
    def construct(self):
        self.camera.background_color = BG
        static = world(closed=(1, 1), rates=(0.14, 0.14), moving=False)
        self.add(static, cortex_label(), model_label(), activity_badge(1, True),
                 activity_badge(1, False), prediction_card())
        track = Line(p(-4.65, -3.63), p(4.65, -3.63), color=GREY, stroke_width=4)
        bar = Line(track.get_start(), track.get_end(), color=GOLD, stroke_width=6)
        self.add(track)
        self.play(Create(bar), run_time=4.5, rate_func=linear)


def activity_units(kept, total, y, height=0.24):
    """Equal tiles make the numerator and denominator visible without a fitted scale."""
    step = 4.18 / total
    left = PANEL_X - 2.09
    return VGroup(*[
        Rectangle(width=step - 0.045, height=height, stroke_width=0,
                  fill_color=C_EYE if j < kept else GREY,
                  fill_opacity=1 if j < kept else 0.63).move_to(p(left + (j + 0.5) * step, y))
        for j in range(total)
    ])


def prediction_rows():
    headings = VGroup(label("Disuse", PANEL_X, 1.85, 33),
                      label("Competition", PANEL_X, 0.25, 33))
    disuse = label(percent_line(1, 10) + " either way", PANEL_X, 1.27, 32)
    formula = M("B ÷ (A + B)", 33).move_to(p(PANEL_X, -0.32))
    one = label("One shut   " + percent_line(1, 11), PANEL_X, -0.99, 30)
    both = label("Both shut   " + percent_line(1, 2), PANEL_X, -1.60, 30, GREEN)
    return headings, disuse, formula, one, both


class S08ControlsCompetition(SpokenScene):
    def construct(self):
        picture = world(closed=(1, 1), rates=(0.14, 0.14))
        top, bottom = activity_badge(1, True), activity_badge(1, False)
        q = prediction_card()
        self.add(picture, cortex_label(), model_label(), top, bottom, q)
        headings, disuse, formula, one, both = prediction_rows()
        self.at("Under disuse", lead=0)
        self.play(FadeOut(q), FadeIn(headings[0]), run_time=0.60)
        quotient = M("1 ÷ 10", 33).move_to(disuse)
        self.at("one of ten units")
        self.play(FadeIn(quotient), run_time=0.58)
        self.at("ten percent either")
        disuse_units = activity_units(1, 10, 0.78)
        self.play(swap(quotient, disuse, 0.65),
                  LaggedStart(*[GrowFromCenter(unit) for unit in disuse_units], lag_ratio=0.18),
                  run_time=1.55)
        self.at("Under competition")
        self.play(FadeIn(headings[1]), run_time=0.61)
        both_a, b = activity_badge(1, False, "A"), activity_badge(1, True, "B")
        self.at("its activity divided")
        self.play(FadeIn(formula), swap(bottom, both_a, 0.68), swap(top, b, 0.68), run_time=0.68)
        open_a = activity_badge(10, False, "A")
        self.at("With one eye closed")
        self.play(picture.lids[1].animate.set_value(0), picture.outputs[1].animate.set_value(0.58),
                  swap(both_a, open_a, 0.88), run_time=0.88)
        self.at("one divided by eleven")
        self.play(FadeIn(one), GrowFromCenter(activity_units(1, 11, -2.35, height=0.34)),
                  run_time=0.84)
        self.at("With both closed")
        self.play(picture.lids[1].animate.set_value(1), picture.outputs[1].animate.set_value(0.14),
                  swap(open_a, both_a, 0.91), run_time=0.91)
        self.at("one divided by two")
        self.play(FadeIn(both), GrowFromCenter(activity_units(1, 2, -2.96, height=0.34)),
                  run_time=0.85)
        self.finish()


def relay_callouts():
    retina = Circle(radius=0.16, color=GREEN, stroke_width=3,
                    fill_color=GREEN, fill_opacity=0.55).move_to(p(-3.7, 1.92))
    lgn = Circle(radius=0.24, color=GREEN, stroke_width=3,
                 fill_color=GREEN, fill_opacity=0.46).move_to(p(-2.98, 0.97))
    return retina, lgn


class S09ControlsLimits(SpokenScene):
    def construct(self):
        picture = world(closed=(1, 0), rates=(0.14, 0.58))
        self.add(picture, cortex_label())
        ret, lgn = relay_callouts()
        retina_name = place_label(T("Retina", 28, GREEN), ret, dirs=(UP,), buff=0.66)
        relay_name = label("LGN:\nrelay to cortex", -4.75, 0.14, 28, GREEN)
        self.at("closed eyes retina", lead=0.54)
        self.play(FadeIn(ret), run_time=0.32)
        self.play(FadeIn(retina_name), run_time=0.4)
        self.at("and LGN", lead=0.28)
        self.play(FadeIn(lgn), run_time=0.39)
        self.play(FadeIn(relay_name), run_time=0.53)
        pulse(ret, base=4, amp=2.4)
        pulse(lgn, base=5, amp=2.8)
        age = ValueTracker(19)
        axis, cursor = age_axis(age, xlabel="Age", with_outcome=True)
        # The threshold and linear decline illustrate the definitions, without a numerical y scale.
        critical = lambda age: 0.84 if age < 26 else 0.10
        sensitive = lambda age: np.interp(age, [15, 19, 34, 36], [0.64, 0.64, 0.18, 0.18])
        self.at("Test adults too")
        self.play(FadeOut(retina_name), FadeOut(relay_name), run_time=0.46)
        self.play(FadeIn(axis.axes), FadeIn(axis.xlabel),
                  FadeIn(label("Effect of deprivation", PANEL_X, 2.71, 31)),
                  FadeIn(scope_tag("Schematic", size=28, color=GOLD)), run_time=0.65)
        self.at("sample the whole age curve")
        self.play(FadeIn(cursor), age.animate.set_value(36), run_time=2.45)
        self.play(FadeOut(cursor), run_time=0.35)
        self.at("a critical period", lead=0.70)
        sharp = axis.curve(critical, color=GOLD, width=7)
        self.play(Create(sharp), run_time=1.60, rate_func=linear)
        self.play(FadeIn(label("Critical period", 3.54, 1.28, 31, GOLD)), run_time=0.46)
        self.at("A sensitive period", lead=0.75)
        gradual = axis.curve(sensitive, color=TEAL, width=7)
        self.play(Create(gradual), run_time=2.25, rate_func=linear)
        self.play(FadeIn(label("Sensitive period", 5.32, 0.11, 29, TEAL)), run_time=0.54)
        self.finish()


def stripe_field(balance):
    """Equal-width columns partition a fixed layer into complementary territories."""
    stripes = VGroup()
    start, width, pair_count = 1.20, 4.89, 5
    period = width / pair_count
    for j in range(pair_count):
        x = start + j * period
        for left, fraction, color in [(x, balance, C_EYE),
                                      (x + period * balance, 1 - balance, I_EYE)]:
            dx = fraction * period
            r = Rectangle(width=dx, height=3.33, stroke_width=0,
                          fill_color=color, fill_opacity=0.90)
            stripes.add(r.move_to(p(left + dx / 2, -0.09)))
    return stripes


class S10Unlocked1(SpokenScene):
    def construct(self):
        picture = world(closed=(1, 0), rates=(0.14, 0.58))
        self.add(picture, cortex_label(), scope_tag("Schematic", size=28, color=GOLD))
        byline = label("Wiesel & Hubel, 1963", PANEL_X, 2.78, 31, GOLD)
        kitten = label("Kitten", PANEL_X, 1.97, 35)
        length = label("About three months", PANEL_X, 1.38, 30)
        self.at("In 1963")
        self.play(FadeIn(byline), run_time=0.65)
        self.at("one kitten eye")
        self.play(FadeIn(kitten), run_time=0.60)
        self.at("for about three months")
        self.play(FadeIn(length), run_time=0.55)
        response_labels, response_bars = VGroup(), VGroup()
        # The bars show relative cortical responses without a numerical scale.
        for name, color, y, width in [("Closed eye", C_EYE, 0.87, 0.16),
                                      ("Open eye", I_EYE, 0.35, 2.39)]:
            response_labels.add(label(name, 2.39, y, 28, color))
            response_bars.add(Rectangle(width=width, height=0.22, stroke_width=0,
                                        fill_color=color, fill_opacity=1)
                              .move_to(p(3.51 + width / 2, y)))
        self.at("Very few cortical cells")
        self.play(FadeIn(response_labels), GrowFromEdge(response_bars[0], LEFT),
                  GrowFromEdge(response_bars[1], LEFT), run_time=0.55)
        self.play(picture.outputs[0].animate.set_value(0.01), run_time=2.65)
        self.at("its retina and LGN")
        ret, lgn = relay_callouts()
        self.play(FadeIn(ret), FadeIn(lgn), run_time=0.67)
        pulse(ret, base=4, amp=2.4)
        pulse(lgn, base=5, amp=2.8)
        adult = label("Adult cat", PANEL_X, -0.13, 33)
        adult_gauge = dominance_gauge(lambda: 0.42)
        no_change = label("No shift", PANEL_X, -0.76, 31, GREEN)
        self.at("An adult cat")
        self.play(FadeIn(adult), FadeIn(adult_gauge[0]), run_time=0.60)
        self.at("showed no change", lead=0.42)
        self.play(FadeIn(adult_gauge[1]), FadeIn(no_change), run_time=0.40)
        self.at("In infant macaques", lead=0)
        self.play(*[FadeOut(m) for m in (kitten, length, response_labels, response_bars,
                                       adult, adult_gauge, no_change, ret, lgn)],
                  run_time=0.68)
        macaque_byline = label("Hubel, Wiesel & LeVay", PANEL_X, 2.78, 31, GOLD)
        self.play(swap(byline, macaque_byline, 0.65),
                  FadeIn(label("Infant macaque", PANEL_X, 2.14, 30)), run_time=0.65)
        share = ValueTracker(0.5)
        stripes = always_redraw(lambda: stripe_field(share.get_value()))
        self.at("traced each eye's stripes")
        self.play(FadeIn(stripes), run_time=0.92)
        self.at("layer 4C")
        self.play(FadeIn(label("Layer 4C", PANEL_X, -2.10, 32)), run_time=0.56)
        self.at("Open eye stripes widened")
        self.play(share.animate.set_value(0.27), run_time=2.55)
        self.finish()


# Relative, schematic effect only. Anchors encode the reported low / peak / low
# ordering for P19, P28 and P32 in Gordon & Stryker (1996), with smooth interpolation.
def mouse_shift(age):
    ages = [15, 19, 28, 32, 36]
    effects = [0.06, 0.10, 0.90, 0.17, 0.09]
    j = max(0, min(np.searchsorted(ages, age) - 1, len(ages) - 2))
    u = (age - ages[j]) / (ages[j + 1] - ages[j])
    smooth = u * u * (3 - 2 * u)
    return interpolate(effects[j], effects[j + 1], smooth)


class S11Unlocked2(SpokenScene):
    def construct(self):
        picture = world(closed=(1, 0), rates=(0.14, 0.58))
        self.add(picture, cortex_label())
        age = ValueTracker(19)
        axis, _ = age_axis(age, with_outcome=True)
        ready = ValueTracker(15.01)
        curve = axis.live_curve(mouse_shift, ready, color=BLUE, width=8)
        dot = axis.dot(age.get_value, lambda: mouse_shift(age.get_value()), color=GOLD)
        byline = label("Gordon & Stryker, 1996", PANEL_X, 2.79, 32, GOLD)
        axis_label = label("Shift in eye preference", PANEL_X, 2.12, 30)
        self.at("In 1996")
        self.play(FadeIn(byline), run_time=0.65)
        self.at("varied the age")
        self.play(FadeIn(axis), FadeIn(axis_label),
                  FadeIn(scope_tag("Schematic", size=28, color=GOLD)), run_time=0.72)
        self.add(curve)
        self.play(ready.animate.set_value(19), run_time=1.47, rate_func=linear)
        self.add(dot)
        self.at("The shift was largest", lead=0.37)
        self.play(age.animate.set_value(28), ready.animate.set_value(28), run_time=2.02, rate_func=linear)
        self.at("much smaller before")
        self.play(age.animate.set_value(19), run_time=1.65, rate_func=linear)
        self.at("or after about day", lead=0.34)
        self.play(age.animate.set_value(32), ready.animate.set_value(32), run_time=1.93, rate_func=linear)
        self.at("Those ages hold")
        self.play(FadeIn(label("Mouse visual cortex only", PANEL_X, 1.56, 28, GREEN)),
                  ready.animate.set_value(36), run_time=1.0)
        self.at("input across ages")
        self.play(age.animate.set_value(28), run_time=1.40)
        self.finish()


class S12End(EndCard):
    LINE = "Control sensory input across ages to reveal when experience wires circuits."
