"""Hearing Hundreds of Neurons at Once, synchronized to audio/words.json.

Color map (from the patch-clamp reference): blue for recording hardware, grey
for tissue and structure, yellow for recorded activity, purple for sorted
units, orange for an odour stimulus, green for checks, red for pitfalls and
gold for dates and the rule. All teaching traces are computed schematics.
"""
from bp_parts import *
from bp_style import EndCard

PURPLE = "#B58CD9"
ORANGE = "#F29E4C"
TISSUE = "#243743"
SCREEN = "#1C2E40"
LANE = "#2A4053"
CX, RX = -3.25, 3.25
ROWS = (1.32, 0.02, -1.32)
QUESTION = "300 units from three mice — how many samples?"
QUESTION_LAYOUT = {"y": 3.16, "size": 36, "max_w": 11.4}


def point(x, y):
    return np.array([x, y, 0.0])


def panel(left="Neural tissue", right="Recorded activity"):
    backdrop = TwoPanel(left, right, colors=(GREY, YELLOW), top=3.02, bottom=-2.65)
    backdrop.left_frame.set_stroke(GREY, opacity=0.48)
    backdrop.right_frame.set_stroke(BLUE, opacity=0.42).set_fill(SCREEN, opacity=1)
    return backdrop


def schematic():
    return scope_tag(size=28, color=TEXT).shift(UP * 0.07)


def outline(cx, cy, rx, ry, phase=0):
    angles = np.linspace(0, TAU, 100, endpoint=False)
    shape = VMobject(stroke_color=GREY, stroke_width=2.6, fill_color=TISSUE, fill_opacity=1)
    ripple = 1 + 0.042 * np.sin(5 * angles + phase) + 0.027 * np.cos(9 * angles)
    shape.set_points_smoothly([
        point(cx + rx * r * np.cos(a), cy + ry * r * np.sin(a)) for a, r in zip(angles, ripple)
    ] + [point(cx + rx * ripple[0], cy)])
    return shape


def neuron(x, y, radius, rng):
    rays = VGroup()
    for a in np.linspace(0, TAU, 5, endpoint=False) + rng.uniform(0, TAU):
        start = point(x + radius * np.cos(a), y + radius * np.sin(a))
        end = point(x + radius * 2.1 * np.cos(a), y + radius * 2.1 * np.sin(a))
        rays.add(Line(start, end, color=GREY, stroke_width=1.5, stroke_opacity=0.52))
    return VGroup(rays, Dot(point(x, y), radius=radius, color=GREY, fill_opacity=0.54))


def neural_field(brain=False):
    """The same tissue and same sample cells anchor the hook, hardware and odour scenes."""
    rng = np.random.default_rng(38)
    body = outline(CX, -0.19, 2.73, 2.15, phase=1.4)
    cells = VGroup()
    for row in range(8):
        for col in range(9):
            x = CX + (col - 4) * 0.56 + rng.uniform(-0.14, 0.14)
            y = -0.18 + (row - 3.5) * 0.52 + rng.uniform(-0.12, 0.12)
            if ((x - CX) / 2.49) ** 2 + ((y + 0.18) / 1.93) ** 2 < 1 and np.hypot(x - CX, y - 0.3) > 0.36:
                cells.add(neuron(x, y, rng.uniform(0.053, 0.084), rng))
    for x, y in ((CX, 0.30), (CX + 1.26, -0.64), (CX - 1.06, -0.92)):
        cells.add(neuron(x, y, 0.115, rng))
    folds = VGroup()
    if brain:
        for x, y, dx in ((-4.82, 0.77, 0.65), (-3.22, 0.87, 0.85), (-2.02, 0.65, 0.75),
                         (-4.78, -0.50, 0.68), (-2.97, -0.58, 0.85), (-2.10, -1.3, 0.70)):
            folds.add(ArcBetweenPoints(point(x, y), point(x + dx, y - 0.27), angle=-1.15,
                                      stroke_color=GREY, stroke_opacity=0.62, stroke_width=3))
    return VGroup(body, folds, cells), cells


def refresh_cells(cells, activity):
    """Draw only the changing activity. The grey anatomy stays fixed."""
    t = 0.0
    positions = [cell[1].get_center() for cell in cells]
    halos = VGroup(*[Dot(p, radius=0.16 if i < len(cells) - 3 else 0.34, color=YELLOW)
                     for i, p in enumerate(positions)])

    def refresh(group, dt):
        nonlocal t
        t += dt
        for i, (halo, p) in enumerate(zip(group, positions)):
            halo.set_fill(opacity=float(np.clip(activity(i, p, t), 0, 0.92)))

    refresh(halos, 0)
    return halos.add_updater(refresh)


def spike(t, center, width=0.027):
    """Biphasic illustrative voltage transient, using two displaced Gaussians."""
    d = (t - center) / width
    return -0.96 * np.exp(-d ** 2) + 0.40 * np.exp(-((d - 1.5) / 1.18) ** 2)


def spikes(t, centers, width=0.027):
    return sum(spike(t, c, width) for c in centers)


def network(t, richness):
    """Illustrative bursts plus linked oscillatory components as richness increases."""
    early = 0.76 * spikes(t, (0.84, 3.22, 4.24, 6.70), 0.042)
    burst = (0.52 + 0.36 * np.cos(2 * PI * (t / 3.25 - 0.25))) ** 2
    late = burst * (0.65 * np.sin(2 * PI * t * 0.76) + 0.24 * np.sin(2 * PI * t * 1.8))
    late += 0.12 * np.sin(2 * PI * t * 0.29)
    return (1 - richness) * early + richness * late


def traces(rows=3, x0=0.68, x1=5.80, y0=-2.04, y1=1.94, sources=None, richness=None, inset=False):
    """Plot calculated traces and move one acquisition cursor through the same time window."""
    plot = Plot((x0, x1, y0, y1), (0, 8), (-1, 1), color=GREY, stroke=1.65)
    if inset:
        plot.axes.set_opacity(0.55)
    if sources is None:
        sources = ((0.68, 2.24, 4.02, 6.0, 6.75), (1.2, 2.27, 3.12, 4.05, 7.38),
                   (0.97, 3.16, 4.07, 5.36, 5.58, 7.4)) if rows > 1 else ((1.2, 3.75, 6.55),)
    size = 1.62 / rows
    amplitude = size * (0.52 if inset else 0.91)
    curves, signals = VGroup(), []
    for i, events in enumerate(sources):
        level = 0.81 - (i + 0.5) * size

        def signal(t, level=level, events=events):
            value = spikes(t, events) if richness is None else network(t, richness.get_value())
            return level + amplitude * value

        signals.append(signal)
        curve = plot.curve(signal, color=YELLOW, width=3.1, n=360)
        if richness is not None:
            def redraw(mob, dt, signal=signal):
                mob.set_points_as_corners(plot._pts(signal, 0, 8, 270))
            curve.add_updater(redraw)
        curves.add(curve)

    for curve in curves:
        curve.set_z_index(2)
    cursor = Line(plot.pt(0, -1), plot.pt(0, 1), stroke_color=YELLOW, stroke_width=2.2,
                  stroke_opacity=0.67)
    highlight = Rectangle(width=1, height=y1 - y0, stroke_width=0, fill_color=YELLOW, fill_opacity=0.23)
    heads = VGroup(*[Dot(radius=0.085, color=YELLOW).set_z_index(3) for _ in signals])
    live = VGroup(highlight, cursor, heads)
    read = 0.0

    def scan(mob, dt):
        nonlocal read
        read = (read + 1.85 * dt) % 8
        right = plot.pt(read, 0)[0]
        left = plot.pt(max(0, read - 1.35), 0)[0]
        highlight.stretch_to_fit_width(max(right - left, 0.001)).move_to(point((right + left) / 2, (y0 + y1) / 2))
        cursor.put_start_and_end_on(plot.pt(read, -1), plot.pt(read, 1))
        for head, signal in zip(heads, signals):
            head.move_to(plot.pt(read, signal(read)))

    scan(live, 0)
    return VGroup(plot, curves, live.add_updater(scan))


def single_electrode():
    p = point(CX, 0.31)
    return Polygon(p, p + point(-0.86, 1.35), p + point(-0.55, 1.54),
                   color=BLUE, stroke_width=2.4, fill_color=BLUE, fill_opacity=0.65)


def packed_dots(positions, radius, color, opacity=1):
    """Combine marks in a single path so large site and unit counts render efficiently."""
    marks = VMobject(stroke_width=0, fill_color=color, fill_opacity=opacity)
    disc = Dot(radius=radius).get_points()
    marks.set_points(np.concatenate([disc + p for p in positions]))
    return marks


def flat_array():
    base = Polygon(point(-5.94, -2.19), point(-1.17, -2.19), point(-0.62, -1.49), point(-5.40, -1.49),
                   color=BLUE, stroke_width=2.4, fill_color=BLUE, fill_opacity=0.19)
    sites = packed_dots([point(-5.51 + 0.42 * c + 0.12 * r, -2.04 + 0.14 * r)
                         for r in range(4) for c in range(10)], 0.038, BLUE)
    return VGroup(base, sites)


def shank():
    x = -3.68
    body = Polygon(point(x - 0.35, 1.86), point(x + 0.35, 1.86),
                   point(x + 0.35, -1.76), point(x, -2.06), point(x - 0.35, -1.76),
                   color=BLUE, stroke_width=2.5, fill_color="#22566D", fill_opacity=1)
    cap = RoundedRectangle(width=0.94, height=0.28, corner_radius=0.06, stroke_width=2,
                           stroke_color=BLUE, fill_color=BLUE, fill_opacity=0.55).move_to(point(x, 1.87))
    # A dense, enlarged face marks all 960 sites. The drawing is not dimensionally scaled.
    sites = packed_dots([point(x + (col - 1.5) * 0.15, -1.72 + (row + 0.5 * (col % 2)) * 0.01445)
                         for col in range(4) for row in range(240)], 0.0058, BLUE)
    return VGroup(body, cap, sites)


def inserted_probe():
    return shank().shift(DOWN * 0.28)


def retina():
    tissue = outline(CX, -0.83, 2.48, 1.02)
    cells = VGroup()
    for row in range(5):
        dy = (row - 2) * 0.265
        # Leave a margin for the glow inside the rippled outline, including at the row ends.
        half_width = 2.16 * np.sqrt(1 - (dy / 0.82) ** 2)
        for col, dx in enumerate(np.linspace(-half_width, half_width, 20)):
            x = CX + dx + 0.032 * np.sin(2 * row + col)
            cells.add(Dot(point(x, -0.83 + dy), radius=0.044, color=GREY))
    return VGroup(tissue, cells)


def wave_strength(x, t, start=-5.7, width=1.03, speed=1.05, period=6.3):
    front = start + (speed * t) % period
    return np.exp(-((x - front) / width) ** 2) * (0.65 + 0.28 * np.cos(9 * t - x))


def chain(indices, y=-3.05):
    names = ("Sites", "Channels", "Units", "Neurons", "Animals")
    colors = (BLUE, YELLOW, PURPLE, GREY, GREEN)
    xs = (-5.48, -3.39, -0.86, 1.15, 3.57)
    labels = {i: boxed_label(names[i], colors[i], size=30, min_size=28, pad=0.16).move_to(point(xs[i], y))
              for i in indices}
    arrows = {}
    for i, j in zip(indices, indices[1:]):
        arrows[j] = Arrow(labels[i].get_right() + RIGHT * 0.08, labels[j].get_left() + LEFT * 0.08,
                          buff=0, stroke_width=3, tip_length=0.13, color=GREY)
    return labels, arrows


class S01Hook(SpokenScene):
    def construct(self):
        stage = panel()
        field, cells = neural_field()
        trace = traces(1)
        electrode = single_electrode()
        self.add(stage.left_frame, stage.right_frame, field, schematic())
        self.at("how do you listen")
        single = refresh_cells(cells, lambda i, p, t: (0.58 + 0.34 * np.sin(5 * t) ** 4)
                               if i == len(cells) - 3 else 0)
        self.play(FadeIn(electrode), FadeIn(single), Create(trace[0]), run_time=1.15)
        self.at("neurons firing at once")
        self.play(Create(trace[1]), run_time=1.8)
        self.add(trace[2])
        self.at("one electrode in")
        self.play(FadeIn(stage.left_head), FadeIn(stage.right_head), run_time=0.6)
        mode = ValueTracker(0)
        self.at("yet waves")
        population = refresh_cells(cells, lambda i, p, t: (
            wave_strength(p[0], t) if mode.get_value() < 0.5 else
            0.73 * (0.5 + 0.5 * np.sin(5.5 * t)) ** 2 if mode.get_value() < 1.5 else
            0.79 * (0.5 + 0.5 * np.sin(2.4 * t + i * 2.4)) ** 5
        ))
        self.play(FadeOut(single), FadeIn(population), run_time=0.55)
        self.at("oscillations and")
        mode.set_value(1)
        self.at("odor patterns")
        mode.set_value(2)
        self.finish()


class S02Title(TitleCard):
    LESSON = "Multielectrode arrays and high-density recording"
    TITLE = "Hearing Hundreds of Neurons at Once"

    def construct(self):
        field, cells = neural_field()
        field.move_to(ORIGIN).set_opacity(0.22)
        title = T(self.TITLE, 50, font=TITLE_FONT)
        fit(title, max_w=11.6)
        lesson = T(self.LESSON, 29, color=TEXT)
        rule = Line(LEFT * 0.74, RIGHT * 0.74, color=GOLD, stroke_width=3)
        words = VGroup(title, lesson, rule).arrange(DOWN, buff=0.29).move_to(point(0, 0.35))
        glow = refresh_cells(cells, lambda i, p, t: 0.22 * wave_strength(p[0], t, start=-2.4))
        self.add(field, glow)
        self.play(FadeIn(words), run_time=0.45)
        self.wait(1.07)
        self.play(FadeOut(words), run_time=0.4)


class S03Hardware(SpokenScene):
    def construct(self):
        stage = panel("Recording hardware", "Recorded activity")
        field, _ = neural_field()
        electrode = single_electrode()
        array, sheet = flat_array(), retina()[0]
        probe = shank()
        trace = traces(1)
        self.add(stage.left_frame, stage.left_head, stage.right_frame, stage.right_head, field, electrode, trace, schematic())
        self.at("instead of one")
        self.play(electrode.animate.set_color(BLUE), run_time=0.65)
        self.at("tissue rests on")
        self.play(ReplacementTransform(electrode, array), ReplacementTransform(field, sheet),
                  FadeOut(trace), FadeOut(stage.right_head), run_time=1.42)
        self.at("holds a probe")
        self.play(FadeOut(sheet), ReplacementTransform(array, probe), run_time=1.02)
        self.at("the original")
        name = T("Neuropixels (2017)", 34, BLUE).move_to(point(RX, 2.25))
        self.play(FadeIn(name), run_time=0.55)
        inset_sites = VGroup(*[VGroup(*[
            Dot(point(2.25 + 0.66 * c + 0.08 * (r % 2), 1.48 - 0.25 * r), radius=0.079, color=BLUE)
            for c in range(4)
        ]) for r in range(8)])
        inset = RoundedRectangle(width=3.52, height=2.28, corner_radius=0.13, stroke_color=BLUE,
                                 stroke_width=2.3, fill_color="#22566D", fill_opacity=1).move_to(point(RX, 0.59))
        self.play(GrowFromPoint(inset, point(0.55, 0.54)), run_time=2.10)
        self.at("carries 960")
        self.play(LaggedStart(*(FadeIn(row, shift=DOWN * 0.16) for row in inset_sites), lag_ratio=0.53),
                  run_time=1.37)
        self.at("recording sites")
        count = T("960 recording sites", 35, BLUE).move_to(point(RX, -1.12))
        scan = RoundedRectangle(width=3.15, height=0.52, corner_radius=0.10,
                                stroke_width=1.7, stroke_color=BLUE, fill_color=BLUE,
                                fill_opacity=0.51).move_to(point(RX, 1.36))
        self.play(FadeIn(count), FadeIn(scan), run_time=0.52)
        self.play(scan.animate.shift(DOWN * 1.54), run_time=1.65, rate_func=linear)
        self.play(FadeOut(scan), run_time=0.38)
        self.at("along one shank")
        bracket = BraceBetweenPoints(point(-3.55, 1.87), point(-3.55, -2.06), direction=LEFT, color=BLUE)
        length = T("About\n10 mm", 32, BLUE).next_to(bracket, LEFT, buff=0.20)
        self.play(probe.animate.shift(RIGHT * 0.68), GrowFromCenter(bracket), run_time=0.80)
        self.at("about 10 millimeters")
        self.play(FadeIn(length), run_time=0.68)
        self.at("push it into")
        brain, active_cells = neural_field(brain=True)
        self.bring_to_back(brain)
        brain.set_z_index(1)
        stage.left_head.set_z_index(2)
        probe.set_z_index(3)
        self.remove(brain)
        self.play(FadeOut(bracket), FadeOut(length), run_time=0.30)
        self.play(FadeIn(brain), FadeOut(VGroup(name, count, inset, inset_sites)),
                  probe.animate.shift(LEFT * 0.68 + DOWN * 0.28), run_time=1.35)
        self.at("you hear spikes")
        read = traces()
        self.play(Create(read[0]), Create(read[1]), FadeIn(stage.right_head), run_time=1.25)
        live = refresh_cells(active_cells, lambda i, p, t: 0.64 * (0.5 + 0.5 * np.sin(t * 3 + i * 2.2)) ** 6)
        live.set_z_index(2)
        self.add(read[2], live)
        self.finish()


def odour_cloud(color):
    cloud = VGroup(*[Circle(radius=r, stroke_width=1.2, stroke_color=color, stroke_opacity=0.78,
                            fill_color=color, fill_opacity=0.39).move_to(point(x, y))
                     for x, y, r in ((0.0, 0.13, 0.51), (-0.34, -0.08, 0.32), (0.42, -0.05, 0.35),
                                     (0.12, -0.28, 0.28), (-0.14, 0.37, 0.24))])
    return cloud.move_to(point(-5.54, 1.00))


def response_list():
    bars, track, text = [], VGroup(), VGroup()
    for i, y in enumerate(ROWS):
        text.add(T(str(i + 1), 32, TEXT).move_to(point(1.00, y)))
    for x, strengths in ((1.48, (1, 0, 0.37)), (3.88, (0.76, 0, 0.59))):
        group = []
        for y, strength in zip(ROWS, strengths):
            track.add(RoundedRectangle(width=1.95, height=0.43, corner_radius=0.09, stroke_width=1.7,
                                       stroke_color=GREY, stroke_opacity=0.56, fill_color=LANE,
                                       fill_opacity=1).move_to(point(x + 0.975, y)))
            bar = None
            if strength:
                width = 1.72 * strength
                bar = RoundedRectangle(width=width, height=0.25, corner_radius=0.05, stroke_width=0,
                                       fill_color=YELLOW, fill_opacity=0.93).move_to(point(x + 0.11 + width / 2, y))
            group.append(bar)
        bars.append(group)
    return track, text, bars


class S04Population(SpokenScene):
    def construct(self):
        stage = panel("Neural tissue", "Population response")
        field, cells = neural_field(brain=True)
        old_trace = traces()
        self.add(stage.left_frame, stage.right_frame, stage.left_head, field, inserted_probe(), old_trace, schematic())
        self.at("hearing many neurons")
        live = refresh_cells(cells, lambda i, p, t: 0.45 * (0.5 + 0.5 * np.sin(3 * t + i * 2)) ** 4)
        self.add(live)
        self.at("list of each")
        tracks, keys, bars = response_list()
        self.play(FadeOut(old_trace), run_time=0.45)
        self.play(FadeIn(stage.right_head), FadeIn(keys), LaggedStart(*(Create(track) for track in tracks), lag_ratio=0.11),
                  FadeOut(live), run_time=1.32)
        a = T("Odour A", 32, ORANGE).move_to(point(2.45, 2.06))
        b = T("Odour B", 32, ORANGE).move_to(point(4.85, 2.06))
        self.at("mouse smells odor")
        cloud = odour_cloud(ORANGE)
        self.play(FadeIn(cloud), FadeIn(a), run_time=0.52)
        self.at("one neuron fires")
        focus = [Circle(radius=0.30, color=YELLOW, stroke_width=3,
                        fill_color=YELLOW, fill_opacity=opacity).move_to(cell[1])
                 for cell, opacity in zip(cells[-3:], (0.59, 0, 0.33))]
        strength = [0.93, 0.0, 0.62]
        self.play(cloud.animate.shift(RIGHT * 1.93 + DOWN * 0.40), Create(focus[0]),
                  GrowFromEdge(bars[0][0], LEFT), run_time=0.93)
        self.at("one stays quiet")
        focus[1].set_stroke(GREY, opacity=0.75)
        self.play(cloud.animate.shift(RIGHT * 1.30), Create(focus[1]), run_time=0.95)
        self.at("another fires a little")
        self.play(cloud.animate.shift(RIGHT * 0.70 + DOWN * 0.27), Create(focus[2]),
                  GrowFromEdge(bars[0][2], LEFT), run_time=1.02)
        self.play(FadeOut(cloud), run_time=0.58)
        self.at("do the same")
        cloud_b = odour_cloud(ORANGE)
        self.play(FadeOut(VGroup(*focus)), FadeIn(cloud_b), FadeIn(b), run_time=0.78)
        self.at("odor b")
        live_b = refresh_cells(cells, lambda i, p, t: (
            strength[i - len(cells) + 3] * (0.68 + 0.23 * np.sin(4 * t + i))
            if i >= len(cells) - 3 else 0))
        self.add(live_b)
        self.play(cloud_b.animate.shift(RIGHT * 3.99 + DOWN * 0.48),
                  LaggedStart(*(GrowFromEdge(bar, LEFT) for bar in bars[1] if bar), lag_ratio=0.4),
                  run_time=1.75)
        self.play(FadeOut(cloud_b), run_time=0.47)
        self.at("two odors are represented")
        overlap = VGroup(*[RoundedRectangle(width=4.53, height=0.67, corner_radius=0.12, fill_color=YELLOW, fill_opacity=0.12,
                                           stroke_color=YELLOW, stroke_width=2.7)
                           .move_to(point(3.66, ROWS[i])) for i in (0, 2)])
        self.play(LaggedStart(*(Create(ring) for ring in overlap), lag_ratio=0.42), run_time=1.65)
        self.at("same neurons respond")
        self.play(LaggedStart(*(ring.animate.set_fill(YELLOW, opacity=0.26) for ring in overlap),
                              lag_ratio=0.63), run_time=1.5)
        self.play(*(ring.animate.set_fill(YELLOW, opacity=0.13) for ring in overlap), run_time=1.10)
        self.finish()


def waveforms(x0, y0, which, color, w=1.22, h=0.65):
    plot = Plot((x0, x0 + w, y0 - h / 2, y0 + h / 2), (0, 1), (-1, 1))
    width = 0.10 if which == 0 else 0.19
    return VGroup(*[
        plot.curve(lambda t, offset=offset: scale * spike(t, 0.4 + offset, width),
                   color=color, width=2.5, n=52, opacity=0.72 + i * 0.10)
        for i, (offset, scale) in enumerate(((-0.045, 0.82), (0.028, 0.69), (0, 0.98)))
    ])


def sorting_examples():
    locations = (0.81, 2.45, 4.12)
    one_to_many = VGroup(*[waveforms(x, 1.0, 0, YELLOW, w=1.5) for x in locations])
    many_to_one = VGroup(waveforms(1.22, -0.78, 0, YELLOW, w=1.94),
                         waveforms(3.35, -0.78, 1, YELLOW, w=1.94))
    return one_to_many, many_to_one


def sorting_error(split=False):
    source_rows = (0.43, 0.43) if split else (1.03, -0.36)
    target_rows = (1.03, -0.36) if split else (0.43, 0.43)
    left, paths, right = VGroup(), VGroup(), VGroup()
    for y in dict.fromkeys(source_rows):
        cell = VGroup(Dot(point(1.08, y), radius=0.16, color=GREY),
                      Circle(radius=0.25, stroke_color=GREY, stroke_width=2).move_to(point(1.08, y)))
        left.add(cell)
    for y, dest in zip(source_rows, target_rows):
        paths.add(Line(point(1.49, y), point(4.44, dest), color=RED, stroke_width=4))
    for y in dict.fromkeys(target_rows):
        right.add(Circle(radius=0.47, stroke_color=PURPLE, stroke_width=2.5, fill_color=PURPLE,
                         fill_opacity=0.24).move_to(point(5.04, y)))
    return left, paths, right


class S05Sorting(SpokenScene):
    def construct(self):
        stage = panel("Probe in tissue", "Spike shapes")
        field, cells = neural_field(brain=True)
        probe = inserted_probe()
        input_traces = traces()
        self.add(stage.left_frame, stage.right_frame, field, probe, input_traces, schematic())
        labels, arrows = chain(range(4))
        self.at("to build that list")
        self.play(FadeIn(stage.left_head), FadeIn(stage.right_head), run_time=0.48)
        self.at("sites feed channels")
        self.play(FadeIn(labels[0]), run_time=0.37)
        self.play(GrowArrow(arrows[1]), FadeIn(labels[1]), run_time=0.57)
        self.at("then sorted units")
        self.play(GrowArrow(arrows[2]), FadeIn(labels[2]), run_time=0.68)
        overlay = VGroup(*(waveforms(1.3 + i * 1.52, 0.23 + 0.31 * (i % 2), i % 2,
                                      YELLOW, h=0.95) for i in range(3)))
        self.at("sorting groups spikes")
        self.play(FadeOut(input_traces), run_time=0.32)
        self.play(FadeIn(overlay), run_time=0.65)
        units = VGroup(waveforms(1.1, 0.65, 0, PURPLE, w=2.0, h=1.05),
                       waveforms(3.62, -0.44, 1, PURPLE, w=2.0, h=1.05))
        self.at("by shape")
        self.play(ReplacementTransform(overlay, units), run_time=0.79)
        self.at("meant to be")
        self.play(GrowArrow(arrows[3]), FadeIn(labels[3]), run_time=0.72)
        groups = VGroup(*(SurroundingRectangle(row, color=PURPLE, buff=0.20, corner_radius=0.16,
                                               fill_color=PURPLE, fill_opacity=0.14) for row in units))
        for frame in groups:
            frame.set_z_index(1)
        for row in units:
            row.set_z_index(2)
        self.play(LaggedStart(*(Create(frame) for frame in groups), lag_ratio=0.45), run_time=1.49)
        self.at("yet 960 sites")
        mismatch = T("960 sites ≠ 960 neurons", 31, RED).move_to(point(RX, -1.86))
        self.play(FadeIn(mismatch), run_time=0.60)
        sample_sites = Rectangle(width=1.25, height=1.05, stroke_color=BLUE, stroke_width=3,
                                 fill_color=BLUE, fill_opacity=0.54).move_to(point(-3.68, 1.01))
        self.play(FadeIn(sample_sites), run_time=0.52)
        self.at("do not equal")
        self.play(sample_sites.animate.shift(DOWN * 2.48), run_time=2.64, rate_func=linear)
        self.play(FadeOut(sample_sites), run_time=0.40)
        self.at("neuron can reach")
        same_spike, two_spikes = sorting_examples()
        first_caption = T("One neuron, several sites", 29, TEXT).move_to(point(RX, 1.76))
        second_caption = T("One site, several neurons", 29, TEXT).move_to(point(RX, -0.03))
        self.play(FadeOut(units), FadeOut(groups), FadeOut(mismatch), run_time=0.36)
        one_cell = Circle(radius=0.30, color=YELLOW, fill_color=YELLOW, fill_opacity=0.40,
                          stroke_width=2).move_to(cells[-3][1])
        pickup = VGroup(*[Dot(point(-3.68, y), color=BLUE, radius=0.11) for y in (0.58, 0.28, -0.02)])
        self.play(FadeIn(first_caption), FadeIn(one_cell), FadeIn(pickup),
                  LaggedStart(*(Create(form) for form in same_spike), lag_ratio=0.34), run_time=1.64)
        self.at("one site can hear")
        other_cell = one_cell.copy().move_to(cells[-1][1])
        self.play(FadeIn(second_caption), FadeIn(other_cell), FadeOut(pickup[0]), FadeOut(pickup[2]),
                  LaggedStart(*(Create(form) for form in two_spikes), lag_ratio=0.43), run_time=1.48)
        self.at("quality scores")
        quality = T("Quality scores: partial check", 28, GREEN).move_to(point(RX, -2.16))
        self.play(FadeOut(VGroup(same_spike, two_spikes, first_caption, second_caption, one_cell, other_cell, pickup[1])), run_time=0.55)
        left, pathways, right = sorting_error()
        VGroup(left, pathways, right).scale(0.66).move_to(point(RX, 0.94))
        self.play(FadeIn(quality), FadeIn(left), run_time=0.71)
        self.at("can still merge")
        merge_label = T("Merge", 32, RED).move_to(point(RX, 1.92))
        self.play(Create(pathways), FadeIn(right), FadeIn(merge_label), run_time=0.75)
        self.at("or split neurons")
        split_left, split_paths, split_right = sorting_error(split=True)
        VGroup(split_left, split_paths, split_right).scale(0.66).move_to(point(RX, -1.03))
        split_label = T("Split", 32, RED).move_to(point(RX, 0.03))
        self.play(FadeIn(split_left), Create(split_paths), FadeIn(split_right), FadeIn(split_label), run_time=1.12)
        pulse(split_paths[0], base=4, amp=1.85, speed=4.6)
        pulse(split_paths[1], base=4, amp=1.85, speed=4.6)
        self.finish()


def mouse(cx, cy):
    """Side silhouette with the head at right, preserving the unit region at its center."""
    coords = [(-1.43, -0.43), (-1.40, 0.27), (-1.08, 0.84), (-0.48, 1.13),
              (0.35, 1.10), (0.69, 0.99), (0.87, 1.19), (1.12, 1.03),
              (1.06, 0.73), (1.40, 0.48), (1.72, 0.03), (1.30, -0.28),
              (0.94, -0.36), (0.71, -0.66), (0.22, -0.80), (-0.79, -0.81),
              (-1.33, -0.63), (-1.43, -0.43)]
    body = VMobject(stroke_width=2.7, stroke_color=GREY, fill_color=TISSUE, fill_opacity=1)
    body.set_points_smoothly([point(cx + x, cy + y) for x, y in coords])
    tail = CubicBezier(point(cx - 1.40, cy - 0.43), point(cx - 2.24, cy - 0.72),
                       point(cx - 0.94, cy - 1.42), point(cx - 1.73, cy - 1.43),
                       stroke_width=3.1, color=GREY)
    eye = Dot(point(cx + 1.16, cy + 0.40), radius=0.065, color=TEXT)
    return VGroup(tail, body, eye)


def samples(include_units=True):
    mice, probes, units = VGroup(), VGroup(), VGroup()
    for cx, count in zip((-4.20, 0, 4.20), (96, 104, 100)):
        mice.add(mouse(cx, -0.22))
        pin = Polygon(point(cx - 0.15, 1.22), point(cx + 0.15, 1.22),
                      point(cx + 0.12, 0.37), point(cx, 0.20), point(cx - 0.12, 0.37),
                      color=BLUE, fill_color=BLUE, fill_opacity=0.82, stroke_width=2.4)
        probes.add(pin.set_z_index(2))
        if include_units:
            dots = [point(cx + 0.10 + 0.12 * (i % 13 - 6) + 0.022 * np.sin(i * 6),
                          -0.36 + 0.11 * (i // 13 - 3.5) + 0.025 * np.cos(i * 3))
                    for i in range(count)]
            units.add(packed_dots(dots, 0.036, PURPLE, 0.91).set_z_index(3))
    return mice, probes, units


def sampling_backdrop():
    labels, arrows = chain((2, 4))
    return VGroup(*samples(), *labels.values(), *arrows.values(), schematic())


def animal_bars(xs, bottoms, heights, width):
    return VGroup(*[RoundedRectangle(width=width, height=h, corner_radius=0.095, stroke_color=GREEN,
                                     stroke_width=2.4, fill_color=GREEN, fill_opacity=0.59)
                    .move_to(point(x, y + h / 2)).set_z_index(3) for x, y, h in zip(xs, bottoms, heights)])


class S06Predict(SpokenScene):
    def construct(self):
        stage = panel("Probe in tissue", "Spike shapes")
        field, _ = neural_field(brain=True)
        probe = inserted_probe()
        labels, arrows = chain((2, 4))
        mice, probes, units = samples()
        self.add(stage.left_frame, stage.right_frame, field, probe, labels[2], schematic())
        self.at("now check the")
        self.play(FadeOut(stage.left_frame), FadeOut(stage.right_frame), FadeOut(field),
                  ReplacementTransform(probe, probes[1]), FadeIn(mice[1]), run_time=1.6)
        self.at("from units to")
        self.play(GrowArrow(arrows[4]), FadeIn(labels[4]), run_time=1.0)
        self.at("suppose a study")
        self.play(LaggedStart(FadeIn(mice[0]), FadeIn(mice[2]), lag_ratio=0.30), FadeIn(probes[0]),
                  FadeIn(probes[2]), run_time=1.23)
        self.at("sorted units from")
        self.play(LaggedStart(*(FadeIn(group, shift=UP * 0.20) for group in units), lag_ratio=0.42), run_time=1.42)
        self.at("how many samples")
        self.play(FadeIn(question_card(QUESTION, **QUESTION_LAYOUT)), run_time=0.85)
        self.finish()


class S07Pause(PredictPause):
    QUESTION = QUESTION
    CARD = QUESTION_LAYOUT
    RING_AT = (5.90, 2.10, 0)
    SECONDS = 4.5

    def backdrop(self):
        picture = sampling_backdrop()
        time = 0.0

        def glow(dots, dt):
            nonlocal time
            time += dt
            dots.set_fill(opacity=0.61 + 0.30 * np.cos(TAU * time / self.SECONDS))

        picture[2].add_updater(glow)
        return picture

    def construct(self):
        self.add(self.backdrop(), question_card(self.QUESTION, **self.CARD))
        ring, progress = countdown(self.SECONDS, self.RING_AT, radius=0.60)
        ring[0].set_fill(opacity=0)
        self.add(ring)
        self.play(progress)


class S08Controls(SpokenScene):
    def construct(self):
        mice, probes, units = samples()
        short, short_arrows = chain((2, 4))
        question = question_card(QUESTION, **QUESTION_LAYOUT)
        self.add(mice, probes, units, *short.values(), *short_arrows.values(), question, schematic())
        self.at("3 not 300")
        answer = T("3 samples", 43, GREEN, weight=BOLD).move_to(question)
        self.play(swap(question, answer, 0.8))
        self.at("more units sharpen")
        xs = tuple(probe.get_center()[0] for probe in probes)
        bars = animal_bars(xs, (-0.82,) * 3, (0.78, 0.62, 0.90), 0.65)
        self.play(LaggedStart(*[ReplacementTransform(dots, bar) for dots, bar in zip(units, bars)],
                              lag_ratio=0.25), run_time=2.80)
        self.at("same mouse")
        self.play(LaggedStart(*[Indicate(m[1], color=GREEN, scale_factor=1.065) for m in mice],
                              lag_ratio=0.55), run_time=1.70)
        self.at("more animals add")
        bodies = VGroup(*(animal[1] for animal in mice))
        animal_fill = interpolate_color(ManimColor(TISSUE), ManimColor(GREEN), 0.42)
        self.play(LaggedStart(*(bar.animate.set_fill(GREEN, opacity=0.94) for bar in bars),
                              lag_ratio=0.65),
                  bodies.animate.set_fill(animal_fill).set_stroke(GREEN), run_time=2.0)
        self.at("works at the animal level")
        analysis_label = T("Animal-level analysis", 36, GREEN).move_to(point(0, 2.15))
        self.play(FadeIn(analysis_label), bodies.animate.set_fill(TISSUE), run_time=0.75)
        self.at("arrays hear populations")
        long, long_arrows = chain(range(5))
        self.play(FadeOut(short_arrows[4]), run_time=0.38)
        self.play(FadeIn(long[0]), GrowArrow(long_arrows[1]), FadeIn(long[1]),
                  GrowArrow(long_arrows[2]), run_time=1.25)
        self.at("sites are not neurons")
        bodies.save_state()
        bars.save_state()
        self.play(GrowArrow(long_arrows[3]), FadeIn(long[3]), bodies.animate.set_opacity(0.40),
                  bars.animate.set_opacity(0.28), run_time=0.62)
        self.play(Indicate(long[0].box, scale_factor=1.02), Indicate(long[3].box, scale_factor=1.02),
                  run_time=0.78)
        self.at("sorted units are not animals")
        self.play(GrowArrow(long_arrows[4]), Indicate(short[2].box, scale_factor=1.02),
                  Indicate(short[4].box, scale_factor=1.02), Restore(bodies), Restore(bars), run_time=1.35)
        self.finish()


def retinal_glow(cells, live=False):
    time = 0.0
    positions = [cell.get_center() for cell in cells]
    start = -positions[0][0] if live else -5.7
    # Reflect the live pathway so increasing wave phase runs from eye to brain.
    direction = -1 if live else 1
    period = 3.7 if live else 6.0
    glows = VGroup(*[Dot(p, radius=0.095, color=YELLOW, fill_opacity=0) for p in positions])

    def refresh(g, dt):
        nonlocal time
        time += dt
        for glow, p in zip(g, positions):
            glow.set_fill(opacity=wave_strength(direction * p[0], time, start=start, width=0.79,
                                                speed=1.02, period=period))

    refresh(glows, 0)
    return glows.add_updater(refresh)


def visual_pathway():
    animal = mouse(3.12, -0.05).scale(1.28, about_point=point(3.12, -0.05))
    retina_node = point(4.59, 0.46)
    brain_node = point(2.22, 0.68)
    route = CubicBezier(retina_node, point(3.88, 0.49), point(3.20, 0.05), brain_node,
                        color=GREY, stroke_width=4)
    dots = VGroup(*[Dot(route.point_from_proportion(t), radius=0.053, color=GREY)
                    for t in np.linspace(0, 1, 17)])
    nodes = VGroup(*[Circle(radius=r, stroke_width=2, color=GREY).move_to(p)
                     for p, r in ((retina_node, 0.14), (brain_node, 0.29))])
    return VGroup(animal, route, nodes, dots), dots


class S09Waves(SpokenScene):
    def construct(self):
        stage = panel("1991 · Isolated retina", "2012 · Live mice")
        array, sheet = flat_array(), retina()
        self.add(stage.left_frame, stage.right_frame, schematic())
        self.at("in 1991")
        self.play(FadeIn(sheet[0], shift=DOWN * 0.68), run_time=2.18)
        self.at("laid isolated retinas")
        self.play(Create(array), sheet[0].animate.shift(DOWN * 0.12), run_time=1.28)
        self.play(sheet[0].animate.shift(UP * 0.12), FadeIn(stage.left_head), run_time=0.72)
        self.at("recorded up to")
        burst_heading = T("Ganglion cell traces", 32, YELLOW).move_to(stage.right_head)
        burst_times = ((1.82, 1.97, 2.10, 6.09, 6.19, 6.34),
                       (1.96, 2.11, 2.24, 6.23, 6.36, 6.50),
                       (3.47, 3.59, 3.67, 7.40, 7.50, 7.66))
        bursts = traces(sources=burst_times)
        hundred = T("Up to 100 ganglion cells", 30, TEXT).move_to(point(CX, 1.35))
        count_rows = VGroup(*[VGroup(*sheet[1][i:i + 20]) for i in range(0, 100, 20)])
        self.play(LaggedStart(*(FadeIn(row) for row in count_rows), lag_ratio=0.43),
                  FadeIn(hundred), FadeIn(burst_heading), Create(bursts[0]), Create(bursts[1]), run_time=2.36)
        self.add(bursts[2])
        self.at("newborn ferrets")
        species = T("Newborn ferrets · fetal cats", 28, TEXT).move_to(point(CX, 0.62))
        self.play(FadeIn(species), run_time=0.65)
        self.at("nearby cells fired")
        glow = retinal_glow(sheet[1])
        self.add(glow)
        self.play(FadeOut(species), run_time=0.55)
        self.at("waves several hundred")
        distance = T("Several hundred µm wide", 29, YELLOW).move_to(point(CX, 0.45))
        self.play(FadeIn(distance), run_time=0.75)
        self.at("in 2012")
        live, dots = visual_pathway()
        self.play(FadeOut(VGroup(burst_heading, bursts)), run_time=0.54)
        self.play(FadeIn(live[0]), run_time=1.55)
        self.at("imaged live neonatal")
        self.play(Create(live[1]), FadeIn(live[2]), FadeIn(dots), FadeIn(stage.right_head), run_time=1.18)
        self.at("showing waves are")
        self.add(retinal_glow(dots, live=True))
        self.finish()


def organoid():
    tissue = outline(CX, -0.29, 2.02, 1.51, phase=2.6)
    rng = np.random.default_rng(2019)
    points = []
    for _ in range(210):
        x, y = rng.uniform(-1, 1, 2)
        if x * x + y * y < 0.88:
            points.append(point(CX + 1.95 * x, -0.29 + 1.43 * y))
    granular = packed_dots(points, 0.036, GREY, 0.58)
    folds = VGroup(*[ArcBetweenPoints(point(x, y), point(x + dx, y + dy), angle=angle,
                                      stroke_color=GREY, stroke_opacity=0.71, stroke_width=2.5)
                     for x, y, dx, dy, angle in ((-4.81, 0.12, 0.94, 0.35, 1.3), (-3.8, 0.73, 1.1, 0.15, -0.9),
                                                 (-3.2, -0.13, 1.12, 0.7, -1.4), (-4.45, -0.75, 0.88, -0.37, 1.4),
                                                 (-3.20, -1.08, 1.2, 0.44, 1.0))])
    return VGroup(tissue, granular, folds)


class S10Organoids(SpokenScene):
    def construct(self):
        stage = panel("Cortical organoid", "Recorded activity")
        array, sheet = flat_array(), retina()
        grown = organoid()
        self.add(stage.left_frame, array, sheet, schematic())
        self.at("arrays also track")
        self.play(ReplacementTransform(sheet[0], grown[0]), FadeOut(sheet[1]),
                  FadeIn(grown[1:]), run_time=1.57)
        self.at("tissue grown in")
        self.play(FadeIn(stage.left_head), run_time=0.75)
        self.at("for months")
        month = T("2019 · Months on array", 31, GOLD).move_to(point(CX, 1.73))
        self.play(FadeIn(month), run_time=0.79)
        self.at("in 2019")
        richness = ValueTracker(0)
        recording = traces(1, y0=-1.35, y1=1.75, richness=richness)
        self.play(FadeIn(stage.right_frame), Create(recording[0]), run_time=1.95)
        self.at("colleagues recorded these")
        self.play(FadeIn(stage.right_head), Create(recording[1]), run_time=2.0)
        self.add(recording[2])
        self.at("network oscillations growing")
        oscillations = T("Network oscillations", 31, YELLOW).move_to(point(RX, -1.94))
        self.play(richness.animate.set_value(0.78), FadeIn(oscillations), run_time=2.85)
        self.at("features resembling")
        eeg = T("Some features resemble\npreterm infant EEG", 30, TEXT,
                line_spacing=0.82).move_to(point(RX, -2.02))
        self.play(richness.animate.set_value(1), swap(oscillations, eeg, 1.12), run_time=1.72)
        self.at("yet coordinated firing")
        self.play(FadeOut(eeg), run_time=0.6)
        self.at("with no inputs")
        caution = boxed_label("No inputs", GREEN, size=28).move_to(point(-4.92, -3.22))
        term = T("Mini-brain", 32, RED).next_to(caution, RIGHT, buff=0.45)
        slash = Line(term.get_left() + LEFT * 0.08, term.get_right() + RIGHT * 0.08,
                     stroke_color=RED, stroke_width=3.6)
        slash.layout_ok = "covered"  # intentional strike-through of the rejected label
        self.play(FadeIn(caution), FadeIn(term), run_time=0.62)
        self.at("a working brain")
        self.play(Create(slash), run_time=0.52)
        self.finish()


class S11Closing(SpokenScene):
    def construct(self):
        stage = panel("Recording hardware", "Recorded activity")
        array = flat_array()
        grown = organoid()
        old_sheet = retina()
        self.add(stage.left_frame, stage.right_frame, array, old_sheet, schematic())
        self.at("from retinal waves")
        glow = retinal_glow(old_sheet[1])
        self.add(glow)
        self.at("organoid rhythms")
        self.play(FadeOut(glow), FadeOut(old_sheet[1]), run_time=0.27)
        self.play(ReplacementTransform(old_sheet[0], grown[0]), FadeIn(grown[1:]), run_time=0.97)
        self.at("arrays and probes")
        probe = inserted_probe().scale(0.73).move_to(point(-3.68, 0.57))
        read = traces(3, x0=0.48, x1=2.85, y0=-2.02, y1=1.90, inset=True)
        body, _ = neural_field()
        body.scale(0.73).move_to(point(CX, 0.54))
        bars = animal_bars((3.75, 4.70, 5.65), (-1.66,) * 3, (2.46, 2.00, 2.78), 0.68)
        hardware = T("Array and probe", 31, BLUE).move_to(point(CX, 2.56))
        units = T("Population traces", 28, YELLOW, font="Avenir Next Condensed").move_to(point(1.73, 2.56))
        animals = T("Animal estimates", 28, GREEN, font="Avenir Next Condensed").move_to(point(4.70, 2.56))
        self.play(FadeOut(grown), FadeIn(body), FadeIn(probe), run_time=1.18)
        self.play(Create(read[0]), Create(read[1]), run_time=1.31)
        self.add(read[2])
        self.play(FadeIn(hardware), FadeIn(units), run_time=0.68)
        self.at("big recording numbers")
        self.play(LaggedStart(*(GrowFromEdge(bar, DOWN) for bar in bars), lag_ratio=0.38), run_time=1.65)
        self.at("count real neurons")
        count = caption("Sites ≠ neurons", size=31, color=PURPLE)
        self.play(FadeIn(count), run_time=0.42)
        self.at("at the animal level")
        self.play(FadeOut(count), FadeIn(animals),
                  LaggedStart(*[Indicate(b, color=GREEN, scale_factor=1.03) for b in bars],
                              lag_ratio=0.46), run_time=1.08)
        self.at("match every claim")
        self.play(LaggedStart(*[Indicate(m, scale_factor=1.01, color=c)
                                for m, c in ((hardware, BLUE), (units, YELLOW), (animals, GREEN))],
                              lag_ratio=0.72), run_time=1.95)
        self.finish()


class S12End(EndCard):
    LINE = "Electrode arrays hear populations together; never confuse sites, units, and animals."
