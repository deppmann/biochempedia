"""Recording Living Synapses in a Brain Slice.

BLUE: recording apparatus. GREY: tissue and membranes. PURPLE: receptors
and circuit fibres. YELLOW: electrical signals and recorded responses.
GREEN: glia and uptake. RED: magnesium block. ORANGE: applied compounds
and glutamate. TEAL: bath and chloride. GOLD: dates and prediction.
"""
from bp_parts import *
from bp_style import EndCard

PURPLE = "#B58CD9"
ORANGE = "#F29E4C"
TISSUE = "#514066"
BATH = "#183438"
GLIA = "#314A3B"
CELL = "#493D59"
K_COLOR = "#F3A6CB"
QUESTION = "Which side changes concentration faster?"
QUESTION_STYLE = {"size": 36}
RELAY_COLORS = (BLUE, PURPLE, YELLOW)


def p(x, y):
    return np.array([x, y, 0.0])


def label(text, x, y, color=TEXT, size=30):
    return T(text, size, color).move_to(p(x, y))


def panel(width, height, x, y, color, fill, radius=0.26):
    return RoundedRectangle(width=width, height=height, corner_radius=radius,
                            stroke_color=color, stroke_width=2, fill_color=fill,
                            fill_opacity=1).move_to(p(x, y))


def contour(points, color, width=4, fill=None):
    line = VMobject()
    line.set_points_smoothly([p(x, y) for x, y in points])
    line.set_stroke(color, width)
    if fill:
        line.set_fill(fill, 1)
    return line


def arrow(start, end, color=YELLOW, width=5):
    return Arrow(start, end, buff=0, color=color, stroke_width=width,
                 tip_length=0.20, max_stroke_width_to_length_ratio=15)


def bath():
    return panel(13.0, 5.12, 0, 0.1, "#31585F", BATH, radius=0.50)


def stream(color=TEAL, lanes=(-2.29, -1.96, 2.21, 2.45), speed=0.98, span=12.4):
    """Perfusion moving behind the tissue, inside the recording chamber."""
    flow = VGroup()
    for row, y in enumerate(lanes):
        for col in range(9):
            start = (span / 9 * col + 0.46 * row) % span
            streak = Line(LEFT * (0.17 + col % 3 * 0.065), RIGHT * 0.23,
                          stroke_color=color, stroke_width=9.0)
            phase = ValueTracker(start)

            def advect(mob, dt, phase=phase, y=y, row=row):
                x = (phase.get_value() + speed * dt * (1 + 0.06 * row)) % span
                phase.set_value(x)
                mob.move_to(p(x - 6.2, y + 0.025 * np.sin(x + row)))
                mob.set_stroke(opacity=0.63 * min(1, x / 0.45, (span - x) / 0.45))

            streak.add_updater(advect, call_updater=True)
            flow.add(streak)
    return flow


def hippocampus():
    """A stylized hippocampal cross-section with the three relays in register."""
    body = contour([(-4.05, -1.00), (-5.18, 0.08), (-4.50, 1.58), (-2.41, 2.02),
                    (0.35, 1.62), (2.55, 0.82), (3.74, -0.32), (3.25, -1.26),
                    (1.50, -1.57), (-0.47, -0.97), (-2.20, -1.50),
                    (-3.20, -1.72), (-4.05, -1.00)], "#88739D", 3, TISSUE)
    ribbons = VGroup(
        contour([(-4.65, 0.30), (-3.95, 1.25), (-2.22, 1.45), (-0.03, 1.20),
                 (1.79, 0.62), (2.69, -0.09), (2.54, -0.63)], "#745D89", 9),
        contour([(-3.70, -0.93), (-4.05, -0.15), (-3.22, 0.60), (-2.08, 0.53),
                 (-1.19, 0.06), (-1.52, -0.64), (-2.45, -0.98)], "#806696", 11),
        contour([(-2.98, -1.26), (-1.75, -1.08), (-0.43, -0.49), (0.90, -0.74),
                 (2.13, -1.11)], "#655377", 6),
    )
    paths = [
        contour([(-4.73, 0.76), (-4.05, 0.24), (-3.57, 0.17), (-3.00, 0.39)], BLUE),
        contour([(-3.00, 0.39), (-2.39, 0.33), (-1.82, -0.09), (-1.20, -0.35)], PURPLE),
        contour([(-1.20, -0.35), (-0.50, -0.13), (0.20, 0.30), (0.92, 0.35),
                 (1.71, 0.21), (2.22, -0.10)], YELLOW),
    ]
    nodes = VGroup(*[Circle(radius=0.15, stroke_color=color, stroke_width=3,
                            fill_color=BG, fill_opacity=1).move_to(path.get_end())
                    for color, path in zip(RELAY_COLORS, paths)])
    world = VGroup(body, ribbons, *paths, nodes)
    world.paths = paths
    world.nodes = nodes
    return world


def relay_pulse(path, color, seconds=2.6, phase=0.0):
    glows = VGroup()
    for i in range(3):
        seed = phase + i * 0.12
        mote = Dot(radius=0.09 - i * 0.018, color=color)
        clock = ValueTracker(seed)

        def travel(mob, dt, clock=clock, i=i):
            t = (clock.get_value() + dt / seconds) % 1
            clock.set_value(t)
            mob.move_to(path.point_from_proportion(t))
            mob.set_opacity((1 - i * 0.21) * min(1, t * 10, (1 - t) * 10))

        glows.add(mote.add_updater(travel, call_updater=True))
    return glows


def slice_stage(scene, active=(2,)):
    world = hippocampus()
    scene.add(bath(), stream(), world, scope_tag(size=28, color=TEXT))
    for i in active:
        scene.add(relay_pulse(world.paths[i], RELAY_COLORS[i], phase=0.2))
    return world


def brain_silhouette():
    return contour([(-6.10, -0.12), (-5.56, 1.54), (-3.93, 2.44), (-1.46, 2.69),
                    (1.16, 2.53), (3.63, 1.85), (5.23, 0.94), (5.73, -0.33),
                    (4.32, -1.03), (3.22, -1.00), (2.01, -1.76), (1.45, -2.23),
                    (0.53, -2.02), (-0.27, -1.39), (-2.44, -1.38),
                    (-4.50, -1.09), (-6.10, -0.12)], GREY, 4)


def electrode(start, tip):
    direction = (start - tip) / np.linalg.norm(start - tip)
    side = p(-direction[1], direction[0])
    return Polygon(start + 0.19 * side, start - 0.19 * side,
                   tip - 0.04 * side, tip + 0.04 * side,
                   stroke_width=2, stroke_color=BLUE, fill_color="#326679", fill_opacity=1)


def epsp(t, amplitude=1.0):
    """Normalized schematic difference of exponentials, not measured voltages."""
    rise, decay = 0.075, 0.36
    peak = np.log(decay / rise) / (1 / rise - 1 / decay)
    norm = np.exp(-peak / decay) - np.exp(-peak / rise)
    x = max(0, t - 0.30)
    return -amplitude * (np.exp(-x / decay) - np.exp(-x / rise)) / norm


def response_scope(amplitude, sweep=None, reference=False):
    """Same plot extent and baseline for every field EPSP comparison."""
    screen = panel(3.82, 4.5, 4.55, 0.04, "#75949A", "#202E39")
    axes = Plot(box=(2.93, 6.15, -1.38, 1.06), xr=(0, 1.8), yr=(-1.8, 0.24),
                xlabel="Time", color=TEXT, label_size=28)
    heading = label("Field EPSP", 4.55, 1.80, YELLOW, 32)
    marker = label("schematic", 4.55, 1.32, TEXT, 28)
    baseline = axes.hline(0, color="#748796")
    trace = always_redraw(lambda: axes.curve(
        lambda t: epsp(t, amplitude.get_value()),
        x1=sweep.get_value() if sweep is not None else None, color=YELLOW, width=6,
        n=75))
    scope = VGroup(screen, axes, heading, marker, baseline)
    if reference:
        scope.add(axes.curve(epsp, color=GREY, width=3, opacity=0.6, n=75))
    scope.add(trace)
    return scope


def synapse():
    """Close-up of the CA1 contact, with membrane gaps for AMPA and NMDA."""
    terminal = contour([(-6.02, 1.63), (-5.34, 2.31), (-3.26, 2.06), (-0.74, 2.07),
                        (0.95, 1.46), (0.64, 0.78), (-1.45, 0.66), (-4.72, 0.66),
                        (-5.76, 0.97), (-6.02, 1.63)], "#9A85AC", 4, TISSUE)
    dendrite = panel(7.19, 1.65, -2.57, -1.42, "#8F7DA1", CELL)
    dendrite.set_stroke(width=0)
    membrane = VGroup(*[Line(p(a, -0.60), p(b, -0.60), color=GREY, stroke_width=7)
                        for a, b in [(-5.95, -4.26), (-3.34, -2.11), (-1.19, 0.82)]])
    return VGroup(terminal, dendrite, membrane)


def gate(x):
    return VGroup(*[panel(0.30, 0.83, x + dx, -0.60, PURPLE, "#704895", 0.12)
                    for dx in (-0.30, 0.30)])


def droplets(color, starts, ends, radius=0.074, seconds=2.25, run=True):
    """One group of particles moving between the given physical landmarks."""
    group = VGroup()
    for i, (start, end) in enumerate(zip(starts, ends)):
        phase = ValueTracker((i * 0.143) % 1)
        dot = Dot(start, radius=radius, color=color)

        def descend(mob, dt, phase=phase, start=start, end=end):
            t = (phase.get_value() + dt / seconds) % 1
            phase.set_value(t)
            mob.move_to(interpolate(start, end, t))
            mob.set_opacity(min(1, t * 8, (1 - t) * 8))

        if run:
            dot.add_updater(descend, call_updater=True)
        else:
            descend(dot, 0)
        group.add(dot)
    return group


def transmitter(x=-2.65, span=5.35, color=ORANGE):
    return droplets(color, [p(i, 0.62) for i in np.linspace(x - span/2, x + span/2, 13)],
                    [p(i, -0.42) for i in np.linspace(x - span/2, x + span/2, 13)])


class S01Hook(SpokenScene):
    def construct(self):
        slice_stage(self, active=(0, 1, 2))
        self.at("watch living synapses")
        question = label("?", 0.0, 3.10, GOLD, 62)
        self.play(FadeIn(question, shift=UP * 0.12), run_time=0.55)
        self.at("inside an intact brain")
        brain = brain_silhouette()
        self.play(FadeOut(question), Create(brain), run_time=1.6)
        self.at("keep a thin brain slice")
        self.play(FadeOut(brain), run_time=1.25)
        self.finish()


class S02Title(TitleCard):
    LESSON = "Brain Slice Electrophysiology"
    TITLE = "Recording Living Synapses in a Brain Slice"

    def construct(self):
        slice_stage(self, active=(0, 1, 2))
        title = T(self.TITLE, 42, TEXT, font=TITLE_FONT).move_to(p(0, 3.20))
        self.play(FadeIn(title), run_time=0.24)
        self.wait(max(0.1, self.narration_s - 0.54))
        self.play(FadeOut(title), run_time=0.24)


class S03Map(SpokenScene):
    def construct(self):
        world = slice_stage(self, active=())
        for path in world.paths:
            path.set_stroke(opacity=0.24)
        world.nodes.set_opacity(0.30)
        self.at("work uses rat")
        heading = label("Rat hippocampus", -2.45, 3.00, TEXT, 36)
        self.play(FadeIn(heading), run_time=0.42)

        relays = [
            ("the perforant path", "dentate gyrus", "Perforant path", "Dentate gyrus"),
            ("and mossy fibers", "feed ca3", "Mossy fibres", "CA3"),
            ("shaffer collaterals", "feed ca1", "Schaffer collaterals", "CA1"),
        ]
        name, destination = None, None
        for i, (cue, target, fibre, region) in enumerate(relays):
            self.at(cue, lead=0.45)
            path = world.paths[i]
            run = relay_pulse(path, RELAY_COLORS[i], seconds=1.65)
            self.add(run)
            new_name = label(fibre, 3.86, 3.02, RELAY_COLORS[i], 31)
            self.play(path.animate.set_stroke(opacity=1), run_time=0.36)
            self.play(swap(name, new_name, 0.38) if name else FadeIn(new_name), run_time=0.38)
            self.at(target, lead=0.25)
            new_destination = label(region, 3.86, 3.53, RELAY_COLORS[i], 30)
            self.play(world.nodes[i].animate.set_opacity(1),
                      swap(destination, new_destination, 0.44) if destination else FadeIn(new_destination),
                      run_time=0.44)
            name, destination = new_name, new_destination
        self.at("inside the neuropill")
        mesh = Ellipse(width=1.85, height=0.88, stroke_color=GREEN, stroke_width=2,
                       fill_color=GREEN, fill_opacity=0.16).move_to(p(1.62, 0.27))
        self.play(FadeIn(mesh), run_time=0.4)
        glia = VGroup(*[Dot(p(x, y), 0.068, color=GREEN)
                        for x, y in [(1.10, 0.45), (1.35, 0.63), (1.75, 0.04), (2.26, 0.29)]])
        for i, cell in enumerate(glia):
            bob(cell, amp=0.046, speed=2.5, seed=i)
        self.add(glia)
        self.play(FadeIn(label("CA1 neuropil", 1.62, -2.92, GREEN, 31)), run_time=0.4)
        self.finish()


class S04Record(SpokenScene):
    def construct(self):
        world = slice_stage(self)
        self.at("stimulate shaffer")
        self.play(world.animate.scale(1.12, about_point=ORIGIN).shift(p(-0.40, -0.04)),
                  run_time=0.82)
        stimulating = electrode(p(-3.80, 2.42), world.paths[2].get_start())
        self.play(GrowFromPoint(stimulating, stimulating.get_top()), run_time=0.58)
        self.at("release glutamate")
        target = world.paths[2].get_end()
        starts = [target + p(-0.31 + i * 0.055, 0.14) for i in range(12)]
        ends = [q + p(0.15, -0.43) for q in starts]
        release = droplets(ORANGE, starts, ends, seconds=1.32)
        stim_label = label("Stimulating electrode", -3.5, 3.05, BLUE)
        glut = label("Glutamate", -1.1, -2.89, ORANGE)
        self.add(release)
        self.play(FadeIn(stim_label), FadeIn(glut), run_time=0.45)

        self.at("a field electrode")
        field = electrode(p(0.62, 2.46), target + p(0.15, 0.38))
        field_label = label("Field electrode", 0.55, 3.05, BLUE)
        self.play(FadeOut(stim_label), FadeIn(field), FadeIn(field_label), run_time=0.65)
        self.at("the field epsp")
        sweep = ValueTracker(0.01)
        scope = response_scope(ValueTracker(1), sweep)
        self.add(scope)
        self.play(sweep.animate.set_value(1.8), FadeOut(glut), run_time=2.3, rate_func=linear)
        self.at("from many synapses")
        summed = label("Many synapses", 4.0, -2.82, TEXT)
        self.play(FadeIn(summed), run_time=0.45)

        self.at("a whole cell electrode")
        self.play(FadeOut(field), FadeOut(field_label), FadeOut(summed),
                  FadeOut(scope), run_time=0.4)
        one_cell = Dot(target + p(0.10, -0.52), radius=0.29, color="#A88FB7",
                       stroke_color=PURPLE, stroke_width=4)
        whole = electrode(p(-0.52, 2.34), one_cell.get_top())
        self.play(FadeIn(one_cell), FadeIn(whole), run_time=0.45)
        self.play(FadeIn(label("Whole-cell electrode", -0.76, 3.05, BLUE)), run_time=0.40)
        self.finish()


class S05Plasticity(SpokenScene):
    def construct(self):
        chamber = bath()
        amplitude = ValueTracker(1)
        scope = response_scope(amplitude, reference=True)
        self.add(chamber, stream(), synapse(), scope)

        self.at("control their chemistry")
        self.play(chamber.animate.set_fill("#28686D"), run_time=1.7)
        ampa, nmda = gate(-3.80), gate(-1.65)
        ampa_plug = panel(0.29, 0.38, -3.80, -0.60, PURPLE, PURPLE, 0.05)
        ampa_name = label("AMPA", -3.80, -2.76, PURPLE, 33)
        nmda_name = label("NMDA", -1.65, -2.76, PURPLE, 33)
        self.at("glutamate opens", lead=0.60)
        self.play(FadeIn(ampa), FadeIn(ampa_plug), run_time=0.38)
        self.add(transmitter())
        current = arrow(p(-3.80, -0.26), p(-3.80, -1.97))
        self.play(FadeOut(ampa_plug), GrowArrow(current), FadeIn(ampa_name), run_time=0.66)

        self.at("yet slower")
        mag = Dot(p(-1.65, -0.61), 0.154, color=RED)
        self.play(FadeIn(nmda), FadeIn(mag), run_time=0.35)
        self.play(FadeIn(nmda_name), run_time=0.37)
        self.at("blocked by magnesium")
        mag_name = label("Magnesium", -0.52, -1.54, RED)
        self.play(FadeIn(mag_name), run_time=0.39)

        self.at("also need glycine")
        coagonist = Dot(p(-1.36, -0.235), 0.12, color=GREEN)
        co_name = label("Glycine or D-serine", -2.62, 2.93, GREEN)
        self.play(FadeIn(coagonist, shift=DOWN * 0.24), run_time=0.51)
        self.play(FadeIn(co_name), run_time=0.39)
        self.at("depolarization relieves")
        depol = label("Depolarization", -2.62, 2.93, YELLOW)
        self.play(swap(co_name, depol, 0.56), chamber.animate.set_fill("#2C555A"), run_time=0.62)
        self.play(mag.animate.shift(p(0, 0.85)), FadeOut(mag_name), run_time=1.05)
        self.at("allowing larger current")
        added_current = arrow(p(-1.65, -0.27), p(-1.65, -1.97), width=12)
        self.play(GrowArrow(added_current), FadeOut(mag), run_time=0.8)
        self.at("lasting larger response")
        self.play(amplitude.animate.set_value(1.57), run_time=1.35)
        self.at("term potentiation")
        self.play(FadeIn(label("Long-term potentiation", 3.96, -2.89, YELLOW)),
                  FadeOut(depol), run_time=0.49)
        self.finish()


def tissue():
    """Dimensionless tissue volume strip constructed from four inside parts to one outside."""
    total = 12.1
    portion = total / (4 + 1)
    edge = -total / 2
    inside = panel(portion * 4, 3.50, edge + portion * 2, 0.42, "#A084B7", CELL, 0.27)
    outside = panel(portion, 3.50, edge + portion * 4.5, 0.42, "#5CAFAE", "#244D52", 0.23)
    cell = contour([(-5.73, 0.77), (-4.99, 1.73), (-3.71, 1.64), (-2.38, 1.19),
                    (-0.98, 1.52), (1.45, 1.29), (3.29, 0.65), (3.04, 0.10),
                    (1.52, 0.11), (-0.58, -0.43), (-2.16, -0.04), (-4.45, -0.38),
                    (-5.73, 0.77)], "#866B9E", 3, "#635074")
    glia = contour([(-5.59, -0.60), (-3.86, -0.58), (-2.35, -0.31), (-0.67, -0.65),
                    (0.45, -0.37), (1.66, -0.11), (3.13, -0.20), (3.25, -0.73),
                    (1.55, -0.98), (-1.05, -0.97), (-3.90, -1.07), (-5.59, -0.60)],
                   "#739578", 3, GLIA)
    out_text = label("Outside cells", 4.84, 2.98, TEAL, 30)
    in_text = label("Inside cells", -1.20, 2.98, PURPLE, 30)
    out_fraction = label("⅕", 4.84, 3.46, TEXT, 36)
    in_fraction = label("⅘", -1.20, 3.46, TEXT, 36)
    gap = label("Gaps tens of\nnanometres wide", 4.65, -1.91, TEXT, 28)
    return (VGroup(inside, outside, cell, glia), VGroup(out_text, out_fraction, gap),
            VGroup(in_text, in_fraction))


def potassium(flowing=True, dense=False, astrocyte=None):
    n = 16 if dense else 10
    outside = [p(4.15 + (i % 5) * 0.34, -0.78 + (i % 8) * 0.36) for i in range(n)]
    if astrocyte is not None:
        tip_x = astrocyte.get_right()[0]
        # Route upper particles farther out so they pass around the neuronal tip.
        starts = [p(max(x, 4.15 + 0.48 * max(y, 0)), y) for x, y, _ in outside]
        uptake = [p(tip_x - 0.26 - (i % 3) * 0.08, -0.54 + (i % 4) * 0.025)
                  for i in range(n)]
        return droplets(K_COLOR, starts, uptake, radius=0.098, seconds=1.5, run=flowing)
    neuron = [p(3.28 + (i % 3) * 0.11, -0.04 + (i % 6) * 0.25) for i in range(n)]
    return droplets(K_COLOR, neuron, outside, radius=0.098,
                    seconds=2.0 if dense else 2.95, run=flowing)


def predict_frame():
    bar, outside, inside = tissue()
    return VGroup(bar, outside, inside, potassium())


class S06PredictQ(SpokenScene):
    def construct(self):
        slice_stage(self)
        bar, outside, inside = tissue()
        self.at("in adult brain tissue", lead=1.25)
        old = Group(*self.mobjects)
        self.play(FadeOut(old), run_time=0.40)
        self.add(bath(), stream(lanes=(-2.28, -1.96, 2.40), span=9.22))
        self.play(FadeIn(bar), run_time=0.65)
        self.at("space outside cells")
        self.play(FadeIn(outside), run_time=0.53)
        self.at("fifths lies inside")
        self.play(FadeIn(inside), run_time=0.53)
        self.at("fire hard and leak")
        self.add(potassium())
        potassium_name = label("Potassium", -0.50, -3.10, K_COLOR)
        self.play(FadeIn(potassium_name), run_time=0.46)
        self.at("which side changes")
        self.play(swap(potassium_name, question_card(QUESTION, **QUESTION_STYLE), 0.58))
        self.finish()


class S07PredictPause(PredictPause):
    QUESTION = QUESTION
    CARD = QUESTION_STYLE
    SECONDS = 4.5

    def backdrop(self):
        return VGroup(bath(), stream(lanes=(-2.28, -1.96, 2.40), span=9.22), predict_frame())


class S08ControlsIons(SpokenScene):
    def construct(self):
        bar, outside, inside = tissue()
        ions = potassium()
        self.add(bath(), stream(lanes=(-2.28, -1.96, 2.40), span=9.22), bar, outside, inside, ions)
        narrow = bar[1]
        self.at("the outside space")
        self.play(narrow.animate.set_fill("#38646B"), run_time=0.7)
        self.at("the same leaked potassium")
        dose = caption("Same leaked potassium", color=K_COLOR, size=32)
        self.play(FadeIn(dose), run_time=0.43)
        self.at("quarter of the volume")
        volume = caption("Same potassium ÷ ¼ volume", color=K_COLOR, size=32)
        self.play(swap(dose, volume, 0.55))
        self.at("four times as much")
        equation = caption("Same potassium ÷ ¼ volume = 4 × the change", color=K_COLOR, size=32)
        self.play(swap(volume, equation, 0.55), narrow.animate.set_fill("#477980"))
        self.at("holds little potassium")
        self.play(FadeOut(ions), narrow.animate.set_fill("#244D52"), run_time=0.7)
        low = VGroup(Dot(p(4.34, 0.51), 0.10, color=K_COLOR), Dot(p(5.23, -0.42), 0.10, color=K_COLOR))
        for i, dot in enumerate(low):
            bob(dot, amp=0.1, speed=1.8, seed=i)
        self.add(low)
        self.play(FadeOut(equation), run_time=0.38)

        self.at("seizure like firing")
        dense = potassium(dense=True)
        self.add(dense)
        self.play(FadeOut(low), narrow.animate.set_fill("#4D6679"), run_time=1.0)
        self.at("can shift ek")
        ek = ValueTracker(0)
        gauge = dial(ek, p(-2.30, 0.90), radius=0.66, color=K_COLOR,
                     fmt="Scale: tens of mV", size=28)
        gauge_box = panel(4.8, 1.95, -2.30, 1.10, "#9480A1", BG)
        title = MarkupText("E<sub>K</sub> shift (schematic)", font=FONT, font_size=30,
                           color=TEXT).move_to(p(-2.30, 1.81))
        self.play(FadeIn(gauge_box), run_time=0.38)
        self.add(gauge, title)
        self.at("by tens of millivolts", lead=0.55)
        self.play(ek.animate.set_value(1), run_time=1.25)

        self.at("healthy astrocytes")
        glia = bar[3]
        cleared = potassium(dense=True, astrocyte=glia)
        astro = label("Astrocyte", -0.65, -2.86, GREEN, 31)
        self.play(FadeOut(dense), glia.animate.set_fill("#537851"), FadeIn(astro), run_time=0.42)
        self.add(cleared)
        self.play(ek.animate.set_value(0), narrow.animate.set_fill("#294F55"), run_time=1.2)
        self.at("high affinity transporters")
        self.play(FadeOut(gauge), FadeOut(title), FadeOut(cleared), run_time=0.23)
        self.play(FadeOut(gauge_box), run_time=0.18)
        gluts = droplets(ORANGE, [p(4.06 + i * 0.20, 0.38) for i in range(9)],
                          [p(3.31, -0.23 if i % 2 else 0.32) for i in range(9)], seconds=1.25)
        self.add(gluts)
        uptake = label("Glutamate uptake", -0.65, -2.86, ORANGE, 31)
        self.play(swap(astro, uptake, 0.62))
        self.finish()


class S09ControlsCircuits(SpokenScene):
    def construct(self):
        world = slice_stage(self)
        self.at("local circuits also")
        display = panel(3.82, 4.49, 4.55, 0.04, "#75949A", "#202E39")
        heading = label("Membrane voltage", 4.55, 1.74, TEXT, 30)
        track = Line(p(4.55, -1.48), p(4.55, 1.13), stroke_color=GREY, stroke_width=4)
        chloride = DashedLine(p(2.97, -0.92), p(6.12, -0.92), color=TEAL, stroke_width=3)
        v = ValueTracker(-0.52)
        dot = Dot(p(4.55, v.get_value()), 0.18, color=YELLOW)
        dot.add_updater(lambda m: m.move_to(p(4.55, v.get_value())))
        self.play(FadeIn(display), run_time=0.54)
        self.play(FadeIn(heading), Create(track), FadeIn(dot), run_time=0.64)
        self.at("excitatory glutamate")
        excit = arrow(p(3.57, -0.52), p(3.57, 0.91), ORANGE, 7)
        excitation = label("Glutamate", -2.82, 2.92, ORANGE, 33)
        self.play(GrowArrow(excit), FadeIn(excitation), run_time=0.60)
        self.at("pulls voltage up")
        self.play(v.animate.set_value(0.85), run_time=0.84)
        self.at("inhibitory transmitter gaba")
        gaba = label("GABA", -2.82, 2.92, TEAL, 33)
        interneuron = Circle(radius=0.24, stroke_width=3, stroke_color=TEAL,
                            fill_color="#1D5C61", fill_opacity=1).move_to(p(0.76, -0.64))
        connection = contour([(0.94, -0.59), (1.23, -0.19), (1.54, -0.10), (1.74, -0.05)], TEAL)
        self.play(swap(excitation, gaba, 0.47), FadeIn(interneuron), Create(connection),
                  run_time=0.53)
        self.at("opens chloride channels")
        down = arrow(p(5.51, 0.84), p(5.51, -0.80), TEAL, 7)
        self.play(GrowArrow(down), Create(chloride), run_time=0.56)
        self.at("near chloride's equilibrium")
        level = label("Chloride equilibrium", 4.55, -1.77, TEAL, 28)
        self.play(v.animate.set_value(-0.85), FadeIn(level), run_time=1.14)
        self.at("even in one hippocampus")
        self.play(FadeOut(level), run_time=0.27)
        self.play(FadeOut(VGroup(display, heading, track, chloride, dot, down, excit)),
                  FadeOut(gaba), FadeOut(interneuron), FadeOut(connection), run_time=0.62)
        self.at("mossy fiber to")
        self.add(relay_pulse(world.paths[1], PURPLE, seconds=1.25))
        pulse(world.paths[1], base=6, amp=2.1, speed=3)
        self.play(FadeIn(label("Mossy fibres → CA3", 2.25, 3.07, PURPLE, 33)), run_time=0.55)
        self.finish()


class S10UnlockedPlasticity(SpokenScene):
    def construct(self):
        world = slice_stage(self, active=())
        self.at("synapses strengthen and weaken")
        self.add(relay_pulse(world.paths[2], YELLOW))
        self.at("first measured in rabbits")
        historical = label("First measured in live rabbits", 0, 3.08, GOLD, 34)
        path = world.paths[0]
        self.add(relay_pulse(path, BLUE, seconds=1.4))
        self.play(path.animate.set_stroke(width=9), run_time=0.53)
        self.play(FadeIn(historical), run_time=0.45)
        self.at("perforant path to")
        ribbon = label("Perforant path → dentate gyrus", -1.32, -2.92, BLUE, 31)
        self.play(FadeIn(ribbon), run_time=0.56)
        self.at("rat hippocampal slices")
        self.play(FadeOut(historical), FadeOut(ribbon), path.animate.set_stroke(width=4), run_time=0.46)
        amplitude = ValueTracker(1)
        sweep = ValueTracker(0.04)
        scope = response_scope(amplitude, sweep, reference=True)
        self.add(scope)
        self.play(sweep.animate.set_value(1.8), run_time=1.75, rate_func=linear)
        self.at("shaffer collateral to")
        ltp = label("Long-term potentiation", 4.04, -2.90, YELLOW, 30)
        schaffer = label("Schaffer collaterals → CA1", -2.56, 2.89, YELLOW, 32)
        self.play(FadeIn(schaffer), amplitude.animate.set_value(1.55), run_time=1.22)
        self.play(FadeIn(ltp), run_time=0.42)

        self.at("group 1 metabolotropic")
        self.play(FadeOut(ltp), FadeOut(schaffer), amplitude.animate.set_value(1), run_time=0.62)
        receptor = Circle(radius=0.18, stroke_color=PURPLE, stroke_width=5, fill_color=BG,
                          fill_opacity=1).move_to(p(1.41, 0.56))
        self.play(FadeIn(receptor), run_time=0.48)
        self.at("like m glue r5")
        compound = Dot(p(0.67, 0.76), 0.12, color=ORANGE)
        nm = label("mGluR5", -1.54, 2.90, PURPLE, 34)
        self.play(FadeIn(nm), FadeIn(compound), run_time=0.47)
        self.play(compound.animate.move_to(p(1.31, 0.70)), run_time=0.72)
        self.at("long term depression")
        ltd = label("Long-term depression", 4.04, -2.90, YELLOW, 30)
        self.play(amplitude.animate.set_value(0.42), run_time=0.88)
        self.play(FadeIn(ltd), run_time=0.42)
        self.at("lasting hours")
        hours = label("Lasts hours", -1.77, -2.91, TEXT, 30)
        self.play(FadeIn(hours), run_time=0.38)
        self.at("block protein synthesis")
        block = label("Protein synthesis blocked", -2.51, 3.07, RED, 31)
        self.play(swap(nm, block, 0.62), FadeOut(compound), FadeOut(receptor), FadeOut(hours), run_time=0.62)
        self.at("weakening does not last")
        self.play(amplitude.animate.set_value(1), FadeOut(ltd), run_time=0.94)
        self.finish()


def ca1_neurons():
    """CA1 dendrites and somata with a gap where the preparation is cut."""
    dendrites, bodies = VGroup(), VGroup()
    for i, y in enumerate(np.linspace(-0.28, 1.43, 4)):
        x = -2.90 + i * 0.16
        branch = contour([(-5.33, y + 0.12), (-4.58, y + 0.01), (-3.79, y - 0.15),
                          (x - 0.07, y - 0.16)], PURPLE, 6)
        contact = Dot(branch.get_start(), radius=0.075, color=YELLOW)
        dendrites.add(VGroup(branch, contact))
        bodies.add(VGroup(Line(p(x + 0.07, y - 0.16), p(-1.22, y - 0.22),
                               stroke_color=PURPLE, stroke_width=6),
                          Dot(p(-1.22, y - 0.22), 0.18, color="#A98DBE")))
    return dendrites, bodies


class S11UnlockedLocal(SpokenScene):
    def construct(self):
        world = slice_stage(self)
        amplitude = ValueTracker(1)
        scope = response_scope(amplitude, reference=True)
        self.add(scope)
        self.at("in 1996")
        credit = label("Kang and Schuman, 1996", -2.45, 3.08, GOLD, 32)
        self.play(FadeIn(credit), run_time=0.52)
        self.at("applied growth factor")
        bdnf = stream(ORANGE, lanes=(-1.21, -0.80, 1.34, 1.53), speed=1.19)
        self.add(bdnf)
        self.bring_to_front(world, scope, credit)
        bdnf_name = label("BDNF", -2.84, -2.88, ORANGE, 33)
        self.play(FadeIn(bdnf_name), run_time=0.50)
        self.at("synapses strengthened")
        self.play(amplitude.animate.set_value(1.48), run_time=1.18)

        self.at("cut the slices", lead=0.53)
        dendrites, bodies = ca1_neurons()
        world.save_state()
        self.play(world.animate.fade(0.68), FadeIn(dendrites), FadeIn(bodies), FadeOut(bdnf_name),
                  amplitude.animate.set_value(1), run_time=0.61)
        cutline = DashedLine(p(-2.64, -0.99), p(-2.64, 1.84), color=TEXT, stroke_width=4)
        self.play(dendrites.animate.shift(LEFT * 0.25), bodies.animate.shift(RIGHT * 0.18),
                  Create(cutline), run_time=0.65)
        self.at("separate synapses from")
        synapses = label("Synapses", -4.74, -2.91, PURPLE)
        somata = label("Cell bodies", -1.18, -2.91, PURPLE)
        self.play(FadeIn(synapses), FadeIn(somata), run_time=0.43)
        self.play(amplitude.animate.set_value(1.48), run_time=1.27)

        self.at("depended on protein synthesis")
        local = label("Local protein synthesis", -2.45, 3.08, GREEN, 32)
        self.play(swap(credit, local, 0.55))
        self.at("made near the synapses")
        local_glow = droplets(GREEN, [p(-5.5, y) for y in np.linspace(-0.34, 1.50, 12)],
                              [p(-3.31, y - 0.18) for y in np.linspace(-0.34, 1.50, 12)],
                              radius=0.09, seconds=1.9)
        self.add(local_glow)
        self.at("living circuits open")
        self.play(FadeOut(dendrites), FadeOut(bodies), FadeOut(local_glow),
                  FadeOut(cutline), FadeOut(synapses), FadeOut(somata), FadeOut(bdnf),
                  FadeOut(local), Restore(world), run_time=1.10)
        pulse(world.paths[2], base=6, amp=2.7, speed=2.6)
        self.finish()


class S12End(EndCard):
    LINE = "Living brain slices keep circuits intact for controlled synaptic recording."
