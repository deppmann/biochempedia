"""Single-cell RNA sequencing, staged against the supplied narration.

Color map follows the patch-clamp palette: grey is structure, blue is the
sequencing workflow, yellow highlights a measurement, green is a control,
red flags loss, and gold marks the questions and dates. Teal, purple, and
orange distinguish RNA patterns and their corresponding cell groups.
"""

from bp_parts import *
from bp_style import EndCard

PURPLE = "#B58CD9"
ORANGE = "#F29E4C"
PATTERNS = (TEAL, PURPLE, ORANGE)
QUESTION = "Is every cluster a proven cell type?"
CELL_SITES = (
    (-5, 1.36), (-3, 1.45), (-1, 1.38), (1, 1.45), (3, 1.36),
    (-5, -0.74), (-3, -0.83), (-1, -0.76), (1, -0.83), (3, -0.74),
)
TISSUE_TYPES = (2, 1, 0, 2, 1, 0, 2, 1, 0, 2)
HOOK_TYPES = (0, 1, 2, 0, 1, 2, 0, 1, 2, 0)
# Four illustrated reads from each of the three barcoded cells.
COUNTS = np.array([[3, 1, 0], [0, 3, 1], [1, 0, 3]]).T


def xy(x, y):
    return np.array([x, y, 0.0])


def heading(text, color=TEXT):
    return fit_text(text, size=36, min_size=28, color=color, max_w=11).move_to(xy(0, 3.25))


def footer(text, color=TEXT):
    return caption(text, size=31, color=color, y=-3.03).set_x(0)


def schematic():
    return scope_tag(size=28, color=TEXT)


def organic(points, color=GREY, fill="#263344", stroke=2.6):
    return VMobject().set_points_smoothly([xy(*p) for p in (*points, points[0])]).set_stroke(
        color, stroke
    ).set_fill(fill, 1)


def cell(kind, center=ORIGIN, scale=1, rna=True):
    """Cartoon outlines and abstract RNA particles. Each profile has a fixed dot count."""
    color = PATTERNS[kind]
    paints = ("#1D4652", "#3D345B", "#594036")
    if kind == 1:
        edge = organic(((-.89, .31), (-.48, .14), (-.40, .41), (-.26, .91),
                        (.03, .52), (.49, .48), (.84, .68), (.64, .28),
                        (.64, -.23), (.86, -.71), (.44, -.56), (.11, -.69),
                        (-.12, -.92), (-.30, -.54), (-.60, -.30), (-.94, -.30)),
                       GREY, paints[kind])
    else:
        edge = Ellipse(width=(1.48, 1.6, 1.82)[kind], height=(1.64, 1.6, 1.88)[kind],
                       color=GREY, stroke_width=2.6, fill_color=paints[kind], fill_opacity=1)
    dots = VGroup()
    for i in range((4, 7, 10)[kind] if rna else 0):
        angle = i * 2.39996
        radius = .135 * np.sqrt(i + 1)
        point = xy(radius * np.cos(angle), radius * np.sin(angle))
        dots.add(VGroup(Dot(point, radius=.106, color=color, fill_opacity=.24),
                        Dot(point, radius=.052, color=color)))
    group = VGroup(edge, dots).scale(scale, about_point=ORIGIN).shift(center)
    group.edge, group.rna = edge, dots
    return group


def drift_rna(cells):
    for row, sample in enumerate(cells):
        for index, dot in enumerate(sample.rna):
            bob(dot, amp=.08, speed=1.7 + .1 * (index % 3), seed=1.7 * row + index)


def tissue(types=TISSUE_TYPES):
    boundary = organic(((-6.08, 1.81), (-5.5, 2.44), (-3.4, 2.67), (-1, 2.54),
                        (1.2, 2.66), (3.6, 2.47), (4.1, 1.29), (4.04, -.53),
                        (3.76, -1.66), (2.3, -2.03), (.5, -1.94), (-1.8, -2.04),
                        (-4.1, -1.91), (-5.8, -1.67), (-6.14, -.37)))
    cells = VGroup(*(cell(kind, xy(*site)) for kind, site in zip(types, CELL_SITES)))
    return VGroup(boundary, cells)


def zoom_cells():
    return VGroup(cell(1, xy(-2.85, .20), 2.62), cell(0, xy(2.85, .20), 2.62))


def active_patterns():
    return VGroup(strands(xy(-2.85, -.42), (1.52, .6, 1.0), PURPLE),
                  strands(xy(2.85, -.42), (.56, 1.55, 1.1), TEAL))


def strands(center, widths, color, gap=.27):
    return VGroup(*(RoundedRectangle(width=w, height=.15, corner_radius=.07,
                                      stroke_width=0, fill_color=color, fill_opacity=1)
                    for w in widths)).arrange(DOWN, buff=gap, aligned_edge=LEFT).move_to(center)


def pool():
    """Color on the left end identifies the source cell of every abstract copy."""
    reads = VGroup()
    for i in range(12):
        x, y = (i % 4 - 1.5) * 2.55, (1 - i // 4) * 1.54
        body = RoundedRectangle(width=1.82, height=.36, corner_radius=.11,
                                color=BLUE, stroke_width=2, fill_color="#28465A", fill_opacity=1)
        tag = RoundedRectangle(width=.32, height=.29, corner_radius=.06,
                               stroke_width=0, fill_color=PATTERNS[i % 3], fill_opacity=1)
        tag.move_to(xy(-.69, 0))
        reads.add(VGroup(body, tag).move_to(xy(x, y)))
    return reads


def read_current(reads):
    for i, read in enumerate(reads):
        bob(read, amp=.25, speed=1.5, seed=i)


CLUSTER_CENTERS = (xy(-3.72, -.32), xy(0, .67), xy(3.74, -.57))
CLUSTER_OFFSETS = ((-.68, .55), (.52, .66), (-.47, -.55), (.63, -.58))


def cluster_world(highlight=False):
    """The same schematic point positions before annotation, prediction, and resolution changes."""
    stage = RoundedRectangle(width=12.0, height=5.16, corner_radius=.28,
                             fill_color="#213043", fill_opacity=1, color="#465B72",
                             stroke_width=2).move_to(xy(0, .04))
    groups, halos = VGroup(), VGroup()
    for i, (color, center) in enumerate(zip(PATTERNS, CLUSTER_CENTERS)):
        halos.add(Ellipse(width=3.02, height=2.65, color=color, stroke_width=3,
                          stroke_opacity=.85 if highlight and i == 1 else .5,
                          fill_color=color, fill_opacity=.24 if highlight and i == 1 else .14
                          ).move_to(center))
        groups.add(VGroup(*(Dot(center + xy(*offset), radius=.19, color=color)
                            for offset in CLUSTER_OFFSETS)))
    return stage, halos, groups


def cluster_motion(groups):
    for i, group in enumerate(groups):
        for j, dot in enumerate(group):
            bob(dot, amp=.14, speed=1.55, seed=i + j)


def count_matrix():
    tiles, values = VGroup(), VGroup()
    for column, profile in enumerate(COUNTS.T):
        tile_column, value_column = VGroup(), VGroup()
        for row, value in enumerate(profile):
            p = xy((column - 1) * 2.44 + .42, (1 - row) * 1.42 - .16)
            color = PATTERNS[column % 3]
            tile_column.add(RoundedRectangle(width=2.34, height=1.33, corner_radius=.12,
                                             color=color, stroke_width=1.5, stroke_opacity=.7,
                                             fill_color=interpolate_color(ManimColor("#223044"),
                                                                          ManimColor(color), value / 5.5),
                                             fill_opacity=1).move_to(p))
            value_column.add(M(str(value), 36).move_to(p))
        tiles.add(tile_column)
        values.add(value_column)
    return tiles, values


class S01Hook(SpokenScene):
    def construct(self):
        world = tissue()
        outline, cells = world
        drift_rna(cells)
        question = heading("How can you tell cells apart?", GOLD)
        self.add(world, schematic())
        self.at("can you tell")
        self.play(FadeIn(question), run_time=.65)
        self.at("averaging a whole", lead=.45)
        frame = RoundedRectangle(width=1.04, height=2.60, corner_radius=.10,
                                 color=BLUE, stroke_width=2, fill_color="#243648",
                                 fill_opacity=1).move_to(xy(5.32, -.64))
        measure = ValueTracker(np.mean([len(c.rna) for c in cells]))
        bar = always_redraw(lambda: RoundedRectangle(
            width=.78, height=2.32 * measure.get_value() / 10, corner_radius=.08,
            stroke_width=0, fill_color=YELLOW, fill_opacity=1
        ).align_to(xy(5.32, -1.80), DOWN).set_x(5.32))
        name = T("Avg. RNA\nper cell", 28).move_to(xy(5.32, 1.26))
        self.play(FadeOut(question), FadeIn(frame), FadeIn(bar), run_time=.5)
        self.play(FadeIn(name), run_time=.4)
        self.at("the average shifts")
        visible = list(cells)
        for indices, kind in (((2, 5, 8), 2), ((0, 3, 6, 9), 0)):
            outgoing = [visible[i] for i in indices]
            incoming = [cell(kind, xy(*CELL_SITES[i])) for i in indices]
            for i, sample in zip(indices, incoming):
                visible[i] = sample
            new_count = np.mean([len(sample.rna) for sample in visible])
            self.play(*(AnimationGroup(FadeOut(old, shift=DOWN * .22),
                                       FadeIn(new, shift=UP * .22), lag_ratio=.44)
                        for old, new in zip(outgoing, incoming)),
                      measure.animate.set_value(new_count), run_time=1.32)
            drift_rna(incoming)
        self.at("read one cell", lead=.45)
        ring = Circle(radius=1.04, color=YELLOW, stroke_width=5).move_to(xy(*CELL_SITES[1]))
        self.play(Create(ring), FadeOut(frame), FadeOut(bar), FadeOut(name), run_time=.65)
        pulse(ring, base=5.5, amp=1.5, speed=4)
        self.finish()


class S02Title(TitleCard):
    LESSON = "Single-cell RNA sequencing"
    TITLE = "Reading a Tissue One Cell at a Time"

    def construct(self):
        world = tissue(HOOK_TYPES)
        world.set_opacity(.32)
        drift_rna(world[1])
        title = fit_text(self.TITLE, size=53, min_size=42, max_w=11.8, font=TITLE_FONT)
        title.move_to(xy(0, 3.24))
        self.add(world)
        self.play(FadeIn(title), run_time=.46)
        self.wait(1.02)
        self.play(FadeOut(title), run_time=.46)


class S03WhyRna(SpokenScene):
    def construct(self):
        world, pair = tissue(HOOK_TYPES), zoom_cells()
        self.add(world, schematic())
        self.at("every cell")
        outline, cells = world
        self.play(FadeOut(outline), *(FadeOut(c) for i, c in enumerate(cells) if i not in (1, 2)),
                  ReplacementTransform(cells[1], pair[0]), ReplacementTransform(cells[2], pair[1]),
                  run_time=1.45)
        genome = VGroup(*(strands(c.edge.get_center(), (1.22, 1.22), BLUE) for c in pair))
        self.at("essentially the same", lead=.64)
        self.play(FadeIn(genome, shift=UP * .22), run_time=.55)
        label = footer("Same genome", BLUE)
        self.play(FadeIn(label), run_time=.35)
        drift_rna(pair)
        self.at("the genome alone", lead=.35)
        comparison = VGroup(*(RoundedRectangle(width=1.72, height=1.18, corner_radius=.12,
                                                stroke_width=4, color=YELLOW).move_to(g)
                              for g in genome))
        self.play(LaggedStart(*(Create(r) for r in comparison), lag_ratio=.32), run_time=.85)
        scans = VGroup(*(RoundedRectangle(width=1.57, height=.35, corner_radius=.08,
                                          stroke_width=0, fill_color=BLUE, fill_opacity=.40)
                         .move_to(g.get_center() + UP * .35) for g in genome))
        genome.set_z_index(1)
        self.play(FadeIn(scans), run_time=.25)
        self.play(scans.animate.shift(DOWN * .70), run_time=1.60, rate_func=linear)
        self.play(FadeOut(scans), FadeOut(comparison), run_time=.45)
        self.at("what differs is")
        self.play(FadeOut(label), genome.animate.shift(UP * .99).set_opacity(.38), run_time=.62)
        patterns = active_patterns()
        self.at("actively transcribes", lead=.7)
        self.play(LaggedStart(*(GrowFromEdge(s, LEFT) for p in patterns for s in p), lag_ratio=.18),
                  run_time=1.68)
        self.add(patterns)
        rna = footer("Active RNA")
        self.play(FadeIn(rna), run_time=.42)
        self.play(patterns[0].animate.shift(LEFT * .64), patterns[1].animate.shift(RIGHT * .64),
                  run_time=1.72)
        self.at("sequencing reads")
        inset = RoundedRectangle(width=2.15, height=1.52, corner_radius=.18, color=YELLOW,
                                 stroke_width=4).move_to(patterns[1])
        self.play(Create(inset), run_time=1.05)
        self.play(inset.animate.move_to(patterns[0]), run_time=1.36)
        pulse(inset, base=4.5, amp=1.6)
        self.finish()


class S04Barcode(SpokenScene):
    def construct(self):
        world = tissue(HOOK_TYPES)
        outline, cells = world
        self.add(world, schematic())
        drift_rna(cells)
        self.at("enzymes usually separate", lead=.75)
        for sample in cells:
            for dot in sample.rna:
                dot.clear_updaters()
        loose = VGroup(*(cell(i, xy(x, .13), 1.98) for i, x in enumerate((-4.02, 0, 4.02))))
        traced = (0, 1, 2)
        self.play(FadeOut(outline),
                  *(FadeOut(c, scale=.7) for i, c in enumerate(cells) if i not in traced),
                  LaggedStart(*(ReplacementTransform(cells[i], loose[i]) for i in traced),
                              lag_ratio=.20), run_time=3.18)
        drift_rna(loose)
        self.at("cell's captured rna", lead=.45)
        lengths = (1.56, .91, 1.25, 1.12)
        rna = VGroup(*(strands(xy(x, .80), lengths, color, gap=.17)
                       for x, color in zip((-4.02, 0, 4.02), PATTERNS)))
        self.play(FadeIn(rna, shift=UP * .22), run_time=.72)
        self.at("copied into dna", lead=.45)
        dna = VGroup(*(strands(xy(x, -.53), lengths, BLUE, gap=.17)
                       for x in (-4.02, 0, 4.02)))
        self.play(*(TransformFromCopy(a, b) for a, b in zip(rna, dna)), run_time=1.22)
        copy_label = footer("RNA copied into DNA", BLUE)
        self.play(FadeIn(copy_label), run_time=.42)
        self.at("every copy from")
        batches = VGroup(*(RoundedRectangle(width=2.10, height=1.41, corner_radius=.16,
                                            stroke_color=BLUE, stroke_width=3, fill_color=BLUE,
                                            fill_opacity=.18).move_to(g) for g in dna))
        self.play(FadeOut(copy_label), LaggedStart(*(FadeIn(b) for b in batches),
                                                  lag_ratio=.65), run_time=1.17)
        stripes = VGroup(*(VGroup(*(RoundedRectangle(width=.24, height=.15, corner_radius=.046,
                                                      stroke_width=0, fill_color=color, fill_opacity=1)
                                    .move_to(s.get_left() + RIGHT * .12) for s in group))
                           for color, group in zip(PATTERNS, dna)))
        self.at("cell's unique barcode", lead=.65)
        self.play(FadeOut(batches), LaggedStart(*(FadeIn(s, shift=RIGHT * .22)
                                                 for g in stripes for s in g),
                                                lag_ratio=.18), run_time=1.5)
        self.add(stripes)
        tag_label = footer("Cell barcode")
        self.play(FadeIn(tag_label), run_time=.45)
        self.at("with those tags")
        self.play(FadeOut(loose), FadeOut(rna), FadeOut(tag_label), run_time=1.1)
        reads = pool()
        self.at("dna is pooled", lead=.52)
        sources = VGroup(*(VGroup(dna[i % 3][i // 3].copy(), stripes[i % 3][i // 3].copy())
                           for i in range(len(reads))))
        self.remove(dna, *dna, stripes, *stripes)
        self.add(sources)
        self.play(LaggedStart(*(ReplacementTransform(a, b) for a, b in zip(sources, reads)),
                              lag_ratio=.11), run_time=1.65)
        self.add(reads)
        read_current(reads)
        self.play(FadeIn(footer("Pooled sequencing", BLUE)), run_time=.48)
        self.finish()


class S05Clusters(SpokenScene):
    def construct(self):
        reads, tiles_values = pool(), count_matrix()
        tiles, values = tiles_values
        pooled = footer("Pooled sequencing", BLUE)
        scope = schematic()
        self.add(reads, pooled, scope)
        read_current(reads)
        self.at("software sorts")
        for read in reads:
            read.clear_updaters()
        lanes = VGroup(*(VGroup(*reads[color::3]) for color in range(3)))
        self.add(lanes)
        lane_targets = [[xy(tiles[i].get_x(), 1.38 - .86 * row) for row in range(len(lane))]
                        for i, lane in enumerate(lanes)]
        self.play(FadeOut(pooled), LaggedStart(*(read.animate.move_to(target)
                    for lane, targets in zip(lanes, lane_targets) for read, target in zip(lane, targets)),
                    lag_ratio=.04), run_time=1.34)
        self.play(*(ReplacementTransform(lane, col) for lane, col in zip(lanes, tiles)),
                  run_time=.88)
        title = heading("Count matrix", BLUE)
        self.at("a count matrix")
        self.play(FadeIn(title), run_time=.52)
        self.at("rows are genes")
        genes = T("Genes", 30).move_to(xy(-4.60, -.16))
        self.play(FadeIn(genes), *(block.animate.set_fill(opacity=.44)
                                  for col in tiles for row, block in enumerate(col) if row != 1),
                  run_time=.52)
        self.at("columns are cells")
        cell_label = T("Cells", 30).move_to(xy(.42, 2.18))
        self.play(FadeIn(cell_label), *(block.animate.set_fill(opacity=1 if column == 1 else .44)
                                       for column, col in enumerate(tiles) for block in col),
                  run_time=.46)
        self.at("entries count reads")
        self.play(LaggedStart(*(FadeIn(g) for g in values), lag_ratio=.15),
                  *(block.animate.set_fill(opacity=1) for col in tiles for block in col),
                  run_time=2.15)
        self.at("software then groups", lead=.45)
        stage, halos, groups = cluster_world()
        stage.set_z_index(-1)
        self.play(FadeOut(values), FadeOut(genes), FadeOut(cell_label), FadeOut(title),
                  FadeIn(stage), run_time=.48)
        self.play(LaggedStart(*(ReplacementTransform(column, group[0])
                                for column, group in zip(tiles, groups)), lag_ratio=.13),
                  run_time=1.28)
        for halo in halos:
            halo.set_z_index(-.5)
        clusters_heading = heading("Clusters")
        self.play(FadeIn(halos), FadeIn(clusters_heading),
                  LaggedStart(*(FadeIn(dot, scale=.55) for group in groups for dot in group[1:]),
                              lag_ratio=.08), run_time=.82)
        cluster_motion(groups)
        self.at("known profiles", lead=.62)
        profiles = VGroup(*(strands(xy(c[0], -2.13), (.75, .36, .59), color).scale(.55)
                            for c, color in zip(CLUSTER_CENTERS, PATTERNS)))
        self.play(LaggedStart(*(FadeIn(p, shift=UP * .22) for p in profiles), lag_ratio=.38), run_time=1.16)
        self.at("proposes an identity")
        self.play(FadeOut(scope), run_time=.24)
        tags = VGroup(*(boxed_label(f"Candidate {letter}", color=color, size=28,
                                   pad=.16).move_to(xy(center[0], -3.00))
                        for center, color, letter in zip(CLUSTER_CENTERS, PATTERNS, "ABC")))
        self.play(FadeIn(tags, shift=UP * .17), run_time=.52)
        self.at("called annotation")
        self.play(swap(clusters_heading, heading("Annotation")), run_time=.7)
        self.finish()


def predict_world():
    stage, halos, groups = cluster_world(highlight=True)
    ghost = tissue()[0].set_fill(opacity=0).set_stroke("#516275", width=3, opacity=.52)
    question = question_card(QUESTION, y=3.27, size=37).set_x(0)
    return stage, ghost, halos, groups, question


class S06Predict(SpokenScene):
    def construct(self):
        stage, ghost, halos, groups, question = predict_world()
        tags = VGroup(*(boxed_label(f"Candidate {letter}", color=color, size=28, pad=.16)
                        .move_to(xy(c[0], -3.00)) for c, color, letter in
                        zip(CLUSTER_CENTERS, PATTERNS, "ABC")))
        title = heading("Annotation")
        self.add(stage, halos, groups, tags, title)
        cluster_motion(groups)
        self.at("look closely")
        self.play(FadeOut(tags), FadeOut(title), run_time=.62)
        halos.set_z_index(1)
        groups.set_z_index(2)
        self.play(Create(ghost), run_time=2.15)
        self.add(schematic())
        self.at("by their rna")
        self.play(halos[1].animate.scale(1.07), run_time=1.22)
        self.play(halos[1].animate.scale(1 / 1.07), run_time=1.35)
        self.at("predict if")
        self.play(FadeIn(question), run_time=.72)
        pulse(halos[1], base=3, amp=1.7, speed=2.8)
        self.finish()


class S07Pause(NarratedScene):
    def construct(self):
        stage, ghost, halos, groups, question = predict_world()
        self.add(stage, ghost, halos, groups, question, schematic())
        accent = VGroup(halos[1], groups[1])
        self.play(accent.animate.stretch(1.13, 0), rate_func=there_and_back,
                  run_time=self.narration_s)


def resolution_control(value):
    track = RoundedRectangle(width=3.6, height=.15, corner_radius=.07, stroke_width=0,
                             fill_color="#506275", fill_opacity=1).move_to(xy(.64, -3.04))
    thumb = Dot(xy(-.98, -3.04), radius=.15, color=YELLOW)
    thumb.add_updater(lambda m: m.set_x(-.98 + 3.24 * value.get_value()))
    return VGroup(T("Resolution", 28).move_to(xy(-2.66, -3.04)), track, thumb)


class S08Limits(SpokenScene):
    def construct(self):
        stage, ghost, halos, groups, question = predict_world()
        self.add(stage, ghost, halos, groups, question, schematic())
        self.at("treat a cluster")
        candidate = heading("Candidate type", GOLD)
        self.play(swap(question, candidate), FadeOut(ghost), run_time=.86)
        cluster_motion(groups)
        self.at("finer settings")
        setting = ValueTracker(0)
        control = resolution_control(setting)
        self.play(FadeIn(control), run_time=.56)
        center = CLUSTER_CENTERS[1]
        top, bottom = VGroup(*groups[1][:2]), VGroup(*groups[1][2:])
        for dot in groups[1]:
            dot.clear_updaters()
        top_halo, bottom_halo = (
            Ellipse(width=2.18, height=.92, color=PURPLE, stroke_width=3, fill_color=PURPLE,
                    fill_opacity=.18).move_to(center + xy(shift, y))
            for shift, y in ((-.28, 1.02), (.28, -1.02))
        )
        self.at("split one cluster", lead=.9)
        self.play(setting.animate.set_value(1), FadeOut(halos[1]),
                  top.animate.shift(xy(-.28, .39)), bottom.animate.shift(xy(.28, -.42)),
                  FadeIn(top_halo), FadeIn(bottom_halo), run_time=2.13)
        self.at("cells can enter")
        state_label = footer("Temporary state", YELLOW)
        dot = bottom[1]
        self.play(FadeOut(control), dot.animate.set_color(YELLOW).scale(1.26), run_time=.95)
        self.play(FadeIn(state_label), run_time=.55)
        self.play(dot.animate.set_color(PURPLE).scale(1 / 1.26), run_time=2.05)
        for j, d in enumerate(groups[1]):
            bob(d, amp=.10, seed=j)
        self.at("separating tissue")
        world = tissue()
        self.play(FadeOut(candidate), FadeOut(state_label), FadeOut(stage), FadeOut(halos),
                  FadeOut(top_halo), FadeOut(bottom_halo), FadeOut(groups),
                  FadeIn(world), run_time=.85)
        outline, cells = world
        markers = VGroup(*(Circle(radius=.34, stroke_width=2.8, color=GREY).move_to(xy(*site))
                           for site in CELL_SITES))
        self.at("erases locations", lead=.4)
        self.play(FadeOut(outline), FadeIn(markers), *(sample.animate.scale(.67).shift(
            xy(.32 if i % 2 else -.26, .43 if i < 5 else -.45))
            for i, sample in enumerate(cells)), run_time=1.55)
        locations_lost = footer("Locations lost")
        self.play(FadeIn(locations_lost), run_time=.36)
        self.at("probably depletes")
        fragile = [sample for i, sample in enumerate(cells) if TISSUE_TYPES[i] in (1, 2)]
        breaking = (fragile[1], fragile[2], fragile[4])
        survivors = [sample for sample in cells if sample not in breaking]
        fragments = [
            VGroup(*(Line(sample.get_center() + xy(.32 * np.cos(a), .32 * np.sin(a)),
                          sample.get_center() + xy(.68 * np.cos(a), .68 * np.sin(a)),
                          color=RED, stroke_width=3)
                     for a in np.linspace(0, TAU, 6, endpoint=False)))
            for sample in breaking
        ]
        self.play(*(ReplacementTransform(a, b) for a, b in zip(breaking, fragments)),
                  swap(locations_lost, footer("Possible loss of fragile neurons", RED), .86),
                  run_time=1.3)
        self.play(*(FadeOut(f, scale=1.5) for f in fragments), run_time=.78)
        drift_rna(survivors)
        self.finish()


def location_map():
    world = tissue()
    grid = VGroup(*(Line(xy(x, -1.69), xy(x, 2.13), color="#728399",
                         stroke_width=1.5, stroke_opacity=.45) for x in (-5, -3, -1, 1, 3)),
                  *(Line(xy(-5.66, y), xy(3.58, y), color="#728399",
                         stroke_width=1.5, stroke_opacity=.45) for y in (-.75, .32, 1.37)))
    positions = VGroup(*(Circle(radius=.42, color=PATTERNS[kind], stroke_width=3.5)
                         .move_to(xy(*site)) for kind, site in zip(TISSUE_TYPES, CELL_SITES)))
    return world, grid, positions


def response_plot():
    plot = Plot((4.29, 6.27, -1.63, -.42), (0, 1), (0, 1), stroke=2)
    # Stylized evoked transient, in arbitrary units with no measured amplitude.
    def evoked(t):
        elapsed = max(0.0, t - .20)
        return .12 + 9.0 * elapsed * np.exp(-5.15 * elapsed)

    return plot, plot.curve(evoked, color=YELLOW, width=3.4)


class S09Controls(SpokenScene):
    def construct(self):
        stage, halos, groups = cluster_world()
        bad = VGroup(*(Star(n=7, outer_radius=.17, inner_radius=.104, color=RED,
                            stroke_width=1.8, fill_color=RED, fill_opacity=.5).move_to(xy(*p))
                       for p in ((-2.0, 1.76), (-2.2, -1.58), (2.12, 1.13), (1.48, -1.44))))
        self.add(stage, halos, groups, bad, schematic())
        cluster_motion(groups)
        self.at("experimenters guard")
        for d in bad:
            pulse(d, base=2, amp=1, speed=3.8)
        self.at("quality control", lead=.50)
        qc = heading("Quality control", GREEN)
        self.play(FadeIn(qc), run_time=.52)
        self.play(LaggedStart(*(FadeOut(d, shift=DOWN * .4) for d in bad), lag_ratio=.38),
                  run_time=2.15)
        world, grid, positions = location_map()
        self.at("spatial transcriptomics", lead=.55)
        self.play(FadeOut(qc), FadeOut(stage), FadeOut(halos), FadeIn(world),
                  FadeIn(grid), run_time=1.05)
        spot_dots = VGroup(*(Dot(xy(*site), radius=.21, color=PATTERNS[kind])
                             for kind, site in zip(TISSUE_TYPES, CELL_SITES)))
        for group in groups:
            for dot in group:
                dot.clear_updaters()
        self.play(LaggedStart(*(TransformFromCopy(groups[kind][i % 4], target) for i, (kind, target)
                                in enumerate(zip(TISSUE_TYPES, spot_dots))), lag_ratio=.12),
                  FadeOut(groups), run_time=2.75)
        self.remove(*spot_dots)
        spatial = heading("Spatial map", GREEN)
        self.play(FadeIn(positions), FadeIn(spatial), run_time=.55)
        drift_rna(world[1])
        self.at("candidate cluster")
        self.play(FadeOut(spatial), positions.animate.set_stroke(opacity=.33), run_time=.75)
        anchor_point = xy(*CELL_SITES[4])
        ring = Circle(radius=.67, stroke_width=5, color=YELLOW).move_to(anchor_point)
        self.at("when it recurs", lead=.45)
        self.play(Create(ring), run_time=.60)
        pulse(ring, base=5, amp=1.6)
        self.at("and location")
        leader = Line(anchor_point + RIGHT * .69, xy(4.33, 1.36), color=YELLOW, stroke_width=2.5)
        location = T("Location", 28).move_to(xy(5.37, 1.36))
        self.play(Create(leader), FadeIn(location), run_time=.58)
        self.at("shape", lead=.22)
        silhouette = cell(1, xy(5.4, .47), .36, rna=False)
        shape = T("Shape", 28).move_to(xy(5.42, -.12))
        shape_link = Line(xy(4.17, 1.36), xy(5.03, .50), color=YELLOW, stroke_width=2)
        self.play(Create(shape_link), FadeIn(silhouette), FadeIn(shape), run_time=.48)
        self.at("or response", lead=.27)
        axes, curve = response_plot()
        response_link = Line(xy(4.17, 1.36), xy(4.17, -.54), color=YELLOW, stroke_width=2)
        self.play(Create(response_link), Create(axes), Create(curve), run_time=.70)
        self.play(FadeIn(T("Response", 28).move_to(xy(5.28, -2.04))), run_time=.38)
        self.finish()


def olfactory_strip():
    strip = organic(((-6, 1.41), (-5.34, 2.42), (-2.83, 2.57), (0, 2.55),
                     (2.95, 2.51), (5.60, 2.44), (6.05, 1.48), (6.02, -.93),
                     (5.58, -1.99), (3.2, -2.10), (0, -2.19), (-3.7, -2.15),
                     (-5.57, -1.96), (-6.08, -.92)))
    positions = [xy(x, .28) for x in (-4.65, -2.80, -1.0, 1.0, 2.80, 4.65)]
    cells = VGroup(*(cell(1, p, .83, rna=False).stretch(2.48, 1, about_point=p)
                     for p in positions))
    return strip, cells, positions


def mature_fill(color):
    return interpolate_color(ManimColor("#233140"), ManimColor(color), .35)


def receptor_particles(center, mature_color=None):
    n = 15 if mature_color else 6
    dots = VGroup()
    for i in range(n):
        y = (i % 5 - 2) * .42
        x = .13 * np.sin(i * 2.39996) + (i // 5 - .8) * .16
        color = mature_color or PATTERNS[i % 3]
        point = center + xy(x, y)
        dots.add(VGroup(Dot(point, radius=.19, color=color, fill_opacity=.30 if mature_color else .21),
                        Dot(point, radius=.088, color=color, fill_opacity=1 if mature_color else .73)))
    return dots


class S10UnlockedOlfactory(SpokenScene):
    def construct(self):
        original, grid, positions = location_map()
        strip, cells, centers = olfactory_strip()
        self.add(original, grid, positions, schematic())
        self.at("reading single cells")
        self.play(ReplacementTransform(original[0], strip), FadeOut(grid), FadeOut(positions),
                  LaggedStart(*(FadeOut(c) for c in original[1]), lag_ratio=.07),
                  LaggedStart(*(FadeIn(c, shift=RIGHT * .30) for c in cells), lag_ratio=.11),
                  run_time=3.1)
        date = heading("Hanchate et al., 2015", GOLD)
        self.at("and colleagues sequenced", lead=.7)
        self.play(FadeIn(date), run_time=.6)
        lenses = VGroup(*(Ellipse(width=1.55, height=3.72, color=YELLOW, stroke_width=3)
                          .move_to(p) for p in centers[:2]))
        self.at("single mouse", lead=.42)
        self.play(LaggedStart(*(AnimationGroup(Create(l), c.edge.animate.set_fill("#574770"))
                                for l, c in zip(lenses, cells)), lag_ratio=.57), run_time=1.7)
        self.at("many immature neurons", lead=.45)
        self.play(FadeOut(lenses), run_time=.41)
        immature = VGroup(*(receptor_particles(p) for p in centers[:3]))
        self.play(LaggedStart(*(AnimationGroup(FadeIn(d, shift=UP * .28),
                                               c.edge.animate.set_fill("#554070"))
                                for d, c in zip(immature, cells)), lag_ratio=.43), run_time=2.24)
        for i, dots in enumerate(immature):
            for j, dot in enumerate(dots):
                bob(dot, amp=.10, seed=i + j)
        imm = T("Immature", 30).move_to(xy(-2.80, -2.53))
        self.play(FadeIn(imm), run_time=.45)
        self.at("most mature ones", lead=.45)
        mature = VGroup(*(receptor_particles(p, color) for p, color in zip(centers[3:], PATTERNS)))
        self.play(LaggedStart(*(AnimationGroup(FadeIn(d, shift=UP * .28),
                                               c.edge.animate.set_fill(mature_fill(color)))
                                for d, c, color in zip(mature, cells[3:], PATTERNS)),
                              lag_ratio=.56), run_time=2.1)
        for i, dots in enumerate(mature):
            for j, dot in enumerate(dots):
                bob(dot, amp=.10, seed=i + j)
        mat = T("Mature", 30).move_to(xy(2.8, -2.53))
        self.play(FadeIn(mat), run_time=.46)
        self.finish()


DOPAMINE_COLORS = (ORANGE, TEAL, PURPLE, "#639BE6", "#E4BD6B", "#D78DB2",
                   "#B0C879", "#D08871", "#7EBEB6", "#A6A6E6")
MIDBRAIN_SITES = ((-3.01, -.75), (-3.80, .33), (-2.71, 1.04), (-1.71, .37),
                  (-1.42, -1.06), (1.40, -1.04), (1.73, .40), (2.69, 1.04),
                  (3.8, .33), (3.1, -.73))


def midbrain():
    edge = organic(((-5.2, 1.22), (-3.9, 2.12), (-2.1, 2.48), (-.56, 1.95),
                    (0, 1.82), (.56, 1.95), (2.1, 2.48), (3.9, 2.12),
                    (5.2, 1.22), (5.05, -.62), (3.67, -1.81), (1.65, -2.02),
                    (0, -1.71), (-1.65, -2.02), (-3.67, -1.81), (-5.05, -.62)))
    shapes = VGroup(*(organic(((-4.38, -.15), (-3.76, .98), (-2.5, 1.16), (-1.14, .56),
                              (-.66, -.65), (-1.43, -1.40), (-2.86, -1.37), (-4.01, -.85)),
                             "#6A7C95", "#303E57", stroke=2) for _ in range(2)))
    shapes[1].flip(UP, about_point=ORIGIN)
    return VGroup(edge, shapes)


def population(color, point):
    base = Circle(radius=.43, stroke_width=2.7, color=color, fill_color=color, fill_opacity=.24)
    dots = VGroup(*(Dot(xy(x, y), radius=.067, color=color) for x, y in
                    ((.13, .10), (.18, -.12), (-.09, -.16), (-.17, .05), (-.05, .17))))
    return VGroup(base, dots).move_to(point)


def dopamine_populations():
    return VGroup(*(population(color, xy(*site)) for color, site in
                    zip(DOPAMINE_COLORS, MIDBRAIN_SITES)))


class S11UnlockedParkinson(SpokenScene):
    def construct(self):
        strip, cells, sites = olfactory_strip()
        for sample, color in zip(cells[3:], PATTERNS):
            sample.edge.set_fill(mature_fill(color))
        for sample in cells[:3]:
            sample.edge.set_fill("#554070")
        particles = VGroup(*(receptor_particles(p) for p in sites[:3]),
                           *(receptor_particles(p, color) for p, color in zip(sites[3:], PATTERNS)))
        previous_labels = VGroup(heading("Hanchate et al., 2015", GOLD),
                                 T("Immature", 30).move_to(xy(-2.8, -2.53)),
                                 T("Mature", 30).move_to(xy(2.8, -2.53)))
        section = midbrain()
        date = heading("Kamath et al., 2022", GOLD)
        self.add(strip, cells, particles, previous_labels, schematic())
        self.at("2022 kamath")
        self.play(ReplacementTransform(strip, section[0]), FadeOut(cells), FadeOut(particles),
                  FadeOut(previous_labels), FadeIn(section[1]), run_time=1.55)
        self.play(FadeIn(date), run_time=.55)
        nuclei = VGroup(*(Circle(radius=.30, color=BLUE, stroke_width=2.6, fill_color=BLUE,
                                 fill_opacity=.23).move_to(xy(*p)) for p in MIDBRAIN_SITES))
        self.at("single nuclei", lead=.34)
        self.play(LaggedStart(*(FadeIn(n, scale=.76) for n in nuclei), lag_ratio=.17), run_time=1.9)
        for i, n in enumerate(nuclei):
            bob(n, amp=.16, seed=i)
        label = footer("Human substantia nigra")
        self.at("human substantia", lead=.16)
        self.play(FadeIn(label), run_time=.59)
        self.at("a midbrain nucleus", lead=.42)
        slices = section[1]
        self.play(slices.animate.set_fill("#435978"), run_time=.72)
        self.play(slices.animate.set_fill("#303E57"), run_time=.72)
        self.at("they sorted dopamine", lead=.38)
        sorted_groups = dopamine_populations()
        for i, pop in enumerate(sorted_groups):
            pop.move_to(xy((i % 5 - 2) * 1.56, .78 - (i // 5) * 1.78))
        for n in nuclei:
            n.clear_updaters()
        self.play(section[0].animate.set_opacity(.55), section[1].animate.set_opacity(.27),
                  LaggedStart(*(ReplacementTransform(n, pop) for n, pop in zip(nuclei, sorted_groups)),
                              lag_ratio=.13), run_time=1.96)
        ten = footer("10 dopamine populations")
        self.play(swap(label, ten), run_time=.6)
        self.at("and mapped them", lead=.44)
        self.play(section[0].animate.set_fill(opacity=1).set_stroke(opacity=1),
                  section[1].animate.set_fill(opacity=1).set_stroke(opacity=1),
                  LaggedStart(*(p.animate.move_to(xy(*pos)) for p, pos
                                in zip(sorted_groups, MIDBRAIN_SITES)), lag_ratio=.10),
                  run_time=2.0)
        mapped = footer("Macaque midbrain · Slide-seq")
        self.play(swap(ten, mapped), run_time=.56)
        self.at("one marked by")
        marker = Circle(radius=.58, color=YELLOW, stroke_width=3.8).move_to(sorted_groups[0])
        agtr = T("AGTR1", 29, YELLOW).move_to(xy(-5.57, -2.17))
        pointer = Line(xy(-4.80, -1.95), xy(-3.52, -1.10), color=YELLOW, stroke_width=2.1)
        self.play(Create(marker), Create(pointer), FadeIn(agtr), run_time=.86)
        for i, pop in enumerate(sorted_groups[1:]):
            for j, dot in enumerate(pop[1]):
                bob(dot, amp=.075, seed=i + j)
        self.at("highly susceptible")
        loss = footer("Vulnerable in Parkinson disease", RED)
        self.play(sorted_groups[0].animate.set_opacity(.16), marker.animate.set_stroke(RED),
                  swap(mapped, loss, 1.2), run_time=2.0)
        pulse(marker, base=4, amp=1.65, speed=3)
        self.finish()


def whole_brain():
    edge = organic(((-5.98, -.70), (-5.45, .51), (-4.55, 1.66), (-2.73, 2.43), (-.8, 2.57),
                    (.83, 2.34), (2.03, 1.86), (2.99, 1.15), (3.66, .72), (3.67, -.31),
                    (3.20, -1.27), (2.12, -1.64), (1.30, -2.1), (-.35, -2.07),
                    (-1.37, -1.56), (-3.04, -1.60), (-4.38, -1.51), (-5.33, -1.23)))
    regions = VGroup(
        organic(((-4.92, -.64), (-4.14, .53), (-2.74, 1.71), (-.61, 2.02),
                 (.79, 1.78), (1.54, 1.36), (.2, 1.38), (-1.05, .97),
                 (-2.64, .14), (-3.36, -.8)), "#54697F", "#30465A", 2),
        organic(((-3.16, -.79), (-2.13, .14), (-.52, .76), (.58, .65), (.95, .1),
                 (.51, -.65), (-.55, -1.02), (-1.74, -.97)), "#596B82", "#35455E", 2),
        organic(((1.49, .11), (2.45, .76), (3.23, .45), (3.25, -.43),
                 (2.62, -.94), (1.63, -.84)), "#637088", "#3B465C", 2),
        organic(((-.82, -1.46), (.09, -1.12), (1.33, -.95), (2.23, -1.07),
                 (1.42, -1.70), (.52, -1.82)), "#596B82", "#34435A", 2),
    )
    return VGroup(edge, regions)


def atlas_dots():
    rng = np.random.default_rng(36)
    zones = ((-3.66, -.19, .71, .50), (-2.23, 1.10, .66, .40),
             (-.15, 1.65, .75, .32), (-1.2, -.27, .80, .45),
             (.54, -.38, .59, .42), (2.42, .03, .59, .46), (.63, -1.50, .60, .20))
    spots = []
    for i, (x, y, w, h) in enumerate(zones):
        for _ in range(21):
            angle, radius = rng.uniform(0, TAU), np.sqrt(rng.uniform())
            point = xy(x + w * radius * np.cos(angle), y + h * radius * np.sin(angle))
            spots.append(Dot(point, radius=rng.uniform(.050, .088), color=DOPAMINE_COLORS[i],
                             fill_opacity=rng.uniform(.55, .96)))
    return VGroup(*sorted(spots, key=lambda point: point.get_x()))


def atlas_label(text):
    return T(text, 28).move_to(xy(5.24, -.31))


class S12UnlockedAtlas(SpokenScene):
    def construct(self):
        section, brain = midbrain(), whole_brain()
        date = heading("Yao, Zeng et al., 2023", GOLD)
        populations = dopamine_populations()
        populations[0].set_opacity(.16)
        self.add(section, populations, schematic())
        self.at("in 2023")
        self.play(ReplacementTransform(section[0], brain[0]), FadeOut(section[1]),
                  FadeOut(populations), FadeIn(brain[1]), run_time=2.12)
        self.play(FadeIn(date), run_time=.65)
        dots = atlas_dots().set_z_index(2)
        self.at("profiled around")
        total = ValueTracker(7_000_000)
        number = counter("{:,.0f}", total, at=xy(5.24, .49), size=36, color=YELLOW)
        profiled = atlas_label("Profiled\n(approx.)")
        neutral = dots.copy().set_color(BLUE).set_opacity(.64)
        number.suspend_updating()
        self.add(number)
        self.play(LaggedStart(*(FadeIn(neutral[i:i + 24]) for i in range(0, len(neutral), 24)),
                              lag_ratio=.15), FadeIn(profiled), run_time=2.47)
        regions = brain[1]
        region_colors = [region.get_fill_color() for region in regions]
        self.play(LaggedStart(*(region.animate.set_fill(interpolate_color(color, ManimColor(BLUE), .35))
                                for region, color in zip(regions, region_colors)), lag_ratio=.12),
                  run_time=1.57)
        self.at("roughly 4")
        self.play(FadeOut(profiled), run_time=.27)
        total.set_value(4_000_000)
        number.resume_updating().suspend_updating()
        passed = atlas_label("Passed QC\n(approx.)")
        retained = VGroup(*(d for i, d in enumerate(neutral) if i % 7 < 4))
        excluded = VGroup(*(d for i, d in enumerate(neutral) if i % 7 >= 4))
        self.add(retained, excluded)
        self.play(FadeOut(excluded), FadeIn(passed),
                  *(region.animate.set_fill(color) for region, color in zip(regions, region_colors)),
                  run_time=1.32)
        self.at("and formed")
        self.play(FadeOut(passed), run_time=.30)
        total.set_value(5_322)
        number.resume_updating().suspend_updating()
        atlas = atlas_label("Clusters")
        representatives = VGroup(*(Dot(xy(x, y), radius=.15, color=DOPAMINE_COLORS[i])
                                    for i, (x, y) in enumerate(((-3.66, -.19), (-2.23, 1.10),
                                        (-.15, 1.65), (-1.2, -.27), (.54, -.38), (2.42, .03),
                                        (.63, -1.50)))))
        self.play(FadeOut(retained), LaggedStart(*(FadeIn(d, scale=.45) for d in representatives),
                                               lag_ratio=.16), FadeIn(atlas), run_time=1.62)
        for i, dot in enumerate(representatives):
            pulse(dot, base=3.2, amp=1.3, speed=2.)
        self.at("murfish in about")
        map_label = T("MERFISH", 28, TEAL).move_to(xy(5.24, 1.15))
        self.play(FadeOut(representatives), FadeOut(atlas), FadeOut(number), run_time=.56)
        total.set_value(4_300_000)
        number.resume_updating().suspend_updating()
        self.play(FadeIn(number), FadeIn(map_label),
                  FadeIn(atlas_label("Mapped cells\n(approx.)")), run_time=.56)
        scan = Line(xy(-5.6, -.9), xy(-5.6, .37), color=TEAL, stroke_width=4)
        self.play(FadeIn(scan), run_time=.35)
        self.play(scan.animate.put_start_and_end_on(xy(3.36, -.66), xy(3.36, .74)),
                  LaggedStart(*(FadeIn(dots[i:i + 14]) for i in range(0, len(dots), 14)),
                              lag_ratio=.16), run_time=3.66, rate_func=linear)
        self.play(FadeOut(scan), run_time=.34)
        self.play(LaggedStart(*(region.animate.set_fill(interpolate_color(color, ManimColor(TEAL), .32))
                                for region, color in zip(regions, region_colors)), lag_ratio=.17),
                  run_time=1.25)
        self.at("still not every", lead=.23)
        caution = footer("Not every cluster may be a true type", GOLD)
        self.play(FadeIn(caution), run_time=.6)
        for i, dot in enumerate(dots[::3]):
            bob(dot, amp=.07, seed=i)
        self.finish()


class S13End(EndCard):
    LINE = "Sort cells by RNA; anchor candidate types with location and function."
