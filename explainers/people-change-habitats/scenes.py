"""One Change, Many Ripples — people change habitats.

COLOR MAP (fixed for the whole film)
  BLUE  introduced blue catfish
  GOLD  native white catfish
  TEAL  crabs, small fish, and shared prey
  GREEN healthy shoreline habitat
  RED   human pressures
  TEXT  other labels and evidence
"""
from bp_parts import *


# ---------------------------------------------------------------------------
# Reusable drawings.  Every carried picture is rebuilt through these builders.

def fish(color, scale=1.0, facing=RIGHT):
    """A labelled-animal cartoon, deliberately not an anatomical drawing."""
    body = Ellipse(width=1.55, height=0.72, color=color, stroke_width=4,
                   fill_color=color, fill_opacity=0.30)
    tail = Polygon([-0.68, 0, 0], [-1.18, 0.42, 0], [-1.18, -0.42, 0],
                   color=color, stroke_width=4, fill_color=color, fill_opacity=0.24)
    eye = Dot([0.44, 0.12, 0], radius=0.055, color=TEXT)
    whiskers = VGroup(
        ArcBetweenPoints([0.67, -0.05, 0], [1.02, -0.24, 0], angle=-0.35,
                         color=color, stroke_width=2.5),
        ArcBetweenPoints([0.65, -0.10, 0], [0.96, -0.38, 0], angle=-0.35,
                         color=color, stroke_width=2.5),
    )
    g = VGroup(tail, body, eye, whiskers).scale(scale)
    if np.dot(np.array(facing)[:2], np.array(RIGHT)[:2]) < 0:
        g.flip(UP)
    return g


def crab(scale=1.0):
    body = RoundedRectangle(corner_radius=0.18, width=0.78, height=0.48,
                            color=TEAL, stroke_width=3, fill_color=TEAL, fill_opacity=0.28)
    claws = VGroup(
        Arc(radius=0.22, start_angle=0.2, angle=1.7, color=TEAL, stroke_width=3).shift(LEFT * 0.52 + UP * 0.22),
        Arc(radius=0.22, start_angle=1.2, angle=1.7, color=TEAL, stroke_width=3).shift(RIGHT * 0.52 + UP * 0.22),
    )
    legs = VGroup(*[
        Line([sx * 0.30, yy, 0], [sx * 0.62, yy - 0.16, 0], color=TEAL, stroke_width=2.5)
        for sx in (-1, 1) for yy in (-0.14, 0.06)
    ])
    return VGroup(legs, claws, body).scale(scale)


def prey_fish(scale=1.0):
    return fish(TEAL, 0.38 * scale)


def person(scale=1.0):
    head = Circle(radius=0.16, color=TEXT, stroke_width=4).shift(UP * 0.73)
    body = Line([0, 0.55, 0], [0, -0.25, 0], color=TEXT, stroke_width=5)
    limbs = VGroup(
        Line([0, 0.28, 0], [-0.38, -0.05, 0], color=TEXT, stroke_width=4),
        Line([0, 0.28, 0], [0.42, -0.02, 0], color=TEXT, stroke_width=4),
        Line([0, -0.25, 0], [-0.32, -0.78, 0], color=TEXT, stroke_width=4),
        Line([0, -0.25, 0], [0.32, -0.78, 0], color=TEXT, stroke_width=4),
    )
    return VGroup(head, body, limbs).scale(scale)


def home(scale=1.0, color=RED):
    walls = Rectangle(width=1.0, height=0.72, color=color, stroke_width=4,
                      fill_color=color, fill_opacity=0.18).shift(DOWN * 0.18)
    roof = Polygon([-0.62, 0.18, 0], [0, 0.72, 0], [0.62, 0.18, 0],
                   color=color, stroke_width=4, fill_color=color, fill_opacity=0.18)
    window = Square(0.22, color=YELLOW, fill_color=YELLOW, fill_opacity=0.75).shift(DOWN * 0.15)
    return VGroup(walls, roof, window).scale(scale)


def population_bar(color, height=2.1, label="population", x=5.35, base_y=-1.75):
    frame = RoundedRectangle(corner_radius=0.12, width=1.05, height=3.0, color=GREY,
                             stroke_width=2.5).move_to([x, base_y + 1.5, 0])
    fill = Rectangle(width=0.78, height=height, color=color, stroke_width=0,
                     fill_color=color, fill_opacity=0.72)
    fill.move_to([x, base_y + height / 2, 0])
    lab = fit_text(label, max_w=1.9, size=26, color=color, max_lines=2).next_to(frame, UP, buff=0.14)
    tag = T("schematic", 24, GREY).next_to(frame, DOWN, buff=0.12)
    tag.layout_ok = True  # deliberate small scope label required by the script
    g = VGroup(frame, fill, lab, tag)
    g.fill = fill
    g.frame = frame
    return g


def compact_population_bar(color, height=1.25, label="population", center=(5.4, 1.0, 0),
                           frame_h=2.15, show_tag=True):
    """A genuinely compact bar; its text is never geometrically scaled."""
    x, y, _ = center
    frame = RoundedRectangle(corner_radius=0.10, width=0.92, height=frame_h, color=GREY,
                             stroke_width=2.5).move_to([x, y, 0])
    base = y - frame_h / 2 + 0.12
    fill = Rectangle(width=0.66, height=height, color=color, stroke_width=0,
                     fill_color=color, fill_opacity=0.72).move_to([x, base + height / 2, 0])
    lab = fit_text(label, max_w=1.65, size=27, color=color, min_size=22,
                   max_lines=2).next_to(frame, UP, buff=0.2)
    tag = T("schematic", 22, GREY).next_to(frame, DOWN, buff=0.08)
    tag.layout_ok = True
    g = VGroup(frame, fill, lab, tag) if show_tag else VGroup(frame, fill, lab)
    g.frame, g.fill = frame, fill
    return g


def shared_tag(bars, y_pad=0.08):
    """One 'schematic' tag centred under a row of bars (their own tags would touch)."""
    left = min(b.frame.get_left()[0] for b in bars)
    right = max(b.frame.get_right()[0] for b in bars)
    bottom = min(b.frame.get_bottom()[1] for b in bars)
    tag = T("schematic", 22, GREY).move_to([(left + right) / 2, bottom - y_pad - 0.17, 0])
    tag.layout_ok = True
    return tag


def _flow_updater(mob, dt):
    mob._flow_t = getattr(mob, "_flow_t", 0.0) + dt
    mob.set_x(-5.2 + (mob._flow_t * mob._flow_speed) % 10.4)


def river_world(with_blue=False, with_native=True, with_people=False, wide=True):
    """The carried river cross-section, always at the same coordinates and scale."""
    water = Rectangle(width=13.2, height=4.65, stroke_width=0, fill_color="#18384A",
                      fill_opacity=1).move_to([0, -0.55, 0])
    bed = Polygon([-6.6, -2.88, 0], [6.6, -2.88, 0], [6.6, -2.18, 0],
                  [3.6, -2.35, 0], [0.4, -2.08, 0], [-3.2, -2.32, 0], [-6.6, -2.08, 0],
                  color=GOLD, stroke_width=3, fill_color="#5A4930", fill_opacity=0.9)
    bank = Polygon([-6.6, 3.0, 0], [-3.85, 3.0, 0], [-3.25, 1.75, 0], [-6.6, 1.75, 0],
                   color=GREEN, stroke_width=3, fill_color="#26472E", fill_opacity=1)
    grasses = VGroup(*[
        Line([x, 1.78, 0], [x + 0.12 * (-1) ** i, 2.72 - 0.10 * (i % 3), 0],
             color=GREEN, stroke_width=6)
        for i, x in enumerate(np.linspace(-6.2, -3.7, 10))
    ])
    roots = VGroup(*[
        Line([x, 1.78, 0], [x + 0.16 * (-1) ** i, 0.20 - 0.12 * (i % 3), 0],
             color=GREEN, stroke_width=4)
        for i, x in enumerate(np.linspace(-6.0, -3.8, 8))
    ])
    currents = VGroup(*[
        Line([-5.2, y, 0], [-4.25, y, 0], color=TEAL, stroke_width=3).set_opacity(0.55)
        for y in (-1.55, -0.72, 0.10, 0.88)
    ])
    for i, line in enumerate(currents):
        line._flow_speed = 0.32 + 0.05 * i
        line.add_updater(_flow_updater)
    world = VGroup(water, bed, bank, grasses, roots, currents)
    world.water, world.bed, world.bank = water, bed, bank
    world.grasses, world.roots, world.currents = grasses, roots, currents
    if with_native:
        natives = VGroup(
            fish(GOLD, 0.72).move_to([-1.8, 0.45, 0]),
            fish(GOLD, 0.68).move_to([0.15, -0.58, 0]),
            fish(GOLD, 0.62).move_to([1.85, 0.48, 0]),
        )
        for i, f in enumerate(natives):
            bob(f, amp=0.055, speed=1.2, seed=i)
        world.add(natives)
        world.natives = natives
    prey = VGroup(
        prey_fish(0.9).move_to([-3.8, -0.45, 0]),
        prey_fish(0.82).move_to([-2.9, -1.25, 0]),
        crab(0.64).move_to([-4.75, -1.72, 0]),
    )
    for i, p in enumerate(prey):
        bob(p, amp=0.045, speed=1.45, seed=i + 4)
    world.add(prey)
    world.prey = prey
    if with_blue:
        blues = VGroup(
            fish(BLUE, 0.78).move_to([2.9, -0.45, 0]),
            fish(BLUE, 0.70).move_to([3.95, 0.58, 0]),
        )
        for i, f in enumerate(blues):
            bob(f, amp=0.055, speed=1.25, seed=i + 7)
        world.add(blues)
        world.blues = blues
    if with_people:
        people = VGroup(person(0.78).move_to([-5.5, 3.05, 0]), home(0.82, TEXT).move_to([-4.05, 2.75, 0]))
        world.add(people)
        world.people = people
    return world


def release_arrow():
    return CurvedArrow([-5.28, 2.95, 0], [-2.95, 0.92, 0], angle=-0.45,
                       color=BLUE, stroke_width=7, tip_length=0.24)


def prey_world(question=False, half_bar=False, sparse=False):
    """The carried close-up used without drift in s05–s08."""
    water = Rectangle(width=13.2, height=6.35, stroke_width=0, fill_color="#18384A",
                      fill_opacity=1).move_to([0, -0.15, 0])
    currents = VGroup(*[
        Line([-5.2, y, 0], [-4.15, y, 0], color=TEAL, stroke_width=3).set_opacity(0.42)
        for y in (-2.1, -1.2, 1.1, 2.0)
    ])
    for i, line in enumerate(currents):
        line._flow_speed = 0.30 + i * 0.045
        line.add_updater(_flow_updater)
    pool = RoundedRectangle(corner_radius=0.28, width=4.3, height=3.35, color=TEAL,
                            stroke_width=5, fill_color=TEAL, fill_opacity=0.09).move_to([0, -0.2, 0])
    spots = [(-1.2, 0.65), (0.0, 0.72), (1.18, 0.55), (-1.15, -0.48), (0.1, -0.55), (1.18, -0.60)]
    items = VGroup()
    count = 3 if sparse else 6
    for i, (x, y) in enumerate(spots[:count]):
        p = (crab(0.52) if i in (1, 4) else prey_fish(0.82)).move_to([x, y - 0.2, 0])
        bob(p, amp=0.06, speed=1.35, seed=i)
        items.add(p)
    blue = fish(BLUE, 1.08).move_to([-3.9, -0.6, 0])
    gold = fish(GOLD, 1.08, LEFT).move_to([4.7, -0.6, 0])
    bob(blue, amp=0.055, speed=1.1, seed=2)
    bob(gold, amp=0.055, speed=1.1, seed=5)
    blue_lab = T("blue catfish", 28, BLUE).next_to(blue, DOWN, buff=0.17)
    gold_lab = T("white catfish", 28, GOLD).next_to(gold, DOWN, buff=0.17)
    pool_lab = T("shared prey", 30, TEAL, weight=BOLD).move_to([0, 2.38, 0])
    bar = compact_population_bar(BLUE, 1.35 if half_bar else 0.68, "blue\npopulation",
                                 center=(-5.68, 1.62, 0), frame_h=2.05)
    world = VGroup(water, currents, pool, items, blue, gold, blue_lab, gold_lab, pool_lab, bar)
    world.pool, world.items, world.blue, world.gold, world.bar = pool, items, blue, gold, bar
    world.currents = currents
    if question:
        q = fit_text("If blue catfish grow, what remains for white catfish?", max_w=10.2,
                     size=34, color=TEXT, max_lines=2).move_to([0.35, 3.20, 0])
        world.add(q)
        world.question = q
    return world


def arrow_between(a, b, color):
    return CurvedArrow(a, b, angle=0.22, color=color, stroke_width=6, tip_length=0.22)


def response_bars(question=False):
    labels = [("blue catfish", BLUE, 2.65), ("shared prey", TEAL, 1.65),
              ("crabs", TEAL, 1.25), ("small fish", TEAL, 1.85), ("white catfish", GOLD, 1.40)]
    bars = VGroup()
    for i, (lab, col, h) in enumerate(labels):
        x = -4.7 + i * 2.35
        frame = RoundedRectangle(corner_radius=0.10, width=1.28, height=3.15, color=GREY,
                                 stroke_width=2.5).move_to([x, -0.75, 0])
        fill = Rectangle(width=0.96, height=h, color=col, stroke_width=0,
                         fill_color=col, fill_opacity=0.72).move_to([x, -2.32 + h / 2, 0])
        text = fit_text(lab, max_w=2.0, size=28, color=col, max_lines=2).next_to(frame, UP, buff=0.13)
        tag = T("schematic", 24, GREY).next_to(frame, DOWN, buff=0.10)
        tag.layout_ok = True
        g = VGroup(frame, fill, text, tag)
        g.fill = fill
        bars.add(g)
    if question:
        q = T("may change", 34, TEXT, weight=BOLD).move_to([0, 3.22, 0])
        bars.question = q
        return bars
    return bars


# ---------------------------------------------------------------------------
# Scenes

class S00Hook(SpokenScene):
    def construct(self):
        world = river_world(with_blue=False, with_native=True, with_people=True)
        self.play(FadeIn(world), run_time=1.0)
        q = fit_text("How can one choice make one population rise while another falls?",
                     max_w=9.6, size=36, color=TEXT, max_lines=2).move_to([1.5, 3.23, 0])
        self.at("one human choice")
        self.play(FadeIn(q, shift=DOWN * 0.12), run_time=0.7)
        arrow = release_arrow()
        incoming = fish(BLUE, 0.70).move_to([-3.0, 0.92, 0])
        self.at("one river population rise")
        self.play(Create(arrow), FadeIn(incoming, scale=0.7), run_time=1.0)
        up = compact_population_bar(BLUE, 0.55, "blue", center=(4.45, 1.15, 0), show_tag=False)
        down = compact_population_bar(GOLD, 1.55, "white", center=(6.0, 1.15, 0), show_tag=False)
        self.play(FadeIn(up), FadeIn(down), FadeIn(shared_tag([up, down])), run_time=0.65)
        self.at("while another falls")
        self.play(up.fill.animate.stretch_to_fit_height(1.55).align_to(up.frame, DOWN),
                  down.fill.animate.stretch_to_fit_height(0.62).align_to(down.frame, DOWN), run_time=1.5)
        self.at("Watch one Virginia river")
        ring = SurroundingRectangle(world.water, color=TEXT, buff=0.04, stroke_width=4)
        self.play(Create(ring), run_time=0.4)
        self.play(FadeOut(ring), run_time=0.4)
        self.at("what each population can use")
        self.play(Indicate(world.prey, color=TEAL, scale_factor=1.14), run_time=0.9)
        self.finish()


class S01Title(TitleCard):
    LESSON = "People Change Habitats"
    TITLE = "One Change, Many Ripples"


class S02World(SpokenScene):
    def construct(self):
        world = river_world(with_native=False)
        self.play(FadeIn(VGroup(world.water, world.bed, world.bank, world.grasses, world.currents)), run_time=1.0)
        self.at("Green marsh plants")
        self.play(LaggedStart(*[Create(r) for r in world.roots], lag_ratio=0.08), run_time=1.3)
        self.at("Teal crabs and small fish")
        self.play(LaggedStart(*[FadeIn(p, shift=RIGHT * 0.12) for p in world.prey], lag_ratio=0.18), run_time=1.1)
        natives = VGroup(
            fish(GOLD, 0.82).move_to([-0.8, 0.45, 0]),
            fish(GOLD, 0.76).move_to([1.0, -0.55, 0]),
            fish(GOLD, 0.72).move_to([2.75, 0.45, 0]),
        )
        for i, f in enumerate(natives):
            bob(f, amp=0.055, speed=1.2, seed=i)
        self.at("Gold white catfish")
        self.play(LaggedStart(*[FadeIn(f, shift=LEFT * 0.2) for f in natives], lag_ratio=0.18), run_time=1.2)
        bracket = Brace(natives, UP, color=GOLD)
        label = T("one population: white catfish", 30, GOLD).next_to(bracket, UP, buff=0.14)
        self.at("All the white catfish")
        self.play(GrowFromCenter(bracket), FadeIn(label), run_time=0.9)
        self.at("shoreline shelters animals")
        self.play(Indicate(VGroup(world.roots, world.prey), color=GREEN, scale_factor=1.03), run_time=1.1)
        self.at("moving water carries food")
        self.play(world.prey.animate.shift(RIGHT * 0.75), run_time=1.4, rate_func=linear)
        self.finish()


class S03People(SpokenScene):
    def construct(self):
        world = river_world(with_native=True, with_people=False)
        self.add(world)
        p1 = person(0.82).move_to([-5.55, 3.00, 0])
        p2 = person(0.76).move_to([-4.45, 2.98, 0])
        house = home(0.82, TEXT).move_to([-3.45, 2.72, 0])
        self.at("People belong inside")
        self.play(FadeIn(p1), FadeIn(p2), FadeIn(house), run_time=1.0)
        basket = RoundedRectangle(corner_radius=0.12, width=0.72, height=0.42, color=GOLD,
                                  fill_color=GOLD, fill_opacity=0.18).move_to([-4.02, 2.67, 0])
        arrows = VGroup(
            Arrow([-5.45, 2.30, 0], [-4.8, 1.15, 0], color=TEAL, stroke_width=3, buff=0.08),
            Arrow([-4.05, 2.32, 0], [-2.65, 0.65, 0], color=GOLD, stroke_width=3, buff=0.08),
            Arrow([-3.35, 2.20, 0], [-2.05, 1.25, 0], color=TEXT, stroke_width=3, buff=0.08),
        )
        labels = VGroup(T("water", 28, TEAL), T("food", 28, GOLD), T("energy", 28, TEXT))
        for lab, pos in zip(labels, [(0.15, 2.72, 0), (1.65, 2.72, 0), (3.05, 2.72, 0)]):
            lab.move_to(pos)
        self.at("food water energy")
        self.play(FadeIn(basket), LaggedStart(*[GrowArrow(a) for a in arrows], lag_ratio=0.15),
                  LaggedStart(*[FadeIn(l) for l in labels], lag_ratio=0.15), run_time=1.5)
        choices = VGroup(T("habitat", 28, GREEN), T("resources", 28, TEAL), T("species", 28, BLUE))
        choices.arrange(RIGHT, buff=0.38).move_to([1.6, 2.72, 0])
        self.at("Their choices can change")
        self.play(FadeOut(arrows), FadeOut(labels),
                  LaggedStart(*[FadeIn(c, shift=DOWN * 0.12) for c in choices], lag_ratio=0.18), run_time=1.2)
        outline = RoundedRectangle(corner_radius=0.30, width=6.7, height=4.25, color=GREEN,
                                   stroke_width=6).move_to([-2.0, -0.25, 0])
        self.at("A habitat is where")
        self.play(FadeOut(choices), Create(outline), run_time=1.1)
        hab = T("habitat = needs met here", 38, GREEN, weight=BOLD).move_to([2.25, -2.58, 0])
        self.at("food water and shelter")
        self.play(FadeIn(hab, shift=UP * 0.12), run_time=1.1)
        self.finish()


class S04Release(SpokenScene):
    def construct(self):
        world = river_world(with_native=True, with_people=True)
        self.add(world)
        bucket = Arc(radius=0.46, start_angle=PI, angle=PI, color=TEXT, stroke_width=5).rotate(-0.55).move_to([-5.28, 2.48, 0])
        arrow = release_arrow()
        one = fish(BLUE, 0.76).move_to([-2.95, 0.92, 0])
        self.at("release blue catfish")
        self.play(FadeIn(bucket), Create(arrow), FadeIn(one, scale=0.6), run_time=1.2)
        outside = T("from outside these rivers", 28, TEXT).move_to([0.2, 2.70, 0])
        self.at("outside Virginia's Bay rivers")
        self.play(FadeIn(outside, shift=DOWN * 0.12), one.animate.move_to([0.1, 0.25, 0]), run_time=1.2)
        copies = VGroup(one, fish(BLUE, 0.66).move_to([2.0, -0.70, 0]), fish(BLUE, 0.66).move_to([3.1, 0.55, 0]))
        bar = compact_population_bar(BLUE, 0.62, "blue catfish", center=(5.55, 0.42, 0), frame_h=2.25)
        self.at("Here they spread")
        self.play(FadeIn(copies[1]), FadeIn(copies[2]), FadeIn(bar), run_time=0.9)
        self.play(bar.fill.animate.stretch_to_fit_height(2.25).align_to(bar.frame, DOWN), run_time=1.2)
        steps = VGroup(chip("brought here", BLUE, 28), chip("spreads", BLUE, 28), chip("causes harm", RED, 28))
        steps.arrange(RIGHT, buff=0.28).move_to([0.5, -3.28, 0])
        self.at("cause harm")
        self.play(FadeOut(outside), LaggedStart(*[FadeIn(s, shift=UP * 0.1) for s in steps], lag_ratio=0.22), run_time=1.3)
        invasive = T("INVASIVE", 44, BLUE, weight=BOLD).move_to([1.0, 2.75, 0])
        self.at("so they are invasive")
        self.play(FadeIn(invasive, scale=0.8), run_time=0.8)
        self.at("Being new is not enough")
        self.play(Indicate(VGroup(steps[1], steps[2]), color=RED, scale_factor=1.06), run_time=1.0)
        self.finish()


class S05Share(SpokenScene):
    def construct(self):
        world = prey_world()
        self.play(FadeIn(world), run_time=1.0)
        a_blue = arrow_between(world.blue.get_right(), world.pool.get_left(), BLUE)
        self.at("including fish and sometimes")
        self.play(Create(a_blue), Indicate(world.items, color=TEAL, scale_factor=1.08), run_time=1.1)
        a_gold = arrow_between(world.gold.get_left(), world.pool.get_right(), GOLD)
        self.at("white catfish eat similar prey")
        self.play(Create(a_gold), run_time=1.0)
        limited = T("same limited resource", 34, TEAL, weight=BOLD).move_to([0, 2.92, 0])
        self.at("same limited resource")
        self.play(FadeIn(limited, shift=DOWN * 0.10), Indicate(world.pool, color=TEAL, scale_factor=1.02), run_time=1.0)
        compete = T("may compete", 40, TEXT, weight=BOLD).move_to([0, -2.75, 0])
        self.at("they may compete")
        self.play(FadeIn(compete), run_time=0.7)
        nofight = chip("no fight needed", TEXT, 28).move_to([3.8, -2.75, 0])
        self.at("without a fight")
        self.play(FadeIn(nofight), run_time=0.7)
        self.at("eat food another fish needed")
        self.play(FadeOut(world.items[0], scale=0.5), FadeOut(world.items[1], scale=0.5),
                  FadeOut(world.items[2], scale=0.5), run_time=1.5)
        self.add(scope_tag("schematic"))
        self.finish()


class S06Predict(SpokenScene):
    def construct(self):
        world = prey_world(question=False, half_bar=False)
        self.add(world)
        self.at("Both catfish now use")
        a1 = arrow_between(world.blue.get_right(), world.pool.get_left(), BLUE)
        a2 = arrow_between(world.gold.get_left(), world.pool.get_right(), GOLD)
        self.play(Create(a1), Create(a2), run_time=1.0)
        self.at("blue population grows")
        self.play(world.bar.fill.animate.stretch_to_fit_height(1.55).align_to(world.bar.frame, DOWN), run_time=1.4)
        self.at("what do you predict")
        q = fit_text("If blue catfish grow, what remains for white catfish?", max_w=10.2,
                     size=34, color=TEXT, max_lines=2).move_to([0.35, 3.20, 0])
        self.play(FadeIn(q, shift=DOWN * 0.12), FadeOut(a1), FadeOut(a2), run_time=0.8)
        self.finish()


class S07Pause(PredictPause):
    QUESTION = "If blue catfish grow, what remains for white catfish?"
    SECONDS = 4.5
    CARD = {"y": 3.20, "size": 34, "color": TEXT, "max_w": 10.2}
    RING_AT = (6.0, 3.05, 0)

    def backdrop(self):
        return prey_world(question=False, half_bar=True)


class S08Reveal(SpokenScene):
    def construct(self):
        world = prey_world(question=False, half_bar=True)
        self.add(world)
        more = VGroup(fish(BLUE, 0.72).move_to([-3.7, 1.35, 0]), fish(BLUE, 0.66).move_to([-5.2, -2.05, 0]))
        self.at("More blue catfish feed")
        self.play(FadeIn(more), world.bar.fill.animate.stretch_to_fit_height(2.3).align_to(world.bar.frame, DOWN), run_time=1.2)
        arrows = VGroup(arrow_between(world.blue.get_right(), world.pool.get_left(), BLUE),
                        arrow_between(more[0].get_right(), world.pool.get_left() + UP * 0.55, BLUE))
        self.play(*[Create(a) for a in arrows], run_time=0.9)
        may = T("may", 38, TEAL, weight=BOLD).move_to([2.55, 2.55, 0])
        down = Arrow([1.7, 1.85, 0], [1.7, 0.85, 0], color=TEAL, stroke_width=6)
        self.at("prey pool may shrink")
        self.play(FadeOut(world.items[0]), FadeOut(world.items[1]), FadeOut(world.items[2]),
                  world.pool.animate.scale(0.82), FadeIn(may), GrowArrow(down), run_time=1.4)
        fewer = T("fewer prey", 32, GOLD).move_to([4.45, 1.52, 0])
        self.at("Less food may remain")
        self.play(FadeIn(fewer), Indicate(world.gold, color=GOLD, scale_factor=1.05), run_time=1.0)
        possible = T("possible pathway", 34, TEXT, weight=BOLD).move_to([0, -2.78, 0])
        bracket = Brace(VGroup(world.blue, world.pool, world.gold), DOWN, color=TEXT)
        bracket.set_stroke(opacity=0.75)
        self.at("possible competition pathway")
        self.play(GrowFromCenter(bracket), FadeIn(possible), run_time=1.0)
        self.at("not proof")
        self.play(possible.animate.set_color(GREY), run_time=0.7)
        other = VGroup(T("?", 52, RED), T("?", 52, RED)).arrange(DOWN, buff=0.42).move_to([6.1, 1.45, 0]).set_opacity(0.62)
        other_arrows = VGroup(
            DashedLine([5.65, 2.55, 0], [3.65, 2.72, 0], color=RED, stroke_width=3),
            DashedLine([5.65, -1.85, 0], [3.65, -2.12, 0], color=RED, stroke_width=3),
        )
        self.at("Other habitat changes")
        self.play(FadeIn(other), Create(other_arrows), run_time=1.1)
        self.finish()


class S09Shore(SpokenScene):
    def construct(self):
        world = river_world(with_blue=True, with_native=True)
        self.add(world)
        block = Rectangle(width=1.55, height=1.25, color=RED, stroke_width=4,
                          fill_color=RED, fill_opacity=0.35).move_to([-5.25, 2.38, 0])
        houses = VGroup(home(0.52).move_to([-5.65, 2.48, 0]), home(0.52).move_to([-4.75, 2.48, 0]))
        self.at("fill part of the green marsh")
        self.play(FadeIn(block, shift=RIGHT * 0.6), FadeIn(houses),
                  VGroup(*world.grasses[:5]).animate.set_opacity(0.12), run_time=1.4)
        self.at("Habitat disappears")
        self.play(world.prey.animate.shift(RIGHT * 1.6 + DOWN * 0.15), run_time=1.3)
        runoff = CurvedArrow([-2.9, 2.55, 0], [-1.1, 0.65, 0], angle=-0.3,
                             color=RED, stroke_width=12, tip_length=0.30)
        field = Rectangle(width=2.0, height=0.55, color=RED, fill_color=RED,
                          fill_opacity=0.18).move_to([-2.5, 2.70, 0])
        self.at("Runoff enters the water")
        self.play(FadeIn(field), Create(runoff), run_time=1.2)
        fert = T("extra fertilizer", 30, RED).move_to([0.25, 2.65, 0])
        self.at("extra fertilizer")
        self.play(FadeIn(fert), run_time=0.7)
        oxygen = ValueTracker(0.82)
        gauge = dial(oxygen, center=[4.65, 1.35, 0], radius=1.15, label="oxygen",
                     color=TEAL, fmt="{:.0f}%", scale=100, size=32)
        tag = T("schematic", 24, GREY).move_to([4.65, -0.15, 0])
        tag.layout_ok = True
        self.at("can later lower oxygen")
        self.play(FadeOut(world.blues), FadeIn(gauge), FadeIn(tag), run_time=0.8)
        self.play(oxygen.animate.set_value(0.56), run_time=1.6, rate_func=linear)
        self.at("affect several local populations")
        self.play(Indicate(VGroup(world.natives, world.prey), color=RED, scale_factor=1.03), run_time=1.0)
        self.finish()


class S10Ripples(SpokenScene):
    def construct(self):
        barset = response_bars(question=True)
        heading = barset.question
        self.play(FadeIn(heading), FadeIn(barset), run_time=1.2)
        for i, bar in enumerate(barset):
            pulse(bar[0], base=2.5, amp=0.75, speed=1.25 + 0.09 * i)
        signal = Circle(radius=0.24, color=TEXT, stroke_width=5).set_opacity(0.75).move_to([-5.1, 2.48, 0])
        signal._travel_t = 0.0

        def travel(mob, dt):
            mob._travel_t += dt
            mob.move_to([-5.1 + (1.25 * mob._travel_t) % 10.2,
                         2.48 + 0.08 * np.sin(2.0 * mob._travel_t), 0])

        signal.add_updater(travel)
        self.add(signal)
        self.at("whole river not one arrow")
        self.play(LaggedStart(*[Indicate(b[0], color=TEXT, scale_factor=1.02) for b in barset], lag_ratio=0.10), run_time=1.2)
        self.at("Blue catfish rise")
        self.play(barset[0][1].animate.stretch_to_fit_height(2.95).align_to(barset[0][0], DOWN), run_time=1.0)
        self.at("Shared prey and shoreline habitat change")
        self.play(barset[1][1].animate.stretch_to_fit_height(1.25).align_to(barset[1][0], DOWN), run_time=0.9)
        self.at("may respond differently")
        self.play(barset[2][1].animate.stretch_to_fit_height(0.95).align_to(barset[2][0], DOWN),
                  barset[3][1].animate.stretch_to_fit_height(1.55).align_to(barset[3][0], DOWN),
                  barset[4][1].animate.stretch_to_fit_height(1.05).align_to(barset[4][0], DOWN), run_time=1.3)
        ripples = VGroup(*[
            Arc(radius=r, start_angle=-0.35, angle=0.7, color=TEXT, stroke_width=4).move_to([0, -0.7, 0])
            for r in (1.2, 2.4, 3.6, 4.8)
        ])
        self.at("food web effects spread")
        self.play(LaggedStart(*[Create(r) for r in ripples], lag_ratio=0.18), run_time=1.5)
        basket = RoundedRectangle(corner_radius=0.15, width=1.4, height=0.75, color=GOLD,
                                  fill_color=GOLD, fill_opacity=0.18).move_to([5.65, 2.42, 0])
        hand = person(0.62).move_to([4.65, 2.48, 0])
        self.at("species people catch and eat")
        self.play(FadeIn(hand), FadeIn(basket), Indicate(barset[4], color=GOLD, scale_factor=1.04), run_time=1.1)
        self.finish()


class S11Help(SpokenScene):
    def construct(self):
        world = river_world(with_blue=True, with_native=True)
        self.add(world)
        new_grass = VGroup(*[
            Line([x, 1.78, 0], [x + 0.08 * (-1) ** i, 2.65, 0], color=GREEN, stroke_width=6)
            for i, x in enumerate(np.linspace(-3.55, -2.4, 6))
        ])
        self.at("restore habitat")
        self.play(LaggedStart(*[GrowFromEdge(g, DOWN) for g in new_grass], lag_ratio=0.12), run_time=1.3)
        boat = Arc(radius=0.75, start_angle=PI, angle=PI, color=TEXT, stroke_width=6).move_to([2.6, 1.48, 0])
        lifted = world.blues[1].copy()
        self.at("remove some invasive fish")
        self.play(FadeIn(boat), lifted.animate.move_to([2.6, 1.60, 0]), FadeOut(world.blues[1]), run_time=1.4)
        mini_frames = VGroup(*[
            RoundedRectangle(corner_radius=0.08, width=0.62, height=1.75, color=GREY, stroke_width=2)
            for _ in range(3)
        ]).arrange(RIGHT, buff=0.20).move_to([4.85, 0.25, 0])
        mini_fills = VGroup(*[
            Rectangle(width=0.44, height=h, color=c, stroke_width=0, fill_color=c, fill_opacity=0.72)
            for h, c in ((1.30, BLUE), (0.82, TEAL), (1.02, GOLD))
        ])
        for fill, frame in zip(mini_fills, mini_frames):
            fill.move_to([frame.get_x(), frame.get_bottom()[1] + fill.height / 2 + 0.08, 0])
        mini_label = T("population responses", 28, TEXT).next_to(mini_frames, UP, buff=0.14)
        mini = VGroup(mini_frames, mini_fills, mini_label)
        self.at("How far each population recovers")
        self.play(FadeOut(boat), FadeOut(lifted), FadeIn(mini), run_time=0.8)
        question = T("?", 130, TEXT, weight=BOLD).move_to(mini)
        question.layout_ok = True  # deliberate uncertainty stamp covering unsettled bars
        self.at("a question to test")
        self.play(FadeIn(question, scale=0.7), mini.animate.set_opacity(0.25), run_time=0.9)
        loop = CurvedArrow([-0.4, -2.0, 0], [2.0, -2.0, 0], angle=PI * 1.1,
                           color=TEXT, stroke_width=5, tip_length=0.25)
        label = T("test one change", 32, TEXT).move_to([4.15, -3.32, 0])
        self.at("change one thing at a time")
        self.play(Create(loop), FadeIn(label), run_time=1.2)
        self.finish()


class S12Rule(SpokenScene):
    def construct(self):
        world = river_world(with_blue=True, with_native=True, with_people=True)
        self.play(FadeIn(world), run_time=0.9)
        rule = fit_text("When people change an ecosystem, populations may rise or fall.",
                        max_w=10.2, size=38, color=TEXT, max_lines=2).move_to([1.55, 3.20, 0])
        self.at("rule to carry forward")
        self.play(FadeIn(rule, shift=DOWN * 0.12), run_time=0.9)
        bars = VGroup(
            compact_population_bar(BLUE, 1.65, "blue", center=(3.3, -0.55, 0), show_tag=False),
            compact_population_bar(GOLD, 0.78, "white", center=(4.85, -0.55, 0), show_tag=False),
            compact_population_bar(TEAL, 1.12, "prey", center=(6.4, -0.55, 0), show_tag=False),
        )
        self.at("populations may rise or fall")
        self.play(FadeOut(world.natives), FadeOut(world.blues),
                  LaggedStart(*[FadeIn(b, shift=UP * 0.10) for b in bars], lag_ratio=0.14),
                  FadeIn(shared_tag(list(bars))), run_time=1.2)
        lens = Circle(radius=0.72, color=TEXT, stroke_width=7).move_to([-1.1, -1.15, 0])
        handle = Line([-0.58, -1.66, 0], [0.15, -2.38, 0], color=TEXT, stroke_width=9)
        evidence = T("real river evidence", 34, TEXT, weight=BOLD).move_to([-2.1, -2.65, 0])
        self.at("evidence must show")
        self.play(Create(lens), Create(handle), FadeIn(evidence), run_time=1.1)
        legend = VGroup(T("blue catfish", 24, BLUE), T("white catfish", 24, GOLD), T("shared prey", 24, TEAL))
        legend.arrange(DOWN, aligned_edge=LEFT, buff=0.10).move_to([-4.9, 0.30, 0])
        self.play(FadeOut(world.currents), FadeOut(world.roots), run_time=0.25)
        self.at("real river")
        self.play(FadeIn(legend), Indicate(evidence, color=TEXT, scale_factor=1.04), run_time=0.9)
        self.finish()


class S13End(EndCard):
    LINE = "When people change an ecosystem, populations may rise or fall."
