"""Why the map outgrows the count.

Colour map carried exactly from chapter 1:
BLUE / YELLOW homologues; GREEN parental; RED recombinant and crossover;
TEAL map distance and computed curves; GOLD the 50% ceiling; GREY structure.
"""
from bp_parts import *  # noqa: F401,F403


DOM, REC = BLUE, YELLOW


def scene_board():
    """Shared dark teaching board: one landscape across the whole chapter."""
    board = RoundedRectangle(corner_radius=0.28, width=12.9, height=6.5, stroke_width=0, stroke_opacity=0,
                             fill_color=GREY, fill_opacity=0.18).move_to([0, 0, 0])
    board.set_z_index(-8)
    traces = VGroup()
    for i, x in enumerate((-5.2, -2.6, 0.0, 2.6, 5.2)):
        trace = Rectangle(width=0.34, height=6.2, stroke_width=0, fill_color=TEAL,
                          fill_opacity=0.16).move_to([x, 0, 0])
        trace.set_z_index(-7)

        def drift(mob, dt, speed=4.0):
            mob.shift(RIGHT * speed * dt)
            if mob.get_x() > 6.55:
                mob.shift(LEFT * 13.1)

        trace.add_updater(drift)
        traces.add(trace)
    return VGroup(board, traces)


def marker_label(letter, point, color=TEXT, direction=UP):
    dot = Dot(point, radius=0.13, color=color)
    lab = T(letter, 30, color, weight=BOLD).next_to(dot, direction, buff=0.16)
    return VGroup(dot, lab)


def chromatid_line(y, cuts, colors, x0=-5.2, x1=5.2, width=32):
    """A thick chromatid assembled from honest coloured blocks."""
    points = [x0, *cuts, x1]
    parts = VGroup()
    for a, b, col in zip(points[:-1], points[1:], colors):
        parts.add(Line([a, y, 0], [b, y, 0], color=col, stroke_width=width))
    return parts


def parental_pair(y_top=1.25, y_bottom=-0.25, x0=-5.2, x1=5.2, labels=True):
    top = chromatid_line(y_top, [], [DOM], x0, x1)
    bottom = chromatid_line(y_bottom, [], [REC], x0, x1)
    g = VGroup(top, bottom)
    if labels:
        g.add(marker_label("A", [x0 + 0.55, y_top, 0], TEXT), marker_label("B", [x1 - 0.55, y_top, 0], TEXT),
              marker_label("a", [x0 + 0.55, y_bottom, 0], TEXT, DOWN), marker_label("b", [x1 - 0.55, y_bottom, 0], TEXT, DOWN))
    g.top, g.bottom = top, bottom
    return g


def recombinant_pair(second_site=False, question=False):
    """The carried crossover picture used unchanged by scenes 3--6."""
    y1, y2, x0, x1 = 1.2, -0.35, -5.2, 5.2
    if second_site:
        top = chromatid_line(y1, [-0.8, 2.1], [DOM, REC, DOM], x0, x1)
        bot = chromatid_line(y2, [-0.8, 2.1], [REC, DOM, REC], x0, x1)
    else:
        top = chromatid_line(y1, [-0.8], [DOM, REC], x0, x1)
        bot = chromatid_line(y2, [-0.8], [REC, DOM], x0, x1)
    left_top = marker_label("A", [x0 + 0.55, y1, 0], TEXT)
    right_top = marker_label("b", [x1 - 0.55, y1, 0], TEXT)
    left_bot = marker_label("a", [x0 + 0.55, y2, 0], TEXT, DOWN)
    right_bot = marker_label("B", [x1 - 0.55, y2, 0], TEXT, DOWN)
    g = VGroup(top, bot, left_top, right_top, left_bot, right_bot)
    if question:
        q1 = T("?", 40, GOLD, weight=BOLD).next_to(right_top[0], DOWN, buff=0.16)
        q2 = T("?", 40, GOLD, weight=BOLD).next_to(right_bot[0], UP, buff=0.16)
        g.add(q1, q2)
    g.top, g.bottom = top, bot
    return g


def state_badge(text, color):
    return chip(text, color, 34).move_to([0, -2.45, 0])


def crossover_spark(point, color=RED, radius=0.28):
    rays = VGroup(*[Line(point + radius * 0.35 * np.array([np.cos(a), np.sin(a), 0]),
                              point + radius * np.array([np.cos(a), np.sin(a), 0]),
                              color=color, stroke_width=5) for a in np.linspace(0, TAU, 8, endpoint=False)])
    return rays


def haldane_percent(cm):
    return 50.0 * (1.0 - np.exp(-2.0 * cm / 100.0))


def curve_world():
    plot = Plot(box=(-5.6, 5.7, -2.35, 2.45), xr=(0, 150), yr=(0, 55),
                xticks=[0, 50, 100, 150], yticks=[(0, "0"), (25, "25"), (50, "50")],
                xlabel="map distance (cM)", ylabel="recombination frequency (%)", label_size=28)
    ceiling = plot.hline(50, "50% ceiling", GOLD, size=28)
    return plot, ceiling


def interval_map(show_rf=False):
    """The same three-marker map, rebuilt at one scale and position."""
    y, x0, xm, x1 = 0.7, -5.2, -0.7, 5.2
    bar = Line([x0, y, 0], [x1, y, 0], color=DOM, stroke_width=20)
    marks = VGroup(marker_label("A", [x0 + 0.25, y, 0], TEXT),
                   marker_label("C", [xm, y, 0], TEAL),
                   marker_label("B", [x1 - 0.25, y, 0], TEXT))
    b1 = VGroup(Line([x0 + 0.25, -0.1, 0], [xm, -0.1, 0], color=TEAL, stroke_width=4),
                Line([x0 + 0.25, -0.25, 0], [x0 + 0.25, 0.05, 0], color=TEAL, stroke_width=4),
                Line([xm, -0.25, 0], [xm, 0.05, 0], color=TEAL, stroke_width=4),
                T("short interval", 28, TEAL).move_to([(x0 + xm) / 2, -0.55, 0]))
    b2 = VGroup(Line([xm, -0.1, 0], [x1 - 0.25, -0.1, 0], color=TEAL, stroke_width=4),
                Line([xm, -0.25, 0], [xm, 0.05, 0], color=TEAL, stroke_width=4),
                Line([x1 - 0.25, -0.25, 0], [x1 - 0.25, 0.05, 0], color=TEAL, stroke_width=4),
                T("short interval", 28, TEAL).move_to([(xm + x1) / 2, -0.55, 0]))
    g = VGroup(bar, marks, b1, b2)
    if show_rf:
        left_dial = dial(ValueTracker(0.18), [-2.8, -1.9, 0], radius=0.75, label="raw RF", color=RED, size=28)
        right_dial = dial(ValueTracker(0.22), [2.8, -1.9, 0], radius=0.75, label="raw RF", color=RED, size=28)
        bad = VGroup(left_dial,
                     Dot([0, -1.9, 0], radius=0.01, color=GREY).set_opacity(0),
                     right_dial)
        cross = VGroup(Cross(Square(0.8).move_to([0, -1.9, 0]), stroke_color=RED, stroke_width=8))
        g.add(bad, cross)
    return g


class S01Hook(SpokenScene):
    def construct(self):
        self.add(scene_board())
        short = parental_pair(x0=-2.8, x1=2.8)
        ruler = VGroup(Line([-2.8, -1.45, 0], [2.8, -1.45, 0], color=TEAL, stroke_width=8),
                       T("short chromosome ruler", 30, TEAL).move_to([0, -1.95, 0]))
        self.play(FadeIn(short), GrowFromCenter(ruler), run_time=1.2)
        self.at("Why does that ruler fail")
        why = T("Why does the count fall behind?", 38, GOLD, weight=BOLD).move_to([0, 3.15, 0])
        self.play(FadeIn(why, shift=DOWN * 0.15), run_time=0.8)
        self.at("Reuse the blue and gold")
        long_pair = parental_pair()
        self.play(Transform(short, long_pair), run_time=1.3)
        self.at("Move their outside markers apart")
        long_rule = VGroup(Line([-5.2, -1.45, 0], [5.2, -1.45, 0], color=TEAL, stroke_width=8),
                           T("map distance keeps growing", 30, TEAL).move_to([0, -1.95, 0]))
        self.play(Transform(ruler, long_rule), run_time=1.3)
        self.at("let more crossover sparks")
        sparks = VGroup(*[crossover_spark([x, 0.45, 0], radius=0.23) for x in (-3.2, -1.5, 0.2, 1.9, 3.5)])
        self.play(LaggedStart(*[FadeIn(s, scale=0.3) for s in sparks], lag_ratio=0.18), run_time=2.0)
        self.at("The map keeps growing")
        rf = ValueTracker(0.18)
        gauge = dial(rf, [3.8, -2.05, 0], radius=0.72, label="observed RF", color=RED, size=28)
        tag = scope_tag("schematic")
        self.play(FadeOut(why), FadeIn(gauge), FadeIn(tag), rf.animate.set_value(0.47), run_time=3.2, rate_func=smooth)
        self.finish()


class S02Title(NarratedScene):
    def construct(self):
        self.add(scene_board())
        world = parental_pair()
        sparks = VGroup(*[crossover_spark([x, 0.45, 0], radius=0.18).set_opacity(0.45) for x in (-3, -1, 1, 3)])
        title = fit_text("Why the Map Outgrows the Count", max_w=11.2, size=52, font=TITLE_FONT).move_to([0, 2.8, 0])
        rule = Line([-2.0, 2.25, 0], [2.0, 2.25, 0], color=GOLD, stroke_width=4)
        self.add(world, sparks)
        self.play(Write(title), GrowFromCenter(rule), run_time=0.9)
        self.play(LaggedStart(*[Rotate(s, PI / 3) for s in sparks], lag_ratio=0.1), run_time=0.8)
        self.finish()


class S03FinalState(SpokenScene):
    def construct(self):
        self.add(scene_board())
        parental = parental_pair()
        pulse(parental.top, base=32, amp=12, speed=2.4)
        pulse(parental.bottom, base=32, amp=12, speed=2.1)
        badge = state_badge("parental", GREEN)
        self.play(FadeIn(parental), FadeIn(badge), run_time=2.8)
        self.at("It reads only the final combination")
        outside = VGroup(parental[2], parental[3], parental[4], parental[5])
        self.play(Indicate(outside, color=GOLD, scale_factor=1.08), run_time=1.3)
        self.at("One exchange between them")
        spark = crossover_spark([-0.8, 0.43, 0], radius=0.34)
        self.play(FadeIn(spark, scale=0.2), Rotate(spark, PI / 2), run_time=0.8)
        mixed = recombinant_pair()
        self.play(Transform(parental, mixed), run_time=1.5)
        self.at("into a recombinant one")
        new_badge = state_badge("recombinant", RED)
        self.play(swap(badge, new_badge), run_time=0.8)
        self.at("Another exchange can flip")
        second = crossover_spark([2.1, 0.43, 0], radius=0.3)
        pulse(second)
        self.play(FadeIn(second, scale=0.2), run_time=0.8)
        self.at("The gamete remembers its ending")
        end_glow = SurroundingRectangle(VGroup(mixed[2], mixed[3], mixed[4], mixed[5]), color=GOLD, buff=0.2, corner_radius=0.15)
        self.play(Create(end_glow), run_time=1.0)
        self.at("not the number of turns")
        self.play(Indicate(new_badge, color=RED, scale_factor=1.08), Rotate(second, PI), run_time=1.2)
        self.finish()


class S04Predict(SpokenScene):
    QUESTION = "After another crossover, what will the outside markers show?"

    def construct(self):
        self.add(scene_board())
        mixed = recombinant_pair(question=True)
        pulse(mixed.top, base=32, amp=12, speed=2.4)
        pulse(mixed.bottom, base=32, amp=12, speed=2.1)
        badge = state_badge("recombinant", RED)
        self.add(mixed, badge)
        self.play(badge.animate.shift(RIGHT * 0.45),
                  Indicate(VGroup(mixed[2], mixed[3], mixed[4], mixed[5]), color=GOLD, scale_factor=1.08),
                  run_time=3.2, rate_func=there_and_back)
        self.at("What will those markers show")
        site = crossover_spark([2.1, 0.43, 0], radius=0.34)
        pulse(site)
        self.play(FadeIn(site, scale=0.3), run_time=1.0)
        self.at("after another crossover lands")
        self.play(Rotate(site, PI), run_time=1.4)
        self.at("Follow only their colors")
        self.play(Indicate(VGroup(mixed[2], mixed[3], mixed[4], mixed[5]), color=TEXT, scale_factor=1.1), run_time=1.2)
        self.at("not the cross segments")
        q = question_card(self.QUESTION, y=-3.15, max_w=11.3, size=30)
        self.play(FadeIn(q.question, shift=UP * 0.1), run_time=0.8)
        self.finish()


class S05Pause(Scene):
    def construct(self):
        self.camera.background_color = BG
        self.add(scene_board())
        mixed = recombinant_pair(question=True)
        badge = state_badge("recombinant", RED)
        q = question_card(S04Predict.QUESTION, y=-3.15, max_w=11.3, size=30)
        path = Line([-4.65, 1.65, 0], [4.65, 1.65, 0])
        glow = Dot(path.get_start(), radius=0.12, color=GOLD)
        self.add(mixed, badge, q, glow)
        self.play(MoveAlongPath(glow, path), run_time=4.2, rate_func=linear)
        self.wait(0.3)


class S06Restore(SpokenScene):
    def construct(self):
        self.add(scene_board())
        mixed = recombinant_pair()
        badge = state_badge("recombinant", RED)
        site = crossover_spark([2.1, 0.43, 0], radius=0.34)
        self.add(mixed, badge, site)
        self.play(Rotate(site, PI / 2), run_time=0.7)
        restored = recombinant_pair(second_site=True)
        self.play(Transform(mixed, restored), run_time=1.2)
        self.at("restore the parental outside combination")
        par_badge = state_badge("parental", GREEN)
        self.play(swap(badge, par_badge), run_time=0.8)
        self.at("The middle still records")
        middle = SurroundingRectangle(VGroup(restored.top[1], restored.bottom[1]), color=RED, buff=0.18, corner_radius=0.12)
        self.play(Create(middle), run_time=1.0)
        self.at("a two point score misses it")
        self.play(FadeOut(middle), Indicate(par_badge, color=GREEN, scale_factor=1.08), run_time=1.0)
        self.at("Even numbers of effective flips")
        self.play(FadeOut(VGroup(mixed, site, par_badge)), run_time=0.6)
        panels = TwoPanel("even flips → parental", "odd flips → recombinant", colors=(GREEN, RED), bottom=-2.4)
        even = VGroup(*[crossover_spark([-0.7 + i * 1.4, 0, 0], radius=0.28) for i in range(2)])
        odd = VGroup(*[crossover_spark([-1.4 + i * 1.4, 0, 0], radius=0.28) for i in range(3)])
        panels.put(even, "left"), panels.put(odd, "right")
        self.play(FadeIn(panels), LaggedStart(*[FadeIn(s, scale=0.2) for s in even], lag_ratio=0.2), run_time=1.1)
        self.at("Odd numbers look recombinant")
        self.play(LaggedStart(*[FadeIn(s, scale=0.2) for s in odd], lag_ratio=0.18), run_time=1.2)
        self.at("Long intervals contain more hidden histories")
        cap = caption("Different histories can end with the same visible state.", color=GOLD)
        self.play(FadeIn(cap), Rotate(even, PI / 4), Rotate(odd, -PI / 4), run_time=2.0)
        self.finish()


class S07Ceiling(SpokenScene):
    def construct(self):
        self.add(scene_board())
        base, xs = -1.85, (-4.4, -1.7)
        labels = VGroup(T("parental", 30, GREEN).move_to([xs[0], -2.35, 0]),
                        T("recombinant", 30, RED).move_to([xs[1], -2.35, 0]))
        outlines = VGroup(*[Rectangle(width=1.7, height=3.6, color=GREY, stroke_width=3).move_to([x, -0.05, 0]) for x in xs])
        h = ValueTracker(0.15)
        bars = VGroup(*[always_redraw(lambda x=x, col=col: Rectangle(width=1.35, height=3.2 * h.get_value(), stroke_width=0,
                                                                      fill_color=col, fill_opacity=0.9).move_to([x, base + 1.6 * h.get_value(), 0]))
                         for x, col in zip(xs, (GREEN, RED))])
        self.add(outlines, labels, bars, scope_tag("schematic"))
        histories = VGroup(*[crossover_spark([0.4 + (i % 4) * 0.48, 2.0 - (i // 4) * 0.48, 0], radius=0.14) for i in range(16)])
        self.play(LaggedStart(*[FadeIn(s, scale=0.2) for s in histories], lag_ratio=0.05), h.animate.set_value(0.95), run_time=3.8)
        self.at("Recombination frequency therefore")
        ceiling = T("50% ceiling", 38, GOLD, weight=BOLD).move_to([-3.05, 2.55, 0])
        self.play(FadeIn(ceiling), run_time=0.8)
        self.at("So distant linked loci")
        linked = VGroup(T("distant linked", 28, TEAL), Line([0, 0, 0], [3.2, 0, 0], color=DOM, stroke_width=16),
                        Dot([-1.35, 0, 0], color=TEXT), Dot([1.35, 0, 0], color=TEXT)).arrange(DOWN, buff=0.25).move_to([3.8, 1.0, 0])
        self.play(FadeOut(histories), FadeIn(linked), run_time=1.2)
        self.at("like loci on different chromosomes")
        unlinked = VGroup(T("different chromosomes", 28, GREY),
                          Line([-1.5, 0, 0], [-0.2, 0, 0], color=DOM, stroke_width=16),
                          Line([0.2, 0, 0], [1.5, 0, 0], color=REC, stroke_width=16)).arrange(DOWN, buff=0.25).move_to([3.8, -1.15, 0])
        self.play(FadeIn(unlinked), run_time=1.0)
        self.at("cannot distinguish those cases")
        same = T("same two-point display", 30, GOLD).move_to([3.8, -2.6, 0])
        self.play(FadeIn(same), Indicate(VGroup(linked, unlinked), color=GOLD, scale_factor=1.04), run_time=1.3)
        self.finish()


class S08Curve(SpokenScene):
    def construct(self):
        self.add(scene_board())
        plot, ceiling = curve_world()
        self.play(Create(plot), run_time=1.4)
        self.at("Use Haldane's no interference equation")
        equation = M("RF = (1 − exp(−2d)) / 2", 30, TEAL).move_to([2.6, 3.25, 0])
        tag = scope_tag("no interference")
        self.play(FadeIn(equation), FadeIn(tag), run_time=0.8)
        self.at("not a sketch")
        self.play(FadeIn(ceiling), run_time=0.7)
        d = ValueTracker(0.1)
        area = always_redraw(lambda: Polygon(plot.pt(0, 0),
                                             *[plot.pt(x, haldane_percent(x)) for x in np.linspace(0, max(d.get_value(), 0.1), 60)],
                                             plot.pt(max(d.get_value(), 0.1), 0),
                                             fill_color=TEAL, fill_opacity=0.18, stroke_width=0))
        live = plot.live_curve(haldane_percent, d, color=TEAL, width=7)
        dot = plot.dot(lambda: d.get_value(), lambda: haldane_percent(d.get_value()), color=TEXT, ring=TEAL)
        tracer = always_redraw(lambda: Line(plot.pt(d.get_value(), 0), plot.pt(d.get_value(), haldane_percent(d.get_value())),
                                            color=TEXT, stroke_width=7).set_opacity(0.7))
        self.add(area, live, tracer, dot)
        self.at("The computed curve starts")
        self.play(d.animate.set_value(35), run_time=3.0, rate_func=linear)
        self.at("then bends toward the ceiling")
        self.play(d.animate.set_value(90), run_time=3.0, rate_func=linear)
        self.at("Distance continues across the axis")
        self.play(d.animate.set_value(150), run_time=3.8, rate_func=linear)
        self.finish()


class S09ShortIntervals(SpokenScene):
    def construct(self):
        self.add(scene_board())
        pair = parental_pair()
        self.add(pair)
        self.at("A third marker")
        middle = VGroup(Dot([-0.7, 1.25, 0], radius=0.15, color=TEAL), T("C", 30, TEAL, weight=BOLD).next_to([-0.7, 1.25, 0], UP, buff=0.2),
                        Dot([-0.7, -0.25, 0], radius=0.15, color=TEAL), T("c", 30, TEAL, weight=BOLD).next_to([-0.7, -0.25, 0], DOWN, buff=0.2))
        self.play(FadeIn(middle, scale=0.5), run_time=0.9)
        self.at("breaks a long span into shorter intervals")
        mapped = interval_map()
        self.play(FadeOut(pair), FadeOut(middle), FadeIn(mapped), run_time=1.3)
        self.at("Count each short interval")
        self.play(Indicate(mapped[2], color=TEAL, scale_factor=1.04), Indicate(mapped[3], color=TEAL, scale_factor=1.04), run_time=1.4)
        self.at("Place those distances end to end")
        seg1 = Line([-4.8, -1.75, 0], [-0.7, -1.75, 0], color=TEAL, stroke_width=16)
        seg2 = Line([-0.7, -1.75, 0], [4.8, -1.75, 0], color=TEAL, stroke_width=16)
        self.play(TransformFromCopy(mapped[2][0], seg1), TransformFromCopy(mapped[3][0], seg2), run_time=1.5)
        self.at("Their map distances add")
        add = T("map distances add", 34, TEAL, weight=BOLD).move_to([0, -2.45, 0])
        self.play(FadeIn(add), run_time=0.8)
        self.at("Their raw recombination frequencies do not")
        self.play(FadeOut(VGroup(seg1, seg2, add)), run_time=0.5)
        bad = interval_map(show_rf=True)
        self.play(FadeOut(mapped), FadeIn(bad), run_time=1.3)
        self.at("whole span count can erase double crossovers")
        self.play(Indicate(bad[-1], color=RED, scale_factor=1.05), run_time=1.4)
        self.finish()


class S10Model(SpokenScene):
    def construct(self):
        self.add(scene_board())
        plot, ceiling = curve_world()
        haldane = plot.curve(haldane_percent, color=TEAL, width=7)
        label = chip("independent crossovers", TEAL, 26).move_to([-3.0, 1.3, 0])
        model_tag = scope_tag("computed Haldane model")
        self.add(plot, ceiling, haldane, label, model_tag)
        self.play(Indicate(label, color=TEAL, scale_factor=1.04), run_time=1.0)
        self.at("not a universal correction")
        model = T("model ≠ universal rule", 34, GOLD, weight=BOLD).move_to([2.2, 3.25, 0])
        self.play(FadeIn(model), run_time=0.8)
        self.at("assumes independent crossover placement")
        self.play(Indicate(haldane, color=TEAL, scale_factor=1.02), run_time=1.3)
        self.at("Interference changes how often")
        alt_fn = lambda cm: 50.0 * (1.0 - np.exp(-1.35 * cm / 100.0))
        alt = DashedVMobject(plot.curve(alt_fn, color=GOLD, width=5), num_dashes=28)
        alt_label = chip("schematic interference model", GOLD, 24).move_to([2.9, -0.7, 0])
        self.play(Create(alt), FadeIn(alt_label), run_time=1.7)
        self.at("another function may fit better")
        self.play(Indicate(alt, color=GOLD, scale_factor=1.02), run_time=1.1)
        self.at("The durable practice")
        tiled = interval_map().scale(0.95)
        self.play(FadeOut(VGroup(plot, ceiling, haldane, label, model, alt, alt_label, model_tag)), FadeIn(tiled), run_time=1.3)
        self.at("map short intervals")
        self.play(Indicate(tiled[2], color=TEAL, scale_factor=1.04), run_time=0.9)
        self.at("add their distances")
        self.play(Indicate(tiled[3], color=TEAL, scale_factor=1.04), run_time=0.9)
        self.at("state the model")
        cap = caption("Map short intervals; state the correction model.", color=GOLD)
        self.play(FadeIn(cap), run_time=0.9)
        self.finish()


class S11Close(SpokenScene):
    def construct(self):
        self.add(scene_board())
        xs, base = (-4.8, -2.5), -1.35
        bins = VGroup(*[Rectangle(width=1.5, height=3.0, color=col, fill_color=col, fill_opacity=0.65).move_to([x, 0.15, 0])
                        for x, col in zip(xs, (GREEN, RED))],
                      T("final states", 30, TEXT).move_to([-3.65, -1.8, 0]),
                      T("≈ 50 : 50", 34, GOLD, weight=BOLD).move_to([-3.65, 2.05, 0]))
        self.play(FadeIn(bins), run_time=1.0)
        self.at("The map represents")
        start, stop = 0.2, 5.6
        map_line = Line([start, 0.4, 0], [2.0, 0.4, 0], color=TEAL, stroke_width=36)
        map_label = T("expected crossovers per chromatid", 28, TEAL).move_to([3.0, -0.65, 0])
        self.play(GrowFromEdge(map_line, LEFT), FadeIn(map_label), run_time=3.0)
        self.at("Those quantities track closely")
        near = VGroup(Line([0.5, 1.4, 0], [2.0, 1.4, 0], color=RED, stroke_width=7),
                      Line([0.5, 1.15, 0], [2.0, 1.15, 0], color=TEAL, stroke_width=7))
        self.play(Create(near), run_time=1.0)
        self.at("while hidden exchanges are rare")
        spark1 = crossover_spark([2.45, 0.4, 0], radius=0.3)
        self.play(FadeIn(spark1, scale=0.2), run_time=0.8)
        self.at("As the interval grows")
        self.play(FadeOut(near), map_line.animate.put_start_and_end_on([start, 0.4, 0], [stop, 0.4, 0]), run_time=1.8)
        self.at("the map can keep lengthening")
        spark2 = crossover_spark([4.3, 0.4, 0], radius=0.3)
        self.play(FadeIn(spark2, scale=0.2), map_line.animate.put_start_and_end_on([start, 0.4, 0], [6.0, 0.4, 0]), run_time=1.8)
        self.at("count has nearly stopped changing")
        self.play(FadeOut(bins, shift=DOWN * 0.2), Rotate(spark1, PI / 3), Rotate(spark2, PI / 3), run_time=1.5)
        self.finish()


class S12End(EndCard):
    LINE = "Over long intervals, hidden crossovers make\nrecombination frequency underestimate distance."
