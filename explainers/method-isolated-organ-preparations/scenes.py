"""Isolated organ and muscle preparations, timed to the supplied Kokoro narration."""

from bp_parts import *
from bp_style import EndCard

# Patch-clamp palette: BLUE glass, TEAL bath, GREY tissue, PURPLE lining,
# ORANGE added solution, YELLOW recorded signal, GREEN successful response
# and its messenger, RED inhibition or caveat, GOLD historical dates.
PURPLE = "#B58CD9"
ORANGE = "#F29E4C"
WATER = "#1A4350"
WALL = "#565E70"
LX, RX, CY = -3.22, 3.22, -0.40
QUESTION = "Does the ring still relax?"


def p(x, y):
    return np.array([x, y, 0.0])


def label(text, x, y, color=TEXT, size=32):
    return T(text, size, color).move_to(p(x, y))


def line(a, b, color, width=4):
    return Line(p(*a), p(*b), color=color, stroke_width=width)


def arrow(a, b, color, width=4):
    return Arrow(p(*a), p(*b), buff=0, color=color, stroke_width=width, tip_length=0.18)


def bubbles(x, half, surface, bottom, moving=True):
    group = VGroup()
    for side in (-1, 1):
        for i in range(5):
            phase = (i / 5 + (0.09 if side == 1 else 0)) % 1
            center = x + side * (half - 0.35 - (i % 2) * 0.20)
            bead = Circle(radius=0.052 + (i % 3) * 0.023, stroke_width=2,
                          stroke_color=TEAL).set_stroke(opacity=0.88)
            height = surface - bottom - 0.28

            def rise(mob, dt, center=center, height=height):
                mob.phase = (mob.phase + 0.19 * dt) % 1
                mob.move_to(p(center + 0.075 * np.sin(TAU * mob.phase),
                              bottom + 0.14 + height * mob.phase))
                mob.set_stroke(opacity=0.86 * min(1, mob.phase * 12, (1 - mob.phase) * 12))

            bead.phase = phase
            rise(bead, 0)
            if moving:
                bead.add_updater(rise)
            group.add(bead)
    return group


def currents(x, half, surface, bottom, moving):
    """Broad, slow trails of aerated bath fluid behind the mounted tissue."""
    ribbons = VGroup()
    xs = np.linspace(x - half + 0.13, x + half - 0.13, 26)
    height = 0.72
    for index in range(3):
        ribbon = VMobject(stroke_width=0, fill_color=BLUE)
        ribbon.phase = (index + 0.4) / 3

        def rise(mob, dt, index=index):
            mob.phase = (mob.phase + 0.26 * dt) % 1
            y = bottom + 0.47 + (surface - bottom - 0.94) * mob.phase
            offsets = 0.10 * np.sin(xs * 1.8 + mob.phase * TAU + index)
            top_edge = [p(xx, y + dy + height / 2) for xx, dy in zip(xs, offsets)]
            bottom_edge = [p(xx, y + dy - height / 2) for xx, dy in zip(xs, offsets)]
            mob.set_points_as_corners([*top_edge, *reversed(bottom_edge), top_edge[0]])
            mob.set_fill(opacity=0.23 * min(1, mob.phase * 8, (1 - mob.phase) * 8))

        rise(ribbon, 0)
        if moving:
            ribbon.add_updater(rise)
        ribbons.add(ribbon)
    return ribbons


def glass_bath(x=LX, width=5.86, moving=True, lit=False):
    """The same rim, water level and floor in every apparatus shot."""
    half, top, surface, base = width / 2, 2.12, 1.30, -2.58
    left, right = x - half, x + half
    water = Rectangle(width=width - 0.11, height=surface - base - 0.05,
                      fill_color="#235363" if lit else WATER, fill_opacity=1,
                      stroke_width=0).move_to(p(x, (surface + base + 0.05) / 2))
    walls = VMobject(stroke_color=BLUE, stroke_width=4).set_points_as_corners([
        p(left, top), p(left, base + 0.15), p(left + 0.17, base),
        p(right - 0.17, base), p(right, base + 0.15), p(right, top)])
    rim = VGroup(line((left - 0.09, top), (left + 0.33, top), BLUE),
                 line((right - 0.33, top), (right + 0.09, top), BLUE))
    wave = line((left + 0.04, surface), (right - 0.04, surface), TEAL, 3)
    return VGroup(water, currents(x, half, surface, base, moving), wave,
                  bubbles(x, half, surface, base, moving), walls, rim)


def vessel_ring(x=LX, y=CY, relaxed=0, intact=True, scale=1):
    """En-face tissue section. The wall thins as the lumen opens."""
    inner = 0.72 + 0.35 * relaxed
    outer = 1.46 + 0.11 * relaxed
    wall = Annulus(inner_radius=inner + 0.085, outer_radius=outer,
                   color=WALL, fill_opacity=1, stroke_width=0)
    edges = VGroup(Circle(radius=outer, color=GREY, stroke_width=3),
                   Circle(radius=inner + 0.085, color=GREY, stroke_width=2))
    lining = Annulus(inner_radius=inner, outer_radius=inner + 0.085,
                     color=PURPLE, fill_opacity=1, stroke_width=0)
    ring = VGroup(wall, edges, lining if intact else VGroup())
    ring.stretch(1.13, 0).scale(scale, about_point=ORIGIN).shift(p(x, y))
    ring.lining = ring[2]
    return ring


def supports(x=LX, y=CY, scale=1):
    """Two opposing hooks keep their attachment points as the lumen widens."""
    rods = VGroup(line((x, 2.12), (x, y + 1.43 * scale), BLUE, 3),
                  line((x, -2.58), (x, y - 1.43 * scale), BLUE, 3))
    for direction in (-1, 1):
        rods.add(Arc(radius=0.12, start_angle=0 if direction == -1 else PI,
                     angle=PI, color=BLUE, stroke_width=3).move_to(
                         p(x + direction * 0.105, y + direction * 1.42 * scale)))
    return rods


def mounted_ring(x=LX, relaxed=0, intact=True):
    return VGroup(vessel_ring(x=x, relaxed=relaxed, intact=intact), supports(x))


def pipette(x, y, angle=0, color=ORANGE, length=0.97, spread=0.64):
    glass = Polygon(p(-0.08, 0), p(-spread / 2, length), p(spread / 2, length),
                    p(0.08, 0), stroke_width=2.6, stroke_color=BLUE,
                    fill_color=color, fill_opacity=0.38)
    return glass.rotate(angle, about_point=ORIGIN).shift(p(x, y))


def dropper(x=LX):
    return pipette(x + 1.12, 1.37, angle=-0.25)


def tracer_dots(starts, ends, color, duration=1.8, radius=0.073, moving=True):
    """A packet of schematic tracer marks, each with a reproducible resting position."""
    dots = VGroup()
    for i, (start, end) in enumerate(zip(starts, ends, strict=True)):
        bead = Dot(p(*start), radius=radius, color=color)
        bead.age = 0.0

        def drift(mob, dt, start=start, end=end, lag=i * 0.13):
            mob.age += dt
            a = np.clip((mob.age - lag) / duration, 0, 1)
            mob.move_to(interpolate(p(*start), p(*end), a))
            mob.set_opacity(min(1, max(0, (mob.age - lag) * 8)))

        if moving:
            drift(bead, 0)
            bead.add_updater(drift)
        else:
            bead.move_to(p(*end))
        dots.add(bead)
    return dots


def dose(x=LX, moving=True):
    starts = [(x + 1.12, 1.32)] * 6
    ends = [(x + 1.10, 0.67), (x + 0.79, 0.35), (x + 0.44, 0.13),
            (x + 0.19, -0.02), (x + 0.37, -0.31), (x + 0.66, -0.45)]
    return tracer_dots(starts, ends, ORANGE, moving=moving)


def messenger(x=LX):
    angles = np.linspace(-0.37, 0.73, 7)
    starts = [(x + 0.90 * np.cos(a), CY + 0.79 * np.sin(a)) for a in angles]
    ends = [(x + 1.60 * np.cos(a), CY + 1.40 * np.sin(a)) for a in angles]
    return tracer_dots(starts, ends, GREEN, duration=2.9, radius=0.062)


def chart(title="Ring tension"):
    return Plot(box=(0.68, 6.30, -2.21, 1.77), xr=(0, 1), yr=(0, 1),
                xlabel="Time", ylabel=title, color=GREY, label_size=30)


def tension(time, start=0.40, transition=0.25):
    """Schematic state interpolation: baseline followed by relaxation, with no numeric axes."""
    relaxed = np.clip((time - start) / transition, 0, 1)
    return 0.75 - 0.52 * smooth(relaxed)


def trace(scene, plot, end, fn, duration, start=0):
    pen = ValueTracker(max(0.003, start))
    curve = plot.live_curve(fn, pen, color=YELLOW, x0=start)
    dot = plot.dot(pen.get_value, lambda: fn(pen.get_value()), color=YELLOW, ring=YELLOW,
                   radius=0.085)
    scene.add(curve, dot)
    scene.play(pen.animate.set_value(end), run_time=duration, rate_func=linear)
    return curve, dot


def tag():
    return scope_tag(size=28, color=TEXT)


def comparison(relaxed=0, treated=False):
    panel = TwoPanel("Intact ring", "Rubbed ring", colors=(PURPLE, GREY), top=3.05,
                     bottom=-2.87, width=12.88, size=31)
    panel.left_head.shift(UP * 0.14)
    panel.right_head.shift(UP * 0.14)
    left, right = mounted_ring(LX, relaxed), mounted_ring(RX, intact=False)
    tanks = VGroup(glass_bath(LX, 5.36), glass_bath(RX, 5.36))
    result = VGroup(panel, tanks, left, right, dropper(LX), dropper(RX))
    if treated:
        result.add(dose(LX, moving=False), dose(RX, moving=False))
    return result, left, right


def silhouette():
    outline = [
        (-0.64, 2.24), (-0.78, 1.85), (-1.86, 1.51), (-2.54, 0.78),
        (-3.04, -1.84), (-2.29, -2.33), (-1.55, -0.63), (-1.40, -2.99),
        (1.40, -2.99), (1.55, -0.63), (2.29, -2.33), (3.04, -1.84),
        (2.54, 0.78), (1.86, 1.51), (0.78, 1.85), (0.64, 2.24),
    ]
    torso = VMobject(fill_color="#303A4C", fill_opacity=1, stroke_color=GREY,
                     stroke_width=3)
    torso.set_points_as_corners([p(*xy) for xy in outline] + [p(*outline[0])])
    head = Ellipse(width=1.46, height=1.56, fill_color="#303A4C", fill_opacity=1,
                   stroke_color=GREY, stroke_width=3).move_to(p(0, 2.43))
    return VGroup(torso, head)


def body_vessel(width):
    outer = RoundedRectangle(width=width, height=3.94, corner_radius=0.30,
                             stroke_color=GREY, stroke_width=3,
                             fill_color=WALL, fill_opacity=1).move_to(p(0, -0.48))
    lumen = RoundedRectangle(width=width - 0.45, height=3.76, corner_radius=0.22,
                             stroke_width=0, fill_color="#262B3A",
                             fill_opacity=1).move_to(outer)
    return VGroup(outer, lumen)


class S01Hook(SpokenScene):
    def construct(self):
        body = silhouette()
        vessel = body_vessel(1.23)
        self.add(body, vessel, tag())
        self.at("When a blood vessel")
        self.play(Transform(vessel, body_vessel(1.79)), run_time=2.35)
        self.at("what made it relax")
        question = label("?", 1.48, -0.04, GOLD, 66)
        self.play(FadeIn(question), run_time=0.48)
        inputs = VGroup()
        for cue, text, x, y, target in [
            ("Nerves hormones", "Nerves", -4.79, 1.30, 0.70),
            ("hormones wall", "Hormones", 4.68, 1.29, 0.59),
            ("wall stretch", "Wall stretch", -4.74, -1.29, -0.89),
            ("local chemicals", "Local chemicals", 4.68, -1.32, -0.95),
        ]:
            self.at(cue)
            name = label(text, x, y, TEXT, 30)
            inward = RIGHT if x < 0 else LEFT
            start = name.get_critical_point(inward) + 0.2 * inward
            path = arrow(start[:2], (-0.94 if x < 0 else 0.94, target), BLUE)
            inputs.add(path, name)
            self.play(GrowArrow(path), FadeIn(name), run_time=0.43)
            pulse(path, base=4.5, amp=2.2, speed=4)
        self.at("all pull on it")
        self.play(Transform(vessel, body_vessel(2.06)), run_time=1.7)
        self.at("To test one signal")
        self.play(FadeOut(inputs), FadeOut(question), run_time=0.65)
        self.at("take a living piece")
        ring = vessel_ring(x=0, y=-0.48, scale=0.61)
        ring.set_z_index(2)
        self.play(FadeIn(ring), vessel.animate.set_opacity(0.36), run_time=0.52)
        self.play(ring.animate.shift(p(LX, 0.49)).scale(1 / 0.61), run_time=2.15)
        self.finish()


class S02Title(TitleCard):
    TITLE = "Testing an Organ Outside the Body"
    LESSON = "Isolated organ and muscle preparations"

    def construct(self):
        body = VGroup(silhouette(), body_vessel(2.06).set_opacity(0.36))
        ring = vessel_ring(y=0.01)
        tank = glass_bath()
        heading = fit_text(self.TITLE, max_w=11.9, size=49, min_size=40,
                           font=TITLE_FONT).move_to(p(0, 3.12))
        self.add(body, ring, tag())
        self.play(FadeOut(body), FadeIn(tank), ring.animate.shift(DOWN * 0.41),
                  run_time=0.60)
        ring.set_z_index(1)
        self.play(FadeIn(heading), run_time=0.40)
        self.wait(0.80)


class S03Bath(SpokenScene):
    def construct(self):
        tank, ring, hooks = glass_bath(), vessel_ring(), supports()
        self.add(tank, ring, tag())
        self.at("They mount")
        self.play(Create(hooks), run_time=1.55)
        self.at("called an organ bath")
        bath_name = label("Organ bath", LX, 2.90, BLUE, 40)
        self.play(FadeIn(bath_name), run_time=0.65)
        self.at("Nerves and circulating")
        nerve = VGroup(line((1.00, 1.32), (1.75, 1.32), GREY, 7),
                       line((1.50, 1.32), (1.93, 1.64), GREY, 4),
                       line((1.50, 1.32), (1.93, 1.01), GREY, 4)).shift(0.35 * LEFT)
        hormone = VGroup(*[Dot(p(1.23 + i * 0.28, -0.19 + (i % 2) * 0.22),
                               radius=0.105, color=GREY) for i in range(3)]).shift(0.35 * LEFT)
        inputs = VGroup(nerve, hormone, label("Nerves", 4.35, 1.32),
                        label("Circulating hormones", 4.35, -0.10, size=30))
        crosses = VGroup(line((1.06, 0.89), (1.94, 1.75), RED, 5),
                         line((1.06, -0.48), (1.94, 0.38), RED, 5)).shift(0.35 * LEFT)
        self.play(FadeIn(inputs), run_time=0.65)
        self.at("are now gone")
        self.play(Create(crosses), run_time=0.40)
        self.play(FadeOut(inputs), FadeOut(crosses), run_time=0.65)
        self.at("the fluid around")
        fluid = label("Bath fluid", RX, 1.28, TEAL, 36)
        self.play(tank[0].animate.set_fill("#235363"), FadeIn(fluid), run_time=0.9)
        self.at("the load stretching")
        load = label("Stretching load", RX, 1.28, BLUE, 36)
        self.play(swap(fluid, load), hooks[0].animate.set_stroke(width=7), run_time=0.83)
        self.at("chemical dripped in")
        dripper = dropper()
        addition = label("Added chemical", RX, 1.28, ORANGE, 36)
        self.play(FadeIn(dripper), swap(load, addition), hooks[0].animate.set_stroke(width=3),
                  tank[0].animate.set_fill(WATER), run_time=1.0)
        self.at("A trace shows")
        self.play(FadeOut(addition), run_time=0.35)
        plot = chart()
        self.play(Create(plot.axes), FadeIn(plot.xlabel), FadeIn(plot.ylabel), run_time=0.55)
        trace(self, plot, 0.40, lambda _: tension(0), 2.77)
        self.finish()


class S04LiningAndIdea(SpokenScene):
    def construct(self):
        tank, ring, hooks = glass_bath(), vessel_ring(), supports()
        plot = chart()
        baseline = plot.curve(tension, x1=0.40, color=YELLOW)
        tip = Dot(plot.pt(0.40, tension(0)), radius=0.085, color=YELLOW)
        self.add(tank, ring, hooks, dropper(), label("Organ bath", LX, 2.90, BLUE, 40),
                 plot, baseline, tip, tag())
        self.at("inner lining called")
        highlight = ring.lining.copy().set_stroke(PURPLE, width=6)
        self.play(FadeIn(highlight), run_time=0.42)
        self.at("the endothelium")
        inner = label("Endothelium", RX, 2.60, PURPLE, 32)
        self.play(FadeIn(inner), run_time=0.48)
        self.at("over smooth muscle")
        outer = label("Smooth muscle", RX, 2.60, GREY, 32)
        self.play(swap(inner, outer), FadeOut(highlight), ring[1][0].animate.set_stroke(width=8),
                  run_time=0.86)
        self.at("Drip acetylcholine")
        dose_label = label("Acetylcholine", RX, 2.60, ORANGE, 32)
        self.add(dose())
        self.play(swap(outer, dose_label), ring[1][0].animate.set_stroke(width=3), run_time=0.85)
        self.at("ring relaxes")
        self.remove(baseline, tip)
        pen = ValueTracker(0.40)
        self.add(plot.live_curve(tension, pen, color=YELLOW),
                 plot.dot(pen.get_value, lambda: tension(pen.get_value()),
                          color=YELLOW, ring=YELLOW, radius=0.085))
        self.play(Transform(ring, vessel_ring(relaxed=1)), pen.animate.set_value(0.65),
                  run_time=2.35, rate_func=linear)
        self.at("That illustrates")
        self.play(FadeOut(dose_label), pen.animate.set_value(0.80), run_time=2.8)
        self.at("Remove a living tissue")
        rule = caption("Control the bath. Test one cause.", size=34, color=GOLD, y=-3.23)
        self.play(FadeIn(rule), pen.animate.set_value(1), run_time=3.85)
        self.finish()


def predict_world(moving):
    plot = chart()
    bath = VGroup(glass_bath(moving=moving), mounted_ring(intact=False), dropper(),
                  dose(moving=False))
    trace_so_far = plot.curve(lambda _: tension(0), x1=0.40, color=YELLOW)
    unknown = label("?", 3.44, -0.13, GOLD, 58)
    return VGroup(bath, plot, trace_so_far, unknown, tag())


class S05PredictQ(SpokenScene):
    def construct(self):
        tank, ring, hooks, dripper = glass_bath(), vessel_ring(relaxed=1), supports(), dropper()
        plot = chart()
        completed = plot.curve(tension, color=YELLOW)
        self.add(tank, ring, hooks, dripper, plot, completed, tag())
        self.at("Now change just")
        baseline = plot.curve(lambda _: tension(0), x1=0.40, color=YELLOW)
        self.play(FadeOut(completed), Transform(ring, vessel_ring()), run_time=1.8)
        self.play(Create(baseline), run_time=0.9)
        self.at("Gently rub off")
        lining = ring.lining
        self.play(lining.animate.shift(1.77 * UP).scale(0.74), run_time=2.15)
        self.at("leaving the smooth")
        self.play(FadeOut(lining, shift=0.42 * UP), run_time=1.28)
        self.at("Drip acetylcholine")
        self.add(dose())
        self.at("Predict what happens")
        question = question_card(QUESTION, y=-3.21, size=36)
        self.play(FadeIn(label("?", 3.44, -0.13, GOLD, 58)), FadeIn(question), run_time=0.70)
        self.finish()


class S06PredictPause(PredictPause):
    QUESTION = QUESTION
    SECONDS = 4.5

    def construct(self):
        self.add(predict_world(moving=False), question_card(self.QUESTION, y=-3.21, size=36))
        self.wait(self.SECONDS)


class S07PredictA(SpokenScene):
    def construct(self):
        world = predict_world(moving=True)
        question = question_card(QUESTION, y=-3.21, size=36)
        self.add(world, question)
        self.at("No without its lining")
        self.play(FadeOut(question), FadeOut(world[3]), run_time=0.38)
        curve, cursor = trace(self, world[1], 1, lambda _: tension(0), 2.95, start=0.40)
        self.at("Acetylcholine does not")
        pair, intact, rubbed = comparison()
        self.play(FadeOut(VGroup(world, curve, cursor)), run_time=0.42)
        self.play(FadeIn(pair), FadeIn(tag()), run_time=0.48)
        self.add(dose(RX))
        self.at("It acts on endothelial")
        self.add(dose(LX))
        self.at("which make nitric oxide")
        note = caption("Nitric oxide", size=35, color=GREEN, y=-3.24)
        source = Dot(p(LX + 0.88, CY + 0.04), radius=0.13, color=GREEN)
        self.play(GrowFromCenter(source), FadeIn(note), run_time=0.72)
        self.at("nitric oxide crosses")
        self.remove(source)
        dots = messenger()
        self.add(dots)
        self.at("and relaxes it")
        self.play(Transform(intact[0], vessel_ring(relaxed=1)), run_time=1.75)
        self.at("Comparing intact and rubbed")
        self.play(FadeOut(dots), FadeOut(note), run_time=0.55)
        outcome = caption("Only the intact ring relaxes", size=35, color=GOLD, y=-3.24)
        self.play(FadeIn(outcome), run_time=0.72)
        self.at("Later work showed")
        final = caption("The messenger was nitric oxide", size=34, color=GREEN, y=-3.24)
        self.play(swap(outcome, final), run_time=0.88)
        self.finish()


def nerve_muscle(x=LX, y=CY, span=4.55):
    """Side view with an explicit gap between the nerve terminal and muscle."""
    left = x - span / 2
    terminal = x + 0.16
    nerve_scale = span / 4.55
    path = VMobject(stroke_color=GREY, stroke_width=25)
    path.set_points_smoothly([p(left, y + 0.35), p(left + 0.52 * nerve_scale, y + 0.49),
                              p(left + 1.05 * nerve_scale, y + 0.22),
                              p(terminal - 0.56 * nerve_scale, y),
                              p(terminal, y)])
    ending = VGroup(*[
        line((terminal - 0.48 * nerve_scale, y), (terminal, y + sign * 0.27), GREY, 6)
        for sign in (-1, 1)
    ])
    muscle_x = terminal + 1.10
    muscle = Ellipse(width=1.50, height=2.03, stroke_color=GREY, stroke_width=3,
                     fill_color=WALL, fill_opacity=1).move_to(p(muscle_x, y))
    striations = VGroup(*[
        Line(p(muscle_x - half, y + offset), p(muscle_x + half, y + offset),
             stroke_color=GREY, stroke_opacity=0.65, stroke_width=3)
        for offset, half in [(-0.65, 0.46), (-0.34, 0.62), (0, 0.68),
                             (0.34, 0.62), (0.65, 0.46)]
    ])
    return VGroup(path, ending), VGroup(muscle, striations)


def impulse(path, warmth):
    dot = Dot(radius=0.13, color=YELLOW)
    dot.phase = 0.0

    def travel(mob, dt):
        mob.phase = (mob.phase + (0.23 + 0.57 * warmth.get_value()) * dt) % 1
        mob.move_to(path.point_from_proportion(mob.phase))

    travel(dot, 0)
    return dot.add_updater(travel)


def thermometer(level):
    x, bottom, top = 1.7, -1.40, 1.90
    tube = RoundedRectangle(width=0.30, height=top - bottom + 0.27, corner_radius=0.15,
                            stroke_color=BLUE, stroke_width=3,
                            fill_color=WATER, fill_opacity=1).move_to(p(x, (top + bottom) / 2))
    bulb = Dot(p(x, bottom), radius=0.27, color=ORANGE)

    def column():
        return line((x, bottom), (x, bottom + (top - bottom) * level.get_value()), ORANGE, 7)

    ticks = VGroup(line((1.90, 1.90), (2.17, 1.90), GREY, 3),
                   line((1.90, -0.17), (2.17, -0.17), GREY, 3))
    return VGroup(tube, always_redraw(column), bulb, ticks)


def delay_bar():
    """Total delay is partitioned into three schematic intervals."""
    start, width, y = 0.73, 5.57, -0.32
    spans = (("Nerve", 0.53, YELLOW), ("Junction", 0.22, PURPLE),
             ("Muscle", 0.25, GREY))
    strips = VGroup()
    for _, share, color in spans:
        w = width * share
        block = Rectangle(width=w - 0.045, height=0.69, stroke_width=0,
                          fill_color=color, fill_opacity=1).move_to(p(start + w / 2, y))
        strips.add(block)
        start += w
    # Stagger the last label to keep both narrow segments' labels legible.
    legend = VGroup(*[
        label(name, block.get_x(), legend_y, color, size=28)
        for (name, _, color), block, legend_y in zip(spans, strips, (-1.15, -1.15, -1.65))
    ])
    return strips, legend


class S08Controls(SpokenScene):
    def construct(self):
        tank = glass_bath()
        nerve, muscle = nerve_muscle()
        warmth = ValueTracker(1)
        self.add(tank, tag())
        self.at("an isolated bath")
        self.play(FadeIn(nerve), FadeIn(muscle), run_time=1.05)
        self.at("frog nerve and")
        specimen = label("Frog nerve and muscle", LX, 2.91, TEXT, 34)
        self.play(FadeIn(specimen), run_time=0.55)
        self.at("temperature follows")
        thermometer_body = thermometer(warmth)
        temperature = label("37 °C", 3.87, 1.90, ORANGE, 36)
        room = label("Room temperature", 4.19, -0.18, TEAL, 32)
        self.add(impulse(nerve[0], warmth))
        self.play(FadeIn(thermometer_body), FadeIn(temperature), run_time=0.78)
        self.at("cooling slows conduction")
        self.play(warmth.animate.set_value(0.38), run_time=2.18)
        self.at("room temperature frog")
        self.play(FadeIn(room), run_time=0.62)
        self.at("human value at")
        mismatch = label("Frog ≠ human", 3.84, -1.66, RED, 35)
        self.play(FadeIn(mismatch), run_time=0.75)
        self.at("Nerve speed is")
        self.play(FadeOut(VGroup(thermometer_body, temperature, room, mismatch)), run_time=0.46)
        formula = label("Nerve speed =\ndistance ÷ nerve delay", 3.48, 2.10, TEXT, 32)
        strips, legend = delay_bar()
        total = label("Total delay", 3.47, 0.63, TEXT, 34)
        self.play(FadeIn(formula), FadeIn(strips), FadeIn(total), FadeIn(legend), run_time=1.05)
        self.at("first subtract junction")
        self.play(FadeOut(strips[1]), FadeOut(legend[1]), run_time=0.83)
        self.at("muscle delays")
        nerve_delay = label("Nerve delay", strips[0].get_x(), 0.63, YELLOW, 34)
        self.play(FadeOut(strips[2]), FadeOut(legend[2]), swap(total, nerve_delay), run_time=0.86)
        self.at("match controls")
        checks = caption("Matched controls", color=GREEN, size=35, y=-3.22)
        self.play(FadeIn(checks), run_time=0.56)
        self.at("subtracted delays")
        subtract = caption("Subtract other delays", color=GREEN, size=35, y=-3.22)
        self.play(swap(checks, subtract), run_time=0.78)
        self.at("species checks")
        self.play(swap(subtract, caption("Check the species", color=GREEN, size=35, y=-3.22)),
                  run_time=0.78)
        self.finish()


class S09UnlockedVessel(SpokenScene):
    def construct(self):
        pair, intact, _ = comparison()
        self.add(pair, tag())
        self.at("With controls like those")
        self.play(Create(pair[2][0][1][0].copy().set_stroke(PURPLE, width=5)),
                  run_time=0.70, rate_func=there_and_back, remover=True)
        self.at("In 1980")
        history = label("1980 — Furchgott & Zawadzki", 0, 3.44, GOLD, 35)
        self.play(FadeIn(history), run_time=0.75)
        self.at("organ bath test")
        rabbit = caption("Rabbit aortic rings", size=35, y=-3.30)
        self.play(FadeIn(rabbit), run_time=0.74)
        self.at("Only intact rings")
        left_dose, right_dose = dose(), dose(RX)
        self.add(left_dose, right_dose)
        self.play(Transform(intact[0], vessel_ring(relaxed=1)), run_time=2.3)
        self.at("the lining sends")
        direction = arrow((LX + 1.12, CY + 0.20), (LX + 1.69, CY + 0.32), GREEN, 5)
        self.play(GrowArrow(direction), run_time=0.66)
        pulse(direction, base=5, amp=2.3, speed=4)
        self.finish()


def tubule(x=0, y=CY, scale=1):
    tube = RoundedRectangle(width=5.12, height=1.22, corner_radius=0.35,
                            stroke_color=GREY, stroke_width=4,
                            fill_color=WALL, fill_opacity=1)
    lumen = RoundedRectangle(width=5.06, height=0.68, corner_radius=0.28,
                             stroke_width=0, fill_color="#285B6F", fill_opacity=1)
    tips = VGroup(pipette(-2.38, 0, PI / 2, TEAL, length=2.22, spread=1.23),
                  pipette(2.38, 0, -PI / 2, TEAL, length=2.22, spread=1.23))
    return VGroup(tube, lumen, tips).scale(scale).shift(p(x, y))


def perfusate():
    stream = VGroup()
    for i in range(14):
        bead = Dot(radius=0.07 + (i % 2) * 0.028, color=TEAL)
        bead.phase = i / 14

        def flow(mob, dt, lane=i % 3):
            mob.phase = (mob.phase + dt * 0.20) % 1
            mob.move_to(p(-4.37 + 8.74 * mob.phase, CY + (lane - 1) * 0.13))
            mob.set_opacity(min(1, 15 * mob.phase, 15 * (1 - mob.phase)))

        flow(bead, 0)
        bead.add_updater(flow)
        stream.add(bead)
    return stream


def water_drops(x, lanes, rate):
    """Schematic water crossing from the lumen into the bath."""
    drops = VGroup()
    for offset, phase in lanes:
        drop = VMobject(stroke_width=0, fill_color=TEAL)
        drop.set_points_smoothly([
            p(0, 0.15), p(0.105, -0.015), p(0, -0.12),
            p(-0.105, -0.015), p(0, 0.15),
        ])
        drop.phase = phase

        def cross_wall(mob, dt, lane=x + offset):
            mob.phase = (mob.phase + rate * dt) % 1
            mob.move_to(p(lane, CY - 1.48 * mob.phase))
            mob.set_fill(opacity=min(1, 9 * mob.phase, 6 * (1 - mob.phase)))

        cross_wall(drop, 0)
        drops.add(drop.add_updater(cross_wall))
    return drops


class S10UnlockedTubule(SpokenScene):
    def construct(self):
        tank = glass_bath(0, 11.88)
        ring = vessel_ring(x=0, relaxed=1)
        specimen = tubule()
        wall = VGroup(specimen[0], specimen[1])
        self.add(tank, ring, tag())
        self.at("In 1970")
        history = label("1970 — Kokko", 0, 3.14, GOLD, 39)
        self.play(FadeIn(history), run_time=0.62)
        self.at("held tiny rabbit")
        self.play(ReplacementTransform(ring, wall), run_time=1.72)
        thin = label("Thin descending limb", 0, 1.83, TEXT, 34)
        self.at("thin descending limbs")
        self.play(FadeIn(thin), run_time=0.56)
        self.at("between glass pipettes")
        self.play(FadeIn(specimen[2][0], shift=0.30 * RIGHT),
                  FadeIn(specimen[2][1], shift=0.30 * LEFT), run_time=0.84)
        self.at("flowed controlled fluid")
        stream = perfusate()
        self.add(stream)
        inside = caption("Flow through the tubule", size=34, color=BLUE, y=-3.27)
        self.play(FadeIn(inside), run_time=0.68)
        self.at("setting the bath")
        outside = caption("Control the surrounding bath", size=34, color=TEAL, y=-3.27)
        self.play(swap(inside, outside), tank[0].animate.set_fill("#235363"), run_time=1.0)
        self.at("low sodium permeability")
        sodium = tracer_dots([(-1.51, CY - 0.08), (-0.40, CY + 0.07), (1.31, CY - 0.13),
                             (0.58, CY + 0.14)],
                            [(-1.36, CY - 0.24), (-0.18, CY + 0.23), (1.48, CY - 0.24),
                             (0.68, CY + 0.91)], YELLOW, duration=2.6, radius=0.09)
        self.add(sodium)
        low = caption("Low sodium permeability", size=34, color=YELLOW, y=-3.27)
        self.play(swap(outside, low), run_time=0.82)
        self.at("no detectable active")
        none = caption("No detectable active salt transport", size=34, color=YELLOW, y=-3.27)
        self.play(swap(low, none), run_time=0.87)
        self.at("Water permeability")
        check = caption("Water permeability varies across species", size=34, color=TEXT, y=-3.27)
        left, right = -2.85, 2.85
        species = VGroup(tubule(left, scale=0.52), tubule(right, scale=0.52))
        names = VGroup(label("Species A", left, 0.70), label("Species B", right, 0.70))
        self.play(FadeOut(VGroup(wall, *specimen[2], stream, sodium, history, thin)),
                  run_time=0.25)
        self.play(FadeIn(species), FadeIn(names), swap(none, check), run_time=0.55)
        self.add(water_drops(left, [(-0.72, 0.1), (0, 0.42), (0.72, 0.74)], rate=0.92),
                 water_drops(right, [(0, 0.23)], rate=0.40))
        self.finish()


def synaptic_dots(blocked):
    group = VGroup()
    for i in range(8):
        bead = Dot(radius=0.060, color=ORANGE)
        bead.phase = i / 8

        def release(mob, dt, i=i):
            mob.phase = (mob.phase + 0.86 * dt) % 1
            saved = blocked.get_value()
            travel = mob.phase if not saved else (i + 1) / 9
            mob.move_to(p(LX + 0.21 + 0.25 * travel,
                          CY + (i % 5 - 2) * 0.12 + 0.045 * np.sin(TAU * mob.phase)))
            mob.set_opacity(1 if saved else min(1, 8 * mob.phase, 3.1 * (1 - mob.phase)))

        release(bead, 0)
        bead.add_updater(release)
        group.add(bead)
    return group


def detector_signal(time):
    """Uncalibrated schematic interpolating baseline, contraction and hold."""
    return 0.24 + 0.53 * smooth(np.clip((time - 0.32) / 0.37, 0, 1))


def closing_bath():
    tank = glass_bath(0, 11.88)
    nerve, muscle = nerve_muscle(3.3, CY, span=2.70)
    return VGroup(tank, vessel_ring(x=-3.78, scale=0.70), tubule(x=-0.31, scale=0.29),
                  nerve, muscle)


class S11UnlockedMuscleClose(SpokenScene):
    def construct(self):
        tank = glass_bath()
        nerve, muscle = nerve_muscle()
        blocked = ValueTracker(0)
        drops = synaptic_dots(blocked)
        history = label("Dale & Feldberg", LX, 2.95, GOLD, 39)
        self.add(tank, nerve, muscle, tag())
        self.at("And Dale and")
        self.add(drops)
        self.play(FadeIn(history), run_time=0.68)
        self.at("An enzyme called")
        enzyme = Dot(p(LX + 0.37, CY - 0.61), radius=0.18, color=PURPLE)
        self.play(GrowFromCenter(enzyme), run_time=0.47)
        enzyme_name = label("Acetylcholinesterase", RX, 1.28, PURPLE, 36)
        self.play(FadeIn(enzyme_name), run_time=0.67)
        self.at("clears acetylcholine")
        clearance = label("Clears acetylcholine", RX, 0.13, ORANGE, 35)
        self.play(FadeIn(clearance), run_time=0.75)
        self.at("in milliseconds")
        milliseconds = label("Milliseconds", RX, -0.95, GOLD, 32)
        self.play(FadeIn(milliseconds), run_time=0.55)
        self.at("They blocked that enzyme")
        stop = Line(enzyme.get_corner(DL) + 0.035 * DL, enzyme.get_corner(UR) + 0.035 * UR,
                    stroke_color=RED, stroke_width=6)
        self.play(Create(stop), blocked.animate.set_value(1),
                  FadeOut(VGroup(enzyme_name, clearance, milliseconds)), run_time=0.72)
        plot = chart("Muscle response")
        self.at("used a living muscle")
        self.play(FadeIn(plot), run_time=0.64)
        pen = ValueTracker(0.012)
        signal = plot.live_curve(detector_signal, pen, color=YELLOW)
        cursor = plot.dot(pen.get_value, lambda: detector_signal(pen.get_value()),
                          color=YELLOW, ring=YELLOW, radius=0.085)
        self.add(signal, cursor)
        self.play(pen.animate.set_value(0.32), run_time=0.37)
        self.at("as a detector")
        self.play(muscle.animate.stretch(0.74, 0).stretch(1.13, 1),
                  pen.animate.set_value(0.69), run_time=1.04)
        self.play(pen.animate.set_value(1), run_time=0.82)
        self.at("Strip away competing")
        apparatus = VGroup(tank, nerve, muscle, history, drops, enzyme, stop, plot, signal, cursor)
        self.play(FadeOut(apparatus), run_time=0.38)
        closing = closing_bath()
        self.play(FadeIn(closing), run_time=0.52)
        self.at("keep the tissue alive")
        self.play(closing[0][0].animate.set_fill("#235363"), run_time=1.15)
        self.at("one controlled test")
        rule = caption("One controlled test can reveal the cause.", size=35, color=GOLD, y=-3.26)
        self.play(FadeIn(rule), run_time=0.83)
        self.finish()


class S12End(EndCard):
    LINE = "Isolate a tissue to control its bath and test one cause."
