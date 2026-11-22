"""Reading Behaviour Without Words, timed to the supplied Kokoro narration.

Colour map, adapted from the patch-clamp film:
BLUE: apparatus and tone. GREY: animal and chamber structure.
YELLOW: movement and movement readouts. PURPLE: neurons and circuits.
TEAL: arterial pressure and acesulfame K. ORANGE: sugar.
GREEN: a preserved response or an active control. RED: shock, lesion or loss.
GOLD: study dates and prediction. TEXT: labels.
"""

from bp_parts import *

PURPLE = "#B58CD9"
ORANGE = "#F29E4C"
SLATE = "#344257"
DISPLAY = "#192331"
EDGE = "#526985"
FLOOR = "#637D97"
FUR = "#93A5BE"
FUR_DARK = "#637892"
EAR = "#D1A9BB"
BED = "#334457"
LEFT_X, RIGHT_X = -3.45, 3.45
PAW_X = -1.83
CIRCUIT_JUNCTION_Y = 1.38
PREDICTION = "What happens to freezing?"
PREDICTION_CARD = {"y": -3.19, "left": -2.14, "size": 36}
PREDICTION_RING = (5.62, 0.33, 0)


def point(x, y):
    return np.array([x, y, 0.0])


def label(text, x, y, color=TEXT, size=30, width=5.55):
    return fit_text(text, max_w=width, size=size, min_size=28, color=color).move_to(point(x, y))


def panel(x, fill, width=6.16, height=5.42):
    return RoundedRectangle(
        width=width, height=height, corner_radius=0.24, stroke_color=EDGE,
        stroke_width=2.5, fill_color=fill, fill_opacity=1,
    ).move_to(point(x, -0.04))


def path(points, color, width=4):
    return VMobject(stroke_color=color, stroke_width=width).set_points_as_corners(
        [point(*xy) for xy in points]
    )


def ellipse(x, y, width, height, color):
    return Ellipse(width=width, height=height, stroke_width=0, fill_color=color,
                   fill_opacity=1).move_to(point(x, y))


def rodent(mouse=False, lifted=False):
    """Side view with independent paw, head and breathing torso."""
    tail = CubicBezier(point(-4.68, -1.33), point(-5.43, -1.46),
                      point(-5.10, -2.03), point(-6.32, -1.72),
                      stroke_color=EAR, stroke_width=7)
    haunch = ellipse(-4.17, -1.45, 1.35, 0.94, FUR_DARK)
    rear_paw = ellipse(-3.92, -1.94, 0.78, 0.15, EAR)

    body = VMobject(stroke_width=0, fill_color=FUR, fill_opacity=1)
    body.start_new_path(point(-5.04, -1.38))
    body.add_cubic_bezier_curve_to(point(-5.04, -0.21), point(-4.35, 0.51), point(-3.51, 0.37))
    body.add_cubic_bezier_curve_to(point(-2.89, 0.28), point(-2.58, -0.02), point(-2.26, -0.43))
    body.add_cubic_bezier_curve_to(point(-1.97, -0.93), point(-2.37, -1.60), point(-3.18, -1.69))
    body.add_cubic_bezier_curve_to(point(-3.87, -1.82), point(-4.87, -1.93), point(-5.04, -1.38))
    body.close_path()

    limb = CubicBezier(point(-2.81, -0.89), point(-2.87, -1.43), point(-2.55, -1.82),
                       point(-2.08, -1.89), stroke_color=FUR_DARK, stroke_width=18)
    paw = VGroup(limb, ellipse(PAW_X - 0.11, -1.94, 0.61, 0.17, EAR))
    pivot = point(-2.81, -0.89)
    if lifted:
        paw.rotate(0.59, about_point=pivot)

    ear_size = 0.83 if mouse else 0.69
    ear = ellipse(-2.19, 0.11, ear_size, ear_size, FUR).rotate(0.20)
    inner_ear = ellipse(-2.16, 0.13, ear_size * .65, ear_size * .65, EAR).rotate(0.20)
    head_shape = VMobject(stroke_width=0, fill_color=FUR, fill_opacity=1)
    head_shape.start_new_path(point(-2.91, -0.45))
    head_shape.add_cubic_bezier_curve_to(point(-2.89, 0.23), point(-2.13, 0.21), point(-1.82, -0.17))
    head_shape.add_cubic_bezier_curve_to(point(-1.54, -0.46), point(-1.23, -0.52), point(-1.03, -0.63))
    head_shape.add_cubic_bezier_curve_to(point(-0.95, -0.94), point(-2.25, -1.14), point(-2.83, -0.83))
    head_shape.close_path()
    eye = Dot(point(-1.89, -0.38), radius=0.107, color=DISPLAY)
    glint = Dot(point(-1.865, -0.353), radius=0.029, color=TEXT)
    nose = ellipse(-1.075, -0.651, 0.21, 0.18, EAR)
    whiskers = VGroup(
        Line(point(-1.26, -.71), point(-.74, -.58), stroke_color=TEXT, stroke_width=1.7),
        Line(point(-1.26, -.75), point(-.75, -.78), stroke_color=TEXT, stroke_width=1.7),
        Line(point(-1.28, -.78), point(-.82, -.95), stroke_color=TEXT, stroke_width=1.7),
    )
    head = VGroup(ear, inner_ear, head_shape, eye, glint, nose, whiskers)
    animal = VGroup(tail, haunch, rear_paw, body, paw, head)
    if mouse:
        animal.scale(0.83, about_point=point(LEFT_X, -2.02))

    animal.torso, animal.paw, animal.head = body, paw, head
    animal.shoulder = pivot
    return animal


def breathe(animal, amp=0.135):
    bob(animal.torso, amp=amp, speed=2.3)


def world(mouse=False, lifted=False):
    """The carried chamber, animal, readout housing, and schematic scope."""
    chamber = panel(LEFT_X, SLATE)
    display = panel(RIGHT_X, DISPLAY)
    floor = path([(-6.23, -2.05), (-2.03, -2.05)], FLOOR, 4)
    other_edge = path([(-1.69, -2.05), (-.68, -2.05)], FLOOR, 4)
    animal = rodent(mouse=mouse, lifted=lifted)
    return VGroup(chamber, display, floor, other_edge), animal, scope_tag(size=28, color=TEXT)


def add_world(scene, **kwargs):
    shell, animal, scope = world(**kwargs)
    scene.add(shell, animal, scope)
    return animal


def gauge(tracker, x, y, color, width=4.88, height=0.48):
    rim = RoundedRectangle(width=width, height=height, corner_radius=.1,
                           stroke_color=EDGE, stroke_width=2, fill_opacity=0)
    rim.move_to(point(x, y))
    trough = rim.copy().set_stroke(width=0).set_fill(BED, opacity=1)
    left = x - width / 2 + 0.07

    def fill():
        w = max(0.001, (width - .14) * np.clip(tracker.get_value(), 0, 1))
        return Rectangle(width=w, height=height - .14, stroke_width=0,
                         fill_color=color, fill_opacity=1).move_to(point(left + w / 2, y))

    meter = VGroup(trough, always_redraw(fill), rim)
    meter.rim = rim
    return meter


def highlight_gauge(meter, color):
    return meter.rim.animate(rate_func=there_and_back).set_stroke(color, width=10)


def trial_meter(progress):
    return VGroup(label("Behavioural assay", RIGHT_X, 1.00, BLUE, 36),
                  gauge(progress, RIGHT_X, -0.05, BLUE, height=.65))


def filament(stroke_width, y):
    return Line(point(PAW_X, y - .54), point(PAW_X, y),
                stroke_color=BLUE, stroke_width=stroke_width)


def filament_key(x, width):
    handle = RoundedRectangle(width=.89, height=.65, corner_radius=.12,
                              fill_color=BLUE, fill_opacity=.82, stroke_width=0)
    handle.move_to(point(x, -.88))
    shaft = Rectangle(width=width, height=1.52, fill_color=BLUE, fill_opacity=1,
                      stroke_width=0).move_to(point(x, .14))
    return VGroup(handle, shaft)


def question_badge(x, y, radius, size, fill="#745831"):
    disk = Circle(radius=radius, stroke_color=GOLD, stroke_width=4,
                  fill_color=fill, fill_opacity=1).move_to(point(x, y))
    return VGroup(disk, label("?", x, y, GOLD, size))


def lift(animal, angle):
    return Rotate(animal.paw, angle=angle, about_point=animal.shoulder)


def withdrawal_plot(threshold):
    plot = Plot(box=(1.65, 6.02, -1.61, 1.35), xr=(0, 1), yr=(0, 1), color=EDGE)
    names = VGroup(label("Paw-lift fraction", 3.7, 1.89, YELLOW, 32),
                   label("Filament force →", 3.88, -2.15, TEXT, 28))

    # A schematic monotone response. The narration supplies the half-height
    # criterion and the direction of its shift. Distances are illustrative.
    def fraction(force):
        midpoint = threshold.get_value()
        limits = [0, midpoint * .44, midpoint, midpoint + .58 * (1 - midpoint), 1]
        return np.interp(force, limits, [.02, .09, .5, .91, .98])

    curve = always_redraw(lambda: plot.curve(fraction, color=YELLOW, width=6, n=100))
    half = VGroup(plot.hline(.5, color=EDGE),
                  label("½", 1.17, -0.13, TEXT, 31, width=.45))
    marker = plot.dot(threshold.get_value, lambda: .5, color=YELLOW, ring=DISPLAY)
    foot = always_redraw(lambda: DashedLine(plot.pt(threshold.get_value(), 0),
                                            plot.pt(threshold.get_value(), .5),
                                            color=YELLOW, stroke_width=3, dash_length=.14))
    criterion = VGroup(half, foot, marker)
    return plot, names, curve, criterion


def speaker(low=False):
    face = RoundedRectangle(width=.67, height=.67, corner_radius=.11, stroke_color=BLUE,
                            stroke_width=2.8, fill_color=DISPLAY, fill_opacity=1)
    face.move_to(point(-5.68, .12 if low else 1.36))
    cone = Circle(.18, color=BLUE, stroke_width=3).move_to(face)
    return VGroup(face, cone, Dot(face.get_center(), radius=.063, color=BLUE))


def sound_rings(low=False):
    origin = point(-5.40, .12 if low else 1.36)
    spread = .34 if low else .49
    reach = 1.45 if low else 2.50

    def rings(elapsed):
        phases = [(elapsed / 1.45 + k / 3) % 1 for k in range(3)]
        return VGroup(*[
            Arc(radius=.28 + reach * p, start_angle=-spread, angle=2 * spread,
                arc_center=origin, stroke_width=8, stroke_color=BLUE,
                stroke_opacity=.9 * np.sin(PI * p))
            for p in phases
        ])

    elapsed = 0.0

    def advance(group, dt):
        nonlocal elapsed
        elapsed += dt
        group.become(rings(elapsed))

    return rings(0).add_updater(advance)


def sound_wave(scene, duration, low=False):
    rings = sound_rings(low)
    scene.add(rings)
    scene.wait(duration)
    scene.play(FadeOut(rings), run_time=.30)


def pressure_trace(level, box):
    # Qualitative pressure response: baseline, rise, then sustained response.
    # No pressure or time units are implied.
    x0, x1, y0, y1 = box
    plot = Plot(box=box, xr=(0, 1), yr=(0, 1))
    baseline = Line(point(x0, y0 + .16 * (y1 - y0)), point(x1, y0 + .16 * (y1 - y0)),
                    stroke_color=EDGE, stroke_width=2)

    def trace():
        def response(t):
            rise = np.clip((t - .21) / .49, 0, 1)
            return .16 + .71 * level.get_value() * rise**2 * (3 - 2 * rise)

        return plot.curve(response, color=TEAL, width=6, n=65)

    return baseline, always_redraw(trace)


def response_panel(freezing, pressure):
    p_base, p_trace = pressure_trace(pressure, (1.05, 5.85, -2.13, -.59))
    return (
        VGroup(label("Freezing", RIGHT_X, 1.89, YELLOW, 32),
               gauge(freezing, RIGHT_X, .81, YELLOW, height=.57)),
        VGroup(label("Arterial pressure", RIGHT_X, -.08, TEAL, 32), p_base, p_trace),
    )


def control_circuit(lesioned=False):
    nucleus = boxed_label("Central amygdala", PURPLE, size=29, pad=.21, fill_opacity=.44).move_to(point(LEFT_X, 2.16))
    nucleus.label.set_color(TEXT)
    y = CIRCUIT_JUNCTION_Y
    stem = Line(nucleus.get_bottom(), point(LEFT_X, y), stroke_color=PURPLE, stroke_width=7)
    freezing_path = path([(LEFT_X, y), (-2.15, y), (-1.60, .97)], YELLOW, 12)
    if lesioned:
        pressure_path = VGroup(
            path([(LEFT_X, y), (-4.60, y)], TEAL, 12),
            path([(-4.91, y - .18), (-5.30, .97)], TEAL, 8).set_stroke(opacity=.52),
            Line(point(-4.63, y - .15), point(-4.81, y + .09), stroke_color=RED, stroke_width=8),
            Line(point(-4.77, y - .29), point(-4.95, y - .05), stroke_color=RED, stroke_width=8),
        )
    else:
        pressure_path = path([(LEFT_X, y), (-4.75, y), (-5.30, .97)], TEAL, 12)
    return nucleus, stem, pressure_path, freezing_path


def prediction_gauges():
    frozen, pressure = ValueTracker(0), ValueTracker(0)
    return (
        VGroup(label("Freezing", 3.25, 1.47, YELLOW, 33),
               gauge(frozen, 2.94, .33, YELLOW, width=3.72, height=.58)),
        VGroup(label("Arterial pressure", RIGHT_X, -.75, TEAL, 33),
               *pressure_trace(pressure, (1.05, 5.85, -2.22, -1.14))),
        frozen, pressure,
    )


def question_mark():
    return label("?", *PREDICTION_RING[:2], GOLD, 39, width=.58).set_z_index(2)


def prediction_timer(seconds):
    timer, advance = countdown(seconds, center=PREDICTION_RING, radius=.45)
    timer[1].set_stroke(width=24).add_updater(lambda arc: arc.set_stroke(width=24))
    remaining = advance.mobject
    timer[0].add_updater(
        lambda disk: disk.set_fill(opacity=.50 - .40 * remaining.get_value()),
        call_updater=True,
    )
    return timer, advance


def freezing_emphasis():
    return RoundedRectangle(
        width=5.80, height=2.25, corner_radius=.22, stroke_width=0,
        fill_color=YELLOW, fill_opacity=.27,
    ).move_to(point(RIGHT_X, .77))


def predict_backdrop():
    shell, animal, scope = world()
    freeze, pressure, _, _ = prediction_gauges()
    return VGroup(shell, animal, scope, *control_circuit(lesioned=True),
                  speaker(low=True), freeze.set_z_index(1), pressure, question_mark())


class S01Hook(SpokenScene, TitleCard):
    LESSON = "Rodent behavioural assays"
    TITLE = "Reading Behaviour Without Words"

    def construct(self):
        animal = add_world(self)
        breathe(animal)
        arrow = Arrow(point(PAW_X, -2.52), point(PAW_X, -2.00), buff=0,
                      color=BLUE, stroke_width=5, tip_length=.11)
        self.at("a touch")
        nod = point(-2.63, -.54)
        self.play(GrowArrow(arrow), Rotate(animal.head, -.14, about_point=nod), run_time=.58)
        q = question_badge(-1.98, 1.32, .76, 66, fill=BG)
        self.at("How do scientists")
        self.play(FadeIn(q, shift=UP * .14), Rotate(animal.head, .14, about_point=nod), run_time=.51)
        title = T(self.TITLE, 42, TEXT, font=TITLE_FONT).move_to(point(-.7, 3.22))
        self.at("fear or choice")
        self.play(FadeIn(title), run_time=.28)
        self.wait(1.08)
        self.play(FadeOut(title), run_time=.28)
        progress = ValueTracker(0)
        meter = trial_meter(progress)
        self.at("They use behavioral")
        self.play(FadeIn(meter[1]), FadeOut(q), run_time=.29)
        self.at("behavioral assays")
        self.play(FadeIn(meter[0]),
                  progress.animate.set_value(.26), run_time=1.35)
        self.at("turn an animal's actions")
        self.play(progress.animate.set_value(.97), run_time=3.25, rate_func=linear)
        self.finish()


class S02Vonfrey(SpokenScene):
    def construct(self):
        animal = add_world(self)
        breathe(animal)
        trial = trial_meter(ValueTracker(.97))
        arrow = Arrow(point(PAW_X, -2.52), point(PAW_X, -2.00), buff=0,
                      color=BLUE, stroke_width=5, tip_length=.11)
        self.add(trial, arrow)
        self.at("Start with touch")
        self.play(FadeOut(arrow), FadeOut(trial), run_time=.55)
        probe = filament(3, -2.12)
        self.add(probe)
        self.at("Researchers press")
        probes = [filament_key(x, width) for x, width in ((1.96, .07), (3.45, .14), (4.94, .24))]
        self.play(probe.animate.shift(UP * .20), FadeIn(probes[0], shift=UP * .34), run_time=1.20)
        self.play(probe.animate.shift(DOWN * .20), run_time=.48)
        self.at("increasing stiffness")
        second = filament(6, -2.12)
        self.play(ReplacementTransform(probe, second), FadeIn(probes[1], shift=UP * .34),
                  probes[0].animate.set_opacity(.47), run_time=.55)
        self.play(second.animate.shift(UP * .20), run_time=.70)
        name = label("von Frey filaments", RIGHT_X, 1.64, BLUE, 34)
        self.at("called von Frey")
        self.play(FadeIn(name), second.animate.shift(DOWN * .20), run_time=.92)
        self.at("against a paw")
        third = filament(10, -2.12)
        self.play(ReplacementTransform(second, third), FadeIn(probes[2], shift=UP * .34),
                  probes[1].animate.set_opacity(.47), run_time=.40)
        self.play(third.animate.shift(UP * .20), run_time=1.05)
        self.play(lift(animal, .59), third.animate.shift(DOWN * .18), run_time=.50)

        threshold = ValueTracker(.64)
        plot, names, curve, criterion = withdrawal_plot(threshold)
        self.at("Repeating the test")
        self.play(FadeOut(VGroup(name, *probes)), lift(animal, -.59), run_time=.37)
        self.play(Create(plot), FadeIn(names), run_time=.49)
        self.play(Create(curve), run_time=.75)
        self.at("withdrawal threshold")
        heading = label("Withdrawal threshold", -3.47, 1.62, YELLOW, 32)
        self.play(FadeIn(heading), run_time=.68)
        self.at("force that makes")
        self.play(third.animate.shift(UP * .18), run_time=1.0)
        self.play(lift(animal, .59), third.animate.shift(DOWN * .18), run_time=.62)
        self.at("Many labs use")
        self.play(FadeIn(criterion[0]), run_time=1.1)
        self.at("half the time")
        self.play(FadeIn(criterion[1]), FadeIn(criterion[2]), lift(animal, -.59), run_time=1.1)
        self.at("A fall in that threshold")
        thin = filament(4, -2.10)
        self.play(threshold.animate.set_value(.33), ReplacementTransform(third, thin), run_time=2.05)
        self.play(thin.animate.shift(UP * .18), run_time=.54)
        self.at("allodynia pain")
        self.play(lift(animal, .59), thin.animate.shift(DOWN * .18),
                  swap(heading, label("Allodynia", LEFT_X, 1.62, YELLOW, 35)), run_time=.80)
        self.play(thin.animate.shift(DOWN * .08), run_time=1.35)
        self.finish()


class S03Conditioning(SpokenScene):
    def construct(self):
        animal = add_world(self, lifted=True)
        breathe(animal)
        plot, names, curve, half = withdrawal_plot(ValueTracker(.33))
        previous = VGroup(plot, names, curve, half, label("Allodynia", LEFT_X, 1.62, YELLOW, 35))
        probe = filament(4, -2.18)
        self.add(previous, probe)
        self.at("Assays also measure")
        self.play(FadeOut(previous), FadeOut(probe, shift=DOWN * .12), lift(animal, -.59), run_time=.9)
        horn = speaker()
        self.play(FadeIn(horn), run_time=.76)
        self.at("In Pavlovian threat conditioning")
        conditioning = label("Pavlovian threat conditioning", RIGHT_X, 1.65, TEXT, 32)
        self.play(FadeIn(conditioning), run_time=.65)
        self.at("a harmless conditioned stimulus")
        tone = boxed_label("Conditioned stimulus", BLUE, size=33, pad=.26, fill_opacity=.31)
        tone.move_to(point(RIGHT_X, .62))
        tone.label.set_color(TEXT)
        head_pivot = point(-2.62, -.50)
        paired_tone = sound_rings()
        self.add(paired_tone)
        self.play(Rotate(animal.head, .16, about_point=head_pivot), run_time=.80)
        self.play(FadeIn(tone, scale=.95), run_time=.49)

        self.at("a brief foot shock")
        flash = Rectangle(width=4.74, height=.23, stroke_width=0, fill_color=RED,
                          fill_opacity=.6).move_to(point(-3.45, -1.87))
        self.play(FadeIn(flash), lift(animal, .36),
                  Rotate(animal.head, .11, about_point=head_pivot), run_time=.21)
        self.play(FadeOut(flash), FadeOut(paired_tone), run_time=.30)
        self.at("That shock is")
        shock = boxed_label("Unconditioned stimulus", RED, size=32, pad=.26, fill_opacity=.26)
        shock.move_to(point(RIGHT_X, -.76))
        shock.label.set_color(TEXT)
        self.play(FadeIn(shock), run_time=.65)
        self.at("an unlearned reaction")
        self.play(lift(animal, -.36),
                  Rotate(animal.head, -.27, about_point=head_pivot), run_time=1.0)

        self.at("Later the tone alone", lead=.60)
        animal.torso.clear_updaters()
        animal.torso.move_to(rodent().torso)
        breathe(animal, amp=.068)
        self.play(FadeOut(VGroup(conditioning, tone, shock)), run_time=.43)
        sound_wave(self, .72)
        f, p = ValueTracker(0), ValueTracker(0)
        free, pressure = response_panel(f, p)
        self.at("triggers conditioned responses")
        self.play(FadeIn(free[1]), run_time=.4)
        self.at("freezing still")
        self.play(FadeIn(free[0]), f.animate.set_value(1), run_time=1.55)
        self.at("and rising arterial pressure")
        self.play(FadeIn(pressure), p.animate.set_value(1), run_time=1.9)
        self.finish()


class S04PredictQ(SpokenScene):
    def construct(self):
        animal = add_world(self)
        rest = animal.torso.get_center().copy()
        breathe(animal)
        horn = speaker()
        f, p = ValueTracker(1), ValueTracker(1)
        free, pressure = response_panel(f, p)
        self.add(horn, free, pressure)
        self.at("An assay measures an action")
        self.play(highlight_gauge(free[1], YELLOW), run_time=1.38)
        self.at("paired controls")
        rule = caption("Paired controls separate causes", size=34, color=GREEN)
        self.play(FadeIn(rule),
                  Indicate(pressure[2], color=TEAL, scale_factor=1.04), run_time=1.21)
        self.at("Test that idea")
        self.play(FadeOut(rule), FadeOut(free), FadeOut(pressure),
                  horn.animate.move_to(speaker(low=True)), run_time=.54)
        blank_free, blank_pressure, _, _ = prediction_gauges()
        self.play(FadeIn(blank_free.set_z_index(1)), FadeIn(blank_pressure), run_time=.55)
        node, stem, intact, second = control_circuit()
        self.at("Suppose you damage")
        self.play(FadeIn(node[0]), Create(stem), run_time=.73)
        self.play(Create(intact), Create(second), run_time=1.24)
        self.at("below the central amygdala")
        self.play(FadeIn(node[1]), run_time=.56)
        self.at("then condition rats")
        sound_wave(self, 1.44, low=True)
        self.at("If that target drives")
        damaged = control_circuit(lesioned=True)[2]
        pressure_focus = RoundedRectangle(
            width=5.40, height=1.94, corner_radius=.18, stroke_width=0,
            fill_color=TEAL, fill_opacity=.28,
        ).move_to(point(RIGHT_X, -1.43))
        self.play(FadeOut(intact), run_time=.29)
        blank_pressure.set_z_index(1)
        self.play(FadeIn(damaged), FadeIn(pressure_focus), run_time=.68)
        self.at("what happens to freezing")
        question = question_card(PREDICTION, **PREDICTION_CARD)
        mark = question_mark()
        ring, _ = prediction_timer(4.5)
        ring.set_z_index(1)
        self.play(FadeIn(question), FadeIn(mark), FadeOut(pressure_focus),
                  FadeIn(freezing_emphasis()), run_time=.59)
        animal.torso.clear_updaters()
        self.play(FadeIn(ring, scale=.82), animal.torso.animate.move_to(rest), run_time=.51)
        self.finish()


class S05PredictPause(PredictPause):
    QUESTION = PREDICTION
    CARD = PREDICTION_CARD
    SECONDS = 4.5

    def backdrop(self):
        return predict_backdrop()

    def construct(self):
        self.add(self.backdrop(), question_card(self.QUESTION, **self.CARD))
        ring, advance = prediction_timer(self.SECONDS)
        remaining = advance.mobject
        emphasis = freezing_emphasis()
        emphasis.add_updater(lambda box: box.set_fill(opacity=.27 * remaining.get_value()))
        self.add(emphasis, ring.set_z_index(1))
        self.play(advance)


def reflex_comparison():
    split = TwoPanel("Reflex\nreadout", "Reported\npain", colors=(YELLOW, GREY),
                     top=2.01, bottom=-2.03, width=5.65, gap=.24, size=30).shift(RIGHT * RIGHT_X)
    split.left_head.shift(DOWN * .18)
    split.right_head.shift(DOWN * .18)
    tracker = ValueTracker(0)
    reflex = gauge(tracker, 1.97, -.26, YELLOW, width=1.91, height=.51)
    missing = label("—", 4.92, -.24, GREY, 53, width=1.05)
    return split, reflex, missing, tracker


class S06Controls(SpokenScene):
    def construct(self):
        animal = add_world(self)
        breathe(animal)
        circuit = VGroup(*control_circuit(lesioned=True))
        horn = speaker(low=True)
        freeze, pressure, f, p = prediction_gauges()
        question = question_card(PREDICTION, **PREDICTION_CARD)
        mark = question_mark()
        pause_ring, _ = prediction_timer(4.5)
        pause_ring.remove(pause_ring[1])
        pause_ring[0].clear_updaters().set_fill(opacity=.5)
        self.add(circuit, horn, freeze, pressure, question, mark, pause_ring)
        self.at("Freezing stays intact")
        self.play(FadeOut(question), FadeOut(mark), FadeOut(pause_ring), f.animate.set_value(1), run_time=1.34)
        self.at("the pressure rise drops")
        # Rebuild the pressure trace from the reference rise, then flatten it
        # over the lesion result. The freezing bar remains at its matched level.
        p.set_value(1)
        self.play(p.animate.set_value(0), run_time=1.7)
        self.at("Measuring two responses")
        self.play(highlight_gauge(freeze[1], YELLOW), run_time=1.65)
        self.play(Indicate(pressure[1], color=TEAL, scale_factor=1.02), run_time=1.48)
        self.at("If freezing survives")
        survived = label("Threat learning intact", LEFT_X, 1.47, GREEN, 34)
        self.play(FadeOut(circuit), FadeOut(horn), run_time=.52)
        self.play(FadeIn(survived), run_time=.63)
        self.play(highlight_gauge(freeze[1], GREEN), run_time=1.65)
        self.at("Still readouts")
        self.play(FadeOut(VGroup(freeze, pressure, survived)), run_time=.52)
        split, reflex, missing, value = reflex_comparison()
        self.play(FadeIn(split[::2]), FadeIn(reflex), run_time=.80)
        self.at("A paw lift measures")
        probe = filament(5, -2.13)
        self.add(probe)
        self.play(probe.animate.shift(UP * .20), run_time=.46)
        self.play(lift(animal, .59), probe.animate.shift(DOWN * .20),
                  value.animate.set_value(1), FadeIn(split.left_head), run_time=.65)
        self.at("a report of pain")
        self.play(FadeIn(split.right_head), FadeIn(missing), run_time=.66)
        self.finish()


def cell_icon(x, y, color=PURPLE):
    soma = ellipse(x, y, .86, .71, color)
    branches = VGroup(
        path([(x - .42, y + .04), (x - .83, y + .34), (x - 1.1, y + .34)], PURPLE, 4),
        path([(x - .81, y + .34), (x - .91, y + .62)], PURPLE, 4),
        path([(x - .31, y - .19), (x - .72, y - .46), (x - .98, y - .48)], PURPLE, 4),
        path([(x + .39, y), (x + 1.13, y), (x + 1.31, y - .2)], PURPLE, 4),
    )
    return VGroup(branches, soma, Dot(point(x, y), .14, color=DISPLAY))


def spike_monitor(progress):
    plot = Plot(box=(1.07, 5.84, -.99, .17), xr=(0, 1), yr=(0, 1), color=EDGE)
    times = np.array([.19, .42, .72, .84])

    def activity(t):
        return .21 + .74 * np.maximum(0, 1 - np.abs(times - t) / .027).max()

    return plot, plot.live_curve(activity, progress, color=PURPLE, width=5)


def neural_timeline():
    x0, x1 = 1.34, 5.65
    top = VGroup(label("Lifelong mutant", RIGHT_X, 1.81, PURPLE, 33),
                 path([(x0, 1.04), (x1, 1.04)], EDGE, 5))
    bottom = VGroup(label("Acute change", RIGHT_X, -.22, PURPLE, 33),
                    path([(x0, -.97), (x1, -.97)], EDGE, 5),
                    label("Adult", x1, -1.58, TEXT, 29, width=1.12))
    whole = path([(x0, 1.04), (x1, 1.04)], RED, 9)
    part = path([(4.4, -.97), (x1, -.97)], RED, 9)
    toggle = Dot(point(4.40, -.97), radius=.16, color=RED)
    return top, bottom, whole, part, toggle


class S07Limits(SpokenScene):
    def construct(self):
        animal = add_world(self, lifted=True)
        breathe(animal)
        split, reflex, missing, value = reflex_comparison()
        value.set_value(1)
        probe = filament(5, -2.13)
        self.add(split, reflex, missing, probe)
        self.at("Behavior alone cannot")
        self.play(FadeOut(VGroup(split, reflex, missing, probe)), lift(animal, -.59), run_time=1.0)
        cell = cell_icon(RIGHT_X, .66).scale(1.16)
        self.play(FadeIn(cell, scale=.65), run_time=.67)
        self.at("which circuit mechanism")
        unknown = question_badge(RIGHT_X, -.89, .65, 52)
        self.play(FadeIn(unknown, shift=UP * .18), run_time=.69)
        self.at("So scientists pair")
        self.play(FadeOut(unknown), cell.animate.shift(UP * .33), run_time=.85)
        progress = ValueTracker(0)
        axes, spikes = spike_monitor(progress)
        self.at("with neural tests")
        self.play(Create(axes), run_time=.86)
        self.add(spikes)
        self.at("Recording tracks")
        recording = label("Recording", RIGHT_X, -1.62, PURPLE, 34)
        self.play(FadeIn(recording), progress.animate.set_value(1), run_time=1.85, rate_func=linear)
        self.at("Stimulation tests")
        lamp = Triangle(stroke_width=0, fill_color=BLUE, fill_opacity=.26).scale(.70)
        lamp.rotate(-PI / 2).stretch(2.1, 0).move_to(point(2.21, 1.77))
        lamp.rotate(-.47).shift(DOWN * .28 + RIGHT * .36)
        stimulation = label("Stimulation", RIGHT_X, -1.62, BLUE, 34)
        self.play(FadeOut(VGroup(axes, spikes)), FadeIn(lamp), run_time=.42)
        self.play(cell[1].animate.set_fill(GREEN), swap(recording, stimulation), run_time=.72)
        suff = label("Are these cells enough?", RIGHT_X, -.64, TEXT, 31)
        self.play(FadeIn(suff), run_time=.42)
        self.at("and silencing")
        silencing = label("Silencing", RIGHT_X, -1.62, RED, 34)
        mute = Line(point(4.64, .74), point(5.03, 1.21), stroke_color=RED, stroke_width=8)
        self.play(FadeOut(lamp), FadeOut(suff), Create(mute),
                  cell[1].animate.set_fill(FUR_DARK),
                  swap(stimulation, silencing), run_time=.77)
        need = label("Are these cells needed?", RIGHT_X, -.64, TEXT, 31)
        self.at("whether they are needed")
        self.play(FadeIn(need), run_time=.51)
        self.at("A lifelong mutant")
        self.play(FadeOut(VGroup(cell, mute, need, silencing)), run_time=.42)
        top, bottom, whole, part, toggle = neural_timeline()
        self.play(FadeIn(top), Create(whole), run_time=1.04)
        self.at("an acute change")
        self.play(FadeIn(bottom), run_time=.67)
        self.at("when the loss happened")
        self.play(FadeIn(toggle), Create(part), run_time=1.19)
        self.at("Conditions matter too")
        self.play(FadeOut(VGroup(top, bottom, whole, part, toggle)), run_time=.49)
        mouse = rodent(mouse=True)
        self.play(ReplacementTransform(animal, mouse), run_time=.50)
        breathe(mouse)
        males = boxed_label("Male mice", PURPLE, size=30, pad=.24).move_to(point(RIGHT_X, 1.43))
        females = boxed_label("Female mice", PURPLE, size=30, pad=.24).move_to(point(RIGHT_X, -.10))
        self.at("Male and female")
        self.play(FadeIn(males), FadeIn(females, shift=DOWN * .12), run_time=.59)
        self.play(FadeIn(label("Responses can differ", RIGHT_X, -1.67, TEXT, 31)), run_time=.58)
        self.finish()


def outcome_cards():
    left_title = "Lateral\nhypothalamus\nlesion"
    right_title = "Caudal PAG\nlesion"
    split = TwoPanel(left_title, right_title, colors=(PURPLE, PURPLE), top=1.77,
                     bottom=-2.27, width=5.72, gap=.25, size=28).shift(RIGHT * RIGHT_X)
    split.left_head.become(T(left_title, 28, PURPLE, line_spacing=.56).move_to(point(1.96, 1.04)))
    split.right_head.become(label(right_title, 4.94, 1.18, PURPLE, 28, 2.41))

    def channels(x):
        f, p = ValueTracker(1), ValueTracker(1)
        return (
            VGroup(label("Freezing", x, .035, YELLOW, 28, 2.30), gauge(f, x, -.48, YELLOW, width=2.05, height=.41)),
            VGroup(label("Pressure", x, -.97, TEAL, 28, 2.30),
                   *pressure_trace(p, (x - 1.02, x + 1.02, -2.03, -1.39))),
            f, p,
        )

    return split, channels(1.96), channels(4.94)


def study(text):
    return label(text, RIGHT_X, 2.27, GOLD, 30)


def circuit_legend():
    return VGroup(label("Pressure", -5.26, .62, TEAL, 28, 2.3),
                  label("Freezing", -1.59, .62, YELLOW, 28, 2.3))


class S08UnlockedA(SpokenScene):
    def construct(self):
        animal = add_world(self, mouse=True)
        ending = VGroup(
            boxed_label("Male mice", PURPLE, size=30, pad=.24).move_to(point(RIGHT_X, 1.43)),
            boxed_label("Female mice", PURPLE, size=30, pad=.24).move_to(point(RIGHT_X, -.10)),
            label("Responses can differ", RIGHT_X, -1.67, TEXT, 31),
        )
        self.add(ending)
        self.at("Those controls let")
        rat = rodent()
        self.play(FadeOut(ending), ReplacementTransform(animal, rat), run_time=.67)
        breathe(rat)
        node, stem, left, right = control_circuit()
        self.play(FadeIn(node), Create(stem), run_time=.66)
        self.play(Create(left), Create(right), run_time=1.25)
        names = circuit_legend()
        self.play(FadeIn(names), run_time=.60)
        self.at("In 1988")
        reference = study("LeDoux et al., 1988")
        self.play(FadeIn(reference), run_time=.74)
        self.at("tested threat conditioning")
        horn = speaker(low=True).shift(DOWN * .21)
        self.play(FadeIn(horn), run_time=.56)
        self.play(Indicate(horn[1], color=BLUE, scale_factor=1.25), run_time=1.45)
        self.at("Lateral hypothalamic lesions")
        cards, first, second = outcome_cards()
        lf, lp, lfv, lpv = first
        rf, rp, rfv, rpv = second
        damaged = control_circuit(lesioned=True)[2]
        self.play(FadeOut(left), FadeIn(cards.left_frame), run_time=.37)
        self.play(FadeIn(damaged), FadeIn(cards.left_head), FadeIn(lf), FadeIn(lp), run_time=.59)
        self.at("impaired the pressure")
        self.play(lpv.animate.set_value(0), run_time=1.51)
        self.at("while sparing freezing")
        self.play(highlight_gauge(lf[1], YELLOW), run_time=1.2)
        self.at("Lesions in a midbrain")
        self.play(FadeOut(damaged), FadeIn(cards.right_frame), run_time=.43)
        self.play(FadeIn(left), FadeIn(rf), FadeIn(rp), run_time=.70)
        self.at("the caudal")
        self.play(FadeIn(cards.right_head), run_time=.75)
        broken_right = damaged.copy().flip(UP, about_point=point(LEFT_X, CIRCUIT_JUNCTION_Y))
        broken_right[0].set_stroke(YELLOW)
        broken_right[1].set_stroke(YELLOW)
        self.at("disrupted freezing")
        self.play(FadeOut(right), run_time=.22)
        self.play(FadeIn(broken_right), rfv.animate.set_value(0), run_time=.81)
        self.at("while sparing pressure")
        self.play(Indicate(rp[2], color=TEAL, scale_factor=1.015), run_time=.94)
        self.at("Measuring both responses")
        self.play(FadeOut(broken_right), run_time=.26)
        self.play(FadeIn(right), FadeOut(horn), run_time=.45)
        self.play(Indicate(left, color=TEAL, scale_factor=1.045),
                  Indicate(right, color=YELLOW, scale_factor=1.045), run_time=1.6)
        rule = caption("Two output routes", size=34, color=GREEN)
        self.play(FadeIn(rule), run_time=.78)
        self.finish()


def cord_inset():
    y = 1.47
    sheath = RoundedRectangle(width=4.62, height=.98, corner_radius=.32,
                              stroke_color=PURPLE, stroke_width=3.2,
                              fill_color=BG, fill_opacity=1).move_to(point(LEFT_X, y))
    center = path([(-5.44, y), (-1.45, y)], FUR_DARK, 4)
    cells = VGroup(*[
        Dot(point(x, y + offset), radius=.16, color=PURPLE)
        for x, offset in [(-5.02, -.11), (-4.55, .09), (-3.76, -.10),
                          (-3.24, .11), (-2.57, -.07), (-2.02, .10)]
    ])
    selected = VGroup(cells[1], cells[3], cells[5])
    return VGroup(sheath, center), cells, selected


def ablation_marks(selected):
    return VGroup(*[
        VGroup(
            Line(point(-.14, -.14), point(.14, .14), stroke_color=RED, stroke_width=5),
            Line(point(-.14, .14), point(.14, -.14), stroke_color=RED, stroke_width=5),
        ).move_to(cell)
        for cell in selected
    ])


def itch_pain_panel(scratching, pain):
    return (
        VGroup(label("Scratching", RIGHT_X, 1.16, YELLOW, 33),
               gauge(scratching, RIGHT_X, .55, YELLOW, height=.57)),
        VGroup(label("Pain behaviours", RIGHT_X, -.64, YELLOW, 33),
               gauge(pain, RIGHT_X, -1.24, YELLOW, height=.57)),
    )


class S09UnlockedB(SpokenScene):
    def construct(self):
        animal = add_world(self)
        previous_circuit = VGroup(*control_circuit(), circuit_legend())
        self.add(previous_circuit)
        cards, (lf, lp, _, lpv), (rf, rp, rfv, _) = outcome_cards()
        lpv.set_value(0)
        rfv.set_value(0)
        previous = VGroup(cards, lf, lp, rf, rp, study("LeDoux et al., 1988"),
                          caption("Two output routes", size=34, color=GREEN))
        self.add(previous)
        self.at("In 2009")
        mouse = rodent(mouse=True)
        self.play(FadeOut(previous), FadeOut(previous_circuit),
                  ReplacementTransform(animal, mouse), run_time=.75)
        breathe(mouse)
        citation = study("Sun et al., 2009")
        self.play(FadeIn(citation), run_time=.58)
        scratch, pain = ValueTracker(.88), ValueTracker(.77)
        scratch_row, pain_row = itch_pain_panel(scratch, pain)
        self.at("separated itch from pain")
        self.play(FadeIn(scratch_row), FadeIn(pain_row), run_time=.76)
        inset, cells, selected = cord_inset()
        self.at("They ablated")
        self.play(FadeIn(inset, scale=.85), run_time=.66)
        self.play(LaggedStart(*[FadeIn(c) for c in cells], lag_ratio=.15), run_time=.90)
        self.at("set of spinal neurons")
        self.play(*[c.animate.scale(1.45).set_stroke(RED, width=5) for c in selected], run_time=.84)
        self.at("marked by GRPR")
        named = label("GRPR spinal neurons", LEFT_X, 2.26, PURPLE, 29)
        self.play(FadeIn(named), run_time=.48)
        marks = ablation_marks(selected)
        self.play(*[FadeOut(c) for c in selected], FadeIn(marks), run_time=.45)
        self.at("stimuli dropped sharply")
        self.play(scratch.animate.set_value(.17), run_time=1.42)
        self.at("measured pain behaviors")
        self.play(highlight_gauge(pain_row[1], GREEN), run_time=1.75)
        self.finish()


def spout(x, color, backwards=False):
    head = RoundedRectangle(width=.66, height=1.16, corner_radius=.14, stroke_color=color,
                            stroke_width=3, fill_opacity=1, fill_color=DISPLAY).move_to(point(x, 1.26))
    tank = RoundedRectangle(width=.41, height=.68, corner_radius=.09, stroke_width=0,
                            fill_color=color, fill_opacity=.8).move_to(point(x, 1.13))
    direction = -1 if backwards else 1
    neck = path([(x, .66), (x, .46), (x + direction * .41, .25)], color, 7)
    tip = Dot(point(x + direction * .41, .25), radius=.09, color=TEXT)
    return VGroup(head, tank, neck, tip)


def choice_timeline(clock):
    start, end = 1.02, 5.88
    y = -1.82
    base = path([(start, y), (end, y)], EDGE, 3)
    ticks = VGroup(*[
        path([(x, y - .07), (x, y + .07)], EDGE, 3)
        for x in [start, (start + end) / 2, end]
    ])
    labels = VGroup(label("Start", start + .17, -2.26, TEXT, 28, 1.04),
                    label("24 h", (start + end) / 2, -2.26, TEXT, 28, 1.04),
                    label("48 h", end - .05, -2.26, TEXT, 28, 1.04))
    marker = Dot(point(start, y), radius=.102, color=GOLD)
    marker.add_updater(lambda dot: dot.move_to(point(start + (end - start) * clock.get_value() / 48, y)))
    return VGroup(base, ticks, labels, marker)


def taste_icon():
    x, y = LEFT_X, 1.17
    frame = Circle(radius=.68, color=RED, stroke_width=4).move_to(point(x, y))
    mouth = Arc(radius=.38, start_angle=PI, angle=PI, arc_center=point(x, y + .13),
                stroke_width=4, stroke_color=TEXT)
    tongue = ellipse(x, y + .02, .33, .47, EAR)
    strike = Line(point(x - .45, y - .43), point(x + .45, y + .45), stroke_color=RED, stroke_width=6)
    return VGroup(frame, mouth, tongue, strike)


class S10UnlockedCClose(SpokenScene):
    def construct(self):
        animal = add_world(self, mouse=True)
        breathe(animal)
        inset, cells, selected = cord_inset()
        old_rows = itch_pain_panel(ValueTracker(.17), ValueTracker(.77))
        previous = VGroup(inset, cells[::2], ablation_marks(selected),
                          label("GRPR spinal neurons", LEFT_X, 2.26, PURPLE, 29),
                          *old_rows, study("Sun et al., 2009"))
        self.add(previous)
        self.at("In 2020")
        self.play(FadeOut(previous), run_time=.57)
        citation = study("Tan et al., 2020")
        self.play(FadeIn(citation), run_time=.57)
        sugar_spout, ace_spout = spout(-4.76, ORANGE), spout(-2.21, TEAL, backwards=True)
        sugar_name = label("Sugar", -4.76, 2.20, ORANGE, 31, 2.52)
        ace_name = label("Acesulfame K", -2.21, 2.20, TEAL, 30, 2.52)
        self.at("colleagues offered mice")
        self.play(FadeIn(sugar_spout, shift=DOWN * .37), run_time=.58)
        self.play(FadeIn(sugar_name), FadeIn(ace_spout, shift=DOWN * .37), run_time=.73)
        self.play(FadeIn(ace_name), run_time=.53)

        clock = ValueTracker(0)
        # A qualitative time scrubber. The displayed fills encode the reported
        # equal start, a shift by 24 h and near-exclusive sugar by 48 h.
        s = ValueTracker(.50)
        a = ValueTracker(.50)

        sugar = VGroup(label("Sugar", RIGHT_X, 1.48, ORANGE, 34),
                       gauge(s, RIGHT_X, .85, ORANGE, height=.51))
        ace = VGroup(label("Acesulfame K", RIGHT_X, .08, TEAL, 32),
                     gauge(a, RIGHT_X, -.54, TEAL, height=.51))
        timeline = choice_timeline(clock)
        self.at("equally attractive at first")
        self.play(FadeIn(sugar), FadeIn(ace), run_time=.67)
        self.play(FadeIn(timeline), run_time=.81)
        self.at("Preference shifted within")
        self.play(clock.animate.set_value(24), s.animate.set_value(.70), a.animate.set_value(.30),
                  run_time=2.10, rate_func=linear)
        self.at("By 48 hours")
        self.play(clock.animate.set_value(48), s.animate.set_value(.96), a.animate.set_value(.04),
                  run_time=1.18, rate_func=linear)
        self.at("even mice unable")
        self.play(FadeOut(VGroup(sugar_spout, ace_spout, sugar_name, ace_name)), run_time=.52)
        taste = taste_icon()
        self.play(FadeIn(taste), run_time=.66)
        self.at("In this assay")
        learned = label("Learned preference", LEFT_X, 2.23, GREEN, 32)
        self.play(FadeIn(learned), highlight_gauge(sugar[1], ORANGE), run_time=1.58)
        self.at("sweet taste signaling")
        self.play(Indicate(taste[3], color=RED, scale_factor=1.09), run_time=1.12)
        self.at("Across every test")
        self.play(FadeOut(VGroup(learned, taste, citation, sugar, ace, timeline)), run_time=.46)
        badges = [
            boxed_label("Two threat outputs", PURPLE, size=28, pad=.14).move_to(point(RIGHT_X, 1.55)),
            boxed_label("Itch and pain", YELLOW, size=28, pad=.14).move_to(point(RIGHT_X, .48)),
            boxed_label("Learned sugar preference", ORANGE, size=28, pad=.14).move_to(point(RIGHT_X, -.59)),
        ]
        self.play(LaggedStart(*[FadeIn(b, shift=UP * .15) for b in badges], lag_ratio=.52), run_time=2.36)
        self.at("trustworthy evidence")
        rule = caption("Animal actions need sharp controls", size=34, color=GREEN)
        self.play(FadeIn(rule), run_time=.71)
        self.finish()


class S11End(EndCard):
    LINE = "Behavioural assays measure actions; controls and circuit tests separate their causes."
