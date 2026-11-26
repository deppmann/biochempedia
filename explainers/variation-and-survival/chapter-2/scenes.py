"""Reading Selection in a Population.

COLOR MAP
  TEAL = inherited tusklessness
  GOLD = inherited tusks
  BLUE = blue crab
  GREEN = successful passage and evidence supporting selection
  RED = environmental limits and blocked passage
  GREY = neutral structure, models, and limits
  ORANGE = crab eggs
"""

from importlib.util import module_from_spec, spec_from_file_location
from math import comb
from pathlib import Path

import numpy as np

from bp_parts import *
from bp_style import EndCard


# Load the chapter 1 artwork by path because both chapters have a scenes.py.
chapter_one_spec = spec_from_file_location(
    "variation_and_survival_chapter_one", Path(__file__).resolve().parents[1] / "scenes.py"
)
chapter_one = module_from_spec(chapter_one_spec)
chapter_one_spec.loader.exec_module(chapter_one)

DATA = (
    ("Prewar", 54, 18.5),
    ("War survivors", 108, 50.9),
    ("Postwar daughters", 91, 33.0),
)
BAR_X = (-5.0, 0.0, 4.65)
BAR_WIDTH = 2.30
BAR_BOTTOM = -1.70
BAR_HEIGHT = 4.0
TRACK_Y = (1.22, -0.83)
TRACK_X = (-3.16, -1.84)
EGG_COLOR = "#F29E4C"
PREDICT = "What changed?"
RETURN = "Who left the next generation?"


def point(x, y):
    return np.array([x, y, 0.0])


def stage():
    return RoundedRectangle(
        width=13.25, height=6.65, corner_radius=0.24, stroke_width=0,
        fill_color="#2A303C", fill_opacity=1,
    ).set_z_index(-100)


class FilmScene(SpokenScene):
    def setup(self):
        super().setup()
        self.add(stage())


def elephant(color, scale=1.0, outline=False):
    animal = chapter_one.elephant(color, tusked=color == GOLD, scale=scale)
    if outline:
        for part in (animal[0], animal[2], animal[3]):
            part.set_fill(opacity=0)
    return animal


def label(text, x, y, size=30, color=TEXT, max_width=12):
    return fit_text(text, max_w=max_width, size=size, color=color, min_size=28).move_to(point(x, y))


def empty_bar(x, width=BAR_WIDTH, height=BAR_HEIGHT):
    return Rectangle(
        width=width, height=height, stroke_color=GREY, stroke_width=2.5,
        fill_color=BG, fill_opacity=0.22,
    ).move_to(point(x, BAR_BOTTOM + height / 2))


def share_level(percent, height=BAR_HEIGHT):
    return BAR_BOTTOM + height * percent / 100


class ShareBar(VGroup):
    """Each column encodes a share. Sample sizes are printed separately."""

    def __init__(self, index, x=None, *, compact=False):
        name, count, percent = DATA[index]
        if x is None:
            x = BAR_X[index]
        width, height = (1.33, 3.28) if compact else (BAR_WIDTH, BAR_HEIGHT)
        if compact:
            name = ("Prewar", "Survivors", "Daughters")[index]
        teal_height = height * percent / 100
        gold_height = height - teal_height
        self.shell = empty_bar(x, width, height)
        self.teal = Rectangle(
            width=width, height=teal_height, stroke_width=0, fill_color=TEAL,
            fill_opacity=0.87,
        ).move_to(point(x, BAR_BOTTOM + teal_height / 2))
        self.gold = Rectangle(
            width=width, height=gold_height, stroke_width=0, fill_color=GOLD,
            fill_opacity=0.83,
        ).move_to(point(x, BAR_BOTTOM + teal_height + gold_height / 2))
        self.fills = VGroup(self.teal, self.gold)
        heading_offset = 0.43 if compact else 0.30
        self.heading = label(name, x, BAR_BOTTOM + height + heading_offset, 28 if compact else 29 if index == 2 else 33)
        self.percent = M(f"{percent:g}%", 31 if compact else 38, TEAL).move_to(point(x, -2.12))
        self.sample = label(f"n = {count}", x, -2.68, 28)
        self.readings = VGroup(self.percent) if compact else VGroup(self.percent, self.sample)
        super().__init__(self.shell, self.fills, self.heading, self.readings)


def share_highlight(bar):
    return SurroundingRectangle(bar.teal, buff=-0.12, color=TEXT, stroke_width=3)


def measured_bars():
    return VGroup(*(ShareBar(i) for i in range(3)))


def trait_legend():
    return VGroup(
        label("Tuskless females", -2.05, 3.02, 30, TEAL),
        label("Tusked females", 2.05, 3.02, 30, GOLD),
    )


def timeline():
    return Arrow(point(-5.78, -2.91), point(5.82, -2.91), buff=0, stroke_width=3, color=GREY)


def segments(points, color, stroke_width=4):
    return VMobject(stroke_color=color, stroke_width=stroke_width).set_points_as_corners(
        [point(x, y) for x, y in points]
    )


def elephants_in_tracks(x, outline=False):
    return VGroup(*(
        elephant(color, 0.65, outline=outline).move_to(point(x, y))
        for color, y in zip((GOLD, TEAL), TRACK_Y)
    ))


def predict_details():
    source = elephants_in_tracks(TRACK_X[0])
    target = elephants_in_tracks(TRACK_X[1], outline=True)
    options = VGroup(
        boxed_label("Did elephants lose\ntheir tusks?", GOLD, 29, fill_opacity=0.24).move_to(point(3.93, 1.40)),
        boxed_label("Did group shares change?", TEAL, 28, fill_opacity=0.26).move_to(point(3.93, -0.55)),
    )
    card = question_card(PREDICT, y=-2.99, size=31).set_x(-2.50)
    return source, target, options, card


def tracked_paths():
    return VGroup(*(
        Line(point(x1, y), point(x2, y), buff=0, color=color, stroke_width=4)
        for x1, x2, y, color in (
            (-3.64, -1.35, 1.22, GOLD),
            (-3.64, -2.30, 1.75, GOLD),
            (-3.64, -2.65, 0.65, GOLD),
            (-3.64, -1.35, -0.83, TEAL),
            (-3.64, -1.35, -1.37, TEAL),
            (-3.64, -2.25, -0.25, TEAL),
        )
    )).set_z_index(-1)


def schematic_paths_label():
    return label("Schematic paths", -2.85, 3.00, 28)


def poaching_filter(narrowed=False):
    channels = VGroup()
    for (color, y), opening in zip(zip((GOLD, TEAL), TRACK_Y), (0.31, 0.93) if narrowed else (1.1, 1.1)):
        channel = Polygon(
            point(-3.64, y + 0.58), point(-1.35, y + opening / 2),
            point(-1.35, y - opening / 2), point(-3.64, y - 0.58),
            stroke_color=color, stroke_width=3, fill_color=color, fill_opacity=0.38,
        )
        channels.add(channel)
    return channels


def typical_chance_range():
    """Illustrative independent draws at the prewar share, not the study's fitted model."""
    n, p = DATA[1][1], DATA[0][2] / 100
    cdf = np.cumsum([comb(n, k) * p**k * (1 - p)**(n - k) for k in range(n + 1)])
    return tuple(100 * int(np.searchsorted(cdf, q)) / n for q in (0.025, 0.975))


def chance_band(x, width, bottom=BAR_BOTTOM, height=BAR_HEIGHT):
    low, high = typical_chance_range()
    y = bottom + height * (low + high) / 200
    band = Rectangle(
        width=width, height=height * (high - low) / 100, stroke_color=BLUE,
        stroke_width=3, fill_color=BLUE, fill_opacity=0.25,
    ).move_to(point(x, y))
    return band


def blue_crab():
    body = Ellipse(width=1.91, height=1.03, stroke_color=BLUE, stroke_width=4,
                   fill_color=BLUE, fill_opacity=0.42)
    legs = VGroup()
    claws = VGroup()
    for side in (-1, 1):
        for y, outer_y in ((0.08, 0.19), (-0.12, -0.22), (-0.29, -0.53)):
            legs.add(segments([(0.74 * side, y), (1.16 * side, y + 0.13),
                               (1.52 * side, outer_y)], BLUE, 5))
        claws.add(segments([(0.63 * side, 0.26), (1.17 * side, 0.48),
                            (1.34 * side, 0.88)], BLUE, 7))
        claw = Arc(radius=0.24, start_angle=-PI / 4, angle=3 * PI / 2,
                   color=BLUE, stroke_width=9).move_to(point(1.36 * side, 0.99))
        claws.add(claw)
    eggs = VGroup(*(
        Dot(point((col - 4) * 0.129 + (row % 2) * 0.036, -0.38 - row * 0.115),
            radius=0.075, color=interpolate_color(
                ManimColor(EGG_COLOR), ManimColor(GOLD), ((col + 3 * row) % 5) / 8,
            ))
        for row in range(5) for col in range(9) if (col - 4) ** 2 + (row - 2) ** 2 < 21
    ))
    eyes = VGroup(*(Dot(point(x, 0.29), radius=0.051, color=TEXT) for x in (-0.31, 0.31)))
    return VGroup(legs, claws, body, eggs, eyes), eggs


def strategy_animals():
    crab, eggs = blue_crab()
    crab.scale(1.22).move_to(point(-4.08, 0.84))
    mother = elephant(GOLD, 1.32)
    calf = elephant(GOLD, 0.65)
    calf.next_to(mother, RIGHT, buff=0.17, aligned_edge=DOWN)
    family = VGroup(mother, calf).move_to(point(4.05, 0.84))
    return crab, eggs, family


def strategy_panels():
    return TwoPanel(
        "Blue crab", "Elephant", colors=(BLUE, GOLD), top=2.94, bottom=-2.37,
        width=12.3, gap=3.53, size=32,
    )


def survival_gate(x=0, y=0, width=2.75, height=1.96, opening=0.34):
    """The aperture narrows from young at the top to survivors below."""
    top, bottom = y + height / 2, y - height / 2
    return VGroup(*(
        Polygon(
            point(x + side * width / 2, top),
            point(x + side * width / 2, bottom),
            point(x + side * width * opening / 2, bottom),
            point(x + side * width * 0.43, top),
            stroke_color=RED, stroke_width=3, fill_color=RED, fill_opacity=0.30,
        )
        for side in (-1, 1)
    ))


def offspring_dot(x, y, color, radius=0.16):
    return Dot(point(x, y), radius=radius, color=color)


def middle_species():
    fish = VGroup(
        Ellipse(width=0.69, height=0.40),
        Triangle().scale(0.20).rotate(-PI / 2).move_to(LEFT * 0.41),
    )
    bird = Polygon(point(-0.51, 0.17), point(-0.08, 0.08), point(0.16, 0.28),
                   point(0.51, 0.19), point(0.23, 0.09), point(0.07, -0.22),
                   point(-0.10, -0.05))
    hare = VGroup(
        Ellipse(width=0.61, height=0.40), Circle(radius=0.13).move_to(point(0.25, 0.17)),
        Ellipse(width=0.10, height=0.30).rotate(-0.27).move_to(point(0.24, 0.33)),
        Circle(radius=0.10).move_to(point(-0.33, -0.02)),
    )
    return VGroup(*(
        shape.set_stroke(width=0).set_fill(GREY, opacity=1).move_to(point(x, 0.83))
        for shape, x in zip((fish, bird, hare), (-1.56, 0.0, 1.54))
    ))


def compact_bars():
    return VGroup(*(ShareBar(i, x, compact=True) for i, x in enumerate((-5.38, -3.42, -1.46))))


def evidence_filter(expanded=False):
    x, y = (0.0 if expanded else 0.76), -0.20
    width, height = (3.68, 2.20) if expanded else (2.17, 1.55)
    gate = survival_gate(x=x, y=y, width=width, height=height)
    scale = 1.46 if expanded else 1.0
    young = VGroup(*(offspring_dot(x + dx * scale, y + height / 2 + 0.47, color, 0.16 * scale)
                     for dx, color in ((-0.75, GOLD), (-0.25, GOLD), (0.25, TEAL), (0.75, TEAL))))
    next_generation = VGroup(*(offspring_dot(x + dx * scale, y - height / 2 - 0.50, color,
                                            0.16 * scale)
                               for dx, color in ((-0.50, GOLD), (0.0, TEAL), (0.50, TEAL))))
    return gate, young, next_generation


def evidence_strands():
    names = ("Trait pattern", "Pressure", "Survival", "Daughters")
    colors = (TEAL, RED, GREEN, TEAL)
    labels = VGroup()
    lines = VGroup()
    junction = point(5.83, -1.64)
    for i, (name, color) in enumerate(zip(names, colors)):
        y = 2.60 - i * 0.79
        labels.add(label(name, 3.65, y, 29, color))
        lines.add(CubicBezier(
            point(4.90, y), point(6.53 - i * 0.26, y),
            point(5.14 + i * 0.22, -1.02), junction,
            color=color, stroke_width=4,
        ))
    lead = Arrow(junction, point(3.12, -2.05), buff=0, color=GREEN, stroke_width=5)
    result = boxed_label("Selection supported", GREEN, 32, fill_opacity=0.10).move_to(point(3.06, -2.60))
    return labels, lines, lead, result


class S00Hook(FilmScene):
    def construct(self):
        herd = chapter_one.herd(teal_n=5, y_shift=-0.2, scale=0.9, moving=False)
        dots = VGroup(*(
            Dot(animal.get_center(), radius=0.24, color=TEAL if i < 5 else GOLD)
            for i, animal in enumerate(herd)
        ))
        question = label("Selection or chance?", 0, 3.06, 42)
        legend = VGroup(
            label("Inherited tusklessness", -2.72, -2.55, 30, TEAL),
            label("Inherited tusks", 2.72, -2.55, 30, GOLD),
        )
        self.add(dots)
        self.at("The first film")
        self.play(LaggedStart(*(ReplacementTransform(d, a) for d, a in zip(dots, herd)),
                              lag_ratio=0.09), run_time=2.00)
        self.play(FadeIn(legend), run_time=0.75)
        self.at("How can data show", lead=1.0)
        self.play(Write(question), run_time=1.18)
        self.at("rather than chance")
        bars = VGroup(*(empty_bar(x) for x in BAR_X))
        empty = bars.copy().set_stroke(opacity=0).set_fill(GREY, opacity=0.34).set_z_index(-2)
        self.play(LaggedStart(*(GrowFromEdge(bar, DOWN) for bar in empty), lag_ratio=0.32), run_time=2.55)
        self.at("Return to the same")
        self.play(FadeOut(legend), FadeOut(question), run_time=0.54)
        gorongosa = label("Gorongosa elephants", 0, 3.0, 42)
        self.at("same teal and gold")
        # Move the schematic herd into three empty sample columns, without showing counts.
        groups = (herd[0:2] + herd[6:8], herd[2:4] + herd[8:10], herd[4:6] + herd[10:12])
        self.play(*(FadeOut(group, target_position=bar.get_center(), scale=0.1)
                    for group, bar in zip(groups, bars)),
                  *(Transform(old, new) for old, new in zip(empty, bars)), run_time=1.72)
        self.at("tied to Gorongosa")
        self.play(FadeIn(gorongosa), run_time=0.82)
        self.finish()


class S01Title(TitleCard):
    LESSON = "Variation and Survival"
    TITLE = "Reading Selection in a Population"

    def construct(self):
        columns = VGroup(*(empty_bar(x) for x in BAR_X))
        title = fit_text(self.TITLE, max_w=12, size=52, font=TITLE_FONT).move_to(point(0, 0.20))
        lesson = label(self.LESSON.upper(), 0, 1.35, 28)
        rule = Line(LEFT * 1.34, RIGHT * 1.34, color=GOLD, stroke_width=4).shift(DOWN * 0.68)
        teal = elephant(TEAL, 0.56).move_to(point(-5.0, -1.24))
        gold = elephant(GOLD, 0.56).move_to(point(5.0, -1.24))
        self.add(stage(), columns.set_opacity(0.25))
        self.play(FadeOut(columns), run_time=0.23)
        self.play(Write(title), FadeIn(lesson), GrowFromCenter(rule), run_time=0.94)
        self.play(FadeIn(teal, shift=RIGHT * 0.40), FadeIn(gold, shift=LEFT * 0.40), run_time=0.60)
        self.wait(max(1 / config.frame_rate, self.narration_s - self.elapsed()))


class S02Groups(FilmScene):
    def construct(self):
        prewar, survivors, daughters = measured_bars()
        legend = trait_legend()
        self.add(prewar.shell, survivors.shell, daughters.shell)
        teal_example = elephant(TEAL, 1.16).move_to(point(-2.49, 0.70))
        gold_example = elephant(GOLD, 1.16).move_to(point(2.33, 0.70))
        self.at("Teal marks tuskless")
        self.play(GrowFromCenter(teal_example), run_time=0.82)
        self.play(FadeIn(legend[0]), run_time=0.64)
        self.at("gold marks tusked")
        self.play(GrowFromCenter(gold_example), run_time=0.84)
        self.play(FadeIn(legend[1]), run_time=0.62)
        self.at("Historical film")
        self.play(GrowFromEdge(prewar.fills, DOWN), FadeOut(teal_example), FadeOut(gold_example),
                  run_time=1.62)
        self.play(FadeIn(prewar.heading), run_time=0.52)
        self.at("Later sightings")
        self.play(GrowFromEdge(survivors.fills, DOWN), run_time=1.57)
        self.play(FadeIn(survivors.heading), run_time=0.55)
        self.at("The bars use")
        self.play(FadeOut(daughters.shell), run_time=0.55)
        self.at("reported group sizes")
        self.play(FadeIn(VGroup(prewar.sample, survivors.sample)), run_time=0.75)
        self.at("and percentages")
        self.play(FadeIn(VGroup(prewar.percent, survivors.percent)), FadeOut(legend), run_time=0.85)
        self.finish()


class S03Predict(FilmScene):
    def construct(self):
        prewar, survivors, _ = measured_bars()
        source, target, options, card = predict_details()
        self.add(prewar, survivors)
        self.at("The teal share")
        borders = VGroup(*(
            share_highlight(bar)
            for bar in (prewar, survivors)
        ))
        self.play(Create(borders[0]), Create(borders[1]),
                  prewar.gold.animate.set_fill(opacity=0.36),
                  survivors.gold.animate.set_fill(opacity=0.36), run_time=0.93)
        self.at("higher among survivors")
        prewar_level = share_level(DATA[0][2])
        comparison = DashedLine(point(-3.80, prewar_level), point(-1.20, prewar_level),
                                color=TEAL, stroke_width=4)
        self.play(Create(comparison), FadeOut(borders[0]), run_time=1.30)
        self.at("What changed")
        self.play(Write(card.question), FadeOut(borders[1]), FadeOut(comparison),
                  prewar.gold.animate.set_fill(opacity=0.83),
                  survivors.gold.animate.set_fill(opacity=0.83), run_time=1.27)
        self.at("Did individual elephants")
        self.play(FadeIn(source[0], target_position=point(-5.0, TRACK_Y[0])),
                  FadeIn(source[1], target_position=point(-5.0, -1.30)), run_time=1.48)
        self.play(FadeIn(options[0]), run_time=0.62)
        self.at("the two groups")
        self.play(FadeIn(target[0], shift=RIGHT * 0.20),
                  FadeIn(target[1], shift=RIGHT * 0.20), run_time=1.12)
        self.at("born with each")
        self.play(FadeIn(options[1], shift=UP * 0.58), run_time=2.49, rate_func=linear)
        self.finish()


class S04Pause(Scene):
    def construct(self):
        self.camera.background_color = ManimColor(BG)
        prewar, survivors, _ = measured_bars()
        self.add(stage(), prewar, survivors, *predict_details())
        self.wait(4.5)


class S05GroupReveal(FilmScene):
    def construct(self):
        prewar, survivors, _ = measured_bars()
        source, target, options, card = predict_details()
        self.add(prewar, survivors, source, target, options, card)
        self.at("Track two schematic")
        self.play(FadeOut(options), FadeOut(card), run_time=0.50, rate_func=linear)
        self.play(Write(schematic_paths_label()), run_time=1.18)
        paths = tracked_paths()
        self.at("A gold animal")
        self.play(Create(paths[0]), source[0].animate.move_to(target[0]),
                  prewar.teal.animate.set_fill(opacity=0.37),
                  survivors.teal.animate.set_fill(opacity=0.37), run_time=1.85)
        self.remove(target[0])
        self.at("a teal animal")
        self.play(Create(paths[3]), source[1].animate.move_to(target[1]),
                  prewar.teal.animate.set_fill(opacity=0.87),
                  survivors.teal.animate.set_fill(opacity=0.87),
                  prewar.gold.animate.set_fill(opacity=0.39),
                  survivors.gold.animate.set_fill(opacity=0.39), run_time=1.88)
        self.remove(target[1])
        self.at("The survivor group")
        extra = (paths[1], paths[2], paths[4], paths[5])
        markers = VGroup(*(
            offspring_dot(path.get_start()[0], path.get_start()[1], path.get_color(), radius=0.125)
            for path in extra
        ))
        self.play(LaggedStart(*(Create(path) for path in extra), lag_ratio=0.16),
                  prewar.gold.animate.set_fill(opacity=0.83),
                  survivors.gold.animate.set_fill(opacity=0.83), run_time=1.85)
        self.at("tuskless females survived")
        self.play(*(m.animate.move_to(p.get_end()) for m, p in zip(markers, extra)),
                  run_time=1.45, rate_func=linear)
        self.at("poaching more often")
        self.play(FadeOut(markers), *(path.animate.set_stroke(opacity=0.22)
                                     for path in (paths[1], paths[2], paths[5])),
                  survivors.gold.animate.set_fill(opacity=0.53), run_time=1.02)
        self.finish()


class S06Pressure(FilmScene):
    def construct(self):
        prewar, survivors, _ = measured_bars()
        paths = tracked_paths()
        for i in (1, 2, 5):
            paths[i].set_stroke(opacity=0.22)
        survivors.gold.set_fill(opacity=0.53)
        tracked = elephants_in_tracks(TRACK_X[1])
        tag = schematic_paths_label()
        self.add(prewar, survivors, paths, tracked, tag)
        self.at("Ivory poaching")
        gates = poaching_filter()
        self.play(ReplacementTransform(paths, gates), FadeOut(tracked), run_time=1.35)
        pressure = label("Ivory poaching", -2.85, 3.00, 29, RED)
        self.at("selective pressure")
        self.play(swap(tag, pressure, 0.92))
        self.at("affected the variants")
        narrow = poaching_filter(narrowed=True)
        self.play(Transform(gates, narrow), run_time=1.78)
        self.at("elephants were killed")
        blocked = elephants_in_tracks(-2.82)[0]
        passing = elephants_in_tracks(-2.82)[1]
        self.play(FadeIn(blocked), FadeIn(passing), run_time=0.55)
        obstruction = Rectangle(width=0.57, height=0.30, stroke_width=0,
                                fill_color=RED, fill_opacity=0.90).move_to(point(-1.69, 1.22))
        self.play(GrowFromEdge(obstruction, RIGHT), blocked.animate.move_to(point(-2.53, TRACK_Y[0])),
                  passing.animate.move_to(point(-1.99, TRACK_Y[1])), run_time=0.86)
        self.play(FadeOut(blocked), survivors.gold.animate.set_fill(opacity=0.83), run_time=0.82)
        self.at("The data support")
        supported = boxed_label("Supported explanation", GREEN, 31, fill_opacity=0.13)
        supported.move_to(point(3.85, 1.40))
        self.play(FadeIn(supported, shift=UP * 0.12), run_time=1.20)
        self.at("population's makeup")
        self.play(FadeOut(passing), run_time=0.45)
        self.at("a choice or transformation")
        cartoon = VGroup(
            elephant(GOLD, 0.84).move_to(point(2.55, -0.55)),
            Arrow(point(3.18, -0.55), point(4.42, -0.55), color=GREY, buff=0.09),
            elephant(TEAL, 0.84).move_to(point(5.03, -0.55)),
        )
        slash = Cross(cartoon, stroke_color=RED, stroke_width=6, scale_factor=0.74)
        self.play(FadeIn(VGroup(cartoon, slash)), run_time=1.18)
        self.finish()


class S07ChanceModel(FilmScene):
    def construct(self):
        prewar, survivors, _ = measured_bars()
        self.add(prewar, survivors)
        tags = VGroup(
            label("Equal-survival simulation", -3.89, 2.49, 32, max_width=4.55),
            scope_tag("Schematic model", size=28, color=TEXT).move_to(point(-3.90, -2.87)),
        )
        block = RoundedRectangle(width=4.56, height=3.91, corner_radius=0.16,
                                 stroke_color=GREY, stroke_width=3).move_to(point(-3.89, 0.06))
        sample = chapter_one.herd(teal_n=2, moving=False).scale(0.39).move_to(point(-3.89, 0.83))
        self.at("A severe population crash")
        self.play(FadeOut(prewar), Create(block), run_time=1.20)
        self.play(FadeIn(sample), FadeIn(tags[1]), run_time=0.68)
        self.at("change shares by chance")
        keep = (0, 4, 7, 9, 11)
        self.play(LaggedStart(*(FadeOut(a, scale=0.35) for i, a in enumerate(sample) if i not in keep),
                              lag_ratio=0.14), run_time=1.52)
        self.at("Researchers modeled the crash")
        self.play(FadeIn(tags[0]), run_time=1.05)
        self.at("equal survival")
        band = chance_band(-2.48, 1.48).set_fill(opacity=0.75)
        arrows = Arrow(point(-4.06, 0.72), point(-3.30, -0.92), color=BLUE, buff=0.05)
        typical = label("Typical range", -4.65, -1.34, 28, BLUE)
        remaining = VGroup(*(sample[i] for i in keep))
        self.play(remaining.animate.scale(0.78).move_to(point(-4.14, 1.25)), run_time=0.82)
        self.at("tusked and tuskless")
        self.play(GrowArrow(arrows), run_time=1.00)
        self.play(GrowFromEdge(band, LEFT), FadeIn(typical), run_time=1.24)
        self.at("The observed rise")
        y = share_level(DATA[1][2])
        rule = DashedLine(point(-3.09, y), point(-1.21, y), color=TEAL, stroke_width=3)
        marker = Line(point(1.21, y), point(2.59, y), color=TEAL, stroke_width=4)
        observed = label("Observed 50.9%", 4.62, y, 34, TEAL)
        self.play(Create(rule), Create(marker), survivors.gold.animate.set_fill(opacity=0.35),
                  run_time=1.15)
        self.at("far beyond what")
        bracket = DoubleArrow(point(-1.82, band.get_top()[1] + 0.08), point(-1.82, y - 0.06),
                              buff=0, color=TEXT, stroke_width=3, tip_length=0.15)
        self.play(GrowFromCenter(bracket), FadeIn(observed), run_time=1.28)
        self.at("that chance model")
        self.play(band.animate.set_fill(opacity=0.33),
                  survivors.gold.animate.set_fill(opacity=0.83), run_time=1.48)
        self.finish()


def allele_labels():
    return VGroup(
        boxed_label("Visible\ntrait", TEAL, 29, pad=0.13, fill_opacity=0.23).move_to(point(-2.50, 0.16)),
        boxed_label("Exact allele\nunknown", TEXT, 28, pad=0.10, fill_opacity=0.12).move_to(point(2.33, 0.16)),
    )


class S08Daughters(FilmScene):
    def construct(self):
        prewar, survivors, daughters = measured_bars()
        self.add(prewar, survivors, daughters.shell)
        self.at("Daughters born later")
        self.play(GrowFromEdge(daughters.fills, DOWN), run_time=1.65)
        self.play(FadeIn(daughters.heading), FadeIn(daughters.readings), run_time=0.68)
        self.at("above the pre")
        compare = VGroup(share_highlight(prewar), share_highlight(daughters))
        self.play(Create(compare[0]), Create(compare[1]),
                  prewar.gold.animate.set_fill(opacity=0.45),
                  daughters.gold.animate.set_fill(opacity=0.45), run_time=1.35)
        self.at("That pattern fits")
        time_arrow = timeline().shift(DOWN * 0.24)
        self.play(GrowArrow(time_arrow), FadeOut(compare),
                  prewar.gold.animate.set_fill(opacity=0.83),
                  daughters.gold.animate.set_fill(opacity=0.83), run_time=1.56)
        trait, unknown = allele_labels()
        self.play(FadeIn(trait, shift=UP * 0.17), run_time=1.12)
        self.at("response to selection")
        self.play(survivors.gold.animate.set_fill(opacity=0.50),
                  daughters.gold.animate.set_fill(opacity=0.50), run_time=1.30)
        self.at("identify the exact")
        self.play(FadeIn(unknown, shift=UP * 0.17), run_time=1.23)
        self.at("what happened to every")
        self.play(survivors.gold.animate.set_fill(opacity=0.83),
                  daughters.gold.animate.set_fill(opacity=0.83), run_time=1.10)
        self.finish()


class S10Surplus(FilmScene):
    def construct(self):
        bars = measured_bars()
        last_scene = VGroup(
            bars, timeline().shift(DOWN * 0.24),
            allele_labels(),
        )
        self.add(last_scene)
        self.at("Now widen the picture")
        panels = strategy_panels()
        crab, eggs, family = strategy_animals()
        crab.remove(eggs)
        mother, calf = family
        self.play(FadeOut(last_scene), run_time=0.56)
        self.play(Create(panels.left_frame), GrowFromCenter(crab), run_time=0.97)
        self.play(Create(panels.right_frame), GrowFromCenter(mother), run_time=0.92)
        self.at("Populations usually produce")
        gate = survival_gate()
        young = VGroup(*(
            offspring_dot(x, y, EGG_COLOR, 0.143)
            for y in (1.77, 1.35) for x in (-0.88, -0.44, 0.0, 0.44, 0.88)
        ))
        self.play(LaggedStart(*(GrowFromCenter(d) for d in young), lag_ratio=0.10), run_time=1.71)
        self.at("their environments can support")
        self.play(Create(gate), run_time=1.35)
        limit = label("Environment", 0, -1.48, 28, RED)
        self.play(FadeIn(limit), run_time=0.66)
        self.at("A female blue crab")
        self.play(FadeIn(panels.left_head), run_time=0.63)
        self.at("an enormous egg mass")
        self.play(LaggedStart(*(GrowFromCenter(d) for d in eggs), lag_ratio=0.045), run_time=1.65)
        self.at("An elephant mother")
        self.play(FadeIn(panels.right_head), run_time=0.78)
        self.at("invests years in")
        herd_path = calf.copy().scale(0.47).shift(LEFT * 0.50)
        self.play(FadeIn(herd_path), run_time=0.37)
        self.play(ReplacementTransform(herd_path, calf), run_time=1.61, rate_func=smooth)
        self.at("Most crab young")
        survivors = (young[1], young[7])
        self.play(LaggedStart(
            *(FadeOut(d, target_position=point(d.get_x() * 0.7, 0.18)) for d in young if d not in survivors),
            lag_ratio=0.08,
        ), *(d.animate.move_to(point(x, -1.11)) for d, x in zip(survivors, (-0.20, 0.20))),
            gate.animate.set_fill(opacity=0.63), run_time=1.60)
        self.play(FadeOut(VGroup(*survivors)), gate.animate.set_fill(opacity=0.30), run_time=0.67)
        self.finish()


class S11Range(FilmScene):
    def construct(self):
        panels = strategy_panels()
        crab, eggs, family = strategy_animals()
        gate = survival_gate()
        environment = label("Environment", 0, -1.48, 28, RED)
        self.add(panels, crab, family, gate, environment)
        self.at("These are endpoints")
        self.play(FadeOut(gate), FadeOut(environment),
                  FadeOut(panels.left_head), FadeOut(panels.right_head), run_time=0.72)
        arrow = DoubleArrow(point(-5.90, -1.12), point(5.90, -1.12), buff=0,
                            color=GREY, stroke_width=5)
        self.play(ReplacementTransform(VGroup(panels.left_frame, panels.right_frame), arrow),
                  run_time=1.37)
        title = label("Reproductive strategies", 0, -1.77, 35)
        tag = scope_tag("Schematic", size=28, color=TEXT).move_to(point(5.48, -3.03))
        self.play(FadeIn(title), FadeIn(tag), run_time=0.60)
        self.at("One strategy makes")
        many = label("Many young\nLess care per young", -4.08, -2.45, 29, BLUE)
        clutch = eggs.copy().arrange_in_grid(5, 9, buff=0.088).scale(1.30)
        clutch.move_to(point(-0.63, 0.59))
        self.play(TransformFromCopy(eggs, clutch), run_time=1.67)
        self.at("less investment")
        self.play(FadeIn(many), run_time=0.93)
        self.at("The other makes")
        fewer = label("Fewer young\nMore care per young", 4.05, -2.45, 29, GOLD)
        mother, calf = family
        self.play(FadeOut(clutch), calf.animate.shift(LEFT * 0.08), run_time=1.01)
        self.at("with more care")
        self.play(FadeIn(fewer), mother.animate.shift(RIGHT * 0.05), run_time=0.85)
        self.at("Many species fall")
        self.play(LaggedStart(*(GrowFromCenter(s) for s in middle_species()), lag_ratio=0.35), run_time=1.70)
        self.finish()


class S12Fitness(FilmScene):
    def construct(self):
        gate = survival_gate(y=-0.20, width=3.68, height=2.20, opening=0.52)
        input_markers = VGroup(
            elephant(GOLD, 1.04).move_to(point(-1.00, 1.97)),
            elephant(TEAL, 1.04).move_to(point(1.00, 1.97)),
        )
        gate_tag = label("Survival and reproduction", 0, 2.88, 35)
        self.add(gate, input_markers)
        self.at("For selection")
        self.play(FadeIn(gate_tag), run_time=0.97)
        children = VGroup(*(offspring_dot(x, 1.24, color, 0.18)
                            for x, color in ((-0.56, GOLD), (0.50, TEAL))))
        self.at("count offspring")
        self.play(LaggedStart(*(GrowFromCenter(d) for d in children), lag_ratio=0.22), run_time=0.70)
        self.at("survive and reproduce")
        self.play(*(MoveAlongPath(d, segments([(d.get_x(), d.get_y()), (side * 0.26, -1.46),
                                              (side * 0.78, -1.66)], d.get_color()))
                    for d, side in zip(children, (-1, 1))), run_time=1.39, rate_func=linear)
        left = caption("Offspring left", size=36, color=GREEN, y=-2.42).move_to(point(0, -2.42))
        self.play(FadeIn(left), run_time=0.71)
        self.at("Strength effort")
        distractions = VGroup(*(boxed_label(name, TEXT, 34, fill_opacity=0.15)
                                for name in ("Strength", "Effort", "Need")))
        distractions.arrange(DOWN, buff=0.22).move_to(point(4.15, 0.47))
        self.play(LaggedStart(*(FadeIn(word) for word in distractions), lag_ratio=0.35), run_time=0.93)
        self.at("are not the score")
        self.play(FadeOut(distractions, shift=RIGHT * 0.43), run_time=1.28)
        self.at("The conditions decide")
        narrowed = survival_gate(y=-0.20, width=3.68, height=2.20, opening=0.34)
        narrowed.set_fill(opacity=0.60)
        self.play(Transform(gate, narrowed), run_time=1.22)
        self.at("an inherited variant")
        next_young = VGroup(*(offspring_dot(x, 1.24, color, 0.18)
                              for x, color in ((-0.88, GOLD), (-0.10, TEAL), (0.42, TEAL))))
        self.play(FadeIn(next_young), run_time=0.22)
        passing = (
            MoveAlongPath(d, segments([(d.get_x(), d.get_y()), (side * 0.09, -1.46),
                                       (side * 0.26, -1.66)], TEAL), rate_func=linear)
            for d, side in zip(next_young[1:], (-1, 1))
        )
        self.play(FadeOut(next_young[0], target_position=point(-0.85, -0.45)),
                  LaggedStart(*passing, lag_ratio=0.52), run_time=0.93, rate_func=linear)
        self.at("changes reproductive success")
        generation = boxed_label("Next generation", GREEN, 31, fill_opacity=0.13).move_to(point(4.53, -2.40))
        survivors = VGroup(children[0], next_young[1], next_young[2], children[1])
        new_row = survivors.copy().move_to(point(4.53, -1.61))
        self.play(TransformFromCopy(survivors, new_row), FadeIn(generation), run_time=0.80)
        self.finish()


class S13Rule(FilmScene):
    def construct(self):
        bars = compact_bars()
        gate, young, next_generation = evidence_filter()
        opening, input_row, output_row = evidence_filter(expanded=True)
        names, lines, lead, result = evidence_strands()
        self.add(opening)
        self.at("When inherited variations")
        self.play(LaggedStart(*(GrowFromCenter(d) for d in input_row), lag_ratio=0.24), run_time=1.11)
        self.at("affect reproductive success")
        self.play(LaggedStart(
            *(TransformFromCopy(d, target) for d, target in zip(input_row[1:], output_row)),
            FadeOut(input_row[0].copy(), target_position=point(-0.92, -0.72)),
            lag_ratio=0.11,
        ), run_time=1.88)
        self.at("populations change across")
        self.play(ReplacementTransform(opening, gate), ReplacementTransform(input_row, young),
                  ReplacementTransform(output_row, next_generation),
                  LaggedStart(*(GrowFromEdge(bar.fills, DOWN) for bar in bars), lag_ratio=0.25),
                  run_time=1.71)
        self.play(LaggedStart(*(FadeIn(VGroup(bar.shell, bar.heading, bar.readings)) for bar in bars),
                              lag_ratio=0.18), run_time=1.03)
        self.at("In Gorongosa")
        self.play(FadeIn(label("Gorongosa", -3.53, 2.78, 35)), run_time=0.72)
        for cue, name, line in zip(
            ("the trait pattern", "selective pressure", "survival difference", "and daughters"),
            names, lines,
        ):
            self.at(cue)
            self.play(FadeIn(name), Create(line), run_time=0.71)
        self.at("all support that")
        self.play(GrowArrow(lead), run_time=0.66)
        self.play(FadeIn(result), run_time=0.80)
        self.finish()


class S14Limits(FilmScene):
    def construct(self):
        bars = compact_bars()
        gate, young, next_generation = evidence_filter()
        names, lines, lead, result = evidence_strands()
        region_title = label("Gorongosa", -3.53, 2.78, 35)
        self.add(bars, gate, young, next_generation, names, lines, lead, result, region_title)
        frame = segments([(6.35, -2.64), (6.35, -3.18), (-6.35, -3.18), (-6.35, 3.18),
                          (6.35, 3.18), (6.35, -1.40)], GREY, 3)
        self.at("before and after data")
        highlights = VGroup(*(share_highlight(b) for b in bars[:2]))
        self.play(Create(highlights[0]), Create(highlights[1]),
                  *(b.gold.animate.set_fill(opacity=0.42) for b in bars[:2]), run_time=1.35)
        self.at("show a pattern")
        self.play(FadeOut(highlights), *(b.gold.animate.set_fill(opacity=0.83) for b in bars[:2]),
                  run_time=1.02)
        self.at("The selective pressure")
        self.play(gate.animate.set_fill(opacity=0.76), run_time=1.04)
        self.at("survival estimate")
        model_trials = VGroup(*(d.copy() for d in young[1:]))
        self.play(ReplacementTransform(model_trials, next_generation.copy().set_opacity(0.0)),
                  gate.animate.set_fill(opacity=0.30), run_time=1.39)
        self.at("chance comparison")
        comparison_label = label("Chance comparison", 0.60, 2.84, 28, BLUE)
        chance = chance_band(0.80, 1.95, bottom=1.47, height=2.80).set_fill(opacity=0.63)
        self.play(GrowFromEdge(chance, LEFT), FadeIn(comparison_label), run_time=0.86)
        self.at("and later daughters")
        daughter_outline = share_highlight(bars[2])
        self.play(Create(daughter_outline), bars[2].gold.animate.set_fill(opacity=0.37), run_time=0.87)
        self.at("selection explanation stronger")
        self.play(FadeOut(daughter_outline), lead.animate.set_stroke(width=7),
                  bars[2].gold.animate.set_fill(opacity=0.83),
                  result.box.animate.set_stroke(width=4).set_fill(opacity=0.33), run_time=1.64)
        self.at("Good evidence supports")
        self.play(Create(frame), run_time=1.44)
        evidence = label("Evidence", -5.19, 2.80, 31)
        self.play(swap(region_title, evidence, 0.77))
        self.at("keeping its limits")
        limits = label("Limits", 5.86, -2.00, 31)
        self.play(FadeIn(limits, shift=LEFT * 0.17), run_time=0.90)
        self.finish()


class S15Return(FilmScene):
    def construct(self):
        old = compact_bars()
        bars = measured_bars()
        self.add(old)
        self.at("Read the bars")
        self.play(*(FadeOut(VGroup(bar.heading, bar.readings)) for bar in old), run_time=0.40)
        self.play(*(ReplacementTransform(VGroup(a.shell, a.fills), VGroup(b.shell, b.fills))
                    for a, b in zip(old, bars)), run_time=0.86)
        time_arrow = timeline().shift(DOWN * 0.23)
        self.at("snapshots")
        self.play(*(FadeIn(VGroup(bar.heading, bar.readings)) for bar in bars),
                  GrowArrow(time_arrow), run_time=1.35)
        gates = poaching_filter(narrowed=True)
        self.at("Read the filter")
        self.play(Create(gates), run_time=0.75)
        self.at("as a comparison")
        paths = tracked_paths()
        self.play(Create(paths[0]), Create(paths[3]), run_time=1.12)
        self.at("not a promise")
        stopped = Line(point(-3.64, 1.02), point(-2.35, 1.12), buff=0, color=GOLD,
                       stroke_width=4, stroke_opacity=0.45)
        self.play(Create(stopped), run_time=0.80)
        self.at("Then ask whether")
        connectors = VGroup(*(
            Arrow(point(x, -2.54), point(x + 2.60, -2.54), buff=0, color=GREY, stroke_width=3)
            for x in (-3.78, 1.18)
        ))
        self.play(FadeOut(time_arrow), run_time=0.22)
        self.play(*(GrowArrow(arrow) for arrow in connectors),
                  *(bar.sample.animate.set_y(-2.54) for bar in bars), run_time=0.36)
        self.at("inherited differences changed")
        animals = VGroup(
            elephant(GOLD, 0.46).move_to(stopped.point_from_proportion(0.36)),
            elephant(TEAL, 0.46).move_to(point(TRACK_X[0], TRACK_Y[1])),
        )
        self.play(FadeIn(animals), run_time=0.60)
        self.play(FadeOut(animals[0], target_position=stopped.get_end(), scale=0.45),
                  animals[1].animate.move_to(point(TRACK_X[1], TRACK_Y[1])), run_time=1.18)
        self.at("who left the next")
        card = question_card(RETURN, y=-2.98, color=TEXT, size=33)
        self.play(FadeIn(card.question, shift=UP * 0.21), run_time=0.98)
        self.finish()


class S16End(EndCard):
    LINE = "When inherited variations affect reproductive success,\npopulations change across generations."
