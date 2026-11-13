from bp_parts import *


# COLOR MAP (continued exactly from chapter 1)
# chromosome pair A: BLUE / light blue; pair B: ORANGE / light orange
# spindle fibres: GREEN; nuclear envelopes: YELLOW; cell boundaries: TEAL; labels: TEXT
ORANGE = "#F28E5B"
LIGHT_BLUE = "#9ADBE8"
LIGHT_ORANGE = "#F7B58D"


def chromosome(color=BLUE, height=0.48, x=0, y=0):
    """A chromosome cartoon, not a molecular structure."""
    a = Line(UL * 0.16, DR * 0.16, color=color, stroke_width=7)
    b = Line(DL * 0.16, UR * 0.16, color=color, stroke_width=7)
    g = VGroup(a, b).set_height(height).move_to([x, y, 0])
    for line in g:
        line.set_cap_style(CapStyleType.ROUND)
    return g


def cell_icon(stage="interphase", width=1.35, height=1.0):
    """One reusable onion-cell drawing at a fixed scale."""
    wall = RoundedRectangle(corner_radius=0.09, width=width, height=height,
                            stroke_color=TEAL, stroke_width=3, fill_color=TEAL,
                            fill_opacity=0.11)
    contents = VGroup()
    if stage == "interphase":
        nucleus = Circle(radius=0.29 * height, color=YELLOW, stroke_width=3,
                         fill_color=YELLOW, fill_opacity=0.06)
        loose = VGroup(*[
            Arc(radius=0.11 + 0.025 * i, start_angle=0.4 + i, angle=1.8,
                color=(BLUE if i % 2 == 0 else ORANGE), stroke_width=3)
            for i in range(4)
        ]).move_to(nucleus)
        contents.add(nucleus, loose)
    elif stage == "prophase":
        nucleus = Circle(radius=0.31 * height, color=YELLOW, stroke_width=3)
        xs = VGroup(chromosome(BLUE, 0.26), chromosome(ORANGE, 0.26),
                    chromosome(LIGHT_BLUE, 0.23), chromosome(LIGHT_ORANGE, 0.23))
        xs.arrange_in_grid(2, 2, buff=0.09).move_to(nucleus)
        contents.add(nucleus, xs)
    elif stage == "metaphase":
        fibres = VGroup(*[
            Line([-width * 0.42, yy, 0], [0, yy * 0.25, 0], color=GREEN, stroke_width=2)
            for yy in (-0.25, 0, 0.25)
        ], *[
            Line([width * 0.42, yy, 0], [0, yy * 0.25, 0], color=GREEN, stroke_width=2)
            for yy in (-0.25, 0, 0.25)
        ])
        xs = VGroup(chromosome(BLUE, 0.27), chromosome(ORANGE, 0.27),
                    chromosome(LIGHT_BLUE, 0.24)).arrange(DOWN, buff=0.05)
        contents.add(fibres, xs)
    elif stage == "anaphase":
        fibres = VGroup(*[
            Line([-width * 0.43, yy, 0], [-0.25, yy * 0.6, 0], color=GREEN, stroke_width=2)
            for yy in (-0.24, 0, 0.24)
        ], *[
            Line([width * 0.43, yy, 0], [0.25, yy * 0.6, 0], color=GREEN, stroke_width=2)
            for yy in (-0.24, 0, 0.24)
        ])
        left = VGroup(chromosome(BLUE, 0.21), chromosome(ORANGE, 0.21)).arrange(DOWN, buff=0.06).shift(LEFT * 0.28)
        right = left.copy().shift(RIGHT * 0.56)
        contents.add(fibres, left, right)
    else:  # telophase
        nuclei = VGroup(
            Circle(radius=0.23 * height, color=YELLOW, stroke_width=3).shift(LEFT * width * 0.23),
            Circle(radius=0.23 * height, color=YELLOW, stroke_width=3).shift(RIGHT * width * 0.23),
        )
        xs = VGroup(chromosome(BLUE, 0.18).shift(LEFT * width * 0.23),
                    chromosome(ORANGE, 0.18).shift(RIGHT * width * 0.23))
        contents.add(nuclei, xs)
    return VGroup(wall, contents)


FIELD_STAGES = [
    "interphase", "interphase", "prophase", "interphase", "metaphase", "interphase",
    "anaphase", "interphase", "interphase", "telophase", "prophase", "interphase",
]


def root_field(scale=1.0, center=ORIGIN):
    """The carried microscope field; every scene calls this builder."""
    cells = VGroup(*[cell_icon(stage) for stage in FIELD_STAGES]).arrange_in_grid(3, 4, buff=0.12)
    cells.scale(scale).move_to(center)
    field = Ellipse(width=8.3 * scale, height=5.7 * scale, color=GREY, stroke_width=4,
                    fill_color="#26364A", fill_opacity=0.95).move_to(center)
    cells.set_z_index(2)
    return VGroup(field, cells)


def lane_world(include_assumptions=True, include_question=True):
    """The predict/reveal frame, rebuilt identically for s04-s06."""
    left_box = RoundedRectangle(corner_radius=0.2, width=5.2, height=4.35,
                                color=BLUE, stroke_width=4, fill_color=BLUE,
                                fill_opacity=0.18).move_to([-2.9, 0.35, 0])
    right_box = RoundedRectangle(corner_radius=0.2, width=5.2, height=4.35,
                                 color=ORANGE, stroke_width=4, fill_color=ORANGE,
                                 fill_opacity=0.18).move_to([2.9, 0.35, 0])
    left_cells = VGroup(*[cell_icon("interphase", 0.72, 0.5) for _ in range(10)]).arrange_in_grid(2, 5, buff=0.18)
    right_cells = VGroup(*[cell_icon("prophase", 0.72, 0.5) for _ in range(4)]).arrange_in_grid(2, 2, buff=0.25)
    left_cells.move_to(left_box.get_center() + DOWN * 0.15)
    right_cells.move_to(right_box.get_center() + DOWN * 0.15)
    world = VGroup(left_box, right_box, left_cells, right_cells)
    world.left_box, world.right_box = left_box, right_box
    world.left_cells, world.right_cells = left_cells, right_cells
    if include_assumptions:
        checks = VGroup(chip("✓ steady cycling", GREEN, 26), chip("✓ fair sample", GREEN, 26))
        checks.arrange(RIGHT, buff=0.35).move_to([0, 3.25, 0])
        world.add(checks)
        world.checks = checks
    if include_question:
        q = question_card("Which lane lasts longer?", y=-3.12, size=30)
        world.add(q)
        world.question = q
    return world


def phase_arc(start, angle, color, radius=2.45, width=18):
    return Arc(radius=radius, start_angle=start, angle=angle, color=color, stroke_width=width)


def cycle_ring():
    arcs = VGroup(
        phase_arc(0, 1.15 * PI, BLUE),
        phase_arc(1.15 * PI, 0.28 * PI, ORANGE),
        phase_arc(1.43 * PI, 0.20 * PI, GREEN),
        phase_arc(1.63 * PI, 0.18 * PI, RED),
        phase_arc(1.81 * PI, 0.19 * PI, YELLOW),
    )
    return arcs


class S00Hook(SpokenScene):
    def construct(self):
        nuclei = VGroup(
            cell_icon("telophase", 2.7, 2.0).move_to([-2.0, 0.2, 0]),
            cell_icon("telophase", 2.7, 2.0).move_to([2.0, 0.2, 0]),
        )
        self.add(nuclei)
        self.at("first film showed")
        small_nuclei = nuclei.copy().scale(0.38).arrange(RIGHT, buff=0.2).move_to([0, 2.5, 0])
        self.play(Transform(nuclei, small_nuclei), run_time=1.8)
        root = Polygon([-2.0, 2.0, 0], [2.0, 2.0, 0], [1.15, -2.8, 0], [-1.15, -2.8, 0],
                       color=TEAL, stroke_width=4, fill_color=TEAL, fill_opacity=0.06)
        mini = root_field(0.5, [0, -0.2, 0])
        self.play(FadeIn(root), Transform(nuclei, mini[1]), run_time=2.0)
        self.at("frozen onion root")
        field = root_field(0.95)
        self.play(ReplacementTransform(VGroup(root, nuclei), field), run_time=1.6)
        self.at("which part of that cycle")
        question = T("?", 150, GOLD, weight=BOLD).move_to([0, 0, 0]).set_z_index(5)
        question.layout_ok = True  # deliberate question stamp over the microscope field
        self.play(GrowFromCenter(question), field.animate.set_opacity(0.48), run_time=1.0)
        pulse(question, base=3.0, amp=1.0, speed=2.0)
        self.at("patterns can")
        self.play(field.animate.set_opacity(0.85), run_time=0.6)
        self.finish()


class S01Title(TitleCard):
    LESSON = "Cell Cycle and Mitosis"
    TITLE = "A Snapshot Becomes a Clock"


class S02Snapshot(SpokenScene):
    def construct(self):
        field = root_field(1.0)
        cells = field[1]
        for i, cell in enumerate(cells):
            bob(cell, amp=0.025, speed=1.25, seed=i)
        self.play(FadeIn(field, scale=0.92), run_time=1.2)
        self.at("each cell is caught")
        wave = [cells[i].animate.shift(UP * 0.12 if i % 2 else DOWN * 0.12) for i in range(len(cells))]
        self.play(LaggedStart(*wave, lag_ratio=0.04), run_time=1.5)
        self.play(LaggedStart(*[cells[i].animate.shift(DOWN * 0.12 if i % 2 else UP * 0.12)
                                for i in range(len(cells))], lag_ratio=0.04), run_time=1.2)
        self.at("some show loose chromosomes")
        spot = SurroundingRectangle(cells[0], color=YELLOW, buff=0.08, stroke_width=5)
        label = T("interphase", 28, YELLOW).next_to(field, RIGHT, buff=0.25)
        self.play(Create(spot), FadeIn(label), run_time=0.8)
        stages = [(2, "prophase", ORANGE), (4, "metaphase", GREEN),
                  (6, "anaphase", RED), (9, "telophase", YELLOW)]
        cues = ["chromosomes coiling", "lining up", "separating", "reaching opposite ends"]
        for (idx, name, color), cue in zip(stages, cues):
            self.at(cue)
            new_spot = SurroundingRectangle(cells[idx], color=color, buff=0.08, stroke_width=5)
            new_label = T(name, 28, color).move_to(label)
            self.play(Transform(spot, new_spot), swap(label, new_label, 0.55), run_time=0.65)
            label = new_label
        tag = scope_tag("schematic")
        self.play(FadeIn(tag), run_time=0.35)
        self.finish()


class S03TimeLogic(SpokenScene):
    def construct(self):
        track = cycle_ring()
        runners = VGroup(*[Dot(radius=0.13, color=TEXT) for _ in range(12)])
        angles = np.linspace(0.08, TAU - 0.08, len(runners))
        for dot, a in zip(runners, angles):
            dot.move_to(2.45 * np.array([np.cos(a), np.sin(a), 0]))
        self.play(Create(track), LaggedStart(*[FadeIn(d) for d in runners], lag_ratio=0.05), run_time=2.0)
        self.at("random points around")
        self.play(Rotate(runners, angle=0.55, about_point=ORIGIN), run_time=1.4, rate_func=linear)
        self.at("slow section holds")
        slow = phase_arc(0, 1.15 * PI, BLUE, width=27)
        gathered = runners.copy()
        gathered_angles = [0.08, 0.33, 0.58, 0.83, 1.08, 1.35, 1.65, 2.0, 2.45, 3.1, 4.5, 5.4]
        for dot, a in zip(gathered, gathered_angles):
            dot.move_to(2.45 * np.array([np.cos(a), np.sin(a), 0]))
        self.play(Transform(track[0], slow), Transform(runners, gathered), run_time=2.1)
        self.at("cycling cells follow")
        field = root_field(0.95)
        self.play(ReplacementTransform(VGroup(track, runners), field), run_time=1.5)
        self.at("longer phase should appear")
        many = SurroundingRectangle(VGroup(*[field[1][i] for i in [0, 1, 3, 5, 7, 8, 11]]),
                                    color=BLUE, buff=0.16, stroke_width=5)
        rule = caption("Longer phase  →  more cells", color=BLUE)
        self.play(Create(many), FadeIn(rule), run_time=1.0)
        pulse(many, base=5, amp=1.4, speed=2.4)
        self.finish()


class S04Predict(SpokenScene):
    def construct(self):
        world = lane_world(include_assumptions=False, include_question=False)
        self.play(FadeIn(VGroup(world.left_box, world.right_box)), run_time=0.8)
        self.at("different numbers of cells")
        self.play(LaggedStart(*[FadeIn(c, shift=UP * 0.12) for c in world.left_cells], lag_ratio=0.05),
                  LaggedStart(*[FadeIn(c, shift=UP * 0.12) for c in world.right_cells], lag_ratio=0.08), run_time=1.5)
        for c in world.left_cells:
            bob(c, amp=0.025, speed=1.6, seed=len(c.submobjects))
        for c in world.right_cells:
            bob(c, amp=0.025, speed=1.6, seed=2)
        self.at("moves steadily")
        checks = VGroup(chip("✓ steady cycling", GREEN, 26), chip("✓ fair sample", GREEN, 26))
        checks.arrange(RIGHT, buff=0.35).move_to([0, 3.25, 0])
        self.play(FadeIn(checks, shift=DOWN * 0.1), run_time=1.0)
        self.at("which lane represents")
        q = question_card("Which lane lasts longer?", y=-3.12, size=30)
        self.play(FadeIn(q), run_time=0.8)
        self.at("hold your answer")
        pulse(world.left_box, base=4, amp=1.3, speed=2.2)
        pulse(world.right_box, base=4, amp=1.3, speed=2.2)
        self.finish()


class S05Pause(PredictPause):
    QUESTION = "Which lane lasts longer?"
    SECONDS = 4.5

    def backdrop(self):
        world = lane_world(include_assumptions=True, include_question=False)
        pulse(world.left_box, base=4, amp=1.3, speed=2.2)
        pulse(world.right_box, base=4, amp=1.3, speed=2.2)
        for c in VGroup(*world.left_cells, *world.right_cells):
            bob(c, amp=0.02, speed=1.5, seed=1)
        return world


class S06Reveal(SpokenScene):
    def construct(self):
        world = lane_world(include_assumptions=False, include_question=False)
        for i, cell in enumerate(VGroup(*world.left_cells, *world.right_cells)):
            bob(cell, amp=0.03, speed=1.35, seed=i)
        self.add(world)
        longer = T("LONGER", 34, BLUE, weight=BOLD).move_to([-2.9, -2.15, 0])
        self.at("fuller lane")
        self.play(FadeIn(longer, shift=UP * 0.15), world.left_box.animate.set_stroke(width=7), run_time=0.9)
        self.at("more cells were caught")
        self.play(LaggedStart(*[Indicate(c, color=BLUE, scale_factor=1.08) for c in world.left_cells], lag_ratio=0.07), run_time=2.2)
        self.at("gives a fraction")
        numerator = VGroup(*[cell_icon("interphase", 0.95, 0.7) for _ in range(4)]).arrange(RIGHT, buff=0.16)
        denominator = VGroup(*[cell_icon("interphase", 0.72, 0.52) for _ in range(7)]).arrange(RIGHT, buff=0.10)
        bar = Line(LEFT * 3.0, RIGHT * 3.0, color=TEXT, stroke_width=6)
        frac = VGroup(numerator, bar, denominator).arrange(DOWN, buff=0.25).move_to(ORIGIN)
        self.play(FadeOut(VGroup(world, longer)), FadeIn(frac), run_time=1.3)
        not_watch = chip("not a stopwatch", RED, 28).move_to([5.2, 0, 0])
        self.play(FadeIn(not_watch), run_time=0.65)
        self.at("divide the cells")
        self.play(Indicate(numerator, color=BLUE), run_time=0.8)
        self.at("all the cells counted")
        self.play(Indicate(denominator, color=GOLD), run_time=0.8)
        ring = Circle(radius=2.4, color=GREY, stroke_width=15)
        share = Arc(radius=2.4, start_angle=PI / 2, angle=-TAU * 4 / 7, color=BLUE, stroke_width=18)
        self.play(FadeOut(not_watch), ReplacementTransform(frac, VGroup(ring, share)), run_time=1.4)
        self.finish()


def sort_bin(title, count, color, x):
    frame = RoundedRectangle(corner_radius=0.13, width=2.35, height=4.7, color=color, stroke_width=3,
                             fill_color=color, fill_opacity=0.14)
    head = T(title, 25, color).move_to(frame.get_top() + DOWN * 0.38)
    number = M(str(count), 38, color).move_to(frame.get_top() + DOWN * 1.0)
    sample_stage = {"interphase": "interphase", "prophase": "prophase", "metaphase": "metaphase",
                    "anaphase": "anaphase", "telophase": "telophase"}[title]
    sample = cell_icon(sample_stage, 1.55, 1.12).move_to(frame.get_center() + DOWN * 0.35)
    g = VGroup(frame, head, number, sample).move_to([x, -0.05, 0])
    return g


class S07Sort(SpokenScene):
    def construct(self):
        title = T("schematic reconstruction", 28, GREY).move_to([0, 3.4, 0])
        source = root_field(0.62, [0, 0, 0])
        self.play(FadeIn(source), FadeIn(title), run_time=1.2)
        names = ["interphase", "prophase", "metaphase", "anaphase", "telophase"]
        counts = [20, 10, 3, 2, 1]
        colors = [BLUE, ORANGE, GREEN, RED, YELLOW]
        xs = [-5.1, -2.55, 0, 2.55, 5.1]
        bins = [sort_bin(*args) for args in zip(names, counts, colors, xs)]
        self.at("visible clues")
        self.play(FadeOut(source), LaggedStart(*[FadeIn(b[0]) for b in bins], lag_ratio=0.08), run_time=1.3)
        cues = ["intact nuclei", "coiled chromosomes", "middle row", "separating groups", "two forming nuclei"]
        shown = VGroup()
        for b, cue in zip(bins, cues):
            self.at(cue)
            parts = VGroup(b[1], b[2], b[3])
            self.play(FadeIn(parts, shift=UP * 0.12), run_time=0.75)
            shown.add(parts)
        total = chip("total 36", TEXT, 28).move_to([5.35, 3.35, 0])
        self.play(FadeIn(total), run_time=0.45)
        self.finish()


class S08Convert(SpokenScene):
    def construct(self):
        panel = RoundedRectangle(corner_radius=0.22, width=12.2, height=6.25, color=GREY,
                                 stroke_width=3, fill_color="#26364A", fill_opacity=0.92)
        segments = VGroup(*[
            Rectangle(width=w, height=1.1, color=c, stroke_width=3, fill_color=c, fill_opacity=0.34)
            for w, c in zip([6.4, 3.2, 0.96, 0.64, 0.32], [BLUE, ORANGE, GREEN, RED, YELLOW])
        ]).arrange(RIGHT, buff=0).move_to([0, 0.75, 0])
        fraction = VGroup(M("cells in phase", 32, BLUE), Line(LEFT * 2, RIGHT * 2, stroke_width=4),
                          M("all cells", 32, TEXT)).arrange(DOWN, buff=0.18).move_to([0, 1.0, 0])
        self.play(FadeIn(panel), FadeIn(fraction), run_time=1.0)
        self.at("multiply a phase's fraction")
        formula = M("time in a phase = fraction × 1,440 min", 30, TEXT).move_to([0, -1.0, 0])
        self.play(FadeIn(formula, shift=UP * 0.1), run_time=1.0)
        self.at("round total time")
        assumed = chip("24 h = 1,440 min  (assumed)", GOLD, 30).move_to([0, 2.8, 0])
        self.play(FadeIn(assumed), run_time=1.0)
        self.at("put that value")
        blanks = VGroup(*[RoundedRectangle(corner_radius=0.1, width=1.85, height=0.72, color=c, stroke_width=3)
                          for c in [BLUE, ORANGE, GREEN, RED, YELLOW]])
        blanks.arrange(RIGHT, buff=0.3).move_to([0, -2.2, 0])
        self.play(FadeIn(blanks), run_time=0.8)
        self.at("model estimate")
        label = T("model estimate", 30, GOLD).move_to([0, -2.72, 0])
        self.play(FadeOut(fraction), FadeOut(formula), Transform(blanks, segments), FadeIn(label), run_time=1.5)
        self.finish()


def failure_card(kind):
    panel = RoundedRectangle(corner_radius=0.22, width=11.2, height=5.5, color=RED,
                             stroke_width=3, fill_color=RED, fill_opacity=0.08)
    if kind == "chosen":
        cells = VGroup(*[cell_icon(s, 0.9, 0.65) for s in ["prophase", "metaphase", "anaphase"]]).arrange(RIGHT, buff=0.35)
        hand = Arrow([0, -2.5, 0], [0, -0.8, 0], color=RED, stroke_width=7)
        return VGroup(panel, cells, hand, T("chosen pictures", 30, RED).move_to([0, 2.35, 0]))
    if kind == "stopped":
        cells = VGroup(*[cell_icon("interphase", 1.25, 0.9) for _ in range(5)]).arrange(RIGHT, buff=0.35)
        stop = chip("left the cycle", RED, 30).move_to([0, -1.4, 0])
        return VGroup(panel, cells, stop, T("some stop cycling", 30, RED).move_to([0, 2.35, 0]))
    speed = ValueTracker(0.25)
    gauge = dial(speed, [0, 0.4, 0], radius=2.0, label="changing pace", color=RED)
    return VGroup(panel, gauge, T("different speeds", 30, RED).move_to([0, -2.3, 0]))


class S09Limits(SpokenScene):
    def construct(self):
        chosen = failure_card("chosen")
        self.play(FadeIn(chosen), run_time=1.1)
        self.at("display every stage")
        self.play(Indicate(chosen[1], color=RED), run_time=1.0)
        self.at("cells stopped cycling")
        stopped = failure_card("stopped")
        self.play(ReplacementTransform(chosen, stopped), run_time=1.1)
        self.at("changed pace")
        speed = failure_card("speed")
        self.play(ReplacementTransform(stopped, speed), run_time=1.0)
        self.play(Rotate(speed[1][2], angle=-0.8, about_point=[0, 0.4, 0]), run_time=0.8)
        self.at("random field")
        grid = VGroup(*[Square(0.5, color=BLUE) for _ in range(16)]).arrange_in_grid(4, 4, buff=0.08)
        path = VGroup(Line([-1, 0, 0], [1, 0, 0], color=GREEN, stroke_width=6),
                      Arrow([0.2, -0.8, 0], [0.2, 0.8, 0], color=GREEN, stroke_width=5))
        clock = VGroup(Circle(0.75, color=GOLD, stroke_width=4),
                       Line(ORIGIN, UP * 0.48, color=GOLD, stroke_width=5),
                       Line(ORIGIN, RIGHT * 0.36, color=GOLD, stroke_width=5))
        good = TwoPanel("random field", "clear sampling rule", colors=(BLUE, GREEN), top=2.8, bottom=-2.3)
        good.left_frame.set_fill(BLUE, opacity=0.16)
        good.right_frame.set_fill(GREEN, opacity=0.16)
        good.put(grid, "left"), good.put(path, "right")
        self.play(FadeOut(speed), FadeIn(good), FadeIn(grid), FadeIn(path), run_time=1.2)
        self.at("measured total time")
        clock.move_to([0, -2.95, 0]).scale(0.7)
        measured = T("measured total time", 28, GOLD).next_to(clock, RIGHT, buff=0.25)
        self.play(FadeIn(clock), FadeIn(measured), run_time=0.9)
        self.finish()


def process_tracks():
    top = RoundedRectangle(corner_radius=0.18, width=11.6, height=2.15, color=YELLOW, stroke_width=3,
                           fill_color=YELLOW, fill_opacity=0.14).move_to([0, 1.45, 0])
    bottom = RoundedRectangle(corner_radius=0.18, width=11.6, height=2.15, color=TEAL, stroke_width=3,
                              fill_color=TEAL, fill_opacity=0.14).move_to([0, -1.25, 0])
    return VGroup(top, bottom)


class S10TwoProcesses(SpokenScene):
    def construct(self):
        tracks = process_tracks()
        self.play(FadeIn(tracks), run_time=1.0)
        self.at("mitosis separates chromosomes")
        top_label = T("MITOSIS", 32, YELLOW, weight=BOLD).move_to([-4.8, 2.1, 0])
        before = VGroup(chromosome(BLUE, 0.55), chromosome(ORANGE, 0.55)).arrange(RIGHT, buff=0.35).move_to([-1.8, 1.2, 0])
        nuclei = VGroup(Circle(0.58, color=YELLOW, stroke_width=4), Circle(0.58, color=YELLOW, stroke_width=4)).arrange(RIGHT, buff=2.2).move_to([2.4, 1.2, 0])
        copies = VGroup(chromosome(BLUE, 0.35).move_to(nuclei[0]), chromosome(ORANGE, 0.35).move_to(nuclei[1]))
        self.play(FadeIn(top_label), FadeIn(before), run_time=0.8)
        self.play(ReplacementTransform(before, copies), Create(nuclei), run_time=1.2)
        self.at("cytokinesis separates")
        bottom_label = T("CYTOKINESIS", 32, TEAL, weight=BOLD).move_to([-4.15, -0.58, 0])
        cell = RoundedRectangle(corner_radius=0.15, width=5.3, height=1.35, color=TEAL, stroke_width=4).move_to([1.5, -1.35, 0])
        plate = Line([1.5, -1.95, 0], [1.5, -0.75, 0], color=TEAL, stroke_width=10).scale(0.05)
        self.play(FadeIn(bottom_label), Create(cell), run_time=0.8)
        self.play(plate.animate.scale(20), run_time=4.6, rate_func=linear)
        bottom_action = VGroup(cell, plate)
        bob(bottom_action, amp=0.045, speed=1.2, seed=2)
        bob(VGroup(nuclei, copies), amp=0.045, speed=1.35, seed=1)
        self.at("phase count sorts chromosome patterns")
        count_label = T("phase count", 28, BLUE).move_to([4.35, 3.18, 0])
        pointer = Arrow([4.35, 2.92, 0], [4.35, 2.35, 0], color=BLUE, stroke_width=5, buff=0.04)
        self.play(FadeIn(count_label), GrowArrow(pointer), run_time=0.9)
        self.play(Indicate(VGroup(nuclei, copies), color=BLUE, scale_factor=1.03), run_time=2.2)
        self.at("does not directly time")
        dim = SurroundingRectangle(VGroup(bottom_label, bottom_action), color=GREY, buff=0.15)
        self.play(Create(dim), VGroup(bottom_label, bottom_action).animate.set_opacity(0.35), run_time=1.0)
        self.play(ShowPassingFlash(dim.copy().set_color(TEAL), time_width=0.7), run_time=2.4)
        self.at("two processes overlap")
        time_line = Line([-5.0, -3.05, 0], [5.0, -3.05, 0], color=GREY, stroke_width=5)
        mit = Line([-3.8, -3.05, 0], [2.0, -3.05, 0], color=YELLOW, stroke_width=12)
        cyt = Line([0.0, -3.05, 0], [4.2, -3.05, 0], color=TEAL, stroke_width=12)
        self.play(Create(time_line), Create(mit), Create(cyt), run_time=1.2)
        self.finish()


class S11Meaning(SpokenScene):
    def construct(self):
        field = root_field(0.95)
        self.play(FadeIn(field), run_time=1.0)
        self.at("cells spend time growing")
        inter = VGroup(*[field[1][i] for i in [0, 1, 3, 5, 7, 8, 11]])
        self.play(inter.animate.set_stroke(width=6), run_time=1.1)
        ring = cycle_ring().scale(1.04)
        ring.move_to(field)
        self.play(FadeIn(ring), field.animate.set_opacity(0.45), run_time=1.3)
        self.at("preparing before chromosomes")
        self.play(Indicate(ring[0], color=BLUE, scale_factor=1.03), run_time=1.2)
        self.at("copy each chromosome first")
        badge = chip("COPY → SEPARATE → MATCH", GOLD, 28).move_to([0, 3.3, 0])
        self.play(FadeIn(badge), run_time=0.8)
        self.at("separate the copies")
        self.play(Indicate(VGroup(ring[1], ring[2], ring[3], ring[4]), color=YELLOW), run_time=1.2)
        self.at("counting rule is just as short")
        lanes = lane_world(include_assumptions=False, include_question=False).scale(0.75).move_to([0, -0.15, 0])
        self.play(FadeOut(VGroup(field, ring)), FadeIn(lanes), badge.animate.move_to([0, 3.3, 0]), run_time=1.2)
        self.at("fair snapshot")
        rule = caption("In a fair snapshot, a longer phase holds more cells.", color=BLUE, y=-3.15)
        self.play(FadeIn(rule), lanes.left_box.animate.set_stroke(width=7), run_time=1.0)
        self.play(FadeOut(VGroup(lanes, badge, rule)), run_time=0.7)
        self.finish()


class S12End(EndCard):
    LINE = "In a fair snapshot, a longer phase holds more cells."
