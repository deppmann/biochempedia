"""Viral vector gene delivery, timed to the supplied narration.

COLOR MAP
  GREY: membranes and structure                 BLUE: vectors and first cargo part
  TEAL: intact gene cargo                        ORANGE: second vector and cargo part
  GOLD: overlap, dates and the guiding rule      PURPLE: channels
  YELLOW: current and light                     GREEN: controls and expression
  RED: external reagent
"""
from bp_parts import *  # noqa: F403

PURPLE = "#B58CD9"
ORANGE = "#F29E4C"
CYTOPLASM = "#294653"
MEMBRANE_INNER = "#527080"
STAGE = np.array([2.35, 0.05, 0.0])
DOCK = np.array([-1.45, 0.1, 0.0])
INSIDE = np.array([2.15, -0.45, 0.0])
QUESTION = "Each reaches 70% independently.\nWhat fraction makes full-length otoferlin?"
QUESTION_LAYOUT = dict(y=3.16, size=32, max_w=10.5)


def p(x, y):
    return np.array([x, y, 0.0])


def heading(text):
    return T(text, 33, GOLD).move_to(p(-0.75, 3.18))


def cell(center=STAGE, width=6.7, height=5.2, hair=False):
    """Shared cell silhouette. The hair-cell version adds a simple apical bundle."""
    body = Ellipse(width=width, height=height, stroke_color=GREY, stroke_width=5,
                   fill_color=CYTOPLASM, fill_opacity=1).move_to(center)
    inner = Ellipse(width=width - 0.21, height=height - 0.21, stroke_color=MEMBRANE_INNER,
                    fill_color=MEMBRANE_INNER, stroke_width=2).move_to(center)
    picture = VGroup(body, inner)
    if hair:
        for x, h in [(-0.74, 0.26), (-0.46, 0.38), (-0.18, 0.51), (0.10, 0.65)]:
            base = center + p(x, height / 2 - 0.09)
            picture.add(Line(base, base + UP * h, stroke_width=7, color=GREY))
    return picture


def living(picture):
    """Breathe the membrane and cytoplasm without moving diagram landmarks."""
    pulse(picture[0], base=5, amp=2, speed=1.7)
    body = picture[0]
    elapsed = 0.0

    def breathe(mob, dt):
        nonlocal elapsed
        elapsed += dt
        light = 0.16 * (1 - np.cos(1.7 * elapsed))
        mob.set_fill(interpolate_color(ManimColor(CYTOPLASM), ManimColor("#55798B"), light))

    return body.add_updater(breathe)


def cargo(center, width=1.1, color=TEAL, height=0.30):
    return RoundedRectangle(width=width, height=height, corner_radius=min(0.10, height / 3),
                            stroke_color=color, stroke_width=2, fill_color=color,
                            fill_opacity=0.95).move_to(center)


def shell(center, color=BLUE, radius=0.72):
    outer = RegularPolygon(n=6, radius=radius, start_angle=0, stroke_color=color,
                           stroke_width=4, fill_color=color, fill_opacity=0.18)
    inner = RegularPolygon(n=6, radius=radius * 0.82, start_angle=0, stroke_color=color,
                           fill_color=color, stroke_width=1.5)
    return VGroup(outer, inner).move_to(center)


def loaded(center, color=BLUE, width=1.0, gene_color=TEAL):
    return VGroup(shell(center, color), cargo(center, width, gene_color))


def pair_at(x):
    return VGroup(loaded(p(x, 0.82), BLUE, 0.84, BLUE),
                  loaded(p(x, -0.82), ORANGE, 0.84, ORANGE))


def joined_gene():
    return cargo(INSIDE, width=2.25, height=0.39)


def channel(center, width=1.52, height=0.85, open_gate=False):
    """Two walls and a gate, with a visible passage when the gate opens."""
    walls = VGroup()
    for sign in (-1, 1):
        post = RoundedRectangle(width=width * 0.28, height=height, corner_radius=0.12,
                                stroke_width=3, stroke_color=PURPLE, fill_color=PURPLE,
                                fill_opacity=0.85)
        post.move_to(center + RIGHT * sign * width * 0.34)
        walls.add(post)
    gate = cargo(center, width * 0.53, PURPLE, height * 0.21)
    if open_gate:
        gate.set_opacity(0)
    return VGroup(*walls, gate)


class S01Hook(SpokenScene):
    def construct(self):
        world = cell()
        living(world)
        gene = cargo(p(-5.2, 0.1), width=1.28)
        self.add(world, gene)
        self.at("How do you")
        self.play(gene.animate.move_to(p(-1.83, 0.1)), run_time=3.0)
        self.at("a gene alone")
        self.play(gene.animate.move_to(p(-3.8, 0.1)), run_time=2.9)
        self.at("instead biologists use")
        vector = shell(p(-5.45, 1.56))
        self.play(FadeIn(vector), run_time=0.45)
        self.play(vector.animate.move_to(gene), run_time=2.0)
        self.at("called viral vectors")
        label = place_label(T("Viral vector", 32, BLUE), vector, dirs=(DOWN,), buff=0.38)
        self.play(FadeIn(label), run_time=0.50)
        self.at("to carry chosen")
        self.play(FadeOut(label), VGroup(vector, gene).animate.move_to(DOCK), run_time=2.6)
        self.finish()


class S02Title(TitleCard):
    LESSON = "Viral vector gene delivery"
    TITLE = "Delivering New Genes With Engineered Viruses"

    def construct(self):
        world = cell().set_stroke(opacity=0.58)
        world[0].set_fill(opacity=0.58)
        approach = loaded(DOCK, width=1.28).set_stroke(opacity=0.64)
        approach[0][0].set_fill(opacity=0.12)
        approach[1].set_fill(opacity=0.64)
        self.add(bob(world, amp=0.045), bob(approach, amp=0.10, seed=1))
        title = T(self.TITLE.replace("New ", "New\n").replace("With ", "With\n"), 42,
                  font=TITLE_FONT, line_spacing=0.9).move_to(p(-3.98, 2.02))
        lesson = T(self.LESSON, 28, TEAL).move_to(p(-3.8, -1.35))
        rule = Line(p(-5.1, -0.78), p(-2.5, -0.78), color=GOLD, stroke_width=4)
        card = VGroup(title, rule, lesson)
        self.play(FadeIn(card), run_time=0.37)
        self.wait(1.07)
        self.play(FadeOut(card), run_time=0.33)


class S03HowItWorks(SpokenScene):
    def construct(self):
        world = cell()
        living(world)
        package = loaded(DOCK, width=1.28)
        vector, gene = package
        self.add(world, vector, gene)
        self.at("researchers pack")
        self.play(vector.animate.move_to(p(-3.65, 0.15)), gene.animate.move_to(p(-3.65, 1.55)),
                  run_time=0.95)
        self.play(gene.animate.move_to(vector).stretch_to_fit_width(1.0), run_time=2.25)
        retro = T("Retrovirus", 32, BLUE).move_to(p(-3.65, -1.05))
        aav = T("AAV", 32, BLUE).move_to(retro)
        self.at("such as a retrovirus")
        self.play(FadeIn(retro), Rotate(vector, PI / 6), run_time=0.65)
        self.at("adeno associated")
        self.play(swap(retro, aav), Rotate(vector, PI / 6), run_time=0.9)
        self.at("the vector enters")
        self.play(FadeOut(aav), VGroup(vector, gene).animate.move_to(p(0.65, 0.15)), run_time=2.10)
        self.at("delivers that gene")
        self.play(FadeOut(vector), gene.animate.move_to(INSIDE), run_time=1.6)
        self.at("the cell then builds")
        protein = channel(INSIDE + UP * 0.95)
        self.play(GrowFromPoint(protein, gene.get_center()), run_time=1.40)
        surface = STAGE + UP * 2.56
        self.play(protein.animate.move_to(surface), run_time=1.75)
        self.at("light gated channel")
        beam = Polygon(p(0.9, 3.67), p(1.45, 3.67), surface + RIGHT * 0.46,
                       surface + LEFT * 0.35, stroke_width=0, color=YELLOW, fill_opacity=0.60)
        name = T("Light-gated channel", 31, PURPLE).move_to(p(-3.42, 1.55))
        self.play(FadeIn(beam), FadeOut(protein[2]), FadeIn(name), run_time=0.78)
        self.finish()


class S04SizeLimit(SpokenScene):
    def construct(self):
        world = cell()
        vector = shell(DOCK)
        big_shell = shell(p(-3.7, 0.16), radius=2.37)
        big_shell[0].set_fill(opacity=0.28)
        self.add(world, vector)
        self.at("not every gene fits")
        self.play(FadeOut(world), ReplacementTransform(vector, big_shell), run_time=1.6)
        pulse(big_shell[0], base=5, amp=2.7, speed=2.4)
        scale = Plot(box=(-0.4, 5.9, -1.42, 1.65), xr=(0, 7), yr=(0, 3),
                     xticks=list(range(8)), yticks=[], size=28)
        scale.axes[1].set_opacity(0)
        kb = T("kb", 28, TEXT).move_to(p(6.4, -1.87))
        self.at("a conventional adeno")
        self.play(Create(scale), FadeIn(kb), run_time=2.25)
        aav = T("Conventional AAV", 32, BLUE).move_to(p(-3.7, -2.25))
        self.play(FadeIn(aav), run_time=0.6)

        def kb_bar(lo, hi, row, color, opacity=1.0):
            start = scale.pt(lo, row)
            end = scale.pt(hi, row)
            bar = cargo((start + end) / 2, width=end[0] - start[0], color=color, height=0.49)
            return bar.set_fill(opacity=opacity)

        self.at("carries about 4")
        capacity = kb_bar(0, 4.7, 2.09, BLUE, 0.70)
        band = kb_bar(4.7, 5, 2.09, BLUE, 0.29)
        cap = T("AAV capacity  4.7–5 kb", 31, BLUE).move_to(p(2.04, 1.55))
        self.play(GrowFromEdge(capacity, LEFT), GrowFromEdge(band, LEFT), run_time=1.60)
        self.play(FadeIn(cap), run_time=0.46)
        self.at("a kilobase is")
        unit = caption("1 kb = 1,000 DNA letters", 32)
        self.play(FadeIn(unit), run_time=0.62)
        self.at("coding sequence is")
        oto = kb_bar(0, 6, 0.75, TEAL)
        oto_label = T("Otoferlin (6 kb)", 31, TEAL).move_to(p(2.3, -0.12))
        self.play(GrowFromEdge(oto, LEFT), run_time=1.50)
        self.play(FadeIn(oto_label), run_time=0.36)
        self.at("a promoter switch")
        promoter = cargo(p(5.63, -0.65), 0.52, GREEN, 0.48)
        prom_label = T("Promoter", 28, GREEN).move_to(p(5.52, 0.05))
        self.play(FadeIn(promoter, shift=LEFT * 0.28), FadeIn(prom_label), run_time=0.62)
        self.at("so two vectors")
        world = cell()
        pair = pair_at(-3.8)
        big_shell[0].clear_updaters()
        self.play(FadeOut(VGroup(scale, kb, aav, capacity, band, cap, unit, oto, oto_label,
                                 promoter, prom_label)), run_time=0.33)
        self.play(FadeIn(world), ReplacementTransform(big_shell, pair), run_time=0.78)
        living(world)
        self.bring_to_front(pair)
        self.play(pair.animate.shift(RIGHT * 5.9), run_time=2.25)
        self.at("rejoin the full gene")
        self.play(ReplacementTransform(pair, joined_gene()), run_time=0.9)
        self.finish()


GRID_SIDE = 10
REACH = 7
GRID_X = 0.64
GRID_Y = 0.49
GRID_CENTER = p(0, 0.04)
RNG = np.random.default_rng(24)
ROWS = RNG.permutation(GRID_SIDE)
COLS = RNG.permutation(GRID_SIDE)


def grid_point(row, col):
    return GRID_CENTER + p(GRID_X * (col - 4.5), GRID_Y * (4.5 - row))


def grid_state(blue=False, amber=False, ordered=False, gold=False):
    """Two independent 7-of-10 dimensions yield 70 blue, 70 amber and 49 shared cells."""
    tiles = VGroup()
    for row in range(GRID_SIDE):
        for col in range(GRID_SIDE):
            a = blue and COLS[col] < REACH
            b = amber and ROWS[row] < REACH
            xy = grid_point(ROWS[row], COLS[col]) if ordered else grid_point(row, col)
            base_color = GOLD if gold and a and b else CYTOPLASM
            base = RoundedRectangle(width=GRID_X - 0.054, height=GRID_Y - 0.053, corner_radius=0.09,
                                    stroke_width=1.4, stroke_color=MEMBRANE_INNER, fill_color=base_color,
                                    fill_opacity=1).move_to(xy)
            left = cargo(xy + LEFT * 0.114, 0.18, BLUE, 0.26).set_opacity(float(a and not gold))
            right = cargo(xy + RIGHT * 0.114, 0.18, ORANGE, 0.26).set_opacity(float(b and not gold))
            if gold and not (a and b):
                left.set_opacity(float(a))
                right.set_opacity(float(b))
            tiles.add(VGroup(base, left, right))
    return tiles


def animate_grid(grid, gold=False):
    """Draw a slow wave through the tiles while their delivery marks stay fixed."""
    dark, light = ManimColor(CYTOPLASM), ManimColor("#618190")
    gold_dark, gold_light = ManimColor(GOLD), ManimColor("#FFE7A2")
    elapsed = 0.0

    def shimmer(mob, dt):
        nonlocal elapsed
        elapsed += dt
        for i, tile in enumerate(mob):
            row, col = divmod(i, GRID_SIDE)
            shared = gold and ROWS[row] < REACH and COLS[col] < REACH
            display_row = ROWS[row] if gold else row
            amount = min(elapsed, 0.7) * 0.32 * (1 - np.cos(1.85 * elapsed - 0.41 * display_row))
            lo, hi = (gold_dark, gold_light) if shared else (dark, light)
            tile[0].set_fill(interpolate_color(lo, hi, amount))

    return grid.add_updater(shimmer)


def reach_labels():
    return VGroup(T("70%", 38, BLUE).move_to(p(-4.7, 0.0)),
                  T("70%", 38, ORANGE).move_to(p(4.7, 0.0)))


class S05PredictQ(SpokenScene):
    def construct(self):
        world, gene = cell(), joined_gene()
        self.add(world, gene)
        grid = grid_state()
        self.at("splitting a gene")
        self.play(FadeOut(VGroup(world, gene)),
                  GrowFromPoint(grid, world.get_center()), run_time=2.65)
        labels = reach_labels()
        self.at("each of two vectors")
        first = grid_state(blue=True)
        self.play(LaggedStart(*[Transform(tile, target) for tile, target in zip(grid, first)],
                              lag_ratio=0.075), run_time=2.3)
        self.at("reaches 70")
        self.play(FadeIn(labels[0]), run_time=0.40)
        second = grid_state(blue=True, amber=True)
        self.play(LaggedStart(*[Transform(tile, target) for tile, target in zip(grid, second)],
                              lag_ratio=0.055), run_time=2.1)
        self.play(FadeIn(labels[1]), run_time=0.45)
        self.remove(*grid)
        self.add(animate_grid(grid))
        self.at("what fraction of those")
        card = question_card(QUESTION, **QUESTION_LAYOUT)
        self.play(FadeIn(card), run_time=0.75)
        self.at("pause and find")
        self.play(Indicate(labels[0], color=BLUE, scale_factor=1.08),
                  Indicate(labels[1], color=ORANGE, scale_factor=1.08), run_time=1.1)
        self.finish()


class S06PredictPause(PredictPause):
    QUESTION = QUESTION
    CARD = QUESTION_LAYOUT
    SECONDS = 4.5

    def backdrop(self):
        return VGroup(animate_grid(grid_state(blue=True, amber=True)), reach_labels())


class S07PredictA(SpokenScene):
    def construct(self):
        grid = grid_state(blue=True, amber=True)
        labels = reach_labels()
        card = question_card(QUESTION, **QUESTION_LAYOUT)
        self.add(grid, labels, card)
        self.at("because both deliveries")
        arranged = grid_state(blue=True, amber=True, ordered=True)
        self.play(FadeOut(card), LaggedStart(*[Transform(tile, target) for tile, target in zip(grid, arranged)],
                                            lag_ratio=0.012), run_time=2.65)
        self.at("multiply the two fractions")
        multiply = heading("Multiply the independent fractions")
        self.play(FadeIn(multiply), run_time=0.7)
        animate_grid(grid)
        formula = VGroup(M("0.7", 40, BLUE), M("×", 40), M("0.7", 40, ORANGE),
                         M("=", 40), M("0.49", 40, GOLD), M("(49%)", 38, GOLD))
        formula.arrange(RIGHT, buff=0.27).move_to(p(0, -3.14))
        self.at("0 .7 times")
        self.play(FadeIn(formula[0]), run_time=0.48)
        self.at("times 0 .7")
        self.play(FadeIn(formula[1]), FadeIn(formula[2]), run_time=0.52)
        self.at("is 0 .49")
        grid.clear_updaters()
        overlap = grid_state(blue=True, amber=True, ordered=True, gold=True)
        self.play(FadeIn(formula[3]), FadeIn(formula[4]),
                  Transform(grid, overlap), run_time=1.25)
        animate_grid(grid, gold=True)
        self.at("or 49%")
        count = T("49 of 100", 33, GOLD).move_to(p(4.87, -0.92))
        self.play(FadeIn(formula[5]), FadeIn(count), run_time=0.75)
        self.at("fewer than half")
        self.play(Indicate(count, color=GOLD, scale_factor=1.10), run_time=1.10)
        self.at("viral vectors deliver")
        grid.clear_updaters()
        world = cell()
        gene = joined_gene()
        self.play(FadeOut(VGroup(labels, multiply, formula, count)), run_time=0.35)
        self.play(FadeOut(grid, scale=0.28, target_position=world.get_center()),
                  FadeIn(world, scale=0.55), run_time=1.65)
        living(world)
        self.play(FadeIn(gene, shift=RIGHT * 0.35), run_time=0.95)
        self.at("but size and controls")
        rule = caption("Cargo size and controls bound every claim.", 32, GOLD, y=-3.23)
        self.play(FadeIn(rule), run_time=0.65)
        self.finish()


def current_plot(box):
    """Normalized schematic response. Both measured states use the same axes."""
    plot = Plot(box=box, xr=(0, 1), yr=(0, 1), xticks=[], yticks=[])
    resting = plot.curve(lambda _: 0.17, color=YELLOW)
    restored = plot.curve(lambda t: 0.17 + 0.55 * (t >= 0.42), color=YELLOW)
    changed = plot.curve(lambda t: 0.17 + 0.55 * (t >= 0.42) - 0.30 * (t >= 0.75), color=YELLOW)
    return plot, resting, restored, changed


class S08Controls(SpokenScene):
    def construct(self):
        world, gene = cell(), joined_gene()
        living(world)
        self.add(world, gene)
        self.at("getting a gene inside")
        plot, resting, restored, _ = current_plot((-6.08, -1.92, -1.10, 1.45))
        self.play(Create(plot), Create(resting), run_time=2.35)
        schematic = T("Current (schematic)", 28).move_to(p(-4.04, -1.60))
        self.play(FadeIn(schematic), run_time=0.46)
        self.at("restoring a lost current")
        self.play(Transform(resting, restored), run_time=1.20)
        rescue = T("Rescue", 33, YELLOW).move_to(p(-4.04, 1.95))
        self.at("called rescue")
        self.play(FadeIn(rescue), run_time=0.58)
        self.at("still needs vector")
        comparison = cell(center=p(-3.92, -0.02), width=5.12, height=4.68)
        expression = ValueTracker(0)
        meter = dial(expression, p(-3.92, -0.28), radius=0.98, label="Cargo expression", color=GREEN,
                     fmt="{:.0f}", size=28)
        empty = shell(p(-6.0, 1.05), GREEN, radius=0.66)
        control = heading("Vector & expression controls")
        self.play(FadeOut(VGroup(resting, plot, rescue, schematic)), run_time=0.33)
        self.play(FadeIn(comparison), FadeIn(empty), FadeIn(control), run_time=0.72)
        living(comparison)
        self.play(empty.animate.move_to(p(-3.92, 1.43)), FadeIn(meter), run_time=1.9)
        self.at("even then rescue")
        self.play(FadeOut(VGroup(comparison, empty, meter, control, gene)), run_time=0.60)
        options = VGroup(channel(p(1.1, 0.34), width=1.5, height=1.23, open_gate=True),
                         channel(p(3.6, 0.34), width=1.5, height=1.23, open_gate=True))
        options[1].rotate(PI / 2)
        q = T("?", 67, GOLD).move_to(p(2.35, 1.72))
        self.play(FadeIn(q), GrowFromCenter(options), run_time=1.12)
        self.at("a channel pore")
        pore = T("Pore", 28, PURPLE).move_to(p(1.1, -0.79))
        substitute = T("Substitute", 28, PURPLE).move_to(p(3.6, -0.79))
        self.play(FadeIn(pore), run_time=0.4)
        self.at("an over expressed")
        self.play(FadeIn(substitute), run_time=0.55)
        self.at("and preserving cones")
        cone = Polygon(p(1.87, 2.07), p(2.83, 2.07), p(3.69, -0.70), p(2.8, -1.02),
                       p(2.66, -2.27), p(2.04, -2.27), p(1.9, -1.02), p(1.01, -0.70),
                       color=GREY, fill_color=CYTOPLASM, fill_opacity=1, stroke_width=5)
        for m in world:
            m.clear_updaters()
        self.play(FadeOut(VGroup(q, options, pore, substitute)), run_time=0.32)
        self.play(ReplacementTransform(world, cone), run_time=1.13)
        self.play(FadeIn(caption("Animal models ≠ human trial", 35, GOLD)), run_time=1.0)
        self.finish()


def fibroblast():
    outline = VMobject(stroke_color=GREY, stroke_width=5, fill_color=CYTOPLASM, fill_opacity=1)
    outline.set_points_smoothly([p(-1.83, -1.65), p(0.0, -0.59), p(0.89, 1.31), p(3.22, 1.68),
                                 p(6.05, 2.25), p(4.8, 0.70), p(4.17, -0.85),
                                 p(1.99, -1.28), p(-1.83, -1.65)])
    return VGroup(outline, outline.copy().scale(0.95).set_fill(opacity=0)
                  .set_stroke(MEMBRANE_INNER, 2))


def colony():
    return VGroup(*[cell(p(x, y), 2.72, 2.35) for x, y in [(0.9, -0.80), (3.7, -0.80),
                                                           (2.3, 1.50), (2.3, -0.32)]])


class S09UnlockedIps(SpokenScene):
    def construct(self):
        world = cell()
        living(world)
        self.add(world)
        self.at("with tight controls")
        landmarks = VGroup(T("2006", 34, GOLD), T("2018", 34, GOLD), T("2019", 34, GOLD))
        landmarks.arrange(DOWN, buff=0.75).move_to(p(-4.2, 0.0))
        self.play(LaggedStart(*[FadeIn(year, shift=RIGHT * 0.25) for year in landmarks],
                              lag_ratio=0.67), run_time=3.6)
        self.at("in 2006")
        for m in world:
            m.clear_updaters()
        fibro = fibroblast()
        self.play(FadeOut(landmarks), ReplacementTransform(world, fibro), run_time=1.4)
        living(fibro)
        credit = heading("2006 · Takahashi & Yamanaka")
        self.at("takahashi and shinya")
        self.play(FadeIn(credit), run_time=0.65)
        self.at("used retroviruses on")
        virus = loaded(p(-5.55, 0.75))
        self.play(FadeIn(virus), run_time=0.55)
        self.play(virus.animate.move_to(p(0.5, 0.55)), run_time=2.95)
        fibro_name = caption("Mouse fibroblast", 31, TEXT, y=-3.18)
        self.at("called fibroblasts")
        self.play(FadeIn(fibro_name), run_time=0.55)
        genes = VGroup(*[cargo(p(0.85 + col * 0.60, -0.62 + row * 0.29), 0.45,
                               TEAL, 0.15) for row in range(4) for col in range(6)])
        self.at("delivering 24")
        self.play(FadeOut(virus), LaggedStart(*[GrowFromCenter(gene) for gene in genes],
                                             lag_ratio=0.065), run_time=2.48)
        self.at("then omitting one")
        self.play(LaggedStart(*[FadeOut(gene, shift=UP * 0.25) for gene in list(genes)[4:]],
                              lag_ratio=0.10), run_time=2.2)
        self.at("four gene switching")
        factors = caption("Oct3/4   ·   Sox2   ·   Klf4   ·   c-Myc", 31, TEAL, y=-3.18)
        self.play(swap(fibro_name, factors), run_time=0.85)
        self.at("those four turned")
        for m in fibro:
            m.clear_updaters()
        stem = colony()
        self.play(FadeOut(VGroup(*list(genes)[:4])), ReplacementTransform(fibro, stem), run_time=3.0)
        self.at("induced pluripotent")
        name = caption("iPS cells", 35, TEAL, y=-3.18)
        self.play(swap(factors, name), run_time=1.1)
        self.finish()


class S10UnlockedTmc1(SpokenScene):
    def construct(self):
        stem, hair = colony(), cell(hair=True)
        self.add(stem)
        self.at("in 2018")
        self.play(ReplacementTransform(stem, hair), run_time=1.4)
        living(hair)
        credit = T("2018 · Pan & colleagues", 33, GOLD).move_to(p(-3.47, 3.14))
        mutant = T("Tmc1/Tmc2 double-null", 28).move_to(p(-3.70, 2.43))
        self.play(FadeIn(credit), run_time=0.60)
        plot, trace, restored, changed = current_plot((-6.1, -1.95, -1.65, 0.76))
        self.at("probed a working")
        self.play(Create(plot), Create(trace), run_time=1.65)
        schematic = T("Current (schematic)", 28).move_to(p(-4.02, -2.17))
        self.play(FadeIn(schematic), run_time=0.48)
        self.at("a vector delivered")
        vector = loaded(p(-3.8, 1.54))
        self.play(FadeIn(vector), run_time=0.65)
        self.play(vector.animate.move_to(p(0.7, 0.8)), run_time=2.24)
        self.at("mutant mouse hair")
        self.play(FadeIn(mutant), FadeOut(vector), FadeIn(cargo(INSIDE)), run_time=0.70)
        ch_position = p(4.53, 2.04)
        pore = channel(ch_position, open_gate=True).rotate(-PI / 5)
        self.at("restoring current")
        self.play(Transform(trace, restored), GrowFromPoint(pore, INSIDE), run_time=1.40)
        self.at("each copy carried")
        site = Dot(p(4.77, 2.42), radius=0.145, color=ORANGE)
        self.play(GrowFromCenter(site), run_time=0.95)
        name = caption("Tmc1 · one added cysteine", 31, ORANGE, y=-3.17)
        self.play(FadeIn(name), run_time=0.65)
        self.at("a reagent that")
        dots = VGroup(*[Dot(p(x, y), color=RED, radius=0.103)
                        for x, y in [(6.32, 2.32), (6.09, 1.94), (6.38, 1.57)]])
        self.play(FadeIn(dots, shift=LEFT * 0.20), run_time=0.65)
        self.play(dots.animate.shift(p(-0.29, 0.05)), run_time=1.45)
        self.at("grab cysteine")
        self.play(dots[0].animate.move_to(site.get_center() + p(0.16, 0.10)), run_time=1.70)
        self.at("when it altered")
        self.play(Transform(trace, changed), run_time=1.35)
        self.at("neither synthesis nor delivery")
        ruled_out = caption("Synthesis / delivery", 31, TEXT, y=-3.17)
        line = Line(ruled_out.get_left() + LEFT * 0.13, ruled_out.get_right() + RIGHT * 0.13,
                    color=RED, stroke_width=5)
        line.layout_ok = "covered"  # Deliberate strike-through of the ruled-out explanation.
        self.play(swap(name, ruled_out), run_time=0.74)
        self.play(Create(line), run_time=0.65)
        self.finish()


class S11UnlockedClose(SpokenScene):
    def construct(self):
        hair = cell(hair=True)
        living(hair)
        self.add(hair)
        self.at("in 2019")
        credit = T("2019 · Al-Moyed & colleagues", 33, GOLD).move_to(p(-3.0, 3.13))
        self.play(FadeIn(credit), run_time=0.55)
        whole = joined_gene().move_to(p(-4.03, 0.02))
        self.at("worked around the size")
        self.play(GrowFromEdge(whole, LEFT), run_time=1.5)
        self.at("they split its coding")
        pair = pair_at(-4.03)
        self.play(ReplacementTransform(whole, pair), run_time=1.9)
        aav = T("Two AAV2/6 vectors", 31, BLUE).move_to(p(-4.03, -2.03))
        self.play(FadeIn(aav), run_time=0.55)
        self.at("cells receiving both")
        self.play(FadeOut(aav), pair.animate.shift(RIGHT * 6.12), run_time=1.50)
        self.at("the full length gene")
        gene = joined_gene()
        self.play(ReplacementTransform(pair, gene), run_time=1.12)
        self.at("from stem cells")
        badges = VGroup(boxed_label("iPS cells", TEAL, size=30),
                        boxed_label("TMC1 current", PURPLE, size=30),
                        boxed_label("Full-length otoferlin", GOLD, size=30))
        badges.arrange(RIGHT, buff=0.34).move_to(p(0, -3.18))
        self.play(LaggedStart(*[FadeIn(badge, shift=UP * 0.13) for badge in badges],
                              lag_ratio=0.49), run_time=1.9)
        self.at("engineered viruses answer")
        for m in hair:
            m.clear_updaters()
        self.play(FadeOut(credit), VGroup(hair, gene).animate.shift(LEFT * 2.35), run_time=2.85)
        living(hair)
        self.finish()


class S12End(EndCard):
    LINE = "Engineered viruses deliver genes into living cells, bounded by size and controls."
