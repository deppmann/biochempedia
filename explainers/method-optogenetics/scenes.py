"""Optogenetics: one cell and its electrical recording, carried through the trials.

Color map: blue and yellow are the two light inputs, green is electrical
activity, red is warming, purple is membrane protein, grey is structure,
teal is chloride, and gold marks the prediction and historical captions.
"""
from bp_parts import *

PURPLE = "#B58CD9"
CELL = "#3C5367"
TISSUE = "#344352"
SCREEN = "#222D3B"
EDGE = "#62738A"
SOURCE_X = -3.42
MEMBRANE_Y = 0.65
WINDOW = 7.0
QUESTION = "What if spikes drop?"


def at_xy(x, y):
    return np.array([x, y, 0.0])


def rect(x, y, w, h, fill, edge=None, radius=0.16):
    return RoundedRectangle(
        width=w, height=h, corner_radius=radius, fill_color=fill,
        fill_opacity=1, stroke_color=edge or fill, stroke_width=2 if edge else 0,
    ).move_to(at_xy(x, y))


def line_path(points, color, width):
    path = VMobject(stroke_color=color, stroke_width=width)
    return path.set_points_smoothly([at_xy(x, y) for x, y in points])


def heading(label, x=0.82, y=3.26, color=TEXT):
    return fit_text(label, max_w=min(5.10, 5.94 - x), size=32, min_size=28,
                    color=color, weight=BOLD, max_lines=2).move_to(at_xy(x, y), aligned_edge=LEFT)


def scope():
    return scope_tag("Schematic", size=28, color=TEXT)


def neuron():
    """The soma, dendrites and axon used in every view of the same cell."""
    axon = line_path(
        [(-3.45, -1.28), (-2.74, -1.84), (-1.62, -1.95), (-0.64, -1.77), (0.04, -2.12)],
        CELL, 16,
    )
    branches = VGroup(
        line_path([(-4.75, -0.22), (-5.55, 0.28), (-6.1, 0.93)], EDGE, 10),
        line_path([(-5.43, 0.23), (-5.89, 0.18), (-6.28, 0.35)], EDGE, 7),
        line_path([(-4.8, -0.73), (-5.46, -1.04), (-6.08, -1.72)], EDGE, 10),
        line_path([(-5.44, -1.08), (-5.99, -1.13), (-6.31, -0.98)], EDGE, 7),
        line_path([(-1.06, -1.84), (-0.48, -1.43), (-0.10, -1.40)], CELL, 9),
    )
    soma = line_path(
        [(-3.42, MEMBRANE_Y), (-2.51, 0.43), (-2.06, -0.43), (-2.58, -1.37),
         (-3.58, -1.65), (-4.70, -1.30), (-5.01, -0.47), (-4.53, 0.30),
         (-3.42, MEMBRANE_Y)], GREY, 4,
    ).set_fill(CELL, 1)
    soma.close_path()
    return VGroup(branches, axon, soma), axon


def smaller_cell(x, y, scale):
    cell, _ = neuron()
    cell.scale(scale).move_to(at_xy(x, y))
    return cell


def tissue():
    field = rect(-3.10, -0.30, 6.82, 5.00, TISSUE, EDGE, radius=0.46)
    return VGroup(field, smaller_cell(-1.59, 1.00, 0.36),
                  smaller_cell(-5.20, 1.58, 0.30))


def culture_dish():
    return rect(-3.11, -0.50, 6.88, 5.00, TISSUE, EDGE, radius=0.85).set_stroke(width=5)


def optical_source():
    body = rect(SOURCE_X, 2.55, 1.00, 0.57, SCREEN, GREY)
    lens = rect(SOURCE_X, 2.25, 0.61, 0.13, GREY, radius=0.05)
    return VGroup(body, lens)


def light_cone(clock, drive, color=BLUE, wide=False, *, top=2.20):
    spread = 2.56 if wide else 1.14
    bottom = -2.72 if wide else 0.18
    cone = Polygon(
        at_xy(SOURCE_X - 0.28, top), at_xy(SOURCE_X + 0.28, top),
        at_xy(SOURCE_X + spread, bottom), at_xy(SOURCE_X - spread, bottom),
        stroke_width=0, fill_color=color,
    )

    def illuminate(m):
        t = clock.get_value()
        m.set_fill(opacity=drive(t) * (0.31 + (0.115 if wide else 0.045) * np.sin(3.6 * t)))

    illuminate(cone)
    return cone.add_updater(illuminate)


def protein(kind="gate", open_amount=0):
    if kind == "pump":
        outer = rect(SOURCE_X, MEMBRANE_Y, 0.92, 0.81, PURPLE, radius=0.22)
        pore = rect(SOURCE_X, MEMBRANE_Y, 0.33, 0.58, BG, radius=0.12)
        return VGroup(outer, pore)
    left = rect(SOURCE_X - 0.22 - open_amount, MEMBRANE_Y, 0.39, 0.81, PURPLE)
    right = left.copy().move_to(at_xy(SOURCE_X + 0.22 + open_amount, MEMBRANE_Y))
    return VGroup(left, right)


def membrane_view():
    cytoplasm = Polygon(at_xy(-6.34, -2.64), at_xy(-0.50, -2.64),
                         at_xy(-0.50, MEMBRANE_Y), at_xy(-6.34, MEMBRANE_Y),
                         stroke_width=0, fill_color=CELL, fill_opacity=1)
    membrane = VGroup(
        rect(-5.12, MEMBRANE_Y, 2.43, 0.51, EDGE, radius=0.12),
        rect(-1.72, MEMBRANE_Y, 2.43, 0.51, EDGE, radius=0.12),
    )
    return VGroup(cytoplasm, membrane)


def gene_tile():
    return boxed_label("Gene", color=TEXT, size=30, fill_opacity=0.13).move_to(at_xy(-3.56, -0.53))


def ions(clock, start, negative=False):
    """Qualitative ion flow. Charge signs are geometric icons inside badges."""
    badges = VGroup()
    for i in range(6):
        color = TEAL if negative else TEXT
        disk = Circle(radius=0.15, fill_color=SCREEN, fill_opacity=1,
                      stroke_color=color, stroke_width=2.5)
        sign = VGroup(Line(LEFT * 0.063, RIGHT * 0.063, stroke_width=4, color=color))
        if not negative:
            sign.add(Line(DOWN * 0.063, UP * 0.063, stroke_width=4, color=color))
        badge = VGroup(disk, sign)

        def drift(m, index=i):
            age = clock.get_value() - start - index * 0.61
            phase = (age % 3.66) / 3.66
            x = SOURCE_X + 0.59 * np.sin(index * 2.4) * (1 - phase) ** 6
            m.move_to(at_xy(x, 1.89 - 4.04 * phase))
            m.set_opacity(min(1, 13 * phase, 10 * (1 - phase)) if age >= 0 else 0)

        drift(badge)
        badges.add(badge.add_updater(drift))
    return badges


def spike(t):
    """Normalized, schematic action potential: fast rise, fall and small undershoot."""
    age = np.maximum(t, 0)
    activation = (age / 0.103) ** 2 * np.exp(2 * (1 - age / 0.103))
    recovery = 0.13 * np.exp(-((age - 0.44) / 0.15) ** 2)
    return np.where(t >= 0, activation - recovery, 0)


def ramp(t, start, tau=0.48):
    return 1 - np.exp(-np.maximum(t - start, 0) / tau)


def voltage(t, spikes=(), level=None):
    baseline = 0.24 if level is None else level(t)
    amplitude = np.minimum(0.59, 0.94 - baseline)
    return baseline + amplitude * sum((spike(t - onset) for onset in spikes), np.zeros_like(t))


def intervals(t, spans):
    return sum(
        (np.asarray((t >= start) & (t < end), dtype=float) for start, end in spans), np.zeros_like(t, dtype=float)
    ).clip(0, 1)


def screen():
    return rect(3.58, 0.04, 5.88, 5.40, SCREEN, EDGE, radius=0.28)


def sweep(clock, plot, origin, window):
    """A moving recording head keeps the direction of time visible between events."""
    width = 0.78
    region = rect(0, 0, width, plot.y1 - plot.y0 + 0.04, "#627B94", radius=0.06)
    region.set_fill(opacity=0.64)

    def move(m):
        x = plot.x1 - width / 2 - ((clock.get_value() - origin) % window) * (
            (plot.x1 - plot.x0 - width) / window)
        m.move_to(at_xy(x, (plot.y0 + plot.y1) / 2))

    move(region)
    return region.add_updater(move)


def recording(clock, signal=None, *, bounds=(1.06, 6.10, -1.77, 1.48),
              light=(), color=BLUE, threshold=False, origin=0, window=WINDOW):
    """Draw a rolling, shared time window for voltage and the light input."""
    plot = Plot(box=bounds, xr=(0, window), yr=(0, 1), color=EDGE, stroke=2)
    group = VGroup(plot)
    if signal is None:
        return group
    group.add_to_back(sweep(clock, plot, origin, window))
    group.add(plot.hline(0.55, color=GREY) if threshold else VGroup())
    xs = np.linspace(0, window, round(280 * window / WINDOW))

    def redraw():
        now = clock.get_value() - origin
        values = signal(xs + now - window)
        return plot.curve(lambda x: np.interp(x, xs, values), color=GREEN, width=5, n=len(xs))

    group.add(always_redraw(redraw))
    if light:
        track_y = plot.y0 - 0.42
        group.add(Line(at_xy(plot.x0, track_y), at_xy(plot.x1, track_y), color=EDGE, stroke_width=2))
        for start, end in light:
            mark = Line(LEFT, RIGHT, color=color, stroke_width=9)

            def scroll(m, start=start, end=end):
                now = clock.get_value() - origin
                a, b = np.clip((start - now + window, end - now + window), 0, window)
                x = plot.pt(a, 0)[0]
                right = max(x + 0.001, plot.pt(b, 0)[0])
                m.put_start_and_end_on(at_xy(x, track_y), at_xy(right, track_y))
                m.set_stroke(opacity=min(1, max(0, (b - a) * 20)))

            scroll(mark)
            group.add(mark.add_updater(scroll))
    return group


def axon_pulse(clock, axon, starts):
    glow = VGroup(Dot(radius=0.21, color=GREEN, fill_opacity=0.23),
                  Dot(radius=0.105, color=GREEN))

    def propagate(m):
        phase = clock.get_value() - max((t for t in starts if t <= clock.get_value()), default=-10)
        amount = np.clip(phase / 0.9, 0, 1)
        m.move_to(axon.point_from_proportion(amount))
        m[0].set_opacity(0.28 * np.sin(PI * amount))
        m[1].set_opacity(np.sin(PI * amount))

    propagate(glow)
    return glow.add_updater(propagate)


def control_world(clock, question=False):
    cell, _ = neuron()
    view = VGroup(tissue(), cell, light_cone(clock, lambda t: 1, YELLOW, wide=True), optical_source())
    label = heading("Without the opsin", x=-6.30)
    panel = screen()
    if question:
        panel = VGroup(panel, recording(clock), predict_card())
    return view, label, panel


def predict_card():
    card = question_card(QUESTION, y=0.50, size=42, color=TEXT, left=1.52, max_w=4.44)
    return card


class OptogeneticsScene(SpokenScene):
    def start(self):
        clock = ValueTracker(0)
        clock.add_updater(lambda m, dt: m.increment_value(dt))
        self.add(clock, scope())
        return clock


class S01Hook(OptogeneticsScene, TitleCard):
    LESSON = "Optogenetics"
    TITLE = "What Can a Flash Make a Neuron Do?"

    def construct(self):
        clock = self.start()
        flash = self.t_of("the flash above")
        events = ((flash, flash + 0.62),)
        drive = lambda t: intervals(t, events)
        cell, axon = neuron()
        panel = screen()
        self.add(cell, light_cone(clock, drive), optical_source(), panel,
                 recording(clock, lambda t: voltage(t, (flash + 0.13,)), light=events, window=12),
                 axon_pulse(clock, axon, (flash + 0.13,)))
        self.at("on cue", lead=0)
        title = caption(self.TITLE, size=36, y=-3.19)
        self.play(FadeIn(title), run_time=0.20)
        self.wait(0.85)
        self.play(FadeOut(title), run_time=0.25)
        self.at("electrical recording")
        label = heading("Electrical recording")
        self.play(FadeIn(label), run_time=0.35)
        self.at("sharp peak")
        self.play(swap(label, heading("Spike", color=GREEN)), run_time=0.45)
        self.finish()


class S02ChooseCells(OptogeneticsScene):
    def construct(self):
        clock = self.start()
        cell, _ = neuron()
        source = optical_source()
        neighbor = smaller_cell(-0.95, 0.65, 0.28)
        gene = gene_tile()
        gate = protein()
        overview = VGroup(cell, source)
        self.add(overview, screen(), recording(clock, voltage))
        self.at("its target")
        self.play(FadeIn(neighbor), run_time=0.60)
        self.at("a gene")
        self.play(FadeIn(gene, scale=0.8), run_time=0.55)
        self.at("selected neurons")
        name = heading("Selected neuron", x=-6.30)
        self.play(FadeIn(name), run_time=0.50)
        self.at("light sensitive protein")
        self.play(FadeIn(gate, shift=UP * 0.60), run_time=0.72)
        self.at("called an opsin")
        opsin = heading("Opsin", color=PURPLE)
        self.play(FadeIn(opsin), run_time=0.45)
        self.at("which sits in")
        self.play(FadeOut(neighbor), FadeOut(gene), FadeOut(name),
                  FadeOut(cell), FadeIn(membrane_view()), run_time=0.85)
        self.bring_to_front(gate)
        self.at("the cell's thin boundary")
        self.play(swap(opsin, heading("Cell membrane")), run_time=0.52)
        self.finish()


class S03OpenChannel(OptogeneticsScene):
    def construct(self):
        clock = self.start()
        influx = self.t_of("positive charge flow") - 0.38
        level = lambda t: 0.24 + 0.27 * ramp(t, influx + 1.12, 3.3)
        gate = protein()
        panel = screen()
        self.add(membrane_view(), gate, optical_source(), panel,
                 recording(clock, lambda t: voltage(t, level=level)))
        self.at("channel rhodopsin 2")
        name = heading("Channelrhodopsin-2", color=PURPLE)
        self.play(FadeIn(name), run_time=0.45)
        self.at("under blue light")
        cone = light_cone(clock, lambda t: 1)
        self.add(cone)
        self.bring_to_front(gate)
        self.play(Transform(gate, protein(open_amount=0.20)), run_time=0.48)
        self.at("positive charge flow")
        self.add(ions(clock, influx))
        self.at("particles are ions")
        charge = heading("Positive ions", color=TEXT)
        self.play(swap(name, charge), run_time=0.55)
        self.at("inside less negative")
        self.play(swap(charge, heading("Voltage rises", color=GREEN)), run_time=0.55)
        self.finish()


class S04Fire(OptogeneticsScene):
    def construct(self):
        clock = self.start()
        first = self.t_of("spike shoots") - 0.14
        repeat = self.t_of("flash after flash")
        flashes = (repeat, repeat + 2.05, repeat + 4.10, repeat + 6.15)
        events = ((-2, first + 0.26),) + tuple((t, t + 0.42) for t in flashes)
        spikes = (first,) + tuple(t + 0.12 for t in flashes)
        level = lambda t: 0.24 + (0.25 + 0.09 * ramp(t, 0, 2.2)) * (1 - ramp(t, first, 0.23))
        cell, axon = neuron()
        gate = protein(open_amount=0.18)
        patch = membrane_view()
        cone = light_cone(clock, lambda t: intervals(t, events))
        self.add(patch, cone, optical_source(), gate, screen(),
                 recording(clock, lambda t: voltage(t, spikes, level), light=events, threshold=True),
                 heading("Firing threshold", y=1.95))
        self.at("voltage reaches")
        self.play(FadeOut(patch), FadeIn(cell), run_time=0.85)
        self.add(axon_pulse(clock, axon, spikes))
        self.bring_to_front(cone, gate)
        self.at("flash after flash")
        self.play(FadeIn(heading("Light and spikes")), run_time=0.45)
        self.finish()


class S05Silence(OptogeneticsScene):
    def construct(self):
        clock = self.start()
        light_on = self.t_of("yellow light") - 0.13
        events = ((light_on, 25),)
        spikes = tuple(np.arange(-8, light_on - 0.20, 1.43))
        level = lambda t: 0.24 - 0.11 * ramp(t, light_on + 0.50, 0.85)
        cell, _ = neuron()
        patch = membrane_view()
        gate = protein()
        self.add(cell, optical_source(), gate, screen(),
                 recording(clock, lambda t: voltage(t, spikes, level),
                           light=events, color=YELLOW, threshold=True),
                 heading("Firing threshold", y=1.95))
        self.at("a different opsin")
        self.play(FadeOut(cell), FadeIn(patch), Transform(gate, protein("pump")), run_time=0.88)
        self.bring_to_front(gate)
        self.at("halorhodopsin is")
        name = heading("Halorhodopsin", color=PURPLE)
        self.play(FadeIn(name), run_time=0.45)
        self.at("yellow light")
        self.add(light_cone(clock, lambda t: intervals(t, events), YELLOW))
        self.bring_to_front(gate)
        self.at("negative chloride ions")
        self.add(ions(clock, clock.get_value(), negative=True))
        self.play(swap(name, heading("Chloride ions", color=TEAL)), run_time=0.50)
        self.at("can stop spikes")
        self.finish()


class S06GuidingIdea(OptogeneticsScene):
    def construct(self):
        clock = self.start()
        on = self.t_of("the beam reaches tissue") - 0.2
        light = ((on, 30),)
        flashes = tuple(np.arange(-8, on - 0.2, 1.22)) + (on + 0.6, on + 3.9, on + 7.4)
        cell, _ = neuron()
        field = tissue()
        gene = gene_tile()
        gate = protein("pump")
        drive = lambda t: intervals(t, light)
        self.add(cell, light_cone(clock, drive, YELLOW, wide=True), optical_source(), gate,
                 screen(), recording(clock, lambda t: voltage(t, flashes), light=light, color=YELLOW))
        self.at("gene choosing")
        self.play(FadeIn(gene), run_time=0.50)
        self.at("light choosing")
        self.play(FadeOut(gene), run_time=0.55)
        self.at("test what their activity causes")
        rule = caption("Choose the cells and the moment", size=32)
        self.play(FadeIn(rule), run_time=0.50)
        self.at("the beam reaches tissue")
        self.bring_to_back(field)
        self.play(FadeIn(field), FadeOut(rule), run_time=0.75)
        self.at("spikes on your recording")
        self.play(FadeIn(heading("With the opsin")), run_time=0.45)
        self.finish()


class S07Predict(OptogeneticsScene):
    def construct(self):
        clock = self.start()
        view, label, panel = control_world(clock)
        gate = protein("pump")
        trace = recording(clock, lambda t: voltage(t, (-6.8, -3.5, -0.2)), light=((-8, 20),), color=YELLOW)
        old = heading("With the opsin")
        self.add(view, gate, panel, trace, old)
        self.at("now keep")
        self.play(FadeOut(trace), run_time=0.60)
        self.add(recording(clock))
        self.at("tissue without the opsin")
        self.play(FadeOut(gate), swap(old, label), run_time=0.70)
        self.at("what would fewer spikes")
        self.play(FadeIn(predict_card()), run_time=0.50)
        self.finish()


class S08Think(Scene):
    def construct(self):
        self.camera.background_color = BG
        clock = ValueTracker(8.95)
        clock.add_updater(lambda m, dt: m.increment_value(dt))
        self.add(clock, scope(), *control_world(clock, question=True))
        self.wait(4.5)


class S09MatchedControl(OptogeneticsScene):
    def construct(self):
        clock = self.start()
        view, label, panel = control_world(clock)
        on = -4.5
        light = ((on, 30),)
        control_spikes = (-7.9, -6.8, -5.7, -4.6, -2.4, 1.25, 5.1, 9.1, 13.0, 17.1)
        opsin_spikes = (-7.9, -6.8, -5.7, -4.6, -1.35, 4.5, 10.7, 16.6)
        question = predict_card()
        self.add(view, label, panel, question)
        self.at("fewer spikes without")
        self.remove(question)
        trace = recording(clock, lambda t: voltage(t, control_spikes), light=light, color=YELLOW)
        self.add(trace)
        self.at("continuous light")
        finding = heading("Light alone affects firing")
        self.play(FadeIn(finding), run_time=0.55)
        self.at("light can warm tissue")
        heat = Ellipse(width=4.75, height=3.65, fill_color=RED, fill_opacity=0.19,
                       stroke_width=0).move_to(at_xy(-3.39, -0.78))
        self.play(FadeIn(heat), FadeOut(finding), run_time=0.68)
        self.at("compare recordings")
        self.remove(trace)
        review_start = clock.get_value() - (on + 2.4)
        top = recording(clock, lambda t: voltage(t, control_spikes), bounds=(1.06, 6.10, 0.62, 1.98),
                        light=light, color=YELLOW, origin=review_start)
        bottom = recording(clock, lambda t: voltage(t, opsin_spikes), bounds=(1.06, 6.10, -2.18, -0.78),
                           light=light, color=YELLOW, origin=review_start)
        self.add(top, bottom)
        self.play(FadeIn(heading("Without opsin", x=1.09, y=2.34)),
                  FadeIn(heading("With opsin", x=1.09, y=-0.38)), run_time=0.47)
        self.finish()


class S10CheckFiring(OptogeneticsScene):
    def construct(self):
        clock = self.start()
        on = self.t_of("while the light")
        switch = self.t_of("keep recording") + 0.52
        off = self.t_of("abruptly ending silencing") + 0.60
        blue = ((on, switch),)
        yellow = ((-4.2, off - switch),)
        high = lambda t: 0.24 + 0.52 * ramp(t, on, 1.50)
        low = lambda t: 0.24 - 0.11 * (ramp(t, -4.2, 0.38) - ramp(t, off - switch, 0.28))
        cell, axon = neuron()
        gate = protein()
        panel = screen()
        firing = (on + 0.17, on + 1.02, on + 2.21)
        excited = recording(clock, lambda t: voltage(t, firing, high), light=blue)
        cone = light_cone(clock, lambda t: intervals(t, blue))
        name = heading("Excitation")
        self.add(cell, cone, gate, optical_source(), panel, excited, axon_pulse(clock, axon, firing), name)
        self.at("while the light")
        self.play(Transform(gate, protein(open_amount=0.18)), run_time=0.44)
        self.at("voltage too high")
        high_label = heading("Voltage stays high", color=GREEN)
        self.play(swap(name, high_label), run_time=0.48)
        self.at("keep recording")
        silence_label = heading("Silencing")
        self.play(swap(high_label, silence_label, run_time=0.56),
                  Transform(gate, protein("pump")), run_time=0.56)
        self.remove(excited, cone)
        rebound = (off + 0.16, off + 0.77, off + 1.50, off + 2.35)
        spike_times = (-6.5, -5.35, -4.42) + tuple(t - switch for t in rebound)
        self.add(light_cone(clock, lambda t: intervals(t - switch, yellow), YELLOW),
                 recording(clock, lambda t: voltage(t, spike_times, low), light=yellow, color=YELLOW, origin=switch),
                 axon_pulse(clock, axon, rebound))
        self.bring_to_front(gate)
        self.at("rebound firing")
        self.play(swap(silence_label, heading("Rebound firing", color=GREEN)), run_time=0.48)
        self.finish()


class S11FollowFlashes(OptogeneticsScene):
    def construct(self):
        clock = self.start()
        result = self.t_of("fired in step")
        flashes = (result - 0.17, result + 0.87, result + 1.96, result + 3.00)
        light = tuple((t, t + 0.23) for t in flashes)
        spikes = tuple(t + 0.11 for t in flashes)
        cell, axon = neuron()
        dish = culture_dish()
        self.add(cell, optical_source(), screen(), recording(clock, lambda t: voltage(t, spikes), light=light))
        self.at("edward boyden")
        date = heading("Boyden et al. · 2005", color=GOLD)
        self.play(FadeIn(date), run_time=0.54)
        self.at("brain cells grown")
        self.bring_to_back(dish)
        self.play(GrowFromCenter(dish), run_time=1.2)
        self.at("hippocampal neurons")
        culture = heading("Hippocampal neurons")
        self.play(swap(date, culture), run_time=0.55)
        self.at("gene for")
        gate = protein()
        self.play(FadeIn(gate, shift=UP * 0.26), run_time=0.58)
        self.at("channel rhodopsin 2")
        name = heading("Channelrhodopsin-2", color=PURPLE)
        self.play(swap(culture, name), run_time=0.55)
        self.at("the cells fired")
        self.add(light_cone(clock, lambda t: intervals(t, light), top=dish.get_top()[1]),
                 axon_pulse(clock, axon, spikes))
        self.bring_to_front(gate)
        self.at("millisecond flashes")
        self.play(swap(name, heading("Light and spikes")), run_time=0.55)
        self.finish()


def mouse():
    tail = line_path([(-3.50, -1.54), (-4.39, -2.33), (-5.47, -2.05), (-6.34, -1.83)], GREY, 7)
    body = Ellipse(width=4.30, height=3.30, stroke_color=GREY, stroke_width=3,
                   fill_color=CELL, fill_opacity=1).rotate(0.14).move_to(at_xy(-3.92, -0.64))
    ear = Circle(radius=0.59, color=GREY, stroke_width=3, fill_color=CELL,
                 fill_opacity=1).move_to(at_xy(-2.82, 1.16))
    head = line_path([(-3.44, -0.66), (-3.35, 0.33), (-2.82, 0.88), (-2.05, 0.85),
                      (-1.58, 0.41), (-0.76, 0.06), (-1.19, -0.46), (-2.09, -0.77),
                      (-3.44, -0.66)], GREY, 3).set_fill(CELL, 1)
    head.close_path()
    foot = line_path([(-3.48, -1.93), (-2.99, -2.26), (-2.37, -2.26)], GREY, 7)
    eye = Dot(at_xy(-1.71, 0.31), radius=0.08, color=TEXT)
    brain = Ellipse(width=1.13, height=0.58, stroke_color=PURPLE, stroke_width=2,
                    fill_color=PURPLE, fill_opacity=0.47).move_to(at_xy(-2.56, 0.36))
    return VGroup(tail, body, ear, head, foot, eye, brain)


def optical_fibre(clock):
    x = -2.56
    wire = line_path([(-4.80, 2.50), (-3.67, 2.51), (x, 1.95), (x, 0.62)], GREY, 8)
    tip = Dot(at_xy(x, 0.60), radius=0.10, color=BLUE)
    halo = Ellipse(width=0.94, height=0.52, fill_color=BLUE, fill_opacity=0.20,
                   stroke_width=0).move_to(at_xy(x, 0.34))
    cue = Dot(radius=0.13, color=BLUE)

    def carry_light(m):
        phase = (clock.get_value() * 0.9) % 1
        m.move_to(wire.point_from_proportion(phase))
        m.set_opacity(np.sin(PI * phase))

    cue.add_updater(carry_light)
    cone = Polygon(at_xy(x - 0.05, 0.61), at_xy(x + 0.05, 0.61),
                   at_xy(x + 0.26, 0.15), at_xy(x - 0.26, 0.15),
                   stroke_width=0, fill_color=BLUE, fill_opacity=0.45)
    cone.add_updater(lambda m: m.set_fill(opacity=0.30 + 0.24 * (1 + np.sin(clock.get_value() * 4)) / 2))
    halo.add_updater(lambda m: m.set_fill(opacity=0.10 + 0.36 * (1 + np.sin(clock.get_value() * 4)) / 2))
    return VGroup(wire, halo, cone, tip, cue)


def transition(clock, start, stop, phase):
    arrow = Arrow(start, stop, buff=0, color=GOLD, stroke_width=4, tip_length=0.15)
    marker = Triangle(color=GOLD, fill_opacity=1, stroke_width=0).scale(0.105)
    dx, dy, _ = stop - start
    marker.rotate(np.arctan2(dy, dx) - PI / 2)
    marker.add_updater(
        lambda m: m.move_to(interpolate(start, stop, (0.50 * clock.get_value() + phase) % 1))
    )
    marker.update()
    return VGroup(arrow, marker)


class S12Wake(OptogeneticsScene):
    def construct(self):
        clock = self.start()
        cell, _ = neuron()
        animal = mouse()
        center = animal.get_center().copy()
        offset = RIGHT * 1.70 + UP * 0.10
        zoom = 1.20
        animal.shift(offset)
        target = cell.copy().scale(0.13).move_to(at_xy(-2.56, 0.34) + offset)
        source = optical_source()
        dish = culture_dish()
        beam = light_cone(clock, lambda t: 0.35 + 0.27 * np.sin(t * 3) ** 2,
                          top=dish.get_top()[1])
        gate = protein(open_amount=0.18)
        self.add(dish, cell, source, beam, gate)
        self.at("in an animal")
        self.remove(beam)
        self.bring_to_back(animal)
        self.play(FadeIn(animal), Transform(cell, target),
                  FadeOut(source), FadeOut(dish), FadeOut(gate), run_time=1.90)
        self.at("and colleagues delivered")
        study = heading("Adamantidis et al. · 2007", color=GOLD)
        self.play(FadeIn(study), run_time=0.50)
        self.at("through a fiber")
        fibre = optical_fibre(clock).scale(zoom, about_point=center).shift(offset)
        self.play(FadeIn(fibre), VGroup(animal, cell).animate.scale(zoom, about_point=center + offset),
                  run_time=1.0)
        self.at("these were")
        world = VGroup(animal, cell, fibre)
        panel = screen()
        detail, _ = neuron()
        detail = VGroup(detail, protein(open_amount=0.18)).scale(0.66).move_to(at_xy(3.59, -0.16))
        self.play(world.animate.shift(-offset).scale(1 / zoom, about_point=center),
                  FadeIn(panel), FadeIn(detail), run_time=0.68)
        self.at("hypocretin neurons")
        name = heading("Hypocretin neurons", x=1.12, y=2.08, color=PURPLE)
        self.play(FadeIn(name), run_time=0.45)
        self.at("woke more often")
        wake = boxed_label("Waking", size=32, color=GOLD).move_to(at_xy(3.59, -1.77))
        self.play(FadeOut(detail), FadeOut(name), FadeIn(wake), run_time=0.40)
        self.at("slow wave sleep")
        slow = boxed_label("Slow-wave sleep", size=31).move_to(at_xy(3.59, 1.91))
        first = transition(clock, at_xy(3.16, 1.45), at_xy(3.16, -1.34), 0.2)
        self.play(FadeIn(slow), FadeIn(first), run_time=0.41)
        self.at("rem sleep")
        rem = boxed_label("REM sleep", size=31).move_to(at_xy(4.97, 0.57))
        second = transition(clock, at_xy(4.96, 0.12), at_xy(4.03, -1.34), 0.9)
        self.play(FadeIn(rem), FadeIn(second), run_time=0.39)
        self.finish()


class S13End(EndCard):
    LINE = "Light controls chosen cells to test what their activity causes."
