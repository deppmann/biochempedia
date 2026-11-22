"""Chemogenetics and genetic silencing, timed to the supplied narration.

COLOR MAP (patch-clamp palette): BLUE target cells and actuators, GREY tissue
and neighbours, PURPLE receptors, ORANGE added ligand or toxin, YELLOW
neural signals, GREEN observed responses, RED blocks and targeting errors,
GOLD questions and study credits, TEAL reporter and driver range, PINK target protein.
"""

from bp_parts import *  # noqa: F403
from bp_style import EndCard


PURPLE = "#B58CD9"
ORANGE = "#F29E4C"
PINK = "#F397B2"
TISSUE = "#303e51"
PANEL = "#273441"
QUESTION = "Force to pull away: rise or fall?"
CARD = {"size": 34}
CELL_CENTRES = ((-0.15, 1.88), (-1.10, 0.99), (-1.70, 0), (-0.94, -0.99), (-0.15, -1.88))
TARGETS = (1, 2, 3)


def point(x, y):
    return np.array([x, y, 0.0])


def path(points, color=GREY, width=3):
    curve = VMobject(stroke_color=color, stroke_width=width)
    curve.set_points_smoothly([point(*p) for p in points])
    return curve


def arrow(a, b, color=GREY, width=5):
    return Arrow(point(*a), point(*b), buff=0, color=color, stroke_width=width, tip_length=0.20)


def label(text, x, y, color=TEXT, size=30):
    return T(text, size, color).move_to(point(x, y))


def heading(text, color=TEXT):
    return label(text, 0, 3.22, color, 34)


def panel(x, y, w, h, color=PANEL):
    return RoundedRectangle(
        width=w, height=h, corner_radius=0.24,
        stroke_width=0, fill_color=color, fill_opacity=1,
    ).move_to(point(x, y))


def neuron(x, y, color):
    """A single soma, with dendrites and an axon ending at the circuit output."""
    axon = path([(x, y), (x + 0.86, y * .94), (0.92, y * .72), (1.42, y * .25)], color, 4.2)
    dendrites = VGroup(*[
        path([(-3.77, y * .70 + bend * .25), (-2.95, y + bend * .56),
              (x - .62, y + bend * .46), (x, y)], color, 3.4)
        for bend in (-.7, .7)
    ])
    shape = Ellipse(width=1.36, height=.81, stroke_color=color, stroke_width=3.2,
                    fill_color=color, fill_opacity=.39).rotate(.15).move_to(point(x, y))
    nucleus = Dot(point(x + .07, y), radius=.13, color=color, fill_opacity=.80)
    terminal = Dot(axon.get_end(), radius=.095, color=color)
    return VGroup(dendrites, axon, terminal, shape, nucleus), dendrites[0], axon, shape


def moving_signal(fibre, phase, level):
    """Highlight a travelling stretch of fibre as an activity packet passes."""
    packet = fibre.copy().set_stroke(YELLOW, width=19)

    def travel(mob, dt):
        nonlocal phase
        phase = (phase + dt * .46) % 1.38
        lo, hi = np.clip((phase - .38, phase), 0, 1)
        mob.pointwise_become_partial(fibre, lo, hi)
        # Keep the same number of Bézier points when the whole circuit zooms.
        padding = len(fibre.points) - len(mob.points)
        mob.append_points(np.repeat(mob.points[-1:], padding, axis=0))
        mob.set_stroke(opacity=level.get_value() * min(1, 4 * (hi - lo)))

    return packet.add_updater(travel, call_updater=True)


class Circuit(VGroup):
    """Rebuild the teaching circuit at the same coordinates for every carry-over."""

    def __init__(self, active=.64, ambient=True):
        self.tissue = panel(-1.31, 0, 6.36, 5.12, TISSUE)
        cells = [neuron(*xy, BLUE if i in TARGETS else GREY) for i, xy in enumerate(CELL_CENTRES)]
        self.cells = VGroup(*(cell for cell, _, _, _ in cells))
        self.targets = VGroup(*(self.cells[i] for i in TARGETS))
        self.active_targets = self.targets.copy()
        self.activity = ValueTracker(active)
        self.neighbour_activity = ValueTracker(.90)
        self.signals = VGroup()
        if ambient:
            for i, (_, dendrite, axon, soma) in enumerate(cells):
                level = self.activity if i in TARGETS else self.neighbour_activity
                glow = soma.copy().set_stroke(width=0)
                glow.scale(.99)
                phase = .27 * i
                self.signals.add(VGroup(glow, moving_signal(dendrite, 1.30 - phase, level),
                                        moving_signal(axon, phase, level)))
                self.heartbeat(glow, level, i)
        super().__init__(self.tissue, self.cells, self.signals)

    @staticmethod
    def heartbeat(glow, level, index):
        phase = .7 * index

        def update(mob, dt):
            nonlocal phase
            phase += 3.8 * dt
            mob.set_fill(opacity=level.get_value() * (.06 + .81 * (1 + np.sin(phase)) / 2))

        glow.add_updater(update, call_updater=True)

    def quiet(self):
        return (self.activity.animate.set_value(.04), self.targets.animate.fade(.60))

    def reactivate(self):
        return (self.activity.animate.set_value(.78), Transform(self.targets, self.active_targets.copy()))


def receptors():
    cups = VGroup()
    for i in TARGETS:
        x, y = CELL_CENTRES[i]
        cups.add(path([(x + .29, y + .36), (x + .32, y + .13),
                       (x + .61, y + .13), (x + .64, y + .36)], PURPLE, 8))
    return cups


def ligand_dots(cups, docked=False):
    dots = VGroup()
    for i, cup in enumerate(cups):
        dock = point(cup.get_x(), cup.get_bottom()[1] + .16)
        start = point(-3.95 + .4 * i, 2.12 - .17 * i)
        dots.add(Dot(dock if docked else start, radius=.105, color=ORANGE))
    return dots


def docking(cups, dots):
    return AnimationGroup(*[
        MoveAlongPath(dot, path([(dot.get_x(), dot.get_y()), (-2.45 + i * .16, 1.5 - .52 * i),
                                 (cup.get_x() + .21, cup.get_y() + .6),
                                 (cup.get_x(), cup.get_bottom()[1] + .16)]))
        for i, (cup, dot) in enumerate(zip(cups, dots))
    ], lag_ratio=.19)


def probe(touch=False):
    pad = RoundedRectangle(width=.34, height=1.80, corner_radius=.13, stroke_width=2,
                           stroke_color=GREY, fill_color=GREY, fill_opacity=.38).move_to(point(-4.80, 0))
    tip = Polygon(point(-6.34, .26), point(-5.52, .17), point(-5.20, 0),
                  point(-5.52, -.17), point(-6.34, -.26), color=GREY,
                  fill_color=GREY, fill_opacity=.67, stroke_width=2)
    if touch:
        tip.shift(RIGHT * .23)
    return pad, tip


def readout(lit=.45):
    box = panel(4.50, 0, 3.55, 4.15)
    lamp = Circle(radius=.71, stroke_color=GREEN, stroke_width=4,
                  fill_color=GREEN, fill_opacity=lit).move_to(point(4.50, .28))
    return VGroup(box, lamp, label("Behaviour", 4.50, -1.22)), lamp


def question_meter():
    box = panel(4.50, 0, 3.55, 4.15)
    question = label("?", 4.50, .34, GOLD, 76)
    up = arrow((5.34, .01), (5.34, 1.02), GOLD)
    down = arrow((3.66, .78), (3.66, -.23), GOLD)
    return VGroup(box, question, up, down, label("Force to pull away", 4.50, -1.22, size=28)), VGroup(up, down)


def threshold_meter(level):
    return VGroup(panel(4.50, 0, 3.55, 4.15),
                  dial(level, (4.50, .11, 0), radius=1.32, color=GREEN, fmt="↑", size=34),
                  label("Withdrawal\nthreshold", 4.50, -1.22, size=28))


def spinal_picture(ambient=True):
    circuit = Circuit(active=.72, ambient=ambient)
    cups = receptors()
    dots = ligand_dots(cups, docked=True)
    pad, tip = probe(touch=True)
    output = arrow((1.89, 0), (2.62, 0), YELLOW, 13)
    tag = label("Spinal cord", -1.31, 2.95)
    return circuit, cups, dots, pad, tip, output, tag


class S01Hook(SpokenScene):
    def construct(self):
        circuit = Circuit()
        response, lamp = readout()
        incoming = arrow((-5.95, 0), (-4.52, 0), YELLOW, 9)
        output = arrow((1.89, 0), (2.62, 0), YELLOW, 9)
        hook = label("?", -1.31, 3.06, GOLD, 65)
        self.add(circuit, response, incoming, output, hook, scope_tag(size=28))
        self.at("many kinds of")
        self.play(FadeOut(hook), FadeIn(label("Sensory input", -5.35, -.81, size=28)), run_time=.65)
        self.at("watching them fire")
        pulse(incoming, base=14, amp=8, speed=7)
        pulse(output, base=14, amp=8, speed=7)
        self.play(lamp.animate.set_fill(opacity=.72), run_time=1.35)
        self.finish()


class S02Title(TitleCard):
    LESSON = "Chemogenetics and genetic silencing"
    TITLE = "Switching One Cell Type On or Off"

    def construct(self):
        circuit = Circuit()
        title = fit_text(self.TITLE, size=48, min_size=36, max_w=11.8, font=TITLE_FONT).move_to(point(0, 3.16))
        lesson = label(self.LESSON, -1.31, -3.15, TEXT)
        self.add(circuit, scope_tag(size=28))
        self.play(FadeIn(title), FadeIn(lesson), run_time=5 / 15)
        self.wait(20 / 15)
        self.play(FadeOut(title), FadeOut(lesson), run_time=5 / 15)


def lox(x, y):
    return Triangle(stroke_width=0, fill_color=PURPLE, fill_opacity=1).scale(.15).rotate(-PI / 2).move_to(point(x, y))


def gene_row(y, text, color):
    block = boxed_label("Actuator gene", GREY, size=29, pad=.15, fill_opacity=.13).move_to(point(4.65, y))
    stop = boxed_label("STOP", RED, size=29, pad=.14, fill_opacity=.16).move_to(point(1.96, y))
    left, right = lox(.78, y), lox(3.09, y)
    backbone = Line(point(.05, y), point(.53, y), color=GREY, stroke_width=4)
    return VGroup(backbone, left, right, stop, block,
                  label(text, 1.75, y + .58, color, size=28)), stop, right, block


class S03Targeting(SpokenScene):
    def construct(self):
        circuit = Circuit()
        gene_panel = panel(3.13, 0, 6.40, 4.55)
        self.add(circuit, scope_tag(size=28))
        self.at("mouse genetics")
        self.play(circuit.activity.animate.set_value(1), run_time=1.1)
        definition = heading("Actuator", BLUE)
        self.at("an actuator is")
        self.play(FadeIn(definition), run_time=.5)
        switches = VGroup(*[
            RoundedRectangle(width=.46, height=.19, corner_radius=.09,
                             stroke_color=BLUE, stroke_width=3, fill_color=BLUE,
                             fill_opacity=.17).move_to(point(x - .19, y + .38))
            for x, y in (CELL_CENTRES[i] for i in TARGETS)
        ])
        knobs = VGroup(*(Dot(s.get_left() + RIGHT * .13, radius=.09, color=BLUE) for s in switches))
        examples = VGroup(switches, knobs)
        self.play(FadeIn(examples), run_time=.55)
        self.at("that starts or")
        self.play(knobs.animate.shift(RIGHT * .20), run_time=.74)
        self.at("stops cell activity")
        self.play(knobs.animate.shift(LEFT * .20), FadeOut(definition), run_time=.55)
        neighbour, _, _, _ = gene_row(.92, "Neighbour cell", GREY)
        target, stop, site, inactive = gene_row(-.82, "Target cell", BLUE)
        sites = label("loxP sites", 1.96, -1.49, PURPLE, size=28)
        self.at("a stop flank")
        self.play(FadeOut(examples), circuit.animate.scale(.73).move_to(point(-3.72, 0)),
                  FadeIn(gene_panel, shift=RIGHT * .23), run_time=.64)
        examples.scale(.73, about_point=point(-1.31, 0)).shift(LEFT * 2.41)
        self.play(FadeIn(neighbour, shift=RIGHT * .25), run_time=.48)
        self.play(FadeIn(target, shift=RIGHT * .25), FadeIn(sites), run_time=.63)
        cre = boxed_label("Cre recombinase", TEAL, size=29, pad=.14).move_to(point(1.96, -1.72))
        contact = Line(cre.get_top() + UP * .03, stop.get_bottom() + DOWN * .03,
                       color=TEAL, stroke_width=4)
        self.at("cells making cre")
        self.play(swap(sites, cre), run_time=.58)
        self.play(Create(contact), run_time=.28)
        self.at("delete that stop")
        self.play(FadeOut(stop, shift=UP * .12), FadeOut(site), FadeOut(contact), run_time=.62)
        active = boxed_label("Actuator gene", BLUE, size=29, pad=.15, fill_opacity=.34).move_to(inactive)
        bridge = Line(point(1.03, -.82), point(3.21, -.82), color=BLUE, stroke_width=4)
        self.at("switching it on")
        self.play(Create(bridge), swap(inactive, active, .67), FadeOut(cre), FadeIn(examples), run_time=.67)
        self.play(knobs.animate.shift(RIGHT * .15), run_time=.63)
        self.finish()


class S04Dreadd(SpokenScene):
    def construct(self):
        circuit = Circuit(active=.48)
        cups = receptors()
        dots = ligand_dots(cups)
        top_x, top_y = CELL_CENTRES[0]
        bottom_x, bottom_y = CELL_CENTRES[4]
        bypass_paths = (
            path([(-2.75, 2.28), (top_x - .99, top_y + .13),
                  (top_x - .64, top_y + .49), (top_x + .21, top_y + .55),
                  (1.53, 2.37)]),
            path([(-2.91, -1.67), (bottom_x - 1.03, bottom_y - .03),
                  (bottom_x - .62, bottom_y - .48), (bottom_x + .18, bottom_y - .55),
                  (1.57, -2.34)]),
        )
        bypass = VGroup(*(Dot(track.get_start(), radius=.105, color=ORANGE) for track in bypass_paths))
        response, lamp = readout(lit=.12)
        output = arrow((1.89, 0), (2.62, 0), YELLOW, 8)
        self.add(circuit, response, output, scope_tag(size=28))
        self.at("targeted cells build")
        self.play(LaggedStart(*(Create(cup) for cup in cups), lag_ratio=.24), run_time=1.1)
        name = heading("DREADD", PURPLE)
        self.at("designer receptor")
        self.play(FadeIn(name), run_time=.5)
        ligand = heading("Synthetic ligand", ORANGE)
        self.at("a synthetic ligand")
        self.play(FadeIn(dots), FadeIn(bypass), swap(name, ligand, .6), run_time=.6)
        self.at("that ligand drifts")
        self.play(docking(cups, dots),
                  *(MoveAlongPath(dot, track) for dot, track in zip(bypass, bypass_paths)), run_time=4.2)
        sufficient = caption("Sufficient?", size=36, color=GOLD)
        activating = heading("Activating DREADD", PURPLE)
        self.at("driving the targeted")
        self.play(FadeOut(bypass, shift=RIGHT * .23),
                  circuit.activity.animate.set_value(1), lamp.animate.set_fill(opacity=.82),
                  output.animate.set_stroke(width=19), swap(ligand, activating), run_time=1.45)
        self.at("sufficient for a")
        self.play(FadeIn(sufficient), run_time=.45)
        incoming = arrow((-5.91, 0), (-4.52, 0), YELLOW, 11)
        necessary = caption("Necessary?", size=36, color=GOLD)
        self.at("quieting them tests")
        self.play(FadeIn(incoming), *circuit.quiet(), lamp.animate.set_fill(opacity=.12),
                  output.animate.set_stroke(width=3), swap(sufficient, necessary),
                  swap(activating, heading("Inhibitory DREADD", PURPLE)), run_time=1.4)
        pulse(incoming, base=13, amp=7, speed=7)
        self.finish()


def toxin(x, y):
    drop = path([(x, y + .37), (x + .24, y), (x, y - .27), (x - .24, y), (x, y + .37)], ORANGE, 3)
    return drop.set_fill(ORANGE, opacity=.82)


class S05Silencing(SpokenScene):
    def construct(self):
        circuit = Circuit()
        self.add(circuit, scope_tag(size=28))
        self.at("can also quiet")
        self.play(circuit.activity.animate.set_value(.24), run_time=1.5)
        dots = VGroup(*(Dot(point(1.67, y), radius=.10, color=YELLOW) for y in (.32, 0, -.32)))
        self.at("silence transmitter release")
        self.play(FadeIn(dots, shift=RIGHT * .16), circuit.activity.animate.set_value(0), run_time=.72)
        release = heading("Transmitter release blocked")
        self.play(FadeIn(release), run_time=.5)
        drop = toxin(-1.65, 2.15)
        ablation = caption("Ablation", color=RED, size=34)
        toxin_label = heading("Diphtheria toxin", ORANGE)
        self.at("permanently remove cells")
        self.play(FadeOut(dots), FadeOut(release), FadeIn(drop, shift=DOWN * .30), run_time=.48)
        self.play(drop.animate.shift(DOWN * .75), run_time=.65)
        self.at("called ablation")
        self.play(FadeIn(toxin_label), circuit.targets.animate.fade(1),
                  FadeOut(drop), FadeIn(ablation), run_time=.75)
        self.at("reversible inhibition tests")
        restored = Circuit(active=.64)
        cups = receptors()
        ligand = ligand_dots(cups, docked=True)
        self.play(FadeOut(toxin_label), FadeOut(ablation), run_time=.40)
        self.remove(circuit)
        self.add(restored)
        self.play(FadeIn(cups), FadeIn(ligand), run_time=.6)
        rev = heading("Reversible inhibition", PURPLE)
        self.play(*restored.quiet(), FadeIn(rev), run_time=1.50)
        self.at("a genetic switch")
        self.play(FadeOut(rev), run_time=.35)
        self.play(FadeOut(ligand, shift=UP * .30), *restored.reactivate(),
                  FadeIn(caption("Switch on or off to test the role", size=34)), run_time=2.35)
        self.finish()


class S06PredictQ(SpokenScene):
    def construct(self):
        circuit, cups, dots, pad, tip, output, tag = spinal_picture()
        tip.shift(LEFT * .23)
        meter, _ = question_meter()
        self.add(circuit, output, scope_tag(size=28))
        self.at("suppose excitatory spinal")
        self.play(FadeIn(tag), FadeIn(pad), FadeIn(tip), run_time=.75)
        self.at("responses to mechanical")
        self.play(tip.animate.shift(RIGHT * .23), run_time=1.15)
        self.at("an inhibitory designer")
        self.play(LaggedStart(*(Create(cup) for cup in cups), lag_ratio=.23), run_time=1.6)
        travelling = ligand_dots(cups)
        self.at("and give the ligand")
        self.add(travelling)
        self.play(docking(cups, travelling), run_time=1.9)
        self.remove(travelling)
        self.add(dots)
        self.at("force needed to")
        self.play(FadeIn(meter), FadeIn(question_card(QUESTION, **CARD)), run_time=.62)
        self.at("rise or fall")
        self.play(circuit.activity.animate.set_value(0), circuit.neighbour_activity.animate.set_value(0),
                  run_time=1.1)
        self.finish()


class S07PredictPause(PredictPause):
    QUESTION = QUESTION
    CARD = CARD
    SECONDS = 4.5
    RING_AT = (-5.85, -3.02, 0)

    def backdrop(self):
        circuit, cups, dots, pad, tip, output, tag = spinal_picture(ambient=False)
        meter, arrows = question_meter()
        for index, (ligand, indicator) in enumerate(zip(dots, arrows)):
            bob(ligand, amp=.047, speed=2.7, seed=index)
            pulse(indicator, base=7, amp=2.4, speed=2.7)
        return VGroup(circuit, cups, dots, pad, tip, output, tag, meter, scope_tag(size=28))

    def finish(self):
        remaining = self.narration_s - self.elapsed()
        if remaining > 0:
            self.wait(remaining)


class S08PredictAnswer(SpokenScene):
    def construct(self):
        circuit, cups, dots, pad, tip, output, tag = spinal_picture()
        meter, _ = question_meter()
        question = question_card(QUESTION, **CARD)
        self.add(circuit, cups, dots, pad, tip, output, tag, meter, question, scope_tag(size=28))
        level = ValueTracker(.26)
        threshold = threshold_meter(level)
        self.at("it rises", lead=0)
        self.play(swap(meter, threshold, 1.0), FadeOut(question), run_time=1.0)
        self.play(level.animate.set_value(.55), run_time=.95)
        self.at("quieting those excitatory")
        self.play(*circuit.quiet(), output.animate.set_stroke(width=3), run_time=1.60)
        self.at("sensitive to mechanical")
        self.play(tip.animate.shift(LEFT * .23), rate_func=there_and_back, run_time=1.35)
        self.at("mechanical withdrawal threshold")
        self.play(level.animate.set_value(.85), run_time=2.6)
        self.at("takes stronger force")
        self.play(tip.animate.shift(RIGHT * .10),
                  FadeIn(caption("Takes stronger force", color=GREEN, size=34)), run_time=1.35)
        self.finish()


class S09Controls(SpokenScene):
    def construct(self):
        circuit = Circuit()
        self.add(circuit, scope_tag(size=28))
        past = heading("Past expression", BLUE)
        former = circuit.cells[0]
        stray = circuit.cells[4]
        self.at("cre marking is")
        self.play(former.animate.set_color(BLUE), run_time=1.25)
        self.at("cell that ever")
        self.play(FadeIn(past), run_time=.6)
        leaky = label("Leaky", 3.79, -1.40, RED, 35)
        mosaic = label("Mosaic", 3.81, 1.16, RED, 35)
        leaky_line = path([(3.04, -1.40), (2.44, -1.51), (1.64, -1.92), (.56, -1.92)], RED, 3)
        mosaic_line = path([(2.84, 1.16), (2.16, 1.16), (.26, .91), (-.43, .88)], RED, 3)
        self.at("be leaky in")
        self.play(FadeOut(past), former.animate.set_color(GREY), stray.animate.set_color(BLUE),
                  FadeIn(leaky), Create(leaky_line), run_time=.85)
        self.at("mosaic missing")
        missed = VGroup(circuit.cells[1], circuit.cells[2])
        self.play(missed.animate.set_color(GREY).fade(.6), FadeIn(mosaic),
                  Create(mosaic_line), FadeOut(circuit.signals[1]), FadeOut(circuit.signals[2]),
                  run_time=1.25)
        halo = Circle(radius=.47, color=TEAL, fill_color=TEAL, fill_opacity=.38, stroke_width=5)
        halo.move_to(point(*CELL_CENTRES[3]))
        reporter = heading("Reporter light", TEAL)
        protein = Dot(point(-.76, -1.01), radius=.16, color=PINK)
        self.at("reporter light misses")
        self.play(FadeOut(VGroup(leaky, mosaic, leaky_line, mosaic_line)), FadeIn(halo),
                  FadeIn(reporter), run_time=.68)
        pulse(halo, base=9, amp=5, speed=5)
        self.at("leftover target protein")
        self.add(protein)
        self.play(FadeOut(halo), run_time=1.07)
        self.at("measure driver range")
        verify = heading("Verify directly in tissue")
        driver = VGroup(*(
            DashedVMobject(Ellipse(width=1.53, height=1.07, stroke_color=TEAL, stroke_width=7),
                           num_dashes=14)
            .move_to(point(*CELL_CENTRES[i])) for i in (3, 4)
        ))
        driver_key = VGroup(
            DashedVMobject(Circle(radius=.23, stroke_color=TEAL, stroke_width=7), num_dashes=8),
            T("Driver range", 30, TEAL),
        ).arrange(RIGHT, buff=.24).move_to(point(4.38, .76))
        protein_key = VGroup(Dot(radius=.16, color=PINK), T("Target protein", 30, PINK))
        protein_key.arrange(RIGHT, buff=.24).move_to(point(4.38, -.77))
        self.play(swap(reporter, verify), FadeIn(driver_key), FadeIn(protein_key), Create(driver), run_time=1.4)
        self.finish()


def hairy_skin():
    skin = panel(-5.38, -.1, 1.78, 2.58, "#68535b")
    hairs = VGroup(*(path([(-6.21 + .46 * i, .62), (-6.21 + .46 * i, 1.46),
                           (-6.47 + .46 * i, 1.96)], GREY, 5)
                     for i in range(1, 4)))
    return VGroup(skin, hairs, label("Hairy skin", -5.38, -1.84, size=28))


def mouse():
    body = Ellipse(width=.73, height=.39, color=TEXT, stroke_width=0, fill_opacity=1)
    head = Ellipse(width=.35, height=.24, color=TEXT, stroke_width=0, fill_opacity=1).move_to(point(.34, .05))
    ear = Dot(point(.24, .19), radius=.09, color=GREY)
    eye = Dot(point(.43, .09), radius=.031, color=BG)
    tail = path([(-.32, -.03), (-.53, -.15), (-.65, -.08), (-.72, .03)], TEXT, 2.8)
    return VGroup(body, head, ear, eye, tail)


def chambers():
    first = panel(3.67, -.03, 1.55, 3.80)
    paired = panel(5.33, -.03, 1.55, 3.80)
    animal = mouse().move_to(point(3.65, -.37))
    return VGroup(first, paired), paired, animal


class S10UnlockedTouch(SpokenScene):
    def construct(self):
        circuit = Circuit(active=.43)
        cups = receptors()
        ligand = ligand_dots(cups)
        skin = hairy_skin()
        box, paired, animal = chambers()
        self.add(circuit, scope_tag(size=28))
        self.at("those checks these")
        self.play(FadeIn(skin), run_time=.9)
        credit = label("Vrontou et al., 2013", 4.52, 2.63, GOLD, 28)
        self.at("and colleagues put")
        self.play(FadeIn(cups), FadeIn(credit), run_time=.9)
        self.at("in mrgprb for")
        self.play(FadeIn(heading("MrgprB4 sensory neurons", BLUE)), run_time=.65)
        self.at("activating those hairy")
        self.add(ligand)
        self.play(docking(cups, ligand), circuit.activity.animate.set_value(1.0),
                  FadeIn(box), run_time=2.70)
        self.play(FadeIn(animal), paired.animate.set_fill(GREEN, opacity=.43), run_time=.84)
        self.at("conditioned place preference")
        self.play(FadeIn(caption("Conditioned place preference", size=33)), run_time=.75)
        paired_label = VGroup(T("Activation-", 26, GREEN), T("paired", 26, GREEN))
        paired_label.arrange(DOWN, buff=.10).move_to(point(5.33, -2.47))
        self.at("spent more time")
        self.play(FadeOut(ligand), circuit.activity.animate.set_value(.46),
                  FadeIn(paired_label), run_time=.59)
        self.play(MoveAlongPath(animal, path([(3.65, -.37), (4.40, -.55), (5.28, -.40)])), run_time=1.13)
        self.play(MoveAlongPath(animal, path([(5.28, -.40), (5.49, -.12), (5.40, .43), (5.28, .67)])), run_time=2.55)
        self.finish()


def count_chart():
    plot = Plot(box=(.23, 6.09, -2.04, 2.24), xr=(0, 3), yr=(0, 120),
                yticks=[(0, "0"), (50, "50"), (100, "100")], size=28)
    unit = label("Neurons per lumbar hemisection", 3.17, 2.73, size=28)
    chart = VGroup(plot, unit, label("4 weeks after treatment", 3.17, 3.25, GREY, 28))
    bars = []
    for x, (name, mean, sem, color) in enumerate((("Control", 105, 4, GREY), ("Ablated", 17, 2, BLUE)), 1):
        foot, top = plot.pt(x, 0), plot.pt(x, mean)
        bar = Rectangle(width=1.05, height=top[1] - foot[1], stroke_color=color,
                        stroke_width=2.3, fill_color=color, fill_opacity=.65).move_to((foot + top) / 2)
        lo, hi = plot.pt(x, mean - sem), plot.pt(x, mean + sem)
        cap = RIGHT * .16
        whiskers = VGroup(Line(lo - cap, lo + cap), Line(lo, hi), Line(hi - cap, hi + cap)).set_stroke(TEXT, 3)
        value = T(str(mean), 30, TEXT)
        uncertainty = T(f"± {sem}", 30, TEXT)
        VGroup(value, uncertainty).arrange(RIGHT, buff=.10).next_to(hi, UP, buff=.18)
        name_label = label(name, foot[0], -2.40, size=28)
        bars.append((bar, value, VGroup(whiskers, uncertainty), name_label))
    return chart, bars


class S11UnlockedAblation(SpokenScene):
    def construct(self):
        circuit = Circuit()
        schematic = scope_tag(size=28)
        self.add(circuit, schematic)
        credit = label("Duan et al., 2014", -3.75, 3.18, GOLD, 29)
        line = label("Spinal somatostatin lineage", -3.75, 2.52, BLUE, 28)
        self.at("colleagues ablated spinal")
        self.play(circuit.animate.scale(.62).move_to(point(-3.78, .15)),
                  FadeIn(credit), FadeOut(schematic), run_time=1.2)
        self.play(FadeIn(line), FadeIn(schematic.move_to(point(-3.78, 2.02))), run_time=.56)
        drop = toxin(-4.24, 1.10)
        self.at("with diphtheria toxin")
        self.play(FadeIn(drop, shift=DOWN * .38), run_time=.6)
        removed = VGroup(circuit.cells[1], circuit.cells[2])
        self.play(FadeOut(drop, shift=DOWN * .26), removed.animate.fade(1),
                  FadeOut(circuit.signals[1]), FadeOut(circuit.signals[2]),
                  circuit.activity.animate.set_value(.17), run_time=1.15)
        chart, bars = count_chart()
        count = label("4 weeks later", 3.21, .48, TEXT, 36)
        self.at("weeks later tissue")
        self.play(FadeIn(count), run_time=.85)
        self.play(FadeOut(count), run_time=.6)
        self.play(FadeIn(chart), run_time=1.65)
        control, control_mean, control_error, control_name = bars[0]
        ablated, ablated_mean, ablated_error, ablated_name = bars[1]
        self.at("controls averaged 105")
        self.play(GrowFromEdge(control, DOWN), FadeIn(control_name), run_time=.55)
        self.play(FadeIn(control_mean), run_time=.16)
        self.at("minus 4 neurons")
        self.play(FadeIn(control_error), run_time=.66)
        self.at("ablated mice fell")
        self.play(GrowFromEdge(ablated, DOWN), FadeIn(ablated_name), run_time=.60)
        self.play(FadeIn(ablated_mean), run_time=.16)
        self.at("minus 2")
        self.play(FadeIn(ablated_error), run_time=.6)
        detail = label("Mean ± SEM · 3 mice per group", 2.69, -2.92, size=28)
        sections = label("15–17 lumbar hemisections", 2.33, -3.38, GREY, 28)
        self.at("across 3 mice")
        self.play(FadeIn(detail), FadeIn(sections), run_time=.65)
        response = ValueTracker(.78)
        gauge = dial(response, (-3.70, -2.36, 0), radius=.73, color=GREEN, fmt="↓", size=31)
        result = label("Defensive response", -3.70, -3.32, size=28)
        self.at("ablation impaired acute")
        self.play(FadeIn(gauge), FadeIn(result), run_time=.82)
        self.play(response.animate.set_value(.20), run_time=3.85)
        self.finish()


class S12UnlockedReversible(SpokenScene):
    def construct(self):
        circuit = Circuit()
        cups = receptors()
        dots = ligand_dots(cups)
        credit = label("Christensen et al., 2016", 4.48, 2.86, GOLD, 29)
        self.add(circuit, scope_tag(size=28))
        self.at("reversible tools strengthen", lead=0)
        self.play(FadeIn(cups), run_time=1.55)
        self.at("and colleagues used")
        self.play(FadeIn(credit), FadeIn(dots), run_time=.66)
        self.at("chemogenetic inhibition on")
        self.play(docking(cups, dots), *circuit.quiet(), run_time=3.75)
        self.play(FadeIn(label("Spinal somatostatin neurons", -1.31, 3.22, BLUE, 34)), run_time=.70)
        level = ValueTracker(.25)
        box = panel(4.50, -.09, 4.20, 4.98)
        mechanical = dial(level, (4.51, 1.28, 0), radius=.78, color=GREEN, fmt="↑", size=29)
        thermal = dial(level, (4.51, -1.26, 0), radius=.78, color=GREEN, fmt="↑", size=29)
        gauges = VGroup(box, mechanical, thermal, label("Mechanical threshold", 4.51, .32, size=28),
                        label("Thermal latency", 4.51, -2.28, size=28))
        self.at("mechanical withdrawal thresholds")
        self.play(FadeIn(gauges), run_time=.66)
        self.at("thresholds rose and")
        self.play(level.animate.set_value(.86), run_time=4.1)
        self.at("switching one genetic")
        self.play(FadeOut(dots, shift=UP * .25), FadeOut(gauges), *circuit.reactivate(), run_time=3.5)
        self.finish()


class S13End(EndCard):
    LINE = "Genetically switch one cell type on or off to test its role."
