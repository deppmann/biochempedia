"""Population genetics teaching film.

Gold and teal are A and a. Grey is structure and the neutral reference, white
is the measured mean, blue is a directional change, and red rejects a hypothesis.
Purple and green complete the four-color palette for the cell lineage example.
"""
from bp_parts import *  # noqa: F403
from bp_style import EndCard


AMBER = GOLD
PURPLE = "#B58CD9"
PANEL = "#273444"
DARK_AMBER = "#644622"
DARK_TEAL = "#23565B"
START = 0.5
GENERATIONS = 20


def point(x, y):
    return np.array([x, y, 0.0])


def plate(w, h, x, y, color=PANEL, stroke=0, opacity=1):
    return RoundedRectangle(width=w, height=h, corner_radius=0.22,
                            stroke_color=GREY, stroke_width=stroke,
                            fill_color=color, fill_opacity=opacity).move_to(point(x, y))


def bead(x, y, color, radius=0.24):
    return Dot(point(x, y), radius=radius, color=color, stroke_color=BG, stroke_width=1.5)


def heading(words, x=0, y=3.22, color=TEXT, size=38, width=10):
    return fit_text(words, max_w=width, size=size, min_size=28,
                    color=color, weight=BOLD).move_to(point(x, y))


def label(words, x, y, color=TEXT, size=32):
    return T(words, size, color).move_to(point(x, y))


def sway(dots, amp=0.14, speed=2.0):
    for i, dot in enumerate(dots):
        bob(dot, amp=amp, speed=speed, seed=i)


def paths(seed, n=8, gene_flow=0):
    """Wright–Fisher sampling of 2N copies, optionally after mixing in migrants."""
    rng = np.random.default_rng(seed)
    samples = np.full((n, GENERATIONS + 1), START)
    for g in range(GENERATIONS):
        probability = samples[:, g] * (1 - gene_flow) + 0.90 * gene_flow
        samples[:, g + 1] = rng.binomial(24, probability) / 24
    return samples


# Seed 23 supplies the neutral ensemble used throughout the film.
NEUTRAL = paths(23)
FLOW = paths(23, gene_flow=0.22)
RISING = int(np.argmax(NEUTRAL[:, -1]))

# Each row is a chosen, possible history under the same sampling rule. The
# two-example ending of the sampling scene pairs an increase with a loss.
def small_pool_history():
    rng = np.random.default_rng(5899)
    copies = [6]
    for _ in range(8):
        copies.append(rng.binomial(12, copies[-1] / 12))
    return np.array(copies) / 12


SMALL_POOL = small_pool_history()


def curve(plot, series, color, width, opacity=1):
    x = np.arange(len(series))
    return plot.curve(lambda t: np.interp(t, x, series), x0=0, x1=x[-1],
                      n=len(x), color=color, width=width, opacity=opacity)


def frequency_axis():
    return Plot(box=(0.7, 6.05, -2.05, 2.33), xr=(0, GENERATIONS), yr=(0, 1),
                yticks=[0, 1], xlabel="Generations", size=29, label_size=29,
                color=TEXT)


def frequency_stage():
    return VGroup(plate(6.25, 5.7, 3.35, 0.03),
                  heading("A frequency", 3.36, 2.66, AMBER, size=30))


def large_pool(frequency):
    rng = np.random.default_rng(20)
    dots = VGroup()
    order = rng.permutation(48)
    for i in range(48):
        row, col = divmod(i, 8)
        x = -3.38 + (col - 3.5) * 0.61 + rng.uniform(-0.09, 0.09)
        y = 0.1 + (row - 2.5) * 0.72 + rng.uniform(-0.12, 0.12)
        color = AMBER if order[i] < round(frequency * 48) else TEAL
        dots.add(bead(x, y, color, 0.22))
    return dots, order


def pool_stage():
    return plate(5.63, 5.7, -3.39, 0.03)


class S01Hook(SpokenScene):
    def construct(self):
        plot = frequency_axis()
        t = ValueTracker(0)
        series = NEUTRAL[RISING]
        sample = lambda: np.interp(t.get_value(), np.arange(len(series)), series)
        dots, order = large_pool(START)
        sway(dots)
        for i, dot in enumerate(dots):
            def color_copy(mob, rank=order[i]):
                mob.set_fill(AMBER if rank < round(sample() * 48) else TEAL)
            dot.add_updater(color_copy)
        line = plot.live_curve(lambda x: np.interp(x, np.arange(len(series)), series), t, AMBER, 6)
        marker = plot.dot(t.get_value, sample, color=AMBER, ring=TEXT)
        question = heading("Selection or luck?", -2.95, 3.25, AMBER, size=42)

        self.at("when one version")
        self.add(pool_stage(), frequency_stage(), plot, dots, line, marker)
        self.play(t.animate(rate_func=linear).set_value(7),
                  run_time=2.45)
        self.at("did selection")
        self.play(FadeIn(question), run_time=0.42)
        self.at("population genetic models")
        self.play(t.animate.set_value(GENERATIONS), run_time=3.5, rate_func=linear)
        self.finish()


class S02Title(TitleCard):
    LESSON = "Population Genetics: Hardy-Weinberg and Evolutionary Forces"
    TITLE = "Telling Luck From Cause in Populations"

    def construct(self):
        pool, _ = large_pool(NEUTRAL[RISING, -1])
        for i, dot in enumerate(pool):
            row, col = divmod(i, 12)
            y = (2.24, 2.95, -2.24, -2.95)[row]
            dot.move_to(point(-5.86 + 1.06 * col, y + 0.10 * np.sin(i * 1.8)))
            dot.set_opacity(0.27)
        sway(pool, amp=0.14)
        self.add(pool)
        super().construct()


def chromosome_pair(x, y, colors):
    rails = VGroup(*[plate(0.43, 1.76, x + dx, y, "#35485C")
                     for dx in (-0.31, 0.31)])
    copies = VGroup(*[bead(x + dx, y + 0.16, color, 0.24)
                      for dx, color in zip((-0.31, 0.31), colors)])
    return VGroup(rails, copies)


def allele_strip(x=0, y=-1.85, w=10.8, h=0.64):
    segs = VGroup(*[Rectangle(width=w / 2, height=h, stroke_width=0,
                              fill_color=c, fill_opacity=1).move_to(point(x + d * w / 4, y))
                    for d, c in ((-1, DARK_AMBER), (1, DARK_TEAL))])
    letters = VGroup(label("p", x - w / 4, y, AMBER, 32),
                     label("q", x + w / 4, y, TEAL, 32))
    return VGroup(segs, letters)


class S03Alleles(SpokenScene):
    def construct(self):
        pairs = VGroup(*[chromosome_pair(x, y, (AMBER, TEAL) if i % 2 else (TEAL, AMBER))
                         for i, (x, y) in enumerate((x, y) for y in (1.6, -0.50)
                                                     for x in (-3.9, -1.95, 0, 1.95, 3.9))])
        locus = heading("One locus", -3.75, 3.22, TEXT)
        legend = heading("Alleles", 2.95, 3.22, TEXT)
        letters = VGroup(chip("A", AMBER, size=35), chip("a", TEAL, size=35))
        letters.arrange(DOWN, buff=0.34).move_to(point(5.28, 0.65))
        strip = allele_strip(y=-2.05)
        total = caption("p + q = 1", size=40)

        self.at("at one locus")
        self.add(plate(11.75, 4.6, 0, 0.53))
        self.play(LaggedStart(*[FadeIn(pair, shift=UP * 0.16) for pair in pairs],
                              lag_ratio=0.12), run_time=1.4)
        self.play(FadeIn(locus), run_time=0.4)
        for i, pair in enumerate(pairs):
            sway(pair[1], amp=0.10, speed=2.6 + 0.10 * i)
        self.at("called alleles")
        self.play(FadeIn(legend), run_time=0.36)
        self.at("two alleles")
        self.play(FadeIn(letters[0]), run_time=0.48)
        self.at("and little")
        self.play(FadeIn(letters[1]), run_time=0.42)
        self.at("allele frequencies")
        self.play(GrowFromCenter(strip[0]), run_time=0.6)
        self.play(FadeIn(strip[1]), run_time=0.4)
        self.at("together")
        self.play(FadeIn(total), run_time=0.65)
        self.finish()


SQUARE_X = -2.48
SQUARE_Y = -0.35
TILE = 2.28
STEP = 2.43
TILE_DATA = (
    ("AA = p × p", DARK_AMBER, AMBER, -1, 1),
    ("Aa = p × q", DARK_AMBER, TEXT, 1, 1),
    ("Aa = q × p", DARK_TEAL, TEXT, -1, -1),
    ("aa = q × q", DARK_TEAL, TEAL, 1, -1),
)


def tile_halves(x, y, size=TILE, first=DARK_AMBER, second=DARK_TEAL):
    return VGroup(*[Rectangle(width=size / 2, height=size, stroke_width=0,
                              fill_color=color, fill_opacity=1)
                    .move_to(point(x + sign * size / 4, y))
                    for sign, color in ((-1, first), (1, second))])


def hardy_square():
    grid, fills, formulas, copies = VGroup(), VGroup(), VGroup(), VGroup()
    for i, (formula, tint, color, dx, dy) in enumerate(TILE_DATA):
        x, y = SQUARE_X + dx * STEP / 2, SQUARE_Y + dy * STEP / 2
        grid.add(Rectangle(width=TILE, height=TILE, stroke_width=1.5, stroke_color=GREY,
                           fill_color=PANEL, fill_opacity=1).move_to(point(x, y)))
        fill = tile_halves(x, y, first=tint, second=tint if i in (0, 3)
                           else (DARK_TEAL if i == 1 else DARK_AMBER))
        fills.add(fill)
        formulas.add(label(formula, x, y + 0.51, color, 30).set_z_index(3))
        a, b = ((AMBER, AMBER), (AMBER, TEAL), (TEAL, AMBER), (TEAL, TEAL))[i]
        copies.add(VGroup(bead(x - 0.36, y - 0.43, a, 0.25),
                          bead(x + 0.36, y - 0.43, b, 0.25)))
    top = VGroup(*[plate(TILE, 0.39, SQUARE_X + s * STEP / 2, 2.27, c)
                   for s, c in ((-1, DARK_AMBER), (1, DARK_TEAL))])
    left = VGroup(*[plate(0.45, TILE, -5.27, SQUARE_Y + s * STEP / 2, c)
                    for s, c in ((1, DARK_AMBER), (-1, DARK_TEAL))])
    marks = VGroup(*[
        label(letter, x, y, color, 29)
        for letter, color, x, y in (
            ("p", AMBER, SQUARE_X - STEP / 2, 2.28),
            ("q", TEAL, SQUARE_X + STEP / 2, 2.28),
            ("p", AMBER, -5.27, SQUARE_Y + STEP / 2),
            ("q", TEAL, -5.27, SQUARE_Y - STEP / 2),
            ("Sperm", TEXT, SQUARE_X, 2.76),
            ("Eggs", TEXT, -5.73, -0.35),
        )
    ])
    marks[-1].rotate(PI / 2)
    return grid, fills, formulas, copies, top, left, marks


def hardy_heading():
    return heading("Hardy-Weinberg proportions", -0.80, 3.32, size=39)


def parent_row(x, y, colors, radius=0.26):
    tray = plate(3.8, 0.75, x, y, PANEL)
    dots = VGroup(*[bead(x + (i - (len(colors) - 1) / 2) * 0.62, y, color, radius)
                    for i, color in enumerate(colors)])
    return VGroup(tray, dots)


class S04HwSquare(SpokenScene):
    def construct(self):
        grid, fills, formulas, copies, top, left, marks = hardy_square()
        panels = VGroup(*(parent_row(3.22, 1.52 - i * 1.12, colors)
                          for i, colors in enumerate(((AMBER, TEAL, TEAL, AMBER),
                                                       (TEAL, AMBER, AMBER, TEAL),
                                                       (TEAL, AMBER, TEAL, AMBER)))))
        strip = allele_strip(3.22, -2.18, 4.24, 0.54)
        random_label = heading("Random mating", 3.22, 2.22, size=32)
        conditions = label("No selection, mutation, or migration", 3.22, -3.01, TEXT, 28)
        pair_label = heading("Pair by chance", 3.22, 2.22, size=33)

        first_strip = allele_strip(y=-2.05)
        strip_total = caption("p + q = 1", size=40)
        self.at("for hardy")
        self.add(first_strip, strip_total)
        self.play(ReplacementTransform(first_strip, strip), FadeOut(strip_total), run_time=0.66)
        self.play(FadeIn(grid), FadeIn(hardy_heading()), run_time=0.65)
        self.at("large population")
        self.play(LaggedStart(*[FadeIn(row) for row in panels], lag_ratio=0.25),
                  FadeIn(random_label), run_time=1.45)
        for i, row in enumerate(panels):
            sway(row[1], amp=0.12, speed=2.2 + i * 0.3)
        self.at("with no selection")
        self.play(FadeIn(conditions), run_time=0.45)
        self.at("eggs and sperm")
        strip[1].set_z_index(3)
        self.play(swap(random_label, pair_label), FadeOut(conditions),
                  TransformFromCopy(strip[0], top), run_time=0.72)
        self.play(TransformFromCopy(strip[0], left), run_time=0.65)
        self.play(FadeIn(marks), run_time=0.57)
        self.at("multiply their frequencies")
        parent_draws = VGroup(*[row[1][j].copy().clear_updaters()
                                for row, j in ((panels[0], 0), (panels[1], 1))])
        self.add(parent_draws)
        self.play(*[dot.animate.move_to(target.get_center())
                    for dot, target in zip(parent_draws, copies[0])], run_time=2.25)
        self.remove(parent_draws)
        self.add(copies[0])
        self.at("big a big a")
        self.play(FadeIn(fills[0]), FadeIn(formulas[0]), run_time=0.62)
        self.bring_to_front(copies[0])
        self.at("q times q")
        self.play(FadeIn(fills[3]), run_time=0.38)
        self.play(FadeIn(copies[3]), FadeIn(formulas[3]), run_time=0.52)
        self.at("forms both ways")
        self.play(FadeIn(fills[1]), FadeIn(copies[1]), run_time=0.55)
        self.play(FadeIn(fills[2]), FadeIn(copies[2]), run_time=0.55)
        self.at("p times q plus")
        self.play(FadeIn(formulas[1]), run_time=0.52)
        self.at("plus q times")
        self.play(FadeIn(formulas[2]), run_time=0.55)
        self.play(FadeOut(VGroup(panels, pair_label, strip)), run_time=0.48)
        self.finish()


class S05Recount(SpokenScene):
    def construct(self):
        grid, fills, formulas, copies, top, left, marks = hardy_square()
        hw = hardy_heading()
        count = heading("Count the A copies", 3.35, 2.13, AMBER, size=34)
        all_a = label("All A", 3.35, 1.58, AMBER, 31)
        two_pq = label("2pq", 3.35, -1.18, TEXT, 36)
        half_a = label("Half A → pq", 3.35, -1.18, AMBER, 36)
        edge = allele_strip(3.32, -2.30, 5.3, 0.61)
        edge_total = label("p + q = 1", 3.32, -3.03, TEXT, 31)
        capacity = plate(5.69, 5.05, 3.32, 0, PANEL)
        # Equal-sized heterozygote tiles meet edge to edge with their A halves
        # in the middle. Their joint left-to-right amber share is one half.
        a = tile_halves(2.41, -0.05, size=1.62, first=DARK_TEAL, second=DARK_AMBER)
        b = tile_halves(4.08, -0.05, size=1.62, first=DARK_AMBER, second=DARK_TEAL)
        contributions = VGroup(*[
            Rectangle(width=1.325, height=0.61, stroke_width=0, fill_color=color,
                      fill_opacity=1).move_to(point(x, -0.05))
            for x, color in ((1.33, DARK_AMBER), (2.655, AMBER))
        ])
        words = [label(s, 3.30, 1.22, AMBER, 40) for s in
                 ("p × p + p × q", "p × (p + q)", "p × 1", "p")]
        shuffle = VGroup(bead(1.68, 0.1, AMBER), bead(2.44, 0.10, TEAL),
                         bead(4.21, 0.1, TEAL), bead(4.97, 0.10, AMBER))
        rule = label("Same allele frequency", 3.32, 1.26, AMBER, 32)

        self.add(grid, fills, formulas, copies, top, left, marks, hw)
        light = ValueTracker(0)
        for i, fill in enumerate(fills[:3]):
            fill.add_updater(lambda mob, i=i: mob.set_fill(
                opacity=0.84 + 0.16 * np.sin(2.45 * light.get_value() + i)))
        self.add_updater(lambda dt: light.increment_value(dt))
        self.at("recount big")
        self.play(FadeIn(capacity), FadeIn(count), FadeOut(VGroup(formulas[3], copies[3])),
                  fills[3].animate.set_opacity(0.18), run_time=0.85)
        self.at("is all a")
        self.play(FadeIn(all_a), TransformFromCopy(fills[0], contributions[0]),
                  run_time=1.27)
        self.at("the two big")
        self.play(FadeOut(all_a), contributions[0].animate.shift(DOWN * 1.34),
                  TransformFromCopy(fills[1], b), TransformFromCopy(fills[2], a),
                  run_time=1.6)
        self.play(FadeIn(two_pq), run_time=0.48)
        self.at("half their copies")
        self.play(a[0].animate.set_opacity(0.22), b[1].animate.set_opacity(0.22),
                  swap(two_pq, half_a), run_time=1.05)
        self.at("that sums to")
        self.play(FadeOut(VGroup(half_a, a[0], b[1])), run_time=0.45)
        self.play(ReplacementTransform(VGroup(a[1], b[0]), contributions[1]),
                  contributions[0].animate.shift(UP * 1.34), run_time=0.7)
        self.play(FadeIn(words[0]), FadeIn(edge), run_time=0.52)
        self.play(swap(words[0], words[1]), run_time=0.70)
        self.at("since p plus q")
        self.play(FadeIn(edge_total), swap(words[1], words[2]), run_time=0.85)
        self.at("that stays p")
        self.play(swap(words[2], words[3]),
                  contributions.animate.set_color(AMBER).move_to(point(2, -1.34)),
                  run_time=1.05)
        self.at("mating reshuffles")
        self.play(swap(words[3], rule), FadeIn(shuffle), run_time=0.58)
        self.play(Swap(shuffle[1], shuffle[3], path_arc=PI / 2), run_time=1.2)
        self.play(Swap(shuffle[0], shuffle[2], path_arc=-PI / 2), run_time=1.15)
        self.finish()


def bag(x, y, count, amber, scale=1):
    shell = plate(5.0 * scale, 2.05 * scale, x, y, "#34475A", stroke=1.5)
    dots = VGroup()
    columns = (count + 1) // 2
    order = np.random.default_rng(7).permutation(count)
    for i in range(count):
        row, col = divmod(i, columns)
        dx = (col - (columns - 1) / 2) * min(0.67, 4.2 / columns)
        dots.add(bead(x + dx * scale, y + (0.37 - row * 0.74) * scale,
                      AMBER if order[i] < amber else TEAL, 0.24 * scale))
    return VGroup(shell, dots)


def small_pool_start():
    return bag(-3.40, 0.12, 12, 6)


class S06Drift(SpokenScene):
    def construct(self):
        plot = frequency_axis()
        left = pool_stage()
        square = hardy_square()
        tile_group = VGroup(square[0], square[1], square[3], square[4], square[5])
        tile_group.scale(0.82).move_to(point(-3.38, 0.03))
        current = small_pool_start()
        stage = frequency_stage()
        drift = heading("Genetic drift", -3.35, 3.20, AMBER, size=42)
        first = label("Which copy enters a gamete?", -3.39, 2.15, TEXT, 29)
        second = label("How many offspring?", -3.39, 2.15, TEXT, 30)
        equal = label("No fitness difference needed", -3.37, 2.12, TEXT, 28)
        parents = VGroup(parent_row(-3.38, 1.38, (AMBER, TEAL)),
                         parent_row(-3.38, -0.25, (TEAL, AMBER)),
                         parent_row(-3.38, -1.86, (AMBER, TEAL)))
        t = ValueTracker(0)
        series = SMALL_POOL
        interpolate = lambda x: np.interp(x, np.arange(len(series)), series)
        line = plot.live_curve(interpolate, t, AMBER, 5.5)
        marker = plot.dot(t.get_value, lambda: interpolate(t.get_value()), AMBER, TEXT)

        self.add(left, stage, plot, tile_group)
        self.at("in a small population")
        self.play(ReplacementTransform(tile_group, current), run_time=1.7)
        self.add(line, marker)
        self.at("chance sampling moves")
        self.play(t.animate.set_value(2), run_time=2.72, rate_func=linear)
        self.at("genetic drift")
        self.play(FadeIn(drift), run_time=0.52)
        sway(current[1], amp=0.14, speed=3)
        self.at("two chance steps")
        current[1].clear_updaters(recursive=True)
        self.play(FadeOut(current), LaggedStart(*[FadeIn(p) for p in parents], lag_ratio=0.2),
                  run_time=1.45)
        self.at("which parental copy")
        gametes = VGroup(*[p[1][i].copy() for p, i in zip(parents, (0, 0, 1))])
        self.add(gametes)
        self.play(*[dot.animate.move_to(point(-1.56, parent.get_y() - 0.51))
                    for dot, parent in zip(gametes, parents)], FadeIn(first), run_time=2.12)
        self.at("how many offspring")
        offspring = VGroup()
        for p, color, n in zip(parents, (AMBER, TEAL, TEAL), (3, 1, 0)):
            offspring.add(VGroup(*[bead(-4.04 + 0.64 * i, p.get_y() - 0.50,
                                        color, 0.18) for i in range(n)]))
        self.play(swap(first, second), run_time=0.55)
        self.play(LaggedStart(*[TransformFromCopy(gametes[i], offspring[i])
                                for i in (0, 1)], lag_ratio=0.65),
                  t.animate.set_value(3), run_time=2.32)
        self.at("drift needs no")
        current = bag(-3.40, 0.12, 12, 8)
        self.play(FadeOut(VGroup(parents, gametes, offspring)), FadeIn(current),
                  swap(second, equal), run_time=1.6)
        self.at("relative number")
        def recount(mob):
            order = np.random.default_rng(7).permutation(12)
            for rank, dot in zip(order, mob):
                dot.set_fill(AMBER if rank < round(12 * interpolate(t.get_value())) else TEAL)
        current[1].add_updater(recount)
        sway(current[1], amp=0.17, speed=2.8)
        self.play(t.animate.set_value(3.12), run_time=2.2)
        self.at("harmful alleles")
        rise = label("A harmful allele can rise", -3.40, -1.70, AMBER, 29)
        loss = label("A beneficial allele can vanish", -3.40, -1.70, AMBER, 28)
        self.play(FadeOut(equal), FadeIn(rise), t.animate.set_value(4), run_time=1.20)
        self.at("or beneficial")
        self.play(swap(rise, loss), t.animate(rate_func=linear).set_value(8), run_time=1.81)
        self.finish()


def replicate_pools():
    pools = VGroup(*[bag(-3.4, 1.65 - i * 1.59, 12, 6, 0.72) for i in range(3)])
    return pools


def starting_dots(plot):
    return VGroup(*[Circle(radius=0.115 + i * 0.069, color=color, stroke_width=3,
                           fill_opacity=0).move_to(plot.pt(0, START))
                    for i, color in enumerate((AMBER, TEAL, PURPLE))])


def predict_world():
    plot = frequency_axis()
    pools = replicate_pools()
    rings = starting_dots(plot)
    label_text = heading("Same starting frequency", -3.38, 3.23, TEXT, size=33)
    return VGroup(pool_stage(), frequency_stage(), plot, pools, rings, label_text), pools, rings, plot


def predict_question():
    return question_card("Spread? Average?", y=3.22, left=1.05, size=36, max_w=4.9)


class S07Predict(SpokenScene):
    def construct(self):
        world, pools, rings, plot = predict_world()
        self.add(*world[:3])
        current = small_pool_start()
        self.add(current)
        self.at("now start replicate")
        self.play(ReplacementTransform(current, pools[1]), run_time=0.88)
        self.play(TransformFromCopy(pools[1], pools[0]),
                  TransformFromCopy(pools[1], pools[2]), run_time=1.34)
        self.at("the same frequency")
        self.play(FadeIn(world[-1]), LaggedStart(*[Create(r) for r in rings],
                                               lag_ratio=0.25), run_time=1.15)
        settle = ValueTracker(1)
        for i, pool in enumerate(pools):
            for j, dot in enumerate(pool[1]):
                center = dot.get_center().copy()
                dot.add_updater(lambda m, dt, i=i, j=j, center=center: m.move_to(
                    center + UP * settle.get_value() * 0.14
                    * np.sin((2.6 + 0.20 * i) * self.elapsed() + 0.77 * j)))
        self.at("let only chance act")
        guide = plot.hline(START, color=GREY)
        self.play(Create(guide), run_time=2.65)
        self.play(FadeOut(guide), run_time=0.53)
        self.at("what happens to")
        self.play(FadeIn(predict_question()), run_time=0.52)
        # The centered question stays fixed as the beads settle into the pause frame.
        self.wait(max(0.01, self.narration_s - self.elapsed() - 0.34))
        self.play(settle.animate.set_value(0), rate_func=linear, run_time=0.69)
        self.finish()


class S08Pause(Scene):
    def construct(self):
        self.camera.background_color = BG
        world, _, _, _ = predict_world()
        self.add(world, predict_question())
        self.wait(4.5)


REPLICATE_COLORS = (TEAL, PURPLE, AMBER, BLUE, TEAL, PURPLE, AMBER, GREEN)


def model_lines(plot, data, directional=False):
    return VGroup(*[curve(plot, row, BLUE if directional else color, 3.3,
                          opacity=0.68 if directional else 0.83)
                    for color, row in zip(REPLICATE_COLORS, data)])


def revealed_lines(lines, amount):
    """Reveal all precomputed paths to the same fractional generation."""
    visible = VGroup(*[line.copy() for line in lines])
    for partial, full in zip(visible, lines):
        partial.pointwise_become_partial(full, 0, 0.00001)

        def reveal(mob, ref=full):
            mob.pointwise_become_partial(ref, 0, max(0.00001, amount.get_value()))
        partial.add_updater(reveal)
    return visible


def plot_key(words, color):
    return boxed_label(words, color, size=29, fill_opacity=0.08).move_to(point(-3.39, -2.05))


class S09Replicates(SpokenScene):
    def construct(self):
        world, pools, rings, plot = predict_world()
        question = predict_question()
        amount = ValueTracker(0)
        neutral = model_lines(plot, NEUTRAL)
        growing = revealed_lines(neutral, amount)
        average = curve(plot, NEUTRAL.mean(axis=0), TEXT, 6)
        live_average = revealed_lines(VGroup(average), amount)
        expected = plot.hline(START, color=GREY)
        null = plot_key("Neutral null", TEXT)
        fan = heading("Spread grows", -3.38, 3.23, TEAL, size=36)
        mean = heading("Expected average stays put", -3.37, 3.23, TEXT, size=31)
        force = heading("Selection or gene flow", -3.37, 3.23, BLUE, size=34)
        flow_key = plot_key("Average shifts", BLUE)
        direction = model_lines(plot, FLOW, directional=True)
        directional_mean = curve(plot, FLOW.mean(axis=0), TEXT, 6)
        flow_progress = ValueTracker(0)
        flow_visible = revealed_lines(direction, flow_progress)
        flow_average = revealed_lines(VGroup(directional_mean), flow_progress)
        self.add(world, question)
        self.at("across replicates")
        self.add(growing)
        order = np.random.default_rng(7).permutation(12)

        def show_sample(group, row, tracker):
            generation = tracker.get_value() * GENERATIONS
            count = round(12 * np.interp(generation, np.arange(len(row)), row))
            for dot, rank in zip(group, order):
                dot.set_fill(AMBER if rank < count else TEAL)

        neutral_updates = []
        for i, pool in enumerate(pools):
            def show_neutral(group, i=i):
                show_sample(group, NEUTRAL[i], amount)
            neutral_updates.append(show_neutral)
            pool[1].add_updater(show_neutral)
            sway(pool[1], amp=0.093, speed=2.7 + i * 0.34)
        self.play(FadeOut(question), FadeOut(rings), run_time=0.28)
        self.play(swap(world[-1], fan), amount.animate.set_value(0.11),
                  run_time=1.30, rate_func=linear)
        self.at("drift spreads allele")
        self.play(amount.animate.set_value(0.35), run_time=1.72, rate_func=linear)
        self.at("without pushing")
        self.add(live_average)
        self.play(amount.animate.set_value(0.53), run_time=2.22, rate_func=linear)
        self.at("chance favors no")
        self.play(swap(fan, mean), Create(expected), amount.animate.set_value(0.75),
                  run_time=3.5, rate_func=linear)
        self.at("that is the neutral")
        self.play(Succession(FadeOut(pools[2], run_time=0.36), FadeIn(null, run_time=0.36)),
                  amount.animate(run_time=3.63, rate_func=linear).set_value(1))
        self.at("consistent selection")
        growing.clear_updaters(recursive=True)
        live_average.clear_updaters(recursive=True)
        self.play(*[line.animate.set_stroke(opacity=0.22) for line in growing],
                  FadeOut(live_average), swap(mean, force), swap(null, flow_key),
                  run_time=0.84)
        for i, pool in enumerate(pools[:2]):
            def show_flow(group, i=i):
                show_sample(group, FLOW[i], flow_progress)
            pool[1].remove_updater(neutral_updates[i])
            pool[1].add_updater(show_flow)
        self.add(flow_visible, flow_average)
        self.play(flow_progress.animate.set_value(1), run_time=3.55, rate_func=linear)
        self.finish()


def comparison_chart():
    plot = frequency_axis()
    paths_group = model_lines(plot, NEUTRAL)
    average = curve(plot, NEUTRAL.mean(axis=0), TEXT, 6)
    expected = plot.hline(START, color=GREY)
    return plot, paths_group, average, expected


class S10Limits(SpokenScene):
    def construct(self):
        plot, traces, average, expected = comparison_chart()
        flow = model_lines(plot, FLOW, directional=True)
        flow_average = curve(plot, FLOW.mean(axis=0), TEXT, 6)
        single = traces[RISING]
        rest = VGroup(*[line for i, line in enumerate(traces) if i != RISING])
        for line in traces:
            line.set_stroke(opacity=0.22)
        question = heading("One population:\nluck or cause?", -3.36, 2.00, AMBER, size=38)
        drift = label("Drift", -4.66, 0.36, TEAL, 32)
        selection = label("Selection", -2.08, 0.36, BLUE, 32)
        drift_arrow = Arrow(point(-4.67, -0.06), point(-3.64, -1.10),
                            color=TEAL, stroke_opacity=0.7, buff=0.08)
        selection_arrow = Arrow(point(-2.08, -0.06), point(-3.11, -1.10),
                                color=BLUE, stroke_opacity=0.7, buff=0.08)
        target = bead(-3.38, -1.36, AMBER)
        compare = heading("Neutral null", -3.38, 2.09, TEXT, size=36)
        checks = VGroup(*[
            boxed_label(words, color, size=29, min_size=28, pad=0.23, fill_opacity=0.10)
            .move_to(point(-3.38, y))
            for words, color, y in (("✓ Average vs neutral null", TEXT, 1.07),
                                    ("✓ Fitness assay", AMBER, -0.12),
                                    ("✓ Ancestry", BLUE, -1.32))
        ])
        tracker = ValueTracker(0)
        mean_at = lambda: np.interp(tracker.get_value(), np.arange(GENERATIONS + 1), NEUTRAL.mean(axis=0))
        marker = plot.dot(tracker.get_value, mean_at, TEXT, AMBER, radius=0.115)
        example_t = ValueTracker(0)
        example = lambda x: np.interp(x, np.arange(GENERATIONS + 1), NEUTRAL[RISING])
        highlight = plot.live_curve(example, example_t, AMBER, 6.8)
        dot = plot.dot(example_t.get_value, lambda: example(example_t.get_value()),
                       AMBER, TEXT, radius=0.15)
        self.add(pool_stage(), frequency_stage(), plot, expected, traces, flow, flow_average)
        self.at("one trap")
        self.play(FadeOut(VGroup(flow, flow_average, expected, rest)),
                  single.animate.set_stroke(AMBER, width=3, opacity=0.32), run_time=1.17)
        self.at("a single population's")
        self.add(highlight, dot)
        self.play(FadeIn(question), FadeIn(target), example_t.animate.set_value(8),
                  run_time=3.32, rate_func=linear)
        self.at("since drift")
        self.play(FadeIn(drift), GrowArrow(drift_arrow), example_t.animate.set_value(12),
                  run_time=1.37, rate_func=linear)
        self.play(FadeIn(selection), GrowArrow(selection_arrow), example_t.animate.set_value(19),
                  run_time=1.72, rate_func=linear)
        self.at("so compare")
        highlight.clear_updaters()
        dot.clear_updaters()
        self.play(FadeOut(VGroup(question, target, drift, selection, drift_arrow, selection_arrow,
                                 highlight, dot)), run_time=0.44)
        single.set_stroke(width=3.3, opacity=0.83)
        for line in rest:
            line.set_stroke(opacity=0.73)
        self.play(FadeIn(rest), FadeIn(expected), Create(average), FadeIn(compare),
                  run_time=1.03)
        self.add(marker)
        self.play(FadeIn(checks[0]), tracker.animate(rate_func=linear).set_value(7), run_time=1.85)
        self.at("test selection")
        self.play(FadeIn(checks[1]), tracker.animate(rate_func=linear).set_value(14), run_time=1.65)
        self.at("gene flow with")
        self.play(FadeIn(checks[2]), tracker.animate(rate_func=linear).set_value(20), run_time=1.36)
        self.finish()


def outline(points, fill):
    return Polygon(*[point(x, y) for x, y in points], stroke_color=GREY,
                   stroke_width=2.5, fill_color=fill, fill_opacity=1)


def panther_cluster():
    coords = [(0.05, -1.77), (-0.16, -1.57), (-0.32, -1.37),
              (-0.57, -1.18), (-0.07, -1.32), (-0.40, -1.65)]
    return VGroup(*[bead(x, y, TEAL if i == 4 else AMBER, 0.096)
                    for i, (x, y) in enumerate(coords)])


def outcome_bars():
    """A before/after comparison, normalized independently to each baseline."""
    levels = (3, 2)
    xs = (2.8, 5.18)
    base, unit = -1.84, 1.12
    tracks, before = VGroup(), VGroup()
    for x in xs:
        tracks.add(plate(1.14, 3 * unit, x, base + 1.5 * unit, "#34475A"))
        before.add(Line(point(x - 0.78, base + unit), point(x + 0.78, base + unit),
                        color=TEXT, stroke_width=3))
    return xs, levels, base, unit, tracks, before


class S11UnlockedPanthers(SpokenScene):
    def construct(self):
        map_plate = plate(7.05, 5.65, -2.9, 0.01)
        land = outline([(-6.17, 1.56), (-4.80, 1.55), (-4.64, 0.66),
                        (-3.90, 0.68), (-3.57, 0.38), (-3.44, -0.16),
                        (-2.91, -0.29), (-2.57, 0.05), (-1.67, 0.21),
                        (-1.35, 0.57), (-0.82, 0.68), (-0.43, 1.03),
                        (0.32, 1.41), (0.39, 0.74), (-0.14, 0.23),
                        (-0.36, -0.44), (-0.11, -0.83), (0.14, -1.29),
                        (0.11, -1.97), (-0.22, -2.16), (-0.60, -1.70),
                        (-0.75, -1.06), (-1.18, -0.62), (-1.86, -0.61),
                        (-2.34, -0.47), (-2.73, -0.69), (-3.30, -0.88),
                        (-3.61, -1.64), (-4.14, -1.24), (-4.40, -0.61),
                        (-4.91, -0.54), (-5.57, 0.22), (-6.16, 0.22)],
                       "#405469")
        texas = label("Texas", -4.87, 2.20, TEAL, 31)
        florida = label("Florida panthers", -1.78, -2.50, AMBER, 30)
        source = heading("1995: eight Texas pumas", -2.91, 3.22, TEAL, size=35)
        year = heading("By 2010", 3.96, 2.54, TEXT, size=34)
        results_plate = plate(5.49, 5.65, 3.75, 0.01)
        destination = panther_cluster()
        starts = [point(-4.85 + 0.23 * (i % 4), 0.42 - 0.245 * (i // 4))
                  for i in range(8)]
        ends = [point(-0.70 + 0.26 * (i % 4), -1.82 + 0.26 * (i // 4))
                for i in range(8)]
        arcs = VGroup(*[ArcBetweenPoints(a, b, angle=-0.85 - i * 0.065,
                                        color=TEAL, stroke_width=6.0, stroke_opacity=0.87)
                        for i, (a, b) in enumerate(zip(starts, ends))])
        immigrants = VGroup(*[Dot(start, radius=0.138, color=TEAL, stroke_color=BG, stroke_width=2) for start in starts])
        xs, levels, base, unit, tracks, before = outcome_bars()
        factors = [ValueTracker(1) for _ in levels]
        bars = VGroup(*[
            always_redraw(lambda x=x, f=f, col=col: Rectangle(
                width=1.08, height=f.get_value() * unit, stroke_width=0,
                fill_color=col, fill_opacity=1).move_to(point(x, base + f.get_value() * unit / 2)))
            for x, f, col in zip(xs, factors, (AMBER, TEAL))
        ])
        outcomes = VGroup(label("Numbers", xs[0], -2.13, AMBER, 29),
                          label("about tripled", xs[0], -2.60, TEXT, 28),
                          label("Heterozygosity", xs[1] - 0.05, -2.13, TEAL, 28),
                          label("doubled", xs[1], -2.60, TEXT, 28))
        starting_count = label("Before", 1.71, base + unit, TEXT, 28)
        before[0].put_start_and_end_on(starting_count.get_right() + RIGHT * 0.13,
                                       before[0].get_end())

        self.at("in conservation")
        self.add(map_plate)
        self.play(DrawBorderThenFill(land), run_time=1.37)
        self.play(LaggedStart(*[GrowFromCenter(dot) for dot in destination], lag_ratio=0.25),
                  run_time=1.71)
        self.play(FadeIn(florida), run_time=0.43)
        sway(destination, amp=0.047, speed=3.4)
        self.at("in 1995")
        self.play(FadeIn(texas), FadeIn(source), run_time=0.71)
        self.play(LaggedStart(*[GrowFromCenter(dot) for dot in immigrants], lag_ratio=0.10),
                  run_time=1.26)
        self.at("released eight")
        transfers = [AnimationGroup(Create(arc), MoveAlongPath(dot, arc.copy()),
                                    rate_func=smooth)
                     for arc, dot in zip(arcs, immigrants)]
        self.play(LaggedStart(*transfers, lag_ratio=0.20), run_time=5.0)
        self.at("inbred panther")
        destination.clear_updaters(recursive=True)
        florida_focal_point = point(-0.26, -1.44)
        self.play(FadeOut(arcs),
                  VGroup(land, destination, immigrants).animate.scale(0.87,
                      about_point=florida_focal_point), run_time=2.12)
        for i, dot in enumerate(immigrants):
            bob(dot, amp=0.055, speed=3.2, seed=i)
        self.at("by 2010")
        self.play(FadeIn(results_plate), FadeIn(year), FadeIn(tracks), run_time=0.75)
        self.add(bars, before, starting_count)
        self.at("panther numbers")
        self.play(FadeIn(outcomes[0]), factors[0].animate.set_value(levels[0]), run_time=1.52)
        self.play(FadeIn(outcomes[1]), run_time=0.43)
        self.at("and heterozygosity")
        self.play(FadeIn(outcomes[2]), factors[1].animate.set_value(levels[1]),
                  run_time=3.20, rate_func=smooth)
        self.at("had doubled")
        self.play(FadeIn(outcomes[3]), run_time=0.48)
        self.finish()


CELL_COLORS = (AMBER, TEAL, PURPLE, GREEN)
NUM_CELLS = 16
CRYPT_X = -2.82
CRYPT_Y = -0.02


def cell_history():
    """Neutral ring model: a random site inherits one random neighbor's clone."""
    rng = np.random.default_rng(44)
    state = np.repeat(np.arange(4), NUM_CELLS // 4)
    history = [state.copy()]
    for _ in range(3000):
        site = rng.integers(NUM_CELLS)
        neighbor = (site + rng.choice((-1, 1))) % NUM_CELLS
        if state[site] != state[neighbor]:
            state[site] = state[neighbor]
            history.append(state.copy())
        if len(set(state)) == 1:
            break
    return history


def crypt_cells(colors):
    angles = np.arange(NUM_CELLS) * TAU / NUM_CELLS + PI / 16
    return VGroup(*[bead(CRYPT_X + 1.94 * np.cos(a), CRYPT_Y + 1.94 * np.sin(a), c, 0.333)
                    for a, c in zip(angles, colors)])


def crypt_board():
    tray = plate(7.08, 5.67, CRYPT_X, 0.03)
    ring = Annulus(inner_radius=1.48, outer_radius=2.37,
                   fill_color="#394C60", fill_opacity=1, stroke_width=0)
    ring.move_to(point(CRYPT_X, CRYPT_Y))
    return VGroup(tray, ring)


def division_diagram():
    parent = bead(3.54, 1.16, TEXT, 0.33)
    stem = bead(2.36, -0.40, TEXT, 0.30)
    progenitor = bead(4.72, -0.40, GREY, 0.24)
    daughters = VGroup(stem, progenitor)
    branches = VGroup(*[
        Arrow(parent.get_center() + DOWN * 0.33, d.get_center() + UP * 0.31,
              color=GREY, stroke_width=3.5, buff=0.08, tip_length=0.16)
        for d in daughters
    ])
    return parent, daughters, branches


class S12UnlockedStem(SpokenScene):
    def construct(self):
        board = crypt_board()
        history = cell_history()
        limit = next(i for i, state in enumerate(history) if len(set(state)) == 2)
        fractions = np.array([np.bincount(state, minlength=len(CELL_COLORS))
                              for state in history[:limit + 1]]) / NUM_CELLS
        cells = crypt_cells([TEXT] * NUM_CELLS).set_z_index(2)
        source = heading("2010: Snippert, Clevers and colleagues", -1.40, 3.22,
                         TEXT, size=34, width=9.9)
        stem_label = label("Small-intestinal stem cells", CRYPT_X, -2.59, TEXT, 29).set_z_index(3)
        right = plate(5.48, 5.67, 3.68, 0.03)
        parent, daughters, branches = division_diagram()
        question = label("One of each?", 3.56, 2.15, TEXT, 35)
        stem = label("Stem cell", 2.32, -1.11, TEXT, 28)
        progenitor = label("Short-lived\nprogenitor", 4.90, -1.21, TEXT, 28)
        # Rejection crosses the picture, with the labels below it.
        strike = Line(point(1.94, 1.47), point(5.13, -0.63), color=RED, stroke_width=7)
        symmetric = heading("Most divisions symmetric", 3.54, 2.15, TEXT, size=30)
        clock = label("1 to 6 months", 3.65, 2.14, TEXT, 35)
        progress = ValueTracker(0)
        span = Line(point(1.77, 1.36), point(5.54, 1.36), color=GREY, stroke_width=4)
        moving = always_redraw(lambda: bead(1.77 + 3.77 * progress.get_value(),
                                            1.36, AMBER, 0.11))
        plot = Plot(box=(1.43, 5.96, -1.92, 0.83), xr=(0, limit), yr=(0, 1),
                    color=GREY)
        traces = VGroup(*[curve(plot, row, col, 3.7, opacity=0.62)
                          for row, col in zip(fractions.T, CELL_COLORS)])
        drift = label("Neutral drift", 3.59, -2.29, TEXT, 32)
        old_pool = panther_cluster().move_to(point(CRYPT_X, CRYPT_Y)).set_z_index(2)

        self.at("in 2010")
        self.add(board[0], old_pool)
        self.play(FadeIn(source), Create(board[1]), run_time=1.12)
        self.play(ReplacementTransform(old_pool, cells), run_time=1.8)
        sway(cells, amp=0.03, speed=2.6)
        self.at("does each division")
        self.play(FadeIn(right), FadeIn(parent), FadeIn(question), run_time=0.68)
        self.play(Create(branches), run_time=0.60)
        self.play(GrowFromCenter(daughters[0]), FadeIn(stem), run_time=0.65)
        self.at("short lived progenitor")
        self.play(GrowFromCenter(daughters[1]), FadeIn(progenitor), run_time=0.67)
        self.at("they gave mouse")
        self.play(FadeIn(stem_label), run_time=0.45)
        self.at("one of four")
        self.play(LaggedStart(*[cell.animate.set_fill(CELL_COLORS[c])
                                for cell, c in zip(cells, history[0])], lag_ratio=0.046),
                  run_time=1.29)
        self.at("most divisions were")
        self.play(Create(strike), run_time=0.51)
        self.play(FadeOut(VGroup(daughters[1], progenitor, strike)), swap(question, symmetric),
                  run_time=0.58)
        other = daughters[0].copy().move_to(point(4.72, -0.40))
        other_label = label("Stem cell", 4.77, -1.11, TEXT, 28)
        self.play(TransformFromCopy(daughters[0], other), FadeIn(other_label), run_time=0.70)
        self.at("to six months")
        self.play(FadeOut(VGroup(parent, branches, daughters[0], stem, other, other_label)),
                  swap(symmetric, clock), run_time=0.60)
        self.play(Create(span), run_time=0.44)
        self.add(moving)
        self.at("some color patches")
        # Choose chronological snapshots that show an expanding and a
        # disappearing clone, with the last contrast held as the rule lands.
        last = history[0]
        for step in np.linspace(1, limit, 7, dtype=int):
            state = history[step]
            self.play(*[cell.animate.set_fill(CELL_COLORS[c])
                        for cell, a, c in zip(cells, last, state) if a != c],
                      progress.animate.set_value(step / limit), run_time=0.77)
            last = state
        self.at("stem cell positions")
        self.play(LaggedStart(*[Create(line) for line in traces], lag_ratio=0.19),
                  run_time=2.2)
        self.at("neutral drift")
        self.play(FadeIn(drift), run_time=0.46)
        self.finish()


class S13End(EndCard):
    LINE = "Model random mating and chance drift to tell luck from cause."
