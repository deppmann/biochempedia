"""Dominant Is Not Popular · Inherited or Acquired? · Chapter 2.

Chapter 1 color map: blue genes and alleles, green environment, gold acquired
body changes, teal routes to offspring, red stopped routes, grey structures.
The model uses grey for the second allele and gold for the rejected trophy.
"""
from bp_parts import *
from bp_style import EndCard


LEFT_X, RIGHT_X = -3.40, 3.40
SLOTS_X = (2.38, 4.42)
SLOTS_Y = 1.06
QUESTION = "Will the trait show?"
QUESTION_STYLE = {"y": 3.35, "size": 34}
BLUE_CELLS = (1, 6, 9)
HOOK_OFFSETS = ((-0.03, 0.43, 0), (0.20, 0.22, 0), (-0.38, -0.24, 0))
# Local bowl coordinates. Each empty space in the top two rows is a landing site.
BOWL_CELLS = (
    (-1.35, 1.08), (-0.44, 1.08), (0.47, 1.08), (1.38, 1.08),
    (-1.84, 0.20), (-0.92, 0.20), (0.00, 0.20), (0.92, 0.20), (1.84, 0.20),
    (-1.37, -0.68), (-0.46, -0.68), (0.46, -0.68), (1.37, -0.68),
    (-0.47, -1.46), (0.47, -1.46),
)
LANDINGS = ((-2.26, 0.97), (2.26, 0.97), (-1.91, -0.62),
            (1.91, -0.62), (-1.31, -1.45), (1.31, -1.45))


def label(word, x, y, color=TEXT, size=32):
    return T(word, size, color, weight=BOLD).move_to([x, y, 0])


def card(color, scale=1):
    """Chapter 1's rounded gene card, with two distinct locus patterns."""
    blue = color == BLUE
    face = RoundedRectangle(width=0.54, height=0.70, corner_radius=0.075,
                            stroke_color=color, stroke_width=3, fill_color=color, fill_opacity=0.40)
    widths = (0.28, 0.34, 0.22) if blue else (0.16, 0.20, 0.36)
    bars = VGroup(*(Line(LEFT * w / 2, RIGHT * w / 2, color=TEXT,
                         stroke_width=2.4).shift(UP * y)
                    for w, y in zip(widths, (0.17, -0.01, -0.18))))
    return VGroup(face, bars).scale(scale).set_z_index(2)


def person(x, y, scale=1):
    head = Circle(radius=0.19, color=GREY, stroke_width=3,
                  fill_color=GREY, fill_opacity=0.35).shift(UP * 0.22)
    body = Arc(radius=0.40, start_angle=0.1 * PI, angle=0.8 * PI,
               arc_center=DOWN * 0.34, color=GREY, stroke_width=4)
    return VGroup(head, body).scale(scale).move_to([x, y, 0])


def bowl(x=LEFT_X, size=1, people=False):
    """The shared glass bowl. Its lip, cards and landing sites share one origin."""
    glass = VMobject(stroke_color=GREY, stroke_width=4,
                     fill_color=GREY, fill_opacity=0.29)
    glass.set_points_as_corners([[-2.94, 2.21, 0], [2.94, 2.21, 0]])
    glass.add_cubic_bezier_curve_to(*np.array([[2.72, 0.43, 0], [2.33, -1.9, 0], [1.43, -2.25, 0]]))
    glass.add_line_to(np.array([-1.43, -2.25, 0]))
    glass.add_cubic_bezier_curve_to(*np.array([[-2.33, -1.9, 0], [-2.72, 0.43, 0], [-2.94, 2.21, 0]]))
    lip = ArcBetweenPoints(np.array([-2.94, 2.21, 0]), np.array([2.94, 2.21, 0]), angle=0.21,
                           color=GREY, stroke_width=3)
    cards = VGroup(*(card(BLUE if i in BLUE_CELLS else GREY, 0.79).move_to([cx, cy, 0])
                     for i, (cx, cy) in enumerate(BOWL_CELLS)))
    silhouettes = VGroup()
    if people:
        for px, py in ((-2.6, 2.48), (-0.85, 2.48), (0.85, 2.48), (2.6, 2.48),
                       (-3.70, 0.83), (3.70, 0.83)):
            silhouettes.add(person(px, py, 1.17))
    world = VGroup(glass, lip, cards, silhouettes).scale(size, about_point=ORIGIN)
    world.shift([x, 0.69, 0])
    world.cards, world.glass = cards, glass
    return world


def pair(left=None, right=GREY, result=None):
    """One individual's card slots and phenotype window, anchored across scenes."""
    frame = RoundedRectangle(width=5.72, height=4.48, corner_radius=0.26,
                             stroke_color=GREY, stroke_width=3,
                             fill_color=GREY, fill_opacity=0.20).move_to([RIGHT_X, 0.69, 0])
    slots = VGroup(*(RoundedRectangle(width=1.35, height=1.13, corner_radius=0.13,
                                      stroke_color=GREY, stroke_width=3,
                                      fill_color=BG, fill_opacity=0.92).move_to([x, SLOTS_Y, 0])
                     for x in SLOTS_X))
    copies = [None if color is None else card(color, 1.30).move_to(slot)
              for color, slot in zip((left, right), slots)]
    window = phenotype_window(result)
    individual = person(RIGHT_X, 2.30, 1.18)
    world = VGroup(frame, individual, slots, *[c for c in copies if c is not None], window)
    world.frame, world.individual, world.slots = frame, individual, slots
    world.copies, world.window = copies, window
    return world


def phenotype_window(result=None):
    color = result or GREY
    return RoundedRectangle(width=3.55, height=0.94, corner_radius=0.17, stroke_color=color,
                            stroke_width=4, fill_color=color if result else BG,
                            fill_opacity=0.65 if result else 0.80).move_to([RIGHT_X, -0.64, 0])


def shows():
    return label("shows", RIGHT_X, -0.64, BG, 32)


def emphasis(shape, color=BLUE, inset=0.13):
    """A finite outline drawn when narration points to a specific object."""
    return SurroundingRectangle(shape, color=color, buff=inset, corner_radius=0.16, stroke_width=4)


def focus(scene, shape, color=BLUE, time=1.2, inset=0.13):
    scene.play(ShowPassingFlash(emphasis(shape, color, inset), time_width=0.58), run_time=time)


def highlight_fill(scene, shape, opacity, time=1.35):
    """Briefly distinguish the narrated area without changing its state."""
    scene.play(shape.animate.set_fill(opacity=opacity), rate_func=there_and_back, run_time=time)


def card_lane():
    return card(BLUE, 1.30).move_to([-0.13, SLOTS_Y, 0])


def before_answer():
    return bowl(), pair(), card_lane()


def prediction_prompt():
    question = question_card(QUESTION, **QUESTION_STYLE)
    question.move_to([RIGHT_X, QUESTION_STYLE["y"], 0]).set_z_index(2)
    backing = RoundedRectangle(width=question.width + 0.32, height=0.70, corner_radius=0.15,
                               color=GOLD, stroke_width=4, fill_color=GREY,
                               fill_opacity=0.44).move_to(question)
    return question, backing


def blue_fraction(added=0):
    return (len(BLUE_CELLS) + added) / (len(BOWL_CELLS) + added)


def level_display(tracker, x, name):
    """Filled share of a fixed track, driven by the illustrated sample or phenotype."""
    width, height, y = 4.55, 0.53, -2.15
    track = RoundedRectangle(width=width, height=height, corner_radius=0.11,
                             stroke_color=GREY, stroke_width=3,
                             fill_color=GREY, fill_opacity=0.13).move_to([x, y, 0])

    def fill():
        fill_width = max(0.001, (width - 0.16) * tracker.get_value())
        return Rectangle(width=fill_width, height=height - 0.15, stroke_width=0,
                         fill_color=BLUE, fill_opacity=float(fill_width > 0.001)).move_to(
                             [x - width / 2 + 0.08 + fill_width / 2, y, 0])

    return VGroup(track, always_redraw(fill), label(name, x, -2.78, BLUE, 28))


def displays(group=None, showing=1):
    group_value = ValueTracker(blue_fraction() if group is None else group)
    show_value = ValueTracker(showing)
    return (level_display(group_value, LEFT_X, "common in this group"),
            level_display(show_value, RIGHT_X, "shows in this individual"),
            group_value, show_value)


def trait_route():
    return Arrow([RIGHT_X, 0.42, 0], [RIGHT_X, -0.11, 0], color=TEAL, buff=0.06,
                 stroke_width=4, tip_length=0.15)


class S00Hook(SpokenScene):
    def construct(self):
        population = bowl(x=0, size=1.07, people=True)
        tag = scope_tag(size=28)
        self.at("The first film")
        self.play(DrawBorderThenFill(population[0]), FadeIn(population[1:]),
                  FadeIn(tag), run_time=1.5)
        blue = VGroup(*(population.cards[i] for i in BLUE_CELLS))
        self.at("If an allele")
        grey = [c for i, c in enumerate(population.cards) if i not in BLUE_CELLS]
        grey_targets = [c.copy() for c in grey]
        question = label("?", 4.17, 2.62, GOLD, 88)
        self.play(*(c.animate.set_opacity(0.28) for c in grey),
                  population.glass.animate.set_fill(opacity=0.47), GrowFromCenter(question),
                  LaggedStart(*(ShowPassingFlash(emphasis(c, BLUE, 0.09), time_width=0.6)
                                for c in blue), lag_ratio=0.55), run_time=1.55)
        self.at("Watch a few blue cards")
        # Small arcs take the highlighted cards through clear spaces in the sample.
        self.play(population.glass.animate.set_fill(opacity=0.29),
                  *(Transform(c, target) for c, target in zip(grey, grey_targets)),
                  LaggedStart(*(MoveAlongPath(c, ArcBetweenPoints(
            c.get_center(), c.get_center() + np.array(offset), angle=0.85))
            for c, offset in zip(blue, HOOK_OFFSETS)),
            lag_ratio=0.23), run_time=2.15)
        self.finish()


class S01Title(TitleCard):
    LESSON = "Inherited or Acquired?"
    TITLE = "Dominant Is Not Popular"

    def construct(self):
        population = bowl(x=0, size=1.07, people=True)
        for index, offset in zip(BLUE_CELLS, HOOK_OFFSETS):
            population.cards[index].shift(np.array(offset))
        question = label("?", 4.17, 2.62, GOLD, 88)
        tag = scope_tag(size=28)
        self.add(population, question, tag)
        target = bowl()
        self.play(FadeOut(question), FadeOut(population[3]),
                  Transform(population[:3], target[:3]), run_time=0.75)
        title = T(self.TITLE.replace(" Is ", " Is\n"), 46, TEXT, font=TITLE_FONT)
        lesson = T(self.LESSON, 28, GREY)
        rule = Line(LEFT * 0.65, RIGHT * 0.65, color=GOLD, stroke_width=4)
        words = VGroup(lesson, title, rule).arrange(DOWN, buff=0.28).move_to([RIGHT_X, 0.72, 0])
        self.play(FadeIn(lesson), FadeIn(title), GrowFromCenter(rule), run_time=0.55)
        self.wait(max(0.07, self.narration_s - self.elapsed()))


class S02Words(SpokenScene):
    def construct(self):
        population, individual = bowl(), pair(right=None)
        tag = scope_tag(size=28)
        self.add(population, tag)
        self.at("An allele is")
        allele = label("allele", LEFT_X, -2.24, BLUE)
        self.play(ShowPassingFlash(emphasis(population.cards[6], inset=0.09), time_width=0.70),
                  FadeIn(allele), run_time=1.55)
        self.at("In this simple model")
        parents = VGroup(*(person(x, 2.37, 1.35) for x in SLOTS_X))
        self.play(FadeOut(allele), FadeIn(individual.frame), FadeIn(individual.slots),
                  FadeIn(parents), run_time=1.35)
        self.at("receives one copy")
        paths = [Arrow([x, 2.17, 0], [x, 1.59, 0], buff=0.04, color=TEAL,
                       tip_length=0.16, stroke_width=4) for x in SLOTS_X]
        copies = [card(color, 0.9).move_to([x, 2.04, 0]) for x, color in zip(SLOTS_X, (BLUE, GREY))]
        self.play(LaggedStart(*(GrowArrow(p) for p in paths), lag_ratio=0.35), run_time=0.65)
        self.play(LaggedStart(*(c.animate.scale(1.30 / 0.9).move_to(s)
                                for c, s in zip(copies, individual.slots)), lag_ratio=0.55), run_time=1.22)
        self.at("The pair is")
        genotype = label("genotype", RIGHT_X, 0.11, BLUE)
        self.play(FadeOut(parents), *(FadeOut(p) for p in paths), FadeIn(individual.individual),
                  FadeIn(genotype), run_time=0.95)
        self.at("The trait that appears")
        self.play(Create(individual.window), run_time=0.75)
        self.at("its phenotype")
        phenotype = label("phenotype", RIGHT_X, -1.95)
        self.play(FadeIn(phenotype), run_time=0.65)
        self.at("Dominant and recessive")
        self.play(LaggedStart(*(s.animate.set_fill(color, 0.46)
                                for s, color in zip(individual.slots, (BLUE, GREY))),
                  lag_ratio=0.7), run_time=1.55)
        self.at("affects that phenotype")
        self.play(FadeOut(genotype), FadeOut(phenotype),
                  *(s.animate.set_fill(BG, 0.92) for s in individual.slots), run_time=0.32)
        self.play(GrowArrow(trait_route()), run_time=0.55)
        self.finish()


class S03ShowingRule(SpokenScene):
    def construct(self):
        population, individual = bowl(), pair(BLUE)
        word, route = shows(), trait_route()
        self.add(population, individual, route, scope_tag(size=28))
        self.at("A dominant allele")
        focus(self, individual.copies[0], time=1.02, inset=0.08)
        self.at("shows its trait")
        self.play(Transform(individual.window, phenotype_window(BLUE)), run_time=0.7)
        self.play(FadeIn(word), run_time=0.55)
        self.at("only one copy")
        focus(self, individual.copies[0], time=1.1, inset=0.08)
        self.at("A recessive allele")
        self.play(FadeOut(word), FadeOut(individual.copies[0]),
                  Transform(individual.window, phenotype_window()), run_time=0.52)
        second_grey = card(GREY, 1.30).move_to(individual.slots[0])
        self.play(FadeIn(second_grey, shift=LEFT * 0.42), run_time=0.85)
        self.at("when both copies")
        self.play(Transform(individual.window, phenotype_window(GREY)), run_time=0.72)
        self.play(FadeIn(word), run_time=0.46)
        self.at("So a dominant")
        self.play(FadeOut(word), FadeOut(second_grey),
                  Transform(individual.window, phenotype_window()), run_time=0.48)
        self.play(FadeIn(individual.copies[0], shift=LEFT * 0.43), run_time=0.85)
        self.at("can mask a recessive")
        self.play(Transform(individual.window, phenotype_window(BLUE)), run_time=0.83)
        self.play(FadeIn(word), run_time=0.55)
        self.at("Neither word means")
        strength = dial(ValueTracker(0.5), [LEFT_X, -2.80, 0], radius=0.90,
                        fmt="neutral", scale=1, color=GREY, size=28)
        gauge = strength[:3]
        backing = RoundedRectangle(width=3.10, height=1.53, corner_radius=0.15,
                                   color=GREY, stroke_width=2, fill_color=GREY,
                                   fill_opacity=0.39).move_to([LEFT_X, -2.40, 0])
        legend = label("strength", LEFT_X, -3.48, GREY, 28)
        self.play(FadeIn(backing), FadeIn(gauge), FadeIn(legend), run_time=0.73)
        cross = Cross(gauge, stroke_color=RED, stroke_width=6).scale(1.06)
        self.at("stronger healthier")
        self.play(Create(cross), run_time=1.1)
        self.finish()


class S04Predict(SpokenScene):
    def construct(self):
        population, individual, incoming = before_answer()
        self.add(population, individual, scope_tag(size=28))
        self.at("Only a few")
        self.play(population.glass.animate.set_fill(opacity=0.48),
                  LaggedStart(*(ShowPassingFlash(emphasis(population.cards[i], inset=0.08), time_width=0.65)
                                for i in BLUE_CELLS), lag_ratio=0.45), run_time=1.68)
        self.play(population.glass.animate.set_fill(opacity=0.29), run_time=1.02)
        self.at("When one blue card")
        moving = incoming.copy().move_to([-2.76, 2.29, 0])
        self.add(moving)
        path = CubicBezier(moving.get_center(), [-1.58, 2.16, 0], [-1.33, 1.20, 0], incoming.get_center())
        self.play(MoveAlongPath(moving, path), run_time=2.08)
        self.at("will its trait show")
        question, prompt_box = prediction_prompt()
        self.play(FadeIn(question), run_time=0.72)
        self.at("before the window changes", lead=0)
        focus(self, individual.window, color=GOLD, time=1.77, inset=0.08)
        self.play(FadeIn(prompt_box), run_time=0.48)
        self.finish()


class S05Pause(PredictPause):
    QUESTION = QUESTION
    SECONDS = 4.5
    CARD = QUESTION_STYLE

    def construct(self):
        question, prompt_box = prediction_prompt()
        self.add(*before_answer(), scope_tag(size=28), prompt_box, question)
        self.wait(self.SECONDS)


class S06Reveal(SpokenScene):
    def construct(self):
        population, individual, incoming = before_answer()
        question, prompt_box = prediction_prompt()
        self.add(population, individual, incoming, scope_tag(size=28), prompt_box, question)
        self.at("The blue card enters")
        self.play(incoming.animate(run_time=1.10).move_to(individual.slots[0]),
                  FadeOut(question, run_time=0.25), FadeOut(prompt_box, run_time=0.25))
        self.at("and the trait shows")
        self.play(Transform(individual.window, phenotype_window(BLUE)), run_time=0.80)
        self.play(FadeIn(shows()), run_time=0.55)
        common, showing, _, show_value = displays(showing=0)
        self.at("That is dominance")
        self.play(GrowArrow(trait_route()), FadeIn(showing), run_time=0.8)
        self.play(show_value.animate.set_value(1), run_time=1.45)
        self.at("Yet the population bowl")
        self.play(FadeIn(common), run_time=0.65)
        self.at("very few blue cards")
        self.play(population.glass.animate.set_fill(opacity=0.49),
                  LaggedStart(*(ShowPassingFlash(emphasis(population.cards[i], inset=0.08), time_width=0.6)
                                for i in BLUE_CELLS), lag_ratio=0.44), run_time=1.65)
        self.at("The rule for showing")
        self.play(population.glass.animate.set_fill(opacity=0.29), run_time=0.58)
        highlight_fill(self, individual.window, 1, time=1.62)
        self.at("did not make the allele common")
        highlight_fill(self, population.glass, 0.48, time=1.94)
        self.finish()


class S07IndependentControls(SpokenScene):
    def construct(self):
        population, individual = bowl(), pair(BLUE, result=BLUE)
        word, route = shows(), trait_route()
        common, showing, group_value, show_value = displays()
        self.add(population, individual, word, route, common, showing, scope_tag(size=28))
        arrivals = VGroup(*(card(BLUE, 0.79).move_to([LEFT_X + x, 3.28, 0])
                             for x, _ in LANDINGS))
        landings = [[LEFT_X + x, 0.69 + y, 0] for x, y in LANDINGS]

        self.at("Now move more blue")
        # A pair of cards reaches the bowl on each beat, then enters the sample.
        for start in range(0, len(arrivals), 2):
            self.play(*(FadeIn(arrivals[i]) for i in (start, start + 1)), run_time=0.20)
            self.play(*(arrivals[i].animate.move_to(landings[i]) for i in (start, start + 1)),
                      group_value.animate.set_value(blue_fraction(start + 2)), run_time=0.96)
        self.at("The group display rises")
        focus(self, common[0], time=1.44, inset=0.08)
        self.at("Move them out")
        for start in (4, 2, 0):
            exiting = [arrivals[i] for i in (start, start + 1)]
            self.play(*(c.animate.set_y(3.26) for c in exiting),
                      group_value.animate.set_value(blue_fraction(start)), run_time=0.63)
            self.play(*(FadeOut(c) for c in exiting), run_time=0.18)
        self.at("The individual display")
        original = individual.copies[0]
        alternate = card(GREY, 1.30).move_to(original)
        self.play(FadeOut(original), FadeOut(word), Transform(individual.window, phenotype_window()),
                  show_value.animate.set_value(0), run_time=0.50)
        self.play(FadeIn(alternate), Transform(individual.window, phenotype_window(GREY)), run_time=0.95)
        self.at("follows the allele pair")
        self.play(FadeOut(alternate), Transform(individual.window, phenotype_window()), run_time=0.35)
        self.play(FadeIn(original), run_time=0.30)
        self.play(FadeIn(word), Transform(individual.window, phenotype_window(BLUE)),
                  show_value.animate.set_value(1), run_time=0.94)
        self.at("Frequency belongs")
        highlight_fill(self, population.glass, 0.49, time=1.75)
        self.at("Dominance belongs")
        self.play(LaggedStart(*(s.animate.set_fill(color, 0.46)
                                for s, color in zip(individual.slots, (BLUE, GREY))),
                  lag_ratio=0.58, rate_func=there_and_back), run_time=2.2)
        self.finish()


def case_map():
    axes = Plot(box=(-4.55, 4.97, -2.39, 2.69), xr=(0, 1), yr=(0, 1),
                xlabel="showing rule", ylabel="group frequency", label_size=32)
    categories = VGroup(label("common", -5.57, 1.42, GREY, 28),
                        label("rare", -5.57, -1.12, GREY, 28),
                        label("recessive", -2.17, -2.76, GREY, 28),
                        label("dominant", 2.59, -2.76, BLUE, 28))
    axes.xlabel.set_y(-3.28)
    quadrants = VGroup(*(RoundedRectangle(width=4.53, height=2.33, corner_radius=0.17,
                                          stroke_color=GREY, stroke_width=2,
                                          fill_color=GREY, fill_opacity=0.25).move_to(axes.pt(x, y))
                         for x in (0.25, 0.75) for y in (0.25, 0.75)))
    return axes, categories, quadrants


def pair_key(left=BLUE):
    return VGroup(card(left), card(GREY)).arrange(RIGHT, buff=0.22)


def sample_key(common=False, color=BLUE):
    shape = RoundedRectangle(width=1.31, height=0.82, corner_radius=0.19, color=GREY,
                             fill_color=GREY, fill_opacity=0.30, stroke_width=3)
    dots = VGroup(*(Square(side_length=0.15, stroke_color=color, stroke_width=1.4,
                           stroke_opacity=1 if i < (6 if common else 2) else 0.55,
                           fill_color=color, fill_opacity=float(i < (6 if common else 2)))
                    for i in range(8))).arrange_in_grid(2, 4, buff=0.11)
    return VGroup(shape, dots.move_to(shape))


class S08FourCases(SpokenScene):
    def construct(self):
        axes, categories, cells = case_map()
        common, showing, _, _ = displays()
        population, individual, word, route = bowl(), pair(BLUE, result=BLUE), shows(), trait_route()
        self.add(population, individual, word, route, common, showing, scope_tag(size=28))
        self.at("A dominant trait")
        self.play(FadeOut(word), FadeOut(common[2]), FadeOut(showing[2]), run_time=0.13)
        self.play(FadeOut(population), FadeOut(individual), FadeOut(route), FadeOut(common[:2]),
                  FadeOut(showing[:2]), Create(axes.axes), FadeIn(cells), run_time=0.20)
        genotype = pair_key().move_to(cells[3])
        sample = sample_key(True).move_to([5.83, 1.42, 0])
        self.play(FadeIn(axes.xlabel), FadeIn(axes.ylabel), FadeIn(categories),
                  FadeIn(genotype), FadeIn(sample),
                  cells[3].animate.set_fill(BLUE, 0.52), run_time=0.20)
        self.at("rare", lead=0)
        self.play(Transform(sample, sample_key().move_to([5.83, -1.12, 0])),
                  genotype.animate.move_to(cells[2]),
                  cells[3].animate.set_fill(GREY, 0.25),
                  cells[2].animate.set_fill(BLUE, 0.52), run_time=0.46)
        self.at("A recessive trait")
        self.play(Transform(genotype, pair_key(GREY).move_to(cells[1])),
                  Transform(sample, sample_key(True, GREY).move_to([5.83, 1.42, 0])),
                  cells[2].animate.set_fill(GREY, 0.25),
                  cells[1].animate.set_fill(GREY, 0.52), run_time=0.54)
        self.at("or rare these", lead=0)
        self.play(Transform(sample, sample_key(color=GREY).move_to([5.83, -1.12, 0])),
                  genotype.animate.move_to(cells[0]),
                  cells[1].animate.set_fill(GREY, 0.25),
                  cells[0].animate.set_fill(GREY, 0.52), run_time=0.46)
        self.at("These are separate")
        self.play(cells[0].animate.set_fill(GREY, 0.25),
                  axes.axes.animate.set_stroke(TEAL, width=4), run_time=1.35)
        self.at("One asks what")
        self.play(Transform(genotype, pair_key().move_to(cells[2])),
                  Transform(sample, sample_key().move_to([5.83, -1.12, 0])),
                  cells[2].animate.set_fill(BLUE, 0.52), run_time=2.05)
        self.at("The other asks")
        self.play(Transform(sample, sample_key(True).move_to([5.83, 1.42, 0])),
                  genotype.animate.move_to(cells[3]),
                  cells[2].animate.set_fill(GREY, 0.25),
                  cells[3].animate.set_fill(BLUE, 0.52), run_time=2.45)
        self.finish()


def trophy():
    bowl_shape = Arc(radius=0.35, start_angle=PI, angle=PI, color=GOLD, stroke_width=6)
    lip = Line(LEFT * 0.35, RIGHT * 0.35, color=GOLD, stroke_width=4)
    stem = Line(DOWN * 0.35, DOWN * 0.58, color=GOLD, stroke_width=6)
    foot = Line([-0.24, -0.58, 0], [0.24, -0.58, 0], color=GOLD, stroke_width=6)
    handles = VGroup(*(Arc(radius=0.15, start_angle=a, angle=PI, color=GOLD,
                           stroke_width=4).move_to([x, -0.11, 0])
                       for a, x in ((PI / 2, -0.41), (-PI / 2, 0.41))))
    return VGroup(bowl_shape, lip, stem, foot, handles)


class S09NarrowMeaning(SpokenScene):
    def construct(self):
        population, individual = bowl(), pair(BLUE, result=BLUE)
        common, showing, _, _ = displays()
        self.add(population, individual, shows(), common, showing, scope_tag(size=28))
        dominant = label("dominant", RIGHT_X, 3.35, BLUE, 35)
        barrier = Line([-1.44, -0.58, 0], [-1.44, 2.10, 0], color=RED, stroke_width=10)
        cup = trophy().scale(1.9).move_to([-4.75, 0.87, 0])
        self.at("The everyday word")
        self.play(FadeIn(dominant), FadeOut(population), run_time=0.82)
        self.play(DrawBorderThenFill(cup), run_time=0.62)
        self.at("can sound like")
        winning = label("winning", -3.80, -0.84, GOLD, 36)
        self.play(FadeIn(winning), Create(barrier), cup.animate.shift(RIGHT * 2.13), run_time=1.6)
        self.at("Genetics uses it")
        self.play(FadeOut(cup), FadeOut(winning), FadeOut(barrier), run_time=0.51)
        self.play(FadeIn(population), run_time=1.0)
        self.at("It describes how")
        self.play(GrowArrow(trait_route()), run_time=1.15)
        highlight_fill(self, individual.window, 1, time=0.97)
        self.at("different alleles share")
        self.play(*(s.animate.set_fill(color, 0.45)
                    for s, color in zip(individual.slots, (BLUE, GREY))), run_time=1.18)
        self.play(*(s.animate.set_fill(BG, 0.92) for s in individual.slots), run_time=0.50)
        self.at("It does not say")
        stop = Line([-0.96, -1.94, 0], [-0.96, -1.28, 0], color=RED, stroke_width=9)
        arrow = Polygon([-0.84, -1.79, 0], [-0.62, -1.98, 0], [-0.62, -1.90, 0],
                        [0.90, -1.90, 0], [0.90, -1.68, 0], [-0.62, -1.68, 0],
                        [-0.62, -1.60, 0], stroke_width=0, fill_color=BLUE, fill_opacity=1)
        spread = label("spread", 0, -2.37, BLUE, 33)
        replace = label("replace", 0, -2.37, BLUE, 33)
        self.play(Create(stop), run_time=0.62)
        self.at("allele will spread")
        self.play(GrowFromEdge(arrow, RIGHT), FadeIn(spread), run_time=0.85)
        self.at("replace another")
        self.play(FadeOut(arrow), FadeOut(spread), run_time=0.31)
        replacement_arrow = arrow.copy()
        self.play(FadeIn(replace), GrowFromEdge(replacement_arrow, RIGHT), run_time=0.65)
        self.at("or become common")
        self.play(FadeOut(replacement_arrow), FadeOut(stop), FadeOut(replace), run_time=0.56)
        highlight_fill(self, population.glass, 0.50, time=1.44)
        self.at("Population frequency is")
        self.play(population.glass.animate.set_fill(opacity=0.49), run_time=1.42)
        self.play(population.glass.animate.set_fill(opacity=0.29), run_time=1.08)
        self.finish()


def offspring_shapes():
    parent_places = ((2.03, 1.53), (4.77, 1.53))
    parents = VGroup(*(pair_key(c).scale(0.88).move_to([x, y, 0])
                      for (x, y), c in zip(parent_places, (BLUE, GREY))))
    slots = VGroup(*(RoundedRectangle(width=0.82, height=0.87, corner_radius=0.11,
                                      stroke_color=GREY, stroke_width=3, fill_color=BG,
                                      fill_opacity=0.77).move_to([x, -0.20, 0])
                     for x in (2.90, 3.90)))
    routes = VGroup(*(Arrow([x, 1.11, 0], s.get_top() + UP * 0.06, buff=0,
                            tip_length=0.17, color=TEAL, stroke_width=4)
                      for (x, _), s in zip(parent_places, slots)))
    window = RoundedRectangle(width=2.35, height=0.66, corner_radius=0.12,
                              stroke_color=GREY, stroke_width=3, fill_color=BG,
                              fill_opacity=0.75).move_to([RIGHT_X, -1.24, 0])
    return parents, routes, slots, window


class S10EvidenceBridge(SpokenScene):
    def construct(self):
        panels = TwoPanel("group frequency", "showing rule", colors=(BLUE, TEAL),
                          top=3.0, bottom=-2.43)
        for frame in (panels.left_frame, panels.right_frame):
            frame.set_fill(GREY, opacity=0.24)
        common, showing, _, _ = displays()
        self.add(panels, scope_tag(size=28))
        for display in (common, showing):
            track, fill = display[:2].copy().clear_updaters().shift(UP * 0.20)
            self.add(track, fill)
        common_title = label("count in this group", LEFT_X, 1.81, TEXT, 30)
        tally = RoundedRectangle(width=4.60, height=1.95, corner_radius=0.20, stroke_color=GREY,
                                 stroke_width=3, fill_color=BG, fill_opacity=0.48).move_to([LEFT_X, -0.57, 0])
        people = VGroup(*(person(x, 0.99, 1.22) for x in (-5.21, -4.01, -2.79, -1.59)))
        self.at("To test a claim")
        self.play(FadeIn(people), FadeIn(common_title), run_time=1.5)
        self.at("count traits or alleles")
        self.play(Create(tally), run_time=0.52)
        self.play(LaggedStart(*(m.animate.move_to([x, -0.50, 0])
                                for m, x in zip(people, (-4.96, -3.92, -2.88, -1.84))),
                  lag_ratio=0.37), run_time=2.35)
        parents, paths, slots, window = offspring_shapes()
        self.at("To test dominance")
        self.play(FadeIn(parents), FadeIn(slots), FadeIn(window), run_time=1.03)
        self.at("follow which phenotypes")
        self.play(LaggedStart(*(GrowArrow(path) for path in paths), lag_ratio=0.5), run_time=0.60)
        copies = VGroup(*(card(color, 0.87).move_to(path.get_start())
                           for color, path in zip((BLUE, GREY), paths)))
        self.play(LaggedStart(*(c.animate.move_to(slot) for c, slot in zip(copies, slots)),
                  lag_ratio=0.48), run_time=0.90)
        self.at("in offspring")
        self.play(window.animate.set_fill(BLUE, 0.65).set_stroke(BLUE), run_time=0.58)
        self.at("as Mendel did with peas")
        peas = VGroup(*(Dot(radius=0.105, color=GREEN) for _ in range(3))).arrange(RIGHT, buff=0.12)
        pod = Ellipse(width=1.15, height=0.43, color=GREEN, stroke_width=3)
        pea_icon = VGroup(pod, peas.move_to(pod)).move_to([5.52, -1.28, 0])
        self.play(Create(pod), LaggedStart(*(FadeIn(p) for p in peas), lag_ratio=0.4), run_time=1.02)
        self.at("One kind of evidence")
        divider = Line([0, -2.47, 0], [0, 2.96, 0], color=TEAL, stroke_width=4)
        self.play(Create(divider), run_time=1.78)
        self.at("Later courses add")
        beyond = label("more patterns later", 1.55, -3.04, TEXT, 28)
        self.play(FadeIn(beyond), run_time=0.65)
        self.at("inheritance patterns beyond")
        self.play(GrowArrow(Arrow(beyond.get_right() + RIGHT * 0.14,
                                  beyond.get_right() + RIGHT * 0.98, buff=0, color=TEAL,
                                  tip_length=0.19, stroke_width=4)), run_time=1.65)
        self.finish()


class S11Close(SpokenScene):
    def construct(self):
        population, individual = bowl(), pair(BLUE, result=BLUE)
        common, showing, _, _ = displays()
        group_label = label("whole group", LEFT_X, 3.37, TEXT, 33)
        dom = label("dominant", RIGHT_X, 3.37, BLUE, 36)
        freq = label("common", LEFT_X, 3.37, BLUE, 36)
        word = shows()
        tag = scope_tag(size=28)
        self.add(population, individual, word, common, showing, tag)
        self.at("So when you hear")
        self.play(FadeIn(dom), run_time=0.72)
        self.at("look inside one genotype")
        self.play(population.animate.set_opacity(0.27),
                  ScaleInPlace(individual.slots, 1.08),
                  ScaleInPlace(VGroup(*individual.copies), 1.08), run_time=1.45)
        self.at("Ask whether a copy")
        self.play(GrowArrow(trait_route()), run_time=0.66)
        highlight_fill(self, individual.window, 1, time=1.55)
        self.at("When you hear common")
        # Restore the original bowl strokes and fills before drawing attention to the group.
        self.play(Transform(population, bowl()),
                  ScaleInPlace(individual.slots, 1 / 1.08),
                  ScaleInPlace(VGroup(*individual.copies), 1 / 1.08),
                  FadeIn(group_label), run_time=1.32)
        self.at("look across the whole")
        self.play(population.glass.animate.set_fill(opacity=0.49), run_time=1.35)
        self.at("Ask how often")
        self.play(population.glass.animate.set_fill(opacity=0.29),
                  ShowPassingFlash(emphasis(common[0], inset=0.08), time_width=0.65), run_time=1.4)
        self.play(swap(group_label, freq, run_time=0.81))
        self.at("Never use one answer")
        divider = Line([0, -3.13, 0], [0, 3.22, 0], color=TEAL, stroke_width=5)
        self.play(Create(divider), FadeOut(common[2]), FadeOut(showing[2]),
                  FadeOut(word), FadeOut(tag), run_time=1.65)
        self.finish()


class S12End(EndCard):
    LINE = "Dominant tells how an allele shows, not how common it is."
