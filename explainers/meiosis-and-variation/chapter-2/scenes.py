"""How Meiosis Remixes Alleles.

COLOR MAP (continued exactly from chapter 1)
  GREEN  chromosome inherited from one parent
  ORANGE chromosome inherited from the other parent
  BLUE   cell boundary / destination cell
  YELLOW current action, cut, flip, or routing arrow
  TEXT   explanatory labels

Chromosomes are schematic rounded rods.  They are not molecular structures.
All carried chromosome pictures are rebuilt by the builders below.
"""
from bp_parts import *

PARENT_A = GREEN
PARENT_B = ORANGE
CELL = BLUE
ACTION = YELLOW


def pt(x, y):
    return np.array([x, y, 0.0])


def living_stage(width=11.8):
    """A quiet, breathing field shared by every scene in this chromosome world."""
    field = RoundedRectangle(
        corner_radius=0.42, width=width, height=6.75,
        stroke_color=CELL, stroke_width=2.5,
        fill_color=CELL, fill_opacity=0.16,
    ).move_to(pt(0, -0.42))
    field.set_z_index(-20)
    field.layout_ok = True  # deliberate full-scene background, behind every label
    field._stage_t = 0.0

    def breathe(mob, dt):
        mob._stage_t += dt
        mob.set_fill(opacity=0.16 + 0.055 * np.sin(2.0 * mob._stage_t))

    field.add_updater(breathe)
    return field


class FilmScene(SpokenScene):
    def setup(self):
        super().setup()
        self.add(living_stage())


class FilmPause(PredictPause):
    def setup(self):
        super().setup()
        self.add(living_stage(11.0))


def rod(color, height, center=ORIGIN, width=0.34):
    return RoundedRectangle(
        corner_radius=0.15, width=width, height=height,
        stroke_color=color, stroke_width=4,
        fill_color=color, fill_opacity=0.58,
    ).move_to(center)


def copied_chromosome(color, height, center=ORIGIN, scale=1.0):
    """The same joined-sister X used in chapter 1."""
    a = rod(color, height * scale, width=0.26 * scale).rotate(0.43)
    b = rod(color, height * scale, width=0.26 * scale).rotate(-0.43)
    g = VGroup(a, b).move_to(center)
    connection = Dot(g.get_center(), radius=0.11 * scale, color=ACTION)
    g.add(connection)
    g.connection = connection
    return g


def cell_outline(center=ORIGIN, rx=3.0, ry=2.65, stroke=4):
    return Ellipse(
        width=2 * rx, height=2 * ry, stroke_color=CELL, stroke_width=stroke,
        fill_color=CELL, fill_opacity=0.055,
    ).move_to(center)


def hook_world():
    """Central diploid model and four faint possible haploid outcomes."""
    boundary = cell_outline(pt(0, -0.15), rx=2.55, ry=2.65)
    chroms = VGroup(
        rod(PARENT_A, 2.25, pt(-0.72, 0.70)),
        rod(PARENT_B, 2.25, pt(0.72, 0.70)),
        rod(PARENT_A, 1.25, pt(-0.72, -1.15)),
        rod(PARENT_B, 1.25, pt(0.72, -1.15)),
    )
    outcomes = VGroup()
    for x, y in [(-4.75, 1.55), (4.75, 1.55), (-4.75, -1.55), (4.75, -1.55)]:
        c = cell_outline(pt(x, y), rx=0.72, ry=0.82, stroke=2.5).set_opacity(0.32)
        q = T("?", 38, ACTION, weight=BOLD).move_to(pt(x, y)).set_opacity(0.55)
        outcomes.add(VGroup(c, q))
    g = VGroup(boundary, chroms, outcomes)
    g.boundary, g.chroms, g.outcomes = boundary, chroms, outcomes
    return g


def long_paired_world(with_bands=False):
    """Large copied long homologs; the short pair waits below."""
    green = copied_chromosome(PARENT_A, 2.65, pt(-1.02, 0.55), scale=1.05)
    orange = copied_chromosome(PARENT_B, 2.65, pt(1.02, 0.55), scale=1.05)
    shorts = VGroup(
        copied_chromosome(PARENT_A, 1.10, pt(-0.58, -2.15), scale=0.78),
        copied_chromosome(PARENT_B, 1.10, pt(0.58, -2.15), scale=0.78),
    ).set_opacity(0.30)
    g = VGroup(green, orange, shorts)
    g.green, g.orange, g.shorts = green, orange, shorts
    if with_bands:
        bands = VGroup()
        for y in (-0.22, 0.80, 1.50):
            pair = VGroup(
                Rectangle(width=1.10, height=0.18, stroke_width=0, fill_color=TEXT, fill_opacity=0.95).move_to(pt(-1.02, y)),
                Rectangle(width=1.10, height=0.18, stroke_width=0, fill_color=TEXT, fill_opacity=0.95).move_to(pt(1.02, y)),
            )
            bands.add(pair)
        g.add(bands)
        g.bands = bands
    return g


def crossover_world(recombined=False):
    """Four aligned chromatids with the two inner, non-sisters emphasized."""
    xs = (-1.42, -0.54, 0.54, 1.42)
    cols = (PARENT_A, PARENT_A, PARENT_B, PARENT_B)
    chromatids = VGroup(*[rod(c, 4.55, pt(x, 0), width=0.30) for x, c in zip(xs, cols)])
    if recombined:
        for i, new_color in ((1, PARENT_B), (2, PARENT_A)):
            chromatids[i].stretch_to_fit_height(3.35).move_to(pt(xs[i], 0.60))
            tip = rod(new_color, 1.20, pt(xs[i], -1.675), width=0.30)
            chromatids[i] = VGroup(chromatids[i], tip)
    outer = VGroup(chromatids[0], chromatids[3]).set_opacity(0.46)
    g = VGroup(chromatids)
    g.chromatids, g.outer = chromatids, outer
    return g


def homolog_pair(height, y, left_color=PARENT_A, right_color=PARENT_B, xgap=0.82):
    left = rod(left_color, height, pt(-xgap, y), width=0.30)
    right = rod(right_color, height, pt(xgap, y), width=0.30)
    g = VGroup(left, right)
    g.left, g.right = left, right
    return g


def assortment_world(three=True):
    """Pairs straddling the fixed central division line."""
    line = DashedLine(pt(0, -2.55), pt(0, 2.55), color=CELL, stroke_width=3)
    specs = [(2.05, 1.55), (1.50, 0.0), (0.95, -1.55)] if three else [(2.05, 1.05), (0.95, -1.10)]
    pairs = VGroup(*[homolog_pair(h, y) for h, y in specs])
    g = VGroup(line, pairs)
    g.line, g.pairs = line, pairs
    return g


def flip_arrow(pair):
    return CurvedArrow(
        pair.right.get_top() + RIGHT * 0.38,
        pair.left.get_top() + LEFT * 0.38,
        angle=1.25, color=ACTION, stroke_width=5,
    )


def predict_world(flipped=False, targets=True):
    """Two-pair prediction picture, identical in s05--s07."""
    line = DashedLine(pt(0, -2.15), pt(0, 2.20), color=CELL, stroke_width=3)
    long_pair = homolog_pair(2.25, 0.95)
    if flipped:
        short_pair = homolog_pair(1.15, -1.25, PARENT_B, PARENT_A)
    else:
        short_pair = homolog_pair(1.15, -1.25, PARENT_A, PARENT_B)
    target_group = VGroup()
    if targets:
        left = cell_outline(pt(-4.3, 0), rx=1.0, ry=1.65, stroke=3.5)
        right = cell_outline(pt(4.3, 0), rx=1.0, ry=1.65, stroke=3.5)
        target_group.add(left, right)
    g = VGroup(line, long_pair, short_pair, target_group)
    g.line, g.long_pair, g.short_pair, g.targets = line, long_pair, short_pair, target_group
    return g


def recombinant_rod(center=ORIGIN, height=3.4, main=PARENT_A, tip=PARENT_B, width=0.34):
    body_h, tip_h = height * 0.72, height * 0.28
    body = rod(main, body_h, center + UP * (tip_h / 2), width=width)
    end = rod(tip, tip_h, center + DOWN * (body_h / 2), width=width)
    return VGroup(body, end)


def mix_icon(center, colors, scale=1.0):
    boundary = cell_outline(center, rx=0.72 * scale, ry=0.82 * scale, stroke=3)
    a = rod(colors[0], 0.92 * scale, center + LEFT * 0.18 * scale, width=0.18 * scale)
    b = rod(colors[1], 0.58 * scale, center + RIGHT * 0.20 * scale, width=0.18 * scale)
    return VGroup(boundary, a, b)


def stage_tag(text="schematic"):
    t = scope_tag(text)
    return t.move_to(pt(5.65 - t.width / 2, -3.5))


class S01Hook(TitleCard, FilmScene):
    LESSON = "Meiosis and Variation"
    TITLE = "How Meiosis Remixes Alleles"

    def construct(self):
        world = hook_world()
        pulse(world.boundary, base=4.0, amp=0.7, speed=1.35)
        self.play(FadeIn(world.boundary), run_time=0.55)
        self.play(LaggedStart(*[FadeIn(c, shift=UP * 0.1) for c in world.chroms], lag_ratio=0.12), run_time=1.0)
        self.at("different allele mixes")
        self.play(LaggedStart(*[FadeIn(o, scale=0.9) for o in world.outcomes], lag_ratio=0.10), run_time=0.9)
        self.at("Return to the same model")
        self.play(Indicate(world.chroms, color=ACTION), run_time=0.8)
        self.at("Green chromosomes")
        green_key = T("one parent", 28, PARENT_A).move_to(pt(-4.75, 3.4))
        self.play(FadeOut(world.outcomes), FadeIn(green_key), Indicate(VGroup(world.chroms[0], world.chroms[2]), color=PARENT_A), run_time=0.8)
        self.at("orange chromosomes")
        orange_key = T("other parent", 28, PARENT_B).move_to(pt(4.75, 3.4))
        self.play(FadeIn(orange_key), Indicate(VGroup(world.chroms[1], world.chroms[3]), color=PARENT_B), run_time=0.8)
        title = fit_text(self.TITLE, max_w=6.2, size=30, font=TITLE_FONT).move_to(pt(0, 3.4))
        self.play(FadeIn(title, shift=DOWN * 0.1), run_time=0.5)
        self.finish()


class S02Alleles(FilmScene):
    def construct(self):
        world = long_paired_world()
        self.add(world)
        self.at("same genes in matching positions")
        bands = VGroup()
        for y in (-0.22, 0.80, 1.50):
            pair = VGroup(
                Rectangle(width=1.10, height=0.18, stroke_width=0, fill_color=TEXT, fill_opacity=0.95).move_to(pt(-1.02, y)),
                Rectangle(width=1.10, height=0.18, stroke_width=0, fill_color=TEXT, fill_opacity=0.95).move_to(pt(1.02, y)),
            )
            bands.add(pair)
        self.play(LaggedStart(*[FadeIn(b, shift=LEFT * 0.12) for b in bands], lag_ratio=0.18), run_time=1.1)
        self.at("alleles may differ")
        A = T("A", 32, PARENT_A, weight=BOLD).move_to(pt(-1.02, 2.45))
        a = T("a", 32, PARENT_B, weight=BOLD).move_to(pt(1.02, 2.45))
        self.play(FadeIn(A), FadeIn(a), run_time=0.55)
        self.at("Copying")
        self.play(Indicate(VGroup(world.green, world.orange), color=ACTION), run_time=0.8)
        sister = T("SISTER\nCHROMATIDS", 30, ACTION, weight=BOLD).move_to(pt(4.30, 1.55))
        pointer = Arrow(sister.get_left(), world.orange.get_right(), buff=0.18, color=ACTION)
        self.play(FadeIn(sister), GrowArrow(pointer), run_time=0.65)
        self.at("lie side by side")
        self.play(FadeOut(VGroup(sister, pointer)), world.green.animate.shift(RIGHT * 0.22), world.orange.animate.shift(LEFT * 0.22), A.animate.shift(RIGHT * 0.22), a.animate.shift(LEFT * 0.22), run_time=0.8)
        self.at("regions beside each other")
        guides = VGroup(*[DashedLine(p[0].get_right(), p[1].get_left(), color=ACTION, stroke_width=3) for p in bands])
        self.play(LaggedStart(*[Create(g) for g in guides], lag_ratio=0.16), run_time=0.9)
        self.finish()


class S03CrossingOver(FilmScene):
    def construct(self):
        world = crossover_world()
        self.add(world)
        pulse(world.chromatids[1], base=4.0, amp=0.8, speed=1.5)
        pulse(world.chromatids[2], base=4.0, amp=0.8, speed=1.5)
        self.at("non -sister chromatids")
        lab = T("NON-SISTER CHROMATIDS", 30, ACTION, weight=BOLD).move_to(pt(0, 3.4))
        self.play(FadeIn(lab), Indicate(VGroup(world.chromatids[1], world.chromatids[2]), color=ACTION), run_time=0.8)
        self.at("two chromatids cross")
        self.play(world.chromatids[1].animate.rotate(-0.24, about_point=pt(-0.54, 0)), world.chromatids[2].animate.rotate(0.24, about_point=pt(0.54, 0)), run_time=1.0)
        self.at("break at matching positions")
        cuts = VGroup(
            Line(pt(-0.88, -0.72), pt(-0.18, -0.72), color=ACTION, stroke_width=8),
            Line(pt(0.18, -0.72), pt(0.88, -0.72), color=ACTION, stroke_width=8),
        )
        self.play(LaggedStart(*[Create(c) for c in cuts], lag_ratio=0.2), run_time=0.65)
        self.at("and reconnect")
        result = crossover_world(recombined=True)
        self.play(FadeOut(cuts), ReplacementTransform(world, result), run_time=1.4)
        self.at("green and orange sections")
        recomb = T("RECOMBINANT", 34, ACTION, weight=BOLD).move_to(pt(0, 3.4))
        self.play(swap(lab, recomb), Indicate(VGroup(result.chromatids[1], result.chromatids[2]), color=ACTION), run_time=0.9)
        self.at("combining alleles")
        self.play(Rotate(VGroup(result.chromatids[1], result.chromatids[2]), angle=0.07), run_time=1.1, rate_func=there_and_back)
        self.finish()


class S04Assortment(FilmScene):
    def construct(self):
        world = assortment_world(three=True)
        self.play(
            Create(world.line),
            LaggedStart(*[FadeIn(p, shift=UP * 0.1) for p in world.pairs], lag_ratio=0.16),
            run_time=1.0,
        )
        self.at("face either direction")
        arrows = VGroup(*[flip_arrow(p) for p in world.pairs])
        self.play(LaggedStart(*[Create(a) for a in arrows], lag_ratio=0.16), run_time=0.9)
        self.at("One pair's direction")
        medium = world.pairs[1]
        flipped = homolog_pair(1.50, 0.0, PARENT_B, PARENT_A)
        self.play(ReplacementTransform(medium, flipped), Indicate(VGroup(world.pairs[0], world.pairs[2]), color=TEXT), run_time=1.2)
        self.at("independent assortment")
        heading = T("INDEPENDENT ASSORTMENT", 34, ACTION, weight=BOLD).move_to(pt(0, 3.4))
        self.play(FadeIn(heading, shift=DOWN * 0.1), run_time=0.55)
        self.at("either or choice")
        self.play(LaggedStart(*[Indicate(p, color=ACTION) for p in (world.pairs[0], flipped, world.pairs[2])], lag_ratio=0.18), run_time=1.1)
        self.add(stage_tag("schematic"))
        self.finish()


class S05Predict(FilmScene):
    def construct(self):
        world = predict_world(flipped=False)
        for p in (world.long_pair, world.short_pair):
            bob(p, amp=0.035, speed=1.4, seed=1)
        self.add(world)
        self.at("long green homologue")
        self.play(Indicate(VGroup(world.long_pair.left, world.short_pair.right), color=ACTION), run_time=0.85)
        self.at("short pair flips")
        arrow = flip_arrow(world.short_pair)
        pulse(arrow, base=5.0, amp=1.2, speed=1.5)
        self.play(Create(arrow), run_time=0.65)
        self.at("which chromosome mix")
        q = question_card("WHICH MIX ENTERS LEFT?", y=-3.28, size=34, max_w=9.8)
        self.play(FadeIn(q.question, shift=UP * 0.12), run_time=0.6)
        self.at("Predict before")
        self.play(Indicate(world.targets[0], color=ACTION), run_time=0.75)
        self.finish()


class S06Pause(FilmPause):
    QUESTION = "WHICH MIX ENTERS LEFT?"
    SECONDS = 4.5
    CARD = {"y": -3.28, "size": 34, "max_w": 9.8}
    RING_AT = (6.0, -3.22, 0)

    def backdrop(self):
        world = predict_world(flipped=False)
        arrow = flip_arrow(world.short_pair)
        pulse(arrow, base=5.0, amp=1.2, speed=1.5)
        return VGroup(world, arrow)


class S07Reveal(FilmScene):
    def construct(self):
        world = predict_world(flipped=False)
        arrow = flip_arrow(world.short_pair)
        self.add(world, arrow)
        self.at("short pair flips")
        flipped = homolog_pair(1.15, -1.25, PARENT_B, PARENT_A)
        self.play(FadeOut(arrow), ReplacementTransform(world.short_pair, flipped), run_time=1.0)
        self.at("green from both pairs")
        self.play(Indicate(VGroup(world.long_pair.left, flipped.right), color=PARENT_A), run_time=0.8)
        self.at("Separation sends")
        left_long = world.long_pair.left.copy()
        left_short = flipped.right.copy()
        right_long = world.long_pair.right.copy()
        right_short = flipped.left.copy()
        routes = VGroup(
            Arrow(left_long.get_left(), world.targets[0].get_right(), color=ACTION, buff=0.12),
            Arrow(left_short.get_left(), world.targets[0].get_right() + DOWN * 0.3, color=ACTION, buff=0.12),
            Arrow(right_long.get_right(), world.targets[1].get_left(), color=ACTION, buff=0.12),
            Arrow(right_short.get_right(), world.targets[1].get_left() + DOWN * 0.3, color=ACTION, buff=0.12),
        )
        self.play(LaggedStart(*[GrowArrow(a) for a in routes], lag_ratio=0.10), run_time=0.8)
        self.play(
            left_long.animate.scale(0.68).move_to(pt(-4.70, 0.45)),
            left_short.animate.scale(0.68).move_to(pt(-4.15, -0.55)),
            right_long.animate.scale(0.68).move_to(pt(4.20, 0.45)),
            right_short.animate.scale(0.68).move_to(pt(4.70, -0.55)),
            FadeOut(VGroup(world.long_pair, flipped, routes, world.line)), run_time=1.2,
        )
        self.add(left_long, left_short, right_long, right_short)
        self.at("Changing one pair")
        self.play(Indicate(VGroup(left_long, left_short), color=ACTION), run_time=0.75)
        self.at("member of each pair")
        check = VGroup(T("✓", 44, ACTION), T("ONE FROM EACH PAIR", 32, TEXT, weight=BOLD)).arrange(RIGHT, buff=0.25).move_to(pt(0, 3.4))
        self.play(FadeIn(check, shift=DOWN * 0.12), run_time=0.6)
        self.finish()


class S08Count(FilmScene):
    def construct(self):
        levels = [(-4.8, 0.0, 1), (-1.6, 0.0, 2), (1.75, 0.0, 4), (5.0, 0.0, 8)]
        root = Dot(pt(levels[0][0], levels[0][1]), radius=0.12, color=TEXT)
        self.add(root)
        self.at("grows by doubling")
        previous = [root]
        all_nodes = VGroup(root)
        counts = VGroup()
        for li, (x, y, count) in enumerate(levels[1:], start=1):
            nodes = []
            branches = VGroup()
            target_ys = np.linspace(1.7, -2.3, 2 ** li)
            for j, p in enumerate(previous):
                for target_y in target_ys[2 * j:2 * j + 2]:
                    d = Dot(pt(x, target_y), radius=0.10, color=PARENT_A if len(nodes) % 2 == 0 else PARENT_B)
                    branches.add(Line(p.get_center(), d.get_center(), color=GREY, stroke_width=3))
                    nodes.append(d)
            lab = M(str(count), 36, ACTION).move_to(pt(x, 2.35))
            self.play(Create(branches), FadeIn(VGroup(*nodes)), FadeIn(lab), run_time=0.8)
            all_nodes.add(branches, *nodes)
            counts.add(lab)
            previous = nodes
        self.at("Each added pair")
        self.play(LaggedStart(*[Indicate(c, color=ACTION) for c in counts], lag_ratio=0.18), run_time=1.0)
        self.at("computed pattern")
        computed = T("COMPUTED", 28, ACTION, weight=BOLD).move_to(pt(0, 3.45))
        rule = M("choices = 2 × 2 × 2", 30, TEXT).move_to(pt(0, -3.15))
        self.play(FadeIn(computed), FadeIn(rule), run_time=0.65)
        self.at("Crossing over adds")
        tips = VGroup()
        for d in previous[::2]:
            tip = VGroup(rod(PARENT_A, 0.56, d.get_center() + UP * 0.12, width=0.13), rod(PARENT_B, 0.22, d.get_center() + DOWN * 0.27, width=0.13))
            tips.add(tip)
        self.play(LaggedStart(*[ReplacementTransform(previous[i * 2].copy(), tip) for i, tip in enumerate(tips)], lag_ratio=0.12), run_time=1.1)
        self.finish()


class S09Limit(FilmScene):
    def construct(self):
        chrom = recombinant_rod(pt(-2.8, 0), height=4.7)
        other = rod(PARENT_B, 3.0, pt(3.1, 0), width=0.38)
        self.play(FadeIn(chrom, shift=UP * 0.1), run_time=0.7)
        self.at("ignores crossing over")
        self.play(Indicate(chrom, color=ACTION), run_time=0.8)
        self.at("limit for genes")
        bands = VGroup(
            Rectangle(width=0.78, height=0.18, stroke_width=0, fill_color=TEXT, fill_opacity=0.95).move_to(pt(-2.8, 0.55)),
            Rectangle(width=0.78, height=0.18, stroke_width=0, fill_color=TEXT, fill_opacity=0.95).move_to(pt(-2.8, 0.05)),
        )
        self.play(FadeIn(bands), run_time=0.55)
        self.at("close together")
        bracket = Brace(bands, RIGHT, color=ACTION)
        linked = fit_text("OFTEN TRAVEL\nTOGETHER", max_w=3.0, size=30, color=ACTION, weight=BOLD).next_to(bracket, RIGHT, buff=0.25)
        self.play(GrowFromCenter(bracket), FadeIn(linked), run_time=0.75)
        self.at("Independent assortment applies")
        self.play(FadeIn(other, shift=UP * 0.1), run_time=0.65)
        separate_band = Rectangle(width=0.82, height=0.18, stroke_width=0, fill_color=TEXT, fill_opacity=0.95).move_to(pt(3.1, 0.3))
        self.play(FadeIn(separate_band), run_time=0.45)
        either = CurvedArrow(pt(2.3, 1.65), pt(3.9, 1.65), angle=-1.15, color=ACTION, stroke_width=5)
        lab = T("EITHER–OR", 30, ACTION, weight=BOLD).next_to(either, UP, buff=0.15)
        self.play(Create(either), FadeIn(lab), run_time=0.8)
        self.at("different chromosomes")
        self.play(Indicate(VGroup(other, separate_band), color=ACTION), run_time=0.65)
        self.finish()


class S10Rule(FilmScene):
    def construct(self):
        panels = TwoPanel("CROSSING OVER", "ASSORTMENT", colors=(PARENT_A, ACTION), top=2.65, bottom=-2.7, width=10.8)
        left = recombinant_rod(height=3.45)
        panels.put(left, "left")
        right = assortment_world(three=True).scale(0.72)
        panels.put(right, "right")
        self.play(FadeIn(panels), FadeIn(left), FadeIn(right), run_time=0.8)
        self.at("crossing over and assortment")
        self.play(Indicate(left, color=ACTION), Indicate(right.pairs, color=ACTION), run_time=0.8)
        self.at("chromosome sections")
        sections = T("SECTIONS", 30, PARENT_A, weight=BOLD).move_to(pt(-2.8, -3.1))
        self.play(FadeIn(sections), Indicate(left, color=ACTION), run_time=0.75)
        self.at("whole chromosomes")
        whole = T("WHOLE CHROMOSOMES", 30, ACTION, weight=BOLD).move_to(pt(2.8, -3.1))
        self.play(FadeIn(whole), Indicate(right.pairs, color=ACTION), run_time=0.75)
        self.at("Fertilization then joins")
        self.play(FadeOut(VGroup(panels, left, right, sections, whole)), run_time=0.45)
        egg = mix_icon(pt(-3.3, 0), (PARENT_A, PARENT_B), 1.35)
        sperm = mix_icon(pt(3.3, 0), (PARENT_B, PARENT_A), 1.35)
        egg_lab = T("egg", 28, TEXT).next_to(egg, DOWN, buff=0.22)
        sperm_lab = T("sperm", 28, TEXT).next_to(sperm, DOWN, buff=0.22)
        self.play(FadeIn(egg), FadeIn(sperm), FadeIn(egg_lab), FadeIn(sperm_lab), run_time=0.7)
        joined = cell_outline(pt(0, 0), rx=1.35, ry=1.55)
        self.play(FadeOut(VGroup(egg_lab, sperm_lab)), ReplacementTransform(VGroup(egg, sperm), joined), run_time=1.1)
        self.at("siblings different combinations")
        siblings = VGroup(
            mix_icon(pt(-4.5, -1.45), (PARENT_A, PARENT_B), 0.85),
            mix_icon(pt(-1.5, -1.45), (PARENT_B, PARENT_B), 0.85),
            mix_icon(pt(1.5, -1.45), (PARENT_A, PARENT_A), 0.85),
            mix_icon(pt(4.5, -1.45), (PARENT_B, PARENT_A), 0.85),
        )
        self.play(FadeOut(joined), LaggedStart(*[FadeIn(s, shift=UP * 0.12) for s in siblings], lag_ratio=0.14), run_time=1.1)
        self.finish()


class S11Close(FilmScene):
    def construct(self):
        icons = VGroup()
        combos = [
            (PARENT_A, PARENT_A), (PARENT_A, PARENT_B), (PARENT_B, PARENT_A),
            (PARENT_B, PARENT_B), (PARENT_A, PARENT_B), (PARENT_B, PARENT_A),
        ]
        for (x, y), cols in zip([(-4.5, 1.3), (-1.5, 1.3), (1.5, 1.3), (4.5, 1.3), (-2.7, -1.2), (2.7, -1.2)], combos):
            icons.add(mix_icon(pt(x, y), cols, 0.90))
        self.play(LaggedStart(*[FadeIn(i, shift=UP * 0.1) for i in icons], lag_ratio=0.10), run_time=1.0)
        self.at("not a promise")
        not_guarantee = T("CHANCE, NOT GUARANTEE", 34, ACTION, weight=BOLD).move_to(pt(0, 3.4))
        self.play(FadeIn(not_guarantee, shift=DOWN * 0.1), run_time=0.55)
        self.at("more allele combinations")
        self.play(LaggedStart(*[Indicate(i, color=ACTION) for i in icons], lag_ratio=0.10), run_time=1.0)
        self.at("conditions change")
        environment = RoundedRectangle(corner_radius=0.42, width=11.6, height=6.6, stroke_width=0, fill_color=BLUE, fill_opacity=0.08).move_to(pt(0, -0.42))
        environment.set_z_index(-2)
        self.play(FadeIn(environment), run_time=0.8)
        self.at("some combinations may")
        self.play(icons[0].animate.set_opacity(0.15), icons[3].animate.set_opacity(0.15), icons[4].animate.set_opacity(0.15), run_time=1.0)
        self.at("survive and reproduce")
        survivors = VGroup(icons[1], icons[2], icons[5])
        offspring = VGroup(
            mix_icon(pt(-1.1, -2.30), (PARENT_A, PARENT_B), 0.58),
            mix_icon(pt(0.0, -2.30), (PARENT_B, PARENT_A), 0.58),
            mix_icon(pt(1.1, -2.30), (PARENT_B, PARENT_A), 0.58),
        )
        self.play(Indicate(survivors, color=ACTION), LaggedStart(*[FadeIn(o, scale=0.8) for o in offspring], lag_ratio=0.16), run_time=1.1)
        self.add(stage_tag("schematic"))
        self.at("does not guarantee")
        self.play(Indicate(not_guarantee, color=ACTION), run_time=0.8)
        self.finish()


class S12End(EndCard):
    LINE = "Crossing over and assortment remix alleles."
