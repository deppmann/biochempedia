"""Which Picture of DNA Should You Trust?

COLOR MAP (one meaning throughout)
  BLUE   DNA base blocks
  GREY   backbones, outlines, and neutral structure
  YELLOW the question lens and comparisons
  GREEN  features a view shows / evidence-supported features
  ORANGE features a view leaves out / claims still to test
  PURPLE evidence and constraints

All DNA views are labelled blocks, bars, cards, or silhouettes. No molecular
structure, atoms, ribbon, or bond geometry is drawn.
"""
from bp_parts import *


PURPLE = "#B58CD9"
ORANGE = "#F29E4C"


def workbench():
    """A quiet full-frame field so the diagram reads as one carried workbench."""
    panel = RoundedRectangle(corner_radius=0.28, width=13.0, height=6.9,
                             stroke_color=GREY, stroke_width=2,
                             fill_color=GREY, fill_opacity=0.32).set_z_index(-20)
    panel.layout_ok = True  # deliberate non-informational background behind all labels
    return panel


class FilmScene(SpokenScene):
    def setup(self):
        super().setup()
        self.add(workbench())


def labelled_box(text, width=3.0, height=1.25, color=GREY, size=30, fill=0.12):
    box = RoundedRectangle(corner_radius=0.18, width=width, height=height,
                           stroke_color=color, stroke_width=3,
                           fill_color=color, fill_opacity=fill)
    label = fit_text(text, max_w=width - 0.35, size=size, color=color, max_lines=2).move_to(box)
    label.layout_ok = True  # labels intentionally sit inside their own cards
    return VGroup(box, label)


def base_block(letter, width=0.78, height=0.58, size=28):
    box = RoundedRectangle(corner_radius=0.09, width=width, height=height,
                           stroke_color=BLUE, stroke_width=3,
                           fill_color=BLUE, fill_opacity=0.25)
    label = T(letter, size, TEXT, weight=BOLD).move_to(box)
    label.layout_ok = True  # block label
    return VGroup(box, label)


def sample_box(at=(-4.9, 0.0, 0), scale=1.0):
    g = labelled_box("DNA sample", 2.45, 2.05, PURPLE, 32, 0.09).move_to(at).scale(scale)
    pulse(g[0], base=3.2, amp=0.8, speed=2.0)
    return g


def question_lens(at=(0, 1.75, 0), scale=1.0):
    ring = Circle(radius=0.58, color=YELLOW, stroke_width=7)
    handle = Line([0.40, -0.40, 0], [0.90, -0.90, 0], color=YELLOW, stroke_width=7)
    dot = Dot(radius=0.08, color=YELLOW)
    return VGroup(ring, handle, dot).move_to(at).scale(scale)


FRAME_POS = {
    "pairing": (-3.9, 1.75, 0),
    "shape": (3.9, 1.75, 0),
    "order": (-3.9, -1.45, 0),
    "occupied space": (3.9, -1.45, 0),
}


def question_frame(name, at=None, scale=1.0):
    at = at or FRAME_POS[name]
    box = RoundedRectangle(corner_radius=0.18, width=3.35, height=1.65,
                           stroke_color=GREY, stroke_width=3)
    label = T(name, 28, TEXT).next_to(box, UP, buff=0.12)
    label.layout_ok = True  # Create() briefly clips glyphs; the settled label is 28 pt
    return VGroup(box, label).move_to(at).scale(scale)


def opening_world(with_frames=True):
    sample = sample_box((0, 0, 0), 1.12)
    frames = VGroup(*[question_frame(k) for k in FRAME_POS]) if with_frames else VGroup()
    lens = question_lens((0, 2.7, 0), 0.9)
    return VGroup(sample, frames, lens, scope_tag("schematic"))


def ladder(at=(0, 0.15, 0), scale=1.0, rows=("AT", "GC", "TA")):
    left = Rectangle(width=0.16, height=4.35, stroke_color=GREY, stroke_width=2,
                     fill_color=GREY, fill_opacity=0.65).move_to([-1.4, 0, 0])
    right = left.copy().move_to([1.4, 0, 0])
    rungs = VGroup()
    for y, pair in zip((1.25, 0, -1.25), rows):
        a = base_block(pair[0], 1.26, 0.72, 32).move_to([-0.65, y, 0])
        b = base_block(pair[1], 1.26, 0.72, 32).move_to([0.65, y, 0])
        rungs.add(VGroup(a, b))
    g = VGroup(left, right, rungs).move_to(at).scale(scale)
    g.rails, g.rungs = VGroup(left, right), rungs
    return g


def letter_strip(seq="ATGCTA", at=(0, 0, 0), scale=1.0):
    return VGroup(*[base_block(x, 0.82, 0.64, 28) for x in seq]).arrange(RIGHT, buff=0.08).move_to(at).scale(scale)


def shape_card(at=(0, 0, 0), scale=1.0):
    card = labelled_box("double-helix\nribbon model", 3.5, 2.0, GREY, 28, 0.10)
    return card.move_to(at).scale(scale)


def space_card(at=(0, 0, 0), scale=1.0):
    frame = RoundedRectangle(corner_radius=0.16, width=3.5, height=2.0,
                             stroke_color=GREY, stroke_width=3)
    silhouette = Polygon([-1.25, -0.55, 0], [-1.55, 0.2, 0], [-0.9, 0.72, 0],
                         [0.1, 0.56, 0], [0.9, 0.76, 0], [1.48, 0.08, 0],
                         [0.95, -0.68, 0], [-0.15, -0.5, 0],
                         fill_color=GREY, fill_opacity=0.72, stroke_width=0)
    label = T("space occupied", 27, TEXT).move_to(silhouette)
    label.layout_ok = True
    return VGroup(frame, silhouette, label).move_to(at).scale(scale)


def candidate_world(question=True):
    sample = sample_box((0, 0.35, 0), 0.74)
    lad = ladder((-4.5, 0.25, 0), 0.48)
    shape = shape_card((4.35, 1.55, 0), 0.65)
    strip = letter_strip("ATGCTA", (0, -1.45, 0), 0.72)
    space = space_card((4.35, -1.15, 0), 0.65)
    lens = question_lens((0, 2.25, 0), 0.75)
    for i, mob in enumerate((lad, shape, strip, space)):
        bob(mob, amp=0.025, speed=1.2, seed=i)
    g = VGroup(sample, lad, shape, strip, space, lens)
    if question:
        g.add(question_card("Which bases face each other?", y=-3.18, size=34))
    return g


def tested_model(at=(0, 0.1, 0), scale=1.0):
    return ladder(at, scale, ("AT", "GC", "CG"))


class S00Hook(FilmScene, TitleCard):
    LESSON = "Discovering DNA structure"
    TITLE = "Which Picture of DNA Should You Trust?"

    def construct(self):
        sample = sample_box((0, 0, 0), 1.2)
        self.at("Several pictures")
        self.play(FadeIn(sample, scale=0.9), run_time=0.8)
        frames = VGroup(*[question_frame(k) for k in FRAME_POS])
        self.play(LaggedStart(*[Create(f) for f in frames], lag_ratio=0.14), run_time=1.5)
        self.play(Rotate(frames, angle=0.045, about_point=ORIGIN), run_time=1.45, rate_func=linear)
        lens = question_lens(FRAME_POS["pairing"], 0.72)
        self.at("Which one should")
        self.play(FadeIn(lens), run_time=0.4)
        self.play(lens.animate.move_to(FRAME_POS["shape"]), run_time=0.7)
        self.play(Rotate(frames, angle=0.035, about_point=ORIGIN), run_time=0.9, rate_func=linear)
        self.at("The answer changes")
        self.play(lens.animate.move_to(FRAME_POS["order"]), run_time=0.8)
        self.play(lens.animate.move_to(FRAME_POS["occupied space"]), run_time=0.8)
        self.at("Keep one short sample")
        self.play(lens.animate.move_to([0, 2.7, 0]), frames.animate.scale(0.96), run_time=1.0)
        self.add(scope_tag("schematic"))
        self.finish()


class S01Title(TitleCard):
    LESSON = "Discovering DNA structure"
    TITLE = "Which Picture of DNA Should You Trust?"


class S02ModelTool(FilmScene):
    def construct(self):
        sample = sample_box((-4.9, 0, 0), 0.9)
        self.add(sample, scope_tag("schematic"))
        tool = labelled_box("MODEL TOOLBOX", 5.3, 4.6, GREY, 34, 0.08).move_to([2.1, 0, 0])
        tool[1].move_to(tool[0].get_top() + DOWN * 1.0)
        handle = Arc(radius=1.2, start_angle=0, angle=PI, color=GREY, stroke_width=8).move_to([2.1, 2.3, 0])
        self.at("A scientific model")
        self.play(GrowFromCenter(tool[0]), FadeIn(handle), run_time=0.8)
        model = labelled_box("MODEL", 2.6, 1.15, BLUE, 38, 0.18).move_to([2.1, 0.25, 0])
        self.play(FadeIn(model, shift=UP * 0.4), run_time=0.7)
        self.play(Rotate(VGroup(tool, handle), angle=0.025, about_point=[2.1, 0, 0],
                         rate_func=there_and_back), run_time=2.75)
        lens = question_lens([3.95, 0.45, 0], 0.5)
        self.at("It helps explain")
        self.play(FadeIn(lens), run_time=0.6)
        self.play(model.animate.shift(UP * 0.16), rate_func=there_and_back, run_time=2.55)
        shown = T("shows", 32, GREEN).move_to([0.5, -1.45, 0])
        omitted = T("leaves out", 32, ORANGE).move_to([3.55, -1.45, 0])
        self.at("It is a tool")
        self.play(FadeIn(shown), FadeIn(omitted), model.animate.shift(UP * 0.25), run_time=0.8)
        self.at("Every tool has")
        self.play(Rotate(VGroup(shown, omitted), angle=0.06, about_point=[2.1, -1.45, 0], rate_func=there_and_back),
                  handle.animate.shift(UP * 0.12), run_time=1.0)
        self.finish()


class S03Ladder(FilmScene):
    def construct(self):
        sample = sample_box((-5.15, 0, 0), 0.75)
        lens = question_lens([-2.8, 2.45, 0], 0.65)
        lab = T("pairing", 30, YELLOW).next_to(lens, RIGHT, buff=0.28)
        self.at("Ask which bases")
        self.play(FadeIn(sample), FadeIn(lens), FadeIn(lab), run_time=0.8)
        lad = ladder([0.3, 0, 0], 1.0)
        self.at("A flat ladder")
        self.play(FadeIn(lad.rails), run_time=0.7)
        self.at("Labeled base blocks")
        self.play(LaggedStart(*[FadeIn(r, shift=UP * 0.15) for r in lad.rungs], lag_ratio=0.18), run_time=1.3)
        curtain = labelled_box("twist and atoms\nleft out", 2.4, 4.35, ORANGE, 28, 0.18).move_to([4.85, 0, 0])
        self.at("Pairing is clear")
        self.play(*[Indicate(r, color=GREEN, scale_factor=1.05) for r in lad.rungs], run_time=0.9)
        self.at("but the twist")
        self.play(FadeIn(curtain, shift=LEFT * 0.25), run_time=0.8)
        self.add(scope_tag("schematic"))
        self.finish()


class S04Letters(FilmScene):
    def construct(self):
        sample = sample_box((-5.15, 0, 0), 0.75)
        lens = question_lens([-2.8, 2.45, 0], 0.65)
        lab = T("order", 30, YELLOW).next_to(lens, RIGHT, buff=0.28)
        lad = ladder([0.35, 0, 0], 0.78)
        self.add(sample, lad, scope_tag("schematic"))
        self.at("Ask for base order")
        self.play(FadeIn(lens), FadeIn(lab), run_time=0.7)
        strip = letter_strip("ATGCTA", [0.65, 0.65, 0], 1.0)
        self.at("The ladder folds")
        self.play(FadeOut(lad.rails), ReplacementTransform(lad.rungs, strip), run_time=1.2)
        compare = letter_strip("ATCCTA", [0.65, -0.65, 0], 1.0)
        compare_lab = T("comparison sequence", 26, GREY).next_to(compare, DOWN, buff=0.2)
        self.at("Comparing positions")
        self.play(FadeIn(compare, shift=UP * 0.2), FadeIn(compare_lab), run_time=0.8)
        self.play(Indicate(VGroup(strip[0], strip[1], compare[0], compare[1]), color=GREEN),
                  Indicate(VGroup(strip[2], compare[2]), color=YELLOW), run_time=0.8)
        mask = labelled_box("shape, size, partner\nleft out", 2.55, 3.7, ORANGE, 27, 0.2).move_to([4.95, 0, 0])
        self.at("Shape size")
        self.play(FadeIn(mask, shift=LEFT * 0.25), run_time=0.9)
        self.finish()


class S05ShapeSpace(FilmScene):
    def construct(self):
        shape = shape_card([-2.55, 0.25, 0], 1.25)
        twist = ValueTracker(0.15)
        d = dial(twist, [2.65, 0.7, 0], radius=1.55, label="twist", color=YELLOW, fmt="{:.0f}°", scale=180)
        lens = question_lens([-2.55, 2.7, 0], 0.65)
        self.at("A ribbon model")
        self.play(FadeIn(shape), FadeIn(lens), FadeIn(d), run_time=0.8)
        self.play(twist.animate.set_value(0.85), Rotate(shape, angle=0.10, rate_func=there_and_back), run_time=2.2)
        space = space_card([2.4, 0.15, 0], 1.25)
        self.at("A space filling model")
        self.play(FadeOut(d), lens.animate.move_to([2.4, 2.7, 0]), FadeIn(space, scale=0.75),
                  shape.animate.scale(0.62).move_to([-3.9, -1.25, 0]), run_time=1.2)
        strip = letter_strip("ATGCTA", [0, -1.55, 0], 0.62)
        masks = VGroup(labelled_box("order unreadable", 2.5, 0.72, ORANGE, 25, 0.24).move_to([-3.9, -2.25, 0]),
                       labelled_box("order unreadable", 2.5, 0.72, ORANGE, 25, 0.24).move_to([3.9, -2.25, 0]))
        self.at("Neither is best")
        self.play(space.animate.scale(0.62).move_to([3.9, -1.25, 0]), FadeIn(strip), FadeIn(masks), run_time=1.0)
        self.add(scope_tag("schematic"))
        self.finish()


class S06Predict(FilmScene):
    def construct(self):
        world = candidate_world(False)
        self.at("Now predict")
        self.play(FadeIn(world, lag_ratio=0.08), run_time=1.0)
        q = question_card("Which bases face each other?", y=-3.18, size=34)
        self.at("You need to show")
        self.play(FadeIn(q), run_time=0.7)
        self.at("Which model should")
        self.play(world[-2].animate.scale(1.12), run_time=0.8)
        self.at("Hold your answer")
        self.play(world[-2].animate.scale(1 / 1.12), run_time=0.6)
        self.finish()


class S07Pause(PredictPause):
    QUESTION = "Which bases face each other?"
    SECONDS = 4.5
    CARD = {"y": -3.18, "size": 34}
    RING_AT = (6.05, -2.35, 0)

    def backdrop(self):
        return VGroup(workbench(), candidate_world(False))


class S08RevealRule(FilmScene):
    def construct(self):
        world = candidate_world(False)
        sample, lad, shape, strip, space, lens = world[:6]
        self.add(world)
        self.at("The latter moves")
        self.play(lad.animate.scale(1.7).move_to([-0.5, 0.1, 0]),
                  lens.animate.move_to([-0.5, 2.55, 0]),
                  sample.animate.scale(0.7).move_to([-5.55, 2.0, 0]), run_time=1.2)
        self.play(*[Indicate(r, color=GREEN, scale_factor=1.07) for r in lad.rungs], run_time=0.9)
        self.at("The other models")
        self.play(shape.animate.scale(0.7).move_to([4.8, 1.8, 0]),
                  strip.animate.scale(0.7).move_to([4.8, 0.1, 0]),
                  space.animate.scale(0.7).move_to([4.8, -1.55, 0]), run_time=1.0)
        labels = VGroup(T("shape?", 25, GREY).next_to(shape, LEFT, buff=0.12),
                        T("order?", 25, GREY).next_to(strip, LEFT, buff=0.12),
                        T("space?", 25, GREY).next_to(space, LEFT, buff=0.12))
        self.at("still useful")
        self.play(FadeIn(labels), run_time=0.7)
        rule = caption("Choose DNA models by the question; every model leaves features out.", 30, GREEN)
        self.at("Choose D and a")
        self.play(FadeIn(rule, shift=UP * 0.15), run_time=0.8)
        self.at("Every model leaves")
        self.play(Indicate(rule, color=GREEN, scale_factor=1.02), run_time=0.8)
        self.finish()


class S09BaseEvidence(FilmScene):
    def construct(self):
        track = RoundedRectangle(corner_radius=0.2, width=10.6, height=4.9,
                                 stroke_color=GREY, stroke_width=3).move_to([0.5, 0, 0])
        title = T("structure models", 32, TEXT).next_to(track, UP, buff=0.15)
        self.at("Usefulness is not")
        self.play(Create(track), FadeIn(title), run_time=0.8)
        evidence = labelled_box("EVIDENCE\nbase amounts", 2.45, 1.4, PURPLE, 27, 0.18).move_to([-4.9, 1.2, 0])
        self.at("Evidence can reject")
        self.play(FadeIn(evidence, shift=RIGHT * 0.3), run_time=0.8)
        bars = VGroup()
        for x, letters in ((-1.5, "A   T"), (1.5, "G   C")):
            b1 = Rectangle(width=0.55, height=2.1, fill_color=BLUE, fill_opacity=0.65, stroke_width=0).move_to([x - 0.42, 0.1, 0])
            b2 = b1.copy().move_to([x + 0.42, 0.1, 0])
            lab = T(letters, 30, TEXT).next_to(VGroup(b1, b2), DOWN, buff=0.18)
            bars.add(VGroup(b1, b2, lab))
        self.at("Measured base amounts")
        self.play(LaggedStart(*[GrowFromEdge(g[0], DOWN) for g in bars], lag_ratio=0.2),
                  LaggedStart(*[GrowFromEdge(g[1], DOWN) for g in bars], lag_ratio=0.2), run_time=1.0)
        self.at("adenine with thymine")
        self.play(FadeIn(bars[0][2]), Indicate(bars[0], color=GREEN), run_time=0.8)
        self.at("guanine with cytosine")
        self.play(FadeIn(bars[1][2]), Indicate(bars[1], color=GREEN), run_time=0.8)
        good = labelled_box("pairing fits", 2.1, 1.0, GREEN, 28, 0.16).move_to([4.25, 1.1, 0])
        bad = labelled_box("pairing conflicts", 2.4, 1.0, ORANGE, 26, 0.18).move_to([4.25, -1.2, 0])
        self.at("A structure model")
        self.play(FadeIn(good, shift=RIGHT * 0.2), FadeIn(bad), run_time=0.8)
        self.at("or be ruled out")
        self.play(bad.animate.shift(RIGHT * 1.8).set_opacity(0.35), run_time=0.8)
        other = T("other views answer a different question", 25, GREY).move_to([0, -3.2, 0])
        self.play(FadeIn(other), run_time=0.4)
        self.finish()


class S10XrayEvidence(FilmScene):
    def construct(self):
        card = labelled_box("EVIDENCE\nX-ray diffraction", 3.0, 1.35, PURPLE, 28, 0.16).move_to([-4.8, 2.25, 0])
        self.at("X ray diffraction")
        self.play(FadeIn(card, shift=RIGHT * 0.25), run_time=0.8)
        beam = Arrow([-5.7, 0.4, 0], [-3.0, 0.4, 0], color=PURPLE, stroke_width=6, buff=0.05)
        fibers = VGroup(*[Rectangle(width=0.12, height=2.5, fill_color=GREY, fill_opacity=0.65, stroke_width=0) for _ in range(5)]).arrange(RIGHT, buff=0.13).move_to([-2.6, 0.4, 0])
        fiblab = T("lined-up DNA fibers", 27, TEXT).next_to(fibers, DOWN, buff=0.22)
        self.at("It came from spots")
        self.play(GrowArrow(beam), FadeIn(fibers), FadeIn(fiblab), run_time=0.9)
        detector = Rectangle(width=4.4, height=4.7, stroke_color=GREY, stroke_width=3).move_to([3.0, 0.25, 0])
        spots = VGroup(*[Dot([3.0 + sx * d, 0.25 + sy * d, 0], radius=0.07, color=PURPLE)
                         for d in (0.45, 0.9, 1.35) for sx, sy in ((1, 1), (-1, 1), (1, -1), (-1, -1))])
        rays = VGroup(*[Arrow([-2.15, 0.4, 0], p.get_center(), color=PURPLE, stroke_width=2.5, buff=0.1) for p in spots[::3]])
        self.at("lined up fibers")
        self.play(FadeIn(detector), LaggedStart(*[GrowArrow(a) for a in rays], lag_ratio=0.2),
                  LaggedStart(*[FadeIn(p) for p in spots], lag_ratio=0.05), run_time=1.3)
        tag = labelled_box("schematic\nnot a photograph", 3.25, 1.0, ORANGE, 26, 0.18).move_to([3.0, -2.55, 0])
        measures = VGroup(DoubleArrow([2.1, 0.25, 0], [3.0, 1.15, 0], color=YELLOW, buff=0.08, tip_length=0.14),
                          DoubleArrow([1.65, -1.1, 0], [4.35, -1.1, 0], color=YELLOW, buff=0.08, tip_length=0.14))
        self.at("The pattern was")
        self.play(FadeIn(tag), GrowFromCenter(measures), run_time=0.9)
        self.at("not a photograph")
        self.play(Indicate(tag, color=ORANGE), run_time=0.8)
        self.finish()


class S11ModelBuilding(FilmScene):
    def construct(self):
        chemistry = labelled_box("EVIDENCE\nchemistry", 2.65, 1.2, PURPLE, 28, 0.16).move_to([-4.9, 2.35, 0])
        self.at("Chemistry supplied")
        self.play(FadeIn(chemistry, shift=RIGHT * 0.25), run_time=0.8)
        # Four open corner brackets read as a testing frame without crossing its labels.
        x0, x1, y0, y1, arm = -3.15, 4.45, -2.85, 2.75, 0.62
        frame = VGroup(
            Line([x0, y1, 0], [x0 + arm, y1, 0]), Line([x0, y1, 0], [x0, y1 - arm, 0]),
            Line([x1, y1, 0], [x1 - arm, y1, 0]), Line([x1, y1, 0], [x1, y1 - arm, 0]),
            Line([x0, y0, 0], [x0 + arm, y0, 0]), Line([x0, y0, 0], [x0, y0 + arm, 0]),
            Line([x1, y0, 0], [x1 - arm, y0, 0]), Line([x1, y0, 0], [x1, y0 + arm, 0]),
        ).set_stroke(PURPLE, 4)
        constraints = VGroup(T("base amounts", 25, PURPLE).move_to([-1.8, 2.35, 0]),
                             T("X-ray clues", 25, PURPLE).move_to([0.8, 2.35, 0]),
                             T("chemistry", 25, PURPLE).move_to([3.15, 2.35, 0]))
        self.at("Watson and Crick")
        self.play(Create(frame), LaggedStart(*[FadeIn(c) for c in constraints], lag_ratio=0.2), run_time=1.0)
        model = tested_model([0.65, -0.25, 0], 1.05)
        self.at("built a model")
        self.play(FadeIn(model.rails), run_time=0.6)
        self.play(LaggedStart(*[FadeIn(r) for r in model.rungs], lag_ratio=0.2), run_time=1.0)
        outside = VGroup(T("backbones outside", 28, GREY).move_to([-4.75, -0.65, 0]),
                         Arrow([-3.55, -0.55, 0], [-1.0, -0.25, 0], color=GREY, buff=0.1))
        self.at("Backbones stayed")
        self.play(FadeIn(outside), Indicate(model.rails, color=GREY), run_time=0.8)
        inside = T("bases paired inside", 28, BLUE).move_to([4.9, -0.65, 0])
        self.at("bases paired")
        self.play(FadeIn(inside), Indicate(model.rungs, color=GREEN), run_time=0.8)
        arrows = VGroup(Arrow([-0.75, 1.8, 0], [-0.75, -2.1, 0], color=YELLOW, buff=0),
                        Arrow([2.05, -2.1, 0], [2.05, 1.8, 0], color=YELLOW, buff=0))
        self.at("opposite directions")
        self.play(GrowArrow(arrows[0]), GrowArrow(arrows[1]), run_time=0.9)
        self.add(scope_tag("schematic"))
        self.finish()


class S12Caution(FilmScene):
    def construct(self):
        model = tested_model([0, 0.15, 0], 1.05)
        prediction = labelled_box("copying prediction", 4.4, 0.8, PURPLE, 28, 0.15).move_to([0, 2.75, 0])
        self.at("Pairing also suggested")
        self.play(FadeIn(model), FadeIn(prediction), run_time=0.9)
        left_rail, right_rail = model.rails
        left_blocks = VGroup(*[r[0] for r in model.rungs])
        right_blocks = VGroup(*[r[1] for r in model.rungs])
        self.at("Separate the strands")
        self.play(FadeOut(VGroup(left_blocks, right_blocks)), run_time=0.4)
        self.play(left_rail.animate.shift(LEFT * 1.05),
                  right_rail.animate.shift(RIGHT * 1.05), run_time=1.1)
        new_left = VGroup(base_block("T", 1.0, 0.65), base_block("C", 1.0, 0.65), base_block("G", 1.0, 0.65)).arrange(DOWN, buff=0.59).move_to([-0.8, 0.15, 0])
        new_right = VGroup(base_block("A", 1.0, 0.65), base_block("G", 1.0, 0.65), base_block("C", 1.0, 0.65)).arrange(DOWN, buff=0.59).move_to([0.8, 0.15, 0])
        self.at("each row fixes")
        self.play(FadeIn(new_left, shift=LEFT * 0.35), FadeIn(new_right, shift=RIGHT * 0.35), run_time=1.1)
        caution = labelled_box("still to test", 2.2, 0.85, ORANGE, 28, 0.18).move_to([4.8, -2.65, 0])
        self.at("That was a prediction")
        self.play(prediction.animate.move_to([3.9, 2.75, 0]), FadeIn(caution), run_time=0.8)
        self.at("not proof")
        self.play(Indicate(caution, color=ORANGE), run_time=0.7)
        self.add(scope_tag("schematic"))
        self.finish()


class S13Caution(FilmScene):
    def construct(self):
        model = tested_model([-2.5, 0, 0], 0.92)
        twist = ValueTracker(0.05)
        d = dial(twist, [3.45, -0.15, 0], radius=1.65, label="twist", color=YELLOW, fmt="{:.0f}°", scale=180)
        self.at("The result was")
        self.play(FadeIn(model), FadeIn(d), run_time=0.8)
        self.play(twist.animate.set_value(0.85), run_time=1.2)
        wc = labelled_box("Watson and Crick:\nunproved", 3.7, 1.05, PURPLE, 27, 0.14).move_to([-3.9, -2.75, 0])
        self.at("Watson and Crick")
        self.play(FadeIn(wc, shift=UP * 0.15), run_time=0.8)
        fg = labelled_box("Franklin and Gosling:\nhighly probable (a helix)", 4.3, 1.05, PURPLE, 25, 0.14).move_to([1.0, -2.75, 0])
        self.at("Franklin and Gosling")
        self.play(FadeIn(fg, shift=UP * 0.15), run_time=0.8)
        timeline = Arrow([0.7, 3.0, 0], [6.4, 3.0, 0], color=GREY, stroke_width=4, buff=0)
        tests = VGroup(*[labelled_box("test ✓", 1.5, 0.6, GREEN, 24, 0.14).move_to([x, 2.45, 0]) for x in (1.6, 3.55, 5.5)])
        self.at("Later tests")
        self.play(GrowArrow(timeline), LaggedStart(*[FadeIn(t, shift=RIGHT * 0.12) for t in tests], lag_ratio=0.2), run_time=1.1)
        self.at("main features")
        self.play(Indicate(model, color=GREEN, scale_factor=1.03), run_time=0.8)
        self.add(scope_tag("schematic"))
        self.finish()


class S14Return(FilmScene):
    def construct(self):
        sample = sample_box([0, 0, 0], 1.1)
        self.at("Return to the")
        self.play(FadeIn(sample, scale=0.85), run_time=0.8)
        frames = VGroup(*[question_frame(k) for k in FRAME_POS])
        self.at("Pairing shape")
        self.play(LaggedStart(*[Create(f) for f in frames], lag_ratio=0.12), sample.animate.scale(0.78), run_time=1.2)
        views = VGroup(ladder(FRAME_POS["pairing"], 0.28), shape_card(FRAME_POS["shape"], 0.43),
                       letter_strip("ATGC", FRAME_POS["order"], 0.48), space_card(FRAME_POS["occupied space"], 0.43))
        self.play(LaggedStart(*[FadeIn(v) for v in views], lag_ratio=0.12), run_time=1.0)
        tabs = VGroup(*[labelled_box("leaves out", 2.0, 0.5, ORANGE, 24, 0.18).move_to([p[0], p[1] - 1.2, 0]) for p in FRAME_POS.values()])
        rot = VGroup(frames, views, tabs)
        self.at("different views")
        self.play(LaggedStart(*[FadeIn(t) for t in tabs], lag_ratio=0.1), run_time=0.8)
        self.play(Rotate(rot, angle=0.028, about_point=ORIGIN), run_time=1.05, rate_func=linear)
        lens = question_lens(FRAME_POS["pairing"], 0.52)
        self.at("Start with the question")
        self.play(FadeIn(lens), run_time=0.3)
        self.play(lens.animate.move_to(FRAME_POS["shape"]), Rotate(rot, angle=0.012, about_point=ORIGIN), run_time=0.45)
        self.play(lens.animate.move_to(FRAME_POS["occupied space"]), Rotate(rot, angle=0.012, about_point=ORIGIN), run_time=0.45)
        self.play(lens.animate.move_to(FRAME_POS["order"]), Rotate(rot, angle=0.012, about_point=ORIGIN), run_time=0.45)
        self.at("then inspect")
        self.play(Indicate(tabs[2], color=ORANGE, scale_factor=1.06),
                  Rotate(rot, angle=0.02, about_point=ORIGIN), run_time=0.8)
        self.add(scope_tag("schematic"))
        self.finish()


class S15End(EndCard):
    LINE = "Choose DNA models by the question; every model leaves features out."
