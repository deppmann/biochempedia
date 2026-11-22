"""Measuring What a Mind Detects, timed to the supplied Kokoro word alignment.

BLUE: stimulus and apparatus. GREY: subject and bench structure. YELLOW:
measured response. GREEN: fixed rules and safeguards. RED: noise and bias.
ORANGE: autistic study cohort. GOLD: questions, dates and takeaways.
"""

from bp_parts import *
from bp_style import EndCard

ORANGE = "#F29E4C"
PANEL = "#2A3649"
QUESTION = "Higher threshold: better or poorer detection?"
QUESTION_STYLE = dict(y=3.18, size=36, max_w=11.6)
TYPICAL, AUTISTIC = 6.59, 9.13
DIFFERENCE = round(AUTISTIC - TYPICAL, 2)


def point(x, y):
    return np.array([x, y, 0.0])


def label(text, x, y, color=TEXT, size=30):
    return T(text, size, color).move_to(point(x, y))


def plate(x, y, width, height):
    return RoundedRectangle(
        width=width, height=height, corner_radius=0.22,
        stroke_color="#566982", stroke_width=2,
        fill_color=PANEL, fill_opacity=1,
    ).move_to(point(x, y))


def arrow(start, end, color=YELLOW, double=False):
    cls = DoubleArrow if double else Arrow
    return cls(start, end, buff=0, stroke_width=4, color=color, tip_length=0.15)


def bench(kind="three", tag=True):
    """The instrument rail and the interchangeable work surfaces above it."""
    zones = {
        "three": [(-4.38, 3.85), (0, 4.45), (4.38, 3.85)],
        "two": [(-4.38, 3.85), (1.94, 8.72)],
        "left": [(-1.94, 8.72), (4.38, 3.85)],
        "wide": [(0, 12.65)],
    }
    surfaces = VGroup(*[plate(x, 0.30, w, 4.30) for x, w in zones[kind]])
    rail = Line(point(-6.30, -2.27), point(6.30, -2.27), color=GREY, stroke_width=6)
    jacks = VGroup(*[Dot(point(x, -2.27), 0.11, color=BLUE) for x in (-4.38, 0, 4.38)])
    result = VGroup(surfaces, rail, jacks)
    if tag:
        result.add(scope_tag(size=28, color=TEXT))
    return result


def trace(plot, function, color, phase, width=5):
    return always_redraw(lambda: plot.curve(
        lambda x: function(x, phase.get_value()), color=color, width=width, n=85
    ))


def running_clock(scene, start=0):
    tracker = ValueTracker(start)
    tracker.add_updater(lambda obj, dt: obj.increment_value(dt))
    scene.add(tracker)
    return tracker


def noise(x, t):
    return (0.54 * np.sin(2.8*x + 3.1*t) + 0.28 * np.sin(6.4*x - 4.3*t + 1.5)
            + 0.16 * np.sin(11.5*x + 5.8*t + 0.8))


def silhouette(x, y, infant=False, facing=1):
    """A pose made from a head, nose, and shoulders at the same bench station."""
    r = 0.46 if infant else 0.55
    head = Circle(radius=r, color=GREY, stroke_width=3, fill_color=GREY, fill_opacity=0.85)
    head.move_to(point(x, y + (0.30 if infant else 0.49)))
    body = RoundedRectangle(
        width=1.05 if infant else 1.38, height=0.95 if infant else 1.22,
        corner_radius=0.37, stroke_color=GREY, stroke_width=3,
        fill_color=GREY, fill_opacity=0.6,
    ).move_to(point(x - 0.10*facing, y - 0.58))
    eye_y = head.get_y() + 0.08
    nose = Polygon(point(x + facing*(r - 0.06), eye_y + 0.1),
                   point(x + facing*(r + 0.16), eye_y - 0.08),
                   point(x + facing*(r - 0.06), eye_y - 0.11),
                   stroke_width=0, fill_color=GREY, fill_opacity=1)
    eye = Dot(point(x + facing*0.24, eye_y), 0.063, color=BG)
    return VGroup(body, head, nose, eye)


def stimulus_dial(level, center=None, radius=1.43):
    """The bench uses a relative level without an invented force or intensity unit."""
    if center is None:
        center = point(-4.38, 0.20)
    gauge = dial(level, center, radius=radius, color=BLUE, size=28)
    gauge.remove(gauge[3])
    return gauge


def calibrated_fill(level):
    center = point(-4.38, 0.20)
    return always_redraw(lambda: Sector(
        radius=1.37, start_angle=PI, angle=-PI*max(0.001, level.get_value()),
        stroke_width=0, fill_color=BLUE, fill_opacity=0.89,
    ).move_arc_center_to(center))


def bench_instruments(level, phase):
    gauge = stimulus_dial(level)
    plot = Plot(box=(-1.93, 1.93, -0.96, 1.47), xr=(0, 6), yr=(-1.2, 1.2))
    baseline = Line(plot.pt(0, 0), plot.pt(6, 0), color=GREY, stroke_width=2)
    wave = trace(plot, noise, RED, phase, width=7)
    person = silhouette(3.72, -0.04)
    frame = plate(5.36, 0.40, 1.04, 1.04).set_stroke(GREEN, 3)
    return gauge, VGroup(baseline, wave), person, frame


def calibration():
    center = point(-4.38, 0.20)
    return VGroup(*[
        Line(center + 1.49*point(np.cos(a), np.sin(a)),
             center + 1.63*point(np.cos(a), np.sin(a)), color=TEXT, stroke_width=2)
        for a in np.linspace(0.16, PI - 0.16, 9)
    ])


class S01Hook(SpokenScene):
    def construct(self):
        clock = running_clock(self)
        level = ValueTracker(0.38)
        level.add_updater(lambda m: m.set_value(0.38 + 0.10*np.sin(2*clock.get_value())))
        self.add(level)
        gauge, wave, subject, choice = bench_instruments(level, clock)
        question = label("?", 5.36, 0.40, GOLD, 58)
        self.add(bench(), gauge, wave, subject, choice, question)
        self.at("baby cannot speak", lead=0.65)
        self.play(Transform(subject, silhouette(3.72, -0.04, infant=True)), run_time=0.55)
        self.at("a person's report", lead=0.55)
        bar = Line(point(4.94, 0.4), point(5.78, 0.4), color=GREY, stroke_width=3)
        cursor = Line(point(5.10, 0.19), point(5.10, 0.61), color=RED, stroke_width=6)
        self.play(FadeOut(question), Transform(subject, silhouette(3.72, -0.04)), run_time=0.45)
        self.add(bar, cursor)
        self.play(cursor.animate.shift(RIGHT * 0.57), run_time=1.05)
        self.play(cursor.animate.shift(LEFT * 0.32), run_time=1.0)
        self.at("random fluctuation")
        pulse(wave[1], base=7, amp=2)
        self.at("controlled trials", lead=0.65)
        level.clear_updaters()
        check = label("✓", 5.36, 0.40, GREEN, 45)
        self.play(FadeOut(VGroup(bar, cursor)), Create(calibration()),
                  level.animate.set_value(0.46), run_time=0.55)
        self.add(check)
        self.finish()


class S02Title(TitleCard):
    LESSON = "Psychophysics and signal detection"
    TITLE = "Measuring What a Mind Detects"

    def construct(self):
        clock = running_clock(self)
        gauge, wave, subject, choice = bench_instruments(ValueTracker(0.46), clock)
        self.add(bench(), gauge, calibration(), wave, subject, choice,
                 label("✓", 5.36, 0.40, GREEN, 45))
        title = T(self.TITLE, 53, font=TITLE_FONT).move_to(point(0, 3.12))
        self.play(FadeIn(title), run_time=0.35)
        self.wait(1.30)
        self.play(FadeOut(title), run_time=0.35)


def psychometric():
    return Plot(box=(-0.94, 5.69, -1.45, 1.64), xr=(0, 1), yr=(0, 1),
                yticks=[(0, "0%"), (0.5, "50%"), (1, "100%")],
                size=28)


def probability(x):
    """Schematic psychometric curve: logistic model with its midpoint at x = 0.5."""
    return 1 / (1 + np.exp(-11 * (x - 0.50)))


def paw(x=-4.38, y=0.62):
    toes = VGroup(*[Ellipse(width=0.35, height=0.48, stroke_width=2, color=GREY,
                            fill_color=GREY, fill_opacity=0.7).move_to(point(x+dx, y+dy))
                    for dx, dy in [(-0.62, 0.21), (-0.21, 0.39), (0.20, 0.39), (0.61, 0.21)]])
    pad = Ellipse(width=1.75, height=0.83, stroke_width=3, color=GREY,
                  fill_color=GREY, fill_opacity=0.7).move_to(point(x, y-0.40))
    return VGroup(toes, pad)


class S03Threshold(SpokenScene):
    def construct(self):
        level = ValueTracker(0.05)
        gauge = stimulus_dial(level)
        plot = psychometric()
        rule = boxed_label("Fixed response rule", GREEN, 30).move_to(point(2.08, 2.91))
        ticks = calibration()
        fill = calibrated_fill(level)
        self.add(bench("two"), fill, gauge, ticks, plot)
        self.at("response rule fixed", lead=0.75)
        self.play(FadeIn(rule), run_time=0.42)
        self.at("repeated trials", lead=0.58)
        live = plot.live_curve(probability, level, YELLOW, width=7)
        dot = plot.dot(level.get_value, lambda: probability(level.get_value()), radius=0.13)
        self.add(live, dot)
        for value in (0.18, 0.30, 0.40):
            self.play(level.animate.set_value(value), run_time=0.98)
        threshold = label("Detection threshold", 2.12, -2.95, YELLOW, 34)
        self.at("smallest stimulus", lead=0.52)
        self.play(FadeIn(threshold), run_time=0.45)
        right_curve = plot.curve(probability, x0=0.4, color=YELLOW, width=7)
        right_reveal = ValueTracker(0.4)
        right_fill = always_redraw(lambda: shaded_curve(
            plot, probability, YELLOW, opacity=0.39, x_end=right_reveal.get_value(), x_start=0.4))
        self.add(right_fill)
        self.play(Create(right_curve), right_reveal.animate.set_value(1),
                  run_time=2.40, rate_func=linear)
        animal_paw = paw(y=1.23)
        self.at("rat cannot speak", lead=0.45)
        self.play(FadeOut(VGroup(fill, gauge, ticks, threshold)), run_time=0.34)
        self.play(FadeIn(animal_paw), run_time=0.42)
        # Track the next task independently while preserving the readout axes.
        self.remove(live, dot)
        self.play(FadeOut(rule), FadeOut(right_curve), FadeOut(right_fill), run_time=0.32)
        self.at("labs measure", lead=0.38)
        y_label = label("Paw lifts", 0.0, 2.02, YELLOW)
        self.play(FadeIn(y_label), run_time=0.34)
        force = ValueTracker(0.06)
        rise = ValueTracker(0)

        def filament():
            f = force.get_value()
            dy = rise.get_value()
            mount = RoundedRectangle(width=1.41, height=0.44, corner_radius=0.13,
                                     stroke_color=BLUE, stroke_width=3, fill_color=BLUE,
                                     fill_opacity=0.62).move_to(point(-4.38, -1.52+dy))
            stem = Line(point(-4.38, -1.30+dy), point(-4.38, -0.68+dy), color=BLUE,
                        stroke_width=4 + 19*f)
            return VGroup(mount, stem)

        fiber = always_redraw(filament)
        self.play(FadeIn(fiber), animal_paw.animate.shift(DOWN*0.61), run_time=0.54)
        self.play(rise.animate.set_value(0.51), run_time=0.94)
        self.at("Calibrated von Frey", lead=0.50)
        f_curve = plot.live_curve(probability, force, YELLOW, width=7)
        f_dot = plot.dot(force.get_value, lambda: probability(force.get_value()), radius=0.13)
        f_fill = always_redraw(lambda: shaded_curve(
            plot, probability, YELLOW, opacity=0.42, x_end=force.get_value()))
        self.add(f_fill, f_curve, f_dot)
        for value, lifts in ((0.15, False), (0.32, False), (0.50, False), (0.50, True)):
            self.play(force.animate.set_value(value), rise.animate.set_value(0), run_time=0.60)
            self.play(rise.animate.set_value(0.51), run_time=0.46)
            if lifts:
                self.play(animal_paw.animate.shift(UP*0.57), rate_func=there_and_back, run_time=0.41)
        self.at("Many labs use", lead=0.60)
        tail = ValueTracker(0.50)
        tail_fill = always_redraw(lambda: shaded_curve(
            plot, probability, YELLOW, opacity=0.42,
            x_start=0.50, x_end=tail.get_value()))
        tail_curve = plot.live_curve(probability, tail, YELLOW, width=7, x0=0.50)
        self.add(tail_fill, tail_curve)
        self.play(tail.animate.set_value(1), run_time=1.66, rate_func=linear)
        self.at("the force that lifts", lead=0.24)
        mid = DashedLine(plot.pt(0, 0.5), plot.pt(0.48, 0.5), color=GREEN, stroke_width=3)
        self.play(Create(mid), FadeIn(label("Withdrawal threshold", 2.12, -2.95, YELLOW, 34)),
                  run_time=0.62)
        self.finish()


def grating(cycles):
    """Equal-width black and white stripes have half the white luminance."""
    width, height = 1.49, 1.80
    count = 2 * cycles
    return VGroup(*[
        Rectangle(width=width/count, height=height, stroke_width=0, fill_opacity=1,
                  fill_color=WHITE if i % 2 else BLACK)
        .move_to(point(-5.29 - width/2 + (i+0.5)*width/count, 0.64))
        for i in range(count)
    ])


class S04ForcedChoice(SpokenScene):
    def construct(self):
        infant = silhouette(-0.80, 0.42, infant=True, facing=-1)
        observer = silhouette(4.45, 0.32, facing=-1)
        plain = Rectangle(width=1.49, height=1.80, stroke_width=0, fill_opacity=1,
                          fill_color="#BCBCBC").move_to(point(-3.48, 0.64))
        pattern = grating(3)
        self.add(bench("left"), infant)
        self.play(FadeIn(pattern, shift=RIGHT*0.36), FadeIn(plain, shift=LEFT*0.20), run_time=1.42)
        self.at("preferential looking")
        heading = label("Forced-choice preferential looking", 0, 3.12, TEXT, 37)
        self.play(FadeIn(heading), run_time=0.52)
        self.at("Infants prefer", lead=0.90)
        gaze = CurvedArrow(point(-1.86, 1.16), point(-5.29, 1.64),
                           angle=0.85, color=YELLOW, stroke_width=4, tip_length=0.15)
        self.play(infant.animate.shift(LEFT*0.40 + UP*0.16), run_time=0.61)
        self.play(Create(gaze), run_time=0.62)
        self.at("striped grating")
        border = VGroup(*[
            SurroundingRectangle(field, color=BLUE, buff=0.10, stroke_width=4)
            for field in (pattern, plain)
        ])
        self.play(Create(border), pattern.animate.stretch(1.10, 1),
                  plain.animate.stretch(1.10, 1), run_time=0.83)
        self.play(pattern.animate.stretch(1/1.10, 1), plain.animate.stretch(1/1.10, 1),
                  run_time=0.68)
        self.at("equal brightness", lead=0.35)
        brightness = label("Equal mean brightness", -3.93, -0.98, BLUE, 29)
        self.play(FadeIn(brightness), run_time=0.48)
        self.at("An observer who", lead=0.50)
        screen = RoundedRectangle(width=0.24, height=2.66, corner_radius=0.10,
                                  fill_color=BLUE, fill_opacity=0.87, stroke_width=0)
        screen.move_to(point(1.78, 0.52))
        self.play(FadeIn(screen), FadeIn(observer), FadeOut(brightness), run_time=0.70)
        self.at("judges the gaze", lead=0.42)
        score = boxed_label("Judged left", GREEN, 29).move_to(point(4.42, -1.43))
        self.play(FadeIn(score), run_time=0.50)
        self.at("finest grating", lead=0.70)
        for cycles in (6, 12, 24):
            self.play(FadeOut(pattern), run_time=0.12)
            pattern = grating(cycles)
            self.add(pattern)
            self.wait(0.30)
        inconclusive = boxed_label("No clear side", GREY, 29).move_to(score)
        self.play(FadeOut(gaze), FadeOut(pattern), swap(score, inconclusive, run_time=0.42),
                  run_time=0.42)
        too_fine = grating(40)
        self.add(too_fine)
        self.at("gives acuity", lead=0.54)
        self.remove(too_fine)
        self.add(grating(24))
        acuity_mark = label("Acuity", -4.42, -1.12, YELLOW, 34)
        self.play(FadeIn(gaze), FadeIn(acuity_mark), swap(inconclusive, score, run_time=0.50),
                  run_time=0.50)
        self.finish()


def gaussian(x, mean):
    """Equal-variance signal detection model, mean in units of the noise SD."""
    return np.exp(-0.5*(x - mean)**2) / np.sqrt(2*PI)


def shaded_curve(plot, fn, color, opacity=0.41, x_end=None, x_start=None):
    start = plot.xr[0] if x_start is None else x_start
    end = plot.xr[1] if x_end is None else max(x_end, start + 0.0001)
    xs = np.linspace(start, end, 100)
    curve_points = [plot.pt(x, fn(x)) for x in xs]
    return Polygon(plot.pt(xs[0], 0), *curve_points, plot.pt(xs[-1], 0),
                   stroke_width=0, fill_color=color, fill_opacity=opacity)


class S05SignalNoise(SpokenScene):
    def construct(self):
        plot = Plot(box=(-5.65, 5.65, -1.41, 2.03), xr=(-3.5, 5), yr=(0, 0.46),
                    xlabel="Internal response", label_size=28)
        plot.xlabel.move_to(point(3.30, -2.72))
        axis_label = label("Noise", -4.12, 1.89, RED, 31)
        clock = running_clock(self)
        mean = ValueTracker(0.0)
        noise_fn = lambda x: gaussian(x, 0)
        sweep = ValueTracker(-1.10)
        partial = always_redraw(lambda: shaded_curve(
            plot, noise_fn, RED, opacity=0.46 + 0.27*np.sin(2.45*clock.get_value()),
            x_end=sweep.get_value()))
        noise_curve = plot.live_curve(noise_fn, sweep, RED, width=7)
        self.add(bench("wide"), plot, partial, noise_curve)
        self.at("Why is there")
        self.play(sweep.animate.set_value(5), run_time=4.22, rate_func=linear)
        self.add(axis_label)
        self.at("responses fluctuate", lead=0.5)
        rng = np.random.default_rng(23)
        samples = rng.normal(size=(12, 22))
        samples = np.clip(samples, -2.6, 2.6)

        def sample_marks():
            row = samples[int(clock.get_value() * 3) % len(samples)]
            previous = VGroup(*[
                Dot(plot.pt(x, 0.019 + 0.008*(i % 12)), radius=0.102,
                    color=RED, fill_opacity=0.82)
                for i, x in enumerate(row[:-1])
            ])
            last = row[-1]
            current = Rectangle(width=0.33, height=1.43, stroke_width=0,
                                fill_color=RED, fill_opacity=0.76)
            current.move_to(plot.pt(last, 0) + UP*0.74)
            tip = Dot(current.get_top(), radius=0.14, color=TEXT)
            return VGroup(previous, current, tip)

        dots = always_redraw(sample_marks)
        self.add(dots)
        self.at("standard deviation", lead=0.83)
        a, b = plot.pt(0, 0), plot.pt(1, 0)
        width = arrow(a + DOWN*0.87, b + DOWN*0.87, RED, double=True)
        sd = label("Noise SD", -0.95, -2.93, RED, 30)
        # Put the width annotation below the bench rail in a dedicated lane.
        width.shift(DOWN*0.40)
        sd.move_to(point(-2.55, -2.71))
        self.play(GrowFromCenter(width), FadeIn(sd), run_time=0.52)
        self.at("Detectability", lead=0.44)
        base = label("d′ =", -3.70, 3.12, TEXT, 40)
        signal_curve = always_redraw(lambda: plot.curve(
            lambda x: gaussian(x, mean.get_value()), color=YELLOW, width=7))
        signal_fill = always_redraw(lambda: shaded_curve(
            plot, lambda x: gaussian(x, mean.get_value()), YELLOW, opacity=0.28))
        self.remove(dots)
        self.add(signal_fill, signal_curve)
        self.play(FadeIn(base), mean.animate.set_value(0.76), run_time=1.48)
        self.at("shift in mean", lead=0.25)
        span = always_redraw(lambda: arrow(
            plot.pt(0, gaussian(0, 0)) + UP*0.30,
            plot.pt(mean.get_value(), gaussian(0, 0)) + UP*0.30,
            YELLOW, double=True,
        ))
        shift = label("Mean shift", -0.57, 3.12, YELLOW, 38)
        self.add(span)
        self.play(FadeIn(shift), mean.animate.set_value(2.2), run_time=2.30)
        self.add(label("Signal + noise", 4.30, 1.87, YELLOW, 29))
        self.at("divided by that", lead=0.35)
        self.play(FadeIn(label("/", 1.06, 3.12, TEXT, 39)),
                  FadeIn(label("Noise SD", 2.69, 3.12, RED, 38)), run_time=0.59)
        self.at("Psychophysics pairs", lead=0.65)
        self.play(FadeOut(Group(*[m for m in self.mobjects if m is not clock])),
                  run_time=0.42)
        gauge, wave, subject, choice = bench_instruments(ValueTracker(0.46), clock)
        self.add(bench(), gauge, wave, subject, choice, label("✓", 5.36, 0.40, GREEN, 45))
        for text, x, color, cue in (
            ("Controlled stimulus", -4.38, BLUE, "controlled stimuli"),
            ("Fixed rules", 4.38, GREEN, "fixed rules"),
            ("Signal vs noise", 0, YELLOW, "separate signals"),
        ):
            self.at(cue, lead=0.44)
            self.play(FadeIn(label(text, x, -1.54, color, 29)), run_time=0.45)
        self.finish()


def fingertip():
    return RoundedRectangle(width=2.60, height=1.04, corner_radius=0.50,
                            fill_color=GREY, fill_opacity=0.65, stroke_color=GREY,
                            stroke_width=3).move_to(point(-4.38, 0.97))


def vibration_probe(clock, amplitude):
    def body():
        offset = 0.40 * amplitude.get_value() / AUTISTIC * np.sin(7.9*clock.get_value())
        return RoundedRectangle(
            width=0.72, height=1.37, corner_radius=0.16,
            stroke_color=BLUE, stroke_width=4, fill_color=BLUE, fill_opacity=0.57,
        ).move_to(point(-4.38 + offset, -0.23))

    return always_redraw(body)


def threshold_data():
    """Puts et al. static fingertip-vibration threshold means, in micrometres."""
    plot = Plot(box=(-1.25, 5.83, -1.11, 2.02), xr=(0, 3), yr=(0, 10),
                yticks=[(0, "0"), (5, "5"), (10, "10")], size=28)
    axis = label("µm", -0.64, 2.17, TEXT, 28)
    bars = VGroup()
    for x, value, color in ((0.86, TYPICAL, BLUE), (2.15, AUTISTIC, ORANGE)):
        h = plot.pt(x, value)[1] - plot.y0
        bar = Rectangle(width=1.12, height=max(h, 0.001), fill_color=color,
                        fill_opacity=0.82, stroke_color=color, stroke_width=2)
        bar.move_to(plot.pt(x, 0) + UP*h/2)
        bars.add(bar)
    groups = VGroup(
        label("Typically developing", plot.pt(0.86, 0)[0], -1.50, BLUE, 28),
        label("Autistic", plot.pt(2.15, 0)[0], -1.50, ORANGE, 28),
    )
    counts = VGroup(
        label("n = 67", plot.pt(0.86, 0)[0], -2.69, TEXT, 28),
        label("n = 32", plot.pt(2.15, 0)[0], -2.69, TEXT, 28),
    )
    return plot, axis, bars, groups, counts


def bar_value(bar, value, color):
    return label(f"{value:.2f} µm", bar.get_x(), bar.get_top()[1] + 0.25, color, 29)


def study_note():
    return label("Puts and colleagues, 2014  ·  Ages 8–12", -2.40, -3.31, GOLD, 28)


def study_world(clock=None, amplitude=None):
    plot, axis, bars, groups, counts = threshold_data()
    probe = vibration_probe(clock if clock is not None else ValueTracker(0),
                            amplitude if amplitude is not None else ValueTracker(TYPICAL))
    digits = VGroup(bar_value(bars[0], TYPICAL, BLUE), bar_value(bars[1], AUTISTIC, ORANGE))
    world = VGroup(bench("two"), fingertip(), probe, plot, axis, bars, groups, counts, digits, study_note())
    world.chart, world.bars = plot, bars
    return world


class S06PredictQ(SpokenScene):
    def construct(self):
        clock = running_clock(self)
        top = label("Static finger-vibration threshold", -0.42, 3.18, TEXT, 36)
        plot, axis, bars, groups, counts = threshold_data()
        self.add(bench("two"), fingertip(), vibration_probe(clock, ValueTracker(TYPICAL)))
        self.at("2014")
        self.play(FadeIn(study_note()), run_time=0.44)
        self.at("measured static finger", lead=0.65)
        self.play(FadeIn(top), FadeIn(plot), FadeIn(axis), run_time=0.72)
        self.at("typically developing children", lead=0.45)
        self.play(FadeIn(groups), FadeIn(counts), run_time=0.56)
        self.at("cohort averaged", lead=0.35)
        self.play(GrowFromEdge(bars[1], DOWN), run_time=0.89)
        self.play(FadeIn(bar_value(bars[1], AUTISTIC, ORANGE)), run_time=0.35)
        self.at("against 6", lead=0.55)
        self.play(GrowFromEdge(bars[0], DOWN), run_time=0.91)
        self.play(FadeIn(bar_value(bars[0], TYPICAL, BLUE)), run_time=0.35)
        self.at("Does that higher", lead=0.43)
        self.play(swap(top, question_card(QUESTION, **QUESTION_STYLE), run_time=0.60))
        # Settle to the same probe pose as the prediction hold.
        self.wait(2.95)
        clock.clear_updaters()
        clock.set_value(0)
        self.finish()


class S07PredictPause(PredictPause):
    QUESTION = QUESTION
    CARD = QUESTION_STYLE
    RING_AT = (5.37, 0.08, 0)
    SECONDS = 4.5

    def backdrop(self):
        return study_world()

    def construct(self):
        self.add(self.backdrop(), question_card(self.QUESTION, **self.CARD))
        ring, sweep = countdown(self.SECONDS, center=self.RING_AT, radius=0.89)
        progress = sweep.mobject
        dial_face = always_redraw(lambda: Sector(
            radius=0.85, start_angle=PI/2,
            angle=max(progress.get_value(), 0.001)*TAU,
            fill_color=YELLOW, fill_opacity=0.94, stroke_width=0,
        ).move_arc_center_to(self.RING_AT))
        self.add(dial_face, ring)
        self.play(sweep)


class S08PredictA(SpokenScene):
    def construct(self):
        clock = running_clock(self)
        amplitude = ValueTracker(TYPICAL)
        world = study_world(clock, amplitude)
        question = question_card(QUESTION, **QUESTION_STYLE)
        self.add(world, question)
        self.at("Poorr detection")
        verdict = label("Poorer detection", -0.50, 3.17, YELLOW, 42)
        self.play(swap(question, verdict, run_time=0.64))
        self.at("a higher threshold")
        self.play(Indicate(world.bars[1], color=ORANGE, scale_factor=1.03), run_time=1.75)
        self.at("stimulus had to grow", lead=0.51)
        self.play(amplitude.animate.set_value(AUTISTIC), run_time=1.62)
        self.at("Subtract 6", lead=0.30)
        self.play(FadeOut(verdict), run_time=0.28)
        minuend = label(f"{AUTISTIC:.2f}", -3.48, 3.17, ORANGE, 37)
        subtrahend = label(f"− {TYPICAL:.2f}", -2.05, 3.17, BLUE, 37)
        self.play(FadeIn(subtrahend), run_time=0.47)
        self.at("from 9", lead=0.26)
        self.play(FadeIn(minuend), run_time=0.42)
        equation_a = VGroup(minuend, subtrahend)
        self.at("2 .54", lead=0.30)
        equation_b = label(f"= {DIFFERENCE:.2f} µm", 0.37, 3.17, YELLOW, 37)
        self.play(FadeIn(equation_b), run_time=0.42)
        chart = world.chart
        a = chart.pt(1.55, TYPICAL)
        b = chart.pt(1.55, AUTISTIC)
        gap = arrow(a, b, YELLOW, double=True)
        guides = VGroup(
            DashedLine(point(world.bars[0].get_right()[0] + 0.05, a[1]), a + LEFT*0.11,
                       color=BLUE, stroke_width=2, dash_length=0.09),
            DashedLine(b + RIGHT*0.11, point(world.bars[1].get_left()[0] - 0.05, b[1]),
                       color=ORANGE, stroke_width=2, dash_length=0.09),
        )
        self.play(Create(guides), GrowFromCenter(gap), run_time=0.59)
        self.at("Divided by 6", lead=0.55)
        fraction = label(f"{DIFFERENCE:.2f} / {TYPICAL:.2f}", -2.52, 3.17, TEXT, 37)
        self.play(FadeOut(equation_b), swap(equation_a, fraction), run_time=0.48)
        self.at("38 .5", lead=0.35)
        relative = label(f"= {100*DIFFERENCE/TYPICAL:.1f}% higher", 1.04, 3.17, YELLOW, 37)
        self.play(FadeIn(relative), run_time=0.51)
        self.finish()


def warning_tag(text, x, y):
    return boxed_label(text, RED, 30).move_to(point(x, y))


def shield(x, y):
    return Polygon(*[point(x+dx, y+dy) for dx, dy in
                     [(-0.59, 0.51), (0.59, 0.51), (0.51, -0.19), (0, -0.64), (-0.51, -0.19)]],
                   color=GREEN, stroke_width=4, fill_color=GREEN, fill_opacity=0.36)


class S09Controls(SpokenScene):
    def construct(self):
        clock = running_clock(self)
        self.add(bench("wide"))
        level = ValueTracker(0.55)
        level.add_updater(lambda m: m.set_value(0.55 + 0.32*np.sin(1.8*clock.get_value())))
        self.add(level)
        gauge = stimulus_dial(level, point(-3.20, 0.10), radius=1.48)
        measured = label("Lab detection", -3.20, -1.27, YELLOW, 33)
        self.at("a threshold only", lead=0.55)
        self.play(FadeIn(gauge), run_time=0.75)
        self.play(FadeIn(measured), run_time=0.42)
        self.at("Lab detection cannot", lead=0.57)
        wall = Line(point(0, -1.43), point(0, 1.86), color=GREY, stroke_width=4)
        distress = silhouette(3.03, 0.42, facing=-1)
        bolt = Polygon(*[point(x, y) for x, y in [(4.03, 1.44), (3.74, 0.83), (4.02, 0.88),
                                                  (3.82, 0.31), (4.44, 1.05), (4.14, 1.00)]],
                       fill_color=RED, fill_opacity=1, stroke_width=0)
        right_label = label("Everyday distress", 3.13, -1.27, TEXT, 33)
        self.play(Create(wall), FadeIn(distress), FadeIn(bolt), run_time=0.74)
        self.play(FadeIn(right_label), run_time=0.38)
        self.at("paw withdrawal", lead=0.52)
        pet = paw(-3.20, 0.43)
        lift = arrow(point(-1.98, -0.42), point(-1.98, 1.25), YELLOW)
        self.play(FadeOut(gauge), FadeOut(measured), FadeIn(pet), GrowArrow(lift), run_time=0.72)
        self.play(pet.animate.shift(UP*0.50), rate_func=there_and_back, run_time=0.82)
        reflex = label("Withdrawal reflex", -3.20, -1.27, YELLOW, 33)
        self.play(FadeIn(reflex), run_time=0.38)
        self.at("not unpleasantness", lead=0.42)
        other = label("Unpleasantness", 3.13, -1.27, TEXT, 33)
        self.play(swap(right_label, other), run_time=0.52)
        self.at("Practice", lead=0.58)
        self.play(FadeOut(VGroup(pet, lift, reflex, wall, distress, bolt, other)), run_time=0.42)
        gauge = stimulus_dial(level, point(3.92, 0.04), radius=1.49)
        self.add(gauge)
        hazards = VGroup(warning_tag("Practice", -4.18, 1.41),
                         warning_tag("Expectation", -4.08, 0.24),
                         warning_tag("Grader bias", -4.02, -0.93))
        self.play(FadeIn(hazards[0]), run_time=0.55)
        self.at("expectation")
        self.play(FadeIn(hazards[1]), hazards[0].animate.shift(RIGHT*1.30), run_time=0.69)
        self.at("greater bias", lead=0.26)
        self.play(FadeIn(hazards[2]), hazards[1].animate.shift(RIGHT*1.22), run_time=0.52)
        self.play(hazards.animate.shift(RIGHT*1.15), run_time=2.33)
        self.at("masked observers", lead=0.47)
        first, second = shield(-0.03, 1.08), shield(0.02, -0.44)
        self.play(FadeIn(first, shift=LEFT*0.55), run_time=0.56)
        self.at("masked grading", lead=0.46)
        self.play(hazards.animate.shift(LEFT*1.42), FadeIn(second),
                  FadeIn(label("Masked grading", -0.03, 1.98, GREEN, 28)), run_time=0.65)
        self.at("randomized control", lead=0.46)
        self.play(FadeOut(hazards, shift=LEFT*1.23),
                  FadeIn(label("Randomized controls", 0.02, -1.47, GREEN, 28)), run_time=0.67)
        self.finish()


def rod_grid():
    grid = VGroup()
    for j in range(25):
        for i in range(20):
            grid.add(Dot(point(-2.70+0.354*j, -1.50+0.179*i), radius=0.067, color=GREY))
    return grid


def photon(x, y):
    return Star(n=4, outer_radius=0.33, inner_radius=0.09,
                color=BLUE, stroke_width=0, fill_color=BLUE, fill_opacity=1).move_to(point(x, y))


def rod(x, y):
    return VGroup(
        RoundedRectangle(width=0.55, height=1.38, corner_radius=0.21,
                         stroke_color=YELLOW, stroke_width=3, fill_color=YELLOW,
                         fill_opacity=0.45).move_to(point(x, y+0.44)),
        Circle(radius=0.29, color=GREY, fill_color=GREY, fill_opacity=0.68)
        .move_to(point(x, y-0.46)),
    )


def rod_response(t):
    """Normalized schematic of a quantal current response with rise and recovery."""
    u = max(0, t - 0.18)
    return (1-np.exp(-u/0.13))*np.exp(-u/0.63)


class S10UnlockedVision(SpokenScene):
    def construct(self):
        clock = running_clock(self)
        grid = rod_grid()
        grid.set_opacity(0.32)
        flash = photon(-4.55, 0.39)
        pulse(flash, base=2, amp=1.8)
        flash.add_updater(lambda m: m.set_fill(opacity=0.63 + 0.34*np.sin(4.0*clock.get_value())))
        self.add(bench("wide"), grid)
        self.at("safeguards unlocked")
        self.play(FadeIn(flash, scale=0.63), run_time=1.1)
        self.at("1942", lead=0.62)
        title = label("Hecht, Shlaer & Pirenne, 1942", -0.48, 3.16, GOLD, 36)
        self.play(FadeIn(title), grid.animate.set_opacity(1), run_time=1.35)
        self.at("the faintest flashes", lead=0.63)
        beam = Polygon(point(-4.36, 0.80), point(-2.66, 2.01), point(-2.66, -1.49),
                       stroke_width=0, fill_color=BLUE, fill_opacity=0.38)
        self.play(flash.animate.move_to(point(-4.45, 0.80)).scale(1.38), FadeIn(beam),
                  run_time=1.24)
        self.play(beam.animate.stretch(1.28, 0).set_fill(opacity=0.58), run_time=1.25)
        self.play(beam.animate.set_fill(opacity=0.22), run_time=1.41)
        hits = VGroup(*[Dot(grid[n].get_center(), radius=0.11, color=YELLOW)
                        for n in (61, 138, 189, 273, 306, 422)])
        self.at("few absorptions", lead=0.64)
        self.play(LaggedStart(*[GrowFromCenter(d) for d in hits], lag_ratio=0.26),
                  FadeOut(beam), run_time=1.60)
        self.at("about 500 rods", lead=0.44)
        cell_count = label("About 500 rods", 1.53, -2.96, TEXT, 32)
        self.play(FadeIn(cell_count), run_time=0.59)
        cell = rod(-4.42, 0.08)
        self.at("one quantum of light", lead=0.57)
        self.play(FadeOut(flash), FadeIn(cell), run_time=0.60)
        single = photon(-4.42, 1.76)
        self.play(GrowFromCenter(single), run_time=0.50)
        self.at("single photon", lead=0.28)
        self.play(single.animate.move_to(point(-4.42, 0.92)).set_opacity(0.1), run_time=0.73)
        self.remove(single)
        self.at("enough to excite", lead=0.46)
        glow = Circle(radius=0.81, stroke_color=YELLOW, stroke_width=5,
                      fill_color=YELLOW, fill_opacity=0.28).move_to(cell)
        self.play(Indicate(cell, color=YELLOW, scale_factor=1.16),
                  FadeIn(glow, scale=0.44, rate_func=there_and_back), run_time=1.55)
        self.remove(glow)
        self.at("rod recordings", lead=1.06)
        old = VGroup(grid, hits, title, cell_count)
        self.play(FadeOut(old), run_time=0.40)
        pipette = Polygon(point(-4.25, 0.32), point(-3.49, 0.32), point(-3.24, 2.18), point(-4.50, 2.18),
                          stroke_color=BLUE, stroke_width=4, fill_color=BLUE, fill_opacity=0.25)
        local_rod = rod(-3.87, -0.47)
        self.remove(cell)
        plot = Plot(box=(-1.50, 5.79, -1.29, 1.78), xr=(0, 2.6), yr=(0, 0.9),
                    xlabel="Time", label_size=28)
        cursor = ValueTracker(0.04)
        self.add(plot, local_rod, pipette, plot.live_curve(rod_response, cursor, YELLOW, width=8))
        self.play(FadeIn(label("Baylor, Lamb & Yau, 1979", -0.46, 3.16, GOLD, 36)),
                  cursor.animate.set_value(2.6), run_time=2.25, rate_func=linear)
        self.add(label("Single-quantum response", 2.21, -2.99, YELLOW, 30))
        self.finish()


def contacts(n=20):
    points = [point(-4.36 + 1.40*np.cos(a), 0.28+1.40*np.sin(a))
              for a in np.linspace(0.18, TAU-0.65, 20)]
    cable = VMobject(stroke_color=GREY, stroke_width=8).set_points_as_corners(points)
    pads = VGroup(*[Dot(p, 0.092, color=BLUE if i < n else GREY) for i, p in enumerate(points)])
    return cable, pads


def sense_icons():
    x, y = -4.38, 0.44
    eye = VGroup(Ellipse(width=2.28, height=1.05, color=BLUE, stroke_width=5),
                 Circle(radius=0.37, color=BLUE, stroke_width=3, fill_color=BLUE, fill_opacity=0.53))
    eye.move_to(point(x, y))
    top = RoundedRectangle(width=2.37, height=1.09, corner_radius=0.53,
                           color=BLUE, stroke_width=4, fill_color=GREY, fill_opacity=0.58).move_to(point(0, y+0.40))
    tap = Line(point(0, y-0.54), point(0, y-0.13), color=BLUE, stroke_width=7)
    ear = VGroup(*[Arc(radius=r, start_angle=-1.0, angle=3.4, stroke_width=5, color=BLUE,
                        arc_center=point(4.38, y)) for r in (0.46, 0.79, 1.10)])
    return eye, VGroup(top, tap), ear


class S11UnlockedClose(SpokenScene):
    def construct(self):
        phase = running_clock(self)
        cable, pads = contacts()
        plot = Plot(box=(-1.65, 5.67, -1.28, 1.72), xr=(0, 6), yr=(0, 3))
        strength = ValueTracker(1.25)
        noise_plot = trace(plot, lambda x, t: 0.66 + 0.31*noise(x, t), RED, phase, width=5)
        speech = trace(plot, lambda x, t: strength.get_value()
                       + 0.38*noise(x*0.76, t*0.68), YELLOW, phase, width=7)
        author = label("Schvartz-Leyzac, Zwolan & Pfingst, 2017", -0.40, 3.16, GOLD, 35)
        self.add(bench("two"), plot, noise_plot)
        self.at("2017", lead=0.30)
        self.play(FadeIn(author), run_time=0.62)
        self.at("seven adults listening", lead=0.60)
        count = label("20 active contacts", -4.38, -1.45, BLUE, 29)
        self.play(Create(cable), FadeIn(pads), FadeIn(speech), run_time=1.22)
        self.play(FadeIn(count), run_time=0.53)
        self.at("to 8", lead=0.58)
        next_count = label("8 active contacts", -4.38, -1.45, BLUE, 29)
        self.play(*[p.animate.set_color(GREY).set_opacity(0.42) for p in pads[8:]],
                  swap(count, next_count), run_time=0.88)
        self.at("be louder against", lead=0.52)
        ref_y = 2.03
        ref = DashedLine(plot.pt(0, ref_y), plot.pt(6, ref_y), color=GREEN, stroke_width=3)
        self.play(Create(ref), strength.animate.set_value(2.27), run_time=1.29)
        noise_label = label("Background noise", 1.94, -2.94, RED, 30)
        self.add(noise_label)
        self.at("the touch thresholds", lead=0.42)
        self.play(FadeOut(VGroup(cable, pads, next_count, plot, noise_plot, speech, ref, author, noise_label)),
                  run_time=0.40)
        self.remove(*[m for m in self.mobjects if m is not phase])
        self.add(bench())
        eye, touch, hearing = sense_icons()
        self.play(LaggedStart(FadeIn(eye), FadeIn(touch), FadeIn(hearing), lag_ratio=0.42), run_time=1.25)
        self.at("what controlled trials", lead=0.76)
        for item in (eye, touch, hearing):
            pulse(item, base=5, amp=2.4, speed=4)
        self.play(LaggedStart(*[
            FadeIn(label(text, x, -1.27, color, 29))
            for text, x, color in (("Vision", -4.38, TEXT), ("Touch", 0, TEXT),
                                   ("Hearing", 4.38, TEXT))
        ], lag_ratio=0.38), run_time=1.25)
        self.finish()


class S12End(EndCard):
    LINE = "Fixed rules and controls separate sensory signals from noise and bias."
