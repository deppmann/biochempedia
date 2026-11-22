"""Function-blocking antibodies, timed to the provided narration.

Color map (from the patch-clamp film): GREY marks cell structure, PURPLE
marks membrane receptors, GOLD marks the signal being tested and dates,
BLUE marks the second factor, ORANGE marks added blockers, GREEN marks a
cell response, RED marks a loss, and TEAL marks the extracellular space.
"""
from bp_parts import *

PURPLE = "#B58CD9"
ORANGE = "#F29E4C"
SOURCE_FILL = "#263E4D"
TARGET_FILL = "#293D52"
TARGET_RIM = "#536C85"
QUESTION = "Sympathetic ganglia? Eyelids?"
UPPER, LOWER = 0.88, -0.92
MOUTH_X = 1.75


def pt(x, y):
    return np.array([x, y, 0.0])


def line(a, b, color=GREY, width=5):
    return Line(pt(*a), pt(*b), color=color, stroke_width=width)


def path(points, color, width=5):
    shape = VMobject().set_points_smoothly([pt(*p) for p in points])
    shape.set_stroke(color, width)
    return shape


def branch(growth=1.0, x=4.22, y=-0.04, size=1.0):
    """A soma and its extending branches, also used at the ganglion scale."""
    roots = ((-0.10, 0.06), (0.08, 0.13), (0.08, -0.15), (0.09, -0.02))
    ends = ((-0.96, 0.58), (1.22, 1.47), (1.27, -1.28), (1.52, 0.12))
    fibers = VGroup()
    for i, ((rx, ry), (ex, ey)) in enumerate(zip(roots, ends)):
        ax, ay = ex * growth, ey * growth
        fibers.add(path([(rx, ry), (ax * 0.55, ay * 0.52), (ax, ay)], TARGET_RIM, 7))
        side = 1 if i % 2 else -1
        fibers.add(path([(ax * 0.63, ay * 0.61), (ax * 0.85, ay * 0.72 + side * 0.13),
                         (ax * 1.08, ay * 0.76 + side * 0.34)], TARGET_RIM, 4))
    soma = Ellipse(width=0.87, height=0.97, stroke_width=0, fill_color=TARGET_RIM, fill_opacity=1)
    nucleus = Dot(pt(0.04, -0.02), radius=0.16, color=TARGET_FILL)
    return VGroup(fibers, soma, nucleus).scale(size, about_point=ORIGIN).shift(pt(x, y))


def cup(x, y, scale=1):
    """An open receptor pocket. Free decoys use the very same silhouette."""
    pocket = Arc(radius=0.37, start_angle=-2.30, angle=4.60, arc_center=ORIGIN)
    pocket.set_stroke(PURPLE, 10)
    stem = line((0.30, 0), (0.63, 0), PURPLE, 8)
    return VGroup(stem, pocket).scale(scale, about_point=ORIGIN).shift(pt(x, y))


def antibody(x, y, scale=1, angle=0):
    cartoon = VGroup(line((0, -0.52), (0, -0.03), ORANGE, 12),
                     line((0, -0.03), (-0.36, 0.34), ORANGE, 12),
                     line((0, -0.03), (0.36, 0.34), ORANGE, 12),
                     line((-0.36, 0.34), (-0.47, 0.45), ORANGE, 7),
                     line((0.36, 0.34), (0.47, 0.45), ORANGE, 7))
    return cartoon.scale(scale, about_point=ORIGIN).rotate(angle, about_point=ORIGIN).shift(pt(x, y))


def wedge(x, y, scale=1):
    shape = Polygon(pt(-0.30, -0.23), pt(-0.30, 0.23), pt(0.23, 0.12), pt(0.23, -0.12),
                    fill_color=ORANGE, fill_opacity=1, stroke_width=0)
    return shape.scale(scale, about_point=ORIGIN).shift(pt(x, y))


def bead(x, y, color=GOLD, radius=0.19):
    halo = Dot(radius=radius * 1.58, color=color, fill_opacity=0.16)
    core = Dot(radius=radius, color=color)
    glint = Dot(pt(-radius * 0.28, radius * 0.30), radius=radius * 0.30, color=TEXT)
    return VGroup(halo, core, glint).shift(pt(x, y))


def grow_pulse(y, strong=True):
    """The intracellular response travels away from the occupied receptor."""
    color = GREEN
    trace = path([(2.30, y), (3.03, y * 0.68), (3.68, y * 0.25), (4.25, -0.04)], color, 10)
    trace.set_opacity(0.85 if strong else 0.55)
    return trace


def chamber(growth=1, neuron=True, receptors=True):
    """The fixed two-cell section stays registered across all experiments."""
    source = Ellipse(width=3.45, height=4.80, stroke_width=0,
                     fill_color=SOURCE_FILL, fill_opacity=1).move_to(pt(-4.82, 0.05))
    target = Ellipse(width=4.40, height=4.92, stroke_width=0,
                     fill_color=TARGET_FILL, fill_opacity=1).move_to(pt(4.45, 0))
    nucleus = Ellipse(width=1.27, height=1.55, stroke_width=0,
                      fill_color="#375569", fill_opacity=1).move_to(pt(-5.07, 0.05))
    borders = VGroup(
        path([(-3.93, 1.86), (-3.36, 1.28), (-3.10, 0.05), (-3.35, -1.17), (-3.92, -1.79)], GREY, 4),
        path([(2.94, 1.80), (2.42, 0.98), (2.25, 0), (2.42, -0.98), (2.94, -1.80)], GREY, 4),
    )
    body = VGroup(source, target, nucleus, borders)
    tree = branch(growth)
    pockets = VGroup(cup(MOUTH_X, UPPER), cup(MOUTH_X, LOWER))
    world = VGroup(body)
    if neuron:
        world.add(tree)
    if receptors:
        world.add(pockets)
    return world, tree, pockets


def flow(color=GOLD, start=-2.94, stop=1.33, y=0, spread=1.28, phase=0, count=6):
    """Visible transport in the gap, bounded short of the receptor mouths."""
    stream = VGroup()
    for i in range(count):
        particle = bead(0, 0, color, radius=0.16 + 0.027 * (i % 3))
        lane = ((i * 3) % 7 - 3) / 3
        def drift(mob, dt, lane=lane, i=i):
            mob.clock += dt
            u = (mob.clock / (6.6 + 0.4 * (i % 3)) + i / count) % 1
            h = y + spread * lane + 0.15 * np.sin(TAU * u + i)
            mob.move_to(pt(interpolate(start, stop, u), h))
            # Each particle fades at the left source rim and at the flow boundary.
            level = min(1, u / 0.09, (1 - u) / 0.12)
            mob[0].set_opacity(0.16 * level)
            mob[1].set_opacity(level)
            mob[2].set_opacity(level)
        particle.clock = phase
        particle.add_updater(drift, call_updater=True)
        stream.add(particle)
    return stream


def legend(label, x=0, color=TEXT, y=2.93, size=32):
    return T(label, size, color).move_to(pt(x, y))


def dock(particle, x, y, arch=0.28):
    a = particle.get_center()
    b = pt(x, y)
    return MoveAlongPath(particle, CubicBezier(a, interpolate(a, b, 0.32) + UP * arch,
                                              interpolate(a, b, 0.72) + UP * arch, b))


def drift_together(scene, blocker, particle, **motion):
    assembly = VGroup(blocker, particle)
    scene.remove(blocker, particle)
    scene.add(bob(assembly, **motion))
    return assembly


def tagged_world(scene, **options):
    world, tree, pockets = chamber(**options)
    scene.add(world, scope_tag(color=TEXT))
    return world, tree, pockets


class S01Hook(SpokenScene):
    def construct(self):
        _, tree, _ = tagged_world(self, growth=0.72)
        stream = flow(phase=0.7)
        first = bead(-1.52, 0.43)
        self.add(stream, first)
        self.at("a secreted signal")
        self.play(dock(first, MOUTH_X - 0.11, UPPER), FadeIn(legend("Signal", -2.20, GOLD)), run_time=0.95)
        response = grow_pulse(UPPER)
        self.play(Create(response), Transform(tree, branch()), run_time=0.80)
        self.at("yet does it")
        question = legend("?", 0, TEXT, y=2.80, size=60)
        self.play(FadeIn(question, shift=UP * 0.32), FadeIn(legend("Receptor", 1.98, PURPLE)), run_time=0.55)
        self.at("to find out")
        ring = Ellipse(width=4.21, height=3.93, stroke_color=TEAL, stroke_width=5, stroke_opacity=0.62)
        ring.move_to(pt(-0.76, -0.02))
        self.play(Create(ring), FadeOut(question), FadeOut(response), run_time=1.65)
        self.finish()


class S02Title(TitleCard):
    LESSON = "Function-Blocking Antibodies"
    TITLE = "Stopping a Signal Outside the Cell"

    def construct(self):
        world, _, _ = chamber()
        self.add(world, flow(phase=2.50), scope_tag(color=TEXT))
        title = fit_text(self.TITLE, max_w=11.7, size=45, min_size=35, font=TITLE_FONT)
        title.move_to(pt(0, 3.12))
        self.play(FadeIn(title), run_time=0.40)
        self.wait(1.20)
        self.play(FadeOut(title), run_time=0.40)


class S03Antibody(SpokenScene):
    def construct(self):
        tagged_world(self)
        stream = flow(phase=1.13, stop=1.28)
        initial_pulse = grow_pulse(UPPER)
        initial_pulse.set_opacity(0.55)
        self.add(stream, initial_pulse)
        upper = antibody(-0.77, 0.43)
        lower = antibody(0.33, -1.40)
        self.at("one tool is", lead=0)
        self.play(FadeIn(upper, shift=DOWN * 1.00), run_time=1.1)
        self.at("neutralizing antibody")
        name = legend("Antibody", 0, ORANGE)
        self.play(FadeIn(name), FadeIn(lower, shift=UP * 0.65), run_time=1.25)
        self.at("added outside")
        passing = bead(-2.45, 1.06)
        another = bead(-1.82, -0.74)
        self.add(passing, another)
        self.play(dock(passing, -0.77, 0.75), run_time=2.20)
        self.play(dock(another, 0.33, -1.08), run_time=1.9)
        self.at("the receptors stay empty")
        drift_together(self, upper, passing, amp=0.17, speed=1.6)
        drift_together(self, lower, another, amp=0.14, speed=1.4, seed=2)
        self.at("so the message")
        self.play(FadeOut(initial_pulse), run_time=1.50)
        self.finish()


def decoys():
    return VGroup(cup(-0.75, 1.00), cup(0.15, -0.91))


class S04Decoy(SpokenScene):
    def construct(self):
        tagged_world(self)
        stream = flow(phase=2.1, stop=0.90)
        previous = VGroup(antibody(-0.77, 0.43), bead(-0.77, 0.75),
                          antibody(0.33, -1.40), bead(0.33, -1.08))
        self.add(stream, previous)
        traps = decoys()
        self.at("a second tool", lead=0)
        self.play(FadeOut(previous, shift=DOWN * 0.58), FadeIn(traps, shift=DOWN * 0.54), run_time=1.0)
        self.at("decoy receptor")
        self.play(FadeIn(legend("Decoy receptor", 0, PURPLE)), run_time=0.6)
        self.at("why does")
        incoming = bead(-2.60, 0.53)
        lower = bead(-2.48, -1.03)
        self.add(incoming, lower)
        self.play(dock(incoming, -1.37, 0.84), dock(lower, -1.15, -0.98), run_time=2.4)
        self.at("its binding pocket")
        self.play(dock(incoming, -0.87, 1.00, 0.13), dock(lower, 0.03, -0.91, 0.14), run_time=2.35)
        self.at("leaving the cell's")
        drift_together(self, traps[0], incoming, amp=0.15, speed=1.9)
        drift_together(self, traps[1], lower, amp=0.16, speed=1.7, seed=1)
        self.finish()


def receptor_cap():
    return antibody(1.35, UPPER, scale=0.78, angle=-PI / 2)


def receptor_plug():
    return wedge(1.62, LOWER, 0.91)


class S05ReceptorBlock(SpokenScene):
    def construct(self):
        _, tree, _ = tagged_world(self)
        previous = VGroup(decoys(), bead(-0.87, 1), bead(0.03, LOWER))
        stream = flow(phase=2.45, stop=0.94)
        self.add(previous, stream)
        self.at("block the receptor")
        self.play(FadeOut(previous, shift=DOWN * 0.72), run_time=1.1)
        cap = receptor_cap()
        plug = receptor_plug()
        self.at("an antibody caps", lead=0.85)
        self.play(FadeIn(cap, shift=RIGHT * 1.02), run_time=1.4)
        self.at("a short peptide", lead=0.68)
        self.play(FadeIn(plug, shift=RIGHT * 0.88), run_time=1.07)
        self.play(FadeIn(legend("Peptide", 1.43, ORANGE, y=-2.03)), run_time=0.38)
        self.at("every blocker works")
        a, b = bead(-1.65, 0.72), bead(-1.90, -1.29)
        self.add(a, b)
        self.play(dock(a, 0.85, UPPER, 0.13), dock(b, 1.04, LOWER, 0.18), run_time=2.1)
        self.at("keep signal and receptor")
        self.play(dock(a, -1.2, 1.43), dock(b, -1.55, -1.43, -0.25),
                  Transform(tree, branch(0.70)), run_time=2.75)
        self.finish()


def ganglion(x=4.55, y=1.16, color=TARGET_RIM, sparse=False):
    positions = [(-0.65, -0.12), (0.02, 0.29), (0.68, -0.23), (-0.08, -0.43), (0.65, 0.29)]
    neurons = VGroup()
    for i, (dx, dy) in enumerate(positions[:1] if sparse else positions):
        n = branch(x=x + dx, y=y + dy, size=0.28 if i % 2 else 0.33)
        n[1].set_fill(color)
        neurons.add(n)
    return neurons


def eyelid(opened=False):
    x, y = 4.53, -1.01
    a, b = pt(x - 0.86, y), pt(x + 0.86, y)
    if opened:
        top = ArcBetweenPoints(a, b, angle=-1.45, color=BLUE, stroke_width=5)
        bottom = ArcBetweenPoints(a, b, angle=1.34, color=BLUE, stroke_width=5)
        iris = Dot(pt(x, y), radius=0.26, color=BLUE)
        pupil = Dot(pt(x, y), radius=0.12, color=TARGET_FILL)
        return VGroup(top, bottom, iris, pupil)
    lid = ArcBetweenPoints(a, b, angle=0.62, color=BLUE, stroke_width=5)
    lashes = VGroup(*(line((x + i * 0.23, y - 0.11), (x + i * 0.26, y - 0.30), BLUE, 3)
                     for i in (-2, -1, 0, 1, 2)))
    return VGroup(lid, lashes)


def outcome_labels():
    return (legend("Sympathetic ganglia", 4.51, TEXT, y=2.82, size=28),
            legend("Eyelids", 4.51, TEXT, y=-1.80, size=28))


def ngf_antiserum():
    return VGroup(antibody(-0.80, 1.03), antibody(0.35, 0.32, 0.92))


def predict_world():
    world, _, _ = chamber(neuron=False)
    return world, ganglion(), eyelid(), outcome_labels(), ngf_antiserum()


def factors():
    return (legend("NGF", -2.24, GOLD, size=34),
            legend("Second factor", 0.38, BLUE, size=32))


def predict_prompt():
    return question_card(QUESTION, y=-3.04, size=38)


def approaching_ngf():
    particle = bead(-1.59, 1.39)
    particle.clock = 0

    def approach(mob, dt):
        mob.clock += dt
        mob.move_to(pt(-1.38 - 0.23 * np.cos(2.0 * mob.clock),
                       1.38 + 0.073 * np.sin(2.0 * mob.clock)))

    return particle.add_updater(approach, call_updater=True)


class S06PredictQ(SpokenScene):
    def construct(self):
        world, nerves, eye, (nerve_lab, eye_lab), antibodies = predict_world()
        ngf, second = factors()
        gold = flow(phase=1.40, y=0.72, spread=0.8, count=5)
        blue = flow(BLUE, phase=0.62, y=-1.02, spread=0.64, count=5)
        self.add(world, gold, scope_tag(color=TEXT))
        self.at("nerve growth factor")
        self.play(FadeIn(ngf), run_time=0.65)
        self.at("which acts on")
        self.play(LaggedStart(*(GrowFromCenter(n) for n in nerves), lag_ratio=0.21), run_time=1.7)
        self.play(FadeIn(nerve_lab), run_time=0.55)
        self.at("a sample holds")
        self.play(Indicate(ngf, color=GOLD, scale_factor=1.08), run_time=1.35)
        self.at("a second factor", lead=0.65)
        self.add(blue)
        self.play(FadeIn(second), run_time=0.72)
        self.at("opens eyelids", lead=0.45)
        self.play(Create(eye), run_time=0.60)
        self.play(FadeIn(eye_lab), run_time=0.50)
        self.at("sample plus anti")
        self.play(FadeIn(antibodies, shift=DOWN * 0.68), run_time=1.65)
        self.at("carrying antibodies")
        self.remove(gold)
        self.add(flow(phase=5.45, stop=0.34, y=0.83, spread=0.69, count=5))
        active = bead(-2.47, 1.42)
        self.add(active)
        self.play(dock(active, -1.36, 1.43, 0.35), run_time=2.4)
        self.at("what happens to")
        self.play(FadeOut(active), FadeIn(predict_prompt()), run_time=0.65)
        self.add(approaching_ngf())
        self.finish()


class S07PredictPause(Scene):
    def construct(self):
        self.camera.background_color = BG
        world, nerves, eye, labels, antibodies = predict_world()
        gold = flow(phase=12.3, stop=0.34, y=0.83, spread=0.69, count=5)
        blue = flow(BLUE, phase=16.1, y=-1.02, spread=0.64, count=5)
        approaching = approaching_ngf()
        self.add(world, gold, blue, nerves, eye, *labels, *factors(), antibodies,
                 approaching, predict_prompt(), scope_tag(color=TEXT))
        self.wait(4.5)


class S08PredictAnswer(SpokenScene):
    def construct(self):
        world, nerves, eye, (nerve_lab, eye_lab), antibodies = predict_world()
        blue = flow(BLUE, phase=1.9, y=-1.12, spread=0.55, count=5)
        ngf, second = factors()
        sample, own = bead(-1.58, 1.41), bead(1.03, 0.55)
        self.add(world, blue, nerves, eye, nerve_lab, eye_lab, ngf, second, antibodies,
                 sample, own, scope_tag(color=TEXT))
        self.at("anti -serum traps")
        self.play(dock(sample, -0.80, 1.35), run_time=2.08)
        self.at("the mouse's own")
        self.play(dock(own, 0.35, 0.62, 0.19), run_time=1.32)
        drift_together(self, antibodies[0], sample, amp=0.15, speed=1.8)
        drift_together(self, antibodies[1], own, amp=0.15, speed=1.6, seed=3)
        self.at("most sympathetic ganglia")
        losses = [FadeOut(n, scale=0.22) for n in nerves[1:]]
        self.play(LaggedStart(*losses, lag_ratio=0.20), run_time=2.40)
        destroyed = legend("Most destroyed", 4.48, RED, y=0.17, size=30)
        self.play(FadeIn(destroyed), run_time=0.48)
        self.at("cohen raised it")
        credit = caption("Cohen / Levi-Montalcini & Booker", color=GOLD, y=-3.04)
        self.play(FadeIn(credit), run_time=0.60)
        self.at("yet the eyelids")
        arriving = bead(-0.32, -1.40, BLUE)
        self.add(arriving)
        self.play(dock(arriving, MOUTH_X - 0.11, LOWER, 0.10), FadeOut(credit), run_time=1.62)
        self.play(Transform(eye, eyelid(True)), run_time=0.60)
        self.at("the second factor slips")
        other = bead(-2.21, -1.45, BLUE)
        self.add(other)
        self.play(dock(other, 1.14, -1.08, -0.13), run_time=2.65)
        self.finish()


def developmental_strip():
    xs = (-4.85, -1.20, 2.45)
    y = -2.74
    rail = line((xs[0], y), (xs[-1], y), GREY, 4)
    stops = VGroup(*(Dot(pt(x, y), radius=0.067, color=GREY) for x in xs))
    ages = VGroup(*(legend(age, x, TEXT, y=-3.24, size=28)
                   for age, x in zip(("Before birth", "Newborn", "Older"), xs)))
    marker = Dot(pt(xs[1], y), radius=0.149, color=GOLD)
    return VGroup(rail, stops, ages), marker, tuple(pt(x, y) for x in xs)


class S09LimitsTiming(SpokenScene):
    def construct(self):
        tagged_world(self, neuron=False)
        strip, marker, (prenatal, _, older) = developmental_strip()
        older_nerves = ganglion(x=4.55, y=0.40)
        older_label = outcome_labels()[0]
        gold = flow(phase=0.65, y=0.21, spread=1.47, stop=1.06, count=7)
        self.add(gold)
        self.at("a blocker can mislead", lead=0)
        self.play(FadeIn(older_nerves), run_time=0.92)
        self.at("dose or timing")
        self.play(FadeIn(strip), FadeIn(marker), FadeIn(older_label), run_time=0.75)
        circulating = antibody(-0.67, 0.83)
        self.at("the same anti")
        self.play(FadeIn(circulating, shift=RIGHT * 1.25), marker.animate.move_to(older), run_time=2.4)
        gold_hit = bead(-2.19, 1.29)
        self.add(gold_hit)
        self.play(dock(gold_hit, -0.67, 1.14, 0.21), run_time=1.95)
        self.at("sensory neurons")
        sensory = ganglion(x=4.55, y=0.40, color=TEAL)
        sensory_label = legend("Sensory neurons", 4.51, TEXT, y=2.82, size=28)
        self.play(marker.animate.move_to(prenatal), FadeOut(older_nerves), FadeIn(sensory),
                  FadeOut(VGroup(circulating, gold_hit)), swap(older_label, sensory_label), run_time=2.55)
        window = line((-5.34, -2.74), (-4.36, -2.74), GOLD, 10)
        self.add(window)
        self.bring_to_front(marker)
        self.at("johnson and colleagues")
        paper = legend("Johnson and colleagues, 1980", -0.40, GOLD, size=30)
        self.play(FadeIn(paper), run_time=0.50)
        self.at("with maternal antibody", lead=1.68)
        maternal = ngf_antiserum()
        self.play(FadeIn(maternal, shift=RIGHT * 1.30), run_time=1.10)
        remaining = bead(-1.95, 1.38)
        self.add(remaining)
        self.play(dock(remaining, -0.80, 1.35), run_time=1.32)
        self.play(LaggedStart(*(FadeOut(n, scale=0.20) for n in sensory), lag_ratio=0.15), run_time=1.78)
        self.at("test at the wrong")
        lesson = legend("Timing can hide a need", -0.40, TEXT, size=32)
        intact = ganglion(x=4.55, y=0.40, color=TEAL)
        self.play(marker.animate.move_to(older), FadeOut(window), FadeIn(intact),
                  swap(paper, lesson), run_time=0.75)
        self.finish()


def fragment_test(panels):
    """Side-by-side intervention cartoons built inside the shared panels."""
    left = VGroup(*(bead(x, y, radius=0.24) for x, y in
                    ((-0.95, 0.23), (-0.40, -0.36), (0.05, 0.58), (0.58, -0.18), (1.12, 0.26))))
    panel_left = panels.area("left")[0]
    panel_right = panels.area("right")[0]
    left.move_to(panel_left + LEFT * 0.65)
    collector = cup(panel_right[0] - 0.48, panel_right[1], 1.50)
    incoming = bead(panel_right[0] - 1.99, panel_right[1] - 0.16, radius=0.26)
    targets = VGroup()
    for center in (panel_left, panel_right):
        target_center = center + UP * 0.35
        cell = Ellipse(width=1.90, height=2.48, fill_color=TARGET_FILL,
                       fill_opacity=1, stroke_width=0).move_to(target_center + RIGHT * 1.72)
        receptor = cup(target_center[0] + 0.79, target_center[1] - 0.42, scale=0.72)
        targets.add(VGroup(cell, receptor))
    return left, collector, incoming, targets


class S10LimitsControls(SpokenScene):
    def construct(self):
        world, _, _ = tagged_world(self)
        cap = receptor_cap()
        gold = flow(phase=1.16, stop=1.15, count=7)
        self.add(gold)
        self.at("overlap can also", lead=0)
        first = bead(-2.26, UPPER)
        other = bead(-2.75, LOWER)
        self.add(first, other)
        self.play(dock(first, -0.67, UPPER, 0.08), dock(other, -0.84, LOWER, -0.12), run_time=3.50)
        self.at("when two receptors")
        both = legend("Shared job", 0.60, PURPLE)
        self.play(FadeIn(both), run_time=0.58)
        self.at("blocking one")
        response = grow_pulse(LOWER, False)
        self.play(FadeIn(cap, shift=LEFT * 0.75), dock(other, MOUTH_X - 0.11, LOWER, -0.10),
                  dock(first, -1.45, 1.10, 0.32), run_time=1.18)
        self.play(Create(response), run_time=0.80)
        self.at("experimenters pair blocking")
        panels = TwoPanel("Add factor", "Block factor", colors=(GOLD, PURPLE),
                          top=2.53, bottom=-2.48, size=32)
        gain, collector, incoming, targets = fragment_test(panels)
        self.play(FadeOut(VGroup(world, cap, gold, first, other, both, response)), run_time=0.45)
        self.play(FadeIn(panels), FadeIn(targets), FadeIn(gain, shift=RIGHT * 0.38), Create(collector),
                  FadeIn(incoming), run_time=1.2)
        for i, particle in enumerate(gain):
            bob(particle, amp=0.42, speed=1.80, seed=i)
        bob(incoming, amp=0.34, speed=1.9)
        self.at("and check against", lead=0.85)
        genetics = caption("✓ Genetics cross-check", color=GREEN, y=-3.09)
        self.play(FadeIn(genetics), run_time=0.35)
        self.at("in 2001", lead=0)
        self.play(FadeOut(genetics), run_time=0.38)
        paper = legend("Fukuchi-Shimogori & Grove, 2001", -0.40, GOLD, size=30)
        self.play(FadeIn(paper), run_time=0.55)
        self.at("added fgf8")
        self.play(FadeIn(legend("FGF8", -3.2, GOLD, y=-1.67)), run_time=0.52)
        self.at("a receptor fragment")
        incoming.clear_updaters()
        fragment = legend("Receptor-fragment blocker", 3.2, PURPLE, y=-1.67, size=28)
        self.play(dock(incoming, collector.get_x() - 0.38, panels.area("right")[0][1]),
                  FadeIn(fragment),
                  run_time=1.12)
        self.finish()


def fibronectin(phase=0, retraction=0):
    anchors = [(-3.22, 0.36), (-2.54, 0.04), (-1.97, 0.38), (-1.35, 0.99),
               (-0.63, 1.19), (0.03, 1.02), (0.78, 1.18), (1.52, UPPER)]
    left_x, right_x = anchors[0][0], anchors[-1][0]
    last = len(anchors) - 1
    bowed = [(x - retraction * (x - left_x) / (right_x - left_x),
              y + 0.38 * np.sin(PI * i / last) * np.sin(phase - i * 0.65))
             for i, (x, y) in enumerate(anchors)]
    tether = path(bowed, TEAL, 13)
    return VGroup(tether, bead(1.55 - retraction, UPPER, GOLD, radius=0.20))


def flex_tether(strand):
    strand.clock = 0

    def flex(tether, dt):
        tether.clock += dt
        tether.become(fibronectin(tether.clock * 1.65)[0])

    strand.add_updater(flex)


def attached_cell():
    silhouette = Ellipse(width=1.84, height=1.30, fill_opacity=1, stroke_width=0,
                         fill_color=SOURCE_FILL).move_to(pt(-0.84, -1.25))
    nucleus = Dot(pt(-1.04, -1.22), radius=0.26, color="#44657A")
    tether = path([(-0.02, -1.23), (0.37, -0.98), (0.98, -1.11), (1.53, LOWER)], TEAL, 8)
    return VGroup(silhouette, nucleus), VGroup(tether, bead(1.55, LOWER, radius=0.16))


def myelin_sign(x, y):
    backing = RegularPolygon(8, radius=0.41, color=RED, stroke_width=4,
                             fill_color="#512A34", fill_opacity=1).move_to(pt(x, y))
    stop = line((x - 0.20, y), (x + 0.20, y), RED, 7)
    return VGroup(backing, stop)


class S11UnlockedA(SpokenScene):
    def construct(self):
        _, tree, pockets = tagged_world(self, growth=0.70)
        strand = fibronectin()
        cell, held = attached_cell()
        self.at("with those checks", lead=0)
        self.play(Create(strand[0]), GrowFromCenter(strand[1]), FadeIn(cell), FadeIn(held), run_time=2.5)
        flex_tether(strand[0])
        grip = legend("RGD", 1.51, GOLD, y=1.58, size=30)
        paper = legend("Pierschbacher & Ruoslahti, 1984", -0.38, GOLD, size=30)
        self.at("in 1984")
        self.play(FadeIn(paper), run_time=0.55)
        self.at("found r .g")
        self.play(FadeIn(grip), Indicate(strand[1], color=GOLD, scale_factor=1.22), run_time=1.35)
        self.at("free r .g")
        plugs = VGroup(wedge(-0.72, 1.02), wedge(-1.84, -0.61))
        self.play(FadeIn(plugs, shift=RIGHT * 0.7), run_time=0.73)
        self.at("fills the cell's")
        strand[0].clear_updaters()
        retracted = fibronectin(strand[0].clock * 1.65, retraction=0.86)
        peptide = legend("Free RGD peptide", 0.0, ORANGE, y=-2.42, size=30)
        attached = VGroup(cell, held)
        self.play(Transform(strand, retracted),
                  attached.animate.shift(LEFT * 0.55 + DOWN * 0.18),
                  plugs[0].animate.move_to(pt(1.61, UPPER)),
                  plugs[1].animate.move_to(pt(1.61, LOWER)),
                  FadeOut(grip), FadeIn(peptide), run_time=1.54)
        self.at("so fewer cells")
        self.play(attached.animate.shift(LEFT * 0.78), run_time=1.72)

        self.at("in 1988")
        stops = VGroup(myelin_sign(1.45, 0.77), myelin_sign(1.35, -0.65))
        old = VGroup(strand, attached, plugs, peptide, pockets)
        later_paper = legend("Caroni & Schwab, 1988", -0.38, GOLD, size=30)
        self.play(FadeOut(old), FadeIn(stops), swap(paper, later_paper), run_time=0.87)
        inhibit = VGroup(antibody(-0.60, 0.48, 0.72, -PI / 2),
                         antibody(-0.96, -0.65, 0.72, -PI / 2)).set_z_index(1)
        self.at("schwab's antibody", lead=0.53)
        self.play(FadeIn(inhibit, shift=RIGHT * 0.78), run_time=0.69)
        in_one = legend("IN-1", 0.60, ORANGE, size=32, y=-2.06)
        self.play(FadeIn(in_one), run_time=0.41)
        self.at("neutralized myelin")
        self.play(inhibit[0].animate.shift(RIGHT * 1.46 + UP * 0.29),
                  inhibit[1].animate.shift(RIGHT * 1.72), run_time=1.26)
        caught = VGroup(stops, inhibit)
        self.play(caught.animate.shift(LEFT * 1.65).set_opacity(0.70),
                  Transform(tree, branch(1.04)), run_time=1.22)
        extension = path([(4.22, 0.07), (3.79, 0.11), (3.16, 0.44), (2.63, 0.37),
                          (1.91, 0.14), (1.17, 0.21), (0.42, 0.49)], GREEN, 14)
        self.at("nerve growth", lead=0.14)
        self.play(Create(extension), run_time=2.35, rate_func=linear)
        self.at("was later cloned", lead=0.16)
        antigen = legend("Nogo-A (cloned later)", 0.33, RED, size=30, y=-2.06)
        fresh_tip = path([(1.17, 0.21), (0.82, -0.04), (0.55, -0.22), (0.32, -0.45)], GREEN, 9)
        self.play(swap(in_one, antigen), Create(fresh_tip), run_time=1.68)
        self.finish()


def cortex():
    layers = VGroup()
    for row, y in enumerate((-1.23, -0.43, 0.39, 1.18)):
        layer = VGroup()
        for col in range(4):
            x = 3.25 + col * 0.74 + (0.09 if row % 2 else 0)
            cell = Ellipse(width=0.31, height=0.50, stroke_width=0,
                           fill_color=(BLUE if row % 2 else TEAL), fill_opacity=0.88)
            cell.move_to(pt(x, y))
            layer.add(cell)
        layers.add(layer)
    return layers


def capture_and_plug():
    """The two extracellular interventions in the closing picture."""
    a = antibody(-0.93, 0.74)
    b = antibody(-1.60, -0.81)
    ca = VGroup(a, bead(-0.93, 1.06))
    cb = VGroup(b, bead(-1.60, -0.49))
    return VGroup(ca, cb), receptor_plug()


class S12UnlockedB(SpokenScene):
    def construct(self):
        tagged_world(self, neuron=False, receptors=False)
        layers = cortex()
        reelin = flow(phase=1.63, stop=1.08, spread=1.15, count=7)
        self.add(layers, reelin)
        blocker = antibody(-0.83, 0.67)
        credit = legend("Ogawa, Mikoshiba and colleagues", -0.40, GOLD, size=30)
        self.at("and colleagues added")
        self.play(FadeIn(credit), FadeIn(blocker, shift=RIGHT * 1.0), run_time=1.30)
        cr = legend("CR-50", -0.86, ORANGE, y=-2.0)
        self.at("antibody cr50")
        self.play(FadeIn(cr), run_time=0.49)
        self.at("embryonic cortical")
        cultured = legend("Embryonic cortical cells", 4.51, TEXT, y=-2.78, size=28)
        ball = bead(-2.51, 1.03)
        self.add(ball)
        self.play(FadeIn(cultured), dock(ball, -0.83, 0.99, 0.25), run_time=1.76)
        captured = drift_together(self, blocker, ball, amp=0.17, speed=1.6)
        self.at("normal tissue then")
        offsets = ((0.15, 0.28), (-0.16, -0.26), (0.12, -0.48), (0.22, 0.37),
                   (-0.15, -0.30), (0.28, 0.41), (-0.11, -0.35), (-0.24, 0.55),
                   (0.19, 0.04), (-0.18, 0.30), (0.18, 0.29), (-0.23, 0.08),
                   (-0.15, -0.20), (0.21, -0.34), (-0.18, -0.22), (0.12, -0.56))
        self.play(LaggedStart(*(cell.animate.shift(pt(*offset)).rotate((i % 3 - 1) * 0.68)
                                for i, (cell, offset) in enumerate(zip(
                                    (cell for row in layers for cell in row), offsets))),
                              lag_ratio=0.15), run_time=2.3)
        reeler = legend("reeler pattern", 4.51, TEXT, y=-2.78, size=28)
        self.play(swap(cultured, reeler), run_time=0.72)
        self.at("in 1997")
        result = legend("1997  ·  CR-50 recognizes Reelin", -0.40, GOLD, size=30)
        self.play(swap(credit, result), run_time=0.78)
        self.at("a secreted glycoprotein")
        reelin_lab = legend("Reelin", -2.65, GOLD, y=-2.0, size=30)
        self.play(FadeIn(reelin_lab), run_time=0.63)

        self.at("catch the signal", lead=0.53)
        _, tree, pockets = chamber(growth=0.76)
        trapped, plug = capture_and_plug()
        self.play(FadeOut(VGroup(layers, captured, reeler, reelin_lab, result, cr)), run_time=0.48)
        self.play(FadeIn(tree), FadeIn(pockets), FadeIn(trapped), run_time=0.65)
        for i, complex_ in enumerate(trapped):
            bob(complex_, amp=0.22, speed=1.6, seed=i)
        self.at("plug its receptor")
        self.play(FadeIn(plug, shift=RIGHT * 0.88), run_time=0.65)
        self.finish()


class S13End(EndCard):
    LINE = "Block a signal or receptor to test whether it is needed."
