"""When Nature's Calendar Shifts — chapter 2.

COLOR MAP (kept from chapter 1)
  BLUE  = light, day length, and the cold checkpoint
  RED   = temperature and warmth
  GOLD  = the organism's inner rhythm
  GREEN = the organism's response

All dials are built by ``year_dial`` and all evidence plots by ``bloom_plot`` so carried
pictures keep exactly the same scale and landmarks from scene to scene.
"""
from bp_parts import *


PINK = "#F3A6C8"
MEANS = [92.7, 96.8, 93.4, 96.8, 97.4, 95.5, 93.3, 90.9, 90.7, 91.7]


def fade_existing(mob, alpha):
    """Dim existing ink without turning zero-fill lines and arcs into filled shapes."""
    for part in mob.family_members_with_points():
        strokes = part.get_stroke_opacities()
        fills = part.get_fill_opacities()
        if len(strokes):
            part.set_stroke(opacity=float(np.max(strokes)) * alpha)
        if len(fills):
            part.set_fill(opacity=float(np.max(fills)) * alpha)
    return mob


def cherry_bud(scale=1.0, open_amount=0.0):
    """The lesson's cherry twig: a labelled-cartoon bud, never a molecular drawing."""
    twig = Line(LEFT * 0.75, RIGHT * 0.72, color=GREY, stroke_width=8).rotate(0.25)
    stem = Line(ORIGIN, UP * 0.55, color=GREY, stroke_width=7).shift(RIGHT * 0.1)
    closed = Ellipse(width=0.48 + 0.35 * open_amount, height=0.7,
                     stroke_color=GREEN, stroke_width=4, fill_color=GREEN,
                     fill_opacity=0.35).move_to(stem.get_end() + UP * 0.18)
    petals = VGroup(*[
        Circle(radius=0.15 + 0.05 * open_amount, stroke_width=2, stroke_color=PINK,
               fill_color=PINK, fill_opacity=0.9).move_to(closed.get_center() +
                    open_amount * 0.27 * np.array([np.cos(a), np.sin(a), 0]))
        for a in np.linspace(0, TAU, 5, endpoint=False)
    ]).set_opacity(open_amount)
    return VGroup(twig, stem, closed, petals).scale(scale)


def year_dial(center=ORIGIN, radius=2.55, phase=None, warmth_shift=0.0,
              cold_fraction=1.0, bloom_shift=0.0, bud_open=0.0, opacity=1.0):
    """One consistent schematic year dial; cue sectors are angular data, not sketched curves."""
    center = np.array(center, dtype=float)
    phase = phase or ValueTracker(0.08)
    outer = Circle(radius=radius, stroke_color=GREY, stroke_width=5).move_to(center)
    # Fixed angular sectors: day-length/cold, warmth, and response.
    light = Arc(radius=radius - 0.16, start_angle=0.72 * PI, angle=0.72 * PI,
                arc_center=center, color=BLUE, stroke_width=18)
    warm_start = -0.10 * PI + warmth_shift
    warm = Arc(radius=radius - 0.42, start_angle=warm_start, angle=0.60 * PI,
               arc_center=center, color=RED, stroke_width=18)
    cold = Arc(radius=radius - 0.68, start_angle=0.78 * PI,
               angle=max(0.16, 0.42 * PI * cold_fraction), arc_center=center,
               color=BLUE, stroke_width=13)
    rhythm = Circle(radius=radius - 0.94, stroke_color=GOLD, stroke_width=7).move_to(center)
    # A broad, breathing gold field makes the inner clock visibly continue through narration holds.
    glow = Circle(radius=radius - 0.98, stroke_width=0, fill_color=GOLD,
                  fill_opacity=0.16 * opacity).move_to(center)
    glow._clock_t = 0.0
    def breathe(mob, dt, alpha=opacity):
        mob._clock_t += dt
        mob.set_fill(opacity=alpha * (0.18 + 0.16 * np.sin(2.6 * mob._clock_t)))
    glow.add_updater(breathe)
    pulse(rhythm, base=7.0, amp=2.8, speed=1.8)
    rhythm_layer = VGroup(glow, rhythm)
    bloom_angle = -0.03 * PI + warmth_shift + bloom_shift
    bloom = Dot(center + (radius - 0.12) * np.array([np.cos(bloom_angle), np.sin(bloom_angle), 0]),
                radius=0.14, color=GREEN)
    bud = cherry_bud(0.72, bud_open).move_to(center)
    needle = always_redraw(lambda: Arrow(
        center, center + (radius - 0.98) * np.array([
            np.cos(PI / 2 - TAU * phase.get_value()),
            np.sin(PI / 2 - TAU * phase.get_value()), 0]),
        buff=0, color=GOLD, stroke_width=5, tip_length=0.22).set_opacity(opacity))
    g = VGroup(outer, light, warm, cold, rhythm_layer, bloom, bud, needle)
    if opacity < 1.0:
        fade_existing(VGroup(outer, light, warm, cold, rhythm, bloom, bud), opacity)
    g.phase = phase
    g.bloom = bloom
    g.warm = warm
    g.cold = cold
    return g


def dial_stack(phases=None):
    """Three receding years, with the nearest dial always at the same landmark."""
    phases = phases or [ValueTracker(0.08), ValueTracker(0.18), ValueTracker(0.28)]
    back = year_dial([2.8, 1.25, 0], 1.55, phases[2], opacity=0.38)
    middle = year_dial([1.35, 0.55, 0], 2.0, phases[1], opacity=0.62)
    front = year_dial([-1.0, -0.35, 0], 2.75, phases[0], opacity=1.0)
    return VGroup(back, middle, front), phases


def add_clock_motion(scene, phases, speed=0.018):
    """Continuous, slow year motion that survives narration holds."""
    driver = Dot(radius=0.001).set_opacity(0)
    driver.layout_ok = True
    driver.add_updater(lambda _m, dt: [p.increment_value(dt * speed) for p in phases])
    scene.add(driver)
    return driver


def lone_timeline(with_question=True):
    line = Arrow(LEFT * 5.6 + DOWN * 0.35, RIGHT * 5.6 + DOWN * 0.35,
                 buff=0, color=GREY, stroke_width=5, tip_length=0.24)
    point = Dot([-3.4, -0.35, 0], radius=0.18, color=GREEN)
    cursor = Line([-3.4, -1.8, 0], [-3.4, 1.8, 0], color=GREEN, stroke_width=4)
    pulse(cursor, base=7.0, amp=5.0, speed=3.0)
    cursor._sway_t = 0.0
    cursor._sway_base = cursor.get_center().copy()
    def sway(mob, dt):
        mob._sway_t += dt
        mob.move_to(mob._sway_base + RIGHT * 0.45 * np.sin(3.2 * mob._sway_t))
    cursor.add_updater(sway)
    g = VGroup(line, point, cursor)
    if with_question:
        g.add(question_card("ONE YEAR PROVES A SHIFT?", y=-3.05, size=36))
    return g


def lone_ripples(point):
    """Bold green ripples spreading from the lone point, so the held picture keeps moving."""
    rings = VGroup(*[Circle(radius=0.2, stroke_color=GREEN, stroke_width=8, fill_opacity=0)
                     .move_to(point.get_center()) for _ in range(3)])
    for k, ring in enumerate(rings):
        ring._rt = 0.0
        ring._off = k * 0.9
        def grow(mob, dt):
            mob._rt += dt
            f = ((mob._rt + mob._off) % 2.7) / 2.7
            mob.become(Circle(radius=0.2 + 2.6 * f, stroke_color=GREEN,
                              stroke_width=9 * (1 - f) + 1.0, fill_color=GREEN,
                              fill_opacity=0.10 * (1 - f)).move_to(point.get_center())
                       .set_stroke(opacity=1.0 - 0.8 * f))
        ring.add_updater(grow)
        ring.layout_ok = True
    return rings


def bloom_plot(dim=False):
    """Exact plot of the ten decade means supplied in the lesson table."""
    p = Plot(box=(-5.55, 5.55, -2.0, 2.45), xr=(0, 9), yr=(89, 99),
             xticks=[(0, "1920s"), (4, "1960s"), (9, "2010s")],
             yticks=[89, 91, 93, 95, 97, 99], xlabel="DECADE GROUP", ylabel="MEAN DAY",
             size=24, label_size=28)
    pts = [p.pt(i, v) for i, v in enumerate(MEANS)]
    line = VMobject(stroke_color=GREEN, stroke_width=6, fill_opacity=0)
    line.set_points_as_corners(pts)
    pulse(line, base=6.0, amp=2.8, speed=1.8)
    dots = VGroup(*[Dot(q, radius=0.11, color=GREEN) for q in pts])
    earlier = VGroup(Arrow([-6.1, 1.0, 0], [-6.1, -1.2, 0], buff=0,
                           color=GREEN, stroke_width=5, tip_length=0.22),
                     T("EARLIER", 28, GREEN).rotate(PI / 2).move_to([-6.45, -0.1, 0]))
    scan_opacity = 0.82
    def scan_at(x):
        return VGroup(
            Line(p.pt(x, 89), p.pt(x, 99), color=GOLD, stroke_width=6).set_opacity(scan_opacity),
            Dot(p.pt(x, float(np.interp(x, np.arange(10), MEANS))),
                radius=0.17, color=GOLD).set_opacity(scan_opacity))
    scan = scan_at(0.0)
    scan._scan_x = 0.0
    def scan_across(mob, dt):
        mob._scan_x = (mob._scan_x + 1.35 * dt) % 9.0
        x = mob._scan_x
        mob.become(scan_at(x))
        mob._scan_x = x
    scan.add_updater(scan_across)
    g = VGroup(p, line, dots, earlier)
    if dim:
        fade_existing(g, 0.3)
        g.layout_ok = True
    g.plot = p
    g.line = line
    g.dots = dots
    g.scan = scan
    return g


class S01Link(SpokenScene):
    def construct(self):
        front_phase = ValueTracker(0.02)
        front = year_dial([0, -0.2, 0], 2.85, front_phase)
        add_clock_motion(self, [front_phase])
        self.at("The first film")
        self.play(FadeIn(front, scale=0.94), run_time=1.0)
        self.at("What happens")
        q = fit_text("WHAT IF CUES CHANGE FOR YEARS?", max_w=11.5, size=42,
                     color=TEXT, font=TITLE_FONT).move_to([0, 3.25, 0])
        self.play(Write(q), run_time=1.0)
        self.at("Return to the same dial")
        self.play(Indicate(front, color=GOLD, scale_factor=1.03), run_time=1.0)
        self.at("The nearest dial")
        self.play(Indicate(front[6], color=GREEN, scale_factor=1.18), run_time=0.8)
        self.at("This time")
        back = year_dial([3.25, 1.35, 0], 1.45, ValueTracker(0.3), opacity=0.38)
        middle = year_dial([1.9, 0.7, 0], 1.95, ValueTracker(0.2), opacity=0.62)
        years = T("MANY YEARS", 34, TEXT).move_to([4.25, -2.7, 0])
        self.play(FadeOut(q), FadeIn(back, shift=RIGHT * 0.25), run_time=0.7)
        self.play(FadeIn(middle, shift=RIGHT * 0.2), FadeIn(years), run_time=1.0)
        self.finish()


class S02Title(TitleCard):
    LESSON = "Daily and Seasonal Rhythms"
    TITLE = "When Nature's Calendar Shifts"


class S03Changes(SpokenScene):
    def construct(self):
        stack, phases = dial_stack()
        add_clock_motion(self, phases)
        stack.scale(0.72).shift(LEFT * 3.4)
        self.at("Long term change")
        self.play(FadeIn(stack), run_time=0.8)
        cause = fit_text("NATURAL EVENTS  +  PEOPLE", 6.4, 34, color=TEXT).move_to([3.0, 2.8, 0])
        self.play(FadeIn(cause), run_time=0.7)
        self.at("Wildfires and floods")
        natural = VGroup(Arc(radius=0.6, start_angle=0, angle=PI, color=RED, stroke_width=9),
                         VGroup(*[Arc(radius=r, start_angle=PI, angle=PI, color=BLUE,
                                     stroke_width=5) for r in (0.25, 0.45, 0.65)]).shift(DOWN * 0.55))
        natural.move_to([1.6, 1.45, 0])
        self.play(Create(natural), run_time=1.0)
        self.at("People can cause")
        people = VGroup(Rectangle(width=1.3, height=0.9, color=GREY, stroke_width=4),
                        VGroup(*[Line(ORIGIN, UP * h, color=RED, stroke_width=7)
                                 for h in (0.5, 0.8, 1.1)]).arrange(RIGHT, buff=0.2))
        people.move_to([4.5, 1.35, 0])
        self.play(FadeIn(people), run_time=0.9)
        self.at("Change can alter")
        self.play(FadeOut(natural), FadeOut(people), FadeOut(cause), run_time=0.5)
        many = VGroup(*[Dot(radius=0.12, color=GREEN) for _ in range(12)]).arrange_in_grid(3, 4, buff=0.16)
        few = VGroup(*[Dot(radius=0.12, color=GREEN) for _ in range(4)]).arrange(RIGHT, buff=0.18)
        many.move_to([1.35, 1.5, 0]); few.move_to([1.35, 1.5, 0])
        patch = RoundedRectangle(width=1.4, height=0.8, corner_radius=0.15,
                                 color=GREEN, fill_color=GREEN, fill_opacity=0.2).move_to([3.6, 1.5, 0])
        links = VGroup(Dot([1.1, -0.35, 0], color=GREEN), Dot([2.1, -0.35, 0], color=GREEN),
                       Line([1.1, -0.35, 0], [2.1, -0.35, 0], color=GREEN, stroke_width=5))
        cal = VGroup(RoundedRectangle(width=1.5, height=1.25, corner_radius=0.12, color=GREEN),
                     Line([3.8, -0.1, 0], [5.0, -0.1, 0], color=GREEN, stroke_width=4),
                     Dot([4.65, -0.55, 0], radius=0.13, color=GREEN))
        self.play(FadeIn(many), FadeIn(patch), FadeIn(links), FadeIn(cal), run_time=0.8)
        self.play(Transform(many, few), patch.animate.shift(RIGHT * 0.65),
                  links[1].animate.shift(RIGHT * 0.7), links[2].animate.set_opacity(0),
                  cal[2].animate.shift(LEFT * 0.65), run_time=1.5)
        self.at("Here we will follow timing")
        twig = cherry_bud(1.7).move_to([3.2, 0.8, 0])
        timing = T("TIMING", 38, GREEN).move_to([3.4, -1.45, 0])
        self.play(FadeOut(many), FadeOut(patch), FadeOut(links), FadeOut(cal),
                  FadeIn(twig, scale=0.7), FadeIn(timing), run_time=1.0)
        self.finish()


class S04Warmth(SpokenScene):
    def construct(self):
        shifts = [0.0, -0.20, -0.40]
        centers = [-4.2, 0.0, 4.2]
        phases = [ValueTracker(0.05 + i * 0.1) for i in range(3)]
        dials = VGroup(*[year_dial([x, 0.2, 0], 1.75, phases[i], warmth_shift=shifts[i],
                                  bud_open=0.15 + 0.35 * i) for i, x in enumerate(centers)])
        add_clock_motion(self, phases, 0.014)
        tag = scope_tag("SCHEMATIC", size=26)
        self.at("Suppose winter")
        self.play(LaggedStart(*[FadeIn(d) for d in dials], lag_ratio=0.2), FadeIn(tag), run_time=1.2)
        self.at("A tree that responds")
        may = caption("MAY BLOOM EARLIER", size=34, color=GREEN)
        self.play(FadeIn(may), run_time=0.7)
        self.at("On each new dial")
        self.play(LaggedStart(*[Indicate(d.warm, color=RED, scale_factor=1.08) for d in dials],
                              lag_ratio=0.3), run_time=2.0)
        self.at("The green bloom marker")
        self.play(LaggedStart(*[Flash(d.bloom, color=GREEN, flash_radius=0.35) for d in dials],
                              lag_ratio=0.3), run_time=1.8)
        self.finish()


class S05Cold(SpokenScene):
    def construct(self):
        panels = TwoPanel("ENOUGH COLD", "TOO LITTLE COLD", colors=(BLUE, BLUE), top=3.0)
        p1, p2 = ValueTracker(0.05), ValueTracker(0.22)
        left = year_dial([-3.2, 0.0, 0], 2.0, p1, cold_fraction=1.0, bud_open=1.0)
        right = year_dial([3.2, 0.0, 0], 2.0, p2, cold_fraction=0.42,
                          bloom_shift=0.45, bud_open=0.25)
        add_clock_motion(self, [p1, p2], 0.015)
        self.at("But warmth")
        self.play(FadeIn(panels), FadeIn(left), FadeIn(right), run_time=1.0)
        self.at("Many buds need")
        self.play(Indicate(left.cold, color=BLUE), Indicate(right.cold, color=BLUE), run_time=1.2)
        self.at("If winter becomes")
        late_blooms = VGroup(*[cherry_bud(0.42, a).move_to([2.4 + i * 0.75, -1.65 + 0.18 * (i % 2), 0])
                               for i, a in enumerate((0.2, 0.7, 1.0))])
        self.play(LaggedStart(*[FadeIn(b) for b in late_blooms], lag_ratio=0.35), run_time=1.8)
        self.at("Warming does not")
        outcome = caption("MAY OPEN LATE OR UNEVENLY", size=32, color=GREEN)
        self.play(FadeIn(outcome), run_time=0.8)
        self.at("Different timing systems")
        self.play(Indicate(VGroup(left, right), color=GOLD, scale_factor=1.02), run_time=1.0)
        self.finish()


class S06Predict(SpokenScene):
    def construct(self):
        p = ValueTracker(0.08)
        d = year_dial([0, 0.25, 0], 2.55, p)
        add_clock_motion(self, [p])
        self.at("Now predict")
        self.play(FadeIn(d), run_time=0.7)
        self.at("One spring")
        line = Arrow(LEFT * 5.6 + DOWN * 0.35, RIGHT * 5.6 + DOWN * 0.35,
                     buff=0, color=GREY, stroke_width=5, tip_length=0.24)
        point = Dot([-3.4, -0.35, 0], radius=0.18, color=GREEN)
        self.play(ReplacementTransform(d[0].copy(), line), FadeOut(d), FadeIn(point), run_time=1.2)
        self.at("Does that single year")
        ripples = lone_ripples(point)
        self.add(ripples)
        q = question_card("ONE YEAR PROVES A SHIFT?", y=-3.05, size=36)
        self.play(FadeIn(q), run_time=0.8)
        self.at("The rest of the record")
        hidden = VGroup(*[Dot([x, -0.35, 0], radius=0.11, color=GREY)
                          for x in np.linspace(-2.7, 5.0, 20)]).set_opacity(0.12)
        self.play(FadeIn(hidden), run_time=0.6)
        self.play(FadeOut(hidden), run_time=0.5)
        self.at("Hold your answer")
        cursor = Line([-3.4, -1.8, 0], [-3.4, 1.8, 0], color=GREEN, stroke_width=4)
        pulse(cursor, base=7.0, amp=5.0, speed=3.0)
        cursor._sway_t = 0.0
        cursor._sway_base = cursor.get_center().copy()
        cursor.add_updater(lambda mob, dt: (
            setattr(mob, "_sway_t", mob._sway_t + dt),
            mob.move_to(mob._sway_base + RIGHT * 0.45 * np.sin(3.2 * mob._sway_t))))
        self.play(FadeIn(cursor), run_time=0.5)
        self.finish()


class S07Pause(PredictPause):
    QUESTION = "ONE YEAR PROVES A SHIFT?"
    SECONDS = 4.5
    CARD = {"y": -3.05, "size": 36}

    def backdrop(self):
        base = lone_timeline(with_question=False)
        return VGroup(base, lone_ripples(base[1]))


class S08Reveal(SpokenScene):
    def construct(self):
        base = lone_timeline(with_question=False)
        self.add(base)
        self.at("No")
        no = T("NO", 60, RED, weight=BOLD).move_to([0, 2.9, 0])
        self.play(FadeIn(no, scale=1.3), run_time=0.6)
        self.at("One year can differ")
        self.play(FadeOut(no), base[1].animate.shift(UP * 0.45 + RIGHT * 0.25), run_time=0.9)
        self.at("A long term claim")
        xs = np.linspace(-5.0, 5.0, 34)
        points = VGroup(*[Dot([x, -0.35 + 0.38 * np.sin(i * 1.7), 0], radius=0.09, color=GREEN)
                          for i, x in enumerate(xs)])
        self.play(LaggedStart(*[FadeIn(dot, scale=0.5) for dot in points], lag_ratio=0.035), run_time=2.6)
        self.at("Observers use")
        rule = chip("70% OPEN", GREEN, size=36).move_to([0, 2.65, 0])
        self.play(FadeIn(rule, shift=DOWN * 0.2), run_time=0.8)
        self.at("At the tidal basin")
        water = ArcBetweenPoints([-5.4, -1.7, 0], [5.4, -1.7, 0], angle=-0.18,
                                 color=BLUE, stroke_width=8)
        trees = VGroup(*[cherry_bud(0.42, 1).move_to([x, -2.05, 0]) for x in (-3.4, 0, 3.4)])
        loc = T("TIDAL BASIN", 30, TEXT).move_to([0, -2.65, 0])
        self.play(Create(water), LaggedStart(*[FadeIn(t) for t in trees], lag_ratio=0.25),
                  FadeIn(loc), run_time=1.4)
        self.finish()


class S09Daynumber(SpokenScene):
    def construct(self):
        axis = Arrow([-5.7, 0, 0], [5.7, 0, 0], buff=0, color=GREY,
                     stroke_width=7, tip_length=0.28)
        ticks = VGroup(*[Line([x, -0.18, 0], [x, 0.18, 0], color=GREY, stroke_width=4)
                         for x in np.linspace(-5.3, 5.1, 12)])
        labs = VGroup(T("DAY 1", 30, TEXT).move_to([-5.2, -0.65, 0]),
                      T("DEC 31", 30, TEXT).move_to([5.0, -0.65, 0]))
        marker = Dot([2.8, 0, 0], radius=0.2, color=GREEN)
        self.at("The record uses")
        self.play(Create(axis), LaggedStart(*[Create(t) for t in ticks], lag_ratio=0.05), run_time=1.2)
        self.play(FadeIn(labs), FadeIn(marker), run_time=0.6)
        self.at("A smaller day number")
        self.play(marker.animate.move_to([-2.8, 0, 0]), run_time=1.8)
        earlier = VGroup(Arrow([1.8, 1.0, 0], [-2.4, 1.0, 0], buff=0, color=GREEN,
                               stroke_width=7, tip_length=0.28),
                         T("EARLIER", 38, GREEN).move_to([-0.3, 1.55, 0]))
        self.play(GrowArrow(earlier[0]), FadeIn(earlier[1]), run_time=0.8)
        self.at("That direction")
        backward = T("SMALLER NUMBER", 34, GREEN).move_to([-2.8, -1.35, 0])
        self.play(FadeIn(backward), run_time=0.7)
        self.at("Imagine the year")
        winter = T("WINTER", 34, BLUE).move_to([-4.3, 2.65, 0])
        summer = T("SUMMER", 34, RED).move_to([4.3, 2.65, 0])
        self.play(FadeIn(winter), FadeIn(summer), run_time=0.8)
        self.at("Moving left")
        self.play(Indicate(VGroup(marker, earlier), color=GREEN, scale_factor=1.04), run_time=1.0)
        self.finish()


class S10Means(SpokenScene):
    def construct(self):
        g = bloom_plot()
        p = g.plot
        self.at("Scientists can group")
        self.play(Create(p), run_time=1.3)
        self.at("The plotted means")
        self.play(LaggedStart(*[FadeIn(d, scale=0.5) for d in g.dots], lag_ratio=0.08), run_time=1.0)
        self.play(Create(g.line), FadeIn(g[3]), run_time=0.8)
        self.add(g.scan)
        self.at("The line never")
        self.play(Indicate(g.line, color=GREEN, scale_factor=1.01), run_time=1.0)
        self.at("Several groups")
        later = VGroup(*[Arrow(g.plot.pt(i, MEANS[i]) + DOWN * 0.6, g.plot.pt(i, MEANS[i]) + DOWN * 0.15,
                                buff=0, color=RED, stroke_width=4, tip_length=0.16)
                         for i in (1, 3, 4, 9)])
        self.play(LaggedStart(*[GrowArrow(a) for a in later], lag_ratio=0.18), run_time=1.5)
        self.at("After the group")
        self.play(FadeOut(later), Flash(g.dots[4], color=GOLD, flash_radius=0.35), run_time=0.8)
        self.play(Indicate(VGroup(*g.dots[5:]), color=GREEN, scale_factor=1.12), run_time=1.1)
        self.finish()


class S11Compare(SpokenScene):
    def construct(self):
        g = bloom_plot(dim=True)
        self.add(g, g.scan)
        a, b = 3, 7
        da = Dot(g.plot.pt(a, MEANS[a]), radius=0.17, color=RED)
        db = Dot(g.plot.pt(b, MEANS[b]), radius=0.17, color=GREEN)
        la = chip("1950–1959: 96.8", RED, size=28).move_to([-2.9, 3.3, 0])
        lb = chip("1990–1999: 90.9", GREEN, size=28).move_to([2.9, 3.3, 0])
        self.at("Compare two groups")
        self.play(FadeIn(da), FadeIn(db), FadeIn(la), FadeIn(lb), run_time=1.0)
        self.at("Subtract the smaller")
        eq = M("96.8 − 90.9 = 5.9 days", 38, TEXT).move_to([0, -2.95, 0])
        self.play(Write(eq), run_time=0.3)
        self.at("The smaller mean")
        self.play(Indicate(VGroup(db, lb), color=GREEN, scale_factor=1.05), run_time=1.0)
        self.at("The difference shown")
        move = Arrow(g.plot.pt(a, 94.0), g.plot.pt(b, 94.0), buff=0,
                     color=GREEN, stroke_width=8, tip_length=0.25)
        self.play(GrowArrow(move), run_time=1.2)
        self.finish()


class S12Limit(SpokenScene):
    def construct(self):
        g = bloom_plot(dim=True)
        frame = RoundedRectangle(width=12.25, height=6.0, corner_radius=0.2,
                                 stroke_color=GREEN, stroke_width=4).move_to([0, -0.05, 0])
        label = chip("ONE GROUP OF TREES, ONE CITY", GREEN, size=30).move_to([0, 3.3, 0])
        self.at("Be careful")
        self.play(FadeIn(g), Create(frame), FadeIn(label), run_time=1.0)
        self.at("These trees")
        self.play(Indicate(frame, color=GREEN, scale_factor=1.01), run_time=1.0)
        self.at("The dates show")
        temp = VGroup(Arc(radius=0.8, start_angle=PI, angle=-PI, color=RED, stroke_width=10),
                      T("TEMPERATURE", 28, RED).move_to([0, -0.4, 0])).move_to([-2.0, -1.45, 0])
        bloom = chip("BLOOM DATES", GREEN, size=28).move_to([2.1, -1.45, 0])
        equals = T("=", 52, TEXT).move_to([0.15, -1.45, 0])
        self.play(FadeIn(temp), FadeIn(equals), FadeIn(bloom), run_time=0.8)
        self.at("but they alone")
        question = T("?", 60, GOLD).move_to(equals)
        self.play(swap(equals, question), run_time=0.8)
        self.at("Testing cause")
        need = fit_text("CAUSE NEEDS MORE EVIDENCE", 9.0, 32, color=GOLD).move_to([0, -3.6, 0])
        self.play(FadeIn(need), run_time=0.8)
        self.finish()


class S13Synthesis(SpokenScene):
    def construct(self):
        plot = bloom_plot(dim=True)
        self.at("The dial record")
        self.play(FadeIn(plot), run_time=0.7)
        stack, phases = dial_stack()
        add_clock_motion(self, phases, 0.017)
        self.play(FadeOut(plot), FadeIn(stack), run_time=1.2)
        self.at("Organisms use")
        self.play(Indicate(stack[2][4], color=GOLD, scale_factor=1.04), run_time=1.0)
        self.at("Long term conditions")
        self.play(LaggedStart(*[Indicate(d.warm, color=RED, scale_factor=1.07) for d in stack],
                              lag_ratio=0.2), run_time=1.5)
        self.play(LaggedStart(*[Indicate(d.cold, color=BLUE, scale_factor=1.07) for d in stack],
                              lag_ratio=0.2), run_time=1.5)
        self.at("Responses may shift")
        self.play(LaggedStart(*[Flash(d.bloom, color=GREEN, flash_radius=0.35) for d in stack],
                              lag_ratio=0.25), run_time=1.5)
        may = caption("RESPONSES MAY SHIFT", size=34, color=GREEN, y=-3.5)
        self.play(FadeIn(may), run_time=0.7)
        self.at("A careful claim")
        rule = fit_text("PATTERN  +  LIMIT", max_w=8.0, size=42, color=TEXT,
                        font=TITLE_FONT).move_to([2.8, 3.35, 0])
        self.play(FadeIn(rule), FadeOut(may), run_time=0.9)
        self.play(Indicate(stack[2], color=GOLD, scale_factor=1.02), run_time=0.8)
        self.finish()


class S14End(EndCard):
    LINE = "Inner rhythms and environmental cues time responses;\nlong-term changes can shift them."
