"""Next-generation sequencing, timed against the supplied narration.

BLUE: glass and optics. GREY: chromosome structure. PURPLE: DNA and reads.
TEAL / BLUE / YELLOW / ORANGE: A / C / G / T fluorescence (schematic colours).
RED: gaps, blocked ends and variants. GREEN: verified placement and positive evidence.
GOLD: dates and the prediction.
"""
from bp_parts import *
from bp_style import EndCard

PURPLE = "#B58CD9"
ORANGE = "#F29E4C"
BASE_COLORS = dict(A=TEAL, C=BLUE, G=YELLOW, T=ORANGE)
TRACK_Y = 1.77
REPEAT_X = (-3.8, 0, 3.8)
CHROMOSOME_EDGES = (-5.86, -4.42, -3.18, -0.62, 0.62, 3.18, 4.42, 5.86)
QUESTION = "Will more short reads close the gaps?"
QUESTION_STYLE = dict(y=3.16, size=36)
AMBIGUOUS_POSITIONS = ((-1.9, -0.10), (0, -0.55), (1.9, -0.10))
SPOTS = tuple(
    (x + 0.1 * np.sin(2 * j + i), y + 0.08 * np.cos(j + 3 * i))
    for j, y in enumerate((-2.65, -2.09, -1.53, -0.97, -0.41, 0.15))
    for i, x in enumerate(np.linspace(-5.55, 5.55, 13))
)


def plate(w, h, x, y, color, fill=0.48, edge=0, radius=0.11):
    return RoundedRectangle(
        width=w, height=h, corner_radius=min(radius, h / 3),
        stroke_color=color, stroke_width=edge, fill_color=color, fill_opacity=fill,
    ).move_to([x, y, 0])


def label(text, x=0, y=3.16, size=34, color=TEXT):
    return T(text, size, color).move_to([x, y, 0])


def fragment(x, y, w=1.34, h=0.29, color=PURPLE, striped=False):
    body = plate(w, h, x, y, color, 0.84)
    bars = VGroup(*(
        plate(w * 0.065, h * 0.64, x + w * f, y, TEXT, 0.9)
        for f in (-0.32, -0.13, 0.14, 0.32)
    )) if striped else VGroup()
    return VGroup(body, bars)


def chromosome(mode="gaps"):
    """The same track and repeat coordinates in the opening, assembly and conclusion."""
    g = VGroup(plate(12, 0.88, 0, TRACK_Y, GREY, 0.28, 2))
    for i, (a, b) in enumerate(zip(CHROMOSOME_EDGES, CHROMOSOME_EDGES[1:])):
        w, x = b - a, (a + b) / 2
        if i % 2 == 0:
            g.add(plate(w - 0.03, 0.70, x, TRACK_Y, GREY, 0.68))
            for f in np.linspace(0.16, 0.84, round(3 * w)):
                g.add(plate(0.055, 0.46, a + f * w, TRACK_Y, TEXT, 0.46))
        elif mode == "repeats":
            g.add(plate(w - 0.06, 0.68, x, TRACK_Y, BG, 1, 2))
            g.add(fragment(x, TRACK_Y, w - 0.34, 0.45, striped=True))
        else:
            color = GREEN if mode == "complete" else BG
            g.add(plate(w - 0.06, 0.68, x, TRACK_Y, color, 0.82 if mode == "complete" else 1, 2))
    return g


def optic(width=11.6, height=0.42, y=-2.6, opacity=0.28):
    """The moving patch of illumination stays inside the glass."""
    return VGroup(*(
        plate(width - 0.10 * i, height * f, 0, y, BLUE, opacity * strength)
        for i, (f, strength) in enumerate(((1, 0.24), (0.75, 0.38), (0.34, 0.55)))
    ))


def glass(live=True, clusters=True, lanes=True):
    rim = plate(12, 3.53, 0, -1.25, BLUE, 0.62, radius=0.22)
    pane = plate(11.93, 3.46, 0, -1.25, "#284452", 1, radius=0.20)
    g = VGroup(rim, pane)
    if lanes:
        for y in (-2.81, -2.55, -1.99, -1.43, -0.87, -0.31, 0.25):
            g.add(plate(11.48, 0.022, 0, y, BLUE, 0.18))
    if live:
        sweep = optic(y=-1.31)
        g.add(bob(sweep, amp=1.37, speed=1.65))
    if clusters:
        g.add(cluster_field())
    return g


def cluster_field():
    sites = VGroup()
    colors = tuple(BASE_COLORS.values())
    for i, (x, y) in enumerate(SPOTS):
        col = colors[(i * 9 + i // 13) % len(colors)]
        sites.add(VGroup(
            Dot([x, y, 0], radius=0.14, color=col, fill_opacity=0.29),
            Dot([x, y, 0], radius=0.062, color=col, fill_opacity=0.94),
        ))
    return sites


def scheme():
    return scope_tag(size=25, color=TEXT)


def repeat_picture():
    more = VGroup(*(fragment(x, y, striped=True) for x, y in AMBIGUOUS_POSITIONS))
    return VGroup(glass(live=False), chromosome("repeats"), fragment(0, 0.88, striped=True), more)


def sequence(bases, x, y, tile_w=0.59, gap=0.045):
    tiles = VGroup()
    for i, base in enumerate(bases):
        sx = x + (i - (len(bases) - 1) / 2) * tile_w
        tiles.add(VGroup(
            plate(tile_w - gap, 0.53, sx, y, BASE_COLORS[base], 1),
            label(base, sx, y, 29, BG),
        ))
    return tiles


def rise_reads(scene, targets, sources, color=PURPLE, runtime=3, striped=False):
    reads = []
    animations = []
    for (x, y), (sx, sy) in zip(targets, sources):
        read = fragment(x, y, color=color, striped=striped)
        reads.append(read)
        animations.append(FadeIn(read, shift=np.array([x - sx, y - sy, 0])))
    scene.play(LaggedStart(*animations, lag_ratio=0.24), run_time=runtime)
    return VGroup(*reads)


class S01Hook(SpokenScene):
    def construct(self):
        track = chromosome()
        cell = glass(clusters=False)
        marks = VGroup(*(label("?", x, TRACK_Y, 39, GOLD) for x in REPEAT_X))
        year = ValueTracker(2001)
        clock = counter("{:.0f}", year, [0, 3.13, 0], color=GOLD, size=47)
        self.add(cell, track, scheme())
        self.at("why did closing")
        self.play(LaggedStart(*(FadeIn(m) for m in marks), lag_ratio=0.20), run_time=1.7)
        self.at("take from 2001")
        self.add(clock)
        self.play(year.animate.set_value(2022), run_time=2.6, rate_func=linear)
        self.at("two drafts appeared")
        clock.clear_updaters()
        self.play(FadeOut(clock), FadeOut(marks), run_time=0.32)
        drafts = VGroup(*(chromosome().scale(0.68).move_to([0, y, 0]) for y in (-0.45, -1.45)))
        self.play(LaggedStart(*(FadeIn(d, shift=UP * 0.27) for d in drafts), lag_ratio=0.4), run_time=1.35)
        feb = label("February 2001 · Two drafts", color=GOLD)
        self.play(FadeIn(feb), run_time=0.45)
        self.at("every chromosome except")
        self.play(FadeOut(feb), FadeOut(drafts), run_time=0.85)
        self.at("without a gap", lead=0.7)
        closed = chromosome("complete")
        self.play(Transform(track, closed), run_time=1.1)
        self.at("gap in 2022")
        result = label("2022 · All except Y", color=GOLD)
        self.play(FadeIn(result), run_time=0.5)
        self.at("next generation sequencing")
        sites = cluster_field()
        self.play(FadeOut(result, run_time=0.45), LaggedStart(*(
            FadeIn(VGroup(*sites[i:i + 13])) for i in range(0, len(sites), 13)
        ), lag_ratio=0.24, run_time=3.05))
        self.finish()


class S02Title(TitleCard):
    LESSON = "Next-generation sequencing and genome assembly"
    TITLE = "Reading Millions of DNA Fragments at Once"

    def construct(self):
        cell = glass()
        track = chromosome("complete")
        veil = Rectangle(width=11.35, height=1.04, fill_color=BG, fill_opacity=1,
                         stroke_width=0).move_to([0, -1.24, 0])
        heading = fit_text(self.TITLE, max_w=10.65, size=49, min_size=36, font=TITLE_FONT)
        heading.move_to(veil)
        self.add(cell, track, scheme())
        veil.set_z_index(1)
        heading.set_z_index(2)
        self.play(FadeIn(veil), FadeIn(heading), run_time=self.beat(0.3))
        self.wait(self.beat(0.44))
        self.play(FadeOut(heading), FadeOut(veil), run_time=self.beat(0.24))
        self.finish()


class S03Prepare(SpokenScene):
    def construct(self):
        cell = glass(clusters=False)
        track = chromosome("complete")
        scan = plate(2.2, 0.70, -4.6, TRACK_Y, YELLOW, 0.53, 2)
        sites = cluster_field()
        self.add(cell, track, sites, scheme())
        self.at("each sanger reaction")
        self.play(FadeOut(sites), FadeIn(scan), run_time=0.83)
        self.at("reads one region")
        self.play(scan.animate.set_x(-3.47), run_time=1.6)
        sanger = label("Sanger · 800–1,000 bases", color=YELLOW)
        self.play(FadeIn(sanger), run_time=0.55)
        self.at("short")
        parallel = label("Short-read sequencing", color=PURPLE)
        windows = VGroup(*(plate(1.18, 0.67, x, TRACK_Y, PURPLE, 0.58, 2)
                           for x in np.linspace(-5.12, 5.12, 8)))
        self.play(FadeOut(scan, run_time=0.75), swap(sanger, parallel, 0.75),
                  LaggedStart(*(FadeIn(b) for b in windows), lag_ratio=0.18, run_time=2.1))
        self.at("genomic dna breaks")
        self.play(FadeOut(track), run_time=0.45)
        targets = [(x, y) for y in (-0.36, -1.5, -2.57) for x in (-4.7, -2.36, 0, 2.36, 4.7)]
        pieces = VGroup(*(fragment(x, y) for x, y in targets))
        self.play(FadeOut(windows), LaggedStart(*(
            FadeIn(p, shift=(p.get_y() - TRACK_Y) * UP) for p in pieces
        ), lag_ratio=0.10), run_time=2.5)
        self.at("fitted with adapters")
        caps = VGroup(*(plate(0.22, 0.29, x + dx, y, ORANGE, 0.95)
                        for x, y in targets for dx in (-0.72, 0.72)))
        self.play(LaggedStart(*(GrowFromCenter(c) for c in caps), lag_ratio=0.06), run_time=1.25)
        adapters = label("Adapters", color=ORANGE)
        self.play(swap(parallel, adapters))
        self.at("each fragment copies")
        stacks = VGroup(*(VGroup(*(fragment(x, y + dy, w=0.94, h=0.095)
                                    for dy in (-0.16, 0, 0.16))) for x, y in targets))
        self.play(FadeOut(caps), FadeOut(pieces), FadeIn(stacks), run_time=1.3)
        cluster = label("Clusters of identical copies", color=PURPLE)
        self.play(swap(adapters, cluster))
        sites = cluster_field()
        self.play(FadeOut(stacks), FadeIn(sites), run_time=1.55)
        self.finish()


def cluster_detail():
    """A close view of one cluster, with copies aligned to the same growing end."""
    bed = plate(12, 4.4, 0, -0.55, BLUE, 0.39, 2.5, 0.22)
    rows = VGroup()
    for y in (0.99, 0.23, -0.53, -1.29):
        row = VGroup(fragment(-2.43, y, w=5.7, h=0.35), fragment(-0.19, y - 0.22, w=10.21, h=0.08))
        rows.add(row)
    return VGroup(bed, bob(optic(y=-0.35), amp=1.4, speed=1.5), rows)


def attached(column_x, base, tagged=True):
    g = VGroup()
    for y in (0.99, 0.23, -0.53, -1.29):
        unit = plate(0.47, 0.35, column_x, y, BASE_COLORS[base], 1)
        if tagged:
            dye = Dot([column_x, y + 0.28, 0], radius=0.10, color=BASE_COLORS[base])
            stop = plate(0.13, 0.35, column_x + 0.28, y, RED, 1)
            g.add(VGroup(unit, dye, stop))
        else:
            g.add(VGroup(unit))
    return g


class S04Cycle(SpokenScene):
    def construct(self):
        full = glass()
        detail = cluster_detail()
        self.add(full, scheme())
        self.at("now every cluster")
        self.play(FadeOut(full), FadeIn(detail, scale=0.45), run_time=1.35)
        steps = label("Add   ·   Image   ·   Reset", color=BLUE)
        self.play(FadeIn(steps), run_time=0.65)
        self.at("each nucleotide carries")
        tokens = sequence("ACGT", 0, 2.15, tile_w=1.35, gap=0.22)
        tags = VGroup(*(VGroup(
            Dot(t.get_center() + UP * 0.38, radius=0.088, color=BASE_COLORS[b]),
            plate(0.14, 0.53, t.get_right()[0] + 0.05, t.get_y(), RED, 1),
        ) for t, b in zip(tokens, "ACGT")))
        self.play(FadeIn(tokens, shift=LEFT * 0.8), FadeIn(tags, shift=LEFT * 0.8), run_time=1.32)
        self.at("reversible terminator")
        terminator = label("Reversible terminator", color=RED)
        self.play(swap(steps, terminator))
        self.at("that removable block")
        add = label("Add", color=BLUE)
        joined = attached(0.65, "G")
        self.play(FadeOut(tokens), FadeOut(tags), LaggedStart(*(
            FadeIn(t, shift=LEFT * 2.2) for t in joined
        ), lag_ratio=0.15), run_time=1.27)
        self.play(swap(terminator, add))
        stalled = VGroup(*(plate(0.36, 0.31, 1.82, y, TEAL, 0.7)
                           for y in (0.99, 0.23, -0.53, -1.29)))
        self.play(FadeIn(stalled, shift=LEFT * 0.35), run_time=0.44)
        self.play(stalled.animate.shift(LEFT * 0.34), run_time=0.45)
        self.play(FadeOut(stalled, shift=RIGHT * 0.33), run_time=0.65)
        self.at("imaging logs each")
        image = label("Image", color=BLUE)
        flash = optic(11.7, 0.56, 1.30, 0.85)
        read = sequence("G", 2.6, -2.0)
        self.play(swap(add, image, 0.55), FadeIn(flash), run_time=0.55)
        self.play(flash.animate.set_y(-1.9), FadeIn(read), run_time=1.12, rate_func=linear)
        self.at("cleaving removes")
        reset = label("Reset", color=BLUE)
        debris = VGroup(*(v for row in joined for v in row[1:]))
        self.play(swap(image, reset), FadeOut(debris, shift=UP * 0.5), FadeOut(flash), run_time=1.28)
        self.remove(joined)
        self.add(attached(0.65, "G", tagged=False))
        notch = VGroup(*(Line([0.9, y, 0], [1.1, y, 0], color=GREEN, stroke_width=5)
                         for y in (0.99, 0.23, -0.53, -1.29)))
        self.at("regenerating the 3'")
        self.play(Create(notch), run_time=0.6)
        hydroxyl = label("Open 3′ hydroxyl", color=GREEN)
        self.play(swap(reset, hydroxyl, 0.66))
        self.at("starts the next cycle")
        new = attached(1.14, "A")
        self.play(FadeOut(notch), LaggedStart(*(FadeIn(row, shift=LEFT * 1.5) for row in new),
                                            lag_ratio=0.12), run_time=1.35)
        self.finish()


class S05Reads(SpokenScene):
    def construct(self):
        cell, track = glass(), chromosome()
        detail = cluster_detail()
        self.add(detail, attached(0.65, "G", False), attached(1.14, "A"), scheme())
        self.at("repeating cycles yields")
        self.play(FadeOut(VGroup(*self.mobjects[:-1])), FadeIn(cell), FadeIn(track), run_time=1.36)
        letters = sequence("GACT", 0, 0.88)
        self.play(LaggedStart(*(FadeIn(t, shift=UP * 0.70) for t in letters), lag_ratio=0.20), run_time=1.82)
        name = label("Read", color=PURPLE)
        self.play(FadeIn(name), run_time=0.52)
        self.at("software aligns or assembles")
        self.play(FadeOut(name), run_time=0.4)
        locks = rise_reads(self, [(x, TRACK_Y) for x in (-5.05, -2.04, 1.85, 5.05)],
                           [(-4.1, -2.55), (-3.2, -1.1), (2.6, -2.7), (5, -1.7)],
                           color=GREEN, runtime=4.1)
        self.at("genome results depend")
        records = label("What it records", color=PURPLE)
        self.play(FadeIn(records), Flash(letters, color=PURPLE, flash_radius=1.28, num_lines=8),
                  run_time=1.1)
        self.at("and where it fits")
        fits = label("Where it fits", color=GREEN)
        self.play(swap(records, fits, 0.77), Flash(locks[-1], color=GREEN, flash_radius=0.82, num_lines=8),
                  run_time=1.13)
        self.finish()


class S06Predict(SpokenScene):
    def construct(self):
        cell, track, read, _ = repeat_picture()
        gaps = chromosome()
        self.add(cell, gaps, scheme())
        self.at("a short read matches")
        self.play(FadeIn(read, shift=UP * 2.1), run_time=1.15)
        self.at("a repetitive sequence")
        self.play(FadeIn(track), FadeOut(gaps), run_time=0.64)
        repeat = label("Repetitive sequence", color=PURPLE)
        self.play(FadeIn(repeat), run_time=0.55)
        self.at("appearing in several places", lead=0)
        self.play(read.animate.set_x(-3.8), run_time=1.55, rate_func=there_and_back)
        self.at("if a faster machine")
        extra = rise_reads(self, AMBIGUOUS_POSITIONS,
                           [(-3.4, -2.55), (2.3, -2.6), (4.9, -2.8)], runtime=2.46, striped=True)
        self.at("will the assembly gaps")
        question = question_card(QUESTION, **QUESTION_STYLE)
        crowd = VGroup(read, *extra)
        span = (self.narration_s + 0.40 - self.elapsed()) / 2
        self.play(swap(repeat, question, 0.75), crowd.animate.shift(RIGHT * 3.35),
                  run_time=span, rate_func=linear)
        self.play(crowd.animate.shift(LEFT * 3.35), run_time=span, rate_func=linear)
        self.finish()


class S07Pause(Scene):
    def construct(self):
        self.camera.background_color = BG
        self.add(repeat_picture(), question_card(QUESTION, **QUESTION_STYLE), scheme())
        self.wait(4.5)


class S08Answer(SpokenScene):
    def construct(self):
        cell, track, read, extra = repeat_picture()
        question = question_card(QUESTION, **QUESTION_STYLE)
        self.add(cell, track, read, extra, question, scheme())
        self.at("no because reporting")
        crowd = VGroup(read, *extra)
        self.play(FadeOut(question), crowd.animate.shift(LEFT * 3.2), run_time=0.62, rate_func=linear)
        sweep = bob(optic(y=-1.31), amp=1.37, speed=1.65).set_z_index(1)
        self.add(sweep)
        track.set_z_index(2)
        crowd.set_z_index(3)
        rule = label("Reporting a base ≠ locating it", color=GOLD)
        self.play(FadeIn(rule), crowd.animate.shift(RIGHT * 0.7), run_time=1.5)
        self.at("short reads from repetitive")
        self.play(crowd.animate.shift(RIGHT * 5.8), run_time=2.69)
        self.at("leaving gaps between")
        self.play(FadeOut(track), FadeOut(crowd), FadeIn(chromosome()), run_time=0.55)
        rise_reads(self, [(x, TRACK_Y) for x in (-5.05, -1.9, 1.9, 5.05)],
                   [(-4.4, -1.9), (-2.1, -2.5), (2.1, -1.5), (4.2, -2.65)],
                   color=GREEN, runtime=2.53)
        self.at("faster machines alone")
        year = ValueTracker(2001)
        dates = counter("{:.0f}", year, [0, 3.15, 0], color=GOLD, size=44)
        self.play(swap(rule, dates, 0.45))
        self.play(year.animate.set_value(2022), run_time=2.6, rate_func=linear)
        self.finish()


def read_stack(n, x, top, w=3.55, variant=(), step=0.39):
    rows = VGroup()
    for i in range(n):
        y = top - i * step
        cx = x + (i % 3 - 1) * 0.16
        row = fragment(cx, y, w=w, h=0.24)
        if i in variant:
            row.add(Dot([x + 0.37, y, 0], radius=0.098, color=RED))
        rows.add(row)
    return rows


def stack_backdrop():
    return VGroup(glass(clusters=False, lanes=False), chromosome("complete"))


class S09ControlsSample(SpokenScene):
    def construct(self):
        self.add(stack_backdrop(), scheme())
        shallow = read_stack(3, -3.1, -0.30)
        self.at("even when reads align")
        self.play(LaggedStart(*(FadeIn(r, shift=UP * 1.4) for r in shallow), lag_ratio=0.33), run_time=1.9)
        sample = label("One parental sample", -3.1, 0.88, 31)
        self.play(FadeIn(sample), run_time=0.48)
        self.at("an apparently new variant")
        child_reads = read_stack(3, 3.1, -0.30, variant=(0, 1, 2))
        self.play(LaggedStart(*(FadeIn(r, shift=UP * 1.4) for r in child_reads), lag_ratio=0.26), run_time=1.8)
        child = label("Child", 3.1, 0.88, 31)
        self.play(FadeIn(child), run_time=0.5)
        self.at("deep sequencing across")
        deep = VGroup(*(read_stack(3, -3.1, y, variant=v, step=0.25)
                        for y, v in ((-0.3, ()), (-1.2, (1,)), (-2.1, ()))))
        tissues = label("Several parental tissues", -3.1, 0.88, 31)
        self.play(FadeOut(shallow), swap(sample, tissues), LaggedStart(*(
            FadeIn(rows, shift=UP * 0.38) for rows in deep
        ), lag_ratio=0.33), run_time=2.5)
        self.at("caught this germline")
        tally = ValueTracker(0)
        result = counter("{:.0f} of 58 families", tally, [0, 3.12, 0], size=40, color=GREEN)
        self.play(FadeIn(result), Flash(deep[1][1][-1], color=RED, flash_radius=0.45, num_lines=6),
                  run_time=0.58)
        self.play(tally.animate.set_value(5), run_time=1.0, rate_func=linear)
        self.finish()


def cells(n, x, y, color=PURPLE):
    offsets = [(0, 0), (-0.52, -0.38), (0.52, -0.38), (0, -0.83),
               (-0.93, -0.82), (0.93, -0.82), (-0.49, -1.24), (0.49, -1.24)]
    return VGroup(*(VGroup(
        Dot([x + dx, y + dy, 0], radius=0.29, color=color, fill_opacity=0.67),
        Dot([x + dx, y + dy, 0], radius=0.11, color=color),
    ) for dx, dy in offsets[:n]))


class S10ControlsMeaning(SpokenScene):
    def construct(self):
        cell, track = stack_backdrop()
        self.add(cell, track, scheme())
        before_reads = read_stack(1, -1.1, 0.06, w=4.65)
        relapse_reads = read_stack(1, -1.1, -0.70, w=4.65, variant=(0,))
        before = label("Before treatment", 3.03, 0.06, 29)
        relapse = label("Relapse", 3.03, -0.70, 29)
        comparison = VGroup(before_reads, relapse_reads, before, relapse)
        variant_read = read_stack(1, -0.37, -0.66, w=6.2, variant=(0,))
        self.at("read evidence alone")
        self.play(FadeIn(variant_read, shift=RIGHT * 1.4), run_time=1.35)
        self.at("what a variant")
        self.play(Flash(variant_read[0][-1], color=RED, flash_radius=0.42, num_lines=6), run_time=0.72)
        self.at("a change may be")
        panel = TwoPanel("Driver", "Passenger", top=1.04, bottom=-2.66, width=11.8, gap=0.6,
                         colors=(GREEN, PURPLE), size=32)
        for frame in (panel.left_frame, panel.right_frame):
            frame.set_fill("#284452", opacity=1)
        driver, passenger = cells(3, -3.1, -0.43, GREEN), cells(3, 3.1, -0.43)
        origin = variant_read[0][-1]
        self.play(FadeOut(variant_read[0][0]), FadeOut(cell),
                  origin.animate.move_to([0, 1.20, 0]), run_time=0.45)
        branches = VGroup()
        for frame in (panel.left_frame, panel.right_frame):
            top = frame.get_top()
            branches.add(VMobject(color=RED, stroke_width=3).set_points_as_corners([
                origin.get_center(), [top[0], origin.get_y(), 0], top,
            ]))
        self.play(Create(branches[0]), FadeIn(panel.left_frame), FadeIn(panel.left_head),
                  FadeIn(driver), run_time=0.67)
        grown = cells(8, -3.1, -0.43, GREEN)
        self.play(LaggedStart(*(GrowFromCenter(c) for c in grown[3:]), lag_ratio=0.33), run_time=1.93)
        self.at("a passenger giving")
        self.play(Create(branches[1]), FadeIn(panel.right_frame), FadeIn(panel.right_head),
                  FadeIn(passenger), run_time=0.63)
        self.at("comparing before treatment")
        self.play(FadeOut(VGroup(panel, driver, *grown[3:], passenger, origin, branches)), run_time=0.58)
        self.play(FadeIn(cell), FadeIn(comparison), run_time=0.68)
        self.at("still requires testing")
        test = label("Does the enzyme still work?", 0, 3.13, 34)
        enzyme = boxed_label("Mutant enzyme", PURPLE, 30).move_to([-2.65, -1.93, 0])
        drug = boxed_label("Drug", ORANGE, 30).move_to([2.78, -1.93, 0])
        for badge in (enzyme, drug):
            badge.box.set_fill(BG, opacity=1)
        self.play(FadeIn(enzyme), run_time=0.48)
        self.play(FadeIn(drug, shift=LEFT * 0.8), run_time=0.72)
        self.play(FadeIn(test), run_time=0.48)
        activity = VGroup(*(plate(0.38, 0.24 + 0.09 * i, x, -1.93, GREEN, 0.87)
                            for i, x in enumerate((-0.61, 0, 0.61, 1.22))))
        self.play(LaggedStart(*(GrowFromCenter(b) for b in activity), lag_ratio=0.45), run_time=1.6)
        self.play(FadeIn(label("Activity with drug", 0.47, -2.67, 28)), run_time=0.48)
        self.finish()


SOIL_COLORS = (PURPLE, ORANGE, TEAL, YELLOW)
SOIL_PROFILE_Y = 1.83
SOIL_LABEL_Y = 2.42


def soil_profile(x, kind):
    """Categorical read patterns schematize similarity, with no abundance scale."""
    patterns = {"young": (0, 1, 0, 1, 1, 2, 0, 1),
                "treated": (2, 0, 2, 3, 2, 0, 3, 2),
                "old": (2, 0, 2, 3, 2, 0, 2, 2)}
    return VGroup(*(fragment(x + 0.8 * (i % 2 - 0.5), SOIL_PROFILE_Y - 0.32 * (i // 2),
                             w=0.66, h=0.25, color=SOIL_COLORS[c])
                    for i, c in enumerate(patterns[kind])))


def soil_comparison():
    young = soil_profile(-3.43, "treated")
    old = soil_profile(3.43, "old")
    young_label = label("Nitrogen + phosphorus", -3.43, SOIL_LABEL_Y, 30, ORANGE)
    old_label = label("About 85 years", 3.43, SOIL_LABEL_Y, 30)
    return VGroup(young, old, young_label, old_label)


class S11UnlockedA(SpokenScene):
    def construct(self):
        cell = glass()
        self.add(cell, scheme())
        track = chromosome()
        self.at("parallel sequencing unlocked")
        self.play(FadeIn(track, shift=UP * 0.68), run_time=1.18)
        leading = rise_reads(self, [(-5.05, TRACK_Y), (-2.0, TRACK_Y), (2, TRACK_Y), (5.05, TRACK_Y)],
                             [(-4, -2.34), (-2.9, -2.2), (1.12, -2.5), (4.58, -1.8)], runtime=2.78)
        self.at("in 2008")
        bentley = label("2008 · Bentley & colleagues", color=GOLD)
        self.play(FadeIn(bentley), run_time=0.66)
        self.at("sequenced a human genome")
        coverage = VGroup()
        for left, right in zip(CHROMOSOME_EDGES[::2], CHROMOSOME_EDGES[1::2]):
            span = right - left
            coverage.add(VGroup(*(
                fragment(left + span * f, TRACK_Y + dy, w=span * 0.34, h=0.14)
                for dy, centers in ((0.15, (0.24, 0.64)), (-0.15, (0.37, 0.77)))
                for f in centers
            )))
        self.play(FadeOut(leading), LaggedStart(*(FadeIn(reads) for reads in coverage),
                                                lag_ratio=0.35), run_time=2.06)
        self.at("in 2014")
        knelman = label("2014 · Knelman & colleagues", color=GOLD)
        self.play(FadeOut(track), FadeOut(coverage), swap(bentley, knelman), run_time=0.88)
        self.at("sequenced bacteria in")
        soil = label("Puca Glacier soil", 0, 1.35, 34)
        initial = soil_profile(-3.43, "young")
        self.play(LaggedStart(*(FadeIn(r, shift=UP * 0.16) for r in initial), lag_ratio=0.26), run_time=2.12)
        self.play(FadeIn(soil), run_time=0.51)
        age = label("About three years", -3.43, SOIL_LABEL_Y, 30)
        self.at("exposed about three years")
        self.play(FadeIn(age), run_time=0.54)
        self.at("plots given nitrogen")
        treated, old, treatment, older = soil_comparison()
        self.play(FadeOut(soil), swap(age, treatment), run_time=0.8)
        one_year = label("One year", 0, 1.35, 30, ORANGE)
        self.play(FadeIn(one_year), run_time=0.45)
        self.play(Transform(initial, treated), run_time=1.55)
        self.at("most resembled soils")
        self.play(LaggedStart(*(FadeIn(r, shift=UP * 0.16) for r in old), lag_ratio=0.2), run_time=1.65)
        self.play(FadeIn(older), run_time=0.63)
        self.play(FadeOut(one_year), run_time=0.42)
        self.finish()


def donor_chromosomes():
    """Pairs of tracks with illustrative crossover positions from different donors."""
    panel = plate(12, 4.60, 0, -0.18, BLUE, 0.32, 2.1, 0.22)
    panel.set_fill("#263e4c", opacity=1)
    tracks, crossed, spacing = VGroup(), VGroup(), VGroup()
    for x, y in zip((-1.8, 1.3, -0.7, 2.0), (1.05, 0.18, -0.69, -1.56)):
        xs = (-5.45, x - 0.31, x + 0.31, 5.45)
        for rows, direction in ((tracks, 1), (crossed, -1)):
            row = VGroup()
            for dy, color in ((0.15, PURPLE), (-0.15, TEAL)):
                start_y, end_y = y + dy, y + direction * dy
                points = [(px, py, 0) for px, py in zip(xs, (start_y, start_y, end_y, end_y))]
                row.add(*(Line(start, end, color=color, stroke_width=8)
                          for start, end in zip(points, points[1:])))
            rows.add(row)
        spacing.add(plate(2.35, 0.64, x, y, GOLD, 0.24))
    return panel, tracks, crossed, spacing


class S12UnlockedB(SpokenScene):
    def construct(self):
        cell = glass()
        prior = soil_comparison()
        knelman = label("2014 · Knelman & colleagues", color=GOLD)
        self.add(cell, prior, knelman, scheme())
        self.at("that shift was in")
        scope = label("Puca Glacier soils", 0, 1.35, 32)
        self.play(FadeIn(scope), run_time=0.6)
        self.at("in 2020")
        panel, tracks, crossed, zone = donor_chromosomes()
        donor = label("2020 · 20 human donors", color=GOLD)
        self.play(FadeOut(prior), FadeOut(scope), swap(knelman, donor),
                  Succession(FadeOut(cell, run_time=0.38), FadeIn(panel, run_time=0.58)),
                  run_time=0.96)
        self.at("single sperm sequencing")
        self.play(LaggedStart(*(FadeIn(r, shift=UP * 1.01) for r in tracks), lag_ratio=0.4), run_time=2.89)
        self.at("one crossover makes")
        self.play(Transform(tracks[0], crossed[0]), run_time=0.48)
        nearby = label("Nearby crossover less likely", 0, 1.72, 30, GOLD)
        self.play(GrowFromCenter(zone[0]), FadeIn(nearby), run_time=1.42)
        self.at("it detected crossover interference")
        self.play(LaggedStart(*(AnimationGroup(Transform(tracks[i], crossed[i]), GrowFromCenter(zone[i]))
                                for i in (1, 2, 3)), lag_ratio=0.51), run_time=2.19)
        interference = label("Crossover interference · All 20", color=GREEN)
        self.play(swap(donor, interference, 0.72))
        self.at("confirming what sturdevant")
        self.play(LaggedStart(*(Flash(c, color=GOLD, flash_radius=0.38, num_lines=6) for c in zone),
                              lag_ratio=0.43), run_time=2.66)
        self.play(FadeOut(nearby), run_time=0.35)
        self.at("parallel reads unlock")
        track = chromosome()
        self.play(FadeOut(VGroup(panel, tracks, zone)), FadeOut(interference),
                  FadeIn(cell), FadeIn(track), run_time=0.68)
        rise_reads(self, [(x, TRACK_Y) for x in REPEAT_X],
                   [(-4.7, -2.1), (0, -2.75), (4.7, -2.1)], color=GREEN, runtime=3.12)
        self.finish()


class S13End(EndCard):
    LINE = "Read millions of fragments at once, then prove where each belongs."
