"""Where the Bay's Oxygen Goes.

COLOR MAP (one concept, one colour throughout)
  ORANGE = nutrients; GREEN = algae; BLUE = dissolved oxygen
  CYAN = fresh surface water; NAVY = salty bottom water
  GOLD = underwater-grass habitat / sunlight; PURPLE = bacteria
  RED = hypoxia or harm; GREY = neutral structure and water motion

The landscape is rebuilt by ``bay_world`` in every continuing scene so its
shore, layer boundary, deep channel, and labels never drift.
"""
from bp_parts import *


ORANGE = "#F29E4C"
CYAN = "#39C6D4"
NAVY = "#173B68"
PURPLE = "#B58CD9"
NUTRIENT, ALGAE, OXYGEN, SURFACE, BOTTOM, HABITAT, BACTERIA, HYPOXIA = (
    ORANGE, GREEN, BLUE, CYAN, NAVY, GOLD, PURPLE, RED
)

LAND_X, SHORE_X, BAY_X = -6.3, -2.35, 6.25
SURFACE_Y, MIX_Y, BOTTOM_Y0 = 1.15, -0.55, -3.05


def arrow(a, b, color=TEXT, width=5, tip=0.18):
    return Arrow(a, b, buff=0.08, color=color, stroke_width=width,
                 tip_length=tip, max_tip_length_to_length_ratio=0.35)


def dots(n, color, box, seed=1, radius=0.10):
    """Deterministic markers, used as symbols rather than quantitative data."""
    x0, x1, y0, y1 = box
    rng = np.random.RandomState(seed)
    return VGroup(*[
        Dot([rng.uniform(x0, x1), rng.uniform(y0, y1), 0], radius=radius,
            color=color) for _ in range(n)
    ])


def drift(mob, speed=0.10, span=8.0):
    """Slow horizontal water motion that persists while narration lands."""
    mob._drift_left = mob.get_left()[0]

    def update(group, dt):
        group.shift(RIGHT * speed * dt)
        if group.get_left()[0] > group._drift_left + 0.45:
            group.shift(LEFT * 0.45)
    mob.add_updater(update)
    return mob


def current_field():
    """Clearly visible but quiet water motion behind each narrated scene."""
    strokes = VGroup()
    for row, y in enumerate(np.linspace(-2.7, 1.0, 6)):
        for col, x in enumerate(np.linspace(-6.0, 5.2, 6)):
            stroke = Line([x, y, 0], [x + 0.62, y, 0], color=CYAN,
                          stroke_width=4, stroke_opacity=0.50)
            stroke._base_x = x
            stroke._speed = 0.95 + 0.08 * ((row + col) % 3)

            def flow(mob, dt):
                mob.shift(RIGHT * mob._speed * dt)
                if mob.get_left()[0] > mob._base_x + 1.05:
                    mob.shift(LEFT * 1.05)
            stroke.add_updater(flow)
            strokes.add(stroke)
    strokes.set_z_index(-20)
    strokes.layout_ok = True
    return strokes


class BaySpoken(SpokenScene):
    """Spoken scene with the film's persistent moving-water field."""
    def setup(self):
        super().setup()
        self.add(current_field())


def bay_world(labels=True, split=True, dim=1.0):
    """The carried landscape at one exact scale and position."""
    land = Polygon(
        [LAND_X, BOTTOM_Y0, 0], [LAND_X, 1.75, 0], [-5.0, 1.45, 0],
        [SHORE_X, 0.80, 0], [SHORE_X, BOTTOM_Y0, 0],
        stroke_color=GREY, stroke_width=3, fill_color="#6D6044",
        fill_opacity=0.55 * dim,
    )
    surface = Rectangle(width=BAY_X - SHORE_X, height=SURFACE_Y - MIX_Y,
                        stroke_width=0, fill_color=SURFACE,
                        fill_opacity=0.24 * dim).move_to([(BAY_X + SHORE_X) / 2,
                                                         (SURFACE_Y + MIX_Y) / 2, 0])
    bottom = Rectangle(width=BAY_X - SHORE_X, height=MIX_Y - BOTTOM_Y0,
                       stroke_width=0, fill_color=BOTTOM,
                       fill_opacity=0.58 * dim).move_to([(BAY_X + SHORE_X) / 2,
                                                        (MIX_Y + BOTTOM_Y0) / 2, 0])
    bed = Polygon([SHORE_X, BOTTOM_Y0, 0], [BAY_X, BOTTOM_Y0, 0],
                  [BAY_X, -2.55, 0], [4.9, -2.72, 0], [2.0, -2.96, 0],
                  [-0.7, -2.55, 0], [SHORE_X, -1.15, 0],
                  stroke_color=GREY, stroke_width=3, fill_color="#5B5350",
                  fill_opacity=0.55 * dim)
    boundary = DashedLine([SHORE_X, MIX_Y, 0], [BAY_X, MIX_Y, 0],
                          color=CYAN, stroke_width=3, dash_length=0.18)
    if not split:
        boundary.set_opacity(0.18)
    # Background fills intentionally hold labels; exclude them from shape/text crossing checks.
    for background in (land, surface, bottom, bed):
        background.set_z_index(-30)
        background.layout_ok = True
    waves = VGroup(*[
        Line([x, y, 0], [x + 0.52, y, 0], color=TEXT, stroke_width=2,
             stroke_opacity=0.22)
        for y in (0.72, 0.22, -1.02, -1.62, -2.18)
        for x in (-1.65, 0.45, 2.55, 4.65)
    ])
    drift(waves)
    group = VGroup(land, surface, bottom, bed, boundary, waves)
    group.land, group.surface, group.bottom = land, surface, bottom
    group.bed, group.boundary, group.waves = bed, boundary, waves
    if labels:
        farm = T("farm", 28, TEXT).move_to([-4.65, 0.35, 0])
        bay = T("Chesapeake Bay", 30, TEXT, weight=BOLD).move_to([2.0, 1.62, 0])
        channel = T("deep channel", 28, TEXT).move_to([2.0, -2.45, 0])
        for label in (farm, bay, channel):
            label.layout_ok = True  # deliberately labels its own landscape region
        group.add(farm, bay, channel)
        group.farm_label, group.bay_label, group.channel_label = farm, bay, channel
    return group


def fertilizer_bag(at=(-4.75, 0.95, 0)):
    bag = Polygon([-0.55, -0.62, 0], [0.55, -0.62, 0], [0.43, 0.48, 0],
                  [0.23, 0.66, 0], [-0.23, 0.66, 0], [-0.43, 0.48, 0],
                  color=NUTRIENT, stroke_width=4, fill_color=NUTRIENT,
                  fill_opacity=0.16).move_to(at)
    label = T("fertilizer", 28, NUTRIENT, weight=BOLD).move_to(bag).shift(DOWN * 0.95)
    label.layout_ok = True
    return VGroup(bag, label)


def grass_patch(opacity=1.0):
    sand = Line([4.55, -2.62, 0], [6.05, -2.62, 0], color=GREY, stroke_width=7)
    blades = VGroup(*[
        Line([4.7 + i * 0.16, -2.60, 0],
             [4.7 + i * 0.16 + 0.05 * ((i % 3) - 1), -1.75 - 0.12 * (i % 3), 0],
             color=HABITAT, stroke_width=6)
        for i in range(9)
    ]).set_opacity(opacity)
    return VGroup(sand, blades)


def bacterium(at):
    body = RoundedRectangle(width=0.52, height=0.28, corner_radius=0.14,
                            stroke_color=BACTERIA, stroke_width=3,
                            fill_color=BACTERIA, fill_opacity=0.35).move_to(at)
    return body


def animal(name, at):
    c = chip(name, TEXT, size=28, fill_opacity=0.12).move_to(at)
    bob(c, amp=0.045, speed=1.3, seed=len(name))
    return c


def oxygen_gauge(value, center, label, radius=1.12):
    return dial(value, center=center, radius=radius, label=label, color=OXYGEN,
                fmt="{:.0f}%", scale=100, size=34)


def prediction_backdrop(surface_value=None, bottom_value=None):
    surface_value = surface_value or ValueTracker(0.78)
    bottom_value = bottom_value or ValueTracker(0.78)
    layers = VGroup(
        RoundedRectangle(width=12.2, height=2.18, corner_radius=0.16,
                         stroke_color=SURFACE, stroke_width=3,
                         fill_color=SURFACE, fill_opacity=0.18).move_to([0, 1.25, 0]),
        RoundedRectangle(width=12.2, height=2.18, corner_radius=0.16,
                         stroke_color=BOTTOM, stroke_width=3,
                         fill_color=BOTTOM, fill_opacity=0.55).move_to([0, -1.16, 0]),
    )
    layers.set_z_index(-30)
    layers.layout_ok = True
    labels = VGroup(T("fresh surface water", 30, SURFACE, weight=BOLD).move_to([-3.9, 1.9, 0]),
                    T("salty bottom water", 30, TEXT, weight=BOLD).move_to([-3.9, -0.52, 0]))
    top = oxygen_gauge(surface_value, [2.55, 1.5, 0], "surface oxygen", radius=0.72)
    low = oxygen_gauge(bottom_value, [2.55, -1.2, 0], "bottom oxygen", radius=0.85)
    return VGroup(layers, labels, top, low), surface_value, bottom_value


class S00Hook(BaySpoken):
    def construct(self):
        world = bay_world(split=False)
        bag = fertilizer_bag()
        oxygen = ValueTracker(0.28)
        gauge = oxygen_gauge(oxygen, [4.35, -1.25, 0], "bottom oxygen")
        world.farm_label.move_to([-4.65, -0.75, 0])
        world.channel_label.shift(LEFT * 0.8)
        question = T("?", 76, GOLD, weight=BOLD).move_to([-0.45, 0.18, 0])
        path1 = arrow(bag.get_right(), question.get_left(), NUTRIENT, width=6)
        path2 = DashedLine(question.get_right(), gauge.get_left(), color=GOLD,
                           stroke_width=5, dash_length=0.2)
        self.play(FadeIn(world), run_time=0.65)
        self.play(FadeIn(bag), FadeIn(gauge), run_time=0.55)
        self.at("fertilizer spread far upstream")
        self.play(GrowArrow(path1), FadeIn(question), Create(path2), run_time=0.9)
        self.play(oxygen.animate.set_value(0.33), run_time=3.4, rate_func=there_and_back)
        self.at("never grabs oxygen")
        cross = VGroup(Line([-4.98, 0.63, 0], [-4.51, 1.28, 0], color=HYPOXIA, stroke_width=7),
                       Line([-4.51, 0.63, 0], [-4.98, 1.28, 0], color=HYPOXIA, stroke_width=7))
        self.play(Create(cross), run_time=0.55)
        self.play(oxygen.animate.set_value(0.23), run_time=3.0, rate_func=there_and_back)
        self.at("Follow this cross")
        self.play(Indicate(world, color=GOLD, scale_factor=1.01), run_time=1.0)
        self.at("missing oxygen comes")
        living = VGroup(Dot([-0.2, -0.05, 0], color=ALGAE, radius=0.13),
                        bacterium([1.05, -1.95, 0]))
        self.play(FadeIn(living), oxygen.animate.set_value(0.16), run_time=1.25)
        self.finish()


class S01Title(TitleCard):
    LESSON = "The Chesapeake Under Pressure"
    TITLE = "Where the Bay's Oxygen Goes"


class S02Watershed(BaySpoken):
    def construct(self):
        world = bay_world()
        outline = DashedVMobject(Polygon([-6.05, -0.85, 0], [-6.05, 2.55, 0],
                                         [-4.55, 2.95, 0], [-2.55, 2.25, 0],
                                         [-1.92, 0.82, 0], [-2.5, -1.0, 0],
                                         color=NUTRIENT, stroke_width=5), num_dashes=30)
        outline.layout_ok = True
        watershed = T("watershed", 34, NUTRIENT, weight=BOLD).move_to([-4.3, 2.35, 0])
        watershed.layout_ok = True
        self.play(FadeIn(world), Create(outline), run_time=0.8)
        self.at("watershed is all")
        self.play(FadeIn(watershed), run_time=0.45)
        rain = VGroup(*[Line([x, 2.92, 0], [x - 0.18, 2.48, 0], color=SURFACE,
                                  stroke_width=4) for x in np.linspace(-5.8, -2.8, 9)])
        runoff = arrow([-5.8, 1.30, 0], [-1.85, 0.72, 0], SURFACE, width=7)
        self.at("Rain becomes runoff")
        self.play(FadeIn(rain, shift=DOWN * 0.15), run_time=0.55)
        self.play(GrowArrow(runoff), run_time=0.8)
        sources = VGroup(*[
            chip(name, NUTRIENT, 24).move_to(pos)
            for name, pos in (("fields", [-5.3, 0.55, 0]), ("lawns", [-4.1, -0.25, 0]),
                              ("wastewater", [-4.4, -1.08, 0]), ("air", [-2.9, 2.62, 0]))
        ])
        markers = dots(12, NUTRIENT, (-5.5, -2.8, 0.35, 1.75), 22, 0.10)
        self.at("Orange nutrient markers")
        self.play(FadeOut(watershed), FadeOut(world.farm_label),
                  FadeIn(sources), FadeIn(markers), run_time=0.65)
        self.play(LaggedStart(*[d.animate.move_to([-1.6 + 0.45 * (i % 8),
                                                   0.35 - 0.15 * (i % 3), 0])
                                for i, d in enumerate(markers)], lag_ratio=0.04), run_time=1.5)
        self.at("Here nutrients mean")
        np_chips = VGroup(chip("nitrogen", NUTRIENT, 30), chip("phosphorus", NUTRIENT, 30))
        np_chips.arrange(RIGHT, buff=0.4).move_to([2.05, 2.45, 0])
        self.play(FadeOut(VGroup(sources, rain)), FadeIn(np_chips), run_time=0.65)
        self.finish()


class S03Bloom(BaySpoken):
    def construct(self):
        world = bay_world()
        grass = grass_patch()
        nutrients = dots(12, NUTRIENT, (-1.8, 4.7, -0.25, 0.75), 7)
        self.add(world, grass, nutrients)
        self.at("orange markers reach")
        self.play(nutrients.animate.shift(RIGHT * 1.05), run_time=0.8)
        algae = dots(30, ALGAE, (-1.9, 5.9, 0.12, 0.92), 9, 0.12)
        self.at("Green algae multiply")
        self.play(ReplacementTransform(nutrients, VGroup(*algae[:12])), run_time=0.8)
        self.play(LaggedStart(*[FadeIn(a, scale=0.25) for a in algae[12:]], lag_ratio=0.035), run_time=1.2)
        bloom_label = T("algal bloom", 34, ALGAE, weight=BOLD).move_to([2.1, 2.1, 0])
        self.at("thick bloom")
        self.play(FadeIn(bloom_label), world.surface.animate.set_fill(ALGAE, 0.28), run_time=0.65)
        sun = Circle(radius=0.34, color=HABITAT, fill_color=HABITAT,
                     fill_opacity=0.75).move_to([5.75, 2.75, 0])
        rays = VGroup(*[Arrow([x, 2.35, 0], [x, -1.55, 0], buff=0,
                                  color=HABITAT, stroke_width=5, tip_length=0.16)
                        for x in (4.75, 5.25, 5.75)])
        self.at("bloom shades")
        self.play(FadeIn(sun), LaggedStart(*[GrowArrow(r) for r in rays], lag_ratio=0.15), run_time=0.75)
        self.play(*[r.animate.put_start_and_end_on(r.get_start(), [r.get_end()[0], -0.05, 0])
                    for r in rays], grass[1].animate.set_opacity(0.38), run_time=0.75)
        attached = dots(8, ALGAE, (4.65, 5.95, -2.45, -1.75), 30, 0.08)
        self.at("algae also grow")
        self.play(FadeIn(attached), run_time=0.55)
        pale = dots(10, GREY, (-1.4, 4.3, 0.15, 0.75), 31, 0.10)
        self.at("dead algae begin sinking")
        self.play(FadeOut(VGroup(rays, sun, bloom_label)),
                  LaggedStart(*[p.animate.shift(DOWN * (2.35 + 0.18 * (i % 3)))
                                for i, p in enumerate(pale)], lag_ratio=0.06), run_time=1.5)
        self.finish()


class S04Decomposition(BaySpoken):
    def construct(self):
        # Enlarged bottom third, still using the established deep-channel x positions.
        water = RoundedRectangle(width=12.2, height=5.3, corner_radius=0.2,
                                 stroke_color=BOTTOM, stroke_width=3,
                                 fill_color=BOTTOM, fill_opacity=0.62).move_to([0, -0.25, 0])
        water.set_z_index(-30)
        water.layout_ok = True
        bed = Line([-6.0, -2.65, 0], [6.0, -2.65, 0], color=GREY, stroke_width=9)
        dead = dots(17, GREY, (-4.9, 1.5, -2.45, -2.0), 45, 0.12)
        bacteria = VGroup(*[bacterium([x, -2.10 + 0.18 * (i % 2), 0])
                            for i, x in enumerate((-4.2, -2.9, -1.6, -0.3, 1.0))])
        for b in bacteria:
            pulse(b, base=3, amp=1.5, speed=2.1)
        oxygen = ValueTracker(0.86)
        gauge = oxygen_gauge(oxygen, [3.95, 0.7, 0], "bottom oxygen")
        oxy_dots = dots(13, OXYGEN, (-4.8, 1.7, -1.45, 1.65), 12, 0.11)
        animals = VGroup(animal("fish", [-3.75, 0.65, 0]),
                         animal("crab", [-1.55, -0.85, 0]),
                         animal("oyster", [0.75, -1.25, 0]))
        self.play(FadeIn(water), Create(bed), FadeIn(dead), run_time=0.7)
        self.at("bacteria break down")
        self.play(FadeIn(bacteria, scale=0.5), run_time=0.65)
        self.play(*[d.animate.scale(0.55).set_opacity(0.4) for d in dead[::2]], run_time=0.75)
        decomp = T("decomposers", 34, BACTERIA, weight=BOLD).move_to([-2.45, 2.5, 0])
        self.at("Bacteria are decomposers")
        self.play(FadeIn(decomp), Indicate(bacteria, color=BACTERIA), run_time=0.75)
        self.at("They use blue")
        self.play(FadeIn(oxy_dots), FadeIn(gauge), run_time=0.55)
        self.play(LaggedStart(*[FadeOut(d, target_position=bacteria[i % len(bacteria)].get_center())
                                for i, d in enumerate(oxy_dots[:8])], lag_ratio=0.08),
                  oxygen.animate.set_value(0.42), run_time=1.55)
        definition = T("oxygen gas mixed into water", 30, OXYGEN).move_to([-2.6, 1.65, 0])
        self.at("Dissolved oxygen is")
        self.play(FadeOut(decomp), FadeIn(definition), run_time=0.55)
        self.at("Fish crabs")
        self.play(FadeOut(definition), FadeIn(animals), run_time=0.75)
        self.finish()


class S05Predict(BaySpoken):
    def construct(self):
        backdrop, surface_o2, bottom_o2 = prediction_backdrop()
        self.play(FadeIn(backdrop[0]), run_time=0.65)
        self.at("split the bay")
        self.play(FadeIn(backdrop[1]), run_time=0.45)
        self.at("Both begin with oxygen")
        self.play(FadeIn(VGroup(backdrop[2], backdrop[3])), run_time=0.75)
        # Gentle equal motion demonstrates that neither answer has been revealed.
        self.play(surface_o2.animate.set_value(0.81), bottom_o2.animate.set_value(0.81), run_time=0.5)
        self.play(surface_o2.animate.set_value(0.78), bottom_o2.animate.set_value(0.78), run_time=0.5)
        self.at("which oxygen gauge")
        q = question_card("Which gauge falls first?", y=-3.35, size=34, max_w=10.5)
        self.play(FadeIn(q.question), run_time=0.55)
        self.finish()


class S06Pause(PredictPause):
    QUESTION = "Which gauge falls first?"
    SECONDS = 4.5
    CARD = {"y": -3.35, "size": 34, "max_w": 10.5}
    RING_AT = (6.0, -3.25, 0)

    def backdrop(self):
        return prediction_backdrop()[0]


class S07Layers(BaySpoken):
    def construct(self):
        backdrop, surface_o2, bottom_o2 = prediction_backdrop()
        self.add(backdrop)
        fish = animal("fish", [-3.25, -1.25, 0])
        self.add(fish)
        self.at("bottom gauge falls")
        self.play(bottom_o2.animate.set_value(0.24), run_time=1.35)
        self.at("Fresh river water")
        self.play(Indicate(backdrop[0][0], color=SURFACE, scale_factor=1.01), run_time=0.7)
        self.at("boundary slows mixing")
        boundary = DashedLine([-5.9, 0.03, 0], [5.9, 0.03, 0], color=GOLD,
                              stroke_width=7, dash_length=0.2)
        self.play(Create(boundary), run_time=0.7)
        air = T("air", 30, TEXT, weight=BOLD).move_to([5.0, 3.25, 0])
        incoming = arrow([5.0, 2.95, 0], [5.0, 1.75, 0], OXYGEN, width=7)
        bend = CurvedArrow([5.0, 1.55, 0], [4.0, 0.85, 0], angle=-0.65,
                           color=OXYGEN, stroke_width=6, tip_length=0.2)
        self.at("Surface water still exchanges")
        self.play(FadeIn(air), GrowArrow(incoming), Create(bend),
                  surface_o2.animate.set_value(0.88), run_time=1.1)
        bacteria = VGroup(*[bacterium([x, -2.0, 0]) for x in (-4.8, -3.9, -3.0)])
        for b in bacteria:
            pulse(b, base=3, amp=1.4, speed=2)
        self.at("decomposition keeps using")
        self.play(FadeIn(bacteria), bottom_o2.animate.set_value(0.10), run_time=1.35)
        self.at("Water this low")
        hypoxia = T("hypoxia", 42, HYPOXIA, weight=BOLD).move_to([-1.1, -1.45, 0])
        self.play(FadeIn(hypoxia), fish.animate.move_to([-3.2, 1.15, 0]), run_time=1.0)
        self.finish()


class S08Season(BaySpoken):
    def construct(self):
        world = bay_world(labels=False)
        world.scale(0.88, about_point=[0, -3.05, 0]).shift(DOWN * 0.2)
        winter_x, spring_x, summer_x = -4.8, -0.4, 4.4
        strip = Line([-5.7, 2.75, 0], [5.7, 2.75, 0], color=GREY, stroke_width=5)
        seasons = VGroup(T("winter", 30, SURFACE).move_to([winter_x, 3.18, 0]),
                         T("spring", 30, NUTRIENT).move_to([spring_x, 3.18, 0]),
                         T("summer", 30, HABITAT).move_to([summer_x, 3.18, 0]))
        marks = VGroup(*[Line([x, 2.6, 0], [x, 2.9, 0], color=GREY, stroke_width=4)
                         for x in (winter_x, spring_x, summer_x)])
        oxygen = ValueTracker(0.55)
        gauge = oxygen_gauge(oxygen, [3.9, -1.15, 0], "bottom oxygen")
        bacteria = VGroup(*[bacterium([x, -2.35, 0]) for x in (-0.8, 0.2, 1.2)])
        for b in bacteria:
            pulse(b, base=3, amp=1.8, speed=3.2)
        self.add(world, scope_tag("schematic"))
        self.play(Create(strip), FadeIn(seasons), FadeIn(marks), run_time=0.8)
        self.at("Warm water holds less")
        heat = VGroup(Circle(radius=0.33, color=HABITAT, fill_color=HABITAT,
                             fill_opacity=0.8).move_to([4.9, 1.72, 0]),
                      T("warm", 28, HABITAT).move_to([4.9, 1.15, 0]))
        self.play(FadeIn(heat), FadeIn(gauge), oxygen.animate.set_value(0.40), run_time=1.0)
        self.at("bacteria decompose faster")
        self.play(FadeIn(bacteria), LaggedStart(*[Indicate(b, color=BACTERIA) for b in bacteria],
                                                lag_ratio=0.2), run_time=1.0)
        self.at("strengthens the summer shortage")
        self.play(oxygen.animate.set_value(0.12), run_time=1.25)
        shortest = T("shortest on oxygen", 34, HYPOXIA, weight=BOLD).move_to([2.75, 1.7, 0])
        self.at("deep channel runs shortest")
        self.play(FadeOut(heat), FadeIn(shortest), Indicate(seasons[2], color=HABITAT), run_time=0.8)
        self.finish()


class S09Timing(BaySpoken):
    def construct(self):
        world = bay_world(labels=False)
        world.scale(0.82, about_point=[0, -3.05, 0]).shift(DOWN * 0.25)
        xs = [-5.2, -2.2, 0.9, 4.6]
        names = ["late winter", "spring", "early summer", "summer"]
        calendar = Line([-5.8, 2.65, 0], [5.7, 2.65, 0], color=GREY, stroke_width=5)
        labs = VGroup(*[T(n, 28, TEXT).move_to([x, 3.15, 0]) for x, n in zip(xs, names)])
        marks = VGroup(*[Line([x, 2.50, 0], [x, 2.82, 0], color=GREY, stroke_width=4) for x in xs])
        cursor = Dot([xs[0], 2.65, 0], radius=0.15, color=GOLD)
        nutrients = dots(10, NUTRIENT, (-5.7, -4.55, 0.15, 0.8), 52)
        self.add(world, scope_tag("schematic"))
        self.play(Create(calendar), FadeIn(labs), FadeIn(marks), FadeIn(cursor), run_time=0.75)
        self.at("chain also has a delay")
        delay = arrow([-5.0, 2.05, 0], [4.4, 2.05, 0], GOLD, width=5)
        self.play(GrowArrow(delay), run_time=1.0)
        self.at("nitrogen arrives")
        self.play(FadeIn(nutrients), cursor.animate.move_to([xs[1], 2.65, 0]), run_time=1.1)
        algae = dots(18, ALGAE, (-1.6, 3.5, 0.05, 0.75), 53, 0.11)
        self.at("Algae grow die")
        self.play(ReplacementTransform(nutrients, algae), cursor.animate.move_to([xs[2], 2.65, 0]), run_time=1.1)
        self.play(LaggedStart(*[a.animate.set_color(GREY).shift(DOWN * (1.8 + 0.14 * (i % 3)))
                                for i, a in enumerate(algae)], lag_ratio=0.04), run_time=1.2)
        bacteria = VGroup(*[bacterium([x, -2.35, 0]) for x in (-0.3, 0.7, 1.7)])
        oxygen = ValueTracker(0.58)
        gauge = oxygen_gauge(oxygen, [4.2, -1.15, 0], "bottom oxygen")
        self.at("Decomposition can continue")
        self.play(FadeIn(bacteria), FadeIn(gauge), cursor.animate.move_to([xs[3], 2.65, 0]),
                  oxygen.animate.set_value(0.16), run_time=1.5)
        forecast = T("spring input → summer hypoxia", 32, GOLD, weight=BOLD).move_to([0.8, 1.45, 0])
        self.at("scientists use spring")
        self.play(FadeIn(forecast), run_time=0.65)
        self.finish()


class S10Chain(BaySpoken):
    def construct(self):
        layers = VGroup(Rectangle(width=13.0, height=2.0, fill_color=SURFACE,
                                  fill_opacity=0.12, stroke_width=0).move_to([0, 1.4, 0]),
                        Rectangle(width=13.0, height=2.7, fill_color=BOTTOM,
                                  fill_opacity=0.48, stroke_width=0).move_to([0, -1.0, 0]))
        layers.set_z_index(-30)
        layers.layout_ok = True
        boundary = DashedLine([-6.2, 0.25, 0], [6.2, 0.25, 0], color=CYAN,
                              stroke_width=3, dash_length=0.18)
        title = T("eutrophication", 42, GOLD, weight=BOLD).move_to([0, 3.18, 0])
        nodes = VGroup(chip("nutrients", NUTRIENT, 28), chip("algal bloom", ALGAE, 28),
                       chip("dead algae", GREY, 28), chip("bacteria", BACTERIA, 28),
                       chip("oxygen falls", OXYGEN, 28))
        nodes.arrange(RIGHT, buff=0.38).move_to([0, 0.75, 0])
        arrows = VGroup(*[arrow(nodes[i].get_right(), nodes[i + 1].get_left(),
                                [NUTRIENT, ALGAE, GREY, BACTERIA][i], width=5, tip=0.15)
                         for i in range(4)])
        self.add(layers, boundary)
        self.at("process is eutrophication")
        self.play(FadeIn(title), run_time=0.55)
        self.at("Nutrient enrichment")
        self.play(FadeIn(nodes[0]), run_time=0.4)
        self.play(LaggedStart(*[Succession(GrowArrow(arrows[i]), FadeIn(nodes[i + 1]))
                                for i in range(4)], lag_ratio=0.18), run_time=2.2)
        fish = animal("fish", [2.4, -1.3, 0])
        oyster = animal("oyster", [4.6, -1.75, 0])
        self.at("Animals that can leave")
        self.play(FadeIn(fish), fish.animate.move_to([0.6, 2.05, 0]), run_time=1.0)
        self.at("Others may sicken")
        self.play(FadeIn(oyster), oyster.animate.set_opacity(0.30), run_time=0.8)
        careful = T("nutrients start  ≠  nutrients use oxygen", 32, GOLD,
                    weight=BOLD).move_to([0, -2.75, 0])
        self.at("Follow the cause carefully")
        self.play(FadeIn(careful), run_time=0.65)
        self.at("Nutrients start the chain")
        self.play(Indicate(nodes[0], color=NUTRIENT), run_time=0.65)
        self.at("living things use")
        self.play(Indicate(nodes[3], color=BACTERIA), Indicate(nodes[4], color=OXYGEN), run_time=0.8)
        self.finish()


class S11Refine(BaySpoken):
    def construct(self):
        world = bay_world(labels=False)
        grass = grass_patch()
        bloom = dots(25, ALGAE, (-1.8, 5.8, 0.15, 0.88), 70, 0.11)
        self.add(world, grass, bloom)
        self.at("not the only effect")
        split = T("two harms", 38, GOLD, weight=BOLD).move_to([2.0, 2.45, 0])
        self.play(FadeIn(split), run_time=0.5)
        sun = Circle(radius=0.32, color=HABITAT, fill_color=HABITAT,
                     fill_opacity=0.8).move_to([5.65, 3.05, 0])
        light_path = arrow([5.45, 2.65, 0], [5.1, -1.55, 0], HABITAT, width=6)
        sink_path = arrow([1.35, 0.05, 0], [1.35, -1.85, 0], GREY, width=6)
        self.at("block sunlight")
        self.play(FadeIn(sun), GrowArrow(light_path), run_time=0.75)
        block = Line([4.72, 0.98, 0], [5.55, 0.98, 0], color=HYPOXIA, stroke_width=9)
        self.play(Create(block), grass[1].animate.set_opacity(0.30), run_time=0.65)
        habitat = T("weaker grass habitat", 30, HABITAT, weight=BOLD).move_to([4.3, -3.28, 0])
        self.at("weaken underwater grass")
        self.play(FadeIn(habitat), run_time=0.55)
        self.at("second harm")
        self.play(GrowArrow(sink_path), run_time=0.75)
        low = T("low bottom oxygen", 30, OXYGEN, weight=BOLD).move_to([1.35, -2.15, 0])
        self.play(FadeIn(low), run_time=0.45)
        weather = VGroup(T("wind", 28, TEXT), T("rain", 28, SURFACE)).arrange(RIGHT, buff=0.45)
        weather.move_to([-4.5, 2.65, 0])
        self.at("Weather changes the outcome")
        self.play(FadeIn(weather), weather.animate.shift(RIGHT * 0.35), run_time=0.9)
        reduce = T("people can reduce nutrient inputs", 30, NUTRIENT,
                   weight=BOLD).move_to([-2.95, 3.2, 0])  # own row above the land and above "two harms"
        self.at("human nutrient inputs remain")
        self.play(FadeOut(weather), FadeIn(reduce), run_time=0.65)
        self.finish()


class S12End(EndCard):
    LINE = "Extra nutrients feed algae; bacteria use oxygen while poor mixing limits replacement."
