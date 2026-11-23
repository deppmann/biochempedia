"""A continuous overhead tabletop for the parent guide."""
from bp_parts import *

# COLOR MAP (shared template): TEAL materials, GOLD setup and sorting, GREEN
# observations, RED safety, BLUE water. The specimens retain their own colors.
TABLE = "#271C20"
TRAY_EDGE = "#916E62"
TRAY = "#564047"
PAPER = "#F5DFB8"
CARD_BACK = "#356D75"
PLUM = "#C888A8"
FUR = "#C38657"
SHELL = "#F3D9B8"
SKIN = "#E6A37F"
FISH = "#65AAA2"
DARK_INK = "#30202B"
FOAM = "#DCF6F7"

FEATHER_AT = (-3.75, 0.55)
FUR_AT = (-0.65, 0.55)
SHELL_AT = (2.28, 0.55)
PLATE_AT = (5.25, -1.55)
DECK_AT = (4.95, 1.2)
QUESTION = "Same covering group?"
QUESTION_STYLE = dict(y=3.02, size=44)


def point(x, y):
    return np.array([x, y, 0.0])


def at_pos(mob, xy):
    return mob.move_to(point(*xy))


def tile(w, h, color, radius=0.18, opacity=1):
    return RoundedRectangle(
        width=w, height=h, corner_radius=radius, fill_color=color,
        fill_opacity=opacity, stroke_width=0,
    )


def oval(w, h, color, x=0, y=0, angle=0):
    return at_pos(Ellipse(width=w, height=h, stroke_width=0,
                          fill_color=color, fill_opacity=1).rotate(angle), (x, y))


def silhouette(vertices, color, smooth=True):
    path = VMobject(fill_color=color, fill_opacity=1, stroke_width=0)
    points = [point(*xy) for xy in (*vertices, vertices[0])]
    if smooth:
        path.set_points_smoothly(points)
    else:
        path.set_points_as_corners(points)
    return path


def ink_path(vertices, color, width=3):
    return VMobject(stroke_color=color, stroke_width=width).set_points_smoothly(
        [point(*xy) for xy in vertices]
    )


def table():
    surface = Rectangle(width=16, height=10, stroke_width=0,
                        fill_color=TABLE, fill_opacity=1)
    grain = VGroup(*[
        Line(point(x, y), point(x + 0.64, y + 0.10), color="#38282B", stroke_width=2)
        for x in (-6.78, 6.08) for y in (-3.45, -2.75, -1.55, -0.24, 1.1, 2.1, 3.38)
    ])
    rim = at_pos(tile(9.65, 5.18, TRAY_EDGE, 0.39), (-1.15, -0.02))
    bed = at_pos(tile(9.38, 4.92, TRAY, 0.32), (-1.15, -0.02))
    return VGroup(surface, grain, rim, bed)


def feather(xy=FEATHER_AT, height=2.45, spread=0):
    """Layered barbs part on one edge and return to the same shaft."""
    barbs = VGroup()
    for side in (-1, 1):
        for i in range(20):
            s = i / 19
            y = -1.38 + 2.72 * s
            x = 0.17 * s - 0.18 * s * s
            width = (0.08 + 0.74 * np.sin(PI * s) ** 0.62) * (1.06 if side < 0 else 0.83)
            lift = spread * side * np.exp(-((s - 0.55) / 0.17) ** 2)
            color = ("#F6D6A2", "#E3A876", "#EEC08D")[i % 3] if side < 0 else ("#CA8B80", "#D99C86", "#E7AE90")[i % 3]
            barbs.add(ink_path([(x, y), (x + side * width * 0.55, y + 0.18 + lift * 0.3),
                                (x + side * width, y + 0.4 + lift)], color, 5))
    shaft = ink_path([(-0.12, -1.86), (-0.01, -0.89), (0.02, 0.36),
                      (-0.01, 1.72)], PAPER, 4)
    return at_pos(VGroup(barbs, shaft).rotate(-26 * DEGREES).set_height(height), xy)


def feather_hooks(gap):
    """Two neighboring barbs and the shorter branches that join their edges."""
    picture = VGroup()
    for side, color in [(-1, "#F6D6A2"), (1, "#DF9F8E")]:
        y = side * (0.58 + gap / 2)
        picture.add(ink_path([(-1.22, y - 0.36), (0, y), (1.24, y + 0.36)], color, 9))
        for x in np.linspace(-0.98, 0.78, 6):
            base = y + x * 0.29
            tip = base - side * 0.67
            picture.add(ink_path([(x, base), (x + 0.14, base - side * 0.34),
                                  (x + 0.26, tip), (x + 0.35, tip + side * 0.10)],
                                 color, 4))
    return picture.shift(RIGHT * 0.86)


def fur(xy=FUR_AT, height=2.15):
    patch = silhouette([(-1.15, -0.7), (-1.14, 0.73), (-0.48, 1.04), (0.73, 0.95),
                        (1.18, 0.37), (1.03, -0.81), (0.01, -1.03)], FUR)
    hairs = VGroup()
    for row in range(6):
        for col in range(8):
            x = -0.87 + col * 0.24 + 0.06 * (row % 2)
            y = -0.78 + row * 0.28
            hairs.add(ink_path([(x - 0.1, y - 0.08), (x, y), (x + 0.11, y + 0.19)],
                               ("#F1C18B", "#A76452", "#DEA16D")[(col + 2 * row) % 3], 3))
    return at_pos(VGroup(patch, hairs).rotate(8 * DEGREES).set_height(height), xy)


def shell(xy=SHELL_AT, height=1.85):
    hinge = (0, -0.77)
    fan = [(1.08 * np.cos(a), 0.83 * np.sin(a) + 0.05)
           for a in np.linspace(0.17, PI - 0.17, 13)]
    lip = silhouette([hinge, (0.63, -0.52), *fan, (-0.64, -0.5)], SHELL)
    ribs = VGroup(*[
        ink_path([hinge, (x * 0.56, y * 0.45 - 0.38), (x * 0.92, y * 0.92)],
                 "#AB653F" if i % 2 == 0 else "#C08B65", 3)
        for i, (x, y) in enumerate(fan[1:-1])
    ])
    return at_pos(VGroup(lip, ribs).rotate(-13 * DEGREES).set_height(height), xy)


def scale_skin():
    base = silhouette([(-1.24, 0.39), (-0.74, 0.76), (1.25, 0.43),
                       (1.03, -0.45), (-0.95, -0.65)], FISH)
    scales = VGroup()
    for row, count in enumerate((4, 5, 5, 4)):
        for col in range(count):
            x = -0.95 + col * 0.37 + (0.16 if count == 4 else 0)
            y = -0.42 + row * 0.30
            scales.add(ink_path([(x, y - 0.13), (x + 0.20, y), (x, y + 0.13)],
                                "#2B605D", 3.4))
    return VGroup(base, scales)


def fish_plate(xy=PLATE_AT, width=2.45):
    plate = VGroup(oval(2.85, 2.2, "#D1C4CE"), oval(2.58, 1.94, "#F8EADC"))
    return at_pos(VGroup(plate, scale_skin().set_width(2.05)).set_width(width), xy)


def sample_set():
    return VGroup(feather(), fur(), shell())


def card_base(back=False):
    return tile(2.05, 2.65, CARD_BACK if back else PAPER)


def card_back(xy, height=2.65):
    deco = VGroup(tile(1.77, 2.37, "#40858C"), tile(0.84, 0.84, "#65A1A0"))
    deco[1].rotate(PI / 4)
    return at_pos(VGroup(card_base(True), deco).set_height(height), xy)


def stack(xy=DECK_AT, height=2.05):
    x, y = xy
    return VGroup(*[
        card_back((x + 0.10 * i, y + 0.10 * i), height).rotate(i * 4 * DEGREES)
        for i in (2, 1, 0)
    ])


def bat():
    wing = [(0.06, 0.19), (0.38, 0.45), (0.91, 0.59), (0.82, 0.14),
            (0.87, -0.21), (0.57, -0.09), (0.48, -0.36), (0.26, -0.25),
            (0.10, -0.47)]
    wings = VGroup(silhouette(wing, "#744F76", False),
                   silhouette([(-x, y) for x, y in wing], "#744F76", False))
    body = VGroup(oval(0.47, 0.76, FUR, y=-0.10), oval(0.43, 0.39, FUR, y=0.34),
                  silhouette([(-0.22, 0.43), (-0.18, 0.70), (-0.02, 0.44)], FUR, False),
                  silhouette([(0.02, 0.44), (0.18, 0.70), (0.22, 0.43)], FUR, False),
                  Dot(point(-0.08, 0.37), 0.03, color=DARK_INK),
                  Dot(point(0.08, 0.37), 0.03, color=DARK_INK))
    feet = VGroup(*[
        ink_path([(x, -0.40), (x, -0.53), (x * 1.65, -0.57)], "#99563F", 5)
        for x in (-0.10, 0.10)
    ])
    art = VGroup(wings, feet, body)
    art.covering = body
    return art


def penguin():
    body = VGroup(oval(0.94, 1.45, DARK_INK), oval(0.66, 0.96, "#FFF5E2", y=-0.14),
                  oval(0.66, 0.56, DARK_INK, y=0.57), oval(0.12, 0.13, TEXT, x=0.14, y=0.62),
                  silhouette([(0.23, 0.56), (0.55, 0.51), (0.25, 0.42)], FUR, False),
                  oval(0.28, 0.13, FUR, x=-0.23, y=-0.69),
                  oval(0.28, 0.13, FUR, x=0.23, y=-0.69))
    flippers = VGroup(oval(0.24, 0.86, DARK_INK, x=-0.42, angle=-0.35),
                      oval(0.21, 0.82, DARK_INK, x=0.43, angle=0.33))
    art = VGroup(flippers, body)
    art.covering = body[1]
    return art


def dog():
    legs = VGroup(*[
        oval(0.17, length, color, x=x, y=-0.26, angle=angle)
        for x, angle, length, color in [
            (-0.34, 0.14, 0.57, "#A56049"), (0.23, -0.12, 0.57, "#A56049"),
            (-0.58, 0.19, 0.68, FUR), (0.48, -0.14, 0.68, FUR),
        ]
    ])
    tail = ink_path([(-0.62, 0.18), (-0.80, 0.28), (-1.03, 0.55)], FUR, 7)
    return VGroup(legs, tail, oval(1.43, 0.64, FUR, y=0.03),
                  oval(0.56, 0.60, FUR, x=0.58, y=0.29),
                  oval(0.32, 0.23, FUR, x=0.86, y=0.22),
                  oval(0.19, 0.42, "#99563F", x=0.46, y=0.40, angle=-0.4),
                  Dot(point(0.71, 0.41), 0.036, color=DARK_INK))


def snake():
    body = ink_path([(-0.93, -0.33), (-0.68, 0.28), (-0.17, 0.29),
                     (0.03, -0.20), (0.39, -0.31), (0.70, 0.13)], "#54794B", 18)
    return VGroup(body, oval(0.42, 0.29, "#54794B", x=0.78, y=0.16),
                  Dot(point(0.87, 0.21), 0.033, color=DARK_INK))


def fish():
    fins = VGroup(
        silhouette([(-0.55, 0), (-1.06, 0.37), (-1.04, -0.39)], "#39776F", False),
        silhouette([(-0.31, 0.26), (0.05, 0.57), (0.24, 0.22)], "#39776F", False),
        silhouette([(0.18, -0.15), (-0.12, -0.51), (-0.26, -0.14)], "#39776F", False),
    )
    return VGroup(fins, oval(1.56, 0.77, FISH, x=0.05),
                  Dot(point(0.54, 0.10), 0.049, color=DARK_INK))


ANIMALS = {"Dog": dog, "Snake": snake, "Bat": bat, "Fish": fish, "Penguin": penguin}


def animal_card(name, xy, height=2.65):
    body = ANIMALS[name]()
    body.scale(min(1.65 / body.width, 1.63 / body.height)).move_to(UP * 0.12)
    card = VGroup(card_base(), body).set_height(height)
    card.art = body
    return at_pos(card, xy)


def photo_card(xy, height=2.6):
    return at_pos(VGroup(card_base(), scale_skin().set_width(1.76)).set_height(height), xy)


def card_fan():
    return VGroup(*[
        animal_card(name, (4.75 + 0.36 * i, 0.4 + 0.40 * i), 2.05)
        .rotate((-16 + i * 14) * DEGREES)
        for i, name in enumerate(("Dog", "Fish", "Penguin"))
    ])


def dropper(xy, height=2.05):
    bulb = oval(0.50, 0.69, TEAL, y=0.66)
    tube = at_pos(tile(0.25, 1.18, "#E4E1DC", 0.10), (0, -0.10))
    water = at_pos(tile(0.12, 0.67, BLUE, 0.05), (0, -0.29))
    tip = silhouette([(-0.10, -0.56), (0.10, -0.56), (0, -0.95)], "#E4E1DC", False)
    return at_pos(VGroup(bulb, tube, water, tip).set_height(height), xy)


def water_cup(xy):
    return at_pos(VGroup(oval(1.63, 1.55, "#D5E1E1"), oval(1.44, 1.35, "#377888"),
                         oval(1.23, 1.15, BLUE), oval(0.54, 0.15, FOAM, x=-0.22, y=0.28,
                                                     angle=0.16)), xy)


def water_drop(xy, radius=0.16, bead=False):
    shape = oval(2 * radius, 1.6 * radius, BLUE) if bead else silhouette(
        [(0, 1.6 * radius), (radius, -0.15 * radius), (0, -radius),
         (-radius, -0.15 * radius)], BLUE,
    )
    glint = oval(radius * 0.44, radius * 0.32, FOAM, x=-radius * 0.32, y=radius * 0.19)
    return at_pos(VGroup(shape, glint), xy)


def hand(xy, height=2.65, pointing=False):
    palm = oval(0.93, 1.18, SKIN, y=-0.23)
    wrist = at_pos(tile(0.63, 0.65, SKIN, 0.11), (0.02, -0.82))
    thumb = oval(0.32, 0.75, SKIN, x=-0.49, y=-0.16, angle=0.62)
    fingers = VGroup()
    for i, length in enumerate((1.23, 1.44, 1.33, 1.05)):
        if pointing:
            length = 1.75 if i == 0 else 0.62
        fingers.add(at_pos(tile(0.24, length, SKIN, 0.11),
                           (-0.33 + i * 0.24, 0.06 + length / 2 - 0.3)))
    return at_pos(VGroup(wrist, palm, thumb, fingers).set_height(height), xy)


def pencil(xy):
    return at_pos(VGroup(tile(0.18, 1.23, GOLD, 0.06),
                         silhouette([(-0.09, -0.6), (0.09, -0.6), (0, -0.93)],
                                    PAPER, False)).rotate(-35 * DEGREES), xy)


def trace_arrow(x, y, length=1.22, reverse=False):
    delta = -1 if reverse else 1
    return Arrow(point(x, y), point(x + delta * length, y), buff=0, color=GOLD, stroke_width=6)


def sort_label(words):
    return caption(words, size=36, color=GOLD, y=-3.16).move_to(DOWN * 3.16)


def top_label(words, color=GOLD):
    return T(words, 36, color, weight=BOLD).move_to(UP * 3.11)


def flip(scene, old, new, seconds=0.68):
    """Turn each card around its own vertical centerline."""
    thin = 0.035
    scene.play(*[card.animate.stretch(thin, 0) for card in old],
               run_time=seconds * 0.45, rate_func=linear)
    scene.remove(old, *old)
    for card in new:
        card.stretch(thin, 0)
    scene.add(new)
    scene.play(*[card.animate.stretch(1 / thin, 0) for card in new],
               run_time=seconds * 0.55, rate_func=linear)


def eye_and_hand():
    eye = VGroup(oval(1.7, 0.72, PAPER, x=-0.58, y=0.38),
                 oval(0.53, 0.53, TEAL, x=-0.58, y=0.38),
                 oval(0.20, 0.20, DARK_INK, x=-0.58, y=0.38))
    return VGroup(eye, hand((0.53, -0.31), 1.48).rotate(-24 * DEGREES))


def check_drop():
    tick = VMobject(stroke_color=GREEN, stroke_width=8).set_points_as_corners(
        [point(0.05, -0.23), point(0.33, -0.53), point(0.95, 0.2)]
    )
    return VGroup(water_drop((-0.28, 0.20), 0.58), tick)


def badge_picture(icon, x):
    return at_pos(VGroup(oval(2.48, 2.40, "#77565B"), icon.move_to(ORIGIN)), (x, 0.52))


def fridge(xy):
    case = tile(2.48, 4.58, "#D5D3C8", 0.24)
    top = at_pos(tile(2.16, 1.26, "#8DB5B0"), (0, 1.44))
    lower = at_pos(tile(2.16, 2.65, "#65988F"), (0, -0.61))
    handles = VGroup(at_pos(tile(0.14, 0.56, TEXT, 0.06), (-0.79, 1.44)),
                     at_pos(tile(0.15, 0.72, TEXT, 0.06), (-0.79, -0.25)))
    return at_pos(VGroup(case, top, lower, handles), xy)


def clock_face(xy):
    clock = VGroup(oval(2.42, 2.42, "#B49786"), oval(2.13, 2.13, PAPER))
    for k in range(12):
        a = PI / 2 - k * TAU / 12
        v = point(np.cos(a), np.sin(a))
        clock.add(Line(v * 0.86, v * 0.98, color=DARK_INK, stroke_width=2.5))
    clock.add(Line(ORIGIN, UP * 0.78, color=DARK_INK, stroke_width=4.5))
    clock.hour = Line(ORIGIN, UP * 0.60, color="#9A4441", stroke_width=7)
    clock.add(clock.hour, Dot(radius=0.07, color=DARK_INK))
    return at_pos(clock, xy)


def bin_icon(xy):
    bucket = silhouette([(-0.95, 0.65), (0.95, 0.65), (0.69, -1.5),
                         (-0.69, -1.5)], "#607784", False)
    lid = VGroup(at_pos(tile(2.16, 0.24, "#A4B2B7"), (0, 0.79)),
                 at_pos(tile(0.57, 0.26, "#A4B2B7"), (0, 1.0)))
    icon = at_pos(VGroup(bucket, lid), xy)
    icon.lid = lid
    return icon


def wash_picture():
    basin = VGroup(oval(5.7, 4.65, "#708E95", y=-0.14), oval(5.30, 4.18, "#35535F", y=-0.14))
    tap = ink_path([(0, 1.08), (0.02, 1.62), (-0.13, 1.84),
                    (-0.62, 1.81), (-0.65, 1.44)], "#B6CFD1", 15)
    hands = VGroup(hand((-0.67, -0.28), 2.26).rotate(-56 * DEGREES),
                   hand((0.70, -0.57), 2.26).rotate(65 * DEGREES))
    bubbles = VGroup(*[
        Circle(radius=r, stroke_width=3, stroke_color=FOAM,
               fill_color=BLUE, fill_opacity=0.25).move_to(point(x, y))
        for x, y, r in [(-0.63, 0.03, .15), (-0.29, .37, .20), (0.07, .14, .25),
                        (0.59, .39, .13), (0.39, -.34, .17), (-0.37, -.30, .12)]
    ])
    drops = VGroup(*[water_drop((-0.66 + dx, y), 0.10)
                     for dx, y in [(0, 1.11), (0.06, 0.79), (-0.04, 0.50)]])
    return VGroup(basin, tap, hands, drops, bubbles), hands, drops, bubbles


def scrub(scene, hands, drops, bubbles, seconds):
    left, right = hands
    scene.play(
        left.animate.shift(RIGHT * 0.58 + UP * 0.27),
        right.animate.shift(LEFT * 0.51 + DOWN * 0.32),
        drops.animate.shift(DOWN * 0.35),
        bubbles.animate.shift(UP * 0.55).scale(1.2),
        run_time=seconds, rate_func=there_and_back,
    )


class S01Hook(SpokenScene, TitleCard):
    TITLE = "Fur, Feathers and Scales: Parent Guide"
    LESSON = "Fur, Feathers and Scales"

    def construct(self):
        sample = feather((-1.6, 0.13), 4.55)
        self.add(table(), sample)
        self.at("smooth one way")
        arrow = trace_arrow(0, 0).rotate(64 * DEGREES).move_to(point(-2.77, -1.18))
        self.play(GrowArrow(arrow), run_time=0.32)
        self.play(arrow.animate.shift(UP * 0.90 + RIGHT * 0.42), run_time=0.64)
        self.at("rough the other")
        back = trace_arrow(0, 0, reverse=True).rotate(64 * DEGREES).move_to(arrow)
        self.play(Transform(arrow, back), run_time=0.22)
        self.play(arrow.animate.shift(DOWN * 0.90 + LEFT * 0.42),
                  Transform(sample, feather((-1.6, 0.13), 4.55, 1.12)), run_time=0.68)
        self.play(FadeOut(arrow), run_time=0.38)
        self.at("fish scales can")
        detail = photo_card((2.12, 0.20), 3.75)
        self.play(Transform(sample, feather((-3.25, 0.18), 3.22, 0)),
                  FadeIn(detail, shift=LEFT * 0.40), run_time=0.66)
        sheen = trace_arrow(0.77, -0.66, 1.38)
        self.play(GrowArrow(sheen), run_time=0.38)
        self.play(sheen.animate.shift(UP * 0.45), rate_func=there_and_back, run_time=0.90)
        self.play(FadeOut(sheen), run_time=0.25)
        self.at("at the kitchen table")
        title = fit_text(self.TITLE, max_w=11.6, size=42, min_size=32,
                         font=TITLE_FONT, weight=BOLD).move_to(UP * 3.17)
        self.play(FadeIn(title), run_time=0.27)
        self.wait(1.02)
        self.play(FadeOut(title), run_time=0.26)
        self.at("compare animal coverings")
        tuft = fur((-0.72, 0.12), 2.02)
        self.play(FadeIn(tuft, shift=UP * 0.3), run_time=0.70)
        self.at("use what they notice")
        fan = card_fan()
        self.play(LaggedStart(*[FadeIn(c, shift=RIGHT * 0.5) for c in fan], lag_ratio=0.30),
                  run_time=1.65)
        self.finish()


class S02Payoff(SpokenScene):
    def construct(self):
        samples = VGroup(feather((-3.25, 0.18), 3.22), fur((-0.72, 0.12), 2.02),
                         photo_card((2.12, 0.20), 3.75), card_fan())
        self.add(table(), samples)
        self.at("practice looking closely")
        look = badge_picture(eye_and_hand(), -4.10)
        self.play(FadeOut(samples[:3]), FadeIn(look, shift=UP * 0.3), run_time=1.02)
        first = at_pos(T("Look & feel", 33, PAPER), (-4.10, -1.20))
        self.at("describing what")
        self.play(FadeIn(first, shift=UP * 0.15), run_time=0.55)
        self.play(look[1][1].animate.rotate(-0.18).shift(UP * 0.27), run_time=1.38,
                  rate_func=there_and_back)
        self.at("they make a guess")
        test = badge_picture(check_drop(), -1.12)
        self.play(FadeIn(test, shift=DOWN * 0.36), run_time=0.72)
        self.at("test it with water")
        second = at_pos(T("Guess & test", 33, PAPER), (-1.12, -1.20))
        self.play(FadeIn(second), test[1][0].animate.shift(DOWN * 0.24), run_time=0.63)
        self.at("sort animal pictures")
        cards = samples[3]
        sorted_cards = VGroup(*[
            stack((0.89 + i * 0.73, 0.42), 0.92) for i in range(3)
        ])
        sort = badge_picture(sorted_cards, 1.86)
        self.add(sort[0])
        self.bring_to_front(*cards)
        self.play(*[Transform(c, dest) for c, dest in zip(cards, sorted_cards)], run_time=1.48)
        third = at_pos(T("Sort by rule", 33, PAPER), (1.86, -1.20))
        self.play(FadeIn(third), run_time=0.50)
        self.at("formal group names")
        sorting_badge = sort[0]
        self.play(sorting_badge.animate.scale(1.06),
                  cards[0].animate.shift(UP * 0.28).rotate(0.09),
                  cards[1].animate.shift(UP * 0.38),
                  cards[2].animate.shift(UP * 0.28).rotate(-0.09),
                  run_time=2.40, rate_func=there_and_back)
        self.finish()


class S03Gather(SpokenScene):
    def construct(self):
        feathers = VGroup(feather((-4.40, 0.42), 2.3), feather((-3.78, 0.58), 2.6),
                          feather((-3.18, 0.43), 2.14))
        tuft = fur()
        shells = VGroup(shell((1.55, 0.66), 1.57), shell((2.40, 0.41), 1.34))
        self.add(table())
        self.at("set out")
        self.play(LaggedStart(*[FadeIn(f, shift=DOWN * 0.5) for f in feathers], lag_ratio=0.35),
                  run_time=1.74)
        self.at("fake fur")
        self.play(FadeIn(tuft, shift=DOWN * 0.50), run_time=0.60)
        self.at("two or three")
        self.play(LaggedStart(*[FadeIn(s, shift=UP * 0.40) for s in shells], lag_ratio=0.40),
                  run_time=1.40)
        self.at("add a cup")
        cup = water_cup((4.84, 1.55))
        self.play(FadeIn(cup, shift=LEFT * 0.48), run_time=0.70)
        self.at("a dropper")
        pipette = dropper((5.99, 0.55), 1.70).rotate(-18 * DEGREES)
        self.play(FadeIn(pipette, shift=DOWN * 0.35), run_time=0.65)
        self.at("if you use")
        sample = at_pos(scale_skin(), (4.87, -1.22))
        self.play(FadeIn(sample, shift=LEFT * 0.50), run_time=1.10)
        self.at("skin and scales")
        self.play(sample.animate.scale(1.17), run_time=1.42, rate_func=there_and_back)
        self.at("put it on")
        plate = fish_plate()
        self.play(FadeOut(sample), FadeIn(plate, shift=DOWN * 0.40), run_time=0.67)
        self.at("12 to 16")
        self.play(cup.animate.move_to(point(1.55, -1.42)),
                  pipette.animate.move_to(point(2.80, -1.48)),
                  FadeIn(stack(), shift=LEFT * 0.65), run_time=1.94)
        self.finish()


class S04Safety(SpokenScene):
    def construct(self):
        specimens = sample_set()
        plate = fish_plate()
        adult = hand((4.75, -0.58), 2.28, pointing=True).rotate(PI)
        self.add(table(), specimens, plate, stack())
        self.at("stay with your child")
        self.play(FadeIn(adult, shift=LEFT * 0.50), run_time=1.35)
        self.at("handle raw fish")
        handle = top_label("Adults handle tools and fish", RED)
        self.play(FadeIn(handle), adult.animate.shift(DOWN * 0.39), run_time=1.10)
        shears = VGroup(
            *[oval(0.32, 0.49, RED, x=x, y=-0.27) for x in [-0.19, 0.19]],
            Line(point(-0.18, -0.12), point(0.28, 0.56), color=TEXT, stroke_width=5),
            Line(point(0.18, -0.12), point(-0.29, 0.56), color=TEXT, stroke_width=5),
        ).scale(1.42).move_to(point(-1.15, -1.58))
        self.at("scissors")
        self.play(FadeIn(shears, shift=UP * 0.25), run_time=0.49)
        lens = VGroup(Circle(radius=0.44, color=TEAL, stroke_width=7),
                      Line(point(0.29, -0.34), point(0.65, -0.72), color=TEAL, stroke_width=10))
        at_pos(lens, (0.74, -1.50))
        self.at("glass magnifiers")
        self.play(FadeIn(lens, shift=UP * 0.23), run_time=0.62)
        self.at("check shells")
        self.play(FadeOut(handle), FadeOut(shears), FadeOut(lens),
                  adult.animate.move_to(point(3.35, 0.93)).rotate(-0.92), run_time=1.10)
        self.play(adult.animate.shift(LEFT * 0.38), run_time=0.67, rate_func=there_and_back)
        self.at("use only craft")
        craft = top_label("Craft-store feathers only", GREEN)
        self.play(FadeIn(craft), adult.animate.move_to(point(-3.12, 1.53)).rotate(0.70),
                  run_time=1.22)
        self.at("leave wild feathers")
        self.play(adult.animate.move_to(point(-5.0, 0.70)).rotate(-0.55),
                  run_time=1.76, rate_func=there_and_back)
        self.at("keep small shells")
        small = VGroup(shell((1.1, -1.30), 0.73), feather((-0.35, -1.28), 1.02),
                       oval(0.31, 0.52, TEAL, x=-1.42, y=-1.30))
        caution = top_label("Small parts out of reach", RED)
        self.play(FadeOut(craft), FadeOut(adult), FadeOut(specimens),
                  LaggedStart(*[FadeIn(item, shift=DOWN * 0.30) for item in small], lag_ratio=0.55),
                  run_time=2.35)
        self.play(FadeIn(caution), run_time=0.58)
        self.play(FadeOut(small, shift=UP * 1.48), run_time=1.72)
        self.at("call 911")
        emergency = boxed_label("Choking? Call 911", RED, size=54, pad=0.38).move_to(LEFT * 1.12)
        self.play(FadeOut(caution), FadeIn(emergency), run_time=0.47)
        self.at("use photos")
        photo = photo_card(PLATE_AT)
        self.play(FadeOut(emergency), swap(plate, photo), run_time=0.93)
        allergy = top_label("Allergy? Use a photo", TEAL)
        self.play(FadeIn(allergy), photo.animate.move_to(point(-0.85, -0.02)).scale(1.40),
                  run_time=1.56)
        self.finish()


class S05Touch(SpokenScene):
    def construct(self):
        samples = sample_set()
        self.add(table(), samples)
        lead = pencil((-2.70, -0.49))
        self.at("have your child")
        self.play(FadeIn(lead, shift=DL * 0.30), samples[0].animate.shift(DOWN * 0.35),
                  run_time=0.62)
        descriptors = []
        for specimen, (cue, x, description) in zip(samples, [
            ("the feather", -3.75, "Light · smooth"),
            ("fur and shell", -0.65, "Soft · fuzzy"),
            ("two words each", 2.27, "Hard · ridged"),
        ]):
            self.at(cue)
            label = at_pos(T(description, 29, PAPER), (x, -1.52))
            descriptors.append(label)
            self.play(lead.animate.move_to(point(x + 0.98, -0.56)),
                      specimen.animate.move_to(point(x, 0.75)).scale(1.10), Write(label), run_time=0.66)
        self.at("open and smooth")
        macro_at = (-3.80, 0.02)
        macro = feather(macro_at, 4.68, 1.85)
        focal = samples[0]
        inset = at_pos(oval(3.84, 3.62, "#382A32"), (0.86, 0))
        hooks = feather_hooks(gap=0.50)
        self.play(FadeOut(VGroup(lead, *descriptors, samples[1], samples[2])),
                  Transform(focal, macro), FadeIn(inset), FadeIn(hooks), run_time=0.56)
        self.play(Transform(focal, feather(macro_at, 4.68)),
                  Transform(hooks, feather_hooks(gap=0.0)), run_time=1.32)
        self.at("if you're using")
        closeup = fish_plate((-1.0, 0.0), 5.8)
        adult = hand((2.72, -0.48), 2.40, pointing=True).rotate(PI / 2)
        self.play(FadeOut(VGroup(focal, inset, hooks)), FadeIn(closeup), run_time=0.68)
        self.play(FadeIn(adult, shift=LEFT * 0.40), run_time=0.83)
        no_cuts = top_label("Hands free of cuts or sores", RED)
        self.at("no cuts or sores")
        self.play(FadeIn(no_cuts), adult.animate.shift(LEFT * 0.52), run_time=0.88)
        self.at("stroke it both ways")
        self.play(adult.animate.shift(LEFT * 2.5), run_time=0.57)
        self.play(adult.animate.shift(RIGHT * 2.28), run_time=0.63)
        self.at("keep hands away")
        away = top_label("Hands away from faces and mouths", RED)
        self.play(swap(no_cuts, away),
                  adult.animate.shift(RIGHT * 0.72 + DOWN * 0.78), run_time=1.22)
        self.at("wash your hands")
        wash, hands, drops, bubbles = wash_picture()
        self.play(FadeOut(VGroup(away, adult, closeup)), FadeIn(wash), run_time=0.62)
        self.play(FadeIn(top_label("Wash right away", TEAL)), run_time=0.55)
        scrub(self, hands, drops, bubbles, 2.05)
        scrub(self, hands, drops, bubbles, 2.24)
        self.finish()


class S06WaterTest(SpokenScene):
    def construct(self):
        plume = feather((-3.68, -0.02), 4.03)
        tuft = fur((0.47, -0.06), 3.15)
        pipette = dropper((3.35, 1.13), 1.75).rotate(0.28)
        self.add(table(), plume, tuft)
        self.at("before the water test")
        self.play(FadeIn(pipette, shift=LEFT * 0.50), run_time=0.71)
        self.at("which one will stay")
        self.play(FadeIn(top_label("Guess, then drip")), pipette.animate.move_to(point(-0.72, 1.61)),
                  run_time=1.57)
        self.at("place three drops")
        feather_beads = VGroup()
        fur_beads = VGroup()
        for positions, beads, tempo in [
            ([(-3.27, 0.70), (-3.55, 0.16), (-3.80, -0.37)], feather_beads, 0.28),
            ([(0.02, 0.44), (0.50, 0.16), (0.99, -0.25)], fur_beads, 0.25),
        ]:
            for x, y in positions:
                self.play(pipette.animate.move_to(point(x + 0.12, y + 1.29)), run_time=tempo)
                falling = water_drop((x, y + 0.43), 0.15)
                self.add(falling)
                self.play(Transform(falling, water_drop((x, y), 0.17, bead=True)), run_time=0.2)
                beads.add(falling)
        self.play(FadeOut(pipette), run_time=0.37)
        self.at("water often beads")
        wet_feather = VGroup(plume, feather_beads)
        self.play(wet_feather.animate.scale(1.19).shift(RIGHT * 0.44 + UP * 0.16),
                  run_time=1.19)
        self.play(LaggedStart(*[b.animate.scale(1.40) for b in feather_beads], lag_ratio=0.35),
                  run_time=0.55, rate_func=there_and_back)
        self.at("while fur and craft")
        spots = [oval(0.52, 0.32, "#81513F").move_to(b) for b in fur_beads[1:]]
        self.play(wet_feather.animate.scale(1 / 1.19).shift(LEFT * 0.44 + DOWN * 0.16),
                  tuft.animate.scale(1.14), *[Transform(b, spot) for b, spot in zip(fur_beads[1:], spots)],
                  fur_beads[0].animate.scale(0.82), run_time=1.92)
        self.play(FadeIn(sort_label("Results can vary")), run_time=0.50)
        self.at("each coat fits")
        self.play(wet_feather.animate.shift(UP * 0.28),
                  VGroup(tuft, fur_beads).animate.shift(UP * 0.36),
                  run_time=1.64, rate_func=there_and_back)
        self.finish()


class S07MatchSort(SpokenScene):
    def construct(self):
        names = ("Dog", "Bat", "Snake", "Fish")
        xs = (-4.68, -2.29, 0.08, 2.48)
        cards = VGroup(*[animal_card(name, (x, 0.37), 2.47) for name, x in zip(names, xs)])
        backs = VGroup(*[card_back((x, 0.37), 2.47) for x in xs])
        swatches = VGroup(fur((-3.48, -1.76), 0.94),
                          at_pos(scale_skin().set_width(1.35), (1.28, -1.78)))
        self.add(table(), backs)
        self.at("flip the pictures over")
        flip(self, backs, cards, 0.96)
        self.at("match animals")
        self.play(FadeIn(swatches), cards[0].animate.shift(RIGHT * 0.13 + DOWN * 0.28),
                  cards[1].animate.shift(LEFT * 0.13 + DOWN * 0.28), run_time=0.78)
        self.play(cards[2].animate.shift(RIGHT * 0.13 + DOWN * 0.28),
                  cards[3].animate.shift(LEFT * 0.13 + DOWN * 0.28), run_time=0.78)
        self.at("look for legs")
        feature = top_label("Legs", PAPER)
        wings = top_label("Wings", PAPER)
        fins = top_label("Fins", PAPER)
        tails = top_label("Tails", PAPER)
        self.play(FadeIn(feature), *[card.animate.shift(UP * 0.24) for card in cards],
                  run_time=0.25)
        self.play(Indicate(cards[0].art[0], color=DARK_INK, scale_factor=1.06), run_time=0.50)
        self.at("wings")
        self.play(swap(feature, wings), Indicate(cards[1].art[0], color=DARK_INK, scale_factor=1.06),
                  run_time=0.57)
        self.at("fins")
        self.play(swap(wings, fins), Indicate(cards[3].art[0][1:], color=DARK_INK, scale_factor=1.06),
                  run_time=0.45)
        self.at("and tails")
        self.play(swap(fins, tails), Indicate(cards[3].art[0][0], color=DARK_INK, scale_factor=1.08),
                  run_time=0.54)
        self.play(FadeOut(tails), run_time=0.38)
        self.at("land or in water")
        habitat = top_label("Land or water?", TEAL)
        self.play(FadeIn(habitat), FadeOut(swatches), cards[3].animate.shift(UP * 0.50),
                  run_time=0.86)
        self.at("and how does it move")
        move = top_label("How does it move?", TEAL)
        self.play(swap(habitat, move, run_time=0.30),
                  *[card.art.animate(rate_func=there_and_back, run_time=1.33).shift(offset)
                    for card, offset in zip(cards, (RIGHT * 0.10, UP * 0.24,
                                                    RIGHT * 0.10, RIGHT * 0.10))])
        self.at("sort by covering")
        covering = sort_label("Sort by covering")
        self.play(swap(move, covering, run_time=0.30), FadeIn(swatches),
                  *[card.animate.shift(DOWN * 0.24) for card in cards[:3]],
                  cards[3].animate.shift(DOWN * 0.74), run_time=0.30)
        self.at("then by leg count")
        legs = sort_label("Sort by leg count")
        leg_counts = VGroup(*[at_pos(T(word, 30, PAPER), (x, -1.77)) for word, x in
                               zip(("4 legs", "2 legs", "0 legs"), (-4.78, -2.12, 1.48))])
        self.play(swap(covering, legs), swap(swatches, leg_counts),
                  cards[0].animate.move_to(point(-4.78, 0.18)),
                  cards[1].animate.move_to(point(-2.12, 0.18)),
                  cards[2].animate.move_to(point(0.44, 0.18)),
                  cards[3].animate.move_to(point(2.52, 0.18)), run_time=0.30)
        self.at("then by movement")
        motion = sort_label("Sort by movement")
        actions = VGroup(*[at_pos(T(word, 29, PAPER), (x, -1.78)) for word, x in
                           zip(("Walk", "Fly", "Crawl", "Swim"), (-4.78, -2.12, 0.44, 2.52))])
        self.play(cards[0].art.animate.shift(RIGHT * 0.10 + UP * 0.08),
                  cards[1].art.animate.shift(UP * 0.20),
                  cards[2].art.animate.shift(RIGHT * 0.10),
                  cards[3].art.animate.shift(RIGHT * 0.10 + UP * 0.05),
                  run_time=0.90, rate_func=there_and_back)
        self.play(swap(legs, motion), swap(leg_counts, actions), run_time=0.30)
        self.at("pick a fourth rule")
        self.play(swap(motion, sort_label("Your own rule?")), FadeOut(actions), run_time=0.92)
        self.finish()


def prediction_samples():
    return VGroup(fur((-4.20, 1.22), 1.54), feather((2.38, 1.15), 1.85))


def prediction_cards(back=False):
    positions = ((-1.85, -0.40), (0.64, -0.40))
    if back:
        return VGroup(*[card_back(xy, 2.80) for xy in positions])
    return VGroup(*[animal_card(name, xy, 2.80)
                    for name, xy in zip(("Bat", "Penguin"), positions)])


def prediction_question():
    return question_card(QUESTION, **QUESTION_STYLE)


class S08PredictQ(SpokenScene):
    def construct(self):
        samples = prediction_samples()
        cards = prediction_cards()
        self.add(table(), samples)
        self.at("a bat flies")
        self.play(FadeIn(cards[0], shift=RIGHT * 0.79), run_time=0.67)
        self.at("and a penguin")
        self.play(FadeIn(cards[1], shift=LEFT * 0.77), run_time=0.81)
        self.at("imagine your child sorts")
        self.play(cards[0].animate.rotate(-0.11), cards[1].animate.rotate(0.10),
                  run_time=2.56, rate_func=there_and_back)
        self.at("before you turn")
        backs = prediction_cards(back=True)
        flip(self, cards, backs, 0.88)
        self.play(backs[0].animate.shift(LEFT * 0.30 + DOWN * 0.36),
                  backs[1].animate.shift(DOWN * 0.36), run_time=0.53)
        self.at("predict whether")
        self.play(FadeIn(prediction_question(), shift=UP * 0.22), run_time=0.51)
        self.play(backs[0].animate.shift(RIGHT * 0.30 + UP * 0.36),
                  backs[1].animate.shift(UP * 0.36),
                  run_time=3.12, rate_func=linear)
        self.finish()


class S09PredictPause(Scene):
    def construct(self):
        self.camera.background_color = BG
        self.add(table(), prediction_samples(), prediction_cards(back=True), prediction_question())
        self.wait(4.5)


class S10PredictReveal(SpokenScene):
    def construct(self):
        backs = prediction_cards(back=True)
        cards = prediction_cards()
        samples = prediction_samples()
        question = prediction_question()
        self.add(table(), samples, backs, question)
        self.at("turn the bat")
        flip(self, backs, cards, 0.86)
        self.play(FadeOut(question), run_time=0.54)
        self.at("which one flies")
        self.play(cards[0].art[0].animate.scale(1.14), cards[0].animate.shift(UP * 0.46),
                  run_time=0.95, rate_func=there_and_back)
        self.at("which one has feathers")
        self.play(cards[1].animate.shift(UP * 0.48), run_time=0.98, rate_func=there_and_back)
        self.at("bats have fur")
        bat_ring = SurroundingRectangle(cards[0].art.covering, color=GOLD, corner_radius=0.17,
                                        buff=0.10, stroke_width=5)
        self.play(Create(bat_ring), run_time=0.61)
        self.at("penguins have feathers")
        feather_ring = SurroundingRectangle(cards[1].art.covering, color=GOLD, corner_radius=0.16,
                                            buff=0.08, stroke_width=5)
        self.play(Create(feather_ring), run_time=0.72)
        self.at("put them in different groups")
        self.play(FadeOut(bat_ring), FadeOut(feather_ring), run_time=0.24)
        self.play(cards[0].animate.move_to(point(-4.20, -1.08)),
                  cards[1].animate.move_to(point(2.38, -1.08)), run_time=1.10)
        labels = VGroup(at_pos(T("Fur", 35, PAPER), (-4.20, 3.07)),
                        at_pos(T("Feathers", 35, PAPER), (2.38, 3.07)))
        self.play(LaggedStart(*[FadeIn(label) for label in labels], lag_ratio=0.35), run_time=0.80)
        self.at("the group depends")
        self.play(FadeIn(sort_label("Choose a feature to sort by")),
                  samples[0].animate.shift(UP * 0.16), samples[1].animate.shift(UP * 0.16),
                  run_time=1.38)
        self.finish()


class S11Wrapup(SpokenScene):
    def construct(self):
        plate = fish_plate((-3.28, -0.20), 3.08)
        refrigerator = fridge((2.32, -0.04))
        self.add(table(), plate)
        self.at("wrap and refrigerate")
        wrap = oval(3.16, 2.39, "#C0CDD4").set_fill(opacity=0.73).move_to(plate)
        self.play(FadeIn(wrap, shift=UP * 0.22), run_time=0.40)
        self.play(FadeIn(refrigerator, shift=LEFT * 0.50), run_time=0.40)
        door = VGroup(refrigerator[2], refrigerator[3][1])
        shelf = at_pos(tile(1.93, 2.39, "#425A5A"), (2.32, -0.65))
        self.add(shelf)
        self.bring_to_front(door, plate, wrap)
        self.play(door.animate.stretch(0.26, 0, about_point=door.get_right()),
                  VGroup(plate, wrap).animate.scale(0.49).move_to(point(2.16, -0.57)),
                  run_time=1.00)
        self.at("within two hours")
        clock = clock_face((-2.82, 0.44))
        time = at_pos(T("Within 2 hours", 38, PAPER), (-2.82, -1.44))
        self.play(FadeIn(clock), run_time=0.56)
        self.play(Rotate(clock.hour, -60 * DEGREES, about_point=clock.get_center()),
                  FadeIn(time), run_time=0.78)
        self.bring_to_front(door)
        self.play(door.animate.stretch(1 / 0.26, 0, about_point=door.get_right()),
                  run_time=0.70)
        self.at("if the room is above")
        hot = top_label("Room above 90°F", RED)
        self.play(FadeOut(time), FadeOut(clock), run_time=0.35)
        self.play(FadeIn(hot), run_time=0.53)
        clock = clock_face((-2.82, 0.44))
        self.play(FadeIn(clock, shift=UP * 0.23), run_time=0.80)
        self.at("you have one hour")
        short = at_pos(T("Within 1 hour", 38, PAPER), (-2.82, -1.44))
        self.play(FadeIn(short), Rotate(clock.hour, -30 * DEGREES, about_point=clock.get_center()),
                  run_time=1.30)
        self.at("if it has been out longer")
        trash = bin_icon((2.27, -0.18))
        excess = fish_plate((-2.85, 0.16), 3.03)
        self.play(FadeOut(VGroup(hot, refrigerator, shelf, door, clock, short, plate, wrap)),
                  FadeIn(trash), FadeIn(excess), run_time=0.98)
        self.at("throw it away")
        self.play(trash.lid.animate.shift(UP * 0.58).rotate(0.16), run_time=0.35)
        self.play(excess.animate.move_to(point(1.45, 1.28)).scale(0.51).rotate(-0.18), run_time=0.76)
        self.play(FadeOut(excess[1], shift=DOWN * 0.90 + RIGHT * 0.67),
                  trash.lid.animate.shift(DOWN * 0.58).rotate(-0.16), run_time=0.46)
        self.at("wash hands with soap")
        wash, hands, drops, bubbles = wash_picture()
        self.play(FadeOut(trash), FadeOut(excess[0]), FadeIn(wash), run_time=0.52)
        scrub(self, hands, drops, bubbles, 1.28)
        self.at("20 seconds")
        duration = top_label("20 seconds", TEAL)
        self.play(FadeIn(duration), run_time=0.48)
        scrub(self, hands, drops, bubbles, 0.67)
        self.at("wash the tray")
        sponge = VGroup(tile(2.15, 0.94, GOLD), at_pos(tile(2.15, 0.27, GREEN), (0, -0.35)))
        at_pos(sponge, (-4.43, 0.62))
        self.play(FadeOut(wash), FadeOut(duration), FadeIn(sponge), run_time=0.52)
        suds = VGroup(*[oval(r, r, FOAM, x=x, y=y)
                        for x, y, r in [(-4.35, 0.71, 0.18), (-3.92, 0.38, 0.29),
                                        (-3.26, 0.45, 0.17), (-2.79, 0.16, 0.25),
                                        (-2.24, 0.21, 0.18), (-1.56, -0.04, 0.24)]])
        self.play(sponge.animate.move_to(point(-0.67, -0.05)),
                  LaggedStart(*[GrowFromCenter(s) for s in suds], lag_ratio=0.30), run_time=1.24)
        self.play(sponge.animate.move_to(point(3.94, -0.96)),
                  FadeOut(suds, shift=RIGHT * 0.56), run_time=1.04)
        self.finish()


class S12End(EndCard):
    LINE = "Each animal's covering fits where it lives and how it moves."
