"""How a scaffold keeps signals on route.

COLOR MAP (continued exactly from chapter 1)
  BLUE    input / receptor cue
  GREEN   organizer / scaffold
  ORANGE  enzyme / kinase
  PURPLE  output
  GOLD    activation pulse
  GREY    membrane / inactive routes

All pathway pictures are explicitly schematic. Proteins are labelled blocks; no
molecular structures are drawn.
"""
from bp_parts import *  # noqa: F401,F403


ORANGE = "#F29E4C"
PURPLE = "#B58CD9"

MEM_Y = 2.82
ROUTE_Y = 0.20
KINASE_X = (-1.45, 0.85, 3.15)


def breathe_fill(mob, color=GREEN, base=0.22, amp=0.07, speed=1.35, seed=0):
    """Continuous low-frequency organizer motion across a visibly large area."""
    mob._breath_t = seed * 0.65

    def update(m, dt):
        m._breath_t += dt
        m.set_fill(color, opacity=base + amp * np.sin(speed * m._breath_t))

    return mob.add_updater(update)


def protein_block(name, center, color=ORANGE, output=False, scale=1.0, dim=False):
    """One labelled protein block; output kinases carry a purple outer stroke."""
    lab = T(name, max(24, 31 * scale), color if not dim else GREY,
            weight=BOLD)
    width = max(1.72 * scale, lab.width + 0.48)
    height = max(0.94 * scale, lab.height + 0.34)
    rect = RoundedRectangle(
        corner_radius=0.20, width=width, height=height,
        stroke_color=PURPLE if output else color, stroke_width=6 if output else 3.5,
        fill_color=color, fill_opacity=0.34 if not dim else 0.10,
    ).move_to(center)
    lab.move_to(rect)
    g = VGroup(rect, lab)
    g.box, g.label = rect, lab
    if dim:
        g.set_opacity(0.48)
    return g


def input_block(text="pheromone", center=(-5.35, ROUTE_Y, 0), dim=False):
    g = boxed_label(text, BLUE if not dim else GREY, size=29,
                    box=(2.10, 0.96), fill_opacity=0.30 if not dim else 0.09)
    g.move_to(center)
    if dim:
        g.set_opacity(0.48)
    return g


def membrane():
    """The common membrane, kept below the top-right brand-mark exclusion."""
    return RoundedRectangle(
        corner_radius=0.10, width=12.25, height=0.38,
        stroke_color=GREY, stroke_width=3, fill_color=GREY, fill_opacity=0.32,
    ).move_to([0, MEM_Y, 0])


def connector(a, b, color=GREY, width=5, opacity=1.0):
    """A route segment that stops at block edges rather than crossing labels."""
    line = Line(a, b, color=color, stroke_width=width)
    line.set_opacity(opacity)
    return line


def route_row(y=ROUTE_Y, scaffold=False, dim=False, names=("Ste11", "Ste7", "Fus3"),
              input_name="pheromone", output_ring=True):
    """Canonical left-to-right mating route at fixed coordinates."""
    inp = input_block(input_name, (-5.35, y, 0), dim=dim)
    blocks = VGroup(
        protein_block(names[0], (KINASE_X[0], y, 0), dim=dim),
        protein_block(names[1], (KINASE_X[1], y, 0), dim=dim),
        protein_block(names[2], (KINASE_X[2], y, 0), output=output_ring, dim=dim),
    )
    links = VGroup(
        connector(inp.get_right() + RIGHT * 0.04, blocks[0].get_left() + LEFT * 0.04,
                  BLUE if not dim else GREY, opacity=0.75 if not dim else 0.35),
        connector(blocks[0].get_right() + RIGHT * 0.04, blocks[1].get_left() + LEFT * 0.04,
                  GREY, opacity=0.75 if not dim else 0.35),
        connector(blocks[1].get_right() + RIGHT * 0.04, blocks[2].get_left() + LEFT * 0.04,
                  GREY, opacity=0.75 if not dim else 0.35),
    )
    g = VGroup(links, inp, blocks)
    g.input, g.blocks, g.links = inp, blocks, links
    g.rail = None
    if scaffold:
        rail = scaffold_rail(y)
        g.add_to_back(rail)
        g.rail = rail
    return g


def scaffold_rail(y=ROUTE_Y, open_shape=True):
    """The carried Ste5 picture: one green organizer with three irregular slots."""
    if open_shape:
        field = RoundedRectangle(
            corner_radius=0.34, width=7.55, height=1.48,
            stroke_opacity=0, fill_color=GREEN, fill_opacity=0.22,
        ).move_to([0.82, y, 0])
        breathe_fill(field)
        rail = Line([-2.65, y - 0.68, 0], [4.25, y - 0.68, 0],
                    color=GREEN, stroke_width=11)
        pulse(rail, base=11, amp=2.6, speed=1.7)
        slots = VGroup(*[
            Line([x, y - 0.68, 0], [x, y - 0.53, 0], color=GREEN, stroke_width=7)
            for x in KINASE_X
        ])
        label = boxed_label("Ste5 · organizer", GREEN, size=28).move_to([0.82, y - 1.43, 0])
        g = VGroup(field, rail, slots, label)
        g.field, g.body, g.slots, g.label = field, rail, slots, label
        return g

    left = Arc(radius=1.55, start_angle=35 * DEGREES, angle=290 * DEGREES,
               color=GREEN, stroke_width=11).move_to([0.75, -0.02, 0])
    pulse(left, base=11, amp=2.6, speed=1.7)
    label = boxed_label("Ste5 · closed", GREEN, size=28).move_to([0.75, -2.03, 0])
    g = VGroup(left, label)
    g.body, g.label = left, label
    return g


def route_pulse(a, b, color=GOLD):
    dot = Dot(a, radius=0.15, color=color)
    return dot, dot.animate.move_to(b)


def fork_picture(scaffold=True):
    """The canonical shared-part fork used by the hook and payoff."""
    shared = protein_block("shared kinase", (-0.65, 0.15, 0), scale=1.08)
    inp = input_block("input", (-4.95, 0.15, 0))
    outputs = VGroup(
        protein_block("output A", (4.35, 1.58, 0), color=PURPLE, output=True, dim=True),
        protein_block("Fus3", (4.35, 0.15, 0), output=True),
        protein_block("output B", (4.35, -1.28, 0), color=PURPLE, output=True, dim=True),
    )
    links = VGroup(
        connector(inp.get_right(), shared.get_left(), BLUE, 6),
        connector(shared.get_right(), outputs[0].get_left(), GREY, 5, 0.42),
        connector(shared.get_right(), outputs[1].get_left(), GREY, 5, 0.85),
        connector(shared.get_right(), outputs[2].get_left(), GREY, 5, 0.42),
    )
    g = VGroup(links, inp, shared, outputs)
    g.input, g.shared, g.outputs, g.links = inp, shared, outputs, links
    g.organizer = None
    if scaffold:
        field = RoundedRectangle(corner_radius=0.30, width=7.25, height=1.22,
                                 stroke_opacity=0, fill_color=GREEN,
                                 fill_opacity=0.22).move_to([1.72, 0.15, 0])
        breathe_fill(field)
        org = VGroup(
            field,
            Line([-1.72, -0.58, 0], [5.28, -0.58, 0], color=GREEN, stroke_width=8),
            Line([-1.72, -0.58, 0], [-1.72, -0.35, 0], color=GREEN, stroke_width=8),
            Line([5.28, -0.58, 0], [5.28, -0.35, 0], color=GREEN, stroke_width=8),
        )
        for line in org[1:]:
            pulse(line, base=8, amp=2.0, speed=1.7)
        for line in org:
            pulse(line, base=8, amp=2.0, speed=1.7)
        g.add_to_back(org)
        g.organizer = org
    return g


def mini_scaffold(center, complete=False):
    """A compact Ste5 used only for the scaffold-excess prediction."""
    c = np.array(center, dtype=float)
    rail = RoundedRectangle(corner_radius=0.24, width=3.02, height=0.72,
                            stroke_color=GREEN, stroke_width=5,
                            fill_color=GREEN, fill_opacity=0.25).move_to(c)
    breathe_fill(rail, base=0.25, amp=0.08, speed=1.25, seed=int(abs(c[0]) * 3 + abs(c[1])))
    # Invisible anchors preserve three distinct landing positions without drawing
    # slot marks through the compact kinase labels.
    slots = VGroup(*[VectorizedPoint(c + RIGHT * dx) for dx in (-0.92, 0, 0.92)])
    g = VGroup(rail, slots)
    g.rail, g.slots = rail, slots
    g.blocks = VGroup()
    if complete:
        for name, dx, output in (("11", -0.92, False), ("7", 0, False), ("3", 0.92, True)):
            b = protein_block(name, c + RIGHT * dx, output=output, scale=0.45)
            g.blocks.add(b)
        g.add(g.blocks)
    return g


PREDICT_Q = "Must complete assemblies keep rising?"


def prediction_backdrop(complete=True, drifting=False):
    centers = [(-3.65, 1.22, 0), (0, 1.22, 0), (3.65, 1.22, 0),
               (-1.82, -0.15, 0), (1.82, -0.15, 0)]
    scaffolds = VGroup(*[mini_scaffold(c, complete=(complete and i == 2))
                         for i, c in enumerate(centers)])
    kinases = VGroup(
        protein_block("11", (-1.35, 2.38, 0), scale=0.45),
        protein_block("7", (0, 2.38, 0), scale=0.45),
        protein_block("3", (1.35, 2.38, 0), output=True, scale=0.45),
    )
    if drifting:
        for i, s in enumerate(scaffolds):
            bob(s, amp=0.035, speed=1.3 + 0.08 * i, seed=i)
        for i, k in enumerate(kinases):
            bob(k, amp=0.05, speed=1.5, seed=i + 7)
    g = VGroup(scaffolds, kinases)
    g.scaffolds, g.kinases = scaffolds, kinases
    return g


class S00Hook(SpokenScene):
    def construct(self):
        old = VGroup(
            boxed_label("receptor", BLUE, 28).move_to([-3.9, 0.25, 0]),
            boxed_label("Grb2", GREEN, 28).move_to([-1.25, 0.25, 0]),
            boxed_label("Sos", ORANGE, 28).move_to([1.15, 0.25, 0]),
            protein_block("Ras", (3.85, 0.25, 0), color=PURPLE, output=True),
        )
        old_links = VGroup(*[connector(old[i].get_right(), old[i + 1].get_left(), GREY, 5)
                             for i in range(3)])
        tag = scope_tag()
        self.play(FadeIn(old_links), FadeIn(old), FadeIn(tag), run_time=0.8)
        self.at("But what if")
        fork = fork_picture(scaffold=False)
        self.play(Succession(FadeOut(VGroup(old_links, old), run_time=0.55),
                             FadeIn(fork, run_time=1.15)))
        self.at("share the same kinase")
        self.play(Indicate(fork.shared, color=ORANGE, scale_factor=1.10), run_time=1.2)
        self.at("Follow the same colors")
        self.play(Indicate(fork.input, color=BLUE), run_time=0.8)
        self.at("one orange kinase")
        self.play(fork.shared.animate.shift(UP * 0.12), rate_func=there_and_back, run_time=1.4)
        self.at("two possible purple outputs")
        self.play(LaggedStart(*[Indicate(o, color=PURPLE, scale_factor=1.07)
                                for o in fork.outputs], lag_ratio=0.25), run_time=1.5)
        self.finish()


class S01Title(TitleCard):
    LESSON = "Adaptors and Scaffolds"
    TITLE = "How a Scaffold Keeps Signals on Route"


class S02Problem(SpokenScene):
    def construct(self):
        route = route_row(scaffold=False)
        top = protein_block("other output", (4.65, 1.72, 0), color=PURPLE,
                            output=True, dim=True)
        bottom = protein_block("other output", (4.65, -1.42, 0), color=PURPLE,
                               output=True, dim=True)
        branches = VGroup(
            connector(route.blocks[1].get_right(), top.get_left(), GREY, 4, 0.38),
            connector(route.blocks[1].get_right(), bottom.get_left(), GREY, 4, 0.38),
            top, bottom,
        )
        self.play(FadeIn(route.input), Create(route.links[0]), run_time=0.8)
        self.at("kinase root")
        self.play(FadeIn(route.blocks), FadeIn(route.links[1:]), run_time=1.3)
        self.at("ending in fuss")
        self.play(Indicate(route.blocks[2], color=PURPLE), FadeIn(scope_tag()), run_time=0.9)
        self.at("also serve other responses")
        self.play(FadeIn(branches), run_time=1.2)
        self.at("A pheromone input")
        dot, move = route_pulse(route.input.get_right() + DOWN * 0.75,
                                route.blocks[1].get_center() + DOWN * 0.75)
        self.add(dot)
        self.play(move, run_time=2.0)
        self.at("without making the cell")
        self.play(dot.animate.shift(UP * 0.38), rate_func=there_and_back, run_time=1.5)
        self.at("shares a part")
        self.play(Indicate(route.blocks[1], color=ORANGE), run_time=1.0)
        self.finish()


class S02Shared(SpokenScene):
    def construct(self):
        fork = fork_picture(scaffold=False)
        fork.shared.label.set_opacity(0)
        self.add(fork, scope_tag())
        self.play(Rotate(fork.shared, angle=TAU, run_time=2.6, rate_func=linear))
        self.at("does not carry a label")
        q = T("?", 58, ORANGE, weight=BOLD).move_to(fork.shared)
        self.play(FadeIn(q), run_time=0.7)
        self.at("partners around it")
        self.play(LaggedStart(*[Indicate(o, color=PURPLE, scale_factor=1.06)
                                for o in fork.outputs], lag_ratio=0.2), run_time=1.5)
        self.at("needs an organizer")
        field = RoundedRectangle(corner_radius=0.30, width=7.25, height=1.22,
                                 stroke_opacity=0, fill_color=GREEN,
                                 fill_opacity=0.22).move_to([1.72, 0.15, 0])
        breathe_fill(field)
        org = VGroup(
            field,
            Line([-1.72, -0.58, 0], [5.28, -0.58, 0], color=GREEN, stroke_width=8),
            Line([-1.72, -0.58, 0], [-1.72, -0.35, 0], color=GREEN, stroke_width=8),
            Line([5.28, -0.58, 0], [5.28, -0.35, 0], color=GREEN, stroke_width=8),
        )
        self.play(Create(org), run_time=1.4)
        self.at("under the mating input")
        m = membrane()
        target = VGroup(org, fork.input, fork.shared, fork.outputs[1], fork.links[0], fork.links[2])
        self.play(FadeOut(fork.outputs[0]), FadeOut(fork.outputs[2]),
                  FadeOut(fork.links[1]), FadeOut(fork.links[3]),
                  FadeIn(m), target.animate.shift(UP * 1.25), run_time=1.7)
        self.finish()


class S03Assembly(SpokenScene):
    def construct(self):
        rail = scaffold_rail()
        blocks = VGroup(
            protein_block("Ste11", (-4.25, 2.05, 0)),
            protein_block("Ste7", (0.15, 2.05, 0)),
            protein_block("Fus3", (4.45, 2.05, 0), output=True),
        )
        self.play(FadeIn(rail.field), Create(rail.body), FadeIn(rail.label), run_time=1.2)
        self.at("no enzyme activity")
        no_enzyme = boxed_label("no enzyme activity", GREY, 28).move_to([-4.45, -2.05, 0])
        self.play(FadeIn(no_enzyme), run_time=0.8)
        self.at("Different regions bind")
        self.play(LaggedStart(*[Create(s) for s in rail.slots], lag_ratio=0.22), run_time=1.1)
        self.at("STI")
        targets = [(-1.45, ROUTE_Y, 0), (0.85, ROUTE_Y, 0), (3.15, ROUTE_Y, 0)]
        self.play(LaggedStart(*[b.animate.move_to(t) for b, t in zip(blocks, targets)],
                              lag_ratio=0.22), run_time=2.1)
        self.at("hold all three")
        self.play(Indicate(VGroup(rail.body, blocks), color=GREEN, scale_factor=1.03), run_time=1.2)
        self.at("productive encounters")
        pulse_lines = VGroup(
            connector(blocks[0].get_right() + RIGHT * 0.05,
                      blocks[1].get_left() + LEFT * 0.05, GOLD, 10),
            connector(blocks[1].get_right() + RIGHT * 0.05,
                      blocks[2].get_left() + LEFT * 0.05, GOLD, 10),
        )
        self.play(FadeOut(no_enzyme),
                  LaggedStart(*[Create(x) for x in pulse_lines], lag_ratio=0.35), run_time=1.8)
        self.finish()


class S03Order(SpokenScene):
    def construct(self):
        route = route_row(scaffold=True)
        for i, block in enumerate(route.blocks):
            bob(block, amp=0.09, speed=3.2, seed=i)
        self.add(route, scope_tag())
        self.at("activates STI")
        flash1 = connector(route.blocks[0].get_right() + RIGHT * 0.05,
                           route.blocks[1].get_left() + LEFT * 0.05, GOLD, 10)
        self.play(Create(flash1),
                  route.blocks[1].box.animate.set_fill(ORANGE, 0.52),
                  route.blocks[1].label.animate.set_color(TEXT), run_time=1.2)
        self.at("activates FUS")
        flash2 = connector(route.blocks[1].get_right() + RIGHT * 0.05,
                           route.blocks[2].get_left() + LEFT * 0.05, GOLD, 10)
        self.play(Create(flash2),
                  route.blocks[2].box.animate.set_fill(ORANGE, 0.52),
                  route.blocks[2].label.animate.set_color(TEXT), run_time=1.2)
        self.at("prepare the cell for mating")
        output = boxed_label("mating response", PURPLE, 30).move_to([4.85, -1.48, 0])
        self.play(FadeIn(output, shift=LEFT * 0.25), run_time=1.2)
        self.at("does not perform")
        self.play(route.rail.body.animate.set_stroke(width=5), rate_func=there_and_back, run_time=1.4)
        self.at("It organizes")
        self.play(Indicate(route.rail.label, color=GREEN), run_time=1.0)
        self.at("proteins that do")
        self.play(LaggedStart(*[Indicate(b, color=ORANGE) for b in route.blocks],
                              lag_ratio=0.22), run_time=1.3)
        self.finish()


class S04Refine(SpokenScene):
    def construct(self):
        closed = scaffold_rail(open_shape=False)
        m = membrane()
        cue = input_block("pheromone", (-4.75, 2.05, 0))
        self.play(FadeIn(closed), run_time=1.0)
        self.at("only the first model")
        first = boxed_label("proximity", GREY, 28).move_to([-3.9, -1.95, 0])
        self.play(FadeIn(first), closed.body.animate.rotate(0.22), run_time=1.0)
        self.at("pheromone linked recruitment")
        self.play(FadeIn(m), FadeIn(cue), closed.animate.shift(UP * 1.15), run_time=1.7)
        self.at("shape opens there")
        open_rail = scaffold_rail(y=1.15)
        self.play(FadeOut(first), ReplacementTransform(closed, open_rail), run_time=1.5)
        self.at("domain also helps")
        ste7 = protein_block("Ste7", (0.85, 1.15, 0))
        fus3 = protein_block("Fus3", (3.15, 1.15, 0), output=True)
        gate = VGroup(
            Line([0.20, 0.50, 0], [3.80, 0.50, 0], color=GREEN, stroke_width=8),
            Line([0.20, 0.50, 0], [0.20, 0.72, 0], color=GREEN, stroke_width=8),
            Line([3.80, 0.50, 0], [3.80, 0.72, 0], color=GREEN, stroke_width=8),
        )
        self.play(FadeIn(ste7), FadeIn(fus3), Create(gate), run_time=1.2)
        self.at("activate FUS")
        self.play(ste7.animate.shift(RIGHT * 0.22), fus3.animate.shift(LEFT * 0.22), run_time=1.3)
        self.at("poor substrate")
        flash = connector(ste7.get_right(), fus3.get_left(), GOLD, 10)
        self.play(Create(flash), run_time=1.0)
        self.finish()


class S05Specificity(SpokenScene):
    def construct(self):
        route = route_row(y=1.05, scaffold=True)
        bob(route.input, amp=0.09, speed=3.0)
        bob(route.blocks[2], amp=0.09, speed=3.2, seed=2)
        bob(route.rail.label, amp=0.08, speed=3.1, seed=4)
        m = membrane()
        self.add(m, route, scope_tag())
        self.at("helps select an output")
        dot = Dot(route.input.get_right() + DOWN * 0.76, radius=0.16, color=GOLD)
        self.add(dot)
        self.play(dot.animate.move_to(route.blocks[2].get_center() + DOWN * 0.76), run_time=2.0)
        self.play(Indicate(route.blocks[2], color=PURPLE), run_time=0.8)
        self.at("controls partners")
        labels = VGroup(
            boxed_label("partners", GREEN, 27),
            boxed_label("place", GREEN, 27),
            boxed_label("activation", GREEN, 27),
        ).arrange(RIGHT, buff=0.38).move_to([0, -1.95, 0])
        self.play(LaggedStart(*[FadeIn(x, shift=UP * 0.15) for x in labels], lag_ratio=0.18),
                  run_time=1.4)
        self.at("rather than locking")
        self.play(route.blocks[0].animate.shift(UP * 0.18),
                  route.blocks[1].animate.shift(UP * 0.18), rate_func=there_and_back, run_time=1.4)
        self.at("different organized context")
        faint = RoundedRectangle(corner_radius=0.3, width=4.55, height=1.40,
                                 stroke_color=GREEN, stroke_width=5,
                                 fill_color=GREEN, fill_opacity=0.03).set_opacity(0.38)
        faint.move_to([-0.25, -1.10, 0])
        self.play(FadeOut(labels), FadeOut(route.rail.label), FadeIn(faint),
                  route.blocks[0].animate.move_to([-1.35, -1.10, 0]),
                  route.blocks[1].animate.move_to([0.85, -1.10, 0]), run_time=1.7)
        self.finish()


class S05Context(SpokenScene):
    def construct(self):
        mating = route_row(y=2.05, scaffold=True)
        mating.rail.label.set_opacity(0)
        filament = route_row(y=0.05, scaffold=False, dim=True,
                             names=("Ste11", "Ste7", "Kss1"), input_name="filament", output_ring=False)
        salt = route_row(y=-1.95, scaffold=False, dim=True,
                         names=("Ste11", "middle", "Hog1"), input_name="salt stress", output_ring=False)
        bob(filament.blocks[2], amp=0.09, speed=3.1)
        bob(salt.blocks[2], amp=0.09, speed=3.3, seed=2)
        labels = VGroup(
            T("MATING", 25, GREEN, weight=BOLD).move_to([-5.85, 2.88, 0]),
            T("FILAMENT", 25, GREY, weight=BOLD).move_to([-5.72, 0.88, 0]),
            T("SALT STRESS", 25, GREY, weight=BOLD).move_to([-5.55, -1.12, 0]),
        )
        self.play(FadeIn(filament), FadeIn(labels[1]), run_time=0.9)
        self.at("ends at KSS1")
        pulse1 = Dot(filament.input.get_right() + DOWN * 0.63, radius=0.13, color=GREY)
        self.add(pulse1)
        self.play(pulse1.animate.move_to(filament.blocks[2].get_center() + DOWN * 0.63), run_time=1.5)
        self.at("One salt stress branch")
        self.play(FadeIn(salt), FadeIn(labels[2]), run_time=1.0)
        self.at("different middle kinase")
        self.play(Indicate(salt.blocks[1], color=ORANGE), run_time=1.0)
        self.at("ends at HOG1")
        pulse2 = Dot(salt.input.get_right() + DOWN * 0.63, radius=0.13, color=GREY)
        self.add(pulse2)
        self.play(pulse2.animate.move_to(salt.blocks[2].get_center() + DOWN * 0.63), run_time=1.4)
        self.at("Only the mating root")
        self.play(FadeIn(mating), FadeIn(labels[0]), run_time=1.0)
        self.at("only the mating root switches")
        pulse3 = Dot(mating.input.get_right() + DOWN * 0.63, radius=0.14, color=GOLD)
        self.add(pulse3)
        self.play(pulse3.animate.move_to(mating.blocks[2].get_center() + DOWN * 0.63), run_time=1.4)
        self.play(Indicate(mating.blocks[2], color=PURPLE), run_time=0.7)
        self.finish()


class S06Predict(SpokenScene):
    def construct(self):
        picture = prediction_backdrop(complete=True)
        card = question_card(PREDICT_Q, y=-3.12, size=30)
        # Begin with one complete assembly; empty scaffolds arrive one at a time.
        self.play(FadeIn(picture.scaffolds[2]), run_time=0.7)
        self.at("keeps adding empty")
        empties = VGroup(*[s for i, s in enumerate(picture.scaffolds) if i != 2])
        self.play(LaggedStart(*[FadeIn(s, shift=UP * 0.14) for s in empties], lag_ratio=0.18),
                  run_time=1.5)
        self.at("complete kinase assemblies")
        self.play(FadeIn(picture.scaffolds[2].blocks), run_time=0.8)
        self.at("keep rising")
        self.play(FadeIn(card), Indicate(picture.scaffolds[2], color=GREEN), run_time=1.0)
        self.at("Watch where each kinase")
        self.play(FadeIn(picture.kinases), run_time=0.8)
        for i, scaffold in enumerate(picture.scaffolds):
            bob(scaffold, amp=0.08, speed=3.0, seed=i)
        self.at("make your prediction")
        self.play(LaggedStart(*[k.animate.shift(DOWN * 0.10) for k in picture.kinases],
                              lag_ratio=0.15), rate_func=there_and_back, run_time=1.2)
        self.finish()


class S07Pause(PredictPause):
    QUESTION = PREDICT_Q
    SECONDS = 4.5
    CARD = {"y": -3.12, "size": 30}
    RING_AT = (6.05, -3.08, 0)

    def backdrop(self):
        return prediction_backdrop(complete=True, drifting=True)


class S08Reveal(SpokenScene):
    def construct(self):
        picture = prediction_backdrop(complete=False)
        scaffolds, kinases = picture.scaffolds, picture.kinases
        gauge_v = ValueTracker(0.82)
        gauge = dial(gauge_v, center=[4.80, -1.62, 0], radius=1.0,
                     label="model output", color=PURPLE, fmt="{:.0f}%", scale=100, size=34)
        tag = scope_tag("model · schematic")
        self.add(scaffolds, kinases)
        self.play(LaggedStart(*[k.animate.shift(UP * 0.10) for k in kinases],
                              lag_ratio=0.15), rate_func=there_and_back, run_time=1.3)
        self.at("all three kinases")
        target = scaffolds[2]
        self.play(Succession(
            kinases[2].animate.move_to(target.slots[2]),
            kinases[1].animate.move_to(target.slots[1]),
            kinases[0].animate.move_to(target.slots[0]),
        ), run_time=1.8)
        self.at("With scaffold in excess")
        self.play(FadeIn(gauge), FadeIn(tag), run_time=0.8)
        self.at("spread across different")
        destinations = [scaffolds[0].slots[0], scaffolds[2].slots[1], scaffolds[4].slots[2]]
        self.play(*[k.animate.move_to(d) for k, d in zip(kinases, destinations)], run_time=2.0)
        for i, kinase in enumerate(kinases):
            bob(kinase, amp=0.10, speed=3.2, seed=i)
        self.at("Fewer scaffolds are complete")
        self.play(LaggedStart(*[Indicate(s, color=GREEN, scale_factor=1.03)
                                for s in scaffolds], lag_ratio=0.12), run_time=1.5)
        self.at("predicted output falls")
        self.play(gauge_v.animate.set_value(0.18), run_time=2.0)
        self.at("model effect is called")
        label = caption("combinatorial inhibition", size=32, color=GOLD, y=-3.08)
        self.play(FadeIn(label), run_time=1.0)
        self.at("combinatorial inhibition")
        self.play(Indicate(label, color=GOLD), run_time=1.0)
        self.finish()


class S09Evidence(SpokenScene):
    def construct(self):
        route = route_row(scaffold=True)
        route.rail.label.shift(UP * 0.12)
        bob(route.input, amp=0.10, speed=3.0)
        bob(route.blocks[0], amp=0.10, speed=3.2, seed=2)
        bob(route.rail.label, amp=0.09, speed=3.1, seed=4)
        self.add(route)
        assembly = boxed_label("assembly", GREEN, 28).move_to([-3.75, -2.08, 0])
        selective = boxed_label("selective activation", GREEN, 28).move_to([3.25, -2.08, 0])
        self.at("binds the mating kinases")
        self.play(LaggedStart(*[Indicate(s, color=GREEN) for s in route.rail.slots],
                              lag_ratio=0.22), run_time=1.4)
        self.at("different regions")
        check1 = T("✓", 45, GOLD, weight=BOLD).next_to(assembly, LEFT, buff=0.22)
        self.play(FadeIn(assembly), FadeIn(check1), run_time=0.9)
        self.at("Later work showed")
        gate = VGroup(
            Line([0.20, -0.45, 0], [3.80, -0.45, 0], color=GREEN, stroke_width=8),
            Line([0.20, -0.45, 0], [0.20, -0.25, 0], color=GREEN, stroke_width=8),
            Line([3.80, -0.45, 0], [3.80, -0.25, 0], color=GREEN, stroke_width=8),
        )
        for line in gate:
            pulse(line, base=8, amp=2.0, speed=1.8)
        self.play(Create(gate), run_time=1.0)
        self.at("makes fuss")
        self.play(route.blocks[1].animate.shift(RIGHT * 0.18),
                  route.blocks[2].animate.shift(LEFT * 0.18), run_time=1.1)
        self.at("easier for STI")
        check2 = T("✓", 45, GOLD, weight=BOLD).next_to(selective, LEFT, buff=0.22)
        self.play(FadeIn(selective), FadeIn(check2), run_time=0.9)
        self.at("work together")
        bracket = VGroup(
            Line([-5.45, -2.62, 0], [5.05, -2.62, 0], color=GOLD, stroke_width=6),
            Line([-5.45, -2.62, 0], [-5.45, -2.43, 0], color=GOLD, stroke_width=6),
            Line([5.05, -2.62, 0], [5.05, -2.43, 0], color=GOLD, stroke_width=6),
        )
        both = T("together", 30, GOLD, weight=BOLD).move_to([0, -3.14, 0])
        self.play(Create(bracket), FadeIn(both), run_time=1.3)
        self.finish()


class S10Payoff(SpokenScene):
    def construct(self):
        fork = fork_picture(scaffold=True)
        bob(fork.input, amp=0.09, speed=3.0)
        bob(fork.outputs[0], amp=0.09, speed=3.2, seed=2)
        bob(fork.outputs[2], amp=0.09, speed=3.2, seed=4)
        m = membrane()
        self.play(FadeIn(fork), run_time=1.0)
        self.at("A shared kinase")
        self.play(Indicate(fork.shared, color=ORANGE), run_time=1.0)
        self.at("does not choose")
        self.play(LaggedStart(*[o.animate.shift(RIGHT * 0.10) for o in fork.outputs],
                              lag_ratio=0.18), rate_func=there_and_back, run_time=1.2)
        self.at("organizer around it")
        self.play(Create(m), Indicate(fork.organizer, color=GREEN), run_time=1.1)
        self.at("which partners meet")
        pulse_dot = Dot(fork.input.get_right() + DOWN * 0.75, radius=0.16, color=GOLD)
        self.add(pulse_dot)
        self.play(pulse_dot.animate.move_to(fork.shared.get_center() + DOWN * 0.75), run_time=1.2)
        self.at("where the complex forms")
        self.play(FadeOut(fork.outputs[0]), FadeOut(fork.outputs[2]),
                  FadeOut(fork.links[1]), FadeOut(fork.links[3]),
                  VGroup(fork.organizer, fork.shared, fork.outputs[1], fork.links[2])
                  .animate.shift(UP * 1.15), run_time=1.2)
        self.at("last step can proceed")
        self.play(pulse_dot.animate.move_to(fork.outputs[1].get_center() + UP * 0.40), run_time=1.1)
        self.play(Indicate(fork.outputs[1], color=PURPLE), run_time=0.7)
        self.finish()


class S11End(EndCard):
    LINE = "Scaffolds route shared parts by controlling partners, place and activation."
