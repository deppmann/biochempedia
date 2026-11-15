"""Reading a Tumor Family Tree — chapter 2.

COLOR MAP (shared with chapter 1 and fixed for this chapter)
  PALE/GRAY = ordinary cells, ordinary DNA, outlines
  CLAY      = somatic change and tumor lineage
  GOLD      = germline change
  GREEN     = working suppressor
  RED       = lost function
  TEAL      = sequencing reads
  BLUE      = intentionally unused
"""
import numpy as np
from bp_parts import *  # noqa: F401,F403


CLAY = "#F29E4C"
PALE = "#D7D9DB"


def arrow(a, b, color=GREY, width=4, buff=0.08):
    return Arrow(a, b, buff=buff, color=color, stroke_width=width,
                 tip_length=0.20, max_tip_length_to_length_ratio=0.35)


def marker(kind="circle", color=CLAY, filled=True, size=0.23):
    if kind == "square":
        return Square(side_length=size * 1.7, stroke_color=color, stroke_width=3,
                      fill_color=color, fill_opacity=0.15 if not filled else 1)
    return Circle(radius=size, stroke_color=color, stroke_width=3,
                  fill_color=color, fill_opacity=1 if filled else 0.15)


TREE_POINTS = [
    (-5.25, 0.0), (-3.05, 1.45), (-3.05, -1.45),
    (-0.45, 2.45), (-0.45, 0.82), (-0.45, -0.82), (-0.45, -2.45),
]
TREE_LINKS = [(0, 1), (0, 2), (1, 3), (1, 4), (2, 5), (2, 6)]


def lineage_cell(point, scale=1.0, ordinary=False):
    col = PALE if ordinary else CLAY
    box = RoundedRectangle(corner_radius=0.16 * scale, width=1.34 * scale, height=1.04 * scale,
                           stroke_color=col, stroke_width=3, fill_color=col,
                           fill_opacity=0.16 if ordinary else 0.35).move_to([*point, 0])
    dna = VGroup(
        RoundedRectangle(corner_radius=0.04, width=0.12 * scale, height=0.42 * scale,
                         stroke_width=0, fill_color=PALE, fill_opacity=1),
        RoundedRectangle(corner_radius=0.04, width=0.12 * scale, height=0.42 * scale,
                         stroke_width=0, fill_color=GREEN, fill_opacity=1),
    ).arrange(RIGHT, buff=0.14 * scale).move_to(box)
    g = VGroup(box, dna)
    g.box, g.dna = box, dna
    return g


def family_tree(circle_badges=True, square_badges=False, gold_badges=False):
    """The carried world; every tree scene calls this at the same scale and position."""
    cells = VGroup(*[lineage_cell(p) for p in TREE_POINTS])
    links = VGroup(*[
        arrow(cells[a].get_right(), cells[b].get_left(), CLAY, 3, 0.12)
        for a, b in TREE_LINKS
    ])
    circles = VGroup()
    squares = VGroup()
    golds = VGroup()
    if circle_badges:
        for c in cells:
            circles.add(marker().move_to(c.get_center() + UP * 0.20))
    if square_badges:
        for i in (2, 5, 6):
            squares.add(marker("square", filled=False, size=0.17).move_to(cells[i].get_center() + DOWN * 0.20))
    if gold_badges:
        for c in cells:
            golds.add(marker(color=GOLD, size=0.11).move_to(c.get_center() + LEFT * 0.31 + DOWN * 0.20))
    g = VGroup(links, cells, circles, squares, golds)
    g.links, g.cells, g.circles, g.squares, g.golds = links, cells, circles, squares, golds
    return g


def branch_motion(tree):
    """Barely visible living motion without moving the carried geometry itself."""
    for i, c in enumerate(tree.cells):
        pulse(c.box, base=3.0, amp=0.35, speed=1.2 + 0.08 * i)
        c.box._fill_t = i * 0.37

        def breathe(m, dt):
            m._fill_t += dt
            m.set_fill(CLAY, opacity=0.34 + 0.10 * np.sin(1.05 * m._fill_t))
        c.box.add_updater(breathe)
        bob(c.dna, amp=0.055, speed=1.1, seed=i)
    for i, m in enumerate(list(tree.circles) + list(tree.squares) + list(tree.golds)):
        bob(m, amp=0.05, speed=1.2, seed=i)
    return tree


def sample_tube(center, title, width=4.5, height=4.7):
    x, y, _ = center
    body = RoundedRectangle(corner_radius=0.28, width=width, height=height,
                            stroke_color=PALE, stroke_width=3, fill_color=TEAL,
                            fill_opacity=0.16).move_to(center)
    rim = Line([x - width * 0.38, y + height / 2, 0], [x + width * 0.38, y + height / 2, 0],
               color=PALE, stroke_width=6)
    label = T(title, 30, PALE).next_to(body, UP, buff=0.16)
    g = VGroup(body, rim, label)
    g.body, g.label = body, label
    return g


def read_tile(color=TEAL, filled=False, width=0.72):
    return RoundedRectangle(corner_radius=0.07, width=width, height=0.22,
                            stroke_color=color, stroke_width=3, fill_color=color,
                            fill_opacity=1 if filled else 0.12)


def read_column(x, y0=-1.55, n=6, variant=None, seed=0):
    ys = np.linspace(y0, y0 + 3.0, n)
    reads = VGroup()
    for i, y in enumerate(ys):
        col = variant if i == 2 and variant else TEAL
        reads.add(read_tile(col, filled=bool(variant and i == 2)).move_to([x + (0.16 if i % 2 else -0.16), y, 0]))
    for i, tile in enumerate(reads):
        base_y = tile.get_y()
        tile._drift_t = seed * 0.31 + i * 0.42

        def drift(m, dt, base_y=base_y):
            m._drift_t += dt
            m.set_y(base_y + 0.09 * np.sin(0.9 * m._drift_t))
        tile.add_updater(drift)
    return reads


def tube_pair(clay=False, gold=False, narrow=False):
    if narrow:
        left = sample_tube([3.0, 0.65, 0], "tumor", 2.0, 3.5)
        right = sample_tube([5.35, 0.65, 0], "matched\nnormal", 2.0, 3.5)
        lx, rx = 3.0, 5.35
    else:
        left = sample_tube([-3.25, 0.25, 0], "tumor")
        right = sample_tube([3.25, 0.25, 0], "matched normal")
        lx, rx = -3.25, 3.25
    lv = GOLD if gold else (CLAY if clay else None)
    rv = GOLD if gold else None
    y0 = -0.75 if narrow else -1.55
    lreads = read_column(lx, y0=y0, variant=lv, seed=1)
    rreads = read_column(rx, y0=y0, variant=rv, seed=4)
    g = VGroup(left, right, lreads, rreads)
    g.tumor, g.normal, g.tumor_reads, g.normal_reads = left, right, lreads, rreads
    return g


def predict_world():
    return tube_pair(gold=True).shift(UP * 0.45)


def predict_card():
    return question_card("When did the gold variant enter?",
                         ["before tumor lineage", "after one tumor branch"],
                         y=-3.25, size=30)


def mixed_tip_tube():
    body = RoundedRectangle(corner_radius=0.30, width=1.55, height=6.05,
                            stroke_color=TEAL, stroke_width=3, fill_color=TEAL,
                            fill_opacity=0.05).move_to([-0.45, 0, 0])
    rim = Line([-0.98, 3.02, 0], [0.08, 3.02, 0], color=TEAL, stroke_width=6)
    return VGroup(body, rim)


class S00Hook(SpokenScene):
    def construct(self):
        tree = family_tree(circle_badges=False)
        root = tree.cells[0]
        self.at("The first film followed")
        self.play(FadeIn(root), run_time=0.7)
        self.play(Create(tree.links), FadeIn(tree.cells[1:]), run_time=2.2)
        branch_motion(tree)
        self.at("How can mixed")
        question = fit_text("Which lineage carries the change?", max_w=4.5, size=34, color=TEAL,
                            max_lines=2).move_to([3.6, 1.15, 0])
        reads = VGroup(*[read_tile().move_to([3.0 + (i % 3) * 0.75, -0.55 - (i // 3) * 0.52, 0])
                         for i in range(6)])
        self.play(FadeIn(reads, shift=UP * 0.15), FadeIn(question), run_time=0.8)
        self.at("Start with that same")
        self.play(Indicate(tree.cells, color=CLAY, scale_factor=1.02), run_time=0.8)
        self.at("An early clay marker")
        badge = marker().move_to(root.get_center() + UP * 0.20)
        self.play(FadeIn(badge, scale=0.5), run_time=0.5)
        self.at("Every later branch")
        copies = VGroup(*[marker().move_to(c.get_center() + UP * 0.20) for c in tree.cells[1:]])
        self.play(*[TransformFromCopy(badge, m) for m in copies], run_time=1.4)
        for i, m in enumerate(copies):
            bob(m, amp=0.025, speed=1.2, seed=i)
        self.finish()


class S01Title(TitleCard):
    LESSON = "Cancer as a Genetic Disease"
    TITLE = "Reading a Tumor Family Tree"


class S02Subclone(SpokenScene):
    def construct(self):
        tree = family_tree(circle_badges=True)
        self.add(tree)
        branch_motion(tree)
        self.at("Later, one branch")
        square0 = marker("square", filled=False, size=0.17).move_to(tree.cells[2].get_center() + DOWN * 0.20)
        self.play(FadeIn(square0), run_time=0.5)
        self.at("Only that branch")
        descendants = VGroup(*[
            marker("square", filled=False, size=0.17).move_to(tree.cells[i].get_center() + DOWN * 0.20)
            for i in (5, 6)
        ])
        self.play(*[TransformFromCopy(square0, m) for m in descendants], run_time=0.9)
        self.at("so it is a subclone")
        sub = boxed_label("subclonal", CLAY, 28).move_to([3.4, -1.35, 0])
        sub_arrow = arrow(sub.get_left(), tree.cells[5].get_right(), CLAY, 3, 0.12)
        self.play(FadeIn(sub), GrowArrow(sub_arrow), run_time=0.6)
        self.at("The trunk marker")
        clonal = boxed_label("clonal", CLAY, 28).move_to([3.4, 1.15, 0])
        clonal_arrow = arrow(clonal.get_left(), tree.cells[3].get_right(), CLAY, 3, 0.12)
        self.play(FadeIn(clonal), GrowArrow(clonal_arrow), run_time=0.6)
        self.at("The pattern records ancestry")
        tube = mixed_tip_tube()
        self.play(FadeOut(sub_arrow), FadeOut(clonal_arrow), FadeOut(sub), FadeOut(clonal),
                  FadeIn(tube), run_time=0.7)
        self.at("sample mixes all branches")
        mix = T("mixed sample", 30, TEAL).move_to([3.6, 0, 0])
        faint = VGroup(*[arrow(c.get_right(), [2.25, 0.45 - i * 0.18, 0], TEAL, 2, 0.04)
                         for i, c in enumerate(tree.cells[3:])]).set_opacity(0.38)
        self.play(FadeIn(faint), FadeIn(mix), run_time=0.7)
        self.finish()


class S03MatchedNormal(SpokenScene):
    def construct(self):
        pair = tube_pair()
        self.at("Now place a matched")
        self.play(FadeIn(pair.tumor), FadeIn(pair.normal), run_time=0.8)
        self.play(FadeIn(pair.tumor_reads), FadeIn(pair.normal_reads), run_time=0.7)
        self.at("same person")
        same = T("same person • often blood", 28, PALE).move_to([0, 3.35, 0])
        self.play(FadeIn(same), run_time=0.5)
        self.at("A variant found only")
        clay = read_tile(CLAY, True).move_to(pair.tumor_reads[2])
        self.play(Transform(pair.tumor_reads[2], clay), run_time=0.5)
        self.at("usually somatic")
        somatic = boxed_label("usually somatic", CLAY, 28).move_to([-3.25, -2.55, 0])
        self.play(FadeIn(somatic), run_time=0.5)
        self.at("A variant found in both")
        gold_l = read_tile(GOLD, True).move_to(pair.tumor_reads[4])
        gold_r = read_tile(GOLD, True).move_to(pair.normal_reads[4])
        self.play(Transform(pair.tumor_reads[4], gold_l), Transform(pair.normal_reads[4], gold_r), run_time=0.6)
        self.at("usually germline")
        germline = boxed_label("usually germline", GOLD, 28).move_to([3.25, -2.55, 0])
        self.play(FadeIn(germline), run_time=0.5)
        self.at("The word usually matters")
        self.play(Indicate(VGroup(somatic, germline), color=GOLD, scale_factor=1.03), run_time=0.8)
        self.finish()


class S04Predict(SpokenScene):
    def construct(self):
        world = predict_world()
        self.add(world)
        self.at("Here is a gold variant")
        self.play(Indicate(VGroup(world.tumor_reads[2], world.normal_reads[2]), color=GOLD,
                           scale_factor=1.12), run_time=0.8)
        self.at("Predict")
        q = predict_card()
        self.play(FadeIn(q.chips), run_time=0.6)
        self.play(FadeIn(q.question), run_time=0.5)
        self.finish()


class S05Pause(PredictPause):
    QUESTION = "When did the gold variant enter?"
    OPTIONS = ["before tumor lineage", "after one tumor branch"]
    CARD = {"y": -3.25, "size": 30}
    SECONDS = 4.5

    def backdrop(self):
        return predict_world()


class S06Reveal(SpokenScene):
    def construct(self):
        pair = predict_world()
        q = predict_card()
        self.add(pair, q)
        self.at("Most likely")
        before = q.chips[0]
        self.play(before[0].animate.set_stroke(GOLD).set_fill(GOLD, 0.25),
                  before[1].animate.set_color(GOLD), run_time=0.7)
        self.at("before the tumor lineage")
        root_badge = marker(color=GOLD, size=0.18).move_to([-6.15, 0, 0])
        self.play(FadeOut(pair), FadeOut(q), FadeIn(root_badge), run_time=0.6)
        tree = family_tree(circle_badges=True, gold_badges=True)
        normal = VGroup(lineage_cell([2.25, 1.0], ordinary=True), lineage_cell([2.25, -1.0], ordinary=True))
        normal_gold = VGroup(*[marker(color=GOLD, size=0.11).move_to(c.get_center() + LEFT * 0.31 + DOWN * 0.20)
                               for c in normal])
        self.play(Create(tree.links), FadeIn(tree.cells),
                  *[TransformFromCopy(root_badge, m) for m in tree.golds], run_time=1.0)
        self.at("usually germline")
        self.play(FadeIn(normal), *[TransformFromCopy(root_badge, m) for m in normal_gold], run_time=0.8)
        germline = boxed_label("usually germline", GOLD, 30).move_to([4.55, 0, 0])
        self.play(FadeIn(germline), FadeOut(root_badge), run_time=0.4)
        branch_motion(tree)
        self.at("The matched normal gives")
        self.play(FadeOut(tree), FadeOut(normal), FadeOut(normal_gold), FadeOut(germline), run_time=0.5)
        clue_pair = tube_pair(gold=True)
        clue = T("timing clue", 32, GOLD).move_to([0, 3.2, 0])
        self.play(FadeIn(clue_pair), FadeIn(clue), run_time=0.7)
        self.at("Tumor data alone")
        unknown = boxed_label("timing ?", GOLD, 34).move_to([3.25, 0.2, 0])
        self.play(FadeOut(clue_pair.normal), FadeOut(clue_pair.normal_reads), FadeOut(clue),
                  FadeIn(unknown), run_time=0.7)
        self.at("cannot reliably separate")
        self.play(FadeOut(unknown), FadeIn(clue_pair.normal), FadeIn(clue_pair.normal_reads), run_time=0.7)
        self.finish()


def counter_lane(y, title, n, variants=0):
    label = T(title, 30, TEAL).move_to([-4.9, y, 0])
    tiles = VGroup(*[read_tile(CLAY if i < variants else TEAL, filled=i < variants, width=0.68)
                     for i in range(n)]).arrange(RIGHT, buff=0.16).move_to([1.0, y, 0])
    panel = RoundedRectangle(corner_radius=0.18, width=12.0, height=1.05, stroke_width=0,
                             fill_color=TEAL, fill_opacity=0.16).move_to([0, y, 0]).set_z_index(-1)
    return VGroup(label, tiles, panel)


class S07Vaf(SpokenScene):
    def construct(self):
        variant = counter_lane(1.55, "variant reads", 4, 4)
        all_reads = counter_lane(0.15, "all reads", 10, 4)
        for i, tile in enumerate(list(variant[1]) + list(all_reads[1])):
            bob(tile, amp=0.055, speed=1.15, seed=i)
        line = Line([-4.8, 0.85, 0], [5.8, 0.85, 0], color=PALE, stroke_width=3)
        self.at("Variant allele fraction")
        self.play(FadeIn(variant[1], shift=UP * 0.2), run_time=0.6)
        self.play(FadeIn(variant[0]), Create(line), FadeIn(all_reads), run_time=0.8)
        frac = Readout([("VAF", lambda: 4 / 10, "{:.2f}", TEAL)], at=[0, -1.45, 0], widest=[0.40], size=34)
        self.at("fraction of reads")
        self.play(FadeIn(frac), run_time=0.5)
        self.at("A clonal variant")
        clonal = boxed_label("clonal", CLAY, 28).move_to([-3.4, -1.45, 0])
        self.play(FadeIn(clonal), run_time=0.4)
        self.at("Normal cells dilute")
        normals = VGroup(*[read_tile(PALE, False) for _ in range(4)]).arrange_in_grid(2, 2, buff=0.16)
        normals.move_to([5.25, -0.45, 0])
        diluted = Readout([("VAF", lambda: 4 / 14, "{:.2f}", TEAL)], at=[0, -1.45, 0], widest=[0.29], size=34)
        self.play(FadeIn(normals, shift=LEFT * 0.2), Transform(frac, diluted), run_time=0.9)
        self.at("Copy gains")
        self.play(FadeOut(VGroup(variant, all_reads, normals, line, frac, clonal)), run_time=0.5)
        copies = VGroup(*[boxed_label("copy", PALE, 32, box=(2.25, 1.25), fill_opacity=0.30)
                          for _ in range(3)]).arrange(RIGHT, buff=0.65)
        copies.move_to([0, 0.6, 0])
        gain = T("gain", 30, GOLD).move_to([-3.7, -0.8, 0])
        loss = T("loss", 30, RED).move_to([0, -0.8, 0])
        loh = T("loss of heterozygosity", 30, CLAY).move_to([3.7, -0.8, 0])
        self.play(FadeIn(copies[:2]), FadeIn(gain), run_time=0.5)
        self.play(TransformFromCopy(copies[1], copies[2]), run_time=0.5)
        self.at("losses")
        self.play(FadeIn(loss), FadeOut(copies[2]), run_time=0.5)
        self.at("loss of heterozygosity")
        self.play(FadeIn(loh), copies[1][0].animate.set_stroke(CLAY), copies[1][1].animate.set_color(CLAY), run_time=0.7)
        self.at("variant and non variant copies")
        self.play(Indicate(copies, color=TEAL, scale_factor=1.04), run_time=0.7)
        self.add(scope_tag("schematic"))
        self.finish()


def sample_cells():
    cells = VGroup()
    for i in range(20):
        col = CLAY if i < 8 else PALE
        cells.add(RoundedRectangle(corner_radius=0.08, width=0.62, height=0.52,
                                   stroke_color=col, stroke_width=2.5, fill_color=col,
                                   fill_opacity=0.25 if col == CLAY else 0.06))
    cells.arrange_in_grid(4, 5, buff=0.18).move_to([-3.75, 0.15, 0])
    frame = RoundedRectangle(corner_radius=0.22, width=4.55, height=3.75,
                             stroke_color=PALE, stroke_width=3, fill_color=CLAY,
                             fill_opacity=0.10).move_to([-3.75, 0.15, 0])
    return VGroup(frame, cells)


class S08Purity(SpokenScene):
    def construct(self):
        sample = sample_cells()
        for i, c in enumerate(sample[1]):
            bob(c, amp=0.035, speed=1.05, seed=i)
        self.at("Purity is the fraction")
        self.play(FadeIn(sample[0]), FadeIn(sample[1]), run_time=0.8)
        purity = Readout([("purity", lambda: 8 / 20, "{:.0%}", CLAY)], at=[-3.75, -2.35, 0], widest=[0.40], size=30)
        self.play(FadeIn(purity), run_time=0.5)
        self.at("tumor cells")
        changed = []
        for i in range(8, 14):
            new = sample[1][i].copy().set_stroke(CLAY).set_fill(CLAY, 0.25)
            changed.append(Transform(sample[1][i], new))
        self.play(LaggedStart(*changed, lag_ratio=0.10), run_time=1.2)
        self.at("For a heterozygous clonal")
        lhs = boxed_label("expected VAF", TEAL, 30)
        eq = T("=", 34, PALE)
        p = boxed_label("purity", CLAY, 30)
        times = T("×", 34, PALE)
        half = boxed_label("0.5", GOLD, 30)
        relation = VGroup(lhs, eq, p, times, half).arrange(RIGHT, buff=0.22).move_to([2.65, 1.25, 0])
        self.play(FadeIn(lhs), run_time=0.35)
        self.at("expected VAF")
        self.play(FadeIn(eq), FadeIn(p), run_time=0.45)
        self.at("purity times one")
        self.play(FadeIn(times), FadeIn(half), run_time=0.45)
        self.at("The shortcut also assumes")
        assumption = boxed_label("normal cells lack it", PALE, 28).move_to([2.65, -0.05, 0])
        self.play(FadeIn(assumption), run_time=0.5)
        self.at("It fails after")
        self.play(FadeOut(sample), FadeOut(purity), FadeOut(assumption), run_time=0.3)
        self.play(relation.animate.move_to([0, 2.25, 0]), run_time=0.3)
        warnings = VGroup(
            boxed_label("normal cells carry it", GOLD, 28),
            boxed_label("copy number changed", RED, 28),
            boxed_label("other allele lost", RED, 28),
            boxed_label("subclone", CLAY, 28),
        ).arrange_in_grid(2, 2, buff=(0.6, 0.55)).move_to([0, -0.45, 0])
        stem = Line(relation.get_bottom(), [0, 1.15, 0], color=GREY, stroke_width=2.5)
        fork = Line([-2.5, 1.15, 0], [2.5, 1.15, 0], color=GREY, stroke_width=2.5)
        stems = VGroup(stem, fork,
                       arrow([-2.5, 1.15, 0], warnings[0].get_top(), GREY, 2.5, 0.10),
                       arrow([2.5, 1.15, 0], warnings[1].get_top(), GREY, 2.5, 0.10))
        for i, w in enumerate(warnings):
            w[0]._fill_t = i * 0.5

            def breathe_warning(m, dt):
                m._fill_t += dt
                m.set_fill(opacity=0.18 + 0.09 * np.sin(1.15 * m._fill_t))
            w[0].add_updater(breathe_warning)
        self.play(Create(stems), LaggedStart(*[FadeIn(w) for w in warnings], lag_ratio=0.16), run_time=1.2)
        self.at("only a subclone")
        self.play(Indicate(warnings[3], color=CLAY, scale_factor=1.05), run_time=0.6)
        self.finish()


def evidence_world():
    tree = family_tree(circle_badges=True, square_badges=True)
    pair = tube_pair(gold=True, narrow=True)
    return VGroup(tree, pair), tree, pair


class S09Limits(SpokenScene):
    def construct(self):
        world, tree, pair = evidence_world()
        branch_motion(tree)
        self.at("read the evidence in order")
        self.play(FadeIn(tree), FadeIn(pair), run_time=0.9)
        steps = VGroup(
            boxed_label("1  compare samples", TEAL, 24),
            boxed_label("2  map to branches", CLAY, 24),
            boxed_label("3  count copies", GOLD, 24),
        ).arrange(DOWN, buff=0.12, aligned_edge=LEFT).move_to([3.95, -2.45, 0])
        self.at("Compare tumor")
        self.play(FadeIn(steps[0]), Indicate(pair, color=TEAL, scale_factor=1.01), run_time=0.6)
        self.at("Ask which lineages")
        self.play(FadeIn(steps[1]), Indicate(tree.cells, color=CLAY, scale_factor=1.02), run_time=0.6)
        self.at("Then count mutant")
        self.play(FadeIn(steps[2]), Indicate(tree.circles, color=GOLD, scale_factor=1.06), run_time=0.6)
        self.at("Purity, copy number")
        self.play(FadeOut(steps), run_time=0.4)
        frame = DashedVMobject(RoundedRectangle(corner_radius=0.2, width=5.2, height=1.25,
                                                stroke_color=GOLD, stroke_width=3).move_to([3.75, -2.65, 0]),
                                 num_dashes=24)
        bounds = VGroup(T("purity", 22, CLAY), T("copy number", 22, RED), T("read depth", 22, TEAL))
        bounds.arrange(RIGHT, buff=0.25).move_to([3.75, -2.65, 0])
        self.play(Create(frame), LaggedStart(*[FadeIn(x) for x in bounds], lag_ratio=0.2), run_time=0.9)
        self.at("family tree estimate")
        estimate = T("estimate, not a replay", 30, GOLD).move_to([3.75, -2.65, 0])
        self.play(FadeOut(bounds), run_time=0.3)
        self.play(FadeIn(estimate), run_time=0.3)
        self.finish()


class S10Rule(SpokenScene):
    def construct(self):
        tree = family_tree(circle_badges=True, square_badges=True, gold_badges=True)
        normal = VGroup(lineage_cell([2.0, 1.1], ordinary=True), lineage_cell([2.0, -1.1], ordinary=True))
        normal_gold = VGroup(*[marker(color=GOLD, size=0.11).move_to(c.get_center() + LEFT * 0.31 + DOWN * 0.20)
                               for c in normal])
        self.add(tree, normal, normal_gold)
        branch_motion(tree)
        self.at("A high or low fraction")
        meter = dial(ValueTracker(0.35), center=[4.55, 1.25, 0], radius=1.25, label="fraction", color=TEAL)
        verdict = boxed_label("not a verdict", PALE, 30).move_to([4.55, -0.65, 0])
        self.play(FadeIn(meter), FadeIn(verdict), run_time=0.7)
        self.at("Read it with")
        clues = VGroup(boxed_label("matched normal", GOLD, 26), boxed_label("copy structure", RED, 26))
        clues.arrange(DOWN, buff=0.28).move_to([4.55, -2.05, 0])
        self.play(FadeIn(clues), FadeOut(verdict), run_time=0.6)
        self.at("Different branch histories")
        self.play(Indicate(VGroup(tree.links, tree.squares), color=CLAY, scale_factor=1.02), run_time=0.7)
        self.at("supporting clues matter")
        self.play(Indicate(clues, color=GOLD, scale_factor=1.03), run_time=0.6)
        self.at("That uncertainty belongs")
        uncertainty = boxed_label("interpret with uncertainty", PALE, 28).move_to([4.35, 0.0, 0])
        self.play(FadeOut(meter), run_time=0.3)
        self.play(FadeIn(uncertainty), run_time=0.3)
        self.at("Together, those clues")
        self.play(FadeOut(clues), FadeOut(uncertainty), run_time=0.4)
        gold_reads = VGroup(*[read_tile(GOLD, True, 0.55).move_to([5.3, 1.2 - i * 0.35, 0]) for i in range(3)])
        clay_reads = VGroup(*[read_tile(CLAY, True, 0.55).move_to([4.3, 0.35 - i * 0.35, 0]) for i in range(4)])
        square_reads = VGroup(*[read_tile(CLAY, False, 0.55).move_to([5.2, -1.35 - i * 0.35, 0]) for i in range(2)])
        self.play(FadeIn(gold_reads), FadeIn(clay_reads), FadeIn(square_reads), run_time=0.6)
        self.at("mixed sequencing reads")
        gold_targets = [tree.cells[0].get_center(), normal[0].get_center(), normal[1].get_center()]
        clay_targets = [tree.cells[i].get_center() for i in (0, 1, 2, 3)]
        square_targets = [tree.cells[i].get_center() for i in (5, 6)]
        self.play(*[r.animate.move_to(t) for r, t in zip(gold_reads, gold_targets)],
                  *[r.animate.move_to(t) for r, t in zip(clay_reads, clay_targets)],
                  *[r.animate.move_to(t) for r, t in zip(square_reads, square_targets)],
                  run_time=1.5)
        self.at("expanding cell lineages")
        self.play(FadeOut(gold_reads), FadeOut(clay_reads), FadeOut(square_reads),
                  Indicate(tree, color=CLAY, scale_factor=1.02), run_time=0.8)
        self.finish()


class S11End(EndCard):
    LINE = "Variant fractions trace DNA changes through expanding tumor cell lineages."
