"""Testing Treatments and Tracing Causes.

TEAL: treatment. GOLD: comparison and dates. BLUE: people and clinical outcomes.
PURPLE: biological observations. ORANGE: exposure and relapse. RED: harm.
Grey outlines are apparatus, paths and masks. All plots without units are schematic.
"""
from bp_parts import *

PURPLE = "#B58CD9"
ORANGE = "#F29E4C"
STAGE = "#2B384B"
MASK = "#354354"
LEFT_X, RIGHT_X = -6.05, 5.65
QUESTION = "What must the placebo curve do?"
SHADES = (BLUE, TEXT, "#85A4C5", "#A2BECD")


def point(x, y):
    return np.array([x, y, 0.0])


def label(text, x=0, y=3.16, color=TEXT, size=34):
    return fit_text(text, max_w=11.2, size=size, min_size=28, color=color).move_to(point(x, y))


def plate(w, h, x, y, color=STAGE, fill=1, edge=None):
    return RoundedRectangle(
        width=w, height=h, corner_radius=0.19, fill_color=color, fill_opacity=fill,
        stroke_color=edge or color, stroke_width=2 if edge else 0,
    ).move_to(point(x, y))


def path_between(fn, start=0, stop=1, steps=80):
    return [fn(u) for u in np.linspace(start, stop, steps)]


def path(fn, color, width=4, start=0, stop=1):
    return VMobject().set_points_as_corners(path_between(fn, start, stop)).set_stroke(color, width)


def ribbon(fn, color, half_width, opacity=1):
    centers = path_between(fn, steps=54)
    return Polygon(
        *(p + UP * half_width for p in centers),
        *(p - UP * half_width for p in reversed(centers)),
        fill_color=color, fill_opacity=opacity, stroke_width=0,
    )


def flow(route, count=28, speed=0.10, spread=0.6, colors=SHADES, radius=0.078):
    """The beads encode people. A wrapped bead fades at both ends of the path."""
    beads = VGroup(*[Dot(radius=radius, color=colors[i % len(colors)]) for i in range(count)])
    clock = 0.0

    def advance(group, dt):
        nonlocal clock
        clock += dt
        for i, bead in enumerate(group):
            u = (i / count + (i % 4) * 0.019 + clock * speed) % 1
            offset = spread * (0.72 * np.sin(i * 2.4) + 0.22 * np.sin(clock * 2.1 + i))
            bead.move_to(route(i, u) + UP * offset)
            bead.set_opacity(min(1, u * 14, (1 - u) * 14))

    beads.add_updater(advance)
    advance(beads, 0)
    return beads


def lane_route(i, u, split=1):
    x = interpolate(LEFT_X, RIGHT_X, u)
    if split < 0:
        return point(x, 1.60 - 3.05 * u)
    branch = np.clip((u - 0.39) / 0.31, 0, 1)
    branch = branch * branch * (3 - 2 * branch)
    direction = 1 if (i % 7) in (0, 2, 3, 6) else -1
    return point(x, split * direction * branch * 1.52)


def lane_beds(split=1):
    if split < 0:
        route = lambda u: lane_route(0, u, -1)
        return VGroup(ribbon(route, STAGE, 1.14), path(route, BLUE, 4))
    upper = lambda u: lane_route(0, u)
    lower = lambda u: lane_route(1, u)
    return VGroup(ribbon(upper, STAGE, 0.94), ribbon(lower, STAGE, 0.94),
                  path(upper, TEAL), path(lower, GOLD))


def gate(x=-1.40, y=0, radius=0.71):
    center = point(x, y)
    coin = Circle(radius=radius, stroke_color=BLUE, stroke_width=3.5,
                  fill_color=BG, fill_opacity=1).move_to(center)
    marks = VGroup()
    for a in np.arange(6) * TAU / 6:
        direction = np.array([np.cos(a), np.sin(a), 0])
        marks.add(Line(center + direction * radius * 0.33,
                       center + direction * radius * 0.72, color=BLUE, stroke_width=4))
    marks.add(Dot(center, radius=radius * 0.15, color=TEXT))
    marks.add_updater(lambda m, dt: m.rotate(1.8 * dt, about_point=center))
    return VGroup(coin, marks)


def clipboard(x, y):
    board = plate(1.45, 1.9, x, y, MASK, edge=GREY)
    clip = plate(0.54, 0.25, x, y + 0.91, GREY)
    lines = VGroup(*[
        Line(point(x - 0.42, y + dy), point(x + 0.42, y + dy), color=TEXT, stroke_width=3)
        for dy in (0.43, 0.04, -0.35)
    ])
    return VGroup(board, clip, lines)


def pill(x, y, active):
    shell = plate(1.26, 0.52, x, y, BG, edge=TEXT)
    center = Line(point(x, y - 0.21), point(x, y + 0.21), color=GREY, stroke_width=2)
    content = Dot(point(x + 0.28, y), radius=0.15, color=TEAL).set_opacity(1 if active else 0)
    return VGroup(shell, center, content)


def shutter(w, h, x, y):
    return plate(w, h, x, y, MASK, edge=GREY)


def plaque(x, y, size=1.0):
    return VGroup(*[
        Dot(point(x + dx * size, y + dy * size), radius=r * size, color=PURPLE).set_opacity(0.8)
        for dx, dy, r in ((0, 0, .32), (.30, .11, .22), (-.23, .18, .21), (.12, -.21, .23), (-.24, -.13, .18))
    ])


def decline(end):
    # Schematic straight interpolation, anchored to the sign-reversed Clarity AD
    # 18-month CDR-SB changes (van Dyck et al., doi:10.1056/NEJMoa2212948).
    return lambda month: -end * month / 18


def trial_plot():
    graph = Plot(box=(-5.8, 3.9, -2.52, 2.13), xr=(0, 18), yr=(-1.77, 0.16),
                 xticks=[0, (18, "18 months")], ylabel="Clinical status",
                 size=28, label_size=28, stroke=2)
    back = plate(10.02, 4.8, -0.96, -0.20)
    return graph, back, scope_tag(size=28)


def trend_field(graph, fn, color, alpha=0.25):
    curve_points = [graph.pt(month, fn(month)) for month in np.linspace(0, 18, 36)]
    return Polygon(
        *curve_points, graph.pt(18, graph.yr[0]), graph.pt(0, graph.yr[0]),
        stroke_width=0, fill_color=color, fill_opacity=alpha,
    )


def trend_people(graph, end, colors=(TEXT, TEAL), count=26):
    return flow(lambda i, u: graph.pt(18 * (0.018 + 0.964 * u), decline(end)(18 * (0.018 + 0.964 * u))),
                count=count, speed=0.17, spread=0.25, colors=colors, radius=0.13)


def lec_world():
    graph, back, schematic = trial_plot()
    fn = decline(1.21)
    field = trend_field(graph, fn, TEAL, 0.24)
    lec = VGroup(graph.curve(fn, color=TEAL, width=7), trend_people(graph, 1.21))
    title = label("Lecanemab", 2.40, 1.20, TEAL)
    return graph, back, schematic, field, lec, title


def prediction():
    cover = shutter(1.94, 1.61, 5.19, -1.38)
    question_mark = label("?", 5.19, -1.36, GOLD, 55)
    tag = label("Placebo", 5.19, -0.23, GOLD, 29)
    q = question_card(QUESTION, y=3.16, size=38)
    return cover, question_mark, tag, q


class S01Hook(SpokenScene, TitleCard):
    TITLE = "Testing Treatments and Tracing Causes"
    LESSON = "Randomized controlled trials"

    def construct(self):
        beds = lane_beds(-1)
        cloud = flow(lambda i, u: lane_route(i, u, -1), count=45, speed=0.15, spread=0.9)
        schematic = scope_tag(size=28)
        self.add(beds, cloud, schematic)
        self.at("What if every")
        question = question_card("Getting worse — still working?", y=3.19, size=39)
        self.play(FadeIn(question, shift=UP * 0.1), run_time=0.52)
        self.at("Could it still")
        pulse(beds[1], base=5, amp=2.1, speed=2.0)
        self.at("Illness changes on")
        drift = ribbon(lambda u: lane_route(0, u, -1), BLUE, 0.68, 0.21)
        self.play(FadeIn(drift), run_time=0.62)
        self.at("knowing who got")
        board = clipboard(4.38, 1.46)
        self.play(FadeIn(board, shift=LEFT * 0.2), run_time=0.48)
        self.play(Rotate(board, -0.22), run_time=1.30)
        self.at("Clinical trials and")
        self.play(FadeOut(question), FadeOut(board), FadeOut(drift), run_time=0.43)
        beds[1].clear_updaters()
        split = ValueTracker(0)
        cloud.clear_updaters()
        moving = flow(
            lambda i, u: interpolate(lane_route(i, u, -1), lane_route(i, u), split.get_value()),
            count=45, speed=0.15, spread=0.75,
        )
        self.remove(cloud)
        self.add(moving)
        self.play(ReplacementTransform(beds, lane_beds()), split.animate.set_value(1), run_time=2.8)
        self.finish()


class S02Title(TitleCard):
    TITLE = "Testing Treatments and Tracing Causes"
    LESSON = "Randomized controlled trials"

    def construct(self):
        self.add(lane_beds(), flow(lane_route, count=45, speed=0.14, spread=0.75))
        shade = Rectangle(width=13.2, height=7.4, stroke_width=0, fill_color=BG, fill_opacity=0.66)
        backing = plate(8.0, 2.95, 0, .02, BG)
        title = T(self.TITLE.replace(" and ", "\nand ", 1), 52, font=TITLE_FONT, line_spacing=0.9).move_to(UP * 0.22)
        rule = Line(point(-1.08, -1.22), point(1.08, -1.22), color=GOLD, stroke_width=4)
        self.play(FadeIn(shade), FadeIn(backing), run_time=.20)
        self.play(FadeIn(title), Create(rule), run_time=.34)
        self.wait(.94)
        self.play(FadeOut(title), FadeOut(rule), run_time=.27)
        self.play(FadeOut(shade), FadeOut(backing), run_time=.20)


class S03Randomize(SpokenScene):
    def construct(self):
        self.add(lane_beds())
        cloud = flow(lane_route, count=56, speed=0.17, spread=0.67)
        self.add(cloud)
        self.at("To test a")
        coin = gate()
        self.play(FadeIn(coin, scale=0.7), run_time=0.55)
        self.at("split one group")
        chance = label("Chance assignment", -1.40, 2.89, BLUE)
        self.play(FadeIn(chance), run_time=0.52)
        self.at("That chance split")
        random = label("Randomized trial", -0.90, 3.14, BLUE, 38)
        self.play(swap(chance, random, 0.75))
        self.at("both groups start")
        mix = VGroup(*[Dot(point(2.62 + i * .33, y), radius=.105, color=c)
                       for y in (2.80, -2.77) for i, c in enumerate(SHADES)])
        self.play(FadeIn(mix), run_time=0.48)
        self.at("One group gets")
        treated = label("Treated", 4.03, 2.93, TEAL)
        active = pill(4.10, 1.55, True)
        self.play(FadeOut(mix), FadeIn(active), run_time=0.44)
        self.play(FadeIn(treated), run_time=0.38)
        self.at("the other gets")
        dummy = pill(4.10, -1.51, False)
        self.play(FadeIn(dummy), run_time=0.44)
        self.at("a placebo")
        control = label("Placebo", 4.03, -2.91, GOLD)
        self.play(FadeIn(control), run_time=0.48)
        self.at("Neither patient nor")
        board = clipboard(-4.55, 2.12)
        self.play(FadeIn(board), FadeOut(random), run_time=0.48)
        covers = VGroup(shutter(2.28, .60, 4.03, 2.93), shutter(2.28, .60, 4.03, -2.91),
                        shutter(1.52, 1.99, -4.55, 2.12))
        self.at("rater knows which", lead=-.22)
        self.play(FadeOut(treated), FadeOut(control), FadeOut(board), FadeOut(active[2]), run_time=0.38)
        self.play(FadeIn(covers, shift=LEFT * .30), run_time=0.62)
        self.at("keeping the trial")
        self.play(FadeIn(label("Double-blind", -0.85, 3.13, BLUE, 40)), run_time=0.50)
        self.finish()


class S04PredictQ(SpokenScene):
    def construct(self):
        graph, back, schematic, field, lec, lec_name = lec_world()
        cover, mark, placebo, question = prediction()
        beds = lane_beds()
        cloud = flow(lane_route, count=45, speed=.14, spread=.75)
        self.add(beds, cloud)
        self.at("Take a large")
        heading = label("Early Alzheimer disease", -0.45, 3.17, TEXT, 38)
        self.play(ReplacementTransform(beds, back), FadeOut(cloud), FadeIn(graph.axes), FadeIn(schematic), run_time=1.25)
        self.play(FadeIn(heading), FadeIn(graph.ylabel), run_time=0.46)
        self.play(FadeIn(field), Create(lec[0]), run_time=2.03)
        self.add(lec[1])
        self.at("People received")
        self.play(FadeIn(lec_name), run_time=0.37)
        self.at("that clears amyloid")
        deposits = VGroup(*[plaque(-4.5 + 1.14 * i, y, 0.58)
                            for i, y in enumerate((.58, .16, -.25))])
        self.play(FadeIn(deposits), run_time=0.46)
        self.play(LaggedStart(*[ShrinkToCenter(p) for p in deposits], lag_ratio=.45), run_time=2.6)
        self.at("or a placebo")
        self.play(FadeIn(cover), FadeIn(mark), FadeIn(placebo), run_time=0.56)
        self.at("18 months")
        self.play(FadeIn(graph.ticks), FadeIn(graph.tick_labels), run_time=0.48)
        self.at("Suppose treated patients")
        pulse(lec[0], base=7, amp=2, speed=2.0)
        self.at("What must the")
        self.play(swap(heading, question, 0.70))
        self.finish()


class S05PredictPause(NarratedScene):
    def construct(self):
        graph, back, schematic, field, lec, name = lec_world()
        cover, mark, placebo, question = prediction()
        self.add(back, field, graph, lec, name, cover, mark, placebo, question, schematic)
        # Keep the prompt fixed while the three possible comparison paths take turns.
        for endpoint in (0.85, 1.21, 1.66):
            fn = decline(endpoint)
            option = DashedVMobject(graph.curve(fn, x0=1.6, x1=17.8, color=GOLD, width=4), num_dashes=27)
            option.set_stroke(opacity=.82 if endpoint == 1.21 else .54)
            self.play(FadeIn(option), run_time=5 / 15)
            self.wait(11 / 15)
            self.play(FadeOut(option), run_time=6 / 15)


class S06Reveal(SpokenScene):
    def construct(self):
        graph, back, schematic, field, lec, lec_name = lec_world()
        cover, mark, control_name, question = prediction()
        self.add(back, field, graph, lec, lec_name, cover, mark, control_name, question, schematic)
        self.at("The placebo group")
        self.play(FadeOut(cover, shift=DOWN * 0.12), FadeOut(mark), FadeOut(question),
                  FadeOut(control_name), run_time=0.53)
        control = graph.curve(decline(1.66), color=GOLD, width=7)
        lower = trend_field(graph, decline(1.66), GOLD, .24).set_z_index(-1)
        back.set_z_index(-2)
        self.play(Create(control), FadeIn(lower), run_time=2.35)
        self.play(FadeIn(label("Placebo", 5.22, -2.26, GOLD, 29)), run_time=.33)
        self.add(trend_people(graph, 1.66, (TEXT, GOLD), count=23))
        self.at("Both groups got")
        pulse(control, base=7, amp=2.4, speed=1.75)
        self.at("yet treated patients")
        pulse(lec[0], base=7, amp=2.4, speed=1.75)
        self.at("The gap between")
        a = graph.pt(18, -1.21)
        b = graph.pt(18, -1.66)
        x = a[0] + 0.21
        bracket = VGroup(Line(point(x, a[1]), point(x, b[1]), color=TEXT, stroke_width=4),
                         Line(a, point(x + 0.12, a[1]), color=TEXT, stroke_width=4),
                         Line(b, point(x + 0.12, b[1]), color=TEXT, stroke_width=4))
        formula = label("Effect = Treated − Placebo", -0.40, 3.18, TEXT, 37)
        self.play(Create(bracket), run_time=.55)
        self.play(FadeIn(formula), run_time=.57)
        self.at("Decline slowed without")
        shade = Polygon(*path_between(lambda u: graph.pt(18 * u, decline(1.21)(18 * u)), steps=42),
                        *reversed(path_between(lambda u: graph.pt(18 * u, decline(1.66)(18 * u)), steps=42)),
                        fill_color=TEAL, fill_opacity=.30, stroke_width=0).set_z_index(-1)
        self.play(FadeIn(shade), run_time=1.18)
        self.at("Random assignment and")
        coin = gate(5.18, 1.18, .46)
        blind = shutter(.95, .49, 5.18, -1.18)
        self.play(FadeIn(coin), run_time=.55)
        self.play(FadeIn(blind, shift=LEFT * .18), run_time=.55)
        self.finish()


def meter(x, y, title, color):
    track = plate(3.36, .52, x, y, BG, edge=GREY)
    reading = plate(1.13, .25, x, y, color)
    center = point(x, y)
    angle = 0.0

    def scan(mob, dt):
        nonlocal angle
        angle += dt * 2.0
        mob.move_to(center + RIGHT * .86 * np.sin(angle))

    reading.add_updater(scan)
    return VGroup(track, reading, label(title, x, y + .65, color, 29))


class S07Limits(SpokenScene):
    def construct(self):
        bed = plate(11.70, 4.91, -.22, -.06)
        schematic = scope_tag(size=28)
        deposits = VGroup(*[plaque(-2.72 + dx, dy, r) for dx, dy, r in
                            ((0, .12, 1.34), (-1.17, -.74, .88), (1.08, -.7, .97), (.77, 1.10, .68))])
        for i, cluster in enumerate(deposits):
            bob(cluster, amp=.15, speed=1.8, seed=i)
        dish = Circle(radius=1.99, color=PURPLE, stroke_width=4, fill_color=BG,
                      fill_opacity=.36).move_to(point(-2.73, -.13))
        self.add(bed, dish, deposits, schematic)
        self.at("Even a biological")
        deposit_title = label("Biological deposit", -2.68, 2.98, PURPLE, 37)
        self.play(FadeIn(deposit_title), run_time=.56)
        self.at("An autopsy deposit")
        pulse(dish, base=4, amp=2, speed=1.5)
        focus = Circle(radius=.98, color=TEXT, stroke_width=3).move_to(point(-2.72, .12))
        self.play(Create(focus), run_time=1.2)
        self.at("Trials judge clinical")
        clinical = label("Clinical outcomes", .64, 3.13, BLUE, 39)
        thinking = meter(-2.8, .75, "Thinking", BLUE)
        daily = meter(1.36, .75, "Daily function", BLUE)
        survival = meter(-2.8, -1.24, "Survival", BLUE)
        harm_level = ValueTracker(.30)
        harm_gauge = dial(harm_level, point(1.36, -1.51), radius=.90, color=RED, fmt="—", size=30)
        harm_gauge.remove(harm_gauge[-1])  # a schematic instrument with no measured value
        harms_name = label("Harms", 1.36, -.25, RED, 29)
        tracks = VGroup(thinking[0], daily[0], survival[0], harm_gauge[0])
        self.play(FadeOut(deposits), FadeOut(dish), FadeOut(focus), FadeOut(deposit_title), run_time=.38)
        self.play(FadeIn(clinical), FadeIn(tracks, shift=UP * .12), run_time=.49)
        self.at("like thinking")
        self.play(FadeIn(thinking[1]), FadeIn(thinking[2]), run_time=.42)
        self.at("daily function")
        self.play(FadeIn(daily[1]), FadeIn(daily[2]), run_time=.42)
        self.at("or survival")
        self.play(FadeIn(survival[1]), FadeIn(survival[2]), run_time=.42)
        self.at("measure harms")
        self.play(FadeIn(harm_gauge[1]), FadeIn(harm_gauge[2]), FadeIn(harms_name), run_time=.42)
        self.play(harm_level.animate.set_value(.70), run_time=.76)

        self.at("In fragile x")
        graph, back, _ = trial_plot()
        heading = label("Fragile X syndrome", -.55, 3.14, TEXT, 38)
        lanes = lane_beds()
        cohort = flow(lane_route, count=40, speed=.13, spread=.63)
        indications = VGroup(*thinking[1:], *daily[1:], *survival[1:], *harm_gauge[1:], harms_name)
        self.play(FadeOut(clinical), FadeOut(tracks), FadeOut(indications), run_time=.36)
        self.play(ReplacementTransform(bed, lanes), run_time=.65)
        self.play(FadeIn(heading), FadeIn(cohort), run_time=.55)
        self.at("in 2016")
        mav = label("Mavoglurant 2016", -3.24, -3.09, TEAL, 30)
        self.play(FadeIn(mav), run_time=.44)
        self.at("in 2018")
        bas = label("Basimglurant 2018", .74, -3.09, TEAL, 30)
        self.play(FadeIn(bas), run_time=.44)
        self.at("tested against placebo")
        self.play(FadeOut(cohort), ReplacementTransform(lanes, back), FadeIn(graph.axes), run_time=.53)
        treated = lambda t: -.96 + .33 * (1 - np.exp(-t / 6))
        comparison = lambda t: treated(t) - .06 * (1 - np.exp(-t / 6))
        p_band = ribbon(lambda u: graph.pt(18 * u, comparison(18 * u)), GOLD, .39, .27)
        t_band = ribbon(lambda u: graph.pt(18 * u, treated(18 * u)), TEAL, .39, .31)
        teal = graph.curve(treated, color=TEAL, width=6)
        gold = DashedVMobject(graph.curve(comparison, color=GOLD, width=5), num_dashes=30)
        self.play(FadeIn(p_band), FadeIn(t_band), Create(teal), Create(gold), run_time=1.32)
        self.add(flow(lambda i, u: graph.pt(18 * (.035 + .93 * u),
                                           (treated if i % 2 else comparison)(18 * u)),
                      count=35, speed=.16, spread=.34, colors=(GOLD, TEAL), radius=.125))
        self.at("beat placebo on")
        self.play(FadeIn(label("No clear advantage", -.20, 1.32, TEXT, 34)), run_time=.56)
        self.finish()


def map_route(i, u):
    return point(interpolate(LEFT_X, RIGHT_X, u), .47 * np.sin(TAU * (u - .13))
                 + (i % 3 - 1) * .78)


def map_parts():
    beds = VGroup(*[ribbon(lambda u, i=i: map_route(i, u), STAGE, .64) for i in range(3)])
    traces = VGroup(*[path(lambda u, i=i: map_route(i, u), BLUE, 2) for i in (0, 2)])
    people = flow(map_route, count=48, speed=.13, spread=.22)
    return beds, traces, people


def exposure_wave():
    return ribbon(lambda u: point(interpolate(-3.05, 3.75, u), .61 * np.sin(TAU * u)),
                  ORANGE, 1.08, .31)


def animal_badge(x, y):
    shell = Circle(radius=.94, color=PURPLE, stroke_width=3, fill_color=STAGE,
                   fill_opacity=1).move_to(point(x, y))
    body = Ellipse(width=.99, height=.53, stroke_width=0, fill_color=PURPLE, fill_opacity=1).move_to(point(x, y-.04))
    head = Circle(radius=.26, stroke_width=0, fill_color=PURPLE, fill_opacity=1).move_to(point(x+.47, y+.12))
    ear = Circle(radius=.11, stroke_width=0, fill_color=PURPLE, fill_opacity=1).move_to(point(x+.34, y+.35))
    eye = Dot(point(x+.55, y+.16), radius=.04, color=BG)
    tail = CubicBezier(point(x-.46,y-.05), point(x-.79,y-.27), point(x-.88,y+.36), point(x-.61,y+.29),
                      color=PURPLE, stroke_width=3)
    return VGroup(shell, body, head, ear, eye, tail)


class S08Epidemiology(SpokenScene):
    def construct(self):
        beds = lane_beds()
        coin = gate()
        cloud = flow(lane_route, count=38)
        self.add(beds, cloud, coin)
        self.at("You cannot randomly")
        hazard = Triangle(color=RED, fill_color=RED, fill_opacity=.23, stroke_width=4).scale(.63).move_to(point(3.75, -.01))
        symbol = label("!", 3.75, -.06, RED, 37)
        self.play(FadeIn(hazard), FadeIn(symbol), run_time=.46)
        self.at("a harmful drug")
        stop = Line(point(-2.04, -.65), point(-.76, .65), color=RED, stroke_width=8)
        self.play(Create(stop), run_time=.57)
        self.at("Instead epidemiology tracks")
        map_beds, traces, people = map_parts()
        self.play(FadeOut(coin), FadeOut(cloud), FadeOut(stop), FadeOut(hazard), FadeOut(symbol), run_time=.42)
        self.remove(beds)
        self.add(*beds)
        self.play(ReplacementTransform(VGroup(*beds[:2]), map_beds), FadeOut(VGroup(*beds[2:])),
                  run_time=1.02)
        self.add(traces, people)
        wave = exposure_wave()
        wave.set_z_index(-1)
        map_beds.set_z_index(-2)
        self.play(FadeIn(wave), run_time=.67)
        self.at("called cohorts")
        cohort_label = label("Cohorts", -.35, 3.13, BLUE, 40)
        self.play(FadeIn(cohort_label), run_time=.44)
        self.at("across time and place")
        axis_label = label("Time and place", -.4, -2.96, TEXT, 30)
        schematic = scope_tag(size=28)
        self.play(FadeIn(axis_label), FadeIn(schematic), run_time=.52)

        self.at("A small cohort")
        tiny = VGroup(*[Dot(point(-4.78 + .48 * i, y), radius=.19, color=BLUE)
                        for i, y in enumerate((-.19, .16, -.07, .22))])
        bob(tiny, amp=.31, speed=1.65)
        self.play(FadeOut(people), FadeOut(cohort_label), FadeOut(traces), FadeIn(tiny),
                  wave.animate.set_opacity(.14), run_time=.87)
        small_band = ribbon(lambda u: point(-5.54 + 7.78 * u, .20 * np.sin(TAU * u)),
                            STAGE, .70).set_z_index(-2)
        self.play(ReplacementTransform(map_beds, small_band), run_time=1.3)
        self.at("shows feasibility")
        feasibility = label("Feasibility only", -3.99, 1.49, BLUE, 32)
        self.play(FadeIn(feasibility), run_time=.45)
        tiny.clear_updaters()
        self.play(tiny.animate.shift(RIGHT * 1.68), run_time=2.53, rate_func=linear)

        self.at("Defects after isotretinoin")
        human = flow(lambda i, u: point(-5.20 + 2.70 * u, .35),
                     count=15, speed=.24, spread=.78, radius=.13)
        event = label("Isotretinoin 1985", -3.90, 2.85, GOLD, 32)
        tick = Line(point(-3.92, 2.50), point(-3.92, 1.77), color=ORANGE, stroke_width=4)
        self.play(FadeOut(feasibility), FadeOut(tiny), FadeOut(axis_label),
                  FadeIn(human), run_time=.55)
        self.play(FadeIn(event), Create(tick), run_time=.55)
        self.at("fit animal results")
        animal = animal_badge(3.08, .35)
        self.play(FadeIn(animal), run_time=.53)
        bob(animal, amp=.23, speed=2.0)
        self.at("human mechanism stayed")
        tie = DashedLine(point(-2.22, .35), point(1.95, .35), color=PURPLE, stroke_width=5, dash_length=.18)
        inferred = label("Inferred", -.22, 1.10, PURPLE, 32)
        self.play(Create(tie), run_time=.70)
        self.play(FadeIn(inferred), run_time=.48)
        self.finish()


def neural_tube():
    body = plate(5.7, 3.60, -.30, -.05, STAGE)
    center = point(-.32, .14)
    wall = Arc(radius=1.32, start_angle=113 * DEGREES, angle=314 * DEGREES, arc_center=center,
               stroke_color=PURPLE, stroke_width=16)
    inner = Arc(radius=.91, start_angle=115 * DEGREES, angle=310 * DEGREES, arc_center=center,
                stroke_color=BLUE, stroke_width=6)
    pointer = Arrow(point(-.32, 2.36), point(-.32, 1.32), buff=.10, color=RED, stroke_width=5)
    return VGroup(body, wall, inner, pointer)


def bar_height(tracker, x, color):
    def shape():
        height = max(.006, 3.32 * tracker.get_value())
        return Rectangle(width=1.25, height=height, stroke_width=0, fill_color=color,
                         fill_opacity=.92).move_to(point(x, -2.12 + height / 2))
    return always_redraw(shape)


class S09UnlockedFolate(SpokenScene):
    def construct(self):
        beds = lane_beds()
        coin = gate()
        cohort = flow(lane_route, count=46, speed=.15)
        self.add(beds, cohort)
        self.at("Fair trials unlocked")
        self.play(FadeIn(coin), run_time=.51)
        self.at("A neural tube defect")
        tube = neural_tube()
        defect = label("Neural tube defect", -.25, 2.97, PURPLE, 39)
        self.play(FadeOut(coin), FadeOut(cohort), FadeIn(tube), run_time=.74)
        self.play(FadeIn(defect), run_time=.46)
        self.at("left open")
        self.play(Indicate(tube[-1], scale_factor=1.12, color=RED), run_time=1.35)
        self.at("In 1991")
        title = label("MRC Vitamin Study, 1991", -.46, 3.35, GOLD, 38)
        self.play(FadeOut(tube), FadeOut(defect), run_time=.45)
        self.play(FadeIn(title), run_time=.57)
        self.at("study randomized women")
        cohort = flow(lane_route, count=46, speed=.15)
        self.play(FadeIn(coin), FadeIn(cohort), run_time=.78)
        self.at("with a prior")
        prior = caption("Prior affected pregnancy", 32)
        self.play(FadeIn(prior), run_time=.44)
        self.at("Four milligrams of")
        dose = label("Folic acid, 4 mg/day", 2.85, 2.70, TEAL, 31)
        comparison = label("Comparison", 3.15, -2.77, GOLD, 31)
        self.play(FadeOut(prior), FadeIn(dose), run_time=.47)
        self.play(FadeIn(comparison), run_time=.47)
        self.at("started before conception")
        before = caption("Before conception", 30)
        self.play(FadeIn(before), run_time=.43)

        self.at("cut recurrence by")
        back = plate(10.51, 4.75, -.2, -.18)
        self.play(FadeOut(dose), FadeOut(comparison), FadeOut(before), FadeOut(coin), FadeOut(cohort),
                  ReplacementTransform(beds, back), run_time=.42)
        baseline = Line(point(-4.46, -2.12), point(4.07, -2.12), color=GREY, stroke_width=2)
        recurrence = label("Relative recurrence", -.30, 1.83, TEXT, 30)
        comp_lab = label("Comparison", -2.76, -2.80, GOLD, 31)
        folate_lab = label("Folic acid", .0, -2.80, TEAL, 31)
        control_value, treatment_value = ValueTracker(.001), ValueTracker(.001)
        control_bar = bar_height(control_value, -2.75, GOLD)
        treated_bar = bar_height(treatment_value, 0, TEAL)
        self.add(control_bar, treated_bar)
        self.play(Create(baseline), FadeIn(recurrence), FadeIn(comp_lab), FadeIn(folate_lab),
                  control_value.animate.set_value(1), treatment_value.animate.set_value(1), run_time=.48)
        self.at("72 percent", lead=.50)
        reduction = .72
        down = Arrow(point(1.25, 1.20), point(1.25, -2.12 + 3.32 * (1 - reduction)),
                     color=TEAL, buff=0, stroke_width=5)
        pct = label("−72%", 2.69, .05, TEAL, 50)
        self.play(treatment_value.animate(run_time=.80, rate_func=linear).set_value(1 - reduction),
                  GrowArrow(down, run_time=.80))
        self.play(FadeIn(pct), run_time=.28)
        self.at("seven of every ten")
        marks = VGroup(*[Dot(point(2.13 + (i % 5) * .51, -.81 - (i // 5) * .56),
                             radius=.194, color=TEAL if i < round(10 * reduction) else GREY)
                         for i in range(10)])
        self.play(LaggedStart(*[GrowFromCenter(m) for m in marks], lag_ratio=.13), run_time=2.13)
        self.finish()


def crossover_point(u):
    theta = TAU * u
    return point(5.18 * np.sin(theta), 1.97 * np.sin(2 * theta))


def crossover_tracks():
    return VGroup(*[
        ribbon(lambda u: crossover_point(start + .5 * u), STAGE, .42)
        for start in (0, .5)
    ], path(crossover_point, BLUE, 5))


def crossover_grid(center_x):
    return [point(center_x + (i % 7 - 3) * .30, -.45 - (i // 7) * .29)
            for i in range(21)]


class S10UnlockedDelgado(SpokenScene):
    def construct(self):
        split = lane_beds()
        tracks = crossover_tracks()
        self.add(split)
        self.at("In 1990")
        self.play(ReplacementTransform(split, tracks), run_time=1.15)
        self.at("Delgado and colleagues")
        self.play(FadeIn(label("Delgado et al., 1990", -.40, 3.14, GOLD, 40)), run_time=.48)
        self.at("21 patients")
        elapsed = ValueTracker(0)
        elapsed.add_updater(lambda t, dt: t.increment_value(dt))
        relapse = ValueTracker(0)
        beads = VGroup(*[Dot(radius=.125, color=BLUE) for _ in range(21)])

        def move(group):
            for i, bead in enumerate(group):
                # Offset the two orders by half a turn. Everyone passes through both loops.
                start = 0.0 if i < 11 else 0.5
                u = start + (i % 11) * .023 + elapsed.get_value() / 11
                bead.move_to(crossover_point(u) + UP * .11 * np.sin(i * 1.8))

        beads.add_updater(move)
        move(beads)
        self.add(elapsed)
        self.play(FadeIn(beads), run_time=.62)
        participants = caption("21 patients", size=32, color=BLUE)
        self.play(FadeIn(participants), run_time=.43)
        self.at("Each patient received")
        self.play(Indicate(tracks[-1], color=TEXT, scale_factor=1), run_time=1.0)
        self.at("both a control")
        control = label("Control", -3.35, 0, GOLD, 34)
        self.play(FadeIn(control), run_time=.43)
        self.at("challenge lowering tryptophan")
        depletion = label("Tryptophan\ndepletion", 3.45, .25, TEAL, 30)
        self.play(FadeIn(depletion), run_time=.45)
        self.at("in double blind")
        covers = VGroup(shutter(2.40, .78, -3.35, 0), shutter(2.66, 1.02, 3.45, .25))
        self.play(FadeOut(control), FadeOut(depletion), FadeOut(participants), run_time=.36)
        self.play(FadeIn(covers, shift=LEFT * .24), run_time=.49)
        blind = caption("Double-blind crossover", size=34, color=BLUE)
        self.play(FadeIn(blind), run_time=.44)
        self.at("crossover", lead=-.58)
        beads.clear_updaters()
        self.play(FadeOut(covers), FadeOut(blind),
                  *[b.animate.move_to(p) for b, p in zip(beads, crossover_grid(3.45))],
                  run_time=.60)
        self.play(FadeIn(control), FadeIn(depletion), run_time=.38)

        def show_relapses(group):
            for i, bead in enumerate(group):
                bead.set_color(ORANGE if i < round(relapse.get_value()) else BLUE)

        beads.add_updater(show_relapses)
        result = counter("{:.0f} of 21 relapsed", relapse, point(0, -3.11), size=33, color=ORANGE)
        self.at("14 of the", lead=.30)
        self.add(result)
        self.play(relapse.animate.set_value(14), run_time=.60)
        result.clear_updaters()
        self.at("while the control", lead=-.10)
        beads.clear_updaters()
        self.play(FadeOut(result),
                  *[b.animate.set_color(BLUE).move_to(p) for b, p in zip(beads, crossover_grid(-3.35))],
                  run_time=.76)
        self.play(FadeIn(label("No significant effect", -3.36, -2.62, GOLD, 29)), run_time=.59)
        self.finish()


def outbreak_plot():
    chart = Plot(box=(-5.8, 5.62, -2.35, 2.02), xr=(0, 1), yr=(0, 1), stroke=2)
    base = plate(11.78, 4.62, -.08, -.15)
    return chart, base


def outbreak(u, lag=0):
    return .79 * (np.exp(-((u - .23 - lag) / .105)**2)
                  + np.exp(-((u - .69 - lag) / .137)**2))


def epidemic_wave(chart, lag, color, opacity):
    fn = lambda u: outbreak(u, lag)
    trace = chart.curve(fn, color=color, width=6)
    xs = np.linspace(0, 1, 65)
    area = Polygon(*[chart.pt(x, fn(x)) for x in xs], chart.pt(1, 0), chart.pt(0, 0),
                   fill_color=color, fill_opacity=opacity, stroke_width=0)
    return area, trace


def pathology_lens():
    outline = Circle(radius=1.95, color=BLUE, fill_color=STAGE, fill_opacity=1, stroke_width=4).move_to(point(-1.95, -.1))
    handle = Line(point(-.62, -1.52), point(.08, -2.29), color=BLUE, stroke_width=11)
    lobes = VGroup(*[
        Ellipse(width=1.42, height=1.90, color=PURPLE, fill_color=PURPLE, fill_opacity=.16,
                stroke_width=3).rotate(sign * .30).move_to(point(-1.95 + sign * .47, .02))
        for sign in (-1, 1)
    ])
    particles = VGroup(*[
        Dot(point(-1.95 + dx, .02 + dy), radius=.125, color=ORANGE)
        for dx, dy in ((-.65, .34), (-.31, -.38), (-.27, .45), (.17, .30), (.56, .42), (.48, -.24), (.32, -.59))
    ])
    for i, d in enumerate(particles):
        bob(d, amp=.08, seed=i)
    scan = plate(.58, 2.18, -1.95, -.08, BLUE, fill=.32)
    elapsed = 0.0

    def sweep(mob, dt):
        nonlocal elapsed
        elapsed += dt
        mob.move_to(point(-1.95 + .99 * np.sin(elapsed * 1.9), -.08))

    scan.add_updater(sweep)
    return VGroup(handle, outline, lobes, scan, particles)


def culture_dish():
    rim = Ellipse(width=7.54, height=4.35, color=BLUE, fill_color=STAGE, fill_opacity=1,
                  stroke_width=4).move_to(point(-.40, -.15))
    cells, buds = VGroup(), VGroup()
    for i, (x, y) in enumerate(((-2.89,.08), (-2.32,.79), (-1.72,-.96), (-.85,.53),
                                (-.24,-.84), (.45,.85), (1.02,-.08), (1.97,-.71), (2.23,.67))):
        cell = Circle(radius=.27, color=PURPLE, fill_color=PURPLE, fill_opacity=.31, stroke_width=3)
        cell.move_to(point(x, y))
        bud = Circle(radius=.17, color=PURPLE, fill_color=PURPLE, fill_opacity=.31, stroke_width=3)
        bud.move_to(point(x+.36, y+.15))
        bob(cell, amp=.11, speed=2.9, seed=i)
        bob(bud, amp=.16, speed=2.9, seed=i)
        cells.add(cell)
        buds.add(bud)
    return rim, cells, buds


class S11UnlockedZika(SpokenScene):
    def construct(self):
        beds, traces, people = map_parts()
        schematic = scope_tag(size=28)
        self.add(beds, traces, people, schematic)
        self.at("Epidemiology then pairs")
        chart, base = outbreak_plot()
        for trace in traces:
            pulse(trace, base=2.8, amp=1.5, speed=2.0)
        z_area, z_line = epidemic_wave(chart, 0, ORANGE, .31)
        m_area, m_line = epidemic_wave(chart, .078, PURPLE, .25)
        self.at("In 2015 and")
        self.play(ReplacementTransform(beds, base), FadeOut(traces), FadeOut(people),
                  FadeIn(chart.axes), run_time=.72)
        right = label("2015–2016", 2.81, -2.77, GOLD, 30)
        self.play(FadeIn(right), FadeIn(z_area), Create(z_line), run_time=1.35)
        self.at("microcephaly tracked zika")
        self.play(FadeIn(m_area), Create(m_line), run_time=1.08)
        legend = VGroup(label("Zika", -2.82, 2.79, ORANGE, 34),
                        label("Microcephaly", 1.33, 2.79, PURPLE, 34))
        self.play(FadeIn(legend), run_time=.46)
        traveling = flow(lambda i, u: chart.pt(.035 + .93 * u, outbreak(.035 + .93 * u, .078 if i % 2 else 0)),
                         count=31, speed=.20, colors=(ORANGE, PURPLE), spread=.16, radius=.124)
        self.add(traveling)
        self.at("matching a 2013")
        left = label("2013–2014 French Polynesia", -3.25, -2.77, GOLD, 29)
        self.play(FadeIn(left), run_time=.52)
        self.at("In 2016")
        lens = pathology_lens()
        self.play(FadeOut(VGroup(chart.axes, z_area, z_line, m_area, m_line, legend, left, right, traveling)),
                  FadeIn(lens, shift=RIGHT * .14), run_time=.96)
        self.at("and colleagues found")
        author = label("Mlakar et al., 2016", -1.32, 3.04, GOLD, 36)
        self.play(FadeIn(author), run_time=.50)
        self.at("in a fetal brain")
        brain = label("Fetal brain", 2.50, .06, PURPLE, 34)
        self.play(FadeIn(brain), run_time=.45)

        self.at("Ming Song and")
        rim, cells, buds = culture_dish()
        self.play(FadeOut(lens), FadeOut(author), FadeOut(brain), run_time=.42)
        self.play(FadeIn(rim), run_time=.42)
        research = label("Ming, Song & Tang, 2016", -.45, 3.06, GOLD, 35)
        self.play(FadeIn(cells), FadeIn(buds), FadeIn(research), run_time=.54)
        self.at("kills some cultured")
        self.play(LaggedStart(*[FadeOut(VGroup(cells[i], buds[i]), scale=.35)
                                for i in (1, 3, 5, 8)], lag_ratio=.33), run_time=1.54)
        self.at("and slows the rest")
        surviving = (0, 2, 4, 6, 7)
        for i in surviving:
            for cell in (cells[i], buds[i]):
                cell.clear_updaters()
                bob(cell, amp=.08, speed=.48, seed=i)
        progenitor = label("Cortical progenitors", -.35, -2.79, PURPLE, 33)
        self.play(FadeIn(progenitor), run_time=.48)

        self.at("Fair trials test")
        trial_icon = lane_beds().scale(.41).move_to(point(-3.19, .14))
        shuffle = gate(-3.68, .14, .27)
        survivors = VGroup(*[m for i in surviving for m in (cells[i], buds[i])])
        self.play(FadeOut(rim), FadeOut(survivors), FadeOut(research), FadeOut(progenitor),
                  FadeIn(trial_icon), FadeIn(shuffle), run_time=.69)
        self.play(FadeIn(label("Fair trials", -3.24, 1.66, BLUE, 34)), run_time=.43)
        self.at("Cohorts and biology")
        cohort_icon = VGroup(*map_parts()[:2]).scale(.43).move_to(point(2.90, .08))
        biology = Circle(radius=.53, color=PURPLE, stroke_width=4, fill_color=BG, fill_opacity=1).move_to(point(2.89, .31))
        evidence = VGroup(biology, plaque(2.89, .31, .56))
        self.play(FadeIn(cohort_icon), FadeIn(evidence), run_time=.68)
        self.play(FadeIn(label("Cohorts + biology", 2.80, 1.66, PURPLE, 34)), run_time=.47)
        self.finish()


class S12End(EndCard):
    LINE = "Randomize and blind to test treatments; track cohorts to trace causes."
