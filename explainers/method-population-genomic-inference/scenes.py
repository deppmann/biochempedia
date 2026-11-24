"""Reading History and Selection from Genomes.

BLUE: African / modern-human lineage. TEAL: Eurasian lineage.
PURPLE: Neanderthal lineage. GREY: chimpanzee and tree scaffolding.
YELLOW: neutral marks and observed difference. GREEN: corrected distance.
ORANGE: hidden changes, derived B, introgression and the finch comparison. RED: departures
and limits. GOLD: clock calibration and prediction.
"""

from bp_parts import *
from bp_style import EndCard

PURPLE = "#B58CD9"
ORANGE = "#F29E4C"
SLATE = "#26384B"
PANEL_EDGE = "#41596C"

NAMES = ("African", "Eurasian", "Neanderthal", "Chimpanzee")
COLORS = (BLUE, TEAL, PURPLE, TEXT)
TIP_X = (-5.12, -3.38, -1.64, 0.1)
ROW_Y = (-0.79, -1.44, -2.09, -2.74)
SITE_X = (-2.71, -2.02, -1.33, -0.64, 0.05, 0.74)
B_SITES = (2, 4)
QUESTION = "Without gene flow, who shares B more?"
QUESTION_CARD = {"y": 3.4, "size": 34}


def point(x, y):
    return np.array([x, y, 0.0])


def label(words, x, y, color=TEXT, size=32, **kwargs):
    return T(words, size, color, **kwargs).move_to(point(x, y))


def path(coords, color, width=8):
    return VMobject(stroke_color=color, stroke_width=width).set_points_as_corners(
        [point(x, y) for x, y in coords]
    )


def stage(x, y, width, height):
    return RoundedRectangle(
        width=width, height=height, corner_radius=0.24,
        stroke_color=PANEL_EDGE, stroke_width=2, fill_color=SLATE, fill_opacity=1,
    ).move_to(point(x, y)).set_z_index(-2)


def main_stage():
    return stage(-2.49, -0.08, 8.14, 6.16)


def side_stage():
    return stage(4.28, -0.08, 4.54, 6.16)


def schematic():
    return scope_tag(size=28, color=TEXT).set_y(-3.52)


def cell(x, y, color=GREY, opacity=0.23, width=0.57, height=0.46):
    return RoundedRectangle(
        width=width, height=height, corner_radius=0.07,
        stroke_width=0, fill_color=color, fill_opacity=opacity,
    ).move_to(point(x, y))


def genome(row, name=None, mode="plain"):
    """The row slots and aligned sites stay fixed throughout the film."""
    y = ROW_Y[row]
    color = COLORS[row]
    name = label(name or NAMES[row], 0, y, color, 28)
    name.align_to(point(-5.89, y), LEFT)
    swatch = Dot(point(-6.18, y), radius=0.078, color=color)
    cells = VGroup(*[
        cell(x, y, opacity=0.09 if mode == "derived" and i not in B_SITES else 0.27)
        for i, x in enumerate(SITE_X)
    ])
    return VGroup(swatch, name, cells)


def bar_mark(row, i, color=YELLOW):
    return cell(SITE_X[i], ROW_Y[row], color, 1, width=0.16, height=0.35)


def allele(row, i, letter, color):
    return label(letter, SITE_X[i], ROW_Y[row], color, 30, weight=BOLD)


def alleles(mode):
    if mode == "ancestral":
        return VGroup(*(allele(row, 1, "A", TEXT) for row in (3, 2, 1, 0)))
    return VGroup(*(allele(2, i, "B", ORANGE) for i in B_SITES))


def tree(variant="four"):
    """The leaf columns, stem and internal junctions share fixed landmarks."""
    a, e, n, c = TIP_X
    sister = (a + e) / 2
    older = (sister + n) / 2
    root = (older + c) / 2
    if variant == "clock":
        return VGroup(
            path([(older, 2.68), (older, 1.38)], GREY),
            path([(older, 1.38), (a, 1.38), (a, 0.48)], BLUE),
            path([(older, 1.38), (n, 1.38), (n, 0.48)], PURPLE),
        )
    shared = path([(older, 1.38), (sister, 1.38), (sister, 0.91)], BLUE)
    african = path([(sister, 0.91), (a, 0.91), (a, 0.48)], BLUE)
    eurasian = path([(sister, 0.91), (e, 0.91), (e, 0.48)], TEAL)
    neanderthal = path([(older, 1.38), (n, 1.38), (n, 0.48)], PURPLE)
    if variant == "hook":
        return VGroup(path([(older, 2.68), (older, 1.38)], GREY), shared,
                      african, eurasian, neanderthal)
    return VGroup(
        path([(root, 2.68), (root, 2.02), (older, 2.02), (older, 1.38)], GREY),
        shared, african, eurasian, neanderthal,
        path([(root, 2.02), (c, 2.02), (c, 0.48)], GREY),
    )


def bridge():
    return DashedVMobject(
        ArcBetweenPoints(point(TIP_X[2], 1.01), point(TIP_X[1], 0.66), angle=-0.9,
                         color=ORANGE, stroke_width=8),
        num_dashes=10, dashed_ratio=0.62,
    )


def tree_flash(branch, color=TEXT, width=15, halo_width=126):
    halo = branch.copy().set_stroke(color, width=halo_width, opacity=0.65)
    halo.set_cap_style(CapStyleType.ROUND)
    halo.set_z_index(-1)
    core = branch.copy().set_stroke(TEXT, width=width, opacity=0.94)
    return AnimationGroup(
        ShowPassingFlash(halo, time_width=0.88),
        ShowPassingFlash(core, time_width=0.88),
    )


def scan_sites(first_row, last_row, color=BLUE):
    """Sweep the aligned sites together, as a single comparison window."""
    height = ROW_Y[first_row] - ROW_Y[last_row] + 0.51
    y = (ROW_Y[first_row] + ROW_Y[last_row]) / 2
    window = cell(SITE_X[0], y, color, 0.63, width=0.90, height=height).set_z_index(-1)
    return Succession(FadeIn(window, run_time=0.25),
                      window.animate(run_time=2.1, rate_func=linear).set_x(SITE_X[-1]),
                      FadeOut(window, run_time=0.25))


def clock_progress(tracker):
    """The bar and its count both track the same accumulated neutral ticks."""
    track = cell(4.28, -2.17, GREY, 0.32, width=3.68, height=0.67)

    def fill():
        width = 3.68 * tracker.get_value() / 12
        return cell(2.44 + width / 2, -2.17, YELLOW, 1, width=width, height=0.55)

    return track, always_redraw(fill)


def clock_axis(ticks, years=False):
    axis = Arrow(point(-6.04, 2.49), point(-6.04, 0.26), buff=0,
                 stroke_width=4, color=GOLD, tip_length=0.14)
    marks = VGroup(*(
        Line(point(-6.18, y), point(-5.9, y), color=GOLD, stroke_width=4)
        for y in ticks
    ))
    title = label("Years" if years else "Time", -5.96, 2.69, GOLD, 28)
    return VGroup(axis, marks, title)


def calibration():
    x = ((TIP_X[0] + TIP_X[1]) / 2 + TIP_X[2]) / 2
    marker = Circle(radius=0.17, color=GOLD, stroke_width=4,
                    fill_color=SLATE, fill_opacity=1).move_to(point(x, 1.38))
    date = boxed_label("Dated split", GOLD, size=29).move_to(point(-1.32, 2.29))
    return VGroup(marker, date)


def tally():
    """An unnumbered schematic of equally scaled tallies."""
    labels = VGroup(label("African", 4.28, 1.72, BLUE),
                    label("Eurasian", 4.28, -0.37, TEAL))
    tracks = VGroup(cell(4.28, 1.02, GREY, 0.33, 3.70, 0.62),
                    cell(4.28, -1.07, GREY, 0.33, 3.70, 0.62))
    return VGroup(labels, tracks)


def tally_fill(row, width):
    y = (1.02, -1.07)[row]
    return cell(2.43 + width / 2, y, COLORS[row], 1, width, 0.46)


def tally_baseline():
    return VGroup(*(DashedLine(point(4.75, y - 0.48), point(4.75, y + 0.36),
                              color=TEXT, stroke_width=4, dash_length=0.11)
                    for y in (1.02, -1.07)))


def prediction_world():
    return VGroup(main_stage(), side_stage(), tree(),
                  VGroup(*(genome(i, mode="derived") for i in range(4))),
                  alleles("derived"), tally(), schematic())


def difference_plot():
    return Plot(box=(2.50, 6.20, -1.48, 2.30), xr=(0, 2), yr=(0, 0.42),
                color=TEXT, stroke=3)


def distance(p):
    """Jukes–Cantor correction used for the two examples in the lesson."""
    return -0.75 * np.log1p(-4 * p / 3)


def difference_bar(plot, x, value, color):
    bottom = plot.pt(x, 0)
    height = plot.pt(x, value)[1] - bottom[1]
    return Rectangle(width=0.90, height=height, stroke_width=0,
                     fill_color=color, fill_opacity=0.92).move_to(bottom + UP * height / 2)


def baseline_meter():
    plot = Plot(box=(2.53, 6.15, -1.39, 2.1), xr=(0, 1), yr=(0, 1),
                color=GREY)
    baseline = plot.hline(0.4, color=YELLOW)
    title = label("Neutral baseline", 4.32, -0.45, YELLOW, 28)
    rise = difference_bar(plot, 0.61, 0.80, RED)
    rise.stretch_to_fit_height(plot.pt(0, 0.80)[1] - plot.pt(0, 0.40)[1])
    rise.move_to((plot.pt(0.61, 0.80) + plot.pt(0.61, 0.40)) / 2)
    return plot, baseline, title, rise


def bird(x, y, scale, color):
    """Filled finch silhouette for a qualitative size comparison."""
    body = Ellipse(width=1.56, height=0.97, color=color, stroke_width=0,
                   fill_opacity=1).rotate(0.29).shift(LEFT * 0.15)
    head = Circle(radius=0.39, color=color, stroke_width=0, fill_opacity=1)
    head.move_to(point(0.48, 0.40))
    bill = Polygon(point(0.71, 0.61), point(1.18, 0.46), point(0.72, 0.24),
                   color=YELLOW, stroke_width=0, fill_opacity=1)
    tail = Polygon(point(-0.52, 0.02), point(-1.23, -0.24), point(-1.08, -0.52),
                   point(-0.47, -0.33), color=color, stroke_width=0, fill_opacity=1)
    legs = VGroup(path([(-0.25, -0.32), (-0.29, -0.69), (-0.04, -0.69)], color, 5),
                  path([(0.04, -0.30), (0.03, -0.65), (0.26, -0.65)], color, 5))
    eye = Dot(point(0.60, 0.53), radius=0.055, color=BG)
    return VGroup(tail, legs, body, head, bill, eye).scale(scale).move_to(point(x, y))


class S01Hook(TitleCard, SpokenScene):
    TITLE = "Reading History and Selection from Genomes"
    LESSON = "Population Genomic Inference"

    def construct(self):
        branches = tree("hook")
        strips = VGroup(*(genome(i) for i in range(3)))
        title = fit_text(self.TITLE, max_w=12.5, size=35, min_size=28,
                         font=TITLE_FONT).move_to(point(0, 3.43))
        question = question_card("Date splits from DNA?", y=3.43, size=35)
        self.add(main_stage(), branches, strips, schematic())
        self.at("how can genomes")
        self.add(title)
        self.play(tree_flash(branches[0], BLUE, halo_width=60), run_time=0.60)
        self.play(swap(title, question, run_time=0.44))
        self.at("date splits that", lead=0)
        self.play(tree_flash(branches[2], BLUE), run_time=1.75)
        self.at("spot selection")
        self.play(tree_flash(branches[3], TEAL), run_time=1.15)

        self.at("our species arose")
        self.play(FadeOut(question), tree_flash(branches[2], BLUE),
                  scan_sites(0, 2, BLUE), run_time=2.62)
        self.at("outside africa")
        self.play(tree_flash(branches[3], TEAL), run_time=1.25)
        thread = bridge()
        self.at("little neanderthal dna")
        self.play(Create(thread), tree_flash(branches[4], PURPLE), run_time=1.15)
        self.play(scan_sites(0, 2, ORANGE), run_time=1.9)
        self.at("genomes record history")
        marks = VGroup(*(bar_mark(r, i) for r, i in ((0, 1), (1, 2), (2, 2), (0, 4), (2, 5))))
        self.play(LaggedStart(*(GrowFromCenter(m) for m in marks), lag_ratio=0.65),
                  scan_sites(0, 2, YELLOW), run_time=1.4)
        self.at("the sites where")
        self.play(FadeIn(label("Variants", 4.27, -1.45, YELLOW, 38)), run_time=0.68)
        self.finish()


class S02NeutralClock(SpokenScene):
    def construct(self):
        branches = tree("clock")
        axis = clock_axis((2.25, 1.90, 1.55, 1.20, 0.85, 0.50))
        strips = VGroup(genome(0, "Modern human"), genome(2))
        marks = [bar_mark(r, i) for i in range(6) for r in (0, 2)]
        neutral = label("Neutral changes", 4.28, 1.95, YELLOW, 33)
        active = ValueTracker(4)
        count = counter("{:.0f} neutral ticks", active, point(4.28, -1.48),
                        size=28, color=YELLOW)
        self.add(main_stage(), side_stage(), branches, strips, schematic())
        self.at("start with neutral changes")
        self.play(Create(axis[0]), FadeIn(axis[2]), run_time=0.8)
        self.play(LaggedStart(*(GrowFromCenter(m) for m in marks[:4]), lag_ratio=0.85),
                  run_time=1.35)
        self.at("no effect on survival")
        self.play(Write(neutral), run_time=0.95)
        self.play(LaggedStart(*(Create(t) for t in axis[1]), lag_ratio=0.65),
                  tree_flash(branches[1], BLUE), run_time=2.45)
        self.at("on average")
        track, fill = clock_progress(active)
        self.add(count, track, fill)
        for m in marks[4:]:
            m.save_state()
            m.scale(0.02)
            m.set_opacity(0)
        self.play(LaggedStart(*(Restore(m) for m in marks[4:8]), lag_ratio=1),
                  active.animate.set_value(8), run_time=3.35, rate_func=linear)
        self.at("whatever the population size")
        self.play(LaggedStart(*(Restore(m) for m in marks[8:10]), lag_ratio=1),
                  active.animate.set_value(10), tree_flash(branches[1], BLUE),
                  run_time=2.0, rate_func=linear)

        k = label("K  (substitution rate)", 4.28, 0.91, YELLOW, 28)
        equals = label("=", 4.28, 0.24, TEXT, 37)
        mu = label("μ  (mutation rate)", 4.28, -0.43, YELLOW, 29)
        self.at("the substitution rate")
        self.play(FadeOut(neutral), FadeIn(k), tree_flash(branches[1], BLUE), run_time=1.25)
        self.at("equals the mutation rate")
        self.play(Write(equals), run_time=0.37)
        self.play(FadeIn(mu), tree_flash(branches[2], PURPLE), run_time=1.95)
        self.at("neutral differences pile up")
        self.play(LaggedStart(*(Restore(m) for m in marks[10:]), lag_ratio=1),
                  active.animate.set_value(12), run_time=1.75, rate_func=linear)
        self.at("one dated split")
        marker, date = calibration()
        self.play(GrowFromCenter(marker), run_time=0.45)
        self.play(FadeIn(date), run_time=0.55)
        year_ticks = clock_axis((2.25, 1.90, 1.55, 1.20, 0.85, 0.50), years=True)
        self.play(swap(axis[2], year_ticks[2], run_time=0.64),
                  LaggedStart(*(tree_flash(t, YELLOW, width=8, halo_width=23) for t in axis[1]),
                              lag_ratio=0.28), run_time=1.23)
        self.finish()


class S03HiddenChanges(SpokenScene):
    def construct(self):
        strips = VGroup(genome(0, "Modern human"), genome(2))
        branches = tree("clock")
        plot = difference_plot()
        self.add(main_stage(), side_stage(), branches, strips, schematic())
        x = SITE_X[2]
        target = cell(x, ROW_Y[2], YELLOW, 1, width=0.17, height=0.36)
        self.add(target)
        self.at("over long spans")
        upper_y, lower_y = 1.50, -0.27
        upper, lower = strips
        reference = bar_mark(0, 2)
        self.add(reference)
        self.play(FadeOut(branches), run_time=0.48)
        self.play(upper.animate.set_y(upper_y), lower.animate.set_y(lower_y),
                  reference.animate.set_y(upper_y), target.animate.set_y(lower_y),
                  run_time=1.22)
        self.at("change twice")
        focus = cell(x, (upper_y + lower_y) / 2, GOLD, 0.58,
                     width=0.59, height=2.38).set_z_index(-1)
        self.play(target.animate.set_color(ORANGE), FadeIn(focus), run_time=0.62)
        self.play(target.animate.set_fill(YELLOW, opacity=1), run_time=0.85)
        self.play(FadeOut(focus), run_time=0.58)
        hidden = label("Two changes at one site", -2.48, -2.12, TEXT)
        self.play(FadeIn(hidden), run_time=0.7)

        self.at("observed difference p")
        self.play(Create(plot), run_time=1.22)
        observed = label("Observed difference", -2.48, 2.40, YELLOW, 34)
        corrected = label("Corrected distance", -2.48, 2.40, GREEN, 34)
        p_name = label("p", 3.43, -1.91, YELLOW, 38)
        d_name = label("D", 5.28, -1.91, GREEN, 38)
        self.play(FadeIn(observed), FadeIn(p_name), run_time=0.55)
        self.at("corrected into distance")
        low_zone = cell(4.35, -1.29, GREEN, 0.38, width=3.42, height=0.27).set_z_index(-1)
        self.play(swap(observed, corrected, run_time=0.95), FadeIn(d_name),
                  FadeIn(low_zone), run_time=1.35)

        p, d = 0.012, distance(0.012)
        p_bar = difference_bar(plot, 0.5, p, YELLOW)
        d_bar = difference_bar(plot, 1.5, d, GREEN)
        p_val = label(f"{p:.3f}", 3.43, -0.90, YELLOW, 29)
        d_val = label(f"{d:.4f}", 5.28, -0.90, GREEN, 29)
        self.at("for small p")
        match = cell(x, (upper_y + lower_y) / 2, YELLOW, 0.56,
                     width=0.79, height=2.38).set_z_index(-1)
        self.play(GrowFromEdge(p_bar, DOWN), GrowFromEdge(d_bar, DOWN), GrowFromEdge(match, UP),
                  run_time=0.9)
        self.play(FadeIn(p_val), FadeIn(d_val), run_time=0.75)
        self.play(FadeOut(match), run_time=0.43)
        self.at("at p of 0 .30", lead=0.4)
        p, d = 0.30, distance(0.30)
        self.play(FadeOut(p_val, run_time=0.28), FadeOut(d_val, run_time=0.28),
                  FadeOut(low_zone, run_time=0.28),
                  Transform(p_bar, difference_bar(plot, 0.5, p, YELLOW), run_time=0.65))
        self.add(label(f"{p:.2f}", 3.43, 1.55, YELLOW, 29))
        self.at("d is 0 .383", lead=0.4)
        d_readout = label(f"{d:.3f}", 5.28, 2.30, GREEN, 29)
        self.play(LaggedStart(
            Transform(d_bar, difference_bar(plot, 1.5, d, GREEN), run_time=0.65),
            FadeIn(d_readout, run_time=0.18), lag_ratio=0.52,
        ))

        self.at("d over p")
        ratio = label(f"D ÷ p = {d:.3f} ÷ {p:.2f} ≈ {d / p:.2f}", -2.48, -1.62,
                      TEXT, 34)
        self.play(swap(hidden, ratio, run_time=1.85))
        self.at("over a quarter more")
        p_level = DashedLine(
            plot.pt(0.5, p) + RIGHT * p_bar.width / 2,
            plot.pt(1.5, p) + LEFT * d_bar.width / 2,
            color=TEXT, stroke_width=3, stroke_opacity=0.60, dash_length=0.09,
        )
        gap = Line(plot.pt(1.5, p), plot.pt(1.5, d), color=ORANGE, stroke_width=17)
        self.play(Create(p_level), Create(gap), run_time=1.2)
        self.finish()


class S04FourGenomes(SpokenScene):
    def construct(self):
        clock = tree("clock")
        world = tree()
        modern = genome(0, "Modern human")
        ancient = genome(2)
        plot, base, base_label, rise = baseline_meter()
        self.add(main_stage(), side_stage(), clock, modern, schematic(), plot, base)
        self.at("departures from this neutral baseline")
        self.play(GrowFromEdge(rise, DOWN), run_time=1.8)
        self.play(FadeIn(base_label), tree_flash(clock[1], BLUE), run_time=0.75)
        selection = label("Selection?", 4.28, -2.14, RED)
        self.play(FadeIn(selection), run_time=0.75)
        self.at("or to gene flow")
        flow = label("Gene flow?", 4.28, -2.14, ORANGE)
        self.play(swap(selection, flow, run_time=0.9))
        thread = bridge()
        hook = tree("hook")
        self.play(ReplacementTransform(clock, hook), run_time=0.62)
        self.play(Create(thread), tree_flash(hook[4], PURPLE), run_time=1.58)
        clock = tree("clock")
        self.play(FadeOut(thread), ReplacementTransform(hook, clock), run_time=0.65)
        self.at("ancient dna")
        self.play(FadeOut(plot), FadeOut(base), FadeOut(base_label), FadeOut(rise), FadeOut(flow),
                  run_time=0.42)
        marrow = RoundedRectangle(width=1.35, height=0.27, corner_radius=0.13,
                                  color=ORANGE, fill_opacity=1, stroke_width=0)
        ends = VGroup(*(Circle(radius=0.20, stroke_width=0, fill_color=ORANGE,
                               fill_opacity=1).move_to(point(x, y))
                        for x in (-0.62, 0.62) for y in (-0.10, 0.10)))
        bone = VGroup(marrow, ends).rotate(0.35).move_to(point(4.28, 0.44))
        self.play(GrowFromCenter(bone), run_time=0.70)
        self.at("from bones tens")
        self.play(Transform(bone, ancient[2].copy()), run_time=2.05)
        self.add(ancient[2])
        self.remove(bone)
        self.at("compared with living genomes")
        self.play(FadeIn(ancient[0]), FadeIn(ancient[1]), run_time=0.7)
        self.play(tree_flash(clock[1], BLUE), scan_sites(0, 2, BLUE), run_time=1.6)

        self.at("place four genomes")
        self.play(ReplacementTransform(clock, world), run_time=1.08)
        african, eurasian, chimp = genome(0), genome(1), genome(3)
        self.play(swap(modern[1], african[1], run_time=0.85))
        self.at("eurasian neanderthal")
        self.play(FadeIn(eurasian), tree_flash(world[3], TEAL), run_time=1.1)
        self.at("chimpanzee outgroup")
        self.play(FadeIn(chimp), run_time=0.55)
        outgroup = boxed_label("Outgroup", TEXT, size=28).move_to(point(4.28, 0.96))
        self.play(FadeIn(outgroup), tree_flash(world[5], TEXT), run_time=1.07)
        self.at("marks each site's older")
        marks = alleles("ancestral")
        column = cell(SITE_X[1], (ROW_Y[0] + ROW_Y[3]) / 2, BLUE, 0.53,
                      width=0.64, height=2.46).set_z_index(-1)
        ancestral = label("Ancestral allele A", 4.28, -0.53, BLUE, 29)
        self.play(GrowFromEdge(column, DOWN, run_time=1.8),
                  tree_flash(world[5], TEXT),
                  LaggedStart(*(FadeIn(m) for m in marks), lag_ratio=0.76, run_time=1.8),
                  FadeIn(ancestral, run_time=0.45))
        self.play(FadeOut(column), run_time=0.30)
        self.finish()


class S05PredictQ(SpokenScene):
    def construct(self):
        main, side, branches, dimmed, derived, bars, tag = prediction_world()
        strips = VGroup(*(genome(i) for i in range(4)))
        ancestral = alleles("ancestral")
        self.add(main, side, branches, strips, ancestral, tag)
        self.at("derived variant b")
        highlights = VGroup(*(cell(SITE_X[i], (ROW_Y[0] + ROW_Y[3]) / 2, ORANGE, 0.60,
                                    width=0.58, height=2.46).set_z_index(-1) for i in B_SITES))
        self.play(FadeOut(ancestral), *(GrowFromEdge(c, UP) for c in highlights), run_time=0.62)
        self.play(FadeOut(highlights), run_time=0.32)
        self.play(LaggedStart(*(GrowFromCenter(m) for m in derived), lag_ratio=0.72), run_time=0.83)
        self.at("where the neanderthal carries b")
        self.play(scan_sites(0, 3, ORANGE),
                  *(Transform(row[2], new[2]) for row, new in zip(strips, dimmed)), run_time=2.1)
        self.at("on this tree")
        self.play(tree_flash(branches[1], BLUE), run_time=1.38)
        self.at("african and eurasian")
        self.play(tree_flash(branches[2], BLUE), tree_flash(branches[3], TEAL), run_time=3.35)
        self.at("without later gene flow")
        self.play(FadeIn(bars[1]), run_time=1)
        self.play(FadeIn(question_card(QUESTION, **QUESTION_CARD)), run_time=1)
        self.at("which living genome")
        self.play(LaggedStart(*(Write(t) for t in bars[0]), lag_ratio=0.62), run_time=2.15)
        self.finish()


class S06PredictPause(PredictPause):
    QUESTION = QUESTION
    CARD = QUESTION_CARD
    SECONDS = 4.5

    def backdrop(self):
        return prediction_world()

    def construct(self):
        backdrop = self.backdrop()
        self.add(backdrop, question_card(self.QUESTION, **self.CARD))
        progress = cell(-1.39, -3.53, GOLD, 1, width=10.22, height=0.15)
        self.add(cell(-1.39, -3.53, GREY, 0.45, width=10.22, height=0.15))
        self.play(GrowFromEdge(progress, LEFT), rate_func=linear, run_time=self.SECONDS)


class S07PredictAnswer(SpokenScene):
    def construct(self):
        main, side, branches, strips, letters, bars, tag = prediction_world()
        question = question_card(QUESTION, **QUESTION_CARD)
        self.add(main, side, branches, strips, letters, bars, tag, question)
        self.at("without gene flow")
        self.play(FadeOut(question), run_time=0.48)
        baseline = tally_baseline()
        self.play(Create(baseline), run_time=0.56)
        fills = (tally_fill(0, 2.32), tally_fill(1, 2.32))
        self.play(*(GrowFromEdge(f, LEFT) for f in fills), run_time=1.76)
        self.at("both reach the neanderthal")
        self.play(tree_flash(branches[2], BLUE), tree_flash(branches[3], TEAL), run_time=1.75)
        self.at("the same shared ancestor")
        self.play(tree_flash(branches[1], BLUE, width=18), run_time=2.25)
        self.at("ancestry in europe or asia")
        thread = bridge()
        self.play(Create(thread), tree_flash(branches[4], PURPLE), run_time=1.78)
        self.at("a little neanderthal dna")
        self.play(Transform(fills[1], tally_fill(1, 2.78)),
                  scan_sites(0, 3, ORANGE), run_time=1.9)
        self.at("that is past gene flow")
        callout = boxed_label("Past gene flow", ORANGE, size=32).move_to(point(4.28, -2.28))
        self.play(Write(callout), run_time=1.07)
        self.play(tree_flash(branches[4], PURPLE), run_time=1.6)
        self.at("patterns can mislead")
        self.play(FadeOut(callout), run_time=1.0)
        self.finish()


class S08Limits(SpokenScene):
    def construct(self):
        branches = tree()
        axis = clock_axis((2.25, 1.90, 1.55, 1.20, 0.85, 0.50), years=True)
        strips = VGroup(*(genome(i) for i in range(4)))
        self.add(main_stage(), side_stage(), branches, strips, axis, schematic())
        self.at("the clock requires")
        anchor = calibration()[0]
        target = Circle(radius=0.14, color=GOLD, stroke_width=4).move_to(point(TIP_X[0], 0.48))
        steady = label("One steady rate", 4.28, 0.92, GOLD)
        self.play(GrowFromCenter(anchor), run_time=0.92)
        self.play(tree_flash(branches[1], BLUE), tree_flash(branches[2], BLUE),
                  GrowFromCenter(target), run_time=1.9)
        self.play(FadeIn(steady), tree_flash(branches[4], PURPLE), run_time=1.48)
        self.at("real substitutions arrive")
        uneven = clock_axis((2.36, 2.21, 1.78, 1.14, 0.98, 0.57))
        self.play(Transform(axis[1], uneven[1]), swap(axis[2], uneven[2], run_time=0.8),
                  FadeOut(steady), run_time=1.6)
        marks = [bar_mark(0, i) for i in (0, 1, 4, 5)]
        self.play(LaggedStart(*(GrowFromCenter(m) for m in marks), lag_ratio=0.62),
                  scan_sites(0, 3, YELLOW), run_time=2.0)

        self.at("slightly harmful mutations")
        caution = label("Slightly harmful", 4.28, 0.92, RED)
        self.play(FadeOut(anchor), FadeOut(target), FadeIn(caution), run_time=0.7)
        self.play(branches[1].animate.set_stroke(width=24), run_time=1.25)
        self.at("depends on population size")
        pop = label("Population size", 4.28, -0.10, TEXT)
        substitutions = [bar_mark(1, i, RED) for i in (0, 1, 2, 4, 5)]
        self.play(FadeIn(pop), branches[1].animate.set_stroke(width=6),
                  scan_sites(0, 3, RED),
                  LaggedStart(*(GrowFromCenter(m) for m in substitutions), lag_ratio=0.44),
                  run_time=2.05)
        self.at("even the sequence tree")
        self.play(FadeOut(caution), FadeOut(pop), branches[1].animate.set_stroke(width=8, opacity=0.52),
                  run_time=0.92)
        node = Dot(point(-4.25, 0.91), color=BLUE, radius=0.13)
        support = boxed_label("Inferred branch\nStated support", TEXT, size=29).move_to(point(4.28, 0.73))
        self.play(GrowFromCenter(node), run_time=0.78)
        self.at("with stated support")
        self.play(FadeIn(support), tree_flash(branches[1], BLUE), run_time=1.33)

        self.at("a departure from neutral counts")
        plot, base, base_label, rise = baseline_meter()
        self.play(FadeOut(support), run_time=0.32)
        self.play(Create(plot), Create(base), FadeIn(base_label), run_time=0.98)
        self.play(GrowFromEdge(rise, DOWN), run_time=1.22)
        self.at("not proof")
        self.play(Write(label("Clue, not proof", 4.28, -2.25, RED, 34)), run_time=1.05)
        self.finish()


class S09UnlockedOrigins(SpokenScene):
    def construct(self):
        branches = tree()
        strips = VGroup(*(genome(i) for i in range(4)))
        plot, base, base_label, rise = baseline_meter()
        clue = label("Clue, not proof", 4.28, -2.25, RED, 34)
        self.add(main_stage(), side_stage(), branches, strips, schematic(),
                 plot, base, base_label, rise, clue)
        self.at("until the early 1990s")
        self.play(FadeOut(plot), FadeOut(base), FadeOut(base_label), FadeOut(rise), FadeOut(clue),
                  branches.animate.set_stroke(opacity=0.17), run_time=1.5)
        stem_xs = (TIP_X[0], TIP_X[1], TIP_X[2])
        regional = VGroup(*(path([(x, 2.48), (x, 0.48)], BLUE) for x in stem_xs))
        historic = VGroup(T("Multiregional", 33, TEXT),
                          T("Favored to early 1990s", 28, TEXT)).arrange(DOWN, buff=0.22)
        historic.move_to(point(4.28, 0.86))
        self.at("researchers favored")
        self.play(LaggedStart(*(Create(s) for s in regional), lag_ratio=0.55),
                  LaggedStart(*(tree_flash(s, BLUE, halo_width=60) for s in regional), lag_ratio=0.65),
                  run_time=2.05)
        self.at("regional populations each")
        self.play(Write(historic), run_time=1.55)
        self.play(LaggedStart(*(tree_flash(s, BLUE, halo_width=60) for s in regional), lag_ratio=0.45),
                  run_time=2.1)
        self.at("living and ancient genomes")
        self.play(FadeOut(historic), FadeOut(regional), run_time=0.9)
        self.play(branches.animate.set_stroke(opacity=1), scan_sites(0, 3, BLUE), run_time=2.05)
        origin = label("African origin", 4.28, 0.86, BLUE, 34)
        self.at("an african origin")
        self.play(FadeIn(origin), tree_flash(branches[1], BLUE), run_time=1.45)
        self.at("living people trace most ancestry")
        self.play(tree_flash(branches[2], BLUE, width=18),
                  tree_flash(branches[3], TEAL, width=18), run_time=1.99)
        self.at("to african populations")
        self.play(tree_flash(branches[1], BLUE, width=18), run_time=1.9)
        self.at("with ancestors outside africa")
        thread = bridge()
        self.play(Create(thread), tree_flash(branches[4], PURPLE), run_time=1.8)
        self.at("little neanderthal dna")
        self.play(FadeIn(label("A little\nNeanderthal DNA", 4.28, -0.75, ORANGE, 31)),
                  scan_sites(0, 3, ORANGE), run_time=1.45)
        self.finish()


class S10UnlockedSelection(SpokenScene):
    def construct(self):
        world = VGroup(main_stage(), side_stage(), tree(),
                       VGroup(*(genome(i) for i in range(4))), bridge())
        plot, base, base_label, rise = baseline_meter()
        meter = VGroup(plot, base, base_label, rise, label("Clue, not proof", 4.28, -2.25, RED, 34))
        tag = schematic()
        self.add(world, meter, tag)
        self.at("proof of selection")
        self.play(tree_flash(world[2][1], BLUE), run_time=2.25)
        self.at("like field records")
        self.play(FadeOut(world), FadeOut(meter), run_time=0.86)
        panels = TwoPanel("Banded population", "Drought survivors",
                          colors=(BLUE, ORANGE), top=2.42, bottom=-2.86, size=30)
        panels.left_frame.set_fill(SLATE, opacity=1)
        panels.right_frame.set_fill(SLATE, opacity=1)
        field = label("Field record", -0.5, 3.44, TEXT, 34, weight=BOLD)
        credit = label("Boag & Grant, 1981", -0.5, 2.93, GOLD, 28)
        self.play(FadeIn(panels.left_frame), FadeIn(panels.right_frame), run_time=0.95)
        self.add(field)
        left = VGroup(bird(-4.54, 0.14, 0.94, BLUE), bird(-2.09, 0.14, 1.14, BLUE))
        right = VGroup(bird(2.02, 0.14, 1.14, ORANGE), bird(4.64, 0.14, 0.94, ORANGE))
        self.at("and grant in 1981")
        self.play(FadeIn(credit), FadeIn(left[0], shift=RIGHT * 0.20), run_time=1.24)
        self.at("compared survivors")
        self.play(FadeIn(panels.right_head), LaggedStart(*(FadeIn(b) for b in right), lag_ratio=0.42),
                  run_time=1.15)
        self.at("1977 drought on daphne major")
        location = label("Field record · Daphne Major, 1977", -0.5, 3.44, TEXT, 34, weight=BOLD)
        self.play(swap(field, location, run_time=1.5))
        self.at("the banded population beforehand")
        self.play(FadeIn(panels.left_head), FadeIn(left[1], shift=LEFT * 0.20), run_time=1.9)

        self.at("larger birds especially")
        self.play(FadeOut(right[1]), right[0].animate.move_to(point(3.3, 0.17)), run_time=1.65)
        self.at("with larger beaks")
        self.play(right[0].animate.scale(1.34), run_time=2.05)
        self.at("beak and body size")
        beak = label("Beak size", 2.10, -1.52, YELLOW, 29)
        body = label("Body size", 4.49, -1.52, ORANGE, 29)
        bracket = path([(1.37, -1.88), (1.37, -2.08), (5.22, -2.08), (5.22, -1.88)], TEXT, 4)
        self.play(FadeIn(beak), Indicate(right[0][4], color=TEXT, scale_factor=1.14),
                  run_time=0.74)
        self.play(FadeIn(body), Create(bracket),
                  Indicate(right[0][2], color=YELLOW, scale_factor=1.09), run_time=1.15)
        self.at("survival alone cannot name", lead=0.25)
        self.play(FadeIn(label("Target uncertain", 3.30, -2.51, TEXT, 29), run_time=0.45),
                  Indicate(right[0][2], color=YELLOW, scale_factor=1.08, run_time=1.9))
        self.at("neutral baselines turn")
        self.play(*(FadeOut(m) for m in list(self.mobjects) if m is not tag), run_time=0.68)
        self.add(world)
        self.play(Create(plot), Create(base), FadeIn(base_label), run_time=1.45)
        self.play(GrowFromEdge(rise, DOWN), run_time=0.86)
        self.at("testable clues")
        self.play(Write(label("Testable clues", 4.28, -2.25, RED, 34)), run_time=0.82)
        self.finish()


class S11End(EndCard):
    LINE = "Neutral change sets the baseline; departures hint at selection or gene flow."
