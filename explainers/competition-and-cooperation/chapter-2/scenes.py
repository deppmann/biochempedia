"""When Working Together Helps — chapter 2.

COLOR MAP (carried from chapter 1, with the chapter-2 update in TASK.md)
  GOLD   = limited resources / food
  TEAL   = the population being followed
  GREEN  = cooperation and successful links
  BLUE   = abiotic factors
  CORAL  = living threats (disease and predators)
  GREY   = habitat structure and de-emphasised context

The honeycomb is the film's carried world.  ``hive_world`` is the only builder for it, so
landmarks never drift between scenes.
"""
import numpy as np
from bp_parts import *  # noqa: F401,F403

CORAL = "#FC7A70"


def arrow(a, b, color=GREEN, width=6, tip=0.22):
    return Arrow(a, b, buff=0.08, color=color, stroke_width=width,
                 tip_length=tip, max_tip_length_to_length_ratio=0.35)


def flow_dot(path, color=GOLD, speed=0.11, radius=0.09):
    """A continuously travelling resource dot tied to a path."""
    drawable = path if path.get_num_points() else path.family_members_with_points()[0]
    dot = Dot(drawable.point_from_proportion(0), radius=radius, color=color)
    dot._flow_t = 0.0

    def move(mob, dt):
        mob._flow_t = (mob._flow_t + speed * dt) % 1.0
        mob.move_to(drawable.point_from_proportion(mob._flow_t))

    return dot.add_updater(move)


def sway(mob, amount=0.12, speed=1.1, phase=0.0):
    """Small continuous horizontal movement for an active subject."""
    mob._sway_t, base = phase, mob.get_center().copy()

    def move(item, dt):
        item._sway_t += dt
        item.move_to(base + RIGHT * amount * np.sin(speed * item._sway_t))

    return mob.add_updater(move)


def bee(at, scale=1.0, angle=0.0):
    """A labelled-cartoon worker, not an anatomical drawing."""
    body = Ellipse(width=0.82 * scale, height=0.46 * scale, color=TEAL,
                   stroke_width=3, fill_color=TEAL, fill_opacity=0.62)
    wing = Ellipse(width=0.34 * scale, height=0.22 * scale, color=TEXT,
                   stroke_width=2, fill_color=TEXT, fill_opacity=0.12)
    wing.move_to(body.get_center() + UP * 0.27 * scale)
    stripe = Line(UP * 0.19 * scale, DOWN * 0.19 * scale, color=BG, stroke_width=4)
    face = Dot(RIGHT * 0.28 * scale, radius=0.045 * scale, color=TEXT)
    return VGroup(wing, body, stripe, face).rotate(angle).move_to(at)


def honey_cell(at, radius=0.72):
    return RegularPolygon(6, radius=radius, color=GOLD, stroke_width=2,
                          fill_color=GOLD, fill_opacity=0.045).move_to(at)


HIVE_CENTRES = [
    (-4.6, 1.35), (-3.35, 1.35), (-2.1, 1.35), (-0.85, 1.35),
    (0.4, 1.35), (1.65, 1.35), (2.9, 1.35), (4.15, 1.35),
    (-4.0, 0.28), (-2.75, 0.28), (-1.5, 0.28), (-0.25, 0.28),
    (1.0, 0.28), (2.25, 0.28), (3.5, 0.28), (4.75, 0.28),
    (-4.6, -0.79), (-3.35, -0.79), (-2.1, -0.79), (-0.85, -0.79),
    (0.4, -0.79), (1.65, -0.79), (2.9, -0.79), (4.15, -0.79),
]

BEE_POS = [(-4.45, 1.35), (-2.75, 0.28), (0.4, -0.79), (2.25, 0.28), (4.1, 1.35)]


def hive_world(mode="jobs", question=False, labels=True):
    """Rebuild the same large hive, with stable landmarks in every continuing scene."""
    frame = RoundedRectangle(corner_radius=0.34, width=11.7, height=5.45,
                             color=GOLD, stroke_width=3, fill_color=GOLD,
                             fill_opacity=0.035).move_to([0, 0.05, 0])
    cells = VGroup(*[honey_cell([x, y, 0]) for x, y in HIVE_CENTRES])
    entrance = Arc(radius=0.58, start_angle=0, angle=PI, color=GREY,
                   stroke_width=7).move_to([5.25, -1.55, 0])
    larva = VGroup(*[Circle(radius=0.16 + 0.025 * i, color=TEXT, stroke_width=2,
                            fill_color=TEXT, fill_opacity=0.13)
                     for i in range(3)]).arrange(RIGHT, buff=-0.07).move_to([0.4, -0.79, 0])
    flower = VGroup(Circle(radius=0.32, color=GOLD, fill_color=GOLD, fill_opacity=0.25),
                    *[Dot(0.42 * np.array([np.cos(a), np.sin(a), 0]), radius=0.12, color=GOLD)
                      for a in np.linspace(0, TAU, 6)[:-1]]).move_to([-5.05, 2.18, 0])
    food_store = VGroup(*[Dot([-1.8 + 0.28 * (i % 4), 1.55 + 0.27 * (i // 4), 0],
                                  radius=0.105, color=GOLD) for i in range(12)])

    if mode == "collectors":
        bees = VGroup(*[bee([x, y, 0], 0.92, 0.12) for x, y in
                         [(-3.9, 1.35), (-2.7, 1.35), (-1.45, 1.35), (-0.2, 1.35), (1.05, 1.35)]])
        paths = VGroup(*[DashedLine(b.get_center(), flower.get_center(), color=GREEN,
                                   stroke_width=5, dash_length=0.16) for b in bees])
    else:
        bees = VGroup(*[bee([x, y, 0], 0.96, (-0.14 + 0.07 * i)) for i, (x, y) in enumerate(BEE_POS)])
        paths = VGroup(
            arrow(flower.get_center(), bees[0].get_center(), GREEN, 6),
            arrow(bees[0].get_center(), food_store.get_center(), GREEN, 6),
            arrow(food_store.get_center(), bees[2].get_center(), GREEN, 6),
            arrow(bees[3].get_center(), entrance.get_center(), GREEN, 6),
        )

    g = VGroup(frame, cells, entrance, larva, flower, food_store, paths, bees)
    g.frame, g.cells, g.entrance, g.larva = frame, cells, entrance, larva
    g.flower, g.food_store, g.paths, g.bees = flower, food_store, paths, bees
    if labels:
        if mode == "collectors":
            labs = VGroup(T("all collecting", 30, TEAL).move_to([0, 3.18, 0]))
        else:
            labs = VGroup(T("collect", 28, GREEN).move_to([-4.65, 3.18, 0]),
                          T("care", 28, GREEN).move_to([0.35, -1.72, 0]),
                          T("guard", 28, GREEN).move_to([4.85, -2.32, 0]))
        g.add(labs)
        g.labels = labs
    if question:
        qs = VGroup(T("?", 64, CORAL).move_to(entrance.get_center() + UP * 0.72),
                    T("?", 64, CORAL).move_to(larva.get_center() + UP * 0.68))
        for mark in qs:
            mark.layout_ok = True  # deliberately sits on the two unattended needs
        g.add(qs)
        g.questions = qs
    return g


def tube_world():
    glass = RoundedRectangle(corner_radius=0.5, width=5.6, height=5.45,
                             color=GREY, stroke_width=4, fill_color=GREY,
                             fill_opacity=0.08).move_to([-3.3, 0.05, 0])
    food = VGroup(*[Dot([-4.7 + 0.66 * (i % 5), -1.35 + 0.67 * (i // 5), 0],
                              radius=0.12, color=GOLD) for i in range(15)])
    swimmers = VGroup(*[Ellipse(width=0.65, height=0.36, color=TEAL, stroke_width=3,
                                fill_color=TEAL, fill_opacity=0.55).rotate(0.18 * (i - 2)).move_to(p)
                        for i, p in enumerate([(-4.4, 1.7, 0), (-3.1, 0.9, 0),
                                               (-4.25, -0.25, 0), (-2.6, -1.25, 0), (-1.9, 1.65, 0)])])
    return VGroup(glass, food, swimmers)


def forest_link():
    ground = Line([-5.6, -1.85, 0], [5.6, -1.85, 0], color=GREY, stroke_width=4)
    trees = VGroup(*[VGroup(Line([x, -1.85, 0], [x, 0.55, 0], color=GREY, stroke_width=7),
                               Triangle(color=GREEN, fill_color=GREEN, fill_opacity=0.12).scale(0.7).move_to([x, 0.65, 0]))
                     for x in (-5.0, -3.9, 3.9, 5.0)])
    return VGroup(ground, trees)


class S00Hook(SpokenScene):
    def construct(self):
        tube = tube_world()
        self.play(FadeIn(tube[0]), LaggedStart(*[FadeIn(x) for x in tube[1:]], lag_ratio=0.05), run_time=1.8)
        self.at("drawing from one")
        left_lab = T("one limited supply", 34, GOLD).move_to([-3.3, 3.12, 0])
        self.play(FadeIn(left_lab), tube[1].animate.scale(0.82), run_time=1.2)
        self.at("how can working")
        q = fit_text("How can working together help?", max_w=5.5, size=40,
                     color=GREEN, font=TITLE_FONT).move_to([3.6, 2.25, 0])
        self.play(Write(q), run_time=1.2)
        self.at("Gold food dots")
        target = hive_world(labels=False)
        stream = VGroup(*[Dot(tube[1][i].get_center(), radius=0.12, color=GOLD) for i in range(10)])
        self.add(stream)
        self.play(FadeOut(tube[2]), Transform(tube[0], target.frame),
                  *[stream[i].animate.move_to(target.food_store[i].get_center()) for i in range(10)],
                  FadeOut(tube[1]), FadeOut(left_lab), FadeOut(q), run_time=2.1)
        self.add(target.cells, target.entrance, target.larva, target.flower, target.food_store)
        self.remove(stream)
        self.at("same resource now")
        self.play(LaggedStart(*[GrowArrow(p) for p in target.paths], lag_ratio=0.14),
                  LaggedStart(*[FadeIn(b, scale=0.4) for b in target.bees], lag_ratio=0.1), run_time=2.0)
        pulse(target.paths, base=5, amp=1.4, speed=2.0)
        self.at("picture changes")
        cap = caption("The picture changes. Limited needs remain.", color=TEXT)
        self.play(FadeIn(cap), target.bees.animate.shift(RIGHT * 0.3), run_time=1.3)
        self.finish()


class S01Title(TitleCard):
    LESSON = "Competition and Cooperation"
    TITLE = "When Working Together Helps"


class S02Cooperation(SpokenScene):
    def construct(self):
        hive = hive_world(labels=False)
        self.play(FadeIn(hive.frame), FadeIn(hive.cells), run_time=0.7)
        self.play(LaggedStart(*[FadeIn(b, scale=0.5) for b in hive.bees], lag_ratio=0.12),
                  FadeIn(hive.flower), FadeIn(hive.food_store), run_time=1.2)
        sway(hive.bees, amount=0.24, speed=2.0)
        self.at("work together")
        self.play(LaggedStart(*[GrowArrow(p) for p in hive.paths], lag_ratio=0.12), run_time=1.2)
        self.add(*[flow_dot(p, speed=0.09 + 0.012 * i) for i, p in enumerate(hive.paths)])
        count = T("Tens of thousands can live here.", 32, TEAL).move_to([0, 3.25, 0])
        self.play(FadeIn(count), run_time=0.7)
        self.at("workers collect food")
        roles = VGroup(T("collect", 28, GREEN).move_to([-4.7, 3.18, 0]),
                       T("guard", 28, GREEN).move_to([4.9, -2.3, 0]),
                       T("care for young", 28, GREEN).move_to([0.4, -1.72, 0]))
        self.play(FadeIn(roles[0]), hive.bees[0].animate.move_to(hive.flower.get_center() + DOWN * 0.62), run_time=1.0)
        self.at("guard the hive")
        self.add(hive.entrance, hive.larva)
        self.play(FadeIn(roles[1]), hive.bees[3].animate.move_to(hive.entrance.get_center() + LEFT * 0.7), run_time=0.8)
        self.at("care for young")
        self.play(FadeIn(roles[2]), hive.bees[2].animate.move_to(hive.larva.get_center() + LEFT * 0.8), run_time=0.8)
        self.at("pass liquid food")
        drop = Dot(hive.bees[0].get_center() + UP * 0.38, radius=0.15, color=GOLD)
        self.play(FadeIn(drop), run_time=0.3)
        self.play(drop.animate.move_to(hive.bees[1].get_center() + UP * 0.38), run_time=0.9)
        self.at("not always equal")
        big = Circle(radius=0.28, color=GOLD, fill_color=GOLD, fill_opacity=0.7).move_to([-0.6, 0.1, 0])
        small = Circle(radius=0.14, color=GOLD, fill_color=GOLD, fill_opacity=0.7).move_to([0.25, 0.1, 0])
        self.play(ReplacementTransform(drop, big), FadeIn(small), run_time=0.8)
        self.at("picture separates")
        self.play(FadeOut(count), roles.animate.set_opacity(1), hive.paths.animate.set_stroke(width=7), run_time=1.0)
        self.finish()


class S03Predict(SpokenScene):
    QUESTION = "Which needs would go unmet?"

    def construct(self):
        hive = hive_world(mode="collectors", question=False, labels=True)
        self.play(FadeIn(hive.frame), FadeIn(hive.cells), FadeIn(hive.flower), run_time=0.7)
        self.play(LaggedStart(*[FadeIn(b) for b in hive.bees], lag_ratio=0.1), run_time=1.0)
        self.at("nobody guards")
        self.add(hive.entrance, hive.larva)
        self.play(FadeIn(hive.paths), run_time=0.8)
        qmarks = VGroup(T("?", 64, CORAL).move_to(hive.entrance.get_center() + UP * 0.72),
                        T("?", 64, CORAL).move_to(hive.larva.get_center() + UP * 0.68))
        for mark in qmarks:
            mark.layout_ok = True  # deliberately sits on the two unattended needs
        self.play(FadeIn(qmarks, scale=0.7), run_time=0.8)
        self.at("Which needs")
        q = question_card(self.QUESTION, y=-3.15, max_w=8.8)
        self.play(FadeIn(q.question), run_time=0.7)
        self.at("Watch the green")
        pulse(hive.paths, base=5, amp=2, speed=2.6)
        self.add(*[flow_dot(p, color=GREEN, speed=0.09 + 0.015 * i) for i, p in enumerate(hive.paths)])
        self.play(hive.bees.animate.shift(LEFT * 0.35), run_time=2.1, rate_func=there_and_back)
        sway(hive.cells, amount=0.055, speed=2.2)
        self.at("whole colony")
        self.play(Indicate(VGroup(hive.frame, hive.cells), color=GREEN, scale_factor=1.015), run_time=1.2)
        self.finish()


class S04Pause(PredictPause):
    QUESTION = "Which needs would go unmet?"
    SECONDS = 4.5
    CARD = {"y": -3.15, "max_w": 8.8}

    def backdrop(self):
        return hive_world(mode="collectors", question=True, labels=True)


class S05Reveal(SpokenScene):
    def construct(self):
        old = hive_world(mode="collectors", question=True, labels=True)
        self.add(old)
        self.at("Different jobs")
        hive = hive_world(mode="jobs", question=False, labels=True)
        self.play(FadeOut(old), FadeIn(hive), run_time=1.5)
        self.add(*[flow_dot(p, speed=0.09 + 0.012 * i) for i, p in enumerate(hive.paths)])
        sway(hive.cells, amount=0.055, speed=2.1)
        self.at("One worker brings")
        self.play(hive.bees[0].animate.move_to(hive.flower.get_center() + DOWN * 0.62), run_time=0.8)
        self.at("another guards")
        self.play(hive.bees[3].animate.move_to(hive.entrance.get_center() + LEFT * 0.7), run_time=0.8)
        self.at("another tends")
        self.play(hive.bees[2].animate.move_to(hive.larva.get_center() + LEFT * 0.8), run_time=0.8)
        self.at("Together")
        for path in hive.paths:
            pulse(path, base=6, amp=2, speed=3)
        self.play(LaggedStart(*[Indicate(p, color=GREEN, scale_factor=1.03) for p in hive.paths], lag_ratio=0.14), run_time=1.6)
        self.at("Each linked job")
        needs = VGroup(T("food", 28, GOLD), T("young", 28, GREEN), T("safety", 28, GREEN)).arrange(RIGHT, buff=1.2).move_to([0, -2.15, 0])
        self.play(FadeIn(needs, shift=UP * 0.1), hive.bees.animate.shift(UP * 0.08), run_time=1.3)
        self.at("every worker still")
        remaining = hive.food_store[:-4]
        self.play(FadeOut(VGroup(*hive.food_store[-4:])), hive.bees.animate.shift(DOWN * 0.08), run_time=1.4)
        cap = caption("Cooperation helps; resources are still finite.", color=TEXT)
        self.play(FadeOut(needs), FadeIn(cap), Indicate(remaining, color=GOLD, scale_factor=1.12), run_time=1.0)
        self.finish()


def wolf_case():
    wolves = VGroup(*[bee([x, y, 0], 0.65).set_color(TEAL) for x, y in
                       [(-2.1, 0.5), (-1.7, 1.25), (-1.0, 1.65), (-0.25, 1.25), (0.15, 0.5)]])
    elk = VGroup(Ellipse(width=1.1, height=0.65, color=GOLD, fill_color=GOLD, fill_opacity=0.22),
                 Line([0.35, 0.22, 0], [0.72, 0.72, 0], color=GOLD, stroke_width=5)).move_to([-0.9, 0.55, 0])
    arc = Arc(radius=1.55, start_angle=0.1, angle=PI - 0.2, color=GREEN, stroke_width=7).move_to(elk)
    return VGroup(wolves, elk, arc)


def fish_case():
    school = VGroup(*[Triangle(color=TEAL, fill_color=TEAL, fill_opacity=0.55).scale(0.18).rotate(-PI / 2).move_to([x, y, 0])
                      for x, y in [(1.3, 1.2), (1.8, 1.55), (2.15, 1.05), (2.55, 1.45), (2.9, 1.0), (3.25, 1.5)]])
    predator = Triangle(color=CORAL, fill_color=CORAL, fill_opacity=0.4).scale(0.48).rotate(PI / 2).move_to([4.5, 1.25, 0])
    miss = CurvedArrow(predator.get_left(), [3.5, 0.1, 0], color=CORAL, stroke_width=5)
    return VGroup(school, predator, miss)


class S06MoreCases(SpokenScene):
    def construct(self):
        hive = hive_world(labels=False)
        frame = VGroup(hive.frame, hive.cells)
        self.add(frame, hive.paths)
        pulse(hive.paths, base=5, amp=1.3, speed=2)
        sway(hive.cells, amount=0.055, speed=2.1)
        self.at("different ways")
        self.play(hive.paths.animate.set_opacity(0.25), run_time=0.8)
        wolves = wolf_case()
        self.at("wolf pack")
        self.play(Transform(hive.paths[0], wolves[2]), FadeIn(wolves[0]), FadeIn(wolves[1]), run_time=1.3)
        lab1 = T("pack catches large prey", 24, GREEN).move_to([-3.35, -3.12, 0])
        self.play(FadeIn(lab1), run_time=0.6)
        fish = fish_case()
        self.at("tight school")
        self.play(Transform(hive.paths[1], fish[2]), FadeIn(fish[0]), FadeIn(fish[1]), run_time=1.3)
        lab2 = T("school avoids one strike", 24, GREEN).move_to([3.25, -3.12, 0])
        self.play(FadeIn(lab2), fish[0].animate.shift(DOWN * 0.3), run_time=1.0)
        tag = scope_tag("schematic")
        self.add(tag)
        self.at("get food")
        self.play(Indicate(wolves, color=GOLD, scale_factor=1.04), run_time=0.8)
        self.at("stay safe")
        self.play(Indicate(fish[0], color=GREEN, scale_factor=1.12), run_time=0.8)
        self.play(FadeOut(VGroup(wolves[0], wolves[1], fish[0], fish[1], lab1, lab2, tag)),
                  Transform(hive.paths[0], hive_world(labels=False).paths[0]),
                  Transform(hive.paths[1], hive_world(labels=False).paths[1]), run_time=1.1)
        self.finish()


def factor_badge(text, color, at):
    return chip(text, color=color, size=28, fill_opacity=0.14).move_to(at)


class S07Factors(SpokenScene):
    def construct(self):
        n = ValueTracker(0.72)
        bar_bg = RoundedRectangle(corner_radius=0.16, width=1.4, height=4.8, color=GREY, stroke_width=3).move_to([0, -0.15, 0])
        bar = always_redraw(lambda: Rectangle(width=1.08, height=4.3 * n.get_value(), color=TEAL,
                                              fill_color=TEAL, fill_opacity=0.55, stroke_width=0)
                            .align_to(bar_bg, DOWN).shift(UP * 0.18))
        pop_lab = T("population", 30, TEAL).move_to([0, -2.9, 0])
        self.play(FadeIn(bar_bg), FadeIn(bar), FadeIn(pop_lab), run_time=0.8)
        sway(pop_lab, amount=0.1, speed=1.0)
        self.at("does not remove")
        self.play(n.animate.set_value(0.56), run_time=1.1)
        head = T("limiting factors", 38, font=TITLE_FONT).move_to([0, 3.3, 0])
        self.at("anything in the environment")
        self.play(FadeIn(head), run_time=0.7)
        bio_ring = Circle(radius=2.1, color=CORAL, stroke_width=4).move_to([-3.75, 0.0, 0])
        abio_ring = Circle(radius=2.1, color=BLUE, stroke_width=4).move_to([3.75, 0.0, 0])
        sway(bio_ring, amount=0.14, speed=2.0)
        sway(abio_ring, amount=0.14, speed=2.0, phase=PI)
        bio_title = T("BIOTIC", 32, CORAL).move_to([-3.75, 2.48, 0])
        abio_title = T("ABIOTIC", 32, BLUE).move_to([3.75, 2.48, 0])
        self.at("Living factors")
        self.play(Create(bio_ring), FadeIn(bio_title), run_time=0.8)
        food = factor_badge("food", GOLD, [-4.45, 0.75, 0])
        disease = factor_badge("disease", CORAL, [-3.05, 0.0, 0])
        predator = factor_badge("predators", CORAL, [-4.0, -0.95, 0])
        self.play(FadeIn(food), run_time=0.4)
        self.at("disease")
        self.play(FadeIn(disease), n.animate.set_value(0.46), run_time=0.7)
        self.at("predators")
        self.play(FadeIn(predator), n.animate.set_value(0.4), run_time=0.7)
        self.at("Non living factors")
        self.play(Create(abio_ring), FadeIn(abio_title), run_time=0.8)
        water = factor_badge("water", BLUE, [3.1, 0.65, 0])
        temp = factor_badge("temperature", BLUE, [4.05, -0.45, 0])
        self.play(FadeIn(water), run_time=0.5)
        self.at("temperature")
        self.play(FadeIn(temp), n.animate.set_value(0.62), run_time=0.9)
        self.at("Shelter can")
        shelter = factor_badge("shelter: depends", TEXT, [0, 2.66, 0])
        self.play(FadeIn(shelter), n.animate.set_value(0.53), run_time=1.0)
        self.finish()


class S08Linked(SpokenScene):
    def construct(self):
        forest = forest_link()
        self.play(FadeIn(forest), run_time=0.8)
        sway(forest[1], amount=0.24, speed=2.0)
        title = T("one community", 38, font=TITLE_FONT).move_to([0, 3.2, 0])
        self.at("interdependent")
        self.play(FadeIn(title), run_time=0.6)
        rabbit_n = ValueTracker(0.85)
        fox_n = ValueTracker(0.82)
        rab_bg = RoundedRectangle(corner_radius=0.12, width=2.0, height=3.7, color=GREY, stroke_width=3).move_to([-3.0, 0, 0])
        fox_bg = RoundedRectangle(corner_radius=0.12, width=2.0, height=3.7, color=GREY, stroke_width=3).move_to([3.0, 0, 0])
        rab = always_redraw(lambda: Rectangle(width=1.6, height=3.2 * rabbit_n.get_value(), color=TEAL,
                                               fill_color=TEAL, fill_opacity=0.58, stroke_width=0).align_to(rab_bg, DOWN).shift(UP * 0.18))
        fox = always_redraw(lambda: Rectangle(width=1.6, height=3.2 * fox_n.get_value(), color=TEAL,
                                               fill_color=TEAL, fill_opacity=0.58, stroke_width=0).align_to(fox_bg, DOWN).shift(UP * 0.18))
        labs = VGroup(T("rabbits", 30, TEAL).move_to([-3, -2.28, 0]), T("foxes", 30, TEAL).move_to([3, -2.28, 0]))
        self.at("change in one")
        self.play(FadeIn(VGroup(rab_bg, fox_bg, rab, fox, labs)), run_time=0.9)
        food_arrow = arrow([-1.8, 0.45, 0], [1.8, 0.45, 0], GOLD, 8, 0.28)
        food_lab = T("food", 30, GOLD).next_to(food_arrow, UP, buff=0.18)
        self.play(GrowArrow(food_arrow), FadeIn(food_lab), run_time=0.8)
        self.add(flow_dot(food_arrow, color=GOLD, speed=0.10, radius=0.12))
        self.at("disease reduces")
        disease = factor_badge("disease", CORAL, [-4.8, 2.1, 0])
        strike = arrow(disease.get_bottom(), rab_bg.get_top(), CORAL, 7)
        self.play(FadeIn(disease), GrowArrow(strike), rabbit_n.animate.set_value(0.35), run_time=1.5)
        self.at("foxes have less")
        thin = arrow([-1.8, 0.45, 0], [1.8, 0.45, 0], GOLD, 3, 0.20)
        self.play(Transform(food_arrow, thin), fox_n.animate.set_value(0.48), run_time=1.4)
        self.at("strikes rabbits directly")
        self.play(Indicate(strike, color=CORAL, scale_factor=1.05), run_time=0.8)
        self.at("through their food")
        self.play(Indicate(food_arrow, color=GOLD, scale_factor=1.04), fox_n.animate.set_value(0.36), run_time=1.1)
        self.at("never infects them")
        shield = Circle(radius=0.72, color=TEXT, stroke_width=4).move_to([3.0, 1.0, 0])
        no_disease = T("no infection", 26, TEXT).move_to([3.0, 2.38, 0])
        self.play(FadeIn(shield), FadeIn(no_disease), run_time=0.9)
        self.add(scope_tag("schematic"))
        self.finish()


class S09Scope(SpokenScene):
    def construct(self):
        panels = TwoPanel("cooperation helps", "limits remain", colors=(GREEN, CORAL), top=3.0, bottom=-2.35)
        self.play(FadeIn(panels), run_time=0.8)
        hive = hive_world(labels=False).scale(0.48)
        panels.put(hive, "left")
        forest = forest_link().scale(0.45)
        panels.put(forest, "right")
        sway(forest[1], amount=0.48, speed=2.2)
        self.at("can help members")
        self.play(FadeIn(hive), LaggedStart(*[GrowArrow(p) for p in hive.paths], lag_ratio=0.12), run_time=1.2)
        self.add(*[flow_dot(p, speed=0.08 + 0.012 * i, radius=0.08) for i, p in enumerate(hive.paths)])
        sway(hive.bees, amount=0.34, speed=2.0)
        pulse(hive.paths, base=5, amp=1.8, speed=2.2)
        n = ValueTracker(0.25)
        bar_bg = RoundedRectangle(corner_radius=0.12, width=1.45, height=3.4, color=GREY, stroke_width=3).move_to([3.15, 0.0, 0])
        bar = always_redraw(lambda: Rectangle(width=1.12, height=2.8 * n.get_value(), color=TEAL,
                                              fill_color=TEAL, fill_opacity=0.62, stroke_width=0).align_to(bar_bg, DOWN).shift(UP * 0.16))
        factors = VGroup(factor_badge("food", GOLD, [4.9, 1.3, 0]).scale(0.85),
                         factor_badge("water", BLUE, [4.15, 1.95, 0]).scale(0.85),
                         factor_badge("disease", CORAL, [4.75, -1.1, 0]).scale(0.85))
        self.at("Both can happen")
        self.play(FadeIn(forest), FadeIn(bar_bg), FadeIn(bar), FadeIn(factors),
                  n.animate.set_value(0.67), run_time=1.5)
        self.at("changes what members")
        self.play(hive.paths.animate.set_stroke(width=8), hive.bees.animate.shift(RIGHT * 0.16), run_time=1.3)
        self.at("same picture")
        link = arrow([0.0, -2.7, 0], [0.0, -2.7, 0], GREEN)
        summary = caption("Help and limits belong in the same picture.", color=TEXT)
        self.play(FadeIn(summary), n.animate.set_value(0.73), run_time=1.3)
        self.at("does not make food")
        self.play(LaggedStart(*[Indicate(x, scale_factor=1.08) for x in factors], lag_ratio=0.25),
                  n.animate.set_value(0.68), run_time=2.2)
        self.finish()


class S10End(EndCard):
    LINE = "Limited resources can restrict populations;\ncooperation can help members meet their needs."
