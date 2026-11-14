"""When Chromosomes Miss Their Turn — chromosome-changes explainer.

COLOR MAP (fixed for the whole film)
  BLUE   one homologue
  GOLD   the other homologue
  TEAL   a chromosome segment or division currently moving
  GREEN  balanced chromosome dose
  RED    extra or missing chromosome dose / failed separation
  GREY   spindle, cells, and structural context
"""
from bp_parts import *  # noqa: F401,F403


# One carried world.  Every scene uses these exact landmarks.
SOURCE = np.array([-4.65, 0.0, 0.0])
DAUGHTERS = (np.array([-0.75, 1.45, 0.0]), np.array([-0.75, -1.45, 0.0]))
GAMETES = tuple(np.array([4.25, y, 0.0]) for y in (2.35, 0.80, -0.80, -2.35))
CELL_R, DAUGHTER_R, GAMETE_R = 1.40, 1.11, 0.70


def breathe(mob, amp=0.045, speed=2.0, seed=0):
    """A gently flexing cell membrane, large enough to register as real motion."""
    mob._breath_t = seed * 0.45
    base_w = mob.width

    def update(m, dt):
        m._breath_t += dt
        m.scale_to_fit_width(base_w * (1 + amp * np.sin(speed * m._breath_t)))
    return mob.add_updater(update)


def cell_at(point, radius, color=GREY):
    cell = Circle(radius=radius, stroke_color=color, stroke_width=4,
                  fill_color=color, fill_opacity=0.24).move_to(point)
    return breathe(cell, seed=abs(point[0] + 2 * point[1]))


def rod(color, height=1.30, width=0.22):
    return RoundedRectangle(corner_radius=width / 2, width=width, height=height,
                            stroke_color=color, stroke_width=2.5,
                            fill_color=color, fill_opacity=0.88)


def replicated_chromosome(color, center, height=1.55):
    """Two joined sister rods with a visible centromere."""
    left = rod(color, height).shift(LEFT * 0.16)
    right = rod(color, height).shift(RIGHT * 0.16)
    cent = Circle(radius=0.12, stroke_color=TEXT, stroke_width=2.5,
                  fill_color=color, fill_opacity=1.0)
    group = VGroup(left, right, cent).move_to(center)
    group.rods = VGroup(left, right)
    group.centromere = cent
    return group


def single_chromatid(color, center, height=0.82):
    return rod(color, height=height, width=0.18).move_to(center)


def spindle_lines(cell, targets):
    spindle = VGroup()
    for target in targets:
        spindle.add(DashedLine(cell.get_center(), target, dash_length=0.12,
                               color=GREY, stroke_width=2.5).set_opacity(0.65))
    return spindle


def flow_cells(include_source=True, include_daughters=True, include_gametes=True):
    g = VGroup()
    if include_source:
        g.add(cell_at(SOURCE, CELL_R))
    if include_daughters:
        g.add(*[cell_at(p, DAUGHTER_R) for p in DAUGHTERS])
    if include_gametes:
        g.add(*[cell_at(p, GAMETE_R) for p in GAMETES])
    return g


def source_pair():
    blue = replicated_chromosome(BLUE, SOURCE + LEFT * 0.34)
    gold = replicated_chromosome(GOLD, SOURCE + RIGHT * 0.34)
    return blue, gold


def predict_card():
    """Question card with the two answer chips in one row through the gap between daughters (clear of the gamete circles)."""
    q = question_card("Can sister separation repair the dose?",
                      ["REPAIR?", "IMBALANCE REMAINS?"],
                      chips_at=[0, 0, 0], y=-3.30, size=28, chip_size=22)
    q.chips.arrange(RIGHT, buff=0.25).move_to([0.0, 0.0, 0])
    return q


def first_error_backdrop(with_question=False):
    """Exact carried frame for s05 and s06."""
    cells = flow_cells()
    blue = replicated_chromosome(BLUE, DAUGHTERS[0] + LEFT * 0.27, height=1.15)
    gold = replicated_chromosome(GOLD, DAUGHTERS[0] + RIGHT * 0.27, height=1.15)
    sp = VGroup(spindle_lines(cells[1], [GAMETES[0], GAMETES[1]]),
                spindle_lines(cells[2], [GAMETES[2], GAMETES[3]]))
    pulse(sp, base=2.2, amp=0.7, speed=2.2)
    world = VGroup(cells, sp, blue, gold)
    if with_question:
        q = predict_card()
        world.add(q)
    return world


def categorical_gauge(center=(6.0, 0.0, 0.0), state="normal", scale=1.0):
    """Schematic three-state chromosome-dose gauge."""
    c = np.array(center, dtype=float)
    ys = {"extra": 0.72, "normal": 0.0, "missing": -0.72}
    cols = {"extra": RED, "normal": GREEN, "missing": RED}
    rail = Line(c + DOWN * 0.90, c + UP * 0.90, color=GREY, stroke_width=5)
    ticks = VGroup(*[Line(c + LEFT * 0.12 + UP * y, c + RIGHT * 0.12 + UP * y,
                               color=GREY, stroke_width=3) for y in ys.values()])
    label_size = max(28, int(np.ceil(25 / scale)))
    labels = VGroup(*[T(name.upper(), label_size, cols[name]).move_to(c + RIGHT * 1.65 + UP * y)
                      for name, y in ys.items()])
    pointer = Triangle(color=cols[state], fill_color=cols[state], fill_opacity=1,
                       stroke_width=0).scale(0.10).rotate(-PI / 2)
    pointer.move_to(c + LEFT * 0.25 + UP * ys[state])
    g = VGroup(rail, ticks, labels, pointer).scale(scale, about_point=c)
    g.pointer = pointer
    return g


def product_row(kind, y, x0=-4.8, gap=3.15, radius=0.52):
    """Four identical-position bins for the MI/MII comparison."""
    bins = VGroup(*[cell_at([x0 + i * gap, y, 0], radius) for i in range(4)])
    contents = VGroup()
    if kind == "mi":
        for i in (0, 1):
            contents.add(single_chromatid(BLUE, bins[i].get_center() + LEFT * 0.13, 0.68),
                         single_chromatid(GOLD, bins[i].get_center() + RIGHT * 0.13, 0.68))
    elif kind == "mii":
        contents.add(single_chromatid(BLUE, bins[0].get_center() + LEFT * 0.13, 0.68),
                     single_chromatid(BLUE, bins[0].get_center() + RIGHT * 0.13, 0.68),
                     single_chromatid(GOLD, bins[2].get_center(), 0.68),
                     single_chromatid(GOLD, bins[3].get_center(), 0.68))
    return VGroup(bins, contents)


class S00Hook(SpokenScene):
    def construct(self):
        question = fit_text("How can one missed separation create extra and missing material?",
                            max_w=11.7, size=34, color=TEXT, max_lines=2).move_to([0, 3.15, 0])
        cell = cell_at([0, 0.45, 0], 1.65)
        blue = replicated_chromosome(BLUE, [-0.48, 0.45, 0], 2.25)
        gold = replicated_chromosome(GOLD, [0.48, 0.45, 0], 2.25)
        pole = Dot([1.25, 0.45, 0], radius=0.09, color=GREY)
        spindle = VGroup(*[DashedLine(pole, c.centromere, color=GREY, stroke_width=3,
                                      dash_length=0.14) for c in (blue, gold)])
        gametes = VGroup(*[cell_at([x, -2.55, 0], 0.48) for x in (-2.4, -0.8, 0.8, 2.4)])
        bob(blue, amp=0.045, speed=5.0, seed=1)
        bob(gold, amp=0.045, speed=5.4, seed=3)
        pulse(spindle, base=3.0, amp=0.8, speed=2.5)
        self.play(FadeIn(cell), FadeIn(blue), FadeIn(gold),
                  FadeIn(pole), Create(spindle), run_time=1.4)
        self.at("one gamete extra")
        self.play(FadeIn(gametes, shift=UP * 0.18), run_time=0.8)
        self.at("another too little")
        self.play(FadeIn(question, shift=DOWN * 0.12),
                  Indicate(VGroup(blue, gold), color=RED), run_time=0.9)
        self.at("Watch one replicated")
        self.play(VGroup(blue, gold).animate.scale(1.07), rate_func=there_and_back,
                  run_time=1.1)
        self.at("both myotic divisions")
        self.play(Indicate(gametes, color=TEAL), run_time=1.0)
        self.finish()


class S01Title(TitleCard):
    TITLE = "When Chromosomes Miss Their Turn"
    LESSON = "Chromosome changes"


class S02Parts(SpokenScene):
    def construct(self):
        cells = flow_cells()
        pulse(cells, base=4.0, amp=1.1, speed=1.8)
        blue, gold = source_pair()
        self.play(FadeIn(cells[0]), FadeIn(blue), FadeIn(gold), run_time=1.1)
        self.at("joined sister chromatids")
        self.play(Indicate(blue.rods, color=BLUE), Indicate(gold.rods, color=GOLD), run_time=0.9)
        sisters = T("joined sister chromatids", 28, TEXT).move_to([-3.0, -2.75, 0])
        self.play(FadeIn(sisters), run_time=0.5)
        self.at("Blue marks")
        blue_lab = T("blue homologue", 28, BLUE).move_to([-4.8, 2.15, 0])
        self.play(FadeOut(sisters), FadeIn(blue_lab), Indicate(blue, color=BLUE), run_time=0.7)
        self.at("gold marks")
        gold_lab = T("gold homologue", 28, GOLD).move_to([-4.8, -2.15, 0])
        self.play(FadeIn(gold_lab), Indicate(gold, color=GOLD), run_time=0.7)
        self.at("centromeres remain visible")
        cent_lab = T("centromeres", 28, TEXT).move_to([-2.45, 2.45, 0])
        cent_lines = VGroup(*[Line(cent_lab.get_bottom() + DOWN * 0.1, c.centromere.get_top(), color=GREY,
                                   stroke_width=2) for c in (blue, gold)])
        self.play(FadeOut(blue_lab), FadeOut(gold_lab), FadeIn(cent_lab), Create(cent_lines), run_time=0.8)
        self.at("meiosis one")
        mi = chip("MEIOSIS I", TEAL, 28).move_to([-0.75, 3.15, 0])
        sp1 = spindle_lines(cells[0], DAUGHTERS)
        self.play(FadeOut(cent_lab), FadeOut(cent_lines), FadeIn(cells[1:3]), FadeIn(mi),
                  Create(sp1), blue.animate.move_to(DAUGHTERS[0]),
                  gold.animate.move_to(DAUGHTERS[1]), run_time=1.5)
        self.at("meiosis two")
        mii = chip("MEIOSIS II", TEAL, 28).move_to([2.55, 3.15, 0])
        sp2 = VGroup(spindle_lines(cells[1], GAMETES[:2]), spindle_lines(cells[2], GAMETES[2:]))
        self.play(FadeOut(cells[0]), FadeOut(sp1), FadeIn(cells[3:]), FadeIn(mii), Create(sp2), run_time=0.9)
        self.at("sisters normally separate")
        blue_parts = VGroup(single_chromatid(BLUE, GAMETES[0]), single_chromatid(BLUE, GAMETES[1]))
        gold_parts = VGroup(single_chromatid(GOLD, GAMETES[2]), single_chromatid(GOLD, GAMETES[3]))
        self.play(FadeOut(blue), FadeOut(gold), FadeIn(blue_parts), FadeIn(gold_parts), run_time=1.4)
        self.at("first division sorts")
        self.play(Indicate(VGroup(cells[1], cells[2]), color=TEAL), run_time=0.8)
        self.at("second sorts copies")
        self.play(Indicate(VGroup(*cells[3:]), color=TEAL), run_time=0.8)
        self.finish()


class S03Terms(SpokenScene):
    def construct(self):
        source = cell_at(SOURCE, CELL_R)
        blue, gold = source_pair()
        daughters = VGroup(*[cell_at(p, DAUGHTER_R) for p in DAUGHTERS])
        pulse(daughters, base=4.0, amp=1.1, speed=1.8)
        sp = spindle_lines(source, DAUGHTERS)
        pulse(sp, base=2.5, amp=0.7, speed=2.2)
        self.play(FadeIn(source), FadeIn(blue), FadeIn(gold), FadeIn(daughters), Create(sp), run_time=1.0)
        self.at("fail to part")
        fail = chip("NONDISJUNCTION", RED, 30).move_to([0.2, 3.1, 0])
        self.play(FadeIn(fail), VGroup(blue, gold).animate.move_to(DAUGHTERS[0]), run_time=1.2)
        self.at("resulting gamete")
        gametes = VGroup(*[cell_at(p, GAMETE_R) for p in GAMETES])
        self.play(FadeOut(source), FadeOut(sp), FadeIn(gametes), run_time=0.8)
        extra = VGroup(single_chromatid(BLUE, GAMETES[0] + LEFT * 0.13),
                       single_chromatid(GOLD, GAMETES[0] + RIGHT * 0.13))
        self.at("extra chromosome")
        gauge = categorical_gauge([1.20, 0, 0], "extra", 0.82)
        self.play(FadeIn(extra), FadeIn(gauge), run_time=0.8)
        self.at("none of that chromosome")
        missing_ring = Circle(radius=GAMETE_R, color=RED, stroke_width=5).move_to(GAMETES[3])
        self.play(Create(missing_ring), gauge.pointer.animate.shift(DOWN * 1.18), run_time=0.8)
        self.at("This is aneuploidy")
        aneu = chip("ANEUPLOIDY", RED, 30).move_to([0.4, -3.1, 0])
        self.play(swap(fail, aneu), run_time=0.8)
        self.at("individual chromosomes")
        self.play(Indicate(VGroup(extra, missing_ring), color=RED), run_time=0.8)
        self.add(scope_tag("schematic"))
        self.finish()


class S04FirstError(SpokenScene):
    def construct(self):
        cells = flow_cells()
        pulse(cells, base=4.0, amp=1.2, speed=1.8)
        blue, gold = source_pair()
        self.play(FadeIn(cells), FadeIn(blue), FadeIn(gold), run_time=0.9)
        self.at("travel together")
        sp = spindle_lines(cells[0], DAUGHTERS)
        pulse(sp, base=2.5, amp=1.2, speed=2.0)
        self.play(Create(sp), blue.animate.move_to(DAUGHTERS[0] + LEFT * 0.27),
                  gold.animate.move_to(DAUGHTERS[0] + RIGHT * 0.27), run_time=1.5)
        self.at("receives blue and gold")
        extra = categorical_gauge([1.45, 1.45, 0], "extra", 0.55)
        self.play(FadeIn(extra), Indicate(VGroup(blue, gold), color=RED), run_time=0.9)
        self.at("other receives neither")
        missing = categorical_gauge([1.45, -1.45, 0], "missing", 0.55)
        self.play(FadeIn(missing), Indicate(cells[2], color=RED), run_time=0.9)
        self.at("sister chromatids remain joined")
        self.play(Indicate(blue.rods, color=BLUE), Indicate(gold.rods, color=GOLD), run_time=0.9)
        self.at("already created")
        self.play(extra.animate.scale(1.08), missing.animate.scale(1.08),
                  rate_func=there_and_back, run_time=1.0)
        self.finish()


class S05Predict(SpokenScene):
    def construct(self):
        world = first_error_backdrop()
        self.add(world)
        self.at("meiosis II runs normally")
        self.play(Indicate(world[1], color=TEAL), run_time=1.0)
        self.at("Can separating")
        q = predict_card()
        self.play(FadeIn(q.chips), run_time=0.6)
        self.at("final pattern")
        self.play(FadeIn(q.question), run_time=0.7)
        self.finish()


class S06Pause(PredictPause):
    SECONDS = 4.5
    RING_AT = [6.0, -3.15, 0]

    def backdrop(self):
        return first_error_backdrop()

    def construct(self):
        self.add(self.backdrop())
        self.add(predict_card())
        ring, run = countdown(self.SECONDS, center=self.RING_AT)
        self.add(ring)
        self.play(run)
        self.finish()


class S07FirstReveal(SpokenScene):
    def construct(self):
        world = first_error_backdrop()
        cells, sp, blue, gold = world
        self.add(world)
        no_repair = chip("IMBALANCE REMAINS", RED, 28).move_to([1.1, 0, 0])
        self.play(FadeIn(no_repair), run_time=0.7)
        self.at("cannot replace")
        self.play(Indicate(cells[2], color=RED), run_time=0.8)
        self.at("Normal sister separation")
        products = VGroup(single_chromatid(BLUE, GAMETES[0] + LEFT * 0.13),
                          single_chromatid(GOLD, GAMETES[0] + RIGHT * 0.13),
                          single_chromatid(BLUE, GAMETES[1] + LEFT * 0.13),
                          single_chromatid(GOLD, GAMETES[1] + RIGHT * 0.13))
        self.play(FadeOut(no_repair), FadeOut(blue), FadeOut(gold), FadeIn(products), run_time=1.3)
        self.at("matching outcomes")
        brackets = VGroup(SurroundingRectangle(VGroup(cells[3], cells[4]), color=RED, buff=0.12,
                                               corner_radius=0.12),
                          SurroundingRectangle(VGroup(cells[5], cells[6]), color=RED, buff=0.12,
                                               corner_radius=0.12))
        self.play(Create(brackets), run_time=0.9)
        self.at("carry both homologues")
        self.play(Indicate(VGroup(cells[3], cells[4], products), color=RED), run_time=0.9)
        self.at("carry neither")
        self.play(Indicate(VGroup(cells[5], cells[6]), color=RED), run_time=0.9)
        self.at("counts appear")
        labels = VGroup(chip("2 DISOMIC", RED, 28).move_to([1.85, 1.45, 0]),
                        chip("2 NULLISOMIC", RED, 28).move_to([2.1, -1.45, 0]))
        self.play(FadeOut(brackets), FadeOut(sp), FadeIn(labels), run_time=0.8)
        self.finish()


class S08SecondError(SpokenScene):
    def construct(self):
        cells = flow_cells()
        pulse(cells, base=4.0, amp=1.1, speed=1.8)
        blue, gold = source_pair()
        self.play(FadeIn(cells), FadeIn(blue), FadeIn(gold), run_time=0.8)
        self.at("normal meiosis I")
        sp1 = spindle_lines(cells[0], DAUGHTERS)
        self.play(Create(sp1), blue.animate.move_to(DAUGHTERS[0]),
                  gold.animate.move_to(DAUGHTERS[1]), run_time=1.3)
        self.at("different daughter cells")
        self.play(Indicate(VGroup(cells[1], cells[2]), color=GREEN), run_time=0.8)
        self.at("meiosis II")
        sp2 = VGroup(spindle_lines(cells[1], GAMETES[:2]), spindle_lines(cells[2], GAMETES[2:]))
        self.play(FadeOut(cells[0]), FadeOut(sp1), Create(sp2), run_time=0.7)
        self.at("blue sisters fail")
        blue_pair = VGroup(single_chromatid(BLUE, GAMETES[0] + LEFT * 0.13),
                           single_chromatid(BLUE, GAMETES[0] + RIGHT * 0.13))
        self.play(FadeOut(blue), FadeIn(blue_pair),
                  cells[3].animate.set_stroke(RED, width=5),
                  cells[4].animate.set_stroke(RED, width=5), run_time=1.2)
        self.at("Gold sisters")
        gold_parts = VGroup(single_chromatid(GOLD, GAMETES[2]), single_chromatid(GOLD, GAMETES[3]))
        self.play(FadeOut(gold), FadeIn(gold_parts),
                  cells[5].animate.set_stroke(GREEN, width=5),
                  cells[6].animate.set_stroke(GREEN, width=5), run_time=1.2)
        self.at("other cell")
        self.play(Indicate(VGroup(cells[5], cells[6], gold_parts), color=GREEN), run_time=0.8)
        self.finish()


class S09Compare(SpokenScene):
    def construct(self):
        mi = product_row("mi", 1.65)
        mii = product_row("mii", -1.5)
        mi_title = T("MI: 2 extra  |  2 missing", 30, RED).move_to([0, 2.85, 0])
        mii_title = T("MII: 1 extra  |  1 missing  |  2 normal", 30, TEXT).move_to([0, -2.6, 0])
        self.play(FadeIn(mi), FadeIn(mi_title), run_time=1.0)
        self.at("three dose classes")
        self.play(FadeIn(mii), FadeIn(mii_title), run_time=1.1)
        extra = Circle(radius=0.61, color=RED, stroke_width=5).move_to(mii[0][0])
        self.at("extra material")
        self.play(Create(extra), run_time=0.7)
        missing = Circle(radius=0.61, color=RED, stroke_width=5).move_to(mii[0][1])
        self.at("missing it")
        self.play(Create(missing), run_time=0.7)
        normals = VGroup(*[Circle(radius=0.61, color=GREEN, stroke_width=5).move_to(mii[0][i])
                           for i in (2, 3)])
        self.at("remaining products are normal")
        self.play(Create(normals), run_time=0.8)
        self.at("stage of the mist separation")
        bracket = Brace(mi, LEFT, color=TEAL)
        bracket2 = Brace(mii, LEFT, color=TEAL)
        self.play(GrowFromCenter(bracket), run_time=0.5)
        self.play(Transform(bracket, bracket2), run_time=1.0)
        self.at("product pattern")
        self.play(Indicate(VGroup(mi_title, mii_title), color=TEAL), run_time=0.8)
        self.at("DNA markers")
        note = caption("The product pattern leaves a readable fingerprint.", color=TEXT)
        self.play(FadeOut(extra), FadeOut(missing), FadeOut(normals), FadeIn(note), run_time=0.8)
        self.finish()


class S10Zygote(SpokenScene):
    def construct(self):
        left_g = cell_at([-3.8, 1.2, 0], 0.92, RED)
        right_g = cell_at([-3.8, -1.35, 0], 0.92, RED)
        disomic = VGroup(single_chromatid(BLUE, [-3.97, 1.2, 0], 1.05),
                         single_chromatid(GOLD, [-3.63, 1.2, 0], 1.05))
        normal = single_chromatid(GREY, [-0.7, 1.2, 0], 1.05)
        egg = cell_at([-0.7, 1.2, 0], 0.92)
        self.play(FadeIn(left_g), FadeIn(right_g), FadeIn(disomic), FadeIn(egg), FadeIn(normal), run_time=1.0)
        self.at("contributes one copy")
        self.play(Indicate(normal, color=GREEN), run_time=0.8)
        self.at("extra material")
        tri_cell = cell_at([3.25, 1.2, 0], 1.15, RED)
        tri_rods = VGroup(single_chromatid(BLUE, [2.9, 1.2, 0], 1.35),
                          single_chromatid(GOLD, [3.25, 1.2, 0], 1.35),
                          single_chromatid(GREY, [3.6, 1.2, 0], 1.35))
        self.play(FadeIn(tri_cell), Transform(disomic.copy(), tri_rods[:2]),
                  normal.animate.move_to([3.6, 1.2, 0]), run_time=1.2)
        self.at("trisomic zygote")
        tri_label = chip("TRISOMY", RED, 30).move_to([5.0, 2.9, 0])
        self.play(FadeIn(tri_rods[:2]), FadeIn(tri_label), run_time=0.7)
        empty = Circle(radius=0.32, color=RED, stroke_width=4).move_to(right_g)
        normal2 = single_chromatid(GREY, [-0.7, -1.35, 0], 1.05)
        self.at("missing that chromosome")
        self.play(Create(empty), FadeIn(normal2), run_time=0.8)
        mono_cell = cell_at([3.25, -1.35, 0], 1.15, RED)
        mono_rod = single_chromatid(GREY, [3.25, -1.35, 0], 1.35)
        self.play(FadeIn(mono_cell), normal2.animate.move_to(mono_rod), run_time=1.0)
        self.at("monosomic zygote")
        mono_label = chip("MONOSOMY", RED, 30).move_to([5.0, -2.9, 0])
        self.play(FadeIn(mono_label), run_time=0.7)
        self.at("zygote divides")
        daughters = VGroup(cell_at([2.45, -1.35, 0], 0.72, RED),
                           cell_at([4.05, -1.35, 0], 0.72, RED))
        copies = VGroup(single_chromatid(GREY, [2.45, -1.35, 0], 0.9),
                        single_chromatid(GREY, [4.05, -1.35, 0], 0.9))
        self.play(FadeOut(mono_cell), FadeOut(normal2), FadeIn(daughters), FadeIn(copies), run_time=1.2)
        self.finish()


class S11Dose(SpokenScene):
    def construct(self):
        chroms = VGroup()
        for x, col in zip((-1.0, 0.0, 1.0), (BLUE, GOLD, GREY)):
            body = rod(col, height=4.35, width=0.34).move_to([x, 0.35, 0])
            genes = VGroup(*[Rectangle(width=0.52, height=0.14, stroke_width=0,
                                       fill_color=TEXT, fill_opacity=1).move_to([x, y, 0])
                             for y in (-1.05, -0.35, 0.35, 1.05, 1.75)])
            chroms.add(VGroup(body, genes))
        self.play(FadeIn(chroms[0]), run_time=0.6)
        self.at("many genes together")
        self.play(FadeIn(chroms[1]), FadeIn(chroms[2]), run_time=1.2)
        gauge = categorical_gauge([3.00, 0.35, 0], "normal", 1.05)
        self.play(FadeIn(gauge), run_time=0.5)
        self.at("alter development")
        self.play(gauge.pointer.animate.shift(UP * 0.76), Indicate(chroms, color=RED), run_time=1.0)
        self.at("Most aneuploid")
        timeline = Line([-4.6, -2.65, 0], [4.7, -2.65, 0], color=GREY, stroke_width=10)
        ticks = VGroup(*[Dot([x, -2.65, 0], radius=0.09, color=GREY) for x in (-4.0, -1.2, 1.6, 4.4)])
        vary = scope_tag("outcomes vary")
        paths = VGroup(*[Arrow([-3.8, -2.40 + 0.18 * i, 0], [0.4 + 0.45 * i, -2.40 + 0.18 * i, 0],
                                     buff=0, color=GREY, stroke_width=12, tip_length=0.18)
                         for i in range(4)])
        progress = RoundedRectangle(corner_radius=0.16, width=9.2, height=0.82,
                                    stroke_width=0, fill_color=TEAL, fill_opacity=0.24).move_to([0.05, -2.22, 0])
        self.play(chroms.animate.scale(0.58).move_to([-3.8, 0.7, 0]),
                  FadeOut(gauge), Create(timeline), FadeIn(ticks), FadeIn(vary),
                  *[GrowArrow(p) for p in paths], GrowFromEdge(progress, LEFT), run_time=2.0)
        self.at("do not survive pregnancy")
        self.play(paths[:3].animate.set_opacity(0.08).shift(LEFT * 0.35),
                  progress.animate.stretch_to_fit_width(3.6).align_to(timeline, LEFT).set_opacity(0.08),
                  run_time=1.6)
        self.at("Trisomy 21")
        path21 = Arrow([-3.8, -1.9, 0], [4.4, -1.9, 0], buff=0, color=TEAL,
                       stroke_width=5, tip_length=0.18)
        label21 = chip("TRISOMY 21", TEAL, 28).move_to([2.55, -1.2, 0])
        self.play(GrowArrow(path21), FadeIn(label21), run_time=1.0)
        self.at("regularly at birth")
        self.play(Indicate(label21, color=TEAL), run_time=0.8)
        self.finish()


class S12Rule(SpokenScene):
    def construct(self):
        mi = product_row("mi", 0.0, x0=-5.25, gap=1.45, radius=0.50)
        pair = VGroup(replicated_chromosome(BLUE, [-0.32, 2.15, 0], 1.45),
                      replicated_chromosome(GOLD, [0.32, 2.15, 0], 1.45))
        self.play(FadeIn(pair), FadeIn(mi), run_time=1.0)
        self.at("product pattern")
        pattern = chip("PRODUCT PATTERN", TEAL, 30).move_to([-3.7, -2.05, 0])
        p0 = pair.get_left() + LEFT * 0.15
        arrow1 = VGroup(Line(p0, [-6.4, p0[1], 0], color=GREY, stroke_width=4),
                        Line([-6.4, p0[1], 0], [-6.4, -2.05, 0], color=GREY, stroke_width=4),
                        Arrow([-6.4, -2.05, 0], pattern.get_left(), color=GREY,
                              stroke_width=4, buff=0.08, tip_length=0.18))
        self.play(FadeIn(arrow1), FadeIn(pattern), Indicate(mi, color=TEAL), run_time=1.1)
        self.at("DNA dose")
        gauges = VGroup(categorical_gauge([1.20, 0.15, 0], "extra", 0.70),
                        categorical_gauge([3.75, 0.15, 0], "missing", 0.70))
        self.play(FadeIn(gauges), run_time=0.8)
        self.at("matters biologically")
        consequence = chip("BIOLOGICAL CONSEQUENCES", RED, 28).move_to([3.35, -2.05, 0])
        arrow2 = Arrow(gauges.get_bottom(), consequence.get_top(), color=GREY,
                       stroke_width=4, buff=0.12, tip_length=0.18)
        self.play(GrowArrow(arrow2), FadeIn(consequence), run_time=1.0)
        self.at("questions separate")
        self.play(pattern.animate.set_stroke(TEAL, width=5),
                  consequence.animate.set_stroke(RED, width=5), run_time=0.8)
        self.at("Where did separation fail")
        self.play(Indicate(arrow1, color=TEAL), run_time=0.8)
        self.at("what chromosome material")
        self.play(Indicate(gauges, color=RED), run_time=0.8)
        self.at("different routes")
        surround = SurroundingRectangle(VGroup(pair, pattern, consequence), color=GOLD,
                                        buff=0.18, corner_radius=0.18)
        self.play(Create(surround), run_time=1.0)
        self.finish()


class S13End(EndCard):
    LINE = "Chromosome-number changes matter through DNA dose."
