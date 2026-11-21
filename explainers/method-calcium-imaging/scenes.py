"""Calcium imaging teaching film, synchronized to the supplied narration."""
from bp_parts import *

# COLOR MAP (shared patch-clamp palette, assigned to this lesson's concepts):
# BLUE calcium; YELLOW electrical activity and incident light stimulus;
# GREEN fluorescence; GREY membranes and optics; PURPLE channel gate;
# ORANGE, ROSE, LAVENDER taste solutions; TEAL water; GOLD prediction; TEXT labels.
PURPLE = "#B58CD9"
ORANGE = "#F29E4C"
ROSE = "#FF88A6"
LAVENDER = "#C6B5FF"
FIELD = "#192930"
CELL_FILL = "#3B5961"
DISPLAY = "#2C414A"
GREEN_DARK = "#324F43"
WATER = TEAL
MAIN = np.array([-0.15, -0.25, 0.0])
SIDE = np.array([-3.85, -0.2, 0.0])
FIELD_CELLS = ((0, 0, 1, 0), (-3.85, 0.65, 0.78, 0.48), (3.95, 0.15, 0.85, -0.68))
QUESTION = "Separate flashes or one swell?"
SECOND_SPIKE = 2.05
START_BRIGHTNESS = 0.52


def p(x, y):
    return np.array([x, y, 0.0])


def panel(w, h, at=ORIGIN, fill=FIELD, edge=GREY, stroke=2):
    return RoundedRectangle(width=w, height=h, corner_radius=0.27,
                            stroke_color=edge, stroke_width=stroke,
                            fill_color=fill, fill_opacity=1).move_to(at)


def schematic():
    return scope_tag("schematic", size=28, color=TEXT).set_y(-3.52)


def lamp(radius, color=GREEN):
    """A soft disk with a bright core, used for individual optical signals."""
    return VGroup(*[
        Circle(radius=radius * scale, stroke_width=0, fill_color=color, fill_opacity=alpha)
        for scale, alpha in ((1, 0.16), (0.78, 0.20), (0.57, 0.29), (0.36, 0.42), (0.17, 0.72))
    ])


def neuron(angle=0):
    """The same soma and processes in the field, zoom, and chart views."""
    shape = VMobject(stroke_color=GREY, stroke_width=3.2,
                     fill_color=CELL_FILL, fill_opacity=1)
    shape.set_points_smoothly([
        p(-0.52, 0.55), p(-0.83, 1.04), p(-1.20, 1.35), p(-0.81, 1.20),
        p(-0.25, 0.76), p(0.18, 0.79), p(0.36, 1.23), p(0.55, 1.65),
        p(0.48, 1.12), p(0.58, 0.69), p(0.87, 0.46), p(1.37, 0.50),
        p(1.02, 0.30), p(0.76, 0.00), p(0.54, -0.55), p(0.36, -1.26),
        p(0.46, -1.87), p(0.24, -1.47), p(0.12, -0.77), p(-0.31, -0.64),
        p(-0.66, -0.45), p(-1.12, -0.62), p(-1.42, -0.89), p(-1.19, -0.53),
        p(-0.71, -0.22), p(-0.70, 0.20), p(-0.52, 0.55),
    ])
    shape.rotate(angle, about_point=ORIGIN)
    glow = lamp(0.67)
    return VGroup(shape, glow)


def set_glow(glow, strength):
    for part, opacity in zip(glow, (0.16, 0.20, 0.29, 0.42, 0.72)):
        part.set_fill(opacity=opacity * float(np.clip(strength, 0, 1.55)))


def single_cell(at=MAIN, scale=1.46, strength=0.23):
    cell = neuron().scale(scale, about_point=ORIGIN).shift(at)
    set_glow(cell[1], strength)
    return cell


def microscope_back(narrow=False, clock=None):
    """A slow sweep of focal illumination in the microscope's specimen plane."""
    if narrow:
        x, y, w, h, radius, span = -3.98, -0.09, 4.8, 5.75, 1.53, 0.76
    else:
        x, y, w, h, radius, span = 0, -0.12, 12.45, 6.08, 1.89, 3.84
    housing = panel(w, h, p(x, y), edge="#55727B")
    aperture = VGroup(*[
        Circle(radius=radius * scale, stroke_width=0, fill_color="#8AA8A5",
               fill_opacity=0.035 + 0.038 * (1 - scale))
        for scale in np.linspace(1.0, 0.20, 15)
    ])
    aperture.phase = 0.0

    def scan(m, dt):
        m.phase += dt
        time = m.phase if clock is None else clock.get_value()
        phase = TAU * time / (4.0 if narrow else 6.5) - PI / 2
        m.move_to(p(x + span * np.sin(phase), y + 0.79 * np.cos(phase)))

    aperture.add_updater(scan, call_updater=True)
    return VGroup(housing, aperture)


def field(centre_scale=1.43, other_opacity=1, strengths=(0.22, 0.22, 0.22)):
    """One specimen field, with a fixed soma landmark at MAIN."""
    back = microscope_back()
    cells = VGroup()
    for (x, y, scale, angle), strength in zip(FIELD_CELLS, strengths):
        cell = neuron(angle).scale(scale * centre_scale, about_point=ORIGIN).shift(MAIN + p(x, y))
        set_glow(cell[1], strength)
        if x:
            cell.set_opacity(other_opacity)
            set_glow(cell[1], strength * other_opacity)
            cell[0].set_fill(opacity=other_opacity)
        cells.add(cell)
    return back, cells


def light_motion(glow, tracker, fn):
    glow.add_updater(lambda m: set_glow(m, fn(tracker.get_value())), call_updater=True)


def calcium_response(t, spikes=(1.15,)):
    """Schematic first-order rise/decay indicator response to electrical impulses.

    A calcium transient decays exponentially. A slower optical indicator integrates
    that transient with its own first-order response. For the two-spike comparison
    the two normalized responses add, with no fitted times or measured amplitudes.
    """
    rise, decay = 0.24, 1.22
    peak = np.log(decay / rise) / (1 / rise - 1 / decay)
    normalizer = np.exp(-peak / decay) - np.exp(-peak / rise)
    offsets = [max(0.0, t - spike) for spike in spikes]
    return sum(np.exp(-u / decay) - np.exp(-u / rise) for u in offsets) / normalizer


def electrical(t):
    return max(np.exp(-0.5 * ((t - spike) / 0.045) ** 2)
               for spike in (1.15, SECOND_SPIKE))


def current_brightness(t):
    return START_BRIGHTNESS + 0.74 * calcium_response(t)


def relative_light(t):
    return (current_brightness(t) - START_BRIGHTNESS) / START_BRIGHTNESS


def overlapping_light(t):
    return calcium_response(t, (1.15, SECOND_SPIKE))


def sweep(scene, tracker, end, seconds):
    scene.play(tracker.animate.set_value(end), run_time=seconds, rate_func=linear)


def drifting_ions():
    return VGroup(*[Dot(MAIN + p(x, y), radius=0.115, color=BLUE)
                    for x, y in ((-0.48, 0.28), (-0.25, 0.67), (0.07, 0.43), (0.51, 0.15), (0.28, -0.29))])


def continue_ions(ions, phase=0):
    for i, dot in enumerate(ions):
        origin = dot.get_center().copy()
        dot.add_updater(lambda m, i=i, origin=origin: m.move_to(
            origin + p(0.25 * np.sin(m.drift_time * 1.28 + i),
                       0.21 * np.sin(m.drift_time * 1.47 + i * 1.9))))
        dot.drift_time = phase

        def advance(m, dt):
            m.drift_time += dt

        dot.add_updater(advance)


class S01Hook(SpokenScene):
    def construct(self):
        back, cells = field(strengths=(0, 0, 0))
        self.add(back, cells, schematic())
        self.at("which of these")
        self.at("but watch what")
        self.at("cells contain a protein")
        self.play(*[UpdateFromAlphaFunc(cell[1], lambda m, a: set_glow(m, 0.4 * a))
                    for cell in cells], run_time=1.75)
        self.at("brightly it glows")
        self.play(UpdateFromAlphaFunc(cells[0][1], lambda m, a: set_glow(m, 0.4 + 1.13 * a)),
                  run_time=1.4)
        self.at("now there is")
        self.play(UpdateFromAlphaFunc(cells[0][1], lambda m, a: set_glow(m, 1.53 - 0.22 * a)),
                  run_time=2.1)
        self.finish()


class S02Title(TitleCard):
    LESSON = "Calcium imaging, photometry and optical recording of activity"
    TITLE = "Watching Neurons Light Up"

    def construct(self):
        back, cells = field(strengths=(1.31, 0.4, 0.4))
        title = T(self.TITLE, 49, font=TITLE_FONT)
        title.move_to(p(0, 3.37))
        self.add(back, cells, schematic())
        self.play(FadeIn(title), run_time=0.27)
        self.play(Transform(cells[0], single_cell(scale=1.46, strength=0.96)),
                  FadeOut(cells[1]), FadeOut(cells[2]), run_time=1.36)
        self.play(FadeOut(title), run_time=0.27)


class S03Calcium(SpokenScene):
    def construct(self):
        back, _ = field()
        cell = single_cell(strength=0.96)
        center = MAIN + p(-0.85, 1.0)
        gate = Line(center, center + RIGHT * 0.49, color=PURPLE, stroke_width=12)
        pulse_path = VMobject()
        pulse_path.set_points_smoothly([MAIN + p(-1.8, -0.92), MAIN + p(-1.13, -0.31),
                                        MAIN + p(-1.02, 0.36), center])
        flash = lamp(0.35, YELLOW).move_to(pulse_path.get_start())
        ions = drifting_ions()
        outside = [MAIN + p(-1.88 + 0.24 * i, 1.58 + 0.16 * (i % 2)) for i in range(len(ions))]
        incoming = VGroup(*[Dot(q, radius=0.115, color=BLUE) for q in outside])
        self.add(back, cell, schematic())
        self.at("start with that cell")
        self.play(Transform(cell, single_cell(scale=1.50, strength=0.41)), run_time=2.2)
        self.at("an electrical pulse")
        self.add(flash)
        self.play(MoveAlongPath(flash, pulse_path), run_time=1.57, rate_func=linear)
        self.at("opens channels")
        self.play(FadeIn(gate), run_time=0.28)
        self.play(Rotate(gate, 1.03, about_point=center), FadeOut(flash), run_time=0.72)
        self.at("which are gates")
        self.play(FadeIn(incoming), run_time=0.43)
        self.at("let calcium enter")
        paths = []
        for dot, target in zip(incoming, ions):
            path = VMobject()
            path.set_points_smoothly([dot.get_center(), center + p(0.29, 0.07), target.get_center()])
            paths.append(MoveAlongPath(dot, path))
        self.play(LaggedStart(*paths, lag_ratio=0.15), run_time=2.12)
        self.at("calcium inside the cell")
        self.remove(*incoming)
        self.add(ions)
        continue_ions(ions)
        calcium = T("Calcium", 34, BLUE).move_to(p(3.43, 0.48))
        self.play(Rotate(gate, -1.03, about_point=center), FadeIn(calcium), run_time=0.62)
        self.at("stays raised")
        self.play(FadeOut(gate), UpdateFromAlphaFunc(cell[1], lambda m, a: set_glow(m, 0.41 - 0.16 * a)),
                  run_time=2.57)
        self.play(FadeOut(calcium), run_time=0.27)
        self.finish()


class S04Afterglow(NarratedScene):
    def construct(self):
        back, _ = field()
        cell = single_cell(scale=1.50, strength=0.25)
        ions = drifting_ions()
        continue_ions(ions, phase=5.4)
        self.add(back, cell, ions, schematic())
        self.play(UpdateFromAlphaFunc(cell[1], lambda m, a: set_glow(m, 0.25 + 0.29 * a)),
                  run_time=3.65)
        self.play(FadeOut(cell[0]), FadeOut(ions),
                  cell[1].animate.scale(1.88, about_point=MAIN), run_time=2.35)


def indicator(closed=False):
    """Magnified light source and sliding shutter, drawn as an instrument icon."""
    chamber = panel(5.9, 4.25, MAIN, fill=GREEN_DARK, edge=GREEN, stroke=3)
    spot = lamp(2.24).move_to(MAIN)
    set_glow(spot, 1.52 if closed else 0.54)
    # The inlet is on the right. The shutter slides vertically across it.
    inlet_y = 0.15
    inlet = VGroup(Line(p(2.8, inlet_y + 0.46), p(4.25, inlet_y + 0.46), color=GREY, stroke_width=6),
                   Line(p(2.8, inlet_y - 0.46), p(4.25, inlet_y - 0.46), color=GREY, stroke_width=6))
    shutter = RoundedRectangle(width=0.34, height=1.24, corner_radius=0.14,
                               fill_color=PURPLE, fill_opacity=1, stroke_width=0)
    shutter.move_to(p(3.05, inlet_y if closed else inlet_y + 1.22))
    return chamber, spot, inlet, shutter


class S05Indicator(SpokenScene):
    def construct(self):
        back, _ = field()
        chamber, spot, inlet, shutter = indicator()
        water = VGroup(*[Dot(p(3.48 + 0.38 * i, 0.15 + 0.13 * (-1) ** i),
                             radius=0.09, color=WATER) for i in range(5)])
        phase = ValueTracker(0)
        for i, dot in enumerate(water):
            def drift(m, i=i):
                travel = phase.get_value()
                x = 1.45 + (i * 0.65 - travel) % 3.97
                if shutter.get_y() < 0.72:
                    x = max(3.37 + 0.12 * (i % 3), x)
                m.move_to(p(x, 0.15 + 0.16 * np.sin(i + 1.9 * travel)))
            dot.add_updater(drift)
        label = T("GCaMP", 35, GREEN).move_to(p(0, 2.68))
        ion = Dot(p(1.9, 1.97), radius=0.17, color=BLUE)
        self.add(back, spot, schematic())
        self.at("the protein that")
        spot.set_z_index(1)
        self.play(FadeIn(chamber), FadeIn(inlet), FadeIn(shutter), run_time=1.32)
        self.add(water)
        sweep(self, phase, 0.8, 1.76)
        self.at("indicator called gcamp")
        self.play(FadeIn(label), phase.animate.set_value(1.32), run_time=0.65)
        self.at("when calcium binds")
        self.play(FadeIn(ion), run_time=0.3)
        self.play(ion.animate.move_to(p(2.74, 1.37)), phase.animate.set_value(1.76), run_time=1.14)
        self.at("protein closes a gap")
        self.play(shutter.animate.shift(DOWN * 1.22), ion.animate.shift(DOWN * 1.22),
                  phase.animate.set_value(2.14), run_time=1.48)
        self.at("keeps water away")
        water_label = T("Water", 32, WATER).move_to(p(4.52, -0.71))
        self.play(FadeIn(water_label), phase.animate.set_value(2.51), run_time=0.61)
        sweep(self, phase, 3.7, 2.25)
        self.at("protein shines brighter")
        self.play(UpdateFromAlphaFunc(spot, lambda m, a: set_glow(m, 0.54 + 0.98 * a)),
                  phase.animate.set_value(4.25), run_time=1.22)
        self.finish()


def scope_cell(strength=0.32, focus_clock=None):
    """Neuron and sampling window, with unchanged chart-view coordinates."""
    cell = single_cell(SIDE, scale=1.44, strength=strength)
    back = microscope_back(narrow=True, clock=focus_clock)
    pixel = RoundedRectangle(width=0.9, height=0.9, corner_radius=0.08,
                             stroke_color=GREEN, stroke_width=3).move_to(SIDE)
    return VGroup(back, cell, pixel), cell[1]


def display():
    return panel(7.1, 5.75, p(2.62, -0.09), fill=DISPLAY, edge="#55727B")


def brightness_plot(relative):
    return Plot(box=(-0.45, 5.78, -1.88, 1.84), xr=(0, 7.6),
                yr=(0, 1.65 if relative else 1.40), color=GREY, stroke=2.4)


def cursor(plot, t, lo, hi):
    def build():
        x = plot.pt(t.get_value(), 0)[0]
        return Line(p(x, lo), p(x, hi), color=TEXT, stroke_width=2.7, stroke_opacity=0.73)
    return always_redraw(build)


def formula(subtraction_only=False):
    numerator = T("Current − Start" if subtraction_only else "(Current − Start)", 34, GREEN)
    numerator.move_to(p(2.7, 2.33))
    if subtraction_only:
        return numerator
    bar = Line(p(0.88, 1.99), p(4.52, 1.99), color=TEXT, stroke_width=2)
    denominator = T("Start", 31, TEXT).move_to(p(2.7, 1.66))
    return VGroup(numerator, bar, denominator)


def difference_bracket(plot, time):
    # At a fixed response sample; place the bracket clear of the curve.
    x = plot.pt(time, 0)[0] + 0.54
    y0 = plot.pt(0, START_BRIGHTNESS)[1]
    y1 = plot.pt(0, current_brightness(time))[1]
    return VGroup(Line(p(x, y0), p(x, y1), color=GREEN, stroke_width=4),
                  *[Line(p(x - 0.13, y), p(x + 0.13, y), color=GREEN, stroke_width=4) for y in (y0, y1)])


class S06Measure(SpokenScene):
    def construct(self):
        chamber, spot, inlet, shutter = indicator(closed=True)
        back, _ = field()
        view, glow = scope_cell()
        board, plot = display(), brightness_plot(relative=False)
        t = ValueTracker(0)
        start = plot.hline(START_BRIGHTNESS, color=TEXT)
        start_label = T("Start", 30).move_to(p(4.95, -0.20))
        trace = plot.live_curve(current_brightness, t, color=GREEN, width=6)
        self.add(back, chamber, spot, inlet, shutter, schematic())
        self.at("calcium imaging follows")
        self.play(FadeOut(chamber), FadeOut(inlet), FadeOut(shutter), FadeOut(spot),
                  FadeOut(back), FadeIn(view[0]), FadeIn(view[1]), run_time=2.68)
        self.at("by measuring the light")
        self.play(Create(view[2]), run_time=0.58)
        self.play(FadeIn(board), Create(plot), run_time=1.25)
        self.add(trace)
        light_motion(glow, t, lambda x: 0.35 + 0.78 * calcium_response(x))
        sweep(self, t, 0.62, 1.76)
        self.at("first measure the brightness")
        self.play(Create(start), run_time=0.56)
        self.play(FadeIn(start_label), run_time=0.42)
        sweep(self, t, 1.05, 1.48)
        self.at("subtract that starting")
        sweep(self, t, 1.65, 0.80)
        bracket = difference_bracket(plot, 1.65)
        current_label = T("Current", 30, GREEN).move_to(p(4.95, 1.48))
        self.play(Create(bracket), FadeIn(current_label), run_time=0.46)
        num = formula(subtraction_only=True)
        self.play(FadeIn(num), run_time=0.47)
        self.at("then divide the difference")
        eq = formula()
        self.play(bracket.animate.scale(0.32).move_to(p(0.48, 2.31)),
                  FadeOut(current_label), FadeOut(start_label), run_time=0.62)
        self.play(swap(num, eq), FadeOut(bracket), run_time=0.82)
        self.finish()


def relative_view(t, scanning=True):
    view, glow = scope_cell()
    board, plot = display(), brightness_plot(relative=True)
    zero = T("No change (0)", 28).move_to(p(2.7, -2.19))
    curve = plot.live_curve(relative_light, t, color=GREEN, width=6)
    scan = cursor(plot, t, -1.86, 1.74)
    marker = plot.dot(t.get_value, lambda: relative_light(t.get_value()), color=GREEN, ring=GREEN, radius=0.085)
    light_motion(glow, t, lambda x: 0.35 + 0.9 * calcium_response(x))
    return view, board, plot, zero, curve, VGroup(scan, marker) if scanning else VGroup()


class S07Trace(SpokenScene):
    def construct(self):
        t = ValueTracker(0.12)
        view, board, plot, zero, curve, scan = relative_view(t)
        eq = formula()
        raw_plot = brightness_plot(relative=False)
        previous = raw_plot.curve(current_brightness, x1=1.65, color=GREEN, width=6)
        start = raw_plot.hline(START_BRIGHTNESS, color=TEXT)
        header = T("Relative brightness change", 31, GREEN).move_to(p(2.7, 2.33))
        self.add(view, board, plot, eq, previous, start, schematic())
        self.at("the trace now shows")
        self.play(FadeOut(previous), FadeOut(start), run_time=0.44)
        self.play(swap(eq, header), FadeIn(zero), run_time=1.15)
        self.add(curve, scan)
        sweep(self, t, 1.1, 3.28)
        self.at("as the cell brightens")
        sweep(self, t, 1.65, 3.84)
        self.at("as the glow fades")
        sweep(self, t, 3.12, 3.23)
        self.finish()


class S08Baseline(NarratedScene):
    def construct(self):
        t = ValueTracker(3.12)
        view, board, plot, zero, curve, scan = relative_view(t)
        header = T("Relative brightness change", 31, GREEN).move_to(p(2.7, 2.33))
        self.add(view, board, plot, zero, curve, scan, header, schematic())
        sweep(self, t, 7.4, 4.31)
        back, cells = field(strengths=(0.35, 0.22, 0.22))
        self.play(FadeOut(zero), FadeOut(header), run_time=0.25)
        self.play(FadeOut(view), FadeOut(board), FadeOut(plot), FadeOut(curve),
                  FadeOut(scan), FadeIn(back), FadeIn(cells), run_time=0.91)


def collector():
    """Fibre above the original field, with one shared optical output."""
    tip = p(0.0, 1.52)
    body = Polygon(p(-0.46, 1.63), p(0.46, 1.63), p(0.64, 2.75), p(-0.64, 2.75),
                   stroke_color=GREY, stroke_width=3, fill_color=DISPLAY, fill_opacity=1)
    face = Ellipse(width=0.96, height=0.28, stroke_color=GREY, stroke_width=3,
                   fill_color=GREEN_DARK, fill_opacity=1).move_to(tip)
    output = lamp(0.48).move_to(p(0, 2.23))
    return VGroup(body, face, output), output, tip


def light_paths(cells, tip, phase):
    paths, photons = VGroup(), VGroup()
    for i, cell in enumerate(cells):
        path = Line(cell[1].get_center() + UP * 0.37, tip, color=GREEN, stroke_width=3.5,
                    stroke_opacity=0.72)
        paths.add(path)
        packet = lamp(0.29)
        packet.add_updater(lambda m, i=i, path=path: m.move_to(
            path.point_from_proportion((phase.get_value() + i * 0.29) % 1)),
            call_updater=True)
        photons.add(packet)
    return paths, photons


def pooled_field(phase):
    back, cells = field(strengths=(0.89, 0.68, 0.77))
    fibre, output, tip = collector()
    paths, photons = light_paths(cells, tip, phase)
    light_motion(output, phase, lambda x: 0.87 + 0.25 * np.sin(x * TAU))
    return back, cells, fibre, paths, photons


class S09Collect(SpokenScene):
    def construct(self):
        phase = ValueTracker(0)
        back, cells, fibre, paths, photons = pooled_field(phase)
        for cell, strength in zip(cells, (0.35, 0.22, 0.22)):
            set_glow(cell[1], strength)
        boxes = VGroup(*[RoundedRectangle(width=1.22, height=1.22, corner_radius=0.12,
                                         stroke_color=GREEN, stroke_width=2.6).move_to(cell[1])
                         for cell in cells])
        self.add(back, cells, schematic())
        self.at("a microscope can")
        self.play(LaggedStart(*[Create(box) for box in boxes], lag_ratio=0.5), run_time=1.96)
        for i, target in enumerate((0.89, 0.68, 0.77)):
            glow = cells[i][1]
            start = (0.35, 0.22, 0.22)[i]
            self.play(UpdateFromAlphaFunc(glow, lambda m, a: set_glow(m, interpolate(start, target, a))),
                      run_time=1.32)
        self.at("an optical fiber")
        self.play(FadeOut(boxes), FadeIn(fibre, shift=RIGHT * 1.12), run_time=0.89)
        self.at("can collect light")
        self.play(LaggedStart(*[Create(path) for path in paths], lag_ratio=0.35), run_time=1.84)
        self.add(photons)
        sweep(self, phase, 0.78, 2.1)
        self.at("that shared readout")
        label = T("Fibre photometry", 32, GREEN).move_to(p(3.42, 2.54))
        self.play(FadeIn(label), phase.animate.set_value(1.18), run_time=0.63)
        sweep(self, phase, 2.1, 2.23)
        self.finish()


class S10Pool(NarratedScene):
    def construct(self):
        phase = ValueTracker(2.1)
        back, cells, fibre, paths, photons = pooled_field(phase)
        label = T("Fibre photometry", 32, GREEN).move_to(p(3.42, 2.54))
        self.add(back, paths, cells, fibre, photons, label, schematic())
        sweep(self, phase, 3.5, 3.52)
        self.play(FadeOut(photons), FadeOut(paths), FadeOut(fibre, shift=LEFT * 0.76), FadeOut(label),
                  FadeOut(cells[1]), FadeOut(cells[2]),
                  Transform(cells[0], single_cell(scale=1.46, strength=0.42)), run_time=1.95)


def aligned(t, fn=overlapping_light, focus_clock=None):
    """Both recordings, using the same time scale, cursor, and sampled cell."""
    view, glow = scope_cell(focus_clock=focus_clock)
    board = display()
    upper = Plot(box=(-0.45, 5.78, 0.89, 2.18), xr=(0, 7.6), yr=(0, 1.2), stroke=2.4)
    lower = Plot(box=(-0.45, 5.78, -2.01, 0.17), xr=(0, 7.6), yr=(0, 1.80), stroke=2.4)
    spikes = upper.curve(electrical, color=YELLOW, width=5, n=480)
    trace = lower.live_curve(fn, t, color=GREEN, width=6)
    scan = VGroup(cursor(lower, t, -2.00, 0.17), cursor(upper, t, 0.88, 2.18))
    electrical_label = T("Electrical activity", 28, YELLOW).move_to(p(2.85, 2.48))
    optical_label = T("Fluorescence", 28, GREEN).move_to(p(2.85, 0.52))
    light_motion(glow, t, lambda x: 0.35 + 0.88 * fn(x))
    return view, board, upper, lower, spikes, trace, scan, electrical_label, optical_label


def mask_remainder(lower):
    left = lower.pt(SECOND_SPIKE, 0)[0] + 0.12
    right = 5.77
    cover = panel(right - left, 1.86, p((left + right) / 2, -0.87),
                  fill=FIELD, edge=GOLD, stroke=2.5)
    mark = T("?", 50, GOLD).move_to(cover)
    return VGroup(cover, mark)


def prediction_card():
    return question_card(QUESTION, y=-3.36, size=35)


def prediction_frame():
    t = ValueTracker(SECOND_SPIKE)
    focus = ValueTracker(3.0)
    view, board, upper, lower, spikes, trace, scan, electric_label, optical_label = aligned(
        t, calcium_response, focus_clock=focus)
    return VGroup(view, board, upper, lower, spikes, trace, scan,
                  electric_label, optical_label, mask_remainder(lower), prediction_card(), schematic())


class S11Predict(SpokenScene):
    def construct(self):
        t = ValueTracker(0.1)
        focus = ValueTracker(-6.5)
        view, board, upper, lower, spikes, trace, scan, electric_label, optical_label = aligned(
            t, calcium_response, focus_clock=focus)
        back, _ = field()
        cell = single_cell(strength=0.42)
        self.add(back, cell, schematic())
        self.at("now return to one cell")
        self.play(FadeOut(back), FadeIn(view[0]), Transform(cell, view[1]), run_time=0.93)
        self.remove(cell)
        self.add(view[1])
        self.play(Create(view[2]), FadeIn(board), Create(upper), Create(lower), run_time=0.48)
        self.play(Create(spikes), FadeIn(electric_label), run_time=0.43)
        self.at("watch it fire again")
        # Catch the first pulse and follow only its optical response.
        self.add(trace, scan)
        self.play(FadeIn(optical_label), t.animate.set_value(0.9), run_time=0.65)
        self.at("calcium signal is still fading")
        self.play(t.animate.set_value(1.74), focus.animate.set_value(-3.3), run_time=2.3, rate_func=linear)
        self.play(FadeIn(mask_remainder(lower)), t.animate.set_value(1.84), run_time=0.57)
        self.at("two separate flashes")
        self.play(FadeIn(prediction_card()), t.animate.set_value(1.92),
                  focus.animate.set_value(-2.0), run_time=0.76)
        self.at("responses run together")
        self.play(t.animate.set_value(SECOND_SPIKE), focus.animate.set_value(3.0),
                  run_time=self.narration_s + 0.38 - self.elapsed(), rate_func=linear)
        self.finish()


class S12Think(Scene):
    def construct(self):
        self.camera.background_color = BG
        self.add(prediction_frame())
        self.wait(float(os.environ["KX_DURATION"]))


class S13Overlap(SpokenScene):
    def construct(self):
        t = ValueTracker(SECOND_SPIKE)
        focus = ValueTracker(3.0)
        view, board, upper, lower, spikes, trace, scan, electric_label, optical_label = aligned(
            t, focus_clock=focus)
        mask = mask_remainder(lower)
        question = prediction_card()
        self.add(view, board, upper, lower, spikes, trace, scan, electric_label, optical_label,
                 mask, question, schematic())
        self.at("the responses can run")
        self.play(FadeOut(question), FadeOut(mask), focus.animate.set_value(3.82), run_time=0.55)
        self.play(t.animate.set_value(3.35), focus.animate.set_value(6.05), run_time=2.34, rate_func=linear)
        self.at("the indicator brightens")
        # Replay from just before the first spike to compare the time courses.
        self.play(t.animate.set_value(0.9), run_time=0.65)
        self.play(t.animate.set_value(1.93), focus.animate.set_value(10.07), run_time=4.52, rate_func=linear)
        self.at("the next spike can add")
        self.play(t.animate.set_value(3.25), focus.animate.set_value(14.22), run_time=4.08, rate_func=linear)
        self.at("a single swell")
        self.play(t.animate.set_value(6.1), focus.animate.set_value(17.4), run_time=3.25, rate_func=linear)
        self.finish()


def recording_optics():
    # Upper objective and diagonal recording lead directed to the same cell.
    lens = VGroup(
        RoundedRectangle(width=1.22, height=0.57, corner_radius=0.13, stroke_color=GREY,
                         stroke_width=3, fill_color=DISPLAY, fill_opacity=1).move_to(p(-4.74, 2.05)),
        Ellipse(width=1.04, height=0.24, color=GREEN, stroke_width=3).move_to(p(-4.74, 1.76)),
        Line(p(-4.74, 1.58), p(-4.08, 0.42), color=GREEN, stroke_width=3),
    )
    lead = VGroup(Line(p(-2.18, 1.08), p(-3.59, 0.21), color=GREY, stroke_width=11),
                  Line(p(-3.59, 0.21), p(-3.83, 0.07), color=YELLOW, stroke_width=3))
    return lens, lead


def recorded(t):
    view, board, upper, lower, spikes, trace, scan, electric_label, optical_label = aligned(t)
    lens, lead = recording_optics()
    path_electric = VMobject(stroke_color=YELLOW, stroke_width=2.7)
    path_electric.set_points_smoothly([p(-2.19, 1.08), p(-1.65, 1.36), p(-1.22, 1.53), p(-0.65, 1.53)])
    path_light = VMobject(stroke_color=GREEN, stroke_width=2.7)
    path_light.set_points_smoothly([p(-4.24, 1.83), p(-3.49, 1.54), p(-2.55, -0.42),
                                   p(-1.49, -0.96), p(-0.65, -0.96)])
    return (view, board, upper, lower, spikes, trace, scan, electric_label, optical_label), (lens, lead, path_electric, path_light)


class S14Check(SpokenScene):
    def construct(self):
        t = ValueTracker(6.1)
        graph, (lens, lead, path_electric, path_light) = recorded(t)
        self.add(*graph, schematic())
        self.at("to check which spikes")
        self.play(FadeIn(lens), t.animate.set_value(7.25), run_time=2.67)
        self.at("record the cell's electrical")
        self.play(FadeIn(lead, shift=UR * 0.56), run_time=0.61)
        self.play(Create(path_electric), run_time=1.08)
        self.at("while you film it")
        self.play(Create(path_light), run_time=1.14)
        self.at("line up both records")
        self.play(t.animate.set_value(0.26), run_time=0.91)
        sweep(self, t, 1.32, 1.77)
        self.at("that comparison tells you")
        sweep(self, t, 5.35, 5.15)
        self.finish()


def specimen(kind, strengths=None):
    """The microscope housing now holds a retina or a ganglion field."""
    back = microscope_back()
    if kind == "retina":
        coords = ((-3.9, 1.18), (-1.05, 1.28), (2.65, 1.25),
                  (-3.72, -1.42), (-0.75, -1.56), (2.98, -1.22))
    else:
        coords = ((-4.51, 0.72), (-2.96, 0.42), (-1.3, 0.68),
                  (-4.25, -1.05), (-2.78, -0.88), (-1.11, -1.1))
    cells = VGroup()
    for i, ((x, y), strength) in enumerate(zip(coords, strengths or [0.30] * 6)):
        if kind == "retina":
            body = neuron(0.28 * (-1) ** i).scale(0.73, about_point=ORIGIN)
        else:
            soma = Ellipse(width=1.25 + 0.14 * (i % 2), height=1.03,
                           stroke_color=GREY, stroke_width=3,
                           fill_color=CELL_FILL, fill_opacity=1).rotate(0.22 * (-1) ** i)
            body = VGroup(soma, lamp(0.49))
        body.shift(p(x, y))
        set_glow(body[1], strength)
        cells.add(body)
    return back, cells


class S15Aligned(NarratedScene):
    def construct(self):
        t = ValueTracker(5.35)
        graph, optics = recorded(t)
        self.add(*graph, *optics, schematic())
        self.play(t.animate.set_value(0.26), run_time=0.57)
        sweep(self, t, 5.35, 3.56)
        back, cells = specimen("retina")
        self.play(FadeOut(graph[-2]), FadeOut(graph[-1]), run_time=0.29)
        self.play(FadeOut(VGroup(*graph[:-2], *optics)), FadeIn(back), FadeIn(cells), run_time=1.04)


RETINA_TYPES = (0, 1, 2, 0, 1, 2)
RETINA_AT = 5.8


def retina_response(t, kind):
    """Illustrative onset, offset, or onset-and-offset groups from the same kernel."""
    if kind == 0:
        return calcium_response(t, (1.08,))
    if kind == 1:
        return calcium_response(t, (3.45,))
    return 0.79 * calcium_response(t, (1.08, 3.45))


def retina_light(t, kind):
    return 0.30 + 1.22 * retina_response(t, kind)


def stimulus(t):
    edge = Line(p(-5.68, -2.25), p(-5.68, 2.05), color=YELLOW, stroke_width=8)
    beam = RoundedRectangle(width=0.66, height=4.32, corner_radius=0.19, stroke_width=0,
                            fill_color=YELLOW).move_to(p(-5.34, -0.1))
    def update(m):
        time = t.get_value()
        intensity = np.clip(min((time - 0.64) / 0.44, (3.78 - time) / 0.50), 0, 1)
        edge.set_stroke(opacity=0.26 + 0.71 * intensity)
        beam.set_fill(opacity=0.04 + 0.23 * intensity)
    return VGroup(beam, edge).add_updater(update, call_updater=True)


class S16Retina(SpokenScene):
    def construct(self):
        back, cells = specimen("retina")
        t = ValueTracker(0)
        for cell, kind in zip(cells, RETINA_TYPES):
            light_motion(cell[1], t, lambda x, kind=kind: retina_light(x, kind))
        stim = stimulus(t)
        self.add(back, cells, stim, schematic())
        self.at("across many cells")
        sweep(self, t, 1.65, 3.84)
        sweep(self, t, 3.98, 1.79)
        self.at("in 2016")
        sweep(self, t, 4.8, 2.2)
        self.at("imaged isolated mouse")
        label = T("Mouse retina", 34).move_to(p(0, 2.58))
        self.play(FadeIn(label), t.animate.set_value(RETINA_AT), run_time=1.55)
        self.finish()


def sample_trace(kind, at):
    x, y = at[:2]
    plot = Plot(box=(x - 1.35, x + 1.35, y - 0.33, y + 0.35), xr=(0, 6.1), yr=(0, 1.12),
                color=GREY, stroke=1.7)
    return VGroup(plot, plot.curve(lambda t: retina_response(t, kind), color=GREEN, width=4))


class S17Groups(SpokenScene):
    def construct(self):
        strengths = [retina_light(RETINA_AT, kind) for kind in RETINA_TYPES]
        back, cells = specimen("retina", strengths)
        title = T("Mouse retina", 34).move_to(p(0, 2.58))
        t = ValueTracker(RETINA_AT)
        stim = stimulus(t)
        self.add(back, cells, title, stim, schematic())
        self.at("retina's output neurons")
        columns = (-4.52, -2.91, -1.30)
        targets = [p(x, y) for y in (1.03, -1.38) for x in columns]
        outlines = cells.copy()
        for outline, target in zip(outlines, targets):
            outline.scale(0.65).move_to(target)
        self.play(Transform(cells, outlines), FadeOut(stim), run_time=1.71)
        self.at("called ganglion cells")
        label = T("Ganglion cells", 32).move_to(p(columns[1], 2.54))
        self.play(swap(title, label), run_time=0.69)
        before = ((1.33, 1.87), (4.65, 1.87), (1.33, 0.28),
                  (4.65, 0.28), (1.33, -1.31), (4.65, -1.31))
        traces = [sample_trace(kind, p(*at)) for kind, at in zip(RETINA_TYPES, before)]
        self.play(LaggedStart(*[FadeIn(trace, shift=RIGHT * 0.35) for trace in traces],
                               lag_ratio=0.19), run_time=1.48)
        self.at("grouping cells by how")
        top_right, middle_left, middle_right, bottom_left = traces[1:5]
        half_row = UP * ((before[0][1] - before[2][1]) / 2)
        column_step = RIGHT * (before[1][0] - before[0][0])
        # Cross between rows, then clear the middle slots for the arriving traces.
        self.play(top_right.animate.shift(-half_row), bottom_left.animate.shift(half_row), run_time=0.55)
        self.play(top_right.animate.shift(-column_step), bottom_left.animate.shift(column_step), run_time=1.10)
        self.play(middle_right.animate.shift(2 * half_row), middle_left.animate.shift(-2 * half_row), run_time=0.95)
        self.play(top_right.animate.shift(-half_row), bottom_left.animate.shift(half_row), run_time=0.66)
        highlights = VGroup(*[
            RoundedRectangle(width=6.18, height=1.06, corner_radius=0.16,
                             stroke_color=GREEN, stroke_width=2).move_to(p(2.99, y))
            for y in (1.87, 0.28, -1.31)])
        self.play(LaggedStart(*[Create(box) for box in highlights], lag_ratio=0.38), run_time=1.42)
        self.at("distinguished at least")
        count = T("At least 32 types", 36, GREEN).move_to(p(2.94, -2.56))
        self.play(FadeIn(count, shift=UP * 0.16), run_time=0.40)
        self.finish()


def taste_optics():
    lens = RoundedRectangle(width=0.5, height=1.04, corner_radius=0.12,
                            stroke_color=GREY, stroke_width=4,
                            fill_color=DISPLAY, fill_opacity=1).move_to(p(-2.78, 1.75))
    tip = Ellipse(width=0.50, height=0.20, stroke_color=GREEN, stroke_width=3).move_to(p(-2.78, 1.23))
    return VGroup(lens, tip).set_z_index(2)


def tongue_inset():
    """Profile of the anesthetized specimen with the liquid landing on its tongue."""
    at = p(2.89, -0.18)
    back = panel(5.2, 4.4, at, fill=DISPLAY, edge="#55727B")
    head = VMobject(stroke_color=GREY, stroke_width=3, fill_color=CELL_FILL, fill_opacity=1)
    head.set_points_smoothly([p(0.94, -0.91), p(1.19, 0.29), p(1.86, 0.74), p(2.76, 0.49),
                              p(3.67, 0.05), p(4.57, -0.43), p(4.2, -0.70), p(3.55, -0.83),
                              p(2.93, -1.35), p(1.88, -1.45), p(0.94, -0.91)])
    ear = Ellipse(width=0.66, height=0.90, color=GREY, stroke_width=3,
                  fill_color=CELL_FILL, fill_opacity=1).rotate(0.37).move_to(p(1.83, 0.67))
    eye = ArcBetweenPoints(p(2.93, -0.01), p(3.38, -0.03), angle=0.63, color=TEXT, stroke_width=3)
    tongue = Ellipse(width=1.52, height=0.32, stroke_color=GREY, stroke_width=2.2,
                     fill_color="#A16D85", fill_opacity=1).rotate(0.15).move_to(p(4.43, -0.84))
    return VGroup(back, head, ear, eye, tongue)


class S18Taste(SpokenScene):
    def construct(self):
        back, cells = specimen("taste")
        optics = taste_optics()
        inset = tongue_inset()
        name = T("Taste neurons", 34).move_to(p(-2.78, 2.59))
        phase = ValueTracker(0)
        fluid = VGroup(*[Dot(radius=0.095, color=ORANGE) for _ in range(5)])
        for i, drop in enumerate(fluid):
            def flow(m, i=i):
                pos = (phase.get_value() + i * 0.173) % 1
                m.move_to(p(5.08 - 0.19 * pos ** 2, interpolate(1.19, -0.73, pos)))
                m.set_opacity(min(1, 9 * (1 - pos)))
            drop.add_updater(flow, call_updater=True)
        # Five cells favor a single trial; one responds on two trials.
        selections = ((0, 4, 5), (2, 3), (1, 5))
        self.add(back, schematic())
        self.at("you can also ask")
        self.play(LaggedStart(*[FadeIn(cell) for cell in cells], lag_ratio=0.28), run_time=3.17)
        self.at("colleagues imaged a cluster")
        self.play(FadeIn(optics), run_time=1.18)
        self.at("taste neurons the geniculate")
        self.play(FadeIn(name), run_time=0.65)
        self.at("in anesthetized mice")
        self.play(FadeIn(inset, shift=LEFT * 0.57), run_time=1.7)
        self.at("taste solutions flowed")
        self.add(fluid)
        sweep(self, phase, 1.65, 2.72)
        self.at("most responding neurons")
        for trial, (active, color) in enumerate(zip(selections, (ORANGE, ROSE, LAVENDER))):
            if trial > 0:
                self.play(UpdateFromAlphaFunc(cells, lambda m, a: [
                    set_glow(cell[1], interpolate(1.42 if i in selections[trial - 1] else 0.22, 0.22, a))
                    for i, cell in enumerate(m)]), run_time=0.27)
            fluid.set_color(color)
            self.play(phase.animate.increment_value(0.72),
                      UpdateFromAlphaFunc(cells, lambda m, a: [
                          set_glow(cell[1], interpolate(0.22, 1.42 if i in active else 0.22, a))
                          for i, cell in enumerate(m)]), run_time=1.26)
        self.at("tested taste qualities")
        for drop in fluid:
            drop.clear_updaters()
        self.play(FadeOut(fluid), FadeOut(inset),
                  *[UpdateFromAlphaFunc(cells[i][1], lambda m, a: set_glow(m, 1.42 - 0.58 * a))
                    for i in selections[-1]], run_time=1.05)
        self.finish()


class S19End(EndCard):
    LINE = "Calcium imaging turns calcium changes into light to track neural activity."
