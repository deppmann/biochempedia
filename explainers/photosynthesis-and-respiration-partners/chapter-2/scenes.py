from types import SimpleNamespace

from bp_parts import *


# COLOR MAP (identical to the lesson brief / chapter 1):
# photosynthesis GREEN; respiration RED; oxygen and water BLUE;
# light and usable energy YELLOW; carbon dioxide and labels GREY.


def oxygen_model(hour):
    """Schematic oxygen level from a fixed rate difference (not field data)."""
    if hour <= 18:
        return 4.2 + (hour - 6.0) * (3.2 / 12.0)
    return 7.4 - (hour - 18.0) * (2.7 / 12.0)


def _fish(center=(-0.4, -0.25, 0), scale=1.0, color=TEXT):
    body = Ellipse(width=0.85, height=0.42, color=color, stroke_width=3,
                   fill_color=color, fill_opacity=0.08)
    tail = Polygon([-0.40, 0, 0], [-0.72, 0.26, 0], [-0.72, -0.26, 0],
                   color=color, stroke_width=3, fill_opacity=0.06)
    eye = Dot([0.25, 0.08, 0], radius=0.035, color=color)
    return VGroup(tail, body, eye).scale(scale).move_to(center)


def _plant(x, y=-2.32, height=1.25, color=GREEN):
    stems = VGroup()
    for dx, bend in [(-0.23, -0.15), (0, 0.12), (0.23, 0.18)]:
        stem = VMobject(color=color, stroke_width=8)
        stem.set_points_smoothly([
            [x + dx, y, 0], [x + dx + bend * 0.5, y + height * 0.52, 0],
            [x + dx + bend, y + height, 0],
        ])
        stems.add(stem)
    return stems


def _rate_arrow(start, end, color, width=8):
    arrow = Arrow(start, end, buff=0, color=color, stroke_width=width,
                  max_tip_length_to_length_ratio=0.18)
    pulse(arrow, base=width, amp=1.3, speed=2.1)
    return arrow


def creek_world(hour=6.0, oxygen=0.40, light=1.0, photo_rate=0.0,
                resp_rate=0.0, show_gauge=True, show_plot=True,
                show_labels=True, show_question_mark=False):
    """The carried picture. Every continuing creek scene calls this builder."""
    sky = Rectangle(width=13.1, height=2.25, stroke_width=0,
                    fill_color="#182333", fill_opacity=1).move_to([0, 2.45, 0])
    water = Rectangle(width=13.1, height=4.55, stroke_color=BLUE, stroke_width=2,
                      fill_color=BLUE, fill_opacity=0.12).move_to([0, -0.45, 0])
    water._shimmer_t = 0.0

    def shimmer(m, dt):
        m._shimmer_t += dt
        m.set_fill(opacity=0.12 + 0.035 * np.sin(1.35 * m._shimmer_t))
    water.add_updater(shimmer)
    bed = Polygon([-6.55, -2.25, 0], [-3.2, -2.38, 0], [0.2, -2.24, 0],
                  [3.1, -2.42, 0], [6.55, -2.26, 0], [6.55, -2.70, 0],
                  [-6.55, -2.70, 0], color=GREY, stroke_width=3,
                  fill_color=GREY, fill_opacity=0.20)
    habitat = VGroup(sky, water, bed)

    plants = VGroup(_plant(-4.8), _plant(-3.55, height=1.0),
                    _plant(-2.35, height=1.35))
    algae = VGroup(*[
        Circle(radius=0.18 + 0.04 * (i % 2), color=GREEN, stroke_width=3,
               fill_color=GREEN, fill_opacity=0.20).move_to([-5.3 + 0.43 * i, -1.03 + 0.15 * (i % 2), 0])
        for i in range(5)
    ])
    producers = VGroup(plants, algae)
    fish = VGroup(_fish((0.0, -0.25, 0), 1.0), _fish((1.5, -1.25, 0), 0.72))
    bob(fish[0], amp=0.06, speed=1.2)
    bob(fish[1], amp=0.045, speed=1.45, seed=2)
    animals = VGroup(fish, Dot([0.7, -0.72, 0], radius=0.13, color=TEXT),
                     Dot([2.2, -0.60, 0], radius=0.10, color=TEXT))
    microbes = VGroup(*[
        Dot([-1.7 + 0.58 * i, -1.72 + 0.16 * (i % 2), 0], radius=0.055, color=GREY)
        for i in range(8)
    ])
    organisms = VGroup(producers, animals, microbes)

    particles = VGroup(*[
        Dot([-5.8 + 0.70 * i, -1.75 + 0.44 * (i % 6), 0], radius=0.035, color=BLUE)
        .set_opacity(0.40) for i in range(16)
    ])
    for i, dot in enumerate(particles):
        dot.v = 0.07 + 0.012 * (i % 4)

        def drift(m, dt):
            m.shift(RIGHT * m.v * dt)
            if m.get_x() > 6.2:
                m.shift(LEFT * 12.0)
        dot.add_updater(drift)
    currents = VGroup(*[
        Line([-5.8 + 1.75 * (i % 5), -1.95 + 0.48 * (i % 5), 0],
             [-4.9 + 1.75 * (i % 5), -1.95 + 0.48 * (i % 5), 0],
             color=BLUE, stroke_width=5).set_opacity(0.32)
        for i in range(10)
    ])
    for i, current in enumerate(currents):
        current.v = 0.30 + 0.05 * (i % 3)

        def flow(m, dt):
            m.shift(RIGHT * m.v * dt)
            if m.get_left()[0] > 3.7:
                m.shift(LEFT * 9.5)
        current.add_updater(flow)
    particles.add(currents)

    sun = Circle(radius=0.34, color=YELLOW, stroke_width=4,
                 fill_color=YELLOW, fill_opacity=0.20 + 0.45 * light).move_to([-5.65, 2.68, 0])
    rays = VGroup(*[
        Line(sun.get_center() + [0.16 * (i - 2), -0.28, 0],
             [-4.9 + 0.72 * i, -0.82, 0], color=YELLOW,
             stroke_width=3 + 3 * light).set_opacity(light)
        for i in range(5)
    ])
    lighting = VGroup(sun, rays)

    time_x0, time_x1, time_y = -4.45, 3.25, 3.20
    day = Line([time_x0, time_y, 0], [0.0, time_y, 0], color=YELLOW, stroke_width=12)
    night = Line([0.0, time_y, 0], [time_x1, time_y, 0], color="#42506A", stroke_width=12)
    dawn = T("sunrise", 24, YELLOW).next_to([time_x0, time_y, 0], DOWN, buff=0.10)
    dusk = T("sunset", 24, GREY).next_to([0.0, time_y, 0], DOWN, buff=0.10)
    marker_x = interpolate(time_x0, time_x1, np.clip((hour - 6.0) / 24.0, 0, 1))
    marker = Triangle(color=TEXT, fill_color=TEXT, fill_opacity=1).scale(0.10)
    marker.rotate(PI).move_to([marker_x, time_y + 0.20, 0])
    timeline = VGroup(day, night, dawn, dusk, marker)

    level = ValueTracker(oxygen)
    gauge = dial(level, center=[5.25, 0.25, 0], radius=1.08,
                 label="dissolved oxygen", color=BLUE, fmt="{:.0f}%", scale=100, size=32)
    gauge_label = gauge[-1] if show_gauge else VGroup()
    if show_gauge:
        gauge_label.shift(LEFT * 0.35)  # keeps the label inside the water panel border
    if hasattr(gauge_label, "layout_ok"):
        gauge_label.layout_ok = True

    plot = Plot(box=(-4.45, 3.25, 2.00, 2.72), xr=(6, 30), yr=(3.5, 8.0),
                xticks=[], yticks=[], color=GREY, stroke=2)
    plot_curve = plot.curve(oxygen_model, 6, hour, color=BLUE, width=6)
    plot_tag = T("schematic oxygen", 24, BLUE).move_to([-2.3, 1.12, 0])
    plot_tag.layout_ok = True  # Deliberately over background water, not a data mark.
    oxygen_plot = VGroup(plot, plot_curve, plot_tag)

    photo = _rate_arrow([1.45, 0.78, 0], [3.55, 0.78, 0], GREEN,
                        width=max(3, 4 + 12 * photo_rate))
    resp = _rate_arrow([3.55, 0.05, 0], [1.45, 0.05, 0], RED,
                       width=max(3, 4 + 12 * resp_rate))
    photo_label = T("addition: off" if photo_rate <= 0 else "addition", 28, GREEN).next_to(photo, UP, buff=0.10)
    resp_label = T("use", 28, RED).next_to(resp, DOWN, buff=0.10)
    rates = VGroup(photo, resp)
    if show_labels:
        rates.add(photo_label, resp_label)

    qmark = T("?", 54, GREY).move_to([3.80, 2.00, 0])
    qmark.layout_ok = True  # Intentionally in open sky beyond the schematic curve.

    group = VGroup(habitat, particles, organisms, lighting, timeline)
    if show_plot:
        group.add(oxygen_plot)
    if show_gauge:
        group.add(gauge)
    if photo_rate > 0 or resp_rate > 0:
        group.add(rates)
    if show_question_mark:
        group.add(qmark)

    return SimpleNamespace(group=group, habitat=habitat, particles=particles,
                           organisms=organisms, producers=producers, animals=animals,
                           microbes=microbes, lighting=lighting, sun=sun, rays=rays,
                           timeline=timeline, marker=marker, gauge=gauge, level=level,
                           oxygen_plot=oxygen_plot, plot=plot, plot_curve=plot_curve,
                           rates=rates, photo=photo, resp=resp, qmark=qmark)


def oxygen_bubbles():
    bubbles = VGroup(*[
        Circle(radius=0.07 + 0.015 * (i % 3), color=BLUE, stroke_width=3)
        .move_to([-4.7 + 0.48 * i, -1.15 + 0.20 * (i % 2), 0])
        for i in range(8)
    ])
    return bubbles


def energy_marks(world):
    marks = VGroup()
    for p in [(-4.2, -1.45, 0), (-2.8, -1.35, 0), (0.0, -0.25, 0),
              (1.5, -1.25, 0), (-0.1, -1.70, 0)]:
        marks.add(Star(5, outer_radius=0.13, inner_radius=0.06, color=YELLOW,
                       fill_color=YELLOW, fill_opacity=0.75).move_to(p))
    return marks


def tub_picture(level=0.55, tap_on=True):
    basin = RoundedRectangle(corner_radius=0.25, width=6.3, height=3.15,
                             stroke_color=BLUE, stroke_width=7).move_to([0, -0.35, 0])
    water_h = max(0.15, 2.55 * level)
    water = Rectangle(width=5.72, height=water_h, stroke_width=0,
                      fill_color=BLUE, fill_opacity=0.30)
    water.move_to([0, basin.get_bottom()[1] + 0.30 + water_h / 2, 0])
    water._shimmer_t = 0.0

    def shimmer(m, dt):
        m._shimmer_t += dt
        m.set_fill(opacity=0.30 + 0.06 * np.sin(1.5 * m._shimmer_t))
    water.add_updater(shimmer)
    spout = VGroup(Line([-3.8, 2.2, 0], [-2.7, 2.2, 0], color=GREEN, stroke_width=12),
                   Line([-2.7, 2.2, 0], [-2.7, 1.45, 0], color=GREEN, stroke_width=12))
    stream = Line([-2.7, 1.42, 0], [-2.7, 0.6, 0], color=GREEN,
                  stroke_width=12 if tap_on else 2).set_opacity(1 if tap_on else 0.2)
    drain = Circle(radius=0.25, color=RED, stroke_width=7).move_to([2.0, -1.58, 0])
    drain_arrow = _rate_arrow([2.0, -1.15, 0], [2.0, -2.4, 0], RED, 9)
    light_link = VGroup(Circle(radius=0.28, color=YELLOW, fill_color=YELLOW,
                              fill_opacity=0.30).move_to([-4.5, 2.2, 0]),
                        Line([-4.15, 2.2, 0], [-3.85, 2.2, 0], color=YELLOW, stroke_width=4))
    labels = VGroup(T("photosynthesis", 28, GREEN).move_to([-2.7, 2.72, 0]),
                    T("respiration", 28, RED).move_to([2.0, -2.72, 0]))
    return VGroup(basin, water, spout, stream, drain, drain_arrow, light_link, labels)


def tub_motion():
    bubbles = VGroup(*[
        Circle(radius=0.07 + 0.015 * (i % 2), color=BLUE, stroke_width=3)
        .move_to([-2.0 + 0.8 * i, -1.25 + 0.30 * (i % 3), 0])
        for i in range(6)
    ])
    for i, bubble in enumerate(bubbles):
        bubble.v = 0.16 + 0.03 * (i % 3)

        def rise(m, dt):
            m.shift(UP * m.v * dt)
            if m.get_y() > 0.95:
                m.shift(DOWN * 2.15)
        bubble.add_updater(rise)
    return bubbles


class S00Hook(SpokenScene):
    def construct(self):
        cell = Ellipse(width=8.6, height=5.5, color=GREEN, stroke_width=6,
                       fill_color=GREEN, fill_opacity=0.07)
        photo = _rate_arrow([-2.9, 0.65, 0], [1.6, 0.65, 0], GREEN, 13)
        resp = _rate_arrow([1.6, -0.65, 0], [-2.9, -0.65, 0], RED, 9)
        oxygen = VGroup(*[Circle(radius=0.11, color=BLUE, stroke_width=4)
                          .move_to([-1.8 + i * 0.62, 1.55 + 0.12 * (i % 2), 0]) for i in range(7)])
        cell_world = VGroup(cell, photo, resp, oxygen)
        self.play(FadeIn(cell), run_time=0.7)
        self.at("oxygen rose by day")
        self.play(LaggedStart(*[FadeIn(b, shift=UP * 0.2) for b in oxygen], lag_ratio=0.12), run_time=1.0)
        self.at("fell at night")
        self.play(oxygen.animate.shift(DOWN * 0.85), run_time=0.8)
        q = T("Why?", 52, YELLOW).move_to([4.7, 2.6, 0])
        self.at("why")
        self.play(FadeIn(q, scale=0.8), run_time=0.5)
        self.at("whole creek")
        world = creek_world(hour=8, oxygen=0.48, light=1.0, show_gauge=False,
                            show_plot=False, show_labels=False)
        self.play(FadeOut(cell_world, scale=0.55), FadeOut(q),
                  FadeIn(world.group), run_time=1.5)
        self.at("two jobs")
        labels = VGroup(T("photosynthesis", 30, GREEN), T("respiration", 30, RED)).arrange(RIGHT, buff=0.8)
        labels.move_to([0, 1.7, 0])
        for label in labels:
            label.layout_ok = True  # Deliberately over the open-water background.
        self.play(FadeIn(labels, shift=DOWN * 0.15), run_time=0.7)
        self.at("view pulls back")
        self.play(FadeOut(labels), world.group.animate.scale(0.94), run_time=1.0)
        self.finish()


class S01Title(NarratedScene):
    def construct(self):
        world = creek_world(hour=8, oxygen=0.48, light=1.0, show_gauge=False,
                            show_plot=False, show_labels=False)
        title = fit_text("Why Creek Oxygen Rises and Falls", max_w=11.7, size=50,
                         color=TEXT, font=TITLE_FONT)
        title.move_to([0, 1.9, 0])
        title.layout_ok = True  # Deliberately over the creek background for this title beat.
        world.rays.set_opacity(0)  # keep sun rays from crossing the title text
        self.add(world.group)
        self.play(FadeIn(title, shift=UP * 0.15), run_time=0.45)
        self.wait(1.05)
        small = T("creek oxygen", 24, TEXT).move_to([4.7, 3.20, 0])
        self.play(Transform(title, small), run_time=0.45)
        self.finish()


class S02CreekWorld(SpokenScene):
    def construct(self):
        world = creek_world(hour=6, oxygen=0.40, light=1.0, show_gauge=False,
                            show_plot=False, show_labels=False)
        self.play(FadeIn(world.habitat), run_time=0.6)
        self.at("green algae")
        self.play(LaggedStart(FadeIn(world.producers[1]), FadeIn(world.producers[0]), lag_ratio=0.3), run_time=1.0)
        self.at("fish tiny animals")
        self.play(FadeIn(world.animals), run_time=0.7)
        self.at("microbes drift")
        self.play(FadeIn(world.microbes), FadeIn(world.particles), run_time=0.7)
        self.at("blue gauge tracks")
        self.play(FadeIn(world.gauge), run_time=0.8)
        dissolved = T("oxygen mixed into water", 28, BLUE).move_to([3.8, -2.05, 0])
        self.at("oxygen gas mixed")
        self.play(FadeIn(dissolved, shift=UP * 0.12), run_time=0.6)
        self.at("time bar begins")
        self.play(FadeIn(world.timeline), FadeOut(dissolved), run_time=0.8)
        self.add(scope_tag("schematic"))
        self.finish()


class S03TwoRates(SpokenScene):
    def construct(self):
        world = creek_world(hour=9, oxygen=0.48, light=0.0, show_gauge=True,
                            show_plot=False, show_labels=False)
        self.add(world.habitat, world.particles, world.organisms, world.timeline, world.gauge)
        self.at("yellow sunlight reaches")
        self.play(FadeIn(world.sun), LaggedStart(*[Create(r) for r in world.rays], lag_ratio=0.12), run_time=1.1)
        prod_label = T("producers", 30, GREEN).move_to([-4.0, 0.42, 0])
        self.at("these producers")
        self.play(FadeIn(prod_label, shift=DOWN * 0.15), run_time=0.6)
        green_arrows = VGroup(*[_rate_arrow([-4.9 + i * 0.65, -1.0, 0],
                                             [-4.9 + i * 0.65, -0.25, 0], GREEN, 7)
                                for i in range(5)])
        self.at("photosynthesis sends")
        self.play(LaggedStart(*[GrowArrow(a) for a in green_arrows], lag_ratio=0.12), run_time=0.9)
        bubbles = oxygen_bubbles()
        self.at("blue oxygen bubbles")
        self.play(LaggedStart(*[FadeIn(b, shift=UP * 0.35) for b in bubbles], lag_ratio=0.10), run_time=1.0)
        red_arrows = VGroup(_rate_arrow([-1.0, -0.15, 0], [-3.0, -1.2, 0], RED, 7),
                            _rate_arrow([2.8, -0.55, 0], [1.1, -0.35, 0], RED, 7),
                            _rate_arrow([0.0, -1.45, 0], [-0.6, -1.72, 0], RED, 7))
        self.at("at the same time")
        self.play(LaggedStart(*[GrowArrow(a) for a in red_arrows], lag_ratio=0.18), run_time=1.0)
        self.at("both processes")
        self.play(Indicate(green_arrows, color=GREEN), Indicate(red_arrows, color=RED), run_time=1.0)
        self.finish()


class S04DayRise(SpokenScene):
    def construct(self):
        world = creek_world(hour=9, oxygen=0.46, light=1.0, photo_rate=0.25,
                            resp_rate=0.20, show_gauge=True, show_plot=True, show_labels=True)
        self.add(world.group)
        self.at("watch the arrows")
        self.play(Indicate(world.photo, color=GREEN), Indicate(world.resp, color=RED), run_time=0.8)
        rate_label = T("rate = how fast", 26, TEXT).move_to([0.4, 1.42, 0])
        self.at("a rate tells")
        self.play(FadeIn(rate_label, shift=DOWN * 0.12), run_time=0.6)
        wide = _rate_arrow([1.45, 0.78, 0], [3.55, 0.78, 0], GREEN, 17)
        wide_label = T("addition", 28, GREEN).next_to(wide, UP, buff=0.10).shift(RIGHT * 0.30)
        self.at("photosynthesis arrow grows wider")
        self.play(ReplacementTransform(world.photo, wide),
                  ReplacementTransform(world.rates[2], wide_label), FadeOut(rate_label), run_time=0.9)
        self.at("oxygen enters the water faster")
        flow = VGroup(*[Circle(radius=0.08, color=BLUE, stroke_width=3)
                        .move_to([-0.8 + i * 0.42, 1.15, 0]) for i in range(7)])
        self.play(LaggedStart(*[FadeIn(b, shift=RIGHT * 0.2) for b in flow], lag_ratio=0.1), run_time=0.9)
        self.at("blue gauge climbs")
        self.play(world.level.animate.set_value(0.74), run_time=1.6, rate_func=smooth)
        self.at("schematic line rises")
        later = world.plot.curve(oxygen_model, 6, 16, color=BLUE, width=6)
        self.play(ReplacementTransform(world.plot_curve, later), run_time=1.5)
        self.finish()


class S05PlantsRespire(SpokenScene):
    def construct(self):
        world = creek_world(hour=14, oxygen=0.67, light=1.0, photo_rate=0.72,
                            resp_rate=0.42, show_gauge=True, show_plot=True, show_labels=True)
        self.add(world.group)
        resp_side = RoundedRectangle(corner_radius=0.2, width=5.1, height=1.70,
                                     stroke_color=RED, stroke_width=3).move_to([0.0, -1.00, 0])
        self.at("grass and algae appear")
        mini_plants = world.producers.copy().scale(0.38).move_to([-0.9, -1.00, 0])
        mini_animals = world.animals.copy().scale(0.46).move_to([0.9, -1.00, 0])
        self.play(FadeOut(world.rates), Create(resp_side), TransformFromCopy(world.producers, mini_plants),
                  TransformFromCopy(world.animals, mini_animals), run_time=1.0)
        resp_head = T("respiration", 30, RED).next_to(resp_side, UP, buff=0.12)
        self.at("respiration side")
        self.play(FadeIn(resp_head), run_time=0.5)
        self.at("do not stop respiring")
        self.play(Indicate(mini_plants, color=RED), run_time=0.9)
        marks = energy_marks(world)
        self.at("usable energy")
        self.play(LaggedStart(*[FadeIn(m, scale=0.4) for m in marks], lag_ratio=0.15), run_time=1.0)
        self.at("during daylight")
        self.play(FadeOut(resp_side), FadeOut(resp_head), FadeOut(mini_plants),
                  FadeOut(mini_animals), FadeIn(world.rates), run_time=0.7)
        self.at("which rate is faster")
        self.play(Indicate(world.photo, color=GREEN), Indicate(world.resp, color=RED), run_time=1.1)
        self.finish()


class S06PredictSunset(SpokenScene):
    def construct(self):
        world = creek_world(hour=17, oxygen=0.74, light=1.0, photo_rate=0.65,
                            resp_rate=0.40, show_gauge=True, show_plot=True, show_labels=True)
        self.add(world.group)
        sunset_marker = Triangle(color=TEXT, fill_color=TEXT, fill_opacity=1).scale(0.10)
        sunset_marker.rotate(PI).move_to([0.0, 3.40, 0])
        self.at("time bar reaches sunset")
        sunset_curve = world.plot.curve(oxygen_model, 6, 18, color=BLUE, width=6)
        self.play(Transform(world.marker, sunset_marker),
                  Transform(world.plot_curve, sunset_curve), run_time=1.2)
        self.at("yellow light fades")
        self.play(world.rays.animate.set_opacity(0), world.sun.animate.set_fill(opacity=0.20), run_time=1.0)
        zero = _rate_arrow([1.45, 0.78, 0], [3.55, 0.78, 0], GREEN, 3).set_opacity(0.18)
        zero_label = T("addition: off", 28, GREEN).next_to(zero, UP, buff=0.10)
        self.at("photosynthesis stops adding")
        self.play(ReplacementTransform(world.photo, zero),
                  ReplacementTransform(world.rates[2], zero_label), run_time=0.9)
        self.at("respiration keeps using")
        self.play(Indicate(world.resp, color=RED), run_time=0.8)
        q = question_card("What should the blue line do next?", y=-3.18, max_w=9.8)
        self.at("what should the blue line")
        self.play(FadeIn(q.question, shift=UP * 0.12), run_time=0.7)
        self.finish()


class S07Pause(PredictPause):
    QUESTION = "What should the blue line do next?"
    SECONDS = 4.5
    CARD = {"y": -3.18, "max_w": 9.8}

    def backdrop(self):
        world = creek_world(hour=18, oxygen=0.74, light=0.0, photo_rate=0.0,
                            resp_rate=0.40, show_gauge=True, show_plot=True, show_labels=True)
        return world.group


class S08NightFall(SpokenScene):
    def construct(self):
        world = creek_world(hour=18, oxygen=0.74, light=0.0, photo_rate=0.0,
                            resp_rate=0.42, show_gauge=True, show_plot=True, show_labels=True)
        self.add(world.group)
        self.at("line bends downward")
        night_curve = world.plot.curve(oxygen_model, 6, 27, color=BLUE, width=6)
        self.play(ReplacementTransform(world.plot_curve, night_curve), run_time=2.0)
        self.at("keep respiring in darkness")
        self.play(Indicate(world.animals, color=RED), Indicate(world.producers, color=RED),
                  Indicate(world.microbes, color=RED), run_time=1.0)
        self.at("oxygen gauge falls")
        self.play(world.level.animate.set_value(0.44), run_time=1.8, rate_func=smooth)
        self.at("photosynthesis no longer replaces")
        self.play(Indicate(world.resp, color=RED), run_time=0.9)
        rule = caption("Light: oxygen added    •    Day and night: oxygen used", size=28)
        self.at("photosynthesis adds oxygen")
        self.play(FadeIn(rule, shift=UP * 0.10), run_time=0.8)
        self.at("respiration uses oxygen")
        self.play(Indicate(world.resp, color=RED), run_time=0.8)
        sunrise = VGroup(Circle(radius=0.28, color=YELLOW, fill_color=YELLOW,
                                fill_opacity=0.32).move_to([3.2, 2.55, 0]),
                         _rate_arrow([2.7, 0.75, 0], [3.8, 0.75, 0], GREEN, 5))
        self.at("at sunrise")
        self.play(FadeOut(rule), FadeIn(sunrise, shift=UP * 0.12), run_time=1.0)
        self.finish()


class S09TubModel(SpokenScene):
    def construct(self):
        world = creek_world(hour=14, oxygen=0.65, light=1.0, photo_rate=0.68,
                            resp_rate=0.40, show_gauge=True, show_plot=False, show_labels=True)
        self.add(world.group)
        tub = tub_picture(0.58, tap_on=True)
        motion = tub_motion()
        self.at("transform the creek gauge")
        self.play(FadeOut(VGroup(world.habitat, world.particles, world.organisms,
                                 world.lighting, world.timeline, world.rates)),
                  ReplacementTransform(world.gauge, tub), FadeIn(motion), run_time=1.5)
        self.at("photosynthesis is a tap")
        self.play(Indicate(tub[2], color=GREEN), Indicate(tub[6], color=YELLOW), run_time=0.9)
        self.at("respiration is a drain")
        self.play(Indicate(tub[4], color=RED), Indicate(tub[5], color=RED), run_time=0.9)
        high = tub_picture(0.83, tap_on=True)
        self.at("tap outruns the drain")
        self.play(Transform(tub, high), run_time=1.7)
        low = tub_picture(0.34, tap_on=False)
        self.at("tap off")
        self.play(Transform(tub, low), run_time=1.7)
        self.finish()


class S10CompareRates(SpokenScene):
    def construct(self):
        tub = tub_picture(0.50, tap_on=True)
        motion = tub_motion()
        self.add(tub, motion)
        equal = creek_world(hour=12, oxygen=0.56, light=1.0, photo_rate=0.45,
                            resp_rate=0.45, show_gauge=True, show_plot=False, show_labels=True)
        self.at("back into the creek")
        self.play(FadeOut(tub, scale=0.72), FadeOut(motion),
                  FadeIn(equal.group), run_time=1.5)
        self.at("both rate arrows equal")
        self.play(Indicate(equal.photo, color=GREEN), Indicate(equal.resp, color=RED), run_time=1.0)
        hold = T("steady", 30, BLUE).move_to([5.25, 1.68, 0])
        hold.layout_ok = True  # Deliberately over the open-water background above the gauge.
        self.at("gauge holds steady")
        self.play(FadeIn(hold), run_time=0.6)
        rise = creek_world(hour=14, oxygen=0.72, light=1.0, photo_rate=0.78,
                           resp_rate=0.38, show_gauge=True, show_plot=False, show_labels=True)
        self.at("widen photosynthesis")
        self.play(Transform(equal.rates, rise.rates), FadeOut(hold), run_time=0.9)
        self.at("gauge rises")
        self.play(equal.level.animate.set_value(0.72), run_time=1.2)
        fall = creek_world(hour=16, oxygen=0.38, light=1.0, photo_rate=0.28,
                           resp_rate=0.78, show_gauge=True, show_plot=False, show_labels=True)
        self.at("widen respiration")
        self.play(Transform(equal.rates, fall.rates), run_time=0.9)
        self.at("it falls")
        self.play(equal.level.animate.set_value(0.38), run_time=1.2)
        difference = caption("oxygen change = addition − use", size=30, color=BLUE)
        self.at("difference between the rates")
        self.play(FadeIn(difference, shift=UP * 0.12), run_time=0.8)
        self.finish()


class S11ModelLimit(SpokenScene):
    def construct(self):
        world = creek_world(hour=30, oxygen=0.47, light=0.10, photo_rate=0.18,
                            resp_rate=0.48, show_gauge=True, show_plot=True,
                            show_labels=True, show_question_mark=True)
        self.add(world.group)
        model = T("model", 30, BLUE).move_to([0.2, 1.53, 0])
        self.at("smooth line is a model")
        self.play(FadeIn(model, shift=DOWN * 0.12), Indicate(world.plot_curve, color=BLUE), run_time=0.9)
        sensor = VGroup(DashedLine([2.55, 2.05, 0], [3.65, 2.65, 0], color=GREY,
                                   dash_length=0.12), world.qmark)
        self.at("real sensor may not")
        self.play(FadeIn(sensor), run_time=0.8)
        self.at("which process pushes oxygen up")
        self.play(Indicate(world.photo, color=GREEN), run_time=0.9)
        self.at("or down")
        self.play(Indicate(world.resp, color=RED), run_time=0.9)
        other = T("other causes", 30, GREY).move_to([5.05, 2.00, 0])
        other.layout_ok = True  # Deliberately over open sky beyond the schematic curve.
        self.at("other causes separately")
        self.play(Transform(world.qmark, other), run_time=0.8)
        self.finish()


class S12Rule(SpokenScene):
    def construct(self):
        world = creek_world(hour=15, oxygen=0.66, light=1.0, photo_rate=0.68,
                            resp_rate=0.42, show_gauge=True, show_plot=True,
                            show_labels=True, show_question_mark=True)
        self.add(world.group)
        self.at("compare the green addition")
        self.play(Indicate(world.photo, color=GREEN), run_time=0.7)
        self.at("with the red use")
        self.play(Indicate(world.resp, color=RED), run_time=0.7)
        self.at("before judging the line")
        self.play(Indicate(world.plot_curve, color=BLUE), run_time=0.8)
        self.at("in light")
        self.play(Indicate(VGroup(world.photo, world.resp)), run_time=0.9)
        off = world.photo.copy().set_opacity(0.15)
        off_label = T("addition: off", 28, GREEN).move_to(world.rates[2])
        self.at("in darkness")
        self.play(world.rays.animate.set_opacity(0), Transform(world.photo, off),
                  Transform(world.rates[2], off_label), run_time=1.0)
        end_line = T("Photosynthesis adds oxygen in light;\nrespiration uses oxygen day and night.",
                     44, TEXT, font=TITLE_FONT, line_spacing=0.9)
        self.at("use continues")
        self.play(FadeOut(world.group), FadeIn(end_line), run_time=1.2)
        self.finish()


class S13End(EndCard):
    LINE = "Photosynthesis adds oxygen in light; respiration uses oxygen day and night."
