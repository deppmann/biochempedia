"""From DNA Route to Gene Order.

COLOR MAP: gold donor DNA and marker symbols, light grey recipient,
teal donor, purple phage, orange F factor and origin, white chromosome,
blue filter, and red DNase. All DNA drawings are schematic paths.
"""
from bp_parts import *

PURPLE = "#A98BEA"
ORANGE = "#F29E4C"
LIGHT_GREY = "#C7CED8"

ROUTE_Y = (1.85, 0, -1.85)
ROUTE_X = -4.75
DONOR_X, RECIPIENT_X = -3.45, 3.45
QUESTION = "Which carrier fits both clues?"
QUESTION_STYLE = dict(y=3.06, size=44, max_w=11.6)
# The lesson gives entries at 6, 17, and 25 minutes and a 100-minute circle.
# The film shows the resulting relative distances without numeric labels.
ENTRY = (6, 17, 25)
MAP_PERIOD = 100
MARK_SCALE = 0.14
MAP_START = -4.75
MAP_Y = -2.72


def xy(x, y=0):
    return np.array([x, y, 0.0])


def bacterium(center, color, width, height):
    return RoundedRectangle(
        corner_radius=height * 0.42, width=width, height=height,
        stroke_color=color, stroke_width=4.5, fill_color=color, fill_opacity=0.31,
    ).move_to(center)


def chromosome(center, radius=1.18):
    return Circle(radius, color=TEXT, stroke_width=12).move_to(center)


def dna(center, width=0.85):
    return RoundedRectangle(
        width=width, height=0.34, corner_radius=0.12, stroke_width=0,
        fill_color=GOLD, fill_opacity=1,
    ).move_to(center)


def marker(index, center, scale=1):
    shapes = (Square, Circle, Triangle)
    symbol = shapes[index](color=GOLD, stroke_width=0, fill_opacity=1)
    return symbol.scale_to_fit_height(2 * MARK_SCALE * scale).move_to(center)


def phage(center, scale=1):
    coat = RoundedRectangle(
        width=1.54, height=0.87, corner_radius=0.24, stroke_color=PURPLE,
        stroke_width=7, fill_color=PURPLE, fill_opacity=0.59,
    ).move_to(UP * 0.26)
    tail = VMobject(stroke_color=PURPLE, stroke_width=4).set_points_as_corners(
        [xy(-0.26, -0.64), xy(0, -0.42), xy(0), xy(0, -0.42), xy(0.26, -0.64)]
    )
    return VGroup(coat, tail, dna(coat.get_center(), 0.73)).scale(scale).move_to(center)


def filter_gate(x, height=6.08):
    top, _, bottom = ROUTE_Y
    blocks = [(-height / 2, bottom - 0.81), (bottom + 0.87, top - 0.37),
              (top + 0.37, height / 2)]
    # Gaps are drawn at the two paths that pass. The middle rail stops the cell.
    return VGroup(*[
        RoundedRectangle(
            width=0.48, height=hi - lo, corner_radius=0.13, stroke_color=BLUE,
            stroke_width=4, fill_color=BLUE, fill_opacity=0.35,
        ).move_to(xy(x, (hi + lo) / 2))
        for lo, hi in blocks
    ])


def separation_gate(x):
    return RoundedRectangle(
        width=0.48, height=5.55, corner_radius=0.19, stroke_color=BLUE,
        stroke_width=4, fill_color=BLUE, fill_opacity=0.38,
    ).move_to(xy(x))


def route_world():
    recipient = bacterium(xy(4.27), LIGHT_GREY, 4.18, 5.78)
    routes = VGroup(*[
        Line(xy(-6.05, y), xy(2.73, y), color=GREY, stroke_width=4, stroke_opacity=0.49)
        for y in ROUTE_Y
    ]).set_z_index(-1)
    return recipient, routes, scope_tag(size=28, color=LIGHT_GREY).shift(LEFT * 0.22)


def questions():
    return VGroup(*[
        T("?", 53, GOLD).move_to(xy(-2.52, y + 0.51)) for y in ROUTE_Y
    ])


def unknown_cargo(xs):
    return VGroup(*[dna(xy(x, y)) for x, y in zip(xs, ROUTE_Y)])


def route_carriers():
    return (
        dna(xy(ROUTE_X, ROUTE_Y[0]), 1.14),
        bacterium(xy(ROUTE_X), TEAL, 2.42, 1.23),
        phage(xy(ROUTE_X, ROUTE_Y[2]), 1.02),
    )


def contact_pair():
    donor = bacterium(xy(DONOR_X), TEAL, 5.24, 4.58)
    recipient = bacterium(xy(RECIPIENT_X), LIGHT_GREY, 5.24, 4.58)
    return donor, recipient, link(donor, recipient)


def link(donor, recipient):
    x0, x1 = donor.get_right()[0], recipient.get_left()[0]
    return RoundedRectangle(
        width=x1 - x0 + 0.04, height=0.44, corner_radius=0.15, stroke_color=TEAL,
        stroke_width=4, fill_color=TEAL, fill_opacity=0.25,
    ).move_to(xy((x0 + x1) / 2))


def pair_chromosomes():
    return chromosome(xy(DONOR_X - 0.79), 1.19), chromosome(xy(RECIPIENT_X + 0.79), 1.19)


def plasmid(x):
    center = xy(x - np.sign(x) * 1.14)
    return Annulus(inner_radius=0.29, outer_radius=0.66,
                   color=ORANGE, fill_opacity=0.94, stroke_width=0).move_to(center)


def evidence_board(filter_highlight=0.32):
    panels = TwoPanel(
        "survives DNase", "stops at filter", colors=(RED, BLUE), top=2.48,
        bottom=-0.04, gap=0.48, width=12.43, size=33,
    )
    left = VGroup(
        RoundedRectangle(
            width=3.3, height=1.28, corner_radius=0.24, stroke_width=0,
            fill_color=RED, fill_opacity=0.28,
        ),
        dna(ORIGIN, 1.80),
    )
    wall = Rectangle(width=0.32, height=1.25, color=BLUE, fill_opacity=0.58)
    right = VGroup(
        dna(xy(-0.63), 0.7), Line(xy(-0.25), xy(0.42), color=GREY, stroke_width=5),
        wall.move_to(xy(0.66)),
    )
    panels.right_frame.set_fill(BLUE, opacity=filter_highlight)
    panels.put(left, "left")
    panels.put(right, "right")
    items = (
        dna(xy(-4.15, -1.32), 1.34),
        bacterium(xy(0, -1.32), TEAL, 2.6, 1.04),
        phage(xy(4.15, -1.32), 0.82),
    )
    labels = [
        place_label(T(name, 29, color), item, dirs=(DOWN,), buff=0.44)
        for name, color, item in zip(
            ("transformation", "conjugation", "transduction"), (GOLD, TEAL, PURPLE), items
        )
    ]
    # Match baselines across the three answer choices.
    for label in labels:
        label.set_y(-2.47)
    options = VGroup(*[VGroup(item, label) for item, label in zip(items, labels)])
    return VGroup(panels.left_frame, panels.left_head, left), VGroup(
        panels.right_frame, panels.right_head, right
    ), options


def gap_bracket(x0, x1, y, color=GOLD):
    return VMobject(stroke_color=color, stroke_width=5).set_points_as_corners(
        [xy(x0, y + 0.13), xy(x0, y), xy(x1, y), xy(x1, y + 0.13)]
    )


def interval_band(x0, x1, y, color, height=0.19):
    return Rectangle(
        width=x1 - x0 - 0.06, height=height, stroke_width=0, fill_color=color, fill_opacity=0.80,
    ).move_to(xy((x0 + x1) / 2, y))


def colony_marker(index, center):
    colony = Circle(radius=0.32, color=GOLD, stroke_width=4, fill_opacity=0.49).move_to(center)
    return VGroup(colony, marker(index, center, 0.96))


def entry_map(y=MAP_Y, gap_depth=0.52):
    positions = [xy(MAP_START + 0.31 * t, y) for t in ENTRY]
    axis = Line(xy(MAP_START, y), xy(4.10, y), color=TEXT, stroke_width=6)
    marks = VGroup(*[marker(i, p, 1.32) for i, p in enumerate(positions)])
    gaps = VGroup(*[
        gap_bracket(a[0], b[0], y - gap_depth) for a, b in zip(positions, positions[1:])
    ])
    return axis, marks, gaps


def map_angle(t):
    return 110 * DEGREES - TAU * t / MAP_PERIOD


def on_ring(center, radius, t):
    angle = map_angle(t)
    return center + radius * xy(np.cos(angle), np.sin(angle))


def circular_map():
    center, radius = xy(-3.62, 0), 2.67
    ring = Circle(
        radius, color=TEXT, stroke_width=6, fill_color=LIGHT_GREY, fill_opacity=0.20,
    ).move_to(center)
    marks = VGroup(*[marker(i, on_ring(center, radius, t), 1.42) for i, t in enumerate(ENTRY)])
    return center, radius, ring, marks


def origin_arrow(center, radius, time, direction):
    return CurvedArrow(
        on_ring(center, radius - 0.37, time),
        on_ring(center, radius - 0.37, time + direction * 10),
        angle=-direction * TAU / 10, color=ORANGE, stroke_width=5,
        tip_length=0.22,
    )


def plate(center, width, height):
    return Ellipse(
        width=width, height=height, stroke_color=LIGHT_GREY, stroke_width=4,
        fill_color=LIGHT_GREY, fill_opacity=0.23,
    ).move_to(center)


class S00Hook(SpokenScene):
    def construct(self):
        recipient, routes, schematic = route_world()
        marks = questions()
        cargo = unknown_cargo((-5.65, -5.10, -5.42))
        inherited = dna(xy(4.26, 0.35), 1.30)
        self.at("A bacterium gained")
        self.add(recipient, routes, schematic)
        self.play(GrowFromCenter(inherited), run_time=1.12)
        self.play(FadeIn(marks, lag_ratio=0.22), run_time=1.12)
        self.at("What carried it there")
        self.play(routes.animate.set_stroke(opacity=0.88), FadeIn(cargo), run_time=1.21)
        self.at("journey reveal a map")
        self.play(cargo.animate.shift(RIGHT * 1.65), run_time=1.80, rate_func=linear)
        self.at("Watch the donor DNA")
        self.play(cargo.animate.shift(RIGHT * 1.51), run_time=2.59, rate_func=linear)
        self.at("Bacteria do not make")
        self.play(cargo.animate.shift(RIGHT * 1.65), run_time=2.40, rate_func=linear)
        self.at("donor genes can become inherited")
        self.play(
            cargo[0].animate.move_to(xy(1.57, 1.85)),
            cargo[1].animate.move_to(xy(1.63, 0)),
            cargo[2].animate.move_to(xy(1.51, -1.85)), run_time=1.90,
        )
        self.finish()


class S01Title(TitleCard):
    TITLE = "From DNA Route to Gene Order"
    LESSON = "Bacterial and Phage Genetics: Conjugation, Transduction and Transformation"

    def construct(self):
        recipient, routes, schematic = route_world()
        routes.set_stroke(opacity=0.88)
        cargo = unknown_cargo((1.57, 1.63, 1.51))
        title = fit_text(self.TITLE, max_w=11.6, size=49, font=TITLE_FONT).move_to(xy(-0.30, 3.40))
        self.add(recipient, routes, schematic, questions(), cargo, dna(xy(4.26, 0.35), 1.30))
        self.play(FadeIn(title), cargo.animate.shift(RIGHT * 1.74), run_time=self.narration_s)


class S02ThreeRoutes(SpokenScene):
    def construct(self):
        recipient, routes, schematic = route_world()
        routes.set_stroke(opacity=0.88)
        marks = questions()
        bare, donor, virus = route_carriers()
        stray = unknown_cargo((3.31, 3.37, 3.25))
        inherited = dna(xy(4.26, 0.35), 1.30)
        self.add(recipient, routes, schematic, marks, stray, inherited)

        top_label = T("transformation", 31, GOLD).move_to(xy(-4.43, 2.65))
        mid_label = T("conjugation", 31, TEAL).move_to(xy(-4.43, 0.99))
        low_label = T("transduction", 31, PURPLE).move_to(xy(-4.43, -2.91))
        self.at("One path exposes")
        self.play(
            FadeOut(marks[0]), FadeOut(stray), FadeOut(inherited),
            FadeIn(bare, shift=RIGHT * 0.45), run_time=0.82,
        )
        self.play(bare.animate.set_x(-0.65), run_time=1.16, rate_func=linear)
        self.at("for transformation")
        self.play(FadeIn(top_label), run_time=0.58)
        self.at("Another joins donor")
        self.play(FadeOut(marks[1]), FadeIn(donor), run_time=0.58)
        self.play(donor.animate.set_x(0.80), run_time=1.36)
        conduit = link(donor, recipient)
        self.play(FadeIn(conduit), run_time=0.34)
        self.at("for conjugation")
        packet = dna(xy(0.70), 0.63)
        self.play(FadeIn(mid_label), FadeIn(packet), run_time=0.46)
        self.play(packet.animate.set_x(3.49), run_time=1.22, rate_func=linear)
        self.at("The third protects")
        self.play(FadeOut(marks[2]), FadeIn(virus), run_time=0.65)
        self.play(virus.animate.set_x(1.05), run_time=2.68, rate_func=linear)
        self.at("during transduction")
        self.play(FadeIn(low_label), virus.animate.set_x(2.47), run_time=1.03)
        self.at("Competent cells take up")
        self.play(bare.animate.move_to(xy(4.16, 1.68)), run_time=2.06)
        self.finish()


class S03TwoTests(SpokenScene):
    def construct(self):
        recipient, routes, schematic = route_world()
        bare, donor, virus = route_carriers()
        gate = filter_gate(-1.25)
        filter_label = T("filter", 30, BLUE).move_to(xy(-1.25, 3.46))
        self.add(recipient, routes, schematic, bare, donor, virus)
        self.at("A filter that stops")
        self.play(FadeIn(gate, shift=DOWN * 0.65), run_time=0.80)
        self.play(FadeIn(filter_label), donor.animate.set_x(-2.73), run_time=0.88)
        self.at("blocks only the contact")
        self.play(
            bare.animate.set_x(1.09), virus.animate.set_x(0.36),
            run_time=2.60, rate_func=linear,
        )
        self.at("Deoxyribonucleus destroys")
        enzyme = RoundedRectangle(
            width=1.04, height=4.89, corner_radius=0.26,
            stroke_width=0, fill_color=RED, fill_opacity=0.33,
        ).move_to(xy(0.11)).set_z_index(-0.5)
        enzyme_label = T("DNase", 32, RED).move_to(xy(1.48, 3.02))
        self.play(FadeIn(enzyme), FadeIn(enzyme_label), run_time=0.58)
        self.play(
            enzyme.animate.set_x(1.29),
            ShrinkToCenter(bare), run_time=1.64,
        )
        self.at("a phage coat protects")
        self.play(enzyme.animate.set_x(2.01), virus.animate.set_x(1.45), run_time=2.27)
        self.at("two -step test")
        self.play(
            FadeOut(enzyme), FadeOut(enzyme_label), FadeOut(filter_label),
            donor.animate.set_stroke(width=7), virus[0].animate.set_stroke(width=9),
            run_time=1.83,
        )
        self.play(FadeOut(gate), FadeOut(donor), FadeOut(virus), run_time=0.60)
        self.finish()


class S04Predict(SpokenScene):
    def construct(self):
        recipient, routes, schematic = route_world()
        left, right, options = evidence_board(filter_highlight=0)
        question = question_card(QUESTION, **QUESTION_STYLE)
        self.add(recipient, routes, schematic)
        self.at("An unknown transfer")
        self.play(FadeOut(recipient), FadeOut(routes), FadeOut(schematic), run_time=0.45)
        self.play(FadeIn(left[0]), FadeIn(left[2]), run_time=0.89)
        self.play(FadeIn(left[1]), run_time=0.55)
        self.at("but stops when cells")
        self.play(FadeIn(right[0]), FadeIn(right[2]), run_time=1.12)
        self.play(FadeIn(right[1]), run_time=0.57)
        self.at("Which carrier fits")
        self.play(FadeIn(question), run_time=0.69)
        self.play(LaggedStart(*[FadeIn(option) for option in options], lag_ratio=0.38), run_time=1.30)
        self.at("Follow both clues")
        self.play(
            left[0].animate.set_stroke(width=5).set_fill(RED, opacity=0.25),
            right[0].animate.set_stroke(width=5).set_fill(BLUE, opacity=0.14),
            run_time=1.56,
        )
        self.at("One result rules out")
        self.play(left[0].animate.set_stroke(width=2.5).set_fill(opacity=0), run_time=1.22)
        self.at("The other rules out")
        packet = right[2][0]
        initial = packet.get_center()
        self.play(packet.animate.shift(LEFT * 0.78), run_time=0.62)
        self.play(packet.animate.move_to(initial), run_time=0.87, rate_func=linear)
        self.at("a phage", lead=-0.70)
        self.play(right[0].animate.set_stroke(width=2.5).set_fill(BLUE, opacity=0.32),
                  run_time=0.59, rate_func=linear)
        self.finish()


class S05Pause(PredictPause):
    QUESTION = QUESTION
    CARD = QUESTION_STYLE
    SECONDS = 4.5

    def construct(self):
        self.add(*evidence_board(), question_card(self.QUESTION, **self.CARD))
        self.wait(self.SECONDS)


class S06Reveal(SpokenScene):
    def construct(self):
        left, right, options = evidence_board()
        question = question_card(QUESTION, **QUESTION_STYLE)
        donor, recipient, bridge = contact_pair()
        self.add(left, right, options, question)
        self.at("Conjugation fits")
        self.play(
            options[0].animate.set_opacity(0.33), options[2].animate.set_opacity(0.33),
            left.animate.set_opacity(0.28), right[0].animate.set_fill(opacity=0),
            run_time=0.47, rate_func=linear,
        )
        self.play(FadeOut(left), FadeOut(right), FadeOut(question), FadeOut(options[0]),
                  FadeOut(options[2]), FadeOut(options[1][1]), run_time=0.68)
        self.play(ReplacementTransform(options[1][0], donor), FadeIn(recipient), run_time=0.94)
        self.at("Its DNA is never exposed")
        self.play(GrowFromCenter(bridge), run_time=0.79)
        packet = dna(xy(-2.41), 0.80)
        self.add(packet)
        self.play(packet.animate.set_x(0.12), run_time=1.12, rate_func=linear)
        self.at("the enzyme misses it")
        band = RoundedRectangle(
            width=1.0, height=5.34, corner_radius=0.19, stroke_width=0,
            fill_color=RED, fill_opacity=0.33,
        ).move_to(xy(-1.55)).set_z_index(-1)
        self.play(FadeIn(band), run_time=0.30)
        self.play(
            band.animate.set_x(3.00), packet.animate.set_x(3.37),
            run_time=1.80, rate_func=linear,
        )
        self.at("Separating the cells")
        gate = separation_gate(0)
        self.play(FadeOut(band), FadeOut(bridge), FadeIn(gate, shift=DOWN * 0.65),
                  donor.animate.shift(LEFT * 0.34), recipient.animate.shift(RIGHT * 0.34), run_time=1.84)
        self.at("Both clues point")
        rule = caption("direct contact", color=TEAL, size=36, y=-3.00).set_x(0)
        self.play(FadeOut(gate), FadeOut(packet), donor.animate.set_x(DONOR_X),
                  recipient.animate.set_x(RECIPIENT_X), run_time=1.23)
        self.play(GrowFromCenter(bridge), run_time=1.10)
        self.play(FadeIn(rule), run_time=0.59)
        self.at("DNA moving through")
        self.play(bridge.animate.set_fill(opacity=0.65), run_time=0.68)
        self.play(bridge.animate.set_fill(opacity=0.25), FadeOut(rule), run_time=0.84)
        self.finish()


class S07FFactor(SpokenScene):
    def construct(self):
        donor, recipient, bridge = contact_pair()
        chrom_d, chrom_r = pair_chromosomes()
        f = plasmid(DONOR_X)
        f_label = T("F", 30, ORANGE).move_to(f)
        plus = T("F+", 36, ORANGE).move_to(xy(DONOR_X, 2.80))
        minus = T("F−", 36, LIGHT_GREY).move_to(xy(RECIPIENT_X, 2.80))
        self.add(donor, recipient, bridge)
        self.at("In E. coli")
        self.play(Create(chrom_d), Create(chrom_r), run_time=0.80)
        self.play(GrowFromCenter(f), run_time=1.25)
        self.at("a small DNA circle")
        self.play(FadeIn(f_label), run_time=0.60)
        self.at("Free F transfers")
        self.play(FadeIn(plus), FadeIn(minus), FadeOut(f_label),
                  donor.animate.set_fill(opacity=0.49), run_time=0.90)
        strand = VMobject(stroke_color=ORANGE, stroke_width=28).set_points_smoothly(
            [xy(-2.87, -0.10), xy(-2.49, 0.18), xy(-2.16, -0.06), xy(-1.77, 0.04)]
        )
        retained = Arc(radius=0.53, start_angle=0.90, angle=4.84,
                       arc_center=f.get_center(), color=ORANGE, stroke_width=13)
        self.play(ReplacementTransform(f, retained), TransformFromCopy(f, strand), run_time=2.53)
        new_d = plasmid(DONOR_X)
        new_r = plasmid(RECIPIENT_X).shift(LEFT * 0.16)
        self.at("One strand crosses")
        self.play(
            strand.animate.set_x(new_r.get_x()),
            donor.animate.set_fill(opacity=0.31),
            bridge.animate.set_fill(ORANGE, opacity=0.53),
            run_time=2.16, rate_func=linear,
        )
        self.at("each cell completes")
        self.play(
            ReplacementTransform(retained, new_d), ReplacementTransform(strand, new_r),
            bridge.animate.set_fill(TEAL, opacity=0.25), run_time=1.33,
        )
        converted = T("F+", 36, ORANGE).move_to(minus)
        self.play(swap(minus, converted, run_time=0.77))
        self.at("Chromosomal markers rarely")
        self.play(chrom_d.animate.set_stroke(width=18), chrom_r.animate.set_stroke(width=18), run_time=0.88)
        self.play(chrom_d.animate.set_stroke(width=12), chrom_r.animate.set_stroke(width=12),
                  FadeOut(plus), FadeOut(converted),
                  run_time=0.87)
        self.finish()


class S08Hfr(SpokenScene):
    def construct(self):
        donor, recipient, bridge = contact_pair()
        chrom_d, chrom_r = pair_chromosomes()
        # A fresh recipient illustrates the Hfr pairing after the free-F example.
        f = plasmid(DONOR_X)
        self.add(donor, recipient, bridge, chrom_d, chrom_r, f)
        self.at("When F joins")
        embedded = Arc(radius=1.19, start_angle=-0.30, angle=0.62, arc_center=chrom_d.get_center(),
                       color=ORANGE, stroke_width=24)
        self.play(ReplacementTransform(f, embedded), chrom_d.animate.set_stroke(width=17), run_time=1.94)
        self.at("the cell is HFR")
        hfr = T("Hfr", 36, ORANGE).move_to(xy(DONOR_X, 2.80))
        self.play(FadeIn(hfr), run_time=0.70)
        self.at("Transfer now pulls")
        # In the enlarged transfer view the recipient chromosome stays separate from incoming DNA.
        strip = VMobject(stroke_color=TEXT, stroke_width=15).set_points_smoothly(
            [xy(-5.50, 0.04), xy(-3.75, -0.39), xy(-2.44, -0.13), xy(-0.75, 0),
             xy(0.75, 0), xy(1.93, 0.52), xy(3.15, 0.69)]
        )
        arrow = Arrow(xy(-0.71, 0.66), xy(0.71, 0.66), buff=0, color=ORANGE,
                      stroke_width=5, tip_length=0.24)
        origin = strip.get_subcurve(0.96, 1).set_stroke(color=ORANGE, width=17)
        starting_proportions = tuple(0.49 - 0.014 * (t - ENTRY[0]) for t in ENTRY)
        marks = VGroup(*[
            marker(i, strip.point_from_proportion(u), 1.53)
            for i, u in enumerate(starting_proportions)
        ])
        self.play(
            ReplacementTransform(chrom_d, strip), ReplacementTransform(embedded, origin),
            chrom_r.animate.shift(DOWN * 0.82), GrowArrow(arrow), run_time=1.32,
        )
        self.play(FadeIn(marks), run_time=0.41)
        self.at("through the same origin")
        self.play(*[
            MoveAlongPath(mark, VMobject().set_points_smoothly(
                [strip.point_from_proportion(u) for u in np.linspace(start, start + 0.43, 20)]
            ))
            for mark, start in zip(marks, starting_proportions)
        ], run_time=3.16, rate_func=linear)
        self.at("pairs usually separate")
        kept = strip.get_subcurve(0.68, 1)
        rest = strip.get_subcurve(0, 0.47)
        self.remove(strip)
        self.add(kept, rest)
        self.play(
            FadeOut(bridge), FadeOut(arrow), donor.animate.shift(LEFT * 0.34),
            recipient.animate.shift(RIGHT * 0.34), rest.animate.shift(LEFT * 0.34),
            kept.animate.shift(RIGHT * 0.34), marks[0].animate.shift(RIGHT * 0.34),
            marks[1].animate.shift(RIGHT * 0.34), marks[2].animate.move_to(xy(-2.06, -0.20)),
            chrom_r.animate.shift(RIGHT * 0.34),
            origin.animate.shift(RIGHT * 0.34), hfr.animate.shift(LEFT * 0.34),
            run_time=1.63,
        )
        self.at("recipients receive only part")
        piece = caption("part arrives", size=33, color=GOLD, y=-3.02).set_x(RECIPIENT_X)
        received_patch = RoundedRectangle(
            width=2.38, height=1.00, corner_radius=0.28, stroke_width=0,
            fill_color=GOLD, fill_opacity=0.45,
        ).move_to(kept.get_center() + RIGHT * 0.37)
        self.play(
            FadeIn(piece), FadeIn(received_patch),
            kept.animate.set_stroke(color=GOLD, width=22).shift(RIGHT * 0.37),
            marks[0].animate.shift(RIGHT * 0.37), marks[1].animate.shift(RIGHT * 0.37),
            origin.animate.shift(RIGHT * 0.37), run_time=1.29,
        )
        self.bring_to_front(kept, marks[0], marks[1], origin)
        self.at("The remaining F sequence")
        last = T("F sequence arrives last", 31, ORANGE).move_to(xy(DONOR_X, -3.02))
        remaining = rest.get_subcurve(0, 0.18).set_stroke(color=ORANGE, width=24)
        tail_patch = RoundedRectangle(
            width=2.01, height=1.12, corner_radius=0.28, stroke_width=0,
            fill_color=ORANGE, fill_opacity=0.53,
        ).move_to(rest.get_start() + RIGHT * 0.65)
        self.play(
            FadeOut(received_patch), FadeIn(tail_patch), Create(remaining),
            run_time=0.82,
        )
        self.play(FadeIn(last), origin.animate.set_stroke(opacity=0.2), run_time=1.13)
        self.finish()


class S09Timeline(SpokenScene):
    def construct(self):
        heights = (2.12, 0.90, -0.32, -1.54)
        rows, received = [], []
        for j, y in enumerate(heights):
            donor = bacterium(xy(-5.13, y), TEAL, 2.02, 0.87)
            recipient = bacterium(xy(-2.25, y), LIGHT_GREY, 2.02, 0.87)
            bridge = Line(donor.get_right(), recipient.get_left(), color=TEAL, stroke_width=6)
            row_dna = VGroup(*[marker(i, xy(-4.78 - 0.37 * i, y), 0.81) for i in range(len(ENTRY))])
            rows.append((donor, recipient, bridge, row_dna))
            received.append(VGroup(*row_dna[:j]))
        self.add(*[obj for row in rows for obj in row])
        stop = Line(xy(-4.16, 2.61), xy(-4.16, 1.64), color=RED, stroke_width=8)
        self.at("Break different pairs apart")
        self.play(Create(stop), run_time=0.30)
        for j, (donor, recipient, bridge, row_dna) in enumerate(rows):
            ys = heights[j]
            cutoff = Line(xy(-3.68, ys + 0.48), xy(-3.68, ys - 0.48), color=RED, stroke_width=8)
            traveling = [
                m.animate.move_to(xy(-2.55 + 0.30 * i, ys)) for i, m in enumerate(received[j])
            ]
            self.play(Transform(stop, cutoff), *traveling, run_time=0.44)
            self.play(FadeOut(bridge), donor.animate.shift(LEFT * 0.23),
                      recipient.animate.shift(RIGHT * 0.16), run_time=0.19)
        self.at("then score the recipients")
        scoring_plate = plate(xy(3.61, 0.25), 4.9, 4.35)
        self.play(FadeOut(stop), FadeIn(scoring_plate), run_time=0.58)
        score_label = T("Recipient markers", 31, LIGHT_GREY).move_to(xy(3.56, 3.00))
        self.play(FadeIn(score_label), run_time=0.55)
        scores = [
            VGroup(*[colony_marker(i, xy(2.82 + 0.79 * i, heights[j] + 0.48)) for i in range(j)])
            for j in range(len(rows))
        ]

        axis, marks, gaps = entry_map()
        self.at("Markers nearer the origin")
        self.play(Create(axis), run_time=0.57)
        for i, symbol in enumerate(marks):
            self.play(TransformFromCopy(received[i + 1][i], symbol), run_time=0.68)
        self.at("With steady transfer")
        self.play(LaggedStart(*[Create(gap) for gap in gaps], lag_ratio=0.40), run_time=1.55)
        self.at("time gaps become")
        gap_label = T("time gaps", 29, GOLD).move_to(xy(4.46, -3.10))
        self.play(FadeIn(gap_label), run_time=0.64)
        self.at("Selective plates reveal")
        self.play(scoring_plate.animate.set_fill(opacity=0.43), run_time=0.73)
        self.play(LaggedStart(*[
            TransformFromCopy(received[j], scores[j]) for j in range(1, len(rows))
        ], lag_ratio=0.53), run_time=2.73)
        self.at("A marker's entry time")
        # The triangle is missing in the earlier scores and first present on the last row.
        triangle = scores[-1][-1]
        chosen = SurroundingRectangle(triangle, color=GOLD, stroke_width=4, corner_radius=0.12, buff=0.13)
        self.play(Create(chosen), scoring_plate.animate.set_fill(opacity=0.23), run_time=0.69)
        mark_box = SurroundingRectangle(
            marks[-1], color=GOLD, stroke_width=4, corner_radius=0.12, buff=0.10,
        )
        self.play(TransformFromCopy(chosen, mark_box), run_time=0.80)
        self.at("still yields it")
        self.play(*[FadeOut(obj) for donor, recipient, _, row_dna in rows
                    for obj in (donor, recipient, row_dna)],
                  FadeOut(scoring_plate), FadeOut(score_label), FadeOut(chosen),
                  FadeOut(mark_box), FadeOut(gap_label), *[FadeOut(score) for score in scores[1:]],
                  run_time=0.91)
        self.finish()


class S10Reverse(SpokenScene):
    def construct(self):
        axis, line_marks, line_gaps = entry_map()
        center, radius, ring, ring_marks = circular_map()
        first_arrow = origin_arrow(center, radius, 0, 1)
        second_arrow = origin_arrow(center, radius, MAP_PERIOD / 2, -1)
        self.add(axis, line_marks, line_gaps)
        self.at("A different HFR origin")
        ring.set_fill(opacity=0)
        self.play(ReplacementTransform(axis, ring), ReplacementTransform(line_marks, ring_marks),
                  FadeOut(line_gaps), run_time=1.12)
        self.play(Create(first_arrow), ring.animate.set_fill(opacity=0.20), run_time=0.58)
        self.at("can send the same")
        self.play(Transform(first_arrow, second_arrow), run_time=1.39)
        scale, x0 = 0.132, 0.23
        first_times = ENTRY
        reverse_times = tuple(MAP_PERIOD / 2 - t for t in reversed(ENTRY))
        ys = (1.43, -1.19)
        axes = [
            Line(xy(x0, y), xy(6.38, y), color=TEXT, stroke_width=5, stroke_opacity=0.77)
            for y in ys
        ]
        order_a = VGroup(*[
            marker(i, xy(x0 + scale * t, ys[0]), 1.25) for i, t in enumerate(first_times)
        ])
        order_b = VGroup(*[
            marker(i, xy(x0 + scale * t, ys[1]), 1.25)
            for i, t in zip(reversed(range(len(ENTRY))), reverse_times)
        ])
        headings = VGroup(
            T("First origin", 30, ORANGE).move_to(xy(2.45, 2.42)),
            T("Opposite origin", 30, ORANGE).move_to(xy(2.45, -2.50)),
        )
        zero_ticks = VGroup(*[
            Line(xy(x0, y - 0.17), xy(x0, y + 0.17), color=ORANGE, stroke_width=6) for y in ys
        ])
        self.at("the other way")
        self.play(Create(axes[1]), FadeIn(headings[1]), FadeIn(zero_ticks[1]), run_time=0.64)
        self.play(LaggedStart(*[
            TransformFromCopy(mark, target) for mark, target in zip(reversed(ring_marks), order_b)
        ], lag_ratio=0.35), run_time=1.40)
        self.at("Absolute arrival times change")
        self.play(Create(axes[0]), FadeIn(headings[0]), FadeIn(zero_ticks[0]), run_time=0.67)
        self.play(LaggedStart(*[TransformFromCopy(a, b) for a, b in zip(ring_marks, order_a)],
                              lag_ratio=0.30), run_time=0.83)
        brackets = [
            VGroup(*[interval_band(a[0], b[0], y - 0.48, color)
                     for a, b in zip(positions, positions[1:])])
            for positions, y, color in zip(
                ([p.get_center() for p in order_a], [p.get_center() for p in order_b]),
                ys, (GOLD, TEAL),
            )
        ]
        self.at("matching gaps reveal")
        self.play(Create(brackets[0]), Create(brackets[1]), run_time=0.52)
        aligned_y = ys[0] - 0.74
        aligned = VGroup(*[
            interval_band(a.get_x(), b.get_x(), aligned_y, TEAL) for a, b in zip(order_a, order_a[1:])
        ])
        self.play(*[
            Transform(bracket, target, path_arc=-PI / 4)
            for bracket, target in zip(reversed(brackets[1]), aligned)
        ], run_time=1.23)
        arcs = VGroup(*[
            Arc(radius=radius + 0.22, start_angle=map_angle(a), angle=map_angle(b) - map_angle(a),
                arc_center=center, color=GOLD, stroke_width=16)
            for a, b in zip(ENTRY, ENTRY[1:])
        ])
        self.at("one circular map")
        self.play(TransformFromCopy(brackets[0], arcs), run_time=1.25)
        self.at("The origin sets")
        lead_ins = VGroup(*[
            interval_band(x0, order[0].get_x(), y + 0.19, ORANGE, height=0.32)
            for y, order in zip(ys, (order_a, order_b))
        ])
        self.play(
            Transform(first_arrow, origin_arrow(center, radius, 0, 1)),
            LaggedStart(*[GrowFromEdge(band, LEFT) for band in lead_ins], lag_ratio=0.32),
            run_time=1.54,
        )
        self.at("absolute times cannot be compared")
        self.play(FadeOut(zero_ticks), FadeOut(headings), FadeOut(lead_ins), run_time=0.71)
        self.play(FadeOut(axes[0]), FadeOut(axes[1]), FadeOut(order_a), FadeOut(order_b),
                  FadeOut(brackets[0]), FadeOut(brackets[1]), run_time=1.34)
        self.play(FadeOut(arcs), FadeOut(first_arrow), run_time=0.67)
        self.finish()


class S11Readout(SpokenScene):
    def construct(self):
        center, radius, ring, marks = circular_map()
        dish = plate(xy(-2.16, -0.15), 8.45, 5.71).set_z_index(-2)
        spots = (xy(-4.75, 1.07), xy(-3.43, -1.05), xy(-1.80, 1.23),
                 xy(-0.56, -0.76), xy(0.69, 0.65), xy(-2.31, -1.93))
        cells = VGroup(*[bacterium(p, LIGHT_GREY, 0.63, 0.41) for p in spots])
        picks = (1, 4)
        self.add(ring, marks)
        self.at("Selection makes rare")
        tiny_ring = chromosome(spots[picks[1]], 0.10)
        self.play(FadeIn(dish), FadeIn(cells), ReplacementTransform(ring, tiny_ring),
                  FadeOut(marks), run_time=0.96)
        colonies = VGroup(*[
            Circle(radius=0.48, color=GOLD, stroke_width=4, fill_color=GOLD,
                   fill_opacity=0.54).move_to(spots[i])
            for i in picks
        ])
        self.play(*[FadeOut(c) for i, c in enumerate(cells) if i not in picks],
                  *[ReplacementTransform(cells[i], co) for i, co in zip(picks, colonies)],
                  FadeOut(tiny_ring), run_time=1.51)

        chain = VGroup(*[
            chip(name, color, size=30)
            for name, color in (("entry", GOLD), ("integration", GOLD), ("expression", TEXT))
        ]).arrange(DOWN, buff=0.71).move_to(xy(4.17, 1.36))
        arrows = [
            Arrow(a.get_bottom(), b.get_top(), buff=0.16, color=LIGHT_GREY, stroke_width=4, tip_length=0.15)
            for a, b in zip(chain, chain[1:])
        ]
        self.at("but a colony reports")
        focus_at = xy(-2.00, 0.52)
        focus = bacterium(focus_at, LIGHT_GREY, 6.70, 4.81)
        focal_ring = chromosome(focus_at + RIGHT * 0.66, 1.43)
        incoming = dna(xy(-4.52, -0.46), 1.37)
        self.play(
            FadeOut(dish), FadeOut(colonies),
            TransformFromCopy(colonies[1], focus), run_time=1.36,
        )
        self.play(Create(focal_ring), FadeIn(chain[0]), run_time=0.83)
        self.at("The donor piece must")
        self.play(FadeIn(incoming), run_time=0.42)
        self.play(incoming.animate.move_to(xy(-3.52, -1.38)), run_time=1.54)
        self.at("and usually integrated")
        self.play(GrowArrow(arrows[0]), FadeIn(chain[1]), run_time=0.78)
        self.at("Incoming linear DNA")
        # The fragment remains separate until it can replace the same segment of the chromosome.
        recipient_arc = Arc(radius=1.43, start_angle=-2.47, angle=1.06,
                            arc_center=focal_ring.get_center(), color=TEXT, stroke_width=24)
        self.play(
            incoming.animate.move_to(xy(-2.03, -1.42)).stretch(1.18, dim=0),
            Create(recipient_arc), run_time=2.41,
        )
        self.at("with the chromosome")
        self.play(focal_ring.animate.set_fill(TEXT, opacity=0.22), run_time=1.12)
        self.at("Recombination can replace")
        self.play(focal_ring.animate.set_fill(opacity=0), run_time=0.46)
        white = Arc(radius=1.43, start_angle=-1.41, angle=TAU - 1.06,
                    arc_center=focal_ring.get_center(), color=TEXT, stroke_width=12)
        integrated = recipient_arc.copy().set_stroke(color=GOLD)
        self.remove(focal_ring)
        self.add(white)
        self.play(ReplacementTransform(incoming, integrated), FadeOut(recipient_arc), run_time=1.51)
        self.play(GrowArrow(arrows[1]), FadeIn(chain[2]), run_time=0.76)
        self.play(focus.animate.set_fill(opacity=0.41), run_time=0.80)
        self.finish()


class S12Rule(SpokenScene):
    def construct(self):
        donor, recipient, bridge = contact_pair()
        self.add(donor, recipient, bridge)
        strand = Line(xy(-5.29), xy(3.21), color=TEXT, stroke_width=7)
        ordered = VGroup(*[marker(i, xy(-1.08 - 0.088 * (t - ENTRY[0])), 1.42)
                           for i, t in enumerate(ENTRY)])
        self.at("created the readout")
        self.play(Create(strand), FadeIn(ordered), run_time=0.61)
        self.play(ordered.animate.shift(RIGHT * 3.98), run_time=1.60, rate_func=linear)
        self.at("For HFR transfer")
        axis, marks, gaps = entry_map(-0.25, gap_depth=0.39)
        self.play(ReplacementTransform(strand, axis),
                  *[ReplacementTransform(a, b) for a, b in zip(ordered, marks)],
                  donor.animate.set_fill(opacity=0.18).set_stroke(opacity=0.20),
                  recipient.animate.set_fill(opacity=0.18).set_stroke(opacity=0.20),
                  FadeOut(bridge), run_time=1.46)
        self.at("ordered arrival maps")
        title = T("Gene order", 39, TEXT).move_to(xy(0, 2.98))
        self.play(FadeIn(title), run_time=0.51)
        self.play(LaggedStart(*[
            symbol.animate.scale(1.19) for symbol in marks
        ], lag_ratio=0.32), run_time=1.36)
        self.at("If transfer is roughly steady")
        steady = T("Steady transfer", 31, LIGHT_GREY).move_to(xy(0, -2.88))
        self.play(FadeIn(steady), run_time=0.58)
        self.play(LaggedStart(*[Create(gap) for gap in gaps], lag_ratio=0.43), run_time=1.43)
        self.at("time gaps also map")
        bands = VGroup(*[
            interval_band(a.get_x(), b.get_x(), -0.94, GOLD, height=0.40)
            for a, b in zip(marks, marks[1:])
        ])
        self.play(
            swap(steady, T("Time gaps → distance", 33, GOLD).move_to(steady), 1.02),
            LaggedStart(*[GrowFromEdge(band, LEFT) for band in bands], lag_ratio=0.43),
            run_time=1.48,
        )
        self.at("Keep the gaps")
        measured = Line(marks[0].get_center(), marks[-1].get_center(), color=TEXT, stroke_width=6)
        self.play(Transform(axis, measured), bands.animate.set_fill(opacity=0.94), run_time=0.89)
        self.play(bands.animate.set_fill(opacity=0.57), run_time=0.76)
        self.finish()


class S13End(EndCard):
    LINE = "Ordered arrival maps gene order; time gaps map distance."
