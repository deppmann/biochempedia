"""Golgi stain, told through a schematic microscope field.

GREY marks the microscope and unstained tissue. PURPLE marks Nissl-stained
cell bodies, black marks Golgi precipitate, and GREEN marks protein detection.
BLUE marks optical resolution and electron microscopy, YELLOW marks tracing,
and GOLD marks dates, focus and the prediction.
"""

from bp_parts import *  # noqa: F403
from bp_style import EndCard

INK = "#191521"
PAPER = "#E9DBC4"
PAPER_LIGHT = "#F5EAD5"
TISSUE = "#D4BFA8"
GHOST = "#A39193"
PURPLE = "#765190"
DETECTION = "#22745D"
QUESTION = "Separate cells, or fused fibres?"
CARD = {"y": -3.06, "size": 38}
UPPER = 3.13
NM_PER_UNIT = 200 / 4.35


def xy(x, y):
    return np.array([x, y, 0.0])


def curve(points, color=INK, width=4, opacity=1):
    return VMobject().set_points_smoothly([xy(*p) for p in points]).set_stroke(color, width, opacity)


def body(x, y, size, color, angle=0.0):
    return Ellipse(1.6 * size, 2.1 * size, stroke_width=0, fill_color=color,
                   fill_opacity=1).rotate(angle).move_to(xy(x, y))


def title(text, color=TEXT, size=35, x=0):
    return fit_text(text, max_w=11.8, size=size, color=color, min_size=28).move_to(xy(x, UPPER))


def slide():
    """The outer edge of the specimen stays fixed as the microscope view changes."""
    rim = RoundedRectangle(width=12.55, height=5.24, corner_radius=0.30,
                           stroke_color=GREY, stroke_width=2,
                           fill_color=PAPER, fill_opacity=1)
    field = RoundedRectangle(width=12.30, height=4.99, corner_radius=0.23,
                             stroke_width=0, fill_color=PAPER_LIGHT, fill_opacity=1)
    return VGroup(rim, field).move_to(xy(0, 0.07))


def scope():
    return scope_tag(size=28, color=TEXT)


def bundle(paths, color, width, opacity=1):
    """Pack similar dendrites into one drawable while keeping their separate paths."""
    result = VMobject()
    for path in paths:
        result.append_points(curve(path).points)
    return result.set_stroke(color, width, opacity)


# Tips at the apparent junction are shared by the survey and the close-up.
LEFT_BRANCH = [(-3.6, 0.18), (-2.4, 0.54), (-1.55, 0.16), (-0.85, 0.25), (0, 0.08)]
RIGHT_BRANCH = [(3.55, -0.15), (2.45, -0.57), (1.54, -0.30), (0.9, 0.04), (0, 0.08)]
SOMAS = [(-3.6, 0.18), (3.55, -0.15), (0.3, -1.37)]


def stained_cell(index):
    """Three individually traceable neurons, including the two that appear to meet."""
    x, y = SOMAS[index]
    orientation = (1, -1, 1)[index]
    axon_dir = (-1, 1, 1)[index]
    local = [
        [(0, 0), (-0.25, 0.52), (-0.54, 1.1), (-0.48, 1.72)],
        [(-0.54, 1.1), (-0.96, 1.31), (-1.08, 1.64)],
        [(-0.32, 0.71), (0.12, 1.04), (0.36, 1.60)],
        [(0.12, 1.04), (0.6, 1.22), (0.82, 1.50)],
        [(0, 0), (-0.61, 0.15), (-1.12, 0.50), (-1.64, 0.42)],
        [(-1.12, 0.50), (-1.44, 0.91), (-1.73, 1.02)],
        [(0, 0), (0.31, 0.48), (0.58, 0.72), (0.94, 0.91)],
    ]
    vertical = (1, -1, 1)[index]
    scale = (1, 1.09, 0.78)[index]
    dendrites = [[(x + orientation * a * scale, y + vertical * b * scale)
                  for a, b in path] for path in local]
    axon = [(x, y), (x + axon_dir * 0.45, y - 0.24), (x + axon_dir * 1.02, y - 0.48),
            (x + axon_dir * 1.58, y - 0.66), (x + axon_dir * 2.03, y - 0.88)]
    main = (LEFT_BRANCH, RIGHT_BRANCH, [(x, y), (-0.55, -1.21), (-1.1, -0.94), (-1.8, -1.05)])[index]
    return VGroup(body(x, y, 0.27, INK, orientation * 0.52),
                  curve(main, width=8.2), curve(axon, width=4.0),
                  bundle(dendrites, INK, 4.7))


def stained_cells():
    return VGroup(*(stained_cell(i) for i in range(3)))


def tissue():
    """Identical layer landmarks in the dense, Nissl and Golgi views."""
    rng = np.random.default_rng(23)
    locations = []
    for row, (base, count) in enumerate([(1.63, 13), (0.82, 18), (-0.22, 15), (-1.47, 12)]):
        for i, x in enumerate(np.linspace(-5.39, 5.39, count)):
            y = base + 0.13 * np.sin(0.75 * x + row) + rng.uniform(-0.19, 0.19)
            locations.append((x + rng.uniform(-0.18, 0.18), y, rng.uniform(0.083, 0.164)))
    return locations


def strata():
    paths = []
    for base, phase in [(1.2, 1), (0.32, 2), (-0.88, 3)]:
        paths.append([(x, base + 0.13 * np.sin(0.75 * x + phase)) for x in np.linspace(-5.8, 5.8, 20)])
    return bundle(paths, TISSUE, 2.3, 0.54)


def somas(color=GHOST, opacity=0.25, locations=None, nuclei=True):
    locations = tissue() if locations is None else locations
    stains = VGroup()
    for x, y, size in locations:
        stains.add(body(x, y, size, color, -0.28).set_fill(opacity=opacity))
        if nuclei:
            stains.add(Dot(xy(x, y), radius=size * 0.37, color=PAPER_LIGHT).set_fill(opacity=opacity))
    return stains


def tangle(opacity=1):
    rng = np.random.default_rng(93)
    paths = [LEFT_BRANCH, RIGHT_BRANCH]
    for x, y, _ in tissue():
        for direction in (-1, 1):
            a, b, c = rng.uniform(-0.84, 0.84, 3)
            target = (np.clip(x + a * 1.9, -5.95, 5.95), np.clip(y + direction * 1.4, -2.19, 2.31))
            joint = (np.clip(x + a, -5.8, 5.8), np.clip(y + direction * 0.51, -2.06, 2.25))
            paths.append([(x, y), (x + 0.19 * b, y + 0.2 * direction), joint, target])
            paths.append([joint, (np.clip(joint[0] + b * 0.62, -5.89, 5.89),
                                  np.clip(joint[1] + c * 0.67, -2.21, 2.32))])
    return VGroup(bundle(paths, INK, 2.5, 0.70 * opacity), somas(INK, opacity, nuclei=False))


def focus(center=ORIGIN, width=2.7, height=4.2, power=1.0):
    """A soft illumination region traverses the view as the microscope is focused."""
    layers = []
    for amount in np.linspace(1, 0.20, 9):
        layers.append(Ellipse(width * amount, height * amount, stroke_width=0,
                              fill_color=GOLD, fill_opacity=0.047 * power))
    return VGroup(*layers).move_to(center)


def scan(width=2.7, height=4.2, swing=4.2, speed=0.96, y=0.08, power=1):
    light = focus(xy(-swing, y), width, height, power)
    clock = ValueTracker(0)

    def travel(mob, dt):
        clock.increment_value(dt)
        mob.move_to(xy(-swing * np.cos(speed * clock.get_value()), y))

    return light.add_updater(travel)


def branch_pair(gap_nm=0, color=INK):
    """A magnified view of the meeting tips. Only the gap width is to scale."""
    half_gap = gap_nm / NM_PER_UNIT / 2
    left = [(-5.73, 1.65), (-4.5, 1.58), (-3.24, 0.90), (-2.4, 0.37),
            (-1.30, 0.56), (-half_gap, 0.08)]
    right = [(5.73, -1.56), (4.52, -1.71), (3.25, -0.91), (2.35, -0.54),
             (1.25, -0.18), (half_gap, 0.08)]
    twigs = [[left[2], (-3.16, 1.52), (-2.47, 2.02), (-1.73, 2.25)],
             [left[3], (-3.02, -0.26), (-3.48, -0.58), (-4.08, -0.62)],
             [right[2], (3.20, -1.44), (2.72, -1.96), (1.90, -2.20)],
             [right[3], (3.14, 0.07), (3.55, 0.49), (4.20, 0.66)]]
    branches = VGroup(curve(left, color, 23), curve(right, color, 23))
    return VGroup(branches, bundle(twigs, color, 10))


def junction(gap_nm=0):
    return VGroup(slide(), branch_pair(gap_nm))


def reticle():
    return Circle(radius=1.04, stroke_color=DETECTION, stroke_width=3.5,
                  stroke_opacity=0.76).move_to(xy(0, 0.08))


def predict_world():
    return VGroup(junction(), reticle(), scope())


def optical_blur():
    """Layered disc whose outer diameter is 200 nm on the junction scale."""
    radius = 100 / NM_PER_UNIT
    center = xy(0, 0.08)
    return VGroup(
        *(Circle(radius=radius * fraction, stroke_width=0, fill_color=BLUE,
                 fill_opacity=0.055).move_to(center) for fraction in np.linspace(1, 0.18, 9)),
        Circle(radius=radius, stroke_color=DETECTION, stroke_width=2.7).move_to(center),
    )


def dimension(x0, x1, y, color):
    marks = [Line(xy(x0, y), xy(x1, y))]
    marks.extend(Line(xy(x, y - 0.12), xy(x, y + 0.12)) for x in (x0, x1))
    return VGroup(*marks).set_stroke(color, 4)


class S01Hook(SpokenScene):
    def construct(self):
        ghost = tangle(0.49)
        light = scan(power=1.4)
        self.add(slide(), strata(), ghost, light, scope())
        self.at("trace one neuron")
        trace = curve(LEFT_BRANCH, width=4)
        trace.pointwise_become_partial(trace.copy(), 0, 0.78)
        tracer = Dot(trace.get_start(), radius=0.105, color=YELLOW, stroke_color=INK, stroke_width=2)
        self.play(FadeIn(tracer), run_time=0.28)
        self.play(MoveAlongPath(tracer, trace), run_time=3.70, rate_func=linear)
        self.at("stain every cell")
        self.play(Transform(ghost, tangle()), FadeOut(tracer), run_time=3.9)
        self.at("follow a single branch")
        lost = trace.copy().set_stroke(YELLOW, 6)
        self.play(Create(lost), run_time=1.5)
        self.play(Uncreate(lost), run_time=0.82)
        self.at("1873")
        date = title("1873", GOLD, 46)
        self.play(FadeIn(date, shift=UP * 0.09), run_time=0.56)
        self.finish()


class S02Title(TitleCard):
    TITLE = "Staining a Few Neurons to See Them Whole"
    LESSON = "Golgi stain"

    def construct(self):
        base = slide()
        base[0].set_fill(opacity=0.08).set_stroke(opacity=0.24)
        base[1].set_fill(opacity=0.10)
        threads = tangle(0.10)
        # Faint specimen silhouettes remain legible behind the held title.
        threads[0].set_stroke(opacity=0.23)
        picture = VGroup(base, threads, scan(power=0.22))
        heading = fit_text(self.TITLE, max_w=11.6, size=47, min_size=34, font=TITLE_FONT)
        lesson = T(self.LESSON, 28, TEAL)
        rule = Line(LEFT * 0.62, RIGHT * 0.62, color=GOLD, stroke_width=4)
        words = VGroup(lesson, heading, rule).arrange(DOWN, buff=0.31)
        self.add(picture, words)
        self.wait(1.80)
        self.play(FadeOut(words), run_time=0.20)


class S03HowItWorks(SpokenScene):
    def construct(self):
        cells = somas(PURPLE, 0.20)
        boundaries = strata()
        light = scan(power=1.65)
        threads = tangle(0.11)[0]
        self.add(slide(), boundaries, threads, cells, light, scope())
        self.at("stain binds")
        lit = somas(PURPLE, 0.96)
        self.play(LaggedStart(*(Transform(a, b) for a, b in zip(cells, lit)),
                              lag_ratio=0.035), run_time=3.8)
        nissl = title("Nissl stain")
        self.at("marking cell bodies")
        self.play(FadeIn(nissl), run_time=0.45)
        self.at("layer boundaries")
        self.play(boundaries.animate.set_stroke(PURPLE, 3.4, 0.67), run_time=1.35)
        self.at("silver chromate")
        silver = title("Golgi silver chromate")
        self.play(swap(nissl, silver, 0.9), FadeOut(threads),
                  Transform(cells, somas()), Transform(boundaries, strata()), run_time=2.2)
        chosen = stained_cells()
        self.at("blackens only")
        self.play(LaggedStart(*(GrowFromCenter(cell[0]) for cell in chosen), lag_ratio=0.7),
                  run_time=3.4)
        self.at("neuron fills")
        self.play(LaggedStart(*(AnimationGroup(Create(cell[1]), Create(cell[2]), Create(cell[3]))
                                for cell in chosen), lag_ratio=0.26), run_time=4.65)
        self.finish()


class S04PredictQuestion(SpokenScene):
    def construct(self):
        field = VGroup(strata(), somas(), stained_cells())
        light = scan(power=1.45)
        self.add(slide(), field, light, scope())
        separate = title("Separate cells", TEXT, x=-3.48)
        fused = title("Fused fibres", TEXT, x=3.48)
        focus_ring = reticle()
        self.at("system separate cells")
        self.play(FadeIn(separate), run_time=0.58)
        self.at("one continuous network")
        self.play(FadeIn(fused), run_time=0.58)
        self.at("zoom into this")
        near = branch_pair()
        # Keep the two branch tips pinned to the same point during magnification.
        tips = VGroup(field[2][0][1].copy(), field[2][1][1].copy())
        self.add(tips)
        self.play(FadeOut(field), FadeOut(separate), FadeOut(fused),
                  Transform(tips, near[0]), FadeIn(near[1]), run_time=3.35)
        self.at("stain under a light")
        self.play(Create(focus_ring), run_time=1.06)
        self.play(FadeIn(question_card(QUESTION, **CARD)), run_time=0.58)
        self.at("cells are separate")
        self.play(FadeOut(light), run_time=0.5)
        self.finish()


class S05PredictPause(PredictPause):
    QUESTION = QUESTION
    CARD = CARD
    SECONDS = 4.5

    def backdrop(self):
        return predict_world()

    def construct(self):
        world = self.backdrop()
        world[1].add_updater(lambda m, dt: m.set_stroke(
            opacity=0.70 + 0.13 * np.sin(TAU * self.elapsed() / self.SECONDS)))
        question = question_card(self.QUESTION, **self.CARD)
        start, end = xy(-6.10, -3.54), xy(4.20, -3.54)
        rail = Line(start, end, color=GREY, stroke_width=3)
        timer = Line(start, end, color=GOLD, stroke_width=10)
        self.add(world, question, rail)
        self.play(Create(timer), rate_func=linear, run_time=self.SECONDS)


class S06OpticalLimit(SpokenScene):
    def construct(self):
        field = junction()
        ring = reticle()
        question = question_card(QUESTION, **CARD)
        light = scan(width=2.4, height=3.7, swing=4.0, power=1.38)
        self.add(field, ring, question, scope(), light)
        self.at("light blurs tiny gaps")
        self.play(FadeOut(question), FadeOut(ring), run_time=0.48)
        disc = optical_blur()
        self.at("blurs points closer")
        self.play(GrowFromCenter(disc), run_time=1.7)
        outer = 100 / NM_PER_UNIT
        width = dimension(-outer, outer, 2.38, DETECTION)
        label = title("Light-microscope limit · 200 nm", BLUE)
        self.at("200 nanometers side")
        self.play(Create(width), FadeIn(label), run_time=0.82)
        self.at("chemical synapse")
        gap_view = branch_pair(20)
        self.play(Transform(field[1], gap_view), run_time=1.34)
        half_gap = 10 / NM_PER_UNIT
        gap = dimension(-half_gap, half_gap, -0.82, DETECTION)
        self.at("20 nanometers")
        gap_label = caption("Chemical synapse gap · 20 nm", 33, BLUE)
        self.play(Create(gap), FadeIn(gap_label), run_time=0.52)
        equation = VGroup(M("200 nm", 40, BLUE), M("÷", 40), M("20 nm", 40, BLUE),
                          M("=", 40), M("10×", 40, GOLD)).arrange(RIGHT, buff=0.29)
        equation.move_to(xy(-0.65, -3.08))
        self.at("200 divided")
        self.play(FadeOut(gap_label), run_time=0.17)
        self.play(FadeIn(equation[0]), FadeIn(equation[1]), run_time=0.36)
        self.at("by 20 is")
        self.play(FadeIn(equation[2]), run_time=0.31)
        self.at("is 10 so")
        self.play(FadeIn(equation[3]), FadeIn(equation[4]), run_time=0.42)
        self.at("where branches met")
        # Broaden the recorded edges at the gap while keeping the physical tips fixed.
        bridge = VGroup(
            Line(xy(-half_gap, 0.15), xy(half_gap, 0.01), color=INK, stroke_width=20).set_opacity(0.26),
            Line(xy(-half_gap, 0.15), xy(half_gap, 0.01), color=INK, stroke_width=14).set_opacity(0.45),
        )
        self.play(FadeOut(gap), FadeOut(width), FadeIn(bridge),
                  disc.animate.set_stroke(opacity=0.45), run_time=1.8)
        self.finish()


def fibres():
    """Fixed young fibres at three lengths, ending at their observed positions."""
    group = VGroup()
    for x, tip, lean in [(-3.7, -0.32, 0.30), (-1.17, 0.52, 0.57), (1.33, 1.65, 0.72), (3.9, 0.98, 0.5)]:
        group.add(VGroup(body(x, -1.63, 0.25, INK, 0.3),
                         curve([(x, -1.63), (x - 0.04, -1.16),
                                (x + lean * 0.36, (tip - 1.13) / 2), (x + lean, tip)], INK, 7),
                         body(x + lean, tip, 0.105, INK, -0.35)))
    return group


def tilted_section():
    front = [(-5.85, 0.78), (-4.22, -1.47), (5.82, -1.47), (4.22, 0.78)]
    back = [(x, y + 1.02) for x, y in front]
    edge = Polygon(xy(*front[1]), xy(*front[2]), xy(*back[2]), xy(*back[1]),
                   stroke_color=GHOST, stroke_width=3, fill_color=TISSUE, fill_opacity=0.87)
    plane = Polygon(*(xy(*p) for p in back), stroke_color=GHOST, stroke_width=3,
                    fill_color=PAPER, fill_opacity=0.93)
    a = curve([(-4.75, 1.22), (-2.0, 1.33), (0.1, 0.81), (2.11, 0.94), (4.0, 0.36)], width=14)
    b = curve([(-3.82, -0.58), (-1.92, -0.94), (0.70, -0.10), (2.68, 0.38), (4.77, 0.48)],
              "#66505C", 14)
    return VGroup(edge, plane, a, b)


class S07MoreLimits(SpokenScene):
    def construct(self):
        field = branch_pair()
        self.add(slide(), field, scope())
        depth = tilted_section()
        self.at("a stain section")
        self.play(FadeOut(field), FadeIn(depth, scale=0.94), run_time=1.12)
        thickness = title("Section thickness  ≥100 µm", BLUE)
        self.at("100 micrometers or")
        self.play(FadeIn(thickness), run_time=0.52)
        light = focus(xy(0, 1.42), width=10.8, height=0.82, power=1.65)
        self.at("focusing up and down")
        self.play(FadeIn(light), run_time=0.32)
        self.play(light.animate.move_to(xy(0, -0.95)), run_time=1.01)
        axial = title("Depth blur  ~0.5–1 µm", BLUE)
        self.at("roughly 0")
        self.play(swap(thickness, axial), light.animate.move_to(xy(0, 0.41)), run_time=1.62)
        self.at("stacked branches look joined")
        merged = curve([(-3.82, -0.58), (-1.92, -0.56), (0.70, 0.75), (2.68, 0.73), (4.77, 0.48)],
                       INK, 14)
        self.play(Transform(depth[3], merged), light.animate.move_to(xy(0, 0.93)), run_time=1.9)
        self.at("fixed tissue")
        fixed = title("Fixed tissue")
        still = fibres()
        self.play(swap(axial, fixed), FadeOut(depth), FadeOut(light), FadeIn(still), run_time=1.35)
        self.at("shape and position")
        markers = VGroup(*(Circle(radius=0.21, stroke_color=DETECTION, stroke_width=3.0)
                           .move_to(f[2]) for f in still))
        self.play(LaggedStart(*(Create(m) for m in markers), lag_ratio=0.5), run_time=1.25)
        self.at("never movement")
        raking_light = focus(xy(-4.25, 0.08), 3.55, 4.1, power=1.65)
        self.play(FadeIn(raking_light), FadeOut(markers), run_time=0.47)
        self.play(raking_light.animate.move_to(xy(4.25, 0.08)), run_time=1.92, rate_func=linear)
        self.finish()


def electron_view(contact=False):
    """A second instrument's view, with the section edges sharply resolved."""
    plate = RoundedRectangle(width=4.95, height=3.65, corner_radius=0.2,
                             stroke_color=BLUE, stroke_width=3,
                             fill_color="#26313E", fill_opacity=1)
    if contact:
        # Section through an elongated young cell alongside the radial fibre.
        young = [(-1.56, -1.41), (-1.20, -0.94), (-1.35, -0.42),
                 (-1.14, 0.28), (-0.54, 0.72), (0.30, 0.56),
                 (0.43, 0.0), (0.25, -0.46), (-0.43, -0.88), (-1.07, -1.49)]
        radial = [(0.54, -1.52), (0.51, -0.74), (0.43, 0.0),
                  (0.39, 0.81), (0.49, 1.48), (1.79, 1.48),
                  (1.68, 0.55), (1.73, -0.32), (1.86, -1.52)]
        edges = VGroup()
        for outline, fill in [(young, "#71818C"), (radial, "#516A78")]:
            boundary = curve(outline + [outline[0]], PAPER_LIGHT, 2.6)
            boundary.set_fill(fill, 1)
            edges.add(boundary)
        return VGroup(plate, edges).move_to(xy(3.12, 0.08))
    separation = 0.52
    edge_a = [(-2.26, 1.37), (-1.29, 1.24), (-0.56, 0.67), (-separation, 0.37),
              (-separation, -0.35), (-0.61, -0.7), (-1.37, -1.31), (-2.26, -1.39)]
    edge_b = [(2.26, 1.29), (1.44, 1.19), (0.62, 0.72), (separation, 0.34),
              (separation, -0.35), (0.67, -0.72), (1.46, -1.29), (2.26, -1.42)]
    face_a = Polygon(*(xy(*q) for q in edge_a), fill_color="#71818C", fill_opacity=1, stroke_width=0)
    face_b = Polygon(*(xy(*q) for q in edge_b), fill_color="#71818C", fill_opacity=1, stroke_width=0)
    rims = VGroup(curve(edge_a[1:-1], PAPER_LIGHT, 3.0), curve(edge_b[1:-1], PAPER_LIGHT, 3.0))
    return VGroup(plate, face_a, face_b, rims).move_to(xy(3.12, 0.08))


def strips():
    """Serial sections keep the same captured fibre position in each frame."""
    group = VGroup()
    for _ in range(3):
        box = RoundedRectangle(width=1.16, height=0.86, corner_radius=0.10,
                               stroke_color=GHOST, stroke_width=2, fill_color=PAPER, fill_opacity=1)
        mark = curve([(-0.38, -0.27), (-0.07, -0.01), (0.12, 0.25)], width=4.3)
        group.add(VGroup(box, mark))
    return group.arrange(RIGHT, buff=0.18).move_to(xy(-2.91, 0.10))


class S08Guards(SpokenScene):
    def construct(self):
        fixed = fibres()
        layer = strata()
        ghost = somas()
        complete = stained_cells()
        light = scan(power=1.62)
        self.add(slide(), fixed, light, scope())
        self.at("pairing methods")
        self.play(FadeOut(fixed), FadeIn(layer), FadeIn(ghost), FadeIn(complete), run_time=1.46)
        self.at("nissl stains handle")
        nissl = title("Nissl stain · cell bodies")
        self.play(FadeOut(complete), Transform(ghost, somas(PURPLE, 0.96)),
                  layer.animate.set_stroke(PURPLE, 3.8, 0.60), run_time=1.30)
        self.play(FadeIn(nissl), run_time=0.54)
        self.at("immunostaining uses")
        target = title("Immunostaining · protein detection")
        self.play(swap(nissl, target, 1.10), Transform(layer, strata()),
                  Transform(ghost, somas()), run_time=1.28)
        self.at("one chosen protein")
        locations = tissue()
        selected = [locations[i] for i in (6, 15, 25, 36, 46, 54)]
        signal = somas(DETECTION, 1, selected, nuclei=False)
        halos = VGroup(*(Circle(radius=s * 1.44, stroke_color=DETECTION, stroke_width=2.3,
                                fill_color=GREEN, fill_opacity=0.26).move_to(xy(x, y)) for x, y, s in selected))
        self.play(LaggedStart(*(GrowFromCenter(m) for m in halos), lag_ratio=0.31), run_time=2.25)
        self.at("target was detected")
        self.play(FadeIn(signal), run_time=0.64)
        self.at("electron microscopy")
        em = title("Electron microscopy · resolved gap", BLUE)
        detail = electron_view()
        self.play(swap(target, em), FadeOut(signal), FadeOut(halos),
                  FadeIn(detail, scale=0.91), run_time=1.18)
        self.at("proving movement")
        snapshots = strips()
        self.play(FadeOut(ghost), FadeOut(layer), FadeOut(light), FadeIn(snapshots, shift=UP * 0.15),
                  run_time=0.76)
        dot = Dot(radius=0.11, color=DETECTION).move_to(xy(-4.49, -1.05))
        track = curve([(-4.49, -1.05), (-3.57, -1.25), (-2.43, -1.09), (-1.31, -0.65)],
                      DETECTION, 4)
        self.play(FadeIn(dot), run_time=0.31)
        self.play(Create(track), MoveAlongPath(dot, track.copy()), run_time=1.67, rate_func=linear)
        self.finish()


def growth_cone():
    """An enlargement of the swollen tip and its fine projections."""
    axon = curve([(-5.53, -1.65), (-3.65, -1.25), (-2.44, -0.32),
                  (-1.28, 0.13), (-0.18, 0.37)], width=23)
    club = VMobject(fill_color=INK, fill_opacity=1, stroke_width=0)
    contour = [(-1.15, -0.01), (-0.38, 0.05), (0.49, 0.06), (1.37, 0.25),
               (2.13, 0.46), (2.55, 0.92), (2.09, 1.41), (1.33, 1.53),
               (0.54, 1.20), (-0.16, 0.88), (-0.77, 0.52), (-1.15, -0.01)]
    club.set_points_smoothly([xy(*p) for p in contour])
    spikes = [[(2.12, 1.31), (3.18, 1.50), (4.13, 1.42)],
              [(2.50, 0.93), (3.36, 0.93), (4.04, 0.67)],
              [(2.32, 0.61), (3.15, 0.23), (3.68, -0.57)],
              [(1.83, 0.44), (2.60, -0.12), (2.75, -0.73)],
              [(1.20, 1.49), (1.86, 1.91), (2.69, 2.29)],
              [(0.65, 1.19), (0.95, 1.82), (1.26, 2.23)],
              [(0.43, 0.12), (0.77, -0.48), (1.32, -0.80)],
              [(1.64, 1.49), (2.03, 1.74), (2.26, 2.12)]]
    return VGroup(axon, club, bundle(spikes, INK, 5.8))


class S09UnlockedEarly(SpokenScene):
    def construct(self):
        original = VGroup(strata(), somas(), stained_cells())
        light = scan(power=1.65)
        self.add(slide(), original, light, scope())
        self.at("golgi stain unlocked")
        self.play(original[0].animate.set_stroke(opacity=0.25), original[1].animate.set_opacity(0.14),
                  run_time=2.4)
        date = title("1873", GOLD, 46)
        self.at("1873 arrival")
        self.play(FadeIn(date), run_time=0.58)
        separate = caption("Separate cells", size=33).shift(LEFT * 2.0)
        fused = caption("Fused fibres", size=33).shift(RIGHT * 2.0)
        self.at("separate cells versus")
        self.play(FadeIn(separate), run_time=0.42)
        self.at("fused fibers")
        self.play(FadeIn(fused), run_time=0.58)
        cord = fibres()
        cord_label = title("1890 · Chick embryo spinal cord", GOLD)
        self.at("1890")
        self.play(swap(date, cord_label), FadeOut(separate), FadeOut(fused), FadeOut(original),
                  FadeIn(cord), run_time=2.6)
        self.at("young nerve fibers")
        tip = growth_cone()
        self.play(ReplacementTransform(cord[2].copy(), tip),
                  FadeOut(cord), run_time=2.43)
        self.at("the growth cone")
        self.play(FadeIn(caption("Growth cone", 36, GOLD)), run_time=0.56)
        self.finish()


def cortex():
    """The section shows the radial fibres alongside fixed young neurons."""
    band = Polygon(xy(-5.83, 1.84), xy(-5.83, 2.32), xy(5.83, 2.32), xy(5.83, 1.84),
                   stroke_width=0, fill_color=TISSUE, fill_opacity=0.90)
    paths, young = [], VGroup()
    for i, x in enumerate(np.linspace(-5.25, 5.1, 8)):
        offset = (-0.12 if i % 2 == 0 else 0.09)
        path = [(x - 0.27, -2.24), (x + offset, -0.75),
                (x - 0.15, 0.63), (x + 0.24, 2.22)]
        paths.append(path)
        if i in (1, 3, 4, 6):
            y = (-0.68, 0.46, 0.88, -0.73)[(1, 3, 4, 6).index(i)]
            x_near = x + 0.15
            young.add(VGroup(body(x_near, y, 0.249, INK, -0.12),
                             curve([(x_near, y), (x_near - 0.025, y + 0.36),
                                    (x_near + 0.05, y + 0.82)], width=6.8)))
    guide = bundle(paths, "#8A666F", 9)
    return VGroup(band, guide, young)


class S10UnlockedRakicReturn(SpokenScene):
    def construct(self):
        light = scan(width=2.5, power=1.68)
        cone = growth_cone()
        self.add(slide(), cone, light, scope())
        cortical = cortex()
        date = title("1972 · Fetal rhesus cortex", GOLD)
        self.at("1972")
        self.play(FadeOut(cone), FadeIn(cortical[0]), run_time=0.70)
        self.play(FadeIn(date), Create(cortical[1]), run_time=2.00)
        self.at("serial electron microscopy")
        em = electron_view(contact=True)
        self.play(FadeIn(em, scale=0.88), run_time=1.35)
        self.at("fetal")
        self.play(FadeOut(em), run_time=1.18)
        self.at("found young neurons")
        self.play(LaggedStart(*(FadeIn(neuron) for neuron in cortical[2]), lag_ratio=0.63),
                  run_time=2.55)
        self.at("cortical plate")
        plate = caption("Cortical plate", 34)
        self.play(cortical[0].animate.set_fill(color="#CBA383", opacity=1),
                  FadeIn(plate), run_time=0.68)
        self.at("pairing methods answered")
        paired = title("Golgi stain + serial electron microscopy", BLUE)
        self.play(swap(date, paired, 1.1), FadeIn(em, scale=0.93),
                  FadeOut(plate), run_time=1.56)
        self.at("leaving most cells unseen")
        last = stained_cell(0).scale(1.63)
        last.move_to(xy(0, 0.07))
        self.play(FadeOut(cortical[0]), FadeOut(cortical[1]), FadeOut(cortical[2]),
                  FadeOut(em), FadeOut(paired), FadeIn(last), run_time=2.20)
        self.finish()


class S11End(EndCard):
    LINE = "Stain a few cells completely to see shape, not gaps or motion."
