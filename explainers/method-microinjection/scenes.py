"""Microinjection, nuclear transfer, and cell fusion on one schematic stage.

Color map from the methods films: blue glass, grey membranes, teal cytoplasm,
purple resident nuclei, orange introduced material, green controls and positive
outcomes, red unresolved interpretations, gold dates and questions. Yellow
marks the two observable fibroblast responses.
"""

from bp_parts import *


PURPLE = "#B58CD9"
ORANGE = "#F29E4C"
CELL_FILL = "#245B66"
SHARED_FILL = "#34727C"
STAGE_FILL = "#131D28"
HOME = (-1.2, -0.05)
RIGHT_CELL = (3.65, -0.05)
EGG = (-1.2, -0.05)
PAIR_Y = -0.04
QUESTION = "Did specialized nuclei lose developmental genes?"
QUESTION_STYLE = {"y": 3.28, "size": 34, "max_w": 11.8}
EGG_SITES = [(-3.65, 0.95), (-2.05, 0.95), (-0.45, 0.95),
             (-3.65, -1.00), (-2.05, -1.00), (-0.45, -1.00)]
SURVIVOR = (2.8, -0.16)


def xy(x, y):
    return np.array([x, y, 0.0])


def header(words, color=TEXT):
    return fit_text(words, size=39, min_size=30, max_w=11.75, color=color,
                    weight=BOLD).move_to(xy(0, 3.28))


def footer(words, color=TEXT):
    return caption(words, size=34, color=color, y=-3.29).shift(RIGHT * 0.9)


def stage(dish=False):
    if dish:
        return Ellipse(width=12.7, height=5.46, color="#344B5E", stroke_width=2.5,
                       fill_color=STAGE_FILL, fill_opacity=1).shift(DOWN * 0.05)
    return RoundedRectangle(width=13.2, height=5.54, corner_radius=0.55,
                            color="#344B5E", stroke_width=2.3,
                            fill_color=STAGE_FILL, fill_opacity=1)


def contour(rx, ry, pinched=0.0, phase=0.0, ruffles=0.0):
    """Schematic outline with an optional waist or a rippling upper edge."""
    angles = np.linspace(0, TAU, 101)
    points = []
    for a in angles:
        radial = 1 + 0.036 * np.sin(3 * a + 0.7) + 0.025 * np.cos(5 * a - 0.5)
        waist = 1 - pinched * np.exp(-14 * np.cos(a) ** 2)
        edge = ruffles * max(np.sin(a), 0) ** 2 * np.sin(20 * a - phase)
        points.append(xy(rx * (radial + edge) * np.cos(a),
                         ry * (radial + edge) * np.sin(a) * waist))
    return VMobject().set_points_smoothly(points)


def nucleus(radius, color=PURPLE, at=ORIGIN):
    core = Circle(radius=radius, color=color, stroke_width=2.6,
                  fill_color=interpolate_color(ManimColor(BG), ManimColor(color), 0.37),
                  fill_opacity=1)
    rim = Arc(radius=0.82 * radius, start_angle=0.42 * PI, angle=0.83 * PI,
              color=color, stroke_width=1.5).set_stroke(opacity=0.7)
    accent = Dot(xy(-0.24 * radius, 0.17 * radius), radius=radius * 0.18, color=color)
    return VGroup(core, rim, accent).move_to(at)


def cell_body(center, rx, ry, fill=CELL_FILL, rim=GREY, waist=0.0, ruffles=0.0):
    outline = contour(rx, ry, pinched=waist, ruffles=ruffles)
    outline.set_fill(fill, opacity=1).set_stroke(rim, width=3.1)
    return outline.shift(xy(*center))


def cytoplasm(center, rx, ry, seed=8, waist=0.0, animate=True, color=TEAL):
    """Soft, moving cytoplasmic granules confined to the cell interior."""
    rng = np.random.default_rng(seed)
    group = VGroup()
    for index in range(17):
        a = index * TAU / 17 + rng.uniform(-0.13, 0.13)
        r = rng.uniform(0.54, 0.80)
        p = xy(rx * r * np.cos(a), ry * r * np.sin(a) * (1 - waist * 0.65))
        granule = Ellipse(width=rx * rng.uniform(0.18, 0.29),
                          height=ry * rng.uniform(0.085, 0.13),
                          color=color, stroke_width=0, fill_opacity=0.78)
        granule.rotate(a + PI / 2).move_to(xy(*center) + p)
        if animate:
            bob(granule, amp=ry * rng.uniform(0.045, 0.093),
                speed=rng.uniform(2.0, 3.25), seed=index)
        group.add(granule)
    return group


def cell(center=HOME, rx=2.73, ry=2.43, core=PURPLE, fill=CELL_FILL,
         active=True, seed=8, animate=True):
    rim = GREY if active else "#556374"
    membrane = cell_body(center, rx, ry, fill=fill, rim=rim)
    grains = cytoplasm(center, rx, ry, seed, animate=animate,
                       color=TEAL if active else "#3A5967")
    parts = [membrane, grains]
    if core is not None:
        parts.append(nucleus(ry * 0.34, core,
                             xy(center[0] - 0.20 * rx, center[1] + 0.08 * ry)))
    return VGroup(*parts)


def injection_cells():
    return cell(), cell(RIGHT_CELL, 1.52, 1.55, active=False, fill="#294754", seed=4)


def dye_swirl(center=HOME, rx=2.73, ry=2.43):
    layers = VGroup()
    for i in range(5):
        a = TAU * (i + 0.12) / 5
        haze = Ellipse(width=rx * 0.72, height=ry * 0.59, stroke_width=0,
                       fill_color=GREEN, fill_opacity=0.13)
        haze.rotate(a).move_to(xy(center[0] + rx * 0.37 * np.cos(a),
                                 center[1] + ry * 0.37 * np.sin(a)))
        layers.add(bob(haze, amp=0.14, speed=1.75, seed=i))
    return layers


def needle(tip, length=3.03, angle=0):
    outline = Polygon(ORIGIN, xy(0.63, 0.19), xy(length, 0.40),
                      xy(length, -0.40), xy(0.63, -0.19),
                      color=BLUE, stroke_width=2.4, fill_color=BLUE, fill_opacity=0.16)
    seam = Line(xy(length - 0.24, 0.36), xy(length - 0.24, -0.36),
                color=BLUE, stroke_width=1.8)
    return VGroup(outline, seam).rotate(angle, about_point=ORIGIN).shift(xy(*tip))


def fusion_pair(x=0, y=PAIR_Y, scale=1.0, colors=(PURPLE, ORANGE), animate=True):
    return VGroup(
        cell((x - 1.43 * scale, y), 1.27 * scale, 2.04 * scale,
             core=colors[0], seed=11, animate=animate),
        cell((x + 1.43 * scale, y), 1.27 * scale, 2.04 * scale,
             core=colors[1], seed=16, animate=animate),
    )


def fused_cell(x=0, y=PAIR_Y, scale=1.0, colors=(PURPLE, ORANGE), animate=True):
    center = (x, y)
    body = cell_body(center, 2.70 * scale, 2.15 * scale, waist=0.21)
    grains = cytoplasm(center, 2.70 * scale, 2.15 * scale, 13, 0.21, animate)
    left = nucleus(0.68 * scale, colors[0], xy(x - 1.03 * scale, y + 0.19 * scale))
    right = nucleus(0.68 * scale, colors[1], xy(x + 1.03 * scale, y + 0.19 * scale))
    return VGroup(body, grains, left, right)


def merge_cells(scene, pair, fused, duration=1.85):
    """Bring the membranes together, then merge the two interiors."""
    for partner in pair:
        partner[1].clear_updaters(recursive=True)
    scene.play(pair[0].animate.shift(RIGHT * pair.width * 0.056),
               pair[1].animate.shift(LEFT * pair.width * 0.056), run_time=duration * 0.45)
    scene.play(ReplacementTransform(pair, fused), run_time=duration * 0.55)


def tadpole(center=SURVIVOR, scale=1.0, animate=False):
    head = Ellipse(width=2.06, height=1.58, color=GREEN, stroke_width=3.1,
                   fill_color="#3A694C", fill_opacity=1).shift(RIGHT * 0.47)
    tail = VMobject().set_points_smoothly([
        xy(0, 0.46), xy(-0.82, 0.32), xy(-1.75, 0.57), xy(-2.54, 0.16),
        xy(-1.76, 0.20), xy(-0.96, -0.30), xy(0, -0.43), xy(0, 0.46),
    ]).set_fill("#3A694C", 1).set_stroke(GREEN, 2.7)
    eye = Dot(xy(1.08, 0.24), radius=0.12, color=TEXT)
    mouth = Arc(radius=0.24, start_angle=-0.7, angle=1.05, color=GREEN,
                stroke_width=2.4).shift(xy(1.23, -0.23))
    animal = VGroup(tail, head, eye, mouth).scale(scale, about_point=ORIGIN).shift(xy(*center))
    if animate:
        swim_tadpole(animal, center, scale)
    return animal


def swim_tadpole(animal, center=SURVIVOR, scale=1.0, trace=None):
    tail = animal[0]
    rest = tail.get_points().copy()
    curves = [(tail, rest)]
    if trace is not None:
        animal.add(trace)
        curves.append((trace, trace.get_points().copy()))
    waves = []
    for curve, points in curves:
        x = (points[:, 0] - center[0]) / scale
        weight = np.clip(-x / 2.54, 0, 1) ** 1.5
        waves.append((curve, points, x, weight))

    def swim(mob, dt):
        mob.phase += dt * 4.4
        # The tail root has zero wave displacement and follows the animal's bob.
        offset = mob.get_points()[0] - rest[0]
        for curve, points, x, weight in waves:
            moved = points + offset
            moved[:, 1] += 0.42 * scale * weight * np.sin(mob.phase - 2 * x)
            curve.set_points(moved)

    tail.phase = 0.0
    tail.add_updater(swim)
    bob(animal, amp=0.23 * scale, speed=2.5)


def stalled_egg(center):
    return cell(center, 0.70, 0.75, core=None, fill="#263E4A", active=False, animate=False)


def prediction_dish(animate=False):
    eggs = VGroup(*[stalled_egg(p) for p in EGG_SITES])
    animal = tadpole(animate=animate)
    return VGroup(eggs, animal)


def prediction_question():
    return question_card(QUESTION, **QUESTION_STYLE)


def take_home():
    return footer("Put a part inside to test cause", GOLD)


class S01Hook(SpokenScene):
    def construct(self):
        main, other = injection_cells()
        opening = question_card("How do you test what drives a cell from inside?",
                                y=3.28, size=39, max_w=11.85)
        self.add(stage(), main, other, opening)
        self.at("watching from outside")
        outside = VGroup(*[Arc(radius=1.0 + i * 0.22, start_angle=0.74 * PI,
                              angle=0.51 * PI, color=GREY, stroke_width=3)
                           .shift(xy(-3.85, 0.11)) for i in range(3)])
        self.play(LaggedStart(*[Create(a) for a in outside], lag_ratio=0.35),
                  run_time=1.35)
        self.at("events happening together")
        self.play(FadeOut(outside, shift=LEFT * 0.28), run_time=1.65)
        self.at("to test cause directly")
        glass = needle((2.18, 1.58), length=3.7, angle=0.19)
        self.play(FadeOut(opening), FadeIn(glass, shift=RIGHT * 0.62), run_time=1.35)
        self.at("place a molecule")
        payload = Dot(xy(2.86, 1.72), radius=0.125, color=ORANGE)
        self.play(GrowFromCenter(payload), run_time=0.4)
        self.at("nucleus or")
        donor = nucleus(0.17, ORANGE, xy(2.93, 1.72))
        self.play(ReplacementTransform(payload, donor), run_time=0.44)
        self.at("or cytoplasm")
        self.play(FadeOut(donor), other[0].animate.set_fill(SHARED_FILL),
                  other[1].animate.set_fill(TEAL),
                  run_time=0.52)
        self.at("straight inside")
        self.play(glass.animate.shift(LEFT * 1.62 + DOWN * 0.31), run_time=0.72)
        self.play(FadeOut(glass), other[0].animate.set_fill("#294754"),
                  other[1].animate.set_fill("#3A5967"), run_time=0.56)
        self.finish()


class S02Title(TitleCard):
    TITLE = "Reaching Inside One Living Cell"
    LESSON = "Microinjection, nuclear transfer and cell fusion"

    def construct(self):
        self.add(stage(), *injection_cells())
        title = fit_text(self.TITLE, max_w=11.9, size=46, min_size=34,
                         font=TITLE_FONT).move_to(xy(0, 3.27))
        lesson = footer(self.LESSON, GOLD)
        self.play(FadeIn(title), FadeIn(lesson), run_time=0.40)
        self.wait(1.20)
        self.play(FadeOut(title), FadeOut(lesson), run_time=0.40)


class S03Microinjection(SpokenScene):
    def construct(self):
        main, other = injection_cells()
        self.add(stage(), main, other)
        self.at("start with microinjection")
        glass = needle((2.15, 1.59), length=3.9, angle=0.18)
        self.play(FadeIn(glass, shift=RIGHT * 0.8), run_time=0.65)
        title = header("Microinjection")
        self.play(FadeIn(title), run_time=0.4)
        self.at("a fine glass needle")
        self.play(glass.animate.shift(xy(-1.74, -0.31)), run_time=2.35)
        self.at("placing a molecule")
        tip = xy(0.41, 1.28)
        dots = VGroup(*[Dot(tip, radius=0.071, color=ORANGE) for _ in range(9)])
        destinations = [(0.85, 0.85), (0.52, 1.26), (0.05, 1.48), (0.26, 0.97),
                        (0.80, 0.43), (0.40, 0.14), (0.86, -0.12), (0.10, 0.58),
                        (0.14, -0.47)]
        self.add(dots)
        self.play(*[d.animate.move_to(xy(*p)) for d, p in zip(dots, destinations)],
                  run_time=2.05)
        for i, dot in enumerate(dots):
            bob(dot, amp=0.14, speed=2.45, seed=i)
        cyt = footer("Delivery into cytoplasm", TEAL)
        self.play(FadeIn(cyt), run_time=0.4)
        self.at("that skips the steps")
        outside = VGroup(*[Dot(xy(-4.22 - i * 0.30, 0.76 + i * 0.19),
                                radius=0.12, color=GREY) for i in range(4)])
        self.play(FadeOut(glass, shift=RIGHT * 1.2), FadeIn(outside), run_time=0.8)
        self.play(outside.animate.set_opacity(0.26), run_time=1.22)
        self.at("what that molecule does")
        self.play(FadeOut(cyt), run_time=0.55)
        self.at("a marker dye")
        dye = dye_swirl()
        dye.set_z_index(1)
        main[2].set_z_index(2)
        dots.set_z_index(3)
        self.play(FadeOut(outside),
                  LaggedStart(*[FadeIn(m, scale=0.55) for m in dye], lag_ratio=0.18),
                  run_time=2.0)
        label = footer("Dye marks the injected cell", GREEN)
        self.play(FadeIn(label), run_time=0.43)
        self.at("every injected cell")
        self.play(FadeOut(dots), run_time=0.75)
        self.finish()


class S04TransferFusion(SpokenScene):
    def construct(self):
        main, other = injection_cells()
        dye = dye_swirl().set_z_index(1)
        main[2].set_z_index(2)
        self.add(stage(), main, other, dye)
        self.at("other questions need")
        egg = cell(EGG, 2.62, 2.49)
        main[1].clear_updaters(recursive=True)
        self.play(ReplacementTransform(main, egg), FadeOut(other), FadeOut(dye), run_time=2.3)
        self.at("in nuclear transfer")
        title = header("Nuclear transfer")
        self.play(FadeIn(title), run_time=0.48)
        self.at("remove or destroy")
        self.play(FadeOut(egg[2], scale=0.3), run_time=1.68)
        self.at("place another")
        donor = nucleus(0.83, ORANGE, xy(2.81, 0.13))
        glass = needle((3.3, 0.13), length=2.75)
        self.play(FadeIn(donor), FadeIn(glass), run_time=0.42)
        self.play(donor.animate.move_to(xy(-1.72, 0.15)),
                  glass.animate.shift(LEFT * 4.25), run_time=2.02)
        self.at("in cell fusion")
        egg[1].clear_updaters(recursive=True)
        pair = fusion_pair()
        self.play(FadeOut(title), FadeOut(donor), FadeOut(glass),
                  ReplacementTransform(egg, pair), run_time=1.0)
        title = header("Cell fusion")
        self.play(FadeIn(title), run_time=0.34)
        self.at("merge two cells")
        fused = fused_cell()
        merge_cells(self, pair, fused)
        shared = footer("Two nuclei share one cytoplasm", TEAL)
        self.play(FadeIn(shared), run_time=0.46)
        self.at("all three share")
        self.play(swap(shared, take_home()), FadeOut(title), run_time=0.9)
        self.at("put a part inside")
        self.play(fused[0].animate.set_fill(SHARED_FILL), run_time=1.7)
        self.finish()


class S05PredictQ(SpokenScene):
    def construct(self):
        slide, fused, rule = stage(), fused_cell(), take_home()
        fused[0].set_fill(SHARED_FILL)
        self.add(slide, fused, rule)
        self.at("now test how")
        dish = stage(dish=True)
        targets = VGroup(*[cell(p, 0.70, 0.75, core=None) for p in EGG_SITES])
        live_egg = cell(SURVIVOR, 1.55, 1.69, core=None)
        self.play(ReplacementTransform(slide, dish), FadeOut(fused), FadeOut(rule),
                  run_time=0.75)
        self.play(FadeIn(targets), FadeIn(live_egg, scale=0.84),
                  FadeIn(scope_tag(size=28)), run_time=1.65)
        self.at("tadpole gut nucleus")
        donor = nucleus(0.44, ORANGE, xy(4.95, 1.12))
        self.play(FadeIn(donor), run_time=0.48)
        label = header("Tadpole gut nucleus", ORANGE)
        self.play(FadeIn(label), run_time=0.44)
        self.at("into an egg")
        self.play(donor.animate.move_to(xy(2.42, -0.02)), run_time=2.13)
        self.at("was destroyed")
        self.play(FadeOut(label), run_time=0.6)
        self.at("most eggs fail")
        eggs, _ = prediction_dish()
        targets.clear_updaters(recursive=True)
        self.play(ReplacementTransform(targets, eggs), run_time=1.67)
        self.at("a small fraction")
        animal = tadpole()
        live_egg.clear_updaters(recursive=True)
        self.play(FadeOut(donor), ReplacementTransform(live_egg, animal), run_time=2.15)
        swim_tadpole(animal)
        self.at("do those failures show")
        self.play(FadeIn(prediction_question()), run_time=0.62)
        self.at("genes", lead=-0.20)
        animal.clear_updaters(recursive=True)
        self.play(Transform(animal, tadpole()), run_time=0.62)
        self.finish()


class S06PredictPause(PredictPause):
    QUESTION = QUESTION
    CARD = QUESTION_STYLE
    SECONDS = 4.5

    def backdrop(self):
        return VGroup(stage(dish=True), prediction_dish())

    def construct(self):
        self.add(self.backdrop(), prediction_question(), scope_tag(size=28))
        left, right = xy(-3.47, -3.28), xy(3.47, -3.28)
        track = Line(left, right, color=GREY, stroke_width=13).set_stroke(opacity=0.34)
        elapsed = Line(left, right, color=GOLD, stroke_width=13)
        self.add(track)
        self.play(Create(elapsed), run_time=self.SECONDS, rate_func=linear)


class S07ControlsTransfer(SpokenScene):
    def construct(self):
        eggs, animal = prediction_dish(animate=True)
        question = prediction_question()
        self.add(stage(dish=True), eggs, animal, question, scope_tag(size=28))
        self.at("now")
        answer = header("Failures alone cannot tell us", RED)
        self.play(swap(question, answer), run_time=0.86)
        self.at("failures alone")
        self.play(eggs.animate.set_opacity(0.59), run_time=2.3)
        self.at("each normal tadpole")
        survivor = header("A normal tadpole", GREEN)
        self.play(swap(answer, survivor), animal[1].animate.set_fill("#4B8159"),
                  run_time=0.76)
        self.at("specialized nucleus")
        origin = nucleus(0.53, ORANGE, xy(4.57, 1.18))
        self.play(FadeIn(origin, scale=0.65), run_time=0.75)
        self.at("kept the needed instructions")
        retained = footer("The nucleus kept the instructions", ORANGE)
        self.play(FadeIn(retained), run_time=0.55)
        self.at("egg cytoplasm")
        read = footer("Egg cytoplasm could read them", TEAL)
        self.play(swap(retained, read), run_time=0.78)
        self.at("genetic nuclear marker")
        marker = Circle(radius=0.15, stroke_color=GREEN, stroke_width=4).move_to(xy(4.70, 1.03))
        marked = header("Donor genetic marker", GREEN)
        self.play(Create(marker), swap(survivor, marked), FadeOut(read), run_time=0.86)
        self.at("rules out a surviving")
        egg_core = nucleus(0.40, PURPLE, xy(4.35, -1.25))
        self.play(FadeIn(egg_core), run_time=0.40)
        self.play(FadeOut(egg_core, scale=0.2), run_time=1.16)
        self.at("still low success")
        doubt = header("Could rare unspecialized cells explain success?", RED)
        self.play(swap(marked, doubt), FadeOut(origin), FadeOut(marker), run_time=0.97)
        self.finish()


class S08ControlsFusion(SpokenScene):
    def construct(self):
        slide = stage()
        pair = fusion_pair(colors=(PURPLE, PURPLE), animate=True)
        self.add(slide, pair)
        self.at("cell fusion needs")
        title = header("Cell fusion controls")
        self.play(FadeIn(title), run_time=0.48)
        self.at("merging cells might")
        self.play(pair[0][0].animate.set_stroke(BLUE, width=4.2),
                  pair[1][0].animate.set_stroke(BLUE, width=4.2), run_time=1.55)
        alert = footer("Fusion can change the response", RED)
        self.play(FadeIn(alert), run_time=0.43)
        self.at("one partner with")
        resident = pair[1][2]
        dye_color = GREEN
        self.play(Transform(resident, nucleus(0.69, dye_color, resident.get_center())),
                  FadeOut(alert), run_time=0.71)
        dye_label = footer("Nuclear dye identifies one partner", GREEN)
        self.play(FadeIn(dye_label), run_time=0.54)
        self.at("identifies every nucleus")
        fused = fused_cell(colors=(PURPLE, dye_color))
        merge_cells(self, pair, fused)
        self.at("same phase fusions")
        comparison = fused_cell(-4.25, -0.08, 0.64, (PURPLE, PURPLE))
        for m in fused[1]:
            m.clear_updaters()
        moved = fused_cell(0, -0.08, 0.72, (PURPLE, dye_color))
        self.play(ReplacementTransform(fused, moved), FadeOut(dye_label), run_time=0.63)
        self.play(FadeIn(comparison), run_time=0.56)
        same = T("Same phase", 30, TEXT).move_to(xy(-4.25, -2.17))
        self.play(FadeIn(same), run_time=0.30)
        self.at("unfused neighbors")
        neighbour = cell((4.45, -0.08), 1.38, 1.48)
        self.play(FadeIn(neighbour), run_time=0.57)
        self.play(FadeIn(T("Unfused", 30, TEXT).move_to(xy(4.45, -2.17))),
                  FadeIn(T("Mixed phases", 30, TEXT).move_to(xy(0, -2.17))), run_time=0.51)
        self.at("whether fusion itself")
        self.play(FadeIn(footer("Compare on the same slide", GREEN)), run_time=0.52)
        self.finish()


class S09UnlockedGurdon(SpokenScene):
    def construct(self):
        self.add(stage())
        egg = cell((2.12, 0), 2.14, 2.38, core=None, seed=18)
        source = tadpole((-3.1, 0.18), scale=0.98)
        self.at("with controls in place")
        self.play(FadeIn(source), run_time=1.1)
        swim_tadpole(source, (-3.1, 0.18), 0.98)
        self.play(FadeIn(egg, scale=0.82), run_time=1.3)
        self.at("1962")
        title = header("1962 — John Gurdon", GOLD)
        self.play(FadeIn(title), run_time=0.64)
        self.at("tadpole intestinal nuclei")
        gut = VMobject().set_points_smoothly([
            xy(-3.46, 0.20), xy(-3.16, -0.15), xy(-2.84, -0.04),
            xy(-2.60, -0.28), xy(-2.32, -0.14),
        ]).set_stroke(ORANGE, 4.2)
        donor = nucleus(0.39, ORANGE, xy(-2.73, -0.01))
        self.play(Create(gut), run_time=0.53)
        self.play(FadeIn(donor, scale=0.5), run_time=0.53)
        self.at("frog eggs lacking")
        self.play(donor.animate.move_to(xy(1.66, 0.19)), FadeOut(gut), run_time=1.94)
        self.at("a small fraction")
        self.play(FadeOut(source), run_time=0.66)
        egg[1].clear_updaters(recursive=True)
        result_center, result_scale = (1.42, 0.20), 1.62
        result = tadpole(result_center, scale=result_scale)
        self.play(FadeOut(donor), ReplacementTransform(egg, result), run_time=1.78)
        nerve = VMobject().set_points_smoothly([
            xy(-2.32, 0.23), xy(-1.76, 0.38), xy(-0.96, 0.03),
            xy(0, 0.04), xy(0.49, 0.29), xy(0.58, 0.43),
        ]).scale(result_scale, about_point=ORIGIN).shift(xy(*result_center))
        nerve.set_stroke(YELLOW, width=5, opacity=0)
        swim_tadpole(result, result_center, result_scale, trace=nerve)
        food = VGroup(Dot(xy(4.40, -0.28), radius=0.072, color=GREY),
                      Dot(xy(4.23, -0.29), radius=0.062, color=GREY))
        self.play(FadeIn(food), run_time=0.2)
        self.play(FadeOut(food, shift=LEFT * 0.70), run_time=0.58)
        self.at("nervous system")
        self.play(nerve.animate.set_stroke(opacity=1), run_time=1.03)
        pulse(nerve, base=5, amp=1.7, speed=2.7)
        self.at("the gut cell nucleus")
        self.play(FadeIn(footer("Instructions for a whole animal", ORANGE)), run_time=0.68)
        self.finish()


def copying_glow(core):
    center = core[0].get_center()
    radius = core[0].width / 2
    rings = VGroup(*[
        Arc(radius=radius * factor, start_angle=start, angle=angle,
            color=TEAL, stroke_width=4.2).shift(center)
        for factor, start, angle in [(0.70, -0.78, 2.10), (0.51, 2.12, 2.19),
                                      (0.36, 4.44, 1.93)]
    ])
    for arc in rings:
        arc.add_updater(lambda m, dt: m.rotate(1.65 * dt, about_point=center))
    return rings


class S10UnlockedRao(SpokenScene):
    def construct(self):
        self.add(stage())
        left_x, right_x, scale = -3.34, 3.34, 0.97
        colors = (TEAL, PURPLE)
        left = fusion_pair(left_x, scale=scale, colors=colors)
        right = fusion_pair(right_x, scale=scale, colors=colors)
        self.add(left, right)
        self.at("in 1970")
        self.play(FadeIn(header("1970 — Rao and Johnson", GOLD)), run_time=0.65)
        self.at("johnson fused cultured")
        a = fused_cell(left_x, scale=scale, colors=colors)
        b = fused_cell(right_x, scale=scale, colors=colors)
        for pair in (left, right):
            for partner in pair:
                partner[1].clear_updaters(recursive=True)
        self.play(*[pair[0].animate.shift(RIGHT * 0.28) for pair in (left, right)],
                  *[pair[1].animate.shift(LEFT * 0.28) for pair in (left, right)],
                  run_time=1.72)
        self.play(ReplacementTransform(left, a), ReplacementTransform(right, b), run_time=1.66)
        self.at("beside an")
        self.play(FadeIn(T("S phase", 30, TEAL).move_to(xy(-4.34, -2.37))),
                  FadeIn(T("S phase", 30, TEAL).move_to(xy(2.34, -2.37))), run_time=0.46)
        self.at("copying dna")
        copy_a, copy_b = copying_glow(a[2]), copying_glow(b[2])
        self.play(FadeIn(copy_a), FadeIn(copy_b), run_time=0.65)
        self.at("g1 nucleus")
        self.play(FadeIn(T("G1", 32, PURPLE).move_to(xy(-2.34, -2.37))), run_time=0.49)
        self.at("started replicating")
        copying = copying_glow(a[3])
        early = T("Starts copying", 32, GREEN, weight=BOLD).move_to(xy(-3.34, -3.31))
        self.play(FadeIn(copying), run_time=0.78)
        self.play(FadeIn(early), run_time=0.45)
        self.at("copied g2")
        self.play(FadeIn(T("G2", 32, PURPLE).move_to(xy(4.34, -2.37))), run_time=0.48)
        quiet = T("Already copied", 32, TEXT, weight=BOLD).move_to(xy(3.34, -3.31))
        self.play(FadeIn(quiet), run_time=0.51)
        self.at("cytoplasm can start")
        self.play(a[0].animate.set_stroke(TEAL, width=4.6), run_time=1.3)
        self.at("a replicated nucleus")
        no_repeat = T("No new replication", 32, TEXT, weight=BOLD).move_to(xy(3.34, -3.31))
        self.play(swap(quiet, no_repeat), run_time=0.85)
        self.finish()


def fibroblast(center):
    return cell(center, 2.56, 1.89, seed=13)


def actin_cables(center):
    cables = VGroup()
    for x, y, width in [(-0.12, -0.65, 1.76), (0.02, -0.91, 1.61),
                        (0.05, -1.17, 1.30), (0.06, 1.11, 1.23), (0.30, 0.88, 1.45)]:
        cable = ArcBetweenPoints(xy(center[0] + x - width, center[1] + y - 0.21),
                                 xy(center[0] + x + width, center[1] + y + 0.21),
                                 angle=0.16).set_stroke(YELLOW, 4.6)
        cables.add(cable)
    return cables


class S11UnlockedRidley(SpokenScene):
    def construct(self):
        self.add(stage())
        one, two = (-3.16, -0.40), (3.16, -0.40)
        left, right = fibroblast(one), fibroblast(two)
        self.add(left, right)
        self.at("in 1992")
        title = header("1992 — Ridley and Hall", GOLD)
        self.play(FadeIn(title), run_time=0.66)
        self.at("injected purified proteins")
        pipettes = VGroup(needle((-2.38, 1.14), length=1.42, angle=1.04),
                          needle((3.94, 1.14), length=1.42, angle=1.04))
        self.play(FadeIn(pipettes, shift=UP * 0.30), run_time=1.08)
        self.play(pipettes.animate.shift(xy(-0.38, -0.56)), run_time=1.72)
        drops = VGroup(Dot(xy(-2.81, 0.47), radius=0.116, color=ORANGE),
                       Dot(xy(3.51, 0.47), radius=0.116, color=ORANGE))
        self.play(FadeIn(drops), run_time=0.56)
        self.at("those cells start")
        self.play(FadeOut(pipettes, shift=UP * 0.44), run_time=1.06)
        baseline = footer("Few stress fibres")
        self.play(FadeIn(baseline), run_time=0.5)
        self.at("active row filled")
        self.play(FadeOut(baseline), run_time=0.36)
        rho = T("Active Rho", 33, ORANGE, weight=BOLD).move_to(xy(-3.16, -3.30))
        cables = actin_cables(one)
        self.play(FadeIn(rho), FadeOut(drops[0]), run_time=0.43)
        self.play(LaggedStart(*[Create(c) for c in cables], lag_ratio=0.21), run_time=1.85)
        self.at("active rack made")
        rac = T("Active Rac", 33, ORANGE, weight=BOLD).move_to(xy(3.16, -3.30))
        self.play(FadeIn(rac), FadeOut(drops[1]), run_time=0.41)
        edge = right[0]
        self.play(Transform(edge, cell_body(two, 2.56, 1.89, rim=YELLOW, ruffles=0.12)),
                  run_time=1.44)

        def ripple(m, dt):
            m.phase += dt * 4.3
            m.set_points(contour(2.56, 1.89, phase=m.phase, ruffles=0.12)
                         .shift(xy(*two)).get_points())

        edge.phase = 0.0
        edge.add_updater(ripple)
        for cable in cables:
            pulse(cable, base=4.6, amp=1.4, speed=2.9)
        self.at("putting molecules")
        self.play(FadeOut(title), run_time=0.5)
        self.at("shows what controls")
        self.play(FadeIn(header("Put a part inside to test cause", GOLD)), run_time=0.64)
        self.finish()


class S12End(EndCard):
    LINE = "Move molecules, nuclei, or cytoplasm into living cells to test cause."
