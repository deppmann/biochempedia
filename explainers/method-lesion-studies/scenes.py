"""Mapping Function From What Breaks.

COLOR MAP
  GREY / BLUE = nervous-system structure and intact fibre routes
  YELLOW = signals moving along fibres
  GREEN = preserved output
  RED = damage and impaired output
  GOLD = historical attribution, questions, and takeaway rules
"""
from bp_parts import *  # noqa: F403


BRAIN_X = -3.55
PANEL_X = 3.38
QUESTION = "Which side becomes weak?"


def point(x, y):
    return np.array([x, y, 0.0])


def brain_point(x, y):
    return point(BRAIN_X + x, y)


def spline(points, color, width, opacity=1, fill=0):
    curve = VMobject()
    curve.set_points_smoothly([brain_point(*p) for p in points])
    curve.set_stroke(color, width, opacity)
    curve.set_fill(color, fill)
    return curve


def lobe(points, color, opacity, width, hand):
    outline = VMobject()
    outline.set_points_smoothly([brain_point(hand * x, y) for x, y in points])
    outline.set_fill(color, opacity)
    outline.set_stroke(GREY, width=width, opacity=0.46 if width else 0)
    return outline


def nervous_system():
    cerebral_outline = [
        (0.10, 2.82), (0.46, 3.12), (1.24, 3.11), (1.92, 2.85),
        (2.40, 2.32), (2.56, 1.70), (2.48, 1.02), (2.12, 0.31),
        (1.66, -0.13), (1.06, -0.39), (0.53, -0.28), (0.16, 0.13),
        (0.11, 0.85), (0.10, 1.61), (0.12, 2.28), (0.10, 2.82),
    ]
    inner_lobe = [
        (0.30, 2.68), (0.78, 2.93), (1.54, 2.79), (2.16, 2.30),
        (2.33, 1.68), (2.13, 0.98), (1.72, 0.31), (1.04, -0.10),
        (0.55, 0.02), (0.32, 0.45), (0.30, 1.24), (0.35, 2.05), (0.30, 2.68),
    ]
    folds = [
        [(0.40, 2.45), (0.75, 2.56), (1.26, 2.48), (1.69, 2.63), (2.10, 2.39)],
        [(0.38, 1.91), (0.78, 2.09), (1.16, 1.94), (1.56, 2.12), (2.30, 1.92)],
        [(0.41, 1.29), (0.87, 1.49), (1.35, 1.34), (1.82, 1.60), (2.31, 1.37)],
        [(0.40, 0.68), (0.86, 0.91), (1.24, 0.76), (1.64, 0.97), (2.10, 0.79)],
        [(0.64, 0.24), (1.03, 0.37), (1.42, 0.27), (1.75, 0.45)],
    ]
    stem = spline([
        (-0.71, 0.19), (-0.69, -0.51), (-0.53, -1.01),
        (-0.52, -2.53), (-0.39, -2.72), (0.39, -2.72), (0.52, -2.53),
        (0.53, -1.01), (0.69, -0.51), (0.71, 0.19), (0.0, 0.37), (-0.71, 0.19),
    ], GREY, 3, 0.62, 0.58)
    brain = VGroup(stem)
    for side in (-1, 1):
        brain.add(lobe(cerebral_outline, BLUE, 0.25, 3.8, side))
        brain.add(lobe(inner_lobe, BLUE, 0.13, 0, side))
        for fold in folds:
            brain.add(spline([(side * x, y) for x, y in fold], BLUE, 3.2, 0.27))
    return brain


def schematic_tag():
    return scope_tag("Schematic", size=28, color=TEXT)


def midline():
    return DashedLine(brain_point(0, 3.28), brain_point(0, -2.83),
                      dash_length=0.15, dashed_ratio=0.55, color=TEXT,
                      stroke_width=2.4, stroke_opacity=0.65)


class Fibre(VGroup):
    """A fixed route with a moving signal train and a controllable interruption."""

    def __init__(self, points, speed=0.54, count=3, phase=0, stop=1, width=6):
        super().__init__()
        path = spline(points, BLUE, width)
        self.silent_route = path.copy().set_stroke(BLUE, width, 0.29)
        self.live_route = path.copy()
        self.stop = ValueTracker(stop)
        self.signals = VGroup(*[
            VGroup(path.copy(), path.copy(), path.copy(), Dot(radius=0.12, color=YELLOW))
            for _ in range(count)
        ])
        self.add(self.silent_route, self.live_route, self.signals)
        self.clock = phase

        def advance(mob, dt):
            self.clock += dt
            end = self.stop.get_value()
            self.live_route.pointwise_become_partial(path, 0, end)
            self.live_route.set_stroke(BLUE, width, 0.88)
            for i, (wash, halo, tail, head) in enumerate(self.signals):
                t = (self.clock * speed + (i + 0.5) / count) % 1
                end_tail = min(t, end)
                start = max(0, t - 0.19)
                visible = end_tail > start
                for segment, w, opacity in ((wash, 60, 0.25), (halo, 31, 0.55), (tail, 11, 0.98)):
                    segment.pointwise_become_partial(path, min(start, end_tail), end_tail)
                    segment.set_stroke(YELLOW, w, opacity if visible else 0)
                head.move_to(path.point_from_proportion(t)).set_opacity(1 if t < end else 0)

        self.add_updater(advance, call_updater=True)


SPEECH = [(-1.55, 2.73), (-1.36, 2.31), (-1.02, 1.78), (-0.73, 0.83), (-0.42, 0.27)]
UNDERSTANDING = [(1.79, 0.59), (1.43, 1.16), (1.06, 1.54), (0.89, 2.03), (0.47, 2.56)]
MOTOR = [(-1.45, 2.76), (-1.07, 2.04), (-0.62, 1.19), (-0.36, 0.27),
         (0.32, -0.62), (0.30, -1.36), (0.31, -2.51)]
DOUBLE = MOTOR[:5] + [(0.30, -1.18), (-0.29, -1.84), (-0.31, -2.51)]
STROKE_STOP = 0.13
NECK_STOP = 5 / 6
STROKE_AT = (-1.17, 2.20)
NECK_AT = (0.30, -1.36)


def lesion(x, y, radius=0.36, opacity=1):
    patch = spline(
        [(x + radius * a, y + radius * b) for a, b in [
            (-1, 0.12), (-0.73, 0.77), (-0.24, 1), (0.34, 0.73),
            (0.87, 0.64), (1, -0.07), (0.67, -0.67), (0.14, -1),
            (-0.56, -0.76), (-1, 0.12),
        ]], RED, 3.4, opacity, 0,
    )
    patch.set_fill(BG, 0.90 * opacity)
    return pulse(patch, base=3.4, amp=1.1, speed=3.4)


def cut(x, y, tilt=0):
    center = brain_point(x, y)
    gap = Line(center + LEFT * 0.25, center + RIGHT * 0.25,
               color=BG, stroke_width=23)
    mark = VGroup(
        Line(center + point(-0.25, -0.055), center + point(0.25, -0.055),
             color=RED, stroke_width=4.5),
        Line(center + point(-0.25, 0.055), center + point(0.25, 0.055),
             color=RED, stroke_width=4.5),
    )
    for edge in mark:
        pulse(edge, base=4.5, amp=1.4, speed=4)
    return VGroup(gap, mark).rotate(tilt, about_point=center)


def ringing_crossing(y, x=0):
    ring = Circle(radius=0.23, stroke_color=YELLOW, stroke_width=4).move_to(brain_point(x, y))
    return pulse(ring, base=4, amp=1.6, speed=4)


def heading(text, y=2.48, color=TEXT, size=39):
    return fit_text(text, max_w=5.66, size=size, min_size=28, max_lines=2,
                    color=color, weight=SEMIBOLD).move_to(point(PANEL_X, y))


def note(text, y=2.47, color=GOLD):
    return fit_text(text, max_w=5.66, size=31, min_size=28,
                    max_lines=2, color=color).move_to(point(PANEL_X, y))


def panel(top=1.96, bottom=-2.47):
    return RoundedRectangle(width=6.02, height=top - bottom, corner_radius=0.25,
                            stroke_color=GREY, stroke_width=2, stroke_opacity=0.53,
                            fill_color=BLUE, fill_opacity=0.075
                            ).move_to(point(PANEL_X, (top + bottom) / 2))


class Output(VGroup):
    """A named, qualitative output. The same level drives fill and travelling highlight."""

    def __init__(self, label, y, level=0.86, pending=False, color=None):
        super().__init__()
        self.level = ValueTracker(level)
        self.pending = ValueTracker(float(pending))
        self.clock = 0
        self.label = fit_text(label, max_w=5.05, size=34, min_size=28, max_lines=2,
                              weight=SEMIBOLD).move_to(point(PANEL_X, y + 0.34))
        rail_y = y - 0.39
        self.rail = RoundedRectangle(width=4.87, height=0.43, corner_radius=0.18,
                                     stroke_color=GREY, stroke_width=2,
                                     fill_color=BG, fill_opacity=0.65).move_to(point(PANEL_X, rail_y))
        self.fill = RoundedRectangle(width=4.64, height=0.24, corner_radius=0.1,
                                     stroke_width=0, fill_color=GREEN, fill_opacity=0.85)
        self.sweep = Line(ORIGIN, RIGHT, stroke_width=11, color=TEXT)
        self.add(self.rail, self.fill, self.sweep, self.label)

        def animate_meter(mob, dt):
            self.clock += dt
            strength = self.level.get_value()
            left = PANEL_X - 2.32
            end = left + 4.64 * strength
            self.fill.stretch_to_fit_width(4.64 * strength)
            self.fill.move_to(point((left + end) / 2, rail_y))
            result_color = ManimColor(color) if color else interpolate_color(
                ManimColor(RED), ManimColor(GREEN), min(1, strength * 1.55))
            pending = self.pending.get_value()
            self.fill.set_fill(interpolate_color(result_color, ManimColor(GREY), pending))
            x = left + (end - left) * ((self.clock * 0.78) % 1)
            self.sweep.put_start_and_end_on(point(max(left + 0.003, x - 1.16), rail_y),
                                           point(min(end - 0.003, x + 0.002), rail_y))
            self.sweep.set_stroke(opacity=0.74 * (1 - pending) if strength > 0.30 else 0)

        self.add_updater(animate_meter, call_updater=True)


def outputs(names, levels=(0.86, 0.86), second_color=None):
    first = Output(names[0], 0.93, levels[0])
    second = Output(names[1], -0.99, levels[1], color=second_color)
    return panel(), first, second


def opening():
    anatomy = nervous_system()
    speech = Fibre(SPEECH, speed=0.61, count=2)
    understanding = Fibre(UNDERSTANDING, speed=0.55, count=2, phase=0.5)
    return anatomy, speech, understanding


def motor_world(stop=1):
    return nervous_system(), midline(), Fibre(MOTOR, stop=stop)


def body_outputs(level=0.86, pending=False):
    return panel(), Output("Left body", 0.93, pending=pending), Output("Right body", -0.99, level, pending)


def neck_cut():
    return cut(*NECK_AT)


def predict_card():
    return question_card(QUESTION, y=-3.12, size=35)


class S01Hook(SpokenScene):
    def construct(self):
        anatomy, speech, understanding = opening()
        plate, speech_meter, understanding_meter = outputs(("Speech", "Understanding"))
        puzzle = heading("How do we know\nwhat a region does?", size=42)
        patient = heading("Patient Leborgne", y=2.55)
        gap = lesion(-1.51, 2.62)
        name = boxed_label("Left frontal lesion", color=RED, size=32).move_to(point(PANEL_X, 2.55))
        study = heading("Lesion study", y=2.55)
        self.add(anatomy, speech, understanding, schematic_tag())
        self.at("how do we know")
        self.play(FadeIn(puzzle), run_time=0.38)
        self.at("a patient named")
        self.play(swap(puzzle, patient), run_time=0.46)
        self.play(FadeIn(gap), speech.stop.animate.set_value(0.05), run_time=0.6)
        self.at("could hardly speak")
        speech_meter.level.set_value(0.12)
        self.play(FadeIn(plate), FadeIn(speech_meter), run_time=0.50)
        self.at("much of his understanding")
        self.play(FadeIn(understanding_meter), run_time=0.48)
        self.at("on the left frontal lobe")
        self.play(swap(patient, name), run_time=0.61)
        self.at("studying what fails")
        self.play(swap(name, study), run_time=0.64)
        self.finish()


class S02Title(TitleCard):
    LESSON = "Lesion Studies"
    TITLE = "Mapping Function From What Breaks"

    def construct(self):
        anatomy, speech, understanding = opening()
        anatomy.fade(0.22)
        title = T(self.TITLE.replace(" From ", "\nFrom "), 47, font=TITLE_FONT
                  ).move_to(point(PANEL_X, 0.1))
        lesson = T(self.LESSON.upper(), 28, GOLD, weight=SEMIBOLD).move_to(point(PANEL_X, 1.42))
        rule = Line(point(2.52, -1.03), point(4.24, -1.03), color=GOLD, stroke_width=3)
        speech.stop.set_value(0.05)
        self.add(anatomy, speech, understanding, lesion(-1.51, 2.62), lesson, title)
        self.play(GrowFromCenter(rule), run_time=0.6)
        self.wait(self.narration_s - self.elapsed() - 0.5 / config.frame_rate)


class S03TwoWays(SpokenScene):
    def construct(self):
        anatomy, route, spared = opening()
        patch = lesion(-1.51, 2.62)
        route.stop.set_value(0.05)
        patient = heading("Patient study")
        patient_detail = note("Stroke or operation", y=1.68, color=TEXT)
        animal = heading("Animal study")
        planned = note("Planned lesion", y=1.68, color=TEXT)
        tract_cut = cut(-0.96, 1.61, tilt=0.36)
        nucleus_at = brain_point(-1.69, 0.92)
        cluster = VGroup(*[
            Dot(nucleus_at + point(x, y), radius=0.068, color=YELLOW)
            for x, y in [(0, 0), (-0.14, 0.08), (0.10, 0.12), (-0.04, -0.15), (0.15, -0.08)]
        ])
        cut_label = heading("Tract cut", y=0.25)
        nucleus = heading("Nucleus", y=0.25)
        plate, fails, survives = outputs(("Fails", "Survives"))
        self.add(anatomy, route, spared, patch, schematic_tag())
        self.at("in patient studies")
        self.play(FadeIn(patient), run_time=0.47)
        self.at("a stroke or operation")
        self.play(FadeIn(patient_detail), run_time=0.47)
        self.at("in animal studies")
        self.play(swap(patient, animal), FadeOut(patient_detail), FadeOut(patch),
                  route.stop.animate.set_value(1), run_time=0.72)
        self.play(FadeIn(planned), run_time=0.35)
        self.at("researchers cut")
        self.play(FadeIn(tract_cut), route.stop.animate.set_value(0.43), FadeIn(cut_label), run_time=0.53)
        self.at("destroy a neuron cluster")
        self.play(FadeIn(cluster), run_time=0.43)
        self.at("a nucleus")
        self.play(swap(cut_label, nucleus), run_time=0.46)
        self.at("with electric current")
        self.play(Flash(nucleus_at, color=YELLOW, line_length=0.21, flash_radius=0.28),
                  cluster.animate.set_color(RED).set_opacity(0.25), run_time=0.62)
        self.at("either way")
        self.play(FadeOut(animal), FadeOut(planned), FadeOut(nucleus), FadeIn(plate), run_time=0.53)
        self.at("compare what fails")
        self.play(FadeIn(fails), fails.level.animate.set_value(0.14), run_time=0.55)
        self.at("what survives")
        self.play(FadeIn(survives), run_time=0.50)
        self.finish()


class S04Routes(SpokenScene):
    def construct(self):
        anatomy, axis, route = motor_world()
        two_crossings = Fibre(DOUBLE, stop=STROKE_STOP)
        marker = cut(*STROKE_AT, tilt=0.42)
        counter_value = ValueTracker(1)
        crossing_count = counter("{:.0f}", counter_value, at=point(PANEL_X, 0.51),
                                 size=64, color=YELLOW)
        signals_stop = heading("Signal stops at cut")
        count_title = heading("Midline crossings")
        count_plate = panel(top=1.71, bottom=-1.88).set_fill(BLUE, opacity=0.16)
        odd = heading("Opposite side", y=-0.85, color=TEXT)
        even = heading("Same side", y=-0.85, color=TEXT)
        crossing = ringing_crossing(-0.22)
        second_crossing = ringing_crossing(-1.48)
        # Blue traces the fibre's geometry after the lesion stops the yellow signals.
        guide = spline(MOTOR[2:], BLUE, 16, 0.76)
        second_guide = spline(DOUBLE[4:], BLUE, 12, 0.75)
        self.add(anatomy, route, schematic_tag())
        self.at("a lesion removes signals")
        self.play(FadeIn(marker), route.stop.animate.set_value(STROKE_STOP),
                  FadeIn(signals_stop), run_time=0.67)
        self.at("count how many")
        self.play(Create(axis), swap(signals_stop, count_title), run_time=0.60)
        self.play(ShowPassingFlash(guide, time_width=0.60), run_time=2.00, rate_func=linear)
        self.at("each crossing flips")
        self.play(FadeIn(crossing), FadeIn(count_plate), FadeIn(crossing_count), run_time=0.56)
        self.at("an odd count")
        self.play(FadeIn(odd), run_time=0.50)
        self.at("an even count")
        self.play(FadeOut(route), FadeIn(two_crossings), FadeIn(second_crossing),
                  counter_value.animate.set_value(2), swap(odd, even), run_time=0.82)
        self.play(ShowPassingFlash(second_guide, time_width=0.56), run_time=1.30, rate_func=linear)
        self.finish()


class S05PredictQ(SpokenScene):
    def construct(self):
        anatomy, axis, route = motor_world()
        plate, left, right = body_outputs()
        stroke = lesion(*STROKE_AT, radius=0.38)
        neck = neck_cut()
        crossing = ringing_crossing(-0.22)
        case = heading("Left hemisphere stroke", y=2.56)
        total = heading("1 crossing ahead", y=2.56, color=YELLOW)
        result = note("Left stroke → right weakness")
        self.add(anatomy, axis, route, plate, left, right, schematic_tag())
        self.at("a stroke deep")
        self.play(FadeIn(stroke), route.stop.animate.set_value(STROKE_STOP), run_time=0.70)
        self.at("left hemisphere lies")
        self.play(FadeIn(case), run_time=0.58)
        self.at("above one midline crossing")
        self.play(FadeIn(crossing), run_time=0.48)
        self.play(swap(case, total), run_time=0.68)
        self.at("so it weakens")
        self.play(right.level.animate.set_value(0.15), run_time=0.60)
        self.at("the right face")
        self.play(swap(total, result), run_time=0.60)
        self.at("now cut the right half")
        self.play(FadeOut(stroke), FadeOut(result), FadeOut(crossing),
                  right.level.animate.set_value(0.86), route.stop.animate.set_value(1),
                  left.pending.animate.set_value(1), right.pending.animate.set_value(1), run_time=0.52)
        self.play(FadeIn(neck), route.stop.animate.set_value(NECK_STOP), run_time=0.51)
        self.at("which side becomes weak")
        self.play(FadeIn(predict_card()), run_time=0.45)
        self.finish()


class S06PredictPause(PredictPause):
    QUESTION = QUESTION
    CARD = {"y": -3.12, "size": 35}

    def construct(self):
        anatomy, axis, route = motor_world(stop=NECK_STOP)
        plate, left, right = body_outputs(pending=True)
        self.add(anatomy, axis, route, neck_cut(), plate, left, right,
                 schematic_tag(), predict_card())
        self.wait(self.narration_s)


class S07PredictAnswer(SpokenScene):
    def construct(self):
        anatomy, axis, route = motor_world(stop=NECK_STOP)
        plate, left, right = body_outputs(pending=True)
        neck = neck_cut()
        q = predict_card()
        answer = heading("Right arm and leg", color=RED)
        crossed = ringing_crossing(-0.22)
        count = note("0 crossings below cut", color=YELLOW)
        result = note("No crossings → right side")
        sites = heading("Two lesion sites", y=2.52)
        same_chain = heading("One shared pathway", y=2.52)
        stroke = lesion(*STROKE_AT, radius=0.38, opacity=0.76)
        motor_path = spline(MOTOR, BLUE, 13)
        shared_path = motor_path.copy().pointwise_become_partial(motor_path, STROKE_STOP, NECK_STOP)
        rule = caption("Needed in a chain, not alone.", size=37, color=GOLD)
        self.add(anatomy, axis, route, neck, plate, left, right, schematic_tag(), q)
        self.at("the right arm and leg")
        self.play(FadeOut(q), FadeIn(answer), right.level.animate.set_value(0.13),
                  left.pending.animate.set_value(0), right.pending.animate.set_value(0), run_time=0.57)
        self.at("already crossed above")
        self.play(FadeIn(crossed), run_time=0.48)
        self.at("zero crossings remain")
        self.play(swap(answer, count), run_time=0.64)
        self.at("the same side")
        self.play(swap(count, result), run_time=0.65)
        self.at("lesions on opposite sides")
        self.play(Succession(route.stop.animate(run_time=0.20).set_value(STROKE_STOP),
                             FadeIn(stroke, run_time=0.48)),
                  swap(result, sites), run_time=0.68)
        self.at("both break one chain")
        self.play(FadeOut(crossed), swap(sites, same_chain),
                  ShowPassingFlash(shared_path, time_width=0.64), run_time=0.92)
        self.at("a needed link")
        self.play(FadeOut(same_chain), FadeIn(rule), run_time=0.62)
        self.finish()


class S08Limits(SpokenScene):
    def construct(self):
        anatomy, axis, motor = motor_world(stop=STROKE_STOP)
        prior_stroke = lesion(*STROKE_AT, radius=0.38, opacity=0.76)
        prior_neck = neck_cut()
        rule = caption("Needed in a chain, not alone.", size=37, color=GOLD)
        plate, left, right = body_outputs(0.13)
        area = Dot(brain_point(-0.86, 1.22), radius=0.53, color=BLUE, fill_opacity=0.49)
        strands = [
            Fibre([(-2.37, y + 0.51), (-1.65, y), (-0.86, y), (0.24, y + 0.22), (2.15, dest)],
                  count=2, phase=phase)
            for y, dest, phase in [(1.40, 2.09, 0), (1.06, 0.57, 0.4)]
        ]
        region = (-0.86, 1.22)
        cut_area = lesion(*region, radius=0.52)
        heading_fibres = heading("Passing fibres cut")
        heading_relay = heading("Possible relay")
        heading_stretches = heading("Several stretches broken")
        heading_pattern = heading("Same deficit")
        relay_in = Fibre([(-2.40, 1.86), (-1.62, 1.53), region], count=2, stop=0.70)
        relay_out = Fibre([region, (0.21, 0.84), (2.15, 0.57)], count=2, stop=0)
        relay_node = Circle(radius=0.20, color=BLUE, stroke_width=4,
                            fill_color=BG, fill_opacity=1).move_to(brain_point(*region))
        third = Fibre([(-2.05, 0.54), (-1.46, 0.91), (-0.89, 0.99), (0.23, 1.02), (2.08, 1.38)],
                      count=2, stop=0.13, phase=0.4)
        wide_damage = lesion(-0.89, 1.22, radius=0.83).set_z_index(2)
        first_site = lesion(-1.75, 1.51, radius=0.30).set_z_index(2)
        second_site = lesion(0.31, 1.46, radius=0.35).set_z_index(2)
        output_plate = panel(top=1.98, bottom=0.25)
        outcome = Output("Affected skill", 1.30, 0.14)
        checks = VGroup(*[
            T("✓  " + words, 34, GREEN, weight=SEMIBOLD)
            for words in ("Spared skills", "Multiple patients", "Other tests")
        ]).arrange(DOWN, aligned_edge=LEFT, buff=0.26).move_to(point(PANEL_X, -1.16))
        self.add(anatomy, axis, motor, prior_stroke, prior_neck, rule,
                 plate, left, right, schematic_tag())
        self.at("lesions can mislead")
        self.play(FadeOut(axis), FadeOut(motor), FadeOut(prior_stroke), FadeOut(prior_neck),
                  FadeOut(rule), FadeOut(plate), FadeOut(left), FadeOut(right),
                  anatomy.animate.scale(1.08, about_point=brain_point(-0.1, 0.50)),
                  run_time=0.73)
        self.play(FadeIn(area), *(FadeIn(s) for s in strands), run_time=0.52)
        self.at("also cuts fibers")
        self.play(FadeIn(cut_area), *(s.stop.animate.set_value(0.37) for s in strands), run_time=0.53)
        self.at("passing through it")
        self.play(FadeIn(heading_fibres), run_time=0.49)
        self.at("and the region")
        self.play(*(FadeOut(s) for s in strands), FadeIn(relay_in), FadeIn(relay_out),
                  FadeIn(relay_node),
                  swap(heading_fibres, heading_relay), run_time=0.67)
        self.at("real strokes")
        for strand in strands:
            strand.stop.set_value(0.17)
            strand.update(0)
        self.play(FadeOut(area), FadeOut(cut_area), FadeOut(relay_in), FadeOut(relay_out),
                  FadeOut(relay_node), FadeIn(wide_damage),
                  *(FadeIn(s) for s in strands), FadeIn(third),
                  swap(heading_relay, heading_stretches), run_time=0.76)
        self.at("different lesions")
        self.play(FadeOut(wide_damage), FadeOut(third), FadeOut(heading_stretches), run_time=0.26)
        # Change the stops between lesion markers so each visible cut matches its routes.
        strands[0].stop.set_value(0.09)
        strands[1].stop.set_value(1)
        self.play(FadeIn(first_site), FadeIn(heading_pattern),
                  FadeIn(output_plate), FadeIn(outcome), run_time=0.36)
        self.at("give one pattern")
        self.play(FadeOut(first_site), run_time=0.25)
        strands[0].stop.set_value(0.55)
        strands[1].stop.set_value(0.55)
        self.play(FadeIn(second_site), run_time=0.40)
        self.at("testing spared skills")
        self.play(FadeIn(checks[0]), run_time=0.46)
        self.at("comparing patients")
        self.play(FadeIn(checks[1]), run_time=0.46)
        self.at("adding other tests")
        self.play(FadeIn(checks[2]), run_time=0.46)
        self.finish()


def memory_world():
    declarative = Fibre([(-2.04, 2.46), (-1.59, 2.05), (-0.93, 1.45),
                         (-0.64, 0.99), (-0.84, 0.45)], count=2, phase=0.4)
    practice = Fibre([(1.99, 2.25), (1.57, 1.87), (1.08, 1.38),
                      (0.88, 0.85), (1.14, 0.27)], count=2, speed=0.63)
    return nervous_system(), declarative, practice


class S09UnlockedHm(SpokenScene):
    def construct(self):
        anatomy, declaring, drawing = memory_world()
        reference = note("Scoville and Milner, 1957")
        hm = heading("Patient H.M.", y=1.42)
        memory_split = heading("Memory is several abilities", y=2.63, color=GOLD, size=35)
        patch = lesion(-1.01, 1.51, radius=0.44)
        plate, declarative, practice = outputs(
            ("New declarative memories", "Drawing practice"), (0.86, 0.35), second_color=GREEN)
        self.add(anatomy, declaring, drawing, schematic_tag())
        self.at("in 1957")
        self.play(FadeIn(reference), run_time=0.51)
        self.at("described patient")
        self.play(FadeIn(hm), run_time=0.72)
        self.at("after his operation")
        self.play(FadeIn(patch), declaring.stop.animate.set_value(0.48), run_time=0.70)
        self.at("could almost never form")
        self.play(FadeOut(hm), run_time=0.42)
        self.at("new declarative memories")
        self.play(FadeIn(plate), FadeIn(declarative),
                  declarative.level.animate.set_value(0.08), run_time=0.72)
        self.at("practice improved his drawing")
        self.play(FadeIn(practice), run_time=0.55)
        self.at("another system kept")
        self.play(practice.level.animate.set_value(0.88), run_time=2.1, rate_func=smooth)
        self.at("memory is several abilities")
        self.play(swap(reference, memory_split), run_time=0.66)
        self.finish()


def clock_world():
    optic_nerves = VGroup(
        Fibre([(-1.53, 0.70), (-0.88, 0.41), (0.0, 0.23), (0.74, 0.47)],
              speed=0.55, count=1, phase=0.3, width=5),
        Fibre([(1.53, 0.70), (0.88, 0.41), (0.0, 0.23), (-0.74, 0.47)],
              speed=0.55, count=1, phase=0.8, width=5),
    )
    nuclei = VGroup(*[
        Dot(brain_point(x, 0.72), radius=0.15, color=YELLOW) for x in (-0.29, 0.29)
    ])
    return nervous_system(), optic_nerves, nuclei


class S10UnlockedScn(SpokenScene):
    def construct(self):
        anatomy, optic, nuclei = clock_world()
        label = heading("Suprachiasmatic nucleus", y=1.42, size=34)
        reference = note("Stephan and Zucker, 1972", y=2.57)
        # Unitless schematic daily phase and timing, with regular peaks one day apart.
        # The post-lesion ticks convey irregular timing and do not encode observations.
        chart = Plot(box=(0.83, 5.95, -0.32, 1.58), xr=(0, 3), yr=(0, 1),
                     xticks=[0, 1, 2, 3], xlabel="Days", size=28, label_size=28, color=GREY)
        daily = lambda t: (0.5 + 0.5 * np.cos(TAU * (t - 0.5))) ** 3 * 0.78 + 0.10
        waveform = chart.curve(daily, color=GREEN, width=6)
        drinks = (0.17, 0.38, 0.91, 1.72, 1.94, 2.06, 2.75, 2.83)
        ticks = VGroup(*[
            Line(chart.pt(x, 0.14), chart.pt(x, 0.43), color=GREEN, stroke_width=5)
            for x in drinks
        ])
        day_head = heading("Daily rhythm before lesion", y=1.99, size=31)
        irregular_head = heading("Irregular timing", y=1.96, size=34)
        drinking = Output("Drinking continues", -2.00, 0.77)
        rationale = caption("Needed for timing, not proof it keeps time.", size=30, color=GOLD)
        self.add(anatomy, optic, nuclei, schematic_tag())
        self.at("nucleus sits just above")
        self.play(FadeIn(label), run_time=0.53)
        self.at("in 1972")
        self.play(FadeIn(reference), run_time=0.59)
        self.play(FadeOut(label), run_time=0.36)
        self.play(Create(chart), run_time=0.72)
        self.play(Create(waveform), FadeIn(day_head), run_time=1.02)
        self.at("destroyed it on both sides")
        self.play(nuclei.animate.set_color(RED).set_opacity(0.38), run_time=0.57)
        bilat_left = T("SCN, both sides", 30, TEXT).move_to(point(BRAIN_X, -3.28))
        self.play(FadeIn(bilat_left), run_time=0.42)
        self.at("the rats still drank")
        self.play(FadeIn(drinking), run_time=0.54)
        self.at("no longer on a daily schedule")
        self.play(FadeOut(waveform), FadeOut(bilat_left), swap(day_head, irregular_head),
                  LaggedStart(*(GrowFromCenter(t) for t in ticks), lag_ratio=0.14), run_time=1.05)
        self.at("needed for timing")
        self.play(FadeIn(rationale), run_time=0.64)
        self.finish()


def touch_world():
    fast = Fibre([(-2.99, -2.50), (-2.41, -1.87), (-1.52, -1.29),
                  (-0.50, -0.74), (-0.70, 0.16), (-1.42, 1.17), (-1.88, 2.17)],
                 speed=0.84, count=3, width=11)
    slow = Fibre([(-2.67, -2.64), (-2.11, -2.00), (-1.22, -1.43),
                  (-0.31, -0.85), (-0.39, 0.17), (-1.16, 1.09), (-1.62, 2.29)],
                 speed=0.39, count=2, width=4.2, stop=0.04)
    skin = spline([(-3.03, -2.23), (-2.74, -2.33), (-2.51, -2.56),
                   (-2.44, -2.80), (-2.61, -2.98), (-3.02, -2.75), (-3.03, -2.23)],
                  GREY, 3.6, 0.85, 0.45)
    hairs = VGroup(*[
        spline([(x, y), (x - 0.18, y + 0.12), (x - 0.31, y + 0.12)], GREY, 2.7)
        for x, y in [(-2.99, -2.52), (-2.82, -2.65), (-2.64, -2.78)]
    ])
    return nervous_system(), fast, slow, VGroup(skin, hairs)


class S11UnlockedCt(SpokenScene):
    def construct(self):
        anatomy, fast, slow, skin = touch_world()
        reference = note("Olausson and colleagues, 2002")
        absent = heading("Large fibres absent", y=1.37)
        slow_label = heading("Slow C-tactile fibres", y=1.37)
        plate = panel(top=0.72, bottom=-1.14)
        sensation = Output("Faint pleasant sensation", 0, 0.28, color=GREEN)
        final_rule = caption("Compare what broke with what survived.", size=33, color=GOLD)
        branches = [
            Fibre([(-1.62, 2.28), (-0.62, 2.52), (0.46, 2.00), (1.82, 1.69)], count=2, phase=0.34),
            Fibre([(-1.46, 1.78), (-0.61, 0.87), (0.42, 0.72), (1.41, 0.26)], count=2, phase=0.86),
        ]
        self.add(anatomy, fast, slow, skin, schematic_tag())
        self.at("in 2002")
        self.play(FadeIn(reference), run_time=0.58)
        self.at("without the large")
        self.play(FadeOut(fast), run_time=0.62)
        self.at("fast touch fibers")
        self.play(FadeIn(absent), run_time=0.54)
        self.at("stimulating slow")
        self.play(FadeOut(absent),
                  Flash(brain_point(-2.67, -2.58), color=YELLOW, line_length=0.20, flash_radius=0.21),
                  slow.stop.animate.set_value(1), run_time=0.88)
        self.at("c tactile fibers")
        self.play(FadeIn(slow_label), run_time=0.56)
        self.at("still gave a faint")
        self.play(FadeIn(plate), FadeIn(sensation), run_time=0.61)
        self.at("what those fibers can do")
        self.play(FadeOut(reference), anatomy.animate.scale(0.94, about_point=brain_point(0, 0.42)),
                  run_time=1.05)
        self.at("each case compares")
        self.play(FadeOut(slow_label), FadeOut(plate), FadeOut(sensation),
                  *(FadeIn(route) for route in branches), FadeIn(final_rule), run_time=0.66)
        self.finish()


class S12End(EndCard):
    LINE = "Lesions show a region is needed, not that it works alone."
