"""Voltage clamp, built on one schematic preparation and recording display.

Color map from patch clamp: blue electrode and voltage, grey structure,
purple channel pores, yellow current, green control and entry, red blocked
entry, orange added solution, teal bath and cytoplasm, gold historical credits.
"""
from functools import lru_cache

from bp_parts import *
from bp_style import EndCard

PURPLE = "#B58CD9"
ORANGE = "#F29E4C"
BATH = "#183540"
CYTOPLASM = "#2B5965"
DISPLAY = "#192631"
CX, RX = -3.35, 3.46
MEMBRANE_Y = 0.62
REST, EK = -71, -95
QUESTION = "What two results would show positive voltage blocks entry?"
OPTIONS = ("Hold positive", "Hold negative")
TITLE = "Reading a Cell's Voltage and Its Currents"
LESSON = "Intracellular Recording and Voltage Clamp"


def p(x, y):
    return np.array([x, y, 0.0])


def label(text, x, y, color=TEXT, size=32, width=5.5):
    return fit_text(text, max_w=width, size=size, min_size=28, color=color,
                    weight=MEDIUM).move_to(p(x, y))


def tile(width, height, x, y, fill, edge, radius=0.23, stroke=2):
    return RoundedRectangle(width=width, height=height, corner_radius=radius,
                            stroke_color=edge, stroke_width=stroke,
                            fill_color=fill, fill_opacity=1).move_to(p(x, y))


def decks():
    return VGroup(tile(6.12, 6.53, CX, 0, BATH, "#36545F"),
                  tile(6.12, 6.53, RX, 0, DISPLAY, "#37495E")).set_z_index(-2)


def arrow(x, start, end, color=YELLOW):
    return Arrow(p(x, start), p(x, end), buff=0, color=color, stroke_width=7,
                 tip_length=0.19, max_stroke_width_to_length_ratio=24)


def electrode(x=CX, tip=-0.53, height=2.22):
    """Same fine glass electrode tapered to the recording point."""
    top = tip + height
    glass = Polygon(p(x - .27, top), p(x + .27, top), p(x + .035, tip),
                    p(x - .035, tip), color=BLUE, stroke_width=3,
                    fill_color=BLUE, fill_opacity=.25)
    wire = Line(p(x, top - .10), p(x, tip + .08), color=BLUE, stroke_width=2)
    return VGroup(glass, wire, Dot(p(x, tip), radius=.07, color=BLUE))


def pore(x):
    return VGroup(*[
        tile(.16, .44, x + side * .24, MEMBRANE_Y, PURPLE, PURPLE, radius=.06)
        for side in (-1, 1)
    ])


def neuron():
    body_edge = VMobject(stroke_color=GREY, stroke_width=3)
    body_edge.start_new_path(p(CX - 2.55, MEMBRANE_Y))
    body_edge.add_cubic_bezier_curve_to(p(CX - 3.04, .56), p(CX - 2.88, -.85),
                                       p(CX - 2.82, -1.88))
    body_edge.add_cubic_bezier_curve_to(p(CX - 2.76, -2.72), p(CX - 2.42, -2.80),
                                       p(CX - 1.95, -2.80))
    body_edge.add_line_to(p(CX + 1.95, -2.80))
    body_edge.add_cubic_bezier_curve_to(p(CX + 2.42, -2.80), p(CX + 2.76, -2.72),
                                       p(CX + 2.82, -1.88))
    body_edge.add_cubic_bezier_curve_to(p(CX + 2.88, -.85), p(CX + 3.04, .56),
                                       p(CX + 2.55, MEMBRANE_Y))
    body = body_edge.copy().close_path()
    body.set_fill(CYTOPLASM, opacity=1).set_stroke(width=0)
    gaps = [CX - 1.42, CX + 1.42]
    spans = zip([CX - 2.55, gaps[0] + .30, gaps[1] + .30],
                [gaps[0] - .30, gaps[1] - .30, CX + 2.55])
    membrane = VGroup(*[
        Line(p(a, MEMBRANE_Y), p(b, MEMBRANE_Y), color=GREY, stroke_width=7)
        for a, b in spans
    ])
    return VGroup(body, body_edge, membrane, *(pore(x) for x in gaps))


def drifting_ion(x, y, radius, color, phase, reach):
    dot = Dot(p(x, y), radius=radius, color=color, fill_opacity=.87)
    bob(dot, amp=reach * .53, speed=1.6 + .17 * np.cos(phase), seed=phase)
    clock = 0.0

    def drift_horizontal(m, dt):
        nonlocal clock
        clock += dt
        m.set_x(x + reach * np.sin(1.37 * clock + phase))

    return dot.add_updater(drift_horizontal)


def ion_field(keep_label_space=False, clamped=False):
    """Drift stays in the two compartments and leaves the lower label band clear."""
    rng = np.random.default_rng(11)
    group = VGroup()
    for row, y in enumerate([1.68, 2.26, 2.78, -1.06, -1.69, -2.25]):
        for idx, x in enumerate(np.linspace(CX - 2.36, CX + 2.36, 11)):
            if abs(x - CX) < .46 or (keep_label_space and row >= 4):
                continue
            dx, dy = rng.uniform(-.09, .09), rng.uniform(-.085, .085)
            radius, phase = rng.uniform(.083, .127), rng.uniform(0, TAU)
            if clamped and row in (1, 2) and .24 < x - CX < 1.35:
                continue
            group.add(drifting_ion(x + dx, y + dy, radius, TEAL if idx % 2 else BLUE,
                                   phase, .26))
    return group


def egg_ions():
    """Two wells of ion drift, with the sperm's path along the left rim clear."""
    rng = np.random.default_rng(23)
    group = VGroup()
    for y, offsets in [(1.45, [-.87, .78]), (.94, [-1.18, -.64, .77, 1.30]),
                       (.28, [-1.36, -.71, .67, 1.32]),
                       (-.32, [-1.44, -.80, .15, .79, 1.43]),
                       (-.90, [-1.35, -.63, -.06, .62, 1.24]),
                       (-1.5, [-1.21, -.60, .12, .71, 1.21]),
                       (-1.95, [-.54, .05, .63]),
                       (2.80, [-2.24, -1.71, -1.18, -.65, 1.31, 1.85, 2.36]),
                       (2.18, [-2.31, -1.75, 1.72, 2.31]),
                       (-2.60, [-2.23, -1.76, 1.80, 2.32])]:
        for dx in offsets:
            group.add(drifting_ion(CX + dx, y, rng.uniform(.094, .132),
                                   TEAL if rng.integers(2) else BLUE,
                                   rng.uniform(0, TAU), .28))
    return group


def currents():
    return VGroup(pulse(arrow(CX - 1.42, -.72, 1.32), base=7, amp=3),
                  pulse(arrow(CX + 1.42, 1.32, -.72), base=7, amp=3))


def plot(yr=(-105, 55), y0=-2.35, y1=2.04):
    return Plot(box=(.93, 5.99, y0, y1), xr=(0, 1), yr=yr, stroke=2.5,
                color="#8499AE")


def screen_heading(text="Membrane voltage", y=2.61, color=BLUE):
    return label(text, RX, y, color, 32)


def schematic():
    return scope_tag(size=28, color=GREY).move_to(p(5.45, -3.52))


def scan(ax, fn, color=BLUE, period=3.1):
    """An acquisition window moves through the recording behind the signal."""
    clock = ValueTracker(0)
    clock.add_updater(lambda m, dt: m.increment_value(dt))
    progress = lambda: (clock.get_value() % period) / period
    head = ax.dot(progress, lambda: fn(progress()),
                  color=color, ring=color, radius=.12)
    streak = always_redraw(lambda: ax.curve(
        fn, max(0, progress() - .19), progress(), color=TEXT,
        width=9, n=25, opacity=.56))

    def window():
        x = ax.pt(progress(), ax.yr[0])[0]
        width = max(.004, min(.84, x - ax.x0))
        return Rectangle(width=width, height=ax.y1 - ax.y0, stroke_width=0,
                         fill_color=color, fill_opacity=.27).move_to(
                             p(x - width / 2, (ax.y1 + ax.y0) / 2)).set_z_index(-1)

    return Group(clock, always_redraw(window), streak, head)


def draw_signal(scene, ax, fn, duration, color=BLUE, start=.001):
    t = ValueTracker(start)
    trace = ax.live_curve(fn, t, color=color, width=6)
    head = ax.dot(t.get_value, lambda: fn(t.get_value()), color=color, ring=color)
    scene.add(trace, head)
    scene.play(t.animate.set_value(1), run_time=duration, rate_func=linear)
    scene.remove(trace, head)
    trace = ax.curve(fn, color=color)
    scene.add(trace)
    return trace


@lru_cache(maxsize=1)
def squid_signal():
    """Hodgkin–Huxley 1952 membrane equations, modern voltage sign, 6.3 °C.
    Normalized display time and an illustrative stimulus.
    https://pmc.ncbi.nlm.nih.gov/articles/PMC1392413/
    """
    def trap(v, k):
        return k if abs(v) < 1e-7 else v / -np.expm1(-v / k)

    def gates(v):
        return np.array([.1 * trap(v + 40, 10), .07 * np.exp(-(v + 65) / 20),
                         .01 * trap(v + 55, 10)]), np.array([
            4 * np.exp(-(v + 65) / 18), 1 / (1 + np.exp(-(v + 35) / 10)),
            .125 * np.exp(-(v + 65) / 80)
        ])

    dt = .005
    t = np.arange(0, 12 + dt, dt)
    v = np.full(len(t), -65.)
    a, b = gates(v[0])
    g = a / (a + b)
    for i, time in enumerate(t[:-1]):
        m, h, n = g
        voltage = v[i]
        sodium = 120 * m**3 * h * (voltage - 50)
        potassium = 36 * n**4 * (voltage + 77)
        leak = .3 * (voltage + 54.387)
        stimulus = 17 if 2 <= time < 3.2 else 0
        v[i + 1] = voltage + dt * (stimulus - sodium - potassium - leak)
        a, b = gates(voltage)
        g += dt * (a * (1 - g) - b * g)
    return lambda x: np.interp(12 * x, t, v)


class S01Hook(SpokenScene, TitleCard):
    TITLE = TITLE
    LESSON = LESSON

    def construct(self):
        ax = plot()
        flat = ax.curve(lambda _: REST, color=BLUE)
        scanline = scan(ax, lambda _: REST)
        self.add(decks(), neuron(), ion_field(), ax, flat, scanline, schematic())
        self.at("while currents")
        flows = currents()
        self.play(FadeIn(flows), run_time=.84)
        self.at("When its voltage")
        self.remove(scanline)
        self.play(FadeOut(flows), FadeOut(flat), run_time=.45)
        draw_signal(self, ax, squid_signal(), 3.5)
        self.at("Both answers start")
        pip = electrode(tip=.99)
        self.play(FadeIn(pip, shift=UP * .18), run_time=.65)
        self.play(pip.animate.shift(DOWN * .31), run_time=2.6)
        self.finish()


class S02Title(TitleCard):
    TITLE = TITLE
    LESSON = LESSON

    def construct(self):
        field = ion_field()
        # The title occupies the display, alongside the same preparation.
        title = T(self.TITLE.replace(" Voltage", "\nVoltage").replace(" Currents", "\nCurrents"),
                  45, font=TITLE_FONT,
                  line_spacing=.8).move_to(p(RX, .14))
        rule = Line(p(2.25, -1.73), p(4.67, -1.73), color=GOLD, stroke_width=4)
        self.add(decks(), neuron(), field, electrode(tip=.68))
        self.play(FadeIn(title), GrowFromCenter(rule), run_time=8 / 15)
        self.wait(22 / 15)


class S03Intracellular(SpokenScene):
    def construct(self):
        ax = plot()
        pip = electrode(tip=.68)
        self.add(decks(), neuron(), ion_field(keep_label_space=True), pip, ax, schematic())
        self.at("First")
        self.play(pip.animate.shift(DOWN * 1.21), run_time=1.7)
        draw_signal(self, ax, lambda _: REST, 2.7)
        live = scan(ax, lambda _: REST)
        self.add(live)
        self.at("Inside minus outside")
        difference = screen_heading("Inside − Outside")
        self.play(FadeIn(difference), run_time=.67)
        self.at("membrane potential")
        heading = screen_heading()
        self.play(swap(difference, heading), run_time=.7)
        self.at("neuron resting")
        model = label("Made-up neuron", RX, 1.81, GREY, 28)
        self.play(FadeIn(model), run_time=.6)
        self.at("71 millivolts")
        voltage = label("−71 mV", RX, -.61, BLUE, 43)
        self.play(FadeIn(voltage), run_time=.63)
        self.at("Yet about 200")
        flow = currents()
        self.play(FadeIn(flow), run_time=1.0)
        self.at("potassium leave")
        potassium = label("200 pA\nK⁺ out", CX - 1.42, -2.00, YELLOW, 32)
        self.play(FadeIn(potassium), run_time=.55)
        self.at("of sodium enter")
        sodium = label("200 pA\nNa⁺ in", CX + 1.42, -2.00, YELLOW, 32)
        self.play(FadeIn(sodium), run_time=.55)
        self.at("currents cancel")
        balance = label("Net current = 0 pA", RX, -1.98, YELLOW, 32)
        self.play(FadeIn(balance), run_time=.7)
        self.finish()


def update_on_change(mob, key):
    """Avoid re-typesetting a readout whose displayed value is unchanged."""
    redraw, = mob.updaters
    mob.clear_updaters()
    previous = key()

    def refresh(m):
        nonlocal previous
        value = key()
        if value != previous:
            redraw(m)
            previous = value

    return mob.add_updater(refresh)


def driving_meter(voltage):
    """Marker, bracket and value share the same voltage and equilibrium reference."""
    def level(v):
        return -.95 + (v - EK) * .081

    scale = Line(p(2.05, -1.71), p(2.05, 1.87), color=GREY, stroke_width=4)
    tick = Line(p(1.89, level(EK)), p(2.23, level(EK)), color=PURPLE, stroke_width=6)
    ek = label("K⁺ equilibrium (E)\n−95 mV", 3.75, -1.44, PURPLE, 28)
    marker = always_redraw(lambda: Dot(p(2.05, level(voltage.get_value())),
                                       color=BLUE, radius=.13))
    number = counter("Vm {:.0f} mV", voltage, p(3.53, 1.89), size=32, color=BLUE)
    gap = always_redraw(lambda: VGroup(
        Line(p(4.49, level(EK)), p(4.49, level(voltage.get_value())),
             color=YELLOW, stroke_width=5),
        *(Line(p(4.36, level(v)), p(4.62, level(v)), color=YELLOW, stroke_width=5)
          for v in [EK, voltage.get_value()])
    ))
    force = always_redraw(lambda: M(f"{voltage.get_value() - EK:+.0f} mV", 29, YELLOW)
                          .move_to(p(5.42, (level(EK) + level(voltage.get_value())) / 2)))
    key = lambda: round(voltage.get_value())
    update_on_change(number, key)
    update_on_change(force, lambda: voltage.get_value())
    return VGroup(scale, tick), ek, VGroup(marker, number), VGroup(gap, force)


class S04DrivingForce(SpokenScene):
    def construct(self):
        ax = plot()
        trace = ax.curve(lambda _: REST, color=BLUE)
        v = ValueTracker(REST)
        axis, eqlabel, reading, gap = driving_meter(v)
        self.add(decks(), neuron(), ion_field(keep_label_space=True), electrode(), schematic(), ax, trace)
        self.at("Each ion")
        self.play(ReplacementTransform(ax, axis), FadeOut(trace), run_time=1.2)
        concentration = arrow(CX - 1.42, -.67, 1.25, YELLOW)
        electrical = arrow(CX + 1.42, 1.25, -.67, BLUE)
        self.at("where concentration")
        self.play(GrowArrow(concentration), run_time=1.0)
        self.at("electrical pull")
        self.play(GrowArrow(electrical), run_time=1.0)
        forces = VGroup(label("Concentration\npush", CX - 1.42, -1.89, YELLOW, 28),
                        label("Electrical\npull", CX + 1.42, -1.89, BLUE, 28))
        self.play(FadeIn(forces), run_time=.7)
        self.at("Driving force is")
        formula = screen_heading("Driving force = Vm − E", color=TEXT)
        self.play(FadeIn(formula), run_time=.85)
        self.at("potassium value")
        self.play(FadeIn(eqlabel), run_time=1.35)
        self.at("Minus 71 sits")
        self.add(reading)
        self.play(FadeIn(gap), run_time=.72)
        self.at("24 millivolts above")
        arithmetic = label("−71 − (−95) = +24 mV", RX, -2.51, YELLOW, 32)
        self.play(FadeIn(arithmetic), run_time=.65)
        self.at("potassium is pushed")
        self.play(FadeOut(electrical), FadeOut(forces), run_time=.72)
        self.at("voltage moves")
        self.play(FadeOut(arithmetic), run_time=.29)
        self.play(v.animate.set_value(-64),
                  concentration.animate.scale(1.20, about_point=p(CX - 1.42, MEMBRANE_Y)),
                  run_time=1.49)
        self.at("current changes")
        self.play(v.animate.set_value(-82),
                  concentration.animate.scale(.51, about_point=p(CX - 1.42, MEMBRANE_Y)),
                  run_time=1.25)
        self.play(v.animate.set_value(REST),
                  concentration.animate.scale(1 / (.51 * 1.2), about_point=p(CX - 1.42, MEMBRANE_Y)),
                  run_time=1.25)
        self.finish()


def lock_icon(x, y):
    shackle = Arc(radius=.17, start_angle=0, angle=PI, arc_center=p(x, y + .10),
                  color=GREEN, stroke_width=4)
    case = tile(.46, .28, x, y, GREEN, GREEN, radius=.05)
    return VGroup(shackle, case)


def clamp_records():
    return plot((-105, 20), .22, 1.97), plot((-1.1, 1.1), -2.58, -.84)


def command(x):
    return REST if x < .19 else -42


def opening(x):
    """A repeating illustrative conductance change, expressed as an open fraction."""
    return (.5 - .5 * np.cos(TAU * (x - .19) * 2.1)) ** 3 if x >= .19 else 0


def ionic_current(x):
    # I = g(Vm − E), in relative units, with E fixed.
    return opening(x) * (command(x) - EK) / (-42 - EK)


def clamp_force_label():
    x, y = CX, -2.03
    bracket = VMobject(color=YELLOW, stroke_width=4).set_points_as_corners([
        p(x - 1.65, y + .12), p(x - 1.65, y + .28),
        p(x + 1.65, y + .28), p(x + 1.65, y + .12),
    ])
    return VGroup(bracket, label("Driving force held fixed", x, y - .19, GREEN, 29))


class S05VoltageClamp(SpokenScene):
    def construct(self):
        v = ValueTracker(REST)
        axis, eqlabel, reading, gap = driving_meter(v)
        formula = screen_heading("Driving force = Vm − E", color=TEXT)
        meter = VGroup(axis, eqlabel, reading, gap, formula)
        self.add(decks(), neuron(), ion_field(keep_label_space=True, clamped=True),
                 electrode(), meter, schematic())
        self.at("Voltage clamp")
        lock = lock_icon(CX + .58, 2.42)
        self.play(FadeIn(lock), run_time=.72)
        self.at("holding membrane voltage")
        self.play(Indicate(gap[0], color=YELLOW, scale_factor=1), run_time=.72)
        self.at("pick a voltage", lead=.46)
        vp, ip = clamp_records()
        self.play(FadeOut(meter), run_time=.42)
        self.play(FadeIn(vp), run_time=.26)
        draw_signal(self, vp, command, .68)
        held = screen_heading("Voltage command")
        self.play(FadeIn(held), run_time=.23)
        self.at("electrode injects")
        injection = arrow(CX, 1.57, .05)
        self.play(GrowArrow(injection), run_time=.8)
        pulse(injection, base=8, amp=4, speed=3.4)
        self.at("injected current matches")
        outgoing = arrow(CX - 1.42, -.70, 1.05)
        self.play(GrowArrow(outgoing), run_time=.72)
        pulse(outgoing, base=8, amp=4, speed=3.4)
        self.at("so you measure it")
        self.play(FadeIn(ip), run_time=.55)
        measured = screen_heading("Membrane current", -.32, YELLOW)
        self.play(FadeIn(measured), run_time=.55)
        self.at("With voltage fixed")
        constant = clamp_force_label()
        self.play(FadeIn(constant), run_time=.65)
        self.at("current changes track", lead=.5)
        t = ValueTracker(.01)
        plug = tile(.34, .19, CX - 1.42, MEMBRANE_Y, PURPLE, PURPLE, radius=.035)
        injection.clear_updaters()
        outgoing.clear_updaters()
        for indicator in (injection, outgoing):
            indicator.add_updater(lambda m: m.set_opacity(.18 + .82 * opening(t.get_value())))
        plug.add_updater(lambda m: m.set_opacity(1 - opening(t.get_value())))
        path = ip.live_curve(ionic_current, t, color=YELLOW)
        head = ip.dot(t.get_value, lambda: ionic_current(t.get_value()), color=YELLOW, ring=YELLOW)
        self.add(path, head, plug)
        self.play(t.animate.set_value(1), run_time=3.42, rate_func=linear)
        self.finish()


def egg():
    outer = Ellipse(width=5.02, height=4.81, color=GREY, stroke_width=4,
                    fill_color=CYTOPLASM, fill_opacity=1).move_to(p(CX, -.15))
    inner = Ellipse(width=4.79, height=4.58, color=TEAL, stroke_width=1.7,
                    stroke_opacity=.78).move_to(outer)
    return VGroup(outer, inner)


def sperm(x, y, scale=1):
    head = Ellipse(width=.34, height=.20, color=GREEN, stroke_width=2,
                   fill_color=GREEN, fill_opacity=1)
    xs = np.linspace(-.56, -.11, 24)
    tail = VMobject(color=GREEN, stroke_width=3).set_points_as_corners([
        p(a, .065 * np.sin(21 * (a + .11))) for a in xs
    ])
    return VGroup(head, tail).scale(scale, about_point=ORIGIN).shift(p(x, y))


def egg_signal(x):
    return -1 + 2 / (1 + np.exp(-30 * (x - .38)))


def prediction_setup():
    card = question_card(QUESTION, y=2.15, size=35, max_w=5.28,
                         left=.78, color=GOLD)
    options = VGroup(*[
        boxed_label(option, color, 31, box=(4.84, .73), min_size=28)
        .move_to(p(RX, y))
        for option, color, y in zip(OPTIONS, (BLUE, BLUE), (.34, -1.06))
    ])
    return card, options


def egg_preparation(clamped=False):
    prep = VGroup(egg(), electrode())
    if clamped:
        prep.add(lock_icon(CX + .58, 2.42))
    return prep


class S06PredictQ(SpokenScene):
    def construct(self):
        vp, ip = clamp_records()
        prior = VGroup(vp, ip, vp.curve(command, color=BLUE),
                       ip.curve(ionic_current, color=YELLOW),
                       screen_heading("Voltage command"),
                       screen_heading("Membrane current", -.32, YELLOW))
        cell = neuron()
        ax = plot((-1.6, 1.6), -2.12, 1.97)
        controller = lock_icon(CX + .58, 2.42)
        field = ion_field(keep_label_space=True, clamped=True)
        force = clamp_force_label()
        self.add(decks(), cell, field, electrode(), controller, prior, force, schematic())
        self.at("Holding voltage fixed")
        self.play(FadeOut(force), run_time=.31)
        self.play(ReplacementTransform(cell, egg()), FadeOut(prior),
                  FadeOut(field), FadeOut(controller), run_time=1.1)
        egg_field = egg_ions()
        self.play(FadeIn(ax), FadeIn(egg_field), run_time=.6)
        low = draw_signal(self, ax, lambda _: -1, 2.55)
        self.at("several sea urchin")
        tag = label("Sea urchin egg", CX, -2.93, TEXT, 30)
        self.play(FadeIn(tag), run_time=.65)
        inside = screen_heading("Negative inside")
        self.at("unfertilized egg")
        self.play(FadeIn(inside), run_time=.8)
        tracer = scan(ax, lambda _: -1)
        self.add(tracer)
        self.at("After one sperm")
        first = sperm(-5.79, 1.24)
        self.play(FadeIn(first), run_time=.35)
        self.play(first.animate.shift(p(.35, -.34)), run_time=.95)
        self.at("voltage swings positive")
        self.remove(tracer, low)
        self.play(FadeOut(inside), first.animate.shift(p(.25, 0)), run_time=.27)
        signal = draw_signal(self, ax, egg_signal, 1.2)
        positive = screen_heading("Positive inside")
        second = sperm(-5.95, -1.53, .88)
        self.at("a second rarely")
        self.play(FadeIn(positive), FadeIn(second), run_time=.5)
        self.play(second.animate.shift(p(.60, .14)), run_time=.77)
        self.play(second.animate.rotate(PI).shift(p(-.40, -.24)), run_time=.94)
        self.at("Suppose you clamp")
        self.play(*(FadeOut(m) for m in (first, second, positive, signal, ax)), run_time=.6)
        lock = lock_icon(CX + .58, 2.42)
        self.play(FadeIn(lock), run_time=.75)
        card, options = prediction_setup()
        self.at("then add sperm")
        self.play(FadeIn(options), run_time=.95)
        self.at("What two results")
        self.play(FadeIn(card), run_time=.65)
        self.finish()


class S07PredictPause(PredictPause):
    """Keep the exact snapshot and the 4.5 seconds in the supplied edit."""
    def construct(self):
        self.add(decks(), egg_preparation(clamped=True), egg_ions(), schematic(),
                 label("Sea urchin egg", CX, -2.93, TEXT, 30), *prediction_setup())
        self.wait(self.narration_s)


def outcome_plot(y):
    return Plot((1.15, 5.77, y - .46, y + .48), (0, 1), (-1.52, 1.52),
                color="#8499AE", stroke=2)


class S08PredictA(SpokenScene):
    def construct(self):
        card, options = prediction_setup()
        prep = egg_preparation(clamped=True)
        self.add(decks(), prep, egg_ions(), card, options, schematic(),
                 label("Sea urchin egg", CX, -2.93, TEXT, 30))
        self.at("Timing alone")
        self.play(FadeOut(card), run_time=.8)
        self.at("test both ways")
        pos = label(OPTIONS[0], RX, 2.70, BLUE, 33)
        neg = label(OPTIONS[1], RX, -.13, BLUE, 33)
        self.play(FadeOut(options), run_time=.42)
        pa, na = outcome_plot(1.62), outcome_plot(-1.12)
        self.play(FadeIn(pos), FadeIn(neg), FadeIn(pa), FadeIn(na), run_time=.95)
        self.at("hold an unfertilized egg")
        draw_signal(self, pa, lambda _: 1, 1.35)
        positive_scan = scan(pa, lambda _: 1)
        self.add(positive_scan)
        a, b = sperm(-5.87, 1.42), sperm(-5.87, -.99)
        self.at("before adding sperm")
        self.play(FadeIn(a), FadeIn(b), run_time=.3)
        self.play(a.animate.shift(p(.57, -.37)), b.animate.shift(p(.23, .07)),
                  run_time=1.07)
        self.at("Entry should fail")
        self.play(a.animate.rotate(PI).shift(p(-.44, .15)),
                  b.animate.rotate(PI).shift(p(-.10, -.20)), run_time=.8)
        failed = label("Entry blocked", RX, .64, RED, 31)
        self.play(FadeIn(failed), FadeOut(a), FadeOut(b), run_time=.46)
        self.at("hold it negative")
        draw_signal(self, na, lambda _: -1, .8)
        negative_scan = scan(na, lambda _: -1)
        self.add(negative_scan)
        a, b = sperm(-5.82, 1.36), sperm(-5.92, -.99)
        self.at("as sperm arrive")
        self.play(FadeIn(a), FadeIn(b), run_time=.26)
        self.play(a.animate.shift(p(.75, -.44)), b.animate.shift(p(.25, .12)), run_time=1.03)
        self.at("Extra sperm")
        self.play(a.animate.shift(p(.85, -.20)), b.animate.shift(p(1.21, .19)), run_time=.85)
        self.play(FadeIn(label("Extra sperm enter", RX, -2.14, GREEN, 31)), run_time=.55)
        self.finish()


def fiber():
    """A longitudinal view of muscle or giant axon inside the same bath."""
    body = VMobject(stroke_color=GREY, stroke_width=3,
                    fill_color=CYTOPLASM, fill_opacity=1)
    body.start_new_path(p(CX - 1.98, 1.02))
    body.add_line_to(p(CX + 1.98, 1.02))
    body.add_cubic_bezier_curve_to(p(CX + 3.06, 1.02), p(CX + 3.06, -2.48),
                                  p(CX + 1.98, -2.48))
    body.add_line_to(p(CX - 1.98, -2.48))
    body.add_cubic_bezier_curve_to(p(CX - 3.06, -2.48), p(CX - 3.06, 1.02),
                                  p(CX - 1.98, 1.02))
    body.close_path()
    rims = VGroup(*[
        Line(p(CX - 2.45, y), p(CX + 2.45, y), color=TEAL,
             stroke_width=2.2, stroke_opacity=.45) for y in [-1.91, -1.66, .37, .61]
    ])
    return VGroup(body, rims)


def nerve_ending():
    path = VMobject(color=PURPLE, stroke_width=19).set_points_smoothly(
        [p(-5.68, 2.88), p(-5.37, 2.62), p(-5.03, 2.06), p(-4.65, 1.58)]
    )
    branches = VGroup(*[
        Line(p(-4.66, 1.58), p(x, 1.11), color=PURPLE, stroke_width=10)
        for x in [-5.10, -4.69, -4.23]
    ])
    terminals = VGroup(*[
        Dot(p(x, 1.13), radius=.14, color=PURPLE) for x in [-5.10, -4.69, -4.23]
    ])
    return VGroup(path, branches, terminals)


def spontaneous(x):
    """Schematic miniature potentials: irregular onsets and passive decay."""
    return sum(amplitude * (1 - np.exp(-165 * t)) * np.exp(-38 * t)
               for onset, amplitude in [(0.12, .65), (.26, .96), (.48, .62), (.68, 1), (.77, .74)]
               if (t := x - onset) >= 0)


class S09Controls(SpokenScene):
    def construct(self):
        e = egg_preparation(clamped=True)
        field = egg_ions()
        self.add(decks(), e, field, schematic())
        self.at("one other sea urchin")
        other = label("One other sea urchin\nNo electrical block", RX, 1.30, TEXT, 32)
        self.play(FadeIn(other), run_time=1.2)
        self.at("reviews conclude")
        mouse = label("Mouse eggs\nNo electrical block (reviews)", RX, -.66, TEXT, 32)
        self.play(FadeIn(mouse), run_time=1.35)
        self.at("recorded small", lead=.8)
        muscle = fiber()
        ax = plot((-.24, 1.18))
        self.play(FadeOut(field), FadeOut(other), FadeOut(mouse),
                  ReplacementTransform(e, muscle), run_time=.9)
        nerve = nerve_ending()
        pip = electrode(-4.5, -.97)
        self.play(FadeIn(nerve), FadeIn(pip), FadeIn(ax), run_time=.7)
        credit = screen_heading("Fatt & Katz", color=GOLD)
        context = label("Frog muscle", CX, -2.90, TEXT, 31)
        self.play(FadeIn(credit), FadeIn(context), run_time=.46)
        trace = draw_signal(self, ax, spontaneous, 3.25)
        self.at("Move the electrode")
        distance = ValueTracker(0)
        decay = lambda x: spontaneous(x) * np.exp(-3.8 * distance.get_value())
        moving_signal = always_redraw(lambda: ax.curve(decay, color=BLUE, width=6))
        live = scan(ax, decay)
        self.remove(trace)
        self.add(moving_signal, live)
        self.play(pip.animate.shift(RIGHT * 2.18), distance.animate.set_value(1), run_time=4.1)
        self.at("arise at the nerve ending")
        site = label("Nerve ending", -2.55, 2.56, PURPLE, 30)
        self.play(FadeIn(site), run_time=.65)
        self.play(Indicate(nerve[2], color=PURPLE, scale_factor=1.3), run_time=1.4)
        self.finish()


class S10UnlockedRecording(SpokenScene):
    def construct(self):
        ax = plot()
        pip = electrode(-4.5, -.97)
        self.add(decks(), fiber(), pip, ax, schematic())
        baseline = ax.curve(lambda _: -65, color=BLUE)
        live = scan(ax, lambda _: -65)
        self.add(baseline, live)
        self.at("1939")
        credit = screen_heading("Hodgkin & Huxley, 1939", color=GOLD)
        self.play(FadeIn(credit), run_time=.85)
        self.at("pushed an electrode")
        self.play(pip.animate.shift(p(1.15, .44)), run_time=2.65)
        axon = label("Squid giant axon", CX, -2.91, TEXT, 31)
        self.play(FadeIn(axon), run_time=.52)
        self.at("Theory said")
        zero = ax.hline(0, color=GREY)
        self.play(Create(zero), run_time=1.2)
        expected = label("Expected stop · 0 mV", RX, .20, GREY, 30)
        self.at("stop near zero")
        self.play(FadeIn(expected), run_time=.6)
        self.at("Instead")
        self.remove(live, baseline)
        self.play(FadeOut(expected), run_time=.31)
        draw_signal(self, ax, squid_signal(), 2.73)
        self.at("inside became positive")
        positive = label("Peak above 0 mV", 4.68, 1.66, BLUE, 30, 3.15)
        self.play(FadeIn(positive), run_time=.61)
        self.finish()


def hair_body():
    return tile(3.60, 3.57, CX, -.88, CYTOPLASM, GREY, radius=.74, stroke=3)


def bundle(deflection):
    group = VGroup()
    for i in range(7):
        x = CX - .82 + .25 * i
        height = .67 + .15 * i
        group.add(Line(p(x, .92), p(x + deflection * height, .92 + height),
                       color=TEAL, stroke_width=8))
    return group


def frog_response(displacement):
    """Schematic saturation matching the 15 mV amplitude and 20 mV/μm peak slope
    reported by Hudspeth and Corey (1977). The shape is an illustrative fit.
    https://pmc.ncbi.nlm.nih.gov/articles/PMC432181/
    """
    return 15 * np.tanh(displacement * 20 / 15)


class S10bUnlockedHair(SpokenScene):
    def construct(self):
        ax = plot((-1, 16), -2.24, 1.83)
        cell = hair_body()
        d = ValueTracker(0)
        hairs = always_redraw(lambda: bundle(d.get_value() * .22))
        pip = electrode(CX + 1.03, -.70, 1.81).rotate(-.64, about_point=p(CX + 1.03, -.70))
        probe = always_redraw(lambda: Line(p(-5.75 + .34 * d.get_value(), 2.30),
                                           p(-3.84 + .34 * d.get_value(), 1.57),
                                           color=GREY, stroke_width=7))
        self.add(decks(), cell, hairs, pip, ax, schematic())
        credit = screen_heading("Hudspeth & Corey, 1977", color=GOLD)
        self.at("1977")
        self.play(FadeIn(credit), run_time=.85)
        self.at("pushed the sensing")
        self.play(FadeIn(probe), run_time=.58)
        response = lambda x: frog_response(2.3 * x)
        fraction = lambda: d.get_value() / 1.61
        live = always_redraw(lambda: ax.curve(response, x1=fraction(), color=BLUE))
        marker = ax.dot(fraction, lambda: response(fraction()), color=BLUE, ring=BLUE)
        self.add(live, marker)
        self.play(d.animate.set_value(.25), run_time=2.25)
        name = label("Bullfrog hair cell", CX, -2.96, TEXT, 30)
        self.at("while recording inside")
        self.play(FadeIn(name), run_time=.65)
        self.play(d.animate.set_value(.52), run_time=1.2)
        self.at("voltage grew smoothly")
        axis = screen_heading("Bundle displacement", y=-2.78, color=TEAL)
        self.play(d.animate.set_value(1.03), FadeIn(axis), run_time=2.45, rate_func=linear)
        self.at("up to about 15")
        cap = label("Up to ~15 mV\nFrog preparation", 4.38, .15, BLUE, 31)
        self.play(d.animate.set_value(1.61), FadeIn(cap), run_time=3.0, rate_func=linear)
        self.finish()


def node_tissue():
    return VGroup(*[
        tile(4.45, .85, CX + .38 * (-1) ** i, -.64 + (i - 1) * .92,
             CYTOPLASM, TEAL, radius=.38, stroke=2.8)
        for i in range(3)
    ])


PACEMAKER_STEPS = ((0, -42), (.18, -57), (.48, -70), (.75, -83))


def pacemaker_voltage(x):
    return next(v for onset, v in reversed(PACEMAKER_STEPS) if x >= onset)


def pacemaker_current(x, gain):
    """Schematic inward I_f. A first-order gate follows each voltage step
    from the preceding open fraction. Gain illustrates the effect of adrenaline.
    https://pubmed.ncbi.nlm.nih.gov/7230019/
    """
    steady = lambda v: 1 / (1 + np.exp((v + 68) / 8))
    gate = steady(PACEMAKER_STEPS[0][1])
    for (onset, voltage), (next_onset, _) in zip(PACEMAKER_STEPS, (*PACEMAKER_STEPS[1:], (1, None))):
        interval = min(x, next_onset) - onset
        target = steady(voltage)
        gate = target + (gate - target) * np.exp(-15 * interval)
        if x <= next_onset:
            return gain * gate * (pacemaker_voltage(x) + 20) / 70

class S11UnlockedClamp(SpokenScene):
    def construct(self):
        vp, ip = clamp_records()
        tissue = node_tissue()
        pip = electrode()
        self.add(decks(), tissue, pip, schematic())
        self.at("1980")
        credit = screen_heading("Brown & DiFrancesco, 1980", color=GOLD)
        self.play(FadeIn(credit), run_time=.7)
        self.at("studied rabbit")
        name = label("Rabbit sinoatrial node", CX, -2.83, TEXT, 30)
        self.play(FadeIn(name), FadeIn(vp), run_time=.65)
        self.play(pip.animate.shift(DOWN * .23), run_time=.7)
        lock = lock_icon(CX + .58, 2.42)
        self.play(FadeIn(lock), run_time=.5)
        self.at("heart's pacemaker")
        cmd = draw_signal(self, vp, pacemaker_voltage, 2.1)
        self.at("recorded a current")
        measured = screen_heading("Pacemaker current", -.32, YELLOW)
        self.play(FadeIn(ip), FadeIn(measured), run_time=.45)
        trace = draw_signal(self, ip, lambda x: pacemaker_current(x, .68), 2.7, color=YELLOW)
        self.at("adrenaline increased")
        adrenaline = label("Adrenaline", CX - .94, 2.91, ORANGE, 34)
        wave = Line(p(CX - 2.42, 1.85), p(CX + 2.42, 1.85), color=ORANGE,
                    stroke_width=13, stroke_opacity=.84)
        self.play(FadeIn(adrenaline), FadeIn(wave), run_time=.41)
        gain = ValueTracker(.68)
        new_trace = always_redraw(lambda: ip.curve(
            lambda x: pacemaker_current(x, gain.get_value()), color=YELLOW, width=6))
        self.remove(trace)
        self.add(new_trace)
        self.play(wave.animate.shift(DOWN * 2.19).set_stroke(opacity=.20),
                  gain.animate.set_value(1.14), run_time=1.75)
        self.remove(wave)
        self.at("Read voltage inside")
        self.play(FadeOut(adrenaline), Indicate(pip, color=BLUE, scale_factor=1.03), run_time=.9)
        self.at("hold it steady")
        self.play(Indicate(cmd, color=BLUE, scale_factor=1.02), run_time=.84)
        self.at("expose the currents")
        current_scan = scan(ip, lambda x: pacemaker_current(x, 1.14), color=YELLOW, period=1.8)
        self.add(current_scan)
        self.finish()


class S12End(EndCard):
    LINE = "Record voltage from inside; hold it fixed to measure the currents."
