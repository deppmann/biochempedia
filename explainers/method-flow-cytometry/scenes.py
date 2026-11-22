"""Reading and Sorting Cells One by One, timed to the supplied narration.

Colour map (from the patch-clamp film): BLUE apparatus, GREY structure,
YELLOW fluorescence from DNA, GREEN selective labels and counted cells,
RED contamination, ORANGE added stain, PURPLE independent fluorescence,
TEAL fluid and GOLD dates and the guiding rule.
"""
from bp_parts import *  # noqa: F403
from bp_style import EndCard

PURPLE = "#B58CD9"
ORANGE = "#F29E4C"
SCREEN = "#243346"
FLUID = "#204654"
DYE = "#FFCE57"
FLOW_Y = -0.8
LASER_X = -3.65
FORK_X = -2.65
OUT_X = -0.82
LESSON_TITLE = "Flow cytometry and cell sorting"
FILM_TITLE = "Reading and Sorting Cells One by One"
QUESTION = "Can DNA fluorescence alone\ntell these apart?"
FLOW_PERIOD = 0.34
FLOW_SPEED = 3.0
CROSSING_TIME = (1.6 + LASER_X + 5.56) / FLOW_SPEED
SURFACE_TAGS = (True, False, False, True, False, True, False, False, True)
PACKET_DNA = np.array([2.02, 3.47, 3.91, 2.13, 1.94, 4.07, 2.03, 2.62, 3.97])


def crossing_index(time):
    return int(np.floor((time - CROSSING_TIME) / FLOW_PERIOD))


def pos(x, y):
    return np.array([x, y, 0.0])


def label(text, x, y, size=30, color=TEXT):
    return T(text, size, color).move_to(pos(x, y))


def line(points, color=BLUE, width=3):
    return VMobject().set_points_as_corners([pos(*p) for p in points]).set_stroke(color, width)


def plate(x, y, width, height, color=SCREEN):
    return RoundedRectangle(
        width=width, height=height, corner_radius=0.22,
        stroke_color="#415367", stroke_width=2, fill_color=color, fill_opacity=1,
    ).move_to(pos(x, y))


def screen():
    return plate(3.02, 0.04, 7.20, 6.07)


def cell(color=TEAL, radius=0.33, shape=0, nuclear=0, tagged=False, nucleus_only=False):
    """Abstract cell and probe silhouettes, with no molecular geometry."""
    outline = Circle(radius=radius, color=color, stroke_width=3, fill_opacity=0.56)
    if shape == 1:
        outline.stretch(0.76, 1).rotate(0.43)
    if shape == 2:
        outline.stretch(0.75, 0).rotate(-0.50)
    if shape == 3:
        outline.stretch(0.80, 0).rotate(0.52)
    core = Circle(radius=radius * 0.55, stroke_width=0)
    core.set_fill(DYE if nuclear else color, nuclear or 0.33)
    if nucleus_only:
        outline.stretch(0.84, 1)
    g = VGroup(outline, core)
    if tagged:
        for angle in (0.35, 1.7, 3.25, 5.1):
            g.add(Dot(pos(radius * np.cos(angle), radius * np.sin(angle)),
                      radius=radius * 0.19, color=GREEN))
    return g


def chamber_geometry():
    """The reservoir, horizontal channel and orthogonal optical path share fixed landmarks."""
    inlet = [(-6.68, 2.95), (-4.70, 2.95), (-4.70, 1.03), (-4.94, 0.25),
             (-4.82, -0.34), (-2.83, -0.34), (-2.83, -1.26),
             (-5.72, -1.26), (-6.68, 0.60)]
    chamber = VGroup(
        Polygon(*[pos(*p) for p in inlet], stroke_width=0, fill_color=FLUID, fill_opacity=1),
        line(inlet[6:] + inlet[:6]),
    )
    fork_shape = [
        (-2.83, -0.34), (-2.54, -0.33), (-1.78, 0.40), (-0.74, 0.40),
        (-0.74, -0.30), (-1.52, -0.30), (-2.03, FLOW_Y),
        (-1.52, -1.30), (-0.74, -1.30), (-0.74, -2.00), (-1.78, -2.00),
        (-2.54, -1.27), (-2.83, -1.26),
    ]
    fork = VGroup(
        Polygon(*[pos(*p) for p in fork_shape], stroke_width=0, fill_color=FLUID, fill_opacity=1),
        line(fork_shape),
    )
    beam = VGroup(
        line([(LASER_X, -2.42), (LASER_X, 1.34)], BLUE, 13).set_stroke(opacity=0.22),
        line([(LASER_X, -2.42), (LASER_X, 1.34)], BLUE, 3.5),
        RoundedRectangle(width=0.92, height=0.43, corner_radius=0.12,
                         color=BLUE, stroke_width=3, fill_color=FLUID, fill_opacity=1)
        .move_to(pos(LASER_X, -2.43)),
    )
    detector = plate(-3.65, 1.57, 1.22, 0.52, FLUID).set_stroke(BLUE, width=3)
    channel = Polygon(pos(-2.87, -0.34), pos(OUT_X + 0.12, -0.34),
                      pos(OUT_X + 0.12, -1.26), pos(-2.87, -1.26),
                      stroke_width=0, fill_color=FLUID, fill_opacity=1)
    straight = VGroup(channel, line([(-2.87, -0.34), (OUT_X + 0.12, -0.34)]),
                      line([(-2.87, -1.26), (OUT_X + 0.12, -1.26)]))
    return VGroup(chamber, straight), fork, beam, detector


def tube_opacity(tube, opacity):
    tube[0].set_fill(opacity=opacity)
    for wall in tube[1:]:
        wall.set_stroke(opacity=opacity)


def flow(scene, mode="dna", sorting=False, laser=True, moving=True, phase=0.0,
         probes=None, isolate_for_sort=False):
    """Draw this film's hardware and animate packet crossings from one shared clock."""
    passage, fork, beam, detector = chamber_geometry()
    branch = ValueTracker(float(sorting))
    clock = ValueTracker(phase)
    if moving:
        clock.add_updater(lambda m, dt: m.increment_value(dt))
    kind = ValueTracker(0 if mode == "dna" else 1)
    dna_cells = VGroup()
    other_cells = VGroup()
    nuclei = VGroup()
    indices = range(len(SURFACE_TAGS))
    probe_amount = probes.get_value if probes is not None else lambda: 1

    for i in indices:
        dna_cells.add(cell(YELLOW, 0.325, i % 3, nuclear=PACKET_DNA[i] / 5.4))
        is_tagged = SURFACE_TAGS[i]
        tint = GREEN if is_tagged else GREY
        if mode == "mixed":
            tint = (TEAL, PURPLE, ORANGE)[i % 3]
        c = cell(tint, 0.32, i % 3,
                 tagged=is_tagged and mode == "tagged",
                 nuclear=0, nucleus_only=mode == "nuclei")
        other_cells.add(c)
        if isolate_for_sort:
            nuclei.add(cell(tint, 0.275, i % 3, nucleus_only=True))

    def relocate(c, i, variant):
        entry_phase = (clock.get_value() + FLOW_PERIOD * i) % (FLOW_PERIOD * len(indices))
        distance = entry_phase * FLOW_SPEED
        x, y = -5.56 + max(0, distance - 1.6), FLOW_Y
        if distance < 1.6:
            y = 2.20 - distance * 1.875
            x += 0.22 * np.sin(np.pi * distance / 1.6) * (1 if i % 2 else -1)
        if x > FORK_X:
            bend = np.clip((x - FORK_X) / 0.98, 0, 1)
            y += branch.get_value() * 0.85 * bend * (1 if SURFACE_TAGS[i] else -1)
        visibility = np.clip(min(distance / 0.4, (OUT_X - x) / 0.33), 0, 1)
        mixes = (
            1 - kind.get_value(),
            kind.get_value() * (1 - branch.get_value() if isolate_for_sort else 1),
            branch.get_value(),
        )
        c.move_to(pos(x if visibility else min(x, OUT_X), y))
        for j, part in enumerate(c):
            opacity = visibility * mixes[variant]
            if variant == 1 and mode == "tagged" and SURFACE_TAGS[i]:
                if j >= 2:
                    opacity *= probe_amount()
                else:
                    part.set_color(interpolate_color(ManimColor(GREY), ManimColor(GREEN), probe_amount()))
            part.set_stroke(opacity=opacity)
            part.set_fill(opacity=part.flow_fill * opacity)

    for variant, group in enumerate((dna_cells, other_cells, nuclei)):
        for i, c in enumerate(group):
            for part in c:
                part.flow_fill = part.get_fill_opacity()
            relocate(c, i, variant)
            if moving:
                c.add_updater(lambda m, i=i, variant=variant: relocate(m, i, variant))

    tube_opacity(passage[1], 1 - branch.get_value())
    if moving:
        passage[1].add_updater(lambda m: tube_opacity(m, 1 - branch.get_value()))
    flashes = VGroup()
    for color, is_dna in ((DYE, True), (GREEN, False)):
        light = Circle(radius=0.45, stroke_width=7, color=color).move_to(pos(LASER_X, FLOW_Y))
        signal = Dot(pos(LASER_X, FLOW_Y + 0.54), radius=0.105, color=color)

        def flash(group, is_dna=is_dna):
            d = (clock.get_value() - CROSSING_TIME) % FLOW_PERIOD
            i = -crossing_index(clock.get_value()) % len(indices)
            mix = ((1 - kind.get_value()) if is_dna
                   else kind.get_value() * SURFACE_TAGS[i] * probe_amount())
            group[0].set_stroke(opacity=mix * max(0, 1 - d / 0.19))
            group[1].move_to(pos(LASER_X, FLOW_Y + 0.55 + 1.72 * min(1, d / 0.29)))
            group[1].set_opacity(mix if d < 0.29 else 0)

        pair = VGroup(light, signal)
        flash(pair)
        if moving:
            pair.add_updater(flash)
        flashes.add(pair)

    world = VGroup(passage)
    tube_opacity(fork, float(sorting))
    if moving:
        fork.add_updater(lambda m: tube_opacity(m, branch.get_value()))
    world.add(fork)
    if laser:
        world.add(beam, detector)
    world.add(dna_cells, other_cells, nuclei)
    if laser:
        world.add(flashes)
    scene.add(clock, world)
    return branch, kind, clock


def scope():
    return scope_tag(size=24, color=TEXT).shift(LEFT * 0.20)


def mixed_pool():
    pool = VGroup(
        RoundedRectangle(width=6.4, height=5.5, corner_radius=0.70, color=BLUE,
                         stroke_width=4, fill_color=FLUID, fill_opacity=1).move_to(pos(-3.37, 0.28))
    )
    positions = [(-5.3, 1.78), (-3.12, 1.89), (-1.58, 1.23), (-4.4, 0.41),
                 (-2.69, 0.25), (-5.27, -1.25), (-3.39, -1.27), (-1.53, -1.36)]
    colors = (TEAL, PURPLE, ORANGE)
    cells = VGroup()
    for i, (x, y) in enumerate(positions):
        c = cell(colors[i % 3], 0.67, i % 4).move_to(pos(x, y))
        cells.add(c)
    return pool, cells


def title_flow(scene, phase=0.0):
    return flow(scene, mode="mixed", laser=False, phase=phase)


def stain_cell(x, amount):
    center = pos(x, 0.08)
    shell = Circle(radius=1.64, color=TEAL, stroke_width=5, fill_color=FLUID,
                   fill_opacity=1).move_to(center)
    nucleus = Circle(radius=0.92, color=GREY, stroke_width=3,
                     fill_color=SCREEN, fill_opacity=1).move_to(center)
    # Identical mark sizes and twice the number of marks distinguish 2C from 4C.
    dots = VGroup()
    for i in range(amount):
        angle = TAU * i / amount + PI / 4
        dots.add(Dot(center + 0.44 * pos(np.cos(angle), np.sin(angle)),
                     radius=0.17, color=DYE))
    floaters = VGroup()
    for i in range(7):
        angle = TAU * i / 7
        d = Dot(center + 1.27 * pos(np.cos(angle), np.sin(angle)), radius=0.10, color=ORANGE)
        floaters.add(d)
    return shell, nucleus, dots, floaters


# The schematic histogram encodes a diploid population: 2C and 4C centers
# with narrow measurement spread, and intermediate DNA values during S phase.
BINS = np.linspace(1.57, 4.43, 28)
DNA_SAMPLE = np.concatenate([
    2 + 0.114 * np.random.default_rng(7).standard_normal(116),
    4 + 0.120 * np.random.default_rng(8).standard_normal(61),
    np.linspace(2.17, 3.83, 43),
])
DNA_COUNTS = np.histogram(DNA_SAMPLE, BINS)[0]
def dna_plot(max_count=50):
    p = Plot((0.04, 6.28, -1.39, 1.68), (1.56, 4.44), (0, max_count),
             xticks=[(2, "2C"), (4, "4C")], xlabel="DNA fluorescence",
             label_size=28, size=28, color=TEXT)
    heading = label("Cell count", 1.19, 1.97)
    return p, heading


def hist_bars(plot, counts=DNA_COUNTS, opacity=0.89):
    bars = VGroup()
    for lo, hi, n in zip(BINS[:-1], BINS[1:], counts):
        base = plot.pt((lo + hi) / 2, 0)
        top = plot.pt((lo + hi) / 2, n)
        color = YELLOW if hi < 2.31 or lo > 3.69 else ORANGE
        bar = Rectangle(width=plot.pt(hi, 0)[0] - plot.pt(lo, 0)[0] - 0.018,
                        height=max(0.004, top[1] - base[1]), stroke_width=0,
                        fill_color=color, fill_opacity=opacity if n else 0)
        bars.add(bar.move_to((base + top) / 2))
    return bars


def peak_groups():
    p, header = dna_plot()
    low = label("G0 + G1", p.pt(2, 0)[0] + 0.15, -2.64, color=TEXT)
    high = label("G2 + M", p.pt(4, 0)[0] - 0.15, -2.64, color=TEXT)
    return p, header, low, high


def predict_card():
    return question_card(QUESTION, y=2.61, left=0.24, max_w=6.00, size=28)


def sorted_readout():
    rows = VGroup()
    for y, tagged, text, color in ((0.80, True, "Tagged", GREEN), (-0.95, False, "Untagged", TEXT)):
        sample = VGroup(*(cell(GREEN if tagged else GREY, 0.31, i, tagged=tagged) for i in range(3)))
        sample.arrange(RIGHT, buff=0.22).move_to(pos(1.40, y))
        rows.add(VGroup(sample, label(text, 4.47, y, size=34, color=color)))
    return rows


class S01Hook(SpokenScene):
    def construct(self):
        pool, cells = mixed_pool()
        card = question_card("How do you count or sort a mixture?", y=0.85, left=0.45, max_w=5.85, size=39)
        self.add(pool, cells, scope())
        for i, c in enumerate(cells):
            bob(c, amp=0.13, speed=2.0, seed=i)

        self.at("How do you")
        self.play(FadeIn(card), run_time=0.46)

        self.at("Bulk tests")
        positions = [pos(-5.51 + 0.62 * i, 0.46) for i in range(len(cells))]
        for c in cells:
            c.clear_updaters()
        bar = RoundedRectangle(width=5.03, height=0.47, corner_radius=0.18,
                               stroke_width=0, fill_color=GREY, fill_opacity=1).move_to(pos(-3.34, 0.46))
        self.play(*(c.animate.move_to(p).stretch(0.31, 1).set_color(GREY)
                    for c, p in zip(cells, positions)), run_time=0.65)
        self.play(ReplacementTransform(cells, bar), FadeOut(card), run_time=0.42)
        average = label("Bulk average", -3.34, 1.24, size=35)
        self.play(FadeIn(average), run_time=0.32)
        self.at("what single cells")
        self.play(FadeOut(bar), FadeOut(pool), FadeOut(average), run_time=0.38)
        title_flow(self)
        self.finish()


class S02Title(TitleCard):
    LESSON = LESSON_TITLE
    TITLE = FILM_TITLE

    def construct(self):
        # The existing two-second silent slot follows the narrated hook.
        _, _, beam, detector = chamber_geometry()
        title_flow(self, phase=1.1)
        lesson = label(self.LESSON, 0.72, 2.72, size=26, color=BLUE)
        title = T(self.TITLE.replace("Sorting Cells", "Sorting\nCells"), 50, font=TITLE_FONT,
                  line_spacing=0.70).move_to(pos(0.72, 1.37))
        self.play(FadeIn(beam), FadeIn(detector), FadeIn(lesson), FadeIn(title), run_time=0.36)
        self.wait(1.18)
        self.play(FadeOut(lesson), FadeOut(title), run_time=0.40)


class S03DnaStaining(SpokenScene):
    def construct(self):
        # A close-up of the inlet makes the DNA and RNA signals visible.
        self.add(plate(0, 0.03, 12.82, 5.96, FLUID), scope())
        left = stain_cell(-3.60, 2)
        middle = stain_cell(0, 4)
        right = stain_cell(3.60, 4)
        zoom = VGroup(*left[:2]).scale(0.81).shift(LEFT * 0.5)
        self.add(zoom)
        self.at("DNA content")
        self.play(zoom.animate.scale(1 / 0.81).shift(RIGHT * 0.5),
                  FadeIn(left[2][0]), run_time=2.05)
        pulse(left[0], base=5, amp=2.5, speed=2.6)
        bob(left[2][0], amp=0.075, speed=2.1)
        one = label("1C = one haploid genome", 0, 2.28, size=34, color=YELLOW)
        self.at("1C is")
        self.play(FadeIn(one), run_time=0.42)

        self.at("S -phase between")
        self.play(FadeOut(one), FadeIn(middle[0]), FadeIn(middle[1]), FadeIn(right[0]),
                  FadeIn(right[1]), FadeIn(left[2][1]), run_time=0.51)
        phase = label("S phase", 0, -2.12, size=32, color=YELLOW)
        self.play(FadeIn(phase), FadeIn(middle[2][0]), FadeIn(middle[2][1]), run_time=0.42)
        self.at("copies the DNA")
        self.play(LaggedStart(*[TransformFromCopy(middle[2][i], middle[2][i + 2])
                              for i in range(2)], lag_ratio=0.5), run_time=1.46)
        self.play(TransformFromCopy(middle[2], right[2]), run_time=0.55)
        left[2][0].clear_updaters()
        for i, part in enumerate((left[2], middle[2], right[2])):
            self.add(part)
            bob(part, amp=0.10, speed=2.35, seed=i)

        self.at("2C in G1")
        g1 = label("G1 · 2C", -3.6, -2.12, 33)
        self.play(FadeIn(g1), run_time=0.42)
        self.at("4C in G2")
        g2 = label("G2 / M · 4C", 3.6, -2.12, 33)
        self.play(FadeIn(g2), run_time=0.42)

        self.at("Stain fixed cells")
        dye = label("Propidium iodide", 0, 2.32, 35, ORANGE)
        for i, (shell, nucleus, dots, floaters) in enumerate((left, middle, right)):
            bob(floaters, amp=0.14, speed=2.1, seed=i)
        self.play(*(FadeIn(c[3], shift=DOWN * 0.25) for c in (left, middle, right)),
                  *(c[1].animate.set_fill(DYE, a) for c, a in zip((left, middle, right), (0.25, 0.39, 0.57))),
                  run_time=0.77)
        self.at("propidium iodide")
        self.play(FadeIn(dye), run_time=0.38)

        self.at("Add RNase")
        rnase = label("RNase removes RNA signal", 0, 2.32, 34, ORANGE)
        self.play(swap(dye, rnase), *(FadeOut(c[3]) for c in (left, middle, right)), run_time=0.95)
        self.finish()


class S04LaserHistogram(SpokenScene):
    def construct(self):
        branch, kind, clock = flow(self, phase=0.67)
        raster = screen()
        self.add(raster, scope())
        self.at("past a laser")
        laser = label("Laser", LASER_X, -3.02, size=28, color=BLUE)
        self.play(FadeIn(laser), run_time=0.38)

        self.at("Each flash builds")
        p, header = dna_plot(max_count=16)
        initial_crossing = crossing_index(clock.get_value())
        self.play(FadeIn(p), FadeIn(header), run_time=0.38)

        def collected_bars():
            latest = crossing_index(clock.get_value())
            events = range(initial_crossing + 1, latest + 1)
            sample = [PACKET_DNA[-i % len(PACKET_DNA)] for i in events]
            return hist_bars(p, np.histogram(sample, BINS)[0])

        bars = always_redraw(collected_bars)
        self.add(bars)
        self.at("2C peak")
        low = label("G1", p.pt(2, 0)[0] + 0.15, -2.64, color=YELLOW)
        self.play(FadeIn(low), run_time=0.30)
        self.at("4C peak")
        high = label("G2 / M", p.pt(4, 0)[0] - 0.15, -2.64, color=YELLOW)
        self.play(FadeIn(high), run_time=0.30)
        self.at("S phase between")
        sp = label("S phase", p.pt(3, 0)[0], -0.21, color=ORANGE)
        self.play(FadeIn(sp), run_time=0.35)

        self.at("The rule")
        rule = T("Read fluorescent tags on\nsingle cells to count or sort them.",
                 29, color=GOLD, line_spacing=0.68).move_to(pos(3.12, 2.40))
        self.play(FadeOut(header), FadeOut(low), FadeOut(high), run_time=0.36)
        self.play(FadeIn(rule), run_time=0.40)

        self.at("Swap in fluorescent")
        bars.clear_updaters()
        self.play(FadeOut(p), FadeOut(bars), FadeOut(sp), FadeOut(rule),
                  kind.animate.set_value(1), branch.animate.set_value(0.25), run_time=0.62)
        self.at("tagged cells separate")
        labels = sorted_readout()
        self.play(branch.animate.set_value(1), FadeIn(labels), run_time=0.69)
        self.finish()


class S05Predict(SpokenScene):
    def construct(self):
        branch, kind, _ = flow(self, mode="tagged", sorting=True, phase=20.87)
        labels = sorted_readout()
        p, header, low, high = peak_groups()
        bars = hist_bars(p)
        self.add(screen(), labels, scope())
        self.at("Look at that histogram")
        self.play(FadeOut(labels), branch.animate.set_value(0),
                  kind.animate.set_value(0), run_time=0.48)
        self.play(FadeIn(p), FadeIn(bars), FadeIn(header), run_time=0.54)
        self.at("Resting G0 cells")
        self.play(FadeIn(low, shift=RIGHT * 0.22), run_time=0.46)
        self.at("mitotic cells hold")
        self.play(FadeIn(high, shift=LEFT * 0.22), run_time=0.46)
        self.at("Can DNA fluorescence")
        self.play(FadeIn(predict_card()), run_time=0.52)
        self.finish()


class S06PredictPause(NarratedScene):
    def construct(self):
        flow(self, moving=False, phase=36.07)
        p, header, low, high = peak_groups()
        self.add(screen(), p, hist_bars(p), header, low, high, predict_card(), scope())
        self.wait(self.narration_s)


def extra_detector(x, color, clock, detects):
    housing = plate(x, 1.58, 0.98, 0.51).set_stroke(color, width=3)
    lamp = Dot(pos(x, 1.58), radius=0.14, color=color)

    def update(dot):
        t = clock.get_value() - 0.26
        i = -crossing_index(t) % len(PACKET_DNA)
        age = (t - CROSSING_TIME) % FLOW_PERIOD
        dot.set_opacity(0.18 + 0.82 * detects(i) * max(0, 1 - age / 0.17))

    lamp.add_updater(update)
    return housing, lamp


class S07AnswerStains(SpokenScene):
    def construct(self):
        _, _, clock = flow(self, phase=36.07)
        p, header, low, high = peak_groups()
        original = hist_bars(p)
        question = predict_card()
        self.add(screen(), p, original, header, low, high, question, scope())
        self.at("DNA content alone")
        self.play(FadeOut(question), run_time=0.42)

        self.at("A short EDU pulse")
        edu_sensor, edu_light = extra_detector(-2.33, GREEN, clock, lambda i: 2.25 < PACKET_DNA[i] < 3.75)
        self.play(FadeIn(edu_sensor), run_time=0.36)
        self.add(edu_light)
        edu = label("EdU", -2.33, 2.30, size=32, color=GREEN)
        self.play(FadeIn(edu), run_time=0.32)

        self.at("lifting S -phase")
        s_group = VGroup()
        remaining = np.histogram(DNA_SAMPLE[:177], BINS)[0]
        s_counts = DNA_COUNTS - remaining
        for lo, hi, n in zip(BINS[:-1], BINS[1:], s_counts):
            if n:
                x = p.pt((lo + hi) / 2, 0)[0]
                h = p.pt(2, n)[1] - p.pt(2, 0)[1]
                s_group.add(Rectangle(width=0.18, height=h, stroke_width=0,
                                      fill_color=GREEN, fill_opacity=0.90)
                            .move_to(pos(x, p.y0 + h / 2)))
        self.play(Transform(original, hist_bars(p, remaining)),
                  FadeIn(s_group), run_time=0.40)
        self.play(s_group.animate.shift(UP * 1.74), run_time=1.12)
        sl = label("S phase", 3.11, 0.97, color=GREEN)
        self.play(FadeIn(sl), run_time=0.34)

        self.at("An antibody to")
        ph_sensor, ph_light = extra_detector(-1.16, PURPLE, clock, lambda i: i in (2, 5))
        self.play(FadeIn(ph_sensor), run_time=0.42)
        self.add(ph_light)
        self.at("phosphorylated histone H3")
        histone = label("Phospho-H3", -2.10, 2.89, size=31, color=PURPLE)
        self.play(FadeIn(histone), run_time=0.37)
        self.at("marks mitotic chromosomes")
        mitotic = np.histogram(DNA_SAMPLE[116:153], BINS)[0]
        m_group = hist_bars(p, mitotic)
        for bar in m_group:
            bar.set_fill(PURPLE)
        self.play(FadeOut(high), FadeIn(m_group),
                  Transform(original, hist_bars(p, remaining - mitotic)), run_time=0.40)
        self.play(m_group.animate.shift(UP * 1.74), run_time=0.94)
        self.at("starting in late")
        late_g2 = hist_bars(p, np.histogram(DNA_SAMPLE[153:155], BINS)[0], opacity=0.43)
        late_g2.shift(UP * 1.74 + LEFT * 0.16)
        for bar in late_g2:
            bar.set_fill(PURPLE)
        self.add(late_g2)
        ml = label("M + late G2", 5.03, 2.42, 29, PURPLE)
        self.play(FadeIn(ml), run_time=0.40)

        self.at("Still no single stain")
        overlap = label("G0 + G1 overlap", 2.04, 2.70, size=32, color=YELLOW)
        self.play(swap(low, overlap), run_time=0.66)
        self.finish()


def peak(x, center):
    """Schematic intensity distribution with a common instrumental spread."""
    return np.exp(-0.5 * ((x - center) / 0.45) ** 2)


def matched_curves(plot, shift):
    a = plot.curve(lambda x: peak(x, 2.35), color=BLUE, width=8)
    b = plot.curve(lambda x: peak(x, shift), color=PURPLE, width=4)
    return VGroup(a, b)


def lock():
    hoop = Arc(radius=0.28, start_angle=0, angle=PI,
               color=GOLD, stroke_width=5).move_arc_center_to(pos(4.9, 0.57))
    body = plate(4.90, 0.42, 0.77, 0.58, "#493F2B").set_stroke(GOLD, width=3)
    hole = Dot(pos(4.90, 0.44), color=GOLD, radius=0.062)
    return VGroup(hoop, body, hole)


class S08Controls(SpokenScene):
    def construct(self):
        branch, _, clock = flow(self, mode="tagged", phase=0.75, isolate_for_sort=True)
        self.add(screen(), scope())
        controls = label("Controls", 3.1, 2.46, size=38, color=GOLD)
        self.at("Controls keep")
        self.play(FadeIn(controls), run_time=0.38)

        self.at("Comparing two cell lines")
        plot = Plot((0.15, 6.15, -1.17, 1.69), (0, 6), (0, 1.12),
                    xlabel="Tagged protein fluorescence", label_size=29, color=TEXT)
        match = ValueTracker(4.20)
        curves = always_redraw(lambda: matched_curves(plot, match.get_value()))
        keys = VGroup(label("Cell line A", 1.55, 1.91, size=29, color=BLUE),
                      label("Cell line B", 4.53, 1.91, size=29, color=PURPLE))
        self.play(FadeIn(plot), FadeIn(keys), run_time=0.47)
        self.add(curves)

        self.at("matched amounts of")
        self.play(match.animate.set_value(2.35), run_time=1.31)
        matched = label("Matched intensity", 4.49, 1.02, size=28, color=GREEN)
        self.play(FadeIn(matched), run_time=0.36)

        self.at("Amount alone")
        curves.clear_updaters()
        self.play(FadeOut(plot), FadeOut(keys), FadeOut(curves), FadeOut(matched), run_time=0.43)
        clump = VGroup(*[
            cell(GREEN, 0.47, tagged=True).move_to(pos(0.51 + 1.28 * i, -0.13 + 0.47 * (-1)**i))
            for i in range(5)
        ])
        self.play(FadeIn(clump), run_time=0.43)
        self.play(*(c.animate.move_to(pos(3.0 + 0.77 * np.cos(i * TAU / 5),
                                         0.12 + 0.77 * np.sin(i * TAU / 5)))
                    for i, c in enumerate(clump)), run_time=1.25)
        for i, c in enumerate(clump):
            bob(c, amp=0.078, speed=2.8, seed=i)

        self.at("When nuclei are sorted")
        meter = ValueTracker(0.75)
        gauge = dial(meter, center=pos(3.18, 0.13), radius=1.75, color=GREEN, fmt="")
        value = counter("{:.2f}", meter, pos(3.18, -0.52), size=31)
        gauge_label = label("Bulk average", 3.18, -1.13, size=30, color=GREEN)
        self.play(FadeOut(clump), branch.animate.set_value(1), run_time=0.48)
        self.play(FadeIn(gauge), FadeIn(value), FadeIn(gauge_label), run_time=0.39)

        self.at("stray nuclei skew")
        stray = cell(RED, 0.27, nucleus_only=True).move_to(pos(FORK_X, FLOW_Y))
        self.add(stray)
        self.play(stray.animate.move_to(pos(-1.63, -0.04)), run_time=0.64)
        self.play(stray.animate.move_to(pos(-0.98, -0.04)), meter.animate.set_value((4 * .75 + .10) / 5),
                  run_time=0.66)
        self.play(FadeOut(stray), run_time=0.21)

        self.at("And counting immune cells")
        value.clear_updaters()
        self.play(FadeOut(gauge), FadeOut(value), FadeOut(gauge_label), FadeOut(controls),
                  branch.animate.set_value(0), run_time=0.51)
        immune = label("Immune cells", 1.50, 1.52, size=31, color=GREEN)
        bar_bg = plate(1.50, -0.10, 0.72, 2.55, "#16222D").set_stroke(GREEN, width=3)
        start_counting = crossing_index(clock.get_value())

        def fill_count():
            current = crossing_index(clock.get_value())
            count = current - start_counting
            height = min(2.35, 0.18 + 0.29 * count)
            return RoundedRectangle(width=0.54, height=height, corner_radius=0.10,
                                    stroke_width=0, fill_color=GREEN, fill_opacity=1
                                    ).move_to(pos(1.50, -1.27 + height / 2))

        bar = always_redraw(fill_count)
        self.play(FadeIn(bar_bg), FadeIn(immune), run_time=0.37)
        self.add(bar)
        self.at("never measures protection")
        locked = lock()
        protection = label("Protection?", 4.90, 1.52, size=32, color=GOLD)
        endpoint = label("Separate endpoint", 4.90, -0.61, size=28)
        self.play(FadeIn(locked), FadeIn(protection), run_time=0.59)
        self.play(FadeIn(endpoint), run_time=0.34)
        self.finish()


# Northern Hemisphere summer means (Hua & Barbetti 2004, Table 7).
# Sparse annual means are interpolated for the schematic, with no donor measurements plotted.
CARBON_YEARS = [1955.5, 1956.5, 1957.5, 1958.5, 1959.5, 1960.5, 1961.5, 1962.5,
                1963.5, 1964.5, 1966.5, 1967.5, 1970.5, 1975.5, 1979.5, 1980.5, 1985.5, 1987.5, 1990.5]
CARBON_VALUES = [15, 20, 45, 148, 239, 222, 226, 337,
                 686, 785, 668, 618, 534, 387, 295, 270, 204, 187, 149]
BIRTH = 1967.5
LATER = 1979.5


def carbon(year):
    return np.interp(year, CARBON_YEARS, CARBON_VALUES)


def carbon_plot():
    plot = Plot((0.17, 6.17, -1.23, 1.56), (1955, 1992), (0, 850),
                xticks=[(1955.5, "1955"), (1975.5, "1975"), (1990.5, "1990")],
                xlabel="Calendar year", label_size=28, size=28, color=TEXT)
    heading = T("Atmospheric ¹⁴C", 32, color=GOLD).move_to(pos(3.08, 2.07))
    return plot, heading


def carbon_trace(plot):
    return plot.curve(carbon, x0=CARBON_YEARS[0], x1=CARBON_YEARS[-1], color=GOLD, width=6)


def time_pin(plot, year, color):
    return VGroup(
        DashedLine(plot.pt(year, 0.06), plot.pt(year, carbon(year)) + DOWN * 0.12,
                   color=color, stroke_width=3, dash_length=0.12),
        plot.dot(lambda: year, lambda: carbon(year), color=color, ring=TEXT, radius=0.12),
    )


def study(text):
    return label(text, 3.55, -2.60, size=28, color=TEXT)


def brain_stream(scene, sorting, phase):
    return flow(scene, mode="nuclei", sorting=sorting, phase=phase)


class S09UnlockedCortex(SpokenScene):
    def construct(self):
        branch, _, _ = brain_stream(self, sorting=False, phase=0.65)
        p, heading = carbon_plot()
        self.add(screen(), scope())
        sample = label("Brain nuclei", -4.36, 3.25, size=29)
        self.at("Sorting unlocked cell ages")
        self.play(FadeIn(sample), run_time=0.42)

        self.at("Weapons tests in")
        scan = ValueTracker(CARBON_YEARS[0])
        trace = p.live_curve(carbon, scan, color=GOLD, width=6, x0=CARBON_YEARS[0])
        self.play(FadeIn(p), FadeIn(heading), run_time=0.45)
        self.add(trace)
        self.play(scan.animate.set_value(1964.5), run_time=2.2, rate_func=linear)
        self.at("it later fell")
        self.play(scan.animate.set_value(CARBON_YEARS[-1]), run_time=1.92, rate_func=linear)

        self.at("A neuron stops dividing")
        stamp = cell(GREEN, 0.46, nucleus_only=True).move_to(pos(-4.47, -3.06))
        self.play(FadeIn(stamp), run_time=0.47)
        self.at("DNA keeps that")
        locked = label("¹⁴C held in DNA", -2.22, -3.08, size=28, color=GREEN)
        self.play(FadeIn(locked), run_time=0.48)

        self.at("In 2005")
        citation = study("Spalding et al. 2005")
        self.play(FadeIn(citation), FadeOut(stamp), FadeOut(locked), run_time=0.55)

        self.at("sorted nuclei with")
        self.play(branch.animate.set_value(1), run_time=1.15)
        self.at("new N")
        neuron = label("NeuN+", -1.64, 0.89, size=29, color=GREEN)
        non_neuron = label("NeuN−", -1.64, -2.46, size=29)
        self.play(FadeIn(neuron), FadeIn(non_neuron), run_time=0.41)

        self.at("Occipital cortex neurons")
        cortex = label("Occipital cortex", 3.62, 2.66, size=32, color=GREEN)
        self.play(FadeIn(cortex), run_time=0.51)
        self.at("as old as")
        pin = time_pin(p, BIRTH, GREEN)
        birth = label("Donor birth year", 3.81, 1.10, size=28, color=GREEN)
        self.play(Create(pin[0]), FadeIn(pin[1]), run_time=0.53)
        self.play(FadeIn(birth), run_time=0.33)
        self.finish()


class S10UnlockedHippocampus(SpokenScene):
    def construct(self):
        brain_stream(self, sorting=True, phase=28.25)
        p, heading = carbon_plot()
        trace = carbon_trace(p)
        pin = time_pin(p, BIRTH, GREEN)
        birth = label("Donor birth year", 3.81, 1.10, size=28, color=GREEN)
        sample = label("Brain nuclei", -4.36, 3.25, size=29)
        neuron = label("NeuN+", -1.64, 0.89, size=29, color=GREEN)
        non_neuron = label("NeuN−", -1.64, -2.46, size=29)
        cortex = label("Occipital cortex", 3.62, 2.66, size=32, color=GREEN)
        previous = study("Spalding et al. 2005")
        self.add(screen(), p, heading, trace, pin, birth, sample, neuron,
                 non_neuron, cortex, previous, scope())

        self.at("in the hippocampus")
        region = label("Hippocampus", 3.62, 2.66, size=32, color=GREEN)
        self.play(swap(cortex, region), run_time=0.50)

        self.at("In 2013")
        citation = study("Spalding et al. 2013")
        self.play(swap(previous, citation), run_time=0.55)
        self.at("fitted hippocampal carbon")
        y = ValueTracker(BIRTH)
        fitted = p.dot(y.get_value, lambda: carbon(y.get_value()),
                       color=PURPLE, ring=TEXT, radius=0.14)
        self.add(fitted)
        self.play(y.animate.set_value(LATER), pin.animate.set_opacity(0.35),
                  run_time=2.23, rate_func=linear)
        model = label("Turnover model", 4.73, 0.61, size=29, color=PURPLE)
        self.play(FadeIn(model), run_time=0.49)

        self.at("They estimated about")
        self.play(*(FadeOut(m) for m in (p, heading, trace, pin, fitted, birth, model)),
                  run_time=0.47)
        ratio = VGroup(*[
            plate(1.38 + 1.6 * i, 0.92, 1.39, 0.74, "#1D2A38").set_stroke(GREEN, width=3)
            for i in range(3)
        ])
        self.play(FadeIn(ratio), run_time=0.44)
        self.at("one -third of")
        fraction = label("≈ 1/3 renewing", 3.00, 0.15, size=34, color=GREEN)
        self.play(ratio[0].animate.set_fill(GREEN, 0.83), run_time=0.67)
        self.play(FadeIn(fraction), run_time=0.42)

        self.at("700 new ones")
        daily = label("≈ 700 new neurons/day", 3.0, -0.72, size=34, color=GREEN)
        per_region = label("per hippocampus", 3.0, -1.25, size=28)
        self.play(FadeIn(daily), run_time=0.48)
        self.at("per hippocampus per")
        self.play(FadeIn(per_region), run_time=0.39)

        self.at("The estimate rests")
        assumptions = label("Estimate depends on", 3.02, 1.17, size=31, color=GOLD)
        self.play(FadeOut(ratio), FadeOut(fraction), FadeOut(daily), FadeOut(per_region),
                  run_time=0.56)
        self.play(FadeIn(assumptions), run_time=0.35)
        self.at("pure sorting")
        purity = label("Pure sorting", 2.95, 0.43, size=30)
        self.play(FadeIn(purity), run_time=0.31)
        self.at("the model and")
        model_tag = label("Turnover model", 2.95, -0.30, size=30)
        self.play(FadeIn(model_tag), run_time=0.31)
        self.at("little DNA repair")
        repair = label("Little DNA repair", 2.95, -1.03, size=30)
        self.play(FadeIn(repair), run_time=0.32)
        self.finish()


def immune_stream(scene, phase, probes=None):
    return flow(scene, mode="tagged", phase=phase, probes=probes)


def dan_study():
    return study("Dan et al. 2021")


class S11UnlockedImmunity(SpokenScene):
    def construct(self):
        spike = ValueTracker(0)
        _, _, clock = immune_stream(self, 0.57, probes=spike)
        self.add(screen(), scope())
        self.at("In blood")
        blood = label("Blood cells", -4.60, 3.27, size=30, color=TEAL)
        self.play(FadeIn(blood), run_time=0.41)
        self.at("fluorescent viral spike")
        self.play(spike.animate.set_value(1), run_time=0.87)
        probe = label("Fluorescent spike probe", 3.03, 2.12, size=31, color=GREEN)
        self.play(FadeIn(probe), run_time=0.42)
        self.at("memory B cells")
        first_crossing = crossing_index(clock.get_value())

        def tally():
            current = crossing_index(clock.get_value())
            return sum(SURFACE_TAGS[-i % len(SURFACE_TAGS)] for i in range(first_crossing + 1, current + 1))

        readout = Readout([("Memory B cells", tally, "{:02.0f}", GREEN)], at=pos(3.03, 0.64),
                          size=34, widest=[99], color=GREEN)
        self.play(FadeIn(readout), run_time=0.52)
        self.at("In 2021")
        self.play(FadeIn(dan_study()), run_time=0.49)
        self.at("188 people")
        people = label("188 people", 3.03, -0.65, size=35)
        self.play(FadeIn(people), run_time=0.45)
        self.at("eight months after")
        months = label("Up to 8 months", 3.03, -1.37, size=31)
        self.play(FadeIn(months), run_time=0.45)
        self.finish()


def immunity_plots():
    upper = Plot((0.20, 6.03, 0.61, 1.78), (1, 6), (0, 1.30), color=TEXT)
    lower = Plot((0.20, 6.03, -1.44, -0.13), (1, 6), (0, 1.30),
                 xticks=[(1, "1"), (6, "6")], xlabel="Months after symptoms",
                 label_size=28, size=28, color=TEXT)
    return upper, lower


def antibody_trend(month):
    # Dan et al. 2021, Fig. 1A: cross-sectional exponential fit, 140-day half-life.
    return 2 ** (-30.44 * (month - 1) / 140)


def memory_trend(month):
    # A qualitative endpoint comparison from Dan et al. 2021, Fig. 2D.
    # The vertical placement is schematic and does not encode the fold change.
    return np.interp(month, [1, 6], [0.21, 1.15])


class S11bUnlockedImmunityResult(SpokenScene):
    def construct(self):
        immune_stream(self, 16.66)
        upper, lower = immunity_plots()
        scan = ValueTracker(1)
        antibody = upper.live_curve(antibody_trend, scan, color=BLUE, width=7)
        old = label("Plasma spike antibody", 2.96, 2.21, size=30, color=BLUE)
        citation = dan_study()
        self.add(screen(), upper, old, antibody, citation, scope(),
                 label("Blood cells", -4.60, 3.27, size=30, color=TEAL))
        self.at("Plasma spike antibody")
        self.play(scan.animate.set_value(6), run_time=4.34, rate_func=linear)

        self.at("Yet spike -specific")
        month = ValueTracker(1)
        memory = lower.live_curve(memory_trend, month, color=GREEN, width=7)
        heading = label("Spike-specific memory B cells", 3.1, 0.25, size=29, color=GREEN)
        self.play(FadeIn(lower), FadeIn(heading), run_time=0.36)
        self.add(memory)
        self.play(month.animate.set_value(2.2), run_time=1.34, rate_func=linear)
        self.at("more abundant at")
        self.play(month.animate.set_value(6), run_time=2.14, rate_func=linear)

        self.at("One cell at a time")
        for curve in (antibody, memory):
            curve.clear_updaters()
        self.play(FadeOut(antibody), FadeOut(upper), FadeOut(old), run_time=0.47)
        self.play(FadeOut(memory), FadeOut(lower), FadeOut(heading), FadeOut(citation),
                  run_time=0.51)
        final = label("One cell at a time", 3.04, 0.39, size=43, color=GOLD)
        self.play(FadeIn(final), run_time=0.46)
        self.finish()


class S12End(EndCard):
    LINE = "Read fluorescent tags on single cells to count or sort them."
