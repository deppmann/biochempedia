"""Where Differences Begin — mutations and variation.

COLOR MAP (kept for the whole film)
  BLUE   inherited information / DNA / alleles
  GREEN  environment and leaves
  GOLD   mutation
  PURPLE changed trait
  RED    blocked route
  TEXT   neutral routes and labels

The oak, input streams, height comparison, and predict frame each have one builder so
their scale and landmarks stay fixed when a scene continues the same picture.
"""
from bp_parts import *  # noqa: F401,F403


LEAF = "#79B85A"
PURPLE = "#B07CFF"
SUN = "#FFD166"


def diagram_plate():
    """Neutral field shared by the film's diagram scenes; not an information-bearing shape."""
    plate = RoundedRectangle(corner_radius=0.28, width=12.45, height=5.55,
                             stroke_width=0, fill_color=GREY, fill_opacity=0.15)
    plate.set_z_index(-5)
    plate.layout_ok = True
    return plate


def labelled_box(text, color, width=2.0, height=0.72, size=28, fill=0.18):
    box = RoundedRectangle(corner_radius=0.16, width=width, height=height,
                           stroke_color=color, stroke_width=3,
                           fill_color=color, fill_opacity=fill)
    lab = fit_text(text, max_w=width - 0.25, size=size, color=color, max_lines=2).move_to(box)
    lab.layout_ok = True  # deliberate label on its own shape
    return VGroup(box, lab)


def oak_leaf(length=2.0, width=1.0, color=LEAF):
    """One schematic rounded-lobed oak leaf; no biological detail beyond the script."""
    blade = Ellipse(width=width * 0.72, height=length, stroke_color=color,
                    stroke_width=2, fill_color=color, fill_opacity=0.82)
    lobes = VGroup()
    for frac, radius in ((0.28, 0.24), (0.50, 0.29), (0.72, 0.23)):
        for side in (-1, 1):
            lobes.add(Circle(radius=width * radius, stroke_width=0, fill_color=color,
                             fill_opacity=0.82).move_to([side * width * 0.34,
                                                         (frac - 0.5) * length, 0]))
    vein = Line([0, -length * 0.46, 0], [0, length * 0.43, 0], color=BG, stroke_width=2)
    stem = Line([0, -length * 0.50, 0], [0, -length * 0.68, 0], color=LEAF, stroke_width=5)
    return VGroup(stem, blade, lobes, vein)


LEAF_LENGTHS = [1.55, 1.95, 1.70, 2.20, 1.82, 2.35, 1.62, 2.05, 1.76, 2.25]


def oak_world(with_ruler=False, with_branch=True):
    """The carried oak row used in s00, s01, s02, and s12."""
    xs = np.linspace(-5.45, 5.45, 10)
    base = -1.75
    scaled_lengths = [1.45 * L for L in LEAF_LENGTHS]
    leaves = VGroup(*[oak_leaf(L, 0.78).move_to([x, base + L / 2, 0])
                      for x, L in zip(xs, scaled_lengths)])
    branch = CubicBezier([-6.2, -1.70, 0], [-2.4, -1.32, 0],
                         [2.5, -1.95, 0], [6.2, -1.58, 0],
                         color="#8B6A48", stroke_width=18)
    group = VGroup(branch, leaves) if with_branch else VGroup(leaves)
    group.branch, group.leaves = branch, leaves
    if with_ruler:
        body = Rectangle(width=11.7, height=0.42, stroke_color=TEXT, stroke_width=3,
                         fill_color=TEXT, fill_opacity=0.10).move_to([0, -2.82, 0])
        ticks = VGroup(*[Line([x, -2.61, 0], [x, -2.84 if i % 2 else -2.96, 0],
                                  color=TEXT, stroke_width=2)
                         for i, x in enumerate(np.linspace(-5.65, 5.65, 21))])
        ruler = VGroup(body, ticks)
        group.add(ruler)
        group.ruler = ruler
    return group


def tree_crown(x, y, scale=1.0):
    trunk = Line([x, y - 0.72 * scale, 0], [x, y + 0.15 * scale, 0],
                 color="#8B6A48", stroke_width=8 * scale)
    crown = VGroup(*[Circle(radius=0.52 * scale, stroke_color=LEAF, stroke_width=2,
                            fill_color=LEAF, fill_opacity=0.45).move_to([x + dx * scale, y + dy * scale, 0])
                     for dx, dy in ((-0.38, 0), (0.38, 0), (0, 0.35))])
    return VGroup(trunk, crown)


def person_outline(x, base=-2.05, scale=1.0, color=TEXT):
    head = Circle(radius=0.35 * scale, color=color, stroke_width=4).move_to([x, base + 2.45 * scale, 0])
    body = Line([x, base + 2.10 * scale, 0], [x, base + 0.80 * scale, 0], color=color, stroke_width=6)
    arms = Line([x - 0.58 * scale, base + 1.65 * scale, 0],
                [x + 0.58 * scale, base + 1.65 * scale, 0], color=color, stroke_width=5)
    legs = VGroup(Line([x, base + 0.80 * scale, 0], [x - 0.46 * scale, base, 0], color=color, stroke_width=5),
                  Line([x, base + 0.80 * scale, 0], [x + 0.46 * scale, base, 0], color=color, stroke_width=5))
    return VGroup(head, body, arms, legs)


def flow_arrow(start, end, color, width=10):
    return Arrow(start, end, buff=0.05, color=color, stroke_width=width, tip_length=0.25)


def pulse_each(group, base, amp, speed):
    """Keep separately-added stream pieces moving; group updaters do not follow GrowArrow."""
    for i, item in enumerate(group):
        pulse(item, base=base, amp=amp, speed=speed + 0.11 * i)
    return group


def sweep_to(scene, phrase, routes, color=TEXT, width=34):
    """Fill a cue wait with a visible pulse travelling along the narrated route."""
    rest = scene.t_of(phrase) - 0.2 - scene.elapsed()
    if rest > 0.25:
        flashes = [ShowPassingFlash(route.copy().set_stroke(color=color, width=width),
                                    time_width=0.38)
                   for route in routes]
        scene.play(*flashes, run_time=rest, rate_func=linear)
    scene.at(phrase)


def input_world():
    """Two broad streams converging on one child and one leaf (s03)."""
    inherited = flow_arrow([-5.8, 1.45, 0], [-0.85, 0.40, 0], BLUE)
    environment = flow_arrow([-5.8, -1.45, 0], [-0.85, -0.15, 0], GREEN)
    child = person_outline(1.25, base=-2.15, scale=1.05)
    leaf = oak_leaf(2.35, 1.18).move_to([4.25, 0.15, 0])
    return VGroup(inherited, environment, child, leaf)


def height_world(hidden=False, final=False):
    """Exact carried frame for s04 and s08–s10."""
    xs = (-2.6, 2.6)
    people = VGroup(*[person_outline(x, base=-2.15, scale=0.82) for x in xs])
    blue = VGroup(*[flow_arrow([x - 2.25, 2.25, 0], [x - 0.35, 1.15, 0], BLUE, 8) for x in xs])
    green = VGroup(flow_arrow([-5.05, -0.15, 0], [-3.05, 0.25, 0], GREEN, 8),
                   flow_arrow([5.05, -0.75, 0], [3.05, -0.10, 0], GREEN, 8))
    ground = Line([-5.7, -2.15, 0], [5.7, -2.15, 0], color=GREY, stroke_width=3)
    bars = VGroup()
    heights = (3.55, 2.85) if final else (3.20, 3.20)
    for x, h in zip(xs, heights):
        bars.add(RoundedRectangle(corner_radius=0.10, width=0.52, height=h,
                                  stroke_color=PURPLE, stroke_width=3,
                                  fill_color=PURPLE, fill_opacity=0.45)
                 .move_to([x + 1.25, -2.15 + h / 2, 0]))
    group = VGroup(ground, people, blue, green, bars)
    group.people, group.blue, group.green, group.bars = people, blue, green, bars
    if hidden:
        marks = VGroup(*[T("?", 64, GOLD, weight=BOLD).move_to(b) for b in bars])
        for mark in marks:
            mark.layout_ok = True  # deliberate: each question mark hides its own bar
        group.add(marks)
        group.marks = marks
    return group


def allele_card(letter, at, accent=False):
    card = RoundedRectangle(corner_radius=0.14, width=1.20, height=1.55,
                            stroke_color=BLUE, stroke_width=3,
                            fill_color=BLUE, fill_opacity=0.22).move_to(at)
    label = T(letter, 34, BLUE, weight=BOLD).move_to(card)
    label.layout_ok = True
    g = VGroup(card, label)
    if accent:
        corner = Polygon(card.get_corner(UR), card.get_corner(UR) + LEFT * 0.38,
                         card.get_corner(UR) + DOWN * 0.38,
                         fill_color=GOLD, fill_opacity=1, stroke_width=0)
        g.add(corner)
    return g


def dna_row():
    letters = "ACGTACGA"
    blocks = VGroup()
    for letter in letters:
        box = Square(side_length=0.78, stroke_color=BLUE, stroke_width=3,
                     fill_color=BLUE, fill_opacity=0.22)
        lab = M(letter, 32, BLUE).move_to(box)
        lab.layout_ok = True
        blocks.add(VGroup(box, lab))
    blocks.arrange(RIGHT, buff=0.12).move_to([-0.8, 1.0, 0])
    return blocks


def predict_backdrop(final=False):
    world = height_world(hidden=not final, final=final)
    q = question_card("Must their heights match?", y=3.25, size=34, max_w=11.0)
    return VGroup(world, q)


class S00Hook(SpokenScene):
    def construct(self):
        world = oak_world(with_ruler=False)
        bob(world.leaves, amp=0.07, speed=1.4)
        self.play(Create(world.branch), FadeIn(world.leaves, lag_ratio=0.10, shift=UP * 0.18), run_time=2.6)
        self.at("why do they share")
        self.play(LaggedStart(*[Indicate(l, color=GREEN, scale_factor=1.05) for l in world.leaves],
                              lag_ratio=0.06), run_time=2.1)
        self.at("story begins with variation")
        variation = T("Variation", 54, PURPLE, weight=BOLD).move_to([0, 3.05, 0])
        tips = VGroup(*[Dot(l.get_top(), radius=0.06, color=PURPLE) for l in world.leaves])
        self.play(FadeIn(tips, lag_ratio=0.06), GrowFromCenter(variation), run_time=1.4)
        self.at("look closely")
        ruler_world = oak_world(with_ruler=True)
        ruler = ruler_world.ruler
        self.play(FadeIn(ruler, shift=RIGHT * 0.5), run_time=1.5)
        self.play(LaggedStart(*[l.animate.shift(DOWN * 0.08) for l in world.leaves], lag_ratio=0.06), run_time=1.4)
        self.finish()


class S01Title(TitleCard):
    LESSON = "Mutations and Variation"
    TITLE = "Where Differences Begin"

    def construct(self):
        world = oak_world()
        world.set_opacity(0.35)
        world.shift(DOWN * 1.45)
        bob(world.leaves, amp=0.05, speed=1.5)
        title = T(self.TITLE, 54, TEXT, font=TITLE_FONT)
        lesson = T(self.LESSON.upper(), 24, GREEN)
        rule = Line(LEFT * 1.4, RIGHT * 1.4, color=GOLD, stroke_width=4)
        card = VGroup(lesson, title, rule).arrange(DOWN, buff=0.30).move_to([0, 1.35, 0])
        self.add(world)
        self.play(FadeIn(card), run_time=0.75)
        self.wait(0.65)
        self.play(FadeOut(card), run_time=0.55)
        self.finish()


class S02Words(SpokenScene):
    def construct(self):
        world = oak_world()
        bob(world.leaves, amp=0.05, speed=1.5)
        self.add(world)
        outline = world.leaves[4].copy().set_fill(opacity=0).set_stroke(PURPLE, width=6)
        trait = labelled_box("trait", PURPLE, width=1.65).move_to([4.95, 2.75, 0])
        self.play(ShowPassingFlash(outline, time_width=0.8), FadeIn(trait), run_time=1.2)
        self.at("a population")
        crowns = VGroup(*[tree_crown(x, y, 0.78) for x, y in
                          ((-4.7, 0.6), (-2.8, 0.0), (-0.9, 0.65), (1.0, 0.05), (2.9, 0.65), (4.7, 0.0))])
        boundary = RoundedRectangle(corner_radius=0.30, width=11.7, height=4.9,
                                    stroke_color=TEXT, stroke_width=3).move_to([0, 0.15, 0])
        population = T("population", 34, TEXT, weight=BOLD).move_to([0, 2.85, 0])
        self.play(FadeOut(world), FadeOut(trait), Create(boundary),
                  FadeIn(crowns, lag_ratio=0.10), FadeIn(population), run_time=2.4)
        self.at("variation means")
        leaves = VGroup(*[oak_leaf(L, 0.72).move_to([x, -1.15 + L / 2, 0])
                          for x, L in zip(np.linspace(-4.4, 4.4, 7), LEAF_LENGTHS[:7])])
        variation = T("variation = differences", 42, PURPLE, weight=BOLD).move_to([0, -2.75, 0])
        self.play(FadeOut(crowns), FadeIn(leaves, lag_ratio=0.10), FadeIn(variation), run_time=2.0)
        self.at("shared traits")
        self.play(LaggedStart(*[l.animate.shift(RIGHT * (0.08 if i % 2 else -0.08))
                                for i, l in enumerate(leaves)], lag_ratio=0.08), run_time=1.7)
        self.finish()


class S03Inputs(SpokenScene):
    def construct(self):
        self.add(diagram_plate())
        world = input_world()
        blue, green, child, leaf = world
        pulse(blue, base=10, amp=3.2, speed=2.0)
        pulse(green, base=10, amp=3.2, speed=2.3)
        parents = VGroup(person_outline(-5.35, base=0.10, scale=0.55),
                         person_outline(-4.45, base=0.10, scale=0.55))
        self.play(FadeIn(parents), GrowArrow(blue), run_time=2.2)
        inherited = T("inherited information", 30, BLUE, weight=BOLD).move_to([-3.3, 2.72, 0])
        self.at("blue inherited information")
        self.play(FadeIn(inherited), run_time=1.0)
        sweep_to(self, "green environmental conditions", [blue], color=BLUE)
        icons = VGroup(labelled_box("food", GREEN, 1.35, 0.62, 26),
                       labelled_box("health", GREEN, 1.50, 0.62, 26),
                       labelled_box("sunlight", GREEN, 1.85, 0.62, 26),
                       labelled_box("water", GREEN, 1.45, 0.62, 26)).arrange(RIGHT, buff=0.22).move_to([0, -2.82, 0])
        self.play(GrowArrow(green), FadeIn(icons, lag_ratio=0.12), run_time=2.2)
        sweep_to(self, "roots often act together", [blue, green], color=PURPLE)
        self.play(FadeIn(child, shift=UP * 0.2), FadeIn(leaf, shift=UP * 0.2),
                  FadeOut(parents), run_time=1.8)
        both = T("both routes", 38, PURPLE, weight=BOLD).move_to([3.55, 2.75, 0])
        self.at("both matter")
        self.play(FadeIn(both), Indicate(VGroup(child, leaf), color=PURPLE), run_time=1.3)
        self.add(scope_tag("schematic"))
        self.finish()


class S04Height(SpokenScene):
    def construct(self):
        self.add(diagram_plate())
        world = height_world()
        ground, people, blue, green, bars = world
        pulse_each(blue, base=8, amp=2.8, speed=2.0)
        pulse_each(green, base=8, amp=2.8, speed=2.3)
        self.play(Create(ground), FadeIn(people), GrowFromEdge(bars, DOWN), run_time=1.8)
        self.at("many genes")
        blocks = VGroup(*[allele_card(x, [-0.75 + i * 0.5, 2.65, 0]).scale(0.42)
                          for i, x in enumerate("ABCDE")])
        self.play(GrowArrow(blue[0]), GrowArrow(blue[1]), FadeIn(blocks, lag_ratio=0.1), run_time=1.8)
        sweep_to(self, "food and health", list(blue), color=BLUE)
        food = VGroup(labelled_box("food", GREEN, 1.35, 0.62, 26),
                      labelled_box("health", GREEN, 1.50, 0.62, 26)).arrange(RIGHT, buff=0.25).move_to([0, -2.82, 0])
        self.play(GrowArrow(green[0]), GrowArrow(green[1]), FadeIn(food), run_time=1.6)
        sweep_to(self, "similar inherited information", list(blue) + list(green), color=PURPLE)
        self.play(Indicate(blue, color=BLUE, scale_factor=1.03), run_time=1.3)
        sweep_to(self, "exactly the same height", list(blue), color=BLUE)
        target = height_world(final=True).bars
        self.play(Transform(bars, target), run_time=2.0)
        sweep_to(self, "height bar is not", list(blue) + list(green), color=PURPLE)
        note = caption("Schematic bars are not predictions for one person.", size=28, color=PURPLE)
        self.play(FadeOut(food), FadeIn(note), run_time=1.2)
        self.add(scope_tag("schematic"))
        self.finish()


class S05Shuffle(SpokenScene):
    def construct(self):
        self.add(diagram_plate())
        parent_a = VGroup(*[allele_card(x, [-5.55 + i * 1.28, 2.0, 0]) for i, x in enumerate("ABC")])
        parent_b = VGroup(*[allele_card(x, [-5.55 + i * 1.28, -1.65, 0]) for i, x in enumerate("DEF")])
        tray = labelled_box("shuffle", TEXT, 2.1, 1.05, 30).move_to([0, 0.15, 0])
        self.play(FadeIn(parent_a, lag_ratio=0.12), FadeIn(parent_b, lag_ratio=0.12), run_time=2.0)
        self.at("picture blue cards")
        self.play(FadeIn(tray), parent_a.animate.arrange(DOWN, buff=-0.45).move_to(tray),
                  parent_b.animate.arrange(DOWN, buff=-0.45).move_to(tray), run_time=2.0)
        self.at("combinations are new")
        hand1 = VGroup(*[allele_card(x, [3.35 + i * 1.12, 1.45, 0]).scale(0.82) for i, x in enumerate("ADF")])
        hand2 = VGroup(*[allele_card(x, [3.35 + i * 1.12, -1.15, 0]).scale(0.82) for i, x in enumerate("BCE")])
        self.play(FadeOut(parent_a), FadeOut(parent_b), FadeIn(hand1, lag_ratio=0.12),
                  FadeIn(hand2, lag_ratio=0.12), run_time=2.3)
        bracket = Brace(VGroup(hand1, hand2), RIGHT, color=BLUE)
        label = fit_text("new mix of existing alleles", max_w=4.0, size=30,
                         color=BLUE, max_lines=2).move_to([2.9, -3.05, 0])
        self.at("cards already existed")
        self.play(GrowFromCenter(bracket), FadeIn(label), Indicate(VGroup(hand1, hand2), color=BLUE), run_time=1.7)
        self.at("siblings can receive")
        self.play(hand1.animate.shift(UP * 0.18), hand2.animate.shift(DOWN * 0.18), run_time=1.4)
        self.finish()


class S06Mutation(SpokenScene):
    def construct(self):
        self.add(diagram_plate())
        blocks = dna_row()
        pulse(blocks, base=3, amp=1.4, speed=2.2)
        title = T("DNA sequence", 40, BLUE, weight=BOLD).move_to([-0.8, 2.2, 0])
        self.play(FadeIn(title), FadeIn(blocks, lag_ratio=0.10), run_time=2.1)
        self.at("mutation changes")
        changed = blocks[5].copy()
        changed[0].set_stroke(GOLD, width=5).set_fill(GOLD, opacity=0.55)
        changed[1].set_color(GOLD)
        self.play(Rotate(blocks[5], angle=PI, axis=UP), Transform(blocks[5], changed), run_time=1.5)
        self.at("order of its bases")
        order = Arrow(blocks.get_left() + DOWN * 0.75, blocks.get_right() + DOWN * 0.75,
                      color=TEXT, stroke_width=5, tip_length=0.22)
        self.play(GrowArrow(order), run_time=1.1)
        self.at("new allele")
        old = allele_card("A", [-3.2, -1.3, 0])
        new = allele_card("A′", [0.0, -1.3, 0], accent=True)
        self.play(FadeIn(old), FadeIn(new, shift=RIGHT * 0.3), run_time=1.7)
        outcomes = VGroup(labelled_box("protein", PURPLE, 1.75, 0.72, 27),
                          labelled_box("amount", PURPLE, 1.75, 0.72, 27),
                          labelled_box("neither", TEXT, 1.75, 0.72, 27)).arrange(RIGHT, buff=0.28).move_to([2.8, -2.75, 0])
        self.at("it may change")
        self.play(FadeIn(outcomes, lag_ratio=0.14), run_time=1.8)
        self.finish()


class S07Causes(SpokenScene):
    def construct(self):
        self.add(diagram_plate())
        block = dna_row()[5].move_to([0, 0.6, 0])
        block[0].set_stroke(GOLD, width=5).set_fill(GOLD, opacity=0.55)
        block[1].set_color(GOLD)
        causes = VGroup(labelled_box("copy slip", TEXT, 2.0),
                        labelled_box("radiation", SUN, 2.0),
                        labelled_box("some chemicals", TEXT, 2.55)).arrange(RIGHT, buff=0.65).move_to([0, 2.65, 0])
        arrows = VGroup(*[flow_arrow(c.get_bottom(), block.get_top(), GOLD, 5) for c in causes])
        pulse(block, base=5, amp=1.8, speed=2.1)
        pulse_each(arrows, base=5, amp=1.8, speed=2.2)
        self.play(FadeIn(block, scale=0.7), FadeIn(causes, lag_ratio=0.13),
                  LaggedStart(*[GrowArrow(a) for a in arrows], lag_ratio=0.12), run_time=2.6)
        sweep_to(self, "change does not appear", list(arrows), color=GOLD)
        need = labelled_box("NEED", TEXT, 1.75, 0.85, 32).move_to([-4.6, -1.55, 0])
        route = DashedLine(need.get_right(), block.get_left(), color=RED, stroke_width=5)
        barrier = Line([-1.25, -0.25, 0], [-1.25, -1.45, 0], color=RED, stroke_width=10)
        self.play(FadeIn(need), Create(route), GrowFromCenter(barrier), run_time=2.0)
        sweep_to(self, "need sends no instructions", [route], color=RED)
        stopped = T("blocked", 32, RED, weight=BOLD).move_to([-1.25, -1.85, 0])
        self.play(FadeIn(stopped), Indicate(barrier, color=RED), run_time=1.5)
        sweep_to(self, "more exposure", list(arrows), color=GOLD)
        chance = ValueTracker(0.2)
        gauge = dial(chance, center=[3.8, -0.75, 0], radius=1.35, label="chance",
                     color=GOLD, fmt="{:.0f}%", scale=100)
        self.play(FadeIn(gauge), run_time=0.8)
        self.play(chance.animate.set_value(0.72), run_time=2.0, rate_func=linear)
        result = T("result not chosen", 28, TEXT).move_to([3.8, -2.65, 0])
        self.play(FadeIn(result), run_time=0.8)
        self.finish()


class S08Predict(SpokenScene):
    def construct(self):
        self.add(diagram_plate())
        world = height_world(hidden=True)
        ground, people, blue, green, bars, marks = world
        pulse_each(blue, base=8, amp=2.8, speed=2.0)
        pulse_each(green, base=8, amp=2.8, speed=2.3)
        self.play(Create(ground), FadeIn(people), FadeIn(bars), FadeIn(marks), run_time=1.6)
        self.at("two children")
        self.play(GrowArrow(blue[0]), GrowArrow(blue[1]), run_time=1.5)
        sweep_to(self, "but their food", list(blue), color=BLUE)
        self.play(GrowArrow(green[0]), GrowArrow(green[1]), run_time=1.5)
        sweep_to(self, "must they reach", list(blue) + list(green), color=PURPLE)
        q = question_card("Must their heights match?", y=3.25, size=34, max_w=11.0)
        self.play(FadeIn(q.question), run_time=1.2)
        self.at("hold your answer")
        self.play(Indicate(marks, color=GOLD, scale_factor=1.12), run_time=1.3)
        self.at("watch both colored roots")
        self.play(Indicate(blue, color=BLUE), Indicate(green, color=GREEN), run_time=1.8)
        self.finish()


class S09Pause(PredictPause):
    QUESTION = "Must their heights match?"
    SECONDS = 4.5
    CARD = {"y": 3.25, "size": 34, "max_w": 11.0}

    def backdrop(self):
        world = height_world(hidden=True)
        world.add_to_back(diagram_plate())
        pulse_each(world.blue, base=8, amp=2.8, speed=2.0)
        pulse_each(world.green, base=8, amp=2.8, speed=2.3)
        pulse(world.marks, base=4.0, amp=1.2, speed=1.5)
        return world

    def construct(self):
        world = self.backdrop()
        self.add(world)
        self.add(question_card(self.QUESTION, self.OPTIONS, chips_at=self.CHIPS_AT, **self.CARD))
        ring, run = countdown(self.SECONDS, center=self.RING_AT)
        self.add(ring)
        flashes = [ShowPassingFlash(route.copy().set_stroke(color=route.get_color(), width=34),
                                    time_width=0.38)
                   for route in list(world.blue) + list(world.green)]
        self.play(run, *flashes, run_time=self.SECONDS, rate_func=linear)
        self.finish()


class S10Reveal(SpokenScene):
    def construct(self):
        self.add(diagram_plate())
        hidden = height_world(hidden=True)
        pulse_each(hidden.blue, base=8, amp=2.8, speed=2.0)
        pulse_each(hidden.green, base=8, amp=2.8, speed=2.3)
        q = question_card("Must their heights match?", y=3.25, size=34, max_w=11.0)
        self.add(hidden, q)
        answer = T("No", 58, PURPLE, weight=BOLD).move_to([0, 3.28, 0])
        self.play(FadeOut(hidden.marks, shift=UP * 0.3), swap(q.question, answer), run_time=1.4)
        sweep_to(self, "genes and environment", list(hidden.blue) + list(hidden.green), color=PURPLE)
        self.play(Indicate(hidden.blue, color=BLUE), Indicate(hidden.green, color=GREEN), run_time=1.5)
        sweep_to(self, "different conditions", list(hidden.blue) + list(hidden.green), color=PURPLE)
        final = height_world(final=True).bars
        self.play(Transform(hidden.bars, final), run_time=2.2)
        sweep_to(self, "does not prove", list(hidden.blue) + list(hidden.green), color=PURPLE)
        boundary = RoundedRectangle(corner_radius=0.22, width=11.9, height=4.95,
                                    stroke_color=PURPLE, stroke_width=3).move_to([0, 0.12, 0])
        self.play(Create(boundary), run_time=1.3)
        sweep_to(self, "picture shows a possibility", [boundary], color=PURPLE, width=16)
        note = caption("possible outcome, not a diagnosis", size=30, color=PURPLE)
        self.play(FadeIn(note), run_time=1.2)
        self.add(scope_tag("schematic"))
        self.finish()


class S11Routes(SpokenScene):
    def construct(self):
        self.add(diagram_plate())
        parent = RoundedRectangle(corner_radius=0.35, width=6.4, height=5.7,
                                  stroke_color=TEXT, stroke_width=4,
                                  fill_color=TEXT, fill_opacity=0.05).move_to([-2.8, 0.20, 0])
        pulse(parent, base=4, amp=1.8, speed=1.9)
        parent_body = person_outline(-1.3, base=-1.75, scale=1.35).set_opacity(0.32)
        pulse(parent_body, base=5, amp=1.5, speed=2.0)
        offspring = person_outline(4.55, base=-1.95, scale=1.0)
        parent_label = T("parent", 30, TEXT).move_to([-2.8, 2.45, 0])
        self.play(Create(parent), FadeIn(parent_body), FadeIn(parent_label), FadeIn(offspring), run_time=1.9)
        sweep_to(self, "mutation in a body cell", [parent], color=TEXT, width=16)
        skin = labelled_box("skin cell", TEXT, 2.05, 0.82, 28).move_to([-4.15, 0.95, 0])
        gold1 = Dot(skin[0].get_right() + RIGHT * 0.22, radius=0.13, color=GOLD)
        blocked = Arrow(skin.get_right(), [-0.25, 0.95, 0], color=RED, stroke_width=6, tip_length=0.24)
        stop = Line([-0.15, 0.35, 0], [-0.15, 1.55, 0], color=RED, stroke_width=10)
        self.play(FadeIn(skin), FadeIn(gold1), GrowArrow(blocked), GrowFromCenter(stop), run_time=2.0)
        sweep_to(self, "mutation in an egg", [blocked], color=RED)
        sex = labelled_box("egg or sperm", TEXT, 2.55, 0.82, 28).move_to([-4.15, -1.25, 0])
        gold2 = Dot(sex[0].get_right() + RIGHT * 0.22, radius=0.13, color=GOLD)
        self.play(FadeIn(sex), FadeIn(gold2), run_time=1.2)
        self.at("can reach offspring")
        path = Arrow(sex.get_right(), offspring.get_left(), color=TEXT,
                     stroke_width=6, buff=0.12, tip_length=0.25)
        moving = gold2.copy()
        self.add(moving)
        self.play(GrowArrow(path), MoveAlongPath(moving, path), run_time=2.3)
        can_reach = T("can reach", 34, TEXT, weight=BOLD).move_to([2.0, -2.20, 0])
        self.play(FadeIn(can_reach), run_time=0.9)
        sweep_to(self, "path not usefulness", [blocked, path], color=GOLD)
        summary = caption("The path decides whether inheritance is possible.", size=30, color=GOLD)
        self.play(FadeIn(summary), Indicate(VGroup(blocked, path), color=GOLD), run_time=1.8)
        self.finish()


class S12Idea(SpokenScene):
    def construct(self):
        world = oak_world()
        world.scale(0.90).shift(UP * 0.85)
        bob(world.leaves, amp=0.06, speed=1.4)
        self.play(Create(world.branch), FadeIn(world.leaves, lag_ratio=0.08), run_time=2.0)
        self.at("shared traits can vary")
        self.play(LaggedStart(*[Indicate(l, color=PURPLE, scale_factor=1.04) for l in world.leaves],
                              lag_ratio=0.05), run_time=1.5)
        self.at("inherited information")
        blue = flow_arrow([-5.6, -2.15, 0], [-0.45, -1.35, 0], BLUE, 10)
        green = flow_arrow([5.6, -2.15, 0], [0.45, -1.35, 0], GREEN, 10)
        pulse(blue, base=10, amp=3.2, speed=2.0)
        pulse(green, base=10, amp=3.2, speed=2.3)
        self.play(GrowArrow(blue), GrowArrow(green), run_time=2.1)
        self.at("chance mutation")
        allele = allele_card("A′", [0, -1.30, 0], accent=True).scale(0.78)
        self.play(FadeIn(allele, scale=0.7), run_time=1.3)
        self.at("new genetic difference")
        title = T("sources of variation", 42, PURPLE, weight=BOLD).move_to([0, -3.0, 0])
        self.play(FadeIn(title), Indicate(allele, color=GOLD), run_time=1.5)
        self.at("does not make every")
        note = fit_text("not every visible difference is inherited", max_w=6.4,
                        size=28, color=TEXT).move_to([0, 3.25, 0])
        self.play(FadeIn(note), run_time=1.2)
        self.finish()


class S13Handoff(SpokenScene):
    def construct(self):
        leaf = oak_leaf(4.6, 2.4).move_to([-2.3, 0, 0])
        allele = allele_card("A′", [2.7, 0.75, 0], accent=True)
        self.play(FadeIn(leaf, shift=UP * 0.2), FadeIn(allele), run_time=1.5)
        self.at("no fixed label")
        unknown = T("?", 68, GOLD, weight=BOLD).next_to(allele, RIGHT, buff=0.45)
        self.play(FadeIn(unknown), run_time=1.1)
        self.at("surroundings change")
        light = Rectangle(width=14.0, height=8.0, fill_color="#34552F", fill_opacity=0.22,
                          stroke_width=0).move_to([7.0, 0, 0]).set_z_index(-2)
        dark = Rectangle(width=14.0, height=8.0, fill_color="#171127", fill_opacity=0.68,
                         stroke_width=0).move_to([21.0, 0, 0]).set_z_index(-1)
        self.add(light, dark)
        self.play(light.animate.shift(LEFT * 14), dark.animate.shift(LEFT * 14), run_time=3.0, rate_func=linear)
        effect = T("effect ?", 40, PURPLE, weight=BOLD).move_to([3.1, -1.15, 0])
        self.play(FadeIn(effect), run_time=1.0)
        self.finish()


class S14End(EndCard):
    LINE = "Genes and environments shape variation;\nchance mutations add new genetic differences."
