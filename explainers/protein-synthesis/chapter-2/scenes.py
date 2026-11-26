"""When the Reading Changes, chapter 2 of From DNA to Protein.

COLOR MAP from Chapter 1
  BLUE   DNA
  GREEN  messenger RNA
  GOLD   ribosome and reading window
  PURPLE transfer RNA (not pictured in this chapter)
  RED    amino acids, hemoglobin and the red blood cell
  TEAL   transcription enzyme and pore (not pictured in this chapter)
  GREY   cell structure and neutral guides
  TEXT   neutral labels and STOP
"""
from bp_parts import *  # noqa: F401,F403
from bp_style import EndCard

PURPLE = "#B58CD9"
LESSON_TITLE = "From DNA to Protein"
CHAPTER_TITLE = "When the Reading Changes"


def letter_block(letter, color, width=0.72, size=34, height=None):
    """Chapter 1's rounded information block, with its own centered character."""
    block = RoundedRectangle(
        corner_radius=0.09, width=width, height=height or width,
        stroke_color=color, stroke_width=3, fill_color=color, fill_opacity=0.27,
    )
    return VGroup(block, M(letter, size, color).move_to(block)) if letter else VGroup(block)


def letter_row(letters, color, at, width=0.72, size=34, gap=0.1):
    return VGroup(*[letter_block(c, color, width, size) for c in letters]).arrange(RIGHT, buff=gap).move_to(at)


def field():
    return Ellipse(width=12.7, height=6.55, stroke_opacity=0, fill_color=BLUE,
                   fill_opacity=0.24).shift(DOWN * 0.12).set_z_index(-5)


def amino_acid(name, at, radius=0.52):
    bead = Circle(radius=radius, stroke_color=RED, stroke_width=4, fill_color=RED, fill_opacity=0.34)
    bead.move_to(at)
    return VGroup(bead, T(name, 28, TEXT).move_to(bead))


def chain_links(beads):
    return VGroup(*[
        Line(a.get_right(), b.get_left(), stroke_width=5, color=RED)
        for a, b in zip(beads, list(beads)[1:])
    ])


def reading_window(x, y, width, half_height, lobe_height=0.66):
    """The two gold lobes of Chapter 1's ribosome, clear of the letters."""
    top = ArcBetweenPoints([x - width / 2, y + half_height, 0],
                           [x + width / 2, y + half_height, 0], angle=-PI)
    bottom = ArcBetweenPoints([x - width * 0.44, y - half_height, 0],
                              [x + width * 0.44, y - half_height, 0], angle=PI)
    top.stretch(lobe_height / (width / 2), 1, about_point=[x, y + half_height, 0])
    bottom.stretch(lobe_height * 0.80 / (width * 0.44), 1, about_point=[x, y - half_height, 0])
    for lobe in (top, bottom):
        lobe.set_stroke(GOLD, 6).set_fill(GOLD, 0.47)
    return VGroup(top, bottom)


def focus(target, color=GOLD, buff=0.12):
    return SurroundingRectangle(target, color=color, buff=buff, corner_radius=0.12, stroke_width=4)


def base_marks(target, color):
    """Accent a close-packed block without touching its neighbors."""
    return VGroup(*[
        Line([-0.27, 0, 0], [0.27, 0, 0], color=color, stroke_width=5)
        .move_to(target.get_center() + offset * 0.43 * UP)
        for offset in (-1, 1)
    ])


def path_world():
    """Chapter 1's template, transcript and chain, anchored for the hook and recap."""
    dna = letter_row("TACCGATTTAAA", BLUE, [-1.60, 2.23, 0], width=0.58, size=29, gap=0.13)
    rna = letter_row("AUGGCUAAAUUU", GREEN, [-1.60, 0.16, 0], width=0.58, size=29, gap=0.13)
    beads = VGroup(*[
        amino_acid(name, [-4.1 + 1.55 * i, -2.13, 0])
        for i, name in enumerate(("Met", "Ala", "Lys", "Phe"))
    ])
    labels = VGroup(
        T("DNA template", 28, BLUE).move_to([-4.03, 2.98, 0]),
        T("messenger RNA", 28, GREEN).move_to([-4.03, 0.91, 0]),
        T("amino acid chain", 28, RED).move_to([-2.03, -3.05, 0]),
    )
    arrows = VGroup(*[
        Arrow([-1.6, top, 0], [-1.6, bottom, 0], buff=0, color=GREY, stroke_width=4)
        for top, bottom in ((1.75, 0.72), (-0.39, -1.38))
    ])
    return dna, rna, beads, chain_links(beads), labels, arrows


def overview_window(rna, codon=0):
    return reading_window(rna[3 * codon + 1].get_x(), rna.get_y(), 2.03, 0.40)


class S00Hook(SpokenScene, TitleCard):
    TITLE = CHAPTER_TITLE
    LESSON = LESSON_TITLE

    def construct(self):
        dna, rna, beads, links, labels, arrows = path_world()
        title = T(self.TITLE, 36, font=TITLE_FONT).move_to([0.7, 3.47, 0])
        self.add(field(), title)
        self.at("the first film")
        self.play(FadeIn(dna), run_time=0.95)
        self.at("followed blue")
        self.play(FadeIn(labels[0]), run_time=0.50)
        self.at("into green messenger")
        self.play(GrowArrow(arrows[0]), FadeIn(rna), run_time=0.85)
        self.at("messenger RNA")
        self.play(FadeIn(labels[1]), run_time=0.55)
        self.at("a red amino acid")
        self.play(GrowArrow(arrows[1]), run_time=0.65)
        self.play(LaggedStart(*[FadeIn(b) for b in beads], lag_ratio=0.40), Create(links), run_time=1.1)
        self.play(FadeIn(labels[2]), run_time=0.45)

        selected = base_marks(dna[4], BLUE)
        self.at("if a DNA letter")
        self.play(FadeOut(title), Create(selected), run_time=0.65)
        self.play(dna[4].animate.shift(UP * 0.08), selected.animate.shift(UP * 0.08), run_time=0.65)
        self.at("how much of that")
        question = question_card("How much of the chain changes?", y=-3.07, size=34)
        self.play(FadeOut(labels[2]), run_time=0.25)
        self.play(FadeIn(question), run_time=0.85)

        window = overview_window(rna)
        self.at("keep watching the same")
        self.play(FadeOut(labels[1]), run_time=0.23)
        self.play(FadeIn(window), run_time=0.42)
        self.play(window.animate.shift(RIGHT * (rna[4].get_x() - rna[1].get_x())),
                  run_time=1.9, rate_func=smooth)
        self.finish()


class S01Title(TitleCard):
    TITLE = CHAPTER_TITLE
    LESSON = LESSON_TITLE

    def construct(self):
        dna, _, _, _, _, _ = path_world()
        dna[4].shift(UP * 0.08)
        row = VGroup(dna, base_marks(dna[4], BLUE))
        lesson = T(self.LESSON.upper(), 28, TEAL, weight=BOLD)
        title = T(self.TITLE, 54, font=TITLE_FONT)
        rule = Line(LEFT * 1.4, RIGHT * 1.4, color=GOLD, stroke_width=4)
        card = VGroup(lesson, title, rule).arrange(DOWN, buff=0.33).shift(DOWN * 0.47)
        self.add(field(), row)
        self.play(FadeIn(card), run_time=0.45)
        self.wait(0.70)
        self.play(FadeOut(card), row.animate.shift(RIGHT * 1.6).scale(1.12), run_time=0.7)
        self.finish()


CODON_WIDTH = 1.02
DNA_Y, RNA_Y, PROTEIN_Y = 2.05, 0.0, -2.22


def single_codon(letters, color, y):
    return letter_row(letters, color, [0, y, 0], width=CODON_WIDTH, size=43, gap=0.32)


def codon_window():
    return reading_window(0, RNA_Y, 3.72, 0.67, lobe_height=0.48)


def stop_sign(at):
    face = RegularPolygon(n=8, radius=0.67, start_angle=PI / 8, color=TEXT,
                          stroke_width=4, fill_color=BG, fill_opacity=0.95)
    face.move_to(at)
    return VGroup(face, T("STOP", 28, TEXT, weight=BOLD).move_to(face))


def swap_base(scene, block, new_letter, color, size, direction=UP):
    """Exchange a base at its fixed position, leaving the other positions intact."""
    new = letter_block(new_letter, color, block.width, size, height=block.height).move_to(block)
    scene.play(FadeOut(block, shift=direction * 0.42), run_time=0.30)
    scene.play(FadeIn(new, shift=direction * 0.65), run_time=0.55)
    return new


class S02Substitution(SpokenScene):
    def construct(self):
        dna = single_codon("GAG", BLUE, DNA_Y)
        rna = single_codon("GAG", GREEN, RNA_Y)
        dna_label = place_label(T("coding DNA", 30, BLUE), dna, dirs=(LEFT,), buff=0.65)
        rna_label = place_label(T("mRNA", 30, GREEN), rna, dirs=(LEFT,), buff=0.65)
        window = codon_window()
        glu = amino_acid("Glu", [0, PROTEIN_Y, 0], radius=0.63)
        self.add(field())
        self.at("a mutation is")
        self.play(LaggedStart(*[FadeIn(b) for b in dna], lag_ratio=0.50), run_time=1.0)
        self.at("base order")
        self.play(FadeIn(dna_label), run_time=0.50)
        self.play(FadeIn(rna), run_time=0.55)
        self.play(FadeIn(rna_label), run_time=0.45)

        self.at("a substitution swaps")
        last_dna = swap_base(self, dna[2], "A", BLUE, 43)
        last_rna = swap_base(self, rna[2], "A", GREEN, 43, direction=DOWN)
        self.at("because several codons")
        self.play(FadeIn(window), run_time=0.65)
        same = boxed_label("SAME", RED, 30).move_to([3.8, PROTEIN_Y, 0])
        self.at("the same amino acid")
        self.play(FadeIn(glu), FadeIn(same), run_time=0.65)
        self.at("unchanged", lead=-0.52)
        self.play(FadeOut(same), FadeOut(glu), FadeOut(window), run_time=0.35)
        self.play(swap(last_dna, dna[2]), swap(last_rna, rna[2]), run_time=0.55)

        self.at("another swap can", lead=0.35)
        middle_dna = letter_block("T", BLUE, CODON_WIDTH, 43).move_to(dna[1])
        middle_rna = letter_block("U", GREEN, CODON_WIDTH, 43).move_to(rna[1])
        self.play(swap(dna[1], middle_dna), swap(rna[1], middle_rna), run_time=0.58)
        changed = boxed_label("CHANGED", RED, 30).move_to([3.8, PROTEIN_Y, 0])
        val = amino_acid("Val", [0, PROTEIN_Y, 0], radius=0.63)
        self.play(FadeIn(window), FadeIn(val), FadeIn(changed), run_time=0.34)
        self.at("or create an early stop", lead=0)
        self.play(FadeOut(changed), FadeOut(val), FadeOut(window),
                  swap(middle_dna, dna[1]), swap(middle_rna, rna[1]), run_time=0.34)
        first_dna = letter_block("T", BLUE, CODON_WIDTH, 43).move_to(dna[0])
        first_rna = letter_block("U", GREEN, CODON_WIDTH, 43).move_to(rna[0])
        self.play(swap(dna[0], first_dna), swap(rna[0], first_rna), run_time=0.34)
        self.play(FadeIn(window), FadeIn(stop_sign([0, PROTEIN_Y, 0])), run_time=0.30)
        self.finish()


# One base inserted after the G in GGU gives AUG GAG UUU UAG CUG A.
# UUU still means Phe. UAG terminates before the original UGA.
MESSAGE = "AUGGGUUUUAGCUGA"
INSERT_AT = 4
INSERTED = "A"
STEP = 0.73
STRIP_Y = 0.02
STRIP_LEFT = -5.45
STRIP_BLOCK = 0.57
STRIP_HEIGHT = 0.91


def base_x(index):
    return STRIP_LEFT + index * STEP


def message_blocks():
    return VGroup(*[
        letter_block(base, GREEN, STRIP_BLOCK, 34, height=STRIP_HEIGHT).move_to([base_x(i), STRIP_Y, 0])
        for i, base in enumerate(MESSAGE)
    ])


def waiting_block(letter=""):
    return letter_block(letter, GREEN, STRIP_BLOCK, 34, height=STRIP_HEIGHT).move_to([base_x(INSERT_AT), 1.69, 0])


def divider(x):
    return VGroup(*[
        Line([x, STRIP_Y + side * 0.59, 0], [x, STRIP_Y + side * 1.01, 0],
             color=TEXT, stroke_width=4)
        for side in (1, -1)
    ])


def dividers(offset=0):
    return VGroup(*[divider(base_x(i - 0.5 + (offset if i > INSERT_AT else 0)))
                    for i in range(3, len(MESSAGE) + 1, 3)])


def strip_window(codon=0):
    return reading_window(base_x(codon * 3 + 1), STRIP_Y, 1.92, 0.67)


def inserted_strip():
    row = message_blocks()
    VGroup(*row[INSERT_AT:]).shift(RIGHT * STEP)
    base = waiting_block(INSERTED).set_y(STRIP_Y)
    row.insert(INSERT_AT, base)
    return row


def mark_divider(index, offset=1):
    x = base_x(index - 0.5 + offset)
    return Polygon(
        [x, -1.10, 0], [x + 0.73, -1.83, 0], [x + 0.36, -1.83, 0],
        [x + 0.36, -2.49, 0], [x - 0.36, -2.49, 0], [x - 0.36, -1.83, 0],
        [x - 0.73, -1.83, 0], color=GOLD, stroke_width=2, fill_color=GOLD, fill_opacity=1,
    )


def prediction():
    card = question_card("What changes after one inserted base?", ("ONE CODON", "LATER CODONS TOO"),
                         y=-3.03, size=34, chip_size=30)
    card.chips.set_y(2.04)
    return card


class S03InsertDelete(SpokenScene):
    def construct(self):
        row, lines, window = message_blocks(), dividers(), strip_window()
        waiting = waiting_block()
        suffix = VGroup(*row[INSERT_AT:])
        addition = T("insertion", 34, GREEN).move_to([0, 2.73, 0])
        deletion = T("deletion", 34, GREEN).move_to(addition)
        self.add(field(), row)
        self.at("an insertion adds")
        self.play(FadeIn(waiting), suffix.animate.shift(RIGHT * STEP), run_time=0.70)
        self.play(FadeIn(addition), waiting.animate.set_y(STRIP_Y), run_time=0.85)
        self.at("a deletion removes")
        self.play(FadeOut(waiting, shift=UP * 0.5), swap(addition, deletion), run_time=0.63)
        self.play(suffix.animate.shift(LEFT * STEP), run_time=0.68)
        self.at("the ribosome does")
        self.play(FadeOut(deletion), FadeIn(window), run_time=0.85)
        self.at("see spaces between")
        self.play(window.animate.shift(RIGHT * 3 * STEP), run_time=1.45)
        self.at("its reading point")
        self.play(window.animate.shift(LEFT * 3 * STEP), run_time=0.8)
        self.at("groups the message")
        self.play(LaggedStart(*[Create(line) for line in lines], lag_ratio=0.70), run_time=1.75)
        self.at("or removing one base")
        departing = row[5]
        remaining = VGroup(*row[6:])
        tracking_lines = VGroup(*lines[1:-1])
        self.play(departing.animate.shift(UP * 1.66), run_time=0.75)
        self.play(remaining.animate.shift(LEFT * STEP), FadeOut(departing), FadeOut(lines[-1]),
                  tracking_lines.animate.shift(LEFT * STEP), run_time=0.75)
        self.at("shifts that grouping")
        self.play(tracking_lines.animate.shift(RIGHT * STEP), run_time=1.15)
        self.at("this is called", lead=0.60)
        term = T("frameshift", 39, GOLD).move_to([0, 2.73, 0])
        self.play(FadeIn(term), run_time=0.35)
        self.at("frame shift", lead=-0.44)
        departing.set_y(STRIP_Y)
        self.play(FadeOut(term), remaining.animate.shift(RIGHT * STEP), FadeIn(waiting_block()), run_time=0.45)
        self.play(FadeIn(departing), FadeIn(lines[-1]), run_time=0.34)
        self.finish()


class S04Predict(SpokenScene):
    def construct(self):
        row, waiting = message_blocks(), waiting_block()
        lines, window = dividers(), strip_window()
        self.add(field(), row, waiting, lines, window)
        self.at("block enters near")
        tracking_lines = VGroup(*lines[1:])
        self.play(VGroup(*row[INSERT_AT:]).animate.shift(RIGHT * STEP),
                  tracking_lines.animate.shift(RIGHT * STEP), run_time=0.72)
        self.play(waiting.animate.set_y(STRIP_Y), run_time=0.71)
        letter = waiting_block(INSERTED).set_y(STRIP_Y)[1]
        self.play(FadeIn(letter), run_time=0.36)
        card = prediction()
        self.at("will only its codon")
        self.play(FadeIn(card.question), FadeIn(card.chips[0]), run_time=0.80)
        self.at("will later codons")
        self.play(FadeIn(card.chips[1]), run_time=0.80)
        self.at("follow the dividers")
        pointer = mark_divider(6)
        self.play(GrowFromEdge(pointer, DOWN), run_time=0.49)
        self.play(pointer.animate.shift(RIGHT * 6 * STEP), run_time=2.46, rate_func=linear)
        self.finish()


class S05Pause(NarratedScene):
    def construct(self):
        self.add(field(), inserted_strip(), dividers(1), strip_window(), prediction(), mark_divider(12))
        self.wait(self.narration_s)


FRAME_NAMES = ("Met", "Gly", "Phe", "Ser")
def frame_bead(name, i):
    return amino_acid(name, [base_x(3 * i + 1), -2.12, 0])


def strip_stop(codon, y=2.15):
    return stop_sign([base_x(3 * codon + 1), y, 0])


class S06Reveal(SpokenScene):
    def construct(self):
        row, lines, window = inserted_strip(), dividers(1), strip_window()
        question, pointer = prediction(), mark_divider(12)
        self.add(field(), row, lines, window, question, pointer)
        self.at("the inserted block")
        self.play(FadeOut(question), FadeOut(pointer), run_time=0.25)
        self.at("shifts every divider")
        self.play(LaggedStart(*[ln.animate.shift(LEFT * STEP) for ln in lines[1:]], lag_ratio=0.43),
                  run_time=1.75)
        self.at("the gold ribosome")
        beads = VGroup(*[frame_bead(name, i) for i, name in enumerate(FRAME_NAMES)])
        links = chain_links(beads)
        before = T("previous chain", 28, RED).move_to([-2.5, -3.05, 0])
        self.play(FadeIn(beads), Create(links), run_time=0.85)
        self.play(FadeIn(before), run_time=0.45)
        self.at("reads new codons")
        self.play(window.animate.shift(RIGHT * 3 * STEP), run_time=2.3, rate_func=smooth)
        self.at("many later amino acids")
        glu = frame_bead("Glu", 1)
        self.play(swap(beads[1], glu), FadeOut(before), run_time=0.65)
        self.play(window.animate.shift(RIGHT * 3 * STEP), run_time=0.64)
        unchanged = focus(beads[2], RED)
        self.play(Create(unchanged), run_time=0.42)
        self.at("an early stop")
        self.play(FadeOut(unchanged), FadeOut(beads[3]), FadeOut(links[2]),
                  window.animate.shift(RIGHT * 3 * STEP), run_time=0.65)
        stop = strip_stop(3)
        self.play(FadeIn(stop), run_time=0.65)
        self.at("removing a base")
        # Compare a deletion on the same strip. Return to the early-stop case on the final frame.
        removed, suffix = row[5], VGroup(*row[6:])
        chain = VGroup(beads[0], glu, beads[2], *links[:2])
        self.play(FadeOut(stop), FadeOut(chain), FadeOut(window),
                  removed.animate.shift(UP * 1.66), run_time=0.52)
        # The reading frame starts at AUG, so the guides stay fixed as the suffix fills the gap.
        self.play(FadeOut(removed), suffix.animate.shift(LEFT * STEP), run_time=0.62)
        self.at("in the same way", lead=-0.68)
        removed.set_y(STRIP_Y)
        self.play(suffix.animate.shift(RIGHT * STEP), run_time=0.42)
        self.play(FadeIn(removed), FadeIn(window), FadeIn(stop), FadeIn(chain), run_time=0.32)
        self.finish()


class S07SilentExample(SpokenScene):
    def construct(self):
        rna = single_codon("GAG", GREEN, RNA_Y)
        window = codon_window()
        glu = amino_acid("Glu", [0, PROTEIN_Y, 0], radius=0.63)
        full_name = place_label(T("glutamic acid", 30, RED), glu, dirs=(RIGHT,), buff=0.43)
        self.add(field())
        self.at("now compare a quieter")
        self.play(FadeIn(rna), run_time=0.85)
        self.play(FadeIn(window), run_time=0.80)
        self.at("messenger codon")
        self.play(FadeIn(glu), run_time=0.90)
        self.at("means glutamic acid")
        self.play(FadeIn(full_name), run_time=0.65)
        x = 3.15
        self.play(FadeOut(full_name), VGroup(rna, window, glu).animate.shift(LEFT * x), run_time=1.12)
        right_rna = single_codon("GAG", GREEN, RNA_Y).shift(RIGHT * x)
        before = T("Before", 31, TEXT).move_to([-x, 3.02, 0])
        after = T("After", 31, TEXT).move_to([x, 3.02, 0])
        self.at("change its last letter")
        self.play(FadeIn(before), FadeIn(after), FadeIn(right_rna), run_time=0.90)
        swap_base(self, right_rna[2], "A", GREEN, 43, direction=UP)
        self.at("it still means")
        right_window = codon_window().shift(RIGHT * x)
        right_glu = amino_acid("Glu", [x, PROTEIN_Y, 0], radius=0.63)
        self.play(FadeIn(right_window), run_time=0.65)
        self.play(FadeIn(right_glu), run_time=0.96)
        self.at("the DNA changed")
        old_dna = single_codon("GAG", BLUE, DNA_Y).shift(LEFT * x)
        new_dna = single_codon("GAA", BLUE, DNA_Y).shift(RIGHT * x)
        self.play(FadeIn(old_dna), FadeIn(new_dna), run_time=0.75)
        self.play(Create(focus(new_dna[2])), run_time=0.66)
        self.at("this amino acid chain")
        same = caption("SAME CHAIN", 31, color=RED, y=-3.23).set_x(0)
        same_mark = T("=", 74, RED).move_to([0, PROTEIN_Y, 0])
        self.play(FadeIn(same_mark), glu[0].animate.set_fill(RED, 0.64),
                  right_glu[0].animate.set_fill(RED, 0.64), run_time=0.85)
        self.play(FadeIn(same), run_time=0.60)
        self.at("called a silent mutation")
        term = boxed_label("SILENT MUTATION", GOLD, 32, pad=0.27,
                           fill_opacity=0.47).move_to([0, -3.10, 0])
        term.label.set_color(TEXT)
        self.play(swap(same, term), run_time=1.2)
        self.finish()


def sickle_codon_world():
    dna = single_codon("GAG", BLUE, DNA_Y)
    rna = single_codon("GAG", GREEN, RNA_Y)
    glu = amino_acid("Glu", [0, PROTEIN_Y, 0], radius=0.63)
    return dna, rna, glu


def center_marker(y):
    return VGroup(*[
        Line([x, y - 0.55, 0], [x, y + 0.55, 0], color=GOLD, stroke_width=5)
        for x in (-0.66, 0.66)
    ])


class S08SickleCode(SpokenScene):
    def construct(self):
        dna, rna, glu = sickle_codon_world()
        labels = VGroup(
            place_label(T("coding DNA", 30, BLUE), dna, dirs=(LEFT,), buff=0.65),
            place_label(T("mRNA", 30, GREEN), rna, dirs=(LEFT,), buff=0.65),
            place_label(T("amino acid", 30, RED), glu, dirs=(LEFT,), buff=0.65),
        )
        self.add(field())
        self.at("follow the sickle substitution")
        self.play(FadeIn(dna), run_time=0.86)
        self.play(FadeIn(rna), run_time=0.80)
        self.play(FadeIn(glu), run_time=0.58)
        self.at("the usual coding")
        self.play(FadeIn(labels[0]), run_time=0.62)
        self.at("DNA reads")
        marker = center_marker(DNA_Y)
        self.play(Create(marker), run_time=0.70)
        self.at("the sickle allele")
        swap_base(self, dna[1], "T", BLUE, 43, direction=UP)
        self.at("reads GTG")
        allele = boxed_label("sickle allele", BLUE, 30, pad=0.30, fill_opacity=0.48).move_to([3.8, DNA_Y, 0])
        allele.label.set_color(TEXT)
        self.play(FadeIn(allele), run_time=0.65)
        self.at("messenger RNA therefore")
        self.play(marker.animate.shift(DOWN * (DNA_Y - RNA_Y)), run_time=0.87)
        self.play(FadeIn(labels[1]), run_time=0.45)
        self.at("reads GUG instead")
        swap_base(self, rna[1], "U", GREEN, 43, direction=DOWN)
        self.at("the ribosome places")
        window = codon_window()
        self.play(FadeIn(window), run_time=0.54)
        self.play(marker.animate.shift(DOWN * (RNA_Y - PROTEIN_Y)), run_time=0.6)
        self.at("valine instead")
        val = amino_acid("Val", glu.get_center(), radius=0.63)
        self.play(FadeOut(marker), swap(glu, val), run_time=0.85)
        self.play(FadeIn(labels[2]), run_time=0.5)
        self.finish()


def blood_cell(segments):
    cell = VMobject(stroke_color=RED, stroke_width=6, fill_color=RED, fill_opacity=0.29)
    cell.start_new_path(np.array([*segments[0], 0.0]))
    for a, b, c in segments[1:]:
        cell.add_cubic_bezier_curve_to(*[np.array([*pt, 0.0]) for pt in (a, b, c)])
    return cell.set_z_index(-2)


def round_cell():
    return blood_cell((
        (-4.9, -0.32), ((-4.9, 1.16), (-2.72, 2.07), (0, 2.07)),
        ((2.72, 2.07), (4.9, 1.16), (4.9, -0.32)),
        ((4.9, -1.82), (2.72, -2.73), (0, -2.73)),
        ((-2.72, -2.73), (-4.9, -1.82), (-4.9, -0.32)),
    ))


def sickled_cell():
    return blood_cell((
        (-4.9, 1.28), ((-3.55, 0.43), (-1.81, -0.34), (0, -0.34)),
        ((2.20, -0.34), (3.75, 0.24), (4.9, 1.16)),
        ((4.17, -1.18), (2.12, -2.72), (0, -2.72)),
        ((-2.59, -2.72), (-4.62, -1.10), (-4.9, 1.28)),
    ))


def hemoglobin_blob(center):
    return RoundedRectangle(width=0.84, height=0.56, corner_radius=0.26,
                            color=RED, stroke_width=4, fill_color=RED, fill_opacity=0.42).move_to(center)


def hemoglobin_rod(center, angle=0):
    return RoundedRectangle(width=2.34, height=0.42, corner_radius=0.19,
                            color=RED, stroke_width=4, fill_color=RED, fill_opacity=0.57).rotate(angle).move_to(center)


class S09SickleCell(SpokenScene):
    def construct(self):
        self.add(field())
        val = amino_acid("Val", [0, PROTEIN_Y, 0], radius=0.63)
        self.add(val)
        centers = [(-1.37, 0.80, 0), (0.75, -0.11, 0), (-0.10, -1.08, 0)]
        angles = [0.22, -0.19, 0.22]
        clusters = VGroup(*[
            VGroup(*[hemoglobin_blob([dx, dy, 0]) for dx, dy in ((-0.95, -0.20), (0, 0.20), (0.95, -0.11))])
            .rotate(angle).move_to(center)
            for center, angle in zip(centers, angles)
        ])
        hb_label = T("sickle hemoglobin", 33, RED).move_to([0, 2.60, 0])
        self.at("that changed spot")
        self.play(FadeOut(val[1]), run_time=0.35)
        self.play(ReplacementTransform(val[0], clusters), run_time=1.4)
        self.at("alter hemoglobin's")
        self.play(FadeIn(hb_label), run_time=0.76)
        self.at("when oxygen is low")
        low_oxygen = boxed_label("LOW OXYGEN", TEXT, 30, fill_opacity=0.08).move_to([0, 2.60, 0])
        self.play(swap(hb_label, low_oxygen), run_time=0.70)
        self.at("hemoglobin can join")
        rods = VGroup(*[hemoglobin_rod(center, angle) for center, angle in zip(centers, angles)])
        for cluster, rod, angle in zip(clusters, rods, angles):
            self.play(*[
                blob.animate.move_to(rod.get_center() + d * np.array([np.cos(angle), np.sin(angle), 0]))
                for blob, d in zip(cluster, (-0.46, 0, 0.46))
            ], run_time=0.48)
            self.remove(cluster)
            self.add(rod)
        schematic = scope_tag("schematic", 28, TEXT)
        self.play(FadeIn(schematic), run_time=0.50)
        self.at("the rods can bend")
        cell = round_cell()
        self.play(FadeIn(cell), run_time=0.50)
        ends = [(-1.52, -1.03, 0), (1.32, -1.01, 0), (-0.08, -1.86, 0)]
        self.play(Transform(cell, sickled_cell()), *[
            rod.animate.rotate(-angle).move_to(end) for rod, angle, end in zip(rods, angles, ends)
        ], run_time=2.55, rate_func=smooth)
        self.at("a letter change")
        cause = letter_row("GTG", BLUE, [0, 2.60, 0], width=0.66, size=30, gap=0.20)
        self.play(swap(low_oxygen, cause), run_time=0.56)
        self.play(Create(focus(cause[1])), run_time=0.50)
        result = T("sickled red blood cell", 30, RED).move_to([-1.2, -3.23, 0])
        self.at("a whole cell")
        self.play(FadeIn(result), run_time=0.75)
        self.finish()


class S10Context(SpokenScene):
    def construct(self):
        dna, rna, beads, links, labels, arrows = path_world()
        path = VGroup(dna, rna, beads, links, labels, arrows).shift(LEFT * 0.55)
        card_x = 4.70
        selected = base_marks(dna[4], BLUE)
        self.add(field(), dna, labels[0])
        self.at("a changed letter")
        self.play(Create(selected), run_time=0.75)
        self.at("does not guarantee")
        self.play(GrowArrow(arrows[0]), FadeIn(rna), run_time=0.85)
        self.play(FadeIn(labels[1]), run_time=0.37)
        changed = boxed_label("CHANGED PROTEIN", RED, 28, pad=0.14).move_to([card_x, 0.12, 0])
        self.at("a changed trait")
        self.play(FadeIn(beads), Create(links), run_time=0.61)
        self.play(FadeIn(labels[2]), FadeIn(changed), run_time=0.54)
        self.at("some substitutions keep")
        next_focus = base_marks(rna[4], GREEN)
        self.play(swap(selected, next_focus), GrowArrow(arrows[1]), run_time=0.90)
        same = boxed_label("SAME CHAIN", RED, 29).move_to([card_x, -1.12, 0])
        self.at("the same amino acid")
        last_focus = focus(beads[1], RED, 0.12)
        self.play(swap(next_focus, last_focus), FadeIn(same), run_time=0.92)
        self.at("protein effects also")
        self.play(FadeOut(last_focus), run_time=0.42)
        context = boxed_label("CONTEXT MATTERS", TEXT, 29).move_to([card_x, 1.36, 0])
        self.at("which copies a person")
        self.play(FadeIn(context), run_time=0.65)
        self.at("the environment")
        self.play(context.box.animate.set_stroke(TEXT, width=4.5), run_time=0.65)

        self.at("here is the reading rule")
        self.play(FadeOut(VGroup(path, changed, same, context)), run_time=0.55)
        row, lines, window = message_blocks(), dividers(), strip_window()
        self.play(FadeIn(row), FadeIn(window), run_time=0.75)
        self.play(LaggedStart(*[Create(ln) for ln in lines], lag_ratio=0.32), run_time=0.70)
        self.at("in coding DNA")
        start = T("START", 28, GOLD).move_to([base_x(1), 1.62, 0])
        stop = T("STOP", 28, TEXT, weight=BOLD).move_to([base_x(13), 1.62, 0])
        coding = caption("coding part", 30, TEXT, y=1.62).set_x(0)
        self.play(FadeIn(start), FadeIn(coding), FadeIn(stop), run_time=0.65)
        self.at("swaps change one codon")
        self.play(window.animate.shift(RIGHT * 3 * STEP), run_time=0.32)
        old_base = row[5]
        new_base = letter_block("C", GREEN, STRIP_BLOCK, 34, height=STRIP_HEIGHT).move_to(old_base)
        self.play(swap(old_base, new_base), run_time=0.34)
        self.at("codon", lead=-0.48)
        self.play(swap(new_base, old_base), FadeOut(window), run_time=0.28)
        self.at("frame shifts change", lead=0.30)
        base = waiting_block(INSERTED)
        self.play(FadeIn(base), VGroup(*row[INSERT_AT:]).animate.shift(RIGHT * STEP),
                  VGroup(*lines[1:]).animate.shift(RIGHT * STEP),
                  FadeOut(stop), FadeOut(coding), run_time=0.46)
        self.play(base.animate.set_y(STRIP_Y), run_time=0.32)
        self.play(LaggedStart(*[ln.animate.shift(LEFT * STEP) for ln in lines[1:]], lag_ratio=0.34),
                  run_time=0.36)
        self.play(FadeIn(strip_window(3)), FadeIn(strip_stop(3, y=2.25)), run_time=0.27)
        self.finish()


class S11End(EndCard):
    LINE = "In coding DNA, swaps change one codon; frameshifts change later codons."
