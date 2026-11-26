"""The Daphne Major drought, shown with schematic finches and counted birds.

Blue: shallow beak. Yellow: middle beak. Green: deep beak.
Gold: dry conditions and hard seeds. White: measurements, tests and neutral marks.
"""
from bp_parts import *


BEAK_COLORS = (BLUE, YELLOW, GREEN)
LAND = "#577268"
SHORE = "#9AB6A8"
WATER = "#294657"
SOFT_SEED = "#DEA47B"

START = (0, 1, 0, 2, 1, 0, 2, 1, 2)
SURVIVORS = (0, 4, 6, 8)
LOST = tuple(i for i in range(len(START)) if i not in SURVIVORS)
YOUNG = ((0, 1, 1), (2, 2, 2, 2, 2))
ROOSTS = (
    (-4.4, 0.58), (-3.0, 1.92), (-2.0, 0.20),
    (2.98, 1.88), (0.5, 0.25), (1.85, 1.42),
    (2.95, 0.24), (4.25, 1.16), (4.9, 0.02),
)
SORTED = (
    (-3.95, 1.22), (-0.82, 1.22), (-3.2, 0.10),
    (2.48, 1.22), (0, 0.10), (-2.45, 1.22),
    (3.25, 0.10), (0.82, 1.22), (4.03, 1.22),
)
SEARCH = tuple(
    {0: (-4.45, -0.05), 4: (0.15, -0.30), 6: (2.02, 0.04)}.get(i, point)
    for i, point in enumerate(SORTED)
)


def xy(x, y):
    return np.array([x, y, 0.0])


def heading(text, color=TEXT):
    return T(text, 38, color).move_to(xy(0, 3.08))


def finch(kind, scale=1.0, facing=1, neutral=False):
    """Every instance keeps its beak depth fixed, including when it moves or grows."""
    color = TEXT if neutral else BEAK_COLORS[kind]
    body = Ellipse(width=0.96, height=0.67, color=color, fill_opacity=0.66, stroke_width=3)
    tail = Polygon(xy(-0.32, 0.14), xy(-0.84, 0.30), xy(-0.67, 0.01), xy(-0.38, -0.16),
                   color=color, fill_opacity=0.60, stroke_width=2.7)
    head = Circle(radius=0.27, color=color, fill_opacity=1, stroke_width=2.5).move_to(xy(0.38, 0.23))
    depth = (0.17, 0.29, 0.43)[kind]
    beak = Polygon(xy(0.60, 0.22 - depth / 2), xy(0.60, 0.22 + depth / 2), xy(1.11, 0.20),
                   color=color, fill_opacity=0.96, stroke_width=2.4)
    wing = ArcBetweenPoints(xy(-0.36, 0.08), xy(0.2, -0.09), angle=0.85, color=BG, stroke_width=2.8)
    eye = Dot(xy(0.445, 0.315), radius=0.043, color=BG)
    legs = VGroup(*[Line(xy(x, -0.27), xy(x + 0.03, -0.48), color=color, stroke_width=2.6)
                    for x in (-0.18, 0.04)])
    bird = VGroup(tail, legs, body, head, beak, eye, wing)
    if facing < 0:
        bird.flip(UP)
    bird.beak, bird.legs = beak, legs
    return bird.scale(scale)


def island():
    """The same schematic island sits above the same shoreline in each landscape scene."""
    outline = [(-6.55, -1.23), (-5.62, -0.50), (-4.53, -0.18), (-3.25, 0.94),
               (-1.90, 2.03), (-0.82, 1.79), (0.30, 0.99), (1.49, 1.74),
               (2.50, 2.21), (3.77, 1.35), (4.79, 0.22), (5.78, -0.25), (6.55, -1.23)]
    land = Polygon(*[xy(*p) for p in outline], color=SHORE, fill_color=LAND,
                   fill_opacity=1, stroke_width=2.8)
    left_ridge = VMobject(color="#789489", stroke_width=2.5).set_points_as_corners(
        [xy(-5.50, -0.63), xy(-3.37, 0.17), xy(-1.88, 1.35), xy(-0.80, 1.03), xy(0.08, 0.38)])
    right_ridge = VMobject(color="#789489", stroke_width=2.5).set_points_as_corners(
        [xy(0.81, -0.81), xy(2.02, 0.06), xy(2.70, 1.29), xy(3.65, 0.51), xy(4.39, -0.49)])
    sea = Line(xy(-6.62, -1.28), xy(6.62, -1.28), color=WATER, stroke_width=5)
    return VGroup(land, left_ridge, right_ridge, sea)


def flock(positions=ROOSTS):
    return VGroup(*[finch(kind, 0.63).move_to(xy(*point))
                    for kind, point in zip(START, positions)])


def subset(birds, indices):
    return VGroup(*[birds[i] for i in indices])


def counts(kinds):
    return tuple(kinds.count(kind) for kind in range(3))


START_COUNTS = counts(START)
SURVIVOR_COUNTS = counts(tuple(START[i] for i in SURVIVORS))
LOST_COUNTS = counts(tuple(START[i] for i in LOST))
YOUNG_COUNTS = counts(YOUNG[0] + YOUNG[1])


def depth_chart(box=(-4.72, 4.72, -2.90, -1.53), max_count=5, scope=None):
    chart = Plot(box, xr=(-0.5, 2.5), yr=(0, max_count),
                 xticks=((0, "shallow"), (1, "middle"), (2, "deep")), color=SHORE, size=28)
    for label, color in zip(chart.tick_labels, BEAK_COLORS):
        label.set_color(color)
    chart.add(scope if scope is not None else scope_tag("schematic", size=28, color=TEXT))
    return chart


def bars(chart, values, outline=False, width=None):
    """Bin heights use one common scale. Each value is a count from the birds."""
    result = VGroup()
    for i, (value, color) in enumerate(zip(values, BEAK_COLORS)):
        base = chart.pt(i, 0)
        height = chart.pt(i, value)[1] - base[1]
        bar_width = width if width is not None else (1.50 if outline else 0.94)
        bar = Rectangle(width=bar_width, height=height, color=color,
                        stroke_width=3.3, fill_opacity=0 if outline else 0.85)
        result.add(bar.move_to(base + UP * height / 2))
    return result


def grow_bars(group, lag=0.22):
    return LaggedStart(*[GrowFromEdge(bar, DOWN) for bar in group], lag_ratio=lag)


def chart_key(word, y, outline=False):
    mark = Square(.18, color=TEXT, stroke_width=2.5, fill_opacity=0 if outline else 1)
    key = VGroup(mark, T(word, 28)).arrange(RIGHT, buff=.12)
    return key.move_to(xy(-6.70, y), aligned_edge=LEFT)


def calipers(bird):
    tip = bird.beak.get_left()
    top, bottom = bird.beak.get_top()[1], bird.beak.get_bottom()[1]
    x = tip[0] + 0.92
    return VGroup(
        Line(xy(x, bottom - 0.20), xy(x, top + 0.22), color=TEXT, stroke_width=4),
        Line(xy(tip[0] + 0.025, top + 0.055), xy(x, top + 0.055), color=TEXT, stroke_width=3),
        Line(xy(tip[0] + 0.025, bottom - 0.055), xy(x, bottom - 0.055), color=TEXT, stroke_width=3),
    )


def seed(hard, x, y, scale=1.0):
    points = ((-.40, 0), (-.21, .28), (.21, .32), (.44, .08), (.24, -.22), (-.26, -.26))
    if hard:
        shell = Polygon(*[xy(*point) for point in points], color=GOLD, stroke_width=3,
                        fill_color="#AB7540", fill_opacity=1)
        seed_mob = VGroup(shell, Line(xy(-.21, .15), xy(.19, .20), color=GOLD, stroke_width=2.8))
    else:
        seed_mob = VGroup(Ellipse(width=.48, height=.30, color=SOFT_SEED, stroke_width=2.5,
                                 fill_opacity=0.84).rotate(0.35))
    return seed_mob.scale(scale).move_to(xy(x, y))


def food(cracked=False):
    soft = VGroup(*[seed(False, x, y, 1.60) for x, y in (
        (-5.04, -0.75), (-4.04, -0.79), (-1.98, -0.67), (-0.57, -0.79), (.50, -0.78), (4.41, -0.68)
    )])
    hard = VGroup(*[seed(True, x, y, 1.26) for x, y in (
        (-2.99, -0.77), (1.49, -0.78), (2.70, -0.78), (5.57, -0.72)
    )])
    halves = (
        ((2.13, -.79), (2.33, -.49), (2.64, -.41), (2.49, -.76), (2.64, -1.11), (2.28, -1.07)),
        ((2.82, -.43), (3.10, -.45), (3.30, -.70), (3.10, -1.05), (2.82, -1.11), (2.68, -.77)),
    )
    crack = VGroup(*[Polygon(*[xy(*p) for p in half], color=GOLD, fill_color="#C89653",
                              fill_opacity=1, stroke_width=3.4) for half in halves])
    if cracked:
        hard[2].become(crack)
    return soft, hard, crack


def prediction():
    first = question_card("Which birds will contribute more young", size=41, max_w=11)
    second = question_card("to the next generation?", size=38, max_w=11)
    return VGroup(first.move_to(xy(0, 3.28)), second.move_to(xy(0, 2.69)))


def lock(beak):
    body = RoundedRectangle(width=.44, height=.33, corner_radius=.065, color=TEXT, stroke_width=2.8,
                            fill_color=TEXT, fill_opacity=1)
    hoop = Arc(radius=.14, start_angle=0, angle=PI, color=TEXT, stroke_width=3.3).next_to(body, UP, buff=-.018)
    keyhole = Dot(body.get_center(), radius=.040, color=BG)
    return VGroup(body, hoop, keyhole).scale(.75).next_to(beak, UP, buff=.10)


def family_parents():
    """Four survivors retain their beaks as they take up the two parent positions."""
    points = ((-4.0, 1.66), (1.80, 1.66), (-1.80, 1.66), (4.0, 1.66))
    return VGroup(*[finch(START[i], 0.91).move_to(xy(*point)) for i, point in zip(SURVIVORS, points)])


def family_young():
    places = (((-2.90, .20), (-3.75, -.64), (-2.12, -.64)),
              ((2.90, .20), (1.50, -.64), (2.75, -.64), (4.00, -.64), (4.11, .21)))
    return tuple(VGroup(*[finch(kind, .58 if i == 0 else .53).move_to(xy(*point))
                          for i, (kind, point) in enumerate(zip(kinds, positions))])
                 for kinds, positions in zip(YOUNG, places))


def family_branch(parents, child):
    """Two lines join before the arrow to a child, so both parents are visible."""
    x, y, _ = child.get_top()
    joint = xy(x, y + .31)
    legs = VGroup(*[Line(p.get_bottom() + DOWN * .07, joint, color=TEXT, stroke_width=2.5)
                    for p in parents])
    tip = Arrow(joint, child.get_top() + UP * .07, buff=0, color=TEXT,
                tip_length=.12, stroke_width=2.7)
    return VGroup(legs, tip)


class S00Title(TitleCard):
    LESSON = "Natural Selection and New Species"
    TITLE = "The Drought Sorts a Population"

    def construct(self):
        birds = flock()
        wing = (1, 3, 7)
        final = [birds[i].get_center().copy() for i in wing]
        for i, start_shift in zip(wing, (xy(-.8, .36), xy(-.7, .40), xy(-.65, .34))):
            birds[i].shift(start_shift)
        title = fit_text(self.TITLE, size=50, min_size=42, max_w=11.7, font=TITLE_FONT).move_to(xy(0, 3.13))
        self.add(island(), birds)
        self.play(FadeIn(title), *[birds[i].animate.move_to(p) for i, p in zip(wing, final)], run_time=.62)
        self.wait(.86)
        self.play(FadeOut(title), run_time=.36)
        self.wait(.16)


class S01Puzzle(SpokenScene):
    def construct(self):
        birds = flock()
        gone = subset(birds, LOST)
        survivors = subset(birds, SURVIVORS)
        chart = depth_chart()
        before = bars(chart, START_COUNTS, outline=True)
        after = bars(chart, SURVIVOR_COUNTS)
        self.add(island(), *birds)

        question = heading("What did the drought change?", GOLD)
        self.at("Did the drought")
        self.play(FadeIn(question), run_time=.55)
        wind = VGroup(*[Arrow(xy(x, y), xy(x + 2.65, y), buff=0, color=GOLD, stroke_width=11, tip_length=.24)
                        for x, y in ((-5.72, 2.55), (-1.64, 2.36), (2.33, 2.51))])
        self.at("change which birds")
        self.play(LaggedStart(*[GrowArrow(w) for w in wind], lag_ratio=.24), run_time=1.45)
        self.at("On Daphne major")
        place = T("Daphne Major", 48).move_to(xy(0, 3.07))
        self.play(swap(question, place), run_time=.63)
        self.at("finches died")
        self.play(LaggedStart(*[FadeOut(bird) for bird in gone], lag_ratio=.23), run_time=2.04)

        self.at("Researchers had measured")
        before_key = chart_key("Before", -1.92, outline=True)
        survivor_key = chart_key("Survivors", -2.44)
        self.play(FadeOut(wind), FadeIn(gone), FadeIn(chart), FadeIn(before_key), run_time=.62)
        tools = VGroup(*[calipers(birds[i]) for i in (0, 4, 6)])
        self.play(LaggedStart(*[Create(tool) for tool in tools], lag_ratio=.40), run_time=.84)
        self.play(grow_bars(before), FadeOut(tools), run_time=1.0)

        self.at("The survivors had")
        self.play(FadeOut(gone), grow_bars(after), FadeIn(survivor_key), run_time=1.74)
        self.at("Watch the population")
        self.play(LaggedStart(*[birds[i].animate.move_to(xy(*SORTED[i])) for i in SURVIVORS], lag_ratio=.20),
                  run_time=1.65)
        self.play(FadeOut(place), run_time=.50)
        self.finish()


class S02Variation(SpokenScene):
    def construct(self):
        birds = flock()
        chart = depth_chart()
        before = bars(chart, START_COUNTS, outline=True)
        after = bars(chart, SURVIVOR_COUNTS)
        before_key = chart_key("Before", -1.92, outline=True)
        survivor_key = chart_key("Survivors", -2.44)
        for i in SURVIVORS:
            birds[i].move_to(xy(*SORTED[i]))
        self.add(island(), chart, before, after, before_key, survivor_key, *subset(birds, SURVIVORS))

        self.at("Before the drought")
        self.play(FadeOut(after), FadeOut(survivor_key),
                  LaggedStart(*[FadeIn(birds[i]) for i in LOST], lag_ratio=.15),
                  *[birds[i].animate.move_to(xy(*ROOSTS[i])) for i in SURVIVORS], run_time=1.63)
        self.at("height of the beak")
        closeup = finch(2, 1.85).move_to(xy(-0.8, 1.30))
        gauge = calipers(closeup)
        other_birds = VGroup(*(b for i, b in enumerate(birds) if i != 3))
        original = birds[3].copy()
        self.play(FadeOut(other_birds), Transform(birds[3], closeup), run_time=.65)
        self.play(Create(gauge), run_time=.85)
        self.play(Transform(birds[3], original), FadeOut(gauge), FadeIn(other_birds), run_time=.52)

        for kind, phrase in enumerate(("Blue birds had", "yellow birds had", "green birds had")):
            self.at(phrase, lead=.35)
            group = [i for i, k in enumerate(START) if k == kind]
            # The left yellow finch takes the upper route past the already-sorted blue birds.
            moves = [birds[i].animate(path_arc=-PI / 3 if i == 1 else 0).move_to(xy(*SORTED[i]))
                     for i in group]
            self.play(LaggedStart(*moves, lag_ratio=.20), run_time=1.28)
        self.at("These differences existed")
        label = heading("Variation before drought")
        self.play(FadeIn(label), run_time=.68)
        filled = bars(chart, START_COUNTS)
        self.at("Variation gives")
        self.play(grow_bars(filled), run_time=1.45)
        self.play(FadeOut(before), FadeOut(before_key), FadeOut(label), run_time=.42)
        self.finish()


class S03Seeds(SpokenScene):
    def construct(self):
        birds = flock(SORTED)
        chart = depth_chart()
        start = bars(chart, START_COUNTS)
        soft, hard, crack = food()
        self.add(island(), birds, chart, start)

        self.at("Then drought changed")
        self.play(FadeIn(soft), FadeIn(hard), run_time=.85)
        self.at("Small soft seeds")
        self.play(LaggedStart(*[FadeOut(kernel, scale=.32) for kernel in soft], lag_ratio=.26), run_time=2.12)
        self.at("large hard seeds")
        self.play(birds[0].animate.move_to(xy(*SEARCH[0])), birds[4].animate.move_to(xy(*SEARCH[4])), run_time=1.35)

        self.at("Deeper beaks could")
        focused_bird = birds[6]
        rest = VGroup(*(b for b in birds if b is not focused_bird))
        close_bird = focused_bird.copy().scale(1.86).move_to(xy(-.23, .97))
        close_seed = hard[2].copy().scale(1.79).move_to(xy(1.60, .63))
        close_crack = crack.copy().scale(1.79).move_to(close_seed)
        self.play(Transform(focused_bird, close_bird), Transform(hard[2], close_seed),
                  rest.animate.set_opacity(.20), run_time=.77)
        self.at("crack those hard")
        self.play(Transform(hard[2], close_crack), run_time=.73)
        normal_bird = finch(2, .63).move_to(xy(*SEARCH[6]))
        restoration = [Transform(b, target) for i, (b, target) in enumerate(zip(birds, flock(SEARCH))) if i != 6]
        self.play(Transform(focused_bird, normal_bird), Transform(hard[2], crack),
                  *restoration, run_time=.85)
        self.at("Which birds do")
        question = prediction()
        self.play(FadeIn(question[0]), run_time=.74)
        self.at("to the next generation")
        self.play(FadeIn(question[1]), run_time=.66)
        self.at("Follow the colors")
        wide = bars(chart, START_COUNTS, width=1.48)
        self.play(LaggedStart(*[Transform(bar, target) for bar, target in zip(start, wide)], lag_ratio=.56),
                  run_time=1.92)
        emphasized = bars(chart, START_COUNTS, width=2.26)
        self.play(*[Transform(bar, target, rate_func=linear) for bar, target in zip(start, emphasized)],
                  run_time=1.02)
        self.finish()


class S04Pause(Scene):
    def construct(self):
        self.camera.background_color = BG
        chart = depth_chart()
        start = bars(chart, START_COUNTS, width=2.26)
        _, hard, _ = food(cracked=True)
        self.add(island(), flock(SEARCH), chart, start, hard, prediction())
        self.wait(float(os.environ["KX_DURATION"]))


class S05Survival(SpokenScene):
    def construct(self):
        birds = flock(SEARCH)
        chart = depth_chart()
        start = bars(chart, START_COUNTS, width=2.26)
        before = bars(chart, START_COUNTS, outline=True)
        after = bars(chart, SURVIVOR_COUNTS)
        _, hard, _ = food(cracked=True)
        question = prediction()
        self.add(island(), *birds, chart, start, hard, question)

        self.at("More green birds")
        self.remove(question)
        self.play(FadeOut(subset(birds, LOST)), FadeOut(hard),
                  Transform(start, after), run_time=1.77)
        self.at("but some birds")
        self.play(LaggedStart(*[birds[i].animate.move_to(xy(*ROOSTS[i])) for i in SURVIVORS],
                              lag_ratio=.23), run_time=1.65)
        self.at("The groups overlap")
        before_key = chart_key("Before", -1.92, outline=True)
        survivor_key = chart_key("Survivors", -2.44)
        self.play(grow_bars(before), FadeIn(before_key), FadeIn(survivor_key), run_time=1.35)

        better = heading("Better chance here", GREEN)
        self.at("A deep beak")
        green_pair = subset(birds, (6, 8))
        comparison = SurroundingRectangle(green_pair, color=GREEN, buff=.20, corner_radius=.19, stroke_width=3.5,
                                          fill_color=GREEN, fill_opacity=.23)
        self.play(FadeIn(comparison), Indicate(start[2], color=GREEN, scale_factor=1.02), run_time=.94)
        self.play(FadeIn(better), run_time=.64)
        self.at("guarantee survival")
        lost_green = finch(2, 1.46).move_to(xy(-1.71, 1.42))
        self.play(FadeOut(comparison), FadeIn(lost_green), run_time=.55)
        self.play(FadeOut(lost_green, scale=.72), run_time=.92)

        self.at("A helpful trait")
        seed_context = seed(True, 4.28, -.77)
        self.play(FadeIn(seed_context), birds[6].animate.move_to(xy(3.48, -.38)), run_time=1.05)
        self.play(FadeOut(seed_context), FadeOut(better), birds[6].animate.move_to(xy(*ROOSTS[6])), run_time=1.05)
        self.finish()


class S06Inheritance(SpokenScene):
    def construct(self):
        chart = depth_chart()
        before = bars(chart, START_COUNTS, outline=True)
        after = bars(chart, SURVIVOR_COUNTS)
        young_bars = bars(chart, YOUNG_COUNTS)
        previous = subset(flock(), SURVIVORS)
        parents = family_parents()
        before_key = chart_key("Before", -1.92, outline=True)
        survivor_key = chart_key("Survivors", -2.44)
        young_key = chart_key("Young", -2.44)
        self.add(island(), chart, before, after, before_key, survivor_key, *previous)

        self.at("Survival alone")
        self.play(*[Transform(b, p) for b, p in zip(previous, parents)],
                  FadeOut(after), FadeOut(survivor_key), run_time=2.45)
        inherited = heading("Inherited beak depth")
        first_family, second_family = family_young()
        left_child, right_child = first_family[0], second_family[0]
        branches = VGroup(family_branch((previous[0], previous[2]), left_child),
                          family_branch((previous[1], previous[3]), right_child))
        family_highlights = VGroup(*[
            SurroundingRectangle(pair, color=TEXT, buff=.13, corner_radius=.16, stroke_width=3,
                                 fill_color=TEXT, fill_opacity=.19)
            for pair in ((VGroup(previous[0], previous[2])), (VGroup(previous[1], previous[3])))])
        self.at("Beak size is")
        self.play(LaggedStart(*[FadeIn(panel) for panel in family_highlights], lag_ratio=.42),
                  Create(branches[0][0]), Create(branches[1][0]), run_time=1.50)
        self.at("so parents and young")
        self.play(GrowArrow(branches[0][1]), GrowArrow(branches[1][1]), run_time=.45)
        self.play(FadeIn(left_child, scale=.7), FadeIn(right_child, scale=.7), FadeIn(inherited), run_time=1.04)

        left_more, right_more = first_family[1:], second_family[1:]
        self.at("The survivors breed")
        offspring = (*left_more, *right_more)
        origins = (left_child, left_child, right_child, right_child, right_child, right_child)
        self.play(LaggedStart(*[
            FadeIn(b, scale=.62, shift=b.get_center() - origin.get_center()) for b, origin in zip(offspring, origins)
        ], lag_ratio=.18), run_time=1.89)

        young = (VGroup(left_child), left_more, VGroup(right_child, *right_more))
        self.at("Their young form")
        self.play(FadeOut(branches), FadeOut(family_highlights), FadeOut(inherited), run_time=.45)
        for kind in (0, 1):
            self.play(Succession(*[
                Succession(b.animate.move_to(chart.pt(kind, .65)), FadeOut(b, scale=.62)) for b in young[kind]
            ]), run_time=.60)
            self.play(GrowFromEdge(young_bars[kind], DOWN), run_time=.36)
        self.at("now with deeper")
        intake = [Succession(b.animate.move_to(chart.pt(2, .74)), FadeOut(b, scale=.55)) for b in young[2]]
        self.play(LaggedStart(*intake, lag_ratio=.82), run_time=1.65)
        self.play(GrowFromEdge(young_bars[2], DOWN), FadeIn(young_key), run_time=.58)

        self.at("That makes change")
        across = heading("Across generations", GOLD)
        increase = Rectangle(width=1.44, height=chart.pt(2, 5)[1] - chart.pt(2, 3)[1],
                             color=GREEN, stroke_width=2, fill_opacity=.65).move_to(chart.pt(2, 4))
        self.play(FadeIn(across), GrowFromEdge(increase, DOWN), run_time=.82)
        self.at("not within one life")
        locks = VGroup(*[lock(b.beak) for b in previous])
        self.play(FadeOut(increase), LaggedStart(*[FadeIn(mark) for mark in locks], lag_ratio=.23), run_time=1.05)
        self.finish()


class S07Evidence(SpokenScene):
    def construct(self):
        terrain = island()
        adults = family_parents()
        locks = VGroup(*[lock(b.beak) for b in adults])
        chart = depth_chart()
        earlier, next_generation = bars(chart, START_COUNTS, outline=True), bars(chart, YOUNG_COUNTS)
        across = heading("Across generations", GOLD)
        keys = VGroup(chart_key("Before", -1.92, outline=True), chart_key("Young", -2.44))
        self.add(terrain, *adults, locks, chart, earlier, next_generation, across, keys)

        panels = TwoPanel("Measured before", "Checked later", colors=(SHORE, SHORE),
                          top=3.14, bottom=-3.22, gap=.56, size=34)
        tracked = (adults[0], adults[1], adults[2])
        left_x, right_x = -2.86, 3.64
        rows = (1.48, -.17, -1.82)
        ids = ("21", "34", "57")
        self.at("Researchers did not")
        self.play(FadeOut(VGroup(chart, earlier, next_generation, across, keys)), FadeOut(locks), run_time=.40)
        self.bring_to_front(*tracked)
        self.play(FadeOut(terrain), FadeOut(adults[3]),
                  FadeIn(panels), *[b.animate.scale(1.12).move_to(xy(left_x, y)) for b, y in zip(tracked, rows)],
                  run_time=1.40)

        bands = VGroup()
        labels = VGroup()
        for bird, band_id, y in zip(tracked, ids, rows):
            ring = Rectangle(width=.13, height=.10, color=TEXT, stroke_width=2,
                             fill_color=BG, fill_opacity=1).move_to(bird.legs[1])
            label = boxed_label(band_id, size=34, pad=.18, fill_opacity=.31).move_to(xy(-4.80, y - .19))
            bands.add(ring)
            labels.add(label)
        self.at("Each measured bird")
        measures = VGroup(*[calipers(bird) for bird in tracked])
        self.play(LaggedStart(*[Create(tool) for tool in measures], lag_ratio=.38), run_time=1.10)
        self.at("numbered band before")
        self.play(LaggedStart(*[AnimationGroup(FadeIn(ring), FadeIn(label)) for ring, label in zip(bands, labels)],
                              lag_ratio=.32), FadeOut(measures), run_time=1.36)

        self.at("Later the team")
        found = VGroup()
        for i in (1, 2):
            copy = VGroup(tracked[i], bands[i]).copy()
            found.add(copy)
            self.play(copy.animate.shift(RIGHT * (right_x - left_x)), run_time=.79)
        missing = boxed_label("Not found", color=TEXT, size=29, pad=.13).move_to(xy(right_x, rows[0]))
        checks = VGroup(*[labels[i].copy().move_to(xy(1.64, rows[i] - .19)) for i in (1, 2)])
        self.play(FadeIn(missing), FadeIn(checks), run_time=.58)

        large_chart = depth_chart(box=(-5.12, 5.12, -2.55, 1.55), max_count=3)
        nonsurvivors = bars(large_chart, LOST_COUNTS, outline=True)
        survivors = bars(large_chart, SURVIVOR_COUNTS)
        survival = heading("Survival evidence")
        legend = VGroup(T("Outline • nonsurvivors", 29), T("Fill • survivors", 29)).arrange(RIGHT, buff=1.12)
        legend.move_to(xy(0, 2.20))
        self.at("Comparing the groups")
        self.play(FadeOut(VGroup(panels, *tracked, bands, labels, found, missing, checks)), run_time=.52)
        self.play(FadeIn(large_chart), grow_bars(nonsurvivors), run_time=.90)
        self.play(grow_bars(survivors), FadeIn(legend), FadeIn(survival), run_time=1.22)
        self.at("It shows an association")
        overlap = Rectangle(width=10.08, height=1.26, stroke_width=0, color=TEXT, fill_opacity=.21)
        overlap.move_to(xy(0, -1.88))
        self.add(overlap)
        self.bring_to_front(large_chart, nonsurvivors, survivors)
        self.play(GrowFromEdge(overlap, DOWN), run_time=1.22)
        self.at("not a promise")
        self.play(FadeOut(overlap), nonsurvivors[2].animate.set_stroke(TEXT, width=5.5),
                  run_time=1.15)
        self.at("Parents and young")
        self.play(FadeOut(VGroup(large_chart, nonsurvivors, survivors, survival, legend)), run_time=.53)
        pair, child, lines = inheritance_picture()
        self.play(FadeIn(pair), run_time=.61)
        self.play(Create(lines[0]), run_time=.54)
        self.play(GrowArrow(lines[1]), FadeIn(child), run_time=.39)
        self.at("inheritance evidence")
        self.play(FadeIn(heading("Inheritance evidence")), run_time=.53)
        self.finish()


def inheritance_picture():
    pair = VGroup(finch(1, 1.22).move_to(xy(-1.52, 1.32)),
                  finch(2, 1.22, facing=-1).move_to(xy(1.52, 1.32)))
    child = finch(2, .87).move_to(xy(0, -1.52))
    return pair, child, family_branch(pair, child)


class S08Rule(SpokenScene):
    def construct(self):
        pair, child, lines = inheritance_picture()
        evidence = heading("Inheritance evidence")
        inheritance = VGroup(pair, child, lines)
        self.add(inheritance, evidence)
        title = heading("Natural selection")
        self.at("This is natural")
        self.play(swap(evidence, title), inheritance.animate.scale(.78).shift(UP * .52), run_time=1.42)

        variations = VGroup(*[finch(kind, .80).move_to(xy(-4.42, y))
                              for kind, y in enumerate((1.57, .62, -.34))])
        results = VGroup(*[finch(kind, .67).move_to(xy(x, y))
                           for kind, x, y in ((0, 3.65, 1.53), (2, 3.65, .22),
                                              (2, 4.65, .82), (2, 5.33, -.12))])
        first_arrow = Arrow(xy(-3.30, .71), xy(-1.96, .71), color=TEXT, buff=0, tip_length=.20)
        next_arrow = Arrow(xy(1.94, .71), xy(2.84, .71), color=TEXT, buff=0, tip_length=.19)
        labels = (
            T("Variation", 30).move_to(xy(-4.42, -1.19)),
            T("Inherited resemblance", 30).move_to(xy(0, -1.19)),
            T("Unequal offspring", 30).move_to(xy(4.38, -1.19)),
        )
        self.at("It needs variation")
        self.play(FadeIn(variations), run_time=.50)
        self.play(FadeIn(labels[0]), run_time=.34)
        self.at("inheritance and")
        self.play(GrowArrow(first_arrow), FadeIn(labels[1]), run_time=.67)
        self.at("unequal reproductive")
        self.play(GrowArrow(next_arrow), run_time=.51)
        self.play(LaggedStart(*[FadeIn(b, scale=.74) for b in results], lag_ratio=.18), run_time=.95)
        self.play(FadeIn(labels[2]), run_time=.45)

        self.at("Inherited traits spread")
        rule = T("Inherited traits spread when their carriers\nleave more reproducing offspring.",
                 36, GOLD, line_spacing=.80).move_to(xy(0, -2.48))
        self.play(FadeIn(rule), run_time=.75)
        self.at("leave more reproducing")
        row = VGroup(*[finch(2, .74).move_to(xy(x, .02)) for x in (2.87, 4.43, 5.99)])
        self.play(LaggedStart(*[Transform(b, target) for b, target in zip(results[1:], row)],
                              lag_ratio=.30), run_time=1.45)
        self.at("Fitness means that")
        fitness = caption("Fitness • contribution to the next generation", size=34, y=-2.48)
        self.play(swap(rule, fitness), run_time=.75)
        self.play(FadeOut(VGroup(variations, labels[0], first_arrow)),
                  results[0].animate.set_opacity(.34), run_time=1.04)

        self.at("It does not simply")
        descendant = finch(2, .76).move_to(xy(4.95, -1.94))
        pair_at_right = VGroup(results[2], results[3])
        self.play(FadeOut(labels[2]), run_time=.34)
        branch = family_branch(pair_at_right, descendant)
        self.play(Create(branch[0]), run_time=.58)
        self.play(GrowArrow(branch[1]), FadeIn(descendant, scale=.68), run_time=1.12)
        self.finish()


def gene_block(name, color):
    return boxed_label(name, color=color, size=47, pad=.22, box=(1.64, .99), fill_opacity=.25)


class S09Sources(SpokenScene):
    def construct(self):
        shore = island()
        first = heading("Mutation")
        version = gene_block("A", BLUE).move_to(xy(-2.04, .72))
        new_version = gene_block("A′", TEAL).move_to(xy(2.04, .72))
        change = Arrow(xy(-1.00, .72), xy(1.00, .72), color=TEXT, buff=0, stroke_width=5.2, tip_length=.24)
        board = RoundedRectangle(width=11.42, height=5.12, corner_radius=.21, stroke_width=2.4,
                                 stroke_color=WATER, fill_color="#22313D", fill_opacity=1)
        board.move_to(xy(0, -.57))
        self.add(board, version)
        self.at("Mutation supplies")
        self.play(GrowArrow(change), FadeIn(first), run_time=.64)
        self.at("new gene versions")
        self.play(FadeIn(new_version, shift=RIGHT * .20), run_time=.72)

        parents = VGroup(
            VGroup(gene_block("A′", TEAL), gene_block("B", YELLOW)).arrange(RIGHT, buff=.22).move_to(xy(-3.14, .99)),
            VGroup(gene_block("A", BLUE), gene_block("B′", GREEN)).arrange(RIGHT, buff=.22).move_to(xy(3.14, .99)),
        )
        self.at("sexual reproduction")
        self.play(FadeOut(version), FadeOut(new_version), FadeOut(change), run_time=.30)
        recombination_heading = heading("Sexual reproduction")
        self.play(FadeIn(parents), swap(first, recombination_heading), run_time=.75)
        self.at("shuffles them into")
        combined = VGroup(parents[0][0], parents[1][1])
        self.play(*[block.animate.set_y(-1.58) for block in combined], run_time=.79)
        self.play(combined[0].animate.set_x(-.96), combined[1].animate.set_x(.96), run_time=.90)
        combination_label = T("New combination", 30).move_to(xy(0, -2.63))
        self.play(FadeIn(combination_label), run_time=.45)
        self.at("Selection does not")
        birds = flock()
        marks = VGroup(*[lock(b.beak) for b in birds])
        self.play(FadeOut(VGroup(parents, combination_label)), run_time=.47)
        self.play(FadeIn(shore), FadeIn(birds), FadeOut(board), FadeOut(recombination_heading), run_time=.77)
        self.at("because organisms need")
        self.play(FadeIn(marks), run_time=.70)

        self.at("It sorts inherited")
        selection = heading("Selection sorts existing variation")
        self.play(FadeOut(marks), FadeOut(subset(birds, LOST)), run_time=1.43)
        self.play(FadeIn(selection), run_time=.58)
        self.at("including mutations")
        variation = gene_block("A′", TEAL).move_to(xy(-2.36, -2.38))
        inherited = T("New inherited variation", 33).move_to(xy(1.07, -2.38))
        self.play(FadeIn(variation), FadeIn(inherited), run_time=.85)
        self.at("No finch changed")
        self.play(FadeOut(VGroup(selection, variation, inherited)),
                  LaggedStart(*[FadeIn(marks[i]) for i in SURVIVORS], lag_ratio=.28),
                  run_time=1.25)
        self.finish()


class S10Scope(SpokenScene):
    def construct(self):
        terrain = island()
        birds = flock()
        living = subset(birds, SURVIVORS)
        locks = VGroup(*[lock(b.beak) for b in living])
        _, hard, _ = food()
        self.add(terrain, *living, locks)

        self.at("The advantage is")
        self.play(FadeOut(locks), FadeIn(hard), run_time=1.31)
        self.at("If rainfall and")
        rain = VGroup(*[Line(xy(x, y), xy(x - .23, y - .51), color=BLUE,
                             stroke_width=3.4) for x, y in ((-5.30, 2.43), (-4.30, 2.73), (-3.42, 2.35),
                                                             (-2.61, 2.69), (-1.43, 2.75), (-.40, 2.45),
                                                             (.80, 2.69), (1.74, 2.65), (2.78, 2.74),
                                                             (3.82, 2.38), (4.63, 2.63), (5.39, 2.43))])
        soft, _, _ = food()
        self.play(FadeIn(rain, shift=UP * .29), run_time=.38)
        self.play(rain.animate.shift(DOWN * .65), FadeOut(hard[0]), FadeOut(hard[1]),
                  LaggedStart(*[FadeIn(kernel) for kernel in soft], lag_ratio=.12), run_time=1.21)

        self.at("selection can change")
        arrow_center = xy(0, 2.03)
        direction = Arrow(arrow_center + LEFT * .59, arrow_center + RIGHT * .59,
                          buff=0, color=TEXT, stroke_width=4.3, tip_length=.20)
        label = heading("Direction can change")
        self.play(FadeOut(rain), GrowArrow(direction), run_time=.44)
        self.play(Rotate(direction, -PI, about_point=arrow_center), FadeIn(label), run_time=1.06)

        self.at("Chance and arrivals")
        arrival = finch(1, .86, neutral=True).move_to(xy(-5.63, 1.42))
        arrivals = heading("Chance and arrivals")
        self.play(FadeOut(direction), swap(label, arrivals), FadeIn(arrival), run_time=.62)
        self.play(arrival.animate.move_to(xy(-3.14, 1.66)), run_time=2.27)

        fixed = heading("Adult beaks stayed the same")
        self.at("The drought did")
        self.play(FadeOut(VGroup(arrival, soft, hard[2], hard[3])),
                  swap(arrivals, fixed), LaggedStart(*[FadeIn(mark) for mark in locks], lag_ratio=.16), run_time=1.22)

        parents = family_parents()
        self.at("It changed which")
        self.play(FadeOut(locks), FadeOut(fixed),
                  *[Transform(b, p) for b, p in zip(living, parents)], run_time=1.39)
        first_family, second_family = family_young()
        branches = VGroup(family_branch((living[0], living[2]), first_family[0]),
                          family_branch((living[1], living[3]), second_family[0]))
        self.at("and bred")
        self.play(Create(branches[0]), Create(branches[1]), run_time=.54)
        self.play(FadeIn(first_family[0], scale=.72), FadeIn(second_family[0], scale=.72), run_time=.47)

        self.at("The next generation")
        chart = depth_chart()
        before = bars(chart, START_COUNTS, outline=True)
        after = bars(chart, YOUNG_COUNTS)
        self.play(FadeIn(chart), FadeIn(before), FadeIn(chart_key("Before", -1.92, outline=True)),
                  FadeIn(first_family[1:]), FadeIn(second_family[1:]), run_time=.62)
        self.play(grow_bars(after), FadeIn(chart_key("Young", -2.44)),
                  FadeIn(heading("The next generation", GOLD)), run_time=1.52)
        self.finish()


class S11End(EndCard):
    LINE = "Inherited traits spread when their carriers leave more reproducing offspring."
