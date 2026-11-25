"""Overhead kitchen-table animation for the Plant Parts We Eat parent guide."""

from bp_parts import *


# COLOR MAP: the setup template's blue for ideas, teal for materials, gold for
# setup and green for observation, with red for safety. On the drawing, soil
# and roots are brown, stems and leaves are green, flowers gold, fruit red.
TABLE = "#33211d"
PAPER = "#f3e5c8"
INK = "#332b26"
WOOD = "#d4a575"
BROWN = "#895839"
STEM = "#47794a"
LEAF = "#317458"
LIGHT_LEAF = "#84a758"
BUD = "#316450"
BUD_LIGHT = "#5f9160"
FLOWER = "#eab744"
RED_FRUIT = "#c44e41"
RED_DARK = "#983a33"
CARROT = "#df7841"
BLUE_INK = "#21576e"
SAFETY_INK = "#963c34"
WATER = "#4388a4"
SKIN = "#b57756"
CHILD_SKIN = "#e0a77b"
CUFF = "#477e85"
CHILD_CUFF = "#98614f"
CREAM = "#fff6e1"


def pt(x, y):
    return np.array([x, y, 0.0])


def ellipse(x, y, w, h, fill, angle=0, stroke=None, sw=2):
    return Ellipse(
        width=w, height=h, fill_color=fill, fill_opacity=1,
        stroke_color=stroke or fill, stroke_width=sw if stroke else 0,
    ).rotate(angle).move_to(pt(x, y))


def box(x, y, w, h, fill, radius=0.15, stroke=None):
    return RoundedRectangle(
        width=w, height=h, corner_radius=radius, fill_color=fill, fill_opacity=1,
        stroke_color=stroke or fill, stroke_width=2 if stroke else 0,
    ).move_to(pt(x, y))


def path(points, color, width=4):
    line = VMobject(stroke_color=color, stroke_width=width)
    line.set_points_smoothly([pt(*p) for p in points])
    line.set_cap_style(CapStyleType.ROUND)
    return line


def shape(start, segments, fill):
    outline = VMobject(fill_color=fill, fill_opacity=1, stroke_width=0)
    outline.start_new_path(pt(*start))
    for handle1, handle2, end in segments:
        outline.add_cubic_bezier_curve_to(pt(*handle1), pt(*handle2), pt(*end))
    outline.close_path()
    return outline


def note(words, x, y, size=34, color=INK):
    return T(words, size, color, weight=BOLD, line_spacing=0.85).move_to(pt(x, y))


def sheet():
    return VGroup(
        box(0.09, -0.13, 12.1, 6.69, "#211816", 0.14),
        box(0, 0, 12.1, 6.69, PAPER, 0.14),
    )


def botanical_leaf(x, y, length, angle, color=LEAF):
    body = shape(
        (0, 0),
        [((0.22, 0.37), (0.68, 0.43), (1, 0.04)),
         ((0.73, -0.32), (0.34, -0.37), (0, 0))],
        color,
    )
    vein = path([(0.06, 0), (0.47, 0.02), (0.87, 0.05)], "#bed088", 2)
    return VGroup(body, vein).scale(length, about_point=ORIGIN).rotate(
        angle, about_point=ORIGIN
    ).shift(pt(x, y))


def blossom(x, y, radius=0.53):
    petals = VGroup(*[
        ellipse(0.28 * np.cos(a), 0.28 * np.sin(a), 0.52, 0.32, FLOWER, a)
        for a in np.arange(5) * TAU / 5
    ])
    return VGroup(petals, Dot(radius=0.16, color="#8b5e39")).scale(
        radius / 0.53, about_point=ORIGIN
    ).shift(pt(x, y))


def carrot():
    top = VGroup(*[
        botanical_leaf(0, 0.63, 0.57, angle, color)
        for angle, color in [(0.65, STEM), (1.42, LEAF), (2.22, LIGHT_LEAF)]
    ])
    root = shape(
        (0, 0.68),
        [((0.55, 0.68), (0.42, 0.12), (0.3, -0.17)),
         ((0.19, -0.49), (0.05, -0.87), (-0.07, -0.97)),
         ((-0.21, -0.75), (-0.29, -0.31), (-0.39, 0.14)),
         ((-0.45, 0.48), (-0.39, 0.68), (0, 0.68))],
        CARROT,
    )
    marks = VGroup(*[
        path(coords, BROWN, 1.9) for coords in [
            [(-0.36, 0.34), (-0.23, 0.32), (-0.15, 0.34)],
            [(0.33, 0.17), (0.2, 0.14), (0.13, 0.15)],
            [(-0.24, -0.25), (-0.13, -0.27), (-0.04, -0.26)],
            [(0.18, -0.43), (0.08, -0.43), (0.02, -0.41)],
        ]
    ])
    side_roots = VGroup(
        path([(-0.36, 0.34), (-0.51, 0.32), (-0.64, 0.21)], BROWN, 2),
        path([(0.33, 0.17), (0.5, 0.1), (0.58, -0.05)], BROWN, 2),
        path([(-0.24, -0.25), (-0.42, -0.35), (-0.48, -0.49)], BROWN, 2),
    )
    result = VGroup(top, root, marks, side_roots)
    result.clue = side_roots
    return result


def broccoli():
    stalks = VGroup(
        path([(0, -0.9), (0.01, -0.43), (-0.02, 0.42)], LIGHT_LEAF, 18),
        path([(-0.03, -0.43), (-0.33, 0.02), (-0.68, 0.27)], STEM, 12),
        path([(0.03, -0.48), (0.32, -0.01), (0.66, 0.28)], STEM, 12),
    )
    crown = VGroup(*[
        ellipse(x, y, w, h, color, angle)
        for x, y, w, h, color, angle in [
            (-0.58, 0.35, 0.86, 0.69, BUD, 0.3),
            (0.58, 0.39, 0.88, 0.75, BUD, -0.2),
            (0.05, 0.43, 1.16, 0.97, "#3d7854", 0.1),
            (-0.22, 0.76, 0.56, 0.42, STEM, 0.4),
            (0.37, 0.71, 0.54, 0.44, STEM, -0.4),
        ]
    ])
    bumps = VGroup(*[
        ellipse(x, y, r * 2, r * 1.7, BUD_LIGHT if i % 3 else "#77a36c")
        for i, (x, y, r) in enumerate([
            (-0.91, 0.34, 0.10), (-0.79, 0.51, 0.13), (-0.58, 0.58, 0.12),
            (-0.68, 0.29, 0.11), (-0.49, 0.36, 0.15), (-0.26, 0.57, 0.13),
            (-0.33, 0.79, 0.11), (-0.15, 0.91, 0.13), (0.05, 0.82, 0.12),
            (0.25, 0.93, 0.09), (0.37, 0.77, 0.14), (0.59, 0.64, 0.13),
            (0.79, 0.57, 0.11), (0.90, 0.39, 0.10), (0.67, 0.36, 0.10),
            (0.43, 0.49, 0.11), (0.18, 0.57, 0.15), (-0.03, 0.64, 0.12),
            (-0.14, 0.39, 0.12), (0.11, 0.31, 0.13), (0.34, 0.29, 0.10),
        ])
    ])
    head = VGroup(stalks, crown, bumps)
    head.buds = bumps
    return head


def apple():
    body = shape(
        (0, 0.45),
        [((-0.72, 0.89), (-0.9, 0.16), (-0.58, -0.37)),
         ((-0.44, -0.7), (-0.15, -0.72), (0, -0.61)),
         ((0.23, -0.74), (0.53, -0.64), (0.69, -0.21)),
         ((0.88, 0.28), (0.67, 0.84), (0, 0.45))],
        RED_FRUIT,
    )
    return VGroup(
        body, path([(0, 0.44), (0.03, 0.65), (0.13, 0.84)], BROWN),
        botanical_leaf(0.04, 0.68, 0.49, 0.44, LEAF),
        ellipse(-0.44, 0.19, 0.14, 0.42, "#e97c64", -0.25),
    )


def tomato():
    return VGroup(
        ellipse(0, -0.05, 1.59, 1.24, RED_FRUIT),
        ellipse(-0.39, 0.16, 0.18, 0.39, "#e97c64", -0.85),
        *[botanical_leaf(0, 0.51, 0.48, a, STEM) for a in (0.18, 1.32, 2.75, 3.85, 5.35)],
    )


def fruit_slice(kind):
    is_apple = kind == "apple"
    rind = ellipse(0, 0, 1.58, 1.4, RED_DARK)
    pulp = ellipse(0, 0, 1.46, 1.28, "#f9e4ab" if is_apple else "#ea8a65")
    pockets = VGroup()
    seeds = VGroup()
    for a in np.arange(5 if is_apple else 4) * TAU / (5 if is_apple else 4) + PI / 2:
        x, y = np.cos(a), np.sin(a)
        r = 0.23 if is_apple else 0.37
        pockets.add(ellipse(x * r, y * r, 0.31 if is_apple else 0.5, 0.23,
                            "#ebca8e" if is_apple else "#b65041", a))
        for offset in ([0] if is_apple else [-0.16, 0.16]):
            seeds.add(ellipse(x * r - y * offset, y * r + x * offset,
                              0.13, 0.07, BROWN if is_apple else "#fff1a2", a + 0.3))
    result = VGroup(rind, pulp, pockets, seeds)
    result.seeds = seeds
    return result


def potato():
    skin = shape(
        (-0.82, -0.16),
        [((-0.92, 0.33), (-0.42, 0.7), (0.15, 0.61)),
         ((0.58, 0.65), (0.91, 0.38), (0.84, -0.04)),
         ((0.88, -0.44), (0.47, -0.64), (0.09, -0.56)),
         ((-0.34, -0.67), (-0.78, -0.52), (-0.82, -0.16))],
        "#b98254",
    )
    eyes = VGroup(*[
        VGroup(ellipse(x, y, 0.24, 0.13, "#a37149", a), ellipse(x, y, 0.09, 0.04, "#6d4837", a))
        for x, y, a in [(-0.46, 0.21, -0.25), (0.04, -0.05, 0.2), (0.48, 0.3, 0.28),
                        (0.45, -0.32, -0.2)]
    ])
    result = VGroup(skin, eyes)
    result.eyes = eyes
    return result


def celery():
    ribs = VGroup(*[
        path([(i * 0.11, -0.96), (i * 0.16, -0.29), (i * 0.24, 0.52)], col, 10)
        for i, col in [(-1, "#91a754"), (0, "#bbbf67"), (1, "#799b53")]
    ])
    tips = VGroup(
        botanical_leaf(-0.21, 0.51, 0.64, 2.66),
        botanical_leaf(0.02, 0.52, 0.69, 1.36, STEM),
        botanical_leaf(0.21, 0.51, 0.55, 0.66),
    )
    result = VGroup(ribs, tips)
    result.tips = tips
    return result


def asparagus():
    spears = VGroup()
    for x, tilt in [(-0.27, 0.19), (0, -0.05), (0.28, -0.24)]:
        base = box(0, -0.25, 0.17, 1.37, LIGHT_LEAF, 0.08)
        tip = shape(
            (0, 0.93), [((0.23, 0.66), (0.22, 0.26), (0, 0.28)),
                        ((-0.22, 0.26), (-0.19, 0.65), (0, 0.93))],
            LEAF,
        )
        scales = VGroup(*[path([(-0.09, y + 0.07), (0, y), (0.09, y + 0.07)],
                              LIGHT_LEAF, 1.6) for y in (0.44, 0.59)])
        spears.add(VGroup(base, tip, scales).rotate(tilt, about_point=ORIGIN).shift(RIGHT * x))
    return spears


def lettuce():
    return VGroup(*[
        botanical_leaf(0, -0.64, length, a, color)
        for length, a, color in [
            (1.37, 2.32, LEAF), (1.43, 0.77, LEAF),
            (1.62, 1.85, "#4c905d"), (1.48, 1.29, STEM), (1.06, 1.58, LIGHT_LEAF),
        ]
    ])


def seeds_food():
    return VGroup(*[
        ellipse(x, y, 0.38, 0.37, color)
        for x, y, color in [(-0.34, -0.04, STEM), (0, -0.24, LEAF),
                            (0.33, 0, BUD_LIGHT), (0.07, 0.24, LIGHT_LEAF)]
    ])


FOODS = dict(carrot=carrot, asparagus=asparagus, lettuce=lettuce, broccoli=broccoli,
             apple=apple, tomato=tomato, peas=seeds_food, potato=potato, celery=celery)


def food(name, x, y, height, angle=0):
    return FOODS[name]().rotate(angle).set_height(height).move_to(pt(x, y))


def bag():
    back = box(3.43, 0.84, 4.18, 3.56, "#aa754c", 0.37)
    lip = ellipse(3.38, 1.81, 3.66, 1.18, "#5f3c2c", -0.12)
    produce = VGroup(food("broccoli", 2.54, 2.03, 1.65, 0.2),
                     food("apple", 4.31, 1.94, 1.35, -0.2),
                     food("carrot", 3.55, 2.03, 2.54, -0.39))
    front = shape(
        (1.37, 1.63),
        [((2.75, 1.04), (4.43, 1.02), (5.52, 1.57)),
         ((5.38, 0.52), (5.16, -0.55), (4.99, -0.89)),
         ((4.0, -1.12), (2.56, -1.02), (1.88, -0.78)),
         ((1.7, -0.1), (1.45, 0.97), (1.37, 1.63))],
        WOOD,
    )
    folds = VGroup(
        path([(1.78, 1.29), (2.05, 0.43), (2.25, -0.68)], "#b48156", 3),
        path([(5.14, 1.28), (4.93, 0.42), (4.72, -0.77)], "#b48156", 3),
        path([(2.49, -0.66), (3.44, -0.76), (4.48, -0.7)], "#ba8b64", 3),
    )
    return VGroup(back, lip, produce, front, folds)


def plant():
    soil = path([(-3.85, -0.92), (-2.59, -0.88), (-1.1, -0.94),
                 (0.37, -0.91), (1.64, -0.97)], "#ae855f", 3)
    roots = VGroup(*[
        path(points, BROWN, width) for points, width in [
            ([(-0.8, -0.8), (-0.79, -1.56), (-1.09, -2.2), (-1.18, -2.89)], 9),
            ([(-0.79, -1.18), (-1.42, -1.4), (-1.92, -1.82), (-2.37, -2.33)], 5),
            ([(-1.53, -1.5), (-1.91, -1.58), (-2.31, -1.77)], 3),
            ([(-1.92, -1.83), (-2.05, -2.22), (-2.11, -2.53)], 3),
            ([(-0.88, -1.55), (-0.29, -1.8), (0.05, -2.22), (0.53, -2.61)], 5),
            ([(-0.11, -1.98), (0.37, -1.99), (0.73, -2.13)], 3),
            ([(-1.07, -2.12), (-0.78, -2.53), (-0.66, -2.79)], 3),
            ([(-1.12, -2.37), (-1.46, -2.51), (-1.68, -2.76)], 3),
        ]
    ])
    stem = VGroup(
        path([(-0.8, -0.94), (-0.76, 0.24), (-0.85, 1.45), (-0.66, 2.55)], STEM, 13),
        path([(-0.79, 0.43), (-0.14, 0.45), (0.52, 0.26), (0.72, 0.05)], STEM, 6),
    )
    leaves = VGroup(
        botanical_leaf(-0.79, -0.08, 2.36, 2.73),
        botanical_leaf(-0.85, 0.92, 2.15, 2.83, "#45885d"),
        botanical_leaf(-0.86, 1.42, 1.85, 0.42, LEAF),
    )
    flower = blossom(-0.62, 2.51, 0.64)
    fruit = fruit_slice("tomato").scale(0.82).move_to(pt(0.79, -0.14))
    return dict(soil=soil, root=roots, stem=stem, leaf=leaves, flower=flower,
                fruit=VGroup(*fruit[:3]), seeds=fruit.seeds)


PART_LABELS = (
    ("root", (-3.15, -2.28), (-2.49, -2.28), (-2.34, -2.3)),
    ("stem", (-3.13, -0.57), (-2.54, -0.57), (-0.84, -0.65)),
    ("leaf", (-3.78, 1.22), (-3.34, 1.22), (-2.77, 1.42)),
    ("flower", (1.15, 2.84), (0.28, 2.84), (-0.22, 2.7)),
    ("fruit", (2.30, 0.45), (1.68, 0.45), (1.31, 0.18)),
    ("seeds", (2.35, -0.54), (1.57, -0.54), (1.05, -0.34)),
)
GUESSES = dict(broccoli=(-3.15, 0.23, 1.21), carrot=(-2.68, -2.1, 1.46),
               potato=(0.38, -2.34, 0.9))
SORTED = dict(carrot=GUESSES["carrot"], asparagus=(0.3, 0.86, 1.09),
              lettuce=(-4.22, 0.23, 1.16), broccoli=(-2.60, 2.37, 1.34),
              apple=(2.63, 0.87, 1.03), tomato=(2.19, -0.28, 0.94),
              peas=(1.53, -1.13, 0.59), potato=(-1.55, -0.56, 0.64),
              celery=(-3.03, 0.65, 1.4))


def placed(name, layout):
    x, y, height = layout[name]
    if name == "tomato":
        return fruit_slice(name).set_height(height).move_to(pt(x, y))
    return food(name, x, y, height, 0.35 if name == "carrot" else 0)


def foods_on(layout, *names):
    return VGroup(*(placed(name, layout) for name in names or tuple(layout)))


def hand(x, y, height, child=False, angle=0):
    skin = CHILD_SKIN if child else SKIN
    cuff = CHILD_CUFF if child else CUFF
    wrist = box(0, -0.75, 0.56, 0.75, cuff, 0.12)
    palm = ellipse(0, -0.14, 0.65, 0.79, skin)
    fingers = VGroup(*[
        box(dx, y0, 0.135, length, skin, 0.065)
        for dx, y0, length in [(-0.22, 0.24, 0.57), (-0.07, 0.32, 0.67),
                               (0.08, 0.35, 0.7), (0.23, 0.25, 0.58)]
    ])
    thumb = ellipse(0.34, -0.04, 0.23, 0.49, skin, -0.64)
    return VGroup(wrist, palm, fingers, thumb).rotate(angle).set_height(height).move_to(pt(x, y))


def marker(x, y, angle=-0.8, color=LEAF):
    return VGroup(
        box(0, 0, 0.22, 1.35, color, 0.1),
        box(0, -0.42, 0.22, 0.41, INK, 0.08),
        Polygon(pt(-0.07, -0.61), pt(0.07, -0.61), pt(0, -0.78),
                fill_color=INK, fill_opacity=1, stroke_width=0),
    ).rotate(angle).move_to(pt(x, y))


def outline(target, color=BLUE_INK, pad=0.12):
    return Ellipse(width=target.width + pad * 2, height=target.height + pad * 2,
                   stroke_color=color, stroke_width=3.5).move_to(target)


def allergy_note():
    return boxed_label("Check food allergies", SAFETY_INK, size=35, pad=0.27).move_to(pt(-2.5, 1.25))


def picture_card():
    return VGroup(box(0, 0, 2.4, 2.08, CREAM, 0.13, WOOD),
                  food("apple", 0, 0.16, 1.47)).rotate(-0.13).move_to(pt(2.65, 0.27))


def knife():
    blade = shape(
        (-0.17, -0.11),
        [((0.52, -0.2), (1.13, -0.13), (1.59, 0.19)),
         ((0.86, 0.28), (0.2, 0.26), (-0.17, 0.22)),
         ((-0.18, 0.08), (-0.17, 0.0), (-0.17, -0.11))],
        "#c5d5d8",
    )
    handle = box(-0.61, 0.05, 0.95, 0.37, INK)
    pins = VGroup(*[Dot(pt(x, 0.05), radius=0.044, color=WOOD) for x in (-0.84, -0.6, -0.36)])
    return VGroup(blade, handle, pins)


def sink():
    return VGroup(
        box(0, -0.14, 7.8, 5.26, "#5c8790", 0.42),
        box(0, -0.48, 6.73, 3.97, "#2d5764", 0.47),
        Circle(radius=0.26, stroke_color="#8fadb2", stroke_width=4).move_to(pt(0.82, -1.32)),
        path([(0, 2.73), (0.02, 2.33), (0.4, 2.11), (0.86, 2.04)], "#d3dfe2", 17),
    )


def water_drops(x, y, color=WATER):
    return VGroup(*[
        shape((dx, dy + 0.21), [((dx + 0.29, dy - 0.1), (dx + 0.1, dy - 0.21), (dx, dy - 0.21)),
                                 ((dx - 0.1, dy - 0.21), (dx - 0.29, dy - 0.1), (dx, dy + 0.21))], color)
        for dx, dy in [(-0.39, 0.23), (0.11, 0.02), (0.42, 0.47)]
    ]).shift(pt(x, y))


def phone():
    return VGroup(
        box(0, 0, 2.3, 3.62, INK, 0.33),
        box(0, 0.02, 1.93, 2.95, "#dbe9dc", 0.24),
        Circle(radius=0.62, stroke_width=0, fill_color=LEAF, fill_opacity=1),
        path([(-0.24, 0.28), (-0.11, -0.03), (0.21, -0.23)], CREAM, 12),
        box(0, -1.63, 0.48, 0.072, WOOD, 0.03),
    )


def broccoli_question():
    head = food("broccoli", 2.9, -0.13, 4.97, -0.1)
    card = question_card("Broccoli:\nwhich plant part?", y=0.37, color=INK, size=43,
                         left=-5.31, max_w=5.8)
    backing = box(-3.0, 0.37, 5.12, 2.27, CREAM, 0.3, WOOD)
    return head, VGroup(backing, card)


class TableScene(SpokenScene):
    def setup(self):
        super().setup()
        self.camera.background_color = TABLE


class S01Hook(TableScene):
    def construct(self):
        groceries = bag()
        self.add(sheet(), groceries)
        self.at("which part of a plant")
        self.play(FadeIn(note("Which part\nis a carrot?", -3.02, 0.45, 53)), run_time=0.72)
        self.at("and what does")
        self.play(groceries.animate.rotate(-0.045).shift(LEFT * 0.16 + DOWN * 0.13), run_time=1.8)
        self.at("a bag of groceries")
        self.play(groceries.animate.rotate(0.045).shift(RIGHT * 0.16 + UP * 0.13), run_time=1.3)
        self.at("one big drawing")
        self.play(FadeIn(marker(-3.0, -1.43), shift=UP * 0.48), run_time=1.15)
        self.finish()


class S02Title(TitleCard):
    TITLE = "Plant Parts We Eat: Parent Guide"
    LESSON = "Plant Parts We Eat"

    def construct(self):
        self.camera.background_color = TABLE
        groceries = bag().shift(UP * 0.09)
        title_text, subtitle_text = self.TITLE.split(": ", 1)
        title = T(title_text, 52, INK, font=TITLE_FONT).move_to(pt(-2.63, 0.7))
        subtitle = note(subtitle_text, -2.63, -0.13, 29, BLUE_INK)
        self.add(sheet(), groceries)
        self.play(FadeIn(title), groceries.animate.shift(DOWN * 0.09), run_time=0.63)
        self.play(FadeIn(subtitle), run_time=0.43)
        self.wait(self.narration_s - self.elapsed())


class S03Payoff(TableScene):
    def construct(self):
        picture = plant()
        groceries = bag()
        self.add(sheet(), groceries)
        self.at("fruits and vegetables")
        self.play(FadeOut(groceries, shift=RIGHT * 0.65),
                  Create(picture["soil"]), Create(picture["stem"]), run_time=1.25)
        self.play(Create(picture["root"]), run_time=1.28)
        self.play(FadeIn(picture["leaf"], shift=UP * 0.18), run_time=0.95)
        self.at("each part had")
        self.play(FadeIn(picture["flower"], scale=0.62), run_time=0.72)
        self.play(FadeIn(picture["fruit"], scale=0.65), run_time=0.62)
        self.play(FadeIn(picture["seeds"]), run_time=0.61)
        self.at("your child practices")
        self.play(FadeIn(note("Sort", 3.65, 1.33, 35, BLUE_INK), shift=UP * 0.13), run_time=0.82)
        self.at("looking for clues")
        self.play(FadeIn(note("Find clues", 3.65, 0.41, 35, BLUE_INK), shift=UP * 0.13), run_time=0.81)
        self.at("and changing a guess")
        self.play(FadeIn(note("Change the guess", 3.65, -0.53, 35, BLUE_INK), shift=UP * 0.13), run_time=1.02)
        self.finish()


class S04Gather(TableScene):
    def construct(self):
        check = allergy_note()
        card = picture_card()
        self.add(sheet())
        self.at("check for food allergies")
        self.play(FadeIn(check, shift=DOWN * 0.4), run_time=1.03)
        self.at("use pictures for foods")
        self.play(FadeIn(card, shift=LEFT * 1.15), run_time=1.42)
        self.play(card.animate.rotate(0.13).shift(LEFT * 0.18), run_time=1.21)
        self.at("gather paper markers")
        pens = VGroup(marker(-4.91, -1.75), marker(-4.42, -2.0, color=BLUE_INK))
        self.play(FadeOut(check), FadeOut(card), FadeIn(pens, shift=UP * 0.33), run_time=0.65)
        row = [
            ("carrot", "a carrot asparagus", -4.10, -0.25, 2.62, 0.37),
            ("asparagus", "asparagus lettuce", -2.45, -0.17, 2.37, 0.04),
            ("lettuce", "lettuce broccoli", -0.56, -0.37, 1.68, -0.12),
            ("broccoli", "broccoli an apple", 1.61, -0.26, 2.03, -0.07),
            ("apple", "an apple and", 3.52, -0.28, 1.60, -0.09),
            ("tomato", "and a tomato", 5.09, -0.31, 1.29, 0),
        ]
        group = VGroup()
        for name, cue, x, y, height, angle in row:
            self.at(cue)
            item = food(name, x, y, height, angle)
            self.play(FadeIn(item, shift=DOWN * 0.45), run_time=0.41)
            group.add(item)
        self.play(group.animate.scale(0.94).shift(UP * 1.43), run_time=1.12)
        for name, cue, x, height, angle in [
            ("peas", "add canned beans", -2.55, 1.13, 0),
            ("potato", "a firm potato", 0.15, 1.55, 0),
            ("celery", "and celery with", 2.93, 2.32, 0.29),
        ]:
            self.at(cue)
            item = food(name, x, -1.66, height, angle)
            self.play(FadeIn(item, shift=UP * 0.52), run_time=1.17)
        self.finish()


class S05DrawCut(TableScene):
    def construct(self):
        picture = VGroup(*plant().values())
        pen = marker(-4.75, -0.31)
        self.add(sheet(), picture)
        self.at("help your child draw")
        self.play(FadeIn(pen, shift=RIGHT * 0.57), run_time=0.78)
        self.at("and label each part", lead=0.6)
        labels = VGroup()
        for name, position, near_label, near_part in PART_LABELS:
            label = note(name, *position, 29)
            leader = Line(pt(*near_part), pt(*near_label), stroke_color=BROWN, stroke_width=2)
            self.play(Create(leader), FadeIn(label), run_time=0.36)
            labels.add(leader, label)
        self.at("wash the produce")
        produce = VGroup(food("apple", -1.58, -0.13, 2.15), food("tomato", 1.61, -0.13, 1.99))
        basin = sink()
        drops = water_drops(0.66, 0.64, "#a3e3e8")
        self.play(FadeOut(picture), FadeOut(labels), FadeOut(pen), run_time=0.23)
        self.play(FadeIn(basin), FadeIn(produce), FadeIn(drops), run_time=0.54)
        self.play(drops.animate.shift(DOWN * 0.92), run_time=0.9, rate_func=linear)
        self.at("you cut the apple")
        board = box(0, 0, 8.3, 5.52, WOOD, 0.37)
        blade = knife().scale(0.91).rotate(-0.17).move_to(pt(-1.6, 1.41))
        adult = hand(-3.05, 1.55, 1.64, angle=-1.72)
        self.play(FadeOut(drops), ReplacementTransform(basin, board), run_time=0.45)
        self.bring_to_front(produce)
        self.play(FadeIn(adult), FadeIn(blade), run_time=0.37)
        self.at("across the middle")
        self.play(VGroup(adult, blade).animate.shift(DOWN * 0.97), run_time=0.45)
        new_apple = fruit_slice("apple").set_height(2.07).move_to(produce[0])
        self.play(ReplacementTransform(produce[0], new_apple),
                  VGroup(adult, blade).animate.shift(RIGHT * 3.12 + UP * 0.43), run_time=0.46)
        self.at("the seeds show")
        new_tomato = fruit_slice("tomato").set_height(2.0).move_to(produce[1])
        self.play(ReplacementTransform(produce[1], new_tomato),
                  VGroup(adult, blade).animate.shift(DOWN * 0.62), run_time=0.58)
        self.play(FadeOut(adult, shift=LEFT * 0.68), FadeOut(blade, shift=LEFT * 0.68), run_time=0.52)
        self.at("leave everything else")
        wholes = VGroup(food("broccoli", -3.06, -1.76, 1.02),
                        food("carrot", 0.0, -1.85, 1.25, 0.75),
                        food("potato", 3.05, -1.78, 0.78))
        self.play(FadeIn(wholes, shift=UP * 0.42), run_time=0.87)
        self.finish()


class S06PredictChild(TableScene):
    def construct(self):
        drawing = VGroup(*plant().values())
        adult = hand(3.63, -0.91, 2.51, angle=-0.29)
        head = food("broccoli", 3.36, 0.51, 2.40, 0.06)
        self.add(sheet(), drawing)
        self.at("hold up one food")
        self.play(FadeIn(adult, shift=DOWN * 0.53), FadeIn(head, shift=DOWN * 0.53), run_time=1.02)
        self.play(VGroup(adult, head).animate.shift(UP * 0.22), run_time=1.13)
        self.at("ask which part")
        bubble = boxed_label("Which part?", BLUE_INK, size=34, pad=0.24).move_to(pt(3.39, 2.65))
        self.play(FadeIn(bubble), run_time=0.62)
        self.at("let your child place")
        child = hand(4.35, -0.8, 1.64, child=True, angle=0.55)
        self.play(FadeOut(bubble), FadeOut(adult, shift=DOWN * 0.4), run_time=0.31)
        self.play(FadeIn(child), run_time=0.37)
        landed = placed("broccoli", GUESSES)
        self.play(Transform(head, landed, path_arc=0.16),
                  child.animate.move_to(landed.get_center() + pt(0.18, -0.65)), run_time=1.5)
        self.at("don't correct anything")
        for name, starting_point in [("carrot", (-4.57, -2.25)), ("potato", (2.26, -2.32))]:
            placed_food = placed(name, GUESSES)
            moving_food = placed_food.copy().move_to(pt(*starting_point))
            self.play(child.animate.move_to(moving_food.get_center() + DOWN * 0.59),
                      FadeIn(moving_food), run_time=0.46)
            self.play(Transform(moving_food, placed_food),
                      child.animate.move_to(placed_food.get_center() + DOWN * 0.59), run_time=0.8)
        self.at("that first sort")
        self.play(FadeOut(child, shift=DOWN * 0.43),
                  FadeIn(note("First sort", 3.64, 1.3, 39, BLUE_INK)), run_time=0.69)
        self.finish()


class S07Clues(TableScene):
    def construct(self):
        picture = plant()
        guesses = foods_on(GUESSES)
        self.add(sheet(), VGroup(*picture.values()), guesses)
        self.at("now go back")
        whole = food("tomato", 3.68, 0.63, 2.38)
        self.play(FadeIn(whole, shift=DOWN * 0.48), run_time=0.91)
        self.play(whole.animate.rotate(0.15), run_time=1.18)
        self.at("a tomato grows")
        bloom = blossom(3.68, 0.63, 0.81)
        sliced = fruit_slice("tomato").set_height(2.77).move_to(whole)
        self.play(FadeOut(whole), FadeIn(bloom, scale=0.4), run_time=0.47)
        ripened = food("tomato", 3.68, 0.63, 2.63)
        self.play(ReplacementTransform(bloom, ripened), run_time=1.0)
        self.at("and holds seeds")
        self.play(ReplacementTransform(ripened, sliced), run_time=0.44)
        ring = outline(sliced.seeds, CREAM, 0.07)
        self.play(Create(ring), run_time=0.46)
        self.at("so it is a fruit")
        correct = placed("tomato", SORTED)
        child = hand(4.55, -0.47, 1.65, child=True, angle=0.44)
        self.play(FadeOut(ring), FadeIn(child), run_time=0.41)
        self.play(Transform(sliced, correct, path_arc=-0.27),
                  child.animate.move_to(correct.get_center() + pt(0.65, -0.74)), run_time=0.95)
        self.play(FadeOut(child, shift=DOWN * 0.31), run_time=0.29)
        self.at("look for thin side roots")
        carrot_detail = food("carrot", 4.35, -0.15, 3.60, 0.08)
        self.play(TransformFromCopy(guesses[1], carrot_detail, path_arc=-0.17), run_time=1.13)
        tips = VGroup(*[
            Circle(radius=0.18, stroke_color=BLUE_INK, stroke_width=3.5).move_to(side_root.get_end())
            for side_root in carrot_detail.clue
        ])
        self.play(LaggedStart(*[Create(tip) for tip in tips], lag_ratio=0.52), run_time=1.36)
        self.at("ask what", lead=0.33)
        self.play(FadeOut(tips), FadeOut(carrot_detail, shift=DOWN * 0.35), run_time=0.28)
        q = question_card("What is your clue?", y=1.33, color=BLUE_INK, size=34, left=2.25, max_w=3.4)
        self.play(FadeIn(q), run_time=0.25)
        self.finish()


class S08PredictQ(TableScene):
    def construct(self):
        head, card = broccoli_question()
        drawing = VGroup(*plant().values())
        other_foods = VGroup(foods_on(GUESSES, "carrot", "potato"), placed("tomato", SORTED))
        head.save_state()
        head.become(placed("broccoli", GUESSES))
        self.add(sheet(), drawing, other_foods, head)
        self.at("here is one for you")
        self.play(FadeOut(drawing), FadeOut(other_foods), Restore(head, path_arc=-0.17),
                  run_time=1.59)
        self.at("look closely")
        head.save_state()
        self.play(head.animate.rotate(0.11).scale(1.05), run_time=1.22)
        self.play(Restore(head), run_time=1.1)
        self.at("which part of the plant")
        self.play(FadeIn(card, shift=UP * 0.17), run_time=0.62)
        head.save_state()
        self.play(head.animate.shift(LEFT * 0.26).rotate(-0.13), run_time=0.82)
        self.play(Restore(head), run_time=1.31, rate_func=linear)
        self.finish()


class S09Pause(Scene):
    def construct(self):
        self.camera.background_color = TABLE
        head, card = broccoli_question()
        self.add(sheet(), head, card)
        self.wait(4.5)


class S10Reveal(TableScene):
    def construct(self):
        head, card = broccoli_question()
        self.add(sheet(), head, card)
        self.at("each small green bump")
        self.play(FadeOut(card), head.animate.scale(1.14).move_to(pt(1.18, -0.2)),
                  run_time=0.88, rate_func=linear)
        buds = [head.buds[i] for i in (1, 7, 10, 16, 19)]
        rings = VGroup(*[outline(bud, CREAM, 0.07) for bud in buds])
        self.play(LaggedStart(*[Create(ring) for ring in rings], lag_ratio=0.2), run_time=0.96)
        self.at("a flower bud")
        designation = note("Flower buds", -3.65, 1.14, 39, BLUE_INK)
        self.play(FadeIn(designation), run_time=0.64)
        self.at("left to grow")
        flowers = VGroup(*[blossom(*bud.get_center()[:2], radius=0.43) for bud in buds])
        self.play(FadeOut(rings), run_time=0.33)
        self.play(LaggedStart(*[GrowFromCenter(flower) for flower in flowers], lag_ratio=0.34),
                  run_time=2.48)
        self.at("so broccoli moves")
        drawing = VGroup(*plant().values())
        landed = placed("broccoli", SORTED)
        self.play(FadeOut(designation), FadeOut(flowers), run_time=0.33)
        self.play(FadeIn(drawing), Transform(head, landed, path_arc=-0.17), run_time=1.44)
        self.add(foods_on(GUESSES, "carrot", "potato"), placed("tomato", SORTED))
        self.finish()


class S11TrickCards(TableScene):
    def construct(self):
        drawing = VGroup(*plant().values())
        food_in_place = VGroup(foods_on(GUESSES, "carrot"), foods_on(SORTED, "broccoli", "tomato"))
        tuber = placed("potato", GUESSES)
        detail = food("potato", 3.64, 0.12, 2.83, 0.1)
        twig = VGroup(
            path([(-3.05, -1.73), (-2.77, -0.38), (-2.48, 0.6), (-2.04, 1.72)], BROWN, 10),
            path([(-2.62, 0.15), (-3.13, 0.54), (-3.41, 1.06)], BROWN, 6),
            path([(-2.43, 0.74), (-1.9, 0.88), (-1.62, 1.21)], BROWN, 6),
        )
        twig_buds = VGroup(*[
            ellipse(x, y, 0.2, 0.38, STEM, a)
            for x, y, a in [(-2.04, 1.71, -0.3), (-3.41, 1.08, 0.49),
                            (-1.62, 1.21, -0.57), (-2.79, -0.4, 0.38)]
        ])
        twig.add(twig_buds)
        self.add(sheet(), drawing, food_in_place, tuber)
        self.at("now check the trick")
        self.play(FadeOut(drawing), FadeOut(food_in_place), Transform(tuber, detail, path_arc=0.16),
                  run_time=1.44)
        self.at("look at the potatoes'")
        eye_rings = VGroup(*[outline(eye, BLUE_INK, 0.08) for eye in detail.eyes])
        self.play(LaggedStart(*[Create(ring) for ring in eye_rings], lag_ratio=0.32), run_time=1.62)
        self.at("each eye is a bud")
        comparison = VGroup(tuber, eye_rings)
        self.play(FadeIn(twig, shift=RIGHT * 1.48),
                  comparison.animate.shift(LEFT * 0.79).rotate(0.12), run_time=1.2)
        self.at("like a bud on a stem")
        twig_rings = VGroup(*[outline(bud, BLUE_INK, 0.11) for bud in twig_buds])
        self.play(LaggedStart(*[Create(ring) for ring in twig_rings], lag_ratio=0.35), run_time=1.33)
        self.at("a potato is an")
        title = note("Underground stem", 3.12, 2.32, 34, BLUE_INK)
        self.play(FadeOut(eye_rings), FadeOut(twig_rings), FadeIn(title), run_time=0.49)
        self.play(FadeOut(twig), FadeIn(drawing), FadeIn(food_in_place),
                  Transform(tuber, placed("potato", SORTED), path_arc=-0.23), run_time=1.37)
        self.at("celery is mostly")
        stalk = food("celery", 3.86, -0.02, 4.88, 0.15)
        self.play(FadeOut(title), FadeIn(stalk, shift=UP * 0.69), run_time=1.03)
        self.play(stalk.animate.rotate(-0.11), run_time=1.36)
        self.at("look for the leaves")
        leafy_top = outline(stalk.tips)
        self.play(Create(leafy_top), run_time=0.47)
        self.play(FadeOut(leafy_top), Transform(stalk, placed("celery", SORTED), path_arc=0.12),
                  run_time=1.03)
        self.finish()


class S12Jobs(TableScene):
    def construct(self):
        picture = plant()
        produce = foods_on(SORTED)
        self.add(sheet(), VGroup(*picture.values()), produce)
        finger = hand(4.2, -1.2, 1.71, angle=0.46)
        self.at("point to each part")
        self.play(FadeIn(finger, shift=DOWN * 0.46), run_time=0.65)
        self.play(finger.animate.shift(LEFT * 1.26 + UP * 1.74), run_time=1.56)
        self.play(FadeOut(finger), run_time=0.43)
        last = None
        for cue, name, job, color, duration, badge_y in [
            ("roots take in", "root", "Water in", WATER, 1.4, -0.85),
            ("stems hold the plant", "stem", "Holds up", LIGHT_LEAF, 1.4, -0.85),
            ("leaves make food", "leaf", "Makes food", LIGHT_LEAF, 1.52, -0.85),
            ("flowers make seeds", "flower", "Makes seeds", FLOWER, 0.66, -0.45),
            ("and the fruit holds", "fruit", "Holds seeds", CARROT, 0.77, -1.25),
        ]:
            self.at(cue)
            part = picture[name]
            halo = part.copy().set_stroke(color, width=15, opacity=0.84).set_fill(opacity=0)
            badge = note(job, 4.36, badge_y, 32, BLUE_INK)
            if last is None:
                self.play(FadeIn(badge), run_time=0.32)
            elif name == "fruit":
                self.play(FadeOut(last[0]), FadeIn(badge), run_time=0.32)
            else:
                self.play(FadeOut(last[0]), swap(last[1], badge), run_time=0.32)
            self.play(Create(halo), run_time=duration)
            last = halo, badge
        self.finish()


class S13Safety(TableScene):
    def construct(self):
        drawing = VGroup(*plant().values())
        board = box(3.52, -0.45, 4.04, 3.90, WOOD, 0.36)
        blade = knife().scale(0.9).move_to(pt(3.33, 0.66))
        adult = hand(2.3, -1.95, 1.91, angle=-0.18)
        child = hand(0.58, -2.3, 1.53, child=True, angle=-0.33)
        fruits = VGroup(food("apple", 4.33, -0.53, 1.17), food("carrot", 3.26, -0.61, 1.45, -0.48))
        self.add(sheet(), drawing, board, blade, fruits)
        self.at("stay with your child")
        self.play(FadeIn(adult, shift=DOWN * 0.39), FadeIn(child, shift=DOWN * 0.37), run_time=0.9)
        self.play(child.animate.shift(UP * 0.49), adult.animate.shift(UP * 0.25), run_time=1.65)
        self.at("you do all the cutting")
        self.play(adult.animate.move_to(pt(1.89, 0.42)), run_time=0.94)
        self.at("put the knife away")
        self.play(FadeOut(adult, shift=UP * 1.2), FadeOut(blade, shift=UP * 1.2), run_time=0.77)
        self.at("tasting is optional")
        sort_only = note("Sort only", -3.82, 2.19, 39, BLUE_INK)
        self.play(FadeIn(sort_only), child.animate.shift(LEFT * 1.04), run_time=0.76)
        self.at("check allergies first")
        check = boxed_label("Check allergies", SAFETY_INK, size=33, pad=0.23).move_to(pt(3.52, 2.25))
        self.play(FadeIn(check), run_time=0.54)
        self.at("cut small pieces")
        plate = ellipse(3.24, -0.16, 2.93, 2.42, CREAM, stroke="#b98660")
        pieces = VGroup(*[box(x, y, 0.28, 0.24, CARROT, 0.06)
                          for x, y in [(2.93, 0.14), (3.45, 0.22), (3.22, -0.31), (3.58, -0.42)]])
        self.play(FadeOut(fruits), FadeIn(plate), run_time=0.56)
        self.play(LaggedStart(*[FadeIn(piece, shift=DOWN * 0.19) for piece in pieces], lag_ratio=0.19),
                  run_time=1.15)
        self.at("never taste raw potato")
        spud_slice = VGroup(ellipse(3.28, -0.14, 2.1, 1.42, "#b98254"),
                            ellipse(3.28, -0.14, 1.88, 1.2, "#f2d396"))
        slice_no = VGroup(
            Circle(radius=1.09, stroke_color=SAFETY_INK, stroke_width=8).move_to(spud_slice),
            Line(pt(2.51, 0.63), pt(4.05, -0.91), stroke_color=SAFETY_INK, stroke_width=8),
        )
        self.play(FadeOut(check), FadeOut(plate), FadeOut(pieces), FadeIn(spud_slice), run_time=0.51)
        self.play(Create(slice_no), run_time=0.92)
        self.at("wash your hands")
        basin = sink()
        adult = hand(-0.01, -0.5, 2.54, angle=-0.15)
        little = hand(1.7, -0.83, 1.94, child=True, angle=0.24)
        drops = water_drops(0.71, 0.57, "#a3e3e8")
        self.play(*[FadeOut(obj) for obj in (drawing, child, board, sort_only, spud_slice, slice_no)],
                  run_time=0.37)
        self.play(FadeIn(basin), FadeIn(adult, shift=UP * 0.24), FadeIn(drops), run_time=0.55)
        self.play(adult.animate.shift(RIGHT * 0.28), drops.animate.shift(DOWN * 0.53), run_time=0.62)
        self.at("have your child wash")
        self.play(FadeIn(little, shift=LEFT * 0.3), run_time=0.56)
        self.play(little.animate.shift(LEFT * 0.28), adult.animate.shift(LEFT * 0.18),
                  drops.animate.shift(UP * 0.36), run_time=1.11)
        self.finish()


class S14SafetyChoke(TableScene):
    def construct(self):
        plate = ellipse(2.24, -0.05, 5.94, 4.89, CREAM, stroke=WOOD, sw=3)
        risk = note("Under 4:\nchoking risk", -3.18, 0.62, 45, SAFETY_INK)
        peas = food("peas", 0.92, 0.89, 1.03)
        beans = VGroup(*[ellipse(x, y, 0.49, 0.28, "#a34f45", a)
                         for x, y, a in [(2.66, 0.91, 0.44), (3.18, 1.16, -0.56), (3.27, 0.69, 0.32)]])
        carrot_chunks = VGroup(*[box(x, y, 0.58, 0.43, CARROT, 0.08).rotate(a)
                                 for x, y, a in [(1.16, -0.58, 0.26), (0.87, -1.04, -0.33), (1.49, -1, 0.3)]])
        apple_chunks = VGroup(*[
            VGroup(box(x, y, 0.55, 0.47, "#eed19c", 0.07),
                   box(x, y - 0.19, 0.51, 0.1, RED_FRUIT, 0.04)).rotate(a)
            for x, y, a in [(2.84, -0.54, 0.5), (3.04, -1.03, -0.37), (3.47, -0.76, 0.23)]
        ])
        pieces = VGroup(carrot_chunks, apple_chunks)
        platter = VGroup(plate, pieces).shift(LEFT * 0.92)
        self.add(sheet(), platter)
        self.at("keep small food pieces")
        self.play(platter.animate.shift(RIGHT * 0.92), run_time=1.83)
        self.at("children under four")
        self.play(FadeIn(risk, shift=UP * 0.28), run_time=1.0)
        self.at("whole peas")
        self.play(FadeIn(peas, shift=DOWN * 0.43), run_time=0.48)
        self.at("beans and hard chunks")
        self.play(FadeIn(beans, shift=DOWN * 0.37), run_time=0.61)
        self.at("hard chunks of raw")
        self.play(pieces.animate.shift(UP * 0.38).scale(1.12), run_time=1.38)
        self.at("are choking hazards")
        self.play(plate.animate.scale(1.052), run_time=0.77)
        self.at("call 911")
        mobile = phone().scale(1.13).move_to(pt(2.0, 0))
        warning = note("Choking:\ncall 911", -2.95, 0.5, 49, SAFETY_INK)
        self.play(FadeOut(plate), FadeOut(pieces), FadeOut(peas), FadeOut(beans), FadeOut(risk), run_time=0.34)
        self.play(FadeIn(mobile, shift=LEFT * 0.5), FadeIn(warning), run_time=0.84)
        self.play(mobile.animate.rotate(-0.1), run_time=0.79)
        self.finish()


class S15Return(TableScene):
    def construct(self):
        drawing = plant()
        produce = foods_on(SORTED)
        question = question_card("Which part\nis a carrot?", y=2.09, color=INK, left=2.15, size=41, max_w=3.8)
        original = produce[0]
        self.add(sheet(), VGroup(*drawing.values()), produce)
        self.at("end by asking")
        self.play(FadeIn(question, shift=UP * 0.15), run_time=0.86)
        self.at("is a carrot and")
        detail = food("carrot", 4.4, -0.91, 3.53, -0.12)
        self.play(TransformFromCopy(original, detail, path_arc=-0.18), run_time=1.66)
        self.at("if your child is unsure")
        mark = outline(original, BLUE_INK)
        self.play(Create(mark), run_time=1.33)
        self.at("go back to the drawing")
        self.play(FadeOut(question), FadeOut(mark),
                  detail.animate.move_to(pt(3.9, -0.89)), run_time=1.33)
        self.at("check the carrot together")
        soil = drawing["soil"].copy().set_stroke(width=6, opacity=0.8)
        self.play(Create(soil), run_time=0.94)
        self.at("the root holds")
        badge = note("Root", 3.87, 1.54, 40, BLUE_INK)
        anchors = drawing["root"].copy().set_stroke(CARROT, width=5)
        self.play(FadeIn(badge), Create(anchors), run_time=1.09)
        self.at("takes in water")
        drops = water_drops(0.55, -2.63)
        self.play(FadeIn(drops), run_time=0.37)
        self.play(drops.animate.shift(LEFT * 0.63 + UP * 0.42), run_time=0.94)
        self.finish()


class S16End(EndCard):
    LINE = "Every plant food comes from a plant part with a job."
