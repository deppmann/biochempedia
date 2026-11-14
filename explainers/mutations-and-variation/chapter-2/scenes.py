"""When a Mutation Matters — mutations-and-variation, chapter 2.

COLOR MAP (continued throughout this chapter)
  BLUE   inherited information / DNA
  GREEN  environment
  GOLD   mutation
  PURPLE changed trait
  RED    blocked route
  TEXT   other lines and measured outcomes
"""
from bp_parts import *  # noqa: F401,F403

PURPLE = "#B07CFF"


def mutation_card(at=(0, 2.35, 0), locked=False, scale=1.0):
    """The carried GOLD-corner allele card, always rebuilt at the same size."""
    box = RoundedRectangle(corner_radius=0.18, width=3.05, height=1.12,
                           stroke_color=BLUE, stroke_width=4,
                           fill_color=BLUE, fill_opacity=0.12)
    corner = Polygon(box.get_corner(UR), box.get_corner(UR) + LEFT * 0.65,
                     box.get_corner(UR) + DOWN * 0.65,
                     stroke_width=0, fill_color=GOLD, fill_opacity=1)
    label = T("DNA allele", 28, BLUE, weight=BOLD).move_to(box)
    # The label deliberately sits on its own card; the checker otherwise treats
    # the border and gold folded corner as objects drawn across the text.
    box.layout_ok = True
    corner.layout_ok = True
    g = VGroup(box, corner, label)
    if locked:
        shackle = Arc(radius=0.19, start_angle=0, angle=PI, color=GOLD,
                      stroke_width=5).move_to([0, -0.36, 0])
        body = RoundedRectangle(corner_radius=0.05, width=0.46, height=0.36,
                                stroke_color=GOLD, stroke_width=3,
                                fill_color=BG, fill_opacity=1).next_to(shackle, DOWN, buff=-0.08)
        lock = VGroup(shackle, body).move_to([0, -0.53, 0])
        g.add(lock)
    return g.scale(scale).move_to(at)


def beetle(at=(0, -0.25, 0), opacity=1.0, scale=1.0):
    """Large schematic beetle; PURPLE is the changed colour trait."""
    body = Ellipse(width=1.65, height=2.35, color=PURPLE, stroke_width=5,
                   fill_color=PURPLE, fill_opacity=0.78 * opacity)
    head = Circle(radius=0.5, color=PURPLE, stroke_width=5,
                  fill_color=PURPLE, fill_opacity=0.78 * opacity).next_to(body, UP, buff=-0.18)
    seam = Line(body.get_top() + DOWN * 0.15, body.get_bottom() + UP * 0.18,
                color=BG, stroke_width=3).set_opacity(opacity)
    legs = VGroup()
    for y in (-0.65, 0, 0.65):
        for side in (-1, 1):
            start = np.array([side * 0.68, y, 0])
            end = np.array([side * 1.15, y + (0.18 if y else 0), 0])
            legs.add(Line(start, end, color=PURPLE, stroke_width=5).set_opacity(opacity))
    antennae = VGroup(Line([-0.22, 1.35, 0], [-0.55, 1.78, 0], color=PURPLE, stroke_width=4),
                      Line([0.22, 1.35, 0], [0.55, 1.78, 0], color=PURPLE, stroke_width=4)).set_opacity(opacity)
    g = VGroup(legs, body, seam, head, antennae).scale(scale).move_to(at)
    g.marker = Dot(g.get_corner(UR) + LEFT * 0.15 + DOWN * 0.22, radius=0.14,
                   color=GOLD, stroke_color=TEXT, stroke_width=2)
    g.add(g.marker)
    return g


def shimmer(mob, base=0.22, amp=0.055, speed=2.5, seed=0.0):
    """Slow environment-light change across a broad filled region."""
    mob._shimmer_t = seed

    def update(m, dt):
        m._shimmer_t += dt
        m.set_fill(opacity=base + amp * np.sin(speed * m._shimmer_t))
    return mob.add_updater(update)


def panel_wash(at, color, width=5.7, height=3.7, opacity=0.12):
    return RoundedRectangle(corner_radius=0.14, width=width, height=height,
                            stroke_width=0, fill_color=color,
                            fill_opacity=opacity).move_to(at).set_z_index(-1)


def world_panels():
    """The single comparison world used from s03 through s07."""
    panels = TwoPanel("matching background", "contrasting background",
                      colors=(GREEN, GREEN), top=2.45, bottom=-2.35)
    left_fill = RoundedRectangle(corner_radius=0.16, width=5.75, height=3.85,
                                 stroke_width=0, fill_color=PURPLE, fill_opacity=0.28)
    right_fill = RoundedRectangle(corner_radius=0.16, width=5.75, height=3.85,
                                  stroke_width=0, fill_color=GREEN, fill_opacity=0.22)
    panels.put(left_fill, "left")
    panels.put(right_fill, "right")
    return panels, left_fill, right_fill


def comparison_backdrop(question=False, waiting=False):
    panels, lf, rf = world_panels()
    card = mutation_card(at=(0, 3.25, 0), locked=True, scale=0.8)
    bug = beetle(at=(-3.3, -0.2, 0), opacity=0.42, scale=0.78)
    objects = VGroup(panels, lf, rf, card, bug)
    objects.left_fill, objects.right_fill = lf, rf
    if waiting:
        swatch = RoundedRectangle(corner_radius=0.14, width=1.0, height=3.7,
                                  stroke_color=GREEN, stroke_width=4,
                                  fill_color=GREEN, fill_opacity=0.32).move_to([5.75, -0.1, 0])
        objects.add(swatch)
        objects.swatch = swatch
    objects.bug, objects.card = bug, card
    if question:
        q = question_card("Must DNA change first?", y=-3.12, size=34)
        objects.add(q)
    return objects


def eye(at=(5.1, 1.15, 0)):
    lid = ArcBetweenPoints(LEFT * 0.75, RIGHT * 0.75, angle=-1.0, color=TEXT, stroke_width=4)
    lower = ArcBetweenPoints(LEFT * 0.75, RIGHT * 0.75, angle=1.0, color=TEXT, stroke_width=4)
    iris = Circle(radius=0.22, color=TEXT, fill_color=TEXT, fill_opacity=0.75)
    return VGroup(lid, lower, iris).move_to(at)


def route_map():
    """Chapter-one inheritance route, rebuilt as one stable diagram."""
    parent = chip("parent", GREY, 30).move_to([-4.9, 0.2, 0])
    child = chip("offspring", GREY, 30).move_to([5.0, 0.2, 0])
    body = chip("body cell", GREY, 28).move_to([-1.7, 1.45, 0])
    sex = chip("sex cell", PURPLE, 28).move_to([-1.7, -1.2, 0])
    a1 = Arrow(parent.get_right(), body.get_left(), buff=0.14, color=TEXT, stroke_width=4)
    a2 = Arrow(parent.get_right(), sex.get_left(), buff=0.14, color=TEXT, stroke_width=4)
    blocked = Line(body.get_right(), [3.6, 1.45, 0], color=RED, stroke_width=6)
    cross = VGroup(Line([-0.25, -0.25, 0], [0.25, 0.25, 0]),
                   Line([-0.25, 0.25, 0], [0.25, -0.25, 0])).set_color(RED).set_stroke(width=8).move_to([2.1, 1.45, 0])
    possible = Arrow(sex.get_right(), child.get_left(), buff=0.15, color=TEXT, stroke_width=5)
    return VGroup(parent, child, body, sex, a1, a2, blocked, cross, possible)


class S00Hook(SpokenScene):
    def construct(self):
        bg = Rectangle(width=14.2, height=8, stroke_width=0, fill_color=GREEN, fill_opacity=0.08)
        shimmer(bg, base=0.11, amp=0.08, speed=2.1)
        card = mutation_card(at=(0, 0.2, 0), scale=1.35)
        pulse(card[1], base=2.5, amp=1.4, speed=2.3)
        self.at("first film showed")
        self.play(FadeIn(bg), FadeIn(card, scale=0.85), run_time=1.4)
        q = T("?", 90, GOLD, weight=BOLD).next_to(card, RIGHT, buff=0.6)
        effect = T("effect", 38, TEXT).next_to(card, DOWN, buff=0.55)
        self.at("how can one mutation")
        self.play(FadeIn(q), run_time=0.8)
        self.at("follow its effect")
        self.play(FadeIn(effect, shift=UP * 0.12), q.animate.next_to(effect, RIGHT, buff=0.25), run_time=0.9)
        shade = Rectangle(width=7.2, height=8, stroke_width=0, fill_color=GREEN,
                          fill_opacity=0.32).move_to([-7.2, 0, 0])
        self.at("keep the DNA fixed")
        self.play(shade.animate.shift(RIGHT * 14.4), run_time=3.0, rate_func=linear)
        self.finish()


class S01Title(TitleCard):
    LESSON = "Mutations and variation"
    TITLE = "When a Mutation Matters"


class S02NotLabel(SpokenScene):
    def construct(self):
        card = mutation_card(at=(0, 0.25, 0), scale=1.2)
        self.at("mutation does not")
        self.play(FadeIn(card), run_time=0.8)
        bug = beetle(at=(0, -0.1, 0), scale=1.15)
        self.at("effect depends")
        self.play(ReplacementTransform(card, bug), run_time=1.2)
        bob(bug, amp=0.045, speed=1.7)
        labels = VGroup(chip("helpful", GREEN, 28), chip("harmful", RED, 28),
                        chip("no difference", GREY, 28)).arrange(RIGHT, buff=0.55).move_to([0, 2.85, 0])
        self.at("start with color")
        self.play(FadeIn(labels, lag_ratio=0.2, shift=DOWN * 0.15), run_time=1.4)
        orbits = [ArcBetweenPoints(labels[i].get_bottom(), bug.get_top(), angle=(-0.6 + i * 0.6),
                                   color=GREY, stroke_width=2) for i in range(3)]
        self.play(*[Create(a) for a in orbits], run_time=0.7)
        self.at("label only makes sense")
        self.play(FadeOut(labels), FadeOut(VGroup(*orbits)), run_time=0.9)
        measured = T("measure an outcome first", 34, TEXT, weight=BOLD).move_to([0, 2.8, 0])
        self.play(FadeIn(measured), run_time=0.8)
        self.finish()


class S03Background(SpokenScene):
    def construct(self):
        panels, lf, rf = world_panels()
        bug = beetle(at=(-3.3, -0.2, 0), opacity=0.42, scale=0.78)
        bob(bug, amp=0.08, speed=2.2)
        shimmer(lf, base=0.28, amp=0.06, speed=2.2)
        shimmer(rf, base=0.22, amp=0.06, speed=2.4, seed=1.0)
        pulse(bug.marker, base=2.5, amp=1.3, speed=2)
        self.at("place the beetle")
        self.play(FadeIn(panels), FadeIn(lf), FadeIn(rf), FadeIn(bug), run_time=1.2)
        faint_eye = eye().set_opacity(0.3)
        self.at("harder to notice")
        self.play(FadeIn(faint_eye), run_time=0.7)
        self.at("slide the same beetle")
        self.play(bug.animate.move_to([3.3, -0.2, 0]).set_opacity(1),
                  faint_eye.animate.set_opacity(1), run_time=2.0)
        self.at("easier to notice")
        self.play(Indicate(bug, color=TEXT, scale_factor=1.05), run_time=0.8)
        self.at("model shows")
        self.play(FadeIn(scope_tag("schematic")), run_time=0.6)
        self.finish()


class S04Effect(SpokenScene):
    def construct(self):
        panels, lf, rf = world_panels()
        card = mutation_card(at=(0, 3.25, 0), locked=True, scale=0.8)
        self.add(panels, lf, rf, card)
        pulse(card[1], base=2.5, amp=1.2, speed=2.1)
        dna = T("DNA fixed", 34, BLUE, weight=BOLD).next_to(card, LEFT, buff=0.55)
        self.at("DNA did not change")
        self.play(FadeIn(dna), run_time=0.8)
        slider = RoundedRectangle(corner_radius=0.16, width=5.75, height=3.85,
                                  stroke_color=GREEN, stroke_width=4,
                                  fill_color=GREEN, fill_opacity=0.32).move_to(lf)
        env = T("environment moves", 32, GREEN, weight=BOLD).move_to([0, -2.75, 0])
        self.at("environment changed")
        self.play(slider.animate.move_to(rf), FadeIn(env), run_time=2.0)
        here = VGroup(T("effect here", 30, TEXT), T("?", 42, GOLD)).arrange(RIGHT, buff=0.2).move_to([-3.25, -0.1, 0])
        there = VGroup(T("effect there", 30, TEXT), T("?", 42, GOLD)).arrange(RIGHT, buff=0.2).move_to([3.25, -0.1, 0])
        link = DoubleArrow(here.get_right(), there.get_left(), buff=0.25, color=TEXT, stroke_width=4, tip_length=0.18)
        self.at("color that affects survival")
        self.play(FadeOut(slider), FadeIn(here), FadeIn(there), GrowFromCenter(link), run_time=1.4)
        self.at("separation is the key")
        self.play(Indicate(card, color=GOLD), Indicate(env, color=GREEN), run_time=1.0)
        self.finish()


class S05Predict(SpokenScene):
    def construct(self):
        world = comparison_backdrop(waiting=True)
        self.add(world)
        pulse(world.card[1], base=2.5, amp=1.2, speed=2)
        pulse(world.swatch, base=4, amp=1.5, speed=1.8)
        bob(world.bug, amp=0.08, speed=2.2)
        shimmer(world.left_fill, base=0.28, amp=0.055, speed=2.3)
        shimmer(world.right_fill, base=0.22, amp=0.055, speed=2.5, seed=1.0)
        self.at("predict before")
        self.play(FadeIn(T("PREDICT", 28, GOLD, weight=BOLD).move_to([-5.35, 3.25, 0])), run_time=0.7)
        q = question_card("Must DNA change first?", y=-3.12, size=34)
        self.at("background changes again")
        self.play(FadeIn(q.question), run_time=0.8)
        self.at("hold your answer")
        self.play(Indicate(q.question, color=GOLD), run_time=0.8)
        self.at("locked gold marker")
        self.play(Indicate(world.card, color=GOLD), run_time=0.9)
        self.finish()


class S06Pause(PredictPause):
    QUESTION = "Must DNA change first?"
    SECONDS = 4.5
    CARD = {"y": -3.12, "size": 34}

    def backdrop(self):
        world = comparison_backdrop(waiting=True)
        bob(world.bug, amp=0.045, speed=2)
        pulse(world.card[1], base=2.5, amp=1.2, speed=2)
        pulse(world.swatch, base=4, amp=1.4, speed=1.8)
        shimmer(world.left_fill, base=0.28, amp=0.055, speed=2.3)
        shimmer(world.right_fill, base=0.22, amp=0.055, speed=2.5, seed=1.0)
        return world


class S07Reveal(SpokenScene):
    def construct(self):
        world = comparison_backdrop(waiting=True)
        self.add(world)
        pulse(world.card[1], base=2.5, amp=1.2, speed=2)
        shimmer(world.left_fill, base=0.28, amp=0.055, speed=2.3)
        shimmer(world.right_fill, base=0.22, amp=0.055, speed=2.5, seed=1.0)
        answer = T("NO", 62, GOLD, weight=BOLD).move_to([5.65, 3.25, 0])
        self.play(FadeIn(answer, scale=0.7), run_time=0.7)
        self.at("keep the mutation fixed")
        self.play(world.swatch.animate.stretch_to_fit_width(5.75).move_to([3.3, -0.1, 0]), run_time=2.0)
        gauge_v = ValueTracker(0.3)
        gauge = dial(gauge_v, center=[3.3, -0.25, 0], radius=1.35,
                     label="survival + offspring", color=TEXT, fmt="{:.0f}", scale=10)
        self.at("effect can change")
        self.play(FadeOut(world.bug), FadeIn(gauge), run_time=0.8)
        self.at("survival and reproduction")
        self.play(gauge_v.animate.set_value(0.78), run_time=2.5, rate_func=linear)
        self.at("same change now")
        self.play(Indicate(world.card, color=GOLD), Indicate(gauge, color=TEXT), run_time=1.0)
        self.finish()


def outcome_lane(title, colour, y, width):
    change = chip("change", GOLD, 26).move_to([-4.9, y, 0])
    path = Arrow([-3.8, y, 0], [0.2, y, 0], buff=0, color=colour,
                 stroke_width=width, tip_length=0.25)
    out = chip(title, colour, 28).move_to([3.3, y, 0])
    return VGroup(change, path, out)


class S08ThreeOutcomes(SpokenScene):
    def construct(self):
        bands = VGroup(panel_wash([0, 1.65, 0], TEXT, width=12.2, height=1.35, opacity=0.08),
                       panel_wash([0, 0.05, 0], PURPLE, width=12.2, height=1.35, opacity=0.11),
                       panel_wash([0, -1.55, 0], GREEN, width=12.2, height=1.35, opacity=0.11))
        self.add(bands)
        shimmer(bands[0], base=0.08, amp=0.035, speed=2.3)
        shimmer(bands[1], base=0.11, amp=0.035, speed=2.5, seed=0.7)
        shimmer(bands[2], base=0.11, amp=0.035, speed=2.7, seed=1.4)
        heading = T("possible outcomes", 40, TEXT, weight=BOLD).move_to([0, 3.25, 0])
        self.play(FadeIn(heading), run_time=0.7)
        little = outcome_lane("little survival change", TEXT, 1.65, 10)
        self.at("change little")
        self.play(FadeIn(little[0]), GrowArrow(little[1]), FadeIn(little[2]), run_time=1.5)
        harm = outcome_lane("protein works poorly", PURPLE, 0.05, 7)
        self.at("some harm")
        self.play(FadeIn(harm[0]), GrowArrow(harm[1]), FadeIn(harm[2]), run_time=1.5)
        bob(harm[2], amp=0.07, speed=3)
        help_lane = outcome_lane("more growth: condition A", GREEN, -1.55, 4)
        self.at("few can help")
        self.play(FadeIn(help_lane[0]), GrowArrow(help_lane[1]), FadeIn(help_lane[2]), run_time=1.5)
        target = Circle(radius=0.38, color=TEXT, stroke_width=4).move_to([0, -2.75, 0])
        target.add(Dot(target.get_center(), radius=0.1, color=TEXT))
        slash = Line(target.get_corner(DL), target.get_corner(UR), color=RED, stroke_width=7)
        intention = T("not intentions", 32, RED, weight=BOLD).next_to(target, RIGHT, buff=0.3)
        self.at("outcomes not intentions")
        self.play(Create(target), Create(slash), FadeIn(intention), run_time=1.0)
        self.at("how much protein")
        bars = VGroup(*[Rectangle(width=w, height=0.22, stroke_width=0, fill_color=PURPLE,
                                  fill_opacity=0.85) for w in (0.8, 1.3, 1.9)]).arrange(DOWN, buff=0.14)
        bars.move_to(harm[2])
        self.play(FadeOut(harm[2]), FadeIn(bars), run_time=1.0)
        self.add(scope_tag("schematic"))
        self.finish()


def growth_curve(panel_center, colour, rise=1.0, offset=0.0):
    x0, y0 = panel_center[0] - 2.15, panel_center[1] - 1.25
    pts = []
    for x in np.linspace(0, 4.1, 60):
        y = 2.15 * (1 - np.exp(-rise * x / 2.0)) + offset
        pts.append([x0 + x, y0 + y, 0])
    m = VMobject(stroke_color=colour, stroke_width=6, fill_opacity=0)
    m.set_points_as_corners(pts)
    return m


class S09Bacteria(SpokenScene):
    def construct(self):
        card = mutation_card(at=(0, 3.25, 0), locked=True, scale=0.8)
        panels = TwoPanel("antibiotic present", "different food",
                          colors=(TEXT, GREEN), top=2.45, bottom=-2.35)
        washes = VGroup(panel_wash([-3.3, -0.1, 0], TEXT, height=3.7, opacity=0.09),
                         panel_wash([3.3, -0.1, 0], GREEN, height=3.7, opacity=0.13))
        shimmer(washes[0], base=0.09, amp=0.035, speed=2.3)
        shimmer(washes[1], base=0.13, amp=0.04, speed=2.5, seed=1.0)
        self.at("bacteria make")
        self.play(FadeIn(card), FadeIn(washes), FadeIn(panels), run_time=1.0)
        dish = Circle(radius=1.55, color=TEXT, stroke_width=4,
                      fill_color=TEXT, fill_opacity=0.05)
        panels.put(dish, "left")
        colonies = VGroup(*[Dot(radius=0.1 + 0.015 * (i % 3), color=PURPLE)
                            for i in range(18)]).arrange_in_grid(3, 6, buff=0.25).move_to(dish)
        self.at("allow growth")
        self.play(Create(dish), FadeIn(colonies, lag_ratio=0.08), run_time=1.6)
        c1 = growth_curve([3.3, -0.1, 0], PURPLE, rise=1.4)
        c2 = growth_curve([3.3, -0.1, 0], TEXT, rise=0.7, offset=-0.05)
        food = chip("food A", GREEN, 28).move_to([3.3, 1.25, 0])
        self.at("different food")
        self.play(FadeIn(food), Create(c1), Create(c2), run_time=1.6)
        nc1 = growth_curve([3.3, -0.1, 0], PURPLE, rise=0.55)
        nc2 = growth_curve([3.3, -0.1, 0], TEXT, rise=1.5, offset=0.05)
        food_b = chip("food B", GREEN, 28).move_to(food)
        self.at("grows best can change")
        self.play(swap(food, food_b), Transform(c1, nc1), Transform(c2, nc2), run_time=2.0)
        self.at("both parts")
        self.play(Indicate(panels.left_head, color=TEXT), Indicate(food_b, color=GREEN), run_time=1.0)
        self.add(scope_tag("schematic"))
        self.finish()


class S10People(SpokenScene):
    def construct(self):
        panels = TwoPanel("where adults drink milk", "earwax trait",
                          colors=(GREEN, PURPLE), top=3.0, bottom=-2.45)
        washes = VGroup(panel_wash([-3.3, -0.05, 0], GREEN, height=4.45, opacity=0.12),
                         panel_wash([3.3, -0.05, 0], PURPLE, height=4.45, opacity=0.12))
        shimmer(washes[0], base=0.12, amp=0.04, speed=2.3)
        shimmer(washes[1], base=0.12, amp=0.04, speed=2.5, seed=1.0)
        self.at("human examples")
        self.play(FadeIn(washes), FadeIn(panels), run_time=0.9)
        person = VGroup(Circle(radius=0.4, color=TEXT),
                        RoundedRectangle(corner_radius=0.25, width=1.5, height=2.4,
                                         color=TEXT, fill_color=TEXT, fill_opacity=0.08)).arrange(DOWN, buff=0.08)
        cup = VGroup(Rectangle(width=0.85, height=1.0, color=TEXT, stroke_width=4,
                               fill_color=TEXT, fill_opacity=0.12),
                     Arc(radius=0.35, start_angle=-PI/2, angle=PI, color=TEXT, stroke_width=4).shift(RIGHT * 0.5))
        lactase = chip("lactase working", PURPLE, 28)
        left = VGroup(person, cup, lactase).arrange(RIGHT, buff=0.4)
        panels.put(left, "left")
        self.at("continued lactase")
        self.play(FadeIn(person), FadeIn(cup), FadeIn(lactase), run_time=1.4)
        wet = VGroup(Arc(radius=0.75, start_angle=-PI/2, angle=1.55 * PI,
                         color=PURPLE, stroke_width=6), T("wet", 28, PURPLE)).arrange(DOWN, buff=0.25)
        dry = VGroup(Arc(radius=0.75, start_angle=-PI/2, angle=1.55 * PI,
                         color=PURPLE, stroke_width=6), T("dry", 28, PURPLE)).arrange(DOWN, buff=0.25)
        ears = VGroup(wet, dry).arrange(RIGHT, buff=0.75)
        panels.put(ears, "right")
        self.at("dry ear wax")
        self.play(FadeIn(ears), run_time=1.1)
        neutral = T("no survival effect shown", 30, TEXT, weight=BOLD).move_to([3.25, -1.8, 0])
        self.at("no survival effect")
        self.play(FadeIn(neutral), run_time=0.9)
        self.at("different traits")
        self.play(Indicate(lactase, color=PURPLE), Indicate(ears, color=PURPLE), run_time=1.0)
        self.finish()


class S11Inheritance(SpokenScene):
    def construct(self):
        routes = route_map()
        route_washes = VGroup(panel_wash([0.25, 1.45, 0], RED, width=8.2, height=1.55, opacity=0.1),
                              panel_wash([0.25, -1.2, 0], PURPLE, width=8.2, height=1.55, opacity=0.11))
        shimmer(route_washes[0], base=0.1, amp=0.045, speed=2.4)
        shimmer(route_washes[1], base=0.11, amp=0.045, speed=2.6, seed=1.0)
        title = T("effect ≠ inheritance", 42, TEXT, weight=BOLD).move_to([0, 3.4, 0])
        self.at("effect and inheritance")
        self.play(FadeIn(title), FadeIn(route_washes), FadeIn(routes), run_time=1.2)
        body_mark = Dot([-0.85, 1.78, 0], radius=0.16, color=GOLD)
        sex_mark = Dot([-0.85, -0.88, 0], radius=0.16, color=GOLD)
        body_v, sex_v = ValueTracker(0.8), ValueTracker(0.25)
        body_g = dial(body_v, center=[4.5, 1.75, 0], radius=0.6, color=TEXT,
                      fmt="{:.0f}", scale=10, size=26)
        sex_g = dial(sex_v, center=[2.2, -1.45, 0], radius=0.6, color=TEXT,
                     fmt="{:.0f}", scale=10, size=26)
        self.at("helpful body cell")
        self.play(FadeIn(body_mark), FadeIn(body_g), run_time=0.9)
        self.at("cannot reach offspring")
        self.play(Indicate(routes[7], color=RED), run_time=1.0)
        self.at("sex cell mutation")
        self.play(FadeIn(sex_mark), FadeIn(sex_g), run_time=0.9)
        self.at("pass without")
        self.play(MoveAlongPath(sex_mark.copy(), routes[8]), run_time=1.8)
        self.at("usefulness cannot open")
        self.play(body_v.animate.set_value(1.0), Indicate(routes[7], color=RED), run_time=1.5)
        self.finish()


def evidence_chain():
    items = [("changed trait", PURPLE), ("environment", GREEN),
             ("survival", TEXT), ("offspring", TEXT)]
    boxes = VGroup(*[RoundedRectangle(corner_radius=0.18, width=2.55, height=2.7,
                                      stroke_color=c, stroke_width=4,
                                      fill_color=c, fill_opacity=0.08) for _, c in items]).arrange(RIGHT, buff=0.55)
    labels = VGroup(*[T(t, 28, c, weight=BOLD).move_to(b.get_top() + DOWN * 0.42)
                      for (t, c), b in zip(items, boxes)])
    icons = VGroup(
        Ellipse(width=1.15, height=1.5, color=PURPLE, fill_color=PURPLE, fill_opacity=0.55),
        VGroup(*[Line([-0.5, y, 0], [0.5, y, 0], color=GREEN, stroke_width=7) for y in (-0.35, 0, 0.35)]),
        VGroup(Arc(radius=0.65, start_angle=PI, angle=-PI, color=TEXT, stroke_width=6),
               Line(ORIGIN, [0.45, 0.35, 0], color=TEXT, stroke_width=5)),
        VGroup(*[Dot(radius=0.14, color=TEXT) for _ in range(6)]).arrange_in_grid(2, 3, buff=0.28))
    for icon, box in zip(icons, boxes):
        icon.move_to(box.get_center() + DOWN * 0.35)
    return VGroup(boxes, labels, icons)


class S12Evidence(SpokenScene):
    def construct(self):
        card = mutation_card(at=(0, 3.0, 0), scale=0.85)
        chain = evidence_chain().move_to([0, -0.45, 0])
        for i, box in enumerate(chain[0]):
            shimmer(box, base=0.13, amp=0.04, speed=2.2 + i * 0.18, seed=i * 0.6)
        self.at("do not judge")
        self.play(FadeIn(card), run_time=0.7)
        self.at("compare the changed trait")
        self.play(FadeIn(chain[0][0]), FadeIn(chain[1][0]), FadeIn(chain[2][0]), run_time=0.9)
        self.at("the environment")
        self.play(FadeIn(chain[0][1]), FadeIn(chain[1][1]), FadeIn(chain[2][1]), run_time=0.9)
        self.at("survival")
        self.play(FadeIn(chain[0][2]), FadeIn(chain[1][2]), FadeIn(chain[2][2]), run_time=0.7)
        self.at("and reproduction")
        self.play(FadeIn(chain[0][3]), FadeIn(chain[1][3]), FadeIn(chain[2][3]), run_time=0.7)
        lens = Circle(radius=0.58, color=GOLD, stroke_width=6)
        lens.layout_ok = True  # it deliberately surrounds each evidence icon
        handle = Line([0.5, -0.5, 0], [1.0, -1.0, 0], color=GOLD, stroke_width=7)
        glass = VGroup(lens, handle).move_to(chain[2][0])
        self.at("evidence decides")
        self.play(FadeIn(glass), run_time=0.5)
        for icon in chain[2][1:]:
            self.play(glass.animate.move_to(icon), run_time=0.7)
        self.at("label is only")
        guess = T("label = guess without comparison", 32, GOLD, weight=BOLD).move_to([0, -3.2, 0])
        self.play(FadeIn(guess), run_time=0.8)
        self.finish()


class S13Handoff(SpokenScene):
    def construct(self):
        chain = evidence_chain().move_to([0, -0.45, 0])
        self.add(chain)
        headers = ["change", "living thing", "what it does", "effect"]
        table = VGroup()
        for i, h in enumerate(headers):
            x = -4.65 + i * 3.1
            box = Rectangle(width=2.95, height=3.4, color=(PURPLE if i == 0 else GREEN if i == 1 else TEXT),
                            stroke_width=4, fill_color=(PURPLE if i == 0 else GREEN if i == 1 else TEXT),
                            fill_opacity=0.1).move_to([x, -0.1, 0])
            lab = fit_text(h, max_w=2.6, size=28, color=TEXT).move_to([x, 1.15, 0])
            blank = Line([x - 1.1, -0.2, 0], [x + 1.1, -0.2, 0], color=GREY, stroke_width=3)
            table.add(VGroup(box, lab, blank))
        self.at("tables below")
        self.play(FadeOut(chain), run_time=0.5)
        self.play(FadeIn(table), run_time=1.0)
        self.at("separate what changed")
        self.play(Indicate(table[0], color=PURPLE), Indicate(table[3], color=TEXT), run_time=1.0)
        self.at("conditions in which")
        self.play(Indicate(table[1], color=GREEN), Indicate(table[2], color=TEXT), run_time=1.0)
        self.at("text also gives limits")
        limits = T("read the limits too", 34, GOLD, weight=BOLD).move_to([0, -2.8, 0])
        self.play(FadeIn(limits), run_time=0.8)
        self.finish()


class S14End(EndCard):
    LINE = "A mutation’s effect depends on the change and often on its environment."
