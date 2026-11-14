"""What pushes the four arrows? — chapter 2 of Populations Rise and Fall.

COLOR MAP (kept exactly from chapter 1)
  BLUE   = blue crabs, births, and arrivals
  RED    = losses, deaths, departures, and adult predator crabs
  GREEN  = grass and other living/biotic parts
  TEAL   = cold, salt, and other nonliving/abiotic parts
  YELLOW = human actions, walls, harvest, and harvest limits
  GOLD   = questions and emphasis
  GREY   = water, mud, stone, outlines, and qualifications

All population dots and responses are schematic. Curves in s10 are computed from the
explicit functions in evidence_plot(); they are not data from the winter survey.
"""
import numpy as np
from bp_parts import *  # noqa: F401,F403

CRAB = BLUE
LOSS = RED
GRASS = GREEN
NONLIVING = TEAL
PEOPLE = YELLOW

# The script predates the pipeline's top-level `ambient` switch. Use the same restrained drifting
# field locally: it keeps explanatory holds alive without adding a claim or competing with the world.
_PipelineSpokenScene = SpokenScene


def _add_sweep(scene):
    """Slow soft light band crossing the frame every ~6 s: ambient motion for long spoken holds."""
    band = Rectangle(width=2.6, height=8.4, stroke_width=0, fill_color=TEXT, fill_opacity=.07)
    band.move_to([-8, 0, 0]).set_z_index(-15)
    band.t = 0.0
    def go(m, dt):
        m.t += dt
        m.move_to([-8 + 16 * ((m.t / 6.0) % 1.0), 0, 0])
    band.add_updater(go)
    scene.add(band)


class SpokenScene(_PipelineSpokenScene):
    def setup(self):
        super().setup()
        rng = np.random.default_rng(sum(map(ord, self.__class__.__name__)))
        motes = VGroup()
        for _ in range(30):
            d = Dot(radius=rng.uniform(.025, .055), color=rng.choice([TEAL, GREY, TEXT]))
            d.set_opacity(rng.uniform(.10, .20)).move_to([rng.uniform(-6.7, 6.7), rng.uniform(-3.6, 3.6), 0])
            d.v = np.array([rng.uniform(-.16, .16), rng.uniform(.10, .25), 0])
            def drift(m, dt):
                m.shift(m.v * dt)
                if m.get_y() > 3.9:
                    m.shift(DOWN * 7.8)
                if m.get_x() > 7.1:
                    m.shift(LEFT * 14.2)
                elif m.get_x() < -7.1:
                    m.shift(RIGHT * 14.2)
            d.add_updater(drift)
            motes.add(d)
        motes.set_z_index(-20)
        self.add(motes)
        _add_sweep(self)


def arrow(a, b, color=GREY, width=6, tip=0.24):
    return Arrow(a, b, buff=0.06, color=color, stroke_width=width, tip_length=tip,
                 max_tip_length_to_length_ratio=0.45, max_stroke_width_to_length_ratio=12)


def crab_dot(at, color=CRAB, radius=0.15):
    return Dot(at, radius=radius, color=color, stroke_color=color, stroke_width=2)


def population_window(*, wall=False, refuge=1.0, arrow_widths=(7, 7, 7, 7), labels=True):
    """The one carried Bay window used in every population scene.

    Returns a VGroup with named parts. Its geometry is fixed so chapter 2 remains in chapter 1's
    world: a central Bay ellipse, BLUE additions at left, RED losses at right.
    """
    g = VGroup()
    bay = Ellipse(width=6.0, height=4.5, stroke_color=GREY, stroke_width=3,
                  fill_color=GREY, fill_opacity=0.09).move_to([0, -0.05, 0])
    water = Rectangle(width=5.65, height=1.9, stroke_width=0, fill_color=NONLIVING,
                      fill_opacity=0.07).move_to([0, -0.15, 0])
    water.set_clip_path(bay.copy())
    mud = ArcBetweenPoints([-2.6, -1.25, 0], [2.6, -1.25, 0], angle=-0.22,
                           color=GREY, stroke_width=12).set_opacity(0.55)
    positions = [(-1.65, 0.72), (-0.55, 1.18), (0.65, 0.72), (1.58, 1.18),
                 (-1.25, -0.22), (-0.15, 0.12), (1.05, -0.25),
                 (-1.72, -0.92), (-0.55, -1.08), (0.7, -0.92), (1.66, -0.62)]
    dots = VGroup(*[crab_dot([x, y, 0]) for x, y in positions])

    # A shallow refuge on the left; when wall=True it is visibly compressed, not removed.
    shore_x = -2.45 if not wall else -2.80
    shallow_w = 1.45 * refuge
    shallow = Polygon([-2.78, -1.15, 0], [shore_x + shallow_w, -1.15, 0],
                      [shore_x + shallow_w * 0.78, -0.38, 0], [-2.78, -0.58, 0],
                      stroke_color=GREY, stroke_width=2, fill_color=GREY, fill_opacity=0.18)
    grass = VGroup()
    for i in range(max(1, int(6 * refuge))):
        x = -2.52 + i * (shallow_w / max(6 * refuge, 1))
        grass.add(ArcBetweenPoints([x, -1.05, 0], [x + 0.10, -0.48, 0], angle=0.28,
                                   color=GRASS, stroke_width=5))
    structure = VGroup(shallow, grass)
    if wall:
        stones = VGroup(*[RoundedRectangle(corner_radius=0.06, width=0.55, height=0.42,
                                            color=GREY, stroke_width=2, fill_color=GREY,
                                            fill_opacity=0.35).move_to([-2.75, -0.85 + 0.42 * i, 0])
                           for i in range(5)])
        structure.add(stones)

    births = arrow([-5.75, 0.92, 0], [-3.05, 0.92, 0], CRAB, arrow_widths[0])
    arrivals = arrow([-5.75, -1.02, 0], [-3.05, -1.02, 0], CRAB, arrow_widths[1])
    deaths = arrow([3.05, 0.92, 0], [5.75, 0.92, 0], LOSS, arrow_widths[2])
    departures = arrow([3.05, -1.02, 0], [5.75, -1.02, 0], LOSS, arrow_widths[3])
    arrows = VGroup(births, arrivals, deaths, departures)
    # Three beads per arrow make the four flows continuously legible during long spoken holds.
    flow = VGroup()
    for ai, a in enumerate(arrows):
        start, end = a.get_start(), a.get_end()
        for j in range(3):
            d = Dot(radius=.09, color=a.get_color()).set_opacity(.9)
            d.phase = (j / 3 + .13 * ai) % 1
            d.a0, d.a1 = start.copy(), end.copy()
            def travel(m, dt):
                m.phase = (m.phase + .72 * dt) % 1
                m.move_to(interpolate(m.a0, m.a1, m.phase))
            d.add_updater(travel)
            d.move_to(interpolate(start, end, d.phase))
            flow.add(d)
    labs = VGroup()
    if labels:
        labs.add(T("births", 28, CRAB).next_to(births, UP, buff=0.10),
                 T("arrivals", 28, CRAB).next_to(arrivals, DOWN, buff=0.10),
                 T("deaths", 28, LOSS).next_to(deaths, UP, buff=0.10),
                 T("departures", 28, LOSS).next_to(departures, DOWN, buff=0.10))
    g.add(water, bay, mud, structure, dots, arrows, flow, labs)
    g.bay, g.water, g.mud, g.structure, g.grass = bay, water, mud, structure, grass
    g.dots, g.arrows, g.flow, g.labels = dots, arrows, flow, labs
    g.births, g.arrivals, g.deaths, g.departures = births, arrivals, deaths, departures
    return g


def moving_water(width=12.2, y=-0.35):
    """Three low-amplitude waves with a cheap continuous bob (no per-frame rebuilding)."""
    waves = VGroup(*[
        FunctionGraph(lambda x, k=k: y - 0.48 * k + 0.08 * np.sin(1.6 * x + k),
                      x_range=(-width / 2, width / 2), color=NONLIVING, stroke_width=2).set_opacity(0.35)
        for k in range(3)])
    bob(waves, amp=.035, speed=.8)
    return VGroup(), waves


def meter(label, color, level=.7, at=ORIGIN):
    """A lightweight static vertical meter, transformed between stated levels."""
    track = RoundedRectangle(corner_radius=.12, width=.56, height=1.65, color=GREY,
                             stroke_width=3, fill_color=BG, fill_opacity=.9)
    h = max(.12, 1.38 * level)
    fill_bar = Rectangle(width=.34, height=h, stroke_width=0, fill_color=color,
                         fill_opacity=.82).align_to(track, DOWN).shift(UP*.13)
    lab = T(label, 28, color).next_to(track, DOWN, buff=.16)
    return VGroup(track, fill_bar, lab).move_to(at)


def thermometer():
    stem = RoundedRectangle(corner_radius=0.16, width=0.34, height=1.5, color=NONLIVING,
                            stroke_width=4).move_to([0, 0.2, 0])
    bulb = Circle(radius=0.34, color=NONLIVING, stroke_width=4,
                  fill_color=NONLIVING, fill_opacity=0.55).move_to([0, -0.62, 0])
    fill = Rectangle(width=0.16, height=0.9, stroke_width=0, fill_color=NONLIVING,
                     fill_opacity=0.8).move_to([0, -0.12, 0])
    return VGroup(stem, fill, bulb)


def grass_icon():
    return VGroup(*[ArcBetweenPoints([-.55 + .22 * i, -.55, 0], [-.45 + .22 * i, .55, 0],
                                     angle=.35 if i % 2 else -.35, color=GRASS, stroke_width=7)
                    for i in range(6)])


def adult_crab_icon():
    body = Ellipse(width=1.25, height=0.72, color=LOSS, stroke_width=5,
                   fill_color=LOSS, fill_opacity=0.25)
    legs = VGroup(*[Line([s * .35, y, 0], [s * .76, y + .18 * (1 if y > 0 else -1), 0],
                         color=LOSS, stroke_width=4)
                    for s in (-1, 1) for y in (-.22, .22)])
    return VGroup(legs, body)


def pot_icon():
    body = Polygon([-.65, .45, 0], [.65, .45, 0], [.52, -.45, 0], [-.52, -.45, 0],
                   color=PEOPLE, stroke_width=5, fill_color=PEOPLE, fill_opacity=.12)
    slats = VGroup(*[Line([x, .38, 0], [x * .8, -.38, 0], color=PEOPLE, stroke_width=2)
                     for x in (-.38, 0, .38)])
    return VGroup(body, slats)


def factor_icons():
    """The four factor pictures, sized and positioned identically in hook and return."""
    cold = VGroup(thermometer().scale(.72), T("cold", 28, NONLIVING)).arrange(DOWN, buff=.12).move_to([-4.8, 2.42, 0])
    grass = VGroup(grass_icon().scale(.7), T("shelter", 28, GRASS)).arrange(DOWN, buff=.12).move_to([-4.75, -2.65, 0])
    pred = VGroup(adult_crab_icon().scale(.78), T("predators", 28, LOSS)).arrange(DOWN, buff=.12).move_to([4.75, 2.42, 0])
    harvest = VGroup(pot_icon().scale(.72), T("harvest", 28, PEOPLE)).arrange(DOWN, buff=.12).move_to([4.75, -2.65, 0])
    return VGroup(cold, grass, pred, harvest)


def changed_shore_backdrop(question=True):
    world = population_window(wall=True, refuge=.36, labels=True)
    q = question_card("Which arrow could change first?", color=GOLD, y=-3.25, max_w=9.6)
    if question:
        return VGroup(world, q)
    return world


class S00Hook(SpokenScene):
    def construct(self):
        world = population_window()
        icons = factor_icons()
        self.at("The first film")
        self.play(FadeIn(world.bay), FadeIn(world.water), FadeIn(world.mud),
                  FadeIn(world.dots, lag_ratio=.08), run_time=1.8)
        self.at("additions and losses")
        self.play(GrowArrow(world.births), GrowArrow(world.arrivals),
                  GrowArrow(world.deaths), GrowArrow(world.departures), FadeIn(world.labels), run_time=1.8)
        self.at("What pushes those arrows")
        q = T("What pushes the four arrows?", 40, TEXT, font=TITLE_FONT).move_to([0, 3.48, 0])
        self.play(Write(q), run_time=1.2)
        self.at("cold shelter predators")
        self.play(FadeIn(icons, lag_ratio=.12), run_time=2.2)
        for i, ic in enumerate(icons):
            bob(ic, amp=.06, speed=1.1 + .12 * i, seed=i)
        pulse(world.arrows, base=7, amp=1.5, speed=1.2)
        self.at("same color map")
        self.play(Indicate(icons, color=TEXT, scale_factor=1.03), run_time=1.4)
        self.finish()


class S01Title(TitleCard):
    LESSON = "Populations rise and fall"
    TITLE = "What Pushes the Four Arrows?"


class S02TwoSorts(SpokenScene):
    def construct(self):
        head = T("Two separate questions", 42, TEXT, font=TITLE_FONT).move_to([0, 3.3, 0])
        panels = TwoPanel("biotic: living", "abiotic: nonliving", colors=(GRASS, NONLIVING), top=2.75, bottom=-1.2)
        grass = VGroup(grass_icon().scale(.85), T("grass", 28, GRASS)).arrange(DOWN, buff=.18).move_to([-4.25, .45, 0])
        big = VGroup(adult_crab_icon(), T("big crab", 28, LOSS)).arrange(DOWN, buff=.18).move_to([-1.95, .45, 0])
        cold = VGroup(thermometer().scale(.85), T("temperature", 28, NONLIVING)).arrange(DOWN, buff=.18).move_to([2.05, .45, 0])
        salt = meter("salt", NONLIVING, .72, [4.45, .55, 0])

        self.at("Scientists ask")
        self.play(FadeIn(head), run_time=.8)
        self.at("living and non")
        self.play(FadeIn(panels), run_time=1.2)
        self.at("Biotic factors")
        self.play(FadeIn(grass, shift=UP*.15), run_time=.9)
        self.at("grass and big crabs")
        self.play(FadeIn(big, shift=UP*.15), run_time=.9)
        self.at("Abiotic factors")
        self.play(FadeIn(cold, shift=UP*.15), run_time=.9)
        self.at("temperature and salt")
        self.play(FadeIn(salt), run_time=1.5)

        cause = question_card("Cause: natural, human-caused, or both?", y=-2.0, color=GOLD, max_w=11.5)
        self.at("Second is the change")
        self.play(FadeOut(VGroup(grass, big, cold, salt)), panels.animate.set_opacity(.32), FadeIn(cause), run_time=1.2)
        winter = VGroup(thermometer().scale(.62), chip("abiotic + natural", NONLIVING, size=28)).arrange(RIGHT, buff=.35).move_to([-3.25, -.25, 0])
        wall_icon = VGroup(*[RoundedRectangle(corner_radius=.05, width=.65, height=.42, color=GREY,
                                              fill_color=GREY, fill_opacity=.35).shift(RIGHT*.34*(i%2)+UP*.42*(i//2))
                               for i in range(4)]).move_to(ORIGIN)
        wall = VGroup(wall_icon, chip("abiotic + human", GREY, size=28)).arrange(RIGHT, buff=.35).move_to([3.25, -.25, 0])
        self.at("cold winter")
        self.play(FadeIn(winter, shift=RIGHT*.15), run_time=1.0)
        self.at("stone wall")
        self.play(FadeIn(wall, shift=LEFT*.15), run_time=1.0)
        bob(thermometer(), amp=.01)  # no visible extra object; keeps intent explicit
        self.finish()


class S03Cold(SpokenScene):
    def construct(self):
        world = population_window(labels=False)
        cold = Rectangle(width=12.2, height=1.15, stroke_width=0, fill_color=NONLIVING,
                         fill_opacity=.16).move_to([0, 2.15, 0])
        flakes = VGroup(*[T("✦", 26, NONLIVING).move_to([x, 2.75 + .18*(i%2), 0])
                          for i, x in enumerate(np.linspace(-3.2, 3.2, 8))])
        gauges = VGroup(meter("temperature", NONLIVING, .72, [-4.65, 2.25, 0]),
                        meter("salt", NONLIVING, .68, [4.65, 2.25, 0]))
        gauges_low = VGroup(meter("temperature", NONLIVING, .14, [-4.65, 2.25, 0]),
                            meter("salt", NONLIVING, .12, [4.65, 2.25, 0]))
        self.add(world)
        pulse(world.arrows, base=7, amp=1.0, speed=1.0)
        self.at("Watch a nonliving")
        self.play(FadeIn(gauges), run_time=1.0)
        self.at("very cold winter")
        self.play(FadeIn(cold, shift=DOWN*.2), FadeIn(flakes, lag_ratio=.08),
                  Transform(gauges[0], gauges_low[0]), run_time=2.2)
        buried = VGroup(*[d.copy().move_to([d.get_x(), -1.22, 0]) for d in world.dots[:5]])
        self.at("buried crabs")
        self.play(Transform(VGroup(*world.dots[:5]), buried), run_time=1.5)
        self.at("cold low salt water")
        self.play(Transform(gauges[1], gauges_low[1]), run_time=1.8)
        self.at("widen the death arrow")
        dead = VGroup(*[world.dots[i] for i in (1, 4, 7)])
        self.play(dead.animate.move_to(world.deaths.get_end()+RIGHT*.25).set_opacity(0),
                  world.deaths.animate.set_stroke(width=13), run_time=2.2)
        self.at("act together")
        together = caption("cold + low salt may act together", color=NONLIVING)
        self.play(FadeIn(together), Indicate(gauges, color=NONLIVING, scale_factor=1.03), run_time=1.2)
        self.add(scope_tag("schematic"))
        self.finish()


def refuge_cove(refuge=1.0):
    """Warm cove builder shared by refuge, predict, pause, and reveal."""
    water_group, waves = moving_water()
    floor = Polygon([-6.2, -2.1, 0], [6.2, -2.1, 0], [6.2, -3.0, 0], [-6.2, -3.0, 0],
                    color=GREY, stroke_width=2, fill_color=GREY, fill_opacity=.22)
    grass = VGroup(*[ArcBetweenPoints([-5.1 + .38*i, -2.05, 0], [-4.98 + .38*i, -.45, 0],
                                      angle=.28*(-1 if i%2 else 1), color=GRASS, stroke_width=6)
                     for i in range(max(2, int(9*refuge)))])
    young = VGroup(*[crab_dot([-4.65+.6*i, -1.45+.18*(i%2), 0], radius=.14) for i in range(6)])
    predator = adult_crab_icon().scale(1.15).move_to([3.8, -1.15, 0])
    g = VGroup(waves, floor, grass, young, predator)
    g.water_group, g.waves, g.floor, g.grass, g.young, g.predator = water_group, waves, floor, grass, young, predator
    return g


class S04Refuge(SpokenScene):
    def construct(self):
        cove = refuge_cove(1.0)
        self.add(cove.water_group, cove.waves, cove.floor)
        self.at("living and non")
        self.play(FadeIn(cove.grass, lag_ratio=.08), run_time=1.4)
        self.at("Young crabs use")
        self.play(FadeIn(cove.young, lag_ratio=.10), run_time=1.2)
        self.at("bigger crabs")
        self.play(FadeIn(cove.predator, shift=LEFT*.25), run_time=1.1)
        grass_small = VGroup(*[x.copy() for x in cove.grass[:3]])
        self.at("With less refuge")
        self.play(FadeOut(VGroup(*cove.grass[3:])), cove.young[3:].animate.shift(RIGHT*3.2), run_time=2.0)
        self.at("stay exposed")
        exposed = T("exposed", 30, CRAB).move_to([1.0, .25, 0])
        self.play(FadeIn(exposed), cove.predator.animate.shift(LEFT*1.2), run_time=1.4)
        self.at("increase deaths")
        claim = caption("may increase deaths", color=LOSS, y=3.25)
        self.play(FadeIn(claim), Indicate(cove.young[3:], color=LOSS, scale_factor=1.12), run_time=1.3)
        self.at("risk not certainty")
        qual = chip("risk, not certainty", GOLD, size=30).move_to([3.9, 2.45, 0])
        self.play(FadeIn(qual), run_time=1.0)
        self.add(scope_tag("schematic"))
        self.finish()


class S05Predict(SpokenScene):
    def construct(self):
        cove = refuge_cove(1.0)
        self.add(cove.water_group, cove.waves, cove.floor, cove.grass, cove.young, cove.predator)
        self.at("stone wall replaces")
        stones = VGroup(*[RoundedRectangle(corner_radius=.06, width=.85, height=.5, color=GREY,
                                            fill_color=GREY, fill_opacity=.38).move_to([-5.55+.22*(i%2), -1.78+.5*(i//2), 0])
                           for i in range(7)])
        self.play(FadeIn(stones, shift=RIGHT*.2), FadeOut(VGroup(*cove.grass[3:])), run_time=2.0)
        self.at("refuge becomes smaller")
        self.play(cove.young[3:].animate.shift(RIGHT*2.8), run_time=1.5)
        neutral = population_window(wall=True, refuge=.36, labels=True).arrows
        neutral.set_opacity(.72)
        self.at("Which population arrow")
        self.play(FadeOut(VGroup(cove.waves, cove.floor, cove.grass, cove.young, cove.predator, stones)),
                  FadeIn(changed_shore_backdrop(question=False)), run_time=1.2)
        q = question_card("Which arrow could change first?", color=GOLD, y=-3.25, max_w=9.6)
        self.play(FadeIn(q), run_time=1.0)
        self.at("Think in arrows")
        self.play(Indicate(neutral, color=GREY, scale_factor=1.02), run_time=1.2)
        self.finish()


class S06Pause(PredictPause):
    QUESTION = "Which arrow could change first?"
    OPTIONS = ()
    SECONDS = 4.5
    CARD = {"y": -3.25, "max_w": 9.6}

    def setup(self):
        super().setup()
        _add_sweep(self)

    def backdrop(self):
        return population_window(wall=True, refuge=.36, labels=True)


class S07Reveal(SpokenScene):
    def construct(self):
        world = population_window(wall=True, refuge=.36, labels=True)
        self.add(world)
        self.at("death arrow could")
        answer = chip("could increase", LOSS, size=30).move_to([4.48, 2.35, 0])
        self.play(world.deaths.animate.set_stroke(width=13), FadeIn(answer), run_time=1.8)
        self.at("not the only")
        wall_note = T("one factor, not ‘the cause’", 30, GREY).move_to([0, 2.95, 0])
        self.play(FadeIn(wall_note), run_time=1.0)
        cold = VGroup(thermometer().scale(.55), T("?", 38, GOLD)).arrange(RIGHT, buff=.15).move_to([-4.65, -2.55, 0])
        harvest = VGroup(pot_icon().scale(.55), T("?", 38, GOLD)).arrange(RIGHT, buff=.15).move_to([4.65, -2.55, 0])
        self.at("cold harvest")
        self.play(FadeIn(cold), FadeIn(harvest), run_time=1.2)
        self.at("other arrows")
        self.play(Indicate(VGroup(world.births, world.arrivals, world.departures), color=GOLD, scale_factor=1.03), run_time=1.4)
        self.at("keeps the claim honest")
        honest = caption("could — not certainly", color=GOLD)
        self.play(swap(answer, honest), run_time=1.0)
        self.finish()


class S08Harvest(SpokenScene):
    def construct(self):
        world = population_window(labels=False)
        pot = pot_icon().scale(.95).move_to([4.55, 1.45, 0])
        harvest_arrow = arrow([2.0, 1.95, 0], [3.85, 1.95, 0], PEOPLE, width=10)
        hlabel = T("harvest", 30, PEOPLE).next_to(harvest_arrow, UP, buff=.1).shift(LEFT * .55)
        self.add(world)
        pulse(VGroup(world.births, world.arrivals, world.deaths, world.departures), base=7, amp=1.0, speed=1.0)
        self.at("human caused loss")
        self.play(FadeIn(pot), GrowArrow(harvest_arrow), FadeIn(hlabel), run_time=1.5)
        self.at("faster than it can replace")
        caught = VGroup(*[world.dots[i] for i in (3, 6, 9)])
        self.play(caught.animate.move_to(pot).set_opacity(0), harvest_arrow.animate.set_stroke(width=15), run_time=2.0)
        eggs = VGroup(*[crab_dot([-.55+.22*i, .38, 0], PEOPLE, .055) for i in range(6)])
        mother = adult_crab_icon().scale(.72).move_to([-.05, .55, 0])
        eggs.move_to(mother.get_center()+DOWN*.12)
        self.at("Female crabs carry eggs")
        self.play(FadeIn(mother), FadeIn(eggs, lag_ratio=.08), run_time=1.4)
        limit = chip("harvest limit", PEOPLE, size=30).move_to([4.45, 3.07, 0])
        self.at("Leaving more adults")
        self.play(FadeIn(limit), harvest_arrow.animate.set_stroke(width=6), FadeIn(world.dots[3].set_opacity(1)), run_time=1.7)
        young = VGroup(*[crab_dot([-.65+.32*i, -.18-.12*(i%2), 0], radius=.09) for i in range(5)])
        self.at("later births")
        self.play(FadeIn(young, lag_ratio=.12), Indicate(world.births, color=CRAB, scale_factor=1.03), run_time=1.5)
        self.at("other arrows keep moving")
        self.play(Indicate(VGroup(world.arrivals, world.deaths, world.departures), color=TEXT, scale_factor=1.03), run_time=1.6)
        self.at("do not guarantee")
        self.play(FadeIn(caption("more adults ≠ guaranteed survivors", color=GOLD)), run_time=1.0)
        self.add(scope_tag("schematic"))
        self.finish()


class S09Sustainable(SpokenScene):
    def construct(self):
        world = population_window(labels=False)
        gauges = VGroup(meter("harvest", PEOPLE, .85, [-3.7, 2.25, 0]),
                        meter("replacement", CRAB, .45, [3.7, 2.25, 0]))
        gauges_goal = VGroup(meter("harvest", PEOPLE, .45, [-3.7, 2.25, 0]),
                             meter("replacement", CRAB, .55, [3.7, 2.25, 0]))
        goal = T("goal: harvest no greater than replacement over time", 28, TEXT).move_to([0, 3.56, 0])
        self.add(world)
        self.at("Sustainable harvest")
        self.play(FadeIn(gauges), FadeIn(goal), run_time=1.4)
        self.at("only as many")
        self.play(Transform(gauges, gauges_goal), run_time=2.0)
        self.at("reduce one loss")
        h = arrow([2.15, 2.35, 0], [2.8, 2.35, 0], PEOPLE, width=6)
        self.play(GrowArrow(h), world.departures.animate.set_stroke(width=5), run_time=1.4)
        self.at("more adults")
        self.play(FadeIn(world.dots[1:4]), Indicate(world.births, color=CRAB, scale_factor=1.04), run_time=1.2)
        risks = VGroup(chip("harsh winter", NONLIVING, size=27), chip("poor refuge", GRASS, size=27),
                       chip("few new young", CRAB, size=27)).arrange(RIGHT, buff=.25).move_to([0, -2.75, 0])
        self.at("harsh winter")
        self.play(FadeIn(risks[0]), run_time=.7)
        self.at("poor refuge")
        self.play(FadeIn(risks[1]), run_time=.7)
        self.at("few new young")
        self.play(FadeIn(risks[2]), run_time=.7)
        self.at("recovery is not certain")
        uncertain = caption("recovery not certain", color=GOLD)
        self.play(AnimationGroup(FadeOut(risks, run_time=.6), FadeIn(uncertain, run_time=.6), lag_ratio=1))
        year = ValueTracker(1)
        read = counter("year {:.0f}: measure again", year, at=[0, -2.55, 0], size=30, color=TEXT)
        self.at("measuring every year")
        self.play(FadeOut(uncertain), FadeIn(read), year.animate.set_value(5), run_time=2.0, rate_func=linear)
        self.finish()


def evidence_plot():
    """A visibly schematic population curve computed from a smooth sum of sines."""
    fn = lambda t: 55 + 17*np.sin(.85*t) + 7*np.sin(1.9*t + .4)
    p = Plot(box=(-6.0, .2, -1.75, 2.45), xr=(0, 10), yr=(20, 85),
             xticks=[0, 5, 10], yticks=[(20, "low"), (80, "high")],
             xlabel="time", ylabel="population estimate")
    return p, fn


class S10Evidence(SpokenScene):
    def construct(self):
        p, fn = evidence_plot()
        t = ValueTracker(0)
        live = p.live_curve(fn, t, color=CRAB, width=7)
        dot = p.dot(lambda: t.get_value(), lambda: fn(t.get_value()), color=CRAB)
        self.at("population graph")
        self.play(Create(p), run_time=1.4)
        self.add(live, dot, scope_tag("schematic curve"))
        self.play(t.animate.set_value(10), run_time=3.0, rate_func=linear)
        self.at("not which factor")
        qm = T("?", 72, GOLD).move_to([3.8, .4, 0])
        factor = VGroup(thermometer().scale(.6), grass_icon().scale(.45), pot_icon().scale(.5)).arrange(RIGHT, buff=.35).move_to([4.15, 1.65, 0])
        self.play(FadeIn(factor), FadeIn(qm), run_time=1.2)
        cards = VGroup(chip("survey estimates", TEXT, size=26), chip("controlled test", TEXT, size=26),
                       chip("model", TEXT, size=26)).arrange(DOWN, buff=.22).move_to([4.25, -1.5, 0])
        self.at("compare the graph")
        self.play(FadeIn(cards[0]), GrowArrow(arrow([2.65,-.65,0], cards[0].get_left(), GREY, 3, .16)), run_time=.9)
        self.at("Survey estimates experiments")
        self.play(FadeIn(cards[1]), run_time=.8)
        self.at("models each add")
        self.play(FadeIn(cards[2]), run_time=.8)
        connectors = VGroup()
        for i, c in enumerate(cards):
            src = factor[i].get_bottom()
            dst = c.get_left() + LEFT*.18
            path = VMobject(stroke_color=GREY, stroke_width=2, fill_opacity=0)
            path.set_points_as_corners([src, [2.65, src[1], 0], [2.65, dst[1], 0], dst])
            connectors.add(path)
        self.play(Create(connectors), run_time=1.2)
        self.at("None makes every")
        self.play(Indicate(VGroup(live, dot), color=CRAB, scale_factor=1.02), run_time=1.3)
        self.at("narrow possible explanations")
        self.play(qm.animate.scale(.55), connectors.animate.set_color(GOLD), run_time=1.3)
        self.finish()


class S11Return(SpokenScene):
    def construct(self):
        world = population_window(labels=True)
        icons = factor_icons()
        self.at("Return to the shared")
        self.play(FadeIn(world, lag_ratio=.04), run_time=1.8)
        self.at("Natural events and human")
        self.play(FadeOut(world.labels), FadeIn(icons, lag_ratio=.10), run_time=1.6)
        targets = [world.deaths, world.births, world.deaths, world.departures]
        self.at("same additions and losses")
        self.play(*[Indicate(t, color=col, scale_factor=1.03)
                    for t, col in zip(targets, [NONLIVING, GRASS, LOSS, PEOPLE])],
                  *[ic.animate.shift((RIGHT if ic.get_x() < 0 else LEFT)*.20) for ic in icons], run_time=1.8)
        self.at("Management can change")
        self.play(icons[3].animate.shift(RIGHT*.20),
                  world.departures.animate.set_stroke(width=5), run_time=1.3)
        self.at("not command")
        self.play(*[ic.animate.move_to(pos) for ic,pos in zip(icons, [(-4.8,2.42,0),(-4.75,-2.65,0),(4.75,2.42,0),(4.75,-2.65,0)])], run_time=1.4)
        self.at("balance still decides")
        plus = VGroup(world.births, world.arrivals)
        minus = VGroup(world.deaths, world.departures)
        self.play(Indicate(plus, color=CRAB, scale_factor=1.03), Indicate(minus, color=LOSS, scale_factor=1.03), run_time=1.8)
        rule = caption("direction follows the balance", color=TEXT)
        self.play(FadeIn(rule), run_time=.8)
        self.finish()


class S12End(EndCard):
    LINE = "Natural events and human actions can change the same additions and losses."
