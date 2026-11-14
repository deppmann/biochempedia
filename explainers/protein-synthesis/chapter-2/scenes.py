"""When the Reading Changes — chapter 2 of Protein Synthesis.

COLOR MAP (carried unchanged through this chapter)
  BLUE   = DNA
  GREEN  = messenger RNA
  GOLD   = ribosome / reading window / pointers
  PURPLE = transfer RNA
  RED    = amino acids and amino-acid chains
  TEXT   = stop (never red), neutral labels
"""
from bp_parts import *  # noqa: F401,F403

PURPLE = "#B58CD9"
BLOCK = 1.24


def letter_block(letter, color, size=30, width=BLOCK):
    """One schematic letter block; its label intentionally sits inside its box."""
    box = RoundedRectangle(corner_radius=0.09, width=width, height=BLOCK,
                           stroke_color=color, stroke_width=4,
                           fill_color=color, fill_opacity=0.58)
    lab = M(letter, size, color).move_to(box)
    box.layout_ok = lab.layout_ok = True
    return VGroup(box, lab)


def letter_row(letters, color, center=ORIGIN, gap=0.04, width=BLOCK, size=30):
    return VGroup(*[letter_block(c, color, size, width) for c in letters]).arrange(RIGHT, buff=gap).move_to(center)


def divider_row(row, offset=0, color=GOLD):
    """Codon boundaries computed from the block geometry."""
    lines = VGroup()
    for i in range(offset, len(row) + 1, 3):
        x = row[0].get_left()[0] if i == 0 else row[-1].get_right()[0] if i == len(row) else row[i].get_left()[0] - 0.02
        lines.add(Line([x, row.get_bottom()[1] - 0.28, 0], [x, row.get_top()[1] + 0.28, 0],
                       color=color, stroke_width=3))
    return lines


def reading_strip(letters="AUGGAGCAAUUUUGA", y=0.25):
    """The carried green message and gold reading window, always at the same scale and place."""
    r = letter_row(letters, GREEN, [0, y, 0], width=0.70, size=28)
    divs = divider_row(r)
    window = RoundedRectangle(corner_radius=0.22, width=2.42, height=1.55,
                              stroke_color=GOLD, stroke_width=7,
                              fill_color=GOLD, fill_opacity=0.08)
    window.move_to(VGroup(*r[:3]))
    window.layout_ok = True
    return r, divs, window


def path_world():
    """The carried blue → green → red picture, rebuilt identically wherever it returns."""
    dna = letter_row("TACCTCGTTAAA", BLUE, [0, 2.25, 0], width=0.68, size=28)
    mrna = letter_row("AUGGAGCAAUUU", GREEN, [0, 0.25, 0], width=0.68, size=28)
    chain = VGroup(*[Circle(radius=0.34, stroke_color=RED, stroke_width=4,
                            fill_color=RED, fill_opacity=0.36) for _ in range(4)])
    chain.arrange(RIGHT, buff=0.50).move_to([0, -2.0, 0])
    links = VGroup(*[Line(chain[i].get_right(), chain[i + 1].get_left(), color=RED, stroke_width=5)
                     for i in range(3)])
    arrows = VGroup(Arrow([0, 1.75, 0], [0, 0.82, 0], buff=0.08, color=GREY, stroke_width=4),
                    Arrow([0, -0.32, 0], [0, -1.48, 0], buff=0.08, color=GREY, stroke_width=4))
    labels = VGroup(T("DNA", 30, BLUE).move_to([0, 3.18, 0]),
                    T("messenger RNA", 30, GREEN).move_to([3.8, 1.18, 0]),
                    T("amino acid chain", 30, RED).move_to([0, -2.92, 0]))
    return VGroup(dna, mrna, chain, links, arrows, labels)


def predict_backdrop(with_choices=True):
    """Exact last frame shared by the predict scene and its silent pause."""
    row, divs, window = reading_strip()
    inserted = letter_block("U", GREEN).move_to(row[2].get_center() + UP * 1.38)
    pointer = Arrow([row[3].get_center()[0], -1.25, 0], [row[-2].get_center()[0], -1.25, 0],
                    color=GOLD, stroke_width=6, buff=0.0)
    g = VGroup(row, divs, window, inserted, pointer)
    if with_choices:
        q = question_card("What changes after one inserted base?",
                          ["ONE CODON", "LATER CODONS TOO"], y=-3.25, size=30)
        g.add(q)
    return g


def hemoglobin_blob(label="hemoglobin", color=RED):
    b = RoundedRectangle(corner_radius=0.55, width=2.15, height=1.05,
                         stroke_color=color, stroke_width=4,
                         fill_color=color, fill_opacity=0.34)
    t = T(label, 24, color).move_to(b)
    b.layout_ok = t.layout_ok = True
    return VGroup(b, t)


class S00Hook(SpokenScene):
    def construct(self):
        world = path_world()
        dna, mrna, chain = world[0], world[1], world[2]
        self.play(FadeIn(dna, shift=DOWN * 0.12), FadeIn(world[5][0]), run_time=1.0)
        self.at("into green messenger")
        self.play(GrowArrow(world[4][0]), FadeIn(mrna, shift=DOWN * 0.12), FadeIn(world[5][1]), run_time=1.2)
        self.at("red amino acid")
        self.play(GrowArrow(world[4][1]), FadeIn(chain), Create(world[3]), FadeIn(world[5][2]), run_time=1.2)
        self.at("If a DNA")
        wobble = dna[4]
        self.play(Wiggle(wobble, scale_value=1.18, rotation_angle=0.08), run_time=1.5)
        q = T("How much of the chain changes?", 38, GOLD, font=TITLE_FONT).move_to([0, -3.15, 0])
        self.at("how much of")
        self.play(FadeOut(world[5][2]), FadeIn(q, shift=UP * 0.12), run_time=1.0)
        self.at("Keep watching")
        win = SurroundingRectangle(VGroup(*mrna[:3]), buff=0.18, corner_radius=0.18,
                                   color=GOLD, stroke_width=6)
        win.layout_ok = True
        pulse(dna, base=3, amp=1.2, speed=1.2)
        pulse(mrna, base=3, amp=1.2, speed=1.0)
        self.play(Create(win), run_time=0.7)
        self.play(win.animate.move_to(VGroup(*mrna[3:6])), run_time=1.4, rate_func=linear)
        self.finish()


class S01Title(TitleCard):
    LESSON = "Protein Synthesis"
    TITLE = "When the Reading Changes"


class S02Substitution(SpokenScene):
    def construct(self):
        dna = letter_row("TACCTCGTT", BLUE, [0, 2.35, 0], width=0.78, size=31)
        mrna = letter_row("AUGGAGCAA", GREEN, [0, 0.35, 0], width=0.78, size=31)
        window = SurroundingRectangle(VGroup(*mrna[3:6]), buff=0.23, corner_radius=0.20, color=GOLD, stroke_width=7)
        window.layout_ok = True
        aa = Circle(radius=0.42, color=RED, stroke_width=5, fill_color=RED, fill_opacity=0.22).move_to([0, -1.85, 0])
        aa_lab = T("amino acid", 29, RED).next_to(aa, DOWN, buff=0.18)
        self.play(FadeIn(dna), run_time=1.0)
        self.at("change in")
        self.play(Wiggle(dna[4], scale_value=1.18), run_time=1.1)
        self.at("substitution swaps")
        new_dna = letter_block("A", BLUE, 31, 0.78).move_to(dna[4])
        self.play(ReplacementTransform(dna[4], new_dna), run_time=1.0)
        self.play(FadeIn(mrna), Create(window), FadeIn(aa), FadeIn(aa_lab), run_time=1.1)
        pulse(dna, base=3, amp=1.2, speed=1.0)
        pulse(mrna, base=3, amp=1.2, speed=1.2)
        same = chip("SAME", RED, 32).move_to([3.9, -1.85, 0])
        self.at("same amino acid")
        self.play(FadeIn(same, shift=LEFT * 0.15), Indicate(aa, color=RED), run_time=1.2)
        changed = chip("CHANGED", RED, 32).move_to(same)
        aa2 = Circle(radius=0.42, color=RED, stroke_width=5, fill_color=RED, fill_opacity=0.40).move_to(aa)
        self.at("Another swap")
        self.play(FadeOut(same), Transform(aa, aa2), FadeIn(changed), run_time=1.1)
        stop = chip("STOP", TEXT, 32).move_to(same)
        self.at("or create")
        self.play(FadeOut(changed), FadeOut(aa), FadeOut(aa_lab), FadeIn(stop), run_time=1.1)
        self.finish()


class S03InsertDelete(SpokenScene):
    def construct(self):
        row, divs, window = reading_strip()
        self.play(FadeIn(row), FadeIn(window), Create(divs), run_time=1.0)
        pulse(row, base=3, amp=1.3, speed=1.1)
        waiting = letter_block("U", GREEN).move_to(row[2].get_center() + UP * 1.45)
        self.at("insertion adds")
        self.play(FadeIn(waiting, shift=DOWN * 0.2), run_time=0.9)
        self.play(*[row[i].animate.shift(RIGHT * 0.74) for i in range(2, len(row))],
                  waiting.animate.move_to(row[2].get_center()), run_time=1.1)
        self.at("deletion removes")
        leaving = row[6]
        self.play(leaving.animate.shift(UP * 1.45), run_time=0.8)
        self.play(FadeOut(leaving), *[row[i].animate.shift(LEFT * 0.74) for i in range(7, len(row))], run_time=0.9)
        self.at("does not see spaces")
        self.play(FadeOut(divs), run_time=0.8)
        self.at("starts at its")
        new_divs = divider_row(row)
        self.play(Create(new_divs), window.animate.move_to(VGroup(*row[:3])), run_time=1.0)
        self.play(window.animate.move_to(VGroup(*row[3:6])), run_time=1.4, rate_func=linear)
        self.at("Adding or removing")
        pulse(new_divs, base=3, amp=1.4, speed=2.5)
        self.play(*[new_divs[i].animate.shift(RIGHT * 0.70) for i in range(1, len(new_divs))], run_time=2.2)
        tag = chip("FRAMESHIFT", GOLD, 34).move_to([0, -2.05, 0])
        self.at("called a frame")
        self.play(FadeIn(tag, shift=UP * 0.15), run_time=1.0)
        self.finish()


class S04Predict(SpokenScene):
    def construct(self):
        row, divs, window = reading_strip()
        inserted = letter_block("U", GREEN).move_to(row[2].get_center() + UP * 1.38)
        self.add(row, divs, window, inserted)
        pulse(row, base=3, amp=1.3, speed=1.1)
        self.at("Predict what happens")
        self.play(inserted.animate.move_to(row[2].get_center()),
                  *[row[i].animate.shift(RIGHT * 0.72) for i in range(2, len(row))], run_time=1.5)
        q = question_card("What changes after one inserted base?",
                          ["ONE CODON", "LATER CODONS TOO"], y=-3.25, size=30)
        self.at("Will only")
        self.play(FadeIn(q.chips), run_time=1.0)
        self.play(FadeIn(q.question), run_time=0.7)
        pointer = Arrow([row[3].get_center()[0], -1.25, 0], [row[-2].get_center()[0], -1.25, 0],
                        color=GOLD, stroke_width=6, buff=0.0)
        self.at("Follow the dividers")
        self.play(GrowArrow(pointer), run_time=1.5, rate_func=linear)
        self.finish()


class S05Pause(NarratedScene):
    def construct(self):
        g = predict_backdrop()
        self.add(g)
        pointer = g[4]
        pointer.set_opacity(0.25)
        self.play(pointer.animate.set_opacity(1.0), run_time=4.5, rate_func=there_and_back)
        self.finish()


class S06Reveal(SpokenScene):
    def construct(self):
        row, old_divs, window = reading_strip()
        inserted = letter_block("U", GREEN).move_to(row[2].get_center())
        for i in range(2, len(row)):
            row[i].shift(RIGHT * 0.72)
        self.add(row, old_divs, window, inserted)
        pulse(row, base=3, amp=1.3, speed=1.1)
        new_divs = divider_row(row, offset=1)
        self.at("inserted block shifts")
        self.play(Transform(old_divs, new_divs), run_time=2.2)
        aas = VGroup()
        names = ["Met", "Val", "Arg", "Phe"]
        for i, name in enumerate(names):
            c = Circle(radius=0.34, color=RED, stroke_width=4, fill_color=RED, fill_opacity=0.22)
            t = T(name, 22, RED).move_to(c); c.layout_ok = t.layout_ok = True
            aas.add(VGroup(c, t))
        aas.arrange(RIGHT, buff=0.38).move_to([0, -2.05, 0])
        self.at("gold ribosome")
        self.play(window.animate.move_to(VGroup(*row[2:5])), FadeIn(aas[0]), run_time=1.2)
        self.play(window.animate.move_to(VGroup(*row[5:8])), FadeIn(aas[1]), run_time=1.2)
        self.at("Many later amino")
        self.play(window.animate.move_to(VGroup(*row[8:11])), FadeIn(aas[2]), run_time=1.2)
        self.play(window.animate.move_to(VGroup(*row[11:14])), FadeIn(aas[3]), run_time=1.2)
        stop = chip("STOP", TEXT, 34).move_to([4.8, -2.05, 0])
        self.at("early stop")
        self.play(FadeIn(stop, shift=LEFT * 0.2), run_time=1.0)
        self.at("Removing a base")
        self.play(FadeOut(stop), FadeOut(aas[-1]),
                  *[old_divs[i].animate.shift(LEFT * 0.70) for i in range(1, len(old_divs))], run_time=2.0)
        self.finish()


class S07SilentExample(SpokenScene):
    def construct(self):
        left = letter_row("GAG", GREEN, [-3.3, 0.8, 0], width=0.95, size=38)
        right = letter_row("GAG", GREEN, [3.3, 0.8, 0], width=0.95, size=38)
        a1 = chip("Glu", RED, 36).move_to([-3.3, -1.25, 0])
        a2 = chip("Glu", RED, 36).move_to([3.3, -1.25, 0])
        arrow = Arrow([-1.3, 0.8, 0], [1.3, 0.8, 0], color=GOLD, stroke_width=6)
        self.play(FadeIn(left), FadeIn(a1), run_time=1.0)
        pulse(left, base=3, amp=1.3, speed=1.0)
        pulse(right, base=3, amp=1.3, speed=1.2)
        self.at("Messenger codon")
        self.play(Indicate(left, color=GREEN), run_time=1.2)
        self.at("Change its last")
        self.play(GrowArrow(arrow), FadeIn(right), FadeIn(a2), run_time=1.1)
        new_a = letter_block("A", GREEN, 38, 0.95).move_to(right[2])
        self.at("making G")
        self.play(ReplacementTransform(right[2], new_a), run_time=1.0)
        self.at("still means")
        self.play(Indicate(a1, color=RED), Indicate(a2, color=RED), run_time=1.3)
        self.at("DNA changed")
        self.play(new_a.animate.shift(UP * 0.16), run_time=1.0, rate_func=there_and_back)
        same = chip("SAME CHAIN", GOLD, 36).move_to([0, -2.65, 0])
        self.at("chain did not")
        self.play(FadeIn(same, shift=UP * 0.15), run_time=1.1)
        label = T("silent mutation", 36, GREEN, font=TITLE_FONT).move_to([0, 2.6, 0])
        self.at("silent mutation")
        self.play(FadeIn(label), run_time=1.0)
        self.finish()


class S08SickleCode(SpokenScene):
    def construct(self):
        heads = VGroup(T("coding DNA", 30, BLUE), T("messenger RNA", 30, GREEN), T("amino acid", 30, RED))
        heads.arrange(DOWN, buff=1.18).move_to([-4.65, 0.25, 0])
        usual = VGroup(letter_row("GAG", BLUE, [0, 2.0, 0], width=0.92, size=36),
                       letter_row("GAG", GREEN, [0, 0.25, 0], width=0.92, size=36),
                       chip("Glu", RED, 36).move_to([0, -1.55, 0]))
        self.play(FadeIn(heads), run_time=0.8)
        pulse(usual[0], base=3, amp=1.3, speed=1.0)
        pulse(usual[1], base=3, amp=1.3, speed=1.2)
        self.at("usual coding")
        self.play(FadeIn(usual[0]), run_time=1.0)
        sickle_dna = letter_row("GTG", BLUE, [3.25, 2.0, 0], width=0.92, size=36)
        self.at("sickle allele")
        self.play(usual[0].animate.move_to([-1.5, 2.0, 0]), FadeIn(sickle_dna), run_time=1.0)
        mrna = letter_row("GUG", GREEN, [3.25, 0.25, 0], width=0.92, size=36)
        self.at("Messenger RNA")
        self.play(FadeIn(usual[1].move_to([-1.5, 0.25, 0])), FadeIn(mrna), run_time=1.2)
        self.at("instead of")
        self.play(Indicate(usual[1][1], color=GOLD), Indicate(mrna[1], color=GOLD), run_time=1.6)
        glu = usual[2].move_to([-1.5, -1.55, 0])
        val = chip("Val", RED, 36).move_to([3.25, -1.55, 0])
        self.at("ribosome places")
        self.play(FadeIn(glu), FadeIn(val), run_time=1.2)
        hi = SurroundingRectangle(VGroup(sickle_dna[1], mrna[1], val), color=GOLD, buff=0.14,
                                  stroke_width=5, corner_radius=0.15)
        hi.layout_ok = True
        self.play(Create(hi), run_time=1.4)
        self.finish()


class S09SickleCell(SpokenScene):
    def construct(self):
        blobs = VGroup(*[hemoglobin_blob("Hb") for _ in range(4)]).arrange_in_grid(2, 2, buff=0.35).move_to([0, 0.35, 0])
        self.play(LaggedStart(*[FadeIn(b, scale=0.9) for b in blobs], lag_ratio=0.18), run_time=1.4)
        self.at("alter hemoglobin")
        self.play(*[Indicate(b, color=RED, scale_factor=1.05) for b in blobs], run_time=1.3)
        low = chip("LOW OXYGEN", GOLD, 34).move_to([0, 2.75, 0])
        self.at("oxygen is low")
        self.play(FadeIn(low), run_time=0.9)
        rods = VGroup(*[RoundedRectangle(corner_radius=0.16, width=3.9, height=0.46,
                                         color=RED, stroke_width=4, fill_color=RED, fill_opacity=0.25)
                        for _ in range(3)]).arrange(DOWN, buff=0.28).move_to([0, 0.15, 0])
        self.at("join into stiff")
        self.play(ReplacementTransform(blobs, rods), run_time=1.6)
        cell = Circle(radius=2.55, color=RED, stroke_width=8, fill_color=RED, fill_opacity=0.22).move_to([0, 0.0, 0])
        cell.layout_ok = True
        self.play(Create(cell), run_time=0.9)
        pulse(cell, base=8, amp=2.0, speed=1.1)
        sickle = Arc(radius=2.25, start_angle=0.20 * PI, angle=1.28 * PI,
                     color=RED, stroke_width=25).move_to([0, -0.1, 0])
        sickle.set_cap_style(CapStyleType.ROUND)
        self.at("bend a soft")
        self.play(Transform(cell, sickle), rods.animate.rotate(-0.30), run_time=2.0)
        tag = scope_tag("schematic")
        self.at("whole cell")
        self.play(FadeIn(tag), Indicate(cell, color=RED), run_time=1.2)
        self.finish()


class S10Context(SpokenScene):
    def construct(self):
        world = path_world().scale(0.72).move_to([-3.1, 0.15, 0])
        cards = VGroup(chip("SAME CHAIN", GREEN, 28), chip("CHANGED PROTEIN", RED, 28),
                       chip("CONTEXT MATTERS", GOLD, 28)).arrange(DOWN, buff=0.46).move_to([3.75, 0.25, 0])
        self.play(FadeIn(world), run_time=1.2)
        pulse(world[0], base=3, amp=1.2, speed=1.0)
        pulse(world[1], base=3, amp=1.2, speed=1.2)
        self.at("does not guarantee")
        self.play(FadeIn(cards[0]), run_time=1.0)
        self.at("Some substitutions")
        self.play(Indicate(cards[0], color=GREEN), run_time=1.2)
        self.at("Protein effects")
        self.play(FadeIn(cards[1]), FadeIn(cards[2]), run_time=1.2)
        self.play(Indicate(cards[2], color=GOLD), run_time=1.0)
        self.at("reading rule")
        self.play(FadeOut(world), FadeOut(cards), run_time=0.8)
        row, divs, window = reading_strip("AUGGAGCAAUUUUGA", y=0.15)
        start = T("START", 28, GREEN).move_to([row[1].get_center()[0], 1.35, 0])
        stop = T("STOP", 28, TEXT).move_to([row[-2].get_center()[0], 1.35, 0])
        coding = T("coding part", 30, GREEN).move_to([0, 2.2, 0])
        self.play(FadeIn(row), Create(divs), FadeIn(window), FadeIn(start), FadeIn(stop), FadeIn(coding), run_time=1.1)
        pulse(row, base=3, amp=1.3, speed=1.1)
        swap_block = letter_block("A", GREEN).move_to(row[5])
        one = SurroundingRectangle(VGroup(*row[3:6]), color=GOLD, buff=0.16, corner_radius=0.14, stroke_width=5)
        one.layout_ok = True
        self.at("swaps change")
        self.play(ReplacementTransform(row[5], swap_block), Create(one), run_time=1.1)
        self.at("Frame shifts")
        inserted = letter_block("U", GREEN).move_to(row[2].get_center() + UP * 1.25)
        self.play(FadeOut(one), FadeIn(inserted), run_time=0.5)
        self.play(inserted.animate.move_to(row[2]),
                  *[divs[i].animate.shift(RIGHT * 0.70) for i in range(1, len(divs))], run_time=1.4)
        self.finish()


class S11End(EndCard):
    LINE = "In coding DNA, swaps change one codon; frameshifts change later codons."
