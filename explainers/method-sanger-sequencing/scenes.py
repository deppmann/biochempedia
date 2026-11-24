"""Sanger sequencing, drawn as a workbench of schematic tracks and readouts."""
from bp_parts import *
from bp_style import EndCard

# COLOR MAP
# BLUE: glass apparatus and untinted copies; GREY: template and guides.
# PURPLE: polymerase; RED: stop/missing connector; GOLD: dates and direction.
# GREEN / TEAL / YELLOW / ORANGE: A / C / G / T, including detector signals.
PURPLE = "#B58CD9"
ORANGE = "#F29E4C"
BASE = dict(A=GREEN, C=TEAL, G=YELLOW, T=ORANGE)
COPY = "ACGTCA"
COMPLEMENT = str.maketrans("ACGT", "TGCA")
LEFT_EDGE = -5.85
STEP = 1.43
PRIMER_END = LEFT_EDGE + STEP * 2
TEMPLATE_Y = 2.35
COPY_Y = 1.23
LADDER_Y = (1.08, 0.29, -0.50, -1.29, -2.08, -2.87)


def xyz(x, y):
    return np.array([x, y, 0.0])


def slab(w, h, color, x, y, fill=0.30, radius=0.12, stroke=2):
    return RoundedRectangle(
        width=w, height=h, corner_radius=min(radius, w / 2, h / 2),
        stroke_color=color, stroke_width=stroke, fill_color=color, fill_opacity=fill,
    ).move_to(xyz(x, y))


def label(text, x, y, size=30, color=TEXT):
    return T(text, size, color).move_to(xyz(x, y))


def badge(text, x, y, color=TEXT, size=30):
    return boxed_label(text, color=color, size=size, min_size=28).move_to(xyz(x, y))


def template_track():
    cells = VGroup()
    for i in range(8):
        x = LEFT_EDGE + STEP * (i + 0.5)
        cells.add(VGroup(slab(1.30, 0.86, GREY, x, TEMPLATE_Y, fill=0.37),
                         label("?", x, TEMPLATE_Y, 34)))
    return cells


def primer(y=COPY_Y):
    return slab(2 * STEP - 0.13, 0.73, BLUE, (LEFT_EDGE + PRIMER_END) / 2, y, fill=0.46)


def copy_bar(n, y, stopped=True):
    end = PRIMER_END + STEP * n
    width = end - LEFT_EDGE - 0.13
    bar = slab(width, 0.54, BLUE, LEFT_EDGE + width / 2, y, fill=0.45)
    if not stopped:
        return VGroup(bar)
    color = BASE[COPY[n - 1]]
    cap = slab(0.64, 0.50, color, end - 0.46, y, fill=0.88, stroke=0)
    cap.set_z_index(1)
    return VGroup(bar, cap)


def ladder():
    return VGroup(*(copy_bar(i, y) for i, y in enumerate(LADDER_Y, 1)))


def nucleotide(base, x, y, stop=False, large=False):
    color = BASE[base]
    w, h = (1.36, 0.97) if large else (1.14, 0.75)
    left = x - w / 2
    # The side tabs are cartoon connectors. The next tile can dock only
    # when the preceding tile has an open right edge.
    tab = slab(0.19, h * 0.44, color, left - 0.04, y, fill=0.85, stroke=0)
    right = x + w / 2
    edge = (
        Line(xyz(right, y - h * .37), xyz(right, y + h * .37), color=RED, stroke_width=6)
        if stop else
        ArcBetweenPoints(xyz(right - .02, y + h * .15), xyz(right - .02, y - h * .15),
                         angle=PI, color=color, stroke_width=3)
    )
    return VGroup(slab(w, h, color, x, y, fill=0.27), tab, edge,
                  label(base + ("★" if stop else ""), x, y, 34 if large else 28, color))


def stopped_track(with_enzyme=False):
    x = PRIMER_END + STEP / 2
    result = VGroup(template_track(), primer(), nucleotide("A", x, COPY_Y, stop=True, large=True))
    if with_enzyme:
        result.add(enzyme_block(x))
    return result


def enzyme_block(x):
    return slab(2.44, 1.02, PURPLE, x, -0.19, fill=0.42)


def trace_peaks(plot, bases, rough=0):
    """Gaussian pulses evaluated from the illustrated detector calls, in arrival order."""
    peaks = VGroup()
    for i, base in enumerate(bases):
        center = i + 0.5
        width = 0.18 if i >= rough else 0.29
        height = (0.94, 0.79, 0.88, 0.73)[i % 4]
        if i < rough:
            height *= (0.47, 0.62, 0.40)[i % 3]
        def signal(t):
            peak = height * np.exp(-0.5 * ((t - center) / width) ** 2)
            if i < rough:
                peak *= 0.77 + 0.23 * np.cos(30 * (t - center))
            return peak
        a, b = max(0, center - 0.45), min(plot.xr[1], center + 0.45)
        color = BASE[base]
        area = Polygon(plot.pt(a, 0), *(plot.pt(t, signal(t)) for t in np.linspace(a, b, 65)),
                       plot.pt(b, 0), stroke_width=0, fill_color=color, fill_opacity=0.32)
        peaks.add(VGroup(area, plot.curve(signal, a, b, color=color, width=4.5, n=85)))
    return peaks


def detector_readout():
    plot = Plot(box=(-2.40, 5.87, 0.42, 2.94), xr=(0, 6), yr=(0, 1), color=GREY)
    return plot, trace_peaks(plot, COPY)


def capillary():
    tube = slab(1.64, 5.47, BLUE, -4.40, 0.09, fill=0.28)
    beam = Line(xyz(-5.61, -1.55), xyz(-3.19, -1.55), color=GOLD, stroke_width=5)
    sensor = slab(0.55, 0.67, GOLD, -2.91, -1.55, fill=0.35)
    return VGroup(tube, beam, sensor)


def call_slots(plot):
    return VGroup(*(badge(base, plot.pt(i + 0.5, 0)[0], -0.28, BASE[base], 34)
                    for i, base in enumerate("ACG")))


class S01Hook(SpokenScene):
    def construct(self):
        track = template_track()
        self.add(track)
        self.at("read the order")
        self.play(LaggedStart(*(tile[0].animate.set_fill(GREY, 0.51) for tile in track),
                              lag_ratio=0.41), run_time=3.67)
        self.at("turns that challenge")
        copies = ladder()
        offsets = (0.04, 0.11, 0.15, 0.19, 0.23, 0.28)
        for row, offset in zip(copies, offsets):
            row.shift(UP * offset)
        self.play(LaggedStart(*(GrowFromEdge(row[0], LEFT) for row in copies),
                              lag_ratio=0.22), run_time=3.30)
        self.at("it copies the strand")
        self.play(LaggedStart(*(Indicate(row[0], color=BLUE, scale_factor=1.01) for row in copies),
                              lag_ratio=0.25), run_time=1.43)
        self.at("stopping different copies")
        self.play(LaggedStart(*(FadeIn(row[1], scale=0.70) for row in copies),
                              lag_ratio=0.22), run_time=0.85)
        self.add(copies)
        self.play(*(row.animate.shift(DOWN * offset) for row, offset in zip(copies, offsets)),
                  run_time=1.3)
        self.finish()


class S02Title(TitleCard):
    TITLE = "Reading DNA by Stopping the Copy"
    LESSON = "Sanger Sequencing"

    def construct(self):
        track, copies = template_track(), ladder()
        track.set_opacity(0.29)
        copies.set_opacity(0.28)
        self.add(track, copies)
        for i, row in enumerate(copies):
            row[1].set_z_index(0).stretch_to_fit_height(0.29)
            bob(row[1], amp=0.07, speed=2.2, seed=i)
        plate = slab(11.5, 2.35, BLUE, 0, 0, fill=0, stroke=2)
        plate.set_fill(BG, 1)
        lesson = label(self.LESSON, 0, 0.63, 28, BLUE)
        title = T(self.TITLE, 49, font=TITLE_FONT).move_to(xyz(0, -0.12))
        rule = Line(xyz(-1.0, -0.76), xyz(1.0, -0.76), color=GOLD, stroke_width=4)
        self.add(plate)
        self.play(FadeIn(lesson), FadeIn(title), GrowFromCenter(rule), run_time=0.30)
        self.wait(1.70, frozen_frame=False)


class S03Setup(SpokenScene):
    def construct(self):
        track = template_track()
        p = primer()
        p_label = label("Primer", -4.43, 0.48, 30, BLUE)
        template_label = label("Single-stranded template", -2.75, 3.20, 30)
        junction = Dot(xyz(PRIMER_END - 0.07, COPY_Y), radius=0.10, color=GOLD)
        three = label("3′", PRIMER_END - 0.37, 0.62, 32, GOLD)
        enzyme = enzyme_block(PRIMER_END + STEP / 2)
        enzyme_label = label("Polymerase", enzyme.get_x(), -0.19, 30)
        self.at("start with")
        self.play(FadeIn(track, shift=UP * 0.20), run_time=1.05)
        self.play(FadeIn(template_label), run_time=0.40)
        self.at("and a primer")
        self.play(FadeIn(p, shift=UP * 0.58), run_time=1.05)
        self.at("a short dna strand")
        self.play(FadeIn(p_label), Indicate(p, color=BLUE, scale_factor=1.04), run_time=1.40)
        self.at("the primer gives")
        self.play(FadeIn(enzyme, shift=UP * 0.92), run_time=1.25)
        self.at("polymerase")
        self.play(FadeIn(enzyme_label), run_time=0.45)
        self.at("three -prime end")
        self.play(GrowFromCenter(junction), FadeIn(three), run_time=0.70)
        self.at("new nucleotides join")
        preview = slab(1.12, 0.60, BLUE, PRIMER_END + 0.72, COPY_Y, fill=0.60)
        self.play(FadeIn(preview, shift=LEFT * 1.05), run_time=1.24)
        self.play(FadeOut(preview, shift=RIGHT * 0.30), run_time=0.61)
        ordinary = VGroup(*(nucleotide(b, -5.16 + 1.65 * i, -2.42) for i, b in enumerate(BASE)))
        stoppers = VGroup(nucleotide("A", 1.88, -2.42, True), nucleotide("T", 3.43, -2.42, True))
        ordinary_label = label("Ordinary nucleotides", -2.74, -1.62, 30)
        stop_label = label("Dideoxynucleotides", 2.65, -1.62, 30)
        self.at("add ordinary")
        self.play(LaggedStart(*(FadeIn(t, shift=UP * 0.45) for t in ordinary), lag_ratio=0.40),
                  run_time=0.90)
        self.play(FadeIn(ordinary_label), run_time=0.34)
        self.at("plus a little")
        self.play(FadeIn(stoppers, shift=UP * 0.35), run_time=0.75)
        self.play(FadeIn(stop_label), run_time=0.42)
        self.at("dideoxynucleotide")
        self.play(stoppers[0][0].animate.set_fill(BASE["A"], 0.55),
                  stoppers[1][0].animate.set_fill(BASE["T"], 0.55), run_time=1.95)
        self.at("each stopper keeps")
        self.play(FadeOut(ordinary_label), FadeOut(stop_label), run_time=0.45)
        self.play(Indicate(ordinary[0][0], color=BASE["A"], scale_factor=1.04),
                  Indicate(stoppers[0][0], color=BASE["A"], scale_factor=1.04), run_time=1.25)
        self.at("five -prime triphosphate")
        tabs = label("5′ triphosphate tabs", -1.35, -3.27, 30, GOLD)
        self.play(FadeIn(tabs),
                  Indicate(ordinary[0][1], color=GOLD, scale_factor=1.25),
                  Indicate(stoppers[0][1], color=GOLD, scale_factor=1.25), run_time=0.95)
        self.at("so polymerase adds")
        supplied = stoppers[0]
        above_pool = supplied.get_center() + UP * 3.65
        self.play(FadeOut(VGroup(ordinary, stoppers[1], enzyme_label, p_label, three, junction,
                                template_label, tabs)),
                  supplied.animate.move_to(above_pool), run_time=0.56)
        self.play(ReplacementTransform(supplied, nucleotide("A", PRIMER_END + STEP / 2, COPY_Y,
                                                            stop=True, large=True)), run_time=0.78)
        self.finish()


class S04StopAndLadder(SpokenScene):
    def construct(self):
        track, p, stop, enzyme = stopped_track(with_enzyme=True)
        self.add(track, p, stop, enzyme)
        incoming = nucleotide("C", 1.70, COPY_Y, large=True)
        self.at("a dideoxynucleotide")
        self.play(FadeIn(incoming, shift=LEFT * 3.08), run_time=2.52)
        self.at("stops a copy")
        self.play(stop[0].animate.set_fill(BASE["A"], 0.50), run_time=0.72)
        self.at("it lacks the")
        no_oh = badge("No 3′-OH", 0.17, 0.11, RED)
        self.play(FadeIn(no_oh), Indicate(stop[2], color=RED, scale_factor=1.16), run_time=1.05)
        self.at("next nucleotide must bond")
        self.play(incoming.animate.shift(LEFT * 2.32), run_time=0.70)
        self.play(incoming.animate.shift(RIGHT * 1.18), enzyme.animate.shift(DOWN * 0.98), run_time=0.48)
        self.play(FadeOut(incoming), FadeOut(enzyme), FadeOut(no_oh), run_time=0.48)

        self.at("at each site")
        short_rows = VGroup(*(copy_bar(1, y, False) for y in LADDER_Y))
        self.play(FadeOut(VGroup(p, stop)), run_time=0.26)
        self.play(FadeIn(short_rows), run_time=0.41)
        continuing = VGroup(*(copy_bar(3 + (i % 4), y, False) for i, y in enumerate(LADDER_Y)))
        self.play(LaggedStart(*(Transform(a, b) for a, b in zip(short_rows, continuing)),
                              lag_ratio=0.24), run_time=2.67)
        self.at("a few take a stopper")
        stopped = ladder()
        self.play(ReplacementTransform(short_rows[0], stopped[0]),
                  ReplacementTransform(short_rows[1], stopped[1]), run_time=1.35)
        self.at("stops fall at every position")
        self.play(LaggedStart(*(ReplacementTransform(short_rows[i], stopped[i]) for i in range(2, 6)),
                              lag_ratio=0.34), run_time=2.50)
        self.at("stopping copies at known bases")
        self.play(LaggedStart(*(row[0].animate.set_fill(BLUE, 0.79) for row in stopped),
                              lag_ratio=0.65), run_time=3.12)
        self.at("ladder of fragment lengths")
        self.play(LaggedStart(*(row[0].animate.set_fill(BLUE, 0.45) for row in stopped),
                              lag_ratio=0.35), run_time=2.0)
        self.finish()


def gel():
    centers = (-4.20, -1.40, 1.40, 4.20)
    lanes = VGroup(*(slab(2.00, 5.21, BLUE, x, -0.60, fill=0.25) for x in centers))
    names = VGroup(*(badge("dd" + b, x, 2.66, BASE[b]) for b, x in zip(BASE, centers)))
    bands = VGroup(*(slab(1.43, 0.24, BASE[b], centers[list(BASE).index(b)],
                          -2.78 + i * 0.82, fill=0.92, stroke=0)
                     for i, b in enumerate(COPY)))
    return lanes, names, bands


class S05Sorting(SpokenScene):
    def construct(self):
        track, rows = template_track(), ladder()
        self.add(track, rows)
        self.at("sort the stopped copies")
        self.play(LaggedStart(*(row.animate.shift(RIGHT * 0.58) for row in rows),
                              lag_ratio=0.44), run_time=2.35)
        self.at("classically")
        lanes, names, bands = gel()
        tubes = VGroup(*(slab(0.94, 1.37, BLUE, lane.get_x(), 0.57, fill=0.40) for lane in lanes))
        self.play(FadeOut(track), FadeOut(rows), FadeIn(tubes, shift=UP * 0.35), run_time=0.86)
        self.play(LaggedStart(*(FadeIn(n, shift=UP * 0.15) for n in names), lag_ratio=0.43),
                  run_time=2.85)
        self.at("four -gel lanes")
        starts = bands.copy()
        for band in starts:
            band.set_y(1.55)
        self.play(ReplacementTransform(tubes, lanes), run_time=0.75)
        # Long fragments travel less far down the gel.
        for i in reversed(range(len(starts))):
            self.play(FadeIn(starts[i]), run_time=0.11)
            self.play(starts[i].animate.move_to(bands[i]), run_time=0.57, rate_func=linear)
        self.at("each terminator got")
        dye = VGroup(*(Dot(xyz(lane.get_x(), 1.75), radius=0.215, color=BASE[b])
                       for b, lane in zip(BASE, lanes)))
        self.play(LaggedStart(*(GrowFromCenter(dot) for dot in dye), lag_ratio=0.55), run_time=2.50)
        self.at("one reaction holds")
        cap = capillary()
        self.play(FadeOut(names), FadeOut(starts), run_time=0.36)
        self.play(ReplacementTransform(lanes, cap[0]), run_time=1.16)
        packets = VGroup(*(slab(0.48 + i * 0.075, 0.18, BASE[b], -4.40, -0.56 + i * 0.55,
                                fill=1, stroke=0) for i, b in enumerate(COPY)))
        self.play(ReplacementTransform(dye, packets), run_time=0.76)
        self.at("capillary sorts fragments")
        self.play(packets.animate.shift(DOWN * 0.70), run_time=1.18, rate_func=linear)
        self.at("by size")
        plot, peaks = detector_readout()
        self.play(Create(plot), FadeIn(cap[1:]), run_time=0.60)
        self.at("a detector reads")
        for i, (packet, peak) in enumerate(zip(packets, peaks)):
            if i:
                self.play(*(p.animate.shift(DOWN * 0.55) for p in packets[i:]),
                          run_time=0.13, rate_func=linear)
            self.play(FadeOut(packet, shift=DOWN * 0.28), FadeIn(peak), run_time=0.22)
        self.finish()


PREDICT = "Write both strands 5′ → 3′."
PROMPTS = ("New strand (5′→3′): ?", "Template (5′→3′): ?")
CARD = dict(y=-2.72, size=32, chip_size=28)


def direction_question():
    card = question_card(PREDICT, PROMPTS, **CARD)
    card.chips.set_x(2.12)
    card.question.set_x(2.12)
    return card


def puzzle_picture():
    plot, peaks = detector_readout()
    return plot, peaks, call_slots(plot), capillary()


class S06Predict(SpokenScene):
    def construct(self):
        plot, peaks, slots, cap = puzzle_picture()
        self.add(plot, peaks, cap)
        self.at("a direction puzzle")
        self.play(*(FadeOut(p) for p in peaks[3:]), run_time=1.05)
        packets = VGroup(*(slab(0.56 + 0.12 * i, 0.18, BASE[b], -4.40, 0.63 + i * 0.59,
                                 fill=1, stroke=0) for i, b in enumerate("ACG")))
        self.at("a detector reports")
        self.play(FadeIn(packets, shift=DOWN * 0.40), run_time=0.65)
        self.play(packets.animate.shift(DOWN * 1.91), cap[0].animate.set_fill(opacity=0.52),
                  run_time=1.6, rate_func=linear)
        self.at("order as a")
        self.play(LaggedStart(*(AnimationGroup(FadeOut(packet, shift=DOWN * 0.35),
                                              FadeIn(slot, shift=DOWN * 0.18),
                                              Indicate(peak[1], color=BASE[b], scale_factor=1.02))
                                 for packet, slot, peak, b in zip(packets, slots, peaks, "ACG")),
                              lag_ratio=0.68), cap[0].animate.set_fill(opacity=0.28), run_time=2.06)
        q = direction_question()
        self.at("what are the new strand")
        self.play(LaggedStart(*(FadeIn(c, shift=UP * 0.16) for c in q.chips), lag_ratio=0.7),
                  run_time=1.32)
        self.at("each written")
        self.play(FadeIn(q.question, shift=UP * 0.14), run_time=0.80)
        self.finish()


class S07Pause(PredictPause):
    SECONDS = 4.5

    def backdrop(self):
        plot, peaks, slots, cap = puzzle_picture()
        return VGroup(plot, peaks[:3], slots, cap)

    def construct(self):
        self.add(self.backdrop(), direction_question())
        x0, y = -4.75, -3.43
        groove = slab(9.45, 0.16, GREY, -0.05, y, fill=0.32, stroke=1.5)
        fill = slab(9.35, 0.09, GOLD, x0 + 9.35 / 2, y, fill=0.95, stroke=0)
        self.add(groove)
        self.play(GrowFromEdge(fill, LEFT), run_time=self.SECONDS, rate_func=linear)


def strand_cells(bases, y, reverse=False):
    tiles = VGroup()
    for i, base in enumerate(bases):
        tile = boxed_label(base, color=BASE[base], size=42, box=(1.48, 1.02), min_size=32,
                           fill_opacity=0.29).move_to(xyz(-1.2 + i * 2.15, y))
        tile.label.set_color(TEXT)
        tiles.add(tile)
    ends = VGroup(label("3′" if reverse else "5′", -2.91, y, 35, GOLD),
                  label("5′" if reverse else "3′", 4.81, y, 35, GOLD))
    return tiles, ends


class S08Reveal(SpokenScene):
    def construct(self):
        plot, peaks, slots, cap = puzzle_picture()
        q = direction_question()
        self.add(plot, peaks[:3], slots, cap, q)
        p = primer(y=-1.59)
        primer_end = label("3′", -2.75, -2.18, 32, GOLD)
        arrow = Arrow(xyz(-2.75, -1.59), xyz(-2.00, -1.59), buff=0, color=GOLD, stroke_width=7)
        first, first_ends = strand_cells("ACG", -1.59)
        copy_bed = slab(9.2, 1.20, BLUE, 0.95, -1.59, fill=0.30, stroke=0)
        self.at("the copy grows")
        self.play(FadeOut(q), FadeOut(cap), run_time=0.49)
        self.play(GrowFromEdge(p, LEFT), run_time=0.96)
        self.play(GrowArrow(arrow), run_time=0.58)
        self.at("3' end")
        self.play(FadeIn(primer_end), run_time=0.55)
        self.at("the shortest fragment")
        self.play(peaks[0][0].animate.set_fill(opacity=0.88), run_time=1.34)
        self.at("first new base")
        self.play(FadeOut(slots[0]), run_time=0.23)
        self.play(FadeIn(first[0], shift=DOWN * 0.79 + RIGHT * 0.28), run_time=1.09)
        self.at("the new strand reads")
        self.play(FadeOut(VGroup(p, arrow, primer_end)), run_time=0.32)
        copy_bed.set_z_index(-1)
        self.play(GrowFromEdge(copy_bed, LEFT), FadeIn(first_ends), run_time=1.58)
        self.at("c g")
        self.play(FadeOut(slots[1]), FadeOut(slots[2]), run_time=0.21)
        self.play(LaggedStart(*(FadeIn(tile, shift=DOWN * 0.78) for tile in first[1:]),
                              lag_ratio=0.65), run_time=1.22)
        self.at("template pairs opposite")
        self.play(FadeOut(VGroup(peaks[:3], plot)), run_time=0.68)
        strand_y = 0.35
        above, above_ends = strand_cells("ACG".translate(COMPLEMENT), strand_y, reverse=True)
        template_bed = slab(9.2, 1.20, GREY, 0.95, strand_y, fill=0.28, stroke=0).set_z_index(-1)
        paired = VGroup(*(Line(xyz(t.get_x(), -0.92), xyz(t.get_x(), -0.34), color=GREY, stroke_width=4)
                          for t in first))
        self.at("opposite as")
        self.play(GrowFromEdge(template_bed, RIGHT), FadeIn(above_ends), run_time=0.60)
        self.play(LaggedStart(*(AnimationGroup(FadeIn(tile, shift=DOWN * 0.22), Create(link))
                                 for tile, link in zip(above, paired)), lag_ratio=0.72), run_time=2.55)
        self.at("written 5' to")
        self.play(FadeOut(paired), FadeOut(template_bed), run_time=0.32)
        # Lift the outer tiles onto separate paths to turn the strand
        # end-for-end while keeping each letter readable.
        reverse, reverse_ends = strand_cells("ACG".translate(COMPLEMENT)[::-1], strand_y)
        t, _, c = above
        self.play(t.animate.set_y(1.62), c.animate.set_y(2.82),
                  FadeOut(above_ends), run_time=0.46)
        self.play(t.animate.set_x(reverse[2].get_x()), c.animate.set_x(reverse[0].get_x()),
                  run_time=0.68)
        self.play(t.animate.set_y(strand_y), c.animate.set_y(strand_y),
                  FadeIn(reverse_ends), run_time=0.55)
        direction = Arrow(xyz(-3.20, 1.29), xyz(5.06, 1.29), buff=0, color=GOLD, stroke_width=6)
        self.at("that is c")
        self.play(GrowFromEdge(template_bed, LEFT, run_time=1.87), GrowArrow(direction, run_time=0.86))
        self.at("complementing without reversing")
        warning = badge("Not TGC", 0.78, -2.84, RED, size=36)
        slash = Line(warning.label.get_left() + LEFT * 0.04, warning.label.get_right() + RIGHT * 0.04,
                     color=RED, stroke_width=4).set_z_index(3)
        slash.layout_ok = "covered"  # Deliberate strike-through on the direction warning.
        struck_warning = VGroup(warning, slash)
        self.play(FadeIn(struck_warning, shift=UP * 0.20), run_time=0.38)
        self.at("backwards", lead=-0.50)
        self.play(FadeOut(struck_warning, shift=DOWN * 0.23), run_time=0.40)
        self.finish()


def long_trace(rough=0, accent=False):
    plot = Plot(box=(-5.85, 5.85, 0.42, 2.94), xr=(0, 12), yr=(0, 1), color=GREY)
    peaks = trace_peaks(plot, COPY + "GTACGT", rough=rough)
    if accent:
        for i, peak in enumerate(peaks):
            peak[0].set_fill(opacity=0.78 if i < rough else 0.68)
    return plot, peaks


def span_bracket(x0, x1, y, color):
    return VGroup(Line(xyz(x0, y), xyz(x1, y), color=color, stroke_width=3),
                  Line(xyz(x0, y), xyz(x0, y + 0.14), color=color, stroke_width=3),
                  Line(xyz(x1, y), xyz(x1, y + 0.14), color=color, stroke_width=3))


def repeated_genome():
    genome = slab(11.7, 1.14, GREY, 0, -2.53, fill=0.32)
    repeats = VGroup(*(slab(2.12, 0.93, TEAL, x, -2.53, fill=0.50) for x in (-3.85, 3.85)))
    unknowns = VGroup(*(label("?", x, -2.53, 34) for x in (-3.85, 3.85)))
    return VGroup(genome, repeats, unknowns)


class S09Limits(SpokenScene):
    def construct(self):
        plot, peaks, slots, cap = puzzle_picture()
        self.add(plot, peaks[:3], cap)
        wide, clean = long_trace()
        self.at("reads are accurate")
        self.play(FadeOut(cap), ReplacementTransform(plot, wide),
                  ReplacementTransform(peaks[:3], clean[:3]), run_time=1.20)
        self.play(LaggedStart(*(FadeIn(p) for p in clean[3:]), lag_ratio=0.18),
                  run_time=2.32)
        self.at("reads one region")
        length = span_bracket(-5.85, 5.85, 0.00, BLUE)
        self.play(Create(length), run_time=1.32)
        self.at("up to about")
        length_label = label("Schematic: 800 to 1,000 bases", 0, -0.55, 32)
        self.play(FadeIn(length_label, shift=UP * 0.15), run_time=0.62)
        self.at("800 to 1")
        self.play(LaggedStart(*(p[0].animate.set_fill(opacity=0.68) for p in clean),
                              lag_ratio=0.32), run_time=2.76)
        self.at("the first few dozen")
        _, noise = long_trace(rough=3)
        start = span_bracket(-5.85, -3.0, -1.06, RED)
        self.play(LaggedStart(*(ReplacementTransform(clean[i], noise[i])
                                for i in range(3)), lag_ratio=0.55), Create(start), run_time=2.06)
        poor = label("Poor first few dozen bases", -3.25, -1.58, 29, RED)
        self.at("often poor")
        self.play(FadeIn(poor, shift=UP * 0.14), run_time=0.82)
        self.at("cannot rely on the start")
        self.play(LaggedStart(*(p[0].animate.set_fill(opacity=0.78) for p in noise[:3]),
                              lag_ratio=0.55), run_time=1.85)
        self.at("reporting bases")
        genome = repeated_genome()
        self.play(FadeOut(VGroup(length, length_label, start, poor)), FadeIn(genome),
                  run_time=1.18)
        read = slab(2.08, 0.55, BLUE, -3.85, -1.38, fill=0.82)
        self.play(FadeIn(read, shift=DOWN * 0.35), run_time=0.58)
        self.at("across repeated genome")
        self.play(read.animate.set_x(3.85), run_time=1.07)
        self.play(read.animate.set_x(-3.85), run_time=0.93)
        self.finish()


def timeline():
    return slab(11.7, 0.76, GOLD, 0, -2.9, fill=0.25)


def year_tag(text, x):
    return badge(text, x, -2.03, GOLD, 30)


def quarter_century():
    return slab(8.78, 0.40, GOLD, -0.52, -2.90, fill=0.78, stroke=0)


def phage_picture():
    center = xyz(-3.21, -0.78)
    radius = 0.76
    ring = Circle(radius=radius, color=GREY, stroke_width=9).move_to(center)
    tiles = VGroup()
    for i, base in enumerate(COPY * 2):
        angle = PI / 2 - TAU * i / 12
        p = center + radius * xyz(np.cos(angle), np.sin(angle))
        tiles.add(slab(0.34, 0.26, BASE[base], *p[:2], fill=0.92, stroke=0).rotate(angle - PI / 2))
    return ring, tiles


class S10Unlocked1977(SpokenScene):
    def construct(self):
        plot, peaks = long_trace(rough=3, accent=True)
        genome = repeated_genome()
        self.add(plot, peaks, genome)
        self.at("in 1977")
        rail = timeline()
        self.play(FadeOut(genome), GrowFromEdge(rail, LEFT), run_time=1.25)
        year = year_tag("1977", -4.91)
        self.play(FadeIn(year, shift=UP * 0.15), run_time=0.62)
        self.at("published chain termination")
        names = label("Sanger, Nicklen & Coulson", 1.14, -0.65, 33)
        self.play(FadeIn(names, shift=UP * 0.15), run_time=1.12)
        self.at("dna from the phage")
        ring, tiles = phage_picture()
        self.play(Create(ring), run_time=0.64)
        phage = label("Phage φX174", 1.14, -1.36, 28)
        self.play(FadeIn(phage), LaggedStart(*(FadeIn(t, scale=0.6) for t in tiles),
                                             lag_ratio=0.32), run_time=2.85)
        self.at("it became the basis")
        span = quarter_century()
        self.play(GrowFromEdge(span, LEFT), run_time=3.02, rate_func=linear)
        self.at("next quarter century")
        era = label("Basis of most sequencing\nfor the next quarter century", 1.52, -0.64, 30)
        self.play(FadeOut(phage), swap(names, era, run_time=1.20))
        self.at("in 1980")
        prize_year = year_tag("1980", -2.73)
        self.play(FadeOut(VGroup(ring, tiles, era)), FadeIn(prize_year, shift=UP * 0.14),
                  run_time=1.20)
        self.at("shared half of")
        prize = label("Chemistry Nobel (shared)", -2.82, 0.01, 30)
        self.play(FadeIn(prize), run_time=0.62)
        self.at("walter gilbert")
        people = label("Frederick Sanger & Walter Gilbert", -2.35, -0.81, 29)
        self.play(FadeIn(people, shift=UP * 0.15), run_time=0.55)
        self.at("his second nobel")
        self.play(Indicate(prize_year, color=GOLD, scale_factor=1.08), run_time=1.13)
        self.finish()


def chromosome(y, finished=False):
    bed = slab(11.7, 0.91, GREY, 0, y, fill=0.28)
    blocks = VGroup()
    count = 20
    step = 11.20 / count
    for i in range(count):
        # Visible gaps are schematic. Their drawn width is not a coverage measurement.
        if i in ((6, 14) if finished else (2, 6, 9, 14, 16)):
            continue
        x = -5.60 + (i + 0.5) * step
        blocks.add(slab(step - (0.018 if finished else 0.08), 0.64, BASE[COPY[i % 6]],
                        x, y, fill=0.78, stroke=0))
    return bed, blocks


class S11UnlockedGenome(SpokenScene):
    def construct(self):
        plot, peaks = long_trace(rough=3, accent=True)
        rail = timeline()
        early = VGroup(year_tag("1977", -4.91), year_tag("1980", -2.73),
                       label("Chemistry Nobel (shared)", -2.82, 0.01, 30),
                       label("Frederick Sanger & Walter Gilbert", -2.35, -0.81, 29))
        span = quarter_century()
        self.add(plot, peaks, rail, span, early)
        self.at("fluorescent capillary")
        tubes = VGroup(*(slab(11.7, 0.44, BLUE, 0, y, fill=0.33) for y in (2.39, 1.56, 0.73)))
        self.play(FadeOut(early), FadeOut(span), run_time=0.40)
        self.play(ReplacementTransform(VGroup(plot, peaks), tubes), run_time=1.10)
        beads = VGroup(*(slab(0.58, 0.21, BASE[b], -5.12 + (i % 3) * 1.10,
                               2.39 - (i // 3) * 0.83, fill=0.95, stroke=0)
                         for i, b in enumerate(COPY)))
        bed, reads = chromosome(-0.55)
        self.at("produced most")
        self.play(FadeIn(beads), FadeIn(bed), run_time=0.43)
        self.play(beads.animate.shift(RIGHT * 7.95), run_time=1.83, rate_func=linear)
        self.at("february 2001")
        year = year_tag("February 2001", 1.27)
        self.play(FadeIn(year), FadeOut(beads, shift=DOWN * 0.58),
                  LaggedStart(*(FadeIn(b, shift=DOWN * 0.18) for b in reads), lag_ratio=0.14),
                  run_time=2.31)
        heading = label("2001 human genome drafts", 0, -1.29, 30)
        self.play(FadeIn(heading), run_time=0.56)
        self.at("sequencing consortium")
        consortium = badge("Consortium", -2.64, 0.62, BLUE)
        self.play(FadeOut(tubes), run_time=0.42)
        self.play(FadeIn(consortium, shift=DOWN * 0.24), run_time=0.77)
        self.at("celera genomics")
        celera = badge("Celera Genomics", 2.68, 0.62, BLUE)
        self.play(FadeIn(celera, shift=DOWN * 0.24), run_time=0.76)
        self.at("each published one")
        self.play(Indicate(consortium, color=BLUE, scale_factor=1.04),
                  Indicate(celera, color=BLUE, scale_factor=1.04), run_time=1.35)
        self.at("finished sequence")
        finished_year = year_tag("2004", 4.70)
        self.play(FadeOut(celera), FadeOut(heading), FadeIn(finished_year, shift=RIGHT * 0.20),
                  run_time=1.09)
        _, finished = chromosome(-0.55, finished=True)
        self.at("covered about 99")
        self.play(ReplacementTransform(reads, finished), run_time=1.08)
        coverage = label("About 99% of euchromatin", 0, -1.29, 31)
        self.play(FadeIn(coverage), run_time=0.66)
        self.at("euchromatin")
        gaps = VGroup(*(Line(xyz(x, -0.90), xyz(x, -0.20), color=RED, stroke_width=9)
                        for x in (-5.60 + 6.5 * 0.56, -5.60 + 14.5 * 0.56)))
        self.play(Create(gaps), run_time=0.48)
        self.at("one missing hydroxyl", lead=-0.20)
        track, p, stop = stopped_track()
        self.play(FadeOut(VGroup(rail, year, finished_year, coverage, consortium, gaps, bed, finished)),
                  run_time=0.40)
        self.play(FadeIn(VGroup(track, p, stop)), run_time=0.55)
        self.play(Indicate(stop[2], color=RED, scale_factor=1.20), run_time=0.66)
        self.at("into readable lengths")
        rows = ladder()
        self.play(FadeOut(VGroup(p, stop)), run_time=0.30)
        self.play(LaggedStart(*(FadeIn(row, shift=DOWN * 0.15) for row in rows), lag_ratio=0.17),
                  run_time=1.12)
        self.finish()


class S12End(EndCard):
    LINE = "Stopping copies at known bases turns DNA order into fragment length."
