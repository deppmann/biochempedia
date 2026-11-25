"""Backyard Habitat Hunt · Parent Guide."""
from bp_parts import *


# COLOR MAP: GREEN living plants, GOLD food and sunlight, BLUE water,
# TEAL air and adult equipment, RED hazards, GREY nonliving objects, TEXT string.
SKY = "#20383F"
DISTANT = "#294A45"
LAWN = "#4E7540"
TURF = "#395737"
SOIL = "#594033"
DEEP_SOIL = "#3D302C"
PAPER = "#202D32"
WOOD = "#B58255"
SKIN = "#F3BA91"
ANT = "#E7A66D"
SPIDER = "#B7A9D4"

GROUND = -1.48
CORNERS = ((-2.48, -0.2), (2.48, -0.2), (3.92, -1.29), (-3.92, -1.29))
QUESTION = "What will you see moving?"


def pt(x, y):
    return np.array([x, y, 0.0])


def solid(*points, color):
    return Polygon(*(pt(*p) for p in points), fill_color=color, fill_opacity=1, stroke_width=0)


def oval(w, h, color, at=ORIGIN, angle=0):
    return Ellipse(width=w, height=h, fill_color=color, fill_opacity=1, stroke_width=0).rotate(angle).move_to(at)


def path(*points, color=TEXT, width=4):
    return VMobject().set_points_smoothly([pt(*p) for p in points]).set_stroke(color, width)


def line(a, b, color=TEXT, width=4):
    return Line(pt(*a), pt(*b), stroke_color=color, stroke_width=width)


def slab(w, h, color, at=ORIGIN, r=0.18):
    return RoundedRectangle(width=w, height=h, corner_radius=r, stroke_width=0,
                            fill_color=color, fill_opacity=1).move_to(at)


def label(text, at, color=TEXT, size=32):
    return T(text, size=size, color=color, weight=BOLD).move_to(at)


def blade(x, y, h, lean, width, color):
    start = pt(x, y)
    tip = pt(x + lean, y + h)
    shape = VMobject()
    shape.start_new_path(start + LEFT * width)
    shape.add_cubic_bezier_curve_to(pt(x - width, y + h * 0.48),
                                   tip + LEFT * width * 0.9 + DOWN * h * 0.22, tip)
    shape.add_cubic_bezier_curve_to(tip + DOWN * h * 0.22 + RIGHT * width * 0.55,
                                   pt(x + width, y + h * 0.34), start + RIGHT * width)
    shape.close_path()
    return shape.set_fill(color, 1).set_stroke(width=0)


def tuft(x, y, size=1, phase=0, still=False):
    plants = VGroup()
    for i, (dx, h, lean, width, col) in enumerate((
        (-0.22, 0.88, -0.48, 0.095, "#72A758"),
        (-0.12, 1.19, -0.18, 0.105, GREEN),
        (0.04, 1.43, 0.30, 0.095, "#A0CC73"),
        (0.18, 0.85, 0.55, 0.10, "#669C51"),
        (0.30, 0.62, 0.45, 0.08, "#8BB761"),
    )):
        stem_x = x + dx * size
        plant = blade(stem_x, y, h * size, lean * size, width * size, col)
        if not still:
            points = plant.points.copy()
            bend = np.square(np.maximum(points[:, 1] - y, 0) / (h * size))
            angle = phase + 0.40 * i

            def sway(mob, dt, points=points, bend=bend, angle=angle, size=size):
                mob.wind_time += dt
                mob.points[:, 0] = points[:, 0] + 0.28 * size * bend * (
                    np.sin(2.05 * mob.wind_time + angle) - np.sin(angle)
                )

            plant.wind_time = 0.0
            plant.add_updater(sway)
        plants.add(plant)
    return plants


def sunlight(at=pt(-5.05, 2.26), radius=0.6):
    sun = VGroup(
        Circle(radius=radius * 1.30, stroke_width=0, fill_color=GOLD, fill_opacity=0.12),
        Circle(radius=radius, stroke_width=0, fill_color="#F5D587", fill_opacity=1),
    )
    return sun.move_to(at)


def yard(still=False, plain=False):
    """The same cross-section, with the back and front string corners fixed to the lawn."""
    sky = slab(13.14, 7.04, SKY, r=0.30)
    distant = solid((-6.52, 0.28), (-6.52, 0.81), (-5.07, 1.14), (-3.60, 0.93),
                    (-2.24, 0.54), (-0.65, 0.90), (0.85, 0.65), (2.55, 1.09),
                    (4.09, 0.83), (5.67, 1.10), (6.52, 0.86), (6.52, 0.28), color=DISTANT)
    surface = solid((-6.52, 0.33), (6.52, 0.33), (6.52, GROUND), (-6.52, GROUND), color=LAWN)
    verge = solid((-6.52, -1.44), (6.52, -1.44), (6.52, -1.74), (-6.52, -1.74), color=TURF)
    soil = solid((-6.52, -1.73), (6.52, -1.73), (6.52, -3.39), (6.42, -3.50),
                 (-6.42, -3.50), (-6.52, -3.39), color=SOIL)
    subsoil = solid((-6.40, -3.50), (-6.52, -3.39), (-6.52, -2.92), (-4.64, -2.8),
                    (-2.74, -3.03), (-0.91, -2.89), (0.92, -3.06), (3.25, -2.81),
                    (5.13, -2.91), (6.52, -2.79), (6.52, -3.39), (6.42, -3.50), color=DEEP_SOIL)
    light = sunlight()
    if not still:
        bob(light, amp=0.07, speed=1.3)
    freckles = VGroup()
    rng = np.random.default_rng(62)
    for _ in range(26):
        x, y = rng.uniform(-6.21, 6.21), rng.uniform(-3.37, -1.91)
        freckles.add(oval(rng.uniform(0.08, 0.22), 0.06, "#795743", pt(x, y), rng.uniform(-0.5, 0.5)))
    plants = VGroup(*(tuft(x, y, s * (0.48 if plain else 1), i * 0.7, still)
                      for i, (x, y, s) in enumerate((
                          (-5.84, -0.23, 0.83), (-5.30, -1.29, 1.37), (-4.48, -1.26, 0.88),
                          (-3.58, -0.39, 0.48), (-1.48, -0.43, 0.34), (1.42, -0.44, 0.39),
                          (3.91, -0.45, 0.56), (4.75, -1.23, 1.12), (5.48, -0.80, 0.83),
                          (5.92, -1.32, 1.06),
                      ))))
    return VGroup(sky, distant, light, surface, soil, subsoil, freckles, verge, plants)


def survey():
    pegs = VGroup()
    for x, y in CORNERS:
        pegs.add(slab(0.13, 0.49, WOOD, pt(x, y + 0.19), r=0.06))
    cord = VMobject().set_points_as_corners([pt(x, y + 0.24) for x, y in (*CORNERS, CORNERS[0])])
    cord.set_stroke(TEXT, width=4.2)
    return pegs, cord


def crumb():
    return VGroup(solid((-0.36, -0.12), (-0.28, 0.21), (0.03, 0.31), (0.30, 0.12),
                        (0.37, -0.15), (0.08, -0.25), color=GOLD),
                  oval(0.23, 0.10, "#A97645", pt(-0.07, 0.10), 0.34))


def food():
    return VGroup(crumb(), oval(0.68, 0.29, "#CF8C5A", angle=-0.56)).arrange(RIGHT, buff=0.12)


def drop():
    shape = VMobject().start_new_path(pt(0, 0.55))
    shape.add_cubic_bezier_curve_to(pt(0.12, 0.29), pt(0.41, 0.09), pt(0.40, -0.15))
    shape.add_cubic_bezier_curve_to(pt(0.38, -0.63), pt(-0.38, -0.63), pt(-0.40, -0.15))
    shape.add_cubic_bezier_curve_to(pt(-0.41, 0.09), pt(-0.12, 0.29), pt(0, 0.55))
    return VGroup(shape.set_fill(BLUE, 1).set_stroke(width=0),
                  oval(0.13, 0.32, "#C6F0F0", pt(-0.19, -0.12), -0.18))


def dew_grass():
    leaf = blade(-0.35, -0.58, 1.10, 0.47, 0.13, GREEN)
    return VGroup(leaf, drop().scale(0.75).move_to(pt(0.37, 0.02)))


def breeze():
    return VGroup(*(path((-0.85 + offset, y), (-0.34 + offset, y + 0.10),
                         (0.29, y), (0.63 - offset, y + 0.12), color=TEAL, width=5)
                    for y, offset in ((0.22, 0.05), (-0.04, -0.20), (-0.34, 0.13))))


def tunnel():
    bank = oval(1.91, 1.07, "#8E6344")
    opening = path((-0.50, 0.24), (-0.22, 0.17), (-0.12, -0.16), (0.27, -0.19),
                   (0.59, -0.10), color=DEEP_SOIL, width=22)
    return VGroup(bank, opening)


def span(w=1.65):
    x = w / 2
    return VMobject().set_points_as_corners([pt(-x, 0.17), pt(-x, 0), pt(x, 0), pt(x, 0.17)]).set_stroke(GREEN, 4)


def ant(carry=False):
    legs = VGroup(*(path((x, 0.0), (x + dx, sign * 0.26), (x + dx + 0.10, sign * 0.43),
                         color=ANT, width=3)
                    for sign in (-1, 1) for x, dx in ((-0.18, -0.28), (0.0, -0.07), (0.16, 0.18))))
    feelers = VGroup(*(path((0.49, sign * 0.09), (0.61, sign * 0.22), (0.78, sign * 0.22),
                            color=ANT, width=3) for sign in (-1, 1)))
    body = VGroup(oval(0.59, 0.43, ANT, pt(-0.43, 0)), oval(0.38, 0.32, WOOD),
                  oval(0.40, 0.37, ANT, pt(0.36, 0)),
                  oval(0.055, 0.052, DEEP_SOIL, pt(0.48, 0.07)),
                  oval(0.055, 0.052, DEEP_SOIL, pt(0.48, -0.07)))
    bug = VGroup(legs, feelers, body)
    if carry:
        bug.add(crumb().scale(0.36).move_to(pt(0.74, 0)))
    return bug


def scuttle(bug, offset):
    """Move the ant with an alternating tripod gait."""
    base = bug.copy()

    def step(mob, alpha):
        mob.become(base)
        for index, leg in enumerate(mob[0]):
            angle = 0.23 * np.sin(TAU * alpha * 4 + PI * index)
            leg.rotate(angle, about_point=leg.get_start())
        mob.shift(alpha * offset + UP * 0.023 * np.sin(TAU * alpha * 8))

    return UpdateFromAlphaFunc(bug, step, rate_func=linear)


def spider(thread=False):
    legs = VGroup(*(path((side * 0.10, y), (side * mid, y + 0.12), (side * end, y - 0.16),
                         color=SPIDER, width=3)
                    for side in (-1, 1) for y, mid, end in
                    ((0.10, 0.33, 0.45), (-0.01, 0.42, 0.60), (-0.12, 0.48, 0.57), (-0.21, 0.35, 0.41))))
    bug = VGroup(legs, oval(0.47, 0.46, SPIDER, pt(0, 0.10)),
                 oval(0.31, 0.29, "#8F7EBA", pt(0, -0.15)))
    if thread:
        bug.add(line((0, 0.31), (0, 1.17), "#AAC1BB", 1.8))
    return bug


def leaf():
    return VGroup(oval(0.95, 0.47, GREEN, angle=0.58),
                  line((-0.50, -0.32), (0.36, 0.22), TURF, 2.6))


def rock():
    return solid((-0.50, -0.18), (-0.42, 0.17), (-0.07, 0.34), (0.32, 0.25),
                 (0.55, -0.14), (0.31, -0.28), (-0.25, -0.28), color=GREY)


def stone_soil():
    return solid((-0.56, -0.29), (-0.58, 0.04), (-0.23, 0.21), (0.09, 0.19),
                 (0.61, 0.01), (0.57, -0.30), color="#A17150")


def pencil():
    return VGroup(solid((-0.89, -0.095), (0.68, -0.095), (0.68, 0.095), (-0.89, 0.095), color=GOLD),
                  solid((0.68, -0.095), (1.04, 0), (0.68, 0.095), color=SKIN),
                  solid((0.92, -0.03), (1.04, 0), (0.92, 0.03), color=BG),
                  slab(0.22, 0.19, "#CC8580", pt(-0.93, 0), 0.04))


def pencil_hand():
    return VGroup(hand().scale(0.72).rotate(-0.4).move_to(pt(-0.62, 0.23)), pencil())


def pencil_and_grass():
    left_grass = tuft(-0.28, -0.77, 0.89, still=True)
    right_grass = tuft(0.34, -0.77, 0.94, still=True)
    tool = pencil_hand().scale(1.24).rotate(-0.54).move_to(pt(-0.65, 1.41))
    return left_grass, right_grass, tool


def magnifier():
    handle = slab(0.23, 0.86, TEAL, pt(0, -0.80), 0.1)
    lens = Circle(radius=0.48, color=TEAL, stroke_width=7, fill_color=BLUE, fill_opacity=0.2)
    shine = Arc(radius=0.35, start_angle=0.48 * PI, angle=0.35 * PI, color=BLUE, stroke_width=4)
    return VGroup(handle, lens, shine)


def hand(color=SKIN):
    fingers = VGroup(*(slab(0.17, h, color, pt(x, 0.16 + h / 2), r=0.08)
                       for x, h in ((-0.26, 0.40), (-0.08, 0.54), (0.10, 0.49), (0.28, 0.34))))
    thumb = slab(0.19, 0.43, color, pt(-0.38, -0.02), r=0.08).rotate(0.55)
    return VGroup(fingers, thumb, slab(0.66, 0.59, color, pt(0.01, -0.02), r=0.17),
                  slab(0.38, 0.31, color, pt(0.02, -0.40), r=0.10))


def gloves():
    return VGroup(hand("#4F9896").rotate(0.34).shift(LEFT * 0.37),
                  hand(TEAL).rotate(-0.30).shift(RIGHT * 0.34 + DOWN * 0.08))


def coil():
    t = np.linspace(0, 5.9 * TAU, 260)
    r = np.linspace(0.12, 0.67, len(t))
    pts = [pt(rr * np.cos(tt), 0.68 * rr * np.sin(tt)) for rr, tt in zip(r, t)]
    pts.extend((pt(0.64, -0.44), pt(0.87, -0.42)))
    return VMobject().set_points_as_corners(pts).set_stroke(TEXT, width=3)


def clipboard(at, width=3.65, height=2.82):
    return VGroup(slab(width, height, WOOD, at),
                  slab(width - 0.23, height - 0.28, PAPER, at + DOWN * 0.015),
                  slab(1.0, 0.19, GREY, at + UP * (height / 2 - 0.08), r=0.08))


def tally_board(guess=False, count=0):
    board = clipboard(pt(4.38, 1.57), width=3.40, height=2.86)
    rows = Ledger([("Guess", "?", GOLD), ("Count", "Ⅰ Ⅰ", GREEN)],
                  top_left=(3.00, 1.93), row_h=0.88, key_w=1.83, width=2.88, size=32)
    if count:
        marks = VGroup(*(line((4.95 + 0.29 * i, 0.83), (4.90 + 0.29 * i, 1.23), TEXT, 5)
                         for i in range(count)))
        rows.rows[1][1] = marks
    else:
        rows.rows[1].remove(rows.rows[1][1])
    if not guess:
        rows.rows[0][1].set_opacity(0)
    return board, rows


def people(adult=True, facing=1):
    clothing = TEAL if adult else GOLD
    legs = VGroup(path((-0.21, 0.87), (-0.26, 0.46), (-0.33, 0.11), color="#273E56", width=13),
                  path((0.19, 0.87), (0.27, 0.43), (0.27, 0.11), color="#273E56", width=13))
    shoes = VGroup(oval(0.39, 0.18, BG, pt(-0.27, 0.085)), oval(0.39, 0.18, BG, pt(0.34, 0.085)))
    torso = slab(0.73, 0.84, clothing, pt(0, 1.16), r=0.24)
    neck = oval(0.24, 0.28, SKIN, pt(0.04, 1.59))
    head = VGroup(oval(0.64, 0.71, "#573C35", pt(-0.03, 1.95)),
                  oval(0.55, 0.63, SKIN, pt(0.08, 1.88)),
                  oval(0.39, 0.21, "#573C35", pt(-0.12, 2.14), -0.29),
                  oval(0.068, 0.063, BG, pt(0.23, 1.93)))
    arms = VGroup(path((-0.31, 1.40), (-0.47, 1.12), (-0.44, 0.87), color=clothing, width=10),
                  path((0.30, 1.40), (0.45, 1.16), (0.66, 1.13), color=clothing, width=10),
                  oval(0.19, 0.18, SKIN, pt(-0.44, 0.84)), oval(0.22, 0.18, SKIN, pt(0.70, 1.13)))
    figure = VGroup(legs, shoes, neck, torso, arms, head)
    if facing < 0:
        figure.flip(UP, about_point=ORIGIN)
    return figure


def hazard_mound():
    return VGroup(solid((-0.65, -0.20), (-0.40, 0.03), (-0.24, 0.20), (-0.04, 0.27),
                        (0.22, 0.20), (0.62, -0.20), color=WOOD),
                  oval(0.30, 0.11, DEEP_SOIL, pt(-0.02, 0.20)))


def disallow(mob, radius):
    circle = Circle(radius=radius, color=RED, stroke_width=5).move_to(mob)
    mid = circle.get_center()
    slash = Line(mid + UL * radius / np.sqrt(2), mid + DR * radius / np.sqrt(2),
                 color=RED, stroke_width=5)
    return VGroup(circle, slash)


def prediction():
    q = question_card(QUESTION, y=2.05, size=42, color=TEXT, max_w=10.1)
    plate = slab(q.width + 0.65, q.height + 0.48, BG, q.get_center())
    return VGroup(plate, q)


def prediction_view():
    return VGroup(yard(still=True, plain=True), *survey())


class S01Hook(SpokenScene):
    def construct(self):
        ground = yard()
        overhead = VGroup(
            slab(13.04, 6.95, "#65894C", r=0.27),
            solid((-6.50, 2.75), (6.50, 3.38), (6.50, 1.20), (-6.50, 0.28), color="#719653"),
            solid((-6.50, -0.76), (6.50, 0.15), (6.50, -1.38), (-6.50, -2.38), color="#759854"),
            solid((-6.50, -3.28), (6.50, -2.52), (6.50, -3.40), (-6.50, -3.40), color="#6B914C"),
        ).set_z_index(5)
        self.add(ground, overhead)
        self.at("patch of plain grass", lead=0.12)
        self.play(overhead.animate.stretch(0.16, 1, about_edge=DOWN).set_opacity(0), run_time=1.88)
        self.remove(overhead)
        self.at("give your child")
        a = ant(carry=True).scale(0.67).move_to(pt(-2.70, -0.86))
        s = spider(thread=True).scale(0.92).move_to(pt(4.03, 0.39))
        self.play(FadeIn(a), FadeIn(s, shift=DOWN * 0.4), run_time=0.45)
        bob(s, amp=0.12, speed=2.2)
        self.play(scuttle(a, RIGHT * 2.0), run_time=3.15, rate_func=linear)
        self.at("a string square")
        pegs, cord = survey()
        self.play(FadeIn(pegs), Create(cord), run_time=1.12)
        self.play(scuttle(a, RIGHT * 1.19), run_time=1.50, rate_func=linear)
        self.finish()


class S02Title(TitleCard):
    LESSON = "Backyard Habitat Hunt"
    TITLE = "Backyard Habitat Hunt: Parent Guide"

    def construct(self):
        self.add(yard(), *survey(), ant(carry=True).scale(0.67).move_to(pt(0.49, -0.86)))
        s = spider(thread=True).scale(0.92).move_to(pt(4.03, 0.39))
        self.add(bob(s, amp=0.12, speed=2.2))
        title = T(self.LESSON, size=55, font=TITLE_FONT).move_to(pt(0.75, 2.49))
        subtitle = label(self.TITLE.split(": ")[1], pt(0.75, 1.59), "#F5D587")
        self.play(FadeIn(title, shift=UP * 0.15), FadeIn(subtitle), run_time=0.44)
        self.wait(1.44)
        self.play(FadeOut(title), FadeOut(subtitle), run_time=0.12)


class S03Payoff(SpokenScene):
    def construct(self):
        self.add(yard(), *survey())
        a = ant(carry=True).scale(0.67).move_to(pt(0.49, -0.86))
        s = spider(thread=True).scale(0.92).move_to(pt(4.03, 0.39))
        self.add(a, bob(s, amp=0.12, speed=2.2))
        self.at("here is what")
        self.play(scuttle(a, RIGHT * 1.30), run_time=3.35, rate_func=linear)
        self.at("they practice slowing")
        lens = magnifier().scale(1.38).rotate(0.55).move_to(pt(-2.70, 1.50))
        self.play(FadeIn(lens), FadeOut(s), run_time=0.55)
        self.play(lens.animate.shift(RIGHT * 3.15 + DOWN * 0.90), run_time=2.30)
        self.at("with a count")
        board, rows = tally_board(count=1)
        self.play(FadeOut(lens), FadeIn(board), run_time=0.35)
        self.play(rows.reveal(1), run_time=0.45)
        self.at("they also sort")
        self.play(FadeOut(board), FadeOut(rows.everything()), run_time=0.35)
        living = leaf().scale(1.35).move_to(pt(-1.20, 1.65))
        nonliving = rock().scale(1.35).move_to(pt(1.40, 1.65))
        self.play(GrowFromCenter(living), GrowFromCenter(nonliving), run_time=0.55)
        living_name = label("Living", pt(-1.20, 2.65), GREEN)
        nonliving_name = label("Nonliving", pt(1.40, 2.65))
        self.play(FadeIn(living_name), FadeIn(nonliving_name), run_time=0.4)
        self.at("they discover")
        self.play(FadeOut(VGroup(living, nonliving, living_name, nonliving_name)), run_time=0.35)
        _, accent = survey()
        accent.set_stroke(TEXT, 7)
        self.play(Create(accent), a.animate.move_to(pt(0.0, -0.82)), run_time=2.15)
        self.at("every animal needs")
        self.play(FadeOut(accent), FadeOut(a), run_time=0.45)
        needs = (
            ("supplies food", "Food", food(), GOLD, -3.53),
            ("water", "Water", dew_grass(), BLUE, -1.65),
            ("air", "Air", breeze().scale(0.82), TEAL, 0.20),
            ("shelter", "Shelter", tunnel().scale(0.90), "#F0C39C", 2.24),
            ("space", "Space", span(), GREEN, 4.16),
        )
        for cue, word, icon, color, x in needs:
            self.at(cue, lead=0.31)
            icon.move_to(pt(x, 0.91))
            self.play(FadeIn(icon, shift=UP * 0.32), run_time=0.20)
            self.play(FadeIn(label(word, pt(x, 1.96), color, 31)), run_time=0.13)
        self.finish()


class S04PickSpot(SpokenScene):
    def construct(self):
        ground = yard()
        ground[8].set_z_index(2)
        self.add(ground)
        adult = people().scale(1.31).move_to(pt(-1.00, 0.39)).set_z_index(3)
        child = people(False, facing=-1).scale(0.90).move_to(pt(0.76, -0.05)).set_z_index(3)
        self.at("stay within")
        self.play(FadeIn(adult, shift=RIGHT * 0.40), FadeIn(child, shift=RIGHT * 0.40), run_time=0.75)
        self.play(adult.animate.shift(RIGHT * 0.15), child.animate.shift(RIGHT * 0.15), run_time=1.20)
        self.at("choose dry ground")
        road = VGroup(solid((-6.48, -0.77), (-5.25, -0.77), (-4.17, 0.33), (-5.14, 0.33), color="#39434C"),
                      line((-5.92, -0.63), (-5.53, -0.27), GREY, 2),
                      line((-5.34, -0.09), (-5.01, 0.24), GREY, 2)).set_z_index(1)
        pond = VGroup(oval(2.37, 0.82, "#3D899C", pt(4.79, -0.16), -0.10),
                      path((4.15, -0.17), (4.68, -0.14), (5.22, -0.24), color=BLUE, width=2)).set_z_index(1)
        self.play(FadeIn(road), FadeIn(pond), run_time=0.72)
        self.play(adult.animate.shift(LEFT * 0.30), child.animate.shift(LEFT * 0.30), run_time=1.99)
        self.at("check for glass")
        shard = solid((-0.31, -0.15), (0.09, 0.31), (0.36, -0.13), color="#A6D7DB").move_to(pt(1.67, -0.97))
        litter = solid((-0.33, 0.04), (-0.19, -0.17), (0.28, -0.12), (0.39, 0.11),
                       (0.03, 0.08), color=GREY).move_to(pt(2.58, -0.83))
        mound = hazard_mound().move_to(pt(3.35, -0.87))
        self.play(FadeIn(shard), run_time=0.38)
        self.at("sharp litter", lead=0.17)
        self.play(FadeIn(litter), run_time=0.36)
        self.at("ant mounds", lead=0.26)
        self.play(FadeIn(mound), run_time=0.42)
        self.play(adult.animate.shift(LEFT * 1.38), child.animate.shift(LEFT * 1.38), run_time=1.02)
        self.at("keep pebbles")
        attention = VGroup(hand().scale(2.08), rock().scale(0.31).move_to(pt(0.23, 0.12)),
                           slab(0.14, 0.53, WOOD, pt(-0.20, 0.24), r=0.06).rotate(-0.6))
        attention.move_to(pt(2.38, 1.38))
        self.play(FadeOut(VGroup(shard, litter, mound, pond, road)), FadeIn(attention), run_time=0.60)
        self.play(attention.animate.shift(UP * 0.65), adult.animate.shift(LEFT * 0.42),
                  child.animate.shift(LEFT * 0.42), run_time=2.68)
        self.at("away from children")
        small = label("Keep small objects away\nfrom children under 4", pt(0.45, -2.60), TEXT, 32)
        self.play(FadeIn(small), run_time=0.40)
        self.at("call 911")
        emergency = label("Choking? Call 911", pt(0.45, -2.60), "#FFD4C8", 34)
        self.play(swap(small, emergency, run_time=0.54), FadeOut(attention), run_time=0.54)
        self.finish()


class S04Setup(SpokenScene):
    def construct(self):
        self.add(yard())
        board = clipboard(pt(3.73, 1.46), width=4.13, height=3.00)
        string = coil().scale(1.34).move_to(pt(-3.0, 1.64))
        sticks = VGroup(*(slab(0.12, 0.94, WOOD, r=0.06).rotate(-0.22) for _ in CORNERS))
        sticks.arrange(RIGHT, buff=0.13).move_to(pt(-0.95, 1.63))
        pen = pencil().rotate(-0.65).move_to(pt(4.16, 1.33))
        paper = slab(1.62, 1.82, "#F4E4C9", pt(3.28, 1.52), r=0.05).rotate(0.10)
        lens = magnifier().scale(0.82).rotate(0.45).move_to(pt(0.75, 1.24))
        mitts = gloves().scale(0.90).move_to(pt(-1.92, -0.53))
        self.at("uses simple items")
        self.play(FadeIn(board, shift=LEFT * 0.26), run_time=0.75)
        self.at("bring about")
        self.play(Create(string), run_time=0.94)
        length = label("About 4½ meters", pt(-2.38, 2.70), TEXT, 29)
        self.play(FadeIn(length), run_time=0.29)
        self.at("four sticks")
        self.play(LaggedStart(*(FadeIn(stick, shift=UP * 0.28) for stick in sticks), lag_ratio=0.19), run_time=0.68)
        self.at("a pencil")
        self.play(FadeIn(pen, shift=LEFT * 0.28), run_time=0.42)
        self.at("and paper")
        paper.set_z_index(1)
        pen.set_z_index(2)
        self.play(FadeIn(paper, shift=UP * 0.22), run_time=0.48)
        self.at("add a magnifying")
        self.play(FadeIn(lens, shift=UP * 0.30), run_time=0.55)
        self.at("plus garden gloves")
        self.play(FadeIn(mitts, shift=UP * 0.37), run_time=0.54)
        self.at("push the four", lead=0.85)
        self.play(FadeOut(VGroup(length, board, paper, pen, lens, mitts)), run_time=0.65)
        pegs, cord = survey()
        self.play(LaggedStart(*(Transform(s, p) for s, p in zip(sticks, pegs)), lag_ratio=0.09), run_time=1.19)
        measure = span(7.86).rotate(PI).move_to(pt(0, -1.96))
        distance = label("About 1 meter", pt(0, -2.62), TEXT)
        self.play(Create(measure), FadeIn(distance), run_time=0.52)
        self.at("wrap the string")
        self.play(FadeOut(string), Create(cord), run_time=1.12)
        self.play(FadeOut(VGroup(distance, measure)), run_time=0.48)
        self.finish()


class S05Count(SpokenScene):
    def construct(self):
        self.add(yard(), *survey())
        board, rows = tally_board()
        self.at("before you look")
        self.play(FadeIn(board, shift=LEFT * 0.52), run_time=0.80)
        q = question_card("How many animals do you think\nwe will find in our square?",
                          y=1.90, size=32, color=TEXT, max_w=5.8).shift(LEFT * 0.45)
        bubble_box = slab(q.width + 0.55, q.height + 0.51, BG, q.get_center())
        tail_y = bubble_box.get_bottom()[1] + 0.04
        tail = solid((0.05, tail_y), (0.65, tail_y), (0.28, tail_y - 0.36), color=BG)
        bubble = VGroup(bubble_box, tail, q)
        self.at("how many animals")
        self.play(FadeIn(bubble, shift=RIGHT * 0.16), run_time=0.42)
        self.at("write down the guess")
        self.play(FadeOut(bubble), rows.reveal(0), run_time=0.43)
        writer = pencil().scale(0.67).rotate(-0.44).move_to(pt(4.24, 2.37))
        self.play(FadeIn(writer), run_time=0.28)
        question_mark = rows.rows[0][1].set_opacity(1)
        self.remove(question_mark)
        self.play(Write(question_mark), writer.animate.shift(RIGHT * 0.35 + DOWN * 0.36), run_time=0.63)
        self.play(FadeOut(writer), run_time=0.25)
        self.at("then spend")
        timer = VGroup(Circle(radius=0.71, color=GOLD, stroke_width=4),
                       line((0, 0), (0, 0.46), GOLD, 4), line((0, 0), (0.32, 0), GOLD, 4))
        timer.move_to(pt(-2.15, 1.67))
        watch = label("10 minutes", pt(-2.15, 2.83), TEXT, 31)
        self.play(FadeIn(timer), FadeIn(watch), run_time=0.42)
        self.play(Rotate(timer[1], angle=-PI * 0.72, about_point=timer.get_center()), run_time=1.98, rate_func=linear)
        self.at("part the grass")
        left, right, tool = pencil_and_grass()
        self.play(FadeOut(VGroup(timer, watch)), FadeIn(left), FadeIn(right), FadeIn(tool), run_time=0.47)
        self.play(Rotate(left, angle=0.43, about_point=pt(-0.28, -0.77)),
                  Rotate(right, angle=-0.44, about_point=pt(0.34, -0.77)),
                  tool.animate.shift(RIGHT * 0.70 + DOWN * 0.50), run_time=1.30)
        self.at("count each animal")
        a = ant().scale(0.52).move_to(pt(-0.44, -0.78))
        s = spider().scale(0.50).move_to(pt(1.32, -0.69))
        count = label("Count", pt(3.58, 1.05), GREEN)
        ticks = VGroup(line((4.87, 0.85), (4.83, 1.26), TEXT, 5),
                       line((5.17, 0.85), (5.13, 1.26), TEXT, 5))
        self.play(FadeOut(tool), FadeIn(a), FadeIn(count), Create(ticks[0]), run_time=0.53)
        self.play(scuttle(a, RIGHT * 0.56), FadeIn(s), Create(ticks[1]), run_time=0.65)
        self.play(scuttle(a, RIGHT * 0.41), s.animate.shift(UP * 0.17), run_time=1.18)
        self.finish()


class S06PredictQuestion(SpokenScene):
    def construct(self):
        ground = yard()
        self.add(ground, *survey())
        self.at("now picture that")
        near = tuft(0, -0.72, 0.90, still=True)
        self.add(near)
        self.play(near.animate.scale(0.52, about_point=pt(0, -0.72)).set_opacity(0), run_time=3.0)
        self.remove(near)
        self.at("from up here")
        plain = prediction_view()[0]
        ground[8].clear_updaters(recursive=True)
        self.play(Transform(ground[8], plain[8]), run_time=2.06)
        self.play(Transform(ground[2], plain[2]), run_time=0.62)
        self.at("what do you predict")
        self.play(FadeIn(prediction(), shift=UP * 0.18), run_time=0.53)
        self.play(Wiggle(ground[8], scale_value=1.018, rotation_angle=0.018, n_wiggles=2),
                  run_time=4.08)
        self.finish()


class S07PredictPause(Scene):
    def construct(self):
        self.camera.background_color = BG
        self.add(prediction_view(), prediction())
        self.wait(4.5)


class S08PredictReveal(SpokenScene):
    def construct(self):
        view = prediction_view()
        q = prediction()
        self.add(view, q)
        self.at("here", lead=0)
        self.play(FadeOut(q), run_time=0.32)
        new_yard = yard()
        self.play(Transform(view[0][8], new_yard[8].copy().clear_updaters(recursive=True)), run_time=0.35)
        self.remove(view)
        self.add(new_yard, *survey())
        left, right, tool = pencil_and_grass()
        self.add(left, right)
        self.at("parting the grass")
        self.play(FadeIn(tool), run_time=0.28)
        self.play(Rotate(left, angle=0.48, about_point=pt(-0.28, -0.77)),
                  Rotate(right, angle=-0.51, about_point=pt(0.34, -0.77)),
                  tool.animate.shift(RIGHT * 0.76 + DOWN * 0.48), run_time=0.73)
        a = ant().scale(0.84).move_to(pt(-0.87, -0.83))
        s = spider().scale(0.90).move_to(pt(1.70, -0.74))
        self.at("an ant")
        self.play(FadeIn(a), FadeOut(tool), run_time=0.45)
        self.at("a spider")
        self.play(FadeIn(s), run_time=0.41)
        self.play(scuttle(a, RIGHT * 0.64), s.animate.shift(RIGHT * 0.28), run_time=1.19)
        self.at("your square may")
        cloud = VGroup(oval(1.85, 0.48, "#B6C8C6", pt(-3.33, 2.34)),
                       oval(0.69, 0.59, "#B6C8C6", pt(-3.81, 2.47)),
                       oval(0.79, 0.76, "#B6C8C6", pt(-3.37, 2.58)),
                       oval(0.54, 0.48, "#B6C8C6", pt(-2.89, 2.46)))
        rain = VGroup(*(drop().scale(0.22).move_to(pt(x, y)) for x, y in
                        ((-3.99, 1.83), (-3.49, 1.98), (-3.02, 1.81))))
        self.play(FadeIn(cloud, shift=RIGHT * 0.50), run_time=0.46)
        self.play(FadeIn(rain, shift=DOWN * 0.28), scuttle(a, RIGHT * 0.57), run_time=1.24)
        self.play(rain.animate.shift(DOWN * 0.48), s.animate.shift(RIGHT * 0.35), run_time=1.35)
        self.at("grass itself")
        highlight = blade(-0.09, -0.78, 1.40, 0.25, 0.14, "#B6DB83")
        living = place_label(label("Living", ORIGIN, GREEN, 36), highlight, dirs=(UP,), buff=0.30)
        self.play(FadeOut(VGroup(cloud, rain)), GrowFromPoint(highlight, pt(-0.09, -0.78)), run_time=0.59)
        self.play(FadeIn(living), run_time=0.32)
        self.play(scuttle(a, RIGHT * 0.59), run_time=1.31)
        self.at("when you finish")
        self.play(FadeOut(VGroup(living, highlight, left, right)), run_time=0.50)
        board, rows = tally_board(guess=True, count=2)
        self.at("compare your count")
        self.play(FadeIn(board, shift=LEFT * 0.43), run_time=0.42)
        self.play(rows.reveal(0), run_time=0.32)
        self.play(rows.reveal(1), run_time=0.38)
        self.play(scuttle(a, RIGHT * 0.28), s.animate.shift(RIGHT * 0.34), run_time=1.13)
        self.finish()


def dotted(a, b):
    return DashedLine(pt(*a), pt(*b), dash_length=0.12, dashed_ratio=0.45,
                      stroke_color="#F2DDAB", stroke_width=3)


class S09SortNeeds(SpokenScene):
    def construct(self):
        self.add(yard(), *survey())
        a = ant().scale(0.84).move_to(pt(1.21, -0.83))
        self.add(a)
        self.at("help your child sort")
        panel = TwoPanel("Living", "Nonliving", colors=(GREEN, TEXT), top=2.92, bottom=0.26,
                         width=9.75, gap=0.44, size=34)
        back = VGroup(*(slab(f.width - 0.025, f.height - 0.025, PAPER, f.get_center())
                        for f in (panel.left_frame, panel.right_frame)))
        panel_shift = RIGHT * 0.90
        sheet = VGroup(back, panel).shift(panel_shift)
        self.play(FadeIn(sheet, shift=UP * 0.40), a.animate.shift(LEFT * 0.54), run_time=1.34)
        self.at("list living things")
        grass_icon = tuft(0, 0, 0.80, still=True).move_to(pt(-3.28, 1.20) + panel_shift)
        ant_icon = ant().scale(0.79).move_to(pt(-1.89, 1.20) + panel_shift)
        self.play(FadeIn(grass_icon, shift=UP * 0.28), run_time=0.52)
        self.at("and ants", lead=0.25)
        self.play(FadeIn(ant_icon, shift=RIGHT * 0.28), run_time=0.48)
        self.at("and nonliving")
        soil_icon = stone_soil().scale(0.84).move_to(pt(1.24, 1.21) + panel_shift)
        stone_icon = rock().scale(0.84).move_to(pt(2.55, 1.18) + panel_shift)
        sun_icon = sunlight(pt(3.77, 1.26) + panel_shift, 0.38)
        self.play(FadeIn(soil_icon, shift=UP * 0.27), run_time=0.48)
        self.at("rocks")
        self.play(FadeIn(stone_icon, shift=UP * 0.23), run_time=0.39)
        self.at("and sunlight", lead=0.12)
        self.play(GrowFromCenter(sun_icon), run_time=0.46)
        self.at("then pick one")
        self.play(FadeOut(VGroup(sheet, grass_icon, ant_icon, soil_icon, stone_icon, sun_icon)),
                  a.animate.scale(1.30).move_to(pt(0, -0.68)), run_time=1.07)
        self.play(a.animate.shift(LEFT * 0.36), run_time=1.22)
        self.at("where does this ant")
        meal = food().move_to(pt(-3.25, 0.95))
        trail_meal = dotted((-0.98, -0.39), (-2.79, 0.60))
        self.play(LaggedStart(GrowFromCenter(meal), Create(trail_meal), lag_ratio=0.25), run_time=0.63)
        self.play(FadeIn(label("Food", pt(-3.25, 1.84), GOLD)), run_time=0.24)
        self.at("where could it find")
        water = dew_grass().move_to(pt(3.00, 0.93))
        trail_water = dotted((0.31, -0.34), (2.54, 0.66))
        self.play(LaggedStart(GrowFromCenter(water), Create(trail_water), lag_ratio=0.24), run_time=0.63)
        self.play(FadeIn(label("Water", pt(3.00, 1.91), BLUE)), run_time=0.24)
        self.at("together trace")
        burrow = tunnel().scale(0.84).move_to(pt(-2.55, -2.46))
        trail_burrow = dotted((-0.80, -1.13), (-1.93, -2.11))
        self.play(GrowFromCenter(burrow), Create(trail_burrow), run_time=0.61)
        self.play(FadeIn(label("Shelter", pt(-4.22, -2.48), "#F0C39C")), run_time=0.23)
        self.at("and space", lead=0.65)
        room = span(10.05).move_to(pt(0, -3.21))
        trail_room = VGroup(dotted((0.04, -1.10), (0.75, -1.68)),
                            dotted((0.75, -1.68), (0.75, -3.08)))
        self.play(Create(room), Create(trail_room), run_time=0.35)
        self.play(FadeIn(label("Space", pt(2.06, -2.67), GREEN)), run_time=0.18)
        self.finish()


def fallen_log():
    wood = VGroup(slab(2.58, 1.18, "#9E6C48", r=0.29),
                  solid((-0.90, 0.23), (0.81, 0.31), (0.98, 0.22), (-0.18, 0.10),
                        (-0.99, 0.12), color="#BF8B55"),
                  solid((-1.12, -0.22), (-0.23, -0.31), (0.89, -0.25), (0.97, -0.39),
                        (-0.28, -0.44), color="#754D38")).shift(LEFT * 0.43)
    end = VGroup(oval(0.93, 1.18, "#CE9C67"),
                 Ellipse(width=0.66, height=0.89, color="#91613F", stroke_width=3),
                 Ellipse(width=0.40, height=0.59, color="#91613F", stroke_width=2.5),
                 oval(0.12, 0.19, "#91613F"),
                 line((0.04, 0.09), (0.32, 0.39), "#91613F", 2.5)).shift(RIGHT * 0.85)
    return VGroup(wood, end)


def pillbug():
    body = oval(0.76, 0.42, "#A5A5A4")
    bands = VGroup(*(path((x, -0.15), (x - 0.045, 0.0), (x, 0.16), color="#555B61", width=2.5)
                     for x in (-0.19, -0.06, 0.07, 0.20)))
    return VGroup(body, bands)


class S10SafetyLog(SpokenScene):
    def construct(self):
        self.add(yard(), *survey())
        wood = fallen_log().move_to(pt(1.90, -0.66)).set_z_index(2)
        adult = people(facing=-1).scale(1.37).move_to(pt(5.35, 0.63))
        child = people(False).scale(0.91).move_to(pt(-1.62, -0.01))
        self.at("you can skip")
        self.play(FadeIn(wood, shift=LEFT * 0.36), run_time=0.67)
        self.play(FadeIn(adult), FadeIn(child), run_time=0.78)
        self.at("have your child")
        self.play(child.animate.shift(LEFT * 1.75), run_time=1.03)
        self.at("put on garden", lead=0.25)
        self.play(*(palm.animate.set_fill("#80CCC5").scale(1.25) for palm in adult[4][2:]), run_time=0.54)
        self.at("choose a light log")
        exposed = oval(1.36, 0.46, "#825B40", pt(1.28, -0.99)).set_z_index(1)
        self.add(exposed)
        self.at("roll it toward", lead=0.26)
        original = wood.copy()
        rolled = wood.copy().shift(RIGHT * 0.96)
        # Only the grain on the end rotates. The trunk and contact height stay fixed.
        rolled[1][1:].rotate(-0.71, about_point=rolled[1][0].get_center())
        self.play(Transform(wood, rolled), run_time=1.99)
        self.at("look underneath")
        bugs = VGroup(pillbug().scale(0.49).rotate(0.20).move_to(pt(0.83, -0.90)),
                      pillbug().scale(0.43).rotate(-0.32).move_to(pt(1.15, -1.06))).set_z_index(1)
        self.play(FadeIn(bugs), run_time=0.41)
        self.play(bugs[0].animate.shift(LEFT * 0.13), run_time=0.53)
        self.at("gently roll it")
        self.play(Transform(wood, original), FadeOut(bugs), run_time=1.50)
        self.remove(exposed)
        self.finish()


def eye():
    upper = ArcBetweenPoints(LEFT * 0.73, RIGHT * 0.73, angle=-1.38, color=TEXT, stroke_width=5)
    lower = ArcBetweenPoints(LEFT * 0.73, RIGHT * 0.73, angle=1.38, color=TEXT, stroke_width=5)
    pupil = VGroup(oval(0.48, 0.48, TEAL), oval(0.24, 0.24, BG), oval(0.085, 0.085, TEXT, pt(0.09, 0.07)))
    return VGroup(upper, lower, pupil)


def beetle():
    legs = VGroup(*(path((0, y), (side * 0.34, y), (side * 0.54, y - 0.16),
                         color=GOLD, width=4) for side in (-1, 1) for y in (-0.31, -0.04, 0.23)))
    shell = oval(0.75, 1.03, "#BD7556")
    head = oval(0.40, 0.42, WOOD, pt(0, 0.48))
    split = line((0, -0.47), (0, 0.37), "#794D42", 3)
    return VGroup(legs, head, shell, split)


def berries():
    stem = path((-0.28, -0.01), (0.01, 0.16), (0.04, 0.40), color=GREEN, width=4)
    return VGroup(stem, oval(0.39, 0.38, "#CE6C81", pt(-0.22, -0.11)),
                  oval(0.39, 0.38, "#A54266", pt(0.19, -0.08)), leaf().scale(0.29).move_to(pt(0.14, 0.33)))


def mushroom():
    return VGroup(slab(0.26, 0.59, "#E3C598", pt(0, -0.17), r=0.09),
                  oval(0.84, 0.47, "#B27157", pt(0, 0.14)),
                  oval(0.11, 0.077, "#E3C598", pt(0.18, 0.21)),
                  oval(0.12, 0.08, "#E3C598", pt(-0.12, 0.29)))


class S11SafetyHands(SpokenScene):
    def construct(self):
        self.add(yard(), *survey())
        cover = rock().scale(1.30).move_to(pt(0.63, -0.88))
        palm = hand().scale(0.84).rotate(-2.15).move_to(pt(-1.29, 0.09))
        self.at("never put hands")
        self.play(FadeIn(cover), FadeIn(palm, shift=RIGHT * 0.26), run_time=0.60)
        self.play(palm.animate.shift(RIGHT * 0.42), run_time=0.60)
        stop = disallow(palm, 0.74)
        self.play(Create(stop), run_time=0.49)
        self.at("step back", lead=0.70)
        self.play(FadeOut(VGroup(palm, stop)), run_time=0.48)
        snake = VGroup(path((1.13, -0.89), (1.52, -0.69), (1.87, -0.97), (2.34, -0.99),
                            (2.59, -0.75), color="#D8B777", width=11),
                       oval(0.40, 0.24, "#D8B777", pt(2.62, -0.73), 0.25),
                       oval(0.056, 0.05, BG, pt(2.69, -0.68)))
        child = people(False).scale(0.88).move_to(pt(-1.03, 0.11))
        self.play(FadeIn(snake), FadeIn(child), run_time=0.52)
        self.play(child.animate.shift(LEFT * 1.74), run_time=1.24)
        self.at("watch animals")
        bug = beetle().scale(1.06).rotate(-0.80).move_to(pt(0.60, -0.49))
        look = eye().scale(1.04).move_to(pt(-1.85, 0.91))
        self.play(FadeOut(VGroup(snake, child, cover)), run_time=0.37)
        self.play(GrowFromCenter(bug), FadeIn(look), run_time=0.54)
        self.play(bug.animate.shift(RIGHT * 0.64), run_time=1.24, rate_func=linear)
        self.at("keep your hands")
        safe = label("Look, do not touch", pt(-0.50, 2.07), TEXT, 35)
        self.play(FadeIn(safe), bug.animate.shift(RIGHT * 0.42), run_time=0.58)
        self.at("never taste")
        self.play(FadeOut(VGroup(bug, look, safe)), run_time=0.31)
        foods = VGroup(leaf().scale(1.40), berries().scale(1.33), mushroom().scale(1.28))
        foods.arrange(RIGHT, buff=0.89).move_to(pt(0.30, 1.40))
        signs = VGroup(*(disallow(item, 0.78) for item in foods))
        for item, sign in zip(foods, signs):
            self.play(FadeIn(item), run_time=0.24)
            self.play(Create(sign), run_time=0.39)
        self.at("handle any glass", lead=0.58)
        self.play(FadeOut(VGroup(foods, signs)), run_time=0.37)
        adult = people().scale(1.52).move_to(pt(-0.87, 0.67))
        grip = adult[4][3].get_center()
        glass = magnifier().scale(1.04).rotate(-0.69)
        glass.shift(grip - glass[0].get_center())
        self.play(FadeIn(adult, shift=RIGHT * 0.36), run_time=0.52)
        self.play(FadeIn(glass, shift=DOWN * 0.24), run_time=0.55)
        self.at("keep every magnifying")
        self.play(Rotate(glass, angle=-1.37, about_point=grip), run_time=1.42)
        patch = tuft(grip[0] + 0.89, -0.82, 0.62, still=True)
        self.play(FadeIn(patch), run_time=0.55)
        self.wait(0.70)
        self.finish()


def wash(at):
    palm = hand().scale(0.82).rotate(-0.79).move_to(at + DOWN * 0.28)
    drops = VGroup(*(drop().scale(0.22).move_to(at + pt(x, y)) for x, y in
                     ((-0.41, 0.51), (0.08, 0.76), (0.46, 0.56))))
    bubbles = VGroup(*(Circle(radius=r, color=TEXT, stroke_width=2.7).move_to(at + pt(x, y))
                       for x, y, r in ((-0.60, 0.02, 0.12), (0.40, 0.14, 0.16), (0.12, 0.33, 0.11))))
    return VGroup(palm, drops, bubbles)


def tick():
    legs = VGroup(*(path((0, y), (side * 0.32, y + 0.12), (side * 0.46, y - 0.06),
                         color=WOOD, width=3.5) for side in (-1, 1)
                    for y in (-0.27, -0.12, 0.03, 0.18)))
    return VGroup(legs, oval(0.56, 0.69, "#B48762", pt(0, -0.05)),
                  oval(0.32, 0.29, "#815642", pt(0, 0.27)))


class S12Close(SpokenScene):
    def construct(self):
        self.add(yard())
        pegs, cord = survey()
        palm = hand().scale(1.10).rotate(2.20).move_to(pt(-3.21, 0.42))
        restored = leaf().move_to(pt(-0.23, 1.66))
        self.add(pegs, cord)
        self.at("pull up the sticks")
        self.play(FadeIn(palm, shift=DOWN * 0.33), run_time=0.32)
        self.play(LaggedStart(*(FadeOut(peg, shift=UP * 0.70 + RIGHT * 0.15) for peg in pegs), lag_ratio=0.13),
                  Transform(cord, coil().scale(0.90).move_to(pt(-2.96, 1.00))),
                  palm.animate.shift(RIGHT * 0.37 + UP * 0.59), run_time=1.32)
        self.play(FadeOut(VGroup(palm, cord), shift=UP * 0.30), run_time=0.43)
        self.at("put back any")
        self.play(FadeIn(restored), run_time=0.31)
        self.play(restored.animate.rotate(-0.37).move_to(pt(-0.53, -0.87)), run_time=1.29)
        self.at("wash hands")
        handwashing = wash(pt(-2.43, 1.10)).scale(1.12)
        self.play(FadeIn(handwashing), run_time=0.44)
        self.play(handwashing[1].animate.shift(DOWN * 0.28),
                  handwashing[2].animate.shift(UP * 0.20), run_time=1.17)
        self.at("check for ticks")
        inspection = magnifier().scale(1.13).rotate(-0.68).move_to(pt(2.31, 1.27))
        bug = tick().scale(0.81).move_to(inspection[1].get_center())
        self.play(FadeIn(inspection), FadeIn(bug), run_time=0.44)
        self.play(VGroup(inspection, bug).animate.shift(LEFT * 0.48), run_time=1.01)
        self.at("think back")
        self.play(FadeOut(VGroup(handwashing, inspection, bug)), run_time=0.46)
        a = ant().scale(0.79).move_to(pt(-2.88, -0.77))
        self.play(FadeIn(a), run_time=0.37)
        self.play(scuttle(a, RIGHT * 1.88), run_time=1.79, rate_func=linear)
        self.at("its habitat")
        self.play(scuttle(a, RIGHT * 3.97), run_time=3.29, rate_func=linear)
        self.finish()


class S13End(EndCard):
    LINE = "A habitat gives an animal food, water, air, shelter, and space."
