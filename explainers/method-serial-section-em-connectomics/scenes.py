"""Serial-section EM connectomics, timed to the supplied narration.

Color map from the methods films: grey = tissue and micrographs, blue =
ganglion cells, purple = amacrine cells, yellow = contacts and active
highlights, green = functional readout, red = pathway perturbation, gold =
questions and study credits.
"""

from bp_parts import *

PURPLE = "#B58CD9"
BAR = GREEN
BLOCK_X = -2.75
TOP = 1.04
BOTTOM = -2.64
STEP = 0.27
SLICES = 4
ASK = "More contacts = stronger synapse?"
END_LINE = "Serial slices map every contact; proving synapses and function takes more."

# Coordinates are shared by the projected block, its exposed face, and the
# scan. The same depth-indexed face becomes a detached micrograph.
def point(x, y):
    return np.array([x, y, 0.0])


def face(u, v, x=BLOCK_X, y=TOP, scale=1):
    return point(x + scale * (5.7 * (u - 0.5) + 1.25 * v), y + scale * 1.76 * v)


def polygon(vertices, fill, outline=GREY, opacity=1, width=1.8):
    return Polygon(*vertices, fill_color=fill, fill_opacity=opacity,
                   stroke_color=outline, stroke_width=width)


def face_corners(x=BLOCK_X, y=TOP, scale=1):
    return [face(u, v, x, y, scale) for u, v in [(0, 0), (1, 0), (1, 1), (0, 1)]]


def stroke(coords, color, width, opacity=1):
    path = VMobject(stroke_color=color, stroke_width=width, stroke_opacity=opacity)
    path.set_points_smoothly([point(*xy) for xy in coords])
    return path


def arbor(color, root, branches):
    # Each line starts on its parent branch. Dark outer strokes distinguish
    # crossing processes without claiming that each crossing is a contact.
    shadows = [stroke(coords, BG, width + 3, 0.8) for width, coords in branches]
    lines = [stroke(coords, color, width) for width, coords in branches]
    if root is not None:
        soma = Ellipse(width=0.51, height=0.34, color=color, stroke_width=2.5,
                       fill_color=color, fill_opacity=0.75).move_to(point(*root))
        lines.append(soma)
    return VGroup(*shadows, *lines)


LEFT_RUN = [(-0.65, 0.05), (-1.35, 0.48), (-2.1, 0.53), (-2.88, 0.34)]
RIGHT_RUN = [(0.05, 0.03), (0.75, 0.44), (1.55, 0.47), (2.75, 0.27)]
MANY = [(-2.68, 0.42), (-2.40, 0.52), (-2.11, 0.59), (-1.83, 0.60),
        (-1.56, 0.57), (-1.3, 0.49)]
FEW = [(1.0, 0.53), (2.07, 0.46)]


def circuit():
    amacrine = arbor(PURPLE, (-0.32, -0.14), [
        (8, [(-0.32, -0.14), *LEFT_RUN]),
        (7, [(-0.32, -0.14), *RIGHT_RUN]),
        (6, [(-0.32, -0.14), (-0.94, -0.54), (-1.9, -0.71), (-2.66, -0.48)]),
        (6, [(-0.32, -0.14), (0.1, -0.65), (0.92, -1.06), (1.96, -0.9)]),
        (4, [(-1.35, 0.48), (-2.01, 0.04), (-2.81, -0.05)]),
        (4, [(-1.9, -0.71), (-2.14, -1.03), (-2.66, -1.13)]),
        (4, [(1.55, 0.47), (2.03, -0.04), (2.8, -0.24)]),
        (4, [(0.92, -1.06), (1.29, -1.44), (2.18, -1.48)]),
    ])
    left = arbor(BLUE, (-2.12, -1.82), [
        (11, [(-2.12, -1.82), (-2.08, -1.23), (-1.79, -0.62), (-1.83, 0.62)]),
        (8, [(-2.95, 0.33), *MANY, (-0.87, 0.38)]),
        (5, [(-2.4, 0.52), (-2.57, 0.89), (-2.9, 1.03)]),
        (4, [(-1.56, 0.57), (-1.27, 0.87), (-0.73, 0.99)]),
        (6, [(-2.12, -1.82), (-2.33, -2.20)]),
    ])
    right = arbor(BLUE, (1.93, -1.76), [
        (11, [(1.93, -1.76), (1.84, -1.13), (1.62, -0.53), (1.7, 0.66)]),
        (8, [(0.58, 0.66), (1.0, 0.54), (1.7, 0.66), (2.07, 0.46), (2.78, 0.68)]),
        (5, [(1.7, 0.66), (2.2, 0.89), (2.69, 1.02)]),
        (4, [(1.62, -0.53), (1.22, -0.2), (0.65, -0.25)]),
        (6, [(1.93, -1.76), (2.10, -2.17)]),
    ])
    return VGroup(amacrine, left, right)


def retinal_block(x=BLOCK_X, cut=0):
    y = TOP - cut * STEP
    a, b, c, d = face_corners(x, y)
    drop = DOWN * (y - BOTTOM)
    front = polygon([a, b, b + drop, a + drop], "#293D54", TEAL, 0.91)
    side = polygon([b, c, c + drop, b + drop], "#354965", TEAL, 0.88)
    surface = polygon([a, b, c, d], "#445A70", BLUE, 0.83)
    bands = VGroup()
    for f in (0.20, 0.41, 0.64, 0.82):
        offset = drop * f
        bands.add(VMobject(stroke_color=BLUE, stroke_width=1.0, stroke_opacity=0.23)
                  .set_points_as_corners([a + offset, b + offset, c + offset]))
    return VGroup(front, side, surface, bands)


def dense_arbors(x=BLOCK_X):
    """Additional profiles within the same schematic volume."""
    layers = VGroup()
    for index, (dx, dy) in enumerate([(-0.95, 0.36), (0.9, 0.10), (2.0, 0.35),
                                      (-0.80, -0.13), (0.30, 0.55), (1.48, -0.25),
                                      (-1.05, 0.05), (1.34, 0.73), (0.25, -0.33)]):
        cell = circuit()[index % 3].scale(0.43 + 0.08 * (index % 3))
        if index % 2:
            cell.flip()
        cell.move_to(point(x + dx, dy))
        layers.add(cell)
    return layers


def volume(x=BLOCK_X, dense=False):
    block = retinal_block(x)
    branches = circuit().scale(0.87).shift(point(x, -0.25))
    background = dense_arbors(x) if dense else VGroup(*dense_arbors(x)[:3]).fade(0.55)
    return VGroup(block, background, branches)


def drift(mob):
    return bob(mob, amp=0.13, speed=1.6)


def diagram_tag():
    return scope_tag(size=28, color=TEXT)


def head(words, color=TEXT, x=0):
    return fit_text(words, max_w=10.8, size=34, min_size=30, color=color).move_to(point(x, 3.32))


def side_text(words, color=TEXT, x=3.9, y=0.25):
    return T(words, 34, color).move_to(point(x, y))


def profile_data(index, count=38):
    rng = np.random.default_rng(782)
    for n in range(count):
        u = rng.uniform(0.10, 0.90)
        # Put the traced profiles on the exposed band of each stacked plate.
        v = rng.uniform(0.17, 0.40) if n < 12 else rng.uniform(0.14, 0.86)
        radius = rng.uniform(0.022, 0.052)
        phase = rng.uniform(0, TAU)
        yield (u + 0.025 * np.sin(index * 0.72 + phase),
               v + 0.04 * np.cos(index * 0.75 + phase), radius, phase)


def profile(spec, x, y, scale, color, fill, width):
    u, v, radius, phase = spec
    vertices = []
    for theta in np.linspace(0, TAU, 16, endpoint=False):
        r = radius * (1 + 0.15 * np.sin(3 * theta + phase))
        vertices.append(face(u + r * np.cos(theta), v + 2.3 * r * np.sin(theta), x, y, scale))
    outline = VMobject(stroke_color=color, stroke_width=width, fill_color=color, fill_opacity=fill)
    return outline.set_points_smoothly([*vertices, vertices[0]])


def micrograph(index, x, y, scale=1):
    sheet = polygon(face_corners(x, y, scale), "#747E88", TEXT)
    rng = np.random.default_rng(140 + index)
    textures = []
    for _ in range(46):
        u, v = rng.uniform(0.02, 0.98), rng.uniform(0.06, 0.94)
        textures.append(Dot(face(u, v, x, y, scale), radius=rng.uniform(0.015, 0.039) * scale,
                            color=rng.choice(["#B1BAC1", "#505B66", "#636D79"])))
    profiles = [profile(spec, x, y, scale, c, 0.28, 1.3)
                for spec, c in zip(profile_data(index), ["#303941", "#A8B1BA", "#CFD4D9"] * 13)]
    return VGroup(sheet, *textures, *profiles)


def stack_position(index, x=3.75):
    return x - 0.18 * index, -1.70 + 0.66 * index


def stack(x=3.75):
    return VGroup(*(micrograph(i, *stack_position(i, x), scale=0.70) for i in range(SLICES)))


def scan(scene, index, seconds):
    y = TOP - index * STEP
    line = Line(face(0.02, 0, y=y), face(0.02, 1, y=y), color=YELLOW, stroke_width=6)
    scene.add(line)
    scene.play(line.animate.shift(RIGHT * 5.45), run_time=seconds, rate_func=linear)
    scene.remove(line)


def contacts(center=ORIGIN, zoom=1, points=(*MANY, *FEW), rings=()):
    marks = VGroup()
    for n, xy in enumerate(points):
        position = center + zoom * point(*xy)
        if n in rings:
            shape = DashedVMobject(Circle(radius=0.109 * zoom, color=YELLOW, stroke_width=2.8),
                                  num_dashes=7, dashed_ratio=0.58)
            marks.add(shape.move_to(position))
        else:
            marks.add(VGroup(
                Dot(position, radius=0.132 * zoom, color=YELLOW, fill_opacity=0.22),
                Dot(position, radius=0.055 * zoom, color=YELLOW),
            ))
    return marks


FOCUS_CENTER = point(0, 0.48)
FOCUS_ZOOM = 1.53


def focus_tissue():
    # The tangential view behind the enlarged arbors, held during prediction.
    return Polygon(point(-5.59, -2.87), point(4.77, -2.87),
                   point(5.66, 2.46), point(-4.70, 2.46),
                   color=TEAL, stroke_width=2, fill_color="#28374A", fill_opacity=0.92)


def focus_cells():
    return circuit().scale(FOCUS_ZOOM, about_point=ORIGIN).shift(FOCUS_CENTER)


def contact_labels():
    return VGroup(T("many contacts", 34, YELLOW).move_to(point(-3.1, -3.37)),
                  T("few contacts", 34, YELLOW).move_to(point(3.1, -3.37)))


def predict_question():
    return question_card(ASK, size=40, y=3.26).shift(RIGHT * 0.5)


def direction_arrows(x=BLOCK_X):
    return VGroup(
        Arrow(point(x - 2.06, -1.86), point(x - 1.05, -1.86), buff=0, color=BAR, stroke_width=7),
        Arrow(point(x + 1.24, -1.79), point(x + 0.24, -1.81), buff=0, color=BAR, stroke_width=7),
    )


def light_sweep(scene, seconds=2.1, reverse=False, flashes=True):
    start, end = (0.39, -5.48) if reverse else (-5.48, 0.39)
    bar = RoundedRectangle(width=0.39, height=3.17, corner_radius=0.11, color=BAR,
                           fill_color=BAR, fill_opacity=0.83, stroke_width=4).move_to(point(start, -0.22))
    active_soma = point(BLOCK_X + (1.68 if reverse else -1.84), -1.80)
    glow = Circle(radius=0.29, color=BAR, fill_color=BAR, stroke_width=3).move_to(active_soma)
    glow.add_updater(lambda m: m.set_opacity(0.83 * np.exp(-((bar.get_x() - m.get_x()) / 0.82) ** 2)))
    scene.add(bar)
    if flashes:
        glow.update()
        scene.add(glow)
    scene.play(bar.animate.set_x(end), run_time=seconds, rate_func=linear)
    scene.remove(bar, glow)


class S01Hook(SpokenScene):
    def construct(self):
        block, depth, branches = volume()
        self.add(block, diagram_tag())
        self.at("how do you map")
        self.play(LaggedStart(*(Create(neuron) for neuron in branches), lag_ratio=0.18),
                  FadeIn(depth), run_time=3.5)
        full = VGroup(block, depth, branches)
        self.add(drift(full))
        self.at("in the inner retina")
        tissue = side_text("Mouse inner retina", y=1.54)
        self.play(FadeIn(tissue), run_time=0.65)
        self.at("amacrine cells tangle")
        amacrine = side_text("Amacrine cells", PURPLE, y=0.55)
        self.play(FadeIn(amacrine), run_time=0.64)
        self.at("ganglion cells")
        ganglion = side_text("Ganglion cells", BLUE, y=-0.43)
        self.play(FadeIn(ganglion), run_time=0.65)
        self.at("a single slice")
        full.clear_updaters()
        full.move_to(volume().get_center())
        plane = polygon(face_corners(y=-1.0), BLUE, BLUE, 0.23, 3)
        peeled = micrograph(0, 3.82, -0.48, 0.72)
        self.play(FadeOut(VGroup(amacrine, ganglion, tissue)), FadeIn(plane), run_time=0.45)
        self.play(plane.animate.shift(UP * 1.98), run_time=1.08)
        self.play(Transform(plane, peeled, replace_mobject_with_target_in_scene=True), run_time=1.15)
        self.at("where branches cross")
        flat = side_text("One flat slice", y=-1.14)
        self.play(FadeIn(flat), run_time=0.55)
        self.at("to trace who meets")
        self.play(FadeOut(flat), FadeOut(peeled, shift=point(-5.9, 1.38)), run_time=2.28)
        self.add(drift(full))
        self.finish()


class S02Title(TitleCard):
    LESSON = "Serial-section electron microscopy connectomics"
    TITLE = "Mapping Every Contact, Slice by Slice"

    def construct(self):
        block = volume()
        self.add(block, diagram_tag())
        lesson = fit_text(self.LESSON, 11.4, size=29, min_size=28, color=BLUE).move_to(point(0, -3.18))
        title = fit_text(self.TITLE, 12.0, size=46, min_size=38,
                         font=TITLE_FONT).move_to(point(0, 3.38))
        pivot = point(BLOCK_X, 0)
        center = RIGHT * 2.1
        self.play(block.animate.rotate(-0.08, about_point=pivot).shift(center),
                  FadeIn(title), FadeIn(lesson), run_time=0.46)
        self.wait(1.04)
        self.play(block.animate.shift(-center).rotate(0.08, about_point=pivot),
                  FadeOut(title), FadeOut(lesson), run_time=0.46)


class S03Slicing(SpokenScene):
    def construct(self):
        block, depth, branches = volume()
        self.add(block, depth, branches, diagram_tag())
        self.at("serial block face")
        title = head("Serial block-face electron microscopy")
        self.play(FadeIn(title), run_time=0.66)
        self.play(depth.animate.fade(0.60), branches.animate.fade(0.70), run_time=3.0)
        self.at("start with a small")
        name = side_text("Mouse retina", BLUE, y=0.10)
        self.play(swap(title, name), run_time=0.8)
        self.play(branches.animate.fade(0.60), block[2].animate.set_fill("#536D84"),
                  run_time=1.56)
        self.at("the microscope captures")
        self.play(FadeOut(name), run_time=0.35)
        scan(self, 0, 1.55)
        images = stack()
        image = images[0]
        self.play(TransformFromCopy(micrograph(0, BLOCK_X, TOP), image), run_time=1.24)
        self.at("then a thin slice")
        self.cut(block, 0, seconds=1.7)
        self.at("exposing a fresh face")
        scan(self, 1, 1.75)
        self.play(TransformFromCopy(micrograph(1, BLOCK_X, TOP - STEP), images[1]), run_time=0.92)
        self.at("repeating this cycle")
        for i in (2, 3):
            self.cut(block, i - 1, seconds=0.53)
            scan(self, i, 0.55)
            self.play(TransformFromCopy(micrograph(i, BLOCK_X, TOP - i * STEP), images[i]), run_time=0.60)
        self.finish()

    def cut(self, block, step, seconds):
        y = TOP - step * STEP
        a, b, c, d = face_corners(y=y)
        layer = VGroup(polygon([a, b, b + DOWN * STEP, a + DOWN * STEP], "#627991", BLUE),
                       polygon([b, c, c + DOWN * STEP, b + DOWN * STEP], "#71889E", BLUE),
                       polygon([a, b, c, d], "#586E86", BLUE))
        self.add(layer)
        self.play(Transform(block, retinal_block(cut=step + 1)),
                  FadeOut(layer, shift=point(1.4, 0.78)), run_time=seconds)


class S04Tracing(SpokenScene):
    def construct(self):
        block = retinal_block(cut=3)
        _, depth, branches = volume()
        image_stack = stack()
        self.add(block, depth.fade(0.60), branches.fade(0.88), image_stack, diagram_tag())
        self.at("those flat images")
        self.play(FadeOut(VGroup(block, depth, branches)),
                  image_stack.animate.shift(LEFT * 7.1), run_time=3.55)
        self.at("researchers trace each")
        spread = 0.13
        self.play(*(sheet.animate.shift(UP * i * spread) for i, sheet in enumerate(image_stack)),
                  run_time=1.08, rate_func=linear)
        layers = [list(profile_data(i)) for i in range(SLICES)]
        outlines = VGroup()
        for i, specs in enumerate(layers):
            x, y = stack_position(i, -3.35)
            y += i * spread
            spec = specs[4]
            outlines.add(profile(spec, x, y, 0.70, PURPLE, 0.4, 3.5).set_z_index(2))
        self.play(Succession(*(Create(outline) for outline in outlines)), run_time=3.28)
        manual = head("Manual tracing", PURPLE)
        self.at("manual tracing with")
        self.play(FadeIn(manual), run_time=0.53)
        self.at("machine learning segmentation", lead=0.52)
        segments = VGroup()
        for i, specs in enumerate(layers):
            x, y = stack_position(i, -3.35)
            y += i * spread
            for n, spec in enumerate(specs[:12]):
                if n != 4:
                    color = [BLUE, PURPLE, TEAL][n % 3]
                    segments.add(profile(spec, x, y, 0.70, color, 0.51, 2.2).set_z_index(2))
        auto = head("Machine-learning segmentation", BLUE)
        self.play(swap(manual, auto, run_time=0.67),
                  FadeIn(segments, lag_ratio=0.033, run_time=1.83))
        self.at("software that outlines")
        self.play(VGroup(image_stack, outlines, segments).animate.shift(LEFT * 0.65),
                  run_time=3.55, rate_func=linear)
        self.at("stacking those outlines")
        rebuilt = volume(x=2.50)
        self.play(FadeOut(auto), FadeIn(rebuilt[0], shift=RIGHT * 0.35),
                  FadeIn(rebuilt[1], shift=RIGHT * 0.55),
                  LaggedStart(*(Create(tree) for tree in rebuilt[2]), lag_ratio=0.22),
                  FadeOut(outlines, shift=RIGHT * 1.4), FadeOut(segments, shift=RIGHT * 1.4),
                  run_time=2.82)
        self.at("its arbor")
        arbor_label = head("Arbor", BLUE)
        self.play(FadeIn(arbor_label), run_time=0.55)
        self.at("where reconstructed membranes")
        marks = contacts(point(2.50, -0.25), 0.87)
        # Bring the meeting membranes forward before naming the contact.
        self.play(FadeOut(arbor_label), rebuilt.animate.shift(LEFT * 0.5),
                  run_time=1.42)
        marks.shift(LEFT * 0.5)
        self.play(LaggedStart(*(GrowFromCenter(m) for m in marks), lag_ratio=0.28), run_time=1.02)
        self.at("marks a contact")
        contact = head("Contact", YELLOW)
        self.play(FadeIn(contact), run_time=0.60)
        self.at("the reconstructed neurons")
        self.play(FadeOut(image_stack), FadeOut(contact),
                  VGroup(rebuilt, marks).animate.shift(LEFT * 2.25), run_time=2.2)
        self.at("form a connectome")
        self.play(FadeIn(head("Connectome")), run_time=0.66)
        self.finish()


def traced_volume():
    tissue = volume(x=-0.25)
    marks = contacts(point(-0.25, -0.25), 0.87)
    return tissue, marks


class S05Predict(SpokenScene):
    def construct(self):
        tissue, all_marks = traced_volume()
        self.add(tissue, all_marks, diagram_tag())
        connected = head("Connectome")
        self.add(connected)
        self.at("pause and look at")
        glass = focus_tissue()
        focus = focus_cells()
        self.play(FadeOut(connected), ReplacementTransform(tissue[0], glass), FadeOut(tissue[1]), FadeOut(all_marks),
                  ReplacementTransform(tissue[2], focus), run_time=4.05)
        labels = contact_labels()
        marks = contacts(FOCUS_CENTER, FOCUS_ZOOM)
        self.at("one partner gets")
        self.play(LaggedStart(*(GrowFromCenter(m) for m in marks[:6]), lag_ratio=0.20), run_time=1.24)
        self.play(FadeIn(labels[0]), run_time=0.53)
        self.at("while the neighbor")
        self.play(LaggedStart(*(GrowFromCenter(m) for m in marks[6:]), lag_ratio=0.25), run_time=1.14)
        self.play(FadeIn(labels[1]), run_time=0.52)
        self.at("does a larger count")
        detail = VGroup(glass, focus, *marks)
        self.play(FadeIn(predict_question()), detail.animate.scale(0.91, about_point=ORIGIN),
                  run_time=2.53)
        self.at("or even prove")
        # Close in on the appositions as the question shifts to individual contacts.
        self.play(detail.animate.scale(1 / 0.91, about_point=ORIGIN), run_time=3.66, rate_func=linear)
        self.finish()


class S06Pause(Scene):
    def construct(self):
        self.camera.background_color = BG
        self.add(focus_tissue(), focus_cells(), contacts(FOCUS_CENTER, FOCUS_ZOOM), contact_labels(),
                 predict_question(), diagram_tag())
        self.wait(float(os.environ["KX_DURATION"]))


def unknown_gauge(title, center):
    # A scale without a needle leaves the unmeasured value unknown.
    track = Arc(radius=0.89, start_angle=0, angle=PI, arc_center=center,
                color=GREY, stroke_width=8, stroke_opacity=0.65)
    symbol = T("?", 50, TEXT).move_to(center + UP * 0.28)
    label = T(title, 32).move_to(center + DOWN * 0.65)
    return VGroup(track, symbol, label)


class S07Limits(SpokenScene):
    def construct(self):
        trees = focus_cells()
        solid = contacts(FOCUS_CENTER, FOCUS_ZOOM)
        question = predict_question()
        labels = contact_labels()
        glass = focus_tissue()
        self.add(glass, trees, solid, labels, question, diagram_tag())
        self.at("now", lead=0)
        self.play(FadeOut(question), FadeOut(labels), FadeOut(glass), run_time=0.63)
        self.at("serial slices reconstruct")
        self.play(VGroup(trees, solid).animate.shift(UP * 0.36), run_time=2.75)
        self.at("yet a contact alone")
        hollow = contacts(FOCUS_CENTER + UP * 0.36, FOCUS_ZOOM, rings=(0, 2, 3, 5, 7))
        self.play(LaggedStart(*(Transform(a, b) for a, b in zip(solid, hollow)), lag_ratio=0.10),
                  run_time=2.04)
        limit = head("Contact ≠ proven synapse", YELLOW)
        model = VGroup(trees, solid)
        self.play(FadeIn(limit), model.animate.shift(DOWN * 0.36), run_time=1.75)
        self.at("packed branches can touch")
        self.play(model.animate.scale(1.12).shift(point(-0.30, -0.06)), run_time=2.72)
        self.at("contact map proposes")
        self.play(model.animate.scale(0.60).move_to(point(-3.58, -0.19)), run_time=3.93)
        self.at("also counts synapses")
        tally = Ledger([("Synapse count", "|||", YELLOW)], top_left=(0.18, 1.0),
                       width=5.9, key_w=3.20, size=34)
        self.play(FadeOut(limit), tally.reveal(0), run_time=0.75)
        strength = unknown_gauge("Strength", point(1.45, -0.82))
        sign = unknown_gauge("Sign", point(4.72, -0.82))
        self.at("without measuring strength")
        self.play(FadeIn(strength, shift=UP * 0.28), run_time=1.02)
        self.at("meaning excitation or inhibition")
        self.play(FadeIn(sign, shift=UP * 0.28), run_time=0.9)
        kinds = T("Excite / inhibit", 28).move_to(point(4.72, -2.02))
        self.play(FadeIn(kinds), run_time=0.57)
        self.at("treating count as strength")
        contact_field = focus_tissue().scale(0.59).move_to(model)
        contact_field.set_z_index(-1)
        self.play(FadeIn(caption("Count as strength is an assumption", color=YELLOW)),
                  FadeIn(contact_field), run_time=1.18)
        self.play(contact_field.animate.set_fill(opacity=0.62), run_time=1.44)
        self.finish()


class S08Controls(SpokenScene):
    def construct(self):
        tissue = volume()
        arrows = direction_arrows()
        self.add(tissue, diagram_tag())
        self.at("wiring diagram alone")
        self.play(tissue[2].animate.fade(0.56), tissue[1].animate.fade(0.45), run_time=3.05)
        self.at("to guard against")
        self.play(Transform(tissue[2], volume()[2]), tissue[0][2].animate.set_fill(opacity=0.56), run_time=2.10)
        functional = side_text("Read function first", BAR, y=1.06)
        self.at("read function first")
        self.play(FadeIn(functional), run_time=0.64)
        self.at("they image calcium")
        calcium = side_text("Calcium imaging", BAR, y=0.08)
        self.play(FadeIn(calcium), run_time=0.51)
        light_sweep(self, seconds=1.81)
        self.at("using moving bars")
        light_sweep(self, seconds=1.51)
        self.play(GrowArrow(arrows[0]), run_time=0.47)
        light_sweep(self, seconds=1.44, reverse=True)
        self.play(GrowArrow(arrows[1]), run_time=0.49)
        self.at("then they cut")
        slices = stack()
        self.play(FadeOut(functional), FadeOut(calcium), run_time=0.34)
        self.play(Transform(tissue[0], retinal_block(cut=3)),
                  LaggedStart(*(FadeIn(m, shift=RIGHT * 1.4) for m in slices), lag_ratio=0.21),
                  run_time=1.65)
        self.play(Transform(tissue[0], retinal_block()), FadeOut(slices, shift=LEFT * 1.4),
                  Transform(tissue[1], volume()[1]), run_time=1.45)
        self.at("anatomy only observes")
        note = side_text("Observational", y=0.55)
        self.play(FadeIn(note), run_time=0.58)
        self.at("proving a pathway")
        summary = side_text("Observational:\nNeed takes\nmanipulation", x=4.22, y=0.52)
        # Block the left amacrine pathway before showing its paired readout drop.
        site = point(BLOCK_X, -0.25) + 0.87 * point(*LEFT_RUN[0])
        block_mark = VGroup(*(Line(site - offset, site + offset, color=RED, stroke_width=7)
                              for offset in (point(0.20, 0.20), point(0.20, -0.20))))
        left_response = arrows[0]
        self.play(swap(note, summary, run_time=0.97),
                  Succession(Create(block_mark, run_time=0.65),
                             left_response.animate(run_time=1.25)
                             .scale(0.46, about_point=left_response.get_start()).set_opacity(0.60)))
        self.finish()


class S09UnlockedA(SpokenScene):
    def construct(self):
        tissue = volume()
        arrows = direction_arrows()
        self.add(tissue, arrows, diagram_tag())
        self.at("this approach unlocked")
        self.play(tissue[1].animate.fade(0.58), tissue[2][0].animate.fade(0.72),
                  tissue[2][2].animate.fade(0.68), FadeOut(arrows[1]), run_time=2.45)
        first = head("Briggman, Helmstaedter & Denk", GOLD)
        self.at("bregman")
        self.play(FadeIn(first), run_time=0.62)
        self.at("imaged calcium using")
        light_sweep(self, seconds=4.66)
        self.at("they then cut")
        exposed = micrograph(0, 3.78, 0.25, 0.73)
        self.play(TransformFromCopy(micrograph(0, BLOCK_X, TOP), exposed), run_time=1.6)
        self.at("direction selective ganglion")
        marks = contacts(point(BLOCK_X, -0.25), 0.87, points=(MANY[2], MANY[4]))
        self.play(LaggedStart(*(GrowFromCenter(m) for m in marks), lag_ratio=0.42),
                  FadeOut(exposed, shift=LEFT * 1.65), run_time=2.35)
        self.at("in 2013")
        second = head("Helmstaedter and colleagues, 2013", GOLD)
        self.play(FadeOut(arrows[0]), FadeOut(marks), FadeOut(first), run_time=0.48)
        wider = volume(x=-0.25, dense=True)
        self.play(Transform(tissue[0], wider[0]), Transform(tissue[2], wider[2]), FadeOut(tissue[1]),
                  FadeIn(second), run_time=2.03)
        self.at("paired manual tracing")
        growth = wider[1]
        self.play(LaggedStart(*(Create(cell) for cell in growth), lag_ratio=0.24), run_time=3.53)
        self.at("they reconstructed", lead=0.35)
        number = ValueTracker(0)
        tally = counter("{:.0f} neurons", number, point(0, -3.23), size=34, color=YELLOW)
        self.add(tally)
        self.play(number.animate.set_value(950), tissue[0][2].animate(rate_func=there_and_back).set_fill(opacity=0.5),
                  run_time=0.9)
        tally.update(0)
        tally.clear_updaters()
        self.at("mutual contacts")
        more = contacts(point(-0.25, -0.25), 0.87)
        self.play(LaggedStart(*(GrowFromCenter(m) for m in more), lag_ratio=0.28),
                  tissue[0][2].animate(rate_func=there_and_back).set_fill(opacity=0.56),
                  run_time=2.75)
        self.finish()


def light_response(t, onset, amplitude):
    # Bae et al. (2018), equation 5. Illustrative parameters in arbitrary
    # units, so the curves are labelled schematic and carry no data ticks.
    gap = max(0, t - onset)
    return amplitude * (np.exp(-gap / 1.22) - np.exp(-gap / 0.24))


class S10UnlockedB(SpokenScene):
    def construct(self):
        wide = volume(x=-0.25, dense=True)
        marks = contacts(point(-0.25, -0.25), 0.87)
        self.add(wide, marks, diagram_tag())
        self.at("in 2018")
        title = head("Bae and colleagues, 2018", GOLD)
        self.play(FadeIn(title), run_time=0.65)
        self.at("used electron microscopy")
        scene_volume = volume()
        self.play(Transform(wide, scene_volume), FadeOut(marks), run_time=2.25)
        self.at("whose light responses")
        light_sweep(self, seconds=3.14)
        self.at("grouping cells by arbor shape")
        panels = TwoPanel("Arbor shape and depth", "Light responses", colors=(BLUE, GREEN),
                          width=12.4, top=2.76, bottom=-2.54)
        forms = VGroup()
        for i, (x, y) in enumerate([(-4.45, 0.69), (-3.60, -0.13), (-2.55, -0.97)]):
            cell = circuit()[1 + i % 2].scale(0.37 + 0.06 * i).move_to(point(x, y))
            forms.add(cell)
        panels.put(forms, "left")
        traces = VGroup()
        for row, amplitude in enumerate((1.0, 0.63, 0.90)):
            y = -1.27 + row * 0.94
            plot = Plot(box=(1.00, 5.69, y, y + 0.78), xr=(0, 6), yr=(0, 0.95), color=GREY, stroke=1.8)
            traces.add(VGroup(plot, plot.curve(lambda t, a=amplitude, r=row:
                                               light_response(t, 0.65 + r * 0.17, a)
                                               + light_response(t, 3.30, a * (0.36 + r * 0.23)),
                                               color=GREEN, width=4.6)))
        self.play(FadeOut(wide), run_time=0.50)
        self.play(FadeIn(panels),
                  LaggedStart(*(FadeIn(c, shift=LEFT * 1.2) for c in forms), lag_ratio=0.21),
                  LaggedStart(*(Create(t) for t in traces), lag_ratio=0.22), run_time=2.53)
        self.at("47 anatomical clusters")
        clusters = T("47 clusters", 35, YELLOW).move_to(point(-3.12, -2.93))
        depth_planes = VGroup()
        for arbor_shape in forms:
            center = arbor_shape.get_center() + DOWN * 0.14
            depth_planes.add(polygon([center + point(-1.18, -0.22), center + point(0.86, -0.22),
                                      center + point(1.18, 0.22), center + point(-0.86, 0.22)],
                                     "#344F62", BLUE, 0.76))
        forms.set_z_index(1)
        self.play(FadeIn(clusters), LaggedStart(*(FadeIn(plane, shift=UP * 0.31)
                                                 for plane in depth_planes), lag_ratio=0.48),
                  run_time=2.33)
        self.at("at least 35 types")
        types = T("At least 35 types", 35, YELLOW).move_to(point(2.15, -2.93))
        self.play(FadeIn(types), run_time=0.64)
        self.at("a stack of slices")
        slices = stack()
        returned = volume()
        self.play(FadeOut(VGroup(panels, traces, title, clusters, types, depth_planes)), run_time=0.60)
        self.play(FadeIn(returned[0]), FadeIn(slices),
                  FadeOut(forms, shift=RIGHT * 0.50),
                  FadeIn(returned[1]), FadeIn(returned[2]), run_time=1.72)
        self.at("while activity and manipulations")
        self.play(FadeOut(slices, shift=LEFT * 2.4), run_time=0.52)
        light_sweep(self, seconds=1.7)
        self.play(GrowArrow(direction_arrows()[0]), run_time=0.48)
        self.finish()


class S11End(EndCard):
    LINE = END_LINE
