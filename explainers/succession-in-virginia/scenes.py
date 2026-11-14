"""How a Field Changes Its Future — succession in a Virginia Piedmont field.

COLOR MAP (one colour per concept, throughout)
  GOLD/YELLOW  open light
  SOIL         soil
  EARLY        early plants
  TEAL         pines
  ORANGE       hardwoods
  RED          disturbance / mower
  BLUE         evidence and explanatory links

The landscape is schematic.  Every continuing scene calls ``field_world`` so the
ground, canopy, and landmark x positions are rebuilt at exactly the same scale.
"""
from bp_parts import *  # noqa: F401,F403


SOIL = "#9A6B45"
EARLY = "#78C66B"
ORANGE = "#F29E4C"
PINE = TEAL
LIGHT = GOLD
GROUND_Y = -1.35


def _sway(line, phase=0.0, amp=0.075, speed=1.35):
    """Give a stem genuine, gentle wind motion about its fixed base."""
    line._wind_t = phase
    p0, p1 = line.get_start().copy(), line.get_end().copy()
    length = p1[1] - p0[1]

    def move(mob, dt):
        mob._wind_t += dt
        dx = amp * np.sin(speed * mob._wind_t)
        mob.put_start_and_end_on(p0, p1 + RIGHT * dx * max(length, 0.3))
    line.add_updater(move)
    return line


def soil_strip(y=GROUND_Y, height=1.15, x0=-6.3, x1=6.3):
    return Rectangle(
        width=x1 - x0, height=height, stroke_color=SOIL, stroke_width=3,
        fill_color=SOIL, fill_opacity=0.42,
    ).move_to([(x0 + x1) / 2, y - height / 2, 0])


def grass_patch(cx, width=2.0, height=0.8, count=8, color=EARLY, phase=0.0):
    stems = VGroup()
    for i in range(count):
        x = cx - width / 2 + width * i / max(count - 1, 1)
        h = height * (0.72 + 0.25 * ((i * 5) % 7) / 6)
        stem = Line([x, GROUND_Y, 0], [x + (0.045 if i % 2 else -0.045), GROUND_Y + h, 0],
                    color=color, stroke_width=5)
        stems.add(_sway(stem, phase + i * 0.55, amp=0.055))
    return stems


def pine_tree(x, height=3.25, width=1.45, color=PINE):
    trunk = Line([x, GROUND_Y, 0], [x, GROUND_Y + height * 0.7, 0], color=SOIL, stroke_width=7)
    crowns = VGroup()
    for frac, scale in ((0.42, 1.0), (0.62, 0.78), (0.79, 0.56)):
        y = GROUND_Y + height * frac
        crowns.add(Polygon([x - width * scale / 2, y, 0], [x + width * scale / 2, y, 0],
                           [x, y + height * 0.34, 0], stroke_color=color, stroke_width=3,
                           fill_color=color, fill_opacity=0.48))
    return VGroup(trunk, crowns)


def hardwood_tree(x, height=2.7, radius=0.72, color=ORANGE):
    trunk = Line([x, GROUND_Y, 0], [x, GROUND_Y + height * 0.72, 0], color=SOIL, stroke_width=8)
    crown = VGroup(*[
        Circle(radius=radius * s, stroke_color=color, stroke_width=3,
               fill_color=color, fill_opacity=0.48).move_to([x + dx, GROUND_Y + height + dy, 0])
        for dx, dy, s in ((-0.42, -0.08, 0.72), (0.0, 0.14, 0.9), (0.45, -0.08, 0.72))
    ])
    return VGroup(trunk, crown)


def seed_dots():
    buried = VGroup(*[Dot([x, GROUND_Y - 0.35 - 0.12 * (i % 2), 0], radius=0.09, color=EARLY)
                      for i, x in enumerate((-4.8, -3.6, -2.4, -0.8, 0.5, 2.2, 3.7))])
    return buried


def sun_beams(opacity=0.22, gap=None):
    xs = (-4.7, -2.4, 0.0, 2.4, 4.7) if gap is None else gap
    beams = VGroup()
    for x in xs:
        beam = Polygon([x - 0.42, 3.55, 0], [x + 0.42, 3.55, 0],
                       [x + 0.18, GROUND_Y + 0.04, 0], [x - 0.18, GROUND_Y + 0.04, 0],
                       stroke_width=0, fill_color=LIGHT, fill_opacity=opacity)
        beams.add(beam)
    beams._shimmer_t = 0.0

    def shimmer(mob, dt):
        mob._shimmer_t += dt
        value = max(0.03, opacity + 0.07 * np.sin(1.15 * mob._shimmer_t))
        for beam in mob:
            beam.set_fill(opacity=value)
    beams.add_updater(shimmer)
    return beams


def field_world(stage="open", beams=True, roots=False):
    """The one carried landscape, always on the same coordinates."""
    world = VGroup()
    if beams:
        world.add(sun_beams(0.20 if stage == "open" else 0.08))
    ground = soil_strip()
    world.add(ground)
    if roots:
        roots_m = VGroup(*[
            Line([x, GROUND_Y, 0], [x + 0.18 * (-1 if i % 2 else 1), GROUND_Y - 0.65, 0],
                 color=SOIL, stroke_width=4)
            for i, x in enumerate((-4.2, -2.8, -1.0, 0.9, 2.7, 4.3))
        ])
        world.add(roots_m, seed_dots())
    if stage == "open":
        world.add(grass_patch(-4.4, 2.5, 0.65, 9, phase=0.2),
                  grass_patch(-1.4, 2.7, 0.72, 10, phase=1.0),
                  grass_patch(1.8, 2.7, 0.67, 10, phase=2.0),
                  grass_patch(4.6, 2.1, 0.6, 8, phase=2.8))
    elif stage == "young":
        world.add(grass_patch(-4.7, 2.2, 1.0, 8), grass_patch(-1.6, 2.2, 1.45, 8, phase=1),
                  grass_patch(1.4, 2.1, 1.2, 8, phase=2),
                  pine_tree(3.3, 1.65, 0.72), pine_tree(4.6, 2.0, 0.86))
    elif stage == "canopy":
        for x, h in ((-4.7, 3.9), (-3.0, 4.25), (-1.15, 4.0), (0.8, 4.2), (2.75, 4.05), (4.65, 4.2)):
            world.add(pine_tree(x, h, 2.0))
    elif stage == "mixed":
        world.add(pine_tree(-4.8, 3.9, 1.7), pine_tree(-2.7, 4.0, 1.8),
                  hardwood_tree(-0.35, 3.45, 0.82), hardwood_tree(2.0, 3.75, 0.9),
                  hardwood_tree(4.55, 3.55, 0.86))
    return world


def mower():
    body = RoundedRectangle(corner_radius=0.12, width=1.55, height=0.58, stroke_color=RED,
                            fill_color=RED, fill_opacity=0.65, stroke_width=3)
    body.move_to([-4.4, -0.82, 0])
    wheels = VGroup(Circle(0.18, color=TEXT, fill_opacity=0.7).move_to([-4.85, -1.18, 0]),
                    Circle(0.18, color=TEXT, fill_opacity=0.7).move_to([-3.95, -1.18, 0]))
    handle = Line([-3.75, -0.65, 0], [-3.1, 0.2, 0], color=RED, stroke_width=6)
    return VGroup(body, wheels, handle)


def seedling_pair(with_question=False):
    canopy = VGroup(
        Rectangle(width=12.6, height=0.48, stroke_color=PINE, fill_color=PINE,
                  fill_opacity=0.32, stroke_width=3).move_to([0, 2.65, 0]),
        *[Circle(0.7, stroke_color=PINE, fill_color=PINE, fill_opacity=0.38, stroke_width=3)
          .move_to([x, 2.55 + 0.12 * (i % 2), 0]) for i, x in enumerate(np.linspace(-5.8, 5.8, 9))]
    )
    ground = soil_strip(y=-1.45, height=0.65)
    pine = pine_tree(-2.5, 2.1, 1.0)
    pine.shift(DOWN * 0.1)
    hard = hardwood_tree(2.5, 1.65, 0.46)
    labels = VGroup(T("pine", 30, PINE).move_to([-2.5, -2.42, 0]),
                    T("hardwood", 30, ORANGE).move_to([2.5, -2.42, 0]))
    out = VGroup(sun_beams(0.08, (-4.8, 0, 4.8)), canopy, ground, pine, hard, labels)
    if with_question:
        out.add(T("?", 78, LIGHT, weight=BOLD).move_to([0, 0.0, 0]))
    return out


def causal_ribbon(y=2.65):
    labels = [chip("organisms grow", EARLY, 28), chip("conditions change", LIGHT, 28),
              chip("suited species increase", ORANGE, 28)]
    for lab, x in zip(labels, (-4.45, 0, 4.45)):
        lab.move_to([x, y, 0])
    arrows = VGroup(Arrow(labels[0].get_right(), labels[1].get_left(), buff=0.18, color=BLUE, stroke_width=5),
                    Arrow(labels[1].get_right(), labels[2].get_left(), buff=0.18, color=BLUE, stroke_width=5))
    backing = RoundedRectangle(corner_radius=0.16, width=12.35, height=0.7, stroke_width=0,
                               fill_color=BG, fill_opacity=0.94).move_to([0, y, 0]).set_z_index(1)
    for item in (*labels, arrows):
        item.set_z_index(2)
    return VGroup(*labels, arrows, backing)


class S00Hook(SpokenScene):
    def construct(self):
        world = field_world("open", roots=True)
        self.play(FadeIn(world), run_time=1.2)
        self.at("why does a sunny field")
        sweep = sun_beams(0.28)
        self.play(FadeIn(sweep), sweep.animate.shift(RIGHT * 0.18), run_time=2.5)
        self.at("Watch one Virginia")
        tag = scope_tag("schematic")
        self.play(FadeIn(tag), run_time=0.5)
        self.at("The mower leaves")
        mow = mower()
        self.play(FadeIn(mow), mow.animate.shift(LEFT * 3.2), run_time=1.7)
        self.remove(mow)
        self.at("Seeds already in soil")
        buried = seed_dots()
        rising = VGroup(*[d.copy() for d in buried[:4]])
        self.play(FadeIn(buried), FadeIn(rising), rising.animate.shift(UP * 0.72), run_time=1.4)
        self.at("while others arrive")
        incoming = VGroup(*[Dot([6.5 + i * 0.22, 0.7 + 0.25 * (i % 2), 0], radius=0.09, color=EARLY)
                            for i in range(5)])
        bird = VGroup(ArcBetweenPoints([5.5, 2.2, 0], [5.9, 2.2, 0], angle=-1.0, color=TEXT),
                      ArcBetweenPoints([5.9, 2.2, 0], [6.3, 2.2, 0], angle=-1.0, color=TEXT))
        self.play(FadeIn(bird), FadeIn(incoming), incoming.animate.shift(LEFT * 4.0 + DOWN * 1.0),
                  bird.animate.shift(LEFT * 2.0), run_time=2.1)
        self.finish()


class S01Title(NarratedScene):
    def construct(self):
        world = field_world("open", roots=True)
        title = fit_text("How a Field Changes Its Future", max_w=11.5, size=52,
                         color=TEXT, font=TITLE_FONT).move_to([0, 1.15, 0])
        rule = Line([-2.2, 0.55, 0], [2.2, 0.55, 0], color=GOLD, stroke_width=5)
        self.add(world, scope_tag("schematic"))
        self.play(Write(title), GrowFromCenter(rule), run_time=0.9)
        self.wait(0.45)
        self.play(FadeOut(title), FadeOut(rule), run_time=0.55)
        self.finish()


class S02Name(SpokenScene):
    def construct(self):
        world = field_world("open")
        self.add(world, scope_tag("schematic"))
        self.at("Many populations")
        highlights = VGroup(*[SurroundingRectangle(world[i], color=BLUE, buff=0.08, stroke_width=2)
                              for i in range(2, min(len(world), 6))])
        self.play(LaggedStart(*[Create(h) for h in highlights], lag_ratio=0.12), run_time=1.6)
        self.at("forming a community")
        community = T("community", 34, BLUE, weight=BOLD).move_to([0, 2.65, 0])
        brace = Brace(world[2:], UP, color=BLUE)
        self.play(ReplacementTransform(highlights, brace), FadeIn(community), run_time=1.2)
        self.at("Ecological succession")
        self.play(FadeOut(brace), FadeOut(community), run_time=0.7)
        arrow = Arrow([-5.8, 2.65, 0], [5.8, 2.65, 0], color=BLUE, stroke_width=7, buff=0)
        self.play(GrowArrow(arrow), run_time=2.3)
        self.at("over years to centuries")
        older = field_world("young", beams=False)
        world.clear_updaters(recursive=True)
        self.play(Transform(world, older), run_time=2.4)
        self.at("general pattern")
        general = T("general pattern", 30, BLUE).next_to(arrow, UP, buff=0.12)
        varies = T("timing varies", 30, LIGHT).next_to(arrow, DOWN, buff=0.12)
        self.play(FadeIn(general), run_time=0.6)
        self.at("but not a fixed")
        self.play(FadeIn(varies), arrow.animate.set_stroke(opacity=0.65), run_time=1.0)
        self.finish()


class S03Open(SpokenScene):
    def construct(self):
        world = field_world("open")
        self.add(world, scope_tag("schematic"))
        self.at("Weeds and grasses")
        self.play(world[2:].animate.stretch(1.45, 1, about_edge=DOWN), run_time=2.2)
        self.at("Broomsedge and blackberry")
        tall = VGroup(grass_patch(-1.7, 2.4, 1.9, 9, phase=1.2),
                      grass_patch(1.2, 2.1, 1.65, 8, color=EARLY, phase=2.4))
        labels = VGroup(T("broomsedge", 28, EARLY).move_to([-1.8, 1.15, 0]),
                        T("blackberry", 28, EARLY).move_to([1.2, 0.95, 0]))
        self.play(LaggedStart(FadeIn(tall), FadeIn(labels), lag_ratio=0.25), run_time=2.2)
        self.at("Pine seedlings appear")
        seed_trees = VGroup(pine_tree(5.0, 4.1, 1.75), pine_tree(6.1, 4.45, 1.85))
        saplings = VGroup(pine_tree(3.1, 1.55, 0.66), pine_tree(4.0, 1.9, 0.78))
        self.play(FadeIn(seed_trees), FadeIn(saplings, shift=LEFT * 0.3), run_time=2.4)
        self.at("Their crowns climb")
        target = VGroup(pine_tree(3.1, 2.6, 1.02), pine_tree(4.0, 3.0, 1.12))
        self.play(Transform(saplings, target), sun_beams(0.24).animate.set_opacity(0.38), run_time=2.4)
        self.at("sunny field begins")
        future = Arrow([2.7, 2.5, 0], [0.2, 2.5, 0], color=LIGHT, stroke_width=6)
        self.play(GrowArrow(future), FadeOut(labels), run_time=1.5)
        self.finish()


class S04Canopy(SpokenScene):
    def construct(self):
        young = field_world("young")
        young.layout_ok = True  # carried landscape is the deliberate backdrop for gauge/labels
        self.add(young, scope_tag("schematic"))
        self.at("pines grow taller")
        canopy = field_world("canopy")
        young.clear_updaters(recursive=True)
        self.play(Transform(young, canopy), run_time=2.5)
        self.at("canopy now blocks")
        shade = Rectangle(width=12.5, height=2.2, stroke_width=0, fill_color=BG,
                          fill_opacity=0.50).move_to([0, -0.15, 0])
        self.play(FadeIn(shade), run_time=2.0)
        self.at("light meter falls")
        light = ValueTracker(0.82)
        gauge = dial(light, center=[4.8, -0.1, 0], radius=1.05, label="ground light", color=LIGHT)
        gauge.layout_ok = True  # dial needle/readout and label are one standard component
        self.add(gauge)
        self.play(light.animate.set_value(0.18), run_time=2.2)
        self.at("New pine seedlings")
        small_pine = pine_tree(-1.7, 1.25, 0.55)
        self.play(FadeIn(small_pine), small_pine.animate.scale(0.82, about_edge=DOWN), run_time=1.6)
        self.at("young hardwoods")
        hardwoods = VGroup(hardwood_tree(0.3, 1.3, 0.38), hardwood_tree(2.0, 1.45, 0.4))
        label = T("can survive shade", 28, ORANGE).move_to([0.8, -3.12, 0])
        self.play(FadeIn(hardwoods), FadeIn(label), run_time=2.0)
        self.finish()


class S05Predict(SpokenScene):
    QUESTION = "Which is more likely to persist in the shade?"

    def construct(self):
        pair = seedling_pair(with_question=False)
        light = ValueTracker(0.18)
        gauge = dial(light, center=[5.25, 0.0, 0], radius=0.82, label="low light", color=LIGHT, size=30)
        self.add(pair, gauge, scope_tag("schematic"))
        self.at("Two seedlings")
        self.play(pair[3].animate.shift(UP * 0.1), pair[4].animate.shift(UP * 0.1), run_time=1.8)
        self.at("One is pine")
        self.play(Indicate(pair[3], color=PINE), run_time=0.9)
        self.at("one is hardwood")
        self.play(Indicate(pair[4], color=ORANGE), run_time=0.9)
        self.at("which is more likely")
        mark = T("?", 78, LIGHT, weight=BOLD).move_to([0, 0.0, 0])
        self.play(FadeIn(mark, scale=0.7), run_time=1.1)
        self.at("Make your prediction")
        q = question_card(self.QUESTION, y=-3.25, size=28, max_w=10.4)
        self.play(FadeIn(q), run_time=0.8)
        self.finish()


class S06Pause(PredictPause):
    QUESTION = "Which is more likely to persist in the shade?"
    SECONDS = 4.5
    CARD = {"y": -3.25, "size": 28, "max_w": 10.4}

    def backdrop(self):
        pair = seedling_pair(with_question=True)
        light = ValueTracker(0.18)
        gauge = dial(light, center=[5.25, 0.0, 0], radius=0.82, label="low light", color=LIGHT, size=30)
        return VGroup(pair, gauge)


class S07Reveal(SpokenScene):
    def construct(self):
        pair = seedling_pair(with_question=True)
        self.add(pair, scope_tag("schematic"))
        self.at("pine seedling lags")
        self.play(FadeOut(pair[-1]), pair[3].animate.scale(0.72, about_edge=DOWN),
                  pair[4].animate.shift(UP * 0.12), run_time=2.0)
        self.at("old pine dies")
        forest = field_world("canopy")
        forest.layout_ok = True  # landscape stays behind the causal overlay
        self.play(ReplacementTransform(pair, forest), run_time=1.7)
        dead = VGroup(Line([-1.15, GROUND_Y, 0], [-1.15, 2.25, 0], color=GREY, stroke_width=10),
                      Line([-1.15, 1.0, 0], [-1.75, 1.55, 0], color=GREY, stroke_width=6))
        dead.layout_ok = True  # later becomes part of the dimmed causal backdrop
        self.play(FadeOut(forest[4]), FadeIn(dead), run_time=1.6)
        self.at("opens a bright gap")
        gap = sun_beams(0.38, (-1.15,))
        gap.layout_ok = True
        self.play(FadeIn(gap), run_time=1.4)
        self.at("hardwood grows faster")
        hard = hardwood_tree(-1.15, 1.4, 0.42)
        hard.layout_ok = True
        grown = hardwood_tree(-1.15, 3.25, 0.85)
        self.play(FadeIn(hard), Transform(hard, grown), run_time=2.6)
        self.at("No plant planned")
        no_goal = T("no plan • no goal", 30, GREY).move_to([2.4, -3.12, 0])
        self.play(FadeIn(no_goal), run_time=1.2)
        self.at("Growth altered conditions")
        steps = VGroup(chip("growth", EARLY, 26), chip("light changes", LIGHT, 26),
                       chip("different survival", ORANGE, 26)).arrange(RIGHT, buff=0.6).move_to([0, 3.28, 0])
        steps.layout_ok = True  # labels intentionally sit on chips over an opaque reading band
        links = VGroup(Arrow(steps[0].get_right(), steps[1].get_left(), buff=0.12, color=BLUE),
                       Arrow(steps[1].get_right(), steps[2].get_left(), buff=0.12, color=BLUE))
        backing = RoundedRectangle(corner_radius=0.16, width=11.4, height=0.7, stroke_width=0,
                                   fill_color=BG, fill_opacity=0.94).move_to([0, 3.28, 0]).set_z_index(1)
        for item in (steps, links):
            item.set_z_index(2)
        self.play(FadeOut(no_goal),
                  FadeIn(backing), LaggedStart(FadeIn(steps), Create(links), lag_ratio=0.25), run_time=2.3)
        self.finish()


class S08Rule(SpokenScene):
    def construct(self):
        world = field_world("mixed")
        world.layout_ok = True  # the carried field is a dimmed explanatory backdrop
        ribbon = causal_ribbon(3.28)
        self.add(world, scope_tag("schematic"))
        self.at("Organisms change conditions")
        self.play(LaggedStart(FadeIn(ribbon[0]), GrowArrow(ribbon[3][0]), FadeIn(ribbon[1]),
                              GrowArrow(ribbon[3][1]), FadeIn(ribbon[2]), lag_ratio=0.18), run_time=3.8)
        self.at("pine growth changed light")
        light = sun_beams(0.26, (-3.7, -1.8))
        self.play(FadeIn(light), Indicate(ribbon[1], color=LIGHT), run_time=1.7)
        self.at("plants also change soil")
        rich_soil = soil_strip(height=1.45)
        self.play(Transform(world[1], rich_soil), run_time=1.8)
        soil_lab = T("soil", 28, SOIL).move_to([4.9, -2.45, 0])
        self.play(FadeIn(soil_lab), run_time=0.6)
        self.at("pattern comes from survival")
        self.play(world[3].animate.set_opacity(0.45), world[4].animate.scale(1.08, about_edge=DOWN),
                  run_time=2.0)
        self.at("not from a goal")
        rule = caption("survival + growth, not a finish line", 30, TEXT, y=-3.18)
        self.play(FadeOut(soil_lab), FadeIn(rule), run_time=1.2)
        self.finish()


def surface_panels():
    panels = TwoPanel("abandoned field", "bare rock", colors=(SOIL, GREY), top=3.0, bottom=-2.45)
    left_ground = Rectangle(width=5.2, height=1.35, stroke_color=SOIL, fill_color=SOIL,
                            fill_opacity=0.45, stroke_width=3).move_to([-3.25, -0.9, 0])
    left = VGroup(left_ground, grass_patch(-3.25, 3.8, 1.3, 10),
                  VGroup(*[Dot([x, -1.25, 0], radius=0.08, color=EARLY) for x in (-4.5, -3.6, -2.7, -1.9)]),
                  VGroup(*[Line([x, -0.25, 0], [x + 0.18, -1.55, 0], color=SOIL, stroke_width=4)
                           for x in (-4.2, -3.0, -2.0)]))
    rock = Polygon([-5.2, -1.5, 0], [5.2, -1.5, 0], [5.0, -0.15, 0], [3.0, 0.08, 0],
                   [0.5, -0.02, 0], [-2.8, 0.15, 0], [-5.1, -0.2, 0],
                   stroke_color=GREY, fill_color=GREY, fill_opacity=0.35, stroke_width=3)
    rock.scale(0.48).move_to([3.25, -0.75, 0])
    return panels, left, rock


class S09Soil(SpokenScene):
    def construct(self):
        field = field_world("open", roots=True)
        self.add(field, scope_tag("schematic"))
        self.at("compare two starting surfaces")
        panels, left, rock = surface_panels()
        self.play(FadeOut(field), FadeIn(panels), run_time=1.8)
        self.at("abandoned field still has soil")
        self.play(FadeIn(left), run_time=1.7)
        self.at("nutrients")
        items = T("soil • nutrients • seeds • roots", 28, SOIL).move_to([-3.25, -2.1, 0])
        self.play(FadeIn(items), run_time=1.2)
        self.at("secondary succession")
        sec = T("secondary succession", 30, SOIL, weight=BOLD).move_to([-3.25, 2.0, 0])
        self.play(swap(panels.left_head, sec), run_time=0.9)
        self.at("Bear Rock has no soil")
        self.play(FadeIn(rock), run_time=1.7)
        no_soil = T("no soil", 30, GREY).move_to([3.25, -2.0, 0])
        self.play(FadeIn(no_soil), run_time=0.8)
        self.at("Primary succession")
        prim = T("primary succession", 30, GREY, weight=BOLD).move_to([3.25, 2.0, 0])
        self.play(swap(panels.right_head, prim), run_time=1.0)
        self.at("pioneer species")
        pioneers = VGroup(*[Circle(0.12, color=EARLY, fill_color=EARLY, fill_opacity=0.7)
                            .move_to([x, -0.55 + 0.12 * (i % 2), 0]) for i, x in enumerate((2.0, 2.5, 3.1, 3.8, 4.4))])
        self.play(LaggedStart(*[FadeIn(p) for p in pioneers], lag_ratio=0.15), run_time=1.5)
        self.finish()


class S10Rock(SpokenScene):
    def construct(self):
        panels, left, rock = surface_panels()
        self.add(panels, left, rock, scope_tag("schematic"))
        self.at("pioneers are usually")
        patches = VGroup(*[Circle(0.16 + 0.03 * (i % 2), color=EARLY, fill_color=EARLY,
                                  fill_opacity=0.65).move_to([x, -0.45, 0])
                           for i, x in enumerate((1.7, 2.2, 2.8, 3.5, 4.1, 4.7))])
        self.play(LaggedStart(*[GrowFromCenter(p) for p in patches], lag_ratio=0.12), run_time=2.0)
        names = T("lichens + mosses", 28, EARLY).move_to([3.25, 1.45, 0])
        self.play(FadeIn(names), run_time=0.8)
        self.at("Glacial gravel")
        gravel = VGroup(*[Dot([1.7 + 0.35 * i, 0.55 + 0.12 * (i % 2), 0], radius=0.10, color=GREY)
                          for i in range(5)])
        hardy = grass_patch(2.4, 1.4, 0.55, 5, phase=1.5)
        hardy.shift(UP * 1.85)
        self.play(FadeIn(gravel), FadeIn(hardy), run_time=1.8)
        self.at("Soil develops slowly")
        thin_soil = Rectangle(width=4.8, height=0.12, stroke_color=SOIL, fill_color=SOIL,
                              fill_opacity=0.65, stroke_width=2).move_to([3.25, -0.2, 0])
        thick_soil = thin_soil.copy().stretch(3.5, 1, about_edge=UP)
        self.play(FadeIn(thin_soil), Transform(thin_soil, thick_soil), run_time=2.8)
        self.at("rooted plants can establish")
        rooted = grass_patch(3.4, 3.4, 1.0, 8, phase=2.5)
        rooted.shift(UP * 1.15)
        self.play(FadeIn(rooted), run_time=1.5)
        self.at("Starting with soil")
        fast = Line([-5.2, -2.1, 0], [-1.3, -2.1, 0], color=SOIL, stroke_width=12)
        slow = Line([1.3, -2.1, 0], [3.6, -2.1, 0], color=GREY, stroke_width=12)
        labs = VGroup(T("usually faster", 26, SOIL).next_to(fast, UP, buff=0.12),
                      T("usually slower", 26, GREY).next_to(slow, UP, buff=0.12))
        self.play(Create(fast), Create(slow), FadeIn(labs), run_time=2.4)
        self.finish()


class S11Tendency(SpokenScene):
    def construct(self):
        world = field_world("young")
        world.layout_ok = True  # field remains visible behind model/path labels
        self.add(world, scope_tag("schematic"))
        self.at("pines may give way")
        mixed = field_world("mixed")
        world.clear_updaters(recursive=True)
        self.play(Transform(world, mixed), run_time=3.0)
        self.at("older model names")
        panel = RoundedRectangle(corner_radius=0.16, width=7.4, height=1.1, stroke_color=ORANGE,
                                 stroke_width=2, fill_color=BG, fill_opacity=0.94).move_to([0, 3.2, 0])
        panel.layout_ok = True  # two labels intentionally sit on this reading panel
        late = fit_text("model late stage in most of Virginia", max_w=6.9, size=28,
                        color=ORANGE).move_to([0, 3.45, 0])
        self.play(FadeIn(panel), FadeIn(late), run_time=1.6)
        self.at("ochickery forest")
        oak = T("oak–hickory forest", 30, ORANGE, weight=BOLD).move_to([0, 2.93, 0])
        self.play(FadeIn(oak), run_time=1.1)
        self.at("nearby seeds")
        route = Arrow([-5.7, -2.75, 0], [5.6, -2.75, 0], color=BLUE, stroke_width=5, buff=0)
        self.play(GrowArrow(route), run_time=1.3)
        factors = VGroup(*[chip(t, c, 25) for t, c in (("seeds", EARLY), ("soil", SOIL),
                                                        ("climate", LIGHT), ("disturbance", RED))])
        factors.arrange(RIGHT, buff=0.3).move_to([0, -2.95, 0])
        branches = VGroup(*[Arrow([x, -2.65, 0], [x + dx, -1.95, 0], color=c, stroke_width=3, buff=0.08)
                            for (x, dx, c) in ((-3.9, -0.5, EARLY), (-1.4, -0.25, SOIL),
                                               (1.1, 0.25, LIGHT), (3.7, 0.55, RED))])
        self.play(FadeOut(route), LaggedStart(*[FadeIn(f) for f in factors], lag_ratio=0.12),
                  LaggedStart(*[GrowArrow(a) for a in branches], lag_ratio=0.12), run_time=2.8)
        self.finish()


class S12Close(SpokenScene):
    def construct(self):
        world = field_world("mixed")
        world.layout_ok = True  # dimmed field deliberately sits behind the summary controls
        ribbon = causal_ribbon(3.28)
        self.add(world, ribbon, scope_tag("schematic"))
        self.at("Follow the changing conditions")
        light = ValueTracker(0.25)
        soil = ValueTracker(0.45)
        meters = VGroup(dial(light, [-6.2, 0.2, 0], radius=0.6, label="light", color=LIGHT, size=24),
                        dial(soil, [6.2, 0.2, 0], radius=0.6, label="soil", color=SOIL, size=24))
        meters.layout_ok = True  # needles, live numbers, and labels form two standard dials
        self.play(FadeIn(meters), light.animate.set_value(0.75), soil.animate.set_value(0.8), run_time=2.8)
        self.at("not only the plant names")
        self.play(world.animate.set_opacity(0.45), run_time=1.1)
        self.at("explains why one stage")
        self.play(Indicate(ribbon[1], color=LIGHT), Indicate(ribbon[2], color=ORANGE), run_time=2.2)
        self.at("common path")
        paths = VGroup(*[CubicBezier([-5.5, -2.4 + 0.2 * i, 0], [-2.0, -1.7 + 0.1 * i, 0],
                                    [1.5, -2.8 + 0.35 * i, 0], [5.4, -2.15 + 0.22 * i, 0],
                                    color=BLUE, stroke_width=3, stroke_opacity=0.32)
                         for i in range(4)])
        self.play(LaggedStart(*[Create(p) for p in paths], lag_ratio=0.18), run_time=2.2)
        self.at("promise about every field")
        promise = caption("a common path is not a promise", 30, TEXT, y=-3.2)
        self.play(FadeIn(promise), run_time=1.2)
        self.finish()


class S13End(EndCard):
    LINE = "Organisms change conditions, so suited species can become more common."
