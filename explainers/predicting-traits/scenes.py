"""Where Can White Flowers Hide? — one carried pea-cross world.

COLOR MAP (one color per concept, throughout)
  PURPLE = P allele and purple phenotype
  CREAM  = p allele and white phenotype
  TEAL   = sex-cell paths and Punnett grid
  GOLD   = questions and predictions
  GREY   = neutral structure
"""
from bp_parts import *


PURPLE = "#B07CFF"
CREAM = "#FFF1D0"


def allele_tile(letter, center=ORIGIN, scale=1.0):
    """Large, readable allele block; the letter is part of the block, not a molecule."""
    color = PURPLE if letter == "P" else CREAM
    box = RoundedRectangle(
        corner_radius=0.16 * scale,
        width=1.0 * scale,
        height=1.15 * scale,
        stroke_color=color,
        stroke_width=4,
        fill_color=color,
        fill_opacity=0.22,
    )
    label = T(letter, 46 * scale, color, weight=BOLD).move_to(box)
    return VGroup(box, label).move_to(center)


def flower(kind="purple", center=ORIGIN, scale=1.0):
    """A simple five-petal flower, deliberately botanical rather than molecular."""
    color = PURPLE if kind == "purple" else CREAM
    petals = VGroup()
    for angle in np.linspace(0, TAU, 5, endpoint=False):
        p = Ellipse(
            width=0.54 * scale,
            height=0.82 * scale,
            stroke_color=color,
            stroke_width=3,
            fill_color=color,
            fill_opacity=0.78,
        )
        p.rotate(angle).move_to(np.array(center) + 0.31 * scale * np.array([np.cos(angle), np.sin(angle), 0]))
        petals.add(p)
    middle = Dot(center, radius=0.12 * scale, color=GOLD)
    return VGroup(petals, middle)


def pea_plant(kind="purple", center=ORIGIN, height=3.3, label=None):
    """The carried plant picture used in every scene that shows a parent or offspring."""
    c = np.array(center, dtype=float)
    s = height / 3.3
    stem = Line(c + DOWN * 1.15 * s, c + UP * 0.82 * s, color=GREEN, stroke_width=7)
    branch_l = Line(c + DOWN * 0.25 * s, c + LEFT * 0.62 * s + UP * 0.15 * s, color=GREEN, stroke_width=5)
    branch_r = Line(c + UP * 0.05 * s, c + RIGHT * 0.62 * s + UP * 0.42 * s, color=GREEN, stroke_width=5)
    leaf_l = Ellipse(width=0.78 * s, height=0.38 * s, color=GREEN, stroke_width=3,
                     fill_color=GREEN, fill_opacity=0.32).rotate(0.45).move_to(branch_l.get_end())
    leaf_r = Ellipse(width=0.78 * s, height=0.38 * s, color=GREEN, stroke_width=3,
                     fill_color=GREEN, fill_opacity=0.32).rotate(-0.45).move_to(branch_r.get_end())
    bloom = flower(kind, c + UP * 1.22 * s, 0.92 * s)
    soil = Arc(radius=0.72 * s, start_angle=0, angle=PI, color=GREY, stroke_width=4).move_to(c + DOWN * 1.15 * s)
    g = VGroup(soil, stem, branch_l, branch_r, leaf_l, leaf_r, bloom)
    g.bloom = bloom
    if label:
        g.add(T(label, 28, PURPLE if kind == "purple" else CREAM).next_to(soil, DOWN, buff=0.16))
    return g


def hook_world(with_child=True):
    """Exact hook/title layout so the three plants never drift between scenes."""
    left = pea_plant("purple", [-4.1, 0.15, 0], 4.6)
    right = pea_plant("purple", [4.1, 0.15, 0], 4.6)
    child = pea_plant("white", [0, -1.05, 0], 2.8)
    world = VGroup(left, right)
    if with_child:
        world.add(child)
    world.left_parent, world.right_parent, world.child = left, right, child
    return world


def sex_cell(letter, center=ORIGIN, radius=0.62):
    color = PURPLE if letter == "P" else CREAM
    cell = Circle(radius=radius, stroke_color=TEAL, stroke_width=4, fill_color=TEAL, fill_opacity=0.10)
    tile = allele_tile(letter, scale=0.54).move_to(cell)
    return VGroup(cell, tile).move_to(center)


GRID_C = np.array([0.35, -0.30, 0.0])
GRID_CELL = 2.05


def punnett_grid(scale=1.0, center=GRID_C):
    """The fixed two-by-two grid used from s05 through s10."""
    c = np.array(center, dtype=float)
    s = GRID_CELL * scale
    field = Rectangle(width=2 * s, height=2 * s, stroke_width=0, fill_color=TEAL, fill_opacity=0.24).move_to(c)
    outline = Rectangle(width=2 * s, height=2 * s, stroke_color=TEAL, stroke_width=5).move_to(c)
    v = Line(c + UP * s, c + DOWN * s, color=TEAL, stroke_width=5)
    h = Line(c + LEFT * s, c + RIGHT * s, color=TEAL, stroke_width=5)
    g = VGroup(field, outline, v, h)
    g.centers = [c + LEFT * s / 2 + UP * s / 2, c + RIGHT * s / 2 + UP * s / 2,
                 c + LEFT * s / 2 + DOWN * s / 2, c + RIGHT * s / 2 + DOWN * s / 2]
    g.top = [c + LEFT * s / 2 + UP * (s + 0.52 * scale), c + RIGHT * s / 2 + UP * (s + 0.52 * scale)]
    g.side = [c + LEFT * (s + 0.52 * scale) + UP * s / 2, c + LEFT * (s + 0.52 * scale) + DOWN * s / 2]
    return g


def genotype_label(pair, center, size=42):
    """Allele pair with character-level concept colors."""
    t = T(pair, size, CREAM, weight=BOLD, t2c={"P": PURPLE, "p": CREAM})
    return t.move_to(center)


def filled_cross(include_flowers=False, subdued=False):
    """Complete Pp × Pp square, rebuilt at the same coordinates in later scenes."""
    grid = punnett_grid()
    top = VGroup(sex_cell("P", grid.top[0], 0.44), sex_cell("p", grid.top[1], 0.44))
    side = VGroup(sex_cell("P", grid.side[0], 0.44), sex_cell("p", grid.side[1], 0.44))
    pairs = VGroup(*[genotype_label(x, c) for x, c in zip(("PP", "Pp", "Pp", "pp"), grid.centers)])
    flowers = VGroup()
    if include_flowers:
        for i, c in enumerate(grid.centers):
            f = flower("white" if i == 3 else "purple", c + DOWN * 0.52, 0.40)
            pairs[i].shift(UP * 0.42)
            flowers.add(f)
    result = VGroup(grid, top, side, pairs, flowers)
    result.grid, result.top_tokens, result.side_tokens = grid, top, side
    result.pairs, result.flowers = pairs, flowers
    if subdued:
        result.set_opacity(0.32)
    return result


def predict_backdrop(empty_last=True):
    grid = punnett_grid()
    top = VGroup(sex_cell("P", grid.top[0], 0.44), sex_cell("p", grid.top[1], 0.44))
    side = VGroup(sex_cell("P", grid.side[0], 0.44), sex_cell("p", grid.side[1], 0.44))
    pairs = VGroup(*[genotype_label(x, c + UP * 0.34) for x, c in zip(("PP", "Pp", "Pp"), grid.centers[:3])])
    blooms = VGroup(*[flower("purple", c + DOWN * 0.48, 0.40) for c in grid.centers[:3]])
    target = grid.centers[3]
    waiting_top = sex_cell("p", target + UP * 0.78, 0.30)
    waiting_side = sex_cell("p", target + LEFT * 0.78, 0.30)
    path_top = DashedLine(waiting_top.get_bottom(), target + UP * 0.24, color=TEAL, stroke_width=5, dash_length=0.15)
    path_side = DashedLine(waiting_side.get_right(), target + LEFT * 0.24, color=TEAL, stroke_width=5, dash_length=0.15)
    g = VGroup(grid, top, side, pairs, blooms, path_top, path_side, waiting_top, waiting_side)
    g.grid, g.target, g.waiting_top, g.waiting_side = grid, target, waiting_top, waiting_side
    g.paths = VGroup(path_top, path_side)
    return g


class S00Hook(SpokenScene):
    def construct(self):
        world = hook_world(with_child=False)
        bob(world.left_parent, amp=0.12, speed=1.5)
        bob(world.right_parent, amp=0.12, speed=1.35, seed=3)
        self.play(FadeIn(world.left_parent, shift=UP * 0.2), FadeIn(world.right_parent, shift=UP * 0.2), run_time=0.7)

        self.at("white flowered offspring")
        q = T("?", 150, CREAM, weight=BOLD).set_opacity(0.20).move_to([0, 0.35, 0])
        q.layout_ok = True  # deliberately behind the offspring; noted in film_author.json
        child = world.child
        bob(child, amp=0.12, speed=1.7, seed=5)
        self.play(GrowFromCenter(q), FadeIn(child, shift=UP * 0.8), run_time=1.2)

        self.at("Picture two purple")
        self.play(Indicate(VGroup(world.left_parent.bloom, world.right_parent.bloom), color=PURPLE,
                           scale_factor=1.05), run_time=1.0)

        self.at("one offspring")
        self.play(Indicate(child.bloom, color=CREAM, scale_factor=1.12), run_time=0.9)

        self.at("visible color")
        puzzled = VGroup(*[T("?", 46, GOLD).next_to(p.bloom, UP, buff=0.18)
                           for p in (world.left_parent, world.right_parent)])
        self.play(FadeIn(puzzled, shift=DOWN * 0.15), run_time=0.8)

        self.at("answer is hidden")
        self.play(FadeOut(puzzled), q.animate.set_opacity(0.38),
                  Indicate(VGroup(world.left_parent, world.right_parent), color=CREAM, scale_factor=1.02), run_time=1.2)
        self.finish()


class S01Title(TitleCard):
    LESSON = "Predicting Traits with Punnett Squares"
    TITLE = "Where Can White Flowers Hide?"

    def construct(self):
        world = hook_world()
        world.scale(0.72).shift(DOWN * 0.62)
        world.set_opacity(0.30)
        bob(world.left_parent, amp=0.025, speed=1.4)
        bob(world.right_parent, amp=0.025, speed=1.3, seed=2)
        title = fit_text(self.TITLE, max_w=11.5, size=52, color=TEXT, font=TITLE_FONT, min_size=38)
        title.move_to([0, 1.95, 0])
        lesson = fit_text(self.LESSON.upper(), max_w=11.3, size=22, color=TEAL, min_size=22)
        lesson.next_to(title, UP, buff=0.28)
        rule = Line(LEFT * 1.5, RIGHT * 1.5, color=GOLD, stroke_width=4).next_to(title, DOWN, buff=0.28)
        self.add(world)
        self.play(FadeIn(lesson), Write(title), GrowFromCenter(rule), run_time=0.8)
        self.wait(0.7)
        self.play(FadeOut(VGroup(world, lesson, title, rule)), run_time=0.5)
        self.finish()


class S02Alleles(SpokenScene):
    def construct(self):
        parent = pea_plant("purple", [-3.55, -0.15, 0], 5.35)
        bob(parent, amp=0.11, speed=1.4)
        self.play(FadeIn(parent, scale=0.92), run_time=0.8)

        self.at("versions called alleles")
        allele_word = T("alleles", 36, TEAL, weight=BOLD).move_to([3.25, 2.65, 0])
        self.play(FadeIn(allele_word, shift=DOWN * 0.15), run_time=0.7)

        self.at("purple allele and")
        p = allele_tile("P", [2.30, 0.55, 0], 1.5)
        little_p = allele_tile("p", [4.25, -0.35, 0], 1.5)
        self.play(FadeIn(little_p, shift=LEFT * 0.25), FadeIn(p, shift=LEFT * 0.25), run_time=1.0)

        self.at("purple version is dominant")
        dominant = T("dominant", 30, PURPLE, weight=BOLD).next_to(p, UP, buff=0.18)
        self.play(FadeIn(dominant), Indicate(parent.bloom, color=PURPLE, scale_factor=1.08), run_time=0.9)

        self.at("white version is recessive")
        recessive = T("recessive", 30, CREAM, weight=BOLD).next_to(little_p, DOWN, buff=0.18)
        self.play(FadeIn(recessive), Indicate(little_p, color=CREAM, scale_factor=1.08), run_time=0.9)

        self.at("hidden from view")
        p.set_z_index(2)
        self.play(p.animate.shift(RIGHT * 0.25), little_p.animate.shift(LEFT * 0.10), run_time=0.7)
        still_here = T("still carried", 30, CREAM).move_to([4.15, -2.35, 0])
        self.play(FadeIn(still_here), little_p.animate.set_opacity(1.0), run_time=0.7)

        self.at("not damaged")
        self.play(Indicate(little_p, color=CREAM, scale_factor=1.12), run_time=0.9)
        self.finish()


class S03Genotype(SpokenScene):
    def construct(self):
        p = allele_tile("P", [-3.95, 0.45, 0], 1.45)
        little_p = allele_tile("p", [-2.35, 0.45, 0], 1.45)
        self.play(FadeIn(p, shift=RIGHT * 0.2), FadeIn(little_p, shift=LEFT * 0.2), run_time=0.7)

        self.at("is its genotype")
        geno = T("genotype: Pp", 36, TEAL, weight=BOLD, t2c={"P": PURPLE, "p": CREAM})
        geno.move_to([-3.15, 2.35, 0])
        bracket = Brace(VGroup(p, little_p), DOWN, color=TEAL)
        self.play(GrowFromCenter(bracket), FadeIn(geno, shift=DOWN * 0.15), run_time=0.8)

        self.at("is its phenotype")
        plant = pea_plant("purple", [2.65, 0.25, 0], 4.5)
        bob(plant, amp=0.11, speed=1.5)
        phenotype = T("phenotype: purple", 34, PURPLE, weight=BOLD).move_to([2.65, 3.34, 0])
        self.play(FadeIn(plant, scale=0.88), FadeIn(phenotype, shift=DOWN * 0.15), run_time=1.0)

        self.at("one of each")
        self.play(Indicate(VGroup(p, little_p), color=TEAL, scale_factor=1.06), run_time=0.8)

        self.at("phenotype is purple")
        self.play(Indicate(plant.bloom, color=PURPLE, scale_factor=1.10), run_time=0.8)

        self.at("appearance alone")
        unknown = RoundedRectangle(corner_radius=0.16, width=2.2, height=1.0, color=GREY, stroke_width=3,
                                   fill_color=BG, fill_opacity=0.92).move_to([2.65, -2.15, 0])
        mark = T("PP or Pp?", 32, GOLD, weight=BOLD, t2c={"P": PURPLE, "p": CREAM}).move_to(unknown)
        self.play(FadeIn(unknown), FadeIn(mark), run_time=0.8)

        self.at("Carried information")
        link = Arrow([-1.3, 0.35, 0], [0.25, 0.35, 0], color=TEAL, stroke_width=5, buff=0.12)
        rule = caption("What is carried can differ from what shows.", color=GOLD)
        self.play(GrowArrow(link), FadeIn(rule, shift=UP * 0.12), run_time=1.0)
        self.finish()


class S04SexCells(SpokenScene):
    def construct(self):
        left = pea_plant("purple", [-4.4, 1.25, 0], 2.75)
        right = pea_plant("purple", [4.4, 1.25, 0], 2.75)
        left_pair = VGroup(allele_tile("P", [-4.75, -0.25, 0], 0.72), allele_tile("p", [-4.05, -0.25, 0], 0.72))
        right_pair = VGroup(allele_tile("P", [4.05, -0.25, 0], 0.72), allele_tile("p", [4.75, -0.25, 0], 0.72))
        bob(left, amp=0.09, speed=1.4)
        bob(right, amp=0.09, speed=1.3, seed=2)
        self.add(left, right, left_pair, right_pair)

        self.at("pair separates")
        left_cells = VGroup(sex_cell("P", [-3.4, -1.35, 0], 0.55), sex_cell("p", [-3.4, -2.7, 0], 0.55))
        self.play(TransformFromCopy(left_pair[0], left_cells[0]), TransformFromCopy(left_pair[1], left_cells[1]), run_time=1.0)

        self.at("Each sex cell")
        one_each = T("one allele per sex cell", 30, TEAL, weight=BOLD).move_to([-3.95, -3.56, 0])
        self.play(FadeIn(one_each, shift=UP * 0.12), run_time=0.7)

        self.at("purple block enter")
        paths_left = VGroup(
            Arrow([-3.4, -1.35, 0], [-0.75, -1.45, 0], color=TEAL, stroke_width=5, buff=0.67),
            Arrow([-3.4, -2.7, 0], [-0.75, -2.85, 0], color=TEAL, stroke_width=5, buff=0.67),
        )
        self.play(GrowArrow(paths_left[0]), left_cells[0].animate.move_to([-0.75, -1.45, 0]), run_time=1.0)

        self.at("white block enter")
        self.play(GrowArrow(paths_left[1]), left_cells[1].animate.move_to([-0.75, -2.85, 0]), run_time=1.0)

        self.at("other parent does")
        right_cells = VGroup(sex_cell("P", [3.85, -1.45, 0], 0.55), sex_cell("p", [3.85, -2.85, 0], 0.55))
        paths_right = VGroup(
            Arrow([3.2, -1.45, 0], [0.05, -1.45, 0], color=TEAL, stroke_width=5, buff=0.12),
            Arrow([3.2, -2.85, 0], [0.05, -2.85, 0], color=TEAL, stroke_width=5, buff=0.12),
        )
        self.play(TransformFromCopy(right_pair[0], right_cells[0]), TransformFromCopy(right_pair[1], right_cells[1]),
                  GrowArrow(paths_right[0]), GrowArrow(paths_right[1]), run_time=1.2)
        bob(right_cells[0], amp=0.09, speed=1.8)
        bob(right_cells[1], amp=0.09, speed=1.6, seed=4)

        self.at("hidden version onward")
        self.play(Indicate(VGroup(left_cells[1], right_cells[1]), color=CREAM, scale_factor=1.10), run_time=1.0)
        self.finish()


class S05Square(SpokenScene):
    def construct(self):
        grid = punnett_grid()
        title = T("Punnett square", 38, TEAL, weight=BOLD).move_to([0.35, 3.28, 0])
        self.play(Create(grid), FadeIn(title, shift=DOWN * 0.12), run_time=1.2)
        pulse(grid, base=5, amp=0.8, speed=2.2)

        self.at("settle across the top")
        top = VGroup(sex_cell("P", grid.top[0], 0.44), sex_cell("p", grid.top[1], 0.44))
        top_lab = T("parent 1", 28, GREY).move_to([3.85, 2.78, 0])
        self.play(FadeIn(top, shift=DOWN * 0.35), FadeIn(top_lab), run_time=0.9)
        bob(top[0], amp=0.10, speed=1.5)
        bob(top[1], amp=0.10, speed=1.35, seed=2)

        self.at("settle down the side")
        side = VGroup(sex_cell("P", grid.side[0], 0.44), sex_cell("p", grid.side[1], 0.44))
        side_lab = T("parent 2", 28, GREY).move_to([-3.25, -0.30, 0]).rotate(PI / 2)
        self.play(FadeIn(side, shift=RIGHT * 0.35), FadeIn(side_lab), run_time=0.9)
        bob(side[0], amp=0.10, speed=1.4, seed=3)
        bob(side[1], amp=0.10, speed=1.3, seed=5)

        self.at("Follow a teal path")
        target = grid.centers[0]
        path_top = Arrow(top[0].get_bottom(), target + UP * 0.34, color=TEAL, stroke_width=6, buff=0.12)
        path_side = Arrow(side[0].get_right(), target + LEFT * 0.34, color=TEAL, stroke_width=6, buff=0.12)
        self.play(GrowArrow(path_top), GrowArrow(path_side), run_time=1.1)

        self.at("two arriving alleles")
        a = allele_tile("P", target + LEFT * 0.30, 0.52)
        b = allele_tile("P", target + RIGHT * 0.30, 0.52)
        self.play(TransformFromCopy(top[0][1], a), TransformFromCopy(side[0][1], b), run_time=0.9)

        self.at("one possible genotype")
        pair = genotype_label("PP", target, 46)
        self.play(FadeOut(VGroup(a, b)), FadeIn(pair, scale=0.82), run_time=0.7)

        self.at("contributions stay separate")
        parent_marks = VGroup(T("top", 28, TEAL).next_to(top, RIGHT, buff=0.22),
                              T("side", 28, TEAL).next_to(side, DOWN, buff=0.22))
        self.play(FadeIn(parent_marks), Indicate(VGroup(path_top, path_side), color=TEAL, scale_factor=1.02), run_time=1.0)
        self.finish()


class S06Predict(SpokenScene):
    QUESTION = "What genotype and flower color appear in the last box?"

    def construct(self):
        world = predict_backdrop()
        for i, f in enumerate(world[4]):
            bob(f, amp=0.09, speed=1.35 + 0.1 * i, seed=i)
        self.add(world.grid, world[1], world[2])

        self.at("Three boxes now")
        self.play(FadeIn(VGroup(world[3], world[4]), lag_ratio=0.18), run_time=1.0)

        self.at("last box receives")
        self.play(FadeIn(VGroup(world.paths, world.waiting_top, world.waiting_side)), run_time=0.9)
        pulse(world.paths, base=5, amp=2, speed=3)

        self.at("What genotype")
        q = question_card(self.QUESTION, y=-3.22, size=30, max_w=10.4)
        self.play(FadeIn(q.question, shift=UP * 0.12), run_time=0.8)

        self.at("Keep your answer")
        self.play(world.waiting_top.animate.shift(DOWN * 0.12), world.waiting_side.animate.shift(RIGHT * 0.12), run_time=1.0)
        self.finish()


class S07Pause(NarratedScene):
    def construct(self):
        world = predict_backdrop()
        q = question_card(S06Predict.QUESTION, y=-3.22, size=30, max_w=10.4)
        world.waiting_top.shift(DOWN * 0.12)
        world.waiting_side.shift(RIGHT * 0.12)
        for path in world.paths:
            path.layout_ok = True  # tokens deliberately travel along these paths
        self.add(world, q)
        self.play(world.waiting_top.animate.shift(DOWN * 0.28),
                  world.waiting_side.animate.shift(RIGHT * 0.28), run_time=4.45, rate_func=linear)
        self.finish()


class S08Reveal(SpokenScene):
    def construct(self):
        world = predict_backdrop()
        world.waiting_top.shift(DOWN * 0.40)
        world.waiting_side.shift(RIGHT * 0.40)
        for path in world.paths:
            path.layout_ok = True  # dashed paths intentionally end at the moving p tokens
        self.add(world)

        self.at("Both white alleles meet")
        target = world.target
        self.play(world.waiting_top.animate.move_to(target + LEFT * 0.30),
                  world.waiting_side.animate.move_to(target + RIGHT * 0.30), run_time=1.1)

        self.at("genotype has two")
        pp = genotype_label("pp", target + UP * 0.40, 46)
        target_glow = Square(side_length=1.92, stroke_color=CREAM, stroke_width=4,
                             fill_color=CREAM, fill_opacity=0.12).move_to(target)
        self.play(FadeOut(VGroup(world.waiting_top, world.waiting_side)), FadeIn(target_glow),
                  FadeIn(pp, scale=0.85), run_time=1.0)

        self.at("white phenotype appears")
        white = flower("white", target + DOWN * 0.48, 0.48)
        bob(white, amp=0.10, speed=1.8)
        self.play(GrowFromCenter(white), run_time=1.0)

        parents = VGroup(pea_plant("purple", [-5.25, 2.3, 0], 1.55), pea_plant("purple", [5.25, 2.3, 0], 1.55))
        parents[0].shift(LEFT * 1.6).set_opacity(0)
        parents[1].shift(RIGHT * 1.6).set_opacity(0)
        self.add(parents)
        self.play(parents[0].animate.shift(RIGHT * 1.6).set_opacity(1),
                  parents[1].animate.shift(LEFT * 1.6).set_opacity(1), run_time=1.45)

        self.at("never showed")
        self.play(Indicate(parents, color=PURPLE, scale_factor=1.06), run_time=1.0)
        bob(parents[0], amp=0.11, speed=1.45)
        bob(parents[1], amp=0.11, speed=1.30, seed=4)

        self.at("parent's flowers")
        left_p = allele_tile("p", [-5.25, 0.95, 0], 0.56)
        right_p = allele_tile("p", [5.25, 0.95, 0], 0.56)
        self.play(FadeIn(left_p, shift=DOWN * 0.15), FadeIn(right_p, shift=DOWN * 0.15), run_time=0.7)

        self.at("It was carried")
        trail = VGroup(
            DashedLine(left_p.get_right(), world[2][1].get_left(), color=CREAM, stroke_width=7, dash_length=0.13),
            DashedLine(right_p.get_bottom(), world[1][1].get_top(), color=CREAM, stroke_width=7, dash_length=0.13),
        )
        self.play(Create(trail), run_time=0.65)
        pulse(trail, base=7, amp=1.5, speed=2.5)
        carriers = VGroup(Dot(left_p.get_right(), radius=0.15, color=CREAM),
                          Dot(right_p.get_bottom(), radius=0.15, color=CREAM))
        carrier_paths = VGroup(Line(left_p.get_right(), world[2][1].get_left()),
                               Line(right_p.get_bottom(), world[1][1].get_top()))
        self.add(carriers)
        self.play(MoveAlongPath(carriers[0], carrier_paths[0]), MoveAlongPath(carriers[1], carrier_paths[1]),
                  run_time=1.6, rate_func=linear)

        self.at("joined in this offspring")
        self.play(Indicate(VGroup(pp, white), color=CREAM, scale_factor=1.10), run_time=1.0)
        self.finish()


class S09Read(SpokenScene):
    def construct(self):
        cross = filled_cross(include_flowers=True)
        self.add(cross)
        for f in cross.flowers:
            bob(f, amp=0.10, speed=1.5 + 0.08 * len(f.submobjects), seed=len(f.submobjects))

        self.at("allele pairs predict")
        scan = Square(side_length=1.72, color=GOLD, stroke_width=5, fill_color=GOLD, fill_opacity=0.08)
        scan.move_to(cross.grid.centers[0])
        self.play(FadeIn(scan), run_time=0.25)
        self.play(Succession(*[scan.animate.move_to(c) for c in cross.grid.centers[1:]]), run_time=1.7)

        self.at("flowers translate")
        self.play(Succession(*[scan.animate.move_to(c) for c in cross.grid.centers]), run_time=1.8)

        self.at("Most boxes show purple")
        purple_brace = Brace(cross.grid, LEFT, color=GOLD)
        purple_lab = T("3/4 purple", 30, PURPLE, weight=BOLD).next_to(purple_brace, LEFT, buff=0.16)
        self.play(GrowFromCenter(purple_brace), FadeIn(purple_lab), run_time=0.8)

        self.at("one shows white")
        white_box = SurroundingRectangle(cross.flowers[3], color=GOLD, buff=0.18, stroke_width=4)
        white_lab = T("1/4 white", 30, CREAM, weight=BOLD).move_to([4.85, -1.45, 0])
        self.play(Create(white_box), FadeIn(white_lab), run_time=0.8)

        self.at("possible outcome")
        chance = caption("chance for each offspring", color=GOLD)
        self.play(FadeOut(scan), FadeIn(chance, shift=UP * 0.12), run_time=0.8)

        self.at("does not schedule")
        calendar = RoundedRectangle(corner_radius=0.14, width=1.35, height=1.25, color=GREY, stroke_width=4).move_to([5.05, 1.15, 0])
        rings = VGroup(*[Line([x, 1.92, 0], [x, 1.62, 0], color=GREY, stroke_width=5) for x in (4.7, 5.4)])
        slash = Line([4.45, 0.52, 0], [5.65, 1.78, 0], color=RED, stroke_width=7)
        no_schedule = T("not a schedule", 28, RED, weight=BOLD).move_to([5.05, 0.18, 0])
        self.play(Create(calendar), Create(rings), Create(slash), FadeIn(no_schedule), run_time=1.0)
        self.finish()


class S10Scope(SpokenScene):
    def construct(self):
        cross = filled_cross(include_flowers=True)
        cross.scale(0.72).move_to([-1.45, 0.35, 0])
        for token in (*cross.top_tokens, *cross.side_tokens):
            token[1][1].scale(1.30)
        bob(cross, amp=0.08, speed=1.25)
        boundary = RoundedRectangle(corner_radius=0.20, width=6.4, height=5.55, color=TEAL, stroke_width=4,
                                    fill_color=TEAL, fill_opacity=0.22).move_to([-1.45, 0.35, 0])
        boundary_label = T("one-gene model", 32, TEAL, weight=BOLD).move_to([-1.45, 3.38, 0])
        self.play(FadeIn(cross), Create(boundary), FadeIn(boundary_label), run_time=1.0)

        self.at("one gene")
        one_gene = chip("one gene", TEAL, 28).move_to([4.35, 2.15, 0])
        self.play(FadeIn(one_gene, shift=LEFT * 0.2), run_time=0.7)

        self.at("two alleles")
        alleles = chip("two alleles, one dominant", PURPLE, 26).move_to([4.35, 0.95, 0])
        self.play(FadeIn(alleles, shift=LEFT * 0.2), run_time=0.7)

        self.at("known parent genotypes")
        known = chip("known parent genotypes", GREY, 26).move_to([4.35, -0.25, 0])
        self.play(FadeIn(known, shift=LEFT * 0.2), run_time=0.7)

        self.at("links what parents")
        bridge = Arrow([2.0, -1.0, 0], [3.2, -1.25, 0], color=GOLD, stroke_width=5, buff=0.10)
        chance = T("chance for each offspring", 28, GOLD).move_to([4.35, -1.55, 0])
        self.play(GrowArrow(bridge), FadeIn(chance), run_time=0.9)

        self.at("Real groups can")
        kids = VGroup(*[flower(k, [x, -2.72 + 0.12 * ((i % 2) * 2 - 1), 0], 0.36)
                        for i, (x, k) in enumerate(zip(np.linspace(-3.9, 3.7, 7),
                                                     ("purple", "purple", "white", "purple", "purple", "purple", "white")))])
        self.play(FadeIn(kids, lag_ratio=0.12), run_time=1.0)
        for i, f in enumerate(kids):
            bob(f, amp=0.04, speed=1.25 + 0.08 * i, seed=i)

        self.at("Punnett squares predict chances")
        rule = caption("Predict chances — not exact counts.", color=GOLD, y=-3.42)
        self.play(FadeOut(VGroup(one_gene, alleles, known, bridge, chance)), FadeIn(rule, shift=UP * 0.12), run_time=0.9)
        self.finish()


class S11End(EndCard):
    LINE = "For one-gene crosses, Punnett squares predict chances, not exact offspring counts."
