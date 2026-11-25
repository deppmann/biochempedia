"""Measuring Pull and Push in Plants, timed to the supplied Kokoro audio.

BLUE: xylem water and glass instruments. ORANGE: phloem sap and sieve tubes.
GREY: tissue structure, steel and apparatus. TEAL: bath water.
YELLOW: tracer and the active measurement. GREEN: controls and supported results.
RED: cutting artifacts and the pressure objection. GOLD: dates and predict cues.
"""

from bp_parts import *
from bp_style import EndCard


ORANGE = "#F29E4C"
LEAF = "#52765D"
TISSUE = "#466251"
XYLEM = "#246280"
PHLOEM = "#86502A"
STEEL = "#46576A"
LUMEN = "#13283A"

PLANT_X = -2.0
X_WATER = PLANT_X - 0.83
X_SAP = PLANT_X + 0.83
GAUGE_X = 4.52
QUESTION = "Pulls back, stops, or oozes out?"
OPTIONS = ("Pulls back?", "Stops?", "Oozes out?")
CARD = dict(y=-3.12, size=33, chip_size=28, max_w=9)
CHIPS_AT = [2.15, 0.46, 0]


def p(x, y):
    return np.array([x, y, 0.0])


def rect(x, y, w, h, fill, stroke=None, radius=0.0, opacity=1):
    cls = RoundedRectangle if radius else Rectangle
    shape = cls(width=w, height=h, **({"corner_radius": radius} if radius else {}),
                fill_color=fill, fill_opacity=opacity,
                stroke_color=stroke or fill, stroke_width=3 if stroke else 0)
    return shape.move_to(p(x, y))


def line(a, b, color=GREY, width=4):
    return Line(p(*a), p(*b), color=color, stroke_width=width)


def arrow(a, b, color=TEXT, width=5):
    return Arrow(p(*a), p(*b), color=color, stroke_width=width, buff=0,
                 tip_length=0.2, max_tip_length_to_length_ratio=0.45,
                 max_stroke_width_to_length_ratio=12)


def label(text, x, y, color=TEXT, size=32, width=5.6):
    return fit_text(text, max_w=width, size=size, min_size=28, color=color).move_to(p(x, y))


def heading(text, color=TEXT):
    return label(text, 3.08, 2.86, color, 35)


def schematic():
    return scope_tag(size=28, color=TEXT)


def bracket(x, y0, y1, color=TEXT, tick=0.22):
    return VGroup(line((x, y0), (x, y1), color),
                  line((x - tick, y0), (x + tick, y0), color),
                  line((x - tick, y1), (x + tick, y1), color))


def marks_on_path(path, color, n, speed, radius, length=0):
    """Move visible parcels along a schematic route, without implying literal scale."""
    group = VGroup()
    for i in range(n):
        mark = (rect(0, 0, radius * 2, length, color, radius=radius * 0.8)
                if length else Dot(radius=radius, color=color))
        mark.move_to(path(i / n))

        def update(mob, dt, phase=i / n):
            mob.phase = (getattr(mob, "phase", phase) + dt * speed) % 1
            mob.move_to(path(mob.phase))

        mark.add_updater(update)
        group.add(mark)
    return group


def tube_flow(x, y0, y1, width, color, upward=False, count=16):
    """Two independent lanes of moving liquid highlights inside one conduit."""
    group = VGroup()
    for i, lane in enumerate((-0.25, 0.25)):
        start, stop = (y0 + 0.23, y1 - 0.23) if upward else (y1 - 0.23, y0 + 0.23)
        group.add(marks_on_path(
            lambda u, lane=lane, start=start, stop=stop: p(x + width * lane, interpolate(start, stop, u)),
            color, count // 2, (0.20 + i * 0.067), width * 0.166, 0.37,
        ))
    return group


def leaf(base, tip, width=1.1):
    """The same leaf silhouette and branching ribs in the plant and chamber."""
    a, b = p(*base), p(*tip)
    axis = b - a
    across = np.array([-axis[1], axis[0], 0]) / np.linalg.norm(axis)
    outline = VMobject(stroke_color=GREEN, stroke_width=3, fill_color=LEAF, fill_opacity=1)
    outline.set_points(np.array([
        a, a + 0.22 * axis + width * across, a + 0.74 * axis + width * across, b,
        b, a + 0.70 * axis - width * across, a + 0.20 * axis - width * across, a,
    ]))
    vein = Line(a, b, stroke_color=GREEN, stroke_width=3)
    ribs = VGroup(*[
        Line(a + axis * f, a + axis * (f + 0.18) + across * side * width * 0.43,
             stroke_color=GREEN, stroke_width=2, stroke_opacity=0.65)
        for f in (0.23, 0.43, 0.60) for side in (-1, 1)
    ])
    return VGroup(outline, vein, ribs)


def sieve(x, y0, y1, width, plates):
    shell = rect(x, (y0 + y1) / 2, width, y1 - y0, PHLOEM, ORANGE, radius=0.23)
    bars = VGroup()
    for y in plates:
        for i in range(5):
            bars.add(line((x + width * (-0.46 + i * 0.19), y),
                          (x + width * (-0.33 + i * 0.19), y), ORANGE, 7))
    return shell, bars


def plant(moving=True, water=True, sap=True):
    body = rect(PLANT_X, -0.71, 3.73, 4.76, TISSUE, LEAF, radius=0.52)
    leaves = VGroup(leaf((PLANT_X, 1.42), (-5.9, 2.7), 1.34),
                    leaf((PLANT_X, 1.44), (0.34, 3.05), 0.98))
    xylem = rect(X_WATER, -0.70, 1.40, 4.55, XYLEM, BLUE, radius=0.25)
    phloem, plates = sieve(X_SAP, -2.98, 1.58, 1.40, (0.49, -0.64, -1.77))
    flow = VGroup()
    if moving and water:
        flow.add(tube_flow(X_WATER, -2.97, 1.56, 1.4, BLUE, upward=True))
    if moving and sap:
        flow.add(tube_flow(X_SAP, -2.97, 1.56, 1.4, ORANGE))
    return VGroup(leaves, body, xylem, phloem, flow, plates)


def pressure_scale(water=None, sap=None):
    """Signed schematic scale. Zero means ambient pressure."""
    x = GAUGE_X
    face = rect(x, 0, 0.52, 4.48, STEEL, GREY, radius=0.24)
    mid = line((x - 0.45, 0), (x + 0.45, 0), TEXT, 3)
    ticks = VGroup(*[label(s, x + 0.77, y, TEXT, 30)
                     for s, y in (("+", 1.94), ("0", 0), ("−", -1.94))])
    markers = VGroup()
    for tracker, color in ((water, BLUE), (sap, ORANGE)):
        if tracker is not None:
            m = rect(x, 0, 0.51, 0.23, color, radius=0.1)
            m.add_updater(lambda m, tracker=tracker: m.move_to(p(x, 1.9 * tracker.get_value())))
            m.update(0)
            markers.add(m)
    return VGroup(face, mid, ticks, markers)


class S01Hook(SpokenScene):
    def construct(self):
        water, sap = ValueTracker(-0.04), ValueTracker(0.04)
        self.add(plant(moving=False), pressure_scale(water, sap), schematic())
        q = bob(label("?", 1.95, 0.2, GOLD, 91), amp=0.12, speed=2.4)
        self.at("How do you")
        self.play(FadeIn(q), run_time=0.4)

        mist = marks_on_path(lambda u: p(-4.43 - 1.52 * u, 2.76 + 0.77 * u),
                             BLUE, 11, 0.44, 0.087)
        water_flow = tube_flow(X_WATER, -2.79, 1.43, 1.4, BLUE, upward=True)
        water_name = label("Xylem", 1.97, -0.97, BLUE, 39)
        pull = label("Tension < 0", 1.97, -1.62, BLUE)
        self.at("Evaporation")
        self.remove(q)
        self.add(mist, water_flow)
        self.play(water.animate.set_value(-0.75), run_time=1.8)
        self.at("xylem pipes")
        self.play(FadeIn(water_name), run_time=0.4)
        self.at("below zero")
        self.play(FadeIn(pull), run_time=0.4)

        sap_flow = tube_flow(X_SAP, -2.78, 1.41, 1.4, ORANGE)
        sap_name = label("Phloem", 1.97, 1.21, ORANGE, 39)
        push = label("Pressure > 0", 1.97, 0.62, ORANGE)
        self.at("Living flow")
        self.add(sap_flow)
        self.play(sap.animate.set_value(0.75), FadeIn(sap_name), run_time=1.45)
        self.at("positive pressure")
        self.play(FadeIn(push), run_time=0.4)
        self.finish()


class S02Title(TitleCard):
    LESSON = "Measuring plant water potential and phloem flow"
    TITLE = "Measuring Pull and Push in Plants"

    def construct(self):
        background = plant(moving=False).set_opacity(0.09)
        drift = VGroup(tube_flow(X_WATER, -2.95, 1.56, 1.4, BLUE, upward=True),
                       tube_flow(X_SAP, -2.95, 1.56, 1.4, ORANGE)).set_opacity(0.09)
        title = T(self.TITLE, size=54, font=TITLE_FONT)
        rule = line((-1.1, -0.48), (1.1, -0.48), GOLD, 4)
        self.add(background, drift, title, rule)
        self.wait(self.narration_s)


def cut_leaf():
    lamina = leaf((-3.43, -0.13), (-5.16, -1.79), 1.30)
    stalk = rect(-3.37, 0.96, 0.65, 2.4, LEAF, GREEN, radius=0.13)
    cap = line((-3.68, 2.17), (-3.06, 2.17), TEXT, 4)
    return VGroup(lamina, stalk, cap)


def chamber():
    shell = rect(-3.33, -0.73, 5.54, 4.16, STEEL, GREY, radius=0.44)
    inner = rect(-3.33, -0.74, 5.06, 3.72, LUMEN, None, radius=0.35)
    cap = rect(-3.33, 1.49, 4.92, 0.50, STEEL, GREY, radius=0.19)
    seal = rect(-3.37, 1.52, 1.19, 0.42, GREY, TEXT, radius=0.14)
    feet = VGroup(rect(-4.93, -2.96, 0.69, 0.29, STEEL, radius=0.1),
                  rect(-1.74, -2.96, 0.69, 0.29, STEEL, radius=0.1))
    return VGroup(shell, inner, cap, seal, feet)


def gas_gauge(value):
    return dial(value, p(1.31, -0.14), radius=1.08, label="Gas pressure",
                color=BLUE, fmt="", size=30)


class S03PressureChamber(SpokenScene):
    def construct(self):
        negative = ValueTracker(0)
        gas = ValueTracker(0)
        self.add(schematic(), pressure_scale(negative))
        world = plant()
        self.add(world)
        sprig = cut_leaf()
        self.at("Start with xylem")
        cut = Polygon(p(-3.59, 1.88), p(-3.94, 1.68), p(-3.70, 2.35),
                      fill_color=GREY, fill_opacity=1, stroke_color=TEXT, stroke_width=2)
        self.play(FadeIn(cut, shift=UP * 0.37), run_time=0.4)
        self.play(cut.animate.shift(RIGHT * 0.31 + DOWN * 0.28), run_time=0.4)
        self.play(FadeOut(world), FadeIn(sprig, shift=DOWN * 0.35),
                  FadeOut(cut), negative.animate.set_value(-0.75), run_time=1.29)
        stalk_sap = always_redraw(lambda: line((-3.37, -0.10),
                                                (-3.37, 1.75 + 0.41 * gas.get_value() / 0.78), BLUE, 10))
        self.add(stalk_sap)
        vessel = chamber()
        tool = heading("Scholander\npressure chamber", TEXT)
        self.at("Seal a cut leaf")
        self.add(vessel[0:2], vessel[4])
        self.bring_to_front(sprig, stalk_sap)
        self.play(FadeIn(vessel[2:4], shift=UP * 0.25), run_time=0.75)
        self.at("pressure chamber")
        self.play(FadeIn(tool), FadeIn(gas_gauge(gas)), run_time=0.55)

        swirl = marks_on_path(lambda u: p(-3.33 + 1.96 * np.cos(TAU * u),
                                          -0.75 + 1.43 * np.sin(TAU * u)),
                              GREY, 28, 0.325, 0.095)
        bead = Dot(p(-3.37, 2.29), radius=0.15, color=BLUE)
        self.at("Raise gas pressure")
        self.add(swirl)
        self.play(gas.animate.set_value(0.78), run_time=2.55, rate_func=linear)
        self.play(GrowFromCenter(bead), run_time=0.42)
        bob(bead, amp=0.034, speed=2.5)

        mirror = arrow((2.67, -1.41), (4.15, -1.41), BLUE)
        self.at("pressure balances")
        self.play(GrowArrow(mirror), run_time=0.55)
        self.at("water potential")
        self.play(FadeOut(tool), run_time=0.35)
        quantity = label("Shoot water potential", 2.81, 3.08, BLUE, 35)
        definition = label("Relative to pure water", 2.56, 2.55, TEXT, 29, 4.9)
        self.play(FadeIn(quantity), FadeIn(definition), run_time=0.55)
        self.at("roughly minus")
        self.play(swap(definition, label("≈ − balancing pressure", 2.56, 2.55, TEXT, 31, 4.7)), run_time=0.62)
        self.finish()


SIEVE_X = -2.87
STYLET_Y = 0.95
STYLET_TIP = -0.23


def close_phloem(moving=False):
    body = rect(-3, -0.10, 5.17, 5.02, TISSUE, LEAF, radius=0.43)
    shell, plates = sieve(SIEVE_X, -2.54, 2.34, 3.22, (1.6, 0.26, -1.10))
    flow = tube_flow(SIEVE_X, -2.52, 2.30, 3.22, ORANGE)
    if not moving:
        flow.clear_updaters()
    return VGroup(body, shell, flow, plates)


def stylet():
    return VGroup(line((-2.38, STYLET_Y + 0.09), (STYLET_TIP, STYLET_Y + 0.09), GREY, 5),
                  line((-2.38, STYLET_Y - 0.09), (STYLET_TIP, STYLET_Y - 0.09), GREY, 5),
                  line((-2.36, STYLET_Y), (STYLET_TIP - 0.16, STYLET_Y), PHLOEM, 3))


def aphid():
    x, y = 0.58, STYLET_Y
    abdomen = Ellipse(width=1.23, height=0.77, fill_color=LEAF, fill_opacity=1,
                      stroke_color=GREEN, stroke_width=3).rotate(-0.26).move_to(p(x + 0.44, y + 0.34))
    head = Circle(radius=0.24, stroke_color=GREEN, stroke_width=3,
                  fill_color=LEAF, fill_opacity=1).move_to(p(x - 0.44, y + 0.12))
    legs = VGroup(*[VMobject(stroke_color=GREEN, stroke_width=3).set_points_as_corners(
        [p(x + f, y + 0.12), p(x + f + 0.07, y - 0.26), p(x + f - 0.24, y - 0.42)])
        for f in (-0.28, 0.14, 0.53)])
    antennae = VGroup(line((x - 0.57, y + 0.25), (x - 0.94, y + 0.62), GREEN, 3),
                      line((x - 0.54, y + 0.29), (x - 0.66, y + 0.75), GREEN, 3))
    return VGroup(legs, antennae, abdomen, head)


def scissors():
    handles = VGroup(*[Circle(radius=0.15, stroke_color=GREY, stroke_width=4).move_to(p(0.52, y))
                       for y in (STYLET_Y + 0.65, STYLET_Y + 1.11)])
    blades = VGroup(line((0.40, STYLET_Y + 1.03), (-0.24, STYLET_Y), GREY, 5),
                    line((0.40, STYLET_Y + 0.73), (-0.53, STYLET_Y + 0.32), GREY, 5))
    return VGroup(blades, handles)


def choices():
    return VGroup(arrow((0.62, 1.27), (0.08, 1.27), GREY),
                  line((0.30, 0.37), (0.62, 0.37), GREY),
                  arrow((0.05, -0.50), (0.63, -0.50), GREY))


def prediction():
    return question_card(QUESTION, OPTIONS, chips_at=CHIPS_AT, **CARD)


class S04PredictQ(SpokenScene):
    def construct(self):
        overview = plant()
        world = close_phloem(moving=True)
        self.add(overview, schematic())
        self.at("Now flow")
        self.play(FadeOut(overview), FadeIn(world), run_time=1)
        title = heading("Living sieve tube", ORANGE)
        self.at("its sieve tubes")
        self.play(FadeIn(title), run_time=0.4)

        bug = aphid()
        needle = stylet()
        self.at("An aphid pushes")
        self.play(FadeIn(bug, shift=LEFT * 0.72 + DOWN * 0.55), run_time=0.85)
        self.play(FadeIn(needle, shift=LEFT * 1.83), run_time=1.28)
        self.at("into one sieve")
        name = label("Stylet", 0.66, 0.10, TEXT)
        leader = line((STYLET_TIP, STYLET_Y - 0.14), (0.16, 0.36), GREY, 3)
        self.play(FadeIn(name), Create(leader), run_time=0.35)

        snip = scissors()
        self.at("Cut the aphid")
        self.play(FadeIn(snip, shift=DOWN * 0.38), run_time=0.45)
        self.play(FadeOut(snip), FadeOut(bug, shift=UP * 0.33), run_time=0.5)
        self.at("only the open")
        self.play(FadeOut(VGroup(name, leader)), FadeOut(title), run_time=0.45)

        q, prompts = prediction(), choices()
        self.at("Does sap pull")
        self.play(FadeIn(q.question), FadeIn(q.chips[0]), Create(prompts[0]), run_time=0.52)
        self.at("stop or keep")
        self.play(FadeIn(q.chips[1]), Create(prompts[1]), run_time=0.25)
        self.at("oozing out")
        self.play(FadeIn(q.chips[2]), Create(prompts[2]), run_time=0.38)
        self.finish()


class S05PredictPause(PredictPause):
    QUESTION = QUESTION
    OPTIONS = OPTIONS
    CHIPS_AT = CHIPS_AT
    CARD = CARD
    SECONDS = 4.5

    def backdrop(self):
        return VGroup(close_phloem(), stylet(), choices(), schematic())

    def construct(self):
        self.add(self.backdrop(), prediction())
        track = line((-1.7, -3.59), (1.7, -3.59), GREY, 4)
        fill = track.copy().set_stroke(GOLD, width=5)
        self.add(track)
        self.play(Create(fill), run_time=self.SECONDS, rate_func=linear)


def ooze():
    return marks_on_path(lambda u: p(STYLET_TIP + 0.56 * np.sin(u * PI / 2),
                                     STYLET_Y - 1.51 * u ** 2),
                         ORANGE, 5, 0.49, 0.11)


def pico_gauge():
    y = -1.56
    points = [(-2.22, y + 0.12), (-0.98, y + 0.34), (2.86, y + 0.34),
              (2.86, y - 0.34), (-0.98, y - 0.34), (-2.22, y - 0.12)]
    glass = Polygon(*[p(*a) for a in points], fill_color=LUMEN, fill_opacity=1,
                    stroke_color=BLUE, stroke_width=4)
    return glass


class S06StyletProbe(SpokenScene):
    def construct(self):
        photo, needle, q, prompts = close_phloem(), stylet(), prediction(), choices()
        self.add(photo, needle, q, prompts, schematic())
        self.at("SAP keeps oozing")
        droplets = ooze()
        plates = photo[3]
        photo.remove(photo[2])
        self.add(droplets, tube_flow(SIEVE_X, -2.52, 2.30, 3.22, ORANGE))
        self.bring_to_front(plates, needle)
        answer = chip("Oozes out", ORANGE, 30).move_to(p(2.39, 0.06))
        self.play(prompts[2].animate.set_color(ORANGE), FadeOut(q.question),
                  FadeOut(q.chips[0]), FadeOut(q.chips[1]), FadeOut(prompts[0]), FadeOut(prompts[1]),
                  run_time=0.43)
        self.play(FadeOut(prompts[2]), swap(q.chips[2], answer), run_time=0.57)

        turgor = ValueTracker(0)
        gu = pressure_scale(sap=turgor)
        self.at("by positive pressure")
        self.add(gu)
        self.play(turgor.animate.set_value(0.59), run_time=1)
        self.at("nearly pure")
        sap_label = label("Nearly pure\nphloem sap", 2.35, 0.44, ORANGE, width=3.75)
        self.play(swap(answer, sap_label), run_time=0.65)
        self.at("measure that pressure")
        self.play(FadeOut(sap_label), FadeIn(heading("Turgor > 0", ORANGE)), run_time=0.45)
        tube = pico_gauge()
        self.at("a glass pico")
        self.play(FadeIn(tube, shift=LEFT * 0.92), run_time=1.02)
        name = label("Pico-gauge", 1.55, -2.27, BLUE)
        self.play(FadeIn(name), run_time=0.45)

        compression = ValueTracker(0.0)
        meniscus = lambda: 0.04 + 1.10 * compression.get_value()
        trapped = always_redraw(lambda: rect((2.18 + meniscus()) / 2, -1.56,
                                             2.18 - meniscus(), 0.42, TEXT, radius=0.13))
        self.at("Its tip holds")
        self.play(FadeIn(trapped), run_time=0.65)
        oil_label = label("Trapped oil", 1.48, -0.83, TEXT)
        self.at("volume of oil")
        self.play(FadeIn(oil_label), run_time=0.45)

        advance = always_redraw(lambda: line((-2.16, -1.56), (meniscus(), -1.56), ORANGE, 11))
        travel = always_redraw(lambda: VGroup(
            line((0.04, -2.75), (meniscus(), -2.75), YELLOW),
            line((0.04, -2.88), (0.04, -2.62), YELLOW, 3),
            line((meniscus(), -2.88), (meniscus(), -2.62), YELLOW, 3)))
        self.at("SAP squeezes")
        self.add(advance)
        self.play(compression.animate.set_value(0.92), turgor.animate.set_value(0.84), run_time=1.4)
        self.add(travel)
        self.finish()


def detector(y):
    center = p(X_SAP, y)
    return VGroup(*[
        Arc(radius=0.91, start_angle=a, angle=PI, stroke_color=color,
            stroke_width=8, arc_center=center).stretch(0.23, 1, about_point=center)
        for a, color in ((PI, STEEL), (0, GREY))
    ])


def timer(progress):
    t = VGroup(rect(3.71, 1.54, 2.24, 0.87, LUMEN, GREY, radius=0.16),
               label("Travel time", 3.71, 1.56, TEXT, 28))
    tracks = VGroup(*[rect(2.88 + i * 0.235, 0.77, 0.16, 0.32, STEEL, radius=0.07)
                      for i in range(8)])
    for i, bar in enumerate(tracks):
        bar.add_updater(lambda b, i=i: b.set_fill(YELLOW if progress.get_value() * 8 > i else STEEL))
    return VGroup(t, tracks)


class S07TracerIdea(SpokenScene):
    def construct(self):
        world = plant()
        close = VGroup(close_phloem(), stylet(), pico_gauge(), pressure_scale(sap=ValueTracker(0.84)))
        self.add(close, schematic())
        self.at("Pressure alone")
        self.play(FadeOut(close), FadeIn(world), run_time=1.30)

        incoming = marks_on_path(lambda u: p(-6.4 + 3.2 * u, 3.43 - 1.33 * u),
                                 YELLOW, 14, 0.48, 0.09)
        source = heading("Carbon-11", YELLOW)
        self.at("Feed a leaf")
        self.add(incoming)
        self.at("radioactive carbon")
        self.play(FadeIn(source), run_time=0.48)

        front_y = ValueTracker(1.46)
        front = VGroup(*[Dot(p(X_SAP + dx, dy), radius=r, color=YELLOW)
                         for dx, dy, r in ((0, 0, 0.17), (-0.32, 0.16, 0.11), (0.28, 0.24, 0.14),
                                           (-0.06, 0.36, 0.10), (0.44, 0.46, 0.09), (-0.42, 0.46, 0.08))])
        front.add_updater(lambda f: f.set_y(front_y.get_value() + 0.18))
        self.at("makes labeled sugar")
        self.remove(incoming)
        self.add(front)
        sugar_label = heading("Labelled sugar", YELLOW)
        self.play(swap(source, sugar_label), front_y.animate.set_value(0.80), run_time=1.65)

        d1, d2 = detector(0.45), detector(-1.72)
        elapsed = ValueTracker(0.0)
        watch = timer(elapsed)
        self.at("Detectors along")
        self.play(FadeIn(d1), FadeIn(d2), FadeIn(watch), front_y.animate.set_value(0.45), run_time=0.60)
        d1.set_stroke(YELLOW)
        self.play(front_y.animate.set_value(-1.72),
                  elapsed.animate.set_value(1), run_time=2.05, rate_func=linear)
        d2.set_stroke(YELLOW)

        span = bracket(0.14, -1.72, 0.45, YELLOW)
        distance = label("Distance", 1.16, -0.60, YELLOW, 28)
        self.at("Distance between")
        self.play(Create(span), FadeIn(distance), run_time=0.56)
        self.at("divided by travel")
        self.remove(sugar_label)
        key = label("Speed = distance ÷ time", 2.94, -2.76, TEXT, 34, 6.8)
        self.play(FadeIn(key), front_y.animate.set_value(-2.77), run_time=1.15)
        self.at("gives speed")
        trace = marks_on_path(lambda u: p(X_SAP, interpolate(1.34, -2.72, u)),
                              YELLOW, 7, 0.57, 0.098)
        self.add(trace)
        self.finish()


VESSELS = ((-1.14, 0.57), (0.04, 0.82), (1.06, 0.54),
           (-0.64, -0.29), (0.57, -0.27), (-0.03, -0.99))


def scan(x, y, scale=1, air=()):
    """Perspective cutaway of the same vessel positions before and after cutting."""
    extent = 2.09 * scale
    section = VGroup()
    for offset in (0.75, 0.50, 0.25):
        section.add(Ellipse(width=2 * extent, height=1.55 * extent, fill_color=LEAF,
                            fill_opacity=1, stroke_color=TISSUE, stroke_width=4).move_to(
                                p(x, y - offset * scale)))
    face = Ellipse(width=2 * extent, height=1.55 * extent, fill_color=TISSUE, fill_opacity=1,
                   stroke_color=GREEN, stroke_width=3).move_to(p(x, y))
    section.add(face)
    pores = VGroup()
    for i, (dx, dy) in enumerate(VESSELS):
        lumen = TEXT if i in air else XYLEM
        pores.add(Ellipse(width=0.80 * scale, height=0.60 * scale, fill_color=lumen,
                           fill_opacity=1, stroke_color=BLUE, stroke_width=2).move_to(
                               p(x + dx * scale, y + dy * scale)))
    return VGroup(section, pores)


def xray_sweep(x, y, span=2.55, seconds=2.35):
    """The source sweeps different ray angles around the fixed stem section."""
    sweep = ValueTracker(-0.76)

    def beam():
        a = sweep.get_value()
        tip = p(x + span * np.cos(a), y + 0.67 * span * np.sin(a))
        left = p(x - 0.85 * np.sin(a), y + 0.67 * np.cos(a))
        right = p(x + 0.85 * np.sin(a), y - 0.67 * np.cos(a))
        return VGroup(Polygon(tip, left, right, fill_color=YELLOW, fill_opacity=0.51,
                              stroke_color=YELLOW, stroke_width=3),
                      Dot(tip, radius=0.15, color=YELLOW))

    ray = always_redraw(beam)
    return ray, sweep.animate(run_time=seconds, rate_func=linear).set_value(-4.27)


def water_bath():
    return VGroup(rect(-2.99, -0.55, 6.23, 4.72, "#235668", radius=0.38),
                  line((-6.05, 1.83), (0.04, 1.83), TEAL, 4))


def bath_motion():
    currents = VGroup()
    for i, y in enumerate((1.51, -0.02, -1.66)):
        parcels = marks_on_path(lambda u, y=y: p(-5.78 + 5.55 * u, y),
                                TEAL, 7, 0.17 + i * 0.037, 0.068, 0.42)
        for parcel in parcels:
            parcel.rotate(PI / 2)
        currents.add(parcels)
    return currents


def cut_columns():
    world = rect(-3.1, -0.03, 4.24, 5.03, TISSUE, LEAF, radius=0.40)
    channels = VGroup()
    for x in (-4.41, -3.1, -1.79):
        channels.add(rect(x, -0.04, 1.03, 4.79, XYLEM, BLUE, radius=0.29))
    return VGroup(world, channels)


def gap(x, y, h=0.68):
    return rect(x, y, 0.89, h, TEXT, radius=0.24)


class S08Controls(SpokenScene):
    def construct(self):
        bath = water_bath()
        columns = cut_columns()
        motion = bath_motion()
        xylem = VGroup(*(tube_flow(x, -2.32, 2.29, 1.03, BLUE, upward=True, count=12)
                         for x in (-3.1, -1.79)))
        self.add(bath, motion, columns, xylem, schematic())
        original = gap(-4.41, -0.45, 0.84)
        gas = heading("Embolism", BLUE)
        water_label = label("Broken water column", 3.16, 1.94, TEXT)
        self.at("gas bubbles")
        self.play(GrowFromCenter(original), run_time=0.64)
        self.play(FadeIn(gas), FadeIn(water_label), run_time=0.48)

        blade = Polygon(p(-0.25, 0.58), p(-0.25, 0.05), p(-1.22, 0.04),
                        fill_color=GREY, fill_opacity=1, stroke_color=TEXT, stroke_width=2)
        extra = VGroup(gap(-3.1, -0.40), gap(-1.79, -0.76, 0.75))
        self.at("cutting a tense stem")
        self.play(FadeOut(water_label), FadeIn(blade), run_time=0.46)
        self.play(blade.animate.shift(LEFT * 3.62), run_time=1.60)
        self.at("itself create")
        self.remove(xylem)
        self.play(GrowFromCenter(extra), run_time=0.54)

        panels = TwoPanel("Before cutting", "After cutting", colors=(GREY, GREY),
                          top=2.44, bottom=-2.55, size=32)
        before, after = scan(-3.30, -0.03, air=(2,)), scan(3.30, -0.03, air=(2,))
        beam, sweep = xray_sweep(-3.3, -0.03, span=2.37, seconds=4.6)
        self.at("microdemography merges")
        self.play(FadeOut(VGroup(bath, columns, motion, original, gas, blade, extra)), run_time=0.32)
        self.play(FadeIn(panels), FadeIn(before), run_time=0.40)
        imaging = label("X-ray microtomography", 0, 3.03, TEXT, 34, 8.8)
        self.add(beam)
        self.play(FadeIn(imaging), sweep)
        self.play(FadeOut(beam), run_time=0.42)

        air = label("Air-filled", -3.15, -3.0, TEXT, 30)
        wet = label("Water-filled", -0.19, -3.0, BLUE, 30)
        self.at("Air -filled")
        self.play(FadeIn(air), FadeIn(wet), run_time=0.48)
        beam, sweep = xray_sweep(-3.3, -0.03, span=2.37, seconds=2.57)
        self.add(beam)
        self.play(sweep)
        self.remove(beam)
        self.at("before and after")
        self.add(after)
        self.play(LaggedStart(*[after[1][i].animate.set_fill(TEXT) for i in (1, 4)],
                              lag_ratio=0.65), run_time=1.15)
        artifact = label("Cutting artifact", 2.75, -2.99, RED, 30)
        self.play(FadeIn(artifact), run_time=0.38)

        relabel = label("Rehydrate before cutting", 0, 3.03, GREEN, 34, 9.2)
        compare = scan(-2.92, 0.01, scale=1.18, air=(2,))
        relaxed = ValueTracker(-0.80)
        scale = pressure_scale(water=relaxed)
        tension = label("Tension near zero", 2.54, -0.97, GREEN, 30, 3.1)
        control_blade = blade.copy().move_to(p(-0.21, 1.46))
        self.at("Rehydrating first")
        self.play(FadeOut(VGroup(air, wet, artifact, panels, before, after, imaging)), run_time=0.34)
        self.play(FadeIn(compare), FadeIn(scale), FadeIn(relabel), run_time=0.43)
        self.play(relaxed.animate.set_value(-0.08), FadeIn(tension), run_time=0.96)
        self.play(FadeIn(control_blade), run_time=0.25)
        self.play(control_blade.animate.shift(LEFT * 4.20), run_time=0.85)
        self.play(FadeOut(control_blade), run_time=0.28)
        self.finish()


def root(origin, scale=1):
    x, y = origin
    branches = VGroup(*[CubicBezier(p(x + 0.06 * q, y), p(x + q * 0.23, y - 0.60 * scale),
                                         p(x + q * 0.28, y - 0.76 * scale),
                                         p(x + q * 0.48, y - (1.03 - 0.235 * abs(q)) * scale),
                                         stroke_color=LEAF, stroke_width=7)
                        for q in (-2, -1, 0, 1, 2)])
    return branches


def root_detail():
    shell, plates = sieve(-4.64, -2.55, 2.62, 1.24, (1.6, 0.38, -0.84, -2.02))
    sleeve = rect(-3.59, 0.03, 4.57, 5.39, TISSUE, LEAF, radius=0.49)
    cells = VGroup(*[rect(-2.67, y, 1.90, 1.40, LEAF, GREEN, radius=0.41)
                     for y in (-1.60, 0, 1.60)])
    return VGroup(sleeve, root((-3.60, -2.57)), shell, cells, plates)


def tree_silhouette():
    crown = VGroup(*[Circle(radius=r, color=LEAF, stroke_width=0, fill_opacity=1).move_to(p(x, y))
                     for x, y, r in ((2.87, -0.39, 0.62), (3.64, -0.30, 0.64),
                                     (3.30, 0.17, 0.64))])
    return VGroup(rect(3.29, -1.04, 0.27, 1.18, TISSUE), crown).set_opacity(0.65)


class S09Limits(SpokenScene):
    def construct(self):
        self.add(schematic())
        world = plant()
        close = root_detail()
        self.add(world)
        self.at("measurements have limits")
        self.play(FadeOut(world), FadeIn(close), run_time=0.84)
        flow = tube_flow(-4.64, -2.48, 2.57, 1.24, ORANGE)
        self.add(flow)
        glass = Polygon(p(-4.55, 0.05), p(-3.35, 0.23), p(0.43, 0.23), p(0.43, -0.20),
                        p(-3.35, -0.20), fill_color=LUMEN, fill_opacity=1,
                        stroke_color=BLUE, stroke_width=4)
        self.at("pressure at the root")
        self.play(FadeIn(glass, shift=LEFT * 1.25), run_time=0.77)
        self.at("came from root")
        self.play(glass.animate.shift(RIGHT * 1.95), run_time=0.73)
        proxy = heading("Root cortex proxy", GREEN)
        self.play(FadeIn(proxy), run_time=0.45)

        band = DashedLine(p(3.75, -0.18), p(3.75, 0.93), dash_length=0.11,
                          stroke_color=YELLOW, stroke_width=9)
        gauge = pressure_scale(sap=ValueTracker(0.84))
        drop = bracket(3.18, -0.27, 1.58, ORANGE)
        text = label("True drop may be smaller", 2.55, -2.67, YELLOW, 30)
        self.at("real pressure drop")
        self.play(FadeIn(gauge), Create(drop), run_time=0.58)
        self.play(Create(band), run_time=0.97)
        self.play(FadeIn(text), run_time=0.42)

        notebook = Ledger([("Morning glory", "", GREEN), ("Oak", "", GREY)],
                          top_left=(2.42, 1.89), width=3.8, key_w=3.1, row_h=0.69)
        self.at("hold for one species")
        self.play(FadeOut(VGroup(proxy, gauge, drop, band, text, glass)), run_time=0.35)
        self.play(notebook.reveal(0), notebook.reveal(1), run_time=0.53)
        self.at("were removed")
        self.play(FadeOut(notebook.rows[1], shift=RIGHT * 0.5), FadeIn(tree_silhouette()), run_time=0.72)
        self.play(FadeIn(label("Untested", 3.29, -2.04, TEXT, 30)), run_time=0.40)
        self.finish()


class S10UnlockedXylem(SpokenScene):
    def construct(self):
        before = scan(-2.82, 0.15, scale=1.37, air=(2,))
        self.add(before, schematic())
        scan_label = label("Intact stem", 3.26, -0.89, BLUE, 32)
        self.at("These tools")
        self.play(FadeIn(scan_label), run_time=0.5)
        ray, sweep = xray_sweep(-2.82, 0.15, span=3.26, seconds=2.45)
        self.add(ray)
        self.play(sweep)
        self.remove(ray)
        paper = heading("Torres-Ruiz and\ncolleagues, 2015", GOLD)
        self.at("In 2015")
        ray, sweep = xray_sweep(-2.82, 0.15, span=3.26, seconds=3.26)
        self.add(ray)
        self.play(FadeIn(paper), sweep)
        self.remove(ray)

        blade = Polygon(p(-0.37, 2.01), p(-0.34, 1.48), p(-1.08, 1.30),
                        fill_color=GREY, fill_opacity=1, stroke_color=TEXT, stroke_width=2)
        bath = rect(-2.83, -0.61, 6.57, 4.56, "#235668", radius=0.44)
        surface = line((-6.05, 1.54), (0.39, 1.54), TEAL, 4)
        self.at("cutting underwater")
        moving = bath_motion()
        moving.shift(DOWN * 0.11)
        self.add(bath, surface, moving)
        self.bring_to_front(before)
        self.play(FadeIn(blade), run_time=0.46)
        self.play(blade.animate.shift(LEFT * 4.65 + DOWN * 0.30), run_time=2.10)
        self.at("itself created")
        self.remove(blade)
        after_label = label("After the\nunderwater cut", 3.18, -0.89, BLUE)
        self.play(LaggedStart(*[before[1][i].animate.set_fill(TEXT) for i in (1, 4, 5)],
                              lag_ratio=0.5),
                  swap(scan_label, after_label), run_time=1.30)

        species = VGroup(*[scan(x, 0.26, scale=0.61, air=tuple(range(n)))
                           for x, n in zip((-4.88, -1.68, 1.68, 4.88), (1, 3, 2, 4))])
        species_title = label("Four species", 0, 2.13, TEXT, 37)
        self.at("in four species")
        # The groups enter sequentially so the four independent responses can be compared.
        self.play(FadeOut(VGroup(before, bath, surface, moving, paper, after_label)), run_time=0.32)
        self.add(species_title)
        self.play(LaggedStart(*(FadeIn(item, shift=UP * 0.26) for item in species),
                              lag_ratio=0.46), run_time=1.09)
        variance = label("Varies by species and tension", 0, -1.68, GOLD, 33, 8.9)
        self.at("varying with")
        self.play(FadeIn(variance), run_time=0.42)

        tally = Ledger([("Cut-stem count", "Can overstate damage", RED),
                        ("Intact-stem count", "Before cutting", BLUE)],
                       top_left=(-5.65, -1.52), width=11.4, key_w=4.9, row_h=0.70, size=30)
        self.at("So counts from")
        self.play(FadeOut(variance), run_time=0.33)
        self.play(tally.reveal(1), run_time=0.52)
        self.play(tally.reveal(0), run_time=0.65)
        self.play(tally.mark(0, RED), run_time=0.64)
        self.finish()


def vine_x(y):
    return -2.62 + 0.92 * np.sin((y + 0.40) * 0.95)


def source_leaf():
    anchor = p(vine_x(1.61), 1.61)
    blade = leaf((anchor[0], anchor[1]), (-5.80, 2.76), 1.35)
    blade.phase = 0
    blade.angle = 0

    def sway(mob, dt):
        mob.phase += dt
        angle = 0.10 * np.sin(mob.phase * 2.5)
        mob.rotate(angle - mob.angle, about_point=anchor)
        mob.angle = angle

    return blade.add_updater(sway)


def vine(length, width, moving=True):
    top = 1.63

    def axis():
        y0, y1 = top - length.get_value(), top
        path = np.linspace(y0, y1, 60)
        pts = [p(vine_x(y), y) for y in path]
        tissue = VMobject(stroke_color=LEAF, stroke_width=width.get_value() + 36)
        tube = VMobject(stroke_color=PHLOEM, stroke_width=width.get_value() + 9)
        lumen = VMobject(stroke_color=ORANGE, stroke_width=max(3, width.get_value() - 4))
        for current in (tissue, tube, lumen):
            current.set_points_smoothly(pts)
        return VGroup(tissue, tube, lumen)

    def route(u):
        y = interpolate(top - 0.08, top + 0.08 - length.get_value(), u)
        return p(vine_x(y), y)

    tip = always_redraw(lambda: root((vine_x(top - length.get_value()),
                                     top - length.get_value()), 0.58))
    parcels = marks_on_path(route, YELLOW, 14, 0.36, 0.075) if moving else VGroup()
    return VGroup(always_redraw(axis), tip, source_leaf(), parcels)


class S11UnlockedMunch(SpokenScene):
    def construct(self):
        stretch, width = ValueTracker(2.88), ValueTracker(17)
        world = vine(stretch, width, moving=False)
        self.add(world, schematic())
        authors = label("Knoblauch, Holbrook\nand colleagues, 2016", 3.03, 2.81, GOLD, 32)
        idea = label("Münch’s idea · 1930", 3.03, 1.95, TEXT, 32)
        species_label = label("Morning glory", 3.03, 1.10, GREEN, 34)
        self.at("In 2016")
        self.play(FadeIn(authors), stretch.animate.set_value(3.20), run_time=2.5)
        self.at("Munch's 1930")
        self.play(FadeIn(idea), run_time=0.57)
        self.at("morning glory")
        self.play(FadeIn(species_label), run_time=0.50)

        pressure = ValueTracker(0.10)
        instrument = pressure_scale(sap=pressure)
        loader = marks_on_path(lambda u: p(-5.58 + 3.65 * u, 2.65 - 1.03 * u),
                               ORANGE, 15, 0.43, 0.11)
        self.at("sugar loaded")
        self.play(FadeOut(VGroup(authors, idea, species_label)), run_time=0.40)
        self.add(loader, instrument)
        source = heading("Source leaf", ORANGE)
        self.play(FadeIn(source), run_time=0.46)
        self.at("raises pressure")
        self.play(pressure.animate.set_value(0.62), run_time=0.72)
        direction = arrow((-4.49, 0.80), (-4.49, -1.27), ORANGE, 7)
        flow = vine(stretch, width)[3]
        self.at("pushing sap toward")
        self.add(flow)
        self.play(GrowArrow(direction), run_time=0.75)
        root_label = label("Toward the root", -4.55, -2.80, ORANGE, 29)
        self.play(FadeIn(root_label), run_time=0.42)

        doubt = heading("Enough pressure?", RED)
        self.at("Critics argued")
        self.remove(loader)
        self.remove(root_label)
        self.play(swap(source, doubt), FadeOut(direction),
                  width.animate.set_value(7), stretch.animate.set_value(3.75), run_time=1.18)
        self.at("need more pressure")
        self.play(pressure.animate.set_value(0.96), run_time=1.20)
        self.at("team lengthened vines")
        self.play(FadeOut(doubt), FadeOut(instrument), stretch.animate.set_value(4.54),
                  run_time=1.28)
        self.finish()


def turgor_bar(value):
    """Pressure fill and number share a tracker, in MPa."""
    x = 3.0
    floor = -2.28
    limit = 2.4
    scale = 4.12 / limit
    case = rect(x, floor + 2.06, 0.89, 4.23, LUMEN, GREY, radius=0.17)
    fill = always_redraw(lambda: rect(x, floor + scale * value.get_value() / 2,
                                       0.66, scale * value.get_value(), ORANGE, radius=0.10))
    ticks = VGroup(*[
        VGroup(line((3.45, y), (3.63, y), GREY, 3), label(text, 4.70, y, TEXT, 28))
        for y, text in ((floor, "0"), (floor + scale * 0.75, "≈0.75 MPa"),
                        (floor + scale * 2.24, ">2.2 MPa"))
    ])
    return VGroup(case, fill, ticks[0]), ticks[1], ticks[2]


class S12UnlockedVines(SpokenScene):
    def construct(self):
        stretch, width = ValueTracker(4.54), ValueTracker(7)
        value = ValueTracker(0.75)
        self.add(vine(stretch, width), schematic())
        bar, start, high = turgor_bar(value)
        name = heading("Source turgor", ORANGE)
        conversion = label("1 MPa ≈ 10 atmospheres", 2.58, -2.90, TEXT, 29, 5.8)
        self.at("Source turgor")
        self.play(FadeIn(bar), FadeIn(name), run_time=0.68)
        self.at("from about")
        self.play(FadeIn(start), run_time=0.58)
        self.at("more than")
        self.play(value.animate.set_value(2.24), stretch.animate.set_value(4.63), FadeIn(high),
                  FadeIn(conversion), run_time=1.47)

        conduct = label("5–6× the\nconductivity", 0.35, 0.20, ORANGE, 32, 3.6)
        self.at("also conducted")
        self.play(width.animate.set_value(36), FadeIn(conduct), run_time=2.01)
        reach = bracket(-6.05, 1.63 - 4.63, 1.63, GREEN, tick=0.18)
        takeaway = label("Estimated reach\nmatched vine length", 0.58, 0.02, GREEN, 32, 3.76)
        self.at("pressure flow's estimated")
        self.play(FadeOut(conduct), FadeOut(start), Create(reach), run_time=0.88)
        self.at("matched the vine's")
        self.play(FadeIn(takeaway), run_time=0.58)
        self.finish()


class S13End(EndCard):
    LINE = "Gas balances xylem tension; probes and stylets tap positive phloem pressure."
