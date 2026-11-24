"""Ames test • one laboratory bench, with word cues from audio/words.json.

Color map (from the patch-clamp film):
BLUE glassware and apparatus; GREY structure and reference marks;
PURPLE DNA and strain comparisons; YELLOW histidine and the active cue;
GREEN growing revertants; RED invalid inferences; ORANGE test compound
and its activated product; TEAL liver fraction and untreated controls;
GOLD historical dates and the prediction.
"""

from bp_parts import *
from bp_style import EndCard

PURPLE = "#B58CD9"
ORANGE = "#F29E4C"
AGAR = "#30494B"
BENCH_CARD = "#26323F"
QUESTION = "What does Compound X do?"
QUESTION_STYLE = {"y": 3.28, "size": 39}
COUNTS = ((125, 118, 130), (30, 28, 35), (240, 480, 950))
BASELINES = (120, 30, 120)
SERIES = ("TA100 −S9", "TA98 +S9", "TA100 +S9")
SERIES_COLORS = (BLUE, PURPLE, ORANGE)
STRAIN_X = (-3.35, 3.35)
SINGLE_CENTER = (0, -0.35, 0)
SINGLE_RADIUS = 2.58


def label(words, x, y, color=TEXT, size=32):
    return T(words, size, color).move_to([x, y, 0])


def schematic():
    return scope_tag(size=28, color=TEXT)


def dish(center=SINGLE_CENTER, radius=SINGLE_RADIUS, colonies=0):
    """Glass rim, agar, and the same deterministic field of specks at every scale."""
    p = np.array(center)
    rim = Circle(radius, color=BLUE, stroke_width=4, fill_color=AGAR, fill_opacity=1).move_to(p)
    inset = Circle(radius * 0.91, color=TEAL, stroke_width=2, stroke_opacity=0.55).move_to(p)
    shine = Arc(radius=radius * 0.955, start_angle=1.87, angle=0.91,
                arc_center=p, color=BLUE, stroke_width=5)
    rng = np.random.default_rng(31)
    haze = VGroup()
    for angle, distance in zip(rng.uniform(0, TAU, 21), rng.uniform(0.16, 0.83, 21)):
        spot = p + radius * distance * np.array([np.cos(angle), np.sin(angle), 0])
        haze.add(Dot(spot, radius=radius * 0.018, color=TEAL, fill_opacity=0.64))
    spots = [
        (-0.31, 0.17), (0.32, 0.38), (0.48, -0.44), (-0.54, -0.34),
        (-0.47, 0.53), (0.10, -0.44), (0.10, 0.60), (0.36, 0.02),
        (-0.05, -0.68), (-0.60, -0.07), (0.55, 0.20), (0.02, 0.06),
        (-0.25, -0.40), (0.61, -0.17), (0.25, -0.19),
    ]
    growth = VGroup()
    for i, (x, y) in enumerate(spots[:colonies]):
        spot = p + radius * np.array([x, y, 0])
        r = radius * (0.060 + 0.011 * (i % 3))
        growth.add(VGroup(
            Dot(spot, radius=r * 1.56, color=GREEN, fill_opacity=0.24),
            Dot(spot, radius=r, color=GREEN),
            Dot(spot + UP * r * 0.23 + LEFT * r * 0.18, radius=r * 0.26, color=TEXT),
        ))
    plate = VGroup(rim, inset, shine, haze, growth)
    plate.rim, plate.shine, plate.haze, plate.growth = rim, shine, haze, growth
    return plate


def glass_shimmer(plate):
    """A slow reflected-light shift across the agar and its glass rim."""
    pulse(plate.shine, base=5, amp=2, speed=2.1)
    shade = ManimColor(AGAR)
    lit = ManimColor("#496867")
    phase = 0.0

    def reflect(surface, dt):
        nonlocal phase
        phase += dt * 1.32
        surface.set_fill(interpolate_color(shade, lit, (1 - np.cos(phase)) / 2))

    plate.rim.add_updater(reflect)


def paired_dishes(left_n=0, right_n=0):
    return [dish((x, 0.50, 0), 1.68, colonies=n) for x, n in zip(STRAIN_X, (left_n, right_n))]


def drop(point, activated=False):
    color = ORANGE if activated else "#D1AD8E"
    outline = VMobject(fill_color=color, fill_opacity=1, stroke_width=0)
    outline.set_points_smoothly([UP * 0.34, RIGHT * 0.22 + DOWN * 0.06, DOWN * 0.25,
                                 LEFT * 0.22 + DOWN * 0.06, UP * 0.34])
    return outline.move_to(point)


def pipette(tip):
    """Tapered blue glass, as in the patch-clamp color map."""
    origin = np.array(tip)
    return Polygon(*[origin + np.array([x, y, 0]) for x, y in
                     [(-0.09, 0), (0.09, 0), (0.57, 1.11), (1.77, 1.75),
                      (1.48, 2.19), (0.23, 1.40)]],
                   color=BLUE, stroke_width=3, fill_color=BLUE, fill_opacity=0.25)


def vial(point):
    fill = RoundedRectangle(width=0.64, height=0.98, corner_radius=0.12,
                            color=TEAL, stroke_width=3, fill_color=TEAL, fill_opacity=0.48)
    cap = RoundedRectangle(width=0.72, height=0.24, corner_radius=0.07,
                           color=BLUE, stroke_width=2, fill_color=BLUE, fill_opacity=0.65)
    cap.next_to(fill, UP, buff=0.06)
    return VGroup(fill, cap).move_to(point)


def ladder(x, y=-2.0):
    """Abstract base-pair blocks in two rails, with brackets for groups of three."""
    rungs = VGroup()
    for i in range(9):
        rung = RoundedRectangle(width=0.43, height=0.49, corner_radius=0.07, stroke_width=0,
                                fill_color=(PURPLE, BLUE, TEAL)[i % 3], fill_opacity=1)
        rungs.add(rung.move_to([x + (i - 4) * 0.52, y, 0]))
    rails = VGroup(*[
        Line([x - 2.37, y + side * 0.32, 0], [x + 2.37, y + side * 0.32, 0],
             color=GREY, stroke_width=3)
        for side in (-1, 1)
    ])
    return VGroup(rails, rungs), rungs


def reading_brackets(rungs):
    result = VGroup()
    for group in range(0, len(rungs), 3):
        subset = rungs[group:group + 3]
        y = subset.get_bottom()[1] - 0.28
        x0, x1 = subset.get_left()[0], subset.get_right()[0]
        bracket = VMobject(stroke_color=YELLOW, stroke_width=3)
        bracket.set_points_as_corners([[x0, y + 0.10, 0], [x0, y, 0], [x1, y, 0], [x1, y + 0.10, 0]])
        result.add(bracket)
    return result


def chart():
    """Three dose groups on a common count axis. Every bar uses the supplied plate count."""
    field = RoundedRectangle(width=10.88, height=5.65, corner_radius=0.2,
                             fill_color=BENCH_CARD, fill_opacity=1, stroke_width=0)
    field.move_to([0.98, -0.045, 0])
    plot = Plot(box=(-3.46, 6.18, -1.80, 2.34), xr=(0, 10), yr=(0, 1130),
                yticks=[0, 500, 1000], size=28, color=TEXT)
    axis_label = label("Revertants per plate", -1.66, 2.52, size=28)
    dose = label("Dose increases within each group →", 1.30, -3.22, size=28)
    background_title = label("Background", -5.48, 3.27, TEXT, 28)
    backdrop = VGroup(field, plot, axis_label, background_title)
    plates = []
    for y, baseline, strain, color, colonies in [
        (1.41, 120, "TA100", BLUE, 4), (-1.57, 30, "TA98", PURPLE, 1),
    ]:
        plate = dish((-5.48, y, 0), 0.80, colonies)
        plates.append(VGroup(plate, label(strain, -5.48, y + 1.11, color, 28),
                             label(str(baseline), -5.48, y - 1.12, color, 30)))
    dashes, bars, values, names = [], [], [], []
    for index, (name, counts, baseline, color) in enumerate(zip(SERIES, COUNTS, BASELINES, SERIES_COLORS)):
        first = 0.85 + index * 3.25
        dashes.append(DashedLine(plot.pt(first - 0.58, baseline), plot.pt(first + 2.63, baseline),
                                 color=TEXT, stroke_width=2, dash_length=0.12).set_opacity(0.7))
        b, v = VGroup(), VGroup()
        for j, count in enumerate(counts):
            x = first + j * 1.05
            base = plot.pt(x, 0)
            height = plot.pt(x, count)[1] - base[1]
            b.add(Rectangle(width=0.76, height=height, stroke_width=0, fill_color=color, fill_opacity=1)
                  .move_to(base + UP * height / 2))
            v.add(label(str(count), base[0], -2.08, color, 28))
        bars.append(b)
        values.append(v)
        names.append(label(name, plot.pt(first + 1.05, 0)[0], -2.55, color, 30))
    return backdrop, dose, plates, dashes, bars, values, names


def chart_picture(parts):
    backdrop, dose, plates, dashes, bars, values, names = parts
    return VGroup(backdrop, dose, *plates, *dashes, *bars, *values, *names)


def chart_focus(parts, index):
    """A background highlight for the dose series currently being read."""
    backdrop, _, _, _, _, _, names = parts
    backdrop[0].set_z_index(-2)
    focus = RoundedRectangle(width=2.88, height=4.00, corner_radius=0.16, stroke_width=0,
                             fill_color="#496274", fill_opacity=0.8).set_z_index(-1)
    return focus.move_to([names[index].get_x(), 0.18, 0])


def proportion(n, total, center):
    width, height = 5.2, 0.52
    track = RoundedRectangle(width=width, height=height, corner_radius=0.15,
                             color=GREY, stroke_width=2, fill_color=BG, fill_opacity=1).move_to(center)
    inside = width - 0.16
    fill = RoundedRectangle(width=inside * n / total, height=height - 0.16, corner_radius=0.09,
                            stroke_width=0, fill_color=GREEN, fill_opacity=1)
    fill.align_to(track, LEFT).shift(RIGHT * 0.08).set_y(center[1])
    return track, fill


def history_plate(colonies=9):
    return dish((-3.36, -0.12, 0), 2.38, colonies)


def history_field():
    card = RoundedRectangle(width=6.12, height=4.4, corner_radius=0.23,
                            stroke_width=0, fill_color=BENCH_CARD, fill_opacity=1)
    return card.move_to([3.18, 0.10, 0])


def crossed_arrow(x, y):
    arrow = Arrow([x - 0.80, y, 0], [x + 0.80, y, 0], buff=0, color=GREY, stroke_width=4)
    slash = Line([x - 0.28, y - 0.31, 0], [x + 0.28, y + 0.31, 0], color=RED, stroke_width=5)
    return VGroup(arrow, slash)


class S01Hook(SpokenScene):
    def construct(self):
        plate = dish(colonies=5)
        growth = plate.growth
        plate.remove(growth)
        target = plate.copy()
        plate.scale(0.76).shift(LEFT * 0.85)
        tool = pipette([1.47, 1.18, 0])
        sample = drop([1.42, 0.81, 0])
        calendar = boxed_label("Years", color=GOLD, size=37, box=(2.18, 0.94))
        calendar.move_to([-4.96, 0.69, 0])
        pages = VGroup(*[Line(LEFT * (0.92 - i * 0.12), RIGHT * (0.92 - i * 0.12),
                              color=GOLD, stroke_width=3)
                         .move_to([-4.96, 0.04 - i * 0.20, 0]) for i in range(3)])
        self.add(plate, tool, sample, *reversed(list(pages)), calendar, schematic())
        self.at("take years")
        self.play(LaggedStart(*[FadeOut(page, shift=DOWN * 0.25) for page in pages], lag_ratio=0.33),
                  run_time=1.38)
        self.at("how can bacteria")
        mark = label("?", 0, 2.92, GOLD, 64)
        self.play(FadeOut(calendar), Transform(plate, target), FadeIn(mark), run_time=1.03)
        glass_shimmer(plate)
        self.at("screen a chemical")
        self.play(sample.animate.move_to([0.38, 0.34, 0]).scale(0.52),
                  FadeOut(tool, shift=UP * 0.27 + RIGHT * 0.30), run_time=1.38)
        self.at("in a few days")
        self.play(FadeOut(sample), FadeOut(mark), run_time=0.62)
        self.at("Bruce Ames turned")
        self.play(LaggedStart(*[GrowFromCenter(c) for c in growth], lag_ratio=0.36), run_time=3.12)
        self.finish()


class S02Title(TitleCard):
    LESSON = "The Ames Test"
    TITLE = "Catching Mutagens on a Bacterial Plate"

    def construct(self):
        plate = dish(colonies=5)
        glass_shimmer(plate)
        title = fit_text(self.TITLE, max_w=11.8, size=48, color=TEXT, font=TITLE_FONT)
        title.set_y(2.99)
        self.add(plate, schematic())
        self.play(FadeIn(title), run_time=0.52)
        self.wait(0.94)
        self.play(FadeOut(title), run_time=0.50)


class S03Revertants(SpokenScene):
    def construct(self):
        plate = dish(colonies=5)
        self.add(plate, schematic())
        self.at("test uses salmonella")
        self.play(FadeOut(plate.growth), run_time=0.35)
        self.remove(plate, plate.growth)
        plate.remove(plate.growth)
        self.add(plate)
        self.play(plate.animate.shift(LEFT * 1.81), run_time=1.00)
        glass_shimmer(plate)
        strain = label("Histidine-requiring\nSalmonella", 3.98, 0.55, BLUE, 33)
        self.at("cannot make the")
        self.play(FadeIn(strain), run_time=0.52)
        self.at("on a dish with")
        track = RoundedRectangle(width=3.42, height=0.42, corner_radius=0.12,
                                 color=YELLOW, fill_color=BG, fill_opacity=1, stroke_width=2)
        track.move_to([3.95, -0.13, 0])
        trace = label("Trace histidine", 3.95, 0.48, YELLOW)
        amount = Rectangle(width=3.22, height=0.24, stroke_width=0, fill_color=YELLOW, fill_opacity=1)
        amount.move_to(track)
        self.play(FadeOut(strain), FadeIn(track), FadeIn(amount), run_time=0.38)
        self.play(FadeIn(trace), run_time=0.36)
        self.at("cells divide")
        daughters = plate.haze.copy().shift(RIGHT * 0.10 + UP * 0.10)
        self.play(LaggedStart(*[TransformFromCopy(a, b) for a, b in zip(plate.haze, daughters)],
                             lag_ratio=0.08),
                  amount.animate.stretch(0.01, 0, about_edge=LEFT), run_time=1.72)
        self.at("only a new mutation")
        center = plate.get_center() + LEFT * 0.33 + UP * 0.33
        cell = Dot(center, color=GREEN, radius=0.13)
        self.play(Flash(cell, color=YELLOW, flash_radius=0.40, line_length=0.16),
                  FadeIn(cell), FadeOut(amount), run_time=0.90)
        self.at("restoring histidine synthesis")
        halo = Circle(0.22, color=GREEN, fill_color=GREEN, fill_opacity=0.24, stroke_width=2).move_to(cell)
        self.play(GrowFromCenter(halo), cell.animate.scale(1.29), run_time=1.26)
        self.at("lets a cell form")
        self.play(halo.animate.scale(2.25).set_stroke(width=0), cell.animate.scale(1.92),
                  run_time=1.73)
        revertant = label("Revertant", 3.95, 0.53, GREEN, 38)
        self.at("each colony is a")
        self.play(FadeOut(track), FadeOut(trace), run_time=0.38)
        self.play(FadeIn(revertant), run_time=0.48)
        self.at("marking one such")
        self.play(halo.animate.scale(1.18).set_fill(opacity=0.34), run_time=1.14)
        self.at("untreated dishes also")
        control = dish((3.89, -0.56, 0), 1.68, 3)
        self.play(FadeOut(revertant), run_time=0.30)
        self.play(FadeIn(control, shift=UP * 0.16), run_time=0.61)
        untreated = label("Untreated", 3.89, 1.66, TEAL)
        self.play(FadeIn(untreated), run_time=0.45)
        self.at("the spontaneous background")
        self.play(FadeIn(label("Spontaneous background", 3.89, -2.73, GREEN, 29)), run_time=0.54)
        self.finish()


class S04Strains(SpokenScene):
    def construct(self):
        source = dish((-1.81, -0.35, 0), 2.58, 1)
        control = dish((3.89, -0.56, 0), 1.68, 3)
        tag = schematic()
        self.add(source, control, tag)
        glass_shimmer(source)
        glass_shimmer(control)
        self.at("outside agents")
        token = drop([-4.80, 2.15, 0])
        self.play(FadeIn(token, shift=UP * 0.24), run_time=1.05)
        self.at("are mutagens")
        mutagen = label("Mutagens", -4.73, 2.88, ORANGE, 34)
        self.play(FadeIn(mutagen), token.animate.move_to([-3.54, 1.23, 0]), run_time=0.88)
        self.at("change DNA differently")
        self.play(FadeOut(token), FadeOut(mutagen), FadeOut(control), run_time=0.68)
        self.at("uses separate strains")
        left, right = paired_dishes(1, 1)
        self.play(ReplacementTransform(source, left), FadeIn(right, shift=RIGHT * 0.56), run_time=1.32)
        glass_shimmer(left)
        glass_shimmer(right)
        dna_left, rungs_left = ladder(STRAIN_X[0])
        dna_right, rungs_right = ladder(STRAIN_X[1])
        self.play(FadeIn(dna_left, shift=UP * 0.10), run_time=0.58)
        self.at("t a 100 reverts")
        ta100 = label("TA100", STRAIN_X[0], 2.67, BLUE, 36)
        self.play(FadeIn(ta100), run_time=0.45)
        self.at("swapping one base pair")
        self.play(rungs_left[4].animate.set_fill(ORANGE).shift(UP * 0.08), run_time=0.48)
        self.play(rungs_left[4].animate.shift(DOWN * 0.08), run_time=0.42)
        self.play(FadeIn(label("Base-pair swap", STRAIN_X[0], -2.98, PURPLE)), run_time=0.50)
        self.play(FadeIn(dna_right, shift=UP * 0.10), run_time=0.58)
        self.at("t a 98 reverts")
        ta98 = label("TA98", STRAIN_X[1], 2.67, PURPLE, 36)
        bracket = reading_brackets(rungs_right)
        self.play(FadeIn(ta98), FadeIn(bracket), run_time=0.72)
        self.at("adding or removing bases")
        remaining = VGroup(*rungs_right[:2], *rungs_right[3:])
        self.play(FadeOut(rungs_right[2], shift=UP * 0.28), run_time=0.42)
        self.play(rungs_right[3:].animate.shift(LEFT * 0.52), run_time=0.54)
        self.at("not in multiples")
        self.play(ReplacementTransform(bracket, reading_brackets(remaining)),
                  FadeIn(label("Frameshift", STRAIN_X[1], -2.98, PURPLE)), run_time=0.60)
        self.finish()


class S05S9(SpokenScene):
    def construct(self):
        left, right = paired_dishes(1, 1)
        self.add(left, right, schematic())
        glass_shimmer(left)
        glass_shimmer(right)
        pale = drop([-3.35, 2.00, 0])
        self.at("yet many carcinogens")
        self.play(FadeIn(pale, shift=UP * 0.38), run_time=0.90)
        self.play(pale.animate.move_to([-3.35, 0.25, 0]), run_time=1.82)
        self.at("benzopyrin binds")
        chem = label("Benzo[a]pyrene", -3.35, -1.72, ORANGE)
        self.play(FadeIn(chem), FadeOut(pale), run_time=0.64)
        liver = vial([1.11, 1.56, 0])
        next_drop = drop([0.70, 0.58, 0])
        self.at("after liver enzymes")
        self.play(FadeIn(liver, shift=RIGHT * 0.26), FadeIn(next_drop), run_time=0.63)
        self.at("oxidize it into")
        self.play(Transform(next_drop, drop([1.10, 0.52, 0], activated=True)),
                  liver.animate.rotate(-0.27), run_time=1.75)
        self.at("so dishes run")
        no_s9 = label("−S9", -3.35, 2.72, BLUE, 39)
        plus_s9 = label("+S9", 3.35, 2.72, TEAL, 39)
        self.play(FadeIn(no_s9), FadeIn(plus_s9), run_time=0.64)
        self.at("rat liver enzyme fraction")
        liver_label = label("S9 liver enzymes", 3.35, -1.72, TEAL)
        self.play(FadeIn(liver_label), liver.animate.rotate(0.27), run_time=0.57)
        self.play(next_drop.animate.move_to([3.35, 0.33, 0]), run_time=1.04)
        more = paired_dishes(1, 15)[1].growth[1:]
        self.at("a rising revertant count")
        self.play(FadeOut(next_drop), LaggedStart(*[GrowFromCenter(c) for c in more], lag_ratio=0.24),
                  run_time=2.50)
        self.at("flags a bacterial mutagen")
        flag = label("Bacterial mutagen", 0, -2.63, GREEN, 38)
        self.play(FadeIn(flag), run_time=0.54)
        self.at("human cancer")
        self.play(FadeIn(label("≠ human cancer risk", 0, -3.23, RED, 30)), run_time=0.48)
        self.finish()


class S06Predict(SpokenScene):
    def construct(self):
        parts = chart()
        backdrop, dose, plates, dashes, bars, values, names = parts
        left, right = paired_dishes(1, 15)
        self.add(left, right)
        self.at("test compound x")
        flat_left, flat_right = paired_dishes()
        self.play(Transform(left, flat_left), Transform(right, flat_right), run_time=0.25)
        self.play(Transform(left, plates[0][0].copy()), Transform(right, plates[1][0].copy()), run_time=0.78)
        self.remove(left, right)
        self.add(plates[0][0], plates[1][0])
        self.play(FadeIn(VGroup(*backdrop[:3])), run_time=0.36)
        self.at("three rising doses")
        self.play(FadeIn(dose), run_time=0.58)
        self.at("background is about")
        self.play(FadeIn(backdrop[3]), FadeIn(plates[0][1]), FadeIn(plates[1][1]), run_time=0.55)
        focus = [chart_focus(parts, i) for i in range(3)]
        self.at("120 in")
        self.play(FadeIn(plates[0][2]), Create(dashes[0]), FadeIn(focus[0]), run_time=1.05)
        self.play(FadeOut(focus[0]), Create(dashes[2]), FadeIn(focus[2]), run_time=0.85)
        self.at("30 in")
        self.play(FadeOut(focus[2]), FadeIn(plates[1][2]), Create(dashes[1]), FadeIn(focus[1]), run_time=1.25)
        self.at("without s9")
        self.play(FadeOut(focus[1]), FadeIn(focus[0]), FadeIn(names[0]), run_time=1.17)
        self.at("stays flat")
        self.play(LaggedStart(*[GrowFromEdge(bar, DOWN) for bar in bars[0]], lag_ratio=0.32),
                  FadeIn(values[0]), run_time=1.14)
        self.at("so does t")
        self.play(FadeOut(focus[0]), FadeIn(focus[1]), FadeIn(names[1]), run_time=0.85)
        self.play(LaggedStart(*[GrowFromEdge(bar, DOWN) for bar in bars[1]], lag_ratio=0.65),
                  FadeIn(values[1]), run_time=1.59)
        self.at("only t a 100")
        self.play(FadeOut(focus[1]), FadeIn(focus[2]), FadeIn(names[2]), run_time=1.46)
        for j, cue in enumerate(("240", "480", "950")):
            self.at(cue)
            self.play(GrowFromEdge(bars[2][j], DOWN), FadeIn(values[2][j]), run_time=0.68)
        self.at("what does x")
        self.play(FadeIn(question_card(QUESTION, **QUESTION_STYLE)), run_time=0.55)
        self.play(FadeOut(focus[2]), run_time=1.20)
        self.finish()


class S07Pause(PredictPause):
    QUESTION = QUESTION
    CARD = QUESTION_STYLE
    RING_AT = (6.35, -3.40, 0)
    SECONDS = 4.5

    def backdrop(self):
        return chart_picture(chart())

    def construct(self):
        self.add(self.backdrop(), question_card(self.QUESTION, **self.CARD))
        ring, countdown_run = countdown(self.SECONDS, center=self.RING_AT)
        ring[0].set_fill(GOLD, opacity=0.84)
        self.add(ring)
        self.play(countdown_run, ring[0].animate(run_time=self.SECONDS, rate_func=linear)
                  .set_fill(GOLD, opacity=0.05))
        self.finish()

    def finish(self):
        # The pause uses the exact supplied silence, without the spoken-scene tail.
        pass


class S08Answer(SpokenScene):
    def construct(self):
        parts = chart()
        world = chart_picture(parts)
        _, _, plates, _, bars, _, _ = parts
        carried_plate = plates[0][0]
        plates[0].remove(carried_plate)
        question = question_card(QUESTION, **QUESTION_STYLE)
        formula = label("Count / background", -1.84, 3.28, GOLD, 38)
        self.add(world, carried_plate, question)
        self.at("divide each count")
        focus = chart_focus(parts, 2)
        self.play(swap(question, formula, run_time=0.78), FadeIn(focus), run_time=0.78)
        column = RoundedRectangle(width=1.02, height=4.12, corner_radius=0.1, stroke_width=0,
                                  fill_color=BG, fill_opacity=0.82).set_z_index(-0.5)
        column.move_to([bars[2][0].get_x(), 0.27, 0])
        ratios = []
        for j, (cue, result_cue, result) in enumerate(zip(
                ("240 over", "480 is", "950 is"), ("is 2", "is 4", "about 8"), ("2×", "4×", "≈ 8×"))):
            value = COUNTS[2][j]
            expression = label(f"{value} / {BASELINES[2]}", 2.94, 3.27, TEXT, 30)
            answer = label(result, bars[2][j].get_x(), bars[2][j].get_top()[1] + 0.21, ORANGE, 29)
            self.at(cue)
            if j == 0:
                self.play(FadeIn(expression), FadeIn(column), run_time=0.50)
            else:
                self.play(FadeOut(readout), bars[2][j - 1].animate.set_fill(ORANGE), run_time=0.19)
                self.play(FadeIn(expression), column.animate.set_x(bars[2][j].get_x()), run_time=0.30)
            self.at(result_cue)
            result_display = T(result if j == 2 else f"= {result}", 30, ORANGE)
            result_display.next_to(expression, RIGHT, buff=0.14)
            self.play(FadeIn(answer), FadeIn(result_display),
                      bars[2][j].animate.set_fill(YELLOW), run_time=0.43)
            readout = VGroup(expression, result_display)
            ratios.append(answer)
        self.at("the rise needs")
        plate = dish((-3.14, -0.14, 0), 2.36, 9)
        enzyme = vial([0.50, 1.19, 0])
        self.play(FadeOut(world), FadeOut(formula), FadeOut(focus), FadeOut(column), FadeOut(readout),
                  *[FadeOut(r) for r in ratios], run_time=0.39)
        self.play(ReplacementTransform(carried_plate, plate), FadeIn(enzyme), FadeIn(schematic()), run_time=0.86)
        glass_shimmer(plate)
        self.play(FadeIn(label("TA100", -3.14, 2.70, BLUE, 36)),
                  FadeIn(label("S9", 0.50, 2.12, TEAL, 34)), run_time=0.43)
        self.at("a metabolite acts")
        product = drop([2.42, 0.48, 0], activated=True)
        self.play(FadeIn(product, shift=RIGHT * 0.31), run_time=0.85)
        metabolite = label("Metabolite", 3.66, 1.04, ORANGE, 36)
        self.play(FadeIn(metabolite), run_time=0.55)
        self.play(product.animate.move_to([-1.46, -0.61, 0]), run_time=0.63)
        self.at("shows no detectable")
        limit = label("X alone\nNo detectable effect", 3.69, -1.18, BLUE, 31)
        untreated_x = drop([1.05, -1.16, 0])
        self.play(FadeIn(limit), FadeIn(untreated_x), FadeOut(product), run_time=0.66)
        self.at("a 100 reverts by")
        dna, rungs = ladder(3.64, -0.76)
        self.play(FadeOut(limit), FadeOut(untreated_x), run_time=0.36)
        self.play(FadeIn(dna, shift=UP * 0.13), run_time=0.57)
        self.at("that metabolite causes")
        self.play(rungs[4].animate.set_fill(ORANGE), run_time=0.93)
        self.play(FadeIn(label("Base-pair substitutions", 3.59, -1.77, PURPLE, 32)), run_time=0.57)
        self.finish()


class S09Limits(SpokenScene):
    def construct(self):
        parts = chart()
        world = chart_picture(parts)
        backdrop = parts[0]
        field = backdrop[0]
        background_focus = RoundedRectangle(width=1.86, height=5.84, corner_radius=0.16,
                                             stroke_width=0, fill_color="#496274", fill_opacity=0.8)
        background_focus.move_to([-5.48, -0.18, 0]).set_z_index(-1)
        no_s9, ta98_s9, ta100_s9 = [chart_focus(parts, i) for i in range(3)]
        backdrop.remove(field)
        self.add(field, world)
        checklist = VGroup(*[
            label(words, x, 3.26, GOLD, 30)
            for words, x in (("1  Background", -2.55), ("2  Dose", 0.14), ("3  Strains", 2.18), ("4  ±S9", 4.35))
        ])
        self.at("background")
        self.play(FadeIn(checklist[0]), FadeIn(background_focus), run_time=0.26)
        self.at("dose response")
        self.play(FadeIn(checklist[1]), FadeIn(ta100_s9), run_time=0.42)
        self.at("strains and")
        self.play(FadeIn(checklist[2]), FadeOut(background_focus), FadeIn(ta98_s9), run_time=0.42)
        self.at("and s9")
        self.play(FadeIn(checklist[3]), FadeIn(no_s9), run_time=0.42)
        panels = TwoPanel("Positive result", "Negative result", colors=(GREEN, BLUE),
                          top=2.83, bottom=-2.87, width=12.45, size=35)
        left, right = [dish((x, 0.55, 0), 1.46, n) for x, n in
                       ((panels.area("left")[0][0], 15), (panels.area("right")[0][0], 0))]
        self.at("a positive shows")
        self.play(FadeOut(field), FadeOut(world), FadeOut(checklist),
                  FadeOut(VGroup(no_s9, ta98_s9, ta100_s9)), run_time=0.41)
        self.play(FadeIn(panels.left_frame), FadeIn(panels.left_head), FadeIn(left), FadeIn(schematic()), run_time=0.80)
        glass_shimmer(left)
        mutation = label("Mutates bacteria", left.get_x(), -1.30, GREEN)
        self.play(FadeIn(mutation), run_time=0.48)
        self.at("cancer risk in people")
        self.play(FadeIn(crossed_arrow(left.get_x() - 1.58, -2.19)),
                  FadeIn(label("Human cancer", left.get_x() + 0.64, -2.19, TEXT, 29)), run_time=0.68)
        self.at("a negative never")
        self.play(FadeIn(panels.right_frame), FadeIn(panels.right_head), FadeIn(right), run_time=0.82)
        glass_shimmer(right)
        badge = label("Safe", right.get_x() + 0.58, -1.36, TEXT)
        self.play(FadeIn(crossed_arrow(right.get_x() - 1.17, -1.36)), FadeIn(badge), run_time=0.58)
        self.at("without mutating dna")
        route = label("Non-mutagenic routes", right.get_x(), -2.23, BLUE, 29)
        self.play(FadeIn(route, shift=UP * 0.15), run_time=0.74)
        self.at("through processes bacteria lack")
        self.play(Indicate(route, color=TEXT, scale_factor=1.03), run_time=0.93)
        self.finish()


class S10UnlockedA(SpokenScene):
    def construct(self):
        plate = history_plate()
        field = history_field()
        enzyme = vial([-0.68, 1.70, 0])
        self.add(plate, field, schematic())
        glass_shimmer(plate)
        self.at("once liver extract")
        self.play(FadeIn(enzyme, shift=DOWN * 0.28), run_time=0.78)
        self.play(enzyme.animate.rotate(0.33).shift(LEFT * 0.66), run_time=1.35)
        self.play(enzyme.animate.rotate(-0.33).shift(RIGHT * 0.66), run_time=0.92)
        self.at("in 1973")
        year = label("1973", 3.19, 1.62, GOLD, 47)
        self.play(FadeIn(year), run_time=0.54)
        self.at("ames and colleagues")
        author = label("Ames et al.", 3.19, 0.94, TEXT, 35)
        self.play(FadeIn(author), run_time=0.51)
        self.at("18 tested carcinogens")
        total = label("18 tested carcinogens", 3.18, 0.05, TEXT, 33)
        self.play(FadeIn(total), run_time=0.59)
        self.at("into frameshift mutagens")
        finding = label("↓\nFrameshift mutagens", 3.18, -1.00, PURPLE, 33)
        self.play(FadeIn(finding), Indicate(plate.growth, color=GREEN, scale_factor=1.05), run_time=1.08)
        self.at("in 1975")
        new_year = label("1975", 3.19, 1.62, GOLD, 47)
        self.play(FadeOut(total), FadeOut(finding), FadeOut(author), run_time=0.43)
        self.play(swap(year, new_year, run_time=0.55))
        self.at("joyce mccann and")
        who = label("McCann et al.", 3.19, 0.94, TEXT, 35)
        track, fill = proportion(156, 174, [3.19, -0.76, 0])
        self.play(FadeIn(who), FadeIn(track), run_time=0.60)
        self.at("156 of 174")
        count = label("156 of 174", 3.19, 0.03, GREEN, 40)
        self.play(FadeIn(count), GrowFromEdge(fill, LEFT), run_time=2.52)
        self.at("in their tested set")
        self.play(FadeIn(label("Mutagenic in tested set", 3.19, -1.48, TEXT, 29)), run_time=0.55)
        self.finish()


class S11UnlockedB(SpokenScene):
    def construct(self):
        plate = history_plate()
        field = history_field()
        enzyme = vial([-0.68, 1.70, 0])
        self.add(plate, field, enzyme, schematic())
        glass_shimmer(plate)
        bottle = vial([1.48, 0.16, 0]).scale(0.78).set_color(PURPLE)
        self.at("the assay soon")
        self.play(FadeOut(enzyme), FadeIn(bottle, shift=LEFT * 0.43), run_time=1.17)
        self.at("in 1975")
        year = label("1975", 3.20, 1.62, GOLD, 47)
        self.play(FadeIn(year), run_time=0.61)
        self.at("kammen and")
        hair = label("Hair-dye formulations", 3.40, 0.99, TEXT, 31)
        track, fill = proportion(150, 169, [3.19, -0.85, 0])
        self.play(FadeIn(hair), FadeIn(track), run_time=0.63)
        self.at("150 of 169")
        stat = label("150 of 169", 3.99, 0.18, GREEN, 38)
        self.play(FadeIn(stat, run_time=0.50), GrowFromEdge(fill, LEFT, run_time=2.0))
        self.at("formulations mutagenic")
        positive = label("Mutagenic in the assay", 3.19, -1.53, TEXT, 28)
        self.play(FadeIn(positive), run_time=0.57)
        self.at("in 1978")
        year2 = label("1978", 3.20, 1.62, GOLD, 47)
        self.play(FadeOut(bottle), FadeOut(hair), FadeOut(stat), FadeOut(track), FadeOut(fill),
                  FadeOut(positive), run_time=0.44)
        self.play(swap(year, year2, run_time=0.48))
        pan = Circle(0.49, color=GREY, fill_color=BG, fill_opacity=1, stroke_width=4).move_to([2.87, -0.30, 0])
        handle = Line([3.31, -0.48, 0], [4.11, -0.81, 0], color=GREY, stroke_width=9)
        food = VGroup(*[Dot([2.87 + x, -0.30 + y, 0], radius=0.07, color=ORANGE)
                        for x, y in [(-0.18, 0.14), (0.06, 0.14), (-0.08, -0.04), (0.21, -0.04),
                                     (0.05, -0.24), (-0.24, -0.13)]])
        skillet = VGroup(handle, pan, food)
        self.at("and colleagues found")
        author = label("Commoner et al.", 3.19, 0.89, TEXT, 33)
        self.play(FadeIn(skillet, shift=UP * 0.19), FadeIn(author), run_time=0.69)
        self.at("cooked ground beef")
        beef = label("Mutagens in cooked\nground beef", 3.19, -1.46, ORANGE, 30)
        self.play(FadeIn(beef), run_time=0.68)
        self.at("each dish flags")
        self.play(FadeOut(field), FadeOut(year2), FadeOut(author), FadeOut(skillet), FadeOut(beef), run_time=0.44)
        self.play(plate.animate.move_to(SINGLE_CENTER).scale(1.07), run_time=1.12)
        rule = caption("Bacterial mutation ≠ human cancer risk", size=35, color=TEXT, y=-3.31).set_x(0)
        self.at("human cancer risk")
        self.play(FadeIn(rule), Indicate(plate.growth, color=GREEN, scale_factor=1.07), run_time=0.98)
        self.finish()


class S12End(EndCard):
    LINE = "Revertants above background flag bacterial mutagens, not human cancer risk."
