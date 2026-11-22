"""Word-synchronized teaching film for Nerve conduction velocity and EMG.

GREY is anatomy, BLUE is the timing apparatus, YELLOW is electrical activity,
PURPLE is sodium channels, ORANGE is acetylcholine, and GOLD is the prediction
and historical date. TEAL marks myelinated speed examples and Motor unit 1.
GREEN marks Motor unit 2.
"""

from bp_parts import *
from bp_style import EndCard

PURPLE = "#B58CD9"
ORANGE = "#F29E4C"
TISSUE = "#3D4655"
SURFACE = "#262E3B"
MYELIN = "#477B86"
MUSCLE = "#87555F"
DISTANCE = 1.0
QUESTION = "How long at 0.5 m/s over 1.00 m?"
QUESTION_LAYOUT = {"y": 0.35, "left": -0.45, "max_w": 6.5, "size": 34}


def p(x, y):
    return np.array([x, y, 0.0])


def label(text, x, y, color=TEXT, size=32, width=6.4, mono=False):
    return fit_text(text, max_w=width, size=size, min_size=28, color=color,
                    font=MONO if mono else FONT, max_lines=2).move_to(p(x, y))


def line(a, b, color=GREY, width=4):
    return Line(a, b, color=color, stroke_width=width).set_cap_style(CapStyleType.ROUND)


def path(points, color=GREY, width=4, fill=None):
    shape = VMobject(stroke_color=color, stroke_width=width)
    shape.set_points_smoothly([p(*point) for point in points])
    if fill:
        shape.set_fill(fill, 1)
    return shape


def surface():
    return RoundedRectangle(width=7.15, height=5.75, corner_radius=0.26,
                            stroke_color=TISSUE, stroke_width=2, fill_color=SURFACE,
                            fill_opacity=1).move_to(p(2.9, 0.04))


def limb():
    """Fixed side-view anatomy and fixed electrode landmarks."""
    outline = path([
        (-5.22, 3.16), (-3.85, 3.14), (-3.18, 2.35), (-3.28, 1.45),
        (-3.68, 0.45), (-3.18, -0.29), (-3.24, -1.21), (-3.40, -2.03),
        (-3.15, -2.39), (-2.43, -2.52), (-2.05, -2.77), (-2.21, -3.02),
        (-3.79, -3.00), (-4.07, -2.75), (-4.07, -2.27), (-4.35, -1.32),
        (-4.64, -0.37), (-4.51, 0.58), (-5.18, 1.51), (-5.43, 2.47),
        (-5.22, 3.16),
    ], width=3, fill=TISSUE)
    cord = RoundedRectangle(width=0.46, height=1.38, corner_radius=0.22,
                            stroke_color=GREY, stroke_width=3, fill_color=GREY,
                            fill_opacity=0.43).move_to(p(-4.87, 2.45))
    muscle = path([
        (-3.83, 0.20), (-3.36, -0.34), (-3.49, -1.26), (-3.72, -2.13),
        (-3.90, -1.30), (-4.00, -0.40), (-3.83, 0.20),
    ], MUSCLE, 2, MUSCLE)
    striae = VGroup(*[path([(-3.83 + i, -0.23), (-3.77 + i, -0.78),
                            (-3.72 + i * 0.5, -1.52)], "#B67A83", 2)
                      for i in (-0.10, 0, 0.10)])
    bundle = VGroup(muscle, striae)
    nerve = path([(-4.86, 2.63), (-4.82, 1.91), (-4.37, 1.14), (-4.13, 0.46),
                  (-4.13, -0.41), (-3.98, -1.40), (-3.76, -2.32), (-2.73, -2.72)],
                 BLUE, 7)
    motor = path([(-4.86, 2.37), (-4.77, 1.72), (-4.33, 0.94), (-4.19, 0.10),
                  (-3.96, -0.37), (-3.76, -0.68)], TEAL, 4)
    world = VGroup(outline, cord, bundle, nerve, motor)
    world.nerve, world.motor, world.muscle = nerve, motor, bundle
    return world


def electrode(route, fraction):
    return Circle(radius=0.15, color=BLUE, stroke_width=4).move_to(
        route.point_from_proportion(fraction))


def packet(route, phase, color=YELLOW, reverse=False, start=0):
    """A moving envelope denotes local renewal, without depicting transport of matter."""
    head = Dot(radius=0.23, color=color)
    tail = VMobject(stroke_color=color, stroke_width=16, stroke_opacity=0.9)
    halo = VMobject(stroke_color=color, stroke_width=66, stroke_opacity=0.46)
    for stroke in (tail, halo):
        stroke.set_cap_style(CapStyleType.ROUND)
    samples = np.array([route.point_from_proportion(t) for t in np.linspace(0, 1, 101)])
    lengths = np.r_[0, np.cumsum(np.linalg.norm(np.diff(samples, axis=0), axis=1))]
    lengths /= lengths[-1]

    def update(group, dt=0):
        fraction = np.clip(phase(), 0, 1)
        offsets = np.linspace(max(start, fraction - 0.22), fraction + 1e-5, 11)
        if reverse:
            offsets = 1 - offsets
        positions = np.column_stack([np.interp(offsets, lengths, axis) for axis in samples.T])
        halo.set_points_as_corners(positions)
        tail.set_points_as_corners(positions)
        head.move_to(positions[-1])

    group = VGroup(halo, tail, head)
    update(group)
    return group.add_updater(update)


def cycle(scene, route, period=2.5, origin=0, color=YELLOW, reverse=False, start=0):
    return packet(route, lambda: start + (1 - start) * (((scene.time - origin) % period)
                                                       / period), color, reverse, start)


def twitch(scene, muscle, period=2.5, arrival=0.8, pull=None):
    original = muscle.copy()

    def contract(mob, dt=0):
        phase = (scene.time / period - arrival) % 1
        amplitude = pull.get_value() if pull is not None else 1
        strength = amplitude * np.sin(PI * np.clip(phase / 0.28, 0, 1)) ** 2
        mob.become(original.copy().stretch(1 + 0.23 * strength, 0)
                   .stretch(1 - 0.09 * strength, 1))

    muscle.add_updater(contract)


def spike_plot(box=(-0.05, 5.98, -1.8, 1.36), two=True):
    """Schematic spike-time raster. Equal-height ticks encode firing times only."""
    return Plot(box, (0, 1), (0, 2.1 if two else 1), xlabel="Time →", label_size=28,
                color=GREY, stroke=2)


def spike_row(plot, y, events, color, height=0.72):
    return VGroup(line(plot.pt(0, y), plot.pt(1, y), color, 2),
                  *[line(plot.pt(t, y), plot.pt(t, y + height), color, 5)
                    for t in events])


def sweep(scene, plot, period=3):
    cursor = Rectangle(width=0.22, height=plot.y1 - plot.y0, stroke_width=0,
                       fill_color=BLUE, fill_opacity=0.55)

    def update(mob, dt=0):
        x = 0.02 + 0.96 * ((scene.time % period) / period)
        mob.move_to(plot.pt(x, sum(plot.yr) / 2))

    update(cursor)
    return cursor.add_updater(update)


def firing_times(count, phase=0.08):
    return phase + np.arange(count) * (0.86 / count)


class S01Hook(SpokenScene):
    def construct(self):
        world, panel = limb(), surface()
        impulse = cycle(self, world.nerve, 2.4)
        plot = spike_plot((0.02, 6.0, -2.0, -0.15), two=False)
        strip = spike_row(plot, 0.07, firing_times(3), YELLOW)
        marks = VGroup(electrode(world.nerve, 0.31), electrode(world.nerve, 0.59))
        q_nerve = label("?", -1.62, 1.30, YELLOW, 66)
        q_muscle = label("?", -1.54, -0.86, TEAL, 66)
        self.at("how fast")
        self.add(world, impulse, scope_tag())
        self.play(FadeIn(q_nerve), run_time=0.5)
        bob(q_nerve, amp=0.12)
        self.at("how can you read")
        twitch(self, world.muscle, 2.4)
        self.play(FadeIn(q_muscle), run_time=0.5)
        bob(q_muscle, amp=0.12, seed=2)
        self.at("two linked methods")
        self.play(FadeOut(q_nerve), FadeOut(q_muscle), run_time=0.65)
        self.play(FadeIn(marks), run_time=0.45)
        self.at("nerve conduction velocity")
        self.play(FadeIn(panel), FadeIn(label("Nerve conduction velocity", 2.88, 1.9, BLUE, 37)),
                  run_time=0.55)
        self.at("while electromyography")
        self.play(Create(plot.axes), FadeIn(plot.xlabel), run_time=0.48)
        self.play(FadeIn(label("Electromyography (EMG)", 2.88, 0.64, TEAL, 36)),
                  run_time=0.55)
        self.at("records muscle spikes")
        self.play(Create(strip), run_time=0.65)
        self.add(sweep(self, plot))
        self.finish()


class S02Title(TitleCard):
    LESSON = "Nerve conduction velocity and EMG"
    TITLE = "Timing Nerve Impulses and Muscle Spikes"

    def construct(self):
        world = limb()
        world.fade(0.67)
        signal = cycle(self, world.nerve, 2)
        self.add(world, signal)
        title = fit_text(self.TITLE, max_w=7.0, size=52, min_size=43,
                         max_lines=3, font=TITLE_FONT).move_to(p(2.84, 0.38))
        lesson = label(self.LESSON, 2.84, -1.60, BLUE, 31, width=6.85)
        rule = line(p(1.72, -0.97), p(3.96, -0.97), GOLD, 4)
        self.play(FadeIn(title), GrowFromCenter(rule), FadeIn(lesson), run_time=0.4)
        self.wait(1.6)


def timing_row(y, travel, name):
    start = 0.10
    travel_bar = VGroup(line(p(start, y), p(start + travel, y), BLUE, 19),
                        Dot(p(start, y), radius=0.075, color=TEXT))
    delay_start = start + travel + 0.13
    delays = VGroup(*[line(p(delay_start + i * 0.82, y),
                           p(delay_start + i * 0.82 + 0.60, y), ORANGE, 19)
                      for i in range(3)])
    return travel_bar, delays, label(name, 1.12, y + 0.5, BLUE, 29, width=2.6)


class S03TwoPoint(SpokenScene):
    def construct(self):
        world, panel = limb(), surface()
        signal = cycle(self, world.motor, 2.5)
        first, end1, near_text = timing_row(0.25, 2.64, "Point 1 · near")
        second, end2, far_text = timing_row(-1.17, 3.74, "Point 2 · far")
        near, far = (electrode(world.motor, fraction) for fraction in (0.64, 0.27))
        self.at("an action potential")
        self.add(world, signal, panel, scope_tag())
        intro = label("Action potential", 2.9, 1.58, YELLOW, 43)
        self.play(FadeIn(intro), run_time=0.55)
        self.at("response time adds")
        eq = label("time ≈ L/v", 2.9, 2.14, BLUE, 38, mono=True)
        self.play(swap(intro, eq), run_time=0.65)
        self.at("length divided by")
        self.play(Create(first), run_time=0.80)
        self.at("plus delays")
        full = label("time ≈ L/v + end delays", 2.9, 2.14, TEXT, 37, mono=True)
        key = label("Receptor · Junction · Muscle", 3.03, 1.02, ORANGE, 29)
        self.play(swap(eq, full), run_time=0.50)
        self.play(LaggedStart(*[GrowFromCenter(seg) for seg in end1], lag_ratio=0.30),
                  run_time=0.85)
        self.play(FadeIn(key), run_time=0.45)
        self.at("from one point")
        self.remove(signal)
        self.play(FadeIn(near), run_time=0.40)
        near_signal = cycle(self, world.motor, 1.75, origin=self.time, start=0.64)
        self.add(near_signal)
        self.play(Indicate(end1, color=ORANGE, scale_factor=1.05), run_time=1.0)
        self.at("stimulate at two points")
        self.play(FadeOut(key), FadeIn(near_text), FadeIn(far), run_time=0.40)
        self.remove(near_signal)
        self.add(cycle(self, world.motor, 2.3, origin=self.time, start=0.27))
        self.play(Create(second), FadeIn(end2), FadeIn(far_text), run_time=0.75)
        self.at("subtract arrival times")
        self.play(VGroup(first, end1).animate.shift(RIGHT * 1.10), run_time=0.70)
        self.at("shared end delays")
        difference = line(p(0.10, -2.15), p(1.20, -2.15), YELLOW, 10)
        self.play(FadeOut(end1), FadeOut(end2),
                  swap(full, label("Shared delays cancel", 2.9, 2.14, ORANGE, 34)),
                  run_time=0.57)
        self.play(Create(difference), run_time=0.36)
        self.play(FadeIn(label("Time between points", 3.38, -2.15, YELLOW, 30)),
                  run_time=0.33)
        self.finish()


def axons():
    thin = line(p(-5.76, 1.13), p(5.78, 1.13), BLUE, 9)
    thick = line(p(-5.76, -1.25), p(5.78, -1.25), BLUE, 34)
    centers = np.linspace(-4.85, 4.85, 6)
    sheaths = VGroup()
    for x in centers:
        wrap = RoundedRectangle(width=1.68, height=1.17, corner_radius=0.38,
                                stroke_color=BLUE, stroke_width=3, fill_color=MYELIN,
                                fill_opacity=1).move_to(p(x, -1.25))
        layers = VGroup(*[line(p(x - 0.51, -1.25 + y), p(x + 0.51, -1.25 + y),
                               BLUE, 2).set_stroke(opacity=0.65)
                          for y in (-0.35, -0.22, 0.22, 0.35)])
        sheaths.add(VGroup(wrap, layers))
    nodes = (centers[:-1] + centers[1:]) / 2
    channels = VGroup(*[VGroup(*[Dot(p(x + dx, -1.25 + dy), radius=0.041, color=PURPLE)
                                 for dx in (-0.055, 0.055) for dy in (-0.16, 0.16)])
                        for x in nodes])
    return thin, thick, sheaths, nodes, channels


class S04Myelin(SpokenScene):
    def construct(self):
        world, panel = limb(), surface()
        thin, thick, sheaths, nodes, channels = axons()
        markers = VGroup(*[electrode(world.motor, f) for f in (0.27, 0.64)])
        self.at("dividing distance")
        signal = cycle(self, world.motor)
        self.add(world, panel, markers, signal, scope_tag())
        numerator = label("distance", 3.75, 1.58, BLUE, 41, mono=True)
        velocity = label("v =", 1.18, 0.98, BLUE, 42, mono=True)
        between = world.motor.copy()
        between.pointwise_become_partial(world.motor, 0.27, 0.64)
        between.set_stroke(YELLOW, width=10)
        self.play(Create(between), FadeIn(numerator), FadeIn(velocity), run_time=0.65)
        self.at("by time difference")
        divider = line(p(2.32, 0.96), p(5.17, 0.96), BLUE, 4)
        denominator = label("time difference", 3.75, 0.34, BLUE, 33, mono=True)
        self.play(Create(divider), FadeIn(denominator), run_time=0.60)
        self.at("gives conduction velocity")
        name = boxed_label("Conduction velocity", BLUE, size=36, pad=0.26,
                           fill_opacity=0.32).move_to(p(2.9, -1.27))
        self.play(FadeIn(name), run_time=0.62)
        self.at("the impulse's speed")
        self.play(Indicate(markers, color=BLUE, scale_factor=1.10), run_time=0.70)
        self.at("speed rises with")
        self.play(FadeOut(velocity), FadeOut(numerator), FadeOut(divider),
                  FadeOut(denominator), FadeOut(name), run_time=0.32)
        self.play(FadeOut(panel), FadeOut(world), FadeOut(markers), FadeOut(between),
                  FadeOut(signal), Create(thin), Create(thick), run_time=0.61)
        self.add(cycle(self, thin, 7))
        self.at("and myelin")
        self.play(LaggedStart(*[GrowFromCenter(s) for s in sheaths], lag_ratio=0.1),
                  run_time=1.05)
        self.play(FadeIn(label("Thin, bare axon", -3.83, 1.91, BLUE)),
                  FadeIn(label("Myelin wraps a thick axon", -2.90, -2.46, BLUE)),
                  run_time=0.48)
        self.at("short bare gaps")
        node_marker = line(p(nodes[2], -0.93), p(nodes[2], -0.48), PURPLE, 3)
        node_name = label("Nodes of Ranvier", 0, -0.13, PURPLE)
        self.play(Create(node_marker), FadeIn(node_name), run_time=0.58)
        self.at("pack sodium channels")
        self.play(FadeIn(channels), run_time=0.54)
        channel_name = label("Sodium channels", 3.72, -2.46, PURPLE)
        self.play(FadeIn(channel_name), run_time=0.52)
        self.at("the impulse is renewed")
        start = self.time
        flash = Dot(p(nodes[0], -1.25), radius=0.17, color=YELLOW)

        def jump(mob, dt=0):
            phase = ((self.time - start) / 0.32) % len(nodes)
            mob.move_to(p(nodes[int(phase)], -1.25))
            mob.set_opacity(1 - 0.62 * (phase % 1))

        self.add(flash.add_updater(jump))
        self.at("salutatory conduction")
        self.play(swap(channel_name, label("Saltatory conduction", 3.72, -2.46, YELLOW)),
                  run_time=0.61)
        self.finish()


def distance_bracket():
    return VGroup(line(p(-5.92, -2.72), p(-5.92, 2.63), GREY, 3),
                  *[line(p(-6.07, y), p(-5.77, y), GREY, 3) for y in (-2.72, 2.63)],
                  label("1.00 m", -6.24, -0.04, TEXT, 28, width=2).rotate(PI / 2))


def prediction():
    world = limb()
    start = Dot(world.nerve.get_end(), radius=0.14, color=YELLOW)
    formula = label("t = L / v", 2.87, 2.04, BLUE, 43, mono=True)
    speed = label("Bare C fibre · 0.5 m/s", 2.87, -0.74, YELLOW, 32)
    return world, surface(), distance_bracket(), start, formula, speed, scope_tag()


class S05PredictQ(SpokenScene):
    def construct(self):
        world, panel, bracket, start, formula, speed, scope = prediction()
        self.at("test the math")
        self.add(world, scope)
        signal = cycle(self, world.nerve, 3.1, reverse=True)
        self.add(signal)
        self.at("path from foot")
        self.play(Create(bracket[:3]), run_time=0.77)
        self.play(FadeIn(bracket[3]), run_time=0.35)
        self.at("travel time equals")
        self.play(FadeIn(panel), FadeIn(formula), run_time=0.60)
        self.at("an unmyelinated")
        self.play(FadeIn(start), run_time=0.45)
        self.at("conduct at")
        self.play(FadeIn(speed), run_time=0.55)
        self.at("how long does")
        self.remove(signal)
        self.play(FadeIn(question_card(QUESTION, **QUESTION_LAYOUT)), run_time=0.65)
        self.finish()


class S06PredictPause(PredictPause):
    QUESTION = QUESTION
    CARD = QUESTION_LAYOUT
    SECONDS = 4.5
    RING_AT = (5.83, -2.27, 0)

    def backdrop(self):
        return VGroup(*prediction())

    def construct(self):
        self.add(self.backdrop(), question_card(self.QUESTION, **self.CARD))
        ring, run = countdown(self.SECONDS, center=self.RING_AT, radius=0.30)
        start = p(0.12, -2.31)
        track = RoundedRectangle(width=4.90, height=0.38, corner_radius=0.10,
                                 stroke_width=0, fill_color="#778191", fill_opacity=1)
        track.move_to(start + RIGHT * track.width / 2)
        progress = Rectangle(width=0.001, height=0.24, stroke_width=0,
                             fill_color=GOLD, fill_opacity=1)
        progress.move_to(start + RIGHT * 0.08)
        self.add(track, progress, ring)
        self.play(run, progress.animate.stretch_to_fit_width(4.74, about_edge=LEFT),
                  run_time=self.SECONDS, rate_func=linear)


class S07PredictReveal(SpokenScene):
    def construct(self):
        world, panel, bracket, start, formula, _, scope = prediction()
        self.add(world, panel, bracket, start, formula, scope)
        self.at("one meter divided")
        numerator = label("1.00 m ÷", 2.87, 0.98, TEXT, 35, mono=True)
        self.play(FadeIn(numerator), run_time=0.4)
        self.at("0 .5 meters")
        quotient = label("1.00 m ÷ 0.5 m/s", 2.87, 0.98, TEXT, 35, mono=True)
        self.play(swap(numerator, quotient), run_time=0.40)
        elapsed = ValueTracker(0)
        launch = lambda velocity, color: packet(
            world.nerve, lambda: velocity * elapsed.get_value() / DISTANCE,
            color, reverse=True)
        flight = launch(0.5, YELLOW)
        self.remove(start)
        self.add(flight)
        self.play(elapsed.animate.set_value(DISTANCE / 0.5), run_time=DISTANCE / 0.5,
                  rate_func=linear)
        self.at("two seconds")
        self.remove(flight)
        flight = cycle(self, world.nerve, DISTANCE / 0.5, origin=self.time, reverse=True)
        self.add(flight)
        answer = label("= 2 s", 2.87, -0.04, YELLOW, 45, mono=True)
        self.play(FadeIn(answer), run_time=0.45)
        self.at("at two meters")
        self.remove(flight)
        elapsed.set_value(0)
        faster = label("1.00 m ÷ 2 m/s", 2.87, 0.98, TEXT, 35, mono=True)
        self.play(swap(quotient, faster), FadeOut(answer), run_time=0.52)
        flight = launch(2, YELLOW)
        self.add(flight)
        self.play(elapsed.animate.set_value(DISTANCE / 2), run_time=DISTANCE / 2,
                  rate_func=linear)
        self.at("0 .5 seconds")
        self.remove(flight)
        flight = cycle(self, world.nerve, DISTANCE / 2, origin=self.time, reverse=True)
        self.add(flight)
        half = label("= 0.5 s", 2.87, -0.04, YELLOW, 45, mono=True)
        self.play(FadeIn(half), run_time=0.50)
        self.at("thinly myelinated")
        self.remove(flight)
        elapsed.set_value(0)
        delta = label("Thinly myelinated Aδ", 2.87, 0.98, TEAL, 33)
        self.play(swap(faster, delta), FadeOut(half), run_time=0.55)
        self.at("roughly 5 to 30")
        range_label = label("About 5–30 m/s", 2.87, -0.04, TEAL, 37)
        tracks, racers = VGroup(), VGroup()
        for velocity, y in ((5, -0.88), (30, -1.55)):
            track = line(p(0.48, y), p(3.95, y), GREY, 4)
            track_label = label(f"{velocity} m/s", 5.11, y, TEAL, 29, width=1.8)
            tracks.add(track, track_label)
            racer = Dot(track.get_start(), radius=0.15, color=TEAL)
            racer.add_updater(lambda dot, dt, route=track, v=velocity: dot.move_to(
                route.point_from_proportion(min(v * elapsed.get_value() / DISTANCE, 1))))
            racers.add(racer)
        slow_motion = label("Slow motion", 2.87, -2.24, TEXT, 28)
        self.play(FadeIn(range_label), FadeIn(tracks), FadeIn(slow_motion), run_time=0.40)
        slow_flight = launch(5, TEAL)
        self.add(racers, slow_flight)
        transit = DISTANCE / 5
        self.play(elapsed.animate.set_value(transit), run_time=15 * transit, rate_func=linear)
        self.at("large myelinated axons")
        self.remove(racers, slow_flight)
        self.play(swap(delta, label("Large myelinated axon", 2.87, 0.98, TEAL, 33)),
                  FadeOut(range_label), FadeOut(tracks), FadeOut(slow_motion), run_time=0.55)
        self.at("about 100 meters")
        last = label("1.00 m ÷ 100 m/s", 2.87, -0.04, TEXT, 35, mono=True)
        self.play(FadeIn(last), run_time=0.48)
        elapsed.set_value(0)
        fastest = launch(100, TEAL)
        self.add(fastest)
        self.play(elapsed.animate.set_value(DISTANCE / 100), run_time=1 / 15,
                  rate_func=linear)
        self.at("take 100th")
        self.play(FadeIn(label("≈ 0.01 s", 2.87, -1.10, YELLOW, 45, mono=True)),
                  run_time=0.55)
        self.finish()


def motor_unit(y, color):
    """One alpha motor neuron fans out to two visibly isolated fibres."""
    soma = Circle(radius=0.27, color=color, stroke_width=4,
                  fill_color=color, fill_opacity=0.35).move_to(p(0.04, y))
    axon = path([(0.30, y), (1.22, y), (2.10, y)], color, 6)
    branches, fibres, tubules = VGroup(), VGroup(), VGroup()
    for dy in (0.39, -0.39):
        yy = y + dy
        branches.add(path([(2.08, y), (2.52, yy), (3.10, yy)], color, 5))
        band = RoundedRectangle(width=2.89, height=0.50, corner_radius=0.22,
                                stroke_color=color, stroke_width=3,
                                fill_color=color, fill_opacity=0.24).move_to(p(4.77, yy))
        membrane = line(p(3.44, yy), p(6.03, yy), color, 3)
        fibres.add(VGroup(band, membrane))
        tubules.add(VGroup(*[line(p(x, yy + 0.19), p(x, yy - 0.11), color, 3)
                            for x in (4.22, 4.81, 5.40)]))
    unit = VGroup(soma, axon, branches, fibres)
    unit.axon, unit.branches, unit.fibres, unit.tubules = axon, branches, fibres, tubules
    unit.color_code = color
    return unit


def synaptic_release(y):
    return VGroup(*[Dot(p(3.10 + 0.056 * i, y + dy + 0.05 * (-1) ** i),
                         radius=0.032, color=ORANGE)
                    for dy in (-0.39, 0.39) for i in range(1, 5)])


def unit_activity(scene, unit, period, origin=0):
    routes = [unit.axon, *unit.branches, *[f[1] for f in unit.fibres]]
    fractions = [(0, 0.35), (0.34, 0.60), (0.34, 0.60), (0.60, 1), (0.60, 1)]
    dots = VGroup(*[Dot(route.get_start(), radius=0.102, color=YELLOW) for route in routes])

    def update(group, dt=0):
        phase = ((scene.time - origin) % period) / period
        for dot, route, (begin, end) in zip(group, routes, fractions):
            progress = np.clip((phase - begin) / (end - begin), 0, 1)
            dot.move_to(route.point_from_proportion(float(progress)))
            dot.set_opacity(float(begin <= phase < end))
        for fibre, branch in zip(unit.fibres, unit.tubules):
            for tubule in branch:
                fraction = (tubule.get_x() - fibre[1].get_start()[0]) / fibre[1].get_length()
                active = 0 < phase - (0.60 + 0.40 * fraction) < 0.10
                tubule.set_color(YELLOW if active else unit.color_code)

    return dots.add_updater(update)


class S08Emg(SpokenScene):
    def construct(self):
        world, panel = limb(), surface()
        a = motor_unit(0.55, TEAL)
        b = motor_unit(-1.35, GREEN)
        signal = cycle(self, world.motor, 2.1)
        self.at("now follow")
        self.add(world, panel, signal, scope_tag())
        self.play(FadeIn(a), run_time=0.85)
        self.at("skeletal muscle")
        muscle_label = label("Skeletal muscle", 4.77, 1.82, TEAL)
        self.play(FadeIn(muscle_label), run_time=0.50)
        self.at("the neuromuscular junction")
        junction = label("Neuromuscular junction", 2.8, 2.20, TEAL, 31)
        self.play(swap(muscle_label, junction), run_time=0.55)
        self.at("acetylcholine starts")
        release = synaptic_release(0.55)
        ach = label("Acetylcholine", 3.03, -0.42, ORANGE, 29)
        self.play(FadeIn(release), run_time=0.38)
        self.play(FadeIn(ach), FadeIn(a.tubules), run_time=0.48)
        a_activity = unit_activity(self, a, 2.24, self.time - 1.3)
        self.add(a_activity)
        self.at("one alpha motor neuron")
        self.play(FadeOut(release), FadeOut(ach), run_time=0.38)
        neuron = label("Alpha motor neuron", 1.25, 1.41, TEAL, 29, width=3.5)
        self.play(swap(junction, neuron), run_time=0.56)
        self.at("form a motor unit")
        unit_label = label("Motor unit 1", 3.02, 2.20, TEAL, 35)
        self.play(FadeIn(unit_label), run_time=0.50)
        self.at("fibers are not electrically")
        self.play(FadeIn(b), FadeIn(b.tubules), run_time=0.72)
        b_activity = unit_activity(self, b, 2.9, self.time - 0.3)
        self.add(b_activity)
        self.at("when its own motor neuron")
        second_unit = label("Motor unit 2", 3.02, -2.38, GREEN, 33)
        self.play(FadeOut(neuron), FadeIn(second_unit), run_time=0.55)
        self.at("emg records")
        self.remove(a_activity, b_activity)
        self.play(FadeOut(a), FadeOut(a.tubules), FadeOut(b), FadeOut(b.tubules),
                  FadeOut(unit_label), FadeOut(second_unit), run_time=0.46)
        plot = spike_plot()
        self.play(FadeIn(plot), FadeIn(label("EMG · motor-unit spikes", 2.9, 2.15, TEXT, 34)),
                  run_time=0.44)
        self.play(Create(spike_row(plot, 1.14, firing_times(4), TEAL)),
                  Create(spike_row(plot, 0.12, firing_times(3, 0.16), GREEN)),
                  run_time=1.03)
        self.add(sweep(self, plot))
        self.finish()


def emg_response(scene):
    """Rebuild the same recording screen for the guardrails and final recap."""
    world = limb()
    plot = spike_plot()
    title = label("EMG · motor-unit spikes", 2.9, 2.15, TEXT, 34)
    return world, surface(), plot, title, sweep(scene, plot)


def speed_paths():
    touch = path([(0.18, 0.34), (1.85, 0.47), (3.34, 1.25), (4.67, 1.28)], BLUE, 9)
    pain = path([(0.18, -0.34), (1.85, -0.47), (3.34, -1.19), (4.67, -1.22)], BLUE, 9)
    pads = VGroup(VGroup(*[Arc(radius=r, start_angle=0.06, angle=PI - 0.12,
                              color=TEAL, stroke_width=3).move_arc_center_to(p(5.52, 1.25))
                          for r in (0.19, 0.32, 0.45)]),
                  Polygon(p(5.57, -0.70), p(5.25, -1.22), p(5.53, -1.17),
                          p(5.38, -1.68), p(5.87, -1.07), p(5.55, -1.09),
                          color=RED, fill_color=RED, fill_opacity=0.7))
    return touch, pain, pads


class S09Limits(SpokenScene):
    def construct(self):
        world, panel, plot, title, cursor = emg_response(self)
        first = spike_row(plot, 1.14, firing_times(4), TEAL)
        prior = spike_row(plot, 0.12, firing_times(3, 0.16), GREEN)
        dense = spike_row(plot, 1.14, firing_times(8), TEAL)
        recruited = spike_row(plot, 0.12, firing_times(6, 0.13), GREEN)
        self.at("three guardrails")
        self.add(world, panel, plot, title, first, prior, cursor, scope_tag())
        self.add(cycle(self, world.motor, 2.8))
        pull = ValueTracker(0.45)
        self.at("impulses are all or none")
        twitch(self, world.muscle, 2.8, pull=pull)
        self.play(FadeOut(prior), run_time=0.48)
        self.at("stronger force")
        self.play(swap(first, dense, run_time=0.62), pull.animate.set_value(0.8))
        self.at("and motor units")
        self.play(Create(recruited), pull.animate.set_value(1.45), run_time=0.75)
        self.at("not taller spikes")
        equal = label("Same spike height", 2.89, 2.15, YELLOW, 34)
        self.play(swap(title, equal), run_time=0.53)

        self.at("a teaching model")
        self.remove(cursor)
        self.play(FadeOut(plot), FadeOut(equal), FadeOut(dense), FadeOut(recruited),
                  run_time=0.46)
        cord = Ellipse(width=1.55, height=1.2, color=GREY, stroke_width=4,
                       fill_color=TISSUE, fill_opacity=1).move_to(p(3.0, 1.37))
        afferent = path([(0.33, -0.66), (1.05, -0.39), (1.62, 0.93),
                         (2.27, 1.32), (2.78, 1.38)], BLUE, 7)
        efferent = path([(3.22, 1.38), (3.80, 1.35), (4.65, 0.79),
                         (4.50, -0.22), (5.67, -0.68)], TEAL, 7)
        junction = Dot(p(3, 1.38), radius=0.10, color=GOLD)
        reflex = VGroup(cord, afferent, efferent, junction)
        self.play(FadeIn(reflex), run_time=0.64)
        reflex_route = path([(0.33, -0.66), (1.05, -0.39), (1.62, 0.93),
                             (2.27, 1.32), (2.78, 1.38), (3.0, 1.38),
                             (3.22, 1.38), (3.80, 1.35), (4.65, 0.79),
                             (4.50, -0.22), (5.67, -0.68)])
        relay = cycle(self, reflex_route, 2.9)
        self.add(relay)
        reflex_name = label("Knee-jerk reflex", 2.9, 2.39, TEXT, 32)
        ms = label("~1 ms per cord synapse", 2.9, -1.38, GOLD, 33)
        self.at("millisecond per")
        self.play(FadeIn(reflex_name), FadeIn(ms), run_time=0.49)
        self.at("real synapses vary")
        varies = label("~1 ms · actual delays vary", 2.9, -1.38, GOLD, 32)
        self.play(swap(ms, varies), run_time=0.52)
        limit = label("Suggests a count · never proves", 2.9, -2.19, TEXT, 30)
        self.at("delay cannot prove")
        self.play(FadeIn(limit), run_time=0.52)

        self.at("some c fibers carry")
        self.remove(relay)
        self.play(FadeOut(reflex), FadeOut(reflex_name), FadeOut(varies), FadeOut(limit),
                  run_time=0.41)
        touch, pain, pads = speed_paths()
        self.play(Create(touch), Create(pain), FadeIn(pads), run_time=0.64)
        self.add(cycle(self, touch, 3.2), cycle(self, pain, 3.46, origin=-0.9))
        self.play(FadeIn(label("Touch", 5.46, 1.99, TEAL, 30, width=1.5)),
                  FadeIn(label("Pain", 5.46, -1.99, RED, 30, width=1.5)), run_time=0.45)
        self.at("speed alone cannot")
        self.play(FadeIn(label("Speed alone ≠ sensation",
                               2.90, 2.40, TEXT, 32)), run_time=0.53)
        self.finish()


def frog_preparation():
    muscle = path([(4.95, -1.71), (4.32, -1.32), (4.10, -0.68), (4.43, -0.55),
                   (5.13, -0.79), (5.67, -1.25), (5.77, -1.58), (4.95, -1.71)],
                  MUSCLE, 3, MUSCLE)
    nerve = path([(0.05, 0.10), (1.20, 0.27), (2.34, 0.10), (3.35, -0.23),
                  (4.42, -0.91)], BLUE, 8)
    return muscle, nerve, VGroup(*[electrode(nerve, f) for f in (0.24, 0.65)])


class S10Unlocked(SpokenScene):
    def construct(self):
        world, panel = limb(), surface()
        muscle, nerve, markers = frog_preparation()
        self.at("in 1850")
        self.add(world, panel, scope_tag(), cycle(self, world.nerve, 3.2))
        historic = label("Helmholtz · 1850", 2.89, 2.12, GOLD, 38)
        self.play(FadeIn(muscle), Create(nerve), run_time=0.65)
        self.at("helmholtz timed")
        self.play(FadeIn(historic), run_time=0.47)
        frog = label("Frog nerve", 2.90, 1.01, BLUE, 30)
        self.play(FadeIn(frog), run_time=0.5)
        self.at("at two points")
        self.play(LaggedStart(*[FadeIn(m) for m in markers], lag_ratio=0.35), run_time=0.55)
        propagating = cycle(self, nerve, 2.05, origin=self.time)
        self.add(propagating)
        self.at("a few tens")
        speed = label("A few tens of m/s", 2.88, -2.23, YELLOW, 33)
        self.play(FadeIn(speed), run_time=0.56)
        self.at("later timing showed")
        self.remove(propagating)
        self.play(FadeOut(muscle), FadeOut(nerve), FadeOut(markers), FadeOut(speed),
                  FadeOut(historic), FadeOut(frog), run_time=0.49)
        bare = line(p(0.03, 0.95), p(5.92, 0.95), BLUE, 9)
        wrapped = line(p(0.03, -1.45), p(5.92, -1.45), BLUE, 18)
        wraps = VGroup(*[RoundedRectangle(width=0.83, height=0.52, corner_radius=0.18,
                                          stroke_color=BLUE, stroke_width=2,
                                          fill_color=MYELIN, fill_opacity=1)
                         .move_to(p(x, -1.45)) for x in np.linspace(0.59, 5.35, 6)])
        self.play(Create(bare), run_time=0.60)
        self.add(cycle(self, bare, 6.1))
        self.at("thin bare fibers")
        self.play(FadeIn(label("Thin bare fibres", 2.88, 1.91, BLUE, 32)), run_time=0.48)
        self.at("about one meter")
        self.play(FadeIn(label("About 1 m/s or less", 2.88, 0.18, YELLOW, 33)), run_time=0.52)
        self.at("the largest myelinated")
        self.play(Create(wrapped), FadeIn(wraps), run_time=0.68)
        self.add(cycle(self, wrapped, 0.78))
        self.play(FadeIn(label("Largest myelinated fibres", 2.88, -0.80, TEAL, 32)),
                  run_time=0.48)
        self.at("about 100 or")
        self.play(FadeIn(label("About 100 m/s or more", 2.88, -2.24, YELLOW, 33)),
                  run_time=0.54)
        self.finish()


class S11Close(SpokenScene):
    def construct(self):
        world, panel, plot, title, cursor = emg_response(self)
        first = spike_row(plot, 1.14, firing_times(3), TEAL)
        second = spike_row(plot, 0.12, firing_times(2, 0.16), GREEN)
        faster = spike_row(plot, 1.14, firing_times(8), TEAL)
        recruited = spike_row(plot, 0.12, firing_times(6, 0.13), GREEN)
        self.at("on an emg trace")
        self.add(world, panel, plot, title, first, cursor, scope_tag())
        pull = ValueTracker(0.45)
        twitch(self, world.muscle, 2.4, pull=pull)
        self.at("graded force")
        activity = cycle(self, world.motor, 2.4)
        self.add(activity)
        self.at("more motor units")
        self.play(Create(second), pull.animate.set_value(0.8), run_time=0.62)
        self.at("firing more often")
        self.play(swap(first, faster), swap(second, recruited),
                  pull.animate.set_value(1.45), run_time=0.64)
        self.at("time impulses across distance")
        marks = VGroup(*[electrode(world.motor, f) for f in (0.27, 0.64)])
        self.play(FadeIn(marks), run_time=0.50)
        final = label("Time impulses · read spikes", 2.90, 2.14, BLUE, 34)
        self.at("listen to muscle spikes")
        self.play(swap(title, final), run_time=0.52)
        self.finish()


class S12End(EndCard):
    LINE = "Timing impulses gives nerve speed; muscle spikes track active motor units."
