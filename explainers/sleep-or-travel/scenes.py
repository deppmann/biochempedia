"""The parent guide, told through one illustrated yard and its card-sorting table."""

from bp_parts import *
from bp_style import EndCard


# COLOR MAP: the original setup guide's teal, gold, green and safety red.
# Travel is teal, rest is blue, and stay and change is green.
# Snow and paper are pale ivory; navy, slate and walnut belong to the setting.
NAVY = "#1C3049"
SLATE = "#2E4962"
ICE = "#A1C5D9"
SNOW = "#D4E6EC"
WALNUT = "#644239"
WOOD_EDGE = "#9B6B53"
PAPER = "#F3E4CD"
INK = "#17263A"
BARK = "#67494B"
CARDINAL = "#D44848"
HUMMER = "#449C79"
LEAF = "#73A16E"
SOIL = "#684838"
ORANGE = "#ECA45F"

NAMES = (
    "Ruby-throated\nhummingbird", "Monarch\nbutterfly", "Tundra swan",
    "Groundhog", "Bat", "Eastern box\nturtle", "Wood frog",
    "White-tailed\ndeer", "Gray squirrel", "Northern\ncardinal",
)
PLANS = ("Travel", "Rest", "Stay and change")
PLAN_COLORS = (TEAL, BLUE, GREEN)
PILE_X = (-4.26, 0, 4.26)
QUESTION = "Why does one leave and one stay?"


def xy(x, y):
    return np.array([x, y, 0.0])


def oval(x, y, w, h, color, angle=0):
    return Ellipse(width=w, height=h, stroke_width=0, fill_color=color, fill_opacity=1
                   ).rotate(angle).move_to(xy(x, y))


def disc(x, y, radius, color):
    return Dot(xy(x, y), radius, color=color, stroke_width=0)


def shape(points, color):
    return Polygon(*(xy(*p) for p in points), stroke_width=0, fill_color=color, fill_opacity=1)


def line(a, b, color, width=4):
    return Line(xy(*a), xy(*b), stroke_color=color, stroke_width=width)


def panel(x, y, w, h, color, border=None, radius=0.16):
    return RoundedRectangle(width=w, height=h, corner_radius=radius, fill_color=color,
                            fill_opacity=1, stroke_color=border or color,
                            stroke_width=2 if border else 0).move_to(xy(x, y))


def label(words, x, y, size=34, color=TEXT, width=11, **kw):
    return fit_text(words, max_w=width, size=size, min_size=28, color=color, **kw
                    ).move_to(xy(x, y))


def badge(words, x, y, color=GOLD, size=32, fill=INK):
    tag = boxed_label(words, color=color, size=size, pad=0.22)
    tag.box.set_fill(fill, opacity=1)
    return tag.move_to(xy(x, y))


def cardinal():
    bird = VGroup(
        shape([(-0.25, 0), (-1.15, -0.60), (-0.93, -0.72), (-0.20, -0.39)], "#A02E41"),
        oval(0, -0.08, 1.35, 0.91, CARDINAL, 0.14),
        oval(-0.13, -0.11, 0.92, 0.47, "#AF3347", 0.24),
        shape([(0.15, 0.41), (0.29, 0.97), (0.68, 0.46)], CARDINAL),
        disc(0.44, 0.35, 0.40, CARDINAL),
        oval(0.68, 0.30, 0.36, 0.43, INK, 0.30),
        shape([(0.78, 0.40), (1.10, 0.26), (0.79, 0.16)], ORANGE),
        disc(0.65, 0.44, 0.06, PAPER),
        line((0.04, -0.46), (0.08, -0.62), BARK, 3),
        line((0.30, -0.44), (0.36, -0.61), BARK, 3),
    )
    bird.breast = bird[1]
    return bird


def hummingbird():
    bird = VGroup(
        shape([(-0.17, -0.16), (-1.07, -0.64), (-0.93, -0.76), (0.22, -0.25)], "#286854"),
        oval(0.01, -0.09, 1.28, 0.58, HUMMER, 0.32),
        oval(0.19, -0.23, 0.73, 0.29, SNOW, 0.26),
        disc(0.48, 0.17, 0.29, HUMMER),
        oval(0.63, 0.03, 0.26, 0.24, CARDINAL, 0.1),
        shape([(0.68, 0.24), (1.53, 0.34), (0.68, 0.16)], "#263B49"),
        oval(-0.24, 0.30, 0.50, 1.13, "#70B7AB", 0.51),
        disc(0.57, 0.26, 0.06, INK),
    )
    bird.wing = bird[6]
    return bird


def butterfly():
    wings = VGroup()
    for side in (-1, 1):
        wings.add(oval(side * 0.46, 0.26, 0.84, 1.13, INK, side * 0.47),
                  oval(side * 0.43, 0.26, 0.65, 0.91, ORANGE, side * 0.47),
                  oval(side * 0.33, -0.35, 0.7, 0.62, INK, -side * 0.48),
                  oval(side * 0.31, -0.34, 0.53, 0.48, ORANGE, -side * 0.48),
                  line((0, 0), (side * 0.67, 0.53), INK, 3.5),
                  line((0, 0), (side * 0.55, -0.48), INK, 3),
                  disc(side * 0.77, 0.35, 0.048, PAPER),
                  disc(side * 0.54, 0.66, 0.048, PAPER),
                  line((0, 0.34), (side * 0.22, 0.68), INK, 3))
    return VGroup(wings, oval(0, 0, 0.22, 0.84, INK))


def swan():
    neck = CubicBezier(xy(0.31, -0.24), xy(0.8, 0.12), xy(0.22, 0.91), xy(0.77, 0.75))
    neck.set_stroke("#F8F3E8", width=17)
    return VGroup(
        shape([(-0.35, -0.2), (-1.1, 0.18), (-0.93, -0.25), (-0.65, -0.47)], SNOW
              ).set_stroke(SLATE, width=2),
        neck.copy().set_stroke(SLATE, width=21),
        oval(-0.14, -0.32, 1.62, 0.69, "#F8F3E8").set_stroke(SLATE, width=2), neck,
        oval(-0.24, -0.27, 0.91, 0.35, SNOW, 0.04),
        disc(0.77, 0.75, 0.19, "#F8F3E8").set_stroke(SLATE, width=2),
        shape([(0.85, 0.82), (1.16, 0.68), (0.83, 0.66)], INK),
        disc(0.85, 0.8, 0.035, ORANGE),
        disc(0.81, 0.83, 0.034, INK),
    )


def groundhog():
    return VGroup(oval(-0.68, -0.33, 0.56, 0.33, "#7B4C35", 0.26),
                  oval(-0.18, -0.12, 1.48, 1.06, "#9D6645", 0.25),
                  oval(0.08, -0.33, 0.76, 0.43, "#C78F5E", 0.13),
                  disc(0.43, 0.18, 0.39, "#AA7250"), disc(0.31, 0.48, 0.145, "#7B4C35"),
                  oval(0.69, 0.00, 0.54, 0.32, "#D7A578"),
                  disc(0.93, 0.04, 0.075, INK), disc(0.6, 0.25, 0.057, INK))


def bat():
    wings = VGroup()
    for side in (-1, 1):
        pts = [(0, -0.05), (0.47, 0.32), (1.37, 0.12), (1.03, -0.16),
               (0.88, -0.51), (0.57, -0.30), (0.34, -0.55), (0.12, -0.32)]
        wings.add(shape([(side * x, y) for x, y in pts], "#68718D"))
        wings.add(line((0, -0.05), (side * 0.95, 0.11), "#3D415B", 2.8))
    return VGroup(wings, oval(0, -0.16, 0.59, 0.69, "#383B53"),
                  shape([(-0.27, 0.12), (-0.24, 0.58), (-0.03, 0.25)], "#383B53"),
                  shape([(0.27, 0.12), (0.24, 0.58), (0.03, 0.25)], "#383B53"),
                  disc(0, 0.11, 0.28, "#383B53"),
                  disc(-0.11, 0.13, 0.036, PAPER), disc(0.11, 0.13, 0.036, PAPER))


def turtle():
    return VGroup(oval(-0.54, -0.31, 0.39, 0.25, "#465B39"),
                  oval(0.42, -0.31, 0.34, 0.25, "#465B39"),
                  oval(0.67, -0.11, 0.61, 0.32, "#83975A"),
                  oval(-0.12, -0.03, 1.46, 0.79, "#554632"),
                  oval(-0.17, 0.12, 1.22, 0.59, "#916039"),
                  shape([(-0.54, 0.16), (-0.33, 0.35), (-0.19, 0.20), (-0.29, 0.02)], GOLD),
                  shape([(-0.04, 0.12), (0.14, 0.32), (0.33, 0.21), (0.16, 0.00)], GOLD),
                  disc(0.79, -0.05, 0.044, INK))


def frog():
    return VGroup(oval(-0.48, -0.19, 0.70, 0.36, "#91664A", 0.19),
                  oval(0.30, -0.24, 0.66, 0.24, "#91664A", -0.12),
                  oval(-0.11, -0.03, 1.45, 0.59, "#AE8055", 0.10),
                  disc(0.35, 0.18, 0.24, "#B98E62"),
                  oval(0.41, 0.03, 0.72, 0.18, "#604431", -0.11),
                  disc(0.43, 0.25, 0.081, INK), disc(0.45, 0.28, 0.025, PAPER))


def deer(winter=False):
    coat = "#968C83" if winter else "#B2784F"
    legs = VGroup(*[line((x, y), (x + dx, -0.87), coat, 7)
                    for x, y, dx in [(-0.69, -0.02, -0.08), (-0.41, -0.04, 0.12),
                                      (0.27, -0.03, -0.02), (0.5, 0, 0.10)]])
    return VGroup(legs, oval(-0.26, 0.16, 1.54, 0.68, coat),
                  oval(0.43, 0.42, 0.51, 0.89, coat, -0.32),
                  oval(0.76, 0.73, 0.74, 0.44, coat, -0.26),
                  oval(0.52, 0.99, 0.22, 0.41, coat, 0.61),
                  oval(0.72, 1.0, 0.2, 0.37, coat, -0.12),
                  oval(-0.99, 0.33, 0.22, 0.43, PAPER, 0.66),
                  disc(0.89, 0.81, 0.056, INK), disc(1.09, 0.65, 0.063, INK))


def squirrel():
    return VGroup(oval(-0.66, 0.30, 0.76, 1.28, "#798996", -0.42),
                  oval(-0.76, 0.46, 0.46, 0.92, "#A9B8BF", -0.42),
                  oval(0.02, -0.19, 1.03, 0.73, "#8D9EA7", 0.21),
                  oval(0.33, -0.26, 0.55, 0.54, SNOW, 0.27),
                  disc(0.48, 0.14, 0.32, "#8D9EA7"),
                  oval(0.37, 0.42, 0.22, 0.31, "#798996", 0.26),
                  oval(0.73, 0.0, 0.38, 0.25, "#8D9EA7"),
                  disc(0.87, 0.03, 0.063, INK), disc(0.59, 0.23, 0.056, INK))


ANIMALS = (hummingbird, butterfly, swan, groundhog, bat, turtle, frog, deer, squirrel, cardinal)


def branch(x, y, scale=1):
    limbs = VGroup(
        shape([(-1.6, -0.26), (0.50, 0.10), (1.80, 0.49), (0.56, -0.08), (-1.6, -0.52)], BARK),
        shape([(-0.61, -0.19), (-1.30, 0.63), (-0.35, -0.12)], BARK),
        shape([(0.62, 0.04), (1.00, 0.63), (0.82, 0.06)], BARK),
        shape([(-1.59, -0.25), (0.50, 0.11), (1.63, 0.45), (0.48, 0.02), (-1.59, -0.32)], SNOW),
    )
    return limbs.scale(scale).move_to(xy(x, y))


def yard(spring=False):
    """The same window and landmarks in the hook, watch and seasonal comparison."""
    frame = panel(0, 0.06, 12.8, 6.76, WOOD_EDGE, radius=0.26)
    sky = panel(0, 0.12, 12.45, 6.30, "#446D7A" if spring else NAVY, radius=0.19)
    hill = shape([(-6.20, -0.47), (-4.1, 0.19), (-2.6, 0.46), (-0.8, 0.12),
                  (1.4, 0.36), (3.2, 0.73), (6.20, 0.01), (6.20, -2.94),
                  (-6.20, -2.94)], "#608D70" if spring else SLATE)
    bank = shape([(-6.2, -1.18), (-4.2, -0.84), (-2.0, -1.26), (0.04, -0.77),
                  (2.3, -0.96), (4.3, -0.48), (6.2, -0.68), (6.2, -3.03),
                  (-6.2, -3.03)], "#93B47A" if spring else SNOW)
    tree = branch(2.63, -0.25, 1.85)
    if spring:
        tree[-1].set_fill("#7F7B53")
        tree.add(*[oval(x, y, 0.32, 0.16, GREEN, a)
                   for x, y, a in [(0.35, 0.64, 0.8), (1.0, 0.12, -0.4),
                                   (4.18, 0.67, 0.85), (5.05, 0.36, 0.5)]])
    mullion = panel(-0.12, 0.12, 0.11, 6.32, WOOD_EDGE, radius=0.035)
    sill = panel(0, -3.02, 12.8, 0.26, WOOD_EDGE, radius=0.10)
    g = VGroup(frame, sky, hill, bank, mullion, tree, sill)
    g.tree = tree
    return g


def snow(floor=-1.12):
    rng = np.random.default_rng(37)
    flakes = VGroup()
    for _ in range(35):
        x, y = rng.uniform(-6.0, 6.0), rng.uniform(floor, 2.98)
        flake = disc(x, y, rng.uniform(0.025, 0.057), ICE)
        flake.fall = rng.uniform(0.25, 0.50)
        flakes.add(flake)

    def drift(group, dt):
        for flake in group:
            flake.shift(xy(-0.13 * dt, -flake.fall * dt))
            if flake.get_y() < floor:
                flake.shift(UP * (2.98 - floor))
            if flake.get_x() < -6.0:
                flake.shift(RIGHT * 12.0)

    return flakes.add_updater(drift)


def table():
    """The same walnut work surface for making, sorting and checking cards."""
    lip = panel(0, 1.96, 12.8, 0.26, WOOD_EDGE, radius=0.09)
    top = panel(0, -0.42, 12.8, 4.78, WALNUT, radius=0.23)
    front = panel(0, -2.86, 12.8, 0.25, "#4B3033", radius=0.10)
    grain = VGroup(line((-6.18, -2.57), (6.17, -2.57), "#795046", 1.4),
                   line((-6.17, 1.72), (6.17, 1.72), "#795046", 1.4))
    return VGroup(top, front, grain, lip)


def table_world():
    # The upper wall and window remain visible above the work surface.
    return VGroup(yard(), table())


def sort_sheet(idx):
    x = PILE_X[idx]
    sheet = panel(x, -0.34, 3.93, 4.24, "#263748", PLAN_COLORS[idx])
    heading = label(PLANS[idx], x, 1.35, 34, PLAN_COLORS[idx], width=3.49, weight=BOLD)
    rule = line((x - 1.63, 0.98), (x + 1.63, 0.98), PLAN_COLORS[idx], 2)
    return VGroup(sheet, heading, rule)


def animal_card(idx, x, y, w=2.34, h=3.08, named=True, art=None):
    paper = panel(x, y, w, h, PAPER, "#DCBDA2")
    drawing = art if art is not None else ANIMALS[idx]()
    drawing.scale_to_fit_width(w * 0.77)
    fit(drawing, max_h=h * (0.53 if named else 0.72))
    drawing.move_to(xy(x, y + (h * 0.16 if named else 0)))
    g = VGroup(paper, drawing)
    if named:
        name = label(NAMES[idx], x, y - h * 0.33, 30, INK, width=w - 0.23,
                     weight=BOLD)
        g.add(name)
        g.name_label = name
    g.drawing = drawing
    return g


def back(x, y, w=1.95, h=2.70):
    return VGroup(panel(x, y, w, h, NAVY, ICE),
                  panel(x, y, w - 0.25, h - 0.26, SLATE, ICE, radius=0.11),
                  Square(side_length=0.40, fill_color=ICE, fill_opacity=0.74, stroke_width=0).rotate(PI / 4).move_to(xy(x, y)))


def guess_piles():
    cards = []
    for idx, pile, dx, dy in [(1, 0, -0.68, -0.87), (7, 0, 0.68, -1.22),
                              (2, 1, -0.67, -0.87), (5, 1, 0.67, -1.22),
                              (9, 2, -0.67, -0.87), (0, 2, 0.67, -1.22)]:
        cards.append(animal_card(idx, PILE_X[pile] + dx, dy, 1.20, 1.58, named=False))
    return cards


def thermometer():
    return VGroup(panel(0, 0.24, 0.35, 1.62, "#E6ECED", radius=0.17),
                  disc(0, -0.56, 0.36, "#E6ECED"),
                  panel(0, -0.29, 0.15, 0.67, BLUE, radius=0.07),
                  disc(0, -0.56, 0.24, BLUE),
                  *[line((0.08, y), (0.15, y), SLATE, 2) for y in (0.2, 0.44, 0.68)])


def predict_cards():
    return (animal_card(0, -3.53, -0.28, 3.57, 4.35),
            animal_card(9, 3.53, -0.28, 3.57, 4.35))


def predict_question():
    card = question_card(QUESTION, y=2.79, size=42, max_w=10)
    card.question.set_x(0)
    card.add_to_back(panel(0, 2.79, card.question.width + 0.55, 0.72, INK))
    return card


def flower(x, y, scale=1, petal=ORANGE):
    parts = VGroup(line((0, -0.55), (0, 0.20), LEAF, 4),
                   oval(-0.12, -0.26, 0.31, 0.13, LEAF, -0.5),
                   oval(0.13, -0.11, 0.31, 0.13, LEAF, 0.5))
    for th in np.linspace(0, TAU, 6, endpoint=False):
        parts.add(disc(0.18 * np.cos(th), 0.25 + 0.18 * np.sin(th), 0.13, petal))
    parts.add(disc(0, 0.25, 0.105, GOLD))
    return parts.scale(scale).move_to(xy(x, y))


def insect(x, y, scale=1):
    return VGroup(oval(-0.13, 0.08, 0.30, 0.15, ICE, 0.40),
                  oval(0.13, 0.08, 0.30, 0.15, ICE, -0.40),
                  oval(0, 0, 0.13, 0.30, INK)).scale(scale).move_to(xy(x, y))


def spread(positions, start=xy(0, 0), scale=0.06, color=GOLD):
    return VGroup(*[disc(p[0] + start[0], p[1] + start[1], scale, color) for p in positions])


def notebook(x, y, w=3.75, h=2.6):
    page = panel(x, y, w, h, PAPER, "#BF9C79")
    ruled = VGroup(*[line((x - w * 0.37, y + h * dy), (x + w * 0.37, y + h * dy),
                          "#B7A48E", 1.6) for dy in (0.19, -0.05, -0.29)])
    return VGroup(page, ruled)


def ledger_lines(x, y):
    return VGroup(*[line((x, y - i * 0.52), (x + length, y - i * 0.52),
                         "#4F647C", 4)
                    for i, length in enumerate((1.7, 2.37, 1.92))])


def burrow_art(idx):
    earth = panel(0, -0.12, 2.75, 1.65, SOIL)
    snowcap = shape([(-1.37, 0.48), (-0.65, 0.54), (0.36, 0.48), (1.37, 0.57),
                     (1.37, 0.75), (-1.37, 0.75)], SNOW)
    cavity = oval(0.06, -0.29, 2.24, 0.92, "#39303A")
    sleeper = ANIMALS[idx]().scale_to_fit_height(0.72).move_to(xy(0.08, -0.28))
    if idx == 3:
        sleeper.rotate(-0.18)
        sleeper[-1].become(line((0.38, -0.05), (0.46, -0.06), INK, 2.5))
    return VGroup(earth, snowcap, cavity, sleeper)


def acorn():
    return VGroup(oval(0, -0.05, 0.35, 0.46, ORANGE, -0.17),
                  oval(-0.02, 0.10, 0.40, 0.18, SOIL, 0.13),
                  line((-0.03, 0.15), (-0.11, 0.25), SOIL, 3))


def deck_scene(scene):
    sheets = [sort_sheet(i) for i in range(3)]
    scene.add(table_world(), *sheets)
    return sheets


class S01Hook(SpokenScene):
    def construct(self):
        window = yard()
        red = cardinal().scale(1.52).move_to(xy(2.18, 0.44))
        ghost = hummingbird().scale(1.29).flip(UP).move_to(xy(-2.67, 0.95))
        ghost.set_fill(opacity=0.14)
        ghost.set_stroke(ICE, width=1.4, opacity=0.85)
        trail = spread([(-3.67, 0.48), (-4.04, 0.34), (-4.41, 0.22),
                        (-4.78, 0.14), (-5.15, 0.11)], color=ICE)
        self.add(window, snow(), red, ghost, trail)
        self.at("Why does")
        self.play(red.breast.animate.stretch(1.10, 1), run_time=1.1)
        self.at("when hummingbirds")
        self.play(FadeOut(ghost, shift=LEFT * 1.3 + UP * 0.39),
                  LaggedStart(*[FadeOut(d) for d in reversed(trail)], lag_ratio=0.16),
                  run_time=2.1)
        self.at("Use a card sort")
        q = badge("Who leaves? Who stays?", -2.68, 2.35, size=39)
        self.play(FadeIn(q, shift=UP * 0.11), run_time=0.48)
        bob(red, amp=0.045, speed=2.3)
        self.finish()


class S02Title(TitleCard):
    TITLE = "Parent Guide: Sleep, Travel or Stay?"
    LESSON = "Sleep, Travel or Stay?"

    def construct(self):
        self.add(yard(), snow(floor=2.10))
        plate = panel(0, 0.72, 11.28, 2.45, INK, GOLD, radius=0.22)
        guide = label("Parent Guide", 0, 1.39, 29, GOLD, weight=BOLD)
        title = label(self.LESSON, 0, 0.56, 60, font=TITLE_FONT)
        self.play(FadeIn(plate), run_time=0.26)
        self.play(FadeIn(guide), FadeIn(title, shift=UP * 0.12), run_time=0.45)
        self.wait(self.narration_s - self.elapsed())


class S03Payoff(SpokenScene):
    def construct(self):
        sheets = [sort_sheet(i) for i in range(3)]
        self.add(yard())
        self.at("Your child")
        self.play(FadeIn(table(), shift=UP * 0.6), run_time=0.56)
        self.play(LaggedStart(*(FadeIn(s, shift=UP * 0.52) for s in sheets),
                              lag_ratio=0.24), run_time=0.75)
        stack = animal_card(9, 4.26, -0.64, 1.28, 1.65, named=False)
        self.at("sorting with reasons")
        words = badge("Sort with reasons", 0, 2.81, TEAL)
        self.play(FadeIn(stack, shift=LEFT * 0.28), FadeIn(words), run_time=0.48)
        self.at("changing a guess")
        next_words = badge("Change a guess", 0, 2.81, BLUE)
        moth = animal_card(1, 0, -0.64, 1.28, 1.65, named=False)
        self.play(swap(words, next_words), FadeIn(moth), run_time=0.74)
        self.at("new evidence")
        self.play(moth.animate.shift(LEFT * 4.26), run_time=1.44)
        self.at("count what they see")
        count = badge("Count and compare", 0, 2.81, GREEN)
        tally = VGroup(*[line((x, -1.82), (x + 0.02, -1.49), PAPER, 4)
                         for x in (3.98, 4.26, 4.54)])
        self.play(swap(next_words, count), LaggedStart(*[Create(m) for m in tally],
                                                       lag_ratio=0.38), run_time=1.13)
        self.at("30 minutes")
        duration = badge("About 30 min", 0, 2.81, TEXT)
        self.play(swap(count, duration), run_time=0.49)
        self.at("15 -minute window")
        watch = badge("+ 15 min window watch", 0, 2.81, TEXT, size=30)
        self.play(swap(duration, watch), run_time=0.78)
        self.finish()


class S04Cards(SpokenScene):
    def construct(self):
        self.add(table_world())
        self.at("Draw print")
        template = back(0, -0.38)
        intro = badge("Make 10 animal cards", 0, 2.79)
        fan = VGroup(back(-2.10, -0.46).rotate(0.10), back(2.10, -0.46).rotate(-0.10))
        self.play(FadeIn(template, shift=UP * 0.85), run_time=0.65)
        self.play(FadeIn(fan, shift=UP * 0.48), FadeIn(intro), run_time=1.78)
        self.at("Label them")
        self.play(FadeOut(fan, shift=DOWN * 0.48),
                  template.animate.shift(RIGHT * 2.54), run_time=0.72)
        xs = (-5.06, -2.53, 0, 2.53, 5.06)
        cues = ("Ruby -throated", "monarch butterfly", "tundra swan", "groundhog and", "and bat",
                "Eastern box", "wood frog", "white -tailed", "gray squirrel", "northern cardinal")
        cards = []
        for i, cue in enumerate(cues):
            if i == 5:
                self.at(cue, lead=0.82)
                self.play(FadeOut(VGroup(*cards), shift=DOWN * 0.43), run_time=0.47)
                cards.clear()
            self.at(cue, lead=0.35)
            card = animal_card(i, xs[i % 5], -0.31)
            if i == 0:
                self.play(FadeOut(template, shift=DOWN * 0.4),
                          FadeIn(card, shift=UP * 0.70), run_time=0.4)
            else:
                self.play(FadeIn(card, shift=UP * 0.70), run_time=0.4)
            cards.append(card)
        self.finish()


class S05FirstSort(SpokenScene):
    def construct(self):
        self.add(table_world())
        self.at("Lay out")
        sheets = [sort_sheet(i) for i in range(3)]
        self.play(LaggedStart(*(FadeIn(s, shift=UP * 0.38) for s in sheets),
                              lag_ratio=0.35), run_time=1.32)
        self.at("travel rest")
        fanned = VGroup(*[back(x, -0.78, w=1.1, h=1.53).rotate(a)
                          for x, a in [(-0.33, 0.2), (0, 0), (0.33, -0.2)]])
        self.play(FadeIn(fanned, shift=UP * 0.61), run_time=0.87)
        first = badge("First guesses", 0, 2.78, GOLD)
        self.at("Let your child")
        cards = guess_piles()
        self.play(FadeOut(fanned), FadeIn(first), run_time=0.33)
        self.play(LaggedStart(*[FadeIn(c, shift=UP * 1.02 + (RIGHT if c.get_x() < 0 else LEFT) * 0.74)
                               for c in cards], lag_ratio=0.22), run_time=2.28)
        self.at("how did you decide")
        question = badge("How did you decide?", 0, 2.78, GOLD, size=37)
        self.play(swap(first, question), run_time=0.55)
        self.at("Write the reasons")
        note = notebook(0, -0.84, 3.55, 2.57)
        scribbles = ledger_lines(-1.14, -0.39)
        self.play(FadeOut(cards[2]), FadeOut(cards[3]), run_time=0.23)
        self.play(FadeIn(note, shift=UP * 0.37), run_time=0.4)
        self.play(LaggedStart(*[Create(r) for r in scribbles], lag_ratio=0.27), run_time=0.69)
        self.at("don't correct anything")
        self.play(swap(question, badge("No corrections yet", 0, 2.78, GOLD)), run_time=0.61)
        self.finish()


class S06PredictQuestion(SpokenScene):
    def construct(self):
        left, right = predict_cards()
        self.add(table_world())
        self.at("Now a question")
        self.play(FadeIn(thermometer(), shift=UP * 0.18), run_time=0.7)
        self.at("hummingbirds leave", lead=0.42)
        self.play(FadeIn(left, shift=RIGHT * 0.52), run_time=0.77)
        self.at("Cardinals stay", lead=0.55)
        right.shift(RIGHT * 0.72)
        self.play(FadeIn(right, shift=LEFT * 0.52), run_time=0.76)
        self.at("What do you predict")
        self.play(FadeIn(predict_question(), shift=UP * 0.12), run_time=0.55)
        self.at("the main reason", lead=0.12)
        self.play(right.animate.shift(LEFT * 0.24), run_time=1.18, rate_func=linear)
        self.play(right.animate.shift(LEFT * 0.48), run_time=0.58, rate_func=linear)
        self.finish()


class S07PredictPause(Scene):
    def construct(self):
        self.camera.background_color = BG
        self.add(table_world(), *predict_cards(), thermometer(), predict_question())
        self.wait(float(os.environ.get("KX_DURATION", "4.5")))


class S08Reveal(SpokenScene):
    def construct(self):
        left, right = predict_cards()
        q, cold = predict_question(), thermometer()
        self.add(table_world(), left, right, cold, q)
        self.at("Cold matters")
        self.play(FadeOut(q, shift=RIGHT * 0.48),
                  left.animate.shift(LEFT * 0.53), right.animate.shift(RIGHT * 0.53),
                  run_time=0.36, rate_func=linear)
        food = badge("Winter is hard: food runs short", 0, 2.78, GOLD, size=35)
        self.at("food is a big reason")
        self.play(FadeOut(cold, shift=DOWN * 0.42), FadeIn(food), run_time=0.59)
        hub = xy(-3.86, 0.36)
        feeder_flowers = VGroup(flower(-2.23, -0.59, 1.24),
                                flower(-1.47, -0.85, 0.97, RED),
                                insect(-1.83, 0.68, 1.02))
        bare = branch(3.75, -0.99, 1.28)
        red = cardinal().scale(1.39).move_to(xy(3.43, 0.10))
        hum = hummingbird().scale(1.25).move_to(hub).set_z_index(1)
        winter_view = panel(0, -0.38, 12.03, 4.18, NAVY, radius=0.21)
        snowy_ground = shape([(-5.97, -1.00), (-4.30, -0.89), (-3.34, -1.28),
                              (-1.62, -1.04), (0.0, -1.29), (1.85, -1.02),
                              (3.6, -1.12), (5.97, -0.76), (5.97, -2.37),
                              (-5.97, -2.37)], SNOW)
        self.at("Hummingbirds eat nectar", lead=0.65)
        self.play(FadeOut(left), FadeOut(right), FadeIn(winter_view), run_time=0.31)
        self.play(FadeIn(snowy_ground), FadeIn(hum), FadeIn(feeder_flowers), run_time=0.56)
        bob(feeder_flowers[2], amp=0.11, speed=6)
        self.at("those run out")
        frost = oval(-4.68, -0.97, 2.20, 0.61, SNOW)
        self.play(feeder_flowers[0].animate.shift(DOWN * 0.25).set_opacity(0),
                  feeder_flowers[1].animate.shift(DOWN * 0.20).set_opacity(0),
                  FadeOut(feeder_flowers[2]), FadeIn(frost, shift=UP * 0.23),
                  run_time=1.61)
        self.remove(feeder_flowers)
        self.at("So they travel")
        sunspot = VGroup(panel(-0.65, -0.59, 3.72, 3.38, "#3F6C71", ICE),
                         disc(0.23, 0.53, 0.43, GOLD),
                         oval(-0.66, -1.70, 2.85, 0.70, LEAF),
                         flower(-1.42, -1.42, 0.92, RED), flower(-0.47, -1.41, 1.04),
                         flower(0.45, -1.44, 0.80, RED))
        route = spread([(-3.34, 0.54), (-3.03, 0.48), (-2.77, 0.41),
                        (-2.52, 0.28), (-2.29, 0.11)], scale=0.062)
        flight = CubicBezier(hub, xy(-2.83, 0.62), xy(-2.51, 0.04), xy(-0.65, -0.46))
        self.play(FadeIn(sunspot), LaggedStart(*[FadeIn(p) for p in route], lag_ratio=0.15),
                  run_time=0.68)
        self.play(MoveAlongPath(hum, flight), run_time=1.45)
        self.at("Cardinals stay", lead=0.55)
        self.play(FadeIn(bare), run_time=0.44)
        self.play(FadeIn(red), run_time=0.43)
        self.at("fluff their feathers")
        self.play(red.breast.animate.stretch(1.26, 1).stretch(1.12, 0),
                  red[2].animate.stretch(1.17, 1), run_time=1.10)
        bob(red, amp=0.048, speed=2.3)
        self.finish()


def check_cards():
    return (animal_card(5, 0.83, -1.32, 1.53, 1.75, False, burrow_art(5)),
            animal_card(2, -0.71, -0.89, 1.31, 1.79, False))


class S09Check(SpokenScene):
    def construct(self):
        deck_scene(self)
        guesses = guess_piles()
        turtle_card, swan_card = check_cards()
        self.add(guesses[0], guesses[1], guesses[4], guesses[5], swan_card, turtle_card)
        self.at("Use the guide's")
        guide = notebook(-4.25, -0.75, 3.12, 2.54)
        guide.add(label("Animal list", -4.25, 0.06, 30, INK))
        self.play(FadeOut(guesses[0]), FadeOut(guesses[1]), run_time=0.26)
        self.play(FadeIn(guide, shift=UP * 0.45), run_time=0.76)
        reasons = ledger_lines(-5.43, -0.42)[:2]
        self.play(LaggedStart(*[Create(r) for r in reasons], lag_ratio=0.25),
                  run_time=1.14)
        self.at("where do you think")
        q = badge("Where does this one go?", 0, 2.78)
        self.play(FadeIn(q), swan_card.animate.shift(UP * 0.31), run_time=0.83)
        self.at("your child move cards")
        self.play(FadeOut(q), FadeOut(guide), FadeOut(reasons), guesses[5].animate.shift(LEFT * 9.16 + UP * 0.16),
                  swan_card.animate.shift(DOWN * 0.31), run_time=1.04)
        hog = groundhog().scale_to_fit_width(1.63).move_to(xy(-0.87, -0.83))
        den = burrow_art(3).scale_to_fit_width(1.50).move_to(xy(-0.88, -0.92))
        self.at("Groundhogs hibernate", lead=0.51)
        self.play(FadeOut(swan_card), FadeIn(hog), run_time=0.42)
        hog.set_z_index(1)
        self.play(FadeIn(VGroup(*den[:3])), Transform(hog, den[3]), run_time=1.37)
        self.at("Deer grow", lead=0.54)
        summer = deer().scale_to_fit_height(2.21).move_to(xy(3.73, -0.67))
        winter = deer(True).scale_to_fit_height(2.21).move_to(summer)
        self.play(FadeOut(guesses[4]), FadeIn(summer), run_time=0.56)
        self.play(Transform(summer, winter), run_time=1.05)
        self.at("Gray squirrels", lead=0.76)
        gray = squirrel().scale_to_fit_height(1.52).move_to(xy(5.02, -0.72))
        nut = acorn().move_to(xy(5.56, -1.73))
        ground = oval(5.32, -1.79, 1.44, 0.41, SOIL)
        self.play(FadeOut(summer), run_time=0.34)
        self.play(FadeIn(gray, shift=LEFT * 0.25), FadeIn(ground), run_time=0.55)
        self.play(gray.animate.rotate(-0.22).shift(DOWN * 0.24 + RIGHT * 0.13),
                  FadeIn(nut, shift=UP * 0.33), run_time=0.89)
        self.play(gray.animate.rotate(0.22).shift(UP * 0.27), nut.animate.shift(UP * 0.50),
                  run_time=0.91)
        self.finish()


def swan_map():
    board = panel(1.20, -0.33, 9.20, 4.46, NAVY, ICE, radius=0.21)
    land = shape([(-3.22, 1.65), (-2.93, 1.48), (-2.58, 1.69), (-1.90, 1.37),
                  (-1.37, 1.53), (-0.81, 1.26), (-0.19, 1.39), (0.48, 1.04),
                  (0.14, 0.62), (0.72, 0.73), (1.22, 1.07), (2.16, 0.94),
                  (2.57, 0.64), (2.01, 0.33), (2.26, 0.10), (1.71, -0.12),
                  (1.52, -0.40), (0.98, -0.52), (0.97, -0.79), (0.56, -0.97),
                  (0.39, -1.31), (-0.05, -1.60), (-0.05, -2.36),
                  (-3.22, -2.36)], "#587D6F")
    arctic = shape([(-3.22, 1.65), (-2.93, 1.48), (-2.58, 1.69), (-1.9, 1.37),
                    (-1.37, 1.53), (-0.81, 1.26), (-0.19, 1.39), (0.48, 1.04),
                    (-0.26, 0.76), (-0.78, 0.92), (-1.45, 0.51), (-2.25, 0.77),
                    (-2.88, 0.57), (-3.22, 0.69)], SNOW)
    lakes = VGroup(oval(-0.18, 0.06, 1.10, 0.22, SLATE, 0.30),
                   oval(0.15, -0.21, 0.61, 0.15, SLATE, -0.14))
    bay = VGroup(line((0.88, -0.70), (0.45, -0.62), ICE, 3),
                  line((0.62, -0.78), (0.14, -0.87), ICE, 3))
    return VGroup(board, land, arctic, lakes, bay)


class S10Swan(SpokenScene):
    def construct(self):
        sheets = deck_scene(self)
        t, mover = check_cards()
        self.add(t, mover)
        self.at("When a card moves")
        end = xy(-4.25, -0.89)
        move = CubicBezier(mover.get_center(), xy(-1.78, 0.71), xy(-3.55, 0.71), end)
        arc = CurvedArrow(xy(-1.87, -0.21), xy(-3.61, -0.23), angle=0.68,
                          color=GOLD, stroke_width=4, tip_length=0.17)
        self.play(Create(arc), run_time=0.39)
        self.play(MoveAlongPath(mover, move), run_time=1.39)
        self.at("what made you change")
        q = badge("What made you change your mind?", 0, 2.8, size=35)
        self.play(FadeIn(q), FadeOut(arc), run_time=0.49)
        self.at("Tundra swans")
        large = animal_card(2, -4.88, -0.39, 2.36, 3.39)
        self.play(FadeOut(mover), FadeOut(t), FadeOut(sheets[0]), run_time=0.26)
        self.play(FadeIn(large, shift=UP * 0.36), run_time=0.50)
        self.at("They nest in", lead=0.72)
        geo = swan_map()
        self.play(FadeOut(q), FadeOut(sheets[1]), FadeOut(sheets[2]), run_time=0.28)
        self.play(FadeIn(geo, shift=LEFT * 0.12), run_time=0.55)
        start, end = xy(-2.17, 1.11), xy(0.68, -0.86)
        north = badge("Arctic", -0.55, 2.80, ICE, 31)
        south = badge("Virginia rivers and bays", 3.08, -1.87, ICE, 31)
        self.at("in the Arctic")
        self.play(FadeIn(north), FadeIn(disc(*start[:2], 0.10, TEAL)), run_time=0.38)
        self.at("fly thousands", lead=0.40)
        path = CubicBezier(start, xy(-1.36, 0.72), xy(-1.81, -0.64), end)
        path.set_stroke(GOLD, width=6)
        tip = ArrowTriangleFilledTip(length=0.24, color=GOLD)
        bearing = angle_of_vector(end - xy(-1.81, -0.64))
        tip.rotate(bearing - tip.tip_angle).shift(end - tip.tip_point)
        flyer = swan().scale_to_fit_width(0.75).move_to(start)
        self.play(Create(path), MoveAlongPath(flyer, path.copy()), run_time=1.55, rate_func=smooth)
        self.at("south")
        self.play(FadeIn(tip), FadeIn(south), run_time=0.52)
        self.finish()


def watch_sheet(x=4.22, y=-0.25, w=3.77, h=4.77, heading="Window watch"):
    page = panel(x, y, w, h, PAPER, "#C7A98E", radius=0.18)
    title = label(heading, x, y + h * 0.36, 35, INK, width=w - 0.47, weight=BOLD)
    lines = VGroup(*[line((x - w * 0.42, y + h * dy), (x + w * 0.42, y + h * dy),
                          "#B7A48E", 2) for dy in (0.23, -0.05, -0.34)])
    return VGroup(page, title, lines)


def marks(x, y, n, scale=1):
    return VGroup(*[line((x + 0.16 * i * scale, y), (x + (0.16 * i + 0.028) * scale, y + 0.34 * scale),
                         INK, 3.5) for i in range(n)])


def sparrow():
    return VGroup(shape([(-0.22, -0.13), (-0.94, -0.48), (-0.86, -0.58), (0.16, -0.31)], BARK),
                  oval(0, -0.16, 1.20, 0.69, "#A67451", 0.15),
                  oval(-0.07, -0.23, 0.76, 0.36, "#D5AF80", 0.2),
                  disc(0.39, 0.20, 0.29, "#8C654F"),
                  shape([(0.54, 0.24), (0.87, 0.14), (0.61, 0.05)], ORANGE),
                  disc(0.48, 0.27, 0.043, INK))


class S11Watch(SpokenScene):
    def construct(self):
        self.add(yard(), snow())
        self.at("Sit at the window")
        timer = badge("15 min", -3.65, 2.2, ICE, 41)
        clock_track = Circle(radius=0.67, stroke_color=ICE, stroke_width=3).move_to(xy(-4.40, 0.98))
        hand = line((-4.40, 0.98), (-4.40, 1.49), GOLD, 5)
        self.play(FadeIn(timer), Create(clock_track), GrowFromPoint(hand, xy(-4.40, 0.98)),
                  run_time=0.81)
        self.play(Rotate(hand, -PI / 2, about_point=xy(-4.40, 0.98)), run_time=1.29)
        self.at("predict how many")
        page = watch_sheet()
        page.shift(RIGHT * 0.50)
        q = badge("How many kinds?", -3.65, 2.2, GOLD, 37)
        self.play(swap(timer, q), FadeIn(page, shift=LEFT * 0.55), run_time=0.88)
        self.at("kinds of birds")
        self.play(page.animate.shift(LEFT * 0.50),
                  Rotate(hand, -TAU * 0.65, about_point=xy(-4.40, 0.98)),
                  run_time=0.47)
        self.at("Write down their guess")
        guess = label("My guess", 4.22, 0.17, 31, INK)
        written = label("2", 4.22, -0.95, 49, INK)
        self.play(FadeIn(guess), FadeOut(clock_track), FadeOut(hand), run_time=0.38)
        self.play(Write(written), run_time=0.72)
        row1 = cardinal().scale_to_fit_height(0.69).move_to(xy(3.03, 0.20))
        row2 = sparrow().scale_to_fit_height(0.76).move_to(xy(3.04, -1.03))
        red = cardinal().scale_to_fit_height(1.17).move_to(xy(0.83, 0.37))
        brown = sparrow().scale_to_fit_height(0.91).move_to(xy(-2.0, -1.26))
        self.at("Tally the birds")
        self.play(FadeOut(q), FadeOut(guess), FadeOut(written), run_time=0.33)
        upper_tally, lower_tally = marks(3.87, 0.01, 1)[0], marks(3.87, -1.20, 1)[0]
        self.play(FadeIn(red, shift=LEFT * 0.44 + DOWN * 0.83), FadeIn(row1),
                  Create(upper_tally), run_time=0.73)
        action = label("Perched", 4.99, 0.25, 29, INK)
        self.play(FadeIn(brown, shift=RIGHT * 1.28 + DOWN * 0.76), FadeIn(row2), FadeIn(action),
                  Create(lower_tally), run_time=0.72)
        self.at("note what they do")
        hop = ArcBetweenPoints(brown.get_center(), brown.get_center() + RIGHT * 1.1,
                               angle=-0.72)
        behavior = label("Hopping", 4.99, -1.04, 29, INK)
        self.play(MoveAlongPath(brown, hop), FadeIn(behavior), run_time=0.92)
        self.at("An empty yard")
        self.play(FadeOut(red, shift=UP * 0.8 + LEFT * 0.49),
                  FadeOut(brown, shift=UP * 0.51 + LEFT * 1.22),
                  FadeOut(VGroup(row1, row2, action, behavior, upper_tally, lower_tally)), run_time=0.58)
        # Replace the example with a fresh sheet for a watch with zero sightings.
        empty = watch_sheet()
        zero = label("0 birds seen", 4.22, 0.16, 33, INK)
        above = badge("Empty yard? Still a result.", -3.33, 2.24, GOLD, 33)
        self.play(FadeOut(page), run_time=0.22)
        self.play(FadeIn(empty), FadeIn(zero), FadeIn(above), run_time=0.54)
        self.finish()


def people():
    adult = VGroup(disc(-0.55, 0.50, 0.43, "#D89B72"),
                   oval(-0.55, 0.78, 0.82, 0.39, BARK, 0.09),
                   panel(-0.55, -0.49, 1.33, 1.32, TEAL, radius=0.31))
    child = VGroup(disc(0.52, 0.20, 0.32, "#E4B089"),
                   oval(0.52, 0.42, 0.62, 0.30, BARK, 0.14),
                   panel(0.52, -0.62, 0.93, 1.02, GOLD, radius=0.27))
    return VGroup(adult, child)


def hand():
    palm = panel(0, -0.17, 0.77, 0.91, "#D89B72", radius=0.25)
    fingers = VGroup(*[panel(x, y, 0.20, h, "#D89B72", radius=0.10)
                       for x, y, h in [(-0.28, 0.35, 0.73), (-0.07, 0.47, 0.93),
                                       (0.14, 0.43, 0.83), (0.35, 0.36, 0.68)]])
    thumb = oval(-0.43, -0.07, 0.28, 0.59, "#D89B72", 0.49)
    return VGroup(fingers, thumb, palm)


def no_touch():
    palm = hand().scale_to_fit_height(1.14)
    ring = Circle(radius=0.71, stroke_color=RED, stroke_width=6).move_to(palm)
    slash = line((-0.48, 0.49), (0.48, -0.49), RED, 6).move_to(ring)
    return VGroup(palm, ring, slash)


def safety_stage():
    return VGroup(yard(), panel(0, -0.57, 9.88, 4.40, INK, ICE, radius=0.25))


def safety_art(art, x=0, y=-0.57):
    return art.scale_to_fit_height(3.1).move_to(xy(x, y))


class S12Safety(SpokenScene):
    def construct(self):
        self.add(safety_stage())
        together = safety_art(people())
        self.at("Stay with your child")
        self.play(LaggedStart(*[FadeIn(person, shift=UP * 0.33) for person in together],
                              lag_ratio=0.52), run_time=1.05)
        words = badge("Stay together", 0, 2.65, ICE, 39)
        self.play(FadeIn(words), run_time=0.43)
        self.at("the whole activity")
        self.play(together[1].animate.shift(LEFT * 0.22), run_time=0.92)
        self.at("Nobody touches")
        shell = turtle().scale_to_fit_width(3.72).move_to(xy(-1.65, -0.64))
        stop = no_touch().scale(1.4).move_to(xy(2.40, -0.50))
        caution = badge("Hands off wild animals", 0, 2.65, RED, 38)
        self.play(FadeOut(together), FadeOut(words), run_time=0.30)
        self.play(FadeIn(shell, shift=RIGHT * 0.32), FadeIn(stop[0]), run_time=0.64)
        self.play(Create(stop[1]), Create(stop[2]), FadeIn(caution), run_time=0.74)
        self.at("alive or dead")
        self.play(shell.animate.shift(LEFT * 0.50), run_time=1.05)
        self.at("Never touch a bat")
        sleeping = bat().rotate(PI).scale_to_fit_width(3.50).move_to(xy(-1.73, -0.39))
        feet = VGroup(line((-1.81, 0.22), (-1.77, 0.46), "#383B53", 5),
                      line((-1.65, 0.22), (-1.69, 0.46), "#383B53", 5))
        sleeping.add(feet)
        beam = line((-3.3, 0.46), (-0.18, 0.46), WOOD_EDGE, 7)
        never = badge("Never touch a bat", 0, 2.65, RED, 39)
        self.play(FadeOut(shell), FadeOut(caution), run_time=0.36)
        self.play(FadeIn(beam), FadeIn(sleeping), run_time=0.56)
        self.play(FadeIn(never), run_time=0.43)
        self.at("seems asleep or hurt")
        self.play(Rotate(sleeping, 0.22, about_point=xy(-1.73, 0.46)),
                  rate_func=there_and_back, run_time=1.72)
        self.at("Bats can carry rabies")
        rabies = label("Bats can carry rabies", -1.25, -1.97, 33, PAPER)
        self.play(FadeIn(rabies, shift=UP * 0.18), run_time=0.7)
        self.finish()


def litter():
    rng = np.random.default_rng(1126)
    leaves = VGroup()
    for y in (-0.15, -0.58, -0.97):
        for x in np.linspace(-3.15, 3.15, 12):
            leaves.add(oval(x, y + rng.uniform(-0.10, 0.10), rng.uniform(0.65, 1.02), 0.40,
                            rng.choice(["#A1744E", "#AF6743", "#CA8F55", "#74513F"]),
                            rng.uniform(-0.49, 0.49)))
    return leaves


def bird_feeder():
    food = panel(0, -0.28, 1.02, 1.42, "#AE7951", radius=0.08)
    seeds = spread([(-0.33, -0.48), (-0.12, -0.41), (0.12, -0.46), (0.36, -0.40),
                    (-0.24, -0.70), (0.04, -0.63), (0.24, -0.68)], scale=0.048, color=PAPER)
    roof = shape([(-0.92, 0.34), (0, 1.0), (0.92, 0.34)], "#BB7253")
    tray = panel(0, -1.02, 1.76, 0.18, "#CC9970", radius=0.07)
    return VGroup(food, seeds, roof, tray)


def wash():
    hands = VGroup(hand().rotate(-1.07).shift(LEFT * 0.36 + DOWN * 0.33),
                   hand().rotate(1.02).shift(RIGHT * 0.33 + DOWN * 0.64))
    spout = VGroup(panel(-0.56, 0.69, 0.24, 0.82, ICE, radius=0.08),
                   panel(-0.30, 1.03, 0.73, 0.22, ICE, radius=0.08),
                   panel(0.05, 0.88, 0.24, 0.46, ICE, radius=0.08))
    drops = spread([(0.03, 0.45), (0.095, 0.24), (0.02, 0.02)], scale=0.052, color=BLUE)
    g = VGroup(hands, spout, drops)
    g.drops = drops
    return g


class S13Safety2(SpokenScene):
    def construct(self):
        self.add(safety_stage())
        bed = panel(0, -1.00, 7.42, 2.05, SOIL, radius=0.23)
        sleepers = VGroup(turtle().scale_to_fit_width(2.21).move_to(xy(-1.83, -0.61)),
                          frog().scale_to_fit_width(2.05).move_to(xy(1.70, -0.61)))
        self.add(bed, sleepers)
        self.at("Leave resting")
        leaf_cover = litter()
        word = badge("Leave them covered", 0, 2.65, ICE, 38)
        self.play(LaggedStart(*[FadeIn(leaf, shift=UP * 0.85) for leaf in leaf_cover],
                              lag_ratio=0.11), FadeIn(word), run_time=3.50)
        self.at("Use a feeder")
        feeder = bird_feeder().scale(1.31).move_to(xy(-1.77, -0.40))
        winter = badge("Feeder only in winter", 0, 2.65, ICE, 37)
        self.play(FadeOut(bed), FadeOut(sleepers), FadeOut(leaf_cover), FadeOut(word), run_time=0.36)
        self.play(FadeIn(feeder, shift=DOWN * 0.47), FadeIn(winter), run_time=0.68)
        self.at("An adult handles")
        adult_hands = VGroup(hand().rotate(-0.68), hand().rotate(0.88)).arrange(RIGHT, buff=0.65)
        adult_hands.move_to(xy(-1.78, -1.51))
        self.play(FadeIn(adult_hands, shift=UP * 0.46), run_time=0.84)
        self.at("washes hands")
        wash_art = wash().scale(1.30).move_to(xy(2.35, -0.25))
        wash_words = label("Wash hands", 2.40, -2.35, 35, ICE)
        self.play(FadeIn(wash_art, shift=UP * 0.35), run_time=0.63)
        bob(wash_art.drops, amp=0.14, speed=6.0)
        self.play(FadeIn(wash_words), run_time=0.47)
        self.at("Keep birdseed away")
        seeds = VGroup(*[oval(x, y, 0.42, 0.18, color, angle) for x, y, color, angle in
                         [(-0.40, 0.16, ORANGE, 0.40), (0.29, 0.26, GOLD, 1.00),
                          (-0.025, -0.23, PAPER, -0.64), (0.41, -0.19, ORANGE, 0.28)]])
        red_ring = Circle(radius=0.88, stroke_color=RED, stroke_width=7)
        prohibited = VGroup(seeds, red_ring, line((-0.62, 0.62), (0.62, -0.62), RED, 7))
        face = VGroup(disc(0, 0, 0.65, "#E4B089"), oval(-0.06, 0.43, 1.17, 0.50, BARK, 0.1),
                      disc(-0.22, 0.03, 0.056, INK), disc(0.22, 0.03, 0.056, INK),
                      oval(0, -0.22, 0.18, 0.07, BARK))
        age = badge("Under 4: choking risk", 0, 2.65, RED, 38)
        self.play(FadeOut(winter), FadeOut(feeder), FadeOut(adult_hands),
                  FadeOut(wash_art), FadeOut(wash_words), run_time=0.42)
        prohibited.shift(LEFT * 1.02)
        face.shift(RIGHT * 0.97)
        self.play(FadeIn(prohibited, shift=LEFT * 0.3), FadeIn(face, shift=RIGHT * 0.30),
                  run_time=0.76)
        self.play(FadeIn(age), run_time=0.54)
        self.at("from children under")
        self.play(prohibited.animate.shift(LEFT * 0.68), face.animate.shift(RIGHT * 0.68),
                  run_time=1.54)
        self.at("call 911")
        call = badge("Call 911", 0, -1.82, RED, 41)
        self.play(FadeIn(call, shift=UP * 0.31), run_time=0.58)
        self.finish()


def season_notes(spring=False):
    x = 3.11 if spring else -3.11
    page = watch_sheet(x, -0.21, 4.80, 4.84, "Spring watch" if spring else "Winter watch")
    red = cardinal().scale_to_fit_height(0.82).move_to(xy(x - 1.27, 0.27))
    tally = marks(x - 0.36, 0.08, 2 if spring else 1, 1.18)
    brown = sparrow().scale_to_fit_height(0.72).move_to(xy(x - 1.27, -1.10))
    second = marks(x - 0.36, -1.26, 2, 1.18)
    return page, VGroup(red, tally), VGroup(brown, second)


class S14Return(SpokenScene):
    def construct(self):
        window = yard()
        self.add(window)
        self.at("Repeat the window watch")
        time = badge("Same time of day", -3.28, 2.24, ICE, 35)
        self.play(Transform(window, yard(True)), run_time=2.21)
        self.at("at the same time")
        self.play(FadeIn(time, shift=UP * 0.22), run_time=0.56)
        left, lred, _ = season_notes()
        right, rred, new = season_notes(True)
        self.at("Compare the two sheets")
        self.play(FadeOut(time), run_time=0.30)
        self.play(LaggedStart(FadeIn(left, shift=LEFT * 0.54),
                              FadeIn(right, shift=RIGHT * 0.54), lag_ratio=0.31),
                  run_time=1.42)
        self.at("Which kinds did you see both")
        self.play(LaggedStart(FadeIn(lred, shift=RIGHT * 0.18),
                              FadeIn(rred, shift=RIGHT * 0.18), lag_ratio=0.37),
                  run_time=1.02)
        self.at("Which did you see only once")
        who = badge("Who came? Who went?", 0, 2.87, GOLD, 36)
        self.play(FadeIn(new, shift=RIGHT * 0.26), FadeIn(who), run_time=0.85)
        self.at("Think about what food")
        q = badge("What food was available?", 0, 2.87, GOLD, 36)
        bloom = flower(5.45, -2.54, 1.0, ORANGE)
        self.play(swap(who, q), GrowFromPoint(bloom, xy(5.45, -2.98)), run_time=1.63)
        self.finish()


class S15End(EndCard):
    LINE = "Winter food runs short: animals travel, rest, or stay and change."
