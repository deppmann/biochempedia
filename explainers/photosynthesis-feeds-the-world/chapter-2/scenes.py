from bp_parts import *


# COLOR MAP — identical concepts keep one colour throughout both chapters.
# light/energy: GOLD; carbon dioxide: TEAL; water: BLUE; sugar/rate: GREEN;
# wood: BROWN; temperature/heat: RED; chamber/structure: GREY.
BROWN = "#9A6A42"


def rate_from_light(x):
    """A computed schematic saturation curve, normalized to 0..1."""
    return 1.0 - np.exp(-4.0 * max(0.0, x))


def rate_from_temperature(x):
    """A computed schematic optimum curve, normalized to 0..1."""
    return max(0.0, 4.0 * x * (1.0 - x))


BLUEBERRY_LIGHT = np.array([25, 51, 301, 701, 1000, 1500], dtype=float)
BLUEBERRY_UPTAKE = np.array([0.18, 1.21, 6.96, 9.11, 9.73, 9.95], dtype=float)


def blueberry_uptake(x):
    """Piecewise-linear interpolation of the lesson's six displayed measurements."""
    return float(np.interp(x, BLUEBERRY_LIGHT, BLUEBERRY_UPTAKE))


def plant(center=(-2.7, -0.25, 0), height=3.6):
    """The carried plant picture, always rebuilt at the same scale and position."""
    stem = Line(DOWN * 1.25, UP * 0.95, color=GREEN, stroke_width=12)
    branches = VGroup(
        Line(UP * 0.35, UP * 0.82 + LEFT * 0.62, color=GREEN, stroke_width=8),
        Line(UP * 0.12, UP * 0.58 + RIGHT * 0.7, color=GREEN, stroke_width=8),
        Line(DOWN * 0.38, LEFT * 0.65 + UP * 0.02, color=GREEN, stroke_width=7),
    )
    leaves = VGroup(
        Ellipse(1.15, 0.55, color=GREEN, fill_color=GREEN, fill_opacity=0.75).rotate(0.35).move_to([-0.83, 0.9, 0]),
        Ellipse(1.2, 0.58, color=GREEN, fill_color=GREEN, fill_opacity=0.75).rotate(-0.3).move_to([0.92, 0.68, 0]),
        Ellipse(1.05, 0.52, color=GREEN, fill_color=GREEN, fill_opacity=0.75).rotate(0.28).move_to([-0.86, 0.02, 0]),
        Ellipse(1.0, 0.5, color=GREEN, fill_color=GREEN, fill_opacity=0.75).rotate(-0.22).move_to([0.48, 1.25, 0]),
    )
    pot = VGroup(
        Polygon([-0.75, -1.18, 0], [0.75, -1.18, 0], [0.5, -1.72, 0], [-0.5, -1.72, 0],
                color=BROWN, fill_color=BROWN, fill_opacity=0.75),
        Line([-0.82, -1.18, 0], [0.82, -1.18, 0], color=BROWN, stroke_width=9),
    )
    g = VGroup(stem, branches, leaves, pot)
    g.set_height(height).move_to(center)
    g.leaves = leaves
    return g


def lock_mark(at, scale=1.0):
    body = RoundedRectangle(width=0.38 * scale, height=0.32 * scale, corner_radius=0.05,
                            color=GREY, fill_color=BG, fill_opacity=1, stroke_width=3)
    shackle = Arc(radius=0.14 * scale, start_angle=0, angle=PI, color=GREY, stroke_width=3)
    shackle.next_to(body, UP, buff=-0.03 * scale)
    return VGroup(body, shackle).move_to(at)


def sugar_meter(tracker, center=(4.65, -1.55, 0), height=2.1, width=0.62, label=True):
    c = np.array(center, dtype=float)
    outline = RoundedRectangle(width=width, height=height, corner_radius=0.12,
                               color=GREEN, stroke_width=3).move_to(c)

    def fill():
        h = max(0.04, (height - 0.16) * np.clip(tracker.get_value(), 0, 1))
        return Rectangle(width=width - 0.16, height=h, stroke_width=0, fill_color=GREEN,
                         fill_opacity=0.8).align_to(outline, DOWN).set_x(outline.get_x()).shift(UP * 0.08)

    g = VGroup(outline, always_redraw(fill))
    if label:
        g.add(T("SUGAR RATE", 28, GREEN).next_to(outline, DOWN, buff=0.18))
    return g


def light_beam(tracker, target=(-2.7, 0.8, 0), start=(-4.4, 1.65, 0)):
    start = np.array(start, dtype=float)
    target = np.array(target, dtype=float)

    def beam():
        strength = np.clip(tracker.get_value(), 0, 1)
        spread = 0.12 + 0.38 * strength
        poly = Polygon(start + [0, spread, 0], start - [0, spread, 0],
                       target - [0, 0.38, 0], target + [0, 0.38, 0],
                       stroke_color=GOLD, stroke_width=2 + 5 * strength,
                       fill_color=GOLD, fill_opacity=0.08 + 0.25 * strength)
        return poly

    return always_redraw(beam)


def chamber_world(light, co2, temp, rate, locks=(), sway=True):
    """The full carried chamber; all continuing scenes call this builder."""
    frame = RoundedRectangle(width=12.2, height=5.55, corner_radius=0.22, color=GREY,
                             stroke_width=3).move_to([0, 0.05, 0])
    floor = Line([-5.85, -2.08, 0], [5.85, -2.08, 0], color=GREY, stroke_width=2)
    p = plant()
    beam = light_beam(light)
    water = VGroup(*[
        Line([-4.75 + i * 0.23, -1.93, 0], [-4.75 + i * 0.23, -1.63 - 0.08 * (i % 2), 0],
             color=BLUE, stroke_width=5) for i in range(7)
    ])
    d_light = dial(light, [-4.85, 1.92, 0], radius=0.7, label="LIGHT", color=GOLD, size=26)
    d_co2 = dial(co2, [1.75, 1.78, 0], radius=0.78, label="CO₂", color=TEAL, size=26)
    d_temp = dial(temp, [4.75, 1.78, 0], radius=0.78, label="TEMP", color=RED, size=26)
    meter = sugar_meter(rate)
    g = VGroup(frame, floor, beam, water, p, d_light, d_co2, d_temp, meter)
    if sway:
        bob(p.leaves, amp=0.12, speed=1.5)
    for name, pos in (("light", [-4.85, 1.15, 0]), ("co2", [1.75, 0.98, 0]), ("temp", [4.75, 0.98, 0])):
        if name in locks:
            g.add(lock_mark(pos, 0.9))
    return g


def chamber_plot(box=(-5.75, 0.25, -1.35, 2.45)):
    return Plot(box=box, xr=(0, 1), yr=(0, 1.05), xticks=[0, 0.5, 1],
                yticks=[0, 0.5, 1], xlabel="light", ylabel="photosynthesis rate")


def plot_area(P, fn, x0, x1, color=GREEN, opacity=0.16, n=100):
    """Computed fill beneath a plotted curve, kept behind axes and labels."""
    xs = np.linspace(x0, x1, n)
    pts = [P.pt(x0, P.yr[0]), *[P.pt(x, fn(x)) for x in xs], P.pt(x1, P.yr[0])]
    return Polygon(*pts, stroke_width=0, fill_color=color, fill_opacity=opacity).set_z_index(-2)


def live_plot_area(P, fn, tracker, x0, color=GREEN, opacity=0.16):
    return always_redraw(lambda: plot_area(P, fn, x0, max(x0 + 1e-4, tracker.get_value()), color, opacity))


def traveling_marker(P, fn, xr, color=GOLD, seconds=7.0):
    """A continuous, visible trace along the subject curve during an explanation."""
    dot = Dot(P.pt(xr[0], fn(xr[0])), radius=0.2, color=color, stroke_color=TEXT, stroke_width=2)
    dot._travel_t = 0.0

    def move(mob, dt):
        mob._travel_t += dt
        phase = 0.5 - 0.5 * np.cos(TAU * mob._travel_t / seconds)
        x = xr[0] + phase * (xr[1] - xr[0])
        mob.move_to(P.pt(x, fn(x)))

    return dot.add_updater(move)


def small_chamber_controls(light, rate, lock_others=True):
    p = plant(center=(3.45, -0.72, 0), height=2.75)
    beam = light_beam(light, target=(3.45, 0.1, 0), start=(1.7, 1.55, 0))
    dl = dial(light, [3.45, 2.35, 0], radius=0.68, label="LIGHT", color=GOLD, size=26)
    meter = sugar_meter(rate, center=(5.55, -0.25, 0), height=2.65)
    g = VGroup(beam, p, dl, meter)
    if lock_others:
        fixed = VGroup(chip("CO₂  fixed", TEAL, 24), chip("TEMP  fixed", RED, 24)).arrange(DOWN, buff=0.18)
        fixed.move_to([1.75, -2.35, 0])
        g.add(fixed)
    bob(p.leaves, amp=0.12, speed=1.5)
    return g


def predict_backdrop():
    P = chamber_plot(box=(-5.8, 0.15, -1.15, 2.5))
    area = plot_area(P, rate_from_light, 0, 1)
    curve = P.curve(rate_from_light, color=GREEN)
    pulse(curve, base=7, amp=4, speed=1.4)
    marker = Dot(P.pt(0.72, rate_from_light(0.72)), radius=0.22, color=GOLD)
    pulse(marker, base=7, amp=5, speed=3.0)
    first = chip("BRIGHT", GOLD, 24).move_to([1.25, 2.15, 0])
    arrow = Arrow([2.15, 2.15, 0], [2.8, 2.15, 0], color=GOLD, buff=0, stroke_width=5)
    twice = chip("TWICE AS BRIGHT", GOLD, 24).move_to([4.55, 2.15, 0])
    bright = VGroup(first, arrow, twice)
    schematic = T("schematic", 24, GREY).move_to([-0.55, 2.82, 0])
    p = plant(center=(1.65, -0.55, 0), height=2.0)
    bob(p.leaves, amp=0.12, speed=1.5)
    beam = light_beam(ValueTracker(0.9), target=(1.65, 0.0, 0), start=(0.45, 1.45, 0))
    return VGroup(area, P, curve, marker, bright, schematic, beam, p)


class S00Hook(SpokenScene):
    def construct(self):
        light, co2, temp, rate = (ValueTracker(v) for v in (0.14, 0.5, 0.5, 0.1))
        p = plant(center=(-1.2, -0.25, 0), height=4.3)
        sugar = chip("SUGAR", GREEN, 30).move_to([2.0, 0.55, 0])
        wood = chip("WOOD", BROWN, 30).move_to([4.55, 0.55, 0])
        a1 = Arrow(p.get_right(), sugar.get_left(), color=GREEN, buff=0.18)
        a2 = Arrow(sugar.get_right(), wood.get_left(), color=BROWN, buff=0.18)
        self.play(FadeIn(p), GrowArrow(a1), FadeIn(sugar), GrowArrow(a2), FadeIn(wood), run_time=1.6)
        self.at("Now ask how fast")
        q = fit_text("How fast can sugar-building go?", max_w=10.5, size=42, color=GOLD)
        q.move_to([0, 3.1, 0])
        self.play(FadeIn(q), run_time=0.8)
        self.at("If light powers")
        stop = T("Why can brighter light stop helping?", 38, GOLD).move_to([0, -2.95, 0])
        self.play(swap(q, stop), FadeOut(VGroup(a1, a2, sugar, wood)), run_time=1.0)
        self.at("Place the same plant")
        world = chamber_world(light, co2, temp, rate)
        # Grade 7 readers: spell out the dial abbreviations where they first appear.
        legend = VGroup(T("CO₂ = carbon dioxide", 26, TEAL), T("TEMP = temperature", 26, RED)).arrange(RIGHT, buff=0.9)
        legend.move_to([1.6, 3.38, 0])
        self.play(ReplacementTransform(p, world[4]), FadeIn(VGroup(*[m for i, m in enumerate(world) if i != 4])),
                  FadeIn(legend), FadeOut(stop), run_time=1.2)
        self.at("Its light dial")
        self.play(light.animate.set_value(0.2), run_time=1.0)
        self.at("A sugar meter")
        self.play(rate.animate.set_value(0.12), run_time=1.1)
        self.at("We will change")
        one = caption("Change one condition at a time.", color=TEXT)
        self.play(FadeIn(one), run_time=0.7)
        self.finish()


class S01Title(TitleCard):
    LESSON = "Photosynthesis Feeds the World"
    TITLE = "Why More Light Stops Helping"

    def construct(self):
        light, co2, temp, rate = (ValueTracker(v) for v in (0.22, 0.5, 0.5, 0.12))
        world = chamber_world(light, co2, temp, rate)
        world = VGroup(*world[:5])  # chamber, water, beam and plant continue behind the brief title
        world.set_opacity(0.34)
        panel = RoundedRectangle(width=9.8, height=2.55, corner_radius=0.2, stroke_width=0,
                                 fill_color=BG, fill_opacity=0.94).move_to([0, 0.55, 0])
        title = T(self.TITLE, 50, TEXT, font=TITLE_FONT).move_to([0, 0.35, 0])
        lesson = T(self.LESSON.upper(), 22, TEAL).next_to(title, UP, buff=0.3)
        rule = Line(LEFT * 1.4, RIGHT * 1.4, color=GOLD, stroke_width=5).next_to(title, DOWN, buff=0.35)
        self.add(world)
        self.add(panel)
        self.play(FadeIn(lesson), Write(title), GrowFromCenter(rule),
                  light.animate.set_value(0.32), rate.animate.set_value(0.16), run_time=1.35)
        self.play(FadeOut(VGroup(panel, lesson, title, rule)), light.animate.set_value(0.38), run_time=0.55)
        self.finish()


class S02Rate(SpokenScene):
    def construct(self):
        light, rate = ValueTracker(0.05), ValueTracker(0.04)
        P = chamber_plot()
        x = ValueTracker(0.02)
        area = live_plot_area(P, rate_from_light, x, 0.0)
        live = P.live_curve(rate_from_light, x, color=GREEN)
        dot = P.dot(lambda: x.get_value(), lambda: rate_from_light(x.get_value()), color=GREEN, ring=GOLD)
        controls = small_chamber_controls(light, rate)
        self.play(Create(P), FadeIn(controls), run_time=1.3)
        self.add(area, live, dot, scope_tag("schematic"))
        self.at("Here it tracks")
        self.play(Indicate(controls[3], color=GREEN, scale_factor=1.08), run_time=0.7)
        self.at("Turn the light")
        self.play(light.animate.set_value(0.45), x.animate.set_value(0.45),
                  rate.animate.set_value(rate_from_light(0.45)), run_time=5.2, rate_func=linear)
        self.at("More light helps")
        low = P.curve(rate_from_light, x0=0.02, x1=0.62, color=GOLD, width=10)
        self.play(ShowPassingFlash(low, time_width=0.9), light.animate.set_value(0.62),
                  x.animate.set_value(0.62), rate.animate.set_value(rate_from_light(0.62)),
                  run_time=4.2, rate_func=linear)
        self.finish()


class S03Bend(SpokenScene):
    def construct(self):
        light, rate, x = ValueTracker(0.58), ValueTracker(rate_from_light(0.58)), ValueTracker(0.58)
        P = chamber_plot()
        area = plot_area(P, rate_from_light, 0, 1)
        curve = P.curve(rate_from_light, color=GREEN)
        pulse(curve, base=7, amp=3, speed=1.2)
        dot = P.dot(lambda: x.get_value(), lambda: rate_from_light(x.get_value()), color=GREEN, ring=GOLD)
        controls = small_chamber_controls(light, rate)
        self.add(area, P, curve, dot, controls, scope_tag("schematic"))
        self.play(light.animate.set_value(0.68), x.animate.set_value(0.68),
                  rate.animate.set_value(rate_from_light(0.68)), run_time=1.5)
        self.at("The curve still rises")
        steps = VGroup()
        for xa, xb in ((0.35, 0.5), (0.5, 0.65), (0.65, 0.8)):
            steps.add(Arrow(P.pt(xa, rate_from_light(xa)), P.pt(xb, rate_from_light(xb)),
                            buff=0.03, color=GOLD, stroke_width=4, max_tip_length_to_length_ratio=0.18))
        self.play(LaggedStart(*[GrowArrow(a) for a in steps], lag_ratio=0.35),
                  light.animate.set_value(0.8), x.animate.set_value(0.8),
                  rate.animate.set_value(rate_from_light(0.8)), run_time=4.2)
        self.at("Soon it bends")
        plateau = P.curve(rate_from_light, x0=0.62, x1=1, color=GOLD, width=11)
        self.play(ShowPassingFlash(plateau, time_width=1.0), run_time=2.0)
        self.at("The beam brightens again")
        self.play(light.animate.set_value(1.0), x.animate.set_value(1.0),
                  rate.animate.set_value(rate_from_light(1.0)), run_time=3.0)
        self.at("Light is plentiful")
        tag = chip("LIGHT PLENTIFUL", GOLD, 26).move_to([-3.6, -2.75, 0])
        self.play(FadeIn(tag), FadeOut(steps), run_time=0.8)
        self.finish()


class S04Predict(SpokenScene):
    def construct(self):
        back = predict_backdrop()
        self.add(back)
        self.at("If the light")
        q = question_card("Will doubling bright light double the rate?",
                          ["rate doubles", "rate changes little"], chips_at=[5.0, -0.25, 0],
                          left=-5.9, max_w=6.4, size=29)
        self.play(FadeIn(q.question), run_time=0.8)
        self.play(FadeIn(q.chips), run_time=1.0)
        self.at("Watch the curve")
        self.play(Indicate(back[2], color=GOLD, scale_factor=1.35), run_time=1.0)
        self.finish()


class S05Pause(PredictPause):
    QUESTION = "Will doubling bright light double the rate?"
    OPTIONS = ["rate doubles", "rate changes little"]
    CHIPS_AT = [5.0, -0.25, 0]
    CARD = {"left": -5.9, "max_w": 6.4, "size": 29}
    SECONDS = 4.5

    def backdrop(self):
        return predict_backdrop()


class S06Reveal(SpokenScene):
    def construct(self):
        P = chamber_plot(box=(-5.8, 0.15, -1.2, 2.5))
        area = plot_area(P, rate_from_light, 0, 1)
        curve = P.curve(rate_from_light, color=GREEN)
        pulse(curve, base=7, amp=3, speed=1.2)
        x = ValueTracker(0.72)
        dot = P.dot(lambda: x.get_value(), lambda: rate_from_light(x.get_value()), color=GREEN, ring=GOLD)
        light = ValueTracker(0.72)
        rate = ValueTracker(rate_from_light(0.72))
        controls = small_chamber_controls(light, rate, lock_others=False)
        self.add(area, P, curve, dot, controls, scope_tag("schematic"))
        self.play(x.animate.set_value(1.0), light.animate.set_value(1.0),
                  rate.animate.set_value(rate_from_light(1.0)), run_time=1.6)
        little = T("RATE CHANGES LITTLE", 28, GREEN).move_to([-2.65, -2.45, 0])
        self.play(FadeIn(little), run_time=0.7)
        self.at("Something else")
        limit = chip("LIMIT", GOLD, 28).move_to([3.55, -2.45, 0])
        self.play(FadeOut(little), FadeIn(limit), run_time=0.8)
        self.at("A limiting condition")
        brake = Line([2.55, 1.55, 0], [4.25, 1.55, 0], color=RED, stroke_width=12)
        self.play(GrowFromCenter(brake), run_time=1.0)
        self.at("When one condition")
        self.play(FadeOut(limit), light.animate.set_value(0.92), run_time=1.0)
        self.at("a different one")
        unknowns = VGroup(
            chip("CO₂ ?", TEAL, 27), chip("TEMP ?", RED, 27), chip("LEAF ?", TEXT, 27)
        ).arrange(DOWN, buff=0.22).move_to([3.65, 0.0, 0])
        self.remove(controls)
        self.play(FadeOut(brake), LaggedStart(*[FadeIn(m) for m in unknowns], lag_ratio=0.25), run_time=1.5)
        self.at("The level curve")
        plateau = P.curve(rate_from_light, x0=0.62, x1=1, color=GOLD, width=11)
        self.play(ShowPassingFlash(plateau, time_width=0.9), run_time=1.3)
        not_name = caption("A plateau reveals a limit — not its identity.", color=TEXT)
        self.at("but it does not")
        self.play(FadeIn(not_name), run_time=0.7)
        self.finish()


class S07OtherDials(SpokenScene):
    def construct(self):
        co2, temp, rate = ValueTracker(0.25), ValueTracker(0.18), ValueTracker(0.62)
        light_lock = chip("BRIGHT LIGHT  fixed", GOLD, 25).move_to([-3.7, 2.65, 0])
        dco2 = dial(co2, [-3.7, 0.65, 0], radius=1.25, label="CO₂", color=TEAL, size=34)
        meter = sugar_meter(rate, center=(-0.9, 0.25, 0), height=3.3)
        self.play(FadeIn(light_lock), FadeIn(dco2), FadeIn(meter), run_time=1.1)
        self.play(co2.animate.set_value(0.35), rate.animate.set_value(0.66), run_time=2.2, rate_func=linear)
        self.at("Raising it may")
        may = T("may rise", 28, GREEN).move_to([-0.9, 2.25, 0])
        self.play(co2.animate.set_value(0.82), rate.animate.set_value(0.88), FadeIn(may),
                  run_time=3.5, rate_func=linear)
        self.at("Temperature also")
        P = Plot(box=(1.25, 6.05, -1.35, 2.2), xr=(0, 1), yr=(0, 1.05),
                 xticks=[(0, "cold"), (0.5, "warm"), (1, "hot")], yticks=[0, 1],
                 xlabel="temperature", ylabel="rate")
        curve = P.curve(rate_from_temperature, color=GREEN)
        area = plot_area(P, rate_from_temperature, 0, 1)
        pulse(curve, base=7, amp=3, speed=1.2)
        tdot = P.dot(lambda: temp.get_value(), lambda: rate_from_temperature(temp.get_value()), color=RED)
        self.play(FadeOut(VGroup(dco2, may)), rate.animate.set_value(0.62), FadeIn(area), FadeIn(P), FadeIn(curve), FadeIn(tdot),
                  run_time=1.2)
        self.at("Warming can speed")
        self.play(temp.animate.set_value(0.5), rate.animate.set_value(1.0), run_time=2.8, rate_func=linear)
        self.at("Too much heat")
        self.play(temp.animate.set_value(0.95), rate.animate.set_value(rate_from_temperature(0.95)),
                  run_time=2.2, rate_func=linear)
        self.at("These conditions interact")
        links = VGroup(Arrow(light_lock.get_right(), P.get_top(), color=GREY, buff=0.15),
                       Arrow(P.get_left(), meter.get_right(), color=GREY, buff=0.15))
        self.play(LaggedStart(*[GrowArrow(a) for a in links], lag_ratio=0.3), run_time=1.4)
        self.add(scope_tag("schematic"))
        self.finish()


class S08Rule(SpokenScene):
    def construct(self):
        rule = fit_text("Light powers sugar-building from carbon dioxide and water; conditions limit its speed.",
                        max_w=12.2, size=30, color=TEXT, max_lines=2)
        rule.move_to([0, 3.25, 0])
        self.play(Write(rule), run_time=5.4)
        self.at("This rule keeps")
        panels = TwoPanel("ENERGY + MATTER", "RATE", colors=(GOLD, GREEN), top=2.55, bottom=-2.35)
        self.play(FadeIn(panels), run_time=0.9)
        left = VGroup(chip("LIGHT", GOLD, 24), chip("CARBON DIOXIDE", TEAL, 24), chip("WATER", BLUE, 24))
        left.arrange(DOWN, buff=0.18).move_to([-4.75, -0.05, 0])
        sugar = chip("SUGAR", GREEN, 28).move_to([-1.25, -0.05, 0])
        matter_arrow = Arrow([-3.35, -0.05, 0], [-2.05, -0.05, 0], color=GREEN, buff=0, stroke_width=5)
        flow = VGroup(left, matter_arrow, sugar)
        light, co2, temp = ValueTracker(0.12), ValueTracker(0.12), ValueTracker(0.12)
        dials = VGroup(dial(light, [1.55, 0.65, 0], radius=0.62, label="LIGHT", color=GOLD, size=24),
                       dial(co2, [3.45, 0.65, 0], radius=0.62, label="CO₂", color=TEAL, size=24),
                       dial(temp, [5.35, 0.65, 0], radius=0.62, label="TEMP", color=RED, size=24))
        rate_tracker = ValueTracker(0.12)
        rate = sugar_meter(rate_tracker, center=(3.45, -1.55, 0), height=1.65, label=False)
        rate_label = T("RATE", 28, GREEN).next_to(rate, RIGHT, buff=0.25)
        right = VGroup(dials, rate, rate_label)
        self.at("The first asks")
        self.play(FadeIn(flow), run_time=1.5)
        self.at("The second asks")
        self.play(FadeIn(right), light.animate.set_value(0.75), co2.animate.set_value(0.55),
                  temp.animate.set_value(0.5), rate_tracker.animate.set_value(0.72),
                  run_time=4.0, rate_func=linear)
        connector = Arrow([-0.05, 2.0, 0], [0.05, 2.0, 0], color=TEAL,
                          buff=0.0, stroke_width=5)
        self.at("Answering one")
        self.play(GrowArrow(connector), rate_tracker.animate.set_value(0.84), run_time=1.1)
        self.finish()


def blueberry_plot():
    P = Plot(box=(-6.0, -0.55, -1.55, 2.25), xr=(0, 1500), yr=(0, 10.5),
             xticks=[(25, "25"), (301, "301"), (701, "701"), (1000, "1,000"), (1500, "1,500")],
             yticks=[0, 5, 10], xlabel="light", ylabel="carbon dioxide taken in (net)", size=22, label_size=24)
    line = P.curve(blueberry_uptake, x0=25, x1=1500, color=GREEN, n=300)
    dots = VGroup(*[Dot(P.pt(x, y), radius=0.095, color=GREEN) for x, y in zip(BLUEBERRY_LIGHT, BLUEBERRY_UPTAKE)])
    return P, line, dots


class S09Evidence(SpokenScene):
    def construct(self):
        P, line, dots = blueberry_plot()
        trace = traveling_marker(P, blueberry_uptake, (25, 1500), color=GOLD, seconds=8.0)
        x = ValueTracker(25)
        live = P.live_curve(blueberry_uptake, x, color=GREEN, x0=25)
        area = live_plot_area(P, blueberry_uptake, x, 25)
        rows = [(f"{x:,.0f}", f"{y:.2f}", GREEN) for x, y in zip(BLUEBERRY_LIGHT, BLUEBERRY_UPTAKE)]
        table = Ledger(rows, top_left=(0.15, 2.35), title="light     uptake", row_h=0.48,
                       key_w=2.0, width=5.8, size=24)
        source = fit_text("measured, approximate values read from Figure 4", max_w=5.8,
                          size=24, color=GREY, max_lines=2).move_to([3.0, -1.65, 0])
        self.play(Create(P), FadeIn(table), run_time=1.1)
        self.add(area, live, trace)
        self.play(x.animate.set_value(301), FadeIn(dots[0]), FadeIn(dots[1]), FadeIn(dots[2]),
                  table.reveal(0), table.reveal(1), table.reveal(2), run_time=2.7, rate_func=linear)
        self.at("At low light")
        self.play(x.animate.set_value(701), FadeIn(dots[3]), table.reveal(3), run_time=3.1, rate_func=linear)
        low = P.curve(blueberry_uptake, x0=25, x1=301, color=GOLD, width=12, n=80)
        self.play(ShowPassingFlash(low, time_width=0.8), run_time=1.4)
        self.at("At high light")
        high = P.curve(blueberry_uptake, x0=1000, x1=1500, color=GOLD, width=12, n=80)
        self.play(x.animate.set_value(1500), FadeIn(dots[4]), FadeIn(dots[5]),
                  table.reveal(4), table.reveal(5), ShowPassingFlash(high, time_width=0.8),
                  run_time=2.8, rate_func=linear)
        self.at("Those measurements")
        boundary = DashedLine(P.pt(700, 0), P.pt(700, 10.5), color=GREY, stroke_width=3)
        self.play(Create(boundary), FadeIn(source), run_time=1.2)
        self.at("They do not identify")
        unknown = chip("NEXT LIMIT ?", TEXT, 28).move_to([3.0, -2.65, 0])
        self.play(FadeIn(unknown), run_time=0.8)
        self.finish()


class S10Return(SpokenScene):
    def construct(self):
        P = chamber_plot(box=(-5.95, -0.65, -1.45, 2.35))
        area = plot_area(P, rate_from_light, 0, 1)
        curve = P.curve(rate_from_light, color=GREEN)
        trace = traveling_marker(P, rate_from_light, (0.03, 0.98), color=GOLD, seconds=7.0)
        pulse(curve, base=7, amp=3, speed=1.1)
        light, co2, temp, rate = (ValueTracker(v) for v in (0.7, 0.45, 0.45, 0.78))
        p = plant(center=(3.25, -0.82, 0), height=2.7)
        meter = sugar_meter(rate, center=(5.55, -0.7, 0), height=2.6)
        dials = VGroup(dial(light, [2.1, 2.2, 0], radius=0.68, label="LIGHT", color=GOLD, size=24),
                       dial(co2, [3.75, 2.2, 0], radius=0.68, label="CO₂", color=TEAL, size=24),
                       dial(temp, [5.35, 2.2, 0], radius=0.68, label="TEMP", color=RED, size=24))
        self.add(area, P, curve, trace, p, meter, dials, scope_tag("schematic"))
        bob(p.leaves, amp=0.12, speed=1.5)
        self.at("A steep rise")
        steep = P.curve(rate_from_light, x0=0.02, x1=0.4, color=GOLD, width=12)
        self.play(ShowPassingFlash(steep, time_width=0.9), run_time=2.5)
        self.at("A level stretch")
        flat = P.curve(rate_from_light, x0=0.65, x1=1.0, color=GOLD, width=12)
        self.play(ShowPassingFlash(flat, time_width=0.9), run_time=2.1)
        self.at("Then test another")
        locks_a = VGroup(lock_mark([2.1, 3.12, 0]), lock_mark([5.35, 3.12, 0]))
        self.play(FadeIn(locks_a), co2.animate.set_value(0.8), rate.animate.set_value(0.9), run_time=3.1)
        self.at("That is how")
        locks_b = VGroup(lock_mark([2.1, 3.12, 0]), lock_mark([3.75, 3.12, 0]))
        self.play(ReplacementTransform(locks_a, locks_b), rate.animate.set_value(0.55),
                  temp.animate.set_value(0.7), run_time=2.5)
        self.at("When more light")
        final = caption("When more light stops helping, something else holds the rate back.", color=TEXT)
        self.play(FadeIn(final), rate.animate.set_value(0.72), run_time=1.4)
        self.finish()


class S11End(EndCard):
    LINE = "When more light stops helping, something else is holding the rate back."
