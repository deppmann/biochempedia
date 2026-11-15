"""The Timer Inside the Switch — a carried schematic G-protein world.

COLOR MAP: GDP/off = slate; GTP/on = gold; GEF/loading = teal;
GAP/cutting = clay-red.  All traces and timelines marked schematic are cartoons;
the survival curves in S10 are computed from exp(-k t).
"""
from bp_parts import *
import os
import random


SLATE = "#7F8998"
CLAY = "#C96E5C"


class MovingSpokenScene(SpokenScene):
    """A quiet cytosolic particle field keeps held teaching beats visually alive."""
    def setup(self):
        super().setup()
        rng = random.Random(os.environ.get("KX_SCENE_ID", "switch"))
        field = VGroup()
        for _ in range(120):
            d = Dot([rng.uniform(-6.7, 6.7), rng.uniform(-3.6, 3.6), 0],
                    radius=rng.uniform(0.075, 0.105), color=GREY)
            d.set_opacity(rng.uniform(0.22, 0.38)).set_z_index(-20)
            d.velocity = np.array([rng.uniform(0.28, 0.62), rng.uniform(0.12, 0.35), 0])

            def drift(mob, dt):
                mob.shift(mob.velocity * dt)
                if mob.get_x() > 6.9:
                    mob.shift(LEFT * 13.8)
                if mob.get_y() > 3.9:
                    mob.shift(DOWN * 7.8)
            d.add_updater(drift)
            field.add(d)
        self.add(field)


def membrane(receptor_on=False):
    """The carried membrane and receptor, always at the same scale and position."""
    bar = RoundedRectangle(width=12.4, height=0.42, corner_radius=0.18,
                           stroke_color=BLUE, fill_color=BLUE, fill_opacity=0.18,
                           stroke_width=3).move_to([0, 2.55, 0])
    stalk = Line([-4.35, 2.5, 0], [-4.35, 1.3, 0], color=TEAL if receptor_on else SLATE,
                 stroke_width=9)
    cup = Arc(radius=0.62, start_angle=PI, angle=PI, arc_center=[-4.35, 1.25, 0],
              color=TEAL if receptor_on else SLATE, stroke_width=9)
    receptor = VGroup(stalk, cup)
    ligand = Dot([-4.35, 3.15, 0], radius=0.22, color=TEAL)
    if not receptor_on:
        ligand.set_opacity(0.22)
        ligand.move_to([-5.35, 3.15, 0])
        receptor.set_opacity(0.55)
    return VGroup(bar, receptor, ligand)


def nucleotide(kind="GDP", at=(-0.7, -0.15, 0), scale=1.0):
    """A labelled token with two or three phosphate tiles; deliberately not a structure."""
    color = GOLD if kind == "GTP" else SLATE
    core = boxed_label(kind, color=color, size=30, box=(1.25, 0.72), fill_opacity=0.25)
    tabs = VGroup(*[
        Square(0.35, color=color, stroke_width=3, fill_color=color, fill_opacity=0.25)
        for _ in range(3 if kind == "GTP" else 2)
    ]).arrange(RIGHT, buff=0.12).next_to(core, DOWN, buff=0.14)
    g = VGroup(core, tabs).scale(scale).move_to(at)
    g.core, g.tabs = core, tabs
    return g


def switch_block(on=False, at=(-0.7, -0.35, 0), with_token=True):
    """The lesson's own picture: a large protein block with a deep nucleotide pocket."""
    color = GOLD if on else SLATE
    w = 4.4 if on else 3.8
    body = RoundedRectangle(width=w, height=2.55, corner_radius=0.34,
                            color=color, stroke_width=5, fill_color=color,
                            fill_opacity=0.16).move_to(at)
    label = T("G protein", 32, color, weight=BOLD).move_to(np.array(at) + UP * 0.82)
    g = VGroup(body, label)
    if with_token:
        token = nucleotide("GTP" if on else "GDP", np.array(at) + DOWN * 0.35, 0.78)
        g.add(token)
        g.token = token
    g.body, g.label = body, label
    return g


def target_dial(on=False, center=(4.25, -0.25, 0)):
    c = np.array(center, dtype=float)
    track = Arc(radius=1.15, start_angle=PI, angle=-PI, arc_center=c,
                stroke_color=GREY, stroke_width=10)
    angle = 0.82 if on else 0.18
    needle = Line(c, c + 0.82 * np.array([np.cos(PI - PI * angle), np.sin(PI - PI * angle), 0]),
                  color=TEXT, stroke_width=5)
    state = T("ON" if on else "OFF", 34, GOLD if on else SLATE).move_to(c + DOWN * 0.42)
    label = T("target", 28, GOLD if on else SLATE).move_to(c + DOWN * 1.12)
    return VGroup(track, needle, state, label)


def activity_trace(length=5.5, high=True, y=1.25, x0=-1.7, color=GOLD):
    """A large schematic interval trace, built at the same coordinates every time."""
    base = Line([x0, y - 0.58, 0], [x0 + 7.4, y - 0.58, 0], color=SLATE,
                stroke_width=3).set_opacity(0.55)
    if high:
        pts = [[x0, y - 0.58, 0], [x0 + 0.45, y - 0.58, 0],
               [x0 + 0.45, y, 0], [x0 + length, y, 0]]
    else:
        pts = [[x0, y, 0], [x0 + length, y, 0], [x0 + length, y - 0.58, 0],
               [x0 + 7.0, y - 0.58, 0]]
    trace = VMobject(color=color, stroke_width=7).set_points_as_corners(pts)
    dot = Dot(pts[-1], radius=0.13, color=color)
    tag = T("schematic", 24, GREY).move_to([4.95, 1.75, 0])
    return VGroup(base, trace, dot, tag)


def comparison_world(trace_length=4.9, include_question=True):
    """Exact carried frame for S07, S08 and the opening of S09."""
    rows = VGroup()
    for y in (1.05, -1.05):
        block = RoundedRectangle(width=2.5, height=1.15, corner_radius=0.25,
                                 color=GOLD, stroke_width=4, fill_color=GOLD,
                                 fill_opacity=0.17).move_to([-4.35, y, 0])
        token = nucleotide("GTP", [-4.35, y - 0.05, 0], 0.75)
        line = Line([-2.8, y, 0], [-2.8 + trace_length, y, 0], color=GOLD, stroke_width=8)
        tip = Dot(line.get_end(), radius=0.13, color=GOLD)
        rows.add(VGroup(block, token, line, tip))
    gap = boxed_label("GAP", CLAY, 30, box=(1.55, 0.75), fill_opacity=0.25).move_to([3.65, -1.05, 0])
    tag = T("schematic", 24, GREY).move_to([5.35, -2.05, 0])
    world = VGroup(rows, gap, tag)
    if include_question:
        q = fit_text("Which gold interval should end sooner?", max_w=9.8,
                     size=34, color=TEXT, max_lines=1).move_to([-0.5, 3.25, 0])
        world.add(q)
    world.rows, world.gap = rows, gap
    return world


class S00Hook(MovingSpokenScene):
    def construct(self):
        world = membrane(False)
        block = switch_block(True, at=(-0.7, -0.55, 0))
        tr = activity_trace(5.1, True, y=1.25)
        bob(block, amp=0.055, speed=1.4)
        pulse(tr[1], base=7, amp=1.1, speed=2.2)
        self.play(FadeIn(world), FadeIn(block, shift=UP * 0.15), run_time=1.3)
        self.at("yet a G protein")
        self.play(Create(tr[0]), Create(tr[1]), FadeIn(tr[2:]), run_time=1.2)
        self.at("What decides when")
        question = T("What stops an already-loaded switch?", 34, TEXT).move_to([0, -2.55, 0])
        self.play(FadeIn(question, shift=UP * 0.15), run_time=0.8)
        self.at("Follow that molecule")
        self.play(Indicate(block, color=GOLD, scale_factor=1.04), run_time=1.3)
        self.at("answer lies inside")
        self.play(Indicate(block.token, color=GOLD, scale_factor=1.12), run_time=1.4)
        self.finish()


class S01Title(TitleCard):
    LESSON = "GTPase Switches: The Timer"
    TITLE = "The Timer Inside the Switch"


class S02Off(MovingSpokenScene):
    def construct(self):
        mem = membrane(False)
        block = switch_block(False, at=(-0.65, -0.45, 0), with_token=False)
        token = nucleotide("GDP", [-0.65, -0.55, 0], 0.9)
        grip_l = Arc(radius=0.65, start_angle=-PI / 2, angle=PI, color=SLATE,
                     stroke_width=8).move_to([-1.7, -0.5, 0])
        grip_r = Arc(radius=0.65, start_angle=PI / 2, angle=PI, color=SLATE,
                     stroke_width=8).move_to([0.4, -0.5, 0])
        load = ValueTracker(0.06)
        gauge = dial(load, center=[4.35, -0.25, 0], radius=1.25,
                     label="exchange", color=TEAL, size=32)
        self.add(mem)
        self.play(FadeIn(block, shift=UP * 0.12), run_time=0.9)
        self.at("It holds GDP")
        self.play(FadeIn(token, shift=DOWN * 0.3), run_time=1.0)
        self.at("shown as a slate")
        self.play(LaggedStart(*[Indicate(t, color=SLATE) for t in token.tabs], lag_ratio=0.25), run_time=1.1)
        self.at("protein grips that token")
        self.play(Create(grip_l), Create(grip_r), run_time=1.0)
        self.play(grip_l.animate.shift(RIGHT * 0.08), grip_r.animate.shift(LEFT * 0.08), run_time=0.7)
        self.at("exchange is slow")
        self.play(FadeIn(gauge), run_time=0.6)
        self.play(load.animate.set_value(0.12), run_time=1.4)
        self.at("resting complex")
        bob(VGroup(block, token, grip_l, grip_r), amp=0.035, speed=1.3)
        self.play(Indicate(mem[1], color=SLATE, scale_factor=1.02), run_time=1.0)
        self.add(scope_tag("schematic"))
        self.finish()


class S03Gef(MovingSpokenScene):
    def construct(self):
        mem = membrane(True)
        block = switch_block(False, at=(-0.65, -0.45, 0), with_token=False)
        gdp = nucleotide("GDP", [-0.65, -0.55, 0], 0.9)
        grip = VGroup(
            Arc(radius=0.65, start_angle=-PI / 2, angle=PI, color=SLATE, stroke_width=8).move_to([-1.55, -0.5, 0]),
            Arc(radius=0.65, start_angle=PI / 2, angle=PI, color=SLATE, stroke_width=8).move_to([0.25, -0.5, 0]))
        pulse_dot = Dot([-4.35, 1.4, 0], radius=0.18, color=TEAL)
        gef = boxed_label("GEF", TEAL, 30).move_to([-4.35, -0.15, 0])
        pool = VGroup(*[Dot([2.8 + 0.75 * (i % 4), -1.9 + 0.7 * (i // 4), 0],
                                  radius=0.16, color=GOLD) for i in range(8)])
        for i, tok in enumerate(pool):
            bob(tok, amp=0.05, speed=1.5, seed=i)
        self.add(mem, block, gdp, grip, pool)
        self.at("acts as a guanine")
        self.play(FadeIn(gef), pulse_dot.animate.move_to([-4.35, 0.0, 0]), run_time=1.5)
        self.at("opens the grip")
        self.play(grip[0].animate.shift(LEFT * 0.45), grip[1].animate.shift(RIGHT * 0.45),
                  pulse_dot.animate.move_to([-0.65, 0.1, 0]), run_time=1.0)
        self.at("GDP release")
        self.play(gdp.animate.move_to([-1.3, -2.45, 0]).set_opacity(0.25), run_time=1.2)
        self.at("GTP far more plentiful")
        self.play(LaggedStart(*[Indicate(t, color=GOLD, scale_factor=1.05) for t in pool], lag_ratio=0.08), run_time=1.2)
        chosen = nucleotide("GTP", [3.35, -1.55, 0], 0.9)
        self.add(chosen)
        self.at("takes the empty place")
        self.play(chosen.animate.move_to([-0.65, -0.55, 0]), run_time=1.4)
        self.at("receptor promotes exchange")
        arrow = Arrow([-3.85, 0.4, 0], [-1.8, -0.1, 0], color=TEAL, stroke_width=5, buff=0.15)
        self.play(GrowArrow(arrow), FadeOut(pulse_dot), run_time=1.0)
        self.at("does not hand over")
        self.play(FadeOut(arrow), Indicate(pool, color=GOLD, scale_factor=1.02), run_time=1.0)
        self.finish()


class S04On(MovingSpokenScene):
    def construct(self):
        mem = membrane(True)
        off = switch_block(False, at=(-1.2, -0.65, 0))
        on = switch_block(True, at=(-1.2, -0.65, 0))
        dial_parts = target_dial(False, [4.35, -0.65, 0])
        dial_off = VGroup(dial_parts[0], dial_parts[1])
        dial_on = target_dial(True, [4.35, -0.65, 0])
        self.add(mem, off, dial_off)
        self.at("changes the protein's shape")
        self.play(Transform(off, on), FadeOut(dial_off), run_time=1.1)
        self.remove(dial_off)
        self.play(FadeIn(dial_on), run_time=0.3)
        self.at("activity trace rises")
        t = ValueTracker(0.6)
        P = Plot(box=(-2.2, 5.5, 0.8, 1.75), xr=(0, 8), yr=(0, 1), xlabel="", ylabel="")
        live = P.live_curve(lambda x: 0.15 if x < 0.55 else 0.82, t, color=GOLD, width=7)
        dot = P.dot(lambda: t.get_value(), lambda: 0.15 if t.get_value() < 0.55 else 0.82, color=GOLD)
        tag = T("schematic", 24, GREY).move_to([4.95, 2.05, 0])
        self.play(FadeIn(P.axes), run_time=0.6)
        self.add(live, dot, tag)
        self.play(t.animate.set_value(3.2), run_time=2.0, rate_func=linear)
        self.at("target beside it switches")
        self.play(Indicate(dial_off, color=GOLD, scale_factor=1.03), t.animate.set_value(4.7), run_time=1.4)
        self.at("state we will time")
        interval = Brace(Line(P.pt(0.55, 0.82), P.pt(5.3, 0.82)), UP, color=GOLD)
        ilab = T("GTP-bound interval", 28, GOLD).move_to([0.7, 2.0, 0])
        self.play(GrowFromCenter(interval), FadeIn(ilab), t.animate.set_value(6.0), run_time=1.6)
        self.at("Alpha and Beta Gamma")
        self.play(t.animate.set_value(8.0), Indicate(off, color=GOLD, scale_factor=1.02), run_time=2.0)
        self.finish()


class S05Cut(MovingSpokenScene):
    def construct(self):
        mem = membrane(True)
        on = switch_block(True, at=(-1.2, -0.65, 0))
        target = target_dial(True, [4.35, -0.65, 0])
        tr = activity_trace(4.8, True, y=1.35, x0=-2.1)
        pulse(tr[1], base=7, amp=1.5, speed=2.6)
        self.add(mem, on, target, tr)
        self.at("also an enzyme")
        enzyme = boxed_label("GTPase", GOLD, 30).move_to([-4.5, -2.55, 0])
        self.play(FadeIn(enzyme), run_time=0.8)
        self.at("After a variable weight")
        self.play(on.animate.shift(UP * 0.05), rate_func=there_and_back, run_time=1.8)
        self.at("last phosphate")
        last = on.token.tabs[-1]
        self.play(last.animate.shift(DOWN * 1.35 + RIGHT * 0.55).set_opacity(0.18), run_time=1.2)
        self.at("GDP remains")
        new_token = nucleotide("GDP", on.token.get_center(), 0.78)
        self.play(Transform(on.token, new_token), run_time=1.0)
        self.at("shape relaxes")
        off = switch_block(False, at=(-1.2, -0.65, 0))
        off_target = target_dial(False, [4.35, -0.65, 0])
        fallen = activity_trace(4.8, False, y=1.35, x0=-2.1, color=SLATE)
        self.play(Succession(FadeOut(on, run_time=0.35), FadeIn(off, run_time=0.55)),
                  Transform(tr, fallen), FadeOut(enzyme), run_time=1.2)
        self.play(ReplacementTransform(target, off_target), run_time=0.6)
        self.at("Cutting always returns")
        self.play(Indicate(off.token, color=SLATE, scale_factor=1.12), run_time=1.2)
        self.finish()


class S06Rule(MovingSpokenScene):
    def construct(self):
        left_x, right_x, y = -4.9, 4.9, 0.55
        loaded = boxed_label("GTP loaded", TEAL, 30).move_to([left_x, 1.9, 0])
        cut = boxed_label("GTP cut", SLATE, 30).move_to([right_x, 1.9, 0])
        lmark = Line([left_x, y - 0.55, 0], [left_x, y + 0.55, 0], color=TEAL, stroke_width=6)
        rmark = Line([right_x, y - 0.55, 0], [right_x, y + 0.55, 0], color=SLATE, stroke_width=6)
        span = Line([left_x, y, 0], [right_x, y, 0], color=GOLD, stroke_width=15)
        interval = T("time on", 34, GOLD).next_to(span, DOWN, buff=0.62)
        speed = ValueTracker(0.15)
        gauge = dial(speed, center=[0, -2.25, 0], radius=1.0, label="cutting speed",
                     color=CLAY, size=30)
        self.at("rule for that loaded")
        self.play(FadeIn(loaded), Create(lmark), run_time=1.0)
        self.play(Create(span), FadeIn(interval), Create(rmark), FadeIn(cut), run_time=1.5)
        self.at("Faster GTP cutting")
        self.play(FadeIn(gauge), run_time=0.7)
        self.play(speed.animate.set_value(0.9), rmark.animate.shift(LEFT * 4.2),
                  cut.animate.shift(LEFT * 4.2), span.animate.put_start_and_end_on([left_x, y, 0], [0.7, y, 0]),
                  run_time=3.2)
        self.at("Loading starts the interval")
        self.play(Indicate(VGroup(loaded, lmark), color=TEAL, scale_factor=1.04), run_time=1.0)
        self.at("hydrolysis ends it")
        self.play(Indicate(VGroup(cut, rmark), color=SLATE, scale_factor=1.04), run_time=1.0)
        self.at("does not say how often")
        self.play(Indicate(loaded, color=TEAL, scale_factor=1.03), run_time=1.5)
        self.add(scope_tag("schematic"))
        self.finish()


class S07Predict(MovingSpokenScene):
    def construct(self):
        world = comparison_world(trace_length=2.0, include_question=False)
        rows, gap = world.rows, world.gap
        gap.move_to([5.8, -1.05, 0])
        self.at("compare matched gold")
        self.play(FadeIn(rows, shift=RIGHT * 0.15), FadeIn(world[-1]), run_time=1.2)
        self.at("gap approaches only")
        self.play(FadeIn(gap), gap.animate.move_to([3.65, -1.05, 0]), run_time=1.4)
        self.at("Both begin with")
        self.play(Indicate(VGroup(rows[0][1], rows[1][1]), color=GOLD, scale_factor=1.08),
                  rows[0][2].animate.stretch(1.75, 0, about_edge=LEFT),
                  rows[1][2].animate.stretch(1.75, 0, about_edge=LEFT), run_time=2.0)
        self.at("Which gold interval")
        q = fit_text("Which gold interval should end sooner?", max_w=9.8, size=34,
                     color=TEXT, max_lines=1).move_to([-0.5, 3.25, 0])
        self.play(FadeIn(q, shift=DOWN * 0.12), rows[0][2].animate.stretch(1.25, 0, about_edge=LEFT),
                  rows[1][2].animate.stretch(1.25, 0, about_edge=LEFT), run_time=1.4)
        self.at("Hold your answer")
        pulse(rows[0][0], base=4, amp=1, speed=2.4)
        pulse(rows[1][0], base=4, amp=1, speed=2.4)
        self.play(gap.animate.shift(UP * 0.08), rate_func=there_and_back, run_time=0.8)
        self.finish()


class S08Pause(PredictPause):
    QUESTION = "Which gold interval should end sooner?"
    SECONDS = 4.5
    CARD = {"y": 3.25, "size": 34, "max_w": 9.8}
    RING_AT = (6.0, -3.0, 0)

    def backdrop(self):
        world = comparison_world(trace_length=4.9, include_question=False)
        pulse(world.rows[0][0], base=4, amp=1, speed=2.4)
        pulse(world.rows[1][0], base=4, amp=1, speed=2.4)
        bob(world.gap, amp=0.05, speed=1.7)
        return world


class S09Reveal(MovingSpokenScene):
    def construct(self):
        world = comparison_world(trace_length=4.9, include_question=True)
        rows, gap = world.rows, world.gap
        self.add(world)
        self.at("lower interval ends")
        tab = rows[1][1].tabs[-1]
        self.play(tab.animate.shift(DOWN * 0.75).set_opacity(0.15), run_time=0.8)
        lower_off = RoundedRectangle(width=2.5, height=1.15, corner_radius=0.25,
                                     color=SLATE, stroke_width=4, fill_color=SLATE,
                                     fill_opacity=0.17).move_to(rows[1][0])
        fall = VMobject(color=SLATE, stroke_width=8).set_points_as_corners([
            rows[1][2].get_start(), rows[1][2].get_end(), rows[1][2].get_end() + DOWN * 0.55])
        self.play(Transform(rows[1][0], lower_off), Transform(rows[1][2], fall),
                  FadeOut(world[-1]), run_time=1.0)
        self.at("does not remove GTP")
        no_fuel = T("speeds the cut", 30, CLAY).move_to([3.7, -2.65, 0])
        self.play(FadeOut(world[-2]), FadeIn(no_fuel), Indicate(gap, color=CLAY, scale_factor=1.05), run_time=1.3)
        self.at("reach the cutting transition")
        chevs = VGroup(*[
            VGroup(Line([-0.22, 0.22, 0], [0, 0, 0], color=CLAY, stroke_width=7),
                   Line([0, 0, 0], [-0.22, -0.22, 0], color=CLAY, stroke_width=7))
            for _ in range(2)
        ]).arrange(RIGHT, buff=0.12).move_to([2.55, -1.05, 0])
        self.play(LaggedStart(*[GrowFromCenter(c) for c in chevs], lag_ratio=0.25), run_time=1.0)
        self.at("leaves GDP behind")
        gdp = nucleotide("GDP", rows[1][1].get_center(), 0.75)
        self.play(Transform(rows[1][1], gdp), gap.animate.shift(RIGHT * 2.0).set_opacity(0.2),
                  FadeOut(chevs), run_time=1.3)
        self.at("products are unchanged")
        rule = T("same products • different speed", 32, TEXT).move_to([0, -2.75, 0])
        self.play(swap(no_fuel, rule), Indicate(rows[1][1], color=SLATE, scale_factor=1.08), run_time=1.2)
        pulse(rows[0][2], base=8, amp=1.2, speed=2.0)
        self.finish()


class S10Rate(MovingSpokenScene):
    def construct(self):
        # Survival of the loaded state for first-order cutting: S(t) = exp(-k t).
        P = Plot(box=(-5.55, 3.75, -2.25, 2.25), xr=(0, 5), yr=(0, 1),
                 xticks=[0, 1, 2, 3, 4, 5], yticks=[(0, "0"), (0.5, "0.5"), (1, "1")],
                 xlabel="time", ylabel="fraction still GTP-bound", label_size=28)
        k = ValueTracker(0.35)
        curve = always_redraw(lambda: P.curve(lambda t: np.exp(-k.get_value() * t),
                                               color=GOLD, width=8))
        rate = dial(k, center=[5.15, -0.1, 0], radius=1.05, label="cutting rate",
                    color=CLAY, fmt="", scale=0, size=30)
        tag = boxed_label("computed example", TEAL, 26).move_to([4.9, 2.65, 0])
        mean = T("mean time = 1 / cutting rate", 30, TEXT).move_to([-0.8, 3.25, 0])
        self.at("For first order cutting")
        self.play(Create(P), FadeIn(tag), run_time=1.4)
        self.at("average active time")
        self.play(FadeIn(curve), FadeIn(mean), run_time=1.0)
        self.at("larger rate constant")
        self.play(FadeIn(rate), run_time=0.6)
        self.play(k.animate.set_value(0.82), run_time=1.9)
        self.at("exact weight still varies")
        sample_t = [0.55, 1.05, 1.7, 2.5, 3.35]
        dots = VGroup(*[Dot(P.pt(t, np.exp(-k.get_value() * t)), radius=0.11,
                                 color=TEXT) for t in sample_t])
        self.play(LaggedStart(*[FadeIn(d, shift=DOWN * 0.12) for d in dots], lag_ratio=0.16), run_time=1.6)
        self.at("Fewer molecules remain")
        self.play(k.animate.set_value(0.58), LaggedStart(*[FadeOut(d, shift=DOWN * 0.2) for d in dots], lag_ratio=0.1),
                  run_time=2.2)
        self.finish()


class S11Scope(MovingSpokenScene):
    def construct(self):
        mem = membrane(True)
        def mini_switch(x):
            body = RoundedRectangle(width=1.75, height=1.25, corner_radius=0.22,
                                    color=GOLD, stroke_width=4, fill_color=GOLD,
                                    fill_opacity=0.17).move_to([x, -0.65, 0])
            label = T("GTP", 24, GOLD).move_to(body)
            return VGroup(body, label)
        switches = VGroup(*[mini_switch(-2.7 + 2.5 * i) for i in range(3)])
        target = target_dial(True, [4.75, -0.55, 0]).scale(0.78)
        messengers = VGroup(*[Dot([3.3 + 0.45 * (i % 4), -1.7 - 0.4 * (i // 4), 0],
                                     radius=0.11, color=TEAL) for i in range(8)])
        self.play(FadeIn(mem), FadeIn(switches), run_time=1.1)
        self.at("other clocks")
        clocks_text = T("other pathway clocks", 32, TEXT).move_to([0.4, 1.45, 0])
        clocks = VGroup(BackgroundRectangle(clocks_text, color=BG, fill_opacity=0.95, buff=0.12), clocks_text)
        self.play(FadeIn(clocks), run_time=0.7)
        self.at("Receptors can reload")
        self.play(LaggedStart(*[Indicate(s, color=GOLD, scale_factor=1.04) for s in switches], lag_ratio=0.2), run_time=1.4)
        self.at("targets can turn off")
        self.play(FadeIn(target), Indicate(target, color=GOLD, scale_factor=1.03), run_time=1.0)
        self.at("messengers can be cleared")
        self.play(FadeIn(messengers), run_time=0.5)
        self.play(LaggedStart(*[FadeOut(d, shift=DOWN * 0.25) for d in messengers], lag_ratio=0.12), run_time=1.4)
        self.at("clocks also shape")
        self.play(VGroup(mem[1], switches[0], switches[2], target).animate.set_opacity(0.28), run_time=1.0)
        self.at("isolates a single")
        focus = SurroundingRectangle(switches[1], color=TEXT, buff=0.22, stroke_width=4)
        span = Line([-1.25, -2.2, 0], [2.5, -2.2, 0], color=GOLD, stroke_width=10)
        label = T("one loaded lifetime", 30, TEXT).next_to(span, DOWN, buff=0.18)
        self.play(Create(focus), Create(span), FadeIn(label), run_time=1.4)
        bob(switches[1], amp=0.035, speed=1.5)
        self.finish()


class S12Handoff(MovingSpokenScene):
    def construct(self):
        switch_body = RoundedRectangle(width=2.6, height=1.25, corner_radius=0.25,
                                       color=GOLD, stroke_width=5, fill_color=GOLD,
                                       fill_opacity=0.17).move_to([0, 1.45, 0])
        switch = VGroup(switch_body, T("GTP switch", 28, GOLD).move_to(switch_body))
        load = boxed_label("loading", TEAL, 30).move_to([-4.55, 1.45, 0])
        cut = boxed_label("GTP cutting", CLAY, 30).move_to([4.55, 1.45, 0])
        base_y = -0.65
        starts = VGroup(*[Line([-5.4 + i * 2.6, base_y - 0.4, 0], [-5.4 + i * 2.6, base_y + 0.4, 0],
                                  color=TEAL, stroke_width=5) for i in range(5)])
        intervals = VGroup(*[Line([s.get_x(), base_y, 0], [s.get_x() + 1.65, base_y, 0],
                                     color=GOLD, stroke_width=12) for s in starts])
        self.play(FadeIn(switch), run_time=0.8)
        self.at("distinction makes experiments")
        self.play(FadeIn(load, shift=RIGHT * 0.15), FadeIn(cut, shift=LEFT * 0.15), run_time=1.0)
        self.at("Change loading")
        self.play(Create(starts), Create(intervals), run_time=1.2)
        frequent_starts = VGroup(*[Line([-5.4 + i * 1.7, base_y - 0.4, 0], [-5.4 + i * 1.7, base_y + 0.4, 0],
                                           color=TEAL, stroke_width=5) for i in range(7)])
        frequent_intervals = VGroup(*[Line([s.get_x(), base_y, 0], [s.get_x() + 1.05, base_y, 0],
                                              color=GOLD, stroke_width=12) for s in frequent_starts])
        self.play(Indicate(load, color=TEAL), Transform(starts, frequent_starts),
                  Transform(intervals, frequent_intervals), run_time=2.0)
        self.at("Change GTP cutting")
        long_intervals = VGroup(*[Line([s.get_x(), base_y, 0], [min(s.get_x() + 2.25, 6.0), base_y, 0],
                                         color=GOLD, stroke_width=12) for s in frequent_starts])
        self.play(Indicate(cut, color=CLAY), Transform(intervals, long_intervals), run_time=2.2)
        self.at("how long each loaded")
        self.play(Transform(intervals, frequent_intervals), run_time=1.6)
        self.at("Keeping those controls separate")
        divider = DashedLine([0, 0.75, 0], [0, -2.1, 0], color=GREY, stroke_width=3)
        labels = VGroup(T("how often", 30, TEAL).move_to([-3.2, -2.35, 0]),
                        T("how long", 30, CLAY).move_to([3.2, -2.35, 0]))
        self.play(Create(divider), FadeIn(labels), run_time=1.3)
        self.add(scope_tag("schematic"))
        pulse(switch_body, base=5, amp=1, speed=2)
        self.finish()


class S13End(EndCard):
    LINE = "Faster GTP cutting shortens an already-loaded GTPase's time on."
