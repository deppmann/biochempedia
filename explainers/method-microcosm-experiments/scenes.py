"""Ecosystems in a Flask, timed to the supplied word alignment.

COLOR MAP (from the shared palette and the patch-clamp reference)
  BLUE glass apparatus and fresh medium; GREY bench and barriers
  TEAL water; GREEN slow grower and primary grazer food; ORANGE fast grower and oranges
  PURPLE a second ciliate or algal clone, and predator traces; GOLD dates and question
"""
from bp_parts import *
from bp_style import EndCard

ORANGE = "#F29E4C"
PURPLE = "#B58CD9"
WATER = "#305E73"
GLASS = "#253D4A"
SLATE = "#263449"
SHADOW = "#172532"
LIME = "#C7DF7F"

SLOW, FAST = GREEN, ORANGE
QUESTION = "Slow grower or faster grower?"
QUESTION_Y = -3.23
LOW, HIGH = 0.13, 0.67


def point(x, y):
    return np.array([x, y, 0.0])


def label(text, x, y, color=TEXT, size=30):
    return T(text, size, color).move_to(point(x, y))


def heading(text, x=-2.85, color=TEXT):
    return label(text, x, 3.30, color, 33)


def arrow(a, b, color=BLUE, width=5):
    return Arrow(point(*a), point(*b), buff=0, color=color, stroke_width=width, tip_length=0.19)


def bench():
    front = Polygon(point(-6.65, -2.56), point(6.65, -2.56), point(6.65, -2.83),
                    point(-6.65, -2.83), stroke_width=0, fill_color=SLATE, fill_opacity=1)
    lip = Line(point(-6.65, -2.56), point(6.65, -2.56), color=GREY, stroke_width=2)
    return VGroup(front, lip).set_z_index(-2)


def landscape():
    far = Polygon(*[point(x, y) for x, y in [(-6.65, -2.18), (-6.65, 0.45), (-4.1, 1.52),
                                             (-1.8, 0.96), (0.25, 1.85), (2.9, 1.23),
                                             (6.65, 1.72), (6.65, -2.18)]],
                  stroke_width=0, fill_color="#23433F", fill_opacity=1)
    trees = VGroup()
    for x, y, h in [(-5.6, 0.8, 2.15), (-4.8, 1.0, 1.5), (-3.85, 0.8, 2.05),
                    (3.9, 0.95, 1.65), (4.7, 0.83, 2.45), (5.65, 0.67, 2.1)]:
        trees.add(Polygon(point(x, y + h), point(x - h * 0.34, y), point(x + h * 0.34, y),
                          stroke_width=0, fill_color="#396157", fill_opacity=1))
    pond = Ellipse(width=11.7, height=3.9, color=TEAL, stroke_width=3,
                   fill_color=WATER, fill_opacity=1).move_to(point(0.28, -1.02))
    bob(pond, amp=0.22, speed=1.9)
    ripples = VGroup()
    for i, (x, y) in enumerate([(-3.2, -1.62), (0.3, -2.13), (2.9, -1.75), (0.9, -0.58)]):
        ripple = Arc(radius=0.62, start_angle=PI * 1.12, angle=PI * 0.76, color=BLUE, stroke_width=3)
        ripple.stretch(0.27, 1).move_to(point(x, y))
        bob(ripple, amp=0.24, speed=3.2, seed=i)
        ripples.add(ripple)
    for x, y, phase in [(-2.25, -0.49, 0.0), (2.68, -1.68, 0.5)]:
        ring = Ellipse(width=1.55, height=0.58, color=BLUE, stroke_width=4).move_to(point(x, y))
        ring.age = phase
        base = ring.copy()

        def expand(mob, dt, base=base):
            mob.age = (mob.age + 0.55 * dt) % 1
            mob.become(base.copy().scale(0.55 + 1.40 * mob.age).set_stroke(opacity=0.86 * (1 - mob.age)))

        ring.add_updater(expand)
        ripples.add(ring)
    return VGroup(far, trees, pond, ripples)


def vessel(x, bottom=-2.50, w=1.48, h=4.75, colors=(SLOW, FAST), populations=None, level=None,
           moving=True, seed=0, count=12, ciliates=False):
    """Build the same glass profile and cell positions at every cut."""
    if populations is None:
        populations = lambda: (0.66,) * len(colors)
    if level is None:
        level = lambda: 0.73
    center = point(x, bottom + h / 2)
    shell = RoundedRectangle(width=w, height=h, corner_radius=w * 0.23, stroke_color=BLUE,
                             stroke_width=3.4, fill_opacity=1, fill_color=GLASS).move_to(center)

    def fluid():
        depth = h * level()
        return RoundedRectangle(width=w - 0.12, height=depth, corner_radius=min(w * 0.19, depth * 0.43),
                                stroke_width=0, fill_color=WATER, fill_opacity=1).move_to(
                                    point(x, bottom + depth / 2 + 0.08))

    water = always_redraw(fluid) if moving and level() != 0.73 else fluid()
    # The lip and reflection lines cross glass only, with labels kept outside the vessels.
    lip = Ellipse(width=w - 0.07, height=min(0.17, h * 0.07), color=BLUE, stroke_width=3,
                  fill_color=SHADOW, fill_opacity=1).move_to(point(x, bottom + h - min(0.30, h * 0.17)))
    glint = Line(point(x - 0.40 * w, bottom + h * 0.26), point(x - 0.40 * w, bottom + h * 0.76),
                 color=BLUE, stroke_opacity=0.45, stroke_width=2)
    cells = VGroup()
    rng = np.random.default_rng(seed)
    currents = VGroup()
    if h >= 3:
        for i in range(3):
            ripple = Line(LEFT * w * 0.24, RIGHT * w * 0.24, color=BLUE, stroke_width=2.3)
            ripple.age = i / 3

            def circulate(mob, dt):
                mob.age = (mob.age + dt * 0.42) % 1
                mob.move_to(point(x + w * 0.12 * np.sin(TAU * mob.age),
                                  bottom + 0.12 + h * level() * (0.17 + 0.65 * mob.age)))
                mob.set_stroke(opacity=0.53 * np.sin(PI * mob.age))

            circulate(ripple, 0)
            if moving:
                ripple.add_updater(circulate)
            currents.add(ripple)
    for color_index, color in enumerate(colors):
        for i in range(count):
            u, v = rng.uniform(-0.20, 0.20), rng.uniform(0.25, 0.75)
            phase = rng.uniform(0, TAU)
            radius = min(w * 0.078, 0.115)
            if ciliates:
                microbe = Ellipse(width=radius * 3.15, height=radius * 1.5, color=color,
                                  stroke_width=1.5, fill_color=color, fill_opacity=1).rotate(phase)
            else:
                microbe = Dot(radius=radius, color=color)

            def drift(mob, dt, u=u, v=v, phase=phase, i=i, j=color_index):
                mob.age += dt
                a = phase + mob.age * 2.58
                mob.move_to(point(x + w * (u + 0.19 * np.sin(a)),
                                  bottom + 0.1 + h * level() * (v + 0.19 * np.cos(a * 1.13))))
                mob.set_opacity(np.clip(count * populations()[j] - i, 0, 1))

            microbe.age = 0.0
            drift(microbe, 0)
            if moving:
                microbe.add_updater(drift)
            cells.add(microbe)
    return VGroup(shell, water, glint, currents, cells, lip)


def rack(populations=None, level=None, moving=True, xs=(-5.4, -3.66, -1.92), colors=(SLOW, FAST)):
    return VGroup(*[vessel(x, colors=colors, populations=populations, level=level, moving=moving, seed=7 + i)
                    for i, x in enumerate(xs)])


def flow(a, b, color=BLUE, speed=0.60):
    shaft = arrow(a, b, color, 4)
    particles = VGroup()
    start, delta = point(*a), point(*b) - point(*a)
    for fraction in (0.12, 0.42, 0.72):
        bead = Dot(radius=0.092, color=TEXT)
        bead.phase = fraction

        def advance(mob, dt):
            mob.phase = (mob.phase + dt * speed) % 1
            mob.move_to(start + delta * (0.08 + 0.76 * mob.phase))

        advance(bead, 0)
        bead.add_updater(advance)
        particles.add(bead)
    return VGroup(shaft, particles)


def chemostat(x, colors, bottom=-2.50, w=1.9, h=4.1, populations=None):
    top = bottom + h
    side = bottom + h * 0.48
    return VGroup(vessel(x, bottom, w, h, colors, populations, seed=24, count=10),
                  flow((x, top + 0.68), (x, top + 0.11)),
                  flow((x + w * 0.49, side), (x + w * 0.49 + 0.68, side)))


def pipette(x, y):
    tip = Polygon(point(x - 0.07, y), point(x + 0.07, y), point(x + 0.21, y + 1.0),
                  point(x - 0.21, y + 1.0), color=BLUE, stroke_width=2.5,
                  fill_color=GLASS, fill_opacity=1)
    bulb = RoundedRectangle(width=0.48, height=0.36, corner_radius=0.12, color=BLUE,
                            stroke_width=2, fill_color=WATER, fill_opacity=1).move_to(point(x, y + 1.13))
    return VGroup(tip, bulb)


def graph(box=(0.38, 6.23, -1.86, 1.59), end=1, quantity="Population", xlabel="Time"):
    p = Plot(box=box, xr=(0, end), yr=(0, 1.02), color=TEXT, label_size=28, xlabel=xlabel)
    quantity_label = label(quantity, box[0], box[3] + 0.38, size=28)
    quantity_label.align_to(point(box[0], 0), LEFT)
    return VGroup(p, quantity_label), p


def schematic(x=5.04, y=-3.34):
    return scope_tag(size=28, color=TEXT).move_to(point(x, y))


def competition(death, rates, inhibition, initial, duration=36):
    """Integrate the dimensionless Abreu competition model, with Euler steps of 0.025."""
    grid = np.linspace(0, duration, round(duration / 0.025) + 1)
    values = np.empty((len(grid), 2))
    values[0] = initial
    rates = np.array(rates)
    for i, dt in enumerate(np.diff(grid)):
        n = values[i]
        values[i + 1] = n + dt * n * (rates * (1 - inhibition @ n) - death)
    return tuple(lambda t, v=v: float(np.interp(t * duration, grid, v)) for v in values.T)


# https://www.nature.com/articles/s41467-019-09925-0 — illustrative parameters, not fitted data.
RATES = (0.7, 1.55)
INHIBITION = np.array([[1.0, 0.83], [1.22, 1.0]])
LOW_RUN = competition(0.025, RATES, INHIBITION, (0.38, 0.37))
HIGH_RUN = competition(0.49, RATES, INHIBITION, (0.38, 0.37))


def dilution_gauge(value):
    gauge = dial(value, point(3.13, 1.62), radius=0.96, color=BLUE)
    gauge.remove(gauge[3])
    return gauge


def competition_curves(p, run, t):
    return VGroup(*(p.live_curve(fn, t, color=c, width=5) for fn, c in zip(run, (SLOW, FAST))))


def forecast(moving=False):
    """Outcome stays open while two possible winners branch from the same start."""
    cultures = rack(populations=lambda: (0.35, 0.35), level=lambda: 0.73, moving=moving)
    axes, p = graph(box=(0.38, 6.23, -1.86, 0.86))
    gauge = dilution_gauge(ValueTracker(HIGH))
    gauge_label = label("High dilution", 3.66, 1.26, BLUE, 28)
    branch = lambda t: (1 - np.exp(-3 * t)) / (1 - np.exp(-3))
    dashed = VGroup(*[DashedVMobject(p.curve(lambda t, sign=sign: 0.37 + sign * 0.30 * branch(t),
                                           color=TEXT, width=5), num_dashes=14)
                      for sign in (1, -1)])
    mark = label("?", 5.8, -0.80, GOLD, 50)
    origin = Dot(p.pt(0, 0.37), radius=0.066, color=TEXT)
    return VGroup(cultures, axes, gauge, gauge_label, schematic(), origin), dashed, mark


class S01Hook(SpokenScene):
    def construct(self):
        outdoors = landscape()
        question = heading("How do you test one ecological rule?", x=0, color=GOLD)
        self.add(outdoors, question)
        self.at("forest or pond")
        motions = VGroup()
        for i, (name, x, y, color) in enumerate([
            ("Food", -3.95, -0.44, GREEN), ("Weather", 0, 2.15, BLUE),
            ("Predators", 3.45, -0.35, PURPLE), ("Competitors", -0.23, -1.28, ORANGE),
        ]):
            cue = label(name, x, y, TEXT, 29)
            turn = CurvedArrow(point(x - 0.72, y - 0.39), point(x + 0.72, y - 0.39), angle=0.7,
                               color=color, stroke_width=5, tip_length=0.16)
            bob(turn, amp=0.12, speed=2.8, seed=i * 2)
            motions.add(VGroup(turn, cue))
        self.play(FadeOut(question), run_time=0.55)
        self.play(LaggedStart(*(FadeIn(m) for m in motions), lag_ratio=0.44), run_time=2.7)
        self.at("to untangle them")
        self.play(FadeOut(motions), run_time=0.7)
        cultures = rack(xs=(-2.3, 0, 2.3), colors=(TEAL, GREEN))
        self.at("ecologists build")
        self.play(FadeOut(outdoors, scale=0.22), FadeIn(bench()), FadeIn(cultures, shift=UP * 0.18), run_time=2.0)
        self.finish()


class S02Title(TitleCard):
    LESSON = "Microcosm Experiments"
    TITLE = "Ecosystems in a Flask"

    def construct(self):
        self.add(bench(), rack(xs=(-2.3, 0, 2.3), colors=(TEAL, GREEN)))
        title = T(self.TITLE, size=52, font=TITLE_FONT).move_to(point(0, 3.19))
        self.play(FadeIn(title), run_time=5 / 15)
        self.wait(20 / 15)
        self.play(FadeOut(title), run_time=5 / 15)


class S03Setup(SpokenScene):
    def construct(self):
        growth = ValueTracker(0.37)
        level = ValueTracker(0.729)
        start = rack(xs=(-2.3, 0, 2.3), colors=(TEAL, GREEN))
        left = rack(colors=(TEAL, GREEN), populations=lambda: (growth.get_value(), growth.get_value()),
                    level=level.get_value)
        self.add(bench(), start)
        self.at("these are laboratory")
        self.play(ReplacementTransform(start, left), run_time=1.05)
        title = heading("Replicated microcosms")
        self.play(FadeIn(title), run_time=0.55)
        self.at("they hold")
        examples = VGroup(*[label(word, 3.38, 2.3 - j * 0.94, color, 34)
                            for j, (word, color) in enumerate([
                                ("Yeasts", TEXT), ("Bacteria", TEXT), ("Ciliates", TEXT),
                                ("Algae", GREEN), ("Rotifers", PURPLE),
                            ])])
        self.play(LaggedStart(*(FadeIn(m, shift=UP * 0.10) for m in examples), lag_ratio=0.4),
                  growth.animate.set_value(0.65), run_time=4.15)
        self.at("many generations")
        self.play(growth.animate.set_value(1), run_time=1.9)
        self.play(FadeOut(examples), FadeOut(title), run_time=0.36)
        self.at("run in tubes")
        dropper = pipette(-3.66, 2.37)
        drop = Dot(point(-3.66, 2.29), radius=0.075, color=BLUE)
        self.play(FadeIn(dropper), run_time=0.7)
        self.at("a fraction moved")
        self.play(dropper.animate.shift(RIGHT * 1.74), level.animate.set_value(0.62), run_time=0.9)
        drop.shift(RIGHT * 1.74)
        self.add(drop)
        self.play(drop.animate.shift(DOWN * 1.3).set_opacity(0), level.animate.set_value(0.729), run_time=0.9)
        self.remove(drop)
        self.play(FadeOut(dropper), run_time=0.35)
        self.at("others run")
        blank = vessel(3.25, w=2.18, h=4.1, colors=(TEAL, GREEN))
        self.play(FadeIn(blank), run_time=0.55)
        self.at("chemostat")
        right = chemostat(3.25, (TEAL, GREEN), w=2.18)
        self.play(ReplacementTransform(blank, right), run_time=0.55)
        self.play(FadeIn(heading("Chemostat", 3.25)), run_time=0.52)
        self.at("nutrient inflow")
        self.play(FadeIn(label("Nutrient inflow", 1.65, 2.68, BLUE, 28)), run_time=0.55)
        self.at("matching outflow")
        self.play(FadeIn(label("Outflow", 5.50, 0.10, BLUE, 28)), run_time=0.55)
        self.finish()


class S04Method(SpokenScene):
    def construct(self):
        t = ValueTracker(0)
        level = ValueTracker(0.729)
        populations = lambda: tuple(0.97 * fn(t.get_value()) + 0.08 * (1 - t.get_value()) for fn in LOW_RUN)
        cultures = rack(populations, level.get_value)
        value = ValueTracker(LOW)
        gauge = dilution_gauge(value)
        self.add(bench(), cultures)
        self.at("hold conditions fixed")
        title = heading("Fixed conditions")
        self.play(FadeIn(title), run_time=0.55)
        self.at("one ecological cause")
        replicated = heading("Replicated cultures")
        self.play(swap(title, replicated), run_time=0.7)
        self.at("soil bacteria")
        clock_center = point(3.13, -0.45)
        clock = Circle(radius=0.82, stroke_color=BLUE, stroke_width=3, fill_color=GLASS,
                       fill_opacity=1).move_to(clock_center)
        hand = Line(clock_center, clock_center + UP * 0.63, color=TEXT, stroke_width=5)
        self.play(FadeIn(clock), FadeIn(hand), run_time=0.68)
        self.at("every 24 hours")
        day = label("24 hours", 3.13, -1.68, TEXT, 29)
        self.play(FadeIn(day), Rotate(hand, -TAU, about_point=clock_center), run_time=2.48)
        self.at("the share discarded")
        dropper = pipette(-3.66, 2.31)
        self.play(FadeOut(replicated), run_time=0.28)
        self.play(FadeIn(dropper), FadeIn(gauge), run_time=0.52)
        self.play(dropper.animate.shift(UP * 0.10), level.animate.set_value(0.63), run_time=1.0)
        self.play(level.animate.set_value(0.729), FadeOut(dropper), run_time=0.9)
        self.play(FadeOut(VGroup(clock, hand, day)), run_time=0.46)
        self.at("at low dilution")
        axes, p = graph(box=(0.38, 6.23, -1.86, 0.86))
        self.play(FadeIn(axes), FadeIn(schematic()), FadeIn(label("Low dilution", 3.66, 1.26, BLUE, 28)),
                  run_time=0.50)
        self.at("one slow grower")
        key = heading("Slow grower", -4.98, SLOW)
        key2 = heading("Faster grower", -1.55, FAST)
        self.play(FadeIn(key), FadeIn(key2), run_time=0.49)
        self.add(competition_curves(p, LOW_RUN, t))
        self.play(t.animate.set_value(1), run_time=3.93, rate_func=linear)
        self.finish()


class S05Predict(SpokenScene):
    def construct(self):
        level = ValueTracker(0.729)
        slow, fast = (ValueTracker(fn(1) * 0.97) for fn in LOW_RUN)
        value = ValueTracker(LOW)
        cultures = rack(lambda: (slow.get_value(), fast.get_value()), level.get_value)
        axes, p = graph(box=(0.38, 6.23, -1.86, 0.86))
        old_result = VGroup(*(p.curve(fn, color=color, width=5)
                              for fn, color in zip(LOW_RUN, (SLOW, FAST))))
        gauge_low = label("Low dilution", 3.66, 1.26, BLUE, 28)
        gauge_high = label("High dilution", 3.66, 1.26, BLUE, 28)
        self.add(bench(), cultures, axes, dilution_gauge(value), gauge_low, schematic(), old_result)
        self.at("now turn")
        self.play(FadeOut(old_result), slow.animate.set_value(0.88), fast.animate.set_value(0.88), run_time=0.66)
        self.play(FadeIn(Dot(p.pt(0, 0.37), radius=0.066, color=TEXT)), run_time=0.14)
        self.at("dilution dial up")
        self.play(swap(gauge_low, gauge_high), value.animate.set_value(HIGH), run_time=1.35)
        self.at("discarding a much larger")
        self.play(level.animate.set_value(0.29), slow.animate.set_value(0.35), fast.animate.set_value(0.35), run_time=2.35)
        self.at("both species lose")
        equal = heading("Same fraction lost")
        inflow = VGroup(*[flow((x, 2.94), (x, 2.24)) for x in (-5.4, -3.66, -1.92)])
        self.play(FadeIn(equal), FadeIn(inflow), run_time=0.60)
        self.play(level.animate.set_value(0.73), run_time=2.65)
        self.play(FadeOut(equal), FadeOut(inflow), run_time=0.45)
        self.at("predict does the")
        _, dashed, mark = forecast()
        card = question_card(QUESTION, y=QUESTION_Y, size=34)
        self.play(Create(dashed), FadeIn(mark), run_time=1.42)
        self.play(FadeIn(card), run_time=0.60)
        self.finish()


class S06Pause(PredictPause):
    QUESTION = QUESTION
    CARD = {"y": QUESTION_Y, "size": 34}
    SECONDS = 4.5

    def backdrop(self):
        frame, dashed, mark = forecast()
        return VGroup(bench(), frame, dashed, mark)

    def construct(self):
        self.add(self.backdrop(), question_card(self.QUESTION, **self.CARD))
        self.wait(self.SECONDS)


class S07RevealControls(SpokenScene):
    def construct(self):
        t = ValueTracker(0)
        cultures = rack(lambda: tuple(fn(t.get_value()) - 0.025 * (1 - t.get_value()) for fn in HIGH_RUN))
        axes, p = graph(box=(0.38, 6.23, -1.86, 0.86))
        gauge = VGroup(dilution_gauge(ValueTracker(HIGH)), label("High dilution", 3.66, 1.26, BLUE, 28))
        _, dotted, mark = forecast()
        tag = schematic()
        question = question_card(QUESTION, y=QUESTION_Y, size=34)
        origin = Dot(p.pt(0, 0.37), radius=0.066, color=TEXT)
        self.add(bench(), cultures, axes, gauge, dotted, mark, tag, origin, question)
        self.at("in 2019")
        date = heading("Abreu et al. 2019", color=GOLD)
        self.play(FadeOut(question), FadeIn(date), run_time=0.70)
        self.at("flip the faster", lead=0.35)
        self.play(FadeOut(VGroup(dotted, mark, origin)), run_time=0.35)
        traces = competition_curves(p, HIGH_RUN, t)
        winner = caption("Faster grower wins", color=FAST, y=QUESTION_Y)
        self.add(traces)
        self.play(t.animate.set_value(0.57), run_time=0.85, rate_func=linear)
        self.play(t.animate(run_time=0.55, rate_func=linear).set_value(1), FadeIn(winner, run_time=0.35))
        self.at("the model each species")
        self.play(FadeOut(VGroup(axes, traces, gauge, date, winner)), run_time=0.50)
        name = label("Carrying capacity", 3.03, 2.55, size=34)
        self.play(FadeIn(name), run_time=0.58)

        def bars(widths, color, y):
            outer = RoundedRectangle(width=4.5, height=0.50, corner_radius=0.12, color=color,
                                     stroke_width=2.5, fill_color=SHADOW, fill_opacity=1).move_to(point(3.04, y))
            fills = always_redraw(lambda: RoundedRectangle(width=max(0.03, widths() * 4.16),
                                                            height=0.24, corner_radius=0.05,
                                                            stroke_width=0, fill_color=color, fill_opacity=1
                                                            ).move_to(point(0.93 + widths() * 2.08, y)))
            return VGroup(outer, fills)

        death = ValueTracker(0)
        capacity_bars = VGroup(*[bars(lambda r=r: 1 - death.get_value() / r, c, y)
                                 for r, c, y in zip(RATES, (SLOW, FAST), (-0.42, -1.94))])
        self.at("the most its tube")
        self.play(FadeIn(capacity_bars), run_time=0.66)
        self.at("shrinks by death rate")
        equation = label("Fraction lost = death rate ÷ growth rate", 3.02, 1.85, TEXT, 29)
        self.play(FadeIn(equation), run_time=0.60)
        self.play(death.animate.set_value(0.19), run_time=1.86)
        self.at("smaller growth rate")
        growth_bars = VGroup(*[Line(point(1.19, y + 0.43), point(1.19 + 2.02 * r, y + 0.43),
                                    stroke_width=9, color=c)
                              for r, c, y in zip(RATES, (SLOW, FAST), (-0.42, -1.94))])
        growth_labels = VGroup(label("Slow growth", 1.88, 0.44, SLOW, 28),
                               label("Faster growth", 2.76, -1.06, FAST, 28))
        self.play(Create(growth_bars), FadeIn(growth_labels), run_time=0.63)
        self.at("loses the bigger share")
        self.play(death.animate.set_value(0.49), run_time=1.78)
        self.at("monocultures each species")
        self.play(FadeOut(VGroup(capacity_bars, name, equation, growth_bars, growth_labels, tag)), run_time=0.54)
        alone = vessel(3.20, w=2.15, colors=(SLOW,), populations=lambda: (0.66,), seed=19)
        self.play(FadeIn(alone), run_time=0.6)
        self.at("grown alone")
        self.play(FadeIn(heading("Monoculture", 3.2)), FadeIn(heading("Mixed cultures", -3.66)), run_time=0.65)
        self.at("survived that dilution")
        self.play(FadeIn(label("Slow grower survives alone", 3.2, -3.23, SLOW, 30)), run_time=0.55)
        self.finish()


def factorial():
    tubes = VGroup()
    for row in range(3):
        for col in range(3):
            tubes.add(vessel(-5.30 + 1.48 * col, bottom=-2.36 + 1.52 * row, w=0.95, h=1.32,
                             colors=(SLOW, FAST), seed=row * 3 + col, count=5))
    return tubes


class S08Limits(SpokenScene):
    def construct(self):
        self.add(bench())
        grid = factorial()
        self.play(LaggedStart(*(FadeIn(t, shift=UP * 0.13) for t in grid), lag_ratio=0.10), run_time=1.55)
        self.at("disturbance frequency")
        frequency = label("Frequency", -3.80, 2.60, BLUE, 29)
        axis_f = arrow((-5.83, 2.25), (-1.80, 2.25))
        self.play(GrowArrow(axis_f), FadeIn(frequency), run_time=0.72)
        self.at("intensity in bacterial")
        intensity = T("Intensity", 29, BLUE).rotate(PI / 2).move_to(point(-6.46, -0.15))
        axis_i = arrow((-6.11, -2.32), (-6.11, 1.98))
        self.play(GrowArrow(axis_i), FadeIn(intensity), FadeIn(heading("Hall et al. 2012", color=GOLD)),
                  run_time=0.70)
        self.at("different combinations")
        axes, p = graph((0.45, 6.20, -1.94, 2.36), quantity="Diversity", xlabel="")
        tag = schematic()
        by_frequency = label("Frequency", 3.325, -2.29, TEXT, 28)
        by_intensity = label("Intensity", 3.325, -2.29, TEXT, 28)
        self.play(FadeIn(axes), FadeIn(tag), FadeIn(by_frequency), run_time=0.61)
        self.at("gave different diversity")
        # Hall et al. 2012 describes flat, increasing and unimodal responses. These normalized
        # functions show the reported shapes only, with neither treatment identities nor units.
        t = ValueTracker(0)
        s = ValueTracker(0)
        flat, rise, hump = (lambda x: 0.31, lambda x: 0.31 + 0.60 * x,
                            lambda x: 0.31 + 0.65 * 4 * x * (1 - x))
        trace = p.live_curve(lambda x: np.interp(s.get_value(), (0, 1, 2), (flat(x), rise(x), hump(x))),
                             t, color=GREEN, width=6)
        self.add(trace)
        self.play(t.animate.set_value(1), run_time=0.95, rate_func=linear)
        self.play(s.animate.set_value(1), swap(by_frequency, by_intensity), run_time=1.30)
        self.play(s.animate.set_value(2), swap(by_intensity, by_frequency), run_time=1.40)
        self.at("in 2016")
        hall_scene = self.mobjects[1:]
        level = ValueTracker(0.729)
        retained = ValueTracker(0.74)
        culture = vessel(0, w=2.40, h=4.7, level=level.get_value,
                         populations=lambda: (retained.get_value(),) * 2)
        date = heading("Gibbons et al. 2016", x=0, color=GOLD)
        self.play(*(FadeOut(m) for m in hall_scene), FadeIn(culture), run_time=0.68)
        self.play(FadeIn(date), run_time=0.47)
        self.at("replacing culture")
        out = flow((-1.24, -0.32), (-4.18, -0.32), GREEN)
        left_name = label("Cells removed", -2.80, 0.31, GREEN, 30)
        self.play(FadeIn(out), FadeIn(left_name), level.animate.set_value(0.42),
                  retained.animate.set_value(0.42), run_time=1.10)
        self.at("resupplied nutrients")
        into = flow((4.18, 0.70), (1.25, 0.70), BLUE)
        right_name = label("Fresh nutrients", 2.87, 1.34, BLUE, 30)
        self.play(FadeIn(into), FadeIn(right_name), level.animate.set_value(0.729), run_time=1.52)
        self.at("vessels stay simple")
        self.play(FadeOut(VGroup(out, left_name, into, right_name, date)), run_time=0.55)
        boundary = Ellipse(width=5.2, height=5.0, color=BLUE, stroke_width=4).move_to(point(0, 0.06))
        background = landscape()
        background.clear_updaters(recursive=True)
        background.set_opacity(0.34).set_z_index(-3)
        self.play(Create(boundary), FadeIn(background), run_time=1.07)
        self.at("they test mechanisms")
        self.play(FadeIn(heading("Test a mechanism", x=0)), run_time=0.62)
        self.finish()


def ciliate_tubes(populations):
    x1, x2, x3 = -5.35, -3.55, -1.75
    return VGroup(vessel(x1, colors=(GREEN,), populations=lambda: (populations()[0],), seed=19, ciliates=True),
                  vessel(x2, colors=(PURPLE,), populations=lambda: (populations()[1],), seed=20, ciliates=True),
                  vessel(x3, colors=(GREEN, PURPLE), populations=lambda: populations()[2:], seed=21, ciliates=True))


class S09Unlocked1(SpokenScene):
    def construct(self):
        t, mix = ValueTracker(0), ValueTracker(0)
        # Schematic integration of the logistic/Lotka–Volterra forms used by Gause.
        solo = tuple(lambda u, r=r, k=k: k / (1 + (k / 0.14 - 1) * np.exp(-9 * r * u))
                     for r, k in ((0.88, 0.88), (1.04, 0.73)))
        mixed = competition(0, (0.68, 0.82), np.array([[1.0, 0.7], [1.4, 1.0]]), (0.23, 0.37), duration=24)
        cultures = ciliate_tubes(lambda: tuple(fn(t.get_value()) for fn in solo)
                                    + tuple(fn(mix.get_value()) for fn in mixed))
        cultures.save_state()
        cultures.scale(0.85, about_point=point(-3.55, -2.5))
        self.add(bench(), cultures)
        self.at("these tiny worlds")
        self.play(Restore(cultures), run_time=2.48)
        self.at("in 1934")
        date = heading("Gause 1934", color=GOLD)
        self.play(FadeIn(date), run_time=0.52)
        self.at("reported paramecium species")
        key_a = label("P. aurelia", 1.85, 2.81, GREEN, 29)
        key_c = label("P. caudatum", 4.72, 2.81, PURPLE, 29)
        self.play(FadeIn(key_a), run_time=0.50)
        self.play(FadeIn(key_c), run_time=0.50)
        self.at("grown alone and together")
        lab1 = label("Alone", -4.45, -3.24, TEXT, 28)
        lab2 = label("Together", -1.75, -3.24, TEXT, 28)
        self.play(FadeIn(lab1), FadeIn(lab2), run_time=0.55)
        axes, p = graph(box=(0.40, 6.20, -1.86, 1.85))
        tag = schematic()
        self.play(FadeIn(axes), FadeIn(tag), run_time=0.47)
        self.at("alone each grew well")
        solo_curves = VGroup(*(p.live_curve(fn, t, color=c) for fn, c in zip(solo, (GREEN, PURPLE))))
        context = label("Grown alone", 4.12, 2.23, TEXT, 28)
        self.add(solo_curves)
        self.play(t.animate(run_time=0.93, rate_func=linear).set_value(1), FadeIn(context, run_time=0.35))
        self.at("together paramecium")
        self.play(FadeOut(solo_curves), swap(context, label("Grown together", 4.12, 2.23, TEXT, 28)),
                  run_time=0.66)
        self.add(*(p.live_curve(fn, mix, color=c) for fn, c in zip(mixed, (GREEN, PURPLE))))
        self.play(mix.animate.set_value(1), run_time=5.52, rate_func=linear)
        self.at("later named competitive")
        self.play(swap(VGroup(lab1, lab2), label("Competitive exclusion", -3.63, -3.24, GOLD, 30)), run_time=0.8)
        self.finish()


def cycles(period, lag, phase=0.24, offset=0.0):
    """Sine schematics encode reported period and phase; amplitudes are illustrative."""
    return tuple(lambda t, shift=shift, mean=mean: mean + 0.31 * np.sin(TAU * ((t / period) + phase - shift))
                 for shift, mean in ((0, 0.58 + offset), (lag, 0.43)))


def cycle_plot(period, lag, time, end=3, box=(0.52, 6.30, -1.86, 1.91), phase=0.24):
    axes, p = graph(box, end=end)
    functions = cycles(period, lag, phase)
    traces = VGroup(*(p.live_curve(fn, time, color=color, width=5) for fn, color in zip(functions, (GREEN, PURPLE))))
    return axes, p, traces, functions


def orchard(time):
    oranges = VGroup()
    for row in range(3):
        for col in range(3):
            x, y = -5.53 + col * 1.79, -1.86 + row * 1.72
            phase = (row + col) / 9
            fruit = Circle(radius=0.59, stroke_width=3, stroke_color=ORANGE, fill_color="#7D502F",
                           fill_opacity=1).move_to(point(x, y))
            rind = Arc(radius=0.46, start_angle=0.45 * PI, angle=0.44 * PI, color=ORANGE,
                       stroke_opacity=0.62, stroke_width=2, arc_center=point(x, y))
            mites = VGroup()
            for i in range(5):
                mite = Dot(radius=0.113, color=GREEN if i < 3 else PURPLE)

                def step(mob, dt, i=i, x=x, y=y, phase=phase):
                    mob.age += dt
                    a = mob.age * 3.8 + i * TAU / 5
                    mob.move_to(point(x + 0.35 * np.cos(a), y + 0.35 * np.sin(a)))
                    wave = (1 + np.sin(TAU * (time.get_value() - phase - (0.24 if i >= 3 else 0)))) / 2
                    mob.set_opacity(0.16 + 0.84 * wave)

                mite.age = 0
                step(mite, 0)
                mite.add_updater(step)
                mites.add(mite)
            oranges.add(VGroup(fruit, rind, mites))
    barriers = VGroup(*[Line(point(x, y1), point(x, y2), color=GREY, stroke_width=7)
                        for x, y1, y2 in ((-4.63, -2.40, -0.90), (-4.63, -0.31, 1.19),
                                           (-2.84, -1.73, -0.47), (-2.84, 0.37, 1.87))])
    return oranges, barriers


class S10Unlocked2(SpokenScene):
    def construct(self):
        t = ValueTracker(0)
        oranges, barriers = orchard(t)
        self.add(bench(), oranges)
        self.at("huffaker kept")
        self.play(FadeIn(heading("Huffaker 1958", color=GOLD)), run_time=0.56)
        self.at("partial barriers")
        self.play(Create(barriers), run_time=0.65)
        self.play(FadeIn(label("Partial barriers", -3.75, -3.24, TEXT, 29)), run_time=0.54)
        self.at("numbers rose and fell")
        axes, p = graph((0.52, 6.30, -1.86, 1.91), end=3)
        # Relative peak heights from Huffaker 1958 (Fig. 18 and discussion). Use the
        # observed three-wave pattern, with phase and within-wave shape schematic.
        peak_heights = (8550, 12624, 11956)

        def prey(x):
            cycle = min(2, int(x))
            return 0.08 + 0.88 * (peak_heights[cycle] / max(peak_heights)) * np.sin(PI * (x - cycle)) ** 2

        predator = lambda x: 0.06 + 0.69 * np.sin(PI * max(0, x - 0.21)) ** 2
        traces = VGroup(p.live_curve(prey, t, color=GREEN, width=5),
                        p.live_curve(predator, t, color=PURPLE, width=5))
        key = VGroup(label("Prey mites", 1.75, 2.79, GREEN, 28),
                     label("Predatory mites", 4.69, 2.79, PURPLE, 28))
        self.play(FadeIn(axes), FadeIn(key), FadeIn(schematic()), run_time=0.35)
        self.add(traces)
        self.play(t.animate.set_value(3), run_time=2.12, rate_func=linear)
        stop = p.vline(3, color=TEXT)
        self.at("the run ended")
        self.play(Create(stop), FadeIn(label("Run ended", 5.55, 2.27, TEXT, 28)), run_time=0.62)
        self.at("spatial structure")
        self.play(barriers.animate.set_color(BLUE), run_time=0.62)
        self.finish()


def yoshida_tubes(single=None, multi=None):
    return VGroup(chemostat(-5.10, (GREEN, PURPLE), w=1.49, h=4.75, populations=single),
                  chemostat(-2.27, (GREEN, LIME, TEAL, PURPLE), w=1.49, h=4.75, populations=multi))


def grazer_key():
    return VGroup(label("Algae", 1.56, 2.83, GREEN, 29), label("Rotifers", 3.19, 2.83, PURPLE, 29))


class S10bUnlocked3(SpokenScene):
    def construct(self):
        t = ValueTracker(0)
        axes, p, traces, (algae, rotifers) = cycle_plot(0.92, 0.25, t)
        tubes = yoshida_tubes(lambda: (algae(t.get_value()), rotifers(t.get_value())))
        self.add(bench(), tubes)
        self.at("and colleagues grew")
        self.play(FadeIn(heading("Yoshida et al. 2003", color=GOLD)), run_time=0.57)
        self.at("in chemostats")
        self.play(FadeIn(grazer_key()), run_time=0.58)
        self.at("one algal clone")
        single = label("One clone", -5.10, -3.22, TEXT, 28)
        multi = label("Many clones", -2.27, -3.22, TEXT, 28)
        self.play(FadeIn(single), run_time=0.63)
        self.at("a mix of clones")
        self.play(FadeIn(multi), run_time=0.65)
        self.at("with one clone")
        self.play(FadeIn(axes), FadeIn(schematic()), run_time=0.46)
        phase = label("¼-cycle lag", 5.03, 2.83, TEXT, 28)
        self.add(traces)
        self.play(t.animate.set_value(0.72), run_time=1.8, rate_func=linear)
        self.at("by about a", lead=0)
        self.play(t.animate(run_time=1.15, rate_func=linear).set_value(3), FadeIn(phase, run_time=0.35))
        self.finish()


class S10cUnlocked3b(SpokenScene):
    def construct(self):
        t = ValueTracker(3)
        period, lag = ValueTracker(0.92), ValueTracker(0.25)
        axes, p = graph((0.52, 6.30, -1.86, 1.91), end=3)
        algae = lambda x: cycles(period.get_value(), lag.get_value())[0](x)
        rotifers = lambda x: cycles(period.get_value(), lag.get_value())[1](x)
        tubes = yoshida_tubes(multi=lambda: (algae(t.get_value()), 0.43, 0.41, rotifers(t.get_value())))
        tag = schematic()
        multi = label("Many clones", -2.27, -3.22, TEXT, 28)
        self.add(bench(), tubes, multi, axes, grazer_key(), tag)
        self.at("with many clones")
        self.add(p.live_curve(algae, t, color=GREEN, width=5), p.live_curve(rotifers, t, color=PURPLE, width=5))
        self.at("cycles ran long")
        self.play(period.animate.set_value(2.42), lag.animate.set_value(0.48), run_time=1.8, rate_func=linear)
        self.at("algae that resisted")
        alga1 = Circle(radius=0.47, color=GREEN, fill_opacity=0.58).move_to(point(2.16, 0.77))
        alga2 = alga1.copy().move_to(point(4.93, 0.77))
        shield = Polygon(point(2.34, 1.06), point(2.83, 1.06), point(2.78, 0.70), point(2.58, 0.55),
                         point(2.38, 0.70), stroke_color=TEXT, stroke_width=3, fill_color=TEAL, fill_opacity=1)
        # Switch the graph to an enlarged picture of the trade-off before adding its labels.
        graph_items = [mob for mob in self.mobjects if mob is axes or
                       (mob.get_left()[0] >= 0.50 and mob is not tag)]
        self.play(*(FadeOut(mob) for mob in graph_items), run_time=0.48)
        # The key is a group whose left edge starts in this same region.
        self.play(FadeIn(alga1), FadeIn(alga2), Create(shield), run_time=0.55)
        defended = label("Defended", 2.16, -0.03, GREEN, 28)
        undefended = label("Undefended", 4.93, -0.03, GREEN, 28)
        self.play(FadeIn(defended), FadeIn(undefended), run_time=0.42)
        self.at("poorer competitors")
        small = flow((2.16, -1.32), (2.16, -0.53), BLUE)
        large = flow((4.93, -1.94), (4.93, -0.53), BLUE)
        self.play(FadeIn(small), FadeIn(large), run_time=0.88)
        self.at("nutrients that made")
        self.play(FadeIn(label("Nutrient uptake", 3.48, -2.19, BLUE, 28)), run_time=0.52)
        self.at("prey evolution")
        self.play(FadeIn(heading("Prey evolution", 3.48)), run_time=0.55)
        self.finish()


class S11End(EndCard):
    LINE = "Hold conditions fixed in replicated microcosms to test one ecological cause."
