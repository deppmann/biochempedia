"""GWAS: from a continuous trait to a map of regions worth testing.

COLOR MAP: grey-blue = chromosome structure; teal = populations and controls;
blue/purple = the two allele versions; yellow = scores and measurements;
gold = tagged regions and study dates; green = follow-up tests.
"""
from bp_parts import *

PURPLE = "#B58CD9"
STRUCTURE = "#465C7E"
FILL = "#385268"
TRACK_Y = -2.42
TRACK_W = 12.0
TAG_X = 1.66
SCAN_THRESHOLD = 11
QUESTION = "Does this peak prove causation?"
FINCH_SHARE = 0.45


def label(words, x, y, color=TEXT, size=31):
    return T(words, size, color, weight=BOLD).move_to([x, y, 0])


def box(width, height, x, y, color, opacity=1, stroke=0):
    return RoundedRectangle(
        width=width, height=height, corner_radius=min(0.17, height / 3),
        fill_color=color, fill_opacity=opacity, stroke_color=color, stroke_width=stroke,
    ).move_to([x, y, 0])


def person(height, color=TEAL):
    head = Dot([0, 0.34, 0], radius=0.135, color=color)
    body = Polygon(
        [-0.20, 0.12, 0], [0.20, 0.12, 0], [0.30, -0.16, 0],
        [0.19, -0.21, 0], [0.13, -0.05, 0], [0.13, -0.49, 0],
        [0.04, -0.49, 0], [0, -0.25, 0], [-0.04, -0.49, 0],
        [-0.13, -0.49, 0], [-0.13, -0.05, 0], [-0.19, -0.21, 0],
        [-0.30, -0.16, 0], fill_color=color, fill_opacity=1, stroke_width=0,
    )
    return VGroup(body, head).set_height(height)


def bell(x):
    return np.exp(-0.5 * (x / 1.15) ** 2)


def height_world():
    plot = Plot((-5.83, 5.83, 0.45, 2.92), (-3, 3), (0, 1), color=STRUCTURE)
    curve = plot.curve(bell, color=TEAL, width=4)
    xs = np.linspace(-3, 3, 71)
    fill = Polygon(
        plot.pt(-3, 0), *[plot.pt(x, bell(x)) for x in xs], plot.pt(3, 0),
        fill_color=FILL, fill_opacity=1, stroke_width=0,
    )
    crowd = VGroup()
    for i, x in enumerate(np.linspace(-2.8, 2.8, 17)):
        count = max(1, round(3.6 * bell(x)))
        for row in range(count):
            h = 0.36 + 0.045 * (row + (i % 3))
            p = person(h, (TEAL, BLUE, TEXT)[(i + row) % 3])
            p.move_to(plot.pt(x, 0) + UP * (0.24 + 0.49 * row))
            crowd.add(p)
    return VGroup(fill, plot, curve, crowd)


def crowd_drift(group, amplitude=0.14):
    for i, p in enumerate(group):
        bob(p, amp=amplitude, speed=1.9 + 0.2 * (i % 3), seed=i)
    return group


def chromosome():
    strip = box(TRACK_W, 0.58, 0, TRACK_Y, STRUCTURE)
    ticks = VGroup(*[
        box(0.048, 0.33 if i % 5 else 0.43, x, TRACK_Y, BLUE, 0.78)
        for i, x in enumerate(np.linspace(-5.77, 5.77, 81))
    ])
    return VGroup(strip, ticks)


def scope():
    return scope_tag(size=28, color=TEXT)


def locus_mark(x=TAG_X, color=GOLD):
    return box(0.13, 0.54, x, TRACK_Y, color)


def region(width=1.7):
    body = box(width, 0.6, TAG_X, TRACK_Y, GOLD, 0.40)
    marks = VGroup(*[box(0.055, 0.40, x, TRACK_Y, GOLD)
                     for x in np.linspace(TAG_X - 0.39 * width, TAG_X + 0.39 * width, 7)])
    return VGroup(body, marks, locus_mark())


def scanner(tracker, bottom=TRACK_Y - 0.29, top=1.44):
    beam = VGroup(
        box(0.51, top - bottom, 0, (top + bottom) / 2, YELLOW, 0.26),
        box(0.085, top - bottom, 0, (top + bottom) / 2, YELLOW, 0.92),
    )
    return beam.add_updater(lambda m: m.set_x(tracker.get_value()))


def allele_pair(x, y, colors=(BLUE, PURPLE)):
    tracks = VGroup(*[box(3.2, 0.27, x, y + dy, STRUCTURE) for dy in (0.34, -0.34)])
    tokens = VGroup(*[box(0.55, 0.27, x, y + dy, c) for dy, c in zip((0.34, -0.34), colors)])
    return tracks, tokens


def disease_crowd():
    groups = VGroup()
    for x, color in [(-3.35, PURPLE), (3.35, TEAL)]:
        group = VGroup(*[person(0.92 + 0.10 * (i % 3), color) for i in range(7)])
        group.arrange(RIGHT, buff=0.19, aligned_edge=DOWN).move_to([x, 2.30, 0])
        groups.add(group)
    return groups


def disease_heads():
    return VGroup(label("With disease", -3.35, 1.43, PURPLE),
                  label("Without disease", 3.35, 1.43, TEAL))


def chi_square(case_a, control_a, total):
    """Pearson chi-square on two equal-sized groups with two allele versions."""
    expected_a = (case_a + control_a) / 2
    expected_b = total - expected_a
    return (case_a - control_a) ** 2 / 2 * (1 / expected_a + 1 / expected_b)


def scan_plot():
    plot = Plot((-5.8, 5.8, -2.04, 1.19), (-5.8, 5.8), (0, 24), color=TEAL)
    chart = box(11.6, 3.23, 0, -0.425, "#273A4C")
    grid = VGroup(*[
        Line(plot.pt(-5.8, y), plot.pt(5.8, y), color=FILL, stroke_width=1.4)
        for y in (5, 17)
    ])
    plot.add_to_back(chart, grid)
    return plot


def scan_points(plot, prediction=False):
    rng = np.random.default_rng(128 if prediction else 43)
    slots = np.linspace(-5.73, 5.73, 160)
    case = rng.binomial(100, 0.5, len(slots))
    control = rng.binomial(100, 0.5, len(slots))
    hit = np.argmin(abs(slots - TAG_X))
    slots[hit] = TAG_X
    peaks = [(hit, (66, 34))] if prediction else [
        (28, (63, 36)), (hit, (65, 35)), (135, (61, 37)),
    ]
    background = np.ones(len(slots), dtype=bool)
    effects = (4, 6, 9, 11, 0, 11, 9, 6, 4)
    for i, counts in peaks:
        background[i - 4:i + 5] = False
        for offset, effect in enumerate(effects, start=-4):
            case[i + offset], control[i + offset] = 50 + effect, 50 - effect
        case[i], control[i] = counts
    scores = chi_square(case, control, 100)
    dots = VGroup()
    for x, score in zip(slots, scores):
        dots.add(Dot(plot.pt(x, score), radius=0.043, color=TEAL if x < 0 else BLUE))
    hits = [dot for dot, score in zip(dots, scores) if score >= SCAN_THRESHOLD]
    chance_spikes = [dot for dot, score, is_background in zip(dots, scores, background)
                     if is_background and 4.7 < score < SCAN_THRESHOLD]
    if prediction:
        for dot in hits:
            dot.set_color(YELLOW).scale_to_fit_width(0.114)
    return dots, plot.pt(TAG_X, scores[hit]), hits, chance_spikes


def threshold(plot):
    y = plot.pt(0, SCAN_THRESHOLD)[1]
    line = DashedLine([-5.78, y, 0], [5.78, y, 0], color=TEXT, stroke_width=2, dash_length=0.13)
    return VGroup(line, label("Threshold", -1.4, y + 0.34, TEXT, 28))


def tag_halo(peak):
    return Circle(radius=0.19, color=GOLD, stroke_width=4).move_to(peak)


def prediction_world():
    plot = scan_plot()
    dots, peak, _, _ = scan_points(plot, prediction=True)
    return VGroup(chromosome(), disease_crowd(), disease_heads(), plot, dots,
                  threshold(plot), tag_halo(peak), locus_mark(), scope())


def prediction_card():
    return question_card(QUESTION, y=3.25, size=37)


def arrows(start, end, color=GREEN, width=7):
    return Arrow(start, end, buff=0, color=color, stroke_width=width,
                 tip_length=0.44 if width > 20 else 0.22,
                 max_tip_length_to_length_ratio=0.38, max_stroke_width_to_length_ratio=20)


def mouse(x, y, color=TEAL):
    tail = ArcBetweenPoints([-0.59, -0.03, 0], [-1.25, 0.10, 0], angle=-1.55, color=color, stroke_width=5)
    body = Ellipse(width=1.35, height=0.78, fill_color=color, fill_opacity=1, stroke_width=0)
    head = Ellipse(width=0.67, height=0.49, fill_color=color, fill_opacity=1, stroke_width=0).shift([0.61, 0.02, 0])
    ear = Dot([0.46, 0.30, 0], radius=0.20, color=color)
    eye = Dot([0.77, 0.10, 0], radius=0.044, color=BG)
    return VGroup(tail, body, ear, head, eye).scale(1.28).move_to([x, y, 0])


def finch(height, color, beak_length):
    head = Ellipse(width=0.64, height=0.73, fill_color=color, fill_opacity=1, stroke_width=0)
    bill = Polygon([0.22, 0.13, 0], [beak_length, -0.055, 0], [0.20, -0.20, 0],
                   fill_color=GOLD, fill_opacity=1, stroke_width=0)
    neck = Polygon([-0.30, -0.23, 0], [0.17, -0.22, 0], [0.06, -0.53, 0], [-0.58, -0.53, 0],
                   fill_color=color, fill_opacity=1, stroke_width=0)
    eye = Dot([0.12, 0.12, 0], radius=0.043, color=BG)
    return VGroup(neck, head, bill, eye).set_height(height)


class S01Hook(SpokenScene):
    def construct(self):
        track, world = chromosome(), height_world()
        self.at("how can you")
        self.add(track, world[0], world[1], scope())
        query = VGroup(*[label("?", x, -1.65, YELLOW, 44) for x in (-4.65, -2.3, 0, 2.3, 4.65)])
        crowd_drift(world[3])
        self.play(LaggedStart(*[FadeIn(p, shift=UP * 0.17) for p in world[3]], lag_ratio=0.055),
                  FadeIn(query), run_time=2.9)
        for i, mark in enumerate(query):
            bob(mark, amp=0.105, speed=2.5, seed=i)
        self.at("adult height")
        self.play(Create(world[2]), run_time=1.55)
        height = label("Adult height", 0, -0.02, TEAL, 35)
        self.play(FadeIn(height), run_time=0.45)
        self.at("many chromosome positions")
        query.clear_updaters(recursive=True)
        pos = ValueTracker(-5.6)
        beam = scanner(pos, top=-1.08)
        self.play(FadeOut(query), FadeIn(beam), run_time=0.5)
        self.play(pos.animate.set_value(5.6), rate_func=linear, run_time=3.6)
        self.at("polygenic trait")
        polygenic = label("Polygenic trait", 0, -0.02, TEAL, 35)
        self.play(swap(height, polygenic), pos.animate.set_value(TAG_X), run_time=0.9)
        self.at("each position")
        self.play(FadeOut(polygenic), FadeOut(beam), run_time=0.35)
        tracks, tokens = allele_pair(TAG_X, -0.78)
        individual = person(0.98).move_to([-2.32, -0.78, 0])
        self.play(FadeIn(individual, shift=DOWN * 0.25), run_time=0.42)
        self.play(GrowFromPoint(tracks, individual.get_right()), FadeIn(locus_mark()), run_time=0.63)
        loc = label("Locus", TAG_X, -1.79, GOLD)
        self.play(FadeIn(loc), run_time=0.35)
        self.at("alternative versions")
        self.play(LaggedStart(*[GrowFromCenter(t) for t in tokens], lag_ratio=0.32), run_time=0.8)
        self.play(FadeIn(label("Alleles", 4.35, -0.75, BLUE)), run_time=0.45)
        self.finish()


class S02Title(TitleCard):
    LESSON = "Genome-wide association studies (GWAS)"
    TITLE = "Scanning Many Genomes for Trait Signals"

    def construct(self):
        world, track = height_world(), chromosome()
        crowd_drift(world[3])
        self.add(world.fade(0.40), track.fade(0.40))
        title = fit_text(self.TITLE, max_w=12.1, size=46, min_size=34, font=TITLE_FONT, max_lines=1)
        title.move_to([0, -0.52, 0])
        lesson = label(self.LESSON, 0, -1.23, TEAL, 28)
        rule = Line([-1.15, -1.65, 0], [1.15, -1.65, 0], color=GOLD, stroke_width=4)
        self.play(FadeIn(title), FadeIn(lesson), GrowFromCenter(rule), run_time=5 / 15)
        self.wait(17 / 15)
        self.play(FadeOut(title), FadeOut(lesson), FadeOut(rule), run_time=5 / 15)


class S03Count(SpokenScene):
    def construct(self):
        world, track = height_world(), chromosome()
        crowd_drift(world[3])
        scope_label = scope()
        self.add(world, track, scope_label)
        self.at("genome wide association")
        pos = ValueTracker(-5.6)
        beam = scanner(pos, top=0.32)
        self.play(FadeIn(beam), run_time=0.55)
        self.play(pos.animate.set_value(TAG_X), run_time=4.45, rate_func=linear)
        focus = locus_mark()
        self.play(FadeIn(focus), run_time=0.38)
        self.at("it counts alleles")
        x_positions = (-3.65, 0, 3.65)
        pairs = [allele_pair(x, -0.73, c) for x, c in zip(
            x_positions, ((BLUE, PURPLE), (BLUE, BLUE), (PURPLE, BLUE)))]
        people = VGroup(*[person(1.42).move_to([x, 1.43, 0]) for x in x_positions])
        world[3].clear_updaters(recursive=True)
        self.play(FadeOut(world), FadeOut(beam), FadeIn(people), run_time=0.7)
        self.play(LaggedStart(*[GrowFromPoint(p[0], q.get_bottom()) for p, q in zip(pairs, people)],
                              lag_ratio=0.55), run_time=1.65)
        for token_pair in pairs:
            self.add(token_pair[1])
        self.at("two copies")
        tokens = [token for _, copies in pairs for token in copies]
        self.play(LaggedStart(*[t.animate.move_to([-1.69 + i * 0.67, -1.57, 0])
                                for i, t in enumerate(tokens)], lag_ratio=0.14), run_time=1.75)

        self.at("a chi square score")
        self.play(*[FadeOut(x) for x in [people, *[p[0] for p in pairs]]], run_time=0.4)
        groups = disease_heads().set_color(TEXT).shift(UP * 0.94)
        centers = (-3.25, 0.65)
        bottom, unit, total = -1.64, 0.29, 10
        a = ValueTracker(5)
        bar_h = unit * total
        bars = VGroup()
        for index, x in enumerate(centers):
            count = (lambda: a.get_value()) if index == 0 else (lambda: total - a.get_value())

            def stack(x=x, count=count):
                h = count() * unit
                return VGroup(box(2.14, h, x, bottom + h / 2, BLUE),
                              box(2.14, bar_h - h, x, bottom + (bar_h + h) / 2, PURPLE))

            bars.add(always_redraw(stack))
        groups[0].set_x(centers[0])
        groups[1].set_x(centers[1])
        self.play(*[FadeOut(token) for token in tokens], FadeIn(bars), run_time=0.65)
        self.at("with and without")
        self.play(FadeIn(groups), run_time=0.43)
        expected_y = bottom + 5 * unit
        expected = DashedLine([-4.42, expected_y, 0], [2.15, expected_y, 0], color=TEXT, stroke_width=4)
        self.at("counts expected")
        expected_label = place_label(T("Expected,\nno link", 28, TEXT, weight=BOLD),
                                     expected, dirs=(RIGHT,), buff=0.16)
        self.play(Create(expected), FadeIn(expected_label), run_time=0.55)
        self.at("the bigger the score")
        meter = box(0.52, bar_h, 4.56, bottom + bar_h / 2, FILL)

        maximum_score = chi_square(total, 0, total)

        def score_fill():
            fraction = chi_square(a.get_value(), total - a.get_value(), total) / maximum_score
            h = max(0.04, (bar_h - 0.12) * fraction)
            return box(0.39, h, 4.56, bottom + h / 2 + 0.06, YELLOW)

        gauge = always_redraw(score_fill)
        self.play(FadeIn(meter), FadeIn(gauge),
                  FadeIn(label("Chi-square score", 4.47, 1.69, YELLOW, 29)), run_time=0.5)
        self.play(a.animate.set_value(9.5), run_time=2.95, rate_func=smooth)
        self.finish()


class S04Scan(SpokenScene):
    def construct(self):
        plot = scan_plot()
        dots, peak, hits, chance_spikes = scan_points(plot)
        pos = ValueTracker(TAG_X)
        beam = scanner(pos)
        focus = locus_mark()
        overview = height_world()
        crowd = overview[3].copy()
        crowd.scale(0.55).move_to([0, 2.37, 0])
        crowd_drift(crowd)
        self.add(chromosome(), focus, plot, beam, crowd, scope())
        self.at("the scan repeats")
        self.play(pos.animate.set_value(-5.75), FadeOut(focus), run_time=0.85)
        self.play(pos.animate.set_value(5.76),
                  LaggedStart(*[FadeIn(d, shift=UP * 0.19) for d in dots], lag_ratio=0.11),
                  run_time=4.7, rate_func=linear)
        self.play(FadeOut(beam), run_time=0.38)
        self.at("some scores run high")
        scatter = VGroup(*[Circle(radius=0.11, stroke_width=2.5, color=YELLOW).move_to(d)
                           for d in chance_spikes])
        self.play(LaggedStart(*[GrowFromCenter(m) for m in scatter], lag_ratio=0.18), run_time=2.45)
        self.at("crossing a strict threshold")
        rule = threshold(plot)
        self.play(Create(rule[0]), FadeOut(scatter),
                  *[dot.animate.set_color(YELLOW).scale_to_fit_width(0.114) for dot in hits],
                  run_time=0.8)
        self.play(FadeIn(rule[1]), run_time=0.35)
        self.at("because nearby variants")
        band = region()
        halo = tag_halo(peak)
        band.stretch(0.46, 0, about_point=[TAG_X, TRACK_Y, 0])
        self.play(FadeIn(band), Create(halo), run_time=0.60)
        self.play(band.animate.stretch(1 / 0.46, 0, about_point=[TAG_X, TRACK_Y, 0]), run_time=2.55)
        self.at("acts as a tag")
        tag_label = place_label(label("Tag", 0, 0, GOLD), halo, dirs=(UP,), buff=0.16)
        self.play(FadeIn(tag_label), run_time=0.45)
        other_dots = VGroup(*[d for d in dots if abs(d.get_x() - TAG_X) > 0.48])
        self.play(other_dots.animate.set_opacity(0.58), run_time=1.9)
        pulse(halo, base=6, amp=3.5, speed=2.3)
        self.at("genome wide signals")
        linked = label("Linked region", TAG_X, -3.11, GOLD)
        self.play(FadeIn(linked), run_time=0.65)
        self.play(band.animate.stretch(1.25, 0, about_point=[TAG_X, TRACK_Y, 0]), run_time=2.15)
        self.at("proven causal variants")
        self.play(dots.animate.set_opacity(0.37), band.animate.scale([1.18, 1, 1]), run_time=1.45)
        self.finish()


class S05PredictQ(SpokenScene):
    def construct(self):
        track, groups, heads, plot, dots, rule, halo, mark, schematic = prediction_world()
        overview = height_world()
        people = overview[3].scale(0.55).move_to([0, 2.37, 0])
        self.add(track, plot, people, schematic)
        self.at("test that idea")
        self.play(ReplacementTransform(people, VGroup(*[p for g in groups for p in g])),
                  FadeIn(heads), run_time=1.9)
        self.add(groups)
        for g in groups:
            crowd_drift(g, amplitude=0.105)
        self.play(Create(rule[0]), FadeIn(rule[1]), run_time=0.85)
        self.at("one tag variant")
        nearby = VGroup(*[d for d in dots if d.get_y() > 0.20])
        low = VGroup(*[d for d in dots if d.get_y() <= 0.20])
        self.play(LaggedStart(*[FadeIn(d) for d in low], lag_ratio=0.06), run_time=1.35)
        self.play(FadeIn(nearby, shift=UP * 0.36), FadeIn(mark), run_time=1.0)
        pulse(halo, base=4, amp=2.1, speed=2.8)
        self.play(Create(halo), run_time=0.58)
        self.at("does that strong peak")
        self.play(FadeIn(prediction_card()), run_time=0.55)
        self.at("pause and predict")
        halo.clear_updaters()
        halo.set_stroke(width=4)
        self.wait(0.75)
        for live in groups:
            live.clear_updaters(recursive=True)
        self.play(Transform(groups, disease_crowd()), run_time=1.35, rate_func=linear)
        self.finish()


class S06PredictPause(PredictPause):
    QUESTION = QUESTION
    CARD = {"y": 3.25, "size": 37}
    SECONDS = 4.5

    def backdrop(self):
        return prediction_world()

    def construct(self):
        # The scene duration is locked to the script's silent audio.
        world = self.backdrop()
        self.add(world, prediction_card())
        stroke = Circle(radius=0.22, color=GOLD, stroke_width=6).move_to(world[6])
        self.add(stroke)
        self.play(stroke.animate.scale(2.7).set_opacity(0), rate_func=linear, run_time=self.SECONDS)


class S07Limits(SpokenScene):
    def construct(self):
        track, groups, heads, plot, dots, rule, halo, mark, schematic = prediction_world()
        question = prediction_card()
        self.add(track, groups, heads, plot, dots, rule, halo, mark, schematic, question)
        for g in groups:
            crowd_drift(g, amplitude=0.06)
        self.at("the peak flags")
        linked = region()
        linked.stretch(0.36, 0, about_point=[TAG_X, TRACK_Y, 0])
        self.play(FadeOut(question), FadeOut(halo), FadeOut(mark), FadeIn(linked), run_time=0.46)
        self.play(linked.animate.stretch(1 / 0.36, 0, about_point=[TAG_X, TRACK_Y, 0]), run_time=0.65)
        linked_label = label("Linked region", TAG_X, -3.08, GOLD)
        self.play(FadeIn(linked_label), run_time=0.42)
        self.at("a shared environment")
        tint = box(5.62, 1.42, -3.35, 2.41, FILL)
        tint.set_z_index(-1)
        env = label("Shared environment", -3.35, 3.40, TEAL, 31)
        groups.clear_updaters(recursive=True)
        self.play(GrowFromCenter(tint), groups.animate.shift(UP * 0.10), run_time=0.78)
        for g in groups:
            crowd_drift(g, amplitude=0.06)
        self.play(FadeIn(env), run_time=0.5)
        self.at("carriers of an allele")
        torsos = [groups[0][i][0] for i in (1, 3, 5)]
        copies = VGroup(*[box(0.23, 0.18, torso.get_x(), torso.get_y() + 0.12, BLUE)
                          for torso in torsos])
        for token, torso in zip(copies, torsos):
            token.add_updater(lambda m, torso=torso: m.move_to(torso.get_center() + UP * 0.12))
        self.play(LaggedStart(*[GrowFromCenter(c) for c in copies], lag_ratio=0.7), run_time=2.25)
        self.at("population patterns")
        copies.clear_updaters(recursive=True)
        one = person(2.08, TEAL).move_to([0, 1.45, 0])
        self.play(FadeOut(env), FadeOut(tint), FadeOut(copies), FadeOut(heads), FadeOut(groups),
                  FadeOut(plot), FadeOut(rule), FadeOut(dots), FadeIn(one, scale=0.6), run_time=0.82)
        bob(one, amp=0.12, speed=2.5)
        personal_question = label("?", 1.28, 1.64, GOLD, 65)
        self.play(FadeIn(personal_question), run_time=0.47)
        self.at("to test mechanism")
        panels = TwoPanel("Edited", "Unedited control", colors=(GREEN, TEAL),
                          width=10.6, top=2.62, bottom=-1.36, size=34)
        for frame in (panels.left_frame, panels.right_frame):
            frame.set_fill("#273A4C", opacity=1)
        mice = VGroup(*[mouse(x, 0.45, c).scale(1.36) for x, c in ((-2.75, GREEN), (2.75, TEAL))])
        branch = VGroup(arrows([TAG_X, -2.04, 0], [2.75, -1.54, 0]),
                        arrows([TAG_X - 0.35, -2.04, 0], [-2.15, -1.53, 0]))
        self.play(FadeOut(one), FadeOut(personal_question), GrowFromCenter(branch), run_time=0.7)
        self.play(FadeIn(panels), run_time=0.7)
        self.at("edit a candidate gene")
        self.play(FadeIn(mice[0], shift=RIGHT * 0.45), run_time=0.75)
        bob(mice[0], amp=0.16, speed=2.4)
        self.at("unedited controls")
        self.play(FadeIn(mice[1], shift=LEFT * 0.45), run_time=0.72)
        bob(mice[1], amp=0.16, speed=2.4, seed=3)
        self.play(FadeOut(linked_label), run_time=0.45)
        self.finish()


class S08Polygenic(SpokenScene):
    def construct(self):
        track = chromosome()
        schem = scope()
        self.add(track, schem)
        self.at("adding up small effects")
        xs = np.linspace(-5.52, 5.52, 23)
        effects = 0.10 + 0.13 * np.sin(np.arange(len(xs)) * 1.7) ** 2
        ticks = VGroup(*[box(0.13, 4 * e, x, -2.1 + 2 * e, YELLOW) for x, e in zip(xs, effects)])
        amount = ValueTracker(0)
        gauge = dial(amount, center=[0, 0.37, 0], radius=2.07, color=YELLOW, fmt="{}", scale=1)
        gauge.remove(gauge[3])
        face = Sector(
            radius=2.07, angle=PI, fill_color=FILL, fill_opacity=1, stroke_width=0,
        ).shift(UP * 0.37)
        gauge.add_to_back(face)
        self.play(LaggedStart(*[GrowFromEdge(b, DOWN) for b in ticks], lag_ratio=0.085), run_time=1.4)
        streams = VGroup(*[arrows([x, -1.13, 0], [0.49 * x, 0.08, 0], color=YELLOW, width=3)
                           for x in xs[::2]])
        self.play(FadeIn(gauge), LaggedStart(*[GrowArrow(a) for a in streams], lag_ratio=0.08),
                  amount.animate.set_value(sum(effects) / (len(xs) * max(effects))), run_time=2.0)
        self.at("polygenic score")
        name = label("Polygenic score", 0, 2.94, YELLOW, 35)
        self.play(FadeIn(name), run_time=0.55)
        self.at("study cohort")
        self.play(FadeOut(gauge), FadeOut(streams), FadeOut(name), FadeOut(ticks), run_time=0.65)
        groups = disease_crowd().shift(DOWN * 0.16)
        outside = VGroup(*[person(0.84 + 0.16 * (i % 4), (TEAL, BLUE, TEXT, PURPLE)[i % 4])
                           for i in range(8)])
        outside.arrange(RIGHT, buff=0.15, aligned_edge=DOWN).scale_to_fit_width(5.15)
        outside.move_to([3.35, 2.05, 0])
        groups[0].set_color(TEAL)
        groups[1].become(outside)
        backdrops = VGroup(*[box(5.55, 1.78, x, 2.03, "#273A4C") for x in (-3.35, 3.35)])
        self.play(FadeIn(backdrops), FadeIn(groups), run_time=0.65)
        for group in groups:
            crowd_drift(group)
        self.at("studied uk biobank")
        cohort = label("UK Biobank", -3.35, 3.32, TEAL, 35)
        public = label("General population", 3.35, 3.32, TEXT, 35)
        self.play(FadeIn(cohort), run_time=0.56)
        self.at("general population")
        self.play(FadeIn(public), run_time=0.48)
        self.at("their scores were less precise")
        outside_label = label("Outside study ancestry groups", 3.35, 3.34, TEXT, 28)
        self.play(swap(public, outside_label), run_time=0.62)
        base = VGroup(*[box(4.9, 0.42, x, -0.05, FILL) for x in (-3.35, 3.35)])
        self.play(FadeIn(base), run_time=0.55)
        width = ValueTracker(0.46)
        narrow = box(0.46, 0.48, -3.35, -0.05, YELLOW)
        wide = always_redraw(lambda: VGroup(*[
            box(width.get_value() * w, 0.48, 3.35, -0.05, YELLOW, alpha)
            for w, alpha in ((1.0, 0.26), (0.71, 0.36), (0.37, 0.65))
        ]))
        self.play(GrowFromCenter(narrow), FadeIn(wide), run_time=0.63)
        ancestry = label("Mostly European ancestry", -3.35, -0.91, TEAL, 29)
        self.at("mostly european ancestry")
        self.play(FadeIn(ancestry), width.animate.set_value(4.15), run_time=2.0)
        self.finish()


def c4_region():
    return VGroup(chromosome(), region(), label("C4A (2016)", TAG_X, -3.10, GOLD, 34))


class S09UnlockedHuman(SpokenScene):
    def construct(self):
        track = chromosome()
        world = height_world()
        crowd_drift(world[3])
        self.add(track, scope())
        self.at("used carefully")
        self.play(FadeIn(world, scale=0.87), run_time=2.4)
        self.at("study scanned up to")
        extra = VGroup()
        for i, x in enumerate(np.linspace(-5.54, 5.54, 33)):
            extra.add(person(0.30 + 0.11 * bell(x * 0.5), (TEAL, BLUE, TEXT)[i % 3])
                      .move_to([x, 0.65, 0]))
        self.play(LaggedStart(*[FadeIn(p, shift=UP * 0.19) for p in extra], lag_ratio=0.07),
                  run_time=2.3)
        crowd_drift(extra)
        self.at("million people")
        study = label("Up to 5.4 million people · 2022", 0, -0.27, TEAL, 33)
        self.play(FadeIn(study), run_time=0.62)
        self.at("it listed")
        variants = VGroup(*[box(0.044, 0.28 + 0.42 * abs(np.sin(i * 2.1)), x,
                                TRACK_Y + 0.58, YELLOW)
                            for i, x in enumerate(np.linspace(-5.78, 5.78, 101))])
        self.play(LaggedStart(*[GrowFromEdge(v, DOWN) for v in variants], lag_ratio=0.08), run_time=1.24)
        self.at("independent variants")
        variants_label = label("12,111 height variants", 0, -3.1, YELLOW, 33)
        self.play(FadeIn(variants_label), run_time=0.6)
        self.at("in 2016")
        c4 = c4_region()
        self.play(FadeOut(world), FadeOut(extra), FadeOut(variants), FadeOut(study), FadeOut(variants_label),
                  GrowFromCenter(c4[1]), run_time=1.05)
        c4_context = box(8.9, 2.5, TAG_X - 0.30, 0.06, "#273A4C")
        zoom = VGroup(*[box(0.08, 1.15, x, 0.06, GOLD if i == 4 else BLUE, 0.80)
                        for i, x in enumerate(np.linspace(TAG_X - 3.25, TAG_X + 2.65, 9))])
        tether = Line([TAG_X, -2.08, 0], [TAG_X, -1.19, 0], color=GOLD, stroke_width=5)
        self.play(FadeIn(c4[2]), Create(tether), run_time=0.6)
        self.play(FadeIn(c4_context), GrowFromPoint(zoom, [TAG_X, -1.18, 0]), run_time=2.75)
        self.at("c for a gene")
        self.play(zoom[4].animate.stretch(2.3, 0).set_opacity(1), run_time=1.2)
        self.at("predicted to raise")
        self.play(FadeOut(c4_context), FadeOut(zoom), FadeOut(tether), run_time=0.4)
        headings = VGroup(label("Predicted C4A expression", -3.12, 2.74, BLUE, 34),
                          label("Schizophrenia risk", 3.12, 2.74, YELLOW, 34))
        expression = arrows([-3.12, -1.13, 0], [-3.12, 2.00, 0], BLUE, 47)
        risk = arrows([3.12, -1.13, 0], [3.12, 0.85, 0], YELLOW, 47)
        self.play(GrowArrow(expression), run_time=0.9)
        self.play(FadeIn(headings[0]), run_time=0.45)
        self.at("associated with higher")
        self.play(GrowArrow(risk), run_time=0.85)
        self.play(FadeIn(headings[1]), run_time=0.47)
        self.finish()


class S10UnlockedWild(SpokenScene):
    def construct(self):
        track, tagged, c4 = c4_region()
        subject = mouse(-3.2, 0.67)
        self.add(track, tagged, c4, scope())
        self.at("losing c4")
        self.play(FadeIn(subject, shift=UP * 0.25), run_time=0.78)
        c4_loss = label("C4 loss in mice", TAG_X, -3.10, GOLD, 32)
        self.play(swap(c4, c4_loss), run_time=0.63)
        bob(subject, amp=0.17, speed=2.7)
        self.at("reduced synapse pruning")
        drop = arrows([3.12, 1.76, 0], [3.12, -0.77, 0], BLUE, 43)
        self.play(GrowArrow(drop), run_time=1.0)
        pruning = label("Less synapse pruning", 3.12, 2.52, BLUE, 34)
        thalamus = label("Mouse visual thalamus", 3.12, -1.27, TEAL, 29)
        self.play(FadeIn(pruning), FadeIn(thalamus), run_time=0.59)
        self.at("testable hypothesis")
        candidate = arrows([TAG_X, -2.0, 0], [2.5, -1.62, 0], GREEN, 6)
        self.play(GrowArrow(candidate), run_time=1.12)
        self.at("in 2023")
        flock = VGroup(*[finch(1.65, (TEAL, BLUE)[i % 2], length)
                         for i, length in enumerate((0.44, 0.72, 0.57, 0.91, 0.67, 0.83))])
        flock.arrange(RIGHT, aligned_edge=DOWN, buff=0.30).scale_to_fit_width(11.75)
        flock.move_to([0, 1.56, 0])
        self.play(FadeOut(drop), FadeOut(pruning), FadeOut(thalamus), FadeOut(candidate),
                  FadeOut(tagged), FadeOut(c4_loss), ReplacementTransform(subject, flock), run_time=1.3)
        crowd_drift(flock, amplitude=0.22)
        self.at("analyzed 3")
        study = label("3,955 finch genomes · 2023", 0, 3.12, GOLD, 35)
        self.play(FadeIn(study), run_time=0.65)
        self.at("six large effect loci")
        peaks = VGroup(*[box(0.21, h, x, -2.13 + h / 2, YELLOW)
                         for x, h in zip((-5.02, -3.47, -1.68, 0.42, 2.28, 4.88),
                                         (0.68, 0.81, 0.67, 0.93, 0.74, 0.60))])
        self.play(LaggedStart(*[GrowFromEdge(p, DOWN) for p in peaks], lag_ratio=0.25), run_time=1.20)
        self.at("explained 45")
        width, center_y = 11.12, -0.29
        left = -width / 2
        frame = box(width, 0.63, 0, center_y, FILL, opacity=0.30, stroke=2)
        part = Rectangle(width=width * FINCH_SHARE, height=0.57, stroke_width=0,
                         fill_color=YELLOW, fill_opacity=1)
        part.move_to([left + width * FINCH_SHARE / 2, center_y, 0])
        self.play(FadeIn(frame), GrowFromEdge(part, LEFT), run_time=0.90)
        share_label = label(f"{FINCH_SHARE:.0%}", part.get_x(), -0.89, YELLOW, 35)
        self.play(FadeIn(share_label), run_time=0.35)
        self.at("medium ground finch")
        finch_label = label("Medium ground finch", 0, 3.12, TEAL, 35)
        self.play(swap(study, finch_label), run_time=0.6)
        self.at("leaving most unassigned")
        rest = label("Unassigned", width * FINCH_SHARE / 2, -0.89, TEXT, 31)
        self.play(FadeIn(rest), run_time=0.52)
        self.at("genome scans turn traits")
        self.play(FadeOut(frame), FadeOut(part), FadeOut(rest), FadeOut(share_label),
                  FadeOut(finch_label), FadeOut(flock), run_time=0.60)
        routes = VGroup(*[arrows([x, -1.08, 0], [target, 1.73, 0], GREEN, 9)
                          for x, target in ((-3.47, -4.50), (0.42, 0), (2.28, 4.50))])
        self.play(LaggedStart(*[GrowArrow(r) for r in routes], lag_ratio=0.34), run_time=2.0)
        self.at("point experiments")
        self.play(FadeIn(label("Follow-up experiments", 0, 2.48, GREEN, 38)), run_time=0.66)
        self.finish()


class S11End(EndCard):
    LINE = "Genome scans flag regions linked to a trait, not proven causes."
