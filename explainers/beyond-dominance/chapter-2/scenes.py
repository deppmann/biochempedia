"""From Families to Chromosomes — Beyond Dominant and Recessive, chapter 2.

COLOR MAP (kept from chapter 1)
  R_ALLELE = the red R allele / earlier red phenotype (#E85D5D)
  PALE     = the pale W allele and the generic recessive d allele (#F4E7C5)
  BLUE     = the B marker and chromosome-scale evidence
  PURPLE   = a person who shows the chosen trait
  TEAL     = scale / tool labels
  GOLD     = questions and chromosome 21
  GREY     = structure and neutral evidence

The family, prediction, karyotype and closing overview each have one builder.  Consecutive
scenes therefore rebuild carried objects at exactly the same scale and position.
"""
import random

from bp_parts import *  # noqa: F401,F403

R_ALLELE = "#E85D5D"
PALE = "#F4E7C5"
PURPLE = "#B58CD9"


def evidence_stage(color=PURPLE):
    """The film's shared landscape: a quiet evidence field with a slow scanning light."""
    card = RoundedRectangle(
        corner_radius=0.35, width=12.35, height=6.45,
        stroke_color=color, stroke_width=2.5,
        fill_color=color, fill_opacity=0.16,
    )
    scan = VGroup(*[
        Rectangle(width=0.3, height=6.15, stroke_width=0, fill_color=TEXT, fill_opacity=opacity)
        for opacity in (0.02, 0.045, 0.07, 0.045, 0.02)
    ]).arrange(RIGHT, buff=0)
    scan.move_to([-5.4, 0, 0])
    scan._travel = 0.0

    def sweep(mob, dt):
        mob._travel += 0.62 * dt
        mob.move_to([-5.4 + (mob._travel % 10.8), 0, 0])

    scan.add_updater(sweep)
    stage = VGroup(card, scan).set_z_index(-5)
    stage.layout_ok = True
    return stage


def allele_tile(letter, color, size=0.78, opacity=0.9):
    """A chapter-1 allele tile, with its letter deliberately inside its own block."""
    box = RoundedRectangle(
        corner_radius=0.13, width=size, height=size,
        stroke_color=color, stroke_width=3,
        fill_color=color, fill_opacity=opacity,
    )
    label = T(letter, max(24, int(size * 43)), BG, weight=BOLD).move_to(box)
    tile = VGroup(box, label)
    tile.layout_ok = True
    return tile


def person(kind, at, shaded=False, size=0.86, color=GREY):
    shape = (Square(size) if kind == "square" else Circle(radius=size / 2)).set_stroke(color, 4)
    shape.set_fill(PURPLE, 0.95 if shaded else 0.0).move_to(at)
    return shape


def portrait(kind, at, size=0.86):
    """A face-like family portrait that can transform into a pedigree symbol."""
    outline = (Square(size) if kind == "square" else Circle(radius=size / 2)).set_stroke(GREY, 3)
    outline.set_fill(GREY, 0.08).move_to(at)
    eyes = VGroup(Dot(radius=0.035, color=TEXT), Dot(radius=0.035, color=TEXT)).arrange(RIGHT, buff=0.18)
    eyes.move_to(outline.get_center() + UP * 0.10)
    smile = Arc(radius=0.18, start_angle=PI + 0.25, angle=PI - 0.5, color=TEXT, stroke_width=2)
    smile.move_to(outline.get_center() + DOWN * 0.08)
    return VGroup(outline, eyes, smile)


FAMILY_POS = {
    "dad": (-1.25, 1.45, 0),
    "mom": (1.25, 1.45, 0),
    "child": (0.0, -0.55, 0),
}


def nuclear_family(portraits=False, shaded_child=True, lines=True):
    """The carried three-person family used from the hook through the reveal."""
    make = portrait if portraits else person
    dad = make("square", FAMILY_POS["dad"])
    mom = make("circle", FAMILY_POS["mom"])
    child = make("circle", FAMILY_POS["child"], shaded=shaded_child) if not portraits else make("circle", FAMILY_POS["child"])
    partner = Line([-0.82, 1.45, 0], [0.82, 1.45, 0], color=GREY, stroke_width=4)
    down = Line([0, 1.45, 0], [0, -0.12, 0], color=GREY, stroke_width=4)
    g = VGroup(partner, down, dad, mom, child) if lines else VGroup(dad, mom, child)
    g.dad, g.mom, g.child = dad, mom, child
    g.partner, g.down = partner, down
    return g


def prediction_frame(include_question=True):
    """The exact held frame shared by s04 and the deliberate pause s05."""
    stage = evidence_stage(PURPLE)
    fam = nuclear_family(shaded_child=True)
    fam.shift(UP * 0.55)
    ghosts = VGroup(
        allele_tile("D", R_ALLELE, 0.48, 0.18).move_to([-1.55, 1.95, 0]),
        allele_tile("d", PALE, 0.48, 0.18).move_to([-0.95, 1.95, 0]),
        allele_tile("D", R_ALLELE, 0.48, 0.18).move_to([0.95, 1.95, 0]),
        allele_tile("d", PALE, 0.48, 0.18).move_to([1.55, 1.95, 0]),
    )
    cards = question_card(
        "Which simple model fits this clue better?",
        ["dominant?", "recessive?"], y=-3.08, size=30,
    )
    g = VGroup(stage, fam, ghosts, cards) if include_question else VGroup(stage, fam, ghosts)
    g.stage, g.family, g.ghosts, g.cards = stage, fam, ghosts, cards
    return g


def three_generation_pedigree():
    """A large, fixed three-generation pedigree used by s07 and s08."""
    people = VGroup(
        person("square", (-3.8, 2.05, 0), shaded=True),
        person("circle", (-2.25, 2.05, 0)),
        person("square", (1.7, 2.05, 0)),
        person("circle", (3.25, 2.05, 0), shaded=True),
        person("circle", (-3.15, 0.15, 0), shaded=True),
        person("square", (-1.45, 0.15, 0)),
        person("circle", (1.45, 0.15, 0)),
        person("square", (3.15, 0.15, 0), shaded=True),
        person("square", (-1.15, -1.75, 0)),
        person("circle", (0.0, -1.75, 0), shaded=True),
        person("circle", (1.15, -1.75, 0)),
    )
    lines = VGroup(
        Line([-3.37, 2.05, 0], [-2.68, 2.05, 0], color=GREY, stroke_width=4),
        Line([2.13, 2.05, 0], [2.82, 2.05, 0], color=GREY, stroke_width=4),
        Line([-3.02, 2.05, 0], [-3.02, 0.58, 0], color=GREY, stroke_width=4),
        Line([-3.02, 0.58, 0], [-1.45, 0.58, 0], color=GREY, stroke_width=4),
        Line([-3.15, 0.58, 0], [-3.15, 0.58 - 0.43, 0], color=GREY, stroke_width=4),
        Line([-1.45, 0.58, 0], [-1.45, 0.58 - 0.43, 0], color=GREY, stroke_width=4),
        Line([2.48, 2.05, 0], [2.48, 0.58, 0], color=GREY, stroke_width=4),
        Line([1.45, 0.58, 0], [3.15, 0.58, 0], color=GREY, stroke_width=4),
        Line([1.45, 0.58, 0], [1.45, 0.15, 0], color=GREY, stroke_width=4),
        Line([3.15, 0.58, 0], [3.15, 0.15, 0], color=GREY, stroke_width=4),
        Line([-1.02, 0.15, 0], [1.02, 0.15, 0], color=GREY, stroke_width=4),
        Line([0, 0.15, 0], [0, -1.32, 0], color=GREY, stroke_width=4),
        Line([-1.15, -1.32, 0], [1.15, -1.32, 0], color=GREY, stroke_width=4),
        *[Line([x, -1.32, 0], [x, -1.75 + 0.43, 0], color=GREY, stroke_width=4) for x in (-1.15, 0, 1.15)],
    )
    return VGroup(lines, people)


def karyotype(extra21=False):
    """A schematic 23-pair human karyotype with deterministic, countable bars."""
    counts = (8, 8, 7)
    centers = []
    for row, n in enumerate(counts):
        x0 = -5.15 if n == 8 else -4.45
        for col in range(n):
            centers.append(np.array([x0 + 1.47 * col, 1.95 - 1.55 * row, 0]))
    bars = VGroup()
    pairs = []
    for i, c in enumerate(centers):
        h = 0.9 - 0.018 * i
        pair = VGroup(
            RoundedRectangle(corner_radius=0.05, width=0.18, height=h, stroke_width=0, fill_color=BLUE, fill_opacity=0.92).move_to(c + LEFT * 0.17),
            RoundedRectangle(corner_radius=0.05, width=0.18, height=h * (0.98 if i % 3 else 0.92), stroke_width=0, fill_color=BLUE, fill_opacity=0.92).move_to(c + RIGHT * 0.17),
        )
        bars.add(pair)
        pairs.append(pair)
    extra = RoundedRectangle(corner_radius=0.05, width=0.18, height=0.9 - 0.018 * 20,
                             stroke_width=0, fill_color=GOLD, fill_opacity=0.95).move_to(centers[20] + RIGHT * 0.5)
    if extra21:
        bars.add(extra)
    title = T("23 matched chromosome pairs", 34, TEXT, weight=BOLD).move_to([0, 2.8, 0])
    sex = T("XX or XY", 26, TEAL).next_to(pairs[22], DOWN, buff=0.12)
    total = M("47 total" if extra21 else "46 total", 30, GOLD if extra21 else TEXT).move_to([-4.75, -2.28, 0])
    scale = T("whole-chromosome scale", 30, TEAL).move_to([2.6, -2.28, 0])
    g = VGroup(title, bars, sex, total, scale)
    g.bars, g.pairs, g.centers, g.extra, g.total = bars, pairs, centers, extra, total
    return g


def tiny_karyotype(at, scale=0.34):
    k = karyotype(False)
    k.remove(k[0], k[2], k[3], k[4])
    k.scale(scale).move_to(at)
    return k


def closing_panels():
    """Three equal panels containing the three views compared in the closing scene."""
    xs = (-4.35, 0, 4.35)
    titles = ("cross", "pedigree", "karyotype")
    colors = (R_ALLELE, PURPLE, BLUE)
    frames = VGroup()
    for x, title, color in zip(xs, titles, colors):
        frame = RoundedRectangle(corner_radius=0.18, width=3.85, height=4.55, stroke_color=color, stroke_width=3).move_to([x, 0.25, 0])
        label = T(title, 32, color, weight=BOLD).move_to([x, 2.12, 0])
        frames.add(VGroup(frame, label))

    # Dd × Dd, so every square is computed from one allele from each parent.
    cross_cells = VGroup()
    specs = (("DD", R_ALLELE), ("Dd", TEXT), ("Dd", TEXT), ("dd", PALE))
    for i, (txt, col) in enumerate(specs):
        cell = Square(1.05, stroke_color=GREY, stroke_width=2.5, fill_color=col, fill_opacity=0.15).move_to([
            xs[0] + (-0.55 if i % 2 == 0 else 0.55),
            0.45 + (0.55 if i < 2 else -0.55), 0,
        ])
        lab = T(txt, 28, col, weight=BOLD).move_to(cell)
        group = VGroup(cell, lab)
        group.layout_ok = True
        cross_cells.add(group)
    cross_note = T("possible combinations", 24, GREY).move_to([xs[0], -1.55, 0])
    cross = VGroup(cross_cells, cross_note)

    fam = nuclear_family(shaded_child=True).scale(0.72).move_to([xs[1], 0.25, 0])
    fam_note = T("family patterns", 24, GREY).move_to([xs[1], -1.55, 0])
    pedigree = VGroup(fam, fam_note)

    kt = tiny_karyotype([xs[2], 0.35, 0], 0.29)
    kt_note = T("whole chromosomes", 24, GREY).move_to([xs[2], -1.55, 0])
    chrom = VGroup(kt, kt_note)
    return VGroup(frames, cross, pedigree, chrom)


class S01Hook(SpokenScene, TitleCard):
    LESSON = "Beyond Dominant and Recessive"
    TITLE = "From Families to Chromosomes"

    def construct(self):
        self.add(evidence_stage(PURPLE))
        r = allele_tile("R", R_ALLELE, 1.05).move_to([-2.5, 0.8, 0])
        w = allele_tile("W", PALE, 1.05).move_to([2.5, 0.8, 0])
        lens = Circle(radius=1.55, color=TEAL, stroke_width=6, fill_color=PURPLE, fill_opacity=0.15).move_to([0, 0.8, 0])
        phenotype = T("phenotype changed", 30, PURPLE, weight=BOLD).move_to([0, -1.15, 0])
        self.at("The first film")
        self.play(FadeIn(r), FadeIn(w), run_time=0.7)
        self.play(Create(lens), FadeIn(phenotype), run_time=0.8)
        self.at("How can we follow")
        q = fit_text("How can we follow the copies?", max_w=10.5, size=42, color=GOLD).move_to([0, 3.05, 0])
        self.play(FadeIn(q, shift=DOWN * 0.12), run_time=0.6)
        self.play(r.animate.move_to([-0.55, 0.8, 0]), w.animate.move_to([0.55, 0.8, 0]), run_time=1.1)
        self.at("evidence that already exists")
        portraits = nuclear_family(portraits=True, shaded_child=False, lines=False).scale(1.18).shift(DOWN * 0.15)
        self.play(FadeOut(lens), FadeOut(phenotype), FadeIn(portraits), run_time=0.8)
        d1 = allele_tile("D", R_ALLELE, 0.74).move_to([-0.55, -1.55, 0])
        d2 = allele_tile("d", PALE, 0.74).move_to([0.55, -1.55, 0])
        model = T("new family model", 30, TEAL, weight=BOLD).move_to([0, -2.35, 0])
        self.play(Transform(r, d1), Transform(w, d2), FadeIn(model), run_time=0.9)
        self.add(scope_tag("schematic"))
        bob(r, amp=0.05, speed=1.5)
        bob(w, amp=0.05, speed=1.5, seed=3)
        self.at("right scale")
        scales = VGroup(
            chip("family", PURPLE, 28), chip("chromosome", BLUE, 28)
        ).arrange(RIGHT, buff=0.45).move_to([0, 2.75, 0])
        self.play(swap(q, scales), run_time=0.9)
        self.at("only some questions")
        self.play(Indicate(scales[0], color=PURPLE), Indicate(scales[1], color=BLUE), run_time=1.2)
        self.finish()


class S02Title(NarratedScene):
    def construct(self):
        self.add(evidence_stage(PURPLE))
        fam = nuclear_family(portraits=True, shaded_child=False, lines=False).scale(1.18).shift(DOWN * 0.35)
        lines = VGroup(
            Line([-0.97, 1.36, 0], [0.97, 1.36, 0], color=GREY, stroke_width=3),
            Line([0, 1.36, 0], [0, 0.18, 0], color=GREY, stroke_width=3),
        )
        title = T("From Families to Chromosomes", 50, TEXT, font=TITLE_FONT).move_to([0, 3.0, 0])
        fit(title, max_w=11.5)
        tiles = VGroup(
            allele_tile("D", R_ALLELE, 0.55).move_to([-1.45, 1.45, 0]),
            allele_tile("d", PALE, 0.55).move_to([1.45, 1.45, 0]),
        )
        self.add(fam, tiles)
        self.play(Create(lines), Write(title), run_time=0.85)
        bob(tiles[0], amp=0.04, speed=1.7)
        bob(tiles[1], amp=0.04, speed=1.7, seed=2)
        self.wait(0.45)
        self.play(title.animate.scale(0.66).move_to([0, 2.8, 0]), run_time=0.45)
        self.finish()


class S03Pedigree(SpokenScene):
    def construct(self):
        self.add(evidence_stage(PURPLE))
        portraits = nuclear_family(portraits=True, shaded_child=False, lines=False)
        self.add(portraits)
        title = T("family", 32, TEXT).move_to([0, 3.2, 0])
        self.at("A pedigree")
        self.play(FadeIn(title), run_time=0.4)
        symbols = nuclear_family(portraits=False, shaded_child=False, lines=False)
        self.play(*[Transform(a, b) for a, b in zip(portraits, symbols)], run_time=1.1)
        ped_title = T("pedigree model", 36, TEAL, weight=BOLD).move_to([0, 3.2, 0])
        self.play(swap(title, ped_title), run_time=0.6)
        self.at("Squares and circles")
        symbol_key = VGroup(
            VGroup(person("square", ORIGIN, size=0.55), T("person", 28, TEXT)).arrange(RIGHT, buff=0.2),
            VGroup(person("circle", ORIGIN, size=0.55), T("person", 28, TEXT)).arrange(RIGHT, buff=0.2),
        ).arrange(RIGHT, buff=0.65).move_to([0, -2.55, 0])
        self.play(FadeIn(symbol_key), run_time=0.7)
        self.at("Lines connect")
        lines = nuclear_family(shaded_child=False).submobjects[:2]
        self.play(*[Create(x) for x in lines], run_time=0.8)
        self.at("Generations stack downward")
        gen = VGroup(T("I", 28, GREY).move_to([-4.0, 1.45, 0]), T("II", 28, GREY).move_to([-4.0, -0.55, 0]))
        arrow = Arrow([-4.7, 1.8, 0], [-4.7, -1.0, 0], color=GREY, stroke_width=4, buff=0.0, tip_length=0.22)
        time = T("time", 28, GREY).next_to(arrow, LEFT, buff=0.18)
        self.play(FadeIn(gen), GrowArrow(arrow), FadeIn(time), run_time=0.9)
        self.at("shading marks")
        key = VGroup(person("circle", ORIGIN, shaded=True, size=0.55), T("shaded = shows trait", 28, PURPLE)).arrange(RIGHT, buff=0.2).move_to([3.9, -2.55, 0])
        self.play(FadeOut(symbol_key), FadeIn(key), run_time=0.6)
        self.play(portraits[2][0].animate.set_fill(PURPLE, 0.95), run_time=0.7)
        self.at("symbol, not a genotype")
        note = T("symbol ≠ genotype", 34, GOLD, weight=BOLD).move_to([0, -2.55, 0])
        self.play(swap(key, note), run_time=0.7)
        self.finish()


class S04Predict(SpokenScene):
    def construct(self):
        frame = prediction_frame()
        fam, ghosts, cards = frame.family, frame.ghosts, frame.cards
        self.add(frame.stage)
        self.at("The parents")
        self.play(FadeIn(fam), run_time=0.65)
        self.play(Indicate(VGroup(fam.dad, fam.mom), color=TEXT), run_time=0.8)
        self.at("child does")
        self.play(Indicate(fam.child, color=PURPLE, scale_factor=1.18), run_time=0.8)
        self.at("Which simple model")
        self.play(FadeIn(cards.chips), run_time=0.6)
        self.play(FadeIn(cards.question), run_time=0.5)
        self.at("Hold both possibilities")
        self.play(FadeIn(ghosts), run_time=0.7)
        pulse(fam.partner, base=4, amp=1.2, speed=1.5)
        pulse(fam.down, base=4, amp=1.2, speed=1.5)
        self.finish()


class S05Pause(PredictPause):
    QUESTION = "Which simple model fits this clue better?"
    OPTIONS = ["dominant?", "recessive?"]
    SECONDS = 4.5

    def backdrop(self):
        frame = prediction_frame(include_question=False)
        pulse(frame.family.partner, base=4, amp=1.2, speed=1.5)
        pulse(frame.family.down, base=4, amp=1.2, speed=1.5)
        return frame


class S06Reveal(SpokenScene):
    def construct(self):
        frame = prediction_frame()
        fam, ghosts, cards = frame.family, frame.ghosts, frame.cards
        self.add(frame.stage, fam, ghosts, cards)
        self.at("A recessive model can fit")
        answer = chip("recessive can fit", PALE, 30)
        answer.move_to(cards.chips[1]).shift(RIGHT * 0.65)
        self.play(Transform(cards.chips[1], answer), run_time=0.7)
        self.at("Each unshaded parent")
        left_d = allele_tile("d", PALE, 0.62).move_to(fam.dad.get_center())
        right_d = allele_tile("d", PALE, 0.62).move_to(fam.mom.get_center())
        self.play(FadeOut(ghosts), FadeIn(left_d), FadeIn(right_d), run_time=0.7)
        self.at("child may receive both")
        self.play(left_d.animate.move_to(fam.child.get_center() + LEFT * 0.35),
                  right_d.animate.move_to(fam.child.get_center() + RIGHT * 0.35), run_time=1.2)
        self.at("points toward recessive")
        arrow = CurvedArrow([2.4, 0.6, 0], [1.0, -0.1, 0], angle=-0.5, color=PALE, stroke_width=5)
        clue = T("recessive clue", 30, PALE, weight=BOLD).move_to([3.7, 1.0, 0])
        self.play(Create(arrow), FadeIn(clue), run_time=0.75)
        self.at("small family does not prove")
        caution = chip("clue, not proof", GOLD, 30).move_to([3.7, -0.1, 0])
        self.play(FadeOut(cards.question), FadeOut(cards.chips[0]), FadeIn(caution), run_time=0.7)
        self.at("parents are carriers")
        carriers = T("parents: carriers in this model", 30, TEXT).move_to([0, -2.95, 0])
        self.play(FadeOut(cards.chips[1]), FadeIn(carriers), Indicate(VGroup(fam.dad, fam.mom), color=PALE), run_time=0.9)
        self.add(scope_tag("in this model"))
        self.finish()


class S07Test(SpokenScene):
    def construct(self):
        self.add(evidence_stage(PURPLE))
        ped = three_generation_pedigree()
        title = T("test every person", 38, TEXT, weight=BOLD).move_to([0, 2.8, 0])
        self.at("Geneticists test")
        self.play(FadeIn(title), Create(ped[0]), FadeIn(ped[1]), run_time=1.1)
        sweep = Circle(radius=0.6, color=GOLD, stroke_width=5)
        sweep.move_to(ped[1][0])
        checks = counter("checked {:.0f} / 11", ValueTracker(0), at=[4.8, -2.85, 0], size=28, color=GOLD)
        count = checks.get_center()  # keep the always-redraw object alive; tracker is replaced below
        tracker = ValueTracker(0)
        checks = counter("checked {:.0f} / 11", tracker, at=[4.8, -2.85, 0], size=28, color=GOLD)
        self.add(sweep, checks)
        path = VMobject().set_points_as_corners([p.get_center() for p in ped[1]])
        self.play(MoveAlongPath(sweep, path), tracker.animate.set_value(11), run_time=3.0, rate_func=linear)
        self.at("dominant trait usually")
        usual1 = chip("usually: each generation", PURPLE, 28).move_to([0, -2.8, 0])
        self.play(FadeOut(sweep), FadeIn(usual1), run_time=0.65)
        self.at("shaded child usually")
        usual2 = chip("usually: shaded parent", PURPLE, 28).move_to([0, -2.8, 0])
        self.play(FadeOut(checks), swap(usual1, usual2), run_time=0.65)
        self.at("new DNA change")
        question = chip("possible new change?", GOLD, 28).move_to([0, -2.8, 0])
        self.play(swap(usual2, question), Indicate(ped[1][8], color=GOLD), run_time=0.9)
        self.at("several explanations")
        several = T("small family → several explanations", 32, GOLD, weight=BOLD).move_to([0, -2.8, 0])
        self.play(swap(question, several), run_time=0.8)
        self.finish()


class S08Rule(SpokenScene):
    def construct(self):
        self.add(evidence_stage(PURPLE))
        ped = three_generation_pedigree().scale(0.86).move_to([0, 0.35, 0])
        self.add(ped)
        self.at("Alleles remain separate")
        inferred = VGroup(
            allele_tile("D", R_ALLELE, 0.62, 0.12), allele_tile("d", PALE, 0.62, 0.12)
        ).arrange(RIGHT, buff=0.25).move_to([0, -2.65, 0])
        for tile in inferred:
            tile[0].set_stroke(opacity=0.5)
        self.play(FadeIn(inferred), run_time=0.7)
        self.at("different scale")
        bracket = Brace(ped, UP, color=TEAL)
        label = T("family scale", 38, TEAL, weight=BOLD).next_to(bracket, UP, buff=0.16)
        self.play(GrowFromCenter(bracket), FadeIn(label), run_time=0.8)
        self.at("test inheritance models")
        test = chip("tests inheritance models", PURPLE, 28).move_to([-3.35, -2.75, 0])
        self.play(FadeOut(inferred), FadeIn(test), run_time=0.7)
        self.at("cannot show")
        unseen = VGroup(
            allele_tile("D", R_ALLELE, 0.62, 0.08), allele_tile("d", PALE, 0.62, 0.08)
        ).arrange(RIGHT, buff=0.25).move_to([3.45, -2.75, 0])
        for tile in unseen:
            tile[0].set_stroke(opacity=0.35)
        no = T("inferred, not seen", 28, GOLD).next_to(unseen, UP, buff=0.12)
        self.play(FadeIn(unseen), FadeIn(no), run_time=0.8)
        pulse(ped[0], base=4, amp=0.8, speed=1.4)
        self.finish()


class S09Karyotype(SpokenScene):
    def construct(self):
        self.add(evidence_stage(BLUE))
        p = person("circle", ORIGIN, shaded=True, size=2.3, color=PURPLE)
        cell = Circle(radius=2.25, color=TEAL, stroke_width=5, fill_color=TEAL, fill_opacity=0.07)
        nucleus = Circle(radius=0.95, color=BLUE, stroke_width=5, fill_color=BLUE, fill_opacity=0.12)
        self.at("zoom from a person")
        self.play(FadeIn(p), run_time=0.55)
        self.play(Transform(p, cell), run_time=0.85)
        self.at("nucleus")
        self.play(FadeIn(nucleus, scale=0.4), run_time=0.65)
        k = karyotype(False)
        rng = random.Random(21)
        scattered = k.bars.copy()
        scattered.scale(0.65)
        for pair in scattered:
            pair.move_to([rng.uniform(-0.65, 0.65), rng.uniform(-0.65, 0.65), 0]).rotate(rng.uniform(-1.0, 1.0))
        self.play(FadeIn(scattered), run_time=0.6)
        self.at("A karyotype sorts")
        self.play(FadeOut(p), FadeOut(nucleus), FadeIn(k[0]), Transform(scattered, k.bars), run_time=1.5)
        self.at("matched pairs")
        self.play(FadeIn(k[2]), FadeIn(k[3]), run_time=0.65)
        self.at("whole chromosomes")
        self.play(FadeIn(k[4]), run_time=0.55)
        self.at("Matched partners")
        pair_ring = SurroundingRectangle(k.pairs[20], color=GOLD, buff=0.16, stroke_width=4)
        self.play(Create(pair_ring), run_time=0.55)
        self.play(pair_ring.animate.move_to(k.pairs[8]), run_time=1.2)
        self.play(pair_ring.animate.move_to(k.pairs[20]), run_time=1.2)
        self.finish()


class S10Limits(SpokenScene):
    def construct(self):
        self.add(evidence_stage(BLUE))
        k = karyotype(False)
        self.add(k)
        self.at("extra chromosome")
        extra = k.extra
        total47 = M("47 total", 30, GOLD).move_to(k.total)
        self.play(FadeIn(extra, shift=UP * 0.25), swap(k.total, total47), run_time=0.8)
        tri = T("trisomy 21", 30, GOLD, weight=BOLD).next_to(k.pairs[20], DOWN, buff=0.18)
        self.play(FadeIn(tri), Indicate(VGroup(k.pairs[20], extra), color=GOLD), run_time=0.9)
        self.at("A single gene")
        gene_dot = Dot(k.pairs[8][0].get_center(), radius=0.13, color=R_ALLELE)
        gene_lab = T("ABO gene", 28, R_ALLELE, weight=BOLD).move_to([4.85, 2.82, 0])
        arrow = Arrow(gene_lab.get_left(), gene_dot.get_center(), buff=0.16, color=R_ALLELE, stroke_width=4, tip_length=0.2)
        self.play(FadeOut(k[0]), FadeIn(gene_dot), FadeIn(gene_lab), GrowArrow(arrow), run_time=0.8)
        self.at("far too small")
        self.play(gene_dot.animate.scale(0.05).set_opacity(0), FadeOut(arrow), run_time=1.1)
        invisible = chip("not visible on a karyotype", GOLD, 30, pad=0.1).move_to([0.9, 2.82, 0])
        self.play(FadeIn(invisible), run_time=0.6)
        self.at("scale -size changes")
        large = T("large change: visible", 28, BLUE).move_to([-3.85, 2.82, 0])
        self.play(FadeIn(large), Indicate(VGroup(k.pairs[20], extra), color=GOLD), run_time=0.8)
        self.at("cannot identify")
        self.play(Indicate(invisible, color=GOLD), run_time=0.9)
        self.finish()


def body_cell(label, at, color, nucleus=True):
    cell = RoundedRectangle(corner_radius=0.65, width=3.55, height=3.7, stroke_color=color, stroke_width=4,
                            fill_color=color, fill_opacity=0.06).move_to(at)
    name = T(label, 30, color, weight=BOLD).next_to(cell, UP, buff=0.16)
    nuc = Circle(radius=0.62, color=BLUE, stroke_width=4, fill_color=BLUE, fill_opacity=0.12).move_to(cell.get_center() + UP * 0.35)
    chrom = VGroup(*[
        Line([-0.17, -0.24, 0], [0.17, 0.24, 0], color=BLUE, stroke_width=5),
        Line([-0.17, 0.24, 0], [0.17, -0.24, 0], color=BLUE, stroke_width=5),
    ]).move_to(nuc)
    g = VGroup(cell, name)
    if nucleus:
        g.add(nuc, chrom)
    g.cell, g.name, g.nucleus, g.chrom = cell, name, nuc, chrom
    return g


class S11Cells(SpokenScene):
    def construct(self):
        self.add(evidence_stage(TEAL))
        skin = body_cell("skin cell", [-4.35, 0, 0], TEAL)
        muscle = body_cell("muscle cell", [0, 0, 0], PURPLE)
        third = body_cell("body cell", [4.35, 0, 0], GREY)
        self.at("Nearly every body cell")
        self.play(LaggedStart(FadeIn(skin), FadeIn(muscle), FadeIn(third), lag_ratio=0.18), run_time=1.2)
        same = T("same DNA and genes", 34, BLUE, weight=BOLD).move_to([0, -2.45, 0])
        self.play(FadeIn(same), Indicate(VGroup(skin.nucleus, muscle.nucleus, third.nucleus), color=BLUE), run_time=1.0)
        self.at("Skin and muscle")
        skin_lights = VGroup(*[Dot(radius=0.13, color=TEAL) for _ in range(3)]).arrange(RIGHT, buff=0.3).move_to(skin.cell.get_center() + DOWN * 0.85)
        muscle_lights = VGroup(*[Dot(radius=0.13, color=PURPLE) for _ in range(3)]).arrange(RIGHT, buff=0.3).move_to(muscle.cell.get_center() + DOWN * 0.85)
        self.play(FadeIn(skin_lights), run_time=0.55)
        self.at("different gene sets")
        self.play(FadeIn(muscle_lights), FadeOut(same), run_time=0.65)
        use = T("different gene sets used", 32, TEXT, weight=BOLD).move_to([0, -2.45, 0])
        self.play(FadeIn(use), run_time=0.5)
        self.at("Mature red blood cells")
        rbc = Circle(radius=1.5, color=R_ALLELE, stroke_width=5, fill_color=R_ALLELE, fill_opacity=0.14).move_to(third.cell)
        rbc_name = T("mature red blood cell", 28, R_ALLELE, weight=BOLD).move_to(third.name)
        self.play(Transform(third.cell, rbc), Transform(third.name, rbc_name), run_time=0.8)
        self.at("lose their nuclei")
        self.play(FadeOut(third.nucleus, scale=0.2), FadeOut(third.chrom, scale=0.2), run_time=1.0)
        none = T("no chromosomes to count", 28, GOLD).move_to([4.35, -2.15, 0])
        self.play(FadeOut(use), FadeIn(none), run_time=0.55)
        bob(skin_lights, amp=0.04, speed=1.5)
        bob(muscle_lights, amp=0.04, speed=1.5, seed=2)
        self.finish()


class S12Close(SpokenScene):
    def construct(self):
        self.add(evidence_stage(TEAL))
        panels = closing_panels()
        panels.scale(0.94, about_point=ORIGIN).shift(DOWN * 0.05)
        question = chip("What is the question?", GOLD, 30).move_to([0, 2.8, 0])
        self.at("Start with the question")
        self.play(FadeIn(question), run_time=0.6)
        self.at("choose the view")
        self.play(FadeIn(panels[0]), run_time=0.65)
        self.at("cross for possible")
        self.play(question.animate.move_to([-4.35, -2.6, 0]), FadeIn(panels[1]), run_time=0.85)
        self.at("pedigree for family")
        self.play(question.animate.move_to([0, -2.6, 0]), FadeIn(panels[2]), run_time=0.85)
        self.at("karyotype for whole")
        self.play(question.animate.move_to([4.35, -2.6, 0]), FadeIn(panels[3]), run_time=0.85)
        self.at("No view can answer every")
        self.play(question.animate.move_to([0, 2.8, 0]), run_time=0.75)
        question2 = chip("No single view answers everything", GOLD, 30).move_to(question)
        self.play(Transform(question, question2), run_time=0.7)
        self.at("Match the tool")
        rule = T("match the tool to the scale", 38, TEAL, weight=BOLD).move_to([0, -2.6, 0])
        self.play(FadeOut(question), FadeIn(rule), panels.animate.set_opacity(0.62), run_time=0.9)
        pulse(panels[0], base=3, amp=0.6, speed=1.2)
        self.finish()


class S13End(EndCard):
    LINE = "Each genetic tool reveals a different scale."
