"""Two-photon microscopy, from a deep optical focus to living-cell activity.

BLUE: apparatus; GREY: tissue structure; PURPLE: infrared excitation;
YELLOW: electrical spikes; GREEN: fluorescence and microglia; TEAL: calcium;
blue-grey: calcium channels; orange: M13 peptide; RED: background and
readout uncertainty; GOLD: questions and study credits.
Study maps and traces are schematic. Response-map hues distinguish categories.
"""
from bp_parts import *

PURPLE = "#B58CD9"
TISSUE = "#30394D"
LAYER = "#374258"
CELL = "#8491AB"
LOW_GREEN = "#375B52"
CHANNEL_COLOR = "#7FA6B8"
M13_COLOR = "#F29E4C"
FOCUS_Y = -0.75
FOCUS = np.array([-2.95, FOCUS_Y, 0])
SOMA = np.array([-3.65, -0.35, 0])
QUESTION = "What happens to a single spike’s glow?"
QUESTION_STYLE = dict(y=2.78, size=37, max_w=11.5)
RESPONSE_COLORS = (GREEN, PURPLE, TEAL, "#F29E4C")


def p(x, y):
    return np.array([x, y, 0.0])


def label(text, x, y, color=TEXT, size=30):
    return T(text, size, color).move_to(p(x, y))


def plate(width, height, center, color=TISSUE, outline=None):
    return RoundedRectangle(width=width, height=height, corner_radius=0.23,
                            stroke_color=outline or color, stroke_width=2 if outline else 0,
                            fill_color=color, fill_opacity=1).move_to(center)


def branch(points, color, width, opacity=1):
    line = VMobject()
    line.set_points_smoothly(points)
    line.set_fill(opacity=0)
    return line.set_stroke(color, width, opacity=opacity)


def neuron(center, radius=0.36, color=CELL, angle=0, filling=0.38, opacity=1):
    """The same soma and branching silhouette at both magnifications."""
    def at(x, y):
        return center + rotate_vector(p(x, y) * radius, angle)

    branches = VGroup(
        branch([at(-0.47, 0.65), at(-1.0, 1.49), at(-1.8, 2.15)], color, 3, opacity),
        branch([at(-0.94, 1.4), at(-0.83, 2.08), at(-1.16, 2.57)], color, 2.1, opacity),
        branch([at(0.54, 0.55), at(1.22, 1.16), at(1.97, 1.28)], color, 3, opacity),
        branch([at(1.18, 1.13), at(1.47, 1.68), at(2.0, 2.04)], color, 2.1, opacity),
        branch([at(-0.55, -0.43), at(-1.12, -0.99), at(-1.81, -1.18)], color, 2.7, opacity),
        branch([at(0.49, -0.51), at(0.94, -1.18), at(1.51, -1.87)], color, 2.7, opacity),
    )
    soma = Ellipse(width=1.78 * radius, height=1.55 * radius, stroke_width=3.2,
                   stroke_color=color, stroke_opacity=opacity,
                   fill_color=color, fill_opacity=filling * opacity)
    soma.rotate(angle).move_to(center)
    return VGroup(branches, soma)


def glia(center, reach=0.75, color=LOW_GREEN, phase=0):
    rays = VGroup()
    for i in range(7):
        angle = TAU * i / 7 + 0.23
        extent = reach * (0.84 + 0.24 * np.sin(phase + i * 2.4))
        bend = np.sin(i * 4) * 0.45

        def at(radius, turn=0):
            return center + rotate_vector(RIGHT * radius * extent, angle + turn)

        rays.add(branch([at(0.12), at(0.48, bend), at(1.12, bend * 0.46)], color, 3.1))
        rays.add(branch([at(0.48, bend), at(0.79, bend + 0.34), at(0.99, bend + 0.43)], color, 2))
    return VGroup(rays, Dot(center, radius=0.18 * reach, color=color))


CELL_SITES = (
    (-5.12, 0.28, 0.39, -0.50), (-3.55, 0.48, 0.29, 0.51), (-1.08, 0.27, 0.37, -0.7),
    (0.92, 0.5, 0.29, 0.31), (3.18, 0.34, 0.40, -0.4), (5.12, 0.25, 0.37, 0.36),
    (-4.68, -1.69, 0.39, 0.14), (-2.95, FOCUS_Y, 0.43, 0.1), (-0.72, -1.7, 0.40, 0.66),
    (1.15, FOCUS_Y, 0.40, 0.37), (2.81, -1.82, 0.37, -0.56),
    (4.69, FOCUS_Y, 0.43, 0.26), (-2.05, -1.96, 0.30, -0.34),
)
DEEP_SITES = [CELL_SITES[i] for i in (7, 9, 11)]


def tissue_base():
    shell = plate(12.35, 4.62, p(0, -0.54), TISSUE, "#536079")
    layers = VGroup()
    xs = np.linspace(-6.0, 6.0, 26)
    for j, y in enumerate((1.12, 0.25, -0.72, -1.67, -2.4)):
        ridge = [p(x, y + 0.13 * np.sin(x * 0.7 + j) + 0.045 * np.cos(1.6 * x + j))
                 for x in xs]
        skirt = [q + DOWN * 0.22 for q in reversed(ridge)]
        layers.add(Polygon(*ridge, *skirt, stroke_width=0, fill_color=LAYER, fill_opacity=1))
    return VGroup(shell, layers)


def tissue(moving=False):
    cells = VGroup()
    for i, (x, y, radius, angle) in enumerate(CELL_SITES):
        cell = neuron(p(x, y), radius, CELL, angle, filling=0.27, opacity=0.56)
        if moving:
            bob(cell, amp=0.09, speed=1.45 + 0.05 * i, seed=i)
        cells.add(cell)
    for i, center in enumerate((p(-1.78, -0.5), p(2.12, -0.82), p(4.14, -1.87))):
        cell = glia(center)
        if moving:
            bob(cell, amp=0.08, speed=1.25, seed=i)
        cells.add(cell)
    return VGroup(tissue_base(), cells)


def quiet_motion(mob, action):
    """Run a periodic action while narration settles between cues."""
    mob.phase = 0.0

    def update(obj, dt):
        obj.phase += dt
        action(obj, obj.phase)

    return mob.add_updater(update)


def halo(center, strength=1, color=GREEN, radius=0.44):
    glow = VGroup()
    for scale, alpha in ((2.8, 0.13), (2.1, 0.19), (1.45, 0.30), (0.83, 0.56), (0.29, 1)):
        glow.add(Circle(radius=radius * scale, stroke_width=0, fill_color=color,
                        fill_opacity=strength * alpha).move_to(center))
    return glow


def objective():
    body = plate(2.15, 0.61, p(-2.95, 2.71), "#224654", BLUE)
    rim = plate(1.58, 0.26, p(-2.95, 2.32), "#346474", BLUE)
    lens = Ellipse(width=1.27, height=0.19, stroke_width=2.4, stroke_color=BLUE,
                   fill_color=BLUE, fill_opacity=0.42).move_to(p(-2.95, 2.16))
    return VGroup(body, rim, lens)


def optical_beam(x):
    start = -2.95
    surface_y = 1.77
    fraction = (2.12 - surface_y) / (2.12 - FOCUS_Y)
    surface_x = interpolate(start, x, fraction)
    half_width = 0.61 * (1 - fraction)
    upper = Polygon(p(start - 0.61, 2.12), p(start + 0.61, 2.12),
                    p(surface_x + half_width, surface_y), p(surface_x - half_width, surface_y),
                    stroke_width=0, fill_color=PURPLE, fill_opacity=0.22)
    cone = Polygon(p(surface_x - half_width, surface_y), p(surface_x + half_width, surface_y),
                   p(x, FOCUS_Y),
                   stroke_color=PURPLE, stroke_width=1.4, stroke_opacity=0.54,
                   fill_color=PURPLE, fill_opacity=0.22)
    falloff = Polygon(p(x, FOCUS_Y), p(x + 0.87, -2.68), p(x - 0.87, -2.68),
                      stroke_width=0, fill_color=PURPLE, fill_opacity=0.065)
    return VGroup(upper, cone, falloff)


def focus_cells(count=3):
    return VGroup(*[neuron(p(x, y), r, GREEN, a, filling=0.63)
                    for x, y, r, a in DEEP_SITES[:count]])


def close_world():
    shell = plate(5.85, 5.42, p(-3.35, -0.05), TISSUE, "#536079")
    quiet = VGroup(
        neuron(p(-5.32, -1.55), 0.39, CELL, 0.38, opacity=0.36),
        neuron(p(-1.95, -1.65), 0.37, CELL, -0.54, opacity=0.36),
        neuron(p(-5.28, 1.33), 0.31, CELL, -0.7, opacity=0.36),
    )
    for i, cell in enumerate(quiet):
        bob(cell, amp=0.1, speed=1.5, seed=i)
    major = neuron(SOMA, 1.06, GREEN, 0.1)
    return VGroup(shell, quiet), major


def soma_glow(level=1):
    return halo(SOMA, strength=level, radius=0.48)


def breathing_soma():
    return quiet_motion(soma_glow(), lambda m, t: m.become(
        halo(SOMA, 0.53 + 0.45 * np.sin(t * 1.9), radius=0.77)))


def response(t, onset=1.0, decay=2.0, rise=0.22):
    """Schematic calcium transient. First-order onset and exponential clearance."""
    dt = max(0, t - onset)
    return (1 - np.exp(-dt / rise)) * np.exp(-dt / decay)


def plot_card(box, xr, yr):
    return Plot(box, xr, yr, color=GREY, stroke=2.3)


def chart_field(center=p(3.30, -0.05)):
    return plate(5.76, 5.42, center, "#242D40", "#536079")


class S01Hook(SpokenScene):
    def construct(self):
        world = tissue(moving=True)
        glow = halo(FOCUS, 0.85)
        prompt = fit_text("How can you watch single cells work\ndeep inside living tissue?",
                          max_w=11.7, size=39, color=TEXT).move_to(p(0, 2.77))
        self.at("how can you")
        self.add(world, prompt, glow)
        self.play(FadeOut(glow), run_time=2.6)
        self.at("wiring maps show")
        wiring = VGroup(*[branch([p(*a), p(*b), p(*c)], GREY, 2.4)
                          for a, b, c in [
                              ((-5.12, 0.28), (-4.2, 0.32), (-2.95, -0.75)),
                              ((-2.95, -0.75), (-2.16, -1.30), (-0.72, -1.7)),
                              ((-0.72, -1.7), (0.05, -0.93), (1.15, -0.75)),
                              ((1.15, -0.75), (2.18, -0.40), (3.18, 0.34)),
                              ((3.18, 0.34), (4.10, -0.15), (4.69, -0.75)),
                          ]])
        self.play(FadeOut(prompt), Create(wiring), run_time=1.75)
        self.at("yet cannot show")
        self.play(FadeOut(wiring), run_time=1.8)
        self.at("lights only one")
        self.play(FadeIn(glow), run_time=0.55)
        self.play(FadeOut(glow), run_time=1.65)
        self.finish()


class S02Title(TitleCard):
    LESSON = "Two-Photon Microscopy"
    TITLE = "Watching Living Cells Deep Inside Tissue"

    def construct(self):
        self.add(tissue(moving=True))
        title = label(self.TITLE, 0, 3.10, size=47)
        fit(title, max_w=12.1)
        lens = objective()
        self.play(FadeIn(title), run_time=0.35)
        self.wait(0.65)
        self.play(FadeOut(title), run_time=0.35)
        self.play(FadeIn(lens, shift=DOWN * 0.20), run_time=0.55)


class S03Focus(SpokenScene):
    def construct(self):
        self.add(tissue(moving=True), objective())
        x = ValueTracker(FOCUS[0])
        travel = ValueTracker(0)
        beam = always_redraw(lambda: optical_beam(x.get_value()))
        self.at("the microscope aims")
        self.play(Create(beam), run_time=1.4)
        mark = label("Infrared laser", 2.55, 2.62, PURPLE, 34)
        self.at("infrared laser beam")
        self.play(FadeIn(mark), run_time=0.45)

        def photons():
            fraction = travel.get_value()
            origin = p(-2.95, 2.07)
            target = p(x.get_value(), FOCUS_Y)
            return VGroup(*[Dot(interpolate(origin + RIGHT * side * 0.56, target, fraction),
                                color=PURPLE, radius=0.093) for side in (-1, 1)])

        pair = always_redraw(photons)
        flash = halo(FOCUS, radius=0.38)
        self.at("paired infrared photons")
        self.add(pair)
        self.play(travel.animate.set_value(1), run_time=1.78, rate_func=linear)
        self.remove(pair)
        self.at("fluorescence only")
        self.play(FadeIn(flash), run_time=0.45)
        focal_label = label("Deep focus", 2.55, 2.62, GREEN, 34)
        self.play(swap(mark, focal_label, run_time=0.75))
        self.at("fluorescence needs")
        self.play(FadeOut(flash), run_time=0.65)
        travel.set_value(0)
        self.add(pair)
        self.play(travel.animate.set_value(1), run_time=2.0, rate_func=linear)
        self.remove(pair)
        self.play(FadeIn(flash), run_time=0.4)
        self.at("beam is tightest")
        self.play(Indicate(flash, scale_factor=1.18, color=GREEN), run_time=1.5)
        self.at("scanning that spot")
        self.remove(flash)
        scan = always_redraw(lambda: halo(p(x.get_value(), FOCUS_Y), radius=0.36))
        cells = focus_cells()
        self.add(scan, cells[0])
        self.play(x.animate.set_value(1.15), run_time=0.85, rate_func=linear)
        self.play(FadeIn(cells[1]), run_time=0.25)
        self.play(x.animate.set_value(4.69), run_time=0.81, rate_func=linear)
        self.play(FadeIn(cells[2]), FadeOut(focal_label), run_time=0.4)
        self.finish()


class S04Sensor(SpokenScene):
    def construct(self):
        initial = tissue(moving=True)
        highlighted = focus_cells()
        lens, beam, spot = objective(), optical_beam(4.69), halo(p(4.69, FOCUS_Y), radius=0.36)
        self.add(initial, lens, beam, spot, highlighted)
        world, cell = close_world()
        initially_lit = soma_glow(0.18)
        self.at("to see neurons fire")
        self.play(FadeOut(initial, shift=RIGHT * 0.25), FadeOut(lens), FadeOut(beam),
                  FadeOut(spot), FadeOut(highlighted[1:]), FadeIn(world),
                  ReplacementTransform(highlighted[0], cell), run_time=1.4)
        self.add(initially_lit)
        self.bring_to_front(cell)
        self.at("sensor turns spikes")
        preview = halo(SOMA, radius=0.76)
        self.play(FadeIn(preview), run_time=0.62)
        self.play(FadeOut(preview), run_time=1.35)
        self.at("after an action")
        pulse_dot = halo(p(-4.92, 1.29), color=YELLOW, radius=0.47)
        path = branch([p(-4.92, 1.29), p(-4.63, 1.11), p(-4.15, 0.34), SOMA], YELLOW, 3)
        self.add(pulse_dot)
        self.play(MoveAlongPath(pulse_dot, path, rate_func=linear), run_time=1.30)
        self.play(FadeOut(pulse_dot), Flash(SOMA, color=YELLOW, line_length=0.32, flash_radius=1.02),
                  run_time=0.48)

        centers = [p(-4.47, -0.16), p(-4.42, -0.57), p(-4.14, -0.98)]
        gates = VGroup(*[VGroup(
            RoundedRectangle(width=0.24, height=0.13, corner_radius=0.04, color=CHANNEL_COLOR,
                             stroke_width=1.5, fill_opacity=1).move_to(q + UP * 0.072),
            RoundedRectangle(width=0.24, height=0.13, corner_radius=0.04, color=CHANNEL_COLOR,
                             stroke_width=1.5, fill_opacity=1).move_to(q + DOWN * 0.072))
            for q in centers])
        self.at("voltage gated calcium")
        self.play(FadeIn(gates), run_time=0.65)
        self.at("channels open")
        self.play(*[g[0].animate.shift(UP * 0.085) for g in gates],
                  *[g[1].animate.shift(DOWN * 0.085) for g in gates], run_time=0.5)
        ca = VGroup(*[Dot(q + LEFT * 0.31, radius=0.077, color=TEAL) for q in centers])
        self.at("cell body calcium")
        self.play(FadeIn(ca), run_time=0.4)
        calcium_halo = halo(SOMA, strength=0.72, color=TEAL, radius=0.76)
        self.play(*[dot.animate.shift(RIGHT * (0.8 + i * 0.08) + UP * (i - 1) * 0.16)
                    for i, dot in enumerate(ca)], FadeIn(calcium_halo), run_time=1.60)
        self.bring_to_front(cell, ca)
        quiet_motion(calcium_halo, lambda m, t: m.become(
            halo(SOMA + 0.34 * p(np.cos(t * 1.52), np.sin(t * 1.52)),
                 0.56 + 0.23 * np.sin(t * 1.8), color=TEAL, radius=0.73)))
        for i, dot in enumerate(ca):
            bob(dot, amp=0.11, speed=2, seed=i)

        inset = chart_field()
        barrel_color = "#426D55"
        barrel = RoundedRectangle(width=1.21, height=1.54, corner_radius=0.19,
                                  stroke_color=GREEN, stroke_width=3, fill_color=barrel_color,
                                  fill_opacity=1).move_to(p(1.92, -0.26))
        top = Ellipse(width=1.17, height=0.32, stroke_color=GREEN, stroke_width=2.6,
                      fill_color="#56856B", fill_opacity=1).move_to(p(1.92, 0.43))
        cylinder = VGroup(barrel, top)

        def clasp(gap):
            return VGroup(
                branch([p(3.0, -0.15), p(3.34, 0.33), p(3.88, -0.07 + gap),
                        p(4.20, -0.04 + gap)], TEAL, 8),
                branch([p(3.0, -0.15), p(3.36, -0.62), p(3.87, -0.34 - gap),
                        p(4.20, -0.33 - gap)], TEAL, 8),
            )

        clamp = clasp(0.44)
        arm = Line(p(2.54, -0.15), p(3.0, -0.15), stroke_width=4, color=GREY)
        peptide = RoundedRectangle(width=0.86, height=0.19, corner_radius=0.07,
                                   stroke_width=0, fill_color=M13_COLOR, fill_opacity=1).move_to(p(4.49, -0.18))
        tether = branch([p(2.25, -1.03), p(3.47, -1.36), p(4.85, -1.07), p(4.92, -0.18)], GREY, 3)
        self.at("gcamp6 joins")
        self.play(FadeIn(inset), FadeIn(cylinder), run_time=0.65)
        self.play(FadeIn(label("GCaMP6", 3.30, 1.94, GREEN, 36)), run_time=0.4)
        self.at("green fluorescent protein")
        self.play(FadeIn(label("Fluorescent\nprotein", 2.03, 1.20, GREEN, 28)), run_time=0.55)
        self.at("to calmodulin")
        self.play(Create(arm), Create(clamp), run_time=0.6)
        self.play(FadeIn(label("Calmodulin", 4.22, 1.08, TEAL, 29)), run_time=0.44)
        self.play(FadeIn(peptide), Create(tether), run_time=0.55)
        m13 = label("M13", 4.45, -1.88, M13_COLOR, 29)
        self.at("calcium bound calmodulin")
        docking = VGroup(Dot(p(3.02, 0.52), color=TEAL, radius=0.084),
                         Dot(p(2.99, -0.69), color=TEAL, radius=0.084))
        self.play(FadeIn(docking), run_time=0.35)
        self.play(docking[0].animate.move_to(p(3.36, 0.29)),
                  docking[1].animate.move_to(p(3.37, -0.55)), run_time=0.65)
        self.at("grips peptide")
        self.play(Transform(clamp, clasp(0.01)), run_time=0.78)
        self.play(FadeIn(m13), run_time=0.44)
        self.at("changing shape")
        self.play(FadeOut(calcium_halo), barrel.animate.set_fill(GREEN, opacity=0.88),
                  top.animate.set_fill("#B7E891", opacity=1),
                  Transform(initially_lit, soma_glow()), run_time=1.2)
        self.finish()


class S05Normalize(SpokenScene):
    def construct(self):
        world, cell = close_world()
        glow = soma_glow()
        self.add(world, glow, cell)
        inset = chart_field()
        plot = plot_card((1.06, 5.40, -1.84, 1.3), (0, 8), (0, 730))
        clock = ValueTracker(0)
        laser = ValueTracker(1)
        background = ValueTracker(0)
        peak_t = 1 + 0.22 * np.log(1 + 2.0 / 0.22)
        amplitude = 96 / response(peak_t)

        def fluorescence(t):
            return laser.get_value() * (260 + amplitude * response(t)) + background.get_value()

        curve = always_redraw(lambda: plot.curve(fluorescence, x1=clock.get_value(),
                                                  color=GREEN, width=5))
        dot = plot.dot(clock.get_value, lambda: fluorescence(clock.get_value()),
                       color=GREEN, ring=GREEN, radius=0.065)
        rest = always_redraw(lambda: plot.hline(fluorescence(0), color=GREY))
        heading = label("Fluorescence", 3.31, 1.97, GREEN, 34)
        rest_label = label("F₀", 5.72, plot.pt(0, 260)[1], TEXT, 30)
        peak_label = label("F", 1.95, -0.01, GREEN, 30)
        self.at("from that glow")
        self.play(FadeIn(inset), Create(plot.axes), run_time=0.65)
        self.add(curve, rest, dot)
        glow.add_updater(lambda m: m.become(soma_glow(0.22 + 0.76 * response(clock.get_value()) / response(peak_t))))
        self.play(FadeIn(heading), clock.animate.set_value(peak_t), run_time=2.15, rate_func=linear)
        self.at("f with resting")
        self.play(FadeIn(peak_label), run_time=0.32)
        self.at("baseline f0")
        self.play(FadeIn(rest_label), clock.animate.set_value(8), run_time=1.35, rate_func=linear)
        self.remove(dot)
        self.play(FadeOut(peak_label), run_time=0.28)
        sweep = ValueTracker(0)
        self.add(sweep)
        sweep.add_updater(lambda m, dt: m.increment_value(dt * 0.94))
        cursor = always_redraw(lambda: Line(plot.pt(sweep.get_value() % 8, 0),
                                           plot.pt(sweep.get_value() % 8, 730),
                                           color=TEAL, stroke_width=2.2, stroke_opacity=0.45))
        glow.clear_updaters()
        quiet_motion(glow, lambda m, t: m.become(halo(SOMA, 0.22 + 0.78 * response(
            sweep.get_value() % 8) / response(peak_t), radius=0.72)))
        self.add(cursor)

        formula = VGroup(M("(F − F₀)", 34, GREEN), M("/ F₀", 34, TEXT), M("= ΔF/F₀", 34, GREEN))
        formula.arrange(RIGHT, buff=0.26).move_to(p(0, -3.27))
        self.at("the fluorescence change")
        self.play(FadeIn(formula[0]), run_time=0.42)
        self.at("by baseline")
        self.play(FadeIn(formula[1]), run_time=0.42)
        self.at("gives delta")
        self.play(FadeIn(formula[2]), run_time=0.55)

        bar = Rectangle(width=plot.x1 - plot.x0, height=0.44, stroke_width=0,
                        fill_color=RED, fill_opacity=0.27).move_to(p(3.23, -1.60))
        bg_label = label("Background light", 3.23, -1.05, TEXT, 29)
        self.at("with background light")
        self.remove(cursor, sweep)
        glow.clear_updaters()
        background.set_value(120)
        self.play(FadeOut(rest_label), FadeIn(bar), FadeIn(bg_label), run_time=0.38)
        self.wait(0.60)
        self.play(FadeOut(bar), FadeOut(bg_label), background.animate.set_value(0), run_time=0.95)

        track = Line(p(-5.38, -1.98), p(-1.20, -1.98), color=GREY, stroke_width=7)
        knob = always_redraw(lambda: Dot(track.point_from_proportion((laser.get_value() - 1) / 0.75),
                                         color=PURPLE, radius=0.12))
        power_label = label("Laser power", -3.27, -2.39, PURPLE, 29)
        stable = label("ΔF/F₀ stays steady", 3.35, -2.23, GREEN, 28)
        self.at("cancels shared scales")
        self.add(knob)
        self.play(Create(track), FadeIn(power_label), FadeIn(stable), run_time=0.65)
        self.at("laser power")
        self.play(laser.animate.set_value(1.69), run_time=2.15, rate_func=linear)
        self.at("yet cells stay unequal")
        glow.clear_updaters()
        self.remove(knob)
        self.play(FadeOut(track), FadeOut(power_label), FadeOut(stable), FadeOut(formula),
                  FadeOut(heading), run_time=0.45)
        second_center = p(-1.95, -0.70)
        second = neuron(second_center, 0.48, GREEN, -0.44, filling=0.50)
        second_glow = quiet_motion(halo(second_center, 0.55, radius=0.34),
                                   lambda m, t: m.become(halo(second_center, 0.37 + 0.34 * np.sin(t * 5.6),
                                                              radius=0.34)))
        self.play(FadeIn(second), run_time=0.45)
        self.add(second_glow)
        expression = label("More sensor", -1.88, 2.35, GREEN, 28)
        self.play(FadeIn(expression), run_time=0.40)
        self.at("expression changes")
        rng = np.random.default_rng(509)
        fluctuation = rng.normal(0, 12, 161)
        stretched = plot.curve(lambda t: laser.get_value() * (260 + amplitude * response(t, decay=4.2))
                                + np.interp(t, np.linspace(0, 8, 161), fluctuation),
                                color=TEAL, width=4)
        self.play(Create(stretched), FadeIn(label("Calcium buffering", 3.34, 1.96, TEAL, 30)), run_time=2.35)
        self.finish()


PREDICT_WIDTH = 11.66


def scan_area(width):
    return RoundedRectangle(width=width, height=3.72, corner_radius=0.17, stroke_color=PURPLE,
                            stroke_width=2.8, fill_color=PURPLE, fill_opacity=0.12).move_to(p(0, -0.54))


def time_bar():
    bar = plate(3.66, 0.15, p(1.72, -3.21), "#554C68", PURPLE)
    return VGroup(label("Imaging time", -1.81, -3.21, TEXT, 29), bar)


def raster_spot(x, y=-0.54):
    return VGroup(
        Rectangle(width=0.91, height=3.44, stroke_width=0, fill_color=PURPLE,
                  fill_opacity=0.25).move_to(p(x, y)),
        Line(p(x, y + 1.72), p(x, y - 1.72), stroke_color=PURPLE, stroke_width=2.3, stroke_opacity=0.65),
        halo(p(x, y), radius=0.26),
    )


def predict_frame():
    return tissue(), scan_area(PREDICT_WIDTH), time_bar(), raster_spot(4.74)


class S06PredictQ(SpokenScene):
    def construct(self):
        self.at("that photon noise")
        world = tissue()
        width = ValueTracker(3.28)
        scan = always_redraw(lambda: scan_area(width.get_value()))
        x = ValueTracker(-0.84)
        indicator = always_redraw(lambda: raster_spot(x.get_value()))
        self.add(world, scan, indicator)
        self.play(x.animate.set_value(0.86), run_time=2.85, rate_func=linear)
        self.at("image wider regions")
        self.play(width.animate.set_value(5.3), x.animate.set_value(-1.84), run_time=1.7, rate_func=linear)
        self.at("enlarge the field")
        self.play(width.animate.set_value(PREDICT_WIDTH), x.animate.set_value(4.75), run_time=1.7, rate_func=linear)
        self.at("the same imaging")
        self.play(FadeIn(time_bar()), x.animate.set_value(-4.75), run_time=1.45, rate_func=linear)
        self.at("what happens to")
        q = question_card(QUESTION, **QUESTION_STYLE)
        self.play(FadeIn(q), x.animate.set_value(4.76), run_time=1.18, rate_func=linear)
        self.play(x.animate.set_value(-4.75), run_time=1.03, rate_func=linear)
        self.play(x.animate.set_value(4.74), run_time=1.62, rate_func=linear)
        self.finish()


class S07PredictPause(Scene):
    def construct(self):
        self.camera.background_color = BG
        self.add(*predict_frame(), question_card(QUESTION, **QUESTION_STYLE))
        self.wait(4.5)


def minimized_field():
    field = VGroup(tissue(), scan_area(PREDICT_WIDTH))
    field.scale_to_fit_width(5.82).move_to(p(-3.35, -0.54))
    return field


class S08Photons(SpokenScene):
    def construct(self):
        world, scan, duration_bar, spot = predict_frame()
        question = question_card(QUESTION, **QUESTION_STYLE)
        self.add(world, scan, duration_bar, spot, question)
        self.at("as huang and")
        self.play(FadeOut(question), run_time=0.45)
        self.play(FadeOut(spot), run_time=0.45)
        inset = chart_field()
        self.play(Transform(VGroup(world, scan), minimized_field()), run_time=1.3)

        scan_center = scan.get_center()
        scan_width, scan_height = scan.width, scan.height
        pixels = VGroup(*[Square(side_length=0.15, stroke_color=GREEN, stroke_width=1.4,
                                  fill_color=GREEN, fill_opacity=0.45).move_to(scan_center + p(x, y))
                          for x in np.linspace(-0.44 * scan_width, 0.44 * scan_width, 15)
                          for y in np.linspace(-0.40 * scan_height, 0.40 * scan_height, 8)])
        rng = np.random.default_rng(813)
        photon_paths = [(scan_center + p(rng.uniform(-0.43, 0.43) * scan_width,
                                         rng.uniform(-0.39, 0.03) * scan_height),
                         rng.uniform(0.0, 1.0), rng.uniform(0.13, 0.30)) for _ in range(24)]
        returned = ValueTracker(24)
        photon_cloud = VGroup(*[Dot(radius=0.054, color=GREEN) for _ in photon_paths])

        def travel(cloud, phase):
            for i, (dot, (origin, offset, speed)) in enumerate(zip(cloud, photon_paths)):
                t = (offset + phase * speed) % 1
                dot.move_to(origin + t * 0.39 * scan_height * UP)
                dot.set_opacity((1 - t) if i < returned.get_value() else 0)

        quiet_motion(photon_cloud, travel)
        sweep_height = 0.90 * scan_height
        exposure = VGroup(
            Rectangle(width=0.21 * scan_width, height=sweep_height, stroke_width=0,
                      fill_color=PURPLE, fill_opacity=0.47),
            Line(DOWN * sweep_height / 2, UP * sweep_height / 2, stroke_color=PURPLE, stroke_width=2.3),
        )
        quiet_motion(exposure, lambda m, t: m.move_to(
            scan_center + RIGHT * (0.38 * scan_width * np.sin(t * 1.92))))
        self.at("the answer is")
        self.add(exposure, photon_cloud)
        self.play(FadeIn(label("Returned photons", -3.35, 2.42, GREEN, 33)), run_time=0.45)
        self.at("over more pixels")
        self.play(LaggedStart(*[FadeIn(pixel) for pixel in pixels], lag_ratio=0.022),
                  run_time=1.4)
        self.at("each neuron returns")
        self.play(pixels.animate.set_fill(GREEN, opacity=0.08).set_stroke(opacity=0.30),
                  returned.animate.set_value(6), run_time=2.15, rate_func=linear)
        self.at("photon counts flicker")

        graph = plot_card((0.98, 5.67, -1.72, 1.25), (0, 8), (-0.65, 0.70))
        xs = np.linspace(0, 8, 108)
        signal = np.array([0.36 * response(t, onset=2.15, decay=2.4) for t in xs])
        clean = rng.poisson(400 * (1 + signal)) / 400 - 1
        noisy = rng.poisson(23 * (1 + signal)) / 23 - 1
        noise = ValueTracker(0)
        amounts = lambda: (1 - noise.get_value()) * clean + noise.get_value() * noisy
        trace = always_redraw(lambda: graph.curve(lambda t: np.interp(t, xs, amounts()),
                                                   color=GREEN, width=4, n=len(xs)))
        heading = label("Single-spike glow", 3.32, 1.99, GREEN, 33)
        self.play(FadeIn(inset), FadeIn(graph), FadeIn(heading), run_time=0.45)
        self.add(trace)
        self.at("small glow sinks")
        self.play(noise.animate.set_value(1), run_time=2.0, rate_func=linear)

        self.at("in a simple model")
        self.play(FadeOut(trace), run_time=0.4)
        model = scope_tag("simple model", size=28, color=TEXT)
        self.play(FadeIn(model), run_time=0.35)
        slow = lambda t: 0.72 * response(t, onset=2.15, decay=3.6)
        smooth = graph.curve(slow, color=GREEN, width=4)
        self.at("slowly decaying signal")
        self.play(Create(smooth), run_time=0.67)

        def frames(step):
            times = np.arange(0.25, 8, step)
            return VGroup(*[Line(graph.pt(t, -0.63), graph.pt(t, -0.50), color=GREY, stroke_width=2.6)
                            for t in times])

        def samples(step):
            return VGroup(*[Dot(graph.pt(t, slow(t)), radius=0.069, color=TEAL)
                            for t in np.arange(0.25, 8, step)])

        fast_frames, fast_samples = frames(0.25), samples(0.25)
        marker = graph.vline(2.15, color=YELLOW, dashed=False)
        coarse = Rectangle(width=graph.pt(2.53, 0)[0] - graph.pt(1.79, 0)[0],
                           height=graph.y1 - graph.y0, stroke_width=0,
                           fill_color=YELLOW, fill_opacity=0.28).move_to(graph.pt(2.16, 0.025))
        self.add(fast_frames, fast_samples)
        self.at("slower framing")
        self.play(Transform(fast_frames, frames(0.86)), Transform(fast_samples, samples(0.86)),
                  run_time=1.55)
        self.at("photons hold steady")
        self.play(pixels.animate.set_fill(GREEN, opacity=0.45).set_stroke(opacity=1),
                  returned.animate.set_value(len(photon_paths)),
                  FadeIn(label("Steady photon return", 3.31, -2.22, GREEN, 28)), run_time=0.55)
        self.at("frame rates still")
        self.play(Create(marker), run_time=0.35)
        self.play(ReplacementTransform(marker, coarse), run_time=0.75)
        self.finish()


def pipette(soma):
    tip = soma.point_from_proportion(0.12)
    lower = p(-1.57, 1.75)
    upper = p(-2.07, 2.16)
    barrel = Polygon(tip, tip + p(0.12, 0.085), lower, upper, stroke_color=BLUE,
                     stroke_width=3.1, fill_color=BLUE, fill_opacity=0.24)
    return VGroup(barrel, Line(lower, upper, color=BLUE, stroke_width=3))


class S09Calibrate(SpokenScene):
    def construct(self):
        background, cell = close_world()
        field = minimized_field()
        self.add(field)
        pane = chart_field()
        volts = plot_card((0.98, 5.65, 0.25, 1.48), (0, 8), (0, 1.2))
        calcium = plot_card((0.98, 5.65, -2.04, -0.63), (0, 8), (-0.05, 1.18))
        spike_times = (1.41, 4.03, 6.18)
        clock = ValueTracker(0)

        def signal(t):
            return sum(response(t, onset=start, decay=1.16) for start in spike_times)

        fluorescence = calcium.live_curve(signal, clock, color=GREEN, width=4.7)
        electrical = VGroup(*[Line(volts.pt(t, 0.03), volts.pt(t, 1.0),
                                   color=YELLOW, stroke_width=4) for t in spike_times])
        top = label("Electrical spikes", 3.32, 2.02, YELLOW, 31)
        bottom = label("ΔF/F₀", 3.32, -0.20, GREEN, 31)
        self.at("light is not")
        self.play(FadeOut(field, scale=1.10), FadeIn(background),
                  GrowFromPoint(cell, p(-4.69, FOCUS_Y)), run_time=0.82)
        self.add(breathing_soma())
        self.bring_to_front(cell)
        self.play(FadeIn(pane), Create(calcium.axes), run_time=0.55)
        self.add(fluorescence)
        self.play(FadeIn(bottom), clock.animate.set_value(8), run_time=2.25, rate_func=linear)
        self.at("record light and spikes")
        self.play(Create(volts.axes), FadeIn(top), run_time=0.55)
        self.play(LaggedStart(*[GrowFromEdge(tick, DOWN) for tick in electrical], lag_ratio=0.65),
                  run_time=1.5)
        self.at("a fine glass")
        probe = pipette(cell[1])
        self.play(FadeIn(probe, shift=DOWN * 0.56 + LEFT * 0.42), run_time=1.38)
        self.at("picks up spikes")
        self.remove(*electrical)
        clock.set_value(0)
        for start, tick in zip(spike_times, electrical):
            self.play(clock.animate.set_value(start), run_time=0.66, rate_func=linear)
            self.play(GrowFromEdge(tick, DOWN), run_time=0.27)
        self.play(clock.animate.set_value(8), run_time=0.62, rate_func=linear)
        self.at("that cell attached")
        # Keep the linking arrows over their shared time coordinates and clear of the trace label.
        links = VGroup(*[Arrow(volts.pt(t, -0.05) + DOWN * 0.10,
                              calcium.pt(t + 0.27, 1.14) + UP * 0.06,
                              buff=0, tip_length=0.10, color=YELLOW, stroke_width=2.4)
                         for t in spike_times if t != spike_times[1]])
        self.play(Create(links), run_time=1.0)
        self.at("estimate with error")
        xs = np.linspace(0, 8, 141)
        upper = [calcium.pt(t, signal(t) + 0.14) for t in xs]
        lower = [calcium.pt(t, max(-0.04, signal(t) - 0.14)) for t in xs[::-1]]
        band = Polygon(*upper, *lower, stroke_width=0, fill_color=RED, fill_opacity=0.33)
        self.play(FadeIn(band), run_time=1.0)
        self.bring_to_front(fluorescence)
        self.play(FadeIn(label("Estimate with error", 3.32, -2.38, TEXT, 28)), run_time=0.6)
        self.finish()


def study_panels():
    panels = TwoPanel("Rat V1", "Cat area 18", colors=(TEXT, TEXT),
                      top=2.24, bottom=-2.72, width=12.25, size=34)
    for frame in (panels.left_frame, panels.right_frame):
        frame.set_fill(TISSUE, opacity=1).set_stroke("#536079", width=2)
    return panels


def map_scan(x):
    return Rectangle(width=0.86, height=3.73, stroke_width=0, fill_color=GREEN,
                     fill_opacity=0.44).move_to(p(x, -0.65))


def map_field(side, grouped, active=False):
    rng = np.random.default_rng(108 + side)
    left = -5.51 if side == 0 else 0.56
    field = VGroup()
    for i in range(7):
        for j in range(5):
            center = p(left + i * 0.79 + rng.uniform(-0.11, 0.11),
                       -2.16 + j * 0.77 + rng.uniform(-0.10, 0.10))
            category = int(rng.integers(4))
            if grouped:
                category = min(3, (i + (j == 3 and i == 1)) // 2)
            color = RESPONSE_COLORS[category] if active else CELL
            cell = Ellipse(width=0.46, height=0.27, stroke_color=color, stroke_width=2.0,
                           fill_color=color, fill_opacity=0.77 if active else 0.27)
            cell.rotate((category * 0.74 if active else rng.uniform(0, PI))).move_to(center)
            field.add(cell)
    return field


def cortex_maps(active):
    panels = study_panels()
    return panels, map_field(0, False, active), map_field(1, True, active)


class S10Unlocked1(SpokenScene):
    def construct(self):
        world = tissue(moving=True)
        panels, rat, cat = cortex_maps(False)
        self.at("in 2005")
        self.add(world)
        self.play(FadeOut(world), FadeIn(panels.left_frame), FadeIn(panels.right_frame),
                  FadeIn(rat), FadeIn(cat), run_time=1.45)
        credit = label("Ohki, Reid & colleagues, 2005", 0, 3.11, GOLD, 35)
        self.play(FadeIn(credit), run_time=0.48)
        self.at("imaged single cells")
        scan = map_scan(-5.65)
        self.play(FadeIn(scan), run_time=0.35)
        self.play(scan.animate.shift(RIGHT * 4.98), run_time=2.2, rate_func=linear)
        self.play(FadeOut(scan), run_time=0.34)

        self.at("rat v1 showed")
        self.play(FadeIn(panels.left_head), run_time=0.48)
        rat_active = map_field(0, False, True)
        self.play(LaggedStart(*[Transform(a, b) for a, b in zip(rat, rat_active)],
                              lag_ratio=0.066), run_time=2.75)
        self.at("called salt and pepper")
        mixture = label("Salt-and-pepper", -3.10, -3.24, TEXT, 30)
        self.play(FadeIn(mixture), run_time=0.48)
        for i, cell in enumerate(rat):
            base = cell.get_center().copy()
            quiet_motion(cell, lambda m, t, i=i, base=base: m.set_fill(
                opacity=0.76 + 0.22 * np.sin(t * 2.4 + i * 0.6)).move_to(
                base + UP * 0.06 * np.sin(t * 2 + i * 0.5)))
        self.at("the method was")
        scan = map_scan(0.67)
        self.play(FadeIn(scan), run_time=0.30)
        self.play(scan.animate.shift(RIGHT * 4.98), run_time=1.60, rate_func=linear)
        self.play(FadeOut(scan), run_time=0.27)
        self.at("cat area 18")
        self.play(FadeIn(panels.right_head), run_time=0.44)
        cat_active = map_field(1, True, True)
        self.play(LaggedStart(*[Transform(a, b) for a, b in zip(cat, cat_active)],
                              lag_ratio=0.047), run_time=1.70)
        self.at("column borders were")
        border = Line(p(3.28, -2.42), p(3.28, 1.21),
                      color=TEXT, stroke_width=2.4, stroke_opacity=0.73)
        span = label("Border 1–2 cells wide", 3.10, -3.24, TEXT, 30)
        self.play(Create(border), run_time=0.56)
        self.play(FadeIn(span), run_time=0.46)
        self.at("so tuning needs")
        self.play(FadeOut(border), FadeOut(span), FadeOut(mixture), run_time=0.6)
        for cell in rat:
            cell.clear_updaters()
        self.finish()


def retinal_sites():
    rng = np.random.default_rng(88)
    sites = []
    for j in range(5):
        for i in range(14):
            sites.append((p(-5.37 + 0.82 * i + rng.uniform(-0.12, 0.12),
                            -1.95 + 0.75 * j + rng.uniform(-0.1, 0.1)),
                          int(rng.integers(len(RESPONSE_COLORS)))))
    return sites


class S10bUnlockedRetina(SpokenScene):
    def construct(self):
        panels, rat, cat = cortex_maps(True)
        prior_credit = label("Ohki, Reid & colleagues, 2005", 0, 3.11, GOLD, 35)
        self.add(panels, rat, cat, prior_credit)
        cells = VGroup(*rat, *cat)
        layer = plate(12.26, 4.89, p(0, -0.17), TISSUE, "#536079")
        sites = retinal_sites()
        self.at("in 2016")
        self.play(FadeOut(panels.left_head), FadeOut(panels.right_head), run_time=0.32)
        self.play(FadeOut(panels.left_frame), FadeOut(panels.right_frame), FadeIn(layer),
                  swap(prior_credit, label("Baden & colleagues, 2016", 0, 3.11, GOLD, 35)),
                  *[Transform(c, Circle(radius=0.155, color=CELL, stroke_width=2,
                                        fill_opacity=0.48).move_to(q))
                    for c, (q, _) in zip(cells, sites)], run_time=1.40)
        self.bring_to_front(*cells)
        self.at("retinal ganglion cell")
        self.play(FadeIn(label("Retinal ganglion cell layer", 0, 1.85, TEXT, 32)),
                  LaggedStart(*[c.animate.set_color(RESPONSE_COLORS[category]).set_fill(opacity=0.76)
                                for c, (_, category) in zip(cells, sites)], lag_ratio=0.025), run_time=2.15)
        self.at("grouping cells by")
        layout = [0] * len(RESPONSE_COLORS)
        grouped = []
        for cell, (_, category) in zip(cells, sites):
            n = layout[category]
            layout[category] += 1
            x = -4.65 + category * 3.1 + (n % 5 - 2) * 0.41
            y = 0.86 - (n // 5) * 0.47
            grouped.append(cell.animate.move_to(p(x, y)))
        self.play(*grouped, run_time=1.8)
        profiles = VGroup(*[label(letter, -4.65 + i * 3.1, -1.50, color, 29)
                            for i, (letter, color) in enumerate(zip("ABCD", RESPONSE_COLORS))])
        self.play(FadeIn(profiles), FadeIn(label("Example light-response groups", 0, -2.09, TEXT, 29)),
                  run_time=0.40)
        self.at("at least 32")
        self.play(FadeIn(caption("At least 32 functional types", size=35, color=GREEN, y=-3.22)),
                  run_time=0.6)
        for cell, (_, category) in zip(cells, sites):
            pulse(cell, base=2, amp=1.5, speed=2.5 + category)
        self.finish()


class S11Unlocked2(SpokenScene):
    def construct(self):
        world = tissue(moving=True)
        source = objective()
        center = p(2.50, -0.52)
        scan_x = ValueTracker(center[0])
        beam = always_redraw(lambda: optical_beam(scan_x.get_value()))
        focus = quiet_motion(halo(p(center[0], FOCUS_Y), radius=0.36),
                             lambda m, t: m.become(halo(p(scan_x.get_value(), FOCUS_Y),
                                                       strength=0.58 + 0.36 * np.sin(t * 3),
                                                       radius=0.36)))
        branch_speed = ValueTracker(1.65)
        cell = glia(center, reach=1.62, color=GREEN)
        self.add(world, source, beam, focus)
        self.at("the method also")
        self.play(GrowFromCenter(cell), run_time=1.2)
        label_g = label("Microglia", 2.80, 2.66, GREEN, 35)
        self.play(FadeIn(label_g), run_time=0.42)

        cell.phase = 0.0

        def survey(mob, dt):
            mob.phase += dt * branch_speed.get_value()
            mob.become(glia(center, reach=1.62, color=GREEN, phase=mob.phase))

        cell.add_updater(survey)
        self.at("in healthy adult")
        location = label("Healthy adult mouse neocortex", -3.14, -3.27, TEXT, 28)
        self.play(FadeIn(location), run_time=0.55)
        self.at("saw presumed resting")
        author = label("Nimmerjahn, Kirchhoff & Helmchen", 0, -3.27, GOLD, 30)
        self.play(swap(location, author, run_time=0.88))
        self.at("continually extend")
        self.play(branch_speed.animate.set_value(2.02), run_time=1.8)
        self.at("used anesthetized")
        sleeping = label("Anesthetized", 2.79, 2.66, TEXT, 32)
        self.play(swap(label_g, sleeping, run_time=0.85))
        self.at("in awake mice")
        awake = label("Awake (Stowell & colleagues)", 2.80, 2.66, TEXT, 30)
        self.play(FadeOut(author), swap(sleeping, awake, run_time=0.95),
                  branch_speed.animate.set_value(0.66), run_time=1.2)
        self.at("lighting one deep")
        self.play(FadeOut(awake), scan_x.animate.set_value(-2.95), run_time=1.6, rate_func=linear)
        lit = focus_cells()
        self.play(FadeIn(lit[0]), run_time=0.35)
        self.play(scan_x.animate.set_value(1.15), run_time=0.85, rate_func=linear)
        self.play(FadeIn(lit[1]), run_time=0.25)
        self.play(scan_x.animate.set_value(4.69), run_time=0.85, rate_func=linear)
        self.play(FadeIn(lit[2]), run_time=0.35)
        self.finish()


class S12End(EndCard):
    LINE = "Paired infrared photons light only the focus, revealing deep living cells."
