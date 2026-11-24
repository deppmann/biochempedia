"""Genetic mosaics, timed to the supplied Kokoro word alignment.

TEAL: normal cells and epidermis. MAGENTA: marked mutant lineage.
ORANGE: the globally disrupted tissue in the hook. GOLD: neural fate and credits.
YELLOW: Delta signal and directional changes. PURPLE: Notch receptor.
BLUE: transient EdU mark. GREY: unlabelled structures.
"""

from bp_parts import *
from bp_style import EndCard


MAGENTA = "#EF82D0"
ORANGE = "#F29E4C"
PURPLE = "#B58CD9"
ASK = "Patch lacks Delta: does it turn neural?"
SHEET_CENTER = np.array([0.0, 0.25, 0.0])
RADIUS = 0.73
CLONE_STEPS = (
    ((4, 2),),
    ((4, 2), (5, 2)),
    ((4, 2), (5, 2), (4, 1), (4, 3)),
    ((4, 2), (5, 2), (4, 1), (4, 3), (3, 2), (3, 1), (3, 3), (5, 1)),
    ((4, 2), (5, 2), (4, 1), (4, 3), (3, 2), (3, 1), (3, 3), (5, 1),
     (5, 3), (6, 1), (6, 2), (6, 3), (2, 1), (2, 2), (2, 3), (1, 2)),
)
CLONE = frozenset(CLONE_STEPS[-1])
CONTACT_CELLS = frozenset((col, row) for col in (3, 4) for row in (1, 2, 3))
CONTACT_ZOOM = 1.55


def xy(x, y):
    return np.array([x, y, 0.0])


def cell(center, radius=RADIUS, color=TEAL, fill=0.49):
    return RegularPolygon(
        n=6, radius=radius * 0.965, start_angle=PI / 2,
        stroke_color=color, stroke_width=2.1, fill_color=color, fill_opacity=fill,
    ).move_to(center)


def light_wave(shapes, amplitude=0.11):
    """Keep the schematic tissue alive with a slow sweep across its existing fills."""
    def update_fill(shape, dt):
        opacity = shape.get_fill_opacity()
        if not np.isclose(opacity, shape.wave_previous, atol=1e-5):
            # A tint or fate animation has supplied a new resting fill.
            shape.wave_base = opacity
        shape.wave_time += dt
        phase = shape.wave_time * 1.30 - shape.wave_offset
        variation = amplitude * min(1.0, shape.wave_base / 0.42)
        shape.wave_previous = np.clip(shape.wave_base + variation * np.sin(phase), 0, 1)
        shape.set_fill(opacity=shape.wave_previous, family=False)

    for shape in shapes:
        x, y, _ = shape.get_center()
        shape.wave_time = 0.0
        shape.wave_offset = x * 0.72 + y * 0.38
        shape.wave_base = shape.wave_previous = shape.get_fill_opacity()
        shape.add_updater(update_fill)


def sheet(marks=(), mark_color=MAGENTA, base=TEAL, cols=9, rows=5,
          radius=RADIUS, center=SHEET_CENTER, moving=True):
    """Build the epithelium at the same coordinates whenever a scene carries it over."""
    step = np.sqrt(3) * radius
    tiles = {}
    marks = set(marks)
    for row in range(rows):
        for col in range(cols):
            key = (col, row)
            x = (col - (cols - 1) / 2 + 0.5 * (row % 2) - 0.25) * step
            y = (row - (rows - 1) / 2) * 1.5 * radius
            tiles[key] = cell(center + xy(x, y), radius, mark_color if key in marks else base)
    if moving:
        light_wave(tiles.values())
    return VGroup(*tiles.values()), tiles


def tint(tile, color, fill=0.49):
    return tile.animate.set_fill(color, opacity=fill).set_stroke(color)


def paint(tiles, keys, color, fill=0.49):
    return AnimationGroup(*(tint(tiles[key], color, fill) for key in keys), lag_ratio=0)


def seam(tiles, marks, color=TEXT, width=4.5):
    """The common edges with normal cells, excluding the outside of the sheet."""
    edges = VGroup()
    distance = RADIUS * np.sqrt(3)
    for key in sorted(marks):
        a = tiles[key].get_center()
        for other, tile in tiles.items():
            if other in marks:
                continue
            v = tile.get_center() - a
            if not np.isclose(np.linalg.norm(v), distance):
                continue
            mid = a + v / 2
            tangent = rotate_vector(v / distance, PI / 2)
            edges.add(DashedLine(mid - RADIUS * tangent / 2, mid + RADIUS * tangent / 2,
                                 dash_length=0.15, dashed_ratio=0.66,
                                 color=color, stroke_width=width))
    return edges


def title_label(text, color=TEXT, x=0):
    return T(text, 32, color).move_to(xy(x, 3.50))


def bottom_label(text, color=TEXT, x=0):
    return T(text, 32, color).move_to(xy(x, -3.36))


def pointer(start, end, color=YELLOW, width=5):
    return Arrow(start, end, buff=0, color=color, stroke_width=width, tip_length=0.15,
                 max_stroke_width_to_length_ratio=12)


def ring_at(point, radius=0.41, color=TEXT, width=4):
    return Circle(radius=radius, stroke_color=color, stroke_width=width).move_to(point)


def traveling_rings(points, color, run_time=2.0):
    """Local highlighting expands from the cells involved in the current beat."""
    rings = [ring_at(point, radius=0.12, color=color, width=4) for point in points]
    waves = [Succession(
        FadeIn(ring, run_time=0.16),
        AnimationGroup(ring.animate.scale(3.8).set_stroke(opacity=0.40), run_time=0.64),
        FadeOut(ring, run_time=0.25),
    ) for ring in rings]
    return LaggedStart(*waves, lag_ratio=0.38, run_time=run_time)


def split_cells(scene, tiles, stages, color, total, fills=None, shades=None):
    """Give the staged daughter cells a shared colour from the previous generation."""
    per_stage = total / len(stages)
    for index, stage in enumerate(stages):
        fill = fills[index] if fills else 0.58
        shade = shades[index] if shades else color
        scene.play(
            paint(tiles, stage, shade, fill),
            traveling_rings([tiles[key].get_center() for key in stage[-4:]], color),
            run_time=per_stage,
        )


class S01Hook(SpokenScene):
    def construct(self):
        world, tiles = sheet()
        arrows = VGroup(*[
            pointer(tile.get_center() + LEFT * 0.16, tile.get_center() + RIGHT * 0.30, TEXT, 3)
            for tile in tiles.values()
        ])
        self.add(world, arrows)
        self.at("when a broken gene")
        self.play(traveling_rings([tiles[key].get_center() for key in ((3, 2), (4, 2), (5, 2))], TEAL),
                  run_time=1.0)
        self.at("scrambles a tissue")
        turns = [0.85, -1.9, 2.25, -0.75, 1.6, -2.7, 0.42]
        self.play(
            paint(tiles, tiles, ORANGE, 0.56),
            AnimationGroup(*(Rotate(arrow, turns[(i * 3 + i // 9) % len(turns)])
                             for i, arrow in enumerate(arrows))),
            run_time=1.20,
        )
        self.at("which cells actually")
        question = question_card("Which cells actually need the gene?", y=-3.32, size=35)
        self.play(FadeIn(question), run_time=0.42)
        focus = ring_at(tiles[4, 2].get_center(), 0.48)
        self.at("did each cell")
        self.play(Create(focus), run_time=0.9)
        self.at("because its neighbors")
        self.play(focus.animate.move_to(tiles[5, 2]), run_time=0.7)
        self.play(focus.animate.move_to(tiles[4, 3]), run_time=0.7)
        self.at("if every cell")
        self.play(FadeOut(focus), traveling_rings(
            [tiles[key].get_center() for key in ((2, 2), (3, 1), (4, 3), (5, 2), (6, 1))],
            ORANGE, run_time=3.5), run_time=3.5)
        self.at("to separate them")
        self.play(FadeOut(question), run_time=0.46)
        self.at("place mutant cells")
        normal = [key for key in tiles if key[0] >= 5]
        self.play(
            LaggedStart(*(tint(tiles[key], TEAL) for key in normal), lag_ratio=0.065),
            FadeOut(arrows), run_time=2.45,
        )
        self.finish()


class S02Title(TitleCard):
    TITLE = "Testing a Gene One Patch at a Time"
    LESSON = "Genetic Mosaics"

    def construct(self):
        world, _ = sheet(((col, row) for col in range(5) for row in range(5)), ORANGE,
                         moving=False)
        world.set_fill(opacity=0.09).set_stroke(opacity=0.22)
        self.add(world)
        title = fit_text(self.TITLE, max_w=11.8, size=53, min_size=36, font=TITLE_FONT)
        lesson = T(self.LESSON, 30, TEAL)
        rule = Line(LEFT * 0.75, RIGHT * 0.75, color=GOLD, stroke_width=4)
        lockup = VGroup(lesson, title, rule).arrange(DOWN, buff=0.32)
        card = SurroundingRectangle(lockup, buff=0.42, corner_radius=0.19,
                                   color=GREY, stroke_opacity=0.60,
                                   fill_color=BG, fill_opacity=1)
        self.play(FadeIn(card), FadeIn(lockup), world.animate.shift(UP * 0.06), run_time=0.38)
        self.play(world.animate.shift(DOWN * 0.12), run_time=1.23)
        self.play(FadeOut(lockup), FadeOut(card), run_time=0.33)


class S03Clone(SpokenScene):
    def construct(self):
        half = [(col, row) for col in range(5) for row in range(5)]
        world, tiles = sheet(half, ORANGE)
        self.add(world)
        self.at("genetic mosaic analysis")
        self.play(LaggedStart(*(tint(tiles[key], MAGENTA) for key in half), lag_ratio=0.065),
                  run_time=2.3)
        self.at("two genetic kinds")
        self.play(traveling_rings([tiles[key].get_center() for key in ((3, 2), (6, 2))], TEXT),
                  run_time=1.32)
        self.at("inside an otherwise normal")
        self.play(LaggedStart(*(tint(tiles[key], TEAL) for key in reversed(half)), lag_ratio=0.05),
                  run_time=1.4)
        self.at("you mutate one cell")
        seed = CLONE_STEPS[0][0]
        self.play(tint(tiles[seed], MAGENTA, 0.68),
                  traveling_rings([tiles[seed].get_center()], MAGENTA), run_time=1.45)
        self.at("permanently mark it")
        self.play(Indicate(tiles[seed], color=MAGENTA, scale_factor=1.10), run_time=0.9)
        self.at("every descendant inherits")
        split_cells(self, tiles, CLONE_STEPS[1:3], MAGENTA, total=2.2)
        self.at("forming a clone")
        split_cells(self, tiles, CLONE_STEPS[3:], MAGENTA, total=2.42,
                    fills=(0.56, 0.49))
        self.at("amid normal cells")
        names = VGroup(bottom_label("Mutant clone (schematic)", MAGENTA, -3.15),
                       bottom_label("Normal neighbours", TEAL, 3.30))
        self.play(FadeIn(names), run_time=0.62)
        self.finish()


class S04Border(SpokenScene):
    def construct(self):
        world, tiles = sheet(CLONE)
        names = VGroup(bottom_label("Mutant clone (schematic)", MAGENTA, -3.15),
                       bottom_label("Normal neighbours", TEAL, 3.30))
        self.add(world, names)
        self.at("watch the border")
        self.play(FadeOut(names), run_time=0.34)
        # Enlarge the central section while keeping the original border in view.
        outer = [tile for key, tile in tiles.items() if key[0] in (0, 8)]
        self.play(FadeOut(VGroup(*outer)), run_time=0.27)
        inner = VGroup(*(tile for key, tile in tiles.items() if key[0] not in (0, 8)))
        self.remove(world)
        self.add(inner)
        border = seam(tiles, CLONE)
        zoom_origin = xy(0, 0.25)
        self.play(inner.animate.scale(1.15, about_point=zoom_origin), run_time=0.9)
        border.scale(1.15, about_point=zoom_origin)
        self.play(Create(border), run_time=1.38)
        self.at("acts inside the cell")
        inside = bottom_label("Inside the cell", MAGENTA)
        core = [(3, 2), (4, 2), (5, 2), (4, 1), (4, 3)]
        self.play(traveling_rings([tiles[key].get_center() for key in core], MAGENTA),
                  FadeIn(inside), run_time=1.25)
        self.at("only the patch changes")
        self.play(paint(tiles, core, MAGENTA, 0.76), run_time=1.17)
        self.at("signals between cells")
        between = bottom_label("Between cells", YELLOW)
        self.play(swap(inside, between, run_time=0.7), paint(tiles, core, MAGENTA), run_time=0.7)
        contacts = [((6, row), (7, row)) for row in (1, 2, 3)]
        arrows = [pointer(tiles[a].get_center(), tiles[b].get_center()) for a, b in contacts]
        self.play(LaggedStart(*(GrowArrow(arrow) for arrow in arrows), lag_ratio=0.20), run_time=1.05)
        self.at("normal neighbors can change")
        self.play(paint(tiles, [b for _, b in contacts], TEAL, 0.83),
                  traveling_rings([tiles[b].get_center() for _, b in contacts], TEAL),
                  run_time=1.55)
        self.at("or supply what")
        self.play(
            *(Transform(arrow, pointer(tiles[b].get_center(), tiles[a].get_center()))
              for arrow, (a, b) in zip(arrows, contacts)),
            paint(tiles, [b for _, b in contacts], TEAL), run_time=0.76,
        )
        self.play(traveling_rings([tiles[a].get_center() for a, _ in contacts], YELLOW),
                  run_time=1.0)
        self.finish()


def peg(point, direction, extension=0):
    """A cartoon signal projecting from its cell wall."""
    return VGroup(Line(point - direction * 0.20, point + direction * (0.06 + extension),
                       color=YELLOW, stroke_width=6),
                  Dot(point + direction * (0.065 + extension), radius=0.068, color=YELLOW))


def cup(point, direction):
    """A cartoon receptor, open towards the adjoining cell."""
    tangent = rotate_vector(direction, PI / 2)
    rim, back = point - direction * 0.04, point - direction * 0.22
    return VMobject(color=PURPLE, stroke_width=6).set_points_as_corners(
        [rim + tangent * 0.115, back + tangent * 0.115,
         back - tangent * 0.115, rim - tangent * 0.115]
    )


def contact_tiles(tiles):
    return {key: tile for key, tile in tiles.items()
            if 1 <= key[0] <= 5 and 1 <= key[1] <= 3}


def zoom_contact(world, center):
    return world.scale(CONTACT_ZOOM, about_point=center).shift(SHEET_CENTER - center)


def contact_parts(tiles, docked=False):
    incoming, receptors, outgoing = VGroup(), VGroup(), VGroup()
    spacing = tiles[3, 2].get_x() - tiles[2, 2].get_x()
    magnification = spacing / (RADIUS * np.sqrt(3))
    extension = 0.34 if docked else 0
    for row in (1, 2, 3):
        left, mid, right = (tiles[col, row].get_center() for col in (2, 3, 4))
        boundary = (left + mid) / 2
        incoming.add(peg(boundary + LEFT * 0.12, RIGHT, extension).scale(
            magnification, about_point=boundary))
        receptors.add(cup(boundary + RIGHT * 0.19, LEFT
                          ).scale(magnification, about_point=boundary))
        other_border = (mid + right) / 2
        outgoing.add(peg(other_border + LEFT * 0.10, RIGHT
                         ).scale(magnification, about_point=other_border))
    return incoming, receptors, outgoing


def predict_world(moving=True, docked=False):
    _, tiles = sheet(CONTACT_CELLS, moving=moving)
    tiles = contact_tiles(tiles)
    world = zoom_contact(VGroup(*tiles.values()), tiles[3, 2].get_center())
    incoming, receptors, _ = contact_parts(tiles, docked=docked)
    return world, tiles, incoming, receptors


def predict_card():
    return question_card(ASK, y=-3.32, size=35)


class S05PredictQ(SpokenScene):
    def construct(self):
        world, tiles = sheet(CONTACT_CELLS)
        self.add(world)
        self.at("touching cells talk")
        self.play(traveling_rings([tiles[key].get_center() for key in ((2, 2), (3, 2), (4, 2))],
                                  TEAL, run_time=2.2), run_time=2.2)
        neural_sample, epidermis_sample = (tiles[key] for key in ((2, 2), (6, 2)))
        neural = bottom_label("Neural", GOLD, -2.78)
        skin = bottom_label("Epidermis (outer skin)", TEAL, 2.68)
        self.at("each becomes", lead=0.16)
        self.play(tint(neural_sample, GOLD, 0.74), FadeIn(neural), run_time=0.7)
        self.at("epidermis the outer")
        self.play(epidermis_sample.animate.stretch(0.68, 1).set_fill(TEAL, 0.77),
                  FadeIn(skin), run_time=0.73)
        self.at("the outer skin", lead=-0.42)
        self.play(tint(neural_sample, TEAL), epidermis_sample.animate.stretch(1 / 0.68, 1).set_fill(TEAL, 0.49),
                  FadeOut(neural), FadeOut(skin), run_time=0.54)
        center = tiles[3, 2].get_center()
        close_tiles = contact_tiles(tiles)
        periphery = VGroup(*(tile for key, tile in tiles.items() if key not in close_tiles))
        closeup = VGroup(*close_tiles.values())
        self.remove(world)
        self.add(periphery, closeup)
        self.play(FadeOut(periphery),
                  closeup.animate.scale(CONTACT_ZOOM, about_point=center).shift(SHEET_CENTER - center),
                  run_time=0.75)
        incoming, receptors, outgoing = contact_parts(close_tiles)
        self.at("delta is the signal", lead=0.1)
        delta = title_label("Delta: signal", YELLOW, -2.9)
        self.play(LaggedStart(*(GrowFromCenter(p) for p in (*incoming, *outgoing)), lag_ratio=0.16),
                  run_time=0.76)
        self.play(FadeIn(delta), run_time=0.36)
        self.at("do not turn neural")
        self.play(LaggedStart(*(Indicate(p, color=YELLOW, scale_factor=1.25)
                               for p in incoming), lag_ratio=0.35), run_time=1.55)
        self.at("notch is the receptor")
        notch = title_label("Notch: receptor", PURPLE, 2.9)
        self.play(LaggedStart(*(Create(c) for c in receptors), lag_ratio=0.24), run_time=0.88)
        self.play(FadeIn(notch), run_time=0.38)
        self.at("patches lacking notch")
        missing = bottom_label("Patch lacks Notch", MAGENTA)
        self.play(FadeOut(receptors), FadeIn(missing), run_time=0.52)
        self.play(LaggedStart(*(p.animate(rate_func=there_and_back).shift(RIGHT * (0.19 * CONTACT_ZOOM))
                              for p in incoming), lag_ratio=0.12), run_time=0.86)
        self.at("so they turn neural")
        result = bottom_label("Neural", GOLD)
        self.play(paint(tiles, sorted(CONTACT_CELLS), GOLD, 0.76),
                  swap(missing, result, run_time=0.7), run_time=0.8)
        self.at("predict")
        self.play(
            paint(tiles, sorted(CONTACT_CELLS), MAGENTA), FadeIn(receptors),
            FadeOut(outgoing), FadeOut(result), FadeOut(delta), FadeOut(notch),
            run_time=0.70,
        )
        self.play(FadeIn(predict_card()), run_time=0.5)
        self.finish()


class S06PredictPause(Scene):
    def construct(self):
        self.camera.background_color = BG
        world, _, incoming, receptors = predict_world(moving=False)
        self.add(world, incoming, receptors, predict_card())
        self.wait(float(os.environ.get("KX_DURATION", 4.5)))


class S07PredictA(SpokenScene):
    def construct(self):
        world, tiles, incoming, receptors = predict_world()
        question = predict_card()
        self.add(world, incoming, receptors, question)
        self.at("patches lacking delta")
        self.play(FadeOut(question), run_time=0.38)
        docked, _, _ = contact_parts(tiles, docked=True)
        self.play(LaggedStart(*(Transform(source, target) for source, target in zip(incoming, docked)),
                              lag_ratio=0.23), run_time=1.1)
        no_neural = bottom_label("No neural fate on its own", TEAL)
        self.at("do not turn neural")
        self.play(FadeIn(no_neural),
                  traveling_rings([tiles[3, row].get_center() for row in (1, 2, 3)], PURPLE),
                  run_time=1.55)
        self.at("losing delta removes")
        _, _, ghost = contact_parts(tiles)
        for p in ghost:
            p.set_color(GREY).set_opacity(0.65)
        send = title_label("Sending: lost", YELLOW, -2.9)
        self.play(FadeOut(no_neural), FadeIn(send), run_time=0.45)
        self.play(LaggedStart(*(FadeIn(p, shift=RIGHT * 0.12) for p in ghost), lag_ratio=0.25),
                  run_time=0.77)
        self.play(LaggedStart(*(FadeOut(p, shift=LEFT * 0.18) for p in ghost), lag_ratio=0.32),
                  run_time=1.38)
        self.at("not what it hears")
        self.play(LaggedStart(*(Indicate(c, color=PURPLE, scale_factor=1.20) for c in receptors),
                               lag_ratio=0.30), run_time=1.45)
        self.at("they still have notch")
        hear = title_label("Hearing: intact", PURPLE, 2.9)
        self.play(FadeIn(hear), run_time=0.65)
        self.at("normal neighbors")
        self.play(traveling_rings([tiles[2, row].get_center() for row in (1, 2, 3)], YELLOW),
                  run_time=1.65)
        self.at("tells them not you")
        reply = bottom_label("Not you", PURPLE)
        self.play(FadeIn(reply), traveling_rings(
            [tiles[key].get_center() for key in ((3, 1), (3, 2), (3, 3), (4, 2))], PURPLE),
            run_time=1.9)
        self.at("separates sending a signal")
        self.play(FadeOut(reply), LaggedStart(
            *(Indicate(c, color=PURPLE, scale_factor=1.18) for c in receptors), lag_ratio=0.35),
            run_time=1.9)
        self.finish()


class S08Controls(SpokenScene):
    def construct(self):
        closeup, close_tiles, incoming, receptors = predict_world(docked=True)
        self.add(closeup, incoming, receptors)
        self.at("two traps")
        world, tiles = sheet()
        context = VGroup(*(tile for key, tile in tiles.items() if key not in close_tiles))
        center = tiles[3, 2].get_center()
        self.play(FadeOut(incoming), FadeOut(receptors),
                  paint(close_tiles, sorted(CONTACT_CELLS), TEAL), run_time=0.63)
        self.play(
            closeup.animate.scale(1 / CONTACT_ZOOM, about_point=SHEET_CENTER).shift(center - SHEET_CENTER),
            FadeIn(context), run_time=0.84,
        )
        self.remove(context, closeup)
        self.add(world)
        seed = CLONE_STEPS[0][0]
        self.at("pulse labels like edu")
        edu = bottom_label("EdU", BLUE)
        pulse_blue = interpolate_color(ManimColor(BLUE), ManimColor(TEXT), 0.36)
        self.play(tint(tiles[seed], pulse_blue, 0.82),
                  traveling_rings([tiles[seed].get_center()], BLUE), run_time=0.68)
        self.play(FadeIn(edu), run_time=0.33)
        self.at("dilute as cells divide")
        diluted = [interpolate_color(ManimColor(TEAL), pulse_blue, fraction)
                   for fraction in (0.60, 0.30, 0.10)]
        split_cells(self, tiles, CLONE_STEPS[1:4], BLUE, total=1.72,
                    fills=(0.63, 0.54, 0.49), shades=diluted)
        self.at("marks must be permanent")
        permanent = bottom_label("Permanent mark", MAGENTA)
        self.play(paint(tiles, CLONE_STEPS[3], MAGENTA, 0.66),
                  swap(edu, permanent, run_time=0.7), run_time=0.9)
        self.play(traveling_rings([tiles[key].get_center() for key in CLONE_STEPS[3][::2]], MAGENTA),
                  run_time=1.25)
        self.at("marking two neighboring cells")
        roots = ((4, 2), (5, 2))
        self.play(FadeOut(permanent), paint(tiles, CLONE_STEPS[3], TEAL), run_time=0.48)
        self.play(paint(tiles, roots, MAGENTA, 0.75),
                  traveling_rings([tiles[key].get_center() for key in roots], MAGENTA),
                  run_time=0.9)
        self.at("can mimic one clone")
        left_clone = ((4, 1), (4, 3), (3, 2))
        right_clone = ((5, 1), (5, 3), (6, 2))
        self.play(LaggedStart(paint(tiles, left_clone, MAGENTA), paint(tiles, right_clone, MAGENTA),
                              lag_ratio=0.32), run_time=1.0)
        merged = bottom_label("Two clones merged", MAGENTA)
        self.play(FadeIn(merged), run_time=0.5)
        self.at("controls mark sparsely")
        panels = TwoPanel("Sparse", "No inducer (trigger)", colors=(TEAL, GREY),
                          top=2.83, bottom=-2.52, size=31)
        sparse_marks = [(0, 0), (4, 2)]
        sparse, sparse_tiles = sheet(sparse_marks, cols=5, rows=3, radius=0.55)
        dark, _ = sheet(base=GREY, cols=5, rows=3, radius=0.55)
        dark.set_fill(GREY, opacity=0.19)
        panels.put(sparse, "left")
        panels.put(dark, "right")
        self.play(FadeOut(merged), run_time=0.25)
        self.play(FadeOut(world), FadeIn(panels.left_frame), FadeIn(sparse), run_time=0.59)
        self.play(FadeIn(panels.left_head), run_time=0.21)
        self.at("count close pairs")
        spacing = bottom_label("Short-term spacing check", TEAL, -3.26)
        a, b = [sparse_tiles[key].get_center() for key in sparse_marks]
        gap_line = DashedLine(a + 0.46 * normalize(b - a), b - 0.46 * normalize(b - a),
                              color=TEXT, dash_length=0.16, stroke_width=3)
        self.play(Create(gap_line), FadeIn(spacing), run_time=1.65)
        self.at("the mark stays off")
        self.play(FadeIn(panels.right_frame), FadeIn(panels.right_head), FadeIn(dark), run_time=0.9)
        mark_off = bottom_label("Mark off", TEXT, 3.26)
        self.play(FadeIn(mark_off), traveling_rings([dark.get_center()], GREY), run_time=1.55)
        self.finish()


def wing_hair(point):
    return VMobject(color=TEXT, stroke_width=4.2).set_points_as_corners(
        [point + xy(-0.26, -0.11), point + xy(-0.04, -0.03), point + xy(0.31, 0.02)]
    )


class S09UnlockedWing(SpokenScene):
    def construct(self):
        world, tiles = sheet()
        hairs = {key: wing_hair(tile.get_center()) for key, tile in tiles.items()}
        self.add(world)
        self.at("mosaics also unlocked")
        self.play(traveling_rings([tiles[key].get_center() for key in ((1, 1), (3, 2), (5, 3), (7, 2))],
                                  TEAL, run_time=3.3), run_time=3.3)
        self.at("fly wing hairs", lead=0.38)
        self.play(LaggedStart(*(Create(hairs[key]) for key in sorted(hairs)), lag_ratio=0.033),
                  run_time=1.56)
        self.at("toward the tip")
        tip = bottom_label("Wing tip", TEAL, 3.89)
        tip_arrow = pointer(tip.get_right() + RIGHT * 0.28, xy(5.82, -3.36), TEAL)
        self.play(FadeIn(tip), GrowArrow(tip_arrow), run_time=0.69)
        self.at("in 1987")
        credit = title_label("Vinson & Adler, 1987 (schematic)", GOLD)
        self.play(FadeIn(credit), run_time=0.72)
        self.at("made patches lacking")
        mutant = [(col, row) for col in (3, 4, 5) for row in (1, 2, 3)]
        self.play(LaggedStart(*(tint(tiles[key], MAGENTA) for key in mutant), lag_ratio=0.15),
                  run_time=2.64)
        self.at("normal cells on the tip side")
        affected = [(6, 1), (6, 2), (6, 3), (7, 2)]
        angles = (1.88, 2.70, -1.74, -2.25)
        self.play(LaggedStart(*(Rotate(hairs[key], angle, about_point=tiles[key].get_center())
                               for key, angle in zip(affected, angles)), lag_ratio=0.24),
                  run_time=2.62)
        self.at("on the other side")
        aligned = [(2, 1), (2, 2), (2, 3)]
        self.play(traveling_rings([tiles[key].get_center() for key in aligned], TEAL), run_time=1.48)
        self.at("effect reached beyond")
        self.play(traveling_rings([tiles[key].get_center() for key in affected], YELLOW), run_time=2.0)
        self.finish()


def activity_bars(c, relative):
    """Qualitative bars, with the middle (normal) cell at the same level in each panel."""
    offsets = (-1.43, 0.0, 1.43)
    widths = (relative, 0.72, relative)
    tracks, fills = VGroup(), VGroup()
    for offset, width in zip(offsets, widths):
        center = c + xy(offset, -1.35)
        tracks.add(RoundedRectangle(width=1.14, height=0.23, corner_radius=0.075,
                                    stroke_color=PURPLE, stroke_width=2).move_to(center))
        fill = RoundedRectangle(width=width, height=0.13, corner_radius=0.05,
                                stroke_width=0, fill_color=PURPLE, fill_opacity=1)
        fills.add(fill.move_to(center + RIGHT * (-0.52 + width / 2)))
    return tracks, fills


class S10UnlockedNotum(SpokenScene):
    def construct(self):
        world, _, incoming, receptors = predict_world()
        self.add(world, incoming, receptors)
        self.at("those notch and delta patches")
        self.play(LaggedStart(*(Indicate(part, color=color, scale_factor=1.2)
                               for parts, color in ((incoming, YELLOW), (receptors, PURPLE))
                               for part in parts), lag_ratio=0.24), run_time=1.85)
        self.at("came from pascal")
        credit = title_label("Heitzler & Simpson, 1991", GOLD)
        self.play(FadeIn(credit), run_time=0.68)
        self.at("they also varied")
        panels = TwoPanel("Less Notch in neighbours", "More Notch in neighbours",
                          colors=(PURPLE, PURPLE), top=2.8, bottom=-2.68, size=30)
        groups, centers, levels = [], [], []
        for name, fill, level in (("left", 0.23, 0.35), ("right", 0.79, 0.99)):
            center = panels.area(name)[0] + UP * 0.32
            side_cells = [cell(center + xy(x, 0), 0.83, PURPLE, fill) for x in (-1.43, 1.43)]
            focal = cell(center, 0.83, TEAL, 0.57)
            light_wave([*side_cells, focal], amplitude=0.18)
            tracks, fills = activity_bars(center, level)
            groups.append(VGroup(*side_cells, focal, tracks))
            centers.append(focal)
            levels.append(fills)
        self.play(FadeOut(world), FadeOut(incoming), FadeOut(receptors),
                  FadeIn(groups[0]), FadeIn(groups[1]), run_time=0.75)
        self.play(FadeIn(panels), run_time=0.55)
        self.at("a normal cell besides")
        self.play(LaggedStart(*(GrowFromEdge(bar, LEFT) for bar in levels[0]), lag_ratio=0.24),
                  traveling_rings([tile.get_center() for tile in groups[0][:3]], PURPLE), run_time=1.8)
        self.at("became epidermis")
        skin = bottom_label("Epidermis", TEAL, -3.30)
        self.play(centers[0].animate.stretch(0.64, 1).set_fill(TEAL, 0.77), FadeIn(skin), run_time=0.84)
        self.at("beside more")
        self.play(LaggedStart(*(GrowFromEdge(bar, LEFT) for bar in levels[1]), lag_ratio=0.20),
                  traveling_rings([tile.get_center() for tile in groups[1][:3]], PURPLE), run_time=0.97)
        self.at("a neural precursor")
        neural = bottom_label("Neural precursor", GOLD, 3.30)
        self.play(tint(centers[1], GOLD, 0.80), FadeIn(neural), run_time=0.9)
        self.at("fate followed")
        self.play(LaggedStart(*(Indicate(bars, color=PURPLE, scale_factor=1.06) for bars in levels),
                              lag_ratio=0.47), run_time=1.66)
        self.at("compared with its neighbors")
        self.play(traveling_rings([tile.get_center() for tile in centers], TEXT), run_time=1.35)
        self.finish()


def neuron(center, facing, size=1.0, color=GREY, opacity=0.65):
    """Cartoon arbor with a soma, main stem and prunable branch tips."""
    def point(x, y):
        return center + rotate_vector(xy(x, y) * size, facing)

    def branch(coords, thickness):
        return VMobject(stroke_color=color, stroke_width=thickness, stroke_opacity=opacity
                       ).set_points_as_corners([point(x, y) for x, y in coords])

    trunk = branch([(0, 0), (0.32, 0.18), (0.59, 0.52), (0.81, 0.72)], 4.2)
    branches = VGroup(
        branch([(0.32, 0.18), (0.58, 0.08), (0.95, 0.16)], 3.2),
        branch([(0.59, 0.52), (0.53, 0.81), (0.67, 1.15)], 3.2),
        branch([(0.81, 0.72), (1.05, 0.76), (1.30, 0.98)], 3.2),
        branch([(0, 0), (-0.27, 0.08), (-0.49, 0.26)], 3.2),
    )
    soma = Dot(center, radius=0.103 * size, color=color, fill_opacity=opacity)
    return VGroup(trunk, branches, soma)


def brain():
    # The two broad lobes and central bridge are a schematic silhouette.
    parts = VGroup(
        Ellipse(width=5.65, height=5.37, color=GREY, stroke_width=2.6, stroke_opacity=0.68,
                fill_color=GREY, fill_opacity=0.21).rotate(-0.15).move_to(xy(-2.88, 0.22)),
        Ellipse(width=5.65, height=5.37, color=GREY, stroke_width=2.6, stroke_opacity=0.68,
                fill_color=GREY, fill_opacity=0.21).rotate(0.15).move_to(xy(2.88, 0.22)),
        RoundedRectangle(width=1.65, height=2.28, corner_radius=0.46, stroke_width=0,
                         fill_color=GREY, fill_opacity=0.21).move_to(xy(0, 0.22)),
    )
    light_wave(parts[:2], amplitude=0.27)
    positions = [(-4.40, 1.02, -0.2), (-3.42, 1.92, -1.20), (-2.28, 1.05, 0.3),
                 (-3.82, -0.68, 0.42), (-2.72, -1.57, 0.22), (-1.30, -0.70, 0.72),
                 (0.68, 0.72, 0.45), (1.44, 1.76, -0.20), (3.08, 1.70, -0.90),
                 (4.40, 0.58, 1.10), (2.08, -0.42, -0.57), (3.48, -1.66, 0.72),
                 (1.32, -1.47, 0.22)]
    normals = [neuron(xy(x, y), angle, 0.84) for x, y, angle in positions]
    mutant = neuron(xy(-0.85, -0.24), 0.30, 1.27, MAGENTA, 1.0)
    return parts, normals, mutant


class S11UnlockedMarcm(SpokenScene):
    def construct(self):
        world, _ = sheet()
        outline, surrounding, gamma = brain()
        self.add(world)
        self.at("mosaics even reach")
        self.play(FadeOut(world), FadeIn(outline), run_time=1.15)
        self.play(LaggedStart(*(FadeIn(n) for n in surrounding), lag_ratio=0.09), run_time=2.2)
        self.at("m a r c m")
        marcm = title_label("MARCM", MAGENTA)
        self.play(LaggedStart(*(Create(part) for part in gamma), lag_ratio=0.30), run_time=1.10)
        self.play(FadeIn(marcm), run_time=0.52)
        self.at("one or a few neurons")
        self.play(traveling_rings([gamma[2].get_center(), gamma[0].get_end()], MAGENTA),
                  run_time=2.6)
        self.at("making only those mutant")
        self.play(Indicate(gamma, color=MAGENTA, scale_factor=1.10), run_time=1.75)
        self.at("in 2000")
        credit = title_label("Lee, Luo et al., 2000", GOLD)
        self.play(swap(marcm, credit, run_time=0.83), run_time=0.83)
        self.at("colleagues tested")
        self.play(traveling_rings([gamma[0].get_end(), gamma[2].get_center()], MAGENTA),
                  run_time=1.7)
        self.at("called gamma neurons")
        gamma_label = bottom_label("Gamma neuron", MAGENTA)
        self.play(FadeIn(gamma_label), run_time=0.66)
        self.at("needed the steroid receptor")
        receptor = bottom_label("EcR-B1 mutant", MAGENTA)
        self.play(swap(gamma_label, receptor, run_time=0.83), run_time=0.83)
        self.play(Indicate(gamma[2], color=MAGENTA, scale_factor=1.5), run_time=1.4)
        self.at("to remodel at metamorphosis")
        ordered = sorted(surrounding, key=lambda n: n.get_x())
        pruning = []
        for n in ordered:
            tips = n[1]
            pruning.append(AnimationGroup(*(
                branch.animate.scale(0.20, about_point=branch.get_start()).set_stroke(opacity=0.23)
                for branch in tips
            )))
        self.play(LaggedStart(*pruning, lag_ratio=0.18), run_time=2.85)
        self.at("pinpoint where a gene")
        self.play(traveling_rings([gamma[2].get_center(), gamma[0].get_end()], MAGENTA),
                  run_time=1.45)
        self.finish()


class S12End(EndCard):
    LINE = "Mutant patches beside normal neighbours reveal where a gene must act."
