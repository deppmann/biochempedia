"""Thymidine-analog birthdating, timed to the supplied narration.

Colour map, adapted from the patch-clamp film: grey is tissue and unlabelled
cells, teal is the ventricular surface, orange is the administered pulse,
yellow is retained label, purple is the later cohort, red is injury or
ambiguity, blue is microscopy, green is corroboration, and gold marks time.
"""
from bp_parts import *
from bp_style import EndCard

PURPLE = "#B58CD9"
ORANGE = "#F29E4C"
WALL = "#263749"
DEEP = "#30465A"
SURFACE = "#36546A"
ZONE = "#294D58"
CELL = "#48586B"
NUCLEUS = "#8195A9"
QUESTION = "Must this cell have passed through S phase?"
QUESTION_POSITION = dict(y=3.24, size=34, max_w=11.6)


def point(x, y):
    return np.array([x, y, 0.0])


def label(text, x=0, y=3.22, color=TEXT, size=34):
    return T(text, size, color).move_to(point(x, y))


def strip(x0, x1, y, width, color, opacity=1):
    return Line(point(x0, y), point(x1, y), stroke_width=width,
                color=color, stroke_opacity=opacity)


def section_band(top, bottom, color, left=-6.28, right=6.28):
    """A broad tissue layer seen in section, with gently curved boundaries."""
    xs = np.linspace(left, right, 33)
    edge = 0.14 * np.cos(xs * 0.58) - 0.07 * np.sin(xs * 1.02)
    return Polygon(*[point(x, top + dy) for x, dy in zip(xs, edge)],
                   *[point(x, bottom + dy) for x, dy in zip(xs[::-1], edge[::-1])],
                   fill_color=color, fill_opacity=1, stroke_width=0)


def wall(injured=False, basal=False):
    """The shared cross-section and its radial fibres, with fixed landmarks."""
    bands = VGroup(
        section_band(2.57, 1.50, SURFACE),
        section_band(1.50, 0.37, DEEP),
        section_band(0.37, -2.02, WALL),
        section_band(-2.02, -2.57, ZONE),
    )
    if basal:
        bands[0].set_fill(DEEP)
        bands[1].set_fill(WALL)
    fibres = VGroup()
    for x in ([] if basal else np.linspace(-5.72, 5.55, 12)):
        fibre = CubicBezier(point(x, -2.42), point(x - 0.22, -0.72),
                           point(x + 0.12, 0.68), point(x + 0.37, 2.47))
        fibre.set_stroke(GREY, width=2, opacity=0.25)
        fibres.add(fibre)
    world = VGroup(bands, fibres)
    if injured:
        wound = Polygon(point(0.6, 2.75), point(1.13, 2.18), point(0.82, 1.73),
                        point(1.39, 1.20), point(1.57, 0.35), point(1.91, 1.26),
                        point(2.47, 1.70), point(2.26, 2.17), point(2.93, 2.75),
                        stroke_width=0, fill_opacity=1, fill_color=BG)
        edge = VMobject(stroke_color=RED, stroke_width=3, stroke_opacity=0.7)
        edge.set_points_as_corners(wound.get_vertices()[1:-1])
        world.add(wound, edge)
    return world


def cell(x, y, r=0.46, *, kind="neuron", signal=None, strength=1.0):
    """Cell bodies, a nucleus and, for neurons, simple branching processes."""
    body = Ellipse(width=1.65 * r, height=2 * r, stroke_color=GREY,
                   stroke_width=2.4, fill_color=CELL, fill_opacity=1)
    branches = VGroup()
    if kind == "neuron":
        for vertices in [
            [(0, 0.6), (0.09, 1.12), (0.19, 1.70), (0.06, 2.05)],
            [(0.16, 1.52), (0.52, 1.81), (0.76, 1.92)],
            [(-0.43, 0.51), (-0.88, 0.94), (-1.11, 1.00)],
            [(0.03, -0.58), (0.14, -1.31), (-0.20, -1.74)],
        ]:
            trace = VMobject(stroke_color=GREY, stroke_width=2.3)
            trace.set_points_as_corners([point(r * a, r * b) for a, b in vertices])
            branches.add(trace)
    elif kind == "glia":
        body.rotate(-0.6)
        body.set_fill(DEEP)
    nucleus = Circle(radius=0.40 * r, stroke_width=0, fill_color=NUCLEUS,
                     fill_opacity=1)
    if signal:
        nucleus.set_fill(interpolate_color(ManimColor(NUCLEUS), ManimColor(signal), strength))
    glow = Circle(radius=0.60 * r, stroke_color=signal or NUCLEUS,
                  stroke_width=3, stroke_opacity=0.85 * strength if signal else 0,
                  fill_color=signal or NUCLEUS, fill_opacity=0.17 * strength if signal else 0)
    return VGroup(branches, body, glow, nucleus).shift(point(x, y))


def cohort(positions, *, radius=0.43, signal=None, kind="neuron", strength=1.0):
    return VGroup(*(cell(x, y, radius, kind=kind, signal=signal, strength=strength)
                    for x, y in positions))


def collapse_branches_at_nucleus(recipient, neuron):
    """Give a cell invisible branches matching the neuron's path structure."""
    center = neuron[3].get_center()
    branches = neuron[0].copy().scale(0, about_point=center)
    branches.shift(recipient[3].get_center() - center).set_stroke(opacity=0)
    recipient[0].set_submobjects(list(branches))


def divide(scene, parents, daughters, *other_animations, run_time):
    splits = []
    for i, parent in enumerate(parents):
        twin = parent.copy()
        scene.add(twin)
        splits.extend((ReplacementTransform(parent, daughters[2 * i]),
                       ReplacementTransform(twin, daughters[2 * i + 1])))
    scene.play(*splits, *other_animations, run_time=run_time)


def drift(group, amp=0.13):
    for i, item in enumerate(group):
        bob(item, amp=amp, speed=1.55 + 0.16 * (i % 3), seed=i)
    return group


ADULT_ROWS = (
    (-5.0, 1.54), (-2.54, 1.74), (0.10, 1.48), (3.0, 1.62), (5.06, 1.44),
    (-4.52, -0.04), (-1.80, 0.05), (0.85, -0.30), (3.80, -0.05),
    (-5.07, -1.52), (-2.98, -1.43), (0, -1.76), (2.62, -1.6), (5.02, -1.48),
)
EARLY = ((-4.65, -0.64), (-3.45, -0.79), (-2.25, -0.61))
LATE = ((-3.92, 1.49), (-2.61, 1.56), (-1.30, 1.48))
PARENTS = ((-3.45, -1.64), (2.78, -1.64))
INJURED = ((-5.03, 1.42), (-3.65, 1.26), (-4.34, -0.46),
           (-2.67, -1.54), (4.51, 1.27), (4.98, -0.57), (3.72, -1.58))
INJURY_CELL = (0.06, -0.65)


def adult():
    return wall(), cohort(ADULT_ROWS, radius=0.41)


def birthday_wall():
    tissue = wall()
    others = cohort(((-4.94, 0.61), (0.30, 1.45), (2.05, 1.29), (4.74, 1.49),
                     (1.08, -0.50), (3.06, -0.74), (5.01, -0.45),
                     (-4.72, -1.88), (-0.17, -1.79), (4.0, -1.77)))
    return tissue, others


def injury_view(marked=False):
    tissue = wall(injured=True)
    neighbours = cohort(INJURED, radius=0.51)
    focal = cell(*INJURY_CELL, r=0.88, signal=YELLOW if marked else None)
    tag = boxed_label("BrdU+", YELLOW, 32).move_to(point(-0.07, -3.15))
    return tissue, neighbours, focal, tag


def pulse_wash():
    """An orange band travels across the section while label is available."""
    return VGroup(*[RoundedRectangle(width=w, height=4.98, corner_radius=0.24,
                                     stroke_width=0, fill_color=ORANGE, fill_opacity=a)
                    for w, a in [(2.15, 0.10), (1.45, 0.10), (0.69, 0.15)]]
                  ).move_to(point(-5.10, 0))


def time_strip(names, colors, active, *, ends=(-5.60, 5.60), y=-3.45, label_rise=0.39, label_size=29):
    """A schematic sequence without numerical time intervals."""
    xs = np.linspace(*ends, len(names))
    track = strip(xs[0], xs[-1], y, 3, GREY, 0.64)
    nodes = VGroup(*(Dot(point(x, y), radius=0.062, color=c)
                     for x, c in zip(xs, colors)))
    names = VGroup(*(label(name, x, y + label_rise, color, label_size)
                     for name, x, color in zip(names, xs, colors)))
    cursor = always_redraw(lambda: Dot(point(np.interp(active.get_value(),
                                                       np.arange(len(xs)), xs), y),
                                     radius=0.108, color=GOLD))
    return VGroup(track, nodes, names), cursor


def chromosome_bars(x, y):
    return VGroup(*[RoundedRectangle(width=0.11, height=h, corner_radius=0.05,
                                     fill_color=TEXT, fill_opacity=1, stroke_width=0)
                    .move_to(point(x + dx, y)) for dx, h in [(-0.22, 0.43), (0.18, 0.60)]])


class S01Hook(SpokenScene):
    def construct(self):
        tissue, neurons = adult()
        self.add(tissue, drift(neurons))
        self.at("which ones were", lead=0.65)
        q = question_card("Which ones were born first?", y=3.25, size=37).question
        self.play(FadeIn(q, shift=0.12 * UP), run_time=0.55)
        self.at("no date stamps")
        self.play(FadeOut(q), run_time=0.65)
        self.at("to learn when")
        preview = neurons[11]
        preview.clear_updaters()
        ring = Circle(radius=0.30, stroke_color=YELLOW, stroke_width=5).move_to(preview[3])
        self.play(Create(ring), run_time=2.35)
        self.at("into a clock")
        self.play(FadeOut(ring), run_time=0.7)
        self.finish()


class S02Title(TitleCard):
    TITLE = "Marking When a Cell Was Born"
    LESSON = "Birthdating with thymidine analogs"

    def construct(self):
        tissue, neurons = adult()
        self.add(tissue, drift(neurons))
        title = fit_text(self.TITLE, max_w=11.6, size=47, min_size=39,
                         font=TITLE_FONT).move_to(point(0, 3.17))
        self.play(FadeIn(title, shift=UP * 0.08), run_time=0.40)
        self.wait(1.15)
        self.play(FadeOut(title), run_time=0.45)


class S03Sphase(SpokenScene):
    def construct(self):
        tissue, adult_cells = adult()
        self.add(tissue, adult_cells)
        mature = cell(-3.48, 0.91, 0.64)
        progenitors = cohort(PARENTS, radius=0.84, kind="progenitor")
        x, y = PARENTS[0]
        bars = chromosome_bars(x, y)
        other_bars = chromosome_bars(*PARENTS[1])
        other_bars.add(*chromosome_bars(*PARENTS[1]).shift(RIGHT * 0.15))
        self.at("a dividing cell")
        self.play(FadeOut(adult_cells), FadeIn(mature), FadeIn(progenitors),
                  FadeIn(bars), FadeIn(other_bars), run_time=0.75)
        self.at("copies its dna")
        paired = bars.copy()
        self.add(paired)
        self.play(bars.animate.shift(LEFT * 0.085).stretch(1.16, 1),
                  paired.animate.shift(RIGHT * 0.085).stretch(1.16, 1),
                  progenitors[0].animate.scale(1.24), run_time=2.0)
        self.at("in s phase")
        s_phase = label("S phase", -3.45, -3.12, BLUE)
        self.play(FadeIn(s_phase), progenitors[0].animate.scale(1 / 1.24), run_time=0.95)
        self.at("a neuron that", lead=0.55)
        mature_tag = label("Mature neuron", -3.48, color=TEXT)
        outline = Ellipse(width=1.43, height=1.54, stroke_color=BLUE,
                          stroke_width=3, stroke_opacity=0.75).move_to(point(-3.48, 0.91))
        focus = Ellipse(width=2.9, height=3.08, stroke_width=0,
                        fill_color=BLUE, fill_opacity=0.18).move_to(point(-3.48, 0.91))
        focus.set_z_index(1)
        mature.set_z_index(2)
        self.play(GrowFromCenter(focus), run_time=1.10)
        self.play(Create(outline), FadeIn(mature_tag), run_time=1.75)
        self.at("not copy its")
        self.play(FadeOut(outline), FadeOut(focus), run_time=1.38)
        self.at("biologists give a", lead=0.30)
        pulse_tag = label("Pulse", color=ORANGE)
        wash = pulse_wash()
        self.play(FadeOut(mature_tag), FadeOut(s_phase), FadeIn(wash), run_time=0.50)
        self.play(FadeIn(pulse_tag), wash.animate.move_to(point(-1.2, 0)), run_time=1.62)
        self.at("a labeled dna")
        dots = VGroup(*(Dot(point(a + dx, b + dy), radius=0.064, color=YELLOW)
                        for a, b in PARENTS
                        for dx, dy in [(-0.61, 0.62), (0.52, 0.67), (0.53, -0.62)]))
        end = VGroup(*(Dot(point(a + dx, b + dy), radius=0.064, color=YELLOW)
                       for a, b in PARENTS
                       for dx, dy in [(-0.19, 0.13), (0.22, 0.23), (0.16, -0.13)]))
        self.play(FadeIn(dots), wash.animate.move_to(point(2.18, 0)), run_time=2.54)
        self.at("because thymidine goes")
        self.play(Transform(dots, end), wash.animate.move_to(point(5.14, 0)), run_time=2.9)
        self.at("cell in s phase")
        glowing = cohort(PARENTS, radius=0.84, signal=YELLOW, kind="progenitor")
        self.play(Transform(progenitors, glowing), FadeOut(dots), FadeOut(bars),
                  FadeOut(paired), FadeOut(other_bars), FadeOut(wash), run_time=1.30)
        self.finish()


class S04Chase(SpokenScene):
    def construct(self):
        tissue = wall()
        mature = cell(-3.48, 0.91, 0.64)
        parents = cohort(PARENTS, radius=0.84, signal=YELLOW, kind="progenitor")
        self.add(tissue, mature, *parents)
        active = ValueTracker(0)
        time, cursor = time_strip(("Pulse", "Chase"), (ORANGE, TEXT), active, ends=(-3.6, 3.6))
        self.at("next comes the")
        wash_end = section_band(2.57, -2.57, ORANGE).set_fill(opacity=0.17)
        self.play(FadeIn(time), FadeIn(cursor), FadeIn(wash_end), run_time=0.75)
        self.at("the label is gone")
        self.play(active.animate.set_value(1), FadeOut(wash_end), run_time=2.9, rate_func=linear)
        self.at("labeled progenitor that")
        left_daughters = cohort(((-4.03, -1.53), (-2.87, -1.53)), radius=0.54,
                                signal=YELLOW, kind="progenitor", strength=0.85)
        divide(self, [parents[0]], left_daughters, run_time=2.8)
        self.remove(*left_daughters)
        self.add(left_daughters)
        self.at("passes heavy label")
        left_tag = label("Last division", -3.45, color=YELLOW)
        birth_focus = Ellipse(width=3.15, height=1.63, stroke_width=0,
                              fill_color=YELLOW, fill_opacity=0.28).move_to(point(-3.45, -1.53))
        tissue.set_z_index(-2)
        birth_focus.set_z_index(-1)
        self.play(FadeIn(left_tag), GrowFromCenter(birth_focus),
                  left_daughters.animate.stretch(1.10, 0), run_time=1.38)
        self.at("those newborn neurons")
        rising = cohort(((-4.15, -1.02), (-2.75, -0.85)), radius=0.49,
                        signal=YELLOW, strength=0.85)
        landed = cohort(((-4.15, -0.52), (-2.75, -0.27)), radius=0.49,
                        signal=YELLOW, strength=0.85)
        for daughter, neuron in zip(left_daughters, rising):
            collapse_branches_at_nucleus(daughter, neuron)
        self.play(Transform(left_daughters, rising), FadeOut(mature),
                  FadeOut(birth_focus, shift=UP * 0.63), run_time=2.55)
        self.at("stay heavily labeled")
        self.play(Transform(left_daughters, landed), run_time=2.4)
        self.at("progenitors that keep", lead=0.45)
        amount = ValueTracker(1)
        x, y = 3.00, 0.57
        frame = RoundedRectangle(width=4.24, height=0.40, corner_radius=0.09,
                                 stroke_width=2.5, stroke_color=YELLOW).move_to(point(x, y))
        bar = always_redraw(lambda: Rectangle(width=4.03 * amount.get_value(), height=0.21,
                                               fill_color=YELLOW, fill_opacity=1, stroke_width=0)
                            .move_to(point(x - 2.015 + 2.015 * amount.get_value(), y)))
        bar_label = label("Label per daughter", x, color=YELLOW, size=31)
        self.play(FadeIn(frame), FadeIn(bar), FadeIn(bar_label), run_time=0.60)
        self.at("split that label")
        first = cohort(((2.13, -1.47), (3.43, -1.47)), radius=0.51,
                       kind="progenitor", signal=YELLOW, strength=0.50)
        second = cohort(((1.55, -1.57), (2.45, -1.57), (3.35, -1.57), (4.25, -1.57)),
                        radius=0.38, kind="progenitor", signal=YELLOW, strength=0.25)
        divide(self, [parents[1]], first, amount.animate.set_value(0.5), run_time=1.16)
        divide(self, first, second, amount.animate.set_value(0.25), run_time=1.20)
        self.finish()


class S05Birthday(SpokenScene):
    def construct(self):
        tissue, others = birthday_wall()
        arriving = ((-4.15, -0.52), (-2.75, -0.27))
        early = cohort(arriving, radius=0.49, signal=YELLOW, strength=0.85)
        self.add(tissue, others, early)
        self.at("heavy label therefore")
        self.play(Transform(early, cohort(EARLY, signal=YELLOW)), run_time=1.65)
        self.at("approximate last s")
        last = label("Approximate last S phase", -0.3, color=YELLOW)
        self.play(FadeIn(last), run_time=0.70)
        drift(early, amp=0.10)
        drift(others)
        self.at("in the cortical")
        late = cohort(((-4.12, -1.55), (-2.61, -1.67), (-1.51, -1.62)), signal=PURPLE)
        self.play(FadeIn(late), run_time=0.75)
        self.at("earlier birthdays settle")
        early_label = label("Earlier pulse", -3.48, -3.16, YELLOW, 30)
        later_label = label("Later pulse", 2.35, -3.16, PURPLE, 30)
        self.play(FadeIn(early_label), run_time=0.57)
        self.play(Transform(late, cohort(LATE, signal=PURPLE)), run_time=2.50)
        self.play(FadeIn(later_label), run_time=0.55)
        drift(late, amp=0.10)
        self.at("early work used")
        labels = VGroup(
            boxed_label("Tritiated thymidine", YELLOW, 29),
            boxed_label("BrdU", ORANGE, 29),
            boxed_label("EdU", BLUE, 29),
        ).arrange(RIGHT, buff=0.65).move_to(point(0, -3.22))
        self.play(FadeOut(last), FadeOut(early_label), FadeOut(later_label), run_time=0.50)
        self.play(FadeIn(labels[0]), run_time=0.60)
        self.at("followed later by")
        self.play(FadeIn(labels[1]), run_time=0.63)
        self.at("a newer mimic")
        self.play(FadeIn(labels[2]), run_time=0.63)
        self.at("clique chemistry")
        fluoresce = Circle(radius=0.34, stroke_color=BLUE, stroke_width=5).move_to(
            labels[2].get_right() + RIGHT * 0.62)
        self.play(Create(fluoresce), run_time=1.25)
        self.at("attaches a fluorescent")
        self.play(fluoresce.animate.set_fill(BLUE, 0.78), run_time=1.0)
        self.finish()


class S06PredictQ(SpokenScene):
    def construct(self):
        tissue, others = birthday_wall()
        marked = VGroup(cohort(EARLY, signal=YELLOW), cohort(LATE, signal=PURPLE))
        self.add(tissue, drift(others), marked)
        self.at("a glowing nucleus")
        dim = []
        for group in marked:
            for branches, body, glow, nucleus in group:
                dim.append(branches.animate.set_stroke(opacity=0.54))
                dim.extend(part.animate.set_opacity(0.54) for part in (body, glow, nucleus))
        self.play(*dim, run_time=1.50)
        self.at("picture an injured", lead=0.55)
        damaged, neighbours, focal, tag = injury_view()
        self.play(FadeOut(others), FadeOut(marked), ReplacementTransform(tissue, damaged),
                  FadeIn(neighbours), FadeIn(focal), run_time=2.2)
        self.at("after a pulse", lead=0.5)
        wash = pulse_wash()
        self.play(FadeIn(wash), run_time=0.3)
        self.play(wash.animate.move_to(point(4.98, 0)), run_time=1.58)
        highlighted = cell(*INJURY_CELL, r=0.88, signal=YELLOW)
        self.play(FadeOut(wash), Transform(focal, highlighted), run_time=0.95)
        self.at("nucleus appears", lead=0.3)
        self.play(FadeIn(tag), run_time=0.65)
        self.at("must that cell", lead=0.45)
        question = question_card(QUESTION, **QUESTION_POSITION)
        self.play(FadeIn(question), run_time=0.54)
        self.finish()


class S07PredictWait(PredictPause):
    QUESTION = QUESTION
    CARD = QUESTION_POSITION
    SECONDS = 4.5

    def construct(self):
        tissue, neighbours, focal, tag = injury_view(marked=True)
        self.add(tissue, neighbours, focal, tag, question_card(self.QUESTION, **self.CARD))
        pulse(focal[2], base=3.3, amp=0.9, speed=2.4)
        track = Rectangle(width=11.6, height=0.12, stroke_width=0,
                          fill_color=GREY, fill_opacity=0.40).move_to(point(0, -3.65))
        elapsed = ValueTracker(0.001)
        progress = always_redraw(lambda: Rectangle(width=elapsed.get_value(), height=track.height,
                                                    stroke_width=0, fill_color=GOLD, fill_opacity=1)
                                  .align_to(track, LEFT).set_y(track.get_y()))
        self.add(track, progress)
        self.play(elapsed.animate.set_value(track.width), run_time=self.SECONDS, rate_func=linear)


def microscope_field():
    """The same two touching cells, resolved at two levels of detail."""
    nerve = cell(-0.83, -0.13, r=1.07)
    glia = cell(0.66, -0.50, r=0.82, kind="glia", signal=YELLOW)
    field = Circle(radius=2.28, stroke_color=BLUE, stroke_width=4,
                   fill_color=WALL, fill_opacity=1).move_to(point(0, 0))
    halo = VGroup(*(Ellipse(width=w, height=h, stroke_width=0,
                            fill_color=YELLOW, fill_opacity=a).move_to(point(0.34, -0.43))
                    for w, h, a in [(3.18, 1.62, 0.10), (2.65, 1.41, 0.11),
                                    (1.94, 1.16, 0.14), (1.22, 0.93, 0.20)]))
    return field, nerve, glia, halo


class S08ControlsLimits(SpokenScene):
    def construct(self):
        tissue, neighbours, focal, tag = injury_view(marked=True)
        q = question_card(QUESTION, **QUESTION_POSITION)
        self.add(tissue, neighbours, focal, tag, q)
        self.at("now")
        inset = Circle(radius=1.64, stroke_color=BLUE, stroke_width=4,
                       fill_color=DEEP, fill_opacity=1).move_to(point(0, 0.16))
        self.play(FadeOut(q), FadeOut(tag), GrowFromPoint(inset, point(*INJURY_CELL)), run_time=1.60)
        self.at("repair also builds", lead=0.58)
        # Two blocks stand for the stretches of DNA on either side of a break.
        left = strip(-1.63, -0.36, 0.18, 18, NUCLEUS)
        right = strip(0.36, 1.63, 0.18, 18, NUCLEUS)
        patch = strip(-0.36, 0.36, 0.18, 18, YELLOW)
        self.play(inset.animate.scale(2.15 / 1.64), Create(left), Create(right), run_time=1.10)
        self.at("short new dna")
        repair_focus = Ellipse(width=2.00, height=1.28, stroke_width=0,
                               fill_color=YELLOW, fill_opacity=0.27).move_to(point(0, 0.18))
        self.play(GrowFromCenter(repair_focus), Create(patch), run_time=1.95)
        self.at("that analogs can")
        repair = label("DNA repair", color=YELLOW)
        self.play(FadeIn(repair), run_time=0.65)
        self.at("in injured tissue")
        ambig = boxed_label("S phase?", RED, 32).move_to(point(4.43, 3.23))
        glowing_patch = strip(-0.36, 0.36, 0.18, 34, YELLOW, 0.32)
        self.play(VGroup(inset, left, right, repair_focus, patch).animate.shift(LEFT * 1.62),
                  glowing_patch.animate.shift(LEFT * 1.62), FadeIn(ambig), run_time=2.35)
        self.bring_to_front(patch)
        self.at("separate repair from")
        strike = Line(ambig.get_corner(DL) + point(-0.12, -0.12),
                      ambig.get_corner(UR) + point(0.12, 0.12), color=RED, stroke_width=5)
        strike.layout_ok = {"covered", "straddle"}
        self.play(Create(strike), run_time=0.9)
        self.at("cell cycle evidence")
        evidence = boxed_label("Cell-cycle evidence", GREEN, 31).move_to(point(0, -3.14))
        self.play(FadeIn(evidence, shift=UP * 0.23), run_time=1.12)
        self.at("nor is a birth")
        field, nerve, glia, halo = microscope_field()
        context = VGroup(inset, left, right, repair_focus, patch, glowing_patch, repair, ambig, strike, evidence, focal)
        self.play(FadeOut(context), FadeOut(neighbours), run_time=0.60)
        field_contents = VGroup(field, nerve, glia, halo)
        field_contents.shift(LEFT * 0.65)
        self.play(GrowFromPoint(field, point(0.07, -0.15)), run_time=1.36)
        self.play(FadeIn(nerve), FadeIn(halo), run_time=0.70)
        self.at("under a light")
        optical = label("Light microscope", color=BLUE)
        self.play(FadeIn(optical), run_time=0.50)
        self.at("label might belong")
        visible_field = VGroup(field, nerve, halo)
        glia.shift(RIGHT * 0.65)
        self.play(visible_field.animate.shift(RIGHT * 0.65), run_time=2.16)
        self.at("a support cell")
        self.play(FadeIn(glia), halo.animate.set_opacity(0.21), run_time=1.8)
        self.at("confirming cell type")
        cells = VGroup(field, nerve, glia)
        self.play(FadeOut(halo), cells.animate.scale(1.08, about_point=ORIGIN), run_time=1.8)
        self.at("like electron microscopy", lead=0.45)
        self.play(swap(optical, label("Electron microscopy", color=BLUE), run_time=0.80))
        glia_tag = label("Labelled glial cell", 3.85, -3.19, YELLOW, 31)
        nerve_tag = label("Unlabelled neuron", -3.85, -3.19, TEXT, 31)
        self.play(FadeIn(glia_tag), FadeIn(nerve_tag), run_time=0.62)
        self.finish()


def trail(points, color=YELLOW):
    path = VMobject(stroke_color=color, stroke_width=4, stroke_opacity=0.75)
    path.set_points_smoothly([point(x, y) for x, y in points])
    return path


class S09UnlockedNeuro(SpokenScene):
    def construct(self):
        tissue, other = birthday_wall()
        other.remove(other[7])
        self.add(tissue, drift(other))
        neuron = cell(-2.62, 0.36, 0.70, signal=YELLOW)
        self.at("that check showed")
        self.play(GrowFromCenter(neuron), run_time=1.35)
        trace_time = ValueTracker(0)
        time, cursor = time_strip(("1960s\nAltman", "1977\nKaplan & Hinds",
                                  "1983\nGoldman & Nottebohm"), (GOLD, GOLD, GOLD),
                                 trace_time, ends=(-4.62, 3.94), y=-3.70, label_rise=0.48, label_size=28)
        self.at("in the 1960s")
        self.play(FadeIn(time[0]), FadeIn(time[1]), FadeIn(time[2][0]),
                  FadeIn(cursor), run_time=0.74)
        self.at("found labeled cells")
        dentate = cohort(((-4.26, 0.21), (-3.58, 0.46)), radius=0.30, signal=YELLOW,
                         kind="progenitor")
        self.play(FadeIn(dentate), run_time=0.74)
        self.at("rat dentate gyrus")
        dentate_tag = label("Rat dentate gyrus", -3.66, color=TEXT, size=31)
        self.play(FadeIn(dentate_tag), run_time=0.65)
        self.at("moving toward the", lead=0.38)
        rat_path = trail([(-1.5, -1.67), (-0.1, -1.0), (1.42, -0.38), (3.80, 0.98)])
        rat_cell = cell(-1.5, -1.67, 0.38, signal=YELLOW, kind="progenitor")
        bulb = label("Toward the olfactory bulb", 3.36, color=TEXT, size=30)
        self.add(rat_cell)
        self.play(Create(rat_path, rate_func=linear), MoveAlongPath(rat_cell, rat_path, rate_func=linear),
                  FadeIn(bulb, rate_func=squish_rate_func(smooth, 0, 0.53 / 1.85)),
                  run_time=1.85)
        self.at("in 1977")
        self.play(FadeOut(dentate_tag), FadeOut(bulb), FadeIn(time[2][1]), trace_time.animate.set_value(1), run_time=1.47)
        self.at("used electron microscopy", lead=0.5)
        lens = Circle(radius=1.12, stroke_color=BLUE, stroke_width=5).move_to(neuron[1])
        scope = label("Electron microscopy", -2.3, color=BLUE, size=32)
        self.play(Create(lens), run_time=0.83)
        self.play(FadeIn(scope), run_time=0.50)
        self.at("confirm they were")
        confirmed = label("✓", -1.01, 0.93, GREEN, 52)
        self.play(FadeIn(confirmed, scale=0.7), run_time=0.78)
        self.at("in 1983")
        self.play(FadeOut(lens), FadeOut(neuron), FadeOut(confirmed), FadeOut(scope), FadeOut(dentate),
                  FadeOut(rat_path), FadeOut(rat_cell), FadeIn(time[2][2]), trace_time.animate.set_value(2), run_time=1.35)
        self.at("tracked new adult")
        bird_cells = cohort(((-1.5, -2.05), (-2.04, -2.04)), radius=0.30,
                            signal=YELLOW, kind="progenitor")
        start_x, start_y, _ = bird_cells.get_center()
        bird_path = trail([(start_x, start_y), (-0.45, -1.18), (0.71, 0.11), (3.35, 1.39)])
        ventricle = label("Canary ventricle", -3.61, color=TEAL, size=30)
        self.play(FadeIn(bird_cells), run_time=0.57)
        self.play(FadeIn(ventricle), run_time=0.54)
        self.at("from ventricle to", lead=0.43)
        self.play(Create(bird_path), MoveAlongPath(bird_cells, bird_path), run_time=1.53, rate_func=linear)
        self.at("song nucleus hvc", lead=0.3)
        song = label("Song nucleus HVC", 2.74, color=TEXT, size=32)
        self.play(swap(ventricle, song, run_time=0.75))
        self.finish()


def clone_panel_data(x, *, expanded=False):
    basal = [(x - 0.58, -0.65), (x + 0.43, -0.65)]
    upper = [(x - 0.68, 0.46), (x + 1.38, 0.84)]
    if expanded:
        basal = [(x - 1.38, -0.67), (x - 0.46, -0.67),
                 (x + 0.46, -0.67), (x + 1.38, -0.67)]
        upper = [(x + 0.67, 0.61)]
    return basal, upper


class S10UnlockedFate(SpokenScene):
    def construct(self):
        tissue = wall(basal=True)
        self.add(tissue)
        left, right = -3.22, 3.22
        phase = ValueTracker(0)
        timeline, cursor = time_strip(("Short EdU pulse", "Chase"), (ORANGE, TEXT),
                                     phase, ends=(-3.55, 3.55), y=-3.55)
        comparator = TwoPanel("Control", "Reduced Notch1", colors=(GREY, TEAL),
                              top=2.62, bottom=-2.55, width=12.22, size=32)
        basal_l, upper_l = clone_panel_data(left)
        basal_r, upper_r = clone_panel_data(right)
        control = cohort(basal_l + upper_l, radius=0.41, kind="progenitor")
        test = cohort(basal_r + upper_r, radius=0.41, kind="progenitor")
        self.at("edu can also")
        self.play(FadeIn(timeline), FadeIn(cursor), FadeIn(control), FadeIn(test), run_time=1.15)
        self.at("division speed from")
        wash = pulse_wash().stretch_to_fit_height(3.65)
        self.play(FadeIn(wash), run_time=0.30)
        seeded_l = VGroup(*cohort(basal_l, radius=0.41, signal=YELLOW, kind="progenitor"),
                          *cohort(upper_l, radius=0.41, kind="progenitor"))
        seeded_r = VGroup(*cohort(basal_r, radius=0.41, signal=YELLOW, kind="progenitor"),
                          *cohort(upper_r, radius=0.41, kind="progenitor"))
        self.play(Transform(control, seeded_l), Transform(test, seeded_r),
                  wash.animate.move_to(point(5.10, 0)), run_time=2.35)
        self.at("a short pulse")
        caveat = fit_text("Also depends on S-phase length and cycling cells",
                          size=30, min_size=28).move_to(point(0, 3.25))
        self.play(FadeIn(caveat), FadeOut(wash), run_time=1.05)
        self.at("a chase shows")
        focus = VGroup(*(Ellipse(width=1.50, height=1.95, stroke_width=0,
                                  fill_color=YELLOW, fill_opacity=0.30)
                         .move_to(point(x + 0.43, -0.58)) for x in (left, right)))
        tissue.set_z_index(-2)
        focus.set_z_index(-1)
        self.play(FadeIn(focus), run_time=0.55)
        chased_l = cell(left + 0.43, 0.58, 0.41, signal=YELLOW)
        chased_r = cell(right + 0.43, 0.58, 0.41, signal=YELLOW)
        collapse_branches_at_nucleus(control[1], chased_l)
        collapse_branches_at_nucleus(test[1], chased_r)
        self.play(phase.animate.set_value(1), focus.animate.shift(UP * 1.20),
                  Transform(control[1], chased_l), Transform(test[1], chased_r),
                  run_time=2.25)
        self.at("in 2023")
        study = label("2023 · Abby & colleagues", color=GOLD)
        collapse_branches_at_nucleus(seeded_l[1], chased_l)
        collapse_branches_at_nucleus(seeded_r[1], chased_r)
        self.play(swap(caveat, study), FadeIn(comparator), FadeOut(focus),
                  Transform(control, seeded_l), Transform(test, seeded_r), run_time=1.07)
        self.at("tracked mouse clones")
        left_wash, right_wash = [
            pulse_wash().stretch_to_fit_width(1.18).stretch_to_fit_height(3.64)
            .move_to(point(x - 1.92, 0)) for x in (left, right)
        ]
        self.play(FadeIn(left_wash), FadeIn(right_wash), phase.animate.set_value(0), run_time=0.75)
        match = label("Similar pulse labelling", 0, -2.82, YELLOW, 30)
        self.play(FadeIn(match), left_wash.animate.shift(RIGHT * 1.92),
                  right_wash.animate.shift(RIGHT * 1.92), run_time=1.40)
        self.at("copies of notch1")
        self.play(left_wash.animate.shift(RIGHT * 1.92),
                  right_wash.animate.shift(RIGHT * 1.92), run_time=1.38)
        self.play(FadeOut(left_wash), FadeOut(right_wash), run_time=0.48)
        self.at("the clones expanded", lead=0.33)
        new_basal_r, new_upper_r = clone_panel_data(right, expanded=True)
        expanded_basal = cohort(new_basal_r, radius=0.38, signal=YELLOW, kind="progenitor")
        expanded_upper = cell(*new_upper_r[0], r=0.44, signal=YELLOW)
        known = VGroup(*cohort(basal_l, radius=0.38, signal=YELLOW, kind="progenitor"),
                       *cohort(upper_l, radius=0.44, signal=YELLOW))
        self.play(FadeOut(match), phase.animate.set_value(1), run_time=1.06)
        for source, target in zip((*control[2:], test[3]), (*known[2:], expanded_upper)):
            collapse_branches_at_nucleus(source, target)
        divide(self, test[:2], expanded_basal, Transform(control, known),
               FadeOut(test[2]), ReplacementTransform(test[3], expanded_upper), run_time=2.4)
        self.at("tracking fit more", lead=0.35)
        fate = label("More basal progenitors", 3.10, -1.81, TEAL, 30)
        self.play(FadeIn(fate), run_time=0.63)
        drift(expanded_basal, amp=0.12)
        self.at("fate not speed")
        self.play(swap(study, label("Fate, not speed", color=GOLD)), run_time=0.77)
        self.finish()


class S11Return(SpokenScene):
    def construct(self):
        tissue, others = birthday_wall()
        early = cohort(EARLY, signal=YELLOW)
        late = cohort(LATE, signal=PURPLE)
        self.add(tissue, drift(others))
        self.at("across tissues")
        self.play(FadeIn(early, shift=0.28 * UP), FadeIn(late, shift=0.42 * UP), run_time=1.44)
        drift(early, amp=0.11)
        drift(late, amp=0.11)
        active = ValueTracker(0)
        time, cursor = time_strip(("Timed pulse", "Chase"), (ORANGE, TEXT), active, ends=(-4.66, 0.12))
        self.at("dna pulse with")
        self.play(FadeIn(time), FadeIn(cursor), run_time=0.7)
        self.play(active.animate.set_value(1), run_time=1.6, rate_func=linear)
        self.at("heavy label records")
        bracket = VGroup(strip(-5.68, -3.66, -2.76, 3, YELLOW),
                         Line(point(-5.68, -2.76), point(-5.68, -2.61), stroke_width=3, color=YELLOW),
                         Line(point(-3.66, -2.76), point(-3.66, -2.61), stroke_width=3, color=YELLOW))
        last = label("Last division", -4.63, -3.06, YELLOW, 29)
        self.play(Create(bracket), run_time=0.55)
        self.play(swap(time[2][0], last, run_time=0.60))
        self.at("what the cell became")
        note = boxed_label("✓  Identity check", GREEN, 31).move_to(point(3.75, -3.18))
        verified = VMobject(stroke_color=GREEN, stroke_width=5)
        verified.set_points_as_corners([point(-1.62, -0.34), point(-1.46, -0.50), point(-1.15, -0.15)])
        self.play(Create(verified), run_time=0.70)
        self.play(FadeIn(note), run_time=0.80)
        self.finish()


class S12End(EndCard):
    LINE = "A DNA pulse marks when cells stopped dividing, not their identity."
