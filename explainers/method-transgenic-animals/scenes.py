"""Transgenic animals: one schematic from fertilized egg to whole animal.

Color map: slate and GREY = anatomy; BLUE = apparatus; ORANGE = added DNA;
GREEN = reporters; GOLD = inheritance, highlighted outcomes and questions;
PURPLE = neural tissue and Version B; RED = disrupted DNA.
"""

from bp_parts import *  # noqa: F403
from bp_style import EndCard


ORANGE = "#F29E4C"
PURPLE = "#B58CD9"
ANATOMY = "#344A60"
INNER = "#222F42"
EGG = np.array([-3.93, -0.12, 0])
MOUSE = np.array([3.38, -0.52, 0])
BRAIN = MOUSE + np.array([-0.85, 0.90, 0])
RIBBON_HOME = EGG + UP * 2.64
QUESTION = "Does glowing prove cause?"
QUESTION_STYLE = {"y": 2.93, "left": -0.90, "size": 36}


def point(x, y):
    return np.array([x, y, 0])


def shape(start, segments, fill, outline=GREY, width=3):
    """Smooth closed silhouette from cubic segments in local coordinates."""
    path = VMobject(fill_color=fill, fill_opacity=1, stroke_color=outline, stroke_width=width)
    path.start_new_path(point(*start))
    for control1, control2, end in segments:
        path.add_cubic_bezier_curve_to(point(*control1), point(*control2), point(*end))
    path.close_path()
    return path


def disc(radius, fill, outline=GREY, width=2):
    return Circle(radius=radius, fill_color=fill, fill_opacity=1, stroke_color=outline, stroke_width=width)


def ribbon(center, color=ORANGE, width=1.23):
    glow = RoundedRectangle(
        width=width + 0.18, height=0.42, corner_radius=0.17,
        stroke_width=0, fill_color=color, fill_opacity=0.22,
    )
    bar = RoundedRectangle(
        width=width, height=0.23, corner_radius=0.10,
        stroke_width=1.5, stroke_color=color, fill_color=color, fill_opacity=1,
    )
    return VGroup(glow, bar).move_to(center)


def egg(center=EGG, radius=1.92, chromosomes=True):
    """The same membrane and pronuclei at each magnification."""
    shell = disc(radius, ANATOMY, width=4)
    inner = disc(radius * 0.88, INNER, outline="#627A96", width=2.5)
    left = disc(radius * 0.28, ANATOMY, outline="#829CB7").shift(LEFT * radius * 0.37 + DOWN * radius * 0.13)
    right = disc(radius * 0.25, ANATOMY, outline="#829CB7").shift(RIGHT * radius * 0.29 + UP * radius * 0.21)
    pronuclei = VGroup(left, right)
    bars = VGroup(
        Line(left.get_center() + LEFT * radius * 0.09, left.get_center() + RIGHT * radius * 0.09),
        Line(right.get_center() + LEFT * radius * 0.08, right.get_center() + RIGHT * radius * 0.08),
    ).set_stroke(GREY, 5)
    picture = VGroup(shell, inner, pronuclei)
    if chromosomes:
        picture.add(bars)
    picture.shift(center)
    return picture


def mouse(center=MOUSE, scale=1):
    """A left-facing mouse with the same landmarks across the film."""
    body = shape((-2.43, 0.50), [
        ((-2.48, 0.77), (-2.20, 1.06), (-1.85, 1.30)),
        ((-1.71, 1.49), (-1.41, 1.79), (-0.94, 1.64)),
        ((-0.57, 2.08), (-0.08, 2.06), (0.08, 1.52)),
        ((0.65, 1.90), (1.60, 1.76), (1.99, 1.12)),
        ((2.52, 0.41), (2.20, -0.57), (1.63, -0.94)),
        ((1.73, -1.16), (1.40, -1.32), (0.83, -1.27)),
        ((0.51, -1.25), (0.56, -1.07), (0.64, -0.94)),
        ((0.12, -1.06), (-0.56, -0.99), (-0.89, -0.75)),
        ((-0.94, -1.07), (-1.62, -1.10), (-1.74, -0.89)),
        ((-1.84, -0.75), (-1.59, -0.62), (-1.46, -0.52)),
        ((-1.59, -0.14), (-1.73, 0.13), (-2.09, 0.30)),
        ((-2.32, 0.34), (-2.42, 0.39), (-2.43, 0.50)),
    ], ANATOMY, width=3.6)
    tail = CubicBezier(point(1.68, -0.62), point(3.02, -0.64), point(2.91, -2.45), point(1.86, -1.86))
    tail.set_stroke(GREY, 4.5)
    ear = Ellipse(width=0.45, height=0.56, stroke_width=0, fill_color=INNER, fill_opacity=1)
    ear.move_to(point(-0.38, 1.52))
    eye = Dot(point(-1.70, 1.01), radius=0.072, color=TEXT)
    nose = Dot(point(-2.40, 0.54), radius=0.086, color=TEXT)
    return VGroup(tail, body, ear, eye, nose).scale(scale, about_point=ORIGIN).shift(center)


def development_arrow(color=GREY, end_x=0.62):
    return Arrow(point(-1.66, -0.45), point(end_x, -0.45), buff=0, color=color, stroke_width=5,
                 tip_length=0.23)


def breathe_fill(mob, low, high, period=3.8):
    """Let the schematic tissue breathe while keeping all landmarks fixed."""
    low, high = ManimColor(low), ManimColor(high)
    elapsed = 0

    def breathe(tissue, dt):
        nonlocal elapsed
        elapsed += dt
        amount = 0.5 - 0.5 * np.cos(TAU * elapsed / period)
        tissue.set_fill(interpolate_color(low, high, amount))

    mob.add_updater(breathe)


def light_egg(embryo):
    breathe_fill(embryo[1], INNER, "#3D546B")


def light_mouse(adult):
    breathe_fill(adult[1], ANATOMY, "#4C667D")


def stage(marked=False, moving=False):
    """Build the full stage. Overlays use the same coordinates as the anatomy."""
    embryo = egg()
    if marked:
        embryo.add(ribbon(EGG + point(0.49, 0.40), width=0.46).scale(0.62))
    adult = mouse()
    if moving:
        light_egg(embryo)
        light_mouse(adult)
    return embryo, development_arrow(), adult


def heading(text, x=0, y=3.05, color=TEXT, size=34):
    return T(text, size=size, color=color, weight=BOLD).move_to(point(x, y))


def bottom_label(text, x, color=TEXT):
    return T(text, size=30, color=color).move_to(point(x, -3.04))


def dish():
    center = EGG + DOWN * 2.55
    well = Ellipse(width=3.85, height=0.72, color=BLUE, stroke_width=2.5,
                   fill_color=ANATOMY, fill_opacity=0.64).move_to(center)
    cells = VGroup(*[
        Dot(center + point(dx, dy), radius=0.065, color=BLUE)
        for dx, dy in [(-1.34, -0.04), (-0.98, -0.16), (-0.59, 0.12), (0.26, -0.08), (0.84, -0.16), (1.24, 0.04)]
    ])
    return VGroup(well, cells)


def grow_signal(center=BRAIN, radius=0.11):
    return VGroup(*[
        VGroup(disc(radius * 1.6, "#3C5F50", width=0), Dot(point(0, 0), radius=radius * 0.58, color=GREEN))
        .move_to(center + point(x, y))
        for x, y in [(-0.33, 0.02), (-0.14, 0.26), (0.10, -0.12), (0.35, 0.12)]
    ])


def turn_arrow():
    arc = ArcBetweenPoints(point(0.77, 0.34), point(-1.79, 1.12), angle=1.26, color=GOLD, stroke_width=5)
    return arc.add_tip(tip_length=0.24)


def predict_backdrop():
    embryo, arrow, adult = stage(marked=True)
    return VGroup(embryo, arrow, adult, grow_signal(), turn_arrow(), scope_tag(color=TEXT))


def cortical_shape(center, folded=False):
    """Schematic tissue outline, drawn as a filled anatomical shape."""
    if folded:
        edge = [
            ((-2.17, 0.62), (-1.96, 1.49), (-1.58, 1.45)),
            ((-1.23, 1.48), (-1.42, 0.90), (-1.10, 0.91)),
            ((-0.82, 0.93), (-0.98, 1.79), (-0.39, 1.80)),
            ((0.00, 1.81), (-0.02, 1.16), (0.32, 1.16)),
            ((0.67, 1.16), (0.58, 1.86), (1.08, 1.64)),
            ((1.42, 1.51), (1.23, 0.97), (1.55, 0.92)),
            ((1.93, 0.84), (2.15, 0.85), (2.13, 0.24)),
            ((2.12, -0.73), (1.62, -1.13), (0.74, -1.28)),
            ((-0.42, -1.49), (-2.20, -1.10), (-2.12, 0.08)),
        ]
    else:
        edge = [
            ((-2.10, 0.91), (-1.22, 1.63), (-0.07, 1.63)),
            ((1.21, 1.63), (2.17, 1.10), (2.15, 0.24)),
            ((2.12, -0.73), (1.62, -1.13), (0.74, -1.28)),
            ((-0.42, -1.49), (-2.20, -1.10), (-2.12, 0.08)),
        ]
    return shape((-2.12, 0.08), edge, "#4B3D65", PURPLE, width=4).shift(center)


class S01Hook(SpokenScene):
    def construct(self):
        embryo, arrow, adult = stage(moving=True)
        dna = ribbon(RIBBON_HOME)
        query = T("?", size=97, color=GOLD, weight=BOLD).move_to(MOUSE + UP * 0.38)
        culture = dish()
        self.add(embryo, adult, query, dna, scope_tag(color=TEXT))
        self.at("how do you test")
        self.play(dna.animate.shift(DOWN * 0.47), run_time=4.7, rate_func=smooth)
        self.at("cells in a dish")
        self.play(FadeIn(culture, shift=DOWN * 0.18), run_time=0.60)
        self.at("yet a dish")
        self.play(FadeOut(culture), Create(arrow), run_time=1.45)
        self.at("to test one gene")
        self.play(dna.animate.move_to(EGG + UP * 2.46), run_time=2.75)
        self.finish()


class S02Title(TitleCard):
    TITLE = "Adding One Gene to a Living Animal"
    LESSON = "Transgenic animals"

    def construct(self):
        embryo, arrow, adult = stage()
        picture = VGroup(embryo, arrow, adult).fade(0.40)
        dna = ribbon(EGG + UP * 2.46)
        title = fit_text(self.TITLE, max_w=11.9, size=46, min_size=34, font=TITLE_FONT)
        title.move_to(point(0, 3.12))
        self.add(picture, dna, scope_tag(color=TEXT))
        self.play(FadeIn(title, shift=UP * 0.12), run_time=0.55)
        self.play(dna.animate.shift(DOWN * 0.18), run_time=1.44)


class S03Inject(SpokenScene):
    def construct(self):
        embryo, arrow, adult = stage(moving=True)
        dna = ribbon(EGG + UP * 2.28)
        cell_center = point(-2.80, -0.30)
        enlarged_egg = egg(cell_center, 2.44)
        target = enlarged_egg[2][1].get_center()
        pickup = point(2.14, 1.96)
        self.add(embryo, arrow, adult, dna, scope_tag(color=TEXT))
        self.at("that added dna")
        self.play(Transform(embryo, enlarged_egg), FadeOut(arrow), FadeOut(adult),
                  dna.animate.move_to(pickup), run_time=1.20)
        label = heading("Transgene", x=2.14, y=2.70, color=ORANGE)
        self.at("is a transgene")
        self.play(FadeIn(label), run_time=0.42)
        for cue, word in [("gene", "Gene"), ("regulatory switch", "Switch"), ("visible label", "Label")]:
            self.at(cue, lead=0.31)
            next_label = heading(word, x=2.14, y=2.70, color=ORANGE)
            self.play(swap(label, next_label, 0.44), run_time=0.44)
            label = next_label
        needle_tip = dna.get_right() + RIGHT * 0.34
        needle = Polygon(needle_tip, needle_tip + point(2.60, 1.21), needle_tip + point(2.73, 0.87),
                         stroke_color=BLUE, stroke_width=2.5, fill_color=ANATOMY, fill_opacity=1)
        self.at("next pronuclear injection")
        self.play(FadeOut(label), FadeIn(needle), run_time=0.40)
        injection = bottom_label("Pronuclear injection", 2.00, BLUE)
        pickup_tip = dna.get_right() + RIGHT * 0.05
        self.play(FadeIn(injection), needle.animate.shift(pickup_tip - needle_tip), run_time=0.62)
        deposit_tip = target + RIGHT * (dna.width * 0.52 / 2 + 0.05)
        self.play(needle.animate.shift(deposit_tip - pickup_tip),
                  dna.animate.scale(0.52).move_to(target), run_time=2.80)
        self.play(FadeOut(needle, shift=point(3.5, 1.38)), run_time=0.78)
        cluster = VGroup(*[
            disc(0.96, ANATOMY, color, 3.0).move_to(cell_center + point(x, y))
            for x, y, color in [(-0.90, 0.76, GREY), (0.64, 0.71, GOLD), (-0.87, -0.69, GREY), (0.76, -0.72, GOLD)]
        ])
        self.at("when it joins")
        self.play(ReplacementTransform(embryo, cluster), FadeOut(injection),
                  dna.animate.move_to(cluster[1].get_center()), run_time=1.10)
        germ = bottom_label("Germ line", -2.77, GOLD)
        self.at("the cells that pass")
        self.play(FadeIn(germ), run_time=0.38)
        for cell in cluster:
            breathe_fill(cell, ANATOMY, "#506A82")
        pulse(cluster[1], base=5, amp=2, speed=2.1)
        pulse(cluster[3], base=5, amp=2, speed=2.1)
        baby = mouse(point(2.84, -0.49), 0.76)
        self.at("offspring can inherit")
        self.play(FadeIn(baby, shift=RIGHT * 0.32), run_time=0.88)
        self.finish()


class S04Express(SpokenScene):
    def construct(self):
        embryo, arrow, adult = stage(marked=True, moving=True)
        self.add(embryo, scope_tag(color=TEXT))
        self.at("transgenic embryo grows")
        self.play(Create(arrow), FadeIn(adult, shift=RIGHT * 0.62), run_time=2.72)
        organ = Ellipse(width=1.53, height=1.00, stroke_width=2.5,
                        stroke_color=GREY, fill_color=INNER, fill_opacity=1).rotate(0.24).move_to(MOUSE + point(0.76, 0.28))
        extra = bottom_label("Extra / ectopic", 3.58, GOLD)
        self.at("one tests extra")
        self.play(FadeIn(organ), run_time=0.54)
        self.play(FadeIn(extra), run_time=0.48)
        self.at("turning a gene on")
        self.play(organ.animate.set_fill(GOLD, 0.89).set_stroke(GOLD, 3.5), run_time=1.75)
        cells = VGroup(*[
            Dot(MOUSE + point(x, y), color=GREEN, radius=0.125)
            for x, y in [(-1.2, 0.67), (-0.45, 0.54), (0.08, 0.12), (0.54, 0.88), (0.94, 0.32), (1.42, 0.71)]
        ])
        self.at("another builds a reporter")
        self.play(FadeOut(organ), FadeOut(extra), run_time=0.52)
        self.play(LaggedStart(*[GrowFromCenter(dot) for dot in cells], lag_ratio=0.17), run_time=1.37)
        self.at("giving specific cells")
        reporter_label = bottom_label("Reporter line", 3.58, GREEN)
        self.play(FadeIn(reporter_label), run_time=0.50)
        self.at("adding a gene")
        highlight = development_arrow(ORANGE)
        self.play(GrowArrow(highlight), FadeOut(reporter_label, rate_func=squish_rate_func(smooth, 0, 0.24)),
                  run_time=1.60)
        self.play(highlight.animate.set_stroke(width=7), run_time=1.78, rate_func=there_and_back)
        self.finish()


class S05Predict(SpokenScene):
    def construct(self):
        embryo, arrow, adult = stage(marked=True, moving=True)
        signal = grow_signal()
        turn = turn_arrow()
        self.add(embryo, arrow, adult, scope_tag(color=TEXT))
        self.at("suppose a reporter")
        self.play(LaggedStart(*[GrowFromCenter(dot) for dot in signal], lag_ratio=0.28), run_time=1.73)
        self.at("when calcium rises")
        self.play(signal.animate.scale(1.32), run_time=1.45, rate_func=there_and_back)
        self.at("the mouse turns left")
        self.play(Create(turn), run_time=0.94)
        self.play(signal.animate.scale(1.35), run_time=1.12, rate_func=there_and_back)
        self.at("does that glowing signal")
        self.play(FadeIn(question_card(QUESTION, **QUESTION_STYLE)), run_time=0.46)
        self.play(signal.animate.scale(1.35), run_time=2.75, rate_func=there_and_back)
        embryo[1].clear_updaters()
        adult[1].clear_updaters()
        self.play(embryo[1].animate.set_fill(INNER), adult[1].animate.set_fill(ANATOMY), run_time=0.78)
        self.finish()


class S06Pause(Scene):
    def construct(self):
        self.camera.background_color = BG
        self.add(predict_backdrop(), question_card(QUESTION, **QUESTION_STYLE))
        track = Line(point(-5.95, -3.07), point(4.53, -3.07), color=ANATOMY, stroke_width=10)
        progress = track.copy().set_color(GOLD)
        clock = ValueTracker(0)
        progress.add_updater(lambda line: line.pointwise_become_partial(track, 0, clock.get_value()))
        self.add(track, progress)
        self.play(clock.animate.set_value(1), run_time=4.5, rate_func=linear)


class S07WatchVsDrive(SpokenScene):
    def construct(self):
        backdrop = predict_backdrop()
        embryo, _, adult, signal, turn, _ = backdrop
        light_egg(embryo)
        light_mouse(adult)
        q = question_card(QUESTION, **QUESTION_STYLE)
        answer = question_card("No: watching is not causing.", **QUESTION_STYLE)
        self.add(backdrop, q)
        self.at("now")
        self.play(swap(q, answer, 0.70))
        meter = RoundedRectangle(width=2.50, height=1.58, corner_radius=0.20,
                                 color=GREEN, stroke_width=3, fill_color=ANATOMY, fill_opacity=1)
        meter.move_to(point(5.00, 2.01)).stretch_to_fit_height(1.10)
        scale = Arc(radius=0.47, start_angle=0.40, angle=2.34, color=GREEN, stroke_width=3)
        scale.move_arc_center_to(meter.get_center() + DOWN * 0.20)
        pointer = Line(scale.get_arc_center(), scale.point_from_proportion(0.88), color=TEXT, stroke_width=4)
        leader = Line(BRAIN + point(0.50, 0.17), meter.get_left(), color=GREEN, stroke_width=2)
        readout = VGroup(leader, meter, scale, pointer)
        self.at("a reporter is a voltmeter")
        self.play(FadeIn(readout), run_time=0.55)
        meter_label = bottom_label("Reporter = voltmeter", 2.87, GREEN)
        self.play(FadeIn(meter_label), run_time=0.45)
        self.at("watching neurons glow")
        self.play(Rotate(pointer, angle=-1.45, about_point=scale.get_arc_center()),
                  signal.animate.scale(1.21), run_time=2.0, rate_func=there_and_back)
        self.at("to test cause")
        self.play(FadeOut(readout), FadeOut(meter_label), FadeOut(answer), FadeOut(turn), run_time=0.65)
        beam = Polygon(point(-1.45, 1.36), point(-1.45, 2.10), BRAIN, stroke_color=BLUE,
                       stroke_width=2.5, fill_color=BLUE, fill_opacity=0.24)
        probe = Line(point(3.70, 2.58), BRAIN, color=BLUE, stroke_width=6)
        actuator = heading("Actuator", x=-1.53, y=2.59, color=BLUE)
        electrode = heading("Electrode", x=3.85, y=3.07, color=BLUE)
        self.at("light triggered actuator", lead=0.76)
        self.play(FadeIn(beam), FadeIn(actuator), run_time=0.40)
        self.play(signal.animate.scale(1.35), run_time=1.50, rate_func=there_and_back)
        self.at("or an electrode", lead=0)
        self.play(FadeOut(beam), FadeOut(actuator), run_time=0.24)
        self.play(Create(probe), FadeIn(electrode), run_time=0.52)
        self.play(signal.animate.scale(1.35), run_time=1.05, rate_func=there_and_back)
        self.at("then watch", lead=0.4)
        self.play(FadeOut(probe), FadeOut(electrode), Create(turn),
                  FadeIn(bottom_label("Turns left?", 2.87, GOLD)), run_time=0.50)
        self.finish()


class S08Guards(SpokenScene):
    def construct(self):
        embryo, arrow, adult = stage(marked=True, moving=True)
        self.add(embryo, arrow, adult, scope_tag(color=TEXT))
        compare = TwoPanel("Transgene: enough?", "Knockout: needed?", colors=(ORANGE, RED),
                           top=2.75, bottom=-2.65)
        left = compare.put(egg(ORIGIN, 1.86), "left")
        light_egg(left)
        right = compare.put(egg(ORIGIN, 1.86), "right")
        left_nucleus, right_nucleus = left[2][1], right[2][1]
        right[3].remove(right[3][1])
        added = ribbon(left_nucleus.get_center(), width=left_nucleus.width * 0.56)
        locus = right_nucleus.get_center()
        half_width = right_nucleus.width * 0.28
        damaged = VGroup(
            Line(locus + LEFT * half_width, locus + LEFT * half_width * 0.30, color=RED, stroke_width=9),
            Line(locus + RIGHT * half_width * 0.30, locus + RIGHT * half_width, color=RED, stroke_width=9),
        )
        self.at("two more limits")
        self.play(FadeOut(arrow), FadeOut(adult), ReplacementTransform(embryo, left),
                  FadeIn(compare.left_frame), run_time=1.45)
        self.at("adding a gene")
        self.play(FadeIn(compare.left_head), FadeIn(added), left[3][1].animate.set_opacity(0), run_time=0.67)
        self.play(FadeIn(compare.right_frame), FadeIn(right, shift=RIGHT * 0.22), run_time=1.13)
        self.at("for necessity")
        self.play(FadeIn(compare.right_head), run_time=0.48)
        light_egg(right)
        intact = ribbon(locus, GREY, width=half_width * 2)
        self.play(FadeIn(intact), run_time=0.40)
        self.at("disrupt the gene")
        self.play(ReplacementTransform(intact, damaged), run_time=0.85)
        self.at("also forcing an effect", lead=0.3)
        self.play(FadeOut(compare.left_frame), FadeOut(compare.right_frame),
                  FadeOut(compare.left_head), FadeOut(compare.right_head), FadeOut(damaged), run_time=0.33)
        lane_scale = 0.54
        lane_a_center, lane_b_center = point(-4.00, 1.29), point(-4.00, -1.29)
        version_a = VGroup(left, added)
        self.play(version_a.animate.scale(lane_scale, about_point=left.get_center()).move_to(lane_a_center),
                  right.animate.scale(lane_scale).move_to(lane_b_center), run_time=1.00)
        self.at("compare two versions", lead=0.4)
        lane_a = Arrow(point(-2.55, 1.29), point(0.50, 1.29), buff=0, color=ORANGE, stroke_width=4)
        lane_b = Arrow(point(-2.55, -1.29), point(0.50, -1.29), buff=0, color=PURPLE, stroke_width=4)
        label_a = heading("Version A", x=-1.04, y=1.81, color=ORANGE)
        label_b = heading("Version B", x=-1.04, y=-0.76, color=PURPLE)
        version_b_mark = ribbon(right_nucleus.get_center(), PURPLE, width=right_nucleus.width * 0.56 / lane_scale)
        self.play(FadeIn(version_b_mark.scale(lane_scale)), GrowArrow(lane_a), GrowArrow(lane_b),
                  FadeIn(label_a), FadeIn(label_b),
                  FadeIn(mouse(point(2.30, 1.13), 0.63), shift=RIGHT * 0.28),
                  FadeIn(mouse(point(2.30, -1.45), 0.63), shift=RIGHT * 0.28), run_time=0.84)
        self.finish()


class S09UnlockedSry(SpokenScene):
    def construct(self):
        embryo, arrow, adult = stage(moving=True)
        self.add(embryo, arrow, adult, scope_tag(color=TEXT))
        xx = VGroup(*[
            VGroup(Line(point(-0.20, 0.35), point(0.20, -0.35)),
                   Line(point(0.20, 0.35), point(-0.20, -0.35)))
            .set_stroke(TEXT, 7).move_to(EGG + point(x, -0.09))
            for x in [-0.46, 0.46]
        ])
        self.at("in 1991")
        dna = ribbon(RIBBON_HOME)
        self.play(FadeIn(dna, shift=DOWN * 0.35), run_time=1.25)
        self.at("containing sry")
        self.play(FadeIn(heading("Sry (1991)", x=-1.80, y=2.56, color=ORANGE)), run_time=0.44)
        self.at("female mouse embryos", lead=0.8)
        self.play(embryo[2:].animate.set_opacity(0), FadeIn(xx, scale=0.78),
                  FadeIn(bottom_label("XX embryo", EGG[0])), run_time=0.55)
        self.play(dna.animate.scale(0.58).move_to(EGG + UP * 0.77), run_time=1.62)
        self.at("even with no y")
        marked_arrow = development_arrow(ORANGE)
        self.play(GrowArrow(marked_arrow), run_time=1.68)
        primordium = Ellipse(width=0.81, height=0.48, color=GREY, stroke_width=3,
                             fill_color=INNER, fill_opacity=1).move_to(MOUSE + point(0.89, -0.49))
        self.at("that single gene")
        self.play(FadeIn(primordium), run_time=0.43)
        testes = VGroup(*[
            Ellipse(width=0.36, height=0.65, color=GOLD, stroke_width=3,
                    fill_color=GOLD, fill_opacity=0.75).rotate(angle).move_to(MOUSE + point(x, -0.47))
            for x, angle in [(0.65, 0.18), (1.12, -0.18)]
        ])
        self.at("develop testes", lead=0.8)
        self.play(ReplacementTransform(primordium, testes), FadeIn(bottom_label("Testes formed", 2.90, GOLD)),
                  run_time=0.56)
        self.finish()


class S10UnlockedBrain(SpokenScene):
    def construct(self):
        embryo, arrow, adult = stage(moving=True)
        dna = ribbon(RIBBON_HOME)
        self.add(embryo, arrow, adult, dna, scope_tag(color=TEXT))
        treatment = heading("β-catenin (2002)", x=-1.20, y=3.02, color=ORANGE)
        self.at("in 2002")
        self.play(dna.animate.shift(DOWN * 0.36), run_time=2.20)
        self.at("put stabilized beta")
        self.play(FadeIn(treatment), dna.animate.scale(0.52).move_to(EGG + point(0.49, 0.40)), run_time=1.38)
        center = point(3.54, -0.12)
        smooth_cortex = cortical_shape(center)
        cortex = cortical_shape(BRAIN).scale(0.31, about_point=BRAIN)
        self.at("neural progenitors")
        self.play(FadeIn(cortex), run_time=0.69)
        self.play(Transform(cortex, smooth_cortex), FadeOut(adult), run_time=2.01)
        parent_positions = [(-0.99, -0.18), (-0.58, 0.51), (0.34, 0.61), (0.72, -0.32)]
        parents = VGroup(*[Dot(center + point(x, y), radius=0.14, color=PURPLE) for x, y in parent_positions])
        self.at("stabilized means")
        self.play(LaggedStart(*[GrowFromCenter(dot) for dot in parents], lag_ratio=0.26), run_time=1.28)
        signal = Circle(radius=0.36, color=ORANGE, stroke_width=3).move_to(parents[0])
        self.at("so its signal")
        self.play(Create(signal), run_time=0.50)
        self.play(signal.animate.move_to(parents[1]), run_time=0.62)
        self.play(signal.animate.move_to(parents[2]), run_time=0.71)
        self.play(signal.animate.move_to(parents[3]), run_time=0.71)
        self.at("cells kept dividing")
        progeny = VGroup(*[
            Dot(parent.get_center() + point(dx, dy), radius=0.12, color=PURPLE)
            for parent in parents for dx, dy in [(-0.26, 0.19), (0.29, -0.18)]
        ])
        self.play(FadeOut(signal), LaggedStart(*[
            GrowFromPoint(dot, parents[i // 2].get_center()) for i, dot in enumerate(progeny)
        ], lag_ratio=0.13), run_time=1.46)
        self.at("the smooth cortex")
        folded = cortical_shape(center, folded=True).scale(1.15, about_point=center)
        self.play(Transform(cortex, folded), VGroup(parents, progeny).animate.scale(1.18, about_point=center),
                  run_time=2.42)
        self.at("did not live past birth")
        survival = bottom_label("Did not live past birth", 2.72, TEXT)
        self.play(FadeIn(survival), run_time=0.50)
        self.at("folding was unlike primates")
        caveat = bottom_label("Not primate folding", 2.72, GOLD)
        self.play(swap(survival, caveat, 0.70))
        self.at("extra divisions can enlarge")
        self.play(cortex.animate.scale(1.08, about_point=center),
                  VGroup(parents, progeny).animate.scale(1.08, about_point=center), run_time=2.75)
        self.finish()


class S11UnlockedMct1(SpokenScene):
    def construct(self):
        embryo, arrow, adult = stage(moving=True)
        dna = ribbon(RIBBON_HOME)
        self.add(embryo, arrow, adult, dna, scope_tag(color=TEXT))
        reporter = heading("MCT1 reporter (2012)", x=-0.98, y=3.08, color=GREEN)
        self.at("in 2012")
        self.play(dna.animate.shift(DOWN * 0.47), run_time=2.20)
        self.at("used reporter mice")
        self.play(FadeIn(reporter), dna.animate.scale(0.52).move_to(EGG + point(0.49, 0.40)), run_time=1.75)
        axon = Line(point(0.87, -0.20), point(6.10, -0.20), color=BLUE, stroke_width=11)
        soma = disc(0.36, ANATOMY, BLUE, 3).move_to(axon.get_start())
        wraps = VGroup(*[
            RoundedRectangle(width=0.72, height=1.02, corner_radius=0.19, stroke_width=3,
                             stroke_color=GREEN, fill_color="#354D43", fill_opacity=1).move_to(point(x, -0.20))
            for x in [1.77, 2.75, 3.73, 4.71, 5.69]
        ])
        glia = disc(0.36, "#354D43", GREEN, 3).move_to(point(3.73, 1.52))
        branches = VGroup(*[
            Line(glia.get_bottom(), wrap.get_top(), color=GREEN, stroke_width=2.5) for wrap in wraps
        ])
        inset = VGroup(axon, soma, branches, wraps, glia)
        self.at("the visible tag")
        self.play(FadeOut(adult), FadeIn(inset, scale=0.38, target_position=BRAIN),
                  Transform(arrow, development_arrow(end_x=0.15)), run_time=1.87)
        self.at("concentrated in oligodendrocytes")
        self.play(wraps.animate.set_fill(GREEN, 0.65), glia.animate.set_fill(GREEN, 0.85), run_time=1.53)
        cell_label = heading("Oligodendrocyte", x=3.71, y=2.55, color=GREEN, size=32)
        self.at("glia that wrap", lead=0.35)
        self.play(FadeIn(cell_label), run_time=0.47)
        axon_label = bottom_label("Axon", 3.72, BLUE)
        self.play(FadeIn(axon_label), run_time=0.42)
        self.at("they then lowered it")
        lowered = heading("MCT1 lowered", x=3.71, y=2.55, color=GREEN)
        self.play(swap(cell_label, lowered, 0.65), wraps.animate.set_fill("#354D43", 1),
                  glia.animate.set_fill("#354D43", 1), run_time=0.82)
        focus = Circle(radius=0.54, color=BLUE, stroke_width=3).move_to(soma)
        self.at("watched the neurons")
        self.play(Create(focus), run_time=0.70)
        self.at("labeling cells or driving")
        self.play(FadeOut(reporter), FadeOut(lowered), FadeOut(axon_label), FadeOut(focus),
                  FadeOut(inset, scale=0.38, target_position=BRAIN), FadeIn(adult),
                  Transform(arrow, development_arrow()), run_time=1.37)
        self.at("one added gene")
        link = development_arrow(ORANGE)
        self.play(GrowArrow(link), run_time=1.68)
        self.play(link.animate.set_stroke(width=7), run_time=1.54, rate_func=there_and_back)
        self.finish()


class S12End(EndCard):
    LINE = "A transgene tests what one added gene can do inside an animal."
