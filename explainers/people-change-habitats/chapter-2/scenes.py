"""Reading the River's Record — chapter 2 of People change habitats.

COLOR MAP (shared with chapter 1's current script)
  BLUE  = blue catfish
  GOLD  = white catfish
  TEAL  = prey and river water
  GREEN = shoreline habitat
  RED   = human pressures / possible harm
  TEXT  = labels and evidence
"""
import numpy as np
from bp_parts import *  # noqa: F401,F403


YEARS = np.array([1988, 1990, 1995, 2000, 2005, 2010, 2015, 2019, 2020, 2022], dtype=float)
BLUE_DATA = np.array([0.00, 0.00, 8.97, 17.44, 47.07, 16.45, 58.84, 317.77, 47.74, 54.42])
GOLD_DATA = np.array([0.20, 1.83, 1.31, 0.05, 0.15, 0.41, 0.20, 0.23, 0.32, 0.16])


def fish(color, scale=1.0, flip=False):
    """The carried catfish cartoon, matching chapter 1's simple filled-outline style."""
    body = Ellipse(width=1.55, height=0.72, color=color, stroke_width=3,
                   fill_color=color, fill_opacity=0.35)
    tail = Polygon([-0.65, 0, 0], [-1.16, 0.38, 0], [-1.16, -0.38, 0],
                   color=color, stroke_width=3, fill_color=color, fill_opacity=0.35)
    eye = Dot([0.43, 0.10, 0], radius=0.045, color=TEXT)
    whiskers = VGroup(Line([0.65, 0.0, 0], [1.02, 0.20, 0], color=color, stroke_width=2),
                      Line([0.65, -0.04, 0], [1.02, -0.23, 0], color=color, stroke_width=2))
    mob = VGroup(tail, body, eye, whiskers).scale(scale)
    if flip:
        mob.flip(UP)
    return mob


def river_world(boat=False, murky=False, labels=False):
    """Build the same full-height river cross-section for every carried river scene."""
    water = RoundedRectangle(corner_radius=0.18, width=12.5, height=4.55, color=TEAL,
                             stroke_width=3, fill_color=TEAL, fill_opacity=0.20).move_to([0, -0.35, 0])
    surface = Line([-6.2, 1.82, 0], [6.2, 1.82, 0], color=TEAL, stroke_width=5)
    bottom = VMobject(color=GOLD, stroke_width=6).set_points_smoothly([
        [-6.2, -2.35, 0], [-3.6, -2.15, 0], [-1.0, -2.42, 0], [1.9, -2.18, 0], [6.2, -2.35, 0]
    ])
    plants = VGroup()
    for x in [-5.65, -5.25, -4.82, -4.36]:
        stem = VMobject(color=GREEN, stroke_width=6).set_points_smoothly([
            [x, -2.18, 0], [x - 0.10, -1.15, 0], [x + 0.12, 0.10, 0], [x - 0.04, 1.45, 0]
        ])
        plants.add(stem)
    blue = fish(BLUE, 0.88).move_to([2.8, -0.05, 0])
    gold = fish(GOLD, 0.76).move_to([-1.7, -0.85, 0])
    prey = VGroup(*[fish(TEAL, 0.25).move_to(p) for p in
                    [(-0.2, 0.5, 0), (0.7, -0.9, 0), (-3.4, 0.1, 0)]])
    currents = VGroup(*[Line([x, y, 0], [x + 0.34, y, 0], color=TEAL, stroke_width=3).set_opacity(0.42)
                        for y in [1.2, 0.55, -0.1, -0.75, -1.4]
                        for x in [-5.5, -2.6, 0.3, 3.2]])

    def flow(mob, dt):
        mob.shift(RIGHT * 1.8 * dt)
        for mark in mob:
            if mark.get_left()[0] > 6.1:
                mark.shift(LEFT * 11.8)
    currents.add_updater(flow)
    g = VGroup(water, surface, bottom, plants, currents, prey, blue, gold)
    g.water, g.surface, g.bottom, g.plants = water, surface, bottom, plants
    g.blue, g.gold, g.prey, g.currents = blue, gold, prey, currents
    if boat:
        hull = Polygon([-0.85, 0.0, 0], [0.85, 0.0, 0], [0.55, -0.34, 0], [-0.55, -0.34, 0],
                       color=TEXT, fill_color=TEXT, fill_opacity=0.18, stroke_width=3)
        cabin = Rectangle(width=0.65, height=0.38, color=TEXT, fill_color=TEXT, fill_opacity=0.12).move_to([0.15, 0.2, 0])
        vessel = VGroup(hull, cabin).move_to([-3.7, 2.02, 0])
        g.add(vessel)
        g.boat = vessel
    if murky:
        band = Rectangle(width=7.2, height=3.85, color="#8B6A45", stroke_width=0,
                         fill_color="#8B6A45", fill_opacity=0.50).move_to([1.9, -0.25, 0])
        g.add(band)
        g.murky = band
    if labels:
        labs = VGroup(chip("blue catfish", BLUE, 28).move_to([3.95, 0.75, 0]),
                      chip("white catfish", GOLD, 28).move_to([-2.65, -1.6, 0]),
                      chip("habitat", GREEN, 28).move_to([-5.05, 2.65, 0]))
        g.add(labs)
        g.labels = labs
    return g


def survey_panels(full=True, dim=False):
    """Two fixed-scale panels computed directly from the lesson table."""
    blue_p = Plot(box=(-5.55, 5.65, 0.45, 2.55), xr=(1988, 2022), yr=(0, 340),
                  xticks=[], yticks=[(0, "0"), (320, "320")], ylabel="blue survey index", color=BLUE, size=22)
    gold_p = Plot(box=(-5.55, 5.65, -2.45, -0.35), xr=(1988, 2022), yr=(0, 2.0),
                  xticks=[(1988, "1988"), (2005, "2005"), (2022, "2022")],
                  yticks=[(0, "0"), (1.8, "1.8")], xlabel="", ylabel="white survey index", color=GOLD, size=22)
    gold_p.ylabel.shift(DOWN * 0.27)

    def series(plot, vals, color):
        pts = [plot.pt(x, y) for x, y in zip(YEARS, vals)]
        line = VMobject(color=color, stroke_width=5).set_points_as_corners(pts)
        dots = VGroup(*[Dot(p, radius=0.075, color=color) for p in pts])
        return VGroup(line, dots)

    bs, gs = series(blue_p, BLUE_DATA, BLUE), series(gold_p, GOLD_DATA, GOLD)
    if dim:
        bs.set_opacity(0.30), gs.set_opacity(0.30)
    blue_bg = Rectangle(width=11.2, height=2.1, stroke_width=0, fill_color=BLUE, fill_opacity=0.18).move_to([0.05, 1.5, 0])
    gold_bg = Rectangle(width=11.2, height=2.1, stroke_width=0, fill_color=GOLD, fill_opacity=0.14).move_to([0.05, -1.4, 0])
    blue_bg.layout_ok = gold_bg.layout_ok = True  # deliberate panel fields behind their labels
    g = VGroup(blue_bg, gold_bg, blue_p, gold_p)
    if full:
        g.add(bs, gs)
    g.blue_plot, g.gold_plot, g.blue_series, g.gold_series = blue_p, gold_p, bs, gs
    g.high = bs[1][7]
    g.zeros = VGroup(bs[1][0], bs[1][1])
    g.divider = DashedLine([-6.05, -0.02, 0], [6.05, -0.02, 0], color=GREY, stroke_width=3)
    g.divider.layout_ok = True  # deliberate divider through the fixed panel-title band
    sweep = Line([-5.5, -2.42, 0], [-5.5, 2.52, 0], color=TEXT, stroke_width=3).set_opacity(0.24)
    sweep.layout_ok = True  # moving year-sampling cursor, allowed to cross panel marks

    def scan(mob, dt):
        mob.shift(RIGHT * 0.75 * dt)
        if mob.get_x() > 5.55:
            mob.shift(LEFT * 11.0)
    sweep.add_updater(scan)
    sample_marks = VGroup(*[
        Line([x, y, 0], [x + 0.18, y, 0], color=TEXT, stroke_width=3).set_opacity(0.32)
        for y in [2.15, 1.72, 1.27, 0.83, -0.78, -1.22, -1.66, -2.10]
        for x in [-5.1, -3.2, -1.3, 0.6, 2.5, 4.4]
    ])
    sample_marks.set_z_index(-0.5)
    sample_marks.layout_ok = True

    def drift(mob, dt):
        mob.shift(RIGHT * 1.9 * dt)
        for mark in mob:
            if mark.get_left()[0] > 5.5:
                mark.shift(LEFT * 10.8)
    sample_marks.add_updater(drift)
    g.add(g.divider, sample_marks, sweep)
    g.sweep = sweep
    return g


def compact_evidence_panels(boxes=((-6.0, 0.3, 0.45, 2.55), (-6.0, 0.3, -2.45, -0.35))):
    """Exact lesson traces without tiny ticks, for scenes where the cause/pattern contrast shares space."""
    out = VGroup()
    for (x0, x1, y0, y1), vals, ymax, color, label in [
        (boxes[0], BLUE_DATA, 340.0, BLUE, "blue survey index"),
        (boxes[1], GOLD_DATA, 2.0, GOLD, "white survey index"),
    ]:
        frame = RoundedRectangle(corner_radius=0.12, width=x1 - x0, height=y1 - y0,
                                 color=color, stroke_width=2, fill_color=color, fill_opacity=0.16).move_to([(x0 + x1) / 2, (y0 + y1) / 2, 0])
        frame.layout_ok = True  # deliberate filled data panel behind its label
        pts = [np.array([x0 + (yr - 1988) / 34 * (x1 - x0), y0 + val / ymax * (y1 - y0), 0])
               for yr, val in zip(YEARS, vals)]
        trace = VMobject(color=color, stroke_width=5).set_points_as_corners(pts)
        dots = VGroup(*[Dot(p, radius=0.055, color=color) for p in pts])
        lab = T(label, 28, color).move_to([x0 + 1.55, y1 + 0.22, 0])
        out.add(frame, trace, dots, lab)
    x0, x1 = boxes[0][0], boxes[0][1]
    sweep = Line([x0, boxes[1][2], 0], [x0, boxes[0][3], 0], color=TEXT, stroke_width=3).set_opacity(0.24)
    sweep.layout_ok = True

    def scan(mob, dt):
        mob.shift(RIGHT * 0.68 * dt)
        if mob.get_x() > x1:
            mob.shift(LEFT * (x1 - x0))
    sweep.add_updater(scan)
    marks = VGroup(*[
        Line([x, y, 0], [x + 0.16, y, 0], color=TEXT, stroke_width=3).set_opacity(0.34)
        for y in np.linspace(boxes[1][2] + 0.25, boxes[0][3] - 0.25, 7)
        for x in np.linspace(x0 + 0.25, x1 - 0.45, 6)
    ])
    marks.set_z_index(-0.5)
    marks.layout_ok = True

    def drift(mob, dt):
        mob.shift(RIGHT * 1.8 * dt)
        for mark in mob:
            if mark.get_left()[0] > x1:
                mark.shift(LEFT * (x1 - x0 - 0.2))
    marks.add_updater(drift)
    out.add(marks, sweep)
    return out


def roamer(scene, path, color):
    """A bright dot that keeps travelling along a trace, so a long held sentence stays alive."""
    pts = path.get_points()[::3]
    dot = Dot(pts[0], radius=0.17, color=color)
    dot.layout_ok = True
    dot._t = 0.0

    def go(m, dt):
        m._t += dt * 0.3
        f = (m._t % 1.0) * (len(pts) - 1)
        i = int(f)
        m.move_to(pts[i] * (1 - (f - i)) + pts[min(i + 1, len(pts) - 1)] * (f - i))
    dot.add_updater(go)
    scene.add(dot)
    return dot


def plot_question_backdrop():
    panels = survey_panels(full=True, dim=True)
    panels.high.set_opacity(1)
    ring = Circle(radius=0.34, color=GOLD, stroke_width=6).move_to(panels.high)
    q = question_card("One point, or the full series?", y=-3.25, size=32)
    return VGroup(panels, ring, q)


class S00Hook(SpokenScene, TitleCard):
    LESSON = "People change habitats"
    TITLE = "Reading the River's Record"

    def construct(self):
        world = river_world(murky=False)
        self.play(FadeIn(world), run_time=0.8)
        self.at("How can scientists tell")
        glass = VGroup(Circle(radius=0.68, color=TEXT, stroke_width=5),
                       Line([0.48, -0.48, 0], [1.05, -1.05, 0], color=TEXT, stroke_width=7)).move_to([-2.8, 0.25, 0])
        question = fit_text("How can scientists tell whether populations changed?", max_w=10.8, size=36, color=TEXT).to_edge(UP, buff=0.25)
        self.play(FadeIn(question), FadeIn(glass), run_time=0.7)
        self.play(glass.animate.shift(RIGHT * 5.0), run_time=2.0, rate_func=linear)
        self.at("They need the river's record")
        record = chip("the river's record", TEAL, 34).move_to([0, 2.65, 0])
        self.play(swap(question, record), run_time=0.7)
        self.at("Murky water")
        murk = Rectangle(width=7.2, height=3.85, stroke_width=0, fill_color="#8B6A45",
                         fill_opacity=0.62).move_to([1.9, -0.25, 0])
        self.play(FadeIn(murk), world.blue.animate.set_opacity(0.12), world.gold.animate.set_opacity(0.12), run_time=1.0)
        self.play(glass.animate.shift(LEFT * 2.0), run_time=0.8)
        self.finish()


class S01Title(NarratedScene):
    def construct(self):
        world = river_world(boat=True)
        title = T("Reading the River's Record", 50, TEXT, font=TITLE_FONT).move_to([0, 2.75, 0])
        self.add(world)
        self.play(world.boat.animate.shift(RIGHT * 3.0), FadeIn(title), run_time=1.0, rate_func=linear)
        self.play(world.boat.animate.shift(RIGHT * 2.0), FadeOut(title), run_time=0.8, rate_func=linear)
        self.finish()


class S02Tow(SpokenScene):
    def construct(self):
        world = river_world(boat=True)
        world.boat.move_to([-4.4, 2.02, 0])
        net = Polygon([-3.8, 1.55, 0], [-2.1, -1.75, 0], [-0.5, -1.55, 0],
                      color=TEXT, fill_color=TEXT, fill_opacity=0.06, stroke_width=3)
        self.play(FadeIn(world), FadeIn(net), run_time=0.7)
        self.at("repeat bottom")
        stations = VGroup(*[Dot([3.8 + 0.75 * (i % 3), 1.0 - 0.75 * (i // 3), 0], radius=0.13, color=TEAL)
                           for i in range(6)])
        map_box = RoundedRectangle(corner_radius=0.18, width=3.0, height=2.7, color=TEAL, fill_color=BG, fill_opacity=0.85).move_to([4.65, 0.2, 0])
        self.play(world.boat.animate.shift(RIGHT * 2.0), net.animate.shift(RIGHT * 2.0), FadeIn(map_box), run_time=1.2)
        self.play(LaggedStart(*[GrowFromCenter(d) for d in stations], lag_ratio=0.15), run_time=1.0)
        self.at("same kind of net")
        clock = Circle(radius=0.5, color=TEXT).move_to([-4.7, 2.75, 0])
        hands = VGroup(Line(clock.get_center(), clock.get_center() + UP * 0.32, color=TEXT),
                       Line(clock.get_center(), clock.get_center() + RIGHT * 0.26, color=TEXT))
        self.play(FadeIn(clock), Create(hands), run_time=0.6)
        self.at("catch is sorted")
        tubs = VGroup(chip("blue catch", BLUE, 30), chip("white catch", GOLD, 30)).arrange(RIGHT, buff=0.8).move_to([0, -3.0, 0])
        self.play(FadeOut(net), FadeIn(tubs, shift=UP * 0.2), run_time=0.8)
        self.at("Repeating the method")
        repeat = CurvedArrow([-1.6, 2.65, 0], [1.6, 2.65, 0], angle=-TAU / 4, color=TEAL, stroke_width=5)
        self.play(Create(repeat), Indicate(stations, color=TEAL), run_time=1.0)
        self.finish()


class S03Index(SpokenScene):
    def construct(self):
        stations = VGroup(*[VGroup(Dot(radius=0.13, color=TEAL), M(str(n), 26, TEXT)).arrange(RIGHT, buff=0.12)
                           for n in [4, 7, 3, 9, 5, 6]]).arrange(DOWN, buff=0.24).move_to([-4.5, 0.1, 0])
        calc = chip("survey calculation", TEXT, 34).move_to([0, 0.1, 0])
        outline = RoundedRectangle(corner_radius=1.0, width=12.2, height=5.0, color=TEAL, stroke_width=3).set_stroke(opacity=0.45)
        self.play(Create(outline), FadeIn(stations), run_time=0.8)
        self.at("counts become")
        self.play(ReplacementTransform(stations.copy(), calc), run_time=1.0)
        blue_point = Dot([4.3, 0.75, 0], radius=0.18, color=BLUE)
        gold_point = Dot([4.3, -0.55, 0], radius=0.18, color=GOLD)
        labels = VGroup(T("one year", 28, TEXT).next_to(blue_point, LEFT, buff=0.3),
                        T("one year", 28, TEXT).next_to(gold_point, LEFT, buff=0.3))
        self.play(FadeIn(blue_point), FadeIn(gold_point), FadeIn(labels), run_time=0.7)
        self.at("tracks how common")
        signal = T("consistent signal from samples", 32, TEAL).move_to([0, -3.0, 0])
        pulse(outline)
        self.play(FadeIn(signal), run_time=0.7)
        self.at("not a count")
        whole = chip("every fish in the river", RED, 30).move_to([0, 3.05, 0])
        whole.layout_ok = True  # label is intentionally inside its chip
        strike = Cross(whole, stroke_color=RED, stroke_width=6)
        strike.layout_ok = True  # deliberate crossed-out whole-river counter
        self.play(FadeIn(whole), Create(strike), run_time=0.8)
        self.at("consistent signal")
        self.play(Indicate(signal, color=TEAL), run_time=0.8)
        self.finish()


class S04Separate(SpokenScene):
    def construct(self):
        world = river_world(labels=True)
        self.play(FadeIn(world), run_time=0.7)
        self.at("Build a separate trace")
        panels = survey_panels(full=False)
        self.play(FadeOut(world), FadeIn(panels), run_time=1.0)
        sep = chip("separate scales", TEXT, 32).move_to([0, 3.35, 0])
        sep.layout_ok = True  # label belongs inside its chip
        self.play(FadeIn(sep), run_time=0.5)
        self.at("different math")
        rulers = VGroup(M("blue 0 — 320", 28, BLUE), M("white 0 — 1.8", 28, GOLD)).arrange(RIGHT, buff=1.0).move_to([0, 3.35, 0])
        self.play(FadeOut(sep), FadeIn(rulers), run_time=0.8)
        self.at("cannot be compared")
        arrow = DoubleArrow([3.3, 1.5, 0], [3.3, -1.5, 0], color=RED, stroke_width=5)
        self.play(FadeIn(arrow), Create(Cross(arrow, stroke_color=RED, stroke_width=6)), run_time=0.8)
        pulse(arrow, base=5, amp=2.5, speed=3)
        roamer(self, panels.blue_series[0], BLUE)
        roamer(self, panels.gold_series[0], GOLD)
        self.finish()


class S05Series(SpokenScene):
    def construct(self):
        panels = survey_panels(full=False)
        self.add(panels)
        self.at("full traces grow")
        self.play(Create(panels.blue_series[0]), LaggedStart(*[GrowFromCenter(d) for d in panels.blue_series[1]], lag_ratio=0.08), run_time=2.4)
        self.at("blue index rises")
        self.play(Indicate(panels.blue_series, color=BLUE), run_time=0.8)
        self.at("white index")
        self.play(Create(panels.gold_series[0]), LaggedStart(*[GrowFromCenter(d) for d in panels.gold_series[1]], lag_ratio=0.08), run_time=2.2)
        self.at("Each dot")
        tag = scope_tag("computed from lesson table")
        one = Circle(radius=0.18, color=TEXT, stroke_width=4).move_to(panels.gold_series[1][2])
        self.play(FadeIn(tag), Create(one), run_time=0.7)
        self.finish()


class S06Predict(SpokenScene):
    def construct(self):
        panels = survey_panels(full=True, dim=True)
        panels.high.set_opacity(1)
        self.add(panels)
        self.at("One blue point")
        ring = Circle(radius=0.34, color=GOLD, stroke_width=6).move_to(panels.high)
        year = M("2019", 30, BLUE).next_to(ring, RIGHT, buff=0.15)
        self.play(Create(ring), FadeIn(year), run_time=0.8)
        self.at("Should that single point")
        q = question_card("One point, or the full series?", y=-3.25, size=32)
        self.play(FadeIn(q), ring.animate.scale(1.18), run_time=0.8)
        self.at("Make your prediction")
        self.play(Indicate(q, color=GOLD), run_time=0.7)
        self.finish()


class S07Pause(PredictPause):
    QUESTION = "One point, or the full series?"
    SECONDS = 4.5
    CARD = {"y": -3.25, "size": 32}
    RING_AT = (6.2, -3.3, 0)

    def backdrop(self):
        panels = survey_panels(full=True, dim=True)
        panels.high.set_opacity(1)
        ring = pulse(Circle(radius=0.34, color=GOLD, stroke_width=6).move_to(panels.high), base=6, amp=1, speed=2)
        return VGroup(panels, ring)


class S08Reveal(SpokenScene):
    def construct(self):
        panels = survey_panels(full=True)
        self.add(panels)
        self.at("Use the full series")
        bracket = Brace(Line(panels.gold_plot.pt(1988, 0), panels.gold_plot.pt(2022, 0)), DOWN, color=TEXT, buff=0.42)
        rule = T("use the full series", 28, TEXT).next_to(bracket, DOWN, buff=0.05)
        roamer(self, panels.blue_series[0], BLUE)
        roamer(self, panels.gold_series[0], GOLD)
        pulse(bracket, base=4, amp=2.5, speed=3)
        self.play(GrowFromCenter(bracket), FadeIn(rule), run_time=0.8)
        self.at("One year can")
        self.play(Indicate(panels.high, color=GOLD), Indicate(panels.blue_series[1][8], color=BLUE), run_time=0.9)
        self.at("A zero also means")
        empty = VGroup(Arc(radius=0.35, start_angle=PI, angle=PI, color=TEXT),
                       Line([-0.35, 0, 0], [0.35, 0, 0], color=TEXT)).move_to([-1.7, 2.1, 0])
        lab = T("none caught in this survey", 28, BLUE).next_to(empty, RIGHT, buff=0.2)
        self.play(Indicate(panels.zeros, color=BLUE), FadeIn(empty), FadeIn(lab), run_time=0.9)
        self.at("not that none lived")
        faint = VGroup(*[fish(BLUE, 0.25).set_opacity(0.28).move_to([3.7 + i * 0.65, 2.1, 0]) for i in range(3)])
        self.play(FadeIn(faint), run_time=0.7)
        self.at("other years")
        self.play(Indicate(panels.blue_series[1], color=BLUE), run_time=0.9)
        self.finish()


class S09Compare(SpokenScene):
    def construct(self):
        panels = survey_panels(full=True)
        self.add(panels)
        self.at("Compare each fish")
        blue_b = DoubleArrow(panels.blue_plot.pt(1995, 285), panels.blue_plot.pt(2022, 285), color=BLUE, stroke_width=4)
        blue_l = T("higher later", 30, BLUE).next_to(blue_b, DOWN, buff=0.1)
        self.play(GrowArrow(blue_b), FadeIn(blue_l), run_time=0.8)
        self.at("white index stayed")
        gold_b = DoubleArrow(panels.gold_plot.pt(1995, 1.65), panels.gold_plot.pt(2022, 1.65), color=GOLD, stroke_width=4)
        gold_l = T("below early highs", 30, GOLD).next_to(gold_b, DOWN, buff=0.1)
        self.play(GrowArrow(gold_b), FadeIn(gold_l), run_time=0.8)
        self.at("opposite pattern")
        community = chip("community pattern changed", TEAL, 34).move_to([0, 3.28, 0])
        community.layout_ok = True  # label belongs inside its chip
        self.play(FadeOut(blue_l), FadeOut(gold_l), FadeIn(community), run_time=0.9)
        self.at("does not count")
        counter_box = chip("whole-river count", RED, 30).move_to([0, -3.2, 0])
        counter_box.layout_ok = True
        strike = Cross(counter_box, stroke_color=RED, stroke_width=6)
        strike.layout_ok = True
        self.play(FadeOut(community), FadeIn(counter_box), Create(strike), run_time=0.8)
        self.finish()


class S10Cause(SpokenScene):
    def construct(self):
        panels = compact_evidence_panels()
        boundary = DashedLine([1.0, -2.65, 0], [1.0, 2.75, 0], color=TEXT, stroke_width=4)
        boundary_label = T("pattern ≠ cause", 34, TEXT).move_to([3.8, 2.85, 0])
        self.play(FadeIn(panels), Create(boundary), FadeIn(boundary_label), run_time=0.8)
        self.at("Shared prey")
        paths = VGroup(chip("shared prey ?", TEAL, 30), chip("runoff ?", RED, 30), chip("habitat loss ?", GREEN, 30))
        paths.arrange(DOWN, buff=0.45).move_to([4.0, 0.25, 0])
        self.play(FadeIn(paths[0], shift=LEFT * 0.2), run_time=0.7)
        self.at("Pollution")
        self.play(FadeIn(paths[1], shift=LEFT * 0.2), run_time=0.6)
        self.at("habitat loss")
        self.play(FadeIn(paths[2], shift=LEFT * 0.2), run_time=0.6)
        self.at("graph alone")
        self.play(Indicate(boundary_label, color=GOLD), LaggedStart(*[Indicate(p, color=TEXT) for p in paths], lag_ratio=0.2), run_time=1.0)
        self.finish()


class S11Claim(SpokenScene):
    def construct(self):
        panels = TwoPanel("CLAIM: pattern", "EVIDENCE: same years", colors=(TEAL, BLUE), top=3.0, bottom=-0.2)
        reasoning_frame = RoundedRectangle(corner_radius=0.18, width=12.8, height=2.0, color=GOLD, stroke_width=3).move_to([0, -2.05, 0])
        panels.left_frame.set_fill(TEAL, opacity=0.16)
        panels.right_frame.set_fill(BLUE, opacity=0.16)
        reasoning_frame.set_fill(GOLD, opacity=0.14)
        panels.left_frame.layout_ok = panels.right_frame.layout_ok = reasoning_frame.layout_ok = True
        reasoning_head = T("REASONING: may link", 32, GOLD).move_to([0, -1.45, 0])
        sweep = Line([-6.0, -2.85, 0], [-6.0, 2.75, 0], color=TEXT, stroke_width=3).set_opacity(0.22)
        sweep.layout_ok = True

        def scan(mob, dt):
            mob.shift(RIGHT * 0.72 * dt)
            if mob.get_x() > 6.0:
                mob.shift(LEFT * 12.0)
        sweep.add_updater(scan)
        tokens = VGroup(*[
            Line([x, y, 0], [x + 0.18, y, 0], color=TEXT, stroke_width=3).set_opacity(0.34)
            for y in [2.35, 1.65, 0.85, 0.15, -1.85, -2.5]
            for x in [-5.7, -3.8, -1.9, 0.0, 1.9, 3.8, 5.5]
        ])
        tokens.set_z_index(-0.5)
        tokens.layout_ok = True

        def drift(mob, dt):
            mob.shift(RIGHT * 1.9 * dt)
            for mark in mob:
                if mark.get_left()[0] > 6.0:
                    mark.shift(LEFT * 11.7)
        tokens.add_updater(drift)
        self.add(tokens, sweep)
        self.play(FadeIn(panels.left_frame), FadeIn(panels.left_head), run_time=0.6)
        self.at("three parts")
        self.play(FadeIn(panels.right_frame), FadeIn(panels.right_head), FadeIn(reasoning_frame), FadeIn(reasoning_head), run_time=0.8)
        self.at("State the pattern")
        claim = fit_text("blue higher; white below early highs", max_w=5.4, size=30, color=TEAL).move_to(panels.area("left")[0])
        self.play(FadeIn(claim), run_time=0.6)
        self.at("values from the same years")
        values = VGroup(M("1995:  8.97  |  1.31", 27, TEXT), M("2022: 54.42  |  0.16", 27, TEXT)).arrange(DOWN, buff=0.3).move_to(panels.area("right")[0])
        self.play(FadeIn(values), run_time=0.7)
        self.at("possible link")
        reason = T("shared prey may link the changes", 30, TEXT).move_to([0, -2.35, 0])
        self.play(FadeIn(reason), run_time=0.6)
        self.at("Keep May")
        may = T("may", 56, GOLD, weight=BOLD).move_to(reason.get_center())
        self.play(FadeOut(reason), GrowFromCenter(may), run_time=0.7)
        self.at("small word")
        may_target = T("may", 30, GOLD, weight=BOLD).move_to([-2.3, -2.35, 0])
        honest = T("keeps the evidence honest", 30, TEXT).move_to([1.0, -2.35, 0])
        self.play(Transform(may, may_target), FadeIn(honest), run_time=0.8)
        self.finish()


class S12Rule(SpokenScene):
    def construct(self):
        world = river_world(labels=False).scale(0.58).move_to([0.7, -1.85, 0])
        panels = compact_evidence_panels(boxes=((-5.4, 5.5, 2.05, 3.05), (-5.4, 5.5, 0.35, 1.35)))
        self.play(FadeIn(world), FadeIn(panels), run_time=0.9)
        self.at("When people change")
        rule = fit_text("When people change an ecosystem, populations may rise or fall.", max_w=11.5, size=32, color=TEXT).move_to([0, -3.45, 0])
        self.play(FadeIn(rule), world.blue.animate.shift(UP * 0.12), world.gold.animate.shift(DOWN * 0.12), run_time=0.8)
        self.at("Evidence shows")
        observed_l = chip("observed pattern", TEXT, 26).move_to([-4.3, -0.3, 0])
        observed_l.layout_ok = True
        self.play(FadeIn(observed_l), run_time=0.7)
        self.at("Further tests")
        causes = VGroup(chip("prey ?", TEAL, 26), chip("runoff ?", RED, 26), chip("habitat ?", GREEN, 26)).arrange(RIGHT, buff=0.3).move_to([1.7, -0.3, 0])
        causes.layout_ok = True  # labels are intentionally carried on opaque path chips
        arrows = VGroup(*[DashedLine(c.get_bottom(), c.get_bottom() + DOWN * 0.7, color=c.get_color(), stroke_width=3) for c in causes])
        self.play(FadeIn(causes), Create(arrows), run_time=0.9)
        self.at("Good science")
        line = DashedLine([-5.5, 0.12, 0], [5.5, 0.12, 0], color=GOLD, stroke_width=5)
        line.layout_ok = True  # intentional boundary between observed traces and possible causes
        self.play(Create(line), Indicate(rule, color=GOLD), run_time=0.9)
        self.finish()


class S13End(EndCard):
    LINE = "When people change an ecosystem, populations may rise or fall."
