"""Tracing inheritance from the same marker bands through two kinds of pedigree.

Patch-clamp palette: grey for structure, yellow for the active cue, green for
a match, red for a mismatch, and gold for the question and the study credit.
Alleles 1–4 keep blue, teal, purple, and orange wherever they appear.
"""
from bp_parts import *


PURPLE = "#B58CD9"
ORANGE = "#F29E4C"
ALLELES = (GREY, BLUE, TEAL, PURPLE, ORANGE)
BOARD = "#283447"
ACTIVE = "#3E506C"
BODY = "#53657D"
EDGE = "#768BA3"
QUESTION = "Which parent? Which division?"
QUESTION_Y = -2.98
PARENT_X = (-4.8, -2.15, 2.15, 4.8)


def point(x, y):
    return np.array([x, y, 0.0])


def label(words, x, y, size=31, color=TEXT):
    return T(words, size, color, weight=MEDIUM).move_to(point(x, y))


def inset(x, y, w, h, color=BOARD, edge="#43536C"):
    return RoundedRectangle(width=w, height=h, corner_radius=0.23,
                            fill_color=color, fill_opacity=1, stroke_color=edge,
                            stroke_width=1.5).move_to(point(x, y))


def board():
    return inset(0, 0.03, 12.9, 6.86, "#171F2D", "#39485E")


def stripe(a, x, y, w=0.62, h=0.21):
    return RoundedRectangle(width=w, height=h, corner_radius=min(h, w) * 0.25,
                            stroke_width=0, fill_color=ALLELES[a],
                            fill_opacity=1).move_to(point(x, y))


def focus(panel, active=True):
    return panel.animate.set_fill(ACTIVE if active else BOARD)


def schematic():
    return scope_tag(size=28).move_to(point(5.39, -3.14))


def chromosome(x, y, a, scale=1, locus=0.75, pinched=False):
    """A chromosome bar with an independently movable marker band."""
    if pinched:
        outline = [(-.32, 1.53), (.32, 1.53), (.35, .28), (.23, 0),
                   (.35, -.28), (.32, -1.53), (-.32, -1.53), (-.35, -.28),
                   (-.23, 0), (-.35, .28)]
        body = Polygon(*[point(x + u * scale, y + v * scale) for u, v in outline],
                       fill_color=BODY, fill_opacity=1, stroke_color=EDGE, stroke_width=2)
        body.round_corners(0.08 * scale)
    else:
        body = RoundedRectangle(width=.67 * scale, height=3.12 * scale,
                                corner_radius=.27 * scale, fill_color=BODY,
                                fill_opacity=1, stroke_color=EDGE,
                                stroke_width=2).move_to(point(x, y))
    band = stripe(a, x, y + locus * scale, .60 * scale, .22 * scale)
    return VGroup(body, band)


def sister_pair(x, y, a, scale=1, locus=.40):
    off = .40 * scale
    left = chromosome(x - off, y, a, scale, locus, True)
    right = chromosome(x + off, y, a, scale, locus, True)
    join = Line(point(x - off, y), point(x + off, y), color=YELLOW,
                stroke_width=10 * scale)
    return VGroup(left, right, join)


def parent_backdrop():
    panels = TwoPanel("Father", "Mother", colors=(BLUE, PURPLE), top=3.10,
                      bottom=-2.62, width=12.15, size=34)
    for panel in (panels.left_frame, panels.right_frame):
        panel.set_fill(BOARD, 1).set_stroke("#50627C", 2)
    return VGroup(board(), panels), panels


def parent_numbers():
    return VGroup(*[label(str(a), x, -1.97, 36, ALLELES[a])
                    for a, x in enumerate(PARENT_X, 1)])


def bird(x, y, color, scale=1, facing=1):
    """Side-on finch silhouette, built around the beak used in the feeding beat."""
    tail = Polygon(point(-.47, -.05), point(-1.11, .03), point(-.77, -.36),
                   fill_color=color, fill_opacity=1, stroke_width=0)
    torso = Ellipse(width=1.48, height=1.00, color=color, fill_opacity=1,
                    stroke_width=0).shift(LEFT * .08)
    wing = Ellipse(width=.88, height=.48, color=interpolate_color(ManimColor(color), ManimColor(BG), .37),
                   fill_opacity=1, stroke_width=0).rotate(.34).shift(LEFT * .24)
    head = Circle(.42, color=color, fill_opacity=1, stroke_width=0).move_to(point(.44, .39))
    beak = Polygon(point(.76, .49), point(1.11, .34), point(.77, .20),
                   color=GOLD, fill_opacity=1, stroke_width=0)
    eye = Dot(point(.57, .49), radius=.056, color=BG)
    feet = VGroup(*[Line(point(u, -.41), point(u + .11, -.66), color=GOLD,
                         stroke_width=3) for u in (-.29, .14)])
    g = VGroup(feet, tail, torso, wing, head, beak, eye)
    if facing == -1:
        g.flip(axis=UP)
    return g.scale(scale).move_to(point(x, y))


def nest(x, y, width=2.25):
    bowl = AnnularSector(inner_radius=.65, outer_radius=.86, angle=PI,
                         start_angle=PI, color="#76604D", fill_opacity=1, stroke_width=0)
    rim = Line(LEFT * .9, RIGHT * .9, color="#B59373", stroke_width=5)
    return VGroup(bowl, rim).stretch_to_fit_width(width).move_to(point(x, y))


def opening_board(colored=False):
    stage = board()
    left = inset(-3.1, 1.04, 5.96, 3.93)
    right = inset(3.1, 1.04, 5.96, 3.93)
    bottom = inset(0, -2.01, 12.16, 1.51)
    birds = VGroup(bird(-4.85, 1.40, BLUE, .84),
                   bird(-1.38, 1.45, PURPLE, .84, -1),
                   bird(-3.13, .66, "#C8ABB5", .58, -1))
    cradle = nest(-3.13, .02, 1.95)
    origins = VGroup(chromosome(2.15, 1.87, 0, .35),
                     chromosome(4.05, 1.87, 0, .35))
    slot = inset(3.1, .21, 3.65, 1.40, "#202B3D", EDGE)
    copies = VGroup(*[chromosome(x, .21, 0, .35) for x in (2.58, 3.10, 3.62)])
    bars = VGroup(*[chromosome(x, -2.0, a if colored else 0, .77).rotate(PI / 2)
                    for a, x in enumerate((-4.42, -1.47, 1.47, 4.42), 1)])
    questions = VGroup(label("?", -4.83, 2.52, 42, YELLOW),
                       label("?", 5.2, 1.73, 42, YELLOW))
    return VGroup(stage, left, right, bottom, cradle, birds, origins, slot, copies, bars, questions)


class S01Hook(SpokenScene):
    def construct(self):
        world = opening_board()
        _, left, right, bottom, _, birds, origins, _, copies, bars, questions = world
        arrival = copies[2]
        copies.remove(arrival)
        self.add(world, schematic())
        pulse(questions[0], base=1.3, amp=1.2)
        pulse(questions[1], base=1.3, amp=1.2)
        bob(birds[2], amp=.11, speed=2.4)
        self.at("who really fathered")
        self.play(focus(left), birds[0].animate.rotate(-.11), run_time=1.65)
        self.at("passed an extra")
        extra = origins[1].copy()
        self.add(extra)
        self.play(extra.animate.move_to(arrival), focus(left, False), focus(right), run_time=1.78)
        self.remove(extra)
        copies.add(arrival)
        self.at("watching birds")
        food = Dot(point(-4.02, 1.58), color=YELLOW, radius=.10)
        self.add(food)
        self.play(birds[0].animate.rotate(-.22).shift(RIGHT * .25),
                  food.animate.move_to(point(-3.53, .93)), focus(left), focus(right, False),
                  run_time=1.75)
        self.play(FadeOut(food), birds[0].animate.rotate(.33).shift(LEFT * .25), run_time=1.3)
        self.at("counting chromosomes")
        self.play(focus(left, False), focus(right), run_time=.83)
        self.play(LaggedStart(
            *[copy[0].animate(rate_func=there_and_back).set_stroke(YELLOW, 6) for copy in copies],
            lag_ratio=.39), run_time=2.92)
        self.at("dna markers", lead=.65)
        targets = opening_board(True)[9]
        self.play(LaggedStart(*[Transform(bar[1], target[1]) for bar, target in zip(bars, targets)],
                             lag_ratio=.23), focus(right, False), focus(bottom), run_time=1.58)
        self.finish()


class S02Title(TitleCard):
    TITLE = "Tracing Inheritance with DNA Markers"
    LESSON = "DNA Marker Genotyping"

    def construct(self):
        hook = opening_board(True)
        hook[3].set_fill(ACTIVE)
        background = VGroup(hook, schematic())
        self.add(background)
        original = background.copy()
        title = T(self.TITLE, 53, TEXT, font=TITLE_FONT).move_to(point(0, .22))
        lesson = label(self.LESSON, 0, 1.06, 33, TEAL)
        rule = Line(point(-1.2, -.50), point(1.2, -.50), color=GOLD, stroke_width=4)
        self.play(background.animate.fade(.88), run_time=.30)
        self.play(FadeIn(title), FadeIn(lesson), GrowFromCenter(rule), run_time=.34)
        self.wait(.77)
        self.play(FadeOut(VGroup(title, lesson, rule)), run_time=.22)
        self.play(Transform(background, original), run_time=.34)
        self.finish()


class S03Markers(SpokenScene):
    def construct(self):
        back, panels = parent_backdrop()
        rods = VGroup(*[chromosome(x, .24, 0) for x in PARENT_X])
        self.add(back, rods, schematic())
        self.at("a locus")
        self.play(LaggedStart(*[r[1].animate.set_fill(YELLOW) for r in rods], lag_ratio=.15),
                  focus(panels.left_frame), focus(panels.right_frame), run_time=1.23)
        locus = caption("Locus", 34, YELLOW)
        self.play(FadeIn(locus), run_time=.35)
        self.at("and its versions")
        alleles = caption("Alleles", 34)
        self.play(swap(locus, alleles, .55))
        self.play(LaggedStart(*[r[1].animate.set_fill(ALLELES[i]) for i, r in enumerate(rods, 1)],
                             lag_ratio=.21), focus(panels.left_frame, False), focus(panels.right_frame, False),
                  run_time=1.52)
        self.at("at microsatellite")
        repeats = VGroup(*[VGroup(*[stripe(a, 0, 0, .29, .48) for _ in range(n)])
                           .arrange(RIGHT, buff=.075).move_to(point(x, -.69))
                           for a, (x, n) in enumerate(zip(PARENT_X, (2, 3, 4, 5)), 1)])
        texts = caption("Microsatellite repeats", 34)
        self.play(swap(alleles, texts, .54))
        self.play(LaggedStart(*[GrowFromPoint(g, r[1].get_center()) for g, r in zip(repeats, rods)],
                             lag_ratio=.25), focus(panels.left_frame), focus(panels.right_frame),
                  run_time=2.1)
        self.at("vary between individuals")
        self.play(LaggedStart(*[repeat.animate.stretch(1.26, 0).shift(DOWN * .44)
                                for repeat in repeats], lag_ratio=.26),
                  focus(panels.left_frame, False), run_time=2.12)
        self.at("when parents carry")
        self.play(LaggedStart(*[FadeOut(g, target_position=r[1].get_center())
                                for r, g in zip(rods, repeats)], lag_ratio=.27),
                  focus(panels.left_frame, False), focus(panels.right_frame, False), run_time=2.1)
        self.at("it forms an")
        marker = caption("Informative DNA marker", 34)
        self.play(swap(texts, marker, .62))
        self.play(LaggedStart(*[r[1].animate.stretch(1.40, 1) for r in rods],
                             lag_ratio=.18, rate_func=there_and_back),
                  focus(panels.left_frame), focus(panels.right_frame), run_time=1.95)
        self.at("a father carries")
        numbers = parent_numbers()
        self.play(FadeIn(numbers[0]), FadeIn(numbers[1]), focus(panels.right_frame, False), run_time=1.34)
        self.at("and a mother")
        self.play(FadeIn(numbers[2]), FadeIn(numbers[3]), FadeOut(marker),
                  focus(panels.left_frame, False), focus(panels.right_frame), run_time=1.53)
        self.finish()


class S04Centromere(SpokenScene):
    def construct(self):
        back, panels = parent_backdrop()
        panels.right_frame.set_fill(ACTIVE)
        rods = VGroup(*[chromosome(x, .24, a) for a, x in enumerate(PARENT_X, 1)])
        numbers = parent_numbers()
        self.add(back, rods, numbers, schematic())
        self.at("now put that")
        self.play(*[Transform(r[0], chromosome(x, .24, 0, pinched=True)[0])
                    for x, r in zip(PARENT_X, rods)], run_time=1.16)
        self.play(*[r[1].animate.shift(DOWN * .35) for r in rods],
                  focus(panels.right_frame, False), run_time=1.38)
        heading = caption("Chromosome 21 centromere", 34, YELLOW)
        self.at("chromosome 21 centromere")
        self.play(FadeIn(heading), run_time=.48)
        self.at("before division")
        twins = VGroup(*[sister_pair(x, .24, a) for a, x in enumerate(PARENT_X, 1)])
        for a, (rod, target, number) in enumerate(zip(rods, twins, numbers), 1):
            sibling = rod.copy()
            self.add(sibling)
            pair_numbers = VGroup(*[label(str(a), part[1].get_x(), -1.97, 31, ALLELES[a])
                                    for part in target[:2]])
            self.play(Transform(rod, target[0]), Transform(sibling, target[1]),
                      GrowFromCenter(target[2]), swap(number, pair_numbers, 1.13), run_time=1.16)
        self.at("sister copies joined")
        self.play(focus(panels.left_frame), focus(panels.right_frame),
                  *[pair[2].animate.set_stroke(width=15) for pair in twins], run_time=2.2)
        self.at("homologues can carry")
        different = caption("Homologues can differ", 34, PURPLE)
        self.play(swap(heading, different, .57), focus(panels.left_frame, False), run_time=.68)
        mother = VGroup(*[bands for target in twins[2:] for bands in
                          (target[0][1].copy(), target[1][1].copy())])
        self.add(mother)
        self.play(*[b.animate.stretch(1.53, 1) for b in mother],
                  rate_func=there_and_back, run_time=1.86)
        self.at("while sister copies")
        usual = caption("Sister copies usually match", 34)
        self.play(swap(different, usual, .58), focus(panels.right_frame, False), run_time=1.08)
        self.at("distinguishable dna alleles")
        self.play(LaggedStart(*[b.animate.stretch(1.30, 1) for b in mother], lag_ratio=.24),
                  focus(panels.right_frame), run_time=2.0)
        self.at("each inherited chromosome")
        self.play(FadeOut(usual), FadeOut(mother), focus(panels.right_frame, False), run_time=.91)
        self.finish()


def prediction_board():
    stage = board()
    panels = VGroup(inset(-3.04, 1.67, 5.8, 2.75), inset(3.04, 1.67, 5.8, 2.75),
                    inset(0, -1.18, 6.85, 2.77))
    headings = VGroup(label("Father", -3.04, 2.62, 34, BLUE),
                      label("Mother", 3.04, 2.62, 34, PURPLE),
                      label("Child A", -.27, -.18, 34))
    parent_x = (-4.03, -2.05, 2.05, 4.03)
    child_x = (-1.56, 0, 1.56)
    parents = VGroup(*[chromosome(x, 1.64, a, .47, .40, True)
                       for a, x in enumerate(parent_x, 1)])
    parent_ids = VGroup(*[label(str(a), x, .62, 31, ALLELES[a])
                          for a, x in enumerate(parent_x, 1)])
    child = VGroup(*[chromosome(x, -1.31, a, .40, .40, True)
                     for x, a in zip(child_x, (1, 3, 4))])
    child_ids = VGroup(*[label(str(a), x, -2.19, 31, ALLELES[a])
                         for x, a in zip(child_x, (1, 3, 4))])
    backdrop = VGroup(stage, panels, headings, parents, parent_ids, schematic())
    return backdrop, child, child_ids


def predict_card():
    return question_card(QUESTION, y=QUESTION_Y, size=36)


class S05PredictQ(SpokenScene):
    def construct(self):
        back, child, child_ids = prediction_board()
        self.add(back)
        self.at("test this rule")
        panels = back[1]
        self.play(focus(panels[2]), run_time=1.82)
        self.at("the father carries")
        self.play(*[m[1].animate(rate_func=there_and_back).stretch(1.46, 1) for m in back[3][:2]],
                  focus(panels[0]), focus(panels[2], False), run_time=1.95)
        self.at("and the mother")
        self.play(*[m[1].animate(rate_func=there_and_back).stretch(1.46, 1) for m in back[3][2:]],
                  focus(panels[1]), focus(panels[0], False), run_time=1.78)
        self.at("a inherits alleles", lead=.85)
        # The child bars enter together before the allele identities settle into place.
        self.play(LaggedStart(*[FadeIn(m, shift=DOWN * 1.25) for m in child],
                             lag_ratio=.28), focus(panels[1], False), run_time=1.30)
        self.play(LaggedStart(*[FadeIn(t) for t in child_ids], lag_ratio=.41),
                  focus(panels[2]), run_time=1.65)
        self.at("which parents supplied")
        self.play(FadeIn(predict_card()), focus(panels[2], False), run_time=1.05)
        self.at("and which classical")
        self.play(focus(panels[2]), run_time=1.71)
        self.finish()


class S06PredictPause(PredictPause):
    QUESTION = QUESTION
    CARD = {"y": QUESTION_Y, "size": 36}
    RING_AT = (3.73, -2.98, 0)
    def construct(self):
        self.add(self.backdrop(), predict_card())
        # The supplied 4.5-second audio already contains the full thinking pause.
        ring, sweep = countdown(self.narration_s, center=self.RING_AT, radius=.32)
        self.add(ring)
        self.play(sweep)

    def backdrop(self):
        back, child, numbers = prediction_board()
        back[1][2].set_fill(ACTIVE)
        return VGroup(back, child, numbers)


def trace_path(points, color):
    return VMobject(color=color, stroke_width=5).set_points_as_corners(
        [point(x, y) for x, y in points])


def maternal_pairs(x0=-2.38, x1=2.38, y=.36, locus=.40):
    return VGroup(sister_pair(x0, y, 3, 1.25, locus),
                  sister_pair(x1, y, 4, 1.25, locus))


class S07PredictAnswer(SpokenScene):
    def construct(self):
        back, child, child_ids = prediction_board()
        prompt = predict_card()
        panels = back[1]
        panels[2].set_fill(ACTIVE)
        self.add(back, child, child_ids, prompt)
        self.at("trace each allele")
        self.play(FadeOut(prompt), focus(panels[2], False), run_time=.67)
        # Run paths between the two rows, clear of the allele numbers and Child A heading.
        father = trace_path([(-1.56, -.66), (-1.56, -.26), (-2.88, -.04), (-4.49, .29), (-4.40, 1.75)], BLUE)
        mother3 = trace_path([(0.18, -.66), (1.11, -.35), (1.24, .10), (1.63, .35), (1.73, 1.75)], PURPLE)
        mother4 = trace_path([(1.70, -.67), (2.44, -.35), (3.64, -.03), (4.45, .28), (4.40, 1.75)], ORANGE)
        self.at("allele 1 comes")
        self.play(Create(father), focus(panels[0]), run_time=1.43)
        self.at("while alleles 3")
        self.play(LaggedStart(Create(mother3), Create(mother4), lag_ratio=.44),
                  focus(panels[0], False), focus(panels[1]), run_time=2.03)
        self.at("so the mother")
        self.play(back[1][1].animate.set_stroke(PURPLE, 5), run_time=.55)
        pairs = maternal_pairs()
        frames = TwoPanel("Meiosis I", "Meiosis II", colors=(PURPLE, BLUE), top=3.05,
                          bottom=-2.43, width=12.0, size=35)
        for frame in (frames.left_frame, frames.right_frame):
            frame.set_fill(BOARD, 1).set_stroke("#50627C", 2)
        left = maternal_pairs(-4.23, -1.97, .26)
        right = sister_pair(3.10, .26, 3, 1.25)
        self.at("meiosis 1 parts", lead=.85)
        self.play(FadeOut(VGroup(father, mother3, mother4, back[1], back[2], back[3], back[4],
                                 child, child_ids)), run_time=.37)
        self.play(FadeIn(frames), FadeIn(left), FadeIn(right), run_time=.49)
        li = label("Homologues part", -3.10, -2.04, 30, PURPLE)
        ri = label("Sisters part", 3.10, -2.04, 30, BLUE)
        self.play(left[0].animate.shift(LEFT * .39), left[1].animate.shift(RIGHT * .39),
                  FadeIn(li), focus(frames.left_frame), run_time=1.10)
        self.at("and meiosis 2")
        self.play(right[0].animate.shift(LEFT * .55), right[1].animate.shift(RIGHT * .55),
                  FadeOut(right[2]), FadeIn(ri), focus(frames.left_frame, False),
                  focus(frames.right_frame), run_time=1.48)
        self.at("receiving both 3")
        self.play(FadeOut(VGroup(frames, li, ri, left, right)), FadeIn(pairs), run_time=.55)
        inward = RIGHT * 1.03
        pair_ids = VGroup(label("3", -2.38, 2.71, 36, PURPLE).shift(inward),
                          label("4", 2.38, 2.71, 36, ORANGE).shift(-inward))
        self.play(FadeIn(pair_ids[0], shift=inward), FadeIn(pair_ids[1], shift=-inward),
                  pairs[0].animate.shift(inward), pairs[1].animate.shift(-inward), run_time=1.45)
        self.at("mother's homologs")
        self.play(FadeOut(pair_ids), run_time=.28)
        egg = Ellipse(width=6.05, height=4.72, fill_color=BOARD, fill_opacity=1,
                      stroke_color=PURPLE, stroke_width=4).move_to(point(0, .18)).set_z_index(-1)
        # Add the egg above the board, and keep the chromosome cartoons in front of it.
        back[0].set_z_index(-2)
        self.play(FadeOut(pairs[0][0], shift=LEFT * 1.04), FadeOut(pairs[1][1], shift=RIGHT * 1.04),
                  FadeOut(pairs[0][2]), FadeOut(pairs[1][2]), run_time=.72)
        self.play(GrowFromCenter(egg), pairs[0][1].animate.shift(LEFT * .35 + DOWN * .14),
                  pairs[1][0].animate.shift(RIGHT * .35 + DOWN * .14), run_time=1.03)
        self.at("a meiosis 1 error")
        self.play(FadeIn(caption("Egg receives 3 and 4 · Meiosis I error", 34, YELLOW)), run_time=.67)
        self.finish()


class S08Limits(SpokenScene):
    def construct(self):
        left_x, right_x = -2.38, 2.38
        stage = board()
        field = inset(0, .28, 11.72, 5.28)
        pairs = maternal_pairs()
        self.add(stage, field, pairs, schematic())
        inner = (pairs[0][1], pairs[1][0])
        all_bands = [pair[i][1] for pair in pairs for i in (0, 1)]
        self.at("one condition")
        self.play(*[band.animate.shift(UP * 1.06) for band in all_bands], focus(field), run_time=2.3)
        self.at("a crossover exchanges")
        # The inner chromatids are from different homologues. Split their arms
        # at the exchange site, above the centromere and below the distant marker.
        cut_y = 1.12
        center_y = .36
        scale = 1.25
        top_y = center_y + 1.53 * scale
        shoulder = .28 * scale
        end_half = .32 * scale
        shoulder_half = .35 * scale
        pinch_half = .23 * scale
        cut_half = np.interp(cut_y, (center_y + shoulder, top_y), (shoulder_half, end_half))
        tip_outline = [(-end_half, top_y), (end_half, top_y),
                       (cut_half, cut_y), (-cut_half, cut_y)]
        lower_outline = [(-cut_half, cut_y), (cut_half, cut_y),
                         (shoulder_half, center_y + shoulder), (pinch_half, center_y),
                         (shoulder_half, center_y - shoulder), (end_half, center_y - 1.53 * scale),
                         (-end_half, center_y - 1.53 * scale), (-shoulder_half, center_y - shoulder),
                         (-pinch_half, center_y), (-shoulder_half, center_y + shoulder)]
        tips = VGroup()
        for rod in inner:
            x = rod[1].get_x()
            style = dict(fill_color=BODY, fill_opacity=1, stroke_color=EDGE, stroke_width=2)
            arm = Polygon(*[point(x + u, y) for u, y in tip_outline], **style)
            tips.add(VGroup(arm, rod[1].copy()))
            lower = Polygon(*[point(x + u, y) for u, y in lower_outline], **style)
            rod[0].become(lower)
            rod[1].set_opacity(0)
        self.add(tips)
        cut = Line(point(-1.95, cut_y), point(1.95, cut_y), stroke_width=3,
                   color=YELLOW)
        self.play(Create(cut), run_time=.65)
        delta = tips[1].get_x() - tips[0].get_x()
        self.play(tips[0].animate(path_arc=-.76).shift(RIGHT * delta),
                  tips[1].animate(path_arc=-.76).shift(LEFT * delta),
                  FadeOut(cut), focus(field, False), run_time=2.42)
        new_pairs = maternal_pairs(locus=1.248)
        new_pairs[0][1][1].set_fill(ORANGE)
        new_pairs[1][0][1].set_fill(PURPLE)
        self.remove(tips, pairs)
        self.add(new_pairs)
        self.at("between marker")
        gap = BraceBetweenPoints(point(-3.47, .36), point(-3.47, 1.91), direction=LEFT,
                                 color=YELLOW)
        self.play(GrowFromCenter(gap), focus(field), run_time=1.62)
        self.at("make sister copies differ")
        nums = VGroup(*[label(str(a), x, -2.09, 35, ALLELES[a])
                        for a, x in zip((3, 4, 3, 4),
                                        (left_x - .5, left_x + .5, right_x - .5, right_x + .5))])
        self.play(LaggedStart(*[FadeIn(m) for m in nums], lag_ratio=.31),
                  focus(field, False), run_time=1.86)
        self.at("then meiosis ii")
        caution = caption("Meiosis II can mimic I", 34, YELLOW)
        self.play(FadeIn(caution), focus(field), run_time=.83)
        self.play(*[rod[1].animate.stretch(1.40, 1) for pair in new_pairs for rod in pair[:2]],
                  rate_func=there_and_back, run_time=1.4)
        self.at("and the reverse")
        reverse = caption("Meiosis I can mimic II", 34, YELLOW)
        self.play(swap(caution, reverse, .73))
        self.at("markers close", lead=0)
        target = maternal_pairs()
        self.play(FadeOut(nums), FadeOut(reverse), run_time=.40)
        short_gap = BraceBetweenPoints(point(-3.47, .36), point(-3.47, .86),
                                       direction=LEFT, color=YELLOW)
        self.play(Transform(new_pairs, target), Transform(gap, short_gap),
                  focus(field, False), run_time=2.02)
        self.at("human eggs also")
        note = caption("Human eggs can depart from this model", 33)
        self.play(FadeIn(note), FadeOut(gap), focus(field), run_time=1.14)
        self.play(*[pair[2].animate.set_stroke(YELLOW, 18) for pair in new_pairs],
                  rate_func=there_and_back, run_time=2.63)
        self.finish()


BIRD_PATTERN = (
    (1, 4, 1, 1, 4, 1, 2, 1),
    (3, 3, 2, 4, 3, 2, 3, 4),
    (1, 1, 1, 1, 1, 1, 2, 1),
)


def finch_strip(x, y, pitch=.52, mode="social"):
    """Schematic bands; the chick's two bands at each locus are drawn side by side."""
    rows = []
    for row, pattern in enumerate(BIRD_PATTERN):
        bands = VGroup()
        for i, allele in enumerate(pattern):
            px = x + (i - 3.5) * pitch
            py = y - row * .37
            if row == 0 and mode == "genetic":
                allele = BIRD_PATTERN[2][i]
            if row == 2:
                bands.add(VGroup(stripe(allele, px - .093, py, .15, .23),
                                 stripe(BIRD_PATTERN[1][i], px + .093, py, .15, .23)))
            else:
                bands.add(VGroup(stripe(allele, px, py, .32, .23)))
        rows.append(bands)
    return VGroup(*rows)


def finch_board(mode):
    stage = board()
    panel = inset(-2.91, .08, 6.44, 5.84)
    screen = inset(3.12, .08, 5.42, 5.84)
    heading = label("Daphne Major", -2.91, 2.56, 36, GOLD)
    birds = VGroup(bird(-4.55, 1.37, BLUE, .84),
                   bird(-1.29, 1.37, PURPLE, .84, -1),
                   bird(-2.91, .36, "#C8ABB5", .57, -1))
    cradle = nest(-2.91, -.10, 1.78)
    father_title = "Social father" if mode == "social" else "Genetic father"
    names = VGroup(*[label(name, -4.95, -.77 - i * .37, 28, color)
                     for i, (name, color) in enumerate(zip((father_title, "Mother", "Chick"),
                                                           (BLUE, PURPLE, TEXT)))])
    names.arrange(DOWN, buff=0, aligned_edge=LEFT)
    for i, name in enumerate(names):
        name.align_to(point(-5.95, 0), LEFT).set_y(-.77 - i * .47)
    strips = finch_strip(-1.56, -.77, pitch=.38, mode=mode)
    for i, row in enumerate(strips):
        row.shift(DOWN * i * .10)
    loci = label("Eight microsatellite loci", -2.91, -2.31, 31)
    return VGroup(stage, panel, screen, heading, cradle), birds, names, strips, loci


def finch_plot():
    return Plot(box=(1.35, 5.35, -1.34, 1.61), xr=(0, 1), yr=(0, 1),
                xlabel="Parent trait", ylabel="Chick trait", label_size=29, color=TEXT)


def slope_line(plot, slope, color):
    return plot.curve(lambda x: slope * x, color=color, width=7)


def finch_curve_tags():
    return VGroup(label("Father", 5.05, -.34, 28, BLUE),
                  label("Mother", 4.90, 1.49, 28, PURPLE))


# Normalize the PC1-bill father–offspring slope with extra-pair young excluded
# to 0.60. The other lines show the relative changes from the full sample
# (Table 3) and the checked single-cohort maternal comparison (Table 4).
# Keller et al. (2001), https://www.nature.com/articles/6889000
CHECKED_SLOPE = .60
PAIRED_SLOPE = CHECKED_SLOPE / 1.29
MATERNAL_SLOPE = CHECKED_SLOPE * 1.41


class S09UnlockedBirds(SpokenScene):
    def construct(self):
        back, birds, names, strip, loci = finch_board("social")
        self.add(back, birds, schematic())
        self.at("dna markers also")
        bob(birds[2], amp=.06, speed=2.6)
        morsel = Dot(point(-3.79, 1.48), radius=.093, color=YELLOW)
        self.add(morsel)
        self.play(birds[0].animate.rotate(-.25).shift(RIGHT * .31), focus(back[1]),
                  morsel.animate.move_to(point(-3.30, .53)), run_time=2.6)
        self.play(FadeOut(morsel), birds[0].animate.rotate(.25).shift(LEFT * .31),
                  focus(back[1], False), run_time=1.35)
        self.at("in 2001")
        credit = label("Keller, Grant, Grant\nand Petren, 2001", 3.12, 2.08, 33, GOLD)
        self.play(FadeIn(credit), focus(back[2]), run_time=1.21)
        self.play(LaggedStart(*[FadeIn(n) for n in names], lag_ratio=.45), run_time=1.61)
        self.at("typed birds at")
        columns = [AnimationGroup(*[GrowFromCenter(row[k]) for row in strip]) for k in range(8)]
        self.play(LaggedStart(*columns, lag_ratio=.23), focus(back[1]), focus(back[2], False),
                  run_time=2.37)
        self.play(FadeIn(loci), run_time=.40)
        self.at("twenty percent", lead=.9)
        tracker = ValueTracker(0)
        gauge = dial(tracker, center=point(3.12, -.11), radius=1.52,
                     label="Extra-pair young", color=GOLD)
        self.add(gauge)
        self.play(tracker.animate.set_value(.2), focus(back[1], False), focus(back[2]), run_time=.9)
        self.at("their social father")
        mismatch = VGroup(*[SurroundingRectangle(VGroup(strip[0][i], strip[2][i][0]),
                                                  color=RED, buff=.045, stroke_width=3)
                            for i in (1, 4)])
        self.play(LaggedStart(*[Create(m) for m in mismatch], lag_ratio=.35),
                  focus(back[1]), focus(back[2], False), run_time=1.23)
        self.at("in this study", lead=.65)
        self.play(FadeOut(mismatch), FadeOut(gauge), FadeOut(credit), run_time=.64)
        plot = finch_plot()
        title = label("Trait resemblance", 3.12, 2.52, 32)
        line = slope_line(plot, CHECKED_SLOPE, BLUE)
        self.play(FadeIn(plot), FadeIn(title), Create(line), focus(back[1], False), run_time=1.76)
        self.at("who were not theirs")
        wrong = label("Social fathers", 3.34, -2.26, 31, BLUE)
        self.play(FadeIn(wrong), Transform(line, slope_line(plot, PAIRED_SLOPE, BLUE)),
                  focus(back[2]), run_time=2.75)
        self.finish()


def finch_links():
    return (trace_path([(-4.01, .97), (-3.35, .70)], BLUE).set_stroke(width=3),
            trace_path([(-1.81, .97), (-2.47, .70)], PURPLE).set_stroke(width=8))


class S10UnlockedMaternal(SpokenScene):
    def construct(self):
        back, birds, names, strip, loci = finch_board("social")
        _, _, corrected, matches, _ = finch_board("genetic")
        self.add(back, birds, names, strip, loci, schematic())
        plot = finch_plot()
        title = label("Trait resemblance", 3.12, 2.52, 32)
        line = slope_line(plot, PAIRED_SLOPE, BLUE)
        status = label("Social fathers", 3.34, -2.26, 31, BLUE)
        back[2].set_fill(ACTIVE)
        self.add(plot, title, line, status)
        self.at("even after dna")
        new_status = label("Genetic fathers", 3.34, -2.26, 31, BLUE)
        self.play(swap(names[0], corrected[0], .85), swap(status, new_status, .85),
                  Transform(strip[0], matches[0]), focus(back[1]), focus(back[2], False),
                  Transform(line, slope_line(plot, CHECKED_SLOPE, BLUE)), run_time=2.03)
        self.at("chicks still resembled")
        paternal, maternal = finch_links()
        father_tag, mother_tag = finch_curve_tags()
        self.play(FadeOut(new_status), Create(paternal), Create(maternal),
                  focus(back[1], False), run_time=1.25)
        mother_line = slope_line(plot, MATERNAL_SLOPE, PURPLE)
        self.play(Create(mother_line), FadeIn(father_tag), FadeIn(mother_tag),
                  focus(back[2]), run_time=1.82)
        self.at("as maternal effects")
        self.play(focus(back[1]), focus(back[2], False), run_time=1.41)
        self.at("like egg size")
        egg = EggIcon().move_to(point(-1.50, .81))
        seed = Ellipse(width=.20, height=.31, color=GOLD,
                       fill_opacity=1, stroke_width=0).rotate(-.4).move_to(point(-1.44, .88))
        self.add(egg)
        self.play(egg.animate.shift(LEFT * 1.15 + DOWN * .22), run_time=.92)
        self.play(FadeOut(egg), FadeIn(seed), run_time=.35)
        self.play(seed.animate.move_to(point(-2.63, .56)), birds[1].animate.rotate(.15).shift(LEFT * .16),
                  focus(back[1], False), run_time=1.15)
        self.play(FadeOut(seed), run_time=.27)
        self.at("a maternal effect tracking")
        # Keep the genetic-father comparison fixed while the maternal curve builds.
        slope = ValueTracker(CHECKED_SLOPE)
        rising = always_redraw(lambda: slope_line(plot, slope.get_value(), PURPLE))
        self.remove(mother_line)
        self.add(rising)
        change = label("Maternal effects", 3.34, -2.26, 31, PURPLE)
        self.play(slope.animate(rate_func=linear).set_value(MATERNAL_SLOPE), focus(back[2]),
                  Succession(FadeIn(change, run_time=.60), Wait(3.07)),
                  birds[1].animate.rotate(-.15).shift(RIGHT * .16), run_time=3.67)
        self.finish()


class EggIcon(Ellipse):
    def __init__(self):
        super().__init__(width=.25, height=.35, color="#F0DED1", fill_opacity=1, stroke_width=0)


class S11UnlockedClose(SpokenScene):
    def construct(self):
        back, birds, names, strip, loci = finch_board("genetic")
        back[2].set_fill(ACTIVE)
        plot = finch_plot()
        previous = VGroup(plot, label("Trait resemblance", 3.12, 2.52, 32),
                          slope_line(plot, CHECKED_SLOPE, BLUE),
                          slope_line(plot, MATERNAL_SLOPE, PURPLE),
                          finch_curve_tags(),
                          label("Maternal effects", 3.34, -2.26, 31, PURPLE), *finch_links())
        self.add(back, birds, names, strip, loci, schematic(), previous)
        right_title = label("Chromosome 21", 3.12, 2.56, 36, GOLD)
        upper = VGroup(chromosome(1.52, 1.28, 1, .49, .40, True),
                       chromosome(3.12, 1.28, 3, .49, .40, True),
                       chromosome(4.72, 1.28, 4, .49, .40, True))
        lower = VGroup(*[chromosome(x, -1.30, 0, .55, .40, True) for x in (1.52, 3.12, 4.72)])
        self.at("alongside wild parentage")
        self.play(LaggedStart(*[m.animate.stretch(1.3, 1) for m in strip[2]],
                             lag_ratio=.24, rate_func=there_and_back),
                  FadeOut(previous), focus(back[1]), focus(back[2], False), run_time=1.95)
        self.at("centromere linked markers")
        self.play(LaggedStart(*[FadeIn(m) for m in upper], lag_ratio=.40), run_time=1.66)
        self.play(FadeIn(right_title), FadeIn(lower), focus(back[2]), run_time=1.35)
        self.at("they identify which")
        labels = VGroup(label("Father", 1.52, .22, 29, BLUE),
                        label("Mother", 3.92, .22, 29, PURPLE))
        self.play(FadeIn(labels), focus(back[1], False), run_time=.98)
        self.play(upper[1][1].animate.stretch(1.45, 1),
                  upper[2][1].animate.stretch(1.45, 1), rate_func=there_and_back, run_time=1.73)
        self.at("which classical division")
        division = label("Meiosis I error", 3.12, -2.55, 32, YELLOW)
        self.play(FadeIn(division), focus(back[2], False), run_time=1.20)
        self.at("wherever parental alleles")
        self.play(FadeOut(division), FadeOut(labels), focus(back[1]), run_time=1.12)
        self.at("reading those dna")
        tags = VGroup(*[r[1].copy() for r in upper])
        bird_tags = VGroup(strip[0][3][0].copy(), strip[1][3][0].copy())
        self.add(tags, bird_tags)
        targets = (strip[2][3][0], strip[2][3][1])
        moves = [Transform(tag, part[1].copy().set_fill(ALLELES[allele]))
                 for tag, part, allele in zip(tags, lower, (1, 3, 4))]
        # Fit each copy to its own lane before the two bands converge on the chick row.
        bird_moves = [
            Succession(Transform(tag, target.copy().set_y(tag.get_y()), run_time=.42),
                       Transform(tag, target.copy(), run_time=2.62))
            for tag, target in zip(bird_tags, targets)
        ]
        self.play(LaggedStart(*moves, lag_ratio=.35),
                  *bird_moves,
                  focus(back[2]), run_time=3.04)
        self.finish()


class S12End(EndCard):
    LINE = "Distinguishable DNA alleles trace genetic parentage and each inherited chromosome."
