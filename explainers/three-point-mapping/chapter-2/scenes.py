"""Do Crossovers Act Independently? — Three-point mapping, chapter 2.

COLOR MAP (kept for the whole chapter pair)
  BLUE  = one parental chromosome
  GOLD  = the other parental chromosome
  GREEN = the middle marker C
  RED   = crossover events and double-crossover bars
  GREY  = structure, rulers, and scope
  TEXT  = neutral labels
"""
from bp_parts import *  # noqa: F401,F403


MAP_X = (-4.7, 0.0, 4.7)


def chromosome_world(y=1.55, width=10.6, labels=True, crossovers=True):
    """The carried chapter-pair picture, always rebuilt at the same scale and place."""
    left, right = -width / 2, width / 2
    top_y, bot_y = y + 0.68, y - 0.68
    ribbons = VGroup(
        RoundedRectangle(width=width, height=0.86, corner_radius=0.18,
                         stroke_color=BLUE, stroke_width=3, fill_color=BLUE, fill_opacity=0.42).move_to([0, top_y, 0]),
        RoundedRectangle(width=width, height=0.86, corner_radius=0.18,
                         stroke_color=GOLD, stroke_width=3, fill_color=GOLD, fill_opacity=0.42).move_to([0, bot_y, 0]),
    )
    middle = VGroup(*[
        RoundedRectangle(width=0.72, height=0.70, corner_radius=0.12,
                         stroke_color=GREEN, stroke_width=4, fill_color=GREEN, fill_opacity=0.75).move_to([0, yy, 0])
        for yy in (top_y, bot_y)
    ])
    g = VGroup(ribbons, middle)
    g.ribbons, g.middle = ribbons, middle
    if labels:
        labs = VGroup(T("A", 30), T("C", 30, GREEN), T("B", 30))
        label_y = y + 1.50
        for lab, x in zip(labs, (-4.25, 0, 4.25)):
            lab.move_to([x, label_y, 0])
        g.add(labs)
        g.labels = labs
    if crossovers:
        points = VGroup(*[
            VGroup(Circle(radius=0.20, color=RED, stroke_width=6), Dot(radius=0.075, color=RED)).move_to([x, y, 0])
            for x in (-1.65, 1.65)
        ])
        g.add(points)
        g.crossovers = points
    return g


def comparison_bars(expected=2.25, observed=1.25, base=-2.15, x_expected=2.1, x_observed=4.55,
                    labels=True):
    """Expected outline and observed solid bar, used unchanged across the interference story."""
    ew, ow = 1.6, 1.6
    exp = RoundedRectangle(width=ew, height=expected, corner_radius=0.10,
                           stroke_color=RED, stroke_width=4, fill_opacity=0).move_to([x_expected, base + expected / 2, 0])
    obs = RoundedRectangle(width=ow, height=max(observed, 0.04), corner_radius=0.10,
                           stroke_color=RED, stroke_width=3, fill_color=RED, fill_opacity=0.72).move_to(
                               [x_observed, base + max(observed, 0.04) / 2, 0])
    g = VGroup(exp, obs)
    g.expected, g.observed = exp, obs
    if labels:
        labs = VGroup(T("expected\ndoubles", 28, RED, line_spacing=0.8).next_to(exp, DOWN, buff=0.16),
                      T("observed\ndoubles", 28, RED, line_spacing=0.8).next_to(obs, DOWN, buff=0.16))
        g.add(labs)
        g.labels = labs
    return g


def predict_backdrop():
    chrom = chromosome_world(y=1.95, width=10.6)
    bars = comparison_bars(base=-2.10)
    return VGroup(chrom, bars, scope_tag("schematic"))


def ruler_line(y, color=GREY, ticks=(-5.4, -2.7, 0, 2.7, 5.4), width=10.8):
    line = VGroup(*[Line([-width / 2, y + dy, 0], [width / 2, y + dy, 0], color=color,
                         stroke_width=5, stroke_opacity=0.55) for dy in np.linspace(-0.18, 0.18, 5)])
    marks = VGroup(*[Line([x, y - 0.28, 0], [x, y + 0.28, 0], color=color, stroke_width=6) for x in ticks])
    return VGroup(line, marks)


def rulers_world(show_sparks=True):
    """The carried two-ruler picture for scenes 11–13."""
    genetic = ruler_line(1.25, BLUE, ticks=(-5.4, -3.9, -0.5, 1.0, 5.4))
    dna = ruler_line(-1.05, GREY, ticks=(-5.4, -2.7, 0, 2.7, 5.4))
    gl = T("genetic map: crossover frequency", 30, BLUE).move_to([0, 2.15, 0])
    dl = T("DNA sequence: physical length", 30, TEXT).move_to([0, -1.95, 0])
    g = VGroup(genetic, dna, gl, dl)
    g.genetic, g.dna = genetic, dna
    if show_sparks:
        sparks = VGroup(*[
            VGroup(Line(UL * 0.14, DR * 0.14, color=RED, stroke_width=5),
                   Line(DL * 0.14, UR * 0.14, color=RED, stroke_width=5)).move_to([x, 0.05 + 0.10 * (i % 2), 0])
            for i, x in enumerate((-3.8, -0.1, 0.25, 0.58, 0.9, 3.5))
        ])
        g.add(sparks)
        g.sparks = sparks
    return g


class S00LinkAndQuestion(SpokenScene):
    def construct(self):
        chrom = chromosome_world(y=0.55, width=10.8)
        self.play(FadeIn(chrom.ribbons), run_time=0.8)
        self.at("middle marker")
        self.play(FadeIn(chrom.middle), FadeIn(chrom.labels), run_time=0.7)
        self.at("double crossovers")
        self.play(FadeIn(chrom.crossovers), run_time=0.6)
        pulse(chrom.crossovers[0], base=5.5, amp=2.0, speed=2.2)
        pulse(chrom.crossovers[1], base=5.5, amp=2.0, speed=2.0)
        self.at("Do those doubles")
        q = fit_text("As often as independence predicts?", max_w=11.5, size=40, color=TEXT).move_to([0, 3.15, 0])
        self.play(FadeIn(q, shift=DOWN * 0.12), run_time=0.8)
        bob(chrom.ribbons, amp=0.10, speed=0.75)
        self.at("same blue and gold")
        self.play(Indicate(chrom.ribbons[0], color=BLUE), Indicate(chrom.ribbons[1], color=GOLD), run_time=1.2)
        self.at("green middle marker")
        self.play(Indicate(chrom.middle, color=GREEN), run_time=0.7)
        self.at("red crossover points")
        self.play(Indicate(chrom.crossovers, color=RED), run_time=0.8)
        self.add(scope_tag("schematic"))
        self.finish()


class S01Title(NarratedScene):
    def construct(self):
        chrom = chromosome_world(y=0.25, width=10.8)
        q = fit_text("As often as independence predicts?", max_w=11.5, size=36).move_to([0, 3.0, 0])
        self.add(chrom, q, scope_tag("schematic"))
        title = fit_text("Do Crossovers Act Independently?", max_w=12, size=50, font=TITLE_FONT).move_to([0, 3.0, 0])
        self.play(swap(q, title, run_time=0.9),
                  chrom.crossovers.animate.scale(1.12), rate_func=there_and_back, run_time=0.9)
        self.finish()


class S02Independence(SpokenScene):
    def construct(self):
        chrom = chromosome_world(y=1.95, width=10.6)
        self.add(chrom)
        bob(chrom.ribbons, amp=0.10, speed=0.72)
        left = chip("event", RED, 28).move_to([-3.5, 0.35, 0])
        right = chip("event", RED, 28).move_to([0.3, 0.35, 0])
        self.at("crossover in each interval")
        self.play(FadeIn(left, shift=DOWN * 0.5), run_time=0.7)
        self.play(FadeIn(right, shift=DOWN * 0.5), run_time=0.7)
        mult = T("×", 54, TEXT).move_to([-1.58, -0.65, 0])
        self.at("Under independence")
        self.play(left.animate.move_to([-2.7, -0.65, 0]), right.animate.move_to([-0.45, -0.65, 0]), FadeIn(mult), run_time=1.0)
        beads = VGroup(*[Dot(radius=0.13, color=RED) for _ in range(12)]).arrange_in_grid(4, 3, buff=0.14)
        beads.move_to([3.7, -0.8, 0])
        self.at("multiply the two")
        self.play(ReplacementTransform(VGroup(left, right, mult), beads), run_time=1.1)
        outline = RoundedRectangle(width=2.3, height=2.5, corner_radius=0.12, stroke_color=RED,
                                   stroke_width=4).move_to([3.7, -0.8, 0])
        lab = T("expected doubles", 30, RED).next_to(outline, DOWN, buff=0.2)
        self.at("product fills")
        self.play(Create(outline), beads.animate.arrange_in_grid(4, 3, buff=0.25).move_to(outline), run_time=1.2)
        self.play(FadeIn(lab), run_time=0.5)
        self.at("marked schematic")
        self.play(FadeIn(scope_tag("schematic")), run_time=0.4)
        self.finish()


class S03Predict(SpokenScene):
    def construct(self):
        chrom = chromosome_world(y=1.95, width=10.6)
        bars = comparison_bars(observed=0.05, base=-2.1)
        self.add(chrom, bars.expected, bars.labels[0], scope_tag("schematic"))
        bob(chrom.ribbons, amp=0.10, speed=0.8)
        self.at("compare an observed bar")
        self.play(FadeIn(bars.labels[1]), FadeIn(bars.observed), run_time=0.8)
        target = comparison_bars(observed=1.25, base=-2.1).observed
        self.at("observed bar is shorter")
        self.play(Transform(bars.observed, target), run_time=1.2)
        q = question_card("Positive or negative interference?", y=0.45, size=36, max_w=7.4)
        self.at("Does that mean")
        self.play(FadeIn(q.question, shift=DOWN * 0.12), run_time=0.8)
        self.finish()


class S04PredictPause(PredictPause):
    QUESTION = "Positive or negative interference?"
    SECONDS = 4.5
    CARD = {"y": 0.45, "size": 36, "max_w": 7.4}
    RING_AT = (6.0, -1.65, 0)

    def backdrop(self):
        g = predict_backdrop()
        pulse(g[1].expected, base=4.0, amp=1.0, speed=1.5)
        pulse(g[1].observed, base=3.0, amp=0.8, speed=1.7)
        bob(g[0].ribbons, amp=0.035, speed=1.0)
        return g


class S05Positive(SpokenScene):
    def construct(self):
        chrom = chromosome_world(y=2.07, width=10.6)
        bars = comparison_bars(base=-2.1)
        q = question_card("Positive or negative interference?", y=0.45, size=36, max_w=7.4).question
        schematic = scope_tag("schematic")
        self.add(chrom, bars, q, schematic)
        bob(chrom.ribbons, amp=0.10, speed=0.78)
        self.at("Fewer doubles")
        self.play(Indicate(bars.observed, color=RED), Indicate(bars.expected, color=RED), run_time=1.0)
        answer = T("positive interference", 38, GREEN).move_to(q).shift(LEFT * 0.45)
        self.at("positive interference")
        self.play(swap(q, answer, run_time=0.8))
        self.at("crossover in one interval")
        self.play(Indicate(chrom.crossovers[0], color=RED, scale_factor=1.5), run_time=0.8)
        arrow = Arrow([1.65, 0.72, 0], [1.65, 0.12, 0], color=GREEN, stroke_width=7, buff=0.05)
        fewer = T("fewer nearby", 30, GREEN).move_to([4.0, 0.40, 0])
        self.at("fewer in its neighbor")
        self.play(GrowArrow(arrow), FadeIn(fewer), chrom.crossovers[1].animate.set_opacity(0.35), run_time=1.0)
        tag = scope_tag("association, not mechanism", size=24)
        self.at("shows association")
        self.play(swap(schematic, tag, run_time=0.7))
        self.at("not a molecular cause")
        self.play(Indicate(tag, color=GREY), run_time=0.8)
        self.finish()


class S06Measures(SpokenScene):
    def construct(self):
        exp = RoundedRectangle(width=2.5, height=0.85, corner_radius=0.12, color=RED, stroke_width=4)
        obs = RoundedRectangle(width=1.55, height=0.85, corner_radius=0.12, color=RED, stroke_width=3,
                               fill_color=RED, fill_opacity=0.72)
        frac = VGroup(obs, Line(LEFT * 1.5, RIGHT * 1.5, color=TEXT, stroke_width=4), exp).arrange(DOWN, buff=0.22)
        frac.move_to([-2.10, 0.35, 0])
        flabs = VGroup(T("observed doubles", 28, RED).next_to(obs, LEFT, buff=0.25),
                       T("expected doubles", 28, RED).next_to(exp, LEFT, buff=0.25),
                       T("coincidence", 34, BLUE).next_to(frac, UP, buff=0.38))
        fraction_world = VGroup(frac[1], exp, flabs)
        self.at("observed doubles divided")
        self.play(FadeIn(obs), FadeIn(flabs[0]), run_time=0.7)
        self.play(Create(frac[1]), FadeIn(exp), FadeIn(flabs[1]), FadeIn(flabs[2]), run_time=0.9)
        coincidence = ValueTracker(0.55)
        interference = ValueTracker(0.45)
        gauge = dial(interference, center=[3.35, 0.45, 0], radius=1.55,
                     label="interference", color=GREEN, fmt="{:.2f}", scale=1.0, size=38)
        rule = T("1 − coincidence", 30, GREEN).move_to([3.35, 2.65, 0])
        self.at("Interference is the complement")
        self.play(FadeIn(gauge), FadeIn(rule), run_time=1.0)
        brace = BraceBetweenPoints([-5.5, -2.0, 0], [5.5, -2.0, 0], direction=DOWN, color=GREY)
        pair = T("one paired comparison", 30, TEXT).next_to(brace, DOWN, buff=0.12)
        self.at("Keep the pair together")
        self.play(Create(brace), FadeIn(pair), run_time=0.8)
        self.at("what appeared")
        self.play(coincidence.animate.set_value(0.75), interference.animate.set_value(0.25),
                  obs.animate.stretch_to_fit_width(2.15), fraction_world.animate.shift(UP * 0.20),
                  run_time=1.7, rate_func=there_and_back)
        self.at("departure from independence")
        self.play(interference.animate.set_value(0.60), obs.animate.stretch_to_fit_width(1.2),
                  fraction_world.animate.shift(DOWN * 0.20), run_time=1.4, rate_func=there_and_back)
        self.finish()


class S07ThreeCases(SpokenScene):
    def construct(self):
        chrom = chromosome_world(y=1.90, width=10.2)
        expected_h, base = 2.15, -2.25
        expected = RoundedRectangle(width=1.8, height=expected_h, corner_radius=0.10,
                                    stroke_color=RED, stroke_width=4).move_to([-1.25, base + expected_h / 2, 0])
        h = ValueTracker(1.1)
        observed = always_redraw(lambda: RoundedRectangle(width=1.8, height=max(h.get_value(), 0.05), corner_radius=0.10,
                                  stroke_color=RED, stroke_width=3, fill_color=RED, fill_opacity=0.72).move_to(
                                      [1.25, base + max(h.get_value(), 0.05) / 2, 0]))
        labs = VGroup(T("expected", 28, RED).next_to(expected, DOWN, buff=0.2),
                      T("observed", 28, RED).move_to([1.25, -2.68, 0]))
        state = T("positive", 38, GREEN).move_to([4.35, -0.9, 0])
        self.add(chrom, expected, observed, labs)
        bob(chrom.ribbons, amp=0.10, speed=0.76)
        self.at("Three comparisons")
        self.play(FadeIn(state), run_time=0.7)
        self.at("Observed below expected")
        self.play(h.animate.set_value(1.1), Indicate(state, color=GREEN), run_time=1.0)
        none = T("none", 38, TEXT).move_to(state)
        self.at("Equal bars")
        self.play(h.animate.set_value(expected_h), swap(state, none), run_time=1.2)
        negative = T("negative: excess", 36, RED).move_to(state)
        self.at("Observed above expected")
        self.play(h.animate.set_value(2.8), swap(none, negative), run_time=1.3)
        pin = VGroup(Dot(radius=0.14, color=TEXT), Triangle(color=TEXT, fill_color=TEXT, fill_opacity=1).scale(0.12))
        pin[1].next_to(pin[0], DOWN, buff=-0.03)
        pin.move_to([-3.2, 1.9, 0])
        self.at("reported in some fungal")
        self.play(FadeIn(pin), pin.animate.shift(RIGHT * 2.1), run_time=1.5)
        self.at("No single value")
        self.play(pin.animate.shift(RIGHT * 2.8), run_time=1.4)
        self.finish()


class S08IntervalScope(SpokenScene):
    def construct(self):
        chrom = chromosome_world(y=0.85, width=8.4, labels=False)
        species = T("one organism", 32, TEXT).move_to([0, 3.15, 0])
        left_br = BraceBetweenPoints([-1.6, -0.52, 0], [0, -0.52, 0], direction=DOWN, color=GREEN)
        right_br = BraceBetweenPoints([0, -0.52, 0], [1.6, -0.52, 0], direction=DOWN, color=GREEN)
        pair_lab = T("this interval pair", 30, GREEN).move_to([0, -1.20, 0])
        expected = RoundedRectangle(width=1.45, height=2.0, corner_radius=0.1, color=RED, stroke_width=4).move_to([4.7, -1.15, 0])
        observed = RoundedRectangle(width=1.45, height=1.15, corner_radius=0.1, color=RED, stroke_width=3,
                                    fill_color=RED, fill_opacity=0.72).align_to(expected, DOWN).move_to([2.65, -1.58, 0])
        self.add(chrom, species, left_br, right_br, pair_lab, expected, observed, scope_tag("schematic"))
        self.at("intervals lie farther apart")
        self.play(chrom.animate.stretch(1.35, 0),
                  left_br.animate.stretch(1.65, 0).shift(LEFT * 0.5),
                  right_br.animate.stretch(1.65, 0).shift(RIGHT * 0.5), run_time=2.2)
        bob(chrom.ribbons, amp=0.10, speed=0.74)
        target = observed.copy().stretch_to_fit_height(1.9).align_to(expected, DOWN)
        self.at("approach the independent expectation")
        self.play(Transform(observed, target), run_time=1.8)
        self.at("belongs to one pair")
        self.play(Indicate(VGroup(left_br, right_br, pair_lab), color=GREEN), run_time=1.0)
        whole = T("not a whole species", 30, GREY).move_to([0, -2.55, 0])
        self.at("not to a whole species")
        self.play(FadeIn(whole), Indicate(species, color=GREY), run_time=0.9)
        self.finish()


class S09Sampling(SpokenScene):
    def construct(self):
        expected = RoundedRectangle(width=1.8, height=2.25, corner_radius=0.1, color=RED, stroke_width=4).move_to([0, 0.2, 0])
        observed = RoundedRectangle(width=1.8, height=1.2, corner_radius=0.1, color=RED, stroke_width=3,
                                    fill_color=RED, fill_opacity=0.72).align_to(expected, DOWN)
        headline = T("one cross = an estimate", 38, TEXT).move_to([0, 3.15, 0])
        self.play(FadeIn(headline), FadeIn(expected), FadeIn(observed), run_time=0.9)
        self.at("not a law")
        self.play(Indicate(headline, color=GOLD), run_time=0.8)
        zero = T("zero observed?", 34, RED).move_to([0, -1.7, 0])
        self.at("zero observed bar")
        self.play(observed.animate.stretch_to_fit_height(0.05).align_to(expected, DOWN), FadeIn(zero), run_time=1.0)
        cards = VGroup(chip("strong interference", GREY, 27).move_to([-4.25, 0.8, 0]),
                       chip("small sample", GREY, 27).move_to([4.15, 0.8, 0]),
                       chip("missing classes", GREY, 27).move_to([0, 2.0, 0]))
        self.at("strong interference")
        self.play(FadeIn(cards[0], shift=RIGHT * 0.3), run_time=0.6)
        self.at("small sample")
        self.play(FadeIn(cards[1], shift=LEFT * 0.3), run_time=0.6)
        self.at("missing classes")
        self.play(FadeIn(cards[2], shift=DOWN * 0.3), run_time=0.6)
        self.play(Rotate(cards, angle=0.22, about_point=ORIGIN), run_time=1.0)
        checks = VGroup(T("✓ survival", 30, GREEN), T("✓ scoring", 30, GREEN)).arrange(DOWN, aligned_edge=LEFT, buff=0.3)
        checks.move_to([-4.2, -2.2, 0])
        tray = RoundedRectangle(width=4.3, height=1.15, corner_radius=0.14, color=BLUE, stroke_width=3).move_to([3.55, -2.0, 0])
        offspring = VGroup(*[RoundedRectangle(width=0.38, height=0.28, corner_radius=0.05,
                                              stroke_color=BLUE, fill_color=BLUE, fill_opacity=0.45) for _ in range(18)])
        offspring.arrange_in_grid(3, 6, buff=0.12).move_to(tray)
        self.at("Check survival and scoring")
        self.play(FadeOut(cards), FadeOut(zero), FadeIn(checks), Create(tray), run_time=0.9)
        self.at("collect more offspring")
        self.play(LaggedStart(*[FadeIn(o, shift=UP * 0.15) for o in offspring], lag_ratio=0.06), run_time=1.8)
        self.finish()


class S10GeneticDistance(SpokenScene):
    def construct(self):
        bars = comparison_bars(base=-1.85, x_expected=-1.25, x_observed=1.25)
        self.add(bars)
        chrom = chromosome_world(y=0.65, width=10.6)
        self.at("answered one question")
        self.play(ReplacementTransform(bars, chrom), run_time=1.1)
        bracket = BraceBetweenPoints([-1.65, -0.15, 0], [1.65, -0.15, 0], direction=DOWN, color=RED)
        spacing = T("spacing between crossovers", 30, RED).next_to(bracket, DOWN, buff=0.15)
        self.at("crossovers are spaced")
        self.play(Create(bracket), FadeIn(spacing), run_time=0.9)
        straight = ruler_line(0.35, BLUE, ticks=(-5.3, 0, 5.3), width=10.6)
        self.at("second question")
        self.play(FadeOut(bracket), FadeOut(spacing), ReplacementTransform(chrom, straight), run_time=1.1)
        q = question_card("Where along the DNA do crossovers fall?", y=2.55, size=38, max_w=11).question
        self.at("where along the DNA")
        self.play(FadeIn(q, shift=DOWN * 0.15), run_time=0.8)
        blank = ruler_line(-1.55, GREY, ticks=(-5.3, 0, 5.3), width=10.6)
        self.at("needs a second ruler")
        self.play(FadeIn(blank, shift=UP * 0.25), run_time=0.9)
        self.finish()


class S11TwoRulers(SpokenScene):
    def construct(self):
        world = rulers_world(show_sparks=False)
        self.at("genetic map records")
        self.play(FadeIn(world.genetic), FadeIn(world[2]), run_time=0.9)
        self.at("DNA ruler records")
        self.play(FadeIn(world.dna), FadeIn(world[3]), run_time=0.9)
        self.at("Align them")
        self.play(world.genetic.animate.shift(DOWN * 0.35), world.dna.animate.shift(UP * 0.35), run_time=1.2)
        self.play(world.genetic.animate.shift(UP * 0.35), world.dna.animate.shift(DOWN * 0.35), run_time=0.8)
        sparks = rulers_world(show_sparks=True).sparks
        hotspot = T("hotspot", 30, RED).move_to([0.45, 0.55, 0])
        self.at("not spread evenly")
        self.play(LaggedStart(*[FadeIn(s, scale=0.5) for s in sparks], lag_ratio=0.10), FadeIn(hotspot), run_time=1.4)
        bob(sparks, amp=0.10, speed=0.78)
        braces = VGroup(*[BraceBetweenPoints([a, -1.42, 0], [b, -1.42, 0], direction=DOWN, color=GREY)
                          for a, b in ((-5.4, -2.7), (-2.7, 0), (0, 2.7), (2.7, 5.4))])
        self.at("equal DNA lengths")
        self.play(LaggedStart(*[Create(b) for b in braces], lag_ratio=0.12), run_time=1.2)
        self.at("different genetic distances")
        self.play(Indicate(world.genetic[1], color=BLUE), run_time=1.0)
        self.add(scope_tag("schematic"))
        self.finish()


class S12HotspotScope(SpokenScene):
    def construct(self):
        world = rulers_world(show_sparks=True)
        self.add(world, scope_tag("schematic"))
        bob(world.sparks, amp=0.10, speed=0.74)
        pulse(world.genetic[0], base=5.0, amp=1.8, speed=1.1)
        pulse(world.dna[0], base=5.0, amp=1.5, speed=0.9)
        hotspot_box = SurroundingRectangle(VGroup(*world.sparks[1:5]), color=RED, buff=0.22, stroke_width=3)
        human_mouse = T("humans and mice", 32, TEXT).move_to([-4.2, 3.05, 0])
        hm_brace = BraceBetweenPoints([-5.7, 2.55, 0], [-2.7, 2.55, 0], direction=UP, color=TEXT)
        self.at("humans and mice")
        self.play(Create(hm_brace), FadeIn(human_mouse), run_time=0.8)
        self.at("cluster in hotspots")
        self.play(Create(hotspot_box),
                  *[s.animate.move_to([0.15 + 0.28 * i, 0.10 + 0.08 * (i % 2), 0]) for i, s in enumerate(world.sparks[1:5])],
                  run_time=1.4)
        hot = T("hotspot", 32, RED).move_to([2.30, 0.18, 0])
        self.at("short DNA stretch")
        self.play(FadeIn(hot), run_time=0.7)
        self.at("more recombination")
        self.play(Indicate(VGroup(*world.sparks[1:5]), color=RED), run_time=1.0)
        q = question_card("What chooses the positions?", y=-3.05, size=34, max_w=8.8, left=-4.5).question
        arrow = Arrow(q.get_bottom(), q.get_bottom() + DOWN * 0.35, color=GREY, buff=0.03, stroke_width=5)
        self.at("text below explains")
        self.play(FadeIn(q), GrowArrow(arrow), run_time=0.9)
        self.at("scope is not universal")
        self.play(Indicate(human_mouse, color=GREY), run_time=0.9)
        self.finish()


class S13Variation(SpokenScene):
    def construct(self):
        dna = ruler_line(-1.1, GREY, ticks=(-5.4, -2.7, 0, 2.7, 5.4))
        dna_lab = T("DNA sequence: fixed", 30, TEXT).move_to([0, -2.0, 0])
        female = ruler_line(1.2, BLUE, ticks=(-5.4, -4.0, -0.8, 1.3, 5.4))
        map_lab = T("female", 34, BLUE).move_to([0, 2.25, 0])
        sparks = VGroup(*[Dot(radius=0.11, color=RED).move_to([x, 0.25, 0]) for x in (-4.0, -1.1, 0.3, 1.4, 4.2)])
        self.add(dna, dna_lab, female, map_lab, sparks, scope_tag("schematic"))
        bob(sparks, amp=0.10, speed=0.76)
        pulse(dna[0], base=5.0, amp=1.5, speed=0.9)
        pulse(female[0], base=5.0, amp=1.8, speed=1.1)
        self.at("gamete maker")
        self.play(female.animate.stretch(1.08, 0), run_time=1.0)
        male = ruler_line(1.2, BLUE, ticks=(-5.4, -3.0, -1.8, 2.8, 5.4))
        male_lab = T("male", 34, BLUE).move_to(map_lab)
        self.at("Female and male maps")
        self.play(ReplacementTransform(female, male), swap(map_lab, male_lab),
                  *[s.animate.shift(RIGHT * (0.25 if i % 2 else -0.18)) for i, s in enumerate(sparks)], run_time=1.4)
        pulse(male[0], base=5.0, amp=1.8, speed=1.1)
        muted = RoundedRectangle(width=2.2, height=0.65, corner_radius=0.12, color=GREY,
                                 fill_color=GREY, fill_opacity=0.22).move_to([3.55, 1.2, 0])
        suppressed = T("suppressed here", 30, GREY).next_to(muted, DOWN, buff=0.2)
        self.at("regions suppress crossovers")
        self.play(FadeIn(muted), FadeIn(suppressed), FadeOut(sparks[-1]), run_time=1.0)
        self.at("without moving the underlying DNA")
        self.play(Indicate(dna, color=TEXT), run_time=1.1)
        self.finish()


class S14Rule(SpokenScene):
    def construct(self):
        rulers = rulers_world(show_sparks=True)
        self.add(rulers)
        bob(rulers.sparks, amp=0.10, speed=0.74)
        chrom = chromosome_world(y=0.55, width=10.6)
        self.at("Return to the two bars")
        self.play(ReplacementTransform(rulers, chrom), run_time=1.0)
        bars = comparison_bars(base=-1.75, x_expected=-1.25, x_observed=1.25)
        self.play(ReplacementTransform(chrom.ribbons, VGroup(bars.expected, bars.observed)),
                  FadeIn(bars.labels), FadeOut(chrom.labels), run_time=1.1)
        bracket = BraceBetweenPoints([-2.35, -2.72, 0], [2.35, -2.72, 0], direction=DOWN, color=GREEN)
        pair = T("this interval pair", 30, GREEN).next_to(bracket, DOWN, buff=0.12)
        self.at("spacing test")
        self.play(Create(bracket), FadeIn(pair), run_time=0.8)
        self.at("scope limited")
        self.play(Indicate(VGroup(bracket, pair), color=GREEN),
                  bars.observed.animate.shift(UP * 0.22), rate_func=there_and_back, run_time=1.4)
        rule = fit_text("Comparing observed and expected doubles reveals crossover spacing.",
                        max_w=11.6, size=38, color=TEXT).move_to([0, 2.75, 0])
        self.at("Comparing observed and expected")
        self.play(FadeIn(rule, shift=DOWN * 0.12), Indicate(chrom.middle, color=GREEN),
                  bars.expected.animate.scale(1.06), rate_func=there_and_back, run_time=1.4)
        pulse(chrom.crossovers[0], base=5.5, amp=2.0, speed=2.2)
        pulse(chrom.crossovers[1], base=5.5, amp=2.0, speed=2.0)
        self.at("crossover spacing")
        self.play(Indicate(chrom.crossovers, color=RED),
                  bars.observed.animate.scale(1.08), rate_func=there_and_back, run_time=1.4)
        self.finish()


class S15End(EndCard):
    LINE = "Comparing observed and expected doubles reveals crossover spacing."
