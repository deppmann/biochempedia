"""Controlled genetic crosses, animated on a single breeding table.

GREEN/YELLOW = seed colour and yellow-mouse phenotype; shape = seed texture.
BLUE = observed counts and A; GOLD = probabilities; PURPLE = a.
GREY = structure; RED = exclusion, caution, or red fly eyes.
"""
from itertools import product

from bp_parts import *
from bp_style import EndCard

PURPLE = "#B58CD9"
TABLE = "#2C4254"
EDGE = "#496377"
OBSERVED = (315, 108, 101, 32)
CLASSES = ("Round yellow", "Round green", "Wrinkled yellow", "Wrinkled green")
GAMETES = ("AB", "Ab", "aB", "ab")
QUESTION = "Does that mismatch break the 9:3:3:1 rule?"
QUESTION_LAYOUT = {"y": 2.94, "size": 33}


def pt(x, y):
    return np.array([x, y, 0.0])


def label(value, x, y, size=31, color=TEXT):
    return T(value, size, color).move_to(pt(x, y))


def number(value, x, y, size=34, color=TEXT):
    return M(value, size, color).move_to(pt(x, y))


def tray(width, height, x, y, color=EDGE, fill=TABLE):
    return RoundedRectangle(width=width, height=height, corner_radius=0.15,
                            stroke_color=color, stroke_width=2, fill_color=fill,
                            fill_opacity=1).move_to(pt(x, y))


def table():
    return tray(13.30, 6.55, 0, 0.315, color="#354859", fill="#19232D").set_z_index(-10)


def sway(stalk, anchor, amplitude=0.11):
    """Let a mounted flower bend gently while keeping the base of the stem still."""
    t, angle = 0.0, 0.0

    def bend(mob, dt):
        nonlocal t, angle
        t += dt
        new_angle = amplitude * np.sin(1.65 * t)
        mob.rotate(new_angle - angle, about_point=anchor)
        angle = new_angle

    stalk.add_updater(bend)


def drift_in_cells(tokens, amp=0.14):
    for i, token in enumerate(tokens):
        bob(token, amp=amp, speed=1.9, seed=i)


def seed(center=ORIGIN, radius=0.37, wrinkled=False, color=GREEN):
    if wrinkled:
        angles = np.linspace(0, TAU, 33)
        points = [pt(np.cos(a), np.sin(a)) * radius * (1 + 0.12 * np.cos(7 * a)) for a in angles]
        shell = VMobject().set_points_smoothly(points).set_stroke(color, 2)
    else:
        shell = Circle(radius, color=color, stroke_width=2)
    shell.set_fill(color, 0.8)
    gleam = Arc(radius=radius * 0.68, start_angle=1.0, angle=1.4, color=TEXT, stroke_width=2)
    gleam.shift(LEFT * radius * 0.04 + UP * radius * 0.04).set_stroke(opacity=0.52)
    return VGroup(shell, gleam).move_to(center)


def pod(x, wrinkled=False):
    shell = Ellipse(width=4.30, height=1.44, color=GREEN, stroke_width=3,
                    fill_color="#375D46", fill_opacity=1)
    row = VGroup(*(seed(pt(i * 0.83, 0), 0.32, wrinkled) for i in (-1.5, -0.5, 0.5, 1.5)))
    stem = ArcBetweenPoints(shell.get_right(), pt(2.52, 0.49), angle=0.85,
                            color=GREEN, stroke_width=5)
    return VGroup(shell, row, stem).rotate(-0.14 if wrinkled else 0.14).move_to(pt(x, 1.60))


def pollen(path, count=13, radius=0.067):
    """A stream of pollen grains along a schematic transfer path."""
    return AnimationGroup(*(
        Succession(FadeIn(grain, run_time=0.12), MoveAlongPath(grain, path, rate_func=linear),
                   FadeOut(grain, run_time=0.12))
        for grain in (Dot(path.get_start(), radius=radius, color=YELLOW) for _ in range(count))
    ), lag_ratio=0.15)


def flower(x=0, y=0, scale=1.0, opened=False, wrinkled=False):
    petal_color = PURPLE if wrinkled else BLUE
    stem = Line(pt(0, -1.87), pt(0, -0.28), color=GREEN, stroke_width=12)
    leaves = VGroup(*(Ellipse(width=0.86, height=0.37, fill_color=GREEN, fill_opacity=0.65,
                              stroke_width=0).rotate(side * 0.48).move_to(pt(side * 0.42, -1.30))
                       for side in (-1, 1)))
    petals = VGroup(*(Ellipse(width=1.16, height=2.45, color=petal_color, stroke_width=3,
                              fill_color=petal_color, fill_opacity=0.29)
                      .rotate(side * (0.94 if opened else 0.30))
                      .move_to(pt(side * (1.05 if opened else 0.42), 0.54)) for side in (-1, 1)))
    pistil = Line(pt(0, -0.31), pt(0, 0.79), color=GREEN, stroke_width=8)
    anthers = VGroup(*(Dot(pt(side * 0.40, 0.38), radius=0.13, color=YELLOW) for side in (-1, 1)))
    result = VGroup(stem, leaves, petals, pistil, Dot(pt(0, 0.79), radius=0.13, color=GREEN), anthers)
    return result.scale(scale, about_point=ORIGIN).shift(pt(x, y))


class S01Hook(SpokenScene):
    def construct(self):
        left, right = pod(-3.5), pod(3.18, True)
        bed = tray(8.74, 1.68, -0.22, -1.18)
        ghost = seed(pt(4.95, -1.23), 0.44, True).set_opacity(0.37)
        mark = label("?", 4.95, -0.25, 56, GOLD)
        self.add(table(), left, right, bed, scope_tag(size=28, color=TEXT))
        bob(left, amp=0.14, speed=1.85)
        bob(right, amp=0.14, speed=1.85, seed=3)
        self.at("Where does a")
        self.play(FadeIn(ghost), FadeIn(mark), run_time=0.75)
        pulse(ghost[0], base=2, amp=1.4, speed=2)
        self.at("two lines cross")
        self.play(pollen(ArcBetweenPoints(pt(-1.53, 1.68), pt(1.25, 1.68), angle=-0.55)),
                  run_time=3.2)
        self.at("every hybrid")
        hybrids = VGroup(*(seed(pt(-3.60 + i * 0.95, -1.18), 0.34) for i in range(8)))
        self.play(LaggedStart(*(FadeIn(pea, shift=DOWN * 0.85) for pea in hybrids), lag_ratio=0.28),
                  run_time=3.0)
        self.at("count offspring")
        self.play(LaggedStart(*(Indicate(pea, color=GREEN, scale_factor=1.23) for pea in hybrids),
                              lag_ratio=0.35), run_time=2.2)
        self.finish()


class S02Title(TitleCard):
    LESSON = "Controlled genetic crosses"
    TITLE = "Reading Hidden Genes From Planned Crosses"

    def construct(self):
        self.add(table(), pod(-3.5).set_opacity(0.18), pod(3.18, True).set_opacity(0.18))
        title = fit_text(self.TITLE, max_w=11.8, size=40, min_size=38, font=TITLE_FONT)
        course = label(self.LESSON.upper(), 0, -1.10, 28, TEAL)
        self.play(FadeIn(title), FadeIn(course), run_time=0.5)
        self.finish()


class S03Parents(SpokenScene):
    def construct(self):
        round_flower = flower(-2.2, 0.22, 1.34)
        pure = label("Pure lines", 0, 3.22, 36, GOLD)
        self.add(table(), round_flower, scope_tag(size=28, color=TEXT))
        sway(round_flower, round_flower[0].get_start())
        self.at("pure lines")
        self.play(FadeIn(pure), run_time=0.55)
        self.at("Garden pea flowers")
        self.play(Indicate(round_flower[2], color=BLUE, scale_factor=1.09), run_time=3.7)
        self.at("so they normally")
        loop = ArcBetweenPoints(pt(-2.73, 0.73), pt(-2.2, 1.28), angle=-2.2)
        self.play(pollen(loop, radius=0.052), run_time=3)
        self.at("a line stays pure")
        selfed = VGroup(*(seed(pt(-3.35 + i * 0.76, -2.18), 0.25) for i in range(4)))
        self.play(LaggedStart(*(GrowFromCenter(p) for p in selfed), lag_ratio=0.35), run_time=1.1)
        self.at("Opened by hand")
        round_flower.clear_updaters()
        donor = flower(3.12, 0.18, 1.06, opened=True, wrinkled=True)
        brush = VGroup(Line(pt(-0.38, 0), pt(0.55, 0.13), color=BLUE, stroke_width=10),
                       Ellipse(width=0.38, height=0.22, color=GOLD, fill_opacity=1).move_to(pt(-0.48, -0.025)))
        brush.move_to(pt(2.30, 1.16))
        self.play(Transform(round_flower, flower(-2.2, 0.22, 1.34, opened=True)),
                  FadeIn(donor), FadeOut(selfed), FadeOut(pure), run_time=1.0)
        path = ArcBetweenPoints(brush.get_center(), pt(-1.64, 1.28), angle=-0.53)
        grains = VGroup(*(Dot(pt(2.05 + i * 0.105, 1.07 + 0.10 * (i % 2)), radius=0.045, color=YELLOW)
                          for i in range(5)))
        self.add(brush, grains)
        self.at("it can be crossed")
        self.play(MoveAlongPath(VGroup(brush, grains), path), run_time=1.10)
        barrier = Arc(radius=0.80, start_angle=-0.48, angle=0.96, arc_center=pt(-0.04, 0.92),
                      color=TEAL, stroke_width=5)
        impact = barrier.point_from_proportion(0.5) + RIGHT * 0.09
        stray_path = ArcBetweenPoints(pt(1.70, 2.45), impact, angle=0.38)
        stray_path.append_vectorized_mobject(ArcBetweenPoints(impact, pt(2.50, 2.13), angle=-0.32))
        self.at("stray pollen")
        self.play(Create(barrier, run_time=0.32), pollen(stray_path, count=7).set_run_time(1.15))
        self.finish()


def tally_bar(axis, x, value, color, width, opacity=0.86):
    foot = axis.pt(x, 0)
    height = max(0.005, axis.pt(x, value)[1] - foot[1])
    return Rectangle(width=width, height=height, stroke_color=color, stroke_width=2,
                     fill_color=color, fill_opacity=opacity).move_to(foot + UP * (height / 2))


class S04Counts(SpokenScene):
    def construct(self):
        hybrid = flower(-4.32, 0.08, 1.17)
        self.add(table(), hybrid)
        sway(hybrid, hybrid[0].get_start())
        self.at("let the round")
        self.play(pollen(ArcBetweenPoints(pt(-4.78, 0.53), pt(-4.32, 1.01), angle=-2.2)),
                  run_time=2.45)
        axis = Plot(box=(-1.71, 5.65, -2.02, 2.41), xr=(0, 3), yr=(0, 6000))
        x_values = (0.79, 2.17)
        for x, wrinkled in zip(x_values, (False, True)):
            self.add(seed(axis.pt(x, 0) + DOWN * 0.46, 0.26, wrinkled))
        self.at("count every seed")
        stream = ArcBetweenPoints(pt(-3.23, 0.31), pt(-0.48, -1.96), angle=-0.65)
        self.play(Create(axis.axes), pollen(stream, count=17), run_time=3.15)
        total = number("7,324 total", 0, 3.24, 37, GOLD)
        self.at("7 ,324")
        self.play(FadeIn(total), run_time=0.55)
        bars = VGroup(*(tally_bar(axis, x, value, BLUE, 1.65) for x, value in zip(x_values, (5474, 1850))))
        counts = [number(f"{value:,}", bar.get_x(), bar.get_top()[1] + 0.35, 35, BLUE)
                  for bar, value in zip(bars, (5474, 1850))]
        for cue, bar, count in zip(("5 ,474", "1 ,850"), bars, counts):
            self.at(cue)
            self.play(GrowFromEdge(bar, DOWN, run_time=0.75), FadeIn(count, run_time=0.45))
        self.at("Round divided")
        math = number("5,474 ÷ 1,850", -4.19, 0.45, 31)
        self.play(FadeOut(hybrid), run_time=0.42)
        self.play(Write(math), run_time=1.12)
        self.at("2 .96")
        result = number("= 2.96", -4.19, -0.43, 38, GOLD)
        self.play(Write(result), run_time=0.75)
        self.at("nearly 3")
        self.play(FadeIn(boxed_label("≈ 3:1", GOLD, size=35).move_to(pt(-4.19, -1.47))), run_time=0.6)
        self.finish()


def genotype(left, right):
    return "".join("".join(sorted(pair)) for pair in zip(left, right))


def punnett(gametes=("A", "a")):
    """Equal outcomes at fixed table coordinates, shared across both generations."""
    step = 4.64 / len(gametes)
    cell_width = 5.22 / len(gametes)
    cells, terms, headers = VGroup(), VGroup(), VGroup()
    x0, y0 = 0.44, 2.40
    for i, gamete in enumerate(gametes):
        headers.add(number(gamete, x0 + (i + 0.5) * cell_width, 2.81, 29, GOLD),
                    number(gamete, -0.04, y0 - (i + 0.5) * step, 29, GOLD))
    for (i, egg), (j, grain) in product(enumerate(gametes), repeat=2):
        x, y = x0 + (j + 0.5) * cell_width, y0 - (i + 0.5) * step
        cells.add(tray(cell_width - 0.095, step - 0.095, x, y))
        terms.add(number(genotype(egg, grain), x, y, 28 if len(gametes) == 4 else 38))
    return cells, terms, headers


def pea_class(genes):
    return 2 * ("A" not in genes) + ("B" not in genes)


def pea_tokens(cells, groups, radius):
    return VGroup(*(seed(cell.get_center(), radius, group >= 2, GREEN if group % 2 else YELLOW)
                    for cell, group in zip(cells, groups)))


def fill_cells(cells, groups, tokens, duration):
    return LaggedStart(*(AnimationGroup(
        cell.animate.set_fill(GREEN if group % 2 else YELLOW, opacity=0.34), GrowFromCenter(token))
        for cell, group, token in zip(cells, groups, tokens)), lag_ratio=0.12, run_time=duration)


def single_world():
    cells, terms, headers = punnett()
    groups = (1, 1, 1, 3)
    tokens = pea_tokens(cells, groups, 0.56)
    for cell, group in zip(cells, groups):
        cell.set_fill(GREEN, opacity=0.34)
    return VGroup(cells, tokens, headers)


def coins(genes, x, y):
    return VGroup(*(boxed_label(gene, BLUE if gene.isupper() else PURPLE, size=32)
                    .move_to(pt(x + (i - (len(genes) - 1) / 2) * 0.77, y))
                    for i, gene in enumerate(genes)))


class S05Boxes(SpokenScene):
    def construct(self):
        parents = VGroup(coins("Aa", -3.43, 1.09), coins("Aa", -3.43, -0.85))
        cells, terms, headers = punnett()
        lanes = VGroup(*(tray(10.95, 1.68, 0, y) for y in (1.09, -0.85)))
        hybrids = VGroup(*(seed(pt(3.21, y), 0.48) for y in (1.09, -0.85)))
        self.add(table(), lanes, hybrids, parents, scope_tag(size=28, color=TEXT))
        drift_in_cells(hybrids, amp=0.26)
        self.at("two copies")
        self.play(LaggedStart(*(Indicate(pair, color=BLUE, scale_factor=1.20) for pair in parents),
                              lag_ratio=0.62), run_time=2.8)
        versions = label("Alleles", -3.43, 2.39, 36, GOLD)
        self.at("called alleles")
        self.play(FadeIn(versions), run_time=0.45)
        hybrid = label("Heterozygotes", -3.43, 2.39, 34, GOLD)
        self.at("hybrid with 2")
        self.play(*(pair[1].animate.shift(RIGHT * 0.46) for pair in parents), run_time=1.6)
        self.at("is a heterozygote")
        self.play(swap(versions, hybrid), run_time=0.8)
        self.at("Segregation deals")
        gamete_labels = VGroup(label("Eggs", -1.32, 1.09, 28), label("Pollen", -1.32, -0.85, 28))
        self.play(FadeIn(gamete_labels),
                  *(pair[0].animate.shift(LEFT * 0.32) for pair in parents), run_time=1.55)
        self.at("fair coin toss")
        self.play(LaggedStart(*(Indicate(pair, scale_factor=1.14, color=GOLD) for pair in parents),
                              lag_ratio=0.5), run_time=1.25)
        self.at("fill 4 equal")
        self.play(FadeOut(lanes), FadeOut(hybrids), run_time=0.35)
        self.play(LaggedStart(*(GrowFromCenter(cell) for cell in cells), lag_ratio=0.23),
                  FadeIn(headers), run_time=1.3)
        self.play(LaggedStart(*(FadeIn(term) for term in terms), lag_ratio=0.25), run_time=1.36)
        self.at("complete dominance")
        self.play(FadeOut(terms), FadeOut(gamete_labels), FadeOut(parents), FadeOut(hybrid), run_time=0.45)
        tokens = pea_tokens(cells, (1, 1, 1, 3), 0.56)
        self.play(fill_cells(cells, (1, 1, 1, 3), tokens, 2.45))
        drift_in_cells(tokens)
        self.at("3 round")
        self.play(FadeIn(boxed_label("3 round · 1 wrinkled", GOLD, size=31).move_to(pt(-3.25, 0.1))),
                  run_time=0.65)
        self.finish()


class S06TwoTraits(SpokenScene):
    def construct(self):
        world = single_world()
        observed = number("2.96:1", -3.25, 0.82, 52, BLUE)
        expected = number("3:1", -3.25, -0.75, 52, GOLD)
        ratio = boxed_label("3 round · 1 wrinkled", GOLD, size=31).move_to(pt(-3.25, 0.1))
        self.add(table(), world, ratio, scope_tag(size=28, color=TEXT))
        drift_in_cells(world[1])
        self.at("comparing offspring counts")
        self.play(FadeOut(ratio), run_time=0.4)
        observed_caption = label("Counted", -3.25, 1.46, 29, BLUE)
        self.play(FadeIn(observed), FadeIn(observed_caption), run_time=0.6)
        self.at("expected probabilities")
        expected_caption = label("Predicted", -3.25, -0.11, 29, GOLD)
        self.play(FadeIn(expected), FadeIn(expected_caption), run_time=0.64)
        self.at("Add an unlinked")
        self.play(FadeOut(observed), FadeOut(expected), FadeOut(observed_caption), FadeOut(expected_caption),
                  run_time=0.45)
        parents = VGroup(coins("AaBb", -3.32, 1.06), coins("AaBb", -3.32, -0.82))
        self.play(FadeIn(parents), run_time=0.78)
        self.at("its own coin")
        self.play(LaggedStart(*(Indicate(pair, color=GOLD, scale_factor=1.10) for pair in parents),
                              lag_ratio=0.55), run_time=1.7)
        cells, terms, headers = punnett(GAMETES)
        self.at("4 gamete types")
        self.play(FadeOut(world[1]), FadeOut(world[2]), run_time=0.38)
        self.play(ReplacementTransform(world[0], cells), FadeIn(headers), run_time=1.38)
        self.at("quarter each")
        fourth = label("¼ each", -3.32, -1.96, 37, GOLD)
        self.play(FadeIn(fourth), run_time=0.50)
        self.at("dealing 16")
        self.play(LaggedStart(*(FadeIn(term) for term in terms), lag_ratio=0.10), run_time=2.10)
        self.at("Dominance groups")
        self.play(FadeOut(terms), FadeOut(parents), FadeOut(fourth), run_time=0.45)
        groups = tuple(pea_class(genotype(a, b)) for a, b in product(GAMETES, repeat=2))
        phenotype_ratio = VGroup(*(VGroup(seed(radius=0.24, wrinkled=i >= 2,
                                               color=GREEN if i % 2 else YELLOW),
                                           number(str(groups.count(i)), 0, 0, 35, GOLD)).arrange(RIGHT, buff=0.23)
                                  for i in range(4))).arrange(RIGHT, buff=0.4).move_to(pt(-3.13, 0.22))
        self.play(fill_cells(cells, groups, pea_tokens(cells, groups, 0.27), 1.0),
                  FadeIn(phenotype_ratio, run_time=0.75))
        self.finish()


def chart_grid():
    cells, _, _ = punnett(GAMETES)
    groups = tuple(pea_class(genotype(a, b)) for a, b in product(GAMETES, repeat=2))
    for cell, group in zip(cells, groups):
        cell.set_fill(GREEN if group % 2 else YELLOW, 0.34)
    return VGroup(cells, pea_tokens(cells, groups, 0.27))


def two_trait_chart():
    """The same measured and predicted bars in the question, pause, and answer."""
    plot = Plot(box=(-5.45, 5.92, -1.80, 2.22), xr=(0, 4), yr=(0, 350),
                yticks=((0, "0"), (100, "100"), (200, "200"), (300, "300")), size=28)
    expected = [sum(OBSERVED) * share / 16 for share in (9, 3, 3, 1)]
    seen, model, seen_text, model_text, differences, headings = (VGroup() for _ in range(6))
    for i, (value, prediction, trait) in enumerate(zip(OBSERVED, expected, CLASSES)):
        x = i + 0.5
        seen.add(tally_bar(plot, x - 0.24, value, BLUE, 1.16))
        model.add(tally_bar(plot, x + 0.24, prediction, GOLD, 1.16))
        seen_text.add(number(str(value), seen[-1].get_x(), seen[-1].get_top()[1] + 0.34, 28, BLUE))
        model_text.add(number(f"{prediction:.2f}", model[-1].get_x(), model[-1].get_top()[1] + 0.44, 28, GOLD))
        low = plot.pt(x, min(value, prediction))
        high = plot.pt(x, max(value, prediction))
        differences.add(Line(low + DOWN * 0.07, high + UP * 0.07, stroke_width=5, color=TEXT))
        headings.add(label(trait.replace(" ", "\n"), plot.pt(x, 0)[0], -2.43, 28))
    key = VGroup(label("Observed", -4.03, -3.27, 29, BLUE), label("Expected", -1.76, -3.27, 29, GOLD))
    return plot, seen, model, seen_text, model_text, differences, headings, key


def miniature_grid():
    return chart_grid().scale(0.45).move_to(pt(4.63, 1.23))


def comparison_world():
    return VGroup(*two_trait_chart())


class S07PredictQ(SpokenScene):
    def construct(self):
        plot, seen, model, seen_text, model_text, differences, headings, key = two_trait_chart()
        miniature = chart_grid()
        self.add(table(), miniature)
        self.at("Mendel counted")
        count = number(f"{sum(OBSERVED)} seeds", -3.08, 0.55, 44, BLUE)
        self.play(Write(count), run_time=1.3)
        self.at("across those 4")
        self.play(Transform(miniature, miniature_grid()), FadeOut(count), run_time=0.74)
        self.play(Create(plot), FadeIn(headings), FadeIn(key[0]), run_time=1.15)
        cues = ("315", "108", "101", "32")
        for i, cue in enumerate(cues):
            self.at(cue)
            self.play(GrowFromEdge(seen[i], DOWN), run_time=0.55)
            self.play(FadeIn(seen_text[i]), run_time=0.22)
        self.at("9 sixteenths")
        left_math, n, result = VGroup(*(M(part, 31, GOLD) for part in ("9/16 ×", "556", "= 312.75"))
                                      ).arrange(RIGHT, buff=0.27).move_to(pt(3.72, 2.95))
        self.play(FadeIn(left_math), FadeIn(key[1]), run_time=0.65)
        self.at("of 556")
        self.play(FadeIn(n), run_time=0.55)
        self.at("312 .75")
        self.play(FadeIn(result), GrowFromEdge(model[0], DOWN), run_time=1.20)
        self.play(FadeIn(model_text[0]), run_time=0.35)
        self.at("round yellow")
        self.play(LaggedStart(*(AnimationGroup(GrowFromEdge(model[i], DOWN), FadeIn(model_text[i]))
                                for i in range(1, 4)), lag_ratio=0.35), run_time=1.35)
        self.at("None matched exactly")
        self.play(LaggedStart(*(Create(mark) for mark in differences), lag_ratio=0.33), run_time=1.35)
        self.at("Does that mismatch")
        self.play(FadeOut(left_math), FadeOut(n), FadeOut(result), run_time=0.36)
        self.play(FadeIn(question_card(QUESTION, **QUESTION_LAYOUT)), run_time=0.65)
        self.finish()


class S08PredictPause(PredictPause):
    QUESTION = QUESTION
    CARD = QUESTION_LAYOUT
    SECONDS = 4.5

    def backdrop(self):
        return VGroup(table(), comparison_world(), miniature_grid())

    def construct(self):
        self.add(self.backdrop(), question_card(self.QUESTION, **self.CARD))
        left, width, y = 0.59, 5.55, -3.29
        remaining = ValueTracker(width)
        self.add(tray(width + 0.10, 0.33, left + width / 2, y))

        def remaining_bar():
            span = max(0.001, remaining.get_value())
            return Rectangle(width=span, height=0.24, stroke_width=0, fill_color=YELLOW,
                             fill_opacity=1).move_to(pt(left + span / 2, y))

        self.add(always_redraw(remaining_bar))
        self.play(remaining.animate.set_value(0), run_time=self.SECONDS, rate_func=linear)
        self.finish()


def score_gauge():
    rail = tray(4.25, 0.49, 3.22, -0.56)
    caution = RoundedRectangle(width=1.24, height=0.34, corner_radius=0.06,
                               stroke_width=0, fill_color=RED, fill_opacity=0.75).move_to(pt(4.63, -0.56))
    usual = RoundedRectangle(width=1.58, height=0.34, corner_radius=0.06,
                             stroke_width=0, fill_color=GOLD, fill_opacity=0.74).move_to(pt(1.98, -0.56))
    marker = Triangle(color=GOLD, fill_opacity=1, stroke_width=0).scale(0.13).rotate(PI)
    marker.move_to(pt(2.30, -0.05))
    return VGroup(rail, usual, caution, marker)


class S09Chisquare(SpokenScene):
    def construct(self):
        chart = comparison_world()
        q = question_card(QUESTION, **QUESTION_LAYOUT)
        miniature = miniature_grid()
        self.add(table(), chart, miniature, q)
        _, seen, model, _, _, differences, _, _ = chart
        self.at("Not by itself")
        answer = label("Counts vary from cross to cross", 0, 2.96, 33, GOLD)
        self.play(swap(q, answer, run_time=0.85), FadeOut(differences),
                  *(bar.animate.set_fill(GOLD, 0.57) for bar in model))
        self.at("predicts probabilities")
        self.play(*(bar.animate.set_fill(BLUE, 0.69) for bar in seen),
                  *(bar.animate.set_fill(GOLD, 0.86) for bar in model), run_time=0.68)
        bands = VGroup(*(RoundedRectangle(width=1.43, height=0.37, corner_radius=0.10,
                                          stroke_color=GOLD, stroke_width=3, fill_color=GOLD,
                                          fill_opacity=0.36).move_to(bar.get_top())
                         for bar in model))
        self.at("spread of counts")
        self.play(LaggedStart(*(GrowFromCenter(band) for band in bands), lag_ratio=0.25), run_time=1.7)
        schematic = scope_tag(size=28, color=TEXT)
        self.play(FadeIn(schematic), run_time=0.36)
        self.at("score tests")
        gauge = score_gauge()
        self.play(FadeOut(chart), FadeOut(bands), FadeOut(miniature), FadeOut(answer), run_time=0.56)
        markers = VGroup(*(seed(pt(-4.42 + 1.42 * (i % 2), 0.80 - 1.65 * (i // 2)), 0.46,
                                i >= 2, GREEN if i % 2 else YELLOW) for i in range(4)))
        left_tray = tray(3.94, 3.84, -3.70, 0.08)
        self.play(FadeIn(left_tray), FadeIn(markers), GrowFromCenter(gauge[0]), FadeIn(gauge[1]),
                  run_time=1.6)
        drift_in_cells(markers, amp=0.07)
        title = label("Chi-square score", 3.22, 1.96, 36)
        self.play(FadeIn(title), run_time=0.55)
        average = label("Average if the ratio holds", 3.22, 0.97, 28, GOLD)
        self.at("fixed ratio holds")
        self.play(FadeIn(average), FadeIn(gauge[3], shift=DOWN * 0.20), run_time=1.1)
        formula = number("classes − 1", 3.22, 0.48, 34, GOLD)
        self.at("classes minus one")
        self.play(Write(formula), run_time=0.95)
        self.at("or 3 here")
        equation = number("4 − 1 = 3", 3.22, 0.48, 36, GOLD)
        self.play(swap(formula, equation, run_time=0.95))
        self.at("Higher scores")
        self.play(GrowFromEdge(gauge[2], LEFT), run_time=1.10)
        self.at("reason to doubt")
        caution = label("Reason to doubt", 4.16, -1.20, 30, RED)
        self.play(FadeIn(caution), run_time=0.61)
        self.finish()


class S10Limits(SpokenScene):
    def construct(self):
        world = single_world()
        self.add(table(), world, scope_tag(size=28, color=TEXT))
        drift_in_cells(world[1])
        heading = label("Hidden assumptions", -3.42, 2.19, 34, GOLD)
        self.at("Hidden assumptions")
        chromosome = RoundedRectangle(width=4.74, height=0.54, corner_radius=0.21,
                                      fill_color=BLUE, fill_opacity=0.35, stroke_color=BLUE,
                                      stroke_width=2).move_to(pt(-3.34, 0.71))
        loci = VGroup(Dot(pt(-3.63, 0.71), radius=0.16, color=GOLD),
                      Dot(pt(-3.04, 0.71), radius=0.16, color=PURPLE))
        self.play(FadeIn(heading), GrowFromCenter(chromosome), run_time=1.05)
        self.at("Genes close together")
        self.play(FadeIn(loci), run_time=0.55)
        self.at("travel together")
        self.play(VGroup(chromosome, loci).animate.shift(DOWN * 1.45), run_time=2.7)
        self.at("Standard ratios")
        self.play(FadeOut(VGroup(chromosome, loci)), FadeOut(heading), run_time=0.52)
        checks = [
            ("equal survival", "Equal survival"),
            ("equal transmission", "Equal transmission"),
            ("accurate scoring", "Accurate scoring"),
        ]
        old = None
        for i, (cue, text) in enumerate(checks):
            self.at(cue)
            check = label(text, -3.38, 0.64, 34, GOLD)
            if i == 0:
                world[1][3].save_state()
                self.play(FadeIn(check), world[0][3].animate.set_fill(TABLE, 1),
                          world[1][3].animate.set_opacity(0.20), run_time=0.95)
            elif i == 1:
                self.play(swap(old, check, run_time=0.76), Restore(world[1][3]),
                          world[0][3].animate.set_fill(GREEN, 0.34))
            else:
                self.play(swap(old, check, run_time=0.76))
            old = check
        self.at("Swapping which parent")
        parents = VGroup(seed(pt(-4.84, -0.68), 0.53), seed(pt(-2.08, -0.68), 0.53, True))
        self.play(FadeOut(old), FadeIn(parents), run_time=0.63)
        a, b = (pea.get_center() for pea in parents)
        self.play(MoveAlongPath(parents[0], ArcBetweenPoints(a, b, angle=1.65)),
                  MoveAlongPath(parents[1], ArcBetweenPoints(b, a, angle=1.65)),
                  run_time=2.05)
        self.at("parental origin")
        self.play(FadeIn(label("Parental origin", -3.45, 1.10, 34, GOLD)), run_time=0.6)
        self.finish()


def mouse(center, yellow):
    coat = YELLOW if yellow else GREY
    tail = Arc(radius=0.42, start_angle=-0.22, angle=1.75, color=coat, stroke_width=4).move_to(pt(-0.67, -0.17))
    body = Ellipse(width=0.95, height=0.58, color=coat, fill_opacity=0.83).move_to(pt(-0.17, -0.05))
    head = Ellipse(width=0.60, height=0.43, color=coat, fill_opacity=1).move_to(pt(0.41, 0.04))
    ear = Circle(radius=0.15, color=coat, fill_opacity=0.94).move_to(pt(0.26, 0.22))
    eye = Dot(pt(0.49, 0.10), radius=0.037, color=BG)
    nose = Dot(pt(0.70, 0.015), radius=0.043, color=TEXT)
    return VGroup(tail, body, head, ear, eye, nose).move_to(center)


class S11UnlockedA(SpokenScene):
    def construct(self):
        world = single_world()
        self.add(table(), world, scope_tag(size=28, color=TEXT))
        drift_in_cells(world[1])
        mendel = label("Mendel", -3.38, 1.34, 45, GOLD)
        trait = label("Segregation", -3.38, 0.38, 34)
        self.at("Mendel's pea")
        self.play(FadeIn(mendel), run_time=0.65)
        self.at("read as segregation")
        self.play(FadeIn(trait), LaggedStart(*(Indicate(seed, color=GREEN, scale_factor=1.10) for seed in world[1]),
                                             lag_ratio=0.48), run_time=1.88)
        self.at("independent assortment")
        next_trait = label("Independent assortment", -3.38, 0.38, 29)
        assorted = chart_grid()
        self.play(swap(trait, next_trait),
                  Succession(FadeOut(world, run_time=0.42), FadeIn(assorted, run_time=0.59)))
        self.at("first years")
        self.play(FadeOut(mendel), FadeOut(next_trait), FadeOut(assorted), run_time=0.60)
        cells, _, _ = punnett()
        cuenot = label("Lucien Cuénot", -3.38, 1.34, 41, GOLD)
        self.play(FadeIn(cuenot), FadeIn(cells), run_time=0.72)
        self.at("mouse crosses")
        mice = VGroup(*(mouse(cell.get_center() + UP * 0.24, i < 3) for i, cell in enumerate(cells)))
        genes = VGroup(*(number(gene, cell.get_x(), cell.get_y() - 0.54, 29, GOLD if i < 3 else TEXT)
                         for i, (cell, gene) in enumerate(zip(cells, ("YY", "Yy", "Yy", "yy")))))
        self.play(LaggedStart(*(AnimationGroup(FadeIn(m), FadeIn(g)) for m, g in zip(mice, genes)),
                              lag_ratio=0.35), run_time=2.4)
        drift_in_cells(mice, amp=0.15)
        self.at("They did not")
        self.play(Indicate(cells[0], color=RED, scale_factor=1.0), run_time=1.5)
        self.at("2 yellow alleles")
        self.play(FadeOut(mice[0], shift=DOWN * 0.26), cells[0].animate.set_fill("#151D25", 1),
                  run_time=1.35)
        self.at("dropping 1 box")
        dies = label("dies", cells[0].get_x(), cells[0].get_y() + 0.20, 31, RED)
        self.play(FadeIn(dies), run_time=0.55)
        self.at("live yellow")
        self.play(LaggedStart(*(Indicate(m, color=YELLOW, scale_factor=1.14) for m in mice[1:3]),
                              lag_ratio=0.55), run_time=1.25)
        self.at("a heterozygote")
        self.play(FadeIn(label("Live yellow mice are Yy", -3.38, 0.38, 31, GOLD)), run_time=0.55)
        self.finish()


def fly(center, red_eyes, scale=1):
    eye_color = RED if red_eyes else TEXT
    wings = VGroup(*(Ellipse(width=0.61, height=1.52, color=BLUE, fill_opacity=0.46, stroke_width=3)
                     .rotate(side * 0.60).move_to(pt(side * 0.43, -0.25)) for side in (-1, 1)))
    body = Ellipse(width=0.42, height=1.17, color=GOLD, fill_opacity=0.9, stroke_width=2)
    head = Circle(radius=0.25, color=GOLD, fill_opacity=0.9, stroke_width=2).shift(UP * 0.49)
    eyes = VGroup(*(Dot(pt(side * 0.175, 0.54), radius=0.14, color=eye_color) for side in (-1, 1)))
    return VGroup(wings, body, head, eyes).scale(scale).move_to(center)


class S12UnlockedB(SpokenScene):
    def construct(self):
        slots = VGroup(*(tray(4.58, 2.65, x, y) for y in (1.37, -1.49) for x in (-3.10, 3.10)))
        context = label("Morgan · Columbia University", 0, 3.23, 35, GOLD)
        tag = scope_tag(size=28, color=TEXT)
        self.add(table(), slots[:2], context, tag)
        male = fly(pt(-3.1, 1.61), False, 1.09)
        female = fly(pt(3.1, 1.61), True, 1.09)
        self.at("Columbia University")
        self.play(GrowFromCenter(male), run_time=1.20)
        self.at("white eyed Drosophila")
        male_label = label("White-eyed male", -3.1, 0.42, 30)
        self.play(FadeIn(male_label), run_time=0.43)
        self.at("red eyed females")
        self.play(GrowFromCenter(female), run_time=0.86)
        female_label = label("Red-eyed female line", 3.1, 0.42, 30)
        self.play(FadeIn(female_label), run_time=0.46)
        self.at("offspring of both")
        cross = label("×", 0, 1.57, 52, GOLD)
        self.add(cross)
        self.play(FadeIn(slots[2:]), run_time=0.46)
        young = VGroup(fly(pt(-3.1, -1.26), True, 0.94), fly(pt(3.1, -1.26), True, 0.94))
        self.play(LaggedStart(*(FadeIn(child, shift=DOWN * 0.38) for child in young), lag_ratio=0.55),
                  run_time=0.95)
        labels = VGroup(label("Red-eyed son", -3.1, -2.41, 30), label("Red-eyed daughter", 3.1, -2.41, 30))
        self.play(FadeIn(labels), run_time=0.5)
        self.at("white is recessive")
        rule = label("White is recessive", 0, -3.22, 35, GOLD)
        self.play(FadeIn(rule), run_time=0.56)
        self.at("work in Science")
        article = label("Science · Sex-limited inheritance", 0, 3.23, 35, GOLD)
        self.play(swap(context, article), run_time=1.1)
        self.at("Fitting or breaking")
        figures = VGroup(slots, male, female, young, cross, male_label, female_label, labels, tag)
        self.play(FadeOut(figures), FadeOut(article), FadeOut(rule), run_time=0.65)
        world = single_world()
        gauge = score_gauge().shift(LEFT * 6.5 + UP * 0.56)
        self.play(FadeIn(world, shift=UP * 0.18), GrowFromCenter(gauge), run_time=1.44)
        self.at("counts expose")
        self.play(FadeIn(label("Compare counts to probabilities", -3.26, 0.95, 29, GOLD)), run_time=0.70)
        self.finish()


class S13End(EndCard):
    LINE = "Planned crosses test inheritance rules by comparing offspring counts to probability."
