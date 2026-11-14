"""Why the Wolves Never Finish the Moose — a grade 7 biology explainer.

COLOR MAP
  MOOSE_BROWN = moose / prey
  WOLF_GREY   = wolves / predators
  TREE_GREEN  = young trees / plant food
  ORANGE      = a low moose-per-wolf counter
  LAKE_BLUE   = lake water

The recurring model island, animals, and counter are rebuilt by the builder
functions below so their scale and landmarks do not drift between scenes.
"""
from bp_parts import *  # noqa: F401,F403

MOOSE_BROWN = "#B8783F"
WOLF_GREY = "#AAB1BA"
TREE_GREEN = "#58B66B"
ORANGE = "#F59E42"
LAKE_BLUE = "#347FA3"
SNOW = "#EAF2F6"


def fir(height=1.15):
    """A simple young fir: the lesson's plant picture, not a molecule."""
    trunk = Rectangle(width=0.12, height=0.36, stroke_width=0,
                      fill_color=MOOSE_BROWN, fill_opacity=1).shift(DOWN * 0.38)
    crown = VGroup(*[
        Triangle(stroke_color=TREE_GREEN, stroke_width=2, fill_color=TREE_GREEN,
                 fill_opacity=0.75).scale(s).shift(UP * y)
        for s, y in ((0.48, -0.12), (0.38, 0.16), (0.28, 0.42))
    ])
    return VGroup(trunk, crown).set_height(height)


def moose(height=0.85, calf=False):
    """Flat brown moose icon with a clear body, head, legs, and antlers."""
    body = Ellipse(width=1.25, height=0.55, stroke_color=MOOSE_BROWN, stroke_width=3,
                   fill_color=MOOSE_BROWN, fill_opacity=0.65)
    neck = Line([0.48, 0.15, 0], [0.72, 0.55, 0], color=MOOSE_BROWN, stroke_width=10)
    head = Ellipse(width=0.48, height=0.3, stroke_color=MOOSE_BROWN, stroke_width=3,
                   fill_color=MOOSE_BROWN, fill_opacity=0.8).move_to([0.82, 0.57, 0])
    legs = VGroup(*[Line([x, -0.18, 0], [x - 0.03, -0.58, 0], color=MOOSE_BROWN,
                               stroke_width=5) for x in (-0.38, 0.35)])
    antlers = VGroup(
        Line([0.78, 0.72, 0], [0.65, 0.94, 0], color=MOOSE_BROWN, stroke_width=3),
        Line([0.65, 0.9, 0], [0.52, 1.02, 0], color=MOOSE_BROWN, stroke_width=3),
        Line([0.69, 0.88, 0], [0.8, 1.03, 0], color=MOOSE_BROWN, stroke_width=3),
    )
    g = VGroup(body, neck, head, legs, antlers)
    g.set_height(height * (0.72 if calf else 1.0))
    return g


def wolf(height=0.62, pup=False):
    """Flat grey wolf icon, facing right."""
    body = Ellipse(width=1.15, height=0.43, stroke_color=WOLF_GREY, stroke_width=3,
                   fill_color=WOLF_GREY, fill_opacity=0.7)
    head = Polygon([0.43, 0.12, 0], [0.9, 0.35, 0], [0.82, -0.05, 0],
                   stroke_color=WOLF_GREY, stroke_width=3, fill_color=WOLF_GREY,
                   fill_opacity=0.8)
    ear = Triangle(stroke_color=WOLF_GREY, stroke_width=2, fill_color=WOLF_GREY,
                   fill_opacity=0.8).scale(0.13).move_to([0.62, 0.39, 0])
    legs = VGroup(*[Line([x, -0.12, 0], [x, -0.48, 0], color=WOLF_GREY,
                               stroke_width=5) for x in (-0.35, 0.35)])
    tail = Line([-0.5, 0.08, 0], [-0.92, 0.38, 0], color=WOLF_GREY, stroke_width=6)
    g = VGroup(body, head, ear, legs, tail)
    g.set_height(height * (0.68 if pup else 1.0))
    return g


MOOSE_POS = [(-3.8, 1.3), (-2.5, 1.5), (-1.0, 1.25), (0.5, 1.45),
             (-3.2, 0.15), (-1.8, 0.25), (-0.25, 0.1), (1.25, 0.3),
             (-3.7, -1.1), (-2.25, -1.05), (-0.75, -1.2), (0.75, -1.0)]
WOLF_POS = [(-3.5, 0.7), (-2.0, 0.85), (-0.5, 0.75), (0.9, 0.8),
            (-3.0, -0.55), (-1.4, -0.5), (0.25, -0.55), (1.1, -1.3)]
TREE_POS = [(-4.45, 0.3), (-4.25, -1.45), (1.85, 0.35), (1.65, -1.45)]


def model_island(moose_n=8, wolf_n=3, trees_n=4, animal_scale=1.0):
    """The single carried island world used throughout the film."""
    water = Ellipse(width=11.8, height=5.75, stroke_color=LAKE_BLUE, stroke_width=5,
                    fill_color=LAKE_BLUE, fill_opacity=0.14).move_to([0, -0.05, 0])
    shore = Ellipse(width=8.0, height=4.75, stroke_color=SNOW, stroke_width=4,
                    fill_color=SNOW, fill_opacity=0.12).move_to([-1.2, -0.05, 0])
    ripples = VGroup(*[
        Arc(radius=0.7, start_angle=0, angle=PI, color=LAKE_BLUE, stroke_width=3)
        .stretch(0.24, 1).move_to([x, y, 0])
        for x, y in ((3.8, 1.0), (4.2, -0.25), (3.55, -1.45))
    ])
    trees = VGroup(*[fir(0.85).move_to([x, y, 0]) for x, y in TREE_POS[:trees_n]])
    ms = VGroup(*[moose(0.72 * animal_scale).move_to([x, y, 0]) for x, y in MOOSE_POS[:moose_n]])
    ws = VGroup(*[wolf(0.55 * animal_scale).move_to([x, y, 0]) for x, y in WOLF_POS[:wolf_n]])
    g = VGroup(water, shore, ripples, trees, ms, ws)
    g.water, g.shore, g.ripples, g.trees, g.moose, g.wolves = water, shore, ripples, trees, ms, ws
    # Labels intentionally sit over this pale background world; foreground labels
    # and diagrams are still checked normally.
    g.layout_ok = True
    for part in g.family_members_with_points():
        part.layout_ok = True
    return g


def model_tag():
    return T("model (schematic)", 24, GREY).move_to([-5.35, -3.45, 0])


def food_counter(value=100, color=TEXT, at=(4.0, 2.65, 0)):
    tracker = ValueTracker(value)
    panel = Readout([("moose per wolf", lambda: tracker.get_value(), "{:3.0f}", color)],
                    at=at, size=26, widest=[100], color=color)
    panel.tracker = tracker
    return panel


def add_idle(world):
    """Breathing animals and moving lake marks keep the living model alive."""
    for i, animal in enumerate([*world.moose, *world.wolves]):
        bob(animal, amp=0.035, speed=1.45 + 0.08 * (i % 4), seed=i)
    bob(world.ripples, amp=0.055, speed=1.1, seed=2)
    return world


def low_world(with_question=False):
    world = add_idle(model_island(moose_n=5, wolf_n=7))
    counter_box = food_counter(10, ORANGE)
    tag = model_tag()
    g = VGroup(world, counter_box, tag)
    if with_question:
        g.add(question_card("Only 10 moose for each wolf. What happens to the wolves next?",
                            y=-3.05, max_w=10.3, size=28))
    return g


class S00Title(TitleCard):
    LESSON = "Predators and prey"
    TITLE = "Why the Wolves Never Finish the Moose"


class S01Question(SpokenScene):
    def construct(self):
        q = fit_text("If wolves eat moose, why don't they eat every last moose?",
                     max_w=11.5, size=44, color=TEXT, font=TITLE_FONT).move_to([0, 2.75, 0])
        w, m = wolf(1.25).move_to([-3.5, -0.6, 0]), moose(1.65).move_to([3.2, -0.55, 0])
        mark = T("?", 96, GOLD, font=TITLE_FONT).move_to([0, 0.1, 0])
        self.at("If wolves eat moose")
        self.play(AddTextLetterByLetter(q), FadeIn(w, shift=RIGHT), FadeIn(m, shift=LEFT),
                  run_time=3.2)
        self.play(FadeIn(mark, scale=0.5), w.animate.shift(RIGHT * 0.45), run_time=0.55)
        # A recognisable but intentionally simple Lake Superior outline.
        lake = Polygon([-5.2, 0.7, 0], [-3.7, 1.8, 0], [-1.2, 1.45, 0], [0.3, 0.7, 0],
                       [2.8, 0.8, 0], [4.7, 0.1, 0], [3.4, -1.4, 0], [0.2, -1.8, 0],
                       [-2.7, -1.25, 0], [-5.2, 0.7, 0], stroke_color=LAKE_BLUE,
                       stroke_width=5, fill_color=LAKE_BLUE, fill_opacity=0.13)
        isle = Ellipse(width=1.4, height=0.32, color=GOLD, stroke_width=5).rotate(-0.18).move_to([1.5, -0.35, 0])
        lab = T("Isle Royale", 30, GOLD).next_to(isle, DOWN, buff=0.25)
        self.at("On one real island")
        self.play(FadeOut(VGroup(q, w, m, mark)), FadeIn(lake), run_time=0.55)
        self.play(Create(isle), FadeIn(lab), run_time=0.8)
        self.at("they never have")
        self.play(Indicate(isle, color=GOLD, scale_factor=1.2), run_time=0.7)
        world = model_island(moose_n=7, wolf_n=3)
        self.at("starting with a model island")
        self.play(FadeOut(VGroup(lake, isle, lab)), FadeIn(world), FadeIn(model_tag()), run_time=1.0)
        add_idle(world)
        self.finish()


class S02Population(SpokenScene):
    def construct(self):
        world = add_idle(model_island(moose_n=8, wolf_n=3))
        head = T("population", 48, TEXT, font=TITLE_FONT).move_to([0, 3.25, 0])
        definition = T("one species, one place", 30, TEXT).next_to(head, DOWN, buff=0.14)
        self.at("First two words")
        self.play(FadeIn(world), FadeIn(model_tag()), run_time=0.7)
        self.at("A population is")
        self.play(Write(head), FadeIn(definition, shift=UP * 0.1), run_time=1.1)
        mr = Ellipse(width=6.6, height=3.8, color=MOOSE_BROWN, stroke_width=5).move_to([-1.25, 0, 0])
        mr.layout_ok = True  # deliberate population enclosure
        ml = chip("population: moose", MOOSE_BROWN, size=28).move_to([-2.4, -2.65, 0])
        self.at("All the moose")
        self.play(Create(mr), FadeIn(ml), Indicate(world.moose, color=MOOSE_BROWN), run_time=1.0)
        wr = Ellipse(width=5.8, height=3.35, color=WOLF_GREY, stroke_width=5).move_to([-1.2, 0.05, 0])
        wr.layout_ok = True  # deliberate population enclosure
        wl = chip("population: wolves", WOLF_GREY, size=28).move_to([2.35, -2.65, 0])
        self.at("All the wolves")
        self.play(Transform(mr, wr), FadeOut(ml), FadeIn(wl), Indicate(world.wolves, color=WOLF_GREY), run_time=1.0)
        self.finish()


class S03Predator(SpokenScene):
    def construct(self):
        prey = moose(2.0).move_to([3.4, 0, 0])
        hunter = wolf(1.45).move_to([-3.7, 0, 0])
        self.at("A predator is")
        self.play(FadeIn(hunter, shift=RIGHT * 0.4), run_time=0.7)
        pl = chip("predator", WOLF_GREY, size=34).next_to(hunter, UP, buff=0.4)
        pd = T("catches and eats other animals", 28, TEXT).next_to(pl, UP, buff=0.18)
        self.at("catches and eats")
        self.play(hunter.animate.shift(RIGHT * 0.7), FadeIn(pl), FadeIn(pd), run_time=0.8)
        self.at("The animal it eats")
        self.play(FadeIn(prey, shift=LEFT * 0.3), run_time=0.6)
        ql = chip("prey", MOOSE_BROWN, size=34).next_to(prey, UP, buff=0.35)
        qd = T("the animal that is eaten", 28, TEXT).next_to(ql, UP, buff=0.18)
        self.at("is its prey")
        self.play(FadeIn(ql), FadeIn(qd), run_time=0.65)
        pack = VGroup(hunter, wolf(1.25).move_to([-4.3, -1.4, 0]),
                      wolf(1.18).move_to([-3.0, -1.55, 0]))
        self.add(pack[1], pack[2])
        self.at("wolves are the predators")
        self.play(pack.animate.shift(RIGHT * 1.0), Indicate(pl, color=WOLF_GREY), run_time=1.0)
        self.at("moose are their prey")
        self.play(prey.animate.shift(LEFT * 0.35), Indicate(ql, color=MOOSE_BROWN), run_time=0.8)
        self.finish()


class S04Arrow(SpokenScene):
    def construct(self):
        tree = fir(2.4).move_to([-4.5, 0.25, 0])
        prey = moose(1.7).move_to([0, 0.1, 0])
        hunter = wolf(1.25).move_to([4.5, 0.1, 0])
        self.at("Moose eat young trees")
        self.play(FadeIn(tree, shift=UP * 0.3), run_time=0.65)
        self.play(FadeIn(prey, shift=LEFT * 0.3), run_time=0.55)
        a1 = Arrow(tree.get_right(), prey.get_left(), buff=0.25, color=TREE_GREEN,
                   stroke_width=8, tip_length=0.28)
        self.play(GrowArrow(a1), prey.animate.shift(LEFT * 0.2), run_time=0.7)
        self.at("Wolves eat moose")
        self.play(FadeIn(hunter, shift=LEFT * 0.3), run_time=0.55)
        a2 = Arrow(prey.get_right(), hunter.get_left(), buff=0.25, color=MOOSE_BROWN,
                   stroke_width=8, tip_length=0.28)
        self.play(GrowArrow(a2), hunter.animate.shift(LEFT * 0.2), run_time=0.7)
        note = T("arrow: from the food to the eater", 30, TEXT).move_to([0, -2.55, 0])
        self.at("We draw arrows")
        self.play(Indicate(VGroup(a1, a2), color=GOLD), FadeIn(note, shift=UP * 0.1), run_time=0.85)
        self.at("Each arrow points")
        self.play(ShowPassingFlash(a1.copy().set_stroke(width=14), run_time=0.8),
                  ShowPassingFlash(a2.copy().set_stroke(width=14), run_time=0.8))
        self.finish()


class S05Counter(SpokenScene):
    def construct(self):
        world = add_idle(model_island(moose_n=10, wolf_n=3))
        c = food_counter(100)
        self.at("Now we need one number")
        self.play(FadeIn(world), FadeIn(model_tag()), run_time=0.65)
        self.play(FadeIn(c, shift=DOWN * 0.15), run_time=0.65)
        formula = M("moose ÷ wolves", 34, TEXT).move_to([3.9, 1.65, 0])
        self.at("Count the moose")
        self.play(FadeIn(formula), Indicate(world.moose, color=MOOSE_BROWN), run_time=0.8)
        arithmetic = M("1,000 ÷ 10 = 100", 38, TEXT).move_to([3.65, 0.7, 0])
        note = fit_text("one island-wide clue, not each wolf's own share", max_w=5.2,
                        size=28, color=GREY).move_to([3.35, -0.2, 0])
        self.at("counter in the corner")
        self.play(Transform(formula, arithmetic), Indicate(c, color=GOLD), run_time=0.8)
        self.play(FadeIn(note, shift=UP * 0.1), run_time=0.45)
        clue = T("rough clue to finding food", 28, GOLD).move_to([3.35, -1.35, 0])
        self.at("rough clue")
        self.play(FadeIn(clue), world.wolves.animate.shift(RIGHT * 0.35), run_time=0.8)
        self.finish()


class S06Start(SpokenScene):
    def construct(self):
        world = add_idle(model_island(moose_n=12, wolf_n=2))
        c = food_counter(100)
        self.add(world, c, model_tag())
        ml = chip("1,000 moose", MOOSE_BROWN, size=30).move_to([-3.4, 2.55, 0])
        wl = chip("10 wolves", WOLF_GREY, size=30).move_to([-0.45, 2.55, 0])
        self.at("many moose")
        self.play(FadeIn(ml), Indicate(world.moose, color=MOOSE_BROWN), run_time=0.7)
        self.at("only a few wolves")
        self.play(FadeIn(wl), Indicate(world.wolves, color=WOLF_GREY), run_time=0.7)
        high = T("HIGH", 30, GOLD, weight=BOLD).next_to(c, DOWN, buff=0.18)
        self.at("counter is high")
        self.play(FadeIn(high), Indicate(c, color=GOLD), run_time=0.65)
        path = ArcBetweenPoints(world.wolves[0].get_center(), [-0.2, -0.8, 0], angle=-0.45)
        self.at("hunting is easy")
        self.play(MoveAlongPath(world.wolves[0], path), run_time=1.0)
        belly = T("eats well", 30, WOLF_GREY).move_to([1.6, -1.8, 0])
        self.at("wolves eat well")
        self.play(FadeIn(belly), world.wolves[0].animate.scale(1.12), run_time=0.7)
        self.finish()


class S07Grow(SpokenScene):
    def construct(self):
        world = add_idle(model_island(moose_n=12, wolf_n=2))
        c = food_counter(100)
        self.add(world, c, model_tag())
        den = Arc(radius=0.8, start_angle=0, angle=PI, color=GREY, stroke_width=6).move_to([-2.8, -1.75, 0])
        pups = VGroup(*[wolf(0.55, pup=True).move_to([-3.2 + i * 0.55, -1.5, 0]) for i in range(3)])
        self.at("plenty of food")
        self.play(Indicate(c, color=GOLD), FadeIn(den), run_time=0.6)
        self.at("more wolf pups survive")
        self.play(LaggedStart(*[FadeIn(p, shift=UP * 0.15) for p in pups], lag_ratio=0.2), run_time=0.8)
        self.at("grow up")
        self.play(pups.animate.scale(1.55).shift(UP * 0.25), run_time=0.65)
        year = ValueTracker(1)
        year_label = counter("year {:.0f}", year, at=[0, 3.25, 0], size=34, color=TEXT)
        self.add(year_label)
        more = VGroup(*[wolf(0.52).move_to([x, y, 0]) for x, y in WOLF_POS[2:6]])
        self.at("Year by year")
        self.play(year.animate.set_value(3), FadeIn(more, lag_ratio=0.15), run_time=1.8, rate_func=linear)
        wolf_label = chip("30 wolves", WOLF_GREY, size=30).move_to([-0.8, 2.5, 0])
        self.at("more wolves")
        self.play(FadeIn(wolf_label), Indicate(VGroup(world.wolves, pups, more), color=WOLF_GREY), run_time=0.65)
        self.at("catch more moose")
        self.play(LaggedStart(*[FadeOut(x, shift=DOWN * 0.15) for x in world.moose[-4:]], lag_ratio=0.18), run_time=1.0)
        self.finish()


class S08Fall(SpokenScene):
    def construct(self):
        world = add_idle(model_island(moose_n=9, wolf_n=7))
        c = food_counter(100)
        self.add(world, c, model_tag())
        ml = chip("900 moose", MOOSE_BROWN, size=30).move_to([-3.3, 2.55, 0])
        self.add(ml)
        self.at("moose population falls")
        self.play(LaggedStart(*[FadeOut(x) for x in world.moose[-4:]], lag_ratio=0.12),
                  swap(ml, chip("300 moose", MOOSE_BROWN, size=30).move_to(ml)), run_time=1.1)
        self.at("Watch the counter drop")
        self.play(c.tracker.animate.set_value(10), c.box.animate.set_stroke(ORANGE), run_time=2.0,
                  rate_func=linear)
        low = T("LOW", 32, ORANGE, weight=BOLD).next_to(c, DOWN, buff=0.18)
        self.at("only a few moose")
        self.play(FadeIn(low), Indicate(world.moose[:5], color=MOOSE_BROWN),
                  world.wolves.animate.shift(RIGHT * 0.2), run_time=0.85)
        self.finish()


class S09Predict(SpokenScene):
    def construct(self):
        world = add_idle(model_island(moose_n=5, wolf_n=7))
        c = food_counter(10, ORANGE)
        self.add(world, c, model_tag())
        self.at("Here is a question")
        self.play(Indicate(c, color=ORANGE), run_time=0.7)
        self.at("only 10 moose")
        ring = SurroundingRectangle(c, color=ORANGE, buff=0.12, corner_radius=0.15)
        self.play(Create(ring), run_time=0.65)
        q = question_card("Only 10 moose for each wolf. What happens to the wolves next?",
                          y=-3.05, max_w=10.3, size=28)
        self.at("What happens to the wolves")
        self.play(FadeIn(q.question, shift=UP * 0.1), run_time=0.8)
        pulse(ring, base=4.5, amp=2.0, speed=3.0)
        self.at("Pause and predict")
        self.play(Indicate(q.question, color=GOLD), run_time=0.7)
        self.finish()


class S10Pause(PredictPause):
    QUESTION = "Only 10 moose for each wolf. What happens to the wolves next?"
    CARD = {"y": -3.05, "max_w": 10.3, "size": 28}
    RING_AT = (6.0, -3.05, 0)
    SECONDS = 5.0

    def backdrop(self):
        return low_world(False)


class S11Reveal(SpokenScene):
    def construct(self):
        world = add_idle(model_island(moose_n=5, wolf_n=7))
        c = food_counter(10, ORANGE)
        self.add(world, c, model_tag())
        rule = fit_text("model rule: too few to feed the wolves", max_w=5.0, size=28,
                        color=ORANGE).move_to([2.8, 1.55, 0])
        self.at("that number is too low")
        self.play(FadeIn(rule), Indicate(c, color=ORANGE), run_time=0.8)
        search_paths = [Line(w.get_center(), w.get_center() + RIGHT * (0.5 + 0.12 * i))
                        for i, w in enumerate(world.wolves[:3])]
        self.at("Wolves catch too little food")
        self.play(*[MoveAlongPath(w, p) for w, p in zip(world.wolves[:3], search_paths)], run_time=0.9)
        pups = VGroup(*[wolf(0.45, pup=True).move_to([-2.8 + i * 0.55, -1.8, 0]) for i in range(3)])
        self.add(pups)
        self.at("fewer pups survive")
        self.play(FadeOut(pups[1:]), pups[0].animate.shift(UP * 0.1), run_time=0.75)
        wolves_label = chip("30 wolves", WOLF_GREY, size=28).move_to([-1.0, 2.55, 0])
        self.add(wolves_label)
        new_label = chip("12 wolves", WOLF_GREY, size=28).move_to(wolves_label)
        self.at("wolf population falls")
        self.play(LaggedStart(*[FadeOut(w) for w in world.wolves[3:]], lag_ratio=0.12),
                  swap(wolves_label, new_label), run_time=1.0)
        self.at("look at the moose")
        self.play(FadeOut(rule), world.animate.shift(RIGHT * 0.65), run_time=0.75)
        rings = VGroup(*[Circle(radius=0.48, color=MOOSE_BROWN, stroke_width=4).move_to(m)
                         for m in world.moose])
        alive = T("still alive", 34, MOOSE_BROWN, weight=BOLD).move_to([2.7, -2.2, 0])
        self.at("Many moose are still alive")
        self.play(LaggedStart(*[Create(r) for r in rings], lag_ratio=0.1), FadeIn(alive), run_time=1.0)
        self.finish()


def cycle_diagram(scale=1.0, center=ORIGIN):
    labels = [chip("many moose", MOOSE_BROWN, size=26), chip("wolves increase", WOLF_GREY, size=26),
              chip("fewer moose", MOOSE_BROWN, size=26), chip("wolves decrease", WOLF_GREY, size=26)]
    positions = [UP * 2.0, RIGHT * 3.0, DOWN * 2.0, LEFT * 3.0]
    for lab, pos in zip(labels, positions):
        lab.move_to(pos)
    ends = [(labels[0].get_right(), labels[1].get_top()),
            (labels[1].get_bottom(), labels[2].get_right()),
            (labels[2].get_left(), labels[3].get_bottom()),
            (labels[3].get_top(), labels[0].get_left())]
    arrows = VGroup(*[CurvedArrow(a, b, angle=-0.34, color=GOLD,
                                  stroke_width=4, tip_length=0.2) for a, b in ends])
    g = VGroup(*labels, arrows).scale(scale).move_to(center)
    g.labels, g.arrows = VGroup(*labels), arrows
    return g


class S12Recover(SpokenScene):
    def construct(self):
        world = add_idle(model_island(moose_n=5, wolf_n=3))
        c = food_counter(10, ORANGE)
        self.add(world, c, model_tag())
        calves = VGroup(*[moose(0.62, calf=True).move_to([-2.7 + i * 1.25, -1.55, 0]) for i in range(3)])
        self.at("fewer wolves hunting")
        self.play(Indicate(world.wolves, color=WOLF_GREY), run_time=0.65)
        self.at("more moose calves survive")
        self.play(LaggedStart(*[FadeIn(x, shift=UP * 0.15) for x in calves], lag_ratio=0.2), run_time=0.9)
        self.at("moose population grows")
        self.play(calves.animate.scale(1.35).shift(UP * 0.15),
                  LaggedStart(*[FadeIn(x) for x in world.moose[3:]], lag_ratio=0.15), run_time=1.0)
        self.at("counter climbs back up")
        self.play(c.tracker.animate.set_value(55), c.box.animate.set_stroke(TEXT), run_time=1.5,
                  rate_func=linear)
        cycle = cycle_diagram(0.88)
        self.at("loop can start over")
        self.play(FadeOut(VGroup(world, calves, c)), FadeIn(cycle.labels, lag_ratio=0.12), run_time=0.8)
        self.play(LaggedStart(*[Create(a) for a in cycle.arrows], lag_ratio=0.16), run_time=1.1)
        self.finish()


class S13Scope(SpokenScene):
    def construct(self):
        panels = TwoPanel("rule fits", "rule may fail", colors=(GOLD, WOLF_GREY), top=3.2, bottom=-2.5)
        self.add(panels)
        left_world = model_island(moose_n=3, wolf_n=2, trees_n=1).scale(0.47)
        panels.put(left_world, "left")
        one_prey = fit_text("mostly one prey\non an island", max_w=4.6, size=30,
                            color=GOLD).move_to([-3.3, -1.65, 0])
        self.at("predator that eats mostly")
        self.play(FadeIn(left_world), FadeIn(one_prey), run_time=0.85)
        boundary = DashedVMobject(Ellipse(width=4.7, height=2.7, color=GOLD, stroke_width=4).move_to([-3.3, 0.3, 0]))
        self.at("On an island")
        self.play(Create(boundary), run_time=0.65)
        no_exit = T("cannot easily leave", 28, TEXT).move_to([-3.3, -2.15, 0])
        self.at("cannot easily leave")
        self.play(FadeIn(no_exit), Indicate(boundary, color=GOLD), run_time=0.7)
        pred = wolf(1.15).move_to([2.45, 0.4, 0])
        bowl = Arc(radius=0.65, start_angle=PI, angle=PI, color=TEXT, stroke_width=6).move_to([4.55, 0.35, 0])
        food = VGroup(*[Dot(radius=0.11, color=TREE_GREEN).move_to([4.2 + 0.28 * i, 0.55, 0]) for i in range(3)])
        other = T("other food", 28, TREE_GREEN).next_to(bowl, DOWN, buff=0.2)
        self.at("predator with other food")
        self.play(FadeIn(pred), FadeIn(bowl), FadeIn(food), FadeIn(other), run_time=0.8)
        prey = VGroup(*[moose(0.58).move_to([2.3 + 0.85 * i, -1.25, 0]) for i in range(3)])
        self.at("may not go hungry")
        self.play(pred.animate.shift(RIGHT * 0.55), FadeIn(prey), run_time=0.75)
        fail = fit_text("not hungry: rule does not hold", max_w=5.3, size=28,
                        color=WOLF_GREY).move_to([3.25, -2.15, 0])
        self.at("keep eating a prey")
        self.play(LaggedStart(*[FadeOut(x) for x in prey], lag_ratio=0.18), FadeIn(fail), run_time=1.0)
        self.finish()


class S14Messy(SpokenScene):
    def construct(self):
        world = add_idle(model_island(moose_n=6, wolf_n=3))
        c = food_counter(25)
        self.add(world, c, model_tag())
        heading = T("A real island is messier", 42, TEXT, font=TITLE_FONT).move_to([-1.9, 3.25, 0])
        self.at("real island is messier")
        self.play(FadeIn(heading, shift=DOWN * 0.1), run_time=0.7)
        cloud = VGroup(*[Circle(radius=r, color=SNOW, stroke_width=3, fill_color=SNOW,
                               fill_opacity=0.18) for r in (0.38, 0.5, 0.34)]).arrange(RIGHT, buff=-0.25).move_to([-3.6, 1.6, 0])
        flakes = VGroup(*[T("✦", 24, SNOW).move_to([-4.1 + 0.35 * i, 0.8 - 0.22 * (i % 2), 0]) for i in range(4)])
        flakes.layout_ok = True  # snowflake glyphs are themselves the weather drawing
        weather = T("weather", 28, SNOW).next_to(cloud, UP, buff=0.15)
        self.at("Weather")
        self.play(FadeIn(cloud), FadeIn(flakes, shift=DOWN * 0.2), FadeIn(weather), run_time=0.65)
        tick = VGroup(Circle(radius=0.17, color=GREY, fill_color=GREY, fill_opacity=0.6),
                      *[Line(ORIGIN, d * 0.3, color=GREY, stroke_width=3) for d in (UL, UR, DL, DR)]).move_to([0.0, 1.25, 0])
        tl = T("ticks", 28, GREY).next_to(tick, UP, buff=0.15)
        self.at("ticks")
        self.play(FadeIn(tick, scale=0.5), FadeIn(tl), run_time=0.5)
        germ = VGroup(Circle(radius=0.28, color=ORANGE, fill_color=ORANGE, fill_opacity=0.25),
                      *[Line(d * 0.28, d * 0.43, color=ORANGE, stroke_width=3) for d in (UP, DOWN, LEFT, RIGHT, UL, DR)]).move_to([2.4, 1.1, 0])
        dl = T("disease", 28, ORANGE).next_to(germ, UP, buff=0.15)
        self.at("disease")
        self.play(FadeIn(germ, scale=0.5), FadeIn(dl), run_time=0.5)
        note = fit_text("real island: this number alone cannot show hunger", max_w=10.5,
                        size=30, color=TEXT).move_to([0, -2.55, 0])
        self.at("number alone cannot show")
        self.play(FadeIn(note), c.animate.set_opacity(0.45), run_time=0.85)
        next_film = T("next: real counts", 30, TEAL).move_to([3.8, -1.65, 0])
        self.at("real counts in the second film")
        self.play(FadeIn(next_film, shift=LEFT * 0.15), run_time=0.75)
        self.finish()


class S15Rule(SpokenScene):
    def construct(self):
        world = add_idle(model_island(moose_n=5, wolf_n=3)).set_opacity(0.65)
        for animal in [*world.moose, *world.wolves]:
            animal.clear_updaters()
            bob(animal, amp=0.075, speed=1.5)
        self.add(world, model_tag())
        n = ValueTracker(45)
        big = Readout([("moose per wolf", lambda: n.get_value(), "{:3.0f}", ORANGE)],
                      at=[0, 1.25, 0], size=44, widest=[100], color=ORANGE, pad=0.5)
        hungry = wolf(1.25).move_to([-3.7, -0.15, 0]).rotate(-0.12)
        self.at("answer to our question")
        self.play(FadeIn(big, scale=0.85), FadeIn(hungry), run_time=0.85)
        track = Rectangle(width=9.0, height=0.42, color=TEAL, stroke_width=3).move_to([0.7, 3.3, 0])
        glabel = T("wolf's food", 28, TEAL).next_to(track, LEFT, buff=0.25)
        fill = Rectangle(width=9.0, height=0.42, stroke_width=0, fill_color=TEAL, fill_opacity=0.85)
        fill.move_to(track.get_left() + RIGHT * 4.5)
        fill.add_updater(lambda m: m.become(Rectangle(width=max(0.08, 9.0 * n.get_value() / 45), height=0.42,
                         stroke_width=0, fill_color=(ORANGE if n.get_value() < 20 else TEAL), fill_opacity=0.85)
                         .move_to(track.get_left(), aligned_edge=LEFT)))
        self.add(fill)
        self.play(FadeIn(track), FadeIn(glabel), run_time=0.5)
        self.at("few moose for each wolf")
        far = [m for m in world.moose][:3]
        self.play(n.animate.set_value(10), hungry.animate.shift(RIGHT * 1.6),
                  *[m.animate.shift(RIGHT * (1.2 + 0.5 * i) + UP * 0.2) for i, m in enumerate(far)],
                  run_time=3.6, rate_func=linear)
        miss = Arrow(hungry.get_right(), [1.8, 0.1, 0], color=WOLF_GREY, stroke_width=5)
        self.at("catch moose less often")
        self.play(GrowArrow(miss), run_time=1.0)
        self.play(miss.animate.shift(RIGHT * 1.2), hungry.animate.shift(RIGHT * 0.8), run_time=1.2)
        self.play(FadeOut(miss), hungry.animate.shift(LEFT * 1.0), run_time=1.2)
        self.at("too little food")
        self.play(hungry.animate.rotate(0.22).shift(DOWN * 0.22), n.animate.set_value(6), run_time=1.5)
        self.at("fewer wolves survive")
        self.play(hungry.animate.set_opacity(0.3), Indicate(big, color=ORANGE, scale_factor=1.1), run_time=1.6)
        final = fit_text("Wolves usually run short of food\nbefore the moose run out.",
                         max_w=11.2, size=40, color=TEXT, font=TITLE_FONT).move_to([1.3, -3.2, 0])
        self.at("Wolves usually run short")
        self.play(Write(final), Indicate(world.moose, color=MOOSE_BROWN), run_time=1.8)
        self.play(Indicate(final, color=ORANGE, scale_factor=1.04), hungry.animate.shift(LEFT * 0.5),
                  n.animate.set_value(8), run_time=2.0)
        self.finish()


class S16End(EndCard):
    LINE = "Wolves usually run short of food before the moose run out."
