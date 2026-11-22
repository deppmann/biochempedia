"""Following Tracers Along Axons, timed to the supplied narration.

Colour map: GREY for tissue and axons, BLUE for the pipette, cyan for
anterograde dye, ORANGE for retrograde dye, GOLD for bidirectional dye and
dates, PURPLE for one-step labelling, RED for unresolved functional questions.
GREEN, BLUE and PURPLE distinguish the three chick segment pairs.
"""

from bp_parts import *
from bp_style import EndCard

ORANGE = "#F29E4C"
PURPLE = "#B58CD9"
TISSUE = "#333D50"
FIBRE = "#68788E"
QUESTION = "Do axons enter or leave?"
CYAN_DYE = "#68DBED"


def point(x, y):
    return np.array([x, y, 0.0])


def label(text, x=0, y=3.04, color=TEXT, size=32):
    return T(text, size, color).move_to(point(x, y))


def schematic():
    return scope_tag(size=28, color=TEXT).move_to(point(5.53, -3.28))


def curve(a, b, c, d, color=FIBRE, width=3):
    return CubicBezier(a, b, c, d).set_stroke(color, width)


def tissue_outline():
    outline = VMobject().set_points_smoothly([
        point(-6.35, 0), point(-5.5, 2.33), point(-3.78, 2.45),
        point(-1.65, 1.15), point(0, 0.98), point(1.65, 1.15),
        point(3.78, 2.45), point(5.5, 2.33), point(6.35, 0),
        point(5.55, -2.25), point(3.75, -2.43), point(1.58, -1.24),
        point(0, -1.04), point(-1.58, -1.24), point(-3.75, -2.43),
        point(-5.55, -2.25), point(-6.35, 0),
    ])
    return outline.set_fill(TISSUE, 1).set_stroke(FIBRE, 2)


def soma(at, radius=0.22, color=GREY):
    rim = Circle(radius, stroke_color=color, stroke_width=2, fill_color=color, fill_opacity=0.24)
    nucleus = Dot(radius=radius * 0.33, color=color)
    return VGroup(rim, nucleus).move_to(at)


def terminals(at, side=1, color=GREY):
    branches = VGroup()
    for dy in (-0.14, 0.14):
        end = at + point(side * 0.28, dy)
        branch = Line(at - point(side * 0.13, 0), end, color=color, stroke_width=2)
        branches.add(branch, Dot(end, radius=0.042, color=color))
    return branches


def tract_world():
    """Return the common tissue, its fibres, and the two endpoint populations."""
    fibres, left, right = VGroup(), VGroup(), VGroup()
    for i, y in enumerate(np.linspace(-1.72, 1.64, 24)):
        offset = (i % 4) * 0.32
        a, b = point(-5.36 + offset, y), point(5.35 - offset, y * 0.96)
        fibres.add(curve(a, point(-1.45, 1.15 - y), point(1.65, -1.15 - y), b,
                         width=2.15 if i % 3 else 3.0))
        if i % 2 == 0:
            left.add(soma(a, 0.16 + offset * 0.065))
            right.add(terminals(b))
        else:
            left.add(terminals(a, side=-1))
            right.add(soma(b, 0.16 + offset * 0.065))
    return VGroup(tissue_outline(), fibres, left, right), fibres, left, right


def dim_tissue(world):
    world[0].fade(0.23)
    for structural_layer in world[1:]:
        structural_layer.fade(0.87)
    return world


def flow(paths, color, *, directions=None, travel=3.8, spread=True, radius=0.13):
    """Animate visible cargo along the actual drawn fibres."""
    directions = directions or [1] * len(paths)
    packets = VGroup()
    for index, (path, direction) in enumerate(zip(paths, directions)):
        packet = VGroup(
            Circle(radius * 2.8, stroke_width=0, fill_color=color, fill_opacity=0.43),
            Dot(radius=radius, color=color),
        )
        phase = index / len(paths) if spread else -index * 0.085
        packet.motion_time = 0.0

        def drift(mob, dt, path=path, direction=direction, phase=phase):
            mob.motion_time += dt
            position = (mob.motion_time / travel + phase) % 1
            mob.move_to(path.point_from_proportion(position if direction > 0 else 1 - position))
            envelope = min(1.0, 12 * position, 12 * (1 - position))
            mob[0].set_fill(opacity=0.43 * envelope)
            mob[1].set_fill(opacity=envelope)

        drift(packet, 0)
        packet.add_updater(drift)
        packets.add(packet)
    return packets


def light_paths(paths, color, width=5):
    return VGroup(*[path.copy().set_stroke(color, width, 0.85) for path in paths])


def pipette(tip):
    x, y, _ = tip
    return Polygon(point(x, y), point(x - 0.38, y + 1.12),
                   point(x - 0.08, y + 1.23), point(x + 0.06, y + 0.16),
                   stroke_color=BLUE, stroke_width=2.5, fill_color=BLUE, fill_opacity=0.37)


def pool(at, color, width=1.65, height=1.42):
    return VGroup(
        Ellipse(width=width, height=height, stroke_width=0, fill_color=color, fill_opacity=0.15),
        Ellipse(width=width * 0.77, height=height * 0.74, stroke_color=color,
                stroke_width=2.5, fill_color=color, fill_opacity=0.24),
        Ellipse(width=width * 0.47, height=height * 0.46, stroke_width=0,
                fill_color=color, fill_opacity=0.34),
    ).move_to(at)


def breathe_glow(patch):
    """Keep attention on the region being labelled while its outline stays fixed."""
    patch.glow_time = 0.0

    def update(mob, dt):
        mob.glow_time += dt
        strength = 0.5 - 0.5 * np.cos(2.5 * mob.glow_time)
        mob[0].set_fill(opacity=0.16 + 0.34 * strength)
        mob[1].set_fill(opacity=0.25 + 0.42 * strength)

    return patch.add_updater(update)


def arrival(cells, color):
    return VGroup(*[
        Dot(cell.get_center(), radius=0.28, color=color, fill_opacity=0.33, stroke_width=0)
        for cell in cells
    ])


class S01Hook(SpokenScene):
    def construct(self):
        world, fibres, _, _ = tract_world()
        cargo = flow(fibres[::2], GREY, travel=5.4, radius=0.142)
        question = label("?", y=2.01, color=GOLD, size=68)
        self.add(world, cargo)
        self.at("How do you map")
        self.play(FadeIn(question), run_time=0.45)
        bob(question, amp=0.10, speed=2.4)
        self.at("A neuron's long", lead=0.55)
        question.clear_updaters()
        self.play(FadeOut(question), run_time=0.3)
        axon = light_paths([fibres[12]], TEXT, 6)
        self.play(Create(axon), run_time=1.6)
        self.at("travels inside bundles")
        band = light_paths(fibres[8:16], GREY, 4)
        self.play(FadeIn(band), run_time=0.9)
        self.at("a neuron carries no")
        self.play(FadeOut(band), run_time=0.7)
        self.at("wiring stays hidden")
        self.play(FadeOut(axon), run_time=0.7)
        self.finish()


class S02Title(TitleCard):
    LESSON = "Neuronal tract tracing"
    TITLE = "Following Tracers Along Axons"

    def construct(self):
        world, fibres, _, _ = tract_world()
        cargo = flow(fibres[::2], GREY, travel=5.4, radius=0.142)
        title = fit_text(self.TITLE, max_w=10.1, size=51, min_size=40, font=TITLE_FONT)
        title.move_to(point(0, 3.02))
        lesson = T(self.LESSON, 28, GOLD).move_to(point(0, -3.09))
        words = VGroup(lesson, title)
        shade = Rectangle(width=13.2, height=5.35, stroke_width=0, fill_color=BG, fill_opacity=0.38)
        self.add(world, cargo)
        self.play(FadeIn(shade), FadeIn(words), run_time=0.30)
        self.wait(1.70)


class S03Anterograde(SpokenScene):
    def construct(self):
        world, fibres, _, right = tract_world()
        selected = fibres[2::4]
        cargo = flow(fibres[::2], GREY, travel=5.4, radius=0.142)
        self.at("Neurons already move")
        self.add(world, cargo)
        tip = point(-4.6, 0.64)
        tool = pipette(tip)
        dye = pool(tip + DOWN * 0.4, CYAN_DYE)
        dye_name = label("Biotinylated dextran amine", -3.18, color=CYAN_DYE)
        self.at("puts visible dye")
        self.play(FadeIn(tool, shift=DOWN * 0.65), run_time=1.15)
        self.at("Inject biotinylated")
        self.play(GrowFromPoint(dye, tip), run_time=0.7)
        pulse(dye[1], base=3, amp=1.6, speed=3.1)
        self.play(FadeIn(dye_name), run_time=0.38)
        self.at("near cell bodies")
        self.play(FadeOut(tool), run_time=0.42)
        self.at("Those neurons carry", lead=0.65)
        lit = light_paths(selected, CYAN_DYE)
        packets = flow(selected, CYAN_DYE, travel=2.55, spread=False, radius=0.17)
        self.remove(cargo)
        self.add(packets)
        self.play(Create(lit, lag_ratio=0.06), FadeOut(dye_name), run_time=2.35)
        self.at("their terminals")
        glow = arrival(right[2::4], CYAN_DYE)
        self.play(FadeIn(glow), run_time=0.65)
        self.at("called anterograde")
        self.play(FadeIn(label("Anterograde", color=CYAN_DYE, size=39)), run_time=0.45)
        self.finish()


class S04Retrograde(SpokenScene):
    def construct(self):
        world, fibres, left, right = tract_world()
        selected = fibres[2::4]
        prior = VGroup(light_paths(selected, CYAN_DYE),
                       pool(point(-4.6, 0.24), CYAN_DYE), arrival(right[2::4], CYAN_DYE),
                       label("Anterograde", color=CYAN_DYE, size=39))
        self.add(world, prior)
        self.at("Axon transport also")
        tool = pipette(point(4.82, 0.66))
        self.play(FadeOut(prior), run_time=0.48)
        cargo = flow(selected, GREY, directions=[-1] * len(selected), travel=4.7, radius=0.145)
        self.add(cargo)
        self.at("from terminals")
        self.play(FadeIn(tool, shift=DOWN * 0.65), run_time=1.05)
        self.at("Inject fluorogold")
        dye = pool(point(4.82, 0.26), ORANGE)
        self.play(GrowFromPoint(dye, point(4.82, 0.66)), run_time=0.7)
        pulse(dye[1], base=3, amp=1.6, speed=3.1)
        name = label("Fluorogold", 4.1, color=ORANGE)
        self.play(FadeIn(name), run_time=0.48)
        self.at("Terminals there absorb")
        lit = light_paths(selected, ORANGE)
        for path in lit:
            path.reverse_points()
        packets = flow(selected, ORANGE, directions=[-1] * len(selected), travel=2.7,
                       spread=False, radius=0.17)
        self.remove(cargo)
        self.add(packets)
        self.play(FadeOut(tool), FadeOut(name), Create(lit, lag_ratio=0.05), run_time=2.40)
        self.at("distant cell bodies")
        glow = arrival(left[2::4], ORANGE)
        self.play(FadeIn(glow), run_time=0.75)
        self.at("is retrograde tracing")
        heading = label("Retrograde", color=ORANGE, size=39)
        self.play(FadeIn(heading), run_time=0.48)
        self.at("hidden wiring")
        self.play(FadeOut(heading), lit.animate.set_stroke(width=6), run_time=0.8)
        self.finish()


def prediction_world():
    world, fibres, _, _ = tract_world()
    paths = VGroup(*[path.get_subcurve(0.5, 1) for path in fibres[::4]])
    return world, paths


def both_directions(color=GOLD):
    return VGroup(
        Arrow(point(0.58, 1.43), point(2.47, 1.43), color=color, buff=0,
              stroke_width=7, tip_length=0.24),
        Arrow(point(2.47, -1.43), point(0.58, -1.43), color=color, buff=0,
              stroke_width=7, tip_length=0.24),
    )


def prediction_result():
    return (pool(point(0, 0), GOLD, width=1.36, height=1.31),
            pool(point(4.75, -0.07), GOLD, width=2.65, height=3.55),
            both_directions())


class S05Predict(SpokenScene):
    def construct(self):
        world, paths = prediction_world()
        dye, patch, arrows = prediction_result()
        dye_name = label("Cholera toxin B subunit", color=GOLD)
        tool = pipette(point(0, 0.4)).shift(UP * 0.8)
        question = question_card(QUESTION, size=39)
        self.add(world)
        self.at("Now test that logic")
        cargo = flow(paths, GREY, directions=[1, -1] * 3, travel=3.1, radius=0.16)
        self.add(cargo)
        self.at("travels both ways")
        self.play(LaggedStart(*[GrowArrow(arrow) for arrow in arrows], lag_ratio=0.25), run_time=0.85)
        self.at("Suppose you inject", lead=0.48)
        self.play(FadeIn(tool), run_time=0.28)
        self.play(tool.animate.shift(DOWN * 0.8), run_time=0.62)
        self.play(GrowFromPoint(dye, point(0, 0.4)), run_time=0.55)
        self.remove(cargo)
        packets = flow(paths, GOLD, directions=[1, -1] * 3, travel=2.7, spread=False)
        self.add(packets)
        self.play(FadeIn(dye_name), FadeOut(tool), run_time=0.48)
        self.at("region glows")
        self.play(GrowFromCenter(patch), run_time=0.85)
        self.at("From that bright patch")
        self.play(FadeOut(dye_name), run_time=0.32)
        self.at("can you tell")
        self.play(FadeIn(question), run_time=0.48)
        self.finish()


class S06PredictPause(PredictPause):
    QUESTION = QUESTION
    CARD = {"size": 39}
    SECONDS = 4.5

    def backdrop(self):
        world, paths = prediction_world()
        packets = flow(paths, GOLD, directions=[1, -1] * 3, travel=4.5, radius=0.135)
        return VGroup(world, *prediction_result(), packets)

    def construct(self):
        self.add(self.backdrop(), question_card(self.QUESTION, **self.CARD))
        self.wait(self.SECONDS)


def direction_panels():
    panels = TwoPanel("Incoming terminals", "Outgoing cell bodies", colors=(GOLD, GOLD),
                      top=2.80, bottom=-2.08, width=12.3)
    paths, ends = [], []
    for side, direction in (("left", 1), ("right", -1)):
        a, b = point(-1.72, -0.45), point(1.72, 0.52)
        path = curve(a, point(-0.58, 0.63), point(0.45, -0.44), b, GOLD, 4)
        end = terminals(b, color=GOLD) if direction > 0 else soma(a, 0.44, GOLD)
        diagram = VGroup(path, end)
        panels.put(diagram, side)
        paths.append(path)
        ends.append(end)
    return panels, paths, ends


def population():
    world, fibres, left, right = tract_world()
    selected = fibres[::2]
    return world, selected, light_paths(selected, GOLD, 4.8), VGroup(
        arrival(left[::2], GOLD), arrival(right[::2], GOLD),
    )


class S07ControlsDye(SpokenScene):
    def construct(self):
        world, paths = prediction_world()
        opening = VGroup(*prediction_result(), question_card(QUESTION, size=39))
        self.add(world, opening)
        cargo = flow(paths, GOLD, directions=[1, -1] * 3, radius=0.13)
        self.add(cargo)
        panels, cases, ends = direction_panels()
        self.at("Not from the glow")
        self.play(FadeOut(opening[-1]), run_time=0.48)
        self.at("travels both ways")
        self.play(FadeOut(opening), FadeOut(world), FadeOut(cargo), run_time=0.56)
        self.play(FadeIn(panels), run_time=0.48)
        self.play(Create(cases[0]), FadeIn(ends[0]), run_time=0.95)
        self.at("researchers must establish")
        self.play(Create(cases[1]), FadeIn(ends[1]), run_time=0.95)
        case_flow = flow(cases, GOLD, directions=[1, -1], travel=2.25, radius=0.19)
        self.add(case_flow)
        self.at("injections carry a second")
        self.play(FadeOut(panels), FadeOut(VGroup(*cases, *ends)), FadeOut(case_flow), run_time=0.55)
        world, selected, lit, glow = population()
        dye = pool(point(-4.85, 0.13), GOLD)
        self.play(FadeIn(world), FadeIn(dye), run_time=0.65)
        self.at("They mark cells")
        packets = flow(selected, GOLD, travel=3.1, radius=0.14)
        self.add(packets)
        self.play(Create(lit, lag_ratio=0.075), run_time=2.45)
        self.at("reveals population wiring")
        self.play(FadeIn(glow), run_time=0.52)
        self.play(FadeIn(label("Population wiring only", color=GOLD)), run_time=0.51)
        self.finish()


def synaptic_world():
    """Two incoming axons end just outside the right-hand starter cell."""
    body = soma(point(3.93, 0), 0.98)
    incoming = VGroup(soma(point(-4.25, 1.22), 0.63), soma(point(-4.25, -1.22), 0.63))
    fibres = VGroup()
    for s in (1, -1):
        fibres.add(curve(point(-3.70, s * 1.1), point(-1.33, s * 1.47),
                         point(0.96, s * 0.66), point(2.74, s * 0.43), width=6))
    return body, incoming, fibres


class S08Rabies(SpokenScene):
    def construct(self):
        world, selected, lit, glow = population()
        previous = VGroup(lit, glow, pool(point(-4.85, 0.13), GOLD),
                          label("Population wiring only", color=GOLD))
        cargo = flow(selected, GOLD, travel=3.1, radius=0.14)
        self.add(world, previous, cargo)
        starter, inputs, paths = synaptic_world()
        self.at("pinpoint direct partners")
        self.play(FadeOut(previous), FadeOut(cargo), world.animate.become(dim_tissue(world.copy())), run_time=0.9)
        self.play(FadeIn(starter), run_time=0.7)
        self.play(Create(paths), FadeIn(inputs), run_time=2)
        self.at("A modified rabies virus")
        marker = Dot(starter.get_center(), radius=0.20, color=PURPLE)
        marker_halo = pool(starter.get_center(), PURPLE, width=2.07, height=2.08)
        self.play(GrowFromCenter(marker_halo), GrowFromCenter(marker), run_time=1.2)
        breathe_glow(marker_halo)
        virus = label("Modified rabies marker", color=PURPLE)
        self.play(FadeIn(virus), run_time=0.5)
        self.at("one starter cell")
        self.play(swap(virus, label("Starter cell", 3.92, 3.11)), run_time=0.7)
        self.at("Restricted to one synaptic step")
        gap = Ellipse(width=0.68, height=1.62, color=PURPLE, stroke_width=7,
                      fill_color=PURPLE, fill_opacity=0.16).move_to(point(2.94, 0))
        step = label("One synaptic step", -0.55, 2.98, color=PURPLE, size=37)
        self.play(GrowFromCenter(gap), run_time=0.42)
        forks = VGroup(*[Dot(marker.get_center(), radius=0.17, color=PURPLE) for _ in paths])
        self.add(forks)
        self.play(FadeIn(step), *[dot.animate.move_to(point(3.08, s * 0.43))
                                  for dot, s in zip(forks, (1, -1))], run_time=0.83)
        self.at("it crosses one synapse")
        self.play(FadeOut(gap), *[dot.animate.move_to(path.get_end()) for dot, path in zip(forks, paths)],
                  run_time=0.38)
        reverse = [path.copy().reverse_points() for path in paths]
        traced = light_paths(reverse, PURPLE, 12)
        self.play(Create(traced), *[MoveAlongPath(dot, path) for dot, path in zip(forks, reverse)],
                  run_time=1.63, rate_func=linear)
        self.at("the neurons that feed it")
        left_glow = VGroup(*[pool(cell.get_center(), PURPLE, width=1.85, height=1.85) for cell in inputs])
        self.play(FadeOut(forks), FadeOut(step), FadeIn(left_glow), run_time=0.8)
        for patch in left_glow:
            breathe_glow(patch)
        self.finish()


def mouse(color):
    body = Ellipse(width=0.72, height=0.40, stroke_color=color, stroke_width=2.5,
                   fill_color=color, fill_opacity=0.48)
    snout = Circle(0.19, stroke_color=color, stroke_width=2.5, fill_color=color,
                   fill_opacity=0.48).move_to(point(0.4, 0.07))
    ears = VGroup(Dot(point(0.30, 0.24), radius=0.09, color=color),
                  Dot(point(0.44, 0.23), radius=0.065, color=color))
    tail = curve(point(-0.33, -0.01), point(-0.60, -0.16),
                 point(-0.77, 0.08), point(-0.67, 0.2), color, 3)
    return VGroup(body, snout, ears, tail)


def gut_link():
    cell = RoundedRectangle(width=1.55, height=2.20, corner_radius=0.44,
                            stroke_color=GREY, stroke_width=3,
                            fill_color=TISSUE, fill_opacity=1).move_to(point(-4.25, 0.25))
    nucleus = Dot(cell.get_center(), radius=0.21, color=GREY)
    neuron = soma(point(3.93, 0.25), 0.91)
    path = curve(point(-3.17, 0.43), point(-1.08, 1.39),
                 point(0.55, -0.75), point(3.05, 0.25), PURPLE, 6)
    return VGroup(cell, nucleus), neuron, path


def ruled_out(text, x):
    wording = label(text, x, -2.87, TEXT, 29).set_opacity(0.8)
    strike = Line(wording.get_left() + LEFT * 0.13, wording.get_right() + RIGHT * 0.13,
                  color=RED, stroke_width=3)
    strike.layout_ok = "covered"
    return VGroup(wording, strike)


class S09LimitFunction(SpokenScene):
    def construct(self):
        world, _, _, _ = tract_world()
        dim_tissue(world)
        starter, inputs, paths = synaptic_world()
        prior = VGroup(starter, inputs, light_paths(paths, PURPLE, 12),
                       pool(starter.get_center(), PURPLE, 2.07, 2.08),
                       Dot(starter.get_center(), radius=0.2, color=PURPLE),
                       *[pool(cell.get_center(), PURPLE, 1.85, 1.85) for cell in inputs])
        starter_label = label("Starter cell", 3.92, 3.11)
        for glow in (prior[3], prior[5], prior[6]):
            breathe_glow(glow)
        self.add(world, prior, starter_label)
        self.at("has a strict limit")
        self.play(FadeOut(starter_label), run_time=0.45)
        cell, neuron, path = gut_link()
        self.at("In mice")
        self.play(FadeOut(prior), FadeIn(cell), FadeIn(neuron), run_time=0.8)
        self.play(Create(path), run_time=1.65)
        cargo = flow([path, path, path], PURPLE, directions=[-1, -1, -1], travel=2.55, radius=0.18)
        self.add(cargo)
        self.at("gut lining cells")
        cell_name = label("Gut-lining cell", -4.25, 2.93)
        neuron_name = label("Vagal sensory neuron", 3.85, 3.14)
        self.play(FadeIn(cell_name), run_time=0.40)
        self.at("vagal sensory neurons")
        self.play(FadeIn(neuron_name), run_time=0.40)
        icons = VGroup(*[mouse(GREY) for _ in range(5)]).arrange(RIGHT, buff=0.23).move_to(point(-2.52, -2.02))
        self.at("Labeling reach them")
        self.play(LaggedStart(*[FadeIn(icon, shift=UP * 0.13) for icon in icons], lag_ratio=0.18), run_time=1.13)
        self.at("two of five mice")
        bright = VGroup(*[mouse(PURPLE).move_to(icon) for icon in icons[:2]])
        self.play(Transform(icons[0], bright[0]), Transform(icons[1], bright[1]), run_time=0.55)
        count = caption("2 of 5, infected colon nerves", y=-2.98, size=30).set_x(-3.42)
        self.at("infected colon nerves")
        self.play(FadeIn(count), FadeIn(schematic().move_to(point(0, 2.93))), run_time=0.5)
        self.at("shows a connection")
        self.play(path.animate.set_stroke(width=9), run_time=0.65)
        for phrase, question, x in (("the transmitter", "Transmitter?", 1.94),
                                    ("behavioral role", "Behaviour?", 4.76)):
            self.at(phrase)
            mark = ruled_out(question, x)
            self.play(FadeIn(mark[0]), run_time=0.23)
            self.play(Create(mark[1]), run_time=0.28)
        self.finish()


def station(x, y, color=GREY, radius=0.93):
    at = point(x, y)
    outer = Circle(radius, stroke_color=color, stroke_width=2.6,
                   fill_color=color, fill_opacity=0.23).move_to(at)
    cells = VGroup(*[soma(at + point(np.cos(a), np.sin(a)) * radius * 0.56, radius * 0.16, color)
                     for a in np.linspace(0, TAU, 7, endpoint=False)])
    return VGroup(outer, cells)


def song_world():
    nodes = VGroup(station(-4.48, 0.46), station(0, 0.12), station(4.48, -0.44))
    tracts = VGroup()
    for i in range(2):
        a, b = nodes[i].get_center() + RIGHT * 0.85, nodes[i + 1].get_center() + LEFT * 0.85
        bundle = VGroup(*[curve(a + UP * offset, a + point(0.84, 0.42 + offset),
                                b + point(-0.84, -0.42 + offset), b + UP * offset, width=3.7)
                          for offset in np.linspace(-0.30, 0.30, 5)])
        tracts.add(bundle)
    return nodes, tracts


def song_labels():
    return VGroup(label("HVC", -4.48, 2.00, size=34), label("RA", 0, 1.66, size=34),
                  label("Vocal motor neurons", 4.36, -2.78, size=30))


def source(text):
    return label(text, x=-3.0, y=-3.10, color=GOLD, size=28)


class S10UnlockedSong(SpokenScene):
    def construct(self):
        world, _, _, _ = tract_world()
        dim_tissue(world)
        cell, neuron, gut_path = gut_link()
        self.add(world, cell, neuron, gut_path)
        cargo = flow([gut_path] * 3, PURPLE, directions=[-1] * 3, travel=2.55)
        self.add(cargo)
        self.at("circuit mapping unlocked")
        nodes, tracts = song_world()
        self.play(FadeOut(cargo), FadeOut(gut_path), ReplacementTransform(cell, nodes[0]),
                  ReplacementTransform(neuron, nodes[2]), run_time=1.55)
        self.play(GrowFromCenter(nodes[1]), run_time=0.7)
        self.at("In 1976")
        self.play(FadeIn(source("Nottebohm, Stokes & Leonard, 1976")), FadeIn(schematic()), run_time=0.52)
        self.at("Fernando")
        tracts[0].set_stroke(GREY, width=6.2)
        self.play(Create(tracts[0]), run_time=2.95)
        first_cargo = flow(tracts[0], GREY, travel=2.15, radius=0.17)
        self.add(first_cargo)
        self.at("adult canary")
        tracts[1].set_stroke(GREY, width=6.2)
        self.play(Create(tracts[1]), run_time=1.34)
        second_cargo = flow(tracts[1], GREY, travel=2.15, radius=0.17)
        self.add(second_cargo)
        names = song_labels()
        self.at("cluster HVC")
        self.play(FadeIn(names[0]), run_time=0.35)
        self.at("projects to a second", lead=0.52)
        first = light_paths(tracts[0], TEAL, 5)
        self.remove(first_cargo)
        self.add(flow(tracts[0], TEAL, travel=2.15, radius=0.135))
        self.play(Create(first), run_time=1.2)
        self.at("cluster RA", lead=0.25)
        self.play(FadeIn(names[1]), run_time=0.46)
        self.at("RA reaches brainstem")
        second = light_paths(tracts[1], TEAL, 5)
        self.remove(second_cargo)
        self.add(flow(tracts[1], TEAL, travel=2.15, radius=0.135))
        self.play(Create(second), run_time=1.22)
        self.at("motor neurons of")
        self.play(FadeIn(names[2]), run_time=0.49)
        self.finish()


PAIR_COLORS = (TEAL, PURPLE, GREEN)
MUSCLES = ("Jaw", "Face", "Throat")


def hindbrain_world():
    pairs = VGroup()
    routes = VGroup()
    for i, x in enumerate((-3.95, 0, 3.95)):
        pair = VGroup(*[
            RoundedRectangle(width=1.20, height=2.45, corner_radius=0.34, stroke_color=GREY,
                             stroke_width=2.8, fill_color=TISSUE, fill_opacity=1)
            .move_to(point(x + dx, 1.08))
            for dx in (-0.68, 0.68)
        ])
        pairs.add(pair)
        routes.add(VGroup(*[
            curve(point(x + dx, 0.01), point(x + dx * 1.2, -0.45),
                  point(x + dx * 0.42, -0.97), point(x + dx * 0.26, -1.48),
                  width=5)
            for dx in (-0.68, 0.68)
        ]))
    return pairs, routes


class S11UnlockedHindbrain(SpokenScene):
    def construct(self):
        world, _, _, _ = tract_world()
        dim_tissue(world)
        nodes, tracts = song_world()
        song = VGroup(*[light_paths(tract, TEAL, 5) for tract in tracts])
        names = song_labels()
        pairs, routes = hindbrain_world()
        self.add(world, nodes, song, names)
        self.at("In 1989")
        self.play(FadeOut(names), FadeOut(song), run_time=0.48)
        self.play(*[ReplacementTransform(node, pair) for node, pair in zip(nodes, pairs)], run_time=1.63)
        self.play(FadeIn(source("Lumsden & Keynes, 1989").move_to(point(-3.50, 3.03))),
                  FadeIn(schematic().move_to(point(4.92, -3.46))), run_time=0.54)
        self.at("mapped cranial motor neurons")
        self.play(LaggedStart(*[Create(bundle) for bundle in routes], lag_ratio=0.53), run_time=3.55)
        motor_flow = flow([path.get_subcurve(0.20, 1) for bundle in routes for path in bundle], GREY,
                          travel=2.4, radius=0.16)
        self.add(motor_flow)
        self.at("muscles of the jaw")
        words = VGroup(*[label(name, x, -2.92, size=32)
                         for name, x in zip(MUSCLES, (-3.95, 0, 3.95))])
        self.play(FadeIn(words[0]), run_time=0.45)
        self.at("face and throat")
        self.play(LaggedStart(FadeIn(words[1]), FadeIn(words[2]), lag_ratio=0.65), run_time=0.80)
        self.at("Mapping their origins")
        self.remove(motor_flow)
        for pair, route, color in zip(pairs, routes, PAIR_COLORS):
            self.play(pair.animate.set_fill(color, 0.42).set_stroke(color, 3.2),
                      route.animate.set_stroke(color, 6), run_time=1.12)
        for bundle, color in zip(routes, PAIR_COLORS):
            self.add(flow(bundle, color, travel=2.2, radius=0.135))
        self.finish()


def eye(x, closed=False):
    a, b = point(x - 0.83, 2.08), point(x + 0.83, 2.08)
    if closed:
        return VGroup(curve(a, point(x - 0.37, 1.65), point(x + 0.37, 1.65), b, GREY, 5))
    rim = VMobject().set_points_smoothly([a, point(x, 2.56), b, point(x, 1.60), a])
    rim.set_fill(BLUE, 0.22).set_stroke(BLUE, 4)
    pupil = Dot(point(x, 2.08), radius=0.245, color=BLUE)
    return VGroup(rim, pupil)


def cortex_stripes(bias=0):
    stripes = VGroup()
    x = -5.64
    for i in range(10):
        width = 1.128 + (bias if i % 2 == 0 else -bias)
        color = BLUE if i % 2 == 0 else PURPLE
        stripes.add(Rectangle(width=width - 0.06, height=2.56,
                              stroke_color=color, stroke_width=1.8,
                              fill_color=color, fill_opacity=0.49 if i % 2 == 0 else 0.38)
                    .move_to(point(x + width / 2, -0.92)))
        x += width
    return stripes


def eye_fibres(stripes):
    paths = VGroup()
    for i, stripe in enumerate(stripes):
        x = -3.72 if i % 2 == 0 else 3.72
        start = point(x, 1.50)
        end = stripe.get_top()
        paths.add(curve(start, start + DOWN * 0.58, end + UP * 0.28, end,
                        BLUE if i % 2 == 0 else PURPLE, 3))
    return paths


class S12UnlockedVision(SpokenScene):
    def construct(self):
        world, _, _, _ = tract_world()
        dim_tissue(world)
        pairs, routes = hindbrain_world()
        for pair, route, color in zip(pairs, routes, PAIR_COLORS):
            pair.set_fill(color, 0.42).set_stroke(color, 3.2)
            route.set_stroke(color, 6)
        self.add(world, pairs, routes)
        stripes = cortex_stripes()
        eyes = VGroup(eye(-3.72), eye(3.72))
        pathways = eye_fibres(stripes)
        self.at("And David Hubel")
        self.play(FadeOut(pairs), FadeOut(routes), FadeIn(eyes), run_time=1.4)
        self.play(FadeIn(source("Hubel, Wiesel & LeVay")), FadeIn(schematic()), run_time=0.6)
        self.at("closed one eye")
        self.play(Transform(eyes[1], eye(3.72, closed=True)), run_time=0.62)
        self.play(Create(pathways, lag_ratio=0.07), run_time=2.2)
        self.at("Tracing stripes")
        self.play(FadeIn(stripes, lag_ratio=0.1), run_time=1.54)
        self.play(FadeIn(label("Visual cortex", 0, -2.61)), run_time=0.48)
        self.at("stripes widened", lead=0.46)
        self.add(flow(pathways[::2], BLUE, travel=2.15, radius=0.18))
        expanded = cortex_stripes(0.53)
        target_paths = eye_fibres(expanded)
        for path in target_paths[1::2]:
            path.set_stroke(opacity=0.34)
        self.play(Transform(stripes, expanded), Transform(pathways, target_paths), run_time=2.76)
        self.at("Across brains")
        self.play(stripes[::2].animate.set_fill(BLUE, 0.74), run_time=1.48)
        self.at("turns hidden wiring")
        network = light_paths(pathways[::2], BLUE, 4.8)
        self.play(Create(network, lag_ratio=0.16), run_time=2.05)
        self.finish()


class S13End(EndCard):
    LINE = "Axon transport carries tracers to map connections; function takes separate tests."
