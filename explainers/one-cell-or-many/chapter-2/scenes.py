"""Different Cells, Shared DNA — chapter 2 of One Cell or Many.

COLOR MAP (shared with chapter 1; one meaning throughout)
  BLUE    = movement
  GOLD    = feeding
  TEAL    = water balance
  GREEN   = reproduction
  VIOLET  = nerve signalling
  RED     = oxygen carrying / red blood cells
  MAGENTA = shared DNA and genes
  ORANGE  = muscle, tissues, and organs
  CREAM   = neutral cell outlines

All cell drawings are schematic and not to scale.  Builders below are reused whenever a
picture carries across a cut, so landmarks do not drift between scenes.
"""
import numpy as np
from bp_parts import *  # noqa: F401,F403


VIOLET = "#B58CD9"
MAGENTA = "#E66FB7"
ORANGE = "#F29E4C"
CREAM = "#F3E6C9"
SOIL = "#9C7A5B"


def arrow(a, b, color=GREY, width=5, tip=0.22):
    return Arrow(a, b, buff=0.06, color=color, stroke_width=width, tip_length=tip,
                 max_tip_length_to_length_ratio=0.4, max_stroke_width_to_length_ratio=12)


def cell_outline(center=ORIGIN, width=2.0, height=1.5, color=CREAM, opacity=0.12):
    return Ellipse(width=width, height=height, stroke_color=color, stroke_width=5,
                   fill_color=color, fill_opacity=opacity).move_to(center)


def schematic_tag():
    return scope_tag("schematic • not to scale", color=GREY)


def microscope_field():
    """The shared dark slide used behind every diagram in this chapter."""
    return RoundedRectangle(corner_radius=0.35, width=13.1, height=6.7,
                            stroke_color=CREAM, stroke_width=2,
                            fill_color=CREAM, fill_opacity=0.10).set_stroke(opacity=0.16).set_z_index(-20)


class FilmScene(SpokenScene):
    """Spoken scene on the chapter's single, softly lit microscope-slide stage."""
    def setup(self):
        super().setup()
        self.add(microscope_field())


def job_cluster(question=False):
    """The chapter-one many-cell cluster, rebuilt identically in s01."""
    colors = [BLUE, GOLD, TEAL, GREEN]
    cells = VGroup()
    for row in range(2):
        for col in range(4):
            c = Circle(radius=0.62, stroke_color=CREAM, stroke_width=4,
                       fill_color=CREAM, fill_opacity=0.08)
            c.move_to([-3.0 + col * 2.0, 1.15 - row * 2.0, 0])
            token = Dot(c.get_center(), radius=0.18, color=colors[(row + col) % 4])
            cells.add(VGroup(c, token))
    labels = VGroup(*[T(t, 28, c) for t, c in zip(
        ["move", "feed", "water", "reproduce"], colors)])
    labels.arrange(RIGHT, buff=0.65).move_to([0, -2.35, 0])
    g = VGroup(cells, labels)
    if question:
        faint = VGroup(*[
            Ellipse(width=1.35 + 0.2 * (i % 3), height=0.9 + 0.22 * ((i + 1) % 3),
                    stroke_color=CREAM, stroke_width=2).set_opacity(0.18).move_to(c[0])
            for i, c in enumerate(cells)
        ])
        q = T("?", 80, GOLD, font=TITLE_FONT).move_to([0, 0.1, 0])
        g.add(faint, q)
    return g


def neuron_picture(labels=True):
    """Neuron used in s03 and the DNA/closing worlds, at one fixed scale."""
    body = Circle(radius=0.68, stroke_color=CREAM, stroke_width=5,
                  fill_color=CREAM, fill_opacity=0.12).move_to([-3.9, 0.35, 0])
    dendrites = VGroup(*[
        Line(body.get_center() + np.array([-0.42, dy, 0]),
             [-5.25, 0.35 + 1.25 * dy, 0], color=CREAM, stroke_width=4)
        for dy in (-0.42, 0, 0.42)
    ])
    axon = Line(body.get_right(), [5.0, 0.35, 0], color=CREAM, stroke_width=7)
    terminals = VGroup(*[
        Line([5.0, 0.35, 0], [5.65, 0.35 + dy, 0], color=CREAM, stroke_width=4)
        for dy in (-0.55, 0, 0.55)
    ])
    g = VGroup(dendrites, body, axon, terminals)
    if labels:
        spine = T("spine", 28, VIOLET).move_to([-5.45, -1.25, 0])
        foot = T("foot", 28, VIOLET).move_to([5.55, -1.25, 0])
        axlab = T("long, thin axon", 30, CREAM).move_to([0.8, 1.15, 0])
        g.add(spine, foot, axlab)
    return g


def muscle_picture(center=ORIGIN, width=9.2, height=2.55, labels=True):
    box = RoundedRectangle(corner_radius=0.7, width=width, height=height,
                           stroke_color=CREAM, stroke_width=5,
                           fill_color=ORANGE, fill_opacity=0.12).move_to(center)
    fibres = VGroup(*[
        Line([center[0] - width * 0.39, center[1] + y, 0],
             [center[0] + width * 0.39, center[1] + y, 0],
             color=ORANGE, stroke_width=8)
        for y in (-0.62, 0, 0.62)
    ])
    g = VGroup(box, fibres)
    if labels:
        g.add(T("skeletal muscle cell", 32, ORANGE).next_to(box, UP, buff=0.3))
    return g


def root_hair_picture(labels=True):
    soil = Rectangle(width=10.8, height=2.55, stroke_color=SOIL, stroke_width=3,
                     fill_color=SOIL, fill_opacity=0.14).move_to([0.5, -0.75, 0])
    grains = VGroup(*[
        Circle(radius=0.18 + 0.05 * (i % 3), color=SOIL, stroke_width=2,
               fill_color=SOIL, fill_opacity=0.32).move_to([-4.3 + i * 0.85, -0.25 - 0.65 * (i % 2), 0])
        for i in range(12)
    ])
    body = RoundedRectangle(corner_radius=0.25, width=3.0, height=1.3,
                            stroke_color=CREAM, stroke_width=5,
                            fill_color=CREAM, fill_opacity=0.1).move_to([-4.2, 1.3, 0])
    hair = VMobject(stroke_color=CREAM, stroke_width=8, fill_opacity=0)
    hair.set_points_smoothly([[-3.2, 1.25, 0], [-1.5, 0.9, 0], [0.1, 0.1, 0],
                              [1.6, -0.8, 0], [3.9, -1.0, 0]])
    water = VGroup(*[
        arrow([x, -1.65, 0], hair.point_from_proportion(p), TEAL, width=4, tip=0.16)
        for x, p in ((-0.5, 0.5), (1.4, 0.7), (3.5, 0.93))
    ])
    g = VGroup(soil, grains, body, hair, water)
    if labels:
        g.add(T("root hair cell", 32, TEAL).move_to([-4.2, 2.45, 0]))
    return g


def seedling(x, long_hairs=True):
    stem = Line([x, 1.8, 0], [x, 0.5, 0], color=GREEN, stroke_width=7)
    leaves = VGroup(
        Ellipse(width=0.9, height=0.42, color=GREEN, fill_color=GREEN, fill_opacity=0.3).rotate(0.35).move_to([x - 0.42, 1.75, 0]),
        Ellipse(width=0.9, height=0.42, color=GREEN, fill_color=GREEN, fill_opacity=0.3).rotate(-0.35).move_to([x + 0.42, 1.75, 0]),
    )
    root = Line([x, 0.5, 0], [x, -2.05, 0], color=CREAM, stroke_width=7)
    length = 1.0 if long_hairs else 0.35
    hairs = VGroup()
    for y in np.linspace(0.1, -1.8, 7):
        hairs.add(Line([x, y, 0], [x - length, y - 0.12, 0], color=TEAL, stroke_width=3))
        hairs.add(Line([x, y - 0.08, 0], [x + length, y + 0.08, 0], color=TEAL, stroke_width=3))
    return VGroup(stem, leaves, root, hairs)


def vessel_panel_world(with_question=True, nuclei=True):
    """Identical final frame for s05 and backdrop for s06/s07."""
    panels = TwoPanel("stiff sphere • schematic", "flexible dented disc • schematic",
                      colors=(CREAM, RED), top=2.9, bottom=-2.0)
    vessels = VGroup()
    cells = VGroup()
    nucs = VGroup()
    for x, dented in ((-3.3, False), (3.3, True)):
        top = Line([x + 0.45, 0.7, 0], [x + 2.3, 0.7, 0], color=RED, stroke_width=8)
        bot = Line([x + 0.45, -0.7, 0], [x + 2.3, -0.7, 0], color=RED, stroke_width=8)
        vessels.add(VGroup(top, bot))
        outer = Circle(radius=0.8, stroke_color=CREAM, stroke_width=5,
                       fill_color=RED, fill_opacity=0.18).move_to([x - 0.35, 0, 0])
        cell = VGroup(outer)
        if dented:
            cell.add(Ellipse(width=0.75, height=0.32, stroke_color=RED, stroke_width=3,
                             fill_color=BG, fill_opacity=1).move_to(outer))
        cells.add(cell)
        nucs.add(Circle(radius=0.22, color=MAGENTA, fill_color=MAGENTA,
                        fill_opacity=0.4).move_to(outer))
    g = VGroup(panels, vessels, cells)
    if nuclei:
        g.add(nucs)
    if with_question:
        g.add(question_card("Which passes a narrow vessel?", y=-3.12, max_w=9.8))
    g.panels, g.vessels, g.cells, g.nuclei = panels, vessels, cells, nucs
    return g


def gene_strip(center, active=None, active_color=ORANGE):
    blocks = VGroup(*[
        RoundedRectangle(corner_radius=0.08, width=0.68, height=0.58,
                         stroke_color=MAGENTA, stroke_width=3,
                         fill_color=MAGENTA, fill_opacity=0.14)
        for _ in range(6)
    ]).arrange(RIGHT, buff=0.10).move_to(center)
    if active is not None:
        blocks[active].set_stroke(active_color, width=5).set_fill(active_color, opacity=0.72)
    return blocks


def scanning_glow(strips):
    """A soft moving highlight showing that the shared strip is being read."""
    glows = VGroup()
    for j, strip in enumerate(strips):
        glow = RoundedRectangle(corner_radius=0.1, width=1.0, height=2.6,
                                stroke_width=0, fill_color=MAGENTA, fill_opacity=0.18)
        left, right = strip.get_left()[0] + 0.35, strip.get_right()[0] - 0.35
        glow.move_to([left, strip.get_y(), 0]).set_z_index(-1)
        glow._scan_t = j * 0.5

        def scan(mob, dt, left=left, right=right, y=strip.get_y()):
            mob._scan_t += dt
            u = (0.36 * mob._scan_t) % 1.0
            mob.move_to([left + (right - left) * u, y, 0])
        glow.add_updater(scan)
        glows.add(glow)
    return glows


def dna_comparison(active=False):
    """The exact same-DNA world carried through s08, s09, and s11."""
    panels = TwoPanel("neuron", "muscle cell", colors=(VIOLET, ORANGE), top=3.0, bottom=-2.2)
    left_cell = cell_outline([-3.3, -0.1, 0], 5.2, 3.2)
    right_cell = RoundedRectangle(corner_radius=0.65, width=5.2, height=3.2,
                                  stroke_color=CREAM, stroke_width=5,
                                  fill_color=CREAM, fill_opacity=0.08).move_to([3.3, -0.1, 0])
    n1 = Circle(radius=0.82, color=MAGENTA, stroke_width=4).move_to([-3.3, -0.1, 0])
    n2 = Circle(radius=0.82, color=MAGENTA, stroke_width=4).move_to([3.3, -0.1, 0])
    b1 = gene_strip([-3.3, -0.1, 0], 4 if active else None, VIOLET).scale(0.78)
    b2 = gene_strip([3.3, -0.1, 0], 1 if active else None, ORANGE).scale(0.78)
    bracket = BraceBetweenPoints([-5.35, -2.48, 0], [5.35, -2.48, 0], direction=DOWN, color=MAGENTA)
    same = T("same DNA", 34, MAGENTA).next_to(bracket, DOWN, buff=0.12)
    g = VGroup(panels, left_cell, right_cell, n1, n2, b1, b2, bracket, same)
    g.strips, g.cells, g.nuclei = VGroup(b1, b2), VGroup(left_cell, right_cell), VGroup(n1, n2)
    return g


class S00Title(TitleCard):
    LESSON = "One Cell or Many"
    TITLE = "Different Cells, Shared DNA"


class S01Link(FilmScene):
    def construct(self):
        cluster = job_cluster(False)
        self.play(FadeIn(cluster[0], lag_ratio=0.05), run_time=0.9)
        self.at("share life's jobs")
        self.play(FadeIn(cluster[1], lag_ratio=0.12), run_time=0.8)
        self.at("How can their cells")
        possible = job_cluster(True)
        self.play(FadeIn(possible[2], lag_ratio=0.05), FadeIn(possible[3]), run_time=1.0)
        self.play(possible[2].animate.stretch(1.12, 0), run_time=1.2, rate_func=there_and_back)
        self.finish()


class S02Specialized(FilmScene):
    def construct(self):
        cell = cell_outline([0, 0.1, 0], 7.0, 4.2)
        self.play(GrowFromCenter(cell), run_time=0.8)
        self.at("structure suited")
        lab = T("specialized: fitted for a job", 38, CREAM, font=TITLE_FONT).to_edge(UP, buff=0.45)
        self.play(FadeIn(lab), run_time=0.6)
        self.at("Form is not decoration")
        long = cell_outline([0, 0.1, 0], 10.0, 2.3)
        flat = cell_outline([0, 0.1, 0], 7.0, 1.4)
        bent = Arc(radius=2.2, start_angle=0.15, angle=PI - 0.3, color=CREAM, stroke_width=16).stretch(1.45, 0)
        self.play(Transform(cell, long), run_time=0.9)
        self.play(Transform(cell, flat), run_time=0.8)
        self.play(Transform(cell, bent), run_time=0.8)
        self.at("cell can reach")
        acts = VGroup(T("reach", 34, VIOLET), T("carry", 34, RED), T("move", 34, BLUE))
        acts.arrange(RIGHT, buff=1.1).move_to([0, -2.6, 0])
        self.play(FadeIn(acts[0], shift=UP * 0.15), run_time=0.35)
        self.at("carry")
        self.play(FadeIn(acts[1], shift=UP * 0.15), run_time=0.35)
        self.at("move")
        self.play(FadeIn(acts[2], shift=UP * 0.15), run_time=0.35)
        self.add(schematic_tag())
        self.finish()


class S03Neuron(FilmScene):
    def construct(self):
        seed = cell_outline([-3.9, 0.35, 0], 1.36, 1.36)
        self.play(GrowFromCenter(seed), run_time=0.45)
        self.at("grows a long")
        neuron = neuron_picture(False)
        self.play(Transform(seed, neuron[1]), Create(neuron[0]), Create(neuron[2]), Create(neuron[3]), run_time=2.55)
        pulse(neuron[2], base=9, amp=4, speed=1.5)
        axlab = T("long, thin axon", 30, CREAM).move_to([0.8, 1.25, 0])
        self.play(FadeIn(axlab), run_time=0.35)
        self.at("carry a signal")
        spine = T("spine", 28, VIOLET).move_to([-5.45, -1.25, 0])
        foot = T("foot", 28, VIOLET).move_to([5.55, -1.25, 0])
        pulse_dot = Circle(radius=0.46, stroke_color=VIOLET, stroke_width=8,
                           fill_color=VIOLET, fill_opacity=0.22).move_to([-3.2, 0.35, 0])
        self.play(FadeIn(spine), FadeIn(foot), FadeIn(pulse_dot), run_time=0.45)
        self.play(pulse_dot.animate.move_to([5.0, 0.35, 0]), run_time=2.0, rate_func=linear)
        self.at("reach fits")
        cap = caption("Long reach fits long-distance signalling.", color=VIOLET)
        self.play(FadeIn(cap), pulse_dot.animate.move_to([5.65, 0.35, 0]), run_time=0.7)
        self.add(schematic_tag())
        self.finish()


class S04MuscleRoot(FilmScene):
    def construct(self):
        muscle = muscle_picture()
        self.play(FadeIn(muscle[0]), run_time=0.55)
        self.at("packed with fibers")
        self.play(Create(muscle[1], lag_ratio=0.15), FadeIn(muscle[2]), run_time=0.9)
        self.at("shorten together")
        short = muscle_picture(width=6.6)
        self.play(Transform(muscle, short), run_time=1.2)
        self.at("root hair cell")
        root = root_hair_picture(False)
        self.play(FadeOut(muscle), FadeIn(root[0]), FadeIn(root[1]), FadeIn(root[2]), run_time=0.7)
        self.at("grows a thin tube")
        self.play(Create(root[3]), run_time=1.2)
        lab = T("root hair cell", 32, TEAL).move_to([-4.2, 2.45, 0])
        self.play(FadeIn(lab), run_time=0.3)
        self.at("water enters")
        self.play(LaggedStart(*[GrowArrow(a) for a in root[4]], lag_ratio=0.2), run_time=1.0)
        self.add(schematic_tag())
        self.finish()


class S04bEvidence(FilmScene):
    def construct(self):
        soil = Rectangle(width=12.0, height=2.8, color=SOIL, fill_color=SOIL,
                         fill_opacity=0.15).move_to([0, -1.0, 0]).rotate(-0.06)
        long = seedling(-3.1, True)
        short = seedling(3.1, False)
        self.play(FadeIn(soil), run_time=0.4)
        self.play(FadeIn(long, shift=UP * 0.25), FadeIn(short, shift=UP * 0.25), run_time=2.1)
        self.at("Arabidopsis seedlings")
        names = VGroup(T("long root hairs", 30, TEAL), T("short root hairs", 30, TEAL))
        names[0].move_to([-3.1, 2.7, 0]); names[1].move_to([3.1, 2.7, 0])
        self.play(FadeIn(names), run_time=0.5)
        self.at("longer root hairs")
        rain = VGroup(*[Line([x, 3.2, 0], [x - 0.35, 2.35, 0], color=BLUE, stroke_width=4)
                        for x in np.linspace(-5.5, 5.5, 10)])
        self.play(FadeOut(names), LaggedStart(*[Create(r) for r in rain], lag_ratio=0.06), run_time=1.0)
        self.play(rain.animate.shift(DOWN * 4.8), short.animate.shift(RIGHT * 0.55 + DOWN * 0.15).rotate(-0.12),
                  run_time=1.6)
        self.at("main roots were")
        same = caption("main roots: about the same size", color=CREAM)
        self.play(FadeOut(rain), FadeIn(same), Indicate(VGroup(long[2], short[2]), color=CREAM), run_time=0.8)
        self.at("root hair length")
        likely = T("root hairs differ", 32, TEAL).move_to([0, 1.55, 0])
        self.play(FadeIn(likely), Indicate(VGroup(long[3], short[3]), color=TEAL), run_time=0.9)
        self.add(schematic_tag())
        self.finish()


class S05Predict(FilmScene):
    def construct(self):
        panels = TwoPanel("stiff sphere • schematic", "flexible dented disc • schematic",
                          colors=(CREAM, RED), top=2.9, bottom=-2.0)
        self.play(FadeIn(panels), run_time=0.6)
        self.at("One is a stiff sphere")
        world = vessel_panel_world(False, True)
        for vessel in world.vessels:
            pulse(vessel, base=8, amp=3, speed=1.4)
        world.cells[0].shift(LEFT * 1.35)
        world.nuclei[0].shift(LEFT * 1.35)
        world.cells[1].shift(LEFT * 1.35)
        world.nuclei[1].shift(LEFT * 1.35)
        self.play(FadeIn(world.vessels[0]), FadeIn(world.cells[0]), FadeIn(world.nuclei[0]), run_time=0.7)
        self.play(world.cells[0].animate.shift(RIGHT * 1.35), world.nuclei[0].animate.shift(RIGHT * 1.35), run_time=1.45)
        self.at("other is a flexible")
        self.play(FadeIn(world.vessels[1]), FadeIn(world.cells[1]), FadeIn(world.nuclei[1]), run_time=0.7)
        self.play(world.cells[1].animate.shift(RIGHT * 1.35), world.nuclei[1].animate.shift(RIGHT * 1.35), run_time=2.15)
        self.at("Which passes")
        q = question_card("Which passes a narrow vessel?", y=-3.12, max_w=9.8)
        self.play(FadeIn(q), run_time=0.55)
        self.finish()


class S06Pause(PredictPause):
    QUESTION = "Which passes a narrow vessel?"
    CARD = {"y": -3.12, "max_w": 9.8}
    RING_AT = (6.05, -3.12, 0)

    def backdrop(self):
        world = vessel_panel_world(False, True)
        for vessel in world.vessels:
            pulse(vessel, base=8, amp=3, speed=1.4)
        return VGroup(microscope_field(), world)

    def construct(self):
        self.add(self.backdrop())
        self.add(question_card(self.QUESTION, y=-3.12, max_w=9.8))
        timer = ValueTracker(0.001)
        track = Circle(radius=1.65, color=GREY, stroke_width=8).set_opacity(0.45)
        arc = always_redraw(lambda: Arc(radius=1.65, start_angle=PI / 2,
                                        angle=timer.get_value(), color=GOLD,
                                        stroke_width=18, arc_center=ORIGIN))
        bead = always_redraw(lambda: Dot(
            1.65 * np.array([np.cos(PI / 2 + timer.get_value()),
                             np.sin(PI / 2 + timer.get_value()), 0]),
            radius=0.25, color=GOLD))
        self.add(track, arc, bead)
        self.play(timer.animate.set_value(TAU), run_time=self.SECONDS, rate_func=linear)
        self.finish()


class S07Reveal(FilmScene):
    def construct(self):
        world = vessel_panel_world(False, True)
        self.add(world)
        for vessel in world.vessels:
            pulse(vessel, base=8, amp=3, speed=1.4)
        stiff, flex = world.cells
        self.at("flexible dented disc")
        orig_flex = flex.copy()
        squeezed = flex.copy().stretch(1.65, 0).stretch(0.48, 1).move_to([4.25, 0, 0])
        self.play(Transform(flex, squeezed), run_time=0.8)
        self.play(flex.animate.move_to([5.0, 0, 0]), run_time=0.8)
        restored = orig_flex.copy().move_to([5.0, 0, 0])
        self.play(Transform(flex, restored), run_time=0.65)
        flow = RoundedRectangle(corner_radius=0.12, width=1.35, height=1.08,
                                stroke_width=0, fill_color=RED, fill_opacity=0.28).move_to([4.0, 0, 0]).set_z_index(-1)
        flow._x = 4.0

        def carry(mob, dt):
            mob._x += 0.75 * dt
            if mob._x > 5.0:
                mob._x = 3.85
            mob.set_x(mob._x)
        flow.add_updater(carry)
        self.add(flow)
        stop = T("stops", 30, CREAM).next_to(stiff, DOWN, buff=0.25)
        self.play(FadeIn(stop), run_time=0.3)
        self.at("no nucleus")
        no_nucleus = T("no nucleus", 32, RED).move_to([3.3, 1.7, 0])
        self.play(FadeOut(world.nuclei[1], shift=RIGHT * 0.3), FadeIn(no_nucleus), run_time=0.7)
        self.at("form suits transport")
        self.play(flex.animate.shift(RIGHT * 0.10), run_time=1.0)
        self.finish()


class S08Dna(FilmScene):
    def construct(self):
        world = dna_comparison(False)
        self.play(FadeIn(world.cells), FadeIn(world[0]), run_time=0.7)
        pulse(world.cells, base=5, amp=2.5, speed=1.35)
        self.at("deeper question")
        q = T("Different instructions?", 42, GOLD, font=TITLE_FONT).move_to([0, -2.55, 0])
        self.play(FadeIn(q), run_time=0.55)
        self.at("Mostly no")
        ans = T("mostly no", 42, MAGENTA, font=TITLE_FONT).move_to(q)
        self.play(swap(q, ans), run_time=0.65)
        self.at("with a nucleus")
        self.play(FadeOut(ans), FadeIn(world.nuclei), run_time=0.55)
        self.at("same DNA")
        self.play(FadeIn(world.strips), run_time=0.75)
        self.add(scanning_glow(world.strips))
        self.play(FadeIn(VGroup(world[7], world[8])), run_time=0.6)
        self.finish()


class S09Expression(FilmScene):
    def construct(self):
        base = dna_comparison(False)
        self.add(base)
        pulse(base.cells, base=5, amp=2.5, speed=1.35)
        self.add(scanning_glow(base.strips))
        self.at("gene expression")
        title = T("gene expression = using a gene", 36, MAGENTA, font=TITLE_FONT).to_edge(UP, buff=0.35)
        self.play(FadeIn(title), run_time=0.6)
        self.at("make a product")
        active = dna_comparison(True)
        products = VGroup(
            *[Line([-1.0 + 0.35 * i, -0.35, 0], [-0.75 + 0.35 * i, -0.35, 0], color=VIOLET, stroke_width=8) for i in range(3)],
            *[Line([4.15 + 0.35 * i, -0.35, 0], [4.4 + 0.35 * i, -0.35, 0], color=ORANGE, stroke_width=8) for i in range(3)],
        )
        self.play(Transform(base.strips, active.strips), FadeIn(products), run_time=0.9)
        self.at("different set of genes")
        self.play(products[:3].animate.shift(LEFT * 0.7), products[3:].animate.shift(RIGHT * 0.4), run_time=0.8)
        self.at("Cells fit life's jobs")
        rule = caption("Cells fit jobs through structure and gene use.", color=CREAM)
        self.play(FadeOut(VGroup(base[7], base[8])), FadeIn(rule), Indicate(base.cells, color=CREAM), run_time=1.0)
        self.finish()


class S09bExamples(FilmScene):
    def construct(self):
        strip = gene_strip([0, 2.35, 0], 1, ORANGE).scale(1.25)
        label = T("shortening-protein gene", 32, ORANGE).next_to(strip[1], DOWN, buff=0.25)
        muscle = muscle_picture(center=np.array([0, -0.55, 0]), width=9.2, height=2.4, labels=False)
        self.add(strip, muscle[0])
        self.play(FadeIn(label), run_time=0.4)
        self.at("proteins that slide")
        bars = VGroup(*[Line([-3.2, y, 0], [3.2, y, 0], color=ORANGE, stroke_width=8) for y in (-0.9, -0.2)])
        self.play(TransformFromCopy(strip[1], bars), run_time=0.7)
        self.play(bars.animate.stretch(0.68, 0), muscle[0].animate.stretch(0.72, 0), run_time=1.0)
        self.at("Other genes stay unused")
        dim = T("unused ≠ deleted", 32, MAGENTA).move_to([0, -2.55, 0])
        self.play(FadeIn(dim), Indicate(VGroup(*[strip[i] for i in range(6) if i != 1]), color=MAGENTA), run_time=0.8)
        self.finish()


class S10Example(FilmScene):
    def construct(self):
        cell = cell_outline([0, -0.35, 0], 6.0, 4.4, color=RED)
        nucleus = Circle(radius=1.05, color=MAGENTA, stroke_width=5).move_to([-1.15, -0.25, 0])
        strip = gene_strip([-1.15, -0.25, 0], 3, RED).scale(0.72)
        self.play(GrowFromCenter(cell), FadeIn(nucleus), FadeIn(strip), run_time=0.8)
        pulse(cell, base=5, amp=2.5, speed=1.4)
        self.at("genes for hemoglobin")
        lab = T("hemoglobin gene", 34, RED).move_to([0, 2.55, 0])
        self.play(FadeIn(lab), Indicate(strip[3], color=RED), run_time=0.6)
        self.at("carries oxygen")
        cargo = VGroup(*[Dot([x, y, 0], radius=0.16, color=RED)
                         for x, y in ((-2.1, 0.9), (-0.4, 1.0), (1.5, 0.8), (-1.8, -1.3), (0.2, -1.2), (1.8, -0.8))])
        self.play(LaggedStart(*[FadeIn(d, shift=UP * 0.1) for d in cargo], lag_ratio=0.1), run_time=0.9)
        self.at("pushes out its nucleus")
        self.play(VGroup(nucleus, strip).animate.move_to([3.9, -0.25, 0]), run_time=1.0)
        self.play(FadeOut(VGroup(nucleus, strip), shift=RIGHT * 0.5), cell.animate.stretch(0.72, 1), run_time=0.8)
        self.at("specialized contents")
        self.play(cargo.animate.arrange_in_grid(2, 3, buff=0.5).move_to(cell), run_time=0.8)
        self.add(schematic_tag())
        self.finish()


class S11Scope(FilmScene):
    def construct(self):
        strip = gene_strip([0, 1.8, 0]).scale(1.2)
        bracket = Brace(strip, DOWN, color=MAGENTA)
        model = T("main model: nucleated body cells", 34, MAGENTA).next_to(bracket, DOWN, buff=0.2)
        self.play(FadeIn(strip), GrowFromCenter(bracket), FadeIn(model), run_time=0.8)
        pulse(strip, base=3, amp=2, speed=1.4)
        self.at("not a claim without exceptions")
        self.play(VGroup(strip, bracket, model).animate.shift(UP * 0.45), run_time=0.55)
        cards = VGroup(
            chip("some immune cells: DNA rearranged", VIOLET, size=26),
            chip("egg and sperm: one set", GREEN, size=26),
            chip("most body cells: two sets", CREAM, size=26),
        ).arrange(DOWN, buff=0.25, aligned_edge=LEFT).move_to([0, -1.25, 0])
        self.at("Some immune cells")
        self.play(FadeIn(cards[0], shift=RIGHT * 0.2), run_time=0.55)
        self.at("Egg and sperm")
        self.play(FadeIn(cards[1], shift=RIGHT * 0.2), run_time=0.55)
        self.at("most body cells")
        self.play(FadeIn(cards[2], shift=RIGHT * 0.2), run_time=0.55)
        self.finish()


class S11bTest(FilmScene):
    def construct(self):
        gut = cell_outline([-4.7, 1.0, 0], 2.4, 1.8)
        nucleus = Circle(radius=0.38, color=MAGENTA, fill_color=MAGENTA, fill_opacity=0.32).move_to(gut)
        eggs = VGroup(*[Circle(radius=0.58, color=CREAM, stroke_width=4,
                              fill_color=CREAM, fill_opacity=0.08).move_to([-2.0 + i * 1.45, -0.8, 0])
                        for i in range(6)])
        heading = T("frog nucleus transfer", 36, MAGENTA, font=TITLE_FONT).to_edge(UP, buff=0.35)
        self.add(gut, nucleus, eggs)
        self.play(FadeIn(heading), run_time=0.5)
        pulse(eggs, base=4, amp=2.2, speed=1.4)
        self.at("nuclei moved into eggs")
        target = eggs[0].get_center()
        self.play(nucleus.animate.move_to(target), run_time=1.0)
        self.play(FadeIn(VGroup(*[nucleus.copy().move_to(e) for e in eggs[1:]])), run_time=0.6)
        self.at("still built tadpoles")
        failures = VGroup(*[Cross(e, stroke_color=GREY, stroke_width=5) for e in eggs[:5]])
        tadpole = VGroup(Ellipse(width=1.6, height=0.8, color=CREAM, fill_color=CREAM, fill_opacity=0.12),
                         Arc(radius=1.2, start_angle=PI, angle=1.2, color=CREAM, stroke_width=7)).move_to([3.3, 1.05, 0])
        self.play(FadeIn(failures), Transform(eggs[5], tadpole), run_time=1.1)
        icons = VGroup(chip("nerve", VIOLET, size=25), chip("muscle", ORANGE, size=25), chip("blood", RED, size=25))
        icons.arrange(RIGHT, buff=0.25).move_to([2.4, -2.25, 0])
        self.play(FadeIn(icons, lag_ratio=0.15), run_time=0.7)
        note = T("a few succeeded; most failed", 30, GREY).move_to([-3.35, -2.95, 0])
        self.play(FadeIn(note), run_time=0.4)
        self.at("not thrown")
        kept = T("unused genes were still there", 34, MAGENTA).move_to([0, 2.75, 0])
        self.play(FadeIn(kept), Indicate(nucleus, color=MAGENTA), run_time=0.9)
        self.add(schematic_tag())
        self.finish()


class S12Close(FilmScene):
    def construct(self):
        book = RoundedRectangle(corner_radius=0.2, width=4.8, height=4.8,
                                stroke_color=MAGENTA, stroke_width=5,
                                fill_color=MAGENTA, fill_opacity=0.1)
        spine = Line([0, -2.4, 0], [0, 2.4, 0], color=MAGENTA, stroke_width=4)
        strip_l = gene_strip([-1.2, 0.2, 0]).scale(0.72).arrange(DOWN, buff=0.1)
        strip_r = gene_strip([1.2, 0.2, 0]).scale(0.72).arrange(DOWN, buff=0.1)
        self.play(FadeIn(book), Create(spine), FadeIn(strip_l), FadeIn(strip_r), run_time=0.8)
        pulse(book, base=5, amp=2.5, speed=1.35)
        self.at("different instruction books")
        same = T("one shared instruction book", 38, MAGENTA, font=TITLE_FONT).to_edge(UP, buff=0.35)
        self.play(FadeIn(same), run_time=0.6)
        self.at("different parts")
        tabs = VGroup(*[Rectangle(width=0.62, height=0.3, fill_color=c, fill_opacity=0.9, stroke_width=0)
                        for c in (VIOLET, ORANGE, RED, TEAL)])
        for i, t in enumerate(tabs):
            t.move_to([2.7, 1.45 - i * 0.75, 0])
        self.play(LaggedStart(*[FadeIn(t, shift=LEFT * 0.2) for t in tabs], lag_ratio=0.12), run_time=0.8)
        self.at("building structures")
        cells = VGroup(chip("neuron", VIOLET, 26), chip("muscle", ORANGE, 26),
                       chip("red blood", RED, 26), chip("root hair", TEAL, 26))
        cells.arrange(DOWN, buff=0.18).move_to([-4.5, -0.1, 0])
        self.play(FadeIn(cells, lag_ratio=0.12), run_time=0.9)
        rule = caption("Different gene use builds structures suited to each job.", color=CREAM)
        self.play(FadeIn(rule), run_time=0.65)
        self.finish()


class S13End(EndCard):
    LINE = "Cells fit life's jobs through structure and gene use, alone or together."
