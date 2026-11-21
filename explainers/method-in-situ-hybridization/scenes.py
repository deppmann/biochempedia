"""In situ hybridization, from a matching tile to a map of the retina."""

from bp_parts import *
from bp_style import EndCard

# Color map: gray for tissue and the gene, blue for RNA, yellow for probe
# and signal, green for the cell-shape overlay, and white for labels and light.
TISSUE = ("#49505D", "#424B58", "#39424F", "#303845")
CELL_FILL = "#657184"
CELL_EDGE = "#AAB3C1"
CLOSE_FILL = "#394453"
STACK_X = -2.20
ROWS = (2.05, 0.75, -0.55, -1.85)
RAIL_X = 4.27
FOCUS = (1, 2)
EXAMPLE_CELLS = ((0, 0), (0, 3), FOCUS)
RESEARCH_CELLS = ((0, 1), (1, 2))
GANGLION_CELLS = ((0, 1), (0, 3))
RNA_HOME = np.array([1.00, 0.74, 0])
PROBE_BOUND = RNA_HOME + DOWN * 0.88
PROBE_ENTRY = np.array([3.25, -0.95, 0])
WRONG_EXIT = np.array([-1.22, -1.04, 0])
QUESTION = "Where will marks appear?"


def point(x, y):
    return np.array([x, y, 0])


def schematic():
    return scope_tag(size=28, color=TEXT).move_to(point(5.05, -3.39))


def rail(text, y=0.60, color=TEXT, size=34, max_w=4.60):
    return fit_text(text, max_w=max_w, size=size, min_size=28,
                    color=color).move_to(point(RAIL_X, y))


def cell(center, width, height, fill=CELL_FILL, stroke=CELL_EDGE):
    return Ellipse(width=width, height=height, fill_color=fill, fill_opacity=1,
                   stroke_color=stroke, stroke_width=2.4).move_to(center)


def signal(center, radius=0.15):
    return VGroup(
        Dot(center, radius=radius * 2.0, color=YELLOW, fill_opacity=0.23),
        Dot(center, radius=radius, color=YELLOW),
    ).set_z_index(4)


def retina():
    """Return four tissue layers and their fixed cell locations, innermost first."""
    layers, cells = VGroup(), VGroup()
    for i, y in enumerate(ROWS):
        layers.add(RoundedRectangle(
            width=7.65, height=1.22, corner_radius=0.17, stroke_width=0,
            fill_color=TISSUE[i], fill_opacity=1,
        ).move_to(point(STACK_X, y)))
        row = VGroup()
        for j, x in enumerate((-4.91, -3.12, -1.30, 0.51)):
            offset = 0.10 if (i + j) % 2 else -0.09
            row.add(cell(point(x + (0.12 if i % 2 else 0), y + offset),
                         1.28 - 0.11 * i, 0.76 + 0.07 * (j % 2)))
        cells.add(row)
    return VGroup(layers, cells.set_z_index(1))


def spots(section, locations):
    return VGroup(*(signal(section[1][i][j].get_center()) for i, j in locations))


def lift(color, strength):
    return interpolate_color(ManimColor(color), ManimColor(TEXT), strength)


def light_layers(section, rows, strength):
    return [section[0][i].animate.set_fill(lift(TISSUE[i], strength)) for i in rows]


def focus_outline(section):
    return SurroundingRectangle(section[1][FOCUS[0]][FOCUS[1]], buff=0.11,
                                corner_radius=0.15, color=TEXT, stroke_width=2).set_z_index(3)


def context():
    section = retina().scale(0.33).move_to(point(-4.87, 0.10))
    return section, focus_outline(section)


def cell_closeup():
    """The common close-up, anchored to the same cell in the retina inset."""
    return cell(point(1.37, 0.10), 8.65, 5.48, fill=CLOSE_FILL).set_z_index(2)


def eye():
    center = point(STACK_X, 0.04)
    shape = cell(center, 7.10, 5.21, fill="#303A48")
    iris = cell(center + LEFT * 2.39, 0.61, 2.88, fill="#475465")
    back = ParametricFunction(
        lambda t: center + point(3.29 * np.cos(t), 2.39 * np.sin(t)),
        t_range=(-0.90, 0.90), color=TEXT, stroke_width=7,
    )
    return VGroup(shape, iris).set_z_index(-1), back.set_z_index(3)


def tile(role, center):
    """Flat schematic pieces with complementary edges for the RNA and matching probe."""
    width, half_height, tab = 1.55, 0.44, 0.19
    if role == "gene":
        return RoundedRectangle(width=2 * width, height=2 * half_height,
                                corner_radius=0.13, stroke_color=CELL_EDGE, stroke_width=2,
                                fill_color=CELL_FILL, fill_opacity=1).move_to(center).set_z_index(3)
    color = BLUE if role == "rna" else YELLOW
    lower_left, lower_right = (-width, -half_height), (width, -half_height)
    upper_right, upper_left = (width, half_height), (-width, half_height)
    if role == "rna":
        edge = ((-0.43, -half_height), (-0.26, -half_height - tab),
                (0.26, -half_height - tab), (0.43, -half_height))
        corners = (lower_left, *edge, lower_right, upper_right, upper_left)
    else:
        offset = 0.78 if role == "wrong" else 0
        edge = ((0.43 + offset, half_height), (0.26 + offset, half_height - tab),
                (-0.26 + offset, half_height - tab), (-0.43 + offset, half_height))
        corners = (lower_left, lower_right, upper_right, *edge, upper_left)
    piece = Polygon(*(center + point(x, y) for x, y in corners),
                    stroke_width=0, fill_color=color, fill_opacity=1).set_z_index(3)
    if role == "rna":
        return piece
    badge_at = center + point(1.07 if role == "probe" else -1.07, 0)
    badge = Dot(badge_at, color=YELLOW, radius=0.22, stroke_color=BG, stroke_width=2.5)
    return VGroup(piece, badge).set_z_index(3)


def above(text, target, color=TEXT):
    return place_label(T(text, 31, color), target, dirs=(UP,), buff=0.24)


def below(text, target, color=TEXT):
    return place_label(T(text, 31, color), target, dirs=(DOWN,), buff=0.24)


def close_world(probe=None, rna=True):
    section, anchor = context()
    return (
        section, anchor, cell_closeup(),
        tile("rna", RNA_HOME) if rna else None,
        tile(probe, PROBE_BOUND if probe == "probe" else WRONG_EXIT) if probe else None,
    )


def question_mark():
    return T("?", size=116, color=YELLOW, font=TITLE_FONT).move_to(point(RAIL_X, 0.65))


def predict_labels():
    inner = rail("Inner layers", y=2.06)
    question = question_card(QUESTION, y=-0.75, size=32, max_w=4.50,
                             color=YELLOW).question.move_to(point(RAIL_X, -0.75))
    return inner, question_mark(), question


def pair_of_cells(section):
    """Representative ganglion-layer close-ups, with no cell-type assignment."""
    specimen = VGroup(*(section[1][i][j].copy() for i, j in GANGLION_CELLS))
    close = VGroup(
        cell(point(-3.45, 0.15), 4.80, 4.55, fill=CLOSE_FILL),
        cell(point(2.56, 0.15), 4.80, 4.55, fill=CLOSE_FILL),
    )
    return specimen.set_z_index(2), close.set_z_index(2)


class S01Question(SpokenScene, TitleCard):
    LESSON = "In Situ Hybridization"
    TITLE = "Finding a Gene’s Message in Tissue"

    def construct(self):
        section = retina()
        mark = T("?", 100, YELLOW, font=TITLE_FONT).move_to(point(3.82, 1.97))
        self.add(section, schematic(), mark)
        self.at("which cells")
        self.play(mark.animate.move_to(point(4.61, -1.47)), run_time=2.50)

        self.at("the retina is", lead=1.24)
        title = fit_text(self.TITLE, max_w=4.60, size=38, min_size=30,
                         font=TITLE_FONT).move_to(point(RAIL_X, 0.58))
        lesson = above(self.LESSON, title)
        self.play(FadeOut(mark), run_time=0.25)
        self.play(FadeIn(lesson), FadeIn(title), run_time=0.30)
        self.wait(1.05)
        self.play(FadeOut(lesson), FadeOut(title), run_time=0.28)

        self.at("layered tissue", lead=0.28)
        globe, section_trace = eye()
        small_section = retina().scale(0.22).rotate(PI / 2).move_to(point(0.05, 0.04))
        self.play(FadeIn(globe), Transform(section, small_section),
                  run_time=1.30)
        self.at("back of the eye", lead=0.22)
        self.play(Create(section_trace), run_time=1.02)
        eye_label = rail("Retina", y=0.60)
        self.play(FadeIn(eye_label), run_time=0.33)

        self.at("cells are still")
        self.play(FadeOut(globe), FadeOut(section_trace), Transform(section, retina()),
                  run_time=2.27)
        self.at("messages are too small")
        outline = focus_outline(section)
        self.play(Create(outline), *light_layers(section, [1], 0.23), run_time=1.54)
        self.at("need a way")
        self.play(FadeOut(eye_label), FadeOut(outline), *light_layers(section, [1], 0),
                  run_time=2.55)
        self.finish()


class S02Message(SpokenScene):
    def construct(self):
        section = retina()
        inset, anchor, close, _, _ = close_world(rna=False)
        selected = section[1][FOCUS[0]][FOCUS[1]].copy().set_z_index(2)
        self.add(section, schematic(), selected)
        self.at("zoom into a cell")
        self.play(Transform(section, inset), Transform(selected, close), run_time=2.62)
        self.play(Create(anchor), run_time=0.53)

        self.at("a cell can make")
        gene = tile("gene", point(-0.67, 0.93))
        gene_label = T("Gene", 31, TEXT).move_to(gene).set_z_index(5)
        self.play(FadeIn(gene, shift=RIGHT * 0.30), run_time=0.75)
        self.play(FadeIn(gene_label), run_time=0.31)
        rna = tile("rna", point(2.48, 0.93))
        self.play(GrowFromPoint(rna, point(0.92, 0.93)), run_time=0.65)
        self.play(rna.animate.shift(RIGHT * 0.70), run_time=1.01)

        self.at("making that message")
        self.play(rna.animate.shift(DOWN), run_time=2.45)
        self.at("is called messenger")
        rna_label = below("Messenger RNA", rna, BLUE).set_z_index(5)
        self.play(FadeIn(rna_label), close.animate.set_fill(lift(CLOSE_FILL, 0.18)),
                  run_time=1.08)

        self.at("we want to find")
        self.play(FadeOut(gene_label), FadeOut(gene), FadeOut(rna_label), run_time=0.65)
        self.play(rna.animate.shift(RNA_HOME - point(3.18, -0.07)),
                  close.animate.set_fill(CLOSE_FILL), run_time=2.65)
        self.finish()


class S03Probe(SpokenScene):
    def construct(self):
        section, anchor, close, rna, _ = close_world()
        probe = tile("probe", PROBE_ENTRY)
        self.add(section, anchor, close, rna, schematic())
        self.at("experimenters add")
        self.play(FadeIn(probe, shift=LEFT * 0.10), run_time=1.12)
        label = above("Probe", probe, YELLOW).set_z_index(5)
        self.at("called a probe")
        self.play(FadeIn(label), close.animate.set_fill(lift(CLOSE_FILL, 0.13)), run_time=1.23)

        self.at("carries a label")
        ring = Circle(radius=0.28, color=YELLOW, stroke_width=3).move_to(probe[1]).set_z_index(5)
        pulse(ring, base=4, amp=1.8, speed=3.0)
        self.add(ring)
        self.play(ring.animate.scale(2.45).set_stroke(opacity=0),
                  close.animate.set_fill(CLOSE_FILL), run_time=2.39)
        self.remove(ring)
        self.play(FadeOut(label), run_time=0.38)

        self.at("when it meets")
        self.play(probe.animate.shift(point(1.00, -0.95) - PROBE_ENTRY), run_time=1.77)
        self.at("the two bind")
        self.play(probe.animate.shift(UP * 0.81), run_time=0.68)

        self.at("unbound probes")
        spare = tile("probe", point(3.37, -1.52)).scale(0.63)
        self.play(FadeIn(spare), run_time=0.34)
        self.play(FadeOut(spare, shift=RIGHT * 1.76), run_time=1.50)
        self.finish()


class S04Place(SpokenScene):
    def construct(self):
        section, anchor, close, rna, probe = close_world("probe")
        self.add(section, anchor, close, rna, probe, schematic())
        self.at("pairing is called")
        hybrid = T("Hybridization", 34, TEXT).move_to(point(1.00, 1.71)).set_z_index(5)
        self.play(FadeIn(hybrid), close.animate.set_fill(lift(CLOSE_FILL, 0.12)), run_time=1.13)
        self.at("means in place")
        in_place = T("In situ = in place", 33, TEXT).move_to(point(1.00, -1.37)).set_z_index(5)
        self.play(FadeIn(in_place), close.animate.set_fill(lift(CLOSE_FILL, 0.23)), run_time=1.55)

        self.at("hybridization marks")
        self.play(FadeOut(hybrid), FadeOut(in_place), run_time=0.47)
        center_signal = signal(probe[1].get_center(), radius=0.22)
        self.play(TransformFromCopy(probe[1], center_signal), FadeOut(probe),
                  FadeOut(rna), close.animate.set_fill(CLOSE_FILL), run_time=2.10)

        self.at("zoom back out", lead=0.49)
        wide = retina()
        focused = spots(wide, [FOCUS])[0]
        others = spots(wide, EXAMPLE_CELLS[:-1])
        self.play(Transform(section, wide), FadeOut(anchor),
                  Transform(close, wide[1][FOCUS[0]][FOCUS[1]].copy()),
                  Transform(center_signal, focused), run_time=2.04)
        self.remove(close)
        self.at("give us a map", lead=0.04)
        self.play(LaggedStart(*(GrowFromCenter(dot) for dot in others), lag_ratio=0.52),
                  *light_layers(section, [0, 1], 0.12),
                  run_time=1.54)
        self.play(*light_layers(section, [0, 1], 0), run_time=1.36)
        self.finish()


class S05Predict(SpokenScene):
    def construct(self):
        section = retina()
        previous = spots(section, EXAMPLE_CELLS)
        inner, mark, question = predict_labels()
        self.add(section, previous, schematic())
        self.at("use that rule")
        self.play(FadeOut(previous), *light_layers(section, range(4), 0.13), run_time=1.30)
        self.play(*light_layers(section, range(4), 0), run_time=1.30)
        self.at("imagine the message")
        enlarged = retina().scale(1.12).move_to(point(STACK_X + 0.25, 0.21))
        neutral = retina()
        zoomed_out = neutral.copy().scale(1.07).shift(RIGHT * 0.25)
        rnas = VGroup(*(tile("rna", zoomed_out[1][i][j].get_center()).scale(0.30)
                       for i, j in EXAMPLE_CELLS))
        target_rnas = VGroup(*(tile("rna", enlarged[1][i][j].get_center()).scale(0.33)
                              for i, j in EXAMPLE_CELLS))
        self.play(Transform(section, enlarged), run_time=1.21)
        self.play(LaggedStart(*(GrowFromCenter(t) for t in target_rnas), lag_ratio=0.45),
                  run_time=1.46)
        self.at("inner layers")
        self.play(FadeIn(inner), *light_layers(section, [0, 1], 0.18), run_time=1.19)

        self.at("probe meeting its match")
        self.play(*(piece.animate.scale(0.87) for piece in target_rnas),
                  *light_layers(section, [0, 1], 0.24), run_time=1.89)
        self.at("zoom out and look", lead=0.46)
        self.play(Transform(section, zoomed_out), Transform(target_rnas, rnas),
                  run_time=1.31)
        self.play(LaggedStart(*(ShrinkToCenter(t) for t in target_rnas), lag_ratio=0.33),
                  run_time=0.94)
        self.at("where would you expect")
        settle_time = self.narration_s + 0.4 - self.elapsed()
        self.play(Transform(section, neutral, rate_func=linear, run_time=settle_time),
                  Succession(FadeIn(mark, shift=UP * 0.19, run_time=0.43),
                             FadeIn(question, run_time=0.65)))
        self.finish()


class S06Think(Scene):
    def construct(self):
        self.camera.background_color = BG
        self.add(retina(), schematic(), *predict_labels())
        self.wait(4.5)


class S07Answer(SpokenScene):
    def construct(self):
        section = retina()
        inner, mark, question = predict_labels()
        dots = spots(section, EXAMPLE_CELLS)
        self.add(section, schematic(), inner, mark, question)
        self.at("marks would appear")
        self.play(FadeOut(mark), FadeOut(question), *light_layers(section, [0, 1], 0.19),
                  rate_func=rush_from, run_time=0.38)
        self.play(LaggedStart(*(GrowFromCenter(dot) for dot in dots), lag_ratio=0.35),
                  run_time=0.85)

        self.at("where the probe")
        inset, anchor, close, rna, probe = close_world("probe")
        selected = section[1][FOCUS[0]][FOCUS[1]].copy().set_z_index(2)
        self.add(selected)
        inset_dots = spots(inset, EXAMPLE_CELLS[:-1])
        self.play(Transform(section, inset), Transform(selected, close),
                  Transform(dots[2], signal(probe[1].get_center(), radius=0.22)),
                  *(Transform(dot, target.scale(0.33).set_opacity(0))
                    for dot, target in zip(dots[:2], inset_dots)),
                  FadeOut(inner), run_time=2.14)
        self.remove(dots[0], dots[1])
        self.play(FadeIn(anchor), FadeIn(rna), FadeIn(probe), FadeOut(dots[2]), run_time=0.62)

        self.at("now imagine")
        self.play(FadeOut(probe, shift=RIGHT * 3.55 + DOWN * 0.63), run_time=1.48)
        wrong = tile("wrong", PROBE_ENTRY)
        outline_width = selected.get_stroke_width()
        self.play(FadeIn(wrong, shift=LEFT * 0.10), selected.animate.set_stroke(width=0),
                  run_time=0.57)
        wrong_label = below("Wrong probe", wrong, YELLOW).set_z_index(5)
        self.at("wrong probe")
        self.play(FadeIn(wrong_label), run_time=0.44)

        self.at("you could miss", lead=0.60)
        travel = WRONG_EXIT - PROBE_ENTRY
        # 2026-11-21 (frame check): the label no longer slides across the cell edge; it fades as the probe leaves
        self.play(wrong.animate.shift(travel), FadeOut(wrong_label, run_time=0.6),
                  run_time=2.65)
        self.at("where it really is")
        self.play(FadeOut(wrong, shift=LEFT * 1.03), run_time=0.70)
        self.play(selected.animate.set_stroke(width=outline_width), run_time=0.33)
        self.finish()


class S08Limits(SpokenScene):
    def construct(self):
        section, anchor, close, rna, _ = close_world()
        self.add(section, anchor, close, rna, schematic())
        self.at("check that the probe")
        probe = tile("probe", PROBE_ENTRY)
        self.play(FadeIn(probe, shift=LEFT * 0.10), run_time=0.56)
        self.play(probe.animate.shift(point(1.00, -0.95) - PROBE_ENTRY), run_time=1.35)
        self.play(probe.animate.shift(UP * 0.81), run_time=0.81)

        self.at("with the right probe", lead=0.57)
        wide = retina()
        center_signal = signal(probe[1].get_center(), radius=0.22)
        self.add(center_signal)
        self.remove(rna, probe)
        self.play(Transform(section, wide), FadeOut(anchor),
                  Transform(close, wide[1][FOCUS[0]][FOCUS[1]].copy()),
                  Transform(center_signal, spots(wide, [FOCUS])[0]), run_time=1.51)
        self.remove(close)
        dots = spots(wide, EXAMPLE_CELLS[:-1])
        self.play(*(GrowFromCenter(dot) for dot in dots), run_time=0.51)
        self.at("only location")
        location = rail("Location only", color=YELLOW)
        self.play(FadeIn(location), *light_layers(section, [0, 1], 0.15),
                  run_time=1.18)

        self.at("having an")
        other_view = retina().scale(0.88).shift(RIGHT * 0.32)
        self.play(FadeOut(center_signal), FadeOut(dots), FadeOut(location),
                  Transform(section, other_view), run_time=2.14)
        living = rail("Separate living test", y=2.30)
        self.play(FadeIn(living), run_time=0.63)
        self.at("testing light responses")
        beam = Rectangle(width=0.76, height=4.45, stroke_width=0,
                         fill_color=TEXT, fill_opacity=0.32).move_to(point(-4.83, 0.10)).set_z_index(3)
        light = rail("Light", y=1.34)
        self.play(FadeIn(beam), FadeIn(light), run_time=0.52)
        self.play(beam.animate.move_to(point(1.08, 0.10)), run_time=2.01, rate_func=linear)
        self.at("separate recording", lead=0.05)
        self.play(FadeOut(beam), FadeOut(light), run_time=0.29)
        empty = RoundedRectangle(width=3.81, height=1.90, corner_radius=0.15,
                                 stroke_color=GREY, stroke_width=2.5).move_to(point(RAIL_X, -0.51))
        record = rail("Record a response", y=-1.86)
        self.play(Create(empty), run_time=0.56)
        self.play(FadeIn(record), run_time=0.46)
        self.finish()


class S09Melanopsin(SpokenScene):
    def construct(self):
        section = retina()
        self.add(section, schematic())
        self.at("in 2000")
        study = rail("Provencio and colleagues", y=1.40)
        year = rail("2000", y=0.69, color=GOLD)
        self.play(FadeIn(year), *light_layers(section, range(4), 0.10), run_time=0.83)
        self.at("provencio and colleagues", lead=0.55)
        self.play(FadeIn(study), *light_layers(section, range(4), 0.18), run_time=1.75)
        self.at("to map a gene")
        target = rail("Melanopsin RNA", y=3.05, color=BLUE)
        self.play(FadeIn(target), *light_layers(section, range(4), 0.04), run_time=1.77)

        self.at("they tested")
        self.play(FadeOut(study), FadeOut(year), FadeOut(target), run_time=0.52)
        self.at("adult macaque", lead=0.77)
        macaque = rail("Adult macaque", y=0.75)
        self.play(FadeIn(macaque, run_time=0.35), *light_layers(section, range(4), 0.15))
        self.at("and from adult", lead=0)
        mice = rail("Adult mice", y=0.75)
        self.play(swap(macaque, mice, run_time=0.55), *light_layers(section, range(4), 0.03),
                  run_time=0.64)
        pups = rail("10-day-old mice", y=0.75)
        self.at("10 day old", lead=0.23)
        self.play(swap(mice, pups, run_time=0.56), *light_layers(section, range(4), 0.17),
                  run_time=1.12)
        self.at("mice", lead=-0.78)
        self.play(swap(pups, target, run_time=0.68), *light_layers(section, range(4), 0),
                  run_time=0.84)

        self.at("marks appeared")
        dots = spots(section, RESEARCH_CELLS)
        self.play(LaggedStart(*(GrowFromCenter(dot) for dot in dots), lag_ratio=0.42),
                  *light_layers(section, [0, 1], 0.17),
                  run_time=1.37)
        self.at("ganglion and", lead=0.49)
        ganglion = rail("Ganglion cell layer", y=ROWS[0], size=32)
        self.play(FadeIn(ganglion), *light_layers(section, [0], 0.31), run_time=0.63)
        self.at("amacrine cell layers", lead=0.32)
        amacrine = rail("Amacrine cell layer", y=ROWS[1], size=32)
        self.play(FadeIn(amacrine), *light_layers(section, [1], 0.31), run_time=1.18)
        self.at("no light response")
        no_response = rail("Light response\nnot recorded", y=-1.86, size=30)
        self.play(FadeIn(no_response), *light_layers(section, [0, 1], 0.13), run_time=1.45)
        self.finish()


class S10Fluorescence(SpokenScene):
    def construct(self):
        section = retina()
        self.add(section, schematic())
        self.at("in 2019")
        study = rail("Peng and colleagues", y=1.48)
        year = rail("2019", y=0.78, color=GOLD)
        self.play(FadeIn(year), *light_layers(section, range(4), 0.13), run_time=0.94)
        self.at("peng and colleagues", lead=0.55)
        self.play(FadeIn(study), *light_layers(section, range(4), 0), run_time=1.51)
        self.at("from adult macaque", lead=0.47)
        sample = rail("Adult macaque", y=-0.28)
        self.play(FadeIn(sample), *light_layers(section, [0], 0.15), run_time=1.53)

        self.at("check which cells")
        selected, close = pair_of_cells(section)
        self.add(selected)
        self.play(FadeOut(study), FadeOut(year), FadeOut(sample), run_time=0.62)
        self.play(FadeOut(section), Transform(selected, close), run_time=2.07)

        self.at("fluorescent in situ")
        method = T("Fluorescent in situ hybridization", 32, TEXT).move_to(point(-0.45, 3.07))
        self.play(FadeIn(method), *(c.animate.set_fill(lift(CLOSE_FILL, 0.14)) for c in selected),
                  run_time=1.83)
        self.at("fluorescent means")
        self.play(FadeOut(method), *(c.animate.set_fill(CLOSE_FILL) for c in selected), run_time=1.07)
        dots = VGroup(*(signal(c.get_center(), radius=0.26) for c in close))
        self.at("label gives off light")
        self.play(LaggedStart(*(GrowFromCenter(dot) for dot in dots), lag_ratio=0.44),
                  run_time=1.03)
        self.play(*(dot[0].animate.scale(1.65).set_fill(opacity=0.35) for dot in dots),
                  rate_func=there_and_back, run_time=2.48)
        self.finish()


class S11CellTypes(SpokenScene):
    def construct(self):
        section = retina()
        selected, close = pair_of_cells(section)
        dots = VGroup(*(signal(c.get_center(), radius=0.26) for c in close))
        outlines = VGroup(*(c.copy().set_fill(opacity=0).set_stroke(GREEN, width=4.5)
                            for c in close)).set_z_index(5)
        self.add(close, dots, schematic())
        self.at("label cell shapes", lead=0.71)
        self.play(LaggedStart(*(Create(outline) for outline in outlines), lag_ratio=0.40),
                  *(c.animate.set_fill(lift(CLOSE_FILL, 0.17)) for c in close),
                  run_time=2.15)
        self.at("together the fluorescent")
        section_signals = spots(section, GANGLION_CELLS)
        overlays = VGroup(*(c.copy().set_fill(opacity=0).set_stroke(GREEN, width=4)
                           for c in selected)).set_z_index(5)
        self.play(Transform(close, selected), Transform(outlines, overlays),
                  Transform(dots, section_signals), FadeIn(section), run_time=3.23)
        self.remove(close)

        self.at("ganglion cell groups", lead=0.12)
        heading = rail("Ganglion cells", y=1.45)
        self.play(FadeIn(heading), run_time=0.62)
        self.at("called midget", lead=0.25)
        types = VGroup(T("Midget", 34, TEXT), T("Parasol", 34, TEXT)).arrange(
            DOWN, aligned_edge=LEFT, buff=0.33).move_to(point(RAIL_X, 0.30))
        self.play(FadeIn(types), run_time=0.65)
        self.finish()


class S12End(EndCard):
    LINE = "A matching probe marks where a gene’s RNA is present."
