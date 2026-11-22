"""Electrical microstimulation and sensory prostheses, timed to the supplied narration.

Colour map from the patch-clamp film: blue = apparatus, grey = anatomy,
purple = neurons, yellow = current or spikes, green = observed responses,
red = damage or interference, gold = questions and conclusions.
"""

from bp_parts import *  # noqa: F403

PURPLE = "#B58CD9"
NEURAL_PANEL = "#27344A"
RESPONSE_PANEL = "#192130"
LEFT_X, RIGHT_X = -3.3, 3.3
CONTACTS = 22
MODEL_LENGTH, FIELD_WIDTH = 16, 1.75
PACKED_COUNT = int(MODEL_LENGTH / FIELD_WIDTH)
X_MIN, X_MAX = -5.85, -0.75
FIBRE_X = np.linspace(-5.66, -0.94, 7)
FIBRE_BOTTOM = -1.99
QUESTION = "How many separate\nchannels?"
END_LINE = "Stimulation tests cause only as finely as it drives distinct neurons."


def point(x, y):
    return np.array([x, y, 0.0])


def label(text, x, y, color=TEXT, size=30, max_w=5.55):
    return fit_text(text, max_w=max_w, size=size, min_size=28, color=color).move_to(point(x, y))


def world(left="Neuron groups", right="Perception and behaviour"):
    panels = TwoPanel(left, right, colors=(PURPLE, GREEN), top=3.2, bottom=-2.6, size=31)
    panels.left_frame.set_fill(NEURAL_PANEL, 1)
    panels.right_frame.set_fill(RESPONSE_PANEL, 1)
    return panels


def diagram_tag():
    return scope_tag("Schematic", size=28).shift(UP * 0.14)


def poly(points, color, width, opacity=1):
    return VMobject().set_points_as_corners(points).set_stroke(color, width, opacity)


def nerve_path(x, y):
    return point(x + 0.13 * np.sin((y + 2.1) * 2.6), y)


def fibres(mode="brain"):
    top = {"brain": 0.75, "ear": -0.28, "eye": 0.40, "toy": -0.19}[mode]
    paths = VGroup()
    for x in FIBRE_X:
        soma = Ellipse(width=0.33, height=0.45, color=PURPLE, fill_opacity=0.65, stroke_width=2)
        soma.move_to(nerve_path(x, top))
        axon = poly([nerve_path(x, y) for y in np.linspace(top - 0.16, FIBRE_BOTTOM, 40)], PURPLE, 5, 0.66)
        fork = VGroup(*[Line(nerve_path(x, FIBRE_BOTTOM + 0.34),
                             nerve_path(x, FIBRE_BOTTOM) + RIGHT * offset,
                             color=PURPLE, stroke_width=2.5, stroke_opacity=0.65)
                        for offset in (-0.22, 0.22)])
        paths.add(VGroup(axon, fork, soma))
    return paths


def travelling_spikes(indices, rate, top):
    """Identical packets travel down each recruited fibre, with their spacing set by rate."""
    packets = VGroup()
    for index in indices:
        for copy in range(6):
            packet = RoundedRectangle(width=0.23, height=0.43, corner_radius=0.11,
                                      stroke_width=0, fill_color=YELLOW, fill_opacity=1)
            packet.phase = (copy + index * 0.23) / 6

            def travel(mob, dt, x=FIBRE_X[index], number=copy):
                frequency = rate.get_value()
                mob.phase = (mob.phase + dt * 0.61) % 1
                fraction = (mob.phase + number * (1 / max(frequency, 1) - 1 / 6)) % 1
                y = top + fraction * (FIBRE_BOTTOM - top)
                mob.move_to(nerve_path(x, y))
                fade = min(1, 12 * fraction, 12 * (1 - fraction))
                mob.set_fill(opacity=fade * np.clip(frequency - number, 0, 1))

            travel(packet, 0)
            packets.add(packet.add_updater(travel))
    return packets


def probe(active=False):
    body = Polygon(point(-3.9, 2.30), point(-2.72, 2.30), point(-3.19, 1.06),
                   point(-3.42, 1.06), stroke_color=BLUE, stroke_width=4,
                   fill_color=BLUE, fill_opacity=0.21 if active else 0.10)
    tip = Line(point(-3.3, 1.22), point(-3.3, 0.94), stroke_width=6, color=YELLOW if active else BLUE)
    return VGroup(body, tip)


def dot_cloud(y_range=(-1.43, 1.57)):
    rng = np.random.default_rng(54)
    dots = VGroup()
    for i in range(46):
        phase, y = rng.random(), rng.uniform(*y_range)
        d = Dot(radius=rng.uniform(0.035, 0.075), color=GREEN).set_opacity(rng.uniform(0.48, 0.92))
        d.phase = phase
        speed = 0.14 if i % 4 else -0.09

        def drift(mob, dt, y=y, speed=speed):
            mob.phase = (mob.phase + dt * speed) % 1
            mob.move_to(point(1.04 + 4.53 * mob.phase, y))

        drift(d, 0)
        dots.add(d.add_updater(drift))
    return dots


def choice_arrow():
    return Arrow(point(2.0, 0.10), point(5.12, 0.10), buff=0, color=GREEN,
                 stroke_width=10, tip_length=0.38)


def cochlea_point(t):
    angle = 1.12 * TAU * t - 0.40
    radius = 1 - 0.80 * t
    return point(LEFT_X - 0.3 + 2.52 * radius * np.cos(angle),
                 1.05 + 1.16 * radius * np.sin(angle))


def cochlea():
    points = [cochlea_point(t) for t in np.linspace(0, 1, 165)]
    wall = poly(points, GREY, 43, 0.32)
    channel = poly(points, NEURAL_PANEL, 29)
    hairs = VGroup()
    for t in np.linspace(0.13, 0.75, 12):
        marks = VGroup(*[Line(cochlea_point(t) + point(dx - 0.045, -0.34),
                               cochlea_point(t) + point(dx + 0.045, -0.21),
                               color=RED, stroke_width=3) for dx in (-0.07, 0.07)])
        hairs.add(marks)
    return VGroup(wall, channel), hairs


def array(mode="ear", count=0, reach=1.0):
    if mode == "ear":
        path = cochlea_point
    else:
        path = lambda t: point(X_MIN + (X_MAX - X_MIN) * t, 1.02)
    rail = poly([path(t) for t in np.linspace(0, reach, 100)], BLUE, 7, 0.72)
    active = set(np.linspace(0, CONTACTS - 1, count).round().astype(int)) if count else set()
    contacts = VGroup(*[Dot(path(t), radius=0.079 if mode == "ear" else 0.080,
                            color=YELLOW if i in active else BLUE,
                            stroke_color=NEURAL_PANEL, stroke_width=1.8)
                        for i, t in enumerate(np.linspace(0, reach, CONTACTS))])
    return VGroup(rail, contacts)


def retina():
    sheet = RoundedRectangle(width=5.25, height=0.64, corner_radius=0.17, color=GREY,
                             fill_color=GREY, fill_opacity=0.22, stroke_width=2)
    sheet.move_to(point(LEFT_X, 0.65))
    rows = VGroup()
    for y in (1.05, 1.37, 1.69):
        row = Line(point(-5.7, y), point(-0.9, y), color=BLUE, stroke_width=3.5)
        rows.add(row, *[Dot(point(x, y), radius=0.078, color=BLUE)
                        for x in np.linspace(-5.7, -0.9, 11)])
    return sheet, rows


def field(x, y, width, height, color=YELLOW, opacity=0.24):
    return Ellipse(width=width, height=height, stroke_color=color, stroke_width=3,
                   fill_color=color, fill_opacity=opacity).move_to(point(x, y))


def fading_field(x, y, width, height):
    layers = VGroup()
    for scale in np.linspace(1.5, 0.14, 15):
        # Concentric samples of a Gaussian falloff, feathered towards the outer edge.
        alpha = 0.08 * np.exp(-2.2 * scale**2)
        layers.add(field(x, y, width * scale, height * scale, opacity=alpha).set_stroke(width=0))
    return layers


def bracket(x0, x1, y, color):
    return VGroup(Line(point(x0, y), point(x1, y), color=color, stroke_width=3),
                  *[Line(point(x, y - 0.10), point(x, y + 0.10), color=color, stroke_width=3)
                    for x in (x0, x1)])


def model_x(mm):
    return X_MIN + mm * (X_MAX - X_MIN) / MODEL_LENGTH


MODEL_FIELD_X = model_x(MODEL_LENGTH * 10 / (CONTACTS - 1))
MODEL_FIELD_SPAN = model_x(FIELD_WIDTH) - model_x(0)


def model_labels():
    return VGroup(label("22 contacts", LEFT_X, 1.98, BLUE),
                  label("16 mm", LEFT_X, 1.53, BLUE),
                  label("1.75 mm (illustrative)", LEFT_X, -2.27, YELLOW))


def model_measurements():
    return VGroup(bracket(X_MIN, X_MAX, 1.28, BLUE),
                  bracket(MODEL_FIELD_X - MODEL_FIELD_SPAN / 2,
                          MODEL_FIELD_X + MODEL_FIELD_SPAN / 2, -1.88, YELLOW))


def model_field():
    return field(MODEL_FIELD_X, -0.35, MODEL_FIELD_SPAN, 2.80)


def charge(halo, strength, speed=2.0):
    """Make the applied field visibly build and relax while its width stays fixed."""
    halo.phase = 0.0

    def vary(mob, dt):
        mob.phase += speed * dt
        glow = (1 - np.cos(mob.phase)) / 2
        mob.set_fill(opacity=0.24 + strength * glow)
        mob.set_stroke(width=3 + 3 * glow)

    return halo.add_updater(vary)


def model_source():
    return Dot(point(MODEL_FIELD_X, 1.02), radius=0.11, color=YELLOW)


def predict_card():
    card = question_card(QUESTION, size=43, max_w=5.15)
    return card.move_to(point(RIGHT_X, 0.20))


def packing_guide():
    """Show the available length and one field-width unit without revealing the count."""
    width = 4.70
    available = RoundedRectangle(width=width, height=0.65, corner_radius=0.08,
                                 stroke_color=BLUE, stroke_width=3,
                                 fill_color=BLUE, fill_opacity=0.73).move_to(point(RIGHT_X, -1.18))
    unit = RoundedRectangle(width=width * FIELD_WIDTH / MODEL_LENGTH, height=0.65,
                            corner_radius=0.07, stroke_color=YELLOW, stroke_width=3,
                            fill_color=YELLOW, fill_opacity=0.90)
    unit.move_to(available).align_to(available, LEFT)
    return VGroup(available, unit)


def sound_plot():
    return Plot(box=(0.92, 5.77, -1.55, 1.72), xr=(0, 1), yr=(-1, 1), stroke=2)


def speech_wave(t, clarity=0):
    """Schematic harmonics with a clipped envelope for the initial robotic percept."""
    envelope = 0.49 + 0.26 * np.sin(TAU * 3 * t) ** 2
    voice = np.sin(TAU * 8 * t)
    harsh = np.clip(0.77 * voice + 0.29 * np.sin(TAU * 21 * t), -0.55, 0.55)
    return envelope * (clarity * voice + (1 - clarity) * harsh) * 1.38


def sweeping_wave(plot, clarity):
    """A full waveform sweeps through the perception window, with no numerical scale."""
    trace = plot.curve(lambda t: speech_wave(t, clarity.get_value()), color=GREEN, width=5, n=240)
    trace.phase = 0.0

    def advance(mob, dt):
        mob.phase += 0.17 * dt
        x = np.linspace(0, 1, 240)
        mob.set_points_as_corners([plot.pt(t, speech_wave(t + mob.phase, clarity.get_value())) for t in x])

    return trace.add_updater(advance)


class S01Hook(SpokenScene):
    def construct(self):
        rate = ValueTracker(1.6)
        self.add(world(), fibres(), probe(), dot_cloud(), diagram_tag())
        self.add(travelling_spikes([3], rate, 0.72))
        self.at("fires faster")
        self.play(rate.animate.set_value(3.7), run_time=2.25)
        question = label("Causes choice?", RIGHT_X, 1.95, GOLD, size=39)
        self.at("does it cause it")
        self.play(FadeIn(question), run_time=0.46)
        self.at("moves its eyes")
        self.play(GrowArrow(choice_arrow()), run_time=0.8)
        self.at("on average")
        self.play(rate.animate.set_value(6), run_time=4.35)
        self.at("recording spikes alone")
        mark = T("?", 87, GOLD, weight=BOLD).move_to(point(RIGHT_X, -0.84))
        self.play(GrowFromCenter(mark), run_time=0.58)
        bob(mark, amp=0.07, speed=2.5)
        self.finish()


class S02Title(TitleCard):
    TITLE = "Driving Neurons to Test What They Cause"
    LESSON = "Electrical microstimulation"

    def construct(self):
        panels = world()
        panels.remove(panels.left_head, panels.right_head)
        background = VGroup(panels, fibres(), probe(), dot_cloud(),
                            travelling_spikes([3], ValueTracker(4), 0.72))
        shade = Rectangle(width=13.2, height=7.3, stroke_width=0, fill_color=BG, fill_opacity=0.70)
        title = fit_text(self.TITLE, max_w=11.8, size=52, min_size=36, font=TITLE_FONT)
        lesson = T(self.LESSON, size=28, color=BLUE)
        rule = Line(LEFT * 1.05, RIGHT * 1.05, color=GOLD, stroke_width=4)
        card = VGroup(lesson, title, rule).arrange(DOWN, buff=0.30)
        backing = Rectangle(width=12.7, height=2.42, stroke_width=0, fill_color=BG, fill_opacity=1)
        self.add(background, shade, backing)
        self.play(FadeIn(card), run_time=0.35)
        self.wait(2.0 - self.elapsed())


class S03Method(SpokenScene):
    def construct(self):
        rate = ValueTracker(2)
        electrode = probe()
        anatomy = fibres()
        self.add(world(right="Stimulation"), anatomy, electrode, diagram_tag())
        self.add(travelling_spikes([3], rate, 0.72))
        self.at("only listening")
        self.play(Transform(electrode, probe(active=True)), run_time=0.65)
        self.at("activate neurons")
        evoked_field = field(LEFT_X, 0.20, 2.34, 2.35, opacity=0.34)
        self.play(rate.animate.set_value(4), anatomy[3][2].animate.set_fill(YELLOW, opacity=0.85),
                  GrowFromCenter(evoked_field), run_time=2.50)
        spark = Line(point(-3.3, 1.05), point(-3.3, 0.81), color=YELLOW, stroke_width=10)
        self.at("small currents")
        self.play(Create(spark), evoked_field.animate.stretch(0.65, 0), run_time=0.60)
        self.play(FadeOut(evoked_field, scale=1.55), run_time=0.76)
        arcs = VGroup(*[Arc(radius=r, start_angle=0.30, angle=PI - 0.60,
                            arc_center=point(RIGHT_X, -0.55), color=BLUE,
                            stroke_width=5, stroke_opacity=opacity)
                        for r, opacity in ((0.72, 1), (1.18, 0.75), (1.63, 0.5), (2.08, 0.27))])
        self.at("magnetic pulses")
        self.play(LaggedStart(*[Create(a) for a in arcs], lag_ratio=0.22), run_time=1.9)
        magnetic = label("Magnetic pulse", RIGHT_X, -1.21, BLUE)
        self.play(FadeIn(magnetic), run_time=0.4)
        self.at("every sense")
        self.play(FadeOut(arcs), FadeOut(magnetic), run_time=0.45)
        plot = Plot(box=(0.93, 5.68, -1.27, 1.25), xr=(0, 1), yr=(0, 1), stroke=2)
        spike_fn = lambda t: 0.11 + 0.77 * max(0, 1 - abs((t * 5) % 1 - 0.50) / 0.14)
        trace = plot.curve(spike_fn, color=YELLOW, n=360)
        self.play(Create(trace), run_time=2.45)
        self.at("spike rate")
        recruited = travelling_spikes([2, 4, 5], rate, 0.72)
        self.add(recruited)
        faster_trace = plot.curve(
            lambda t: 0.11 + 0.77 * max(0, 1 - abs((t * 8) % 1 - 0.50) / 0.14),
            color=YELLOW, n=360)
        self.play(rate.animate.set_value(6), Transform(trace, faster_trace), run_time=1.55)
        self.at("how much")
        self.play(FadeIn(label("How much", RIGHT_X, -1.75, YELLOW, size=35)), run_time=0.38)
        self.finish()


class S04Prosthesis(SpokenScene):
    def construct(self):
        panels = world(right="Hearing")
        anatomy = fibres()
        coil, hairs = cochlea()
        electrode = probe(active=True)
        contacts = array()
        self.add(panels, anatomy, electrode, diagram_tag())
        self.at("a cochlear implant")
        self.play(Transform(anatomy, fibres("ear")), Create(coil), run_time=2.1)
        self.at("threading electrode contacts")
        self.play(FadeOut(electrode), Create(contacts[0]), run_time=1.75)
        self.play(LaggedStart(*[FadeIn(contact) for contact in contacts[1]], lag_ratio=0.075), run_time=1.58)
        cochlea_label = label("Cochlea", RIGHT_X, 0.4, TEXT, size=42)
        self.at("hearing coil")
        self.play(FadeIn(cochlea_label), run_time=0.45)
        self.at("skips damaged hair cells")
        self.play(FadeIn(hairs), FadeOut(cochlea_label), run_time=0.8)
        bypass = VGroup(*[CubicBezier(cochlea_point(t), cochlea_point(t) + DOWN * 0.33,
                                     nerve_path(FIBRE_X[i], 0.45), nerve_path(FIBRE_X[i], -0.08),
                                     color=YELLOW, stroke_width=8)
                          for t, i in ((0.35, 1), (0.52, 3), (0.10, 5))])
        self.play(hairs.animate.set_opacity(0.36), LaggedStart(*[Create(c) for c in bypass], lag_ratio=0.23),
                  run_time=1.65)
        self.at("excites the auditory nerve")
        self.add(travelling_spikes([1, 3, 5], ValueTracker(4.2), -0.29))
        self.play(Transform(contacts[1], array(count=8)[1]), FadeOut(bypass), run_time=0.7)
        nerve_label = label("Auditory nerve", RIGHT_X, 0.4, PURPLE, size=37)
        self.play(FadeIn(nerve_label), run_time=0.5)
        self.at("speech often sounds", lead=0.45)
        self.play(FadeOut(nerve_label), run_time=0.35)
        clarity = ValueTracker(0)
        plot = sound_plot()
        wave = sweeping_wave(plot, clarity)
        wave.suspend_updating()
        self.play(Create(wave), run_time=0.9)
        wave.resume_updating()
        self.at("at first")
        self.play(FadeIn(label("At first", RIGHT_X, -1.8, GREEN, size=35)), run_time=0.45)
        self.at("22 contacts")
        self.play(FadeIn(label("22 contacts", LEFT_X, -2.32, BLUE, size=29)), run_time=0.6)
        self.finish()


class S05GuidingIdea(SpokenScene):
    def construct(self):
        coil, hairs = cochlea()
        contacts = array(count=8)
        anatomy = fibres("ear")
        sheet, grid = retina()
        self.add(world(right="Visual percept"), anatomy, coil, contacts, hairs.set_opacity(0.36), diagram_tag())
        self.at("in the eye")
        self.play(FadeOut(hairs), Transform(anatomy, fibres("eye")),
                  ReplacementTransform(coil, sheet), ReplacementTransform(contacts, grid.shift(UP * 0.29)),
                  run_time=2.1)
        self.play(grid.animate.shift(DOWN * 0.29), run_time=1.42)
        retina_label = label("Retina", LEFT_X, -2.30, PURPLE)
        self.at("inner surface")
        self.play(FadeIn(retina_label), run_time=0.42)
        source = Dot(point(LEFT_X, 1.37), radius=0.13, color=YELLOW)
        halo = field(LEFT_X, 0.42, 0.68, 1.74)
        target = field(RIGHT_X, 0.28, 0.6, 0.6, GREEN, 0.75)
        self.at("asked to draw")
        self.play(FadeIn(source), GrowFromCenter(halo), GrowFromCenter(target), run_time=1.6)
        streak = field(RIGHT_X + 0.24, 0.20, 2.95, 0.53, GREEN, 0.65).rotate(0.36)
        self.at("drew elongated")
        self.play(Transform(target, streak), run_time=2.1)
        self.at("current spread")
        self.play(Transform(halo, field(LEFT_X + 0.28, 0.12, 2.65, 2.84)), run_time=2.2)
        self.at("wrong neurons")
        self.play(halo.animate.shift(RIGHT * 0.59), target.animate.shift(RIGHT * 0.65 + DOWN * 0.47),
                  run_time=1.9)
        self.at("drives distinct groups", lead=0.55)
        distinct = VGroup(*[field(FIBRE_X[i], -0.25, 0.59, 2.59, c, 0.20)
                            for i, c in ((1, BLUE), (3, YELLOW), (5, PURPLE))])
        self.play(ReplacementTransform(halo, distinct), FadeOut(target), run_time=1.4)
        self.add(travelling_spikes([1, 3, 5], ValueTracker(3.4), 0.38))
        self.finish()


class S06PredictQ(SpokenScene):
    def construct(self):
        sheet, grid = retina()
        anatomy = fibres("eye")
        contacts = array("toy")
        labels, widths = model_labels(), model_measurements()
        self.add(world(right="Toy case"), anatomy, sheet, grid, diagram_tag())
        self.at("try a toy case")
        self.play(FadeOut(sheet), ReplacementTransform(grid, contacts),
                  Transform(anatomy, fibres("toy")), run_time=1.90)
        self.at("22 contacts")
        self.play(FadeIn(labels[0]), run_time=0.45)
        self.play(LaggedStart(*[Indicate(c, color=YELLOW, scale_factor=1.75) for c in contacts[1]],
                              lag_ratio=0.14), run_time=1.02)
        source = model_source()
        self.at("about 16")
        span = Rectangle(width=X_MAX - X_MIN, height=0.63, stroke_width=0,
                         fill_color=BLUE, fill_opacity=0.84).move_to(point(LEFT_X, 0.58))
        self.play(GrowFromEdge(span, LEFT), Create(widths[0]), FadeIn(labels[1]), run_time=1.48)
        self.play(FadeOut(span), run_time=1.12)
        tiny = field(MODEL_FIELD_X, 0.59, 0.19, 0.48)
        self.at("electric field")
        self.play(FadeIn(source), GrowFromCenter(tiny), run_time=0.52)
        halo = model_field()
        self.play(ReplacementTransform(tiny, halo), run_time=2.28)
        self.at(".75 millimeters", lead=0.2)
        self.play(Create(widths[1]), FadeIn(labels[2]), run_time=0.80)
        self.at("roughly how many")
        self.play(FadeIn(predict_card()), run_time=0.60)
        charge(halo, strength=0.58, speed=2.75)
        guide = packing_guide()
        self.at("fit before fields", lead=0)
        self.play(GrowFromEdge(guide[0], LEFT), FadeIn(guide[1]),
                  run_time=self.narration_s + 0.39 - self.elapsed(), rate_func=linear)
        self.finish()


class S07PredictPause(Scene):
    def construct(self):
        self.camera.background_color = BG
        halo = model_field()
        pulse(halo, base=3, amp=0.65, speed=2.1)
        self.add(world(right="Toy case"), fibres("toy"), array("toy"), model_labels(), model_measurements(),
                 halo, model_source(), predict_card(), packing_guide(), diagram_tag())
        self.wait(4.5)


class S08MathInteraction(SpokenScene):
    def construct(self):
        labels, widths = model_labels(), model_measurements()
        halo = model_field()
        source = model_source()
        self.add(world(right="Toy case"), fibres("toy"), array("toy"), labels, widths,
                 halo, source, diagram_tag())
        formula_right = label("Length ÷ field width", RIGHT_X, 0.69, GOLD, size=43)
        self.at("length divided")
        charge(halo, strength=0.69, speed=2.9)
        self.play(FadeIn(formula_right), run_time=0.58)
        whole = bracket(1.0, 5.6, 0.14, BLUE)
        self.play(Create(whole), run_time=1.68)
        self.at("rough channel count")
        unit_span = 4.6 * FIELD_WIDTH / MODEL_LENGTH
        unit = bracket(1.0, 1.0 + unit_span, -0.22, YELLOW)
        self.play(Create(unit), run_time=0.48)
        self.play(unit.animate.shift(RIGHT * unit_span * 2), run_time=1.56)
        first = label("16 mm ÷ field width", RIGHT_X, 0.69, GOLD, size=35)
        self.at("16 mm divided")
        self.play(swap(formula_right, first), run_time=0.60)
        second = label("16 mm ÷ 1.75 mm", RIGHT_X, 0.69, GOLD, size=36)
        self.at("1 .75 mm")
        self.play(swap(first, second), run_time=0.65)
        result = label(f"≈ {PACKED_COUNT} channels", RIGHT_X, -0.85, GOLD, size=51)
        centers = [model_x((MODEL_LENGTH - PACKED_COUNT * FIELD_WIDTH) / 2 + (i + 0.5) * FIELD_WIDTH)
                   for i in range(PACKED_COUNT)]
        packed = VGroup(*[field(x, -0.35, MODEL_FIELD_SPAN, 2.8) for x in centers])
        self.at("about 9")
        self.play(FadeOut(halo), FadeOut(source), widths[1].animate.set_x(centers[PACKED_COUNT // 2]),
                  LaggedStart(*[FadeIn(f) for f in packed], lag_ratio=0.11), FadeIn(result), run_time=1.30)
        count = label("22 contacts", RIGHT_X, -1.95, BLUE, size=34)
        self.at("fewer than 22")
        self.play(FadeIn(count), run_time=0.47)
        self.at("overlapping fields excite")
        spread = VGroup(*[field(x, -0.35, MODEL_FIELD_SPAN * 1.57, 2.8) for x in centers])
        self.play(FadeOut(widths[1]), FadeOut(labels[2]), run_time=0.24)
        self.play(Transform(packed, spread), run_time=1.36)
        self.add(travelling_spikes(range(7), ValueTracker(3.5), -0.23))
        interaction = label("Channel interaction", RIGHT_X, 0.69, YELLOW, size=34)
        self.at("channel interaction")
        self.play(swap(second, interaction), FadeOut(result), FadeOut(count), FadeOut(whole),
                  FadeOut(unit), run_time=0.68)
        toy = label("Toy packing", RIGHT_X, -0.87, GOLD, size=34)
        self.at("a toy picture")
        self.play(FadeIn(toy), run_time=0.53)
        self.at("real fields fade gradually")
        fades = VGroup(*[fading_field(x, -0.35, MODEL_FIELD_SPAN * 1.57, 2.8) for x in centers])
        self.play(FadeOut(packed), FadeIn(fades), run_time=1.55)
        self.finish()


class S09Controls(SpokenScene):
    def construct(self):
        anatomy, contacts = fibres("ear"), array(count=8)
        coil, _ = cochlea()
        badge = boxed_label("22 contacts", BLUE, size=31).move_to(point(RIGHT_X, 0.25))
        self.add(world(right="Measured in listeners"), anatomy, coil, contacts, badge, diagram_tag())
        self.add(travelling_spikes([1, 3, 5], ValueTracker(3.3), -0.30))
        self.at("must measure")
        progress = ValueTracker(0.16)
        gauge = dial(progress, point(RIGHT_X, -0.1), radius=1.7, color=GREEN, fmt="")
        gauge.remove(gauge[3])
        outcome = label("What the user\ntells apart", RIGHT_X, -1.35, GREEN, size=34)
        self.play(FadeOut(badge), run_time=0.35)
        self.play(FadeIn(gauge), FadeIn(outcome), progress.animate.set_value(0.69), run_time=2.45)
        self.at("no single channel count")
        self.play(progress.animate.set_value(0.42), run_time=2.65)
        factor = label("Neural survival", LEFT_X, -2.32, PURPLE)
        self.at("neural survival")
        self.play(anatomy[0].animate.set_opacity(0.22), anatomy[6].animate.set_opacity(0.22),
                  FadeIn(factor), run_time=0.78)
        distance = label("Contact-to-neuron distance", LEFT_X, -2.32, BLUE)
        canal_offset = UP * 0.075
        self.at("the distance from contacts")
        self.play(contacts.animate.shift(canal_offset), swap(factor, distance), run_time=1.62)

        def shorten_array(mob, alpha):
            # Resample the canal at every frame so the rail follows the bend as it retracts.
            mob.become(array(count=8, reach=1 - 0.35 * alpha).shift(canal_offset * (1 - alpha)))

        reach = label("Array reach", LEFT_X, -2.32, BLUE)
        self.at("the arrays reach")
        self.play(UpdateFromAlphaFunc(contacts, shorten_array), swap(distance, reach), run_time=1.72)
        weeks = label("Weeks to months", RIGHT_X, -1.92, GOLD)
        track = Line(point(1.34, -2.25), point(5.26, -2.25), color=GREY, stroke_width=6, stroke_opacity=0.40)
        fill = always_redraw(lambda: Line(track.get_start(), track.point_from_proportion(progress.get_value()),
                                          color=GREEN, stroke_width=6))
        self.at("many users also understand")
        clarity = label("Speech clarity", RIGHT_X, -1.18, GREEN, size=33)
        self.play(swap(outcome, clarity), FadeOut(reach), FadeIn(track), FadeIn(fill), run_time=0.56)
        self.play(progress.animate.set_value(0.70), run_time=1.61)
        self.at("weeks to months", lead=0.58)
        self.play(FadeIn(weeks), progress.animate.set_value(0.90), run_time=1.15)
        self.finish()


class S10UnlockedPlateau(SpokenScene):
    def construct(self):
        contacts = array(count=8)
        coil, _ = cochlea()
        self.add(world(right="Speech recognition"), fibres("ear"), coil, contacts, diagram_tag())
        self.add(travelling_spikes([1, 3, 5], ValueTracker(3.3), -0.29))
        self.at("switching channels")
        for n in (14, 6, 10):
            self.play(Transform(contacts[1], array(count=n)[1]), run_time=0.91)
        study = label("Berg and colleagues, 2020", RIGHT_X, 1.97, TEXT)
        cohort = label("18 adults", RIGHT_X, 1.48, BLUE)
        self.at("berg and colleagues")
        self.play(FadeIn(study), run_time=0.46)
        self.at("18 adult")
        self.play(FadeIn(cohort), run_time=0.49)
        plot = Plot(box=(1.12, 5.61, -1.66, 1.00), xr=(0, 16), yr=(0, 1),
                    xlabel="Active channels", label_size=28)
        start, end = 8, 10

        def recognition(n):
            # Normalized schematic: the onset of the reported 8–10 plateau anchors this guide.
            fraction = min(n / start, 1.0)
            return 0.12 + 0.69 * (2 * fraction - fraction**2)

        curve = plot.curve(recognition, color=GREEN)
        plateau = plot.curve(recognition, x0=start, x1=end, color=YELLOW, width=9, n=20)
        self.at("speech recognition", lead=1.15)
        self.play(FadeIn(plot), run_time=0.44)
        self.play(Create(curve), run_time=2.15)
        self.at("8 to 10 channels", lead=0.6)
        self.play(Create(plateau), FadeIn(label("8–10", 3.66, 0.76, YELLOW, size=32)), run_time=0.65)
        self.finish()


class S11UnlockedNoise(SpokenScene):
    def construct(self):
        contacts = array(count=20)
        coil, _ = cochlea()
        self.add(world(right="Speech-in-noise threshold"), fibres("ear"), coil, contacts, diagram_tag())
        self.add(travelling_spikes([1, 3, 5], ValueTracker(4.1), -0.29))
        self.at("extra contacts")
        highlight = boxed_label("20 active electrodes", BLUE, size=30).move_to(point(RIGHT_X, -0.45))
        self.play(FadeIn(highlight), run_time=0.64)
        citation = label("Schvartz-Leyzac, Zwolan\nand Pfingst, 2017", RIGHT_X, 1.72, TEXT, size=29)
        self.at("in 2017")
        self.play(FadeIn(citation), run_time=0.65)
        self.at("cut active electrodes")
        reduced = label("20 → 8 active electrodes", LEFT_X, -2.31, BLUE, size=29)
        self.play(Transform(contacts[1], array(count=8)[1]), FadeOut(highlight),
                  run_time=1.20)
        self.play(FadeIn(reduced), run_time=0.54)
        self.at("7 adults")
        self.play(FadeIn(label("7 adults", RIGHT_X, 0.95, BLUE)), run_time=0.45)
        noise_level = ValueTracker(0.13)
        xp = Plot(box=(1.0, 5.62, -1.87, 0.57), xr=(0, 1), yr=(0, 2.5))
        noise = always_redraw(lambda: xp.curve(
            lambda t: 0.35 + noise_level.get_value() * (0.65 * np.sin(TAU * 27 * t)
                                                        + 0.27 * np.sin(TAU * 63 * t)),
            color=RED, width=3, n=300))
        self.at("their speech")
        self.add(noise)
        baseline = label("Background noise", RIGHT_X, -2.15, RED)
        self.play(noise_level.animate.set_value(0.28), FadeIn(baseline), run_time=0.95)
        required = ValueTracker(0.98)
        speech = always_redraw(lambda: xp.curve(
            lambda t: required.get_value() + 0.23 * np.sin(TAU * 6 * t)
            * (0.62 + 0.33 * np.sin(TAU * 2 * t)), color=GREEN, width=5))
        self.at("threshold worsened")
        self.add(speech)
        self.play(FadeIn(label("Speech", RIGHT_X, 0.39, GREEN)), run_time=0.42)
        self.at("be louder relative")
        self.play(required.animate.set_value(1.74), run_time=2.55)
        self.finish()


class S12Close(SpokenScene):
    def construct(self):
        active = [1, 3, 5]
        halos = VGroup(*[field(FIBRE_X[i], -0.27, 2.42, 3.24) for i in active])
        probes = VGroup(*[probe(active=True).shift(RIGHT * (FIBRE_X[i] - LEFT_X)) for i in active])
        self.add(world(), fibres(), halos, probes, diagram_tag())
        self.add(travelling_spikes(active, ValueTracker(4), 0.68))
        self.at("acts independently")
        self.play(halos.animate.shift(RIGHT * 0.11), run_time=1.72)
        dots = dot_cloud(y_range=(0.42, 1.12))
        self.at("probing a decision")
        self.add(dots)
        self.play(GrowArrow(choice_arrow().shift(UP * 1.45)), run_time=0.94)
        waveform = sound_plot().curve(speech_wave, color=GREEN, width=5, n=220)
        waveform.stretch(0.48, 1).move_to(point(RIGHT_X, -0.92))
        self.at("restoring a sense")
        self.play(Create(waveform), run_time=1.17)
        separate = VGroup(*[field(FIBRE_X[i], -0.27, 0.56, 3.24, c, 0.23)
                            for i, c in zip(active, (BLUE, YELLOW, PURPLE))])
        self.at("as precise as")
        self.play(Transform(halos, separate), run_time=3.15)
        self.at("behavior then shows")
        self.play(FadeIn(label("Observe behaviour", RIGHT_X, -1.96, GREEN, size=34)), run_time=0.62)
        self.finish()


class S13End(EndCard):
    LINE = END_LINE
