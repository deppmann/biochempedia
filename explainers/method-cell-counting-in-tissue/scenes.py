"""Counting Cells Without Being Fooled.

Color map (from the patch-clamp palette): grey is tissue and structure, cyan
is neurons, amber is non-neuronal nuclei, yellow marks a sample, green is a
reference trajectory, red marks loss, teal is fluid, and gold is attribution.
"""
from bp_parts import *
from bp_style import EndCard

AMBER = "#F29E4C"
TISSUE = "#596681"
CORTEX = "#697894"
CEREBELLUM = "#7B6E96"
INK = "#3E5070"
LOSS_INK = "#382137"
LESSON = "Counting cells: stereology and the isotropic fractionator"
TITLE = "Counting Cells Without Being Fooled"
QUESTION = "Made then lost: which curve?"


def point(x, y):
    return np.array([x, y, 0.0])


def label(words, x=0, y=3.12, color=TEXT, size=34, **kwargs):
    return T(words, size, color, **kwargs).move_to(point(x, y))


def schematic():
    return scope_tag(size=28, color=TEXT)


def shape(start, segments, color, outline=GREY, opacity=1, width=3):
    path = VMobject()
    path.start_new_path(point(*start))
    for a, b, end in segments:
        path.add_cubic_bezier_curve_to(point(*a), point(*b), point(*end))
    return path.set_fill(color, opacity).set_stroke(outline, width)


def brain():
    """Lateral view, anchored identically at the hook, title and whole-brain return."""
    cortex = shape((-4.38, -0.72), [
        ((-5.35, -0.45), (-5.33, 1.13), (-4.16, 1.53)),
        ((-4.09, 2.47), (-2.95, 2.94), (-2.10, 2.64)),
        ((-1.36, 3.05), (-0.25, 2.88), (0.30, 2.48)),
        ((1.33, 2.66), (2.51, 1.92), (2.66, 1.06)),
        ((3.13, 0.27), (2.35, -0.49), (1.63, -0.46)),
        ((0.95, -0.31), (0.31, -0.54), (-0.04, -1.27)),
        ((-0.74, -2.30), (-2.07, -2.37), (-2.78, -1.84)),
        ((-3.95, -2.10), (-4.78, -1.57), (-4.38, -0.72)),
    ], CORTEX, opacity=0.72)
    hind = shape((0.11, -1.22), [
        ((0.32, -0.64), (1.10, -0.51), (1.87, -0.67)),
        ((2.77, -0.68), (3.04, -1.52), (2.45, -2.04)),
        ((1.78, -2.58), (0.18, -2.35), (0.11, -1.22)),
    ], CEREBELLUM, opacity=0.82)
    stem = shape((-0.62, -1.45), [
        ((0.13, -1.39), (0.38, -1.65), (0.40, -2.00)),
        ((0.38, -2.49), (0.70, -2.77), (0.88, -2.94)),
        ((0.56, -3.01), (0.03, -3.01), (-0.08, -2.83)),
        ((-0.36, -2.49), (-0.68, -1.97), (-0.62, -1.45)),
    ], TISSUE)
    folds = VGroup(*[
        shape(a, [(b, c, d)], BG, outline="#A5ACC0", opacity=0, width=2)
        for a, b, c, d in [
            ((-4.55, 0.90), (-3.4, 1.74), (-3.65, -0.28), (-2.73, 0.07)),
            ((-3.62, 1.84), (-3.48, 1.17), (-2.69, 1.94), (-2.55, 2.39)),
            ((-1.83, 2.39), (-1.14, 1.76), (-2.63, 1.20), (-1.8, 0.74)),
            ((-3.94, -0.59), (-3.18, -0.27), (-3.69, -1.42), (-2.8, -1.48)),
            ((-2.42, -0.97), (-1.6, -1.23), (-1.42, -0.35), (-0.7, -0.55)),
            ((-0.85, 2.36), (-1.3, 1.41), (0.54, 1.71), (0.40, 0.95)),
            ((-0.94, 0.63), (-0.22, -0.62), (0.18, 1.2), (1.54, 0.32)),
            ((0.80, 2.12), (1.52, 1.74), (1.17, 1.13), (1.96, 1.01)),
            ((0.52, -1.26), (1.24, -0.93), (1.8, -1.36), (2.44, -1.16)),
            ((0.78, -1.78), (1.46, -1.47), (1.91, -1.89), (2.38, -1.62)),
        ]
    ])
    return VGroup(stem, VGroup(hind, *folds[-2:]), VGroup(cortex, *folds[:-2]))


def brain_cells(clear_title=False):
    rng = np.random.default_rng(61)
    cells = VGroup()
    for x, y in rng.uniform([-4.55, -2.02], [2.5, 2.55], (510, 2)):
        inside = ((x + 1.15) / 3.63) ** 2 + ((y - 0.35) / 2.23) ** 2 < 0.94
        if inside and not (x > 0 and y < -0.35) and not (clear_title and -1.12 < y < 1.55):
            color = BLUE if rng.random() < 0.52 else AMBER
            dot = Dot(point(x, y), radius=rng.uniform(0.025, 0.065), color=color)
            dot.set_opacity(rng.uniform(0.45, 1))
            bob(dot, amp=0.085, speed=rng.uniform(1.25, 2.3), seed=len(cells))
            cells.add(dot)
    return cells


def tissue_slice(x=-2.95, y=0.15, seed=9):
    edge = RoundedRectangle(width=2.65, height=3.9, corner_radius=0.35, stroke_width=3,
                            stroke_color=GREY, fill_color=TISSUE, fill_opacity=1)
    rng = np.random.default_rng(seed)
    cells = VGroup(*[
        Dot(point(cx, cy), radius=rng.uniform(0.045, 0.105), color=BLUE if i % 3 else AMBER)
        for i, (cx, cy) in enumerate(rng.uniform([-1.08, -1.68], [1.08, 1.68], (77, 2)))
    ])
    return VGroup(edge, cells).move_to(point(x, y))


def serial_tissue(spacing=0.76):
    return VGroup(*(tissue_slice(-4.8 + i * spacing, 0.24 + 0.07 * i, 11 + i)
                    for i in range(7)))


def sample_frame(w, h, center):
    return Rectangle(width=w, height=h, stroke_color=YELLOW, stroke_width=4).move_to(center)


class S01Hook(SpokenScene, TitleCard):
    TITLE = TITLE
    LESSON = LESSON

    def construct(self):
        specimen, cells = brain(), brain_cells()
        self.add(specimen, cells, schematic())
        self.at("count the cells")
        question = label("How many\ncells?", 4.55, 1.05, size=43)
        self.play(FadeIn(question), run_time=0.55)
        self.at("older textbooks")
        ratio = boxed_label("10 to 1?", AMBER, size=33).move_to(point(4.55, -0.73))
        self.play(FadeIn(ratio), run_time=0.55)
        pulse(ratio.box, base=3, amp=1.6, speed=2.9)
        self.at("solid tissue")
        frame = sample_frame(1.08, 1.08, point(-3.65, 0.3))
        self.play(Create(frame), run_time=0.55)
        self.play(frame.animate.move_to(point(-1.45, 0.85)), run_time=1.04)
        self.at("one patch")
        self.play(frame.animate.move_to(point(0.72, 0.23)), run_time=1.22)
        self.finish()


class S02Title(TitleCard):
    TITLE = TITLE
    LESSON = LESSON

    def construct(self):
        specimen, cells = brain(), brain_cells(clear_title=True)
        veil = Rectangle(width=13.8, height=7.6, stroke_width=0, fill_color=BG, fill_opacity=0.76)
        title = label("Counting Cells\nWithout Being Fooled", 0, 0.32, size=56, font=TITLE_FONT)
        rule = Line(point(-1.35, -0.96), point(1.35, -0.96), color=GOLD, stroke_width=4)
        backing = Rectangle(width=9.4, height=2.50, stroke_width=0, fill_color=BG, fill_opacity=1)
        backing.move_to(point(0, 0.03))
        self.add(specimen, cells, veil, backing)
        self.play(FadeIn(title), GrowFromCenter(rule), run_time=0.63)
        self.finish()


class S03Stereology(SpokenScene):
    def construct(self):
        specimen = brain()
        block = serial_tissue(0.22)
        scope = schematic()
        self.add(specimen, scope)
        self.at("one method")
        self.play(ReplacementTransform(specimen, block), run_time=2.18)
        self.at("fix a region")
        fixed = label("Fixed tissue", -2.65, 2.92)
        self.play(FadeIn(fixed), run_time=0.46)
        self.at("cut thin serial")
        sliced = serial_tissue()
        self.play(Transform(block, sliced), FadeOut(fixed), run_time=2.05)
        self.at("systematic sampling")
        sampled = list(block[::2])
        centers = [section.get_center() + LEFT * 0.91 for section in sampled]
        frame = sample_frame(0.61, 2.26, centers[0]).set_fill(YELLOW, 0.24)
        count = ValueTracker(0)
        tally = counter("Counted: {:.0f}", count, point(4.23, 0.23), size=31)
        self.play(Create(frame), run_time=0.50)
        self.add(tally)
        observed = 0
        for i, (section, center) in enumerate(zip(sampled, centers)):
            if i:
                self.play(frame.animate.move_to(center), run_time=0.70)
            if i == 2:
                self.at("called stereology")
                name = label("Stereology", 3.95, 1.24, size=38)
                self.play(FadeIn(name), run_time=0.44)
            in_frame = [dot for dot in section[1]
                        if abs(dot.get_x() - center[0]) < 0.305 and abs(dot.get_y() - center[1]) < 1.13]
            observed += len(in_frame)
            self.play(count.animate.set_value(observed),
                      *[dot.animate.scale(1.32).set_color(YELLOW) for dot in in_frame],
                      run_time=0.69)
        self.at("sections also show")
        zoom = tissue_slice(-2.8, 0.25, seed=17).scale(1.42).set_opacity(0.47)
        self.play(FadeOut(VGroup(*block[:-1], frame, name, tally)),
                  Transform(sampled[-1], zoom), run_time=1.12)
        membrane = Ellipse(width=3.05, height=2.12, color=BLUE, stroke_width=4,
                           fill_color=BLUE, fill_opacity=0.48).move_to(point(2.78, 0.26))
        nucleus = Dot(membrane.get_center(), radius=0.53, color="#B1D9F0")
        self.play(FadeIn(VGroup(membrane, nucleus)), run_time=0.63)
        self.at("a regulated death")
        self.play(membrane.animate.scale(0.57), run_time=1.15)
        self.at("condense into")
        self.play(nucleus.animate.scale(0.40).set_color(LOSS_INK), run_time=1.25)
        self.at("called panodic")
        self.play(FadeIn(label("Pyknotic nucleus", 2.78, -1.00, size=31)), run_time=0.43)
        self.finish()


def tube():
    outer = shape((-5.46, 2.49), [
        ((-5.46, 1.12), (-5.46, -0.75), (-5.46, -1.44)),
        ((-5.44, -2.10), (-4.75, -2.66), (-3.44, -2.77)),
        ((-2.17, -2.66), (-1.47, -2.10), (-1.44, -1.44)),
        ((-1.44, -0.35), (-1.44, 1.42), (-1.44, 2.49)),
    ], BG, outline=BLUE, opacity=0, width=4)
    liquid = shape((-5.41, 1.39), [
        ((-5.41, 0.2), (-5.41, -0.70), (-5.41, -1.44)),
        ((-5.39, -2.07), (-4.72, -2.60), (-3.44, -2.71)),
        ((-2.21, -2.60), (-1.52, -2.07), (-1.49, -1.44)),
        ((-1.49, -0.70), (-1.49, 0.2), (-1.49, 1.39)),
        ((-2.76, 1.17), (-4.30, 1.54), (-5.41, 1.39)),
    ], TEAL, opacity=0.38, width=0)
    lip = Line(point(-5.65, 2.49), point(-1.25, 2.49), color=BLUE, stroke_width=5)
    return VGroup(liquid, outer, lip)


def suspension():
    rng = np.random.default_rng(25)
    dots = VGroup()
    for x, y in rng.uniform([-5.14, -2.32], [-1.79, 1.19], (113, 2)):
        if y > -1.62 or ((x + 3.44) / 1.60) ** 2 + ((y + 1.42) / 1.06) ** 2 < 1:
            d = Dot(point(x, y), radius=rng.uniform(0.037, 0.084), color="#C6D0E4")
            bob(d, amp=0.12, speed=rng.uniform(1.15, 2.5), seed=len(dots))
            dots.add(d)
    return dots


class S04Fractionator(SpokenScene):
    def construct(self):
        block, vessel, scope = serial_tissue(0.22), tube(), schematic()
        self.add(block, scope)
        self.at("slicing every")
        self.play(Transform(block, serial_tissue(0.39)), run_time=1.9)
        self.at("another method")
        self.play(block.animate.scale(0.38).move_to(point(-3.44, 2.98)),
                  FadeIn(vessel), run_time=0.61)
        self.at("dissolves the tissue")
        self.play(block.animate.move_to(point(-3.44, -0.55)), run_time=1.02)
        self.at("nuclei float free")
        cloud = suspension()
        self.play(FadeOut(block, scale=0.4), FadeIn(cloud, scale=0.34), run_time=1.52)
        self.at("this mixture is uniform")
        window = sample_frame(1.15, 0.76, point(-4.56, 0.37))
        self.play(Create(window), run_time=0.57)
        self.play(window.animate.move_to(point(-2.39, -0.91)), run_time=2.68)
        self.at("small samples")
        self.play(window.animate.move_to(point(-2.13, -0.76)), run_time=0.64)
        columns, rows = 7, 3
        frame = Rectangle(width=4.6, height=1.45, stroke_color=GREY, stroke_width=2,
                          stroke_opacity=0.7).move_to(point(3.48, -0.75))
        cell_width, cell_height = frame.width / columns, frame.height / rows
        left, bottom = frame.get_left()[0], frame.get_bottom()[1]
        grid = VGroup(frame)
        for column in range(1, columns):
            x = left + column * cell_width
            grid.add(Line(point(x, bottom), point(x, frame.get_top()[1]),
                          color=GREY, stroke_width=2, stroke_opacity=0.7))
        for row in range(1, rows):
            y = bottom + row * cell_height
            grid.add(Line(point(left, y), point(frame.get_right()[0], y),
                          color=GREY, stroke_width=2, stroke_opacity=0.7))
        pipette = Polygon(point(-0.2, 0.08), point(-0.2, -0.08), point(1.6, -0.18), point(1.6, 0.18),
                          color=BLUE, stroke_width=3, fill_color=BLUE, fill_opacity=0.45)
        pipette.move_to(point(-0.92, -0.76))
        self.play(FadeIn(grid), FadeIn(pipette), FadeOut(window), run_time=0.38)
        self.play(pipette.animate.shift(RIGHT * 3.34), run_time=1.0)
        sample = VGroup(*[
            Dot(point(left + (column + 0.5) * cell_width, bottom + (row + 0.5) * cell_height),
                radius=0.063, color="#C6D0E4")
            for row in range(rows) for column in range(columns)
        ])
        self.play(FadeOut(pipette), FadeIn(sample), run_time=0.53)
        self.at("staining separates")
        self.play(*[d.animate.set_color(BLUE if i % 2 else AMBER)
                    for dots in (cloud, sample) for i, d in enumerate(dots)], run_time=1.16)
        legend = VGroup(label("Neuronal nuclei", 3.5, 1.21, BLUE, 29),
                        label("Non-neuronal nuclei", 3.5, 0.61, AMBER, 29))
        n = ValueTracker(0)
        tally = Readout([("Sample", n.get_value, "{:.0f}", TEXT)],
                        at=point(3.5, -2.15), widest=[len(sample)], size=29)
        self.play(FadeIn(legend), FadeIn(tally), run_time=0.48)
        self.play(n.animate.set_value(len(sample)), run_time=0.72)
        self.at("the isotropic fractionator")
        self.play(FadeIn(label("Isotropic fractionator", 3.15, 2.67, size=34)), run_time=0.55)
        self.play(FadeOut(tally), run_time=0.30)
        self.play(FadeIn(label("Whole estimate = sample count\n÷ sampled fraction", 3.45, -2.37, YELLOW, 28)),
                  run_time=0.54)
        self.finish()


def slab_dots(origin, across, rise, width, span, density, radius, rng):
    """Distribute a fixed number of dots per unit area across an entire face."""
    count = round(density * width * span)
    rows = max(1, round(span * np.sqrt(density)))
    columns, extra = divmod(count, rows)
    dots = VGroup()
    for row in range(rows):
        columns_in_row = columns + (row < extra)
        row_dots = VGroup()
        for column in range(columns_in_row):
            offset_x, offset_y = rng.uniform(0.25, 0.75, 2)
            a = (column + offset_x) / columns_in_row
            b = (row + offset_y) / rows
            row_dots.add(Dot(origin + across * a + rise * b, radius=radius, color=BLUE))
        dots.add(row_dots)
    return dots


def cortical_sheet(x, width, height, depth, seed):
    """A schematic cortical slab with a fixed left edge and bottom face."""
    y = -1.25
    corner = point(x, y)
    across = RIGHT * width
    up = UP * height
    back = point(depth * 0.57, depth)
    top = Polygon(corner + up, corner + up + back, corner + up + across + back,
                  corner + up + across, color=GREY, fill_color=CORTEX, fill_opacity=0.91)
    side = Polygon(corner + across, corner + across + up, corner + across + up + back,
                   corner + across + back, color=GREY, fill_color=INK, fill_opacity=1)
    front = Polygon(corner, corner + across, corner + across + up, corner + up,
                    color=GREY, fill_color=TISSUE, fill_opacity=0.97)
    rng = np.random.default_rng(seed)
    surface = slab_dots(corner + up, across, back, width, depth, 23, 0.041, rng)
    cells = slab_dots(corner, across, up, width, height, 36, 0.052, rng)
    return VGroup(top, side, front, surface, cells)


def cortex_pair(human_width=2.15, human_height=0.78, human_depth=1.57):
    return VGroup(cortical_sheet(-5.75, 2.15, 0.78, 1.57, 18),
                  cortical_sheet(-1.15, human_width, human_height, human_depth, 32))


def area_window(x, height=0.78, depth=1.57, column=False):
    foot = point(x + 0.36, -1.25)
    up = UP * height
    side = RIGHT * 0.57
    back = point(0.25, 0.44) * (1 if column else depth / 1.57)
    face = Polygon(foot + up, foot + up + side, foot + up + side + back, foot + up + back,
                   stroke_color=YELLOW, stroke_width=4)
    if not column:
        return VGroup(face)
    section = Polygon(foot, foot + side, foot + side + up, foot + up,
                      stroke_color=YELLOW, stroke_width=4, fill_color=YELLOW, fill_opacity=0.14)
    return VGroup(face, section)


def cortex_names(mouse, human):
    return VGroup(label("Mouse", mouse[2].get_x(), -1.87, size=32),
                  label("Human", human[2].get_x(), -1.87, size=32))


class S05DensityTrap(SpokenScene):
    def construct(self):
        mouse, human = cortex_pair()
        names, scope = cortex_names(mouse, human), schematic()
        incoming = tissue_slice(-3.44, -0.20)
        self.add(incoming, scope)
        self.at("counts mislead")
        self.play(ReplacementTransform(incoming, mouse), FadeIn(human, shift=RIGHT * 0.35), run_time=1.73)
        self.play(FadeIn(names), run_time=0.5)
        self.at("density is cells")
        windows = VGroup(area_window(-5.75), area_window(-1.15))
        self.play(Create(windows), run_time=0.95)
        density = label("Density = cells per area or volume", 0, 2.84, size=33)
        self.play(FadeIn(density), run_time=0.55)
        self.play(Indicate(windows, color=YELLOW, scale_factor=1.17), run_time=1.58)
        self.at("cortex volume equals")
        rule = label("Cortex volume = height × area", 0, 2.84, size=35)
        self.play(swap(density, rule, run_time=0.78))
        self.play(Transform(windows, VGroup(area_window(-5.75, column=True),
                                            area_window(-1.15, column=True))), run_time=1.2)
        self.at("height gives a factor")
        height_factor, area_factor = 2, 1_000
        tall = cortex_pair(human_height=0.78 * height_factor)[1]
        tall_windows = VGroup(area_window(-5.75, column=True),
                              area_window(-1.15, height=1.56, column=True))
        self.play(Transform(human, tall), Transform(windows, tall_windows), run_time=1.3)
        self.at("area about 1000")
        wide = cortex_pair(5.92, 1.56, 1.93)[1]
        self.play(Transform(human, wide), names[1].animate.set_x(wide[2].get_x()), run_time=2.18)
        self.at("2 times 1000")
        factors = label(f"{height_factor} × {area_factor:,}", -1.25, -2.87, GOLD, 39)
        result = label(f"= {height_factor * area_factor:,}", 1.83, -2.87, GOLD, 39)
        self.play(FadeIn(factors), run_time=0.53)
        self.at("equals 2000")
        self.play(FadeIn(result), run_time=0.64)
        self.at("all the gain")
        final_sheet = cortex_pair(6.54, 1.56, 2.16)[1]
        self.play(Transform(human, final_sheet), names[1].animate.set_x(final_sheet[2].get_x()),
                  run_time=1.55)
        self.finish()


# Curves use the narrated landmarks or the relationships specified in the script.
# The unnumbered time courses are schematic interpolants, never extra measured points.
def ease(x, start, end):
    fraction = np.clip((x - start) / (end - start), 0, 1)
    return fraction * fraction * (3 - 2 * fraction)


def age_plot(xr=(0, 10), yr=(0, 1), right=2.7, ticks=(), title="Neuron count"):
    return Plot(box=(-5.85, right, -2.30, 2.32), xr=xr, yr=yr, xticks=ticks,
                ylabel=title, color=TEXT, size=28, label_size=30, stroke=3.5)


def area_under(plot, fn, end, color, start=None, opacity=0.43):
    start = plot.xr[0] if start is None else start
    x_values = np.linspace(start, max(start + 0.001, end), 54)
    return Polygon(plot.pt(start, plot.yr[0]), *(plot.pt(x, fn(x)) for x in x_values),
                   plot.pt(max(start + 0.001, end), plot.yr[0]),
                   stroke_width=0, fill_color=color, fill_opacity=opacity)


def sweep_plot(scene, plot, fn, tracker, color, duration, endpoint, *, start=None, shade=True):
    start = plot.xr[0] if start is None else start
    fill = always_redraw(lambda: area_under(plot, fn, tracker.get_value(), color, start)) if shade else None
    curve = plot.live_curve(fn, tracker, color=color, width=6, x0=start)
    dot = plot.dot(tracker.get_value, lambda: fn(tracker.get_value()), color=color)
    if fill is not None:
        scene.add(fill)
    scene.add(curve, dot)
    scene.play(tracker.animate.set_value(endpoint), run_time=duration, rate_func=linear)
    if fill is not None:
        fill.clear_updaters()
    curve.clear_updaters()
    dot.clear_updaters()
    return VGroup(*(m for m in (fill, curve, dot) if m is not None))


def age_window(plot, age, width=0.78):
    """Highlight the age currently being sampled."""
    height = plot.y1 - plot.y0
    x = np.clip(plot.pt(age, plot.yr[0])[0], plot.x0 + width / 2, plot.x1 - width / 2)
    return Rectangle(width=width, height=height, stroke_width=0, fill_color=YELLOW,
                     fill_opacity=0.24).move_to(point(x, plot.y0 + height / 2))


def scrub(plot, clock, width=0.78):
    return always_redraw(lambda: age_window(plot, clock.get_value(), width))


def between_curves(plot, upper, lower, start, end, color, opacity=0.37):
    ages = np.linspace(start, end, 54)
    return Polygon(*(plot.pt(x, upper(x)) for x in ages),
                   *(plot.pt(x, lower(x)) for x in ages[::-1]),
                   fill_color=color, fill_opacity=opacity, stroke_width=0)


def chick_count(day):
    # Hamburger (1975): the raw peak is just over 20,000 at 5.5–6.5 days.
    # The lesson places most loss between 6.5 and 9.5 days, to about 12,000.
    return 20_400 - 8_400 * ease(day, 6.5, 9.5)


def buns(center, occupied=6):
    x, y = center[:2]
    shelf = VGroup(*[
        Line(point(x - 1.45, y + step), point(x + 1.45, y + step), stroke_width=8, color=GREY)
        for step in (-0.74, 0.07, 0.88)
    ])
    goods = VGroup(*[
        RoundedRectangle(width=0.34, height=0.31, corner_radius=0.12, color=GOLD,
                         stroke_width=2, fill_color=GOLD, fill_opacity=0.72)
        .move_to(point(x - 1.11 + 0.44 * (i % 6), y - 0.51 + 0.81 * (i // 6)))
        for i in range(occupied)
    ])
    return VGroup(shelf, goods)


class S06SnapshotTrap(SpokenScene):
    def construct(self):
        plot = age_plot((5.5, 10), (0, 23_000), ticks=[(6, "Day 6"), (10, "Day 10")],
                        title="Chick leg motor neurons")
        tissue = tissue_slice(-2.9, 0.32).scale(1.34)
        self.add(tissue, schematic())
        self.at("time hides")
        self.play(tissue.animate.shift(LEFT * 0.60).scale(0.84), run_time=1.47)
        self.at("raw counts")
        self.play(FadeOut(tissue), FadeIn(plot), run_time=0.70)
        day = ValueTracker(5.5)
        peak = sweep_plot(self, plot, chick_count, day, BLUE, 2.00, 6)
        self.at("just over")
        above = label(">20,000", 4.65, 1.63, BLUE, 39)
        self.play(FadeIn(above), run_time=0.55)
        self.at("by about day")
        self.play(FadeOut(above), run_time=0.30)
        remainder = sweep_plot(self, plot, chick_count, day, BLUE, 1.92, 10, start=6)
        self.at("roughly")
        low = label("~12,000", 4.65, 1.63, BLUE, 39)
        self.play(FadeIn(low), run_time=0.47)
        endpoint = Rectangle(width=0.53, height=1.33, stroke_color=BLUE, stroke_width=4,
                             fill_color=BLUE, fill_opacity=0.58).move_to(point(4.65, 0.44))
        self.play(GrowFromEdge(endpoint, DOWN), run_time=0.75)
        self.at("half empty bakery shelf")
        shelf = buns(point(4.63, 0.29))
        self.play(ReplacementTransform(endpoint, shelf), FadeOut(low), run_time=1.01)
        self.at("never made")
        never = label("Never made?", 4.65, -1.05, YELLOW, 30)
        lost = label("Made then lost?", 4.65, -1.73, RED, 30)
        self.play(FadeIn(never), run_time=0.52)
        self.at("made then lost")
        self.play(FadeIn(lost), run_time=0.55)
        self.at("reliable counts")
        self.play(FadeOut(VGroup(shelf, never, lost)), run_time=0.63)
        self.remove(*peak, *remainder)
        self.add(area_under(plot, chick_count, 10, BLUE), plot.curve(chick_count, color=BLUE, width=6))
        scan = plot.dot(day.get_value, lambda: chick_count(day.get_value()), color=YELLOW)
        self.add(scrub(plot, day), scan)
        self.play(day.animate.set_value(5.5), run_time=3.0, rate_func=linear)
        self.finish()


def normal_count(age):
    return 0.33 + 0.46 * ease(age, 0, 5.1)


def made_then_lost(age):
    return normal_count(age) - 0.49 * ease(age, 4.7, 10)


def too_few_made(age):
    return 0.16 + 0.14 * ease(age, 0, 10)


def ganglion():
    plot = age_plot(ticks=[(0.70, "Earlier"), (10, "Birth")])
    baseline = VGroup(area_under(plot, normal_count, 10, GREEN, opacity=0.39),
                      plot.curve(normal_count, color=GREEN, width=6))
    normal = label("Normal", 4.63, 1.34, GREEN, 33)
    mutant = label("Mutant at birth", 4.69, -0.91, RED, 32)
    endpoint = Dot(plot.pt(10, made_then_lost(10)), radius=0.14, color=RED).set_z_index(3)
    paths = VGroup(*[
        DashedVMobject(plot.curve(fn, color=TEXT, width=5), num_dashes=24, dashed_ratio=0.52)
        for fn in (made_then_lost, too_few_made)
    ])
    return plot, baseline, normal, mutant, endpoint, paths


def prediction_card():
    return question_card(QUESTION, size=36, y=-3.31)


class S07Predict(SpokenScene):
    def construct(self):
        plot, baseline, normal, mutant, endpoint, paths = ganglion()
        self.add(plot, schematic())
        self.at("test that idea")
        self.play(FadeIn(baseline[0]), Create(baseline[1]), run_time=2.4)
        self.at("a mutant ganglion")
        self.play(FadeIn(normal), run_time=0.51)
        self.at("at birth holds")
        self.play(GrowFromCenter(endpoint), run_time=0.5)
        self.play(FadeIn(mutant), run_time=0.51)
        pulse(endpoint, base=4, amp=2.6, speed=2.8)
        endpoint.set_stroke(RED)
        self.at("far fewer neurons")
        age = ValueTracker(7.0)
        window = scrub(plot, age)
        self.add(window)
        self.play(age.animate.set_value(10), run_time=2.44, rate_func=linear)
        self.at("count serial sections")
        for path in paths:
            age.set_value(10)
            path.submobjects.reverse()
            for dash in path:
                dash.reverse_points()
            trace = LaggedStart(*[Create(dash) for dash in path], lag_ratio=0.10)
            self.play(trace, age.animate.set_value(0), run_time=1.9, rate_func=linear)
            self.remove(*path)
            self.add(path)
        self.at("were made normally")
        question = prediction_card()
        self.play(FadeIn(question), age.animate.set_value(2.6), run_time=0.85)
        self.at("how should its curve")
        self.play(age.animate.set_value(9.9), run_time=2.49, rate_func=linear)
        window.clear_updaters()
        self.play(FadeOut(window), run_time=0.30)
        endpoint.clear_updaters()
        endpoint.set_stroke(width=0)
        self.finish()


class S08Pause(NarratedScene):
    def construct(self):
        self.add(*ganglion(), schematic(), prediction_card())
        self.wait(self.narration_s)


def delayed_count(age):
    extra = 0.16 * ease(age, 3.8, 7.8) * (1 - ease(age, 9.2, 13.6))
    return normal_count(age) + extra


class S09Controls(SpokenScene):
    def construct(self):
        plot, baseline, normal, mutant, endpoint, paths = ganglion()
        scope = schematic()
        self.add(plot, baseline, normal, mutant, endpoint, paths, scope)
        self.at("early on")
        upper = plot.curve(made_then_lost, color=RED, width=6)
        loss = between_curves(plot, normal_count, made_then_lost, 4.7, 10, RED)
        self.play(FadeIn(loss), FadeOut(paths[0]), run_time=0.35)
        self.play(Create(upper), run_time=2.01)
        self.at("then drops")
        dying = VGroup(*[
            Circle(radius=0.111, stroke_width=2.5, stroke_color=RED, fill_color=LOSS_INK, fill_opacity=1)
            .move_to(plot.pt(age, made_then_lost(age))) for age in [5.9, 7.1, 8.35]
        ])
        dropping = ValueTracker(5.0)
        drop_window = scrub(plot, dropping)
        self.add(drop_window)
        self.play(LaggedStart(*[GrowFromCenter(n) for n in dying], lag_ratio=0.75),
                  dropping.animate.set_value(9.7), run_time=2.50)
        drop_window.clear_updaters()
        self.play(FadeOut(drop_window), run_time=0.35)
        self.at("if too few were made")
        low = label("Too few made", 4.67, -0.91, YELLOW, 31)
        self.play(swap(mutant, low, run_time=0.75))
        missing = between_curves(plot, normal_count, too_few_made, 0, 10, YELLOW, opacity=0.24)
        self.play(FadeIn(missing), run_time=0.63)
        self.play(FadeOut(paths[1]), FadeOut(low), FadeOut(missing), run_time=0.91)
        self.at("count across ages")
        tracer = ValueTracker(2.8)
        sample = plot.dot(tracer.get_value, lambda: made_then_lost(tracer.get_value()), color=YELLOW)
        window = scrub(plot, tracer)
        self.add(window, sample)
        self.play(tracer.animate.set_value(5.7), run_time=1.36, rate_func=linear)
        self.at("marking dividing")
        dividing = VGroup(*[
            Dot(plot.pt(age, made_then_lost(age)) + d * 0.09, radius=0.079, color=BLUE)
            for age in [1.2, 2.05] for d in [UP, DOWN]
        ])
        self.play(LaggedStart(FadeIn(dividing), Indicate(dying, color=RED, scale_factor=1.15),
                              lag_ratio=0.30), tracer.animate.set_value(9.25), run_time=2.36)
        window.clear_updaters()
        self.at("stop counting too early")
        extended = age_plot((0, 14), right=6.12, ticks=[(0.7, "Earlier"), (10, "Birth"), (13.5, "Adult")])
        self.play(FadeOut(VGroup(normal, upper, dying, dividing, endpoint, sample, loss, window)),
                  Transform(plot, extended), run_time=0.72)
        extension = extended.curve(normal_count, x0=10, color=GREEN, width=6)
        extended_fill = area_under(extended, normal_count, 14, GREEN, start=10, opacity=0.39)
        self.play(Create(extension), FadeIn(extended_fill), run_time=0.4)
        cutoff = extended.vline(8, color=YELLOW)
        delayed = extended.curve(delayed_count, x0=4, x1=8, color="#B58CD9", width=6)
        self.play(Create(cutoff), Create(delayed), run_time=0.81)
        self.at("loss that is merely delayed")
        age = ValueTracker(8)
        sweep_plot(self, extended, delayed_count, age, "#B58CD9", 2.15, 13.65, start=8, shade=False)
        callout = label("Delayed, not lasting", 3.40, 0.04, color=TEXT, size=34)
        self.play(FadeIn(callout), run_time=0.65)
        self.finish()


def composition_bars(neurons, other):
    # Mean cell counts in billions, Azevedo et al. (2009), Fig. 2.
    return VGroup(*[
        Rectangle(width=4.45 * count / 86.06, height=0.58, stroke_color=color, stroke_width=3,
                  fill_color=color, fill_opacity=0.73).align_to(point(2.02, 0), LEFT).set_y(y)
        for count, color, y in [(neurons, BLUE, 0.48), (other, AMBER, -1.03)]
    ])


class S10UnlockedGlia(SpokenScene):
    def construct(self):
        specimen, cells = brain(), brain_cells()
        self.add(specimen, cells, schematic())
        self.at("in 2009")
        study = label("Azevedo and\ncolleagues, 2009", 4.49, 2.02, GOLD, 29)
        self.play(FadeIn(study), run_time=0.65)
        for cell in cells:
            cell.clear_updaters()
        whole = VGroup(specimen, cells)
        self.play(whole.animate.scale(0.89).shift(LEFT * 0.95), run_time=3.35)
        for i, cell in enumerate(cells):
            bob(cell, amp=0.14, speed=1.7 + 0.24 * (i % 5), seed=i)
        self.at("on whole human brains")
        ratio = label("10 to 1?", 4.55, -0.68, AMBER, 41)
        self.play(FadeIn(ratio), run_time=0.85)
        self.at("instead of 10")
        strike = Line(ratio.get_left() + LEFT * 0.12, ratio.get_right() + RIGHT * 0.12,
                      color=RED, stroke_width=6)
        strike.layout_ok = "covered"
        self.play(Create(strike), run_time=0.55)
        self.play(FadeOut(VGroup(ratio, strike)), run_time=0.44)
        bars = composition_bars(86.06, 84.61)
        labels = VGroup(label("Neurons", 4.24, 1.09, BLUE, 31),
                        label("Non-neuronal cells", 4.24, -0.43, AMBER, 31))
        self.at("non neuronal cells")
        self.play(GrowFromEdge(bars[1], LEFT), FadeIn(labels[1]), run_time=1.56)
        self.at("roughly equaled")
        self.play(GrowFromEdge(bars[0], LEFT), FadeIn(labels[0]), run_time=1.42)
        self.at("glia outnumbered")
        region = label("Cerebral cortex", 4.24, 2.10, size=37)
        self.play(swap(study, region, run_time=0.62), FadeOut(cells), run_time=0.65)
        stem, hind, cortex = specimen
        self.play(Transform(bars, composition_bars(16.34, 60.84)),
                  cortex.animate.shift(UP * 0.29),
                  hind.animate.shift(DOWN * 0.30).set_fill(opacity=0).set_stroke(opacity=0.42),
                  stem.animate.set_fill(opacity=0.38).set_stroke(opacity=0.38), run_time=1.48)
        self.at("neurons far outnumbered")
        cerebellum = label("Cerebellum", 4.24, 2.10, size=37)
        self.play(swap(region, cerebellum, run_time=0.65))
        self.play(Transform(bars, composition_bars(69.03, 16.04)),
                  cortex[0].animate.set_fill(opacity=0.38).set_stroke(opacity=0.38),
                  *[fold.animate.set_stroke(opacity=0.25) for fold in cortex[1:]],
                  hind.animate.shift(RIGHT * 0.45).set_stroke(opacity=1), run_time=1.36)
        self.play(hind[0].animate.set_fill(opacity=0.90), run_time=0.34)
        self.finish()


def column_detail(x, count):
    center = point(x, 0.23)
    section = RoundedRectangle(width=0.91, height=2.42, corner_radius=0.10,
                               fill_color=TISSUE, fill_opacity=1, stroke_width=3, stroke_color=YELLOW)
    section.move_to(center)
    cells = VGroup(*[
        Dot(center + point(0.20 if i % 2 else -0.20, 0.91 - 0.36 * (i // 2)),
            radius=0.076, color=BLUE) for i in range(count)
    ])
    return VGroup(section, cells)


class S11UnlockedCortex(SpokenScene):
    def construct(self):
        mouse, human = cortex_pair()
        names, scope = cortex_names(mouse, human), schematic()
        specimen = brain()
        self.add(specimen, scope)
        self.at("in 1980")
        self.play(ReplacementTransform(specimen, VGroup(mouse, human)), run_time=1.35)
        authors = label("Rockel et al., 1980", 0, 2.84, GOLD, 32)
        self.play(FadeIn(authors), FadeIn(names), run_time=0.56)
        self.at("and in 2008")
        authors2 = label("Herculano-Houzel et al., 2008", 0, 2.84, GOLD, 32)
        self.play(swap(authors, authors2, run_time=0.76))
        self.play(human[0].animate.set_fill(BLUE, 0.36), run_time=1.12)
        self.play(human[0].animate.set_fill(CORTEX, 0.91), run_time=1.12)
        self.at("counted cortical neurons")
        columns = VGroup(area_window(-5.75, column=True), area_window(-1.15, column=True))
        self.play(Create(columns), run_time=1.05)
        mouse_column = column_detail(3.51, 7)
        human_column = column_detail(5.41, 11)
        self.play(TransformFromCopy(columns[0], mouse_column), run_time=0.82)
        self.play(TransformFromCopy(columns[1], human_column), run_time=1.14)
        self.at("under each square")
        unit = label("Neurons under 1 mm²", 0, 2.84, size=34)
        self.play(swap(authors2, unit, run_time=0.72))
        self.at("only a few")
        detail_names = VGroup(label("Mouse", 3.51, -1.37, size=29), label("Human", 5.41, -1.37, size=29))
        ratio = label("Counts differ a few-fold", 0, -2.81, YELLOW, 32)
        self.play(FadeIn(ratio), FadeIn(detail_names), run_time=0.52)
        self.play(human_column[0].animate.set_stroke(width=8), rate_func=there_and_back, run_time=1.5)
        self.at("area differs")
        self.play(FadeOut(VGroup(ratio, unit, mouse_column, human_column, detail_names)), run_time=0.4)
        wide = cortex_pair(4.5, 1.56, 1.85)[1]
        self.play(Transform(human, wide), names[1].animate.set_x(wide[2].get_x()),
                  Transform(columns[1], area_window(-1.15, height=1.56, column=True)), run_time=1.34)
        area = label("~1,000× area", 0, 2.99, GOLD, 37)
        self.play(FadeIn(area), run_time=0.59)
        self.at("extra neurons sit")
        final_sheet = cortex_pair(6.54, 1.56, 2.16)[1]
        self.play(Transform(human, final_sheet), names[1].animate.set_x(final_sheet[2].get_x()),
                  run_time=2.45)
        self.finish()


def synaptic_density(age, peak, prune_start, prune_end):
    """Relative density, with the study's age landmarks and schematic heights."""
    return 0.38 + 0.54 * ease(age, 0, peak) - 0.43 * ease(age, prune_start, prune_end)


def auditory(age):
    # Huttenlocher and Dabholkar (1997): peak near 3 months, loss ends by age 12.
    return synaptic_density(age, 0.25, 4.2, 12)


def prefrontal(age):
    # Peak after 15 months and pruning into mid-adolescence.
    return synaptic_density(age, 1.55, 6.3, 16)


def synapse_pair():
    first = Dot(point(3.41, -0.68), radius=0.22, color=BLUE)
    second = Dot(point(5.98, -0.68), radius=0.22, color=BLUE)
    fibers = VGroup(
        shape((3.58, -0.68), [((3.82, -0.34), (4.13, -0.95), (4.63, -0.68))],
              BG, outline=BLUE, opacity=0, width=5),
        shape((5.80, -0.68), [((5.49, -0.49), (5.18, -0.87), (4.84, -0.68))],
              BG, outline=BLUE, opacity=0, width=5),
    )
    contact = Dot(point(4.735, -0.68), radius=0.072, color=YELLOW)
    return VGroup(first, second, fibers, contact)


class S12UnlockedPruning(SpokenScene):
    def construct(self):
        plot = age_plot((-0.5, 17), right=2.43, ticks=[(0, "Birth"), (16.1, "Adolescence")],
                        title="Synaptic density")
        specimen = brain()
        inset = brain().scale(0.40).move_to(point(4.66, 1.28))
        self.add(specimen, schematic())
        self.at("counting across ages")
        early_axis = Line(plot.pt(plot.xr[0], 0), plot.pt(plot.xr[1], 0), color=TEXT, stroke_width=4)
        rail_age = ValueTracker(0)
        cursor = always_redraw(lambda: Triangle(color=YELLOW, fill_color=YELLOW, fill_opacity=1)
                               .scale(0.15).move_to(plot.pt(rail_age.get_value(), 0) + UP * 0.18))
        self.play(specimen.animate.scale(0.85).shift(LEFT * 0.46 + UP * 0.75), run_time=0.75)
        self.play(Create(early_axis), run_time=0.83)
        self.add(cursor)
        self.play(rail_age.animate.set_value(6.0), run_time=1.62, rate_func=linear)
        self.at("in 1997")
        citation = label("Peter Huttenlocher\nand Arun Dabholkar\n1997", 4.55, -2.07, GOLD, 29)
        self.play(FadeIn(citation), run_time=0.56)
        self.play(Transform(specimen, inset), rail_age.animate.set_value(13.8),
                  run_time=2.75)
        self.at("counted synapses")
        pair = synapse_pair().scale(2.35).move_to(point(-2.10, 0.12))
        bodies = VGroup(*pair[:2])
        self.play(FadeIn(bodies, scale=0.65), run_time=0.47)
        self.play(Create(pair[2]), run_time=0.92)
        self.play(FadeIn(pair[3]), run_time=0.36)
        self.at("the connections between")
        self.play(pair[3].animate.scale(1.6), run_time=0.81)
        self.at("in human cortex")
        cursor.clear_updaters()
        self.play(FadeOut(VGroup(pair, citation, cursor, early_axis)), run_time=0.49)
        self.play(FadeIn(plot), run_time=0.61)
        auditory_color = BLUE
        prefrontal_color = "#B58CD9"
        a_name = label("Auditory cortex", 4.63, -0.47, auditory_color, 30)
        p_name = label("Prefrontal cortex", 4.63, -1.19, prefrontal_color, 30)
        age = ValueTracker(0)
        fill = always_redraw(lambda: area_under(plot, auditory, age.get_value(), auditory_color, start=0))
        a = plot.live_curve(auditory, age, color=auditory_color, width=6, x0=0)
        p = plot.live_curve(prefrontal, age, color=prefrontal_color, width=6, x0=0)
        dot = plot.dot(age.get_value, lambda: prefrontal(age.get_value()), color=prefrontal_color)
        self.at("synaptic density peaked")
        self.add(fill, a, p, dot)
        self.play(age.animate.set_value(3.1), run_time=2.0, rate_func=linear)
        self.at("in prefrontal")
        self.play(FadeIn(p_name), age.animate.set_value(4.6), run_time=0.66)
        self.at("than in auditory")
        self.play(FadeIn(a_name), age.animate.set_value(6.4), run_time=1.22)
        self.at("with pruning")
        self.play(age.animate.set_value(13.2), run_time=2.80, rate_func=linear)
        self.at("into adolescence")
        current_sample = scrub(plot, age)
        self.add(current_sample)
        self.play(age.animate.set_value(16.7), run_time=1.7, rate_func=linear)
        self.at("measure whole tissue")
        for mob in (fill, a, p, dot):
            mob.clear_updaters()
        current_sample.clear_updaters()
        self.play(FadeOut(dot), FadeOut(current_sample), run_time=0.34)
        trace = ValueTracker(0)
        window = scrub(plot, trace)
        self.add(window)
        self.play(trace.animate.set_value(16.7), run_time=3.42, rate_func=linear)
        self.finish()


class S13End(EndCard):
    LINE = "One snapshot misleads; unbiased cell counts sample whole tissue across time."
