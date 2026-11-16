"""How a receptor reaches Ras.

COLOR MAP
  BLUE   receptor / input
  GREEN  Grb2 / binding organiser
  ORANGE Sos / enzyme
  PURPLE Ras / output switch
  GOLD   phosphate / GTP highlight
  GREY   membrane / inactive labels

All proteins are schematic labelled cartoons.  No molecular structures are drawn.
"""
from bp_parts import *  # noqa: F401,F403


ORANGE = "#F29E4C"
PURPLE = "#B58CD9"

MEM_Y = 1.65
REC_X = -3.85
RAS_X = 3.75
TAIL_Y = -0.35


def membrane():
    """The one membrane used throughout the film."""
    m = RoundedRectangle(
        corner_radius=0.12, width=12.5, height=0.5,
        stroke_color=GREY, stroke_width=3, fill_color=GREY, fill_opacity=0.24,
    ).move_to([0, MEM_Y, 0])
    return pulse(m, base=3.0, amp=2.2, speed=4.0)


def cell_field():
    """A broad, quiet cell-interior field below the membrane."""
    return Rectangle(width=12.5, height=3.45, stroke_width=0,
                     fill_color=GREY, fill_opacity=0.16).move_to([0, -0.33, 0])


def phosphate_badge(point, scale=1.0):
    ring = Circle(radius=0.27 * scale, color=GOLD, stroke_width=3,
                  fill_color=GOLD, fill_opacity=0.92).move_to(point)
    letter = T("P", size=max(22, 25 * scale), color=BG, weight=BOLD).move_to(ring)
    g = VGroup(ring, letter)
    g.ring = ring
    return g


def receptor(phosphates=0, growth_factor=False):
    """Shared receptor builder; every membrane-world scene calls this."""
    outer = RoundedRectangle(corner_radius=0.22, width=1.9, height=1.15,
                             stroke_color=BLUE, stroke_width=4,
                             fill_color=BLUE, fill_opacity=0.22).move_to([REC_X, 2.42, 0])
    outer_label = T("receptor", 28, BLUE, weight=BOLD).move_to(outer)
    tail = Line([REC_X, 1.62, 0], [REC_X, -1.45, 0], color=BLUE, stroke_width=8)
    ys = [0.55, -0.35, -1.2]
    twigs = VGroup(*[
        Line([REC_X, y, 0], [REC_X + 0.55, y, 0], color=BLUE, stroke_width=6)
        for y in ys
    ])
    tips = VGroup(*[Dot([REC_X + 0.55, y, 0], radius=0.08, color=BLUE) for y in ys])
    g = VGroup(tail, twigs, tips, outer, outer_label)
    g.outer, g.outer_label, g.tail = outer, outer_label, tail
    g.badges = VGroup(*[
        phosphate_badge([REC_X + 0.82, ys[i], 0]) for i in range(phosphates)
    ])
    if phosphates:
        g.add(g.badges)
    g.factor = None
    if growth_factor:
        g.factor = boxed_label("growth factor", BLUE, size=28).move_to([REC_X, 3.35, 0])
        g.add(g.factor)
    return g


def ras(x=RAS_X, state="", nucleotide=None, scale=1.0):
    """Shared membrane-bound Ras cartoon."""
    y = 0.55
    anchor = Line([x, 1.42, 0], [x, 1.03, 0], color=PURPLE, stroke_width=6)
    body = RoundedRectangle(corner_radius=0.28, width=2.15 * scale, height=0.95 * scale,
                            stroke_color=PURPLE, stroke_width=4,
                            fill_color=PURPLE, fill_opacity=0.20).move_to([x, y, 0])
    name = T("Ras" if not state else f"Ras {state}", 30, PURPLE, weight=BOLD).move_to(body)
    g = VGroup(anchor, body, name)
    g.anchor, g.body, g.name = anchor, body, name
    g.tag = None
    if nucleotide:
        col = GOLD if nucleotide == "GTP" else GREY
        g.tag = boxed_label(nucleotide, col, size=26).next_to(body, DOWN, buff=0.48)
        g.add(g.tag)
    return g


def sh2_cup(center=(0, 0, 0), scale=1.0, label=True):
    """A visibly open phosphotyrosine-reading cup."""
    arc = Arc(radius=0.62 * scale, start_angle=55 * DEGREES, angle=250 * DEGREES,
              color=GREEN, stroke_width=12 * scale).rotate(PI).move_to(center)
    g = VGroup(arc)
    if label:
        lab = T("SH2", max(24, 29 * scale), GREEN, weight=BOLD)
        lab.move_to(np.array(center, dtype=float) + UP * 0.98 * scale)
        g.add(lab)
        g.label = lab
    g.arc = pulse(arc, base=12 * scale, amp=2.5, speed=4.0)
    return g


def sh3_grip(center=(0, 0, 0), scale=1.0, label=True):
    lines = VGroup(
        Line([-0.55, 0.36, 0], [0.28, 0.36, 0], color=GREEN, stroke_width=10),
        Line([-0.55, -0.36, 0], [0.28, -0.36, 0], color=GREEN, stroke_width=10),
        Line([-0.55, -0.36, 0], [-0.55, 0.36, 0], color=GREEN, stroke_width=10),
    ).scale(scale).move_to(center)
    pulse(lines, base=10 * scale, amp=2.0, speed=4.0)
    g = VGroup(lines)
    if label:
        lab = T("SH3", max(24, 27 * scale), GREEN, weight=BOLD)
        lab.move_to(np.array(center, dtype=float) + UP * 0.80 * scale)
        g.add(lab)
        g.label = lab
    return g


def grb2_sos(center=(-1.85, -0.45, 0), scale=1.0, with_sos=True,
             activity_tag=False, separate_notch=False):
    """Shared Grb2–Sos builder, rebuilt at an identical scale and place."""
    c = np.array(center, dtype=float)
    backplate = RoundedRectangle(corner_radius=0.35 * scale, width=4.35 * scale,
                                 height=1.30 * scale, stroke_width=0,
                                 fill_color=GREEN, fill_opacity=0.18).move_to(c)
    left = sh3_grip(c + LEFT * 1.35 * scale, 0.82 * scale)
    cup = sh2_cup(c, 0.82 * scale)
    right = sh3_grip(c + RIGHT * 1.35 * scale, 0.82 * scale)
    name = boxed_label("Grb2", GREEN, size=max(24, 29 * scale), pad=0.18).move_to(c + UP * 1.65 * scale)
    adaptor = VGroup(backplate, left, cup, right, name)
    g = VGroup(adaptor)
    g.adaptor, g.name, g.cup, g.grips = adaptor, name, cup, VGroup(left, right)
    g.sos = None
    if with_sos:
        sos = boxed_label("Sos", ORANGE, size=max(24, 31 * scale),
                          box=(2.0 * scale, 0.82 * scale), pad=0.16)
        sos.move_to(c + DOWN * 1.25 * scale)
        if separate_notch:
            notch = Circle(radius=0.16 * scale, color=ORANGE, stroke_width=3,
                           fill_color=BG, fill_opacity=1).move_to(sos.get_right() + LEFT * 0.03)
            sos.add(notch)
            sos.notch = notch
        g.sos = sos
        g.add(sos)
    g.activity = None
    if activity_tag:
        tag = T("no enzyme activity", max(24, 25 * scale), GREY)
        tag.next_to(g, DOWN, buff=0.2)
        g.activity = tag
        g.add(tag)
    return g


def base_world(phosphates=0, factor=False, ras_x=RAS_X, ras_state="", ras_nucleotide=None):
    """The carried membrane world at its canonical scale and position."""
    field = cell_field()
    m = membrane()
    rec = receptor(phosphates=phosphates, growth_factor=factor)
    r = ras(ras_x, ras_state, ras_nucleotide)
    world = VGroup(field, m, rec, r)
    world.field, world.membrane, world.receptor, world.ras = field, m, rec, r
    return world


def predict_picture():
    rec = receptor(phosphates=1)
    rec.shift(LEFT * 0.45 + DOWN * 0.25)
    badge = rec.badges[0]
    cup = sh2_cup([-0.75, 0.9, 0], 1.18)
    grip = sh3_grip([2.2, 0.9, 0], 1.05)
    return VGroup(rec, cup, grip)


def route_cluster(ras_state="ON"):
    world = base_world(phosphates=1, factor=False, ras_x=3.2, ras_state=ras_state,
                       ras_nucleotide="GTP" if ras_state == "ON" else None)
    pair = grb2_sos(center=(-1.6, -0.55, 0), scale=0.84)
    g = VGroup(world, pair)
    g.world, g.pair = world, pair
    return g


class S00Hook(SpokenScene):
    def construct(self):
        world = base_world()
        question = T("?", 72, GOLD, weight=BOLD).move_to([0, 0.3, 0])
        dotted = VGroup(
            DashedLine([-2.8, 0.35, 0], [-0.65, 0.35, 0], color=GREY,
                       stroke_width=4, dash_length=0.12),
            DashedLine([0.65, 0.35, 0], [2.75, 0.35, 0], color=GREY,
                       stroke_width=4, dash_length=0.12),
        )
        schematic = scope_tag()
        self.play(FadeIn(world.field), FadeIn(world.membrane),
                  FadeIn(world.receptor), FadeIn(world.ras), run_time=0.8)
        self.at("without ever touching")
        self.play(Create(dotted), FadeIn(question), run_time=1.0)
        self.at("How does the message")
        self.play(question.animate.scale(1.15), rate_func=there_and_back, run_time=1.3)
        self.at("Watch the blue receptor")
        self.play(Indicate(world.receptor.outer, color=BLUE),
                  Indicate(world.ras.body, color=PURPLE), FadeIn(schematic), run_time=1.4)
        self.at("Both sit at")
        self.play(world.receptor.animate.shift(RIGHT * 0.10),
                  world.ras.animate.shift(LEFT * 0.16), rate_func=there_and_back, run_time=2.1)
        self.finish()


class S01Title(NarratedScene):
    def construct(self):
        world = base_world()
        world.set_opacity(0.34)
        title = fit_text("How a Receptor Reaches Ras", max_w=10.8, size=50,
                         color=TEXT, font=TITLE_FONT).move_to([0, -2.65, 0])
        question = T("?", 72, GOLD, weight=BOLD).move_to([0, 0.3, 0])
        self.add(world, question)
        self.play(ReplacementTransform(question, title), run_time=0.7)
        self.wait(0.55)
        self.play(FadeOut(title), FadeOut(world), run_time=0.55)
        self.finish()


class S02Phosphate(SpokenScene):
    def construct(self):
        world = base_world()
        sos_wait = boxed_label("Sos", ORANGE, size=30).move_to([0.45, -1.85, 0])
        self.add(world)
        factor = boxed_label("growth factor", BLUE, size=28).move_to([0.5, 3.18, 0])
        self.play(FadeIn(factor), factor.animate.move_to([-1.25, 3.18, 0]), run_time=1.4)
        self.at("receptor add phosphate")
        self.play(world.receptor.outer.animate.scale(1.08), rate_func=there_and_back, run_time=0.9)
        badges = VGroup(*[phosphate_badge([REC_X + 0.82, y, 0]) for y in (0.55, -0.35, -1.2)])
        self.play(LaggedStart(*[GrowFromCenter(b) for b in badges], lag_ratio=0.35), run_time=1.7)
        self.at("Each gold mark")
        self.play(LaggedStart(*[Indicate(b, color=GOLD, scale_factor=1.25) for b in badges],
                              lag_ratio=0.25), run_time=1.7)
        self.at("Yet a phosphate")
        stopped = DashedLine([REC_X + 1.2, -0.35, 0], [-0.45, -0.35, 0],
                             color=GOLD, stroke_width=5, dash_length=0.13)
        self.play(FadeIn(sos_wait), Create(stopped), run_time=1.3)
        self.play(badges[1].animate.scale(1.22), rate_func=there_and_back, run_time=1.0)
        self.finish()


class S03Problem(SpokenScene):
    def construct(self):
        world = base_world(phosphates=1)
        outline = RoundedRectangle(corner_radius=0.3, width=2.7, height=1.25,
                                   color=GREEN, stroke_width=4).set_stroke(opacity=0.6)
        outline.move_to([-1.65, -0.55, 0])
        sos_wait = boxed_label("Sos", ORANGE, size=30).move_to([-0.4, -2.15, 0])
        self.add(world)
        self.at("each free to drift")
        self.play(world.receptor.animate.shift(RIGHT * 0.12),
                  world.ras.animate.shift(LEFT * 0.24), rate_func=there_and_back, run_time=2.2)
        self.at("missing part must bind")
        self.play(FadeIn(outline, shift=UP * 0.35), run_time=1.3)
        self.play(outline.animate.shift(LEFT * 0.75 + UP * 0.15), run_time=1.2)
        self.at("It must also carry")
        self.play(FadeIn(sos_wait, shift=UP * 0.25), run_time=0.9)
        self.play(outline.animate.shift(RIGHT * 0.15), sos_wait.animate.shift(UP * 0.15),
                  rate_func=there_and_back, run_time=1.5)
        self.finish()


class S03Grb2(SpokenScene):
    def construct(self):
        pair = grb2_sos(center=(0, 0.45, 0), scale=1.18, with_sos=False)
        pair.activity = T("no enzyme activity", 27, GREY).next_to(pair, DOWN, buff=0.35)
        self.play(FadeIn(pair.adaptor, shift=UP * 0.2), run_time=1.1)
        back = pair.adaptor[0]
        clock = ValueTracker(0)
        clock.add_updater(lambda m, dt: m.increment_value(dt))
        self.add(clock)
        back.add_updater(lambda m: m.set_fill(GREEN, opacity=0.26 + 0.12 * np.sin(clock.get_value() * 3.0)))
        self.at("green adapter with")
        self.play(FadeIn(pair.activity), run_time=0.8)
        self.at("Its central")
        self.play(Indicate(pair.cup, color=GREEN, scale_factor=1.12), run_time=1.1)
        p = phosphate_badge(pair.cup.get_center() + LEFT * 1.7, 1.15)
        self.play(FadeIn(p), p.animate.move_to(pair.cup.get_center()), run_time=1.3)
        self.at("domains are paired")
        self.play(LaggedStart(*[Indicate(x, color=GREEN, scale_factor=1.12) for x in pair.grips],
                              lag_ratio=0.3), run_time=1.4)
        self.at("grips already hold")
        sos = boxed_label("Sos", ORANGE, size=34, box=(2.35, 0.95)).move_to([0, -1.55, 0])
        self.play(FadeIn(sos, shift=UP * 0.35), run_time=1.2)
        self.play(pair.grips.animate.shift(DOWN * 0.12), sos.animate.shift(UP * 0.12),
                  rate_func=there_and_back, run_time=1.3)
        self.finish()


class S04Predict(SpokenScene):
    QUESTION = "Which faces the phosphate: SH2 or SH3?"

    def construct(self):
        picture = predict_picture()
        rec, cup, grip = picture
        card = question_card(self.QUESTION, y=-3.18, size=29)
        self.play(FadeIn(rec), run_time=0.8)
        self.at("the SH2 cup")
        self.play(FadeIn(cup, shift=LEFT * 0.2), run_time=0.8)
        self.at("or an SH3")
        self.play(FadeIn(grip, shift=LEFT * 0.2), FadeIn(card), run_time=0.9)
        self.at("two shapes move")
        self.play(cup.animate.shift(LEFT * 0.45), grip.animate.shift(LEFT * 0.45),
                  rate_func=there_and_back, run_time=2.0)
        self.finish()


class S05Pause(PredictPause):
    QUESTION = S04Predict.QUESTION
    SECONDS = 4.5
    CARD = {"y": -3.18, "size": 29}
    RING_AT = (6.05, -3.15, 0)

    def backdrop(self):
        picture = predict_picture()
        pulse(picture[0].badges[0].ring, base=3.0, amp=1.5, speed=2.2)
        bob(picture[1], amp=0.05, speed=1.8)
        bob(picture[2], amp=0.05, speed=1.8, seed=2)
        return picture


class S06Reveal(SpokenScene):
    def construct(self):
        picture = predict_picture()
        rec, cup, grip = picture
        self.add(picture)
        self.play(FadeOut(grip, shift=RIGHT * 0.4), run_time=0.7)
        self.at("cup closes around")
        badge = rec.badges[0]
        self.play(cup.animate.move_to(badge).scale(1.18), run_time=1.3)
        self.play(Indicate(VGroup(cup, badge), color=GOLD, scale_factor=1.08), run_time=0.9)
        self.at("grips keep holding")
        full = grb2_sos(center=(-1.35, -0.55, 0), scale=0.80)
        self.play(FadeOut(cup), FadeIn(full), run_time=1.2)
        self.at("complete GRB2")
        self.play(full.animate.shift(LEFT * 0.3), run_time=0.7)
        self.play(full.animate.shift(RIGHT * 0.3), run_time=0.7)
        self.at("adapter has connected")
        path1 = VMobject(color=GREEN, stroke_width=7).set_points_as_corners([
            badge.get_left() + LEFT * 0.08,
            [-3.45, -1.72, 0],
            full.adaptor[0].get_left() + LEFT * 0.08,
        ])
        path2 = Line(full.cup.get_bottom() + DOWN * 0.08, full.sos.get_top() + UP * 0.08,
                     color=ORANGE, stroke_width=7)
        self.play(Create(path1), Create(path2), run_time=1.5)
        self.finish()


class S07Exchange(SpokenScene):
    def construct(self):
        cluster = route_cluster(ras_state="OFF")
        world, pair = cluster.world, cluster.pair
        old_gdp = boxed_label("GDP", GREY, size=27).next_to(world.ras.body, DOWN, buff=0.48)
        self.add(world.field, world.membrane, world.receptor, pair, world.ras, old_gdp)
        self.play(world.ras.animate.shift(LEFT * 1.05), run_time=1.4)
        self.at("SOs is a")
        self.play(Indicate(pair.sos, color=ORANGE, scale_factor=1.1), run_time=1.1)
        self.at("It releases GDP")
        self.play(old_gdp.animate.shift(DOWN * 0.75), FadeOut(old_gdp), run_time=1.1)
        self.at("allowing GTP")
        gtp = boxed_label("GTP", GOLD, size=27).next_to(world.ras.body, DOWN, buff=0.48)
        self.play(FadeIn(gtp, shift=UP * 0.45), run_time=1.0)
        self.at("Purple RAS changes")
        on = T("Ras ON", 30, TEXT, weight=BOLD).move_to(world.ras.name)
        self.play(swap(world.ras.name, on), world.ras.body.animate.set_fill(PURPLE, 0.52), run_time=1.2)
        self.at("GRB2 never")
        self.play(Indicate(pair.adaptor, color=GREEN, scale_factor=1.05), run_time=1.1)
        self.play(pair.sos.animate.scale(1.08), rate_func=there_and_back, run_time=1.1)
        self.finish()


class S07Position(SpokenScene):
    def construct(self):
        panels = TwoPanel("BEFORE", "AFTER")
        left_pair = grb2_sos(center=(-3.25, -0.55, 0), scale=0.75)
        right_mem = RoundedRectangle(corner_radius=0.08, width=5.2, height=0.34,
                                     color=GREY, stroke_width=2, fill_color=GREY,
                                     fill_opacity=0.25).move_to([3.25, 1.45, 0])
        rec_box = boxed_label("receptor", BLUE, size=24, box=(1.75, 0.72)).move_to([2.05, 1.95, 0])
        rec_tail = Line([2.05, 1.59, 0], [2.05, 0.2, 0], color=BLUE, stroke_width=6)
        rec_p = phosphate_badge([2.34, 0.32, 0])
        right_rec = VGroup(rec_tail, rec_box, rec_p)
        right_pair = grb2_sos(center=(3.35, -0.72, 0), scale=0.75)
        right_ras = ras(5.2, scale=0.82)
        pin = VGroup(Circle(radius=0.18, color=GOLD, fill_color=GOLD, fill_opacity=0.8),
                     Triangle(color=GOLD, fill_color=GOLD, fill_opacity=0.8).scale(0.16).rotate(PI))
        pin.arrange(DOWN, buff=-0.05).next_to(left_pair.sos, DOWN, buff=0.12)
        self.play(FadeIn(panels), FadeIn(left_pair), FadeIn(pin), run_time=1.0)
        self.at("not chemical identity")
        self.play(Indicate(left_pair.sos, color=ORANGE, scale_factor=1.08), run_time=1.1)
        self.at("already attached")
        self.play(left_pair.animate.shift(UP * 0.15), rate_func=there_and_back, run_time=1.1)
        self.at("After the")
        self.play(FadeIn(right_mem), FadeIn(right_rec), run_time=0.9)
        self.at("same SOES sits")
        right_pin = pin.copy().next_to(right_pair.sos, RIGHT, buff=0.08)
        self.play(FadeIn(right_pair, shift=RIGHT * 0.25),
                  FadeIn(right_pin, shift=RIGHT * 0.25), run_time=1.4)
        self.at("where it can meet")
        self.play(FadeIn(right_ras), right_ras.animate.shift(LEFT * 0.25), run_time=1.0)
        self.at("Positioning has become")
        rule = caption("Recruitment changes location", size=30, color=GOLD)
        self.play(FadeIn(rule), run_time=0.9)
        self.finish()


class S07Feedback(SpokenScene):
    def construct(self):
        sos = boxed_label("Sos", ORANGE, size=38, box=(3.2, 2.5)).move_to([0, 0.25, 0])
        exchange = Circle(radius=0.28, color=ORANGE, stroke_width=5).move_to([-1.25, 0.25, 0])
        allosteric = Circle(radius=0.28, color=ORANGE, stroke_width=5).move_to([1.25, 0.75, 0])
        exchange_lab = T("exchange site", 27, ORANGE).move_to([-1.8, 2.15, 0])
        second_lab = T("Ras-binding site", 27, PURPLE).move_to([1.55, 2.15, 0])
        self.add(sos, exchange, exchange_lab)
        self.at("another RAS binding")
        self.play(Create(allosteric), FadeIn(second_lab), run_time=1.1)
        self.at("away from the")
        self.play(Indicate(VGroup(exchange, allosteric), color=GOLD, scale_factor=1.06), run_time=1.1)
        self.at("RAS with GTP")
        activator = boxed_label("Ras–GTP", PURPLE, size=29).move_to([4.65, 0.75, 0])
        self.play(FadeIn(activator), activator.animate.move_to([2.8, 0.75, 0]), run_time=1.3)
        self.at("speed SOES")
        neighbor = ras(-4.45, state="", nucleotide="GDP", scale=0.88)
        neighbor.anchor.set_opacity(0)
        self.play(FadeIn(neighbor), run_time=0.7)
        flash = Arrow(exchange.get_left(), neighbor.body.get_right(), buff=0.12,
                      color=GOLD, stroke_width=7, tip_length=0.22)
        tag = scope_tag()
        self.play(GrowArrow(flash), FadeIn(tag), run_time=0.7)
        self.play(flash.animate.set_stroke(width=12), rate_func=there_and_back, run_time=1.2)
        self.at("help SOES activate")
        more = VGroup(*[Dot([-4.7 + i * 0.55, -1.65, 0], radius=0.14, color=PURPLE) for i in range(4)])
        self.play(LaggedStart(*[GrowFromCenter(d) for d in more], lag_ratio=0.22), run_time=1.3)
        self.finish()


class S08Route(SpokenScene):
    def construct(self):
        cluster = route_cluster()
        world, pair = cluster.world, cluster.pair
        self.add(cluster)
        self.at("follow the route")
        self.play(Indicate(world.receptor.outer, color=BLUE, scale_factor=1.08), run_time=1.0)
        self.at("receptor recruits")
        self.play(Indicate(pair.adaptor, color=GREEN, scale_factor=1.08), run_time=1.0)
        self.at("GRB2 brings")
        self.play(Indicate(pair.sos, color=ORANGE, scale_factor=1.1), run_time=1.0)
        self.at("where RAS sits")
        self.play(world.ras.animate.shift(LEFT * 0.35), rate_func=there_and_back, run_time=1.0)
        self.at("performs the exchange")
        flash = Line(pair.sos.get_right(), world.ras.body.get_left(), color=GOLD, stroke_width=9)
        self.play(Create(flash), Indicate(world.ras.body, color=PURPLE), run_time=1.0)
        self.at("Binding controls")
        bind_label = boxed_label("binding", GREEN, size=27).move_to([-0.2, 2.75, 0])
        self.play(FadeIn(bind_label), run_time=0.7)
        self.at("while SOs performs")
        work_label = boxed_label("chemical work", ORANGE, size=27).move_to([2.5, -1.8, 0])
        self.play(FadeOut(bind_label), FadeIn(work_label),
                  flash.animate.set_stroke(width=13), rate_func=there_and_back, run_time=1.3)
        self.finish()


class S09Payoff(SpokenScene):
    def construct(self):
        cluster = route_cluster()
        world, pair = cluster.world, cluster.pair
        # Only the three requested labels remain.
        for obj in (world.receptor.outer_label, pair.name, pair.sos.label, world.ras.name,
                    world.ras.tag.label if world.ras.tag else VGroup()):
            obj.set_opacity(0)
        adaptor_lab = T("adaptor", 28, GREEN).move_to(pair.name)
        enzyme_lab = T("enzyme", 28, ORANGE).move_to(pair.sos)
        ras_lab = T("Ras ON", 28, PURPLE).move_to(world.ras.body)
        self.add(cluster, adaptor_lab, enzyme_lab, ras_lab)
        self.at("but the receptor")
        self.play(world.receptor.animate.shift(RIGHT * 0.10),
                  world.ras.animate.shift(LEFT * 0.20), rate_func=there_and_back, run_time=1.8)
        self.at("adapter changes")
        self.play(Indicate(pair.adaptor, color=GREEN, scale_factor=1.07), run_time=1.1)
        self.at("who meets whom")
        pulse1 = VMobject(color=GREEN, stroke_width=8).set_points_as_corners([
            world.receptor.badges[0].get_left() + LEFT * 0.08,
            [-3.45, -1.72, 0],
            pair.adaptor[0].get_left() + LEFT * 0.08,
        ])
        pulse2 = Line(pair.sos.get_right() + RIGHT * 0.08,
                      world.ras.body.get_left() + LEFT * 0.08,
                      color=ORANGE, stroke_width=8)
        self.play(Create(pulse1), Create(pulse2), run_time=1.3)
        self.at("right enzyme reach")
        self.play(Indicate(pair.sos, color=ORANGE, scale_factor=1.1),
                  Indicate(world.ras.body, color=PURPLE, scale_factor=1.08), run_time=1.2)
        self.at("without the adapter")
        self.play(pair.adaptor.animate.scale(1.04), rate_func=there_and_back, run_time=1.3)
        self.finish()


class S10End(EndCard):
    LINE = "Adaptors route signals by linking partners, not by catalyzing reactions."
