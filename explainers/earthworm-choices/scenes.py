"""Schematic illustrations for What Do Earthworms Like?"""
import os

from bp_parts import *

# COLOR MAP: blue/teal = water and damp paper; sand = dry paper and cardboard;
# pink = earthworms; brown = soil and wood; grey = tray and tools; mint = oxygen.
WORM = "#CB776A"
BAND = "#F5AD98"
SOIL = "#443228"
MOIST_SOIL = "#3B3D36"
WOOD = "#875B40"
CARD = "#AF8660"
PAPER = "#D9BC96"
DAMP = "#87BDC3"
STEEL = "#617788"
TABLE = "#302833"
SKIN = "#E5A680"
OXYGEN = "#D7F3E3"
TRAY_CENTER = np.array([-1.65, 0.1, 0])
TRAY_W, TRAY_H = 8.35, 4.65
LAMP_BASE = np.array([3.75, 1.05, 0])
QUESTION = "Where will most worms go after the swap?"
config.background_color = BG


def p(x, y):
    return np.array([x, y, 0])


def plate(w, h, color, at=ORIGIN, stroke=None, radius=0.18, opacity=1):
    return RoundedRectangle(
        width=w, height=h, corner_radius=radius, fill_color=color,
        fill_opacity=opacity, stroke_color=stroke or color, stroke_width=2 if stroke else 0,
    ).move_to(at)


def disk(x, y, radius, color):
    return Dot(p(x, y), radius=radius, color=color)


def stroke(a, b, color, width=3):
    return Line(a, b, color=color, stroke_width=width)


def curve(points, color, width):
    return VMobject(stroke_color=color, stroke_width=width).set_points_smoothly(points)


def label(words, x, y, color=TEXT, size=32):
    return T(words, size, color).move_to(p(x, y))


def tabletop():
    return plate(12.95, 5.8, TABLE, p(0, 0.05), radius=0.28)


class Earthworm(VGroup):
    """A legless, segmented body. The positive-x end is the front."""
    def __init__(self, at, length=1.05, phase=0, angle=0, band=BAND, amp=0.13, bristles=False):
        super().__init__()
        self.length, self.angle, self.band_color, self.amp = length, angle, band, amp
        self.skin = VMobject(stroke_color=WORM, stroke_width=13 * length)
        self.rings = VGroup(*[VMobject(stroke_color="#A85250", stroke_width=0.95 * length)
                              for _ in range(15 if length > 2 else 5)])
        self.band = VMobject(stroke_color=band, stroke_width=15 * length)
        self.hairs = VGroup(*[VMobject(stroke_color="#73474A", stroke_width=1.25 * length)
                              for _ in range(7 if bristles else 0)])
        self.add(self.hairs, self.skin, self.rings, self.band)
        self.pose(at, phase)

    def pose(self, at, phase):
        axis = p(np.cos(self.angle), np.sin(self.angle))
        across = p(-axis[1], axis[0])

        def offset(u, v=0):
            ripple = self.amp * np.sin(1.55 * TAU * u - phase)
            return at + self.length * (u - 0.5) * axis + (ripple + v) * across

        def section(mob, lo, hi, steps):
            mob.set_points_smoothly([offset(u) for u in np.linspace(lo, hi, steps)])

        section(self.skin, 0, 1, 17)
        for u, ring in zip(np.linspace(0.07, 0.94, len(self.rings)), self.rings):
            ring.set_points_as_corners([offset(u, -0.055 * self.length), offset(u, 0.055 * self.length)])
        section(self.band, 0.70, 0.79, 4)
        for u, hair in zip(np.linspace(0.22, 0.62, len(self.hairs)), self.hairs):
            hair.set_points_as_corners([offset(u, -0.04 * self.length),
                                        offset(u + 0.019, -0.12 * self.length)])
        return self

    def wriggle(self, at, speed=2.4, drift=0.12, phase=0):
        def move(worm, dt):
            nonlocal phase
            phase += speed * dt
            worm.pose(at + p(drift * np.sin(phase * 0.55), 0), phase)
        self.add_updater(move)
        return self


def towels(colors):
    halves = VGroup()
    for side, color in zip((-1, 1), colors):
        at = TRAY_CENTER + p(side * 1.91, 0)
        halves.add(plate(3.79, 4.16, color, at, radius=0.18))
    return halves


def tray(colors=None):
    rim = plate(TRAY_W, TRAY_H, STEEL, TRAY_CENTER, stroke="#9AABBA", radius=0.28)
    inside = plate(7.85, 4.27, "#3F515F", TRAY_CENTER, radius=0.22)
    grp = VGroup(rim, inside)
    if colors is not None:
        grp.add(towels(colors))
    return grp


def sides(flipped=False):
    words, colors = (("Damp", BLUE), ("Dry", PAPER))
    ordered = (colors, words) if flipped else (words, colors)
    return VGroup(*[label(word, TRAY_CENTER[0] + sign * 1.91, 3.25, color)
                    for sign, (word, color) in zip((-1, 1), ordered)])


def cardboard(side=0):
    width = 8.27 if side == 0 else 4.12
    at = TRAY_CENTER + p(side * 2.08, 0)
    board = plate(width, 4.55, CARD, at, stroke="#D6B18B", radius=0.18)
    grain = VGroup(*[stroke(at + p(-width / 2 + 0.2, y), at + p(width / 2 - 0.2, y), "#9B754F", 1)
                     for y in (-1.92, -1.75, 1.75, 1.92)])
    return VGroup(board, grain)


def clear_lid(side=1):
    at = TRAY_CENTER + p(side * 2.08, 0)
    lid = plate(4.12, 4.55, "#CBEDF0", at, stroke="#E0F6F8", opacity=0.17)
    reflections = VGroup(*[stroke(at + p(x, 1.15), at + p(x + 0.53, 1.91), "#E0F6F8", 4)
                           for x in (0.65, 0.95)])
    return VGroup(lid, reflections)


def water_cup(at, scale=1):
    glass = Polygon(p(-0.65, 0.72), p(0.65, 0.72), p(0.47, -0.72), p(-0.47, -0.72),
                    color=BLUE, stroke_width=4, fill_color="#304F5E", fill_opacity=1)
    water = Polygon(p(-0.56, 0.12), p(0.56, 0.12), p(0.46, -0.68), p(-0.46, -0.68),
                    color=BLUE, stroke_width=0, fill_color=BLUE, fill_opacity=0.85)
    return VGroup(glass, water).scale(scale).move_to(at)


def light_test_cup():
    return water_cup(p(-6.15, -2.34), 0.38)


def drops(origins):
    return VGroup(*[VGroup(disk(x, y, 0.075, BLUE), disk(x + 0.08, y + 0.15, 0.038, TEXT))
                    for x, y in origins])


def timer():
    value = ValueTracker(0)
    face = dial(value, p(4.72, 0.48), radius=0.93, color=TEAL,
                fmt="{:.0f} min", scale=10, size=29)
    return value, VGroup(face, label("Timer", 4.72, -0.66, TEXT, 29))


def middle_positions():
    return [TRAY_CENTER + p(0, y) for y in np.linspace(-1.66, 1.66, 8)]


def result_positions():
    return [TRAY_CENTER + p(x, y) for x, y in (
        (-2.85, 1.3), (-1.26, 1.47), (-2.66, 0.08), (-1.16, 0.15),
        (-2.92, -1.22), (-1.36, -1.34), (2.10, -0.47), (0, 0.86),
    )]


def worms_at(positions):
    return VGroup(*[Earthworm(at, phase=i * 0.8, amp=0.075)
                    for i, at in enumerate(positions)])


def swim(worms, starts, ends):
    def animate(group, alpha):
        for i, (worm, start, end) in enumerate(zip(group, starts, ends)):
            worm.pose(interpolate(start, end, alpha), i * 0.8 + TAU * alpha)
    return UpdateFromAlphaFunc(worms, animate)


def predict_question():
    return question_card(QUESTION, y=-3.28, size=34).question


def tally(values, title="Tally"):
    sheet = Ledger(values, top_left=(3.34, 1.53), width=3.02, title=title,
                   key_w=1.55, row_h=0.72, size=28)
    sheet[0].set_color(TEXT)
    return sheet


def counting_view():
    """A low view of the opened tray keeps the unreported counts out of sight."""
    return VGroup(plate(8.35, 0.42, "#374B58", p(-1.65, 0.28), radius=0.10),
                  plate(8.35, 1.02, STEEL, p(-1.65, -0.38), stroke="#9AABBA", radius=0.15))


def person(x, y, scale=1, facing=1, child=False, reach=False):
    color = "#BE884B" if child else "#488E8B"
    hand = p(0.83 * facing, -0.05) if reach else p(0.55 * facing, -0.33)
    head = disk(0, 0.94, 0.31, SKIN)
    grip = disk(*hand[:2], 0.105, SKIN)
    hair = Arc(radius=0.29, start_angle=0.2, angle=2.83,
               arc_center=p(0, 1.01), color="#3B2430", stroke_width=10)
    figure = VGroup(
        stroke(p(-0.13, -0.51), p(-0.26, -1.39), "#536579", 11),
        stroke(p(0.15, -0.51), p(0.31, -1.39), "#536579", 11),
        plate(0.64, 1.05, color, radius=0.23),
        stroke(p(0.23 * facing, 0.34), hand, SKIN, 11),
        grip, head, hair,
        disk(0.11 * facing, 0.98, 0.029, "#3B2430"),
    )
    figure.hand = grip
    return figure.scale(scale, about_point=ORIGIN).shift(p(x, y))


def palm(at, facing=1, scale=1):
    fingers = VGroup(*[plate(0.63 + 0.11 * (i % 2), 0.16, SKIN, p(0.5, 0.24 - i * 0.16), radius=0.08)
                       for i in range(4)])
    hand = VGroup(plate(0.78, 0.74, SKIN, radius=0.25), fingers,
                  plate(0.2, 0.48, SKIN, p(0.22, 0.4), radius=0.09).rotate(-0.55))
    if facing < 0:
        hand.flip(UP)
    return hand.scale(scale).move_to(at)


def soil_patch(width, height, at, wet=True):
    earth = plate(width, height, MOIST_SOIL if wet else SOIL, at, radius=0.22)
    grains = VGroup()
    for i in range(34):
        x = width * (0.91 * ((i * 0.618) % 1) - 0.455)
        y = height * (0.85 * ((i * 0.373) % 1) - 0.425)
        grains.add(Ellipse(width=0.12 + 0.07 * (i % 3), height=0.06,
                           color="#677165" if wet else "#785947", fill_opacity=1,
                           stroke_width=0).move_to(at + p(x, y)).rotate(i * 0.52))
    return VGroup(earth, grains)


def garden():
    sky = plate(12.9, 5.78, "#233945", p(0, 0), radius=0.3)
    canopy = VGroup(*[Ellipse(width=w, height=h, color="#32524D", fill_opacity=1,
                              stroke_width=0).move_to(p(x, y))
                      for w, h, x, y in [(4, 1.6, -4.15, 1.80), (4, 1.15, -2.45, 2.05),
                                         (5.2, 1.6, 0.7, 1.85), (4.2, 1.32, 4.14, 1.92)]])
    return VGroup(sky, canopy, soil_patch(12.55, 2.67, p(0, -1.37)))


def log_at(at, scale=1):
    shell = plate(3.65, 1.07, WOOD, stroke="#BA8866", radius=0.35)
    bark = VGroup(*[curve([p(-1.63, y), p(-0.65, y + 0.09), p(0.42, y - 0.05), p(1.37, y)],
                          "#624333", 3) for y in (-0.29, 0, 0.27)])
    end = VGroup(*[Ellipse(width=w, height=h, color="#C9946B", fill_opacity=0.5 if i == 0 else 0,
                           stroke_width=2).move_to(p(1.42, 0))
                   for i, (w, h) in enumerate(((0.81, 0.99), (0.52, 0.72), (0.25, 0.42)))])
    return VGroup(shell, bark, end).scale(scale, about_point=ORIGIN).shift(at)


def tub(at, bait=False, occupied=True):
    pot = Polygon(p(-1.52, 0.48), p(1.52, 0.48), p(1.16, -1.05), p(-1.16, -1.05),
                  stroke_width=3, color=STEEL, fill_color=STEEL, fill_opacity=1)
    soil = Ellipse(width=3.14, height=0.75, color="#78624E", fill_color=SOIL,
                   fill_opacity=1, stroke_width=3).move_to(p(0, 0.53))
    group = VGroup(pot, soil)
    if occupied:
        group.add(Earthworm(p(0.16, 0.55), amp=0.075))
    if bait:
        group.add(plate(1.34, 0.55, "#334958", p(0, -0.39)), label("Bait", 0, -0.39))
    return group.shift(at)


def trowel(at):
    metal = Polygon(p(-0.30, -0.10), p(0.30, -0.10), p(0.23, -0.54), p(0, -0.79),
                    p(-0.23, -0.54), color="#9CABBA", stroke_width=0, fill_opacity=1)
    return VGroup(metal, plate(0.18, 0.71, CARD, p(0, 0.22), radius=0.08)).shift(at)


def lamp_bulb(side):
    return TRAY_CENTER + p(side * 1.91, 2.64)


def lamp(bulb_at, base_at):
    rise = min(1.36, bulb_at[1] - base_at[1] + 0.50)
    stem = CubicBezier(base_at, base_at + UP * rise, bulb_at + p(1.45, 0.54),
                       bulb_at + UP * 0.43, color=STEEL, stroke_width=12)
    shade = Polygon(p(-0.25, 0.5), p(0.25, 0.5), p(0.49, 0.02), p(-0.49, 0.02),
                    color=STEEL, fill_opacity=1, stroke_width=3)
    shade.shift(bulb_at)
    bulb = stroke(bulb_at + LEFT * 0.33, bulb_at + RIGHT * 0.33, YELLOW, 7)
    # The cord exits behind the stand, away from the cup.
    cord = curve([base_at, base_at + p(0.52, 0), base_at + p(0.92, 0.12)], "#8895A2", 4)
    return VGroup(cord, stem, shade, bulb, plate(0.87, 0.15, STEEL, base_at, radius=0.06))


def rays(side, from_lamp=False):
    x, y, _ = lamp_bulb(side)
    spread, top = (0.28, y) if from_lamp else (0.6, 1.77)
    return VGroup(*[stroke(p(x + dx * spread, top), p(x + dx, -1.63), YELLOW, 3).set_opacity(0.46)
                    for dx in (-1.14, -0.58, 0.58, 1.14)])


class S01Hook(SpokenScene):
    def construct(self):
        wet = plate(6.15, 4.8, "#273F4C", p(-3.24, 0.29), radius=0.28)
        dry = plate(6.15, 4.8, "#674F45", p(3.24, 0.29), radius=0.28)
        dirt = VGroup(soil_patch(5.96, 1.92, p(-3.24, -1.1)),
                      soil_patch(5.96, 1.92, p(3.24, -1.1), wet=False))
        rain = VGroup(*[stroke(p(x, y), p(x - 0.16, y - 0.29), BLUE, 3)
                        for x in (-5.67, -4.75, -3.83, -2.94, -2.05, -1.13)
                        for y in (1.25, 2.02)])
        sun = disk(4.43, 1.62, 0.61, GOLD)
        left_log, right_log = log_at(p(-2.75, -0.47), 0.89), log_at(p(3.25, -0.47), 0.89)
        question = question_card("Where do earthworms go on a hot, dry day?", y=-3.21, size=35).question
        adult = person(-5.35, -0.1, 0.88, reach=True)
        stick = stroke(p(-4.69, -0.04), p(-1.76, -0.38), PAPER, 7)
        labels = VGroup(label("After rain", -3.22, 3.13, BLUE), label("Hot, dry day", 3.24, 3.13, PAPER))
        seen = worms_at([p(-3.44, -1.25), p(-2.25, -1.56), p(-1.56, -0.89)])
        self.add(wet, dry, dirt, rain, sun, right_log, adult, stick, left_log, question)
        bob(rain, amp=0.145, speed=4)
        self.at("After rain", lead=0.85)
        self.play(Rotate(left_log, 0.49, about_point=p(-4.2, -0.53)),
                  Rotate(stick, 0.20, about_point=p(-4.69, -0.04)), run_time=1.0)
        self.play(FadeIn(seen), FadeIn(labels), run_time=0.65)
        self.at("With a baking", lead=0.65)
        table, pan = tabletop(), tray()
        pan.shift(RIGHT * 0.92)
        self.play(FadeOut(VGroup(wet, dry, dirt, rain, sun, right_log, adult, stick, left_log, seen, labels, question)),
                  FadeIn(table), FadeIn(pan, scale=0.85), run_time=0.85)
        worms = VGroup(Earthworm(p(-3.3, -1.02), length=1.53),
                       Earthworm(p(-0.32, 1), length=1.53))
        self.play(FadeIn(worms), run_time=0.42)
        self.play(pan.animate.shift(LEFT * 0.92),
                  swim(worms, [p(-3.3, -1.02), p(-0.32, 1)], [p(-1.97, -1.30), p(1.38, 0.17)]),
                  run_time=3.42)
        self.finish()


class S02Title(TitleCard):
    TITLE = "What Do Earthworms Like?"
    LESSON = "What Do Earthworms Like?"

    def construct(self):
        worm_left = Earthworm(p(-3.5, -2.25), length=1.8)
        worm_right = Earthworm(p(2.14, 1.98), length=1.68, angle=-0.43)
        self.add(tabletop(), tray(), worm_left, worm_right)
        worm_left.wriggle(p(-3.5, -2.25))
        worm_right.wriggle(p(2.14, 1.98), phase=1.7)
        words = T(self.TITLE, 46, TEXT, font=TITLE_FONT).move_to(p(0, 3.38))
        self.play(FadeIn(words, shift=UP * 0.12), run_time=0.36)
        self.wait(1.58)


class S03Payoff(SpokenScene):
    def construct(self):
        pan = tray()
        lining = towels((PAPER, PAPER))
        cup = water_cup(p(4.8, 1.75), 0.76)
        cover = cardboard()
        sample = Earthworm(p(0.47, 0.27), length=2.18, amp=0.19)
        note = label("About 35 minutes", -1.65, 3.22, TEXT, 34)
        elapsed, clock = timer()
        ledger = tally([("Left", "│", DAMP)])
        self.add(tabletop(), pan, cup)
        self.at("Allow about")
        self.play(FadeIn(lining, shift=DOWN * 0.65), FadeIn(note), run_time=1.25)
        self.at("once you have your", lead=0.05)
        self.play(FadeIn(sample), run_time=0.55)
        hand = palm(p(4.53, -1.22), -1, 1.65)
        lens = VGroup(Circle(radius=0.92, color=STEEL, stroke_width=15,
                             fill_color=TEXT, fill_opacity=0.14).move_to(p(3.34, -0.37)),
                      stroke(p(4.02, -1.01), p(4.65, -1.62), STEEL, 24))
        viewer = VGroup(hand, lens)
        self.at("Your child practices")
        self.play(FadeIn(viewer, shift=LEFT * 0.42), run_time=0.55)
        self.play(viewer.animate.shift(LEFT * 5.47),
                  swim(VGroup(sample), [p(0.47, 0.27)], [p(-3.95, -0.22)]),
                  run_time=3.58, rate_func=linear)
        self.play(FadeOut(viewer, shift=DOWN * 0.39), run_time=0.42)
        sample.wriggle(p(-3.95, -0.22), drift=0.16, phase=TAU)
        self.at("change one thing")
        self.play(FadeOut(note), FadeOut(cup), FadeIn(cover, shift=DOWN * 0.32), FadeIn(clock), run_time=0.6)
        self.play(elapsed.animate.set_value(1), run_time=0.88, rate_func=linear)
        self.at("count where", lead=0.4)
        self.play(FadeOut(cover, shift=UP * 0.32), FadeOut(clock), run_time=0.44)
        self.play(FadeIn(ledger), run_time=0.38)
        self.play(ledger.reveal(0), run_time=0.52)
        self.finish()


class S04SafetyFind(SpokenScene):
    def construct(self):
        setting = garden()
        bait = tub(p(-4.33, -0.5), bait=True)
        adult = person(0.12, -0.3, 1.15, reach=True)
        child = person(4.55, -0.18, 0.83, facing=-1, child=True)
        tool_shape = trowel(p(0, -0.41))
        tilt = ValueTracker(0.44)
        tool = tool_shape.copy()

        def grip_trowel(mob):
            mob.become(tool_shape.copy().rotate(tilt.get_value(), about_point=ORIGIN)
                       .shift(adult.hand.get_center()))

        grip_trowel(tool)
        adult.hand.set_z_index(1)
        count = label("6–10 earthworms", 0, 3.25, TEXT, 34)
        found = worms_at([p(2.35, -1.82), p(1.38, -1.44), p(2.55, -0.93)])
        container = tub(p(-3.96, -0.72), occupied=False)
        self.add(setting, bait, adult, child)
        self.at("Start with")
        self.play(FadeIn(count), run_time=0.6)
        self.at("damp garden bed")
        self.play(FadeIn(tool), FadeOut(bait, shift=LEFT * 0.4), run_time=0.80)
        tool.add_updater(grip_trowel)
        self.at("Stay with")
        bob(child, amp=0.06, speed=2)
        self.play(adult.animate.shift(RIGHT * 0.50).rotate(-0.14),
                  tilt.animate.set_value(-0.18), run_time=1.7)
        self.at("You do the digging")
        self.play(adult.animate.shift(LEFT * 0.50).rotate(0.14),
                  tilt.animate.set_value(0.50), FadeIn(found), run_time=1.6)
        self.at("Keep the worms")
        tool.remove_updater(grip_trowel)
        self.play(FadeIn(container), FadeOut(tool), FadeOut(count), run_time=0.65)
        self.bring_to_front(found)
        self.play(swim(found, [p(2.35, -1.82), p(1.38, -1.44), p(2.55, -0.93)],
                       [p(-4.74, -0.21), p(-4.03, -0.08), p(-3.22, -0.22)]), run_time=2.45)
        self.finish()


class S04OutdoorSafety(SpokenScene):
    def construct(self):
        setting = garden()
        adult = person(0.12, -0.3, 1.15, facing=-1, reach=True)
        child = person(4.55, -0.18, 0.83, facing=-1, child=True)
        log = log_at(p(-3.14, -0.95))
        grip = adult.hand.get_center()
        stick = stroke(grip, p(-4.30, -1.47), PAPER, 7)
        distance = DoubleArrow(p(0.55, -2.26), p(4.45, -2.26), buff=0, color=TEXT, stroke_width=3)
        six = label("About six feet", 2.5, -3.17)
        self.add(setting, stick, log, adult, child)
        self.at("children stand back")
        self.play(GrowFromCenter(distance), run_time=0.65)
        self.play(FadeIn(six), run_time=0.35)
        self.at("Tilt the log")
        self.play(Rotate(log, -0.57, about_point=p(-1.59, -1.1)),
                  Rotate(stick, -0.50, about_point=grip), run_time=2.5)
        self.at("Never touch snakes")
        snake = curve([p(-5.0, -0.31), p(-4.28, 0.48), p(-3.42, -0.28), p(-2.62, 0.49),
                       p(-2.19, 0.64)], GREEN, 23)
        berry = VGroup(disk(3.22, 0.06, 0.38, "#DA6574"), disk(3.88, -0.07, 0.34, "#DA6574"),
                       disk(3.51, -0.52, 0.35, "#DA6574"),
                       curve([p(3.19, 0.24), p(3.48, 0.72), p(3.88, 0.18)], GREEN, 6))
        icons = []
        for x, item in [(-3.53, VGroup(snake, palm(p(-3.45, -0.64), scale=0.74))),
                        (3.49, VGroup(berry, Arc(radius=0.47, start_angle=3.5, angle=2.3,
                                                 arc_center=p(4.25, 0.37), color=SKIN, stroke_width=10)))]:
            outline = Circle(radius=1.7, color=RED, stroke_width=7).move_to(p(x, 0))
            slash = stroke(p(x - 1.18, 1.18), p(x + 1.18, -1.18), RED, 8)
            icons.append((item, VGroup(outline, slash)))
        self.play(FadeOut(VGroup(adult, child, stick, log, distance, six)), FadeIn(icons[0][0]), run_time=0.62)
        self.play(Create(icons[0][1]), run_time=0.65)
        self.at("Never taste outdoor")
        self.play(FadeIn(icons[1][0]), run_time=0.47)
        self.play(Create(icons[1][1]), run_time=0.7)
        self.finish()


class S04JumpingWorm(SpokenScene):
    def construct(self):
        ground = soil_patch(12.85, 5.85, p(0, 0))
        at = p(-0.65, -0.34)
        worm = Earthworm(at, length=5.6, band="#FFF1DB", amp=0.55)
        phone = VGroup(plate(1.62, 2.42, "#394957", stroke=GREY),
                       plate(1.35, 1.88, "#263841", p(0, 0.13)),
                       Earthworm(p(0, 0.1), length=0.85, band="#FFF1DB", amp=0.09),
                       disk(0, -0.97, 0.076, TEXT)).move_to(p(4.87, 0.25))
        hand = palm(p(5.41, -0.67), -1, 0.85)
        tag = label("May be a jumping worm", -1.45, 3.24, TEXT, 34)
        self.add(ground, worm)
        worm.wriggle(at, speed=7.8, drift=0)
        self.at("may be a jumping")
        self.play(FadeIn(tag), run_time=0.56)
        self.at("Leave it and")
        worm.clear_updaters()
        worm.wriggle(at, speed=4.2, drift=0)
        self.at("Take a photo")
        self.play(FadeIn(hand, shift=LEFT * 0.5), FadeIn(phone, shift=LEFT * 0.5), run_time=0.8)
        self.play(Flash(phone.get_center(), color=TEXT, flash_radius=0.8), run_time=0.55)
        self.finish()


class S05Choking(SpokenScene):
    def construct(self):
        worm = Earthworm(p(-4.83, 0.15), length=1.54)
        soil = soil_patch(1.82, 1.34, p(-2.08, 0.13), wet=False)
        stones = VGroup(*[Ellipse(width=w, height=h, color=c, fill_opacity=1, stroke_width=0).move_to(p(x, y))
                          for w, h, c, x, y in [(0.94, 0.67, GREY, 0.66, 0.34),
                                                (0.71, 0.53, STEEL, 1.21, -0.26),
                                                (0.65, 0.45, "#A0A2A7", 0.31, -0.46)]])
        wrapper = VGroup(plate(1.86, 1.55, "#B2CFD8", stroke="#BDD9E1", opacity=0.21),
                         *[curve([p(-0.72, y), p(-0.23, y + 0.22), p(0.28, y - 0.1), p(0.72, y + 0.14)],
                                  "#BED9E1", 3) for y in (-0.36, 0, 0.38)]).move_to(p(4.31, 0.14))
        items = VGroup(worm, soil, stones, wrapper)
        words = label("Keep away from children under 4", 0, -2.3, TEXT, 36)
        urgent = label("Call 911 if choking", 0, -2.3, RED, 42)
        self.add(tabletop())
        self.at("Keep worms")
        self.play(LaggedStart(*[FadeIn(item, shift=UP * 0.25) for item in items], lag_ratio=0.56), run_time=3.05)
        worm.wriggle(p(-4.83, 0.15))
        self.at("away from children")
        self.play(FadeIn(words), run_time=0.55)
        self.at("Call 911")
        self.play(swap(words, urgent, run_time=0.65))
        self.finish()


class S05LookClosely(SpokenScene):
    def construct(self):
        towel = plate(10.18, 4.55, DAMP, p(0, 0.07), stroke="#CDE6E5", radius=0.24)
        hands = VGroup(palm(p(-2.45, 0.2), scale=2.05), palm(p(2.39, 0.2), facing=-1, scale=1.45))
        wet = drops([(-3.15, 1.11), (-1.98, 1.13), (2.46, 0.87), (3.24, 0.75)])
        worm = Earthworm(p(-0.4, 0.37), length=2.2, amp=0.21)
        self.add(tabletop(), towel, hands, wet)
        self.at("Wet your hands")
        self.play(wet.animate.shift(DOWN * 0.37), run_time=1.06)
        self.at("never squeeze")
        self.play(FadeIn(worm), hands.animate.shift(DOWN * 0.43 + RIGHT * 0.8), FadeOut(wet), run_time=1.65)
        self.play(hands[0].animate.shift(LEFT * 0.8), hands[1].animate.shift(RIGHT * 0.45), run_time=1.35)
        self.at("Watch one")
        self.play(FadeOut(hands, shift=DOWN * 0.65),
                  swim(VGroup(worm), [p(-0.4, 0.37)], [p(0, 0.11)]), run_time=2.45)
        close = Earthworm(p(0, 0.17), length=6.5, amp=0.37)
        self.play(ReplacementTransform(worm, close), run_time=1.28)
        front = question_card("Which end is the front?", y=-3.22, size=33).question
        answer = label("Front", 3.55, 1.7, "#26313C")
        pointer = Arrow(p(3.51, 1.39), p(3.23, 0.71), buff=0.04, color="#26313C")
        self.at("which end is")
        self.play(FadeIn(front), run_time=0.47)
        self.at("band is near")
        self.play(FadeIn(answer), GrowArrow(pointer), run_time=0.59)
        self.at("bristles scratch", lead=0.9)
        hairs = Earthworm(p(0, 0.17), length=6.5, amp=0.37, bristles=True).hairs
        self.play(FadeOut(front), FadeIn(hairs), run_time=0.43)
        self.play(FadeIn(label("Bristles grip the paper", -0.35, -1.58, "#26313C")), run_time=0.55)
        self.finish()


class S06DampDry(SpokenScene):
    def construct(self):
        lining = towels((PAPER, PAPER))
        damp = towels((DAMP, PAPER))[0]
        names = sides()
        cup = water_cup(p(4.82, 0.38), 1.05)
        moisture = drops([(-4.42, 0.87), (-3.77, 0.21), (-3.1, 0.75), (-2.81, -0.41), (-4.11, -0.78)])
        hand = palm(p(4.78, -1.67), -1, 1.17)
        question = question_card("Which side will the worms go to, damp or dry?", y=-3.25, size=32).question
        self.add(tabletop(), tray())
        self.at("Line the tray")
        self.play(FadeIn(lining, shift=DOWN * 0.5), run_time=1.03)
        self.at("Keep one half")
        self.play(FadeIn(names[1]), FadeIn(cup, shift=LEFT * 0.27), run_time=0.69)
        self.at("Dampen the other")
        self.play(cup.animate.rotate(0.61), FadeIn(moisture, shift=DOWN * 0.47), run_time=1.03)
        self.play(Transform(lining[0], damp), FadeOut(moisture), run_time=1.35)
        self.play(FadeIn(names[0]), FadeOut(cup), run_time=0.59)
        self.at("Which side will", lead=0.75)
        self.play(FadeIn(hand, shift=LEFT * 0.22), run_time=0.42)
        self.play(hand.animate.move_to(p(-0.63, -1.54)), run_time=1.03)
        self.play(hand.animate.move_to(p(-3.83, -1.54)), run_time=0.93)
        self.play(FadeOut(hand), FadeIn(question), run_time=0.42)
        self.finish()


class S06Count(SpokenScene):
    def construct(self):
        starts = [at + p(1.40 if i % 2 else -1.4, 0) for i, at in enumerate(middle_positions())]
        worms = worms_at(starts)
        board = cardboard()
        clock_value, clock = timer()
        ledger = tally([("Damp", "—", BLUE), ("Dry", "—", PAPER), ("Middle", "—", TEXT)])
        center = plate(0.68, 4.16, "#326677", TRAY_CENTER, radius=0.11)
        self.add(tabletop(), tray((DAMP, PAPER)), sides())
        self.at("Place the worms")
        self.play(FadeIn(worms), run_time=0.5)
        self.play(swim(worms, starts, middle_positions()), run_time=2.15)
        self.at("Cover the whole tray")
        self.play(FadeIn(board, shift=UP * 0.4), run_time=1.0)
        self.remove(worms)
        self.play(FadeIn(clock), run_time=0.5)
        self.play(clock_value.animate.set_value(1), run_time=3.35, rate_func=linear)
        self.at("After 10 minutes")
        results = worms_at(result_positions())
        self.add(results)
        self.bring_to_front(board)
        self.play(FadeOut(board, shift=UP * 0.72), FadeOut(clock), run_time=0.54)
        self.play(FadeIn(ledger), run_time=0.32)
        self.play(ledger.reveal(0), ledger.reveal(1), run_time=0.72)
        self.at("Count any worm")
        self.add(center)
        self.bring_to_front(results)
        self.play(FadeIn(center), run_time=0.60)
        self.play(ledger.reveal(2), ledger.mark(2), run_time=0.5)
        self.play(FadeOut(center), run_time=0.48)
        self.finish()


def example_world():
    return tabletop(), tray((DAMP, PAPER)), sides(), worms_at(result_positions())


class S07PredictQ(SpokenScene):
    def construct(self):
        table, pan, names, worms = example_world()
        ledger = tally([("Damp", "6", BLUE), ("Dry", "1", PAPER), ("Middle", "1", TEXT)], title="Example")
        self.add(table, pan, names, worms)
        self.at("Suppose")
        damp_paper = pan[2][0]
        self.play(damp_paper.animate.set_fill("#B7DFDF"),
                  swim(worms, result_positions(), result_positions()), run_time=1.04)
        for i, (worm, at) in enumerate(zip(worms, result_positions())):
            worm.wriggle(at, drift=0.045, phase=i * 0.8)
        self.play(FadeIn(ledger), run_time=0.38)
        self.play(ledger.reveal(0), ledger.reveal(1), ledger.reveal(2), run_time=0.62)
        self.play(damp_paper.animate.set_fill(DAMP), run_time=1.36)
        self.at("Imagine turning")
        turn = Arc(radius=0.71, start_angle=0.28, angle=4.65,
                   arc_center=p(4.76, -2.21), color=GOLD, stroke_width=5)
        turn.add_tip(tip_length=0.22)
        self.play(Create(turn), run_time=1.2)
        self.at("damp half is")
        self.play(FadeOut(turn), FadeOut(ledger.everything()), run_time=0.68)
        self.at("Where do you predict")
        hand = palm(p(5.55, -0.12), -1, 1.58)
        self.play(FadeIn(predict_question()), FadeIn(hand, shift=LEFT * 0.6), run_time=0.66)
        self.play(hand.animate.move_to(p(3.17, -0.12)), run_time=1.36)
        self.play(FadeOut(hand, shift=RIGHT * 1.22), run_time=1.55)
        for i, (worm, at) in enumerate(zip(worms, result_positions())):
            worm.clear_updaters()
            worm.pose(at, i * 0.8)
        self.finish()


class S08PredictPause(Scene):
    def construct(self):
        self.add(*example_world(), predict_question())
        self.wait(float(os.environ.get("KX_DURATION", "4.5")))


class S09SwapWhy(SpokenScene):
    def construct(self):
        table, pan, names, worms = example_world()
        dried, dampened = PAPER, DAMP
        question = predict_question()
        after = tray((dried, dampened))
        dest = [2 * TRAY_CENTER - at for at in result_positions()]
        flipped = worms_at(dest)
        moving = VGroup(pan, worms)
        self.add(table, moving, names, question)
        self.at("Turn the tray")
        self.play(FadeOut(question), FadeOut(names), run_time=0.42)
        original = moving.copy()

        def turn_tray(group, alpha):
            group.become(original).rotate(PI * alpha, about_point=TRAY_CENTER)
            group.scale(1 - 0.40 * np.sin(PI * alpha), about_point=TRAY_CENTER)

        self.play(UpdateFromAlphaFunc(moving, turn_tray), run_time=1.55)
        self.remove(moving)
        self.add(after, flipped)
        names = sides(flipped=True)
        again = question_card("Will most choose damp again?", size=33, y=-3.26).question
        self.at("do you think more")
        self.play(FadeIn(names), FadeIn(again), run_time=0.62)
        for i, (worm, at) in enumerate(zip(flipped, dest)):
            worm.wriggle(at, drift=0.045, phase=i * 0.8)
        self.at("Return the worms")
        for worm in flipped:
            worm.clear_updaters()
        self.play(FadeOut(again), swim(flipped, dest, middle_positions()), run_time=1.5)
        self.at("cover the tray")
        board = cardboard()
        clock_value, clock = timer()
        self.play(FadeIn(board, shift=UP * 0.36), FadeIn(clock), run_time=0.65)
        self.remove(flipped)
        self.play(clock_value.animate.set_value(1), run_time=1.44, rate_func=linear)
        self.at("count again", lead=0.55)
        front = counting_view()
        self.play(ReplacementTransform(after, front), FadeOut(board, shift=UP * 1.05),
                  FadeOut(clock), FadeOut(names), run_time=0.59)
        totals = tally([("Damp", "6 + □", BLUE), ("Dry", "1 + □", PAPER)], title="Add both runs")
        self.play(FadeIn(totals), run_time=0.55)
        self.at("Add the damp")
        self.play(totals.reveal(0), run_time=0.51)
        self.at("then the dry")
        self.play(totals.reveal(1), run_time=0.55)
        self.finish()


class S09Why(SpokenScene):
    def construct(self):
        pan = tray((PAPER, DAMP))
        ground_dry = soil_patch(12.9, 3.60, p(0, -0.94), wet=False)
        lower = soil_patch(12.9, 2.14, p(0, -1.67))
        tunnel = plate(9.84, 0.67, "#263836", p(0.54, -1.47), radius=0.31)
        sky = plate(12.9, 1.90, "#3C4144", p(0, 1.77), radius=0.2)
        shade = plate(7.18, 0.42, "#25303A", p(2.71, 1.69), radius=0.18)
        worm = Earthworm(p(-1.92, 0.46), length=5.1, amp=0.26)
        oxygen = VGroup(*[disk(x, 1.47 + 0.13 * (i % 2), 0.095, OXYGEN)
                          for i, x in enumerate(np.linspace(-4.0, 0, 7))])
        self.add(tabletop(), pan)
        self.at("Earthworms breathe")
        landscape = VGroup(sky, ground_dry, lower, tunnel)
        self.play(pan.animate.stretch(0.74, dim=1).shift(DOWN * 0.45), run_time=0.32)
        self.play(FadeOut(pan), FadeIn(landscape), FadeIn(worm), run_time=0.58)
        self.play(FadeIn(oxygen), run_time=0.32)
        oxygen_text = label("Oxygen", -2.0, 2.24, OXYGEN)
        self.play(FadeIn(oxygen_text), run_time=0.38)
        self.at("has to stay")
        self.play(oxygen.animate.shift(DOWN * 0.99), run_time=1.33, rate_func=linear)
        self.play(FadeOut(oxygen), FadeOut(oxygen_text), run_time=0.46)
        self.at("Most move away")
        sunny = disk(-4.76, 1.95, 0.46, YELLOW)
        self.play(FadeIn(sunny), FadeIn(shade), run_time=0.60)
        self.play(swim(VGroup(worm), [p(-1.92, 0.46)], [p(2.33, -1.45)]),
                  run_time=2.41, rate_func=linear)
        self.play(FadeIn(label("Damp, dark soil", 2.85, -3.2, BLUE)), run_time=0.48)
        self.finish()


class S10LightTest(SpokenScene):
    def construct(self):
        pan = tray()
        lining = towels((PAPER, DAMP))
        damp = towels((DAMP, DAMP))[0]
        cup = light_test_cup()
        mist = drops([(-4.42, 0.87), (-3.77, 0.21), (-3.1, 0.75), (-2.81, -0.41), (-4.11, -0.78)])
        board, lid = cardboard(-1), clear_lid(1)
        names = VGroup(label("Cardboard", -3.56, 3.25, PAPER),
                       label("Clear lid", 0.26, 3.25, BLUE))
        beam = rays(1)
        desk_lamp = lamp(lamp_bulb(1), LAMP_BASE)
        adult = person(4.94, 1.04, 0.83, facing=-1, reach=True)
        height = label("About two feet", 4.02, -1.79, TEXT, 29)
        height_arrow = DoubleArrow(p(2.90, -1.40), p(2.90, lamp_bulb(1)[1]),
                                   buff=0, color=TEXT, stroke_width=3, tip_length=0.16)
        safe = label("Away from water", 4.23, -2.44, BLUE, 28)
        room_light = label("Bright room light", 4.34, 0.72, TEXT, 30)
        self.add(tabletop(), pan, lining)
        self.at("dampen the tray")
        self.play(FadeIn(cup), FadeIn(mist, shift=DOWN * 0.37), run_time=0.7)
        self.play(Transform(lining[0], damp), FadeOut(mist), run_time=1.15)
        self.at("out of direct sun")
        shade_label = label("Out of direct sun", -1.65, 3.22, TEXT, 32)
        self.play(FadeIn(shade_label), run_time=0.5)
        self.at("Cover half with cardboard")
        self.play(FadeOut(shade_label), FadeIn(board, shift=UP * 0.56), run_time=0.72)
        self.play(FadeIn(names[0]), run_time=0.50)
        self.at("with a clear")
        self.play(FadeIn(lid, shift=UP * 0.53), run_time=0.75)
        self.play(FadeIn(names[1]), run_time=0.45)
        self.at("bright room light")
        self.play(Create(beam), FadeIn(room_light), run_time=1.03)
        self.at("Or set a cool")
        self.play(FadeOut(room_light), FadeOut(names), run_time=0.3)
        self.play(FadeIn(adult), FadeIn(desk_lamp), Transform(beam, rays(1, from_lamp=True)),
                  run_time=0.73)
        self.at("about two feet")
        self.play(GrowFromCenter(height_arrow), FadeIn(height), run_time=0.48)
        self.at("away from water")
        self.play(FadeIn(safe), run_time=0.52)
        self.finish()


class S10LightRepeat(SpokenScene):
    def construct(self):
        table, pan = tabletop(), tray((DAMP, DAMP))
        lid, board = clear_lid(1), cardboard(-1)
        beam = rays(1, from_lamp=True)
        desk_lamp = lamp(lamp_bulb(1), LAMP_BASE)
        adult = person(4.94, 1.04, 0.83, facing=-1, reach=True)
        cup = light_test_cup()
        starts = [at + p(1.08 if i % 2 else -1.0, 0) for i, at in enumerate(middle_positions())]
        worms = worms_at(starts)
        sample_at = p(0.27, -0.16)
        model = Earthworm(sample_at, length=2.94, amp=0.26)
        no_eyes = label("No eyes", 4.71, 0.3)
        light_skin = label("Skin senses light", 4.65, 0.3, YELLOW, 30)
        question = question_card("Where will the worms go?", size=33, y=-3.31).question
        self.add(table, pan, cup, board, lid, beam, desk_lamp)
        self.at("Earthworms have no eyes")
        self.play(FadeIn(model), run_time=0.52)
        model.wriggle(sample_at)
        self.play(FadeIn(no_eyes), run_time=0.52)
        self.at("skin senses light")
        self.play(swap(no_eyes, light_skin, run_time=0.62))
        self.at("Predict where")
        self.play(FadeOut(light_skin), FadeIn(question), run_time=0.62)
        self.at("Start them in")
        self.play(FadeOut(VGroup(question, model, lid, board, beam)), FadeIn(worms), run_time=0.55)
        self.play(swim(worms, starts, middle_positions()), run_time=1.55)
        self.at("Cover both halves")
        self.play(FadeIn(board, shift=UP * 0.4), FadeIn(lid, shift=UP * 0.4), FadeIn(beam), run_time=0.68)
        self.remove(worms)
        time, clock = timer()
        self.play(FadeIn(clock), FadeOut(desk_lamp), run_time=0.42)
        self.play(time.animate.set_value(1), run_time=2.64, rate_func=linear)
        self.at("after 10 minutes")
        sheet = tally([("Dark", "—", PAPER), ("Light", "—", YELLOW), ("Middle", "—", TEXT)])
        front = counting_view()
        self.play(ReplacementTransform(pan, front),
                  FadeOut(VGroup(board, lid, beam, clock), shift=UP * 0.74), run_time=0.54)
        self.play(FadeIn(sheet), run_time=0.32)
        self.play(sheet.reveal(0), sheet.reveal(1), sheet.reveal(2), run_time=0.58)
        self.at("Swap covers")
        self.play(ReplacementTransform(front, tray((DAMP, DAMP))), FadeOut(sheet.everything()), run_time=0.40)
        self.play(FadeIn(cardboard(1)), FadeIn(clear_lid(-1)), run_time=0.33)
        self.at("move the lamp")
        lifted_lamp = lamp(lamp_bulb(1), p(LAMP_BASE[0], 2.70))
        self.play(FadeIn(desk_lamp), FadeIn(adult), FadeOut(cup), run_time=0.20)
        self.play(Transform(desk_lamp, lifted_lamp), run_time=0.27)
        self.play(desk_lamp.animate.shift(lamp_bulb(-1) - lamp_bulb(1)), run_time=0.46)
        self.play(FadeIn(rays(-1, from_lamp=True)), run_time=0.20)
        self.at("and repeat")
        time.set_value(0)
        self.play(FadeOut(adult), run_time=0.3)
        self.play(FadeIn(clock), run_time=0.44)
        self.finish()


class S11Return(SpokenScene):
    def construct(self):
        setting = garden()
        adult = person(0.12, -0.3, 1.15, facing=-1, reach=True)
        child = person(4.55, -0.18, 0.83, facing=-1, child=True)
        origin = p(-2.30, -1.24)
        angle = 0.48
        container = tub(origin, occupied=False)
        moist = drops([(-3.14, -0.20), (-2.62, -0.03), (-2.23, -0.14), (-1.83, -0.10)])
        seats = [p(-0.65, 0.63), p(0.09, 0.42), p(0.60, 0.68)]
        worms = VGroup(*[Earthworm(origin + seat, phase=i * 0.8, angle=PI, amp=0.06)
                         for i, seat in enumerate(seats)])
        self.add(setting, adult, child, container, worms)
        self.at("worms with plain")
        self.play(FadeIn(moist, shift=DOWN * 0.22), run_time=0.52)
        self.play(moist.animate.shift(DOWN * 0.38), run_time=1.34)
        self.at("Return them to")
        self.play(FadeOut(moist), Rotate(VGroup(container, worms), angle, about_point=origin),
                  adult.animate.shift(p(-0.24, 0.27)), run_time=0.74)

        targets = [p(-5.55, -1.89), p(-5.23, -2.37), p(-4.92, -1.96)]
        paths = []
        for i, (seat, target) in enumerate(zip(seats, targets)):
            start = origin + rotate_vector(seat, angle)
            rim = origin + rotate_vector(p(-1.72, 0.63 + i * 0.06), angle)
            over_rim = CubicBezier(start, start + p(-0.55, 0.06), rim + p(0.55, 0.26), rim)
            onto_soil = CubicBezier(rim, rim + p(-0.44, -0.12), target + p(0.35, 0.05), target)
            paths.append((over_rim, onto_soil))

        def crawl_out(group, alpha):
            for i, (worm, (over_rim, onto_soil)) in enumerate(zip(group, paths)):
                progress = np.clip((alpha - i * 0.10) / 0.80, 0, 1)
                worm.angle = PI + interpolate(angle, 0.16, progress)
                if progress < 0.60:
                    at = over_rim.point_from_proportion(progress / 0.60)
                else:
                    at = onto_soil.point_from_proportion((progress - 0.60) / 0.40)
                worm.pose(at, i * 0.8 + TAU * progress)

        self.play(UpdateFromAlphaFunc(worms, crawl_out), run_time=2.55, rate_func=linear)
        self.at("Watch them burrow")
        self.play(LaggedStart(*[FadeOut(worm, shift=DOWN * 0.38, scale=0.5) for worm in worms], lag_ratio=0.39), run_time=1.73)
        self.at("Never release bait")
        bait = tub(p(0, 0.02), bait=True)
        rule = label("Never release outside", 0, -3.22, RED, 36)
        self.play(FadeOut(VGroup(adult, child, container)), FadeIn(bait, scale=0.87), run_time=0.60)
        self.play(FadeIn(rule), run_time=0.55)
        self.at("Wash your hands")
        hands = VGroup(palm(p(-0.71, -0.42), scale=1.94), palm(p(0.55, -0.44), -1, 1.8))
        water = drops([(-0.83, 0.45), (-0.27, 0.97), (0.24, 1.23), (0.83, 0.83), (0.72, 0.35)])
        soap = VGroup(*[Circle(radius=r, color=TEXT, stroke_width=3).move_to(p(x, y))
                        for x, y, r in [(0.28, 0.1, 0.14), (-0.37, 0.03, 0.10), (0.51, 0.18, 0.09)]])
        self.play(FadeOut(VGroup(setting, bait, rule)), FadeIn(tabletop()),
                  FadeIn(hands), FadeIn(water), FadeIn(soap), run_time=0.64)
        self.play(water.animate.shift(DOWN * 0.7), soap.animate.shift(UP * 0.45), run_time=1.3)
        self.finish()


class S12End(EndCard):
    LINE = "Earthworms breathe through moist skin, so most choose damp, dark places."
