"""Tracer flux assays, synchronized to the supplied narration.

GREY membrane and accessory proteins; teal candidate; PURPLE channels and
enzyme markers; BLUE water; YELLOW transported solute and current; ORANGE
added reagents and heat; GREEN intact seals; RED leaks; GOLD dates and rules.
"""
from bp_parts import *
from bp_style import EndCard

PURPLE = "#B58CD9"
ORANGE = "#F29E4C"
LUMEN = "#244954"
BATH = "#172E38"
CORE = "#343945"

CENTER = np.array([-2.10, -0.18, 0])
RADIUS = 2.58
PORT = CENTER + RIGHT * (RADIUS - 0.15)
BATH_POINTS = [(1.55, 1.38), (1.61, 0.53), (1.67, -0.92), (1.31, -1.68)]
GAUGE_X = 4.33
INNER_POINTS = [(-1.23, 0.87), (-2.22, 1.35), (-2.91, -0.80), (-1.56, -1.31)]
QUESTION = "Nothing crosses — wrong protein?"
PAUSE_RESET = 0.42


def point(x, y):
    return np.array([x, y, 0.0])


def heading(text, x=-2.10, color=TEXT):
    return T(text, 32, color, weight=BOLD).move_to(point(x, 3.13))


def beside(text, y, color=TEXT, size=32):
    return T(text, size, color).move_to(point(3.58, y))


def particle(xy, color=YELLOW, radius=0.14):
    return Dot(point(*xy), radius=radius, color=color, stroke_width=2, stroke_color=TEXT)


def particles(positions, color=YELLOW, radius=0.14):
    return VGroup(*(particle(xy, color, radius) for xy in positions))


def diffuse(group, amplitude=0.38, speed=2.2):
    """Bounded drift around each particle's location, with distinct phases."""
    for index, dot in enumerate(group):
        home = dot.get_center().copy()
        phase = index * 1.9
        dot.motion_time = 0.0

        def drift(mob, dt, home=home, phase=phase):
            mob.motion_time += dt
            t = speed * mob.motion_time
            mob.move_to(home + amplitude * point(
                0.70 * (np.cos(t + phase) - np.cos(phase)),
                np.sin(0.87 * t + phase) - np.sin(phase),
            ))

        dot.add_updater(drift)
    return group


def settle(group):
    for dot in group:
        dot.clear_updaters()
    return group


def animate_fluid(fluid, color=LUMEN):
    """A slow lighting shift makes the fluid visible during held diagram beats."""
    base = ManimColor(color)
    light = interpolate_color(base, ManimColor(TEAL), 0.46)
    shade = interpolate_color(base, ManimColor(BG), 0.23)
    fluid.motion_time = 0.0

    def shimmer(mob, dt):
        mob.motion_time += dt
        strength = (1 + np.sin(2.55 * mob.motion_time - 0.38)) / 2
        mob.set_fill(interpolate_color(shade, light, strength), opacity=1)

    return fluid.add_updater(shimmer)


def flat_membrane(oily=False):
    """Two geometric leaflets between the outer bath and inner fluid."""
    def band(x, width, color):
        corners = [point(x + dx * width / 2, -0.18 + dy * 2.61)
                   for dx, dy in ((-1, -1), (1, -1), (1, 1), (-1, 1))]
        return Polygon(*corners, stroke_width=0, fill_color=color, fill_opacity=1)

    outer = band(-5.14, 2.54, BATH)
    inner = band(-1.20, 4.30, LUMEN)
    core = band(-3.54, 0.73, "#634B29" if oily else CORE)
    leaflets = VGroup(
        band(-3.91, 0.13, GREY),
        band(-3.18, 0.13, GREY),
    )
    return VGroup(outer, inner, core, leaflets)


def vesicle(gap=0, center=CENTER, radius=RADIUS):
    """The carried double leaflet and lumen, with an optional breach at the right."""
    thickness = 0.29
    lumen = Circle(radius=radius - thickness, stroke_width=0,
                   fill_color=LUMEN, fill_opacity=1).move_to(center)
    # Keep the same arc topology as the opening widens.
    angle = TAU - 2 * gap
    core = AnnularSector(inner_radius=radius - thickness, outer_radius=radius,
                         start_angle=gap, angle=angle, stroke_width=0,
                         fill_color=CORE, fill_opacity=1).shift(center)
    edges = [
        Arc(radius=edge, start_angle=gap, angle=angle, arc_center=center,
            stroke_width=3, color=GREY)
        for edge in (radius, radius - thickness)
    ]
    rim = VGroup(core, *edges)
    return VGroup(lumen, rim)


def protein(at=PORT, color=TEAL, channel=False):
    """Cartoon transport protein. Its lobes distinguish its two faces."""
    pair = VGroup(*[
        RoundedRectangle(width=1.15, height=height, corner_radius=0.16,
                         fill_color=color, fill_opacity=1, stroke_color=BG, stroke_width=3)
        for height in (0.34, 0.28)
    ]).arrange(DOWN, buff=0.18 if channel else 0.015)
    pair[0].shift(RIGHT * 0.20)
    if channel:
        pore = Rectangle(width=0.55, height=0.18, stroke_width=0,
                         fill_color=BG, fill_opacity=1).move_to(pair)
        pair.add_to_back(pore)
    return pair.move_to(at)


def companion(angle):
    location = CENTER + (RADIUS - 0.13) * point(np.cos(angle), np.sin(angle))
    return protein(location, GREY).scale(0.53).rotate(angle)


def arrow(start, end, color=YELLOW):
    return Arrow(start, end, buff=0, color=color, stroke_width=5, tip_length=0.18)


def route(dot, through, destination):
    return MoveAlongPath(dot, VMobject().set_points_smoothly(
        [dot.get_center(), *through, destination]), rate_func=smooth)


def gauge(level, labels=("Outside", "Inside"), amounts=None, color=YELLOW):
    """Bars and their live values use the same normalized amount."""
    amounts = amounts or (lambda: 1 - level.get_value(), level.get_value)
    result = VGroup()
    for y, label, amount in zip((0.74, -0.85), labels, amounts):
        track = RoundedRectangle(width=3.70, height=0.40, corner_radius=0.10,
                                 stroke_color=GREY, stroke_width=2,
                                 fill_color=CORE, fill_opacity=1).move_to(point(GAUGE_X, y))
        left = track.get_left() + RIGHT * 0.085

        def fill(amount=amount, left=left):
            fraction = np.clip(amount(), 0, 1)
            width = max(0.002, 3.53 * fraction)
            return Rectangle(width=width, height=0.23, stroke_width=0,
                             fill_color=color, fill_opacity=float(fraction > 0)
                             ).move_to(left + RIGHT * width / 2)

        result.add(T(label, 28).move_to(point(GAUGE_X, y + 0.55)), track, always_redraw(fill))
    return result


def atp_token():
    return (
        beside("ATP", -2.12, ORANGE, 30),
        particle((1.42, -2.12), ORANGE, 0.19),
    )


def unknown_slot():
    center = point(-3.54, -0.18)
    slot = RoundedRectangle(width=0.88, height=1.05, corner_radius=0.20, color=GOLD,
                            fill_color=BG, fill_opacity=1).move_to(center)
    return VGroup(slot, T("?", 40, GOLD).move_to(center))


def predict_frame():
    level = ValueTracker(0)
    bath = particles(BATH_POINTS)
    bars = VGroup(gauge(level), T("0", 28, YELLOW).move_to(point(GAUGE_X, -1.45)))
    diagram = VGroup(vesicle(), protein(), bars, scope_tag())
    question = question_card(QUESTION, y=3.24, size=36)
    return diagram, bath, question


class S01Hook(TitleCard, SpokenScene):
    TITLE = "Tracking What Crosses a Membrane"
    LESSON = "Tracer Flux Assays"

    def construct(self):
        sodium = particle((-4.84, -0.69), radius=0.16)
        water = particle((-5.66, 0.85), BLUE, 0.224)
        diagram = flat_membrane()
        self.at("Why does water")
        self.add(diagram, sodium, water, scope_tag())
        animate_fluid(diagram[1])
        comparison = beside("Crossing rate", 2.27)
        faster = beside("~10 billion times faster", -1.73, BLUE, 30)
        # Use decades relative to sodium, with one decade of room below 1×.
        scale = beside("Log scale", -2.26, TEXT, 28)
        ratios = (("Na⁺", "1×", 1, YELLOW, 1.06), ("Water", "10¹⁰×", 10**10, BLUE, -0.25))
        rows = VGroup()
        for name, value, ratio, color, y in ratios:
            start = point(1.58, y)
            rows.add(
                T(name, 28, color).move_to(point(2.30, y + 0.40)),
                T(value, 28, color).move_to(point(5.00, y + 0.40)),
                Line(start, start + RIGHT * 4.00, color=CORE, stroke_width=12),
                Line(start, start + RIGHT * 4 * (1 + np.log10(ratio)) / 11,
                     color=color, stroke_width=12),
            )
        self.play(
            route(sodium, [point(-4.10, -0.55)], point(-5.65, -1.26)),
            route(water, [point(-3.53, 0.70)], point(-1.59, 1.22)),
            run_time=2.18,
        )
        self.at("10 billion times")
        self.play(FadeIn(comparison), FadeIn(rows), FadeIn(scale), run_time=0.54)
        self.play(FadeIn(faster), run_time=0.42)
        self.play(
            route(sodium, [point(-4.11, -0.64)], point(-5.02, -0.93)),
            water.animate.move_to(point(-2.47, 0.34)), run_time=2.44,
        )
        self.at("Sodium is about")
        sodium_size = T("Na⁺ ~1.0 Å", 30, YELLOW).move_to(point(-5.07, -1.95))
        self.play(FadeIn(sodium_size), run_time=0.37)
        self.play(route(sodium, [point(-4.11, -0.68)], point(-5.28, -0.51)),
                  water.animate.move_to(point(-0.12, 0.72)), run_time=2.45)
        self.at("Water is about")
        water_size = T("Water ~1.4 Å", 30, BLUE).move_to(point(-0.93, 2.76))
        self.play(FadeIn(water_size), run_time=0.44)
        self.play(
            route(water, [point(-3.52, 0.79)], point(-5.62, 0.99)),
            route(sodium, [point(-4.12, -0.60)], point(-5.33, -0.72)), run_time=2.03,
        )
        self.at("How do scientists prove")
        self.play(FadeOut(VGroup(comparison, rows, scale, faster, sodium_size, water_size, water)),
                  run_time=0.44)
        slot = unknown_slot()
        pulse(slot[0], base=5, amp=2.8, speed=5)
        title = T(self.TITLE, 38, font=TITLE_FONT).move_to(point(1.25, 3.31))
        lesson = T(self.LESSON, 28, TEAL).move_to(point(1.25, 2.76))
        self.play(FadeIn(slot), run_time=0.52)
        self.wait(0.57)
        self.play(FadeIn(title), FadeIn(lesson), run_time=0.44)
        self.wait(0.87)
        self.play(FadeOut(title), FadeOut(lesson), run_time=0.32)
        self.finish()


class S02Barrier(SpokenScene):
    def construct(self):
        diagram = flat_membrane()
        sodium = particle((-5.33, -0.72), radius=0.16)
        scope = scope_tag()
        self.at("Sodium loses")
        slot = unknown_slot()
        self.add(diagram, sodium, scope, slot)
        animate_fluid(diagram[1])
        self.play(route(sodium, [point(-4.10, -0.58)], point(-5.53, -0.47)), run_time=2.33)
        self.at("oily core")
        flat_heading = heading("Oily core", -3.54, ORANGE)
        self.play(Transform(diagram, flat_membrane(oily=True)),
                  FadeOut(slot), FadeIn(flat_heading), run_time=0.55)
        self.at("Gases like oxygen")
        oxygen = particles([(-6.08, 1.03), (-5.59, 0.33), (-5.82, -0.24)], TEXT, 0.12)
        gas = beside("Oxygen diffuses", 1.68)
        self.play(FadeIn(oxygen), run_time=0.40)
        self.play(
            FadeIn(gas),
            LaggedStart(*(route(dot, [point(-3.52, y)], point(-0.36 - i * 0.75, y + 0.45))
                          for i, (dot, y) in enumerate(zip(oxygen, (1.14, 0.48, -0.17)))),
                        lag_ratio=0.20),
            run_time=3.17,
        )
        self.at("leaving water for oil")
        sugar = particle((-5.88, -1.52), radius=0.22)
        blocked = beside("Ions and sugars", 1.68, YELLOW)
        self.play(swap(gas, blocked), FadeIn(sugar), FadeOut(oxygen), run_time=0.65)
        self.play(
            route(sodium, [point(-4.10, -0.58)], point(-5.18, -0.62)),
            route(sugar, [point(-4.18, -1.62)], point(-5.54, -1.55)), run_time=2.57,
        )
        self.play(
            route(sugar, [point(-4.17, -1.41)], point(-5.86, -1.63)),
            route(sodium, [point(-4.10, -0.53)], point(-5.50, -0.36)), run_time=1.50,
        )
        self.at("So cells build")
        slot_position = point(-3.54, -0.18)
        channel = protein(slot_position, TEAL, channel=True)
        label = beside("Transport protein", 1.68, TEAL)
        self.play(FadeIn(channel, shift=RIGHT * 1.25), swap(blocked, label), FadeOut(sugar), run_time=0.72)
        sodium.set_z_index(10)
        self.play(route(sodium, [slot_position], point(-1.38, -0.13)), run_time=1.84)
        self.at("To measure transport")
        self.play(FadeOut(sodium), FadeOut(label), run_time=0.52)
        tracer = beside("Labelled tracer", 1.68, YELLOW)
        dots = particles([(1.63, 1.02), (1.78, -0.98)])
        self.at("scientists follow tracers")
        self.play(FadeIn(dots, shift=LEFT * 0.42), FadeIn(tracer), run_time=0.65)
        world = vesicle()
        diagram[1].clear_updaters()
        self.play(FadeOut(diagram), FadeOut(flat_heading), FadeOut(channel),
                  FadeIn(world), FadeIn(protein()), run_time=1.20)
        animate_fluid(world[0])
        self.at("across sealed")
        self.play(FadeOut(tracer), FadeOut(dots), run_time=0.57)
        self.finish()


class S03VesicleAssay(SpokenScene):
    def construct(self):
        level = ValueTracker(0)
        bars = gauge(level)
        pump = protein()
        world = vesicle()
        self.at("First researchers isolate")
        self.add(world, pump, scope_tag())
        animate_fluid(world[0])
        name = heading("Vesicle")
        self.play(Create(world[1].copy(), remover=True), run_time=1.58)
        self.at("sealed bubbles")
        self.play(FadeIn(name), run_time=0.60)
        self.play(Indicate(world[1], color=GREY, scale_factor=1.025), run_time=1.45)
        self.at("They add a tracked")
        solute = particles(BATH_POINTS)
        self.play(FadeIn(bars),
                  LaggedStart(*(FadeIn(dot, shift=LEFT * 0.45) for dot in solute),
                              lag_ratio=0.24), run_time=1.32)
        diffuse(solute, amplitude=0.29)
        self.at("plus any fuel")
        fuel_name, fuel = atp_token()
        self.play(FadeIn(fuel), run_time=0.32)
        self.play(FadeIn(fuel_name), fuel.animate.move_to(point(0.73, -0.59)), run_time=1.58)
        self.at("When transport runs")
        self.play(Indicate(pump, color=TEAL, scale_factor=1.1), FadeOut(fuel), FadeOut(fuel_name), run_time=0.65)
        settle(solute)
        self.play(
            LaggedStart(*(route(dot, [PORT], point(*xy)) for dot, xy in zip(solute, INNER_POINTS)),
                        lag_ratio=0.30),
            level.animate.set_value(1), run_time=5.15,
        )
        self.finish()


class S04Reconstitution(SpokenScene):
    def construct(self):
        world, candidate = vesicle(), protein()
        solute = diffuse(particles(INNER_POINTS))
        others = VGroup(*(companion(angle) for angle in (0.95, 1.82, 2.64, 3.54, 4.48)))
        self.at("Yet a cell vesicle")
        self.add(world, candidate, solute, scope_tag())
        animate_fluid(world[0])
        self.play(LaggedStart(*(FadeIn(block) for block in others), lag_ratio=0.26),
                  run_time=2.63)
        self.at("To test one candidate")
        candidate_name = beside("Candidate protein", 1.32, TEAL)
        self.play(candidate.animate.move_to(point(3.58, 0.40)), run_time=1.56)
        self.play(FadeIn(candidate_name), run_time=0.48)
        self.at("scientists purify it")
        self.play(FadeOut(others), FadeOut(solute), run_time=1.12)
        self.at("They place it into")
        self.play(FadeOut(candidate_name), FadeIn(heading("Liposome")), run_time=0.58)
        self.play(candidate.animate.move_to(PORT), run_time=1.72)
        outside = particles(BATH_POINTS)
        self.play(LaggedStart(*(FadeIn(dot, shift=LEFT * 0.50) for dot in outside),
                              lag_ratio=0.27), run_time=1.64)
        self.finish()


class S05PredictQ(SpokenScene):
    def construct(self):
        diagram, bath, question = predict_frame()
        self.at("Pause and predict")
        self.add(diagram[0], diagram[1], diagram[3])
        fluid = animate_fluid(diagram[0][0])
        name = heading("Liposome")
        self.play(FadeIn(name), run_time=0.46)
        self.play(Indicate(diagram[0][1], color=GREY, scale_factor=1.04), run_time=1.8)
        self.at("You purify a candidate")
        self.play(Indicate(diagram[1], color=TEAL, scale_factor=1.18), run_time=1.6)
        self.at("into bare liposomes")
        self.play(Indicate(diagram[0][1], color=GREY, scale_factor=1.025), run_time=1.17)
        self.at("You add the solute")
        self.play(FadeIn(bath, shift=LEFT * 0.46), run_time=0.62)
        diffuse(bath, amplitude=0.32)
        self.at("nothing crosses")
        self.play(FadeIn(diagram[2]), run_time=0.52)
        self.at("Does that prove")
        self.play(swap(name, question), run_time=0.70)
        hold_at = self.narration_s + 0.4 - PAUSE_RESET - 0.50
        self.wait(max(0.07, hold_at - self.elapsed()))
        fluid.clear_updaters()
        self.play(fluid.animate.set_fill("#306C77"), run_time=0.50)
        settle(bath)
        self.play(fluid.animate.set_fill(LUMEN),
                  *(dot.animate.move_to(point(*xy)) for dot, xy in zip(bath, BATH_POINTS)),
                  run_time=PAUSE_RESET, rate_func=linear)
        self.finish()


class S06PredictPause(Scene):
    def construct(self):
        self.camera.background_color = BG
        diagram, bath, question = predict_frame()
        self.add(diagram, bath, question)
        self.wait(float(os.environ["KX_DURATION"]))


class S07PredictAnswer(SpokenScene):
    def construct(self):
        diagram, bath, question = predict_frame()
        world, candidate, bars, scope = diagram
        answer = question_card("Not necessarily.", y=3.24, size=36)
        self.at("Not necessarily")
        self.add(world, candidate, bars, scope, bath, question)
        animate_fluid(world[0])
        diffuse(bath, amplitude=0.36)
        self.play(swap(question, answer), FadeOut(bars), run_time=0.73)
        self.at("A failure")
        partner = companion(0.33)
        start = partner.get_center() + point(1.68, 0.65)
        partner_name = beside("Partner protein", 2.11)
        self.play(FadeIn(partner.move_to(start)), run_time=0.55)
        self.at("may only mean")
        self.play(partner.animate.move_to(companion(0.33)), run_time=1.10)
        self.play(FadeIn(partner_name), run_time=0.40)
        chosen = bath[1]
        chosen.clear_updaters()
        self.play(route(chosen, [PORT], point(-1.78, 0.35)), run_time=1.52)
        self.at("Orientation matters")
        self.play(FadeOut(partner), FadeOut(answer), FadeOut(partner_name), run_time=0.42)
        orient = beside("Pump orientation", 2.11, TEAL)
        self.play(Rotate(candidate, PI), FadeIn(orient), run_time=1.03)
        self.at("placed backward")
        pushes = arrow(point(0.40, 0.34), point(1.82, 0.34))
        self.play(GrowArrow(pushes),
                  route(chosen, [PORT], point(2.30, -0.27)), run_time=2.52)
        self.at("And a channel")
        channel = protein(color=PURPLE, channel=True)
        gradient = beside("Downhill push", 2.11, PURPLE)
        self.play(FadeOut(pushes), Transform(candidate, channel), swap(orient, gradient), run_time=0.77)
        drive = arrow(point(1.78, 0.56), point(0.55, 0.56))
        self.play(GrowArrow(drive), run_time=0.55)
        self.play(route(chosen, [PORT], point(-1.67, -0.38)), run_time=2.46)
        self.at("without a concentration")
        self.play(FadeOut(drive), swap(gradient, beside("No downhill push", 2.11, PURPLE)),
                  run_time=0.65)
        # Hold equal distributions on both sides while the channel remains open.
        settle(bath)
        two_sides = diffuse(particles([(-1.56, -0.43), (-2.29, 0.83), (1.75, 0.83), (1.68, -0.88)]),
                            amplitude=0.39)
        self.play(FadeOut(bath), FadeIn(two_sides), run_time=0.60)
        self.finish()


class S08ControlsLeak(SpokenScene):
    def construct(self):
        world, pump = vesicle(), protein(color=PURPLE, channel=True)
        inside = particles(INNER_POINTS)
        level = ValueTracker(1)
        test_bath = diffuse(particles([(1.25, 1.38), (1.25, 0.53)]), amplitude=0.22)
        self.at("Controls also guard")
        self.add(world, pump, inside, test_bath, scope_tag())
        animate_fluid(world[0])
        control_center = point(3.58, -0.18)
        control = vesicle(center=control_center, radius=1.73)
        name = T("No protein", 32, GREEN).move_to(point(3.58, 2.22))
        self.play(FadeIn(control), run_time=1.0)
        animate_fluid(control[0])
        self.at("liposomes measure")
        self.play(FadeIn(name), run_time=0.43)
        leak = particle((5.92, -0.18), RED, 0.10)
        self.play(FadeIn(leak), run_time=0.43)
        self.play(route(leak, [point(5.13, -0.19)], point(4.47, -0.38)), run_time=2.63)
        self.at("Without an intact seal")
        bars = gauge(level, labels=("Outside", "Inside"), color=RED)
        control[0].clear_updaters()
        self.play(FadeOut(VGroup(control, name, leak)), FadeOut(test_bath), run_time=0.47)
        self.play(Transform(world, vesicle(gap=0.26)), FadeIn(bars), FadeOut(pump), run_time=0.65)
        self.play(LaggedStart(*(route(dot, [PORT], point(*xy))
                                for dot, xy in zip(inside, BATH_POINTS)), lag_ratio=0.23),
                  level.animate.set_value(0), run_time=2.60)
        self.at("In a cell sheet")
        left_cell = vesicle(center=point(-2.54, -0.26), radius=2.28)
        right_cell = vesicle(center=point(2.54, -0.26), radius=2.28)
        clasp = RoundedRectangle(width=0.90, height=0.36, corner_radius=0.13,
                                 color=GREEN, fill_color=GREEN, fill_opacity=1).move_to(point(0, 0.47))
        self.play(FadeOut(bars), FadeOut(inside),
                  ReplacementTransform(world, left_cell), run_time=0.58)
        self.play(FadeIn(right_cell), run_time=0.48)
        animate_fluid(left_cell[0])
        animate_fluid(right_cell[0])
        self.at("tight seals")
        self.play(GrowFromCenter(clasp), run_time=0.43)
        label = heading("Tight seal", 0, GREEN)
        drops = particles([(-0.28, 2.51), (0.05, 2.13), (0.32, 2.52)])
        self.play(FadeIn(label), FadeIn(drops), run_time=0.47)
        self.play(LaggedStart(*(route(dot, [point((i - 1) * 0.07, 0.88)],
                                      point((i - 1) * 0.27, 1.63 + i * 0.32))
                                for i, dot in enumerate(drops)), lag_ratio=0.21), run_time=2.45)
        diffuse(drops, amplitude=0.28)
        self.finish()


class S09ControlsLatency(SpokenScene):
    def construct(self):
        intact, total = 10, 100
        hidden = total - intact
        activity = ValueTracker(intact)
        world = vesicle()
        enzymes = VGroup(*[
            RoundedRectangle(width=0.56, height=0.36, corner_radius=0.15, color=PURPLE,
                             fill_color=PURPLE, fill_opacity=0.78).move_to(point(*xy))
            for xy in INNER_POINTS
        ])
        substrate = diffuse(particles(BATH_POINTS), amplitude=0.31)
        self.at("Another check asks")
        self.add(world, substrate, scope_tag())
        animate_fluid(world[0])
        self.play(LaggedStart(*(GrowFromCenter(marker) for marker in enzymes), lag_ratio=0.35),
                  run_time=1.68)
        self.at("enzyme sits inside")
        enzyme = heading("Enzyme", -2.10, PURPLE)
        blocked = beside("Substrate", 1.65, YELLOW)
        self.play(FadeIn(enzyme), run_time=0.55)
        self.play(FadeIn(blocked), run_time=0.50)
        self.at("stuck outside")
        self.play(Indicate(world[1], color=GREY, scale_factor=1.035), run_time=1.35)
        self.at("Detergent opens")
        drops = particles([(2.18, 0.75), (2.33, -0.65)], ORANGE, 0.20)
        detergent = beside("Detergent", 1.65, ORANGE)
        self.play(swap(blocked, detergent), FadeIn(drops), run_time=0.55)
        self.play(LaggedStart(*(dot.animate.move_to(PORT + UP * ((i - 0.5) * 0.7))
                                for i, dot in enumerate(drops)), lag_ratio=0.28), run_time=1.36)
        self.play(Transform(world, vesicle(gap=0.34)), FadeOut(drops), run_time=0.51)
        settle(substrate)
        self.play(LaggedStart(*(route(dot, [PORT], point(x + 0.47, y + 0.20))
                               for dot, (x, y) in zip(substrate, INNER_POINTS)),
                             lag_ratio=0.18), run_time=1.35)
        diffuse(substrate, amplitude=0.34)
        self.at("Suppose intact vesicles")
        settle(substrate)
        self.play(FadeOut(detergent), FadeOut(substrate), Transform(world, vesicle()), run_time=0.47)
        substrate = diffuse(particles(BATH_POINTS), amplitude=0.35)
        self.add(substrate)
        bars = gauge(activity, labels=("Activity",), amounts=(lambda: activity.get_value() / total,),
                     color=PURPLE)
        readout = counter("{:.0f}%", activity, point(GAUGE_X, -0.06), color=PURPLE)
        condition = T("Intact", 28).move_to(point(GAUGE_X, -0.69))
        self.at("10 of the activity")
        self.play(FadeIn(bars), FadeIn(readout), FadeIn(condition), run_time=0.64)
        self.at("detergent raises it")
        settle(substrate)
        self.play(swap(condition, T("+ detergent", 28, ORANGE).move_to(point(GAUGE_X, -0.69))),
                  Transform(world, vesicle(gap=0.34)), run_time=0.58)
        self.play(LaggedStart(*(route(dot, [PORT], point(x + 0.47, y + 0.20))
                               for dot, (x, y) in zip(substrate, INNER_POINTS)), lag_ratio=0.18),
                  activity.animate.set_value(total), run_time=1.47)
        diffuse(substrate, amplitude=0.37)
        self.at("Hidden equals total")
        formula = beside("Hidden = Total − Intact", -1.43, TEXT, 30)
        self.play(FadeIn(formula), run_time=0.57)
        math = M(f"{total}% − {intact}%", 30).move_to(point(2.98, -2.17))
        answer = M(f"= {hidden}%", 30, GREEN).next_to(math, RIGHT, buff=0.20)
        self.at("100 minus 10")
        self.play(FadeIn(math), run_time=0.50)
        self.at("90 inside")
        self.play(FadeIn(answer), FadeIn(beside("Inside", -2.76, GREEN, 28)), run_time=0.48)
        self.finish()


class S10UnlockedVesicles(SpokenScene):
    def construct(self):
        level = ValueTracker(0)
        world, pump = vesicle(), protein()
        calcium = particles([(1.69, 0.72), (1.69, -0.64)], radius=0.18)
        self.at("These assays unlocked")
        self.add(world, pump, scope_tag())
        animate_fluid(world[0])
        self.play(FadeIn(calcium, shift=LEFT * 0.45), run_time=0.65)
        diffuse(calcium, amplitude=0.40)
        self.at("In 1961")
        date = beside("1961", 2.20, GOLD, 42)
        self.play(FadeIn(date), run_time=0.51)
        fuel_name, fuel = atp_token()
        self.at("added a TP")
        self.play(FadeIn(fuel), run_time=0.30)
        self.play(FadeIn(fuel_name), fuel.animate.move_to(point(0.73, -0.59)), run_time=1.15)
        self.at("muscle vesicles")
        name = heading("Muscle vesicles")
        bars = gauge(level)
        self.play(FadeIn(name), FadeIn(bars), run_time=0.55)
        self.play(Indicate(pump, color=TEAL, scale_factor=1.15), FadeOut(fuel), FadeOut(fuel_name), run_time=0.69)
        self.at("Calcium left")
        settle(calcium)
        self.play(LaggedStart(*(route(dot, [PORT], point(-1.65 - i * 0.90, 0.70 - i * 1.44))
                              for i, dot in enumerate(calcium)), lag_ratio=0.40),
                  level.animate.set_value(1), run_time=2.65)
        diffuse(calcium, amplitude=0.49)
        self.at("independently reported")
        date_range = beside("1961–1962", 2.20, GOLD, 38)
        self.play(swap(date, date_range), run_time=1.15)
        self.at("The cost was about")
        ratio = beside("~2 Ca²⁺ per ATP", -2.02, YELLOW, 36)
        self.play(FadeIn(ratio), run_time=0.55)
        self.finish()


class S11UnlockedReconst(SpokenScene):
    def construct(self):
        world, carrier = vesicle(), protein()
        egg = vesicle(radius=3.00)
        egg_port = CENTER + RIGHT * 2.85
        egg_name = heading("Frog oocyte").shift(UP * 0.25)
        self.at("Expressed in frog")
        self.add(world, carrier, scope_tag())
        animate_fluid(world[0])
        self.play(Transform(world, egg), carrier.animate.move_to(egg_port), run_time=1.14)
        self.play(FadeIn(egg_name), run_time=0.48)
        self.at("human SGLT1")
        carrier_name = beside("SGLT1", 1.88, TEAL, 38)
        cargo = VGroup(particle((2.08, 0.74)), particle((2.27, -0.43)),
                       particle((1.90, -1.36), radius=0.23))
        self.play(FadeIn(cargo, shift=LEFT * 0.40), FadeIn(carrier_name), run_time=0.74)
        self.at("moves two sodium")
        ratio = beside("2 Na⁺ : 1 sugar", -2.00, YELLOW)
        self.play(LaggedStart(*(route(dot, [egg_port], point(x, y))
                                for dot, (x, y) in zip(cargo, INNER_POINTS)),
                              lag_ratio=0.29, run_time=2.0),
                  FadeIn(ratio, run_time=0.40))
        self.at("Purified rat channel")
        self.play(FadeOut(cargo), FadeOut(egg_name), FadeOut(ratio), FadeOut(carrier_name), run_time=0.46)
        self.play(Transform(world, vesicle()),
                  Transform(carrier, protein(color=PURPLE, channel=True)), run_time=1.32)
        channel_name = beside("TRPV1", 2.67, PURPLE, 38)
        liposome_name = heading("Liposome")
        self.play(FadeIn(channel_name), FadeIn(liposome_name), run_time=0.52)
        self.at("a rapid heat jump")
        heat = Circle(radius=0.38, stroke_width=7, color=ORANGE).move_to(PORT)
        self.play(heat.animate.scale(5.5).set_stroke(opacity=0.0), run_time=0.80)
        self.remove(heat)
        # Cao et al., Neuron (2013), doi:10.1016/j.neuron.2012.12.016, Fig. 4F.
        # Normalized single-exponential rise using the reported 3.5 ms time constant.
        tau_ms = 3.5
        current = lambda t: -np.expm1(-t / tau_ms)
        graph = Plot(box=(1.72, 6.20, -1.95, 1.52), xr=(0, 12), yr=(0, 1.08),
                     xticks=(0, 4, 8, 12), xlabel="Time (ms)",
                     ylabel="Relative current", size=28, label_size=28, color=TEXT)
        elapsed_ms = ValueTracker(0)
        curve = graph.live_curve(current, elapsed_ms, color=YELLOW)
        self.at("its current rose")
        self.play(FadeIn(graph), run_time=0.53)
        self.add(curve)
        self.play(elapsed_ms.animate.set_value(12), run_time=1.35, rate_func=linear)
        self.at("milliseconds")
        time_constant = beside("~3.5 ms", -3.09, YELLOW, 32).shift(LEFT * 1.12)
        self.play(FadeIn(time_constant), run_time=0.43)
        self.at("Isolating membranes")
        self.play(FadeOut(VGroup(graph, curve, channel_name, time_constant)), FadeOut(liposome_name),
                  run_time=0.67)
        clean = Group(world, carrier)
        self.play(clean.animate.shift(RIGHT * 2.10).scale(1.09), run_time=1.75)
        self.play(Indicate(world[1], color=GREY, scale_factor=1.04),
                  Indicate(carrier, color=PURPLE, scale_factor=1.09), run_time=1.63)
        self.finish()


class S12End(EndCard):
    LINE = "Measure transport across sealed membranes, then test one purified protein alone."
