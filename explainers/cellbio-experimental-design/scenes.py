"""Before the Data Arrive — cell-biology experimental-design explainer.

COLOR MAP
  BLUE   cells and the physical dish
  GREEN  FUCCI-green / S-phase entry
  GOLD   decisions, tracked division, and locked design choices
  RED    starting cell state / a broken link
  TEAL   treatment and run 1
  PURPLE run 2
  ORANGE run 3
  GREY   shared predictions, barriers, axes, and de-emphasis

All cell-state drawings are explicitly schematic.  The SuperPlot uses the lesson's
three pairs of percentages and 200 binary observations per dish.
"""
import numpy as np
from bp_style import *  # noqa: F401,F403

PURPLE = "#B58CD9"
ORANGE = "#F29E4C"
RUNC = [TEAL, PURPLE, ORANGE]
CTRL = [20, 25, 15]
TRT = [34, 27, 28]


def arrow(a, b, color=TEXT, width=5, tip=0.22):
    return Arrow(a, b, buff=0.08, color=color, stroke_width=width,
                 tip_length=tip, max_tip_length_to_length_ratio=0.35)


def bench_mat():
    """The single carried bench world: broad enough to make the action fill the frame."""
    return RoundedRectangle(corner_radius=0.38, width=12.55, height=6.85,
                            stroke_color=GREY, stroke_width=3,
                            fill_color=BLUE, fill_opacity=0.15).set_z_index(-20)


def dish(center=(0, -0.15), width=8.7, height=4.7, color=GREY):
    d = RoundedRectangle(corner_radius=0.55, width=width, height=height,
                         stroke_color=color, stroke_width=5,
                         fill_color=BLUE, fill_opacity=0.045)
    return d.move_to([center[0], center[1], 0])


def cells_in_dish(center=(0, -0.15), cols=12, rows=5, width=7.6, height=3.6,
                  green_count=0, radius=0.095):
    """Deterministic epithelial-cell cartoons; green_count counts green nuclei."""
    out = VGroup()
    for i in range(cols * rows):
        c, r = i % cols, i // cols
        x = center[0] + (c - (cols - 1) / 2) * width / max(cols - 1, 1)
        y = center[1] + ((rows - 1) / 2 - r) * height / max(rows - 1, 1)
        body = Circle(radius=radius * 1.7, stroke_color=BLUE, stroke_width=2,
                      fill_color=BLUE, fill_opacity=0.13).move_to([x, y, 0])
        nucleus = Dot([x, y, 0], radius=radius,
                      color=GREEN if i < green_count else BLUE)
        out.add(VGroup(body, nucleus))
    return out


def cell_icon(color=RED, radius=0.34):
    body = Circle(radius=radius, stroke_color=BLUE, stroke_width=4,
                  fill_color=BLUE, fill_opacity=0.12)
    nucleus = Dot(radius=radius * 0.42, color=color)
    return VGroup(body, nucleus)


def daughters(scale=1.0):
    a = cell_icon(RED, 0.27).shift(LEFT * 0.38)
    b = cell_icon(RED, 0.27).shift(RIGHT * 0.38)
    return VGroup(a, b).scale(scale)


def stretch_arrows(y=-0.15, x=4.45):
    return VGroup(arrow([-x, y, 0], [-5.35, y, 0], TEXT, 6),
                  arrow([x, y, 0], [5.35, y, 0], TEXT, 6))


def gently_drift(mob, amplitude=0.09, speed=0.9, direction=RIGHT):
    """Keep a held diagram alive without changing any scientific position or label spacing."""
    mob.drift_clock = 0.0
    mob.drift_offset = 0.0

    def update(m, dt):
        m.drift_clock += dt
        offset = amplitude * np.sin(speed * m.drift_clock)
        m.shift(direction * (offset - m.drift_offset))
        m.drift_offset = offset

    mob.add_updater(update)
    return mob


def slot(label, width=3.7):
    box = RoundedRectangle(corner_radius=0.18, width=width, height=0.78,
                           stroke_color=GOLD, stroke_width=4,
                           fill_color=GOLD, fill_opacity=0.08)
    txt = T(label, 28, TEXT)
    return VGroup(box, txt.move_to(box))


def lock_icon(label, content=None, width=3.75):
    base = slot(label, width)
    shackle = Arc(radius=0.28, start_angle=0, angle=PI,
                  color=GOLD, stroke_width=5).rotate(PI).next_to(base, UP, buff=-0.02)
    g = VGroup(base, shackle)
    if content:
        badge = T(content, 28, GOLD).next_to(base, DOWN, buff=0.1)
        g.add(badge)
    return g


def branch_world():
    start = cell_icon(GREEN, 0.42).move_to([-4.4, 0, 0])
    fork = Dot([-2.9, 0, 0], radius=0.08, color=GOLD)
    top = VMobject(color=GREEN, stroke_width=6).set_points_smoothly([
        [-4.0, 0, 0], [-3.25, 0, 0], [-2.7, 0.35, 0], [-1.65, 1.65, 0], [0.4, 1.65, 0]])
    low = VMobject(color=GOLD, stroke_width=6).set_points_smoothly([
        [-4.0, 0, 0], [-3.25, 0, 0], [-2.7, -0.35, 0], [-1.65, -1.65, 0], [2.65, -1.65, 0]])
    camera = VGroup(Rectangle(width=1.2, height=0.78, color=GREEN, stroke_width=4),
                    Circle(radius=0.22, color=GREEN, stroke_width=3)).move_to([1.2, 1.65, 0])
    ds = daughters(1.25).move_to([3.7, -1.65, 0])
    q = T("Which observation separates the models?", 38, TEXT, weight=BOLD).move_to([0, 3.05, 0])
    schematic = T("schematic", 28, GREY).move_to([-5.15, -2.9, 0])
    return start, fork, top, low, camera, ds, q, schematic


def pipette(x=0, y=2.75, color=TEAL):
    barrel = RoundedRectangle(corner_radius=0.1, width=0.48, height=1.5,
                              stroke_color=color, stroke_width=4,
                              fill_color=color, fill_opacity=0.12).rotate(-0.28)
    barrel.move_to([x + 0.25, y, 0])
    drop = Dot([x, y - 1.05, 0], radius=0.13, color=color)
    return VGroup(barrel, drop)


class S01Hook(SpokenScene):
    def construct(self):
        self.add(bench_mat())
        d = dish()
        cs = cells_in_dish(green_count=0)
        gently_drift(cs, amplitude=0.16, speed=1.4)
        stretch = stretch_arrows()
        schematic = T("cell state · schematic", 28, GREY).move_to([0, -3.18, 0])
        self.play(FadeIn(d), FadeIn(cs), GrowFromCenter(stretch), FadeIn(schematic), run_time=1.05)

        self.at("or did the experiment")
        green_nuclei = VGroup(*[c[1] for c in cs[:22]])
        self.play(green_nuclei.animate.set_color(GREEN),
                  stretch.animate.scale(1.07), run_time=1.25)

        self.at("And how many experiments")
        qs = VGroup(*[T("?", 46, GOLD, weight=BOLD).move_to(p) for p in
                      [(-5.35, 2.2, 0), (5.35, 2.15, 0), (-5.15, -2.05, 0), (5.2, -2.1, 0)]])
        counter = M("0 cells", 44, TEXT).move_to([0, 3.05, 0])
        self.play(FadeIn(qs), FadeIn(counter), run_time=0.55)
        for n in (120, 300, 600):
            nxt = M(f"{n} cells", 44, TEXT).move_to(counter)
            self.play(Transform(counter, nxt), Rotate(qs, angle=0.16), run_time=0.38)

        self.at("inside one dish")
        one = VGroup(d.copy().scale(0.22).set_fill(BLUE, 0.08), T("one dish", 34, BLUE, weight=BOLD))
        one[1].next_to(one[0], DOWN, buff=0.18)
        one.move_to([0, 2.7, 0])
        self.play(ReplacementTransform(counter, one), qs.animate.rotate(0.22), run_time=0.9)

        self.at("Watch one bench")
        bench = Line([-6.1, -3.45, 0], [6.1, -3.45, 0], color=GREY, stroke_width=8)
        self.play(Create(bench), d.animate.set_stroke(BLUE, 6),
                  Rotate(qs, angle=0.2), run_time=1.1)
        self.finish()


class S02Title(TitleCard):
    LESSON = "Designing a cell biology experiment"
    TITLE = "Before the Data Arrive"

    def construct(self):
        self.add(bench_mat())
        d = dish(center=(0, -1.4), width=5.7, height=2.25).set_opacity(0.3)
        cs = cells_in_dish(center=(0, -1.4), cols=8, rows=3, width=4.8, height=1.45,
                           green_count=7, radius=0.075).set_opacity(0.3)
        title = T(self.TITLE, 52, TEXT, font=TITLE_FONT).move_to([0, 2.55, 0])
        slots = VGroup(slot("prediction"), slot("endpoint"), slot("independent unit"))
        slots.arrange(RIGHT, buff=0.35).move_to([0, 0.75, 0])
        self.add(d, cs)
        self.play(Write(title), LaggedStart(*[FadeIn(s, shift=UP * 0.12) for s in slots], lag_ratio=0.18), run_time=1.0)
        self.wait(0.35)
        self.play(FadeOut(title), run_time=0.45)
        self.finish()


class S03Models(SpokenScene):
    def model_card(self, which, x):
        box = RoundedRectangle(corner_radius=0.3, width=5.75, height=5.25,
                               stroke_color=BLUE, stroke_width=4, fill_color=BLUE, fill_opacity=0.04)
        box.move_to([x, -0.2, 0])
        head = T(f"MODEL {which}", 34, TEXT, weight=BOLD).move_to([x, 2.72, 0])
        red = cell_icon(RED).move_to([x - 1.8, 0.65, 0])
        green = cell_icon(GREEN).move_to([x, 0.65, 0])
        ds = daughters().move_to([x + 1.8, 0.65, 0])
        a1 = arrow([x - 1.3, 0.65, 0], [x - 0.55, 0.65, 0], GREEN)
        a2 = arrow([x + 0.55, 0.65, 0], [x + 1.2, 0.65, 0], GOLD)
        if which == "B":
            barrier = Rectangle(width=0.14, height=1.1, color=GREY, fill_opacity=1).move_to([x + 0.82, 0.65, 0])
            signal = chip("signal", GOLD, 28).move_to([x + 0.82, -0.45, 0])
            row = VGroup(red, a1, green, a2, barrier, signal, ds)
        else:
            row = VGroup(red, a1, green, a2, ds)
        return VGroup(box, head, row)

    def construct(self):
        self.add(bench_mat())
        d = dish(center=(0, -2.85), width=4.2, height=1.05).set_opacity(0.45)
        self.add(d)
        a = self.model_card("A", -3.15).shift(LEFT * 6)
        b = self.model_card("B", 3.15).shift(RIGHT * 6)
        self.play(a.animate.shift(RIGHT * 6), b.animate.shift(LEFT * 6), run_time=1.4)
        # The competing models remain active objects while each sentence lands.
        a.add_updater(lambda m, dt: m.shift(UP * 0.022 * dt))
        b.add_updater(lambda m, dt: m.shift(DOWN * 0.022 * dt))

        self.at("Model A says")
        self.play(Indicate(a[2][2], color=GREEN), GrowArrow(a[2][3]), run_time=1.2)
        self.at("Model B says")
        self.play(Indicate(b[2][2], color=GREEN), run_time=0.75)
        self.at("another signal")
        self.play(b[2][6].animate.shift(UP * 0.45), b[2][5].animate.set_opacity(0.25), run_time=1.0)
        self.play(GrowArrow(b[2][3]), b[2][6].animate.set_opacity(0.25), run_time=0.75)

        self.at("Both predict more green cells")
        glows = VGroup(a[2][2], b[2][2])
        self.play(glows.animate.scale(1.2), rate_func=there_and_back, run_time=1.0)
        self.at("The green snapshot")
        shared = chip("same green snapshot", GREY, 32).move_to([0, -2.65, 0])
        self.play(FadeOut(d), FadeOut(a[0]), FadeOut(b[0]), FadeIn(shared), run_time=0.9)
        self.finish()


class S04PredictionLock(SpokenScene):
    def construct(self):
        self.add(bench_mat())
        headings = VGroup(T("MODEL A", 30, TEXT), T("MODEL B", 30, TEXT)).arrange(RIGHT, buff=4.2).move_to([0, 2.95, 0])
        shared_lab = T("green cells", 34, GREY).move_to([-4.75, 1.25, 0])
        shared = VGroup(cell_icon(GREEN), cell_icon(GREEN)).arrange(RIGHT, buff=3.2).move_to([1.2, 1.25, 0])
        diff_lab = T("completed division", 38, GOLD, weight=BOLD).move_to([-4.3, -1.0, 0])
        diff = VGroup(daughters(1.2), VGroup(cell_icon(GREEN), Rectangle(width=0.16, height=1.15, color=GREY, fill_opacity=1)).arrange(RIGHT, buff=0.35))
        diff.arrange(RIGHT, buff=3.0).move_to([1.55, -1.0, 0])
        grid = VGroup(headings, shared_lab, shared, diff_lab, diff)
        gently_drift(shared, amplitude=0.08, speed=1.05, direction=UP)
        gently_drift(diff, amplitude=0.08, speed=0.9, direction=UP)
        self.play(FadeIn(grid), run_time=1.1)

        self.at("A shared prediction")
        self.play(VGroup(shared_lab, shared).animate.set_opacity(0.22), run_time=0.8)
        self.at("Here the disagreement")
        self.play(diff.animate.scale(1.15), diff_lab.animate.scale(1.04), run_time=1.0)

        self.at("The first gold lock")
        lock = lock_icon("prediction", "different result").move_to([0, 2.35, 0])
        self.play(FadeOut(headings), FadeOut(shared_lab), FadeOut(shared), run_time=0.4)
        self.play(VGroup(diff_lab, diff).animate.move_to([0, -0.7, 0]), FadeIn(lock), run_time=0.75)

        self.at("Write each model's numerical")
        blanks = VGroup(*[VGroup(T(n, 28, TEXT), RoundedRectangle(corner_radius=0.12, width=2.2, height=0.75,
                  color=GOLD, stroke_width=3)).arrange(RIGHT, buff=0.2) for n in ("A", "B")])
        blanks.arrange(RIGHT, buff=1.0).move_to([0, -2.65, 0])
        self.play(FadeOut(diff_lab), FadeOut(diff), LaggedStart(*[FadeIn(x) for x in blanks], lag_ratio=0.25),
                  run_time=1.15)
        self.finish()


class S05Predict(SpokenScene):
    def construct(self):
        self.add(bench_mat())
        start, fork, top, low, camera, ds, q, schematic = branch_world()
        self.play(FadeIn(start), FadeIn(q), FadeIn(schematic), run_time=0.7)
        self.play(Create(top), Create(low), FadeIn(fork), run_time=1.25)
        self.play(FadeIn(camera), FadeIn(ds), run_time=0.85)
        followers = VGroup()
        for path, color, phase in ((top, GREEN, 0.05), (top, GREEN, 0.55),
                                   (low, GOLD, 0.18), (low, GOLD, 0.68)):
            f = cell_icon(color, 0.18).move_to(path.point_from_proportion(phase))
            f.path, f.phase, f.clock = path, phase, 0.0
            def travel(m, dt):
                m.clock += dt
                m.move_to(m.path.point_from_proportion((m.phase + m.clock / 7.0) % 1.0))
            f.add_updater(travel)
            followers.add(f)
        self.add(followers)
        self.at("Both paths are real observations")
        self.play(Indicate(camera, color=GREEN), Indicate(ds, color=GOLD), run_time=1.05)
        self.at("but only one separates")
        self.play(start.animate.scale(1.12), rate_func=there_and_back, run_time=0.75)
        self.at("Is it more green cells")
        snap = T("green cells now", 32, GREEN).next_to(camera, DOWN, buff=0.22)
        self.play(FadeIn(snap), camera.animate.scale(1.12), rate_func=there_and_back, run_time=0.85)
        self.at("or more tracked divisions")
        track = T("tracked divisions later", 32, GOLD).next_to(ds, UP, buff=0.25)
        self.play(FadeIn(track), ds.animate.scale(1.15), rate_func=there_and_back, run_time=0.95)
        self.at("Hold your answer")
        self.play(MoveAlongPath(start, low.copy()), run_time=1.75, rate_func=linear)
        self.finish()


class S06Pause(Scene):
    def construct(self):
        self.add(bench_mat())
        start, fork, top, low, camera, ds, q, schematic = branch_world()
        snap = T("green cells now", 32, GREEN).next_to(camera, DOWN, buff=0.22)
        track = T("tracked divisions later", 32, GOLD).next_to(ds, UP, buff=0.25)
        movers = VGroup(cell_icon(GREEN, 0.25).move_to(top.get_start()),
                        cell_icon(GOLD, 0.25).move_to(low.get_start()))
        self.add(start, fork, top, low, camera, ds, q, schematic, snap, track, movers)
        self.play(MoveAlongPath(movers[0], top.copy()), MoveAlongPath(movers[1], low.copy()),
                  start.animate.scale(1.12), rate_func=linear, run_time=4.3)
        self.wait(0.2)


class S07EndpointReveal(SpokenScene):
    def construct(self):
        self.add(bench_mat())
        start, fork, top, low, camera, ds, q, schematic = branch_world()
        self.add(start, fork, top, low, camera, ds, q, schematic)
        reporter = VGroup(cell_icon(RED), arrow([-0.5, 0, 0], [0.5, 0, 0], GREEN), cell_icon(GREEN)).arrange(RIGHT, buff=0.5).scale(1.3)
        reporter.move_to([0, 1.25, 0])
        self.play(FadeOut(q), FadeOut(fork), FadeOut(top), FadeOut(low), FadeOut(camera), FadeOut(ds),
                  FadeOut(start), FadeIn(reporter), run_time=1.05)

        self.at("In its simplest picture")
        label = T("FUCCI · schematic", 34, TEXT, weight=BOLD).move_to([0, 3.05, 0])
        self.play(FadeIn(label), reporter[2].animate.scale(1.18), rate_func=there_and_back, run_time=0.8)
        self.at("green marks entry")
        entry = slot("S-phase entry", 3.4).move_to([2.8, -0.1, 0])
        self.play(FadeIn(entry), reporter[2].animate.move_to([0.6, -0.1, 0]), run_time=0.9)
        self.at("not completion")
        barrier = Rectangle(width=0.16, height=1.25, color=GREY, fill_opacity=1).move_to([4.85, -0.1, 0])
        self.play(FadeIn(barrier), entry.animate.set_stroke(GREY), run_time=0.75)

        self.at("The camera must follow")
        path = VMobject(color=GOLD, stroke_width=12).set_points_smoothly([
            [-4.8, -1.1, 0], [-2.5, -1.1, 0], [0, -1.1, 0], [2.7, -1.1, 0], [4.3, -1.1, 0]])
        tracked = cell_icon(RED, 0.52).move_to(path.get_start())
        cam = VGroup(Rectangle(width=1.4, height=0.95, color=GOLD, stroke_width=5), Circle(radius=0.28, color=GOLD)).move_to([-4.8, -2.65, 0])
        self.play(FadeOut(reporter), FadeOut(entry), FadeOut(barrier), FadeOut(schematic),
                  Create(path), FadeIn(tracked), FadeIn(cam), run_time=1.0)
        self.play(MoveAlongPath(tracked, path.copy()), cam.animate.shift(RIGHT * 4.6), run_time=2.2, rate_func=linear)

        self.at("Follow that cell")
        tracked_green = cell_icon(GREEN, 0.52).move_to([2.2, -1.1, 0])
        rounded = cell_icon(GREEN, 0.65).move_to([3.15, -1.1, 0])
        kids = daughters(1.65).move_to([4.3, -1.1, 0])
        self.play(Transform(tracked, tracked_green), run_time=0.55)
        self.play(Transform(tracked, rounded), run_time=0.55)
        self.play(ReplacementTransform(tracked, kids), run_time=0.85)

        self.at("For division claims")
        end = lock_icon("endpoint", "observed division").move_to([0, 2.5, 0])
        self.play(FadeOut(label), FadeOut(cam), FadeIn(end), kids.animate.set_color(GOLD), run_time=0.9)
        gently_drift(kids, amplitude=0.20, speed=1.5, direction=UP)
        self.at("track cells to division")
        self.play(ShowPassingFlash(path.copy().set_stroke(GOLD, 12), time_width=0.8),
                  kids.animate.scale(1.15), rate_func=there_and_back, run_time=1.3)
        self.finish()


class S08Unit(SpokenScene):
    def construct(self):
        self.add(bench_mat())
        d = dish(center=(0, -0.35), width=8.8, height=4.3, color=BLUE)
        cs = cells_in_dish(center=(0, -0.35), cols=12, rows=5, width=7.6, height=3.25,
                           green_count=18)
        gently_drift(cs, amplitude=0.10, speed=1.0)
        self.play(FadeIn(d), FadeIn(cs), run_time=1.0)
        self.at("Every cell here")
        pip = pipette(0, 3.0)
        stretch = stretch_arrows()
        self.play(FadeIn(pip), GrowFromCenter(stretch), run_time=1.0)
        self.at("one pipetting")
        drop = pip[1].copy()
        self.play(drop.animate.move_to([0, 1.45, 0]).scale(1.5), d.animate.set_fill(TEAL, 0.1), run_time=0.85)
        self.at("and one stretch")
        self.play(stretch.animate.scale(1.12), d.animate.stretch(1.05, 0), run_time=0.85)

        self.at("If the dish is odd")
        links = VGroup(*[Line(c.get_center(), d.get_center(), color=BLUE, stroke_width=1).set_opacity(0.22) for c in cs])
        self.play(Create(links), d.animate.set_stroke(RED, 6), run_time=1.05)
        self.at("every cell carries")
        self.play(VGroup(*[c[0] for c in cs]).animate.set_stroke(RED), run_time=0.85)

        self.at("When treatment is applied")
        counter = M("600 cells", 42, BLUE).move_to([0, 3.05, 0])
        token = VGroup(d.copy().scale(0.22).set_stroke(BLUE, 7), T("1 dish", 34, BLUE, weight=BOLD)).arrange(DOWN, buff=0.15).move_to([0, 2.85, 0])
        self.play(FadeOut(pip), FadeOut(drop), FadeOut(links), FadeIn(counter), run_time=0.55)
        self.play(ReplacementTransform(counter, token), run_time=0.9)
        self.at("the dish is the experimental")
        lock = lock_icon("independent unit", "dish").move_to([0, 2.75, 0])
        self.play(FadeOut(token), FadeIn(lock), d.animate.set_stroke(BLUE, 7), run_time=0.85)
        self.finish()


class S09Runs(SpokenScene):
    def construct(self):
        self.add(bench_mat())
        big = dish(width=7.0, height=3.7, color=BLUE)
        dots = cells_in_dish(cols=14, rows=6, width=5.9, height=2.8, green_count=22, radius=0.07)
        precision = M("200 cells", 42, BLUE).move_to([0, 2.75, 0])
        self.play(FadeIn(big), FadeIn(dots), FadeIn(precision), run_time=0.9)
        self.play(Transform(precision, M("600 cells", 42, BLUE).move_to(precision)), dots.animate.scale(1.03), run_time=0.8)
        self.at("but it does not repeat")
        one = chip("1 treatment", RED, 34).move_to([0, -2.75, 0])
        self.play(FadeIn(one), big.animate.set_stroke(RED, 6), run_time=0.85)

        self.at("Fresh runs do")
        self.play(FadeOut(big), FadeOut(dots), FadeOut(precision), FadeOut(one), run_time=0.45)
        columns = VGroup()
        for i, x in enumerate((-4.2, 0, 4.2)):
            head = T(f"day {i + 1}", 32, RUNC[i], weight=BOLD).move_to([x, 3.05, 0])
            ds = VGroup(dish((x, 1.1), 3.1, 1.45, RUNC[i]), dish((x, -1.05), 3.1, 1.45, RUNC[i]))
            labs = VGroup(T("control", 28, TEXT).move_to([x, 1.1, 0]), T("treated", 28, TEXT).move_to([x, -1.05, 0]))
            columns.add(VGroup(head, ds, labs))
        self.play(LaggedStart(*[FadeIn(c, shift=UP * 0.15) for c in columns], lag_ratio=0.25), run_time=1.4)

        self.at("A new day")
        pips = VGroup(*[pipette(x, 2.05, RUNC[i]).scale(0.65) for i, x in enumerate((-4.2, 0, 4.2))])
        self.play(LaggedStart(*[FadeIn(p) for p in pips], lag_ratio=0.2), run_time=1.1)
        self.at("run to run variation")
        summaries = VGroup()
        for i, x in enumerate((-4.2, 0, 4.2)):
            summaries.add(VGroup(Dot([x - 0.45, -2.35, 0], radius=0.22, color=RUNC[i]),
                                 Dot([x + 0.45, -2.35, 0], radius=0.22, color=RUNC[i])))
        self.play(FadeIn(summaries), columns[1].animate.set_opacity(0.5), run_time=0.85)
        self.play(columns[1].animate.set_opacity(1), run_time=0.45)

        self.at("Three separately treated")
        old = T("3 dishes × 200 cells", 32, BLUE).move_to([0, -3.05, 0])
        new = T("3 run summaries per condition", 34, GOLD, weight=BOLD).move_to(old)
        self.play(FadeIn(old), run_time=0.5)
        self.play(Transform(old, new), summaries.animate.scale(1.22), run_time=1.0)
        self.finish()


def superplot():
    xvals = [-3.4, 3.4]
    y0, y100 = -2.35, 2.35
    axes = VGroup(Line([-5.3, y0, 0], [-5.3, y100, 0], color=TEXT, stroke_width=4),
                  Line([-5.3, y0, 0], [5.6, y0, 0], color=TEXT, stroke_width=4))
    ticks = VGroup(M("0", 26, TEXT).move_to([-5.75, y0, 0]),
                   M("100", 26, TEXT).move_to([-5.78, y100, 0]))
    xlab = VGroup(T("control", 30, TEXT).move_to([xvals[0], -2.92, 0]),
                  T("treated", 30, TEXT).move_to([xvals[1], -2.92, 0]))
    ylabel = T("percent EdU-positive", 30, TEXT).rotate(PI / 2).move_to([-6.35, 0, 0])
    dots, means, joins = VGroup(), VGroup(), VGroup()
    for run, color in enumerate(RUNC):
        pair = []
        for cond, pct in enumerate((CTRL[run], TRT[run])):
            mx = xvals[cond] + (run - 1) * 0.42
            # Exactly 200 binary observations: EdU+ at 100%, EdU− at 0%.
            group = VGroup()
            for i in range(200):
                positive = i < 2 * pct
                xx = mx + ((i * 37) % 17 - 8) * 0.018
                yy = (y100 if positive else y0) + ((i * 19) % 13 - 6) * 0.018
                group.add(Dot([xx, yy, 0], radius=0.018, color=color).set_opacity(0.48))
            dots.add(group)
            my = y0 + (y100 - y0) * pct / 100
            mark = Dot([mx, my, 0], radius=0.15, color=color)
            means.add(mark)
            pair.append(mark.get_center())
        joins.add(Line(pair[0], pair[1], color=color, stroke_width=5))
    return axes, ticks, xlab, ylabel, dots, means, joins


class S10Superplot(SpokenScene):
    def construct(self):
        self.add(bench_mat())
        axes, ticks, xlab, ylabel, dots, means, joins = superplot()
        title = T("SuperPlot", 42, TEXT, weight=BOLD).move_to([0, 3.25, 0])
        self.add(title, axes, ticks, xlab, ylabel)
        self.play(ShowPassingFlash(axes.copy().set_stroke(GOLD, 10), time_width=0.35),
                  Indicate(title, color=TEXT, scale_factor=1.04), run_time=3.55)
        self.at("Small dots show cells")
        self.play(LaggedStart(*[FadeIn(g) for g in dots], lag_ratio=0.08), run_time=1.4)
        self.at("while large symbols")
        self.play(FadeIn(means), Create(joins), run_time=1.05)
        # All plotted marks breathe together, preserving their exact coordinates and pairings.
        for mob in (dots, means, joins):
            mob.sway_clock, mob.sway_offset = 0.0, 0.0
            def sway(m, dt):
                m.sway_clock += dt
                new_offset = 0.16 * np.sin(1.0 * m.sway_clock)
                m.shift(RIGHT * (new_offset - m.sway_offset))
                m.sway_offset = new_offset
            mob.add_updater(sway)
        self.at("Run 2 now")
        self.play(Indicate(joins[1], color=PURPLE, scale_factor=1.05),
                  VGroup(means[2], means[3]).animate.scale(1.35), run_time=1.15)
        flat = T("run 2: nearly flat", 30, PURPLE).move_to([0, 2.65, 0])
        self.play(FadeIn(flat), ShowPassingFlash(joins[1].copy().set_stroke(PURPLE, 11)), run_time=0.85)
        self.at("A SuperPlot keeps cell variation")
        self.play(dots.animate.set_opacity(0.75), run_time=0.85)
        self.at("comparing independent runs")
        self.play(LaggedStart(*[ShowPassingFlash(j.copy().set_stroke(RUNC[i], 10)) for i, j in enumerate(joins)], lag_ratio=0.2), run_time=1.25)
        self.finish()


class S11Rule(SpokenScene):
    def construct(self):
        self.add(bench_mat())
        locks = VGroup(lock_icon("prediction", "different outcomes"),
                       lock_icon("endpoint", "tracked division"),
                       lock_icon("independent unit", "dish summaries"))
        locks.arrange(RIGHT, buff=0.45).move_to([0, 2.25, 0])
        d = dish(center=(0, -1.3), width=6.8, height=2.0, color=BLUE)
        cs = cells_in_dish(center=(0, -1.3), cols=10, rows=3, width=5.7, height=1.35,
                           green_count=9, radius=0.08)
        self.play(FadeIn(d), FadeIn(cs), LaggedStart(*[FadeIn(l, shift=UP * 0.2) for l in locks], lag_ratio=0.18), run_time=1.25)
        cs.direction = 1
        def drift_cells(m, dt):
            m.shift(RIGHT * m.direction * 0.045 * dt)
            if abs(m.get_x()) > 0.42:
                m.direction *= -1
        cs.add_updater(drift_cells)
        self.at("In shared dish cell experiments")
        self.play(LaggedStart(*[Indicate(l, color=GOLD, scale_factor=1.04) for l in locks], lag_ratio=0.18), run_time=1.15)
        self.at("lock the prediction")
        self.play(locks[0].animate.set_fill(GOLD, 0.16), run_time=0.5)
        self.at("endpoint")
        self.play(locks[1].animate.set_fill(GOLD, 0.16), run_time=0.5)
        self.at("independent unit")
        self.play(locks[2].animate.set_fill(GOLD, 0.16), run_time=0.5)

        self.at("Break one link")
        links = VGroup(Line(locks[0].get_right(), locks[1].get_left(), color=GOLD, stroke_width=7),
                       Line(locks[1].get_right(), locks[2].get_left(), color=GOLD, stroke_width=7))
        self.play(Create(links), run_time=0.55)
        broken = VGroup(Line([-0.22, 0.22, 0], [0.22, -0.22, 0], color=RED, stroke_width=8),
                        Line([-0.22, -0.22, 0], [0.22, 0.22, 0], color=RED, stroke_width=8)).move_to(links[1])
        self.play(FadeOut(links[1]), FadeIn(broken), locks[2].animate.shift(RIGHT * 0.35), run_time=0.85)

        self.at("With all three aligned")
        self.play(FadeOut(broken), locks[2].animate.shift(LEFT * 0.35), Create(links[1]), run_time=0.8)
        claim = slot("claim", 3.0).move_to([0, -2.9, 0])
        beam = VMobject(color=GOLD, stroke_width=9).set_points_as_corners([
            locks[0].get_center(), locks[1].get_center(), locks[2].get_center(), claim.get_center()])
        self.play(ShowPassingFlash(beam, time_width=1.1), FadeIn(claim), run_time=1.35)
        self.at("the claim measurement")
        self.play(claim.animate.set_fill(TEXT, 0.15), cs.animate.shift(RIGHT * 0.08), run_time=0.75)
        self.at("answer the same question")
        self.play(Indicate(claim, color=TEXT, scale_factor=1.08), cs.animate.shift(LEFT * 0.08), run_time=0.85)

        self.at("Controls then test")
        control = chip("dull explanation?", GREY, 30).move_to([4.4, -1.55, 0])
        probe = arrow([3.25, -1.55, 0], [3.7, -1.55, 0], GREY)
        self.play(d.animate.shift(LEFT * 0.7), cs.animate.shift(LEFT * 0.7), FadeIn(control), GrowArrow(probe), run_time=1.0)
        self.finish()


class S12Return(SpokenScene):
    def construct(self):
        self.add(bench_mat())
        d = dish(width=8.8, height=4.45, color=BLUE)
        # 600 visible observation dots, with a deterministic green subset.
        dots = VGroup()
        for i in range(600):
            c, r = i % 30, i // 30
            x = (c - 14.5) * 0.275
            y = (9.5 - r) * 0.205 - 0.15
            dots.add(Dot([x, y, 0], radius=0.027, color=GREEN if i < 178 else BLUE).set_opacity(0.8))
        self.play(FadeIn(d), FadeIn(dots), run_time=1.25)
        self.at("600 glowing cells")
        count = M("600 observations", 40, TEXT).move_to([0, 3.1, 0])
        self.play(FadeIn(count), dots[:178].animate.scale(1.08), run_time=0.9)

        self.at("They are still one treated")
        bracket = VGroup(Line([-4.55, -2.72, 0], [4.55, -2.72, 0], color=BLUE, stroke_width=7),
                         Line([-4.55, -2.72, 0], [-4.55, -2.48, 0], color=BLUE, stroke_width=7),
                         Line([4.55, -2.72, 0], [4.55, -2.48, 0], color=BLUE, stroke_width=7),
                         T("ONE TREATED UNIT", 32, BLUE, weight=BOLD).move_to([0, -3.12, 0]))
        self.play(Create(bracket), run_time=1.0)
        self.at("and green still marks")
        phase = chip("S-phase entry", GREEN, 30).move_to([-4.85, 2.8, 0])
        self.play(FadeOut(count), FadeIn(phase), dots[:178].animate.set_opacity(1), run_time=0.85)

        self.at("More dots cannot repair")
        path = arrow([3.9, 1.25, 0], [5.05, 1.25, 0], GOLD, 6)
        kids = daughters(0.9).move_to([5.65, 1.25, 0])
        mismatch = T("endpoint", 28, GOLD).next_to(kids, DOWN, buff=0.15)
        self.play(GrowArrow(path), FadeIn(kids), FadeIn(mismatch), run_time=1.0)
        self.play(ShowPassingFlash(path.copy().set_stroke(RED, 11)), run_time=0.7)

        self.at("Trust the conclusion")
        locks = VGroup(lock_icon("prediction", width=3.3), lock_icon("endpoint", width=3.3), lock_icon("independent unit", width=3.3))
        locks.arrange(RIGHT, buff=0.35).scale(0.82).move_to([0, 2.85, 0])
        self.play(FadeOut(phase), FadeOut(path), FadeOut(kids), FadeOut(mismatch), FadeIn(locks), run_time=1.05)
        self.at("all three locks fit")
        checks = VGroup(*[T("✓", 42, GREEN, weight=BOLD).move_to(l) for l in locks])
        self.play(LaggedStart(*[FadeIn(c, scale=0.7) for c in checks], lag_ratio=0.2),
                  d.animate.set_stroke(GOLD, 7), run_time=1.35)
        self.finish()


class S13End(EndCard):
    LINE = "Lock prediction, endpoint, and independent unit before the data."

    def construct(self):
        hexm = hex_mascot(1.5)
        line = VGroup(T("Lock prediction, endpoint, and", 40, TEXT, font=TITLE_FONT),
                      T("independent unit before the data.", 40, TEXT, font=TITLE_FONT))
        line.arrange(DOWN, buff=0.16)
        sub = T("biochemistrypedia.com", 28, TEAL)
        g = VGroup(hexm, line, sub).arrange(DOWN, buff=0.38)
        self.play(FadeIn(hexm, shift=UP * 0.2), FadeIn(line, shift=UP * 0.15), run_time=self.beat(0.3))
        self.play(FadeIn(sub), run_time=self.beat(0.15))
        shoulder = hexm.arm.get_start()
        for angle in (0.28, -0.28, 0.22, -0.22):
            self.play(Rotate(hexm.arm, angle=angle, about_point=shoulder), run_time=self.beat(0.08))
        self.finish()
