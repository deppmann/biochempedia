"""Weighing Evidence Across Studies, animated to the supplied narration.

COLOR MAP (from the patch-clamp palette)
BLUE / TEAL: study measurements and precise estimates
GREY: the shared scale and low-precision estimates
YELLOW: the pooled result
GREEN: eligible studies and agreement with the niche limit
RED: excluded or missing studies and unsuitable conditions
PURPLE: climate redistribution and elevation limits
GOLD: questions, dates, and the takeaway
"""
from bp_parts import *  # noqa: F403

PURPLE = "#B58CD9"
PANEL = "#23374A"
ALT_PANEL = "#1E3042"
AXIS_Y = -2.07
SUMMARY_Y = -3.02
ROW_Y = (2.18, 1.27, 0.36, -0.55, -1.46)
HOOK_Y = (1.82, 0.87, 0.10, -0.71, -1.38)
QUESTION = "Where does the pooled diamond land?"
QUESTION_STYLE = {"y": 3.23, "size": 38}

# Schematic effects and interval half-widths on one common scale. All rows
# use the same interval multiplier, so relative inverse variances are 1/h².
EXAMPLE = ((2.40, 0.55), (-0.80, 2.65), (1.25, 0.68), (0.15, 1.78), (3.30, 1.52))
PREDICTION = ((0.18, 2.25), (3.22, 0.48), (-0.32, 2.50), (1.82, 0.58), (0.03, 2.05))
MISSING = ((-1.72, 1.70), (-2.25, 1.45))
NICHES = (0.46, 0.26, 0.23)
WARMING_X = (0.12, 0.28, 0.44, 0.66, 0.88)
SHIFT_Y = (0.17, 0.31, 0.27, 0.60, 0.83)


def p(x, y):
    return np.array([x, y, 0.0])


def wide_text(words, x=0, y=3.23, color=TEXT, size=38):
    return fit_text(words, max_w=11.6, min_size=28, size=size, color=color).move_to(p(x, y))


def field(width, height, center, color=PANEL):
    return RoundedRectangle(
        width=width, height=height, corner_radius=0.13,
        stroke_width=0, fill_color=color, fill_opacity=1,
    ).move_to(center)


def trace_rows(scene, bands, strength=0.50, release=0.60, tail=0.0):
    """Pass a soft row highlight down the chart without moving the data marks."""
    base = [band.get_fill_color() for band in bands]
    highlight = ManimColor("#466579")
    duration = scene.narration_s + tail

    def scan(group, dt):
        t = scene.elapsed()
        envelope = min(1, t / 0.60, max(0, duration - t) / release)
        for i, (band, color) in enumerate(zip(group, base)):
            wave = 0.5 + 0.5 * np.cos(TAU * (t / 3.7 - i / len(group)))
            band.set_fill(interpolate_color(color, highlight, strength * envelope * wave))

    bands.add_updater(scan)


def overview():
    """Plot scaffold shared from the hook to the study-bias discussion."""
    axis = Plot(
        box=(-6.0, 6.0, AXIS_Y, 2.57),
        xr=(-6, 6), yr=(AXIS_Y, 2.57), color=TEXT, stroke=3.2,
        xticks=[(0, "0")], size=28,
    )
    bands = VGroup(*[
        field(11.7, 0.73, p(0, y), PANEL if i % 2 == 0 else ALT_PANEL)
        for i, y in enumerate(ROW_Y)
    ])
    zero = axis.vline(0, color=GREY)
    return VGroup(bands, zero, axis.axes[0], axis.ticks, axis.tick_labels,
                  scope_tag("schematic", size=28, color=TEXT))


def row_color(half_width):
    if half_width <= 0.7:
        return BLUE
    if half_width >= 1.7:
        return GREY
    return TEAL


def interval(effect, half_width, y, color):
    left, right = effect - half_width, effect + half_width
    return VGroup(
        Line(p(left, y), p(right, y), color=color, stroke_width=5),
        *[Line(p(x, y - 0.11), p(x, y + 0.11), color=color, stroke_width=4)
          for x in (left, right)],
    )


def estimate(effect, half_width, y, weighted=False, color=None):
    color = color or row_color(half_width)
    if weighted:
        return Square(
            side_length=0.26 / half_width, stroke_color=color, stroke_width=2,
            fill_color=color, fill_opacity=1,
        ).move_to(p(effect, y))
    return Dot(p(effect, y), radius=0.105, color=color)


def forest(studies=EXAMPLE, weighted=False):
    return [
        VGroup(interval(x, h, y, row_color(h)), estimate(x, h, y, weighted))
        for (x, h), y in zip(studies, ROW_Y)
    ]


def pooled(studies, multipliers=None):
    effects, half_widths = np.array(studies).T
    weights = half_widths ** -2
    if multipliers is not None:
        weights *= multipliers
    return float(np.average(effects, weights=weights))


def diamond(x, filled=True):
    y = SUMMARY_Y
    return Polygon(
        p(x - 0.41, y), p(x, y + 0.22), p(x + 0.41, y), p(x, y - 0.22),
        stroke_color=YELLOW, stroke_width=3.5, fill_color=YELLOW,
        fill_opacity=0.96 if filled else 0,
    )


def candidates():
    return VGroup(diamond(0, filled=False), diamond(pooled(PREDICTION), filled=False))


def tethers(studies, target):
    return VGroup(*[
        Line(p(x, y), p(target, SUMMARY_Y), color=row_color(h),
             stroke_width=2 + 3.0 / h, stroke_opacity=min(0.72, 0.32 / h))
        for (x, h), y in zip(studies, ROW_Y)
    ])


def focus_ticks(x, h, y, color):
    return VGroup(*[
        Line(p(x + h * offset, y - 0.23), p(x + h * offset, y - 0.12),
             color=color, stroke_width=3)
        for offset in (-0.72, -0.36, 0.36, 0.72)
    ])


def study_card(x, y):
    card = RoundedRectangle(
        width=0.68, height=0.43, corner_radius=0.07,
        stroke_color=BLUE, stroke_width=3, fill_color=PANEL, fill_opacity=1,
    ).move_to(p(x, y))
    marks = VGroup(*[
        Line(p(x - 0.20, y + dy), p(x + length, y + dy),
             color=BLUE, stroke_width=3)
        for dy, length in ((0.08, 0.17), (-0.07, 0.07))
    ])
    return VGroup(card, marks)


def search_gate():
    gate = field(6.4, 0.57, p(0, 0.38))
    slots = VGroup(*[
        RoundedRectangle(width=0.76, height=0.21, corner_radius=0.07,
                         stroke_color=TEAL, stroke_width=3, fill_color=BG,
                         fill_opacity=1).move_to(p(x, 0.38))
        for x in (-2.4, -1.2, 0, 1.2, 2.4)
    ])
    frame = RoundedRectangle(width=6.4, height=0.57, corner_radius=0.13,
                             stroke_color=TEAL, stroke_width=3).move_to(gate)
    return VGroup(gate, slots, frame)


def lock():
    center = p(-4.36, 0.42)
    shackle = Arc(radius=0.15, start_angle=0, angle=PI,
                  color=GOLD, stroke_width=4).shift(center + UP * 0.09)
    case = RoundedRectangle(width=0.42, height=0.30, corner_radius=0.06,
                            color=GOLD, fill_opacity=0.9).move_to(center)
    return shackle, case


class S01Hook(SpokenScene):
    def construct(self):
        stage = overview()
        rows = forest()
        scattered = HOOK_Y
        for row, offset, y in zip(rows, scattered, ROW_Y):
            row.shift(UP * (offset - y))
        self.add(stage, *rows)
        trace_rows(self, stage[0])
        self.at("which answer should you trust")
        question = T("?", 58, GOLD, weight=BOLD).move_to(p(0, SUMMARY_Y))
        self.play(GrowFromCenter(question), run_time=0.65)
        self.play(Indicate(question, color=GOLD, scale_factor=1.18), run_time=1.15)
        for cue, indices in [
            ("some report a large", (0, 4)),
            ("others see little change", (2, 3)),
            ("lean the opposite way", (1,)),
        ]:
            self.at(cue)
            self.play(*[rows[i].animate.shift(UP * 0.10) for i in indices],
                      run_time=0.75, rate_func=there_and_back)
        self.at("simply counting")
        tallies = VGroup()
        for side, count in ((-1, 1), (1, 4)):
            for i in range(count):
                x = side * 4.1 + 0.14 * i
                tallies.add(Line(p(x - 0.03, -3.18), p(x + 0.03, -2.83),
                                 color=GREY, stroke_width=5))
        self.play(FadeOut(question), LaggedStart(*[Create(mark) for mark in tallies],
                                                lag_ratio=0.25), run_time=1.1)
        self.at("noisy results like sharp ones")
        self.play(Indicate(rows[1], color=GREY, scale_factor=1.05),
                  Indicate(rows[0], color=BLUE, scale_factor=1.10), run_time=1.6)
        self.at("combines their measurements", lead=0.55)
        result = diamond(pooled(EXAMPLE))
        self.play(FadeOut(tallies), *[
            TransformFromCopy(row[1], Dot(result.get_center(), 0.025, color=YELLOW),
                              remover=True)
            for row in rows
        ], run_time=2.2)
        self.play(GrowFromCenter(result), run_time=0.58)
        self.finish()


class S02Title(TitleCard):
    TITLE = "Weighing Evidence Across Studies"
    LESSON = "Meta-analysis and systematic review"

    def construct(self):
        rows = forest()
        for row, offset, y in zip(rows, HOOK_Y, ROW_Y):
            row.shift(UP * (offset - y))
        result = diamond(pooled(EXAMPLE))
        title = fit_text(self.TITLE, size=47, min_size=34, max_w=11.6,
                         font=TITLE_FONT).move_to(p(0, 3.29))
        stage = overview()
        self.add(stage, *rows, result)
        trace_rows(self, stage[0])
        self.play(FadeIn(title), FadeOut(result),
                  *[row.animate.set_y(y) for row, y in zip(rows, ROW_Y)], run_time=0.61)
        self.wait(0.72)
        self.play(FadeOut(title), run_time=0.38)


class S03Systematic(SpokenScene):
    def construct(self):
        stage = overview()
        # Dim the bands while the studies are documents, then re-use the same
        # scale and lanes as the documents become estimates.
        rows = forest()
        self.add(stage, *rows)
        trace_rows(self, stage[0])
        self.at("gather studies fairly", lead=1.85)
        cards = VGroup(*[
            study_card(x, 2.22 + 0.43 * (i % 2))
            for i, x in enumerate((-2.4, -1.2, 0, 1.2, 2.4, -3.8, 3.8))
        ])
        self.play(
            LaggedStart(*[ReplacementTransform(row, card) for row, card in zip(rows, cards)],
                        FadeIn(cards[5], shift=DOWN * 0.28), FadeIn(cards[6], shift=DOWN * 0.28),
                        lag_ratio=0.14),
            stage[0].animate.set_fill(opacity=0.68), stage[1].animate.set_opacity(0.35),
            run_time=2.75,
        )
        self.at("systematic review", lead=0.85)
        gate = search_gate()
        self.play(FadeIn(gate), run_time=0.68)
        review = wide_text("Systematic review")
        self.play(FadeIn(review), *[card.animate.shift(DOWN * 0.65) for card in cards],
                  run_time=1.75)
        self.at("preset rules")
        rules = boxed_label("preset rules", TEAL, size=30).move_to(p(4.83, 0.38))
        self.play(FadeIn(rules), run_time=0.60)
        self.at("before seeing results")
        shackle, case = lock()
        self.play(FadeIn(case), Create(shackle), run_time=0.78)
        self.at("you cannot cherry", lead=0.25)
        self.play(
            LaggedStart(*[card.animate.shift(DOWN * 2.33) for card in cards[:5]],
                        lag_ratio=0.15),
            FadeOut(cards[5], shift=LEFT * 1.20, target_position=p(-5.1, 0.57)),
            FadeOut(cards[6], shift=RIGHT * 1.20, target_position=p(5.1, 1.05)),
            run_time=2.55,
        )
        self.at("each matching study")
        dots = [estimate(x, h, y) for (x, h), y in zip(EXAMPLE, ROW_Y)]
        self.play(FadeOut(gate), FadeOut(rules), FadeOut(review), FadeOut(shackle), FadeOut(case),
                  stage[0].animate.set_fill(opacity=1), stage[1].animate.set_opacity(1),
                  run_time=0.65)
        self.play(LaggedStart(*[ReplacementTransform(card, dot) for card, dot in zip(cards, dots)],
                              lag_ratio=0.16), run_time=2.15)
        self.at("effect size")
        label = wide_text("Effect size")
        self.play(FadeIn(label), run_time=0.42)
        self.play(LaggedStart(*[Indicate(dot, color=dot.get_color(), scale_factor=1.40)
                               for dot in dots], lag_ratio=0.23), run_time=2.1)
        self.play(FadeOut(label), run_time=0.55)
        self.finish()


class S04Forest(SpokenScene):
    def construct(self):
        stage = overview()
        rows = forest()
        self.add(stage, *[row[1] for row in rows])
        trace_rows(self, stage[0])
        self.at("horizontal bar", lead=1.25)
        self.play(LaggedStart(*[GrowFromCenter(row[0]) for row in rows], lag_ratio=0.20),
                  run_time=2.6)
        self.at("stacked above one shared axis")
        sweep = Line(p(-5.8, ROW_Y[0]), p(5.8, ROW_Y[0]), color=BLUE,
                     stroke_width=3, stroke_opacity=0.65)
        self.play(FadeIn(sweep), run_time=0.25)
        self.play(sweep.animate.set_y(AXIS_Y + 0.20), run_time=2.1)
        self.play(FadeOut(sweep), run_time=0.35)
        self.at("forest plot")
        title = wide_text("Forest plot")
        self.play(FadeIn(title), run_time=0.52)
        self.at("a narrow bar")
        x, h = EXAMPLE[0]
        narrow_ticks = focus_ticks(x, h, ROW_Y[0], BLUE)
        high = boxed_label("high precision", BLUE, size=30).move_to(p(-4.20, ROW_Y[0]))
        self.play(FadeIn(narrow_ticks), Indicate(rows[0], color=BLUE, scale_factor=1.08),
                  run_time=0.84)
        self.at("high precision")
        self.play(FadeIn(high), run_time=0.38)
        self.at("random scatter is small")
        self.play(narrow_ticks.animate.stretch(1.32, 0), rate_func=there_and_back, run_time=1.62)
        self.at("a wide bar")
        x, h = EXAMPLE[1]
        wide_ticks = focus_ticks(x, h, ROW_Y[1], GREY)
        low = boxed_label("low precision", TEXT, size=30).move_to(p(4.13, ROW_Y[1]))
        self.play(FadeOut(high), FadeOut(narrow_ticks), FadeIn(wide_ticks), run_time=0.75)
        self.at("low precision")
        self.play(FadeIn(low), run_time=0.43)
        self.at("a noisy estimate", lead=0.56)
        self.play(wide_ticks.animate.stretch(1.28, 0), rate_func=there_and_back, run_time=1.25)
        self.play(FadeOut(low), FadeOut(wide_ticks), FadeOut(title), run_time=0.48)
        self.finish()


class S05Weighting(SpokenScene):
    def construct(self):
        stage = overview()
        rows = forest()
        target_rows = forest(weighted=True)
        self.add(stage, *rows)
        trace_rows(self, stage[0])
        self.at("precision sets each")
        self.play(LaggedStart(*[Transform(row[1], target[1]) for row, target in zip(rows, target_rows)],
                              lag_ratio=0.24), run_time=2.65)
        self.at("narrow bars earn")
        self.play(*[Indicate(rows[i][1], color=BLUE, scale_factor=1.27) for i in (0, 2)],
                  run_time=1.55)
        self.at("wide bars earn small ones")
        self.play(*[Indicate(rows[i][1], color=GREY, scale_factor=1.58) for i in (1, 3)],
                  run_time=1.55)
        product = T("weight × effect", 34, TEXT).move_to(p(0.85, 3.30))
        left_paren = T("sum(", 34, TEXT).next_to(product, LEFT, buff=0.10)
        right_paren = T(")", 34, TEXT).next_to(product, RIGHT, buff=0.09)
        total = T("sum(weight)", 34, TEXT).next_to(right_paren, RIGHT, buff=0.58)
        divide = T("/", 34, GOLD).move_to((right_paren.get_right() + total.get_left()) / 2)
        name = T("pooled =", 34, YELLOW).next_to(left_paren, LEFT, buff=0.38)
        formula = VGroup(name, left_paren, product, right_paren, divide, total)
        formula.set_x(0)
        self.at("multiply each effect's size")
        self.play(FadeIn(product), run_time=0.65)
        self.at("sum them")
        self.play(FadeIn(left_paren), FadeIn(right_paren), run_time=0.55)
        self.at("divide by the total weight")
        self.play(FadeIn(divide), FadeIn(total), run_time=0.62)
        self.play(FadeIn(name), run_time=0.45)
        self.at("studies by precision", lead=0.85)
        track = ValueTracker(float(np.mean([x for x, _ in EXAMPLE])))
        result = always_redraw(lambda: diamond(track.get_value()))
        pull = always_redraw(lambda: tethers(EXAMPLE, track.get_value()))
        self.add(pull, result)
        self.bring_to_front(*rows, result)
        self.at("sharp measurements pull", lead=0.50)
        self.play(track.animate.set_value(pooled(EXAMPLE)), run_time=3.2)
        pull.clear_updaters()
        result.clear_updaters()
        self.play(FadeOut(pull), FadeOut(formula), run_time=0.55)
        self.finish()


class S06Predict(SpokenScene):
    def construct(self):
        rows = forest(weighted=True)
        targets = forest(PREDICTION, weighted=True)
        result = diamond(pooled(EXAMPLE))
        stage = overview()
        self.add(stage, *rows, result)
        trace_rows(self, stage[0], release=0.22, tail=0.30)
        self.at("now test this rule")
        self.play(FadeOut(result), run_time=0.44)
        self.at("most rows are noisy", lead=1.85)
        self.play(LaggedStart(*[Transform(rows[i], targets[i]) for i in (0, 2, 4)],
                              lag_ratio=0.45), run_time=3.2)
        self.at("wide bars near zero")
        self.play(*[Indicate(rows[i], color=GREY, scale_factor=1.035) for i in (0, 2, 4)],
                  run_time=1.28)
        self.at("only a few rows")
        self.play(LaggedStart(*[Transform(rows[i], targets[i]) for i in (1, 3)],
                              lag_ratio=0.50), run_time=2.65)
        self.at("if you wait by precision")
        options = candidates()
        self.play(LaggedStart(*[FadeIn(d, shift=UP * 0.12) for d in options], lag_ratio=0.60),
                  run_time=1.38)
        self.at("where does the pool diamond")
        self.play(FadeIn(question_card(QUESTION, **QUESTION_STYLE)), run_time=0.65)
        self.finish()


class S07Pause(PredictPause):
    """Use the shared question layout and hold the exact prediction frame."""
    QUESTION = QUESTION
    CARD = QUESTION_STYLE
    SECONDS = 4.5

    def backdrop(self):
        return VGroup(overview(), *forest(PREDICTION, weighted=True), candidates())

    def construct(self):
        self.add(self.backdrop(), question_card(self.QUESTION, **self.CARD))
        self.wait(self.SECONDS)


class S08Resolve(SpokenScene):
    def construct(self):
        stage = overview()
        rows = forest(PREDICTION, weighted=True)
        choices = candidates()
        question = question_card(QUESTION, **QUESTION_STYLE)
        self.add(stage, *rows, choices, question)
        trace_rows(self, stage[0])
        self.at("the diamond lands")
        result = diamond(pooled(PREDICTION))
        self.play(FadeOut(choices[0]), Transform(choices[1], result), FadeOut(question),
                  run_time=1.20)
        self.at("wide bar studies outnumber")
        self.play(LaggedStart(*[Indicate(rows[i], color=GREY, scale_factor=1.025)
                                for i in (0, 2, 4)], lag_ratio=0.32), run_time=2.45)
        self.at("large uncertainty shrinks")
        lines = tethers(PREDICTION, pooled(PREDICTION))
        self.play(LaggedStart(*[Create(lines[i]) for i in (1, 3, 0, 2, 4)], lag_ratio=0.12),
                  *[rows[i].animate.set_opacity(0.42) for i in (0, 2, 4)], run_time=2.28)
        self.bring_to_front(*rows, choices[1])
        self.at("a simple vote count")
        self.play(FadeOut(lines), *[rows[i].animate.set_opacity(1) for i in (0, 2, 4)],
                  Indicate(choices[1], color=YELLOW, scale_factor=1.25), run_time=2.35)
        self.finish()


class S09Limits(SpokenScene):
    def construct(self):
        rows = forest(PREDICTION, weighted=True)
        stage = overview()
        published = pooled(PREDICTION)
        full = pooled(PREDICTION + MISSING)
        dominant_weight = 5.0
        dominant = pooled(PREDICTION, [1, 1, 1, dominant_weight, 1])
        result = diamond(published)
        ghosts = VGroup(*[
            VGroup(interval(x, h, y, RED), estimate(x, h, y, weighted=True, color=RED))
            .set_opacity(0.58)
            for (x, h), y in zip(MISSING, (ROW_Y[0] + 0.22, ROW_Y[2] + 0.24))
        ])
        self.add(stage, *rows, result)
        trace_rows(self, stage[0])
        self.at("pooling cannot rescue")
        self.play(FadeIn(ghosts, shift=LEFT * 0.38), result.animate.set_x(full), run_time=2.1)
        self.at("studies with weak results")
        unpublished = wide_text("Unpublished", x=-3.8, color=RED, size=32)
        self.play(FadeIn(unpublished), run_time=0.57)
        self.at("stay unpublished")
        self.play(FadeOut(ghosts, shift=LEFT * 0.38), FadeOut(unpublished),
                  result.animate.set_x(published), run_time=1.02)
        self.at("one population dominates", lead=0.10)
        self.play(rows[3][1].animate.scale(np.sqrt(dominant_weight)), run_time=1.12)
        self.at("the diamond tilts")
        self.play(result.animate.set_x(dominant), run_time=1.65)
        self.at("clean trends across studies")
        self.play(LaggedStart(*[Indicate(rows[i][1], color=BLUE, scale_factor=1.12)
                               for i in (1, 3)], lag_ratio=0.5), run_time=1.5)
        self.at("correlation", lead=0)
        correlation = wide_text("Correlation only", color=GOLD, size=35)
        self.play(FadeIn(correlation), run_time=0.56)
        self.at("reviewers guard against bias")
        scan = Line(p(-5.78, ROW_Y[0] + 0.3), p(5.78, ROW_Y[0] + 0.3),
                    color=TEAL, stroke_width=4)
        self.play(FadeIn(scan), run_time=0.26)
        self.play(scan.animate.set_y(AXIS_Y + 0.13), run_time=1.47)
        self.play(FadeOut(scan), run_time=0.25)
        self.at("search rules up front")
        rules = wide_text("Preset rules", color=TEAL, size=35)
        self.play(swap(correlation, rules, run_time=0.72))
        self.at("checking study design")
        design = wide_text("Study design", color=TEAL, size=35)
        self.play(swap(rules, design, run_time=0.72), rows[3][1].animate.scale(1 / np.sqrt(dominant_weight)),
                  result.animate.set_x(published), run_time=0.85)
        self.at("stating those limits")
        self.play(swap(design, correlation, run_time=0.72))
        self.play(FadeOut(correlation), run_time=0.45)
        self.finish()


def chen_citation():
    return wide_text("Chen, Thomas et al. 2011", x=-2.4, color=GOLD, size=36)


def pecl_citation():
    return wide_text("Pecl et al. 2017", x=3.71, color=GOLD, size=36)


def association_label():
    return caption("Correlation across studies", size=30, color=GOLD)


def warming_plot():
    """Qualitative positive association, with no numerical data implied."""
    plot = Plot(
        box=(-5.77, 0.51, -1.98, 2.02), xr=(0, 1), yr=(0, 1),
        label_size=30, xlabel="Regional warming", color=TEXT,
    )
    bands = VGroup(*[
        field(6.19, 0.76, p(-2.61, -1.50 + i * 0.82),
              PANEL if i % 2 == 0 else ALT_PANEL)
        for i in range(5)
    ])
    label = T("Range shift", 28, TEXT).move_to(p(-4.6, 2.49))
    return plot, VGroup(bands, plot, label)


def climate_points(plot, heights):
    return [Dot(plot.pt(x, y), radius=0.105, color=BLUE)
            for x, y in zip(WARMING_X, heights)]


def climate_nodes():
    points = [p(3.61, 1.28), p(3.61, -0.12), p(3.61, -1.52)]
    nodes = VGroup(*[
        boxed_label(word, PURPLE, size=31, box=(3.48, 0.70), fill_opacity=0.18)
        .move_to(where)
        for word, where in zip(("communities", "ecosystems", "well-being"), points)
    ])
    trunk_x = 1.35
    trunk = Line(p(trunk_x, points[-1][1]), p(trunk_x, points[0][1]),
                 stroke_width=4, color=PURPLE)
    branches = VGroup(*[
        Line(p(trunk_x, center[1]), p(1.72, center[1]), color=PURPLE, stroke_width=4)
        for center in points
    ])
    inlet = Line(p(0.70, -0.12), p(trunk_x, -0.12), color=PURPLE, stroke_width=4)
    return nodes, trunk, branches, inlet


class S10UnlockedClimate(SpokenScene):
    def construct(self):
        stage = overview()
        rows = forest(PREDICTION, weighted=True)
        result = diamond(pooled(PREDICTION))
        tag = stage[-1]
        stage.remove(tag)
        self.add(stage, *rows, result, tag)
        trace_rows(self, stage[0])
        self.at("in 2011")
        citation = chen_citation()
        self.play(FadeIn(citation), run_time=0.85)
        self.at("pooled published range shifts")
        plot, warming = warming_plot()
        points = climate_points(plot, (0.13,) * len(WARMING_X))
        self.play(FadeOut(stage), FadeOut(result), FadeIn(warming),
                  *[ReplacementTransform(row, dot) for row, dot in zip(rows, points)],
                  run_time=2.45)
        trace_rows(self, warming[0], strength=0.72)
        self.at("shifts were greatest")
        self.play(LaggedStart(*[dot.animate.move_to(plot.pt(x, y))
                                for dot, x, y in zip(points, WARMING_X, SHIFT_Y)],
                               lag_ratio=0.20), run_time=3.25)
        self.at("correlation across studies")
        association = association_label()
        self.play(FadeIn(association),
                  Indicate(points[-1], color=BLUE, scale_factor=1.50), run_time=1.4)
        self.at("in 2017")
        pecl = pecl_citation()
        self.play(FadeIn(pecl), run_time=0.72)
        nodes, trunk, branches, inlet = climate_nodes()
        self.at("climate driven redistribution", lead=0.45)
        self.play(Create(inlet), Create(trunk), run_time=1.45)
        for cue, node, branch in zip(
            ("alters communities", "ecosystem functioning", "human wellbeing"),
            nodes, branches,
        ):
            self.at(cue, lead=0.45)
            self.play(Create(branch), run_time=0.38)
            self.play(FadeIn(node), run_time=0.52)
        self.finish()


def proportion_track(y):
    return field(10.8, 0.55, p(0, y))


def fraction_fill(fraction, y, color):
    length = 10.8 * fraction
    bar = field(length, 0.55, p(-5.4 + length / 2, y), color)
    return bar


def niche_bars():
    return VGroup(*[proportion_track(y) for y in (1.50, -0.21, -1.92)])


def niche_title():
    return wide_text("2014 transplant review", color=GOLD)


def niche_match():
    return VGroup(fraction_fill(NICHES[0], 1.50, GREEN),
                  T("46% niche limit", 34, GREEN).move_to(p(-2.90, 2.13)))


def niche_survival():
    return VGroup(
        fraction_fill(NICHES[1], -0.21, BLUE),
        T("26% survived beyond range", 34, BLUE).move_to(p(-2.20, 0.43)),
        T("Mostly north–south or east–west limits", 28, TEXT).move_to(p(2.5, -0.86)),
    )


class S11UnlockedNiches(SpokenScene):
    def construct(self):
        plot, warming = warming_plot()
        nodes, trunk, branches, inlet = climate_nodes()
        climate_labels = VGroup(
            chen_citation(), pecl_citation(), association_label(),
            scope_tag("schematic", size=28, color=TEXT),
        )
        points = VGroup(*climate_points(plot, SHIFT_Y))
        plot_detail = VGroup(warming[1], warming[2], points)
        connections = VGroup(trunk, *branches, inlet, nodes)
        self.add(warming[0], plot_detail, connections, climate_labels)
        self.at("a 2014 review")
        self.play(FadeOut(climate_labels), FadeOut(connections), FadeOut(plot_detail),
                  run_time=0.46)
        title = niche_title()
        bars = niche_bars()
        self.play(FadeIn(title), ReplacementTransform(warming[0], bars), run_time=0.96)
        trace_rows(self, bars, strength=0.83)
        self.at("plant transplant tests")
        # A document crosses the dashed range border in a small schematic
        # beside the tracks. The tracks themselves are on a 0–100% scale.
        border = DashedLine(p(4.10, -2.72), p(4.10, 0.98), color=GREY, stroke_width=3)
        transplant = study_card(3.43, -1.05)
        self.play(Create(border), FadeIn(transplant), run_time=0.68)
        self.at("across range borders")
        self.play(transplant.animate.set_x(4.80), run_time=1.28)
        self.play(FadeOut(transplant), FadeOut(border), run_time=0.42)
        match = niche_match()
        self.at("46 percent", lead=0.36)
        self.play(GrowFromEdge(match[0], LEFT), run_time=1.36)
        self.at("matched a niche limit", lead=0.42)
        self.play(FadeIn(match[1]), run_time=0.63)
        self.at("conditions turned unsuitable")
        boundary = Line(p(match[0].get_right()[0], 1.13), p(match[0].get_right()[0], 1.86),
                        color=RED, stroke_width=4)
        self.play(Create(boundary), run_time=0.82)
        self.play(FadeOut(boundary), run_time=0.52)
        survival = niche_survival()
        self.at("26 percent")
        self.play(GrowFromEdge(survival[0], LEFT), run_time=1.10)
        self.at("mostly north south")
        self.play(FadeIn(survival[2]), run_time=0.68)
        self.at("transplants survived beyond")
        self.play(FadeIn(survival[1]), run_time=0.72)
        self.finish()


class S11bUnlockedNiches(SpokenScene):
    def construct(self):
        title = niche_title()
        bars = niche_bars()
        match, survival = niche_match(), niche_survival()
        self.add(bars, title, match, survival)
        trace_rows(self, bars, strength=0.83)
        third = VGroup(
            fraction_fill(NICHES[2], -1.92, PURPLE),
            T("23% past niche limit", 34, PURPLE).move_to(p(-2.72, -1.29)),
            T("All at elevation limits", 28, TEXT).move_to(p(3.10, -2.53)),
        )
        self.at("in 23")
        self.play(GrowFromEdge(third[0], LEFT), run_time=1.27)
        self.at("all at elevation limits")
        self.play(FadeIn(third[2]), run_time=0.73)
        self.at("ran past the niche limit")
        self.play(FadeIn(third[1]), run_time=0.65)
        self.at("the shares do not add")
        note = caption("Shares do not add to 100%", size=30)
        self.play(FadeIn(note), run_time=0.57)
        self.at("gathering every test")
        stage = overview()
        rows = forest(PREDICTION, weighted=True)
        self.play(FadeOut(title), FadeOut(note), FadeOut(match), FadeOut(survival),
                  FadeOut(third), run_time=0.46)
        bars.clear_updaters()
        self.play(ReplacementTransform(bars, stage[0]), FadeIn(VGroup(*stage[1:])),
                  run_time=0.85)
        trace_rows(self, stage[0])
        self.play(LaggedStart(*[FadeIn(row, shift=DOWN * 0.18) for row in rows], lag_ratio=0.22),
                  run_time=2.07)
        self.at("clearer pattern")
        result = diamond(pooled(PREDICTION))
        self.play(GrowFromCenter(result), run_time=0.83)
        self.finish()


class S12End(EndCard):
    LINE = "Weight studies by precision, not votes, to measure the shared effect."
