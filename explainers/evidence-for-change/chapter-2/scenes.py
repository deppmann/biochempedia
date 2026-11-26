"""Two Clues, One Family Tree — the riverbank chapter's relationship test.

COLOUR MAP, shared with Chapter 1
    GOLD   fossils and fossil-bearing observations
    BLUE   matching body structures
    TEAL   DNA and protein sequences
    GREEN  supported comparisons and inferences
    GREY   missing or uncertain evidence
"""
from importlib.util import module_from_spec, spec_from_file_location
from pathlib import Path

from bp_parts import *
from bp_style import EndCard


_reference_spec = spec_from_file_location("evidence_chapter_one", Path(__file__).resolve().parents[1] / "scenes.py")
chapter_one = module_from_spec(_reference_spec)
_reference_spec.loader.exec_module(chapter_one)

ROCK = chapter_one.ROCK
ROCK_LIGHT = chapter_one.ROCK_LIGHT
SAND = chapter_one.SAND
LIMB_X = (-4.65, -1.55, 1.55, 4.65)
LIMB_NAMES = ("human arm", "cat leg", "whale flipper", "bat wing")
BONE_SHADES = (BLUE, "#48A8C9", "#8AD5E6", "#67B8DC")
SPECIES_X = (-3.55, 0.0, 3.55)
PROTEINS = ("MPLKGA", "MPLKGS", "MQLTAS")
DNA = "ATGCCG"
CELL_X = (-2.45, -1.46, -0.47, 0.52, 1.51, 2.50)
ROW_Y = (1.76, 0.74, -0.28)
PREDICT = "Do the clues agree?"
TITLE = "Two Clues, One Family Tree"
LESSON = "Evidence for Change Over Time"


def xy(x, y):
    return np.array([x, y, 0.0])


def label(text, x, y, size=30, color=TEXT):
    return T(text, size, color).move_to(xy(x, y))


def slab(width, height, x, y, color, opacity=0.4, border=0):
    return RoundedRectangle(
        width=width, height=height, corner_radius=0.13,
        fill_color=color, fill_opacity=opacity, stroke_color=color, stroke_width=border,
    ).move_to(xy(x, y))


def path(*points, color=GREY, width=10):
    line = VMobject(stroke_color=color, stroke_width=width)
    line.set_points_as_corners([xy(*point) for point in points])
    line.set_cap_style(CapStyleType.ROUND)
    return line


def still_riverbank():
    bank = chapter_one.riverbank(label=False)
    bank.clear_updaters(recursive=True)
    return bank


def inset_riverbank():
    return still_riverbank().scale(0.26).move_to(xy(-4.85, 0.45))


def fossil_base():
    """A cutaway at the root keeps the riverbank and the growth diagram in one world."""
    layers = VGroup(
        slab(9.0, 0.27, 0, -2.79, ROCK_LIGHT, opacity=0.74),
        slab(9.3, 0.27, 0, -3.08, ROCK, opacity=0.87),
    )
    fossils = VGroup(chapter_one.shell(xy(x, -3.14), 0.48, changed=variant)
                    for x, variant in ((-3.35, 0), (2.15, 0.35), (3.55, 0.65)))
    return VGroup(layers, fossils)


def limb_tree():
    """All four limb examples share an origin; this diagram leaves their branching order open."""
    hub_y = -2.20
    stem = path((0, -2.85), (0, hub_y), width=13)
    branches = VGroup(path((0, hub_y), (x, -1.30), (x, -1.13), width=10) for x in LIMB_X)
    return VGroup(stem, branches)


def limb_board():
    return VGroup(slab(2.87, 3.78, x, 0.70, BLUE, opacity=0.23).set_z_index(-2) for x in LIMB_X)


def bone_segment(start, end, thickness, color):
    a, b = xy(*start), xy(*end)
    shape = RoundedRectangle(
        width=np.linalg.norm(b - a) + 0.06, height=thickness, corner_radius=thickness * 0.30,
        stroke_color=color, stroke_width=2.5, fill_color=color, fill_opacity=0.78,
    )
    return shape.rotate(angle_of_vector(b - a)).move_to((a + b) / 2)


def limb(index, form=None):
    """Block diagrams share proximal-to-distal order and have different proportions."""
    form = index if form is None else form
    # Elbow, wrist and digit fan. Each specimen has one upper block and two lower blocks.
    elbow_x, elbow_y, wrist_x, wrist_y, fan, length = (
        (-0.10, -0.14, 0.08, 0.91, 0.48, 0.69),
        (0.34, -0.34, -0.25, 0.94, 0.37, 0.43),
        (-0.32, -0.42, -0.08, 0.23, 0.68, 1.46),
        (-0.31, -0.08, 0.17, 0.65, 0.94, 1.18),
        (0.0, -0.17, 0.0, 0.60, 0.50, 0.72),
    )[form]
    x = LIMB_X[index]
    upper = bone_segment((x, -1.06), (x + elbow_x, elbow_y - 0.09), 0.36, BONE_SHADES[0])
    lower = VGroup(bone_segment(
        (x + elbow_x + offset, elbow_y + 0.07),
        (x + wrist_x + 0.8 * offset, wrist_y - 0.08), 0.145, BONE_SHADES[1],
    ) for offset in (-0.145, 0.145))
    wrist = VGroup(slab(0.19, 0.21, x + wrist_x + offset, wrist_y + 0.08, BONE_SHADES[2], opacity=0.90)
                   for offset in (-0.19, 0, 0.19))
    fingers = VGroup()
    for j in range(5):
        lateral = (j - 2) / 2
        start = (x + wrist_x + 0.105 * (j - 2), wrist_y + 0.23)
        tip = (x + wrist_x + fan * lateral, wrist_y + 0.23 + length * (1 - 0.40 * abs(lateral)))
        mid = tuple(0.52 * np.array(start) + 0.48 * np.array(tip))
        gap = np.array(tip) - np.array(start)
        fingers.add(
            bone_segment(start, tuple(np.array(mid) - gap * 0.05), 0.118, BONE_SHADES[3]),
            bone_segment(tuple(np.array(mid) + gap * 0.05), tip, 0.095, BONE_SHADES[3]),
        )
    return VGroup(upper, lower, wrist, fingers)


def limb_labels():
    return VGroup(label(name, x, 2.83, size=29, color=BLUE) for x, name in zip(LIMB_X, LIMB_NAMES))


def jobs():
    return VGroup(label(job, x, 3.38, size=28) for x, job in zip(LIMB_X, ("grasp", "walk", "swim", "fly")))


def comparison_band(limbs, part):
    """A sweep lights the same part on each limb without crossing the words."""
    spans = []
    for x, picture in zip(LIMB_X, limbs):
        section = picture[part]
        spans.append(slab(2.63, section.height + 0.12, x, section.get_y(),
                          BONE_SHADES[part], opacity=0.48).set_z_index(-1))
    return VGroup(spans)


def sweep(band):
    return LaggedStart(*(GrowFromEdge(highlight, LEFT) for highlight in band), lag_ratio=0.23)


def lineage_tree(pair=None, *, level=0.00, root=-2.71):
    """No pair is joined above the unresolved split until a grouping has support."""
    hub = (0.0, root + 0.75)
    stem = path((0, root), hub, width=13)
    tips = [(x, level) for x in SPECIES_X]
    if pair is None:
        branches = [path(hub, (x, level - 0.29), tip) for x, tip in zip(SPECIES_X, tips)]
        return VGroup(stem, VGroup(branches))

    first, second = pair
    fork_x = (SPECIES_X[first] + SPECIES_X[second]) / 2
    fork = (fork_x, level - 0.97)
    shared = path(hub, fork, color=GREEN, width=13)
    branches = VGroup(
        path(fork if i in pair else hub, (x, level - 0.29), tip,
             color=GREEN if i in pair else GREY)
        for i, (x, tip) in enumerate(zip(SPECIES_X, tips))
    )
    return VGroup(stem, branches, shared, Dot(xy(*fork), radius=0.115, color=GREEN))


def tree_field(opacity=0.29):
    return slab(11.7, 2.95, 0, -1.28, GREY, opacity=opacity).set_z_index(-3)


def species_labels(names):
    return VGroup(label(f"species {name}", x, 0.53, size=30) for x, name in zip(SPECIES_X, names))


def bracket(pair, y, color):
    left, right = (SPECIES_X[i] for i in pair)
    return path((left, y - 0.26), (left, y), (right, y), (right, y - 0.26), color=color, width=6)


def bracket_endpoints(pair, y, color, protein=False):
    x1, x2 = (SPECIES_X[i] for i in pair)
    if protein:
        return VGroup(*(protein_icon(width=1.40).move_to(xy(x, y)) for x in (x1, x2)))
    return VGroup(*(chapter_one.bone_icon(color).scale(0.58).move_to(xy(x, y)) for x in (x1, x2)))


def paired_wash(color=GREEN):
    """Shade the area between the supported branches."""
    return Polygon(xy(-3.55, 0.25), xy(0, 0.25), xy(0, -0.29), xy(-1.775, -0.97),
                   xy(-3.55, -0.29), stroke_width=0, fill_color=color,
                   fill_opacity=0.46).set_z_index(-2)


def protein_icon(width=2.65):
    return VGroup(slab(width / 6 - 0.075, 0.46, (i - 2.5) * width / 6, 0,
                       TEAL, opacity=0.44 if i in (1, 4) else 0.76, border=2)
                  for i in range(6))


def evidence_brackets(conflict=True):
    blue = bracket((0, 1), 1.36, BLUE)
    teal = bracket((0, 2) if conflict else (0, 1), 2.66, TEAL)
    blue_note = label(f"Shared structure, {'C' if conflict else 'F'} lacks it", -1.78, 1.76, size=30, color=BLUE)
    teal_note = label("More similar protein", 0 if conflict else -1.78, 3.05, size=30, color=TEAL)
    blue_ends = bracket_endpoints((0, 1), 1.04, BLUE)
    teal_ends = bracket_endpoints((0, 2) if conflict else (0, 1), 2.34, TEAL, protein=True)
    for ends in (blue_ends, teal_ends):
        ends.set_z_index(2)
    return VGroup(blue, blue_note, blue_ends), VGroup(teal, teal_note, teal_ends)


def question_plate(text, fill=0.40):
    card = question_card(text, y=-3.25, color=TEXT, size=43)
    backing = slab(7.6, 0.81, -0.50, -3.25, GREY, opacity=fill)
    return VGroup(backing, card)


def prediction_frame():
    field = tree_field(0.42)
    tree = lineage_tree()
    names = species_labels("ABC")
    blue, teal = evidence_brackets()
    question = question_plate(PREDICT)
    return field, tree, names, blue, teal, question


def sequence_cell(letter, x, y, matched=False):
    cell = slab(0.79, 0.73, x, y, TEAL, opacity=0.68 if matched else 0.30, border=2)
    glyph = M(letter, 34, TEXT).move_to(cell).set_z_index(1)
    return VGroup(cell, glyph)


def sequence_row(letters, y, name=None):
    cells = VGroup(sequence_cell(letter, x, y) for letter, x in zip(letters, CELL_X))
    marker = label(name, -4.32, y, size=29) if name else VGroup()
    return VGroup(cells, marker)


def sequence_board():
    return slab(10.15, 3.43, -0.68, 0.73, TEAL, opacity=0.22).set_z_index(-3)


def alignment():
    head = label("Same protein", 0, 2.97, size=35, color=TEAL)
    rows = [sequence_row(seq, y, f"species {i + 1}") for i, (seq, y) in enumerate(zip(PROTEINS, ROW_Y))]
    return head, rows


def alignment_marks(rows):
    marks = VGroup()
    for j, row in enumerate(rows):
        for i, cell in enumerate(row[0]):
            if PROTEINS[j][i] == PROTEINS[0][i]:
                cell[0].set_fill(TEAL, opacity=0.62)
            else:
                x, y, _ = cell.get_center()
                marks.add(path((x - 0.12, y - 0.44), (x + 0.12, y - 0.44),
                               color=ManimColor(TEAL).interpolate(WHITE, 0.55), width=4))
    return marks


def fossil_tile():
    layers = VGroup(slab(2.56, 0.24, 0, -0.31, ROCK_LIGHT, opacity=0.84),
                    slab(2.62, 0.25, 0, -0.59, ROCK, opacity=0.92))
    shells = VGroup(chapter_one.shell(xy(-0.70, -0.61), 0.52),
                    chapter_one.shell(xy(0.52, -0.29), 0.62, changed=0.65))
    return VGroup(layers, shells)


def structure_tile():
    return VGroup(limb(0).scale(0.38).rotate(-0.22).move_to(xy(-0.56, -0.20)),
                  limb(3).scale(0.36).rotate(0.17).move_to(xy(0.58, -0.20)))


def sequence_tile():
    return VGroup(protein_icon().shift(0.04 * UP), protein_icon().shift(0.55 * DOWN))


def clue_panel(kind, x, title=None, stacked=False):
    color, picture = {
        "fossil": (GOLD, fossil_tile),
        "structure": (BLUE, structure_tile),
        "sequence": (TEAL, sequence_tile),
    }[kind]
    panel = slab(3.30, 2.10, x, 1.57, color, opacity=0.28, border=3)
    image = picture().shift(panel.get_center())
    heading = label(title, x, 3.03 if stacked else 2.20, size=29, color=color) if title else VGroup()
    if stacked:
        backing = VGroup(slab(3.30, 2.10, x + 0.07, 1.49, color, opacity=0.24, border=2),
                         slab(3.30, 2.10, x + 0.14, 1.41, color, opacity=0.24, border=2))
        return VGroup(backing, panel, heading, image)
    return VGroup(panel, heading, image)


def evidence_into_tree():
    """The first link ends at the strata; the other two reach the branch under test."""
    fork = (-1.775, -0.97)
    fossil = path((-4.04, 0.52), (-4.04, -2.27), (-3.58, -2.68), color=GOLD, width=6)
    structure = path((0, 0.52), (-0.55, 0.06), fork, color=BLUE, width=6).set_z_index(-1)
    sequence = path((4.04, 0.52), (2.77, 0.06), fork, color=TEAL, width=6).set_z_index(-1)
    return fossil, structure, sequence


class S00LinkQuestion(TitleCard, SpokenScene):
    LESSON = LESSON
    TITLE = TITLE

    def construct(self):
        bank = still_riverbank()
        tree = chapter_one.branch_tree(at=(3.94, -0.28, 0), scale=0.98)
        q = question_card("Which branches are closest?", y=-3.46, color=TEXT, size=38)
        bone = chapter_one.bone_icon(BLUE).scale(0.78).move_to(xy(2.27, 1.88))
        protein = protein_icon(width=2.0).move_to(xy(4.89, 1.88))
        self.add(bank, tree)
        self.at("bat wing", lead=0.6)
        self.play(FadeIn(bone, shift=0.25 * RIGHT), run_time=0.78)
        self.at("a protein", lead=0.25)
        self.play(FadeIn(protein, shift=0.25 * LEFT), run_time=0.70)
        self.at("same relatives")
        self.play(FadeIn(q), run_time=0.65)
        self.at("used fossils")
        self.play(LaggedStart(*(fossil.animate.set_stroke(GOLD, width=6)
                                for fossil in bank.shells), lag_ratio=0.35), run_time=1.30)
        self.at("through time")
        self.play(Transform(bank, inset_riverbank()), run_time=1.26)
        self.at("test relationships")
        full = limb_tree()
        self.play(
            Transform(tree, VGroup(*full[0:1], *full[1])),
            bone.animate.scale(1 / 0.78).move_to(xy(1.15, 0.69)),
            protein.animate.move_to(xy(4.40, 0.69)),
            run_time=1.75,
        )
        self.finish()


class S01Title(TitleCard):
    LESSON = LESSON
    TITLE = TITLE

    def construct(self):
        bank = inset_riverbank()
        bone = chapter_one.bone_icon(BLUE).move_to(xy(1.15, 0.69))
        protein = protein_icon(width=2.0).move_to(xy(4.40, 0.69))
        self.add(bank, limb_tree(), bone, protein)
        title = T(self.TITLE, 53, TEXT, font=TITLE_FONT).move_to(xy(0, 2.53))
        lesson = label(self.LESSON.upper(), 0, 3.30, size=28, color=TEAL)
        rule = path((-1.40, 1.99), (1.40, 1.99), color=GOLD, width=4)
        self.play(FadeIn(lesson), FadeIn(title, shift=0.14 * UP), Create(rule), run_time=0.72)
        self.finish()


class S02CommonAncestor(SpokenScene):
    def construct(self):
        tree = limb_tree()
        board = limb_board()
        node = Dot(xy(0, -2.20), radius=0.16, color=GREEN)
        population = Circle(radius=0.48, stroke_color=GREEN, stroke_width=4,
                            fill_color=GREEN, fill_opacity=0.30).move_to(node)
        ancestor = label("common ancestor", -0.30, -3.22, size=32, color=GREEN)
        provisional = limb_tree()
        self.add(provisional, scope_tag(size=28))
        self.at("common ancestor", lead=0.42)
        self.play(FadeOut(provisional[1]), GrowFromCenter(population),
                  Transform(provisional[0], tree[0].copy().set_stroke(width=19)),
                  run_time=1.25)
        self.at("earlier population")
        self.play(GrowFromCenter(node), run_time=0.52)
        self.play(FadeIn(ancestor), run_time=0.56)
        self.at("later groups")
        self.play(FadeIn(board, shift=0.32 * UP), run_time=1.56)
        self.at("branch splitting")
        self.play(LaggedStart(*(Create(branch) for branch in tree[1]), lag_ratio=0.18), FadeOut(population),
                  provisional[0].animate.set_stroke(width=13), run_time=1.54)
        self.at("inherits old features", lead=0.6)
        bones = [limb(i, form=4) for i in range(4)]
        self.play(LaggedStart(*(GrowFromPoint(bone, xy(x, -1.13)) for bone, x in zip(bones, LIMB_X)),
                              lag_ratio=0.16), run_time=1.67)
        self.at("then changes")
        self.play(LaggedStart(*(Transform(bone, limb(i)) for i, bone in enumerate(bones)),
                              lag_ratio=0.21), FadeOut(ancestor), run_time=1.80)
        self.finish()


class S03BoneMap(SpokenScene):
    def construct(self):
        bones = [limb(i) for i in range(4)]
        headers = limb_labels()
        board = limb_board()
        node = Dot(xy(0, -2.20), radius=0.16, color=GREEN)
        self.add(limb_tree(), board, *bones, node, scope_tag(size=28))
        for i, cue in enumerate(LIMB_NAMES):
            self.at(cue)
            self.play(FadeIn(headers[i]), board[i].animate.set_fill(BLUE, opacity=0.46), run_time=0.55)
        upper, lower, wrist, fingers = (comparison_band(bones, part) for part in range(4))
        parts = [caption(part, size=32, color=BLUE, y=-3.29) for part in
                 ("Upper bone", "Paired lower bones", "Wrist bones", "Finger bones")]
        self.at("upper bone")
        self.play(sweep(upper), FadeIn(parts[0]), FadeOut(node),
                  *(panel.animate.set_fill(BLUE, opacity=0.23) for panel in board), run_time=0.73)
        self.at("paired lower bones")
        self.play(FadeOut(upper), sweep(lower), swap(parts[0], parts[1]), run_time=1.29)
        self.at("Wrist and finger", lead=0.72)
        self.play(FadeOut(lower), sweep(wrist), swap(parts[1], parts[2]), run_time=1.04)
        self.at("finger bones")
        self.play(FadeOut(wrist), sweep(fingers), swap(parts[2], parts[3]), run_time=1.32)
        self.at("Shapes and jobs")
        self.play(FadeOut(fingers), FadeOut(parts[3]),
                  LaggedStart(*(FadeIn(word) for word in jobs()), lag_ratio=0.22), run_time=1.15)
        self.at("positions match")
        position = comparison_band(bones, 1)
        self.play(sweep(position), run_time=1.23)
        self.play(FadeOut(position), run_time=0.48)
        self.finish()


class S04Construction(SpokenScene):
    def construct(self):
        bones = [limb(i) for i in range(4)]
        work = jobs()
        tree = limb_tree()
        self.add(tree, limb_board(), limb_labels(), *bones, work, scope_tag(size=28))
        lower = comparison_band(bones, 1)
        self.at("compare construction")
        self.play(sweep(lower), run_time=1.48)
        self.at("only jobs")
        self.play(LaggedStart(*(FadeOut(word, shift=UP * 0.20) for word in work), lag_ratio=0.14),
                  run_time=1.18)
        self.at("Inherited changes")
        self.play(FadeOut(lower), run_time=0.43)
        # The common outline is an ancestor schematic, beside each reshaped upper block.
        outlines = [bone_segment((x, -1.04), (x, -0.31), 0.25, BONE_SHADES[0])
                    .set_opacity(0.43).shift(0.83 * LEFT) for x in LIMB_X]
        self.play(LaggedStart(*(TransformFromCopy(bone[0], outline) for bone, outline in zip(bones, outlines)),
                              lag_ratio=0.18), run_time=1.25)
        self.at("old set of parts")
        wrist_bands = comparison_band(bones, 2)
        self.play(*(FadeOut(outline) for outline in outlines), sweep(wrist_bands), run_time=1.13)
        self.at("shared bone map")
        self.play(FadeOut(wrist_bands), run_time=0.40)
        links = VGroup(path((x, -1.15), (x, -1.30), (0, -2.20), color=BLUE, width=7) for x in LIMB_X)
        self.at("points back")
        self.play(LaggedStart(*(Create(link) for link in links), lag_ratio=0.13), run_time=1.28)
        self.at("a common ancestor", lead=0.1)
        self.play(GrowFromCenter(Dot(xy(0, -2.20), radius=0.17, color=GREEN)), run_time=0.45)
        self.play(FadeIn(caption("Same construction and position", size=32, color=GREEN, y=-3.19)), run_time=0.56)
        self.finish()


class S05Sequence(SpokenScene):
    def construct(self):
        board, names, tree = limb_board(), limb_labels(), limb_tree()
        limbs = [limb(i) for i in range(4)]
        links = VGroup(path((x, -1.15), (x, -1.30), (0, -2.20), color=BLUE, width=7) for x in LIMB_X)
        dot = Dot(xy(0, -2.20), radius=0.17, color=GREEN)
        rule = caption("Same construction and position", size=32, color=GREEN, y=-3.19)
        self.add(tree, board, names, *limbs, links, dot, rule, scope_tag(size=28))
        little = [pic.copy().scale(0.28).move_to(xy(x, -0.84)) for pic, x in zip(limbs, LIMB_X)]
        self.at("Sequences offer")
        self.play(*(Transform(pic, small) for pic, small in zip(limbs, little)),
                  FadeOut(names), FadeOut(board), FadeOut(rule), run_time=1.48)
        dna_row = sequence_row(DNA, ROW_Y[0])
        dna_label = label("DNA sequence", 0, 2.97, size=35, color=TEAL)
        self.at("DNA sequence", lead=0.6)
        self.play(FadeIn(dna_row, shift=0.56 * LEFT), run_time=0.88)
        self.play(FadeIn(dna_label), run_time=0.54)
        self.at("order of its bases")
        self.play(LaggedStart(*(cell[0].animate.set_fill(TEAL, opacity=0.59) for cell in dna_row[0]),
                              lag_ratio=0.26), run_time=1.74)
        self.at("genes carry instructions")
        self.play(FadeOut(dna_label), FadeOut(dna_row), run_time=0.61)
        head, rows = alignment()
        self.at("for proteins", lead=0.40)
        self.play(FadeIn(sequence_board()), FadeIn(rows[0][0], shift=0.44 * LEFT),
                  *(FadeOut(pic) for pic in limbs), FadeOut(links), FadeOut(dot), run_time=1.19)
        self.at("line up the same", lead=0.8)
        self.play(FadeIn(head), FadeIn(rows[0][1]), run_time=0.56)
        for row in rows[1:]:
            row[0].shift(RIGHT * 0.44)
            self.play(FadeIn(row, shift=UP * 0.22), run_time=0.41)
            self.play(row[0].animate.shift(0.44 * LEFT), run_time=0.42)
        cursor = slab(0.91, 3.13, CELL_X[0], 0.74, TEAL, opacity=0.18).set_z_index(-2)
        self.at("position by position", lead=0.36)
        self.add(cursor)
        for i, x in enumerate(CELL_X):
            changes = []
            for j, row in enumerate(rows):
                cell = row[0][i]
                if PROTEINS[j][i] == PROTEINS[0][i]:
                    changes.append(cell[0].animate.set_fill(TEAL, opacity=0.62))
                else:
                    y = cell.get_y() - 0.44
                    changes.append(Create(path((x - 0.12, y), (x + 0.12, y),
                                               color=ManimColor(TEAL).interpolate(WHITE, 0.55), width=4)))
            self.play(cursor.animate.set_x(x), *changes, run_time=0.29)
        self.play(FadeOut(cursor), run_time=0.27)
        self.finish()


def change_tree():
    """Branch distances are schematic; the marks show unevenly spaced inherited changes."""
    left, middle, right = SPECIES_X
    root, old_split, recent_split = (0, -2.84), (0, -2.43), (-1.70, -2.08)
    pieces = VGroup(
        path(root, old_split, width=12),
        path(old_split, recent_split, width=9),
        path(recent_split, (left, -1.06), width=9),
        path(recent_split, (middle, -1.06), width=9),
        path(old_split, (right, -1.06), width=9),
    )
    positions = ((), (), (), (0.72,), (0.18, 0.56, 0.83, 0.94))
    ticks = [VGroup() for _ in pieces]
    for branch, intervals, group in zip(pieces, positions, ticks):
        for fraction in intervals:
            center = branch.point_from_proportion(fraction)
            direction = rotate_vector(normalize(branch.get_end() - branch.get_start()), PI / 2)
            group.add(Line(center - 0.13 * direction, center + 0.13 * direction, color=TEAL, stroke_width=6))
    return pieces, ticks


def clock_face():
    center = xy(4.87, -1.84)
    dial_face = Circle(radius=0.69, color=GREY, stroke_width=4, fill_color=GREY,
                       fill_opacity=0.28).move_to(center)
    marks = VGroup()
    for angle in (0, PI / 2, PI, 3 * PI / 2):
        vector = xy(np.cos(angle), np.sin(angle))
        marks.add(Line(center + 0.49 * vector, center + 0.60 * vector, color=GREY, stroke_width=4))
    hand = Line(center, center + 0.45 * UP, color=TEXT, stroke_width=5)
    return VGroup(dial_face, marks), hand


class S06Changes(SpokenScene):
    def construct(self):
        head, rows = alignment()
        marks = alignment_marks(rows)
        previous = limb_tree()
        timepieces, ticks = change_tree()
        field = slab(11.7, 2.18, 0, -1.98, GREY, opacity=0.27).set_z_index(-3)
        clock, hand = clock_face()
        scope = scope_tag(size=28)
        self.add(sequence_board(), head, *rows, marks, previous, scope)
        self.at("inherited DNA")
        self.play(swap(head, label("Inherited sequence changes", 0, 2.97, size=34, color=TEAL)),
                  LaggedStart(*(Indicate(mark, color=TEAL, scale_factor=1.5) for mark in marks),
                              lag_ratio=0.34), run_time=1.37)
        self.at("remain in later")
        self.play(FadeOut(previous), FadeIn(field), Create(timepieces[0]), Create(timepieces[1]), run_time=1.08)
        first_tick = ticks[4][0]
        self.play(Create(timepieces[4]), Create(first_tick), run_time=1.33)
        self.at("Branches split")
        self.play(FadeIn(clock), FadeIn(hand), run_time=0.60)
        self.play(Rotate(hand, -0.72 * PI, about_point=hand.get_start()),
                  LaggedStart(Create(timepieces[2]), Create(timepieces[3]), lag_ratio=0.25),
                  run_time=1.42)
        self.at("closer relatives")
        near = VGroup(*(slab(4.95, 0.84, CELL_X[2], y, TEAL, opacity=0.30).set_z_index(-2) for y in ROW_Y[:2]))
        self.play(GrowFromEdge(near[0], LEFT), GrowFromEdge(near[1], LEFT), run_time=1.1)
        matching_columns = [tuple(row[0][i][0] for row in rows[:2]) for i in range(5)]
        self.at("more similar sequences")
        self.play(LaggedStart(*(AnimationGroup(*(cell.animate.set_stroke(width=6) for cell in column))
                                for column in matching_columns), lag_ratio=0.28),
                  Create(ticks[3][0]), Create(ticks[4][1]), run_time=1.56)
        tick_xs = (clock.get_x() + offset * 0.27 for offset in range(-3, 4))
        steady_marks = VGroup(*(path((x, -2.96), (x, -2.77), color=GREY, width=4) for x in tick_xs))
        self.at("Usually matters")
        self.play(FadeOut(near), FadeIn(label("Usually", 4.31, 2.95, size=34, color=TEXT)),
                  *(cell.animate.set_stroke(width=2) for column in matching_columns for cell in column),
                  LaggedStart(*(Create(mark) for mark in steady_marks), lag_ratio=0.16), run_time=1.43)
        self.at("do not build up")
        self.play(FadeOut(steady_marks),
                  Rotate(hand, -0.55 * PI, about_point=hand.get_start()),
                  LaggedStart(Create(ticks[4][2]), Create(ticks[4][3]), lag_ratio=0.70), run_time=1.88)
        self.finish()


class S07Predict(SpokenScene):
    def construct(self):
        field, tree, names, blue, teal, question = prediction_frame()
        scope = scope_tag(size=28)
        field.set_fill(GREY, opacity=0.18)
        self.add(field, scope)
        self.at("test two clues")
        self.play(Create(tree[0]), run_time=0.53)
        self.play(LaggedStart(*(Create(branch) for branch in tree[1]), lag_ratio=0.18), run_time=1.13)
        self.play(LaggedStart(*(FadeIn(name) for name in names), lag_ratio=0.18), run_time=0.75)
        self.at("share a blue", lead=0.66)
        self.play(Create(blue[0]), LaggedStart(*(GrowFromCenter(icon) for icon in blue[2]), lag_ratio=0.32),
                  run_time=1.18)
        self.at("C lacks")
        self.play(FadeIn(blue[1]), run_time=0.67)
        self.at("teal protein strip")
        self.play(Create(teal[0]), LaggedStart(*(GrowFromCenter(icon) for icon in teal[2]), lag_ratio=0.32),
                  run_time=1.27)
        self.at("with C")
        self.play(FadeIn(teal[1]), run_time=0.63)
        self.at("Have the clues", lead=0.1)
        self.play(FadeIn(question, shift=UP * 0.16), run_time=0.69)
        self.at("branch turn green")
        self.play(field.animate.set_fill(GREY, opacity=0.42), run_time=2.42, rate_func=linear)
        self.finish()


class S08Pause(Scene):
    def construct(self):
        self.camera.background_color = BG
        self.add(*prediction_frame(), scope_tag(size=28))
        self.wait(4.5)


class S09Conflict(SpokenScene):
    def construct(self):
        field, tree, names, blue, teal, question = prediction_frame()
        self.add(field, tree, names, blue, teal, question, scope_tag(size=28))
        answer = question_plate("Not yet", fill=0.20)
        self.at("No")
        self.remove(question)
        self.add(answer)
        self.play(field.animate.set_fill(GREY, opacity=0.29), run_time=0.73)
        self.at("different groupings", lead=0.7)
        grouped_blue = slab(5.0, 0.48, -1.775, 1.16, BLUE, opacity=0.30).set_z_index(-1)
        grouped_teal = slab(8.65, 0.75, 0, 2.43, TEAL, opacity=0.31).set_z_index(-1)
        self.play(GrowFromEdge(grouped_blue, LEFT), run_time=0.86)
        self.play(GrowFromEdge(grouped_teal, LEFT), run_time=0.86)
        self.at("Keep the branches")
        self.play(tree.animate.set_stroke(GREY, width=13), FadeOut(grouped_blue), FadeOut(grouped_teal), run_time=0.82)
        magnifier_center = xy(-3.55, 1.18)
        magnifier = VGroup(Circle(radius=0.21, stroke_color=TEXT, stroke_width=5).move_to(magnifier_center),
                           Line(magnifier_center + xy(0.15, -0.15), magnifier_center + xy(0.31, -0.31),
                                color=TEXT, stroke_width=6)).set_z_index(3)
        self.at("check the comparison")
        self.play(FadeIn(magnifier), run_time=0.22)
        self.play(magnifier.animate.shift(3.55 * RIGHT), run_time=0.67)
        self.remove(magnifier)
        magnifier = magnifier.copy().move_to(xy(-3.50, 2.47))
        self.play(FadeIn(magnifier), run_time=0.22)
        self.play(magnifier.animate.shift(7.05 * RIGHT), run_time=0.68)
        self.play(FadeOut(magnifier), run_time=0.19)
        slots = VGroup(slab(2.36, 1.31, -4.37, -1.74, GREY, opacity=0.45, border=3),
                       slab(2.36, 1.31, 4.37, -1.74, GREY, opacity=0.45, border=3))
        self.at("more evidence")
        self.play(LaggedStart(*(GrowFromCenter(slot) for slot in slots), lag_ratio=0.31), run_time=1.12)
        self.at("A conflict")
        self.play(GrowFromEdge(grouped_blue, LEFT), GrowFromEdge(grouped_teal, LEFT), run_time=1.31)
        self.at("question to investigate")
        glyph = label("?", -0.88, -0.98, size=64, color=GREY)
        self.play(FadeOut(answer), FadeIn(glyph, shift=0.18 * DOWN),
                  field.animate.set_fill(GREY, opacity=0.38), run_time=1.10)
        self.finish()


class S10Agreement(SpokenScene):
    def construct(self):
        field, old_tree, names, old_blue, old_teal, _ = prediction_frame()
        old_tree.set_stroke(GREY, width=13)
        previous = VGroup(old_tree, old_blue[0], old_teal[0]).scale(0.24).move_to(xy(-5.66, 2.01))
        previous.set_color(GREY)
        self.add(field, previous, scope_tag(size=28))
        tree = lineage_tree()
        blue, teal = evidence_brackets(conflict=False)
        new_case = label("A different case", 2.65, 3.43, size=34)
        self.at("different case", lead=0.66)
        self.play(FadeIn(tree, shift=1.05 * RIGHT), run_time=1.22)
        self.play(FadeIn(new_case), FadeIn(species_labels("DEF")), run_time=0.78)
        self.at("share a structure", lead=0.74)
        self.play(Create(blue[0]), FadeIn(blue[2]), run_time=1.26)
        self.at("third species lacks")
        self.play(FadeIn(blue[1]), run_time=0.68)
        self.at("protein strip")
        self.play(Create(teal[0]), FadeIn(teal[2]), run_time=0.75)
        self.play(FadeIn(teal[1]), run_time=0.60)
        supported = lineage_tree((0, 1))
        self.at("that same pair", lead=0.02)
        self.play(Transform(tree[1], supported[1]), Create(supported[2]), GrowFromCenter(supported[3]),
                  GrowFromEdge(paired_wash(), UP), run_time=1.12)
        self.at("independent clues agree")
        outline = slab(6.15, 0.68, -1.775, 0.60, GREEN, opacity=0.12, border=4)
        self.play(FadeOut(blue), FadeOut(teal), FadeOut(new_case), run_time=0.49)
        self.play(Create(outline), run_time=0.89)
        self.at("stronger explanation")
        self.play(supported[2].animate.set_stroke(GREEN, width=18),
                  supported[3].animate.scale(1.3), run_time=1.27)
        self.finish()


class S11Theory(SpokenScene):
    def construct(self):
        tree = lineage_tree((0, 1))
        agreement = paired_wash()
        self.add(tree_field(), tree, agreement, fossil_base(), scope_tag(size=28))
        panels = [clue_panel(kind, x) for kind, x in zip(("fossil", "structure", "sequence"), (-4.04, 0, 4.04))]
        theory = label("Evolution: tested explanation", 0, 3.20, size=36, color=GREEN)
        self.at("scientific theory")
        self.play(FadeIn(theory), tree[2].animate.set_stroke(GREEN, width=17), run_time=1.15)
        self.at("Each line of evidence")
        self.play(LaggedStart(*(FadeIn(panel, shift=UP * 0.23) for panel in panels), lag_ratio=0.46), run_time=2.20)
        self.at("different story")
        self.play(LaggedStart(*(Indicate(panel[2], color=color, scale_factor=1.025)
                                for panel, color in zip(panels, (GOLD, BLUE, TEAL))), lag_ratio=0.27), run_time=1.06)
        self.at("Evolution predicts")
        blank = slab(1.52, 0.95, 4.50, -1.49, GREY, opacity=0.19, border=3)
        test_arrow = Arrow(xy(0.28, -1.95), xy(3.67, -1.70), buff=0.04, color=GREEN,
                           stroke_width=5, tip_length=0.19)
        query = label("?", 2.70, -2.27, size=46, color=GREEN)
        self.play(FadeIn(blank, shift=0.42 * LEFT), GrowArrow(test_arrow), FadeIn(query), run_time=1.18)
        for cue, link, panel, color in zip(("among fossils", "structures", "and sequences"),
                                           evidence_into_tree(), panels, (GOLD, BLUE, TEAL)):
            self.at(cue)
            self.play(Create(link), panel[0].animate.set_fill(color, opacity=0.58), run_time=0.72)
        self.at("broad patterns")
        self.play(agreement.animate.set_fill(GREEN, opacity=0.76),
                  tree[2].animate.set_stroke(GREEN, width=19), run_time=1.50)
        self.finish()


class S12Limits(SpokenScene):
    def construct(self):
        field = tree_field()
        tree = lineage_tree()
        self.add(field, tree, scope_tag(size=28))
        panels = TwoPanel("One clue", "One clue", colors=(BLUE, TEAL), top=3.45, bottom=0.55, width=10.85, gap=0.46)
        panels.left_frame.set_fill(BLUE, opacity=0.24)
        panels.right_frame.set_fill(TEAL, opacity=0.24)
        bone = limb(0).scale(0.42).rotate(-0.63)
        strip = protein_icon(width=3.14)
        panels.put(bone, "left")
        panels.put(strip, "right")
        for picture in (bone, strip):
            picture.shift(0.24 * DOWN)
        self.at("One limb")
        self.play(FadeIn(panels.left_frame), FadeIn(bone, shift=RIGHT * 0.28), run_time=1.02)
        self.play(FadeIn(panels.left_head), run_time=0.42)
        self.at("small protein")
        self.play(FadeIn(panels.right_frame), FadeIn(strip, shift=LEFT * 0.28), run_time=0.85)
        self.play(FadeIn(panels.right_head), run_time=0.41)
        uncertainty = VGroup(*(slab(4.68, 1.48, picture.get_x(), picture.get_y(), GREY, opacity=0, border=3)
                               for picture in (bone, strip)))
        self.at("settle every relationship")
        self.play(Create(uncertainty[0]), Create(uncertainty[1]), run_time=1.05)
        flipper = limb(2).scale(0.42).rotate(-0.90).set_color(GREY)
        # A continuous fin contrasts with the flipper's articulated bones.
        fin = VMobject(stroke_color=GREY, stroke_width=3, fill_color=GREY, fill_opacity=0.55)
        fin.start_new_path(xy(-0.75, -0.32))
        fin.add_cubic_bezier_curve_to(xy(-0.32, -0.11), xy(0.13, 0.48), xy(0.78, 0.52))
        fin.add_cubic_bezier_curve_to(xy(0.48, 0.20), xy(0.41, -0.24), xy(0.54, -0.45))
        fin.add_cubic_bezier_curve_to(xy(0.16, -0.31), xy(-0.33, -0.47), xy(-0.75, -0.45))
        fin.close_path()
        different = VGroup(flipper, fin).arrange(RIGHT, buff=0.42).move_to(bone)
        self.at("Similar jobs")
        self.play(FadeOut(bone), run_time=0.28)
        self.play(LaggedStart(FadeIn(flipper), FadeIn(fin), lag_ratio=0.30), run_time=0.86)
        self.at("different structures")
        job = label("Similar jobs", different.get_x(), 2.51, size=29)
        self.play(FadeIn(job), run_time=0.64)
        self.at("Scientists compare")
        self.play(FadeOut(panels.left_head), FadeOut(panels.right_head), FadeOut(job), run_time=0.54)
        self.play(FadeOut(panels.left_frame), FadeOut(panels.right_frame), FadeOut(different), FadeOut(strip),
                  uncertainty[0].animate.scale(0.40).move_to(xy(4.04, -1.74)),
                  uncertainty[1].animate.scale(0.34).move_to(xy(4.04, -1.74)), run_time=0.65)
        for cue, clue in (
            ("more body parts", clue_panel("structure", 0, "More body parts", stacked=True)),
            ("more sequences", clue_panel("sequence", 4.04, "More sequences", stacked=True)),
            ("fossil record", clue_panel("fossil", -4.04, "Fossil record", stacked=True)),
        ):
            self.at(cue)
            self.play(FadeIn(clue, shift=UP * 0.38), run_time=1.07)
        self.finish()


class S13Return(SpokenScene):
    def construct(self):
        field = tree_field()
        fossils = fossil_base()
        tree = lineage_tree()
        self.add(field, fossils, scope_tag(size=28))
        self.at("Return to the family tree")
        self.play(Create(tree[0]),
                  LaggedStart(*(Create(branch) for branch in tree[1]), lag_ratio=0.26), run_time=1.66)
        icons = [chapter_one.bone_icon(BLUE).scale(0.72).move_to(xy(x, 0.45)) for x in SPECIES_X[:2]]
        self.at("Matching parts", lead=0.56)
        self.play(LaggedStart(*(FadeIn(icon) for icon in icons), lag_ratio=0.25), run_time=0.80)
        self.at("inherited construction")
        node = xy(-1.775, -0.97)
        trails = [path((x, 0.45), (x, -0.29), (-1.775, -0.97), color=BLUE, width=6) for x in SPECIES_X[:2]]
        self.play(*(Create(trail) for trail in trails),
                  *(MoveAlongPath(icon, trail) for icon, trail in zip(icons, trails)), run_time=1.51)
        self.play(*(FadeOut(icon, target_position=node) for icon in icons), run_time=0.40)
        self.at("Similar sequences", lead=0.36)
        strips = [sequence_row(seq, 0, None)[0] for seq in PROTEINS[:2]]
        for row, center in zip(strips, (xy(-3.55, 1.73), xy(0.0, 1.73))):
            row.scale(0.44).move_to(center)
        # The returning rows use plain blocks; full-sized residue text belongs to the alignment.
        for row in strips:
            for cell in row:
                cell.remove(cell[1])
        self.play(LaggedStart(*(FadeIn(row, shift=UP * 0.31) for row in strips), lag_ratio=0.32), run_time=1.10)
        self.at("the same protein")
        self.play(FadeIn(label("Same protein", -1.775, 2.57, size=33, color=TEAL)),
                  LaggedStart(*(cell[0].animate.set_fill(TEAL, opacity=0.72)
                                for row in strips for cell in row[:5]), lag_ratio=0.09), run_time=1.52)
        self.at("independent check")
        teal = bracket((0, 1), 1.20, TEAL)
        sequence_focus = slab(6.4, 0.81, -1.775, 1.73, TEAL, opacity=0.35).set_z_index(-1)
        self.play(Create(teal), GrowFromEdge(sequence_focus, LEFT), run_time=1.43)
        self.at("both fit one branch")
        confirmed = lineage_tree((0, 1))
        check = path((-1.775, 1.19), (-1.775, -0.82), color=TEAL, width=5)
        self.play(Create(check), run_time=1.44)
        self.at("common ancestry")
        self.play(Transform(tree[1], confirmed[1]),
                  Create(confirmed[2]), GrowFromCenter(confirmed[3]),
                  GrowFromEdge(paired_wash(), UP),
                  *(FadeOut(trail) for trail in trails), FadeOut(check), run_time=1.45)
        self.play(FadeIn(caption("Common ancestry", size=32, color=GREEN, y=-3.55)), run_time=0.52)
        self.finish()


class S14Scope(SpokenScene):
    def construct(self):
        field, tree, fossils = tree_field(), lineage_tree((0, 1)), fossil_base()
        agreement = paired_wash()
        self.add(field, tree, fossils, agreement, scope_tag(size=28))
        card = [clue_panel(kind, x, title) for kind, x, title in (
            ("fossil", -4.04, "Time"), ("structure", 0, "Structure"), ("sequence", 4.04, "Sequence"))]
        links = evidence_into_tree()
        self.at("different jobs")
        self.play(LaggedStart(*(FadeIn(panel[0], shift=0.45 * UP) for panel in card), lag_ratio=0.22), run_time=1.40)
        self.at("Fossils place")
        self.play(FadeIn(card[0][2]), run_time=0.64)
        self.play(FadeIn(card[0][1]), Create(links[0]), run_time=1.39)
        self.at("Bones of living")
        self.play(FadeIn(card[1][2]), run_time=0.65)
        self.play(FadeIn(card[1][1]), Create(links[1]), run_time=1.04)
        self.at("plus sequences")
        self.play(FadeIn(card[2][2]), run_time=0.63)
        self.play(FadeIn(card[2][1]), Create(links[2]), run_time=1.45)
        self.at("broad agreement")
        self.play(tree[2].animate.set_stroke(GREEN, width=19), tree[3].animate.scale(1.33),
                  agreement.animate.set_fill(GREEN, opacity=0.78), run_time=1.26)
        self.at("uncertainty stays visible")
        unknown = label("?", 4.15, -0.69, size=51, color=GREY)
        unresolved = slab(2.62, 1.76, 3.96, -0.52, BG, opacity=0.72).set_z_index(-2)
        self.play(GrowFromEdge(unresolved, DOWN), FadeIn(unknown), run_time=1.05)
        self.at("open to testing")
        self.play(Indicate(unknown, color=TEXT, scale_factor=1.09), run_time=0.86)
        fade = VGroup(field, tree, fossils, agreement, *card, *links, unknown, unresolved)
        self.play(fade.animate.fade(0.62), run_time=0.65)
        self.finish()


class S15End(EndCard):
    LINE = "Matching structures and protein sequences point to common ancestry."
