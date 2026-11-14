"""Four Ways a Population Changes.

Colour map used throughout:
BLUE = crabs and additions; RED = losses; TEAL = cold/nonliving factors;
GREEN = shelter; YELLOW = harvest/people; GREY = Bay structure and estimates.
All dots and arrows in the population window are explicitly schematic.
"""
from bp_parts import *


CRAB = BLUE
ADD = BLUE
LOSS = RED
SHELTER = GREEN
COLD = TEAL
HARVEST = YELLOW

DOT_POSITIONS = [
    (-2.20, 0.95), (-1.25, 1.25), (-0.20, 1.05), (0.95, 1.35), (2.05, 0.85),
    (-2.45, 0.00), (-1.45, 0.25), (-0.35, -0.05), (0.80, 0.25), (2.25, -0.10),
    (-1.85, -0.90), (-0.75, -1.15), (0.35, -0.85), (1.45, -1.10),
]


def crab_dot(radius=0.15, color=CRAB):
    """A schematic crab mark, intentionally a dot rather than an anatomical drawing."""
    return Dot(radius=radius, color=color, stroke_color=TEXT, stroke_width=1.5)


def moving_water(width=12.0, center_y=0.0, rows=7, color=BLUE):
    """A field of gently moving water strokes that keeps the Bay world alive."""
    g = VGroup()
    for j in range(rows):
        y = center_y + (j - (rows - 1) / 2) * 0.48
        row = VGroup()
        for i in range(9):
            x = -width / 2 + 0.45 + i * (width - 0.9) / 8
            row.add(ArcBetweenPoints([x - 0.32, y, 0], [x + 0.32, y, 0], angle=-0.22,
                                     color=color, stroke_width=2).set_opacity(0.25))
        row._water_t = 0.0
        base = row.get_center().copy()

        def drift(mob, dt, base=base, phase=j * 0.7):
            mob._water_t += dt
            mob.move_to(base + RIGHT * 0.28 * np.sin(0.7 * mob._water_t + phase)
                        + UP * 0.06 * np.sin(1.1 * mob._water_t + phase))
        row.add_updater(drift)
        g.add(row)
    return g


def flow_arrow(start, end, color, width=7):
    a = Arrow(start, end, buff=0.04, color=color, stroke_width=width, tip_length=0.26,
              max_tip_length_to_length_ratio=0.35, max_stroke_width_to_length_ratio=12)
    return a


def flow_motes(start, end, color, count=3):
    """Dots circulating along a flow arrow, providing meaningful continuous motion."""
    a, b = np.array(start, dtype=float), np.array(end, dtype=float)
    g = VGroup(*[Dot(radius=0.07, color=color) for _ in range(count)])
    g._flow_t = 0.0

    def travel(mob, dt):
        mob._flow_t += dt
        for i, d in enumerate(mob):
            f = (0.28 * mob._flow_t + i / count) % 1.0
            d.move_to(a + f * (b - a))
    g.add_updater(travel)
    return g


def shimmer_fill(mob, color, base, amp=0.035, speed=1.6, phase=0.0):
    """Slow opacity shimmer for water or a live estimate; geometry stays fixed."""
    mob._shimmer_t = phase

    def shimmer(m, dt):
        m._shimmer_t += dt
        m.set_fill(color, opacity=base + amp * np.sin(speed * m._shimmer_t))
    return mob.add_updater(shimmer)


def bay_window(dot_count=10, add_width=7, loss_width=7, labels=True, question=False,
               factor=None, small=False):
    """The carried population picture; all continuing scenes call this exact builder."""
    scale = 0.82 if small else 1.0
    frame = RoundedRectangle(corner_radius=0.65, width=7.0 * scale, height=4.65 * scale,
                             stroke_color=GREY, stroke_width=5, fill_color=BLUE,
                             fill_opacity=0.14).move_to([0, 0.15, 0])
    shimmer_fill(frame, BLUE, 0.14, amp=0.045, speed=1.7)
    water = moving_water(5.8 * scale, center_y=0.15, rows=5 if small else 6).scale(scale)
    water.move_to(frame)
    dots = VGroup(*[crab_dot(0.13 * scale).move_to([x * scale, 0.15 + y * scale, 0])
                    for x, y in DOT_POSITIONS[:dot_count]])
    for i, d in enumerate(dots):
        bob(d, amp=0.11 * scale, speed=1.25 + 0.08 * (i % 4), seed=i)
    left_x = frame.get_left()[0]
    right_x = frame.get_right()[0]
    add = flow_arrow([left_x - 2.0 * scale, 0.15, 0], [left_x - 0.08, 0.15, 0], ADD, add_width)
    loss = flow_arrow([right_x + 0.08, 0.15, 0], [right_x + 2.0 * scale, 0.15, 0], LOSS, loss_width)
    pulse(add, base=add_width, amp=1.0, speed=1.5)
    pulse(loss, base=loss_width, amp=1.0, speed=1.7)
    add_motes = flow_motes([left_x - 2.0 * scale, 0.15, 0], [left_x - 0.08, 0.15, 0], ADD)
    loss_motes = flow_motes([right_x + 0.08, 0.15, 0], [right_x + 2.0 * scale, 0.15, 0], LOSS)
    g = VGroup(frame, water, dots, add, loss, add_motes, loss_motes)
    g.frame, g.water, g.dots, g.add_arrow, g.loss_arrow = frame, water, dots, add, loss
    if labels:
        al = T("additions", 30, ADD, weight=BOLD).next_to(add, UP, buff=0.18)
        ll = T("losses", 30, LOSS, weight=BOLD).next_to(loss, UP, buff=0.18)
        g.add(al, ll)
        g.add_label, g.loss_label = al, ll
    if factor:
        g.add(factor)
    if question:
        q = question_card("Which way will the population move?", size=30, max_w=9.6)
        g.add(q)
        g.question = q
    return g


def survey_bars(show_double=True):
    """Survey bars computed directly from 367 and 852 million."""
    base, max_h = -2.25, 4.65
    h1, h2 = max_h * 367 / 852, max_h
    axis = Line([-4.6, base, 0], [4.6, base, 0], color=GREY, stroke_width=4)
    b1 = Rectangle(width=2.25, height=h1, stroke_color=BLUE, stroke_width=4,
                   fill_color=BLUE, fill_opacity=0.35).move_to([-2.35, base + h1 / 2, 0])
    b2 = Rectangle(width=2.25, height=h2, stroke_color=BLUE, stroke_width=4,
                   fill_color=BLUE, fill_opacity=0.58).move_to([2.35, base + h2 / 2, 0])
    shimmer_fill(b1, BLUE, 0.35, amp=0.055, speed=1.5)
    shimmer_fill(b2, BLUE, 0.58, amp=0.055, speed=1.7, phase=0.8)
    n1 = M("367 million", 34, TEXT).next_to(b1, UP, buff=0.14)
    n2 = M("852 million", 34, TEXT).next_to(b2, UP, buff=0.14)
    w1 = T("winter 1991–1992", 26, GREY).next_to(b1, DOWN, buff=0.14)
    w2 = T("winter 1992–1993", 26, GREY).next_to(b2, DOWN, buff=0.14)
    est = T("ESTIMATES", 30, GREY, weight=BOLD).move_to([0, 3.35, 0])
    g = VGroup(axis, b1, b2, n1, n2, w1, w2, est)
    g.axis, g.b1, g.b2, g.n1, g.n2, g.w1, g.w2, g.est = axis, b1, b2, n1, n2, w1, w2, est
    if show_double:
        y = base + 2 * h1
        double = DashedLine([-4.25, y, 0], [4.25, y, 0], color=YELLOW,
                            stroke_width=4, dash_length=0.16)
        dl = M("twice 367\n= 734 million", 22, YELLOW, line_spacing=0.8).move_to([-0.2, y + 0.05, 0])
        g.add(double, dl)
        g.double, g.double_label = double, dl
    return g


def factor_icon(kind, at, size=1.0):
    """Simple labelled lesson icons; no molecular or anatomical detail."""
    if kind == "cold":
        bulb = Circle(radius=0.18 * size, color=COLD, fill_color=COLD, fill_opacity=0.55)
        stem = Line(UP * 0.65 * size, DOWN * 0.05 * size, color=COLD, stroke_width=8)
        icon = VGroup(stem, bulb.move_to(DOWN * 0.22 * size))
        lab, col = "cold", COLD
    elif kind == "shelter":
        blades = VGroup(*[ArcBetweenPoints([x, -0.42, 0], [x + dx, 0.45, 0], angle=0.25,
                                          color=SHELTER, stroke_width=6)
                          for x, dx in [(-0.45, 0.28), (-0.15, -0.22), (0.15, 0.20), (0.42, -0.26)]])
        icon, lab, col = blades, "shelter", SHELTER
    elif kind == "predators":
        icon = crab_dot(0.38 * size, LOSS)
        lab, col = "predators", LOSS
    else:
        pot = RoundedRectangle(corner_radius=0.12, width=1.05 * size, height=0.72 * size,
                               stroke_color=HARVEST, stroke_width=4)
        slats = VGroup(*[Line([x, -0.32 * size, 0], [x, 0.32 * size, 0], color=HARVEST, stroke_width=2)
                         for x in (-0.28 * size, 0, 0.28 * size)])
        icon, lab, col = VGroup(pot, slats), "harvest", HARVEST
    label = T(lab, 28, col).next_to(icon, DOWN, buff=0.14)
    return VGroup(icon, label).move_to(at)


class S00Hook(SpokenScene):
    def construct(self):
        water = Rectangle(width=13.0, height=4.35, stroke_width=0, fill_color=BLUE,
                          fill_opacity=0.08).move_to([0, 0.20, 0])
        waves = moving_water(12.0, center_y=0.45, rows=8)
        mud = Rectangle(width=13.0, height=1.05, stroke_color=GREY, stroke_width=2,
                        fill_color=GREY, fill_opacity=0.25).move_to([0, -2.48, 0])
        shore = VGroup(
            ArcBetweenPoints([-6.2, 2.35, 0], [-4.2, 2.0, 0], angle=-0.25, color=GREY),
            ArcBetweenPoints([4.2, 2.0, 0], [6.2, 2.35, 0], angle=0.25, color=GREY),
        ).set_stroke(width=6)
        crabs = VGroup(*[crab_dot(0.14).move_to([x, -2.30 + 0.08 * (i % 2), 0])
                         for i, x in enumerate((-4.7, -3.2, -1.8, -0.3, 1.2, 2.7, 4.3))])
        for i, d in enumerate(crabs):
            bob(d, amp=0.035, speed=1.2, seed=i)
        question = fit_text("How can the crab estimate jump when the Bay has not grown?",
                            max_w=11.8, size=40, font=TITLE_FONT).move_to([0, 3.25, 0])
        boat = VGroup(
            Polygon([-0.9, -0.05, 0], [0.9, -0.05, 0], [0.55, -0.42, 0], [-0.65, -0.42, 0],
                    color=GREY, fill_color=GREY, fill_opacity=0.45),
            Rectangle(width=0.72, height=0.40, color=GREY, fill_color=GREY,
                      fill_opacity=0.32).move_to([0.05, 0.16, 0]),
        ).move_to([-5.0, 1.65, 0])
        dredge = Rectangle(width=0.75, height=0.42, color=TEXT, stroke_width=3,
                           fill_color=TEXT, fill_opacity=0.18).move_to([-4.0, -1.95, 0])
        tow = always_redraw(lambda: Line(boat.get_bottom(), dredge.get_top(), color=GREY, stroke_width=4))

        self.play(FadeIn(water), FadeIn(waves), FadeIn(mud), Create(shore), Write(question), run_time=1.5)
        self.at("Watch a survey boat")
        self.play(FadeIn(boat, shift=RIGHT * 0.2), FadeIn(dredge), FadeIn(tow), run_time=0.8)
        self.play(boat.animate.shift(RIGHT * 5.8), dredge.animate.shift(RIGHT * 5.8),
                  run_time=3.6, rate_func=linear)
        self.at("Its dredge catches")
        caught = crabs[:3].copy().arrange(RIGHT, buff=0.12).scale(0.75).move_to(dredge)
        self.play(FadeIn(crabs), FadeIn(caught, scale=0.5), run_time=1.2)
        self.at("Those catches become")
        rings = VGroup(*[Circle(radius=0.28, color=YELLOW, stroke_width=4).move_to(p)
                         for p in [(-4.7, -0.45, 0), (-2.4, 0.65, 0), (0.0, -0.5, 0),
                                   (2.2, 0.65, 0), (4.55, -0.35, 0)]])
        self.play(LaggedStart(*[Create(r) for r in rings], lag_ratio=0.14), run_time=1.6)
        estimate = chip("Bay-wide estimate", YELLOW, size=36).move_to([0, 2.85, 0])
        self.play(FadeOut(question), ReplacementTransform(rings, estimate), run_time=1.2)
        self.at("A moving estimate")
        self.play(estimate.animate.shift(UP * 0.35), shore.animate.set_stroke(opacity=0.45),
                  run_time=1.4, rate_func=there_and_back)
        self.finish()


class S01Title(TitleCard):
    LESSON = "Populations rise and fall"
    TITLE = "Four Ways a Population Changes"


class S02Estimates(SpokenScene):
    def construct(self):
        g = survey_bars(show_double=False)
        self.at("The earlier estimate")
        self.play(Create(g.axis), FadeIn(g.b1, shift=UP * 0.2), FadeIn(g.n1), FadeIn(g.w1), run_time=1.3)
        self.at("The next estimate")
        self.play(FadeIn(g.b2, shift=UP * 0.2), FadeIn(g.n2), FadeIn(g.w2), run_time=1.4)
        self.at("These are estimates")
        self.play(FadeIn(g.est, shift=DOWN * 0.15), run_time=0.8)
        y = -2.25 + 2 * (4.65 * 367 / 852)
        double = DashedLine([-4.25, y, 0], [4.25, y, 0], color=YELLOW,
                            stroke_width=4, dash_length=0.16)
        dl = M("twice 367\n= 734 million", 22, YELLOW, line_spacing=0.8).move_to([-0.2, y + 0.05, 0])
        self.at("The survey pattern")
        self.play(Create(double), FadeIn(dl), run_time=1.2)
        unknown = T("cause: ?", 32, YELLOW, weight=BOLD).move_to([-4.9, 2.55, 0])
        self.play(FadeIn(unknown), run_time=0.8)
        self.at("So read height")
        self.play(Indicate(VGroup(g.b1, g.b2), color=TEXT, scale_factor=1.02),
                  FadeOut(unknown), run_time=1.5)
        self.finish()


class S03Population(SpokenScene):
    def construct(self):
        world = bay_window(dot_count=12, labels=False)
        world.remove(world.add_arrow, world.loss_arrow)
        heading = T("blue crab population", 38, TEXT, weight=BOLD).move_to([0, 3.25, 0])
        rule = T("same species, same place", 30, BLUE).move_to([0, 2.72, 0])
        self.at("To explain the change")
        self.play(FadeIn(world.frame, scale=0.96), FadeIn(world.water), run_time=1.2)
        self.at("A population is")
        self.play(FadeIn(world.dots, lag_ratio=0.06), run_time=1.4)
        self.play(FadeIn(heading, shift=DOWN * 0.12), run_time=0.8)
        self.at("same species")
        self.play(FadeIn(rule), run_time=0.9)
        self.at("Put the bays crabs")
        self.play(Indicate(world.dots, color=BLUE, scale_factor=1.04), run_time=1.2)
        self.at("Now track what enters")
        left = flow_arrow([-5.7, 0.15, 0], [-3.58, 0.15, 0], ADD, 7)
        right = flow_arrow([3.58, 0.15, 0], [5.7, 0.15, 0], LOSS, 7)
        self.play(GrowArrow(left), GrowArrow(right), run_time=1.5)
        self.at("The boundary matters")
        pulse(world.frame, base=5, amp=2.2, speed=2.0)
        self.play(Indicate(world.frame, color=YELLOW, scale_factor=1.015), run_time=1.4)
        self.finish()


class S04AdditionsLosses(SpokenScene):
    def construct(self):
        world = bay_window(dot_count=8, labels=False)
        births = T("births", 29, ADD).move_to([-5.15, 1.25, 0])
        arrivals = T("arrivals", 29, ADD).move_to([-5.15, -0.95, 0])
        deaths = T("deaths", 29, LOSS).move_to([5.15, 1.25, 0])
        departures = T("departures", 29, LOSS).move_to([5.15, -0.95, 0])
        self.add(world.frame, world.water, world.dots)
        self.at("Births add")
        born = VGroup(*[crab_dot(0.13).move_to(p) for p in [(-0.8, 0.55, 0), (0.2, -0.55, 0)]])
        self.play(FadeIn(births), GrowArrow(world.add_arrow), FadeIn(born, scale=0.4), run_time=1.3)
        self.at("Arrivals add")
        incoming = VGroup(*[crab_dot(0.13).move_to([-5.2 - 0.45 * i, -0.4, 0]) for i in range(2)])
        self.play(FadeIn(arrivals), incoming.animate.shift(RIGHT * 3.1), run_time=1.4)
        self.at("Deaths remove")
        self.play(FadeIn(deaths), GrowArrow(world.loss_arrow), FadeOut(world.dots[-2:]), run_time=1.2)
        self.at("Departures remove")
        leaving = world.dots[-4:-2].copy()
        self.play(FadeIn(departures), leaving.animate.shift(RIGHT * 5.0), run_time=1.4)
        self.at("Call births and arrivals")
        addlab = T("ADDITIONS", 34, ADD, weight=BOLD).move_to([-5.15, 1.05, 0])
        self.play(FadeOut(births), FadeOut(arrivals), FadeIn(addlab), run_time=1.1)
        self.at("Call deaths and departures")
        losslab = T("LOSSES", 34, LOSS, weight=BOLD).move_to([5.15, 1.05, 0])
        self.play(FadeOut(deaths), FadeOut(departures), FadeIn(losslab), run_time=1.1)
        self.at("Population change is")
        balance = caption("population change = additions − losses", size=33)
        self.play(FadeIn(balance, shift=UP * 0.1), run_time=1.2)
        self.at("Additions and losses can")
        self.play(Indicate(world.add_arrow, color=ADD), Indicate(world.loss_arrow, color=LOSS),
                  run_time=2.0)
        self.finish()


class S05Predict(SpokenScene):
    def construct(self):
        world = bay_window(dot_count=10, labels=True)
        self.add(world)
        pulse(world.frame, base=5, amp=2.5, speed=1.3)
        tag = scope_tag("schematic")
        self.at("Imagine the loss arrows")
        wider = flow_arrow([3.58, 0.15, 0], [5.72, 0.15, 0], LOSS, 15)
        pulse(wider, base=15, amp=2.0, speed=1.4)
        self.play(ReplacementTransform(world.loss_arrow, wider), run_time=2.8)
        self.at("What should happen")
        q = question_card("Which way will the population move?", size=30, max_w=9.6)
        self.play(FadeIn(q), FadeIn(tag), run_time=1.2)
        self.at("Follow the arrows")
        self.play(Indicate(VGroup(world.add_arrow, wider), color=YELLOW, scale_factor=1.02), run_time=1.6)
        self.at("Watch the balance")
        self.play(Circumscribe(VGroup(world.add_arrow, wider), color=YELLOW, time_width=0.8), run_time=1.6)
        self.finish()


class S06Pause(PredictPause):
    QUESTION = "Which way will the population move?"
    SECONDS = 4.5

    def backdrop(self):
        return bay_window(dot_count=10, add_width=7, loss_width=15, labels=True)


class S07Reveal(SpokenScene):
    def construct(self):
        world = bay_window(dot_count=12, add_width=7, loss_width=15, labels=True)
        tag = scope_tag("schematic")
        self.add(world, tag)
        self.at("The number falls")
        self.play(LaggedStart(*[FadeOut(d, shift=RIGHT * 0.5) for d in world.dots[-6:]], lag_ratio=0.10),
                  run_time=2.2)
        fall = T("falls", 38, LOSS, weight=BOLD).move_to([0, 2.8, 0])
        self.play(FadeIn(fall), run_time=0.7)
        self.at("Reverse the balance")
        blue = flow_arrow([-5.72, 0.15, 0], [-3.58, 0.15, 0], ADD, 15)
        red = flow_arrow([3.58, 0.15, 0], [5.72, 0.15, 0], LOSS, 7)
        pulse(blue, base=15, amp=2, speed=1.5)
        pulse(red, base=7, amp=1, speed=1.7)
        rise = T("rises", 38, ADD, weight=BOLD).move_to(fall)
        self.play(ReplacementTransform(world.add_arrow, blue), ReplacementTransform(world.loss_arrow, red),
                  swap(fall, rise), run_time=1.5)
        newdots = VGroup(*[crab_dot(0.13).move_to([x, 0.15 + y, 0]) for x, y in DOT_POSITIONS[8:14]])
        self.play(LaggedStart(*[FadeIn(d, shift=RIGHT * 0.4) for d in newdots], lag_ratio=0.10), run_time=2.0)
        self.at("Match the arrows")
        blue2 = flow_arrow([-5.72, 0.15, 0], [-3.58, 0.15, 0], ADD, 10)
        red2 = flow_arrow([3.58, 0.15, 0], [5.72, 0.15, 0], LOSS, 10)
        pulse(blue2, base=10, amp=1, speed=1.5)
        pulse(red2, base=10, amp=1, speed=1.7)
        steady = T("steady", 38, TEXT, weight=BOLD).move_to([0, 2.8, 0])
        self.play(ReplacementTransform(blue, blue2), ReplacementTransform(red, red2),
                  FadeOut(rise), FadeIn(steady), run_time=1.5)
        self.at("This gives the rule")
        rule = fit_text("Populations rise when additions exceed losses, and fall when losses exceed additions.",
                        max_w=11.5, size=34, color=TEXT, max_lines=2).move_to([0, -3.05, 0])
        self.play(FadeIn(rule, shift=UP * 0.1), run_time=1.4)
        self.at("Populations rise")
        self.play(Indicate(blue2, color=ADD), run_time=1.1)
        self.at("and fall when")
        self.play(Indicate(red2, color=LOSS), run_time=1.1)
        self.at("The dots show direction")
        direction = scope_tag("direction, not forecast")
        self.play(FadeOut(steady), swap(tag, direction), run_time=1.1)
        self.finish()


class S08LimitingFactor(SpokenScene):
    def construct(self):
        world = bay_window(dot_count=10, labels=True)
        self.add(world)
        pulse(world.frame, base=5, amp=2.5, speed=1.3)
        heading = T("limiting factor", 38, TEXT, weight=BOLD).move_to([0, 3.25, 0])
        self.at("A limiting factor")
        self.play(FadeIn(heading), FadeOut(world.water), FadeOut(world.dots),
                  Indicate(VGroup(world.add_arrow, world.loss_arrow), color=YELLOW), run_time=1.4)
        self.at("A very cold winter")
        cold = factor_icon("cold", [0, 0.45, 0], 1.1)
        bob(cold, amp=0.14, speed=1.15, seed=1)
        self.play(FadeIn(cold, shift=DOWN * 0.15), run_time=1.0)
        thick = flow_arrow([3.58, 0.15, 0], [5.72, 0.15, 0], LOSS, 14)
        self.play(ReplacementTransform(world.loss_arrow, thick), run_time=1.4)
        self.at("Better shelter")
        grass = factor_icon("shelter", [0, 0.45, 0], 1.1)
        bob(grass, amp=0.14, speed=1.25, seed=2)
        narrow = flow_arrow([3.58, 0.15, 0], [5.72, 0.15, 0], LOSS, 5)
        self.play(FadeOut(cold), FadeIn(grass), ReplacementTransform(thick, narrow), run_time=1.5)
        young = VGroup(*[crab_dot(0.11).move_to([-1.0 + 0.45 * i, -0.7, 0]) for i in range(4)])
        self.play(FadeIn(young, lag_ratio=0.12), run_time=0.9)
        self.at("Heavy harvest")
        pot = factor_icon("harvest", [0, 0.45, 0], 1.0)
        bob(pot, amp=0.14, speed=1.35, seed=3)
        heavy = flow_arrow([3.58, 0.15, 0], [5.72, 0.15, 0], LOSS, 14)
        self.play(FadeOut(grass), FadeOut(young), FadeIn(pot), ReplacementTransform(narrow, heavy), run_time=1.5)
        self.at("Each factor matters")
        tag = scope_tag("schematic")
        self.play(FadeIn(tag), Indicate(VGroup(world.add_arrow, heavy), color=YELLOW), run_time=1.4)
        self.at("Different factors")
        trio = VGroup(factor_icon("cold", [-2.0, 0.65, 0], 0.8),
                      factor_icon("shelter", [0, 0.65, 0], 0.8),
                      factor_icon("harvest", [2.0, 0.65, 0], 0.8))
        self.play(FadeOut(pot), FadeIn(trio, lag_ratio=0.15), run_time=1.7)
        self.finish()


class S09Scope(SpokenScene):
    def construct(self):
        world = bay_window(dot_count=9, labels=False, small=True)
        world.shift(DOWN * 0.15)
        self.add(world)
        self.at("The balance tells")
        self.play(Indicate(VGroup(world.add_arrow, world.loss_arrow), color=YELLOW), run_time=1.5)
        self.at("It cannot identify")
        unknown = T("cause?", 38, YELLOW, weight=BOLD).move_to([0, 2.75, 0])
        self.play(FadeIn(unknown), run_time=1.0)
        self.at("Scientists need measurements")
        icons = VGroup(factor_icon("cold", [-4.9, 1.8, 0], 0.8),
                       factor_icon("shelter", [-4.9, -1.35, 0], 0.8),
                       factor_icon("predators", [5.2, 1.8, 0], 0.8),
                       factor_icon("harvest", [5.2, -1.35, 0], 0.8))
        self.play(LaggedStart(*[FadeIn(i, scale=0.9) for i in icons], lag_ratio=0.15), run_time=2.2)
        bracket = BraceBetweenPoints([-4.15, 2.65, 0], [-4.15, -2.25, 0], direction=RIGHT, color=TEXT)
        measure = T("measure\neach factor", 28, TEXT, line_spacing=0.85).move_to([-5.75, 0.2, 0])
        self.play(FadeIn(bracket), FadeIn(measure), run_time=1.1)
        self.at("The survey gives")
        pattern = chip("survey pattern", BLUE, size=28).move_to([0, -2.3, 0])
        self.play(FadeIn(pattern), run_time=1.0)
        self.at("Evidence about the arrows")
        links = VGroup(
            flow_arrow([-4.15, 1.8, 0], [-3.1, 0.9, 0], COLD, 4),
            flow_arrow([-4.15, -1.35, 0], [-3.1, -0.55, 0], SHELTER, 4),
            flow_arrow([4.45, 1.8, 0], [3.1, 0.9, 0], LOSS, 4),
            flow_arrow([4.45, -1.35, 0], [3.1, -0.55, 0], HARVEST, 4),
        )
        self.play(LaggedStart(*[GrowArrow(a) for a in links], lag_ratio=0.12), run_time=1.8)
        self.at("That extra evidence")
        tested = caption("pattern + evidence → tested cause", size=32)
        self.play(FadeOut(pattern), FadeIn(tested), FadeOut(unknown), run_time=1.4)
        self.finish()


class S10Return(SpokenScene):
    def construct(self):
        bars = survey_bars(show_double=True)
        self.at("Return to the winter bars")
        self.play(FadeIn(bars, lag_ratio=0.05), run_time=1.6)
        self.at("If the estimates")
        add = flow_arrow([-1.4, -3.15, 0], [-0.15, -3.15, 0], ADD, 10)
        loss = flow_arrow([0.15, -3.15, 0], [1.1, -3.15, 0], LOSS, 5)
        self.play(GrowArrow(add), GrowArrow(loss), Indicate(bars.b2, color=ADD), run_time=1.6)
        self.at("The bars alone")
        icons = VGroup(factor_icon("cold", [-5.25, 1.0, 0], 0.75),
                       factor_icon("shelter", [5.25, 1.0, 0], 0.75),
                       factor_icon("harvest", [5.25, -1.25, 0], 0.75))
        q = T("?", 54, YELLOW, weight=BOLD).move_to([0, 0.65, 0])
        self.play(FadeIn(icons, lag_ratio=0.12), FadeIn(q), run_time=1.5)
        self.at("Keep the bay window")
        ghost = RoundedRectangle(corner_radius=0.25, width=2.0, height=1.25, color=GREY,
                                 stroke_width=4).set_opacity(0.45).move_to([0, 0.35, 0])
        self.play(FadeOut(bars.double_label), Create(ghost), run_time=1.2)
        self.at("Every explanation")
        prompt = fit_text("Which addition or loss changed — and what evidence supports it?",
                          max_w=11.5, size=30, max_lines=1).move_to([0, 3.35, 0])
        self.play(FadeOut(ghost), FadeOut(bars.est), FadeIn(prompt), run_time=1.4)
        self.play(Indicate(VGroup(add, loss), color=YELLOW, scale_factor=1.05), run_time=1.6)
        self.finish()


class S11End(EndCard):
    LINE = "Populations rise when additions exceed losses,\nand fall when losses exceed additions."
