"""Finding Causes Across Sites and Years.

COLOR MAP
BLUE: focal populations and their responses. GREEN: breeding habitat and food.
TEAL: comparison habitat and comparison tracks. GOLD: time and event markers.
RED: stresses and rival causes. GREY: shared structure and chance variation.
"""
from bp_parts import *

SITES = (-4.15, 0, 4.15)
QUESTION = "Wintering adults drop: is mismatch the main cause?"
QUESTION_CARD = dict(y=3.25, size=34, max_w=11.5)
LAND = ("#375B53", "#4C6A50", "#365A58")
REEF = ("#275477", "#316B82", "#275A78")
SOIL = ("#705747", "#77654A", "#625846")
SKY = "#182936"


def point(x, y):
    return np.array([x, y, 0.0])


def rect(w, h, x, y, colour, opacity=1):
    return Rectangle(width=w, height=h, stroke_width=0, fill_color=colour,
                     fill_opacity=opacity).move_to(point(x, y))


def polygon(coords, colour, opacity=1):
    return Polygon(*(point(x, y) for x, y in coords), stroke_width=0,
                   fill_color=colour, fill_opacity=opacity)


def line(a, b, colour=GREY, width=4):
    return Line(point(*a), point(*b), color=colour, stroke_width=width)


def heading(text, colour=TEXT):
    return T(text, 36, colour, weight=BOLD).move_to(point(-0.35, 3.23))


def label(text, x, y, colour=TEXT, size=30):
    return T(text, size, colour).move_to(point(x, y))


def schematic():
    return scope_tag(size=28, color=TEXT)


def arrow(a, b, colour=GOLD, width=5):
    return Arrow(point(*a), point(*b), buff=0, color=colour, stroke_width=width,
                 tip_length=0.19, max_stroke_width_to_length_ratio=18)


def tree(x, y, s, colour):
    return VGroup(
        rect(0.09*s, 0.5*s, x, y+0.25*s, colour),
        polygon([(x-0.36*s, y+0.31*s), (x, y+1.02*s), (x+0.36*s, y+0.31*s)], colour),
        polygon([(x-0.29*s, y+0.51*s), (x, y+1.17*s), (x+0.29*s, y+0.51*s)], colour),
    )


def bird(x, y, s=1, colour=BLUE, beak=0.18):
    wing = polygon([(-0.52, 0.08), (-0.10, 0.03), (0.20, 0.18), (0.03, -0.14),
                    (-0.17, -0.20), (-0.37, -0.10), (-0.61, -0.11)], colour)
    body = Ellipse(width=0.59, height=0.3, stroke_width=0,
                   fill_color=colour, fill_opacity=1)
    head = Dot(point(0.25, 0.11), radius=0.13, color=colour)
    bill = polygon([(0.34, 0.13), (0.34 + beak, 0.06), (0.34, -0.01)], GOLD)
    eye = Dot(point(0.28, 0.145), radius=0.027, color=BG)
    return VGroup(wing, body, head, bill, eye).scale(s).move_to(point(x, y))


def fish(x, y, s, colour=BLUE):
    shape = VGroup(
        Ellipse(width=0.63, height=0.38, stroke_width=0, fill_color=colour, fill_opacity=1),
        polygon([(-0.25, 0), (-0.49, 0.17), (-0.49, -0.17)], colour),
        Dot(point(0.18, 0.045), radius=0.037, color=BG),
    )
    return shape.scale(s).move_to(point(x, y))


def drift(obj, dx=0.35, dy=0.12, speed=1.25, phase=0):
    """A slow oscillation around a fixed landmark."""
    home = obj.get_center().copy()
    time = 0

    def update(mob, dt):
        nonlocal time
        time += dt
        mob.move_to(home + point(dx*(np.cos(speed*time+phase)-np.cos(phase)),
                                 dy*(np.sin(speed*time+phase)-np.sin(phase))))

    obj.add_updater(update)
    return obj


def site(x, colour, mode):
    ground = polygon([(x-1.98, -2.42), (x-1.98, -1.19), (x-1.46, -0.72),
                      (x-0.94, -0.43), (x-0.3, -0.62), (x+0.55, -1.04),
                      (x+1.18, -0.75), (x+1.98, -1.12), (x+1.98, -2.42)], colour)
    stratum = polygon([(x-1.98, -2.42), (x-1.98, -1.88), (x-1.21, -1.95),
                       (x-0.45, -1.77), (x+0.57, -2.04), (x+1.98, -1.79),
                       (x+1.98, -2.42)], interpolate_color(ManimColor(colour), ManimColor(BG), 0.26))
    if mode == "reef":
        crowns = VGroup(*[
            VGroup(*(line((x+d, -1.34), (x+d+e, -1.34+h), TEAL, 5)
                     for e, h in [(-0.18, 0.36), (0.03, 0.54), (0.21, 0.28)]))
            for d in (-1.23, -0.22, 0.83)
        ])
    else:
        crowns = VGroup(*[tree(x+d, y, s, interpolate_color(ManimColor(colour), ManimColor(GREEN), 0.4))
                          for d, y, s in [(-1.4, -1.12, 0.86), (-0.98, -0.94, 1.07),
                                          (0.35, -1.51, 0.88), (0.82, -1.32, 1.17),
                                          (1.37, -1.23, 0.71)]])
    return VGroup(ground, stratum, crowns)


def world(mode="land", moving=True, birds=False, sites=SITES):
    colours = REEF if mode == "reef" else LAND
    sky = polygon([(-6.45, -2.43), (-6.45, 1.15), (-4.6, 1.59),
                   (-2.55, 0.99), (-0.4, 1.52), (1.33, 1.29),
                   (3.5, 1.61), (6.45, 0.96), (6.45, -2.43)],
                  "#173747" if mode == "reef" else SKY).set_z_index(-5)
    sites_group = VGroup(*(site(x, colours[i], mode) for i, x in enumerate(sites))).set_z_index(-3)
    light = VGroup()
    for i, x in enumerate(sites):
        streak = Ellipse(width=2.20, height=0.40, stroke_width=0,
                         fill_color=TEAL if mode == "reef" else GREEN,
                         fill_opacity=0.58).move_to(point(x, -1.91+0.12*(i % 2)))
        light.add(drift(streak, 0.38, 0.09, 1.45+i*0.15, 0.45*i) if moving else streak)
    light.set_z_index(-2)
    flock = VGroup()
    if birds:
        for i, x in enumerate(sites):
            flyer = bird(x-0.05, 0.83+0.15*i, 0.71, BLUE)
            flock.add(drift(flyer, 0.5, 0.19, 1.15, i*0.35) if moving else flyer)
    return VGroup(sky, sites_group, light, flock)


def timeline(end="Years", start="", progress=0, moving=False):
    x0, x1, y = -5.85, 4.0, -2.83
    rail = line((x0, y), (x1, y), GREY, 6)
    ticks = VGroup(*(line((x, y-0.10), (x, y+0.10), GREY, 2)
                     for x in np.linspace(x0, x1, 12)))
    end_label = label(end, x1, -3.36, GOLD, 28)
    end_label.align_to(point(4.34, -3.36), RIGHT)
    labels = VGroup(end_label)
    if start:
        labels.add(label(start, x0+0.48, -3.36, TEXT, 28))
    cursor = Dot(point(x0+(x1-x0)*progress, y), radius=0.12, color=GOLD)
    if moving:
        drift(cursor, 0.09, 0, 1.7)
    return VGroup(rail, ticks, labels), cursor


def map_curve(plot, values, colour, width=7):
    """Interpolate relative values for a schematic comparison with no numeric axes."""
    xs = np.linspace(*plot.xr, len(values))
    return plot.curve(lambda x: np.interp(x, xs, values), color=colour, width=width)


def prey_curve(plot, peak):
    """Schematic seasonal prey availability centred on a relative peak date."""
    return plot.curve(lambda x: 0.10+0.78*np.exp(-((x-peak)/0.17)**2), color=GREEN, width=7)


def peak_picture(x, prey_peak, laying):
    plot = Plot((x-1.65, x+1.65, 0.28, 2.1), (0, 1), (0, 1))
    gap = line((plot.pt(prey_peak, 0)[0], 0.53), (plot.pt(laying, 0)[0], 0.53), GOLD, 5)
    return VGroup(plot, prey_curve(plot, prey_peak), plot.vline(laying, color=BLUE), gap)


def filled_meter(w, h, x, y, value, colour):
    frame = RoundedRectangle(width=w, height=h, corner_radius=0.12,
                             stroke_color=colour, stroke_width=2.5,
                             fill_color=BG, fill_opacity=0.88).move_to(point(x, y))
    inset = 0.09

    def fill_bar():
        width = (w-2*inset)*max(0.002, min(1, value.get_value()))
        return rect(width, h-2*inset, x-w/2+inset+width/2, y, colour)

    return VGroup(frame, always_redraw(fill_bar))


def site_mark(x):
    return VGroup(Dot(point(x, -0.13), radius=0.13, color=GOLD),
                  line((x, -0.33), (x, -0.60), GOLD, 3))


def cracks(x):
    return VGroup(*[
        VMobject(stroke_color=RED, stroke_width=4).set_points_as_corners(
            [point(x+d+a, b) for a, b in [(0, -1.25), (0.12, -1.52), (-0.07, -1.78), (0.17, -2.05)]])
        for d in (-0.72, -0.13, 0.49)
    ])


def flask():
    return VGroup(
        line((-0.24, 0.94), (-0.24, 1.43), BLUE),
        line((0.24, 0.94), (0.24, 1.43), BLUE),
        Polygon(point(-0.24, 0.94), point(-0.65, 0.19), point(0.65, 0.19),
                point(0.24, 0.94), stroke_color=BLUE, stroke_width=4),
    ).shift(UP*0.55)


class S01Hook(TitleCard, SpokenScene):
    LESSON = "Natural Experiments and Long-Term Studies"
    TITLE = "Finding Causes Across Sites and Years"

    def construct(self):
        landscape = world(birds=True)
        rail, cursor = timeline()
        glass = flask().set_stroke(opacity=0.43)
        q = question_card("Cause without a lab?", y=3.25, size=38)
        title = fit_text(self.TITLE, max_w=11.2, size=43, min_size=32,
                         font=TITLE_FONT).move_to(point(0, 2.34))
        self.add(landscape, rail, cursor, glass, q, schematic())
        self.at("find a cause")
        self.play(FadeIn(title), FadeOut(glass), run_time=0.43)
        self.wait(0.95)
        self.play(FadeOut(title), run_time=0.4)
        self.at("assign drought")
        dry = cracks(0)
        self.play(Create(dry), run_time=0.58)
        self.at("competitors")
        arrival = bird(0.83, 0.82, 1.02, TEAL)
        self.play(FadeIn(arrival, shift=LEFT*0.62), run_time=0.58)
        self.at("or warming")
        warmth = VGroup(*(Arc(radius=r, start_angle=0.28, angle=2.58, color=RED,
                              stroke_width=6).shift(point(0, -0.68)) for r in (1.05, 1.32, 1.6)))
        self.play(LaggedStart(*(Create(a) for a in warmth), lag_ratio=0.2), FadeOut(q), run_time=1.7)
        for a in warmth:
            pulse(a, 5, 2.5, 3.0)
        self.at("nature imposes events")
        wave = Ellipse(width=2.8, height=0.5, stroke_color=GOLD, stroke_width=5).move_to(point(0, -1))
        self.play(GrowFromCenter(wave), FadeOut(warmth), FadeOut(arrival), run_time=1.05)
        self.play(wave.animate.scale(1.25).shift(DOWN*0.35), run_time=1.05)
        self.at("following populations")
        marks = [site_mark(x) for x in SITES]
        self.play(cursor.animate.shift(RIGHT*6), FadeOut(wave), FadeOut(dry),
                  LaggedStart(*(FadeIn(m, shift=DOWN*0.35) for m in marks), lag_ratio=0.7),
                  run_time=3.85, rate_func=linear)
        self.play(FadeOut(VGroup(*marks)), run_time=0.55)
        self.finish()


class S02TwoTools(SpokenScene):
    def construct(self):
        landscape = world(birds=True)
        rail, cursor = timeline(progress=6/9.85)
        self.add(landscape, rail, cursor, schematic())
        wave = Ellipse(width=3.0, height=0.55, stroke_color=GOLD, stroke_width=5).move_to(point(0, -1.15))
        concept = heading("Natural experiment", GOLD)
        self.at("natural experiment", lead=0.55)
        self.play(GrowFromCenter(wave), run_time=0.55)
        self.play(FadeIn(concept), run_time=0.48)
        self.at("nature supplies an event")
        self.play(wave.animate.scale(1.22).shift(DOWN*0.4), run_time=1.1)
        die = RoundedRectangle(width=0.83, height=0.83, corner_radius=0.12, color=GREY,
                               stroke_width=3).move_to(point(0, 1.93))
        dots = VGroup(*(Dot(point(x, 1.93+y), radius=0.043, color=GREY)
                        for x, y in [(-0.23, -0.23), (0.23, 0.23), (0, 0), (0.23, -0.23), (-0.23, 0.23)]))
        restriction = VGroup(die, dots, line((-0.54, 1.38), (0.54, 2.48), RED, 6))
        self.at("random assignment")
        self.play(Create(restriction), FadeOut(wave), run_time=0.66)
        self.at("long -term study")
        study = heading("Long-term study", GOLD)
        plot = Plot((-3.5, 3.5, 0.55, 2.56), (0, 1), (0, 1))
        trend = map_curve(plot, (0.34, 0.38, 0.35, 0.47, 0.44, 0.49, 0.51), BLUE)
        self.play(swap(concept, study, 0.75), FadeOut(restriction), Create(plot), run_time=0.8)
        self.at("measure the same")
        self.play(Create(trend), cursor.animate.move_to(point(3.9, -2.83)), run_time=3.1, rate_func=linear)
        self.at("returning matters")
        sweep = plot.dot(lambda: 0.63, lambda: 0.46, color=GOLD)
        self.play(FadeIn(sweep), run_time=0.48)
        self.at("year's weather")
        spike = plot.curve(lambda x: 0.34+0.18*x+0.55*np.exp(-((x-0.64)/0.066)**2),
                           x0=0.49, x1=0.79, color=RED, width=7)
        self.play(Create(spike), run_time=0.68)
        self.play(FadeOut(spike), FadeOut(sweep), run_time=1.05)
        self.finish()


class S03SpaceVsTime(SpokenScene):
    def construct(self):
        landscape = world(birds=True)
        reef = world("reef")
        rail, cursor = timeline(progress=0.50)
        self.add(landscape, rail, cursor, schematic())
        self.at("comparing sites")
        self.play(ReplacementTransform(landscape, reef), run_time=1.15)
        one = heading("One year: space", GOLD)
        one_tick = line((cursor.get_x(), -3.03), (cursor.get_x(), -2.62), GOLD, 5)
        self.play(FadeIn(one), Create(one_tick), run_time=0.73)
        shoals = VGroup()
        for i, x in enumerate(SITES):
            school = VGroup(*(fish(x-1.17+0.62*(k % 4), 0.22+0.43*(k // 4),
                                   0.70+0.06*(k % 3)) for k in range(3+3*i)))
            shoals.add(drift(school, 0.20, 0.15, 1.3+0.2*i, i*0.2))
        self.at("young blue")
        self.play(LaggedStart(*(FadeIn(s, shift=RIGHT*0.53) for s in shoals), lag_ratio=0.4), run_time=2)
        crowding = Plot((-4.15, 4.15, 1.48, 2.68), (0, 1), (0, 1), stroke=2)
        slope = map_curve(crowding, (0.81, 0.63, 0.25), GOLD, 6)
        self.at("crowding effect")
        self.play(Create(crowding), Create(slope), run_time=1.35)
        self.at("pattern in space")
        pattern = heading("Pattern in space", GOLD)
        self.play(swap(one, pattern), run_time=0.75)
        self.at("showing numbers returned")
        recovery = Plot((-4.25, 4.25, 0.52, 2.64), (0, 1), (0, 1))
        recovered = map_curve(recovery, (0.78, 0.64, 0.50, 0.46, 0.43, 0.43, 0.43), BLUE)
        baseline = recovery.hline(0.43, color=GREY)
        time = heading("Records through time", GOLD)
        self.play(FadeOut(shoals), FadeOut(slope), FadeOut(crowding), FadeOut(one_tick),
                  swap(pattern, time), run_time=0.78)
        self.play(Create(recovery), Create(baseline), Create(recovered),
                  cursor.animate.shift(RIGHT*3.5), run_time=3.35, rate_func=linear)
        self.at("catch time lags")
        winter, spring = ValueTracker(0.83), ValueTracker(0.83)
        food = filled_meter(3.88, 0.57, -3.05, 0.97, winter, GREEN)
        births = filled_meter(3.88, 0.57, 3.05, 0.97, spring, BLUE)
        food_text = label("Winter food", -3.05, 1.79, GREEN)
        spring_text = label("Next spring’s births", 3.05, 1.79, BLUE)
        delay = arrow((-0.67, 0.97), (0.67, 0.97))
        lag = heading("Time lag", GOLD)
        self.play(FadeOut(recovery), FadeOut(recovered), FadeOut(baseline), swap(time, lag),
                  FadeIn(food), FadeIn(births), run_time=0.74)
        self.play(FadeIn(food_text), FadeIn(spring_text), run_time=0.45)
        self.at("winter food")
        self.play(winter.animate.set_value(0.25), run_time=0.56)
        self.play(Create(delay), run_time=0.29)
        self.at("next spring's births")
        self.play(spring.animate.set_value(0.28), run_time=0.95)
        self.finish()


class S04GuidingDesign(SpokenScene):
    def construct(self):
        reef = world("reef")
        forest = world(birds=True)
        rail, cursor = timeline()
        self.add(reef, rail, cursor, schematic())
        self.at("without random assignment")
        self.play(ReplacementTransform(reef, forest), run_time=1.25)
        year = heading("Track years", GOLD)
        compare = heading("Compare sites", TEAL)
        rivals = heading("Rule out rivals", RED)
        self.at("tracking years")
        self.play(FadeIn(year), cursor.animate.shift(RIGHT*2.9), run_time=1.05)
        self.at("comparing sites")
        pins = VGroup(*(site_mark(x) for x in SITES))
        self.play(swap(year, compare), FadeIn(pins), run_time=0.85)
        self.at("ruling out rivals")
        self.play(swap(compare, rivals), FadeOut(pins), run_time=0.9)
        self.at("mismatch is a gap")
        mismatch = heading("Prey peak and laying dates", GOLD)
        centre = peak_picture(0, 0.28, 0.77)
        self.play(swap(rivals, mismatch), FadeOut(forest[3]), FadeIn(centre), run_time=0.98)
        prey = label("Prey peak", -2.84, 1.45, GREEN, 28)
        laying = label("Laying date", 2.87, 1.45, BLUE, 28)
        self.at("the prey peak")
        self.play(FadeIn(prey), FadeIn(laying), run_time=0.6)
        self.at("both and colleagues")
        birds = heading("Dutch pied flycatchers", BLUE)
        forest_birds = VGroup(*(drift(bird(x, -0.15, 0.69, BLUE), 0.23, 0.12, 1.4)
                               for x in SITES))
        self.play(swap(mismatch, birds), FadeOut(prey), FadeOut(laying), FadeIn(forest_birds),
                  run_time=0.95)
        self.at("whose prey peaks")
        other = VGroup(peak_picture(SITES[0], 0.59, 0.77), peak_picture(SITES[2], 0.48, 0.77))
        self.play(LaggedStart(*(FadeIn(p) for p in other), lag_ratio=0.35), run_time=1.3)
        self.at("if mismatch matters")
        birth, survive = ValueTracker(0.81), ValueTracker(0.72)
        values = VGroup()
        for i, x in enumerate(SITES):
            impact = (0.4, 1, 0.65)[i]
            local_birth = ValueTracker()
            local_birth.add_updater(lambda m, d=impact: m.set_value(0.81-d*(0.81-birth.get_value())))
            local_survive = ValueTracker()
            local_survive.add_updater(lambda m, d=impact: m.set_value(0.72-d*(0.72-survive.get_value())))
            local_birth.update()
            local_survive.update()
            self.add(local_birth, local_survive)
            values.add(filled_meter(1.37, 0.31, x, -1.38, local_birth, BLUE),
                       filled_meter(1.37, 0.31, x, -1.85, local_survive, TEAL))
        key = VGroup(label("Births", 1.34, -1.38, TEXT, 28), label("Survival", 1.48, -1.85, TEXT, 28))
        self.play(FadeIn(values), FadeIn(key), run_time=0.7)
        self.at("decline should be steepest")
        self.play(birth.animate.set_value(0.26), survive.animate.set_value(0.47),
                  cursor.animate.move_to(point(4.0, -2.83)), run_time=3.15, rate_func=linear)
        self.finish()


BREEDING_RATES = (0.77, 0.75, 0.77, 0.72, 0.74, 0.72)
ADULT_RATES = (0.78, 0.75, 0.63, 0.43, 0.27, 0.14)


def survival_track(plot, values, colour, end=1):
    """Build the trace and its shading from the same schematic year-by-year rates."""
    years = np.linspace(0, 1, len(values))
    last = float(np.clip(end, 0.002, 1))
    xs = [*years[years < last], last]
    curve = VMobject(stroke_color=colour, stroke_width=7).set_points_as_corners(
        [plot.pt(x, np.interp(x, years, values)) for x in xs])
    area = Polygon(plot.pt(0, 0), *[plot.pt(x, np.interp(x, years, values)) for x in xs],
                   plot.pt(last, 0), fill_color=colour, fill_opacity=0.23, stroke_width=0)
    return VGroup(area, curve)


def breathe_track(track):
    phase = 0.0

    def update(area, dt):
        nonlocal phase
        phase += dt
        area.set_fill(opacity=0.23 + 0.18*np.sin(2.15*phase))

    track[0].add_updater(update)
    pulse(track[1], 7, 1.6, 2.7)


def predict_stage():
    ground = world(sites=(-3.2, 3.2), moving=False)
    panels = TwoPanel("Breeding and young", "Wintering adults", colors=(BLUE, TEAL),
                      top=2.45, bottom=-2.52, size=34)
    left = Plot((-5.68, -0.67, -0.88, 1.40), (0, 1), (0, 1))
    right = Plot((0.67, 5.68, -0.88, 1.40), (0, 1), (0, 1))
    lcurve = survival_track(left, BREEDING_RATES, BLUE)
    rcurve = survival_track(right, ADULT_RATES, TEAL)
    route = DashedLine(point(-2.3, -1.73), point(2.3, -1.73), color=GOLD,
                       stroke_width=4, dash_length=0.19)
    birds = VGroup(bird(-3.16, -1.74, 0.86, BLUE), bird(3.16, -1.74, 0.86, TEAL))
    rail, cursor = timeline(progress=0.79)
    return ground, panels, left, right, lcurve, rcurve, route, birds, rail, cursor, schematic()


class S05PredictQ(SpokenScene):
    def construct(self):
        ground, panels, left, right, breeding, adults, route, birds, rail, cursor, tag = predict_stage()
        start = world(birds=True)
        prey = peak_picture(-2.8, 0.24, 0.80)
        drop = Plot((0.57, 5.18, 0.28, 2.1), (0, 1), (0, 1))
        decline = map_curve(drop, (0.85, 0.77, 0.71, 0.45, 0.30, 0.18), BLUE)
        title = heading("Large mismatch", GOLD)
        numbers = label("Population numbers", 2.86, 2.54, BLUE, 28)
        cursor.shift(LEFT*3.5)
        self.add(start, prey, drop, rail, cursor, tag)
        self.at("flycatchers decline")
        self.play(Create(decline), FadeIn(numbers), run_time=1.26)
        self.at("mismatch is large")
        self.play(FadeIn(title), run_time=0.72)
        self.at("each year you track")
        self.play(ReplacementTransform(start, ground), FadeOut(prey), FadeOut(drop), FadeOut(decline),
                  FadeOut(numbers), FadeOut(title), run_time=0.75)
        self.play(FadeIn(panels.left_frame), FadeIn(panels.left_head), Create(left),
                  FadeIn(birds[0]), run_time=0.8)
        self.at("survival of young")
        self.play(FadeIn(breeding[0]), Create(breeding[1]), run_time=1.05)
        self.at("wintering adult survival")
        self.play(FadeIn(panels.right_frame), FadeIn(panels.right_head), Create(right),
                  Create(route), FadeIn(birds[1]), run_time=1.55)
        self.at("falling wintering adult")
        year = ValueTracker(0)
        live_adults = always_redraw(lambda: survival_track(right, ADULT_RATES, TEAL, year.get_value()))
        self.add(live_adults)
        self.play(year.animate.set_value(1), cursor.animate.shift(RIGHT*3.5),
                  run_time=3.4, rate_func=linear)
        self.remove(live_adults)
        self.add(adults)
        self.at("is mismatch likely")
        self.play(FadeIn(question_card(QUESTION, **QUESTION_CARD)), run_time=0.86)
        self.finish()


class S06PredictPause(PredictPause):
    QUESTION = QUESTION
    CARD = QUESTION_CARD
    RING_AT = (-6.20, -3.30, 0)
    SECONDS = 4.5

    def backdrop(self):
        parts = predict_stage()
        breathe_track(parts[4])
        breathe_track(parts[5])
        return VGroup(*parts)

    def finish(self):
        # The supplied silent clip is exactly 4.5 s, including the countdown.
        remaining = self.SECONDS - self.elapsed()
        if remaining >= 1 / config.frame_rate:
            self.wait(remaining)


class S07PredictAnswer(SpokenScene):
    def construct(self):
        ground, panels, left, right, breeding, adults, route, birds, rail, cursor, tag = predict_stage()
        question = question_card(QUESTION, **QUESTION_CARD)
        self.add(ground, panels, left, right, breeding, adults, route, birds, rail, cursor, tag, question)
        self.at("unlikely")
        answer = heading("Mismatch is unlikely", GOLD)
        self.play(swap(question, answer), route.animate.set_stroke(opacity=0.35), run_time=0.82)
        self.at("mismatch should show")
        pulse(breeding[1], base=8, amp=3, speed=2.8)
        self.play(adults[0].animate.set_fill(opacity=0.10),
                  adults[1].animate.set_stroke(opacity=0.48),
                  panels.left_frame.animate.set_stroke(width=5), run_time=1.2)
        self.at("breeding success")
        drift(birds[0], 0.23, 0.12, 1.5)
        self.at("carryover effects")
        bridge = ArcBetweenPoints(point(-2.68, -1.42), point(2.66, -1.42), angle=-0.46,
                                  color=GOLD, stroke_width=7)
        carry = heading("Carry-over effect", GOLD)
        self.play(swap(answer, carry), Create(bridge), run_time=1.25)
        pulse(bridge, base=7, amp=2.5, speed=2.7)
        drift(birds[1], 0.18, 0.11, 1.55)
        self.at("so test habitat")
        rival_label = heading("Rival causes", RED)
        markers = [label(text, x, 2.02, RED) for text, x in
                   zip(("Habitat", "Predators", "Disease"), SITES)]
        self.play(swap(carry, rival_label), FadeOut(panels), FadeOut(left), FadeOut(right),
                  FadeOut(breeding), FadeOut(adults), FadeOut(bridge), FadeOut(route), run_time=0.45)
        self.play(FadeIn(markers[0]), run_time=0.42)
        self.at("predators and disease")
        self.play(LaggedStart(*(FadeIn(m) for m in markers[1:]), lag_ratio=0.4), run_time=0.88)
        self.at("try feeding birds")
        feeder = VGroup(line((-0.26, -1.70), (-0.26, -0.65), GOLD, 5),
                        line((0.26, -1.70), (0.26, -0.65), GOLD, 5),
                        rect(1.12, 0.13, 0, -1.04, GOLD),
                        polygon([(-0.67, -0.65), (0, -0.22), (0.67, -0.65)], GREEN)).shift(LEFT*2.23)
        feeding = heading("Does food timing limit breeding?", GOLD)
        after = label("Feeding after prey peak", -3.2, 1.8, GREEN)
        self.play(FadeOut(VGroup(*markers)), swap(rival_label, feeding), GrowFromCenter(feeder),
                  cursor.animate.shift(RIGHT*1.6), run_time=1.12)
        self.play(FadeIn(after), run_time=0.69)
        self.finish()


class S08Limits(SpokenScene):
    def construct(self):
        sites = (-3.2, 3.2)
        ground = world(sites=sites, birds=True)
        rail, cursor = timeline(progress=0.95)
        self.add(ground, rail, cursor, schematic())
        self.at("wild comparisons")
        stakes = VGroup(*(site_mark(x) for x in sites))
        self.play(FadeIn(stakes, shift=DOWN*0.25), run_time=0.7)
        self.at("sites differ in soils")
        layers = VGroup(*(polygon([(x-1.97, -2.41), (x-1.97, -1.03), (x-0.94, -1.28),
                                   (x+0.21, -1.04), (x+1.97, -1.48), (x+1.97, -2.41)],
                                  SOIL[i]) for i, x in enumerate(sites)))
        self.play(FadeIn(layers, shift=DOWN*0.53), FadeOut(stakes), run_time=0.9)
        self.at("species pools")
        residents = VGroup(bird(-3.35, -0.11, 0.82, BLUE),
                           bird(3.52, -0.11, 0.94, TEAL),
                           tree(2.64, -0.64, 0.62, GREEN))
        self.play(FadeIn(residents, shift=UP*0.25), run_time=0.63)
        self.at("history")
        scar = cracks(3.2).scale(0.8).shift(DOWN*0.16)
        self.play(Create(scar), run_time=0.6)
        self.at("confounders that mimic")
        issue = heading("Confounders", RED)
        self.play(FadeIn(issue), run_time=0.6)
        self.at("statistical model")
        model = TwoPanel("Measured rival", "Unmeasured rival", colors=(TEAL, GREY),
                         top=2.63, bottom=-0.58, size=32)
        strength = ValueTracker(0.23)
        measured = filled_meter(3.72, 0.68, -3.3, 0.83, strength, TEAL)
        hidden = rect(3.65, 0.68, 3.3, 0.83, GREY, 0.16)
        model_title = heading("Statistical model", TEXT)
        self.play(swap(issue, model_title), FadeIn(model), FadeIn(measured), FadeIn(hidden),
                  FadeOut(residents), FadeOut(ground[3]), run_time=0.94)
        self.at("rival driver it")
        self.play(strength.animate.set_value(0.87), run_time=1.4)
        self.at("when it missed")
        cover = polygon([(1.4, 0.43), (1.4, 0.83), (2.55, 1.29), (3.18, 0.98),
                         (4.24, 1.28), (5.19, 0.81), (5.19, 0.43)], SOIL[1])
        self.play(FadeIn(cover, shift=UP*0.36), run_time=1.2)
        self.at("detection shows change")
        plot = Plot((-5.32, 1.32, -0.68, 2.58), (0, 1), (0, 1))
        band = rect(6.58, 0.67, -2.0, 0.74, GREY, 0.25)
        trace = map_curve(plot, (0.35, 0.46, 0.42, 0.53, 0.66, 0.87), BLUE)
        detection = heading("Detection", BLUE)
        self.play(FadeOut(model), FadeOut(measured), FadeOut(hidden), FadeOut(cover),
                  swap(model_title, detection), run_time=0.66)
        self.play(FadeIn(band), Create(plot), Create(trace), run_time=1.65, rate_func=linear)
        self.at("attribution tests")
        attribution = heading("Attribution", GOLD)
        alternatives = VGroup(*(arrow((1.55, plot.pt(1, 0.87)[1]), (4.72, y), RED, 5)
                               for y in (2.30, 1.36, 0.42)))
        self.play(swap(detection, attribution),
                  LaggedStart(*(GrowArrow(a) for a in alternatives), lag_ratio=0.27), run_time=1.53)
        self.finish()


def island():
    water = rect(12.8, 3.54, 0, -0.64, "#244957").set_z_index(-5)
    waves = VGroup(*(drift(line((a, y), (b, y), TEAL, 4), 0.3, 0.06, 1.62, i*0.25)
                    for i, (a, b, y) in enumerate([(-5.70, -3.45, -1.33), (3.8, 5.90, -0.86),
                                                    (-4.93, -2.8, -2.06), (3.5, 5.54, -1.91)])))
    earth = polygon([(-4.8, -1.47), (-4.15, -1.14), (-2.97, -0.77), (-1.8, 0.03),
                     (-0.88, 0.41), (0.08, 0.12), (1.28, -0.54), (3.3, -0.89),
                     (4.74, -1.54), (3.65, -2.03), (-3.26, -2.08)], SOIL[1])
    cap = polygon([(-4.1, -1.13), (-2.97, -0.77), (-1.8, 0.03), (-0.88, 0.41),
                   (0.08, 0.12), (1.28, -0.54), (3.3, -0.89), (3.95, -1.24),
                   (1.55, -1.15), (-0.49, -0.78), (-2.7, -1.30)], LAND[1])
    return VGroup(water, waves, earth, cap)


class S09UnlockedFinches(SpokenScene):
    def construct(self):
        terrain = island()
        rail, cursor = timeline(end="22 years")
        location = heading("Daphne Major, Galapagos", GOLD)
        seeds = VGroup(*(Ellipse(width=0.19, height=0.09, stroke_width=0, fill_color=GREEN,
                                 fill_opacity=1).rotate(0.47*(-1)**i).move_to(point(x, y))
                         for i, (x, y) in enumerate([(-2.7, -1.03), (-2.22, -1.44), (-1.58, -1.19),
                                                    (-0.89, -1.44), (-0.43, -0.94), (0.26, -1.20),
                                                    (0.8, -0.96), (1.23, -1.59), (1.84, -1.08),
                                                    (2.31, -1.47), (2.6, -1.18)])))
        medium = VGroup(bird(-4.45, 0.16, 0.93, BLUE), bird(-3.35, 0.10, 0.82, BLUE))
        self.add(terrain, rail, cursor, medium, schematic())
        self.at("on daphne major")
        self.play(FadeIn(location, run_time=0.78), medium.animate.shift(point(1.60, 0.34)),
                  run_time=2.4, rate_func=linear)
        self.at("peter and rosemary")
        self.play(FadeIn(seeds, run_time=1.12), medium.animate.shift(point(0.97, -0.81)),
                  run_time=2.45)
        drift(medium, 0.26, 0.13, 1.8)
        self.at("years after the")
        large = bird(1.82, -0.34, 1.18, TEAL, beak=0.29).flip(UP)
        arrival = label("Large ground finch arrives", -4.25, -3.36, TEAL, 28)
        self.play(FadeIn(large, shift=LEFT*1.35), FadeIn(arrival), run_time=1.35)
        drift(large, 0.18, 0.12, 1.6)
        self.at("species together severely")
        depletion = heading("Food depleted", GREEN)
        self.play(cursor.animate.move_to(point(4, -2.83)),
                  LaggedStart(*(FadeOut(seed, scale=0.25) for seed in seeds[:-1]), lag_ratio=0.33),
                  swap(location, depletion), run_time=3.4, rate_func=linear)
        self.at("their beak sizes")
        beaks = heading("Beak sizes diverge", BLUE)
        plot = Plot((-4.85, 4.85, 0.49, 2.65), (0, 1), (0, 1))
        medium_track = map_curve(plot, (0.49, 0.49, 0.49, 0.48, 0.32, 0.18), BLUE)
        large_track = map_curve(plot, (0.71, 0.72, 0.72, 0.70, 0.71, 0.71), TEAL)
        self.play(swap(depletion, beaks), Create(plot), Create(medium_track), Create(large_track),
                  run_time=1.95)
        self.at("coinciding drought")
        drought = heading("Competition vs. drought", RED)
        stress = VGroup(*(Ellipse(width=w, height=h, stroke_width=0, fill_color=RED,
                                  fill_opacity=0.27).move_to(point(x, y))
                          for w, h, x, y in ((1.65, 0.35, 2.4, 0.10), (1.16, 0.43, 2.98, 0.22),
                                              (1.32, 0.29, 3.53, 0.07))))
        self.play(swap(beaks, drought), FadeIn(stress, shift=LEFT*0.63),
                  Create(cracks(2.75)), run_time=1.2)
        drift(stress, 0.42, 0.08, 1.55)
        self.finish()


HOSTS = ("#659459", "#A58C5A")


def leaf(x, y, w, h, colour):
    shape = Ellipse(width=w, height=h, stroke_width=0, fill_color=colour, fill_opacity=1).rotate(0.26)
    vein = line((-w*0.39, -h*0.21), (w*0.39, h*0.21), interpolate_color(ManimColor(colour), ManimColor(BG), 0.33), 2.7)
    return VGroup(shape, vein).move_to(point(x, y))


def stick(x, y, scale, colour):
    trunk = line((-0.43, 0), (0.43, 0), colour, 7)
    legs = VGroup(*(line((d, 0), (d+a, b), colour, 3.5)
                    for d in (-0.23, 0.02, 0.27) for a, b in [(-0.18, -0.24), (0.12, 0.23)]))
    feelers = VGroup(line((0.40, 0), (0.62, 0.16), colour, 3),
                     line((0.4, 0), (0.62, -0.10), colour, 3))
    return VGroup(trunk, legs, feelers).scale(scale).rotate(0.25).move_to(point(x, y))


class S10UnlockedSticks(SpokenScene):
    def construct(self):
        ground = world()
        rail, cursor = timeline()
        self.add(ground, rail, cursor, schematic())
        hosts = VGroup(*(leaf(x, 0.45, 4.55, 2.28, colour) for x, colour in zip((-3.15, 3.15), HOSTS)))
        k = heading("Migration load", GOLD)
        self.at("test migration load")
        self.play(GrowFromCenter(hosts), run_time=0.84)
        self.play(FadeIn(k), run_time=0.39)
        self.at("fitness drop from")
        immigrant = stick(-3.25, 0.65, 1.47, HOSTS[1]).set_z_index(2)
        migration = CurvedArrow(point(2.55, 1.48), point(-2.34, 1.45), angle=0.47,
                                stroke_width=6, color=GOLD)
        self.play(Create(migration), FadeIn(immigrant, shift=LEFT*1.3), run_time=2.62)
        energy = ValueTracker(0.85)
        fitbar = filled_meter(2.88, 0.42, -3.15, -1.24, energy, RED)
        fit_label = label("Relative fitness", -3.15, -1.87, TEXT, 28)
        self.play(FadeIn(fitbar), FadeIn(fit_label), energy.animate.set_value(0.43), run_time=1.22)
        self.at("walking sticks")
        morphology = heading("Timema walking-sticks", TEXT)
        self.play(swap(k, morphology), FadeOut(migration), FadeOut(fitbar), FadeOut(fit_label),
                  run_time=0.8)
        drift(hosts[0], 0.37, 0.15, 1.9)
        drift(hosts[1], 0.34, 0.17, 1.6, 0.32)
        self.at("color morphs")
        examples = VGroup(stick(-3.43, 0.08, 1.33, "#4F7844"), stick(3.13, 0.61, 1.35, "#856F47"),
                          stick(2.81, -0.06, 1.28, HOSTS[0]))
        self.play(LaggedStart(*(FadeIn(m, shift=UP*0.18) for m in examples), lag_ratio=0.4), run_time=2.05)
        self.play(examples[0].animate.shift(RIGHT*0.45), examples[1].animate.shift(LEFT*0.41),
                  examples[2].animate.shift(RIGHT*0.66), run_time=1.5, rate_func=linear)
        for i, morph in enumerate(examples):
            drift(morph, 0.12, 0.06, 1.7, i*0.5)
        self.at("in 2007")
        citation = heading("Bolnick and Nosil, 2007", GOLD)
        self.play(swap(morphology, citation), run_time=0.89)
        self.at("compared 25 populations")
        grid = VGroup()
        for row in range(5):
            for col in range(5):
                x, y = -4.5+2.25*col, 1.70-0.69*row
                grid.add(leaf(x, y, 1.19, 0.41, HOSTS[(row+col//2) % 2]))
        population = heading("25 populations", GOLD)
        self.play(FadeOut(hosts), FadeOut(examples), FadeOut(immigrant), swap(citation, population),
                  run_time=0.73)
        self.play(LaggedStart(*(FadeIn(m, scale=0.76) for m in grid), lag_ratio=0.09), run_time=2.05)
        self.at("receiving more immigrants", lead=0.45)
        fork = VGroup(
            CurvedArrow(point(-4.1, 0.32), point(-2.85, -0.25), angle=-0.35, color=GOLD, stroke_width=3),
            CurvedArrow(point(-1.7, 1.02), point(1.74, 1.08), angle=-0.43, color=GOLD, stroke_width=9),
        )
        self.play(LaggedStart(*(Create(a) for a in fork), lag_ratio=0.24), run_time=1.36)
        self.at("more poorly matched", lead=0.45)
        low, high = ValueTracker(0.19), ValueTracker(0.19)
        meter_low = filled_meter(2.25, 0.35, -2.25, 2.36, low, RED)
        meter_high = filled_meter(2.25, 0.35, 2.25, 2.36, high, RED)
        mismatch = heading("Camouflage mismatch", RED)
        meter_label = label("Mismatch", 0, 2.36, RED, 28)
        self.play(swap(population, mismatch), FadeIn(meter_low), FadeIn(meter_high),
                  FadeIn(meter_label), run_time=0.7)
        self.play(high.animate.set_value(0.88), low.animate.set_value(0.37), run_time=0.85)
        self.at("selection shifted")
        shift = heading("Selection shifts morphs", BLUE)
        contrast = VGroup(arrow((-2.92, -1.58), (-1.97, -1.58), BLUE, 4),
                          arrow((1.37, -1.58), (3.22, -1.58), BLUE, 10))
        self.play(swap(mismatch, shift), LaggedStart(*(GrowArrow(a) for a in contrast), lag_ratio=0.35),
                  run_time=1.7)
        self.at("a correlation")
        cap = caption("Correlation, not manipulation", size=32, color=GOLD, y=-3.36)
        cap.set_x(-2.35)
        self.play(FadeIn(cap), cursor.animate.shift(RIGHT*7.5), run_time=1.68)
        self.finish()


# Simplified continent outlines for the schematic geographic comparison.
CONTINENTS = (
    ((-5.8, 1.65), (-5.26, 2.5), (-4.1, 2.51), (-3.55, 2.19), (-2.62, 2.06),
     (-2.35, 1.46), (-3.17, 1.04), (-3.80, 0.77), (-3.95, 0.36), (-4.35, 0.40),
     (-4.36, 0.87), (-5.18, 1.03)),
    ((-3.68, 0.23), (-2.91, 0.25), (-2.34, -0.42), (-2.71, -1.24), (-2.89, -1.85),
     (-3.19, -2.19), (-3.47, -1.49), (-3.54, -0.68), (-4.00, -0.30)),
    ((-0.9, 1.18), (-0.67, 1.79), (0.07, 2.08), (0.54, 2.55), (2.25, 2.46), (3.24, 2.18),
     (4.86, 2.27), (5.89, 1.77), (5.11, 1.45), (4.45, 1.01), (3.55, 0.94), (2.89, 0.34),
     (2.24, 0.44), (1.93, -0.03), (1.33, 0.69), (0.57, 0.88), (0.04, 1.24)),
    ((-0.63, 0.83), (0.41, 0.79), (1.20, 0.08), (0.53, -1.33), (0.09, -1.44),
     (-0.16, -0.54), (-0.82, -0.18), (-1.00, 0.37)),
    ((3.76, -0.8), (4.4, -0.61), (5.28, -0.79), (5.69, -1.41), (5.44, -1.86),
     (4.50, -1.66), (3.92, -1.79)),
)


class S11UnlockedWarming(SpokenScene):
    def construct(self):
        landscape = world(birds=True)
        rail, cursor = timeline()
        map_bg = rect(12.5, 5.15, 0, 0.03, SKY).set_z_index(-5)
        continents = VGroup(*(polygon(outline, LAND[1]) for outline in CONTINENTS))
        tint = VGroup(*(polygon(outline, SOIL[1]) for outline in CONTINENTS))
        attribution = heading("Rosenzweig et al., 2008", GOLD)
        self.add(landscape, rail, cursor, schematic())
        self.at("in 2008")
        self.play(FadeOut(landscape), FadeIn(map_bg), LaggedStart(*(FadeIn(c, scale=0.84) for c in continents),
                  lag_ratio=0.2), run_time=1.4)
        self.play(FadeIn(attribution), run_time=0.55)
        self.at("continental -scale warming")
        warm = heading("Continental warming", RED)
        self.play(swap(attribution, warm), LaggedStart(*(FadeIn(c) for c in tint), lag_ratio=0.33),
                  cursor.animate.shift(RIGHT*2.6), run_time=1.9)
        self.at("observed biological")
        observations = heading("Biological and physical shifts", BLUE)
        shifts = VGroup(*(arrow((x, y), (x, y+0.64), BLUE, 6)
                          for x, y in [(-4.32, 0.92), (-3.1, -1.11), (0.18, 0.33),
                                       (1.15, 1.25), (3.45, 1.05), (4.57, -1.48)]))
        self.play(swap(warm, observations),
                  LaggedStart(*(GrowArrow(a) for a in shifts), lag_ratio=0.37), run_time=2.8)
        self.at("natural climate variation")
        chance = heading("Natural variation alone falls short", TEXT)
        back = rect(8.9, 3.24, 0, -0.15, "#1C313C")
        plot = Plot((-3.99, 3.99, -1.42, 1.20), (0, 1), (0, 1))
        band = rect(7.92, 0.59, 0, -0.32, GREY, 0.30)
        observed = map_curve(plot, (0.32, 0.34, 0.46, 0.54, 0.78, 0.88), BLUE)
        chart = VGroup(back, plot, band)
        self.play(swap(observations, chance), FadeOut(shifts), FadeIn(chart), run_time=1.16)
        self.play(Create(observed), cursor.animate.shift(RIGHT*2.6), run_time=2.75, rate_func=linear)
        self.at("data clustered")
        sample = heading("Biased global sample", GOLD)
        dots = VGroup()
        for x, y, offsets in [
            (-4.2, 1.62, [(-0.58, 0.17), (-0.39, -0.05), (-0.16, 0.33), (0.09, 0.10),
                          (0.35, -0.21), (0.46, 0.33), (0.57, -0.04), (0.84, 0.09)]),
            (0.10, 1.60, [(-0.56, -0.09), (-0.32, -0.23), (-0.21, 0.18), (0.02, 0.02),
                         (0.34, 0.24), (0.53, -0.03), (0.74, 0.22)]),
            (0, 0, [(-3.15, -0.84), (0.35, -0.20), (3.38, 1.45), (5.04, -1.16)]),
        ]:
            for a, b in offsets:
                dots.add(Dot(point(x+a, y+b), radius=0.085, color=GOLD))
        self.play(FadeOut(chart), FadeOut(observed), swap(chance, sample), run_time=0.92)
        self.play(LaggedStart(*(GrowFromCenter(d) for d in dots), lag_ratio=0.19), run_time=2.12)
        self.at("track years and sites")
        final_landscape = world(birds=True)
        self.play(FadeOut(map_bg), FadeOut(continents), FadeOut(tint), FadeOut(dots), FadeOut(sample),
                  FadeIn(final_landscape), cursor.animate.shift(RIGHT*1.57), run_time=1.05)
        self.at("test rivals")
        checks = VGroup()
        for x in SITES:
            pair = VGroup()
            for sign in (-1, 1):
                edge, inset = x+sign*0.53, x+sign*0.34
                bracket = VMobject(stroke_color=RED, stroke_width=5).set_points_as_corners(
                    [point(inset, 0.38), point(edge, 0.38), point(edge, -0.39), point(inset, -0.39)])
                pair.add(bracket)
            checks.add(pair)
        pins = VGroup(*(site_mark(x) for x in SITES))
        self.play(FadeIn(pins), LaggedStart(*(FadeIn(c, scale=1.36) for c in checks), lag_ratio=0.46),
                  cursor.animate.shift(RIGHT*2.80), run_time=3.05, rate_func=linear)
        self.finish()


class S12End(EndCard):
    LINE = "Follow populations for years, compare sites, and test every rival cause."
