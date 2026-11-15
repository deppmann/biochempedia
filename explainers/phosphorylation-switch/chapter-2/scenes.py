"""Two Enzymes Set the Level — phosphorylation switch, chapter 2.

COLOR MAP (kept from chapter 1): protein teal, phosphate gold, kinase blue,
phosphatase red, ATP violet.  Protein copies are schematic blocks; every
population/cycle view is rebuilt by the same builders below.
"""
from bp_parts import *


VIOLET = "#B58CD9"
PROTEIN = TEAL
PHOSPHATE = GOLD
KINASE = BLUE
PHOSPHATASE = RED
ATP = VIOLET

TOTAL = 12
ROW_X = np.linspace(-5.75, 5.75, TOTAL)
LEFT_POS = [(-5.0 + 1.28 * (i % 3), 0.60 - 0.92 * (i // 3)) for i in range(6)]
RIGHT_POS = [(2.45 + 1.28 * (i % 3), 0.60 - 0.92 * (i // 3)) for i in range(6)]
PREDICT_QUESTION = "Which way will the phosphorylated fraction move?"
PREDICT_OPTIONS = ("down", "same", "up")


def copy_block(center=ORIGIN, marked=False, scale=1.0):
    """One protein copy in the same rounded-block language as chapter 1."""
    body = RoundedRectangle(
        corner_radius=0.16 * scale,
        width=0.78 * scale,
        height=0.58 * scale,
        stroke_color=PROTEIN,
        stroke_width=3.5,
        fill_color=PROTEIN,
        fill_opacity=0.25,
    )
    g = VGroup(body)
    if marked:
        g.add(Dot(radius=0.105 * scale, color=PHOSPHATE).move_to(body.get_corner(UR) + 0.02 * LEFT + 0.02 * DOWN))
    return g.move_to(center)


def shimmer_copies(copies):
    """Keep the protein population visibly alive without moving its landmarks."""
    for i, copy in enumerate(copies):
        body = copy[0]
        body._shimmer_t = 0.45 * i

        def update(mob, dt):
            mob._shimmer_t += dt
            mob.set_fill(PROTEIN, opacity=0.23 + 0.09 * (0.5 + 0.5 * np.sin(1.8 * mob._shimmer_t)))
        body.add_updater(update)

        def bob(mob, dt, i=i):
            mob._bob_t = getattr(mob, "_bob_t", 0.7 * i) + dt
            prev = 0.05 * np.sin(1.6 * (mob._bob_t - dt) + i)
            now = 0.05 * np.sin(1.6 * mob._bob_t + i)
            mob.shift(UP * (now - prev))
        copy.add_updater(bob)
    return copies


def flow_particles(start, end, color, phase=0.0):
    dots = VGroup(*[Dot(radius=0.075, color=color) for _ in range(3)])
    a, b = np.array(start, dtype=float), np.array(end, dtype=float)
    for i, dot in enumerate(dots):
        dot._flow_t = phase + i / 3

        def update(mob, dt, a=a, b=b):
            mob._flow_t = (mob._flow_t + 0.24 * dt) % 1.0
            mob.move_to(interpolate(a, b, mob._flow_t))
        dot.add_updater(update)
    return dots


def population_row(marked=6, y=-0.15, scale=0.92):
    """The carried fixed population: always twelve copies at these positions."""
    return shimmer_copies(VGroup(*[
        copy_block([x, y + (0.12 if i % 2 else -0.12), 0], i < marked, scale)
        for i, x in enumerate(ROW_X)
    ]))


def looping_rider(scene, P, fn, lo, hi, period, color=TEXT, radius=0.2, drops=True, phase=0.0):
    """Ambient motion on a computed curve: a marker loops along it with drop lines to the axes."""
    tr = ValueTracker(lo)
    tr._el = phase * period

    def step(mob, dt):
        mob._el += dt
        mob.set_value(lo + (hi - lo) * ((mob._el / period) % 1.0))
    tr.add_updater(step)

    def mk():
        x = tr.get_value()
        d = Dot(P.pt(x, fn(x)), radius=radius, color=color, stroke_color=TEAL, stroke_width=3)
        g = VGroup(d)
        if drops:
            g.add(DashedLine(P.pt(x, fn(x)), P.pt(x, P.yr[0]), color=color, stroke_width=3, dash_length=0.12))
            g.add(DashedLine(P.pt(x, fn(x)), P.pt(P.xr[0], fn(x)), color=color, stroke_width=3, dash_length=0.12))
        return g
    rider = always_redraw(mk)
    scene.add(tr, rider)
    return tr, rider


def flow_arrow(start, end, color, label, width=7):
    arrow = Arrow(start, end, buff=0, color=color, stroke_width=width, tip_length=0.22)
    lab = T(label, 28, color).next_to(arrow, UP, buff=0.12)
    return VGroup(arrow, lab)


def lane_world(marked=6, kinase_width=7, phosphatase_width=7, gauge_value=0.5,
               show_gauge=True, show_total=True, blank_gauge=False):
    """The one cycle world, rebuilt unchanged in every continuing lane scene."""
    left = RoundedRectangle(corner_radius=0.2, width=5.15, height=3.75,
                            stroke_color=PROTEIN, stroke_width=2.5,
                            fill_color=PROTEIN, fill_opacity=0.15).move_to([-3.35, -0.25, 0])
    right = left.copy().move_to([3.35, -0.25, 0])
    lh = T("unphosphorylated", 28, PROTEIN).move_to([-3.35, 1.35, 0])
    rh = T("phosphorylated", 28, PHOSPHATE).move_to([3.35, 1.35, 0])
    n_right = int(np.clip(marked, 0, TOTAL))
    n_left = TOTAL - n_right
    proteins = VGroup()
    for i in range(n_left):
        proteins.add(copy_block([*LEFT_POS[i], 0], False, 0.88))
    for i in range(n_right):
        proteins.add(copy_block([*RIGHT_POS[i], 0], True, 0.88))
    kin = flow_arrow([-1.16, 0.56, 0], [1.16, 0.56, 0], KINASE, "kinase", kinase_width)
    pho = flow_arrow([1.16, -0.72, 0], [-1.16, -0.72, 0], PHOSPHATASE, "phosphatase", phosphatase_width)
    kin[1].move_to([-3.35, -1.62, 0])
    pho[1].move_to([3.35, -1.62, 0])
    shimmer_copies(proteins)
    particles = VGroup(flow_particles([-1.05, 0.56, 0], [1.05, 0.56, 0], KINASE),
                       flow_particles([1.05, -0.72, 0], [-1.05, -0.72, 0], PHOSPHATASE, 0.4))
    g = VGroup(left, right, lh, rh, proteins, kin, pho, particles)
    if show_total:
        total = boxed_label("fixed total: 12", PROTEIN, size=28, pad=0.24).move_to([-5.05, 3.22, 0])
        g.add(total)
        g.total = total
    if show_gauge:
        f = ValueTracker(gauge_value)
        gauge = dial(f, center=[0, 3.0, 0], radius=0.72, label="level", color=PHOSPHATE,
                     fmt="" if blank_gauge else "{:.0f}%", scale=100, size=30)
        g.add(gauge)
        g.f_tracker = f
        g.gauge = gauge
    g.left_lane, g.right_lane = left, right
    g.left_head, g.right_head = lh, rh
    g.proteins, g.kinase, g.phosphatase, g.particles = proteins, kin, pho, particles
    return g


def row_cycle_picture(marked=6, gauge_value=0.5, blank_gauge=False):
    pop = population_row(marked)
    kin = flow_arrow([-5.4, 1.15, 0], [-2.7, 1.15, 0], KINASE, "kinase", 7)
    pho = flow_arrow([5.4, 1.15, 0], [2.7, 1.15, 0], PHOSPHATASE, "phosphatase", 7)
    f = ValueTracker(gauge_value)
    gauge = dial(f, center=[0, 2.55, 0], radius=0.9, label="phosphorylation level",
                 color=PHOSPHATE, fmt="" if blank_gauge else "{:.0f}%", scale=100, size=32)
    g = VGroup(pop, kin, pho, gauge)
    g.proteins, g.kinase, g.phosphatase, g.gauge, g.f_tracker = pop, kin, pho, gauge, f
    return g


def balance_plot(box=(-5.8, 4.4, -2.15, 2.35)):
    return Plot(box=box, xr=(0, 5), yr=(0, 1), xticks=[0, 1, 3, 5],
                yticks=[(0, "0"), (0.5, "0.5"), (1, "1")],
                xlabel="kinase rate kK", ylabel="fraction f")


def plot_backdrop(x0, x1, y0, y1, color=PROTEIN):
    """A quiet filled plotting field, large enough to keep plots visually substantial."""
    return RoundedRectangle(corner_radius=0.18, width=x1 - x0 + 0.5, height=y1 - y0 + 0.5,
                            stroke_width=0, fill_color=color, fill_opacity=0.14).move_to(
                                [(x0 + x1) / 2, (y0 + y1) / 2, 0])


def selector(highlight=None, at=[4.95, 2.82, 0]):
    cols = [TEXT, TEXT, PHOSPHATE if highlight == "up" else TEXT]
    opts = VGroup(*[boxed_label(x, c, size=26, pad=0.18,
                                fill_opacity=0.35 if x == highlight else 0.07)
                    for x, c in zip(PREDICT_OPTIONS, cols)])
    opts.arrange(RIGHT, buff=0.18).move_to(at)
    return opts


class S00Hook(SpokenScene):
    def construct(self):
        one = copy_block([0, 0, 0], marked=True, scale=2.5)
        pulse(one[0], base=3.5, amp=1.2, speed=2.0)
        self.play(FadeIn(one, scale=0.8), run_time=0.7)
        self.at("a cell controls")
        pop = population_row(0)
        self.play(FadeOut(one), LaggedStart(*[FadeIn(p, scale=0.6) for p in pop], lag_ratio=0.05), run_time=1.2)
        self.at("If a kinase writes")
        kin = flow_arrow([-5.5, 1.15, 0], [-2.8, 1.15, 0], KINASE, "kinase", 7)
        self.play(FadeIn(kin), *[
            Transform(pop[i], copy_block(pop[i].get_center(), True, 0.92)) for i in (0, 2, 4, 6, 8, 10)
        ], run_time=1.2)
        self.at("why cannot kinase")
        pho = flow_arrow([5.5, 1.15, 0], [2.8, 1.15, 0], PHOSPHATASE, "phosphatase", 7)
        gauge_f = ValueTracker(0.5)
        gauge = dial(gauge_f, center=[0, 2.55, 0], radius=0.9, label="phosphorylation level",
                     color=PHOSPHATE, fmt="", size=32)
        question = T("?", 64, PHOSPHATE, weight=BOLD).move_to([1.25, 2.55, 0])
        self.play(FadeIn(pho), FadeIn(gauge), FadeIn(question, scale=0.6), run_time=1.0)
        self.at("Follow a fixed population")
        self.play(
            *[pop[i].animate.shift(RIGHT * 0.18 if i % 2 else LEFT * 0.18) for i in range(TOTAL)],
            kin[0].animate.set_stroke(width=9), pho[0].animate.set_stroke(width=9),
            rate_func=there_and_back, run_time=2.4,
        )
        self.finish()


class S01Title(TitleCard):
    LESSON = "Phosphorylation switch"
    TITLE = "Two Enzymes Set the Level"

    def construct(self):
        pop = population_row(6, y=-2.25, scale=0.72).set_opacity(0.45)
        kin = flow_arrow([-5.2, -1.35, 0], [-3.0, -1.35, 0], KINASE, "kinase", 5).set_opacity(0.55)
        pho = flow_arrow([5.2, -1.35, 0], [3.0, -1.35, 0], PHOSPHATASE, "phosphatase", 5).set_opacity(0.55)
        lesson = T(self.LESSON.upper(), 22, PROTEIN).move_to([0, 1.52, 0])
        title = fit_text(self.TITLE, max_w=11.4, size=52, font=TITLE_FONT).move_to([0, 0.55, 0])
        rule = Line(LEFT * 1.4, RIGHT * 1.4, color=PHOSPHATE, stroke_width=4).move_to([0, -0.18, 0])
        self.add(pop, kin, pho)
        self.play(FadeIn(lesson), Write(title), GrowFromCenter(rule), run_time=0.65)
        self.play(
            *[Transform(pop[i], copy_block(pop[i].get_center(), i % 3 != 0, 0.72)) for i in range(TOTAL)],
            kin[0].animate.set_stroke(width=8), pho[0].animate.set_stroke(width=8),
            run_time=0.9,
        )
        self.play(FadeOut(VGroup(pop, kin, pho, lesson, title, rule)), run_time=0.45)
        self.finish()


class S02Pools(SpokenScene):
    def construct(self):
        row = population_row(6)
        self.add(row)
        self.at("Divide the population")
        world = lane_world(marked=6, show_gauge=False)
        self.play(FadeOut(row), FadeIn(VGroup(world.left_lane, world.right_lane)), run_time=0.8)
        self.play(FadeIn(world.left_head), FadeIn(world.right_head),
                  LaggedStart(*[FadeIn(p) for p in world.proteins], lag_ratio=0.04), run_time=1.2)
        self.at("The kinase moves")
        self.add(world.particles[0])
        self.play(FadeIn(world.kinase), world.proteins[0].animate.shift(RIGHT * 1.1), run_time=1.2)
        self.play(world.proteins[0].animate.shift(LEFT * 1.1), run_time=0.6)
        self.at("The phosphatase moves")
        self.add(world.particles[1])
        self.play(FadeIn(world.phosphatase), world.proteins[-1].animate.shift(LEFT * 1.1), run_time=1.2)
        self.play(world.proteins[-1].animate.shift(RIGHT * 1.1), run_time=0.6)
        self.at("The total number")
        self.play(FadeIn(world.total),
                  *[p.animate.shift(UP * 0.09 if i % 2 else DOWN * 0.09) for i, p in enumerate(world.proteins)],
                  rate_func=there_and_back, run_time=2.2)
        self.finish()


class S03Rates(SpokenScene):
    def construct(self):
        world = lane_world(marked=6, show_gauge=True)
        self.add(world)
        model = VGroup(*[boxed_label(x, GREY, 24, pad=0.15) for x in
                         ("one site", "fixed pool", "first-order rates")])
        model.arrange(RIGHT, buff=0.2).move_to([0, -3.22, 0])
        self.at("Use the simplest model")
        self.play(LaggedStart(*[FadeIn(x, shift=UP * 0.1) for x in model], lag_ratio=0.2), run_time=1.4)
        eq_in = M("in = kK(1 − f)", 30, KINASE).move_to([-3.55, 2.5, 0])
        eq_out = M("out = kP f", 30, PHOSPHATASE).move_to([3.45, 2.65, 0])
        self.at("Kinase flow depends")
        self.play(FadeOut(model), FadeIn(eq_in), world.kinase[0].animate.set_stroke(width=10), run_time=1.2)
        self.play(world.proteins[1].animate.shift(RIGHT * 0.55), rate_func=there_and_back, run_time=1.3)
        self.at("Phosphatase flow depends")
        self.play(FadeIn(eq_out), world.phosphatase[0].animate.set_stroke(width=10), run_time=1.2)
        self.play(world.proteins[-2].animate.shift(LEFT * 0.55), rate_func=there_and_back, run_time=1.3)
        steady = boxed_label("steady, not static", PHOSPHATE, 30, pad=0.24).move_to([0, -3.18, 0])
        self.at("A steady level appears")
        self.play(world.kinase[0].animate.set_stroke(width=8), world.phosphatase[0].animate.set_stroke(width=8),
                  FadeIn(steady), run_time=1.1)
        self.at("individual copies still cycle")
        self.play(world.proteins[2].animate.shift(RIGHT * 0.7),
                  world.proteins[-3].animate.shift(LEFT * 0.7), rate_func=there_and_back, run_time=1.8)
        self.finish()


class S04Predict(SpokenScene):
    def construct(self):
        world = lane_world(marked=6, kinase_width=8, phosphatase_width=8,
                           show_gauge=True, blank_gauge=True, show_total=False)
        self.add(world)
        self.at("Make a prediction")
        choices = selector()
        self.play(FadeIn(choices), run_time=0.8)
        self.at("Keep kinase activity fixed")
        narrow = flow_arrow([1.16, -0.72, 0], [-1.16, -0.72, 0], PHOSPHATASE, "phosphatase", 3)
        narrow[1].move_to([3.35, -1.62, 0])
        self.play(Transform(world.phosphatase, narrow),
                  world.proteins[0].animate.shift(RIGHT * 0.3),
                  world.proteins[-1].animate.shift(LEFT * 0.18), run_time=1.4)
        q = question_card(PREDICT_QUESTION, y=-3.18, size=30, max_w=9.8)
        self.at("Which way will")
        self.play(FadeIn(q.question),
                  *[p.animate(rate_func=there_and_back).shift(UP * 0.06 if i % 2 else DOWN * 0.06)
                    for i, p in enumerate(world.proteins)], run_time=1.4)
        self.finish()


class S05Pause(PredictPause):
    QUESTION = PREDICT_QUESTION
    OPTIONS = ()
    SECONDS = 4.5
    CARD = {"y": -3.18, "size": 30, "max_w": 9.8}

    def backdrop(self):
        world = lane_world(marked=6, kinase_width=8, phosphatase_width=3,
                           show_gauge=True, blank_gauge=True, show_total=False)
        world.add(selector())
        for i, p in enumerate(world.proteins):
            bob(p, amp=0.035, speed=1.2 + 0.08 * i, seed=i)
        return world


class S06Reveal(SpokenScene):
    def construct(self):
        world = lane_world(marked=6, kinase_width=8, phosphatase_width=3,
                           show_gauge=True, blank_gauge=False, show_total=False)
        choices = selector()
        q = question_card(PREDICT_QUESTION, y=-3.18, size=30, max_w=9.8)
        self.add(world, choices, q.question)
        self.at("The fraction rises")
        up_choices = selector("up")
        self.play(Transform(choices, up_choices), world.f_tracker.animate.set_value(0.64), run_time=1.2)
        self.at("Writing now outruns")
        self.play(world.kinase[0].animate.set_stroke(width=11),
                  world.phosphatase[0].animate.set_stroke(width=3),
                  FadeOut(q.question), run_time=1.0)
        self.play(*[Transform(world.proteins[i], copy_block([*RIGHT_POS[i], 0], True, 0.88))
                    for i in (0, 1)], world.f_tracker.animate.set_value(0.72), run_time=1.6)
        self.at("As that pool grows")
        self.play(world.phosphatase[0].animate.set_stroke(width=5.5),
                  world.proteins[6:].animate(rate_func=there_and_back).shift(DOWN * 0.28),
                  world.proteins[-1].animate(rate_func=there_and_back).shift(LEFT * 0.45), run_time=1.8)
        self.at("A new steady level")
        steady = boxed_label("new steady level", PHOSPHATE, 28, pad=0.22).move_to([0, -3.18, 0])
        self.play(world.phosphatase[0].animate.set_stroke(width=8),
                  world.kinase[0].animate.set_stroke(width=8), world.f_tracker.animate.set_value(0.75),
                  FadeIn(steady), run_time=1.5)
        self.at("Inhibiting an eraser")
        cards = VGroup(boxed_label("kinase up", KINASE, 30, pad=0.28),
                       boxed_label("phosphatase down", PHOSPHATASE, 30, pad=0.28))
        cards.arrange(RIGHT, buff=0.55).move_to([0, -3.08, 0])
        self.play(FadeOut(choices), swap(steady, cards, 1.0),
                  world.proteins[-2].animate(rate_func=there_and_back).shift(LEFT * 0.45), run_time=2.0)
        self.finish()


class S07Curve(SpokenScene):
    def construct(self):
        kp = 1.0
        rule = M("f = kK / (kK + kP)", 34, PHOSPHATE).move_to([-1.0, 3.25, 0])
        fixed = boxed_label("kP fixed", PHOSPHATASE, 28, pad=0.22).move_to([5.35, 1.35, 0])
        P = balance_plot()
        back = plot_backdrop(-5.8, 4.4, -2.15, 2.35)
        computed = scope_tag("computed", color=PROTEIN)
        fn = lambda x: x / (x + kp) if x + kp else 0
        ghost = P.curve(fn, color=PHOSPHATE, width=5, opacity=0.8)
        self.at("The balance has")
        self.play(Write(rule), FadeIn(fixed), FadeIn(back), Create(P), run_time=1.2)
        self.add(ghost)
        g_tr, g_rider = looping_rider(self, P, fn, 0.05, 5, 3.5)
        self.at("At steady state")
        self.play(Indicate(rule, color=PHOSPHATE, scale_factor=1.04), run_time=1.5)
        self.play(rule.animate.scale(1.22), rate_func=there_and_back, run_time=3.2)
        k = ValueTracker(0)
        live = P.live_curve(fn, k, color=PHOSPHATE, width=7)
        dot = P.dot(lambda: k.get_value(), lambda: fn(k.get_value()), color=PHOSPHATE)
        self.at("Compute that rule")
        g_tr.clear_updaters()
        self.remove(g_tr, g_rider, ghost)
        self.play(FadeOut(rule), run_time=0.6)
        self.add(live, dot, computed)
        self.play(k.animate.set_value(5), run_time=3.1, rate_func=linear)
        self.at("The curve rises smoothly")
        ceiling = P.hline(1, "ceiling", GREY)
        self.play(FadeIn(ceiling), k.animate.set_value(4.6), run_time=1.2)
        self.play(k.animate.set_value(5), rate_func=there_and_back, run_time=1.5)
        looping_rider(self, P, fn, 0.0, 5, 3.5, color=TEXT)
        self.finish()


class S08Speed(SpokenScene):
    def construct(self):
        P = Plot(box=(-5.8, 2.5, -2.1, 2.35), xr=(0, 6), yr=(0, 1),
                 xticks=[0, 2, 4, 6], yticks=[(0, "0"), (0.6, "0.6"), (1, "1")],
                 xlabel="time", ylabel="fraction f")
        f0, fss = 0.08, 0.6
        slow = lambda t: fss + (f0 - fss) * np.exp(-0.75 * t)
        fast = lambda t: fss + (f0 - fss) * np.exp(-2.25 * t)
        t = ValueTracker(0)
        slow_curve = P.live_curve(slow, t, color=PROTEIN, width=6)
        fast_curve = P.live_curve(fast, t, color=PHOSPHATE, width=6)
        plateau = P.hline(fss, "same plateau", GREY)
        back = plot_backdrop(-5.8, 2.5, -2.1, 2.35)
        self.at("The same enzymes")
        self.play(FadeIn(back), Create(P), FadeIn(plateau), run_time=1.2)
        self.add(slow_curve, fast_curve, scope_tag("computed", color=PROTEIN))
        p_tr, p_rider = looping_rider(self, P, lambda v: fss, 0.0, 6, 4.0, color=GREY)
        flows = VGroup(flow_arrow([3.35, 1.15, 0], [5.65, 1.15, 0], KINASE, "kinase", 6),
                       flow_arrow([5.65, 0.0, 0], [3.35, 0.0, 0], PHOSPHATASE, "phosphatase", 6))
        self.at("Increase both rates")
        p_tr.clear_updaters()
        self.remove(p_tr, p_rider)
        parts = VGroup(flow_particles([3.45, 1.15, 0], [5.55, 1.15, 0], KINASE),
                       flow_particles([5.55, 0.0, 0], [3.45, 0.0, 0], PHOSPHATASE, 0.4))
        self.play(FadeIn(flows), flows[0][0].animate.set_stroke(width=10),
                  flows[1][0].animate.set_stroke(width=10), run_time=1.2)
        self.add(parts)
        self.at("The steady fraction stays")
        self.play(t.animate.set_value(6), run_time=3.2, rate_func=linear)
        self.at("The population reaches")
        looping_rider(self, P, fast, 0.0, 6, 4.0, color=PHOSPHATE, drops=False)
        looping_rider(self, P, slow, 0.0, 6, 4.0, color=PROTEIN, drops=False)
        slow_lab = T("slower", 27, PROTEIN).move_to(P.pt(3.2, slow(3.2)) + DOWN * 0.35)
        fast_lab = T("faster", 27, PHOSPHATE).move_to(P.pt(1.4, fast(1.4)) + UP * 0.38)
        self.play(FadeIn(slow_lab), FadeIn(fast_lab),
                  flows[0][0].animate.set_stroke(width=12), flows[1][0].animate.set_stroke(width=12),
                  run_time=1.5)
        atp_left = ValueTracker(100)
        atp_count = counter("ATP {:.0f}", atp_left, at=[4.5, -1.45, 0], size=34, color=ATP)
        atp_box = RoundedRectangle(corner_radius=0.15, width=2.6, height=1.0,
                                   stroke_color=ATP, stroke_width=2.5).move_to([4.5, -1.45, 0])
        self.at("Faster cycling spends")
        self.play(FadeIn(atp_box), FadeIn(atp_count), run_time=0.6)
        self.add(atp_count)
        self.play(atp_left.animate.set_value(62),
                  flows[0].animate.shift(RIGHT * 0.08), flows[1].animate.shift(LEFT * 0.08),
                  rate_func=linear, run_time=1.4)
        self.finish()


class S09Signals(SpokenScene):
    def construct(self):
        world = lane_world(marked=6, show_gauge=False, show_total=False)
        self.add(world)
        signal = boxed_label("signal", PHOSPHATE, 30, pad=0.28).move_to([0, 3.15, 0])
        self.at("A signal can act")
        self.play(FadeIn(signal), run_time=0.8)
        branch_l = Arrow(signal.get_bottom() + LEFT * 0.3, [-0.55, 0.82, 0], buff=0.08,
                         color=KINASE, stroke_width=4, tip_length=0.18)
        branch_r = Arrow(signal.get_bottom() + RIGHT * 0.3, [0.55, -0.45, 0], buff=0.08,
                         color=PHOSPHATASE, stroke_width=4, tip_length=0.18)
        self.play(GrowArrow(branch_l), GrowArrow(branch_r), run_time=0.8)
        self.at("activate the kinase")
        self.play(world.kinase[0].animate.set_stroke(width=12),
                  world.proteins[:6].animate(rate_func=there_and_back).shift(DOWN * 0.28), run_time=1.1)
        self.at("inhibit the phosphatase")
        self.play(world.phosphatase[0].animate.set_stroke(width=3),
                  world.proteins[6:].animate(rate_func=there_and_back).shift(DOWN * 0.28), run_time=1.1)
        self.at("later activate the phosphatase")
        shutoff = T("shutoff", 28, PHOSPHATASE).move_to([0, -2.55, 0])
        self.play(world.phosphatase[0].animate.set_stroke(width=12), FadeIn(shutoff),
                  world.proteins.animate(rate_func=there_and_back).shift(DOWN * 0.22), run_time=1.5)
        self.at("Measuring only the writer")
        bracket = VGroup(Line([-1.1, -2.85, 0], [1.1, -2.85, 0], color=KINASE, stroke_width=4),
                         Line([-1.1, -2.7, 0], [-1.1, -3.0, 0], color=KINASE, stroke_width=4),
                         Line([1.1, -2.7, 0], [1.1, -3.0, 0], color=KINASE, stroke_width=4))
        writer_only = T("kinase only", 26, KINASE).next_to(bracket, DOWN, buff=0.1)
        self.play(FadeOut(shutoff), FadeIn(bracket), FadeIn(writer_only),
                  world.proteins.animate(rate_func=there_and_back).shift(DOWN * 0.22), run_time=1.4)
        self.at("Measure the substrate's")
        full_bracket = VGroup(Line([-5.8, -2.85, 0], [5.8, -2.85, 0], color=PHOSPHATE, stroke_width=4),
                              Line([-5.8, -2.7, 0], [-5.8, -3.0, 0], color=PHOSPHATE, stroke_width=4),
                              Line([5.8, -2.7, 0], [5.8, -3.0, 0], color=PHOSPHATE, stroke_width=4))
        all_three = T("substrate + both activities", 28, PHOSPHATE).next_to(full_bracket, DOWN, buff=0.1)
        self.play(Transform(bracket, full_bracket), swap(writer_only, all_three, 0.9),
                  *[p.animate(rate_func=there_and_back).shift(UP * 0.06 if i % 2 else DOWN * 0.06)
                    for i, p in enumerate(world.proteins)], run_time=1.6)
        self.finish()


class S10Scope(SpokenScene):
    def construct(self):
        frame = RoundedRectangle(corner_radius=0.18, width=9.8, height=6.2,
                                 stroke_color=PHOSPHATE, stroke_width=4,
                                 fill_color=PHOSPHATE, fill_opacity=0.12).move_to([-1.55, 0.05, 0])
        title = T("simple first-order cycle", 30, PHOSPHATE).move_to([-1.65, 2.78, 0])
        P = Plot(box=(-5.55, 1.95, -1.75, 1.5), xr=(0, 5), yr=(0, 1),
                 xticks=[0, 5], yticks=[(0, "0"), (0.5, "0.5"), (1, "1")],
                 xlabel="kinase rate", ylabel="fraction")
        P.xlabel.shift(DOWN * 0.1)
        P.ylabel.move_to([-4.55, 1.55, 0])
        self.at("Keep the model's boundary")
        self.play(Create(frame), FadeIn(title), run_time=1.0)
        assumptions = VGroup(*[boxed_label(x, PROTEIN, 24, pad=0.14) for x in
                               ("fixed pool", "single site", "first-order rates")])
        assumptions.arrange(RIGHT, buff=0.18).move_to([-1.65, 2.15, 0])
        self.at("It assumes a fixed pool")
        x = ValueTracker(0)
        live_curve = P.live_curve(lambda v: v / (v + 1), x, color=PHOSPHATE, width=7)
        dot = P.dot(lambda: x.get_value(), lambda: x.get_value() / (x.get_value() + 1), color=PHOSPHATE)
        self.play(Create(P), LaggedStart(*[FadeIn(a) for a in assumptions], lag_ratio=0.22), run_time=1.2)
        self.add(live_curve, dot)
        self.play(x.animate(rate_func=linear).set_value(5),
                  assumptions.animate(rate_func=there_and_back).shift(RIGHT * 0.35), run_time=3.0)
        looping_rider(self, P, lambda v: v / (v + 1), 0.0, 5, 4.0)
        ys = [1.75, 0.55, -0.65, -1.85]
        names = ("saturation", "multiple sites", "feedback", "turnover")
        extensions = VGroup()
        for y, name in zip(ys, names):
            icon = Circle(radius=0.16, color=GREY, stroke_width=3).move_to([3.38, y, 0])
            lab = T(name, 25, GREY).move_to([4.75, y, 0])
            extensions.add(VGroup(icon, lab))
        self.at("Saturated enzymes")
        self.play(FadeIn(extensions[0]), run_time=0.7)
        self.at("several sites")
        self.play(FadeIn(extensions[1]), run_time=0.6)
        self.at("feedback or protein turnover")
        self.play(FadeIn(extensions[2]), FadeIn(extensions[3]), run_time=1.0)
        self.at("Start with the simple balance")
        self.play(extensions.animate.set_opacity(0.28), Indicate(frame, color=PHOSPHATE, scale_factor=1.01),
                  P.axes.animate.set_stroke(width=5), run_time=1.8)
        self.finish()


class S11Keep(SpokenScene):
    def construct(self):
        world = row_cycle_picture(marked=6, gauge_value=0.5)
        self.add(world)
        self.at("When phosphorylation rises")
        self.play(world.f_tracker.animate.set_value(0.7),
                  *[Transform(world.proteins[i], copy_block(world.proteins[i].get_center(), True, 0.92))
                    for i in (7, 9)], run_time=1.4)
        both = T("what changed on both sides?", 34, PHOSPHATE).move_to([0, -1.6, 0])
        self.at("ask what changed")
        self.play(FadeIn(both), run_time=0.8)
        self.at("More kinase activity")
        self.play(world.kinase.animate.set_opacity(1), world.phosphatase.animate.set_opacity(0.25),
                  world.kinase[0].animate.set_stroke(width=11),
                  world.proteins[:6].animate(rate_func=there_and_back).shift(UP * 0.3), run_time=1.5)
        self.at("Less phosphatase activity")
        self.play(world.kinase.animate.set_opacity(0.25), world.phosphatase.animate.set_opacity(1),
                  world.phosphatase[0].animate.set_stroke(width=3),
                  world.proteins[6:].animate(rate_func=there_and_back).shift(DOWN * 0.3), run_time=1.6)
        self.at("The observed level belongs")
        self.play(world.kinase.animate.set_opacity(1), world.phosphatase.animate.set_opacity(1),
                  world.kinase[0].animate.set_stroke(width=8), world.phosphatase[0].animate.set_stroke(width=8),
                  world.gauge.animate.scale(1.1), FadeOut(both), run_time=1.5)
        self.at("That is why the substrate")
        final = T("measure the cycle", 48, PHOSPHATE, font=TITLE_FONT)
        self.play(FadeOut(world), run_time=0.65)
        self.play(FadeIn(final, scale=0.85), run_time=0.9)
        self.finish()


class S12End(EndCard):
    LINE = "Phosphorylation level depends on both the kinase and the phosphatase."
