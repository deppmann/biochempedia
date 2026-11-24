"""Experimental evolution, animated from the supplied narration and word timings.

Colour map: blue glass and water, grey structure, teal hosts and ancestral cells,
purple phages, green and orange derived types, yellow infection, gold citrate use
and active archive markers. Graphs and qualitative readouts are schematic.
"""

from bp_parts import *

PURPLE = "#B58CD9"
ORANGE = "#F29E4C"
GLASS = "#213E51"
BENCH = "#223543"
SOIL = ("#354253", "#3E4C5B", "#4A5365", "#535968")
HOST_X = (-3.8, 0, 3.8)
HOST_NAMES = ("Past", "Same time", "Future")


def p(x, y):
    return np.array([x, y, 0.0])


def label(text, x, y, color=TEXT, size=32):
    return T(text, size, color).move_to(p(x, y))


def plate(width, height, x, y, color=BENCH, edge=GREY, opacity=1):
    return RoundedRectangle(width=width, height=height, corner_radius=0.17,
                            stroke_color=edge, stroke_width=2.4,
                            fill_color=color, fill_opacity=opacity).move_to(p(x, y))


def arrow(start, end, color=GOLD):
    return Arrow(start, end, buff=0, color=color, stroke_width=4, tip_length=0.17)


def flask(x, y, scale=1, tint=TEAL, seed=0, zoned=False, swirl=False):
    """A flask's local liquid, cell paths and glass stay registered when resized."""
    def polygon(points, fill, opacity, edge=BLUE, width=0):
        return Polygon(*(p(*xy) for xy in points), fill_color=fill, fill_opacity=opacity,
                       stroke_color=edge, stroke_width=width)

    profile = [(-0.31, 1.3), (0.31, 1.3), (0.31, 0.58), (1.05, -0.92),
               (1, -1.13), (-1, -1.13), (-1.05, -0.92), (-0.31, 0.58)]
    glass = polygon(profile, GLASS, 1, width=3.4)
    liquid = polygon([(-0.53, 0.14), (0.53, 0.14), (1.02, -0.92),
                      (0.96, -1.10), (-0.96, -1.10), (-1.02, -0.92)], tint, 0.33)
    rim = Line(p(-0.44, 1.3), p(0.44, 1.3), color=BLUE, stroke_width=4)
    surface = Line(p(-0.52, 0.14), p(0.52, 0.14), color=tint, stroke_width=3)
    bands = VGroup()
    if zoned:
        bands.add(polygon([(-0.53, 0.13), (0.53, 0.13), (0.68, -0.2), (-0.68, -0.2)], GREEN, 0.55))
        bands.add(polygon([(-0.82, -0.5), (0.82, -0.5), (1.02, -0.96),
                           (0.96, -1.1), (-0.96, -1.1), (-1.02, -0.96)], ORANGE, 0.36))
        surface.set_stroke(GREEN, width=8)
    rim.set_z_index(2)
    body = VGroup(glass, liquid, bands, surface, rim)
    cells = VGroup()
    rng = np.random.default_rng(seed)
    for i in range(17):
        sy = rng.uniform(-0.91, 0.02)
        sx = rng.uniform(-0.34, 0.34) * (1 - sy)
        color = GREEN if zoned and sy > -0.24 else ORANGE if zoned and sy < -0.52 else tint
        cell = Ellipse(width=0.23, height=0.13, color=color, fill_opacity=1, stroke_width=0)
        cell.rotate(rng.uniform(-0.8, 0.8))
        cell.move_to(p(sx, sy))
        cells.add(cell)
        cell.home = (sx, sy)
    group = VGroup(body, cells).scale(scale).shift(p(x, y))
    for i, cell in enumerate(cells):
        sx, sy = cell.home
        phase = i * 1.43
        cell.clock = 0.0

        def drift(mob, dt, sx=sx, sy=sy, phase=phase):
            mob.clock += dt
            a = mob.clock * (2.65 if swirl else 2.0) + phase
            # The glass provides the scale and origin through every scene transition.
            unit = glass.height / 2.43
            origin = glass.get_center() - UP * (0.085 * unit)
            if swirl:
                offset = p(0.67 * np.cos(a) * (0.7 + 0.2 * np.sin(phase)), -0.56 + 0.36 * np.sin(a))
            else:
                offset = p(sx + 0.19 * np.sin(a), sy + 0.096 * np.cos(a))
            mob.move_to(origin + unit * offset)

        cell.add_updater(drift)
        drift(cell, 0)
    return group


def flasks_on_bench():
    return VGroup(*(flask(x, 0.95, 1.36, seed=i + 10)
                    for i, x in enumerate((-3.8, 0, 3.8))))


def benchtop():
    return plate(12.6, 0.28, 0, -0.86, edge=BLUE)


def generation_track():
    line = Line(p(-5.8, -1.24), p(5.8, -1.24), color=GREY, stroke_width=3)
    ticks = VGroup(*(Line(p(x, -1.32), p(x, -1.15), color=GREY, stroke_width=3) for x in HOST_X))
    return VGroup(line, ticks)


def vial(x, y, kind="host", scale=1, tint=None):
    color = tint or (TEAL if kind == "host" else PURPLE)
    glass = plate(0.58, 0.75, 0, -0.07, color=GLASS, edge=BLUE)
    cap = plate(0.64, 0.15, 0, 0.34, color=BLUE, edge=BLUE)
    icons = VGroup()
    for dx, dy in ((-0.13, -0.03), (0.12, -0.12), (0, -0.27)):
        icon = (Dot(radius=0.058, color=color) if kind == "host" else
                Triangle(stroke_width=0, fill_color=color, fill_opacity=1).scale(0.064))
        icons.add(icon.move_to(p(dx, dy)))
    return VGroup(glass, cap, icons).scale(scale).move_to(p(x, y))


def archive_shelf():
    shelf = plate(12.1, 1.72, 0, -2.42, edge=BLUE)
    dividers = VGroup(*(Line(p(x, -3.12), p(x, -1.72), color=GLASS, stroke_width=5)
                        for x in (-1.9, 1.9)))
    return VGroup(shelf, dividers)


def archive_samples(paired=False):
    return VGroup(*(VGroup(vial(x - 0.37, -2.33), vial(x + 0.37, -2.33, "phage"))
                    if paired else vial(x, -2.33) for x in HOST_X))


def assay_strip():
    source = vial(0, 2.28, "phage", 1.35)
    hosts = VGroup(*(vial(x, -0.25, scale=1.35) for x in HOST_X))
    names = VGroup(*(label(name, x, -1.20) for name, x in zip(HOST_NAMES, HOST_X)))
    links = VGroup(*(arrow(p(0, 1.67), p(x, 0.42), PURPLE) for x in HOST_X))
    return source, hosts, links, names


def source_tag(text):
    return label(text, -1.0, 3.36, TEXT, 28)


def schema():
    return scope_tag("schematic", size=28, color=TEXT).move_to(p(4.26, -3.31))


class S01Hook(SpokenScene):
    def construct(self):
        slab = VGroup(Polygon(p(-5.75, 2.08), p(4.95, 2.28), p(5.74, 0.98), p(5.05, -1.45),
                              p(-4.94, -1.61), p(-5.77, -0.47), stroke_color=GREY, stroke_width=3,
                              fill_color=BENCH, fill_opacity=1),
                      Line(p(-4.85, -0.59), p(4.8, -0.59), color=GREY, stroke_width=4))
        for i, x in enumerate((-4, -2, 0, 2, 4)):
            slab.add(Line(p(x, -0.72), p(x, -0.45), color=GREY, stroke_width=3))
            impression = VGroup(*(Arc(radius=0.25 + 0.09 * j, start_angle=0.3, angle=3.8,
                                      color=GREY, stroke_width=2.3) for j in range(4)))
            impression.rotate(-0.4 + i * 0.23).move_to(p(x, 0.55 + 0.21 * np.sin(i)))
            slab.add(impression)
        history = label("History", 0, -2.1, TEXT)
        highlight = Dot(p(-4.8, -0.59), color=GOLD, radius=0.11)
        self.add(slab, history, highlight)
        self.at("How can biologists")
        self.play(highlight.animate.move_to(p(4.8, -0.59)), run_time=3.35, rate_func=linear)
        self.at("happened only once")
        crack = VMobject(stroke_color=GOLD, stroke_width=5).set_points_as_corners(
            [p(-0.35, 2.2), p(-0.89, 1.36), p(-0.22, 0.69), p(-0.72, -0.17), p(-0.28, -1.49)])
        question = label("?", 0, 0.35, GOLD, 216)
        self.play(Create(crack), FadeOut(highlight), run_time=0.37)
        halves = VGroup(
            Polygon(p(-5.75, 2.08), p(-1.57, 2.17), p(-1.95, 1.36), p(-1.56, 0.69),
                    p(-1.92, -0.17), p(-1.58, -1.57), p(-4.94, -1.61), p(-5.77, -0.47),
                    fill_color=BENCH, fill_opacity=1, stroke_color=GREY, stroke_width=2.4),
            Polygon(p(1.79, 2.22), p(4.95, 2.28), p(5.74, 0.98), p(5.05, -1.45),
                    p(1.84, -1.52), p(1.48, -0.17), p(1.88, 0.69), p(1.46, 1.36),
                    fill_color=BENCH, fill_opacity=1, stroke_color=GREY, stroke_width=2.4),
        )
        self.play(FadeOut(slab), FadeOut(crack), FadeOut(history), run_time=0.23)
        self.play(FadeIn(halves), FadeIn(question, scale=0.7), run_time=0.55)
        self.at("Experimental evolution")
        flasks, bench, track = flasks_on_bench(), benchtop(), generation_track()
        self.play(FadeOut(question), FadeOut(halves), run_time=0.26)
        self.play(FadeIn(bench), FadeIn(track), LaggedStart(
            *(FadeIn(f, shift=UP * 0.15) for f in flasks), lag_ratio=0.35), run_time=1.75)
        self.at("also archives ancestors", lead=0.7)
        shelf = archive_shelf()
        samples = archive_samples()
        self.play(FadeIn(shelf), run_time=0.36)
        self.play(LaggedStart(*(FadeIn(v, shift=DOWN * 0.48) for v in samples), lag_ratio=0.42), run_time=1.6)
        self.at("past with present")
        self.play(FadeIn(label("Past", -3.8, -3.0)), FadeIn(label("Present", 3.8, -3.0)), run_time=0.45)
        self.finish()


class S02Title(TitleCard):
    LESSON = "Experimental Evolution"
    TITLE = "Replaying Evolution in Real Time"

    def construct(self):
        self.add(flasks_on_bench(), benchtop(), generation_track(), archive_shelf(), archive_samples())
        veil = Rectangle(width=config.frame_width, height=config.frame_height,
                         fill_color=BG, fill_opacity=0.90, stroke_width=0)
        veil.set_z_index(3)
        title = fit_text(self.TITLE, max_w=11.2, size=53, min_size=42, font=TITLE_FONT)
        title.set_z_index(4)
        title.move_to(p(0, 0.15))
        self.play(FadeIn(veil), run_time=0.30)
        self.play(FadeIn(title), run_time=0.32)
        self.wait(0.92)
        self.play(FadeOut(title), run_time=0.29)
        self.play(FadeOut(veil), run_time=0.23)
        self.finish()


class S03Replicates(SpokenScene):
    def construct(self):
        bench = benchtop()
        starter = flask(0, 1.27, 1.34, seed=10)
        # Each treatment has the same number and size of independent flasks.
        positions = (-4.68, -2.18, 2.18, 4.68)
        replica_y = 0.09
        replicas = [flask(x, replica_y, 1.06, seed=i) for i, x in enumerate(positions)]
        self.add(starter, bench)
        self.at("Split one genotype")
        # Cell updaters refer to the original glass, including on Manim's animation copies.
        starter.suspend_updating()
        for f in replicas:
            f.suspend_updating()
        self.play(*(TransformFromCopy(starter, f, suspend_mobject_updating=False) for f in replicas),
                  bench.animate.shift(DOWN * 0.39), run_time=1.55)
        self.play(starter.animate.scale(0.43).move_to(p(0, 2.46)), run_time=0.75)
        for f in replicas:
            f.resume_updating()
        self.at("differing in one factor")
        links = VGroup(*(arrow(starter.get_bottom() + DOWN * 0.09,
                               f.get_top() + UP * 0.08, BLUE) for f in replicas))
        self.play(Create(links), run_time=0.8)
        self.at("Rainey and Travisano")
        reference = label("Rainey & Travisano, 1998", -3.33, 3.36, TEXT, 28)
        self.play(FadeIn(reference), run_time=0.55)
        self.at("grew the bacterium")
        species = label("Pseudomonas fluorescens", 0, -2.76, TEAL)
        self.play(FadeIn(species), run_time=0.5)
        self.at("unshaken or shaken")
        still = label("Unshaken", -3.43, -1.89)
        shaken = label("Shaken", 3.43, -1.89)
        self.play(FadeIn(still), FadeIn(shaken), FadeOut(links), FadeOut(starter), run_time=0.63)
        for i in (2, 3):
            new = flask(positions[i], replica_y, 1.06, seed=i, swirl=True)
            self.play(FadeOut(replicas[i]), FadeIn(new), run_time=0.32)
            replicas[i] = new
        self.at("broth formed zones", lead=0.8)
        zones = [flask(positions[i], replica_y, 1.06, seed=i, zoned=True) for i in (0, 1)]
        bands = [f[0][2] for f in replicas[:2]]
        for layer, zoned in zip(bands, zones):
            layer.add(zoned[0][2][0])
        self.play(*(FadeIn(layer[0]) for layer in bands), run_time=1.7)
        self.at("surface down", lead=0.2)
        for layer, zoned in zip(bands, zones):
            layer.add(zoned[0][2][1])
        self.play(*(FadeIn(layer[1].set_fill(opacity=0.9)) for layer in bands),
                  *(layer[0].animate.set_fill(opacity=0.9) for layer in bands),
                  *(f[0][3].animate.set_stroke(GREEN, width=7) for f in replicas[:2]), run_time=1.8)
        self.at("New heritable types")
        self.play(*(FadeOut(replicas[i][1]) for i in (0, 1)),
                  *(FadeIn(f[1]) for f in zones), run_time=1.0)
        self.at("shaken flasks that diversity")
        self.play(shaken.animate.set_color(TEAL),
                  *(replicas[i][0][1].animate.set_fill(opacity=0.67) for i in (2, 3)), run_time=1.1)
        self.play(*(replicas[i][0][1].animate.set_fill(opacity=0.33) for i in (2, 3)), run_time=1.5)
        self.finish()


class S04Archive(SpokenScene):
    def construct(self):
        flasks, bench, track = flasks_on_bench(), benchtop(), generation_track()
        shelf = archive_shelf()
        samples = archive_samples(paired=True)
        cursor = Dot(p(-5.8, -1.24), radius=0.086, color=GOLD)
        self.add(flasks, bench, track, shelf, cursor)
        self.at("generations pass")
        for x, pair in zip(HOST_X, samples):
            self.play(cursor.animate.move_to(p(x, -1.24)), run_time=0.8, rate_func=linear)
            self.play(FadeIn(pair, shift=DOWN * 0.5), run_time=0.65)
        self.at("Replicate populations")
        sheen = shelf[0].copy().set_fill(opacity=0).set_stroke(GOLD, width=5)
        self.play(Create(sheen), cursor.animate.move_to(p(5.8, -1.24)), run_time=1.5)
        self.at("archived ancestors")
        self.play(*(f[0][-1].animate.set_stroke(width=7) for f in flasks), run_time=1.0)
        self.at("experiment you can repeat")
        self.play(FadeOut(sheen), run_time=0.7)
        self.at("When bacteria evolve")
        source, hosts, links, names = assay_strip()
        self.play(FadeOut(flasks), FadeOut(bench), FadeOut(cursor), FadeOut(track), run_time=0.65)
        self.play(TransformFromCopy(samples[1][1], source),
                  *(TransformFromCopy(pair[0], host) for pair, host in zip(samples, hosts)),
                  run_time=1.35)
        self.at("paired across time")
        self.play(LaggedStart(*(GrowArrow(a) for a in links), lag_ratio=0.25), FadeIn(names), run_time=1.23)
        self.at("That cross is")
        self.play(FadeIn(label("Time-shift assay", 0, 3.31, GOLD)), run_time=0.53)
        self.finish()


def infection_plot(extended=False, host_ticks=True):
    domain = (-3.8, 3.8) if extended else (-1.42, 1.42)
    ticks = list(zip((-1, 0, 1), HOST_NAMES)) if host_ticks else []
    plot = Plot(box=(-5.4, 5.4, -1.66, 2.55), xr=domain, yr=(0, 1), xticks=ticks,
                ylabel="Infection", color=TEXT, size=32, label_size=32)
    backing = Polygon(p(-5.4, -1.66), p(5.4, -1.66), p(5.4, 2.55), p(-5.4, 2.55),
                      fill_color=GLASS, fill_opacity=1, stroke_width=0)
    plot.add_to_back(backing)
    return plot


def infection_flat(x):
    return 0.52


def infection_race(x):
    return 0.52 - 0.25 * x


def infection_peak(x):
    return 0.32 + 0.46 * np.exp(-2 * x ** 2)


def infection_wave(x):
    # Equals the short record at all three displayed sampling points.
    return 0.52 - 0.25 * np.sin(np.pi * x / 2)


def filled_trace(plot, fn, color=YELLOW, x0=-1, x1=1):
    points = [plot.pt(x, fn(x)) for x in np.linspace(x0, x1, 81)]
    area = Polygon(plot.pt(x0, 0), *points, plot.pt(x1, 0),
                   fill_color=color, fill_opacity=0.24, stroke_width=0)
    return VGroup(area, plot.curve(fn, x0, x1, color, width=5.5))


def trace_points(plot, fn, xs=(-1, 0, 1), color=YELLOW, radius=0.084):
    return VGroup(*(Dot(plot.pt(x, fn(x)), radius=radius, color=color) for x in xs))


def running_marker(plot, model, position, x0=-1, x1=1):
    def x():
        return interpolate(x0, x1, position.get_value())

    def sampling_band():
        start = max(x0, x() - 0.19)
        stop = min(x1, x() + 0.19)
        return Polygon(plot.pt(start, 0), plot.pt(start, model(start)), plot.pt(stop, model(stop)),
                       plot.pt(stop, 0), stroke_width=0, fill_color=YELLOW, fill_opacity=0.50)

    return VGroup(always_redraw(sampling_band),
                  plot.dot(x, lambda: model(x()), color=TEXT, ring=YELLOW, radius=0.105))


def predict_bracket(plot):
    ends = (plot.pt(-1, 0)[0], plot.pt(1, 0)[0])
    y = -2.68
    return VGroup(Line(p(ends[0], y), p(ends[1], y), color=BLUE, stroke_width=3),
                  *(Line(p(x, y), p(x, y + 0.17), color=BLUE, stroke_width=3) for x in ends),
                  label("20 weeks", 0, -3.08, BLUE))


PREDICTION = "Arms race?"
PREDICT_CARD = {"y": 3.31, "size": 40, "left": -1.31}


def prediction_still():
    plot = infection_plot()
    return VGroup(plot, filled_trace(plot, infection_race), trace_points(plot, infection_race),
                  predict_bracket(plot), schema())


class S05Timeshift(SpokenScene):
    def construct(self):
        source, hosts, links, names = assay_strip()
        shelf, samples = archive_shelf(), archive_samples(paired=True)
        title = label("Time-shift assay", 0, 3.31, GOLD)
        self.add(shelf, samples, source, hosts, links, names, title)
        self.at("Test phages from")
        for host, link in zip(hosts, links):
            pulse(link, base=4, amp=1.4, speed=2.8)
            bob(host, amp=0.07, speed=1.9)
        self.at("Without heritable change", lead=0.86)
        self.play(FadeOut(source), FadeOut(hosts), FadeOut(links), FadeOut(names),
                  FadeOut(shelf), FadeOut(samples), FadeOut(title), run_time=0.5)
        plot = infection_plot()
        self.play(FadeIn(plot), FadeIn(schema()), run_time=0.45)
        bars = VGroup()
        for x in (-1, 0, 1):
            origin, top = plot.pt(x, 0), plot.pt(x, infection_flat(x))
            bar = Rectangle(width=1.27, height=top[1] - origin[1], stroke_color=YELLOW,
                            stroke_width=3, fill_color=YELLOW, fill_opacity=0.36)
            bar.move_to((origin + top) / 2)
            bars.add(bar)
        self.play(*(GrowFromEdge(bar, DOWN) for bar in bars), run_time=1.45)
        self.at("every pairing gives")
        case = label("No change", 0, 3.30, YELLOW)
        trace = filled_trace(plot, infection_flat)
        points = trace_points(plot, infection_flat)
        self.play(FadeOut(bars), FadeIn(trace), FadeIn(points), FadeIn(case), run_time=0.85)
        progress = ValueTracker(0)
        model = infection_flat
        cursor = running_marker(plot, lambda x: model(x), progress)
        self.add(cursor)
        self.play(progress.animate.set_value(1), run_time=2.25, rate_func=linear)
        self.at("In an arms race")
        self.remove(cursor)
        next_case = label("Arms race", 0, 3.30, YELLOW)
        self.play(swap(case, next_case), Transform(trace, filled_trace(plot, infection_race)),
                  Transform(points, trace_points(plot, infection_race)), run_time=2.6)
        self.at("infection falls from")
        model = infection_race
        progress.set_value(0)
        self.add(cursor)
        self.play(progress.animate.set_value(1), run_time=3.55, rate_func=linear)
        self.at("Under fluctuating selection")
        self.remove(cursor)
        final_case = label("Fluctuating selection", 0, 3.30, YELLOW)
        self.play(swap(next_case, final_case), Transform(trace, filled_trace(plot, infection_peak)),
                  Transform(points, trace_points(plot, infection_peak)), run_time=1.75)
        self.at("parasites track current")
        progress.set_value(0)
        model = infection_peak
        self.add(cursor)
        self.play(progress.animate.set_value(1), run_time=4.75, rate_func=linear)
        self.finish()


class S06PredictQ(SpokenScene):
    def construct(self):
        plot = infection_plot()
        old = filled_trace(plot, infection_peak)
        case = label("Fluctuating selection", 0, 3.30, YELLOW)
        dots = trace_points(plot, infection_peak)
        self.add(plot, old, case, dots, schema())
        self.at("Now try one")
        self.play(FadeOut(old), FadeOut(case), FadeOut(dots), run_time=0.8)
        bracket = predict_bracket(plot)
        self.at("A lab samples")
        window = ValueTracker(-1.0)
        highlight = RoundedRectangle(width=1.25, height=3.87, corner_radius=0.10, stroke_width=0,
                                     fill_color=BLUE, fill_opacity=0.48)
        highlight.add_updater(lambda mob: mob.move_to(plot.pt(window.get_value(), 0.5)))
        highlight.update()
        self.add(highlight)
        self.play(Create(VGroup(*bracket[:3])), window.animate.set_value(-0.26),
                  run_time=2.55, rate_func=linear)
        self.at("20 weeks")
        self.play(FadeIn(bracket[3]), window.animate.set_value(0.28), run_time=1.9, rate_func=linear)
        self.at("time shift assay")
        dots = trace_points(plot, infection_race)
        trace = filled_trace(plot, infection_race)
        self.play(LaggedStart(*(GrowFromCenter(d) for d in dots), lag_ratio=0.56),
                  window.animate.set_value(1), run_time=1.75, rate_func=linear)
        self.at("infection falls steadily")
        highlight.clear_updaters()
        self.play(Create(trace[1]), FadeIn(trace[0]), FadeOut(highlight), run_time=2.1)
        progress = ValueTracker(0)
        cursor = running_marker(plot, infection_race, progress)
        self.add(cursor)
        self.play(progress.animate.set_value(0.42), run_time=2.0, rate_func=linear)
        self.at("Can the lab conclude")
        self.play(FadeIn(question_card(PREDICTION, **PREDICT_CARD), shift=UP * 0.15), run_time=0.65)
        self.play(progress.animate.set_value(1), run_time=2.05, rate_func=linear)
        self.play(FadeOut(cursor), run_time=0.28)
        self.finish()


class S07PredictPause(PredictPause):
    QUESTION = PREDICTION
    CARD = PREDICT_CARD
    SECONDS = 4.5
    RING_AT = (6.03, -2.82, 0)

    def backdrop(self):
        return prediction_still()

    def construct(self):
        self.add(self.backdrop(), question_card(self.QUESTION, **self.CARD))
        ring, run = countdown(self.SECONDS, center=self.RING_AT, radius=0.53, color=YELLOW)
        ring[0].set_fill(GOLD, opacity=0.56)
        self.add(ring)
        self.play(run)


def trajectories():
    plot = Plot(box=(-5.4, 5.4, -2.64, 2.48), xr=(0, 1), yr=(0, 1),
                color=GREY, stroke=3)
    backing = Polygon(p(-5.4, -2.64), p(5.4, -2.64), p(5.4, 2.48), p(-5.4, 2.48),
                      fill_color=GLASS, fill_opacity=1, stroke_width=0)
    plot.add_to_back(backing)
    return plot


def drift_curve(x, i):
    return 0.48 + 0.062 * (i - 1) + 0.32 * (i - 1) * x + 0.11 * np.sin(x * (7 + i) + i) * x


def selection_curve(x, i):
    return 0.18 + 0.12 * i + 0.51 * x + 0.025 * np.sin(6 * x + i) * x


class S08Controls(SpokenScene):
    def construct(self):
        plot, short, dots, bracket, tag = prediction_still()
        q = question_card(PREDICTION, **PREDICT_CARD)
        self.add(plot, short, dots, bracket, tag, q)
        self.at("Not yet")
        answer = label("Not yet", 0, 3.31, TEXT, 40)
        self.play(swap(q, answer), short[0].animate.set_fill(YELLOW, opacity=0.43), run_time=0.88)
        self.at("A short record")
        self.play(FadeOut(plot.tick_labels), FadeOut(plot.ticks), FadeOut(bracket), run_time=0.48)
        expanded = infection_plot(extended=True, host_ticks=False)
        short_wave = filled_trace(expanded, infection_wave, x0=-1, x1=1)
        self.play(Transform(short, short_wave), Transform(dots, trace_points(expanded, infection_wave)),
                  run_time=1.62)
        self.at("of a wave")
        left = filled_trace(expanded, infection_wave, color=BLUE, x0=-3.68, x1=-1)
        right = filled_trace(expanded, infection_wave, color=BLUE, x0=1, x1=3.68)
        self.play(FadeIn(left[0]), Create(left[1]), FadeIn(right[0]), Create(right[1]), run_time=2.0)
        self.at("Long dense records")
        xs = np.linspace(-3.68, 3.68, 31)
        dense = trace_points(expanded, infection_wave, xs, color=TEXT, radius=0.042)
        self.play(LaggedStart(*(FadeIn(d) for d in dense), lag_ratio=0.07), FadeOut(answer), run_time=2.65)
        progress = ValueTracker(-3.5)
        scanner = always_redraw(lambda: Polygon(
            expanded.pt(progress.get_value() - 0.2, 0),
            expanded.pt(progress.get_value() + 0.2, 0),
            expanded.pt(progress.get_value() + 0.2, 1),
            expanded.pt(progress.get_value() - 0.2, 1),
            stroke_width=0, fill_color=BLUE, fill_opacity=0.52))
        self.add(scanner)
        self.play(progress.animate.set_value(3.5), run_time=1.8, rate_func=linear)
        self.at("Replicates also guard")
        self.remove(scanner)
        self.play(FadeOut(plot), FadeOut(short), FadeOut(dots), FadeOut(left), FadeOut(right),
                  FadeOut(dense), run_time=0.52)
        paths = trajectories()
        colors = (TEAL, BLUE, PURPLE)
        traces = [paths.curve(lambda x, i=i: drift_curve(x, i), color=c, width=6)
                  for i, c in enumerate(colors)]
        self.play(FadeIn(paths), run_time=0.47)
        self.at("against drift")
        drift = label("Drift", 0, 3.22, TEXT, 38)
        self.play(*(Create(t) for t in traces), FadeIn(drift), run_time=2.55)
        marks = [trace_points(paths, lambda x, i=i: drift_curve(x, i), (1,), color=c, radius=0.11)
                 for i, c in enumerate(colors)]
        self.at("Drift scatters lines")
        self.play(*(GrowFromCenter(m) for m in marks), run_time=0.55)
        self.at("while selection pushes")
        self.play(swap(drift, label("Selection", 0, 3.22, TEXT, 38)),
                  *(Transform(t, paths.curve(lambda x, i=i: selection_curve(x, i), color=colors[i], width=6))
                    for i, t in enumerate(traces)),
                  *(m.animate.move_to(paths.pt(1, selection_curve(1, i))) for i, m in enumerate(marks)),
                  run_time=2.15)
        self.finish()


def partners(x, y, host_color=TEAL, phage_color=PURPLE, scale=1):
    host = Ellipse(width=1.15, height=0.67, fill_color=host_color, fill_opacity=0.74,
                   stroke_color=host_color, stroke_width=2).move_to(p(-0.38, 0))
    phage = Triangle(fill_color=phage_color, fill_opacity=0.73, stroke_color=phage_color,
                     stroke_width=2).set_height(0.55).move_to(p(0.64, 0))
    return VGroup(host, phage).scale(scale).move_to(p(x, y))


def lock_icon(x, y):
    loop = Arc(radius=0.14, start_angle=0, angle=PI, color=TEXT, stroke_width=4)
    body = RoundedRectangle(width=0.43, height=0.28, corner_radius=0.05,
                            color=TEXT, fill_color=GLASS, fill_opacity=1, stroke_width=3)
    body.next_to(loop, DOWN, buff=-0.025)
    return VGroup(loop, body).move_to(p(x, y))


def meadow():
    hills = VGroup()
    for i, (color, base, amplitude) in enumerate(((GLASS, -0.73, 0.60), ("#36534F", -1.13, 0.52),
                                                 ("#496449", -1.46, 0.46))):
        xs = np.linspace(-1.1, 5.95, 61)
        ridge = [p(x, base + amplitude * np.cos((x - i) * (0.75 + i * 0.16))) for x in xs]
        hills.add(Polygon(p(-1.1, -2.58), *ridge, p(5.95, -2.58),
                          fill_color=color, fill_opacity=1, stroke_width=0))
    sun = Dot(p(3.75, 1.02), radius=0.68, color=GOLD)
    grasses = VGroup()
    rng = np.random.default_rng(92)
    for _ in range(32):
        x = rng.uniform(-0.96, 5.78)
        y = rng.uniform(-2.5, -2.18)
        stem = Line(p(x, y), p(x + 0.13, y + rng.uniform(0.15, 0.48)), color=GREEN, stroke_width=2)
        grasses.add(stem)
        bob(stem, amp=0.05, speed=2, seed=x * 2)
    return VGroup(sun, hills, grasses)


class S09Limits(SpokenScene):
    def construct(self):
        bench = benchtop()
        growing = VGroup(flask(-3.8, 0.95, 1.36, seed=10), flask(0, 0.95, 1.36, seed=11))
        control = flask(3.8, 0.95, 1.36, seed=12)
        room = plate(12.92, 4.85, 0, 0.50, color="#473D36", edge=GOLD)
        shared = label("Shared room", -3.8, 3.34, GOLD)
        control_tag = label("Matched control", 3.8, -1.65, GREEN)
        self.add(room, bench, growing, control)
        self.at("Matched controls")
        self.play(FadeIn(control_tag), control[0][-1].animate.set_stroke(GREEN, width=6),
                  run_time=0.65)
        self.at("shared lab or greenhouse")
        self.play(FadeIn(shared), run_time=0.4)
        self.play(room.animate.set_fill(BENCH).set_stroke(BLUE), shared.animate.set_opacity(0.45),
                  run_time=1.6)
        self.at("To separate coevolution")
        self.play(FadeOut(room), FadeOut(bench), FadeOut(growing), FadeOut(control),
                  FadeOut(shared), FadeOut(control_tag), run_time=0.55)
        panels = TwoPanel("Coevolution", "Constant host", colors=(BLUE, GREEN),
                          top=2.64, bottom=-2.65, gap=0.37, width=12.6, size=32)
        starts = [partners(x, 0.95, scale=1.65) for x in (-3.25, 3.25)]
        ends = [partners(x, -1.28, scale=1.65) for x in (-3.25, 3.25)]
        arrows = VGroup(*(arrow(p(x, 0.30), p(x, -0.59), BLUE) for x in (-3.25, 3.25)))
        self.play(FadeIn(panels), *(FadeIn(s) for s in starts), run_time=0.68)
        self.play(Create(arrows), *(TransformFromCopy(start, end, path_arc=0) for start, end in zip(starts, ends)),
                  run_time=1.25)
        for pair in starts + ends:
            bob(pair, amp=0.045, speed=2.7)
        self.at("colleagues in 2010")
        cite = source_tag("Paterson et al., 2010")
        self.play(FadeIn(cite), run_time=0.55)
        self.at("held the host")
        lock = lock_icon(2.62, -2.08)
        self.play(FadeIn(lock), ends[1][1].animate.set_color(ORANGE), run_time=3.1)
        self.at("coevolution needs heritable")
        self.play(ends[0][0].animate.set_color(GREEN), ends[0][1].animate.set_color(ORANGE),
                  run_time=3.45)
        self.at("And flasks test")
        self.play(FadeOut(panels), FadeOut(arrows), FadeOut(lock), FadeOut(cite),
                  *(FadeOut(m) for m in starts + ends), run_time=0.45)
        scenery = meadow()
        lab_flask = flask(-3.8, -0.6, 1.5, seed=10)
        self.play(FadeIn(lab_flask), FadeIn(scenery, shift=UP * 0.2), run_time=0.85)
        self.at("field communities", lead=0.4)
        self.play(lab_flask.animate.scale(0.77, about_point=p(-3.8, -2.71)),
                  FadeIn(label("Field community", 2.64, -3.07, TEXT)), run_time=1.0)
        self.finish()


def strain_row():
    return VGroup(*(flask(x, y, 0.68, seed=31 + i + row * 6) for row, y in enumerate((2.05, 0.08))
                    for i, x in enumerate(np.linspace(-5.24, 5.24, 6))))


def replay_vials():
    return VGroup(vial(-3.8, -2.33), vial(3.8, -2.33))


class S10UnlockedLenski(SpokenScene):
    def construct(self):
        shelf = archive_shelf()
        bench = benchtop()
        strains = strain_row()
        self.add(bench)
        self.at("What has this unlocked")
        self.play(LaggedStart(*(FadeIn(s, shift=UP * 0.18) for s in strains), lag_ratio=0.14), run_time=4.9)
        self.at("Lenski grew")
        citation = source_tag("Blount, Borland & Lenski, 2008")
        self.play(FadeIn(citation), run_time=0.56)
        self.at("identical Escherichia")
        species = label("12 Escherichia coli populations", 0, -2.06, TEAL)
        self.play(FadeIn(species), run_time=0.65)
        self.at("medium held glucose")
        medium = label("Glucose and citrate", 0, -2.54, TEXT)
        self.play(swap(species, medium), run_time=0.7)
        self.play(*(s[0][1].animate.set_fill(opacity=0.58) for s in strains), run_time=2.22)
        self.at("One evolved citrate")
        generation = ValueTracker(0)
        generation_display = counter("Generation {:,.0f}", generation, at=p(0, -2.53), size=36, color=TEXT)
        self.play(FadeOut(medium), run_time=0.3)
        self.add(generation_display)
        self.play(generation.animate.set_value(31500), run_time=4.15, rate_func=linear)
        specimen = strains[9]
        citrate_label = label("Citrate use", specimen.get_x(), -1.40, GOLD)
        self.play(specimen[0][1].animate.set_fill(GOLD, opacity=0.8),
                  specimen[0][3].animate.set_color(GOLD),
                  *(c.animate.set_fill(YELLOW, opacity=1) for c in specimen[1]),
                  FadeIn(citrate_label), run_time=0.6)
        self.at("Replaying frozen clones")
        vials = replay_vials()
        self.play(FadeOut(citation), FadeOut(generation_display),
                  FadeOut(strains), FadeOut(citrate_label), run_time=0.66)
        self.play(FadeIn(shelf), *(FadeIn(v, shift=UP * 0.12) for v in vials), run_time=0.45)
        titles = VGroup(label("Early clones", -3.35, 2.96), label("Later clones", 3.35, 2.96))
        # Illustrative sets show the qualitative difference without estimating a rate.
        outcomes = [VGroup(*(flask(x + dx, 0.95, 0.72, seed=i + 19)
                              for i, dx in enumerate((-1.55, 0, 1.55)))) for x in (-3.35, 3.35)]
        schematic = label("Schematic replays", 0, -1.28)
        self.play(*(TransformFromCopy(v, result) for v, result in zip(vials, outcomes)),
                  FadeIn(titles), run_time=1.3)
        self.play(FadeIn(schematic), run_time=0.3)
        self.at("evolved it more often")
        replay_note = label("Citrate use more likely", 3.35, -0.32, GOLD)
        self.play(FadeIn(replay_note),
                  *(f[0][1].animate.set_fill(GOLD, opacity=0.70) for f in outcomes[1][1:]),
                  run_time=1.35)
        self.at("earlier changes mattered")
        self.play(*(f[0][3].animate.set_color(GOLD) for f in outcomes[1][1:]), run_time=0.77)
        self.finish()


def pond_layers():
    return VGroup(*(plate(12.1, 0.53, 0, -1.19 - i * 0.59, color=c, edge=c) for i, c in enumerate(SOIL)))


def pond_surface():
    water = Polygon(p(-6.05, -0.86), p(6.05, -0.86), p(6.05, 0.40), p(-6.05, 0.40),
                    fill_color=GLASS, fill_opacity=1, stroke_width=0)
    ripples = VGroup()
    for row in range(3):
        y = -0.06 - row * 0.26
        for i, x in enumerate(np.linspace(-5.35, 5.35, 8)):
            r = ArcBetweenPoints(p(x - 0.58, y), p(x + 0.58, y), angle=0.24,
                                 color=BLUE, stroke_width=2.2, stroke_opacity=0.64)
            ripples.add(bob(r, amp=0.065, speed=2.3, seed=i + row * 3))
    return VGroup(water, ripples)


def egg(x, y):
    return Ellipse(width=0.30, height=0.22, fill_color=TEAL, fill_opacity=0.91,
                   stroke_color=TEXT, stroke_width=1.8).move_to(p(x, y))


def spore(x, y):
    return Dot(p(x, y), radius=0.094, color=PURPLE)


def dish(x, y, kind):
    base = Ellipse(width=2.37, height=1.03, stroke_color=BLUE, stroke_width=3.6,
                   fill_color=GLASS, fill_opacity=1).move_to(p(x, y))
    contents = VGroup(*(kind(x + dx, y + dy) for dx, dy in ((-0.57, -0.04), (0, 0.23), (0.56, -0.09))))
    for i, item in enumerate(contents):
        bob(item, amp=0.056, speed=2.2, seed=i * 2)
    return VGroup(base, contents)


class S11UnlockedSediment(SpokenScene):
    def construct(self):
        shelf = archive_shelf()
        items = replay_vials()
        self.add(shelf, items)
        self.at("Nature archives")
        layers = pond_layers()
        water = pond_surface()
        self.play(FadeOut(items), ReplacementTransform(shelf, layers), FadeIn(water), run_time=1.6)
        self.at("In 2007")
        cite = source_tag("Decaestecker et al., 2007")
        self.play(FadeIn(cite), run_time=0.56)
        self.at("revived dormant", lead=0.65)
        eggs = dish(-3.28, 1.27, egg)
        spores = dish(3.28, 1.27, spore)
        candidates = VGroup(*(VGroup(egg(-3.28, -1.18 - 0.59 * i), spore(3.28, -1.18 - 0.59 * i))
                              for i in range(4)))
        self.play(LaggedStart(*(FadeIn(pair) for pair in candidates), lag_ratio=0.22), run_time=1.35)
        traveler = egg(-3.28, -2.36).set_z_index(4)
        self.add(traveler)
        self.play(FadeIn(eggs[0]), FadeIn(spores[0]),
                  traveler.animate.move_to(p(-3.28, 1.27)), run_time=1.25)
        self.remove(traveler)
        self.add(eggs[1].set_z_index(4))
        self.at("water flea eggs")
        egg_name = label("Daphnia eggs", -3.28, 2.16, TEAL)
        self.play(FadeIn(egg_name), run_time=0.5)
        self.at("parasite spores")
        spore_name = label("Parasite spores", 3.28, 2.16, PURPLE)
        self.play(TransformFromCopy(candidates[2][1], spores[1]), FadeIn(spore_name), run_time=1.2)
        self.at("dated sediment layers")
        layer_names = VGroup(label("Younger", -4.93, -1.19), label("Older", -4.93, -2.96))
        self.play(FadeIn(layer_names), run_time=0.52)
        self.at("This resurrection ecology")
        pair_arrow = arrow(p(1.86, 1.28), p(-1.85, 1.28), PURPLE)
        self.play(GrowArrow(pair_arrow),
                  *(layer.animate.set_fill(interpolate_color(ManimColor(c), ManimColor(BLUE), 0.26))
                    for layer, c in zip(layers, SOIL)), run_time=2.0)
        self.at("Virulence the harm", lead=0.55)
        self.play(FadeOut(pair_arrow), run_time=0.28)
        progress = ValueTracker(0.25)
        # Qualitative gauge aligned from old layers to young.
        gauge_back = plate(0.36, 2.08, 5.29, -2.02, color=BG, edge=GREY)
        gauge = RoundedRectangle(width=0.23, height=1.78, corner_radius=0.085,
                                 fill_opacity=1, fill_color=YELLOW, stroke_width=0)
        gauge.set_z_index(1)

        def fill(mob):
            mob.stretch_to_fit_height(1.76 * progress.get_value()).move_to(
                p(5.29, -2.90 + 0.88 * progress.get_value()))

        gauge.add_updater(fill)
        fill(gauge)
        title = label("Virulence", 5.02, 0.62, YELLOW)
        # Put the labels clear of the water and sediment borders.
        schematic = label("schematic", 0, -3.54, TEXT, 28)
        self.play(FadeIn(gauge_back), FadeIn(gauge), FadeIn(title), FadeIn(schematic), run_time=0.64)
        self.play(progress.animate.set_value(0.93), run_time=3.05, rate_func=linear)
        self.finish()


def mustard(x, height, seed, curling=False):
    soil_y = -2.23
    pot = Polygon(p(x - 0.46, soil_y), p(x + 0.46, soil_y), p(x + 0.30, soil_y - 0.61),
                  p(x - 0.30, soil_y - 0.61), fill_color="#835F56", fill_opacity=1,
                  stroke_color=ORANGE, stroke_width=2.4)
    stem = Line(p(x, soil_y), p(x, soil_y + height), color=GREEN, stroke_width=4.2)
    leaves = VGroup()
    for i, fraction in enumerate((0.24, 0.44, 0.62)):
        side = (-1) ** (i + seed)
        leaf = Ellipse(width=0.53, height=0.22, fill_color=GREEN, fill_opacity=0.81, stroke_width=0)
        leaves.add(leaf.rotate(side * 0.55).move_to(p(x + side * 0.19, soil_y + fraction * height)))
    bloom = VGroup()
    if curling:
        for dx in (-0.11, 0.11):
            petal = Ellipse(width=0.13, height=0.39, fill_color=GOLD, fill_opacity=1, stroke_width=0)
            bloom.add(petal.rotate(-dx * 3).move_to(p(x + dx, soil_y + height + 0.15)))
    else:
        for a in np.pi * np.arange(4) / 2 + np.pi / 4:
            petal = Ellipse(width=0.31, height=0.17, fill_color=YELLOW, fill_opacity=1, stroke_width=0)
            bloom.add(petal.rotate(a).move_to(p(x + 0.16 * np.cos(a), soil_y + height + 0.16 * np.sin(a))))
    return VGroup(VGroup(stem, leaves, bloom), pot)


PLANT_CENTERS = (-4.22, 0, 4.22)


def plant_group(x, i, taller=False, curling=False):
    plants = [mustard(x + dx, h + (0.74 if taller else 0), i + j, curling)
              for j, (dx, h) in enumerate(((-0.64, 2.65), (0.64, 2.87)))]
    return VGroup(*plants)


class S12UnlockedPlants(SpokenScene):
    def construct(self):
        shelf = archive_shelf()
        layers = pond_layers()
        self.add(layers)
        self.at("In 2017")
        plants = [plant_group(x, i) for i, x in enumerate(PLANT_CENTERS)]
        self.play(ReplacementTransform(layers, shelf), run_time=0.6)
        self.play(FadeOut(shelf), *(FadeIn(g, shift=UP * 0.22) for g in plants), run_time=1.35)
        cite = source_tag("Gervasi & Schiestl, 2017")
        self.play(FadeIn(cite), run_time=0.55)
        self.at("pollinated replicate")
        for group in plants:
            for stem, _ in group:
                bob(stem[2], amp=0.06, speed=2.6)
        groups = [label(t, x, -3.27) for x, t in zip(PLANT_CENTERS, ("Bumblebees", "Hoverflies", "Hand"))]
        for cue, text in zip(("by bumblebees", "by hoverflies", "by hand"), groups):
            self.at(cue)
            self.play(FadeIn(text), run_time=0.52)
        self.at("was the control")
        control = label("Hand control", PLANT_CENTERS[2], -3.27, GREEN)
        self.play(swap(groups[2], control), run_time=0.58)
        self.at("Nine generations later", lead=1.5)
        elapsed = ValueTracker(0)
        display = counter("+{:.0f} generations", elapsed, at=p(0, 2.58), size=35, color=TEXT)
        self.add(display)
        self.play(elapsed.animate.set_value(9), run_time=1.35, rate_func=linear)
        self.at("at Generation")
        display.clear_updaters()
        gen = label("Generation 11", 0, 2.58, TEXT, 35)
        self.play(swap(display, gen), run_time=0.53)
        self.at("bumblebee lines were")
        for stem, _ in plants[0]:
            stem[2].clear_updaters()
        self.play(Transform(plants[0], plant_group(PLANT_CENTERS[0], 0, taller=True)), run_time=1.2)
        self.at("hoverfly lines self")
        for stem, _ in plants[1]:
            stem[2].clear_updaters()
        self.play(Transform(plants[1], plant_group(PLANT_CENTERS[1], 1, curling=True)), run_time=1.52)
        self.at("Replicates controls and")
        self.play(*(FadeOut(obj) for obj in (*plants, groups[0], groups[1], control, cite, gen)), run_time=0.65)
        shelf, samples = archive_shelf(), archive_samples()
        flasks = VGroup(*(flask(x, 0.84, 0.66, seed=i + 10) for i, x in enumerate((-5.4, -3.82, -2.24))))
        sediments = pond_layers().scale(0.24).move_to(p(0.15, 0.78))
        mustard_group = plant_group(0, 0).scale(0.53).move_to(p(3.93, 0.82))
        self.play(FadeIn(flasks), FadeIn(sediments), FadeIn(mustard_group), FadeIn(shelf), run_time=1.0)
        self.play(LaggedStart(*(FadeIn(sample, shift=DOWN * 0.34) for sample in samples), lag_ratio=0.31),
                  shelf[0].animate.set_stroke(GOLD, width=5), run_time=1.60)
        self.finish()


class S13End(EndCard):
    LINE = "Replicate populations and archived ancestors turn evolution into a repeatable test."
