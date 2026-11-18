from bp_parts import *


# COLOR MAP — shared with chapter 1 and fixed for the whole film:
# input GOLD; active relay/output BLUE; error accumulator TEAL;
# open channels GREEN; shutoff/inhibitory feedback RED.


def _arrow_between(a, b, color=BLUE, buff=0.12, width=5):
    return Arrow(a, b, buff=buff, color=color, stroke_width=width,
                 max_tip_length_to_length_ratio=0.16)


def pathway_world(feedback=None, scale=1.0, center=ORIGIN, labels=True):
    """The carried circuit. Every scene calls this builder, so geometry never drifts."""
    blocks = VGroup(
        boxed_label("input", GOLD, size=28, box=(1.65, 0.72)),
        boxed_label("relay", BLUE, size=28, box=(1.65, 0.72)),
        boxed_label("output", BLUE, size=28, box=(1.85, 0.72)),
    ).arrange(RIGHT, buff=1.05)
    links = VGroup(
        _arrow_between(blocks[0].get_right(), blocks[1].get_left(), GOLD),
        _arrow_between(blocks[1].get_right(), blocks[2].get_left(), BLUE),
    )
    g = VGroup(links, blocks)
    g.blocks, g.links = blocks, links
    if feedback:
        col = RED if feedback == "negative" else BLUE if feedback == "positive" else TEAL
        end = blocks[1].get_top() + UP * 0.68
        ret = CurvedArrow(blocks[2].get_top() + UP * 0.68, end,
                          angle=TAU / 4, color=col, stroke_width=5)
        if feedback == "negative":
            # A visible inhibitory bar, placed clear of the relay label.
            ret[-1].set_opacity(0)
            bar = Line(end + LEFT * 0.18, end + RIGHT * 0.18, color=RED, stroke_width=7)
            ret = VGroup(ret, bar)
        g.add(ret)
        g.feedback = ret
    g.scale(scale).move_to(center)
    return g


def gauge(center=(4.8, 0.0, 0), value=0.45, color=BLUE, label="output"):
    """Large output vessel; fill height is controlled by `.level`."""
    c = np.array(center, dtype=float)
    box = RoundedRectangle(width=1.45, height=3.6, corner_radius=0.18,
                           stroke_color=GREY, stroke_width=4).move_to(c)
    level = ValueTracker(value)
    fill = always_redraw(lambda: Rectangle(
        width=1.25, height=max(0.04, 3.32 * level.get_value()),
        stroke_width=0, fill_color=color, fill_opacity=0.72
    ).move_to([c[0], c[1] - 1.66 + 1.66 * level.get_value(), 0]))
    lab = T(label, 28, color).next_to(box, DOWN, buff=0.2)
    g = VGroup(fill, box, lab)
    g.level, g.box, g.fill = level, box, fill
    return g


def circuit_stage(feedback=None, level=0.45):
    world = pathway_world(feedback=feedback, scale=1.08, center=LEFT * 1.25)
    meter = gauge((4.9, -0.15, 0), value=level)
    stream = VGroup(*[Dot(radius=0.09, color=GOLD) for _ in range(5)])
    for i, d in enumerate(stream):
        d.move_to([-6.2 + 0.32 * i, -0.15, 0])
    tag = scope_tag("schematic")
    return VGroup(world, meter, stream, tag), world, meter, stream


def animate_stream(stream):
    starts = [d.get_center().copy() for d in stream]
    for i, d in enumerate(stream):
        d._phase = i / max(1, len(stream))

        def drift(m, dt, x0=starts[i][0]):
            m.shift(RIGHT * 0.42 * dt)
            if m.get_x() > -4.55:
                m.set_x(x0)
        d.add_updater(drift)
    return stream


def trace_plot(box=(-5.9, 5.9, -2.0, 2.25), ylabel="output"):
    return Plot(box=box, xr=(0, 10), yr=(0, 1.15), xticks=[0, 5, 10],
                yticks=[(0, "rest"), (1, "high")], xlabel="time", ylabel=ylabel)


def pulse_fn(t, delay=3.0):
    rise = 1 - np.exp(-1.5 * t)
    brake = 1 / (1 + np.exp(-2.2 * (t - delay)))
    return 0.12 + 0.86 * rise * (1 - 0.82 * brake)


def adapt_fn(t):
    return 0.2 + 0.8 * t * np.exp(-0.72 * t)


def high_fn(t):
    return 0.18 + 0.78 * (1 - np.exp(-0.85 * t))


def undershoot_fn(t):
    return max(0.02, 0.18 + 0.72 * t * np.exp(-0.7 * t) - 0.17 / (1 + np.exp(-(t - 6))))


def three_trace_backdrop(highlight=None, question=True):
    heading = T("continuing input", 30, GOLD).move_to([-4.9, 3.2, 0])
    input_line = Line([-3.25, 3.2, 0], [5.7, 3.2, 0], color=GOLD, stroke_width=7)
    plots = VGroup()
    funcs = (high_fn, undershoot_fn, adapt_fn)
    for i, fn in enumerate(funcs):
        x0, x1 = -6.05 + 4.2 * i, -2.55 + 4.2 * i
        p = Plot(box=(x0, x1, -1.85, 1.45), xr=(0, 10), yr=(0, 1.15),
                 xticks=(), yticks=(), xlabel="", ylabel="")
        curve = p.curve(fn, color=BLUE, width=7)
        base = p.hline(0.18, color=GREY)
        tag = T("schematic", 24, GREY).next_to(p.axes, DOWN, buff=0.18)
        group = VGroup(p, base, curve, tag)
        if highlight is not None and i != highlight:
            # Dim strokes and text without raising a curve's fill opacity (which creates a wedge).
            p.axes.set_stroke(opacity=0.25)
            p.ticks.set_stroke(opacity=0.25)
            p.tick_labels.set_opacity(0.25)
            base.set_stroke(opacity=0.25)
            curve.set_stroke(opacity=0.25)
            tag.set_opacity(0.25)
        plots.add(group)
    q = question_card("Which trace is adaptation?", y=-3.18, max_w=9.6)
    out = VGroup(heading, input_line, plots)
    if question:
        out.add(q)
    out.plots, out.question = plots, q
    return out


def landscape(two=True, box=(-0.7, 5.9, -1.45, 1.45)):
    """Schematic state landscape computed from smooth basin functions."""
    axes = Plot(box=box, xr=(0, 10), yr=(0, 1.2),
                xticks=(), yticks=(), xlabel="", ylabel="")
    if two:
        fn = lambda x: 0.18 + 0.018 * (x - 2.0) ** 2 * (x - 8.0) ** 2
    else:
        fn = lambda x: 0.16 + 0.025 * (x - 5.0) ** 2
    curve = axes.curve(fn, color=BLUE, width=7)
    state_lab = T("output state", 26, GREY).next_to(axes.axes, UP, buff=0.16)
    g = VGroup(axes, curve, state_lab, T("schematic", 24, GREY).next_to(axes.axes, DOWN, buff=0.22))
    if two:
        low = T("low state", 28, BLUE).move_to(axes.pt(2, 0) + DOWN * 0.55)
        high = T("high state", 28, BLUE).move_to(axes.pt(8, 0) + DOWN * 0.55)
        g.add(low, high)
    return g


def chemotaxis_world(level=0.75):
    blocks = VGroup(*[boxed_label(x, BLUE if x != "receptor" else GOLD, size=28,
                                  box=(1.75, 0.72)) for x in ("receptor", "CheA", "CheY")])
    blocks.arrange(RIGHT, buff=0.8).move_to([-1.35, 0.45, 0])
    arrows = VGroup(_arrow_between(blocks[0].get_right(), blocks[1].get_left(), GOLD),
                    _arrow_between(blocks[1].get_right(), blocks[2].get_left(), BLUE))
    meter = gauge((4.9, 0.35, 0), level, BLUE)
    ref = DashedLine([4.15, 0.35, 0], [5.65, 0.35, 0], color=TEAL, stroke_width=4)
    ref_lab = T("reference", 24, TEAL).next_to(ref, LEFT, buff=0.16)
    g = VGroup(arrows, blocks, meter, ref, ref_lab, scope_tag("idealized model"))
    g.blocks, g.meter, g.reference = blocks, meter, ref
    return g


def tracer(curve, period=4.0, phase=0.0, color=GOLD, radius=0.09):
    """A small dot that keeps travelling along a curve (continuous motion during holds)."""
    d = Dot(radius=radius, color=color)
    d._tr_t = phase * period
    d.move_to(curve.point_from_proportion(phase % 1.0))

    def u(m, dt):
        m._tr_t += dt
        m.move_to(curve.point_from_proportion((m._tr_t / period) % 1.0))
    d.add_updater(u)
    return d


def sweep(x0, x1, y0, y1, period=2.4, width=0.7, color=TEAL, opacity=0.42):
    """A soft time-cursor band that keeps sweeping across a region (ambient motion for holds)."""
    band = Rectangle(width=width, height=y1 - y0, stroke_width=0, fill_color=color, fill_opacity=opacity)
    band._sw_t = 0.0
    band.z_index = -2

    def u(m, dt):
        m._sw_t += dt
        a = (m._sw_t / period) % 1.0
        m.move_to([x0 + (x1 - x0) * a, (y0 + y1) / 2, 0])
    u(band, 0)
    band.add_updater(u)
    return band


class S00LinkQuestion(SpokenScene):
    def construct(self):
        stage, world, meter, stream = circuit_stage(level=0.2)
        animate_stream(stream)
        self.play(FadeIn(stage), run_time=0.8)
        self.at("cascade multiplying")
        self.play(LaggedStart(*[Indicate(b, color=BLUE) for b in world.blocks], lag_ratio=0.18), run_time=1.5)
        self.at("What can make")
        faint = VGroup(CurvedArrow(meter.box.get_top() + UP * 0.18,
                                  world.blocks[1].get_top() + UP * 0.42, angle=TAU/4,
                                  color=GREY, stroke_opacity=0.35),
                       VMobject(color=GREY, stroke_opacity=0.35, stroke_width=4).set_points_as_corners([
                           meter.box.get_left() + DOWN * 1.25,
                           np.array([3.4, -2.72, 0]), np.array([-1.4, -2.72, 0]),
                           world.blocks[1].get_bottom() + DOWN * 0.42]))
        self.play(Create(faint), meter.level.animate.set_value(0.92), run_time=1.5)
        self.play(meter.level.animate.set_value(0.28), run_time=1.4)
        self.at("One answer lies")
        self.play(faint.animate.set_stroke(color=TEAL, opacity=0.9), run_time=1.0)
        pulse(world.blocks[2].box, base=2.5, amp=1.4, speed=2.2)
        self.finish()


class S01Title(TitleCard):
    LESSON = "Signaling circuits"
    TITLE = "Three Ways a Signal Changes with Time"


class S02FeedbackSign(SpokenScene):
    def construct(self):
        stage, world, meter, stream = circuit_stage(level=0.62)
        animate_stream(stream)
        self.add(stage)
        self.at("output acts back")
        neg = pathway_world("negative", 1.08, LEFT * 1.25).feedback
        neg_lab = T("negative", 30, RED).next_to(neg, UP, buff=0.12)
        self.play(Create(neg), run_time=1.3)
        self.at("opposes the change")
        self.play(FadeIn(neg_lab), meter.level.animate.set_value(0.28), run_time=1.3)
        self.at("reinforces the change")
        pos = pathway_world("positive", 1.08, LEFT * 1.25).feedback
        pos_lab = T("positive", 30, BLUE).next_to(pos, UP, buff=0.12)
        self.play(FadeOut(neg), swap(neg_lab, pos_lab), FadeIn(pos),
                  meter.level.animate.set_value(0.88), run_time=1.5)
        pulse(pos, base=5, amp=1.4, speed=2.0)
        self.finish()


class S02FeedbackTiming(SpokenScene):
    def construct(self):
        stage, world, meter, stream = circuit_stage("positive", level=0.35)
        animate_stream(stream)
        self.add(stage)
        clock = Circle(radius=0.72, color=GOLD, stroke_width=4).move_to([-4.9, 2.45, 0])
        hand = Line(clock.get_center(), clock.get_center() + UP * 0.5, color=GOLD, stroke_width=5)
        timing = T("timing", 28, GOLD).next_to(clock, DOWN, buff=0.12)
        strength = ValueTracker(0.25)
        slider = NumberLine(x_range=[0, 1, 0.5], length=2.2, include_numbers=False,
                            color=BLUE).move_to([2.0, 2.45, 0])
        knob = always_redraw(lambda: Dot(slider.n2p(strength.get_value()), radius=0.13, color=BLUE))
        slabel = T("strength", 28, BLUE).next_to(slider, DOWN, buff=0.15)
        self.play(FadeIn(clock), GrowFromCenter(hand), FadeIn(timing), run_time=1.0)
        self.at("strength decide")
        self.play(FadeIn(slider), FadeIn(knob), FadeIn(slabel), run_time=0.9)
        self.at("different dynamics")
        self.play(Rotate(hand, angle=1.7, about_point=clock.get_center()),
                  strength.animate.set_value(0.92), meter.level.animate.set_value(0.92), run_time=1.6)
        self.at("Connections alone")
        self.play(Rotate(hand, angle=-2.5, about_point=clock.get_center()),
                  strength.animate.set_value(0.38), meter.level.animate.set_value(0.3), run_time=1.5)
        self.finish()


class S03NegativeRise(SpokenScene):
    def construct(self):
        stage, world, meter, stream = circuit_stage("negative", level=0.12)
        animate_stream(stream)
        self.add(stage)
        input_high = T("input stays on", 30, GOLD).move_to([-4.95, 2.65, 0])
        self.play(FadeIn(input_high), meter.level.animate.set_value(0.94), run_time=1.7)
        self.at("accumulates")
        brakes = VGroup(*[RoundedRectangle(width=0.33, height=0.33, corner_radius=0.05,
                                           color=RED, fill_color=RED, fill_opacity=0.75)
                          for _ in range(5)]).arrange(RIGHT, buff=0.12).move_to([0.15, 2.25, 0])
        self.play(LaggedStart(*[FadeIn(b, shift=DOWN * 0.15) for b in brakes], lag_ratio=0.2), run_time=2.0)
        self.at("negative feedback lowers")
        self.play(brakes.animate.shift(DOWN * 0.75), meter.level.animate.set_value(0.3), run_time=1.8)
        pulse(world.feedback, base=5, amp=1.5, speed=2)
        self.finish()


class S03NegativeTiming(SpokenScene):
    def construct(self):
        p = trace_plot(box=(-5.8, 3.1, -1.8, 2.2))
        delay = ValueTracker(4.0)
        curve = always_redraw(lambda: p.curve(lambda t: pulse_fn(t, delay.get_value()), color=BLUE, width=7))
        inp = p.hline(1.02, "input stays high", GOLD)
        tag = scope_tag("schematic")
        dline = always_redraw(lambda: p.vline(delay.get_value(), "brake delay", RED))
        self.play(Create(p), FadeIn(inp), FadeIn(tag), run_time=0.9)
        self.add(curve, dline)
        self.play(delay.animate.set_value(6.1), run_time=1.5)
        self.at("shape the pulse")
        self.play(delay.animate.set_value(2.2), run_time=1.5)
        self.at("Connections alone")
        self.play(delay.animate.set_value(4.7), run_time=1.2)
        self.finish()


class S04PositiveLoop(SpokenScene):
    def construct(self):
        stage, world, meter, stream = circuit_stage("positive", level=0.18)
        animate_stream(stream)
        self.add(stage)
        self.play(world.feedback.animate.set_color(BLUE), run_time=0.7)
        self.at("reinforces its own")
        for val in (0.36, 0.62, 0.92):
            self.play(Indicate(world.blocks[1], color=BLUE), meter.level.animate.set_value(val), run_time=0.85)
        pulse(world.feedback, base=5, amp=1.8, speed=2.3)
        self.finish()


class S04PositiveStates(SpokenScene):
    def construct(self):
        world = pathway_world("positive", 0.8, LEFT * 3.65 + UP * 0.25)
        land = landscape(True)
        self.add(world, scope_tag("schematic"))
        self.at("steep step")
        self.play(Create(land), run_time=1.2)
        marker = Dot(land[0].pt(2, 0.18), radius=0.15, color=GOLD)
        self.play(FadeIn(marker), run_time=0.5)
        self.at("low or high")
        self.play(marker.animate.move_to(land[0].pt(8, 0.18)), run_time=1.5)
        self.at("weaker loop")
        one = landscape(False)
        self.play(FadeOut(land), FadeOut(marker), Transform(world.feedback, world.feedback.copy().set_opacity(0.35)),
                  FadeIn(one), run_time=1.3)
        self.finish()


class S05Steepness(SpokenScene):
    def construct(self):
        p = Plot(box=(-6.0, -0.3, -2.1, 2.25), xr=(0, 1), yr=(0, 1),
                 xticks=[0, 1], yticks=[0, 1], xlabel="input", ylabel="output")
        hill = lambda x: x ** 6 / (0.5 ** 6 + x ** 6)
        curve = p.curve(hill, color=BLUE, width=7)
        x = ValueTracker(0.05)
        dot = p.dot(lambda: x.get_value(), lambda: hill(x.get_value()), color=GOLD)
        self.play(Create(p), Create(curve), FadeIn(T("schematic", 24, GREY).move_to([-0.9, -2.75, 0])), run_time=1.0)
        self.add(dot)
        self.play(x.animate.set_value(0.95), run_time=1.4)
        self.at("reverse when input falls")
        self.play(x.animate.set_value(0.05), run_time=1.4)
        self.at("positive feedback")
        land = landscape(True, box=(1.15, 6.1, -1.45, 1.45))
        land.remove(land[3])  # the scene already carries a clear schematic tag at lower left
        loop = CurvedArrow([2.2, 2.3, 0], [5.1, 2.3, 0], angle=-PI/2, color=BLUE, stroke_width=5)
        self.play(Create(loop), FadeIn(land), run_time=1.4)
        pulse(loop, base=5, amp=1.4, speed=2)
        self.finish()


class S05Memory(SpokenScene):
    def construct(self):
        land = landscape(True)
        c0 = land.get_center().copy()
        land.move_to(ORIGIN + UP * 0.25)
        shift = land.get_center() - c0
        marker = Dot(land[0].pt(2, 0.18) + shift, radius=0.16, color=GOLD)
        input_bar = Rectangle(width=1.0, height=0.1, color=GOLD, fill_color=GOLD,
                              fill_opacity=0.8).move_to([-5.15, 2.4, 0])
        in_lab = T("temporary input", 28, GOLD).next_to(input_bar, UP, buff=0.15)
        self.add(land, marker, scope_tag("schematic"))
        self.add(sweep(-3.3, 3.3, -1.2, 1.5, period=2.4))
        self.play(GrowFromEdge(input_bar, LEFT), FadeIn(in_lab), run_time=1.0)
        self.at("high state")
        self.play(marker.animate.move_to(land[0].pt(8, 0.18) + shift), run_time=1.5)
        self.at("outlasts the input")
        keep = T("with sufficient feedback", 28, BLUE).move_to([2.9, 2.55, 0])
        self.play(FadeOut(input_bar), FadeOut(in_lab), FadeIn(keep), run_time=1.0)
        bob(marker, amp=0.12, speed=2.2)
        self.finish()


class S06Predict(SpokenScene):
    def construct(self):
        bg = three_trace_backdrop(question=False)
        self.play(FadeIn(bg[0]), GrowFromEdge(bg[1], LEFT), run_time=0.9)
        self.at("Three output traces")
        self.play(LaggedStart(*[Create(p) for p in bg.plots], lag_ratio=0.25), run_time=2.4)
        self.at("Which trace represents")
        self.play(FadeIn(bg.question), run_time=0.8)
        self.at("defining pattern")
        self.play(LaggedStart(*[Indicate(p, color=GOLD) for p in bg.plots], lag_ratio=0.22), run_time=1.7)
        for i, p in enumerate(bg.plots):
            self.add(tracer(p[2], period=3.5, phase=0.0 + 0.0 * i))
        self.add(sweep(-6.05, 5.7, -1.8, 1.4, period=2.6))
        self.finish()


class S07Pause(Scene):
    def construct(self):
        bg = three_trace_backdrop(question=True)
        self.add(bg)
        cursor = Triangle(color=GOLD, fill_color=GOLD, fill_opacity=1).scale(0.13).rotate(-PI/2)
        cursor.move_to([-4.3, 2.05, 0])
        self.add(cursor)
        self.play(cursor.animate.move_to([0.0, 2.05, 0]), run_time=2.2, rate_func=linear)
        self.play(cursor.animate.move_to([4.1, 2.05, 0]), run_time=2.2, rate_func=linear)
        self.wait(0.1)


class S08Adaptation(SpokenScene):
    def construct(self):
        bg = three_trace_backdrop(highlight=2, question=False)
        self.add(bg)
        self.at("choose the trace")
        answer = T("adaptation", 30, TEAL).next_to(bg.plots[2], UP, buff=0.15)
        self.play(FadeIn(answer), Indicate(bg.plots[2], color=TEAL), run_time=1.2)
        self.at("delayed")
        self.play(bg.plots[2].animate.set_color(RED), run_time=0.9)
        self.at("Integral feedback")
        chem = chemotaxis_world(level=0.86)
        self.play(FadeOut(bg), FadeOut(answer), FadeIn(chem), run_time=1.2)
        self.at("gap from a reference")
        gap = DoubleArrow([5.85, 0.35, 0], [5.85, 1.57, 0], buff=0, color=TEAL, stroke_width=4)
        gap_lab = T("gap", 28, TEAL).next_to(gap, RIGHT, buff=0.12)
        self.play(FadeIn(gap), FadeIn(gap_lab), run_time=0.8)
        self.at("gap is zero")
        self.play(chem.meter.level.animate.set_value(0.5), gap.animate.scale(0.08, about_point=[5.85, 0.35, 0]),
                  FadeOut(gap_lab), run_time=1.8)
        pulse(chem.reference, base=4, amp=1.2, speed=2)
        self.finish()


class S09Integral(SpokenScene):
    def construct(self):
        chem = chemotaxis_world(level=0.9)
        pulse(chem.reference, base=4, amp=1.2, speed=1.8)
        self.add(chem)
        total = ValueTracker(0.05)
        ledger_box = RoundedRectangle(width=1.15, height=3.0, corner_radius=0.12,
                                      color=TEAL, stroke_width=3).move_to([-5.4, 0.2, 0])
        ledger_fill = always_redraw(lambda: Rectangle(width=0.94, height=max(0.04, 2.75 * total.get_value()),
            stroke_width=0, fill_color=TEAL, fill_opacity=0.68).move_to([-5.4, -1.175 + 1.375 * total.get_value(), 0]))
        ledger_lab = T("running total", 28, TEAL).next_to(ledger_box, UP, buff=0.15)
        self.play(FadeIn(ledger_box), FadeIn(ledger_fill), FadeIn(ledger_lab), run_time=0.9)
        self.add(sweep(-6.5, 6.5, -3.3, -0.5, period=2.4))
        self.at("Correction continues")
        self.play(total.animate.set_value(0.86), chem.meter.level.animate.set_value(0.5), run_time=2.2)
        self.at("integral feedback")
        name = T("integral feedback", 30, TEAL).move_to([0.0, 2.65, 0])
        self.play(FadeIn(name), run_time=0.8)
        self.at("adds methyl groups")
        tabs = VGroup(boxed_label("CheR adds", TEAL, 26), boxed_label("CheB removes", RED, 26))
        tabs.arrange(DOWN, buff=0.25).move_to([-3.55, -2.15, 0])
        methyl = ValueTracker(0.35)
        dg = dial(methyl, center=[0.25, -1.55, 0], radius=1.0, label="methylation", color=TEAL, size=30)
        self.play(FadeIn(tabs[0]), FadeIn(dg), methyl.animate.set_value(0.72), run_time=1.2)
        self.at("removes them")
        self.play(FadeIn(tabs[1]), methyl.animate.set_value(0.5), run_time=1.2)
        self.finish()


class S10Robustness(SpokenScene):
    def construct(self):
        rows = VGroup()
        colors = (TEAL, TEAL, TEAL)
        for i, (name, y) in enumerate(zip(("low enzyme", "middle enzyme", "high enzyme"), (2.0, 0.0, -2.0))):
            label = T(name, 26, TEXT).move_to([-5.55, y, 0])
            gauge_bg = RoundedRectangle(width=1.0, height=0.45, color=TEAL, corner_radius=0.08).move_to([-3.45, y, 0])
            fill = Rectangle(width=(i + 1) * 0.28, height=0.27, stroke_width=0,
                             fill_color=TEAL, fill_opacity=0.8).align_to(gauge_bg, LEFT).move_to([-3.84 + (i + 1)*0.14, y, 0])
            ref_y = y
            ref = DashedLine([-2.7, ref_y, 0], [4.85, ref_y, 0], color=TEAL, stroke_width=3)
            curve = VMobject(color=BLUE, stroke_width=6)
            xs = np.linspace(-2.6, 4.7, 80)
            tau = (3.2, 2.1, 1.2)[i]
            pts = [[x, y + 0.72 * np.exp(-(x + 2.6)/tau) * np.sin(1.45*(x + 2.6)), 0] for x in xs]
            curve.set_points_as_corners(pts)
            clock = T(("slow", "medium", "fast")[i], 24, GOLD).move_to([6.05, y, 0])
            rows.add(VGroup(label, gauge_bg, fill, ref, curve, clock))
        self.play(LaggedStart(*[FadeIn(r) for r in rows], lag_ratio=0.25), run_time=1.7)
        for i, r in enumerate(rows):
            self.add(tracer(r[4], period=(5.0, 4.0, 3.0)[i], phase=0.0))
        self.add(sweep(-2.6, 4.7, -2.9, 2.9, period=2.2))
        self.at("other steady behavior")
        self.play(rows[0][4].animate.shift(DOWN * 0.18), rows[2][4].animate.shift(UP * 0.18), run_time=1.2)
        self.at("precision can remain")
        bracket = BraceBetweenPoints([4.9, 2.65, 0], [4.9, -2.65, 0], direction=RIGHT, color=TEAL)
        lab = T("precision protected", 28, TEAL).move_to([4.2, 3.2, 0])
        self.play(GrowFromCenter(bracket), FadeIn(lab), run_time=1.0)
        self.at("not every feature")
        self.play(LaggedStart(*[Indicate(r[5], color=GOLD) for r in rows], lag_ratio=0.2), run_time=1.5)
        self.finish()


def mini_circuit(kind, x):
    colors = {"negative": RED, "positive": BLUE, "integral": TEAL}
    title = {"negative": "delayed brake", "positive": "reinforcing loop", "integral": "error correction"}[kind]
    blocks = VGroup(*[RoundedRectangle(width=0.75, height=0.48, corner_radius=0.08,
                                      color=BLUE, fill_color=BLUE, fill_opacity=0.14) for _ in range(3)])
    blocks.arrange(RIGHT, buff=0.35).move_to([x, 0.5, 0])
    arr = VGroup(*[_arrow_between(blocks[i].get_right(), blocks[i+1].get_left(), GOLD if i == 0 else BLUE,
                                  buff=0.04, width=4) for i in range(2)])
    ret = CurvedArrow(blocks[2].get_top(), blocks[1].get_top(), angle=PI/2,
                      color=colors[kind], stroke_width=4)
    ttl = T(title, 28, colors[kind]).move_to([x, 2.55, 0])
    input_lab = T("input", 24, GOLD).move_to([x - 1.45, -0.15, 0])
    if kind == "negative":
        fn = pulse_fn
    elif kind == "positive":
        fn = high_fn
    else:
        fn = adapt_fn
    p = Plot(box=(x-1.45, x+1.45, -2.0, -0.55), xr=(0, 10), yr=(0, 1.15), xticks=(), yticks=())
    curve = p.curve(fn, color=BLUE, width=5)
    g = VGroup(ttl, arr, blocks, ret, input_lab, p, curve)
    g.return_arrow = ret
    return g


class S11Compare(SpokenScene):
    def construct(self):
        circuits = VGroup(mini_circuit("negative", -4.45), mini_circuit("positive", 0), mini_circuit("integral", 4.45))
        self.play(LaggedStart(*[FadeIn(c) for c in circuits], lag_ratio=0.25), run_time=1.6)
        self.at("Delayed negative")
        self.play(Indicate(circuits[0], color=RED), run_time=1.1)
        self.at("Sufficient positive")
        self.play(Indicate(circuits[1], color=BLUE), run_time=1.1)
        self.at("Integral feedback corrects")
        self.play(Indicate(circuits[2], color=TEAL), run_time=1.1)
        self.at("restore a reference")
        for c in circuits:
            pulse(c.return_arrow, base=4, amp=1.2, speed=2)
        self.play(LaggedStart(*[Indicate(c[-1], color=GOLD) for c in circuits], lag_ratio=0.25), run_time=1.7)
        self.finish()


class S12Return(SpokenScene):
    def construct(self):
        stage, world, meter, stream = circuit_stage(level=0.25)
        animate_stream(stream)
        self.add(stage)
        self.at("kinetics finish")
        controls = VGroup(*[boxed_label(x, c, size=26, box=(1.8, 0.62)) for x, c in
                            (("sign", RED), ("strength", BLUE), ("delay", GOLD), ("lifetime", TEAL))])
        controls.arrange(RIGHT, buff=0.28).move_to([0, 2.75, 0])
        self.play(LaggedStart(*[FadeIn(c, shift=DOWN * 0.12) for c in controls], lag_ratio=0.18), run_time=1.7)
        self.at("fades commits")
        self.play(meter.level.animate.set_value(0.88), run_time=1.1)
        self.play(meter.level.animate.set_value(0.28), run_time=1.1)
        self.play(meter.level.animate.set_value(0.55), run_time=1.0)
        self.at("Feedback reshapes")
        loop = CurvedArrow(meter.box.get_top(), world.blocks[1].get_top(), angle=TAU/4,
                           color=TEAL, stroke_width=5)
        self.play(Create(loop), run_time=1.0)
        pulse(loop, base=5, amp=1.5, speed=2)
        self.finish()


class S13End(EndCard):
    LINE = "Feedback can limit duration, sharpen decisions, or restore resting output."
