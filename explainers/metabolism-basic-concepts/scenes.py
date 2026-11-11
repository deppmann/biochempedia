"""How cells pull reactions uphill.

COLOR MAP (one meaning throughout)
  BLUE   = glucose / pathway material / reactants
  YELLOW = ATP, phosphoryl transfer, and activated carriers
  GREEN  = favorable actual delta G / forward flux / products
  RED    = unfavorable actual delta G / broken coupling / heat loss
  GREY   = tracks, frames, and neutral structure
  TEXT   = enzymes and ordinary labels

All landscapes are explicitly schematic.  Molecules are labelled carts, badges,
blocks, or beads; no molecular structures are drawn.
"""
import math
import numpy as np

from bp_style import *  # noqa: F401,F403


# ---------------------------------------------------------------------------
# Shared world.  Every continuing scene uses these exact coordinates.
HILL_POINTS = [
    np.array([-6.15, -2.45, 0]),
    np.array([-4.45, -1.95, 0]),
    np.array([-2.45, -0.30, 0]),
    np.array([-0.45, 2.15, 0]),
    np.array([1.35, 1.45, 0]),
    np.array([3.15, 0.15, 0]),
    np.array([5.95, -0.90, 0]),
]


def schematic_tag(pos=(-5.45, 3.35, 0)):
    return T("SCHEMATIC", 28, GREY, weight=BOLD).move_to(pos)


def hill_track(color=GREY, opacity=1.0):
    p = VMobject(color=color, stroke_width=9).set_points_smoothly(HILL_POINTS)
    p.set_opacity(opacity)
    return p


def cart(label, color=BLUE, width=2.25, scale=1.0):
    body = RoundedRectangle(
        corner_radius=0.16, width=width, height=0.76,
        stroke_color=color, stroke_width=4, fill_color=BG, fill_opacity=0.94,
    )
    lab = fit(T(label, 28, color, weight=BOLD), max_w=width - 0.22, max_h=0.50).move_to(body)
    wheels = VGroup(
        Circle(radius=0.18, color=TEXT, stroke_width=4).move_to([-width * 0.31, -0.52, 0]),
        Circle(radius=0.18, color=TEXT, stroke_width=4).move_to([width * 0.31, -0.52, 0]),
    )
    for w in wheels:
        w.add(Line(w.get_center(), w.get_center() + UP * 0.14, color=TEXT, stroke_width=3))
    g = VGroup(body, lab, wheels).scale(scale)
    g.body, g.label, g.wheels = body, lab, wheels
    return g


def dg_gauge(value=0.65, center=(5.25, 2.0, 0), scale=1.0, title="actual ΔG"):
    """A large readout. value is -1..1 and controls both needle and fill."""
    cx, cy, _ = center
    box = RoundedRectangle(
        corner_radius=0.16 * scale, width=2.55 * scale, height=2.35 * scale,
        color=TEXT, stroke_width=3, fill_color=BG, fill_opacity=0.92,
    ).move_to(center)
    zero = Line([cx - 0.88 * scale, cy - 0.16 * scale, 0],
                [cx + 0.88 * scale, cy - 0.16 * scale, 0], color=GREY, stroke_width=3)
    plus = T("+", 30 * scale, RED, weight=BOLD).move_to([cx - 0.92 * scale, cy + 0.38 * scale, 0])
    minus = T("−", 34 * scale, GREEN, weight=BOLD).move_to([cx - 0.92 * scale, cy - 0.68 * scale, 0])
    ttl = fit(T(title, 28 * scale, TEXT, weight=BOLD), max_w=2.15 * scale).move_to([cx, cy + 0.82 * scale, 0])
    tracker = ValueTracker(value)
    fill = always_redraw(lambda: Rectangle(
        width=1.45 * scale,
        height=max(0.05, abs(tracker.get_value()) * 0.60 * scale),
        stroke_width=0,
        fill_color=RED if tracker.get_value() >= 0 else GREEN,
        fill_opacity=0.65,
    ).move_to([cx + 0.18 * scale, cy - 0.16 * scale + tracker.get_value() * 0.30 * scale, 0]))
    needle = always_redraw(lambda: Arrow(
        [cx - 0.48 * scale, cy - 0.16 * scale, 0],
        [cx + 0.60 * scale, cy - 0.16 * scale + tracker.get_value() * 0.74 * scale, 0],
        buff=0, stroke_width=5, tip_length=0.18 * scale,
        color=RED if tracker.get_value() >= 0 else GREEN,
    ))
    g = VGroup(box, zero, fill, plus, minus, ttl, needle)
    g.tracker = tracker
    return g


def balance_arrow(center=(-3.0, 2.65, 0)):
    line = Line(LEFT * 1.2, RIGHT * 1.2, color=TEXT, stroke_width=7)
    tri = Triangle(color=GREY, fill_color=GREY, fill_opacity=1).scale(0.15).rotate(PI).next_to(line, DOWN, buff=0.02)
    left = T("start", 28, BLUE).next_to(line.get_left(), UP, buff=0.12)
    right = T("G6P", 28, GREEN).next_to(line.get_right(), UP, buff=0.12)
    return VGroup(line, tri, left, right).move_to(center)


def marker_stream(y=-2.72, color=GREY):
    """Slow track markers prevent a long narrated hold from becoming a frozen frame."""
    marks = VGroup(*[
        Line(LEFT * 0.28, RIGHT * 0.28, color=color, stroke_width=5).move_to([-5.8 + i * 1.15, y, 0])
        for i in range(11)
    ])

    def drift(m, dt):
        m.shift(LEFT * 1.65 * dt)
        if m.get_x() < -6.25:
            m.shift(RIGHT * 12.65)

    for m in marks:
        m.add_updater(drift)
    return marks


def hill_world(cart_label="glucose + Pi", cart_x=-4.7, gauge_value=0.65, dim=1.0):
    track = hill_track(opacity=dim)
    ground = Polygon(
        HILL_POINTS[0], *HILL_POINTS[1:], [6.15, -3.2, 0], [-6.15, -3.2, 0],
        stroke_width=0, fill_color=GREY, fill_opacity=0.07 * dim,
    )
    c = cart(cart_label).move_to([cart_x, -1.63, 0]).set_opacity(dim)
    target = chip("G6P", GREEN, size=30, pad=0.24).move_to([4.70, -0.10, 0]).set_opacity(dim)
    gauge = dg_gauge(gauge_value).set_opacity(dim)
    tag = schematic_tag().set_opacity(dim)
    marks = marker_stream().set_opacity(dim)
    return VGroup(ground, track, marks, c, target, gauge, tag), c, gauge


def heat_waves(center=(3.3, 1.0, 0)):
    waves = VGroup()
    for i in range(3):
        wave = Arc(radius=0.36 + i * 0.23, start_angle=0.10, angle=PI * 0.82,
                   color=RED, stroke_width=5).move_to(center)
        waves.add(wave)
    return waves


def site_block(label, center, color=TEXT, width=2.3):
    box = RoundedRectangle(corner_radius=0.2, width=width, height=1.25,
                           color=color, stroke_width=4, fill_color=color, fill_opacity=0.12)
    lab = fit(T(label, 28, color, weight=BOLD), max_w=width - 0.25).move_to(box)
    return VGroup(box, lab).move_to(center)


def rope_between(a, b, color=YELLOW, loose=False):
    if loose:
        pts = [a, a + RIGHT * 0.8, (a + b) / 2 + DOWN * 0.75, b + LEFT * 0.8, b]
        return VMobject(color=color, stroke_width=8).set_points_smoothly(pts)
    return Line(a, b, color=color, stroke_width=8)


def sway_rope(rope, a, b):
    """Keep a broken connector visibly loose without implying energy transfer."""
    rope.phase = 0.0

    def update(m, dt):
        m.phase += dt
        sag = 0.68 + 0.16 * math.sin(1.7 * m.phase)
        pts = [a, a + RIGHT * 0.55, (a + b) / 2 + DOWN * sag, b + LEFT * 0.55, b]
        m.set_points_smoothly(pts)

    rope.add_updater(update)
    return rope


def pulse_forever(mob, lo=0.45, hi=0.9, speed=1.4):
    mob.phase = 0.0

    def update(m, dt):
        m.phase += dt
        m.set_opacity(lo + (hi - lo) * (0.5 + 0.5 * math.sin(speed * m.phase)))

    mob.add_updater(update)
    return mob


def rock_forever(mob, direction=RIGHT * 0.34 + UP * 0.10, speed=1.35):
    """Gentle bounded rocking for a cart awaiting an unresolved outcome."""
    mob.rock_phase = 0.0

    def update(m, dt):
        m.rock_phase += speed * dt
        m.shift(direction * math.cos(m.rock_phase) * dt)

    mob.add_updater(update)
    return mob


# ---------------------------------------------------------------------------
# s00: required TitleCard subclass, overridden with the hook-first picture.
class S00Hook(TitleCard, SpokenScene):
    LESSON = "Metabolism: basic concepts"
    TITLE = "How cells pull reactions uphill"

    def construct(self):
        world, c, gauge = hill_world()
        # Before the first word: the cart is already climbing.
        self.add(world)
        self.play(c.animate.move_to([-2.65, -0.25, 0]), run_time=2.4, rate_func=rate_functions.ease_out_cubic)

        self.at("without breaking thermodynamics")
        self.play(c.animate.shift(RIGHT * 0.45 + UP * 0.30), run_time=1.2, rate_func=rate_functions.ease_out_sine)
        self.at("glucose receives a phosphate")
        self.play(Indicate(c, color=YELLOW, scale_factor=1.07), run_time=1.0)
        # The cart visibly loses momentum throughout the concentration sentence.
        self.play(c.animate.shift(LEFT * 0.42 + DOWN * 0.20), run_time=4.7,
                  rate_func=rate_functions.ease_in_out_sine)

        self.at("favors the starting side")
        bal = balance_arrow()
        self.play(FadeIn(bal, shift=DOWN * 0.15), run_time=0.6)
        self.play(Rotate(bal[0], angle=0.24, about_point=bal[1].get_top()), run_time=1.0)

        self.at("actual delta G is positive")
        self.play(gauge.tracker.animate.set_value(0.95), Indicate(gauge, color=RED, scale_factor=1.04), run_time=1.2)
        self.at("cart rolls backward")
        self.play(FadeOut(bal), c.animate.move_to([-4.72, -1.63, 0]), run_time=2.6, rate_func=rate_functions.ease_in_out_cubic)
        self.finish()


# ---------------------------------------------------------------------------
class S01Title(NarratedScene):
    def construct(self):
        world, c, gauge = hill_world(dim=0.26)
        title = fit(T("How cells pull reactions uphill", 54, font=TITLE_FONT), max_w=11.6)
        rule = Line(LEFT * 1.35, RIGHT * 1.35, color=GOLD, stroke_width=5).next_to(title, DOWN, buff=0.34)
        self.add(world)
        self.play(FadeIn(title, shift=UP * 0.12), GrowFromCenter(rule),
                  gauge.tracker.animate.set_value(0.85), run_time=0.75)
        self.play(c.animate.shift(RIGHT * 0.35 + UP * 0.10), run_time=0.75)
        self.play(FadeOut(VGroup(title, rule), shift=UP * 0.20), run_time=0.45)
        self.finish()


# ---------------------------------------------------------------------------
class S02Rule(SpokenScene):
    def construct(self):
        world, c, gauge = hill_world(cart_label="reaction", cart_x=-4.7, gauge_value=-0.75)
        self.add(world)

        self.at("reaction runs forward")
        self.play(gauge.tracker.animate.set_value(-0.80), c.animate.move_to([-1.25, 1.12, 0]),
                  run_time=2.0, rate_func=linear)
        self.at("actual delta G is negative")
        self.play(Indicate(gauge, color=GREEN, scale_factor=1.05), run_time=1.0)
        self.play(gauge.tracker.animate.set_value(0.65), c.animate.move_to([-3.15, -0.05, 0]),
                  run_time=1.6, rate_func=linear)

        self.at("Enzymes lower activation barriers")
        hump = ArcBetweenPoints([-2.7, -0.42, 0], [1.45, 1.32, 0], angle=-PI / 1.7,
                               color=RED, stroke_width=8)
        # Keep the readable gate label clear of the activation-hump stroke.
        gate = site_block("enzyme", [-0.65, 2.72, 0], BLUE, width=2.15)
        flags = VGroup(
            T("start", 28, BLUE).move_to([-5.10, -2.92, 0]),
            T("finish", 28, GREEN).move_to([4.15, -1.48, 0]),
        )
        self.play(FadeOut(world[2]), Create(hump), FadeIn(gate, shift=DOWN * 0.2), FadeIn(flags), run_time=1.1)
        self.play(hump.animate.scale(1, 0.45, about_point=hump.get_bottom()), run_time=1.4)
        self.at("speed traffic")
        self.play(c.animate.move_to([2.65, 0.35, 0]), run_time=1.2, rate_func=linear)

        self.at("cannot change the sign")
        self.play(Indicate(gate, color=BLUE), Indicate(gauge, color=RED), run_time=0.9)
        self.play(c.animate.move_to([-4.72, -1.63, 0]), run_time=1.7, rate_func=linear)

        self.at("change the chemical journey")
        fork1 = Arrow([-3.1, -2.15, 0], [0.75, 0.85, 0], color=YELLOW, stroke_width=7, buff=0)
        fork2 = Arrow([-3.1, -2.35, 0], [1.65, -1.45, 0], color=TEAL, stroke_width=7, buff=0)
        l1 = chip("joined chemistry", YELLOW, size=28).move_to([1.95, 1.20, 0])
        l2 = chip("change concentrations", TEAL, size=28).move_to([2.90, -1.75, 0])
        self.play(FadeOut(VGroup(hump, gate, flags)), GrowArrow(fork1), FadeIn(l1), run_time=1.0)
        self.at("concentrations along it")
        self.play(GrowArrow(fork2), FadeIn(l2), run_time=1.0)
        self.play(ShowPassingFlash(fork1.copy().set_stroke(width=13), time_width=0.45),
                  ShowPassingFlash(fork2.copy().set_stroke(width=13), time_width=0.45), run_time=1.4)
        self.finish()


# ---------------------------------------------------------------------------
def joined_world():
    left_track = VMobject(color=GREY, stroke_width=9).set_points_smoothly([
        [-6.1, -2.20, 0], [-4.4, -1.60, 0], [-2.45, 0.75, 0], [-1.15, 1.55, 0]
    ])
    right_track = VMobject(color=GREY, stroke_width=9).set_points_smoothly([
        [1.15, 2.20, 0], [2.35, 1.20, 0], [4.1, -0.85, 0], [6.05, -2.10, 0]
    ])
    gc = cart("glucose", BLUE, width=1.9, scale=0.92).move_to([-4.65, -1.20, 0])
    ac = cart("ATP", YELLOW, width=1.75, scale=1.12).move_to([2.10, 1.55, 0])
    enzyme = site_block("hexokinase", [0, 0.2, 0], TEXT, width=2.55)
    enzyme[1].shift(DOWN * 0.22)
    rope = VMobject(color=YELLOW, stroke_width=9).set_points_smoothly([
        gc.get_top() + RIGHT * 0.25, [-2.35, 1.72, 0],
        enzyme.get_top() + DOWN * 0.16, [2.0, 2.45, 0], ac.get_top() + LEFT * 0.25
    ])
    tag = schematic_tag()
    marks = marker_stream(y=-3.42)
    return VGroup(left_track, right_track, marks, rope, gc, ac, enzyme, tag), gc, ac, enzyme, rope


def live_joined_rope(gc, ac, enzyme):
    """A taut connector that follows cart tops without ever crossing their labels."""
    return always_redraw(lambda: VMobject(color=YELLOW, stroke_width=9).set_points_smoothly([
        gc.get_top() + RIGHT * 0.25, [-2.35, 1.72, 0],
        enzyme.get_top() + DOWN * 0.16, [2.0, 2.45, 0], ac.get_top() + LEFT * 0.25,
    ]))


class S03Joined(SpokenScene):
    def construct(self):
        world, gc, ac, enzyme, rope = joined_world()
        self.add(world)
        self.play(gc.animate.shift(RIGHT * 0.45 + UP * 0.25), ac.animate.shift(RIGHT * 0.55 + DOWN * 0.35),
                  run_time=1.4, rate_func=linear)

        self.at("uphill reaction to a downhill")
        self.play(Indicate(rope, color=YELLOW, scale_factor=1.0), run_time=1.0)
        self.play(gc.animate.shift(RIGHT * 0.32 + UP * 0.15),
                  ac.animate.shift(RIGHT * 0.28 + DOWN * 0.18),
                  run_time=2.45, rate_func=there_and_back)
        self.at("directly transfers")
        badge = chip("phosphoryl", YELLOW, size=28, pad=0.16).move_to([2.25, 3.15, 0])
        self.play(FadeIn(badge, scale=0.65), run_time=0.45)
        self.play(FadeOut(enzyme[1]), badge.animate.move_to(enzyme.get_center() + UP * 0.38),
                  run_time=1.1, rate_func=linear)
        self.play(FadeIn(enzyme[1]), badge.animate.move_to(gc.get_center() + UP * 0.92),
                  run_time=1.1, rate_func=linear)
        self.at("not through free phosphate")
        self.play(Indicate(badge, color=YELLOW), run_time=0.8)

        self.at("becomes")
        new_a = cart("ADP", YELLOW, width=1.75, scale=1.12).move_to(ac)
        new_g = cart("G6P", GREEN, width=1.9, scale=0.92).move_to(gc)
        self.play(ReplacementTransform(ac, new_a), ReplacementTransform(gc, new_g),
                  FadeOut(badge), FadeOut(rope), run_time=1.2)
        ac, gc = new_a, new_g
        rope = live_joined_rope(gc, ac, enzyme)
        self.add(rope)
        self.bring_to_front(gc, ac, enzyme)
        self.play(gc.animate.shift(RIGHT * 0.30 + UP * 0.16),
                  ac.animate.shift(RIGHT * 0.30 + DOWN * 0.18),
                  run_time=2.3, rate_func=there_and_back)

        self.at("one chemical reaction")
        one = T("ONE CHEMICAL REACTION", 32, TEXT, weight=BOLD).move_to([0, -2.65, 0])
        self.play(FadeIn(one, shift=UP * 0.12), Indicate(enzyme, color=TEXT), run_time=0.9)
        self.at("changes add")
        a_up = Arrow([-4.4, -2.55, 0], [-2.7, -2.55, 0], color=RED, stroke_width=7, buff=0)
        a_dn = Arrow([2.5, -2.55, 0], [0.9, -2.55, 0], color=GREEN, stroke_width=9, buff=0)
        net = Arrow([-1.35, -2.55, 0], [1.35, -2.55, 0], color=GREEN, stroke_width=10, buff=0)
        self.play(FadeOut(one), GrowArrow(a_up), GrowArrow(a_dn), run_time=0.8)
        self.play(ReplacementTransform(VGroup(a_up, a_dn), net), run_time=0.9)

        self.at("actual delta G is negative")
        gauge = dg_gauge(-0.85, center=(5.15, 2.12, 0), scale=0.92)
        self.play(FadeIn(gauge, shift=LEFT * 0.15), run_time=0.7)
        self.play(Indicate(gauge, color=GREEN), run_time=0.8)
        self.at("joined carts move forward")
        self.play(gc.animate.move_to([-1.45, 1.35, 0]), ac.animate.move_to([5.05, -1.52, 0]),
                  run_time=2.5, rate_func=linear)
        self.finish()


# ---------------------------------------------------------------------------
def separated_world():
    lt = VMobject(color=GREY, stroke_width=8).set_points_smoothly([
        [-6.1, -2.2, 0], [-4.8, -1.5, 0], [-3.7, 0.2, 0], [-2.6, 1.15, 0]
    ])
    rt = VMobject(color=GREY, stroke_width=8).set_points_smoothly([
        [2.6, 1.7, 0], [3.6, 0.65, 0], [4.8, -1.2, 0], [6.1, -2.2, 0]
    ])
    up = site_block("attach Pi", [-1.55, 0.40, 0], BLUE, 2.15)
    down = site_block("hydrolyze ATP", [1.65, 0.40, 0], YELLOW, 2.55)
    rope = rope_between(up.get_right(), down.get_left(), loose=True)
    gc = cart("glucose", BLUE, 1.9, 0.90).move_to([-4.85, -1.05, 0])
    ac = cart("ATP", YELLOW, 1.65, 0.95).move_to([4.10, 1.52, 0])
    marks = marker_stream(y=-3.42)
    return VGroup(lt, rt, marks, rope, gc, ac, up, down, schematic_tag()), gc, ac, up, down, rope


class S04Predict(SpokenScene):
    def construct(self):
        # Begin with the joined block and split it in place.
        base, gc, ac, enzyme, rope = joined_world()
        self.add(base)
        rock_forever(gc)
        rock_forever(ac, direction=RIGHT * 0.28 + DOWN * 0.10, speed=1.25)
        self.at("separates the jobs")
        up = site_block("attach Pi", [-1.55, 0.40, 0], BLUE, 2.15)
        down = site_block("hydrolyze ATP", [1.65, 0.40, 0], YELLOW, 2.55)
        loose = rope_between(up.get_right(), down.get_left(), loose=True)
        sway_rope(loose, up.get_right(), down.get_left())
        self.play(FadeOut(rope), ReplacementTransform(enzyme.copy(), up), ReplacementTransform(enzyme, down),
                  FadeIn(loose), run_time=1.3)
        self.play(gc.animate.move_to([-4.85, -1.05, 0]), ac.animate.move_to([4.10, 1.52, 0]), run_time=1.1)

        self.at("One site hydrolyzes")
        water = T("H₂O", 30, TEAL, weight=BOLD).move_to([5.25, 2.35, 0])
        self.play(FadeIn(water, shift=LEFT * 0.15), ac.animate.move_to([4.10, 1.30, 0]), run_time=0.9)
        adp = chip("ADP", YELLOW, size=28).move_to([3.45, -0.95, 0])
        pi = chip("Pi", YELLOW, size=28).move_to([4.85, -1.35, 0])
        self.play(FadeOut(ac), FadeOut(water), FadeIn(adp), FadeIn(pi), run_time=0.9)

        self.at("tries to attach free phosphate")
        pi2 = chip("Pi", YELLOW, size=28).move_to([-4.0, -0.25, 0])
        target = chip("G6P?", GREEN, size=30).move_to([-3.0, 1.45, 0])
        rock_forever(pi2, direction=RIGHT * 0.25 + UP * 0.08, speed=1.35)
        self.play(FadeIn(pi2), FadeIn(target, shift=DOWN * 0.15), run_time=0.7)
        self.play(gc.animate.shift(RIGHT * 0.65 + UP * 0.30), pi2.animate.shift(RIGHT * 0.45 + UP * 0.30),
                  run_time=1.1, rate_func=there_and_back)

        self.at("no shared intermediate")
        broken = VGroup(Line(LEFT * 0.35, RIGHT * 0.35, color=RED, stroke_width=8).rotate(0.7),
                        Line(LEFT * 0.35, RIGHT * 0.35, color=RED, stroke_width=8).rotate(-0.7)).move_to([0, 1.55, 0])
        self.play(FadeIn(broken, scale=0.6), Indicate(loose, color=RED), run_time=0.9)

        self.at("add on paper")
        card = VGroup(
            RoundedRectangle(corner_radius=0.12, width=2.65, height=1.05, color=GREEN,
                             fill_color=BG, fill_opacity=0.95),
            M("sum < 0", 32, GREEN),
        ).move_to([0, -1.85, 0])
        self.play(FadeIn(card, shift=UP * 0.15), run_time=0.8)

        self.at("Will glucose")
        question = fit(T("Will glucose-6-phosphate form?", 45, TEXT, weight=BOLD), max_w=12.0).move_to([0, 2.72, 0])
        self.play(FadeOut(broken), FadeIn(question, shift=DOWN * 0.12), run_time=0.8)
        self.play(gc.animate.shift(RIGHT * 0.25 + UP * 0.10), pi2.animate.shift(RIGHT * 0.18 + UP * 0.10),
                  run_time=1.0, rate_func=there_and_back)
        self.finish()


# ---------------------------------------------------------------------------
class S05PredictHold(NarratedScene):
    def construct(self):
        world, gc, ac, up, down, rope = separated_world()
        question = fit(T("Will glucose-6-phosphate form?", 45, TEXT, weight=BOLD), max_w=12.0).move_to([0, 2.72, 0])
        dots = VGroup(*[Circle(radius=0.13, color=YELLOW, stroke_width=3) for _ in range(4)])
        dots.arrange(RIGHT, buff=0.28).move_to([0, -2.55, 0])
        self.add(world, question, dots)
        sway_rope(rope, up.get_right(), down.get_left())
        for i in range(4):
            self.play(dots[i].animate.set_fill(YELLOW, opacity=1),
                      gc.animate.shift((RIGHT if i % 2 == 0 else LEFT) * 0.13),
                      ac.animate.shift((RIGHT if i % 2 == 0 else LEFT) * 0.10), run_time=1.0)
        self.finish()


# ---------------------------------------------------------------------------
class S06Answer(SpokenScene):
    def construct(self):
        world, gc, ac, up, down, rope = separated_world()
        self.add(world)
        sway_rope(rope, up.get_right(), down.get_left())
        rock_forever(gc, direction=RIGHT * 0.22 + UP * 0.07, speed=1.15)
        rock_forever(ac, direction=LEFT * 0.18 + DOWN * 0.06, speed=1.25)
        no = T("NO", 62, RED, weight=BOLD).move_to([-3.75, 2.25, 0])
        self.play(FadeIn(no, scale=1.35), run_time=0.55)

        self.at("hydrolysis runs downhill")
        adp = cart("ADP", YELLOW, 1.65, 0.95).move_to(ac)
        self.play(ReplacementTransform(ac, adp), run_time=0.55)
        self.play(adp.animate.move_to([5.15, -1.55, 0]), run_time=0.95)
        self.at("leaves as heat")
        heat = heat_waves([3.25, 1.65, 0])
        self.play(Create(heat), run_time=0.8)
        self.play(heat.animate.shift(UP * 0.75).set_opacity(0), run_time=1.2)

        self.at("glucose cart still rolls backward")
        self.play(gc.animate.move_to([-5.35, -1.55, 0]), run_time=1.7, rate_func=rate_functions.ease_in_cubic)

        self.at("Arithmetic alone")
        card_l = VGroup(RoundedRectangle(corner_radius=0.1, width=1.5, height=0.9, color=GREEN), M("sum", 28, GREEN)).move_to([-0.85, -2.15, 0])
        card_r = VGroup(RoundedRectangle(corner_radius=0.1, width=1.5, height=0.9, color=GREEN), M("< 0", 28, GREEN)).move_to([0.85, -2.15, 0])
        self.play(FadeIn(card_l), FadeIn(card_r), run_time=0.55)
        self.at("not coupling")
        self.play(card_l.animate.shift(LEFT * 0.65 + DOWN * 0.18).rotate(0.16),
                  card_r.animate.shift(RIGHT * 0.65 + DOWN * 0.18).rotate(-0.16), run_time=0.75)
        self.play(FadeOut(VGroup(card_l, card_r, no, heat)), run_time=0.4)

        center = np.array([0, -1.35, 0])
        self.at("direct transfer")
        badge = chip("phosphoryl", YELLOW, size=28).move_to([-2.25, 2.42, 0])
        direct = Arrow([-2.2, 1.68, 0], [2.2, 1.68, 0], color=YELLOW, stroke_width=8, buff=0)
        self.play(FadeOut(rope), GrowArrow(direct), FadeIn(badge),
                  up.animate.shift(RIGHT * 0.22 + DOWN * 0.48),
                  down.animate.shift(LEFT * 0.22 + DOWN * 0.48), run_time=0.8)
        self.play(badge.animate.move_to([2.25, 2.42, 0]), run_time=0.8)

        self.at("shared intermediate")
        inter = chip("intermediate", TEAL, size=28).move_to(center)
        self.play(FadeOut(VGroup(direct, badge)), FadeIn(inter, shift=RIGHT * 0.2), run_time=0.55)
        self.play(inter.animate.shift(RIGHT * 1.4), up.animate.shift(LEFT * 0.22 + UP * 0.48),
                  down.animate.shift(RIGHT * 0.22 + UP * 0.48), run_time=0.8)

        self.at("linked shape changes")
        gear1 = Circle(radius=0.60, color=BLUE, stroke_width=8).move_to([-0.52, -1.30, 0])
        gear2 = Circle(radius=0.60, color=YELLOW, stroke_width=8).move_to([0.52, -1.30, 0])
        for g in (gear1, gear2):
            for ang in np.linspace(0, TAU, 8, endpoint=False):
                tooth = Line(g.point_at_angle(ang), g.point_at_angle(ang) + 0.18 * np.array([math.cos(ang), math.sin(ang), 0]),
                             color=g.get_color(), stroke_width=7)
                g.add(tooth)
        self.play(FadeOut(inter), FadeIn(gear1), FadeIn(gear2), run_time=0.55)
        self.play(Rotate(gear1, PI * 1.2), Rotate(gear2, -PI * 1.2), run_time=1.0, rate_func=linear)

        taut = Line(up.get_right(), down.get_left(), color=YELLOW, stroke_width=9)
        self.play(FadeOut(VGroup(gear1, gear2)), FadeIn(taut), run_time=0.7)
        pulse_forever(taut, 0.65, 1.0, 1.7)
        self.finish()


# ---------------------------------------------------------------------------
def pathway_world():
    # Same broad hill footprint, relabelled as a pathway.
    track = hill_track()
    A = chip("A", BLUE, size=32).move_to([-5.45, -1.75, 0])
    Bbox = RoundedRectangle(corner_radius=0.25, width=2.35, height=2.10,
                            color=BLUE, stroke_width=4, fill_color=BLUE, fill_opacity=0.08).move_to([0.0, 1.15, 0])
    Blab = T("B basin", 28, BLUE, weight=BOLD).move_to([0, 2.55, 0])
    C = chip("+ C", BLUE, size=28).move_to([2.10, 2.40, 0])
    D = chip("D", GREEN, size=32).move_to([5.35, -1.45, 0])
    beads = VGroup(*[Dot(radius=0.16, color=BLUE).move_to([
        -0.70 + (i % 4) * 0.46, 0.42 + (i // 4) * 0.43, 0
    ]) for i in range(12)])
    wheel = Circle(radius=0.43, color=GREEN, stroke_width=7).move_to([3.25, -0.10, 0])
    wheel.add(Line(wheel.get_left(), wheel.get_right(), color=GREEN, stroke_width=5),
              Line(wheel.get_top(), wheel.get_bottom(), color=GREEN, stroke_width=5))
    chute = Arrow([3.70, -0.40, 0], [4.85, -1.12, 0], color=GREEN, stroke_width=8, buff=0)
    marks = marker_stream(y=-3.42)
    return VGroup(track, marks, A, Bbox, Blab, C, D, beads, wheel, chute, schematic_tag()), beads, wheel, A


class S07ProductDrain(SpokenScene):
    def construct(self):
        world, beads, wheel, A = pathway_world()
        self.add(world)
        wheel.add_updater(lambda m, dt: m.rotate(-0.55 * dt))
        self.play(A.animate.shift(RIGHT * 0.25 + UP * 0.12), run_time=0.8, rate_func=there_and_back)
        self.play(Wiggle(beads, scale_value=1.02, rotation_angle=0.04, n_wiggles=5), run_time=2.8)

        self.at("A to B plus C")
        first = chip("+21 kJ/mol standard", RED, size=28).move_to([-1.90, 3.18, 0])
        self.play(FadeIn(first, shift=DOWN * 0.15), run_time=0.7)
        self.play(beads.animate.shift(RIGHT * 0.40), run_time=2.3, rate_func=there_and_back)
        self.at("B to D")
        second = chip("−34 kJ/mol standard", GREEN, size=28).move_to([4.30, 3.15, 0])
        self.play(FadeIn(second, shift=DOWN * 0.15), run_time=0.7)
        total = chip("pathway total −13", GREEN, size=30).move_to([0, -2.72, 0])
        self.play(beads.animate.shift(LEFT * 0.30), TransformFromCopy(VGroup(first, second), total),
                  run_time=1.9, rate_func=linear)
        self.play(FadeOut(first), FadeOut(second), run_time=0.35)

        self.at("Draining B")
        self.play(Rotate(wheel, -TAU), run_time=0.75, rate_func=linear)
        drain_beads = VGroup(*[beads[i] for i in range(5)])
        self.play(drain_beads.animate.move_to([4.85, -1.10, 0]).set_opacity(0),
                  Rotate(wheel, -TAU), run_time=0.85, rate_func=linear)

        self.at("actual delta G below zero")
        gauge = dg_gauge(0.40, center=(-4.85, 0.85, 0), scale=0.88, title="step 1 actual ΔG")
        self.play(FadeIn(gauge, shift=RIGHT * 0.1), run_time=0.55)
        self.play(gauge.tracker.animate.set_value(-0.75), run_time=1.1)
        self.play(A.animate.move_to([-2.15, 0.28, 0]), Rotate(wheel, -TAU), run_time=1.5, rate_func=linear)

        self.at("pathway total is minus")
        self.play(Indicate(total, color=GREEN, scale_factor=1.08), run_time=0.8)
        self.at("that is not enough")
        pile = VGroup(*[Dot(radius=0.16, color=BLUE).move_to([
            -0.72 + (i % 4) * 0.47, 0.40 + (i // 4) * 0.38, 0
        ]) for i in range(16)])
        self.play(FadeIn(pile), gauge.tracker.animate.set_value(0.0), A.animate.shift(LEFT * 0.25), run_time=1.2)
        stop = T("STOP", 34, RED, weight=BOLD).move_to([-3.00, 1.55, 0])
        self.play(FadeIn(stop, scale=1.2), run_time=0.55)

        self.at("Every step carrying forward flux")
        self.play(FadeOut(VGroup(pile, stop)), gauge.tracker.animate.set_value(-0.70),
                  Rotate(wheel, -TAU), run_time=1.2, rate_func=linear)
        arrows = VGroup(
            Arrow([-5.0, -1.25, 0], [-3.25, -0.18, 0], color=GREEN, stroke_width=8, buff=0),
            Arrow([1.65, 0.85, 0], [3.0, 0.0, 0], color=GREEN, stroke_width=8, buff=0),
            Arrow([3.6, -0.45, 0], [4.85, -1.15, 0], color=GREEN, stroke_width=8, buff=0),
        )
        self.at("negative actual delta G")
        self.play(LaggedStart(*[GrowArrow(a) for a in arrows], lag_ratio=0.22), run_time=1.3)
        self.play(A.animate.shift(RIGHT * 0.70 + UP * 0.34),
                  beads.animate.move_to([4.45, -0.82, 0]).set_opacity(0.18),
                  Rotate(wheel, -TAU), run_time=1.6, rate_func=linear)
        pulse_forever(arrows, 0.55, 1.0, 1.8)
        self.finish()


# ---------------------------------------------------------------------------
class S08EquilibriumShift(SpokenScene):
    def construct(self):
        track = hill_track(opacity=0.55)
        tag = chip("separate example, not glucose", TEAL, size=28).move_to([-3.00, 2.65, 0])
        reaction = cart("A → B", BLUE, 2.0, 0.9).move_to([-4.65, -1.00, 0])
        atp = chip("ATP", YELLOW, size=30).move_to([-4.55, 1.58, 0])
        marks = marker_stream(y=-3.42)

        dial = RoundedRectangle(corner_radius=0.25, width=5.75, height=3.25,
                                color=TEXT, stroke_width=4, fill_color=BG, fill_opacity=0.96).move_to([2.60, 1.35, 0])
        dial_title = fit(T("COMPUTED FROM STATED K VALUES", 28, TEXT, weight=BOLD), max_w=5.05).move_to([2.60, 2.52, 0])
        arc = Arc(radius=1.38, start_angle=PI, angle=-PI, color=GREY, stroke_width=8).move_to([2.60, 1.25, 0])
        tracker = ValueTracker(0.04)
        needle = always_redraw(lambda: Arrow(
            [2.60, 1.25, 0],
            [2.60 + 1.15 * math.cos(PI - PI * tracker.get_value()),
             1.25 + 1.15 * math.sin(PI - PI * tracker.get_value()), 0],
            color=YELLOW, stroke_width=7, buff=0, tip_length=0.20,
        ))
        readout = M("K = 0.001", 36, RED).move_to([2.60, 0.10, 0])
        self.add(track, marks, tag, reaction, atp, dial, arc, dial_title, needle, readout, schematic_tag())

        react_tray = RoundedRectangle(corner_radius=0.20, width=3.6, height=1.20, color=BLUE,
                                      fill_color=BLUE, fill_opacity=0.08).move_to([-3.70, -2.35, 0])
        prod_tray = RoundedRectangle(corner_radius=0.20, width=3.6, height=1.20, color=GREEN,
                                     fill_color=GREEN, fill_opacity=0.08).move_to([3.70, -2.35, 0])
        rs = VGroup(*[Dot(radius=0.14, color=BLUE).move_to([-5.05 + (i % 7) * 0.43, -2.62 + (i // 7) * 0.42, 0]) for i in range(21)])
        ps = VGroup(Dot(radius=0.14, color=GREEN).move_to([3.7, -2.35, 0]))
        self.play(FadeIn(react_tray), FadeIn(prod_tray), FadeIn(rs), FadeIn(ps), run_time=0.7)
        self.play(rs.animate.shift(UP * 0.28), run_time=1.1, rate_func=there_and_back)
        self.play(reaction.animate.shift(RIGHT * 0.50 + UP * 0.27), run_time=3.0,
                  rate_func=rate_functions.ease_in_out_sine)

        self.at("one thousandth")
        self.play(FadeOut(tag), Indicate(readout, color=RED), run_time=0.65)
        self.at("two hundred sixty")
        new_readout = M("K = 267", 40, GREEN).move_to(readout)
        rope = Arrow(atp.get_right(), dial.get_left(), color=YELLOW, stroke_width=9, buff=0.10)
        self.play(GrowArrow(rope), tracker.animate.set_value(0.92), ReplacementTransform(readout, new_readout),
                  run_time=1.7, rate_func=linear)
        self.play(rs.animate.move_to(prod_tray).set_color(GREEN), reaction.animate.move_to([3.7, -0.95, 0]),
                  run_time=2.0, rate_func=linear)

        self.at("more than two hundred thousand")
        counter = M("×1", 48, TEXT).move_to([-1.65, 0.10, 0])
        self.play(FadeIn(counter), run_time=0.35)
        for txt in ("×100", "×10,000", ">×200,000"):
            nxt = M(txt, 46, GREEN, weight=BOLD).move_to(counter)
            self.play(ReplacementTransform(counter, nxt), run_time=0.50)
            counter = nxt
        pulse_forever(prod_tray, 0.55, 1.0, 1.8)
        self.finish()


# ---------------------------------------------------------------------------
class S09Return(SpokenScene):
    def construct(self):
        world, gc, ac, enzyme, rope = joined_world()
        self.add(world)
        self.at("answer to our puzzle")
        self.play(Indicate(enzyme, color=TEXT), run_time=0.8)
        self.at("direct phosphoryl transfer")
        badge = chip("phosphoryl", YELLOW, size=28).move_to([2.25, 3.15, 0])
        self.play(FadeIn(badge, scale=0.65), run_time=0.35)
        self.play(FadeOut(enzyme[1]), badge.animate.move_to(enzyme.get_center() + UP * 0.38), run_time=0.75)
        self.play(FadeIn(enzyme[1]), badge.animate.move_to(gc.get_center() + UP * 0.92), run_time=0.75)
        self.play(ShowPassingFlash(rope.copy().set_stroke(width=24), time_width=0.65), run_time=1.15)
        self.at("glucose phosphorylation can run forward")
        new_gc = cart("G6P", GREEN, 1.9, 0.92).move_to(gc)
        new_ac = cart("ADP", YELLOW, 1.75, 1.12).move_to(ac)
        self.play(ReplacementTransform(gc, new_gc), ReplacementTransform(ac, new_ac),
                  FadeOut(badge), FadeOut(rope), run_time=0.7)
        rope = live_joined_rope(new_gc, new_ac, enzyme)
        self.add(rope)
        self.bring_to_front(new_gc, new_ac, enzyme)
        self.play(new_gc.animate.move_to([-1.35, 1.35, 0]), new_ac.animate.move_to([5.05, -1.55, 0]),
                  run_time=1.7, rate_func=linear)

        self.at("following step may instead")
        self.play(*[FadeOut(m) for m in list(self.mobjects)], run_time=0.45)
        pworld, beads, wheel, A = pathway_world()
        self.play(FadeIn(pworld), run_time=0.55)
        self.at("keep a product scarce")
        drain = VGroup(*[beads[i] for i in range(5)])
        self.play(drain.animate.move_to([4.85, -1.10, 0]).set_opacity(0), Rotate(wheel, -TAU),
                  A.animate.shift(RIGHT * 1.15 + UP * 0.60), run_time=1.5, rate_func=linear)

        self.at("same rule governs")
        carrier = chip("ATP", YELLOW, size=32).move_to([-3.9, 2.55, 0])
        gauge = dg_gauge(-0.78, center=(4.75, 1.55, 0), scale=0.86)
        self.play(FadeIn(carrier), FadeIn(gauge), run_time=0.55)
        for name in ("activated carrier", "energy carrier"):
            nxt = chip(name, YELLOW, size=28).move_to(carrier)
            self.play(ReplacementTransform(carrier, nxt), run_time=0.55)
            carrier = nxt

        self.at("Uphill chemistry runs only")
        gauge[2].clear_updaters()
        gauge[6].clear_updaters()
        dim_track = hill_track(opacity=0.16)
        dim_marks = marker_stream(y=-3.42).set_opacity(0.28)
        dim_cart = cart("", GREEN, 1.5, 0.55).set_opacity(0.18).move_to([-4.8, -1.55, 0])
        self.play(FadeOut(VGroup(pworld, carrier, gauge)), FadeIn(VGroup(dim_track, dim_marks, dim_cart)), run_time=0.65)
        line1 = T("Uphill chemistry runs only when coupling", 40, TEXT, weight=BOLD)
        line2 = T("makes its actual ΔG negative.", 44, GREEN, weight=BOLD)
        takeaway = VGroup(line1, line2).arrange(DOWN, buff=0.22).move_to([0, 0.15, 0])
        panel = RoundedRectangle(corner_radius=0.18, width=11.7, height=1.65,
                                 stroke_width=0, fill_color=BG, fill_opacity=1.0).move_to(takeaway)
        self.play(FadeIn(panel), FadeIn(takeaway, shift=UP * 0.12),
                  dim_cart.animate.move_to([-1.5, 0.75, 0]), run_time=0.9)
        underline = Line(line2.get_left(), line2.get_right(), color=GREEN, stroke_width=6).next_to(line2, DOWN, buff=0.12)
        self.at("actual delta G negative")
        self.play(Create(underline), dim_cart.animate.move_to([4.85, -1.25, 0]), run_time=1.0)
        self.finish()


# ---------------------------------------------------------------------------
class S10End(EndCard):
    LINE = "Uphill chemistry runs only when coupling makes its actual ΔG negative."

    def construct(self):
        track = hill_track(opacity=0.18)
        faint = cart("", GREEN, 1.5, 0.55).set_opacity(0.18).move_to([-4.8, -1.55, 0])
        hexm = hex_mascot(1.35)
        line1 = T("Uphill chemistry runs only when coupling", 40, font=TITLE_FONT)
        line2 = T("makes its actual ΔG negative.", 43, GREEN, font=TITLE_FONT)
        line = VGroup(line1, line2).arrange(DOWN, buff=0.18).move_to([0, 1.05, 0])
        panel = RoundedRectangle(corner_radius=0.18, width=11.7, height=1.6,
                                 stroke_width=0, fill_color=BG, fill_opacity=1.0).move_to(line)
        hexm.move_to([0, -1.45, 0])
        self.add(track, faint)
        self.play(FadeIn(panel), FadeIn(line, shift=UP * 0.12), FadeIn(hexm), run_time=0.75)
        self.play(faint.animate.move_to([4.85, -1.25, 0]), run_time=2.7, rate_func=linear)
        shoulder = hexm.arm.get_start()
        for _ in range(2):
            self.play(Rotate(hexm.arm, angle=-0.55, about_point=shoulder), rate_func=there_and_back, run_time=0.35)
        self.finish()
