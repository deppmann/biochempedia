"""Chapter 2: test the energy pyramid against the Silver Springs measurements.

COLOR MAP (continued from chapter 1):
GOLD energy/sunlight; GREEN producers; BLUE first-order consumers;
ORANGE second-order consumers; PURPLE third-order consumers;
GREY decomposers/material; RED heat.
"""
from bp_parts import *


ORANGE = "#FF9F43"
PURPLE = "#B084F5"

VALUES = [20810.0, 3368.0, 383.0, 21.0]
COLORS = [GREEN, BLUE, ORANGE, PURPLE]
NAMES = ["Producers", "First-order", "Second-order", "Third-order"]
RATIOS = [VALUES[i + 1] / VALUES[i] for i in range(3)]


def moving_water(top=2.55, bottom=-2.8, color=BLUE):
    """The carried water field used in every Bay and spring picture."""
    water = Rectangle(width=13.5, height=top - bottom, stroke_width=0,
                      fill_color=color, fill_opacity=0.14).move_to([0, (top + bottom) / 2, 0])
    water.layout_ok = True
    lines = VGroup()
    for i, y in enumerate(np.linspace(bottom + 0.35, top - 0.35, 7)):
        wave = FunctionGraph(lambda x, y=y, i=i: y + 0.055 * np.sin(2.2 * x + i),
                             x_range=[-6.7, 6.7, 0.12], color=BLUE, stroke_width=2,
                             stroke_opacity=0.28)
        wave.phase = i * 0.53

        def drift(mob, dt):
            mob.phase += dt * 0.75
            mob.become(FunctionGraph(lambda x, yy=y, p=mob.phase: yy + 0.055 * np.sin(2.2 * x + p),
                                     x_range=[-6.7, 6.7, 0.12], color=BLUE,
                                     stroke_width=2, stroke_opacity=0.28))
        wave.add_updater(drift)
        lines.add(wave)
    return VGroup(water, lines)


def producer_patch(at=(-4.65, -2.25, 0), scale=1.0):
    blades = VGroup(*[
        ArcBetweenPoints([x, -2.55, 0], [x + 0.12 * (-1) ** i, -1.75 - 0.18 * (i % 2), 0],
                         angle=0.22 * (-1) ** i, color=GREEN, stroke_width=8)
        for i, x in enumerate(np.linspace(-0.65, 0.65, 6))
    ])
    blades.scale(scale).move_to(at)
    return blades


def fish(color=ORANGE, length=1.0, at=ORIGIN, flip=False):
    body = Ellipse(width=1.45 * length, height=0.58 * length, color=color,
                   fill_color=color, fill_opacity=0.28, stroke_width=4)
    side = RIGHT if flip else LEFT
    tail = Polygon(side * 0.62 * length + UP * 0.02,
                   side * 1.02 * length + UP * 0.36 * length,
                   side * 1.02 * length + DOWN * 0.36 * length,
                   color=color, fill_color=color, fill_opacity=0.22, stroke_width=4)
    eye_x = -0.42 if flip else 0.42
    eye = Dot([eye_x * length, 0.10 * length, 0], radius=0.045 * length, color=TEXT)
    g = VGroup(tail, body, eye).move_to(at)
    return g


def plankton(color=BLUE, at=ORIGIN, scale=1.0):
    core = Circle(radius=0.24, color=color, fill_color=color, fill_opacity=0.3, stroke_width=4)
    arms = VGroup(*[Line(0.23 * d, 0.48 * d, color=color, stroke_width=3)
                    for d in (UP, DOWN, LEFT, RIGHT, UL, UR, DL, DR)])
    return VGroup(arms, core).scale(scale).move_to(at)


def osprey(at=(4.65, 2.3, 0), scale=1.0):
    wings = VGroup(
        ArcBetweenPoints(LEFT * 1.25, ORIGIN, angle=-0.65, color=PURPLE, stroke_width=8),
        ArcBetweenPoints(ORIGIN, RIGHT * 1.25, angle=-0.65, color=PURPLE, stroke_width=8),
    )
    body = Ellipse(width=0.42, height=0.85, color=PURPLE, fill_color=PURPLE, fill_opacity=0.25)
    return VGroup(wings, body).scale(scale).move_to(at)


def ecosystem_world(kind="spring", labels=False):
    """One-world builder: identical landmarks for every carried cross-section."""
    water = moving_water()
    bottom_color = "#C9B27A" if kind == "spring" else "#5B4634"
    bottom = Rectangle(width=13.5, height=0.55, stroke_width=0, fill_color=bottom_color,
                       fill_opacity=0.3).move_to([0, -2.72, 0])
    bottom.layout_ok = True
    plants = producer_patch((-4.9, -2.15, 0), 1.05)
    zoo = VGroup(plankton(BLUE, (-2.1, -0.45, 0), 1.05), plankton(BLUE, (-1.1, 0.45, 0), 0.8))
    small_fish = VGroup(fish(ORANGE, 0.9, (0.9, -0.65, 0)), fish(ORANGE, 0.72, (1.9, 0.25, 0)))
    top_fish = fish(PURPLE, 1.0, (3.7, 0.85, 0))
    bird = osprey((4.85, 2.55, 0), 0.8)
    sun = VGroup(Circle(radius=0.36, color=GOLD, fill_color=GOLD, fill_opacity=0.3),
                 *[Line(0.48 * d, 0.73 * d, color=GOLD, stroke_width=4)
                   for d in (UP, DOWN, LEFT, RIGHT, UL, UR, DL, DR)]).move_to([-5.65, 2.72, 0])
    world = VGroup(water, bottom, plants, zoo, small_fish, top_fish, bird, sun)
    bob(zoo, amp=0.09, speed=1.1)
    bob(small_fish, amp=0.07, speed=1.35, seed=2)
    bob(top_fish, amp=0.08, speed=1.0, seed=3)
    bob(bird, amp=0.08, speed=1.3, seed=4)
    pulse(sun[0], base=4.0, amp=1.5, speed=2.0)
    if labels:
        tag = chip("rough yearly estimates", GREY, 28).move_to([0, 3.25, 0])
        world.add(tag)
    world.plants, world.zoo, world.small_fish = plants, zoo, small_fish
    world.top_fish, world.bird, world.sun = top_fish, bird, sun
    return world


def energy_bar(value, color, y, min_width=0.16, max_width=10.8, height=0.62):
    width = max(min_width, max_width * value / VALUES[0])
    r = RoundedRectangle(corner_radius=0.1, width=width, height=height, color=color,
                         fill_color=color, fill_opacity=0.42, stroke_width=4).move_to([0, y, 0])
    r.layout_ok = True  # labels intentionally sit near, never across, the data bars
    return r


def data_stage(color=BLUE):
    """Large, gently moving data field shared by every measured-bar scene."""
    board = RoundedRectangle(corner_radius=0.22, width=12.7, height=5.35,
                             stroke_color=GREY, stroke_width=2,
                             fill_color=color, fill_opacity=0.14).move_to([0, -0.05, 0])
    board.layout_ok = True
    band = Rectangle(width=1.15, height=5.05, stroke_width=0,
                     fill_color=GOLD, fill_opacity=0.11).move_to([-5.65, -0.05, 0])
    band.layout_ok = True
    band.clock = 0.0

    def scan(mob, dt):
        mob.clock = (mob.clock + dt * 0.72) % 11.3
        mob.move_to([-5.65 + mob.clock, -0.05, 0])
    band.add_updater(scan)
    stage = VGroup(board, band).set_z_index(-5)
    return stage


def sweep_line(x0=-5.2, x1=5.2, y0=-1.95, y1=1.9, color=GOLD, speed=0.55):
    """A sustained ruler sweep for the measured data scenes."""
    line = Line([x0, y0, 0], [x0, y1, 0], color=color, stroke_width=10).set_opacity(0.82)
    line.clock = 0.0

    def move(mob, dt):
        mob.clock += dt * speed
        u = 0.5 - 0.5 * np.cos(mob.clock)
        x = x0 + (x1 - x0) * u
        mob.put_start_and_end_on([x, y0, 0], [x, y1, 0])
    return line.add_updater(move)


def flowing_packets(points, count=7, color=GOLD, speed=0.12, radius=0.075):
    """Gold packets that continuously traverse a stated energy route."""
    pts = [np.array(p, dtype=float) for p in points]
    g = VGroup()
    for i in range(count):
        d = Dot(pts[0], radius=radius, color=color)
        d.clock = i / count

        def move(mob, dt, pts=pts):
            mob.clock = (mob.clock + dt * speed) % 1.0
            z = mob.clock * (len(pts) - 1)
            j = min(int(z), len(pts) - 2)
            u = z - j
            mob.move_to(interpolate(pts[j], pts[j + 1], u))
        d.add_updater(move)
        g.add(d)
    return g


def measured_stack(with_labels=True, covered=False, include_marker=False, compact=False):
    """The computed Silver Springs stack, rebuilt in exactly one place."""
    ys = [-1.55, -0.55, 0.45, 1.45]
    bars = VGroup(*[energy_bar(v, c, y, min_width=(0.42 if compact else 0.26),
                              max_width=(7.8 if compact else 10.8))
                    for v, c, y in zip(VALUES, COLORS, ys)])
    g = VGroup(bars)
    g.bars = bars
    if with_labels:
        labs = VGroup(*[
            T(f"{n}  {int(v):,}", 28, c).next_to(b, RIGHT, buff=0.18)
            for n, v, c, b in zip(NAMES, VALUES, COLORS, bars)
        ])
        g.add(labs)
        g.labels = labs
    if covered:
        cards = division_cards(covered=True)
        g.add(cards)
        g.cards = cards
    if include_marker:
        marker = model_marker()
        g.add(marker)
        g.marker = marker
    return g


def model_marker(x=3.55):
    line = DashedLine([2.15, -1.95, 0], [5.9, -1.95, 0], color=GOLD, stroke_width=3)
    label = T("10% classroom model", 26, GOLD).next_to(line, DOWN, buff=0.3)
    return VGroup(line, label)


def division_cards(covered=True):
    ys = [1.35, 0.0, -1.35]
    pairs = [(3368, 20810), (383, 3368), (21, 383)]
    g = VGroup()
    for i, ((num, den), y) in enumerate(zip(pairs, ys)):
        eq = M(f"{num:,} ÷ {den:,}", 25, COLORS[i + 1]).move_to([2.85, y, 0])
        arrow = Arrow([4.25, y, 0], [4.65, y, 0], color=GOLD, buff=0.02, stroke_width=5,
                      max_tip_length_to_length_ratio=0.32)
        text = "?" if covered else f"{100 * RATIOS[i]:.1f}%"
        result = chip(text, GREY if covered else COLORS[i + 1], 28).move_to([5.35, y, 0])
        g.add(VGroup(eq, arrow, result))
    return g


def predict_frame():
    stack = measured_stack(with_labels=False)
    stack.scale(0.62).shift(LEFT * 2.45 + UP * 0.15)
    cards = division_cards(covered=True)
    choices = VGroup(chip("match exactly", GREY, 30), chip("differ", GREY, 30)).arrange(RIGHT, buff=0.55)
    choices.move_to([0, 3.3, 0])
    q = question_card("Same fraction every time?", y=-3.15, size=31)
    marker = model_marker()
    return VGroup(stack, cards, choices, q, marker)


def arrow_between(a, b, color=GOLD, width=6, dashed=False):
    cls = DashedLine if dashed else Arrow
    if dashed:
        return cls(a, b, color=color, stroke_width=width, dash_length=0.14)
    return cls(a, b, color=color, stroke_width=width, buff=0.08,
               max_tip_length_to_length_ratio=0.18)


class S00Hook(SpokenScene):
    def construct(self):
        world = ecosystem_world("bay")
        self.add(world)
        bars = VGroup(*[energy_bar(10 ** (3 - i), c, -1.35 + i * 0.9,
                                       min_width=0.75, max_width=7.8, height=0.54)
                        for i, c in enumerate(COLORS)])
        stamp = chip("classroom model", GOLD, 29).move_to([0, 3.2, 0])
        self.at("first film followed")
        self.play(LaggedStart(*[GrowFromCenter(b) for b in bars], lag_ratio=0.16), run_time=1.7)
        self.play(FadeIn(stamp), run_time=0.7)
        self.at("Do real measurements")
        qs = VGroup(*[T("?", 50, c).move_to(b) for b, c in zip(bars, COLORS)])
        self.play(Transform(bars, qs), FadeOut(stamp), run_time=1.3)
        question = T("Do real steps match?", 38, GOLD).move_to([0, -2.8, 0])
        self.play(FadeIn(question, shift=UP * 0.12), run_time=0.7)
        self.at("Test the model")
        self.play(Indicate(question, color=GOLD, scale_factor=1.05), run_time=1.0)
        self.finish()


class S01Title(TitleCard):
    LESSON = "Food Webs and Energy"
    TITLE = "Test the Pyramid with Real Data"


class S02Spring(SpokenScene):
    def construct(self):
        world = ecosystem_world("spring")
        self.add(world)
        place = T("Silver Springs, Florida", 36, TEXT).move_to([0, 3.28, 0])
        self.at("measurements come from")
        self.play(FadeIn(place), run_time=0.8)
        self.at("Researchers estimated")
        calendar = RoundedRectangle(corner_radius=0.15, width=1.45, height=1.3, color=GOLD,
                                    fill_color=BG, fill_opacity=0.88).move_to([5.45, -1.65, 0])
        calendar.layout_ok = True
        season = T("SPRING", 25, GOLD).move_to(calendar)
        season.layout_ok = True  # intentional calendar-face label
        self.play(FadeIn(calendar), FadeIn(season), run_time=0.7)
        for name, col in (("SUMMER", GREEN), ("AUTUMN", ORANGE), ("WINTER", BLUE)):
            nxt = T(name, 25, col).move_to(calendar)
            nxt.layout_ok = True  # intentional calendar-face label
            self.play(swap(season, nxt), run_time=0.55)
            season = nxt
        self.at("values were rough")
        rough = chip("rough yearly estimates", GREY, 30).move_to([0, 3.28, 0])
        self.play(swap(place, rough), run_time=0.9)
        self.at("Each value combines")
        area = DashedVMobject(RoundedRectangle(corner_radius=0.25, width=11.7, height=5.2,
                                               color=GOLD, stroke_width=3), num_dashes=40)
        area.move_to([0, -0.15, 0])
        self.play(Create(area), run_time=1.0)
        self.finish()


class S03Producers(SpokenScene):
    def construct(self):
        world = ecosystem_world("spring")
        plants = world.plants.copy()
        sun = world.sun.copy()
        self.add(world)
        rays = VGroup(*[Arrow(sun.get_center() + RIGHT * 0.3, plants.get_top() + v,
                              color=GOLD, buff=0.1, stroke_width=5)
                        for v in (LEFT * 0.35, ORIGIN, RIGHT * 0.35)])
        self.at("Start with energy")
        self.play(LaggedStart(*[GrowArrow(a) for a in rays], lag_ratio=0.18), run_time=1.1)
        glow = SurroundingRectangle(plants, color=GOLD, buff=0.18, stroke_width=6)
        self.play(Create(glow), run_time=0.7)
        self.at("Their green bar")
        stage = data_stage()
        bar = energy_bar(VALUES[0], GREEN, 0, max_width=10.8, height=1.05)
        label = T("Producers  20,810", 32, GREEN).move_to([0, 2.9, 0])
        self.play(FadeOut(world), FadeOut(rays), FadeOut(glow), FadeIn(stage),
                  GrowFromCenter(bar), run_time=1.25)
        self.play(FadeIn(label), run_time=0.65)
        axis = Line([-5.4, -1.0, 0], [5.4, -1.0, 0], color=GREY, stroke_width=3)
        unit = T("kilocalories per square meter per year", 28, TEXT).next_to(axis, DOWN, buff=0.2)
        note = scope_tag("computed from lesson table")
        self.at("This is the producer")
        self.play(Create(axis), FadeIn(unit), FadeIn(note), run_time=1.0)
        self.at("Everything above")
        paths = VGroup(*[Arrow([x, 0.65, 0], [x, 2.35, 0], color=GOLD, stroke_width=4,
                                    buff=0.05) for x in (-3.2, 0, 3.2)])
        self.play(LaggedStart(*[GrowArrow(a) for a in paths], lag_ratio=0.2), run_time=1.2)
        packets = VGroup(*[flowing_packets([[x, 0.55, 0], [x, 2.35, 0]], count=3,
                                          speed=0.16 + 0.02 * i)
                           for i, x in enumerate((-3.2, 0, 3.2))])
        self.add(packets)
        self.finish()


class S04Consumers(SpokenScene):
    def construct(self):
        stage = data_stage()
        stack = measured_stack(with_labels=False)
        producer = stack.bars[0]
        self.add(stage, producer)
        first_label = T("Producers  20,810", 28, TEXT).move_to(producer.get_left() + RIGHT * 1.55)
        first_label.layout_ok = True
        labels = VGroup(first_label)
        self.add(labels)
        self.at("add the consumers")
        for i in range(1, 4):
            b = stack.bars[i]
            lab = T(f"{NAMES[i]}  {int(VALUES[i]):,}", 28, TEXT)
            lab.move_to([-4.9 + lab.width / 2, b.get_y(), 0])
            lab.layout_ok = True
            self.play(GrowFromCenter(b), FadeIn(lab), run_time=0.72)
            labels.add(lab)
        note = T("thin bars enlarged to be visible", 24, GREY).move_to([0, -2.45, 0])
        self.play(FadeIn(note), run_time=0.55)
        self.at("Each measured bar")
        ruler = sweep_line(-5.2, 5.2, -1.92, 1.85, speed=0.62)
        self.play(Create(ruler), run_time=0.7)
        self.at("A narrower bar")
        for i in range(3):
            self.play(Indicate(stack.bars[i + 1], color=GOLD, scale_factor=1.03), run_time=0.65)
        self.at("Yet the bars")
        end_ticks = VGroup(*[Line(b.get_right() + DOWN * 0.22, b.get_right() + UP * 0.22,
                                      color=GOLD, stroke_width=5) for b in stack.bars])
        self.play(LaggedStart(*[Create(t) for t in end_ticks], lag_ratio=0.16),
                  FadeOut(ruler), run_time=1.15)
        self.finish()


class S05Percentages(SpokenScene):
    def construct(self):
        stage = data_stage()
        stack = measured_stack(with_labels=False)
        stack.scale(0.62).shift(LEFT * 2.45 + UP * 0.15)
        self.add(stage, stack)
        ruler = sweep_line(-5.6, -0.7, -1.75, 1.75, speed=0.5)
        self.add(ruler)
        cards = division_cards(covered=True)
        self.at("Calculate each transfer")
        for card in cards:
            self.play(FadeIn(card[0]), GrowArrow(card[1]), FadeIn(card[2]), run_time=0.76)
        self.at("Each result describes")
        hops = VGroup(*[Arrow(stack.bars[i].get_top(), stack.bars[i + 1].get_bottom(),
                                  color=GOLD, buff=0.05, stroke_width=5)
                        for i in range(3)])
        self.play(LaggedStart(*[GrowArrow(a) for a in hops], lag_ratio=0.22), run_time=1.15)
        self.at("A fixed law")
        marker = model_marker()
        self.play(Create(marker[0]), FadeIn(marker[1]), run_time=0.9)
        self.at("uneven bars already")
        self.play(LaggedStart(*[Indicate(b, color=GOLD, scale_factor=1.04) for b in stack.bars],
                              lag_ratio=0.2), run_time=1.35)
        self.finish()


class S06Predict(SpokenScene):
    def construct(self):
        stage = data_stage()
        frame = predict_frame()
        stack, cards, choices, q, marker = frame
        self.add(stage, stack, cards, marker)
        self.add(sweep_line(-5.6, -0.7, -1.75, 1.75, speed=0.5))
        self.at("Will the three")
        self.play(FadeIn(choices), run_time=0.9)
        self.play(FadeIn(q), run_time=0.7)
        self.at("Choose before")
        self.play(LaggedStart(*[Indicate(c, color=GOLD, scale_factor=1.04) for c in choices],
                              lag_ratio=0.45), run_time=1.25)
        self.at("Use each neighboring")
        self.play(LaggedStart(*[Indicate(c[0], color=GOLD, scale_factor=1.03) for c in cards],
                              lag_ratio=0.23), run_time=1.2)
        self.finish()


class S07Pause(NarratedScene):
    def construct(self):
        stage = data_stage()
        frame = predict_frame()
        self.add(stage, frame)
        self.add(sweep_line(-5.6, -0.7, -1.75, 1.75, speed=0.5))
        ring, run = countdown(4.5, center=[6.0, -3.05, 0])
        self.add(ring)
        self.play(run)
        self.finish()


class S08Reveal(SpokenScene):
    def construct(self):
        stage = data_stage()
        frame = predict_frame()
        stack, covered, choices, q, marker = frame
        self.add(stage, stack, covered, choices, q, marker)
        ruler = sweep_line(-5.6, -0.7, -1.75, 1.75, speed=0.5)
        self.add(ruler)
        differ = choices[1]
        self.at("They differ")
        bright = chip("differ", GOLD, 30).move_to(differ)
        self.play(swap(differ, bright), run_time=0.7)
        results = division_cards(covered=False)
        foot = T("of all captured energy", 22, GREY).move_to([4.0, 0.68, 0])
        self.at("three measured steps")
        for old, new in zip(covered, results):
            self.play(swap(old[2], new[2]), run_time=0.58)
        self.play(FadeIn(foot), run_time=0.6)
        self.at("Real transfer varies")
        dots = VGroup(*[Dot([3.55 + (r - 0.10) * 13.0, -2.0, 0], radius=0.12,
                                 color=c) for r, c in zip(RATIOS, COLORS[1:])])
        baseline = Line([2.35, -2.0, 0], [5.45, -2.0, 0], color=GREY, stroke_width=3)
        ten = Line([3.55, -2.2, 0], [3.55, -1.8, 0], color=GOLD, stroke_width=5)
        self.play(Create(baseline), Create(ten), LaggedStart(*[GrowFromCenter(d) for d in dots], lag_ratio=0.2),
                  run_time=1.1)
        self.at("No single measured")
        self.play(FadeOut(covered), FadeOut(results), FadeOut(foot), FadeOut(baseline), FadeOut(ten),
                  FadeOut(dots), FadeOut(q), FadeOut(choices), FadeOut(bright), FadeOut(marker),
                  FadeOut(ruler), stack.animate.scale(1.55).move_to(ORIGIN), run_time=1.2)
        self.finish()


class S09Routes(SpokenScene):
    def construct(self):
        stage = data_stage()
        stack = measured_stack(with_labels=False, compact=True)
        stack.shift(LEFT * 2.4 + UP * 0.1)
        self.add(stage, stack)
        route_motion = flowing_packets([stack.bars[0].get_center(), stack.bars[1].get_center(),
                                        stack.bars[2].get_center(), stack.bars[3].get_center()],
                                       count=8, speed=0.09)
        self.add(route_motion)
        self.at("missing energy did")
        question = T("missing?", 34, GOLD).move_to([3.9, 2.3, 0])
        self.play(FadeIn(question), run_time=0.7)
        self.at("released much as heat")
        heat = VGroup()
        for i, b in enumerate(stack.bars):
            wave = FunctionGraph(lambda x, y=b.get_y(): y + 0.12 * np.sin(5 * x),
                                 x_range=[b.get_right()[0], min(5.7, b.get_right()[0] + 1.35), 0.08],
                                 color=RED, stroke_width=7)
            heat.add(wave)
        self.play(FadeOut(question), LaggedStart(*[Create(h) for h in heat], lag_ratio=0.18), run_time=1.25)
        heat_label = T("heat", 30, RED).move_to([4.9, 2.45, 0])
        self.play(FadeIn(heat_label), run_time=0.55)
        self.at("material and wastes")
        decomp = energy_bar(5060, GREY, -0.55, min_width=2.1, max_width=7.8, height=1.0)
        decomp.move_to([4.55, -0.65, 0])
        dlab = T("Decomposers\n5,060", 28, GREY, line_spacing=0.8).next_to(decomp, DOWN, buff=0.15)
        routes = VGroup(*[DashedLine(b.get_right(), decomp.get_left() + UP * (0.3 - i * 0.18),
                                          color=GREY, stroke_width=4, dash_length=0.15)
                          for i, b in enumerate(stack.bars)])
        self.play(LaggedStart(*[Create(r) for r in routes], lag_ratio=0.18), run_time=1.25)
        self.play(GrowFromCenter(decomp), FadeIn(dlab), run_time=0.85)
        self.at("Decomposers receive")
        side = T("side branch from all levels", 26, GREY).move_to([3.75, 0.25, 0])
        self.play(FadeIn(side), LaggedStart(*[Indicate(r, color=GOLD) for r in routes], lag_ratio=0.18),
                  run_time=1.3)
        self.finish()


class S10Accounting(SpokenScene):
    def construct(self):
        stage = data_stage()
        captured = energy_bar(20810, GREEN, 0, max_width=11.0, height=1.1)
        caplab = T("captured  20,810", 32, GREEN).next_to(captured, UP, buff=0.2)
        self.add(stage, captured, caplab)
        flow = flowing_packets([captured.get_left() + RIGHT * 0.2,
                                captured.get_right() + LEFT * 0.2], count=10, speed=0.1)
        self.add(flow)
        self.at("producer row needs")
        brace = Brace(captured, DOWN, color=GOLD)
        tag = T("energy accounting", 28, GOLD).move_to([0, -2.55, 0])
        self.play(GrowFromCenter(brace), FadeIn(tag), run_time=0.9)
        self.at("counts all captured")
        self.play(Indicate(captured, color=GOLD, scale_factor=1.03), run_time=0.9)
        red_w = 11.0 * 11977 / 20810
        green_w = 11.0 * 8833 / 20810
        red = RoundedRectangle(corner_radius=0.1, width=red_w, height=1.1, color=RED,
                               fill_color=RED, fill_opacity=0.42, stroke_width=4)
        green = RoundedRectangle(corner_radius=0.1, width=green_w, height=1.1, color=GREEN,
                                 fill_color=GREEN, fill_opacity=0.42, stroke_width=4)
        red.layout_ok = green.layout_ok = True
        parts = VGroup(red, green).arrange(RIGHT, buff=0).move_to(captured)
        rlab = T("respiration  11,977", 29, RED).next_to(red, UP, buff=0.2)
        glab = T("new plant material  8,833", 29, GREEN).move_to([3.25, -1.48, 0])
        self.at("Plants used much")
        self.play(ReplacementTransform(captured, parts), FadeOut(caplab), FadeOut(flow), run_time=1.15)
        self.play(FadeIn(rlab), run_time=0.6)
        heat = VGroup(*[ArcBetweenPoints(red.get_bottom() + RIGHT * x,
                                        red.get_bottom() + RIGHT * x + DOWN * 1.15,
                                        angle=0.35, color=RED, stroke_width=6)
                        for x in (-1.7, 0, 1.7)])
        self.play(LaggedStart(*[Create(h) for h in heat], lag_ratio=0.2), run_time=1.0)
        self.at("only part became")
        self.play(FadeIn(glab), Indicate(green, color=GOLD, scale_factor=1.04), run_time=1.0)
        consumers = VGroup(*[energy_bar(v, c, 1.0 + i * 0.55, min_width=0.3,
                                        max_width=green_w, height=0.42)
                             for i, (v, c) in enumerate(zip(VALUES[1:], COLORS[1:]))])
        consumers.align_to(green, LEFT)
        arrows = VGroup(*[Arrow(green.get_top() + LEFT * 1.45, b.get_bottom(), color=GOLD, stroke_width=4, buff=0.05)
                          for b in consumers])
        self.at("That smaller block")
        self.play(LaggedStart(*[GrowFromCenter(b) for b in consumers], lag_ratio=0.2),
                  LaggedStart(*[GrowArrow(a) for a in arrows], lag_ratio=0.2), run_time=1.25)
        self.finish()


class S11Limits(SpokenScene):
    def construct(self):
        stage = data_stage()
        bar = energy_bar(3368, BLUE, -0.6, min_width=8.2, max_width=8.2, height=0.75)
        axis = T("ENERGY FLOW", 34, BLUE).next_to(bar, DOWN, buff=0.28)
        self.add(stage, bar, axis)
        self.add(flowing_packets([bar.get_left() + RIGHT * 0.2, bar.get_right() + LEFT * 0.2],
                                 count=9, speed=0.11))
        self.at("not animal counts")
        head = T("head count", 38, GREY).move_to([0, 1.8, 0])
        head.layout_ok = True  # deliberate crossed-out misconception
        cross = VGroup(Line(head.get_corner(UL), head.get_corner(DR), color=RED, stroke_width=7),
                       Line(head.get_corner(DL), head.get_corner(UR), color=RED, stroke_width=7))
        self.play(FadeIn(head), Create(cross), run_time=0.95)
        self.at("One large organism")
        large = fish(BLUE, 1.75, (-3.0, 0.55, 0))
        many = VGroup(*[fish(BLUE, 0.45, (x, y, 0))
                        for x, y in ((1.8, 1.0), (2.7, 1.0), (3.6, 1.0),
                                     (2.15, 0.3), (3.05, 0.3), (3.95, 0.3))])
        bob(large, amp=0.08, speed=1.2)
        bob(many, amp=0.07, speed=1.35, seed=2)
        self.play(FadeOut(head), FadeOut(cross), FadeIn(large), FadeIn(many), run_time=1.0)
        same = T("same total energy", 30, GOLD).move_to([0, 2.4, 0])
        self.play(FadeIn(same), run_time=0.65)
        self.at("They came from")
        tags = VGroup(chip("one place", GREY, 28), chip("rough estimates", GREY, 28)).arrange(RIGHT, buff=0.5)
        tags.move_to([0, 3.12, 0])
        self.play(FadeOut(same), FadeIn(tags), run_time=0.8)
        self.at("pattern can guide")
        self.play(ReplacementTransform(many, fish(BLUE, 1.75, (3.0, 0.55, 0))), run_time=1.0)
        guide = caption("Pattern guides direction, not an exact population.", color=GOLD)
        self.play(FadeIn(guide), FadeIn(scope_tag("schematic")), run_time=0.8)
        self.finish()


class S12Return(SpokenScene):
    def construct(self):
        world = ecosystem_world("bay")
        self.add(world)
        self.at("Return to the bay")
        title = T("Chesapeake Bay", 34, TEXT).move_to([0, 3.3, 0])
        self.play(FadeIn(title), run_time=0.75)
        pts = [world.plants.get_center(), world.zoo.get_center(), world.small_fish.get_center(), world.bird.get_center()]
        widths = [15, 10, 6]
        arrows = VGroup(*[arrow_between(pts[i], pts[i + 1], GOLD, widths[i]) for i in range(3)])
        self.at("Different feeding steps")
        self.play(LaggedStart(*[GrowArrow(a) for a in arrows], lag_ratio=0.2), run_time=1.3)
        packets = VGroup(*[Dot(p, radius=r, color=GOLD) for p, r in zip(pts, (0.24, 0.17, 0.11, 0.065))])
        self.play(LaggedStart(*[GrowFromCenter(d) for d in packets], lag_ratio=0.17), run_time=1.0)
        self.at("exact width may")
        self.play(LaggedStart(*[a.animate.set_stroke(width=w * 0.72) for a, w in zip(arrows, widths)],
                              lag_ratio=0.18), run_time=1.1)
        self.at("Repeating those losses")
        school = VGroup(*[fish(ORANGE, 0.58, (x, y, 0))
                          for x, y in ((-0.3, 0.55), (0.75, 0.75), (1.75, 0.45),
                                       (0.2, -0.25), (1.25, -0.2), (2.25, -0.45))])
        self.play(FadeIn(school), Indicate(world.bird, color=PURPLE, scale_factor=1.08), run_time=1.2)
        self.finish()


class S13Rule(SpokenScene):
    def construct(self):
        stage = data_stage()
        world = ecosystem_world("bay")
        for mob in world.get_family():
            mob.clear_updaters()
        world.scale(0.46).move_to([-3.2, -0.15, 0])
        stack = measured_stack(with_labels=False, compact=True)
        stack.scale(0.72).move_to([3.3, -0.15, 0])
        self.add(stage, world, stack)
        bay_packets = flowing_packets([[-5.4, -1.5, 0], [-3.5, -0.2, 0], [-1.5, 1.45, 0]],
                                      count=7, speed=0.09, radius=0.065)
        self.add(bay_packets)
        measured_sweep = sweep_line(1.55, 5.15, -1.65, 1.65, speed=0.45)
        self.add(measured_sweep)
        self.at("measurements refine")
        left = T("BAY WEB", 30, BLUE).move_to([-3.45, 3.2, 0])
        right = T("MEASURED SPRING", 30, GREEN).move_to([3.3, 3.2, 0])
        self.play(FadeIn(left), FadeIn(right), run_time=0.75)
        self.at("At each feeding")
        bay_pulse = Arrow([-5.5, -1.6, 0], [-1.5, 1.6, 0], color=GOLD, stroke_width=10,
                          buff=0.1, max_tip_length_to_length_ratio=0.16)
        spring_pulse = Arrow([3.3, -1.65, 0], [3.3, 1.65, 0], color=GOLD, stroke_width=10,
                             buff=0.1, max_tip_length_to_length_ratio=0.16)
        self.play(GrowArrow(bay_pulse), GrowArrow(spring_pulse), run_time=1.15)
        self.at("less energy is")
        self.play(bay_pulse.animate.set_stroke(width=4), spring_pulse.animate.set_stroke(width=4), run_time=1.0)
        self.at("Use the rule")
        direction = chip("RULE → direction", GOLD, 30).move_to([-3.25, -2.85, 0])
        size = chip("DATA → size", TEAL, 30).move_to([3.25, -2.85, 0])
        self.play(FadeIn(direction), FadeIn(size), run_time=0.85)
        self.at("Every step passes")
        rule = fit_text("Every step passes on less energy, but how much less varies.",
                        max_w=11.8, size=38, color=GOLD).move_to([0, 0, 0])
        self.play(FadeOut(world), FadeOut(stack), FadeOut(left), FadeOut(right), FadeOut(bay_pulse),
                  FadeOut(spring_pulse), FadeOut(direction), FadeOut(size), FadeOut(measured_sweep),
                  FadeOut(bay_packets), FadeOut(stage), FadeIn(rule), run_time=1.15)
        self.finish()


class S14End(EndCard):
    LINE = "Every step passes on less energy, but how much less varies."
