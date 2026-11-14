"""How One Set Becomes Two — cell cycle and mitosis.

COLOR MAP
  BLUE       guide chromosome
  LIGHT_BLUE its homologous partner
  ORANGE     second chromosome pair
  LIGHT_ORANGE its homologous partner
  GREEN      spindle fibres
  YELLOW     nuclear envelopes
  TEAL       cell boundary and cytokinesis structures
  TEXT       phase labels and neutral text

Chromosomes are schematic labelled cartoons, never molecular structures.
"""
from bp_parts import *


LIGHT_BLUE = "#9ADBE8"
ORANGE = "#F29E4C"
LIGHT_ORANGE = "#F7C98B"
CHROM_COLORS = (BLUE, LIGHT_BLUE, ORANGE, LIGHT_ORANGE)
CELL_C = np.array([0.0, -0.25, 0.0])
CELL_W, CELL_H = 9.2, 5.25


def rod(color=BLUE, height=1.25, width=0.28):
    """One condensed chromosome/chromatid cartoon."""
    return RoundedRectangle(
        corner_radius=0.12, width=width, height=height,
        stroke_color=color, stroke_width=3,
        fill_color=color, fill_opacity=0.82,
    )


def copied_chromosome(color=BLUE, height=1.25, spread=0.22, crossed=False):
    """Two sister chromatids and their shared centromere."""
    if crossed:
        a = rod(color, height, 0.24).rotate(0.34)
        b = rod(color, height, 0.24).rotate(-0.34)
    else:
        a = rod(color, height, 0.24).shift(LEFT * spread)
        b = rod(color, height, 0.24).shift(RIGHT * spread)
    center = Circle(radius=0.105, color=TEXT, stroke_width=3, fill_color=BG, fill_opacity=1)
    g = VGroup(a, b, center)
    g.left_sister, g.right_sister, g.centromere = a, b, center
    return g


def cell_outline(width=CELL_W, height=CELL_H, center=CELL_C, opacity=0.16):
    return Ellipse(
        width=width, height=height, color=TEAL, stroke_width=5,
        fill_color=TEAL, fill_opacity=opacity,
    ).move_to(center)


def nucleus_outline(width=4.8, height=3.9, center=CELL_C):
    return Ellipse(
        width=width, height=height, color=YELLOW, stroke_width=4,
        fill_color=YELLOW, fill_opacity=0.11,
    ).move_to(center)


def loose_set(center=CELL_C, scale=1.0):
    """The same four unreplicated rods used whenever interphase is shown."""
    offsets = ((-1.05, 0.55, 0.12), (-0.35, -0.55, -0.14),
               (0.45, 0.55, 0.16), (1.15, -0.5, -0.12))
    rods = VGroup()
    for color, (x, y, angle) in zip(CHROM_COLORS, offsets):
        r = rod(color, (1.25 if color in (BLUE, LIGHT_BLUE) else 0.95) * scale, 0.27 * scale)
        r.rotate(angle).move_to(center + np.array([x, y, 0]) * scale)
        rods.add(r)
    rods.guide = rods[0]
    return rods


def copied_set(center=ORIGIN, crossed=False, scale=1.0):
    """The same four copied chromosomes, arranged as a roomy nucleus view."""
    offsets = ((-1.55, 0.7), (-0.5, -0.75), (0.55, 0.7), (1.55, -0.7))
    out = VGroup()
    for color, (x, y) in zip(CHROM_COLORS, offsets):
        h = (1.45 if color in (BLUE, LIGHT_BLUE) else 1.12) * scale
        c = copied_chromosome(color, h, 0.2 * scale, crossed=crossed).scale(scale)
        c.move_to(center + np.array([x, y, 0]) * scale)
        out.add(c)
    out.guide = out[0]
    return out


def metaphase_world(question=False, blank_stubs=False, fibres=False, lanes=False):
    """Carried world for the predict, reveal, metaphase, and anaphase scenes."""
    boundary = cell_outline()
    pole_l = Circle(radius=0.22, color=GREEN, stroke_width=4).move_to([-4.0, -0.25, 0])
    pole_r = Circle(radius=0.22, color=GREEN, stroke_width=4).move_to([4.0, -0.25, 0])
    ys = (1.25, 0.3, -0.65, -1.55)
    heights = (1.25, 1.25, 0.95, 0.95)
    chroms = VGroup(*[
        copied_chromosome(col, h, 0.2, crossed=True).move_to([0, y, 0])
        for col, h, y in zip(CHROM_COLORS, heights, ys)
    ])
    g = VGroup(boundary, pole_l, pole_r)
    lane_group = VGroup()
    if lanes:
        for col, y in zip(CHROM_COLORS, ys):
            lane_group.add(
                DashedLine([-3.55, y, 0], [-0.5, y, 0], color=col, stroke_opacity=0.25),
                DashedLine([0.5, y, 0], [3.55, y, 0], color=col, stroke_opacity=0.25),
            )
        g.add(lane_group)
    fiber_group = VGroup()
    if fibres:
        for c in chroms:
            left_fiber = Line(pole_l.get_center(), c.left_sister.get_center(), color=GREEN, stroke_width=3)
            right_fiber = Line(pole_r.get_center(), c.right_sister.get_center(), color=GREEN, stroke_width=3)
            left_fiber.add_updater(
                lambda m, c=c: m.put_start_and_end_on(pole_l.get_center(), c.left_sister.get_center())
            )
            right_fiber.add_updater(
                lambda m, c=c: m.put_start_and_end_on(pole_r.get_center(), c.right_sister.get_center())
            )
            fiber_group.add(left_fiber, right_fiber)
        g.add(fiber_group)
    g.add(chroms)
    stubs = VGroup()
    if blank_stubs:
        guide = chroms[0]
        stubs.add(
            Line(guide.left_sister.get_left() + LEFT * 0.05, guide.left_sister.get_left() + LEFT * 0.65,
                 color=BLUE, stroke_width=7),
            Line(guide.right_sister.get_right() + RIGHT * 0.05, guide.right_sister.get_right() + RIGHT * 0.65,
                 color=BLUE, stroke_width=7),
        )
        g.add(stubs)
    q = None
    if question:
        q = fit_text("Where must the blue sister chromatids go?", max_w=10.8, size=30, color=GOLD)
        q.move_to([0, 3.35, 0])
        g.add(q)
    g.boundary, g.poles, g.chroms = boundary, VGroup(pole_l, pole_r), chroms
    g.fibres, g.lanes, g.stubs, g.question = fiber_group, lane_group, stubs, q
    return g


def rule_badge():
    b = chip("copy first • separate copies", GOLD, 25)
    b.move_to([3.9, 3.25, 0])
    return b


class S00Hook(SpokenScene):
    def construct(self):
        cell = cell_outline(8.2, 5.25)
        nuc = nucleus_outline(5.1, 4.0)
        chroms = loose_set(scale=1.35)
        daughters = VGroup(
            Ellipse(width=3.8, height=4.4, color=TEAL, stroke_opacity=0.25).move_to([-2.6, -0.25, 0]),
            Ellipse(width=3.8, height=4.4, color=TEAL, stroke_opacity=0.25).move_to([2.6, -0.25, 0]),
        )
        question = T("?", 86, GOLD).move_to([0, 2.75, 0])
        self.at("How can one cell")
        self.play(FadeIn(cell), FadeIn(nuc), FadeIn(chroms), run_time=1.0)
        self.play(cell.animate.stretch(1.08, 0), FadeIn(daughters), GrowFromCenter(question), run_time=2.2)
        self.play(daughters[0].animate.shift(LEFT * 0.28), daughters[1].animate.shift(RIGHT * 0.28),
                  cell.animate.stretch(1.05, 0), nuc.animate.stretch(1.04, 0),
                  run_time=2.7, rate_func=there_and_back)
        self.at("Watch one blue chromosome")
        spotlight = Circle(radius=0.62, color=BLUE, stroke_width=6).move_to(chroms.guide)
        self.play(FadeOut(question), Create(spotlight), chroms.guide.animate.scale(1.3),
                  cell.animate.stretch(1.035, 1), run_time=1.3, rate_func=there_and_back)
        self.play(chroms.animate.scale(1.08), daughters.animate.scale(1.025),
                  run_time=2.1, rate_func=there_and_back)
        self.at("Its partners will stay visible")
        self.play(chroms[1:].animate.set_opacity(0.72), spotlight.animate.scale(1.12), run_time=1.0)
        self.play(chroms.animate.rotate(0.18), daughters.animate.scale(1.035),
                  spotlight.animate.rotate(0.18).scale(1.08), run_time=2.8, rate_func=there_and_back)
        self.finish()


class S01Title(TitleCard):
    LESSON = "The Cell Cycle and Mitosis"
    TITLE = "How One Set Becomes Two"

    def construct(self):
        title = fit_text(self.TITLE, max_w=9.5, size=54, font=TITLE_FONT).move_to([-0.6, 0.25, 0])
        guide = rod(BLUE, 2.15, 0.42).move_to([5.0, 0.15, 0])
        self.play(Write(title), FadeIn(guide, shift=UP * 0.2), run_time=0.65)
        self.play(Rotate(guide, angle=0.55), rate_func=there_and_back, run_time=0.9)
        self.play(FadeOut(VGroup(title, guide)), run_time=0.35)
        self.finish()


class S02Interphase(SpokenScene):
    def construct(self):
        cell = cell_outline(4.6, 3.7)
        nuc = nucleus_outline(3.35, 2.75)
        chroms = loose_set(scale=0.78)
        ring = VGroup(*[
            Arc(radius=2.75, start_angle=a, angle=ang, color=col, stroke_width=14)
            for a, ang, col in ((PI / 2, -1.55, TEAL), (-0.98, -1.25, BLUE), (-2.23, -1.05, GOLD), (-3.28, -0.43, GREY))
        ]).move_to(CELL_C)
        labels = VGroup(
            T("G1", 30, TEAL).move_to([2.7, 1.65, 0]),
            T("S", 30, BLUE).move_to([2.65, -2.0, 0]),
            T("G2", 30, GOLD).move_to([-1.35, -3.2, 0]),
            T("M", 30, GREY).move_to([-2.8, 1.5, 0]),
        )
        theta = ValueTracker(PI / 2)
        tracker = always_redraw(lambda: Dot(CELL_C + 2.75 * np.array([np.cos(theta.get_value()), np.sin(theta.get_value()), 0]),
                                            radius=0.14, color=TEXT))
        self.at("A new cell enters")
        self.play(FadeIn(cell), FadeIn(nuc), FadeIn(chroms), Create(ring), FadeIn(labels), run_time=1.1)
        self.add(tracker)
        self.at("where it grows")
        self.play(cell.animate.scale(1.08), nuc.animate.scale(1.05),
                  theta.animate.set_value(-0.92), run_time=2.5, rate_func=linear)
        self.at("This busy stretch")
        busy = T("INTERPHASE", 32, TEXT).move_to([0, 3.35, 0])
        self.play(FadeIn(busy), chroms.animate.rotate(0.16), run_time=1.1)
        self.at("Next comes")
        self.play(theta.animate.set_value(-2.2), chroms.animate.rotate(-0.2), run_time=2.2, rate_func=linear)
        self.at("G2 prepares")
        self.play(theta.animate.set_value(-3.25), cell.animate.stretch(1.04, 0), run_time=1.5, rate_func=linear)
        self.finish()


class S03Copy(SpokenScene):
    def construct(self):
        nuc = nucleus_outline(10.2, 5.6)
        singles = loose_set(scale=1.35)
        dna = ValueTracker(4)
        readout = Readout(
            [("chromosome units", lambda: 4, "{:.0f}", TEXT),
             ("DNA copies", lambda: dna.get_value(), "{:.0f}", BLUE)],
            at=[4.2, 3.1, 0], widest=[4, 8], size=24,
        )
        self.at("During S phase")
        self.play(FadeIn(nuc), FadeIn(singles), run_time=0.8)
        self.at("every chromosome is copied")
        self.play(FadeIn(readout), run_time=0.65)
        copies = copied_set(scale=1.0)
        self.at("The blue rod becomes")
        big_guide = copied_chromosome(BLUE, 3.5, 0.5).move_to([-0.8, -0.05, 0])
        self.play(ReplacementTransform(singles[0], big_guide), dna.animate.set_value(5), run_time=1.9)
        cent_label = T("centromere", 28, TEXT).move_to([-2.3, 2.65, 0])
        pointer = Arrow(cent_label.get_bottom(), big_guide.centromere.get_top(), buff=0.14,
                        color=TEXT, stroke_width=3, tip_length=0.16)
        self.at("joined at one centromere")
        self.play(FadeIn(cent_label), GrowArrow(pointer), big_guide.animate.scale(1.08), run_time=1.1)
        self.at("Its partners copy")
        self.play(ReplacementTransform(big_guide, copies[0]),
                  *[ReplacementTransform(singles[i], copies[i]) for i in range(1, 4)],
                  dna.animate.set_value(8), FadeOut(cent_label), FadeOut(pointer), run_time=1.8)
        self.at("The D")
        self.play(Indicate(readout, color=BLUE), run_time=0.8)
        self.at("but each joined pair")
        self.play(*[c.animate.scale(1.14) for c in copies], run_time=2.6, rate_func=there_and_back)
        self.finish()


class S04Predict(SpokenScene):
    def construct(self):
        world = metaphase_world(question=False, blank_stubs=True)
        start = copied_set(crossed=True, scale=0.82)
        self.at("Soon")
        self.play(FadeIn(world.boundary), FadeIn(world.poles), FadeIn(start), run_time=0.8)
        self.play(ReplacementTransform(start, world.chroms), run_time=2.3)
        q = fit_text("Where must the blue sister chromatids go?", max_w=10.8, size=30, color=GOLD).move_to([0, 3.35, 0])
        self.at("Where must the two blue")
        self.play(FadeIn(world.stubs), FadeIn(q), run_time=0.9)
        self.play(world.chroms.animate.stretch(1.08, 0), world.boundary.animate.stretch(1.04, 1),
                  run_time=4.0, rate_func=there_and_back)
        self.at("Hold your answer")
        self.play(Indicate(world.chroms[0], color=BLUE), run_time=0.7)
        self.finish()


class S05Pause(PredictPause):
    QUESTION = "Where must the blue sister chromatids go?"
    SECONDS = 4.5
    CARD = {"y": 3.35, "size": 30, "max_w": 10.8}
    RING_AT = (5.9, -3.05, 0)

    def backdrop(self):
        world = metaphase_world(blank_stubs=True)
        pulse(world.poles[0], base=4.0, amp=1.4, speed=2.1)
        pulse(world.poles[1], base=4.0, amp=1.4, speed=2.1)
        return world


class S06Reveal(SpokenScene):
    def construct(self):
        world = metaphase_world(question=True, blank_stubs=True)
        self.add(world)
        self.at("The blue copies")
        blue_arrows = VGroup(
            Arrow([-0.32, 1.25, 0], [-3.35, 1.25, 0], buff=0.1, color=BLUE, stroke_width=7),
            Arrow([0.32, 1.25, 0], [3.35, 1.25, 0], buff=0.1, color=BLUE, stroke_width=7),
        )
        self.play(FadeOut(world.stubs), GrowArrow(blue_arrows[0]), GrowArrow(blue_arrows[1]), run_time=1.5)
        self.at("The same is true")
        other_arrows = VGroup()
        for col, y in zip(CHROM_COLORS[1:], (0.3, -0.65, -1.55)):
            other_arrows.add(
                Arrow([-0.32, y, 0], [-3.25, y, 0], buff=0.1, color=col, stroke_width=5),
                Arrow([0.32, y, 0], [3.25, y, 0], buff=0.1, color=col, stroke_width=5),
            )
        self.play(LaggedStart(*[GrowArrow(a) for a in other_arrows], lag_ratio=0.12), run_time=1.8)
        self.at("Copy each chromosome first")
        rule = fit_text("Copy each chromosome first; separate the copies so each nucleus gets one.",
                        max_w=11.0, size=29, color=GOLD).move_to([0, 3.35, 0])
        ghosts = VGroup()
        for x in (-3.35, 3.35):
            ghosts.add(VGroup(*[rod(c, 0.6 if i < 2 else 0.46, 0.15).move_to([x + (i - 1.5) * 0.28, -0.25, 0])
                               for i, c in enumerate(CHROM_COLORS)]).set_opacity(0.28))
        ghosts[0].shift(RIGHT * 1.35)
        ghosts[1].shift(LEFT * 1.35)
        self.play(FadeOut(world.question), FadeIn(rule), FadeIn(ghosts), run_time=1.0)
        self.play(ghosts[0].animate.shift(LEFT * 1.35), ghosts[1].animate.shift(RIGHT * 1.35),
                  world.boundary.animate.stretch(1.06, 0), run_time=2.6)
        self.at("That rule preserves")
        badge = rule_badge()
        self.play(ReplacementTransform(rule, badge), Indicate(ghosts, color=GOLD), run_time=1.2)
        self.finish()


class S07Prophase(SpokenScene):
    def construct(self):
        boundary = cell_outline()
        nucleus = nucleus_outline(6.0, 4.35)
        straight = copied_set(scale=0.9)
        badge = rule_badge()
        phase = T("PROPHASE", 34, TEXT).move_to([0, 3.35, 0])
        self.at("M phase begins")
        self.play(FadeIn(boundary), FadeIn(nucleus), FadeIn(straight), FadeIn(phase), FadeIn(badge), run_time=1.0)
        self.at("In prophase")
        thick = copied_set(crossed=True, scale=1.0)
        self.play(ReplacementTransform(straight, thick), run_time=1.8)
        schematic = scope_tag("schematic")
        self.play(FadeIn(schematic), run_time=0.35)
        self.play(thick.animate.scale(1.12).rotate(0.08), nucleus.animate.stretch(1.035, 0),
                  run_time=2.4, rate_func=there_and_back)
        self.at("Green spindle fibers form")
        poles = VGroup(Dot([-4.0, -0.25, 0], radius=0.2, color=GREEN), Dot([4.0, -0.25, 0], radius=0.2, color=GREEN))
        fibers = VGroup()
        for pole, direction in ((poles[0], RIGHT), (poles[1], LEFT)):
            for dy in (-1.45, -0.5, 0.45, 1.4):
                fibers.add(Line(pole.get_center(), pole.get_center() + direction * 2.4 + UP * dy * 0.28,
                                color=GREEN, stroke_width=3))
        self.play(FadeIn(poles), LaggedStart(*[Create(f) for f in fibers], lag_ratio=0.08), run_time=1.8)
        self.at("Near the end")
        fragments = VGroup(*[
            Arc(radius=3.0, start_angle=a, angle=0.48, color=YELLOW, stroke_width=4)
            .stretch(4.35 / 6.0, 1).move_to(CELL_C)
            for a in np.linspace(0, TAU, 8, endpoint=False)
        ])
        self.play(ReplacementTransform(nucleus, fragments), run_time=1.2)
        self.at("opening access")
        dispersal = []
        for f in fragments:
            direction = f.get_center() - CELL_C
            if np.linalg.norm(direction) < 0.01:
                direction = UP
            dispersal.append(f.animate.shift(0.38 * direction / np.linalg.norm(direction)).set_opacity(0.28))
        self.play(*dispersal, fibers.animate.scale(1.08), run_time=2.4, rate_func=there_and_back)
        self.finish()


class S08Metaphase(SpokenScene):
    def construct(self):
        world = metaphase_world(fibres=False, lanes=True)
        start = copied_set(crossed=True, scale=0.92)
        phase = T("METAPHASE", 34, TEXT).move_to([0, 3.35, 0])
        badge = rule_badge()
        self.at("In metaphase")
        self.play(FadeIn(world.boundary), FadeIn(world.poles), FadeIn(start), FadeIn(phase), FadeIn(badge), run_time=0.9)
        fibers = VGroup()
        for c in start:
            fibers.add(Line(world.poles[0].get_center(), c[0].get_center(), color=GREEN, stroke_width=3),
                       Line(world.poles[1].get_center(), c[1].get_center(), color=GREEN, stroke_width=3))
        self.at("spindle fibers line")
        self.play(FadeIn(fibers), FadeIn(world.lanes), ReplacementTransform(start, world.chroms), run_time=2.5)
        settled_fibers = VGroup()
        for c in world.chroms:
            settled_fibers.add(Line(world.poles[0].get_center(), c[0].get_center(), color=GREEN, stroke_width=3),
                               Line(world.poles[1].get_center(), c[1].get_center(), color=GREEN, stroke_width=3))
        self.remove(fibers)
        self.add(settled_fibers)
        self.at("Each sister chromatid")
        self.play(world.chroms[0][0].animate.shift(LEFT * 0.22), world.chroms[0][1].animate.shift(RIGHT * 0.22),
                  world.boundary.animate.stretch(1.035, 0), run_time=1.8, rate_func=there_and_back)
        self.at("The row is not")
        row_mark = DashedLine([0, -2.15, 0], [0, 2.05, 0], color=GREY, stroke_width=3)
        self.play(Create(row_mark), world.chroms.animate.stretch(1.12, 1), run_time=1.7, rate_func=there_and_back)
        self.at("It is the setup")
        self.play(FadeOut(row_mark), world.poles.animate.set_stroke(width=7),
                  world.lanes.animate.set_opacity(0.75), world.boundary.animate.stretch(1.04, 1), run_time=2.5,
                  rate_func=there_and_back)
        self.finish()


class S09Anaphase(SpokenScene):
    def construct(self):
        world = metaphase_world(fibres=True, lanes=True)
        phase = T("ANAPHASE", 34, TEXT).move_to([0, 3.35, 0])
        badge = rule_badge()
        self.add(world, phase, badge)
        sisters = T("sister chromatids", 28, BLUE).move_to([0, 2.65, 0])
        self.at("In anaphase")
        self.play(FadeIn(sisters), run_time=0.55)
        lefts = VGroup(*[c.left_sister for c in world.chroms])
        rights = VGroup(*[c.right_sister for c in world.chroms])
        cents = VGroup(*[c.centromere for c in world.chroms])
        self.at("separate at their centromeres")
        self.play(FadeOut(cents), lefts.animate.shift(LEFT * 0.45), rights.animate.shift(RIGHT * 0.45), run_time=1.1)
        trails = VGroup(
            TracedPath(world.chroms[0].left_sister.get_center, stroke_color=BLUE, stroke_width=6, dissipating_time=2.0),
            TracedPath(world.chroms[0].right_sister.get_center, stroke_color=BLUE, stroke_width=6, dissipating_time=2.0),
        )
        self.add(trails)
        targets_l = [np.array([-3.15, y, 0]) for y in (0.95, 0.2, -0.55, -1.25)]
        targets_r = [np.array([3.15, y, 0]) for y in (0.95, 0.2, -0.55, -1.25)]
        self.at("Spindle fibers pull")
        self.play(*[m.animate.move_to(p) for m, p in zip(lefts, targets_l)],
                  *[m.animate.move_to(p) for m, p in zip(rights, targets_r)],
                  run_time=3.4, rate_func=linear)
        self.at("Follow blue")
        self.play(lefts[0].animate.scale(1.25), rights[0].animate.scale(1.25),
                  world.boundary.animate.stretch(1.035, 0), run_time=1.6, rate_func=there_and_back)
        self.at("One blue copy moves left")
        self.play(lefts.animate.shift(LEFT * 0.35), rights.animate.shift(RIGHT * 0.35), run_time=2.0)
        self.at("Each separated chromatid")
        chromosome = T("chromosomes", 28, BLUE).move_to(sisters)
        self.play(swap(sisters, chromosome), lefts.animate.scale(1.12), rights.animate.scale(1.12),
                  world.boundary.animate.stretch(1.04, 1), run_time=2.2, rate_func=there_and_back)
        self.finish()


class S10Finish(SpokenScene):
    def construct(self):
        boundary = cell_outline()
        phase = T("TELOPHASE", 34, TEXT).move_to([0, 3.35, 0])
        badge = rule_badge()
        sets = VGroup()
        for x in (-2.75, 2.75):
            sets.add(VGroup(*[
                rod(c, 0.82 if i < 2 else 0.62, 0.2).move_to([x + (i - 1.5) * 0.36, -0.25, 0])
                for i, c in enumerate(CHROM_COLORS)
            ]))
        self.at("In telophase")
        self.play(FadeIn(boundary), FadeIn(sets), FadeIn(phase), FadeIn(badge), run_time=0.9)
        envs = VGroup(*[Ellipse(width=2.65, height=3.25, color=YELLOW, stroke_width=4,
                                fill_color=YELLOW, fill_opacity=0.05).move_to([x, -0.25, 0]) for x in (-2.75, 2.75)])
        self.at("Yellow nuclear envelopes")
        self.play(FadeIn(envs), sets.animate.set_opacity(0.72).stretch(1.18, 1),
                  boundary.animate.stretch(1.05, 0), run_time=1.8)
        self.play(sets[0].animate.shift(LEFT * 0.22), sets[1].animate.shift(RIGHT * 0.22),
                  envs[0].animate.shift(LEFT * 0.22), envs[1].animate.shift(RIGHT * 0.22),
                  boundary.animate.stretch(1.04, 1), run_time=2.3, rate_func=there_and_back)
        self.at("Mitosis has made")
        mitosis = caption("MITOSIS = nuclear division", color=YELLOW)
        self.play(FadeIn(mitosis), envs.animate.scale(1.06), boundary.animate.stretch(1.035, 0),
                  run_time=1.5)
        self.at("Cytokinesis often begins")
        self.play(FadeOut(mitosis), FadeOut(phase), FadeOut(badge), run_time=0.6)
        panels = TwoPanel("animal cell", "plant cell", colors=(TEAL, TEAL), top=3.25, bottom=-2.45)
        pinch = ValueTracker(0.0)
        def animal_boundary():
            p = pinch.get_value()
            pts = []
            for t in np.linspace(0, TAU, 180):
                x = 2.65 * np.cos(t)
                y = 1.75 * np.sin(t) * (1 - 0.78 * p * np.exp(-(x / 0.8) ** 2))
                pts.append(np.array([x - 3.35, y - 0.15, 0]))
            m = VMobject(color=TEAL, stroke_width=5, fill_color=TEAL, fill_opacity=0.06)
            m.set_points_smoothly(pts + [pts[0]])
            return m
        animal = always_redraw(animal_boundary)
        animal_nuclei = VGroup(*[Circle(radius=0.65, color=YELLOW).move_to([x, -0.15, 0]) for x in (-4.4, -2.3)])
        plant = RoundedRectangle(width=5.0, height=3.5, corner_radius=0.08, color=TEAL, stroke_width=5,
                                 fill_color=TEAL, fill_opacity=0.14).move_to([3.35, -0.15, 0])
        plant_nuclei = VGroup(*[Circle(radius=0.65, color=YELLOW).move_to([x, -0.15, 0]) for x in (2.3, 4.4)])
        self.at("It divides the cytoplasm")
        self.play(FadeOut(boundary), FadeOut(envs), FadeOut(sets), FadeIn(panels),
                  FadeIn(animal), FadeIn(animal_nuclei), FadeIn(plant), FadeIn(plant_nuclei), run_time=1.1)
        cytokinesis = caption("CYTOKINESIS = cytoplasmic division", color=TEAL)
        self.play(FadeIn(cytokinesis), run_time=0.55)
        self.at("An animal cell")
        self.play(pinch.animate.set_value(0.95), run_time=1.7, rate_func=linear)
        plate = Line([3.35, -0.2, 0], [3.35, -0.1, 0], color=TEAL, stroke_width=9)
        self.at("A plant cell")
        self.play(Create(plate), run_time=0.45)
        self.play(Transform(plate, Line([3.35, -1.9, 0], [3.35, 1.6, 0], color=TEAL, stroke_width=9)), run_time=1.6)
        self.play(animal_nuclei.animate.set_stroke(width=7), plant_nuclei.animate.set_stroke(width=7), run_time=0.8)
        self.finish()


class S11CompleteSet(SpokenScene):
    def construct(self):
        heading = T("WHAT DID NOT HAPPEN", 34, TEXT).move_to([0, 3.35, 0])
        start_cell = cell_outline(3.3, 2.1, center=np.array([0, 1.65, 0]))
        start_rods = loose_set(center=np.array([0, 1.65, 0]), scale=0.48)
        self.at("Notice what did not happen")
        self.play(FadeIn(heading), FadeIn(start_cell), FadeIn(start_rods), run_time=0.8)
        halves = VGroup(
            VGroup(rod(BLUE, 0.8, 0.2), rod(ORANGE, 0.58, 0.2).shift(RIGHT * 0.45)).move_to([-3.1, -1.0, 0]),
            VGroup(rod(LIGHT_BLUE, 0.8, 0.2), rod(LIGHT_ORANGE, 0.58, 0.2).shift(RIGHT * 0.45)).move_to([3.1, -1.0, 0]),
        )
        bad = VGroup(
            Line([-4.25, -2.1, 0], [4.25, 0.15, 0], color=RED, stroke_width=10),
            Line([-4.25, 0.15, 0], [4.25, -2.1, 0], color=RED, stroke_width=10),
        )
        self.at("The cell did not split")
        self.play(FadeIn(halves), Create(bad[0]), Create(bad[1]), run_time=1.6)
        self.at("It copied every chromosome")
        copied = copied_set(center=np.array([0, -0.7, 0]), crossed=False, scale=0.82)
        self.play(FadeOut(halves), FadeOut(bad), FadeIn(copied), run_time=1.3)
        destinations = VGroup()
        for x in (-3.0, 3.0):
            destinations.add(VGroup(*[
                rod(c, 1.0 if i < 2 else 0.75, 0.22).move_to([x + (i - 1.5) * 0.42, -0.8, 0])
                for i, c in enumerate(CHROM_COLORS)
            ]))
        self.play(ReplacementTransform(copied, destinations), run_time=1.8)
        self.at("That is why each")
        envs = VGroup(*[Ellipse(width=3.0, height=3.1, color=YELLOW, stroke_width=5).move_to([x, -0.8, 0]) for x in (-3.0, 3.0)])
        label = caption("a complete set — not a random half", color=GOLD)
        self.play(FadeIn(envs), FadeIn(label), FadeOut(start_cell), FadeOut(start_rods), FadeOut(heading), run_time=1.1)
        self.play(destinations.animate.scale(1.12), envs.animate.scale(1.05), run_time=1.2)
        self.finish()


class S12End(EndCard):
    LINE = "Copy each chromosome first; separate the copies so each nucleus gets one."
