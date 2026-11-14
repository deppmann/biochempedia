from bp_parts import *


# COLOR MAP (shared across this film):
# water = BLUE, carbon = ORANGE, nitrogen = GREEN, sunlight = GOLD,
# human-added flow = RED outline only (not used in this chapter).
WATER = BLUE
CARBON = ORANGE
NITROGEN = GREEN
SUN = GOLD


def token(color, radius=0.13):
    return Dot(radius=radius, color=color, stroke_color=TEXT, stroke_width=1.5)


def crab_shape(scale=1.0):
    """A simple labelled animal silhouette, not an anatomical claim."""
    body = Ellipse(width=1.35, height=0.72, color=TEXT, fill_color="#315E73", fill_opacity=0.95,
                   stroke_width=3)
    eye_l = Dot(body.get_top() + LEFT * 0.28, radius=0.055, color=TEXT)
    eye_r = Dot(body.get_top() + RIGHT * 0.28, radius=0.055, color=TEXT)
    legs = VGroup(*[
        Line(body.get_center() + [x, -0.18, 0], body.get_center() + [x * 1.55, -0.52, 0],
             color=TEXT, stroke_width=3)
        for x in (-0.48, -0.25, 0.25, 0.48)
    ])
    claws = VGroup(
        Arc(radius=0.28, start_angle=-0.3, angle=1.9, color=TEXT).move_to(LEFT * 0.82 + UP * 0.2),
        Arc(radius=0.28, start_angle=PI + 0.3, angle=-1.9, color=TEXT).move_to(RIGHT * 0.82 + UP * 0.2),
    )
    label = T("CRAB", 28, TEXT, weight=BOLD).move_to(body).shift(DOWN * 0.95)
    for shape in (body, legs, claws, eye_l, eye_r):
        shape.layout_ok = True  # the CRAB label deliberately sits on its own silhouette
    return VGroup(legs, claws, body, eye_l, eye_r, label).scale(scale)


def plant_shape(scale=1.0):
    stem = Line(DOWN * 0.6, UP * 0.55, color=GREEN, stroke_width=8)
    leaves = VGroup(
        Ellipse(width=0.55, height=0.26, color=GREEN, fill_color=GREEN, fill_opacity=0.65).rotate(0.45).move_to(LEFT * 0.25),
        Ellipse(width=0.55, height=0.26, color=GREEN, fill_color=GREEN, fill_opacity=0.65).rotate(-0.45).move_to(RIGHT * 0.25 + UP * 0.28),
    )
    return VGroup(stem, leaves).scale(scale)


def microbe_shape(label="MICROBES", color=GREEN, scale=1.0):
    lab = T(label, 30, color, weight=BOLD)
    body = RoundedRectangle(width=lab.width + 0.7, height=lab.height + 0.55, corner_radius=0.34, color=color,
                            fill_color=color, fill_opacity=0.18, stroke_width=3).move_to(lab)
    body.layout_ok = True  # deliberate: the label names its own cartoon body
    return VGroup(body, lab).scale(scale)


def leaf_shape(color=GREEN):
    leaf = Ellipse(width=0.75, height=0.38, color=color, fill_color=color, fill_opacity=0.45,
                   stroke_width=3).rotate(-0.35)
    vein = Line(leaf.get_left() + RIGHT * 0.08, leaf.get_right() + LEFT * 0.08, color=color, stroke_width=2).rotate(-0.35)
    return VGroup(leaf, vein)


def watershed(dim=1.0, labels=False, schematic=True):
    """The carried world. Every full-landscape scene calls this exact builder."""
    sky = Rectangle(width=13.2, height=2.35, stroke_width=0, fill_color="#132B3A",
                    fill_opacity=0.78 * dim).move_to([0, 2.35, 0])
    ground = Polygon([-6.6, 1.25, 0], [-5.1, 1.48, 0], [-3.4, 0.75, 0], [-1.8, -0.05, 0],
                     [0.0, -0.55, 0], [1.25, -1.0, 0], [6.6, -1.0, 0], [6.6, -3.15, 0],
                     [-6.6, -3.15, 0], color="#8A6B44", fill_color="#4E402D", fill_opacity=0.88 * dim,
                     stroke_width=0)
    field = Polygon([-6.6, 1.25, 0], [-5.1, 1.48, 0], [-3.4, 0.75, 0], [-2.0, 0.0, 0],
                    [-4.0, -0.55, 0], [-6.6, -0.2, 0], color=GREEN, fill_color="#355C38",
                    fill_opacity=0.88 * dim, stroke_width=3)
    bay = Polygon([0.3, -0.62, 0], [1.25, -1.0, 0], [6.6, -1.0, 0], [6.6, -3.15, 0],
                  [-0.2, -3.15, 0], color=WATER, fill_color="#174D68", fill_opacity=0.92 * dim,
                  stroke_width=3)
    river = VMobject(color=WATER, stroke_width=20, stroke_opacity=0.9 * dim)
    river.set_points_smoothly([[-4.0, 0.42, 0], [-3.0, 0.10, 0], [-2.2, -0.38, 0],
                               [-1.3, -0.42, 0], [-0.25, -0.8, 0], [0.65, -1.25, 0]])
    cloud = VGroup(*[Circle(r, color=TEXT, fill_color="#B8CBD2", fill_opacity=0.9 * dim, stroke_width=0)
                     .move_to(p) for r, p in [(0.42, [-4.8, 2.55, 0]), (0.58, [-4.25, 2.72, 0]),
                                             (0.45, [-3.67, 2.52, 0]), (0.36, [-4.15, 2.35, 0])]])
    farm = VGroup(
        Polygon([-5.75, 0.45, 0], [-5.15, 0.95, 0], [-4.55, 0.45, 0], color=RED,
                fill_color="#7B3B32", fill_opacity=0.85 * dim),
        Rectangle(width=0.88, height=0.72, color=TEXT, fill_color="#6D5142", fill_opacity=0.9 * dim,
                  stroke_width=2).move_to([-5.15, 0.12, 0]),
        T("FARM", 24, TEXT).move_to([-5.15, 0.1, 0]),
    )
    plant = plant_shape(0.72).move_to([-3.45, 0.14, 0])
    algae = VGroup(*[Arc(radius=0.26, start_angle=-PI / 2, angle=PI, color=GREEN, stroke_width=6)
                     .shift([2.0 + i * 0.34, -2.55 + 0.08 * (i % 2), 0]) for i in range(3)])
    crab = crab_shape(0.78).move_to([4.65, -2.18, 0])
    world = VGroup(sky, ground, field, bay, river, cloud, farm, plant, algae, crab).set_opacity(dim)
    for background in (sky, ground, field, bay):
        background.layout_ok = True  # reservoir labels intentionally sit on these regions
    world.sky, world.ground, world.field, world.bay, world.river = sky, ground, field, bay, river
    world.cloud, world.farm, world.plant, world.algae, world.crab = cloud, farm, plant, algae, crab
    if labels:
        labs = VGroup(T("AIR", 30, TEXT, weight=BOLD).move_to([0.0, 2.65, 0]),
                      T("SOIL", 30, TEXT, weight=BOLD).move_to([-1.9, -2.45, 0]),
                      T("RIVER AND BAY", 30, WATER, weight=BOLD).move_to([2.6, -1.38, 0]),
                      T("LIVING THINGS", 30, GREEN, weight=BOLD).move_to([4.15, 0.1, 0]))
        world.add(labs)
        world.labels = labs
    if schematic:
        world.add(scope_tag("schematic"))
    return world


def moving_water(world):
    pulse(world.river, base=18, amp=3, speed=1.6)
    bob(world.cloud, amp=0.07, speed=1.1)
    bob(world.crab, amp=0.035, speed=1.4, seed=2)
    return world


def predict_backdrop():
    water = Rectangle(width=13.0, height=4.2, stroke_color=WATER, stroke_width=3,
                      fill_color="#174D68", fill_opacity=0.75).move_to([0, -0.75, 0])
    surface = Line([-6.5, 1.35, 0], [6.5, 1.35, 0], color=WATER, stroke_width=7)
    crab = crab_shape(1.55).move_to([0, -0.75, 0])
    c = token(CARBON, 0.22).move_to(crab.get_center() + LEFT * 0.38 + DOWN * 0.1)
    water.layout_ok = True
    pulse(surface, base=7, amp=2, speed=1.5)
    return VGroup(water, surface, crab, c, T("schematic", 24, GREY).move_to([-5.65, -3.3, 0]))


class S00Hook(SpokenScene):
    def construct(self):
        w = moving_water(watershed(schematic=False))
        w.add(T("schematic", 24, GREY).move_to([5.75, 3.35, 0]))
        self.play(FadeIn(w, shift=UP * 0.1), run_time=1.0)
        rain = VGroup(*[Dot([-4.9 + 0.38 * i, 2.05 - 0.12 * (i % 2), 0], radius=0.09, color=WATER)
                        for i in range(7)])
        self.play(rain.animate.shift(DOWN * 2.0 + RIGHT * 0.35), run_time=2.0, rate_func=linear)
        self.at("help build a crab")
        q = T("?", 82, GOLD, weight=BOLD).next_to(w.crab, UP, buff=0.2)
        q.layout_ok = True  # question intentionally floats inside the Bay region
        self.play(FadeIn(q, scale=1.3), w.crab.animate.scale(1.12), run_time=0.8)
        self.at("Keep your eyes")
        outline = SurroundingRectangle(VGroup(w.field, w.river, w.bay), color=TEAL, buff=0.14,
                                       corner_radius=0.25, stroke_width=4)
        self.play(Create(outline), FadeOut(q), run_time=1.0)
        self.at("land river and bay")
        self.play(Indicate(w.field, color=GREEN), Indicate(w.river, color=WATER),
                  Indicate(w.bay, color=WATER), run_time=1.2)
        self.finish()


class S01Title(NarratedScene):
    def construct(self):
        w = moving_water(watershed(dim=0.30, schematic=False))
        title = fit_text("One Crab, Three Connected Cycles", max_w=11.5, size=52,
                         font=TITLE_FONT, weight=BOLD)
        title.layout_ok = True  # deliberate overlay on the dimmed carried watershed
        lesson = T("MATTER CYCLES", 24, TEAL, weight=BOLD).next_to(title, UP, buff=0.28)
        rule = Line(LEFT * 1.4, RIGHT * 1.4, color=GOLD, stroke_width=4).next_to(title, DOWN, buff=0.28)
        self.add(w)
        self.play(FadeIn(lesson), Write(title), GrowFromCenter(rule), run_time=1.1)
        self.wait(0.45)
        self.play(FadeOut(VGroup(lesson, title, rule)), run_time=0.35)
        self.finish()


class S02Map(SpokenScene):
    def construct(self):
        w = moving_water(watershed(labels=True))
        self.add(w)
        blue = VGroup(*[token(WATER).move_to(p) for p in [[-2.5, -0.25, 0], [0.6, -2.0, 0], [3.2, -2.55, 0]]])
        orange = VGroup(*[token(CARBON).move_to(p) for p in [[-1.0, 2.1, 0], [2.7, -1.95, 0]]])
        green = VGroup(*[token(NITROGEN).move_to(p) for p in [[-3.7, -0.3, 0], [2.15, -2.45, 0]]])
        self.play(FadeIn(blue, scale=1.5), run_time=0.7)
        self.at("orange will track")
        self.play(FadeIn(orange, scale=1.5), run_time=0.7)
        self.at("green will track")
        self.play(FadeIn(green, scale=1.5), run_time=0.7)
        self.at("Each colored token")
        self.play(blue.animate.shift(RIGHT * 0.5), orange.animate.shift(UP * 0.25),
                  green.animate.shift(LEFT * 0.35), run_time=2.0, rate_func=there_and_back)
        self.at("A reservoir is")
        self.play(LaggedStart(*[Indicate(x, color=GOLD) for x in w.labels], lag_ratio=0.28), run_time=3.6)
        self.at("such as air")
        self.play(LaggedStart(*[Indicate(x) for x in w.labels], lag_ratio=0.25), run_time=2.2)
        self.finish()


class S03CarbonIn(SpokenScene):
    def construct(self):
        w = moving_water(watershed())
        self.add(w)
        co2 = VGroup(*[token(CARBON, 0.15).move_to(p) for p in [[-1.1, 2.35, 0], [0.1, 2.1, 0],
                                                                 [2.8, -1.65, 0], [3.4, -2.6, 0]]])
        self.play(FadeIn(co2), co2.animate.shift(RIGHT * 0.35), run_time=1.6)
        self.at("Algae and plants")
        rays = VGroup(*[Arrow([x, 3.2, 0], [x, y, 0], color=SUN, stroke_width=5, buff=0.1,
                              max_tip_length_to_length_ratio=0.15) for x, y in [(-3.45, 0.75), (2.3, -2.2)]])
        self.play(Create(rays[0]), Create(rays[1]), run_time=1.0)
        self.at("photosynthesis")
        sugar1 = chip("SUGAR", CARBON, size=30).scale(0.78).move_to(w.plant.get_center() + UP * 0.15)
        sugar2 = chip("SUGAR", CARBON, size=30).scale(0.78).move_to([2.3, -2.35, 0])
        self.play(Transform(co2[0], sugar1), Transform(co2[2], sugar2), FadeOut(rays), run_time=1.5)
        self.at("Food moves")
        animal_body = Circle(0.34, color=TEXT, fill_color=TEXT, fill_opacity=0.16).move_to([3.25, -1.82, 0])
        animal_body.layout_ok = True
        animal_lab = T("ANIMAL", 24, TEXT).next_to(animal_body, UP, buff=0.12)
        animal = VGroup(animal_body, animal_lab)
        path1 = CurvedArrow([2.55, -2.2, 0], [3.55, -1.95, 0], angle=0.25, color=CARBON, stroke_width=7)
        path2 = CurvedArrow([3.55, -1.95, 0], [4.35, -2.15, 0], angle=-0.2, color=CARBON, stroke_width=7)
        food_block = Square(0.32, color=CARBON, fill_color=CARBON, fill_opacity=0.8).move_to(sugar2)
        self.play(FadeIn(animal), Create(path1), ReplacementTransform(sugar2, food_block), run_time=1.5)
        self.play(food_block.animate.move_to(animal_body.get_center()), run_time=.35)
        self.at("until some reaches")
        food_block.layout_ok = True  # deliberate carbon block inside the labelled animal/crab
        self.play(Create(path2), food_block.animate.move_to(w.crab.get_center() + LEFT * .55 + DOWN * .12), run_time=1.3)
        self.finish()


class S04CarbonOut(SpokenScene):
    def construct(self):
        w = moving_water(watershed())
        self.add(w)
        sugar = Square(0.32, color=CARBON, fill_color=CARBON, fill_opacity=0.8).move_to(
            w.crab.get_center() + LEFT * .55 + DOWN * .12)
        sugar.layout_ok = True  # deliberate carbon block inside the labelled crab
        self.add(sugar)
        self.at("releasing carbon dioxide")
        outs = VGroup(*[token(CARBON, 0.14).move_to(w.crab.get_center()) for _ in range(3)])
        targets = [[3.6, -1.55, 0], [4.7, -1.25, 0], [5.65, -1.8, 0]]
        self.play(FadeOut(sugar), *[outs[i].animate.move_to(targets[i]) for i in range(3)], run_time=1.8)
        self.at("Plants and microbes")
        microbes = microbe_shape("MICROBES", CARBON, 0.82).move_to([-1.1, -2.45, 0])
        extra = VGroup(token(CARBON).move_to(w.plant.get_center()),
                       token(CARBON).move_to(microbes.get_center() + RIGHT * 1.4))
        self.play(FadeIn(microbes), FadeIn(extra), run_time=0.8)
        bob(microbes, amp=.035, speed=1.3)
        self.play(extra[0].animate.shift(UP * 1.0), extra[1].animate.shift(RIGHT * 1.0), run_time=1.4)
        self.at("When organisms die")
        leaf = leaf_shape().move_to([-3.2, 0.05, 0])
        self.play(FadeIn(leaf), leaf.animate.move_to([-2.2, -2.15, 0]).rotate(-0.7), run_time=1.3)
        self.at("decomposers break down")
        decomp = microbe_shape("DECOMPOSERS", CARBON, 0.9).move_to([-1.5, -2.35, 0])
        self.play(Transform(microbes, decomp), FadeOut(leaf), run_time=1.1)
        self.at("returns much of")
        returned = VGroup(*[token(CARBON).move_to(decomp.get_center()) for _ in range(3)])
        self.play(returned[0].animate.move_to([-1.5, 1.3, 0]),
                  returned[1].animate.move_to([-0.1, -1.2, 0]),
                  returned[2].animate.move_to([1.0, -1.65, 0]), run_time=2.3)
        self.finish()


class S05Water(SpokenScene):
    def construct(self):
        w = moving_water(watershed())
        self.add(w)
        drops = VGroup(*[token(WATER, 0.11).move_to([2.2 + i * 0.42, -1.35 - 0.18 * (i % 2), 0]) for i in range(6)])
        self.play(drops.animate.shift(UP * 3.7), run_time=2.2)
        self.at("clouds")
        self.play(drops.animate.move_to(w.cloud.get_center()), Indicate(w.cloud), run_time=0.8)
        self.at("precipitation")
        self.play(drops.animate.arrange(RIGHT, buff=0.18).move_to([-4.2, 1.9, 0]), run_time=0.5)
        self.play(drops.animate.shift(DOWN * 2.1), run_time=1.4)
        self.at("flow across land")
        self.play(drops.animate.move_to([-2.4, -0.15, 0]), run_time=1.2)
        self.at("carries other matter")
        ns = VGroup(*[token(NITROGEN, 0.12).move_to([-3.3 + i * 0.35, -0.42, 0]) for i in range(4)])
        self.play(FadeIn(ns, scale=1.4), run_time=0.7)
        self.at("pick up green nitrogen")
        carrier = SurroundingRectangle(VGroup(drops, ns), color=WATER, buff=0.12, corner_radius=0.2)
        self.play(Create(carrier), run_time=0.6)
        self.at("move it into")
        self.play(VGroup(drops, ns, carrier).animate.move_to([-0.25, -0.75, 0]), run_time=1.5)
        self.finish()


class S06Nitrogen(SpokenScene):
    def construct(self):
        w = watershed(schematic=False)
        self.add(w)
        gas = chip("NITROGEN GAS", NITROGEN, size=26).move_to([-3.3, 2.15, 0])
        stop = Line([-3.8, 0.75, 0], [-2.9, 0.75, 0], color=RED, stroke_width=7)
        self.play(FadeIn(gas), gas.animate.move_to([-3.3, 1.05, 0]), Create(stop), run_time=1.7)
        self.at("Certain microbes")
        soil = RoundedRectangle(width=8.0, height=4.7, corner_radius=0.2, color="#8A6B44",
                                fill_color="#4E402D", fill_opacity=0.95).move_to([-1.0, -0.25, 0])
        soil.layout_ok = True
        root = plant_shape(1.45).move_to([-3.0, 1.0, 0])
        microbes = VGroup(microbe_shape("ROOT MICROBES", NITROGEN, 1.0).move_to([-3.4, -1.1, 0]),
                          microbe_shape("SOIL MICROBES", NITROGEN, 1.0).move_to([1.0, -1.1, 0]))
        self.play(FadeOut(w), FadeOut(stop), FadeIn(soil), FadeIn(root), FadeIn(microbes),
                  gas.animate.move_to([-2.8, -0.15, 0]), run_time=1.3)
        bob(root, amp=.10, speed=1.0)
        bob(microbes, amp=.12, speed=1.15)
        self.at("convert it into ammonia")
        ammonia = chip("AMMONIA", NITROGEN, size=28).move_to(gas)
        self.play(Transform(gas, ammonia), run_time=1.0)
        self.at("make nitrate")
        nitrate = chip("NITRATE", NITROGEN, size=28).move_to([0.6, -0.15, 0])
        self.play(gas.animate.move_to([0.0, -0.15, 0]), Transform(gas, nitrate), run_time=1.2)
        self.at("Plants and algae take up")
        self.play(gas.animate.move_to(root.get_center() + RIGHT * 1.05), Indicate(root, color=NITROGEN), run_time=1.4)
        self.at("Food can then")
        mini = watershed(schematic=True)
        green_food = token(NITROGEN, 0.17).move_to(mini.plant.get_center())
        green_food.layout_ok = True  # deliberate nitrogen token inside the labelled crab at the end
        arrow = CurvedArrow(mini.plant.get_center() + RIGHT * 0.3, mini.crab.get_center() + LEFT * 0.4,
                            angle=-0.28, color=NITROGEN, stroke_width=7)
        self.play(FadeOut(VGroup(soil, root, microbes, gas)), FadeIn(mini), FadeIn(green_food), run_time=1.0)
        self.play(Create(arrow), green_food.animate.move_to(mini.crab.get_center() + LEFT * .55 + DOWN * .12), run_time=1.7)
        self.finish()


class S06Return(SpokenScene):
    def construct(self):
        mud = RoundedRectangle(width=12.0, height=5.5, corner_radius=0.3, color="#8A6B44",
                               fill_color="#40382F", fill_opacity=0.95).move_to([0, -0.15, 0])
        mud.layout_ok = True
        decomp = microbe_shape("DECOMPOSERS", NITROGEN, 1.15).move_to([-3.7, -0.4, 0])
        waste = chip("WASTE", NITROGEN, size=26).move_to([-5.3, 1.45, 0])
        dead = leaf_shape(NITROGEN).scale(1.2).move_to([-2.9, 1.55, 0])
        self.add(mud, scope_tag("schematic"))
        self.play(FadeIn(waste), FadeIn(dead), FadeIn(decomp), run_time=1.2)
        self.play(waste.animate.move_to(decomp.get_center() + UP * .8),
                  dead.animate.move_to(decomp.get_center() + RIGHT * 2.7), run_time=1.5)
        bob(decomp, amp=.035, speed=1.2)
        self.at("return their nitrogen")
        ammonium = chip("AMMONIUM", NITROGEN, size=28).move_to([-3.7, -1.65, 0])
        self.play(FadeOut(waste), FadeOut(dead), FadeIn(ammonium), run_time=1.1)
        self.at("In wet soil")
        wet = RoundedRectangle(width=4.6, height=3.4, corner_radius=0.25, color=WATER,
                               fill_color="#174D68", fill_opacity=0.45).move_to([3.6, -0.45, 0])
        low = T("LOW OXYGEN", 30, WATER, weight=BOLD).move_to([3.6, 0.95, 0])
        bact = microbe_shape("BACTERIA", NITROGEN, 0.95).move_to([3.9, -1.0, 0])
        nitrate = chip("NITRATE", NITROGEN, size=28).move_to([-0.1, -0.15, 0])
        self.play(FadeIn(wet), FadeIn(low), FadeIn(bact), FadeIn(nitrate), run_time=1.3)
        bob(bact, amp=.035, speed=1.35)
        self.at("change nitrate back")
        self.play(nitrate.animate.move_to([3.1, 0.05, 0]), run_time=0.8)
        gas = chip("NITROGEN GAS", NITROGEN, size=28).move_to(nitrate)
        self.play(ReplacementTransform(nitrate, gas), run_time=1.0)
        self.at("returns to the air")
        self.play(gas.animate.move_to([3.1, 2.5, 0]), run_time=1.8)
        self.finish()


class S07Predict(SpokenScene):
    QUESTION = "After respiration, where does the crab's carbon go next?"
    OPTIONS = ["AIR", "WATER", "SOIL"]

    def construct(self):
        b = predict_backdrop()
        self.add(b)
        carbon = b[3]
        carbon.layout_ok = True  # deliberate carbon token inside the labelled crab
        self.play(carbon.animate.scale(1.6), run_time=0.8)
        self.at("When the crab respires")
        q = question_card(self.QUESTION, self.OPTIONS, y=3.2, chips_at=[4.75, 0.0, 0],
                          left=-6.2, max_w=7.6, size=30)
        self.play(FadeIn(q.question), run_time=0.7)
        self.play(FadeIn(q.chips), run_time=1.1)
        self.at("Hold your answer")
        pulse(carbon, base=2, amp=5, speed=2.2)
        self.wait(1.3)
        self.finish()


class S08Pause(PredictPause):
    QUESTION = S07Predict.QUESTION
    OPTIONS = S07Predict.OPTIONS
    CHIPS_AT = [4.75, 0.0, 0]
    CARD = {"y": 3.2, "left": -6.2, "max_w": 7.6, "size": 30}
    RING_AT = (6.05, -3.05, 0)
    SECONDS = 4.5

    def backdrop(self):
        b = predict_backdrop()
        b[3].layout_ok = True  # deliberate carbon token inside the labelled crab
        pulse(b[3], base=2, amp=5, speed=2.2)
        return b


class S09Reveal(SpokenScene):
    def construct(self):
        b = predict_backdrop()
        b[3].layout_ok = True  # deliberate carbon token inside the labelled crab
        b[4].move_to([5.75, -3.3, 0])  # keep the scope tag clear of the bottom caption
        self.add(b)
        water_lab = chip("WATER", WATER, size=34).move_to([4.5, 0.0, 0])
        self.play(FadeIn(water_lab), Indicate(b[0], color=WATER), run_time=1.1)
        self.at("carbon dioxide")
        co2 = chip("CARBON DIOXIDE", CARBON, size=28).move_to([3.0, -1.0, 0])
        self.play(Transform(b[3], co2), run_time=1.2)
        self.at("may later enter algae")
        algae = plant_shape(0.65).move_to([-4.5, -1.3, 0])
        air = T("AIR", 30, TEXT, weight=BOLD).move_to([0.0, 2.45, 0])
        downstream = T("DOWNSTREAM", 28, WATER, weight=BOLD).move_to([4.7, -2.25, 0])
        self.play(FadeIn(algae), FadeIn(air), FadeIn(downstream), FadeOut(water_lab), run_time=0.8)
        arrows = VGroup(DashedLine(co2.get_left(), algae.get_right() + RIGHT * .12, color=CARBON, stroke_width=4),
                        DashedLine(co2.get_top(), air.get_bottom() + DOWN * .12, color=CARBON, stroke_width=4),
                        DashedLine(co2.get_right(), downstream.get_left() + LEFT * .12, color=CARBON, stroke_width=4))
        poss = VGroup(T("possible", 24, CARBON).move_to([-2.9, -1.75, 0]),
                      T("possible", 24, CARBON).move_to([-1.0, 1.65, 0]),
                      T("possible", 24, CARBON).move_to([5.2, -1.65, 0]))
        self.play(LaggedStart(*[Create(a) for a in arrows], lag_ratio=0.25), run_time=1.8)
        self.play(FadeIn(poss), run_time=0.7)
        self.at("A cycle is")
        rule = caption("A network of possible routes — not one repeated track.", color=GOLD)
        self.play(FadeIn(rule), run_time=1.0)
        self.finish()


class S10Connections(SpokenScene):
    def construct(self):
        w = moving_water(watershed())
        self.add(w)
        runoff = VGroup(*[token(WATER).move_to([-4.0 + i * .25, 0.25 - i * .08, 0]) for i in range(4)])
        passengers = VGroup(*[token(NITROGEN).move_to([-3.9 + i * .4, 0.05, 0]) for i in range(3)])
        self.at("Blue water carries")
        self.play(VGroup(runoff, passengers).animate.move_to([-1.0, -0.55, 0]), run_time=1.8)
        self.at("Algae can hold")
        c = chip("C", CARBON, size=34).scale(.72).move_to([1.75, -1.85, 0])
        n = chip("N", NITROGEN, size=34).scale(.72).move_to([2.55, -1.85, 0])
        c.layout_ok = n.layout_ok = True  # deliberate element labels inside algae and crab silhouettes
        self.play(FadeIn(c), FadeIn(n), Indicate(w.algae, color=GREEN), run_time=1.1)
        self.at("Animals receive both")
        arrow = CurvedArrow([2.7, -2.15, 0], [4.25, -2.15, 0], angle=0.18, color=TEXT, stroke_width=7)
        self.play(Create(arrow), c.animate.move_to(w.crab.get_center() + LEFT * .38 + DOWN * .15),
                  n.animate.move_to(w.crab.get_center() + RIGHT * .38 + DOWN * .15), run_time=1.6)
        self.at("while decomposers")
        dead = leaf_shape().move_to([3.2, -0.6, 0])
        decomp = microbe_shape("DECOMPOSERS", GREEN, 0.86).move_to([-0.8, -2.35, 0])
        self.play(FadeIn(dead), FadeIn(decomp), dead.animate.move_to(decomp.get_center() + UP * .75), run_time=1.2)
        self.at("send both onward")
        self.play(c.animate.move_to([-1.5, -1.65, 0]), n.animate.move_to([-0.25, -1.65, 0]),
                  FadeOut(dead), run_time=1.6)
        self.finish()


class S10Surface(SpokenScene):
    def construct(self):
        air = Rectangle(width=13.0, height=3.2, stroke_width=0, fill_color="#132B3A",
                        fill_opacity=0.9).move_to([0, 2.0, 0])
        water = Rectangle(width=13.0, height=3.6, stroke_width=0, fill_color="#174D68",
                          fill_opacity=0.9).move_to([0, -1.55, 0])
        surface = Line([-6.5, 0.25, 0], [6.5, 0.25, 0], color=WATER, stroke_width=8)
        pulse(surface, base=8, amp=2, speed=1.25)
        down = Arrow([-1.4, 2.0, 0], [-1.4, -1.6, 0], color=CARBON, stroke_width=8)
        up = Arrow([1.4, -1.6, 0], [1.4, 2.0, 0], color=CARBON, stroke_width=8)
        co2a = chip("CARBON DIOXIDE", CARBON, size=28).move_to([-3.6, 1.7, 0])
        co2w = chip("CARBON DIOXIDE", CARBON, size=28).move_to([3.6, -1.55, 0])
        self.add(air, water, surface, scope_tag("schematic"), co2a)
        self.play(Create(down), co2a.animate.move_to([-3.6, -1.35, 0]), run_time=2.0)
        self.at("comes back out")
        self.play(FadeIn(co2w), Create(up), co2w.animate.move_to([3.6, 1.55, 0]), run_time=2.0)
        self.at("Ocean absorption")
        name = T("OCEAN ABSORPTION", 30, CARBON, weight=BOLD).move_to([-3.8, 1.05, 0])
        self.play(FadeIn(name), Indicate(down, color=GOLD), run_time=1.2)
        self.at("two way exchange")
        label = caption("Direction can change", color=GOLD)
        pulse(down, base=8, amp=3, speed=1.7)
        pulse(up, base=8, amp=3, speed=1.7)
        self.play(FadeIn(label), run_time=0.8)
        self.wait(1.4)
        self.finish()


class S11Rule(SpokenScene):
    def construct(self):
        w = moving_water(watershed())
        self.add(w)
        loop = Ellipse(width=11.7, height=5.8, color=GOLD, stroke_width=7)
        self.play(Create(loop), run_time=1.5)
        self.at("processes connect")
        arrows = VGroup(
            CurvedArrow([-5.2, 1.0, 0], [0.3, -1.2, 0], angle=-0.35, color=WATER, stroke_width=6),
            CurvedArrow([-2.5, -1.8, 0], [4.3, -2.0, 0], angle=0.28, color=NITROGEN, stroke_width=6),
            CurvedArrow([4.5, -1.4, 0], [-1.2, 2.15, 0], angle=0.35, color=CARBON, stroke_width=6),
        )
        self.play(FadeOut(loop), LaggedStart(*[Create(a) for a in arrows], lag_ratio=.2), run_time=2.0)
        moving = VGroup(token(WATER).move_to([-4.8, 0.7, 0]), token(NITROGEN).move_to([-2.0, -1.65, 0]),
                        token(CARBON).move_to([4.4, -1.4, 0]))
        self.add(moving)
        self.play(moving[0].animate.move_to([-0.3, -1.0, 0]), moving[1].animate.move_to([3.8, -1.9, 0]),
                  moving[2].animate.move_to([-0.6, 1.85, 0]), run_time=2.0)
        self.at("The crab is not")
        self.play(*[FadeOut(a) for a in arrows], Indicate(w.crab, color=GOLD, scale_factor=1.35), run_time=1.2)
        self.at("temporary reservoir")
        ring = SurroundingRectangle(w.crab, color=GOLD, buff=0.18, corner_radius=0.25, stroke_width=5)
        lab = T("TEMPORARY RESERVOIR", 28, GOLD, weight=BOLD).move_to([3.65, -0.72, 0])
        self.play(Create(ring), FadeIn(lab), run_time=1.0)
        self.at("moving watershed")
        self.play(FadeOut(VGroup(ring, lab)), w.animate.set_opacity(.92), run_time=1.0)
        self.finish()


class S12End(EndCard):
    LINE = "In ecosystems, atoms move between reservoirs, and processes connect their cycles."
