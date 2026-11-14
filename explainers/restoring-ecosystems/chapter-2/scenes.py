"""When stopping harm is not enough — chapter 2.

COLOR MAP (continued exactly from chapter 1)
  GOLD  = animals, seeds, and living starters
  RED   = harm (disease and storm)
  TEAL  = human action and intervention
  GREEN = habitat and recovery
  BLUE  = water
  GREY  = structure, outlines, and de-emphasized context

The bay is rebuilt by ``bay_world`` in every continuing scene so the waterline,
floor, plots, and seed-source landmark never drift between cuts.
"""
from bp_parts import *  # noqa: F401,F403


FLOOR_Y = -2.05
WATER_TOP = 2.25


def _drifting_water():
    """Large, gently moving water field used by every bay scene."""
    water = Rectangle(width=13.0, height=4.35, stroke_width=0,
                      fill_color=BLUE, fill_opacity=0.18).move_to([0, 0.1, 0])
    surface = VMobject(color=BLUE, stroke_width=5)
    surface._t = 0.0

    def ripple(mob, dt):
        mob._t += dt
        pts = [np.array([x, WATER_TOP + 0.08 * np.sin(1.15 * x + 1.25 * mob._t), 0])
               for x in np.linspace(-6.5, 6.5, 70)]
        mob.set_points_smoothly(pts)

    ripple(surface, 0.0)
    surface.add_updater(ripple)
    particles = VGroup()
    for i in range(11):
        d = Dot(radius=0.035 + 0.008 * (i % 3), color=TEXT).set_opacity(0.24)
        d.move_to([-5.9 + 1.05 * i, -1.45 + 0.29 * (i % 8), 0])
        d._speed = 0.09 + 0.018 * (i % 4)

        def drift(mob, dt):
            mob.shift(RIGHT * mob._speed * dt)
            if mob.get_x() > 6.2:
                mob.shift(LEFT * 12.2)

        d.add_updater(drift)
        particles.add(d)
    return VGroup(water, surface, particles)


def grass_patch(x0, x1, count, height=1.25, seed=1, color=GREEN):
    """A deterministic patch of schematic eelgrass with slow current-driven sway."""
    rng = np.random.RandomState(seed)
    blades = VGroup()
    for i, x in enumerate(np.linspace(x0, x1, count)):
        h = height * (0.66 + 0.32 * rng.rand())
        blade = VMobject(color=color, stroke_width=6)
        base = np.array([x, FLOOR_Y, 0.0])
        blade._base = base
        blade._height = h
        blade._phase = 0.55 * i + seed
        blade._t = 0.0

        def sway(mob, dt):
            mob._t += dt
            bend = 0.13 * np.sin(0.9 * mob._t + mob._phase)
            b = mob._base
            mob.set_points_smoothly([b, b + [0.03, mob._height * 0.45, 0],
                                     b + [bend, mob._height, 0]])

        sway(blade, 0.0)
        blade.add_updater(sway)
        blades.add(blade)
    return blades


def seed_source(empty=True):
    """The fixed seed-source landmark at the right edge of the bay."""
    ring = Circle(radius=0.57, color=GOLD, stroke_width=5).move_to([5.25, -0.65, 0])
    if empty:
        label = T("seed source?", 28, GOLD).next_to(ring, UP, buff=0.14)
        return VGroup(ring, label)
    seeds = VGroup(*[Dot(radius=0.085, color=GOLD) for _ in range(5)]).arrange_in_grid(2, 3, buff=0.12)
    seeds.move_to(ring)
    label = T("starter returned", 28, GOLD).next_to(ring, UP, buff=0.14).shift(LEFT * 0.4)
    return VGroup(ring, seeds, label)


def plot_outlines():
    left = DashedVMobject(Rectangle(width=2.3, height=1.55, color=TEAL, stroke_width=4), num_dashes=26)
    right = DashedVMobject(Rectangle(width=2.3, height=1.55, color=TEAL, stroke_width=4), num_dashes=26)
    left.move_to([-2.75, FLOOR_Y + 0.78, 0])
    right.move_to([1.0, FLOOR_Y + 0.78, 0])
    return VGroup(left, right)


def bay_world(grass="bare", plots=False, source=None, label=False):
    """Build the one carried bay at an invariant scale and position."""
    water = _drifting_water()
    floor = Rectangle(width=13.0, height=0.75, stroke_color=GREY, stroke_width=3,
                      fill_color=GREY, fill_opacity=0.38).move_to([0, FLOOR_Y - 0.375, 0])
    shore = Polygon([-6.5, WATER_TOP, 0], [-6.5, FLOOR_Y, 0], [-5.55, FLOOR_Y, 0],
                    [-5.85, 0.1, 0], color=GREEN, stroke_width=3,
                    fill_color=GREEN, fill_opacity=0.23)
    g = VGroup(water, floor, shore)
    g.water, g.floor, g.shore = water, floor, shore
    if grass == "full":
        g.grass = grass_patch(-5.45, 5.75, 30, 1.45, 4)
        g.add(g.grass)
    elif grass == "sparse":
        g.grass = grass_patch(-4.7, -4.15, 2, 0.8, 8)
        g.add(g.grass)
    elif grass == "plots":
        g.grass = VGroup(grass_patch(-3.7, -1.8, 7, 0.95, 11),
                         grass_patch(0.0, 1.95, 7, 0.95, 13))
        g.add(g.grass)
    elif grass == "spread":
        g.grass = VGroup(grass_patch(-5.35, -1.55, 14, 1.38, 16),
                         grass_patch(-1.25, 3.0, 15, 1.38, 18),
                         grass_patch(3.25, 5.65, 8, 1.28, 20))
        g.add(g.grass)
    if plots:
        g.plots = plot_outlines()
        g.add(g.plots)
    if source is not None:
        g.source = seed_source(empty=(source == "empty"))
        g.add(g.source)
    if label:
        g.place = T("Virginia coastal bay", 30, BLUE).move_to([-3.8, 1.65, 0])
        g.add(g.place)
    return g


def eagle_shoreline():
    """Chapter-1 shoreline vocabulary, used only for the handoff and final merge."""
    water = Rectangle(width=13.0, height=3.5, stroke_width=0, fill_color=BLUE,
                      fill_opacity=0.17).move_to([0, -0.6, 0])
    land = Polygon([-6.5, 2.7, 0], [1.2, 2.7, 0], [0.2, -2.35, 0], [-6.5, -2.35, 0],
                   color=GREEN, fill_color=GREEN, fill_opacity=0.26, stroke_width=3)
    trees = VGroup(*[Triangle(color=GREEN, fill_color=GREEN, fill_opacity=0.6).scale(0.34)
                     .move_to([-5.5 + 0.82 * i, 0.4 + 0.24 * (i % 3), 0]) for i in range(7)])
    nests = VGroup(*[VGroup(Arc(radius=0.22, start_angle=PI, angle=PI, color=GREY, stroke_width=5),
                            Dot(radius=0.09, color=GOLD), Dot(radius=0.09, color=GOLD))
                     .arrange(UP, buff=-0.07).move_to([-4.7 + 1.45 * i, -0.25 + 0.35 * (i % 2), 0])
                     for i in range(4)])
    return VGroup(water, land, trees, nests)


def boat():
    hull = Polygon([-0.75, 0.0, 0], [0.75, 0.0, 0], [0.48, -0.33, 0], [-0.48, -0.33, 0],
                   color=TEAL, fill_color=TEAL, fill_opacity=0.8, stroke_width=3)
    mast = Line([0, 0, 0], [0, 0.72, 0], color=TEAL, stroke_width=5)
    flag = Polygon([0, 0.72, 0], [0.54, 0.49, 0], [0, 0.32, 0], color=TEAL,
                   fill_color=TEAL, fill_opacity=0.7)
    return VGroup(hull, mast, flag)


def animal_icon(kind="fish", color=GOLD):
    body = Ellipse(width=0.62, height=0.3, color=color, fill_color=color, fill_opacity=0.7)
    if kind == "fish":
        tail = Triangle(color=color, fill_color=color, fill_opacity=0.7).scale(0.18).rotate(-PI / 2)
        tail.next_to(body, LEFT, buff=-0.05)
        return VGroup(body, tail)
    legs = VGroup(*[Line(ORIGIN, [0.2 * np.cos(a), 0.2 * np.sin(a), 0], color=color, stroke_width=3)
                    for a in np.linspace(PI, TAU, 5)]).move_to(body)
    return VGroup(legs, body)


def eagle_icon(color=GOLD):
    """A simple flying-bird silhouette, deliberately not anatomical."""
    wings = VGroup(Line([-0.42, 0.16, 0], [0, 0, 0], color=color, stroke_width=7),
                   Line([0, 0, 0], [0.42, 0.16, 0], color=color, stroke_width=7))
    body = Dot(radius=0.075, color=color).shift(DOWN * 0.03)
    return VGroup(wings, body)


class S01Hook(SpokenScene, TitleCard):
    LESSON = "Restoring Ecosystems"
    TITLE = "When Stopping Harm Is Not Enough"

    def construct(self):
        title = fit_text(self.TITLE, max_w=11.5, size=52, color=TEXT, font=TITLE_FONT)
        lesson = T(self.LESSON.upper(), 24, TEAL).next_to(title, UP, buff=0.28)
        rule = Line(LEFT * 1.2, RIGHT * 1.2, color=GOLD, stroke_width=4).next_to(title, DOWN, buff=0.28)
        self.play(FadeIn(lesson), Write(title), GrowFromCenter(rule), run_time=0.65)
        shore = eagle_shoreline()
        self.play(FadeOut(VGroup(lesson, title, rule)), FadeIn(shore), run_time=0.75)
        bob(shore[3], amp=0.035, speed=1.1)
        self.play(shore.animate.shift(RIGHT * 0.35), run_time=4.2, rate_func=linear)

        self.at("But what if")
        q = fit_text("What if harm stops—but recovery does not start?", max_w=11.5,
                     size=36, color=GOLD).move_to([0, 3.15, 0])
        self.play(FadeIn(q, shift=DOWN * 0.12), run_time=0.55)

        self.at("A Bear")
        bay = bay_world("bare", label=True)
        self.play(FadeOut(shore), FadeIn(bay), run_time=1.0)

        self.at("The water moves")
        no_meadow = T("no meadow", 34, GREEN).move_to([0.4, -0.75, 0])
        self.play(FadeIn(no_meadow), run_time=0.5)
        self.finish()


class S02Loss(SpokenScene):
    def construct(self):
        bay = bay_world("bare")
        self.add(bay, scope_tag("schematic"))
        meadow = grass_patch(-5.35, 5.65, 30, 1.45, 4)
        self.play(Create(meadow), run_time=1.35)

        self.at("A disease")
        haze = Rectangle(width=12.2, height=2.6, stroke_width=0, fill_color=RED,
                         fill_opacity=0.18).move_to([-7.2, -0.45, 0])
        disease = chip("disease • biotic", RED, size=28).move_to([-3.7, 2.9, 0])
        self.play(haze.animate.shift(RIGHT * 7.2), FadeIn(disease), run_time=1.1)

        self.at("A hurricane")
        storm = Arc(radius=2.2, start_angle=0.1, angle=PI * 0.82, color=RED,
                    stroke_width=12).stretch(2.1, 0).move_to([1.7, 0.55, 0])
        hurricane = chip("hurricane • abiotic", RED, size=28).move_to([3.35, 2.9, 0])
        self.play(Create(storm), FadeIn(hurricane), meadow.animate.set_stroke(width=4), run_time=1.0)

        self.at("Together")
        survivors = grass_patch(-4.75, -4.2, 2, 0.78, 8)
        self.play(FadeOut(meadow), FadeIn(survivors), storm.animate.shift(RIGHT * 4.5),
                  haze.animate.set_opacity(0.05), run_time=1.25)

        self.at("The green meadow")
        gone = T("meadow lost", 34, GREEN).move_to([0.25, -0.7, 0])
        self.play(FadeIn(gone), FadeOut(storm), run_time=0.55)
        self.at("Few green plants")
        self.play(Indicate(survivors, color=GOLD, scale_factor=1.15), run_time=0.8)
        self.finish()


class S03Barrier(SpokenScene):
    def construct(self):
        bay = bay_world("sparse")
        self.add(bay)
        condition = ValueTracker(0.15)
        gauge = dial(condition, center=[-4.35, 1.1, 0], radius=1.1,
                     label="water conditions", color=GREEN, fmt="{:.0f}%")
        self.play(FadeIn(gauge), condition.animate.set_value(0.88), run_time=1.45)

        self.at("Yet almost no")
        self.play(Indicate(bay.grass, color=GOLD, scale_factor=1.22), run_time=0.7)

        self.at("the door was open")
        door = VGroup(Line([2.7, -1.9, 0], [2.7, 0.25, 0], color=TEAL, stroke_width=10),
                      Line([2.7, 0.25, 0], [3.9, 0.25, 0], color=TEAL, stroke_width=10),
                      Line([3.9, 0.25, 0], [3.9, -1.9, 0], color=TEAL, stroke_width=10))
        open_arrow = Arrow([3.75, -0.45, 0], [4.45, -1.1, 0], buff=0.05,
                           color=TEAL, stroke_width=5, tip_length=0.24)
        self.play(Create(door), GrowArrow(open_arrow), run_time=0.75)

        self.at("But nothing nearby")
        empty = seed_source(True)
        self.play(FadeOut(open_arrow), FadeIn(empty), run_time=0.6)

        self.at("missing starter")
        blocked = T("missing starter population", 34, GOLD).move_to([0.45, 3.1, 0])
        self.play(FadeIn(blocked), Indicate(empty[0], color=GOLD), run_time=0.75)

        self.at("Suitable conditions alone")
        alone = T("suitable water ≠ seeds", 32, TEXT).move_to([0.25, -0.75, 0])
        self.play(FadeOut(door), FadeIn(alone), run_time=0.6)
        self.finish()


class S04Predict(SpokenScene):
    QUESTION = "Refill alone—or add a starter?"

    def construct(self):
        bay = bay_world("bare", source="empty")
        self.add(bay)
        pulse(bay.source[0], base=5.0, amp=1.5, speed=2.1)

        self.at("Will the meadow")
        q = question_card(self.QUESTION, y=3.15, size=38, max_w=11.2)
        self.play(FadeIn(q.question, shift=DOWN * 0.12), run_time=0.65)

        self.at("Or must something")
        arrow = Arrow([2.8, -0.65, 0], bay.source[0].get_left(), buff=0.14,
                      color=GOLD, stroke_width=6, tip_length=0.25)
        self.play(GrowArrow(arrow), run_time=0.65)

        self.at("Keep watching")
        self.play(FadeOut(arrow), bay.source[0].animate.scale(1.08), run_time=0.65)
        self.at("Notice which piece")
        self.play(Indicate(bay.source, color=GOLD, scale_factor=1.12), run_time=0.8)
        self.finish()


class S05Pause(PredictPause):
    QUESTION = "Refill alone—or add a starter?"
    OPTIONS = ()
    SECONDS = 4.5
    CARD = {"y": 3.15, "size": 38, "max_w": 11.2}
    RING_AT = (6.0, -3.05, 0)

    def backdrop(self):
        bay = bay_world("bare", source="empty")
        pulse(bay.source[0], base=5.0, amp=1.5, speed=2.1)
        return bay


class S06Restore(SpokenScene):
    def construct(self):
        bay = bay_world("bare", plots=True, source="empty")
        self.add(bay, scope_tag("schematic"))
        b = boat().move_to([-5.5, 1.45, 0])

        self.at("Scientists supplied")
        self.play(FadeIn(b), b.animate.shift(RIGHT * 5.4), run_time=1.2)

        self.at("They spread")
        seeds = VGroup(*[Dot(radius=0.075, color=GOLD) for _ in range(16)])
        for i, d in enumerate(seeds):
            x = (-3.65 + 0.38 * (i % 6)) if i < 8 else (0.1 + 0.38 * (i % 6))
            d.move_to([x, 1.35 + 0.12 * (i % 3), 0])
        self.play(FadeIn(seeds), seeds.animate.shift(DOWN * 2.8), run_time=1.25)

        self.at("This is restoration")
        definition = caption("Restoration helps a damaged ecosystem recover.", size=32, color=TEAL)
        self.play(FadeIn(definition), run_time=0.65)

        self.at("did not build")
        self.play(FadeOut(definition), FadeOut(b), run_time=0.55)

        self.at("It placed living")
        shoots = VGroup(grass_patch(-3.65, -1.85, 7, 0.95, 11),
                        grass_patch(0.05, 1.9, 7, 0.95, 13))
        source_full = seed_source(False)
        self.play(FadeOut(seeds), FadeOut(bay.source), FadeIn(source_full), Create(shoots), run_time=1.2)

        self.at("Their choice matched")
        match = T("action matches barrier", 34, TEAL).move_to([0, 3.05, 0])
        self.play(FadeIn(match), Indicate(source_full, color=GOLD), run_time=0.8)
        self.finish()


class S07Spread(SpokenScene):
    def construct(self):
        bay = bay_world("plots", plots=True, source="full")
        self.add(bay, scope_tag("schematic"))

        self.at("Seeds grew")
        self.play(bay.grass.animate.scale(1.12, about_point=[0, FLOOR_Y, 0]), run_time=0.85)

        self.at("made more seeds")
        new_seeds = VGroup(*[Dot(radius=0.07, color=GOLD) for _ in range(14)])
        for i, d in enumerate(new_seeds):
            x = (-3.45 + 0.32 * (i % 6)) if i < 7 else (0.25 + 0.32 * (i % 6))
            d.move_to([x, -0.75 + 0.17 * (i % 3), 0])
        self.play(FadeIn(new_seeds), run_time=0.6)

        self.at("moved beyond")
        destinations = [np.array([-5.1 + 0.78 * i, -1.45 + 0.13 * (i % 2), 0]) for i in range(14)]
        self.play(*[d.animate.move_to(p) for d, p in zip(new_seeds, destinations)],
                  run_time=1.1, rate_func=linear)

        self.at("Green patches widened")
        outside = VGroup(grass_patch(-5.35, -3.95, 6, 1.2, 22),
                         grass_patch(-1.45, -0.25, 5, 1.2, 24),
                         grass_patch(2.25, 5.55, 12, 1.28, 26))
        self.play(FadeOut(new_seeds), Create(outside), run_time=1.35)

        self.at("both human help")
        human = T("human help", 30, TEAL).move_to([-3.0, 3.05, 0])
        natural = T("plant reproduction", 30, GREEN).move_to([2.2, 3.05, 0])
        self.play(FadeIn(human), FadeIn(natural), run_time=0.7)

        self.at("plots became sources")
        source_label = T("sources, not borders", 34, GOLD).move_to([0, 2.9, 0])
        self.play(FadeOut(human), FadeOut(natural), FadeIn(source_label),
                  Indicate(bay.plots, color=TEAL), run_time=0.85)
        self.finish()


class S08Limits(SpokenScene):
    def construct(self):
        bay = bay_world("bare")
        divider = Line([0, -2.75, 0], [0, 2.65, 0], color=GREY, stroke_width=4)
        heads = VGroup(T("nearby natural", 32, GREEN).move_to([-3.25, 3.1, 0]),
                       T("restored", 32, TEAL).move_to([3.25, 3.1, 0]))
        left_grass = grass_patch(-5.45, -0.35, 15, 1.38, 27)
        right_grass = grass_patch(0.35, 5.55, 15, 1.38, 29)
        restored_plots = VGroup(
            DashedVMobject(Rectangle(width=1.8, height=1.5, color=TEAL, stroke_width=3), num_dashes=20)
            .move_to([1.55, FLOOR_Y + 0.75, 0]),
            DashedVMobject(Rectangle(width=1.8, height=1.5, color=TEAL, stroke_width=3), num_dashes=20)
            .move_to([4.15, FLOOR_Y + 0.75, 0]))
        self.add(bay, divider, heads, left_grass, right_grass, restored_plots)
        fish_l = animal_icon("fish").move_to([-4.25, 0.55, 0])
        fish_r = animal_icon("fish").move_to([2.15, 0.55, 0])
        unique_l = animal_icon("round").scale(0.8).move_to([-2.2, -0.15, 0])
        unique_r = Triangle(color=GOLD, fill_color=GOLD, fill_opacity=0.7).scale(0.24).move_to([4.4, -0.15, 0])
        bob(fish_l, amp=0.08, speed=1.2)
        bob(fish_r, amp=0.08, speed=1.0, seed=2)
        self.play(FadeIn(fish_l), FadeIn(fish_r), run_time=0.7)

        self.at("exact rewind")
        rewind = T("exact rewind", 32, RED).move_to([0, 3.45, 0])
        strike = Line(rewind.get_left(), rewind.get_right(), color=RED, stroke_width=6)
        strike.layout_ok = True
        self.play(FadeIn(rewind), Create(strike), run_time=0.65)

        self.at("some parts remain")
        self.play(FadeIn(unique_l), run_time=0.6)
        self.at("gain kinds")
        self.play(FadeIn(unique_r), run_time=0.6)

        self.at("Ecosystems keep changing")
        self.play(fish_l.animate.shift(RIGHT * 0.55), fish_r.animate.shift(LEFT * 0.55),
                  unique_l.animate.shift(UP * 0.18), unique_r.animate.shift(DOWN * 0.18), run_time=1.0)

        self.at("Different does not")
        summary = caption("Improved, not rewound.", size=36, color=GOLD)
        self.play(FadeIn(summary), run_time=0.6)
        self.finish()


class S09Choice(SpokenScene):
    def construct(self):
        panels = TwoPanel("protect healthy", "restore after damage", colors=(TEAL, GREEN), top=3.0, bottom=-2.1)
        left = grass_patch(-5.15, -1.45, 14, 1.7, 31)
        right = grass_patch(1.2, 5.15, 13, 1.5, 33)
        left.move_to(panels.area("left")[0] + DOWN * 0.5)
        right.move_to(panels.area("right")[0] + DOWN * 0.5)
        shield = Arc(radius=1.45, start_angle=0.05, angle=PI - 0.1, color=TEAL, stroke_width=12)
        shield.move_to([-3.25, 0.25, 0])
        self.add(panels, left, right)

        self.at("Protecting a healthy")
        self.play(Create(shield), run_time=1.0)

        self.at("When damage")
        cause = chip("cause reduced?", TEAL, size=28).move_to([-4.15, -3.05, 0])
        self.play(FadeIn(cause), run_time=0.55)

        self.at("Then ask")
        remains = chip("what remains?", TEAL, size=28).move_to([0, -3.05, 0])
        self.play(FadeIn(remains), run_time=0.55)

        self.at("what is missing")
        missing = chip("what is missing?", TEAL, size=28).move_to([4.15, -3.05, 0])
        self.play(FadeIn(missing), run_time=0.55)

        self.at("what evidence")
        cursor = Dot([-5.3, -2.25, 0], radius=0.12, color=GOLD)
        measure = Arrow([-5.3, -2.25, 0], [5.3, -2.25, 0], buff=0, color=GREY,
                        stroke_width=4, tip_length=0.22)
        self.play(Create(measure), FadeIn(cursor), cursor.animate.shift(RIGHT * 6.8), run_time=1.0)

        self.at("Restoration begins")
        diagnosis = T("diagnose before choosing a tool", 36, GOLD).move_to([0, 3.45, 0])
        self.play(FadeIn(diagnosis), run_time=0.7)
        self.finish()


class S10Rule(SpokenScene):
    def construct(self):
        water = Rectangle(width=13.0, height=3.5, stroke_width=0, fill_color=BLUE,
                          fill_opacity=0.17).move_to([0, -0.55, 0])
        land = Polygon([-6.5, 2.5, 0], [-0.25, 2.5, 0], [-1.25, -2.05, 0], [-6.5, -2.05, 0],
                       color=GREEN, fill_color=GREEN, fill_opacity=0.25, stroke_width=3)
        forest = VGroup(*[Triangle(color=GREEN, fill_color=GREEN, fill_opacity=0.6).scale(0.34)
                          .move_to([-5.5 + 0.75 * i, -0.2 + 0.2 * (i % 3), 0]) for i in range(6)])
        meadow = grass_patch(0.1, 5.9, 18, 1.35, 40)
        nests = VGroup(*[eagle_icon().scale(0.9).move_to([-4.8 + 1.5 * i, 1.3, 0]) for i in range(3)])
        self.add(water, land, forest, meadow, nests, scope_tag("schematic"))

        self.at("different parts")
        labels = VGroup(T("eagle shoreline", 30, GOLD).move_to([-3.6, 2.95, 0]),
                        T("eelgrass bay", 30, GREEN).move_to([3.25, 2.95, 0]))
        self.play(FadeIn(labels), run_time=0.65)

        self.at("Remove the harm")
        harm = Arrow([-6.0, 1.0, 0], [-4.6, 0.8, 0], color=RED, stroke_width=8, tip_length=0.3)
        block = Line([-5.35, 1.65, 0], [-4.95, 0.2, 0], color=TEAL, stroke_width=13)
        self.play(GrowArrow(harm), Create(block), harm.animate.set_opacity(0.2), run_time=0.8)

        self.at("protect what remains")
        shield = Arc(radius=1.3, start_angle=0.05, angle=PI - 0.1, color=TEAL, stroke_width=10)
        shield.move_to([-3.2, 0.15, 0])
        self.play(Create(shield), run_time=0.7)

        self.at("help ecosystems")
        seeds = VGroup(*[Dot(radius=0.07, color=GOLD).move_to([0.6 + 0.7 * i, -0.55, 0]) for i in range(6)])
        self.play(FadeIn(seeds), seeds.animate.shift(RIGHT * 1.2 + DOWN * 0.45), run_time=1.0)

        self.at("may be protection")
        help_line = T("protection  •  starter  •  repair", 32, TEAL).move_to([0, 2.95, 0])
        self.play(FadeOut(labels), run_time=0.3)
        self.play(FadeIn(help_line), run_time=0.45)

        self.at("patient measurement")
        timeline = Arrow([-5.4, -3.05, 0], [5.4, -3.05, 0], buff=0, color=GREY,
                         stroke_width=5, tip_length=0.25)
        cursor = Dot(timeline.get_start(), radius=0.13, color=GOLD)
        timeline_label = T("measure over time", 30, GOLD).next_to(timeline, UP, buff=0.12)
        self.play(Create(timeline), FadeIn(cursor), FadeIn(timeline_label),
                  cursor.animate.move_to(timeline.point_from_proportion(0.72)), run_time=1.35, rate_func=linear)

        self.at("without promising")
        caution = T("guides action—no perfect return promised", 34, GOLD).move_to([0, 3.25, 0])
        self.play(FadeOut(help_line), run_time=0.3)
        self.play(FadeIn(caution), run_time=0.45)
        self.finish()


class S11End(EndCard):
    LINE = "Remove the harm, protect what remains, and help ecosystems recover over time."
