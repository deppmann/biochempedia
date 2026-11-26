"""One DNA sample, four views, and the evidence that constrained its structure.

COLOR MAP: blue bases, grey backbones and frames, yellow question lens and
differences, green visible or supported features, orange omissions and limits,
purple evidence. Every view is a schematic made of blocks, bars or cards.
"""

from bp_parts import *


PURPLE = "#B58CD9"
ORANGE = "#F29E4C"
SLATE = "#303A4A"
PAIR_X = 0.65
PAIR_Y = -0.20
SAMPLE_LEFT = (-5.15, 0.05)
RULE = "Choose DNA models by the question; every model leaves features out."
PREDICTION = "Which bases face each other?"
VIEWS = ("pairing", "shape", "order", "occupied space")
VIEW_CENTERS = ((-4.55, 1.44), (4.55, 1.44), (-4.55, -1.63), (4.55, -1.63))
SAMPLE_BASES = "AGT"
PARTNER_BASES = "TCA"


def xy(x, y):
    return np.array([x, y, 0.0])


def label(text, at, size=32, color=TEXT):
    return T(text, size, color, weight=BOLD).move_to(xy(*at))


def panel(width, height, at, color=GREY, fill=SLATE, radius=0.16):
    return RoundedRectangle(
        width=width, height=height, corner_radius=radius,
        stroke_color=color, stroke_width=2.5, fill_color=fill, fill_opacity=1,
    ).move_to(xy(*at))


def card(text, at, width, height, color=GREY, size=30):
    box = boxed_label(text, color, size, box=(width, height), min_size=28, pad=0.21)
    box.box.set_fill(SLATE, opacity=1)
    box.label.set_color(TEXT if color == GREY else color).set_z_index(2)
    return box.move_to(xy(*at))


def scope():
    return scope_tag(size=28, color=TEXT)


def sample_box(at=(0, 0), large=True):
    width, height = (3.25, 4.75) if large else (2.65, 2.55)
    shell = panel(width, height, at)
    seam_y = at[1] + 0.28 * height
    seam = Line(xy(at[0] - width / 2 + 0.23, seam_y),
                xy(at[0] + width / 2 - 0.23, seam_y), color=GREY, stroke_width=2)
    title = label("DNA sample", at, 36 if large else 30)
    return VGroup(shell, seam, title)


def lens(at, radius=0.32):
    center = xy(*at)
    ring = Circle(radius=radius, color=YELLOW, stroke_width=6).move_to(center)
    diagonal = (RIGHT + DOWN) / np.sqrt(2)
    handle = Line(center + diagonal * radius, center + diagonal * (radius + 0.22),
                  color=YELLOW, stroke_width=6)
    return VGroup(ring, handle)


def visit(mob, at, **kwargs):
    return mob.animate(**kwargs).shift(xy(*at) - mob[0].get_center())


def opening_world(question_at=(0, 2.88)):
    frames = VGroup(*[panel(3.96, 1.76, at).set_z_index(-1) for at in VIEW_CENTERS])
    names = VGroup(*[label(name, (x, y + 1.18), 31) for name, (x, y) in zip(VIEWS, VIEW_CENTERS)])
    return sample_box(), frames, names, lens(question_at), scope()


def base_block(letter, at, width=1.48, height=0.88, size=40):
    box = RoundedRectangle(width=width, height=height, corner_radius=0.075,
                           stroke_color=BLUE, stroke_width=2.5,
                           fill_color="#24546A", fill_opacity=1)
    return VGroup(box, T(letter, size, TEXT, weight=BOLD).set_z_index(2)).move_to(xy(*at))


def ladder(at=(PAIR_X, PAIR_Y), compact=False):
    x, y = at
    if compact:
        rail_x, rail_w, rail_h, block_x, block_w, block_h, step, size = (
            0.85, 0.085, 1.58, 0.39, 0.66, 0.42, 0.50, 28
        )
    else:
        rail_x, rail_w, rail_h, block_x, block_w, block_h, step, size = (
            1.76, 0.22, 4.74, 0.79, 1.48, 0.88, 1.40, 42
        )
    rails = VGroup(*[
        Rectangle(width=rail_w, height=rail_h, stroke_width=0, fill_color=GREY, fill_opacity=1)
        .move_to(xy(x + s * rail_x, y)) for s in (-1, 1)
    ])
    rows = VGroup(*[
        VGroup(base_block(a, (x - block_x, y + j * step), block_w, block_h, size),
               base_block(b, (x + block_x, y + j * step), block_w, block_h, size))
        for j, (a, b) in zip((1, 0, -1), zip(SAMPLE_BASES, PARTNER_BASES))
    ])
    world = VGroup(rails, rows)
    world.rails, world.rows = rails, rows
    return world


def letter_strip(at, sequence=SAMPLE_BASES, compact=False):
    w, h, gap, size = (0.72, 0.58, 0.13, 32) if compact else (1.48, 1.04, 0.25, 44)
    return VGroup(*[base_block(ch, (0, 0), w, h, size) for ch in sequence]).arrange(
        RIGHT, buff=gap
    ).move_to(xy(*at))


def shape_card(at, compact=False):
    w, h, size = (3.64, 1.36, 29) if compact else (5.35, 3.95, 48)
    return card("Double-helix\nribbon model", at, w, h, size=size)


def space_card(at, compact=False):
    x, y = at
    w, h = (3.64, 1.46) if compact else (5.6, 3.9)
    box = panel(w, h, at)
    outline = [(-0.93, -0.42), (-0.92, 0.22), (-0.55, 0.67), (-0.09, 0.54),
               (0.32, 0.72), (0.86, 0.49), (0.93, -0.23), (0.70, -0.65),
               (0.21, -0.65), (-0.30, -0.50), (-0.68, -0.66)]
    body = Polygon(*[xy(x + px * (w / 2 - 0.15), y + py * (h / 2 - 0.08)) for px, py in outline],
                   stroke_width=0, fill_color="#556376", fill_opacity=1)
    title = label("Space occupied", at, 28 if compact else 42)
    world = VGroup(box, body, title)
    world.box, world.body, world.title = box, body, title
    return world


def twist_dial(tracker, at):
    gauge = dial(tracker, xy(*at), radius=1.78, label="Twist", color=YELLOW)
    gauge.remove(gauge[3])
    return gauge


def question_marker(name):
    return label(name, (-2.42, 2.67), 33, YELLOW)


def predict_world():
    return (
        sample_box((0, 0.25), large=False),
        ladder((-4.55, 0.15), compact=True),
        shape_card((4.55, 1.53), compact=True),
        letter_strip((0, -1.81), compact=True),
        space_card((4.55, -0.65), compact=True),
        lens((0, 2.30), 0.40),
        scope(),
    )


def prediction_card():
    return question_card(PREDICTION, y=-3.06, size=38, color=YELLOW).set_z_index(2)


def hold_panel(question):
    return panel(question.width + 1.35, 1.02, (-0.5, -3.06), YELLOW).set_z_index(1)


def highlighted(row, color=GREEN):
    return [block[0].animate.set_stroke(color, width=5).set_fill(
        "#365642" if color == GREEN else "#66532D", opacity=1
    ) for block in row]


def evidence(text, at, width=3.1):
    return card(text, at, width, 0.75, PURPLE)


def tested_model():
    model = ladder((0, -0.40))
    directions = VGroup(
        Arrow(xy(-2.20, 1.72), xy(-2.20, -2.52), buff=0, color=GREY,
              stroke_width=4, max_tip_length_to_length_ratio=0.07),
        Arrow(xy(2.20, -2.52), xy(2.20, 1.72), buff=0, color=GREY,
              stroke_width=4, max_tip_length_to_length_ratio=0.07),
    )
    return model, directions


def structure_track():
    border = panel(8.24, 5.30, (1.99, -0.05))
    heading = label("Structure models", (1.99, 2.24), 32)
    return border, heading


class S00Hook(SpokenScene, TitleCard):
    TITLE = "Which Picture of DNA Should You Trust?"
    LESSON = "How the DNA Model Was Built"

    def construct(self):
        sample, frames, names, glass, tag = opening_world(VIEW_CENTERS[0])
        self.add(tag, sample[0], sample[1])
        self.at("Several pictures")
        self.play(LaggedStart(*[GrowFromCenter(f) for f in frames], lag_ratio=0.24), run_time=2.25)
        self.play(LaggedStart(*[FadeIn(n) for n in names], lag_ratio=0.19), run_time=1.25)
        self.at("Which one should")
        self.play(FadeIn(glass), frames[0].animate.set_fill("#53503C", 1), run_time=0.64)
        self.play(visit(glass, VIEW_CENTERS[1], path_arc=-0.28),
                  frames[0].animate.set_fill(SLATE, 1), frames[1].animate.set_fill("#53503C", 1),
                  run_time=1.41)
        self.at("The answer changes")
        self.play(visit(glass, VIEW_CENTERS[3]), frames[1].animate.set_fill(SLATE, 1),
                  frames[3].animate.set_fill("#53503C", 1), run_time=1.17)
        self.play(visit(glass, VIEW_CENTERS[2], path_arc=-0.33), frames[3].animate.set_fill(SLATE, 1),
                  frames[2].animate.set_fill("#53503C", 1), run_time=1.53)
        self.at("Keep one short sample")
        self.play(FadeIn(sample[2]), frames[2].animate.set_fill(SLATE, 1),
                  sample[1].animate.set_stroke(YELLOW, width=4), run_time=0.73)
        self.play(FadeOut(glass), run_time=0.35)
        glass = lens((0, 2.88))
        self.play(FadeIn(glass), sample[1].animate.set_stroke(GREY, width=2), run_time=1.0)
        self.finish()


class S01Title(TitleCard):
    TITLE = S00Hook.TITLE
    LESSON = S00Hook.LESSON

    def construct(self):
        sample, frames, names, glass, tag = opening_world()
        title = fit_text(self.TITLE, max_w=11.8, size=47, font=TITLE_FONT).move_to(xy(0, 3.36))
        self.add(sample, frames, names, glass, tag)
        self.play(FadeOut(glass), run_time=0.20)
        self.play(FadeIn(title, shift=UP * 0.10), run_time=0.56)
        self.wait(self.narration_s - self.elapsed())


class S02ModelTool(SpokenScene):
    def construct(self):
        sample, frames, names, _, tag = opening_world()
        self.add(sample, frames, names, tag)
        tool = panel(8.0, 4.70, (2.10, -0.23))
        handle = Arc(radius=0.69, start_angle=0, angle=PI, color=GREY, stroke_width=6)
        handle.move_to(xy(2.10, 2.46))
        model = card("MODEL", (2.02, 0.29), 3.31, 1.5, BLUE, 46)
        small_sample = sample_box(SAMPLE_LEFT, large=False)
        glass = lens((5.24, 0.29), 0.42)
        self.at("A scientific model")
        self.play(FadeOut(frames), FadeOut(names), run_time=0.42)
        self.play(Transform(sample, small_sample), run_time=0.82)
        self.play(GrowFromCenter(tool), Create(handle), run_time=1.13)
        self.play(FadeIn(model[0], shift=RIGHT * 1.1), run_time=0.55)
        self.play(FadeIn(model[1]), run_time=0.42)
        self.at("It helps explain")
        self.play(FadeIn(glass), model.animate.shift(RIGHT * 0.55), run_time=1.05)
        self.play(visit(glass, (4.42, 0.29)), model.animate.move_to(xy(2.02, 0.29)),
                  run_time=1.72)
        self.at("It is a tool")
        self.play(handle.animate.set_stroke(YELLOW, width=6), run_time=0.65)
        self.at("not a perfect copy")
        self.play(model.animate.shift(UP * 0.64), visit(glass, (4.42, 0.93)), run_time=0.88)
        shows = card("Shows", (0.28, -1.27), 3.26, 1.33, GREEN, 34)
        omits = card("Leaves out", (3.82, -1.27), 3.26, 1.33, ORANGE, 34)
        shows.box.set_fill("#365642", 1)
        omits.box.set_fill("#66452F", 1)
        self.at("has a job", lead=0.89)
        self.play(GrowFromEdge(shows.box, UP), run_time=0.64)
        self.play(FadeIn(shows.label), run_time=0.41)
        self.at("a limit", lead=0.37)
        self.play(GrowFromEdge(omits.box, UP), run_time=0.61)
        self.play(FadeIn(omits.label), run_time=0.36)
        self.finish()


class S03Ladder(SpokenScene):
    def construct(self):
        self.add(sample_box(SAMPLE_LEFT, large=False), scope())
        glass = lens((-3.80, 2.67))
        pairing = question_marker("Pairing")
        model = card("MODEL", (PAIR_X, PAIR_Y), 3.20, 1.4, BLUE, 43)
        self.add(model)
        self.at("Ask which bases")
        self.play(FadeIn(glass, shift=LEFT * 0.22), run_time=0.65)
        self.play(FadeIn(pairing), run_time=0.55)
        lad = ladder()
        self.at("A flat ladder")
        self.play(FadeOut(model[1]), run_time=0.33)
        self.play(ReplacementTransform(model[0], lad.rails), run_time=1.12)
        self.at("Labeled base blocks")
        self.play(LaggedStart(*[FadeIn(row, scale=0.78) for row in lad.rows], lag_ratio=0.48), run_time=2.95)
        self.at("Pairing is clear", lead=0.60)
        self.play(LaggedStart(*[AnimationGroup(*highlighted(row)) for row in lad.rows], lag_ratio=0.29),
                  run_time=1.09)
        mask = card("Twist and atoms\nleft out", (4.73, -0.20), 3.43, 4.27, ORANGE, 33)
        self.at("but the twist", lead=0.03)
        self.play(GrowFromEdge(mask.box, RIGHT), run_time=0.70)
        self.play(FadeIn(mask.label), run_time=0.45)
        self.finish()


class S04Letters(SpokenScene):
    def construct(self):
        lad, glass = ladder(), lens((-3.80, 2.67))
        for row in lad.rows:
            for base in row:
                base[0].set_stroke(GREEN, width=5).set_fill("#365642", 1)
        pairing = question_marker("Pairing")
        old = card("Twist and atoms\nleft out", (4.73, -0.20), 3.43, 4.27, ORANGE, 33)
        self.add(sample_box(SAMPLE_LEFT, large=False), lad, glass, pairing, old, scope())
        self.at("Ask for base order")
        self.play(swap(pairing, question_marker("Order"), 0.85), FadeOut(old),
                  visit(glass, (-4.08, 2.67)), run_time=0.85)
        strip = letter_strip((PAIR_X, 0.66))
        strand = [row[0] for row in lad.rows]
        self.at("The ladder folds")
        self.play(FadeOut(lad.rails), *[FadeOut(row[1], shift=RIGHT * 0.24) for row in lad.rows],
                  run_time=0.76)
        self.play(strand[0].animate.shift(LEFT * 1.29), strand[2].animate.shift(RIGHT * 2.52),
                  run_time=0.61)
        self.play(*(ReplacementTransform(src, dst) for src, dst in zip(strand, strip)),
                  run_time=1.37)
        comparison = letter_strip((PAIR_X, -0.76), sequence="ACT")
        compare_label = place_label(T("Comparison sequence", 30, TEXT), comparison, dirs=(DOWN,), buff=0.28)
        self.at("Comparing positions")
        self.play(FadeIn(comparison, shift=UP * 0.33), run_time=0.67)
        self.play(FadeIn(compare_label), run_time=0.53)
        self.play(LaggedStart(*[AnimationGroup(*highlighted((strip[i], comparison[i]), color))
                                for i, color in enumerate((GREEN, YELLOW, GREEN))], lag_ratio=0.40),
                  run_time=1.18)
        mask = panel(2.89, 4.27, (5.03, -0.20), ORANGE, radius=0.14)
        mask_text = VGroup(T("Shape, size,", 28, ORANGE),
                           T("partner strand", 28, ORANGE),
                           T("left out", 28, ORANGE)).arrange(DOWN, buff=0.14).move_to(mask)
        mask_text.set_z_index(2)
        self.at("Shape size")
        self.play(GrowFromEdge(mask, RIGHT), run_time=1.10)
        self.play(FadeIn(mask_text), run_time=0.64)
        self.finish()


class S05ShapeSpace(SpokenScene):
    def construct(self):
        tag = scope()
        strip = letter_strip((PAIR_X, 0.66))
        for base, color in zip(strip, (GREEN, YELLOW, GREEN)):
            base[0].set_stroke(color, width=5).set_fill("#365642" if color == GREEN else "#66532D", 1)
        self.add(tag, strip)
        ribbon = shape_card((-3.16, -0.27))
        glass = lens((-4.29, 2.62))
        shape = label("Shape", (-3.05, 2.62), 33, YELLOW)
        twist = ValueTracker(0.11)
        gauge = twist_dial(twist, (3.40, -0.44))
        self.at("A ribbon model")
        self.play(FadeOut(strip), GrowFromCenter(ribbon.box), FadeIn(glass), run_time=0.65)
        self.play(FadeIn(ribbon.label), Create(gauge[0]), FadeIn(gauge[1:]), run_time=0.67)
        self.at("a shape question", lead=0.40)
        self.play(FadeIn(shape), run_time=0.50)
        self.at("showing coiling", lead=0.48)
        self.play(twist.animate.set_value(0.87), ribbon.animate.rotate(0.075), run_time=1.65)
        solid = space_card((3.09, -0.08))
        small_shape = shape_card((-4.40, 0.35), compact=True)
        self.at("space -filling model", lead=0.71)
        self.play(FadeOut(gauge), FadeOut(shape), run_time=0.43)
        self.play(Transform(ribbon, small_shape), visit(glass, (1.22, 2.62)),
                  GrowFromCenter(solid.box), run_time=0.95)
        occupied = label("Occupied space", (3.61, 2.62), 33, YELLOW)
        self.at("shows occupied", lead=0.52)
        self.play(GrowFromCenter(solid.body), FadeIn(occupied), run_time=1.00)
        self.play(FadeIn(solid.title), run_time=0.46)
        small_solid = space_card((4.40, 0.35), compact=True)
        order = letter_strip((0, 0.35), compact=True)
        masks = VGroup(card("Order hidden", (-4.40, -1.10), 3.27, 0.72, ORANGE),
                       card("Order hidden", (4.40, -1.10), 3.27, 0.72, ORANGE))
        self.at("Neither is best")
        self.play(FadeOut(occupied), FadeOut(glass), Transform(VGroup(*solid), small_solid),
                  run_time=0.90)
        self.play(FadeIn(order), LaggedStart(*(FadeIn(m, shift=UP * 0.13) for m in masks), lag_ratio=0.23),
                  run_time=0.92)
        self.finish()


class S06Predict(SpokenScene):
    def construct(self):
        sample, lad, shape, strip, solid, glass, tag = predict_world()
        old_shape, old_strip, old_solid = (
            shape_card((-4.40, 0.35), compact=True), letter_strip((0, 0.35), compact=True),
            space_card((4.40, 0.35), compact=True),
        )
        # The right-hand options move aside when the open question lens arrives.
        shape.shift(LEFT * 0.88)
        solid.shift(LEFT * 0.88)
        old_masks = VGroup(card("Order hidden", (-4.40, -1.10), 3.27, 0.72, ORANGE),
                           card("Order hidden", (4.40, -1.10), 3.27, 0.72, ORANGE))
        self.add(tag, old_shape, old_strip, old_solid, old_masks)
        self.at("Now predict")
        self.play(FadeOut(old_masks), FadeOut(old_shape), run_time=0.44)
        self.play(ReplacementTransform(old_strip, strip), ReplacementTransform(old_solid, solid),
                  FadeIn(shape, shift=DOWN * 0.42), run_time=1.08)
        self.play(FadeIn(sample, shift=UP * 0.24), run_time=0.69)
        question = prediction_card()
        self.at("You need to show")
        self.play(FadeIn(question), run_time=1.15)
        self.at("across the strands", lead=0.49)
        self.play(FadeIn(lad, shift=RIGHT * 1.06, scale=0.46), run_time=1.38)
        self.at("Which model should", lead=0.60)
        self.play(FadeIn(glass, shift=DOWN * 0.42, scale=0.4),
                  shape.animate.shift(RIGHT * 0.88), solid.animate.shift(RIGHT * 0.88),
                  run_time=1.17)
        self.at("Hold your answer")
        self.play(FadeIn(hold_panel(question)), run_time=2.04, rate_func=linear)
        self.finish()


class S07Pause(NarratedScene):
    def construct(self):
        question = prediction_card()
        self.add(*predict_world(), question, hold_panel(question))
        self.wait(self.narration_s)


class S08RevealRule(SpokenScene):
    def construct(self):
        sample, lad, shape, strip, solid, glass, tag = predict_world()
        q = prediction_card()
        prompt = hold_panel(q)
        self.add(sample, lad, shape, strip, solid, glass, tag, q, prompt)
        answer = ladder((-0.65, -0.15))
        self.at("The latter moves")
        self.play(FadeOut(sample), FadeOut(q), FadeOut(prompt), run_time=0.41)
        self.play(strip.animate.move_to(xy(0, -3.00)), run_time=0.36)
        self.play(ReplacementTransform(lad, answer), visit(glass, (-0.65, 2.83)), run_time=1.24)
        self.at("rungs expose")
        self.play(LaggedStart(*[AnimationGroup(*highlighted(row)) for row in answer.rows], lag_ratio=0.35),
                  run_time=1.43)
        self.at("The other models")
        self.play(shape.animate.shift(DOWN * 0.16 + RIGHT * 0.12),
                  FadeOut(strip, shift=RIGHT * 0.84),
                  solid.animate.move_to(xy(4.67, -1.93)), run_time=0.68)
        self.play(FadeIn(letter_strip((4.67, -0.20), compact=True), shift=RIGHT * 0.54), run_time=0.66)
        questions = VGroup(label("Shape", (4.67, 2.35), 28),
                           label("Order", (4.67, 0.47), 28),
                           label("Occupied space", (4.67, -0.87), 28))
        self.at("still useful")
        self.play(LaggedStart(*[FadeIn(q) for q in questions], lag_ratio=0.41), run_time=1.18)
        rule = caption("Choose DNA models by the question.", size=32, color=GREEN, y=-2.92)
        limit = caption("Every model leaves features out.", size=32, color=ORANGE, y=-3.42)
        self.at("Choose")
        self.play(FadeIn(rule), run_time=0.73)
        self.at("Every model leaves")
        self.play(FadeIn(limit), run_time=0.78)
        self.wait(1.5)
        self.play(FadeOut(rule), FadeOut(limit), run_time=0.40)
        self.finish()


class S09BaseEvidence(SpokenScene):
    def construct(self):
        tag = scope()
        border, heading = structure_track()
        prior = ladder((-0.65, -0.15))
        for row in prior.rows:
            for base in row:
                base[0].set_stroke(GREEN, width=5).set_fill("#365642", 1)
        shape = shape_card((4.67, 1.37), compact=True)
        strip = letter_strip((4.67, -0.20), compact=True)
        solid = space_card((4.67, -1.93), compact=True)
        questions = VGroup(label("Shape", (4.67, 2.35), 28),
                           label("Order", (4.67, 0.47), 28),
                           label("Occupied space", (4.67, -0.87), 28))
        self.add(tag, prior, shape, strip, solid, questions, lens((-0.65, 2.83), 0.40))
        self.at("Usefulness is not")
        self.play(FadeOut(questions), FadeOut(self.mobjects[-1]), FadeOut(prior), run_time=0.46)
        self.play(shape.animate.move_to(xy(-4.52, 1.19)), strip.animate.move_to(xy(-4.52, 0.08)),
                  solid.animate.move_to(xy(-4.52, -1.13)), run_time=1.17)
        outside = label("Answer a different\nquestion", (-4.52, -2.53), 28)
        self.play(FadeIn(outside), run_time=0.47)
        self.at("Evidence can reject")
        base_amounts = evidence("Base amounts", (0.05, 1.26))
        self.play(GrowFromCenter(border), run_time=0.68)
        self.play(FadeIn(heading), FadeIn(base_amounts, shift=RIGHT * 0.47), run_time=0.69)
        pairs = []
        for x, letters, h in ((-0.28, "AT", 1.58), (1.57, "GC", 2.03)):
            bars = VGroup(*[Rectangle(width=0.50, height=h, stroke_width=0,
                                      fill_color=PURPLE, fill_opacity=1).move_to(xy(x + dx, -1.66 + h / 2))
                            for dx in (-0.34, 0.34)])
            names = VGroup(*(label(ch, (x + dx, -2.07), 33)
                             for ch, dx in zip(letters, (-0.34, 0.34))))
            pairs.append((bars, names))
        self.at("Measured base amounts")
        self.play(LaggedStart(*[GrowFromEdge(bars, DOWN) for bars, _ in pairs], lag_ratio=0.47),
                  run_time=1.70)
        self.at("adenine with thymine")
        self.play(FadeIn(pairs[0][1]), pairs[0][0].animate.set_fill(GREEN, 1), run_time=0.76)
        self.at("guanine with cytosine")
        self.play(FadeIn(pairs[1][1]), pairs[1][0].animate.set_fill(GREEN, 1), run_time=0.87)
        fits = card("Pairing fits", (4.24, 0.66), 3.08, 1.36, GREEN, 31)
        fits.box.set_fill("#365642", 1)
        conflict = card("Predicts different\nA and T amounts", (4.24, -0.95), 3.10, 1.35, GREY, 28)
        self.at("A structure model")
        self.play(FadeIn(fits, shift=RIGHT * 0.58), run_time=0.84)
        self.play(FadeIn(conflict, shift=RIGHT * 0.58), run_time=0.83)
        rejected = label("Ruled out", (4.24, -2.18), 30, ORANGE)
        self.at("or be ruled", lead=0.38)
        conflict.generate_target()
        conflict.target.shift(DOWN * 0.22)
        conflict.target[0].set_fill("#66452F", 1).set_stroke(ORANGE, width=4)
        self.play(MoveToTarget(conflict), run_time=0.66)
        self.play(FadeIn(rejected), run_time=0.50)
        self.finish()


class S10XrayEvidence(SpokenScene):
    def construct(self):
        border, heading = structure_track()
        fit_card = card("Pairing fits", (4.24, 0.73), 2.76, 1.02, GREEN, 31)
        self.add(border, heading, fit_card)
        xray = evidence("X-ray diffraction", (-4.45, 2.66), 3.73)
        detector = panel(5.8, 4.72, (3.32, 0.29))
        source = panel(1.74, 1.8, (-5.60, 0.20), PURPLE)
        aperture = Rectangle(width=0.15, height=0.55, stroke_width=0,
                             fill_color=PURPLE, fill_opacity=1).move_to(xy(-4.72, 0.20))
        fibers = VGroup(*[Rectangle(width=0.12, height=2.65, stroke_width=0,
                                    fill_color=GREY, fill_opacity=1).move_to(xy(-1.96 + j * 0.21, 0.20))
                          for j in range(-3, 4)])
        spot_positions = [(3.32 + sx * d, 0.29 + sy * d * 0.88)
                          for d in (0.59, 1.07, 1.59, 2.01) for sx in (-1, 1) for sy in (-1, 1)]
        spots = VGroup(*[Dot(xy(*p), radius=0.095, color=PURPLE) for p in spot_positions])
        qualifier = label("Schematic, not a photograph", (3.32, -2.55), 28)
        self.at("X -ray diffraction")
        self.play(FadeOut(heading), FadeOut(fit_card), run_time=0.44)
        self.play(ReplacementTransform(border, detector), FadeIn(xray, shift=RIGHT * 0.37), run_time=0.85)
        self.play(FadeIn(source), FadeIn(aperture), run_time=0.67)
        self.play(FadeIn(fibers), run_time=0.68)
        beam = Arrow(xy(-4.57, 0.20), xy(0.33, 0.20), buff=0, color=PURPLE,
                     stroke_width=6, max_tip_length_to_length_ratio=0.06)
        fib_label = place_label(T("Lined-up DNA fibers", 28, TEXT), fibers, dirs=(DOWN,), buff=0.25)
        self.at("It came from spots", lead=0.80)
        self.play(GrowArrow(beam), run_time=0.78)
        self.play(LaggedStart(*[FadeIn(s, scale=0.35) for s in spots], lag_ratio=0.052),
                  FadeIn(qualifier), run_time=1.30)
        self.at("lined -up fibers", lead=0.08)
        self.play(FadeIn(fib_label), run_time=0.46)
        arrow1 = DoubleArrow(xy(2.39, -0.65), xy(4.25, -0.65), buff=0, color=PURPLE,
                             stroke_width=4, tip_length=0.16)
        arrow2 = DoubleArrow(xy(4.91, -0.96), xy(4.91, 1.54), buff=0, color=PURPLE,
                             stroke_width=4, tip_length=0.16)
        self.at("The pattern was")
        self.play(GrowFromCenter(arrow1), run_time=0.69)
        self.play(GrowFromCenter(arrow2), run_time=0.68)
        constraint = evidence("X-ray clues", (-4.74, 0.84), 3.08)
        self.at("not a photograph")
        self.play(FadeOut(source), FadeOut(aperture), FadeOut(beam), FadeOut(fibers), FadeOut(fib_label),
                  run_time=0.48)
        self.play(ReplacementTransform(VGroup(arrow1, arrow2), constraint), run_time=1.04)
        self.finish()


class S11ModelBuilding(SpokenScene):
    def construct(self):
        base_amounts = evidence("Base amounts", (-4.74, 1.95))
        xray = evidence("X-ray clues", (-4.74, 0.84), 3.08)
        chemistry = evidence("Chemistry", (-4.74, -0.27))
        old_detector = panel(5.8, 4.72, (3.32, 0.29))
        self.add(xray, old_detector, scope())
        model, arrows = tested_model()
        self.at("Chemistry supplied")
        self.play(FadeOut(old_detector), FadeIn(base_amounts), run_time=0.53)
        self.play(FadeIn(chemistry, shift=RIGHT * 0.72), run_time=1.04)
        brace = VGroup(
            Line(xy(-2.82, 2.16), xy(-2.82, -2.94)),
            Line(xy(-2.82, 2.16), xy(-2.48, 2.16)),
            Line(xy(-2.82, -2.94), xy(-2.48, -2.94)),
        ).set_stroke(PURPLE, width=4)
        self.at("Watson and Crick")
        self.play(Create(brace), run_time=1.02)
        self.at("built a model")
        self.play(LaggedStart(*[GrowFromCenter(r) for r in model.rails], lag_ratio=0.25), run_time=0.91)
        self.play(LaggedStart(*[FadeIn(r, scale=0.68) for r in model.rows], lag_ratio=0.40), run_time=1.50)
        outside = label("Backbones outside", (4.53, 1.25), 29)
        inside = label("Bases paired inside", (4.53, -0.16), 29)
        opposite = label("Opposite directions", (4.53, -1.66), 29)
        self.at("Backbones stayed")
        self.play(FadeIn(outside), *[r.animate.set_fill(TEXT, 1) for r in model.rails], run_time=0.95)
        self.at("bases paired")
        self.play(FadeIn(inside), *(a for row in model.rows for a in highlighted(row)), run_time=0.84)
        self.at("opposite directions", lead=0.68)
        self.play(*(GrowArrow(a) for a in arrows), FadeIn(opposite),
                  *[r.animate.set_fill(GREY, 1) for r in model.rails], run_time=1.30)
        self.finish()


class S12Caution(SpokenScene):
    def construct(self):
        model, arrows = tested_model()
        for row in model.rows:
            for block in row:
                block[0].set_stroke(GREEN, width=5).set_fill("#365642", 1)
        self.add(model, arrows, scope())
        prediction = evidence("Copying prediction", (0, 2.95), 4.07)
        self.at("Pairing also suggested")
        self.play(FadeIn(prediction), run_time=0.73)
        self.play(LaggedStart(*[block[0].animate.set_stroke(BLUE, width=2.5).set_fill("#24546A", 1)
                                for row in model.rows for block in row], lag_ratio=0.35), run_time=1.83)
        left = VGroup(model.rails[0], arrows[0], *[r[0] for r in model.rows])
        right = VGroup(model.rails[1], arrows[1], *[r[1] for r in model.rows])
        self.at("Separate the strands", lead=0.40)
        self.play(left.animate.shift(LEFT * 2.69), right.animate.shift(RIGHT * 2.69), run_time=1.62)
        new_left = [base_block(ch, (-1.90, y), size=42) for ch, y in zip(PARTNER_BASES, (1, -0.40, -1.80))]
        new_right = [base_block(ch, (1.90, y), size=42) for ch, y in zip(SAMPLE_BASES, (1, -0.40, -1.80))]
        self.at("each row fixes", lead=0.11)
        self.play(LaggedStart(*[AnimationGroup(FadeIn(a, shift=LEFT * 1.03),
                                             FadeIn(b, shift=RIGHT * 1.03))
                               for a, b in zip(new_left, new_right)], lag_ratio=0.50), run_time=2.57)
        self.at("That was a prediction")
        self.play(*(a for pair in zip(new_left, new_right) for a in highlighted(pair)),
                  prediction.box.animate.set_stroke(PURPLE, width=5), run_time=1.00)
        self.at("not proof")
        self.play(FadeIn(card("Still to test", (0, 1.88), 3.09, 0.58, ORANGE)), run_time=0.75)
        self.finish()


class S13Caution(SpokenScene):
    def construct(self):
        model, arrows = tested_model()
        self.add(model, scope())
        twist = ValueTracker(0.17)
        gauge = twist_dial(twist, (-4.58, -0.03))
        helix = label("Double helix model", (-0.15, 2.87), 36)
        self.at("The result was")
        self.play(FadeIn(gauge), run_time=0.62)
        self.play(twist.animate.set_value(0.86), FadeIn(helix), run_time=1.90)
        wc = card("Watson and Crick\nUnproved", (4.57, 1.33), 4.24, 1.32, PURPLE, 30)
        fg_box = panel(4.24, 1.32, (4.57, -0.37), PURPLE, radius=0.14)
        fg_text = VGroup(T("Franklin and Gosling", 28, PURPLE),
                         T("Helix highly probable", 28, PURPLE)).arrange(DOWN, buff=0.14).move_to(fg_box)
        fg = VGroup(fg_box, fg_text.set_z_index(2))
        timeline = Line(xy(-6.40, -2.93), xy(5.95, -2.93), color=GREY, stroke_width=2.5)
        anchor = Dot(xy(-4.67, -2.93), radius=0.072, color=PURPLE)
        year = label("1953", (-4.67, -3.30), 28)
        self.at("Watson and Crick")
        self.play(FadeIn(wc, shift=LEFT * 0.25), run_time=1.08)
        self.play(Create(timeline), FadeIn(anchor), FadeIn(year), run_time=1.06)
        self.at("Franklin and Gosling")
        self.play(FadeIn(fg, shift=LEFT * 0.25), run_time=1.27)
        self.play(fg_box.animate.set_stroke(PURPLE, width=5), run_time=0.67)
        tests = card("Later tests", (4.57, -1.96), 3.69, 0.83, PURPLE)
        end = Dot(xy(4.57, -2.93), radius=0.088, color=GREEN)
        support = VGroup(*(label("✓", (2.10, y), 33, GREEN) for y in (1, -0.40, -1.80)))
        self.at("Later tests")
        self.play(FadeIn(tests, shift=RIGHT * 0.43), FadeIn(end), run_time=0.76)
        self.at("supported its")
        self.play(LaggedStart(*[GrowFromCenter(t) for t in support], lag_ratio=0.28),
                  *(a for row in model.rows for a in highlighted(row)), run_time=1.17)
        self.finish()


class S14Return(SpokenScene):
    def construct(self):
        sample, frames, names, _, tag = opening_world()
        self.add(tag.set_x(0))
        self.at("Return to the original")
        self.play(GrowFromCenter(sample[0]), run_time=0.63)
        self.play(Create(sample[1]), FadeIn(sample[2]), run_time=0.60)
        self.play(LaggedStart(*[FadeIn(f, scale=0.85) for f in frames], lag_ratio=0.17), run_time=0.90)
        centers = VIEW_CENTERS
        views = (ladder(centers[0], compact=True), shape_card(centers[1], compact=True),
                 letter_strip(centers[2], compact=True), space_card(centers[3], compact=True))
        self.at("Pairing shape")
        self.play(LaggedStart(*[AnimationGroup(FadeIn(v), FadeIn(n)) for v, n in zip(views, names)],
                              lag_ratio=0.40), run_time=2.46)
        glass = lens((-2.18, 1.44), 0.21)
        tabs = VGroup(*(card("Leaves out", (x, y), 2.21, 0.58, ORANGE, 28)
                        for x, y in ((-4.55, 0.16), (4.55, 0.16), (-4.55, -2.87), (4.55, -2.87))))
        self.at("Start with the question")
        self.play(FadeIn(glass), frames[0].animate.set_fill("#53503C", 1), run_time=0.36)
        self.play(FadeOut(glass), frames[0].animate.set_fill(SLATE, 1), run_time=0.19)
        glass = lens((2.10, 1.44), 0.21)
        self.play(FadeIn(glass), frames[1].animate.set_fill("#53503C", 1), run_time=0.37)
        self.at("then inspect")
        self.play(LaggedStart(*[FadeIn(tab, shift=DOWN * 0.085) for tab in tabs], lag_ratio=0.31),
                  FadeOut(glass), frames[1].animate.set_fill(SLATE, 1), run_time=0.85)
        glass = lens((2.10, -1.63), 0.21)
        self.play(FadeIn(glass), frames[3].animate.set_fill("#53503C", 1), run_time=0.34)
        self.play(FadeOut(glass), frames[3].animate.set_fill(SLATE, 1), run_time=0.22)
        glass = lens((-2.18, -1.63), 0.21)
        self.play(FadeIn(glass), frames[2].animate.set_fill("#53503C", 1), run_time=0.58)
        self.finish()


class S15End(EndCard):
    LINE = RULE
