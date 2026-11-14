"""One Tube, One Shared Supply — competition and cooperation, film 1.

COLOR MAP
  GOLD = limited food/resource
  TEAL = P. aurelia
  CORAL = P. caudatum / living threats
  GREEN = cooperation
  BLUE = abiotic factor
  GREY = glass, axes, and neutral structure

The eight plotted values for each series are copied from the lesson's Gause table.  Lines between
points are only guides to the eye; no fitted or invented values are presented as measurements.
"""
import numpy as np
from bp_parts import *  # noqa: F401,F403


CORAL = "#F27D6D"
TEAL_C = TEAL
DAYS = np.array([0, 2, 4, 6, 8, 12, 16, 25], dtype=float)
A_ALONE = np.array([2, 14, 56, 189, 330, 610, 560, 510], dtype=float)
C_ALONE = np.array([2, 10, 11, 56, 137, 199, 179, 180], dtype=float)
A_SHARED = np.array([2, 10, 58, 202, 221, 302, 363, 350], dtype=float)
C_SHARED = np.array([2, 10, 29, 88, 124, 83, 55, 20], dtype=float)


def glass_tube(cx=0, cy=-0.1, w=5.2, h=5.4, color=GREY):
    """The film's carried glass outline, always rebuilt with the same geometry."""
    return RoundedRectangle(
        corner_radius=0.34, width=w, height=h, stroke_color=color, stroke_width=4,
        fill_color=BLUE, fill_opacity=0.16,
    ).move_to([cx, cy, 0])


def float_motion(mob, amp=0.13, speed=1.0, direction=UP, phase=0.0):
    """Small additive swim/drift motion that remains compatible with later transforms."""
    mob._float_phase = phase

    def update(m, dt):
        old = np.sin(m._float_phase)
        m._float_phase += speed * dt
        m.shift(direction * amp * (np.sin(m._float_phase) - old))
    return mob.add_updater(update)


def swimmer(point, color, scale=1.0, angle=0.0):
    """A labelled-cartoon-free paramecium silhouette with beating edge marks."""
    body = Ellipse(
        width=0.78 * scale, height=0.42 * scale, stroke_color=color, stroke_width=3,
        fill_color=color, fill_opacity=0.48,
    )
    hairs = VGroup()
    for a in np.linspace(-1.05, 1.05, 5):
        p = np.array([0.31 * np.cos(a), 0.17 * np.sin(a), 0]) * scale
        q = p + np.array([0.09 * np.cos(a), 0.09 * np.sin(a), 0]) * scale
        hairs.add(Line(p, q, color=color, stroke_width=2))
    return VGroup(body, hairs).rotate(angle).move_to([point[0], point[1], 0])


def swimmer_group(points, color, seed=1, scale=1.0):
    rng = np.random.default_rng(seed)
    return VGroup(*[swimmer(p, color, scale, rng.uniform(-0.45, 0.45)) for p in points])


def food_group(points, radius=0.095):
    return VGroup(*[Dot([x, y, 0], radius=radius, color=GOLD) for x, y in points])


def pair_world():
    """Two separate tubes used by s00 and s02, at exactly the same scale and position."""
    tubes = VGroup(glass_tube(-3.35), glass_tube(3.35))
    left_pts = [(-4.45, 1.55), (-2.8, 1.05), (-4.1, 0.05), (-2.55, -0.45), (-4.35, -1.45), (-2.7, -1.75)]
    right_pts = [(2.3, 1.45), (4.05, 1.1), (2.65, 0.15), (4.35, -0.4), (2.3, -1.35), (4.0, -1.7)]
    teal = swimmer_group(left_pts, TEAL_C, seed=3, scale=1.05)
    coral = swimmer_group(right_pts, CORAL, seed=5, scale=1.05)
    food_l = food_group([(-4.65, 2.1), (-3.5, 1.75), (-2.3, 2.15), (-3.9, 0.65), (-2.55, -0.9), (-4.5, -2.05)])
    food_r = food_group([(2.1, 2.05), (3.25, 1.75), (4.55, 2.1), (3.8, 0.55), (2.35, -0.75), (4.45, -2.0)])
    return tubes, teal, coral, VGroup(food_l, food_r)


def shared_world(cx=0, w=11.6, h=5.35, opacity=1.0):
    """The single shared tube, reused from competition through the model-limits scene."""
    tube = glass_tube(cx, -0.15, w, h)
    half = w / 2
    a_pts = [(cx + f * half, y) for f, y in [(-0.76, 1.45), (-0.50, 0.55), (-0.25, 1.7), (-0.68, -0.55), (-0.35, -1.65)]]
    c_pts = [(cx + f * half, y) for f, y in [(0.23, 1.35), (0.52, 0.45), (0.76, 1.65), (0.33, -0.75), (0.65, -1.6)]]
    food_pts = [(cx + f * half, y) for f, y in [(-0.83, 2.15), (-0.58, 1.95), (-0.13, 2.15), (0.07, 1.05),
                                                     (0.39, 2.05), (0.82, 1.95), (-0.79, -1.9), (-0.06, -1.65), (0.77, -1.95)]]
    teal = swimmer_group(a_pts, TEAL_C, seed=7, scale=1.08)
    coral = swimmer_group(c_pts, CORAL, seed=11, scale=1.08)
    food = food_group(food_pts, radius=0.105)
    world = VGroup(tube, food, teal, coral)
    if opacity < 1.0:
        tube.set_stroke(opacity=opacity).set_fill(BLUE, opacity=0.16 * opacity)
        food.set_opacity(opacity)
        teal.set_opacity(opacity)
        coral.set_opacity(opacity)
    world.tube, world.food, world.teal, world.coral = tube, food, teal, coral
    return world


def predict_world():
    """Shared tube plus the two empty axes, identical in s04 and the silent pause."""
    world = shared_world(cx=-3.85, w=5.15, h=5.15)
    top = Plot(box=(0.25, 6.05, 0.25, 2.45), xr=(0, 25), yr=(0, 650),
               xticks=[], yticks=[(0, "0"), (300, "300"), (600, "600")], ylabel="aurelia", color=TEAL_C)
    bot = Plot(box=(0.25, 6.05, -2.45, -0.25), xr=(0, 25), yr=(0, 220),
               xticks=[0, 8, 16, 25], yticks=[(0, "0"), (100, "100"), (200, "200")],
               xlabel="day", ylabel="caudatum", color=CORAL)
    return VGroup(world, top, bot)


def interp(values):
    return lambda day: float(np.interp(day, DAYS, values))


def measured_dots(plot, values, color):
    return VGroup(*[Dot(plot.pt(d, v), radius=0.085, color=color) for d, v in zip(DAYS, values)])


def data_plots(include_alone=False, dim_world=True):
    """Two large plots built from the lesson table; used by s06 and s07."""
    backdrop = shared_world(opacity=0.24 if dim_world else 0.0)
    top = Plot(box=(-5.65, 5.8, 0.38, 2.62), xr=(0, 25), yr=(0, 650),
               xticks=[], yticks=[(0, "0"), (300, "300"), (600, "600")], ylabel="P. aurelia", color=GREY)
    bot = Plot(box=(-5.65, 5.8, -2.48, -0.24), xr=(0, 25), yr=(0, 220),
               xticks=[0, 8, 16, 25], yticks=[(0, "0"), (100, "100"), (200, "200")],
               xlabel="day", ylabel="P. caudatum", color=GREY)
    shared = VGroup(
        top.curve(interp(A_SHARED), color=TEAL_C, width=6), measured_dots(top, A_SHARED, TEAL_C),
        bot.curve(interp(C_SHARED), color=CORAL, width=6), measured_dots(bot, C_SHARED, CORAL),
    )
    result = VGroup(backdrop, top, bot, shared)
    result.top, result.bot, result.shared = top, bot, shared
    if include_alone:
        alone = VGroup(
            top.curve(interp(A_ALONE), color=TEAL_C, width=3, opacity=0.42), measured_dots(top, A_ALONE, TEAL_C).set_opacity(0.42),
            bot.curve(interp(C_ALONE), color=CORAL, width=3, opacity=0.42), measured_dots(bot, C_ALONE, CORAL).set_opacity(0.42),
        )
        result.add(alone)
        result.alone = alone
    return result


def fraction_panel():
    """Day-25 count bars and remaining fractions for the fair within-species comparison."""
    panels = TwoPanel("P. aurelia · day 25", "P. caudatum · day 25", colors=(TEAL_C, CORAL), top=2.95, bottom=-2.45)
    bars = VGroup()
    labels = VGroup()
    arrows = VGroup()
    for x, alone, shared, color in [(-3.3, 510, 350, TEAL_C), (3.3, 180, 20, CORAL)]:
        scale = 3.0 / alone
        ba = Rectangle(width=1.25, height=alone * scale, stroke_color=color, fill_color=color, fill_opacity=0.18).move_to([x - 0.9, -1.75 + alone * scale / 2, 0])
        bs = Rectangle(width=1.25, height=shared * scale, stroke_color=color, fill_color=color, fill_opacity=0.68).move_to([x + 0.9, -1.75 + shared * scale / 2, 0])
        la = VGroup(M(str(alone), 30, TEXT), T("alone", 26, GREY)).arrange(DOWN, buff=0.06).next_to(ba, UP, buff=0.12)
        ls = VGroup(M(str(shared), 30, TEXT), T("sharing", 26, GREY)).arrange(DOWN, buff=0.06).next_to(bs, UP, buff=0.12)
        ar = DoubleArrow(ba.get_top() + RIGHT * 0.72, bs.get_top() + LEFT * 0.72, buff=0.05, color=color,
                         stroke_width=4, tip_length=0.16)
        bars.add(ba, bs)
        labels.add(la, ls)
        arrows.add(ar)
    return VGroup(panels, bars, labels, arrows), bars, labels, arrows


class S00Hook(SpokenScene):
    def construct(self):
        tubes, teal, coral, food = pair_world()
        float_motion(food, amp=0.15, speed=0.9, direction=DOWN)
        float_motion(teal, amp=0.30, speed=1.2, direction=RIGHT, phase=0.4)
        float_motion(coral, amp=0.30, speed=1.2, direction=LEFT, phase=1.7)
        self.play(FadeIn(tubes), FadeIn(teal[:2]), FadeIn(coral[:2]), run_time=1.1)
        self.at("What changes")
        q = fit_text("What changes with one food supply?", max_w=11.5, size=42, font=TITLE_FONT).move_to([0, 3.35, 0])
        self.play(Write(q), teal[:2].animate.shift(RIGHT * 0.28), coral[:2].animate.shift(LEFT * 0.28), run_time=1.2)
        self.at("tiny one")
        self.play(LaggedStart(*[FadeIn(s, scale=0.6) for s in list(teal[2:]) + list(coral[2:])], lag_ratio=0.08), run_time=1.3)
        self.play(teal.animate.shift(UP * 0.14), coral.animate.shift(DOWN * 0.14), run_time=1.0, rate_func=there_and_back)
        self.at("Gold food dots")
        self.play(LaggedStart(*[FadeIn(d, shift=UP * 0.3) for d in food], lag_ratio=0.05), run_time=1.0)
        self.play(food.animate.shift(DOWN * 0.38), run_time=1.1, rate_func=linear)
        self.at("Teal swimmers")
        self.play(Indicate(teal, color=TEAL_C, scale_factor=1.07), teal.animate.shift(RIGHT * 0.16), run_time=0.75)
        self.at("coral swimmers")
        self.play(Indicate(coral, color=CORAL, scale_factor=1.07), coral.animate.shift(LEFT * 0.16), run_time=0.75)
        self.finish()


class S01Title(TitleCard):
    LESSON = "Competition and Cooperation"
    TITLE = "One Tube, One Shared Supply"

    def construct(self):
        tubes, teal, coral, food = pair_world()
        float_motion(food, amp=0.12, speed=1.1, direction=DOWN)
        backdrop = VGroup(tubes, teal, coral, food).set_opacity(0.20)
        title = fit_text(self.TITLE, max_w=11.5, size=52, font=TITLE_FONT).move_to([0, 0.2, 0])
        lesson = T(self.LESSON.upper(), 24, TEAL_C).next_to(title, UP, buff=0.38)
        rule = Line(LEFT * 1.4, RIGHT * 1.4, color=GOLD, stroke_width=5).next_to(title, DOWN, buff=0.38)
        self.add(backdrop)
        self.play(tubes[0].animate.shift(RIGHT * 0.24), tubes[1].animate.shift(LEFT * 0.24),
                  food.animate.shift(DOWN * 0.22), FadeIn(lesson), Write(title), GrowFromCenter(rule), run_time=1.35)
        self.wait(0.65)


class S02Alone(SpokenScene):
    def construct(self):
        tubes, teal, coral, food = pair_world()
        float_motion(food, amp=0.15, speed=0.9, direction=DOWN)
        float_motion(teal, amp=0.28, speed=1.25, direction=RIGHT, phase=0.3)
        float_motion(coral, amp=0.28, speed=1.25, direction=LEFT, phase=1.5)
        self.add(tubes, teal, coral, food)
        self.at("A population")
        rings = VGroup(*[Circle(radius=0.48, color=TEAL_C, stroke_width=2).move_to(s) for s in teal])
        definition = fit_text("one species · one place · one time", max_w=10.8, size=32, color=TEXT).move_to([0, 3.32, 0])
        self.play(Create(rings), FadeIn(definition), run_time=1.1)
        self.at("Each tube begins")
        self.play(FadeOut(rings), teal.animate.shift(UP * 0.12), coral.animate.shift(UP * 0.12), run_time=0.9)
        self.play(food.animate.shift(DOWN * 0.35), run_time=0.9)
        self.at("As food arrives")
        extra_a = swimmer_group([(-3.8, 0.85), (-3.15, -0.85), (-4.65, -0.65)], TEAL_C, 21, 0.9)
        extra_c = swimmer_group([(3.75, 0.8), (3.1, -0.9), (4.65, -0.7)], CORAL, 22, 0.9)
        bars = VGroup(
            Rectangle(width=0.3, height=0.35, stroke_color=TEAL_C, fill_color=TEAL_C, fill_opacity=0.8).move_to([-1.05, -2.05, 0]),
            Rectangle(width=0.3, height=0.35, stroke_color=CORAL, fill_color=CORAL, fill_opacity=0.8).move_to([1.05, -2.05, 0]),
        )
        self.play(FadeIn(extra_a), FadeIn(extra_c), FadeIn(bars), run_time=0.7)
        self.play(bars[0].animate.stretch_to_fit_height(3.65).move_to([-1.05, -0.4, 0]),
                  bars[1].animate.stretch_to_fit_height(3.35).move_to([1.05, -0.55, 0]), run_time=2.0)
        self.at("bars stop rising")
        plateaus = VGroup(Line([-1.5, 1.43, 0], [-0.6, 1.43, 0], color=TEAL_C, stroke_width=5),
                          Line([0.6, 1.13, 0], [1.5, 1.13, 0], color=CORAL, stroke_width=5))
        self.play(Create(plateaus), food.animate.shift(DOWN * 0.28), run_time=1.0)
        tag = scope_tag("schematic")
        self.play(FadeIn(tag), bars.animate.shift(UP * 0.04), run_time=0.7, rate_func=there_and_back)
        self.finish()


class S03Competition(SpokenScene):
    def construct(self):
        world = shared_world()
        float_motion(world.food, amp=0.14, speed=0.9, direction=DOWN)
        float_motion(world.teal, amp=0.30, speed=1.2, direction=UP, phase=0.2)
        float_motion(world.coral, amp=0.30, speed=1.2, direction=DOWN, phase=1.4)
        heading = T("same limited food", 36, GOLD).move_to([0, 3.3, 0])
        self.play(FadeIn(world), FadeIn(heading), run_time=1.0)
        self.at("there is not enough")
        self.play(world.teal.animate.shift(RIGHT * 0.35), world.coral.animate.shift(LEFT * 0.35),
                  world.food.animate.shift(DOWN * 0.25), run_time=1.2)
        self.at("does not require")
        no_fight = chip("no fight required", TEXT, size=30).move_to([0, -3.32, 0])
        self.play(FadeIn(no_fight), world.teal.animate.shift(UP * 0.10), world.coral.animate.shift(DOWN * 0.10), run_time=0.9)
        self.at("food dot eaten")
        target = world.food[3]
        eater = world.teal[2]
        start = target.get_center().copy()
        self.play(eater.animate.move_to(start + LEFT * 0.35), target.animate.move_to(start + LEFT * 0.18), run_time=0.85)
        self.play(FadeOut(target, scale=0.2), eater.animate.set_fill(opacity=0.8), run_time=0.45)
        self.at("no longer available")
        turner = world.coral[0]
        self.play(turner.animate.shift(RIGHT * 0.8).rotate(PI / 2), world.food.animate.shift(DOWN * 0.22), run_time=1.0)
        self.finish()


class S04Predict(SpokenScene):
    def construct(self):
        pic = predict_world()
        float_motion(pic[0].food, amp=0.13, speed=0.9, direction=DOWN)
        self.play(FadeIn(pic[0]), run_time=0.7)
        self.at("slide both populations")
        self.play(pic[0].teal.animate.shift(RIGHT * 0.25), pic[0].coral.animate.shift(LEFT * 0.25), run_time=1.0)
        food_level = T("same food supply", 28, GOLD).move_to([-3.85, -3.12, 0])
        self.play(FadeIn(food_level), pic[0].food.animate.shift(DOWN * 0.25), run_time=0.8)
        self.at("Which population")
        self.play(Create(pic[1]), Create(pic[2]), run_time=1.1)
        q = question_card("Which stays common? Which falls?", y=3.34, size=34, max_w=11.2)
        self.play(FadeIn(q.question), pic[0].teal.animate.shift(UP * 0.12), run_time=0.8)
        self.at("Which will fall")
        self.play(pic[0].coral.animate.shift(DOWN * 0.18), pic[0].food.animate.shift(DOWN * 0.18), run_time=0.8)
        self.at("Make a prediction")
        self.play(Indicate(q.question, color=GOLD, scale_factor=1.04), run_time=0.8)
        self.at("real counts")
        self.play(Indicate(VGroup(pic[1], pic[2]), color=TEXT, scale_factor=1.02), run_time=0.7)
        self.finish()


class S05Pause(PredictPause):
    QUESTION = "Which stays common? Which falls?"
    OPTIONS = ()
    CARD = {"y": 3.34, "size": 34, "max_w": 11.2}
    RING_AT = (-0.7, -3.22, 0)
    SECONDS = 4.5

    def backdrop(self):
        pic = predict_world()
        float_motion(pic[0].food, amp=0.13, speed=0.9, direction=DOWN)
        return pic


class S06Reveal(SpokenScene):
    def construct(self):
        plots = data_plots()
        plots[0].food.set_opacity(0.45)
        plots[0].teal.set_opacity(0.38)
        plots[0].coral.set_opacity(0.38)
        float_motion(plots[0].food, amp=0.24, speed=1.2, direction=DOWN)
        float_motion(plots[0].teal, amp=0.32, speed=1.25, direction=UP, phase=1.2)
        float_motion(plots[0].coral, amp=0.32, speed=1.25, direction=DOWN, phase=0.2)
        heading = T("Gause data · selected days", 32, TEXT).move_to([0, 3.35, 0])
        self.play(FadeIn(plots[0]), FadeIn(heading), Create(plots.top), Create(plots.bot), run_time=1.1)
        self.at("bacteria as food")
        food_note = chip("bacteria as food", GOLD, size=26).move_to([4.5, 3.3, 0])
        self.play(FadeIn(food_note), run_time=0.65)
        self.at("each kind alone")
        alone_note = T("alone → then sharing", 28, GREY).move_to([0, 3.35, 0])
        self.play(swap(heading, alone_note), run_time=0.7)
        self.at("grew them together")
        self.play(FadeIn(plots.shared), run_time=1.0)
        cursor = ValueTracker(0)
        sweep = always_redraw(lambda: VGroup(
            Line(plots.top.pt(cursor.get_value(), 0), plots.top.pt(cursor.get_value(), 650), color=GOLD, stroke_width=3),
            Line(plots.bot.pt(cursor.get_value(), 0), plots.bot.pt(cursor.get_value(), 220), color=GOLD, stroke_width=3),
        ))
        self.add(sweep)
        self.at("Teal orlia")
        self.play(cursor.animate.set_value(16), run_time=2.2, rate_func=linear)
        self.play(Indicate(plots.shared[:2], color=TEAL_C, scale_factor=1.01), run_time=0.7)
        self.at("Coral caudatum")
        self.play(cursor.animate.set_value(25), run_time=1.4, rate_func=linear)
        self.play(Indicate(plots.shared[2:], color=CORAL, scale_factor=1.01), run_time=0.65)
        self.finish()


class S07Compare(SpokenScene):
    def construct(self):
        group, bars, labels, arrows = fraction_panel()
        backdrop = shared_world(opacity=0.18)
        backdrop.food.set_opacity(0.2)
        backdrop.teal.set_opacity(0.12)
        backdrop.coral.set_opacity(0.12)
        backdrop.layout_ok = True  # deliberate faint swimmers behind the comparison, required by script visual
        float_motion(backdrop.food, amp=0.24, speed=1.2, direction=DOWN)
        float_motion(backdrop.teal, amp=0.32, speed=1.25, direction=UP, phase=0.4)
        float_motion(backdrop.coral, amp=0.32, speed=1.25, direction=DOWN, phase=1.4)
        self.add(backdrop)
        self.play(FadeIn(group[0]), run_time=0.8)
        self.at("each population against")
        self.play(GrowFromEdge(bars, DOWN), FadeIn(labels), run_time=1.2)
        self.at("last day shown")
        self.play(Create(arrows), run_time=1.0)
        less = VGroup(T("160 fewer", 28, TEAL_C).move_to([-3.3, -2.05, 0]),
                      T("160 fewer", 28, CORAL).move_to([3.3, -2.05, 0]))
        self.play(FadeIn(less), run_time=0.65)
        self.at("caudatum much more")
        self.play(Indicate(bars[3], color=CORAL, scale_factor=1.08), run_time=0.8)
        self.at("larger share")
        fractions = VGroup(
            M("350 / 510 ≈ 69% remains", 30, TEAL_C).move_to([-3.3, 0.0, 0]),
            M("20 / 180 ≈ 11% remains", 30, CORAL).move_to([3.3, 0.0, 0]),
        )
        self.play(FadeOut(VGroup(bars, labels, arrows, less)), FadeIn(fractions), run_time=1.0)
        teal_fill = Rectangle(width=4.7, height=0.58, color=TEAL_C, fill_color=TEAL_C, fill_opacity=0.65).move_to([-3.3, -1.0, 0])
        coral_track = Rectangle(width=4.7, height=0.58, color=CORAL, fill_opacity=0.0).move_to([3.3, -1.0, 0])
        coral_fill = Rectangle(width=0.52, height=0.58, color=CORAL, fill_color=CORAL, fill_opacity=0.7).align_to(coral_track, LEFT).move_to([1.21, -1.0, 0], aligned_edge=LEFT)
        self.play(GrowFromEdge(teal_fill, LEFT), Create(coral_track), GrowFromEdge(coral_fill, LEFT), run_time=1.1)
        self.at("do not show")
        not_zero = chip("not zero", TEXT, size=30).move_to([3.3, -2.0, 0])
        self.play(FadeIn(not_zero), run_time=0.7)
        self.at("still in the tube")
        tiny = swimmer_group([(2.7, -1.95), (3.9, -1.95)], CORAL, seed=31, scale=0.72)
        self.play(FadeOut(not_zero), FadeIn(tiny), tiny.animate.shift(DOWN * 0.10), run_time=0.8)
        falling = Arrow([4.8, -1.6, 0], [4.8, -2.35, 0], color=CORAL, stroke_width=5, tip_length=0.2)
        self.at("count is still falling")
        self.play(GrowArrow(falling), run_time=0.7)
        self.finish()


class S08Quiet(SpokenScene):
    def construct(self):
        world = shared_world()
        float_motion(world.food, amp=0.14, speed=0.9, direction=DOWN)
        heading = T("quiet competition", 40, font=TITLE_FONT).move_to([0, 3.3, 0])
        self.play(FadeIn(world), FadeIn(heading), run_time=0.9)
        self.at("do not chase")
        calm = chip("no chasing · no attack", TEXT, size=28).move_to([0, -3.02, 0])
        self.play(FadeIn(calm), world.teal.animate.shift(UP * 0.1), world.coral.animate.shift(DOWN * 0.1), run_time=0.9)
        self.at("same limited food")
        target = world.food[3]
        self.play(world.teal[2].animate.move_to(target.get_center() + LEFT * 0.28), target.animate.scale(0.3), run_time=0.85)
        self.play(FadeOut(target), world.food.animate.shift(DOWN * 0.18), run_time=0.45)
        self.at("Members of one species")
        self.play(FadeOut(calm), world.coral.animate.set_color(TEAL_C), run_time=0.8)
        outlines = VGroup(
            RoundedRectangle(corner_radius=0.22, width=4.8, height=3.6, color=TEAL_C).move_to([-2.65, -0.15, 0]),
            RoundedRectangle(corner_radius=0.22, width=4.8, height=3.6, color=TEAL_C).move_to([2.65, -0.15, 0]),
        )
        self.play(Transform(world.tube, outlines), world.teal.animate.shift(LEFT * 0.35), world.coral.animate.shift(RIGHT * 0.35), run_time=1.0)
        shared_food = Dot([0, -0.1, 0], radius=0.14, color=GOLD)
        reach = VGroup(Arrow([-1.6, -0.1, 0], [-0.2, -0.1, 0], color=TEAL_C, buff=0.12),
                       Arrow([1.6, -0.1, 0], [0.2, -0.1, 0], color=TEAL_C, buff=0.12))
        self.at("same resources")
        self.play(FadeIn(shared_food), GrowArrow(reach[0]), GrowArrow(reach[1]), run_time=0.9)
        self.finish()


class S09Limits(SpokenScene):
    def construct(self):
        world = shared_world(cx=0, w=7.2, h=4.3)
        world.scale(0.78).move_to([0, -0.15, 0])
        float_motion(world.food, amp=0.14, speed=0.9, direction=DOWN)
        tag = scope_tag("simulation")
        self.play(FadeIn(world), FadeIn(tag), run_time=0.9)
        self.at("food is steady")
        food_read = Readout([("food", lambda: 1.0, "{:4.1f} steady", GOLD)], at=[-4.3, 2.15, 0], widest=[1.0], size=26, title="model control")
        self.play(FadeIn(food_read), world.food.animate.shift(DOWN * 0.18), run_time=0.9)
        self.at("no predators")
        pred = chip("predators", CORAL, size=28).move_to([4.75, 2.15, 0])
        cross = T("×", 52, TEXT).move_to([3.25, 2.15, 0])
        self.play(FadeIn(pred), Create(cross), run_time=0.75)
        self.at("set to use food faster")
        speed = ValueTracker(0.35)
        gauge = dial(speed, center=[4.7, -1.45, 0], radius=1.05, label="model setting", color=GOLD, fmt="{:.0f}", scale=10, size=32)
        neutral = swimmer([3.15, -1.5], GREY, scale=0.85)
        self.play(FadeIn(gauge), FadeIn(neutral), run_time=0.8)
        self.play(speed.animate.set_value(0.86), neutral.animate.shift(RIGHT * 0.18), run_time=1.0)
        self.at("other conditions")
        other = chip("other liquid conditions ?", BLUE, size=26).move_to([0, 3.25, 0])
        self.play(FadeOut(food_read), FadeIn(other), world.teal.animate.shift(UP * 0.08), run_time=0.8)
        self.at("counts support competition")
        evidence = caption("Counts support competition", size=30, color=TEXT)
        self.play(FadeOut(VGroup(pred, cross, gauge, neutral, other)), FadeIn(evidence), run_time=0.8)
        self.at("cannot prove")
        limit = caption("Food was not proven the only cause", size=30, color=BLUE)
        self.play(swap(evidence, limit), world.food.animate.shift(DOWN * 0.15), run_time=0.9)
        self.finish()


class S10Bridge(SpokenScene):
    def construct(self):
        carried = shared_world(opacity=0.55)
        carried.food.set_opacity(0.75)
        carried.teal.set_opacity(0.70)
        carried.coral.set_opacity(0.70)
        float_motion(carried.teal, amp=0.32, speed=1.2, direction=UP, phase=0.3)
        float_motion(carried.coral, amp=0.32, speed=1.2, direction=DOWN, phase=1.3)
        float_motion(carried.food, amp=0.22, speed=1.0, direction=DOWN)
        rule = fit_text("Limited resources can restrict populations; cooperation can help members meet their needs.",
                        max_w=12.0, size=36, color=TEXT, max_lines=2).move_to([0, 3.35, 0])
        self.add(carried)
        self.play(FadeIn(rule), carried.teal.animate.shift(RIGHT * 0.12), carried.coral.animate.shift(LEFT * 0.12), run_time=0.8)
        panels = TwoPanel("limited resource", "cooperation", colors=(GOLD, GREEN), top=2.65, bottom=-2.45)
        self.at("Limited resources")
        self.play(FadeOut(carried), FadeIn(panels), run_time=0.8)
        food = Dot([-3.3, 0.0, 0], radius=0.18, color=GOLD)
        a = swimmer([-4.55, 0.0], TEAL_C, 1.25)
        c = swimmer([-2.05, 0.0], CORAL, 1.25, PI)
        float_motion(a, amp=0.42, speed=1.25, direction=UP, phase=0.2)
        float_motion(c, amp=0.42, speed=1.25, direction=DOWN, phase=1.4)
        inward = VGroup(Arrow(a.get_right(), food.get_center() + LEFT * 0.2, color=TEAL_C, buff=0.12),
                         Arrow(c.get_left(), food.get_center() + RIGHT * 0.2, color=CORAL, buff=0.12))
        self.play(FadeIn(a), FadeIn(c), FadeIn(food), GrowArrow(inward[0]), GrowArrow(inward[1]), run_time=1.0)
        self.at("Cooperation can help")
        workers = swimmer_group([(2.0, 0.65), (3.3, -0.45), (4.6, 0.65)], GREEN, seed=44, scale=0.95)
        path = VGroup(Line(workers[0].get_center(), workers[1].get_center(), color=GREEN, stroke_width=7),
                      Line(workers[1].get_center(), workers[2].get_center(), color=GREEN, stroke_width=7))
        float_motion(workers, amp=0.46, speed=1.25, direction=UP)
        self.play(FadeIn(workers), Create(path), run_time=1.1)
        self.at("first half")
        self.play(Indicate(VGroup(a, c, food, inward), color=GOLD, scale_factor=1.04), run_time=0.8)
        left_rule = T("resources can restrict", 30, GOLD).move_to([-3.3, -1.75, 0])
        self.at("even without a fight")
        self.play(FadeIn(left_rule), a.animate.shift(RIGHT * 0.12), c.animate.shift(LEFT * 0.12), run_time=0.9)
        waiting = T("what can working together change?", 28, GREEN).move_to([3.3, -3.05, 0])
        self.at("second film asks")
        self.play(FadeIn(waiting), workers.animate.shift(UP * 0.08), run_time=0.8)
        self.finish()


class S11End(EndCard):
    LINE = "Limited resources can restrict populations, even without a fight."
