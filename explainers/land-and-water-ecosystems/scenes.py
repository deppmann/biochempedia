"""Two Sides of Every Ecosystem — Biochemistrypedia grade 7 explainer.

COLOR MAP (fixed for the whole film)
  GREEN  living things / biotic factors
  GOLD   nonliving conditions / sunlight / climate
  BLUE   fresh water
  TEAL   mixed estuary water
  PURPLE salt water
  RED    oysters
  TEXT   labels

The two carried pictures are built only by ``virginia_world`` and ``forest_world``.
Every scene that continues one of them calls the same builder, so its landmarks do
not drift between cuts.
"""
from bp_parts import *

PURPLE = "#A98AE8"
BROWN = "#7A5A3A"


def water_motion(water, amp=0.085, speed=1.5):
    """A gentle vertical current; intended for a grouped water surface."""
    water._flow_t = 0.0
    base = water.get_center().copy()

    def drift(mob, dt):
        mob._flow_t += dt
        mob.move_to(base + UP * amp * np.sin(speed * mob._flow_t))
    water.add_updater(drift)
    return water


def sway(mob, angle=0.025, speed=1.3, seed=0.0):
    mob._sway_t = seed
    mob._last_angle = 0.0

    def move(m, dt):
        m._sway_t += dt
        new = angle * np.sin(speed * m._sway_t)
        m.rotate(new - m._last_angle, about_point=m.get_bottom())
        m._last_angle = new
    mob.add_updater(move)
    return mob


def tree(x, ground=-1.55, scale=1.0):
    trunk = RoundedRectangle(corner_radius=0.08, width=0.28 * scale, height=1.45 * scale,
                             stroke_width=0, fill_color=BROWN, fill_opacity=1)
    trunk.move_to([x, ground + 0.72 * scale, 0])
    crown = VGroup(*[
        Circle(radius=r * scale, stroke_width=2, stroke_color=GREEN,
               fill_color=GREEN, fill_opacity=0.72).move_to([x + dx * scale, ground + dy * scale, 0])
        for dx, dy, r in ((-0.38, 1.45, .55), (.32, 1.48, .62), (0, 1.88, .66))
    ])
    return VGroup(trunk, crown)


def little_plant(x, y=-1.72, scale=1.0):
    stem = Line([x, y, 0], [x, y + .58 * scale, 0], color=GREEN, stroke_width=5)
    leaves = VGroup(
        Ellipse(width=.46 * scale, height=.20 * scale, color=GREEN, fill_color=GREEN,
                fill_opacity=.85).rotate(.35).move_to([x - .2 * scale, y + .37 * scale, 0]),
        Ellipse(width=.46 * scale, height=.20 * scale, color=GREEN, fill_color=GREEN,
                fill_opacity=.85).rotate(-.35).move_to([x + .2 * scale, y + .5 * scale, 0]),
    )
    return VGroup(stem, leaves)


def oyster_reef(x=3.35, y=-1.25, scale=1.0, opacity=1.0):
    shells = VGroup(*[
        Ellipse(width=.62 * scale, height=.40 * scale, color=RED, stroke_width=3,
                fill_color=RED, fill_opacity=.55 * opacity).move_to([x + dx * scale, y + dy * scale, 0])
        for dx, dy in ((-.6, -.08), (0, .18), (.58, -.07), (-.05, -.30))
    ])
    shells.set_opacity(opacity)
    return shells


def virginia_world(dim=1.0, salt_boundary=1.4):
    """The film's fixed Virginia cross-section, left-to-right mountain to ocean."""
    sky = Rectangle(width=13.2, height=6.1, stroke_width=0, fill_color="#14243A",
                    fill_opacity=.40 * dim).move_to([0, .35, 0])
    land = Polygon([-6.6, -1.55, 0], [-6.6, .55, 0], [-5.45, 2.05, 0],
                   [-4.3, .78, 0], [-2.8, -.18, 0], [-1.25, -.72, 0],
                   [0.35, -1.0, 0], [6.6, -1.0, 0], [6.6, -2.55, 0],
                   [-6.6, -2.55, 0], stroke_color=GREY, stroke_width=3,
                   fill_color="#314235", fill_opacity=.9 * dim)
    # Water shares one fixed channel. Its three sections meet at fixed landmarks.
    fresh = Polygon([-5.7, .42, 0], [-4.35, -.35, 0], [-2.5, -.88, 0],
                    [salt_boundary, -1.05, 0], [salt_boundary, -1.82, 0],
                    [-2.5, -1.62, 0], [-4.5, -.88, 0], [-5.7, -.05, 0],
                    stroke_width=0, fill_color=BLUE, fill_opacity=.78 * dim)
    mixed = Rectangle(width=max(2.3, 3.9 - salt_boundary), height=.82, stroke_width=0,
                      fill_color=TEAL, fill_opacity=.78 * dim).move_to([(salt_boundary + 3.9) / 2, -1.42, 0])
    salty = Rectangle(width=2.7, height=.82, stroke_width=0, fill_color=PURPLE,
                      fill_opacity=.75 * dim).move_to([5.25, -1.42, 0])
    water = VGroup(fresh, mixed, salty)
    water_motion(water)
    trees = VGroup(tree(-5.72, -.2, .70), tree(-4.92, -.45, .64), tree(-4.18, -.66, .58))
    richmond_text = T("Richmond", 28).next_to([-1.65, -.70, 0], UP, buff=.12)
    # This place label intentionally sits on its mapped landscape region.
    richmond_text.layout_ok = True
    richmond = VGroup(Dot([-1.65, -.78, 0], radius=.10, color=TEXT), richmond_text)
    bay = T("Chesapeake Bay", 28, TEAL).move_to([2.45, -2.2, 0])
    ocean = T("Atlantic", 28, PURPLE).move_to([5.35, -2.2, 0])
    landmarks = VGroup(trees, richmond, bay, ocean).set_opacity(dim)
    return VGroup(sky, land, water, landmarks)


def forest_world(canopy=1.0, rain=False, dark_soil=False):
    """The fixed forest close-up used in s03–s07."""
    sky = Rectangle(width=13.0, height=6.6, stroke_width=0, fill_color="#16283A",
                    fill_opacity=.7).move_to([0, -.05, 0])
    soil_color = "#3B2B22" if dark_soil else "#5B422E"
    soil = Rectangle(width=13.0, height=1.35, stroke_width=0, fill_color=soil_color,
                     fill_opacity=1).move_to([0, -2.25, 0])
    oaks = VGroup(tree(-4.9, -1.65, 1.65), tree(4.9, -1.65, 1.65))
    canopy_blobs = VGroup(*[
        Ellipse(width=2.25 * canopy, height=1.2, color=GREEN, fill_color=GREEN,
                fill_opacity=.82).move_to([x, 2.35 + .12 * np.sin(x), 0])
        for x in np.linspace(-5.7, 5.7, 7)
    ])
    for i, leaf in enumerate(canopy_blobs):
        sway(leaf, angle=.026, speed=1.0 + i * .06, seed=i)
    # Three light columns stop at the forest floor.
    beams = VGroup(*[
        Polygon([x - .38, 2.7, 0], [x + .38, 2.7, 0], [x + .72, -1.48, 0],
                [x - .72, -1.48, 0], stroke_width=0, fill_color=GOLD, fill_opacity=.16)
        for x in (-2.8, 0, 2.8)
    ])
    plants = VGroup(little_plant(-2.7), little_plant(0), little_plant(2.7))
    world = VGroup(sky, beams, soil, oaks, canopy_blobs, plants)
    if rain:
        drops = VGroup(*[
            Line([x, y, 0], [x - .08, y - .35, 0], color=BLUE, stroke_width=3)
            for x, y in zip(np.linspace(-5.8, 5.8, 18), [2.7, 1.8, .8] * 6)
        ])
        world.add(drops)
    world.sky, world.beams, world.soil = sky, beams, soil
    world.oaks, world.canopy, world.plants = oaks, canopy_blobs, plants
    return world


def factor_lenses():
    left = Ellipse(width=7.2, height=5.2, color=GREEN, stroke_width=6,
                   fill_color=GREEN, fill_opacity=.10).shift(LEFT * 1.75)
    right = Ellipse(width=7.2, height=5.2, color=GOLD, stroke_width=6,
                    fill_color=GOLD, fill_opacity=.10).shift(RIGHT * 1.75)
    return VGroup(left, right)


def setting_labels():
    return VGroup(
        chip("terrestrial", GREEN, 28).move_to([-4.85, 2.7, 0]),
        chip("freshwater", BLUE, 28).move_to([-2.15, 1.55, 0]),
        chip("estuary", TEAL, 28).move_to([2.0, 1.45, 0]),
        chip("marine", PURPLE, 28).move_to([5.05, 1.45, 0]),
    )


class S01Hook(SpokenScene):
    def construct(self):
        world = virginia_world()
        boat = VGroup(Polygon([-.3, 0, 0], [.3, 0, 0], [.2, -.15, 0], [-.2, -.15, 0],
                              color=TEXT, fill_color=TEXT, fill_opacity=.8),
                      Line([0, 0, 0], [0, .35, 0], color=TEXT, stroke_width=3)).move_to([-3.5, -.55, 0])
        lower = oyster_reef()
        ghost = oyster_reef(-1.6, -1.08, .7, .35)
        question = fit_text("Why oysters here—but not near Richmond?", 11.5, 40,
                            color=TEXT, font=TITLE_FONT).move_to([0, 3.25, 0])
        self.play(FadeIn(world), FadeIn(question), run_time=1.2)
        self.at("lower James River")
        self.play(FadeIn(lower, scale=.65), FadeIn(ghost),
                  boat.animate.shift(RIGHT * 2.7), run_time=3.0, rate_func=linear)
        self.at("Follow one Virginia")
        self.play(FadeOut(question), boat.animate.shift(RIGHT * 2.7), run_time=3.0, rate_func=linear)
        alive = chip("alive", GREEN, 30).move_to([-3.8, 3.0, 0])
        surroundings = chip("surroundings", GOLD, 30).move_to([3.5, 3.0, 0])
        self.at("Some clues are alive")
        self.play(FadeIn(alive, shift=DOWN * .15), Indicate(lower, color=GREEN), run_time=1.0)
        self.at("parts of the surroundings")
        self.play(FadeIn(surroundings, shift=DOWN * .15), FadeOut(ghost),
                  boat.animate.shift(RIGHT * .5), run_time=1.0)
        self.finish()


class S02Title(NarratedScene):
    def construct(self):
        world = virginia_world(dim=.32)
        title = fit_text("Two Sides of Every Ecosystem", 11.7, 50, font=TITLE_FONT).move_to([0, .35, 0])
        # The title is deliberately superimposed over the dim carried landscape.
        title.layout_ok = True
        self.add(world)
        self.play(Write(title), run_time=.7)
        lenses = factor_lenses()
        # The lenses deliberately inspect the place labels beneath them.
        world[3][2].layout_ok = True
        self.play(ReplacementTransform(title, lenses), run_time=.7)
        self.wait(.6)
        self.finish()


class S03Biotic(SpokenScene):
    def construct(self):
        world = forest_world()
        lenses = factor_lenses()[0]
        log = RoundedRectangle(corner_radius=.18, width=2.5, height=.52, color=BROWN,
                               fill_color=BROWN, fill_opacity=.9).rotate(-.10).move_to([2.35, -1.43, 0])
        deer = VGroup(Ellipse(width=1.2, height=.65, color=GREEN, fill_color=GREEN, fill_opacity=.7),
                      Circle(radius=.25, color=GREEN, fill_color=GREEN, fill_opacity=.7).shift(RIGHT * .75 + DOWN * .25),
                      *[Line([x, -.25, 0], [x, -.75, 0], color=GREEN, stroke_width=4) for x in (-.35, .35)])
        deer.move_to([-1.9, -1.15, 0])
        acorns = VGroup(*[Dot([-1.0 + i * .2, -1.72, 0], radius=.07, color=BROWN) for i in range(3)])
        fungi = VGroup(*[Arc(radius=.35 + i * .1, start_angle=PI, angle=PI,
                            color=GREEN, stroke_width=3).move_to([1.65 + i * .35, -1.45, 0]) for i in range(4)])
        microbes = VGroup(*[Dot([3.0 + .16 * i, -1.2 + .10 * (i % 2), 0], radius=.035, color=GREEN) for i in range(7)])
        self.play(FadeIn(world), run_time=.9)
        self.at("all living things")
        self.play(Create(lenses), FadeIn(deer), FadeIn(log), run_time=1.4)
        self.at("plants animals fungi")
        self.play(LaggedStart(Indicate(world.oaks, color=GREEN), Indicate(deer, color=GREEN),
                              FadeIn(microbes), lag_ratio=.18), run_time=2.2)
        self.at("Watch a deer")
        self.play(deer.animate.rotate(-.18, about_point=deer.get_right()), FadeIn(acorns), run_time=1.2)
        self.at("fungi spread")
        self.play(LaggedStart(*[Create(f) for f in fungi], lag_ratio=.18), run_time=1.7)
        label = chip("biotic: living", GREEN, 34).move_to([0, 3.12, 0])
        label[1].layout_ok = True  # labelled chip intentionally overlays the living canopy
        self.at("biotic factors")
        self.play(FadeIn(label, shift=DOWN * .15), lenses.animate.set_fill(opacity=.18), run_time=.8)
        self.finish()


class S04Abiotic(SpokenScene):
    def construct(self):
        world = forest_world(rain=True, dark_soil=True)
        lenses = factor_lenses()
        left_lab = chip("biotic: living", GREEN, 30).move_to([-3.65, 3.12, 0])
        left_lab[1].layout_ok = True  # labelled chip intentionally overlays the living canopy
        sun = VGroup(Circle(radius=.34, color=GOLD, fill_color=GOLD, fill_opacity=1),
                     *[Line(ORIGIN, RIGHT * .55, color=GOLD, stroke_width=4).rotate(a) for a in np.linspace(0, TAU, 8, endpoint=False)])
        sun.move_to([5.75, 2.75, 0])
        self.add(world, lenses[0], left_lab)
        self.at("climate sunlight water")
        self.play(FadeIn(sun, scale=.7), FadeIn(world[-1]), run_time=1.4)
        self.at("abiotic factors")
        right_lab = chip("abiotic: nonliving", GOLD, 30).move_to([3.7, 3.12, 0])
        right_lab[1].layout_ok = True  # labelled chip intentionally overlays the canopy
        self.play(Create(lenses[1]), FadeIn(right_lab), run_time=1.1)
        self.at("Rain darkens")
        self.play(world.soil.animate.set_fill("#281C18"),
                  world.beams.animate.shift(RIGHT * .5), run_time=2.2)
        self.at("Both sides share")
        self.play(lenses[0].animate.shift(RIGHT * .65), lenses[1].animate.shift(LEFT * .65),
                  left_lab.animate.shift(RIGHT * .35), right_lab.animate.shift(LEFT * .35), run_time=1.5)
        self.at("changes on either side")
        self.play(Indicate(world.plants, color=GREEN), world.beams.animate.shift(LEFT * .5), run_time=1.3)
        self.finish()


class S05Predict(SpokenScene):
    def construct(self):
        world = forest_world()
        self.add(world)
        self.at("canopy grows thicker")
        new_leaves = VGroup(*[
            Ellipse(width=2.2, height=1.1, color=GREEN, fill_color=GREEN, fill_opacity=.9)
            .move_to([x, 1.75 + .1 * np.cos(x), 0]) for x in np.linspace(-5.4, 5.4, 6)
        ])
        for i, leaf in enumerate(new_leaves):
            sway(leaf, angle=.028, speed=1.1, seed=i)
        self.play(LaggedStart(*[FadeIn(l, shift=DOWN * .2) for l in new_leaves], lag_ratio=.10), run_time=2.3)
        self.at("Less sunlight")
        narrow = VGroup(*[b.copy().scale(.42, about_edge=UP) for b in world.beams])
        self.play(ReplacementTransform(world.beams, narrow), run_time=1.4)
        self.at("What do you predict")
        q = question_card("What happens below?", y=-3.12, size=38)
        self.play(FadeIn(q.question, shift=UP * .15), Indicate(world.plants, color=GREEN), run_time=1.2)
        self.finish()


class S06Pause(NarratedScene):
    def construct(self):
        world = forest_world()
        cover = VGroup(*[
            Ellipse(width=2.2, height=1.1, color=GREEN, fill_color=GREEN, fill_opacity=.9)
            .move_to([x, 1.75 + .1 * np.cos(x), 0]) for x in np.linspace(-5.4, 5.4, 6)
        ])
        for i, leaf in enumerate(cover):
            sway(leaf, angle=.028, speed=1.1, seed=i)
        q = question_card("What happens below?", y=-3.12, size=38)
        ring, run = countdown(4.5, center=[6.05, -3.05, 0])
        self.add(world, cover, q, ring)
        self.play(run)
        self.finish()


class S07Reveal(SpokenScene):
    def construct(self):
        world = forest_world()
        cover = VGroup(*[
            Ellipse(width=2.2, height=1.1, color=GREEN, fill_color=GREEN, fill_opacity=.9)
            .move_to([x, 1.75 + .1 * np.cos(x), 0]) for x in np.linspace(-5.4, 5.4, 6)
        ])
        for i, leaf in enumerate(cover):
            sway(leaf, angle=.045, speed=1.15, seed=i)
        bob(world.plants[1], amp=.065, speed=1.1)
        # Broad, slow light shimmer keeps the limiting condition visibly active
        # while the opening sentences land.
        water_motion(world.beams, amp=.16, speed=.9)
        self.add(world, cover)
        self.at("grow poorly or disappear")
        self.play(world.plants[0].animate.scale(.35).set_opacity(.2),
                  world.plants[2].animate.scale(.35).set_opacity(.2), run_time=1.7)
        self.at("Light is one condition")
        self.play(Indicate(world.plants[1], color=GOLD), run_time=1.0)
        # Transform only the lower half: the forest remains recognisable above the water cutaway.
        water = Rectangle(width=13.0, height=3.7, stroke_width=0, fill_color=TEAL,
                          fill_opacity=.72).move_to([0, -.85, 0])
        floor = Rectangle(width=13.0, height=.7, stroke_width=0, fill_color=BROWN,
                          fill_opacity=.9).move_to([0, -2.42, 0])
        mud = VGroup(*[Dot([x, y, 0], radius=.06, color=GOLD).set_opacity(.75)
                       for x, y in zip(np.linspace(-5.7, 5.7, 26), [-.1, -.7, -1.3, -1.8] * 7)])
        water_motion(mud, amp=.07, speed=1.0)
        rays = VGroup(*[Line([x, 1.0, 0], [x, -.25 - .25 * i, 0], color=GOLD,
                             stroke_width=max(2, 7 - i), stroke_opacity=.75 - .12 * i)
                        for i, x in enumerate((-3.3, -1.1, 1.1, 3.3))])
        self.at("Deep or muddy water")
        self.play(FadeOut(VGroup(world.soil, world.plants)), FadeIn(water), FadeIn(floor), run_time=1.5)
        self.at("block light too")
        self.play(LaggedStart(FadeIn(mud), *[Create(r) for r in rays], lag_ratio=.15), run_time=1.8)
        faint = VGroup(little_plant(-2.3, -2.2, .7), little_plant(1.8, -2.2, .7)).set_opacity(.18)
        self.at("few plants grow")
        self.play(FadeIn(faint), run_time=.8)
        self.add(scope_tag("schematic"))
        self.finish()


class S08Climate(SpokenScene):
    def construct(self):
        world = virginia_world()
        self.add(world)
        ribbon = RoundedRectangle(corner_radius=.18, width=12.0, height=.42, color=GOLD,
                                  fill_color=GOLD, fill_opacity=.28).move_to([0, 2.45, 0])
        label = T("climate: usual pattern over many years", 30, GOLD).move_to(ribbon)
        self.at("usual pattern")
        self.play(GrowFromCenter(ribbon), FadeIn(label), run_time=1.3)
        earth = Circle(radius=.58, color=BLUE, fill_color=BLUE, fill_opacity=.45).move_to([1.8, .65, 0])
        axis = Line(earth.get_center() + DOWN * .8 + LEFT * .22,
                    earth.get_center() + UP * .8 + RIGHT * .22, color=TEXT, stroke_width=4)
        sun = Circle(radius=.42, color=GOLD, fill_color=GOLD, fill_opacity=1).move_to([-1.2, .9, 0])
        orbit = Arc(radius=2.0, start_angle=-.25, angle=1.0, color=GREY, stroke_width=3).move_to([-.2, .35, 0])
        beams = VGroup(*[Arrow(sun.get_right() + UP * y, earth.get_left() + UP * y * .45,
                              buff=.08, color=GOLD, stroke_width=4, tip_length=.15) for y in (-.35, 0, .35)])
        self.at("Earth's tilt")
        self.play(FadeIn(sun), Create(orbit), FadeIn(earth), Create(axis), run_time=1.5)
        self.at("changes sunlight angle")
        self.play(LaggedStart(*[GrowArrow(a) for a in beams], lag_ratio=.12),
                  earth.animate.move_to([2.4, .15, 0]), run_time=2.2)
        drivers = VGroup(*[chip(t, GOLD, 26) for t in ("latitude", "elevation", "land shape", "human actions")])
        drivers.arrange(RIGHT, buff=.25).move_to([0, 3.15, 0])
        self.at("Latitude elevation")
        self.play(FadeOut(VGroup(ribbon, label)), LaggedStart(*[FadeIn(c) for c in drivers], lag_ratio=.12), run_time=1.7)
        rain = VGroup(*[Line([x, .3, 0], [x - .06, -.15, 0], color=BLUE, stroke_width=3) for x in np.linspace(-5.8, 5.8, 14)])
        snow = VGroup(*[Circle(radius=.055, stroke_width=0, fill_color=TEXT, fill_opacity=1)
                        .move_to([x, .2 + .25 * (i % 2), 0]) for i, x in enumerate(np.linspace(-5.5, 5.5, 12))])
        self.at("also shape climate")
        self.play(FadeIn(rain), run_time=.7)
        self.play(ReplacementTransform(rain, snow), run_time=.8)
        self.play(FadeOut(snow), world[1].animate.stretch(1.08, 1, about_edge=DOWN), run_time=.8)
        self.at("abiotic side")
        self.play(Indicate(drivers, color=GOLD), run_time=.8)
        self.add(scope_tag("orbit schematic"))
        self.finish()


class S09Settings(SpokenScene):
    def construct(self):
        world = virginia_world()
        labels = setting_labels()
        self.add(world)
        self.at("forest is a terrestrial")
        self.play(FadeIn(labels[0], shift=DOWN * .15), Indicate(world[3][0], color=GREEN), run_time=1.2)
        self.at("mountain stream is freshwater")
        self.play(FadeIn(labels[1], shift=DOWN * .15), run_time=1.0)
        self.at("Ocean water is marine")
        self.play(FadeIn(labels[3], shift=DOWN * .15), run_time=1.0)
        salt = VGroup(*[Dot([x, -1.35 + .16 * (i % 3), 0], radius=.055, color=PURPLE)
                        for i, x in enumerate(np.linspace(1.0, 6.0, 18))])
        self.play(LaggedStart(*[FadeIn(d) for d in salt], lag_ratio=.03), run_time=1.0)
        self.at("Between them an estuary")
        self.play(FadeIn(labels[2], shift=DOWN * .15), run_time=1.0)
        fresh_arrow = Arrow([-2.6, -.65, 0], [1.1, -.95, 0], color=BLUE, stroke_width=7, tip_length=.22)
        tide_arrow = Arrow([5.7, -.72, 0], [2.9, -.72, 0], color=PURPLE, stroke_width=7, tip_length=.22)
        self.at("mixes fresh river water")
        self.play(GrowArrow(fresh_arrow), run_time=1.2)
        self.at("salty ocean water")
        self.play(GrowArrow(tide_arrow), labels[2].animate.set_fill(TEAL, opacity=.28), run_time=1.1)
        self.finish()


class S10Rule(SpokenScene):
    def construct(self):
        world = virginia_world()
        labels = setting_labels()
        self.add(world, labels)
        self.at("not empty containers")
        self.play(FadeOut(labels), run_time=.8)
        tree_icon = little_plant(-4.8, -.05, 1.35)
        insect = VGroup(Ellipse(width=.55, height=.28, color=GREEN, fill_color=GREEN, fill_opacity=.8),
                        *[Line(ORIGIN, [.35 * np.cos(a), .35 * np.sin(a), 0], color=GREEN, stroke_width=3)
                          for a in (.8, 2.3, 3.9, 5.4)]).move_to([-2.7, -.8, 0])
        oyster = oyster_reef(2.5, -1.0, .85)
        self.at("Organisms must handle")
        self.play(FadeIn(tree_icon), FadeIn(insect), FadeIn(oyster), run_time=1.4)
        conditions = VGroup(*[Arrow([x, 2.3, 0], target, buff=.15, color=GOLD,
                                    stroke_width=5, tip_length=.18)
                              for x, target in ((-5.3, tree_icon.get_top()), (-2.7, insect.get_top()), (2.7, oyster.get_top()))])
        interactions = VGroup(*[Arrow([x + .7, .8, 0], target, buff=.15, color=GREEN,
                                      stroke_width=5, tip_length=.18)
                                for x, target in ((-5.3, tree_icon.get_top()), (-2.7, insect.get_top()), (2.7, oyster.get_top()))])
        self.at("those conditions")
        self.play(LaggedStart(*[GrowArrow(a) for a in conditions], lag_ratio=.12), run_time=1.5)
        self.at("finding food")
        self.play(LaggedStart(*[GrowArrow(a) for a in interactions], lag_ratio=.12), run_time=1.5)
        rule = caption("Living interactions + nonliving conditions help decide what lives where.",
                       31, TEXT, y=-3.1)
        self.at("Living interactions")
        self.play(FadeIn(rule, shift=UP * .15), run_time=1.2)
        ghost = oyster_reef(-1.6, -1.0, .7, .35)
        self.at("oyster puzzle")
        self.play(FadeIn(ghost), FadeOut(ghost), Indicate(oyster, color=RED), run_time=1.5)
        self.at("evidence along the river")
        self.play(ShowPassingFlash(Line([-5.5, -.45, 0], [5.7, -.95, 0], color=TEXT, stroke_width=8),
                                   time_width=.5), run_time=1.7)
        self.finish()


class S11Scope(SpokenScene):
    def construct(self):
        world = virginia_world()
        oyster = oyster_reef(2.8, -1.0, .9)
        boundary = DashedLine([.8, -1.82, 0], [.8, -.55, 0], color=TEAL, stroke_width=4)
        self.add(world, oyster, boundary)
        self.at("No single factor")
        self.play(boundary.animate.shift(RIGHT * .7), run_time=1.4)
        self.play(boundary.animate.shift(LEFT * .45), run_time=1.0)
        fit_box = RoundedRectangle(corner_radius=.16, width=3.0, height=1.0, color=GREEN,
                                   fill_color=GREEN, fill_opacity=.12).move_to([2.7, 1.25, 0])
        fit_text_m = T("✓  could fit", 32, GREEN).move_to(fit_box)
        self.at("suitable condition")
        self.play(FadeIn(fit_box), FadeIn(fit_text_m), run_time=1.0)
        observed = RoundedRectangle(corner_radius=.16, width=3.0, height=1.0, color=TEXT,
                                    fill_color=BG, fill_opacity=.85).move_to([2.7, 2.55, 0])
        observed_text = T("counted here?", 30).move_to(observed)
        self.at("does not prove")
        self.play(FadeIn(observed), FadeIn(observed_text), run_time=1.0)
        clue = caption("A range match is a clue—not a complete answer.", 31, GOLD, y=-3.1)
        self.at("A range match")
        self.play(FadeIn(clue, shift=UP * .15), run_time=1.0)
        self.at("Ecosystems also change")
        self.play(boundary.animate.shift(RIGHT * .8), world[2].animate.shift(UP * .06), run_time=1.8)
        self.at("next step is to test")
        self.play(FadeOut(VGroup(fit_box, fit_text_m, observed, observed_text, clue)),
                  ShowPassingFlash(Line([-4.7, -.4, 0], [4.8, -.95, 0], color=GOLD, stroke_width=8),
                                   time_width=.5), run_time=1.5)
        self.finish()


class S12End(EndCard):
    LINE = "Living interactions and nonliving conditions help decide what can live where."
