"""When people change the flow — Matter cycles, chapter 2.

COLOR MAP (kept exactly from chapter 1)
  BLUE   = water
  ORANGE = carbon
  GREEN  = nitrogen
  GOLD   = sunlight
  RED    = human-added flow outline only
  GREY   = air, ground, outlines and neutral labels

All landscapes are rebuilt by watershed() at the same scale and coordinates.
"""
from bp_parts import *  # noqa: F401,F403


ORANGE = "#F29E4C"


def P(x, y):
    return np.array([x, y, 0.0])


def allow(*mobs):
    """Mark deliberate labels-on-shapes as safe for the layout checker."""
    for mob in mobs:
        for part in mob.get_family():
            part.layout_ok = True
    return mobs[0] if len(mobs) == 1 else mobs


def token(letter, color, radius=0.20):
    box = RoundedRectangle(
        corner_radius=0.07, width=radius * 2.2, height=radius * 2.2,
        stroke_color=color, stroke_width=2.5, fill_color=color, fill_opacity=1,
    )
    label = T(letter, 24, BG, weight=BOLD).move_to(box)
    allow(label)
    return VGroup(box, label)


def flow_arrow(start, end, color, width=7, red_outline=False, dashed=False):
    cls = DashedLine if dashed else Arrow
    kw = dict(color=color, stroke_width=width)
    if dashed:
        line = cls(start, end, dash_length=0.15, **kw)
    else:
        line = cls(start, end, buff=0.04, tip_length=0.26,
                   max_stroke_width_to_length_ratio=12, **kw)
    if not red_outline:
        return line
    outline = Arrow(start, end, buff=0.04, tip_length=0.32, color=RED,
                    stroke_width=width + 7, stroke_opacity=0.85,
                    max_stroke_width_to_length_ratio=14)
    line.set_z_index(2)
    return VGroup(outline, line)


def watershed(dim=1.0):
    """The one carried world, matching chapter 1's farm/river/Bay geography."""
    sky = Rectangle(width=13.2, height=2.7, stroke_width=0, fill_color=BLUE,
                    fill_opacity=0.055).move_to(P(0, 2.15))
    ground = Polygon(P(-6.6, 0.75), P(-4.8, 1.0), P(-2.8, 0.35), P(-0.8, -0.15),
                     P(1.4, -0.65), P(6.6, -0.75), P(6.6, -3.0), P(-6.6, -3.0),
                     stroke_color=GREY, stroke_width=3, fill_color=GREY, fill_opacity=0.12)
    field = Polygon(P(-6.1, 0.58), P(-4.8, 0.82), P(-3.3, 0.3), P(-4.0, -0.35),
                    P(-6.15, -0.05), stroke_color=GOLD, stroke_width=3,
                    fill_color=GOLD, fill_opacity=0.13)
    rows = VGroup(*[Line(P(-5.8 + i * 0.55, 0.38 - i * 0.08),
                              P(-5.1 + i * 0.55, -0.12 - i * 0.08),
                              color=GOLD, stroke_width=2) for i in range(4)])
    river = VMobject(stroke_color=BLUE, stroke_width=18, stroke_opacity=0.78)
    river.set_points_smoothly([P(-3.3, 0.15), P(-2.1, -0.5), P(-0.9, -0.25),
                               P(0.1, -0.95), P(1.4, -1.15), P(2.2, -1.0)])
    current = VGroup()
    for i in range(16):
        drop = Dot(river.point_from_proportion(i / 16), radius=0.11, color=TEXT).set_opacity(0.72)
        drop.phase = i / 16

        def flow(mob, dt, path=river):
            mob.phase = (mob.phase + 0.075 * dt) % 1.0
            mob.move_to(path.point_from_proportion(mob.phase))

        drop.add_updater(flow)
        current.add(drop)
    bay = Ellipse(width=5.0, height=2.45, stroke_color=BLUE, stroke_width=4,
                  fill_color=BLUE, fill_opacity=0.20).move_to(P(4.25, -1.55))
    cloud = VGroup(*[Circle(r, stroke_color=GREY, stroke_width=2,
                            fill_color=GREY, fill_opacity=0.16).move_to(p)
                     for r, p in [(0.42, P(-4.6, 2.65)), (0.58, P(-4.0, 2.78)),
                                  (0.43, P(-3.35, 2.62))]])
    crab_body = Ellipse(width=1.15, height=0.65, stroke_color=ORANGE, stroke_width=4,
                        fill_color=ORANGE, fill_opacity=0.16).move_to(P(4.55, -1.6))
    crab = VGroup(crab_body,
                  *[Line(P(4.15 + 0.25 * i, -1.88), P(3.9 + 0.38 * i, -2.2),
                         color=ORANGE, stroke_width=3) for i in range(4)],
                  Arc(radius=0.34, start_angle=0.2, angle=2.4, color=ORANGE).move_to(P(3.95, -1.42)),
                  Arc(radius=0.34, start_angle=0.55, angle=2.4, color=ORANGE).move_to(P(5.15, -1.42)))
    labels = VGroup(
        T("FARM", 28, GOLD).move_to(P(-5.15, -0.65)),
        T("RIVER", 28, BLUE).move_to(P(-0.6, -0.55)),
        T("BAY", 28, BLUE).move_to(P(4.2, -2.75)),
        T("AIR", 28, GREY).move_to(P(1.1, 2.9)),
    )
    for lab in labels:
        allow(lab)
    g = VGroup(sky, ground, field, rows, river, current, bay, cloud, crab, labels)
    g.set_opacity(dim)
    g.sky, g.ground, g.field, g.river, g.bay, g.cloud, g.crab, g.labels = (
        sky, ground, field, river, bay, cloud, crab, labels
    )
    g.current = current
    return g


def rain_group():
    return VGroup(*[Line(P(-5.0 + i * 0.45, 2.15), P(-5.15 + i * 0.45, 1.62),
                              color=BLUE, stroke_width=4) for i in range(5)])


def meter(center, color=BLUE, level=0.50, height=3.7):
    """Transparent amount tank and a vertical amount meter."""
    c = np.array(center, dtype=float)
    tank = RoundedRectangle(corner_radius=0.22, width=3.2, height=height,
                            stroke_color=GREY, stroke_width=4, fill_color=BLUE,
                            fill_opacity=0.045).move_to(c)
    track = RoundedRectangle(corner_radius=0.08, width=0.46, height=height - 0.65,
                             stroke_color=GREY, stroke_width=2).move_to(c + RIGHT * 1.16)
    liquid = Rectangle(width=0.34, height=(height - 0.78) * level, stroke_width=0,
                       fill_color=color, fill_opacity=0.88)
    liquid.move_to(track.get_bottom() + UP * (0.08 + liquid.height / 2))
    amount = T("AMOUNT", 28, color).rotate(PI / 2).move_to(c + RIGHT * 0.55)
    allow(amount)
    return VGroup(tank, track, liquid, amount)


def tank_world(level=0.50, incoming=7, outgoing=7, wide_in=False):
    tank = meter(P(0, 0.3), BLUE, level)
    inp = flow_arrow(P(-5.7, 0.35), P(-1.7, 0.35), BLUE, 13 if wide_in else incoming)
    out = flow_arrow(P(1.7, 0.35), P(5.7, 0.35), BLUE, outgoing)
    in_lab = T("IN", 30, BLUE).move_to(P(-3.75, 1.0))
    out_lab = T("OUT", 30, BLUE).move_to(P(3.75, 1.0))
    return VGroup(tank, inp, out, in_lab, out_lab)


def evidence_cards():
    panels = TwoPanel("MEASURED RECORD", "MODELED FLOWS", colors=(ORANGE, GREEN),
                      top=2.9, bottom=-2.25, width=12.6, size=31)
    return panels


class FilmScene(SpokenScene):
    """Narrated scene with the film's slow moving particulate field behind long holds."""

    def setup(self):
        super().setup()
        currents = VGroup()
        for i in range(10):
            y = -3.45 + i * 0.76
            line = DashedLine(P(-7.2, y), P(7.2, y + 0.55), dash_length=0.16,
                              color=[BLUE, GREY, ORANGE, GREEN][i % 4],
                              stroke_width=2.5).set_opacity(0.16)
            line.velocity = P(0.42 + 0.04 * (i % 3), 0.016)

            def stream(mob, dt):
                mob.shift(mob.velocity * dt)
                if mob.get_left()[0] > -6.7:
                    mob.shift(LEFT * 1.5)

            line.add_updater(stream)
            currents.add(line)
        currents.set_z_index(-2)
        self.add(currents)

        motes = VGroup()
        for i in range(120):
            d = Dot(P(-6.4 + (i * 1.73) % 12.8, -3.4 + (i * 1.17) % 6.8),
                    radius=0.065 + 0.012 * (i % 3),
                    color=[BLUE, ORANGE, GREEN, GREY][i % 4]).set_opacity(0.38)
            d.velocity = P(0.20 + 0.025 * (i % 4), 0.12 + 0.02 * (i % 3))

            def drift(mob, dt):
                mob.shift(mob.velocity * dt)
                if mob.get_x() > 6.8:
                    mob.shift(LEFT * 13.6)
                if mob.get_y() > 3.8:
                    mob.shift(DOWN * 7.6)

            d.add_updater(drift)
            motes.add(d)
        motes.set_z_index(-1)
        self.add(motes)


class S00Hook(FilmScene):
    def construct(self):
        world = watershed()
        self.at("The first film")
        self.play(FadeIn(world), run_time=0.8)
        rain = rain_group()
        orange = token("C", ORANGE).move_to(P(1.0, 2.1))
        green = token("N", GREEN).move_to(P(-4.7, 0.15))
        blue = token("H₂O", BLUE, 0.25).move_to(P(-2.7, -0.05))
        self.play(FadeIn(rain), FadeIn(orange), FadeIn(green), FadeIn(blue), run_time=0.7)
        self.play(orange.animate.shift(RIGHT * 1.5), green.animate.shift(RIGHT * 1.2 + DOWN * 0.45),
                  blue.animate.shift(RIGHT * 1.8 + DOWN * 0.45), run_time=2.2, rate_func=linear)
        human = flow_arrow(P(-6.0, 0.9), P(-4.45, 0.45), GREEN, 8, red_outline=True)
        self.at("What happens when people")
        self.play(GrowFromEdge(human, LEFT), run_time=0.8)
        pulse(human[0], base=15, amp=3, speed=3)
        more = VGroup(*[token("N", GREEN).move_to(P(-5.7 + i * 0.33, 0.82 - i * 0.08))
                        for i in range(4)])
        self.play(LaggedStart(*[FadeIn(t) for t in more], lag_ratio=0.15), run_time=1.0)
        self.at("Return to the same watershed")
        self.play(more.animate.shift(RIGHT * 1.6 + DOWN * 0.45), run_time=2.2, rate_func=linear)
        self.finish()


class S01Title(TitleCard):
    LESSON = "Matter cycles"
    TITLE = "When People Change the Flow"


class S02Flow(FilmScene):
    def construct(self):
        world = watershed(0.28).scale(0.48).to_edge(LEFT, buff=0.35).shift(DOWN * 0.15)
        self.add(world)
        self.at("A flow is matter")
        tank = meter(P(2.3, 0.3), BLUE, 0.48, 4.4)
        self.play(FadeIn(tank[0]), run_time=0.6)
        moving = token("•", BLUE).move_to(P(-0.2, 0.3))
        self.play(FadeIn(moving), moving.animate.move_to(P(1.0, 0.3)), run_time=1.8)
        self.at("Picture each reservoir")
        self.play(FadeIn(VGroup(*tank[1:])), run_time=0.7)
        incoming = flow_arrow(P(-0.6, 0.3), P(0.7, 0.3), BLUE, 6)
        outgoing = flow_arrow(P(3.9, 0.3), P(5.8, 0.3), BLUE, 6)
        self.at("Arrows show matter")
        self.play(GrowArrow(incoming), GrowArrow(outgoing), run_time=0.8)
        streams = VGroup(*[Dot(P(-0.45 - i * 0.25, 0.3), radius=0.10, color=BLUE) for i in range(4)])
        self.play(FadeIn(streams), streams.animate.shift(RIGHT * 2.0), run_time=2.0, rate_func=linear)
        self.at("Their widths show")
        self.play(incoming.animate.set_stroke(width=12), outgoing.animate.set_stroke(width=4), run_time=1.1)
        tag = scope_tag("schematic")
        self.at("every amount here")
        self.play(FadeIn(tag), run_time=0.4)
        self.finish()


class S03Balance(FilmScene):
    def construct(self):
        w = tank_world()
        self.add(w)
        self.at("If matter enters")
        left = VGroup(*[Dot(P(-5.4 - i * 0.32, 0.35), radius=0.11, color=BLUE) for i in range(4)])
        right = VGroup(*[Dot(P(1.9 - i * 0.32, 0.35), radius=0.11, color=BLUE) for i in range(4)])
        self.play(FadeIn(left), FadeIn(right), run_time=0.4)
        self.play(left.animate.shift(RIGHT * 4.1), right.animate.shift(RIGHT * 4.1), run_time=2.4, rate_func=linear)
        same = chip("SAME AMOUNT", TEAL, 32).move_to(P(0, 3.0))
        self.at("the amount can stay steady")
        self.play(FadeIn(same, shift=DOWN * 0.1), run_time=0.6)
        self.at("That does not mean")
        self.play(same.animate.scale(1.06), rate_func=there_and_back, run_time=0.8)
        left2 = VGroup(*[Dot(P(-5.7 - i * 0.3, 0.35), radius=0.11, color=BLUE) for i in range(5)])
        right2 = VGroup(*[Dot(P(1.6 - i * 0.3, 0.35), radius=0.11, color=BLUE) for i in range(5)])
        self.at("Tokens keep crossing")
        self.play(FadeIn(left2), FadeIn(right2), run_time=0.3)
        self.play(left2.animate.shift(RIGHT * 4.5), right2.animate.shift(RIGHT * 4.5), run_time=2.7, rate_func=linear)
        self.finish()


class S04Carbon(FilmScene):
    def construct(self):
        underground = RoundedRectangle(corner_radius=0.22, width=5.2, height=1.45,
                                       stroke_color=GREY, stroke_width=4, fill_color=GREY,
                                       fill_opacity=0.15).move_to(P(0, -2.55))
        fossil = T("FOSSIL FUELS", 38, ORANGE).move_to(underground)
        allow(fossil)
        self.at("Coal")
        self.play(FadeIn(underground), FadeIn(fossil), run_time=1.0)
        air = meter(P(0, 1.1), ORANGE, 0.35, 2.6)
        self.at("Combustion moves")
        combustion = flow_arrow(P(0, -1.78), P(0, -0.18), ORANGE, 12, red_outline=True)
        lab = T("COMBUSTION", 30, ORANGE).move_to(P(-2.5, -0.9))
        self.play(FadeIn(air), GrowFromEdge(combustion, DOWN), FadeIn(lab), run_time=1.0)
        c = VGroup(*[token("C", ORANGE).move_to(P(-0.85 + i * 0.3, -1.55)) for i in range(4)])  # stays left of the AMOUNT label
        self.play(FadeIn(c), c.animate.shift(UP * 2.1), run_time=2.0, rate_func=linear)
        plant = chip("PLANTS", GREEN, 28).move_to(P(-4.8, 1.2))
        ocean = chip("OCEAN", BLUE, 28).move_to(P(4.8, 1.2))
        exch1 = DoubleArrow(P(-3.8, 1.2), P(-1.55, 1.2), color=ORANGE, stroke_width=3, tip_length=0.18)
        exch2 = DoubleArrow(P(1.55, 1.2), P(3.8, 1.2), color=ORANGE, stroke_width=3, tip_length=0.18)
        self.at("Plants and the ocean")
        self.play(FadeIn(plant), FadeIn(ocean), Create(exch1), Create(exch2), run_time=0.9)
        exlab = T("TWO-WAY EXCHANGE", 26, GREY).move_to(P(0, 3.1))
        uptake1 = flow_arrow(P(-1.55, 0.5), P(-3.75, 0.5), ORANGE, 3)
        uptake2 = flow_arrow(P(1.55, 0.5), P(3.75, 0.5), ORANGE, 3)
        net1 = T("NET UPTAKE: PLANTS", 24, ORANGE).move_to(P(-4.2, -0.15))
        net2 = T("NET UPTAKE: OCEAN", 24, ORANGE).move_to(P(4.2, -0.15))
        self.play(FadeIn(exlab), GrowArrow(uptake1), GrowArrow(uptake2), FadeIn(net1), FadeIn(net2), run_time=1.2)
        self.at("combustion adds it faster")
        new_liquid = Rectangle(width=0.34, height=1.35, stroke_width=0, fill_color=ORANGE, fill_opacity=0.88)
        new_liquid.move_to(air[1].get_bottom() + UP * (0.08 + new_liquid.height / 2))
        self.play(Transform(air[2], new_liquid), run_time=2.0, rate_func=linear)
        self.finish()


class S05Predict(FilmScene):
    QUESTION = "What happens to the amount in the reservoir?"

    def construct(self):
        w = tank_world()
        self.add(w)
        self.at("Start from the balanced tank")
        self.play(w[1].animate.set_stroke(width=7), w[2].animate.set_stroke(width=7), run_time=0.5)
        self.at("incoming flow grows wider")
        self.play(w[1].animate.set_stroke(width=13), run_time=1.3)
        approaching = VGroup(*[Dot(P(-5.7 - i * 0.3, 0.35), radius=0.11, color=BLUE) for i in range(6)])
        self.play(FadeIn(approaching), approaching.animate.shift(RIGHT * 2.8), run_time=1.8, rate_func=linear)
        self.at("outgoing flow stays")
        self.play(w[2].animate.set_stroke(width=7), run_time=0.5)
        q = question_card(self.QUESTION)
        self.at("What happens to the amount")
        self.play(FadeIn(q.question, shift=UP * 0.1), run_time=0.7)
        pulse(w[1], base=13, amp=2, speed=3)
        self.at("Hold your answer")
        self.play(approaching.animate.shift(RIGHT * 1.2), run_time=1.0, rate_func=linear)
        self.finish()


class S06Pause(PredictPause):
    QUESTION = "What happens to the amount in the reservoir?"
    SECONDS = 4.5

    def backdrop(self):
        w = tank_world(wide_in=True)
        approaching = VGroup(*[Dot(P(-3.0 - i * 0.32, 0.35), radius=0.11, color=BLUE) for i in range(6)])
        bob(approaching, amp=0.04, speed=1.6)
        return VGroup(w, approaching)


class S07Reveal(FilmScene):
    def construct(self):
        receive = tank_world(wide_in=True)
        source = meter(P(-5.2, 2.35), BLUE, 0.72, 2.2).scale(0.52)
        source_lab = T("SOURCE", 28, BLUE).next_to(source, UP, buff=0.12)
        dotted = flow_arrow(source.get_right(), P(-1.7, 0.35), BLUE, 3, dashed=True)
        self.add(receive)
        self.at("The amount rises")
        incoming = VGroup(*[Dot(P(-3.7 - i * 0.28, 0.35), radius=0.11, color=BLUE) for i in range(7)])
        self.play(FadeIn(incoming), incoming.animate.shift(RIGHT * 2.5), run_time=1.3, rate_func=linear)
        high = Rectangle(width=0.34, height=2.25, stroke_width=0, fill_color=BLUE, fill_opacity=0.88)
        high.move_to(receive[0][1].get_bottom() + UP * (0.08 + high.height / 2))
        self.play(Transform(receive[0][2], high), run_time=1.8, rate_func=linear)
        self.at("atoms were not created")
        self.play(FadeIn(source), FadeIn(source_lab), Create(dotted), run_time=0.9)
        low = Rectangle(width=0.34, height=0.75, stroke_width=0, fill_color=BLUE, fill_opacity=0.88)
        low.move_to(source[1].get_bottom() + UP * (0.08 + low.height / 2))
        self.play(Transform(source[2], low), run_time=1.4, rate_func=linear)
        self.at("They moved from another reservoir")
        transfer = VGroup(*[Dot(P(-4.1 - i * 0.28, 0.35), radius=0.10, color=BLUE) for i in range(5)])
        self.play(FadeIn(transfer), transfer.animate.shift(RIGHT * 3.4), run_time=2.2, rate_func=linear)
        self.add(scope_tag("schematic"))
        self.finish()


class S08Nitrogen(FilmScene):
    def construct(self):
        world = watershed()
        self.add(world)
        fertilizer = VGroup(*[token("N", GREEN).move_to(P(-5.65 + 0.45 * i, 0.55 - 0.12 * i)) for i in range(5)])
        add = flow_arrow(P(-6.15, 1.35), P(-5.15, 0.65), GREEN, 8, red_outline=True)
        self.at("People also add")
        self.play(GrowFromEdge(add, LEFT), FadeIn(fertilizer), run_time=1.1)
        rain = rain_group()
        self.at("Rain and flowing water")
        self.play(FadeIn(rain), run_time=0.6)
        runoff = flow_arrow(P(-5.25, 0.0), P(-1.8, -0.42), BLUE, 13)
        riders = VGroup(fertilizer[1].copy(), fertilizer[3].copy())
        self.play(GrowArrow(runoff), FadeIn(riders), run_time=0.6)
        self.play(riders.animate.move_to(P(-2.0, -0.35)), run_time=2.2, rate_func=linear)
        remain = VGroup(fertilizer[0], fertilizer[2], fertilizer[4])
        self.at("human-added flow rides")
        self.play(riders.animate.move_to(P(0.1, -0.85)), remain.animate.shift(DOWN * 0.35),
                  run_time=2.0, rate_func=linear)
        self.finish()


class S08Paths(FilmScene):
    def construct(self):
        origin = chip("ADDED N", GREEN, 34).move_to(P(-4.9, 0.2))
        self.add(origin)
        self.at("Not every added nitrogen")
        self.play(origin.animate.scale(1.06), rate_func=there_and_back, run_time=0.7)
        names = [("some: STAYS ON LAND", P(2.4, 2.35)), ("some: LIVING THINGS", P(2.4, 0.85)),
                 ("some: WATER", P(2.4, -0.65)), ("some: AIR", P(2.4, -2.15))]
        colors = [GOLD, GREEN, BLUE, GREY]
        branches, boxes = VGroup(), VGroup()
        for (name, pos), col in zip(names, colors):
            b = chip(name, col, 28).move_to(pos)
            a = flow_arrow(origin.get_right(), b.get_left(), GREEN, 3, dashed=True)
            branches.add(a)
            boxes.add(b)
        self.at("Some stays on land")
        self.play(Create(branches[0]), FadeIn(boxes[0]), run_time=0.8)
        self.at("some enters living things")
        self.play(Create(branches[1]), FadeIn(boxes[1]), run_time=0.8)
        self.at("some reaches water")
        self.play(Create(branches[2]), FadeIn(boxes[2]), run_time=0.8)
        self.at("some returns to the air")
        self.play(Create(branches[3]), FadeIn(boxes[3]), run_time=0.8)
        meters = VGroup()
        for i, ((_, pos), col) in enumerate(zip(names, colors)):
            track = RoundedRectangle(corner_radius=0.07, width=0.42, height=1.05,
                                     stroke_color=GREY, stroke_width=2).move_to(pos + RIGHT * 3.0)
            fill = Rectangle(width=0.30, height=0.22, stroke_width=0,
                             fill_color=col, fill_opacity=0.9)
            fill.move_to(track.get_bottom() + UP * (0.07 + fill.height / 2))
            meters.add(VGroup(track, fill))
        self.at("important question is how")
        self.play(FadeIn(meters), run_time=0.6)
        for i, m in enumerate(meters):
            hi = Rectangle(width=m[1].width, height=0.40 + i * 0.13, stroke_width=0,
                           fill_color=colors[i], fill_opacity=0.88)
            hi.move_to(m[0].get_bottom() + UP * (0.07 + hi.height / 2))
            self.play(Transform(m[1], hi), run_time=0.55)
        self.finish()


class S09Evidence(FilmScene):
    def construct(self):
        world = watershed(0.22)
        self.add(world)
        self.at("How can scientists tell")
        q = T("HOW DO WE KNOW?", 42, TEXT).move_to(P(0, 3.25))
        self.play(FadeIn(q), run_time=0.6)
        panels = evidence_cards()
        self.play(FadeIn(panels), FadeOut(q), run_time=0.8)
        instrument = VGroup(Rectangle(width=0.8, height=1.6, color=ORANGE, fill_opacity=0.12),
                            Circle(radius=0.18, color=ORANGE).shift(UP * 0.35)).move_to(P(-4.1, 0.4))
        axis = Plot(box=(-2.8, -0.2, -1.5, 1.5), xr=(0, 4), yr=(0, 4),
                    xticks=[], yticks=[], color=GREY)
        points = VGroup(*[Dot(axis.pt(i, 0.7 + 0.55 * i), radius=0.09, color=ORANGE) for i in range(5)])
        self.at("A measurement records")
        self.play(FadeIn(instrument), Create(axis), run_time=0.8)
        self.at("carbon dioxide in sampled air")
        self.play(LaggedStart(*[FadeIn(d) for d in points], lag_ratio=0.18), run_time=1.4)
        layers = VGroup(*[RoundedRectangle(corner_radius=0.08, width=1.4, height=0.75,
                                          stroke_color=GREEN, fill_color=GREEN, fill_opacity=0.08)
                          .move_to(P(2.9 + i * 0.18, 1.1 - i * 0.22)) for i in range(3)])
        computer = chip("MODEL", GREEN, 32).move_to(P(4.3, -0.65))
        self.at("A model combines")
        self.play(LaggedStart(*[FadeIn(l) for l in layers], lag_ratio=0.2), FadeIn(computer), run_time=1.0)
        assumptions = chip("ASSUMPTIONS", GREY, 24).move_to(P(3.1, -1.65))
        arrows = VGroup(*[flow_arrow(P(3.25, 0.6 - i * 0.25), computer.get_left(), GREEN, 3)
                          for i in range(3)])
        self.at("observations and assumptions")
        self.play(FadeIn(assumptions), *[GrowArrow(a) for a in arrows], run_time=0.9)
        flows = VGroup(*[flow_arrow(P(4.0, -1.55 + i * 0.28), P(5.5, -1.55 + i * 0.28), GREEN, 3)
                         for i in range(3)])
        self.at("estimate flows")
        self.play(*[GrowArrow(a) for a in flows], run_time=1.2)
        self.finish()


class S10Limits(FilmScene):
    def construct(self):
        panels = evidence_cards()
        self.add(panels)
        limit = chip("LIMITS", GOLD, 36).move_to(P(0, 3.35))
        self.at("Each kind of evidence")
        self.play(FadeIn(limit), run_time=0.6)
        globe = Circle(radius=1.5, color=GREY, stroke_width=3).move_to(P(-3.25, 0.2))
        globe_lines = VGroup(Arc(radius=1.1, angle=PI, color=GREY).move_to(globe),
                             Line(P(-4.65, 0.2), P(-1.85, 0.2), color=GREY, stroke_width=2))
        station = Dot(P(-3.75, 0.65), radius=0.16, color=ORANGE)
        one = T("ONE STATION", 30, ORANGE).move_to(P(-3.25, -1.65))
        self.at("One station")
        self.play(Create(globe), Create(globe_lines), FadeIn(station), FadeIn(one), run_time=1.0)
        streams = VGroup(*[flow_arrow(P(1.0, 1.6 - i * 0.7), P(4.9, 0.8 - i * 0.3), GREEN, 3,
                                           dashed=(i % 2 == 1)) for i in range(4)])
        est = T("ESTIMATES", 30, GREEN).move_to(P(3.0, -1.5))
        allow(est)  # label belongs to the modeled-stream diagram
        self.at("watershed model estimates")
        self.play(*[Create(s) for s in streams], FadeIn(est), run_time=1.4)
        boundary = RoundedRectangle(corner_radius=0.25, width=3.2, height=3.6, color=GOLD,
                                    stroke_width=4).move_to(P(3.45, 0.25))
        sources = VGroup(*[Dot(P(2.0 + 0.65 * i, 1.2 - 0.55 * (i % 2)), radius=0.16,
                                color=GREEN) for i in range(4)])
        self.at("depends on which sources")
        self.play(FadeIn(sources), Create(boundary), run_time=0.9)
        self.play(boundary.animate.shift(RIGHT * 0.8), run_time=1.3)
        self.finish()


class S10Compare(FilmScene):
    def construct(self):
        panels = evidence_cards()
        self.at("Use each source")
        self.play(FadeIn(panels), run_time=0.8)
        place = chip("SAMPLING PLACE", ORANGE, 30)
        panels.put(place, "left")
        compare = chip("COMPARE SOURCES", GREEN, 30)
        panels.put(compare, "right")
        self.at("measured record shows")
        self.play(FadeIn(place), run_time=0.8)
        self.at("model can compare")
        self.play(FadeIn(compare), run_time=0.8)
        boundaries = chip("BOUNDARIES", GOLD, 25).move_to(P(2.1, -1.55))
        assumptions = chip("ASSUMPTIONS", GREY, 25).move_to(P(4.7, -1.55))
        self.at("boundaries and assumptions")
        self.play(FadeIn(boundaries), FadeIn(assumptions), run_time=0.8)
        evidence = chip("EVIDENCE", TEXT, 38).move_to(P(0, -3.15))
        links = VGroup(Line(panels.left_frame.get_bottom(), evidence.get_top() + LEFT * 0.45,
                            color=ORANGE, stroke_width=4),
                       Line(panels.right_frame.get_bottom(), evidence.get_top() + RIGHT * 0.45,
                            color=GREEN, stroke_width=4))
        self.play(Create(links), FadeIn(evidence), run_time=1.2)
        self.finish()


class S11Connect(FilmScene):
    def construct(self):
        panels = TwoPanel("CARBON", "NITROGEN", colors=(ORANGE, GREEN),
                          top=2.9, bottom=-1.9, width=12.6, size=34)
        self.at("Carbon and nitrogen")
        self.play(FadeIn(panels), run_time=0.8)
        air = meter(P(-3.25, 0.25), ORANGE, 0.5, 2.8)
        air_lab = T("AIR", 24, ORANGE).move_to(P(-3.8, 1.2))
        bay = meter(P(3.25, 0.25), GREEN, 0.5, 2.8)
        bay_lab = T("BAY WATER", 24, GREEN).move_to(P(2.85, 1.3))
        allow(air_lab, bay_lab)
        self.play(FadeIn(air), FadeIn(air_lab), FadeIn(bay), FadeIn(bay_lab), run_time=0.9)
        c_in = flow_arrow(P(-6.0, 0.25), P(-4.7, 0.25), ORANGE, 8)
        c_out = flow_arrow(P(-1.8, 0.25), P(-0.55, 0.25), ORANGE, 5)
        n_in = flow_arrow(P(0.55, 0.25), P(1.8, 0.25), GREEN, 8)
        n_out = flow_arrow(P(4.7, 0.25), P(6.0, 0.25), GREEN, 5)
        runoff = VGroup(T("FIELD", 22, GREEN), T("RUNOFF", 22, GREEN)).arrange(DOWN, buff=0.06).move_to(P(0.93, 1.6))
        allow(runoff)  # label belongs to the green input arrow
        self.play(GrowArrow(c_in), GrowArrow(c_out), GrowArrow(n_in), GrowArrow(n_out), FadeIn(runoff), run_time=1.0)
        tracker = VGroup(*[chip(t, col, 26) for t, col in
                           [("RESERVOIR", BLUE), ("IN VERSUS OUT", GOLD), ("CHANGED PROCESS", RED)]])
        tracker.arrange(RIGHT, buff=0.35).move_to(P(0, -2.85))
        self.at("Identify the reservoir")
        self.play(FadeIn(tracker[0]), run_time=0.6)
        self.at("compare what enters")
        self.play(FadeIn(tracker[1]), run_time=0.6)
        self.at("ask which process")
        self.play(FadeIn(tracker[2]), run_time=0.6)
        dots = VGroup(Dot(P(-5.7, 0.25), color=ORANGE), Dot(P(0.8, 0.25), color=GREEN))
        self.play(FadeIn(dots), dots.animate.shift(RIGHT * 3.0), run_time=1.9, rate_func=linear)
        self.finish()


class S12Rule(FilmScene):
    def construct(self):
        world = watershed(0.35)
        self.add(world)
        carbon = meter(P(-3.3, 0.5), ORANGE, 0.35, 3.2)
        nitrogen = meter(P(3.3, 0.5), GREEN, 0.35, 3.2)
        cin = flow_arrow(P(-6.0, 0.5), P(-5.0, 0.5), ORANGE, 12)
        cout = flow_arrow(P(-1.6, 0.5), P(-0.6, 0.5), ORANGE, 5)
        nin = flow_arrow(P(0.6, 0.5), P(1.6, 0.5), GREEN, 12)
        nout = flow_arrow(P(5.0, 0.5), P(6.0, 0.5), GREEN, 5)
        self.at("When more matter enters")
        self.play(FadeIn(carbon), FadeIn(nitrogen), GrowArrow(cin), GrowArrow(cout), run_time=0.9)
        high_c = Rectangle(width=0.34, height=1.8, stroke_width=0, fill_color=ORANGE, fill_opacity=0.88)
        high_c.move_to(carbon[1].get_bottom() + UP * (0.08 + high_c.height / 2))
        self.play(Transform(carbon[2], high_c), run_time=1.2)
        self.play(GrowArrow(nin), GrowArrow(nout), run_time=0.6)
        high_n = Rectangle(width=0.34, height=1.8, stroke_width=0, fill_color=GREEN, fill_opacity=0.88)
        high_n.move_to(nitrogen[1].get_bottom() + UP * (0.08 + high_n.height / 2))
        self.play(Transform(nitrogen[2], high_n), run_time=1.1)
        self.at("next step is evidence")
        self.play(FadeOut(VGroup(carbon, nitrogen, cin, cout, nin, nout)), run_time=0.6)
        measured = chip("MEASURED", ORANGE, 38).move_to(P(-3.2, 0.2))
        modeled = chip("MODELED", GREEN, 38).move_to(P(3.2, 0.2))
        allow(measured[1], modeled[1])
        self.play(FadeIn(measured), FadeIn(modeled), run_time=0.8)
        self.at("Compare measured records")
        self.play(measured.animate.shift(UP * 0.3), modeled.animate.shift(UP * 0.3), run_time=0.7)
        limits1 = chip("LIMITS", GOLD, 26).next_to(measured, DOWN, buff=0.3)
        limits2 = chip("LIMITS", GOLD, 26).next_to(modeled, DOWN, buff=0.3)
        allow(limits1[1], limits2[1])
        self.at("different limits in view")
        self.play(FadeIn(limits1), FadeIn(limits2), run_time=0.8)
        self.finish()


class S13End(EndCard):
    LINE = "When more matter enters a reservoir than leaves it, the amount rises."
