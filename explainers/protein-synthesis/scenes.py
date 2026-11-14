"""From Gene Copy to Protein Chain.

COLOR MAP (one color per concept, whole film)
  BLUE   = DNA
  GREEN  = messenger RNA
  GOLD   = ribosome
  PURPLE = transfer RNA
  RED    = amino acids / protein chain
  TEAL   = transcription enzyme and pore
  GREY   = cell and nucleus structure
"""
from bp_parts import *  # noqa: F401,F403


PURPLE = "#B58CD9"
BLOCK = 0.72


def letter_block(letter, color, w=BLOCK, size=34, filled=True):
    """A letter as a cartoon information block, never a molecular structure."""
    box = RoundedRectangle(
        corner_radius=0.09, width=w, height=w,
        stroke_color=color, stroke_width=3,
        fill_color=color, fill_opacity=0.24 if filled else 0.0,
    )
    label = M(letter, size, color).move_to(box) if letter else VGroup()
    g = VGroup(box, label)
    g.layout_ok = True  # the letter is deliberately centred inside its own information block
    return g


def letter_row(letters, color, w=BLOCK, size=34, gap=0.06, filled=True):
    return VGroup(*[letter_block(c, color, w, size, filled) for c in letters]).arrange(RIGHT, buff=gap)


def label_above(text, target, color, size=28):
    return T(text, size, color).next_to(target, UP, buff=0.18)


def ribosome(center=(3.8, -0.25, 0), scale=1.0, open_gap=0.0):
    """Gold two-lobed ribosome cartoon."""
    c = np.array(center, dtype=float)
    top = ArcBetweenPoints(c + [-1.35, 0.20 + open_gap, 0], c + [1.35, 0.20 + open_gap, 0], angle=-PI)
    top.set_stroke(GOLD, 8).set_fill(GOLD, 0.12)
    bottom = ArcBetweenPoints(c + [-1.15, -0.16 - open_gap, 0], c + [1.15, -0.16 - open_gap, 0], angle=PI)
    bottom.set_stroke(GOLD, 8).set_fill(GOLD, 0.12)
    return VGroup(top, bottom).scale(scale)


def cell_world(copy_letters="", faint=False):
    """The whole-cell picture shared by the hook and title."""
    cell = Ellipse(width=12.1, height=6.15, stroke_color=GREY, stroke_width=4,
                   fill_color=GREY, fill_opacity=0.14).move_to(DOWN * 0.15)
    nucleus = Ellipse(width=6.25, height=4.7, stroke_color=BLUE, stroke_width=4,
                      fill_color=BLUE, fill_opacity=0.15).move_to([-2.55, 0.0, 0])
    dna = letter_row("TACGGT", BLUE, w=0.68, size=31).move_to([-2.55, 0.45, 0])
    nuc_label = T("nucleus", 28, TEXT).move_to([-2.55, 2.05, 0])
    dna_label = T("DNA", 28, BLUE).next_to(dna, UP, buff=0.16)
    rib = ribosome((3.9, -0.25, 0), 1.05)
    rib_label = T("ribosome", 28, GOLD).next_to(rib, DOWN, buff=0.2).shift(UP * 0.16)
    path = DashedLine(dna.get_right() + RIGHT * 0.25, rib.get_left() + LEFT * 0.25,
                      dash_length=0.16, color=TEAL, stroke_width=3)
    copy = letter_row(copy_letters, GREEN, w=0.68, size=31).move_to([-2.55, -0.65, 0]) if copy_letters else VGroup()
    g = VGroup(cell, nucleus, dna, nuc_label, dna_label, rib, rib_label, path, copy)
    if faint:
        g.set_opacity(0.20)
        g.layout_ok = True  # deliberate title-card backdrop, not reading content
    return g


def gene_world(rna_letters="", open_gene=True):
    """The zoomed gene picture rebuilt identically through transcription scenes."""
    nucleus = Ellipse(width=12.2, height=5.75, stroke_color=BLUE, stroke_width=3,
                      fill_color=BLUE, fill_opacity=0.14).move_to(DOWN * 0.1)
    top = letter_row("GCTTACGGTAAC", BLUE, w=0.69, size=29).move_to([0, 1.23, 0])
    bottom = letter_row("CGAATGCCATTG", BLUE, w=0.69, size=29).move_to([0, 0.37, 0])
    selected = VGroup(*top[3:9], *bottom[3:9])
    for i, b in enumerate(top):
        if i < 3 or i > 8:
            b.set_opacity(0.28)
            bottom[i].set_opacity(0.28)
    if open_gene:
        for b in top[3:9]:
            b.shift(UP * 0.27)
        for b in bottom[3:9]:
            b.shift(DOWN * 0.27)
    gene_box = SurroundingRectangle(selected, color=TEAL, buff=0.18, stroke_width=3, corner_radius=0.12)
    clamp = VGroup(
        Arc(radius=1.05, start_angle=0.15 * PI, angle=0.7 * PI, color=TEAL, stroke_width=10),
        Arc(radius=1.05, start_angle=1.15 * PI, angle=0.7 * PI, color=TEAL, stroke_width=10),
    ).move_to([0, 0.8, 0])
    rna = letter_row(rna_letters, GREEN, w=0.69, size=29).move_to([0, -1.06, 0]) if rna_letters else VGroup()
    return VGroup(nucleus, top, bottom, gene_box, clamp, rna), {
        "nucleus": nucleus, "top": top, "bottom": bottom, "gene": gene_box,
        "clamp": clamp, "rna": rna,
    }


def pairing_key(at=(4.75, -1.8, 0), compact=True):
    pairs = [("A", "U"), ("T", "A"), ("C", "G"), ("G", "C")]
    rows = VGroup(*[
        VGroup(letter_block(a, BLUE, 0.48, 23), T("→", 26, TEXT), letter_block(b, GREEN, 0.48, 23))
        .arrange(RIGHT, buff=0.12)
        for a, b in pairs
    ])
    rows.arrange(DOWN if compact else RIGHT, buff=0.12).move_to(at)
    title = T("DNA → mRNA", 26, TEXT).next_to(rows, UP, buff=0.16)
    return VGroup(title, rows)


def predict_picture(with_question_mark=True):
    dna = letter_row("TAC", BLUE, w=1.18, size=50, gap=0.18).move_to([-1.55, 1.05, 0])
    empty = letter_row("   ", GREEN, w=1.18, size=50, gap=0.18, filled=False).move_to([-1.55, -0.48, 0])
    links = VGroup(*[
        DashedLine(dna[i].get_bottom(), empty[i].get_top(), color=GREY, stroke_width=3, dash_length=0.12)
        for i in range(3)
    ])
    key = pairing_key((4.75, 0.25, 0))
    qmark = T("?", 54, GOLD).move_to(empty[0]) if with_question_mark else VGroup()
    qmark.layout_ok = True  # deliberately travels inside the three empty answer boxes
    field = Ellipse(width=12.4, height=6.2, stroke_opacity=0,
                    fill_color=BLUE, fill_opacity=0.14).move_to(UP * 0.05).set_z_index(-5)
    return VGroup(dna, empty, links, key, qmark, field), {"dna": dna, "empty": empty, "key": key, "qmark": qmark}


CODONS = ("AUG", "GCU", "AAA", "UUU", "UGA")


def translation_world(ribo_index=0, chain_count=0, show_cytoplasm=False):
    """The carried translation strip, ribosome, dividers, and optional red chain."""
    strip = letter_row("".join(CODONS), GREEN, w=0.63, size=27, gap=0.035).move_to([0, -0.72, 0])
    dividers = VGroup()
    for i in range(1, 5):
        x = (strip[3 * i - 1].get_right()[0] + strip[3 * i].get_left()[0]) / 2
        dividers.add(Line([x, -1.18, 0], [x, -0.26, 0], color=TEXT, stroke_width=3))
    center = VGroup(*strip[3 * ribo_index:3 * ribo_index + 3]).get_center()
    rib = ribosome((center[0], -0.72, 0), 0.92)
    chain = VGroup(*[
        VGroup(Circle(radius=0.4, stroke_color=RED, stroke_width=4, fill_color=RED, fill_opacity=0.22),
               T(name, 24, RED).move_to(ORIGIN))
        for name in ("Met", "Ala", "Lys", "Phe")[:chain_count]
    ])
    if len(chain):
        for acid in chain:
            acid.layout_ok = True  # abbreviation deliberately sits inside its amino-acid circle
        chain.arrange(RIGHT, buff=0.2).move_to([0, 2.05, 0])
        links = VGroup(*[Line(chain[i].get_right(), chain[i + 1].get_left(), color=RED, stroke_width=5)
                         for i in range(len(chain) - 1)])
    else:
        links = VGroup()
    field = Ellipse(width=12.7, height=6.25, stroke_opacity=0,
                    fill_color=BLUE, fill_opacity=0.14).move_to(DOWN * 0.05).set_z_index(-5)
    cytoplasm = T("cytoplasm", 28, TEXT).move_to([0, 2.72, 0]) if show_cytoplasm else VGroup()
    return VGroup(strip, dividers, rib, links, chain, field, cytoplasm), {
        "strip": strip, "dividers": dividers, "rib": rib, "chain": chain, "links": links,
    }


def transfer_rna(anticodon, aa, x=0):
    """A key-shaped tRNA cartoon carrying one labelled amino acid circle."""
    stem = Line([x, -2.65, 0], [x, -1.72, 0], color=PURPLE, stroke_width=10)
    arms = ArcBetweenPoints([x - 0.48, -2.35, 0], [x + 0.48, -2.35, 0], angle=-PI, color=PURPLE, stroke_width=8)
    anti = letter_row(anticodon, PURPLE, w=0.42, size=22, gap=0.03).move_to([x, -1.46, 0])
    acid = VGroup(Circle(radius=0.34, color=RED, stroke_width=4, fill_color=RED, fill_opacity=0.22),
                   T(aa, 24, RED)).move_to([x, -3.05, 0])
    return VGroup(stem, arms, anti, acid)


class S00Hook(SpokenScene):
    def construct(self):
        world = cell_world()
        cell, nucleus, dna, nuc_label, dna_label, rib, rib_label, path, _ = world
        pulse(dna, base=3.0, amp=1.2, speed=2.3)
        self.at("A plant or animal cell")
        self.play(FadeIn(cell), FadeIn(nucleus), run_time=1.25)
        self.play(FadeIn(dna, shift=DOWN * 0.12), run_time=1.2)
        self.at("inside the nucleus")
        self.play(FadeIn(nuc_label), FadeIn(dna_label), run_time=0.65)
        self.at("How can their instructions")
        self.play(Create(path), FadeIn(rib, scale=1.08), run_time=1.2)
        self.at("a ribosome outside")
        self.play(FadeIn(rib_label), Indicate(rib, color=GOLD, scale_factor=1.08), run_time=0.8)
        self.at("Watch the blue")
        copy = letter_row("AUG", GREEN, w=0.68, size=31).move_to([-2.55, -0.65, 0])
        self.play(LaggedStart(*[FadeIn(b, shift=RIGHT * 0.18) for b in copy], lag_ratio=0.25),
                  run_time=3.4)
        self.play(copy.animate.shift(RIGHT * 0.38), run_time=1.0)
        bob(copy, amp=0.06, speed=1.8)
        self.add(copy)
        self.finish()


class S01Title(TitleCard):
    LESSON = "Protein Synthesis"
    TITLE = "From Gene Copy to Protein Chain"

    def construct(self):
        backdrop = cell_world("AUG", faint=True)
        title = T(self.TITLE, 50, font=TITLE_FONT)
        fit(title, max_w=11.5)
        lesson = T(self.LESSON.upper(), 24, TEAL, weight=BOLD)
        rule = Line(LEFT * 1.4, RIGHT * 1.4, color=GOLD, stroke_width=4)
        card = VGroup(lesson, title, rule).arrange(DOWN, buff=0.34)
        self.add(backdrop)
        self.play(FadeIn(card, shift=UP * 0.12), run_time=0.8)
        self.wait(0.75)
        self.play(FadeOut(card), FadeOut(backdrop), run_time=0.45)
        self.finish()


class S02Copy(SpokenScene):
    def construct(self):
        world, p = gene_world()
        heading = T("protein synthesis", 36, TEXT).move_to([0, 3.25, 0])
        self.at("Making a protein")
        self.play(FadeIn(p["nucleus"]), FadeIn(p["top"]), FadeIn(p["bottom"]), run_time=1.2)
        self.play(FadeIn(heading), run_time=0.7)
        self.play(Indicate(VGroup(p["top"], p["bottom"]), color=BLUE, scale_factor=1.015), run_time=1.8)
        self.at("The first stage")
        stage = T("transcription", 36, TEAL).move_to(heading)
        self.play(swap(heading, stage), run_time=0.8)
        self.play(Create(p["gene"]), run_time=1.3)
        self.at("An enzyme opens")
        self.play(FadeIn(p["clamp"], scale=1.12), run_time=1.0)
        self.play(pulse(p["clamp"], base=8, amp=2, speed=2).animate.shift(RIGHT * 0.01), run_time=0.6)
        self.at("It uses the template strand")
        template = T("template strand", 28, BLUE).move_to([0, -2.15, 0])
        self.play(FadeIn(template), Indicate(VGroup(*p["bottom"][3:9]), color=BLUE), run_time=0.9)
        self.at("to build messenger")
        rna = letter_row("AUGCCA", GREEN, w=0.69, size=29).move_to([0, -1.25, 0])
        self.play(FadeOut(template),
                  LaggedStart(*[FadeIn(b, shift=LEFT * 0.16) for b in rna], lag_ratio=0.18), run_time=1.65)
        rna_label = T("messenger RNA", 28, GREEN).next_to(rna, DOWN, buff=0.2)
        self.play(FadeIn(rna_label), run_time=0.45)
        self.at("Only the selected gene")
        self.play(Indicate(p["gene"], color=TEAL, scale_factor=1.03), run_time=0.9)
        bob(rna, amp=0.04, speed=2.0)
        self.finish()


class S03Pair(SpokenScene):
    def construct(self):
        field = Ellipse(width=12.4, height=6.2, stroke_opacity=0,
                        fill_color=BLUE, fill_opacity=0.14).move_to(UP * 0.05).set_z_index(-5)
        self.add(field)
        template = letter_row("ATCG", BLUE, w=1.05, size=44, gap=0.16).move_to([-1.25, 1.15, 0])
        clamp = VGroup(
            Arc(radius=1.25, start_angle=0.15 * PI, angle=0.7 * PI, color=TEAL, stroke_width=11),
            Arc(radius=1.25, start_angle=1.15 * PI, angle=0.7 * PI, color=TEAL, stroke_width=11),
        ).move_to([-1.25, 0.35, 0])
        clamp.layout_ok = True  # enzyme clamp intentionally surrounds the paired blocks
        key = pairing_key((4.75, 0.2, 0))
        answers = letter_row("UAGC", GREEN, w=1.05, size=44, gap=0.16).move_to([-1.25, -0.65, 0])
        links = VGroup(*[Line(template[i].get_bottom(), answers[i].get_top(), color=GREY, stroke_width=3)
                         for i in range(4)])
        self.at("Each green")
        self.play(FadeIn(template), FadeIn(clamp), run_time=0.8)
        self.play(LaggedStart(*[AnimationGroup(Create(links[i]), FadeIn(answers[i], shift=UP * 0.15))
                                for i in range(4)], lag_ratio=0.23), run_time=1.8)
        self.at("letter appears with")
        self.play(FadeIn(key[0]), FadeIn(key[1][0]), run_time=0.7)
        self.at("T pairs with A")
        self.play(FadeIn(key[1][1]), Indicate(VGroup(template[1], answers[1]), color=GOLD), run_time=0.7)
        self.at("C pairs with G")
        self.play(FadeIn(key[1][2]), Indicate(VGroup(template[2], answers[2]), color=GOLD), run_time=0.7)
        self.at("and G pairs with C")
        self.play(FadeIn(key[1][3]), Indicate(VGroup(template[3], answers[3]), color=GOLD), run_time=0.75)
        self.at("uses U instead")
        note = T("RNA uses U, not T", 30, GREEN).move_to([0, -2.35, 0])
        self.play(FadeIn(note), Indicate(answers[0], color=GREEN, scale_factor=1.12), run_time=0.9)
        bob(answers, amp=0.035, speed=1.8)
        self.finish()


class S04Predict(SpokenScene):
    QUESTION = "Which mRNA group pairs with TAC?"

    def construct(self):
        pic, p = predict_picture()
        self.at("Try the next template group")
        self.play(FadeIn(p["dna"], shift=DOWN * 0.12), FadeIn(p["empty"]), run_time=1.0)
        self.at("The blue")
        self.play(LaggedStart(*[Indicate(b, color=BLUE, scale_factor=1.08) for b in p["dna"]], lag_ratio=0.25),
                  FadeIn(p["key"]), run_time=1.25)
        self.at("Which green messenger")
        self.play(Create(VGroup(*pic[2])), FadeIn(p["qmark"]), run_time=0.9)
        q = question_card(self.QUESTION, y=-3.12, max_w=9.9)
        self.play(FadeIn(q), run_time=0.7)
        self.play(p["qmark"].animate.move_to(p["empty"][2]), run_time=2.3, rate_func=there_and_back)
        self.at("Keep the pairing key")
        self.play(Indicate(p["key"], color=GOLD, scale_factor=1.02), run_time=0.8)
        self.at("choose the full group")
        self.play(p["qmark"].animate.move_to(p["empty"][2]), run_time=1.1, rate_func=there_and_back)
        self.finish()


class S05Pause(PredictPause):
    QUESTION = "Which mRNA group pairs with TAC?"
    SECONDS = 4.5

    def backdrop(self):
        pic, p = predict_picture()
        base = p["qmark"].get_center().copy()
        p["qmark"]._loop_t = 0.0

        def loop(mob, dt):
            mob._loop_t += dt
            mob.move_to(base + [1.25 * np.sin(0.85 * mob._loop_t), 0.16 * np.cos(1.7 * mob._loop_t), 0])

        p["qmark"].add_updater(loop)
        return pic


class S06Reveal(SpokenScene):
    def construct(self):
        pic, p = predict_picture(with_question_mark=False)
        self.add(pic)
        answers = letter_row("AUG", GREEN, w=1.18, size=50, gap=0.18).move_to(p["empty"])
        self.at("T pairs with A")
        self.play(ReplacementTransform(p["empty"][0], answers[0]), run_time=0.8)
        focus = SurroundingRectangle(VGroup(p["dna"][0], answers[0]), color=GOLD, buff=0.14,
                                     corner_radius=0.1, stroke_width=4)
        self.play(Create(focus), run_time=1.1)
        self.at("A pairs with U")
        focus2 = SurroundingRectangle(VGroup(p["dna"][1], answers[1]), color=GOLD, buff=0.14,
                                      corner_radius=0.1, stroke_width=4)
        self.play(ReplacementTransform(p["empty"][1], answers[1]), ReplacementTransform(focus, focus2), run_time=0.8)
        self.at("C pairs with G")
        self.play(ReplacementTransform(p["empty"][2], answers[2]), run_time=0.8)
        self.at("The messenger group")
        group_box = SurroundingRectangle(answers, color=GREEN, buff=0.16, corner_radius=0.12, stroke_width=4)
        self.play(FadeOut(focus2), Create(group_box), run_time=0.75)
        self.at("The enzyme releases")
        full = letter_row("AUGCCAUGA", GREEN, w=0.72, size=31).move_to([0, -0.65, 0])
        self.play(FadeOut(p["key"]), FadeOut(pic[2]), ReplacementTransform(VGroup(answers, group_box), full), run_time=1.3)
        self.at("The green strand peels")
        closed = letter_row("TACGGTACG", BLUE, w=0.72, size=31).move_to([0, 0.82, 0])
        self.play(full.animate.shift(UP * 1.45 + RIGHT * 0.5), FadeOut(p["dna"]), FadeIn(closed), run_time=1.7)
        self.at("blue DNA closes")
        dna_box = SurroundingRectangle(closed, color=BLUE, buff=0.12, corner_radius=0.1, stroke_width=3)
        self.play(Create(dna_box), Indicate(closed, color=BLUE, scale_factor=1.02), run_time=1.0)
        inside = T("DNA stays inside", 28, BLUE).next_to(closed, DOWN, buff=0.24)
        self.play(FadeIn(inside), run_time=0.55)
        bob(full, amp=0.05, speed=1.7)
        self.finish()


class S07Translate(SpokenScene):
    def construct(self):
        membrane = VGroup(
            Line([-2.8, -3.0, 0], [-2.8, -0.55, 0], color=BLUE, stroke_width=7),
            Line([-2.8, 0.55, 0], [-2.8, 3.0, 0], color=BLUE, stroke_width=7),
        )
        pore = Circle(radius=0.55, color=TEAL, stroke_width=5).move_to([-2.8, 0, 0])
        pore.layout_ok = True  # message deliberately passes through the pore
        strip = letter_row("AUGGCUAAA", GREEN, w=0.62, size=27, gap=0.03).move_to([-3.65, 0, 0])
        self.at("The messenger RNA")
        self.play(FadeIn(membrane), FadeIn(pore), FadeIn(strip), run_time=0.9)
        self.at("through a pore")
        self.play(strip.animate.move_to([1.0, 0, 0]), Indicate(pore, color=TEAL), run_time=1.7)
        world, p = translation_world(0, show_cytoplasm=True)
        self.at("Translation begins")
        self.play(FadeOut(membrane), FadeOut(pore), ReplacementTransform(strip, p["strip"]),
                  FadeIn(p["rib"], scale=1.12), run_time=1.2)
        rib_label = T("ribosome", 28, GOLD).move_to([0, -2.45, 0])
        self.at("gold ribosome grips")
        self.play(FadeIn(rib_label), Indicate(p["rib"], color=GOLD, scale_factor=1.05), run_time=0.75)
        self.at("It reads each codon")
        self.play(LaggedStart(*[Create(d) for d in p["dividers"]], lag_ratio=0.22), run_time=1.0)
        for i in (1, 2):
            new_center = VGroup(*p["strip"][3 * i:3 * i + 3]).get_center()
            self.play(p["rib"].animate.move_to([new_center[0], -0.72, 0]), run_time=0.55)
        self.at("A codon is")
        codon = SurroundingRectangle(VGroup(*p["strip"][6:9]), color=GOLD, buff=0.12,
                                     corner_radius=0.1, stroke_width=4)
        label = T("codon = 3 letters", 30, TEXT).move_to([0, 1.35, 0])
        self.play(Create(codon), FadeIn(label), run_time=0.8)
        self.at("an amino acid or stop")
        meanings = VGroup(chip("amino acid", RED, 28), T("or", 28, TEXT), chip("STOP", RED, 28)).arrange(RIGHT, buff=0.35)
        meanings.move_to([0, 2.35, 0])
        self.play(FadeIn(meanings, shift=DOWN * 0.12), run_time=0.8)
        bob(p["rib"], amp=0.035, speed=2.0)
        self.finish()


class S08Chain(SpokenScene):
    def construct(self):
        world, p = translation_world(0)
        self.add(world)
        chain = VGroup()
        chain_links = VGroup()
        last_acid = None
        acids = [("UAC", "Met"), ("CGA", "Ala"), ("UUU", "Lys"), ("AAA", "Phe")]
        self.at("Purple transfer RNA")
        trna = transfer_rna(*acids[0], x=p["rib"].get_x())
        self.play(FadeIn(trna, shift=UP * 1.1), run_time=2.4)
        trna_label = T("transfer RNA", 28, PURPLE).move_to([4.9, -2.75, 0])
        self.play(FadeIn(trna_label), run_time=0.55)
        self.play(trna.animate.shift(RIGHT * 0.22), run_time=1.6, rate_func=there_and_back)
        self.at("Its anticodon pairs")
        self.play(trna.animate.shift(UP * 1.45), Indicate(VGroup(*p["strip"][:3]), color=PURPLE), run_time=1.15)
        self.play(FadeOut(trna_label), run_time=0.35)
        self.at("The ribosome joins")
        self.play(trna[3].animate.move_to([-2.15, 2.05, 0]), FadeOut(VGroup(*trna[:3])), run_time=0.85)
        chain.add(trna[3])
        last_acid = trna[3]
        for i in range(1, 4):
            center = VGroup(*p["strip"][3 * i:3 * i + 3]).get_center()
            t = transfer_rna(*acids[i], x=center[0])
            self.play(p["rib"].animate.move_to([center[0], -0.72, 0]), FadeIn(t, shift=UP * 0.3), run_time=0.65)
            target = [-2.15 + i * 1.4, 2.05, 0]
            self.play(t[3].animate.move_to(target), FadeOut(VGroup(*t[:3])), run_time=0.65)
            link = Line(last_acid.get_right(), np.array(target) + LEFT * 0.34, color=RED, stroke_width=5)
            chain.add(t[3])
            last_acid = t[3]
            chain_links.add(link)
            self.play(Create(link), run_time=0.35)
        self.at("At a stop codon")
        stop = SurroundingRectangle(VGroup(*p["strip"][12:15]), color=RED, buff=0.12,
                                    corner_radius=0.1, stroke_width=5)
        no_fit = T("no tRNA fits", 30, RED).move_to([4.8, 1.15, 0])
        self.play(p["rib"].animate.move_to([VGroup(*p["strip"][12:15]).get_x(), -0.72, 0]),
                  Create(stop), FadeIn(no_fit), run_time=1.0)
        self.at("no amino acid is added")
        self.play(Indicate(stop, color=RED, scale_factor=1.04), run_time=0.75)
        self.at("chain is released")
        released = VGroup(chain, chain_links)
        self.play(released.animate.shift(UP * 0.55), p["rib"].animate.scale(1.12), FadeOut(no_fit), run_time=1.1)
        bob(released, amp=0.06, speed=1.6)
        self.finish()


class S09StartStop(SpokenScene):
    def construct(self):
        world, p = translation_world(0, chain_count=4)
        p["dividers"].set_opacity(0)
        self.add(world)
        self.at("Reading usually begins")
        start_box = SurroundingRectangle(VGroup(*p["strip"][:3]), color=GREEN, buff=0.12,
                                         corner_radius=0.1, stroke_width=5)
        start = T("START", 30, GREEN).move_to([p["strip"][1].get_x(), 0.35, 0])
        self.play(Create(start_box), FadeIn(start), run_time=0.9)
        self.play(p["rib"].animate.scale(1.35), run_time=2.2, rate_func=there_and_back)
        self.play(start_box.animate.scale(1.14), run_time=1.1, rate_func=there_and_back)
        self.at("It adds methionine")
        self.play(Indicate(p["chain"][0], color=RED, scale_factor=1.15), run_time=0.75)
        self.at("fixes the grouping")
        self.play(LaggedStart(*[FadeIn(d) for d in p["dividers"]], lag_ratio=0.2),
                  run_time=2.15)
        self.at("ribosome then moves")
        for i in range(1, 5):
            x = VGroup(*p["strip"][3 * i:3 * i + 3]).get_x()
            self.play(p["rib"].animate.move_to([x, -0.72, 0]), run_time=0.55)
        self.at("At UGA")
        stop_box = SurroundingRectangle(VGroup(*p["strip"][12:15]), color=RED, buff=0.12,
                                        corner_radius=0.1, stroke_width=5)
        stop = T("STOP", 32, RED).move_to([p["strip"][13].get_x(), 0.18, 0])
        self.play(FadeOut(start), FadeOut(start_box), Create(stop_box), FadeIn(stop), run_time=0.9)
        self.at("reading window opens")
        open_rib = ribosome((p["rib"].get_x(), -0.72, 0), 0.92, open_gap=0.42)
        self.play(ReplacementTransform(p["rib"], open_rib), run_time=0.85)
        self.at("finished chain floats free")
        self.play(VGroup(p["chain"], p["links"]).animate.shift(UP * 0.62), run_time=1.1)
        bob(VGroup(p["chain"], p["links"]), amp=0.055, speed=1.6)
        self.finish()


class S10Rule(SpokenScene):
    def construct(self):
        field = Ellipse(width=12.7, height=6.25, stroke_opacity=0,
                        fill_color=BLUE, fill_opacity=0.14).move_to(DOWN * 0.05).set_z_index(-5)
        self.add(field)
        chain = VGroup(*[
            VGroup(Circle(radius=0.38, color=RED, stroke_width=4, fill_color=RED, fill_opacity=0.22),
                   T(x, 25, RED))
            for x in ("Met", "Ala", "Lys", "Phe")
        ]).arrange(RIGHT, buff=0.35).move_to([0, 0.6, 0])
        links = VGroup(*[Line(chain[i].get_right(), chain[i + 1].get_left(), color=RED, stroke_width=6)
                         for i in range(3)])
        self.at("The release chain")
        self.play(FadeIn(chain), Create(links), run_time=1.0)
        self.at("fold into a working protein")
        targets = [[-0.85, 0.65, 0], [0.65, 1.05, 0], [0.85, -0.55, 0], [-0.65, -0.85, 0]]
        blob = RoundedRectangle(corner_radius=0.75, width=3.7, height=3.35, color=RED, stroke_width=5,
                                fill_color=RED, fill_opacity=0.09).move_to([0, 0.1, 0])
        self.play(*[chain[i].animate.move_to(targets[i]) for i in range(4)], FadeOut(links), FadeIn(blob), run_time=1.25)
        protein = T("protein", 34, RED).move_to([0, 2.35, 0])
        self.play(FadeIn(protein), run_time=0.45)
        self.at("message changed form")
        dna = letter_row("TAC", BLUE, w=0.82, size=34).move_to([-4.65, 0.1, 0])
        rna = letter_row("AUG", GREEN, w=0.82, size=34).move_to([0, 0.1, 0])
        protein_group = VGroup(blob, chain, protein)
        self.play(FadeIn(dna, shift=RIGHT * 0.2), FadeIn(rna, shift=RIGHT * 0.2),
                  protein_group.animate.move_to([4.55, 0.1, 0]), run_time=0.9)
        self.at("order guided every handoff")
        path1 = Arrow(dna.get_right(), rna.get_left(), buff=0.22, color=TEAL, stroke_width=5)
        path2 = Arrow(rna.get_right(), blob.get_left(), buff=0.22, color=TEAL, stroke_width=5)
        self.play(GrowArrow(path1), GrowArrow(path2), run_time=0.9)
        self.at("protein coding genes")
        labels = VGroup(T("DNA order", 28, BLUE).next_to(dna, DOWN, buff=0.22),
                        T("mRNA codons", 28, GREEN).next_to(rna, DOWN, buff=0.22),
                        T("amino acid order", 28, RED).next_to(blob, DOWN, buff=0.24))
        self.play(FadeIn(labels), run_time=1.1)
        self.at("DN order")
        self.play(Indicate(dna, color=BLUE, scale_factor=1.08), run_time=0.75)
        self.at("sets mRNA codons")
        self.play(Indicate(rna, color=GREEN, scale_factor=1.08), run_time=1.0)
        self.at("amino acid order")
        self.play(Indicate(blob, color=RED, scale_factor=1.035), run_time=1.0)
        self.at("That is how instructions")
        self.play(Indicate(VGroup(dna, rna, blob), color=GOLD, scale_factor=1.025), run_time=1.1)
        bob(blob, amp=0.045, speed=1.7)
        self.finish()


class S11End(EndCard):
    LINE = "In protein-coding genes, DNA order sets mRNA codons and amino acid order."
