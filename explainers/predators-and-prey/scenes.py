"""Why the Wolves Never Finish the Moose — Predators and Prey.

Color map: brown moose, grey wolves, green firs, blue lake, orange low ratio.
The icons illustrate relative abundance. The population totals supply the numbers.
"""
import re

from bp_parts import *


MOOSE_BROWN = "#B8783F"
WOLF_GREY = "#AAB1BA"
TREE_GREEN = "#58B66B"
ORANGE = "#F59E42"
LAKE_BLUE = "#347FA3"
SNOW = "#EAF2F6"

WATER = "#193E55"
SHELF = "#28607D"
SHORE = "#40647B"
SNOWFIELD = "#53788C"
DRIFT = "#618699"
HIDE = "#865131"
ANTLER = "#E0B38A"
WOLF_SHADE = "#6E7C8A"
INK = "#222D37"

CORNER = (4.33, 2.52, 0)
TAKEAWAY = "Wolves usually run short of food before the moose run out."
PREDICTION_SETUP = "Only 10 moose for\neach wolf."
PREDICTION_QUESTION = "What happens to\nthe wolves next?"
PREDICTION_CENTER = 4.33

START_MOOSE, START_WOLVES = 1000, 10
HUNT_MOOSE, PACK_WOLVES = 840, 30
LOW_MOOSE, FEWER_WOLVES = 300, 12
RECOVERED_MOOSE = 600
LOW_RATIO = LOW_MOOSE / PACK_WOLVES

MOOSE_SITES = ((-4.78, 0.98), (-3.46, -0.03), (-0.82, 0.97), (-3.25, 1.42),
               (-1.62, -0.77), (-5.23, -0.66), (-0.47, -0.35), (-3.64, -1.38))
WOLF_SITES = ((-2.13, 0.55), (-0.13, -1.17), (-4.35, -1.42), (-1.74, 1.61),
              (-2.52, -1.47), (0.37, 0.39))
INTRO_MOOSE = ((-4.83, 0.47), (-3.28, 0.96), (-3.27, -0.68), (-4.42, -1.03))
INTRO_WOLVES = ((-0.58, 0.68), (0.08, -0.60))


def point(x, y):
    return [x, y, 0]


def shape(vertices, color):
    return Polygon(*[point(x, y) for x, y in vertices], stroke_width=0,
                   fill_color=color, fill_opacity=1)


def oval(width, height, color, x=0, y=0):
    return Ellipse(width=width, height=height, stroke_width=0,
                   fill_color=color, fill_opacity=1).move_to(point(x, y))


def fir(height=1.15):
    trunk = shape([(-0.06, -0.55), (0.06, -0.55), (0.05, -0.09), (-0.05, -0.09)], HIDE)
    crown = shape([(0, 0.70), (0.23, 0.30), (0.14, 0.32), (0.33, 0.02),
                   (0.23, 0.06), (0.44, -0.27), (0.20, -0.37), (-0.36, -0.34),
                   (-0.44, -0.26), (-0.22, 0.06), (-0.31, 0.01), (-0.13, 0.33),
                   (-0.22, 0.29)], TREE_GREEN)
    shade = shape([(0, 0.62), (0.12, 0.25), (0.30, 0.02), (0.20, 0.05),
                   (0.42, -0.27), (0.20, -0.37), (0, -0.37)], "#36764F")
    snow = shape([(-0.27, -0.03), (-0.13, 0.18), (0.01, 0.12), (0.16, 0.13),
                  (0.30, 0.01), (0.05, 0.04), (-0.10, -0.07)], "#A6C6C8")
    return VGroup(trunk, crown, shade, snow).set_height(height)


def moose(height=0.9, *, left=False, calf=False, browse=False):
    legs = VGroup(*[
        shape([(x - 0.08, -0.14), (x + 0.09, -0.14), (x + 0.05, -0.51),
               (x + 0.09, -0.65), (x - 0.08, -0.65), (x - 0.12, -0.49)], color)
        for x, color in ((-0.38, HIDE), (0.38, HIDE), (-0.53, MOOSE_BROWN), (0.25, MOOSE_BROWN))
    ])
    body = oval(1.38, 0.61, MOOSE_BROWN, -0.15, 0.04)
    belly = oval(1.10, 0.17, HIDE, -0.15, -0.145)
    neck = shape([(0.11, -0.12), (0.15, 0.29), (0.37, 0.47), (0.66, 0.49),
                  (0.59, 0.13), (0.39, -0.33), (0.31, -0.12)], MOOSE_BROWN)
    muzzle = shape([(0.38, 0.49), (0.69, 0.53), (0.85, 0.40), (1.02, 0.33),
                    (0.99, 0.14), (0.72, 0.15), (0.56, 0.25), (0.40, 0.31)], MOOSE_BROWN)
    nose = oval(0.23, 0.14, HIDE, 0.91, 0.245)
    ear = shape([(0.51, 0.45), (0.26, 0.59), (0.27, 0.69), (0.47, 0.62), (0.61, 0.47)], MOOSE_BROWN)
    eye = Dot(point(0.69, 0.40), radius=0.035, color=INK)
    head = VGroup(neck, muzzle, nose, ear, eye)
    if not calf:
        antlers = VGroup(
            shape([(0.61, 0.46), (0.52, 0.64), (0.35, 0.72), (0.20, 0.90), (0.19, 1.04),
                   (0.32, 0.96), (0.38, 1.06), (0.44, 0.86), (0.53, 0.81),
                   (0.58, 1.01), (0.65, 0.92), (0.65, 0.74), (0.71, 0.57)], ANTLER),
            shape([(0.57, 0.61), (0.72, 0.72), (0.82, 0.92), (0.89, 0.87),
                   (0.87, 0.70), (0.70, 0.54)], "#BC8A62"),
        )
        head.add_to_back(antlers)
    if browse:
        head.rotate(-0.62, about_point=point(0.23, 0.19))
    animal = VGroup(legs, body, belly, head)
    if left:
        animal.flip(UP)
    return animal.set_height(height)


def wolf(height=0.62, *, left=False, pup=False, fed=False, seated=False):
    feet = VGroup(*[
        shape([(x - 0.09, -0.08), (x + 0.08, -0.09), (x + 0.04, -0.36),
               (x + 0.16, -0.42), (x + 0.16, -0.49), (x - 0.08, -0.49)], color)
        for x, color in ((-0.32, WOLF_SHADE), (0.44, WOLF_SHADE), (-0.45, WOLF_GREY), (0.32, WOLF_GREY))
    ])
    tail = shape([(-0.50, 0.23), (-0.85, 0.14), (-1.13, -0.17), (-1.00, -0.17),
                  (-0.75, -0.06), (-0.47, 0.04)], WOLF_SHADE)
    haunch = oval(0.46, 0.53, WOLF_GREY, -0.43, -0.19)
    if not seated:
        haunch.set_fill(opacity=0)
    body = oval(1.24, 0.59 if fed else 0.43, WOLF_GREY, -0.10, 0.03)
    saddle = oval(0.94, 0.16, WOLF_SHADE, -0.23, 0.17)
    head = shape([(0.21, -0.13), (0.24, 0.21), (0.49, 0.32), (0.56, 0.60), (0.69, 0.36),
                  (0.81, 0.31), (1.04, 0.23), (1.03, 0.11), (0.76, 0.05), (0.55, -0.16)], WOLF_GREY)
    ear = shape([(0.54, 0.34), (0.57, 0.51), (0.64, 0.36)], WOLF_SHADE)
    nose = oval(0.12, 0.08, INK, 1.00, 0.20)
    eye = Dot(point(0.72, 0.27), radius=0.030, color=INK)
    animal = VGroup(tail, feet, haunch, body, saddle, head, ear, nose, eye)
    if pup:
        animal.stretch(0.83, 0)
    if left:
        animal.flip(UP)
    return animal.set_height(height)


def lake():
    water = oval(9.30, 5.48, WATER, -2.04, -0.07)
    banks = VGroup(*[
        oval(w, h, SHELF, x, y).rotate(angle)
        for x, y, w, h, angle in ((-5.89, 0.94, 0.60, 0.065, 0.7),
                                   (-5.65, 1.69, 0.77, 0.05, 0.62),
                                   (1.65, 0.73, 0.86, 0.06, -0.58),
                                   (0.85, -1.98, 0.84, 0.065, 0.43),
                                   (-2.03, -2.60, 1.40, 0.06, 0.04))
    ])
    return VGroup(water, banks)


def island_land():
    outline = [(-6.15, -0.11), (-5.94, 0.73), (-5.45, 1.25), (-4.51, 1.61),
               (-3.92, 2.10), (-2.75, 2.18), (-2.13, 2.03), (-1.45, 2.27),
               (-0.49, 2.12), (0.20, 1.75), (0.56, 1.19), (1.36, 0.76),
               (1.64, 0.28), (1.49, -0.39), (0.98, -0.71), (0.74, -1.31),
               (0.08, -1.88), (-0.76, -2.03), (-1.51, -1.90), (-2.28, -2.27),
               (-3.51, -2.38), (-4.28, -2.05), (-5.04, -1.99), (-5.66, -1.48),
               (-5.89, -0.91)]
    shelf = shape(outline, SHELF).scale(1.055)
    shore = shape(outline, SHORE)
    field = shape(outline, SNOWFIELD).scale(0.943).shift(UP * 0.08)
    drifts = VGroup(
        shape([(-5.8, -0.31), (-5.41, 0.46), (-4.84, 0.64), (-4.22, 0.49),
               (-4.75, 0.31), (-5.13, -0.17), (-5.48, -0.37)], DRIFT),
        shape([(-4.92, -1.66), (-4.27, -1.77), (-3.66, -2.13), (-2.33, -2.05),
               (-1.65, -1.75), (-2.48, -1.89), (-3.48, -1.87), (-4.24, -1.58)], DRIFT),
        shape([(-2.00, 1.80), (-1.43, 2.02), (-0.63, 1.94), (-0.12, 1.59),
               (-0.67, 1.68), (-1.17, 1.79)], DRIFT),
        shape([(0.39, 1.02), (1.22, 0.62), (1.39, 0.19), (1.28, -0.17),
               (1.14, 0.26), (0.83, 0.58)], DRIFT),
    )
    trees = VGroup(*[
        fir(h).move_to(point(x, y))
        for x, y, h in ((-5.31, 0.36, 1.04), (-4.62, 1.63, 0.84), (-4.50, -0.58, 0.92),
                         (-2.84, 0.63, 0.80), (-1.02, -1.23, 0.91), (0.21, 1.23, 0.99),
                         (0.67, 0.84, 0.69), (0.62, -0.69, 0.94))
    ])
    return VGroup(shelf, shore, field, drifts, trees)


def island(moose_ids=range(8), wolf_ids=range(2), *, introduction=False):
    ms = INTRO_MOOSE if introduction else MOOSE_SITES
    ws = INTRO_WOLVES if introduction else WOLF_SITES
    moose_icons = VGroup(*[moose(0.91, left=introduction or i % 3 == 1)
                           .move_to(point(*ms[i])) for i in moose_ids])
    wolf_icons = VGroup(*[wolf(0.63, left=introduction or i % 3 == 2)
                          .move_to(point(*ws[i])) for i in wolf_ids])
    world = VGroup(lake(), island_land(), moose_icons, wolf_icons)
    world.moose, world.wolves = moose_icons, wolf_icons
    return world


def model_tag():
    return scope_tag("model (schematic)", size=28, color=TEXT).move_to(point(-5.12, -3.53))


def ratio_box(value, *, at=CORNER, size=28):
    """Fit a panel once around the largest counter string, then replace its numeric field."""
    panel = boxed_label("moose per wolf: 100", size=size, pad=0.27, color=GREY, fill_opacity=1)
    panel.box.set_fill("#272C35", opacity=1)
    panel.move_to(at)
    name = T("moose per wolf:", size, TEXT).align_to(panel.label, LEFT).set_y(at[1])
    slot = (name.get_right()[0] + panel.label.get_right()[0]) / 2 + 0.065
    digits = counter("{:.0f}", value, at=point(slot, at[1]), size=size)

    def shade():
        return ORANGE if round(value.get_value()) <= LOW_RATIO else TEXT

    digits.set_color(shade())
    digits.add_updater(lambda mob: mob.set_color(shade()))
    panel.box.add_updater(lambda mob: mob.set_stroke(ORANGE if shade() == ORANGE else GREY))
    panel.box.update()
    return VGroup(panel.box, name, digits)


def ratio_for(moose_total, wolf_total):
    """Expose the quotient to the shared counter without introducing a second animated value."""
    value = ValueTracker(moose_total.get_value() / wolf_total.get_value())
    value.add_updater(lambda tracker: tracker.set_value(moose_total.get_value() / wolf_total.get_value()))
    return value


def totals(moose_total, wolf_total):
    return VGroup(counter("{:,.0f} moose", moose_total, point(4.33, 1.19), size=34,
                          color="#E5AC77", mono=False),
                  counter("{:,.0f} wolves", wolf_total, point(4.33, 0.35), size=34,
                          color=WOLF_GREY, mono=False))


def readout(moose_total, wolf_total):
    ratio = ratio_for(moose_total, wolf_total)
    return ratio, ratio_box(ratio), totals(moose_total, wolf_total)


def ratio_outline(box, color=GOLD):
    return SurroundingRectangle(box, color=color, buff=0.12, corner_radius=0.19, stroke_width=4)


def animal_halos(animals, color):
    """Spotlight a population while its members are being counted or compared."""
    for animal in animals:
        animal.set_z_index(2)
    return VGroup(*[
        Ellipse(width=animal.width + 0.50, height=animal.height + 0.38,
                color=color, stroke_width=4, fill_opacity=0.35)
        .move_to(animal).set_z_index(1)
        for animal in animals
    ])


def lake_superior_map():
    # North is up. The Keweenaw Peninsula projects from the south shore below Isle Royale.
    shore = shape([(-5.75, -0.60), (-5.04, 0.06), (-4.84, 0.53), (-4.10, 0.72),
                   (-3.76, 1.20), (-3.27, 1.38), (-3.02, 1.88), (-2.58, 1.69),
                   (-2.23, 2.02), (-1.72, 1.91), (-1.52, 2.23), (-0.90, 2.15),
                   (-0.55, 1.90), (-0.26, 2.08), (0.15, 1.94), (0.54, 1.55),
                   (0.42, 1.31), (1.08, 1.44), (1.64, 1.10), (1.78, 0.69),
                   (2.29, 0.42), (2.12, 0.13), (1.81, 0.14), (2.26, -0.24),
                   (2.79, -0.43), (2.74, -0.76), (2.48, -1.09), (2.47, -1.41),
                   (1.83, -1.54), (1.17, -1.35), (0.69, -1.41), (0.21, -1.14),
                   (-0.51, -1.20), (-1.25, -0.89), (-1.94, -0.91), (-2.21, -0.43),
                   (-1.96, -0.02), (-1.32, 0.26), (-1.46, 0.42), (-2.03, 0.29),
                   (-2.52, 0.10), (-2.89, -0.36), (-3.48, -0.51), (-3.91, -0.49),
                   (-4.65, -0.83), (-5.48, -0.79)], LAKE_BLUE)
    halo = shape([(-6.02, -0.59), (-5.34, 0.22), (-4.15, 1.39), (-3.19, 2.12),
                  (-1.88, 2.49), (-0.40, 2.32), (0.72, 1.87), (1.94, 1.39),
                  (2.45, 0.62), (3.03, -0.41), (2.89, -1.60), (1.92, -1.91),
                  (0.50, -1.69), (-0.74, -1.53), (-2.15, -1.29), (-3.45, -0.86),
                  (-4.89, -1.13), (-5.89, -0.91)], WATER)
    isle = shape([(-2.94, 0.80), (-2.76, 1.00), (-2.44, 1.16), (-2.06, 1.28),
                  (-1.87, 1.23), (-2.10, 1.08), (-2.63, 0.88), (-2.79, 0.78)], GOLD)
    return VGroup(halo, shore), isle


def word_reveal(text):
    """Reveal the already positioned glyphs in whole words, with their original kerning."""
    spans = [match.span() for match in re.finditer(r"\S+", text.text)]

    def reveal(mob, alpha):
        visible = min(len(spans), 1 + int(alpha * len(spans)))
        for index, (first, last) in enumerate(spans):
            for glyph in mob.chars[first:last]:
                glyph.set_fill(opacity=float(index < visible))

    return UpdateFromAlphaFunc(text, reveal, rate_func=linear)


def den():
    mound = oval(1.92, 0.91, DRIFT, -4.89, -1.35)
    door = oval(0.83, 0.61, WATER, -4.89, -1.43)
    sill = oval(1.16, 0.14, SNOWFIELD, -4.86, -1.69)
    return VGroup(mound, door, sill)


def snow_detail():
    """A close view of the same snowy ground for small animals and short actions."""
    bank = oval(4.42, 1.86, SHELF, 4.33, -1.87)
    snow = oval(4.23, 1.68, SNOWFIELD, 4.33, -1.83)
    drift = oval(2.61, 0.12, DRIFT, 4.35, -2.42)
    return VGroup(bank, snow, drift)


def low_state():
    world = island(range(3), range(6))
    box = ratio_box(ValueTracker(LOW_RATIO))
    counts = totals(ValueTracker(LOW_MOOSE), ValueTracker(PACK_WOLVES))
    return VGroup(world, box, counts, model_tag())


def prediction():
    panel = boxed_label("What happens to", size=30, color=GOLD,
                        box=(4.48, 2.16), fill_opacity=1).box
    panel.set_fill("#3A3022", opacity=1).move_to(point(PREDICTION_CENTER, -1.36))
    setup = question_card(PREDICTION_SETUP, y=-0.81, size=30, max_w=4.04,
                          color=TEXT).question.set_x(PREDICTION_CENTER)
    prompt = question_card(PREDICTION_QUESTION, y=-1.87, size=33, max_w=4.04,
                           color=YELLOW).question.set_x(PREDICTION_CENTER)
    return panel, setup, prompt


def prediction_timer(seconds, center):
    # Use the shared counter's tracker and base ring. A wide band makes the five-second fill legible.
    ring, drain = countdown(seconds, center=center, radius=0.61)
    progress = drain.mobject
    progress.set_value(0)
    band = always_redraw(lambda: AnnularSector(
        inner_radius=0.24, outer_radius=0.60,
        start_angle=PI / 2, angle=max(0.001, progress.get_value()) * TAU,
        color=GOLD, fill_opacity=1, stroke_width=0, arc_center=center,
    ))
    return VGroup(ring[0], band), progress


def cycle():
    """Four fixed steps around the island, with room between every arrow and chip."""
    labels = VGroup(*[
        boxed_label(label, color=color, size=28, pad=0.19).move_to(point(x, y))
        for label, color, x, y in (("many moose", "#E5AC77", -4.79, 2.84),
                                    ("wolves increase", WOLF_GREY, -0.04, 2.84),
                                    ("fewer moose", "#E5AC77", -0.04, -2.90),
                                    ("wolves decrease", WOLF_GREY, -4.57, -2.90))
    ])
    top_left, top_right, bottom_right, bottom_left = labels
    arrows = VGroup(
        Arrow(top_left.get_right(), top_right.get_left(), buff=0.19, color=GOLD, stroke_width=5),
        CurvedArrow(top_right.get_right() + RIGHT * 0.16 + DOWN * 0.11,
                    bottom_right.get_right() + RIGHT * 0.16 + UP * 0.11, angle=-0.60,
                    color=GOLD, stroke_width=5, tip_length=0.20),
        Arrow(bottom_right.get_left(), bottom_left.get_right(), buff=0.18, color=GOLD, stroke_width=5),
        CurvedArrow(bottom_left.get_left() + LEFT * 0.14 + UP * 0.12,
                    top_left.get_left() + LEFT * 0.14 + DOWN * 0.12, angle=-0.36,
                    color=GOLD, stroke_width=5, tip_length=0.20),
    )
    return labels, arrows


class S00Title(TitleCard):
    LESSON = "Predators and Prey"
    TITLE = "Why the Wolves Never Finish the Moose"

    def construct(self):
        meadow = VGroup(lake(), island_land()).move_to(point(0, -0.69))
        animals = VGroup(moose(1.60, left=True).move_to(point(2.16, -0.52)),
                         wolf(1.30).move_to(point(-2.74, -1.28)))
        lesson = T(self.LESSON.upper(), size=28, color=TEAL, weight=BOLD).move_to(point(0, 3.38))
        title = fit_text(self.TITLE, max_w=12, size=52, min_size=44,
                         font=TITLE_FONT).move_to(point(0, 2.52))
        self.add(meadow, animals, lesson, title)
        self.wait(1.65)
        self.play(FadeOut(lesson), FadeOut(title), run_time=0.35)
        self.wait(1.0)


class S01Question(SpokenScene):
    def construct(self):
        backdrop = VGroup(lake(), island_land())
        hunter = wolf(1.29).move_to(point(-4.38, -0.63))
        prey = moose(1.68, left=True).move_to(point(-0.33, 0.14))
        opening = T("If wolves eat moose,", 39, GOLD, font=TITLE_FONT, disable_ligatures=True)
        puzzle = T("why don't the wolves eat every last moose?", 35, TEXT, font=TITLE_FONT,
                   disable_ligatures=True)
        opening.move_to(point(-2.10, 3.27))
        puzzle.move_to(point(-1.55, -2.98))
        tag = model_tag()
        self.add(backdrop, hunter, prey, tag)
        self.at("If wolves eat moose")
        self.play(word_reveal(opening), run_time=1.32)
        self.at("why don't the wolves")
        self.play(word_reveal(puzzle), hunter.animate.shift(RIGHT * 0.84), run_time=2.23)

        map_art, isle = lake_superior_map()
        isle_label = place_label(T("Isle Royale", 31, GOLD, weight=BOLD), isle,
                                 dirs=(UP,), buff=1.16)
        self.at("On one real island")
        self.play(FadeOut(VGroup(backdrop, hunter, prey, opening, puzzle, tag)),
                  FadeIn(map_art, shift=RIGHT * 0.65), run_time=0.81)
        self.at("in Lake Superior")
        self.play(FadeIn(isle), run_time=0.56)
        self.play(FadeIn(isle_label), run_time=0.48)
        self.at("they never have")
        self.play(Indicate(isle, color=GOLD, scale_factor=1.13), run_time=0.90)
        world = island(range(4), range(2), introduction=True)
        self.at("Let's find out why")
        self.play(FadeOut(isle_label), run_time=0.23)
        self.play(FadeOut(VGroup(map_art, isle)), FadeIn(world), FadeIn(tag), run_time=0.91)
        mark = T("?", 90, SNOW, font=TITLE_FONT).move_to(point(-0.75, 2.68))
        self.at("starting with a model island")
        self.play(FadeIn(mark, scale=0.7), run_time=0.63)
        self.play(FadeOut(mark), run_time=0.30)
        self.finish()


class S02Population(SpokenScene):
    def construct(self):
        world = island(range(4), range(2), introduction=True)
        term = T("population", 44, TEXT, font=TITLE_FONT).move_to(point(-2.28, 3.29))
        definition = T("one species, one place", 28, TEXT).move_to(point(4.65, 1.23))
        moose_loop = Ellipse(width=4.33, height=3.22, color=ANTLER, stroke_width=4).move_to(point(-4.00, -0.06))
        wolf_loop = Ellipse(width=2.78, height=2.78, color=WOLF_GREY, stroke_width=4).move_to(point(-0.23, 0.02))
        moose_label = boxed_label("population: moose", size=30, color="#E5AC77").move_to(point(4.65, -0.21))
        wolf_label = boxed_label("population: wolves", size=30, color=WOLF_GREY).move_to(moose_label)
        island_rim = world[1][1].copy().set_fill(opacity=0).set_stroke(SNOW, width=8, opacity=0.82)
        self.add(world, model_tag())
        self.at("First two words")
        self.play(FadeIn(term), run_time=1.13)
        self.at("A population is")
        self.play(term.animate.set_color(GOLD), run_time=0.48)
        self.at("all the members")
        self.play(FadeIn(definition, shift=UP * 0.14), Create(island_rim), run_time=2.69)
        self.at("All the moose")
        self.play(FadeOut(island_rim), Create(moose_loop), run_time=1.43)
        self.play(FadeIn(moose_label), run_time=0.71)
        self.at("All the wolves")
        self.play(FadeOut(moose_loop), swap(moose_label, wolf_label, run_time=1.24),
                  Create(wolf_loop, run_time=1.13))
        self.finish()


class S03Predator(SpokenScene):
    def construct(self):
        snow = oval(12.0, 4.62, SHORE, 0, -0.49)
        shelf = oval(12.8, 5.11, WATER, 0, -0.46)
        hunter = wolf(1.63).move_to(point(-4.18, 0.29))
        prey = moose(2.41).move_to(point(3.52, -0.02))
        predator_tag = boxed_label("predator", WOLF_GREY, size=32,
                                   pad=0.15).move_to(point(-4.13, 3.35))
        pred_def = T("catches and eats\nother animals", 29, TEXT,
                     line_spacing=0.60).move_to(point(-4.18, 2.41))
        prey_tag = boxed_label("prey", "#E5AC77", size=34).move_to(point(3.52, -1.91))
        prey_def = T("the animal that is eaten", 29, TEXT).move_to(point(3.52, -3.25))
        others = VGroup(wolf(1.08).move_to(point(-4.88, -1.35)),
                        wolf(0.98).move_to(point(-3.08, -1.46)))
        self.add(shelf, snow, model_tag())
        self.at("A predator is")
        self.play(FadeIn(hunter, shift=RIGHT * 0.51), run_time=0.71)
        self.play(FadeIn(predator_tag), run_time=0.55)
        self.at("catches and eats")
        self.play(FadeIn(pred_def), hunter.animate.shift(RIGHT * 0.55), run_time=1.50)
        self.at("The animal it eats")
        self.play(FadeIn(prey, shift=LEFT * 0.52), run_time=0.76)
        self.at("is its prey")
        self.play(FadeIn(prey_tag), run_time=0.50)
        self.play(FadeIn(prey_def), run_time=0.61)
        self.at("the wolves are the predators")
        self.play(LaggedStart(*[FadeIn(w, shift=RIGHT * 0.73) for w in others], lag_ratio=0.23),
                  hunter.animate.shift(RIGHT * 0.84), run_time=1.30)
        self.at("the moose are their prey")
        facing = moose(2.41, left=True).move_to(prey)
        self.play(Transform(prey, facing), others.animate.shift(RIGHT * 0.86), run_time=1.07)
        self.finish()


class S04Arrow(SpokenScene):
    def construct(self):
        shelf = oval(12.8, 5.11, WATER, 0, -0.46)
        snow = oval(12.0, 4.62, SHORE, 0, -0.49)
        tree = fir(3.29).move_to(point(-4.80, -0.15))
        prey = moose(2.33, left=True).move_to(point(-0.40, -0.55))
        hunter = wolf(1.55, left=True).move_to(point(4.08, -0.88))
        a1 = Arrow(point(-3.55, -0.50), point(-1.77, -0.50), buff=0,
                   color=TREE_GREEN, stroke_width=14, tip_length=0.32).set_z_index(3)
        a2 = Arrow(point(0.91, -0.60), point(1.98, -0.60), buff=0,
                   color=ANTLER, stroke_width=14, tip_length=0.32).set_z_index(3)
        note = caption("Arrow points from food to eater", size=33, y=-3.10).set_x(0.30)
        self.add(shelf, snow, model_tag())
        self.at("Moose eat young trees")
        self.add(prey)
        self.play(FadeIn(tree, shift=UP * 0.21), run_time=0.68)
        self.play(Transform(prey, moose(2.12, left=True, browse=True).move_to(point(-0.51, -0.58))),
                  run_time=1.31)
        self.at("Wolves eat moose")
        self.play(FadeIn(hunter, shift=LEFT * 0.82), run_time=1.10)
        self.at("eat moose")
        self.play(hunter.animate.shift(LEFT * 0.48), run_time=1.22)
        self.at("We draw arrows")
        self.play(Succession(GrowArrow(a1, run_time=0.73), GrowArrow(a2, run_time=0.78)))
        self.at("Each arrow points")
        self.play(FadeIn(note), run_time=0.62)
        tree_focus = animal_halos([tree], TREE_GREEN)
        moose_focus = animal_halos([prey], ANTLER)
        wolf_focus = animal_halos([hunter], WOLF_GREY)
        self.at("from the food")
        self.play(FadeIn(tree_focus), FadeIn(moose_focus), run_time=0.54)
        self.at("to the eater")
        self.play(FadeOut(tree_focus), FadeIn(wolf_focus), run_time=1.12)
        self.finish()


class S05Counter(SpokenScene):
    def construct(self):
        world = island()
        box = ratio_box(ValueTracker(START_MOOSE / START_WOLVES))
        formula = T("moose ÷ wolves", 33, TEXT, weight=BOLD).move_to(point(4.28, 1.35))
        arithmetic = T("1,000 moose ÷ 10 wolves\n= 100 moose per wolf", 25, TEXT,
                       line_spacing=1.05).move_to(point(4.70, 0.25))
        explanation = T("One number for the\nwhole island, not each\nwolf’s own share", 25,
                        TEXT, line_spacing=0.93).move_to(point(4.60, -1.23))
        self.add(world, model_tag())
        self.at("Now we need one number")
        self.play(FadeIn(formula), run_time=0.77)
        self.at("Count the moose")
        self.play(LaggedStart(*[Indicate(m, color=ANTLER, scale_factor=1.12)
                               for m in world.moose[:3]], lag_ratio=0.30), run_time=1.17)
        self.at("The counter in the corner")
        self.play(FadeIn(arithmetic), FadeIn(box), run_time=1.27)
        self.at("rough clue")
        self.play(FadeIn(explanation), run_time=1.09)
        self.at("wolves find food")
        self.play(world.wolves[0].animate.shift(LEFT * 0.55 + DOWN * 0.15), run_time=1.10)
        self.finish()


class S06Start(SpokenScene):
    def construct(self):
        world = island()
        world.wolves[0].shift(LEFT * 0.55 + DOWN * 0.15)
        _, box, counts = readout(ValueTracker(START_MOOSE), ValueTracker(START_WOLVES))
        moose_halos = animal_halos(world.moose, ANTLER)
        wolf_halos = animal_halos(world.wolves, WOLF_GREY)
        self.add(world, box, model_tag())
        self.at("many moose")
        self.play(FadeIn(counts[0]), FadeIn(moose_halos), run_time=0.86)
        self.at("only a few wolves")
        self.play(FadeIn(counts[1]), FadeOut(moose_halos), FadeIn(wolf_halos), run_time=1.08)
        ring = ratio_outline(box)
        self.at("The counter is high")
        self.play(Create(ring), FadeOut(wolf_halos), run_time=0.99)
        self.at("In this model")
        self.play(FadeOut(ring), run_time=0.55)
        self.at("hunting is easy")
        hunter = world.wolves[0]
        nearby = world.moose[6]
        approach = ArcBetweenPoints(hunter.get_center(), nearby.get_center() + UP * 0.10, angle=0.40)
        self.play(MoveAlongPath(hunter, approach), run_time=1.42)
        self.at("the wolves eat well")
        well_fed = wolf(0.77, fed=True).move_to(point(*WOLF_SITES[0]))
        self.play(Transform(hunter, well_fed), FadeOut(nearby), run_time=1.02)
        self.finish()


class S07Grow(SpokenScene):
    def construct(self):
        world = island((0, 1, 2, 3, 4, 5, 7))
        fed = wolf(0.77, fed=True).move_to(world.wolves[0])
        world.wolves[0].become(fed)
        moose_total, wolf_total, year = ValueTracker(START_MOOSE), ValueTracker(START_WOLVES), ValueTracker(1)
        ratio, box, counts = readout(moose_total, wolf_total)
        year_label = counter("year {:.0f}", year, point(4.33, -3.04), size=32, color=TEXT, mono=False)
        shelter = den()
        detail = snow_detail()
        den_detail = den().set_width(1.61).move_to(point(3.21, -1.88))
        pup_sites = ((3.64, -1.92), (5.35, -1.92))
        pups = VGroup(*[wolf(0.66, pup=True).move_to(point(*xy)) for xy in pup_sites])
        grown = [wolf(0.98, left=i == 0).move_to(pup) for i, pup in enumerate(pups)]
        adults = VGroup(*[wolf(0.63, left=i % 3 == 2).move_to(point(*WOLF_SITES[i]))
                          for i in range(2, 6)])
        self.add(world, ratio, box, counts, model_tag())
        self.at("With plenty of food")
        self.play(FadeIn(shelter), run_time=1.12)
        self.at("more wolf pups survive")
        self.play(FadeIn(detail), FadeIn(den_detail), run_time=0.48)
        self.play(LaggedStart(*[FadeIn(p, shift=RIGHT * 0.20) for p in pups], lag_ratio=0.26),
                  run_time=0.73)
        self.at("grow up")
        self.play(*[Transform(pup, adult) for pup, adult in zip(pups, grown)], run_time=1.51)
        self.at("Year by year")
        self.add(year_label)
        self.play(year.animate.set_value(3), wolf_total.animate.set_value(PACK_WOLVES),
                  LaggedStart(*[FadeIn(adult) for adult in adults], lag_ratio=0.39),
                  Transform(world.wolves[0], wolf(0.63).move_to(world.wolves[0])),
                  FadeOut(shelter), FadeOut(detail), FadeOut(den_detail), FadeOut(pups),
                  run_time=2.23, rate_func=linear)
        self.at("more wolves catch")
        target = world.moose[-1]
        chasers = (adults[0], adults[2])
        starts = [animal.get_center() for animal in chasers]
        self.play(chasers[0].animate.move_to(target.get_center() + LEFT * 0.54),
                  chasers[1].animate.move_to(target.get_center() + RIGHT * 0.54), run_time=0.70)
        self.play(FadeOut(target), *[animal.animate.move_to(at) for animal, at in zip(chasers, starts)],
                  moose_total.animate.set_value(HUNT_MOOSE), FadeOut(year_label), run_time=0.80)
        self.finish()


class S08Fall(SpokenScene):
    def construct(self):
        world = island(range(6), range(6))
        moose_total = ValueTracker(HUNT_MOOSE)
        ratio, box, counts = readout(moose_total, ValueTracker(PACK_WOLVES))
        self.add(world, ratio, box, counts, model_tag())
        self.at("So the moose population falls")
        self.play(LaggedStart(FadeOut(world.moose[5]), FadeOut(world.moose[4]), lag_ratio=0.40),
                  moose_total.animate.set_value(510), run_time=2.45, rate_func=linear)
        ring = ratio_outline(box, ORANGE)
        comparison = T("100 at the start", 24, TEXT).move_to(point(4.33, 1.69))
        self.at("Watch the counter drop")
        self.play(AnimationGroup(FadeOut(world.moose[3]), moose_total.animate.set_value(LOW_MOOSE),
                                 Create(ring), run_time=1.92, rate_func=linear),
                  FadeIn(comparison, run_time=0.50))
        self.at("Now each wolf has")
        self.play(FadeOut(ring), run_time=0.46)
        survivors = animal_halos(world.moose[:3], ANTLER)
        self.play(LaggedStart(*[FadeIn(halo) for halo in survivors], lag_ratio=0.34), run_time=1.26)
        self.play(FadeOut(survivors), FadeOut(comparison), run_time=0.51)
        self.finish()


class S09Predict(SpokenScene):
    def construct(self):
        picture = low_state()
        panel, setup, prompt = prediction()
        ring = ratio_outline(picture[1], ORANGE)
        self.add(picture)
        self.at("Here is a question")
        self.play(FadeIn(panel, shift=UP * 0.28), run_time=1.18)
        self.at("There are now only 10")
        self.play(FadeIn(setup), Create(ring), run_time=1.16)
        self.play(FadeOut(ring), run_time=0.41)
        self.at("What happens to the wolves")
        focus = animal_halos(picture[0].wolves, WOLF_GREY)
        self.play(FadeIn(prompt), FadeIn(focus), run_time=1.41)
        self.at("Pause and predict")
        self.play(FadeOut(focus), run_time=0.80)
        self.finish()


class S10Pause(PredictPause):
    RING_AT = (5.91, -3.12, 0)

    def backdrop(self):
        return low_state()

    def construct(self):
        self.add(self.backdrop(), *prediction())
        ring, progress = prediction_timer(self.SECONDS, self.RING_AT)
        progress.set_value(0)
        self.add(ring)
        self.play(progress.animate(rate_func=linear).set_value(1), run_time=self.SECONDS)


class S11Reveal(SpokenScene):
    def construct(self):
        world = island(range(3), range(6))
        moose_total, wolf_total = ValueTracker(LOW_MOOSE), ValueTracker(PACK_WOLVES)
        ratio, box, counts = readout(moose_total, wolf_total)
        rule = T("Too few moose to\nfeed the wolves", 26, ORANGE, line_spacing=0.87)
        rule.move_to(point(4.45, -0.36))
        detail = snow_detail().shift(DOWN * 0.25)
        searching = wolf(1.04).move_to(point(3.50, -2.13))
        pups = VGroup(*[wolf(0.65, pup=True).move_to(point(x, -2.16)) for x in (3.65, 5.01)])
        self.add(world, ratio, box, counts, model_tag())
        self.at("In this model")
        ring = ratio_outline(box, ORANGE)
        self.play(Create(ring), run_time=1.18)
        self.at("that number is too low")
        self.play(FadeIn(rule), run_time=1.14)
        scout = world.wolves[5]
        partner = world.wolves[2]
        scout_home, partner_home = scout.get_center(), partner.get_center()
        self.at("Wolves catch too little")
        self.play(FadeIn(detail), FadeIn(searching), run_time=0.43)
        self.play(searching.animate.shift(RIGHT * 1.20), scout.animate.move_to(point(0.92, -0.43)),
                  partner.animate.move_to(point(-5.34, -1.12)), run_time=1.02)
        self.at("fewer pups survive")
        self.play(FadeOut(searching), run_time=0.27)
        self.play(scout.animate.move_to(scout_home),
                  partner.animate.move_to(partner_home), FadeIn(pups), run_time=0.53)
        self.play(FadeOut(pups[1]), run_time=1.23)
        self.at("The wolf population falls")
        self.play(LaggedStart(*[FadeOut(w) for w in world.wolves[2:]],
                              lag_ratio=0.20), wolf_total.animate.set_value(FEWER_WOLVES),
                  FadeOut(VGroup(detail, pups[0])), FadeOut(ring), FadeOut(rule),
                  rate_func=linear, run_time=2.19)
        self.at("But look at the moose")
        moose_halos = animal_halos(world.moose, ANTLER)
        self.play(LaggedStart(*[FadeIn(halo) for halo in moose_halos], lag_ratio=0.42), run_time=1.75)
        self.at("Many moose are still alive")
        browser = world.moose[2]
        browsing = moose(0.84, browse=True).move_to(browser).shift(RIGHT * 0.13)
        self.play(Transform(browser, browsing), FadeIn(T("still alive", 35, "#E5AC77", weight=BOLD)
                  .move_to(point(4.34, -0.91))), run_time=1.07)
        self.finish()


class S12Recover(SpokenScene):
    def construct(self):
        world = island(range(3))
        moose_total, wolf_total = ValueTracker(LOW_MOOSE), ValueTracker(FEWER_WOLVES)
        ratio, box, counts = readout(moose_total, wolf_total)
        calf_sites = ((-3.93, 1.12), (-1.63, -0.29), (-4.78, -0.21))
        calves = VGroup(*[moose(0.51, left=i % 3 == 1, calf=True).move_to(point(*xy)).set_z_index(2)
                          for i, xy in zip(range(3, 6), calf_sites)])
        adults = VGroup(*[moose(0.91, left=i % 3 == 1).move_to(point(*MOOSE_SITES[i])) for i in range(3, 6)])
        detail = snow_detail()
        mother = moose(1.33).move_to(point(3.43, -1.83))
        calf_detail = moose(0.63, calf=True).move_to(point(5.19, -2.03))
        self.add(world, ratio, box, counts, model_tag())
        self.at("With fewer wolves hunting")
        self.play(Indicate(world.wolves[0], color=TEXT, scale_factor=1.09), run_time=1.35)
        self.at("more moose calves survive")
        self.play(FadeIn(detail), FadeIn(mother), run_time=0.53)
        self.play(FadeIn(calf_detail), LaggedStart(*[FadeIn(calf, shift=UP * 0.19) for calf in calves],
                                                  lag_ratio=0.42), run_time=1.32)
        self.at("The moose population grows")
        focus = animal_halos(adults, ANTLER)
        self.play(*[Transform(calf, adult) for calf, adult in zip(calves, adults)], FadeIn(focus),
                  Transform(calf_detail, moose(1.12).move_to(point(5.26, -1.88))),
                  moose_total.animate.set_value(516), run_time=2.44, rate_func=linear)
        self.at("The counter climbs")
        ring = ratio_outline(box)
        self.play(moose_total.animate.set_value(RECOVERED_MOOSE), Create(ring), FadeOut(focus),
                  FadeOut(VGroup(detail, mother, calf_detail)), run_time=1.63, rate_func=linear)
        self.at("the loop can start over")
        labels, arrows = cycle()
        self.play(FadeOut(ring), FadeOut(counts),
                  LaggedStart(*[AnimationGroup(FadeIn(label), Create(arrow))
                                for label, arrow in zip(labels, arrows)], lag_ratio=0.38),
                  run_time=1.41)
        self.finish()


class S13Scope(SpokenScene):
    def construct(self):
        world = island(range(6))
        box = ratio_box(ValueTracker(RECOVERED_MOOSE / FEWER_WOLVES))
        labels, arrows = cycle()
        self.add(world, box, model_tag(), labels, arrows)
        scope = boxed_label("Mostly one kind of prey", size=26, color=GOLD,
                            pad=0.16).move_to(point(4.72, 1.12))
        island_scope = boxed_label("An island limits escape", size=26, color=GOLD,
                                   pad=0.16).move_to(point(4.72, 0.13))
        one_prey = moose(1.24, left=True).move_to(point(-1.35, 0.03))
        one_predator = wolf(0.99).move_to(point(-3.66, -0.88))
        self.at("This rule fits")
        loop_icon = VGroup(*[CurvedArrow(point(*start), point(*end), angle=-0.76,
                                         color=GOLD, stroke_width=4, tip_length=0.14)
                             for start, end in (((-5.85, 1.41), (-5.15, 0.96)),
                                                ((-5.12, 0.81), (-5.88, 0.47)),
                                                ((-6.04, 0.55), (-6.03, 1.27)))]).move_to(point(-6.00, 2.52))
        self.play(FadeOut(labels), run_time=0.33)
        self.play(ReplacementTransform(arrows, loop_icon), run_time=0.75)
        self.at("a predator that eats")
        self.play(FadeOut(world.moose), FadeOut(world.wolves), FadeIn(one_prey),
                  FadeIn(one_predator), run_time=1.43)
        self.play(FadeIn(scope), run_time=0.67)
        self.at("On an island")
        rim = world[1][1].copy().set_fill(opacity=0).set_stroke(SNOW, width=4, opacity=0.78)
        self.play(Create(rim), run_time=1.08)
        self.at("neither animal can easily leave")
        self.play(FadeIn(island_scope), run_time=0.82)
        self.play(FadeOut(rim), run_time=0.88)

        panels = TwoPanel("Mostly one prey", "Other food available", colors=(GOLD, TEAL),
                          top=1.69, bottom=-2.85, size=31, gap=0.52, width=12.5)
        example = wolf(1.08).move_to(point(2.15, 0.10))
        bowl = shape([(3.72, 0.10), (5.46, 0.10), (5.02, -0.52), (4.15, -0.52)], TEAL)
        food = VGroup(*[oval(0.26, 0.28, "#D9BCA3", x, 0.18) for x in (4.05, 4.39, 4.72, 5.04)])
        food_label = T("other food", 28, TEXT).move_to(point(4.57, -0.88))
        other_prey = VGroup(*[moose(0.61, left=True).move_to(point(x, -1.51)) for x in (2.05, 3.05, 4.05)])
        outcome = T("Prey could disappear", 31, TEXT).move_to(point(3.26, -2.30))
        left_example = island(range(3), range(2))
        panels.put(left_example, "left")
        self.at("A predator with other food")
        self.play(FadeOut(scope), FadeOut(island_scope), FadeOut(world[0]), FadeOut(world[1]),
                  FadeOut(one_prey), FadeOut(one_predator), FadeOut(loop_icon), FadeOut(box), run_time=0.39)
        self.play(FadeIn(panels), FadeIn(left_example), FadeIn(example), FadeIn(bowl), FadeIn(food),
                  run_time=0.70)
        self.at("may not go hungry")
        self.play(example.animate.shift(RIGHT * 0.65), FadeIn(food_label), FadeIn(other_prey), run_time=1.30)
        self.at("could keep eating")
        self.play(LaggedStart(*[FadeOut(prey) for prey in other_prey], lag_ratio=0.42), run_time=1.36)
        self.play(FadeIn(outcome), run_time=0.81)
        self.finish()


class S14Messy(SpokenScene):
    def construct(self):
        world = island(range(6))
        box = ratio_box(ValueTracker(RECOVERED_MOOSE / FEWER_WOLVES))
        self.add(world, box, model_tag())
        head = T("A real island is messier", 42, TEXT, font=TITLE_FONT).move_to(point(-2.14, 3.35))
        clouds = VGroup(oval(1.64, 0.57, WOLF_GREY, -5.50, 2.36),
                        oval(0.95, 0.78, WOLF_GREY, -5.67, 2.54),
                        oval(0.76, 0.66, WOLF_GREY, -5.14, 2.52))
        snowflakes = VGroup(*[Star(n=6, outer_radius=0.10, inner_radius=0.027,
                                    fill_color=SNOW, fill_opacity=1, stroke_width=0).move_to(point(x, y))
                              for x, y in ((-6.06, 1.88), (-5.76, 1.97), (-5.46, 1.82), (-5.16, 1.93))])
        weather = boxed_label("weather", size=28, color=SNOW, fill_opacity=1).move_to(point(-3.67, 2.61))
        weather.box.set_fill(WATER, opacity=1)
        tick_at = world.moose[1].get_center() + LEFT * 0.08
        tick = VGroup(oval(0.18, 0.13, INK),
                      *[Line(0.07 * d, 0.15 * d, color=INK, stroke_width=3)
                        for d in (UL, UR, DL, DR, UP, DOWN)]).move_to(tick_at)
        tick_ring = Circle(radius=0.33, color=GOLD, stroke_width=3.5).move_to(tick_at)
        ticks = boxed_label("ticks", size=28, color=GOLD, fill_opacity=1).move_to(point(-3.31, -0.93))
        ticks.box.set_fill(WATER, opacity=1)
        spikes = VGroup(*[Line(radius * d, (radius + 0.17) * d, color=ORANGE, stroke_width=5)
                          for radius, d in [(0.32, rotate_vector(RIGHT, i * TAU / 8)) for i in range(8)]])
        germ = VGroup(oval(0.70, 0.68, ORANGE), spikes, oval(0.11, 0.10, HIDE, -0.12, 0.07),
                      oval(0.09, 0.10, HIDE, 0.15, -0.10)).set_height(0.64).move_to(point(-0.30, 0.28))
        disease = boxed_label("disease", size=26, color=ORANGE, pad=0.11,
                              fill_opacity=1).move_to(point(-0.40, -0.36))
        disease.box.set_fill(WATER, opacity=1)
        note = T("On the real island,\nthis number alone\ncannot show hunger.", 27,
                 TEXT, line_spacing=0.92).move_to(point(4.70, 0.36))
        next_film = T("Next film: real counts", 30, TEAL).move_to(point(4.17, -1.92))

        self.at("A real island is messier")
        self.play(FadeIn(head), run_time=1.09)
        self.at("Weather", lead=0.65)
        self.play(FadeIn(clouds), run_time=0.45)
        self.play(FadeIn(snowflakes, shift=DOWN * 0.13), FadeIn(weather), run_time=0.59)
        self.at("ticks")
        self.play(FadeIn(tick), Create(tick_ring), FadeIn(ticks), run_time=0.26)
        self.at("and disease")
        self.play(FadeIn(germ, scale=0.65), run_time=0.60)
        self.play(FadeIn(disease), run_time=1.42)
        ring = ratio_outline(box)
        self.at("this number alone")
        self.play(Create(ring), FadeIn(note), run_time=1.84)
        self.at("wolves are hungry")
        self.play(FadeOut(ring), run_time=0.92)
        self.at("You will see real counts")
        self.play(FadeIn(next_film), run_time=1.36)
        self.finish()


class S15Rule(SpokenScene):
    def construct(self):
        world = island(range(3))
        foreground_height = 1.05
        foreground = wolf(foreground_height, seated=True).move_to(point(-4.22, -1.44))
        value = ValueTracker(RECOVERED_MOOSE / FEWER_WOLVES)
        box = ratio_box(value)
        large_box = ratio_box(value, at=(4.20, 2.52, 0), size=35).set_z_index(4)
        self.add(world[0], world[1], world.moose, world.wolves[1], foreground, box, model_tag())
        self.at("here is the answer")
        # Freeze the source and target geometry for the move, then restore the live ratio.
        box.clear_updaters(recursive=True)
        target = large_box.copy().clear_updaters(recursive=True)
        self.play(ReplacementTransform(box, target), run_time=2.06)
        self.remove(target)
        self.add(large_box)
        self.at("there are few moose")
        self.play(value.animate.set_value(LOW_RATIO), run_time=1.73, rate_func=linear)
        self.at("wolves tend to catch")
        path = ArcBetweenPoints(foreground.get_center(), point(-2.55, -1.45), angle=0.43)
        walker = wolf(foreground_height).move_to(foreground)
        self.play(Transform(foreground, walker), run_time=0.38)
        self.play(MoveAlongPath(foreground, path), run_time=1.92)
        self.at("If they get too little food")
        seated = wolf(foreground_height, seated=True).move_to(foreground).shift(DOWN * 0.19)
        self.play(Transform(foreground, seated), run_time=1.25)
        self.at("fewer wolves survive")
        wolf_focus = animal_halos([foreground, world.wolves[1]], WOLF_GREY)
        world.moose.set_z_index(2)
        self.play(FadeIn(wolf_focus), run_time=0.46)
        self.play(FadeOut(world.wolves[1]), FadeOut(wolf_focus[1]), run_time=1.06)
        line = T(TAKEAWAY.replace(" short", "\nshort").replace(" the moose", "\nthe moose"),
                 31, TEXT, font=TITLE_FONT, line_spacing=0.86).move_to(point(4.65, -0.70))
        self.at("Wolves usually run short")
        self.play(Write(line), FadeOut(wolf_focus[0]), run_time=2.08)
        self.play(LaggedStart(*[Indicate(m, color=ANTLER, scale_factor=1.10)
                               for m in world.moose], lag_ratio=0.30), run_time=1.00)
        self.finish()


class S16End(EndCard):
    LINE = "Wolves usually run short of food before the moose run out."
