"""Extirpation and replacement, timed to the supplied narration.

COLOR MAP
    BLUE: nerves and delivery apparatus. GREY: structure and inactive tissue.
    PURPLE: source tissue. CRIMSON: blood vessels. YELLOW: circulating signal.
    ORANGE: replacement input. GREEN: target response. GOLD: dates and prediction.
"""
from bp_parts import *
from bp_style import EndCard

PURPLE = "#B58CD9"
ORANGE = "#F29E4C"
CRIMSON = "#AF465D"
VESSEL_WALL = "#713044"
TISSUE = "#1D202A"
VESSEL_Y = -0.48
SOURCE = np.array([-4.12, 0.20, 0.0])
GRAFT = np.array([-4.12, -1.42, 0.0])
TARGET = np.array([4.05, 0.02, 0.0])
QUESTION = "Which schedule restores pituitary release?"


def pt(x, y):
    return np.array([x, y, 0.0])


def label(text, x, y, color=TEXT, size=30):
    return T(text, size, color, weight=MEDIUM).move_to(pt(x, y))


def tag(text, color=GOLD):
    return boxed_label(text, color, size=30, pad=0.17).move_to(pt(0, 3.27))


def arrow(a, b, color, width=5):
    return Arrow(a, b, buff=0, color=color, stroke_width=width, tip_length=0.20)


def vessel():
    """The same cross-section for every animal. The inset leaves a visibly wide lumen."""
    def shell(width, height, radius, fill, stroke, stroke_width):
        return RoundedRectangle(width=width, height=height, corner_radius=radius,
                                fill_color=fill, fill_opacity=1, stroke_color=stroke,
                                stroke_width=stroke_width).move_to(pt(0, VESSEL_Y))

    outer = shell(11.78, 4.80, 1.36, VESSEL_WALL, CRIMSON, 3)
    inner = shell(10.59, 3.61, 0.82, TISSUE, CRIMSON, 2)
    route = shell(11.18, 4.20, 1.08, TISSUE, CRIMSON, 0)
    # Start at the upper left with left-to-right flow along the upper branch.
    points = np.array([route.point_from_proportion(i / 280) for i in range(281)])
    if points[8, 0] < points[0, 0]:
        points = points[::-1]
    start = np.argmin(np.linalg.norm(points[:-1] - pt(-4.4, 1.61), axis=1))
    points = np.roll(points[:-1], -start, axis=0)
    return VGroup(outer, inner), np.vstack([points, points[0]])


def moving_signal(points, amount, active=True, speed=0.21, color=YELLOW, radius=0.135, count=24):
    """Circulating packets follow the vessel or feed path. The tracker sets visible density."""
    distances = np.insert(np.cumsum(np.linalg.norm(np.diff(points, axis=0), axis=1)), 0, 0)
    length = distances[-1]
    beads = VGroup(*[Dot(radius=radius, color=color, stroke_width=0) for _ in range(count)])
    elapsed = 0.0

    def circulate(group, dt):
        nonlocal elapsed
        elapsed += dt
        # Interleave the density ranks so even a few packets span the whole vessel.
        for i, bead in enumerate(group):
            t = (i / count + speed * elapsed) % 1
            where = t * length
            bead.move_to(pt(np.interp(where, distances, points[:, 0]),
                            np.interp(where, distances, points[:, 1])))
            rank = (i * (count - 5)) % count
            bead.set_opacity(float(np.clip(amount.get_value() * count - rank, 0, 1)))

    circulate(beads, 0)
    if active:
        beads.add_updater(circulate)
    return beads


def nerves(broken=False):
    def wire(x0, x1):
        return Line(pt(x0, 2.41), pt(x1, 2.41), color=BLUE, stroke_width=7)
    ends = VGroup(Line(pt(-4.12, 1.94), pt(-4.12, 2.41), color=BLUE, stroke_width=7),
                  Line(pt(4.05, 2.41), pt(4.05, 1.94), color=BLUE, stroke_width=7))
    g = VGroup(ends, wire(-4.12, -0.30), wire(0.30, 4.05))
    if broken:
        g.add(*[Line(pt(x - 0.10, 2.25), pt(x + 0.10, 2.57),
                     color=BLUE, stroke_width=4) for x in (-0.32, 0.32)])
    else:
        g.add(wire(-0.30, 0.30))
    return g


def organ(kind="gland", center=SOURCE):
    if kind == "fat":
        shape = VGroup(*[Circle(radius=0.31, stroke_color=PURPLE, stroke_width=2.5,
                                 fill_color=PURPLE, fill_opacity=0.52).move_to(pt(x, y))
                         for x, y in [(-0.38, -0.13), (0, 0.22), (0.38, -0.13)]])
    elif kind == "lesion":
        shape = VGroup(Ellipse(width=1.45, height=0.78, stroke_color=GREY, stroke_width=3,
                               fill_color=GREY, fill_opacity=0.20),
                       Line(pt(-0.24, -0.23), pt(0.24, 0.23), color=GREY, stroke_width=4),
                       Line(pt(-0.24, 0.23), pt(0.24, -0.23), color=GREY, stroke_width=4))
    else:
        shape = VGroup(Ellipse(width=1.42, height=0.85, stroke_color=PURPLE, stroke_width=3,
                               fill_color=PURPLE, fill_opacity=0.60),
                       ArcBetweenPoints(pt(-0.49, -0.13), pt(0.20, 0.24), angle=-1.0)
                       .set_stroke(PURPLE, 5))
    return shape.move_to(center)


def pump(center=GRAFT):
    shell = RoundedRectangle(width=1.41, height=0.73, corner_radius=0.17,
                             stroke_color=BLUE, stroke_width=3, fill_color=BLUE, fill_opacity=0.24)
    chamber = RoundedRectangle(width=0.87, height=0.33, corner_radius=0.11,
                               stroke_width=0, fill_color=ORANGE, fill_opacity=0.93)
    port = Line(pt(0.70, 0), pt(0.94, 0), color=BLUE, stroke_width=8)
    return VGroup(shell, chamber, port).move_to(center)


def graft_vessel():
    return Line(pt(-4.12, -1.79), pt(-4.12, -2.49), color=CRIMSON, stroke_width=10)


def pump_vessel():
    return VMobject(stroke_color=BLUE, stroke_width=5).set_points_as_corners(
        [pt(-3.32, -1.42), pt(-3.00, -1.42), pt(-3.00, -2.52)])


def paired_pump():
    return VGroup(pump_vessel(), pump()).scale(0.52, about_point=ORIGIN).shift(UP * 1.59)


def response(level, center=TARGET, width=2.12, height=0.58):
    outline = RoundedRectangle(width=width, height=height, corner_radius=0.15,
                               stroke_color=GREEN, stroke_width=3, fill_color=BG, fill_opacity=1)
    outline.move_to(center)
    left = center[0] - width / 2 + 0.10

    def fill():
        w = max(0.025, (width - 0.20) * level.get_value())
        return RoundedRectangle(width=w, height=height - 0.20, corner_radius=min(0.12, w / 2),
                                stroke_width=0, fill_color=GREEN, fill_opacity=1).move_to(
                                    pt(left + w / 2, center[1]))

    return VGroup(outline, always_redraw(fill))


def comb(level):
    base = RoundedRectangle(width=1.43, height=0.19, corner_radius=0.09, stroke_width=0,
                            fill_color=GREEN, fill_opacity=0.8).move_to(TARGET + DOWN * 0.32)

    def crest():
        top = Polygon(pt(-0.70, 0), pt(-0.58, 0.54), pt(-0.34, 0.37), pt(-0.15, 0.88),
                      pt(0.12, 0.51), pt(0.38, 0.73), pt(0.65, 0.08), pt(0.70, 0),
                      stroke_width=2, color=GREEN, fill_color=GREEN, fill_opacity=0.65)
        top.stretch(0.26 + 0.74 * level.get_value(), 1, about_edge=DOWN)
        return top.shift(TARGET + DOWN * 0.25)

    return VGroup(base, always_redraw(crest))


def world(amount, active=True):
    body, route = vessel()
    return VGroup(body, moving_signal(route, amount, active=active)), route


def joined_world(amount, lower_amount, active=True):
    """Two copies of the same vessel and nerve diagram, stacked with their own routes."""
    anatomy, route = vessel()
    diagrams, signals = VGroup(), VGroup()
    for y, level in [(1.59, amount), (-1.28, lower_amount)]:
        offset = pt(0, y)
        diagrams.add(VGroup(anatomy.copy(), nerves()).scale(0.52, about_point=ORIGIN).shift(offset))
        signals.add(moving_signal(route * 0.52 + offset, level, active, radius=0.095, count=17, speed=0.24))
    bridges = VGroup(*[Line(pt(x, 0.29), pt(x, -0.69), color=CRIMSON, stroke_width=15)
                       for x in (-2.60, 2.60)])
    return diagrams, bridges, signals


def feed_track(y, amount, pulsed, active):
    left, right = -2.42, 1.78
    tube = RoundedRectangle(width=right - left, height=0.38, corner_radius=0.19,
                            stroke_color=ORANGE, stroke_width=2.5, fill_color=ORANGE, fill_opacity=0.17)
    tube.move_to(pt((left + right) / 2, y))
    path = np.array([pt(left + 0.19, y), pt(right - 0.19, y)])
    if pulsed:
        # The repeating gap makes the input visibly intermittent.
        packets = VGroup(*[Dot(radius=0.093, color=YELLOW, stroke_width=0) for _ in range(9)])
        elapsed = 0.0

        def flow(group, dt):
            nonlocal elapsed
            elapsed += dt
            for i, bead in enumerate(group):
                cluster, inside = divmod(i, 3)
                u = (cluster / 3 + inside * 0.035 + elapsed * 0.32) % 1
                bead.move_to(interpolate(path[0], path[1], u))
        flow(packets, 0)
        if active:
            packets.add_updater(flow)
    else:
        packets = moving_signal(path, amount, active, speed=0.32, radius=0.081, count=21)
    return VGroup(tube, packets)


def timing_world(flow_rate, active=True):
    """Rebuilt at the same coordinates for prediction, the silent pause and the answer."""
    outlines, _ = vessel()
    brain = organ("lesion", SOURCE)
    names = VGroup(label("Hypothalamus", -3.53, 0.90), label("Pituitary", 4.05, 0.97))
    infuser = pump(pt(-4.12, -1.03))
    split = VGroup(Line(pt(-3.30, -1.03), pt(-2.82, -1.03), color=BLUE, stroke_width=5),
                   Line(pt(-2.82, -1.03), pt(-2.82, 0.21), color=BLUE, stroke_width=5),
                   Line(pt(-2.82, 0.21), pt(-2.42, 0.21), color=BLUE, stroke_width=5),
                   Line(pt(-2.82, -1.03), pt(-2.42, -1.03), color=BLUE, stroke_width=5))
    upper = VGroup(feed_track(0.21, flow_rate, True, active), label("Hourly bursts", -0.32, 0.70, ORANGE))
    lower = VGroup(feed_track(-1.03, flow_rate, False, active), label("Steady drip", -0.32, -0.54, ORANGE))
    return outlines, brain, names, infuser, split, upper, lower


def replacement_flow(active=True):
    _, route = vessel()
    return moving_signal(route, ValueTracker(0.58), active=active)


def predict_card():
    return question_card(QUESTION, size=34, y=-3.33)


class S01Hook(SpokenScene):
    def construct(self):
        blood = ValueTracker(0.42)
        growth = ValueTracker(0)
        diagram, _ = world(blood)
        source = organ()
        target = comb(growth)
        nerve = nerves()
        mark = label("?", 1.24, 3.19, GOLD, 49)
        self.add(diagram, nerve, source, target, mark, scope_tag())
        self.at("an organ change")
        source_name = label("Testis", -4.12, 0.96, PURPLE)
        self.play(FadeIn(source_name),
                  FadeIn(label("Comb", 4.05, -0.73, GREEN)), run_time=0.65)
        self.at("without its own nerves")
        self.play(Indicate(nerve, color=TEXT, scale_factor=1), run_time=0.62)
        self.play(FadeOut(nerve), FadeIn(nerves(True)), run_time=0.42)
        self.at("in 1849")
        date = tag("1849")
        self.play(FadeOut(mark), run_time=0.23)
        self.play(FadeIn(date), run_time=0.4)
        self.at("put a testis back")
        self.play(FadeOut(source_name), source.animate.move_to(GRAFT), run_time=1.65)
        self.play(Create(graft_vessel()), FadeIn(label("Testis", -4.12, -0.69, PURPLE)), run_time=0.48)
        self.at("cut off from its")
        self.play(blood.animate.set_value(0.68), run_time=2.4)
        self.at("birds grow combs")
        self.play(growth.animate.set_value(1), run_time=1.35)
        self.finish()


class S02Title(TitleCard):
    TITLE = "Take Out the Gland, Put Back the Signal"
    LESSON = "Extirpation, replacement and parabiosis"

    def construct(self):
        diagram, _ = world(ValueTracker(0.68))
        title = fit_text(self.TITLE, max_w=10.6, size=49, min_size=42, font=TITLE_FONT)
        lesson = label(self.LESSON, 0, 0, GOLD, 28)
        plate = RoundedRectangle(width=11.26, height=2.11, corner_radius=0.28,
                                 stroke_width=0, fill_color=BG, fill_opacity=0.96)
        text = VGroup(lesson, title).arrange(DOWN, buff=0.24).move_to(plate)
        self.add(diagram)
        self.play(FadeIn(plate), FadeIn(text), run_time=0.48)
        self.wait(1.04)
        self.play(FadeOut(text), FadeOut(plate), run_time=0.48)


class S03Extirpation(SpokenScene):
    def construct(self):
        blood, activity = ValueTracker(0.83), ValueTracker(0.92)
        diagram, _ = world(blood)
        source, nerve = organ(), nerves()
        gauge = response(activity)
        source_name = label("Gland", -4.12, -0.67, PURPLE)
        self.add(diagram, nerve, source, gauge, label("Target response", 3.65, -0.67, GREEN), scope_tag())
        self.at("find a chemical signal")
        self.play(FadeIn(source_name), run_time=0.45)
        self.at("take its source away")
        self.play(FadeOut(source_name), FadeOut(source, shift=UP * 0.67), run_time=1.0)
        self.at("disabling it with")
        disabled = organ("lesion")
        self.play(FadeIn(disabled), run_time=0.55)
        self.at("called extirpation")
        heading = tag("Extirpation")
        self.play(FadeIn(heading), run_time=0.55)
        self.at("once secretion stops")
        self.play(FadeOut(disabled), run_time=0.5)
        self.at("normal clearance drains")
        drain = arrow(pt(0, -2.07), pt(0, -3.06), YELLOW)
        drain_name = label("Clearance", 0, -3.44, YELLOW)
        self.play(GrowArrow(drain), run_time=0.45)
        self.play(FadeIn(drain_name), blood.animate.set_value(0.22), run_time=2.0)
        self.at("target response falls")
        self.play(activity.animate.set_value(0), blood.animate.set_value(0), run_time=2.52)
        self.at("removal shows need")
        self.play(FadeOut(drain), FadeOut(drain_name), FadeOut(heading), run_time=0.48)
        self.at("surgery might also cut")
        self.play(Indicate(nerve, color=TEXT, scale_factor=1), run_time=0.68)
        self.play(FadeOut(nerve), FadeIn(nerves(True)), run_time=0.40)
        self.finish()


class S04Replacement(SpokenScene):
    def construct(self):
        blood, activity = ValueTracker(0), ValueTracker(0)
        diagram, _ = world(blood)
        nerve = nerves(True)
        self.add(diagram, nerve, response(activity), label("Target response", 3.65, -0.67, GREEN), scope_tag())
        self.at("rule out cut nerves")
        graft = organ(center=GRAFT)
        graft_link = graft_vessel()
        self.play(Indicate(nerve, color=TEXT, scale_factor=1),
                  FadeIn(graft, shift=DOWN * 0.38), Create(graft_link), run_time=1.45)
        self.at("you next test")
        heading = tag("Replacement")
        self.play(FadeIn(heading), run_time=0.50)
        self.at("place the organ")
        self.play(Indicate(graft, color=PURPLE, scale_factor=1.17),
                  blood.animate.set_value(0.24), run_time=1.65)
        self.at("deliver the missing hormone")
        self.play(ReplacementTransform(graft, pump()),
                  ReplacementTransform(graft_link, pump_vessel()), run_time=1.0)
        self.at("droplets refill the blood")
        self.play(blood.animate.set_value(0.80), run_time=1.7)
        self.at("target response recovers")
        self.play(activity.animate.set_value(0.92), run_time=2.05)
        self.at("chemical carries the signal")
        self.play(swap(heading, tag("Signal in blood", YELLOW)))
        self.finish()


class S05ParabiosisIdea(SpokenScene):
    def construct(self):
        upper, lower, activity = ValueTracker(0.80), ValueTracker(0), ValueTracker(0)
        diagrams, bridges, streams = joined_world(upper, lower)
        upper_meter = response(ValueTracker(0.92), pt(2.10, 1.59), width=1.10, height=0.35)
        lower_meter = response(activity, pt(2.10, -1.26), width=1.10, height=0.35)
        diagram, _ = world(upper)
        full = VGroup(diagram, nerves(True), pump_vessel(), pump(), response(ValueTracker(0.92)))
        self.add(full, scope_tag())
        self.at("test blood transport directly")
        # Scale the vessel and nerve landmarks before introducing the second animal.
        diagram[1].clear_updaters()
        self.play(full.animate.scale(0.52, about_point=ORIGIN).shift(UP * 1.59), run_time=1.50)
        self.remove(full)
        self.add(diagrams[0], streams[0], upper_meter, paired_pump())
        self.play(FadeIn(diagrams[1], shift=UP * 0.45), FadeIn(lower_meter), run_time=1.35)
        self.at("joining two animal")
        self.play(Create(bridges), run_time=0.83)
        self.play(FadeIn(tag("Parabiosis")), run_time=0.5)
        self.at("bloodborne factors cross")
        crossing = VGroup(*[moving_signal(np.array([pt(x, a), pt(x, b)]), upper, radius=0.085,
                                           count=4, speed=1.12)
                            for x, a, b in [(-2.60, 0.30, -0.70), (2.60, -0.70, 0.30)]])
        self.add(crossing, streams[1])
        self.play(lower.animate.set_value(0.42), activity.animate.set_value(0.54), run_time=1.75)
        self.at("nervous system stays separate")
        self.play(Indicate(diagrams[0][1], color=BLUE, scale_factor=1),
                  Indicate(diagrams[1][1], color=BLUE, scale_factor=1), run_time=1.0)
        self.at("here is the core rule")
        steps = VGroup(*[boxed_label(t, GOLD, size=28, pad=0.11)
                         for t in ("Remove", "Replace", "Share blood")]).arrange(RIGHT, buff=0.24)
        steps.move_to(pt(0, -3.45))
        self.at("remove the source")
        self.play(FadeIn(steps[0]), run_time=0.53)
        self.at("replace the signal")
        self.play(FadeIn(steps[1]), run_time=0.53)
        self.at("join blood streams")
        self.play(FadeIn(steps[2]), run_time=0.53)
        self.finish()


class S06Predict(SpokenScene):
    def construct(self):
        rate = ValueTracker(0.78)
        outline, brain, names, infuser, split, upper, lower = timing_world(rate)
        one, two, flow = joined_world(ValueTracker(0.80), ValueTracker(0.42))
        paired = VGroup(one, two, flow, paired_pump(),
                        response(ValueTracker(0.92), pt(2.10, 1.59), width=1.10, height=0.35),
                        response(ValueTracker(0.54), pt(2.10, -1.26), width=1.10, height=0.35))
        self.add(paired, scope_tag())
        self.at("yet replacement is")
        self.play(FadeOut(one[1]), FadeOut(two), FadeOut(flow), FadeOut(paired[3]),
                  FadeOut(paired[4]), FadeOut(paired[5]), FadeOut(one[0][1]), run_time=0.68)
        main_vessel = one[0][0]
        self.play(Transform(main_vessel, outline), run_time=1.63)
        supply = ValueTracker(0.58)
        _, route = vessel()
        circulation = moving_signal(route, supply)
        self.add(circulation)
        intact = organ()
        self.play(FadeIn(intact), run_time=0.55)
        self.at("in rhesus monkeys")
        self.play(FadeIn(names[0]), run_time=0.55)
        self.at("hypothalamic lesions cut off")
        self.play(ReplacementTransform(intact, brain), run_time=0.69)
        self.play(supply.animate.set_value(0), run_time=2.03)
        self.remove(circulation)
        self.at("called gnrh")
        heading = tag("GnRH", YELLOW)
        self.play(FadeIn(heading), run_time=0.53)
        self.at("a pump replaces it")
        self.play(FadeIn(infuser), Create(split), run_time=0.67)
        self.at("hourly bursts")
        self.play(FadeIn(upper), run_time=0.52)
        self.add(replacement_flow())
        self.at("a steady drip")
        self.play(FadeIn(lower), run_time=0.55)
        self.at("which schedule restores")
        mark = label("?", 4.05, -0.22, GOLD, 60)
        self.play(FadeIn(predict_card()), FadeIn(mark), FadeIn(names[1]), run_time=0.55)
        pulse(mark, base=1, amp=0.7, speed=2.9)
        self.finish()


class S07PredictPause(Scene):
    def construct(self):
        self.camera.background_color = BG
        rate = ValueTracker(0.78)
        self.add(*timing_world(rate, active=False), replacement_flow(active=False), tag("GnRH", YELLOW),
                 label("?", 4.05, -0.22, GOLD, 60), predict_card(), scope_tag())
        self.wait(4.5)


class S08ControlsTiming(SpokenScene):
    def construct(self):
        rate = ValueTracker(0.78)
        burst_response, drip_response = ValueTracker(0), ValueTracker(0.68)
        outline, brain, names, infuser, split, upper, lower = timing_world(rate)
        heading, mark, question = tag("GnRH", YELLOW), label("?", 4.05, -0.22, GOLD, 60), predict_card()
        self.add(outline, replacement_flow(), brain, names, infuser, split, upper, lower,
                 heading, mark, question, scope_tag())
        self.at("only the hourly bursts")
        self.play(FadeOut(mark), FadeOut(question), run_time=0.36)
        burst_meter = response(burst_response, pt(4.00, 0.21), width=2.29, height=0.41)
        self.add(burst_meter)
        self.play(burst_response.animate.set_value(0.95), run_time=1.25)
        left_stream = arrow(pt(3.40, -0.04), pt(3.18, -0.45), GREEN)
        right_stream = arrow(pt(4.60, -0.04), pt(4.82, -0.45), GREEN)
        lh, fsh = label("LH", 3.14, -0.75, GREEN), label("FSH", 4.88, -0.75, GREEN)
        self.at("luteinizing hormone")
        self.play(GrowArrow(left_stream), FadeIn(lh), run_time=0.57)
        self.at("follicle stimulating hormone")
        self.play(GrowArrow(right_stream), FadeIn(fsh), run_time=0.57)
        self.at("the steady drip shuts")
        self.play(FadeOut(left_stream), FadeOut(right_stream), FadeOut(lh), FadeOut(fsh), run_time=0.42)
        drip_meter = response(drip_response, pt(4.00, -1.03), width=2.29, height=0.41)
        self.play(FadeIn(drip_meter), drip_response.animate.set_value(0), run_time=2.0)
        self.at("drip ran at four rates")
        level = ValueTracker(0.18)
        dial_view = dial(level, pt(-3.56, -3.52), radius=0.42, color=ORANGE)
        dial_view.remove(dial_view[3])
        rate_label = label("Drip rate", -5.21, -3.25, ORANGE)
        # The number is the tested setting index; the dial is only schematic.
        setting = ValueTracker(1)
        rate_number = counter("Rate {:.0f} of 4", setting, pt(-1.51, -3.25), size=28)
        self.play(FadeIn(dial_view), FadeIn(rate_label), FadeIn(rate_number),
                  rate.animate.set_value(0.27), run_time=0.62)
        self.play(level.animate.set_value(0.38), rate.animate.set_value(0.43),
                  setting.animate.set_value(2), run_time=0.77)
        self.at("the two highest")
        match = label("Matches burst dose", 2.24, -3.25, YELLOW)
        more = label("Exceeds burst dose", 2.24, -3.25, YELLOW)
        self.play(level.animate.set_value(0.67), rate.animate.set_value(0.74),
                  setting.animate.set_value(3), FadeIn(match), run_time=0.82)
        self.at("or more")
        self.play(level.animate.set_value(0.97), rate.animate.set_value(1),
                  setting.animate.set_value(4), swap(match, more), run_time=0.81)
        self.at("dose cannot explain")
        result = tag("Not too little hormone", YELLOW)
        self.play(swap(heading, result))
        self.at("the usual answer is")
        self.play(FadeOut(dial_view), FadeOut(rate_label), FadeOut(rate_number), FadeOut(more), run_time=0.56)
        self.play(swap(result, tag("Desensitization")))
        self.at("cells turn their response down")
        self.play(Indicate(drip_meter[0], color=GREY, scale_factor=1.08), run_time=1.48)
        self.finish()


class S09Limits(SpokenScene):
    def construct(self):
        blood, activity = ValueTracker(0), ValueTracker(0)
        outline, brain, names, infuser, split, upper, lower = timing_world(ValueTracker(1))
        old_target = response(ValueTracker(0), pt(4.00, -1.03), width=2.29, height=0.41)
        old_burst = response(ValueTracker(0.95), pt(4.00, 0.21), width=2.29, height=0.41)
        old_heading = tag("Desensitization")
        self.add(outline, brain, names, infuser, split, upper, lower, old_target,
                 old_burst, old_heading, scope_tag())
        self.at("replacement also fails")
        self.play(FadeOut(brain), FadeOut(names), FadeOut(split), FadeOut(upper), FadeOut(lower),
                  FadeOut(old_target), FadeOut(old_burst), FadeOut(old_heading),
                  infuser.animate.move_to(GRAFT), run_time=1.05)
        tissue = organ("fat")
        diagram, _ = world(blood)
        gauge = response(activity)
        self.add(diagram[1])
        pump_link = pump_vessel()
        self.play(FadeIn(tissue), FadeIn(gauge), run_time=0.63)
        self.at("fat cells make")
        fat_label = label("Fat cells", -4.12, 0.97, PURPLE)
        brain_label = label("Brain", 4.05, 0.97)
        leptin = tag("Leptin", YELLOW)
        self.play(FadeIn(fat_label), FadeIn(leptin), blood.animate.set_value(0.54), run_time=1.1)
        self.at("fuel gauge reporting")
        self.play(FadeIn(brain_label), activity.animate.set_value(0.62), run_time=1.6)
        self.at("stored energy", lead=-0.86)
        empty = tag("No leptin")
        self.play(swap(leptin, empty), blood.animate.set_value(0), activity.animate.set_value(0),
                  run_time=0.75)
        replaced = tag("Leptin replaced", YELLOW)
        self.at("leptin replacement worked")
        self.play(swap(empty, replaced, run_time=0.52), Create(pump_link, run_time=0.52),
                  blood.animate(run_time=1.12).set_value(0.57),
                  activity.animate(run_time=1.12).set_value(0.82))
        self.at("unable to make it", lead=0)
        self.play(Indicate(gauge[0], color=GREEN, scale_factor=1.08), run_time=1.25)
        self.at("most people with")
        high = tag("High leptin", YELLOW)
        self.play(swap(replaced, high), FadeOut(pump_link), blood.animate.set_value(0.82), activity.animate.set_value(0.25),
                  run_time=1.35)
        self.at("replacement does not reliably")
        self.play(Indicate(infuser, color=ORANGE, scale_factor=1.1), Create(pump_link), run_time=0.55)
        self.play(blood.animate.set_value(1), activity.animate.set_value(0.29), run_time=1.43)
        self.finish()


class S10UnlockedA(SpokenScene):
    def construct(self):
        blood, growth = ValueTracker(0.61), ValueTracker(0.15)
        diagram, _ = world(blood)
        graft = organ(center=GRAFT)
        nerve = nerves(True)
        crest = comb(growth)
        cockerel_names = VGroup(label("Testis", -4.12, -0.69, PURPLE), label("Comb", 4.05, -0.73, GREEN))
        date = tag("1849")
        graft_link = graft_vessel()
        self.add(diagram, graft_link, graft, nerve, crest, scope_tag())
        self.at("in 1849")
        self.play(FadeIn(date), FadeIn(cockerel_names), run_time=0.59)
        self.at("relocating a testis")
        self.play(Indicate(graft, color=PURPLE), blood.animate.set_value(0.80), run_time=1.5)
        self.at("organ can act")
        self.play(growth.animate.set_value(1), run_time=2.0)
        self.at("in rhesus monkeys")
        self.play(FadeOut(date), FadeOut(nerve), FadeOut(graft), FadeOut(graft_link), FadeOut(crest), FadeOut(cockerel_names),
                  blood.animate.set_value(0.17), run_time=0.71)
        infuser = pump(pt(-4.12, 0.21))
        feed_link = Line(pt(-3.30, 0.21), pt(-2.42, 0.21), color=BLUE, stroke_width=5)
        burst = feed_track(0.21, blood, True, True)
        drip = feed_track(0.21, ValueTracker(1.0), False, True)
        self.play(FadeIn(infuser), Create(feed_link), FadeIn(burst), run_time=0.48)
        self.at("pulsed gnrh replacement")
        burst_label = label("Pulsed GnRH", -0.32, 0.72, ORANGE)
        self.play(FadeIn(burst_label), run_time=0.45)
        pituitary, testosterone = ValueTracker(0.85), ValueTracker(0.85)
        pit_meter = response(pituitary, pt(4.05, 0.21))
        test_meter = response(testosterone, pt(4.05, -0.99))
        pit_name = label("Pituitary", 4.05, 0.93)
        self.play(FadeIn(pit_meter), FadeIn(pit_name), run_time=0.73)
        self.at("medicine uses that rule")
        self.play(Indicate(infuser, color=ORANGE, scale_factor=1.1), run_time=1.25)
        self.at("luprolide")
        self.play(FadeOut(burst), FadeOut(burst_label), run_time=0.30)
        self.play(FadeIn(drip, run_time=0.42), FadeIn(tag("Slow-release leuprolide", ORANGE), run_time=0.42),
                  blood.animate(run_time=1.0).set_value(0.73))
        self.at("stays steady")
        self.play(FadeIn(test_meter), FadeIn(label("Testosterone", 3.82, -1.54)), run_time=0.52)
        self.at("the pituitary quiets")
        self.play(pituitary.animate.set_value(0.08), run_time=1.12)
        self.at("testosterone falls")
        self.play(testosterone.animate.set_value(0.13), run_time=2.05)
        self.finish()


class S11UnlockedB(SpokenScene):
    def construct(self):
        blood, fuel = ValueTracker(0.84), ValueTracker(0.77)
        diagram, _ = world(blood)
        tissue = organ("fat")
        fuel_dial = dial(fuel, pt(4.05, -0.42), radius=0.94, color=GREEN)
        fuel_dial.remove(fuel_dial[3])
        fat_label = label("Fat cells", -4.12, 0.96, PURPLE)
        brain_label = label("Brain", 4.05, 0.97)
        fuel_label = label("Fuel gauge", 4.05, -0.88, GREEN)
        authors = tag("Ahima and colleagues, 1996")
        self.add(diagram, tissue, fuel_dial, fat_label, brain_label, fuel_label, scope_tag())
        self.at("in 1996")
        self.play(FadeIn(authors), run_time=0.53)
        self.at("falling leptin in")
        self.play(blood.animate.set_value(0.33), fuel.animate.set_value(0.37), run_time=2.4)
        self.at("the starvation response")
        low = caption("Starvation response", color=GOLD, y=-3.28)
        self.play(FadeIn(low), fuel.animate.set_value(0.13), run_time=0.70)
        self.at("because leptin tracks")
        leptin = tag("Leptin", YELLOW)
        self.play(swap(authors, leptin), blood.animate.set_value(0.18), run_time=1.4)
        self.at("signals low fuel")
        self.play(Indicate(fuel_label, color=GREEN, scale_factor=1.08), run_time=1.32)
        self.at("take away the source")
        target_level = ValueTracker(0.15)
        target = response(target_level)
        self.play(FadeOut(low), FadeOut(fuel_dial), FadeOut(fuel_label),
                  FadeOut(fat_label), FadeOut(brain_label), FadeOut(leptin), run_time=0.40)
        self.play(Transform(tissue, organ()), FadeIn(target), run_time=0.62)
        self.at("restore the pattern")
        self.play(blood.animate.set_value(0.69), target_level.animate.set_value(0.83), run_time=1.15)
        self.at("shared blood reveals")
        self.play(Indicate(tissue, color=PURPLE, scale_factor=1.11),
                  Indicate(diagram[0][0], color=CRIMSON, scale_factor=1),
                  Indicate(target[0], color=GREEN, scale_factor=1.07), run_time=1.6)
        self.finish()


class S12End(EndCard):
    LINE = "Remove the source, replace the signal, show what travels in blood."
