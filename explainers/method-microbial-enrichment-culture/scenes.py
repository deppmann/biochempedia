"""Sorting Microbes by How They Live, timed to the supplied narration.

BLUE is glass and apparatus, GREY is structure, TEAL is the liquid,
GREEN is nitrogen fixation, ORANGE is fermentation, PURPLE is archaea,
YELLOW is the measured result, RED marks a pitfall, and GOLD is a question.
"""
from bp_parts import *

PURPLE = "#B58CD9"
ORANGE = "#F29E4C"
MIX = (TEAL, GREEN, ORANGE, PURPLE, BLUE)
QUESTION = "How many days for 9 doublings?"
INPUTS = ("9 × 20 days", "Lag phase: 30–60 days")
DAYS = 20
GENERATIONS = 9
LAG = (30, 60)
HOURS = 3
GROWTH_DAYS = GENERATIONS * DAYS
TOTAL_DAYS = tuple(GROWTH_DAYS + lag for lag in LAG)
FRACTION = HOURS / (DAYS * 24)
FOLD = 2 ** FRACTION


def p(x, y):
    return np.array([x, y, 0.0])


def label(words, x, y, color=TEXT, size=32):
    return T(words, size, color).move_to(p(x, y))


def badge(words, x, y, color=TEXT, *, pad=0.22):
    return boxed_label(words, color=color, size=29, pad=pad).move_to(p(x, y))


def bench():
    return VGroup(
        Rectangle(width=13.4, height=1.26, stroke_width=0,
                  fill_color="#384658", fill_opacity=1).move_to(p(0, -2.27)),
        Rectangle(width=13.4, height=0.15, stroke_width=0,
                  fill_color=BLUE, fill_opacity=0.5).move_to(p(0, -2.97)),
    )


def cell(color, radius, angle=0):
    return Ellipse(width=radius * 2.6, height=radius * 1.55,
                   stroke_color=color, stroke_width=2,
                   fill_color=color, fill_opacity=0.78).rotate(angle)


class Culture(VGroup):
    """The same flat-sided glass vessel, with drifting schematic cell populations."""

    def __init__(self, x=0, width=6.4, colors=MIX, count=25):
        self.clock = 0.0
        self.x = x
        self.inner = width / 2 - 0.26
        stub = RoundedRectangle(width=width, height=4.68, corner_radius=0.32,
                                fill_color="#263C52", fill_opacity=1,
                                stroke_color=BLUE, stroke_width=4).move_to(p(x, -0.12))
        water = Polygon(*[p(x + dx, y) for dx, y in [
            (-self.inner, -2.17), (self.inner, -2.17), (self.inner, 1.04),
            (-self.inner, 1.04)]], stroke_width=0, fill_color="#326579", fill_opacity=1)
        surface = VMobject(stroke_width=5, stroke_color=TEAL)
        ribbon = VMobject(stroke_width=0, fill_color="#659BA5", fill_opacity=0.62)
        glints = VGroup(*(Line(LEFT, RIGHT, stroke_color=TEAL, stroke_width=4)
                          for _ in range(3)))
        rim = RoundedRectangle(width=width + 0.26, height=0.2, corner_radius=0.09,
                               stroke_color=BLUE, stroke_width=3,
                               fill_color="#456987", fill_opacity=1).move_to(p(x, 2.22))
        shine = Line(p(x - self.inner, -1.9), p(x - self.inner, 1.87),
                     stroke_color=BLUE, stroke_width=6).set_opacity(0.45)
        self.landmarks = VGroup(stub, water, ribbon, glints, surface, shine, rim)
        self.cells = VGroup()
        super().__init__(self.landmarks, self.cells)
        self.add_population(colors, count)
        xs = np.linspace(-self.inner, self.inner, 21)

        def move_water(curve, dt):
            self.clock += dt
            top = [p(x + dx, 1.04 + 0.22 * np.sin(2.5 * dx - 3.1 * self.clock)) for dx in xs]
            curve.set_points_smoothly(top)
            water.set_points_as_corners([p(x - self.inner, -2.17), p(x + self.inner, -2.17),
                                         *reversed(top), p(x - self.inner, -2.17)])
            band = [p(x + dx, 0.49 + 0.14 * np.sin(2.5 * dx - 3.1 * self.clock)) for dx in xs]
            lower = [q + DOWN * (0.21 + 0.08 * np.cos(q[0] - self.clock)) for q in band]
            ribbon.set_points_as_corners([*band, *reversed(lower), band[0]])
            for i, glint in enumerate(glints):
                offset = 0.59 * self.inner * np.sin(1.8 * self.clock + 2.1 * i)
                glint.put_start_and_end_on(p(x + offset - 0.40, -0.89 + 0.26 * i),
                                           p(x + offset + 0.40, -0.74 + 0.26 * i))

        surface.add_updater(move_water, call_updater=True)

    def add_population(self, colors, count, seed=22, visible=True):
        rng = np.random.default_rng(seed)
        new = VGroup()
        rows = 4 if count > 10 else 2
        cols = max(1, int(np.ceil(count / rows)))
        for i in range(count):
            color = colors[i % len(colors)]
            dx = (i % cols - (cols - 1) / 2) * 1.55 * self.inner / cols
            dy = (i // cols - (rows - 1) / 2) * 2.7 / rows - 0.5
            origin = p(self.x + dx + rng.uniform(-0.12, 0.12), dy + rng.uniform(-0.13, 0.13))
            phase = rng.uniform(0, TAU)
            microbe = cell(color, rng.uniform(0.14, 0.23), rng.uniform(-1, 1))
            microbe.population_color = color

            def drift(mob, origin=origin, phase=phase):
                t = self.clock
                mob.move_to(origin + p(0.31 * np.sin(1.2 * t + phase),
                                       0.23 * np.cos(1.6 * t + phase)))

            microbe.add_updater(drift, call_updater=True)
            if not visible:
                microbe.set_opacity(0)
            new.add(microbe)
        self.cells.add(*new)
        return new

    def set_selection(self, color, populations):
        for microbe in self.cells:
            microbe.set_opacity(0.86 if microbe.population_color == color else 0.09)
        for count, seed in populations:
            self.add_population((color,), count, seed)

    def select(self, color, count, seed):
        incoming = self.add_population((color,), count, seed, visible=False)
        return AnimationGroup(
            *(m.animate.set_opacity(0.82 if m.population_color == color else 0.09)
              for m in self.cells if m not in incoming),
            LaggedStart(*(m.animate.set_opacity(0.86) for m in incoming), lag_ratio=0.16),
        )


def bubbles(x, color=BLUE):
    group = VGroup()
    for i in range(12):
        bubble = Circle(radius=0.05 + 0.025 * (i % 4), color=color, stroke_width=2)
        bubble.time = i / 12

        def rise(mob, dt, i=i):
            mob.time = (mob.time + dt * (0.27 + 0.03 * (i % 3))) % 1
            mob.move_to(p(x + 0.82 * np.sin(i * 1.8) + 0.10 * np.sin(TAU * mob.time),
                          -1.83 + 2.72 * mob.time))
            mob.set_stroke(opacity=0.8 * np.sin(PI * mob.time) ** 0.5)

        bubble.add_updater(rise, call_updater=True)
        group.add(bubble)
    return group


def lens(x=0, y=0.08, two=False):
    frame = Circle(radius=2.36, stroke_color=BLUE, stroke_width=6,
                   fill_color="#274B65", fill_opacity=1).move_to(p(x, y))
    inner = Circle(radius=2.17, stroke_color=TEAL, stroke_width=2).move_to(frame)
    illumination = Ellipse(width=3.66, height=1.15, fill_color="#426E86",
                           fill_opacity=1, stroke_width=0).move_to(p(x, y - 0.15))
    bob(illumination, amp=0.64, speed=2.7)
    cells = VGroup()
    locations = [(-0.92, 0.16), (0.92, 0.16)] if two else [
        (-0.95, 0.85), (0.63, 1.02), (1.15, -0.52), (-0.62, -0.60), (0.13, 0.16)]
    for i, (dx, dy) in enumerate(locations):
        microbe = cell(TEAL, 0.54 if two else 0.33, -0.31).move_to(p(x + dx, y + dy))
        cells.add(bob(microbe, amp=0.36, speed=2.7, seed=i * 2))
    return VGroup(frame, inner, illumination, cells)


def selector(value, x, y, name, color):
    controls = dial(value, p(x, y), radius=0.79, color=color)
    # A qualitative selector has a needle and named positions, without percentages.
    controls.remove(controls[2], controls[1], controls[3])
    needle = Line(p(x, y), p(x + 0.65, y), color=TEXT, stroke_width=4)

    def turn(mob):
        angle = PI * (1 - value.get_value())
        mob.put_start_and_end_on(p(x, y), p(x + 0.66 * np.cos(angle), y + 0.66 * np.sin(angle)))

    needle.add_updater(turn, call_updater=True)
    controls.add(needle, label(name, x, y - 0.36, color, 28))
    return controls


def calendar(x, y, day):
    page = RoundedRectangle(width=2.65, height=1.03, corner_radius=0.12,
                            fill_color="#273C55", fill_opacity=1,
                            stroke_color=BLUE, stroke_width=3).move_to(p(x, y))
    display = counter("Day {:.0f}", day, at=p(x, y - 0.12), size=28, color=TEXT)
    tabs = VGroup(*[RoundedRectangle(width=0.13, height=0.31, corner_radius=0.05,
                                     stroke_width=0, fill_color=BLUE, fill_opacity=1)
                    .move_to(p(x + dx, y + 0.29)) for dx in (-0.73, 0.73)])
    return VGroup(page, tabs, display)


def undated_calendar(x, y):
    icon = calendar(x, y, ValueTracker(0))
    icon.remove(icon[-1])
    for i in range(3):
        for j in range(2):
            icon.add(Dot(p(x + (i - 1) * 0.26, y - 0.04 - 0.22 * j), radius=0.045, color=BLUE))
    return icon


def slow_dish(count=1):
    return Culture(3.43, 5.9, (PURPLE,), count)


def predict_backdrop():
    dish = slow_dish()
    day = calendar(3.43, 2.94, ValueTracker(0))
    plate = bench()
    blank = badge("?", -3.38, -1.14, GOLD)
    return VGroup(plate, dish, day, blank)


def predict_card():
    q = question_card(QUESTION, INPUTS, y=2.92, size=31, chip_size=29,
                      chips_at=p(-3.38, 0.28), max_w=5.9)
    q.question.move_to(p(-3.38, 2.92))
    return q


class S01Hook(SpokenScene):
    def construct(self):
        dish = Culture(count=0)
        self.add(bench(), dish, scope_tag())
        self.at("how do you")
        drop = cell(BLUE, 0.24, PI / 2).move_to(p(0, 3.17))
        self.play(FadeIn(drop), run_time=0.25)
        self.play(drop.animate.move_to(p(0, 0.97)), run_time=0.7, rate_func=rate_functions.ease_in_quad)
        crowd = dish.add_population(MIX, 25, visible=False)
        self.play(FadeOut(drop), LaggedStart(*(m.animate.set_opacity(0.86) for m in crowd),
                                             lag_ratio=0.12), run_time=1.4)
        self.at("soil seawater")
        mark = label("?", 0, 1.68, GOLD, 55)
        self.play(GrowFromCenter(mark), run_time=0.45)
        self.at("under a microscope")
        inset = lens()
        self.play(FadeOut(mark), run_time=0.27)
        self.play(FadeIn(inset, scale=0.78), run_time=0.56)
        self.finish()


class S02Title(TitleCard):
    LESSON = "Microbial Enrichment Culture"
    TITLE = "Sorting Microbes by How They Live"

    def construct(self):
        dish = Culture()
        self.add(bench(), dish)
        title = fit_text(self.TITLE, max_w=9.4, size=47, min_size=40, font=TITLE_FONT)
        title.move_to(p(0, 3.02))
        lesson = label(self.LESSON, 0, -2.70, TEXT, 28)
        card = VGroup(title, lesson)
        self.play(FadeIn(card), run_time=0.42)
        self.wait(self.beat(0.54))
        self.play(FadeOut(card), run_time=0.42)
        self.finish()


class S03Recipe(SpokenScene):
    def construct(self):
        dish = Culture()
        food, oxygen = ValueTracker(0.36), ValueTracker(0.65)
        nutrient = selector(food, -5.03, 0.38, "Nutrient", ORANGE)
        valve = selector(oxygen, 5.03, 0.38, "Oxygen", BLUE)
        self.add(bench(), dish, scope_tag())
        self.at("you change the world")
        self.play(FadeIn(nutrient, shift=RIGHT * 0.3), run_time=0.53)
        self.play(FadeIn(valve, shift=LEFT * 0.3), run_time=0.53)
        self.at("set conditions")
        self.play(food.animate.set_value(0.88), oxygen.animate.set_value(0.23), run_time=0.8)
        self.at("let growth separate")
        self.play(dish.select(TEAL, 11, 71), run_time=2.5)
        self.at("that is enrichment")
        rule = caption("Enrichment culture", size=37, color=TEAL, y=3.02).move_to(p(0, 3.02))
        self.play(FadeIn(rule), run_time=0.42)
        self.at("able to use them")
        self.play(dish.select(TEAL, 9, 94), run_time=2.0)
        self.finish()


class S04Conditions(SpokenScene):
    def construct(self):
        dish = Culture()
        dish.set_selection(TEAL, [(11, 71), (9, 94)])
        food, oxygen = ValueTracker(0.88), ValueTracker(0.23)
        self.add(bench(), dish, scope_tag(), selector(food, -5.03, 0.38, "Nutrient", ORANGE),
                 selector(oxygen, 5.03, 0.38, "Oxygen", BLUE))
        self.at("change the recipe")
        self.play(food.animate.set_value(0.53),
                  *(m.animate.set_opacity(0.45 if i < 25 else 0.07)
                    for i, m in enumerate(dish.cells)), run_time=1.3)
        self.at("make nitrogen gas")
        gas_label = badge("N₂ only", -5.03, -1.03, GREEN)
        gas = bubbles(0, GREEN)
        self.play(FadeIn(gas_label), FadeIn(gas), run_time=0.7)
        self.at("only fixers")
        enzyme = badge("Nitrogenase", 0, 2.96, GREEN)
        self.play(dish.select(GREEN, 17, 58), FadeIn(enzyme), run_time=2.75)
        self.at("into ammonia")
        result = badge("Ammonia", 0, 2.96, GREEN)
        self.play(swap(enzyme, result, run_time=0.64))
        self.at("cut oxygen")
        gut = badge("Gut food", -5.03, -1.03, ORANGE)
        closed = badge("No oxygen", 5.03, -1.03, BLUE)
        self.play(FadeOut(gas), FadeOut(result), swap(gas_label, gut, run_time=0.85),
                  oxygen.animate.set_value(0.015), food.animate.set_value(0.92), run_time=0.92)
        self.play(FadeIn(closed), run_time=0.28)
        self.at("ferment food")
        self.play(dish.select(ORANGE, 25, 48), run_time=3.5)
        self.at("the goal is")
        rest = [m for m in dish.cells if m.population_color != ORANGE]
        isolate = badge("Isolate: one kind alone", 0, 2.96, ORANGE)
        self.play(*(m.animate.set_opacity(0) for m in rest), FadeIn(isolate), run_time=1.25)
        self.finish()


class S05ClockSetup(SpokenScene):
    def construct(self):
        plate = bench()
        first = Culture(colors=(ORANGE,))
        self.add(plate, first, scope_tag())
        self.at("stop too soon")
        fast, slow = Culture(-3.43, 5.9, (TEAL,), 1), slow_dish()
        self.play(FadeOut(first), run_time=0.34)
        self.play(FadeIn(fast, shift=LEFT * 0.3), FadeIn(slow, shift=RIGHT * 0.3), run_time=0.8)
        hours, days, generations = ValueTracker(0), ValueTracker(0), ValueTracker(0)
        time = counter("{:.1f} hours", hours, at=p(-3.43, 2.93), size=31, color=BLUE)
        day = calendar(3.43, 2.94, days)
        self.at("growth is set")
        clock = Circle(radius=0.48, color=BLUE, stroke_width=3).move_to(p(-5.22, 2.93))
        hand = Line(p(-5.22, 2.93), p(-5.22, 3.28), color=TEXT, stroke_width=3)

        def clock_hand(mob):
            angle = PI / 2 - TAU * hours.get_value() / 12
            mob.put_start_and_end_on(p(-5.22, 2.93), p(-5.22, 2.93) + 0.36 * p(np.cos(angle), np.sin(angle)))

        hand.add_updater(clock_hand)
        self.play(FadeIn(clock), FadeIn(hand), FadeIn(time), FadeIn(day), run_time=0.6)
        self.at("the gut bacterium")
        name = label("E. coli", -3.43, 1.64, TEAL, 34)
        n = counter("{:.0f} doublings", generations, at=p(-3.43, -2.74), color=TEAL, size=28)
        self.play(FadeIn(name), FadeIn(n), run_time=0.52)
        self.at("finishes nine doublings")
        drift = fast.add_population((TEAL,), 43, 68, visible=False)
        self.play(hours.animate.set_value(HOURS), generations.animate.set_value(GENERATIONS),
                  LaggedStart(*(m.animate.set_opacity(0.85) for m in drift), lag_ratio=0.15),
                  rate_func=linear, run_time=1.4)
        self.at("a slow microbe")
        slow_name = label("MK-D1", 3.43, 1.64, PURPLE, 34)
        self.play(FadeIn(slow_name), run_time=0.6)
        self.at("mkd1 needs")
        daughter = slow.add_population((PURPLE,), 1, 88, visible=False)
        daughter[0].clear_updaters()
        daughter[0].move_to(slow.cells[0].get_center())
        destination = daughter[0].get_center() + RIGHT * 0.53
        self.play(days.animate.set_value(DAYS), run_time=1.5, rate_func=linear)
        self.play(daughter[0].animate.move_to(destination).set_opacity(0.85), run_time=0.63)
        self.finish()


class S06PredictQ(SpokenScene):
    def construct(self):
        backdrop = predict_backdrop()
        plate, dish, day, blank = backdrop
        q = predict_card()
        previous_day = calendar(3.43, 2.94, ValueTracker(DAYS))
        self.add(plate, dish, previous_day, scope_tag(), label("MK-D1", 3.43, 1.64, PURPLE, 34))
        self.at("picture mkd1")
        previous_day[-1].clear_updaters()
        day[-1].clear_updaters()
        self.play(FadeOut(previous_day), run_time=0.28)
        self.play(FadeIn(day), run_time=0.35)
        self.at("needing those same")
        self.play(FadeIn(q.chips[0]), run_time=0.55)
        self.at("reported lag phase")
        self.play(FadeIn(q.chips[1]), run_time=0.6)
        self.at("how many days")
        self.play(FadeIn(q.question), FadeIn(blank), run_time=0.62)
        self.finish()


class S07PredictPause(PredictPause):
    SECONDS = 4.5

    def construct(self):
        plate, dish, day, blank = predict_backdrop()
        dish.suspend_updating()
        # Match the spoken scene's final composition, with the question held still.
        self.add(plate, dish, day, blank, predict_card(), scope_tag(),
                 label("MK-D1", 3.43, 1.64, PURPLE, 34))
        self.wait(self.SECONDS)


def measure_bar(x, y, width, fraction, color):
    base = RoundedRectangle(width=width, height=0.32, corner_radius=0.12,
                            stroke_color=BLUE, stroke_width=2,
                            fill_color="#3E617E", fill_opacity=1).move_to(p(x, y))
    left = x - width / 2
    fill = Rectangle(width=width * fraction, height=0.31, stroke_width=0,
                     fill_color=color, fill_opacity=1).move_to(p(left + width * fraction / 2, y))
    return VGroup(base, fill)


class S08PredictReveal(SpokenScene):
    def construct(self):
        plate, dish, day, blank = predict_backdrop()
        days = ValueTracker(0)
        running_day = calendar(3.43, 2.94, days)
        q = predict_card()
        name = label("MK-D1", 3.43, 1.64, PURPLE, 34)
        self.add(plate, dish, day, name, blank, q, scope_tag())
        self.at("9 doublings times")
        self.play(FadeOut(q.question), run_time=0.36)
        self.at("equals 180")
        growth = badge(f"9 × 20 days = {GROWTH_DAYS} days", -3.38, 2.93, TEXT)
        self.play(FadeOut(q.chips[0]), FadeIn(growth), run_time=0.64)
        self.at("add the 30")
        lag = badge("+ 30 to 60 days (lag)", -3.38, 0.28, TEXT)
        self.play(swap(q.chips[1], lag))
        self.at("gives about")
        total = badge(f"{TOTAL_DAYS[0]} to {TOTAL_DAYS[1]} days", -3.38, -1.14, YELLOW)
        self.play(swap(blank, total, run_time=0.72))
        self.remove(day)
        self.add(running_day)
        self.play(days.animate.set_value(LAG[0]), run_time=0.4, rate_func=linear)
        growth_cells = dish.select(PURPLE, 21, 71)
        added_cells = dish.cells[1:]
        self.play(days.animate.set_value(TOTAL_DAYS[0]), growth_cells,
                  run_time=1.4, rate_func=linear)
        self.at("3 hours is")
        self.play(FadeOut(growth), FadeOut(lag), FadeOut(total), FadeOut(running_day),
                  *(m.animate.set_opacity(0) for m in added_cells), run_time=0.38)
        dish.cells.remove(*added_cells)
        duration = label("One 20-day doubling", -3.38, 2.94, BLUE)
        bar = measure_bar(-3.32, 1.8, 5.15, FRACTION, YELLOW)
        dot = Dot(p(-5.895 + 5.15 * FRACTION, 1.8), radius=0.044, color=YELLOW)
        lead = Line(dot.get_center() + DOWN * 0.06, p(-5.63, 1.07), color=YELLOW, stroke_width=2)
        tiny = label("3 hours", -5.16, 0.82, YELLOW, 28)
        self.play(FadeIn(duration), FadeIn(bar), FadeIn(dot), Create(lead), FadeIn(tiny), run_time=1.07)
        self.at("mkd1 grows only")
        fold = label(f"MK-D1 in 3 hours: ~{FOLD:.3f}×", -3.38, -1.35, PURPLE, 29)
        comparison = measure_bar(-3.32, -2.02, 5.15, FOLD - 1, PURPLE)
        scale = VGroup(label("1×", -5.9, -2.44, TEXT, 28),
                       label("2×", -0.74, -2.44, TEXT, 28))
        self.play(FadeIn(fold), FadeIn(comparison), FadeIn(scale), run_time=1.1)
        self.finish()


class S09Controls(SpokenScene):
    def construct(self):
        dish = Culture(count=0)
        self.add(bench(), dish, scope_tag())
        self.at("stopping too soon")
        time = badge("3 hours", 0, 2.97, BLUE)
        self.play(FadeIn(time), run_time=0.5)
        self.at("slow growers")
        early = badge("Too early", 0, -3.45, RED, pad=0.12)
        early.box.set_fill(BG, opacity=1)
        self.play(FadeIn(early), run_time=0.55)
        self.at("a second trap")
        comparison = lens(two=True)
        self.play(FadeOut(time), FadeOut(early), run_time=0.30)
        self.play(FadeOut(dish), FadeIn(comparison, scale=0.76), run_time=0.65)
        self.at("say a rumen")
        source = label("Rumen culture", 0, 2.98, BLUE)
        self.play(FadeIn(source), run_time=0.48)
        self.at("a methanogen")
        left = label("Methanogen", -4.65, 0.86, PURPLE, 29)
        self.play(FadeIn(left), run_time=0.48)
        self.at("and the bacterium")
        right = label("E. coli:\nbacterium", 4.77, 0.78, TEAL, 29)
        self.play(FadeIn(right), run_time=0.48)
        self.at("different domains")
        archaeon = label("Archaea", -4.65, 0.18, PURPLE, 28)
        self.play(FadeIn(archaeon), run_time=0.55)
        self.at("looks alone")
        mark = label("?", 0, 1.53, GOLD, 51)
        self.play(GrowFromCenter(mark), run_time=0.5)
        self.at("other tests")
        arrow = Arrow(p(2.12, -0.96), p(3.72, -0.96), buff=0, color=GOLD)
        tests = label("Other tests", 4.73, -0.96, GOLD, 28)
        self.play(GrowArrow(arrow), FadeIn(tests), run_time=0.7)
        self.finish()


def slow_plot():
    plot = Plot(box=(-5.15, -0.16, -1.88, 1.52), xr=(0, 240), yr=(0, 530),
                xticks=[0, 60, 120, 180, 240], yticks=[128, 256, 512],
                xlabel="Days", ylabel="Relative cell count", color=TEXT, size=28, label_size=28)
    return plot


class S10Unlocked(SpokenScene):
    def construct(self):
        dish = Culture()
        self.add(bench(), dish, scope_tag())
        self.at("hidden players")
        self.play(dish.select(PURPLE, 12, 76), run_time=2.05)
        self.at("in nitrification")
        oxygen = ValueTracker(0.22)
        valve = selector(oxygen, 5.03, 0.38, "Oxygen", BLUE)
        food = selector(ValueTracker(0.78), -5.03, 0.38, "Ammonia", ORANGE)
        self.play(FadeIn(valve), FadeIn(food), run_time=0.6)
        self.at("oxygen requiring")
        self.play(oxygen.animate.set_value(0.93), run_time=1.1)
        self.at("oxidize ammonia")
        steps = [badge(word, x, 2.98, YELLOW) for word, x in
                 [("Ammonia", -3.18), ("Nitrite", 0), ("Nitrate", 3.18)]]
        self.play(FadeIn(steps[0]), run_time=0.36)
        self.at("through nitrite")
        arrow1 = Arrow(steps[0].get_right() + RIGHT * 0.15,
                       steps[1].get_left() + LEFT * 0.15, buff=0, color=YELLOW)
        self.play(GrowArrow(arrow1), FadeIn(steps[1]), run_time=0.42)
        self.at("to nitrate")
        arrow2 = Arrow(steps[1].get_right() + RIGHT * 0.15,
                       steps[2].get_left() + LEFT * 0.15, buff=0, color=YELLOW)
        self.play(GrowArrow(arrow2), FadeIn(steps[2]), run_time=0.49)
        self.at("in 2005")
        paper = badge("Könneke and colleagues, 2005", 0, 2.98, GOLD)
        self.play(*(FadeOut(m) for m in [*steps, arrow1, arrow2]), run_time=0.4)
        self.play(FadeIn(paper), run_time=0.64)
        self.at("marine isolate")
        isolate = badge("Marine archaeal isolate", 0, -3.45, PURPLE, pad=0.12)
        isolate.box.set_fill(BG, opacity=1)
        self.play(dish.select(PURPLE, 17, 42), FadeIn(isolate), run_time=2.7)
        self.at("and cultures of")
        self.play(*(FadeOut(m) for m in (food, valve, paper, isolate)), run_time=0.36)
        slow = slow_dish()
        day = ValueTracker(0)
        cal = calendar(3.43, 2.94, day)
        name = label("MK-D1: 20-day doubling", -3.0, 2.97, PURPLE, 32)
        plot = slow_plot()
        growth = lambda t: 2 ** (max(0, t - LAG[1]) / DAYS)
        curve = plot.live_curve(growth, day, color=PURPLE)
        point = plot.dot(day.get_value, lambda: growth(day.get_value()), color=PURPLE, radius=0.07)
        lag = label("60-day lag shown", -3.05, 2.30, TEXT, 28)
        self.play(swap(dish, slow, run_time=0.58), FadeIn(plot), FadeIn(cal), run_time=0.70)
        self.play(FadeIn(name), FadeIn(lag), run_time=0.45)
        self.add(curve, point)
        self.play(day.animate.set_value(LAG[1]), run_time=1.18, rate_func=linear)
        self.play(day.animate.set_value(TOTAL_DAYS[1]), slow.select(PURPLE, 18, 83),
                  run_time=3.52, rate_func=linear)
        self.finish()


class S11Return(SpokenScene):
    def construct(self):
        dish = Culture()
        oxygen, food = ValueTracker(0.93), ValueTracker(0.78)
        valve = selector(oxygen, 5.03, 0.38, "Oxygen", BLUE)
        nutrient = selector(food, -5.03, 0.38, "Nutrient", ORANGE)
        self.add(bench(), dish, valve, nutrient, scope_tag())
        self.at("dish only catches")
        self.play(dish.select(PURPLE, 10, 72), run_time=3.15)
        self.at("low oxygen sediments")
        low = badge("Low oxygen", 5.03, -1.03, BLUE)
        denit = badge("Denitrification", 0, 2.96, YELLOW)
        sediment = RoundedRectangle(width=5.58, height=0.55, corner_radius=0.15,
                                    stroke_width=0, fill_color="#936952", fill_opacity=1).move_to(p(0, -1.91))
        self.play(oxygen.animate.set_value(0.14), FadeIn(low), FadeIn(sediment),
                  dish.select(ORANGE, 14, 72), run_time=0.95)
        self.play(FadeIn(denit), run_time=0.54)
        self.at("reducing nitrate")
        nitrate = label("Nitrate → gases", 0, 1.66, YELLOW, 31)
        gas = bubbles(0, YELLOW)
        self.play(FadeIn(nitrate), FadeIn(gas), run_time=0.8)
        self.at("while oxygenated")
        nitrif = badge("Nitrification", 0, 2.96, YELLOW)
        air = badge("Oxygen", 5.03, -1.03, BLUE)
        self.play(FadeOut(nitrate), FadeOut(gas), FadeOut(denit), FadeOut(sediment),
                  run_time=0.32)
        self.play(swap(low, air), FadeIn(nitrif), oxygen.animate.set_value(0.91),
                  dish.select(PURPLE, 10, 80), run_time=1.2)
        self.at("match the recipe")
        cal = undated_calendar(0, 2.94)
        self.play(swap(nitrif, cal), food.animate.set_value(0.86), run_time=0.62)
        self.at("the ability you seek")
        others = [m for m in dish.cells if m.population_color != PURPLE]
        self.play(dish.select(PURPLE, 22, 49), run_time=1.55)
        self.play(*(m.animate.set_opacity(0) for m in others), run_time=0.45)
        self.finish()


class S12End(EndCard):
    LINE = "Set conditions only one microbe can exploit, so growth isolates it."
