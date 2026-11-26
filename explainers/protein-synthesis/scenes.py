"""From Gene Copy to Protein Chain.

BLUE = DNA, GREEN = messenger RNA, GOLD = ribosome, PURPLE = transfer RNA,
RED = amino acids and protein, TEAL = transcription enzyme and nuclear pore,
GREY = cell and nucleus boundaries, TEXT = stop signal and neutral labels.
"""
from bp_parts import *  # noqa: F403
from bp_style import EndCard


PURPLE = "#B58CD9"
CYTOPLASM = "#303A46"
NUCLEUS = "#1D303D"
DNA_TO_RNA = str.maketrans("ATCG", "UAGC")
DNA_COMPLEMENT = str.maketrans("ATCG", "TAGC")
RNA_COMPLEMENT = str.maketrans("AUCG", "UAGC")
TEMPLATE = "TACGATCGGACT"
MESSAGE = TEMPLATE.translate(DNA_TO_RNA)
CODONS = tuple(MESSAGE[i:i + 3] for i in range(0, len(MESSAGE), 3))
AMINO_ACIDS = ("Met", "Leu", "Ala")
PAIRING_BASES = "ATCG"
QUESTION = "Which mRNA group pairs with TAC?"
PORE_Y = -0.48
RELEASED_RNA_Y = -1.33


def point(x, y):
    return np.array([x, y, 0.0])


def base(letter, color, width=0.64, size=30, filled=True, stroke=2.5):
    if letter:
        block = boxed_label(letter, color, size=size, min_size=size, box=(width, width),
                            pad=0.045, stroke=stroke, fill_opacity=0.23, corner_radius=0.11)
        block.label.set_z_index(1)
        return block
    return RoundedRectangle(width=width, height=width, corner_radius=0.11,
                            stroke_color=color, stroke_width=2.5,
                            fill_color=color, fill_opacity=0.28 if filled else 0)


def base_row(sequence, color, *, width=0.64, gap=0.1, size=30, at=ORIGIN, stroke=2.5):
    return VGroup(*(base(letter, color, width, size, stroke=stroke) for letter in sequence)).arrange(
        RIGHT, buff=gap
    ).move_to(at)


def cell_field(*, closeup=False, transcribing=False):
    if closeup:
        color = NUCLEUS if transcribing else CYTOPLASM
        frame = RoundedRectangle(width=13.5, height=6.85, corner_radius=1.05,
                                 stroke_width=0, fill_color=color, fill_opacity=1)
    else:
        frame = Ellipse(width=13.0, height=6.78, stroke_color=GREY, stroke_width=3,
                        fill_color=CYTOPLASM, fill_opacity=1)
    return frame.set_z_index(-10)


def ribosome(at, *, scale=1, opened=False):
    """The cartoon's upper lobes leave an opening for the incoming tRNA."""
    gold_fill = interpolate_color(ManimColor(GOLD), ManimColor(BG), 0.63)
    lower = RoundedRectangle(width=2.68, height=0.8, corner_radius=0.38,
                             color=GOLD, stroke_width=3, fill_color=gold_fill, fill_opacity=1)
    lower.move_to(DOWN * (1.08 if opened else 1.0))
    upper = VGroup()
    for side in (-1, 1):
        lobe = RoundedRectangle(width=0.66, height=0.81, corner_radius=0.31,
                                color=GOLD, stroke_width=3, fill_color=gold_fill, fill_opacity=1)
        lobe.move_to(point(side * (1.58 if opened else 1.49), 1.37 if opened else 0.85))
        upper.add(lobe)
    return VGroup(lower, upper).set_z_index(-2).scale(scale, about_point=ORIGIN).shift(at)


def cell_message(sequence, x=-2.72):
    return base_row(sequence, GREEN, width=0.43, gap=0.05, size=28, at=point(x, PORE_Y), stroke=0)


def hook_copy(dna):
    return cell_message(MESSAGE[:3], x=dna[:3].get_x())


def cell_world():
    """A fixed nucleus gap and a horizontal export route through its centre."""
    center = point(-2.72, PORE_Y)
    rx, ry, gap_angle = 3.13, 2.34, 0.22
    fill = Ellipse(width=2 * rx, height=2 * ry, fill_color=NUCLEUS,
                   fill_opacity=1, stroke_width=0).move_to(center).set_z_index(-9)
    outline = Arc(radius=1, start_angle=gap_angle, angle=TAU - 2 * gap_angle,
                  color=BLUE, stroke_width=3)
    outline.stretch(rx, 0, about_point=ORIGIN).stretch(ry, 1, about_point=ORIGIN).shift(center)
    lips = VGroup()
    for side in (-1, 1):
        y = PORE_Y + side * ry * np.sin(gap_angle)
        x = center[0] + rx * np.cos(gap_angle)
        lips.add(Line(point(x - 0.19, y), point(x + 0.29, y), color=TEAL, stroke_width=8))
    nucleus = VGroup(fill, outline, lips)
    dna = base_row(TEMPLATE, BLUE, width=0.40, gap=0.04, size=28, at=point(-2.72, 0.31), stroke=0)
    reader = ribosome(point(3.78, PORE_Y), scale=0.86, opened=True)
    return cell_field(), nucleus, dna, reader


def enzyme_clamp(width, top, bottom, x=0):
    rails = VGroup()
    for y, inward in ((top, DOWN), (bottom, UP)):
        left, right = point(x - width / 2, y), point(x + width / 2, y)
        rail = VMobject(color=TEAL, stroke_width=7)
        rail.set_points_as_corners([left + inward * 0.17, left, right, right + inward * 0.17])
        rails.add(rail)
    return rails


def gene_world(opened):
    """Selected DNA remains registered to the closed DNA on either flank."""
    field = cell_field(closeup=True, transcribing=True)
    upper = base_row(TEMPLATE.translate(DNA_COMPLEMENT), BLUE, at=point(0, 1.87 if opened else 1.09))
    template = base_row(TEMPLATE, BLUE, at=point(0, 0.40 if opened else 0.27))
    flanks = VGroup()
    for x in (-5.7, 5.7):
        for y in (1.09, 0.27):
            flanks.add(RoundedRectangle(width=1.75, height=0.48, corner_radius=0.13,
                                       color=BLUE, stroke_width=2, stroke_opacity=0.40,
                                       fill_color=BLUE, fill_opacity=0.12).move_to(point(x, y)))
    clamp = enzyme_clamp(9.1, 2.4 if opened else 1.62, -1.17)
    copy = base_row(MESSAGE, GREEN, at=point(0, -0.62))
    return field, flanks, upper, template, clamp, copy


def pairing_key():
    rows = VGroup(*(
        VGroup(M(letter, 30, BLUE), T("→", 30), M(letter.translate(DNA_TO_RNA), 30, GREEN))
        .arrange(RIGHT, buff=0.21)
        for letter in PAIRING_BASES
    )).arrange(DOWN, buff=0.27).move_to(point(4.50, 0.12))
    title = place_label(T("DNA → mRNA", 29), rows, dirs=(UP,), buff=0.30)
    return VGroup(title, rows)


def prediction():
    field = cell_field(closeup=True, transcribing=True)
    dna = base_row(TEMPLATE[:3], BLUE, width=1.32, gap=0.24, size=52, at=point(-1.31, 1.36))
    for block in dna:
        block.label.set_color(TEXT)
    slots = VGroup(*(base("", GREEN, 1.32, filled=False) for _ in range(3)))
    slots.arrange(RIGHT, buff=0.24).move_to(point(-1.31, -0.64))
    key = pairing_key()
    card = question_card(QUESTION, size=34, y=-2.84)
    panel = RoundedRectangle(width=8.1, height=0.78, corner_radius=0.19, stroke_width=0,
                             fill_color="#374F60", fill_opacity=1).move_to(card)
    question = VGroup(panel, card)
    key_panel = RoundedRectangle(width=3.18, height=3.28, corner_radius=0.20, stroke_width=0,
                                 fill_color="#394E5C", fill_opacity=1).move_to(key).set_z_index(-1)
    group_panel = RoundedRectangle(width=4.79, height=1.57, corner_radius=0.21,
                                   stroke_width=0, fill_color="#36574B", fill_opacity=1)
    group_panel.move_to(slots).set_z_index(-1)
    mark = T("?", 45, GOLD).move_to(point(slots[2].get_x(), 0.36))
    return field, dna, slots, key, question, mark, key_panel, group_panel


def translation_strip():
    groups = VGroup(*(base_row(codon, GREEN, width=0.72, gap=0.11, size=34)
                      for codon in CODONS)).arrange(RIGHT, buff=0.76).set_y(-0.63)
    dividers = VGroup()
    for left, right in zip(groups, groups[1:]):
        x = (left.get_right()[0] + right.get_left()[0]) / 2
        dividers.add(Line(point(x, -1.15), point(x, -0.26), color=TEXT, stroke_width=2.5))
    return groups, dividers


def amino_acid(name):
    disc = Circle(radius=0.45, stroke_color=RED, stroke_width=3.5,
                  fill_color=interpolate_color(ManimColor(BG), ManimColor(RED), 0.24), fill_opacity=1)
    return VGroup(disc, T(name, 28, RED).move_to(disc))


def chain_world(count=3, lifted=False):
    acids = VGroup(*(amino_acid(name).move_to(point(-3.0 + i * 1.19, 2.15 + 0.57 * lifted))
                     for i, name in enumerate(AMINO_ACIDS[:count])))
    joins = VGroup(*(chain_link(left, right) for left, right in zip(acids, acids[1:])))
    return VGroup(joins, acids)


def chain_link(left, right):
    return Line(left.get_right(), right.get_left(), color=RED, stroke_width=6)


def translation_world(index=0, *, opened=False, count=0, lifted=False):
    groups, dividers = translation_strip()
    rib = ribosome(groups[index].get_center(), opened=opened)
    return cell_field(closeup=True), groups, dividers, rib, chain_world(count, lifted)


def trna_for(codon, x, name):
    anticodon = base_row(codon.translate(RNA_COMPLEMENT), PURPLE, width=0.49, gap=0.34,
                         size=28, at=point(x, 0.24))
    key_head = RoundedRectangle(width=1.75, height=0.40, corner_radius=0.19,
                                stroke_color=PURPLE, stroke_width=3, fill_color=PURPLE,
                                fill_opacity=0.62).move_to(point(x, 0.92))
    stem = Line(point(x, 0.57), point(x, 1.16), color=PURPLE, stroke_width=10)
    return VGroup(stem, key_head, anticodon), amino_acid(name).move_to(point(x, 1.66))


def stop_label(codon):
    label = boxed_label("STOP", TEXT, size=35, min_size=35, pad=0.16, fill_opacity=0.12)
    return label.move_to(point(codon.get_x(), 0.30))


class S00Hook(SpokenScene):
    def construct(self):
        cell, nucleus, dna, rib = cell_world()
        self.add(cell)
        self.at("A plant or animal cell")
        self.play(FadeIn(nucleus), run_time=1.25)
        self.play(LaggedStart(*(FadeIn(b) for b in dna), lag_ratio=0.14), run_time=1.18)
        self.at("inside the nucleus")
        nucleus_label = T("nucleus", 33).move_to(point(-2.72, 1.31))
        dna_label = place_label(T("DNA", 30, BLUE), dna, avoid=(nucleus_label,),
                                dirs=(UP,), buff=0.21)
        self.play(FadeIn(nucleus_label), run_time=0.6)
        self.play(FadeIn(dna_label), run_time=0.55)
        self.at("How can their instructions", lead=0.42)
        route = DashedLine(point(-1.8, PORE_Y), point(3.68, PORE_Y),
                           dash_length=0.15, color=TEAL, stroke_width=4)
        self.play(Create(route), FadeIn(rib), run_time=1.25)
        self.at("reach a ribosome", lead=0.26)
        name = place_label(T("ribosome", 31, GOLD), rib, dirs=(UP,), buff=0.33)
        self.play(FadeIn(name), run_time=0.66)
        self.at("Watch the blue")
        stay = RoundedRectangle(width=dna.width, height=0.68, corner_radius=0.14,
                                stroke_color=BLUE, stroke_width=3, fill_color=BLUE, fill_opacity=0.45)
        stay.move_to(dna).set_z_index(-1)
        self.play(FadeIn(stay), *(block.label.animate.set_color(TEXT) for block in dna), run_time=1.32)
        self.at("a green copy")
        rna = hook_copy(dna)
        self.play(FadeOut(stay), LaggedStart(*(FadeIn(b, shift=DOWN * 0.12) for b in rna),
                                           lag_ratio=0.65),
                  *(block.label.animate.set_color(BLUE) for block in dna), run_time=1.85)
        self.finish()


class S01Title(TitleCard):
    LESSON = "From DNA to Protein"
    TITLE = "From Gene Copy to Protein Chain"

    def construct(self):
        cell, nucleus, dna, rib = cell_world()
        rna = hook_copy(dna)
        # Keep the faint cell diagram below the title band.
        nucleus.set_opacity(0.15)
        rib.set_opacity(0.16)
        dna.set_opacity(0.27)
        rna.set_opacity(0.27)
        title = fit_text(self.TITLE, max_w=11.5, size=50, min_size=36, font=TITLE_FONT)
        lesson = T(self.LESSON, 28, TEAL)
        card = VGroup(lesson, title).arrange(DOWN, buff=0.28).move_to(UP * 2.43)
        self.add(cell.set_fill(opacity=0.32).set_stroke(opacity=0), nucleus, dna, rib, rna)
        self.play(FadeIn(card), run_time=0.52)
        self.wait(0.94)
        self.play(FadeOut(card), run_time=0.51)


class S02Copy(SpokenScene):
    def construct(self):
        close_field, flanks, upper, template, clamp, copy = gene_world(opened=False)
        cell, nucleus, small_dna, _ = cell_world()
        self.add(cell, nucleus, small_dna)
        self.at("Making a protein")
        self.play(FadeOut(cell), FadeOut(nucleus), FadeIn(close_field), run_time=0.52)
        self.play(ReplacementTransform(small_dna, template), run_time=0.96)
        self.play(FadeIn(upper), FadeIn(flanks), run_time=0.52)
        heading = T("Protein synthesis", 35).move_to(UP * 2.87)
        self.at("protein synthesis")
        self.play(FadeIn(heading), run_time=0.72)
        self.at("The first stage")
        stage = T("Transcription", 35, TEAL).move_to(heading)
        self.play(swap(heading, stage), run_time=1.0)
        self.play(Create(clamp), run_time=1.45)
        self.at("An enzyme opens")
        _, _, opened_upper, opened_template, open_clamp, _ = gene_world(opened=True)
        self.play(Transform(upper, opened_upper), Transform(template, opened_template),
                  Transform(clamp, open_clamp), run_time=2.05)
        self.at("It uses the template strand")
        label = T("DNA template strand", 29, BLUE).move_to(point(0, -1.65))
        template_line = Line(template.get_left(), template.get_right(), color=BLUE, stroke_width=4)
        template_line.set_y(-0.10)
        self.play(Create(template_line), FadeIn(label), run_time=0.68)
        self.at("to build messenger")
        self.play(FadeOut(label), FadeOut(template_line),
                  LaggedStart(*(FadeIn(b, shift=DOWN * 0.12) for b in copy[:6]), lag_ratio=0.28),
                  run_time=2.05)
        self.play(FadeIn(T("Messenger RNA", 29, GREEN).move_to(label)), run_time=0.63)
        self.at("Only the selected gene")
        self.play(LaggedStart(*(FadeIn(b, shift=DOWN * 0.12) for b in copy[6:]), lag_ratio=0.25),
                  run_time=1.58)
        self.finish()


class S03Pair(SpokenScene):
    def construct(self):
        field, flanks, upper, template, clamp, copy = gene_world(opened=True)
        self.add(field, flanks, upper, template, clamp, copy)
        self.at("Each green")
        enlarged = base_row(TEMPLATE[4:8], BLUE, width=1.12, gap=0.18, size=45, at=point(-1.8, 1.22))
        frame = enzyme_clamp(6.18, 2.08, -1.57, x=-1.8)
        self.play(FadeOut(flanks), FadeOut(upper), FadeOut(copy), FadeOut(template[:4]),
                  FadeOut(template[8:]), FadeOut(clamp), run_time=0.73)
        self.play(ReplacementTransform(template[4:8], enlarged), run_time=1.25)
        self.play(FadeIn(frame), run_time=0.44)
        key = pairing_key()
        letters = VGroup()
        self.play(enlarged.animate.shift(RIGHT * 0.32), run_time=1.5)

        def show_pair(i):
            dna_base = enlarged[i]
            rna_base = base(PAIRING_BASES[i].translate(DNA_TO_RNA), GREEN, 1.12, 45)
            rna_base.move_to(point(dna_base.get_x(), -0.74))
            bond = DashedLine(dna_base.get_bottom() + DOWN * 0.08, rna_base.get_top() + UP * 0.08,
                              dash_length=0.15, color=GREY, stroke_width=4)
            self.play(FadeIn(rna_base, shift=DOWN * 0.28), Create(bond), run_time=0.64)
            letters.add(VGroup(rna_base, bond))
            key_parts = (key[0], key[1][i]) if i == 0 else (key[1][i],)
            self.play(*(FadeIn(part) for part in key_parts), run_time=0.40)

        self.at("letter appears with")
        show_pair(0)
        self.play(VGroup(enlarged, letters).animate.shift(LEFT * 0.22), run_time=0.75)
        self.at("T pairs with A")
        show_pair(1)
        self.play(VGroup(enlarged, letters).animate.shift(LEFT * 0.22), run_time=0.66)
        self.at("C pairs with G")
        show_pair(2)
        self.at("and G pairs with C")
        show_pair(3)
        self.at("uses U instead")
        note = caption("RNA uses U instead of T", color=GREEN, size=32)
        row = VGroup(*(pair[0] for pair in letters))
        emphasis = RoundedRectangle(width=row.width + 0.26, height=1.38, corner_radius=0.17,
                                    stroke_width=0, fill_color="#2C5041", fill_opacity=1)
        emphasis.move_to(row).set_z_index(-1)
        self.play(FadeIn(note), FadeIn(emphasis), letters[0][0][0].animate.set_stroke(width=5),
                  run_time=1.03)
        self.finish()


class S04Predict(SpokenScene):
    def construct(self):
        field, dna, slots, key, question, mark, key_panel, group_panel = prediction()
        self.add(field, key)
        self.at("Try the next template group")
        self.play(FadeIn(dna, shift=RIGHT * 0.39), run_time=1.45)
        self.at("The blue")
        self.play(LaggedStart(*(b[0].animate.set_fill(opacity=0.66) for b in dna), lag_ratio=0.29),
                  run_time=1.45)
        self.play(*(b[0].animate.set_fill(opacity=0.23) for b in dna), run_time=0.6)
        self.at("Which green messenger")
        self.play(LaggedStart(*(Create(b) for b in slots), lag_ratio=0.43), run_time=1.48)
        self.play(FadeIn(question), run_time=0.73)
        cursor = mark.copy().set_x(slots[0].get_x())
        self.play(FadeIn(cursor), run_time=0.55)
        self.at("Keep the pairing key")
        self.play(FadeIn(key_panel), run_time=0.69)
        self.at("choose the full group")
        self.play(cursor.animate.move_to(mark), run_time=1.31, rate_func=linear)
        self.play(FadeIn(group_panel, rate_func=linear), run_time=1.04)
        self.finish()


class S05Pause(NarratedScene):
    """Hold the exact question frame, including the final cursor position."""

    def construct(self):
        self.add(*prediction())
        self.wait(self.narration_s)


class S06Reveal(SpokenScene):
    def construct(self):
        field, dna, slots, key, question, mark, key_panel, group_panel = prediction()
        self.add(field, dna, slots, key, question, mark, key_panel, group_panel)
        answers = base_row(MESSAGE[:3], GREEN, width=1.32, gap=0.24, size=52, at=slots.get_center())
        self.at("T pairs with A")
        self.play(FadeOut(question), FadeOut(mark), FadeOut(group_panel), run_time=0.27)
        self.play(Transform(slots[0], answers[0][0]), FadeIn(answers[0][1], shift=UP * 0.2), run_time=1.2)
        self.at("A pairs with U")
        self.play(Transform(slots[1], answers[1][0]), FadeIn(answers[1][1], shift=UP * 0.2), run_time=1.2)
        self.at("C pairs with G")
        self.play(Transform(slots[2], answers[2][0]), FadeIn(answers[2][1], shift=UP * 0.2), run_time=1.2)
        self.at("The messenger group")
        result = VGroup(*(VGroup(slot, answer[1]) for slot, answer in zip(slots, answers)))
        group_line = Line(result.get_corner(DL) + DOWN * 0.20, result.get_corner(DR) + DOWN * 0.20,
                          color=GREEN, stroke_width=5)
        self.play(Create(group_line), run_time=0.85)
        _, flanks, upper, template, clamp, full = gene_world(opened=True)
        self.play(FadeOut(key), FadeOut(key_panel), FadeOut(group_line), ReplacementTransform(dna, VGroup(*template[:3])),
                  ReplacementTransform(result, VGroup(*full[:3])), run_time=0.95)
        self.play(FadeIn(flanks), FadeIn(upper), FadeIn(template[3:]), FadeIn(clamp),
                  LaggedStart(*(FadeIn(b, shift=DOWN * 0.13) for b in full[3:]), lag_ratio=0.15),
                  run_time=1.19)
        self.at("The enzyme releases")
        self.play(FadeOut(clamp, shift=RIGHT * 0.22), run_time=1.18)
        self.at("The green strand peels")
        self.play(LaggedStart(*(block.animate.set_y(RELEASED_RNA_Y) for block in reversed(full)),
                              lag_ratio=0.15), run_time=1.6)
        self.at("blue DNA closes")
        _, _, upper_closed, template_closed, _, _ = gene_world(opened=False)
        self.play(Transform(upper, upper_closed), Transform(template, template_closed), run_time=1.55)
        inside = T("DNA stays in the nucleus", 30, BLUE).move_to(point(0, 2.64))
        self.play(FadeIn(inside), run_time=0.78)
        self.finish()


class S07Translate(SpokenScene):
    def construct(self):
        cell, nucleus, dna, reader = cell_world()
        message = cell_message(MESSAGE)
        self.add(cell, nucleus, dna, reader, message)
        self.at("The messenger RNA")
        pore_label = T("Nuclear pore", 29, TEAL).move_to(point(1.39, 1.32))
        pointer = Arrow(point(1.39, 1.00), point(0.66, 0.12), buff=0, color=TEAL, stroke_width=3)
        self.play(FadeIn(pore_label), GrowArrow(pointer), run_time=0.66)
        self.at("passes through")
        self.play(message.animate.set_x(3.43), run_time=1.65, rate_func=linear)
        self.at("into the cytoplasm")
        cytoplasm = T("Cytoplasm", 29).move_to(point(3.55, -2.26))
        self.play(FadeIn(cytoplasm), run_time=0.73)
        self.at("Translation begins")
        field, groups, dividers, rib, _ = translation_world(opened=True)
        big_strip = VGroup(*(letter for group in groups for letter in group))
        self.play(FadeOut(cell), FadeOut(nucleus), FadeOut(dna), FadeOut(pore_label), FadeOut(pointer), FadeOut(cytoplasm),
                  FadeOut(reader), FadeIn(field), run_time=0.42)
        self.play(ReplacementTransform(message, big_strip), run_time=0.87)
        self.play(FadeIn(rib), run_time=0.44)
        title = T("Translation", 35).move_to(UP * 2.52)
        self.play(FadeIn(title), run_time=0.57)
        self.at("grips the message")
        shut = ribosome(groups[0].get_center())
        self.play(Transform(rib, shut), run_time=1.18)
        self.at("It reads each codon")
        self.play(LaggedStart(*(Create(d) for d in dividers), lag_ratio=0.35), run_time=0.61)
        for i in (1, 2):
            self.play(rib.animate.shift(RIGHT * (groups[i].get_x() - groups[i - 1].get_x())), run_time=0.83)
        self.at("A codon is")
        label = T("Codon = 3 letters", 35).move_to(title)
        self.play(swap(title, label), run_time=0.65)
        underline = Line(groups[2].get_left(), groups[2].get_right(), color=GREEN, stroke_width=5)
        underline.set_y(-1.06)
        self.play(Create(underline), run_time=0.69)
        self.at("means an amino")
        meaning = T("Amino acid or stop", 30).move_to(UP * 1.71)
        self.play(FadeIn(meaning), run_time=0.83)
        self.at("or stop")
        self.play(rib.animate.shift(RIGHT * (groups[3].get_x() - groups[2].get_x())),
                  FadeOut(underline), run_time=0.91)
        self.finish()


class S08Chain(SpokenScene):
    def construct(self):
        field, groups, dividers, rib, _ = translation_world(index=3)
        self.add(field, groups, dividers, rib)
        self.at("Purple transfer RNA")
        self.play(FadeOut(rib), run_time=0.32)
        rib = ribosome(groups[0].get_center())
        self.play(FadeIn(rib), run_time=0.33)
        carriers = [trna_for(codon, groups[i].get_x(), AMINO_ACIDS[i]) for i, codon in enumerate(CODONS[:3])]
        trna, cargo = carriers[0]
        parcel = VGroup(trna, cargo).shift(UP * 0.79 + RIGHT * 2.76)
        self.play(FadeIn(parcel, shift=DOWN * 0.38), run_time=0.49)
        name = T("Transfer RNA", 29, PURPLE).move_to(point(0.37, 2.51))
        self.play(FadeIn(name), run_time=0.30)
        self.at("brings the amino")
        self.play(parcel.animate.shift(LEFT * 2.76), run_time=3.08)
        self.at("Its anticodon")
        self.play(FadeOut(name), run_time=0.35)
        self.play(parcel.animate.shift(DOWN * 0.79), run_time=1.66)
        anticodon = trna[2]
        anti = T("Anticodon", 29, PURPLE).next_to(rib[1][1], RIGHT, buff=0.26).set_y(anticodon.get_y())
        alignment = RoundedRectangle(width=2.65, height=1.65, corner_radius=0.15,
                                     stroke_width=2.5, stroke_color=PURPLE, fill_color="#141E37",
                                     fill_opacity=1).move_to(point(groups[0].get_x(), -0.25))
        alignment.set_z_index(-3)
        self.play(FadeIn(alignment), FadeIn(anti), run_time=0.98)
        self.at("The ribosome joins")
        self.play(FadeOut(anti), FadeOut(alignment), run_time=0.31)
        chain = chain_world()
        joins, acids = chain
        self.play(cargo.animate.move_to(acids[0]), FadeOut(trna, shift=UP * 0.35), run_time=1.20)
        for i in (1, 2):
            trna, incoming = carriers[i]
            self.play(rib.animate.shift(RIGHT * (groups[i].get_x() - groups[i - 1].get_x())), run_time=0.36)
            self.play(FadeIn(VGroup(trna, incoming), shift=DOWN * 0.55), run_time=0.45)
            self.play(incoming.animate.move_to(acids[i]), Create(joins[i - 1]),
                      FadeOut(trna, shift=UP * 0.35), run_time=0.80)
        self.at("At a stop codon")
        self.play(rib.animate.shift(RIGHT * (groups[3].get_x() - groups[2].get_x())), run_time=0.72)
        stop = stop_label(groups[3])
        self.play(FadeIn(stop), run_time=0.57)
        self.at("no amino acid")
        self.play(Transform(rib, ribosome(groups[3].get_center(), opened=True)), run_time=1.0)
        self.at("the chain is released")
        # The delivered discs are already in the canonical chain positions.
        self.play(VGroup(cargo, carriers[1][1], carriers[2][1], joins).animate.shift(UP * 0.57), run_time=1.0)
        self.finish()


class S09StartStop(SpokenScene):
    def construct(self):
        field, groups, dividers, rib, chain = translation_world(index=3, opened=True, count=3, lifted=True)
        stop = stop_label(groups[3])
        self.add(field, groups, dividers, rib, chain, stop)
        self.at("Reading usually begins")
        self.play(FadeOut(chain), FadeOut(stop), FadeOut(dividers), FadeOut(rib), run_time=0.57)
        start_codon = groups[0]
        start_codon.save_state()
        rib = ribosome(start_codon.get_center())
        self.play(FadeIn(rib), run_time=0.78)
        start = T("START", 32, GREEN).move_to(point(start_codon.get_x(), 0.39))
        self.at("start codon")
        self.play(FadeIn(start), run_time=0.66)
        marker = Line(start_codon.get_left(), start_codon.get_right(), color=GREEN, stroke_width=5)
        marker.set_y(-1.08)
        self.play(Create(marker), *(block.box.animate.set_fill(opacity=0.70) for block in start_codon),
                  *(block.label.animate.set_color(TEXT) for block in start_codon), run_time=0.68)
        self.at("It adds methionine")
        met = amino_acid("Met").move_to(point(groups[0].get_x(), 1.64))
        name = T("Methionine", 30, RED).move_to(point(groups[0].get_x(), 2.57))
        self.play(FadeIn(met, shift=UP * 0.24), run_time=0.77)
        self.play(FadeIn(name), run_time=0.56)
        self.at("fixes the grouping")
        bands = VGroup(*(RoundedRectangle(width=g.width + 0.27, height=1.11, corner_radius=0.14,
                                          stroke_width=0, fill_color="#192C28", fill_opacity=1)
                         .move_to(g).set_z_index(-3) for g in groups))
        self.play(LaggedStart(*(FadeIn(b) for b in bands), lag_ratio=0.36),
                  LaggedStart(*(Create(d) for d in dividers), lag_ratio=0.54), run_time=1.87)
        self.at("ribosome then moves")
        joins, acids = chain_world()
        self.play(FadeOut(start), FadeOut(marker), FadeOut(name), start_codon.animate.restore(),
                  met.animate.move_to(acids[0]), run_time=0.47)
        for i in (1, 2, 3):
            animations = [rib.animate.shift(RIGHT * (groups[i].get_x() - groups[i - 1].get_x()))]
            if i < 3:
                animations.extend((FadeIn(acids[i], shift=UP * 0.29), Create(joins[i - 1])))
            self.play(*animations, run_time=0.83)
        self.at("At UGA")
        self.play(FadeIn(stop), FadeOut(bands), run_time=0.86)
        self.at("stop sign appears")
        self.play(stop[0].animate.set_stroke(width=4.5), run_time=0.74)
        self.at("reading window opens")
        self.play(Transform(rib, ribosome(groups[3].get_center(), opened=True)), run_time=0.87)
        self.at("finished chain floats free")
        self.play(VGroup(met, acids[1:], joins).animate.shift(UP * 0.57), run_time=1.25)
        self.finish()


def folded_protein(at):
    blob = VMobject(stroke_color=RED, stroke_width=4,
                    fill_color=interpolate_color(ManimColor(CYTOPLASM), ManimColor(RED), 0.28), fill_opacity=1)
    blob.set_points_smoothly([
        point(-1.14, 0.18), point(-0.66, 0.66), point(-0.25, 0.62),
        point(0.35, 0.83), point(0.99, 0.42), point(1.14, -0.17),
        point(0.66, -0.63), point(0.03, -0.53), point(-0.61, -0.70),
        point(-1.08, -0.39), point(-1.14, 0.18),
    ])
    return blob.move_to(at)


class S10Rule(SpokenScene):
    def construct(self):
        field, groups, dividers, rib, chain = translation_world(index=3, opened=True, count=3, lifted=True)
        stop = stop_label(groups[3])
        stop[0].set_stroke(width=4.5)
        self.add(field, groups, dividers, rib, chain, stop)
        self.at("The release chain")
        self.play(FadeOut(groups), FadeOut(dividers), FadeOut(rib), FadeOut(stop),
                  chain.animate.move_to(point(0, 0.77)), run_time=1.27)
        self.at("fold into a working protein")
        blob = folded_protein(point(0, 0.73)).scale(1.40)
        met, leu, ala = chain[1]
        self.play(FadeOut(chain[0]), ala.animate.move_to(point(1.19, -0.44)), run_time=0.53)
        self.play(met.animate.move_to(point(-0.63, 1.18)), leu.animate.move_to(point(0.48, 1.20)),
                  ala.animate.move_to(point(0.02, 0.12)), run_time=0.71)
        self.play(swap(chain[1], blob), run_time=0.56)
        protein = place_label(T("Protein", 31, RED), blob, dirs=(UP,), buff=0.32)
        self.play(FadeIn(protein), run_time=0.70)
        self.at("message changed form")
        cell, nucleus, dna, _ = cell_world()
        cell_protein = folded_protein(point(4.44, 0.80))
        self.play(FadeOut(field), FadeIn(cell), FadeIn(nucleus), FadeIn(dna), FadeOut(protein),
                  Transform(blob, cell_protein), run_time=1.51)
        self.at("order guided every handoff")
        messenger = cell_message(MESSAGE)
        self.play(LaggedStart(*(FadeIn(b, shift=DOWN * 0.08) for b in messenger), lag_ratio=0.14),
                  run_time=1.58)
        self.at("protein -coding genes")
        dna_label = T("DNA order", 32, BLUE).move_to(point(-2.74, 1.45))
        rna_label = T("mRNA codons", 31, GREEN).move_to(point(-2.72, -1.35))
        protein_label = T("Amino acid order", 31, RED).move_to(point(3.05, 2.03))
        self.play(FadeIn(dna_label), run_time=0.74)
        self.at("DN order")
        self.play(LaggedStart(*(b[0].animate.set_fill(opacity=0.44) for b in dna), lag_ratio=0.09),
                  run_time=0.41)
        self.at("sets mRNA codons")
        self.play(FadeIn(rna_label), run_time=0.60)
        underlines = VGroup()
        for i in range(0, len(MESSAGE), 3):
            group = messenger[i:i + 3]
            seg = Line(group.get_left(), group.get_right(), color=GREEN, stroke_width=4)
            seg.set_y(-0.79)
            underlines.add(seg)
        self.play(LaggedStart(*(Create(line) for line in underlines), lag_ratio=0.41), run_time=1.32)
        self.at("amino acid order")
        compact_chain = chain_world().move_to(point(4.42, 0.80))
        self.play(FadeIn(protein_label), run_time=0.60)
        self.play(swap(blob, compact_chain), run_time=0.77)
        self.at("That is how instructions")
        self.play(FadeOut(rna_label), run_time=0.35)
        self.play(VGroup(messenger, underlines).animate.shift(RIGHT * 5.84), run_time=2.18,
                  rate_func=linear)
        self.at("reach a protein")
        through = DashedLine(point(-2.64, PORE_Y), point(0.14, PORE_Y), color=TEAL,
                             dash_length=0.15, stroke_width=4)
        handoff = Arrow(point(2.20, -0.09), point(3.24, 0.47), buff=0,
                        color=TEAL, stroke_width=3, max_tip_length_to_length_ratio=0.19)
        final_label = T("Protein", 31, RED).move_to(point(4.44, 1.92))
        self.play(Create(through), swap(compact_chain, blob), swap(protein_label, final_label), run_time=0.88)
        self.play(GrowArrow(handoff), run_time=0.62)
        self.finish()


class S11End(EndCard):
    LINE = "In protein-coding genes, DNA order sets mRNA codons and amino acid order."
