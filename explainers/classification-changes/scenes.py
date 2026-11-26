"""The Molecule Behind the Tree.

Colour map from the earlier film: teal = methane makers / Archaea,
blue = typical Bacteria, gold = Eukarya, white = evidence, grey = open claims.
Cell and catalogue drawings are schematic.
"""
from bp_parts import *
from bp_style import EndCard

BAC = "#6F86FF"
EUK = GOLD
CELL_COLOURS = (BAC, TEAL, EUK)
CELL_X = (-4.15, 0, 4.15)
PANEL_FILL = "#2B3141"

QUESTION = "Which pair should sit closer on the ancestry tree?"
QUESTION_STYLE = {"y": -3.15, "size": 34, "max_w": 10.6}
PREDICT_X = (-3.24, 3.24)
METHANE = "ABCDEF"
OTHER_METHANE = "ABCDEG"
BACTERIA = "AHIDJK"
OTHER_BACTERIA = "AHLDJM"


def pt(x, y):
    return np.array([x, y, 0.0])


def cell_icon(colour, at, width=3.36, nucleus=False):
    """The same rounded cell cartoon is carried from the microscope to the tree."""
    body = RoundedRectangle(
        corner_radius=0.62, width=3.36, height=1.92,
        stroke_color=colour, stroke_width=5,
        fill_color=colour, fill_opacity=0.68,
    )
    texture = VGroup(*[
        Dot(pt(x, y), radius=r, color=BG, fill_opacity=0.72)
        for x, y, r in ((-1.08, 0.24, 0.085), (0.05, -0.43, 0.075),
                        (0.71, 0.35, 0.075), (1.05, -0.17, 0.06))
    ])
    cell = VGroup(body, texture)
    if nucleus:
        cell.add(Circle(radius=0.38, color=BG, stroke_width=5,
                        fill_color=BG, fill_opacity=0.39).move_to(pt(-0.36, 0.11)))
    return cell.scale(width / 3.36).move_to(at)


def microscope_cells():
    return VGroup(cell_icon(BAC, pt(-2.08, 0.20)), cell_icon(TEAL, pt(2.08, 0.20)))


def branch(start, end, colour=GREY, width=22):
    line = Line(start, end, color=colour, stroke_width=width)
    line.set_cap_style(CapStyleType.ROUND)
    return line


def unresolved_tree(at=ORIGIN, scale=1, tip_y=0.88):
    root, joint = pt(0, -2.28), pt(0, -0.62)
    tips = (pt(-2.10, tip_y), pt(2.10, tip_y))
    fork = VGroup(branch(root, joint), *(branch(joint, t) for t in tips),
                  Dot(joint, radius=0.14, color=TEXT))
    return fork.scale(scale, about_point=ORIGIN).shift(at)


def hook_tree():
    # The round branch caps meet the outlines from behind the translucent cells.
    fork = unresolved_tree(tip_y=0.80).set_z_index(-1)
    cells = VGroup(cell_icon(BAC, pt(-2.10, 1.70), width=2.85),
                   cell_icon(TEAL, pt(2.10, 1.70), width=2.85))
    return fork, cells


def shared_cells():
    return VGroup(*[cell_icon(c, pt(x, 1.36), nucleus=i == 2)
                    for i, (c, x) in enumerate(zip(CELL_COLOURS, CELL_X))])


def rna_record(at, variant=TEXT):
    segments = VGroup(*[
        RoundedRectangle(corner_radius=0.09, width=w, height=0.50,
                         stroke_width=0, fill_color=c, fill_opacity=0.79)
        for w, c in ((0.72, TEXT), (0.52, variant), (0.94, TEXT), (0.72, variant))
    ]).arrange(RIGHT, buff=0.08)
    return segments.move_to(at)


def shared_records():
    return VGroup(*[rna_record(pt(x, -1.72), c) for x, c in zip(CELL_X, CELL_COLOURS)])


def shared_record_labels():
    ribs = VGroup(*[boxed_label("ribosome", TEXT, size=34, box=(2.76, 0.89),
                               fill_opacity=0.23).move_to(pt(x, -0.46)) for x in CELL_X])
    names = VGroup(*[boxed_label("ribosomal RNA", TEXT, size=29, box=(3.45, 0.78),
                                fill_opacity=0.16).move_to(pt(x, -2.65)) for x in CELL_X])
    return ribs, names


def tile_row(pieces, colour, at, width=0.78, size=32):
    tiles = VGroup(*[
        boxed_label(letter, TEXT, size=size, box=(width, 0.62), pad=0.12,
                    stroke=2, fill_opacity=0, corner_radius=0.09)
        for letter in pieces
    ]).arrange(RIGHT, buff=0.10)
    for tile in tiles:
        tile.box.set_fill(colour, opacity=0.29 if colour == TEXT else 0.50)
        tile.box.set_stroke(colour, opacity=0.9)
    return tiles.move_to(at)


def match_links(top, bottom, first, second, width=8):
    return VGroup(*[
        branch(a.get_bottom() + DOWN * 0.14, b.get_top() + UP * 0.14, TEXT, width)
        for a, b, left, right in zip(top, bottom, first, second) if left == right
    ])


def catalogue_pair(first, second, colours, x, y, separation=1.36, width=0.78, size=32):
    top = tile_row(first, colours[0], pt(x, y + separation / 2), width, size)
    bottom = tile_row(second, colours[1], pt(x, y - separation / 2), width, size)
    return VGroup(match_links(top, bottom, first, second), top, bottom)


def predict_panels():
    panels = TwoPanel("Pair A", "Pair B", colors=(GREY, GREY), top=2.92,
                      bottom=-2.35, width=12.40, gap=0.56, size=34)
    for frame in (panels.left_frame, panels.right_frame):
        frame.set_fill(PANEL_FILL, opacity=1).set_z_index(-2)
    return panels


def predict_pairs(many_gap=1.36, few_gap=2.15):
    return (
        catalogue_pair(METHANE, OTHER_METHANE, (TEXT, TEXT), PREDICT_X[0], 0.57, many_gap),
        catalogue_pair(METHANE, BACTERIA, (TEXT, TEXT), PREDICT_X[1], 0.57, few_gap),
    )


def predict_branches():
    forks = VGroup()
    for x in PREDICT_X:
        joint = pt(x, -1.99)
        ends = (pt(x - 0.88, -1.27), pt(x + 0.88, -1.27))
        forks.add(VGroup(*[branch(joint, e, TEXT, 12) for e in ends],
                         *[Circle(radius=0.125, color=TEXT, stroke_width=4).move_to(e)
                           for e in ends]))
    return forks


def predict_markers():
    return VGroup(*[T("?", 36, GOLD, weight=BOLD).move_to(pt(x, -1.32)) for x in PREDICT_X])


def predict_question():
    card = question_card(QUESTION, **QUESTION_STYLE).set_z_index(1)
    plate = RoundedRectangle(corner_radius=0.15, width=10.65, height=0.84,
                             stroke_width=0, fill_color="#3A3127", fill_opacity=1).move_to(card).set_z_index(-1)
    return VGroup(plate, card)


def domain_cells():
    return shared_cells().shift(UP * 0.30)


def domain_tree(hinge=None, combined=False):
    """Build the same root, tips and unaffected gold branch at each stage."""
    root = pt(0, -2.77)
    joint = pt(0, -1.36)
    hinge = pt(0, -1.36) if hinge is None else hinge
    tips = tuple(pt(x, 0.72) for x in CELL_X)
    trunk = branch(root, joint)
    gold = branch(joint, tips[2], EUK)
    stem = branch(joint, hinge, GREY, 20) if combined else None
    pair = VGroup(branch(hinge, tips[0], BAC), branch(hinge, tips[1], TEAL))
    node = Dot(hinge, radius=0.145, color=TEXT)
    return trunk, gold, stem, pair, node


def domain_labels():
    return VGroup(*[T(name, 35, colour, weight=BOLD).move_to(pt(x, 3.02))
                    for name, colour, x in zip(("Bacteria", "Archaea", "Eukarya"),
                                               CELL_COLOURS, CELL_X)])


def model_tag():
    return scope_tag("best-supported model", size=28, color=TEXT)


def evidence_card(text, x, y):
    card = boxed_label(text, TEXT, size=32, pad=0.24, fill_opacity=0)
    card.box.set_fill(PANEL_FILL, opacity=1)
    return card.move_to(pt(x, y))


def cell_outline(cell, colour):
    return cell[0].copy().scale(1.05).set_fill(opacity=0).set_stroke(colour, width=7)


class S00Hook(SpokenScene):
    def construct(self):
        ring = Ellipse(width=9.48, height=5.72, color=GREY, stroke_width=7,
                       fill_color=PANEL_FILL, fill_opacity=1).move_to(UP * 0.22)
        cells = microscope_cells()
        question = question_card("Why a different branch?", y=-3.32, size=43)
        self.at("These methane making microbes")
        self.add(ring, cells[1])
        self.play(Rotate(cells[1], angle=0.30), run_time=1.65)
        self.at("look like typical bacteria")
        self.play(FadeIn(cells[0], shift=UP * 0.12), run_time=0.65)
        self.play(Rotate(cells[0], angle=0.30), FadeIn(question), run_time=1.50)
        self.at("Why would a molecule")
        self.play(ring.animate.set_stroke(TEXT, width=9), run_time=1.40)
        self.at("Under the microscope")
        self.play(Rotate(cells[0], angle=-0.30), Rotate(cells[1], angle=-0.30),
                  ring.animate.stretch(0.91, 0), run_time=2.25)
        self.at("cells without nuclei")
        outlines = VGroup(cell_outline(cells[0], BAC), cell_outline(cells[1], TEAL))
        self.play(Create(outlines, lag_ratio=0.25), run_time=1.05)
        fork, targets = hook_tree()
        self.at("Shape gives us evidence")
        self.play(FadeOut(question), FadeOut(outlines), run_time=0.50)
        self.play(ReplacementTransform(ring, fork[0]),
                  Transform(cells[0], targets[0]), Transform(cells[1], targets[1]), run_time=1.25)
        self.at("it may hide the ancestry")
        self.play(LaggedStart(Create(fork[1]), Create(fork[2]), lag_ratio=0.25),
                  FadeIn(fork[3]), run_time=1.35)
        self.add(scope_tag(size=28, color=TEXT))
        self.finish()


class S01Title(TitleCard):
    LESSON = "Classification Changes"
    TITLE = "The Molecule Behind the Tree"

    def construct(self):
        fork, cells = hook_tree()
        self.add(fork, cells, scope_tag(size=28, color=TEXT))
        title = T(self.TITLE, size=52, font=TITLE_FONT).move_to(pt(0, 3.22))
        base = caption(self.TITLE, size=30, y=-3.15).set_x(0)
        self.play(Write(title), run_time=0.70)
        self.wait(0.52)
        self.play(swap(title, base, run_time=0.60))
        self.wait(0.18)


class S02Shared(SpokenScene):
    def construct(self):
        fork, old_cells = hook_tree()
        cells = shared_cells()
        record_targets = shared_records()
        title = caption(S01Title.TITLE, size=30, y=-3.15).set_x(0)
        schematic = scope_tag(size=28, color=TEXT)
        self.add(fork, old_cells, title, schematic)
        self.at("To compare very different cells")
        self.play(FadeOut(fork), FadeOut(title), FadeOut(schematic),
                  Transform(old_cells[0], cells[0]), Transform(old_cells[1], cells[1]), run_time=1.45)
        self.at("scientists need the same kind")
        self.play(FadeIn(cells[2], shift=LEFT * 0.48), run_time=2.10)

        ribs, strands = shared_record_labels()
        self.at("Every cell builds proteins")
        self.play(LaggedStart(*[FadeIn(r, shift=DOWN * 0.30) for r in ribs], lag_ratio=0.36),
                  run_time=2.35)
        self.at("Ribosomal RNA forms")
        records = VGroup(*[rna_record(r.get_center()) for r in record_targets])
        self.play(LaggedStart(*[FadeIn(r, shift=DOWN * 0.30) for r in records], lag_ratio=0.22),
                  run_time=1.55)
        self.play(LaggedStart(*[FadeIn(s) for s in strands], lag_ratio=0.20), run_time=1.38)
        self.at("Conserved parts let researchers")
        highlights = VGroup(*[
            SurroundingRectangle(r[0], color=TEXT, buff=0.065, stroke_width=4)
            for r in records
        ])
        self.play(LaggedStart(*[Create(h) for h in highlights], lag_ratio=0.42), run_time=1.60)
        self.at("line up distant samples")
        self.play(LaggedStart(*[r[2].animate.set_fill(opacity=1) for r in records], lag_ratio=0.35),
                  run_time=0.95)
        self.at("while differing parts")
        self.play(FadeOut(highlights), *[Transform(r, target) for r, target in zip(records, record_targets)],
                  run_time=1.45)
        self.finish()


class S03Catalogues(SpokenScene):
    def construct(self):
        cells, records = shared_cells(), shared_records()
        ribs, rna_names = shared_record_labels()
        self.add(cells, records, ribs, rna_names)
        fork = unresolved_tree(at=pt(4.15, 0.42), scale=0.69)
        panel = RoundedRectangle(corner_radius=0.2, width=6.72, height=5.46,
                                 color=GREY, stroke_width=2.5, fill_color=PANEL_FILL,
                                 fill_opacity=1).move_to(pt(-2.76, 0.12)).set_z_index(-1)
        self.at("Wose and Fox compared")
        self.play(FadeOut(cells), FadeOut(ribs), FadeOut(rna_names), run_time=0.80)
        copied = records[1].copy()
        self.add(copied)
        self.play(FadeIn(panel), FadeOut(records[0]), FadeOut(records[2]),
                  records[1].animate.move_to(pt(-2.76, 1.53)),
                  copied.animate.move_to(pt(-2.76, -1.29)), run_time=1.55)
        self.at("short ribosomal RNA pieces")
        self.play(LaggedStart(*[Create(b) for b in fork], lag_ratio=0.23), run_time=1.82)
        open_pair = catalogue_pair(METHANE, OTHER_METHANE, (TEAL, TEAL), -2.76, 0.12,
                                   separation=2.82, width=0.91, size=34)
        self.at("Picture each catalog")
        self.play(FadeOut(records[1]), FadeOut(copied), run_time=0.36)
        self.play(LaggedStart(*[FadeIn(t) for row in open_pair[1:] for t in row], lag_ratio=0.10),
                  run_time=2.26)
        self.at("not a complete molecule")
        self.play(FadeIn(scope_tag(size=28, color=TEXT)), run_time=0.60)
        self.at("Matching tiles pull")
        close = catalogue_pair(METHANE, OTHER_METHANE, (TEAL, TEAL), -2.76, 0.12,
                               separation=1.47, width=0.91, size=34)
        self.play(LaggedStart(*[Create(line) for line in open_pair[0]], lag_ratio=0.25), run_time=1.15)
        self.play(Transform(open_pair, close), run_time=1.32)
        far = catalogue_pair(METHANE, BACTERIA, (TEAL, BAC), -2.76, 0.12,
                             separation=2.82, width=0.91, size=34)
        blue_near = catalogue_pair(METHANE, BACTERIA, (TEAL, BAC), -2.76, 0.12,
                                   separation=1.47, width=0.91, size=34)
        self.at("Fewer matches leave")
        self.play(FadeOut(open_pair[0]), FadeOut(open_pair[2]), run_time=0.38)
        self.play(FadeIn(blue_near[2]), Create(blue_near[0]), run_time=0.78)
        self.play(Transform(open_pair[1], far[1]), Transform(blue_near[2], far[2]),
                  Transform(blue_near[0], far[0]), run_time=1.62)
        self.at("The pattern across pairs")
        route = branch(pt(0.77, -0.02), fork[3].get_left() + LEFT * 0.12, TEXT, 7)
        self.play(Create(route), fork[3].animate.scale(1.42), run_time=2.10)
        self.finish()


class S04Predict(SpokenScene):
    def construct(self):
        panels = predict_panels()
        many, open_few = predict_pairs()
        open_many, few = predict_pairs(many_gap=2.15, few_gap=1.36)
        forks = predict_branches()
        markers = predict_markers()
        plate, q = predict_question()
        self.at("Here are hidden pairs")
        self.add(panels)
        self.play(LaggedStart(FadeIn(open_many[1:]), FadeIn(few[1:]), lag_ratio=0.31), run_time=1.72)
        self.at("A pair shares many")
        self.play(LaggedStart(*[Create(line) for line in open_many[0]], lag_ratio=0.26), run_time=1.20)
        self.play(Transform(open_many, many), run_time=1.58)
        self.at("while another shares few")
        self.play(LaggedStart(*[Create(line) for line in few[0]], lag_ratio=0.60), run_time=0.78)
        self.play(Transform(few, open_few), run_time=1.32)
        self.at("Which pair should sit closer")
        self.play(FadeIn(q), LaggedStart(*[Create(fork) for fork in forks], lag_ratio=0.44),
                  run_time=2.30)
        self.at("Hold your answer")
        self.play(FadeIn(plate), LaggedStart(FadeIn(markers[0], shift=DOWN * 0.30),
                              FadeIn(markers[1], shift=DOWN * 0.30), lag_ratio=0.70), run_time=1.55)
        self.finish()


class S05Pause(PredictPause):
    QUESTION = QUESTION
    SECONDS = 4.5
    CARD = QUESTION_STYLE
    RING_AT = (5.9, -3.15, 0)

    def backdrop(self):
        return VGroup(predict_panels(), *predict_pairs(), predict_branches(), predict_markers())

    def construct(self):
        self.add(self.backdrop(), predict_question())
        ring, run = countdown(self.SECONDS, center=self.RING_AT, radius=0.51)
        self.add(ring)
        self.play(run)


class S06Reveal(SpokenScene):
    def construct(self):
        panels, (many, few), forks = predict_panels(), predict_pairs(), predict_branches()
        q, markers = predict_question(), predict_markers()
        self.add(panels, many, few, forks, q, markers)
        self.at("The pair with many shared pieces")
        close = catalogue_pair(METHANE, OTHER_METHANE, (TEXT, TEXT), PREDICT_X[0], 0.57,
                               separation=1.08)
        self.play(Transform(many, close), FadeOut(markers),
                  panels.left_frame.animate.set_fill("#3B465C", opacity=1), run_time=1.36)
        self.at("belongs closer")
        left_branch, right_branch, left_tip, right_tip = forks[0]
        joint = left_branch.get_start()
        left_end = left_tip.get_center() + RIGHT * 0.37
        right_end = right_tip.get_center() + LEFT * 0.37
        self.play(Transform(left_branch, branch(joint, left_end, TEXT, 12)),
                  Transform(right_branch, branch(joint, right_end, TEXT, 12)),
                  left_tip.animate.move_to(left_end), right_tip.animate.move_to(right_end),
                  run_time=1.18)
        self.at("The methane makers matched", lead=1.05)
        self.play(FadeOut(q), FadeOut(forks), run_time=0.85)

        x = -3.48
        teal_pair = catalogue_pair(METHANE, OTHER_METHANE, (TEAL, TEAL), x, 2.30,
                                   separation=0.99, width=0.69, size=28)
        mixed_pair = catalogue_pair(METHANE, BACTERIA, (TEAL, BAC), x, -2.33,
                                    separation=0.99, width=0.69, size=28)
        blue_pair = catalogue_pair(BACTERIA, OTHER_BACTERIA, (BAC, BAC), x, -0.02,
                                   separation=0.99, width=0.69, size=28)
        # The comparison stays on the left while its implication appears on the right.
        centre = pt(3.55, 0)
        left_tip, right_tip = pt(1.94, 1.48), pt(5.16, 1.48)
        attachment, old_joint = pt(3.55, -2.33), pt(3.55, -0.90)
        old = VGroup(branch(attachment, old_joint, GREY, 16),
                     branch(old_joint, left_tip, BAC, 17),
                     branch(old_joint, right_tip, TEAL, 17),
                     Dot(old_joint, radius=0.13, color=TEXT))
        icons = VGroup(cell_icon(BAC, left_tip + UP * 0.54, width=1.96),
                       cell_icon(TEAL, right_tip + UP * 0.54, width=1.96))
        self.play(FadeOut(panels.left_head), FadeOut(panels.right_head), run_time=0.27)
        self.play(FadeOut(VGroup(panels.left_frame, panels.right_frame)), FadeOut(few),
                  ReplacementTransform(many, teal_pair), Create(old[0]), run_time=1.33)
        teal_name = place_label(T("Methane makers", 30, TEAL, weight=BOLD), teal_pair,
                               dirs=(UP,), buff=0.16)
        self.play(FadeIn(teal_name), run_time=0.64)
        self.at("than they matched typical")
        self.play(FadeIn(mixed_pair, shift=LEFT * 0.28), Create(old[1]), FadeIn(icons[0]), run_time=1.70)
        mixed_name = place_label(T("Between groups", 30, TEXT, weight=BOLD), mixed_pair,
                                dirs=(UP,), buff=0.16)
        self.play(FadeIn(mixed_name), run_time=0.57)
        self.at("Typical bacteria also matched")
        self.play(FadeIn(blue_pair, shift=LEFT * 0.28), run_time=1.53)
        blue_name = place_label(T("Typical bacteria", 30, BAC, weight=BOLD), blue_pair,
                               dirs=(UP,), buff=0.16)
        self.play(FadeIn(blue_name), run_time=0.67)

        self.at("better than they matched methane")
        self.play(Create(old[2]), FadeIn(old[3]), FadeIn(icons[1]), run_time=1.65)
        self.at("That repeated pattern challenged")
        contact = pt(2.98, -1.12)
        evidence = VGroup(*[branch(pt(-0.99, y), contact, TEXT, 4)
                            for y in (2.30, -0.02, -2.33)])
        new_joint = pt(4.04, -1.25)
        self.play(LaggedStart(*[Create(line) for line in evidence], lag_ratio=0.26), run_time=1.22)
        self.play(Transform(old[0], branch(attachment, new_joint, GREY, 16)),
                  Transform(old[1], branch(new_joint, left_tip, BAC, 17)),
                  Transform(old[2], branch(new_joint, right_tip, TEAL, 17)),
                  old[3].animate.move_to(new_joint), run_time=0.82)
        self.at("combined prokaryote group")
        old_label = T("Combined prokaryotes?", 32, TEXT).move_to(centre + DOWN * 2.88)
        self.play(FadeOut(evidence), FadeIn(old_label), FadeOut(old[0]),
                  FadeIn(scope_tag(size=28, color=TEXT)), run_time=0.73)
        self.finish()


class S06Claim(SpokenScene):
    def construct(self):
        hinge = pt(-2.26, -0.43)
        trunk, gold, stem, pair, node = domain_tree(hinge, combined=True)
        cells = domain_cells()
        tag = evidence_card("ancestry claim", -4.38, -0.98)
        pointer = branch(tag.get_right() + RIGHT * 0.16, hinge + LEFT * 0.14, TEXT, 4)
        self.at("A classification is")
        self.add(cells)
        self.play(LaggedStart(Create(trunk), Create(stem), Create(pair), Create(gold), FadeIn(node),
                              lag_ratio=0.20), run_time=2.75)
        self.at("A branch claims")
        self.play(FadeIn(tag), Create(pointer), run_time=1.35)
        self.at("more recent common ancestor")
        self.play(stem.animate.set_stroke(TEXT, width=27), run_time=1.40)
        self.at("When several comparisons challenge")
        links = VGroup(*[branch(pt(x, -2.50), hinge + pt(x * 0.06, -0.13), TEXT, 5)
                            for x in (-5.36, -4.08, -2.78)])
        self.play(FadeOut(tag), FadeOut(pointer), run_time=0.40)
        self.play(LaggedStart(*[Create(line) for line in links], lag_ratio=0.35), run_time=2.55)
        self.at("scientists redraw only")
        _, _, _, revised, revised_node = domain_tree()
        self.play(FadeOut(stem), FadeOut(links), Transform(pair, revised), Transform(node, revised_node),
                  run_time=2.00)
        self.at("The organisms themselves")
        outlines = VGroup(*[cell_outline(c, colour) for c, colour in zip(cells[:2], CELL_COLOURS)])
        self.play(LaggedStart(*[Create(r) for r in outlines], lag_ratio=0.30), run_time=1.48)
        self.at("remain unchanged")
        self.play(FadeOut(outlines), run_time=0.88)
        self.finish()


class S07Domains(SpokenScene):
    def construct(self):
        trunk, gold, _, pair, node = domain_tree()
        cells = domain_cells()
        labs = domain_labels()
        date_1977 = M("1977", 31, TEXT).move_to(pt(-0.85, -3.21))
        date_1990 = M("1990", 31, TEXT).move_to(pt(0.85, -3.21))
        self.add(trunk, gold, pair, node, cells)
        self.at("The researchers interpreted this pattern")
        paths = VGroup(*[b.copy().set_stroke(TEXT, width=28) for b in (*pair, gold)])
        self.play(LaggedStart(*[Create(p) for p in paths], lag_ratio=0.50), run_time=2.53)
        self.at("three major lines of descent")
        self.play(FadeIn(date_1977), FadeOut(paths), run_time=1.40)
        self.at("the rank called domain")
        self.play(swap(date_1977, date_1990, run_time=0.63))
        self.at("named bacteria")
        self.play(FadeIn(labs[0], shift=UP * 0.15), cells[0][0].animate.set_fill(opacity=0.93), run_time=0.70)
        self.at("archaea and eukarya")
        self.play(FadeIn(labs[1], shift=UP * 0.15), cells[1][0].animate.set_fill(opacity=0.93), run_time=0.64)
        self.play(FadeIn(labs[2], shift=UP * 0.15), cells[2][0].animate.set_fill(opacity=0.93), run_time=0.75)
        self.at("The methane makers joined")
        signal = pair[1].copy().reverse_direction().set_stroke(TEXT, width=29)
        self.play(Create(signal), cells[0][0].animate.set_fill(opacity=0.68),
                  cells[2][0].animate.set_fill(opacity=0.68), run_time=1.58)
        self.at("Their cells did not change")
        still = cell_outline(cells[1], TEAL)
        self.play(FadeOut(signal), Create(still), run_time=1.60)
        self.at("The evidence changed")
        self.play(FadeOut(date_1990), FadeOut(still), cells[1][0].animate.set_fill(opacity=0.68),
                  node.animate.set_color(TEXT).scale(1.33), run_time=1.54)
        self.finish()


class S07Evidence(SpokenScene):
    def construct(self):
        trunk, gold, _, pair, node = domain_tree()
        node.scale(1.33)
        cells = domain_cells()
        labs = domain_labels()
        self.add(trunk, gold, pair, node, cells, labs)
        rna = evidence_card("RNA", 4.70, -0.34)
        dna = evidence_card("DNA", 4.70, -1.62)
        structure = evidence_card("structure", -4.70, -0.34)
        development = evidence_card("development", -4.70, -1.62)
        self.at("Molecular evidence does not")
        self.play(LaggedStart(FadeIn(rna, shift=LEFT * 0.35), FadeIn(dna, shift=LEFT * 0.35),
                              lag_ratio=0.66), run_time=2.44)
        self.at("every other clue")
        self.play(FadeIn(structure, shift=RIGHT * 0.35), run_time=1.22)
        self.at("It adds a comparison")
        outlines = VGroup(cell_outline(cells[0], BAC), cell_outline(cells[1], TEAL))
        self.play(LaggedStart(*[Create(o) for o in outlines], lag_ratio=0.42), run_time=2.25)
        self.at("similarities in shape")
        self.play(FadeOut(outlines), rna.box.animate.set_stroke(TEXT, width=6), run_time=1.37)
        self.at("Strong classifications weigh")
        self.play(FadeIn(development, shift=RIGHT * 0.35), run_time=1.45)
        self.at("several markers")
        self.play(rna.animate.shift(LEFT * 0.28), structure.animate.shift(RIGHT * 0.28),
                  run_time=1.37)
        self.at("Agreement strengthens")
        self.play(rna.animate.move_to(pt(2.45, -1.68)),
                  dna.animate.move_to(pt(2.45, -2.73)),
                  development.animate.move_to(pt(-2.47, -2.48)),
                  run_time=1.38)
        self.play(pair[1].animate.set_stroke(TEAL, width=31), run_time=0.93)
        self.at("Conflict")
        mark = T("?", 52, GOLD, weight=BOLD).move_to(pt(-1.65, -1.20))
        self.play(swap(structure, mark, run_time=0.69))
        self.wait(1.05)
        self.play(FadeOut(development), FadeOut(rna), FadeOut(dna),
                  pair[1].animate.set_stroke(TEAL, width=22), FadeOut(mark), run_time=0.55)
        self.finish()


class S08Limits(SpokenScene):
    def construct(self):
        trunk, gold, _, pair, node = domain_tree()
        node.scale(1.33)
        self.add(trunk, gold, pair, node, domain_cells(), domain_labels())
        percent = boxed_label("% DNA", TEXT, size=49, box=(3.62, 1.32))
        percent.box.set_fill(PANEL_FILL, opacity=1)
        percent.move_to(pt(-4.43, -1.50))
        clock = VGroup(Circle(radius=0.82, color=TEXT, stroke_width=5,
                              fill_color=PANEL_FILL, fill_opacity=1),
                       branch(ORIGIN, UP * 0.46, TEXT, 8),
                       branch(ORIGIN, RIGHT * 0.41, TEXT, 8)).move_to(pt(4.48, -1.42))
        self.at("The overlap scores")
        self.play(FadeIn(percent, shift=RIGHT * 0.55), run_time=1.14)
        self.at("are not percentages")
        self.play(FadeOut(percent, shift=LEFT * 0.65), run_time=1.53)
        self.at("They do not tell when")
        self.play(FadeIn(clock, shift=LEFT * 0.62), run_time=0.87)
        self.at("branches split")
        self.play(FadeOut(clock, shift=RIGHT * 0.65), run_time=1.05)

        example = catalogue_pair(METHANE, BACTERIA, (TEAL, BAC), -3.68, -1.79,
                                 separation=1.22, width=0.67, size=28)
        self.at("They summarize shared pieces")
        self.play(LaggedStart(FadeIn(example[1]), FadeIn(example[2]), lag_ratio=0.28), run_time=1.28)
        self.at("in these ribosomal RNA catalogs")
        matches = [tile.box for row, pieces, other in
                   ((example[1], METHANE, BACTERIA), (example[2], BACTERIA, METHANE))
                   for tile, a, b in zip(row, pieces, other) if a == b]
        self.play(LaggedStart(*[Create(l) for l in example[0]], lag_ratio=0.75),
                  *[m.animate.set_fill(opacity=0.85) for m in matches], run_time=1.80)
        self.at("A tree remains a claim")
        self.play(FadeOut(example), FadeIn(model_tag()), run_time=1.44)
        options = (evidence_card("more organisms", -4.24, -1.62),
                   evidence_card("other genes", 4.23, -1.30),
                   evidence_card("membranes", 4.22, -2.27))
        self.at("tested against more organisms")
        self.play(FadeIn(options[0], shift=RIGHT * 0.46), run_time=1.54)
        self.at("other genes")
        self.play(FadeIn(options[1], shift=LEFT * 0.46), run_time=1.06)
        self.at("membranes")
        self.play(FadeIn(options[2], shift=LEFT * 0.46), run_time=0.86)
        self.at("any evidence that can challenge")
        line = branch(options[0].get_right() + RIGHT * 0.18, node.get_left() + LEFT * 0.15, TEXT, 5)
        self.play(Create(line), run_time=0.65)
        self.wait(1.47)
        self.play(FadeOut(VGroup(*options)), FadeOut(line), run_time=0.60)
        self.finish()


class S09Close(SpokenScene):
    def construct(self):
        trunk, gold, _, pair, node = domain_tree()
        node.scale(1.33)
        tree = VGroup(trunk, gold, pair, node)
        cells, labs, model = domain_cells(), domain_labels(), model_tag()
        self.add(tree, cells, labs, model)
        self.at("That is why changing a group")
        path = pair[1].copy().reverse_direction().set_stroke(TEXT, width=26)
        self.play(Create(path), run_time=1.65)
        self.at("after careful testing")
        card = evidence_card("evidence", -4.42, -1.94)
        line = branch(card.get_right() + RIGHT * 0.16, node.get_left() + LEFT * 0.16, TEXT, 8)
        self.play(FadeIn(card, shift=RIGHT * 0.50), Create(line), run_time=2.17)

        case = RoundedRectangle(corner_radius=0.20, width=4.85, height=4.78,
                                stroke_color=GREY, stroke_width=6, fill_color=PANEL_FILL,
                                fill_opacity=1).set_z_index(-1)
        drawers = VGroup(*[
            RoundedRectangle(corner_radius=0.10, width=4.25, height=1.23,
                             fill_color=c, color=c, fill_opacity=0.35, stroke_width=3).move_to(pt(0, y))
            for c, y in zip(CELL_COLOURS, (1.42, 0, -1.42))
        ])
        handles = VGroup(*[branch(d.get_center() + LEFT * 0.39,
                                  d.get_center() + RIGHT * 0.39, TEXT, 8) for d in drawers])
        bodies = [cell[0] for cell in cells]
        detail = VGroup(*(piece for cell in cells for piece in cell[1:]))
        original_bodies = [body.copy() for body in bodies]
        self.at("Classification is a model")
        self.play(FadeOut(path), FadeOut(line), FadeOut(card), run_time=0.73)
        self.at("not a permanent filing cabinet", lead=0.44)
        self.play(FadeOut(tree), FadeOut(labs), FadeOut(model), FadeOut(detail), run_time=0.32)
        self.play(FadeIn(case), *[Transform(body, d) for body, d in zip(bodies, drawers)], run_time=0.96)
        self.play(Create(handles), run_time=0.40)
        self.at("When stronger evidence changes")
        self.play(FadeOut(case), FadeOut(handles),
                  *[Transform(body, original) for body, original in zip(bodies, original_bodies)], run_time=0.94)
        self.play(FadeIn(tree), FadeIn(detail), FadeIn(labs), run_time=0.65)
        self.at("changes the picture", lead=0)
        stronger = evidence_card("stronger evidence", -4.27, -1.85)
        new = branch(stronger.get_right() + RIGHT * 0.16, pt(-0.32, -1.38), TEXT, 8)
        self.play(FadeIn(stronger, shift=RIGHT * 0.45), Create(new), run_time=1.38)
        self.at("scientists revise the model")
        trace = pair[1].copy().set_stroke(TEXT, width=22)
        self.play(FadeOut(new), FadeOut(stronger), Create(trace), FadeIn(model), run_time=1.36)
        self.at("keeping its limits visible")
        self.play(FadeOut(trace), FadeIn(evidence_card("limits", 3.02, -2.35), shift=LEFT * 0.48), run_time=1.30)
        self.finish()


class S10End(EndCard):
    LINE = "Classification changes when new evidence changes\nthe best-supported picture of ancestry."
