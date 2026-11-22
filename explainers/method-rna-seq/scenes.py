"""Single-cell RNA sequencing, from tissue to counts and their interpretation."""
from bp_parts import *  # noqa: F403
from bp_style import EndCard

config.background_color = BG

# COLOR MAP
# GREY: cell structure and inactive genome bands. BLUE: sequencing apparatus.
# YELLOW: RNA. PURPLE: DNA copies. TEAL / ORANGE: cell of origin.
# GREEN: surviving neurons and fate evidence. RED: loss. GOLD: the predict question.
PURPLE = "#B58CD9"
ORANGE = "#F29E4C"
CELL_COLORS = (TEAL, ORANGE)
CELL_NAMES = ("Keratinocyte", "Macrophage")
PACKED_X = (-2.52, 2.52)
ISOLATED_X = (-3.28, 3.28)
GENOME_BANDS = (-1.44, -0.96, -0.48, 0, 0.48, 0.96, 1.44)
ACTIVE_BANDS = ((0, 2, 5), (1, 3, 6))
PROFILES = (
    (4, 1, 3, 0), (3, 0, 4, 1), (4, 1, 4, 0),
    (1, 4, 0, 3), (0, 3, 1, 4), (1, 4, 0, 4),
)
QUESTION = "What misleads this RNA comparison?"
QUESTION_STYLE = dict(y=3.15, size=41, max_w=10.8)


def pt(x, y):
    return np.array([x, y, 0.0])


def label(text, x, y, size=32, color=TEXT):
    return T(text, size, color).move_to(pt(x, y))


def schematic():
    return scope_tag(size=28, color=TEXT)


def capsule(w, h, color, fill=0.25, stroke=2.5):
    return RoundedRectangle(width=w, height=h, corner_radius=min(h * 0.46, 0.28),
                            stroke_color=color, stroke_width=stroke,
                            fill_color=color, fill_opacity=fill)


def membrane(w, h, color, form=0, fill=0.30):
    """A cell silhouette. Form 0 is flattened, 1 amoeboid, 2 a rounded cell."""
    t = np.linspace(0, TAU, 33)[:-1]
    if form == 0:
        x, y = np.cos(t), np.sin(t)
        x, y = np.sign(x) * abs(x) ** 0.64, np.sign(y) * abs(y) ** 0.79
    elif form == 1:
        r = 1 + 0.13 * np.cos(5 * t + 0.4) + 0.07 * np.sin(3 * t)
        x, y = r * np.cos(t), r * np.sin(t)
    else:
        r = 1 + 0.045 * np.sin(3 * t + 0.4)
        x, y = r * np.cos(t), r * np.sin(t)
    points = [pt(a, b) for a, b in zip(x, y)]
    cell = VMobject(stroke_color=color, stroke_width=3.2, fill_color=color, fill_opacity=fill)
    cell.set_points_smoothly([*points, points[0]])
    return cell.stretch_to_fit_width(w).stretch_to_fit_height(h).center()


def genome(active=()):
    base = capsule(3.44, 0.34, GREY, 0.32)
    bands = VGroup(*[
        capsule(0.30, 0.23, YELLOW if i in active else GREY, 0.92, 0)
        .move_to(pt(x, 0))
        for i, x in enumerate(GENOME_BANDS)
    ])
    return VGroup(base, bands)


def ribbon(w=0.87):
    """A flat strip for an RNA copy, with no molecular detail."""
    strip = capsule(w, 0.17, YELLOW, 0.98, 0)
    glow = capsule(w + 0.16, 0.30, YELLOW, 0.19, 0)
    return VGroup(glow, strip)


def barcode_tag(strip, color, h=0.19):
    tag = capsule(h * 1.4, h * 1.22, color, 1, 0)
    return tag.move_to(strip.get_right() + LEFT * h * 0.36)


def dna_strip(color=None, w=0.91, h=0.19):
    strip = capsule(w, h, PURPLE, 0.91, 0)
    return strip if color is None else VGroup(strip, barcode_tag(strip, color, h))


def packed_tissue():
    cells = VGroup()
    for x in (-5.56, -2.78, 0, 2.78, 5.56):
        for y in (-2.33, 2.03):
            cell = membrane(2.58, 1.04, BLUE, 0, 0.33).move_to(pt(x, y))
            cell.set_stroke(BLUE, 1.6, opacity=0.65)
            nucleus = Ellipse(width=0.90, height=0.42, stroke_width=1.3,
                              color=BLUE, fill_opacity=0.44).move_to(cell)
            cells.add(VGroup(cell, nucleus))
    for x in (-6.02, 6.03):
        cells.add(membrane(1.24, 2.92, BLUE, 1, 0.31).move_to(pt(x, -0.2)))
    return cells


def tissue_cells(xs=PACKED_X, active=True, copies="rna"):
    cells = VGroup()
    for i, (x, color) in enumerate(zip(xs, CELL_COLORS)):
        packed_height = 2.65 if i == 0 else 3.30
        height = packed_height if xs == PACKED_X else packed_height + 1.00
        body = membrane(4.95 if i == 0 else 4.65, height, color, i).move_to(pt(x, -0.16))
        genome_x = x - 0.40 * i
        genes = genome(ACTIVE_BANDS[i] if active else ()).move_to(pt(genome_x, -0.48 + 0.10 * i))
        strands = VGroup()
        for j, k in enumerate(ACTIVE_BANDS[i]):
            strip = ribbon() if copies == "rna" else dna_strip(color if copies == "tagged" else None)
            strip.move_to(pt(genome_x + GENOME_BANDS[k], 0.15 + (0.31 if j == 1 else 0)))
            strands.add(strip)
        cells.add(VGroup(body, genes, strands))
    return cells


def drift_strands(cells, phase=0):
    for i, (_, _, strands) in enumerate(cells):
        for j, strand in enumerate(strands):
            bob(strand, amp=0.20, speed=1.25, seed=phase + i + 2 * j)


def breathe(mob, base, amplitude=0.09, speed=1.45, phase=0):
    """Shift the fill gently while leaving the cell outline and landmarks fixed."""
    t = phase

    def update(shape, dt):
        nonlocal t
        t += dt
        shape.set_fill(opacity=base + amplitude * np.sin(speed * t))

    return mob.add_updater(update)


def freeze_strands(cells):
    for _, _, strands in cells:
        for strand in strands:
            strand.clear_updaters()


def cell_names(y=-3.19):
    return VGroup(*[label(name, x, y, color=color)
                    for name, x, color in zip(CELL_NAMES, (-3.05, 3.05), CELL_COLORS)])


class S01Hook(SpokenScene):
    def construct(self):
        bed = packed_tissue()
        cells = tissue_cells(active=False)
        self.add(bed, *(VGroup(body, genes) for body, genes, _ in cells), schematic())

        self.at("which genes are active", lead=0.75)
        active = tissue_cells()
        self.play(*[Transform(cell[1], target[1]) for cell, target in zip(cells, active)],
                  run_time=0.55)
        self.play(LaggedStart(*[
            FadeIn(strip, shift=UP * 0.42) for cell in cells for strip in cell[2]
        ], lag_ratio=0.18), run_time=1.35)
        drift_strands(cells)
        names = cell_names()
        self.at("a keratinocyte")
        self.play(FadeIn(names[0]), run_time=0.4)
        self.at("a macrophage")
        self.play(FadeIn(names[1]), run_time=0.4)

        self.at("transcription copies", lead=0.55)
        new_copies = tissue_cells()[0][2]
        for i, strip in enumerate(new_copies):
            strip.shift(UP * (0.34 + 0.04 * i))
        self.play(LaggedStart(*[FadeIn(strip, shift=UP * 0.34) for strip in new_copies],
                              lag_ratio=0.33), run_time=2.25)
        self.play(FadeOut(new_copies), run_time=0.50)

        self.at("transcription factors", lead=0.50)
        regulators = VGroup()
        for i, x in enumerate(PACKED_X):
            regulators.add(capsule(0.70, 0.23, GREEN, 0.86, 0)
                           .move_to(pt(x + (-0.84 if i == 0 else 0.35), -1.03)))
            regulators.add(capsule(0.83, 0.23, GREY, 0.92, 0)
                           .move_to(pt(x + (0.64 if i == 0 else -0.64), -1.03)))
        key = VGroup(*[
            VGroup(capsule(0.55, 0.22, color, 0.92, 0), T(name, 30, TEXT))
            .arrange(RIGHT, buff=0.17)
            for name, color in (("Transcription factors", GREEN), ("Chromatin", GREY))
        ]).arrange(RIGHT, buff=0.60).move_to(pt(0, -3.19))
        self.play(FadeIn(regulators, shift=UP * 0.16), FadeOut(names), run_time=0.62)
        self.play(FadeIn(key), run_time=0.5)

        self.at("Single", lead=0.2)
        self.play(FadeOut(key), FadeOut(regulators), run_time=0.4)
        self.finish()


class S02Title(TitleCard):
    LESSON = "Single-cell RNA sequencing"
    TITLE = "Counting Which Genes a Cell Uses"

    def construct(self):
        cells = tissue_cells()
        self.add(packed_tissue(), cells, schematic())
        drift_strands(cells)
        shade = RoundedRectangle(width=11.9, height=0.93, corner_radius=0.23,
                                 stroke_width=0, fill_color=BG, fill_opacity=1).move_to(pt(0, 3.12))
        shade.set_z_index(2)
        title = fit_text(self.TITLE, max_w=11.1, size=52, min_size=45, font=TITLE_FONT)
        title.move_to(shade).set_z_index(3)
        self.play(FadeIn(shade), run_time=0.2)
        self.play(FadeIn(title, shift=UP * 0.08), run_time=0.27)
        self.wait(0.83)
        self.play(FadeOut(title), run_time=0.2)
        self.play(FadeOut(shade), run_time=0.27)
        self.wait(max(1 / config.frame_rate, self.narration_s - self.elapsed()))


class S03Barcode(SpokenScene):
    def construct(self):
        bed, cells = packed_tissue(), tissue_cells()
        self.add(bed, cells, schematic())
        drift_strands(cells)
        self.at("the tissue is")
        enzyme_waves = VGroup(*[
            Arc(angle=PI * 0.7, radius=1.24, start_angle=-PI * 0.35,
                color=GREEN, stroke_width=5).move_to(pt(x, -0.15))
            for x in (-4.8, 0, 4.2)
        ])
        self.play(FadeIn(enzyme_waves), run_time=0.4)
        freeze_strands(cells)
        self.play(FadeOut(bed), enzyme_waves.animate.shift(RIGHT * 0.36),
                  *[Transform(c, target) for c, target in zip(cells, tissue_cells(ISOLATED_X))],
                  run_time=2.05)
        names = cell_names()
        enzyme_label = label("Enzymes", 0, 2.1, 31, GREEN)
        self.at("usually with enzymes", lead=0.45)
        self.play(FadeIn(enzyme_label), FadeIn(names), run_time=0.5)
        drift_strands(cells)

        self.at("each captured RNA", lead=0.55)
        self.play(FadeOut(enzyme_label), FadeOut(enzyme_waves), run_time=0.34)
        freeze_strands(cells)
        dna = tissue_cells(ISOLATED_X, copies="dna")
        copies = [strip for cell in cells for strip in cell[2]]
        targets = [strip for cell in dna for strip in cell[2]]
        self.play(LaggedStart(*[Transform(a, b) for a, b in zip(copies, targets)],
                              lag_ratio=0.36), run_time=3.45)
        drift_strands(cells)

        self.at("before cells are mixed", lead=0.1)
        freeze_strands(cells)
        for i, (body, _, _) in enumerate(cells):
            breathe(body, base=0.30, phase=i * 0.8)
        tagged = VGroup()
        tags = VGroup()
        for color, (body, genes, strands) in zip(CELL_COLORS, cells):
            pairs = VGroup()
            for strip in strands:
                tag = barcode_tag(strip, color)
                tags.add(tag)
                pairs.add(VGroup(strip, tag))
            tagged.add(VGroup(body, genes, pairs))
        self.play(LaggedStart(*[
            FadeIn(tag) for tag in tags
        ], lag_ratio=0.48), run_time=3.35)
        self.remove(cells, *copies, *tags)
        self.add(tagged)
        drift_strands(tagged)
        tag_title = label("Cell barcode (schematic)", 0, 2.67, 37)
        self.at("that barcode is", lead=1.05)
        self.play(FadeIn(tag_title), run_time=0.6)
        self.finish()


def sequencer(x=0, y=0):
    body = capsule(4.46, 4.17, BLUE, 0.38, 3).move_to(pt(x, y))
    slot = capsule(3.70, 1.12, BLUE, 0.18).move_to(pt(x, y))
    beam = capsule(0.12, 3.29, BLUE, 0.90, 0).move_to(pt(x, y))
    return VGroup(body, slot, beam)


def count_tile(value, color, x, y, w, h):
    box = RoundedRectangle(width=w, height=h, corner_radius=0.12, stroke_color=color,
                           stroke_width=1.4, fill_color=color, fill_opacity=0.22).move_to(pt(x, y))
    count = max(value, 0.07)
    mark = capsule(w * (0.15 * count + 0.08), h * 0.44, color, 0.95 if value else 0.28, 0)
    mark.move_to(pt(x - w * 0.35 + mark.width / 2, y))
    return VGroup(box, mark)


def count_matrix():
    """Each of the six sampled cells occupies one fixed column in both scenes."""
    xs = np.linspace(-2.97, 5.36, len(PROFILES))
    ys = (1.00, -0.02, -1.04, -2.06)
    columns = VGroup()
    for j, x in enumerate(xs):
        c = CELL_COLORS[j // 3]
        columns.add(VGroup(*[count_tile(v, c, x, y, 1.49, 0.91)
                             for v, y in zip(PROFILES[j], ys)]))
    rows = VGroup(*[label(f"Gene {g}", -5.6, y, 32) for g, y in zip("ABCD", ys)])
    heads = VGroup(*[label(f"Cell {i + 1}", x, 1.82, 28, CELL_COLORS[i // 3]) for i, x in enumerate(xs)])
    title = label("Count matrix (schematic)", 0, 2.87, 40)
    return columns, rows, heads, title


class S04Matrix(SpokenScene):
    def construct(self):
        cells = tissue_cells(ISOLATED_X, copies="tagged")
        tag_title = label("Cell barcode (schematic)", 0, 2.67, 37)
        names = cell_names()
        self.add(cells, tag_title, names, schematic())
        self.at("the pooled DNA", lead=0.6)
        pooled = VGroup(*[strip.copy() for cell in cells for strip in cell[2]])
        self.remove(*(cell[2] for cell in cells))
        self.add(pooled)
        gate = sequencer()
        self.play(FadeOut(cells), FadeOut(names), FadeOut(tag_title), FadeIn(gate), run_time=0.62)
        mixed_positions = ((-1.05, 0.31), (0, -0.31), (1.05, 0.31),
                           (-1.05, -0.31), (0, 0.31), (1.05, -0.31))
        self.play(LaggedStart(*[s.animate.move_to(pt(*xy)) for s, xy in zip(pooled, mixed_positions)],
                              lag_ratio=0.14), run_time=2.55)
        self.at("cell barcodes sort", lead=0.28)
        columns, rows, heads, title = count_matrix()
        destinations = [pt(x, y) for x, y in
                        ((-4.65, 0.85), (-3.45, 0.05), (-2.25, -0.72),
                         (2.25, -0.72), (3.45, 0.05), (4.65, 0.85))]
        self.play(LaggedStart(*[s.animate.move_to(target) for s, target in zip(pooled, destinations)],
                              lag_ratio=0.13), run_time=2.6)

        self.at("counts fill", lead=1.02)
        # Each barcode's reads feed a single column. The other sampled cells
        # populate their own columns without going through this two-cell close-up.
        sources = [pooled[:3], pooled[3:]]
        self.remove(pooled)
        self.add(*sources)
        self.play(FadeOut(gate), ReplacementTransform(sources[0], columns[0]),
                  ReplacementTransform(sources[1], columns[3]), run_time=1.12)
        self.play(FadeIn(title), run_time=0.40)
        self.play(LaggedStart(*[FadeIn(columns[i], shift=UP * 0.16) for i in (1, 2, 4, 5)],
                              lag_ratio=0.18), run_time=0.55)
        self.at("row per gene")
        self.play(LaggedStart(*[FadeIn(r, shift=RIGHT * 0.17) for r in rows],
                              lag_ratio=0.16), run_time=0.82)
        self.at("column per sampled cell")
        self.play(LaggedStart(*[FadeIn(h, shift=DOWN * 0.15) for h in heads],
                              lag_ratio=0.14), run_time=1.08)
        entry = SurroundingRectangle(columns[0][0], buff=0.05, color=YELLOW,
                                     corner_radius=0.14, stroke_width=4, fill_opacity=0.22)
        self.at("each entry counts")
        self.play(Create(entry), run_time=0.57)
        read_label = caption("Reads", size=31)
        self.play(FadeIn(read_label), run_time=0.45)
        self.at("or molecules")
        molecule_label = caption("Molecules with unique tags", size=31)
        self.play(swap(read_label, molecule_label, run_time=0.65))
        self.play(entry.animate.move_to(columns[2][2]), run_time=1.7)
        self.at("sequencing RNA counts", lead=0.9)
        self.play(FadeOut(molecule_label), run_time=0.4)
        column_focus = SurroundingRectangle(columns[4], buff=0.05, color=YELLOW,
                                            corner_radius=0.14, stroke_width=4, fill_opacity=0.16)
        self.play(Transform(entry, column_focus), run_time=2.15)
        self.at("each cell uses", lead=0)
        self.play(FadeOut(entry), run_time=1.02)
        self.finish()


def scatter_panel():
    panel = RoundedRectangle(width=12.24, height=4.8, corner_radius=0.25,
                             color=BLUE, stroke_width=2.7, fill_opacity=0.32)
    return panel.move_to(pt(0, -0.05))


def cluster_dots():
    seeds = ((-4.8, 0.90), (-1.16, 0.77), (-4.4, -1.15),
             (4.95, 1.09), (1.40, -1.34), (4.58, -0.69))
    return VGroup(*[Dot(pt(x, y), radius=0.20, color=CELL_COLORS[i // 3])
                    for i, (x, y) in enumerate(seeds)])


def cluster_marks():
    return VGroup(*[
        Ellipse(width=3.86, height=2.98, stroke_color=color, stroke_width=3.4,
                fill_color=color, fill_opacity=0.19).move_to(pt(x, 0.40))
        for x, color in zip((-3.28, 3.28), CELL_COLORS)
    ])


class S05Cluster(SpokenScene):
    def construct(self):
        columns, rows, heads, title = count_matrix()
        self.add(columns, rows, heads, title, schematic())
        self.at("across many cells", lead=0.65)
        panel, dots = scatter_panel(), cluster_dots()
        self.play(FadeOut(rows), FadeOut(heads), FadeOut(title, shift=UP * 0.18), run_time=0.36)
        self.play(FadeIn(panel), run_time=0.42)
        self.bring_to_back(panel)
        self.play(LaggedStart(*[ReplacementTransform(col, dot) for col, dot in zip(columns, dots)],
                              lag_ratio=0.20), run_time=2.05)

        self.at("similar expression profiles", lead=0.45)
        final = ((-4, 0.15), (-3.19, 1.03), (-2.65, 0.08), (2.59, 0.17), (3.24, 1.02), (4.08, 0.04))
        self.play(*[dot.animate.move_to(pt(*loc)) for dot, loc in zip(dots, final)], run_time=2.05)
        marks = cluster_marks()
        self.play(LaggedStart(*[Create(m) for m in marks], lag_ratio=0.25), run_time=0.78)
        self.bring_to_back(marks)
        self.bring_to_back(panel)
        self.at("each group is a cluster", lead=0.15)
        cluster_title = label("Cluster (schematic)", 0, 2.96, 38)
        self.play(FadeIn(cluster_title), run_time=0.64)

        self.at("with known profiles", lead=0.55)
        refs = VGroup(*[VGroup(*[
            count_tile(value, CELL_COLORS[i], x + (j - 1.5) * 0.59, -1.72, 0.52, 0.48)
            for j, value in enumerate(PROFILES[i * 3])
        ]) for i, x in enumerate((-3.28, 3.28))])
        self.play(LaggedStart(*[FadeIn(r, shift=UP * 0.42) for r in refs],
                              lag_ratio=0.24), run_time=1.17)
        names = VGroup(*[label(name + "?", x, -3.08, 32, color)
                         for name, x, color in zip(CELL_NAMES, (-3.16, 3.02), CELL_COLORS)])
        self.at("propose an identity", lead=0.35)
        self.play(FadeIn(names), run_time=0.6)
        self.at("is annotation")
        self.play(swap(cluster_title, label("Annotation", 0, 2.96, 38), run_time=0.7))
        for i, d in enumerate(dots):
            bob(d, amp=0.15, speed=1.6, seed=i)
        self.at("notice the word propose")
        outline = VGroup(*[SurroundingRectangle(n, buff=0.16, color=c, corner_radius=0.13)
                           for n, c in zip(names, CELL_COLORS)])
        self.play(Create(outline), run_time=0.72)
        self.at("counts can still mislead")
        self.play(FadeOut(outline), run_time=0.65)
        self.finish()


GANGLION_X = (-3.33, 3.33)
GANGLION_Y = 0.25
NEURON_PLACES = ((-1.16, 0.53), (0, 0.77), (1.16, 0.53), (-0.61, -0.60), (0.64, -0.63))
GANGLION_COUNTS = ((4, 4, 3, 4), (2, 2, 1, 2))


def neuron(x, y):
    limbs = VGroup()
    for a in (0.22, 1.51, 2.67, 3.86, 5.12):
        r = np.array([np.cos(a), np.sin(a), 0])
        n = np.array([-r[1], r[0], 0])
        l = VMobject(stroke_color=GREEN, stroke_width=3.8)
        home = pt(x, y)
        l.set_points_smoothly([home + 0.23 * r, home + 0.39 * r + 0.07 * n,
                               home + 0.54 * r, home + 0.62 * r - 0.07 * n])
        limbs.add(l)
    soma = membrane(0.64, 0.58, GREEN, 2, 0.77).move_to(pt(x, y))
    nucleus = Dot(pt(x, y), radius=0.108, color=GREEN)
    return VGroup(limbs, soma, nucleus)


def ganglia(panel_bottom=-2.68):
    panels = TwoPanel("Ganglion + NGF", "Ganglion, no NGF", colors=(BLUE, BLUE),
                      top=2.55, bottom=panel_bottom, size=34, width=12.9)
    for frame in (panels.left_frame, panels.right_frame):
        frame.set_fill(BLUE, 0.21)
    bodies = VGroup()
    living = VGroup()
    for x in GANGLION_X:
        bodies.add(membrane(4.06, 2.74, GREY, 1, 0.24).move_to(pt(x - 0.38, GANGLION_Y)))
        living.add(VGroup(*[neuron(x - 0.38 + dx, GANGLION_Y + dy) for dx, dy in NEURON_PLACES]))
    return panels, bodies, living


def condition_counts(values, color, x):
    return VGroup(*[count_tile(value, color, x + 2.30, 0.16 - 0.73 * (i - 1.5), 0.94, 0.60)
                    for i, value in enumerate(values)])


def ngf_signals(x):
    return VGroup(*[Dot(pt(x + dx, y), radius=0.075, color=GOLD)
                    for dx, y in ((-1.40, -0.07), (-1.44, 1.04), (-0.36, 1.42),
                                  (0.44, -0.22), (1.43, 1.10), (1.42, -0.27))])


def animate_neurons(neurons):
    for i, cell in enumerate(neurons):
        bob(cell, amp=0.13, speed=1.35, seed=1.4 * i)


def prediction_world():
    panels, bodies, live = ganglia()
    for limbs, soma, nucleus in live[1]:
        limbs.set_stroke(opacity=0.11).set_fill(opacity=0)
        soma.set_opacity(0.11)
        nucleus.set_opacity(0.11)
    counts = VGroup(condition_counts(GANGLION_COUNTS[0], GREEN, GANGLION_X[0]),
                    condition_counts(GANGLION_COUNTS[0], BLUE, GANGLION_X[1]))
    return panels, bodies, live, counts


class S06PredictQ(SpokenScene):
    def construct(self):
        panels, bodies, live = ganglia()
        self.add(panels.left_frame, panels.right_frame, bodies, schematic())
        self.at("want the genes")
        self.play(LaggedStart(*[FadeIn(g, scale=0.86) for g in live], lag_ratio=0.28),
                  run_time=0.89)
        signals = VGroup(*[ngf_signals(x) for x in GANGLION_X])
        self.at("nerve growth factor", lead=0.15)
        self.play(FadeIn(signals), run_time=0.5)
        for group in live:
            animate_neurons(group)
        for j, signal_group in enumerate(signals):
            for i, signal in enumerate(signal_group):
                bob(signal, amp=0.19, speed=1.52, seed=j + i * 1.3)
        self.at("groups called ganglia", lead=0.4)
        self.play(FadeIn(panels.left_head), run_time=0.7)
        counts = VGroup(*[condition_counts(GANGLION_COUNTS[0], GREEN, x) for x in GANGLION_X])
        self.play(FadeIn(counts, shift=UP * 0.19), run_time=1.3)

        self.at("without NGF", lead=0.55)
        for signal in signals[1]:
            signal.clear_updaters()
        self.play(FadeOut(signals[1], shift=UP * 0.68), FadeIn(panels.right_head), run_time=0.8)
        for neuron_cell in live[1]:
            neuron_cell.clear_updaters()
        target = prediction_world()
        self.at("the neurons die", lead=0.1)
        self.play(Transform(live[1], target[2][1]), Transform(counts[1], target[3][1]),
                  run_time=1.74)
        self.at("if you compare RNA", lead=0.2)
        self.play(FadeOut(signals[0]), run_time=0.55)
        self.at("what misleads your counts", lead=0.9)
        self.play(FadeIn(question_card(QUESTION, **QUESTION_STYLE)), run_time=0.6)
        self.at("your counts", lead=0)
        for n in live[0]:
            n.clear_updaters()
        self.play(*[n.animate.move_to(pose) for n, pose in zip(live[0], target[2][0])], run_time=0.75)
        self.finish()


class S07PredictPause(Scene):
    def construct(self):
        panels, bodies, live, counts = prediction_world()
        self.add(panels, bodies, live, counts, question_card(QUESTION, **QUESTION_STYLE), schematic())
        for column in counts:
            for box, _ in column:
                breathe(box, base=0.22, amplitude=0.09, speed=TAU / 4.5)
        self.wait(4.5)


def snapshot_cell():
    """The same cell and frame close the limit scene and open the lineage scene."""
    cell = membrane(4.0, 3.96, BLUE, 2, 0.52).move_to(pt(-2.77, -0.04))
    frame = SurroundingRectangle(cell, color=BLUE, buff=0.28, corner_radius=0.15, stroke_width=3.4)
    strips = VGroup(*[ribbon(w).move_to(pt(-2.77 + dx, y))
                      for y, dx, w in ((0.86, -0.33, 1.45), (0.34, 0.20, 1.68),
                                       (-0.19, -0.14, 1.28), (-0.71, 0.22, 1.59))])
    return cell, frame, strips


def fate_paths():
    return VGroup(*[
        Arrow(pt(-0.14, 0.05), pt(3.43, y), buff=0, color=GREY, stroke_width=4,
              max_tip_length_to_length_ratio=0.11)
        for y in (-1.46, 1.46)
    ])


class S08Controls(SpokenScene):
    def construct(self):
        panels, bodies, live, counts = prediction_world()
        question = question_card(QUESTION, **QUESTION_STYLE)
        self.add(panels, bodies, live, counts, question, schematic())
        animate_neurons(live[0])
        self.at("without living neurons", lead=0)
        self.play(FadeOut(question), run_time=0.43)
        self.at("every neuron gene drops", lead=0)
        collapsed = condition_counts((0, 0, 0, 0), RED, GANGLION_X[1])
        for _, mark in collapsed:
            mark.stretch_to_fit_height(0.035).shift(DOWN * 0.18)
        self.play(Transform(counts[1], collapsed), run_time=1.56)
        loss = label("Cell loss, not NGF", 3.33, 3.14, 34, RED)
        self.at("your counts measure")
        self.play(FadeIn(loss), run_time=0.55)
        self.play(FadeOut(live[1]), run_time=2.0)

        self.at("both groups must keep", lead=0.55)
        protected = bodies[1].copy().scale(0.90)
        restored = ganglia()[2][1]
        restored.scale(0.90, about_point=bodies[1].get_center())
        control = SurroundingRectangle(VGroup(protected, restored), color=GREEN,
                                       corner_radius=0.23, buff=0.24, stroke_width=4)
        self.play(FadeOut(loss), Transform(bodies[1], protected), Create(control), FadeIn(restored),
                  Transform(counts[1], condition_counts(GANGLION_COUNTS[0], GREEN, GANGLION_X[1])),
                  run_time=1.35)
        animate_neurons(restored)
        self.at("a second limit is time", lead=0.38)
        for group in (live[0], restored):
            for n in group:
                n.clear_updaters()
        cell, frame, strips = snapshot_cell()
        self.play(FadeOut(panels), FadeOut(bodies), FadeOut(live[0]), FadeOut(restored), FadeOut(counts),
                  FadeOut(control), FadeIn(cell, scale=0.72), run_time=1.28)
        self.at("an RNA profile", lead=0.45)
        self.play(Create(frame), LaggedStart(*[FadeIn(s, shift=UP * 0.23) for s in strips],
                                             lag_ratio=0.29), run_time=1.55)
        snapshot = label("RNA snapshot", -2.77, 3.06, 38)
        self.at("a snapshot of active genes", lead=0.12)
        self.play(FadeIn(snapshot), run_time=0.6)
        for i, strip in enumerate(strips):
            bob(strip, amp=0.15, speed=1.55, seed=i * 1.6)

        self.at("a hidden fate bias", lead=0.52)
        paths = fate_paths()
        futures = VGroup(*[membrane(1.46, 1.39, GREY, 2, 0.20).move_to(pt(4.41, y))
                           for y in (-1.46, 1.46)])
        self.play(LaggedStart(*[GrowArrow(p) for p in paths], lag_ratio=0.33), run_time=1.75)
        self.play(LaggedStart(*[FadeIn(c, scale=0.70) for c in futures], lag_ratio=0.33), run_time=1.1)
        self.finish()


class S09UnlockedNgf(SpokenScene):
    def construct(self):
        panels, bodies, live = ganglia(panel_bottom=-2.42)
        self.add(panels.left_frame, panels.right_frame, bodies, live, schematic())
        signals = ngf_signals(GANGLION_X[0])
        self.add(signals)
        for group in live:
            animate_neurons(group)
        for i, dot in enumerate(signals):
            bob(dot, amp=0.17, speed=1.4, seed=i)
        source = label("Deppmann, Ginty and colleagues", 0, 3.12, 33)
        self.at("and colleagues used", lead=0.85)
        self.play(FadeIn(source), run_time=0.6)
        left_head = label("Lacking Bax", GANGLION_X[0], 2.10, 34, BLUE)
        right_head = label("Lacking Bax and NGF", GANGLION_X[1], 2.10, 34, BLUE)
        self.at("mice lacking", lead=0.2)
        self.play(FadeIn(left_head), run_time=0.6)
        right_ngf = ngf_signals(GANGLION_X[1])
        right_out = right_ngf.copy().shift(UP * 0.62)
        self.at("sympathetic neurons survive", lead=0.78)
        self.play(FadeIn(right_ngf), run_time=0.4)
        self.play(Transform(right_ngf, right_out.set_opacity(0)), run_time=1.6)
        self.remove(right_ngf)
        self.at("they compared those ganglia", lead=0.52)
        counts = VGroup(*[condition_counts(GANGLION_COUNTS[0], GREEN, x) for x in GANGLION_X])
        self.play(FadeIn(counts, shift=UP * 0.22), run_time=1.24)
        self.at("ganglia lacking both", lead=0.05)
        self.play(FadeIn(right_head), run_time=0.65)

        self.at("that gave NGF", lead=0.50)
        self.play(FadeOut(source), run_time=0.36)
        genes_title = label("NGF-dependent genes", 0, 3.12, 38)
        self.play(FadeIn(genes_title), run_time=0.62)
        lower = condition_counts(GANGLION_COUNTS[1], GREEN, GANGLION_X[1])
        categories = (
            ("genes transcription", "Transcription factors", -3.20, -2.96),
            ("synaptic genes", "Synaptic genes", 1.50, -2.96),
            ("metabolism", "Metabolism & cell size", -3.20, -3.57),
            ("axon growth", "Axon growth", 1.50, -3.57),
        )
        for i, (cue, words, x, y) in enumerate(categories):
            self.at(cue, lead=0.15)
            self.play(Transform(counts[1][i], lower[i]), FadeIn(label(words, x, y, 30)),
                      run_time=0.56)
        self.finish()


def progenitor(x, y, diameter=2.5, tagged=False):
    shell = membrane(diameter, diameter * 0.95, BLUE, 2, 0.58).move_to(pt(x, y))
    nucleus = membrane(diameter * 0.49, diameter * 0.43, BLUE, 2, 0.68).move_to(pt(x, y))
    barcode = Annulus(inner_radius=diameter * 0.143, outer_radius=diameter * 0.175,
                      fill_color=YELLOW, fill_opacity=1, stroke_width=0).move_to(pt(x, y))
    return VGroup(shell, nucleus, barcode) if tagged else VGroup(shell, nucleus)


def blood_progeny(x, y):
    shell = membrane(1.33, 0.89, GREEN, 1, 0.56).rotate(-0.23).move_to(pt(x, y))
    nucleus = VGroup(*[
        Ellipse(width=0.36, height=0.29, color=GREEN, fill_opacity=0.82, stroke_width=0)
        .move_to(pt(x + dx, y + dy))
        for dx, dy in ((-0.20, 0.07), (0.02, -0.05))
    ])
    barcode = Annulus(inner_radius=0.095, outer_radius=0.124, fill_color=YELLOW,
                      fill_opacity=1, stroke_width=0).move_to(pt(x + 0.34, y - 0.04))
    return VGroup(shell, nucleus, barcode)


class S10UnlockedLineage(SpokenScene):
    def construct(self):
        cell, frame, strips = snapshot_cell()
        self.add(cell, frame, strips, schematic())
        snapshot = label("RNA snapshot", -2.77, 3.06, 38)
        self.add(snapshot)
        for i, strip in enumerate(strips):
            bob(strip, amp=0.15, speed=1.55, seed=i)
        self.at("can also miss things", lead=0.16)
        parent = progenitor(0, 0.22, 3.90)
        self.play(FadeOut(frame), FadeOut(snapshot), FadeOut(strips),
                  ReplacementTransform(cell, parent), run_time=1.35)

        self.at("weinreb klein camargo", lead=0.22)
        credit = label("Weinreb, Klein, Camargo and colleagues", 0, 3.13, 32)
        self.play(FadeIn(credit), run_time=0.6)
        self.at("mouse blood progenitors", lead=0.35)
        name = label("Mouse blood progenitor", 0, -2.23, 33)
        self.play(FadeIn(name), run_time=0.55)
        self.at("inherited DNA barcodes", lead=0.45)
        barcoded = progenitor(0, 0.22, 3.90, tagged=True)
        self.play(FadeIn(barcoded[2], scale=0.4), run_time=0.8)
        self.add(barcoded)
        self.remove(parent)
        sisters = VGroup(progenitor(-3.89, 0.26, 2.32, True), progenitor(3.51, 0.26, 2.32, True))
        self.play(FadeOut(name), ReplacementTransform(barcoded, sisters[1]),
                  ReplacementTransform(barcoded.copy(), sisters[0]), run_time=2.25)

        self.at("they sequenced some cells", lead=0.5)
        gate = sequencer(-3.89, 0.26).scale(0.83)
        sequenced = sisters[0].copy()
        self.play(FadeOut(credit), FadeIn(gate), sequenced.animate.scale(0.38), run_time=0.85)
        self.play(FadeOut(sequenced), sisters[0].animate.move_to(pt(-4.92, 1.86)).scale(0.47),
                  FadeOut(gate), run_time=0.73)
        early = VGroup(*[count_tile(0.5, BLUE, -3.65, 0.70 - 0.70 * i, 1.78, 0.57) for i in range(4)])
        early_label = label("Early RNA profile", -3.65, -2.30, 32)
        self.play(FadeIn(early), FadeIn(early_label), run_time=0.7)

        self.at("followed their sister's progeny", lead=0.3)
        right = sisters[1]
        self.play(right.animate.move_to(pt(1.51, 1.14)).scale(0.64), run_time=0.76)
        paths = VGroup(*[
            Arrow(pt(2.49, 0.96), pt(x, y), buff=0, color=GREY, stroke_width=3,
                  max_tip_length_to_length_ratio=0.12)
            for x, y in ((4.80, 1.58), (4.24, -0.44))
        ])
        progeny = VGroup(blood_progeny(4.30, -1.20), blood_progeny(5.76, -2.00))
        self.play(*[GrowArrow(path) for path in paths], run_time=0.40)
        self.play(LaggedStart(*[TransformFromCopy(right, c) for c in progeny],
                              lag_ratio=0.27), run_time=1.50)
        fates = VGroup(*[SurroundingRectangle(c, buff=0.17, color=GREEN, corner_radius=0.28, stroke_width=3.5)
                         for c in sisters])
        self.at("sister cells shared fate biases", lead=0.45)
        self.play(LaggedStart(*[Create(f) for f in fates], lag_ratio=0.23),
                  paths[1].animate.set_color(GREEN), run_time=1.5)
        fate_title = label("Shared fate bias", 3.65, 2.88, 36, GREEN)
        self.play(FadeIn(fate_title), run_time=0.52)
        for i, c in enumerate(progeny):
            breathe(c[0], base=0.56, amplitude=0.18, speed=1.7, phase=i)
            bob(c, amp=0.11, speed=1.45, seed=i + 1)
        self.at("RNA profiles had not detected")
        self.play(Indicate(early, color=BLUE, scale_factor=1.05), run_time=1.6)
        self.at("RNA counts capture", lead=0.30)
        self.play(FadeOut(fate_title), run_time=0.5)
        self.play(FadeIn(label("Active genes now", -3.65, 2.88, 36, BLUE)), run_time=0.7)
        self.at("a cell's whole story", lead=0.7)
        self.play(fates[1].animate.set_stroke(GREEN, width=5),
                  paths[1].animate.set_stroke(GREEN, width=5), run_time=1.25)
        self.finish()


class S11End(EndCard):
    LINE = "Sequencing RNA counts which genes each cell uses right now."
