"""Pairs First, Copies Second.

COLOR MAP
  GREEN  chromosome inherited from one parent
  ORANGE chromosome inherited from the other parent
  BLUE   cell boundary
  YELLOW current action / centromere connection
  TEXT   explanatory labels

The chromosome and cell builders below are the single source for every carried
picture.  Chromosomes are schematic rods only; no DNA or molecular structure is
drawn.
"""
from bp_parts import *

PARENT_A = GREEN
PARENT_B = ORANGE
CELL = BLUE
ACTION = YELLOW


def pt(x, y):
    return np.array([x, y, 0.0])


def rod(color, height, center=ORIGIN, width=0.34):
    return RoundedRectangle(
        corner_radius=0.15,
        width=width,
        height=height,
        stroke_color=color,
        stroke_width=4,
        fill_color=color,
        fill_opacity=0.58,
    ).move_to(center)


def copied_chromosome(color, height, center=ORIGIN, scale=1.0, connection=True):
    """A copied chromosome: two sister rods joined at one yellow connection."""
    a = rod(color, height * scale, width=0.26 * scale).rotate(0.43)
    b = rod(color, height * scale, width=0.26 * scale).rotate(-0.43)
    g = VGroup(a, b).move_to(center)
    if connection:
        c = Dot(g.get_center(), radius=0.11 * scale, color=ACTION)
        g.add(c)
        g.connection = c
    return g


def cell_outline(center=ORIGIN, rx=3.0, ry=2.65, stroke=4):
    return Ellipse(
        width=2 * rx,
        height=2 * ry,
        stroke_color=CELL,
        stroke_width=stroke,
        fill_color=CELL,
        fill_opacity=0.15,
    ).move_to(center)


def starting_cell(center=pt(0, -0.2), copied=False, brackets=False):
    """The same two-pair diploid model used throughout scenes 1--4."""
    cx, cy = center[:2]
    boundary = cell_outline(center)
    make = copied_chromosome if copied else rod
    if copied:
        chroms = VGroup(
            make(PARENT_A, 2.25, pt(cx - 0.72, cy + 0.90), scale=1.0),
            make(PARENT_B, 2.25, pt(cx + 0.72, cy + 0.90), scale=1.0),
            make(PARENT_A, 1.25, pt(cx - 0.72, cy - 1.25), scale=1.0),
            make(PARENT_B, 1.25, pt(cx + 0.72, cy - 1.25), scale=1.0),
        )
    else:
        chroms = VGroup(
            make(PARENT_A, 2.25, pt(cx - 0.72, cy + 0.90)),
            make(PARENT_B, 2.25, pt(cx + 0.72, cy + 0.90)),
            make(PARENT_A, 1.25, pt(cx - 0.72, cy - 1.25)),
            make(PARENT_B, 1.25, pt(cx + 0.72, cy - 1.25)),
        )
    g = VGroup(boundary, chroms)
    g.boundary, g.chroms = boundary, chroms
    if brackets:
        long_b = Brace(VGroup(chroms[0], chroms[1]), LEFT, color=ACTION)
        short_b = Brace(VGroup(chroms[2], chroms[3]), LEFT, color=ACTION)
        g.add(long_b, short_b)
        g.brackets = VGroup(long_b, short_b)
    return g


def divided_cells(copied=True, pulse_connections=False):
    """The carried state after division one: mixed homologs in two cells."""
    cells = VGroup()
    specs = [(-3.15, ((PARENT_A, PARENT_B),)), (3.15, ((PARENT_B, PARENT_A),))]
    for x, mix_wrap in specs:
        long_c, short_c = mix_wrap[0]
        boundary = cell_outline(pt(x, -0.15), rx=2.35, ry=2.5)
        if copied:
            long_m = copied_chromosome(long_c, 2.25, pt(x - 0.48, 0.55), scale=0.92)
            short_m = copied_chromosome(short_c, 1.35, pt(x + 0.62, -1.05), scale=0.92)
        else:
            long_m = rod(long_c, 2.05, pt(x - 0.48, 0.55), width=0.30)
            short_m = rod(short_c, 1.20, pt(x + 0.62, -1.05), width=0.30)
        one = VGroup(boundary, long_m, short_m)
        one.boundary, one.long_m, one.short_m = boundary, long_m, short_m
        if pulse_connections and copied:
            pulse(long_m.connection, base=2.5, amp=2.0, speed=2.3)
            pulse(short_m.connection, base=2.5, amp=2.0, speed=2.3)
        cells.add(one)
    return cells


def sway(m, amp=0.35, speed=2.4, seed=0.0):
    """Rock a chromosome about its own centre (incremental, so it composes with a parent bob)."""
    m._sw_t = seed

    def u(mob, dt):
        mob._sw_t += dt
        mob.rotate(amp * speed * np.cos(speed * mob._sw_t) * dt, about_point=mob.get_center())
    return m.add_updater(u)


def animate_held(cells):
    """Ambient motion for the held predict picture: cells drift, chromosomes rock, outlines breathe."""
    for i, c in enumerate(cells):
        pulse(c.boundary, base=4.0, amp=1.0, speed=2.6)
        bob(c, amp=0.30, speed=2.0, seed=0 if c.get_x() < 0 else 2)
        sway(c.long_m, seed=i)
        sway(c.short_m, amp=0.45, speed=2.9, seed=i + 1.3)
    return cells


def four_cells():
    """The carried state after division two."""
    group = VGroup()
    for x, y, lc, sc in [
        (-2.75, 1.35, PARENT_A, PARENT_B), (2.75, 1.35, PARENT_A, PARENT_B),
        (-2.75, -1.35, PARENT_B, PARENT_A), (2.75, -1.35, PARENT_B, PARENT_A),
    ]:
        boundary = cell_outline(pt(x, y), rx=1.02, ry=1.15, stroke=3.5)
        long_m = rod(lc, 1.25, pt(x - 0.25, y), width=0.22)
        short_m = rod(sc, 0.78, pt(x + 0.28, y), width=0.22)
        one = VGroup(boundary, long_m, short_m)
        one.boundary = boundary
        group.add(one)
    return group


def parent_key():
    a = VGroup(Dot(color=PARENT_A, radius=0.09), T("one parent", 28, PARENT_A)).arrange(RIGHT, buff=0.14)
    b = VGroup(Dot(color=PARENT_B, radius=0.09), T("other parent", 28, PARENT_B)).arrange(RIGHT, buff=0.14)
    return VGroup(a, b).arrange(DOWN, aligned_edge=LEFT, buff=0.18)


class S01Hook(SpokenScene):
    def construct(self):
        world = starting_cell(brackets=False)
        pulse(world.boundary, base=4.0, amp=0.7, speed=1.4)
        self.play(FadeIn(world.boundary), run_time=0.7)
        self.play(LaggedStart(*[FadeIn(c, shift=UP * 0.12) for c in world.chroms], lag_ratio=0.12), run_time=1.2)
        self.at("losing any chromosome type")
        q = T("How can a cell halve its sets?", 34, ACTION, weight=BOLD).move_to(pt(0, 3.28))
        self.play(FadeIn(q, shift=DOWN * 0.12), run_time=0.55)
        self.at("Watch this cell")
        self.play(Rotate(world.chroms, angle=0.10), run_time=1.2, rate_func=there_and_back)
        self.at("a large pair")
        long_b = Brace(VGroup(world.chroms[0], world.chroms[1]), LEFT, color=ACTION)
        self.play(GrowFromCenter(long_b), run_time=0.55)
        self.at("a small pair")
        short_b = Brace(VGroup(world.chroms[2], world.chroms[3]), LEFT, color=ACTION)
        self.play(GrowFromCenter(short_b), run_time=0.55)
        self.at("Green chromosomes")
        key = parent_key().move_to(pt(4.75, 1.0))
        self.play(FadeIn(key[0], shift=LEFT * 0.15), Indicate(VGroup(world.chroms[0], world.chroms[2]), color=PARENT_A), run_time=0.8)
        self.at("Orange chromosomes")
        self.play(FadeIn(key[1], shift=LEFT * 0.15), Indicate(VGroup(world.chroms[1], world.chroms[3]), color=PARENT_B), run_time=0.8)
        self.at("Every pair")
        title = T("Pairs First, Copies Second", 28, TEXT, font=TITLE_FONT).move_to(pt(0, 3.28))
        self.play(swap(q, title), Indicate(VGroup(long_b, short_b), color=ACTION), run_time=0.9)
        self.finish()


class S02Homologs(SpokenScene):
    def construct(self):
        world = starting_cell(brackets=True)
        pulse(world.boundary, base=4.0, amp=0.7, speed=1.4)
        self.add(world)
        long_pair = VGroup(world.chroms[0], world.chroms[1])
        others = VGroup(world.chroms[2], world.chroms[3], world.brackets)
        self.at("partners in each pair")
        self.play(FadeOut(others), long_pair.animate.scale(1.35).move_to(pt(0, 0)), run_time=1.0)
        self.at("homologous chromosomes")
        hom = T("HOMOLOGOUS CHROMOSOMES", 32, ACTION, weight=BOLD).move_to(pt(0, 3.15))
        self.play(FadeIn(hom, shift=DOWN * 0.12), run_time=0.5)
        self.at("genes in matching positions")
        bands = VGroup()
        for y in (-0.75, 0.0, 0.78):
            pair = VGroup()
            for c in long_pair:
                band = Rectangle(width=0.58, height=0.17, stroke_width=0, fill_color=TEXT, fill_opacity=0.92).move_to(pt(c.get_x(), y))
                pair.add(band)
            bands.add(pair)
        self.play(LaggedStart(*[FadeIn(b, shift=LEFT * 0.15) for b in bands], lag_ratio=0.18), run_time=1.1)
        scan = Line(pt(-1.75, -0.75), pt(1.75, -0.75), color=ACTION, stroke_width=5).set_opacity(0.65)
        bob(scan, amp=0.55, speed=0.85)
        self.add(scan)
        self.at("alleles may differ")
        A = T("A", 30, BG, weight=BOLD).move_to(bands[1][0])
        a = T("a", 30, BG, weight=BOLD).move_to(bands[1][1])
        A.layout_ok = a.layout_ok = True
        self.play(FadeIn(A), FadeIn(a), run_time=0.6)
        self.at("An allele")
        allele = T("allele = a version of a gene", 30, TEXT).move_to(pt(0, -3.32))
        self.play(FadeIn(allele, shift=UP * 0.12), run_time=0.6)
        self.at("Matching does not mean identical")
        self.play(Indicate(A, color=ACTION), Indicate(a, color=ACTION), run_time=0.9)
        self.at("starting cell is diploid")
        pulled = starting_cell(brackets=False)
        dip = T("DIPLOID · both members of every pair", 30, ACTION).move_to(pt(0, 3.15))
        scan.clear_updaters()
        self.play(FadeOut(VGroup(bands, A, a, allele, scan)), ReplacementTransform(VGroup(world.boundary, long_pair), pulled), swap(hom, dip), run_time=1.15)
        pulse(pulled.boundary, base=4.0, amp=0.7, speed=1.4)
        self.finish()


class S03Copy(SpokenScene):
    def construct(self):
        world = starting_cell()
        pulse(world.boundary, base=4.0, amp=0.7, speed=1.4)
        self.add(world)
        self.at("each chromosome copies")
        copied = starting_cell(copied=True)
        sweep = Rectangle(width=0.35, height=5.2, stroke_width=0, fill_color=ACTION, fill_opacity=0.28).move_to(pt(-2.25, -0.2))
        self.add(sweep)
        self.play(
            *[ReplacementTransform(world.chroms[i], copied.chroms[i]) for i in range(4)],
            sweep.animate.shift(RIGHT * 4.5),
            run_time=1.6,
        )
        self.remove(sweep)
        self.at("Each rod becomes")
        sisters = T("JOINED SISTER CHROMATIDS", 30, ACTION).move_to(pt(0, 3.18))
        self.play(FadeIn(sisters, shift=DOWN * 0.12), Indicate(copied.chroms[0], color=ACTION), run_time=0.8)
        self.at("DNA amount doubled")
        amount = ValueTracker(1)
        read = Readout(
            [("chromosomes", lambda: 4, "{:.0f}", TEXT), ("DNA amount", lambda: amount.get_value(), "×{:.0f}", ACTION)],
            at=pt(4.5, -1.9), widest=[4, 2], size=28, title="copying",
        )
        self.play(FadeIn(read), amount.animate.set_value(2), copied.animate.shift(LEFT * 1.35), world.boundary.animate.shift(LEFT * 1.35), run_time=1.2)
        bob(copied, amp=0.14, speed=1.0)
        self.at("chromosome count did not")
        self.play(Indicate(read, color=ACTION), run_time=0.7)
        self.at("An X shape")
        xlab = T("one copied chromosome", 28, TEXT).move_to(pt(4.5, 0.45))
        arrow = Arrow(xlab.get_left(), copied.chroms[1].get_right(), buff=0.15, color=ACTION, stroke_width=4)
        self.play(FadeIn(xlab), GrowArrow(arrow), run_time=0.7)
        self.at("Count join sister")
        one = T("count as 1", 30, ACTION, weight=BOLD).move_to(pt(4.5, 0.45))
        self.play(FadeOut(VGroup(xlab, arrow)), FadeIn(one), Indicate(copied.chroms[1].connection, color=ACTION, scale_factor=1.8), run_time=0.8)
        self.at("connection separates")
        self.play(Flash(copied.chroms[1].connection, color=ACTION, flash_radius=0.45), run_time=0.7)
        self.finish()


class S04FirstDivision(SpokenScene):
    def construct(self):
        world = starting_cell(copied=True)
        pulse(world.boundary, base=4.0, amp=0.7, speed=1.4)
        self.add(world)
        self.at("homologous chromosomes meet")
        self.play(world.chroms.animate.arrange_in_grid(rows=2, cols=2, buff=(0.38, 0.28)).move_to(pt(0, -0.1)), run_time=1.0)
        self.at("first division")
        arrows = VGroup(
            Arrow(pt(-0.5, 0.7), pt(-2.35, 0.7), color=ACTION, buff=0.05),
            Arrow(pt(0.5, 0.7), pt(2.35, 0.7), color=ACTION, buff=0.05),
            Arrow(pt(-0.5, -0.85), pt(-2.35, -0.85), color=ACTION, buff=0.05),
            Arrow(pt(0.5, -0.85), pt(2.35, -0.85), color=ACTION, buff=0.05),
        )
        self.play(LaggedStart(*[GrowArrow(a) for a in arrows], lag_ratio=0.12), run_time=0.85)
        self.at("each homolog moves away")
        target = divided_cells(copied=True)
        self.play(
            FadeOut(arrows),
            ReplacementTransform(world.boundary, VGroup(target[0].boundary, target[1].boundary)),
            ReplacementTransform(world.chroms[0], target[0].long_m),
            ReplacementTransform(world.chroms[3], target[0].short_m),
            ReplacementTransform(world.chroms[1], target[1].long_m),
            ReplacementTransform(world.chroms[2], target[1].short_m),
            run_time=1.8,
        )
        moving_left = VGroup(target[0].long_m, target[0].short_m)
        moving_right = VGroup(target[1].long_m, target[1].short_m)
        bob(moving_left, amp=0.34, speed=0.9, seed=0)
        bob(moving_right, amp=0.34, speed=0.9, seed=2)
        self.add(moving_left, moving_right)
        self.at("green long chromosome")
        self.play(Indicate(target[0].long_m, color=PARENT_A), Indicate(target[0].short_m, color=PARENT_B), run_time=0.9)
        self.at("other homologs")
        self.play(Indicate(target[1].long_m, color=PARENT_B), Indicate(target[1].short_m, color=PARENT_A), run_time=0.9)
        self.finish()


class S05Predict(SpokenScene):
    def construct(self):
        cells = divided_cells(copied=True, pulse_connections=True)
        animate_held(cells)
        self.add(cells)
        self.at("member of every homologous pair")
        self.play(*[Indicate(VGroup(c.long_m, c.short_m), color=ACTION) for c in cells], run_time=0.9)
        self.at("still made of joined sisters")
        conns = VGroup(*[m.connection for c in cells for m in (c.long_m, c.short_m)])
        self.play(Indicate(conns, color=ACTION, scale_factor=1.5), run_time=0.8)
        self.at("What must separate")
        q = question_card("WHAT SEPARATES NEXT?", y=-3.35, size=34, max_w=9.8)
        self.play(FadeIn(q.question, shift=UP * 0.15), run_time=0.6)
        self.at("Follow the yellow connection")
        self.play(LaggedStart(*[Flash(d, color=ACTION, flash_radius=0.34) for d in conns], lag_ratio=0.14), run_time=1.0)
        self.finish()


class S06Pause(PredictPause):
    QUESTION = "WHAT SEPARATES NEXT?"
    SECONDS = 4.5
    CARD = {"y": -3.35, "size": 34, "max_w": 9.8}
    RING_AT = (6.0, -3.25, 0)

    def backdrop(self):
        cells = divided_cells(copied=True, pulse_connections=True)
        animate_held(cells)
        return cells


class S07SecondDivision(SpokenScene):
    def construct(self):
        cells = divided_cells(copied=True, pulse_connections=True)
        for c in cells:
            bob(c, amp=0.34, speed=0.9, seed=0 if c.get_x() < 0 else 2)
        self.add(cells)
        self.at("sister chromatids separate")
        for c in cells:
            self.play(Flash(c.long_m.connection, color=ACTION), Flash(c.short_m.connection, color=ACTION), run_time=0.35)
        self.at("No DNA copying")
        no_copy = T("NO COPYING BETWEEN DIVISIONS", 30, ACTION, weight=BOLD).move_to(pt(0, 3.25))
        self.play(FadeIn(no_copy, shift=DOWN * 0.12), run_time=0.55)
        self.at("Each cell divides again")
        for c in cells:
            c.clear_updaters()
        finished = four_cells()
        self.play(ReplacementTransform(cells, finished), run_time=2.0)
        for c in finished:
            pulse(c.boundary, base=3.5, amp=0.55, speed=1.5)
            bob(c, amp=0.10, speed=0.9, seed=1 if c.get_x() < 0 else 3)
        self.at("joined copies pull apart")
        self.play(*[Indicate(VGroup(c[1], c[2]), color=ACTION) for c in finished], run_time=0.9)
        self.at("finished cells hold")
        label = T("one chromosome from every original pair", 30, TEXT).move_to(pt(0, 3.25))
        self.play(swap(no_copy, label), run_time=0.8)
        self.finish()


class S08Haploid(SpokenScene):
    def construct(self):
        cells = four_cells()
        for c in cells:
            pulse(c.boundary, base=3.5, amp=0.55, speed=1.5)
            bob(c, amp=0.10, speed=0.9, seed=1 if c.get_x() < 0 else 3)
        self.add(cells)
        self.at("cells are haploid")
        hap = T("HAPLOID · one chromosome set", 34, ACTION, weight=BOLD).move_to(pt(0, 3.25))
        self.play(FadeIn(hap, shift=DOWN * 0.12), run_time=0.65)
        self.at("simple animal model")
        scope = scope_tag("simple animal model", size=24)
        self.play(FadeIn(scope), *[Indicate(c, color=CELL) for c in cells], run_time=0.8)
        self.at("Human egg formation")
        egg = Circle(radius=1.55, color=CELL, fill_color=CELL, fill_opacity=0.08).move_to(pt(-3.2, 0))
        polar = VGroup(*[Circle(radius=0.30, color=CELL, fill_color=CELL, fill_opacity=0.08) for _ in range(3)]).arrange(DOWN, buff=0.18).next_to(egg, RIGHT, buff=0.28)
        egg_pic = VGroup(egg, polar)
        egg_lab = T("uneven egg formation", 28, TEXT).next_to(egg_pic, DOWN, buff=0.3)
        self.play(FadeOut(VGroup(cells, hap, scope)), GrowFromCenter(egg), LaggedStart(*[GrowFromCenter(p) for p in polar], lag_ratio=0.18), FadeIn(egg_lab), run_time=1.2)
        self.at("plants make spores")
        spore = VGroup(
            Circle(radius=0.65, color=PARENT_A, fill_color=PARENT_A, fill_opacity=0.14),
            *[Dot(radius=0.07, color=PARENT_A).move_to(pt(4.0 + 0.28*np.cos(a), 0.28*np.sin(a))) for a in np.linspace(0, TAU, 7)[:-1]],
        ).move_to(pt(4.0, 0))
        spore_lab = T("plant spore", 28, TEXT).next_to(spore, DOWN, buff=0.3)
        schematic = T("SCHEMATIC", 24, GREY).move_to(pt(0, 2.9))
        self.play(FadeIn(spore, scale=0.8), FadeIn(spore_lab), FadeIn(schematic), run_time=0.9)
        self.at("refinements do not change")
        back = four_cells()
        self.play(FadeOut(VGroup(egg_pic, egg_lab, spore, spore_lab, schematic)), FadeIn(back), run_time=1.0)
        rule = T("same separation rule", 32, ACTION).move_to(pt(0, 3.25))
        self.play(FadeIn(rule, shift=DOWN * 0.1), run_time=0.6)
        self.finish()


def pathway_stage(title, copied=False, separated=False, center=ORIGIN):
    """Compact chromosome action used in the two-step rule pathway."""
    frame = RoundedRectangle(corner_radius=0.2, width=5.3, height=2.15, color=CELL, stroke_width=3,
                             fill_color=CELL, fill_opacity=0.12).move_to(center)
    lab = T(title, 28, TEXT, weight=BOLD).move_to(frame.get_top() + DOWN * 0.36)
    if copied:
        left = copied_chromosome(PARENT_A, 1.05, center + LEFT * (1.15 if separated else 0.38), scale=0.8)
        right = copied_chromosome(PARENT_B, 1.05, center + RIGHT * (1.15 if separated else 0.38), scale=0.8)
    else:
        left = rod(PARENT_A, 1.10, center + LEFT * (1.15 if separated else 0.38), width=0.24)
        right = rod(PARENT_B, 1.10, center + RIGHT * (1.15 if separated else 0.38), width=0.24)
    pair = VGroup(left, right).shift(DOWN * 0.22)
    return VGroup(frame, lab, pair)


class S09Rule(SpokenScene):
    def construct(self):
        carried = four_cells()
        self.add(carried)
        self.at("Meiosis separates pairs")
        heading = T("PAIRS FIRST, COPIES SECOND", 38, ACTION, weight=BOLD).move_to(pt(0, 3.25))
        self.play(FadeOut(carried), FadeIn(heading, shift=DOWN * 0.12), run_time=0.7)
        paired = pathway_stage("PAIRED HOMOLOGS", copied=True, separated=False, center=pt(-3.5, 1.1))
        split_pairs = pathway_stage("SEPARATED PAIRS", copied=True, separated=True, center=pt(3.5, 1.1))
        arrow1 = Arrow(pt(-0.55, 1.1), pt(0.55, 1.1), color=ACTION, stroke_width=6)
        self.play(FadeIn(paired), run_time=0.6)
        self.at("first division separates")
        self.play(GrowArrow(arrow1), ReplacementTransform(paired.copy(), split_pairs), run_time=1.1)
        self.at("halves the chromosome sets")
        first_lab = T("1 · homologs apart", 28, ACTION).move_to(pt(0, -0.25))
        self.play(FadeIn(first_lab), Indicate(split_pairs[2], color=ACTION), run_time=0.75)
        self.at("The second separates")
        sisters = pathway_stage("JOINED SISTERS", copied=True, separated=False, center=pt(-3.5, -2.05))
        copies = pathway_stage("SEPARATED COPIES", copied=False, separated=True, center=pt(3.5, -2.05))
        arrow2 = Arrow(pt(-0.55, -2.05), pt(0.55, -2.05), color=ACTION, stroke_width=6)
        self.play(FadeIn(sisters), GrowArrow(arrow2), ReplacementTransform(sisters.copy(), copies), run_time=1.2)
        self.at("sister chromatids")
        self.play(Indicate(copies[2], color=ACTION), run_time=0.7)
        self.at("not mitosis repeated")
        mit = T("MITOSIS: homologs never pair", 28, GREY).move_to(pt(0, -3.45))
        strike = Line(mit.get_left() + LEFT * 0.1, mit.get_right() + RIGHT * 0.1, color=RED, stroke_width=5)
        strike.layout_ok = True
        self.play(FadeIn(mit), Create(strike), run_time=0.75)
        self.at("never separates homologous pairs")
        self.play(FadeOut(VGroup(mit, strike)), Indicate(arrow1, color=ACTION), run_time=0.8)
        self.finish()


def haploid_model(center, colors):
    boundary = cell_outline(center, rx=1.45, ry=1.55, stroke=3.5)
    long_m = rod(colors[0], 1.55, center + LEFT * 0.28, width=0.25)
    short_m = rod(colors[1], 0.95, center + RIGHT * 0.32, width=0.25)
    return VGroup(boundary, long_m, short_m)


class S10Close(SpokenScene):
    def construct(self):
        egg = haploid_model(pt(-3.6, 0), (PARENT_A, PARENT_B))
        sperm = haploid_model(pt(3.6, 0), (PARENT_B, PARENT_A))
        egg_lab = T("egg", 28, TEXT).next_to(egg, DOWN, buff=0.2)
        sperm_lab = T("sperm", 28, TEXT).next_to(sperm, DOWN, buff=0.2)
        self.add(egg, sperm, egg_lab, sperm_lab)
        self.at("egg and sperm later join")
        dip = starting_cell(center=pt(0, -0.2))
        self.play(FadeOut(VGroup(egg_lab, sperm_lab)), ReplacementTransform(VGroup(egg, sperm), dip), run_time=1.5)
        pulse(dip.boundary, base=4.0, amp=0.7, speed=1.4)
        self.at("restore a diploid cell")
        label = T("DIPLOID RESTORED", 34, ACTION, weight=BOLD).move_to(pt(0, 3.25))
        self.play(FadeIn(label, shift=DOWN * 0.12), run_time=0.6)
        self.at("keeps chromosome number")
        loop = VGroup(
            CurvedArrow(pt(3.1, 1.6), pt(5.2, 0), angle=-1.1, color=ACTION),
            CurvedArrow(pt(5.2, -0.3), pt(3.1, -1.8), angle=-1.1, color=ACTION),
            T("same number", 28, ACTION).move_to(pt(4.7, 2.25)),
        )
        self.play(dip.animate.shift(LEFT * 1.45), label.animate.shift(LEFT * 1.45), FadeIn(loop), run_time=1.0)
        self.at("different chromosome mixes")
        self.play(FadeOut(VGroup(dip, label, loop)), run_time=0.4)
        products = VGroup(
            haploid_model(pt(-4.5, 0.65), (PARENT_A, PARENT_B)),
            haploid_model(pt(-1.5, -0.65), (PARENT_A, PARENT_B)),
            haploid_model(pt(1.5, 0.65), (PARENT_B, PARENT_A)),
            haploid_model(pt(4.5, -0.65), (PARENT_B, PARENT_A)),
        ).scale(0.82)
        for i, product in enumerate(products):
            bob(product, amp=0.10, speed=0.9, seed=i)
        mix = T("different chromosome mixes", 34, ACTION).move_to(pt(0, 3.2))
        self.play(LaggedStart(*[FadeIn(p, shift=UP * 0.15) for p in products], lag_ratio=0.18), FadeIn(mix), run_time=1.4)
        self.at("next film asks why")
        next_q = T("What creates different allele mixes?", 30, TEXT).move_to(pt(0, -3.15))
        self.play(FadeIn(next_q, shift=UP * 0.12), run_time=0.6)
        self.finish()


class S11End(EndCard):
    LINE = "Meiosis separates pairs, then copies."
