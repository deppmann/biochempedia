"""Activity-dependent tagging, timed to the supplied Kokoro alignment.

Color map
  Slate / grey   quiet tissue and structural links
  Yellow         neural activity and the incoming signal
  Blue           lasting genetic tags
  Purple         a second memory and reorganized links
  Green / red    activating / silencing and their contrasting outcomes
  Gold           evidence ladder and the prediction
"""
from bp_parts import *

SLATE = "#556F8D"
TISSUE = "#26364C"
LINK = "#49617B"
PURPLE = "#B58CD9"
QUESTION = "Recall failed. Was the memory erased?"
CARD = {"y": 3.29, "size": 36}
ACTIVE = (1, 5, 8, 11, 14)
SHARED = (3, 8, 10, 14, 17)
ACTIVE_EDGES = ((1, 5), (5, 8), (8, 11), (8, 14))
POINTS = np.array([
    [-2.55, 1.78, 0], [-1.0, 2.03, 0], [0.78, 2.08, 0], [2.27, 1.86, 0],
    [-2.98, 0.62, 0], [-1.73, 0.85, 0], [-0.32, 0.95, 0], [2.55, 0.64, 0],
    [1.02, 0.71, 0], [-2.25, -0.56, 0], [-0.89, -0.40, 0], [2.67, -0.63, 0],
    [-2.72, -1.81, 0], [-1.46, -1.94, 0], [0.64, -0.61, 0], [2.29, -1.95, 0],
    [0.06, -2.04, 0], [1.19, -1.87, 0],
])
RARE_CELL = 56
GUT_CENTER = np.array([-0.68, -1.15, 0])
BRAIN_SHIFT = np.array([-0.68, 1.30, 0])


def point(x, y):
    return np.array([x, y, 0.0])


def soft_outline(vertices, color, stroke, fill, opacity=1):
    return VMobject().set_points_smoothly([*vertices, vertices[0]]).set_stroke(
        color, stroke
    ).set_fill(fill, opacity)


def neural_body(p, seed, scale=1):
    angles = np.linspace(0, TAU, 8, endpoint=False) + 0.24 * seed
    radii = (0.36 + 0.08 * np.sin(angles * 3 + seed)) * scale
    rim = [p + r * point(np.cos(a), np.sin(a)) for a, r in zip(angles, radii)]
    soma = soft_outline(rim, GREY, 1.7, SLATE)
    core = Dot(p + point(0.035, 0.02) * scale, radius=0.125 * scale, color=LINK)
    return VGroup(soma, core)


def branches(a, b, seed, color=LINK, width=3, opacity=0.85):
    d = b - a
    normal = normalize(np.cross(OUT, d))
    bend = normal * (0.12 if seed % 2 else -0.15)
    path = CubicBezier(a, a + 0.36 * d + bend, a + 0.66 * d - bend, b)
    return path.set_stroke(color, width, opacity=opacity)


def tissue_light(surface, strength=1):
    """Drifting light across the tissue, independent of yellow firing and blue tags."""
    clock = 0.0
    dark = ManimColor(TISSUE)
    light = ManimColor("#3C5572")

    def illuminate(mob, dt):
        nonlocal clock
        clock += dt
        phase = 0.5 - 0.5 * np.cos(TAU * clock / 4.25)
        mob.set_fill(interpolate_color(dark, light, strength * phase), 1)

    surface.add_updater(illuminate)


class NeuralField(VGroup):
    """Fixed cell centers and wiring, with separate layers for firing and identity."""

    def __init__(self, points=POINTS, scale=1, activity=0, tagged=False, quiet=False,
                 strengthened=False):
        self.coords = points
        self.cell_scale = scale
        x, y = np.mean(points, axis=0)[:2]
        w, h = np.ptp(points, axis=0)[:2] / 2 + 0.62 * scale
        boundary = [
            point(x - w, y + 0.12 * h), point(x - 0.78 * w, y + 0.79 * h),
            point(x - 0.24 * w, y + h), point(x + 0.43 * w, y + 0.96 * h),
            point(x + 0.88 * w, y + 0.69 * h), point(x + w, y - 0.08 * h),
            point(x + 0.82 * w, y - 0.73 * h), point(x + 0.24 * w, y - h),
            point(x - 0.46 * w, y - 0.92 * h), point(x - 0.86 * w, y - 0.65 * h),
        ]
        self.tissue = soft_outline(boundary, LINK, 2, TISSUE)
        edges = [
            (0, 1), (0, 4), (0, 5), (1, 2), (2, 6), (2, 8), (2, 3), (3, 7),
            (4, 5), (4, 9), (5, 6), (5, 9), (5, 10), (6, 8), (7, 8), (7, 11),
            (9, 10), (9, 12), (9, 13), (10, 14), (10, 13), (10, 16), (11, 15),
            (12, 13), (13, 16), (14, 16), (14, 17), (15, 17), (16, 17),
        ]
        self.wiring = VGroup(*[branches(points[i], points[j], i + j) for i, j in edges])
        for i, p in enumerate(points):
            for direction in (0.48, 2.6, 4.85):
                a = direction + 0.31 * i
                v = point(np.cos(a), np.sin(a)) * scale
                self.wiring.add(branches(p, p + 0.61 * v, i, width=2.6))
        self.paths = VGroup(*[
            branches(points[i], points[j], i + j, YELLOW if activity else SLATE,
                     4.8 if strengthened or activity else 3, opacity=1)
            for i, j in ACTIVE_EDGES
        ])
        self.cells = VGroup(*[neural_body(p, i, scale) for i, p in enumerate(points)])
        if activity:
            for cell in (self.cells[i] for i in ACTIVE):
                cell[0].set_fill(YELLOW, 0.9).set_stroke(YELLOW, 2.5)
                cell[1].set_color(GOLD)
        self.tags = VGroup(*[
            Circle(radius=0.51 * scale, stroke_color=BLUE, stroke_width=3.6,
                   stroke_opacity=(0.48 if quiet else 1) if tagged else 0).move_to(points[i])
            for i in ACTIVE
        ])
        super().__init__(self.tissue, self.wiring, self.paths, self.cells, self.tags)

    def breathe(self):
        tissue_light(self.tissue)
        for i, cell in enumerate(self.cells):
            bob(cell[1], amp=0.11 * self.cell_scale, speed=2.2, seed=i)
        return self

    def firing(self, on, members=ACTIVE, edges=True):
        color = YELLOW if on else SLATE
        changes = [
            self.cells[i][0].animate.set_fill(color, 0.90 if on else 1).set_stroke(
                color if on else GREY, 2.5 if on else 1.7
            )
            for i in members
        ]
        if edges:
            changes.extend(path.animate.set_stroke(color, 5 if on else 3) for path in self.paths)
        return AnimationGroup(*changes)

    def mark(self, opacity=1):
        return LaggedStart(*[ring.animate.set_stroke(opacity=opacity) for ring in self.tags],
                           lag_ratio=0.16)


def scope():
    return scope_tag(size=28, color=TEXT)


def moving_signal(path, color=YELLOW, radius=0.13):
    head = Dot(path.get_start(), radius=radius, color=color)
    return Succession(FadeIn(head, run_time=0.12),
                      MoveAlongPath(head, path, rate_func=linear, run_time=0.76),
                      FadeOut(head, run_time=0.12))


def incoming(world, name="Recall cue"):
    origin = point(0, 2.94)
    edge = world.coords[1] + point(0.04, 0.28)
    path = branches(origin, edge, 1, color=YELLOW, width=4)
    label = T(name, 29, YELLOW).move_to(point(0, 3.31))
    return path, label


def evidence_ladder():
    rows = []
    for i, name in enumerate(("Correlation", "Sufficiency", "Necessity")):
        y = -1.44 + i * 1.23
        center = point(-5.13, y)
        rung = Line(center + LEFT * 1.12, center + RIGHT * 1.12, stroke_width=4, color=GOLD)
        label = T(name, 30, TEXT).next_to(rung, UP, buff=0.19)
        rows.append(VGroup(rung, label))
    return VGroup(*rows)


def intervention_switches():
    return VGroup(
        boxed_label("ON", GREEN, 30, box=(1.12, 0.59)).move_to(point(4.41, 1.49)),
        boxed_label("OFF", RED, 30, box=(1.18, 0.59)).move_to(point(5.88, 1.49)),
    )


def switch_on(switch, color, active):
    return switch.box.animate.set_fill(color, 0.47 if active else 0.16).set_stroke(
        width=4 if active else 2.5
    )


def behaviour_meter(level):
    x, low, high = 5.15, -1.80, 0.53
    frame = RoundedRectangle(width=1.50, height=high - low, corner_radius=0.15,
                             stroke_color=GREY, stroke_width=2.4).move_to(point(x, (low + high) / 2))
    title = T("Behaviour", 30, TEXT).move_to(point(x, -2.20))
    meter = VGroup(frame, title)

    def fill(value):
        height = 0.055 + 1.94 * value
        ink = interpolate_color(ManimColor(RED), ManimColor(GREEN), value)
        return RoundedRectangle(width=1.16, height=height, corner_radius=min(0.09, height / 2),
                                fill_color=ink, fill_opacity=0.83, stroke_width=0).move_to(
                                    point(x, low + 0.16 + height / 2)
                                )

    return meter, fill(level), fill


def recall_world(level=0, drift=True):
    field = NeuralField(tagged=True, quiet=True)
    if drift:
        field.breathe()
    switches = intervention_switches()
    switches[1].box.set_fill(RED, 0.47).set_stroke(width=4)
    meter, bar, fill = behaviour_meter(level)
    return field, switches, meter, bar, fill


def gut_tube():
    vertices = [
        point(-3.0, -0.60), point(-1.66, -0.49), point(-0.78, -0.81), point(0.25, -0.64),
        point(1.42, -0.83), point(1.76, -1.48), point(0.98, -2.18), point(-0.22, -1.95),
        point(-1.22, -2.15), point(-2.63, -1.96), point(-3.23, -1.40),
    ]
    wall = soft_outline(vertices, GREY, 3.2, SLATE)
    lumen = soft_outline(
        [GUT_CENTER + (p - GUT_CENTER) * np.array([0.87, 0.51, 1]) + DOWN * 0.09
         for p in vertices], LINK, 2.5, TISSUE
    )
    return VGroup(wall, lumen)


def comparison_bar(name, y, color, amount, x=4.62, width=3.55):
    label = T(name, 30, TEXT).move_to(point(x, y + 0.58))
    track = RoundedRectangle(width=width, height=0.33, corner_radius=0.13,
                             fill_color=TISSUE, fill_opacity=1, stroke_width=0).move_to(point(x, y))
    extent = width * amount
    fill = Rectangle(width=extent, height=0.25, stroke_width=0, fill_color=color,
                     fill_opacity=0.82).move_to(track.get_left() + RIGHT * extent / 2)
    return VGroup(track, label), fill


def gut_study_bars():
    learned, acquired = comparison_bar("Learned preference", 0.45, GREEN, 0.90)
    innate, attraction = comparison_bar("Innate attraction", -1.08, GREEN, 0.90)
    return learned, acquired, innate, attraction


def epithelial_wall(native=False):
    """One marked cell in 120 schematic epithelial cells, with cultured and native contours."""
    cells = VGroup()
    for i in range(120):
        row, col = divmod(i, 24)
        if native:
            x = (col - 11.5) * 0.34
            y = (row - 2) * 0.34 + 0.72 * np.cos(x * 0.75)
            heading = 0.08 * np.sin(x)
            width = 0.34
        else:
            angle = TAU * (col + 0.48 * (row % 2)) / 24
            rx, ry = 2.40 + row * 0.33, 0.86 + row * 0.32
            x, y = rx * np.cos(angle), ry * np.sin(angle)
            tx, ty = -rx * np.sin(angle), ry * np.cos(angle)
            heading = np.arctan2(ty, tx)
            width = np.hypot(tx, ty) * TAU / 24 + 0.024
        tile = RoundedRectangle(width=width, height=0.37, corner_radius=0.10,
                                stroke_color=GREY, stroke_width=1.2,
                                fill_color=SLATE, fill_opacity=1).rotate(heading).move_to(point(x, y - 0.32))
        cells.add(tile)
    ring = Circle(radius=0.26, stroke_width=4, color=BLUE).move_to(cells[RARE_CELL])
    return cells, ring


def bound_bar(name, y, color, fraction, greater):
    """The fill reaches the stated bound. The wedge shows the allowed direction."""
    track, fill = comparison_bar(name, y, color, fraction, x=0, width=4.8)
    bound = track[0].get_left() + RIGHT * 4.8 * fraction
    tick = Line(bound + DOWN * 0.22, bound + UP * 0.22, color=TEXT, stroke_width=2)
    x = bound[0]
    tail, tip = (0.08, 0.43) if greater else (0.43, 0.01)
    arrow = Arrow(point(x + tail, y - 0.37), point(x + tip, y - 0.37),
                  buff=0, tip_length=0.11, color=color, stroke_width=3)
    return track, VGroup(fill, tick, arrow)


class S01Hook(SpokenScene):
    def construct(self):
        field = NeuralField().breathe()
        self.add(field, scope())
        banner = T("Experience", 34, YELLOW).move_to(point(0, 3.28))
        sweep = Line(point(-3.22, 2.91), point(3.22, 2.91), stroke_width=2, color=GOLD)
        self.at("During that moment", lead=0.65)
        self.play(Create(sweep), moving_signal(sweep), run_time=0.86)
        self.play(FadeIn(banner), field.firing(True), run_time=0.72)
        self.at("then fades back")
        self.play(field.firing(False), FadeOut(sweep), FadeOut(banner), run_time=1.06)
        rung = evidence_ladder()[0]
        self.at("Watching them fire")
        self.play(GrowFromCenter(rung[0]), run_time=1.0)
        self.play(FadeIn(rung[1], shift=UP * 0.1), run_time=0.54)
        self.at("carry information", lead=0.6)
        arrow = Arrow(point(4.36, -0.55), point(5.91, -0.55), buff=0,
                      color=GREY, stroke_width=4)
        unknown = T("?", 64, GREY).move_to(point(5.16, 0.29))
        self.play(GrowArrow(arrow), run_time=0.64)
        self.at("whether they drive")
        self.play(FadeIn(unknown), run_time=0.55)
        self.finish()


class S02Title(TitleCard):
    LESSON = "Activity-dependent tagging"
    TITLE = "Tagging the Neurons Behind an Experience"

    def construct(self):
        field = NeuralField().breathe()
        self.add(field)
        plate = RoundedRectangle(width=11.6, height=2.50, corner_radius=0.23,
                                 fill_color=BG, fill_opacity=1, stroke_color=LINK, stroke_width=2.2)
        title = T(self.TITLE, 42, TEXT, font=TITLE_FONT).move_to(point(0, -0.19))
        title = fit(title, max_w=10.65)
        lesson = T(self.LESSON, 29, BLUE).move_to(point(0, 0.58))
        self.add(plate)
        self.play(FadeIn(lesson), FadeIn(title), run_time=0.52)
        self.wait(0.83)
        self.play(FadeOut(lesson), FadeOut(title), run_time=0.39)
        self.play(FadeOut(plate), run_time=0.22)


class S03Tagging(SpokenScene):
    def construct(self):
        field = NeuralField().breathe()
        self.add(field, scope())
        tag = T("Genetic tag", 34, BLUE).move_to(point(0, -3.16))
        experience = boxed_label("Experience", YELLOW, 31).move_to(point(0, 3.29))
        self.at("labels cells", lead=0.85)
        self.play(field.firing(True), run_time=1.15)
        self.at("as they fire")
        self.play(LaggedStart(*[moving_signal(path) for path in field.paths], lag_ratio=0.5),
                  run_time=1.95)
        self.at("During a chosen")
        self.play(FadeIn(experience), run_time=0.72)
        self.at("a specific group", lead=0.48)
        self.play(LaggedStart(*[moving_signal(path) for path in field.paths], lag_ratio=0.67),
                  run_time=3.5)
        self.at("the firing itself", lead=0.3)
        self.play(LaggedStart(*[moving_signal(path) for path in field.paths], lag_ratio=0.5),
                  run_time=2.2)
        self.at("lasting genetic label", lead=0.73)
        self.play(field.mark(), run_time=1.27)
        self.play(FadeIn(tag), run_time=0.48)
        self.at("Quiet neighbors")
        self.play(FadeOut(experience), field.firing(False), run_time=1.62)
        for ring in field.tags:
            pulse(ring, base=3.6, amp=1.05, speed=2.15)
        self.at("firing ends")
        self.play(FadeOut(tag), run_time=0.50)
        self.finish()


class S04Interventions(SpokenScene):
    def construct(self):
        field = NeuralField(tagged=True).breathe()
        ladder = evidence_ladder()
        switches = intervention_switches()
        meter, bar, fill = behaviour_meter(0)
        self.add(field, scope())
        self.at("lets you switch", lead=0.45)
        self.play(FadeIn(switches[0]), run_time=0.64)
        self.play(FadeIn(switches[1]), run_time=0.62)
        self.at("climb above correlation")
        self.play(FadeIn(ladder[0], shift=UP * 0.22), run_time=0.64)
        self.play(LaggedStart(*[GrowFromCenter(row[0]) for row in ladder[1:]], lag_ratio=0.38),
                  run_time=1.35)
        self.at("two direct interventions", lead=0)
        self.play(FadeIn(meter), FadeIn(bar), run_time=0.64)
        self.at("Turning tagged cells")
        self.play(switch_on(switches[0], GREEN, True), field.firing(True), run_time=1.06)
        self.play(FadeIn(ladder[1][1]), ladder[1][0].animate.set_color(GREEN), run_time=0.55)
        self.at("enough to drive", lead=0.40)
        self.play(Transform(bar, fill(0.95)), run_time=1.42)
        self.at("Turning them off", lead=0.54)
        self.play(switch_on(switches[0], GREEN, False), switch_on(switches[1], RED, True),
                  field.firing(False), field.mark(0.48), run_time=0.82)
        path, cue = incoming(field)
        self.at("the animal remembers", lead=0.50)
        self.play(FadeIn(cue), Create(path), moving_signal(path), run_time=0.85)
        self.play(FadeOut(cue), FadeOut(path), Transform(bar, fill(0)),
                  run_time=1.12)
        self.at("tests necessity")
        self.play(FadeIn(ladder[2][1]), ladder[2][0].animate.set_color(RED), run_time=0.54)
        self.finish()


class S05Predict(SpokenScene):
    def construct(self):
        field, switches, meter, bar, fill = recall_world()
        self.add(field, switches, meter, bar, scope())
        self.at("Suppose you tag")
        self.play(field.firing(True), switch_on(switches[1], RED, False),
                  FadeOut(meter), FadeOut(bar), run_time=0.86)
        self.play(field.mark(), run_time=1.05)
        self.at("then turn them")
        self.play(field.firing(False), field.mark(0.48), switch_on(switches[1], RED, True),
                  run_time=0.80)
        path, cue = incoming(field)
        self.at("the animal remembers")
        self.play(Create(path), moving_signal(path), FadeIn(cue), run_time=0.94)
        self.play(FadeOut(path), FadeOut(cue), run_time=0.43)
        self.play(FadeIn(meter), run_time=0.74)
        self.at("Recall fails")
        self.play(GrowFromEdge(bar, LEFT), run_time=0.7)
        self.at("Does that prove", lead=0.42)
        self.play(FadeIn(question_card(QUESTION, **CARD), shift=DOWN * 0.10), run_time=0.57)
        self.finish()


class S06Pause(PredictPause):
    QUESTION = QUESTION
    CARD = CARD

    def backdrop(self):
        field, switches, meter, bar, _ = recall_world(drift=False)
        return VGroup(field, switches, meter, bar, scope())

    def construct(self):
        self.add(self.backdrop(), question_card(self.QUESTION, **self.CARD))
        track = RoundedRectangle(width=6.25, height=0.19, corner_radius=0.09,
                                 fill_color=LINK, fill_opacity=1, stroke_width=0)
        track.move_to(point(0, -3.18))
        progress = track.copy().set_fill(GOLD)
        self.add(track)
        self.play(GrowFromEdge(progress, LEFT), run_time=self.narration_s, rate_func=linear)


class S07Controls(SpokenScene):
    def construct(self):
        field, switches, meter, bar, _ = recall_world()
        q = question_card(QUESTION, **CARD)
        answer = question_card("Erasure unproven", **CARD, color=BLUE)
        use = question_card("Used at that moment", **CARD, color=BLUE)
        self.add(field, switches, meter, bar, q, scope())
        self.at("does not prove")
        self.play(swap(q, answer, 0.86), run_time=0.86)
        self.at("the animal uses", lead=0.52)
        self.play(switch_on(switches[1], RED, False), field.mark(),
                  swap(answer, use, 1.15), run_time=1.15)
        self.play(FadeOut(meter), FadeOut(bar), run_time=0.68)
        ladder = evidence_ladder()
        self.at("Sufficiency and necessity")
        ladder[1][0].set_color(GREEN)
        ladder[2][0].set_color(RED)
        self.play(FadeIn(ladder[0], shift=UP * 0.13), run_time=0.64)
        self.play(LaggedStart(FadeIn(ladder[1]), FadeIn(ladder[2]), lag_ratio=0.60), run_time=1.55)
        self.play(FadeOut(use), run_time=0.57)
        checks = VGroup(*[
            T("✓", 32, GREEN).move_to(point(-6.45, row[1].get_y())) for row in ladder
        ])
        controls = T("Controls", 30, GREEN).move_to(point(-5.13, 2.27))
        self.at("Every rung of")
        self.play(FadeIn(controls), run_time=0.52)
        self.play(LaggedStart(*[FadeIn(check) for check in checks], lag_ratio=0.36), run_time=1.60)
        self.at("Networks also share", lead=0.5)
        self.play(FadeOut(controls), FadeOut(checks), FadeOut(ladder), FadeOut(switches), run_time=0.64)
        shared = VGroup(*[
            Circle(radius=0.455, stroke_width=4, color=PURPLE).move_to(field.coords[i]) for i in SHARED
        ])
        self.play(LaggedStart(*[Create(mark) for mark in shared], lag_ratio=0.17), run_time=1.45)
        self.at("circuits reorganize", lead=0.45)
        day_path = Line(point(-2.3, -3.16), point(2.3, -3.16), color=LINK, stroke_width=4)
        days = T("Days", 28, TEXT).move_to(point(-3.13, -3.16))
        scrubber = Dot(day_path.get_start(), color=PURPLE, radius=0.10)
        self.play(FadeIn(days), Create(day_path), FadeIn(scrubber), run_time=0.47)
        new_paths = [
            branches(field.coords[i], field.coords[j], i + j, PURPLE, width=5)
            for i, j in ((3, 8), (8, 10), (10, 14), (14, 17))
        ]
        self.play(MoveAlongPath(scrubber, day_path, rate_func=linear),
                  *[Transform(old, new) for old, new in zip(field.paths, new_paths)], run_time=1.71)
        self.finish()


class S08UnlockedTrap(SpokenScene):
    def construct(self):
        field = NeuralField(tagged=True)
        self.add(field)
        brain = NeuralField(POINTS * 0.53 + BRAIN_SHIFT, scale=0.53)
        gut = gut_tube()
        region = T("Solitary tract (schematic)", 32, TEXT).move_to(point(-0.68, 3.24))
        path = branches(point(-0.66, -1.2), point(-0.52, 0.95), 0, YELLOW, width=4)
        sugar = T("Sugar signal", 30, YELLOW).move_to(point(-2.03, -2.71))
        self.at("gut brain sensing")
        self.play(Transform(field, brain), FadeIn(gut, shift=UP * 0.55), run_time=1.65)
        field.coords, field.cell_scale = brain.coords, brain.cell_scale
        field.breathe()
        tissue_light(gut[1])
        trap = boxed_label("TRAP2", BLUE, 29).move_to(point(-4.85, 1.18))
        self.at("TRAP2")
        self.play(FadeIn(trap), run_time=0.50)
        self.at("It tagged neurons")
        self.play(field.firing(True), run_time=0.76)
        self.play(field.mark(), run_time=0.96)
        self.at("the solitary tract", lead=0.53)
        self.play(FadeIn(region), run_time=0.53)
        self.at("sugar reaching", lead=0.5)
        self.play(Create(path), moving_signal(path), FadeIn(sugar), run_time=1.33)
        trap_count = boxed_label("TRAP2 (n = 6)", BLUE, 29).move_to(trap)
        learned, acquired, innate, attraction = gut_study_bars()
        self.at("six animals", lead=0.42)
        self.play(swap(trap, trap_count, 0.50), run_time=0.50)
        self.play(FadeIn(learned), FadeIn(acquired), run_time=0.65)
        off = intervention_switches()[1].move_to(point(4.62, 2.36))
        self.at("silencing their transmitter", lead=0.43)
        self.play(FadeIn(off), field.firing(False), FadeOut(path), FadeOut(sugar), run_time=0.77)
        self.play(switch_on(off, RED, True), run_time=0.44)
        self.at("abolished development", lead=0)
        empty = Rectangle(width=0.07, height=0.25, stroke_width=0, fill_color=RED, fill_opacity=0.9)
        empty.move_to(learned[0].get_left() + RIGHT * 0.035)
        self.play(Transform(acquired, empty), run_time=1.16)
        self.at("Innate attraction", lead=0.65)
        self.play(FadeIn(innate[0]), GrowFromEdge(attraction, LEFT), run_time=0.73)
        self.play(FadeIn(innate[1]), run_time=0.54)
        self.at("separated first", lead=0.45)
        self.play(Indicate(learned[1], color=RED, scale_factor=1.04),
                  Indicate(innate[1], color=GREEN, scale_factor=1.04), run_time=1.55)
        self.at("the intestinal cell", lead=0.46)
        unknown = T("?", 58, YELLOW).move_to(point(-3.87, -1.57))
        self.play(FadeIn(unknown, shift=LEFT * 0.14), run_time=0.72)
        self.finish()


class S09UnlockedRare(SpokenScene):
    def construct(self):
        gut = gut_tube()
        field = NeuralField(POINTS * 0.53 + BRAIN_SHIFT, scale=0.53, tagged=True)
        self.add(gut, field)
        wall, rare = epithelial_wall()
        self.at("In the gut", lead=0)
        self.play(FadeOut(field, shift=UP * 0.6),
                  gut.animate.shift(-GUT_CENTER).scale(1.65), run_time=1.60)
        self.play(FadeOut(gut), FadeIn(wall), run_time=0.88)
        self.add(scope())
        cell_name = T("Enterochromaffin cell", 32, BLUE).move_to(point(0, -3.19))
        self.at("cells make more", lead=1.23)
        self.play(FadeIn(cell_name), run_time=0.50)
        one, serotonin = bound_bar(">90% serotonin", 2.72, YELLOW, 0.90, True)
        self.at("make more than", lead=0)
        self.play(wall.animate.scale(0.78).shift(DOWN * 0.26), FadeIn(one[0]), run_time=0.74)
        self.play(GrowFromEdge(serotonin[0], LEFT), Create(serotonin[1]),
                  FadeIn(serotonin[2]), run_time=0.88)
        self.play(FadeIn(one[1]), run_time=0.50)
        self.play(wall.animate.scale(1.05).shift(LEFT * 0.13), run_time=1.47)
        self.at("Yet they are under", lead=0.5)
        two, epithelial = bound_bar("<1% epithelial cells", 2.72, BLUE, 0.01, False)
        one_group = VGroup(one, serotonin)
        self.play(one_group.animate.shift(LEFT * 2.97), run_time=0.74)
        VGroup(two, epithelial).shift(RIGHT * 2.97)
        self.play(FadeIn(two[0]), FadeIn(epithelial), run_time=0.63)
        self.play(FadeIn(two[1]), run_time=0.43)
        self.play(wall.animate.scale(1.07).shift(RIGHT * 0.19), run_time=2.64)
        ring_sweep = Ellipse(width=wall.width * 0.81, height=wall.height * 0.80).move_to(wall)
        self.at("Finding so few", lead=0.62)
        self.play(moving_signal(ring_sweep, color=TEXT, radius=0.11), run_time=2.34)
        self.play(FadeOut(one_group), FadeOut(two), FadeOut(epithelial), run_time=0.71)
        target_wall, _ = epithelial_wall()
        self.play(Transform(wall, target_wall), run_time=1.20)
        self.at("Bellono and colleagues", lead=0.6)
        credit = T("Bellono and colleagues, 2017", 32, TEXT).move_to(point(0, 3.16))
        self.play(FadeIn(credit), run_time=0.55)
        self.at("genetically tagged", lead=0.46)
        self.play(Create(rare), wall[RARE_CELL].animate.set_fill(BLUE, 0.85), run_time=0.83)
        cultured = T("Cultured mouse mini-intestine", 32, TEXT).move_to(point(0, -3.03))
        self.play(swap(cell_name, cultured, 0.62), run_time=0.62)
        self.at("then checked native", lead=0.32)
        native, native_ring = epithelial_wall(native=True)
        native[RARE_CELL].set_fill(BLUE, 0.85)
        native_label = T("Native tissue", 32, TEXT).move_to(point(0, -3.03))
        self.play(Transform(wall, native), Transform(rare, native_ring),
                  swap(cultured, native_label, 0.92), run_time=0.92)
        self.finish()


class S10UnlockedEngram(SpokenScene):
    def construct(self):
        wall, ring = epithelial_wall(native=True)
        wall[RARE_CELL].set_fill(BLUE, 0.85)
        field = NeuralField()
        schematic = scope()
        native_label = T("Native tissue", 32, TEXT).move_to(point(0, -3.03))
        credit = T("Bellono and colleagues, 2017", 32, TEXT).move_to(point(0, 3.16))
        self.add(wall, ring, schematic, native_label, credit)
        self.at("In memory circuits", lead=0)
        self.play(FadeOut(wall, shift=DOWN * 0.45), FadeOut(ring, shift=DOWN * 0.45),
                  FadeOut(native_label), FadeOut(credit),
                  FadeIn(field, shift=DOWN * 0.42), run_time=1.33)
        field.breathe()
        self.at("learning strengthens links")
        self.play(field.firing(True), run_time=1.24)
        self.play(LaggedStart(*[moving_signal(path) for path in field.paths], lag_ratio=0.42),
                  run_time=2.22)
        self.at("On this model")
        self.play(field.firing(False, edges=False),
                  *[p.animate.set_stroke(SLATE, 5.4) for p in field.paths], run_time=0.66)
        path, label = incoming(field, "Partial cue")
        self.at("a close enough cue", lead=0.52)
        self.play(FadeIn(label), Create(path), moving_signal(path), run_time=0.92)
        self.play(field.firing(True, members=(1,), edges=False), run_time=0.36)
        self.play(LaggedStart(*[
            AnimationGroup(moving_signal(p), field.firing(True, members=(j,), edges=False))
            for p, (_, j) in zip(field.paths, ACTIVE_EDGES)
        ], lag_ratio=0.36), run_time=1.78)
        proposed = scope_tag("Proposed model", size=28, color=TEXT)
        self.at("one proposed way", lead=0.45)
        self.play(swap(schematic, proposed, 0.68), FadeOut(label), FadeOut(path), run_time=0.68)
        self.play(LaggedStart(*[moving_signal(p) for p in field.paths], lag_ratio=0.43),
                  run_time=3.0)
        self.at("experiments tag those", lead=0.4)
        self.play(field.mark(), run_time=1.24)
        ladder = evidence_ladder()
        switches = intervention_switches()
        self.at("to test sufficiency", lead=0.40)
        self.play(FadeIn(switches[0]), FadeIn(ladder[1]), run_time=0.76)
        self.play(switch_on(switches[0], GREEN, True), run_time=0.44)
        self.at("and necessity")
        self.play(FadeIn(switches[1]), FadeIn(ladder[2]), run_time=0.66)
        self.finish()


class S11Return(SpokenScene):
    def construct(self):
        field = NeuralField(activity=1, tagged=True, strengthened=True).breathe()
        ladder = evidence_ladder()
        switches = intervention_switches()
        self.add(field, scope())
        self.at("Activity fades", lead=0)
        self.play(field.firing(False), run_time=1.35)
        self.at("watching alone")
        self.play(GrowFromCenter(ladder[0][0]), run_time=0.92)
        self.play(FadeIn(ladder[0][1]), run_time=0.61)
        self.at("A lasting genetic", lead=0.40)
        self.play(LaggedStart(*[Indicate(r, color=BLUE, scale_factor=1.14) for r in field.tags],
                              lag_ratio=0.28), run_time=3.95)
        self.at("Switching them on", lead=0.46)
        self.play(FadeIn(switches[0]), FadeIn(ladder[1]), run_time=0.77)
        self.play(FadeIn(switches[1]), FadeIn(ladder[2]), run_time=0.73)
        self.play(switch_on(switches[0], GREEN, True), field.firing(True), run_time=0.72)
        self.play(switch_on(switches[0], GREEN, False), switch_on(switches[1], RED, True),
                  field.firing(False), run_time=0.82)
        self.finish()


class S12End(EndCard):
    LINE = "Tag active neurons genetically, then switch them to test their role."
