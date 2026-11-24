"""One hearing chain, from the sound in the canal to the brainstem response.

COLOR MAP, shared with the patch-clamp film:
GREY = anatomy; BLUE = apparatus and voltage; PURPLE = transduction channels;
YELLOW = moving signal and current; GREEN = threshold pass and living control;
RED = intense noise and contact loss; ORANGE = incoming cations; GOLD = questions.
PINK = ribbon synapses and vesicles; MINT = prestin.
"""
from bp_parts import *

PURPLE = "#B58CD9"
ORANGE = "#F29E4C"
RIBBON = "#F3A7C4"
PRESTIN = "#91DFBE"
TISSUE = "#354454"
DARK_TISSUE = "#263645"
FLUID = "#193F4A"

QUESTION = "Normal threshold = intact ribbon synapses?"
CARD = dict(y=-2.92, size=36, color=TEXT, max_w=11.7)


def xy(x, y):
    return np.array([x, y, 0.0])


def poly(points, color=YELLOW, width=5):
    """Polyline helper from the patch-clamp film, also used for computed traces."""
    return VMobject(stroke_color=color, stroke_width=width).set_points_as_corners(
        [xy(x, y) for x, y in points]
    )


def contour(points, color=GREY, fill=TISSUE):
    return VMobject(stroke_color=color, stroke_width=3.4, fill_color=fill, fill_opacity=1).set_points_smoothly(
        [xy(x, y) for x, y in [*points, points[0]]]
    )


def capsule(w, h, x, y, edge=GREY, fill=TISSUE, stroke=3):
    return RoundedRectangle(
        width=w, height=h, corner_radius=min(w, h) * 0.36,
        stroke_color=edge, stroke_width=stroke, fill_color=fill, fill_opacity=1,
    ).move_to(xy(x, y))


def label(text, x, y, color=TEXT, size=30):
    return T(text, size, color).move_to(xy(x, y))


def stage_scope():
    return scope_tag("schematic", size=28, color=TEXT)


def travelling_dots(path, color=YELLOW, count=5, speed=0.38, size=0.09):
    """Carry signal markers through a fixed anatomy, with soft entrance and exit."""
    dots = VGroup(*[Dot(radius=size, color=color) for _ in range(count)])
    elapsed = 0.0

    def move(group, dt):
        nonlocal elapsed
        elapsed += dt
        for i, dot in enumerate(group):
            f = (elapsed * speed - i * 0.065) % 1
            dot.move_to(path(f)).set_opacity(min(1, f * 14, (1 - f) * 14))
    move(dots, 0)
    return dots.add_updater(move)


def nerve_path(f):
    return xy(3.22 + 2.37 * f, -0.18 + 0.71 * f + 0.20 * np.sin(f * np.pi))


def hearing_chain():
    """The same cutaway and landmarks at every full-chain return."""
    canal = contour([
        (-6.45, -1.92), (-6.3, -0.75), (-6.48, 0.95), (-6.06, 2.24),
        (-5.12, 2.45), (-4.43, 1.45), (-3.66, 0.76), (-3.25, 0.47),
        (-3.03, -0.24), (-3.74, -1.14), (-4.65, -1.02), (-5.46, -1.48),
    ])
    passage = contour([
        (-6.39, -0.42), (-5.58, -0.36), (-4.8, 0.18), (-3.84, 0.3),
        (-3.35, 0.16), (-3.44, -0.56), (-4.35, -0.47), (-5.31, -0.91),
        (-6.32, -1.05),
    ], color="#7E9EAE", fill=BG)
    drum = Line(xy(-3.37, 0.27), xy(-3.57, -0.68), stroke_width=5, color=GREY)
    canal = VGroup(canal, passage, drum)

    coil = contour([
        (-3.18, 0.05), (-2.99, 1.55), (-2.04, 2.48), (-0.78, 2.68),
        (0.45, 2.08), (0.77, 0.91), (0.2, -0.16), (-1.12, -0.55),
        (-2.25, -0.34), (-3.03, -0.81),
    ], fill=FLUID)
    angle = np.linspace(-2.65, -2.65 - 2.42 * np.pi, 135)
    r = np.linspace(1.46, 0.23, len(angle))
    spiral = poly(zip(-1.16 + r * np.cos(angle), 1.10 + 0.91 * r * np.sin(angle)),
                  "#86A7B1", 4)
    bed = contour([
        (-3.22, -0.63), (-1.3, -0.55), (0.15, -0.28), (2.39, -0.52),
        (2.73, -1.03), (1.34, -1.62), (-0.36, -1.74), (-2.32, -1.55),
    ], color="#62808D", fill=DARK_TISSUE)
    membrane = poly(zip(np.linspace(-3.03, 2.44, 96),
                        -0.83 + 0.26 * np.sin(np.linspace(0, np.pi, 96))), TEAL, 5)
    cochlea = VGroup(bed, coil, spiral, membrane)

    fibres = VGroup(*[
        VMobject(stroke_width=3.5, stroke_color="#7C94AA").set_points_smoothly(
            [nerve_path(f) + UP * j * (0.55 + 0.45 * f) for f in np.linspace(0, 1, 22)]
        )
        for j in (-0.37, -0.12, 0.12, 0.37)
    ])
    brain = contour([
        (4.99, 0.69), (4.62, 1.18), (4.71, 2.04), (5.58, 2.48),
        (6.27, 2.17), (6.53, 1.52), (6.19, 0.75), (5.96, 0.25),
        (5.85, -0.88), (5.98, -1.89), (5.37, -2.04), (5.14, -1.15),
        (5.22, -0.12),
    ])
    fold = VMobject(stroke_width=3, stroke_color="#71869A").set_points_smoothly(
        [xy(5.19, 1.62), xy(5.65, 1.70), xy(5.92, 1.27), xy(5.64, 0.49), xy(5.58, -0.51)]
    )
    cells = VGroup(*[
        VGroup(capsule(0.36, 1.14, x, -0.03 + 0.04 * i, fill="#45596B"),
               *[Line(xy(x + dx, 0.52 + 0.04 * i), xy(x + dx, 0.68 + 0.04 * i + dx),
                      color=GREY, stroke_width=2) for dx in (-0.11, 0, 0.11)])
        for i, x in enumerate((2.18, 2.57, 2.96))
    ])
    ribbons = VGroup(*[Dot(xy(x, -0.65 + 0.04 * i), radius=0.11, color=RIBBON)
                        for i, x in enumerate((2.18, 2.57, 2.96))])
    terminal = VMobject(stroke_width=5, stroke_color="#7C94AA").set_points_smoothly(
        [xy(2.15, -0.83), xy(2.72, -0.79), xy(3.02, -0.67), nerve_path(0)]
    )
    return VGroup(canal, cochlea, VGroup(cells, ribbons, terminal), VGroup(brain, fold, fibres))


LANDMARKS = [xy(-5.15, -0.44), xy(-1.9, -0.63), xy(2.62, -0.63), xy(5.56, 0.55)]


def probes():
    return VGroup(*[
        Circle(radius=0.24, color=YELLOW, stroke_width=3, fill_color=YELLOW, fill_opacity=0.20).move_to(p)
        for p in LANDMARKS
    ])


def signal_glow(path, color=YELLOW, speed=0.45, width=1.35, height=0.88):
    """Move the visible emphasis with the signal, within the active part of the diagram."""
    halo = VGroup(*[
        Ellipse(width=width * scale, height=height * scale, stroke_width=0, fill_color=color)
        for scale in (1.0, 0.78, 0.54)
    ])
    elapsed = 0.0

    def move(group, dt):
        nonlocal elapsed
        elapsed += dt
        f = (elapsed * speed) % 1
        power = min(1, f * 7, (1 - f) * 7)
        for oval in group:
            oval.move_to(path(f)).set_fill(opacity=0.28 * power)

    move(halo, 0)
    return halo.add_updater(move)


def sound_ripple(x0, x1, y, color, height=0.58, speed=0.45):
    """A short train of pressure crests, travelling in the selected direction."""
    crests = VGroup(*[
        Arc(angle=0.96, radius=height, start_angle=-0.48, color=color, stroke_width=5)
        for _ in range(5)
    ])
    elapsed = 0.0

    def move(group, dt):
        nonlocal elapsed
        elapsed += dt
        for i, arc in enumerate(group):
            f = (elapsed * speed - 0.11 * i) % 1
            arc.move_to(xy(x0 + f * (x1 - x0), y(f)))
            arc.set_stroke(opacity=min(1, 8 * f, 8 * (1 - f)) * (1 - i * 0.10))
    move(crests, 0)
    if x1 < x0:
        for arc in crests:
            arc.rotate(PI)
    return crests.add_updater(move)


def responsive_tissue(shape, color, strength=0.38):
    """Tint a responding structure as the pressure wave passes through it."""
    base = shape.get_fill_color()
    accent = ManimColor(color)
    elapsed = 0.0

    def respond(m, dt):
        nonlocal elapsed
        elapsed += dt
        intensity = strength * (0.5 - 0.5 * np.cos(5.1 * elapsed))
        m.set_fill(interpolate_color(base, accent, intensity))

    return shape.add_updater(respond), base


def canal_sound(color=YELLOW, reverse=False, height=0.60):
    start, end = (-3.60, -6.15) if reverse else (-6.15, -3.60)
    path = lambda f: xy(start + f * (end - start), -0.62 + 0.42 * (1 - f if reverse else f))
    return VGroup(signal_glow(path, color, height=height * 1.45),
                  sound_ripple(start, end, lambda f: path(f)[1], color, height))


def membrane_envelope(x, peak, left, right):
    """Schematic asymmetric spatial envelope for a single travelling tone."""
    width = np.where(x < peak, left, right)
    return np.exp(-((x - peak) / width) ** 2)


def membrane_view(peak=0.30, compact=False):
    """The unrolled cochlea, with a phase-advancing displacement under its envelope."""
    x0, x1, y = (-6.42, -0.65, -0.65) if compact else (-6.42, 6.42, -0.76)
    bed = capsule(x1 - x0, 3.35, (x0 + x1) / 2, y + 0.12, edge="#62808D", fill=FLUID)
    rail = Line(xy(x0 + 0.20, y), xy(x1 - 0.20, y), color="#6C93A1", stroke_width=2)
    gain = ValueTracker(0.64)
    phase = ValueTracker(0)
    phase.add_updater(lambda m, dt: m.increment_value(6 * dt))
    xs = np.linspace(0, 1, 145)
    pos = x0 + 0.21 + xs * (x1 - x0 - 0.42)
    env = membrane_envelope(xs, peak, 0.25, 0.14)
    wave = always_redraw(lambda: poly(zip(
        pos, y + gain.get_value() * env * np.sin(2 * PI * 2.8 * xs - phase.get_value())
    ), YELLOW, 6))
    picture = VGroup(bed, rail, wave)
    return picture, phase, gain, xy(x0 + 0.21 + peak * (x1 - x0 - 0.42), y)


def plot_surface(box):
    x0, x1, y0, y1 = box
    return RoundedRectangle(width=x1 - x0 + 0.96, height=y1 - y0 + 1.46, corner_radius=0.15,
                            stroke_color="#41566A", stroke_width=2, fill_color=DARK_TISSUE,
                            fill_opacity=1).move_to(xy((x0 + x1) / 2 - 0.02, (y0 + y1) / 2 + 0.01))


def gated_fraction(x):
    """Normalized two-state Boltzmann activation against displacement (schematic)."""
    return 1 / (1 + np.exp(-9 * (x - 0.50)))


def bundle_view(displacement, activation, speed=1.0):
    """Cell body, swaying membrane, staircase, tip links and transduction pores."""
    x = -3.68
    body = contour([
        (x - 1.65, -0.35), (x - 1.29, 0.10), (x + 1.38, 0.10),
        (x + 1.69, -0.36), (x + 1.46, -1.86), (x + 0.78, -2.48),
        (x - 0.84, -2.47), (x - 1.43, -1.78),
    ], color="#9BAFBC", fill=TISSUE)
    root_y = 0.12
    heights = np.array([1.01, 1.49, 1.98])
    roots = np.array([x - 0.91, x - 0.10, x + 0.70])
    phase = ValueTracker(0).add_updater(lambda m, dt: m.increment_value(3.7 * speed * dt))

    def top(i, fraction=1):
        h = heights[i] * fraction
        tilt = 0.06 + 0.28 * displacement.get_value() + 0.045 * np.sin(phase.get_value())
        return xy(roots[i] + h * tilt, root_y + h)

    rods = always_redraw(lambda: VGroup(*[
        Line(top(i, 0), top(i), color="#AEC0CE", stroke_width=28) for i in range(3)
    ]))
    links = always_redraw(lambda: VGroup(*[
        Line(top(i), top(i + 1, (heights[i] + 0.21) / heights[i + 1]),
             stroke_width=4.5, color=GREY) for i in range(2)
    ]))
    pores = always_redraw(lambda: VGroup(*[
        VGroup(
            Line(top(i) + LEFT * 0.10, top(i) + RIGHT * 0.10, color=BG, stroke_width=8),
            Line(top(i) + LEFT * 0.25, top(i) + LEFT * 0.10, color=PURPLE, stroke_width=9),
            Line(top(i) + RIGHT * 0.10, top(i) + RIGHT * 0.25, color=PURPLE, stroke_width=9),
            Line(top(i) + LEFT * 0.105, top(i) + RIGHT * 0.105, color=PURPLE,
                 stroke_width=8, stroke_opacity=1 - activation.get_value()),
        ) for i in range(2)
    ]))
    xs = np.linspace(-6.45, -0.63, 85)
    membrane = always_redraw(lambda: poly(zip(xs, -2.49 + 0.10 * np.sin(1.7 * xs - phase.get_value())),
                                          TEAL, 10))
    ions = VGroup(*[Dot(radius=0.083, color=ORANGE) for _ in range(8)])

    def stream(group):
        for index, dot in enumerate(group):
            point = top(index % 2)
            f = (phase.get_value() * 0.18 - (index // 2) * 0.23) % 1
            dot.move_to(point + DOWN * (f * 1.35 - 0.33))
            dot.set_opacity(activation.get_value() * min(1, 7 * f, (1 - f) * 7))
    stream(ions)
    ions.add_updater(stream)
    return VGroup(body, membrane, rods, links, pores, ions), phase, top


def ribbon_view(loss=None):
    """A local group of ribbon contacts. Six markers denote a schematic count."""
    body = contour([
        (-6.05, 2.07), (-5.69, 2.64), (-1.67, 2.70), (-1.19, 1.92),
        (-1.35, 0.72), (-2.36, 0.14), (-5.12, 0.11), (-5.92, 0.72),
    ], color="#9BAFBC", fill=TISSUE)
    terminals, contacts, signals, flow = VGroup(), VGroup(), VGroup(), VGroup()
    for i, x in enumerate(np.linspace(-5.58, -1.90, 6)):
        ribbon = Ellipse(width=0.25, height=0.36, fill_color=BG, fill_opacity=1,
                         stroke_color=RIBBON, stroke_width=3).move_to(xy(x, 0.66))
        vesicles = VGroup(*[
            Dot(xy(x + dx, 0.66 + dy), radius=0.051, color=RIBBON)
            for dx, dy in [(-0.19, 0.09), (0.19, 0.09), (-0.17, -0.07), (0.17, -0.07), (0, 0.24)]
        ])
        contacts.add(VGroup(ribbon, vesicles))
        terminal = contour([
            (x - 0.25, -0.18), (x + 0.21, -0.18), (x + 0.15, -0.65),
            (x + 0.28, -1.29), (x + 0.08, -1.39), (x - 0.13, -0.97),
            (x - 0.18, -0.55),
        ], color="#7C94AA", fill=FLUID)
        terminals.add(terminal)
        signals.add(travelling_dots(lambda f, x=x: xy(x + 0.18 * f, -0.30 - 1.01 * f),
                                     count=3, speed=0.59 + i * 0.052, size=0.044))
        flow.add(travelling_dots(lambda f, x=x: xy(x, 0.45 - 0.59 * f),
                                  color=RIBBON, count=3, speed=0.62 + i * 0.06, size=0.055))

    if loss is not None:
        for i in (1, 3, 4):
            for group in (contacts[i], terminals[i]):
                group.add_updater(lambda m: m.set_opacity(1 - loss.get_value()))
            for group in (signals[i], flow[i]):
                def dim(m):
                    for dot in m:
                        dot.set_opacity(dot.get_fill_opacity() * (1 - loss.get_value()))
                group.add_updater(dim)
    return VGroup(body, terminals, contacts, flow, signals)


def normal_threshold():
    return boxed_label("Normal threshold", color=GREEN, size=30, fill_opacity=0.22).move_to(xy(3.27, -1.93))


def synapse_ring():
    return Ellipse(width=1.55, height=0.85, color=GOLD, stroke_width=4).move_to(xy(2.59, -0.66))


def prediction_backdrop():
    return VGroup(hearing_chain(), normal_threshold(), synapse_ring(), stage_scope())


def comparison_plot():
    box = (-5.97, 5.96, -2.13, 1.85)
    plot = Plot(box, (0, 1), (0, 1.07), xlabel="Position along the basilar membrane",
                ylabel="Wave amplitude", label_size=30)
    return plot, plot_surface(box)


def passive_envelope(x):
    return 0.31 * membrane_envelope(x, 0.54, 0.31, 0.24)


def living_envelope(x):
    return 0.94 * membrane_envelope(x, 0.38, 0.18, 0.12)


class S01Hook(SpokenScene):
    def construct(self):
        world = hearing_chain()
        incoming = canal_sound()
        canal, canal_base = responsive_tissue(world[0][0], YELLOW, 0.29)
        q = label("?", -5.25, 3.26, GOLD, 62)
        self.add(world, incoming, stage_scope())
        self.at("when hearing fails")
        self.play(FadeIn(q), run_time=0.35)
        self.play(q.animate.shift(RIGHT * 8.0), run_time=3.15)
        self.at("sound enters the ear canal")
        self.play(FadeOut(q), run_time=0.45)
        self.at("the coiled cochlea")
        winding = travelling_dots(lambda f: world[1][2].point_from_proportion(f), speed=0.67)
        self.add(winding)
        self.at("reach the brainstem")
        nerve = travelling_dots(nerve_path, speed=0.49)
        self.add(nerve)
        self.at("a healthy cochlea even")
        self.remove(incoming, winding)
        canal.clear_updaters().set_fill(canal_base)
        responsive_tissue(canal, TEAL, 0.45)
        return_wave = canal_sound(TEAL, reverse=True, height=0.43)
        self.add(return_wave)
        self.at("to test hearing")
        self.remove(return_wave, nerve)
        canal.clear_updaters().set_fill(canal_base)
        points = probes()
        scan = signal_glow(lambda f: xy(-5.18 + 10.78 * f, -0.64 + 1.19 * f**4), speed=0.25)
        self.add(scan)
        self.play(LaggedStart(*[GrowFromCenter(dot) for dot in points], lag_ratio=0.62), run_time=4.0)
        self.remove(scan)
        self.finish()


class S02Title(TitleCard):
    LESSON = "Cochlear Function Tests"
    TITLE = "Measuring Hearing from Ear Canal to Brainstem"

    def construct(self):
        world = hearing_chain()
        for part in world.family_members_with_points():
            part.set_stroke(opacity=0.32)
            if part.get_fill_opacity() > 0:
                part.set_fill(opacity=0.11)
        shimmer = sound_ripple(-3.60, -6.15, lambda f: -0.20 - 0.42 * f, TEAL, height=0.39)
        self.add(world, shimmer)
        title = T(self.TITLE.replace(" from ", " from\n"), 49, TEXT, font=TITLE_FONT,
                  line_spacing=0.82).move_to(xy(0, 0.47))
        title_plate = capsule(title.width + 0.86, title.height + 0.50, 0, 0.47, edge=BG, fill=BG, stroke=0)
        self.add(title_plate)
        self.play(FadeIn(title), run_time=0.25)
        self.wait(1.45)
        self.play(FadeOut(title), run_time=0.25)


class S03Mechanics(SpokenScene):
    def construct(self):
        world = hearing_chain()
        mic = VGroup(
            capsule(1.17, 0.82, -5.77, -0.55, edge=BLUE, fill="#24495D"),
            capsule(0.37, 0.65, -5.06, -0.51, edge=BLUE, fill="#24495D"),
            Line(xy(-4.88, -0.16), xy(-4.88, -0.83), color=GREEN, stroke_width=6),
        )
        return_wave = sound_ripple(-3.60, -5.0, lambda f: -0.21 - 0.25 * f,
                                   TEAL, height=0.37)
        mic_label = label("Sealed microphone", -4.72, -2.46, BLUE)
        self.add(world, stage_scope())
        self.at("start at the ear canal")
        self.play(FadeIn(mic, shift=RIGHT * 0.40), run_time=0.7)
        self.at("a sealed microphone")
        self.play(FadeIn(mic_label), run_time=0.4)
        self.add(return_wave)
        scope_box = (0.86, 5.77, -1.60, 0.89)
        osc = Plot(scope_box, (0, 1), (-1, 1), label_size=30)
        osc_phase = ValueTracker(0).add_updater(lambda m, dt: m.increment_value(4.3 * dt))
        trace = always_redraw(lambda: osc.curve(
            lambda x: 0.58 * np.sin(PI * x) * np.sin(2 * PI * 4 * x - osc_phase.get_value()),
            color=TEAL, width=5, n=90))
        emission = label("Otoacoustic emission", 3.31, 1.18, TEAL)
        display = VGroup(plot_surface(scope_box), osc)
        self.at("microphone records faint")
        self.play(FadeIn(display), run_time=0.55)
        self.add(osc_phase, trace)
        self.at("emission screens newborns")
        self.play(FadeIn(emission), run_time=0.45)
        unrolled, phase, gain, _ = membrane_view()
        self.at("inside sound sets")
        self.remove(trace, return_wave)
        self.play(FadeOut(mic_label), FadeOut(emission), run_time=0.20)
        self.play(FadeOut(world, shift=LEFT * 0.33), FadeOut(mic), FadeOut(display),
                  FadeIn(unrolled, shift=LEFT * 0.33), run_time=0.58)
        self.add(phase)
        base = label("Base", -5.50, -1.74, TEXT)
        apex = label("Apex", 5.44, -1.74, TEXT)
        title = label("Basilar membrane", -3.95, 1.64, TEAL)
        self.at("along the basilar membrane")
        self.play(FadeIn(title), run_time=0.55)
        self.at("each place moves most")
        self.play(FadeIn(base), FadeIn(apex), run_time=0.55)
        high_tone = label("High tone", -3.24, 0.53, YELLOW)
        self.at("high ones near")
        self.play(FadeIn(high_tone), gain.animate.set_value(0.98), run_time=0.60)
        mini, mini_phase, mini_gain, spot = membrane_view(compact=True)
        mini_phase.set_value(phase.get_value())
        marker = Circle(radius=0.17, color=YELLOW, stroke_width=4).move_to(spot)
        box = (0.10, 6.02, -2.26, 2.04)
        plot = Plot(box, (0, 1), (0, 1), xlabel="Sound level (dB)",
                    ylabel="Membrane motion (dB)", label_size=29)
        slots = VGroup(label("Alive", 4.72, 1.20, GREEN), label("After death", 4.72, 0.56))
        tone = ValueTracker(0.12)
        step = Dot(radius=0.11, color=YELLOW).add_updater(
            lambda m: m.move_to(plot.pt(tone.get_value(), 0) + UP * 0.02)
        )
        self.at("scientists measure one")
        self.play(FadeOut(unrolled), FadeOut(base), FadeOut(apex), FadeOut(high_tone), run_time=0.35)
        self.play(FadeIn(mini), FadeIn(marker), FadeIn(VGroup(plot_surface(box), plot)), run_time=0.5)
        self.add(mini_phase, step)
        self.at("a tone gets louder")
        self.play(tone.animate.set_value(0.42), mini_gain.animate.set_value(0.88), run_time=0.40)
        self.play(tone.animate.set_value(0.76), mini_gain.animate.set_value(1.17), run_time=0.40)
        self.at("alive and after death")
        self.play(FadeIn(slots), run_time=0.37)
        self.finish()


class S04Bundle(SpokenScene):
    def construct(self):
        displacement = ValueTracker(0)
        opened = ValueTracker(0)
        view, phase, top = bundle_view(displacement, opened)
        stereocilia = label("Stereocilia", -0.27, 1.94, TEXT, 34)
        tip_links = label("Tip links", -5.80, 1.48, TEXT, 34)
        rod_leader = always_redraw(lambda: Line(
            stereocilia.get_left() + LEFT * 0.15, top(2, 0.91), color=GREY, stroke_width=3,
        ))
        tip_link_leader = always_redraw(lambda: Line(
            tip_links.get_right() + RIGHT * 0.15, view[3][0].get_center(), color=GREY, stroke_width=3,
        ))
        base_label = label("Basilar membrane", -3.55, -3.06, TEAL)
        self.add(view, phase, stage_scope())
        self.at("membrane motion pushes")
        self.play(FadeIn(base_label), run_time=0.50)
        self.at("a staircase of stereocilia")
        self.play(FadeIn(stereocilia), Create(rod_leader), run_time=0.45)
        self.at("linked by tip links")
        self.play(FadeIn(tip_links), Create(tip_link_leader), run_time=0.45)
        self.at("holding the cell")
        clamp = boxed_label("Negative voltage (held)", color=BLUE, size=29).move_to(xy(3.05, -0.37))
        self.play(FadeIn(clamp), run_time=0.52)
        probe = capsule(1.37, 0.23, 0, 0, edge=BLUE, fill="#31556C")
        probe.add_updater(lambda m: m.move_to(top(0, 0.65) + LEFT * 0.84))
        self.at("scientists push the bundle")
        push = 0.62
        self.play(FadeIn(probe), displacement.animate.set_value(push), run_time=1.8)
        self.at("tip links are thought")
        self.play(opened.animate.set_value(gated_fraction(push)), run_time=0.7)
        gating = label("Proposed direct gating", 2.92, 1.72, PURPLE, 33)
        self.play(FadeOut(stereocilia), FadeOut(tip_links),
                  FadeOut(rod_leader), FadeOut(tip_link_leader), run_time=0.28)
        self.play(FadeIn(gating), run_time=0.35)
        ions = label("Positive ions flow in", 2.94, 0.81, ORANGE)
        self.at("positive ions flow")
        self.play(FadeIn(ions), run_time=0.45)
        box = (0.43, 6.02, -2.25, 2.19)
        plot = Plot(box, (0, 1), (0, 1.06), xlabel="Bundle displacement",
                    ylabel="Peak inward current", label_size=29)
        cursor = plot.dot(displacement.get_value, lambda: gated_fraction(displacement.get_value()), color=YELLOW)
        live = plot.live_curve(gated_fraction, displacement, color=YELLOW)
        opened.add_updater(lambda m: m.set_value(gated_fraction(displacement.get_value())))
        self.at("more push opens")
        self.play(FadeOut(gating), FadeOut(ions), FadeOut(clamp), run_time=0.45)
        self.play(FadeIn(VGroup(plot_surface(box), plot)), run_time=0.50)
        self.add(live, cursor, opened)
        self.at("peak current traces")
        self.play(displacement.animate.set_value(1), run_time=3.70, rate_func=linear)
        self.finish()


def threshold_plot():
    box = (0.51, 6.02, -2.25, 1.99)
    plot = Plot(box, (0, 1), (0, 1), xlabel="Tone level", ylabel="Evoked response", label_size=29)
    return plot, plot_surface(box)


def electrical_trace(x):
    # A schematic summed response with a small early deflection and later peaks.
    return (0.20 * np.exp(-((x - 0.27) / 0.032) ** 2)
            - 0.13 * np.exp(-((x - 0.34) / 0.040) ** 2)
            + 0.42 * np.exp(-((x - 0.49) / 0.036) ** 2)
            - 0.27 * np.exp(-((x - 0.56) / 0.038) ** 2)
            + 0.25 * np.exp(-((x - 0.66) / 0.055) ** 2))


class S05Thresholds(SpokenScene):
    def construct(self):
        ribbon = ribbon_view()
        haircell = label("Inner hair cell", -3.68, 1.99)
        contact_name = label("Ribbon synapses", -3.68, 1.40, RIBBON, 34)
        contact_point = ribbon[2][3].get_top()
        contact_leader = Line(xy(contact_point[0], contact_name.get_bottom()[1] - 0.09),
                              contact_point, color=RIBBON, stroke_width=3)
        nerve_name = label("Auditory nerve", -3.72, -1.94, TEXT)
        brain = hearing_chain()[3]
        ending = travelling_dots(nerve_path)
        self.add(ribbon, brain, stage_scope())
        self.at("inner hair cells")
        self.play(FadeIn(haircell), run_time=0.4)
        self.at("signals to nerve fibers")
        self.add(ending)
        self.play(FadeIn(nerve_name), run_time=0.4)
        self.at("called ribbon synapses")
        self.play(FadeIn(contact_name), Create(contact_leader), run_time=0.45)
        plot, surface = threshold_plot()
        criterion = plot.hline(0.46, color=GREEN)
        criterion_text = label("Response criterion", 2.54, 0.62, GREEN, 28)
        tone = ValueTracker(0.92)
        record = plot.dot(tone.get_value, lambda: tone.get_value() * 0.84 + 0.03, color=YELLOW)
        slider = plot.dot(tone.get_value, lambda: 0.012, color=BLUE, radius=0.10)
        self.at("threshold tests then")
        self.remove(ending)
        self.play(FadeOut(brain), FadeOut(contact_name), FadeOut(contact_leader), run_time=0.40)
        panel = VGroup(surface, plot, criterion, criterion_text)
        self.play(FadeIn(panel), run_time=0.52)
        self.add(record, slider)
        self.at("the quietest sound")
        self.play(tone.animate.set_value(0.518), run_time=2.40)
        wide_a = (-5.92, -0.60, -2.20, 1.58)
        wide_b = (0.51, 6.02, -2.20, 1.58)
        audio = Plot(wide_a, (0, 1), (0, 1), xlabel="Frequency", ylabel="Behavioral threshold", label_size=29)
        electric = Plot(wide_b, (0, 1), (-0.40, 0.60), xlabel="Time",
                        ylabel="Nerve + brainstem signal", label_size=29)
        # Audiograms conventionally put the quieter threshold toward the top.
        audiogram = audio.curve(lambda x: 0.68 - 1.45 * (x - 0.58) ** 2, color=YELLOW)
        self.at("an audiogram plots")
        self.remove(record, slider)
        self.play(FadeOut(panel), FadeOut(ribbon), FadeOut(haircell), FadeOut(nerve_name), run_time=0.35)
        audio_panel = VGroup(plot_surface(wide_a), audio)
        electric_panel = VGroup(plot_surface(wide_b), electric)
        self.play(FadeIn(audio_panel), run_time=0.44)
        self.play(Create(audiogram), run_time=1.4)
        self.at("electrical tests record")
        self.play(FadeIn(electric_panel), run_time=0.48)
        signal = electric.curve(electrical_trace, color=YELLOW)
        self.play(Create(signal), run_time=1.65)
        self.at("so different tests")
        world = hearing_chain()
        self.play(FadeOut(audio_panel), FadeOut(electric_panel), FadeOut(audiogram),
                  FadeOut(signal), run_time=0.31)
        self.play(FadeIn(world), run_time=0.42)
        points = probes()
        scan = signal_glow(lambda f: xy(-5.18 + 10.78 * f, -0.64 + 1.19 * f**4), speed=0.29)
        self.add(scan)
        self.play(LaggedStart(*[GrowFromCenter(dot) for dot in points], lag_ratio=0.64), run_time=3.40)
        self.finish()


class S06Predict(SpokenScene):
    def construct(self):
        world, badge, ring, tag = prediction_backdrop()
        points = probes()
        self.add(world, tag, points)
        self.at("now test that idea")
        self.play(FadeOut(points), run_time=0.7)
        self.at("faces loud noise")
        noise = canal_sound(RED, height=0.90)
        in_coil = travelling_dots(lambda f: world[1][2].point_from_proportion(f),
                                  color=RED, speed=0.80, size=0.14)
        self.add(noise, in_coil)
        self.at("yet later passes")
        self.remove(noise, in_coil)
        nerve = travelling_dots(nerve_path, speed=0.45, size=0.13)
        response = signal_glow(nerve_path, speed=0.45, width=1.70, height=1.26)
        self.add(response, nerve)
        self.play(FadeIn(badge), run_time=0.62)
        self.at("does a normal threshold")
        self.play(Create(ring), run_time=0.66)
        card = question_card(QUESTION, **CARD)
        self.at("prove its ribbon synapses")
        self.play(FadeIn(card), run_time=0.52)
        self.at("pause and decide")
        pulse(ring, base=5, amp=3.2, speed=3.0)
        self.finish()


class S07Pause(PredictPause):
    QUESTION = QUESTION
    CARD = CARD
    SECONDS = 4.5

    def construct(self):
        backdrop = prediction_backdrop()
        pulse(backdrop[2], base=5, amp=3.2, speed=3.0)
        bar = capsule(8.5, 0.25, -0.5, -3.47, edge="#41566A", fill="#263645", stroke=1)
        progress = Rectangle(width=8.34, height=0.15, stroke_width=0,
                             fill_color=GOLD, fill_opacity=0.86).move_to(bar)
        self.add(backdrop, question_card(self.QUESTION, **self.CARD), bar)
        self.play(GrowFromEdge(progress, LEFT, rate_func=linear), run_time=self.SECONDS)


class S08Controls(SpokenScene):
    def construct(self):
        world, badge, ring, tag = prediction_backdrop()
        loss = ValueTracker(0)
        contact = ribbon_view(loss)
        self.add(world, badge, ring, tag)
        self.at("a mouse can pass")
        pulse(ring, base=4, amp=2.2, speed=3.0)
        nerve = travelling_dots(nerve_path, size=0.12)
        response = signal_glow(nerve_path, speed=0.43, width=1.70, height=1.26)
        self.add(response, nerve)
        self.at("yet it can lose")
        self.remove(nerve, response)
        ring.clear_updaters()
        self.play(FadeOut(world), FadeOut(ring), FadeIn(contact, shift=RIGHT * 0.3), run_time=0.78)
        locus = label("One cochlear place", -3.69, 1.64)
        self.at("about half the ribbon")
        self.play(loss.animate.set_value(1), run_time=1.40)
        self.play(FadeIn(locus), run_time=0.45)
        quiet = label("Quietest response", 3.15, -0.92, TEXT)
        self.at("only tests the quietest")
        response = signal_glow(nerve_path, GREEN, speed=0.43, width=1.66, height=1.18)
        brain = hearing_chain()[3]
        self.play(FadeIn(brain), run_time=0.33)
        self.add(response)
        self.play(FadeIn(quiet), run_time=0.45)
        p, surface = comparison_plot()
        alive = label("Alive", 3.63, 1.31, GREEN)
        dead = label("After death", 3.63, 0.70, YELLOW)
        shape_t = ValueTracker(0.10)
        # Two matched readings of the same membrane position and axes.
        focus = p.vline(0.38, color=GOLD)
        pulse(focus[0], base=3, amp=1.4, speed=3.2)
        self.at("comparing each cochlea")
        self.remove(response)
        self.play(FadeOut(contact), FadeOut(locus), FadeOut(quiet), FadeOut(badge), FadeOut(brain), run_time=0.38)
        self.play(FadeIn(VGroup(surface, p)), FadeIn(focus), run_time=0.62)
        self.add(p.live_curve(living_envelope, shape_t, color=GREEN))
        self.play(FadeIn(alive), run_time=0.35)
        self.at("after death separates")
        bare = ValueTracker(0.01)
        self.add(p.live_curve(passive_envelope, bare, color=YELLOW))
        self.play(FadeIn(dead), shape_t.animate.set_value(1), bare.animate.set_value(1),
                  run_time=3.02, rate_func=linear)
        self.finish()


def outer_hair_cells(voltage, motor):
    rows = VGroup()
    for row in reversed(range(3)):
        cells = VGroup()
        y = -2.42 + row * 1.86
        for column in range(4):
            x = -5.28 + column * 1.32 + row * 0.44
            emphasized = row == 2 and column == 2

            def cell(x=x, y=y, emphasized=emphasized):
                h = 1.25 - 0.17 * voltage.get_value()
                body = capsule(0.56, h, x, y + h / 2, edge="#9FB2C2", fill="#45596B")
                top = y + h
                bundle = VGroup(*[
                    Line(xy(x + dx, top - 0.02), xy(x + dx * 1.19, top + 0.18 + 0.23 * dx),
                         color=GREY, stroke_width=4) for dx in (-0.16, 0, 0.16)
                ])
                wall = Line(xy(x + 0.238, y + 0.26), xy(x + 0.238, top - 0.27),
                            color=PRESTIN, stroke_width=7, stroke_opacity=motor.get_value() if emphasized else 0)
                return VGroup(body, bundle, wall)
            cells.add(always_redraw(cell))
        rail = capsule(5.78, 0.23, -3.31 + row * 0.44, y - 0.05,
                       edge=TEAL, fill=FLUID)
        rows.add(VGroup(rail, cells))
    return rows


class S09Unlocked1(SpokenScene):
    def construct(self):
        p, surface = comparison_plot()
        alive = label("Alive", 3.63, 1.31, GREEN)
        dead = label("After death", 3.63, 0.70, YELLOW)
        passive = p.curve(passive_envelope, color=YELLOW)
        living = p.curve(living_envelope, color=GREEN)
        focus = p.vline(0.38, color=GOLD)
        self.add(surface, p, alive, dead, passive, living, focus, stage_scope())
        self.at("together these methods")
        world = hearing_chain()
        self.play(FadeOut(VGroup(surface, p, alive, dead, passive, living, focus)),
                  run_time=0.32)
        self.play(FadeIn(world), run_time=0.50)
        points = probes()
        self.play(LaggedStart(*[GrowFromCenter(dot) for dot in points], lag_ratio=0.28), run_time=1.1)
        self.at("a dead cochlea still")
        self.play(FadeOut(world), FadeOut(points), run_time=0.31)
        self.play(FadeIn(VGroup(surface, p, focus)), run_time=0.45)
        living.set_stroke(opacity=0.48)
        self.play(Create(passive), FadeIn(dead), FadeIn(living), FadeIn(alive), run_time=2.20)
        self.at("broadly tuned and")
        shift = Arrow(p.pt(0.38, 1.015), p.pt(0.54, 1.015), buff=0, color=GOLD,
                      stroke_width=4, tip_length=0.18)
        peak = p.dot(lambda: 0.54, lambda: passive_envelope(0.54), color=YELLOW, ring=GOLD)
        self.play(GrowArrow(shift), FadeIn(peak), run_time=0.70)
        pulse(passive, base=6, amp=1.7, speed=3.5)
        self.at("the living cochlea adds")
        overlap = [x for x in np.linspace(0, 1, 121) if living_envelope(x) > passive_envelope(x)]
        amplification = Polygon(
            *[p.pt(x, living_envelope(x)) for x in overlap],
            *[p.pt(x, passive_envelope(x)) for x in reversed(overlap)],
            stroke_width=0, fill_color=GREEN, fill_opacity=0.30,
        )
        amplified = p.curve(living_envelope, color=GREEN, width=7)
        self.play(FadeOut(peak), FadeOut(shift), run_time=0.30)
        self.play(FadeIn(amplification), Create(amplified), run_time=1.90)
        self.remove(living)
        self.bring_to_front(focus, passive)
        voltage = ValueTracker(0)
        phase = ValueTracker(0)
        phase.add_updater(lambda m, dt: m.increment_value(2.9 * dt))
        voltage.add_updater(lambda m: m.set_value(np.sin(phase.get_value())))
        motor = ValueTracker(0)
        cells = outer_hair_cells(voltage, motor)
        row_label = label("Three outer hair cell rows", 3.24, 1.66, TEXT, 31)
        track = Line(xy(1.92, 0.06), xy(4.56, 0.06), color=GREY, stroke_width=4)
        indicator = Dot(track.get_center(), radius=0.13, color=BLUE, stroke_color=BG, stroke_width=3)
        indicator.add_updater(lambda m: m.move_to(track.point_from_proportion((1 + voltage.get_value()) / 2)))
        meter = VGroup(track, indicator, label("Voltage", 3.24, 0.66, BLUE),
                       label("−", 1.53, 0.06, BLUE), label("+", 4.95, 0.06, BLUE))
        self.at("three rows of outer")
        self.remove(surface, p, focus, alive, dead, passive, amplification, amplified)
        self.add(cells[0])
        self.play(LaggedStart(*[FadeIn(row, shift=UP * 0.1) for row in cells[1:]], lag_ratio=0.40),
                  run_time=1.08)
        self.play(FadeIn(row_label), run_time=0.35)
        self.at("shorten and lengthen")
        self.add(phase, voltage)
        self.play(FadeIn(meter), run_time=0.52)
        self.at("side wall protein")
        prestin = label("Prestin", 3.24, -0.89, PRESTIN, 35)
        self.play(motor.animate.set_value(1), FadeIn(prestin), run_time=0.63)
        self.finish()


class S10Unlocked2(SpokenScene):
    def construct(self):
        shift = ValueTracker(0)
        opened = ValueTracker(0)
        cell, phase, _ = bundle_view(shift, opened)
        box = (0.42, 6.02, -2.19, 2.22)
        plot = Plot(box, (0, 8), (0, 1.07), xlabel="Time after push",
                    ylabel="Inward current", label_size=29)
        surface = plot_surface(box)
        self.add(cell, phase, stage_scope())
        self.at("turtle hair cell channels")
        self.play(FadeIn(VGroup(surface, plot)), run_time=0.62)
        cursor = ValueTracker(0)
        # Normalized exponential activation. Time is in units of the fast time
        # constant; the slower comparator is illustrative and has no time label.
        fast = lambda t: 0.90 * (1 - np.exp(-t))
        slow = lambda t: 0.90 * (1 - np.exp(-t / 5) * (1 + t / 5))
        live = plot.live_curve(fast, cursor, color=YELLOW)
        self.at("switch on with")
        self.add(live)
        self.play(shift.animate.set_value(0.86), opened.animate.set_value(0.97),
                  cursor.animate.set_value(8), run_time=3.35, rate_func=linear)
        tau = label("About 50 microseconds", 4.02, 0.54, TEXT, 31)
        self.at("about 50 microseconds")
        self.play(FadeIn(tau), run_time=0.48)
        self.at("too fast for a chain")
        comparison = plot.curve(slow, color=GREY)
        enzyme = label("Enzyme chain", 2.55, -0.97, TEXT, 28)
        self.play(Create(comparison), FadeIn(enzyme), run_time=1.0)
        self.at("force is thought to")
        pulse(live, base=6, amp=2.1, speed=3.8)
        loss = ValueTracker(0)
        contacts = ribbon_view(loss)
        badge = normal_threshold()
        locus = label("One cochlear place", -3.69, 1.64)
        self.at("third in mice")
        self.remove(cell, surface, plot, tau, live, phase, comparison, enzyme)
        self.add(contacts)
        ring = Ellipse(width=4.58, height=0.94, color=GOLD, stroke_width=3.5).move_to(xy(-3.75, 0.57))
        self.play(Create(ring), run_time=0.46)
        self.at("about half the ribbon")
        self.play(loss.animate.set_value(1), FadeOut(ring), FadeIn(locus), run_time=1.55)
        self.at("while thresholds stay normal")
        self.play(FadeIn(badge), run_time=0.48)
        self.at("testing several stages")
        world = hearing_chain()
        self.play(FadeOut(contacts), FadeOut(locus), FadeOut(badge), run_time=0.28)
        self.play(FadeIn(world), run_time=0.40)
        points = probes()
        self.play(*[GrowFromCenter(dot) for dot in points], run_time=0.70)
        for dot in points:
            pulse(dot, base=3, amp=2.3, speed=4.5)
        self.finish()


class S11End(EndCard):
    LINE = "Read hearing at each stage; a normal threshold can hide damage."
