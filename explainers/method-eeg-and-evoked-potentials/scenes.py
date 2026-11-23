"""EEG, ERG and evoked potentials: one surface-recording world.

Color map adapted from Patch Clamp: blue = electrodes and apparatus; yellow =
electrical activity; grey = tissue and structure; green = isolated response;
red = block, absence or inference limit; orange = light; teal = fluid;
purple = sleep pressure and waking duration; gold = dates and takeaways.
Dark fills are shades of the corresponding structural or apparatus colors.
"""
from bp_parts import *


PANEL = "#243045"
TISSUE = "#343D53"
CORTEX = "#555C76"
GRID = "#3A4B63"
ORANGE = "#F29E4C"
SLEEP_PRESSURE = "#C1A0F0"
QUESTION = "What must you block to read only photoreceptors?"
QUESTION_STYLE = dict(y=3.25, max_w=10.8, size=34)
WINDOW = 7.2
START, STOP = 0.83, 6.38
MID = (START + STOP) / 2


def point(x, y):
    return np.array([x, y, 0.0])


def path(start, segments, color=GREY, width=3, fill=None, opacity=1):
    """A cubic outline for the anatomy, using scene coordinates."""
    curve = VMobject(stroke_color=color, stroke_width=width)
    curve.start_new_path(point(*start))
    for a, b, c in segments:
        curve.add_cubic_bezier_curve_to(point(*a), point(*b), point(*c))
    if fill:
        curve.close_path()
        curve.set_fill(fill, opacity)
    return curve


def wire(points, color=BLUE, width=3):
    return VMobject(stroke_color=color, stroke_width=width).set_points_as_corners(
        [point(*p) for p in points]
    )


def left_text(words, x, y, color=TEXT, size=32):
    return T(words, size, color, weight=BOLD).move_to(point(x, y), aligned_edge=LEFT)


def electrode(x, y, angle=0):
    pad = RoundedRectangle(width=0.54, height=0.16, corner_radius=0.08,
                           stroke_width=2.5, stroke_color=BLUE,
                           fill_color=BLUE, fill_opacity=0.65).move_to(point(x, y))
    lead = path((x, y + 0.08), [((x, y + 0.45), (x + 0.24, y + 0.55), (x + 0.55, y + 0.55))],
                BLUE, 3.5)
    return VGroup(lead, pad).rotate(angle, about_point=point(x, y))


class Head(VGroup):
    """Same lateral section for EEG, VEP, looking, and sleep."""
    def __init__(self):
        super().__init__()
        scalp = path((-4.85, -2.5), [
            ((-4.67, -1.88), (-4.86, -1.35), (-5.37, -0.95)),
            ((-6.23, -0.22), (-6.15, 1.26), (-5.49, 1.98)),
            ((-4.72, 2.91), (-3.31, 2.91), (-2.44, 2.38)),
            ((-1.67, 1.94), (-1.52, 1.19), (-1.49, 0.51)),
            ((-1.46, 0.24), (-1.1, 0.02), (-1.00, -0.26)),
            ((-0.96, -0.43), (-1.47, -0.44), (-1.43, -0.55)),
            ((-1.35, -0.69), (-1.32, -0.72), (-1.48, -0.77)),
            ((-1.34, -0.92), (-1.55, -0.92), (-1.50, -1.01)),
            ((-1.34, -1.48), (-1.62, -1.63), (-2.34, -1.51)),
            ((-2.80, -1.52), (-2.82, -2.06), (-2.76, -2.5)),
            ((-3.30, -2.76), (-4.37, -2.74), (-4.85, -2.5)),
        ], GREY, 4, TISSUE)
        brain = path((-5.36, -0.30), [
            ((-5.83, 0.03), (-5.76, 1.24), (-5.23, 1.72)),
            ((-4.51, 2.57), (-3.41, 2.52), (-2.61, 2.08)),
            ((-1.99, 1.72), (-1.85, 1.30), (-1.93, 0.91)),
            ((-2.13, 0.45), (-2.70, 0.61), (-2.98, 0.27)),
            ((-3.24, -0.13), (-3.56, -0.29), (-4.08, -0.21)),
            ((-4.50, -0.10), (-4.99, -0.70), (-5.36, -0.30)),
        ], "#A5ABBE", 3, CORTEX)
        folds = VGroup()
        for x, y, angle in [(-5.12, 0.37, -20), (-5.15, 1.25, 30), (-4.50, 1.67, -25),
                            (-3.75, 1.91, 20), (-3.00, 1.68, -25), (-2.50, 1.21, -20),
                            (-4.47, 0.65, -35), (-3.76, 1.02, 18), (-3.13, 0.98, -25)]:
            fold = path((-0.30, -0.15), [((-0.41, 0.11), (-0.12, 0.35), (0.06, 0.15)),
                                        ((0.23, -0.05), (0.01, -0.31), (0.28, -0.24))],
                        "#7E879F", 3.5)
            folds.add(fold.rotate(angle * DEGREES).shift(point(x, y)))
        stem = path((-4.22, -0.30), [((-4.01, -0.24), (-3.64, -0.30), (-3.59, -0.44)),
                    ((-3.48, -0.68), (-3.67, -0.75), (-3.75, -1.19)),
                    ((-3.87, -1.25), (-4.09, -1.18), (-4.09, -0.99)),
                    ((-4.05, -0.57), (-4.26, -0.67), (-4.22, -0.30))], GREY, 2.5, CORTEX)
        nerve = path((-1.83, 0.26), [((-2.28, 0.12), (-2.62, 0.36), (-2.95, 0.58))],
                     "#8F98B2", 5)
        globe = Ellipse(width=0.81, height=0.56, color=GREY, stroke_width=3,
                        fill_color="#79849A", fill_opacity=1).move_to(point(-1.92, 0.33))
        retinal_arc = Arc(radius=0.29, start_angle=0.65 * PI, angle=0.70 * PI,
                          arc_center=point(-1.98, 0.34), color="#AAB6D0", stroke_width=5)
        self.pupil = Dot(point(-1.67, 0.34), radius=0.10, color=BG)
        self.eye = VGroup(globe, retinal_arc, self.pupil)
        self.lid = path((-2.23, 0.37), [((-2.04, 0.17), (-1.80, 0.17), (-1.60, 0.37))],
                        TEXT, 3)
        self.sleep = VGroup(Ellipse(width=0.81, height=0.56, stroke_width=0,
                                    fill_color=TISSUE, fill_opacity=1).move_to(globe), self.lid)
        self.anatomy = VGroup(scalp, nerve, stem, brain, folds, self.eye)
        self.scalp = VGroup(electrode(-5.73, 1.67, 39 * DEGREES),
                            electrode(-4.49, 2.61, 12 * DEGREES))
        self.eye_pad = electrode(-1.38, 0.53, -75 * DEGREES)
        self.chin_pad = electrode(-1.67, -1.48, 157 * DEGREES)
        self.add(self.anatomy)

    def cortex_currents(self, time, focus=None):
        """Glow on the dendrites. The same source terms also drive the EEG."""
        sites = [(-5.27, 0.61), (-5.27, 1.24), (-4.89, 1.71), (-4.33, 1.95),
                 (-3.68, 2.04), (-3.05, 1.85), (-2.64, 1.58), (-2.27, 1.24),
                 (-4.81, 0.88), (-4.02, 1.19), (-3.23, 1.10), (-4.48, 0.26)]
        currents = VGroup()
        for index, (x, y) in enumerate(sites):
            if focus is not None and index not in (0, 1, 2, 8):
                continue
            branch = VGroup(
                wire([(x - .12, y - .13), (x, y), (x + .13, y + .12)], YELLOW, 5),
                wire([(x, y), (x - .12, y + .14)], YELLOW, 3),
                Dot(point(x, y), radius=.072, color=YELLOW),
            )

            def light(mob, dt, i=index):
                t = time()
                amplitude = (.13 + .87 * flash_glow(t - .31)) if focus else (
                    .16 + .84 * (.5 + .5 * individual_current(t, i)) ** 2
                )
                mob[0].set_stroke(opacity=amplitude)
                mob[1].set_stroke(opacity=amplitude)
                mob[2].set_fill(opacity=amplitude)

            branch.add_updater(light, call_updater=True)
            currents.add(branch)
        return currents


def gaussian(t, center, sigma):
    return np.exp(-0.5 * ((t - center) / sigma) ** 2)


def individual_current(t, index):
    return np.sin(TAU * ((.53 + .135 * (index % 5)) * t + .071 * index))


def eeg(t):
    """Normalized sum of asynchronous dendritic currents."""
    return .20 * sum(individual_current(t, i) for i in range(12))


def phase(t, period=2.8):
    return np.remainder(t, period)


def evoked(t):
    u = phase(t)
    return .14 * eeg(t) - .44 * gaussian(u, .24, .07) + .93 * gaussian(u, .43, .12) - .37 * gaussian(u, .70, .19)


def flash_glow(t):
    return gaussian(phase(t + .12), .14, .13)


def receptor_signal(t):
    u = phase(t)
    return -.76 * (1 - np.exp(-u / .14)) * np.exp(-u / .69)


def bipolar_signal(t):
    u = phase(t)
    return .87 * gaussian(u, .64, .29)


def ganglion_signal(t, sigma=.019):
    u = phase(t)
    return .19 * sum(gaussian(u, spike, sigma) for spike in (.54, .70, .86))


def retinal_sum(t):
    return receptor_signal(t) + bipolar_signal(t) + ganglion_signal(t)


def eye_movement(t):
    u = phase(t, 4.1)
    return .82 * gaussian(u, .8, .21) - .51 * gaussian(u, 2.25, .26)


def chin_tone(t):
    envelope = .29 + .17 * np.sin(TAU * .19 * t)
    return envelope * (np.sin(TAU * 4.7 * t) + .55 * np.sin(TAU * 7.37 * t))


def slow_eeg(t):
    u = phase(t, 3.35)
    return .86 * gaussian(u, .65, .31) - .64 * gaussian(u, 1.27, .42) + .10 * np.sin(TAU * .9 * t)


def csf_flow(t):
    return .86 * gaussian(phase(t, 3.35), 1.95, .43)


def scope():
    return scope_tag("Schematic", size=28, color=TEXT)


def monitor():
    return RoundedRectangle(width=6.25, height=5.6, corner_radius=.22,
                            stroke_color=GRID, stroke_width=2.5,
                            fill_color=PANEL, fill_opacity=1).move_to(point(MID, .16))


def plot_grid(plot):
    return VGroup(
        *[Line(plot.pt(x, -1), plot.pt(x, 1), color=GRID, stroke_width=1.4)
          for x in np.linspace(.6, WINDOW - .6, 9)],
        *[Line(plot.pt(0, y), plot.pt(WINDOW, y), color=GRID, stroke_width=1.4)
          for y in (-.5, .5)],
        Line(plot.pt(0, 0), plot.pt(WINDOW, 0), color=GREY, stroke_width=1.5, stroke_opacity=.5),
    )


def signal(time, fn, limits, color=YELLOW, area=True):
    """A strip chart sampling a moving window of the same voltage function."""
    plot = Plot(box=(START, STOP, *limits), xr=(0, WINDOW), yr=(-1, 1), color=GRID, stroke=2)
    samples = np.linspace(0, WINDOW, 193)
    x = np.linspace(START, STOP, len(samples))
    center = (limits[0] + limits[1]) / 2
    height = (limits[1] - limits[0]) / 2
    curve = plot.curve(lambda offset: fn(time() + offset - WINDOW), color=color, width=4.5, n=len(samples))
    shade = VMobject(stroke_width=0, fill_color=color, fill_opacity=.16)
    cursor = Dot(radius=.075, color=color)
    ink = VGroup(shade, curve, cursor)

    def update(_, dt):
        y = center + height * np.clip(fn(time() + samples - WINDOW), -1, 1)
        pts = np.column_stack((x, y, np.zeros_like(x)))
        curve.set_points_as_corners(pts)
        cursor.move_to(pts[-1])
        if area:
            shade.set_points_as_corners(np.vstack((pts, point(STOP, center),
                                                    point(START, center), pts[0])))

    ink.add_updater(update, call_updater=True)
    return VGroup(plot.axes, plot_grid(plot)), ink


def flash_tile(time, x=-.42, y=.65, patterned=False):
    w, h = .50, 1.25
    lamp = RoundedRectangle(width=w, height=h, corner_radius=.10, stroke_width=2.5,
                            stroke_color=ORANGE, fill_color=ORANGE, fill_opacity=.30).move_to(point(x, y))
    stripes = VGroup(*[Rectangle(width=w * .82, height=h / 12, stroke_width=0,
                                 fill_color=BG, fill_opacity=.8).move_to(point(x, y + j * h / 5))
                       for j in (-2, -1, 0, 1, 2)]) if patterned else VGroup()
    rays = VGroup(*[Line(point(x - w / 2 - .11, y + d), point(x - w / 2 - .37, y - .15 + d / 2),
                         color=ORANGE, stroke_width=3) for d in (-.35, 0, .35)])
    g = VGroup(lamp, stripes, rays)

    def light(_, dt):
        glow = flash_glow(time())
        lamp.set_fill(ORANGE, .22 + .75 * glow)
        rays.set_stroke(opacity=.15 + .85 * glow)

    return g.add_updater(light, call_updater=True)


def clock_for(scene, start=0, offset=0):
    """Scene-relative time, shared by stimulus, cell activity, and plot."""
    return lambda: max(0, scene.elapsed() - start) + offset


FULL = (-1.92, 1.86)
UPPER = (1.14, 2.20)
MIDDLE = (-.60, .48)
LOWER = (-2.35, -1.27)
PAUSE_PHASE = 0.9


def flash_trace(scene, fn, label, clock, *, color=YELLOW):
    grid, ink = signal(clock, fn, FULL, color)
    pair = VGroup(grid, ink)
    scene.add(pair)
    title = left_text(label, START, 2.49, color, 34)
    return pair, title


class Retina(VGroup):
    """Three retinal layers and a pair of electrodes outside the tissue."""
    def __init__(self, separated=False, blocked=False):
        super().__init__()
        self.xs = (-5.31, -3.52, -1.71)
        self.ys = (1.02, -.05, -1.12)
        self.layers = VGroup()
        for x in self.xs:
            layer = RoundedRectangle(width=1.43, height=3.72, corner_radius=.25,
                                     stroke_color=GRID, stroke_width=2,
                                     fill_color=TISSUE, fill_opacity=1).move_to(point(x, -.05))
            self.layers.add(layer)
        self.cells = VGroup(*[VGroup(*[self.cell(i, x, y) for y in self.ys])
                              for i, x in enumerate(self.xs)])
        self.junctions = VGroup(*[
            VGroup(*[
                VGroup(Line(point(a + .56, y), point((a+b)/2 - .10, y), color=GREY, stroke_width=3),
                       Line(point((a+b)/2 + .10, y), point(b - .62, y), color=GREY, stroke_width=3))
                for y in self.ys
            ]) for a, b in zip(self.xs[:-1], self.xs[1:])
        ])
        self.electrodes = VGroup(electrode(-6.13, -.05, PI / 2),
                                 electrode(-.90, -.05, -PI / 2))
        self.blocks = VGroup(*[RoundedRectangle(width=.18, height=.48, corner_radius=.07,
                                               stroke_width=0, fill_color=RED, fill_opacity=1)
                               .move_to(point((self.xs[0] + self.xs[1]) / 2, y)) for y in self.ys])
        self.add(self.layers, self.cells, self.junctions)
        if separated:
            self.add(self.electrodes)
        if blocked:
            self.add(self.blocks)
            self.cells[1:].fade(.62)

    @staticmethod
    def cell(layer, x, y):
        body = Ellipse(width=.39, height=.27, stroke_color="#B3BDD0", stroke_width=2,
                       fill_color=CORTEX, fill_opacity=1).move_to(point(x, y))
        if layer == 0:
            outer = RoundedRectangle(width=.33, height=.30, corner_radius=.075,
                                     stroke_width=2, stroke_color=GREY,
                                     fill_color="#7D89A0", fill_opacity=1).move_to(point(x - .40, y))
            links = wire([(x - .26, y), (x + .22, y), (x + .50, y)], GREY)
            return VGroup(links, outer, body, Dot(point(x + .52, y), radius=.075, color=GREY))
        branches = VGroup(*[wire([(x - .59, y + d), (x - .38, y + d / 2), (x, y),
                                  (x + .55, y)], GREY) for d in (-.25, .25)])
        if layer == 2:
            body.scale(1.26)
        return VGroup(branches, body)

    def names(self):
        xs = (self.xs[0] - .19, *self.xs[1:])
        return VGroup(*[T(name, 28, TEXT, weight=BOLD, line_spacing=.8).move_to(point(x, -2.48))
                        for x, name in zip(xs, ("Photo-\nreceptors", "Bipolar\ncells", "Ganglion\ncells"))])

    def activity(self, time, kind="graded", downstream=lambda: 1):
        # Widen the on-cell flash for legibility without widening the voltage spikes in the plot.
        tracks = (receptor_signal, bipolar_signal, lambda t: ganglion_signal(t, sigma=.06))
        g = VGroup()
        for i, x in enumerate(self.xs):
            layer = VGroup()
            for j, y in enumerate(self.ys):
                orb = Ellipse(width=.87, height=.37, stroke_width=0,
                              fill_color=YELLOW, fill_opacity=.3).move_to(point(x, y))
                tick = wire([(x - .25, y - .10), (x - .05, y - .10), (x + .03, y + .25),
                             (x + .13, y - .19), (x + .29, y - .10)], YELLOW, 5)
                mark = tick if i == 2 else orb

                def glow(mob, dt, index=i, row=j, fn=tracks[i]):
                    t = time() - row * .11
                    level = min(1, abs(fn(t)) * (5 if index == 2 else 1.6))
                    if kind == "chain":
                        level = gaussian(phase(t), .31 + index * .53, .28)
                    mob.set_opacity((.04 + .9 * level) * (downstream() if index else 1))

                mark.add_updater(glow, call_updater=True)
                layer.add(mark)
            g.add(layer)
        return g


def eye_section():
    retina = path((-3.23, 2.1), [((-5.43, 1.85), (-6.10, -.77), (-4.11, -1.93)),
                                  ((-3.75, -2.11), (-3.25, -2.25), (-2.89, -2.15))],
                  "#AAB6D0", 17)
    globe = Ellipse(width=4.6, height=4.65, color=GREY, stroke_width=4,
                    fill_color=TISSUE, fill_opacity=1).move_to(point(-3.52, -.08))
    lens = Ellipse(width=.58, height=1.48, color="#AAB6D0", stroke_width=3.5,
                   fill_color=CORTEX, fill_opacity=1).move_to(point(-1.93, .13))
    pads = VGroup(electrode(-1.20, .11, -PI / 2), electrode(-3.50, -2.51, PI))
    return VGroup(globe, retina, lens, pads)


def prediction_mark():
    return T("?", 43, GOLD, weight=BOLD).move_to(point(5.99, -2.28))


def prediction_picture():
    retina = Retina(separated=True)
    grid, ink = signal(lambda: PAUSE_PHASE, retinal_sum, FULL)
    picture = VGroup(retina, retina.names(), retina.activity(lambda: PAUSE_PHASE),
                     monitor(), grid, ink, left_text("Transretinal ERG", START, 2.49, YELLOW, 34),
                     prediction_mark())
    picture.clear_updaters(recursive=True)
    return picture


class S01Hook(SpokenScene):
    def construct(self):
        head = Head()
        time = clock_for(self)
        self.add(head)
        question = caption("How can you read a working brain?", y=-3.16, size=36, color=GOLD)
        question.shift(LEFT * 1.85)
        self.at("How can you")
        self.play(FadeIn(question), run_time=.52)
        self.at("a working brain")
        glow = head.cortex_currents(time)
        self.add(glow)
        self.at("Rest electrodes", lead=.95)
        self.play(FadeOut(question), FadeIn(head.scalp, shift=UP * .24), run_time=.78)
        grid, trace = signal(time, eeg, FULL)
        self.add(monitor(), grid, trace)
        self.at("listen to many")
        self.play(FadeIn(scope()), run_time=.45)
        self.at("record summed electrical")
        self.play(FadeIn(left_text("Summed voltage", START, 2.49, YELLOW, 34)), run_time=.48)
        self.at("or the retina")
        halo = Ellipse(width=.91, height=.65, stroke_color=YELLOW, stroke_width=4).move_to(head.eye)
        self.play(FadeIn(halo), run_time=.4)
        self.play(FadeOut(halo), run_time=1.1)
        self.finish()


class S02Title(TitleCard):
    LESSON = "EEG, ERG and evoked potentials"
    TITLE = "Reading Brain and Retina from the Surface"

    def construct(self):
        head = Head()
        grid, trace = signal(clock_for(self, offset=15), eeg, FULL)
        world = VGroup(head, head.scalp, monitor(), grid, trace)
        dim = FullScreenRectangle(stroke_width=0, fill_color=BG, fill_opacity=.89)
        self.add(world)
        self.play(FadeIn(dim), run_time=.23)
        title = T(self.TITLE, 44, TEXT, font=TITLE_FONT)
        lesson = T(self.LESSON, 28, color=BLUE)
        rule = Line(LEFT, RIGHT, color=GOLD, stroke_width=4)
        card = VGroup(lesson, title, rule).arrange(DOWN, buff=.30)
        self.play(FadeIn(card), run_time=.32)
        self.wait(.76)
        self.play(FadeOut(card), run_time=.22)
        self.play(FadeOut(dim), run_time=.25)


class S03EegPolysom(SpokenScene):
    def construct(self):
        head = Head()
        time = clock_for(self, offset=16.8)
        grid, trace = signal(time, eeg, FULL)
        epoch_time = np.inf

        def recording_time():
            return min(epoch_time, time())

        tag = scope().move_to(point(-3.62, -3.24))
        self.add(head, head.scalp, head.cortex_currents(time), monitor(), grid, trace, tag)
        full = VGroup(grid, trace)
        name = left_text("EEG", START, 2.49, YELLOW, 34)
        self.at("or EEG")
        self.play(FadeIn(name), run_time=.42)
        self.at("score sleep stages")
        self.play(FadeIn(head.sleep), run_time=.55)
        self.at("adds two more", lead=.48)
        self.play(FadeIn(head.eye_pad, shift=RIGHT * .16), run_time=.52)
        self.play(FadeIn(head.chin_pad, shift=DOWN * .16), run_time=.52)
        self.at("surface traces")
        top_grid, top = signal(recording_time, eeg, UPPER)
        self.play(FadeOut(full), run_time=.28)
        self.add(top_grid, top)
        mid_grid, mid = signal(recording_time, eye_movement, MIDDLE)
        self.at("An electroocularogram", lead=.45)
        self.add(mid_grid, mid)
        self.at("tracks eye movements")
        self.play(FadeIn(left_text("Eye movement", START, .81, BLUE, 29)), run_time=.46)
        self.at("a chin electromyogram", lead=.4)
        low_grid, low = signal(recording_time, chin_tone, LOWER)
        self.add(low_grid, low)
        self.at("tracks muscle tone")
        self.play(FadeIn(left_text("Chin muscle", START, -.95, BLUE, 29)), run_time=.48)
        self.at("The night is cut")
        epoch_time = time()
        width = (STOP - START) / 3
        bands = VGroup(*[
            VGroup(*[
                Rectangle(width=width, height=hi - lo, stroke_color=BLUE, stroke_width=2,
                          fill_color=BLUE, fill_opacity=.075).move_to(
                    point(START + width * (i + .5), (lo + hi) / 2))
                for lo, hi in (UPPER, MIDDLE, LOWER)
            ])
            for i in range(3)
        ])
        self.play(LaggedStart(*[Create(band) for band in bands], lag_ratio=.38), run_time=1.08)
        self.at("30 -second epics")
        epoch = caption("30 s epochs", y=-2.98, color=BLUE)
        epoch.move_to(point(MID, -2.99))
        self.play(FadeIn(epoch), run_time=.42)
        self.at("gets one stage")
        stages = VGroup(*[T(stage, 28, TEXT, weight=BOLD).move_to(
            point(START + width * (i + .5), -2.98)) for i, stage in enumerate(("N2", "N3", "N3"))])
        self.play(FadeOut(epoch), run_time=.22)
        self.play(LaggedStart(*[FadeIn(stage) for stage in stages], lag_ratio=.35), run_time=.84)
        self.finish()


class S04GuidingVep(SpokenScene):
    def construct(self):
        head = Head()
        time = clock_for(self, offset=16.8)
        currents = head.cortex_currents(time)
        self.add(head, head.scalp, currents, monitor(), scope())
        pair, name = flash_trace(self, eeg, "EEG", time)
        self.add(name)
        self.at("revealing timing and state")
        rule = caption("Timing and state", size=34, color=GOLD)
        rule.move_to(point(-3.65, -3.17))
        self.play(FadeIn(rule), run_time=.5)
        self.at("Flash a pattern", lead=.55)
        self.play(FadeOut(rule), FadeOut(currents), FadeOut(pair), FadeOut(name), run_time=.38)
        visual = clock_for(self, self.elapsed())
        tile = flash_tile(visual, patterned=True)
        self.add(tile)
        focused = head.cortex_currents(visual, focus=True)
        self.add(focused)
        pair, name = flash_trace(self, evoked, "Visual evoked potential", visual)
        self.at("a visual evoked potential")
        self.play(FadeIn(name), run_time=.48)
        self.at("a wave locked")
        locked = caption("Locked to the flash", size=30, color=ORANGE)
        locked.move_to(point(-3.62, -3.17))
        self.play(FadeIn(locked), run_time=.45)
        self.at("Move the electrodes", lead=.45)
        self.play(FadeOut(tile), FadeOut(focused), FadeOut(head.scalp),
                  FadeOut(pair), FadeOut(name), FadeOut(locked), run_time=.38)
        eye = eye_section()
        self.play(FadeOut(head, scale=1.19, shift=LEFT * .40),
                  FadeIn(eye, scale=.39, shift=RIGHT * 1.26), run_time=1.25)
        retinal_clock = clock_for(self, self.elapsed(), offset=-.24)
        self.add(flash_tile(retinal_clock))
        _, erg = flash_trace(self, retinal_sum, "ERG", retinal_clock)
        self.at("or ERG")
        self.play(FadeIn(erg), run_time=.42)
        self.finish()


class S05PredictQ(SpokenScene):
    def construct(self):
        eye = eye_section()
        time = clock_for(self)
        self.add(eye, monitor(), scope())
        grid, trace = signal(time, retinal_sum, FULL)
        self.add(grid, trace)
        retina = Retina()
        names = retina.names()
        self.at("Inside the retina")
        self.play(FadeOut(eye, scale=1.14), FadeIn(retina.layers, scale=.60), run_time=.94)
        for phrase, i in (("photoreceptors drive", 0), ("bipolar cells", 1), ("drive ganglion cells", 2)):
            self.at(phrase, lead=.57)
            if i:
                self.play(FadeIn(retina.junctions[i - 1]), run_time=.18)
            self.play(FadeIn(retina.cells[i]), run_time=.34)
            self.play(FadeIn(names[i]), run_time=.35)
        self.at("and most bipolar")
        activity = retina.activity(time)
        self.add(activity[0], activity[1])
        graded = left_text("Graded potentials", -6.23, 2.47, YELLOW, 31)
        self.at("use graded potentials")
        self.play(FadeIn(graded), run_time=.50)
        self.at("while ganglion cells")
        self.add(activity[2])
        spikes = left_text("Ganglion cell spikes", -6.23, 2.47, YELLOW, 31)
        self.play(swap(graded, spikes), run_time=.68)
        self.at("A transretinal ERG", lead=.55)
        self.play(FadeOut(spikes), FadeIn(retina.electrodes), run_time=.55)
        self.play(FadeIn(left_text("Transretinal ERG", START, 2.49, YELLOW, 34)), run_time=.45)
        self.at("sums all those")
        self.play(Indicate(retina.electrodes, color=BLUE, scale_factor=1.04), run_time=1.17)
        self.at("To read only")
        self.play(FadeIn(question_card(QUESTION, **QUESTION_STYLE)),
                  FadeIn(prediction_mark(), shift=UP * .12), run_time=.58)
        self.at("what must you")
        # Ease the strip chart and cell activity to the exact frame the pause holds.
        stop = ValueTracker(time())
        activity.clear_updaters(recursive=True)
        trace.clear_updaters(recursive=True)
        _, still_trace = signal(stop.get_value, retinal_sum, FULL)
        still_activity = retina.activity(stop.get_value)
        self.remove(trace, *activity)
        self.add(still_trace, *still_activity)
        target = PAUSE_PHASE + 2.8 * np.ceil((stop.get_value() - PAUSE_PHASE) / 2.8)
        self.play(stop.animate.set_value(target), run_time=.95, rate_func=rush_from)
        self.finish()


class S06PredictPause(PredictPause):
    QUESTION = QUESTION
    CARD = QUESTION_STYLE
    SECONDS = 4.5

    def backdrop(self):
        return VGroup(prediction_picture(), scope())

    def construct(self):
        self.add(self.backdrop(), question_card(self.QUESTION, **self.CARD))
        track = Line(point(-6.25, -3.19), point(4.05, -3.19), color=GRID, stroke_width=7)
        fill = track.copy().set_stroke(GOLD, 7)
        self.add(track)
        self.play(Create(fill), run_time=self.SECONDS, rate_func=linear)


class S07PredictAnswer(SpokenScene):
    def construct(self):
        retina = Retina(separated=True)
        time = clock_for(self, offset=PAUSE_PHASE)
        level = ValueTracker(1)
        grid, trace = signal(time, lambda t: receptor_signal(t) + level.get_value() * (
            bipolar_signal(t) + ganglion_signal(t)), FULL)
        q = question_card(QUESTION, **QUESTION_STYLE)
        name = left_text("Transretinal ERG", START, 2.49, YELLOW, 34)
        activity = retina.activity(time, downstream=level.get_value)
        mark = prediction_mark()
        self.add(retina, retina.names(), activity, monitor(), grid, trace, name, scope(), q, mark)
        self.at("You block downstream")
        self.play(FadeOut(q), FadeOut(mark), GrowFromCenter(retina.blocks), run_time=.68)
        blocked = left_text("Synaptic responses blocked", -6.24, 2.50, RED, 32)
        self.at("synaptic responses")
        self.play(FadeIn(blocked), level.animate.set_value(0),
                  retina.cells[1:].animate.fade(.62), run_time=1.16)
        self.at("get light signals")
        self.play(Indicate(retina.blocks, color=RED, scale_factor=1.09), run_time=1.4)
        self.at("So once they fall")
        self.play(Indicate(retina.electrodes, color=BLUE, scale_factor=1.02), run_time=1.2)
        self.at("voltage across the retina")
        answer = left_text("Photoreceptors only", START, 2.49, GREEN, 34)
        self.play(swap(name, answer), run_time=.65)
        self.finish()


def cards_for_looking():
    def card(y, stripes):
        board = RoundedRectangle(width=.79, height=1.05, corner_radius=.10,
                                 stroke_color=GREY, stroke_width=2,
                                 fill_color="#8C96AB", fill_opacity=1).move_to(point(-.44, y))
        if not stripes:
            return board
        pattern = VGroup(*[Rectangle(width=.70, height=.071, stroke_width=0,
                                     fill_color=BG, fill_opacity=1).move_to(point(-.44, y + i * .16))
                           for i in range(-2, 3)])
        return VGroup(board, pattern)
    return card(1.29, True), card(-.11, False)


def comparison_bars():
    grid = Line(point(START, -1.99), point(STOP, -1.99), color=GREY, stroke_width=2)
    bars, labels = VGroup(), VGroup()
    # Ordinal heights show only the sign of the difference reported in the lesson.
    for x, h, color, name in [(2.37, 1.18, BLUE, "Looking test"), (4.87, 2.05, YELLOW, "Scalp VEP")]:
        bar = RoundedRectangle(width=1.79, height=h, corner_radius=.10,
                               stroke_color=color, stroke_width=2.4,
                               fill_color=color, fill_opacity=.40).move_to(point(x, -1.99 + h/2))
        bars.add(bar)
        labels.add(T(name, 28, color, weight=BOLD).move_to(point(x, -2.31)))
    sharp = T("Sharper at same age", 28, YELLOW).move_to(point(4.13, .40))
    return grid, bars, labels, sharp


class S08MethodLimit(SpokenScene):
    def construct(self):
        retina = Retina(separated=True, blocked=True)
        names = retina.names()
        activity = retina.activity(clock_for(self), downstream=lambda: 0)
        head = Head()
        time = clock_for(self)
        grid, ink = signal(time, receptor_signal, FULL)
        prev_name = left_text("Photoreceptors only", START, 2.49, GREEN, 34)
        blocked = left_text("Synaptic responses blocked", -6.24, 2.50, RED, 32)
        screen = monitor()
        self.add(retina, names, activity, screen, grid, ink, prev_name, blocked, scope())
        self.at("numbers also depend")
        self.play(FadeOut(VGroup(names, blocked, prev_name)), run_time=.28)
        self.play(FadeOut(VGroup(retina, activity), scale=.66, shift=RIGHT * 1.48),
                  FadeOut(VGroup(screen, grid, ink)), FadeIn(head, scale=1.15, shift=LEFT * .40), run_time=1.09)
        striped, plain = cards_for_looking()
        self.at("Looking tests watch", lead=.75)
        self.play(FadeIn(plain), run_time=.32)
        self.play(FadeIn(striped), run_time=.35)
        axis, bars, labels, sharp = comparison_bars()
        self.at("baby gazes")
        gaze = DashedLine(point(-1.39, .50), point(-.90, 1.28),
                          color=BLUE, stroke_width=3, dash_length=.09)
        self.play(head.pupil.animate.shift(UP * .14), Create(gaze), run_time=.69)
        self.at("the finest stripes")
        self.play(FadeIn(screen), FadeIn(axis), GrowFromEdge(bars[0], DOWN), run_time=.72)
        self.play(FadeIn(labels[0]), run_time=.38)
        self.at("At the same age")
        self.play(FadeOut(plain), FadeOut(gaze), FadeIn(head.scalp, shift=UP * .18), run_time=.60)
        vep_time = clock_for(self, self.elapsed())
        self.add(head.cortex_currents(vep_time, focus=True))
        chart_grid, chart_ink = signal(vep_time, evoked, (.77, 1.88), area=False)
        chart = left_text("Visual evoked potential", START, 2.49, YELLOW, 32)
        self.add(chart_grid, chart_ink)
        self.at("scalp visual -evoked")
        self.play(FadeIn(chart), run_time=.42)
        self.at("report sharper vision", lead=.55)
        self.play(GrowFromEdge(bars[1], DOWN), run_time=.85)
        self.play(FadeIn(labels[1]), run_time=.36)
        self.play(FadeIn(sharp), run_time=.44)
        self.finish()


def process_s_dial(level):
    gauge = dial(level, center=point(3.62, .10), radius=1.72, color=SLEEP_PRESSURE)
    gauge.remove(gauge[2], gauge[3])
    label = left_text("Process S", START, 2.49, SLEEP_PRESSURE, 34)
    return VGroup(gauge, label)


def waking_bars():
    labels = VGroup()
    bars = VGroup()
    for y, length, title in [(1.30, .64, "Shorter waking"), (-.47, 1.22, "Longer waking")]:
        bars.add(Line(point(4.83, y), point(4.83 + length, y), color=SLEEP_PRESSURE, stroke_width=9))
        labels.add(left_text(title, START, y, SLEEP_PRESSURE, 28))
    return bars, labels


class S09CorrelationLimit(SpokenScene):
    def construct(self):
        head = Head()
        time = clock_for(self)
        patterned = flash_tile(time, patterned=True)
        self.add(head, head.scalp, scope(), patterned, monitor())
        current = head.cortex_currents(time, focus=True)
        self.add(current)
        pair, name = flash_trace(self, evoked, "Visual evoked potential", time)
        self.add(name)
        self.at("activity goes with")
        link = boxed_label("Goes with  ≠  used by brain", color=TEXT, size=30,
                           fill_opacity=.06).move_to(point(-3.66, -3.28))
        self.play(FadeIn(link), run_time=.55)
        self.at("Take sleep pressure")
        self.play(FadeOut(VGroup(patterned, current, pair, name, link)), run_time=.44)
        level = ValueTracker(.23)
        gauge = process_s_dial(level)
        waking = T("Awake", 32, SLEEP_PRESSURE).move_to(point(MID, -.84))
        sleep = T("Asleep", 32, SLEEP_PRESSURE).move_to(waking)
        self.play(FadeIn(gauge), run_time=.65)
        self.at("which builds while", lead=.6)
        self.play(FadeIn(waking), level.animate.set_value(.87), run_time=1.48,
                  rate_func=lambda t: (1 - np.exp(-2 * t)) / (1 - np.exp(-2)))
        self.at("and drains in sleep")
        self.play(swap(waking, sleep, run_time=.52), FadeIn(head.sleep),
                  level.animate.set_value(.46), run_time=1.72,
                  rate_func=lambda t: (1 - np.exp(-2 * t)) / (1 - np.exp(-2)))
        self.at("Deep sleep slow waves")
        self.play(FadeOut(VGroup(gauge, sleep)), run_time=.44)
        upper_grid, upper = signal(time, lambda t: .48 * slow_eeg(t), (-.05, 1.01))
        lower_grid, lower = signal(time, slow_eeg, (-1.85, -.78))
        label = left_text("EEG at sleep onset", START, 2.49, YELLOW, 34)
        self.add(upper_grid, upper)
        self.play(FadeIn(label), run_time=.38)
        bars, labels = waking_bars()
        self.play(FadeIn(labels[0]), Create(bars[0]), run_time=.63)
        self.at("larger after longer", lead=.55)
        self.add(lower_grid, lower)
        self.play(FadeIn(labels[1]), Create(bars[1]), run_time=.85)
        self.at("are a marker")
        marker = caption("EEG is a marker, not Process S itself", size=31, color=GOLD)
        marker.move_to(point(-1.0, -3.22))
        self.play(FadeIn(marker), run_time=.56)
        self.finish()


def rod_adaptation(t, light_on, mutant=False):
    """Normalized flash responses from an illustrative gain model.

    A brighter background reduces gain at a fixed flash strength. Separate
    residual gains illustrate the persistence seen by Vinberg et al. (2015,
    PMID 26415569). The ordinate and horizontal scale are schematic.
    """
    u = phase(t, 2.8)
    elapsed = np.maximum(0, t - light_on)
    strength = .54 if mutant else .70
    gain = 1 - strength * (1 - np.exp(-elapsed / 1.55))
    decay = 1.17 if mutant else .67
    return -(.76 if mutant else 1.28) * gain * (1 - np.exp(-u / .10)) * np.exp(-u / decay)


class S10UnlockedErg(SpokenScene):
    def construct(self):
        head = Head()
        self.add(head, head.scalp, head.sleep, monitor(), scope())
        grid, ink = signal(clock_for(self), slow_eeg, FULL)
        old = VGroup(grid, ink, left_text("EEG at sleep onset", START, 2.49, YELLOW, 34))
        self.add(old)
        self.at("Within those limits")
        retina = Retina(separated=True, blocked=True)
        self.play(FadeOut(VGroup(head, head.scalp, head.sleep), scale=1.16, shift=LEFT * .35),
                  FadeIn(retina, scale=.46, shift=RIGHT * 1.36), run_time=1.40)
        self.play(FadeOut(old), run_time=.35)
        time = clock_for(self)
        light_on = np.inf
        rod_limits = (-2.03, .74)
        rod_grid, normal_ink = signal(time, lambda t: rod_adaptation(t, light_on), rod_limits)
        self.add(retina.activity(time, downstream=lambda: 0), rod_grid, normal_ink)
        self.at("In 2015")
        citation = left_text("Vinberg and colleagues, 2015", -6.24, 2.52, GOLD, 31)
        self.play(FadeIn(citation), run_time=.58)
        self.at("that blocked ERG")
        erg = left_text("Blocked transretinal ERG", START, 2.49, YELLOW, 34)
        self.play(FadeIn(erg), run_time=.53)
        self.at("on mouse retinas")
        degrees = boxed_label("37 °C", BLUE, size=30).move_to(point(-2.77, -2.44))
        self.play(FadeIn(left_text("Mouse retina", -6.24, -2.60, TEXT, 30)), run_time=.36)
        self.at("37 degrees", lead=.10)
        self.play(FadeIn(degrees), run_time=.43)
        self.at("In light adaptation")
        light = Rectangle(width=.22, height=1.12, stroke_width=0, fill_color=ORANGE,
                          fill_opacity=.8).move_to(point(-6.55, 1.23))
        beam = Polygon(light.get_corner(UR), point(-5.58, 1.34), point(-5.58, .65),
                       light.get_corner(DR), stroke_width=0, fill_color=ORANGE, fill_opacity=.17)
        light_on = time()
        self.play(FadeIn(light), FadeIn(beam), run_time=.42)
        light_name = left_text("Steady background light", -6.24, 3.16, ORANGE, 30)
        self.play(FadeIn(light_name), run_time=.45)
        self.at("partly through calcium")
        self.play(swap(erg, left_text("Light adaptation", START, 2.49, YELLOW, 34)), run_time=.66)
        self.at("Rods lacked the two")
        normal = left_text("Normal rods", START, 1.82, YELLOW, 29)
        self.play(FadeIn(normal), run_time=.48)
        gcap = boxed_label("No GCAP1 + GCAP2", color=RED, size=28).move_to(point(-6.24, -3.30), aligned_edge=LEFT)
        self.at("GCAP proteins")
        self.play(FadeIn(gcap), run_time=.46)
        rec = boxed_label("No recoverin", color=RED, size=28).next_to(gcap, RIGHT, buff=.26)
        self.at("recoverin")
        self.play(FadeIn(rec), run_time=.47)
        self.at("all three calcium")
        diagram_name = left_text("All three sensors absent", START, 1.25, GREEN, 29)
        # Put the shared light onset back in the comparison window so the viewer
        # can see both response trains shrink after the background comes on.
        compare_time = clock_for(self, self.elapsed(), offset=light_on + 2.50)
        _, normal_comparison = signal(compare_time, lambda t: rod_adaptation(t, light_on), rod_limits)
        _, mutant_ink = signal(compare_time, lambda t: rod_adaptation(t, light_on, mutant=True),
                               rod_limits, GREEN, area=False)
        self.remove(normal_ink)
        self.add(normal_comparison)
        self.play(FadeIn(diagram_name), FadeIn(mutant_ink), run_time=.49)
        still = T("Adaptation persists", 31, GREEN, weight=BOLD).move_to(point(MID, -2.94))
        self.at("still persisted")
        self.play(FadeIn(still), run_time=.54)
        self.finish()


def fluid_path():
    return path((-5.46, -.52), [
        ((-5.93, -.23), (-6.09, 1.04), (-5.42, 1.77)),
        ((-4.52, 2.77), (-3.43, 2.66), (-2.56, 2.19)),
        ((-1.98, 1.86), (-1.81, 1.56), (-1.77, 1.10)),
    ], TEAL, 3)


def fluid_pulse(time, route):
    wave = VGroup(*[Dot(radius=.095 - i * .011, color=TEAL) for i in range(6)])

    def move(_, dt):
        u = float(phase(time(), 3.35))
        for i, dot in enumerate(wave):
            fraction = (u - 1.65 - i * .060) / 1.57
            dot.move_to(route.point_from_proportion(np.clip(fraction, 0, 1)))
            dot.set_opacity(.96 * np.sin(PI * np.clip(fraction, 0, 1)) ** .42)

    return wave.add_updater(move, call_updater=True)


class S11UnlockedEegClose(SpokenScene):
    def construct(self):
        head = Head()
        retina = Retina(separated=True, blocked=True)
        self.add(retina, monitor(), scope())
        self.at("In 2019")
        self.play(FadeOut(retina, scale=.68, shift=RIGHT * 1.48),
                  FadeIn(VGroup(head, head.scalp, head.sleep), scale=1.15, shift=LEFT * .35), run_time=1.35)
        time = clock_for(self, self.elapsed(), offset=.2)
        grid, wave = signal(time, slow_eeg, UPPER)
        self.add(grid, wave)
        self.at("and colleagues", lead=.38)
        study = left_text("Fultz and colleagues, 2019", -6.24, -3.09, GOLD, 30)
        self.play(FadeIn(study), run_time=.47)
        self.at("tracked slow EEG")
        self.play(FadeIn(left_text("Slow EEG waves", START, 2.49, YELLOW, 33)), run_time=.49)
        self.at("13 sleeping people")
        people = left_text("13 sleeping people", START, -2.18, TEXT, 30)
        self.play(FadeIn(people), run_time=.43)
        self.at("were followed by")
        route = fluid_path()
        self.add(route, fluid_pulse(time, route))
        grid_csf, csf = signal(time, csf_flow, (-1.78, .23), TEAL)
        self.add(grid_csf, csf)
        self.at("cerebrospinal fluid")
        fluid = left_text("Cerebrospinal fluid flow", START, .70, TEAL, 30)
        self.play(FadeIn(fluid), run_time=.47)
        self.at("That is a correlation")
        self.play(FadeOut(study), FadeOut(people), run_time=.45)
        hedge = boxed_label("Correlation", RED, size=32, fill_opacity=.08).move_to(point(-3.65, -3.16))
        self.play(FadeIn(hedge), run_time=.49)
        self.at("studies disagree whether")
        debated = boxed_label("Correlation  •  clearance debated", RED, size=30,
                               fill_opacity=.08).move_to(point(-3.24, -3.16))
        self.play(swap(hedge, debated), run_time=.71)
        self.at("Surface waves map")
        final = caption("Surface waves reveal timing and state", size=33, color=GOLD)
        final.move_to(point(-2.88, -3.18))
        self.play(swap(debated, final), run_time=.73)
        self.finish()


class S12End(EndCard):
    LINE = "Surface electrodes sum many cells, revealing timing and state, not cause."
